#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_main_menu.py — 从 ROM 导出主菜单 page table 为结构化 data/main-menu.s

源数据范围: ROM 0x1E5ECD4 .. 0x1E5EE14 (0x140 字节)
GBA 地址:   0x09E5ECD4 .. 0x09E5EE14

布局 (按 ROM 升序):
  0x09E5ECD4: free_duel_rows[2]      (Free Duel sub-rows, 16B)
  0x09E5ECE4: challenge_rows[4]      (Challenge sub-rows, 32B)
  0x09E5ED04: get_cards_rows[2]      (Get Cards sub-rows, 16B)
  0x09E5ED14: options_rows[2]        (Options sub-rows, 16B)
  0x09E5ED24: main_menu_page_table[12]  (12 主 entry × 0x14, 共 0xF0B)

每个 main entry (0x14B):
  +0x0  u16  title_string_id    (如 0x0bba "Deck Edit")
  +0x2  u16  pad (always 0)
  +0x4  u32  pad (always 0)
  +0x8  u32  init_fn (THUMB)    (非0 时直接调用进入子页, 不渲染 row)
  +0xc  u32  row_array_ptr      (init_fn==0 时指向 sub-row 数组)
  +0x10 u8   row_count
  +0x11 u8 × 3  pad

每个 sub-row (8B):
  +0x0  u16  row_title_string_id
  +0x2  u16  pad (always 0)
  +0x4  u32  row_init_fn (THUMB)

12 个主 entry 中前 6 个是 standard 配置, 后 6 个是 alt 配置 (entry[7] init_fn 不同,
直接进入 Campaign 跳过 Free Duel 子菜单选择).

