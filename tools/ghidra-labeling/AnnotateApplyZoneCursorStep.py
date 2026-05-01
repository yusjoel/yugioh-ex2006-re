# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateApplyZoneCursorStep.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - apply_zone_cursor_step (FUN_080c716c) 参数签名 + 行级 EOL 注释
#
# 函数语义 (详见 plate comment):
#   zone 光标单步推进 + 渲染. 入参 = 当前 gPageState[+0x210] packed value.
#   按 input flag/mode 决策新 packed → 写回 gPageState[+0x210] → render 一次.
#   2 caller (FUN_080c7ea0/FUN_080ccab0 系); runtime 验证按 RIGHT 触发 10 步推进.
#
# 前置: RenameKnownFunctions.py 已跑过 (apply_zone_cursor_step 重命名 + plate)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotateApplyZoneCursorStep.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import CodeUnit, ParameterImpl, Function
from ghidra.program.model.data import UnsignedShortDataType
from ghidra.program.model.symbol import SourceType


def u(s):
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


# 参数签名: u16 packed_cursor (gPageState[+0x210] 同款编码)
def set_signature():
    func = getFunctionAt(toAddr(0x080c716c))
    if func is None:
        print("[fail] no function @ 0x080c716c")
        return
    ushort_dt = UnsignedShortDataType.dataType
    params = [
        ParameterImpl(u("packed_cursor"), ushort_dt, currentProgram, SourceType.USER_DEFINED),
    ]
    func.replaceParameters(
        Function.FunctionUpdateType.DYNAMIC_STORAGE_FORMAL_PARAMS,
        True, SourceType.USER_DEFINED, *params)
    print("[ok] set signature: apply_zone_cursor_step(packed_cursor: u16)")


