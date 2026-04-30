# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotatePlayCardZoomIn.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - play_card_zoom_in (FUN_080c3d20) 行级 EOL 注释
#
# 函数语义 (详见 plate comment):
#   卡牌小图→大图缩放/旋转过渡动画 (5-step on gUIEffectState[+0x0]).
#   step 0 = 装小图 (load_card_list_small_image x2)
#   step 1 = 起始帧 (FUN_080f6ccc + FUN_080c3880 stats overlay)
#   step 2 = 4-tick affine 过渡 (rom_sin_table_q8 + rom_card_zoom_anim_curve, OAM)
#   step 3 = 装第二张图 + FUN_080c38cc stats
#   step 4 = 切大图模式 (FUN_080cb1cc, BG VRAM/palette 重磅上传)
#   返回 1=busy / 0=done. 唯一 caller: play_ui_effect (FUN_0801ef94) case 0x1a
#
# 前置: LabelDataCrystalRomMap.py + RenameKnownFunctions.py 已跑过
#       (gUIEffectState / rom_sin_table_q8 / rom_card_zoom_anim_curve label 就位,
#        play_card_zoom_in / play_ui_effect 已 rename)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotatePlayCardZoomIn.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import CodeUnit


def u(s):
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


# 行级 EOL 注释 — play_card_zoom_in (FUN_080c3d20)
EOL_COMMENTS = [
    # 入口 + 状态加载
    (0x080c3d2c, "r7 = &gUIEffectState+0x4 (0x02023114, packed card_ref)"),
    (0x080c3d2e, "r0 = &gUIEffectState (0x02023110)"),
    (0x080c3d32, "[sp+0x14] = gUIEffectState[+0x8] (mode flag, 后用)"),
    (0x080c3d34, "r3 = packed card_ref @ gUIEffectState[+0x4]"),
    (0x080c3d36, "r2 = bit 0 (side 0/1)"),
    (0x080c3d3c, "r1 = bits [5:1] (5b row, 0..31)"),
    (0x080c3d40, "r0 = bits [13:6] (8b col, 0..255)"),

    # 索引 EWRAM 卡牌信息数组
    (0x080c3d48, "r0 = (row+col) * 0x14 (entry stride)"),
    (0x080c3d4a, "r1 = 0x868 (per-side 偏移)"),
    (0x080c3d50, "r1 = 0x868 * side (0 或 0x868)"),
    (0x080c3d54, "r6 = 0x0201c510 (卡牌信息数组基址)"),
    (0x080c3d56, "r0 = 0x0201c510 + (row+col)*0x14 + side*0x868"),
    (0x080c3d58, "r2 = entry[+0]: dword 含尺寸编码"),

    # 第二个 lookup (再次解包参数 + 读 entry)
    (0x080c3d76, "r0 = entry[+0] dword (重新读)"),
    (0x080c3d7c, "r0 |= 高位标志 (合成 card_id 输入)"),
    (0x080c3d7e, "r0 = card_ids_080cc8c8(combined_param) (解析 card_id)"),

    # FUN_080c35ac 调用 (尺寸/帧索引计算)
    (0x080c3d96, "r0 = FUN_080c35ac(side, row, col) (帧/尺寸计算)"),
    (0x080c3da0, "[sp+0x1c] = (r0-4) & 0xffff (width-4)"),
    (0x080c3daa, "[sp+0x20] = (r0-4) & 0xffff (height-4)"),

    # 读 entry[+6] / entry[+8] (后用作 OAM size/attr)
    (0x080c3dc4, "r0 = entry[+6] hword"),
    (0x080c3dde, "r4 = entry[+8] hword (默认 OAM attr)"),

    # mode flag 分支: 若 [sp+0x14] != 0, r4 -= bit17_of_packed
    (0x080c3de4, "if mode flag (gUIEffectState[+0x8]) == 0 -> 跳过 r4 修正"),
    (0x080c3dee, "r4 = 1 - bit17 (mode 修正)"),

    # 主 switch
    (0x080c3df0, "r2 = &gUIEffectState"),
    (0x080c3df2, "r0 = step @ gUIEffectState[+0x0] (u16)"),
    (0x080c3df4, "step > 4 -> default (r0 = 0, 完成)"),
    (0x080c3dfa, "r0 = step * 4 (jump_table 偏移)"),
    (0x080c3dfc, "r1 = jump_table @ 0x080c3e18 (5 entries)"),
    (0x080c3e02, "switch dispatch: bx jump_table[step]"),

    # case 0: 装载小图
    (0x080c3e2c, "case 0: 装小卡图 (双侧/双 size)"),
    (0x080c3e36, "load_card_list_small_image(0x200, r4=card_id, 0)"),
    (0x080c3e3a, "r0 = packed[bit16] (flag_a)"),
    (0x080c3e40, "if r4 == flag_a -> 跳过第二次装载, 直接收尾"),
    (0x080c3e4c, "r1 = (r4 == 0) ? 1 : 0 (alt card_id)"),
    (0x080c3e56, "load_card_list_small_image(0x208, alt_id, 0) (第二张)"),
    (0x080c3e5a, "→ 收尾推进 step++"),

    # case 1: 起始帧渲染
    (0x080c3e5c, "case 1: 起始帧渲染 (OBJ blit + stats overlay)"),
    (0x080c3e6e, "if side != gPlayer[+4]^1 -> r6 += 0x40 (OAM Y 微调)"),
    (0x080c3e72, "if r5 (bit0) != 0 -> r6 += 0x20 (OAM X 微调)"),
    (0x080c3e8e, "FUN_080f6ccc(0x80, w|h, 0x100, oam_combined) (OBJ blit)"),
    (0x080c3e98, "r0 = bits [5:1] (row), > 10 -> default"),
    (0x080c3eae, "FUN_080c3880(side, row, col) (card stats overlay)"),
    (0x080c3eb8, "if r4 == flag_a -> 跳过 stats, 直接收尾"),
    (0x080c3ec0, "FUN_080f9ab4(3) (TODO: 推测 sound/sfx 触发)"),

    # case 2: 4-tick affine 过渡
    (0x080c3ecc, "case 2: 4-tick affine (旋转+缩放) 过渡"),
    (0x080c3ed2, "if r4 == flag_a -> 走 LAB_080c3f30 (无第二图, 仅 affine)"),
    (0x080c3ee6, "r6 += 0x40 (player turn 修正)"),
    (0x080c3eee, "if !(packed[bit15] aka byte+1 bit7) -> r6 += 0x20 - shift*8"),
    (0x080c3f08, "else -> r6 += shift*8 (相反方向)"),
    (0x080c3f26, "FUN_080f6ccc(0x80, w|h, 0x100, oam) (双侧 OBJ blit)"),
    (0x080c3f2a, "→ 进入 LAB_080c4010 (推 sub_tick)"),

    # case 2 主路径 (LAB_080c3f30): affine 矩阵计算
    (0x080c3f30, "LAB_080c3f30: 单侧 affine 过渡主体"),
    (0x080c3f3c, "memcpy(sp+0x8, rom_card_zoom_anim_curve, 10) (4-tick angle 曲线)"),
    (0x080c3f42, "r1 = sub_tick @ gUIEffectState[+0x18]"),
    (0x080c3f44, "if sub_tick > 1 -> r2 = 0x208 (后两 tick 用大尺寸)"),
    (0x080c3f96, "r8 = rom_sin_table_q8 (0x09e5f8f0, 128-entry Q8 sin)"),
    (0x080c3fa4, "r0 = anim_curve[sub_tick] (∈ {0,1,8,15})"),
    (0x080c3faa, "angle_idx = (anim*4) & 0x7f (7-bit, sin table 索引)"),
    (0x080c3fb0, "r2 = sin[angle_idx]"),
    (0x080c3fba, "scale = sin*5 + 0x100 (Q8, 1.0~7×)"),
    (0x080c3fc6, "r0 = sin[(r6 & 0x7f)]  → 此处作 cos 入口?"),
    (0x080c3fca, "PA = cos × scale (affine 矩阵)"),
    (0x080c3fd8, "r3 = sin[(r6+0x20) & 0x7f] (90° 偏移 = cos→sin)"),
    (0x080c3fdc, "PB = sin × scale"),
    (0x080c3fde, "r6 += 0x40 (180° 偏移, 用于 PC/PD)"),
    (0x080c4006, "r6 = sin[(r6+0x40) & 0x7f] (-cos)"),
    (0x080c400c, "FUN_080f72e8(...) (提交 OAM affine 矩阵)"),

    # sub_tick 推进
    (0x080c4010, "LAB_080c4010: sub_tick 推进逻辑"),
    (0x080c4012, "r0 = gUIEffectState[+0x18] (sub_tick byte)"),
    (0x080c4014, "gUIEffectState[+0x18] = sub_tick + 1"),
    (0x080c401e, "if old_sub_tick <= 3 -> 仍在 4-tick 内, r0 = 1 返回"),
    (0x080c4020, "old_sub_tick > 3 -> 主 step++ (gUIEffectState[+0x0])"),

    # case 3: 第二图 + 完整 stats
    (0x080c4030, "case 3: 装第二张图 + 完整 stats overlay"),
    (0x080c4044, "load_card_list_small_image (条件性)"),
    (0x080c407e, "FUN_080f6ccc(...) (OBJ blit)"),
    (0x080c409e, "FUN_080c38cc(side, row, col, flag_a, flag_b) 全 bit-field stats"),

    # case 4: 切大图模式 (终态)
    (0x080c40a8, "case 4: 切大图模式"),
    (0x080c40ae, "if r4 == flag_a -> 跳过 (单侧时不重渲)"),
    (0x080c40b8, "FUN_080cb1cc(side, &gUIEffectState+0x4, 0) (BG VRAM+palette 大图)"),

    # 收尾 (case 0/1/2/3/4 共用) + step++
    (0x080c40bc, "LAB_080c40bc: 共用收尾 (主 step++)"),
    (0x080c40c2, "gUIEffectState[+0x0] (u16) = step + 1"),
    (0x080c40c4, "LAB_080c40c4: 返回 r0 = 1 (busy)"),
    (0x080c40cc, "default: r0 = 0 (done)"),
    (0x080c40d0, "epilogue: 返回 r0 (1=busy / 0=done)"),
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
    print("[ok] play_card_zoom_in EOL comments set: %d / %d"
          % (n_set, len(EOL_COMMENTS)))


def main():
    print("=== AnnotatePlayCardZoomIn ===")
    annotate()
    print("[done]")


main()
