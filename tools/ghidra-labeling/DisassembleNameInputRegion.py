# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleNameInputRegion.py  (Jython 2.7 / Ghidra 12.x)
#
# 强制反汇编 asm/all.s 里被跳过的 pass_input 代码区，创建函数标签，
# 并为跨页共享的数据结构（FS master, state tables, 内联路径字符串）打 label。
#
# 证据来源: doc/analysis/name-input-page-location.md §5-6 (2026-04-24)
#
# Usage:
#   tools\asm-regen\ghidra-run-script.bat DisassembleNameInputRegion.py
#   tools\asm-regen\ghidra-run-script.bat DisassembleNameInputRegion.py dry

from ghidra.program.model.address import Address
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.lang import RegisterValue
from ghidra.program.model.lang import Register
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
from java.lang import Exception as JavaException
from java.math import BigInteger

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


# ---- pass_input 所在 ROM_INCBIN 区的函数入口（从 push 指令扫描得到）----
# 参见 doc/analysis/name-input-page-location.md §6
# 用 Ghidra 默认格式 "FUN_XXXXXXXX"，保持与 asm/all.s 其余函数一致的命名
PASS_INPUT_FUNCS = [
    # 第一批（0x19C44..0x1A49C 的前半）
    (0x08019C48, "FUN_08019c48"),
    (0x08019CA4, "FUN_08019ca4"),
    (0x08019D14, "FUN_08019d14"),
    (0x08019DA4, "FUN_08019da4"),
    (0x08019E2C, "FUN_08019e2c"),
    (0x08019ED4, "FUN_08019ed4"),
    (0x08019F24, "FUN_08019f24"),
    (0x08019F78, "FUN_08019f78"),
    # 第二批（ROM_INCBIN 0x19fe4..0x1a484，1184 B 剩余区）
    (0x08019FE4, "FUN_08019fe4"),
    (0x0801A16C, "FUN_0801a16c"),
    (0x0801A1AC, "FUN_0801a1ac"),
    (0x0801A230, "FUN_0801a230"),
    (0x0801A328, "FUN_0801a328"),
]

