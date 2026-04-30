# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateDuelFieldZoneInfo.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - render_duel_field_zone_info (FUN_080cb998) 参数签名 + 行级 EOL
#   - refresh_duel_field_zone_info (FUN_080cbf0c) EOL 注释 (无参数, void)
#
# 函数关系:
#   refresh_duel_field_zone_info 读 gPageState[+0x210] u16 packed
#     → render_duel_field_zone_info(player_flag, mode, sub_idx)
#     → 按 mode (0..0x7f+) 派发到不同业务 case
#         mode 0..4 = helper 链查询
#         mode 5..b = 决斗场卡数据 struct (0x0201c510 / 0x0201c600)
#         mode c..f = zone label (Fusion Deck:/Deck:/Graveyard:/Removed Cards:)
#         mode >=0x10 = LAB_080cbcfc 公共数字渲染
#     → 渲染到 OBJ VRAM 0x0600a8e0 (右对齐 240px)
#
# 前置: RenameKnownFunctions.py 已跑过 (rename + plate 已就位)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotateDuelFieldZoneInfo.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import (
    ParameterImpl, Function, CodeUnit
)
from ghidra.program.model.data import (
    UnsignedCharDataType
)
from ghidra.program.model.symbol import SourceType


def u(s):
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


# === FUN_080cb998: render_duel_field_zone_info(u8, u8, u8) ===
def annotate_render_duel_field_zone_info_params():
    """三个 u8 参数: (player_flag, mode, sub_idx)."""
    func = getFunctionAt(toAddr(0x080cb998))
    if func is None:
        print("[skip] render_duel_field_zone_info: function not found")
        return False
    name = func.getName()
    if name not in ("FUN_080cb998", "render_duel_field_zone_info"):
        print("[skip] render_duel_field_zone_info: unexpected name '%s'" % name)
        return False

    u8 = UnsignedCharDataType.dataType
    params = [
        ParameterImpl("player_flag", u8, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl("mode", u8, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl("sub_idx", u8, currentProgram, SourceType.USER_DEFINED),
    ]
    try:
        func.replaceParameters(
            Function.FunctionUpdateType.DYNAMIC_STORAGE_FORMAL_PARAMS,
            True, SourceType.USER_DEFINED, *params)
        print("[ok] render_duel_field_zone_info params: (player_flag, mode, sub_idx)")
        return True
    except Exception as e:
        print("[fail] render_duel_field_zone_info replaceParameters: %s" % e)
        return False


# render_duel_field_zone_info (FUN_080cb998) 行级 EOL 注释
EOL_COMMENTS_080CB998 = [
    # 入口 + dispatch
    (0x080cb9a4, "r6 = arg0 = player_flag (0=P1, 1=P2; bit0 控制 0x868 stride)"),
    (0x080cb9a6, "r7 = arg1 = mode (0..0x7f+)"),
    (0x080cb9a8, "r5 = arg2 = sub_idx"),
    (0x080cb9b8, "mode > 0xb -> secondary if/else (LAB_080cbb48)"),
    (0x080cb9c4, "switch dispatch: jump_table @ 0x080cb9cc (12 entries, 4 distinct bodies)"),

    # 主 jump table case bodies
    (0x080cb9fc, "case 0..4: 调 helper 链 (FUN_0803b618/5c0/4b0) + gPageState[+0x220] bit field"),
    (0x080cba90, "case 5..9: 读 0x0201c510 + (player&1)*0x868 决斗场卡 struct"),
    (0x080cbab4, "case 0xa: 类似 5..9 但不同 offset"),
    (0x080cbae8, "case 0xb: 用 0x0201c600 + gPageState[+0x50] lookup, 比对 gActiveCardId"),

    # secondary if/else (>= 0xc)
    (0x080cbb48, "secondary dispatch: mode 0xc/d/e/f / default"),
    (0x080cbb62, "case 0xd: game_str_id_to_row(0x3ec + player) -> 'Deck:' (P1/P2)"),
    (0x080cbbcc, "case 0xe: game_str_id_to_row(0x3ee + player) -> 'Graveyard:' (P1/P2)"),
    (0x080cbc38, "case 0xf: game_str_id_to_row(0x3f0 + player) -> 'Removed Cards:' (P1/P2)"),
    (0x080cbcbc, "case 0xc: game_str_id_to_row(0x3ea + player) -> 'Fusion Deck:' (P1/P2)"),

    # 公共数字渲染 + 文本渲染路径
    (0x080cbcfc, "LAB_080cbcfc: default (>=0x10) 公共路径 / case c..f 文本渲染入口"),
    (0x080cbd02, "FUN_0803b618(player, mode, sub_idx): 通用属性提取"),
    (0x080cbd2e, "数字位数计算: r0 /= 10 循环, r8 = digit_count"),
    (0x080cbd82, "LAB_080cbd82: 准备字体 + measure_string_pixel_width + 渲染"),
    (0x080cbd8a, "FUN_080f0cc0(0x20, 2, 1, 2): 准备 sprite/text 渲染上下文"),
    (0x080cbdc2, "PTR_font_jp_base_table: 按 gSettings 语言选字体 ptr"),
    (0x080cbdd2, "measure_string_pixel_width(string_addr) -> r7 = pixel width"),
    (0x080cbe14, "r4 = 0xf0 - text_width  (右对齐到 240px)"),
    (0x080cbe20, "text_render_wrapper(pos, 2, color, string): 主层文本渲染"),
    (0x080cbe3a, "text_render_wrapper(pos, 2, color2, string): 描边/阴影层"),
    (0x080cbeb0, "commit_line_buffer_to_sprite_vram(0x0600a8e0, 0): ★ 写 OBJ VRAM"),

    # case 5..b 出口包装
    (0x080cbebc, "LAB_080cbebc: case 0..b 出口公共包装"),
    (0x080cbec2, "FUN_080cc8c8(r4): 处理 r4 中的 packed 提取值"),
    (0x080cbec8, "重组 (player, mode, sub_idx, sl, sp+8) 成 [sp+0] packed value"),
    (0x080cbef4, "FUN_080cb1cc(value, sp_ptr, 0): 最终 sprite 渲染提交"),
    (0x080cbef8, "FUN_080c8d30(): 渲染收尾 helper"),

    # epilogue
    (0x080cbefc, "LAB_080cbefc: epilogue (无返回值; pop+bx 是 LR 还原)"),
]


# refresh_duel_field_zone_info (FUN_080cbf0c) 行级 EOL 注释
EOL_COMMENTS_080CBF0C = [
    (0x080cbf0e, "r7 = &gPageState (0x02023130)"),
    (0x080cbf14, "r0 = &gPageState[+0x210] (0x02023340) - packed render-target"),
    (0x080cbf16, "r3 = packed u16 (bit7=player_flag, low7=mode, high7=sub_idx)"),
    (0x080cbf20, "r4 = r6 = (r3 >> 7) & 1 = player_flag"),
    (0x080cbf28, "r5 = r3 & 0x7f = mode"),
    (0x080cbf2e, "r2 = (r3 >> 8) & 0x7f = sub_idx"),
    (0x080cbf30, "若 mode == 0xb (special): sub_idx 经 player-specific lookup 表重映射"),
    (0x080cbf3a, "lookup: gPageState[+0x4c + player_flag*2] (u16)"),
    (0x080cbf3e, "sub_idx = lookup_value + (r3>>8)&0x7f, 截断到 u16"),
    (0x080cbf48, "render_duel_field_zone_info(player_flag, mode, sub_idx)"),
    (0x080cbf50, "epilogue (无返回值)"),
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


def annotate_eol(label, comments):
    n_set = 0
    for addr, txt in comments:
        if set_eol_comment(addr, txt):
            n_set += 1
    print("[ok] %s EOL comments set: %d / %d" % (label, n_set, len(comments)))


def main():
    print("=== AnnotateDuelFieldZoneInfo ===")
    annotate_render_duel_field_zone_info_params()
    annotate_eol("render_duel_field_zone_info", EOL_COMMENTS_080CB998)
    annotate_eol("refresh_duel_field_zone_info", EOL_COMMENTS_080CBF0C)
    print("[done]")


main()
