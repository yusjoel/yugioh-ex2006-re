# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ScanFsLoadStringsRecursive.py  (Jython 2.7 / Ghidra script)
#
# 方法 4.2 - 中间 wrapper 参数追踪.
#
# ScanFsLoadStrings.py 只解析"caller 直接 ldr r0=path; bl fs_load"模式.
# 但很多业务函数走 caller -> wrapper(s) -> fs_load 链, path 在 wrapper 间透传,
# 直到 wrapper 把 r0 直接送给 fs_load. 本脚本递归追踪这种链.
#
# 算法:
#   target_set = {fs_load: arg_idx_at_target=0}    # fs_load 的 path 在 r0
#   loop:
#     for each (target_addr, arg_idx) in target_set:
#       for each bl <target_addr> caller:
#         reverse-scan caller 中 r<arg_idx> 在 bl 处的来源:
#           literal  → record (caller, bl, path, depth, chain)
#           passthrough(N) → caller 是新 wrapper, 在它的 arg<N> 上, 加入 new_targets
#           unknown  → skip
#     target_set = new_targets
#     depth++
#   直到无新 wrapper 或 MAX_DEPTH.
#
# Reverse-scan 处理:
#   - LDR Rd, [PC, #imm]                  → 解 literal pool 得 path 字符串
#   - MOV high-reg form (0x4600-0x46FF)   → 跟踪 source register
#   - ADDS Rd, Rs, #0 (0x1C00 mask)       → 跟踪 source register
#   - MOVS Rd, #imm8                      → 立即数, unknown (path 不会是 imm8)
#   - 遇到 BL (0xF000-0xFFFF, 4-byte)     → 若 target_reg ∈ {r0..r3}, return unknown
#                                           (caller-saved 被覆盖); 否则跳过 4 字节
#   - 反扫到达函数入口仍未找到 r<target> 写 → r<target> = arg<target_reg> → passthrough
#
# Source 寄存器追踪:
#   若 source ∈ {r0..r3}, 直接是 caller arg, 返回 passthrough(source)
#   若 source ∈ {r4..r10}, 查 arg_save 表 (函数入口前 32 字节扫到的 rN←argM 关系)
#     若找到, passthrough(arg_save[source]); 否则 unknown.
#
# 输出: temp/ghidra-fs-load-strings-recursive.csv
#   columns: caller_addr, bl_addr, target_addr, arg_idx, depth, chain, string_addr, string_value
#   chain = '->'.join(target_addr 列表) 表示 path 透传链 (caller -> wrapper1 -> ... -> fs_load)

import os

from ghidra.program.model.symbol import RefType


FS_LOAD_ADDR = 0x08014fa8

ROM_LO = 0x08000000
ROM_HI = 0x09FFFFFF

MAX_DEPTH = 6
MAX_STR_LEN = 96
ENTRY_PROLOGUE_BYTES = 48  # 多扫一些, 因为 callee-saved push 后才 mov rN, r0 等


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def read_hword(mem, af, addr_int):
    try:
        return mem.getShort(af.getAddress("0x%08x" % addr_int)) & 0xFFFF
    except Exception:
        return None


def read_word(mem, af, addr_int):
    try:
        return mem.getInt(af.getAddress("0x%08x" % addr_int)) & 0xFFFFFFFF
    except Exception:
        return None


def read_cstring_at(mem, af, addr_int, max_len):
    out = []
    for i in range(max_len):
        try:
            b = mem.getByte(af.getAddress("0x%08x" % (addr_int + i))) & 0xFF
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


