# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ScanFsLoadStrings.py  (Jython 2.7 / Ghidra script)
#
# 方法 4 - 字符串泄漏锚 (function-naming.md §六).
# fs_load(const char *path, int mode) 的 path 实参是 ROM 内 ASCII 字符串
# (e.g. "titleEx/bg3.LZ5bg", "pack/banner_00.LZ5bg"). 扫每个 fs_load
# 调用点的 r0 字面量, 解出 path, 给 caller 函数添加路径锚证据.
#
# 算法:
#   找 fs_load 入口地址 (默认 0x08014fa8) 的所有 caller (bl ref)
#   对每个 bl_addr:
#     - 反向扫前 N 条 instruction (向前 ≤ 32 字节)
#     - 找最近的 r0 写入指令 (LDR r0,[PC,#imm] / movs r0 / mov hi-reg)
#     - 优先 LDR r0,[PC,#imm]: 从 instruction.getReferencesFrom 解 pc-relative pool addr,
#       再读 4 字节 = 字面量 (字符串地址)
#     - 验证字面量在 ROM 范围 [0x08000000, 0x09FFFFFF]
#     - 读 NUL-terminated ASCII (max 64), 必须可打印
#   输出 temp/ghidra-fs-load-strings.csv:
#     caller_addr, bl_addr, string_addr, string_value
#
# 跳过条件:
#   - 没找到合适的 r0 ldr (可能 r0 是寄存器传递或动态计算)
#   - 字面量指向 RAM/MMIO 区
#   - 字符串非 ASCII / 含控制字符 / 长度 == 0
#
# 用法: tools\asm-regen\ghidra-run-script.bat ScanFsLoadStrings.py

import os

from ghidra.program.model.symbol import RefType


FS_LOAD_ADDR = 0x08014fa8

ROM_LO = 0x08000000
ROM_HI = 0x09FFFFFF

MAX_BACK_BYTES = 32  # 反扫多少字节
MAX_STR_LEN = 96


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def read_cstring(mem, addr_obj, max_len):
    """从 addr 读 NUL-terminated ASCII, 全可打印才返回, 否则 None."""
    out = []
    for i in range(max_len):
        try:
            b = mem.getByte(addr_obj.add(i)) & 0xFF
        except Exception:
            return None
        if b == 0:
            break
        if b < 0x20 or b > 0x7E:
            return None
        out.append(chr(b))
    if not out:
        return None
    return "".join(out)


def find_r0_string(listing, mem, bl_addr):
    """
    反扫 bl_addr 前最多 MAX_BACK_BYTES, 找 r0 最近写入指令.
    若是 ldr r0, [pc,#imm] 或 ldr r0, =#imm 则返回 (string_addr_int, string).
    其它 r0 写入 (movs / 寄存器传递) 返回 None (跳过).
    """
    for back in range(2, MAX_BACK_BYTES + 1, 2):
        check_addr = bl_addr.subtract(back)
        instr = listing.getInstructionAt(check_addr)
        if instr is None:
            continue
        mnem = instr.getMnemonicString().lower()
        ops = instr.getOpObjects(0)
        if not ops:
            continue
        first_op = str(ops[0]).lower()
        if first_op != "r0":
            continue
        if mnem == "ldr":
            # ldr r0, [pc, #imm] -> getReferencesFrom 应有一条指向 literal pool 的 ref
            refs = instr.getReferencesFrom()
            for r in refs:
                ta = r.getToAddress()
                if ta is None:
                    continue
                try:
                    pool_val = mem.getInt(ta) & 0xFFFFFFFF
                except Exception:
                    continue
                if not (ROM_LO <= pool_val <= ROM_HI):
                    continue
                str_addr = currentProgram.getAddressFactory().getAddress(
                    "0x%08x" % pool_val)
                s = read_cstring(mem, str_addr, MAX_STR_LEN)
                if s is None:
                    continue
                return (pool_val, s)
            return None
        # r0 是别的形式写入 (movs / mov hi-reg / adds 等), 视为不可解析, 停止反扫
        return None
    return None


def safe_csv(s):
    if s is None:
        return ""
    s = str(s)
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def main():
    af = currentProgram.getAddressFactory()
    listing = currentProgram.getListing()
    mem = currentProgram.getMemory()
    rm = currentProgram.getReferenceManager()
    fm = currentProgram.getFunctionManager()

    fs_load = af.getAddress("0x%08x" % FS_LOAD_ADDR)
    print("[scan] fs_load entry = %s" % fs_load)

    callers_seen = set()
    rows = []  # (caller_int, bl_int, str_addr, str_val)
    n_call_sites = 0
    n_resolved = 0
    n_unresolvable = 0

    for ref in rm.getReferencesTo(fs_load):
        if not ref.getReferenceType().isCall():
            continue
        n_call_sites += 1
        bl_addr = ref.getFromAddress()
        caller = fm.getFunctionContaining(bl_addr)
        if caller is None:
            continue
        caller_ep = caller.getEntryPoint().getOffset() & 0xFFFFFFFF
        result = find_r0_string(listing, mem, bl_addr)
        if result is None:
            n_unresolvable += 1
            continue
        str_addr, str_val = result
        rows.append((caller_ep, bl_addr.getOffset() & 0xFFFFFFFF,
                     str_addr, str_val))
        callers_seen.add(caller_ep)
        n_resolved += 1

    print("[done] ScanFsLoadStrings")
    print("  call sites       = %d" % n_call_sites)
    print("  resolved (with string)  = %d" % n_resolved)
    print("  unresolvable     = %d  (r0 不是 ldr [pc,#imm] / 字符串验证失败)" %
          n_unresolvable)
    print("  unique callers   = %d" % len(callers_seen))

    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    csv_path = os.path.join(out_dir, "ghidra-fs-load-strings.csv")
    f = open(csv_path, "w")
    f.write("caller_addr,bl_addr,string_addr,string_value\n")
    rows.sort()
    for ca, bl, sa, sv in rows:
        f.write("0x%08x,0x%08x,0x%08x,%s\n" % (ca, bl, sa, safe_csv(sv)))
    f.close()
    print("  -> %s" % csv_path)


main()