# 行级 EOL 注释 — apply_zone_cursor_step (FUN_080c716c)
EOL_COMMENTS = [
    # 入口 + packed 解包
    (0x080c7178, "r0 = (u16)packed_cursor (清高 16 位)"),
    (0x080c717c, "[sp+0x0] = r6 = packed_cursor (保存原始)"),
    (0x080c7186, "[sp+0x4] = player_flag (bit 7)"),
    (0x080c718e, "r5 = mode = packed & 0x7f (低 7 位)"),
    (0x080c7194, "r7 = sub_idx = (packed >> 8) & 0x7f (高 7 位)"),
    (0x080c7196, "r2 = &gPageState (0x02023130)"),
    (0x080c71a4, "[sp+0x8] = gPageState[+0x4c + player*2] (mode==0xb 重映射 lookup base)"),

    # mode 分支: ==0xd 用 gPrng+0x14e (input flag), 其他用 gPrng+0x146
    (0x080c71a8, "if mode == 0xd: 走特殊 input source"),
    (0x080c71b6, "r0 = 0x100 (mask)"),
    (0x080c71b8, "r4 = gPrng + 0x14e (hword input flag)"),
    (0x080c71c4, "default: r4 = gPrng + 0x146 (byte input flag)"),
    (0x080c71cc, "r0 = 0x40 (mask for non-d mode)"),
    (0x080c71ce, "r4 = ldrh [r4]; r4 &= mask (input flag bit set?)"),

    # mode==0xb sub_idx 重映射
    (0x080c71d8, "if mode == 0xb: sub_idx += lookup_base (重映射)"),

    # input flag 路径分歧
    (0x080c71e4, "if r4 == 0 (无 input flag): 跳 LAB_080c724e (mode 决策)"),
    (0x080c71ea, "FUN_080c707c(packed) 检查 zone 是否处于特殊状态"),
    (0x080c71f0, "if FUN_080c707c == 0: 跳 LAB_080c7230 (zone state setter only)"),

    # 特殊路径: 取 zone entry → card_id → 写 dirty
    (0x080c71f4, "FUN_080c6638(packed) 取 zone entry 指针"),
    (0x080c7206, "card_ids_080cc8c8(combined) 拿 card_id"),
    (0x080c7212, "gPageState[+0x21c] = card_id (hword)"),
    (0x080c721e, "gPageState[+0x215] |= 0x4 (dirty bit)"),
    (0x080c7220, "→ return (不调 render)"),

    # zone state setter only 路径
    (0x080c7230, "LAB_080c7230: 调 zone state setter 不 render"),
    (0x080c7248, "FUN_080c699c(player, mode, sub_idx, 0)"),
    (0x080c724c, "→ return"),

    # mode 决策路径 (无 input flag)
    (0x080c724e, "LAB_080c724e: 检查 gPageState[+0x148] bit 0xb8 (mode-bit handler 触发)"),
    (0x080c725e, "若 bit set: 跳 LAB_080c7458 走 mode-bit 修正"),
    (0x080c7260, "检查 0x0201f440 bit 0 (input/menu flag)"),
    (0x080c7270, "检查 [0x02020160 + 0x2f51] bit 0 (input/menu flag)"),
    (0x080c728c, "switch on gP1Player[+0x1cf4] (6 cases: 0..5)"),

    # case 0
    (0x080c72cc, "case 0: 读 gP2[+0x4] turn_flag bit 0"),
    (0x080c72d4, "r6 = (turn<<7) | 0xd (强制 mode=0xd)"),

    # case 1: 复杂 zone scan
    (0x080c72e0, "case 1: 操作 gPageState[+0x212] byte + 双 loop 找有效卡"),
    (0x080c72fa, "gPageState[+0x212] = 修正后 byte"),
    (0x080c730e, "loop A: sub_idx 0..4 用 FUN_080c6638 + card_ids_080cc8c8 找有效卡"),
    (0x080c735e, "loop B: 同上但用不同 mode 编码"),
    (0x080c73a0, "LAB_080c73a0: 用 [gP1+0xc] entry + sub_idx 重映射"),
    (0x080c73ba, "r6 = (lookup<<7) | 0xb (强制 mode=0xb)"),

    # case 3
    (0x080c73c8, "case 3: FUN_0803495c input check + sub_idx loop"),
    (0x080c73d0, "FUN_0803495c(turn, sub_idx, 1) 检查 input"),

    # mode-bit handlers (LAB_080c7458)
    (0x080c7458, "LAB_080c7458: 4 个 mode-bit 修正块"),
    (0x080c7464, "if bit 0x40: r6 = FUN_080c6b04(packed, 0)"),
    (0x080c7478, "if bit 0x80: r6 = FUN_080c6b04(packed, 1)"),
    (0x080c748c, "if bit 0x20: r6 = FUN_080c6e9c(packed, 0)"),
    (0x080c74a0, "if bit 0x10: r6 = FUN_080c6e9c(packed, 1)"),

    # finalize 块: 写回 + setter + 比较 + render
    (0x080c74ae, "switchD_default (finalize): 写 gPageState[+0x210] = 新 packed"),
    (0x080c74b8, "gPageState[+0x210] = r6"),
    (0x080c74c2, "解包 r6: r7=player, r4=mode, r5=sub_idx"),
    (0x080c74d8, "FUN_080c699c(player, mode, sub_idx, 0) zone state setter"),
    (0x080c74de, "比较 r6 vs sp+0 (新 packed == 旧 packed?)"),
    (0x080c74f0, "比较 lookup vs sp+0x8 (lookup 也未变?)"),
    (0x080c74f2, "都未变 → 跳 epilogue, 不 render"),
    (0x080c74f4, "if mode == 0xb: 走重映射 render 路径"),
    (0x080c7502, "r2 = lookup + sub_idx (重映射 sub_idx)"),
    (0x080c7508, "render_duel_field_zone_info(player, 0xb, lookup_remapped)"),
    (0x080c7514, "LAB_080c7514: mode != 0xb 普通 render"),
    (0x080c751a, "render_duel_field_zone_info(player, mode, sub_idx)"),

    # epilogue
    (0x080c751e, "LAB_080c751e: epilogue, 恢复 r4-r10 + 返回"),
]


def set_eol_comment(addr_int, txt):
    listing = currentProgram.getListing()
    a = toAddr(addr_int)
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[skip] no codeunit @ 0x%08x" % addr_int)
        return False
    cu.setComment(CodeUnit.EOL_COMMENT, u(txt))
    return True


def annotate():
    n_set = 0
    for addr, txt in EOL_COMMENTS:
        if set_eol_comment(addr, txt):
            n_set += 1
    print("[ok] apply_zone_cursor_step EOL comments set: %d / %d"
          % (n_set, len(EOL_COMMENTS)))


def main():
    print("=== AnnotateApplyZoneCursorStep ===")
    set_signature()
    annotate()
    print("[done]")


main()
