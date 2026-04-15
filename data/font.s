@ 英文字库（1bpp 8×8，256 字符，ASCII 直接索引）
@ ROM 范围: 0x01CCCA90 - 0x01CCD290 (2048 B)
@ 加载函数: FUN_080f1b60 @ 0x080f1b60
@ 详见 doc/dev/p2-font-location-findings.md
@ 由 tools/rom-export/export_font.py 自动生成

    .section .rodata
    .balign 2
    .global font_ascii_8x8
font_ascii_8x8:
    .incbin "graphics/font/font.bin"
font_ascii_8x8_end:
