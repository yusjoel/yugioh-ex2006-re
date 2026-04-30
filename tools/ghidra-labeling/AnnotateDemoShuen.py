# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateDemoShuen.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - demo_shuen_state_machine (FUN_0801bd08) 行级 EOL 注释
#
# 函数语义 (详见 plate comment):
#   demo 'shuen' (終焉) 过场动画状态机, 7-state on [gDemoState+0x8c] bits 9..16
#   step 0 INIT      (1帧)  fs_load demo BG1+BG2 + OAM + 启 fade-in
#   step 1 WAIT_INIT       等 fade-in (poll FUN_080148f4)
#   step 2 PHASE_A         keyframe 时间线 (3-byte table @ 0x09e3d01f)
#   step 3 WAIT_A          等 phase A
#   step 4 PHASE_B         双 keyframe 6帧循环 (table @ 0x09e3d022/28)
#   step 5 FADEOUT         3 种亮度/blend 模式
#   step 6 WAIT_FADEOUT    设 done flag bit0
#   default                cleanup, 返回 1=busy / 0=done
#
# 前置: LabelDataCrystalRomMap.py + RenameKnownFunctions.py 已跑过
#       (gDemoState label / demo_shuen_state_machine rename / plate 已就位)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotateDemoShuen.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import CodeUnit


def u(s):
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


# 行级 EOL 注释 — demo_shuen_state_machine (FUN_0801bd08)
EOL_COMMENTS = [
    # 入口 + dispatch
    (0x0801bd14, "r6 = &gDemoState (0x02029EC0)"),
    (0x0801bd1a, "r0 = packed bitfield gDemoState[+0x8c]"),
    (0x0801bd1c, "main state = (r0 << 0xf) >> 0x18 (= bits 9..16 of [+0x8c])"),
    (0x0801bd20, "state > 6 -> default (cleanup, 检查 done flag)"),
    (0x0801bd2c, "switch dispatch: jump_table @ 0x0801bd38 (7 entries)"),

    # case 0 INIT
    (0x0801bd54, "case 0 INIT: 加载资源 + 启 fade-in"),
    (0x0801bd56, "FUN_0801b93c('demo/shuen/shuen_bg1.LZ5bg')"),
    (0x0801bd5e, "fs_load('demo/shuen/shuen_bg2.LZ5bg', 0)"),
    (0x0801bd66, "gDemoState[+0x88] = fs_load 返回 (解压数据指针)"),
    (0x0801bd76, "FUN_0801b91c(0,0,1,1) (OAM/window setup #1)"),
    (0x0801bd86, "FUN_0801b91c(0,1,0,2) (OAM/window setup #2)"),
    (0x0801bd94, "FUN_080147d8(0x28, 0, 0x3c) (启 fade-in)"),
    (0x0801bda8, "DISPCNT |= 0x1800 (启 BG3 + OBJ)"),
    (0x0801bdac, "FUN_080f9adc(3) (TODO: 推测 sound/sfx)"),
    (0x0801bdc8, "gDemoState[+0x8c]: state++ (bits 9..16)"),

    # case 1 WAIT_INIT
    (0x0801bddc, "case 1 WAIT_INIT: 等 gl ready (FUN_080148f4)"),
    (0x0801bde2, "r0 != 0 (still busy) -> 不推进, 跳到 helper"),

    # case 2 PHASE_A
    (0x0801be30, "case 2 PHASE_A: keyframe 时间线"),
    (0x0801be36, "memcpy(stack+0x8, 0x09e3d01f, 3) (载 3-byte keyframe table)"),
    (0x0801be46, "switch sub_state (low byte of [+0x8e]): 0x3c/0x96/0x4b/0xa5/0xe6"),

    # case 3 WAIT_A
    (0x0801bf9c, "case 3 WAIT_A: 等 phase A 完成 (FUN_080148f4)"),

    # case 4 PHASE_B
    (0x0801bfd8, "case 4 PHASE_B: 双 keyframe 6 帧循环"),
    (0x0801bfe0, "memcpy(stack+0xc, 0x09e3d022, 6) (keyframe A)"),
    (0x0801bfec, "memcpy(stack+0x14, 0x09e3d028, 6) (keyframe B)"),
    (0x0801c044, "if sub_state == 0x78: BLDY=0x3c, state++"),

    # case 5 FADEOUT
    (0x0801c0c8, "case 5 FADEOUT: 3 种 brightness/blend 模式"),
    (0x0801c116, "gl_set_brightness(0x3f, 0) (mode 0)"),
    (0x0801c168, "gl_set_brightness(0x3f, 0x10) (mode 1)"),
    (0x0801c1c8, "gl_set_brightness(0x3f, 0) (mode 2 -> state++)"),

    # case 6 WAIT_FADEOUT
    (0x0801c208, "case 6 WAIT_FADEOUT: 等最终 fade-out"),
    (0x0801c21a, "gDemoState[+0x8c] |= 1 (set done flag bit0)"),

    # 公共 counter 推进路径
    (0x0801c1f8, "gDemoState[+0x94]++ (frame counter)"),

    # default 退出路径
    (0x0801c21c, "default DONE: cleanup helpers"),
    (0x0801c224, "FUN_080148f4 final ready check"),
    (0x0801c22a, "r0 != 0 (gl busy) -> 走 cleanup return 0 路径"),
    (0x0801c230, "检查 gDemoState[+0x8c] bit0 (done flag)"),
    (0x0801c238, "bit0 set + gl ready -> r0 = 1 (busy, 等下一帧)"),
    (0x0801c23c, "FUN_08014914 final cleanup; r0 = 0 (done)"),
    (0x0801c242, "epilogue: 返回 r0 (1=busy / 0=done)"),
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


def annotate_demo_shuen():
    n_set = 0
    for addr, txt in EOL_COMMENTS:
        if set_eol_comment(addr, txt):
            n_set += 1
    print("[ok] demo_shuen_state_machine EOL comments set: %d / %d"
          % (n_set, len(EOL_COMMENTS)))


def main():
    print("=== AnnotateDemoShuen ===")
    annotate_demo_shuen()
    print("[done]")


main()