用法: python tools/rom-export/export_main_menu.py
输出: data/main-menu.s
"""
import struct
import os

ROM_PATH = "roms/2343.gba"
OUT_PATH = "data/main-menu.s"

DATA_START = 0x1E5ECD4
DATA_END   = 0x1E5EE14
GBA_BASE   = 0x09E5ECD4

# ============================================================================
# string_id → 注释用文本 (来自 text/game-strings/en.txt)
# ============================================================================
STR_TEXT = {
    0x0a28: "Campaign",
    0x0a29: "Link Duel",
    0x0a2b: "Options",
    0x0a8f: "Language Selection",
    0x0bb8: "Challenge!",
    0x0bb9: "Free Duel",
    0x0bba: "Deck Edit",
    0x0bbb: "Get Cards",
    0x0bbd: "Your Status",
    0x0bc2: "Duel Puzzle",
    0x0bc3: "Limited Duel",
    0x0bc4: "Theme Duel",
    0x0bc5: "Survival Duel",
    0x0bcc: "Exchange DP to Pack",
    0x0bcd: "PASSWORD",
    0x10ac: "Forb/Ltd Card Lists",
}

# ============================================================================
# init_fn 地址 → 函数 label 名 (与 RenameKnownFunctions.py 同步)
# 数据中存的是 thumb_addr | 1, label 是真实地址 (偶数), 引用时用 .word label + 1
# ============================================================================
INIT_FN_LABEL = {
    0x080dddc4: "enter_exchange_dp_page",
    0x080dddd4: "enter_password_input_page",
    0x080e1390: "enter_limited_duel_page",
    0x080e1a50: "enter_duel_puzzle_page",
    0x080e2c34: "enter_survival_duel_page",
    0x080e3904: "enter_theme_duel_page",
    0x080e7994: "enter_campaign_page",
    0x080e7a18: "enter_link_duel_page",
    0x080ebfb8: "enter_language_selection_page",
    0x080ece40: "enter_your_status_page",
    0x08108558: "enter_forb_ltd_lists_page",
    0x08108ac0: "enter_deck_edit_page",
}


def fn_ref(thumb_addr):
    """thumb_addr (含 bit 0=1) → '<label> + 1' 引用."""
    if thumb_addr == 0:
        return "0"
    if thumb_addr & 1 != 1:
        raise ValueError(f"non-thumb addr 0x{thumb_addr:08x}")
    real = thumb_addr & ~1
    label = INIT_FN_LABEL.get(real)
    if label is None:
        return f"0x{thumb_addr:08x}"
    return f"{label} + 1"


def str_comment(sid):
    txt = STR_TEXT.get(sid)
    return f'"{txt}"' if txt else "?"


def main():
    with open(ROM_PATH, "rb") as f:
        f.seek(DATA_START)
        blob = f.read(DATA_END - DATA_START)

    def at(off, n):
        return blob[off - 0:off + n]

    def u16(off):
        return struct.unpack_from("<H", blob, off)[0]
    def u32(off):
        return struct.unpack_from("<I", blob, off)[0]
    def u8(off):
        return blob[off]

    lines = []
    P = lines.append

    P("@ =============================================================================")
    P("@ 主菜单 page table + sub-row 数组 (Title Screen 之后的 6 子页主菜单)")
    P("@ ROM偏移: 0x1E5ECD4 - 0x1E5EE14 (0x140 字节)")
    P("@ GBA地址: 0x09E5ECD4 - 0x09E5EE14")
    P("@")
    P("@ 6 子页: Deck Edit / Free Duel / Challenge! / Get Cards /")
    P("@         Forb/Ltd Card Lists / Options")
    P("@ 共 12 个主 entry: 前 6 standard, 后 6 alt (entry[7] 直接进 Campaign)")
    P("@")
    P("@ Entry 结构 (0x14B):")
    P("@   +0x0  u16 title_string_id  (master pointer table logical id)")
    P("@   +0x4  u32 pad")
    P("@   +0x8  u32 init_fn THUMB    (非0 时直接进入子页)")
    P("@   +0xc  u32 row_array_ptr    (init_fn==0 时使用)")
    P("@   +0x10 u8  row_count")
    P("@")
    P("@ Sub-row 结构 (8B): {u16 row_title_string_id, u16 pad, u32 row_init_fn THUMB}")
    P("@")
    P("@ 由 tools/rom-export/export_main_menu.py 生成")
    P("@ =============================================================================")
    P("")

    # game_str id 命名常量
    P("@ -----------------------------------------------------------------------------")
    P("@ game_str logical id 常量 (来自 master pointer table @ 0x08000F40)")
    P("@ -----------------------------------------------------------------------------")
    str_consts = [
        ("game_str_id_deck_edit",            0x0bba),
        ("game_str_id_free_duel",            0x0bb9),
        ("game_str_id_challenge",            0x0bb8),
        ("game_str_id_get_cards",            0x0bbb),
        ("game_str_id_forb_ltd_lists",       0x10ac),
        ("game_str_id_options",              0x0a2b),
        ("game_str_id_campaign",             0x0a28),
        ("game_str_id_link_duel",            0x0a29),
        ("game_str_id_duel_puzzle",          0x0bc2),
        ("game_str_id_limited_duel",         0x0bc3),
        ("game_str_id_theme_duel",           0x0bc4),
        ("game_str_id_survival_duel",        0x0bc5),
        ("game_str_id_exchange_dp_pack",     0x0bcc),
        ("game_str_id_password",             0x0bcd),
        ("game_str_id_your_status",          0x0bbd),
        ("game_str_id_language_selection",   0x0a8f),
    ]
    for name, val in str_consts:
        P(f".equ {name:<35s}, 0x{val:04x}    @ \"{STR_TEXT[val]}\"")
    P("")

    # ---- Sub-row 数组们 ----
    sub_arrays = [
        (0x00, 2, "free_duel_rows",  "Free Duel sub-rows (Campaign / Link Duel)"),
        (0x10, 4, "challenge_rows",  "Challenge! sub-rows (Duel Puzzle / Limited / Theme / Survival)"),
        (0x30, 2, "get_cards_rows",  "Get Cards sub-rows (Exchange DP / PASSWORD)"),
        (0x40, 2, "options_rows",    "Options sub-rows (Your Status / Language Selection)"),
    ]
    for off, n, label, desc in sub_arrays:
        gba_addr = GBA_BASE + off
        P("@ -----------------------------------------------------------------------------")
        P(f"@ {desc}")
        P(f"@ GBA地址: 0x{gba_addr:08X}  ({n} × 8B = 0x{n*8:X}B)")
        P("@ -----------------------------------------------------------------------------")
        P(f"{label}:")
        for i in range(n):
            sid = u16(off + i*8)
            pad = u16(off + i*8 + 2)
            fn = u32(off + i*8 + 4)
            assert pad == 0
            P(f"    .hword 0x{sid:04x}                         @ row[{i}] title: {str_comment(sid)}")
            P(f"    .hword 0")
            P(f"    .word  {fn_ref(fn)}    @ init_fn")
        P("")

    # ---- 主 entry 数组 ----
    P("@ -----------------------------------------------------------------------------")
    P("@ 主菜单 6 子页 page entry 表 (12 × 0x14B = 0xF0B)")
    P("@ GBA地址: 0x09E5ED24  ROM偏移: 0x1E5ED24")
    P("@ 前 6: standard 配置. 后 6: alt 配置 (entry[7] 直接进 Campaign 跳过子菜单选择)")
    P("@ -----------------------------------------------------------------------------")
    P("main_menu_page_table:")
    sub_label_map = {
        0x09E5ECD4: "free_duel_rows",
        0x09E5ECE4: "challenge_rows",
        0x09E5ED04: "get_cards_rows",
        0x09E5ED14: "options_rows",
    }
    main_off = 0x50
    for i in range(12):
        off = main_off + i * 0x14
        sid = u16(off)
        pad1 = u16(off + 2)
        pad2 = u32(off + 4)
        init_fn = u32(off + 8)
        row_ptr = u32(off + 0xc)
        row_cnt = u8(off + 0x10)
        pad3 = blob[off + 0x11:off + 0x14]
        assert pad1 == 0 and pad2 == 0 and pad3 == b"\x00\x00\x00", f"unexpected pad in entry[{i}]"

        # row_array_ptr 引用
        if row_ptr == 0:
            row_ref = "0"
        elif row_ptr in sub_label_map:
            row_ref = sub_label_map[row_ptr]
        else:
            row_ref = f"0x{row_ptr:08x}"

        P(f"    @ entry[{i}]: {str_comment(sid)}")
        P(f"    .hword {[k for k, v in str_consts if v == sid][0]}     @ title_string_id")
        P(f"    .hword 0")
        P(f"    .word  0")
        P(f"    .word  {fn_ref(init_fn)}    @ init_fn")
        P(f"    .word  {row_ref}    @ row_array_ptr")
        P(f"    .byte  {row_cnt}                                     @ row_count")
        P(f"    .byte  0, 0, 0")
    P("")

    # 写文件
    out = "\n".join(lines)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"[ok] wrote {OUT_PATH} ({len(out)} chars, {DATA_END-DATA_START} ROM bytes covered)")


if __name__ == "__main__":
    main()