# ---- 数据标签（跨页共享结构）----
DATA_LABELS = [
    # FS 主结构（fs_load 的 r7 基址）
    (0x09E61178, "fs_master_struct",
        "FS master struct (20B header): +0=file_count(339), +4=paths_off, +8=offtab+4, +C=szt+4, +10=fs_data"),
    # name_input 状态机表
    (0x09E588B8, "name_input_state_table",
        "name_input page state table: 4 fn ptrs {init, load_assets, tick, exit} + 0 sentinel"),
    # name_input 内联路径字符串块（代码字面量池目标）
    (0x09E3B360, "name_input_path_strings",
        "Inline FS path strings: name_o_01.LZncer/LZnanr/LZncgr/LZnclr + name_b_01/02/04.LZ5bg"),
    # pass_input 内联路径字符串块
    (0x09E3C5B4, "pass_input_path_strings",
        "Inline FS path strings: pass_o_01.* + pass_b_01 + moziire_b_01"),
    # NNS g2d assert（证据: Nintendo NITRO 库链接）
    (0x09E3B434, "nns_g2d_assert_anmID",
        "NNS g2d assert message: anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"),
    # GL 库源文件名 + assert
    (0x09E398DC, "gl_common_c_filename",
        "Source filename 'GL/GL_Common.c' used in gl_set_brightness assert"),
    (0x09E398EC, "gl_bright_assert",
        "gl_set_brightness assert: 'bright >= -16 && bright <= 16'"),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def force_disassemble_thumb(addr_int):
    addr = _addr(addr_int)
    # Check if already disassembled
    cu = currentProgram.getListing().getCodeUnitAt(addr)
    if cu is not None and cu.getMnemonicString() != "??":
        return True  # already done
    if RUN_DRY:
        print("[dry] would disassemble THUMB @ 0x%08X" % addr_int)
        return True
    # Set TMode register to 1 (THUMB) before disassembling
    prog_ctx = currentProgram.getProgramContext()
    tmode = prog_ctx.getRegister("TMode")
    if tmode is not None:
        try:
            prog_ctx.setValue(tmode, addr, addr, BigInteger.ONE)
        except Exception as e:
            print("[warn] setValue TMode @ 0x%08X failed: %s" % (addr_int, e))
    cmd = DisassembleCommand(addr, None, True)
    ok = cmd.applyTo(currentProgram)
    if not ok:
        print("[fail] disassemble @ 0x%08X: %s" % (addr_int, cmd.getStatusMsg()))
        return False
    print("[ok]   disassembled THUMB @ 0x%08X" % addr_int)
    return True


def create_function(addr_int, name):
    addr = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    func = fm.getFunctionAt(addr)
    if func is None:
        if RUN_DRY:
            print("[dry] would create function %s @ 0x%08X" % (name, addr_int))
            return True
        # Ghidra headless: use createFunction via API
        func = createFunction(addr, name)
        if func is None:
            print("[fail] createFunction @ 0x%08X (%s)" % (addr_int, name))
            return False
        print("[ok]   created function %s @ 0x%08X" % (name, addr_int))
        return True
    else:
        # exists — ensure name matches
        if func.getName() == name or func.getName().startswith(name):
            return True
        if RUN_DRY:
            print("[dry] would rename %s -> %s @ 0x%08X" % (func.getName(), name, addr_int))
            return True
        try:
            func.setName(name, SourceType.USER_DEFINED)
            print("[ok]   renamed %s -> %s @ 0x%08X" % (func.getName(), name, addr_int))
        except Exception as e:
            print("[fail] rename @ 0x%08X: %s" % (addr_int, e))
            return False
        return True


def define_pc_rel_data_targets(func_addr_int, max_scan_bytes=0x400):
    """Walk instructions starting at func entry. For each LDR PC-relative (or any
    instruction with a data reference), ensure the target address is defined as
    Dword so the exporter emits a DAT_XXXXXXXX label."""
    addr = _addr(func_addr_int)
    listing = currentProgram.getListing()
    inst = listing.getInstructionAt(addr)
    if inst is None:
        return 0
    defined = 0
    scanned = 0
    targets = set()
    while inst is not None and scanned < max_scan_bytes:
        for ref in inst.getReferencesFrom():
            rt = ref.getReferenceType()
            if rt.isData() or rt.isRead() or rt.isWrite():
                to_addr = ref.getToAddress()
                # Only data in ROM range we care about (0x08000000..0x0A000000)
                addr_int = to_addr.getOffset()
                if 0x08000000 <= addr_int < 0x0A000000:
                    targets.add(to_addr)
        # Stop at function end markers: bx lr / pop {..., pc}
        mnem = inst.getMnemonicString().lower()
        op_str = inst.toString().lower()
        if mnem == "bx" and "lr" in op_str:
            break
        if mnem == "pop" and "pc" in op_str:
            break
        scanned += inst.getLength()
        inst = listing.getInstructionAfter(inst.getAddress())

    for t in targets:
        data_at = listing.getDataAt(t)
        if data_at is not None and data_at.isDefined():
            continue
        if RUN_DRY:
            print("[dry]   would define Dword @ %s" % t)
            defined += 1
            continue
        # Clear existing undefined data first if needed
        try:
            # createData via FlatProgramAPI
            existing = listing.getUndefinedDataAt(t)
            if existing is not None:
                clearListing(t, t.add(3))
            createData(t, DWordDataType())
            defined += 1
        except Exception as e:
            print("[warn]  createData @ %s failed: %s" % (t, e))
    if defined:
        print("[ok]   defined %d Dword data refs for function @ 0x%08X" % (defined, func_addr_int))
    return defined


def scan_region_define_data(start_int, end_int):
    """Walk all instructions in [start, end), collect data refs, define Dword at each
    target that isn't yet a defined data item.  Safe to run multiple times."""
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
                if to_addr.getOffset() < 0x08000000:
                    continue
                if to_addr.getOffset() >= 0x0A000000:
                    continue
                targets.add(to_addr)
        scanned += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[ok]   scanned %d instructions, collected %d unique data targets" % (scanned, len(targets)))

    defined = 0
    skipped_aligned = 0
    skipped_conflict = 0
    for t in targets:
        # Require u32-aligned address (PC-rel ldr in THUMB requires word align)
        if (t.getOffset() & 3) != 0:
            skipped_aligned += 1
            continue
        data_at = listing.getDataAt(t)
        if data_at is not None and data_at.isDefined():
            # Already Dword? Check length
            if data_at.getLength() == 4:
                continue
            # If it's some other data (e.g., Byte), leave it alone to avoid clobbering
            skipped_conflict += 1
            continue
        if RUN_DRY:
            defined += 1
            continue
        ok = False
        # Attempt 1: try direct create (works if undefined)
        try:
            createData(t, DWordDataType())
            ok = True
        except (JavaException, Exception):
            pass
        # Attempt 2: clear 4 bytes and retry
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
    print("[ok]   defined %d new Dword targets (%d skipped misaligned, %d skipped conflict)"
          % (defined, skipped_aligned, skipped_conflict))
    return defined


def create_data_label(addr_int, name, comment):
    addr = _addr(addr_int)
    st = currentProgram.getSymbolTable()
    if RUN_DRY:
        print("[dry] would label %s @ 0x%08X (%s)" % (name, addr_int, comment[:40]))
        return True
    # Create label (or rename existing)
    existing = st.getPrimarySymbol(addr)
    if existing is not None and existing.getName() == name:
        # already set
        return True
    try:
        st.createLabel(addr, name, SourceType.USER_DEFINED)
        # EOL comment for context
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(addr)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, comment)
        print("[ok]   label %s @ 0x%08X" % (name, addr_int))
        return True
    except Exception as e:
        print("[fail] label @ 0x%08X: %s" % (addr_int, e))
        return False


def main():
    print("=== DisassembleNameInputRegion ===  RUN_DRY=%s" % RUN_DRY)

    # Phase 1: force-disassemble pass_input functions
    print("\n[Phase 1] Force-disassemble pass_input functions")
    for addr_int, name in PASS_INPUT_FUNCS:
        force_disassemble_thumb(addr_int)
        create_function(addr_int, name)

    # Phase 1.5: sweep full code range for undefined PC-rel data targets.
    # Ghidra's auto-propagation disassembles adjacent code (SUB_XXX) far beyond
    # our initial entry points, but doesn't always define the DAT targets of
    # those instructions — which breaks GAS export.  Scan all code (0x080000C0
    # to end of asm/all.s coverage 0x084C7637) so we cover any ripple.
    print("\n[Phase 1.5] Scan full code range 0x080000C0..0x084C7637 for PC-rel data targets")
    scan_region_define_data(0x080000C0, 0x084C7637)

    # Phase 2: data labels
    print("\n[Phase 2] Data labels")
    for addr_int, name, comment in DATA_LABELS:
        create_data_label(addr_int, name, comment)

    print("\n[done] DisassembleNameInputRegion")


main()
