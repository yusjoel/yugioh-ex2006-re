# -*- coding: utf-8 -*-
#@runtime Jython
#@author
#@category Export
#@menupath Tools.Export.Export Range To GAS

# ExportRangeToGasS_Jython.py（迭代版，文件名保持不变）
#
# 核心功能：
# 1) 导出指定地址范围 [start, end]（包含端点）
# 2) 导出：指令 + 已定义数据(含结构体字段展开) + UNDEF
# 3) 注释格式统一：@ <address> <byteshex>
# 4) XREFS 输出可开关（默认不输出）
# 5) UNDEF 连续区 >16 bytes：用 ROM_INCBIN 宏输出 .incbin（ROM 路径宏只定义一次）
# 6) 修正部分 Ghidra 文本为 GAS 可接受：
#    - ldr rX,[0xADDR] -> 优先 ldr rX, <label>（地址有label且在范围内），否则转 [pc,#imm]
#    - b/bl/cbz/cbnz 0xADDR -> 优先替换成 <label>（目标在范围内且有label）
#    - adr r0,0xADDR -> adr r0, DAT_xxx（目标在范围内：优先现有label，否则合成DAT_标签）
# 7) 自动输出 .arm/.thumb 切换（使用更稳健的 Thumb 判断：地址对齐优先，其次 TMode/ISAMode，其次指令长度）
# 8) label 全局去重（避免 switchD already defined）
#
# 注意：
# - 这是“从 Ghidra 数据库导出 listing”的脚本，不保证 100% 可重汇编回原始 ROM。
# - 但它会尽量避免 GAS 语法报错（如 [0x...]、重复label、Thumb/ARM模式错位）。

import re
from java.io import FileWriter, BufferedWriter
from jarray import zeros
from ghidra.program.model.symbol import SymbolType
from ghidra.program.model.data import Structure

# --------------------------
# 可按需修改的常量
# --------------------------

ROM_BASE_ADDR = 0x08000000
ROM_PATH = "roms/2343.gba"
UNDEF_INCBIN_THRESHOLD = 16

# --------------------------
# 基础工具
# --------------------------

def normalize_hex(s):
    s = s.strip()
    if s.lower().startswith("0x"):
        s = s[2:]
    return s

def sanitize_label(name):
    out = []
    for ch in name:
        if ch.isalnum() or ch in ['_', '.', '$']:
            out.append(ch)
        else:
            out.append('_')
    s = "".join(out)
    if s and s[0].isdigit():
        s = "_" + s
    return s

def iter_any(it):
    if it is None:
        return []
    if hasattr(it, "hasNext"):
        out = []
        while it.hasNext():
            out.append(it.next())
        return out
    return list(it)

def read_bytes(memory, addr, n):
    try:
        buf = zeros(n, 'b')  # Java byte[]
        got = memory.getBytes(addr, buf)
        if got <= 0:
            return []
        return [(buf[i] & 0xff) for i in range(got)]
    except:
        return []

def bytes_hex_from_list(bs):
    return "".join(["%02x" % (b & 0xff) for b in bs])

def bytes_hex_from_java_bytes(bs):
    if bs is None:
        return ""
    return "".join(["%02x" % (b & 0xff) for b in bs])

def uval_le(bs):
    v = 0
    for i, b in enumerate(bs):
        v |= (b & 0xff) << (8 * i)
    return v

def fmt_addr_bytes(addr, hexbytes):
    return "@ %s %s" % (addr.toString(), hexbytes)

def addr_to_rom_offset(addr):
    try:
        off = int(addr.getOffset()) - int(ROM_BASE_ADDR)
        if off < 0:
            off = 0
        return off
    except:
        return 0

def ask_choice_compat(title, message, choices, default_value):
    try:
        return askChoice(title, message, choices, default_value)
    except:
        try:
            return askChoice(title, message, default_value, choices)
        except:
            yn = askYesNo(title, message + " (Yes/No)")
            return "Yes" if yn else "No"

def in_range(addr, start_addr, end_addr):
    return addr is not None and addr.compareTo(start_addr) >= 0 and addr.compareTo(end_addr) <= 0

# --------------------------
# label 全局去重 + 支持合成 DAT_（仅对范围内目标）
# --------------------------