def build_arg_save(mem, af, func_entry_int):
    """
    入口前 ENTRY_PROLOGUE_BYTES 字节内, 找 rN ← rM (M ∈ 0..3) 形式,
    记录 arg_save[N] = M.
    """
    arg_save = {}
    for off in range(0, ENTRY_PROLOGUE_BYTES, 2):
        hw = read_hword(mem, af, func_entry_int + off)
        if hw is None:
            break
        # MOV high-reg form (0x4600-0x46FF)
        if (hw & 0xFF00) == 0x4600:
            H1 = (hw >> 7) & 1
            H2 = (hw >> 6) & 1
            Rm_low = (hw >> 3) & 0x7
            Rd_low = hw & 0x7
            src = (H2 << 3) | Rm_low
            dst = (H1 << 3) | Rd_low
            if 0 <= src <= 3 and 4 <= dst <= 10 and dst not in arg_save:
                arg_save[dst] = src
            continue
        # ADDS Rd, Rs, #0
        if (hw & 0xFE00) == 0x1C00:
            imm3 = (hw >> 6) & 0x7
            Rs = (hw >> 3) & 0x7
            Rd = hw & 0x7
            if imm3 == 0 and 0 <= Rs <= 3 and 4 <= Rd <= 10 and Rd not in arg_save:
                arg_save[Rd] = Rs
            continue
    return arg_save


def resolve_pc_relative(mem, af, instr_addr_int, hw_imm8):
    """LDR Rd,[PC,#imm8*4]: PC at exec = (instr_addr & ~3) + 4."""
    pc_at_exec = ((instr_addr_int & ~3) + 4) & 0xFFFFFFFF
    pool_addr = (pc_at_exec + (hw_imm8 * 4)) & 0xFFFFFFFF
    val = read_word(mem, af, pool_addr)
    return val


def try_resolve_via_ghidra_ref(listing, mem, af, instr_addr_int):
    """
    若 Ghidra 已在该 instruction 上标了 reference (LDR 指向 literal pool 或
    动态查表 Ghidra 静态解析过), 跟链解 string. 否则 None.
    """
    instr = listing.getInstructionAt(af.getAddress("0x%08x" % instr_addr_int))
    if instr is None:
        return None
    for r in instr.getReferencesFrom():
        ta = r.getToAddress()
        if ta is None:
            continue
        try:
            pool_val = mem.getInt(ta) & 0xFFFFFFFF
        except Exception:
            continue
        if not (ROM_LO <= pool_val <= ROM_HI):
            continue
        s = read_cstring_at(mem, af, pool_val, MAX_STR_LEN)
        if s is not None:
            return (pool_val, s)
    return None


