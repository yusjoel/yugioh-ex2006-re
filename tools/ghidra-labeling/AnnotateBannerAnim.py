# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateBannerAnim.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - banner_anim_state_machine (FUN_080bdfac) 行级 EOL 注释
#
# 函数语义 (详见 plate comment + naming-proposals 备忘):
#   banner 出/入场动画状态机, 7-state on [gBannerState+0x10]
#   case 0 INIT          (1帧)  载 palette/tile, 启 BG3
#   case 1 FADE_IN_A    (7帧)  BLDY 渐增 + tile 再渲
#   case 2 DISPLAY     (64帧)  持续显示
#   case 3 FADE_OUT_A   (8帧)  反向 alpha + bl FUN_080f9ab4(8)
#   case 4 TEXT_TRANS  (64帧)  文本 fade in/out
#   case 5 FADE_OUT_B   (8帧)  BLDY 渐减
#   case 6 TEARDOWN     (1帧)  关 BG3
#   default DONE       (return 0)
#
# 前置: LabelDataCrystalRomMap.py + RenameKnownFunctions.py 已跑过
#       (gBannerState label / banner_anim_state_machine rename / plate 已就位)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotateBannerAnim.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import CodeUnit


def u(s):
    """Python 2 str (utf-8 bytes) -> unicode for Java setComment."""
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


# 行级 EOL 注释 — banner_anim_state_machine (FUN_080bdfac)
EOL_COMMENTS = [
    # 入口 + dispatch
    (0x080bdfb8, "r5 = &gBannerState (0x0201FEC0)"),
    (0x080bdfba, "r0 = main state (gBannerState[+0x10])"),
    (0x080bdfbe, "state > 6 -> default (DONE cleanup, return 0)"),
    (0x080bdfca, "switch dispatch: pc = jump_table[state] (table @ 0x080bdfd8)"),

    # 各 case body 入口 (语义标记, 不展开内部细节)
    (0x080bdff4, "case 0 INIT (1 帧): 载 banner palette/tile (lang-dep, gSettings 低3bit), 设 WINOUT, 启 BG3"),
    (0x080be130, "case 1 FADE_IN_A (7 帧): 3行x4次 FUN_080f616c, 末尾 BLDY = sub-counter"),
    (0x080be204, "case 2 DISPLAY (64 帧): 3行x2次 FUN_080f616c, 持续显示无 BLDY 调整"),
    (0x080be26c, "case 3 FADE_OUT_A (8 帧): 3行x8次 FUN_080f616c (复杂坐标), 末尾 bl FUN_080f9ab4(8)"),
    (0x080be404, "case 4 TEXT_TRANSITION (64 帧): 前16帧 fade-in 文本, 16~32帧反向 fade-out"),
    (0x080be4a0, "case 5 FADE_OUT_B (8 帧): 3行x4次 FUN_080f616c, 末尾 BLDY = (8 - sub-counter)"),
    (0x080be598, "case 6 TEARDOWN (1 帧): bl FUN_080f55d4(); DISPCNT &= 0x1FFF (清 BG3 enable)"),

    # case 1 阶段推进示例 (其它 case 同模式不重复标注)
    (0x080be1dc, "gBannerState[+0x11]++ (sub-counter)"),
    (0x080be1ec, "gBannerState[+0x10]++; gBannerState[+0x11] = 0 (满 7 帧, 进 case 2)"),

    # 公共退出路径
    (0x080be5a6, "case 0 / case 6 共用: 写 DISPCNT, gBannerState[+0x10]++"),
    (0x080be5ae, "gBannerState[+0x10]++ (推进主状态)"),
    (0x080be5b0, "LAB_080be5b0: r0 = 1 (busy, 状态机继续运行)"),

    # default 路径 (DONE)
    (0x080be5bc, "default DONE: 读 [0x02023350+0x220] 调 FUN_080f9adc(); 清 gBannerState[+0x0] bit1; 清 [0x02023350+0x215] bit0,2"),
    (0x080be5e6, "r0 = 0 (done)"),
    (0x080be5e8, "epilogue: 返回 r0 (1=busy / 0=done)"),
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


def annotate_banner_anim_state_machine():
    n_set = 0
    for addr, txt in EOL_COMMENTS:
        if set_eol_comment(addr, txt):
            n_set += 1
    print("[ok] banner_anim_state_machine EOL comments set: %d / %d"
          % (n_set, len(EOL_COMMENTS)))


def main():
    print("=== AnnotateBannerAnim ===")
    annotate_banner_anim_state_machine()
    print("[done]")


main()