addr_to_label = {}   # addr.toString() -> unique label
label_to_addr = {}   # unique label -> addr.toString()

def _pick_best_symbol_name(symbols):
    primary = None
    first = None
    for s in symbols:
        st = s.getSymbolType()
        if st != SymbolType.LABEL and st != SymbolType.FUNCTION:
            continue
        try:
            nm = s.getName(True)  # fully qualified（降低重名概率）
        except:
            nm = s.getName()
        nm = sanitize_label(nm)
        if first is None:
            first = nm
        if s.isPrimary():
            primary = nm
            break
    return primary if primary is not None else first

def _make_unique_label(candidate, addr_key):
    cand = sanitize_label(candidate)

    if cand in label_to_addr and label_to_addr[cand] != addr_key:
        cand = "%s_%s" % (cand, sanitize_label(addr_key))

    if cand in label_to_addr and label_to_addr[cand] != addr_key:
        idx = 2
        while True:
            c2 = "%s_%s_%d" % (sanitize_label(candidate), sanitize_label(addr_key), idx)
            if (c2 not in label_to_addr) or (label_to_addr[c2] == addr_key):
                cand = c2
                break
            idx += 1

    return cand

def resolve_unique_label_for_addr(program, addr):
    """只使用 Ghidra 现有 symbol 来解析 label；若无 symbol 返回 None"""
    if addr is None:
        return None

    akey = addr.toString()
    if akey in addr_to_label:
        return addr_to_label[akey]

    symtab = program.getSymbolTable()
    syms = iter_any(symtab.getSymbols(addr))
    base = _pick_best_symbol_name(syms)
    if not base:
        return None

    cand = _make_unique_label(base, akey)
    addr_to_label[akey] = cand
    label_to_addr[cand] = akey
    return cand

def get_or_create_dat_label_for_addr_if_in_range(program, addr, start_addr, end_addr):
    """
    用于 ADR：
    - 如果 addr 在导出范围内：优先现有 label，否则合成 DAT_<addr> 并登记（保证会被定义）
    - 如果 addr 不在导出范围内：不合成，返回 None（避免生成未定义符号）
    """
    if addr is None or (not in_range(addr, start_addr, end_addr)):
        return None

    akey = addr.toString()
    if akey in addr_to_label:
        return addr_to_label[akey]

    lab = resolve_unique_label_for_addr(program, addr)
    if lab:
        return lab

    cand0 = "DAT_%s" % sanitize_label(akey)
    cand = _make_unique_label(cand0, akey)
    addr_to_label[akey] = cand
    label_to_addr[cand] = akey
    return cand

def emit_label_if_any_or_forced(bw, program, addr, emitted_addr_set):
    """输出该地址的 label（现有label 或 ADR 合成的 DAT_），按地址去重"""
    if addr is None:
        return

    akey = addr.toString()
    if akey in emitted_addr_set:
        return

    lab = None
    if akey in addr_to_label:
        lab = addr_to_label.get(akey)
    else:
        lab = resolve_unique_label_for_addr(program, addr)

    if lab:
        bw.write("%s:\n" % lab)
        emitted_addr_set.add(akey)

# --------------------------
# XREF 输出（可开关）
# --------------------------

def emit_xrefs_if_enabled(bw, program, addr, include_xrefs, max_xrefs=12):
    if not include_xrefs:
        return
    refman = program.getReferenceManager()
    refs = iter_any(refman.getReferencesTo(addr))
    if not refs:
        return
    items = []
    for r in refs[:max_xrefs]:
        try:
            items.append("%s(%s)" % (r.getFromAddress().toString(), r.getReferenceType().toString()))
        except:
            pass
    if items:
        suffix = "" if len(refs) <= max_xrefs else " ..."
        bw.write("    @ XREFS: %s%s\n" % (", ".join(items), suffix))

# --------------------------
# ARM/Thumb 模式判断与切换（更稳健）
# --------------------------

def get_context_thumb(program, addr):
    """尝试从 ProgramContext 读取 TMode/ISAMode；失败返回 None"""
    ctx = program.getProgramContext()
    reg = ctx.getRegister("TMode")
    if reg is None:
        reg = ctx.getRegister("ISAMode")
    if reg is None:
        return None
    try:
        rv = ctx.getRegisterValue(reg, addr)
        if rv is None:
            return None
        uv = rv.getUnsignedValue()
        if uv is None:
            return None
        return uv.longValue() != 0
    except:
        return None