def reverse_scan_arg(listing, mem, af, func_entry_int, bl_addr_int, arg_idx,
                     arg_save):
    """
    Reverse-scan r<arg_idx> in [func_entry, bl_addr) for last write source.
    Returns:
        ('literal', addr_int, str_val)    -- 解出 path 字面量
        ('passthrough', N)                -- r<arg_idx> = caller_func 的 arg<N>
        ('unknown',)                      -- 没法解析
    """
    target_reg = arg_idx
    addr = bl_addr_int - 2
    # Cap reverse-scan distance to avoid pathological cases
    while addr >= func_entry_int:
        hw = read_hword(mem, af, addr)
        if hw is None:
            addr -= 2
            continue
        # BL high-half: 0xF800-0xFFFF (THUMB BL is 4 bytes, high half at higher addr)
        if (hw & 0xF800) == 0xF800:
            # BL spans (addr-2, addr). Skip past it.
            if target_reg in (0, 1, 2, 3):
                # caller-saved regs r0..r3 may be modified by callee
                return ('unknown',)
            # r4-r10 callee-preserved, skip past BL
            addr -= 4
            continue
        # LDR Rd, [PC, #imm8] (Rd = bits 8-10)
        if (hw & 0xF800) == 0x4800:
            rd = (hw >> 8) & 0x7
            if rd == target_reg:
                # 优先 Ghidra ref (pool literal 已被 Ghidra 解析过)
                ghidra_res = try_resolve_via_ghidra_ref(listing, mem, af, addr)
                if ghidra_res is not None:
                    return ('literal', ghidra_res[0], ghidra_res[1])
                # Fallback: raw bytes 解 PC-relative
                imm8 = hw & 0xFF
                val = resolve_pc_relative(mem, af, addr, imm8)
                if val is None:
                    return ('unknown',)
                if not (ROM_LO <= val <= ROM_HI):
                    return ('unknown',)
                s = read_cstring_at(mem, af, val, MAX_STR_LEN)
                if s is None:
                    return ('unknown',)
                return ('literal', val, s)
        # MOV high-reg (0x4600-0x46FF)
        if (hw & 0xFF00) == 0x4600:
            H1 = (hw >> 7) & 1
            H2 = (hw >> 6) & 1
            Rm_low = (hw >> 3) & 0x7
            Rd_low = hw & 0x7
            src = (H2 << 3) | Rm_low
            dst = (H1 << 3) | Rd_low
            if dst == target_reg and src != dst:
                if 0 <= src <= 3:
                    return ('passthrough', src)
                if src in arg_save:
                    return ('passthrough', arg_save[src])
                return ('unknown',)
            # NOP (mov rX, rX) or different dst, skip
        # ADDS Rd, Rs, #imm3 (incl. mov via #0)
        if (hw & 0xFE00) == 0x1C00:
            imm3 = (hw >> 6) & 0x7
            Rs = (hw >> 3) & 0x7
            Rd = hw & 0x7
            if Rd == target_reg:
                if imm3 == 0:
                    if 0 <= Rs <= 3:
                        return ('passthrough', Rs)
                    if Rs in arg_save:
                        return ('passthrough', arg_save[Rs])
                    return ('unknown',)
                return ('unknown',)
        # MOVS Rd, #imm8
        if (hw & 0xF800) == 0x2000:
            rd = (hw >> 8) & 0x7
            if rd == target_reg:
                return ('unknown',)
        # 其它指令可能写 target_reg 但格式繁多, 保守起见: 检查常见 LDR/STR/ADD/SUB
        # bits 11-13 = 011: LDR/STR rt, [rn, #imm5] (LDR 写 Rt, STR 不写)
        if (hw & 0xE800) == 0x6800:
            # LDR/LDRH/LDRB rt, [rn, #imm5] family
            rt = hw & 0x7
            if rt == target_reg:
                # 间接 ldr (e.g. ldr r0, [r0, #0] 动态查表). 若 Ghidra 已静态
                # 解析过 (有 ref 标到字符串), 借力跟链.
                ghidra_res = try_resolve_via_ghidra_ref(listing, mem, af, addr)
                if ghidra_res is not None:
                    return ('literal', ghidra_res[0], ghidra_res[1])
                return ('unknown',)
        # LDR (register form) 0x5800-0x5DFF: ldr rt, [rn, rm]
        if (hw & 0xF200) == 0x5000 and (hw & 0x0E00) >= 0x0800:
            rt = hw & 0x7
            if rt == target_reg:
                ghidra_res = try_resolve_via_ghidra_ref(listing, mem, af, addr)
                if ghidra_res is not None:
                    return ('literal', ghidra_res[0], ghidra_res[1])
                return ('unknown',)
        # ADD Rd, [PC, #imm8]: 0xA000-0xA7FF (Rd = bits 8-10), this is "add rd, pc, #imm8"
        if (hw & 0xF800) == 0xA000:
            rd = (hw >> 8) & 0x7
            if rd == target_reg:
                # ADR-like: PC + imm8 → addr in code; could be string addr in some cases
                imm8 = hw & 0xFF
                pc_at_exec = ((addr & ~3) + 4) & 0xFFFFFFFF
                target_val = (pc_at_exec + (imm8 * 4)) & 0xFFFFFFFF
                if ROM_LO <= target_val <= ROM_HI:
                    s = read_cstring_at(mem, af, target_val, MAX_STR_LEN)
                    if s is not None:
                        return ('literal', target_val, s)
                return ('unknown',)
        addr -= 2

    # Reached function entry without finding r<target_reg> write
    # → r<target_reg> = caller's arg<target_reg> at entry → passthrough
    return ('passthrough', target_reg)


