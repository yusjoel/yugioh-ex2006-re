# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleHiddenFuncs.py  (Jython 2.7 / Ghidra 12.x)
#
# 读取 temp/hidden_thumb_func_candidates.csv (由 tools/ad-hoc/scan_hidden_thumb_funcs.py
# 生成), 对每个候选函数:
#   1) 设 TMode=1 (Thumb)
#   2) DisassembleCommand 限定范围 [addr, addr+length), 防止越界污染相邻 incbin
#   3) createFunction(addr, "FUN_<addr>")
#   4) 全 code range scan_region_define_data 补 Dword (避免 GAS export 崩)
#
# 备份: 调用前先手动 cp "Yu-Gi-Oh WCT 2006.rep" 到 .bak-<ts>-pre-disasm-hidden
#
# Usage:
#   tools\asm-regen\ghidra-run-script.bat DisassembleHiddenFuncs.py
#   tools\asm-regen\ghidra-run-script.bat DisassembleHiddenFuncs.py dry

import csv
import os

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.util import CodeUnitInsertionException
from java.lang import Exception as JavaException
from java.math import BigInteger


CSV_PATH = "temp/hidden_thumb_func_candidates.csv"
CODE_LO = 0x080000C0
CODE_HI = 0x084C7637


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def find_repo_root():
    # 脚本由 tools\asm-regen\ghidra-run-script.bat 启动, 工作目录通常是仓库根
    cwd = os.getcwd()
    for cand in [cwd, os.path.dirname(cwd)]:
        if os.path.exists(os.path.join(cand, CSV_PATH)):
            return cand
    return cwd


def load_candidates():
    root = find_repo_root()
    path = os.path.join(root, CSV_PATH)
    print("[load] %s" % path)
    cands = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cands.append({
                "addr": int(row["rom_addr"], 16),
                "length": int(row["length"]),
                "push_hw": int(row["push_hw"], 16),
                "epilogue_kind": row["epilogue_kind"],
            })
    return cands


def force_disassemble_thumb_range(addr_int, length):
    """在 [addr, addr+length) 内反汇编 Thumb 代码, 不跨界。"""
    addr_lo = _addr(addr_int)
    addr_hi = _addr(addr_int + length - 1)
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()

    # 1) Skip 已是函数入口 (本脚本可重跑)
    if fm.getFunctionAt(addr_lo) is not None:
        return "skip_already_func"

    # 2) Skip 落在已有函数体内 (不应该 但防御)
    if fm.getFunctionContaining(addr_lo) is not None:
        return "skip_in_func"

    # 3) 检查是否已反汇编为指令
    cu = listing.getCodeUnitAt(addr_lo)
    if cu is not None and cu.getMnemonicString() != "??":
        # 已是指令, 直接尝试 createFunction
        if not RUN_DRY:
            f = createFunction(addr_lo, None)
            if f is None:
                return "fail_create_after_predisasm"
        return "ok_existed_disasm"

    if RUN_DRY:
        return "dry"

    # 4) 设 TMode=1 (THUMB)
    prog_ctx = currentProgram.getProgramContext()
    tmode = prog_ctx.getRegister("TMode")
    if tmode is not None:
        try:
            prog_ctx.setValue(tmode, addr_lo, addr_hi, BigInteger.ONE)
        except Exception as e:
            return "fail_set_tmode_%s" % e

    # 5) 限定范围反汇编
    aset = AddressSet(addr_lo, addr_hi)
    cmd = DisassembleCommand(addr_lo, aset, True)
    if not cmd.applyTo(currentProgram):
        return "fail_disasm_%s" % cmd.getStatusMsg()

    # 6) 创建函数
    f = createFunction(addr_lo, None)
    if f is None:
        return "fail_create"

    return "ok"


def scan_region_define_data(start_int, end_int):
    """扫指定 range 收集 PC-rel 数据引用, 在每个 target 上定义 Dword (按 4 对齐)。
    防 GAS export 报 'invalid offset 0xFFFFFFFC'。"""
    start = _addr(start_int)
    end = _addr(end_int)
    listing = currentProgram.getListing()
    targets = set()
    inst = listing.getInstructionAt(start)
    if inst is None:
        inst = listing.getInstructionAfter(start)
    scanned = 0
    while inst is not None and inst.getAddress().compareTo(end) < 0:
        for ref in inst.getReferencesFrom():
            rt = ref.getReferenceType()
            if rt.isData() or rt.isRead() or rt.isWrite():
                to_addr = ref.getToAddress()
                if to_addr.getOffset() < 0x08000000 or to_addr.getOffset() >= 0x0A000000:
                    continue
                targets.add(to_addr)
        scanned += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[ok]   scanned %d instructions, %d unique data targets" % (scanned, len(targets)))

    defined = 0
    skipped_aligned = 0
    skipped_conflict = 0
    for t in targets:
        if (t.getOffset() & 3) != 0:
            skipped_aligned += 1
            continue
        data_at = listing.getDataAt(t)
        if data_at is not None and data_at.isDefined():
            if data_at.getLength() == 4:
                continue
            skipped_conflict += 1
            continue
        if RUN_DRY:
            defined += 1
            continue
        ok = False
        try:
            createData(t, DWordDataType())
            ok = True
        except (JavaException, Exception):
            pass
        if not ok:
            try:
                clearListing(t, t.add(3))
                createData(t, DWordDataType())
                ok = True
            except (JavaException, Exception):
                pass
        if ok:
            defined += 1
        else:
            skipped_conflict += 1
    print("[ok]   defined %d Dword targets (%d misaligned, %d conflict)"
          % (defined, skipped_aligned, skipped_conflict))


def main():
    print("=== DisassembleHiddenFuncs ===  RUN_DRY=%s" % RUN_DRY)
    cands = load_candidates()
    print("[load] %d candidates" % len(cands))

    stats = {}
    fail_samples = []
    ok_count = 0
    for i, c in enumerate(cands):
        result = force_disassemble_thumb_range(c["addr"], c["length"])
        # 归一化结果key (去除消息后缀)
        key = result.split("_", 2)[0] + "_" + result.split("_", 2)[1] if "_" in result and result.count("_") >= 1 else result
        if result.startswith("ok"):
            key = "ok"
            ok_count += 1
        elif result.startswith("skip"):
            pass  # keep full skip key
        else:
            key = "fail"
            if len(fail_samples) < 10:
                fail_samples.append((c["addr"], result))
        stats[key] = stats.get(key, 0) + 1
        if (i + 1) % 100 == 0:
            print("[progress] %d/%d processed" % (i + 1, len(cands)))

    print("\n[Phase D summary]")
    for k, v in sorted(stats.items()):
        print("  %s: %d" % (k, v))
    if fail_samples:
        print("[fail samples]")
        for addr, msg in fail_samples:
            print("  0x%08x: %s" % (addr, msg))

    print("\n[Phase E] scan_region_define_data 0x080000C0..0x084C7637")
    scan_region_define_data(CODE_LO, CODE_HI)

    print("\n[done] DisassembleHiddenFuncs (RUN_DRY=%s, ok=%d)" % (RUN_DRY, ok_count))


main()