def determine_thumb_mode(program, ins):
    """
    Thumb/ARM 判断顺序：
    1) addr % 4 != 0 => Thumb（ARM 指令必须 4 对齐）
    2) ProgramContext: TMode/ISAMode（若能取到）
    3) 指令长度==2 => Thumb（经验规则）
    4) 默认 ARM
    """
    addr = ins.getAddress()
    a = int(addr.getOffset())

    if (a & 3) != 0:
        return True

    ct = get_context_thumb(program, addr)
    if ct is not None:
        return ct

    try:
        if ins.getLength() == 2:
            return True
    except:
        pass

    return False

def emit_mode_if_changed_for_instruction(bw, program, ins, mode_state):
    is_thumb = determine_thumb_mode(program, ins)
    if mode_state.get('thumb', None) is None:
        bw.write(".thumb\n" if is_thumb else ".arm\n")
        mode_state['thumb'] = is_thumb
        return
    if mode_state['thumb'] != is_thumb:
        bw.write(".thumb\n" if is_thumb else ".arm\n")
        mode_state['thumb'] = is_thumb

# --------------------------
# 指令文本修正
# --------------------------

_abs_bracket_pat = re.compile(r',\s*\[\s*(0x[0-9A-Fa-f]+)\s*\]')
_branch_twoop_pat = re.compile(r'^(cbz|cbnz)\s+([^,]+)\s*,\s*(0x[0-9A-Fa-f]+)\s*$', re.IGNORECASE)
_branch_oneop_pat = re.compile(r'^(b\w*|bl\w*)\s+(0x[0-9A-Fa-f]+)\s*$', re.IGNORECASE)
_adr_pat = re.compile(r'^(adr(?:\.w)?)\s+([^,]+)\s*,\s*(0x[0-9A-Fa-f]+)\s*$', re.IGNORECASE)

def fix_ldr_abs_bracket(program, ins, text, start_addr, end_addr):
    """
    ldr rX,[0xADDR]：
    - 若 0xADDR 在范围内且有 label：改为 ldr rX, LABEL（GAS 的 literal load 形式）
    - 否则改成 [pc,#imm]（更接近真实编码）
    """
    m = _abs_bracket_pat.search(text)
    if not m:
        return text

    hexaddr = m.group(1)
    try:
        target_val = int(hexaddr, 16)
        target_addr = toAddr(target_val)
    except:
        return text

    # 1) 范围内且有label => 用 label
    if in_range(target_addr, start_addr, end_addr):
        lab = resolve_unique_label_for_addr(program, target_addr)
        if lab:
            return text[:m.start()] + ", " + lab + text[m.end():]

    # 2) 否则转 PC-relative
    try:
        a = int(ins.getAddress().getOffset())
        pc_bias = 8 if ins.getLength() == 4 else 4
        offset = target_val - (a + pc_bias)
        off_str = "#0x%x" % offset if offset >= 0 else "#-0x%x" % (-offset)
        return text[:m.start()] + ", [pc, %s]" % off_str + text[m.end():]
    except:
        return text

def fix_branch_target_to_label(program, text, start_addr, end_addr):
    """
    b/bl/cbz/cbnz 目标 0xADDR：
    - 只有当目标在导出范围内且该地址有 label 时才替换为 label（避免生成未定义符号）
    """
    t = text.strip()

    m = _branch_twoop_pat.match(t)
    if m:
        mnem, op1, hexaddr = m.group(1), m.group(2), m.group(3)
        try:
            target_addr = toAddr(int(hexaddr, 16))
        except:
            return text
        if not in_range(target_addr, start_addr, end_addr):
            return text
        lab = resolve_unique_label_for_addr(program, target_addr)
        return ("%s %s, %s" % (mnem, op1, lab)) if lab else text

    m = _branch_oneop_pat.match(t)
    if m:
        mnem, hexaddr = m.group(1), m.group(2)
        try:
            target_addr = toAddr(int(hexaddr, 16))
        except:
            return text
        if not in_range(target_addr, start_addr, end_addr):
            return text
        lab = resolve_unique_label_for_addr(program, target_addr)
        return ("%s %s" % (mnem, lab)) if lab else text

    return text