def main():
    af = currentProgram.getAddressFactory()
    listing = currentProgram.getListing()
    mem = currentProgram.getMemory()
    rm = currentProgram.getReferenceManager()
    fm = currentProgram.getFunctionManager()

    # arg_save 缓存
    arg_save_cache = {}

    def get_arg_save(func):
        ep = func.getEntryPoint().getOffset() & 0xFFFFFFFF
        if ep not in arg_save_cache:
            arg_save_cache[ep] = build_arg_save(mem, af, ep)
        return arg_save_cache[ep]

    # target_addr -> arg_idx
    targets = {FS_LOAD_ADDR: 0}
    visited_targets = set()
    # 名称查找 (用于 chain 显示)
    name_of = {FS_LOAD_ADDR: "fs_load"}

    # 结果: (caller_addr, bl_addr, target_addr, arg_idx, depth, chain, str_addr, str_val)
    rows = []
    # caller_addr -> set of (target, arg_idx) marking caller is wrapper
    new_wrappers_per_round = []

    n_unresolved = 0
    n_unresolved_per_target = {}

    depth = 0
    while targets and depth <= MAX_DEPTH:
        new_targets = {}
        round_new_wrapper_count = 0
        for target_addr, target_arg_idx in sorted(targets.items()):
            if target_addr in visited_targets:
                continue
            visited_targets.add(target_addr)
            # callers
            t_addr_obj = af.getAddress("0x%08x" % target_addr)
            for ref in rm.getReferencesTo(t_addr_obj):
                if not ref.getReferenceType().isCall():
                    continue
                bl_addr = ref.getFromAddress()
                bl_int = bl_addr.getOffset() & 0xFFFFFFFF
                caller = fm.getFunctionContaining(bl_addr)
                if caller is None:
                    continue
                caller_ep = caller.getEntryPoint().getOffset() & 0xFFFFFFFF
                # 不允许 caller == target (自递归)
                if caller_ep == target_addr:
                    continue
                arg_save = get_arg_save(caller)
                result = reverse_scan_arg(
                    listing, mem, af, caller_ep, bl_int,
                    target_arg_idx, arg_save)
                # 构造 chain (从当前 target 向 fs_load 方向)
                chain = "%s" % name_of.get(target_addr, "0x%08x" % target_addr)
                if result[0] == 'literal':
                    _, val, sv = result
                    rows.append((caller_ep, bl_int, target_addr,
                                 target_arg_idx, depth, chain, val, sv))
                elif result[0] == 'passthrough':
                    _, N = result
                    if caller_ep in visited_targets:
                        continue
                    if caller_ep not in new_targets:
                        new_targets[caller_ep] = N
                        cname = caller.getName()
                        name_of[caller_ep] = "%s@arg%d" % (cname, N)
                        round_new_wrapper_count += 1
                    elif new_targets[caller_ep] != N:
                        # 同一 caller 两个 bl <target> 推出不同 arg_idx → 取第一个 (warning)
                        print("[warn] caller 0x%08x: conflicting arg_idx %d vs %d" % (
                            caller_ep, new_targets[caller_ep], N))
                else:
                    n_unresolved += 1
                    n_unresolved_per_target[target_addr] = \
                        n_unresolved_per_target.get(target_addr, 0) + 1
        new_wrappers_per_round.append(round_new_wrapper_count)
        targets = new_targets
        depth += 1

    # --- 输出 ---
    print("[done] ScanFsLoadStringsRecursive")
    print("  total resolved paths    = %d" % len(rows))
    print("  total unresolved sites  = %d" % n_unresolved)
    print("  rounds (new wrappers)   = %s" % new_wrappers_per_round)
    print("  unique callers (resolved) = %d" %
          len(set([r[0] for r in rows])))

    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    csv_path = os.path.join(out_dir, "ghidra-fs-load-strings-recursive.csv")
    f = open(csv_path, "w")
    f.write("caller_addr,bl_addr,target_addr,arg_idx,depth,chain,string_addr,string_value\n")
    rows.sort()
    for ca, bl, ta, ai, dp, ch, sa, sv in rows:
        sv_safe = sv if "," not in sv else '"' + sv.replace('"', '""') + '"'
        f.write("0x%08x,0x%08x,0x%08x,%d,%d,%s,0x%08x,%s\n" % (
            ca, bl, ta, ai, dp, ch, sa, sv_safe))
    f.close()
    print("  -> %s" % csv_path)


main()
