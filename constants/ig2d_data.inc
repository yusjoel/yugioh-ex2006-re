@ =============================================================================
@ NNS IG2D ROM 数据表地址常量 (源 GL/IG2D_Main.c)
@ 字面量池里的 ROM 数据表地址经 ExportRangeToGas.resolve_word_equate 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@ 注: 表体仍在 rom.s 的 .incbin blob 内 (未 carve); 仅符号化引用地址。
@ =============================================================================

.equ TRIG_TABLE, 0x09e399d0  @ 256 项 s16 cos/sin 查表 (compute_bg_affine_matrix_scaled 用;
                            @ cos(a)=trig[a+0x40], sin(a)=trig[a]); 表体在 .incbin 0x1E399CD+0x283