def fix_adr_immediate_to_label(program, text, start_addr, end_addr):
    """
    adr r0,0xADDR -> adr r0, DAT_xxx（目标在范围内：优先现有label，否则合成DAT_）
    """
    m = _adr_pat.match(text.strip())
    if not m:
        return text
    mnem, rd, hexaddr = m.group(1), m.group(2).strip(), m.group(3)

    try:
        target_addr = toAddr(int(hexaddr, 16))
    except:
        return text

    lab = get_or_create_dat_label_for_addr_if_in_range(program, target_addr, start_addr, end_addr)
    if lab:
        return "%s %s, %s" % (mnem, rd, lab)
    return text

# --------------------------
# 已定义数据（非结构体）输出
# --------------------------

def emit_data_line_with_addr_bytes(bw, mnemonic, operand_text, addr, bs_list):
    bw.write("    %-6s %-30s %s\n" % (mnemonic, operand_text, fmt_addr_bytes(addr, bytes_hex_from_list(bs_list))))

def emit_defined_data(bw, program, data_obj, end_addr):
    memory = program.getMemory()
    addr = data_obj.getAddress()
    total_len = data_obj.getLength()

    max_len = total_len
    if data_obj.getMaxAddress().compareTo(end_addr) > 0:
        max_len = int(end_addr.subtract(addr) + 1)

    bs = read_bytes(memory, addr, max_len)
    if not bs:
        bw.write("    .byte  0x00\n")
        return 1

    if max_len == 4:
        emit_data_line_with_addr_bytes(bw, ".word", "0x%08x" % uval_le(bs), addr, bs)
        return 4
    if max_len == 2:
        emit_data_line_with_addr_bytes(bw, ".hword", "0x%04x" % uval_le(bs), addr, bs)
        return 2
    if max_len == 1:
        emit_data_line_with_addr_bytes(bw, ".byte", "0x%02x" % bs[0], addr, bs)
        return 1

    i = 0
    cur = addr
    while i < len(bs):
        chunk = bs[i:i+16]
        items = ", ".join(["0x%02x" % b for b in chunk])
        emit_data_line_with_addr_bytes(bw, ".byte", items, cur, chunk)
        i += len(chunk)
        cur = cur.add(len(chunk))

    return max_len

# --------------------------
# 结构体实例：按字段输出（两行：注释行 + 数据行）
# --------------------------

def get_component_comment(c):
    try:
        s = c.getComment()
        return "" if s is None else s.strip()
    except:
        return ""

def emit_structure_fields(bw, program, data_obj, end_addr, emitted_addr_set, include_xrefs):
    st = data_obj.getDataType()
    st_name = st.getName() if st is not None else "STRUCT"
    st_len = data_obj.getLength()

    bw.write("    @ STRUCT %s (size=0x%x)\n" % (st_name, st_len))

    n = data_obj.getNumComponents()
    for i in range(n):
        c = data_obj.getComponent(i)
        if c is None:
            continue

        caddr = c.getAddress()
        if caddr is None or caddr.compareTo(end_addr) > 0:
            break

        emit_label_if_any_or_forced(bw, program, caddr, emitted_addr_set)
        emit_xrefs_if_enabled(bw, program, caddr, include_xrefs)

        fname = c.getFieldName()
        if fname is None or fname == "":
            fname = "field_%02d" % i
        fname = sanitize_label(fname)

        fcomment = get_component_comment(c)
        bw.write("    @ %s%s\n" % (fname, (", " + fcomment) if fcomment else ""))

        clen = c.getLength()
        if clen <= 0:
            bw.write("    @ (zero-length field)\n")
            continue

        field_end = caddr.add(clen - 1)
        max_len = clen
        if field_end.compareTo(end_addr) > 0:
            max_len = int(end_addr.subtract(caddr) + 1)
            if max_len <= 0:
                break

        bs = read_bytes(program.getMemory(), caddr, max_len)
        if not bs:
            bw.write("    .byte  0x00                           %s\n" % fmt_addr_bytes(caddr, ""))
            continue

        if max_len == 4:
            emit_data_line_with_addr_bytes(bw, ".word", "0x%08x" % uval_le(bs), caddr, bs)
        elif max_len == 2:
            emit_data_line_with_addr_bytes(bw, ".hword", "0x%04x" % uval_le(bs), caddr, bs)
        elif max_len == 1:
            emit_data_line_with_addr_bytes(bw, ".byte", "0x%02x" % bs[0], caddr, bs)
        else:
            j = 0
            cur = caddr
            while j < len(bs):
                chunk = bs[j:j+16]
                items = ", ".join(["0x%02x" % b for b in chunk])
                emit_data_line_with_addr_bytes(bw, ".byte", items, cur, chunk)
                j += len(chunk)
                cur = cur.add(len(chunk))

# --------------------------
# UNDEF 连续区：.byte 或 .incbin（宏）
# --------------------------

def is_undef_at(listing, addr):
    if listing.getInstructionAt(addr) is not None:
        return False
    d = listing.getDataAt(addr)
    if d is not None and d.isDefined():
        return False
    return True

def find_undef_run(listing, start_addr, end_addr):
    cur = start_addr
    n = 0
    while cur.compareTo(end_addr) <= 0:
        if not is_undef_at(listing, cur):
            break
        n += 1
        cur = cur.add(1)
    return n

def emit_undef_run(bw, program, start_addr, run_len):
    if run_len > UNDEF_INCBIN_THRESHOLD:
        off = addr_to_rom_offset(start_addr)
        bw.write("    ROM_INCBIN 0x%x, 0x%x\n" % (off, run_len))
        return

    bs = read_bytes(program.getMemory(), start_addr, run_len)
    if not bs:
        for _ in range(run_len):
            bw.write("    .byte  0x00\n")
        return

    # UNDEF 小段：只输出 .byte，不带注释
    items = ", ".join(["0x%02x" % b for b in bs])
    bw.write("    .byte  %s\n" % items)

# --------------------------
# （可选）导出 structs.s
# --------------------------

def export_all_struct_types(program, out_file):
    dtm = program.getDataTypeManager()
    bw = BufferedWriter(FileWriter(out_file))
    try:
        bw.write("/* Struct definitions exported from Ghidra */\n")
        bw.write("/* Program: %s */\n" % program.getName())
        bw.write("/* Language ID: %s */\n\n" % program.getLanguageID())

        structs = []
        for dt in iter_any(dtm.getAllDataTypes()):
            try:
                if isinstance(dt, Structure):
                    structs.append(dt)
            except:
                pass
        structs.sort(key=lambda x: x.getName())

        for st in structs:
            st_name = sanitize_label(st.getName())
            st_len = st.getLength()

            bw.write("/* struct %s size=0x%x */\n" % (st_name, st_len))
            bw.write(".struct 0\n")

            n = st.getNumComponents()
            for i in range(n):
                c = st.getComponent(i)
                if c is None:
                    continue

                fname = c.getFieldName()
                if fname is None or fname == "":
                    fname = "field_%02d" % i
                fname = sanitize_label(fname)

                clen = c.getLength()
                cdt = c.getDataType()
                cdt_name = cdt.getName() if cdt is not None else "UNKNOWN"

                label = "%s_%s" % (st_name, fname)
                bw.write("%s = .\n" % label)
                bw.write(".space %d    @ %s\n" % (clen, cdt_name))

            bw.write("%s_SIZE = .\n" % st_name)
            bw.write(".endstruct\n\n")

        bw.write("/* End */\n")
    finally:
        bw.close()

# --------------------------
# 主流程
# --------------------------

def run():
    program = currentProgram
    listing = program.getListing()
    memory = program.getMemory()

    # Headless 模式：-postScript ExportRangeToGas.py <start_hex> <end_hex> <output> [xrefs:0|1]
    script_args = list(getScriptArgs())
    if len(script_args) >= 3:
        start_txt = script_args[0]
        end_txt   = script_args[1]
        out_path  = script_args[2]
        include_xrefs = (len(script_args) >= 4 and script_args[3] in ("1", "yes", "Yes", "true", "True"))
        from java.io import File as _JFile
        out_file = _JFile(out_path)
    else:
        choice = ask_choice_compat("Options", "Output XREFS comments?", ["No", "Yes"], "No")
        include_xrefs = (choice == "Yes")
        start_txt = askString("Export range", "Start address (hex, e.g. 08000000):", "08000000")
        end_txt   = askString("Export range", "End address (hex, inclusive, e.g. 08000100):", "08000100")
        out_file  = askFile("Save range as .s", "Save")

    start_addr = toAddr(normalize_hex(start_txt))
    end_addr   = toAddr(normalize_hex(end_txt))

    if start_addr is None or end_addr is None or start_addr.compareTo(end_addr) > 0:
        printerr("Invalid range.")
        return

    bw = BufferedWriter(FileWriter(out_file))

    emitted_addr_set = set()
    mode_state = {'thumb': None}

    try:
        bw.write("/* Exported from Ghidra */\n")
        bw.write("/* Program: %s */\n" % program.getName())
        bw.write("/* Language ID: %s */\n" % program.getLanguageID())
        bw.write("/* Range: %s - %s (inclusive) */\n\n" % (start_addr, end_addr))

        bw.write(".syntax unified\n")
        bw.write(".text\n\n")

        # incbin 宏（ROM 路径只出现一次）
        bw.write("/* incbin macro for UNDEF runs */\n")
        bw.write(".macro ROM_INCBIN start, length\n")
        bw.write("    .incbin \"%s\", \\start, \\length\n" % ROM_PATH)
        bw.write(".endm\n\n")

        cur = start_addr
        while (not monitor.isCancelled()) and cur.compareTo(end_addr) <= 0:

            # label（现有或 DAT_）+ 可选 XREF
            emit_label_if_any_or_forced(bw, program, cur, emitted_addr_set)
            emit_xrefs_if_enabled(bw, program, cur, include_xrefs)

            # 指令优先
            ins = listing.getInstructionAt(cur)
            if ins is not None:
                if ins.getMaxAddress().compareTo(end_addr) > 0:
                    break

                emit_mode_if_changed_for_instruction(bw, program, ins, mode_state)

                text = ins.toString()
                text = fix_ldr_abs_bracket(program, ins, text, start_addr, end_addr)
                text = fix_branch_target_to_label(program, text, start_addr, end_addr)
                text = fix_adr_immediate_to_label(program, text, start_addr, end_addr)

                hexbytes = bytes_hex_from_java_bytes(ins.getBytes())
                bw.write("    %-40s %s\n" % (text, fmt_addr_bytes(ins.getAddress(), hexbytes)))

                nxt = ins.getMaxAddress().next()
                if nxt is None:
                    break
                cur = nxt
                continue

            # 已定义数据（含结构体）
            d = listing.getDataAt(cur)
            if d is not None and d.isDefined():
                dt = d.getDataType()

                if isinstance(dt, Structure):
                    emit_structure_fields(bw, program, d, end_addr, emitted_addr_set, include_xrefs)
                    nxt = d.getMaxAddress().next()
                    if nxt is None:
                        break
                    if d.getMaxAddress().compareTo(end_addr) >= 0:
                        break
                    cur = nxt
                    continue

                consumed = emit_defined_data(bw, program, d, end_addr)
                if consumed <= 0:
                    consumed = 1
                cur = cur.add(consumed)
                continue

            # UNDEF：连续段合并输出（.byte 或 .incbin），不带注释
            run_len = find_undef_run(listing, cur, end_addr)
            if run_len <= 0:
                # 保险推进
                try:
                    _ = memory.getByte(cur)
                except:
                    pass
                cur = cur.add(1)
                continue

            emit_undef_run(bw, program, cur, run_len)
            cur = cur.add(run_len)

        bw.write("\n/* End */\n")

    finally:
        bw.close()

    println("Done: %s" % out_file.getAbsolutePath())

    # 可选：导出 structs.s（headless 模式跳过）
    if len(script_args) >= 3:
        return
    try:
        yn = askYesNo("Export structs", "Export ALL struct type definitions to structs.s?")
        if yn:
            structs_file = askFile("Save structs.s", "Save")
            export_all_struct_types(program, structs_file)
            println("Done: %s" % structs_file.getAbsolutePath())
    except:
        pass

if __name__ == "__main__":
    run()