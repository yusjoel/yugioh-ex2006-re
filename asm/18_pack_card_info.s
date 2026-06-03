@ ==== 18_pack_card_info.s ====
@ pack 卡信息帧/淡入步进/ATK 行渲染
.thumb
@ 拆包场景卡片信息页图像帧行渲染. 入口保存 r8. 从 pack_ui_state [+0x6fc]/[+0x704] 取卡槽指针和渲染指针, 用 slot_index ([+0x6fa]) 定位当前卡槽描述符. 遍历 [描述符+0x1] bits[3:0] (=slot_count, 0..4) 个卡图: 从卡槽 r7 指针 ldmia 读 card_entry, 提取 bits[19:12] = icid, 调 render_pack_card_frame_to_info_slot(slot_idx, icid). 填完全部卡图后: 计算填充行数 (min(count-1,4))*4+0xa 写入 r8+[+0x6fc] 指向的偏移. 调 render_pack_card_sprite_by_flip_state(1) + render_pack_card_slot_oam(3) + tick_pack_name_scroll_strip_row0(bit6). 最后写 BLDCNT=0x23f + pack_ui_state+0x10=6. 固定返回 1.
render_pack_card_info_frame_row:
    push {r4,r5,r6,r7,lr}                    @ 080d5e84 f0b5
    .hword 0x4647    @ 080d5e86 4746
    push {r7}                                @ 080d5e88 80b4
    ldr r1, DAT_080d5f24                     @ 080d5e8a 2649
    movs r0,#0xc    @ 080d5e8c 0c20
    adds r0,r0,r1    @ 080d5e8e 4018
    .hword 0x4680    @ 080d5e90 8046
    ldr r2, DAT_080d5f28                     @ 080d5e92 254a
    adds r3,r1,r2    @ 080d5e94 8b18
    subs r2,#0x2    @ 080d5e96 023a
    adds r0,r1,r2    @ 080d5e98 8818
    ldrh r0,[r0,#0x0]                        @ 080d5e9a 0088
    lsls r2,r0,#0x2    @ 080d5e9c 8200
    ldr r0,[r3,#0x0]                         @ 080d5e9e 1868
    adds r6,r0,r2    @ 080d5ea0 8618
    ldr r0, DAT_080d5f2c                     @ 080d5ea2 2248
    adds r1,r1,r0    @ 080d5ea4 0918
    ldr r7,[r1,#0x0]                         @ 080d5ea6 0f68
    movs r5,#0x0    @ 080d5ea8 0025
    movs r4,#0x0    @ 080d5eaa 0024
    movs r0,#0xf    @ 080d5eac 0f20
    ldrb r1,[r6,#0x1]                        @ 080d5eae 7178
    ands r0,r1    @ 080d5eb0 0840
    cmp r5,r0                                @ 080d5eb2 8542
    bge LAB_080d5ed4                         @ 080d5eb4 0eda
LAB_080d5eb6:
    ldmia r7!,{r1}                           @ 080d5eb6 02cf
    lsls r1,r1,#0x10    @ 080d5eb8 0904
    lsrs r1,r1,#0x14    @ 080d5eba 090d
    adds r0,r4,#0x0    @ 080d5ebc 201c
    bl render_pack_card_frame_to_info_slot   @ 080d5ebe fff7e5f8
    adds r5,#0x1    @ 080d5ec2 0135
    adds r4,#0x1    @ 080d5ec4 0134
    cmp r4,#0x4                              @ 080d5ec6 042c
    bgt LAB_080d5ed4                         @ 080d5ec8 04dc
    movs r0,#0xf    @ 080d5eca 0f20
    ldrb r2,[r6,#0x1]                        @ 080d5ecc 7278
    ands r0,r2    @ 080d5ece 1040
    cmp r5,r0                                @ 080d5ed0 8542
    blt LAB_080d5eb6                         @ 080d5ed2 f0db
LAB_080d5ed4:
    movs r0,#0xf    @ 080d5ed4 0f20
    ldrb r6,[r6,#0x1]                        @ 080d5ed6 7678
    ands r0,r6    @ 080d5ed8 3040
    subs r0,#0x1    @ 080d5eda 0138
    cmp r0,#0x4                              @ 080d5edc 0428
    ble LAB_080d5ee2                         @ 080d5ede 00dd
    movs r0,#0x4    @ 080d5ee0 0420
LAB_080d5ee2:
    lsls r0,r0,#0x2    @ 080d5ee2 8000
    adds r0,#0xa    @ 080d5ee4 0a30
    ldr r1, DAT_080d5f28                     @ 080d5ee6 1049
    add r1,r8                                @ 080d5ee8 4144
    strh r0,[r1,#0x0]                        @ 080d5eea 0880
    movs r0,#0x1    @ 080d5eec 0120
    bl render_pack_card_sprite_by_flip_state @ 080d5eee fef7dbfb
    movs r0,#0x3    @ 080d5ef2 0320
    bl render_pack_card_slot_oam             @ 080d5ef4 fff746f9
    movs r0,#0xe3    @ 080d5ef8 e320
    lsls r0,r0,#0x3    @ 080d5efa c000
    add r0,r8                                @ 080d5efc 4044
    ldrb r0,[r0,#0x0]                        @ 080d5efe 0078
    lsls r0,r0,#0x19    @ 080d5f00 4006
    lsrs r0,r0,#0x1f    @ 080d5f02 c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d5f04 fff71ef8
    ldr r1, PTR_BLDCNT_080d5f30              @ 080d5f08 0949
    ldr r2, DAT_080d5f34                     @ 080d5f0a 0a4a
    adds r0,r2,#0x0    @ 080d5f0c 101c
    strh r0,[r1,#0x0]                        @ 080d5f0e 0880
    ldr r1, DAT_080d5f24                     @ 080d5f10 0449
    movs r0,#0x6    @ 080d5f12 0620
    strh r0,[r1,#0x10]                       @ 080d5f14 0882
    movs r0,#0x1    @ 080d5f16 0120
    pop {r3}                                 @ 080d5f18 08bc
    .hword 0x4698    @ 080d5f1a 9846
    pop {r4,r5,r6,r7}                        @ 080d5f1c f0bc
    pop {r1}                                 @ 080d5f1e 02bc
    bx r1                                    @ 080d5f20 0847
    .zero  0x2
DAT_080d5f24:
    .word  pack_ui_state                  @ 080d5f24 50580003
DAT_080d5f28:
    .word  0x000006fc                     @ 080d5f28 fc060000
DAT_080d5f2c:
    .word  0x00000704                     @ 080d5f2c 04070000
PTR_BLDCNT_080d5f30:
    .word  BLDCNT                         @ 080d5f30 50000004
DAT_080d5f34:
    .word  0x0000023f                     @ 080d5f34 3f020000

@ 拆包场景卡片揭示帧主驱动. 入口保存 r8/r9/r10. 从 pack_ui_state [+0x6fc]/[+0x6fa]/[+0x704] 取卡组指针, slot_index 和渲染指针, 帧计数器 [+0xc] 递减. 用卡槽描述符 bits[11:8] (card_type, [0..5]) 建立 slot_count 限制 (min 5). 对每个 slot [0..slot_count-1] 调度: 若 slot 位置在 scroll_range 内调 fill_pack_card_slot_tiles + BLDALPHA 渐变; 否则调 sync_state + dispatch_pack_aob_by_type_with_state_base + tick_pack_aob_frame_with_state_base; 通过 set_pack_slot_flag_bit 标记已揭示 slot. 完成后: fill_pack_card_slots_up_to_count 填充剩余卡槽; BLDALPHA=0x10; dispatch_pack_aob_frame_loop_by_reset; 清零 sp buffer; render_pack_label_text_by_flags; pack_ui_state+0x10=2. 末尾调 render_pack_card_spin_oam_by_mode + render_pack_card_sprite_by_flip_state + write_pack_obj_card_entry/tick_pack_aob_frame + render_pack_card_slot_oam + tick_pack_name_scroll_strip_row0. 返回 sp[0x40] (0 或 1).
tick_pack_card_reveal_frame:
    push {r4,r5,r6,r7,lr}                    @ 080d5f38 f0b5
    .hword 0x4657    @ 080d5f3a 5746
    .hword 0x464e    @ 080d5f3c 4e46
    .hword 0x4645    @ 080d5f3e 4546
    push {r5,r6,r7}                          @ 080d5f40 e0b4
    sub sp,#0x4c                             @ 080d5f42 93b0
    ldr r0, DAT_080d5f84                     @ 080d5f44 0f48
    movs r1,#0x0    @ 080d5f46 0021
    str r1,[sp,#0x40]                        @ 080d5f48 1091
    movs r2,#0x0    @ 080d5f4a 0022
    str r2,[sp,#0x44]                        @ 080d5f4c 1192
    ldr r5, DAT_080d5f88                     @ 080d5f4e 0e4d
    adds r3,r0,r5    @ 080d5f50 4319
    ldr r2, DAT_080d5f8c                     @ 080d5f52 0e4a
    adds r1,r0,r2    @ 080d5f54 8118
    ldrh r1,[r1,#0x0]                        @ 080d5f56 0988
    lsls r2,r1,#0x2    @ 080d5f58 8a00
    ldr r1,[r3,#0x0]                         @ 080d5f5a 1968
    adds r1,r1,r2    @ 080d5f5c 8918
    str r1,[sp,#0x34]                        @ 080d5f5e 0d91
    ldr r3, DAT_080d5f90                     @ 080d5f60 0b4b
    adds r1,r0,r3    @ 080d5f62 c118
    ldr r1,[r1,#0x0]                         @ 080d5f64 0968
    .hword 0x4688    @ 080d5f66 8846
    adds r5,#0xc    @ 080d5f68 0c35
    adds r0,r0,r5    @ 080d5f6a 4019
    ldrh r1,[r0,#0x0]                        @ 080d5f6c 0188
    subs r1,#0x1    @ 080d5f6e 0139
    strh r1,[r0,#0x0]                        @ 080d5f70 0180
    ldr r1,[sp,#0x34]                        @ 080d5f72 0d99
    ldr r0,[r1,#0x0]                         @ 080d5f74 0868
    lsls r1,r0,#0x14    @ 080d5f76 0105
    lsrs r0,r1,#0x1c    @ 080d5f78 080f
    cmp r0,#0x5                              @ 080d5f7a 0528
    bhi LAB_080d5f94                         @ 080d5f7c 0ad8
    adds r1,r0,#0x0    @ 080d5f7e 011c
    str r1,[sp,#0x38]                        @ 080d5f80 0e91
    b LAB_080d5f98                           @ 080d5f82 09e0
DAT_080d5f84:
    .word  pack_ui_state                  @ 080d5f84 50580003
DAT_080d5f88:
    .word  0x000006fc                     @ 080d5f88 fc060000
DAT_080d5f8c:
    .word  0x000006fa                     @ 080d5f8c fa060000
DAT_080d5f90:
    .word  0x00000704                     @ 080d5f90 04070000
LAB_080d5f94:
    movs r2,#0x5    @ 080d5f94 0522
    str r2,[sp,#0x38]                        @ 080d5f96 0e92
LAB_080d5f98:
    movs r3,#0x0    @ 080d5f98 0023
    str r3,[sp,#0x3c]                        @ 080d5f9a 0f93
    movs r6,#0x0    @ 080d5f9c 0026
    ldr r5,[sp,#0x38]                        @ 080d5f9e 0e9d
    cmp r6,r5                                @ 080d5fa0 ae42
    blt LAB_080d5fa6                         @ 080d5fa2 00db
    b LAB_080d60ac                           @ 080d5fa4 82e0
LAB_080d5fa6:
    .hword 0x46b2    @ 080d5fa6 b246
LAB_080d5fa8:
    ldr r1, DAT_080d6000                     @ 080d5fa8 1549
    ldr r2, DAT_080d6004                     @ 080d5faa 164a
    adds r0,r1,r2    @ 080d5fac 8818
    movs r3,#0x0    @ 080d5fae 0023
    ldrsh r1,[r0,r3]                         @ 080d5fb0 c15e
    adds r3,r6,#0x1    @ 080d5fb2 731c
    ldr r5,[sp,#0x38]                        @ 080d5fb4 0e9d
    subs r0,r5,r3    @ 080d5fb6 e81a
    lsls r0,r0,#0x2    @ 080d5fb8 8000
    subs r7,r1,r0    @ 080d5fba 0f1a
    lsls r2,r6,#0x2    @ 080d5fbc b200
    .hword 0x4668    @ 080d5fbe 6846
    adds r4,r0,r2    @ 080d5fc0 8418
    .hword 0x4651    @ 080d5fc2 5146
    str r1,[r4,#0x0]                         @ 080d5fc4 2160
    add r1,sp,#0x14                          @ 080d5fc6 05a9
    lsls r0,r6,#0x1    @ 080d5fc8 7000
    adds r5,r1,r0    @ 080d5fca 0d18
    .hword 0x4650    @ 080d5fcc 5046
    strh r0,[r5,#0x0]                        @ 080d5fce 2880
    add r0,sp,#0x20                          @ 080d5fd0 08a8
    adds r0,r0,r2    @ 080d5fd2 8018
    .hword 0x4681    @ 080d5fd4 8146
    .hword 0x4651    @ 080d5fd6 5146
    str r1,[r0,#0x0]                         @ 080d5fd8 0160
    str r3,[sp,#0x48]                        @ 080d5fda 1293
    cmp r7,#0x9                              @ 080d5fdc 092f
    bgt LAB_080d6062                         @ 080d5fde 40dc
    cmp r7,#0x0                              @ 080d5fe0 002f
    blt LAB_080d6008                         @ 080d5fe2 11db
    movs r0,#0x1    @ 080d5fe4 0120
    str r0,[r4,#0x0]                         @ 080d5fe6 2060
    lsls r0,r7,#0x9    @ 080d5fe8 7802
    movs r1,#0xa    @ 080d5fea 0a21
    bl bios_div                              @ 080d5fec 38f006fa
    movs r2,#0x80    @ 080d5ff0 8022
    lsls r2,r2,#0x1    @ 080d5ff2 5200
    adds r0,r0,r2    @ 080d5ff4 8018
    strh r0,[r5,#0x0]                        @ 080d5ff6 2880
    ldr r3,[sp,#0x3c]                        @ 080d5ff8 0f9b
    adds r3,#0x1    @ 080d5ffa 0133
    str r3,[sp,#0x3c]                        @ 080d5ffc 0f93
    b LAB_080d6062                           @ 080d5ffe 30e0
DAT_080d6000:
    .word  0x0300585c                     @ 080d6000 5c580003
DAT_080d6004:
    .word  0x000006fc                     @ 080d6004 fc060000
LAB_080d6008:
    ldr r1, DAT_080d6174                     @ 080d6008 5a49
    ldrh r0,[r1,#0x1a]                       @ 080d600a 488b
    adds r0,#0x1    @ 080d600c 0130
    movs r1,#0x4    @ 080d600e 0421
    bl get_bios_div_remainder                @ 080d6010 38f0f6f9
    adds r1,r0,#0x0    @ 080d6014 011c
    adds r0,r6,#0x0    @ 080d6016 301c
    bl fill_pack_card_slot_tiles             @ 080d6018 fef754ff
    .hword 0x4652    @ 080d601c 5246
    str r2,[r4,#0x0]                         @ 080d601e 2260
    movs r0,#0x80    @ 080d6020 8020
    lsls r0,r0,#0x1    @ 080d6022 4000
    strh r0,[r5,#0x0]                        @ 080d6024 2880
    ldr r3,[sp,#0x3c]                        @ 080d6026 0f9b
    adds r3,#0x1    @ 080d6028 0133
    str r3,[sp,#0x3c]                        @ 080d602a 0f93
    movs r0,#0x7    @ 080d602c 0720
    .hword 0x4645    @ 080d602e 4546
    ldrb r5,[r5,#0x0]                        @ 080d6030 2d78
    ands r0,r5    @ 080d6032 2840
    cmp r0,#0x0                              @ 080d6034 0028
    beq LAB_080d6062                         @ 080d6036 14d0
    movs r0,#0x48    @ 080d6038 4820
    rsbs r0,r0,#0    @ 080d603a 4042
    cmp r7,r0                                @ 080d603c 8742
    ble LAB_080d6062                         @ 080d603e 10dd
    movs r0,#0x1    @ 080d6040 0120
    .hword 0x4649    @ 080d6042 4946
    str r0,[r1,#0x0]                         @ 080d6044 0860
    adds r0,r7,#0x0    @ 080d6046 381c
    adds r0,#0x48    @ 080d6048 4830
    lsls r0,r0,#0x4    @ 080d604a 0001
    movs r1,#0x47    @ 080d604c 4721
    bl bios_div                              @ 080d604e 38f0d5f9
    ldr r2, PTR_BLDALPHA_080d6178            @ 080d6052 494a
    lsls r0,r0,#0x18    @ 080d6054 0006
    lsrs r0,r0,#0x18    @ 080d6056 000e
    movs r3,#0x80    @ 080d6058 8023
    lsls r3,r3,#0x5    @ 080d605a 5b01
    adds r1,r3,#0x0    @ 080d605c 191c
    orrs r0,r1    @ 080d605e 0843
    strh r0,[r2,#0x0]                        @ 080d6060 1080
LAB_080d6062:
    cmp r7,#0x0                              @ 080d6062 002f
    bne LAB_080d608c                         @ 080d6064 12d1
    movs r0,#0x3    @ 080d6066 0320
    bl sync_state_and_init_sprite            @ 080d6068 23f024fd
    movs r0,#0x7    @ 080d606c 0720
    .hword 0x4645    @ 080d606e 4546
    ldrb r5,[r5,#0x0]                        @ 080d6070 2d78
    ands r0,r5    @ 080d6072 2840
    cmp r0,#0x0                              @ 080d6074 0028
    beq LAB_080d609e                         @ 080d6076 12d0
    .hword 0x4640    @ 080d6078 4046
    ldr r1,[r0,#0x0]                         @ 080d607a 0168
    lsls r1,r1,#0x1d    @ 080d607c 4907
    lsrs r1,r1,#0x1d    @ 080d607e 490f
    adds r0,r6,#0x0    @ 080d6080 301c
    bl dispatch_pack_aob_by_type_with_state_base @ 080d6082 fff749f9
    movs r1,#0x48    @ 080d6086 4821
    rsbs r1,r1,#0    @ 080d6088 4942
    str r1,[sp,#0x44]                        @ 080d608a 1191
LAB_080d608c:
    movs r0,#0x7    @ 080d608c 0720
    .hword 0x4642    @ 080d608e 4246
    ldrb r2,[r2,#0x0]                        @ 080d6090 1278
    ands r0,r2    @ 080d6092 1040
    cmp r0,#0x0                              @ 080d6094 0028
    beq LAB_080d609e                         @ 080d6096 02d0
    movs r3,#0x48    @ 080d6098 4823
    rsbs r3,r3,#0    @ 080d609a 5b42
    str r3,[sp,#0x44]                        @ 080d609c 1193
LAB_080d609e:
    movs r5,#0x4    @ 080d609e 0425
    add r8,r5                                @ 080d60a0 a844
    ldr r6,[sp,#0x48]                        @ 080d60a2 129e
    ldr r0,[sp,#0x38]                        @ 080d60a4 0e98
    cmp r6,r0                                @ 080d60a6 8642
    bge LAB_080d60ac                         @ 080d60a8 00da
    b LAB_080d5fa8                           @ 080d60aa 7de7
LAB_080d60ac:
    ldr r1, DAT_080d6174                     @ 080d60ac 3149
    ldr r2, DAT_080d617c                     @ 080d60ae 334a
    adds r0,r1,r2    @ 080d60b0 8818
    movs r3,#0x0    @ 080d60b2 0023
    ldrsh r0,[r0,r3]                         @ 080d60b4 c05e
    cmp r0,#0x0                              @ 080d60b6 0028
    bne LAB_080d611e                         @ 080d60b8 31d1
    movs r5,#0xdf    @ 080d60ba df25
    lsls r5,r5,#0x3    @ 080d60bc ed00
    adds r0,r1,r5    @ 080d60be 4819
    ldr r0,[r0,#0x0]                         @ 080d60c0 0068
    .hword 0x4680    @ 080d60c2 8046
    movs r6,#0x0    @ 080d60c4 0026
    movs r0,#0xf    @ 080d60c6 0f20
    ldr r1,[sp,#0x34]                        @ 080d60c8 0d99
    ldrb r1,[r1,#0x1]                        @ 080d60ca 4978
    ands r0,r1    @ 080d60cc 0840
    cmp r6,r0                                @ 080d60ce 8642
    bge LAB_080d60f2                         @ 080d60d0 0fda
LAB_080d60d2:
    .hword 0x4642    @ 080d60d2 4246
    adds r2,#0x4    @ 080d60d4 0432
    .hword 0x4690    @ 080d60d6 9046
    subs r2,#0x4    @ 080d60d8 043a
    ldmia r2!,{r0}                           @ 080d60da 01ca
    lsls r0,r0,#0x10    @ 080d60dc 0004
    lsrs r0,r0,#0x14    @ 080d60de 000d
    bl set_pack_slot_flag_bit                @ 080d60e0 06f0fefc
    adds r6,#0x1    @ 080d60e4 0136
    movs r0,#0xf    @ 080d60e6 0f20
    ldr r3,[sp,#0x34]                        @ 080d60e8 0d9b
    ldrb r3,[r3,#0x1]                        @ 080d60ea 5b78
    ands r0,r3    @ 080d60ec 1840
    cmp r6,r0                                @ 080d60ee 8642
    blt LAB_080d60d2                         @ 080d60f0 efdb
LAB_080d60f2:
    ldr r5, DAT_080d6174                     @ 080d60f2 204d
    ldr r0, DAT_080d6180                     @ 080d60f4 2248
    adds r4,r5,r0    @ 080d60f6 2c18
    ldrb r3,[r4,#0x0]                        @ 080d60f8 2378
    lsls r0,r3,#0x1e    @ 080d60fa 9807
    lsrs r0,r0,#0x1f    @ 080d60fc c00f
    movs r2,#0x1    @ 080d60fe 0122
    eors r2,r0    @ 080d6100 4240
    lsls r2,r2,#0x1    @ 080d6102 5200
    movs r1,#0x3    @ 080d6104 0321
    rsbs r1,r1,#0    @ 080d6106 4942
    ands r1,r3    @ 080d6108 1940
    orrs r1,r2    @ 080d610a 1143
    strb r1,[r4,#0x0]                        @ 080d610c 2170
    ldr r2,[sp,#0x34]                        @ 080d610e 0d9a
    ldr r0,[r2,#0x0]                         @ 080d6110 1068
    lsls r0,r0,#0x19    @ 080d6112 4006
    lsrs r0,r0,#0x19    @ 080d6114 400e
    lsls r1,r1,#0x1e    @ 080d6116 8907
    lsrs r1,r1,#0x1f    @ 080d6118 c90f
    bl render_pack_owned_count_to_sprite_row @ 080d611a fef795fe
LAB_080d611e:
    ldr r3, DAT_080d6174                     @ 080d611e 154b
    ldr r5, DAT_080d617c                     @ 080d6120 164d
    adds r0,r3,r5    @ 080d6122 5819
    movs r1,#0x0    @ 080d6124 0021
    ldrsh r0,[r0,r1]                         @ 080d6126 405e
    ldr r2,[sp,#0x44]                        @ 080d6128 119a
    cmp r0,r2                                @ 080d612a 9042
    bge LAB_080d6202                         @ 080d612c 69da
    subs r5,#0x4    @ 080d612e 043d
    adds r0,r3,r5    @ 080d6130 5819
    ldr r4,[r0,#0x0]                         @ 080d6132 0468
    movs r0,#0x80    @ 080d6134 8020
    ldr r1,[sp,#0x34]                        @ 080d6136 0d99
    ldrb r1,[r1,#0x0]                        @ 080d6138 0978
    orrs r0,r1    @ 080d613a 0843
    ldr r2,[sp,#0x34]                        @ 080d613c 0d9a
    strb r0,[r2,#0x0]                        @ 080d613e 1070
    adds r5,#0x20    @ 080d6140 2035
    adds r3,r3,r5    @ 080d6142 5b19
    movs r0,#0x8    @ 080d6144 0820
    ldrb r2,[r3,#0x0]                        @ 080d6146 1a78
    orrs r2,r0    @ 080d6148 0243
    strb r2,[r3,#0x0]                        @ 080d614a 1a70
    movs r6,#0x0    @ 080d614c 0026
    ldr r0, DAT_080d6174                     @ 080d614e 0948
    ldrh r0,[r0,#0xa]                        @ 080d6150 4089
    cmp r6,r0                                @ 080d6152 8642
    bge LAB_080d61b8                         @ 080d6154 30da
    ldr r1, DAT_080d6174                     @ 080d6156 0749
    subs r5,#0x28    @ 080d6158 283d
    adds r0,r1,r5    @ 080d615a 4819
    ldr r1,[r0,#0x0]                         @ 080d615c 0168
    movs r0,#0x80    @ 080d615e 8020
    ldrb r1,[r1,#0x0]                        @ 080d6160 0978
    ands r0,r1    @ 080d6162 0840
    cmp r0,#0x0                              @ 080d6164 0028
    bne LAB_080d6184                         @ 080d6166 0dd1
    movs r0,#0x9    @ 080d6168 0920
    rsbs r0,r0,#0    @ 080d616a 4042
    ands r2,r0    @ 080d616c 0240
    strb r2,[r3,#0x0]                        @ 080d616e 1a70
    b LAB_080d61b8                           @ 080d6170 22e0
    .zero  0x2
DAT_080d6174:
    .word  0x0300585c                     @ 080d6174 5c580003
PTR_BLDALPHA_080d6178:
    .word  BLDALPHA                       @ 080d6178 52000004
DAT_080d617c:
    .word  0x000006fc                     @ 080d617c fc060000
DAT_080d6180:
    .word  0x00000719                     @ 080d6180 19070000
LAB_080d6184:
    adds r6,#0x1    @ 080d6184 0136
    ldr r0, DAT_080d6238                     @ 080d6186 2c48
    ldrh r0,[r0,#0xa]                        @ 080d6188 4089
    cmp r6,r0                                @ 080d618a 8642
    bge LAB_080d61b8                         @ 080d618c 14da
    ldr r1, DAT_080d6238                     @ 080d618e 2a49
    movs r2,#0xde    @ 080d6190 de22
    lsls r2,r2,#0x3    @ 080d6192 d200
    adds r0,r1,r2    @ 080d6194 8818
    ldr r0,[r0,#0x0]                         @ 080d6196 0068
    lsls r1,r6,#0x2    @ 080d6198 b100
    adds r1,r1,r0    @ 080d619a 0918
    movs r0,#0x80    @ 080d619c 8020
    ldrb r1,[r1,#0x0]                        @ 080d619e 0978
    ands r0,r1    @ 080d61a0 0840
    cmp r0,#0x0                              @ 080d61a2 0028
    bne LAB_080d6184                         @ 080d61a4 eed1
    ldr r3, DAT_080d6238                     @ 080d61a6 244b
    movs r5,#0xe3    @ 080d61a8 e325
    lsls r5,r5,#0x3    @ 080d61aa ed00
    adds r1,r3,r5    @ 080d61ac 5919
    movs r0,#0x9    @ 080d61ae 0920
    rsbs r0,r0,#0    @ 080d61b0 4042
    ldrb r2,[r1,#0x0]                        @ 080d61b2 0a78
    ands r0,r2    @ 080d61b4 1040
    strb r0,[r1,#0x0]                        @ 080d61b6 0870
LAB_080d61b8:
    ldr r3, DAT_080d6238                     @ 080d61b8 1f4b
    ldrh r0,[r3,#0x1a]                       @ 080d61ba 588b
    adds r0,#0x1    @ 080d61bc 0130
    movs r1,#0x4    @ 080d61be 0421
    bl get_bios_div_remainder                @ 080d61c0 38f01ef9
    movs r1,#0xf    @ 080d61c4 0f21
    ldr r5,[sp,#0x34]                        @ 080d61c6 0d9d
    ldrb r5,[r5,#0x1]                        @ 080d61c8 6d78
    ands r1,r5    @ 080d61ca 2940
    bl fill_pack_card_slots_up_to_count      @ 080d61cc fef790fc
    ldr r1, PTR_BLDALPHA_080d623c            @ 080d61d0 1a49
    movs r0,#0x10    @ 080d61d2 1020
    strh r0,[r1,#0x0]                        @ 080d61d4 0880
    ldr r0,[sp,#0x34]                        @ 080d61d6 0d98
    adds r1,r4,#0x0    @ 080d61d8 211c
    bl dispatch_pack_aob_frame_loop_by_reset @ 080d61da fff725f9
    ldr r0,[sp,#0x38]                        @ 080d61de 0e98
    cmp r0,#0x0                              @ 080d61e0 0028
    beq LAB_080d61f2                         @ 080d61e2 06d0
    movs r1,#0x0    @ 080d61e4 0021
    .hword 0x4668    @ 080d61e6 6846
    ldr r6,[sp,#0x38]                        @ 080d61e8 0e9e
LAB_080d61ea:
    stmia r0!,{r1}                           @ 080d61ea 02c0
    subs r6,#0x1    @ 080d61ec 013e
    cmp r6,#0x0                              @ 080d61ee 002e
    bne LAB_080d61ea                         @ 080d61f0 fbd1
LAB_080d61f2:
    ldr r0,[sp,#0x34]                        @ 080d61f2 0d98
    bl render_pack_label_text_by_flags       @ 080d61f4 fef798fc
    ldr r1, DAT_080d6240                     @ 080d61f8 1149
    movs r0,#0x2    @ 080d61fa 0220
    strh r0,[r1,#0x10]                       @ 080d61fc 0882
    movs r1,#0x1    @ 080d61fe 0121
    str r1,[sp,#0x40]                        @ 080d6200 1091
LAB_080d6202:
    ldr r2,[sp,#0x3c]                        @ 080d6202 0f9a
    cmp r2,#0x0                              @ 080d6204 002a
    ble LAB_080d6210                         @ 080d6206 03dd
    movs r0,#0x1    @ 080d6208 0120
    adds r1,r2,#0x0    @ 080d620a 111c
    bl render_pack_card_spin_oam_by_mode     @ 080d620c fff730f9
LAB_080d6210:
    movs r0,#0x1    @ 080d6210 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6212 fef749fa
    movs r6,#0x0    @ 080d6216 0026
    ldr r3,[sp,#0x38]                        @ 080d6218 0e9b
    cmp r6,r3                                @ 080d621a 9e42
    bge LAB_080d6262                         @ 080d621c 21da
    add r5,sp,#0x14                          @ 080d621e 05ad
    .hword 0x466c    @ 080d6220 6c46
LAB_080d6222:
    lsls r1,r6,#0x2    @ 080d6222 b100
    ldr r0,[r4,#0x0]                         @ 080d6224 2068
    cmp r0,#0x1                              @ 080d6226 0128
    bne LAB_080d6244                         @ 080d6228 0cd1
    ldrh r1,[r5,#0x0]                        @ 080d622a 2988
    adds r0,r6,#0x0    @ 080d622c 301c
    movs r2,#0x2    @ 080d622e 0222
    bl write_pack_obj_card_entry             @ 080d6230 fff718f8
    b LAB_080d6256                           @ 080d6234 0fe0
    .zero  0x2
DAT_080d6238:
    .word  0x0300585c                     @ 080d6238 5c580003
PTR_BLDALPHA_080d623c:
    .word  BLDALPHA                       @ 080d623c 52000004
DAT_080d6240:
    .word  pack_ui_state                  @ 080d6240 50580003
LAB_080d6244:
    add r0,sp,#0x20                          @ 080d6244 08a8
    adds r0,r0,r1    @ 080d6246 4018
    ldr r0,[r0,#0x0]                         @ 080d6248 0068
    cmp r0,#0x1                              @ 080d624a 0128
    bne LAB_080d6256                         @ 080d624c 03d1
    adds r0,r6,#0x0    @ 080d624e 301c
    movs r1,#0x2    @ 080d6250 0221
    bl tick_pack_aob_frame_with_state_base   @ 080d6252 fff76ff8
LAB_080d6256:
    adds r5,#0x2    @ 080d6256 0235
    adds r4,#0x4    @ 080d6258 0434
    adds r6,#0x1    @ 080d625a 0136
    ldr r0,[sp,#0x38]                        @ 080d625c 0e98
    cmp r6,r0                                @ 080d625e 8642
    blt LAB_080d6222                         @ 080d6260 dfdb
LAB_080d6262:
    movs r0,#0x3    @ 080d6262 0320
    bl render_pack_card_slot_oam             @ 080d6264 fef78eff
    ldr r1, DAT_080d628c                     @ 080d6268 0849
    movs r2,#0xe3    @ 080d626a e322
    lsls r2,r2,#0x3    @ 080d626c d200
    adds r0,r1,r2    @ 080d626e 8818
    ldrb r0,[r0,#0x0]                        @ 080d6270 0078
    lsls r0,r0,#0x19    @ 080d6272 4006
    lsrs r0,r0,#0x1f    @ 080d6274 c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d6276 fef765fe
    ldr r0,[sp,#0x40]                        @ 080d627a 1098
    add sp,#0x4c                             @ 080d627c 13b0
    pop {r3,r4,r5}                           @ 080d627e 38bc
    .hword 0x4698    @ 080d6280 9846
    .hword 0x46a1    @ 080d6282 a146
    .hword 0x46aa    @ 080d6284 aa46
    pop {r4,r5,r6,r7}                        @ 080d6286 f0bc
    pop {r1}                                 @ 080d6288 02bc
    bx r1                                    @ 080d628a 0847
DAT_080d628c:
    .word  0x0300585c                     @ 080d628c 5c580003

@ Pack shop 'Open all' 完成时的终态处理. 通过 game_str_id_to_row(0x13f7) 取 row 1086 = 'Opened all packs.', 调 text_overlay_create 弹模态对话框 (h=10, w=30), 然后切 pack_ui_state[+0x10]=8 把 pack 状态机推到完成态. 返回 1.
pack_ui_show_all_opened_done:
    push {r4,lr}                             @ 080d6290 10b5  -- pack_ui_show_all_opened_done: 入口
    ldr r4, DAT_080d62e8                     @ 080d6292 154c  -- r4 = dialog size = (h=10 << 16) | w=30 = 0x000a001e
    ldr r0, DAT_080d62ec                     @ 080d6294 1548  -- r0 = logical string id 0x13f7
    bl game_str_id_to_row                    @ 080d6296 1ef0bffd  -- r0 = master_row (= 1086 = 'Opened all packs.')
    ldr r2, PTR_game_str_pointer_table_080d62f0 @ 080d629a 154a  -- <<< 经典 game_str lookup chain: row -> string addr (lang from gSettings) >>>
    lsls r0,r0,#0x10    @ 080d629c 0004
    lsrs r0,r0,#0x10    @ 080d629e 000c
    lsls r1,r0,#0x1    @ 080d62a0 4100
    adds r1,r1,r0    @ 080d62a2 0918
    lsls r1,r1,#0x1    @ 080d62a4 4900
    ldr r0, DAT_080d62f4                     @ 080d62a6 1348
    ldr r3, DAT_080d62f8                     @ 080d62a8 134b
    adds r0,r0,r3    @ 080d62aa c018
    ldrb r0,[r0,#0x0]                        @ 080d62ac 0078
    lsls r0,r0,#0x1d    @ 080d62ae 4007
    lsrs r0,r0,#0x1d    @ 080d62b0 400f
    adds r1,r1,r0    @ 080d62b2 0918
    lsls r1,r1,#0x2    @ 080d62b4 8900
    adds r1,r1,r2    @ 080d62b6 8918
    ldr r2,[r1,#0x0]                         @ 080d62b8 0a68  -- r2 = master[row].offset[lang]
    ldr r0, PTR_game_str_ja_080d62fc         @ 080d62ba 1048
    adds r2,r2,r0    @ 080d62bc 1218  -- r2 = STRING_TABLE_BASE + offset = 'Opened all packs.' 字符串地址
    adds r0,r4,#0x0    @ 080d62be 201c  -- r0 = size_packed (0x000a001e), r1 = flags (0), r2 = text
    movs r1,#0x0    @ 080d62c0 0021
    bl text_overlay_create                   @ 080d62c2 07f03bf9  -- text_overlay_create(size, 0, 'Opened all packs.')
    movs r0,#0x1    @ 080d62c6 0120
    bl render_pack_card_highlight_sprite     @ 080d62c8 fff780f9  -- FUN_080d55cc(1) -- pack ui helper (TODO: 命名)
    movs r0,#0x1    @ 080d62cc 0120
    bl render_pack_card_sprite_by_flip_state @ 080d62ce fef7ebf9  -- FUN_080d46a8(1) -- pack ui helper (TODO: 命名)
    movs r0,#0x3    @ 080d62d2 0320
    bl render_pack_card_slot_oam             @ 080d62d4 fef756ff  -- FUN_080d5184(3) -- pack ui helper (TODO: 命名)
    ldr r1, DAT_080d6300                     @ 080d62d8 0949
    movs r0,#0x8    @ 080d62da 0820  -- r0 = 8 (next state)
    strh r0,[r1,#0x10]                       @ 080d62dc 0882  -- pack_ui_state[+0x10] = 8  (切 pack 状态机到完成态)
    movs r0,#0x1    @ 080d62de 0120  -- r0 = 1 (return value: success)
    pop {r4}                                 @ 080d62e0 10bc
    pop {r1}                                 @ 080d62e2 02bc
    bx r1                                    @ 080d62e4 0847
    .zero  0x2
DAT_080d62e8:
    .word  0x000a001e                     @ 080d62e8 1e000a00
DAT_080d62ec:
    .word  0x000013f7                     @ 080d62ec f7130000
PTR_game_str_pointer_table_080d62f0:
    .word  game_str_pointer_table         @ 080d62f0 400f0008
DAT_080d62f4:
    .word  0x02000000                     @ 080d62f4 00000002
DAT_080d62f8:
    .word  0x00006c2c                     @ 080d62f8 2c6c0000
PTR_game_str_ja_080d62fc:
    .word  game_str_ja                    @ 080d62fc 109cdb09
DAT_080d6300:
    .word  pack_ui_state                  @ 080d6300 50580003

@ 拆包场景卡片 overlay 开场动画帧驱动. 读取 gPrng+0xa4*2=0x148 halfword 的 bit0 和 bit1: 若 bit0 或 bit1 置位则初始化 overlay: 写 [pack_ui_state+0xc+0x6]=8, BLDCNT=0x3fbf, BLDY=0, state_code=9, r4=1. 随后无条件调 tick_overlay_animation_step(0) 执行 overlay 动画一步. 末尾 render_pack_card_highlight_sprite(1) + render_pack_card_sprite_by_flip_state(1) + render_pack_card_slot_oam(3). 返回 r4 (0 或 1).
tick_pack_card_overlay_intro:
    push {r4,lr}                             @ 080d6304 10b5
    ldr r0, DAT_080d6360                     @ 080d6306 1648
    adds r2,r0,#0x0    @ 080d6308 021c
    adds r2,#0xc    @ 080d630a 0c32
    movs r4,#0x0    @ 080d630c 0024
    ldr r0, PTR_gPrng_080d6364               @ 080d630e 1548
    movs r1,#0xa4    @ 080d6310 a421
    lsls r1,r1,#0x1    @ 080d6312 4900
    adds r0,r0,r1    @ 080d6314 4018
    ldrh r1,[r0,#0x0]                        @ 080d6316 0188
    movs r0,#0x1    @ 080d6318 0120
    ands r0,r1    @ 080d631a 0840
    cmp r0,#0x0                              @ 080d631c 0028
    bne LAB_080d6328                         @ 080d631e 03d1
    movs r0,#0x2    @ 080d6320 0220
    ands r0,r1    @ 080d6322 0840
    cmp r0,#0x0                              @ 080d6324 0028
    beq LAB_080d633e                         @ 080d6326 0ad0
LAB_080d6328:
    movs r0,#0x8    @ 080d6328 0820
    strh r0,[r2,#0x6]                        @ 080d632a d080
    ldr r1, PTR_BLDCNT_080d6368              @ 080d632c 0e49
    ldr r3, DAT_080d636c                     @ 080d632e 0f4b
    adds r0,r3,#0x0    @ 080d6330 181c
    strh r0,[r1,#0x0]                        @ 080d6332 0880
    ldr r0, PTR_BLDY_080d6370                @ 080d6334 0e48
    strh r4,[r0,#0x0]                        @ 080d6336 0480
    movs r0,#0x9    @ 080d6338 0920
    strh r0,[r2,#0x4]                        @ 080d633a 9080
    movs r4,#0x1    @ 080d633c 0124
LAB_080d633e:
    movs r0,#0x0    @ 080d633e 0020
    bl tick_overlay_animation_step           @ 080d6340 07f050f9
    movs r0,#0x1    @ 080d6344 0120
    bl render_pack_card_highlight_sprite     @ 080d6346 fff741f9
    movs r0,#0x1    @ 080d634a 0120
    bl render_pack_card_sprite_by_flip_state @ 080d634c fef7acf9
    movs r0,#0x3    @ 080d6350 0320
    bl render_pack_card_slot_oam             @ 080d6352 fef717ff
    adds r0,r4,#0x0    @ 080d6356 201c
    pop {r4}                                 @ 080d6358 10bc
    pop {r1}                                 @ 080d635a 02bc
    bx r1                                    @ 080d635c 0847
    .zero  0x2
DAT_080d6360:
    .word  pack_ui_state                  @ 080d6360 50580003
PTR_gPrng_080d6364:
    .word  gPrng                          @ 080d6364 40000003
PTR_BLDCNT_080d6368:
    .word  BLDCNT                         @ 080d6368 50000004
DAT_080d636c:
    .word  0x00003fbf                     @ 080d636c bf3f0000
PTR_BLDY_080d6370:
    .word  BLDY                           @ 080d6370 54000004

@ Pack scene card reveal phase frame driver. Decrements pack_ui_state+0xc[+6] frame counter, writes BLDY=(16-counter<<4/8) for linear fade; calls tick_overlay_animation_step(0). When counter reaches zero: iterates card slot list, calls set_pack_slot_flag_bit for slots without bit7; boundary slots use get_bios_div_remainder to trigger fill_pack_card_slots_up_to_count; on completion writes BLDY=0x10, tick_overlay_animation_step(1) loop until done, writes state=0xa. Tail renders highlight/sprite/slot OAM. Returns 0=in_progress, 1=complete.
tick_pack_card_reveal_fade_in:
    push {r4,r5,r6,r7,lr}                    @ 080d6374 f0b5
    .hword 0x4657    @ 080d6376 5746
    .hword 0x464e    @ 080d6378 4e46
    .hword 0x4645    @ 080d637a 4546
    push {r5,r6,r7}                          @ 080d637c e0b4
    sub sp,#0x4                              @ 080d637e 81b0
    ldr r5, DAT_080d6448                     @ 080d6380 314d
    movs r0,#0xc    @ 080d6382 0c20
    adds r0,r0,r5    @ 080d6384 4019
    .hword 0x4681    @ 080d6386 8146
    movs r6,#0x0    @ 080d6388 0026
    ldrh r0,[r0,#0x6]                        @ 080d638a c088
    subs r0,#0x1    @ 080d638c 0138
    .hword 0x4649    @ 080d638e 4946
    strh r0,[r1,#0x6]                        @ 080d6390 c880
    movs r2,#0x6    @ 080d6392 0622
    ldrsh r0,[r1,r2]                         @ 080d6394 885e
    lsls r0,r0,#0x4    @ 080d6396 0001
    movs r1,#0x8    @ 080d6398 0821
    bl bios_div                              @ 080d639a 38f02ff8
    movs r1,#0x10    @ 080d639e 1021
    subs r1,r1,r0    @ 080d63a0 091a
    ldr r0, PTR_BLDY_080d644c                @ 080d63a2 2a48
    strh r1,[r0,#0x0]                        @ 080d63a4 0180
    movs r0,#0x0    @ 080d63a6 0020
    bl tick_overlay_animation_step           @ 080d63a8 07f01cf9
    .hword 0x4649    @ 080d63ac 4946
    movs r2,#0x6    @ 080d63ae 0622
    ldrsh r0,[r1,r2]                         @ 080d63b0 885e
    cmp r0,#0x0                              @ 080d63b2 0028
    beq LAB_080d63b8                         @ 080d63b4 00d0
    b LAB_080d64b4                           @ 080d63b6 7de0
LAB_080d63b8:
    ldr r1, DAT_080d6450                     @ 080d63b8 2549
    adds r0,r5,r1    @ 080d63ba 6818
    ldr r4,[r0,#0x0]                         @ 080d63bc 0468
    movs r2,#0xe0    @ 080d63be e022
    lsls r2,r2,#0x3    @ 080d63c0 d200
    adds r0,r5,r2    @ 080d63c2 a818
    ldr r0,[r0,#0x0]                         @ 080d63c4 0068
    .hword 0x4680    @ 080d63c6 8046
    movs r3,#0x0    @ 080d63c8 0023
    .hword 0x4648    @ 080d63ca 4846
    ldrh r0,[r0,#0xa]                        @ 080d63cc 4089
    cmp r6,r0                                @ 080d63ce 8642
    bge LAB_080d646e                         @ 080d63d0 4dda
    movs r1,#0x80    @ 080d63d2 8021
    .hword 0x468a    @ 080d63d4 8a46
LAB_080d63d6:
    movs r0,#0xde    @ 080d63d6 de20
    lsls r0,r0,#0x3    @ 080d63d8 c000
    add r0,r9                                @ 080d63da 4844
    ldr r1,[r0,#0x0]                         @ 080d63dc 0168
    lsls r0,r3,#0x2    @ 080d63de 9800
    adds r2,r0,r1    @ 080d63e0 4218
    ldrb r1,[r2,#0x0]                        @ 080d63e2 1178
    movs r0,#0x80    @ 080d63e4 8020
    ands r0,r1    @ 080d63e6 0840
    cmp r0,#0x0                              @ 080d63e8 0028
    bne LAB_080d6454                         @ 080d63ea 33d1
    .hword 0x4650    @ 080d63ec 5046
    orrs r0,r1    @ 080d63ee 0843
    strb r0,[r2,#0x0]                        @ 080d63f0 1070
    movs r5,#0x0    @ 080d63f2 0025
    adds r6,r4,#0x0    @ 080d63f4 261c
    ldmia r6!,{r0}                           @ 080d63f6 01ce
    lsls r0,r0,#0x14    @ 080d63f8 0005
    lsrs r0,r0,#0x1c    @ 080d63fa 000f
    adds r7,r3,#0x1    @ 080d63fc 5f1c
    cmp r5,r0                                @ 080d63fe 8542
    bge LAB_080d6424                         @ 080d6400 10da
LAB_080d6402:
    .hword 0x4642    @ 080d6402 4246
    adds r2,#0x4    @ 080d6404 0432
    .hword 0x4690    @ 080d6406 9046
    subs r2,#0x4    @ 080d6408 043a
    ldmia r2!,{r0}                           @ 080d640a 01ca
    lsls r0,r0,#0x10    @ 080d640c 0004
    lsrs r0,r0,#0x14    @ 080d640e 000d
    str r3,[sp,#0x0]                         @ 080d6410 0093
    bl set_pack_slot_flag_bit                @ 080d6412 06f065fb
    adds r5,#0x1    @ 080d6416 0135
    movs r0,#0xf    @ 080d6418 0f20
    ldrb r1,[r4,#0x1]                        @ 080d641a 6178
    ands r0,r1    @ 080d641c 0840
    ldr r3,[sp,#0x0]                         @ 080d641e 009b
    cmp r5,r0                                @ 080d6420 8542
    blt LAB_080d6402                         @ 080d6422 eedb
LAB_080d6424:
    .hword 0x464a    @ 080d6424 4a46
    ldrh r1,[r2,#0x1a]                       @ 080d6426 518b
    subs r0,r1,#0x1    @ 080d6428 481e
    cmp r3,r0                                @ 080d642a 8342
    blt LAB_080d6462                         @ 080d642c 19db
    adds r0,r1,#0x1    @ 080d642e 481c
    cmp r3,r0                                @ 080d6430 8342
    bgt LAB_080d6462                         @ 080d6432 16dc
    adds r0,r7,#0x0    @ 080d6434 381c
    movs r1,#0x4    @ 080d6436 0421
    bl get_bios_div_remainder                @ 080d6438 37f0e2ff
    movs r1,#0xf    @ 080d643c 0f21
    ldrb r4,[r4,#0x1]                        @ 080d643e 6478
    ands r1,r4    @ 080d6440 2140
    bl fill_pack_card_slots_up_to_count      @ 080d6442 fef755fb
    b LAB_080d6462                           @ 080d6446 0ce0
DAT_080d6448:
    .word  pack_ui_state                  @ 080d6448 50580003
PTR_BLDY_080d644c:
    .word  BLDY                           @ 080d644c 54000004
DAT_080d6450:
    .word  0x000006fc                     @ 080d6450 fc060000
LAB_080d6454:
    ldmia r4!,{r0}                           @ 080d6454 01cc
    lsls r0,r0,#0x14    @ 080d6456 0005
    lsrs r0,r0,#0x1c    @ 080d6458 000f
    lsls r0,r0,#0x2    @ 080d645a 8000
    add r8,r0                                @ 080d645c 8044
    adds r7,r3,#0x1    @ 080d645e 5f1c
    adds r6,r4,#0x0    @ 080d6460 261c
LAB_080d6462:
    adds r4,r6,#0x0    @ 080d6462 341c
    adds r3,r7,#0x0    @ 080d6464 3b1c
    .hword 0x4648    @ 080d6466 4846
    ldrh r0,[r0,#0xa]                        @ 080d6468 4089
    cmp r3,r0                                @ 080d646a 8342
    blt LAB_080d63d6                         @ 080d646c b3db
LAB_080d646e:
    movs r1,#0xe3    @ 080d646e e321
    lsls r1,r1,#0x3    @ 080d6470 c900
    add r1,r9                                @ 080d6472 4944
    movs r0,#0x8    @ 080d6474 0820
    ldrb r2,[r1,#0x0]                        @ 080d6476 0a78
    orrs r0,r2    @ 080d6478 1043
    strb r0,[r1,#0x0]                        @ 080d647a 0870
    bl render_pack_card_static_frame         @ 080d647c fff772fc
    movs r2,#0xde    @ 080d6480 de22
    lsls r2,r2,#0x3    @ 080d6482 d200
    add r2,r9                                @ 080d6484 4a44
    ldr r0, DAT_080d64d8                     @ 080d6486 1448
    add r0,r9                                @ 080d6488 4844
    ldrh r0,[r0,#0x0]                        @ 080d648a 0088
    lsls r1,r0,#0x2    @ 080d648c 8100
    ldr r0,[r2,#0x0]                         @ 080d648e 1068
    adds r4,r0,r1    @ 080d6490 4418
    adds r0,r4,#0x0    @ 080d6492 201c
    bl render_pack_label_text_by_flags       @ 080d6494 fef748fb
LAB_080d6498:
    movs r0,#0x1    @ 080d6498 0120
    bl tick_overlay_animation_step           @ 080d649a 07f0a3f8
    cmp r0,#0x0                              @ 080d649e 0028
    beq LAB_080d6498                         @ 080d64a0 fad0
    movs r1,#0x10    @ 080d64a2 1021
    .hword 0x4648    @ 080d64a4 4846
    strh r1,[r0,#0x6]                        @ 080d64a6 c180
    ldr r0, PTR_BLDY_080d64dc                @ 080d64a8 0c48
    strh r1,[r0,#0x0]                        @ 080d64aa 0180
    ldr r1, DAT_080d64e0                     @ 080d64ac 0c49
    movs r0,#0xa    @ 080d64ae 0a20
    strh r0,[r1,#0x10]                       @ 080d64b0 0882
    movs r6,#0x1    @ 080d64b2 0126
LAB_080d64b4:
    movs r0,#0x1    @ 080d64b4 0120
    bl render_pack_card_highlight_sprite     @ 080d64b6 fff789f8
    movs r0,#0x1    @ 080d64ba 0120
    bl render_pack_card_sprite_by_flip_state @ 080d64bc fef7f4f8
    movs r0,#0x3    @ 080d64c0 0320
    bl render_pack_card_slot_oam             @ 080d64c2 fef75ffe
    adds r0,r6,#0x0    @ 080d64c6 301c
    add sp,#0x4                              @ 080d64c8 01b0
    pop {r3,r4,r5}                           @ 080d64ca 38bc
    .hword 0x4698    @ 080d64cc 9846
    .hword 0x46a1    @ 080d64ce a146
    .hword 0x46aa    @ 080d64d0 aa46
    pop {r4,r5,r6,r7}                        @ 080d64d2 f0bc
    pop {r1}                                 @ 080d64d4 02bc
    bx r1                                    @ 080d64d6 0847
DAT_080d64d8:
    .word  0x000006ee                     @ 080d64d8 ee060000
PTR_BLDY_080d64dc:
    .word  BLDY                           @ 080d64dc 54000004
DAT_080d64e0:
    .word  pack_ui_state                  @ 080d64e0 50580003

@ 拆包场景卡片 BLDY 淡出动画帧驱动. 从 pack_ui_state+0xc+0x6 读帧计数器递减; 以 ldrsh 取有符号值计算 BLDY = (counter<<4)/0x10 线性递减; 写 BLDY 寄存器. 当计数器归零时: 写 BLDCNT=0x3f (清除 blend 模式), BLDY=0, state_code=2, r5=1. 末尾无条件调 render_pack_card_highlight_sprite(1) + render_pack_card_spin_oam_by_mode(1,0) + render_pack_card_sprite_by_flip_state(1) + render_pack_card_slot_oam(3). 返回 r5 (0 或 1).
tick_pack_card_bldy_fade_out:
    push {r4,r5,lr}                          @ 080d64e4 30b5
    ldr r0, DAT_080d653c                     @ 080d64e6 1548
    adds r4,r0,#0x0    @ 080d64e8 041c
    adds r4,#0xc    @ 080d64ea 0c34
    movs r5,#0x0    @ 080d64ec 0025
    ldrh r0,[r4,#0x6]                        @ 080d64ee e088
    subs r0,#0x1    @ 080d64f0 0138
    strh r0,[r4,#0x6]                        @ 080d64f2 e080
    movs r1,#0x6    @ 080d64f4 0621
    ldrsh r0,[r4,r1]                         @ 080d64f6 605e
    lsls r0,r0,#0x4    @ 080d64f8 0001
    movs r1,#0x10    @ 080d64fa 1021
    bl bios_div                              @ 080d64fc 37f07eff
    ldr r2, PTR_BLDY_080d6540                @ 080d6500 0f4a
    strh r0,[r2,#0x0]                        @ 080d6502 1080
    movs r1,#0x6    @ 080d6504 0621
    ldrsh r0,[r4,r1]                         @ 080d6506 605e
    cmp r0,#0x0                              @ 080d6508 0028
    bne LAB_080d651a                         @ 080d650a 06d1
    ldr r0, PTR_BLDCNT_080d6544              @ 080d650c 0d48
    movs r1,#0x3f    @ 080d650e 3f21
    strh r1,[r0,#0x0]                        @ 080d6510 0180
    strh r5,[r2,#0x0]                        @ 080d6512 1580
    movs r0,#0x2    @ 080d6514 0220
    strh r0,[r4,#0x4]                        @ 080d6516 a080
    movs r5,#0x1    @ 080d6518 0125
LAB_080d651a:
    movs r0,#0x1    @ 080d651a 0120
    bl render_pack_card_highlight_sprite     @ 080d651c fff756f8
    movs r0,#0x1    @ 080d6520 0120
    movs r1,#0x0    @ 080d6522 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d6524 fef7a4ff
    movs r0,#0x1    @ 080d6528 0120
    bl render_pack_card_sprite_by_flip_state @ 080d652a fef7bdf8
    movs r0,#0x3    @ 080d652e 0320
    bl render_pack_card_slot_oam             @ 080d6530 fef728fe
    adds r0,r5,#0x0    @ 080d6534 281c
    pop {r4,r5}                              @ 080d6536 30bc
    pop {r1}                                 @ 080d6538 02bc
    bx r1                                    @ 080d653a 0847
DAT_080d653c:
    .word  pack_ui_state                  @ 080d653c 50580003
PTR_BLDY_080d6540:
    .word  BLDY                           @ 080d6540 54000004
PTR_BLDCNT_080d6544:
    .word  BLDCNT                         @ 080d6544 50000004

@ 拆包场景卡片 BLDALPHA 淡入动画帧驱动 (带旋转精灵). 与 tick_pack_card_bldy_fade_out 对称: 从 pack_ui_state+0xc+0x6 读帧计数器 (有符号) 递减; 若 >0 计算 BLDALPHA = ((16-q)|q<<8) 线性淡入权重对 (q=(counter<<4)/16) 写 BLDALPHA. 若计数器 <=0: 配置 BG0CNT/BG1CNT/BG2CNT/BG3CNT priority 字段 (清 0xfffc 后 OR 1/2/3), 写 BLDCNT=0x3f/BLDALPHA=0x1010, 写 DISPCNT-0x52 = 0x80<<4=0x800 (DISPCNT 某字段), 若 r6==1 则推进 pack_ui_state+0x10=0x13. 末尾调 render_pack_card_highlight_sprite(r4) + render_pack_card_spin_oam_by_mode(r4,0) + render_pack_card_slot_oam(r4-1). 返回 r6 (sign bit of counter 初始 = 0 进行中 / 1 负完成).
tick_pack_card_bldalpha_fade_in_with_spin:
    push {r4,r5,r6,lr}                       @ 080d6548 70b5
    ldr r0, DAT_080d6584                     @ 080d654a 0e48
    adds r1,r0,#0x0    @ 080d654c 011c
    adds r1,#0xc    @ 080d654e 0c31
    movs r5,#0x1    @ 080d6550 0125
    ldrh r0,[r1,#0x6]                        @ 080d6552 c888
    subs r0,#0x1    @ 080d6554 0138
    strh r0,[r1,#0x6]                        @ 080d6556 c880
    lsls r0,r0,#0x10    @ 080d6558 0004
    asrs r0,r0,#0x10    @ 080d655a 0014
    lsrs r6,r0,#0x1f    @ 080d655c c60f
    cmp r0,#0x0                              @ 080d655e 0028
    ble LAB_080d658c                         @ 080d6560 14dd
    movs r2,#0x6    @ 080d6562 0622
    ldrsh r0,[r1,r2]                         @ 080d6564 885e
    lsls r0,r0,#0x4    @ 080d6566 0001
    movs r1,#0x10    @ 080d6568 1021
    bl bios_div                              @ 080d656a 37f047ff
    ldr r2, PTR_BLDALPHA_080d6588            @ 080d656e 064a
    movs r1,#0x10    @ 080d6570 1021
    subs r1,r1,r0    @ 080d6572 091a
    lsls r1,r1,#0x18    @ 080d6574 0906
    lsrs r1,r1,#0x18    @ 080d6576 090e
    lsls r0,r0,#0x18    @ 080d6578 0006
    lsrs r0,r0,#0x10    @ 080d657a 000c
    orrs r1,r0    @ 080d657c 0143
    strh r1,[r2,#0x0]                        @ 080d657e 1180
    b LAB_080d65e8                           @ 080d6580 32e0
    .zero  0x2
DAT_080d6584:
    .word  pack_ui_state                  @ 080d6584 50580003
PTR_BLDALPHA_080d6588:
    .word  BLDALPHA                       @ 080d6588 52000004
LAB_080d658c:
    ldr r1, PTR_BG0CNT_080d6610              @ 080d658c 2049
    ldrh r2,[r1,#0x0]                        @ 080d658e 0a88
    ldr r3, DAT_080d6614                     @ 080d6590 204b
    adds r0,r3,#0x0    @ 080d6592 181c
    ands r0,r2    @ 080d6594 1040
    strh r0,[r1,#0x0]                        @ 080d6596 0880
    ldrh r0,[r1,#0x0]                        @ 080d6598 0888
    strh r0,[r1,#0x0]                        @ 080d659a 0880
    ldr r2, PTR_BG1CNT_080d6618              @ 080d659c 1e4a
    ldrh r1,[r2,#0x0]                        @ 080d659e 1188
    adds r0,r3,#0x0    @ 080d65a0 181c
    ands r0,r1    @ 080d65a2 0840
    strh r0,[r2,#0x0]                        @ 080d65a4 1080
    ldrh r0,[r2,#0x0]                        @ 080d65a6 1088
    movs r1,#0x2    @ 080d65a8 0221
    orrs r0,r1    @ 080d65aa 0843
    strh r0,[r2,#0x0]                        @ 080d65ac 1080
    adds r2,#0x2    @ 080d65ae 0232
    ldrh r1,[r2,#0x0]                        @ 080d65b0 1188
    adds r0,r3,#0x0    @ 080d65b2 181c
    ands r0,r1    @ 080d65b4 0840
    strh r0,[r2,#0x0]                        @ 080d65b6 1080
    ldrh r0,[r2,#0x0]                        @ 080d65b8 1088
    movs r1,#0x1    @ 080d65ba 0121
    orrs r0,r1    @ 080d65bc 0843
    strh r0,[r2,#0x0]                        @ 080d65be 1080
    adds r2,#0x2    @ 080d65c0 0232
    ldrh r0,[r2,#0x0]                        @ 080d65c2 1088
    ands r3,r0    @ 080d65c4 0340
    strh r3,[r2,#0x0]                        @ 080d65c6 1380
    ldrh r0,[r2,#0x0]                        @ 080d65c8 1088
    movs r1,#0x3    @ 080d65ca 0321
    orrs r0,r1    @ 080d65cc 0843
    strh r0,[r2,#0x0]                        @ 080d65ce 1080
    movs r5,#0x0    @ 080d65d0 0025
    ldr r1, PTR_BLDCNT_080d661c              @ 080d65d2 1249
    movs r0,#0x3f    @ 080d65d4 3f20
    strh r0,[r1,#0x0]                        @ 080d65d6 0880
    adds r1,#0x2    @ 080d65d8 0231
    ldr r2, DAT_080d6620                     @ 080d65da 114a
    adds r0,r2,#0x0    @ 080d65dc 101c
    strh r0,[r1,#0x0]                        @ 080d65de 0880
    subs r1,#0x52    @ 080d65e0 5239
    movs r0,#0x80    @ 080d65e2 8020
    lsls r0,r0,#0x4    @ 080d65e4 0001
    strh r0,[r1,#0x0]                        @ 080d65e6 0880
LAB_080d65e8:
    cmp r6,#0x1                              @ 080d65e8 012e
    bne LAB_080d65f2                         @ 080d65ea 02d1
    ldr r1, DAT_080d6624                     @ 080d65ec 0d49
    movs r0,#0x13    @ 080d65ee 1320
    strh r0,[r1,#0x10]                       @ 080d65f0 0882
LAB_080d65f2:
    adds r4,r5,#0x1    @ 080d65f2 6c1c
    adds r0,r4,#0x0    @ 080d65f4 201c
    bl render_pack_card_highlight_sprite     @ 080d65f6 fef7e9ff
    adds r0,r4,#0x0    @ 080d65fa 201c
    movs r1,#0x0    @ 080d65fc 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d65fe fef737ff
    adds r0,r5,#0x3    @ 080d6602 e81c
    bl render_pack_card_slot_oam             @ 080d6604 fef7befd
    adds r0,r6,#0x0    @ 080d6608 301c
    pop {r4,r5,r6}                           @ 080d660a 70bc
    pop {r1}                                 @ 080d660c 02bc
    bx r1                                    @ 080d660e 0847
PTR_BG0CNT_080d6610:
    .word  BG0CNT                         @ 080d6610 08000004
DAT_080d6614:
    .word  0x0000fffc                     @ 080d6614 fcff0000
PTR_BG1CNT_080d6618:
    .word  BG1CNT                         @ 080d6618 0a000004
PTR_BLDCNT_080d661c:
    .word  BLDCNT                         @ 080d661c 50000004
DAT_080d6620:
    .word  0x00001010                     @ 080d6620 10100000
DAT_080d6624:
    .word  pack_ui_state                  @ 080d6624 50580003

@ 拆包场景卡片卷轴滚动并显示标签和 AOB 动画帧驱动. 入口保存 r8/r9/r10. 调 tick_pack_scroll_interp_step 返回插值完成标志 (sp[4]). 帧计数器 [+0x6] 递减; 计算 BLDY = (4-counter*4/8) 并写 BLDY 寄存器; 计算窗口宽度偏移并写 WIN0H/WIN0V/WIN1H/WIN1V. 当 tick_pack_scroll_interp_step 返回 1 (插值完成) 时: 清 [+0x6]=0, 写 WIN0V/WIN1H/WIN1V 最终值, 调 render_pack_label_text_default_pair + set_pack_scroll_step_mode(2), 清卡片状态 bit7, 更新卡名精灵行 render_pack_card_name_to_sprite_row, 推进 state=0xd. 末尾无条件调 render_pack_card_highlight_sprite(1) + render_pack_card_spin_oam_by_mode(1,0) + render_pack_card_sprite_by_flip_state(1) + tick_pack_aob_frame_loop + render_pack_card_slot_oam(3). 返回 sp[4] (插值步骤结果).
tick_pack_card_scroll_label_with_aob:
    push {r4,r5,r6,r7,lr}                    @ 080d6628 f0b5
    .hword 0x4657    @ 080d662a 5746
    .hword 0x464e    @ 080d662c 4e46
    .hword 0x4645    @ 080d662e 4546
    push {r5,r6,r7}                          @ 080d6630 e0b4
    sub sp,#0x8                              @ 080d6632 82b0
    ldr r7, DAT_080d6744                     @ 080d6634 434f
    adds r4,r7,#0x0    @ 080d6636 3c1c
    adds r4,#0xc    @ 080d6638 0c34
    ldr r1, DAT_080d6748                     @ 080d663a 4349
    adds r0,r7,r1    @ 080d663c 7818
    ldr r0,[r0,#0x0]                         @ 080d663e 0068
    str r0,[sp,#0x0]                         @ 080d6640 0090
    bl tick_pack_scroll_interp_step          @ 080d6642 fef741f9
    str r0,[sp,#0x4]                         @ 080d6646 0190
    ldrh r0,[r4,#0x6]                        @ 080d6648 e088
    subs r0,#0x1    @ 080d664a 0138
    strh r0,[r4,#0x6]                        @ 080d664c e080
    movs r2,#0x6    @ 080d664e 0622
    ldrsh r0,[r4,r2]                         @ 080d6650 a05e
    lsls r0,r0,#0x2    @ 080d6652 8000
    movs r1,#0x8    @ 080d6654 0821
    bl bios_div                              @ 080d6656 37f0d1fe
    ldr r5, PTR_BLDY_080d674c                @ 080d665a 3c4d
    .hword 0x46aa    @ 080d665c aa46
    movs r1,#0x4    @ 080d665e 0421
    .hword 0x4689    @ 080d6660 8946
    .hword 0x464a    @ 080d6662 4a46
    subs r0,r2,r0    @ 080d6664 101a
    strh r0,[r5,#0x0]                        @ 080d6666 2880
    movs r5,#0x6    @ 080d6668 0625
    ldrsh r0,[r4,r5]                         @ 080d666a 605f
    lsls r0,r0,#0x5    @ 080d666c 4001
    movs r1,#0x8    @ 080d666e 0821
    bl bios_div                              @ 080d6670 37f0c4fe
    movs r2,#0x20    @ 080d6674 2022
    subs r2,r2,r0    @ 080d6676 121a
    ldr r0, PTR_WIN0H_080d6750               @ 080d6678 3548
    .hword 0x4680    @ 080d667a 8046
    movs r3,#0xf0    @ 080d667c f023
    strh r3,[r0,#0x0]                        @ 080d667e 0380
    ldr r1, PTR_WIN0V_080d6754               @ 080d6680 3449
    .hword 0x468c    @ 080d6682 8c46
    adds r0,r2,#0x0    @ 080d6684 101c
    adds r0,#0x10    @ 080d6686 1030
    lsls r0,r0,#0x18    @ 080d6688 0006
    lsrs r0,r0,#0x18    @ 080d668a 000e
    movs r5,#0x80    @ 080d668c 8025
    lsls r5,r5,#0x5    @ 080d668e 6d01
    adds r1,r5,#0x0    @ 080d6690 291c
    orrs r0,r1    @ 080d6692 0843
    .hword 0x4661    @ 080d6694 6146
    strh r0,[r1,#0x0]                        @ 080d6696 0880
    ldr r5, PTR_WIN1H_080d6758               @ 080d6698 2f4d
    strh r3,[r5,#0x0]                        @ 080d669a 2b80
    ldr r6, PTR_WIN1V_080d675c               @ 080d669c 2f4e
    movs r1,#0x70    @ 080d669e 7021
    rsbs r1,r1,#0    @ 080d66a0 4942
    adds r0,r1,#0x0    @ 080d66a2 081c
    subs r0,r0,r2    @ 080d66a4 801a
    lsls r0,r0,#0x18    @ 080d66a6 0006
    lsrs r0,r0,#0x10    @ 080d66a8 000c
    movs r1,#0x90    @ 080d66aa 9021
    orrs r0,r1    @ 080d66ac 0843
    strh r0,[r6,#0x0]                        @ 080d66ae 3080
    ldr r2,[sp,#0x4]                         @ 080d66b0 019a
    cmp r2,#0x1                              @ 080d66b2 012a
    bne LAB_080d6700                         @ 080d66b4 24d1
    movs r0,#0x0    @ 080d66b6 0020
    strh r0,[r4,#0x6]                        @ 080d66b8 e080
    .hword 0x4649    @ 080d66ba 4946
    .hword 0x4650    @ 080d66bc 5046
    strh r1,[r0,#0x0]                        @ 080d66be 0180
    .hword 0x4642    @ 080d66c0 4246
    strh r3,[r2,#0x0]                        @ 080d66c2 1380
    ldr r1, DAT_080d6760                     @ 080d66c4 2649
    adds r0,r1,#0x0    @ 080d66c6 081c
    .hword 0x4662    @ 080d66c8 6246
    strh r0,[r2,#0x0]                        @ 080d66ca 1080
    strh r3,[r5,#0x0]                        @ 080d66cc 2b80
    ldr r5, DAT_080d6764                     @ 080d66ce 254d
    adds r0,r5,#0x0    @ 080d66d0 281c
    strh r0,[r6,#0x0]                        @ 080d66d2 3080
    bl render_pack_label_text_default_pair   @ 080d66d4 fef754fa
    movs r0,#0x2    @ 080d66d8 0220
    bl set_pack_scroll_step_mode             @ 080d66da fef74df9
    ldr r0, DAT_080d6768                     @ 080d66de 2248
    adds r1,r7,r0    @ 080d66e0 3918
    movs r0,#0x7f    @ 080d66e2 7f20
    ldrb r2,[r1,#0x0]                        @ 080d66e4 0a78
    ands r0,r2    @ 080d66e6 1040
    strb r0,[r1,#0x0]                        @ 080d66e8 0870
    ldr r5,[sp,#0x0]                         @ 080d66ea 009d
    ldr r1,[r5,#0x0]                         @ 080d66ec 2968
    lsls r0,r1,#0x10    @ 080d66ee 0804
    lsrs r0,r0,#0x14    @ 080d66f0 000d
    lsls r1,r1,#0x1d    @ 080d66f2 4907
    lsrs r1,r1,#0x1d    @ 080d66f4 490f
    movs r2,#0x0    @ 080d66f6 0022
    bl render_pack_card_name_to_sprite_row   @ 080d66f8 fef774fb
    movs r0,#0xd    @ 080d66fc 0d20
    strh r0,[r4,#0x4]                        @ 080d66fe a080
LAB_080d6700:
    movs r0,#0x1    @ 080d6700 0120
    bl render_pack_card_highlight_sprite     @ 080d6702 fef763ff
    movs r0,#0x1    @ 080d6706 0120
    movs r1,#0x0    @ 080d6708 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d670a fef7b1fe
    movs r0,#0x1    @ 080d670e 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6710 fdf7caff
    ldr r0, DAT_080d676c                     @ 080d6714 1548
    adds r2,r7,r0    @ 080d6716 3a18
    ldr r1, DAT_080d6770                     @ 080d6718 1549
    adds r0,r7,r1    @ 080d671a 7818
    ldrh r0,[r0,#0x0]                        @ 080d671c 0088
    lsls r1,r0,#0x2    @ 080d671e 8100
    ldr r0,[r2,#0x0]                         @ 080d6720 1068
    adds r0,r0,r1    @ 080d6722 4018
    ldr r1,[sp,#0x0]                         @ 080d6724 0099
    movs r2,#0x2    @ 080d6726 0222
    bl tick_pack_aob_frame_loop              @ 080d6728 fef720fe
    movs r0,#0x3    @ 080d672c 0320
    bl render_pack_card_slot_oam             @ 080d672e fef729fd
    ldr r0,[sp,#0x4]                         @ 080d6732 0198
    add sp,#0x8                              @ 080d6734 02b0
    pop {r3,r4,r5}                           @ 080d6736 38bc
    .hword 0x4698    @ 080d6738 9846
    .hword 0x46a1    @ 080d673a a146
    .hword 0x46aa    @ 080d673c aa46
    pop {r4,r5,r6,r7}                        @ 080d673e f0bc
    pop {r1}                                 @ 080d6740 02bc
    bx r1                                    @ 080d6742 0847
DAT_080d6744:
    .word  pack_ui_state                  @ 080d6744 50580003
DAT_080d6748:
    .word  0x00000704                     @ 080d6748 04070000
PTR_BLDY_080d674c:
    .word  BLDY                           @ 080d674c 54000004
PTR_WIN0H_080d6750:
    .word  WIN0H                          @ 080d6750 40000004
PTR_WIN0V_080d6754:
    .word  WIN0V                          @ 080d6754 44000004
PTR_WIN1H_080d6758:
    .word  WIN1H                          @ 080d6758 42000004
PTR_WIN1V_080d675c:
    .word  WIN1V                          @ 080d675c 46000004
DAT_080d6760:
    .word  0x00001030                     @ 080d6760 30100000
DAT_080d6764:
    .word  0x00007090                     @ 080d6764 90700000
DAT_080d6768:
    .word  0x00000724                     @ 080d6768 24070000
DAT_080d676c:
    .word  0x000006fc                     @ 080d676c fc060000
DAT_080d6770:
    .word  0x000006fa                     @ 080d6770 fa060000

@ 拆包场景翻到下一张卡的转场. 先调 init_pack_scroll_animation(0x14, 0x50, 8) 启动横向滚动动画 (起点 0x14, 终点 0x50, 步进 8), 然后读取 pack_ui_state+0x724 状态字节的最高位 (bit7) 作为方向标志, 以 (0,0,方向) 调 render_pack_card_name_to_sprite_row 重绘卡名精灵行, 最后将 pack_ui_state+0xc 区 [+0x6] 滚动计数写为 8 重置动画进度. 供拆包翻页状态机在选择下一卡时调用.
open_pack_next_card_with_scroll:
    push {r4,r5,lr}                          @ 080d6774 30b5
    ldr r4, DAT_080d67a0                     @ 080d6776 0a4c
    adds r5,r4,#0x0    @ 080d6778 251c
    adds r5,#0xc    @ 080d677a 0c35
    movs r0,#0x14    @ 080d677c 1420
    movs r1,#0x50    @ 080d677e 5021
    movs r2,#0x8    @ 080d6780 0822
    bl init_pack_scroll_animation            @ 080d6782 fef701f9
    ldr r0, DAT_080d67a4                     @ 080d6786 0748
    adds r4,r4,r0    @ 080d6788 2418
    ldrb r4,[r4,#0x0]                        @ 080d678a 2478
    lsrs r2,r4,#0x7    @ 080d678c e209
    movs r0,#0x0    @ 080d678e 0020
    movs r1,#0x0    @ 080d6790 0021
    bl render_pack_card_name_to_sprite_row   @ 080d6792 fef727fb
    movs r0,#0x8    @ 080d6796 0820
    strh r0,[r5,#0x6]                        @ 080d6798 e880
    pop {r4,r5}                              @ 080d679a 30bc
    pop {r0}                                 @ 080d679c 01bc
    bx r0                                    @ 080d679e 0047
DAT_080d67a0:
    .word  pack_ui_state                  @ 080d67a0 50580003
DAT_080d67a4:
    .word  0x00000724                     @ 080d67a4 24070000

@ Pack scene card page-scroll frame driver with nav input dispatch. Reads gPrng+0x148 status_flags. bit1: open_pack_next_card_with_scroll + sync_state; writes step=0xf. bits[7:4]: dispatches 4 paths by direction bit: forward/back/last/new, each calls tick_pack_card_image_scroll_forward/back or init_pack_scroll_animation + sync_state. On end-of-pack or no-more-cards calls sync_state(2) and sets bit. Tail renders highlight/spin/flip/slot OAM + name/hue scroll. Dispatched by tick_pack_card_info_step jump table.
tick_pack_card_scroll_by_nav_input:
    push {r4,r5,r6,r7,lr}                    @ 080d67a8 f0b5
    .hword 0x4657    @ 080d67aa 5746
    .hword 0x464e    @ 080d67ac 4e46
    .hword 0x4645    @ 080d67ae 4546
    push {r5,r6,r7}                          @ 080d67b0 e0b4
    sub sp,#0x8                              @ 080d67b2 82b0
    ldr r4, DAT_080d682c                     @ 080d67b4 1d4c
    adds r5,r4,#0x0    @ 080d67b6 251c
    adds r5,#0xc    @ 080d67b8 0c35
    movs r0,#0x0    @ 080d67ba 0020
    .hword 0x4680    @ 080d67bc 8046
    movs r1,#0x1    @ 080d67be 0121
    str r1,[sp,#0x4]                         @ 080d67c0 0191
    .hword 0x468a    @ 080d67c2 8a46
    ldr r2, DAT_080d6830                     @ 080d67c4 1a4a
    adds r2,r2,r4    @ 080d67c6 1219
    .hword 0x4691    @ 080d67c8 9146
    ldr r3, DAT_080d6834                     @ 080d67ca 1a4b
    adds r7,r4,r3    @ 080d67cc e718
    ldrh r0,[r7,#0x0]                        @ 080d67ce 3888
    lsls r1,r0,#0x2    @ 080d67d0 8100
    ldr r0,[r2,#0x0]                         @ 080d67d2 1068
    adds r0,r0,r1    @ 080d67d4 4018
    str r0,[sp,#0x0]                         @ 080d67d6 0090
    ldr r0, PTR_gPrng_080d6838               @ 080d67d8 1748
    movs r1,#0xa4    @ 080d67da a421
    lsls r1,r1,#0x1    @ 080d67dc 4900
    adds r6,r0,r1    @ 080d67de 4618
    movs r0,#0x2    @ 080d67e0 0220
    ldrh r2,[r6,#0x0]                        @ 080d67e2 3288
    ands r0,r2    @ 080d67e4 1040
    cmp r0,#0x0                              @ 080d67e6 0028
    beq LAB_080d680a                         @ 080d67e8 0fd0
    bl open_pack_next_card_with_scroll       @ 080d67ea fff7c3ff
    movs r0,#0x1    @ 080d67ee 0120
    bl sync_state_and_init_sprite            @ 080d67f0 23f060f9
    ldr r3, DAT_080d683c                     @ 080d67f4 114b
    adds r0,r4,r3    @ 080d67f6 e018
    movs r1,#0x21    @ 080d67f8 2121
    rsbs r1,r1,#0    @ 080d67fa 4942
    ldrb r2,[r0,#0x0]                        @ 080d67fc 0278
    ands r1,r2    @ 080d67fe 1140
    strb r1,[r0,#0x0]                        @ 080d6800 0170
    movs r0,#0xf    @ 080d6802 0f20
    strh r0,[r5,#0x4]                        @ 080d6804 a880
    movs r3,#0x1    @ 080d6806 0123
    .hword 0x4698    @ 080d6808 9846
LAB_080d680a:
    ldrh r1,[r6,#0x0]                        @ 080d680a 3188
    .hword 0x4650    @ 080d680c 5046
    ands r0,r1    @ 080d680e 0840
    cmp r0,#0x0                              @ 080d6810 0028
    beq LAB_080d6840                         @ 080d6812 15d0
    movs r0,#0x24    @ 080d6814 2420
    bl sync_state_and_init_sprite            @ 080d6816 23f04df9
    ldr r1, DAT_080d683c                     @ 080d681a 0849
    adds r0,r4,r1    @ 080d681c 6018
    movs r1,#0x21    @ 080d681e 2121
    rsbs r1,r1,#0    @ 080d6820 4942
    ldrb r2,[r0,#0x0]                        @ 080d6822 0278
    ands r1,r2    @ 080d6824 1140
    strb r1,[r0,#0x0]                        @ 080d6826 0170
    movs r0,#0x10    @ 080d6828 1020
    b LAB_080d68f6                           @ 080d682a 64e0
DAT_080d682c:
    .word  pack_ui_state                  @ 080d682c 50580003
DAT_080d6830:
    .word  0x000006fc                     @ 080d6830 fc060000
DAT_080d6834:
    .word  0x000006fa                     @ 080d6834 fa060000
PTR_gPrng_080d6838:
    .word  gPrng                          @ 080d6838 40000003
DAT_080d683c:
    .word  0x00000724                     @ 080d683c 24070000
LAB_080d6840:
    movs r0,#0xf0    @ 080d6840 f020
    ands r0,r1    @ 080d6842 0840
    cmp r0,#0x0                              @ 080d6844 0028
    bne LAB_080d684a                         @ 080d6846 00d1
    b LAB_080d69fe                           @ 080d6848 d9e0
LAB_080d684a:
    movs r0,#0x10    @ 080d684a 1020
    ands r0,r1    @ 080d684c 0840
    cmp r0,#0x0                              @ 080d684e 0028
    beq LAB_080d6880                         @ 080d6850 16d0
    ldrh r1,[r5,#0x18]                       @ 080d6852 298b
    movs r0,#0xf    @ 080d6854 0f20
    ldr r2,[sp,#0x0]                         @ 080d6856 009a
    ldrb r2,[r2,#0x1]                        @ 080d6858 5278
    ands r0,r2    @ 080d685a 1040
    subs r0,#0x1    @ 080d685c 0138
    cmp r1,r0                                @ 080d685e 8142
    bge LAB_080d6874                         @ 080d6860 08da
    adds r0,r1,#0x1    @ 080d6862 481c
    movs r1,#0x5    @ 080d6864 0521
    bl get_bios_div_remainder                @ 080d6866 37f0cbfd
    cmp r0,#0x0                              @ 080d686a 0028
    beq LAB_080d68c2                         @ 080d686c 29d0
    ldrh r0,[r5,#0x18]                       @ 080d686e 288b
    adds r0,#0x1    @ 080d6870 0130
    b LAB_080d689e                           @ 080d6872 14e0
LAB_080d6874:
    ldr r3, DAT_080d687c                     @ 080d6874 014b
    adds r4,r4,r3    @ 080d6876 e418
    movs r0,#0x20    @ 080d6878 2020
    b LAB_080d69e8                           @ 080d687a b5e0
DAT_080d687c:
    .word  0x00000724                     @ 080d687c 24070000
LAB_080d6880:
    movs r3,#0x20    @ 080d6880 2023
    adds r0,r3,#0x0    @ 080d6882 181c
    ands r0,r1    @ 080d6884 0840
    cmp r0,#0x0                              @ 080d6886 0028
    beq LAB_080d6904                         @ 080d6888 3cd0
    ldrh r0,[r5,#0x18]                       @ 080d688a 288b
    cmp r0,#0x0                              @ 080d688c 0028
    beq LAB_080d68dc                         @ 080d688e 25d0
    movs r1,#0x5    @ 080d6890 0521
    bl get_bios_div_remainder                @ 080d6892 37f0b5fd
    cmp r0,#0x0                              @ 080d6896 0028
    beq LAB_080d68c2                         @ 080d6898 13d0
    ldrh r0,[r5,#0x18]                       @ 080d689a 288b
    subs r0,#0x1    @ 080d689c 0138
LAB_080d689e:
    strh r0,[r5,#0x18]                       @ 080d689e 2883
    ldrh r0,[r5,#0x18]                       @ 080d68a0 288b
    movs r1,#0x5    @ 080d68a2 0521
    bl get_bios_div_remainder                @ 080d68a4 37f0acfd
    adds r1,r0,#0x0    @ 080d68a8 011c
    lsls r0,r1,#0x2    @ 080d68aa 8800
    adds r0,r0,r1    @ 080d68ac 4018
    adds r0,#0x7    @ 080d68ae 0730
    lsls r0,r0,#0x3    @ 080d68b0 c000
    movs r1,#0x50    @ 080d68b2 5021
    movs r2,#0x8    @ 080d68b4 0822
    bl init_pack_scroll_animation            @ 080d68b6 fef767f8
    movs r0,#0xe    @ 080d68ba 0e20
    strh r0,[r5,#0x4]                        @ 080d68bc a880
    movs r3,#0x1    @ 080d68be 0123
    .hword 0x4698    @ 080d68c0 9846
LAB_080d68c2:
    movs r0,#0x0    @ 080d68c2 0020
    bl sync_state_and_init_sprite            @ 080d68c4 23f0f6f8
    ldr r0, DAT_080d68d8                     @ 080d68c8 0348
    adds r1,r4,r0    @ 080d68ca 2118
    movs r0,#0x21    @ 080d68cc 2120
    rsbs r0,r0,#0    @ 080d68ce 4042
    ldrb r2,[r1,#0x0]                        @ 080d68d0 0a78
    ands r0,r2    @ 080d68d2 1040
    strb r0,[r1,#0x0]                        @ 080d68d4 0870
    b LAB_080d69fe                           @ 080d68d6 92e0
DAT_080d68d8:
    .word  0x00000724                     @ 080d68d8 24070000
LAB_080d68dc:
    bl open_pack_next_card_with_scroll       @ 080d68dc fff74aff
    movs r0,#0x1    @ 080d68e0 0120
    bl sync_state_and_init_sprite            @ 080d68e2 23f0e7f8
    ldr r3, DAT_080d6900                     @ 080d68e6 064b
    adds r0,r4,r3    @ 080d68e8 e018
    movs r1,#0x21    @ 080d68ea 2121
    rsbs r1,r1,#0    @ 080d68ec 4942
    ldrb r2,[r0,#0x0]                        @ 080d68ee 0278
    ands r1,r2    @ 080d68f0 1140
    strb r1,[r0,#0x0]                        @ 080d68f2 0170
    movs r0,#0xf    @ 080d68f4 0f20
LAB_080d68f6:
    strh r0,[r5,#0x4]                        @ 080d68f6 a880
    movs r3,#0x1    @ 080d68f8 0123
    .hword 0x4698    @ 080d68fa 9846
    b LAB_080d69fe                           @ 080d68fc 7fe0
    .zero  0x2
DAT_080d6900:
    .word  0x00000724                     @ 080d6900 24070000
LAB_080d6904:
    movs r2,#0x80    @ 080d6904 8022
    adds r0,r2,#0x0    @ 080d6906 101c
    ands r0,r1    @ 080d6908 0840
    cmp r0,#0x0                              @ 080d690a 0028
    beq LAB_080d6962                         @ 080d690c 29d0
    ldrh r0,[r5,#0xa]                        @ 080d690e 6889
    subs r0,#0x1    @ 080d6910 0138
    ldrh r1,[r5,#0x1a]                       @ 080d6912 698b
    cmp r1,r0                                @ 080d6914 8142
    bge LAB_080d69e2                         @ 080d6916 64da
    ldrh r7,[r7,#0x0]                        @ 080d6918 3f88
    lsls r1,r7,#0x2    @ 080d691a b900
    .hword 0x464b    @ 080d691c 4b46
    ldr r0,[r3,#0x0]                         @ 080d691e 1868
    adds r1,r0,r1    @ 080d6920 4118
    adds r0,r2,#0x0    @ 080d6922 101c
    ldrb r2,[r1,#0x4]                        @ 080d6924 0a79
    ands r0,r2    @ 080d6926 1040
    cmp r0,#0x0                              @ 080d6928 0028
    beq LAB_080d6944                         @ 080d692a 0bd0
    movs r0,#0xf    @ 080d692c 0f20
    ldrb r1,[r1,#0x5]                        @ 080d692e 4979
    ands r0,r1    @ 080d6930 0840
    ldrh r3,[r5,#0x18]                       @ 080d6932 2b8b
    cmp r3,r0                                @ 080d6934 8342
    bcs LAB_080d6944                         @ 080d6936 05d2
    movs r0,#0x0    @ 080d6938 0020
    str r0,[sp,#0x4]                         @ 080d693a 0190
    .hword 0x4682    @ 080d693c 8246
    bl tick_pack_card_image_scroll_forward   @ 080d693e fef72bf9
    b LAB_080d699c                           @ 080d6942 2be0
LAB_080d6944:
    movs r1,#0xe3    @ 080d6944 e321
    lsls r1,r1,#0x3    @ 080d6946 c900
    adds r4,r5,r1    @ 080d6948 6c18
    movs r0,#0x20    @ 080d694a 2020
    ldrb r2,[r4,#0x0]                        @ 080d694c 2278
    ands r0,r2    @ 080d694e 1040
    cmp r0,#0x0                              @ 080d6950 0028
    bne LAB_080d69fe                         @ 080d6952 54d1
    movs r0,#0x2    @ 080d6954 0220
    bl sync_state_and_init_sprite            @ 080d6956 23f0adf8
    movs r0,#0x20    @ 080d695a 2020
    ldrb r3,[r4,#0x0]                        @ 080d695c 2378
    orrs r0,r3    @ 080d695e 1843
    b LAB_080d69fc                           @ 080d6960 4ce0
LAB_080d6962:
    movs r0,#0x40    @ 080d6962 4020
    ands r0,r1    @ 080d6964 0840
    cmp r0,#0x0                              @ 080d6966 0028
    beq LAB_080d69fe                         @ 080d6968 49d0
    ldrh r0,[r5,#0x1a]                       @ 080d696a 688b
    cmp r0,#0x0                              @ 080d696c 0028
    beq LAB_080d69e2                         @ 080d696e 38d0
    ldrh r7,[r7,#0x0]                        @ 080d6970 3f88
    lsls r0,r7,#0x2    @ 080d6972 b800
    .hword 0x464b    @ 080d6974 4b46
    ldr r1,[r3,#0x0]                         @ 080d6976 1968
    adds r1,r1,r0    @ 080d6978 0918
    subs r1,#0x4    @ 080d697a 0439
    adds r0,r2,#0x0    @ 080d697c 101c
    ldrb r2,[r1,#0x0]                        @ 080d697e 0a78
    ands r0,r2    @ 080d6980 1040
    cmp r0,#0x0                              @ 080d6982 0028
    beq LAB_080d69c4                         @ 080d6984 1ed0
    movs r0,#0xf    @ 080d6986 0f20
    ldrb r1,[r1,#0x1]                        @ 080d6988 4978
    ands r0,r1    @ 080d698a 0840
    ldrh r3,[r5,#0x18]                       @ 080d698c 2b8b
    cmp r3,r0                                @ 080d698e 8342
    bcs LAB_080d69c4                         @ 080d6990 18d2
    movs r0,#0x0    @ 080d6992 0020
    str r0,[sp,#0x4]                         @ 080d6994 0190
    .hword 0x4682    @ 080d6996 8246
    bl tick_pack_card_image_scroll_back      @ 080d6998 fef75ef9
LAB_080d699c:
    movs r0,#0x0    @ 080d699c 0020
    bl sync_state_and_init_sprite            @ 080d699e 23f089f8
    ldr r1, DAT_080d69c0                     @ 080d69a2 0749
    adds r2,r4,r1    @ 080d69a4 6218
    movs r0,#0x21    @ 080d69a6 2120
    rsbs r0,r0,#0    @ 080d69a8 4042
    ldrb r3,[r2,#0x0]                        @ 080d69aa 1378
    ands r0,r3    @ 080d69ac 1840
    movs r1,#0x10    @ 080d69ae 1021
    orrs r0,r1    @ 080d69b0 0843
    strb r0,[r2,#0x0]                        @ 080d69b2 1070
    movs r0,#0x3    @ 080d69b4 0320
    strh r0,[r5,#0x4]                        @ 080d69b6 a880
    movs r0,#0x1    @ 080d69b8 0120
    .hword 0x4680    @ 080d69ba 8046
    b LAB_080d69fe                           @ 080d69bc 1fe0
    .zero  0x2
DAT_080d69c0:
    .word  0x00000724                     @ 080d69c0 24070000
LAB_080d69c4:
    movs r1,#0xe3    @ 080d69c4 e321
    lsls r1,r1,#0x3    @ 080d69c6 c900
    adds r4,r5,r1    @ 080d69c8 6c18
    movs r0,#0x20    @ 080d69ca 2020
    ldrb r2,[r4,#0x0]                        @ 080d69cc 2278
    ands r0,r2    @ 080d69ce 1040
    cmp r0,#0x0                              @ 080d69d0 0028
    bne LAB_080d69fe                         @ 080d69d2 14d1
    movs r0,#0x2    @ 080d69d4 0220
    bl sync_state_and_init_sprite            @ 080d69d6 23f06df8
    movs r0,#0x20    @ 080d69da 2020
    ldrb r3,[r4,#0x0]                        @ 080d69dc 2378
    orrs r0,r3    @ 080d69de 1843
    b LAB_080d69fc                           @ 080d69e0 0ce0
LAB_080d69e2:
    ldr r0, DAT_080d6a88                     @ 080d69e2 2948
    adds r4,r4,r0    @ 080d69e4 2418
    adds r0,r3,#0x0    @ 080d69e6 181c
LAB_080d69e8:
    ldrb r1,[r4,#0x0]                        @ 080d69e8 2178
    ands r0,r1    @ 080d69ea 0840
    cmp r0,#0x0                              @ 080d69ec 0028
    bne LAB_080d69fe                         @ 080d69ee 06d1
    movs r0,#0x2    @ 080d69f0 0220
    bl sync_state_and_init_sprite            @ 080d69f2 23f05ff8
    movs r0,#0x20    @ 080d69f6 2020
    ldrb r2,[r4,#0x0]                        @ 080d69f8 2278
    orrs r0,r2    @ 080d69fa 1043
LAB_080d69fc:
    strb r0,[r4,#0x0]                        @ 080d69fc 2070
LAB_080d69fe:
    .hword 0x4643    @ 080d69fe 4346
    cmp r3,#0x1                              @ 080d6a00 012b
    beq LAB_080d6a16                         @ 080d6a02 08d0
    ldr r0, PTR_gPrng_080d6a8c               @ 080d6a04 2148
    movs r2,#0xa3    @ 080d6a06 a322
    lsls r2,r2,#0x1    @ 080d6a08 5200
    adds r1,r0,r2    @ 080d6a0a 8118
    movs r0,#0xf0    @ 080d6a0c f020
    ldrh r1,[r1,#0x0]                        @ 080d6a0e 0988
    ands r0,r1    @ 080d6a10 0840
    cmp r0,#0x0                              @ 080d6a12 0028
    bne LAB_080d6a26                         @ 080d6a14 07d1
LAB_080d6a16:
    movs r3,#0xe3    @ 080d6a16 e323
    lsls r3,r3,#0x3    @ 080d6a18 db00
    adds r1,r5,r3    @ 080d6a1a e918
    movs r0,#0x21    @ 080d6a1c 2120
    rsbs r0,r0,#0    @ 080d6a1e 4042
    ldrb r2,[r1,#0x0]                        @ 080d6a20 0a78
    ands r0,r2    @ 080d6a22 1040
    strb r0,[r1,#0x0]                        @ 080d6a24 0870
LAB_080d6a26:
    movs r0,#0x1    @ 080d6a26 0120
    bl render_pack_card_highlight_sprite     @ 080d6a28 fef7d0fd
    ldr r3,[sp,#0x4]                         @ 080d6a2c 019b
    cmp r3,#0x1                              @ 080d6a2e 012b
    bne LAB_080d6a3a                         @ 080d6a30 03d1
    movs r0,#0x1    @ 080d6a32 0120
    movs r1,#0x0    @ 080d6a34 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d6a36 fef71bfd
LAB_080d6a3a:
    movs r0,#0x1    @ 080d6a3a 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6a3c fdf734fe
    .hword 0x4650    @ 080d6a40 5046
    cmp r0,#0x1                              @ 080d6a42 0128
    bne LAB_080d6a56                         @ 080d6a44 07d1
    movs r1,#0xdf    @ 080d6a46 df21
    lsls r1,r1,#0x3    @ 080d6a48 c900
    adds r0,r5,r1    @ 080d6a4a 6818
    ldr r1,[r0,#0x0]                         @ 080d6a4c 0168
    ldr r0,[sp,#0x0]                         @ 080d6a4e 0098
    movs r2,#0x2    @ 080d6a50 0222
    bl tick_pack_aob_frame_loop              @ 080d6a52 fef78bfc
LAB_080d6a56:
    movs r0,#0x3    @ 080d6a56 0320
    bl render_pack_card_slot_oam             @ 080d6a58 fef794fb
    movs r2,#0xe3    @ 080d6a5c e322
    lsls r2,r2,#0x3    @ 080d6a5e d200
    adds r4,r5,r2    @ 080d6a60 ac18
    ldrb r3,[r4,#0x0]                        @ 080d6a62 2378
    lsls r0,r3,#0x19    @ 080d6a64 5806
    lsrs r0,r0,#0x1f    @ 080d6a66 c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d6a68 fef76cfa
    ldrb r4,[r4,#0x0]                        @ 080d6a6c 2478
    lsrs r0,r4,#0x7    @ 080d6a6e e009
    bl tick_pack_bg_palette_hue_scroll       @ 080d6a70 fef798fa
    .hword 0x4640    @ 080d6a74 4046
    add sp,#0x8                              @ 080d6a76 02b0
    pop {r3,r4,r5}                           @ 080d6a78 38bc
    .hword 0x4698    @ 080d6a7a 9846
    .hword 0x46a1    @ 080d6a7c a146
    .hword 0x46aa    @ 080d6a7e aa46
    pop {r4,r5,r6,r7}                        @ 080d6a80 f0bc
    pop {r1}                                 @ 080d6a82 02bc
    bx r1                                    @ 080d6a84 0847
    .zero  0x2
DAT_080d6a88:
    .word  0x00000724                     @ 080d6a88 24070000
PTR_gPrng_080d6a8c:
    .word  gPrng                          @ 080d6a8c 40000003

@ Pack scene card scroll final-step frame driver. Calls tick_pack_scroll_interp_step; when interpolation complete: reads slot_index to compute card_ptr; toggles [+0x724] bit7 direction flag; extracts card_id/display_flag then calls render_pack_card_name_to_sprite_row to update card name sprite row; writes state=0xd to advance scene step. Tail renders highlight/spin/flip/slot OAM + name/hue scroll. Returns 0=interpolation_in_progress, 1=complete. Dispatched by tick_pack_card_info_step jump table.
tick_pack_card_scroll_final_step:
    push {r4,r5,r6,r7,lr}                    @ 080d6a90 f0b5
    .hword 0x4647    @ 080d6a92 4746
    push {r7}                                @ 080d6a94 80b4
    ldr r6, DAT_080d6b3c                     @ 080d6a96 294e
    movs r0,#0xc    @ 080d6a98 0c20
    adds r0,r0,r6    @ 080d6a9a 8019
    .hword 0x4680    @ 080d6a9c 8046
    bl tick_pack_scroll_interp_step          @ 080d6a9e fdf713ff
    adds r7,r0,#0x0    @ 080d6aa2 071c
    cmp r7,#0x1                              @ 080d6aa4 012f
    bne LAB_080d6ae2                         @ 080d6aa6 1cd1
    ldr r1, DAT_080d6b40                     @ 080d6aa8 2549
    adds r0,r6,r1    @ 080d6aaa 7018
    .hword 0x4642    @ 080d6aac 4246
    ldrh r2,[r2,#0x18]                       @ 080d6aae 128b
    lsls r1,r2,#0x2    @ 080d6ab0 9100
    ldr r3,[r0,#0x0]                         @ 080d6ab2 0368
    adds r3,r3,r1    @ 080d6ab4 5b18
    ldr r0, DAT_080d6b44                     @ 080d6ab6 2348
    adds r5,r6,r0    @ 080d6ab8 3518
    ldrb r4,[r5,#0x0]                        @ 080d6aba 2c78
    lsrs r0,r4,#0x7    @ 080d6abc e009
    movs r1,#0x1    @ 080d6abe 0121
    eors r0,r1    @ 080d6ac0 4840
    lsls r0,r0,#0x7    @ 080d6ac2 c001
    movs r2,#0x7f    @ 080d6ac4 7f22
    ands r2,r4    @ 080d6ac6 2240
    orrs r2,r0    @ 080d6ac8 0243
    strb r2,[r5,#0x0]                        @ 080d6aca 2a70
    ldr r1,[r3,#0x0]                         @ 080d6acc 1968
    lsls r0,r1,#0x10    @ 080d6ace 0804
    lsrs r0,r0,#0x14    @ 080d6ad0 000d
    lsls r1,r1,#0x1d    @ 080d6ad2 4907
    lsrs r1,r1,#0x1d    @ 080d6ad4 490f
    lsrs r2,r2,#0x7    @ 080d6ad6 d209
    bl render_pack_card_name_to_sprite_row   @ 080d6ad8 fef784f9
    movs r0,#0xd    @ 080d6adc 0d20
    .hword 0x4641    @ 080d6ade 4146
    strh r0,[r1,#0x4]                        @ 080d6ae0 8880
LAB_080d6ae2:
    movs r0,#0x1    @ 080d6ae2 0120
    bl render_pack_card_highlight_sprite     @ 080d6ae4 fef772fd
    movs r0,#0x1    @ 080d6ae8 0120
    movs r1,#0x0    @ 080d6aea 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d6aec fef7c0fc
    movs r0,#0x1    @ 080d6af0 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6af2 fdf7d9fd
    ldr r3, DAT_080d6b48                     @ 080d6af6 144b
    adds r2,r6,r3    @ 080d6af8 f218
    ldr r1, DAT_080d6b4c                     @ 080d6afa 1449
    adds r0,r6,r1    @ 080d6afc 7018
    ldrh r0,[r0,#0x0]                        @ 080d6afe 0088
    lsls r1,r0,#0x2    @ 080d6b00 8100
    ldr r0,[r2,#0x0]                         @ 080d6b02 1068
    adds r0,r0,r1    @ 080d6b04 4018
    ldr r2, DAT_080d6b40                     @ 080d6b06 0e4a
    adds r1,r6,r2    @ 080d6b08 b118
    ldr r1,[r1,#0x0]                         @ 080d6b0a 0968
    movs r2,#0x2    @ 080d6b0c 0222
    bl tick_pack_aob_frame_loop              @ 080d6b0e fef72dfc
    movs r0,#0x3    @ 080d6b12 0320
    bl render_pack_card_slot_oam             @ 080d6b14 fef736fb
    ldr r3, DAT_080d6b44                     @ 080d6b18 0a4b
    adds r4,r6,r3    @ 080d6b1a f418
    ldrb r1,[r4,#0x0]                        @ 080d6b1c 2178
    lsls r0,r1,#0x19    @ 080d6b1e 4806
    lsrs r0,r0,#0x1f    @ 080d6b20 c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d6b22 fef70ffa
    ldrb r4,[r4,#0x0]                        @ 080d6b26 2478
    lsrs r0,r4,#0x7    @ 080d6b28 e009
    bl tick_pack_bg_palette_hue_scroll       @ 080d6b2a fef73bfa
    adds r0,r7,#0x0    @ 080d6b2e 381c
    pop {r3}                                 @ 080d6b30 08bc
    .hword 0x4698    @ 080d6b32 9846
    pop {r4,r5,r6,r7}                        @ 080d6b34 f0bc
    pop {r1}                                 @ 080d6b36 02bc
    bx r1                                    @ 080d6b38 0847
    .zero  0x2
DAT_080d6b3c:
    .word  pack_ui_state                  @ 080d6b3c 50580003
DAT_080d6b40:
    .word  0x00000704                     @ 080d6b40 04070000
DAT_080d6b44:
    .word  0x00000724                     @ 080d6b44 24070000
DAT_080d6b48:
    .word  0x000006fc                     @ 080d6b48 fc060000
DAT_080d6b4c:
    .word  0x000006fa                     @ 080d6b4c fa060000

@ 拆包场景卡片滚动并填充卡槽 + AOB 帧驱动. 入口保存 r8/r9/r10. 从 pack_ui_state [+0x704]/[+0x6fa] 取渲染指针和 slot_index 定位当前卡槽描述符 r6. 调 tick_pack_scroll_interp_step (sp[0]). 帧计数器 [+0x6] 递减; 计算 BLDY = (counter*4/8) 写 BLDY; 计算窗口偏移写 WIN0H/WIN0V/WIN1H/WIN1V (与 tick_pack_card_scroll_label_with_aob 对称的窗口计算). 当 tick_pack_scroll_interp_step=1 时: 调 render_pack_label_text_by_flags(card_ptr) + set_pack_scroll_step_mode(0) + 清 [+0x18]=0 + get_bios_div_remainder + fill_pack_card_slots_up_to_count + 写 BLDCNT=0x23f + 清 WIN0H/WIN1H/WIN1V + 配置 WININ=0x3f3f + 写 WIN0V=0xa000/WIN1V=0xf0 + 清 DISPCNT window bits + 推进 state=2. 末尾 render_pack_card_highlight_sprite(1) + render_pack_card_spin_oam_by_mode(1,0) + render_pack_card_sprite_by_flip_state(1) + tick_pack_aob_frame_loop + render_pack_card_slot_oam(3). 返回 sp[0] (tick 结果).
tick_pack_card_scroll_slot_fill_with_aob:
    push {r4,r5,r6,r7,lr}                    @ 080d6b50 f0b5
    .hword 0x4657    @ 080d6b52 5746
    .hword 0x464e    @ 080d6b54 4e46
    .hword 0x4645    @ 080d6b56 4546
    push {r5,r6,r7}                          @ 080d6b58 e0b4
    sub sp,#0x4                              @ 080d6b5a 81b0
    ldr r7, PTR_pack_ui_state_080d6c88       @ 080d6b5c 4a4f
    adds r4,r7,#0x0    @ 080d6b5e 3c1c
    adds r4,#0xc    @ 080d6b60 0c34
    ldr r0, PTR_DAT_080d6c8c                 @ 080d6b62 4a48
    ldrh r0,[r0,#0x0]                        @ 080d6b64 0088
    lsls r1,r0,#0x2    @ 080d6b66 8100
    ldr r2, PTR_DAT_080d6c90                 @ 080d6b68 494a
    ldr r0,[r2,#0x0]                         @ 080d6b6a 1068
    adds r6,r0,r1    @ 080d6b6c 4618
    bl tick_pack_scroll_interp_step          @ 080d6b6e fdf7abfe
    str r0,[sp,#0x0]                         @ 080d6b72 0090
    ldrh r0,[r4,#0x6]                        @ 080d6b74 e088
    subs r0,#0x1    @ 080d6b76 0138
    strh r0,[r4,#0x6]                        @ 080d6b78 e080
    movs r3,#0x6    @ 080d6b7a 0623
    ldrsh r0,[r4,r3]                         @ 080d6b7c e05e
    lsls r0,r0,#0x2    @ 080d6b7e 8000
    movs r1,#0x8    @ 080d6b80 0821
    bl bios_div                              @ 080d6b82 37f03bfc
    ldr r1, PTR_BLDY_080d6c94                @ 080d6b86 4349
    .hword 0x468a    @ 080d6b88 8a46
    strh r0,[r1,#0x0]                        @ 080d6b8a 0880
    movs r2,#0x6    @ 080d6b8c 0622
    ldrsh r0,[r4,r2]                         @ 080d6b8e a05e
    lsls r0,r0,#0x5    @ 080d6b90 4001
    movs r1,#0x8    @ 080d6b92 0821
    bl bios_div                              @ 080d6b94 37f032fc
    movs r5,#0xf0    @ 080d6b98 f025
    ldr r3, PTR_WIN0H_080d6c98               @ 080d6b9a 3f4b
    strh r5,[r3,#0x0]                        @ 080d6b9c 1d80
    adds r1,r0,#0x0    @ 080d6b9e 011c
    adds r1,#0x10    @ 080d6ba0 1031
    lsls r1,r1,#0x18    @ 080d6ba2 0906
    lsrs r1,r1,#0x18    @ 080d6ba4 090e
    movs r3,#0x80    @ 080d6ba6 8023
    lsls r3,r3,#0x5    @ 080d6ba8 5b01
    adds r2,r3,#0x0    @ 080d6baa 1a1c
    orrs r1,r2    @ 080d6bac 1143
    ldr r2, PTR_WIN0V_080d6c9c               @ 080d6bae 3b4a
    strh r1,[r2,#0x0]                        @ 080d6bb0 1180
    ldr r3, PTR_WIN1H_080d6ca0               @ 080d6bb2 3b4b
    .hword 0x4699    @ 080d6bb4 9946
    strh r5,[r3,#0x0]                        @ 080d6bb6 1d80
    ldr r1, PTR_WIN1V_080d6ca4               @ 080d6bb8 3a49
    .hword 0x4688    @ 080d6bba 8846
    movs r2,#0x70    @ 080d6bbc 7022
    rsbs r2,r2,#0    @ 080d6bbe 5242
    adds r1,r2,#0x0    @ 080d6bc0 111c
    subs r1,r1,r0    @ 080d6bc2 091a
    lsls r1,r1,#0x18    @ 080d6bc4 0906
    lsrs r1,r1,#0x10    @ 080d6bc6 090c
    movs r0,#0x90    @ 080d6bc8 9020
    orrs r1,r0    @ 080d6bca 0143
    .hword 0x4643    @ 080d6bcc 4346
    strh r1,[r3,#0x0]                        @ 080d6bce 1980
    ldr r0,[sp,#0x0]                         @ 080d6bd0 0098
    cmp r0,#0x1                              @ 080d6bd2 0128
    bne LAB_080d6c42                         @ 080d6bd4 35d1
    adds r0,r6,#0x0    @ 080d6bd6 301c
    bl render_pack_label_text_by_flags       @ 080d6bd8 fdf7a6ff
    movs r0,#0x0    @ 080d6bdc 0020
    bl set_pack_scroll_step_mode             @ 080d6bde fdf7cbfe
    movs r1,#0x0    @ 080d6be2 0021
    strh r1,[r4,#0x18]                       @ 080d6be4 2183
    ldrh r0,[r4,#0x1a]                       @ 080d6be6 608b
    adds r0,#0x1    @ 080d6be8 0130
    movs r1,#0x4    @ 080d6bea 0421
    bl get_bios_div_remainder                @ 080d6bec 37f008fc
    movs r1,#0xf    @ 080d6bf0 0f21
    ldrb r6,[r6,#0x1]                        @ 080d6bf2 7678
    ands r1,r6    @ 080d6bf4 3140
    bl fill_pack_card_slots_up_to_count      @ 080d6bf6 fdf77bff
    ldr r1, PTR_BLDCNT_080d6ca8              @ 080d6bfa 2b49
    ldr r2, DAT_080d6cac                     @ 080d6bfc 2b4a
    adds r0,r2,#0x0    @ 080d6bfe 101c
    strh r0,[r1,#0x0]                        @ 080d6c00 0880
    movs r0,#0x0    @ 080d6c02 0020
    .hword 0x4653    @ 080d6c04 5346
    strh r0,[r3,#0x0]                        @ 080d6c06 1880
    adds r1,#0x2    @ 080d6c08 0231
    movs r0,#0x10    @ 080d6c0a 1020
    strh r0,[r1,#0x0]                        @ 080d6c0c 0880
    ldr r0, PTR_WININ_080d6cb0               @ 080d6c0e 2848
    ldr r2, DAT_080d6cb4                     @ 080d6c10 284a
    adds r1,r2,#0x0    @ 080d6c12 111c
    strh r1,[r0,#0x0]                        @ 080d6c14 0180
    adds r0,#0x2    @ 080d6c16 0230
    strh r1,[r0,#0x0]                        @ 080d6c18 0180
    ldr r3, PTR_WIN0H_080d6c98               @ 080d6c1a 1f4b
    strh r5,[r3,#0x0]                        @ 080d6c1c 1d80
    movs r0,#0xa0    @ 080d6c1e a020
    ldr r1, PTR_WIN0V_080d6c9c               @ 080d6c20 1e49
    strh r0,[r1,#0x0]                        @ 080d6c22 0880
    .hword 0x464a    @ 080d6c24 4a46
    strh r5,[r2,#0x0]                        @ 080d6c26 1580
    .hword 0x4643    @ 080d6c28 4346
    strh r0,[r3,#0x0]                        @ 080d6c2a 1880
    subs r1,#0x44    @ 080d6c2c 4439
    ldrh r2,[r1,#0x0]                        @ 080d6c2e 0a88
    ldr r0, DAT_080d6cb8                     @ 080d6c30 2148
    ands r0,r2    @ 080d6c32 1040
    strh r0,[r1,#0x0]                        @ 080d6c34 0880
    ldrh r2,[r1,#0x0]                        @ 080d6c36 0a88
    ldr r0, DAT_080d6cbc                     @ 080d6c38 2048
    ands r0,r2    @ 080d6c3a 1040
    strh r0,[r1,#0x0]                        @ 080d6c3c 0880
    movs r0,#0x2    @ 080d6c3e 0220
    strh r0,[r4,#0x4]                        @ 080d6c40 a080
LAB_080d6c42:
    movs r0,#0x1    @ 080d6c42 0120
    bl render_pack_card_highlight_sprite     @ 080d6c44 fef7c2fc
    movs r0,#0x1    @ 080d6c48 0120
    movs r1,#0x0    @ 080d6c4a 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d6c4c fef710fc
    movs r0,#0x1    @ 080d6c50 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6c52 fdf729fd
    ldr r0, PTR_DAT_080d6c8c                 @ 080d6c56 0d48
    ldrh r0,[r0,#0x0]                        @ 080d6c58 0088
    lsls r1,r0,#0x2    @ 080d6c5a 8100
    ldr r2, PTR_DAT_080d6c90                 @ 080d6c5c 0c4a
    ldr r0,[r2,#0x0]                         @ 080d6c5e 1068
    adds r0,r0,r1    @ 080d6c60 4018
    ldr r3, DAT_080d6cc0                     @ 080d6c62 174b
    adds r1,r7,r3    @ 080d6c64 f918
    ldr r1,[r1,#0x0]                         @ 080d6c66 0968
    movs r2,#0x2    @ 080d6c68 0222
    bl tick_pack_aob_frame_loop              @ 080d6c6a fef77ffb
    movs r0,#0x3    @ 080d6c6e 0320
    bl render_pack_card_slot_oam             @ 080d6c70 fef788fa
    ldr r0,[sp,#0x0]                         @ 080d6c74 0098
    add sp,#0x4                              @ 080d6c76 01b0
    pop {r3,r4,r5}                           @ 080d6c78 38bc
    .hword 0x4698    @ 080d6c7a 9846
    .hword 0x46a1    @ 080d6c7c a146
    .hword 0x46aa    @ 080d6c7e aa46
    pop {r4,r5,r6,r7}                        @ 080d6c80 f0bc
    pop {r1}                                 @ 080d6c82 02bc
    bx r1                                    @ 080d6c84 0847
    .zero  0x2
PTR_pack_ui_state_080d6c88:
    .word  pack_ui_state                  @ 080d6c88 50580003
PTR_DAT_080d6c8c:
    .word  0x03005f4a                     @ 080d6c8c 4a5f0003
PTR_DAT_080d6c90:
    .word  0x03005f4c                     @ 080d6c90 4c5f0003
PTR_BLDY_080d6c94:
    .word  BLDY                           @ 080d6c94 54000004
PTR_WIN0H_080d6c98:
    .word  WIN0H                          @ 080d6c98 40000004
PTR_WIN0V_080d6c9c:
    .word  WIN0V                          @ 080d6c9c 44000004
PTR_WIN1H_080d6ca0:
    .word  WIN1H                          @ 080d6ca0 42000004
PTR_WIN1V_080d6ca4:
    .word  WIN1V                          @ 080d6ca4 46000004
PTR_BLDCNT_080d6ca8:
    .word  BLDCNT                         @ 080d6ca8 50000004
DAT_080d6cac:
    .word  0x0000023f                     @ 080d6cac 3f020000
PTR_WININ_080d6cb0:
    .word  WININ                          @ 080d6cb0 48000004
DAT_080d6cb4:
    .word  0x00003f3f                     @ 080d6cb4 3f3f0000
DAT_080d6cb8:
    .word  0x0000dfff                     @ 080d6cb8 ffdf0000
DAT_080d6cbc:
    .word  0x0000bfff                     @ 080d6cbc ffbf0000
DAT_080d6cc0:
    .word  0x00000704                     @ 080d6cc0 04070000

@ Called when user selects a card in pack list UI, switches to card info detail page. Sets blend registers BLDCNT=0xff (all layer blend source), BLDALPHA=0x10; clears DISPCNT window bits (AND 0xdfff; AND 0xbfff). Reads selected card data pointer from pack_ui_state+0x704 list struct, extracts card_id. Calls card_list_on_select_to_info_page to trigger card detail page load. Writes pack_ui_state+0xc+0x4 := 0x11 (state machine switches to state 0x11). Returns r0=1.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - LIST_STRUCT_OFFSET = 0x704 (card list substruct offset)
@ - +0x18: selected_item_index (halfword)
@ - BLDCNT = 0x04000050 (blend control register)
@ - BLDCNT_VAL = 0xff (all layer blend enabled)
@ - BLDALPHA_VAL = 0x10
@ - WIN_MASK_A = 0xdfff (clear bit13), WIN_MASK_B = 0xbfff (clear bit14)
@ - DISPCNT = 0x04000000
@ - STATE_INFO_PAGE = 0x11 (pack state machine: entered info page)
enter_pack_card_info_page:
    push {r4,lr}                             @ 080d6cc4 10b5
    ldr r0, DAT_080d6d14                     @ 080d6cc6 1348
    adds r4,r0,#0x0    @ 080d6cc8 041c
    adds r4,#0xc    @ 080d6cca 0c34
    ldr r1, DAT_080d6d18                     @ 080d6ccc 1249
    adds r0,r0,r1    @ 080d6cce 4018
    ldrh r2,[r4,#0x18]                       @ 080d6cd0 228b
    lsls r1,r2,#0x2    @ 080d6cd2 9100
    ldr r3,[r0,#0x0]                         @ 080d6cd4 0368
    adds r3,r3,r1    @ 080d6cd6 5b18
    ldr r1, PTR_BLDCNT_080d6d1c              @ 080d6cd8 1049
    movs r0,#0xff    @ 080d6cda ff20
    strh r0,[r1,#0x0]                        @ 080d6cdc 0880
    adds r1,#0x4    @ 080d6cde 0431
    movs r0,#0x10    @ 080d6ce0 1020
    strh r0,[r1,#0x0]                        @ 080d6ce2 0880
    subs r1,#0x54    @ 080d6ce4 5439
    ldrh r2,[r1,#0x0]                        @ 080d6ce6 0a88
    ldr r0, DAT_080d6d20                     @ 080d6ce8 0d48
    ands r0,r2    @ 080d6cea 1040
    strh r0,[r1,#0x0]                        @ 080d6cec 0880
    ldrh r2,[r1,#0x0]                        @ 080d6cee 0a88
    ldr r0, DAT_080d6d24                     @ 080d6cf0 0c48
    ands r0,r2    @ 080d6cf2 1040
    strh r0,[r1,#0x0]                        @ 080d6cf4 0880
    ldr r0,[r3,#0x0]                         @ 080d6cf6 1868
    lsls r0,r0,#0x10    @ 080d6cf8 0004
    lsrs r0,r0,#0x14    @ 080d6cfa 000d
    ldr r2, DAT_080d6d28                     @ 080d6cfc 0a4a
    ldr r3, DAT_080d6d2c                     @ 080d6cfe 0b4b
    movs r1,#0x0    @ 080d6d00 0021
    bl card_list_on_select_to_info_page      @ 080d6d02 47f79dfc
    movs r0,#0x11    @ 080d6d06 1120
    strh r0,[r4,#0x4]                        @ 080d6d08 a080
    movs r0,#0x1    @ 080d6d0a 0120
    pop {r4}                                 @ 080d6d0c 10bc
    pop {r1}                                 @ 080d6d0e 02bc
    bx r1                                    @ 080d6d10 0847
    .zero  0x2
DAT_080d6d14:
    .word  pack_ui_state                  @ 080d6d14 50580003
DAT_080d6d18:
    .word  0x00000704                     @ 080d6d18 04070000
PTR_BLDCNT_080d6d1c:
    .word  BLDCNT                         @ 080d6d1c 50000004
DAT_080d6d20:
    .word  0x0000dfff                     @ 080d6d20 ffdf0000
DAT_080d6d24:
    .word  0x0000bfff                     @ 080d6d24 ffbf0000
DAT_080d6d28:
    .word  0x02035fb0                     @ 080d6d28 b05f0302
DAT_080d6d2c:
    .word  0x0200af20                     @ 080d6d2c 20af0002

@ 拆包场景卡片详情页初始化帧驱动. 入口保存 r8/r9/r10. 调 tick_card_info_page_by_state 驱动信息页状态机; 若返回非 1 则直接返回 0. 返回 1 后执行完整的详情页加载序列: 清 DISPCNT, 调 load_pack_detail_bg3_tileset + init_pack_scene_bg_and_vram 初始化 BG; 从卡槽描述符读已拥有数+slot count 设置遍历范围; 对每个 slot [-(max-1)..+(max+1)] 调 dispatch_pack_card_image_render_by_state 渲染卡图; 从 pack_banner_obj_palette 复制调色板到 OBJ PAL (0x05000200) 和 (0x05000000 区域); 调 render_pack_name_to_obj_sprite_row + render_pack_card_name_to_sprite_row + render_pack_owned_count_to_sprite_row + render_pack_label_name_to_sprite_row + init_pack_card_aob_display_row + dispatch_pack_aob_frame_loop_by_reset; 复制 BG palette + load tiles; 调 set_pack_scroll_start_pos + set_pack_scroll_step_mode(2) + copy_pack_card_palette_to_obj_pal + render_pack_label_text_default_pair + refresh_overlay_palette_row; 写 pack_ui_state+0x10=0x12 推进状态. 返回 r4 (0 等待/1 初始化完成).
tick_pack_card_detail_page_setup:
    push {r4,r5,r6,r7,lr}                    @ 080d6d30 f0b5
    .hword 0x4657    @ 080d6d32 5746
    .hword 0x464e    @ 080d6d34 4e46
    .hword 0x4645    @ 080d6d36 4546
    push {r5,r6,r7}                          @ 080d6d38 e0b4
    sub sp,#0xc                              @ 080d6d3a 83b0
    ldr r5, DAT_080d6d9c                     @ 080d6d3c 174d
    movs r0,#0xc    @ 080d6d3e 0c20
    adds r0,r0,r5    @ 080d6d40 4019
    .hword 0x4681    @ 080d6d42 8146
    movs r4,#0x0    @ 080d6d44 0024
    bl tick_card_info_page_by_state          @ 080d6d46 47f7e5fc
    cmp r0,#0x1                              @ 080d6d4a 0128
    beq LAB_080d6d50                         @ 080d6d4c 00d0
    b LAB_080d6ef8                           @ 080d6d4e d3e0
LAB_080d6d50:
    movs r0,#0x80    @ 080d6d50 8020
    lsls r0,r0,#0x13    @ 080d6d52 c004
    strh r4,[r0,#0x0]                        @ 080d6d54 0480
    bl load_pack_detail_bg3_tileset          @ 080d6d56 04f051fe
    bl init_pack_scene_bg_and_vram           @ 080d6d5a fdf73ffe
    .hword 0x4649    @ 080d6d5e 4946
    ldrh r1,[r1,#0x1a]                       @ 080d6d60 498b
    lsls r0,r1,#0x6    @ 080d6d62 8801
    adds r0,#0x10    @ 080d6d64 1030
    movs r1,#0xff    @ 080d6d66 ff21
    ands r0,r1    @ 080d6d68 0840
    .hword 0x464a    @ 080d6d6a 4a46
    strh r0,[r2,#0x3e]                       @ 080d6d6c d087
    bl load_pack_bg_tiles_and_palette        @ 080d6d6e fdf7d5ff
    ldr r0, DAT_080d6da0                     @ 080d6d72 0b48
    adds r2,r5,r0    @ 080d6d74 2a18
    ldr r1, DAT_080d6da4                     @ 080d6d76 0b49
    adds r0,r5,r1    @ 080d6d78 6818
    ldrh r0,[r0,#0x0]                        @ 080d6d7a 0088
    lsls r1,r0,#0x2    @ 080d6d7c 8100
    ldr r0,[r2,#0x0]                         @ 080d6d7e 1068
    adds r0,r0,r1    @ 080d6d80 4018
    subs r6,r0,#0x4    @ 080d6d82 061f
    ldr r2, DAT_080d6da8                     @ 080d6d84 084a
    adds r1,r5,r2    @ 080d6d86 a918
    movs r0,#0xf    @ 080d6d88 0f20
    ldrb r2,[r6,#0x1]                        @ 080d6d8a 7278
    ands r0,r2    @ 080d6d8c 1040
    lsls r0,r0,#0x2    @ 080d6d8e 8000
    ldr r1,[r1,#0x0]                         @ 080d6d90 0968
    subs r7,r1,r0    @ 080d6d92 0f1a
    .hword 0x4649    @ 080d6d94 4946
    ldrh r0,[r1,#0x1a]                       @ 080d6d96 488b
    subs r5,r0,#0x1    @ 080d6d98 451e
    b LAB_080d6de4                           @ 080d6d9a 23e0
DAT_080d6d9c:
    .word  pack_ui_state                  @ 080d6d9c 50580003
DAT_080d6da0:
    .word  0x000006fc                     @ 080d6da0 fc060000
DAT_080d6da4:
    .word  0x000006fa                     @ 080d6da4 fa060000
DAT_080d6da8:
    .word  0x00000704                     @ 080d6da8 04070000
LAB_080d6dac:
    adds r4,r5,#0x1    @ 080d6dac 6c1c
    adds r0,r4,#0x0    @ 080d6dae 201c
    movs r1,#0x4    @ 080d6db0 0421
    bl get_bios_div_remainder                @ 080d6db2 37f025fb
    cmp r5,#0x0                              @ 080d6db6 002d
    blt LAB_080d6dcc                         @ 080d6db8 08db
    .hword 0x464a    @ 080d6dba 4a46
    ldrh r2,[r2,#0xa]                        @ 080d6dbc 5289
    cmp r5,r2                                @ 080d6dbe 9542
    bge LAB_080d6dcc                         @ 080d6dc0 04da
    adds r1,r6,#0x0    @ 080d6dc2 311c
    adds r2,r7,#0x0    @ 080d6dc4 3a1c
    bl dispatch_pack_card_image_render_by_state @ 080d6dc6 fdf749fe
    b LAB_080d6dd4                           @ 080d6dca 03e0
LAB_080d6dcc:
    movs r1,#0x0    @ 080d6dcc 0021
    movs r2,#0x0    @ 080d6dce 0022
    bl dispatch_pack_card_image_render_by_state @ 080d6dd0 fdf744fe
LAB_080d6dd4:
    ldmia r6!,{r0}                           @ 080d6dd4 01ce
    lsls r0,r0,#0x14    @ 080d6dd6 0005
    lsrs r0,r0,#0x1c    @ 080d6dd8 000f
    lsls r0,r0,#0x2    @ 080d6dda 8000
    adds r7,r7,r0    @ 080d6ddc 3f18
    adds r5,r4,#0x0    @ 080d6dde 251c
    .hword 0x4649    @ 080d6de0 4946
    ldrh r0,[r1,#0x1a]                       @ 080d6de2 488b
LAB_080d6de4:
    adds r0,#0x2    @ 080d6de4 0230
    cmp r5,r0                                @ 080d6de6 8542
    blt LAB_080d6dac                         @ 080d6de8 e0db
    ldr r0, DAT_080d6f0c                     @ 080d6dea 4848
    ldr r4, PTR_pack_banner_obj_palette_080d6f10 @ 080d6dec 484c
    movs r5,#0x90    @ 080d6dee 9025
    lsls r5,r5,#0x1    @ 080d6df0 6d00
    adds r1,r4,#0x0    @ 080d6df2 211c
    adds r2,r5,#0x0    @ 080d6df4 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d6df6 1ef087f8
    movs r0,#0xa0    @ 080d6dfa a020
    lsls r0,r0,#0x13    @ 080d6dfc c004
    adds r1,r4,#0x0    @ 080d6dfe 211c
    adds r2,r5,#0x0    @ 080d6e00 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d6e02 1ef081f8
    movs r2,#0xde    @ 080d6e06 de22
    lsls r2,r2,#0x3    @ 080d6e08 d200
    add r2,r9                                @ 080d6e0a 4a44
    .hword 0x4690    @ 080d6e0c 9046
    ldr r0, DAT_080d6f14                     @ 080d6e0e 4148
    add r0,r9                                @ 080d6e10 4844
    .hword 0x4682    @ 080d6e12 8246
    ldrh r2,[r0,#0x0]                        @ 080d6e14 0288
    lsls r1,r2,#0x2    @ 080d6e16 9100
    .hword 0x4642    @ 080d6e18 4246
    ldr r0,[r2,#0x0]                         @ 080d6e1a 1068
    adds r6,r0,r1    @ 080d6e1c 4618
    ldr r0,[r6,#0x0]                         @ 080d6e1e 3068
    lsls r0,r0,#0x19    @ 080d6e20 4006
    lsrs r0,r0,#0x19    @ 080d6e22 400e
    movs r4,#0xe3    @ 080d6e24 e324
    lsls r4,r4,#0x3    @ 080d6e26 e400
    add r4,r9                                @ 080d6e28 4c44
    ldrb r2,[r4,#0x0]                        @ 080d6e2a 2278
    lsls r1,r2,#0x19    @ 080d6e2c 5106
    lsrs r1,r1,#0x1f    @ 080d6e2e c90f
    bl render_pack_name_to_obj_sprite_row    @ 080d6e30 fdf7b2ff
    movs r5,#0xdf    @ 080d6e34 df25
    lsls r5,r5,#0x3    @ 080d6e36 ed00
    add r5,r9                                @ 080d6e38 4d44
    .hword 0x4648    @ 080d6e3a 4846
    ldrh r0,[r0,#0x18]                       @ 080d6e3c 008b
    lsls r1,r0,#0x2    @ 080d6e3e 8100
    ldr r0,[r5,#0x0]                         @ 080d6e40 2868
    adds r7,r0,r1    @ 080d6e42 4718
    ldr r1,[r7,#0x0]                         @ 080d6e44 3968
    lsls r0,r1,#0x10    @ 080d6e46 0804
    lsrs r0,r0,#0x14    @ 080d6e48 000d
    lsls r1,r1,#0x1d    @ 080d6e4a 4907
    lsrs r1,r1,#0x1d    @ 080d6e4c 490f
    ldrb r4,[r4,#0x0]                        @ 080d6e4e 2478
    lsrs r2,r4,#0x7    @ 080d6e50 e209
    bl render_pack_card_name_to_sprite_row   @ 080d6e52 fdf7c7ff
    ldr r0,[r6,#0x0]                         @ 080d6e56 3068
    lsls r0,r0,#0x19    @ 080d6e58 4006
    lsrs r0,r0,#0x19    @ 080d6e5a 400e
    ldr r4, DAT_080d6f18                     @ 080d6e5c 2e4c
    add r4,r9                                @ 080d6e5e 4c44
    ldrb r2,[r4,#0x0]                        @ 080d6e60 2278
    lsls r1,r2,#0x1e    @ 080d6e62 9107
    lsrs r1,r1,#0x1f    @ 080d6e64 c90f
    bl render_pack_owned_count_to_sprite_row @ 080d6e66 fdf7efff
    ldr r0,[r6,#0x0]                         @ 080d6e6a 3068
    lsls r0,r0,#0x19    @ 080d6e6c 4006
    lsrs r0,r0,#0x19    @ 080d6e6e 400e
    ldrb r4,[r4,#0x0]                        @ 080d6e70 2478
    lsls r1,r4,#0x1f    @ 080d6e72 e107
    lsrs r1,r1,#0x1f    @ 080d6e74 c90f
    bl render_pack_label_name_to_sprite_row  @ 080d6e76 fef709f8
    bl init_pack_card_aob_display_row        @ 080d6e7a fef733f9
    .hword 0x4650    @ 080d6e7e 5046
    ldrh r0,[r0,#0x0]                        @ 080d6e80 0088
    lsls r1,r0,#0x2    @ 080d6e82 8100
    .hword 0x4642    @ 080d6e84 4246
    ldr r0,[r2,#0x0]                         @ 080d6e86 1068
    adds r6,r0,r1    @ 080d6e88 4618
    ldr r7,[r5,#0x0]                         @ 080d6e8a 2f68
    adds r0,r6,#0x0    @ 080d6e8c 301c
    adds r1,r7,#0x0    @ 080d6e8e 391c
    bl dispatch_pack_aob_frame_loop_by_reset @ 080d6e90 fef7cafa
    ldr r0, DAT_080d6f1c                     @ 080d6e94 2148
    ldr r1, DAT_080d6f20                     @ 080d6e96 2249
    movs r2,#0x20    @ 080d6e98 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d6e9a 1ef035f8
    movs r0,#0xe8    @ 080d6e9e e820
    lsls r0,r0,#0x1    @ 080d6ea0 4000
    movs r1,#0xa    @ 080d6ea2 0a21
    bl load_pack_card_tile_row_to_obj_vram   @ 080d6ea4 05f068fa
    movs r0,#0xee    @ 080d6ea8 ee20
    lsls r0,r0,#0x1    @ 080d6eaa 4000
    str r0,[sp,#0x0]                         @ 080d6eac 0090
    movs r0,#0x1    @ 080d6eae 0120
    rsbs r0,r0,#0    @ 080d6eb0 4042
    str r0,[sp,#0x4]                         @ 080d6eb2 0190
    movs r0,#0xec    @ 080d6eb4 ec20
    lsls r0,r0,#0x1    @ 080d6eb6 4000
    str r0,[sp,#0x8]                         @ 080d6eb8 0290
    .hword 0x4668    @ 080d6eba 6846
    movs r1,#0x9    @ 080d6ebc 0921
    bl load_pack_card_tiles_to_vram          @ 080d6ebe fdf79dfb
    .hword 0x4649    @ 080d6ec2 4946
    ldrh r0,[r1,#0x18]                       @ 080d6ec4 088b
    movs r1,#0x5    @ 080d6ec6 0521
    bl get_bios_div_remainder                @ 080d6ec8 37f09afa
    adds r1,r0,#0x0    @ 080d6ecc 011c
    lsls r0,r1,#0x2    @ 080d6ece 8800
    adds r0,r0,r1    @ 080d6ed0 4018
    adds r0,#0x7    @ 080d6ed2 0730
    lsls r0,r0,#0x3    @ 080d6ed4 c000
    movs r1,#0x50    @ 080d6ed6 5021
    bl set_pack_scroll_start_pos             @ 080d6ed8 fdf732fd
    movs r0,#0x2    @ 080d6edc 0220
    bl set_pack_scroll_step_mode             @ 080d6ede fdf74bfd
    movs r0,#0xb    @ 080d6ee2 0b20
    bl copy_pack_card_palette_to_obj_pal     @ 080d6ee4 05f082fb
    bl render_pack_label_text_default_pair   @ 080d6ee8 fdf74afe
    bl refresh_overlay_palette_row           @ 080d6eec 06f0bafa
    ldr r1, DAT_080d6f24                     @ 080d6ef0 0c49
    movs r0,#0x12    @ 080d6ef2 1220
    strh r0,[r1,#0x10]                       @ 080d6ef4 0882
    movs r4,#0x1    @ 080d6ef6 0124
LAB_080d6ef8:
    adds r0,r4,#0x0    @ 080d6ef8 201c
    add sp,#0xc                              @ 080d6efa 03b0
    pop {r3,r4,r5}                           @ 080d6efc 38bc
    .hword 0x4698    @ 080d6efe 9846
    .hword 0x46a1    @ 080d6f00 a146
    .hword 0x46aa    @ 080d6f02 aa46
    pop {r4,r5,r6,r7}                        @ 080d6f04 f0bc
    pop {r1}                                 @ 080d6f06 02bc
    bx r1                                    @ 080d6f08 0847
    .zero  0x2
DAT_080d6f0c:
    .word  0x05000200                     @ 080d6f0c 00020005
PTR_pack_banner_obj_palette_080d6f10:
    .word  pack_banner_obj_palette        @ 080d6f10 40045108
DAT_080d6f14:
    .word  0x000006ee                     @ 080d6f14 ee060000
DAT_080d6f18:
    .word  0x00000719                     @ 080d6f18 19070000
DAT_080d6f1c:
    .word  0x050001e0                     @ 080d6f1c e0010005
DAT_080d6f20:
    .word  0x09ccd290                     @ 080d6f20 90d2cc09
DAT_080d6f24:
    .word  pack_ui_state                  @ 080d6f24 50580003

@ 拆包场景卡片详情页混合/窗口寄存器初始化. 无参数入口, 直接写一组 IO 寄存器: BLDCNT=0x2da (全层混合 + BLDY 模式), BLDALPHA+2 (BLDY 偏移) =0x4, BLDALPHA=0x10, WIN0V/WIN1V 设置为 0x3f3f/0x3f1f (窗口区域), WIN0H/WIN1H=0xf0 (全宽), WININ 未使用, WIN1V=0x7090, DISPCNT 写 0xfe<<7=0x7f00 到 0x04000800 偏移 (pack_ui_state+0x10 偏移的 0xfe<<7 写). 调 render_pack_card_highlight_sprite(1) + render_pack_card_spin_oam_by_mode(1,0) + render_pack_card_sprite_by_flip_state(1) + render_pack_card_slot_oam(3). 写 pack_ui_state+0x10=0xd. 固定返回 1.
init_pack_card_detail_blend_regs:
    push {lr}                                @ 080d6f28 00b5
    ldr r1, PTR_BLDCNT_080d6f98              @ 080d6f2a 1b49
    ldr r2, DAT_080d6f9c                     @ 080d6f2c 1b4a
    adds r0,r2,#0x0    @ 080d6f2e 101c
    strh r0,[r1,#0x0]                        @ 080d6f30 0880
    adds r1,#0x4    @ 080d6f32 0431
    movs r0,#0x4    @ 080d6f34 0420
    strh r0,[r1,#0x0]                        @ 080d6f36 0880
    subs r1,#0x2    @ 080d6f38 0239
    movs r0,#0x10    @ 080d6f3a 1020
    strh r0,[r1,#0x0]                        @ 080d6f3c 0880
    subs r1,#0xa    @ 080d6f3e 0a39
    ldr r3, DAT_080d6fa0                     @ 080d6f40 174b
    adds r0,r3,#0x0    @ 080d6f42 181c
    strh r0,[r1,#0x0]                        @ 080d6f44 0880
    adds r1,#0x2    @ 080d6f46 0231
    ldr r2, DAT_080d6fa4                     @ 080d6f48 164a
    adds r0,r2,#0x0    @ 080d6f4a 101c
    strh r0,[r1,#0x0]                        @ 080d6f4c 0880
    ldr r0, PTR_WIN0H_080d6fa8               @ 080d6f4e 1648
    movs r2,#0xf0    @ 080d6f50 f022
    strh r2,[r0,#0x0]                        @ 080d6f52 0280
    subs r1,#0x6    @ 080d6f54 0639
    ldr r3, DAT_080d6fac                     @ 080d6f56 154b
    adds r0,r3,#0x0    @ 080d6f58 181c
    strh r0,[r1,#0x0]                        @ 080d6f5a 0880
    ldr r0, PTR_WIN1H_080d6fb0               @ 080d6f5c 1448
    strh r2,[r0,#0x0]                        @ 080d6f5e 0280
    adds r1,#0x2    @ 080d6f60 0231
    ldr r2, DAT_080d6fb4                     @ 080d6f62 144a
    adds r0,r2,#0x0    @ 080d6f64 101c
    strh r0,[r1,#0x0]                        @ 080d6f66 0880
    subs r1,#0x46    @ 080d6f68 4639
    movs r0,#0xfe    @ 080d6f6a fe20
    lsls r0,r0,#0x7    @ 080d6f6c c001
    strh r0,[r1,#0x0]                        @ 080d6f6e 0880
    movs r0,#0x1    @ 080d6f70 0120
    bl render_pack_card_highlight_sprite     @ 080d6f72 fef72bfb
    movs r0,#0x1    @ 080d6f76 0120
    movs r1,#0x0    @ 080d6f78 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d6f7a fef779fa
    movs r0,#0x1    @ 080d6f7e 0120
    bl render_pack_card_sprite_by_flip_state @ 080d6f80 fdf792fb
    movs r0,#0x3    @ 080d6f84 0320
    bl render_pack_card_slot_oam             @ 080d6f86 fef7fdf8
    ldr r1, DAT_080d6fb8                     @ 080d6f8a 0b49
    movs r0,#0xd    @ 080d6f8c 0d20
    strh r0,[r1,#0x10]                       @ 080d6f8e 0882
    movs r0,#0x1    @ 080d6f90 0120
    pop {r1}                                 @ 080d6f92 02bc
    bx r1                                    @ 080d6f94 0847
    .zero  0x2
PTR_BLDCNT_080d6f98:
    .word  BLDCNT                         @ 080d6f98 50000004
DAT_080d6f9c:
    .word  0x000002da                     @ 080d6f9c da020000
DAT_080d6fa0:
    .word  0x00003f3f                     @ 080d6fa0 3f3f0000
DAT_080d6fa4:
    .word  0x00003f1f                     @ 080d6fa4 1f3f0000
PTR_WIN0H_080d6fa8:
    .word  WIN0H                          @ 080d6fa8 40000004
DAT_080d6fac:
    .word  0x00001030                     @ 080d6fac 30100000
PTR_WIN1H_080d6fb0:
    .word  WIN1H                          @ 080d6fb0 42000004
DAT_080d6fb4:
    .word  0x00007090                     @ 080d6fb4 90700000
DAT_080d6fb8:
    .word  pack_ui_state                  @ 080d6fb8 50580003

@ 拆包场景卡片选择列表初始化帧驱动. 从 pack_ui_state+0xc+0x6 帧计数器递减; 若仍 >0 返回 0 继续等待. 当计数器归零时: 清 gPrng+0xba*2=0x174 halfword 的 bit9 (AND 0xfdff), 调 build_pack_slot_selection_list 建立卡片选择列表; 写 [+0x2]=0 (重置索引), 清 pack_ui_state+0x724 低 2 bit (AND ~0x3), 返回 1. 此为拆包选卡 UI 进入选择状态前的一次性初始化步骤.
tick_pack_slot_selection_list_setup:
    push {r4,r5,lr}                          @ 080d6fbc 30b5
    ldr r5, DAT_080d6ffc                     @ 080d6fbe 0f4d
    adds r4,r5,#0x0    @ 080d6fc0 2c1c
    adds r4,#0xc    @ 080d6fc2 0c34
    ldrh r0,[r4,#0x6]                        @ 080d6fc4 e088
    subs r0,#0x1    @ 080d6fc6 0138
    strh r0,[r4,#0x6]                        @ 080d6fc8 e080
    lsls r0,r0,#0x10    @ 080d6fca 0004
    cmp r0,#0x0                              @ 080d6fcc 0028
    bgt LAB_080d700c                         @ 080d6fce 1ddc
    ldr r1, PTR_gPrng_080d7000               @ 080d6fd0 0b49
    movs r0,#0xba    @ 080d6fd2 ba20
    lsls r0,r0,#0x1    @ 080d6fd4 4000
    adds r1,r1,r0    @ 080d6fd6 0918
    ldr r0, DAT_080d7004                     @ 080d6fd8 0a48
    ldrh r2,[r1,#0x0]                        @ 080d6fda 0a88
    ands r0,r2    @ 080d6fdc 1040
    strh r0,[r1,#0x0]                        @ 080d6fde 0880
    bl build_pack_slot_selection_list        @ 080d6fe0 04f088fa
    movs r0,#0x0    @ 080d6fe4 0020
    strh r0,[r4,#0x2]                        @ 080d6fe6 6080
    ldr r0, DAT_080d7008                     @ 080d6fe8 0748
    adds r1,r5,r0    @ 080d6fea 2918
    movs r0,#0x3    @ 080d6fec 0320
    rsbs r0,r0,#0    @ 080d6fee 4042
    ldrb r2,[r1,#0x0]                        @ 080d6ff0 0a78
    ands r0,r2    @ 080d6ff2 1040
    strb r0,[r1,#0x0]                        @ 080d6ff4 0870
    movs r0,#0x1    @ 080d6ff6 0120
    b LAB_080d700e                           @ 080d6ff8 09e0
    .zero  0x2
DAT_080d6ffc:
    .word  pack_ui_state                  @ 080d6ffc 50580003
PTR_gPrng_080d7000:
    .word  gPrng                          @ 080d7000 40000003
DAT_080d7004:
    .word  0x0000fdff                     @ 080d7004 fffd0000
DAT_080d7008:
    .word  0x00000724                     @ 080d7008 24070000
LAB_080d700c:
    movs r0,#0x0    @ 080d700c 0020
LAB_080d700e:
    pop {r4,r5}                              @ 080d700e 30bc
    pop {r1}                                 @ 080d7010 02bc
    bx r1                                    @ 080d7012 0847

@ Advances pack card info page step state. Reads current step index from pack_ui_state+0xc scroll state [+0x4]; looks up function pointer in ROM table DAT_080d7054 (0x09e493e0). If pointer is non-null calls invoke_r0; if return is non-zero increments step index. If step index is non-zero, writes a scroll param to gPrng+0x1ea. Returns 0 if step done (null fn ptr), 1 if more steps remain. Exits via pop{r1}+bx r1 (Sub-case E).
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d7050)
@ - STEP_TABLE_BASE = 0x09e493e0 (DAT_080d7054; ROM jump table)
@ - gPrng = 0x03000040 (PTR_gPrng_080d7058)
@ - PRNG_WRITE_OFFSET = 0x1ea (movs r2,#0xf5; lsls r2,r2,#1 -> 0xf5<<1=0x1ea)
@ 
@ Inputs: none (entry: ldr r0, pack_ui_state)
@ Returns: r0=u32 (0=step done, 1=more steps pending) (Sub-case E pop{r1}+bx r1)
@ Side effects: [pack_ui_state+0xc+0x4] step_index += 1 if fn returns nonzero; [gPrng+0x1ea] strh scroll param
tick_pack_card_info_step:
    push {r4,lr}                             @ 080d7014 10b5
    ldr r0, DAT_080d7050                     @ 080d7016 0e48
    adds r4,r0,#0x0    @ 080d7018 041c
    adds r4,#0xc    @ 080d701a 0c34
    ldr r1, DAT_080d7054                     @ 080d701c 0d49
    ldrh r2,[r4,#0x4]                        @ 080d701e a288
    lsls r0,r2,#0x2    @ 080d7020 9000
    adds r0,r0,r1    @ 080d7022 4018
    ldr r0,[r0,#0x0]                         @ 080d7024 0068
    cmp r0,#0x0                              @ 080d7026 0028
    beq LAB_080d705c                         @ 080d7028 18d0
    bl invoke_r0                             @ 080d702a 37f0cdfa
    cmp r0,#0x0                              @ 080d702e 0028
    beq LAB_080d7038                         @ 080d7030 02d0
    ldrh r0,[r4,#0x4]                        @ 080d7032 a088
    adds r0,#0x1    @ 080d7034 0130
    strh r0,[r4,#0x4]                        @ 080d7036 a080
LAB_080d7038:
    ldrh r0,[r4,#0x4]                        @ 080d7038 a088
    cmp r0,#0x0                              @ 080d703a 0028
    beq LAB_080d704a                         @ 080d703c 05d0
    ldr r0, PTR_gPrng_080d7058               @ 080d703e 0648
    ldrh r1,[r4,#0x3e]                       @ 080d7040 e18f
    movs r2,#0xf5    @ 080d7042 f522
    lsls r2,r2,#0x1    @ 080d7044 5200
    adds r0,r0,r2    @ 080d7046 8018
    strh r1,[r0,#0x0]                        @ 080d7048 0180
LAB_080d704a:
    movs r0,#0x0    @ 080d704a 0020
    b LAB_080d705e                           @ 080d704c 07e0
    .zero  0x2
DAT_080d7050:
    .word  pack_ui_state                  @ 080d7050 50580003
DAT_080d7054:
    .word  0x09e493e0                     @ 080d7054 e093e409
PTR_gPrng_080d7058:
    .word  gPrng                          @ 080d7058 40000003
LAB_080d705c:
    movs r0,#0x1    @ 080d705c 0120
LAB_080d705e:
    pop {r4}                                 @ 080d705e 10bc
    pop {r1}                                 @ 080d7060 02bc
    bx r1                                    @ 080d7062 0847

@ pack card info subpage init: sets BG control registers and zero-fills all VRAM regions. Writes BG0CNT=0x1c00, BG1CNT=0x1d0d, BG2CNT=0x1e8a. Calls zero_fill_halfword_wrapper to clear 6 VRAM regions: 0x06000000 (0x4000 HW), 0x0600e000 (0x800 HW), 0x0600d000 (0x1000 HW), 0x0600e800 (0x800 HW), 0x06008000 (0x1000 HW), 0x0600f000 (0x800 HW). Calls reset_all_bg_scroll_regs_and_shadows. Called by pack_banner_080d733c on entering card info subpage; zero-parameter pure side-effect function.
@ 
@ Constants:
@ - BG0CNT = 0x04000008
@ - BG0CNT_VAL = 0x1c00 (charblock 7, 256x256, 4bpp)
@ - BG1CNT_VAL = 0x1d0d, BG2CNT_VAL = 0x1e8a
@ - VRAM_TILEMAP = 0x06000000, VRAM_BG2 = 0x0600e000
@ - VRAM_BG_CHAR_A = 0x0600d000, VRAM_BG3 = 0x0600e800
@ - VRAM_BG_CHAR_B = 0x06008000, VRAM_BG_CHAR_C = 0x0600f000
init_pack_card_info_bg_and_vram:
    push {r4,r5,lr}                          @ 080d7064 30b5
    ldr r1, PTR_BG0CNT_080d70c0              @ 080d7066 1649
    movs r0,#0xe0    @ 080d7068 e020
    lsls r0,r0,#0x5    @ 080d706a 4001
    strh r0,[r1,#0x0]                        @ 080d706c 0880
    adds r1,#0x2    @ 080d706e 0231
    ldr r0, DAT_080d70c4                     @ 080d7070 1448
    strh r0,[r1,#0x0]                        @ 080d7072 0880
    adds r1,#0x2    @ 080d7074 0231
    ldr r0, DAT_080d70c8                     @ 080d7076 1448
    strh r0,[r1,#0x0]                        @ 080d7078 0880
    movs r0,#0xc0    @ 080d707a c020
    lsls r0,r0,#0x13    @ 080d707c c004
    movs r1,#0x80    @ 080d707e 8021
    lsls r1,r1,#0x7    @ 080d7080 c901
    bl zero_fill_halfword_wrapper            @ 080d7082 1df009ff
    ldr r0, PTR_DAT_080d70cc                 @ 080d7086 1148
    movs r4,#0x80    @ 080d7088 8024
    lsls r4,r4,#0x4    @ 080d708a 2401
    adds r1,r4,#0x0    @ 080d708c 211c
    bl zero_fill_halfword_wrapper            @ 080d708e 1df003ff
    ldr r0, PTR_DAT_080d70d0                 @ 080d7092 0f48
    movs r5,#0x80    @ 080d7094 8025
    lsls r5,r5,#0x5    @ 080d7096 6d01
    adds r1,r5,#0x0    @ 080d7098 291c
    bl zero_fill_halfword_wrapper            @ 080d709a 1df0fdfe
    ldr r0, PTR_DAT_080d70d4                 @ 080d709e 0d48
    adds r1,r4,#0x0    @ 080d70a0 211c
    bl zero_fill_halfword_wrapper            @ 080d70a2 1df0f9fe
    ldr r0, PTR_DAT_080d70d8                 @ 080d70a6 0c48
    adds r1,r5,#0x0    @ 080d70a8 291c
    bl zero_fill_halfword_wrapper            @ 080d70aa 1df0f5fe
    ldr r0, PTR_DAT_080d70dc                 @ 080d70ae 0b48
    adds r1,r4,#0x0    @ 080d70b0 211c
    bl zero_fill_halfword_wrapper            @ 080d70b2 1df0f1fe
    bl reset_all_bg_scroll_regs_and_shadows  @ 080d70b6 1ef0e7fc
    pop {r4,r5}                              @ 080d70ba 30bc
    pop {r0}                                 @ 080d70bc 01bc
    bx r0                                    @ 080d70be 0047
PTR_BG0CNT_080d70c0:
    .word  BG0CNT                         @ 080d70c0 08000004
DAT_080d70c4:
    .word  0x00001d0d                     @ 080d70c4 0d1d0000
DAT_080d70c8:
    .word  0x00001e8a                     @ 080d70c8 8a1e0000
PTR_DAT_080d70cc:
    .word  0x0600e000                     @ 080d70cc 00e00006
PTR_DAT_080d70d0:
    .word  0x0600d000                     @ 080d70d0 00d00006
PTR_DAT_080d70d4:
    .word  0x0600e800                     @ 080d70d4 00e80006
PTR_DAT_080d70d8:
    .word  0x06008000                     @ 080d70d8 00800006
PTR_DAT_080d70dc:
    .word  0x0600f000                     @ 080d70dc 00f00006

@ Maps pack card slot index r0 to screen Y pixel coordinate. r0==0 or r0==2/3: returns 0x28 (40 px, top row); r0==1: returns 0x78 (120 px, bottom row). No push/pop, pure combinational leaf function. Called by pack card info page when computing OAM sprite Y coordinate.
@ 
@ Constants:
@ - Y_TOP_ROW = 0x28 (40 px, top card slot row)
@ - Y_BOTTOM_ROW = 0x78 (120 px, bottom card slot row)
get_pack_slot_screen_y:
    cmp r0,#0x0                              @ 080d70e0 0028
    beq LAB_080d70e8                         @ 080d70e2 01d0
    cmp r0,#0x1                              @ 080d70e4 0128
    beq LAB_080d70ec                         @ 080d70e6 01d0
LAB_080d70e8:
    movs r0,#0x28    @ 080d70e8 2820
    b LAB_080d70ee                           @ 080d70ea 00e0
LAB_080d70ec:
    movs r0,#0x78    @ 080d70ec 7820
LAB_080d70ee:
    bx lr                                    @ 080d70ee 7047

@ Loads pack card info subpage BG tile graphics and palette, using the second data set from the shared ROM GFX tables (offset +0x8 vs main page +0xc). First zero_fill_halfword_wrapper clears 0x0600d000 (0x1000 HW); reads huffman-compressed tile ptr from ROM 0x09cce2b0+8, decompresses to 0x0600d000; reads from 0x09cce2d0+8, decompresses to 0x0600e800; DMA-copies 0x09cce2c0+8 palette (32 bytes) to 0x050001a0. Called immediately after init_pack_card_info_bg_and_vram on entering card info subpage.
@ 
@ Constants:
@ - ROM_GFX_TABLE_A = 0x09cce2b0 (pack GFX data table A, +0x8 = info page tile ptr)
@ - ROM_GFX_TABLE_B = 0x09cce2d0 (pack GFX data table B)
@ - ROM_PAL_TABLE = 0x09cce2c0 (pack palette table)
@ - VRAM_CLEAR = 0x0600d000 (cleared then written)
@ - VRAM_TILE_A = 0x0600d000, VRAM_TILE_B = 0x0600e800 (huffman decomp targets)
@ - BG_PAL_DST = 0x050001a0
@ - PAL_SIZE = 0x20 (32 bytes)
@ - TABLE_OFFSET = 0x8 (info page data offset in ROM table, vs main page +0xc)
load_pack_card_info_tiles_and_palette:
    push {r4,lr}                             @ 080d70f0 10b5
    ldr r4, DAT_080d7124                     @ 080d70f2 0c4c
    movs r1,#0x80    @ 080d70f4 8021
    lsls r1,r1,#0x5    @ 080d70f6 4901
    adds r0,r4,#0x0    @ 080d70f8 201c
    bl zero_fill_halfword_wrapper            @ 080d70fa 1df0cdfe
    ldr r0, DAT_080d7128                     @ 080d70fe 0a48
    ldr r0,[r0,#0x8]                         @ 080d7100 8068
    adds r1,r4,#0x0    @ 080d7102 211c
    bl bios_huff_uncomp                      @ 080d7104 37f088f9
    ldr r0, DAT_080d712c                     @ 080d7108 0848
    ldr r0,[r0,#0x8]                         @ 080d710a 8068
    ldr r1, DAT_080d7130                     @ 080d710c 0849
    bl bios_huff_uncomp                      @ 080d710e 37f083f9
    ldr r0, DAT_080d7134                     @ 080d7112 0848
    ldr r1, DAT_080d7138                     @ 080d7114 0849
    ldr r1,[r1,#0x8]                         @ 080d7116 8968
    movs r2,#0x20    @ 080d7118 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d711a 1df0f5fe
    pop {r4}                                 @ 080d711e 10bc
    pop {r0}                                 @ 080d7120 01bc
    bx r0                                    @ 080d7122 0047
DAT_080d7124:
    .word  0x0600d000                     @ 080d7124 00d00006
DAT_080d7128:
    .word  0x09cce2b0                     @ 080d7128 b0e2cc09
DAT_080d712c:
    .word  0x09cce2d0                     @ 080d712c d0e2cc09
DAT_080d7130:
    .word  0x0600e800                     @ 080d7130 00e80006
DAT_080d7134:
    .word  0x050001a0                     @ 080d7134 a0010005
DAT_080d7138:
    .word  0x09cce2c0                     @ 080d7138 c0e2cc09

@ Called during pack card info page initialization by two callers (0x080d733c contains init_pack_card_info_bg_and_vram; 0x080d7f3c contains tick_overlay_animation_step/init_pack_scroll_animation). Calls render_pack_label_str13f1_to_bg_vram(0x140) to render the first label string to BG VRAM; calls render_pack_label_str1390_to_bg_vram(0x180) to render the second label string; finally calls copy_pack_card_palette_to_obj_pal(0xb) to copy the card palette to OBJ palette slot 11.
@ 
@ Constants:
@ - LABEL_VRAM_OFFSET_0 = 0xa0<<1 = 0x140 (first label render offset)
@ - LABEL_VRAM_OFFSET_1 = 0x140+0x40 = 0x180 (second label render offset)
@ - OBJ_PAL_SLOT = 0xb (palette slot for copy_pack_card_palette_to_obj_pal)
render_pack_info_label_sprites_and_palette:
    push {r4,lr}                             @ 080d713c 10b5
    movs r4,#0xa0    @ 080d713e a024
    lsls r4,r4,#0x1    @ 080d7140 6400
    adds r0,r4,#0x0    @ 080d7142 201c
    bl render_pack_label_str13f1_to_bg_vram  @ 080d7144 05f0c4fb
    adds r4,#0x40    @ 080d7148 4034
    adds r0,r4,#0x0    @ 080d714a 201c
    bl render_pack_label_str1390_to_bg_vram  @ 080d714c 05f0ecfb
    movs r0,#0xb    @ 080d7150 0b20
    bl copy_pack_card_palette_to_obj_pal     @ 080d7152 05f04bfa
    pop {r4}                                 @ 080d7156 10bc
    pop {r0}                                 @ 080d7158 01bc
    bx r0                                    @ 080d715a 0047

@ Renders pack card stat byte sprite to the info page OBJ VRAM slot selected by player_id. r0=player_id (0 or 1). If r0==0 uses base 0x06000000 (movs r4,#0xc0; lsls r4,#0x13); else loads DAT_080d7180=0x06000680. Computes dest = base+0x240. Calls zero_fill_pack_info_obj_vram(dest) then render_pack_card_stat_byte_to_sprite(dest). Called by pack info page frame drivers.
@ 
@ Constants:
@ - VRAM_BASE_PLAYER0 = 0x06000000 (movs r4,#0xc0; lsls r4,r4,#0x13)
@ - VRAM_BASE_PLAYER1 = 0x06000680 (DAT_080d7180)
@ - VRAM_OFFSET = 0x240 (movs r0,#0x90; lsls r0,r0,#2 -> 0x90<<2=0x240)
@ 
@ Inputs: r0=u32 player_id (0 or 1; selects VRAM base)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM base+0x240 via zero_fill_pack_info_obj_vram] clears stat sprite area; [OBJ VRAM base+0x240 via render_pack_card_stat_byte_to_sprite] writes stat sprite tiles
render_pack_stat_byte_to_info_slot:
    push {r4,lr}                             @ 080d715c 10b5
    movs r4,#0xc0    @ 080d715e c024
    lsls r4,r4,#0x13    @ 080d7160 e404
    cmp r0,#0x0                              @ 080d7162 0028
    beq LAB_080d7168                         @ 080d7164 00d0
    ldr r4, DAT_080d7180                     @ 080d7166 064c
LAB_080d7168:
    movs r0,#0x90    @ 080d7168 9020
    lsls r0,r0,#0x2    @ 080d716a 8000
    adds r4,r4,r0    @ 080d716c 2418
    adds r0,r4,#0x0    @ 080d716e 201c
    bl zero_fill_pack_info_obj_vram          @ 080d7170 05f03af8
    adds r0,r4,#0x0    @ 080d7174 201c
    bl render_pack_card_stat_byte_to_sprite  @ 080d7176 05f03ff8
    pop {r4}                                 @ 080d717a 10bc
    pop {r0}                                 @ 080d717c 01bc
    bx r0                                    @ 080d717e 0047
DAT_080d7180:
    .word  0x06000680                     @ 080d7180 80060006

@ Fills tile IDs for a card image region in pack card info subpage BG tilemap (0x0600f000). Uses r0 (col) and r1 (row_group) to compute offset: (r1*32+r0)*2 bytes. Tile IDs start at 1 and increment consecutively, writing a 4-column x 8-row rectangle (row stride 0x40 bytes to next tilemap row). Used to fill the card image tile area when displaying a card in the info page.
@ 
@ Constants:
@ - TILEMAP_BASE = 0x0600f000 (card-info subpage BG tilemap)
@ - COLS = 4 (columns per block [0..3])
@ - ROWS = 8 (rows per block [0..7])
@ - INITIAL_TILE_ID = 1 (set by movs r3,#0x1 at entry)
@ - TILEMAP_ROW_STRIDE = 0x40 (row stride = 32 tiles * 2 bytes)
fill_pack_info_card_tiles:
    push {r4,lr}                             @ 080d7184 10b5
    movs r3,#0x1    @ 080d7186 0123
    lsls r1,r1,#0x5    @ 080d7188 4901
    adds r1,r1,r0    @ 080d718a 0918
    lsls r1,r1,#0x1    @ 080d718c 4900
    ldr r0, DAT_080d71b8                     @ 080d718e 0a48
    adds r1,r1,r0    @ 080d7190 0918
    movs r0,#0x0    @ 080d7192 0020
LAB_080d7194:
    movs r2,#0x0    @ 080d7194 0022
    adds r4,r0,#0x1    @ 080d7196 441c
LAB_080d7198:
    strh r3,[r1,#0x0]                        @ 080d7198 0b80
    adds r1,#0x2    @ 080d719a 0231
    adds r0,r3,#0x1    @ 080d719c 581c
    lsls r0,r0,#0x10    @ 080d719e 0004
    lsrs r3,r0,#0x10    @ 080d71a0 030c
    adds r2,#0x1    @ 080d71a2 0132
    cmp r2,#0x3                              @ 080d71a4 032a
    bls LAB_080d7198                         @ 080d71a6 f7d9
    adds r1,#0x38    @ 080d71a8 3831
    adds r0,r4,#0x0    @ 080d71aa 201c
    cmp r0,#0x7                              @ 080d71ac 0728
    bls LAB_080d7194                         @ 080d71ae f1d9
    pop {r4}                                 @ 080d71b0 10bc
    pop {r0}                                 @ 080d71b2 01bc
    bx r0                                    @ 080d71b4 0047
    .zero  0x2
DAT_080d71b8:
    .word  0x0600f000                     @ 080d71b8 00f00006

@ Fills the pack info page card name OBJ VRAM tile ID region. r0=slot_idx [0..1], r1=player_id [0..1]. Selects tile_start: player_id==0->0x12, player_id!=0->0x46. If slot_idx==1 calls fill_pack_obj_tile_row_17col_leaf(dest, 0xf); else calls fill_pack_obj_tile_region_17col(dest, tile_start, 0xf). dest = 0x0600e000+0x404. Called by pack info page frame drivers.
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x0600e000 (DAT_080d71d8)
@ - TILE_REGION_OFFSET = 0x404 (DAT_080d71dc)
@ - TILE_COUNT = 0xf (movs r2,#0xf)
@ - TILE_START_P0 = 0x12 (player_id==0)
@ - TILE_START_P1 = 0x46 (player_id!=0)
@ 
@ Inputs: r0=u32 slot_idx [0..1]; r1=u32 player_id [0..1]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM 0x0600e000+0x404 via fill_pack_obj_tile_row_17col_leaf or fill_pack_obj_tile_region_17col] writes card name tile ID sequence
fill_pack_info_card_name_tiles:
    push {lr}                                @ 080d71bc 00b5
    ldr r3, DAT_080d71d8                     @ 080d71be 064b
    movs r2,#0x46    @ 080d71c0 4622
    cmp r1,#0x0                              @ 080d71c2 0029
    bne LAB_080d71c8                         @ 080d71c4 00d1
    movs r2,#0x12    @ 080d71c6 1222
LAB_080d71c8:
    cmp r0,#0x1                              @ 080d71c8 0128
    bne LAB_080d71e0                         @ 080d71ca 09d1
    ldr r0, DAT_080d71dc                     @ 080d71cc 0348
    adds r0,r3,r0    @ 080d71ce 1818
    movs r1,#0xf    @ 080d71d0 0f21
    bl fill_pack_obj_tile_row_17col_leaf     @ 080d71d2 05f0c3f8
    b LAB_080d71ec                           @ 080d71d6 09e0
DAT_080d71d8:
    .word  0x0600e000                     @ 080d71d8 00e00006
DAT_080d71dc:
    .word  0x00000404                     @ 080d71dc 04040000
LAB_080d71e0:
    ldr r0, DAT_080d71f0                     @ 080d71e0 0348
    adds r0,r3,r0    @ 080d71e2 1818
    adds r1,r2,#0x0    @ 080d71e4 111c
    movs r2,#0xf    @ 080d71e6 0f22
    bl fill_pack_obj_tile_region_17col       @ 080d71e8 05f0a0f8
LAB_080d71ec:
    pop {r0}                                 @ 080d71ec 01bc
    bx r0                                    @ 080d71ee 0047
DAT_080d71f0:
    .word  0x00000404                     @ 080d71f0 04040000

@ Writes pack card sprite OAM attributes, dispatching to different write paths based on r2 (affine_param). Extracts coordinates from packed_xy (r0 high16=y_raw, low16=x_raw) and adjusts (x-=0x10, y-=0x20) to align to card sprite reference point. Entry `adds r3,r2,#0` transfers r2 to r3 for comparison. If r2==0x100 (OAM_AFFINE_BIT standard mode): calls write_oam_entry_with_tile_inc(packed_xy_adj, r1, OAM_BASE). Otherwise (rotation-scaling mode, r2 contains rotation param): shifts r3 left 0x10 and calls write_pack_obj_attr_by_dir_stacked.
@ 
@ Constants:
@ - X_ADJUST = 0x10 (x coordinate reference offset subtracted, 16 px)
@ - Y_ADJUST = 0x20 (y coordinate reference offset subtracted, 32 px)
@ - OAM_AFFINE_BIT = 0x100 (OAM_ROT_SCALE_FLAG; r2==0x100 -> standard non-affine path)
@ - OAM_BASE = 0x000080c0 (pack OAM shadow base)
write_pack_card_obj_attr_by_affine_toggle:
    push {r4,lr}                             @ 080d71f4 10b5
    adds r4,r1,#0x0    @ 080d71f6 0c1c
    adds r3,r2,#0x0    @ 080d71f8 131c
    adds r1,r0,#0x0    @ 080d71fa 011c
    subs r1,#0x10    @ 080d71fc 1039
    lsls r1,r1,#0x10    @ 080d71fe 0904
    lsrs r1,r1,#0x10    @ 080d7200 090c
    lsrs r0,r0,#0x10    @ 080d7202 000c
    subs r0,#0x20    @ 080d7204 2038
    lsls r0,r0,#0x10    @ 080d7206 0004
    lsrs r2,r0,#0x10    @ 080d7208 020c
    movs r0,#0x80    @ 080d720a 8020
    lsls r0,r0,#0x1    @ 080d720c 4000
    cmp r3,r0                                @ 080d720e 8342
    bne LAB_080d7228                         @ 080d7210 0ad1
    lsls r0,r2,#0x10    @ 080d7212 1004
    orrs r0,r1    @ 080d7214 0843
    ldr r1, DAT_080d7224                     @ 080d7216 0349
    lsls r2,r4,#0x1a    @ 080d7218 a206
    lsrs r2,r2,#0x10    @ 080d721a 120c
    bl write_oam_entry_with_tile_inc         @ 080d721c 1ff018f9
    b LAB_080d7238                           @ 080d7220 0ae0
    .zero  0x2
DAT_080d7224:
    .word  0x000080c0                     @ 080d7224 c0800000
LAB_080d7228:
    lsls r0,r2,#0x10    @ 080d7228 1004
    orrs r0,r1    @ 080d722a 0843
    ldr r1, DAT_080d7240                     @ 080d722c 0449
    lsls r2,r4,#0x1a    @ 080d722e a206
    lsrs r2,r2,#0x10    @ 080d7230 120c
    lsls r3,r3,#0x10    @ 080d7232 1b04
    bl write_pack_obj_attr_by_dir_stacked    @ 080d7234 1ff04afd
LAB_080d7238:
    pop {r4}                                 @ 080d7238 10bc
    pop {r0}                                 @ 080d723a 01bc
    bx r0                                    @ 080d723c 0047
    .zero  0x2
DAT_080d7240:
    .word  0x000080c0                     @ 080d7240 c0800000

@ Renders card highlight box sprite (two OAM entries) on the pack info page. r0=card_slot [0..3]. Loads fixed OAM params r5=0x0002000d, first sprite attr0=0x00900044, second attr0=0x0090fff4. Sets color attr r4=0x000b0000 (movs r4,#0xb0; lsls r4,r4,#0xc -> 0xb0<<12=0xb0000; python: 0xb0<<0xc==0xb0000). Computes y_base=0x140 (0xa0<<1). Calls render_overlay_oam_sprite_tiled twice (second with y+0x40). Called by pack info page frame drivers.
@ 
@ Constants:
@ - OAM_PARAMS = 0x0002000d (DAT_080d7280)
@ - SPRITE_ATTR0_A = 0x00900044 (DAT_080d727c)
@ - SPRITE_ATTR0_B = 0x0090fff4 (DAT_080d7284)
@ - COLOR_ATTR = 0x000b0000 (movs r4,#0xb0; lsls r4,r4,#0xc -> 0xb0<<12 = 0xb0000; python: 0xb0<<0xc == 0xb0000)
@ 
@ Inputs: r0=u32 card_slot [0..3]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OAM shadow via render_overlay_oam_sprite_tiled x2] writes info page highlight box OAM entries
render_pack_info_card_highlight_sprite:
    push {r4,r5,r6,r7,lr}                    @ 080d7244 f0b5
    adds r6,r0,#0x0    @ 080d7246 061c
    movs r7,#0xa0    @ 080d7248 a027
    lsls r7,r7,#0x1    @ 080d724a 7f00
    cmp r6,#0x3                              @ 080d724c 032e
    bls LAB_080d7252                         @ 080d724e 00d9
    movs r6,#0x3    @ 080d7250 0326
LAB_080d7252:
    ldr r0, DAT_080d727c                     @ 080d7252 0a48
    ldr r5, DAT_080d7280                     @ 080d7254 0a4d
    movs r4,#0xb0    @ 080d7256 b024
    lsls r4,r4,#0xc    @ 080d7258 2403
    adds r2,r7,#0x0    @ 080d725a 3a1c
    orrs r2,r4    @ 080d725c 2243
    adds r1,r5,#0x0    @ 080d725e 291c
    adds r3,r6,#0x0    @ 080d7260 331c
    bl render_overlay_oam_sprite_tiled       @ 080d7262 06f085fa
    adds r7,#0x40    @ 080d7266 4037
    ldr r0, DAT_080d7284                     @ 080d7268 0648
    orrs r7,r4    @ 080d726a 2743
    adds r1,r5,#0x0    @ 080d726c 291c
    adds r2,r7,#0x0    @ 080d726e 3a1c
    adds r3,r6,#0x0    @ 080d7270 331c
    bl render_overlay_oam_sprite_tiled       @ 080d7272 06f07dfa
    pop {r4,r5,r6,r7}                        @ 080d7276 f0bc
    pop {r0}                                 @ 080d7278 01bc
    bx r0                                    @ 080d727a 0047
DAT_080d727c:
    .word  0x00900044                     @ 080d727c 44009000
DAT_080d7280:
    .word  0x0002000d                     @ 080d7280 0d000200
DAT_080d7284:
    .word  0x0090fff4                     @ 080d7284 f4ff9000

@ Renders pack card info page card presence indicator sprites based on a presence bitfield. r0=card_slot [0..3]. Loads presence bitfield r6 from pack_ui_state+0xc at dynamic address r1+slot_row*32+0x58 where slot_row = ldrh r3,[r1,#0x32]. Tile attr r7 = 0xc00c|(card_slot<<10). Loops r5=0..9: if bit0 of r6 set, computes (r5%5, r5/5) -> OAM coords, calls write_oam_entry_from_packed_args; shifts r6 right. Called by pack info page frame drivers.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d72f0)
@ - STRUCT_LDRH_OFFSET = 0x32 (ldrh r3,[r1,#0x32] -> r3 = slot_row halfword at r1+0x32)
@ - PRESENCE_FIELD_OFFSET = 0x58 (ldr r6,[r0,#0x58] -> r0 = r1+r3*32; presence bitfield at r1+slot_row*32+0x58, runtime dynamic address)
@ - OAM_ATTR_BASE = 0xc00c (DAT_080d72f4)
@ - LOOP_COUNT = 10 (cmp r5,#9; bls -> 0..9)
@ - TILE_COL_MOD = 5 (get_bios_div_remainder(r5,5) -> col)
@ - Y_START = 0x10 (adds r0,#0x10)
@ - X_STRIDE = 0x18 (lsls r4,r0,#3)
@ 
@ Inputs: r0=u32 card_slot [0..3]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OAM shadow via write_oam_entry_from_packed_args] writes up to 10 presence indicator sprite OAM entries
render_pack_info_card_presence_sprites:
    push {r4,r5,r6,r7,lr}                    @ 080d7288 f0b5
    adds r2,r0,#0x0    @ 080d728a 021c
    ldr r1, DAT_080d72f0                     @ 080d728c 1849
    adds r1,#0xc    @ 080d728e 0c31
    ldrh r3,[r1,#0x32]                       @ 080d7290 4b8e
    lsls r0,r3,#0x5    @ 080d7292 5801
    adds r0,r0,r1    @ 080d7294 4018
    ldr r6,[r0,#0x58]                        @ 080d7296 866d
    cmp r2,#0x3                              @ 080d7298 032a
    bls LAB_080d729e                         @ 080d729a 00d9
    movs r2,#0x3    @ 080d729c 0322
LAB_080d729e:
    movs r5,#0x0    @ 080d729e 0025
    lsls r0,r2,#0xa    @ 080d72a0 9002
    ldr r2, DAT_080d72f4                     @ 080d72a2 144a
    adds r1,r2,#0x0    @ 080d72a4 111c
    orrs r0,r1    @ 080d72a6 0843
    lsls r7,r0,#0x10    @ 080d72a8 0704
LAB_080d72aa:
    movs r0,#0x1    @ 080d72aa 0120
    ands r0,r6    @ 080d72ac 3040
    cmp r0,#0x0                              @ 080d72ae 0028
    beq LAB_080d72e0                         @ 080d72b0 16d0
    adds r0,r5,#0x0    @ 080d72b2 281c
    movs r1,#0x5    @ 080d72b4 0521
    bl get_bios_div_remainder                @ 080d72b6 37f0a3f8
    lsls r4,r0,#0x2    @ 080d72ba 8400
    adds r4,r4,r0    @ 080d72bc 2418
    lsls r4,r4,#0x3    @ 080d72be e400
    adds r4,#0x18    @ 080d72c0 1834
    adds r0,r5,#0x0    @ 080d72c2 281c
    movs r1,#0x5    @ 080d72c4 0521
    bl bios_div                              @ 080d72c6 37f099f8
    lsls r0,r0,#0x6    @ 080d72ca 8001
    adds r0,#0x10    @ 080d72cc 1030
    lsls r4,r4,#0x10    @ 080d72ce 2404
    lsrs r4,r4,#0x10    @ 080d72d0 240c
    lsls r0,r0,#0x10    @ 080d72d2 0004
    orrs r4,r0    @ 080d72d4 0443
    adds r0,r4,#0x0    @ 080d72d6 201c
    movs r1,#0x80    @ 080d72d8 8021
    lsrs r2,r7,#0x10    @ 080d72da 3a0c
    bl write_oam_entry_from_packed_args      @ 080d72dc 1ef046ff
LAB_080d72e0:
    lsrs r6,r6,#0x1    @ 080d72e0 7608
    adds r5,#0x1    @ 080d72e2 0135
    cmp r5,#0x9                              @ 080d72e4 092d
    bls LAB_080d72aa                         @ 080d72e6 e0d9
    pop {r4,r5,r6,r7}                        @ 080d72e8 f0bc
    pop {r0}                                 @ 080d72ea 01bc
    bx r0                                    @ 080d72ec 0047
    .zero  0x2
DAT_080d72f0:
    .word  pack_ui_state                  @ 080d72f0 50580003
DAT_080d72f4:
    .word  0x0000c00c                     @ 080d72f4 0cc00000

@ Called by the state machine when the pack card info page enters its display phase, to initialize the card info overlay struct and cache the current selected card data pointer. Clears pack_ui_state[+0x18] and [+0x1a] (scroll positions), then calls init_overlay_struct_and_palette with EWRAM address 0x0200af20 (mode=6, color_count=15) to initialize the overlay palette and struct. Finally reads the card data pointer from the currently selected card slot at offset +0x14 and writes it to pack_ui_state[+0x34] for use by subsequent frame render functions.
@ 
@ Constants:
@ - SCROLL_POS_0 = +0x18 (strh 0,[r5,#0x18])
@ - SCROLL_POS_1 = +0x1a (strh 0,[r5,#0x1a])
@ - OVERLAY_EWRAM = 0x0200af20 (DAT_080d7338)
@ - OVERLAY_BUF_SIZE = 0x80<<2 = 0x200 (overlay color buffer size)
@ - OVERLAY_MODE = 6
@ - OVERLAY_COLOR_COUNT = 0xf
@ - STRUCT_STRIDE = 0x20 (per slot, lsls r1,#5)
@ - CARD_PTR_OFFSET = 0x14 (ldr r0,[r4,#0x14])
@ - CARD_PTR_CACHE = +0x34 (str r0,[r5,#0x34])
@ - SLOT_ARRAY_OFFSET = 0xda<<3 = 0x6d0 (r0 += 0x6d0 for overlay target)
@ - SLOT_INDEX_FIELD = +0x32 (ldrh r1,[r5,#0x32] current slot index)
init_pack_card_info_overlay_and_card_ptr:
    push {r4,r5,lr}                          @ 080d72f8 30b5
    sub sp,#0x4                              @ 080d72fa 81b0
    ldr r0, DAT_080d7334                     @ 080d72fc 0d48
    adds r5,r0,#0x0    @ 080d72fe 051c
    adds r5,#0xc    @ 080d7300 0c35
    ldrh r1,[r5,#0x32]                       @ 080d7302 698e
    lsls r4,r1,#0x5    @ 080d7304 4c01
    adds r4,#0x44    @ 080d7306 4434
    adds r4,r4,r5    @ 080d7308 6419
    movs r1,#0x0    @ 080d730a 0021
    strh r1,[r5,#0x18]                       @ 080d730c 2983
    strh r1,[r5,#0x1a]                       @ 080d730e 6983
    movs r1,#0xda    @ 080d7310 da21
    lsls r1,r1,#0x3    @ 080d7312 c900
    adds r0,r0,r1    @ 080d7314 4018
    ldr r1, DAT_080d7338                     @ 080d7316 0849
    movs r2,#0x80    @ 080d7318 8022
    lsls r2,r2,#0x2    @ 080d731a 9200
    movs r3,#0x6    @ 080d731c 0623
    str r3,[sp,#0x0]                         @ 080d731e 0093
    movs r3,#0xf    @ 080d7320 0f23
    bl init_overlay_struct_and_palette       @ 080d7322 06f041f8
    ldr r0,[r4,#0x14]                        @ 080d7326 6069
    str r0,[r5,#0x34]                        @ 080d7328 6863
    movs r0,#0x1    @ 080d732a 0120
    add sp,#0x4                              @ 080d732c 01b0
    pop {r4,r5}                              @ 080d732e 30bc
    pop {r1}                                 @ 080d7330 02bc
    bx r1                                    @ 080d7332 0847
DAT_080d7334:
    .word  pack_ui_state                  @ 080d7334 50580003
DAT_080d7338:
    .word  0x0200af20                     @ 080d7338 20af0002

@ 进入拆包卡片详情画面时一次性建立 BG/OBJ 图层与 VRAM 资源. 读 pack_ui_state+0xc[+0x32] 卡槽索引算出工作结构地址, 依次调 init_pack_card_info_bg_and_vram 与 load_pack_card_info_tiles_and_palette 建立背景与调色板, 再以 load_pack_card_tiles_to_vram 加载卡面图块. 随后用 zero_fill_halfword_wrapper 清零 OBJ VRAM 0x600e000 与字符基区, 经 copy_memory_dma3_with_cpu_fallback 拷贝调色板 (0x50000200/0x500001e0), 用 pack_banner_tile_copy 铺设横幅图块行 (两次, 主屏+副屏), 然后循环 10 次 (icid 0..9) 调 fill_pack_info_card_tiles 填充详情卡图块. 最后若 [+0x1c] bit1 置位则写 pack_ui_state[0x10] 状态 := 2. 供拆包详情画面初始化状态机调用.
init_pack_card_info_detail_screen:
    push {r4,r5,r6,r7,lr}                    @ 080d733c f0b5
    .hword 0x4647    @ 080d733e 4746
    push {r7}                                @ 080d7340 80b4
    sub sp,#0xc                              @ 080d7342 83b0
    ldr r0, DAT_080d7434                     @ 080d7344 3b48
    adds r0,#0xc    @ 080d7346 0c30
    .hword 0x4680    @ 080d7348 8046
    ldrh r1,[r0,#0x32]                       @ 080d734a 418e
    lsls r0,r1,#0x5    @ 080d734c 4801
    adds r0,#0x44    @ 080d734e 4430
    .hword 0x4642    @ 080d7350 4246
    adds r7,r0,r2    @ 080d7352 8718
    bl init_pack_card_info_bg_and_vram       @ 080d7354 fff786fe
    bl load_pack_card_info_tiles_and_palette @ 080d7358 fff7cafe
    movs r0,#0x8    @ 080d735c 0820
    str r0,[sp,#0x0]                         @ 080d735e 0090
    adds r0,#0xf8    @ 080d7360 f830
    str r0,[sp,#0x4]                         @ 080d7362 0190
    movs r0,#0x1    @ 080d7364 0120
    rsbs r0,r0,#0    @ 080d7366 4042
    str r0,[sp,#0x8]                         @ 080d7368 0290
    .hword 0x4668    @ 080d736a 6846
    movs r1,#0xd    @ 080d736c 0d21
    bl load_pack_card_tiles_to_vram          @ 080d736e fdf745f9
    movs r0,#0xc    @ 080d7372 0c20
    movs r1,#0xc    @ 080d7374 0c21
    bl load_pack_card_tile_row_to_obj_vram_c @ 080d7376 05f03ff8
    bl render_pack_info_label_sprites_and_palette @ 080d737a fff7dffe
    movs r0,#0xc0    @ 080d737e c020
    lsls r0,r0,#0x13    @ 080d7380 c004
    movs r1,#0x80    @ 080d7382 8021
    lsls r1,r1,#0x7    @ 080d7384 c901
    bl zero_fill_halfword_wrapper            @ 080d7386 1df087fd
    ldr r0, DAT_080d7438                     @ 080d738a 2b48
    movs r6,#0x80    @ 080d738c 8026
    lsls r6,r6,#0x4    @ 080d738e 3601
    adds r1,r6,#0x0    @ 080d7390 311c
    bl zero_fill_halfword_wrapper            @ 080d7392 1df081fd
    ldr r0, DAT_080d743c                     @ 080d7396 2948
    ldr r1, DAT_080d7440                     @ 080d7398 2949
    movs r2,#0x20    @ 080d739a 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d739c 1df0b4fd
    ldrh r0,[r7,#0x0]                        @ 080d73a0 3888
    ldr r1, DAT_080d7444                     @ 080d73a2 2849
    movs r2,#0x0    @ 080d73a4 0022
    movs r3,#0x1    @ 080d73a6 0123
    bl pack_banner_tile_copy                 @ 080d73a8 04f05afa
    ldr r0, DAT_080d7448                     @ 080d73ac 2648
    ldr r4, PTR_pack_banner_obj_palette_080d744c @ 080d73ae 274c
    movs r5,#0x90    @ 080d73b0 9025
    lsls r5,r5,#0x1    @ 080d73b2 6d00
    adds r1,r4,#0x0    @ 080d73b4 211c
    adds r2,r5,#0x0    @ 080d73b6 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d73b8 1df0a6fd
    ldrh r0,[r7,#0x0]                        @ 080d73bc 3888
    ldr r1, DAT_080d7450                     @ 080d73be 2449
    movs r2,#0x0    @ 080d73c0 0022
    movs r3,#0x0    @ 080d73c2 0023
    bl pack_banner_tile_copy                 @ 080d73c4 04f04cfa
    movs r0,#0xa0    @ 080d73c8 a020
    lsls r0,r0,#0x13    @ 080d73ca c004
    adds r1,r4,#0x0    @ 080d73cc 211c
    adds r2,r5,#0x0    @ 080d73ce 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d73d0 1df09afd
    ldr r0, DAT_080d7454                     @ 080d73d4 1f48
    adds r1,r6,#0x0    @ 080d73d6 311c
    bl zero_fill_halfword_wrapper            @ 080d73d8 1df05efd
    movs r5,#0x0    @ 080d73dc 0025
LAB_080d73de:
    adds r0,r5,#0x0    @ 080d73de 281c
    movs r1,#0x5    @ 080d73e0 0521
    bl get_bios_div_remainder                @ 080d73e2 37f00df8
    lsls r4,r0,#0x2    @ 080d73e6 8400
    adds r4,r4,r0    @ 080d73e8 2418
    adds r4,#0x3    @ 080d73ea 0334
    adds r0,r5,#0x0    @ 080d73ec 281c
    movs r1,#0x5    @ 080d73ee 0521
    bl bios_div                              @ 080d73f0 37f004f8
    adds r1,r0,#0x0    @ 080d73f4 011c
    lsls r1,r1,#0x3    @ 080d73f6 c900
    adds r0,r4,#0x0    @ 080d73f8 201c
    bl fill_pack_info_card_tiles             @ 080d73fa fff7c3fe
    adds r5,#0x1    @ 080d73fe 0135
    cmp r5,#0x9                              @ 080d7400 092d
    bls LAB_080d73de                         @ 080d7402 ecd9
    movs r0,#0xe3    @ 080d7404 e320
    lsls r0,r0,#0x3    @ 080d7406 c000
    add r0,r8                                @ 080d7408 4044
    movs r1,#0x21    @ 080d740a 2121
    rsbs r1,r1,#0    @ 080d740c 4942
    ldrb r2,[r0,#0x0]                        @ 080d740e 0278
    ands r1,r2    @ 080d7410 1140
    strb r1,[r0,#0x0]                        @ 080d7412 0170
    movs r1,#0x2    @ 080d7414 0221
    adds r0,r1,#0x0    @ 080d7416 081c
    ldrb r7,[r7,#0x1c]                       @ 080d7418 3f7f
    ands r0,r7    @ 080d741a 3840
    cmp r0,#0x0                              @ 080d741c 0028
    beq LAB_080d7424                         @ 080d741e 01d0
    ldr r0, DAT_080d7434                     @ 080d7420 0448
    strh r1,[r0,#0x10]                       @ 080d7422 0182
LAB_080d7424:
    movs r0,#0x1    @ 080d7424 0120
    add sp,#0xc                              @ 080d7426 03b0
    pop {r3}                                 @ 080d7428 08bc
    .hword 0x4698    @ 080d742a 9846
    pop {r4,r5,r6,r7}                        @ 080d742c f0bc
    pop {r1}                                 @ 080d742e 02bc
    bx r1                                    @ 080d7430 0847
    .zero  0x2
DAT_080d7434:
    .word  pack_ui_state                  @ 080d7434 50580003
DAT_080d7438:
    .word  0x0600e000                     @ 080d7438 00e00006
DAT_080d743c:
    .word  0x050001e0                     @ 080d743c e0010005
DAT_080d7440:
    .word  0x09ccd290                     @ 080d7440 90d2cc09
DAT_080d7444:
    .word  0x06010000                     @ 080d7444 00000106
DAT_080d7448:
    .word  0x05000200                     @ 080d7448 00020005
PTR_pack_banner_obj_palette_080d744c:
    .word  pack_banner_obj_palette        @ 080d744c 40045108
DAT_080d7450:
    .word  0x06008040                     @ 080d7450 40800006
DAT_080d7454:
    .word  0x0600f000                     @ 080d7454 00f00006

@ Drives the pack card flip-reveal animation frame. Loads pack_ui_state+0x724 as card_state ptr. If INIT_BIT (bit1 of byte[0]) not set: sets DISPCNT|=OBJ_ENABLE_BIT (0x1000), writes counter=0x25 to [+0x6], sets INIT_BIT. Decrements counter [+0x6]. Loops r7 from 9 down to 0: computes frame delta; if delta<=0 calls write_pack_card_obj_attr_by_affine_toggle with no rotation; if 0<delta<=10 calls with affine rotation params; if delta==10 calls sync_state_and_init_sprite(4). After loop: if counter < 0 clears OBJ and clears INIT_BIT. Called via indirect dispatch table 0x080d8504.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d74e4)
@ - CARD_STATE_OFFSET = 0x724 (DAT_080d74e8)
@ - INIT_BIT = 0x2 (bit1 of byte[0])
@ - DISPCNT = 0x04000000 (movs r2,#0x80; lsls r2,#0x13)
@ - OBJ_ENABLE_BIT = 0x1000 (movs r0,#0x80; lsls r0,#5)
@ - COUNTER_INIT = 0x25
@ - LOOP_START = 9
@ - ANIM_THRESHOLD_A = 0
@ - ANIM_THRESHOLD_B = 10
@ - SYNC_STATE_PARAM = 4
@ 
@ Inputs: none (entry: ldr r0, pack_ui_state)
@ Returns: void (Sub-case E: pop{r1}+bx r1; r0 in epilogue = mov r0,r9 = 0 fixed by entry movs r2,#0; mov r9,r2; dispatch callers ignore return value)
@ Side effects: DISPCNT|=0x1000 (first call only); [pack_ui_state+0x724+0x6] counter-=1, init=0x25; byte[0]|=0x2; [OAM shadow via write_pack_card_obj_attr_by_affine_toggle]; [pack state via sync_state_and_init_sprite(4)]
tick_pack_card_reveal_animation:
    push {r4,r5,r6,r7,lr}                    @ 080d7458 f0b5
    .hword 0x464f    @ 080d745a 4f46
    .hword 0x4646    @ 080d745c 4646
    push {r6,r7}                             @ 080d745e c0b4
    ldr r0, DAT_080d74e4                     @ 080d7460 2048
    movs r1,#0xc    @ 080d7462 0c21
    adds r1,r1,r0    @ 080d7464 0918
    .hword 0x4688    @ 080d7466 8846
    movs r2,#0x0    @ 080d7468 0022
    .hword 0x4691    @ 080d746a 9146
    ldr r1, DAT_080d74e8                     @ 080d746c 1e49
    adds r4,r0,r1    @ 080d746e 4418
    ldrb r3,[r4,#0x0]                        @ 080d7470 2378
    movs r0,#0x2    @ 080d7472 0220
    ands r0,r3    @ 080d7474 1840
    cmp r0,#0x0                              @ 080d7476 0028
    bne LAB_080d7494                         @ 080d7478 0cd1
    movs r2,#0x80    @ 080d747a 8022
    lsls r2,r2,#0x13    @ 080d747c d204
    movs r0,#0x80    @ 080d747e 8020
    lsls r0,r0,#0x5    @ 080d7480 4001
    ldrh r1,[r2,#0x0]                        @ 080d7482 1188
    orrs r0,r1    @ 080d7484 0843
    strh r0,[r2,#0x0]                        @ 080d7486 1080
    movs r0,#0x25    @ 080d7488 2520
    .hword 0x4642    @ 080d748a 4246
    strh r0,[r2,#0x6]                        @ 080d748c d080
    movs r0,#0x2    @ 080d748e 0220
    orrs r0,r3    @ 080d7490 1843
    strb r0,[r4,#0x0]                        @ 080d7492 2070
LAB_080d7494:
    .hword 0x4641    @ 080d7494 4146
    ldrh r0,[r1,#0x6]                        @ 080d7496 c888
    subs r0,#0x1    @ 080d7498 0138
    strh r0,[r1,#0x6]                        @ 080d749a c880
    movs r7,#0x9    @ 080d749c 0927
LAB_080d749e:
    .hword 0x4640    @ 080d749e 4046
    movs r1,#0x6    @ 080d74a0 0621
    ldrsh r2,[r0,r1]                         @ 080d74a2 425e
    movs r1,#0x9    @ 080d74a4 0921
    subs r1,r1,r7    @ 080d74a6 c91b
    lsls r0,r1,#0x1    @ 080d74a8 4800
    adds r0,r0,r1    @ 080d74aa 4018
    subs r6,r2,r0    @ 080d74ac 161a
    cmp r6,#0x0                              @ 080d74ae 002e
    bgt LAB_080d74ec                         @ 080d74b0 1cdc
    adds r0,r7,#0x0    @ 080d74b2 381c
    movs r1,#0x5    @ 080d74b4 0521
    bl get_bios_div_remainder                @ 080d74b6 36f0a3ff
    lsls r4,r0,#0x2    @ 080d74ba 8400
    adds r4,r4,r0    @ 080d74bc 2418
    lsls r4,r4,#0x3    @ 080d74be e400
    adds r4,#0x28    @ 080d74c0 2834
    adds r0,r7,#0x0    @ 080d74c2 381c
    movs r1,#0x5    @ 080d74c4 0521
    bl bios_div                              @ 080d74c6 36f099ff
    lsls r0,r0,#0x6    @ 080d74ca 8001
    adds r0,#0x20    @ 080d74cc 2030
    lsls r4,r4,#0x10    @ 080d74ce 2404
    lsrs r4,r4,#0x10    @ 080d74d0 240c
    lsls r0,r0,#0x10    @ 080d74d2 0004
    orrs r4,r0    @ 080d74d4 0443
    adds r0,r4,#0x0    @ 080d74d6 201c
    movs r1,#0x2    @ 080d74d8 0221
    movs r2,#0x80    @ 080d74da 8022
    lsls r2,r2,#0x1    @ 080d74dc 5200
    bl write_pack_card_obj_attr_by_affine_toggle @ 080d74de fff789fe
    b LAB_080d752c                           @ 080d74e2 23e0
DAT_080d74e4:
    .word  pack_ui_state                  @ 080d74e4 50580003
DAT_080d74e8:
    .word  0x00000724                     @ 080d74e8 24070000
LAB_080d74ec:
    cmp r6,#0xa                              @ 080d74ec 0a2e
    bgt LAB_080d7536                         @ 080d74ee 22dc
    lsls r0,r6,#0x7    @ 080d74f0 f001
    movs r1,#0xa    @ 080d74f2 0a21
    bl bios_div                              @ 080d74f4 36f082ff
    movs r5,#0x80    @ 080d74f8 8025
    lsls r5,r5,#0x1    @ 080d74fa 6d00
    subs r5,r5,r0    @ 080d74fc 2d1a
    adds r0,r7,#0x0    @ 080d74fe 381c
    movs r1,#0x5    @ 080d7500 0521
    bl get_bios_div_remainder                @ 080d7502 36f07dff
    lsls r4,r0,#0x2    @ 080d7506 8400
    adds r4,r4,r0    @ 080d7508 2418
    lsls r4,r4,#0x3    @ 080d750a e400
    adds r4,#0x28    @ 080d750c 2834
    adds r0,r7,#0x0    @ 080d750e 381c
    movs r1,#0x5    @ 080d7510 0521
    bl bios_div                              @ 080d7512 36f073ff
    lsls r0,r0,#0x6    @ 080d7516 8001
    adds r0,#0x20    @ 080d7518 2030
    lsls r4,r4,#0x10    @ 080d751a 2404
    lsrs r4,r4,#0x10    @ 080d751c 240c
    lsls r0,r0,#0x10    @ 080d751e 0004
    orrs r4,r0    @ 080d7520 0443
    adds r0,r4,#0x0    @ 080d7522 201c
    movs r1,#0x2    @ 080d7524 0221
    adds r2,r5,#0x0    @ 080d7526 2a1c
    bl write_pack_card_obj_attr_by_affine_toggle @ 080d7528 fff764fe
LAB_080d752c:
    cmp r6,#0xa                              @ 080d752c 0a2e
    bne LAB_080d7536                         @ 080d752e 02d1
    movs r0,#0x4    @ 080d7530 0420
    bl sync_state_and_init_sprite            @ 080d7532 22f0bffa
LAB_080d7536:
    subs r7,#0x1    @ 080d7536 013f
    cmp r7,#0x0                              @ 080d7538 002f
    bge LAB_080d749e                         @ 080d753a b0da
    .hword 0x4642    @ 080d753c 4246
    movs r1,#0x6    @ 080d753e 0621
    ldrsh r0,[r2,r1]                         @ 080d7540 505e
    cmp r0,#0x0                              @ 080d7542 0028
    bge LAB_080d7568                         @ 080d7544 10da
    movs r2,#0x80    @ 080d7546 8022
    lsls r2,r2,#0x13    @ 080d7548 d204
    movs r0,#0x80    @ 080d754a 8020
    lsls r0,r0,#0x3    @ 080d754c c000
    ldrh r1,[r2,#0x0]                        @ 080d754e 1188
    orrs r0,r1    @ 080d7550 0843
    strh r0,[r2,#0x0]                        @ 080d7552 1080
    movs r1,#0xe3    @ 080d7554 e321
    lsls r1,r1,#0x3    @ 080d7556 c900
    add r1,r8                                @ 080d7558 4144
    movs r0,#0x3    @ 080d755a 0320
    rsbs r0,r0,#0    @ 080d755c 4042
    ldrb r2,[r1,#0x0]                        @ 080d755e 0a78
    ands r0,r2    @ 080d7560 1040
    strb r0,[r1,#0x0]                        @ 080d7562 0870
    movs r0,#0x1    @ 080d7564 0120
    .hword 0x4681    @ 080d7566 8146
LAB_080d7568:
    .hword 0x4648    @ 080d7568 4846
    pop {r3,r4}                              @ 080d756a 18bc
    .hword 0x4698    @ 080d756c 9846
    .hword 0x46a1    @ 080d756e a146
    pop {r4,r5,r6,r7}                        @ 080d7570 f0bc
    pop {r1}                                 @ 080d7572 02bc
    bx r1                                    @ 080d7574 0847
    .zero  0x2

@ Called by the state machine when the pack card info page enters its initial display phase. Executes in sequence: renders the pack draw counter OBJ sprite (render_pack_draw_counter_to_sprite_vram); writes the pack name OAM tile sequence to OBJ VRAM 0x0600e426 (write_pack_name_oam_tile_sequence, tile count 15); clears AOB status flags bit[2:0] in pack_ui_state[+0x725]; renders card attribute byte sprites (render_pack_stat_byte_to_info_slot); fills the card name tile area (fill_pack_info_card_name_tiles); clears scroll positions [+0x18] and [+0x1a]; computes initial scroll position via bios_div and calls set_pack_scroll_start_pos; finally selects BG mode based on current card slot bit1 (0 = BG0/BG2/BLDCNT mode 1+2; 1 = BG0/BG3/BLDCNT mode 2+3) and writes the corresponding IO registers.
@ 
@ Constants:
@ - OBJ_VRAM_OAM_TILE = 0x0600e426 (DAT_080d762c, pack name OAM tile target)
@ - TILE_COUNT = 0xf (movs r2,#0xf)
@ - AOB_FLAG_OFFSET = 0x725 (DAT_080d7630 = 0x725, pack_ui_state[+0x725] AOB flags)
@ - BG_MASK = 0xfffc (DAT 0x0000fffc, clears low 2 bits of BG register)
@ - BLDCNT_VAL = 0x1748 (DAT_080d76b0, BG blend control)
@ - BLDALPHA_EVA = 0x10 (movs r0,#0x10 writes BLDALPHA eva component)
@ - SCROLL_TIMER_INIT = 0x14 (strh r0,[r6,#0x6] = initial scroll timer)
@ - BG0CNT = 0x04000008, BG2CNT = 0x0400000c, BG3CNT = 0x0400000e, BLDCNT = 0x04000050
init_pack_card_info_display_state:
    push {r4,r5,r6,lr}                       @ 080d7578 70b5
    ldr r4, DAT_080d7628                     @ 080d757a 2b4c
    adds r6,r4,#0x0    @ 080d757c 261c
    adds r6,#0xc    @ 080d757e 0c36
    movs r0,#0xc0    @ 080d7580 c020
    lsls r0,r0,#0x13    @ 080d7582 c004
    ldrh r1,[r6,#0x32]                       @ 080d7584 718e
    lsls r5,r1,#0x5    @ 080d7586 4d01
    adds r5,#0x44    @ 080d7588 4435
    adds r5,r5,r6    @ 080d758a ad19
    bl render_pack_draw_counter_to_sprite_vram @ 080d758c 04f06afa
    ldr r0, DAT_080d762c                     @ 080d7590 2648
    movs r1,#0x0    @ 080d7592 0021
    movs r2,#0xf    @ 080d7594 0f22
    bl write_pack_name_oam_tile_sequence     @ 080d7596 04f0f3fa
    ldr r2, DAT_080d7630                     @ 080d759a 254a
    adds r4,r4,r2    @ 080d759c a418
    movs r0,#0x5    @ 080d759e 0520
    rsbs r0,r0,#0    @ 080d75a0 4042
    ldrb r1,[r4,#0x0]                        @ 080d75a2 2178
    ands r0,r1    @ 080d75a4 0840
    strb r0,[r4,#0x0]                        @ 080d75a6 2070
    movs r0,#0x0    @ 080d75a8 0020
    bl render_pack_stat_byte_to_info_slot    @ 080d75aa fff7d7fd
    movs r0,#0x0    @ 080d75ae 0020
    movs r1,#0x0    @ 080d75b0 0021
    bl fill_pack_info_card_name_tiles        @ 080d75b2 fff703fe
    movs r0,#0x0    @ 080d75b6 0020
    strh r0,[r6,#0x18]                       @ 080d75b8 3083
    strh r0,[r6,#0x1a]                       @ 080d75ba 7083
    movs r1,#0x5    @ 080d75bc 0521
    bl get_bios_div_remainder                @ 080d75be 36f01fff
    lsls r4,r0,#0x2    @ 080d75c2 8400
    adds r4,r4,r0    @ 080d75c4 2418
    lsls r4,r4,#0x3    @ 080d75c6 e400
    adds r4,#0x28    @ 080d75c8 2834
    movs r0,#0x0    @ 080d75ca 0020
    movs r1,#0x5    @ 080d75cc 0521
    bl bios_div                              @ 080d75ce 36f015ff
    adds r1,r0,#0x0    @ 080d75d2 011c
    lsls r1,r1,#0x6    @ 080d75d4 8901
    adds r1,#0x20    @ 080d75d6 2031
    adds r0,r4,#0x0    @ 080d75d8 201c
    bl set_pack_scroll_start_pos             @ 080d75da fdf7b1f9
    movs r0,#0x2    @ 080d75de 0220
    ldrb r5,[r5,#0x1c]                       @ 080d75e0 2d7f
    ands r0,r5    @ 080d75e2 2840
    cmp r0,#0x0                              @ 080d75e4 0028
    bne LAB_080d7640                         @ 080d75e6 2bd1
    ldr r1, PTR_BG2CNT_080d7634              @ 080d75e8 1249
    ldrh r2,[r1,#0x0]                        @ 080d75ea 0a88
    ldr r3, DAT_080d7638                     @ 080d75ec 124b
    adds r0,r3,#0x0    @ 080d75ee 181c
    ands r0,r2    @ 080d75f0 1040
    strh r0,[r1,#0x0]                        @ 080d75f2 0880
    ldrh r0,[r1,#0x0]                        @ 080d75f4 0888
    strh r0,[r1,#0x0]                        @ 080d75f6 0880
    adds r1,#0x2    @ 080d75f8 0231
    ldrh r2,[r1,#0x0]                        @ 080d75fa 0a88
    adds r0,r3,#0x0    @ 080d75fc 181c
    ands r0,r2    @ 080d75fe 1040
    strh r0,[r1,#0x0]                        @ 080d7600 0880
    ldrh r0,[r1,#0x0]                        @ 080d7602 0888
    strh r0,[r1,#0x0]                        @ 080d7604 0880
    ldr r2, PTR_BG0CNT_080d763c              @ 080d7606 0d4a
    ldrh r1,[r2,#0x0]                        @ 080d7608 1188
    adds r0,r3,#0x0    @ 080d760a 181c
    ands r0,r1    @ 080d760c 0840
    strh r0,[r2,#0x0]                        @ 080d760e 1080
    ldrh r0,[r2,#0x0]                        @ 080d7610 1088
    movs r1,#0x1    @ 080d7612 0121
    orrs r0,r1    @ 080d7614 0843
    strh r0,[r2,#0x0]                        @ 080d7616 1080
    adds r2,#0x2    @ 080d7618 0232
    ldrh r0,[r2,#0x0]                        @ 080d761a 1088
    ands r3,r0    @ 080d761c 0340
    strh r3,[r2,#0x0]                        @ 080d761e 1380
    ldrh r0,[r2,#0x0]                        @ 080d7620 1088
    movs r1,#0x2    @ 080d7622 0221
    b LAB_080d7680                           @ 080d7624 2ce0
    .zero  0x2
DAT_080d7628:
    .word  pack_ui_state                  @ 080d7628 50580003
DAT_080d762c:
    .word  0x0600e426                     @ 080d762c 26e40006
DAT_080d7630:
    .word  0x00000725                     @ 080d7630 25070000
PTR_BG2CNT_080d7634:
    .word  BG2CNT                         @ 080d7634 0c000004
DAT_080d7638:
    .word  0x0000fffc                     @ 080d7638 fcff0000
PTR_BG0CNT_080d763c:
    .word  BG0CNT                         @ 080d763c 08000004
LAB_080d7640:
    ldr r1, PTR_BG3CNT_080d76a0              @ 080d7640 1749
    ldrh r2,[r1,#0x0]                        @ 080d7642 0a88
    ldr r3, DAT_080d76a4                     @ 080d7644 174b
    adds r0,r3,#0x0    @ 080d7646 181c
    ands r0,r2    @ 080d7648 1040
    strh r0,[r1,#0x0]                        @ 080d764a 0880
    ldrh r0,[r1,#0x0]                        @ 080d764c 0888
    strh r0,[r1,#0x0]                        @ 080d764e 0880
    ldr r2, PTR_BG0CNT_080d76a8              @ 080d7650 154a
    ldrh r1,[r2,#0x0]                        @ 080d7652 1188
    adds r0,r3,#0x0    @ 080d7654 181c
    ands r0,r1    @ 080d7656 0840
    strh r0,[r2,#0x0]                        @ 080d7658 1080
    ldrh r0,[r2,#0x0]                        @ 080d765a 1088
    movs r1,#0x1    @ 080d765c 0121
    orrs r0,r1    @ 080d765e 0843
    strh r0,[r2,#0x0]                        @ 080d7660 1080
    adds r2,#0x2    @ 080d7662 0232
    ldrh r1,[r2,#0x0]                        @ 080d7664 1188
    adds r0,r3,#0x0    @ 080d7666 181c
    ands r0,r1    @ 080d7668 0840
    strh r0,[r2,#0x0]                        @ 080d766a 1080
    ldrh r0,[r2,#0x0]                        @ 080d766c 1088
    movs r1,#0x2    @ 080d766e 0221
    orrs r0,r1    @ 080d7670 0843
    strh r0,[r2,#0x0]                        @ 080d7672 1080
    adds r2,#0x2    @ 080d7674 0232
    ldrh r0,[r2,#0x0]                        @ 080d7676 1088
    ands r3,r0    @ 080d7678 0340
    strh r3,[r2,#0x0]                        @ 080d767a 1380
    ldrh r0,[r2,#0x0]                        @ 080d767c 1088
    movs r1,#0x3    @ 080d767e 0321
LAB_080d7680:
    orrs r0,r1    @ 080d7680 0843
    strh r0,[r2,#0x0]                        @ 080d7682 1080
    ldr r1, PTR_BLDCNT_080d76ac              @ 080d7684 0949
    ldr r2, DAT_080d76b0                     @ 080d7686 0a4a
    adds r0,r2,#0x0    @ 080d7688 101c
    strh r0,[r1,#0x0]                        @ 080d768a 0880
    adds r1,#0x2    @ 080d768c 0231
    movs r0,#0x10    @ 080d768e 1020
    strh r0,[r1,#0x0]                        @ 080d7690 0880
    movs r0,#0x14    @ 080d7692 1420
    strh r0,[r6,#0x6]                        @ 080d7694 f080
    movs r0,#0x1    @ 080d7696 0120
    pop {r4,r5,r6}                           @ 080d7698 70bc
    pop {r1}                                 @ 080d769a 02bc
    bx r1                                    @ 080d769c 0847
    .zero  0x2
PTR_BG3CNT_080d76a0:
    .word  BG3CNT                         @ 080d76a0 0e000004
DAT_080d76a4:
    .word  0x0000fffc                     @ 080d76a4 fcff0000
PTR_BG0CNT_080d76a8:
    .word  BG0CNT                         @ 080d76a8 08000004
PTR_BLDCNT_080d76ac:
    .word  BLDCNT                         @ 080d76ac 50000004
DAT_080d76b0:
    .word  0x00001748                     @ 080d76b0 48170000

@ Called each frame during the pack card info page fade-in phase by the frame-driven state machine. First writes BLDALPHA to fully transparent (0x1f00, eva=0, evb=31) to begin fade-in; decrements pack_ui_state[+0x6] timer; if the timer is in (0..0x13] linearly computes BLDALPHA blend coefficient via bios_div and writes it; when the timer reaches 0, switches BG mode (BG0/BG1/BG1CNT+2/+3), sets BLDCNT to 0x3f3f and BLDALPHA to 0x1010, sets card slot [+0x1c] bit1; finally calls render_pack_info_card_presence_sprites and render_pack_info_card_highlight_sprite to update card presence/highlight sprites. Returns 0 (timer still counting) or 1 (switch complete; Sub-case E).
@ 
@ Constants:
@ - BLDALPHA_INIT = 0xf8<<5 = 0x1f00 (fully transparent: evb=0x1f, eva=0)
@ - FADE_TIMER_MAX = 0x14 (movs r0,#0x14)
@ - FADE_THRESHOLD = 0x13 (cmp r0,#0x13; linear fade when <=0x13)
@ - BLDCNT_FINAL = 0x3f3f (DAT_080d77a8)
@ - BLDALPHA_FINAL = 0x1010 (DAT_080d77ac, eva=0x10, evb=0x10)
@ - BG0CNT = 0x04000008, BG1CNT = 0x0400000a, BLDCNT = 0x04000050, BLDALPHA = 0x04000052
@ - CARD_FLAG_BIT = 0x2 (bit1 in slot[+0x1c])
tick_pack_card_info_fade_and_bg_mode:
    push {r4,r5,lr}                          @ 080d76b4 30b5
    ldr r0, DAT_080d76e8                     @ 080d76b6 0c48
    adds r5,r0,#0x0    @ 080d76b8 051c
    adds r5,#0xc    @ 080d76ba 0c35
    movs r4,#0x0    @ 080d76bc 0024
    movs r1,#0x80    @ 080d76be 8021
    lsls r1,r1,#0x13    @ 080d76c0 c904
    movs r0,#0xf8    @ 080d76c2 f820
    lsls r0,r0,#0x5    @ 080d76c4 4001
    strh r0,[r1,#0x0]                        @ 080d76c6 0880
    ldrh r1,[r5,#0x6]                        @ 080d76c8 e988
    subs r1,#0x1    @ 080d76ca 0139
    strh r1,[r5,#0x6]                        @ 080d76cc e980
    lsls r0,r1,#0x10    @ 080d76ce 0804
    asrs r2,r0,#0x10    @ 080d76d0 0214
    cmp r2,#0x0                              @ 080d76d2 002a
    ble LAB_080d76de                         @ 080d76d4 03dd
    movs r3,#0x6    @ 080d76d6 0623
    ldrsh r0,[r5,r3]                         @ 080d76d8 e85e
    cmp r0,#0x13                             @ 080d76da 1328
    bgt LAB_080d76ec                         @ 080d76dc 06dc
LAB_080d76de:
    adds r0,r1,#0x0    @ 080d76de 081c
    cmp r2,#0x0                              @ 080d76e0 002a
    bge LAB_080d76ee                         @ 080d76e2 04da
    movs r0,#0x0    @ 080d76e4 0020
    b LAB_080d76ee                           @ 080d76e6 02e0
DAT_080d76e8:
    .word  pack_ui_state                  @ 080d76e8 50580003
LAB_080d76ec:
    movs r0,#0x14    @ 080d76ec 1420
LAB_080d76ee:
    strh r0,[r5,#0x6]                        @ 080d76ee e880
    lsls r0,r0,#0x10    @ 080d76f0 0004
    cmp r0,#0x0                              @ 080d76f2 0028
    ble LAB_080d771c                         @ 080d76f4 12dd
    movs r1,#0x6    @ 080d76f6 0621
    ldrsh r0,[r5,r1]                         @ 080d76f8 685e
    lsls r0,r0,#0x4    @ 080d76fa 0001
    movs r1,#0x14    @ 080d76fc 1421
    bl bios_div                              @ 080d76fe 36f07dfe
    ldr r3, PTR_BLDALPHA_080d7718            @ 080d7702 054b
    lsls r2,r0,#0x18    @ 080d7704 0206
    lsrs r2,r2,#0x18    @ 080d7706 120e
    movs r1,#0x10    @ 080d7708 1021
    subs r1,r1,r0    @ 080d770a 091a
    lsls r1,r1,#0x18    @ 080d770c 0906
    lsrs r1,r1,#0x10    @ 080d770e 090c
    orrs r2,r1    @ 080d7710 0a43
    strh r2,[r3,#0x0]                        @ 080d7712 1a80
    b LAB_080d7782                           @ 080d7714 35e0
    .zero  0x2
PTR_BLDALPHA_080d7718:
    .word  BLDALPHA                       @ 080d7718 52000004
LAB_080d771c:
    ldrh r2,[r5,#0x32]                       @ 080d771c 6a8e
    lsls r4,r2,#0x5    @ 080d771e 5401
    adds r4,#0x44    @ 080d7720 4434
    adds r4,r5,r4    @ 080d7722 2c19
    ldr r1, PTR_BG0CNT_080d7798              @ 080d7724 1c49
    ldrh r2,[r1,#0x0]                        @ 080d7726 0a88
    ldr r3, DAT_080d779c                     @ 080d7728 1c4b
    adds r0,r3,#0x0    @ 080d772a 181c
    ands r0,r2    @ 080d772c 1040
    strh r0,[r1,#0x0]                        @ 080d772e 0880
    ldrh r0,[r1,#0x0]                        @ 080d7730 0888
    strh r0,[r1,#0x0]                        @ 080d7732 0880
    ldr r2, PTR_BG1CNT_080d77a0              @ 080d7734 1a4a
    ldrh r1,[r2,#0x0]                        @ 080d7736 1188
    adds r0,r3,#0x0    @ 080d7738 181c
    ands r0,r1    @ 080d773a 0840
    strh r0,[r2,#0x0]                        @ 080d773c 1080
    ldrh r0,[r2,#0x0]                        @ 080d773e 1088
    movs r1,#0x1    @ 080d7740 0121
    orrs r0,r1    @ 080d7742 0843
    strh r0,[r2,#0x0]                        @ 080d7744 1080
    adds r2,#0x2    @ 080d7746 0232
    ldrh r1,[r2,#0x0]                        @ 080d7748 1188
    adds r0,r3,#0x0    @ 080d774a 181c
    ands r0,r1    @ 080d774c 0840
    strh r0,[r2,#0x0]                        @ 080d774e 1080
    ldrh r0,[r2,#0x0]                        @ 080d7750 1088
    movs r1,#0x2    @ 080d7752 0221
    orrs r0,r1    @ 080d7754 0843
    strh r0,[r2,#0x0]                        @ 080d7756 1080
    adds r2,#0x2    @ 080d7758 0232
    ldrh r0,[r2,#0x0]                        @ 080d775a 1088
    ands r3,r0    @ 080d775c 0340
    strh r3,[r2,#0x0]                        @ 080d775e 1380
    ldrh r0,[r2,#0x0]                        @ 080d7760 1088
    movs r1,#0x3    @ 080d7762 0321
    orrs r0,r1    @ 080d7764 0843
    strh r0,[r2,#0x0]                        @ 080d7766 1080
    ldr r1, PTR_BLDCNT_080d77a4              @ 080d7768 0e49
    ldr r3, DAT_080d77a8                     @ 080d776a 0f4b
    adds r0,r3,#0x0    @ 080d776c 181c
    strh r0,[r1,#0x0]                        @ 080d776e 0880
    adds r1,#0x2    @ 080d7770 0231
    ldr r2, DAT_080d77ac                     @ 080d7772 0e4a
    adds r0,r2,#0x0    @ 080d7774 101c
    strh r0,[r1,#0x0]                        @ 080d7776 0880
    movs r0,#0x2    @ 080d7778 0220
    ldrb r3,[r4,#0x1c]                       @ 080d777a 237f
    orrs r0,r3    @ 080d777c 1843
    strb r0,[r4,#0x1c]                       @ 080d777e 2077
    movs r4,#0x1    @ 080d7780 0124
LAB_080d7782:
    movs r1,#0x6    @ 080d7782 0621
    ldrsh r0,[r5,r1]                         @ 080d7784 685e
    cmp r0,#0x1                              @ 080d7786 0128
    ble LAB_080d77b0                         @ 080d7788 12dd
    movs r0,#0x1    @ 080d778a 0120
    bl render_pack_info_card_presence_sprites @ 080d778c fff77cfd
    movs r0,#0x2    @ 080d7790 0220
    bl render_pack_info_card_highlight_sprite @ 080d7792 fff757fd
    b LAB_080d77bc                           @ 080d7796 11e0
PTR_BG0CNT_080d7798:
    .word  BG0CNT                         @ 080d7798 08000004
DAT_080d779c:
    .word  0x0000fffc                     @ 080d779c fcff0000
PTR_BG1CNT_080d77a0:
    .word  BG1CNT                         @ 080d77a0 0a000004
PTR_BLDCNT_080d77a4:
    .word  BLDCNT                         @ 080d77a4 50000004
DAT_080d77a8:
    .word  0x00003f3f                     @ 080d77a8 3f3f0000
DAT_080d77ac:
    .word  0x00001010                     @ 080d77ac 10100000
LAB_080d77b0:
    movs r0,#0x0    @ 080d77b0 0020
    bl render_pack_info_card_presence_sprites @ 080d77b2 fff769fd
    movs r0,#0x1    @ 080d77b6 0120
    bl render_pack_info_card_highlight_sprite @ 080d77b8 fff744fd
LAB_080d77bc:
    adds r0,r4,#0x0    @ 080d77bc 201c
    pop {r4,r5}                              @ 080d77be 30bc
    pop {r1}                                 @ 080d77c0 02bc
    bx r1                                    @ 080d77c2 0847

@ 拆包信息页卡片选择滚动输入帧驱动 (大型). 检测 gPrng+0x148 的多个 bit 决定滚动方向和步进: bit1 (0x2) 为 "右/下一张"; bit0 (0x1) 为 "确认/翻页"; bit4 (0x10) 为 "内部行前进"; bit5 (0x20) 为 "内部行后退"; bit6 (0x40) 为 "外部行前进"; bit7 (0x80) 为 "外部行后退"; bit9 (0x200) 为 "外层前进". 每个方向路径检查 [+0x1a] (行索引, [0..2]) 和 [+0x18] (列索引, [0..3]) 边界, 若未越界则增/减索引, 计算滚动目标位置 (行*5+列%5)*8+0x28 作为 init_pack_scroll_animation 起点, 并调 sync_state_and_init_sprite + 清卡片状态 bit0-4. 越界时调 sync_state(0x2) + 置 bit5 到 pack_ui_state+0xe3*8. 完成一步后写 pack_ui_state+0xc+0x4=5 或 0xd 或 0x6/0x7/0x8 等推进状态. 末尾调 render_pack_card_sprite_by_flip_state(0) + render_pack_info_card_presence_sprites(0) + render_pack_info_card_highlight_sprite(1). 返回 r5 (0/1).
tick_pack_info_card_scroll_input:
    push {r4,r5,r6,lr}                       @ 080d77c4 70b5
    movs r5,#0x0    @ 080d77c6 0025
    ldr r4, DAT_080d781c                     @ 080d77c8 144c
    adds r6,r4,#0x0    @ 080d77ca 261c
    adds r6,#0xc    @ 080d77cc 0c36
    ldr r1, PTR_gPrng_080d7820               @ 080d77ce 1449
    movs r0,#0xa4    @ 080d77d0 a420
    lsls r0,r0,#0x1    @ 080d77d2 4000
    adds r1,r1,r0    @ 080d77d4 0918
    movs r2,#0x2    @ 080d77d6 0222
    adds r0,r2,#0x0    @ 080d77d8 101c
    ldrh r1,[r1,#0x0]                        @ 080d77da 0988
    ands r0,r1    @ 080d77dc 0840
    cmp r0,#0x0                              @ 080d77de 0028
    beq LAB_080d785e                         @ 080d77e0 3dd0
    ldrh r1,[r6,#0x1a]                       @ 080d77e2 718b
    cmp r1,#0x1                              @ 080d77e4 0129
    bhi LAB_080d7828                         @ 080d77e6 1fd8
    strh r2,[r6,#0x1a]                       @ 080d77e8 7283
    strh r5,[r6,#0x18]                       @ 080d77ea 3583
    movs r0,#0x1    @ 080d77ec 0120
    bl set_pack_scroll_step_mode             @ 080d77ee fdf7c3f8
    ldrh r0,[r6,#0x18]                       @ 080d77f2 308b
    bl get_pack_slot_screen_y                @ 080d77f4 fff774fc
    movs r1,#0x98    @ 080d77f8 9821
    movs r2,#0x4    @ 080d77fa 0422
    bl init_pack_scroll_animation            @ 080d77fc fdf7c4f8
    movs r0,#0x1    @ 080d7800 0120
    bl sync_state_and_init_sprite            @ 080d7802 22f057f9
    ldr r2, DAT_080d7824                     @ 080d7806 074a
    adds r1,r4,r2    @ 080d7808 a118
    movs r0,#0x21    @ 080d780a 2120
    rsbs r0,r0,#0    @ 080d780c 4042
    ldrb r2,[r1,#0x0]                        @ 080d780e 0a78
    ands r0,r2    @ 080d7810 1040
    strb r0,[r1,#0x0]                        @ 080d7812 0870
    movs r0,#0x5    @ 080d7814 0520
    strh r0,[r6,#0x4]                        @ 080d7816 b080
    movs r5,#0x1    @ 080d7818 0125
    b LAB_080d785e                           @ 080d781a 20e0
DAT_080d781c:
    .word  pack_ui_state                  @ 080d781c 50580003
PTR_gPrng_080d7820:
    .word  gPrng                          @ 080d7820 40000003
DAT_080d7824:
    .word  0x00000724                     @ 080d7824 24070000
LAB_080d7828:
    ldrh r0,[r6,#0x18]                       @ 080d7828 308b
    cmp r0,#0x0                              @ 080d782a 0028
    beq LAB_080d7842                         @ 080d782c 09d0
    strh r5,[r6,#0x18]                       @ 080d782e 3583
    movs r0,#0x0    @ 080d7830 0020
    bl get_pack_slot_screen_y                @ 080d7832 fff755fc
    movs r1,#0x98    @ 080d7836 9821
    movs r2,#0x8    @ 080d7838 0822
    bl init_pack_scroll_animation            @ 080d783a fdf7a5f8
    movs r0,#0x5    @ 080d783e 0520
    b LAB_080d7844                           @ 080d7840 00e0
LAB_080d7842:
    movs r0,#0xd    @ 080d7842 0d20
LAB_080d7844:
    strh r0,[r6,#0x4]                        @ 080d7844 b080
    movs r5,#0x1    @ 080d7846 0125
    movs r0,#0x1    @ 080d7848 0120
    bl sync_state_and_init_sprite            @ 080d784a 22f033f9
    movs r0,#0xe3    @ 080d784e e320
    lsls r0,r0,#0x3    @ 080d7850 c000
    adds r1,r6,r0    @ 080d7852 3118
    movs r0,#0x21    @ 080d7854 2120
    rsbs r0,r0,#0    @ 080d7856 4042
    ldrb r2,[r1,#0x0]                        @ 080d7858 0a78
    ands r0,r2    @ 080d785a 1040
    strb r0,[r1,#0x0]                        @ 080d785c 0870
LAB_080d785e:
    ldr r0, PTR_gPrng_080d7894               @ 080d785e 0d48
    movs r1,#0xa4    @ 080d7860 a421
    lsls r1,r1,#0x1    @ 080d7862 4900
    adds r0,r0,r1    @ 080d7864 4018
    ldrh r1,[r0,#0x0]                        @ 080d7866 0188
    movs r3,#0x1    @ 080d7868 0123
    adds r0,r3,#0x0    @ 080d786a 181c
    ands r0,r1    @ 080d786c 0840
    cmp r0,#0x0                              @ 080d786e 0028
    beq LAB_080d78e8                         @ 080d7870 3ad0
    ldrh r0,[r6,#0x1a]                       @ 080d7872 708b
    cmp r0,#0x1                              @ 080d7874 0128
    bhi LAB_080d789c                         @ 080d7876 11d8
    movs r0,#0x3    @ 080d7878 0320
    bl sync_state_and_init_sprite            @ 080d787a 22f01bf9
    movs r2,#0xe3    @ 080d787e e322
    lsls r2,r2,#0x3    @ 080d7880 d200
    adds r1,r6,r2    @ 080d7882 b118
    movs r0,#0x21    @ 080d7884 2120
    rsbs r0,r0,#0    @ 080d7886 4042
    ldrb r2,[r1,#0x0]                        @ 080d7888 0a78
    ands r0,r2    @ 080d788a 1040
    strb r0,[r1,#0x0]                        @ 080d788c 0870
    ldr r1, DAT_080d7898                     @ 080d788e 0249
    movs r0,#0x6    @ 080d7890 0620
    b LAB_080d7c3a                           @ 080d7892 d2e1
PTR_gPrng_080d7894:
    .word  gPrng                          @ 080d7894 40000003
DAT_080d7898:
    .word  pack_ui_state                  @ 080d7898 50580003
LAB_080d789c:
    cmp r0,#0x2                              @ 080d789c 0228
    beq LAB_080d78a2                         @ 080d789e 00d0
    b LAB_080d7c3e                           @ 080d78a0 cde1
LAB_080d78a2:
    ldrh r0,[r6,#0x18]                       @ 080d78a2 308b
    cmp r0,#0x0                              @ 080d78a4 0028
    bne LAB_080d78c8                         @ 080d78a6 0fd1
    movs r0,#0x1    @ 080d78a8 0120
    bl sync_state_and_init_sprite            @ 080d78aa 22f003f9
    movs r0,#0xe3    @ 080d78ae e320
    lsls r0,r0,#0x3    @ 080d78b0 c000
    adds r1,r6,r0    @ 080d78b2 3118
    movs r0,#0x21    @ 080d78b4 2120
    rsbs r0,r0,#0    @ 080d78b6 4042
    ldrb r2,[r1,#0x0]                        @ 080d78b8 0a78
    ands r0,r2    @ 080d78ba 1040
    strb r0,[r1,#0x0]                        @ 080d78bc 0870
    ldr r1, DAT_080d78c4                     @ 080d78be 0149
    movs r0,#0xd    @ 080d78c0 0d20
    b LAB_080d7c3a                           @ 080d78c2 bae1
DAT_080d78c4:
    .word  pack_ui_state                  @ 080d78c4 50580003
LAB_080d78c8:
    movs r0,#0x24    @ 080d78c8 2420
    bl sync_state_and_init_sprite            @ 080d78ca 22f0f3f8
    movs r0,#0xe3    @ 080d78ce e320
    lsls r0,r0,#0x3    @ 080d78d0 c000
    adds r1,r6,r0    @ 080d78d2 3118
    movs r0,#0x21    @ 080d78d4 2120
    rsbs r0,r0,#0    @ 080d78d6 4042
    ldrb r2,[r1,#0x0]                        @ 080d78d8 0a78
    ands r0,r2    @ 080d78da 1040
    strb r0,[r1,#0x0]                        @ 080d78dc 0870
    ldr r1, DAT_080d78e4                     @ 080d78de 0149
    movs r0,#0x8    @ 080d78e0 0820
    b LAB_080d7c3a                           @ 080d78e2 aae1
DAT_080d78e4:
    .word  pack_ui_state                  @ 080d78e4 50580003
LAB_080d78e8:
    movs r0,#0x10    @ 080d78e8 1020
    ands r0,r1    @ 080d78ea 0840
    cmp r0,#0x0                              @ 080d78ec 0028
    beq LAB_080d79ae                         @ 080d78ee 5ed0
    ldrh r0,[r6,#0x1a]                       @ 080d78f0 708b
    cmp r0,#0x1                              @ 080d78f2 0128
    bhi LAB_080d7966                         @ 080d78f4 37d8
    ldrh r0,[r6,#0x18]                       @ 080d78f6 308b
    cmp r0,#0x3                              @ 080d78f8 0328
    bhi LAB_080d795c                         @ 080d78fa 2fd8
    adds r0,#0x1    @ 080d78fc 0130
    strh r0,[r6,#0x18]                       @ 080d78fe 3083
    ldr r5, DAT_080d7958                     @ 080d7900 154d
    adds r5,#0xc    @ 080d7902 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d7904 698b
    lsls r0,r1,#0x2    @ 080d7906 8800
    adds r0,r0,r1    @ 080d7908 4018
    ldrh r2,[r5,#0x18]                       @ 080d790a 2a8b
    adds r0,r2,r0    @ 080d790c 1018
    movs r1,#0x5    @ 080d790e 0521
    bl get_bios_div_remainder                @ 080d7910 36f076fd
    lsls r4,r0,#0x2    @ 080d7914 8400
    adds r4,r4,r0    @ 080d7916 2418
    lsls r4,r4,#0x3    @ 080d7918 e400
    adds r4,#0x28    @ 080d791a 2834
    ldrh r1,[r5,#0x1a]                       @ 080d791c 698b
    lsls r0,r1,#0x2    @ 080d791e 8800
    adds r0,r0,r1    @ 080d7920 4018
    ldrh r2,[r5,#0x18]                       @ 080d7922 2a8b
    adds r0,r2,r0    @ 080d7924 1018
    movs r1,#0x5    @ 080d7926 0521
    bl bios_div                              @ 080d7928 36f068fd
    adds r1,r0,#0x0    @ 080d792c 011c
    lsls r1,r1,#0x6    @ 080d792e 8901
    adds r1,#0x20    @ 080d7930 2031
    adds r0,r4,#0x0    @ 080d7932 201c
    movs r2,#0x8    @ 080d7934 0822
    bl init_pack_scroll_animation            @ 080d7936 fdf727f8
    movs r0,#0x0    @ 080d793a 0020
    bl sync_state_and_init_sprite            @ 080d793c 22f0baf8
    movs r0,#0xe3    @ 080d7940 e320
    lsls r0,r0,#0x3    @ 080d7942 c000
    adds r1,r6,r0    @ 080d7944 3118
    movs r0,#0x21    @ 080d7946 2120
    rsbs r0,r0,#0    @ 080d7948 4042
    ldrb r2,[r1,#0x0]                        @ 080d794a 0a78
    ands r0,r2    @ 080d794c 1040
    strb r0,[r1,#0x0]                        @ 080d794e 0870
    movs r0,#0x5    @ 080d7950 0520
    strh r0,[r5,#0x4]                        @ 080d7952 a880
    b LAB_080d7c3c                           @ 080d7954 72e1
    .zero  0x2
DAT_080d7958:
    .word  pack_ui_state                  @ 080d7958 50580003
LAB_080d795c:
    movs r0,#0xe3    @ 080d795c e320
    lsls r0,r0,#0x3    @ 080d795e c000
    adds r4,r6,r0    @ 080d7960 3418
    movs r0,#0x20    @ 080d7962 2020
    b LAB_080d7bf8                           @ 080d7964 48e1
LAB_080d7966:
    cmp r0,#0x2                              @ 080d7966 0228
    beq LAB_080d796c                         @ 080d7968 00d0
    b LAB_080d7c3e                           @ 080d796a 68e1
LAB_080d796c:
    ldrh r0,[r6,#0x18]                       @ 080d796c 308b
    cmp r0,#0x0                              @ 080d796e 0028
    bne LAB_080d79a4                         @ 080d7970 18d1
    adds r0,#0x1    @ 080d7972 0130
    strh r0,[r6,#0x18]                       @ 080d7974 3083
    ldrh r0,[r6,#0x18]                       @ 080d7976 308b
    bl get_pack_slot_screen_y                @ 080d7978 fff7b2fb
    movs r1,#0x98    @ 080d797c 9821
    movs r2,#0x8    @ 080d797e 0822
    bl init_pack_scroll_animation            @ 080d7980 fdf702f8
    movs r0,#0x0    @ 080d7984 0020
    bl sync_state_and_init_sprite            @ 080d7986 22f095f8
    movs r0,#0xe3    @ 080d798a e320
    lsls r0,r0,#0x3    @ 080d798c c000
    adds r1,r6,r0    @ 080d798e 3118
    movs r0,#0x21    @ 080d7990 2120
    rsbs r0,r0,#0    @ 080d7992 4042
    ldrb r2,[r1,#0x0]                        @ 080d7994 0a78
    ands r0,r2    @ 080d7996 1040
    strb r0,[r1,#0x0]                        @ 080d7998 0870
    ldr r1, DAT_080d79a0                     @ 080d799a 0149
    movs r0,#0x5    @ 080d799c 0520
    b LAB_080d7c3a                           @ 080d799e 4ce1
DAT_080d79a0:
    .word  pack_ui_state                  @ 080d79a0 50580003
LAB_080d79a4:
    movs r0,#0xe3    @ 080d79a4 e320
    lsls r0,r0,#0x3    @ 080d79a6 c000
    adds r4,r6,r0    @ 080d79a8 3418
    movs r0,#0x20    @ 080d79aa 2020
    b LAB_080d7bf8                           @ 080d79ac 24e1
LAB_080d79ae:
    movs r2,#0x20    @ 080d79ae 2022
    adds r0,r2,#0x0    @ 080d79b0 101c
    ands r0,r1    @ 080d79b2 0840
    cmp r0,#0x0                              @ 080d79b4 0028
    beq LAB_080d7a64                         @ 080d79b6 55d0
    ldrh r0,[r6,#0x1a]                       @ 080d79b8 708b
    cmp r0,#0x1                              @ 080d79ba 0128
    bhi LAB_080d7a24                         @ 080d79bc 32d8
    ldrh r0,[r6,#0x18]                       @ 080d79be 308b
    cmp r0,#0x0                              @ 080d79c0 0028
    bne LAB_080d79c6                         @ 080d79c2 00d1
    b LAB_080d7bf0                           @ 080d79c4 14e1
LAB_080d79c6:
    subs r0,#0x1    @ 080d79c6 0138
    strh r0,[r6,#0x18]                       @ 080d79c8 3083
    ldr r5, DAT_080d7a20                     @ 080d79ca 154d
    adds r5,#0xc    @ 080d79cc 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d79ce 698b
    lsls r0,r1,#0x2    @ 080d79d0 8800
    adds r0,r0,r1    @ 080d79d2 4018
    ldrh r2,[r5,#0x18]                       @ 080d79d4 2a8b
    adds r0,r2,r0    @ 080d79d6 1018
    movs r1,#0x5    @ 080d79d8 0521
    bl get_bios_div_remainder                @ 080d79da 36f011fd
    lsls r4,r0,#0x2    @ 080d79de 8400
    adds r4,r4,r0    @ 080d79e0 2418
    lsls r4,r4,#0x3    @ 080d79e2 e400
    adds r4,#0x28    @ 080d79e4 2834
    ldrh r1,[r5,#0x1a]                       @ 080d79e6 698b
    lsls r0,r1,#0x2    @ 080d79e8 8800
    adds r0,r0,r1    @ 080d79ea 4018
    ldrh r2,[r5,#0x18]                       @ 080d79ec 2a8b
    adds r0,r2,r0    @ 080d79ee 1018
    movs r1,#0x5    @ 080d79f0 0521
    bl bios_div                              @ 080d79f2 36f003fd
    adds r1,r0,#0x0    @ 080d79f6 011c
    lsls r1,r1,#0x6    @ 080d79f8 8901
    adds r1,#0x20    @ 080d79fa 2031
    adds r0,r4,#0x0    @ 080d79fc 201c
    movs r2,#0x8    @ 080d79fe 0822
    bl init_pack_scroll_animation            @ 080d7a00 fcf7c2ff
    movs r0,#0x0    @ 080d7a04 0020
    bl sync_state_and_init_sprite            @ 080d7a06 22f055f8
    movs r0,#0xe3    @ 080d7a0a e320
    lsls r0,r0,#0x3    @ 080d7a0c c000
    adds r1,r6,r0    @ 080d7a0e 3118
    movs r0,#0x21    @ 080d7a10 2120
    rsbs r0,r0,#0    @ 080d7a12 4042
    ldrb r2,[r1,#0x0]                        @ 080d7a14 0a78
    ands r0,r2    @ 080d7a16 1040
    strb r0,[r1,#0x0]                        @ 080d7a18 0870
    movs r0,#0x5    @ 080d7a1a 0520
    strh r0,[r5,#0x4]                        @ 080d7a1c a880
    b LAB_080d7c3c                           @ 080d7a1e 0de1
DAT_080d7a20:
    .word  pack_ui_state                  @ 080d7a20 50580003
LAB_080d7a24:
    cmp r0,#0x2                              @ 080d7a24 0228
    beq LAB_080d7a2a                         @ 080d7a26 00d0
    b LAB_080d7c3e                           @ 080d7a28 09e1
LAB_080d7a2a:
    ldrh r0,[r6,#0x18]                       @ 080d7a2a 308b
    cmp r0,#0x0                              @ 080d7a2c 0028
    bne LAB_080d7a32                         @ 080d7a2e 00d1
    b LAB_080d7bf0                           @ 080d7a30 dee0
LAB_080d7a32:
    subs r0,#0x1    @ 080d7a32 0138
    strh r0,[r6,#0x18]                       @ 080d7a34 3083
    ldrh r0,[r6,#0x18]                       @ 080d7a36 308b
    bl get_pack_slot_screen_y                @ 080d7a38 fff752fb
    movs r1,#0x98    @ 080d7a3c 9821
    movs r2,#0x8    @ 080d7a3e 0822
    bl init_pack_scroll_animation            @ 080d7a40 fcf7a2ff
    movs r0,#0x0    @ 080d7a44 0020
    bl sync_state_and_init_sprite            @ 080d7a46 22f035f8
    movs r0,#0xe3    @ 080d7a4a e320
    lsls r0,r0,#0x3    @ 080d7a4c c000
    adds r1,r6,r0    @ 080d7a4e 3118
    movs r0,#0x21    @ 080d7a50 2120
    rsbs r0,r0,#0    @ 080d7a52 4042
    ldrb r2,[r1,#0x0]                        @ 080d7a54 0a78
    ands r0,r2    @ 080d7a56 1040
    strb r0,[r1,#0x0]                        @ 080d7a58 0870
    ldr r1, DAT_080d7a60                     @ 080d7a5a 0149
    movs r0,#0x5    @ 080d7a5c 0520
    b LAB_080d7c3a                           @ 080d7a5e ece0
DAT_080d7a60:
    .word  pack_ui_state                  @ 080d7a60 50580003
LAB_080d7a64:
    movs r0,#0x40    @ 080d7a64 4020
    ands r0,r1    @ 080d7a66 0840
    cmp r0,#0x0                              @ 080d7a68 0028
    beq LAB_080d7b40                         @ 080d7a6a 69d0
    ldrh r0,[r6,#0x1a]                       @ 080d7a6c 708b
    adds r1,r0,#0x0    @ 080d7a6e 011c
    cmp r1,#0x1                              @ 080d7a70 0129
    bhi LAB_080d7ad8                         @ 080d7a72 31d8
    cmp r1,#0x0                              @ 080d7a74 0029
    bne LAB_080d7a7a                         @ 080d7a76 00d1
    b LAB_080d7bf0                           @ 080d7a78 bae0
LAB_080d7a7a:
    subs r0,#0x1    @ 080d7a7a 0138
    strh r0,[r6,#0x1a]                       @ 080d7a7c 7083
    ldr r5, DAT_080d7ad4                     @ 080d7a7e 154d
    adds r5,#0xc    @ 080d7a80 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d7a82 698b
    lsls r0,r1,#0x2    @ 080d7a84 8800
    adds r0,r0,r1    @ 080d7a86 4018
    ldrh r2,[r5,#0x18]                       @ 080d7a88 2a8b
    adds r0,r2,r0    @ 080d7a8a 1018
    movs r1,#0x5    @ 080d7a8c 0521
    bl get_bios_div_remainder                @ 080d7a8e 36f0b7fc
    lsls r4,r0,#0x2    @ 080d7a92 8400
    adds r4,r4,r0    @ 080d7a94 2418
    lsls r4,r4,#0x3    @ 080d7a96 e400
    adds r4,#0x28    @ 080d7a98 2834
    ldrh r1,[r5,#0x1a]                       @ 080d7a9a 698b
    lsls r0,r1,#0x2    @ 080d7a9c 8800
    adds r0,r0,r1    @ 080d7a9e 4018
    ldrh r2,[r5,#0x18]                       @ 080d7aa0 2a8b
    adds r0,r2,r0    @ 080d7aa2 1018
    movs r1,#0x5    @ 080d7aa4 0521
    bl bios_div                              @ 080d7aa6 36f0a9fc
    adds r1,r0,#0x0    @ 080d7aaa 011c
    lsls r1,r1,#0x6    @ 080d7aac 8901
    adds r1,#0x20    @ 080d7aae 2031
    adds r0,r4,#0x0    @ 080d7ab0 201c
    movs r2,#0x8    @ 080d7ab2 0822
    bl init_pack_scroll_animation            @ 080d7ab4 fcf768ff
    movs r0,#0x0    @ 080d7ab8 0020
    bl sync_state_and_init_sprite            @ 080d7aba 21f0fbff
    movs r0,#0xe3    @ 080d7abe e320
    lsls r0,r0,#0x3    @ 080d7ac0 c000
    adds r1,r6,r0    @ 080d7ac2 3118
    movs r0,#0x21    @ 080d7ac4 2120
    rsbs r0,r0,#0    @ 080d7ac6 4042
    ldrb r2,[r1,#0x0]                        @ 080d7ac8 0a78
    ands r0,r2    @ 080d7aca 1040
    strb r0,[r1,#0x0]                        @ 080d7acc 0870
    movs r0,#0x5    @ 080d7ace 0520
    strh r0,[r5,#0x4]                        @ 080d7ad0 a880
    b LAB_080d7c3c                           @ 080d7ad2 b3e0
DAT_080d7ad4:
    .word  pack_ui_state                  @ 080d7ad4 50580003
LAB_080d7ad8:
    cmp r1,#0x2                              @ 080d7ad8 0229
    beq LAB_080d7ade                         @ 080d7ada 00d0
    b LAB_080d7c3e                           @ 080d7adc afe0
LAB_080d7ade:
    strh r1,[r6,#0x18]                       @ 080d7ade 3183
    subs r0,#0x1    @ 080d7ae0 0138
    strh r0,[r6,#0x1a]                       @ 080d7ae2 7083
    movs r0,#0x0    @ 080d7ae4 0020
    bl sync_state_and_init_sprite            @ 080d7ae6 21f0e5ff
    movs r0,#0xe3    @ 080d7aea e320
    lsls r0,r0,#0x3    @ 080d7aec c000
    adds r1,r6,r0    @ 080d7aee 3118
    movs r0,#0x21    @ 080d7af0 2120
    rsbs r0,r0,#0    @ 080d7af2 4042
    ldrb r2,[r1,#0x0]                        @ 080d7af4 0a78
    ands r0,r2    @ 080d7af6 1040
    strb r0,[r1,#0x0]                        @ 080d7af8 0870
    ldr r5, DAT_080d7b3c                     @ 080d7afa 104d
    adds r5,#0xc    @ 080d7afc 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d7afe 698b
    lsls r0,r1,#0x2    @ 080d7b00 8800
    adds r0,r0,r1    @ 080d7b02 4018
    ldrh r2,[r5,#0x18]                       @ 080d7b04 2a8b
    adds r0,r2,r0    @ 080d7b06 1018
    movs r1,#0x5    @ 080d7b08 0521
    bl get_bios_div_remainder                @ 080d7b0a 36f079fc
    lsls r4,r0,#0x2    @ 080d7b0e 8400
    adds r4,r4,r0    @ 080d7b10 2418
    lsls r4,r4,#0x3    @ 080d7b12 e400
    adds r4,#0x28    @ 080d7b14 2834
    ldrh r1,[r5,#0x1a]                       @ 080d7b16 698b
    lsls r0,r1,#0x2    @ 080d7b18 8800
    adds r0,r0,r1    @ 080d7b1a 4018
    ldrh r2,[r5,#0x18]                       @ 080d7b1c 2a8b
    adds r0,r2,r0    @ 080d7b1e 1018
    movs r1,#0x5    @ 080d7b20 0521
    bl bios_div                              @ 080d7b22 36f06bfc
    adds r1,r0,#0x0    @ 080d7b26 011c
    lsls r1,r1,#0x6    @ 080d7b28 8901
    adds r1,#0x20    @ 080d7b2a 2031
    adds r0,r4,#0x0    @ 080d7b2c 201c
    movs r2,#0x8    @ 080d7b2e 0822
    bl init_pack_scroll_animation            @ 080d7b30 fcf72aff
    movs r0,#0x5    @ 080d7b34 0520
    strh r0,[r5,#0x4]                        @ 080d7b36 a880
    b LAB_080d7c3c                           @ 080d7b38 80e0
    .zero  0x2
DAT_080d7b3c:
    .word  pack_ui_state                  @ 080d7b3c 50580003
LAB_080d7b40:
    movs r0,#0x80    @ 080d7b40 8020
    ands r0,r1    @ 080d7b42 0840
    cmp r0,#0x0                              @ 080d7b44 0028
    beq LAB_080d7c10                         @ 080d7b46 63d0
    ldrh r0,[r6,#0x1a]                       @ 080d7b48 708b
    adds r1,r0,#0x0    @ 080d7b4a 011c
    cmp r1,#0x1                              @ 080d7b4c 0129
    bhi LAB_080d7bf0                         @ 080d7b4e 4fd8
    cmp r1,#0x0                              @ 080d7b50 0029
    bne LAB_080d7bb4                         @ 080d7b52 2fd1
    adds r0,#0x1    @ 080d7b54 0130
    strh r0,[r6,#0x1a]                       @ 080d7b56 7083
    ldr r5, DAT_080d7bb0                     @ 080d7b58 154d
    adds r5,#0xc    @ 080d7b5a 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d7b5c 698b
    lsls r0,r1,#0x2    @ 080d7b5e 8800
    adds r0,r0,r1    @ 080d7b60 4018
    ldrh r2,[r5,#0x18]                       @ 080d7b62 2a8b
    adds r0,r2,r0    @ 080d7b64 1018
    movs r1,#0x5    @ 080d7b66 0521
    bl get_bios_div_remainder                @ 080d7b68 36f04afc
    lsls r4,r0,#0x2    @ 080d7b6c 8400
    adds r4,r4,r0    @ 080d7b6e 2418
    lsls r4,r4,#0x3    @ 080d7b70 e400
    adds r4,#0x28    @ 080d7b72 2834
    ldrh r1,[r5,#0x1a]                       @ 080d7b74 698b
    lsls r0,r1,#0x2    @ 080d7b76 8800
    adds r0,r0,r1    @ 080d7b78 4018
    ldrh r2,[r5,#0x18]                       @ 080d7b7a 2a8b
    adds r0,r2,r0    @ 080d7b7c 1018
    movs r1,#0x5    @ 080d7b7e 0521
    bl bios_div                              @ 080d7b80 36f03cfc
    adds r1,r0,#0x0    @ 080d7b84 011c
    lsls r1,r1,#0x6    @ 080d7b86 8901
    adds r1,#0x20    @ 080d7b88 2031
    adds r0,r4,#0x0    @ 080d7b8a 201c
    movs r2,#0x8    @ 080d7b8c 0822
    bl init_pack_scroll_animation            @ 080d7b8e fcf7fbfe
    movs r0,#0x0    @ 080d7b92 0020
    bl sync_state_and_init_sprite            @ 080d7b94 21f08eff
    movs r0,#0xe3    @ 080d7b98 e320
    lsls r0,r0,#0x3    @ 080d7b9a c000
    adds r1,r6,r0    @ 080d7b9c 3118
    movs r0,#0x21    @ 080d7b9e 2120
    rsbs r0,r0,#0    @ 080d7ba0 4042
    ldrb r2,[r1,#0x0]                        @ 080d7ba2 0a78
    ands r0,r2    @ 080d7ba4 1040
    strb r0,[r1,#0x0]                        @ 080d7ba6 0870
    movs r0,#0x5    @ 080d7ba8 0520
    strh r0,[r5,#0x4]                        @ 080d7baa a880
    b LAB_080d7c3c                           @ 080d7bac 46e0
    .zero  0x2
DAT_080d7bb0:
    .word  pack_ui_state                  @ 080d7bb0 50580003
LAB_080d7bb4:
    movs r0,#0x2    @ 080d7bb4 0220
    strh r0,[r6,#0x1a]                       @ 080d7bb6 7083
    strh r3,[r6,#0x18]                       @ 080d7bb8 3383
    movs r0,#0x1    @ 080d7bba 0120
    bl set_pack_scroll_step_mode             @ 080d7bbc fcf7dcfe
    ldrh r0,[r6,#0x18]                       @ 080d7bc0 308b
    bl get_pack_slot_screen_y                @ 080d7bc2 fff78dfa
    movs r1,#0x98    @ 080d7bc6 9821
    movs r2,#0x8    @ 080d7bc8 0822
    bl init_pack_scroll_animation            @ 080d7bca fcf7ddfe
    movs r0,#0x0    @ 080d7bce 0020
    bl sync_state_and_init_sprite            @ 080d7bd0 21f070ff
    movs r0,#0xe3    @ 080d7bd4 e320
    lsls r0,r0,#0x3    @ 080d7bd6 c000
    adds r1,r6,r0    @ 080d7bd8 3118
    movs r0,#0x21    @ 080d7bda 2120
    rsbs r0,r0,#0    @ 080d7bdc 4042
    ldrb r2,[r1,#0x0]                        @ 080d7bde 0a78
    ands r0,r2    @ 080d7be0 1040
    strb r0,[r1,#0x0]                        @ 080d7be2 0870
    ldr r1, DAT_080d7bec                     @ 080d7be4 0149
    movs r0,#0x5    @ 080d7be6 0520
    b LAB_080d7c3a                           @ 080d7be8 27e0
    .zero  0x2
DAT_080d7bec:
    .word  pack_ui_state                  @ 080d7bec 50580003
LAB_080d7bf0:
    movs r0,#0xe3    @ 080d7bf0 e320
    lsls r0,r0,#0x3    @ 080d7bf2 c000
    adds r4,r6,r0    @ 080d7bf4 3418
    adds r0,r2,#0x0    @ 080d7bf6 101c
LAB_080d7bf8:
    ldrb r1,[r4,#0x0]                        @ 080d7bf8 2178
    ands r0,r1    @ 080d7bfa 0840
    cmp r0,#0x0                              @ 080d7bfc 0028
    bne LAB_080d7c3e                         @ 080d7bfe 1ed1
    movs r0,#0x2    @ 080d7c00 0220
    bl sync_state_and_init_sprite            @ 080d7c02 21f057ff
    movs r0,#0x20    @ 080d7c06 2020
    ldrb r2,[r4,#0x0]                        @ 080d7c08 2278
    orrs r0,r2    @ 080d7c0a 1043
    strb r0,[r4,#0x0]                        @ 080d7c0c 2070
    b LAB_080d7c3e                           @ 080d7c0e 16e0
LAB_080d7c10:
    movs r0,#0x80    @ 080d7c10 8020
    lsls r0,r0,#0x1    @ 080d7c12 4000
    ands r0,r1    @ 080d7c14 0840
    cmp r0,#0x0                              @ 080d7c16 0028
    beq LAB_080d7c3e                         @ 080d7c18 11d0
    ldrh r0,[r6,#0x1a]                       @ 080d7c1a 708b
    cmp r0,#0x1                              @ 080d7c1c 0128
    bhi LAB_080d7c3e                         @ 080d7c1e 0ed8
    movs r0,#0x3    @ 080d7c20 0320
    bl sync_state_and_init_sprite            @ 080d7c22 21f047ff
    movs r2,#0xe3    @ 080d7c26 e322
    lsls r2,r2,#0x3    @ 080d7c28 d200
    adds r1,r6,r2    @ 080d7c2a b118
    movs r0,#0x21    @ 080d7c2c 2120
    rsbs r0,r0,#0    @ 080d7c2e 4042
    ldrb r2,[r1,#0x0]                        @ 080d7c30 0a78
    ands r0,r2    @ 080d7c32 1040
    strb r0,[r1,#0x0]                        @ 080d7c34 0870
    ldr r1, DAT_080d7c80                     @ 080d7c36 1249
    movs r0,#0x7    @ 080d7c38 0720
LAB_080d7c3a:
    strh r0,[r1,#0x10]                       @ 080d7c3a 0882
LAB_080d7c3c:
    movs r5,#0x1    @ 080d7c3c 0125
LAB_080d7c3e:
    cmp r5,#0x1                              @ 080d7c3e 012d
    beq LAB_080d7c54                         @ 080d7c40 08d0
    ldr r0, PTR_gPrng_080d7c84               @ 080d7c42 1048
    movs r2,#0xa3    @ 080d7c44 a322
    lsls r2,r2,#0x1    @ 080d7c46 5200
    adds r1,r0,r2    @ 080d7c48 8118
    movs r0,#0xf0    @ 080d7c4a f020
    ldrh r1,[r1,#0x0]                        @ 080d7c4c 0988
    ands r0,r1    @ 080d7c4e 0840
    cmp r0,#0x0                              @ 080d7c50 0028
    bne LAB_080d7c64                         @ 080d7c52 07d1
LAB_080d7c54:
    movs r0,#0xe3    @ 080d7c54 e320
    lsls r0,r0,#0x3    @ 080d7c56 c000
    adds r1,r6,r0    @ 080d7c58 3118
    movs r0,#0x21    @ 080d7c5a 2120
    rsbs r0,r0,#0    @ 080d7c5c 4042
    ldrb r2,[r1,#0x0]                        @ 080d7c5e 0a78
    ands r0,r2    @ 080d7c60 1040
    strb r0,[r1,#0x0]                        @ 080d7c62 0870
LAB_080d7c64:
    movs r0,#0x0    @ 080d7c64 0020
    bl render_pack_card_sprite_by_flip_state @ 080d7c66 fcf71ffd
    movs r0,#0x0    @ 080d7c6a 0020
    bl render_pack_info_card_presence_sprites @ 080d7c6c fff70cfb
    movs r0,#0x1    @ 080d7c70 0120
    bl render_pack_info_card_highlight_sprite @ 080d7c72 fff7e7fa
    adds r0,r5,#0x0    @ 080d7c76 281c
    pop {r4,r5,r6}                           @ 080d7c78 70bc
    pop {r1}                                 @ 080d7c7a 02bc
    bx r1                                    @ 080d7c7c 0847
    .zero  0x2
DAT_080d7c80:
    .word  pack_ui_state                  @ 080d7c80 50580003
PTR_gPrng_080d7c84:
    .word  gPrng                          @ 080d7c84 40000003

@ 拆包信息页卡片滚动插值步进帧驱动. 从 pack_ui_state+0xc 区读取. 调 tick_pack_scroll_interp_step: 若返回 1 (插值完成) 则检查 [+0x1a] 是否为 2 (已到 row 2); 若是则 set_pack_scroll_step_mode(1); 否则 set_pack_scroll_step_mode(0). 再写 pack_ui_state+0x10=4 推进到步骤 4. 末尾无条件调 render_pack_card_sprite_by_flip_state(0) + render_pack_info_card_presence_sprites(0) + render_pack_info_card_highlight_sprite(1). 返回 r5 = tick_pack_scroll_interp_step 结果 (0=进行中, 1=完成).
tick_pack_info_card_scroll_step:
    push {r4,r5,lr}                          @ 080d7c88 30b5
    ldr r0, DAT_080d7ca8                     @ 080d7c8a 0748
    adds r4,r0,#0x0    @ 080d7c8c 041c
    adds r4,#0xc    @ 080d7c8e 0c34
    bl tick_pack_scroll_interp_step          @ 080d7c90 fcf71afe
    adds r5,r0,#0x0    @ 080d7c94 051c
    cmp r5,#0x1                              @ 080d7c96 012d
    bne LAB_080d7cb8                         @ 080d7c98 0ed1
    ldrh r4,[r4,#0x1a]                       @ 080d7c9a 648b
    cmp r4,#0x2                              @ 080d7c9c 022c
    beq LAB_080d7cac                         @ 080d7c9e 05d0
    movs r0,#0x0    @ 080d7ca0 0020
    bl set_pack_scroll_step_mode             @ 080d7ca2 fcf769fe
    b LAB_080d7cb2                           @ 080d7ca6 04e0
DAT_080d7ca8:
    .word  pack_ui_state                  @ 080d7ca8 50580003
LAB_080d7cac:
    movs r0,#0x1    @ 080d7cac 0120
    bl set_pack_scroll_step_mode             @ 080d7cae fcf763fe
LAB_080d7cb2:
    ldr r1, DAT_080d7cd4                     @ 080d7cb2 0849
    movs r0,#0x4    @ 080d7cb4 0420
    strh r0,[r1,#0x10]                       @ 080d7cb6 0882
LAB_080d7cb8:
    movs r0,#0x0    @ 080d7cb8 0020
    bl render_pack_card_sprite_by_flip_state @ 080d7cba fcf7f5fc
    movs r0,#0x0    @ 080d7cbe 0020
    bl render_pack_info_card_presence_sprites @ 080d7cc0 fff7e2fa
    movs r0,#0x1    @ 080d7cc4 0120
    bl render_pack_info_card_highlight_sprite @ 080d7cc6 fff7bdfa
    adds r0,r5,#0x0    @ 080d7cca 281c
    pop {r4,r5}                              @ 080d7ccc 30bc
    pop {r1}                                 @ 080d7cce 02bc
    bx r1                                    @ 080d7cd0 0847
    .zero  0x2
DAT_080d7cd4:
    .word  pack_ui_state                  @ 080d7cd4 50580003

@ 拆包信息页卡片选择切换帧驱动. 从 pack_ui_state+0xc 读取 [+0x1a] (行索引) 和 [+0x18] (列索引) 确定当前 slot r7. 计算 slot_state 结构偏移 ([+0x32]*32+0x44+base) 取 slot_desc r4. 若 [r4+0x14] bit r7 已置: 说明此 slot 已选中, 则 [+0x18]-=1 + decrement_pack_slot_selection_count. 否则: 调 enforce_pack_purchase_limit 检查购买上限; 若允许则 [+0x18]+=1 + increment_pack_slot_selection_count + toggle bit r7 + 更新 pack_ui_state+0x719 byte bit2-3 (render_stat_byte) + fill_pack_info_card_name_tiles + render_pack_card_sprite_by_flip_state + render_pack_info_card_presence_sprites + render_pack_info_card_highlight_sprite + state=4. 若上限禁止且当前 row 需要跳转: set_pack_scroll_step_mode(1) + get_pack_slot_screen_y + init_pack_scroll_animation + tick_scroll_loop + state=0xa. 固定返回 1.
tick_pack_info_card_select_toggle:
    push {r4,r5,r6,r7,lr}                    @ 080d7cd8 f0b5
    ldr r0, DAT_080d7d10                     @ 080d7cda 0d48
    adds r5,r0,#0x0    @ 080d7cdc 051c
    adds r5,#0xc    @ 080d7cde 0c35
    ldrh r1,[r5,#0x1a]                       @ 080d7ce0 698b
    lsls r0,r1,#0x2    @ 080d7ce2 8800
    adds r0,r0,r1    @ 080d7ce4 4018
    ldrh r1,[r5,#0x18]                       @ 080d7ce6 298b
    adds r7,r1,r0    @ 080d7ce8 0f18
    ldrh r2,[r5,#0x32]                       @ 080d7cea 6a8e
    lsls r0,r2,#0x5    @ 080d7cec 5001
    adds r0,#0x44    @ 080d7cee 4430
    adds r4,r0,r5    @ 080d7cf0 4419
    movs r6,#0x1    @ 080d7cf2 0126
    adds r1,r6,#0x0    @ 080d7cf4 311c
    lsls r1,r7    @ 080d7cf6 b940
    ldr r0,[r4,#0x14]                        @ 080d7cf8 6069
    ands r0,r1    @ 080d7cfa 0840
    cmp r0,#0x0                              @ 080d7cfc 0028
    beq LAB_080d7d14                         @ 080d7cfe 09d0
    ldrh r0,[r4,#0x18]                       @ 080d7d00 208b
    subs r0,#0x1    @ 080d7d02 0138
    strh r0,[r4,#0x18]                       @ 080d7d04 2083
    ldrh r0,[r5,#0x32]                       @ 080d7d06 688e
    movs r1,#0x1    @ 080d7d08 0121
    bl decrement_pack_slot_selection_count   @ 080d7d0a 03f0f9fc
    b LAB_080d7d5c                           @ 080d7d0e 25e0
DAT_080d7d10:
    .word  pack_ui_state                  @ 080d7d10 50580003
LAB_080d7d14:
    adds r0,r2,#0x0    @ 080d7d14 101c
    movs r1,#0x1    @ 080d7d16 0121
    bl enforce_pack_purchase_limit           @ 080d7d18 03f054fd
    cmp r0,#0x0                              @ 080d7d1c 0028
    beq LAB_080d7d30                         @ 080d7d1e 07d0
    ldrh r0,[r4,#0x18]                       @ 080d7d20 208b
    adds r0,#0x1    @ 080d7d22 0130
    strh r0,[r4,#0x18]                       @ 080d7d24 2083
    ldrh r0,[r5,#0x32]                       @ 080d7d26 688e
    movs r1,#0x1    @ 080d7d28 0121
    bl increment_pack_slot_selection_count   @ 080d7d2a 03f0c5fc
    b LAB_080d7d5c                           @ 080d7d2e 15e0
LAB_080d7d30:
    movs r0,#0x2    @ 080d7d30 0220
    strh r0,[r5,#0x1a]                       @ 080d7d32 6883
    strh r6,[r5,#0x18]                       @ 080d7d34 2e83
    movs r0,#0x1    @ 080d7d36 0120
    bl set_pack_scroll_step_mode             @ 080d7d38 fcf71efe
    ldrh r0,[r5,#0x18]                       @ 080d7d3c 288b
    bl get_pack_slot_screen_y                @ 080d7d3e fff7cff9
    movs r1,#0x98    @ 080d7d42 9821
    movs r2,#0x1    @ 080d7d44 0122
    bl init_pack_scroll_animation            @ 080d7d46 fcf71ffe
LAB_080d7d4a:
    bl tick_pack_scroll_interp_step          @ 080d7d4a fcf7bdfd
    cmp r0,#0x0                              @ 080d7d4e 0028
    beq LAB_080d7d4a                         @ 080d7d50 fbd0
    ldr r1, DAT_080d7d58                     @ 080d7d52 0149
    movs r0,#0xa    @ 080d7d54 0a20
    b LAB_080d7daa                           @ 080d7d56 28e0
DAT_080d7d58:
    .word  pack_ui_state                  @ 080d7d58 50580003
LAB_080d7d5c:
    movs r1,#0x1    @ 080d7d5c 0121
    lsls r1,r7    @ 080d7d5e b940
    ldr r0,[r4,#0x14]                        @ 080d7d60 6069
    eors r0,r1    @ 080d7d62 4840
    str r0,[r4,#0x14]                        @ 080d7d64 6061
    ldr r0, DAT_080d7db4                     @ 080d7d66 1348
    adds r4,r5,r0    @ 080d7d68 2c18
    ldrb r2,[r4,#0x0]                        @ 080d7d6a 2278
    lsls r0,r2,#0x1d    @ 080d7d6c 5007
    lsrs r0,r0,#0x1f    @ 080d7d6e c00f
    movs r1,#0x1    @ 080d7d70 0121
    eors r1,r0    @ 080d7d72 4140
    lsls r1,r1,#0x2    @ 080d7d74 8900
    movs r0,#0x5    @ 080d7d76 0520
    rsbs r0,r0,#0    @ 080d7d78 4042
    ands r0,r2    @ 080d7d7a 1040
    orrs r0,r1    @ 080d7d7c 0843
    strb r0,[r4,#0x0]                        @ 080d7d7e 2070
    lsls r0,r0,#0x1d    @ 080d7d80 4007
    lsrs r0,r0,#0x1f    @ 080d7d82 c00f
    bl render_pack_stat_byte_to_info_slot    @ 080d7d84 fff7eaf9
    ldrb r4,[r4,#0x0]                        @ 080d7d88 2478
    lsls r1,r4,#0x1d    @ 080d7d8a 6107
    lsrs r1,r1,#0x1f    @ 080d7d8c c90f
    movs r0,#0x0    @ 080d7d8e 0020
    bl fill_pack_info_card_name_tiles        @ 080d7d90 fff714fa
    movs r0,#0x0    @ 080d7d94 0020
    bl render_pack_card_sprite_by_flip_state @ 080d7d96 fcf787fc
    movs r0,#0x0    @ 080d7d9a 0020
    bl render_pack_info_card_presence_sprites @ 080d7d9c fff774fa
    movs r0,#0x1    @ 080d7da0 0120
    bl render_pack_info_card_highlight_sprite @ 080d7da2 fff74ffa
    ldr r1, DAT_080d7db8                     @ 080d7da6 0449
    movs r0,#0x4    @ 080d7da8 0420
LAB_080d7daa:
    strh r0,[r1,#0x10]                       @ 080d7daa 0882
    movs r0,#0x1    @ 080d7dac 0120
    pop {r4,r5,r6,r7}                        @ 080d7dae f0bc
    pop {r1}                                 @ 080d7db0 02bc
    bx r1                                    @ 080d7db2 0847
DAT_080d7db4:
    .word  0x00000719                     @ 080d7db4 19070000
DAT_080d7db8:
    .word  pack_ui_state                  @ 080d7db8 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 8.
@ Per-frame handler for pack card info page slot selection input. Scans bit-field [+0x14]
@ to check if a slot is already active: if so, decrements selection count and clears the bit
@ via decrement_pack_slot_selection_count; otherwise validates each candidate slot with
@ enforce_pack_purchase_limit, on pass calls increment_pack_slot_selection_count and sets bit.
@ If purchase limit is full: writes [+0x1a]:=2, [+0x18]:=2, calls set_pack_scroll_step_mode(1),
@ blocks in tick_pack_scroll_interp_step loop until scroll completes, then writes [+0x10]:=4
@ to advance the state machine. Unconditionally calls render_pack_stat_byte_to_info_slot,
@ fill_pack_info_card_name_tiles, render_pack_card_sprite_by_flip_state(0),
@ render_pack_info_card_presence_sprites(0), render_pack_info_card_highlight_sprite(1).
@ Returns 1 (Sub-case E pop{r1};bx r1, movs r0,#1 @ 080d7edc fixed).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080d7e24)
@ Returns: r0=u8 1 (step-complete flag)
@ Side effects:
@   [pack_ui_state+0xc+0x18] := 2 (on limit-full path)
@   [pack_ui_state+0xc+0x1a] := 2 (on limit-full path)
@   [slot_entry+0x18] += or -= 1 (per-slot selection count)
@   [slot_entry+0x14] bit set/clear
@   [pack_ui_state+0xc+0x10] := 4 (state-machine step, on limit-full path)
@ Constants:
@   pack_ui_state = 0x03005850
@   SCROLL_TARGET_Y = 0x98
@   SCROLL_MODE = 1
@   NEXT_STATE = 4
@   MAX_SLOT_IDX = 9
tick_pack_card_info_selection_input:
    push {r4,r5,r6,r7,lr}                    @ 080d7dbc f0b5
    .hword 0x464f    @ 080d7dbe 4f46
    .hword 0x4646    @ 080d7dc0 4646
    push {r6,r7}                             @ 080d7dc2 c0b4
    ldr r0, DAT_080d7e24                     @ 080d7dc4 1748
    adds r7,r0,#0x0    @ 080d7dc6 071c
    adds r7,#0xc    @ 080d7dc8 0c37
    ldrh r1,[r7,#0x32]                       @ 080d7dca 798e
    lsls r0,r1,#0x5    @ 080d7dcc 4801
    adds r0,#0x44    @ 080d7dce 4430
    adds r4,r0,r7    @ 080d7dd0 c419
    movs r2,#0x0    @ 080d7dd2 0022
    movs r6,#0x0    @ 080d7dd4 0026
    movs r1,#0x1    @ 080d7dd6 0121
    ldr r0,[r4,#0x14]                        @ 080d7dd8 6069
    ands r0,r1    @ 080d7dda 0840
    cmp r0,#0x0                              @ 080d7ddc 0028
    beq LAB_080d7e28                         @ 080d7dde 23d0
LAB_080d7de0:
    adds r6,#0x1    @ 080d7de0 0136
    cmp r6,#0x9                              @ 080d7de2 092e
    bhi LAB_080d7df4                         @ 080d7de4 06d8
    movs r1,#0x1    @ 080d7de6 0121
    lsls r1,r6    @ 080d7de8 b140
    ldr r0,[r4,#0x14]                        @ 080d7dea 6069
    ands r0,r1    @ 080d7dec 0840
    cmp r0,#0x0                              @ 080d7dee 0028
    bne LAB_080d7de0                         @ 080d7df0 f6d1
    movs r2,#0x1    @ 080d7df2 0122
LAB_080d7df4:
    cmp r2,#0x0                              @ 080d7df4 002a
    bne LAB_080d7e28                         @ 080d7df6 17d1
    movs r6,#0x0    @ 080d7df8 0026
LAB_080d7dfa:
    movs r5,#0x1    @ 080d7dfa 0125
    lsls r5,r6    @ 080d7dfc b540
    ldr r0,[r4,#0x14]                        @ 080d7dfe 6069
    ands r0,r5    @ 080d7e00 2840
    cmp r0,#0x0                              @ 080d7e02 0028
    beq LAB_080d7e1a                         @ 080d7e04 09d0
    ldrh r0,[r4,#0x18]                       @ 080d7e06 208b
    subs r0,#0x1    @ 080d7e08 0138
    strh r0,[r4,#0x18]                       @ 080d7e0a 2083
    ldrh r0,[r7,#0x32]                       @ 080d7e0c 788e
    movs r1,#0x1    @ 080d7e0e 0121
    bl decrement_pack_slot_selection_count   @ 080d7e10 03f076fc
    ldr r0,[r4,#0x14]                        @ 080d7e14 6069
    eors r0,r5    @ 080d7e16 6840
    str r0,[r4,#0x14]                        @ 080d7e18 6061
LAB_080d7e1a:
    adds r6,#0x1    @ 080d7e1a 0136
    cmp r6,#0x9                              @ 080d7e1c 092e
    bls LAB_080d7dfa                         @ 080d7e1e ecd9
    b LAB_080d7e96                           @ 080d7e20 39e0
    .zero  0x2
DAT_080d7e24:
    .word  pack_ui_state                  @ 080d7e24 50580003
LAB_080d7e28:
    movs r6,#0x0    @ 080d7e28 0026
    movs r0,#0x1    @ 080d7e2a 0120
    .hword 0x4680    @ 080d7e2c 8046
    ldr r1, DAT_080d7e60                     @ 080d7e2e 0c49
    .hword 0x4689    @ 080d7e30 8946
LAB_080d7e32:
    .hword 0x4645    @ 080d7e32 4546
    lsls r5,r6    @ 080d7e34 b540
    ldr r0,[r4,#0x14]                        @ 080d7e36 6069
    ands r0,r5    @ 080d7e38 2840
    cmp r0,#0x0                              @ 080d7e3a 0028
    bne LAB_080d7e90                         @ 080d7e3c 28d1
    ldrh r0,[r7,#0x32]                       @ 080d7e3e 788e
    movs r1,#0x1    @ 080d7e40 0121
    bl enforce_pack_purchase_limit           @ 080d7e42 03f0bffc
    cmp r0,#0x0                              @ 080d7e46 0028
    beq LAB_080d7e64                         @ 080d7e48 0cd0
    ldrh r0,[r4,#0x18]                       @ 080d7e4a 208b
    adds r0,#0x1    @ 080d7e4c 0130
    strh r0,[r4,#0x18]                       @ 080d7e4e 2083
    ldrh r0,[r7,#0x32]                       @ 080d7e50 788e
    movs r1,#0x1    @ 080d7e52 0121
    bl increment_pack_slot_selection_count   @ 080d7e54 03f030fc
    ldr r0,[r4,#0x14]                        @ 080d7e58 6069
    orrs r0,r5    @ 080d7e5a 2843
    str r0,[r4,#0x14]                        @ 080d7e5c 6061
    b LAB_080d7e90                           @ 080d7e5e 17e0
DAT_080d7e60:
    .word  0x0300585c                     @ 080d7e60 5c580003
LAB_080d7e64:
    movs r0,#0x2    @ 080d7e64 0220
    strh r0,[r7,#0x1a]                       @ 080d7e66 7883
    .hword 0x4640    @ 080d7e68 4046
    strh r0,[r7,#0x18]                       @ 080d7e6a 3883
    movs r0,#0x1    @ 080d7e6c 0120
    bl set_pack_scroll_step_mode             @ 080d7e6e fcf783fd
    ldrh r0,[r7,#0x18]                       @ 080d7e72 388b
    bl get_pack_slot_screen_y                @ 080d7e74 fff734f9
    movs r1,#0x98    @ 080d7e78 9821
    movs r2,#0x1    @ 080d7e7a 0122
    bl init_pack_scroll_animation            @ 080d7e7c fcf784fd
LAB_080d7e80:
    bl tick_pack_scroll_interp_step          @ 080d7e80 fcf722fd
    cmp r0,#0x0                              @ 080d7e84 0028
    beq LAB_080d7e80                         @ 080d7e86 fbd0
    movs r0,#0xa    @ 080d7e88 0a20
    .hword 0x4649    @ 080d7e8a 4946
    strh r0,[r1,#0x4]                        @ 080d7e8c 8880
    b LAB_080d7edc                           @ 080d7e8e 25e0
LAB_080d7e90:
    adds r6,#0x1    @ 080d7e90 0136
    cmp r6,#0x9                              @ 080d7e92 092e
    bls LAB_080d7e32                         @ 080d7e94 cdd9
LAB_080d7e96:
    ldr r0, DAT_080d7eec                     @ 080d7e96 1548
    adds r4,r7,r0    @ 080d7e98 3c18
    ldrb r2,[r4,#0x0]                        @ 080d7e9a 2278
    lsls r0,r2,#0x1d    @ 080d7e9c 5007
    lsrs r0,r0,#0x1f    @ 080d7e9e c00f
    movs r1,#0x1    @ 080d7ea0 0121
    eors r1,r0    @ 080d7ea2 4140
    lsls r1,r1,#0x2    @ 080d7ea4 8900
    movs r0,#0x5    @ 080d7ea6 0520
    rsbs r0,r0,#0    @ 080d7ea8 4042
    ands r0,r2    @ 080d7eaa 1040
    orrs r0,r1    @ 080d7eac 0843
    strb r0,[r4,#0x0]                        @ 080d7eae 2070
    lsls r0,r0,#0x1d    @ 080d7eb0 4007
    lsrs r0,r0,#0x1f    @ 080d7eb2 c00f
    bl render_pack_stat_byte_to_info_slot    @ 080d7eb4 fff752f9
    ldrb r4,[r4,#0x0]                        @ 080d7eb8 2478
    lsls r1,r4,#0x1d    @ 080d7eba 6107
    lsrs r1,r1,#0x1f    @ 080d7ebc c90f
    movs r0,#0x0    @ 080d7ebe 0020
    bl fill_pack_info_card_name_tiles        @ 080d7ec0 fff77cf9
    movs r0,#0x0    @ 080d7ec4 0020
    bl render_pack_card_sprite_by_flip_state @ 080d7ec6 fcf7effb
    movs r0,#0x0    @ 080d7eca 0020
    bl render_pack_info_card_presence_sprites @ 080d7ecc fff7dcf9
    movs r0,#0x1    @ 080d7ed0 0120
    bl render_pack_info_card_highlight_sprite @ 080d7ed2 fff7b7f9
    ldr r1, DAT_080d7ef0                     @ 080d7ed6 0649
    movs r0,#0x4    @ 080d7ed8 0420
    strh r0,[r1,#0x10]                       @ 080d7eda 0882
LAB_080d7edc:
    movs r0,#0x1    @ 080d7edc 0120
    pop {r3,r4}                              @ 080d7ede 18bc
    .hword 0x4698    @ 080d7ee0 9846
    .hword 0x46a1    @ 080d7ee2 a146
    pop {r4,r5,r6,r7}                        @ 080d7ee4 f0bc
    pop {r1}                                 @ 080d7ee6 02bc
    bx r1                                    @ 080d7ee8 0847
    .zero  0x2
DAT_080d7eec:
    .word  0x00000719                     @ 080d7eec 19070000
DAT_080d7ef0:
    .word  pack_ui_state                  @ 080d7ef0 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 9.
@ Calls render_pack_selection_label_to_bg_vram(0x140, 0x180) to render the label string to
@ BG VRAM. If render completes (returns 1): writes [+0x1a]:=1, [+0x18]:=1, sets next step=9;
@ otherwise sets next step=0xa. Unconditionally calls render_pack_card_sprite_by_flip_state(0),
@ render_pack_info_card_presence_sprites(0), render_pack_info_card_highlight_sprite(1).
@ Returns 1 (Sub-case E pop{r1};bx r1, movs r0,#1 @ 080d7f32 fixed).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080d7f18)
@ Returns: r0=u8 1 (step-complete flag)
@ Side effects:
@   [pack_ui_state+0xc+0x1a] := 1 (on render-complete path)
@   [pack_ui_state+0xc+0x18] := 1 (on render-complete path)
@   [pack_ui_state+0xc+0x4] := 9 or 0xa (step index)
@ Constants:
@   pack_ui_state = 0x03005850
@   LABEL_X = 0x140
@   LABEL_Y = 0x180
@   NEXT_STATE_DONE = 9
@   NEXT_STATE_CONT = 0xa
tick_pack_card_info_label_vram:
    push {r4,lr}                             @ 080d7ef4 10b5
    ldr r0, DAT_080d7f18                     @ 080d7ef6 0848
    adds r4,r0,#0x0    @ 080d7ef8 041c
    adds r4,#0xc    @ 080d7efa 0c34
    movs r0,#0xa0    @ 080d7efc a020
    lsls r0,r0,#0x1    @ 080d7efe 4000
    movs r1,#0xc0    @ 080d7f00 c021
    lsls r1,r1,#0x1    @ 080d7f02 4900
    bl render_pack_selection_label_to_bg_vram @ 080d7f04 04f0dafb
    adds r1,r0,#0x0    @ 080d7f08 011c
    cmp r1,#0x1                              @ 080d7f0a 0129
    bne LAB_080d7f1c                         @ 080d7f0c 06d1
    movs r0,#0x2    @ 080d7f0e 0220
    strh r0,[r4,#0x1a]                       @ 080d7f10 6083
    strh r1,[r4,#0x18]                       @ 080d7f12 2183
    movs r0,#0x9    @ 080d7f14 0920
    b LAB_080d7f1e                           @ 080d7f16 02e0
DAT_080d7f18:
    .word  pack_ui_state                  @ 080d7f18 50580003
LAB_080d7f1c:
    movs r0,#0xa    @ 080d7f1c 0a20
LAB_080d7f1e:
    strh r0,[r4,#0x4]                        @ 080d7f1e a080
    movs r0,#0x0    @ 080d7f20 0020
    bl render_pack_card_sprite_by_flip_state @ 080d7f22 fcf7c1fb
    movs r0,#0x0    @ 080d7f26 0020
    bl render_pack_info_card_presence_sprites @ 080d7f28 fff7aef9
    movs r0,#0x1    @ 080d7f2c 0120
    bl render_pack_info_card_highlight_sprite @ 080d7f2e fff789f9
    movs r0,#0x1    @ 080d7f32 0120
    pop {r4}                                 @ 080d7f34 10bc
    pop {r1}                                 @ 080d7f36 02bc
    bx r1                                    @ 080d7f38 0847
    .zero  0x2

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 0xa.
@ Per-frame handler for pack card info page input with scroll. Calls tick_overlay_animation_step(0)
@ to advance the overlay; reads gPrng+0x1d0 scene pointer [+0x1c] to confirm scene type=2.
@ Then checks gPrng+0x148 input bit-field: if bit1 (down) is set and direction [+0x18]=1,
@ initializes upward scroll (init_pack_scroll_animation, step=0xb); else sets step=0xc and calls
@ render_pack_info_label_sprites_and_palette. If bit0, determines scroll parameters based on
@ [+0x18] and bit5 (flip flag), sets step to 0xb/0xc/0xe/0x11 accordingly. Each branch calls
@ sync_state_and_init_sprite and clears [+0x724] bit. Unconditionally calls
@ render_pack_card_sprite_by_flip_state(0), render_pack_info_card_presence_sprites(0),
@ render_pack_info_card_highlight_sprite(1). Returns r6 (0=animation in progress, 1=advance needed).
@ 
@ Params: none (r0 immediately clobbered)
@ Returns: r0=u8 r6 (0=continue, 1=input handled; Sub-case E adds r0,r6 @ 080d80c4)
@ Side effects:
@   [pack_ui_state+0xc+0x4] := 0xb or 0xc or 0xe (step index)
@   [pack_ui_state+0xc+0x18] := 0 or 1 (direction flag)
@   [pack_ui_state+0x724] byte: bit5 cleared
@   [pack_ui_state+0x718] byte: bit5 set or cleared
@ Constants:
@   pack_ui_state = 0x03005850
@   INPUT_FIELD_OFFSET = 0x148
@   SCENE_TYPE_FIELD_OFFSET = 0x1d0
@   STATE_FLAGS_OFFSET = 0x724
@   SPRITE_CTRL_OFFSET = 0x718
@   SCROLL_Y = 0x98
tick_pack_card_info_input_with_scroll:
    push {r4,r5,r6,lr}                       @ 080d7f3c 70b5
    ldr r4, DAT_080d7f88                     @ 080d7f3e 124c
    adds r5,r4,#0x0    @ 080d7f40 251c
    adds r5,#0xc    @ 080d7f42 0c35
    movs r6,#0x0    @ 080d7f44 0026
    movs r0,#0x0    @ 080d7f46 0020
    bl tick_overlay_animation_step           @ 080d7f48 05f04cfb
    ldr r2, PTR_gPrng_080d7f8c               @ 080d7f4c 0f4a
    movs r1,#0xe8    @ 080d7f4e e821
    lsls r1,r1,#0x1    @ 080d7f50 4900
    adds r0,r2,r1    @ 080d7f52 5018
    ldr r0,[r0,#0x0]                         @ 080d7f54 0068
    ldrh r1,[r0,#0x1c]                       @ 080d7f56 818b
    cmp r1,#0x2                              @ 080d7f58 0229
    beq LAB_080d7f5e                         @ 080d7f5a 00d0
    b LAB_080d808c                           @ 080d7f5c 96e0
LAB_080d7f5e:
    movs r3,#0xa4    @ 080d7f5e a423
    lsls r3,r3,#0x1    @ 080d7f60 5b00
    adds r0,r2,r3    @ 080d7f62 d018
    ldrh r2,[r0,#0x0]                        @ 080d7f64 0288
    ands r1,r2    @ 080d7f66 1140
    cmp r1,#0x0                              @ 080d7f68 0029
    beq LAB_080d7fb6                         @ 080d7f6a 24d0
    ldrh r0,[r5,#0x18]                       @ 080d7f6c 288b
    cmp r0,#0x1                              @ 080d7f6e 0128
    bne LAB_080d7f90                         @ 080d7f70 0ed1
    strh r6,[r5,#0x18]                       @ 080d7f72 2e83
    movs r0,#0x0    @ 080d7f74 0020
    bl get_pack_slot_screen_y                @ 080d7f76 fff7b3f8
    movs r1,#0x98    @ 080d7f7a 9821
    movs r2,#0x8    @ 080d7f7c 0822
    bl init_pack_scroll_animation            @ 080d7f7e fcf703fd
    movs r0,#0xb    @ 080d7f82 0b20
    strh r0,[r5,#0x4]                        @ 080d7f84 a880
    b LAB_080d7f9c                           @ 080d7f86 09e0
DAT_080d7f88:
    .word  pack_ui_state                  @ 080d7f88 50580003
PTR_gPrng_080d7f8c:
    .word  gPrng                          @ 080d7f8c 40000003
LAB_080d7f90:
    movs r0,#0xc    @ 080d7f90 0c20
    strh r0,[r5,#0x4]                        @ 080d7f92 a880
    movs r0,#0x1    @ 080d7f94 0120
    strh r0,[r5,#0x18]                       @ 080d7f96 2883
    bl render_pack_info_label_sprites_and_palette @ 080d7f98 fff7d0f8
LAB_080d7f9c:
    movs r6,#0x1    @ 080d7f9c 0126
    movs r0,#0x1    @ 080d7f9e 0120
    bl sync_state_and_init_sprite            @ 080d7fa0 21f088fd
    movs r2,#0xe3    @ 080d7fa4 e322
    lsls r2,r2,#0x3    @ 080d7fa6 d200
    adds r1,r5,r2    @ 080d7fa8 a918
    movs r0,#0x21    @ 080d7faa 2120
    rsbs r0,r0,#0    @ 080d7fac 4042
    ldrb r3,[r1,#0x0]                        @ 080d7fae 0b78
    ands r0,r3    @ 080d7fb0 1840
    strb r0,[r1,#0x0]                        @ 080d7fb2 0870
    b LAB_080d808c                           @ 080d7fb4 6ae0
LAB_080d7fb6:
    movs r1,#0x1    @ 080d7fb6 0121
    adds r0,r1,#0x0    @ 080d7fb8 081c
    ands r0,r2    @ 080d7fba 1040
    cmp r0,#0x0                              @ 080d7fbc 0028
    beq LAB_080d800c                         @ 080d7fbe 25d0
    ldrh r0,[r5,#0x18]                       @ 080d7fc0 288b
    cmp r0,#0x0                              @ 080d7fc2 0028
    bne LAB_080d7fec                         @ 080d7fc4 12d1
    movs r0,#0xc    @ 080d7fc6 0c20
    strh r0,[r5,#0x4]                        @ 080d7fc8 a880
    strh r1,[r5,#0x18]                       @ 080d7fca 2983
    bl render_pack_info_label_sprites_and_palette @ 080d7fcc fff7b6f8
    movs r0,#0x1    @ 080d7fd0 0120
    bl sync_state_and_init_sprite            @ 080d7fd2 21f06ffd
    ldr r0, DAT_080d7fe8                     @ 080d7fd6 0448
    adds r1,r4,r0    @ 080d7fd8 2118
    movs r0,#0x21    @ 080d7fda 2120
    rsbs r0,r0,#0    @ 080d7fdc 4042
    ldrb r2,[r1,#0x0]                        @ 080d7fde 0a78
    ands r0,r2    @ 080d7fe0 1040
    strb r0,[r1,#0x0]                        @ 080d7fe2 0870
    movs r6,#0x1    @ 080d7fe4 0126
    b LAB_080d808c                           @ 080d7fe6 51e0
DAT_080d7fe8:
    .word  0x00000724                     @ 080d7fe8 24070000
LAB_080d7fec:
    cmp r0,#0x1                              @ 080d7fec 0128
    bne LAB_080d808c                         @ 080d7fee 4dd1
    movs r0,#0x24    @ 080d7ff0 2420
    bl sync_state_and_init_sprite            @ 080d7ff2 21f05ffd
    ldr r3, DAT_080d8008                     @ 080d7ff6 044b
    adds r0,r4,r3    @ 080d7ff8 e018
    movs r1,#0x21    @ 080d7ffa 2121
    rsbs r1,r1,#0    @ 080d7ffc 4942
    ldrb r2,[r0,#0x0]                        @ 080d7ffe 0278
    ands r1,r2    @ 080d8000 1140
    strb r1,[r0,#0x0]                        @ 080d8002 0170
    movs r0,#0xe    @ 080d8004 0e20
    b LAB_080d8064                           @ 080d8006 2de0
DAT_080d8008:
    .word  0x00000724                     @ 080d8008 24070000
LAB_080d800c:
    movs r0,#0x10    @ 080d800c 1020
    ands r0,r2    @ 080d800e 1040
    cmp r0,#0x0                              @ 080d8010 0028
    beq LAB_080d802c                         @ 080d8012 0bd0
    ldrh r0,[r5,#0x18]                       @ 080d8014 288b
    cmp r0,#0x0                              @ 080d8016 0028
    bne LAB_080d801e                         @ 080d8018 01d1
    adds r0,#0x1    @ 080d801a 0130
    b LAB_080d803e                           @ 080d801c 0fe0
LAB_080d801e:
    ldr r3, DAT_080d8028                     @ 080d801e 024b
    adds r4,r4,r3    @ 080d8020 e418
    movs r0,#0x20    @ 080d8022 2020
    b LAB_080d8076                           @ 080d8024 27e0
    .zero  0x2
DAT_080d8028:
    .word  0x00000724                     @ 080d8028 24070000
LAB_080d802c:
    movs r1,#0x20    @ 080d802c 2021
    adds r0,r1,#0x0    @ 080d802e 081c
    ands r0,r2    @ 080d8030 1040
    cmp r0,#0x0                              @ 080d8032 0028
    beq LAB_080d808c                         @ 080d8034 2ad0
    ldrh r0,[r5,#0x18]                       @ 080d8036 288b
    cmp r0,#0x0                              @ 080d8038 0028
    beq LAB_080d8070                         @ 080d803a 19d0
    subs r0,#0x1    @ 080d803c 0138
LAB_080d803e:
    strh r0,[r5,#0x18]                       @ 080d803e 2883
    ldrh r0,[r5,#0x18]                       @ 080d8040 288b
    bl get_pack_slot_screen_y                @ 080d8042 fff74df8
    movs r1,#0x98    @ 080d8046 9821
    movs r2,#0x8    @ 080d8048 0822
    bl init_pack_scroll_animation            @ 080d804a fcf79dfc
    movs r0,#0x0    @ 080d804e 0020
    bl sync_state_and_init_sprite            @ 080d8050 21f030fd
    ldr r3, DAT_080d806c                     @ 080d8054 054b
    adds r1,r4,r3    @ 080d8056 e118
    movs r0,#0x21    @ 080d8058 2120
    rsbs r0,r0,#0    @ 080d805a 4042
    ldrb r2,[r1,#0x0]                        @ 080d805c 0a78
    ands r0,r2    @ 080d805e 1040
    strb r0,[r1,#0x0]                        @ 080d8060 0870
    movs r0,#0xb    @ 080d8062 0b20
LAB_080d8064:
    strh r0,[r5,#0x4]                        @ 080d8064 a880
    movs r6,#0x1    @ 080d8066 0126
    b LAB_080d808c                           @ 080d8068 10e0
    .zero  0x2
DAT_080d806c:
    .word  0x00000724                     @ 080d806c 24070000
LAB_080d8070:
    ldr r3, DAT_080d80cc                     @ 080d8070 164b
    adds r4,r4,r3    @ 080d8072 e418
    adds r0,r1,#0x0    @ 080d8074 081c
LAB_080d8076:
    ldrb r1,[r4,#0x0]                        @ 080d8076 2178
    ands r0,r1    @ 080d8078 0840
    cmp r0,#0x0                              @ 080d807a 0028
    bne LAB_080d808c                         @ 080d807c 06d1
    movs r0,#0x2    @ 080d807e 0220
    bl sync_state_and_init_sprite            @ 080d8080 21f018fd
    movs r0,#0x20    @ 080d8084 2020
    ldrb r2,[r4,#0x0]                        @ 080d8086 2278
    orrs r0,r2    @ 080d8088 1043
    strb r0,[r4,#0x0]                        @ 080d808a 2070
LAB_080d808c:
    cmp r6,#0x1                              @ 080d808c 012e
    beq LAB_080d80a2                         @ 080d808e 08d0
    ldr r0, PTR_gPrng_080d80d0               @ 080d8090 0f48
    movs r3,#0xa3    @ 080d8092 a323
    lsls r3,r3,#0x1    @ 080d8094 5b00
    adds r1,r0,r3    @ 080d8096 c118
    movs r0,#0xf0    @ 080d8098 f020
    ldrh r1,[r1,#0x0]                        @ 080d809a 0988
    ands r0,r1    @ 080d809c 0840
    cmp r0,#0x0                              @ 080d809e 0028
    bne LAB_080d80b2                         @ 080d80a0 07d1
LAB_080d80a2:
    movs r0,#0xe3    @ 080d80a2 e320
    lsls r0,r0,#0x3    @ 080d80a4 c000
    adds r1,r5,r0    @ 080d80a6 2918
    movs r0,#0x21    @ 080d80a8 2120
    rsbs r0,r0,#0    @ 080d80aa 4042
    ldrb r2,[r1,#0x0]                        @ 080d80ac 0a78
    ands r0,r2    @ 080d80ae 1040
    strb r0,[r1,#0x0]                        @ 080d80b0 0870
LAB_080d80b2:
    movs r0,#0x0    @ 080d80b2 0020
    bl render_pack_card_sprite_by_flip_state @ 080d80b4 fcf7f8fa
    movs r0,#0x0    @ 080d80b8 0020
    bl render_pack_info_card_presence_sprites @ 080d80ba fff7e5f8
    movs r0,#0x1    @ 080d80be 0120
    bl render_pack_info_card_highlight_sprite @ 080d80c0 fff7c0f8
    adds r0,r6,#0x0    @ 080d80c4 301c
    pop {r4,r5,r6}                           @ 080d80c6 70bc
    pop {r1}                                 @ 080d80c8 02bc
    bx r1                                    @ 080d80ca 0847
DAT_080d80cc:
    .word  0x00000724                     @ 080d80cc 24070000
PTR_gPrng_080d80d0:
    .word  gPrng                          @ 080d80d0 40000003

@ Called during the pack card info page display phase by the frame driver to advance the overlay animation and perform a one-time scroll reset after animation completes. Calls tick_overlay_animation_step(1) to advance the overlay animation; if the animation completes this frame (returns 1), reads the current selected pack slot screen Y coordinate, calls init_pack_scroll_animation to initialize scroll to the target position (r1=0x98, r2=1), then loops blocking on tick_pack_scroll_interp_step until scroll completes, and writes pack_ui_state[+0x10]=4 to advance the state machine. Each frame calls render_pack_info_card_presence_sprites(0) and render_pack_info_card_highlight_sprite(1). Returns the result of tick_overlay_animation_step (0=animating, 1=complete; Sub-case E).
@ 
@ Constants:
@ - pack_ui_state base = 0x03005850
@ - SCROLL_TARGET_Y = 0x98 (movs r1,#0x98)
@ - SCROLL_MODE = 1 (movs r2,#0x1)
@ - NEXT_STATE = 4 (strh r0,[r1,#0x10] = 4)
tick_pack_card_info_overlay_scroll:
    push {r4,r5,lr}                          @ 080d80d4 30b5
    ldr r0, DAT_080d8118                     @ 080d80d6 1048
    adds r4,r0,#0x0    @ 080d80d8 041c
    adds r4,#0xc    @ 080d80da 0c34
    movs r0,#0x1    @ 080d80dc 0120
    bl tick_overlay_animation_step           @ 080d80de 05f081fa
    adds r5,r0,#0x0    @ 080d80e2 051c
    cmp r5,#0x1                              @ 080d80e4 012d
    bne LAB_080d8104                         @ 080d80e6 0dd1
    ldrh r0,[r4,#0x18]                       @ 080d80e8 208b
    bl get_pack_slot_screen_y                @ 080d80ea fef7f9ff
    movs r1,#0x98    @ 080d80ee 9821
    movs r2,#0x1    @ 080d80f0 0122
    bl init_pack_scroll_animation            @ 080d80f2 fcf749fc
LAB_080d80f6:
    bl tick_pack_scroll_interp_step          @ 080d80f6 fcf7e7fb
    cmp r0,#0x0                              @ 080d80fa 0028
    beq LAB_080d80f6                         @ 080d80fc fbd0
    ldr r1, DAT_080d8118                     @ 080d80fe 0649
    movs r0,#0x4    @ 080d8100 0420
    strh r0,[r1,#0x10]                       @ 080d8102 0882
LAB_080d8104:
    movs r0,#0x0    @ 080d8104 0020
    bl render_pack_info_card_presence_sprites @ 080d8106 fff7bff8
    movs r0,#0x1    @ 080d810a 0120
    bl render_pack_info_card_highlight_sprite @ 080d810c fff79af8
    adds r0,r5,#0x0    @ 080d8110 281c
    pop {r4,r5}                              @ 080d8112 30bc
    pop {r1}                                 @ 080d8114 02bc
    bx r1                                    @ 080d8116 0847
DAT_080d8118:
    .word  pack_ui_state                  @ 080d8118 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 0xb.
@ Per-frame handler that checks confirm-button input and advances the pack info page state.
@ Reads gPrng+0x1d0 scene pointer [+0x1c] to confirm scene type=2; checks gPrng+0x148 bit0
@ (confirm key). If confirm key is pressed: calls sync_state_and_init_sprite(0x24), writes
@ [+0x10]:=0xc to advance state machine, sets r4=1. Unconditionally calls
@ tick_overlay_animation_step(0), render_pack_card_sprite_by_flip_state(0),
@ render_pack_info_card_presence_sprites(0), render_pack_info_card_highlight_sprite(1).
@ Returns r4 (0=waiting for input, 1=confirmed; Sub-case E).
@ 
@ Params: none (r4 initialized to 0 internally via movs r4,#0)
@ Returns: r0=u8 (0=waiting, 1=confirmed; Sub-case E adds r0,r4 @ 080d8166)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 0xc (state-machine step, on confirm-key path)
@ Constants:
@   pack_ui_state = 0x03005850
@   INPUT_FIELD_OFFSET = 0x148
@   SCENE_TYPE_CHECK = 2
@   SPRITE_INIT_CODE = 0x24
@   NEXT_STATE = 0xc
tick_pack_card_info_confirm_input:
    push {r4,lr}                             @ 080d811c 10b5
    movs r4,#0x0    @ 080d811e 0024
    ldr r1, PTR_gPrng_080d8170               @ 080d8120 1349
    movs r2,#0xe8    @ 080d8122 e822
    lsls r2,r2,#0x1    @ 080d8124 5200
    adds r0,r1,r2    @ 080d8126 8818
    ldr r0,[r0,#0x0]                         @ 080d8128 0068
    ldrh r0,[r0,#0x1c]                       @ 080d812a 808b
    cmp r0,#0x2                              @ 080d812c 0228
    bne LAB_080d814e                         @ 080d812e 0ed1
    movs r0,#0xa4    @ 080d8130 a420
    lsls r0,r0,#0x1    @ 080d8132 4000
    adds r1,r1,r0    @ 080d8134 0918
    movs r0,#0x1    @ 080d8136 0120
    ldrh r1,[r1,#0x0]                        @ 080d8138 0988
    ands r0,r1    @ 080d813a 0840
    cmp r0,#0x0                              @ 080d813c 0028
    beq LAB_080d814e                         @ 080d813e 06d0
    movs r0,#0x24    @ 080d8140 2420
    bl sync_state_and_init_sprite            @ 080d8142 21f0b7fc
    ldr r1, DAT_080d8174                     @ 080d8146 0b49
    movs r0,#0xc    @ 080d8148 0c20
    strh r0,[r1,#0x10]                       @ 080d814a 0882
    movs r4,#0x1    @ 080d814c 0124
LAB_080d814e:
    movs r0,#0x0    @ 080d814e 0020
    bl tick_overlay_animation_step           @ 080d8150 05f048fa
    movs r0,#0x0    @ 080d8154 0020
    bl render_pack_card_sprite_by_flip_state @ 080d8156 fcf7a7fa
    movs r0,#0x0    @ 080d815a 0020
    bl render_pack_info_card_presence_sprites @ 080d815c fff794f8
    movs r0,#0x1    @ 080d8160 0120
    bl render_pack_info_card_highlight_sprite @ 080d8162 fff76ff8
    adds r0,r4,#0x0    @ 080d8166 201c
    pop {r4}                                 @ 080d8168 10bc
    pop {r1}                                 @ 080d816a 02bc
    bx r1                                    @ 080d816c 0847
    .zero  0x2
PTR_gPrng_080d8170:
    .word  gPrng                          @ 080d8170 40000003
DAT_080d8174:
    .word  pack_ui_state                  @ 080d8174 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 0xc.
@ Per-frame driver for the pack card info page scroll interpolation animation. Calls
@ tick_pack_scroll_interp_step (r4=return value) to execute one scroll interpolation step;
@ then calls tick_overlay_animation_step(0) to advance overlay animation; unconditionally calls
@ render_pack_card_sprite_by_flip_state(0), render_pack_info_card_presence_sprites(0),
@ render_pack_info_card_highlight_sprite(1). If scroll completes (r4==1): writes
@ [+0x10]:=9 to advance the state machine. Returns r4 (0=scrolling, 1=complete; Sub-case E).
@ 
@ Params: none (no APCS input)
@ Returns: r0=u8 (0=scrolling, 1=complete; Sub-case E adds r0,r4 @ 080d81a2)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 9 (on scroll-complete path)
@ Constants:
@   pack_ui_state = 0x03005850
@   NEXT_STATE = 9
tick_pack_card_info_scroll_interp:
    push {r4,lr}                             @ 080d8178 10b5
    bl tick_pack_scroll_interp_step          @ 080d817a fcf7a5fb
    adds r4,r0,#0x0    @ 080d817e 041c
    movs r0,#0x0    @ 080d8180 0020
    bl tick_overlay_animation_step           @ 080d8182 05f02ffa
    movs r0,#0x0    @ 080d8186 0020
    bl render_pack_card_sprite_by_flip_state @ 080d8188 fcf78efa
    movs r0,#0x0    @ 080d818c 0020
    bl render_pack_info_card_presence_sprites @ 080d818e fff77bf8
    movs r0,#0x1    @ 080d8192 0120
    bl render_pack_info_card_highlight_sprite @ 080d8194 fff756f8
    cmp r4,#0x1                              @ 080d8198 012c
    bne LAB_080d81a2                         @ 080d819a 02d1
    ldr r1, DAT_080d81ac                     @ 080d819c 0349
    movs r0,#0x9    @ 080d819e 0920
    strh r0,[r1,#0x10]                       @ 080d81a0 0882
LAB_080d81a2:
    adds r0,r4,#0x0    @ 080d81a2 201c
    pop {r4}                                 @ 080d81a4 10bc
    pop {r1}                                 @ 080d81a6 02bc
    bx r1                                    @ 080d81a8 0847
    .zero  0x2
DAT_080d81ac:
    .word  pack_ui_state                  @ 080d81ac 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 0xe.
@ Executes BG fade-in animation for the pack card info page (variant A: clears BG3 priority,
@ sets BG0/BG1/BG2 priorities 1/2/3). On first entry (pack_ui_state+0x724 bit1 not set):
@ clears BG3CNT low 2 bits, sets BG0CNT/BG1CNT/BG2CNT priorities 1/2/3, writes BLDCNT=0x1748,
@ BLDALPHA:=0x1000, sets frame counter [+0x6]:=0xa, sets bit1. Each frame decrements counter;
@ while counter>0: interpolates BLDALPHA linearly via bios_div(count*0x10/0xa); when counter<=0:
@ restores BG layer config, writes BLDCNT=0x3f3f, BLDALPHA=0x1010, syncs [+0x18]:=[+0x1c],
@ writes [+0x10]:=0xf to advance state machine. Calls render_pack_card_sprite_by_flip_state(1),
@ render_pack_info_card_presence_sprites(1), render_pack_info_card_highlight_sprite(2).
@ Returns r7 (0=fading, 1=complete; Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080d825c)
@ Returns: r0=u8 (0=fading, 1=complete; Sub-case E adds r0,r7 @ 080d830c)
@ Side effects:
@   [BG3CNT] (0x0400000e): cleared & 0xfffc
@   [BG0CNT] (0x04000008): cleared then |= 1
@   [BG1CNT] (0x0400000a): cleared then |= 2
@   [BG2CNT] (0x0400000c): cleared then |= 3
@   [BLDCNT] (0x04000050): := 0x1748 (init) or 0x3f3f (final)
@   [BLDALPHA] (0x04000052): linear interpolation each frame, final 0x1010
@   [DISPCNT] (0x04000000): |= 0x800 (OBJ tile 1D mapping)
@   [pack_ui_state+0xc+0x6] := 0xa (frame counter)
@   [pack_ui_state+0x724] |= 0x2 (init bit)
@   [pack_ui_state+0xc+0x18] := [+0x1c] (sync selected slot, on complete)
@   [pack_ui_state+0xc+0x10] := 0xf (state machine advance, on complete)
@   [pack_ui_state+0x718] byte &= ~0x3 (on complete)
@ Constants:
@   pack_ui_state = 0x03005850
@   STATE_FLAGS_OFFSET = 0x724
@   FADE_FRAMES = 0xa
@   DISPCNT = 0x04000000, OBJ_TILE_MAP_1D_BIT = 0x800
@   BG3CNT = 0x0400000e, BG0CNT = 0x04000008
@   BLDCNT = 0x04000050, BLDCNT_VAL_INIT = 0x1748, BLDCNT_VAL_FINAL = 0x3f3f
@   BLDALPHA = 0x04000052, BLDALPHA_INIT = 0x1000, BLDALPHA_FINAL = 0x1010
@   NEXT_STATE = 0xf, PRIORITY_MASK = 0xfffc
tick_pack_card_info_fadein_bg_a:
    push {r4,r5,r6,r7,lr}                    @ 080d81b0 f0b5
    ldr r0, DAT_080d825c                     @ 080d81b2 2a48
    adds r4,r0,#0x0    @ 080d81b4 041c
    adds r4,#0xc    @ 080d81b6 0c34
    movs r7,#0x0    @ 080d81b8 0027
    ldr r1, DAT_080d8260                     @ 080d81ba 2949
    adds r6,r0,r1    @ 080d81bc 4618
    ldrb r5,[r6,#0x0]                        @ 080d81be 3578
    movs r0,#0x2    @ 080d81c0 0220
    ands r0,r5    @ 080d81c2 2840
    cmp r0,#0x0                              @ 080d81c4 0028
    bne LAB_080d8228                         @ 080d81c6 2fd1
    ldr r1, PTR_BG3CNT_080d8264              @ 080d81c8 2649
    ldrh r2,[r1,#0x0]                        @ 080d81ca 0a88
    ldr r3, DAT_080d8268                     @ 080d81cc 264b
    adds r0,r3,#0x0    @ 080d81ce 181c
    ands r0,r2    @ 080d81d0 1040
    strh r0,[r1,#0x0]                        @ 080d81d2 0880
    ldrh r0,[r1,#0x0]                        @ 080d81d4 0888
    strh r0,[r1,#0x0]                        @ 080d81d6 0880
    ldr r2, PTR_BG0CNT_080d826c              @ 080d81d8 244a
    ldrh r1,[r2,#0x0]                        @ 080d81da 1188
    adds r0,r3,#0x0    @ 080d81dc 181c
    ands r0,r1    @ 080d81de 0840
    strh r0,[r2,#0x0]                        @ 080d81e0 1080
    ldrh r0,[r2,#0x0]                        @ 080d81e2 1088
    movs r1,#0x1    @ 080d81e4 0121
    orrs r0,r1    @ 080d81e6 0843
    strh r0,[r2,#0x0]                        @ 080d81e8 1080
    adds r2,#0x2    @ 080d81ea 0232
    ldrh r1,[r2,#0x0]                        @ 080d81ec 1188
    adds r0,r3,#0x0    @ 080d81ee 181c
    ands r0,r1    @ 080d81f0 0840
    strh r0,[r2,#0x0]                        @ 080d81f2 1080
    ldrh r0,[r2,#0x0]                        @ 080d81f4 1088
    movs r1,#0x2    @ 080d81f6 0221
    orrs r0,r1    @ 080d81f8 0843
    strh r0,[r2,#0x0]                        @ 080d81fa 1080
    adds r2,#0x2    @ 080d81fc 0232
    ldrh r0,[r2,#0x0]                        @ 080d81fe 1088
    ands r3,r0    @ 080d8200 0340
    strh r3,[r2,#0x0]                        @ 080d8202 1380
    ldrh r0,[r2,#0x0]                        @ 080d8204 1088
    movs r1,#0x3    @ 080d8206 0321
    orrs r0,r1    @ 080d8208 0843
    strh r0,[r2,#0x0]                        @ 080d820a 1080
    ldr r1, PTR_BLDCNT_080d8270              @ 080d820c 1849
    ldr r2, DAT_080d8274                     @ 080d820e 194a
    adds r0,r2,#0x0    @ 080d8210 101c
    strh r0,[r1,#0x0]                        @ 080d8212 0880
    adds r1,#0x2    @ 080d8214 0231
    movs r2,#0x80    @ 080d8216 8022
    lsls r2,r2,#0x5    @ 080d8218 5201
    adds r0,r2,#0x0    @ 080d821a 101c
    strh r0,[r1,#0x0]                        @ 080d821c 0880
    movs r0,#0xa    @ 080d821e 0a20
    strh r0,[r4,#0x6]                        @ 080d8220 e080
    movs r0,#0x2    @ 080d8222 0220
    orrs r0,r5    @ 080d8224 2843
    strb r0,[r6,#0x0]                        @ 080d8226 3070
LAB_080d8228:
    ldrh r0,[r4,#0x6]                        @ 080d8228 e088
    subs r0,#0x1    @ 080d822a 0138
    strh r0,[r4,#0x6]                        @ 080d822c e080
    lsls r0,r0,#0x10    @ 080d822e 0004
    asrs r0,r0,#0x10    @ 080d8230 0014
    cmp r0,#0x0                              @ 080d8232 0028
    bge LAB_080d8238                         @ 080d8234 00da
    movs r7,#0x1    @ 080d8236 0127
LAB_080d8238:
    cmp r0,#0x0                              @ 080d8238 0028
    ble LAB_080d827c                         @ 080d823a 1fdd
    movs r1,#0x6    @ 080d823c 0621
    ldrsh r0,[r4,r1]                         @ 080d823e 605e
    lsls r0,r0,#0x4    @ 080d8240 0001
    movs r1,#0xa    @ 080d8242 0a21
    bl bios_div                              @ 080d8244 36f0daf8
    ldr r2, PTR_BLDALPHA_080d8278            @ 080d8248 0b4a
    movs r1,#0x10    @ 080d824a 1021
    subs r1,r1,r0    @ 080d824c 091a
    lsls r1,r1,#0x18    @ 080d824e 0906
    lsrs r1,r1,#0x18    @ 080d8250 090e
    lsls r0,r0,#0x18    @ 080d8252 0006
    lsrs r0,r0,#0x10    @ 080d8254 000c
    orrs r1,r0    @ 080d8256 0143
    strh r1,[r2,#0x0]                        @ 080d8258 1180
    b LAB_080d82d8                           @ 080d825a 3de0
DAT_080d825c:
    .word  pack_ui_state                  @ 080d825c 50580003
DAT_080d8260:
    .word  0x00000724                     @ 080d8260 24070000
PTR_BG3CNT_080d8264:
    .word  BG3CNT                         @ 080d8264 0e000004
DAT_080d8268:
    .word  0x0000fffc                     @ 080d8268 fcff0000
PTR_BG0CNT_080d826c:
    .word  BG0CNT                         @ 080d826c 08000004
PTR_BLDCNT_080d8270:
    .word  BLDCNT                         @ 080d8270 50000004
DAT_080d8274:
    .word  0x00001748                     @ 080d8274 48170000
PTR_BLDALPHA_080d8278:
    .word  BLDALPHA                       @ 080d8278 52000004
LAB_080d827c:
    ldr r1, PTR_BG0CNT_080d8314              @ 080d827c 2549
    ldrh r2,[r1,#0x0]                        @ 080d827e 0a88
    ldr r3, DAT_080d8318                     @ 080d8280 254b
    adds r0,r3,#0x0    @ 080d8282 181c
    ands r0,r2    @ 080d8284 1040
    strh r0,[r1,#0x0]                        @ 080d8286 0880
    ldrh r0,[r1,#0x0]                        @ 080d8288 0888
    strh r0,[r1,#0x0]                        @ 080d828a 0880
    ldr r2, PTR_BG1CNT_080d831c              @ 080d828c 234a
    ldrh r1,[r2,#0x0]                        @ 080d828e 1188
    adds r0,r3,#0x0    @ 080d8290 181c
    ands r0,r1    @ 080d8292 0840
    strh r0,[r2,#0x0]                        @ 080d8294 1080
    ldrh r0,[r2,#0x0]                        @ 080d8296 1088
    movs r1,#0x1    @ 080d8298 0121
    orrs r0,r1    @ 080d829a 0843
    strh r0,[r2,#0x0]                        @ 080d829c 1080
    adds r2,#0x2    @ 080d829e 0232
    ldrh r1,[r2,#0x0]                        @ 080d82a0 1188
    adds r0,r3,#0x0    @ 080d82a2 181c
    ands r0,r1    @ 080d82a4 0840
    strh r0,[r2,#0x0]                        @ 080d82a6 1080
    ldrh r0,[r2,#0x0]                        @ 080d82a8 1088
    movs r1,#0x2    @ 080d82aa 0221
    orrs r0,r1    @ 080d82ac 0843
    strh r0,[r2,#0x0]                        @ 080d82ae 1080
    adds r2,#0x2    @ 080d82b0 0232
    ldrh r0,[r2,#0x0]                        @ 080d82b2 1088
    ands r3,r0    @ 080d82b4 0340
    strh r3,[r2,#0x0]                        @ 080d82b6 1380
    ldrh r0,[r2,#0x0]                        @ 080d82b8 1088
    movs r1,#0x3    @ 080d82ba 0321
    orrs r0,r1    @ 080d82bc 0843
    strh r0,[r2,#0x0]                        @ 080d82be 1080
    ldr r1, PTR_BLDCNT_080d8320              @ 080d82c0 1749
    ldr r2, DAT_080d8324                     @ 080d82c2 184a
    adds r0,r2,#0x0    @ 080d82c4 101c
    strh r0,[r1,#0x0]                        @ 080d82c6 0880
    adds r1,#0x2    @ 080d82c8 0231
    ldr r2, DAT_080d8328                     @ 080d82ca 174a
    adds r0,r2,#0x0    @ 080d82cc 101c
    strh r0,[r1,#0x0]                        @ 080d82ce 0880
    subs r1,#0x52    @ 080d82d0 5239
    movs r0,#0x80    @ 080d82d2 8020
    lsls r0,r0,#0x4    @ 080d82d4 0001
    strh r0,[r1,#0x0]                        @ 080d82d6 0880
LAB_080d82d8:
    cmp r7,#0x1                              @ 080d82d8 012f
    bne LAB_080d82fa                         @ 080d82da 0ed1
    movs r0,#0x0    @ 080d82dc 0020
    strh r0,[r4,#0x2]                        @ 080d82de 6080
    ldrh r0,[r4,#0x1c]                       @ 080d82e0 a08b
    strh r0,[r4,#0x18]                       @ 080d82e2 2083
    ldr r1, DAT_080d832c                     @ 080d82e4 1149
    movs r0,#0xf    @ 080d82e6 0f20
    strh r0,[r1,#0x10]                       @ 080d82e8 0882
    movs r0,#0xe3    @ 080d82ea e320
    lsls r0,r0,#0x3    @ 080d82ec c000
    adds r1,r4,r0    @ 080d82ee 2118
    movs r0,#0x3    @ 080d82f0 0320
    rsbs r0,r0,#0    @ 080d82f2 4042
    ldrb r2,[r1,#0x0]                        @ 080d82f4 0a78
    ands r0,r2    @ 080d82f6 1040
    strb r0,[r1,#0x0]                        @ 080d82f8 0870
LAB_080d82fa:
    movs r0,#0x1    @ 080d82fa 0120
    bl render_pack_card_sprite_by_flip_state @ 080d82fc fcf7d4f9
    movs r0,#0x1    @ 080d8300 0120
    bl render_pack_info_card_presence_sprites @ 080d8302 fef7c1ff
    movs r0,#0x2    @ 080d8306 0220
    bl render_pack_info_card_highlight_sprite @ 080d8308 fef79cff
    adds r0,r7,#0x0    @ 080d830c 381c
    pop {r4,r5,r6,r7}                        @ 080d830e f0bc
    pop {r1}                                 @ 080d8310 02bc
    bx r1                                    @ 080d8312 0847
PTR_BG0CNT_080d8314:
    .word  BG0CNT                         @ 080d8314 08000004
DAT_080d8318:
    .word  0x0000fffc                     @ 080d8318 fcff0000
PTR_BG1CNT_080d831c:
    .word  BG1CNT                         @ 080d831c 0a000004
PTR_BLDCNT_080d8320:
    .word  BLDCNT                         @ 080d8320 50000004
DAT_080d8324:
    .word  0x00003f3f                     @ 080d8324 3f3f0000
DAT_080d8328:
    .word  0x00001010                     @ 080d8328 10100000
DAT_080d832c:
    .word  pack_ui_state                  @ 080d832c 50580003

@ Called via step-table dispatch from tick_pack_card_select_step (0x080d8504), step index 0xf.
@ Executes BG fade-in animation for the pack card info page (variant B: structurally symmetric
@ with tick_pack_card_info_fadein_bg_a, but on completion also reads card id from current slot
@ entry [entry+0x0] and writes it to [+0x20]). On first entry (pack_ui_state+0x724 bit1 not set):
@ clears BG3CNT low 2 bits, sets BG0CNT/BG1CNT/BG2CNT priorities 1/2/3, writes BLDCNT=0x1748,
@ BLDALPHA:=0x1000, sets frame counter [+0x6]:=0xa, sets bit1. Each frame decrements counter;
@ while counter>0: interpolates BLDALPHA linearly via bios_div; when counter<=0: restores BG
@ config, writes BLDCNT=0x3f3f, BLDALPHA=0x1010. On complete: reads card id from current slot
@ entry base+[+0x0], writes [+0x20]:=card_id, [+0x2]:=2, [+0x10]:=0xf. Calls
@ render_pack_card_sprite_by_flip_state(1), render_pack_info_card_presence_sprites(1),
@ render_pack_info_card_highlight_sprite(2). Returns r7 (Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080d83dc)
@ Returns: r0=u8 (0=fading, 1=complete; Sub-case E adds r0,r7 @ 080d8492)
@ Side effects:
@   [BG3CNT] (0x0400000e): cleared & 0xfffc
@   [BG0CNT/BG1CNT/BG2CNT]: cleared then |= 1/2/3
@   [BLDCNT] (0x04000050): := 0x1748 (init) or 0x3f3f (final)
@   [BLDALPHA] (0x04000052): linear interpolation each frame, final 0x1010
@   [DISPCNT] (0x04000000): |= 0x800
@   [pack_ui_state+0xc+0x6] := 0xa
@   [pack_ui_state+0x724] |= 0x2
@   [pack_ui_state+0xc+0x20] := card_id from slot entry (on complete)
@   [pack_ui_state+0xc+0x2] := 2 (on complete)
@   [pack_ui_state+0xc+0x10] := 0xf (on complete)
@   [pack_ui_state+0x718] byte &= ~0xd (on complete)
@ Constants:
@   pack_ui_state = 0x03005850
@   STATE_FLAGS_OFFSET = 0x724
@   FADE_FRAMES = 0xa
@   BLDCNT_VAL_INIT = 0x1748, BLDCNT_VAL_FINAL = 0x3f3f
@   BLDALPHA_INIT = 0x1000, BLDALPHA_FINAL = 0x1010
@   NEXT_STATE = 0xf
@   SLOT_ENTRY_STRIDE = 0x20, SLOT_ENTRY_BASE_OFF = 0x44
tick_pack_card_info_fadein_bg_b:
    push {r4,r5,r6,r7,lr}                    @ 080d8330 f0b5
    ldr r0, DAT_080d83dc                     @ 080d8332 2a48
    adds r4,r0,#0x0    @ 080d8334 041c
    adds r4,#0xc    @ 080d8336 0c34
    movs r7,#0x0    @ 080d8338 0027
    ldr r1, DAT_080d83e0                     @ 080d833a 2949
    adds r6,r0,r1    @ 080d833c 4618
    ldrb r5,[r6,#0x0]                        @ 080d833e 3578
    movs r0,#0x2    @ 080d8340 0220
    ands r0,r5    @ 080d8342 2840
    cmp r0,#0x0                              @ 080d8344 0028
    bne LAB_080d83a8                         @ 080d8346 2fd1
    ldr r1, PTR_BG3CNT_080d83e4              @ 080d8348 2649
    ldrh r2,[r1,#0x0]                        @ 080d834a 0a88
    ldr r3, DAT_080d83e8                     @ 080d834c 264b
    adds r0,r3,#0x0    @ 080d834e 181c
    ands r0,r2    @ 080d8350 1040
    strh r0,[r1,#0x0]                        @ 080d8352 0880
    ldrh r0,[r1,#0x0]                        @ 080d8354 0888
    strh r0,[r1,#0x0]                        @ 080d8356 0880
    ldr r2, PTR_BG0CNT_080d83ec              @ 080d8358 244a
    ldrh r1,[r2,#0x0]                        @ 080d835a 1188
    adds r0,r3,#0x0    @ 080d835c 181c
    ands r0,r1    @ 080d835e 0840
    strh r0,[r2,#0x0]                        @ 080d8360 1080
    ldrh r0,[r2,#0x0]                        @ 080d8362 1088
    movs r1,#0x1    @ 080d8364 0121
    orrs r0,r1    @ 080d8366 0843
    strh r0,[r2,#0x0]                        @ 080d8368 1080
    adds r2,#0x2    @ 080d836a 0232
    ldrh r1,[r2,#0x0]                        @ 080d836c 1188
    adds r0,r3,#0x0    @ 080d836e 181c
    ands r0,r1    @ 080d8370 0840
    strh r0,[r2,#0x0]                        @ 080d8372 1080
    ldrh r0,[r2,#0x0]                        @ 080d8374 1088
    movs r1,#0x2    @ 080d8376 0221
    orrs r0,r1    @ 080d8378 0843
    strh r0,[r2,#0x0]                        @ 080d837a 1080
    adds r2,#0x2    @ 080d837c 0232
    ldrh r0,[r2,#0x0]                        @ 080d837e 1088
    ands r3,r0    @ 080d8380 0340
    strh r3,[r2,#0x0]                        @ 080d8382 1380
    ldrh r0,[r2,#0x0]                        @ 080d8384 1088
    movs r1,#0x3    @ 080d8386 0321
    orrs r0,r1    @ 080d8388 0843
    strh r0,[r2,#0x0]                        @ 080d838a 1080
    ldr r1, PTR_BLDCNT_080d83f0              @ 080d838c 1849
    ldr r2, DAT_080d83f4                     @ 080d838e 194a
    adds r0,r2,#0x0    @ 080d8390 101c
    strh r0,[r1,#0x0]                        @ 080d8392 0880
    adds r1,#0x2    @ 080d8394 0231
    movs r2,#0x80    @ 080d8396 8022
    lsls r2,r2,#0x5    @ 080d8398 5201
    adds r0,r2,#0x0    @ 080d839a 101c
    strh r0,[r1,#0x0]                        @ 080d839c 0880
    movs r0,#0xa    @ 080d839e 0a20
    strh r0,[r4,#0x6]                        @ 080d83a0 e080
    movs r0,#0x2    @ 080d83a2 0220
    orrs r0,r5    @ 080d83a4 2843
    strb r0,[r6,#0x0]                        @ 080d83a6 3070
LAB_080d83a8:
    ldrh r0,[r4,#0x6]                        @ 080d83a8 e088
    subs r0,#0x1    @ 080d83aa 0138
    strh r0,[r4,#0x6]                        @ 080d83ac e080
    lsls r0,r0,#0x10    @ 080d83ae 0004
    asrs r0,r0,#0x10    @ 080d83b0 0014
    cmp r0,#0x0                              @ 080d83b2 0028
    bge LAB_080d83b8                         @ 080d83b4 00da
    movs r7,#0x1    @ 080d83b6 0127
LAB_080d83b8:
    cmp r0,#0x0                              @ 080d83b8 0028
    ble LAB_080d83fc                         @ 080d83ba 1fdd
    movs r1,#0x6    @ 080d83bc 0621
    ldrsh r0,[r4,r1]                         @ 080d83be 605e
    lsls r0,r0,#0x4    @ 080d83c0 0001
    movs r1,#0xa    @ 080d83c2 0a21
    bl bios_div                              @ 080d83c4 36f01af8
    ldr r2, PTR_BLDALPHA_080d83f8            @ 080d83c8 0b4a
    movs r1,#0x10    @ 080d83ca 1021
    subs r1,r1,r0    @ 080d83cc 091a
    lsls r1,r1,#0x18    @ 080d83ce 0906
    lsrs r1,r1,#0x18    @ 080d83d0 090e
    lsls r0,r0,#0x18    @ 080d83d2 0006
    lsrs r0,r0,#0x10    @ 080d83d4 000c
    orrs r1,r0    @ 080d83d6 0143
    strh r1,[r2,#0x0]                        @ 080d83d8 1180
    b LAB_080d8458                           @ 080d83da 3de0
DAT_080d83dc:
    .word  pack_ui_state                  @ 080d83dc 50580003
DAT_080d83e0:
    .word  0x00000724                     @ 080d83e0 24070000
PTR_BG3CNT_080d83e4:
    .word  BG3CNT                         @ 080d83e4 0e000004
DAT_080d83e8:
    .word  0x0000fffc                     @ 080d83e8 fcff0000
PTR_BG0CNT_080d83ec:
    .word  BG0CNT                         @ 080d83ec 08000004
PTR_BLDCNT_080d83f0:
    .word  BLDCNT                         @ 080d83f0 50000004
DAT_080d83f4:
    .word  0x00001748                     @ 080d83f4 48170000
PTR_BLDALPHA_080d83f8:
    .word  BLDALPHA                       @ 080d83f8 52000004
LAB_080d83fc:
    ldr r1, PTR_BG0CNT_080d849c              @ 080d83fc 2749
    ldrh r2,[r1,#0x0]                        @ 080d83fe 0a88
    ldr r3, DAT_080d84a0                     @ 080d8400 274b
    adds r0,r3,#0x0    @ 080d8402 181c
    ands r0,r2    @ 080d8404 1040
    strh r0,[r1,#0x0]                        @ 080d8406 0880
    ldrh r0,[r1,#0x0]                        @ 080d8408 0888
    strh r0,[r1,#0x0]                        @ 080d840a 0880
    ldr r2, PTR_BG1CNT_080d84a4              @ 080d840c 254a
    ldrh r1,[r2,#0x0]                        @ 080d840e 1188
    adds r0,r3,#0x0    @ 080d8410 181c
    ands r0,r1    @ 080d8412 0840
    strh r0,[r2,#0x0]                        @ 080d8414 1080
    ldrh r0,[r2,#0x0]                        @ 080d8416 1088
    movs r1,#0x1    @ 080d8418 0121
    orrs r0,r1    @ 080d841a 0843
    strh r0,[r2,#0x0]                        @ 080d841c 1080
    adds r2,#0x2    @ 080d841e 0232
    ldrh r1,[r2,#0x0]                        @ 080d8420 1188
    adds r0,r3,#0x0    @ 080d8422 181c
    ands r0,r1    @ 080d8424 0840
    strh r0,[r2,#0x0]                        @ 080d8426 1080
    ldrh r0,[r2,#0x0]                        @ 080d8428 1088
    movs r1,#0x2    @ 080d842a 0221
    orrs r0,r1    @ 080d842c 0843
    strh r0,[r2,#0x0]                        @ 080d842e 1080
    adds r2,#0x2    @ 080d8430 0232
    ldrh r0,[r2,#0x0]                        @ 080d8432 1088
    ands r3,r0    @ 080d8434 0340
    strh r3,[r2,#0x0]                        @ 080d8436 1380
    ldrh r0,[r2,#0x0]                        @ 080d8438 1088
    movs r1,#0x3    @ 080d843a 0321
    orrs r0,r1    @ 080d843c 0843
    strh r0,[r2,#0x0]                        @ 080d843e 1080
    ldr r1, PTR_BLDCNT_080d84a8              @ 080d8440 1949
    ldr r2, DAT_080d84ac                     @ 080d8442 1a4a
    adds r0,r2,#0x0    @ 080d8444 101c
    strh r0,[r1,#0x0]                        @ 080d8446 0880
    adds r1,#0x2    @ 080d8448 0231
    ldr r2, DAT_080d84b0                     @ 080d844a 194a
    adds r0,r2,#0x0    @ 080d844c 101c
    strh r0,[r1,#0x0]                        @ 080d844e 0880
    subs r1,#0x52    @ 080d8450 5239
    movs r0,#0x80    @ 080d8452 8020
    lsls r0,r0,#0x4    @ 080d8454 0001
    strh r0,[r1,#0x0]                        @ 080d8456 0880
LAB_080d8458:
    cmp r7,#0x1                              @ 080d8458 012f
    bne LAB_080d8480                         @ 080d845a 11d1
    ldrh r1,[r4,#0x32]                       @ 080d845c 618e
    lsls r0,r1,#0x5    @ 080d845e 4801
    adds r0,#0x44    @ 080d8460 4430
    adds r0,r4,r0    @ 080d8462 2018
    ldrh r0,[r0,#0x0]                        @ 080d8464 0088
    strh r0,[r4,#0x20]                       @ 080d8466 2084
    movs r0,#0x2    @ 080d8468 0220
    strh r0,[r4,#0x2]                        @ 080d846a 6080
    ldr r1, DAT_080d84b4                     @ 080d846c 1149
    movs r0,#0xf    @ 080d846e 0f20
    strh r0,[r1,#0x10]                       @ 080d8470 0882
    movs r2,#0xe3    @ 080d8472 e322
    lsls r2,r2,#0x3    @ 080d8474 d200
    adds r1,r4,r2    @ 080d8476 a118
    subs r0,#0x12    @ 080d8478 1238
    ldrb r2,[r1,#0x0]                        @ 080d847a 0a78
    ands r0,r2    @ 080d847c 1040
    strb r0,[r1,#0x0]                        @ 080d847e 0870
LAB_080d8480:
    movs r0,#0x1    @ 080d8480 0120
    bl render_pack_card_sprite_by_flip_state @ 080d8482 fcf711f9
    movs r0,#0x1    @ 080d8486 0120
    bl render_pack_info_card_presence_sprites @ 080d8488 fef7fefe
    movs r0,#0x2    @ 080d848c 0220
    bl render_pack_info_card_highlight_sprite @ 080d848e fef7d9fe
    adds r0,r7,#0x0    @ 080d8492 381c
    pop {r4,r5,r6,r7}                        @ 080d8494 f0bc
    pop {r1}                                 @ 080d8496 02bc
    bx r1                                    @ 080d8498 0847
    .zero  0x2
PTR_BG0CNT_080d849c:
    .word  BG0CNT                         @ 080d849c 08000004
DAT_080d84a0:
    .word  0x0000fffc                     @ 080d84a0 fcff0000
PTR_BG1CNT_080d84a4:
    .word  BG1CNT                         @ 080d84a4 0a000004
PTR_BLDCNT_080d84a8:
    .word  BLDCNT                         @ 080d84a8 50000004
DAT_080d84ac:
    .word  0x00003f3f                     @ 080d84ac 3f3f0000
DAT_080d84b0:
    .word  0x00001010                     @ 080d84b0 10100000
DAT_080d84b4:
    .word  pack_ui_state                  @ 080d84b4 50580003

@ pack scene frame delay countdown. Reads pack_ui_state+0x724 byte checking bit1 (init flag): if not set (first call), writes [pack_ui_state+0xc+0x6] := 5 (counter initial value) and sets bit1 (marks initialized). Each call decrements counter [+0xc+0x6]; when it reaches <= 0, clears [+0x724] bit1 (resets init flag) and returns r0=1 (delay expired). Returns r0=0 while still counting down.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - DELAY_COUNTER_OFFSET = 0x12 (= 0xc + 0x6; counter field s16)
@ - FLAG_BYTE_OFFSET = 0x724 (init/run state flag byte)
@ - FLAG_BIT1 = 0x2 (init complete flag bit)
@ - INITIAL_COUNT = 5 (delay frame count)
tick_pack_frame_delay_counter:
    push {r4,lr}                             @ 080d84b8 10b5
    ldr r0, DAT_080d84fc                     @ 080d84ba 1048
    adds r2,r0,#0x0    @ 080d84bc 021c
    adds r2,#0xc    @ 080d84be 0c32
    movs r4,#0x0    @ 080d84c0 0024
    ldr r1, DAT_080d8500                     @ 080d84c2 0f49
    adds r3,r0,r1    @ 080d84c4 4318
    ldrb r1,[r3,#0x0]                        @ 080d84c6 1978
    movs r0,#0x2    @ 080d84c8 0220
    ands r0,r1    @ 080d84ca 0840
    cmp r0,#0x0                              @ 080d84cc 0028
    bne LAB_080d84da                         @ 080d84ce 04d1
    movs r0,#0x5    @ 080d84d0 0520
    strh r0,[r2,#0x6]                        @ 080d84d2 d080
    movs r0,#0x2    @ 080d84d4 0220
    orrs r0,r1    @ 080d84d6 0843
    strb r0,[r3,#0x0]                        @ 080d84d8 1870
LAB_080d84da:
    ldrh r0,[r2,#0x6]                        @ 080d84da d088
    subs r0,#0x1    @ 080d84dc 0138
    strh r0,[r2,#0x6]                        @ 080d84de d080
    lsls r0,r0,#0x10    @ 080d84e0 0004
    cmp r0,#0x0                              @ 080d84e2 0028
    bgt LAB_080d84f2                         @ 080d84e4 05dc
    movs r0,#0x3    @ 080d84e6 0320
    rsbs r0,r0,#0    @ 080d84e8 4042
    ldrb r1,[r3,#0x0]                        @ 080d84ea 1978
    ands r0,r1    @ 080d84ec 0840
    strb r0,[r3,#0x0]                        @ 080d84ee 1870
    movs r4,#0x1    @ 080d84f0 0124
LAB_080d84f2:
    adds r0,r4,#0x0    @ 080d84f2 201c
    pop {r4}                                 @ 080d84f4 10bc
    pop {r1}                                 @ 080d84f6 02bc
    bx r1                                    @ 080d84f8 0847
    .zero  0x2
DAT_080d84fc:
    .word  pack_ui_state                  @ 080d84fc 50580003
DAT_080d8500:
    .word  0x00000724                     @ 080d8500 24070000

@ Pack purchase screen card-select scene frame-step driver. Calls handler from fn-ptr table 0x09e49438 at current step index stored in pack_ui_state+0xc[+0x4] via invoke_r0. If handler returns nonzero, increments step counter. Returns 0 while scene is running, returns 1 when current step completes.
@ 
@ Constants:
@ - FN_TABLE=0x09e49438 // pack card select step handler fn-ptr table
@ - pack_ui_state=0x03005850
tick_pack_card_select_step:
    push {r4,lr}                             @ 080d8504 10b5
    ldr r0, DAT_080d852c                     @ 080d8506 0948
    adds r4,r0,#0x0    @ 080d8508 041c
    adds r4,#0xc    @ 080d850a 0c34
    ldr r1, DAT_080d8530                     @ 080d850c 0849
    ldrh r2,[r4,#0x4]                        @ 080d850e a288
    lsls r0,r2,#0x2    @ 080d8510 9000
    adds r0,r0,r1    @ 080d8512 4018
    ldr r0,[r0,#0x0]                         @ 080d8514 0068
    cmp r0,#0x0                              @ 080d8516 0028
    beq LAB_080d8534                         @ 080d8518 0cd0
    bl invoke_r0                             @ 080d851a 36f055f8
    cmp r0,#0x0                              @ 080d851e 0028
    beq LAB_080d8528                         @ 080d8520 02d0
    ldrh r0,[r4,#0x4]                        @ 080d8522 a088
    adds r0,#0x1    @ 080d8524 0130
    strh r0,[r4,#0x4]                        @ 080d8526 a080
LAB_080d8528:
    movs r0,#0x0    @ 080d8528 0020
    b LAB_080d8536                           @ 080d852a 04e0
DAT_080d852c:
    .word  pack_ui_state                  @ 080d852c 50580003
DAT_080d8530:
    .word  0x09e49438                     @ 080d8530 3894e409
LAB_080d8534:
    movs r0,#0x1    @ 080d8534 0120
LAB_080d8536:
    pop {r4}                                 @ 080d8536 10bc
    pop {r1}                                 @ 080d8538 02bc
    bx r1                                    @ 080d853a 0847

@ Pack scene card-select slot builder. r0=pack_index, r1=card_count, r2=card_mask_word, r3=player_cards_ptr. Reads pack_info_table for the pack's card list base, iterates each card, checks unlock status via check_pack_card_slot_filter or unlock bitmap, writes card_id/rarity/unlock_flag packed dword into EWRAM slot array at 0x0200af20. Returns r0=number of valid slots written.
@ 
@ Constants:
@ - SLOT_ARRAY=0x0200af20 // EWRAM card-select slot array base
@ - UNLOCK_BITS=0x02000006 // IWRAM card unlock bitmap base
@ - MAX_PACK_ID=0x32 // max pack ID (from DAT_080d86fc ldrh)
@ - CARD_LOW4_CLEAR_MASK=0x0000fff0 // clears low 4 bits (keeps [15:4])
build_pack_card_select_slot_data:
    push {r4,r5,r6,r7,lr}                    @ 080d853c f0b5
    .hword 0x4657    @ 080d853e 5746
    .hword 0x464e    @ 080d8540 4e46
    .hword 0x4645    @ 080d8542 4546
    push {r5,r6,r7}                          @ 080d8544 e0b4
    sub sp,#0x4                              @ 080d8546 81b0
    adds r7,r0,#0x0    @ 080d8548 071c
    .hword 0x4689    @ 080d854a 8946
    ldr r0, PTR_pack_info_table_080d8588     @ 080d854c 0e48
    lsls r1,r7,#0x4    @ 080d854e 3901
    adds r0,#0xc    @ 080d8550 0c30
    adds r1,r1,r0    @ 080d8552 0918
    ldr r6,[r1,#0x0]                         @ 080d8554 0e68
    adds r0,r7,#0x0    @ 080d8556 381c
    bl get_pack_total_card_count             @ 080d8558 02f090fc
    lsls r0,r0,#0x10    @ 080d855c 0004
    lsrs r0,r0,#0x10    @ 080d855e 000c
    .hword 0x4680    @ 080d8560 8046
    movs r3,#0x0    @ 080d8562 0023
    ldr r4, DAT_080d858c                     @ 080d8564 094c
    cmp r6,#0x0                              @ 080d8566 002e
    beq LAB_080d8618                         @ 080d8568 56d0
    movs r5,#0x0    @ 080d856a 0025
    cmp r3,r8                                @ 080d856c 4345
    bcc LAB_080d8572                         @ 080d856e 00d3
    b LAB_080d86ea                           @ 080d8570 bbe0
LAB_080d8572:
    movs r0,#0x1    @ 080d8572 0120
    .hword 0x4682    @ 080d8574 8246
    movs r7,#0xf    @ 080d8576 0f27
LAB_080d8578:
    movs r0,#0x1c    @ 080d8578 1c20
    ldrb r1,[r6,#0x2]                        @ 080d857a b178
    ands r0,r1    @ 080d857c 0840
    cmp r0,#0x0                              @ 080d857e 0028
    bne LAB_080d8590                         @ 080d8580 06d1
    movs r1,#0x0    @ 080d8582 0021
    b LAB_080d859a                           @ 080d8584 09e0
    .zero  0x2
PTR_pack_info_table_080d8588:
    .word  pack_info_table                @ 080d8588 e8e2e509
DAT_080d858c:
    .word  0x0200af20                     @ 080d858c 20af0002
LAB_080d8590:
    ldr r0,[r6,#0x0]                         @ 080d8590 3068
    lsls r0,r0,#0xb    @ 080d8592 c002
    lsrs r0,r0,#0x1d    @ 080d8594 400f
    movs r1,#0x5    @ 080d8596 0521
    subs r1,r1,r0    @ 080d8598 091a
LAB_080d859a:
    .hword 0x4650    @ 080d859a 5046
    lsls r0,r1    @ 080d859c 8840
    .hword 0x464a    @ 080d859e 4a46
    ands r0,r2    @ 080d85a0 1040
    cmp r0,#0x0                              @ 080d85a2 0028
    beq LAB_080d8608                         @ 080d85a4 30d0
    movs r0,#0x7    @ 080d85a6 0720
    ands r1,r0    @ 080d85a8 0140
    movs r2,#0x8    @ 080d85aa 0822
    rsbs r2,r2,#0    @ 080d85ac 5242
    adds r0,r2,#0x0    @ 080d85ae 101c
    ldrb r2,[r4,#0x0]                        @ 080d85b0 2278
    ands r0,r2    @ 080d85b2 1040
    orrs r0,r1    @ 080d85b4 0843
    strb r0,[r4,#0x0]                        @ 080d85b6 2070
    ldrh r0,[r6,#0x0]                        @ 080d85b8 3088
    str r3,[sp,#0x0]                         @ 080d85ba 0093
    bl internal_card_id_to_card_id           @ 080d85bc 16f0d6f8
    movs r1,#0x3    @ 080d85c0 0321
    ldrh r2,[r6,#0x2]                        @ 080d85c2 7288
    ands r1,r2    @ 080d85c4 1140
    adds r0,r0,r1    @ 080d85c6 4018
    lsls r0,r0,#0x4    @ 080d85c8 0001
    adds r1,r7,#0x0    @ 080d85ca 391c
    ldrh r2,[r4,#0x0]                        @ 080d85cc 2288
    ands r1,r2    @ 080d85ce 1140
    orrs r1,r0    @ 080d85d0 0143
    strh r1,[r4,#0x0]                        @ 080d85d2 2180
    movs r2,#0x0    @ 080d85d4 0022
    ldr r1,[r4,#0x0]                         @ 080d85d6 2168
    lsls r1,r1,#0x10    @ 080d85d8 0904
    lsrs r1,r1,#0x14    @ 080d85da 090d
    lsls r1,r1,#0x1    @ 080d85dc 4900
    ldr r0, DAT_080d8614                     @ 080d85de 0d48
    adds r1,r1,r0    @ 080d85e0 0918
    adds r0,r7,#0x0    @ 080d85e2 381c
    ldrb r1,[r1,#0x0]                        @ 080d85e4 0978
    ands r0,r1    @ 080d85e6 0840
    ldr r3,[sp,#0x0]                         @ 080d85e8 009b
    cmp r0,#0x0                              @ 080d85ea 0028
    bne LAB_080d85f0                         @ 080d85ec 00d1
    movs r2,#0x1    @ 080d85ee 0122
LAB_080d85f0:
    .hword 0x4651    @ 080d85f0 5146
    ands r1,r2    @ 080d85f2 1140
    lsls r1,r1,#0x3    @ 080d85f4 c900
    movs r2,#0x9    @ 080d85f6 0922
    rsbs r2,r2,#0    @ 080d85f8 5242
    adds r0,r2,#0x0    @ 080d85fa 101c
    ldrb r2,[r4,#0x0]                        @ 080d85fc 2278
    ands r0,r2    @ 080d85fe 1040
    orrs r0,r1    @ 080d8600 0843
    strb r0,[r4,#0x0]                        @ 080d8602 2070
    adds r4,#0x4    @ 080d8604 0434
    adds r3,#0x1    @ 080d8606 0133
LAB_080d8608:
    adds r6,#0x4    @ 080d8608 0436
    adds r5,#0x1    @ 080d860a 0135
    cmp r5,r8                                @ 080d860c 4545
    bcc LAB_080d8578                         @ 080d860e b3d3
    b LAB_080d86ea                           @ 080d8610 6be0
    .zero  0x2
DAT_080d8614:
    .word  0x02000006                     @ 080d8614 06000002
LAB_080d8618:
    .hword 0x4648    @ 080d8618 4846
    cmp r0,#0x1                              @ 080d861a 0128
    bne LAB_080d8690                         @ 080d861c 38d1
    movs r5,#0x1    @ 080d861e 0125
    ldr r0, DAT_080d8688                     @ 080d8620 1948
    ldrh r0,[r0,#0x0]                        @ 080d8622 0088
    cmp r5,r0                                @ 080d8624 8542
    bhi LAB_080d86ea                         @ 080d8626 60d8
    movs r6,#0xf    @ 080d8628 0f26
LAB_080d862a:
    adds r0,r5,#0x0    @ 080d862a 281c
    adds r1,r7,#0x0    @ 080d862c 391c
    str r3,[sp,#0x0]                         @ 080d862e 0093
    bl check_pack_card_slot_filter           @ 080d8630 02f058fc
    ldr r3,[sp,#0x0]                         @ 080d8634 009b
    cmp r0,#0x0                              @ 080d8636 0028
    beq LAB_080d867a                         @ 080d8638 1fd0
    movs r1,#0x8    @ 080d863a 0821
    rsbs r1,r1,#0    @ 080d863c 4942
    adds r0,r1,#0x0    @ 080d863e 081c
    ldrb r2,[r4,#0x0]                        @ 080d8640 2278
    ands r0,r2    @ 080d8642 1040
    strb r0,[r4,#0x0]                        @ 080d8644 2070
    lsls r1,r5,#0x4    @ 080d8646 2901
    adds r0,r6,#0x0    @ 080d8648 301c
    ldrh r2,[r4,#0x0]                        @ 080d864a 2288
    ands r0,r2    @ 080d864c 1040
    orrs r0,r1    @ 080d864e 0843
    strh r0,[r4,#0x0]                        @ 080d8650 2080
    movs r2,#0x0    @ 080d8652 0022
    lsls r1,r5,#0x1    @ 080d8654 6900
    ldr r0, DAT_080d868c                     @ 080d8656 0d48
    adds r1,r1,r0    @ 080d8658 0918
    adds r0,r6,#0x0    @ 080d865a 301c
    ldrb r1,[r1,#0x0]                        @ 080d865c 0978
    ands r0,r1    @ 080d865e 0840
    cmp r0,#0x0                              @ 080d8660 0028
    bne LAB_080d8666                         @ 080d8662 00d1
    movs r2,#0x1    @ 080d8664 0122
LAB_080d8666:
    lsls r1,r2,#0x3    @ 080d8666 d100
    movs r2,#0x9    @ 080d8668 0922
    rsbs r2,r2,#0    @ 080d866a 5242
    adds r0,r2,#0x0    @ 080d866c 101c
    ldrb r2,[r4,#0x0]                        @ 080d866e 2278
    ands r0,r2    @ 080d8670 1040
    orrs r0,r1    @ 080d8672 0843
    strb r0,[r4,#0x0]                        @ 080d8674 2070
    adds r3,#0x1    @ 080d8676 0133
    adds r4,#0x4    @ 080d8678 0434
LAB_080d867a:
    adds r5,#0x1    @ 080d867a 0135
    ldr r0, DAT_080d8688                     @ 080d867c 0248
    ldrh r0,[r0,#0x0]                        @ 080d867e 0088
    cmp r5,r0                                @ 080d8680 8542
    bls LAB_080d862a                         @ 080d8682 d2d9
    b LAB_080d86ea                           @ 080d8684 31e0
    .zero  0x2
DAT_080d8688:
    .word  0x095b7cca                     @ 080d8688 ca7c5b09
DAT_080d868c:
    .word  0x02000006                     @ 080d868c 06000002
LAB_080d8690:
    movs r5,#0x1    @ 080d8690 0125
    ldr r0, DAT_080d86fc                     @ 080d8692 1a48
    ldrh r0,[r0,#0x0]                        @ 080d8694 0088
    cmp r5,r0                                @ 080d8696 8542
    bhi LAB_080d86ea                         @ 080d8698 27d8
    movs r6,#0xf    @ 080d869a 0f26
LAB_080d869c:
    lsls r1,r5,#0x1    @ 080d869c 6900
    ldr r0, DAT_080d8700                     @ 080d869e 1848
    adds r1,r1,r0    @ 080d86a0 0918
    adds r0,r6,#0x0    @ 080d86a2 301c
    ldrb r1,[r1,#0x0]                        @ 080d86a4 0978
    ands r0,r1    @ 080d86a6 0840
    cmp r0,#0x0                              @ 080d86a8 0028
    bne LAB_080d86e0                         @ 080d86aa 19d1
    adds r0,r5,#0x0    @ 080d86ac 281c
    adds r1,r7,#0x0    @ 080d86ae 391c
    str r3,[sp,#0x0]                         @ 080d86b0 0093
    bl check_pack_card_slot_filter           @ 080d86b2 02f017fc
    ldr r3,[sp,#0x0]                         @ 080d86b6 009b
    cmp r0,#0x0                              @ 080d86b8 0028
    beq LAB_080d86e0                         @ 080d86ba 11d0
    movs r1,#0x8    @ 080d86bc 0821
    rsbs r1,r1,#0    @ 080d86be 4942
    adds r0,r1,#0x0    @ 080d86c0 081c
    ldrb r2,[r4,#0x0]                        @ 080d86c2 2278
    ands r0,r2    @ 080d86c4 1040
    strb r0,[r4,#0x0]                        @ 080d86c6 2070
    lsls r1,r5,#0x4    @ 080d86c8 2901
    adds r0,r6,#0x0    @ 080d86ca 301c
    ldrh r2,[r4,#0x0]                        @ 080d86cc 2288
    ands r0,r2    @ 080d86ce 1040
    orrs r0,r1    @ 080d86d0 0843
    strh r0,[r4,#0x0]                        @ 080d86d2 2080
    movs r0,#0x8    @ 080d86d4 0820
    ldrb r1,[r4,#0x0]                        @ 080d86d6 2178
    orrs r0,r1    @ 080d86d8 0843
    strb r0,[r4,#0x0]                        @ 080d86da 2070
    adds r3,#0x1    @ 080d86dc 0133
    adds r4,#0x4    @ 080d86de 0434
LAB_080d86e0:
    adds r5,#0x1    @ 080d86e0 0135
    ldr r0, DAT_080d86fc                     @ 080d86e2 0648
    ldrh r0,[r0,#0x0]                        @ 080d86e4 0088
    cmp r5,r0                                @ 080d86e6 8542
    bls LAB_080d869c                         @ 080d86e8 d8d9
LAB_080d86ea:
    adds r0,r3,#0x0    @ 080d86ea 181c
    add sp,#0x4                              @ 080d86ec 01b0
    pop {r3,r4,r5}                           @ 080d86ee 38bc
    .hword 0x4698    @ 080d86f0 9846
    .hword 0x46a1    @ 080d86f2 a146
    .hword 0x46aa    @ 080d86f4 aa46
    pop {r4,r5,r6,r7}                        @ 080d86f6 f0bc
    pop {r1}                                 @ 080d86f8 02bc
    bx r1                                    @ 080d86fa 0847
DAT_080d86fc:
    .word  0x095b7cca                     @ 080d86fc ca7c5b09
DAT_080d8700:
    .word  0x02000006                     @ 080d8700 06000002

@ Fisher-Yates shuffle of the EWRAM card-select slot array at 0x0200af20. r0=pack_index, r1=total_slot_count, r2=output_slot_count. Calls tick_prng_lcg_rand15 for random numbers, takes modulo slot_count for target slot, checks for duplicate slots (prevents same card twice), writes selected slot word to output array. Retries up to 0x3e7 (999) times to avoid infinite loop. Used to randomise display order in the pack-draw UI.
@ 
@ Constants:
@ - SLOT_ARRAY=0x0200af20 // EWRAM card-select slot array base
@ - MAX_RETRY=0x3e7 // 999: max retry count to prevent infinite loop
@ - MASK_LOW16=0x0000fff0 // low-16 read mask
shuffle_pack_card_select_slots:
    push {r4,r5,r6,r7,lr}                    @ 080d8704 f0b5
    .hword 0x4657    @ 080d8706 5746
    .hword 0x464e    @ 080d8708 4e46
    .hword 0x4645    @ 080d870a 4546
    push {r5,r6,r7}                          @ 080d870c e0b4
    sub sp,#0x14                             @ 080d870e 85b0
    adds r7,r0,#0x0    @ 080d8710 071c
    str r1,[sp,#0x0]                         @ 080d8712 0091
    str r2,[sp,#0x4]                         @ 080d8714 0192
    str r7,[sp,#0x8]                         @ 080d8716 0297
    cmp r1,#0x0                              @ 080d8718 0029
    beq LAB_080d87b8                         @ 080d871a 4dd0
    movs r0,#0x0    @ 080d871c 0020
    .hword 0x4680    @ 080d871e 8046
    cmp r8,r2                                @ 080d8720 9045
    bcs LAB_080d87b8                         @ 080d8722 49d2
    ldr r1, DAT_080d8768                     @ 080d8724 1049
    .hword 0x4689    @ 080d8726 8946
LAB_080d8728:
    movs r4,#0x0    @ 080d8728 0024
    .hword 0x46a2    @ 080d872a a246
    ldr r0,[sp,#0x8]                         @ 080d872c 0298
    adds r0,#0x4    @ 080d872e 0430
    str r0,[sp,#0xc]                         @ 080d8730 0390
    .hword 0x4641    @ 080d8732 4146
    adds r1,#0x1    @ 080d8734 0131
    str r1,[sp,#0x10]                        @ 080d8736 0491
LAB_080d8738:
    movs r6,#0x1    @ 080d8738 0126
    bl tick_prng_lcg_rand15                  @ 080d873a 20f0dbfb
    lsls r0,r0,#0x10    @ 080d873e 0004
    lsrs r0,r0,#0x10    @ 080d8740 000c
    ldr r1,[sp,#0x0]                         @ 080d8742 0099
    bl get_bios_div_remainder                @ 080d8744 35f05cfe
    adds r5,r0,#0x0    @ 080d8748 051c
    movs r3,#0x0    @ 080d874a 0023
    cmp r3,r8                                @ 080d874c 4345
    bcs LAB_080d8790                         @ 080d874e 1fd2
    lsls r2,r5,#0x2    @ 080d8750 aa00
    ldr r4, DAT_080d876c                     @ 080d8752 064c
    adds r0,r2,r4    @ 080d8754 1019
    .hword 0x4649    @ 080d8756 4946
    ldrh r0,[r0,#0x0]                        @ 080d8758 0088
    ands r1,r0    @ 080d875a 0140
    .hword 0x4648    @ 080d875c 4846
    ldrh r4,[r7,#0x0]                        @ 080d875e 3c88
    ands r0,r4    @ 080d8760 2040
    adds r4,r2,#0x0    @ 080d8762 141c
    b LAB_080d878a                           @ 080d8764 11e0
    .zero  0x2
DAT_080d8768:
    .word  0x0000fff0                     @ 080d8768 f0ff0000
DAT_080d876c:
    .word  0x0200af20                     @ 080d876c 20af0002
LAB_080d8770:
    adds r3,#0x1    @ 080d8770 0133
    cmp r3,r8                                @ 080d8772 4345
    bcs LAB_080d8790                         @ 080d8774 0cd2
    ldr r1, DAT_080d87c8                     @ 080d8776 1449
    adds r0,r4,r1    @ 080d8778 6018
    lsls r2,r3,#0x2    @ 080d877a 9a00
    adds r2,r2,r7    @ 080d877c d219
    .hword 0x4649    @ 080d877e 4946
    ldrh r0,[r0,#0x0]                        @ 080d8780 0088
    ands r1,r0    @ 080d8782 0140
    .hword 0x4648    @ 080d8784 4846
    ldrh r2,[r2,#0x0]                        @ 080d8786 1288
    ands r0,r2    @ 080d8788 1040
LAB_080d878a:
    cmp r1,r0                                @ 080d878a 8142
    bne LAB_080d8770                         @ 080d878c f0d1
    movs r6,#0x0    @ 080d878e 0026
LAB_080d8790:
    cmp r6,#0x1                              @ 080d8790 012e
    beq LAB_080d879e                         @ 080d8792 04d0
    movs r4,#0x1    @ 080d8794 0124
    add r10,r4                               @ 080d8796 a244
    ldr r0, DAT_080d87cc                     @ 080d8798 0c48
    cmp r10,r0                               @ 080d879a 8245
    bls LAB_080d8738                         @ 080d879c ccd9
LAB_080d879e:
    lsls r0,r5,#0x2    @ 080d879e a800
    ldr r1, DAT_080d87c8                     @ 080d87a0 0949
    adds r0,r0,r1    @ 080d87a2 4018
    ldr r0,[r0,#0x0]                         @ 080d87a4 0068
    ldr r4,[sp,#0x8]                         @ 080d87a6 029c
    str r0,[r4,#0x0]                         @ 080d87a8 2060
    ldr r0,[sp,#0xc]                         @ 080d87aa 0398
    str r0,[sp,#0x8]                         @ 080d87ac 0290
    ldr r1,[sp,#0x10]                        @ 080d87ae 0499
    .hword 0x4688    @ 080d87b0 8846
    ldr r4,[sp,#0x4]                         @ 080d87b2 019c
    cmp r8,r4                                @ 080d87b4 a045
    bcc LAB_080d8728                         @ 080d87b6 b7d3
LAB_080d87b8:
    add sp,#0x14                             @ 080d87b8 05b0
    pop {r3,r4,r5}                           @ 080d87ba 38bc
    .hword 0x4698    @ 080d87bc 9846
    .hword 0x46a1    @ 080d87be a146
    .hword 0x46aa    @ 080d87c0 aa46
    pop {r4,r5,r6,r7}                        @ 080d87c2 f0bc
    pop {r0}                                 @ 080d87c4 01bc
    bx r0                                    @ 080d87c6 0047
DAT_080d87c8:
    .word  0x0200af20                     @ 080d87c8 20af0002
DAT_080d87cc:
    .word  0x000003e7                     @ 080d87cc e7030000

@ Called by the state machine when the pack purchase confirm panel enters its display phase, to initialize the confirm panel overlay struct and palette. Passes the pack_ui_state[+0x6d0] offset region to init_overlay_struct_and_palette (EWRAM target 0x0200af20, buf_size=0xe, color_count=0xf); then clears pack_ui_state[+0x4] (panel state counter). Returns fixed value 1 indicating initialization complete.
@ 
@ Constants:
@ - OVERLAY_EWRAM = 0x0200af20 (DAT_080d8800)
@ - OVERLAY_BUF_SIZE_IDX = 0xe (movs r2,#0xe; 5th stack argument)
@ - OVERLAY_COLOR_COUNT = 0xf (movs r3,#0xf)
@ - OVERLAY_OFFSET = 0xda<<3 = 0x6d0 (pack_ui_state[+0x6d0])
@ - PANEL_STATE_OFFSET = +0x4 (strh 0,[r4,#0x4])
init_pack_confirm_panel_overlay:
    push {r4,lr}                             @ 080d87d0 10b5
    sub sp,#0x4                              @ 080d87d2 81b0
    ldr r0, DAT_080d87fc                     @ 080d87d4 0948
    adds r4,r0,#0x0    @ 080d87d6 041c
    adds r4,#0xc    @ 080d87d8 0c34
    movs r1,#0xda    @ 080d87da da21
    lsls r1,r1,#0x3    @ 080d87dc c900
    adds r0,r0,r1    @ 080d87de 4018
    ldr r1, DAT_080d8800                     @ 080d87e0 0749
    movs r2,#0xe    @ 080d87e2 0e22
    str r2,[sp,#0x0]                         @ 080d87e4 0092
    movs r2,#0x0    @ 080d87e6 0022
    movs r3,#0xf    @ 080d87e8 0f23
    bl init_overlay_struct_and_palette       @ 080d87ea 04f0ddfd
    movs r0,#0x0    @ 080d87ee 0020
    strh r0,[r4,#0x4]                        @ 080d87f0 a080
    movs r0,#0x1    @ 080d87f2 0120
    add sp,#0x4                              @ 080d87f4 01b0
    pop {r4}                                 @ 080d87f6 10bc
    pop {r1}                                 @ 080d87f8 02bc
    bx r1                                    @ 080d87fa 0847
DAT_080d87fc:
    .word  pack_ui_state                  @ 080d87fc 50580003
DAT_080d8800:
    .word  0x0200af20                     @ 080d8800 20af0002

@ Triggered in the duel puzzle result screen of the pack shop. Calls reset_all_bg_scroll_regs_and_shadows to clear scroll registers, then queries text row for string ID=0x13f6(5110), computes game_str_pointer_table index using IWRAM[0x2006c2c] language flag, passes the text pointer to text_overlay_create at screen pos (x=0x10, y=0x1e). Finally sets pack_ui_state[+0x10] := 1 to mark the text overlay as active.
@ 
@ Constants:
@ - STR_ID=0x13f6 (5110) // duel puzzle result text string
@ - TEXT_POS=0x0010001e // x=16, y=30 pixels
@ - LANG_FLAG_OFFSET=0x6c2c // IWRAM language flag byte offset
init_duel_puzzle_result_text_overlay:
    push {r4,lr}                             @ 080d8804 10b5
    bl reset_all_bg_scroll_regs_and_shadows  @ 080d8806 1df03ff9
    ldr r4, DAT_080d884c                     @ 080d880a 104c
    ldr r0, DAT_080d8850                     @ 080d880c 1048
    bl game_str_id_to_row                    @ 080d880e 1cf003fb
    ldr r2, PTR_game_str_pointer_table_080d8854 @ 080d8812 104a
    lsls r0,r0,#0x10    @ 080d8814 0004
    lsrs r0,r0,#0x10    @ 080d8816 000c
    lsls r1,r0,#0x1    @ 080d8818 4100
    adds r1,r1,r0    @ 080d881a 0918
    lsls r1,r1,#0x1    @ 080d881c 4900
    ldr r0, DAT_080d8858                     @ 080d881e 0e48
    ldr r3, DAT_080d885c                     @ 080d8820 0e4b
    adds r0,r0,r3    @ 080d8822 c018
    ldrb r0,[r0,#0x0]                        @ 080d8824 0078
    lsls r0,r0,#0x1d    @ 080d8826 4007
    lsrs r0,r0,#0x1d    @ 080d8828 400f
    adds r1,r1,r0    @ 080d882a 0918
    lsls r1,r1,#0x2    @ 080d882c 8900
    adds r1,r1,r2    @ 080d882e 8918
    ldr r2,[r1,#0x0]                         @ 080d8830 0a68
    ldr r0, PTR_game_str_ja_080d8860         @ 080d8832 0b48
    adds r2,r2,r0    @ 080d8834 1218
    adds r0,r4,#0x0    @ 080d8836 201c
    movs r1,#0x0    @ 080d8838 0021
    bl text_overlay_create                   @ 080d883a 04f07ffe
    ldr r1, DAT_080d8864                     @ 080d883e 0949
    movs r0,#0x1    @ 080d8840 0120
    strh r0,[r1,#0x10]                       @ 080d8842 0882
    pop {r4}                                 @ 080d8844 10bc
    pop {r1}                                 @ 080d8846 02bc
    bx r1                                    @ 080d8848 0847
    .zero  0x2
DAT_080d884c:
    .word  0x0010001e                     @ 080d884c 1e001000
DAT_080d8850:
    .word  0x000013f6                     @ 080d8850 f6130000
PTR_game_str_pointer_table_080d8854:
    .word  game_str_pointer_table         @ 080d8854 400f0008
DAT_080d8858:
    .word  0x02000000                     @ 080d8858 00000002
DAT_080d885c:
    .word  0x00006c2c                     @ 080d885c 2c6c0000
PTR_game_str_ja_080d8860:
    .word  game_str_ja                    @ 080d8860 109cdb09
DAT_080d8864:
    .word  pack_ui_state                  @ 080d8864 50580003

@ Called during the pack card flip wait phase by the frame driver, monitoring the flip animation completion signal. First writes BLDALPHA to 0x1000 (full brightness, eva=0, evb=31); calls tick_overlay_animation_step(0) to advance the overlay animation; reads gPrng[0x1d0].halfword[+0x1c] (flip state field); if it equals 2, writes pack_ui_state[+0x10]=2 (advances state machine step) and returns 1; otherwise returns 0.
@ 
@ Constants:
@ - BLDALPHA_FULL = 0x80<<5 = 0x1000 (full brightness: eva=0, evb=0x10)
@ - BLDALPHA_ADDR = 0x80<<0x13 = 0x04000000, BLDALPHA = 0x04000052
@ - gPrng_FIELD_OFFSET = 0xe8<<1 = 0x1d0 (gPrng[+0x1d0])
@ - FLIP_STATE_DONE = 2 (cmp r1,#0x2 = flip complete state code)
@ - NEXT_STATE = 2 (strh r1,[r0,#0x10])
tick_pack_card_flip_wait:
    push {r4,lr}                             @ 080d8868 10b5
    movs r4,#0x0    @ 080d886a 0024
    movs r2,#0x80    @ 080d886c 8022
    lsls r2,r2,#0x13    @ 080d886e d204
    movs r0,#0x80    @ 080d8870 8020
    lsls r0,r0,#0x5    @ 080d8872 4001
    ldrh r1,[r2,#0x0]                        @ 080d8874 1188
    orrs r0,r1    @ 080d8876 0843
    strh r0,[r2,#0x0]                        @ 080d8878 1080
    movs r0,#0x0    @ 080d887a 0020
    bl tick_overlay_animation_step           @ 080d887c 04f0b2fe
    ldr r0, PTR_gPrng_080d88a0               @ 080d8880 0748
    movs r1,#0xe8    @ 080d8882 e821
    lsls r1,r1,#0x1    @ 080d8884 4900
    adds r0,r0,r1    @ 080d8886 4018
    ldr r0,[r0,#0x0]                         @ 080d8888 0068
    ldrh r1,[r0,#0x1c]                       @ 080d888a 818b
    cmp r1,#0x2                              @ 080d888c 0229
    bne LAB_080d8896                         @ 080d888e 02d1
    ldr r0, DAT_080d88a4                     @ 080d8890 0448
    strh r1,[r0,#0x10]                       @ 080d8892 0182
    movs r4,#0x1    @ 080d8894 0124
LAB_080d8896:
    adds r0,r4,#0x0    @ 080d8896 201c
    pop {r4}                                 @ 080d8898 10bc
    pop {r1}                                 @ 080d889a 02bc
    bx r1                                    @ 080d889c 0847
    .zero  0x2
PTR_gPrng_080d88a0:
    .word  gPrng                          @ 080d88a0 40000003
DAT_080d88a4:
    .word  pack_ui_state                  @ 080d88a4 50580003

@ Called during the pack card drawing reveal phase by the frame driver, performing random card draw logic and filling reveal data for each pending card slot. Iterates all card slots (slot count from [r2,#8]); for each slot, uses the attribute type from get_pack_info_attr2 (=5 for flash/rare, otherwise common) to call tick_prng_lcg_rand15 multiple times to generate random card type and count; uses get_bios_div_remainder to modulate random values to determine per-column draw count (3 or 4); writes results into a temporary array on the stack; then performs 100 random swap shuffles (0x64 iterations) across 10 card slots (sp[0..9]); finally iterates 10 slots to call set_card_flag_bit to mark revealed cards and writes reveal info to pack_ui_state[+0x6f4/+0x6ee]; calls tick_overlay_animation_step(0) to advance the overlay animation; writes pack_ui_state[+0x10]=3 to advance the state machine. Returns 1 (fixed; Sub-case E).
@ 
@ Constants:
@ - pack_ui_state base = 0x03005850
@ - REVEAL_DATA_OFFSET = 0x6f4 (DAT_080d8a7c)
@ - REVEAL_COUNT_OFFSET = 0x6ee (DAT_080d8a80)
@ - PACK_DATA_PTR = 0x6fc (DAT_080d8910 = 0x6fc, pack_ui_state[+0x6fc])
@ - CARD_POOL_PTR = 0x02029eb0 (DAT_080d8914, pack card data pool)
@ - PRNG_MASK_15BIT = 0x7fff (DAT_080d8918/DAT_080d8960)
@ - SHUFFLE_ITER_COUNT = 0x64 (cmp r5,#0x63 + 1 = 100 shuffles)
@ - SLOT_COUNT = 10 (cmp r5,#0x9 = 10 card slots)
@ - NEXT_STATE = 3 (strh r0,[r1,#0x10])
@ - AOB_SLOT_STRIDE = 4 (adds r4,#0x4 in inner loop)
@ - ANIM_MODE = 0 (tick_overlay_animation_step(0))
tick_pack_card_reveal_slot_loop:
    push {r4,r5,r6,r7,lr}                    @ 080d88a8 f0b5
    .hword 0x4657    @ 080d88aa 5746
    .hword 0x464e    @ 080d88ac 4e46
    .hword 0x4645    @ 080d88ae 4546
    push {r5,r6,r7}                          @ 080d88b0 e0b4
    sub sp,#0x28                             @ 080d88b2 8ab0
    ldr r0, DAT_080d890c                     @ 080d88b4 1548
    movs r1,#0xc    @ 080d88b6 0c21
    adds r1,r1,r0    @ 080d88b8 0918
    .hword 0x468a    @ 080d88ba 8a46
    ldr r2, DAT_080d8910                     @ 080d88bc 144a
    adds r0,r0,r2    @ 080d88be 8018
    ldr r1, DAT_080d8914                     @ 080d88c0 1449
    str r1,[r0,#0x0]                         @ 080d88c2 0160
    .hword 0x4689    @ 080d88c4 8946
    movs r7,#0x0    @ 080d88c6 0027
    .hword 0x4653    @ 080d88c8 5346
    ldrh r3,[r3,#0x8]                        @ 080d88ca 1b89
    cmp r7,r3                                @ 080d88cc 9f42
    bcc LAB_080d88d2                         @ 080d88ce 00d3
    b LAB_080d8a44                           @ 080d88d0 b8e0
LAB_080d88d2:
    lsls r0,r7,#0x5    @ 080d88d2 7801
    adds r0,#0x44    @ 080d88d4 4430
    .hword 0x4654    @ 080d88d6 5446
    adds r6,r4,r0    @ 080d88d8 2618
    ldrh r0,[r6,#0x0]                        @ 080d88da 3088
    bl get_pack_info_attr2                   @ 080d88dc 04f032f9
    adds r1,r0,#0x0    @ 080d88e0 011c
    ldrh r0,[r6,#0x18]                       @ 080d88e2 308b
    adds r2,r7,#0x1    @ 080d88e4 7a1c
    .hword 0x4690    @ 080d88e6 9046
    cmp r0,#0x0                              @ 080d88e8 0028
    bne LAB_080d88ee                         @ 080d88ea 00d1
    b LAB_080d8a38                           @ 080d88ec a4e0
LAB_080d88ee:
    cmp r1,#0x5                              @ 080d88ee 0529
    bne LAB_080d893a                         @ 080d88f0 23d1
    bl tick_prng_lcg_rand15                  @ 080d88f2 20f0fffa
    ldr r3, DAT_080d8918                     @ 080d88f6 084b
    adds r1,r3,#0x0    @ 080d88f8 191c
    ands r1,r0    @ 080d88fa 0140
    adds r0,r1,#0x0    @ 080d88fc 081c
    movs r1,#0x5    @ 080d88fe 0521
    bl get_bios_div_remainder                @ 080d8900 35f07efd
    cmp r0,#0x0                              @ 080d8904 0028
    bne LAB_080d891c                         @ 080d8906 09d1
    movs r0,#0x4    @ 080d8908 0420
    b LAB_080d891e                           @ 080d890a 08e0
DAT_080d890c:
    .word  pack_ui_state                  @ 080d890c 50580003
DAT_080d8910:
    .word  0x000006fc                     @ 080d8910 fc060000
DAT_080d8914:
    .word  0x02029eb0                     @ 080d8914 b09e0202
DAT_080d8918:
    .word  0x00007fff                     @ 080d8918 ff7f0000
LAB_080d891c:
    movs r0,#0x3    @ 080d891c 0320
LAB_080d891e:
    str r0,[sp,#0x0]                         @ 080d891e 0090
    movs r0,#0x2    @ 080d8920 0220
    str r0,[sp,#0x4]                         @ 080d8922 0190
    str r0,[sp,#0x8]                         @ 080d8924 0290
    movs r5,#0x3    @ 080d8926 0325
    adds r7,#0x1    @ 080d8928 0137
    .hword 0x46b8    @ 080d892a b846
    movs r1,#0x1    @ 080d892c 0121
    add r0,sp,#0xc                           @ 080d892e 03a8
LAB_080d8930:
    stmia r0!,{r1}                           @ 080d8930 02c0
    adds r5,#0x1    @ 080d8932 0135
    cmp r5,#0x9                              @ 080d8934 092d
    bls LAB_080d8930                         @ 080d8936 fbd9
    b LAB_080d89a4                           @ 080d8938 34e0
LAB_080d893a:
    bl tick_prng_lcg_rand15                  @ 080d893a 20f0dbfa
    movs r1,#0x1    @ 080d893e 0121
    ands r1,r0    @ 080d8940 0140
    cmp r1,#0x0                              @ 080d8942 0029
    bne LAB_080d8968                         @ 080d8944 10d1
    bl tick_prng_lcg_rand15                  @ 080d8946 20f0d5fa
    ldr r4, DAT_080d8960                     @ 080d894a 054c
    adds r1,r4,#0x0    @ 080d894c 211c
    ands r1,r0    @ 080d894e 0140
    adds r0,r1,#0x0    @ 080d8950 081c
    movs r1,#0x5    @ 080d8952 0521
    bl get_bios_div_remainder                @ 080d8954 35f054fd
    cmp r0,#0x0                              @ 080d8958 0028
    bne LAB_080d8964                         @ 080d895a 03d1
    movs r0,#0x4    @ 080d895c 0420
    b LAB_080d896a                           @ 080d895e 04e0
DAT_080d8960:
    .word  0x00007fff                     @ 080d8960 ff7f0000
LAB_080d8964:
    movs r0,#0x3    @ 080d8964 0320
    b LAB_080d896a                           @ 080d8966 00e0
LAB_080d8968:
    movs r0,#0x0    @ 080d8968 0020
LAB_080d896a:
    str r0,[sp,#0x0]                         @ 080d896a 0090
    movs r4,#0x2    @ 080d896c 0224
    str r4,[sp,#0x4]                         @ 080d896e 0194
    bl tick_prng_lcg_rand15                  @ 080d8970 20f0c0fa
    movs r2,#0x1    @ 080d8974 0122
    adds r1,r2,#0x0    @ 080d8976 111c
    ands r1,r0    @ 080d8978 0140
    cmp r1,#0x0                              @ 080d897a 0029
    bne LAB_080d8982                         @ 080d897c 01d1
    str r4,[sp,#0x8]                         @ 080d897e 0294
    b LAB_080d8984                           @ 080d8980 00e0
LAB_080d8982:
    str r2,[sp,#0x8]                         @ 080d8982 0292
LAB_080d8984:
    movs r5,#0x3    @ 080d8984 0325
    adds r7,#0x1    @ 080d8986 0137
    .hword 0x46b8    @ 080d8988 b846
    movs r1,#0x1    @ 080d898a 0121
    add r0,sp,#0xc                           @ 080d898c 03a8
LAB_080d898e:
    stmia r0!,{r1}                           @ 080d898e 02c0
    adds r5,#0x1    @ 080d8990 0135
    cmp r5,#0x5                              @ 080d8992 052d
    bls LAB_080d898e                         @ 080d8994 fbd9
    movs r5,#0x6    @ 080d8996 0625
    movs r1,#0x0    @ 080d8998 0021
    add r0,sp,#0x18                          @ 080d899a 06a8
LAB_080d899c:
    stmia r0!,{r1}                           @ 080d899c 02c0
    adds r5,#0x1    @ 080d899e 0135
    cmp r5,#0x9                              @ 080d89a0 092d
    bls LAB_080d899c                         @ 080d89a2 fbd9
LAB_080d89a4:
    movs r5,#0x0    @ 080d89a4 0025
LAB_080d89a6:
    bl tick_prng_lcg_rand15                  @ 080d89a6 20f0a5fa
    lsls r0,r0,#0x10    @ 080d89aa 0004
    lsrs r0,r0,#0x10    @ 080d89ac 000c
    movs r1,#0xa    @ 080d89ae 0a21
    bl get_bios_div_remainder                @ 080d89b0 35f026fd
    adds r4,r0,#0x0    @ 080d89b4 041c
    bl tick_prng_lcg_rand15                  @ 080d89b6 20f09dfa
    lsls r0,r0,#0x10    @ 080d89ba 0004
    lsrs r0,r0,#0x10    @ 080d89bc 000c
    movs r1,#0x9    @ 080d89be 0921
    bl get_bios_div_remainder                @ 080d89c0 35f01efd
    adds r1,r0,#0x0    @ 080d89c4 011c
    cmp r4,r1                                @ 080d89c6 8c42
    bne LAB_080d89cc                         @ 080d89c8 00d1
    adds r1,#0x1    @ 080d89ca 0131
LAB_080d89cc:
    lsls r0,r4,#0x2    @ 080d89cc a000
    .hword 0x466b    @ 080d89ce 6b46
    adds r2,r3,r0    @ 080d89d0 1a18
    ldr r3,[r2,#0x0]                         @ 080d89d2 1368
    lsls r0,r1,#0x2    @ 080d89d4 8800
    .hword 0x466c    @ 080d89d6 6c46
    adds r1,r4,r0    @ 080d89d8 2118
    ldr r0,[r1,#0x0]                         @ 080d89da 0868
    str r0,[r2,#0x0]                         @ 080d89dc 1060
    str r3,[r1,#0x0]                         @ 080d89de 0b60
    adds r5,#0x1    @ 080d89e0 0135
    cmp r5,#0x63                             @ 080d89e2 632d
    bls LAB_080d89a6                         @ 080d89e4 dfd9
    movs r7,#0x1    @ 080d89e6 0127
    movs r5,#0x0    @ 080d89e8 0025
LAB_080d89ea:
    ldr r0,[r6,#0x14]                        @ 080d89ea 7069
    ands r0,r7    @ 080d89ec 3840
    cmp r0,#0x0                              @ 080d89ee 0028
    beq LAB_080d8a28                         @ 080d89f0 1ad0
    movs r0,#0x7f    @ 080d89f2 7f20
    ldrb r1,[r6,#0x0]                        @ 080d89f4 3178
    ands r0,r1    @ 080d89f6 0840
    .hword 0x464a    @ 080d89f8 4a46
    strb r0,[r2,#0x0]                        @ 080d89fa 1070
    ldrh r0,[r6,#0x0]                        @ 080d89fc 3088
    bl get_pack_info_attr2                   @ 080d89fe 04f0a1f8
    movs r1,#0xf    @ 080d8a02 0f21
    ands r0,r1    @ 080d8a04 0840
    movs r3,#0x10    @ 080d8a06 1023
    rsbs r3,r3,#0    @ 080d8a08 5b42
    adds r1,r3,#0x0    @ 080d8a0a 191c
    .hword 0x464a    @ 080d8a0c 4a46
    ldrb r2,[r2,#0x1]                        @ 080d8a0e 5278
    ands r1,r2    @ 080d8a10 1140
    orrs r1,r0    @ 080d8a12 0143
    .hword 0x464b    @ 080d8a14 4b46
    strb r1,[r3,#0x1]                        @ 080d8a16 5970
    ldrb r0,[r4,#0x0]                        @ 080d8a18 2078
    lsls r2,r0,#0x4    @ 080d8a1a 0201
    movs r0,#0xf    @ 080d8a1c 0f20
    ands r1,r0    @ 080d8a1e 0140
    orrs r1,r2    @ 080d8a20 1143
    strb r1,[r3,#0x1]                        @ 080d8a22 5970
    movs r1,#0x4    @ 080d8a24 0421
    add r9,r1                                @ 080d8a26 8944
LAB_080d8a28:
    lsls r7,r7,#0x1    @ 080d8a28 7f00
    adds r4,#0x4    @ 080d8a2a 0434
    adds r5,#0x1    @ 080d8a2c 0135
    cmp r5,#0x9                              @ 080d8a2e 092d
    bls LAB_080d89ea                         @ 080d8a30 dbd9
    ldrh r0,[r6,#0x0]                        @ 080d8a32 3088
    bl set_card_flag_bit                     @ 080d8a34 21f02cf8
LAB_080d8a38:
    .hword 0x4647    @ 080d8a38 4746
    .hword 0x4652    @ 080d8a3a 5246
    ldrh r2,[r2,#0x8]                        @ 080d8a3c 1289
    cmp r7,r2                                @ 080d8a3e 9742
    bcs LAB_080d8a44                         @ 080d8a40 00d2
    b LAB_080d88d2                           @ 080d8a42 46e7
LAB_080d8a44:
    ldr r2, DAT_080d8a7c                     @ 080d8a44 0d4a
    add r2,r10                               @ 080d8a46 5244
    .hword 0x464b    @ 080d8a48 4b46
    str r3,[r2,#0x0]                         @ 080d8a4a 1360
    ldr r1, DAT_080d8a80                     @ 080d8a4c 0c49
    add r1,r10                               @ 080d8a4e 5144
    movs r0,#0x0    @ 080d8a50 0020
    strh r0,[r1,#0x0]                        @ 080d8a52 0880
    movs r1,#0xdf    @ 080d8a54 df21
    lsls r1,r1,#0x3    @ 080d8a56 c900
    add r1,r10                               @ 080d8a58 5144
    ldr r0,[r2,#0x0]                         @ 080d8a5a 1068
    str r0,[r1,#0x0]                         @ 080d8a5c 0860
    movs r0,#0x0    @ 080d8a5e 0020
    bl tick_overlay_animation_step           @ 080d8a60 04f0c0fd
    ldr r1, DAT_080d8a84                     @ 080d8a64 0749
    movs r0,#0x3    @ 080d8a66 0320
    strh r0,[r1,#0x10]                       @ 080d8a68 0882
    movs r0,#0x1    @ 080d8a6a 0120
    add sp,#0x28                             @ 080d8a6c 0ab0
    pop {r3,r4,r5}                           @ 080d8a6e 38bc
    .hword 0x4698    @ 080d8a70 9846
    .hword 0x46a1    @ 080d8a72 a146
    .hword 0x46aa    @ 080d8a74 aa46
    pop {r4,r5,r6,r7}                        @ 080d8a76 f0bc
    pop {r1}                                 @ 080d8a78 02bc
    bx r1                                    @ 080d8a7a 0847
DAT_080d8a7c:
    .word  0x000006f4                     @ 080d8a7c f4060000
DAT_080d8a80:
    .word  0x000006ee                     @ 080d8a80 ee060000
DAT_080d8a84:
    .word  pack_ui_state                  @ 080d8a84 50580003

@ Called during the pack card select phase by the frame driver, builds the card select candidate array for each slot of the current pack and performs shuffles. Iterates all pack card slots; for each slot calls get_pack_info_attr2 to get the attribute type (0=empty/invalid, skip); computes candidate card type mask r4 from attribute bit fields; if r4!=1, repeatedly calls build_pack_card_select_slot_data to fill candidate data until successful (non-zero return), then calls shuffle_pack_card_select_slots to shuffle and advances the pointer (+4); if r4=1, fills once and shuffles. After all slots are done, performs 1000 random swap shuffles (0x3e8 iterations) on the pack_ui_state[+0x6ee] pointer array; then increments the pack_ui_state[+0x6ee] counter; if equal to pack[+0xa], writes pack_ui_state[+0x10]=4 to advance state; calls tick_overlay_animation_step(0). Returns r9: 0 (count still below pack[+0xa] target) or 1 (count reached pack[+0xa] target; epilogue .hword 0x4648 = mov r0,r9).
@ 
@ Constants:
@ - PACK_DATA_OFFSET = 0x6fc (DAT_080d8b00)
@ - SLOT_INDEX_OFFSET = 0x6fa (DAT_080d8b04)
@ - SLOT_ARRAY_OFFSET = 0x704 (DAT_080d8b08)
@ - SHUFFLE_SLOT_ITER = 0x3e8 (DAT_080d8bd4 = 0x3e7 + 1 = 1000 shuffles)
@ - REVEAL_COUNT_OFFSET = 0x6ee (DAT_080d8bd8)
@ - TYPE_MASK_TOP4 = 0xf0 (bits[7:4] of slot[+0x1] type mask)
@ - NEXT_STATE = 4 (strh 4,[pack_ui_state,#0x10])
build_pack_card_select_slots_for_pack:
    push {r4,r5,r6,r7,lr}                    @ 080d8a88 f0b5
    .hword 0x464f    @ 080d8a8a 4f46
    .hword 0x4646    @ 080d8a8c 4646
    push {r6,r7}                             @ 080d8a8e c0b4
    ldr r6, DAT_080d8afc                     @ 080d8a90 1a4e
    movs r0,#0xc    @ 080d8a92 0c20
    adds r0,r0,r6    @ 080d8a94 8019
    .hword 0x4680    @ 080d8a96 8046
    movs r1,#0x0    @ 080d8a98 0021
    .hword 0x4689    @ 080d8a9a 8946
    ldr r0, DAT_080d8b00                     @ 080d8a9c 1848
    adds r2,r6,r0    @ 080d8a9e 3218
    ldr r1, DAT_080d8b04                     @ 080d8aa0 1849
    adds r0,r6,r1    @ 080d8aa2 7018
    ldrh r0,[r0,#0x0]                        @ 080d8aa4 0088
    lsls r1,r0,#0x2    @ 080d8aa6 8100
    ldr r0,[r2,#0x0]                         @ 080d8aa8 1068
    adds r7,r0,r1    @ 080d8aaa 4718
    ldr r0,[r7,#0x0]                         @ 080d8aac 3868
    lsls r0,r0,#0x19    @ 080d8aae 4006
    lsrs r0,r0,#0x19    @ 080d8ab0 400e
    bl get_pack_info_attr2                   @ 080d8ab2 04f047f8
    adds r5,r0,#0x0    @ 080d8ab6 051c
    cmp r5,#0x0                              @ 080d8ab8 002d
    beq LAB_080d8b4a                         @ 080d8aba 46d0
    ldr r0,[r7,#0x0]                         @ 080d8abc 3868
    lsls r0,r0,#0x10    @ 080d8abe 0004
    lsrs r1,r0,#0x1c    @ 080d8ac0 010f
    movs r4,#0x1    @ 080d8ac2 0124
    lsls r4,r1    @ 080d8ac4 8c40
    adds r0,r1,#0x0    @ 080d8ac6 081c
    cmp r0,#0x3                              @ 080d8ac8 0328
    bls LAB_080d8ad0                         @ 080d8aca 01d9
    movs r0,#0xf0    @ 080d8acc f020
    orrs r4,r0    @ 080d8ace 0443
LAB_080d8ad0:
    cmp r4,#0x1                              @ 080d8ad0 012c
    beq LAB_080d8b22                         @ 080d8ad2 26d0
    ldr r2, DAT_080d8b08                     @ 080d8ad4 0c4a
    adds r6,r6,r2    @ 080d8ad6 b618
LAB_080d8ad8:
    ldr r0,[r7,#0x0]                         @ 080d8ad8 3868
    lsls r0,r0,#0x19    @ 080d8ada 4006
    lsrs r0,r0,#0x19    @ 080d8adc 400e
    adds r1,r4,#0x0    @ 080d8ade 211c
    bl build_pack_card_select_slot_data      @ 080d8ae0 fff72cfd
    adds r1,r0,#0x0    @ 080d8ae4 011c
    cmp r1,#0x0                              @ 080d8ae6 0029
    beq LAB_080d8b0c                         @ 080d8ae8 10d0
    ldr r0,[r6,#0x0]                         @ 080d8aea 3068
    movs r2,#0x1    @ 080d8aec 0122
    bl shuffle_pack_card_select_slots        @ 080d8aee fff709fe
    subs r5,#0x1    @ 080d8af2 013d
    ldr r0,[r6,#0x0]                         @ 080d8af4 3068
    adds r0,#0x4    @ 080d8af6 0430
    str r0,[r6,#0x0]                         @ 080d8af8 3060
    b LAB_080d8b22                           @ 080d8afa 12e0
DAT_080d8afc:
    .word  pack_ui_state                  @ 080d8afc 50580003
DAT_080d8b00:
    .word  0x000006fc                     @ 080d8b00 fc060000
DAT_080d8b04:
    .word  0x000006fa                     @ 080d8b04 fa060000
DAT_080d8b08:
    .word  0x00000704                     @ 080d8b08 04070000
LAB_080d8b0c:
    movs r0,#0xf0    @ 080d8b0c f020
    ldrb r1,[r7,#0x1]                        @ 080d8b0e 7978
    ands r0,r1    @ 080d8b10 0840
    cmp r0,#0x40                             @ 080d8b12 4028
    bne LAB_080d8b1c                         @ 080d8b14 02d1
    cmp r4,#0xf0                             @ 080d8b16 f02c
    bne LAB_080d8b1c                         @ 080d8b18 00d1
    movs r4,#0x10    @ 080d8b1a 1024
LAB_080d8b1c:
    lsrs r4,r4,#0x1    @ 080d8b1c 6408
    cmp r4,#0x1                              @ 080d8b1e 012c
    bne LAB_080d8ad8                         @ 080d8b20 dad1
LAB_080d8b22:
    cmp r5,#0x0                              @ 080d8b22 002d
    beq LAB_080d8b4a                         @ 080d8b24 11d0
    ldr r0,[r7,#0x0]                         @ 080d8b26 3868
    lsls r0,r0,#0x19    @ 080d8b28 4006
    lsrs r0,r0,#0x19    @ 080d8b2a 400e
    movs r1,#0x1    @ 080d8b2c 0121
    bl build_pack_card_select_slot_data      @ 080d8b2e fff705fd
    adds r1,r0,#0x0    @ 080d8b32 011c
    movs r4,#0xdf    @ 080d8b34 df24
    lsls r4,r4,#0x3    @ 080d8b36 e400
    add r4,r8                                @ 080d8b38 4444
    ldr r0,[r4,#0x0]                         @ 080d8b3a 2068
    adds r2,r5,#0x0    @ 080d8b3c 2a1c
    bl shuffle_pack_card_select_slots        @ 080d8b3e fff7e1fd
    lsls r1,r5,#0x2    @ 080d8b42 a900
    ldr r0,[r4,#0x0]                         @ 080d8b44 2068
    adds r0,r0,r1    @ 080d8b46 4018
    str r0,[r4,#0x0]                         @ 080d8b48 2060
LAB_080d8b4a:
    ldr r0,[r7,#0x0]                         @ 080d8b4a 3868
    lsls r0,r0,#0x19    @ 080d8b4c 4006
    lsrs r0,r0,#0x19    @ 080d8b4e 400e
    bl get_pack_info_attr2                   @ 080d8b50 03f0f8ff
    adds r5,r0,#0x0    @ 080d8b54 051c
    cmp r5,#0x0                              @ 080d8b56 002d
    beq LAB_080d8b9e                         @ 080d8b58 21d0
    movs r0,#0xdf    @ 080d8b5a df20
    lsls r0,r0,#0x3    @ 080d8b5c c000
    add r0,r8                                @ 080d8b5e 4044
    lsls r1,r5,#0x2    @ 080d8b60 a900
    ldr r0,[r0,#0x0]                         @ 080d8b62 0068
    subs r6,r0,r1    @ 080d8b64 461a
    movs r7,#0x0    @ 080d8b66 0027
LAB_080d8b68:
    bl tick_prng_lcg_rand15                  @ 080d8b68 20f0c4f9
    lsls r0,r0,#0x10    @ 080d8b6c 0004
    lsrs r0,r0,#0x10    @ 080d8b6e 000c
    adds r1,r5,#0x0    @ 080d8b70 291c
    bl get_bios_div_remainder                @ 080d8b72 35f045fc
    adds r4,r0,#0x0    @ 080d8b76 041c
    bl tick_prng_lcg_rand15                  @ 080d8b78 20f0bcf9
    lsls r0,r0,#0x10    @ 080d8b7c 0004
    lsrs r0,r0,#0x10    @ 080d8b7e 000c
    adds r1,r5,#0x0    @ 080d8b80 291c
    bl get_bios_div_remainder                @ 080d8b82 35f03dfc
    lsls r4,r4,#0x2    @ 080d8b86 a400
    adds r4,r4,r6    @ 080d8b88 a419
    ldr r2,[r4,#0x0]                         @ 080d8b8a 2268
    lsls r0,r0,#0x2    @ 080d8b8c 8000
    adds r0,r0,r6    @ 080d8b8e 8019
    ldr r1,[r0,#0x0]                         @ 080d8b90 0168
    str r1,[r4,#0x0]                         @ 080d8b92 2160
    str r2,[r0,#0x0]                         @ 080d8b94 0260
    adds r7,#0x1    @ 080d8b96 0137
    ldr r0, DAT_080d8bd4                     @ 080d8b98 0e48
    cmp r7,r0                                @ 080d8b9a 8742
    bls LAB_080d8b68                         @ 080d8b9c e4d9
LAB_080d8b9e:
    ldr r1, DAT_080d8bd8                     @ 080d8b9e 0e49
    add r1,r8                                @ 080d8ba0 4144
    ldrh r0,[r1,#0x0]                        @ 080d8ba2 0888
    adds r0,#0x1    @ 080d8ba4 0130
    strh r0,[r1,#0x0]                        @ 080d8ba6 0880
    lsls r0,r0,#0x10    @ 080d8ba8 0004
    lsrs r0,r0,#0x10    @ 080d8baa 000c
    .hword 0x4642    @ 080d8bac 4246
    ldrh r2,[r2,#0xa]                        @ 080d8bae 5289
    cmp r0,r2                                @ 080d8bb0 9042
    bne LAB_080d8bbe                         @ 080d8bb2 04d1
    ldr r1, DAT_080d8bdc                     @ 080d8bb4 0949
    movs r0,#0x4    @ 080d8bb6 0420
    strh r0,[r1,#0x10]                       @ 080d8bb8 0882
    movs r0,#0x1    @ 080d8bba 0120
    .hword 0x4681    @ 080d8bbc 8146
LAB_080d8bbe:
    movs r0,#0x0    @ 080d8bbe 0020
    bl tick_overlay_animation_step           @ 080d8bc0 04f010fd
    .hword 0x4648    @ 080d8bc4 4846
    pop {r3,r4}                              @ 080d8bc6 18bc
    .hword 0x4698    @ 080d8bc8 9846
    .hword 0x46a1    @ 080d8bca a146
    pop {r4,r5,r6,r7}                        @ 080d8bcc f0bc
    pop {r1}                                 @ 080d8bce 02bc
    bx r1                                    @ 080d8bd0 0847
    .zero  0x2
DAT_080d8bd4:
    .word  0x000003e7                     @ 080d8bd4 e7030000
DAT_080d8bd8:
    .word  0x000006ee                     @ 080d8bd8 ee060000
DAT_080d8bdc:
    .word  pack_ui_state                  @ 080d8bdc 50580003

@ Called during the pack card purchase finalization phase by the frame driver (indeg=0, Sub-type A), completing deal, coin deduction, and puzzle WRAM initialization. Iterates all card slots (count from pack[+0xa]); for each slot calls apply_delta_to_hand_oam_entry to update hand OAM (card-into-hand effect); if slot bit3=1, writes EWRAM card ownership flag (byte at 0x02000006+card_id*2+1, bit4 set to 1); after all slots, calls deduct_money_clamped to deduct coins (price from pack data [+0xc]), init_puzzle_wram_and_checksum and init_puzzle_wram_then_copy to initialize puzzle state; writes pack_ui_state[+0x6ee]=0, [+0xdf<<3] := [+0x6f4] reveal data pointer, [r1,+0x22]=0x3c; calls tick_overlay_animation_step(0); writes pack_ui_state[+0x10]=5 to advance state. Returns fixed 1.
@ 
@ Constants:
@ - PACK_DATA_OFFSET = 0x6fc (DAT_080d8c1c, pack data pointer)
@ - SLOT_COUNT_FIELD = pack[+0xa] (ldrh r1,[r1,#0xa])
@ - HAND_FLAG_OFFSET = 0xe0<<3 = 0x700 (pack_ui_state[+0x700])
@ - EWRAM_CARD_TABLE = 0x02000006 (DAT_080d8cb8, card ownership flag base)
@ - CARD_FLAG_BIT = 0x10 (bit4 of byte at EWRAM_CARD_TABLE[card_id*2+1])
@ - REVEAL_COUNT_CLEAR = 0x6ee (DAT_080d8cbc, clear reveal count)
@ - REVEAL_DATA_OFFSET = 0x6f4 (DAT_080d8cc0)
@ - AOB_SLOT_STRIDE = 4 (4 bytes per card slot)
@ - DEAL_COUNTER = 0x3c (strh 0x3c,[r1,#0x22])
@ - NEXT_STATE = 5 (strh 5,[pack_ui_state,#0x10])
finalize_pack_deal:
    push {r4,r5,r6,r7,lr}                    @ 080d8be0 f0b5
    .hword 0x4657    @ 080d8be2 5746
    .hword 0x464e    @ 080d8be4 4e46
    .hword 0x4645    @ 080d8be6 4546
    push {r5,r6,r7}                          @ 080d8be8 e0b4
    ldr r0, DAT_080d8c18                     @ 080d8bea 0b48
    movs r1,#0xc    @ 080d8bec 0c21
    adds r1,r1,r0    @ 080d8bee 0918
    .hword 0x468a    @ 080d8bf0 8a46
    ldr r2, DAT_080d8c1c                     @ 080d8bf2 0a4a
    adds r1,r0,r2    @ 080d8bf4 8118
    ldr r5,[r1,#0x0]                         @ 080d8bf6 0d68
    movs r1,#0xe0    @ 080d8bf8 e021
    lsls r1,r1,#0x3    @ 080d8bfa c900
    adds r0,r0,r1    @ 080d8bfc 4018
    ldr r4,[r0,#0x0]                         @ 080d8bfe 0468
    movs r2,#0x0    @ 080d8c00 0022
    .hword 0x4691    @ 080d8c02 9146
    movs r0,#0x0    @ 080d8c04 0020
    .hword 0x4651    @ 080d8c06 5146
    ldrh r1,[r1,#0xa]                        @ 080d8c08 4989
    cmp r9,r1                                @ 080d8c0a 8945
    bcs LAB_080d8c6c                         @ 080d8c0c 2ed2
LAB_080d8c0e:
    movs r6,#0x0    @ 080d8c0e 0026
    adds r2,r5,#0x4    @ 080d8c10 2a1d
    .hword 0x4690    @ 080d8c12 9046
    adds r7,r0,#0x1    @ 080d8c14 471c
    b LAB_080d8c52                           @ 080d8c16 1ce0
DAT_080d8c18:
    .word  pack_ui_state                  @ 080d8c18 50580003
DAT_080d8c1c:
    .word  0x000006fc                     @ 080d8c1c fc060000
LAB_080d8c20:
    ldr r0,[r4,#0x0]                         @ 080d8c20 2068
    lsls r0,r0,#0x10    @ 080d8c22 0004
    lsrs r0,r0,#0x14    @ 080d8c24 000d
    movs r1,#0x1    @ 080d8c26 0121
    bl apply_delta_to_hand_oam_entry         @ 080d8c28 20f014fa
    movs r0,#0x8    @ 080d8c2c 0820
    ldrb r1,[r4,#0x0]                        @ 080d8c2e 2178
    ands r0,r1    @ 080d8c30 0840
    cmp r0,#0x0                              @ 080d8c32 0028
    beq LAB_080d8c4a                         @ 080d8c34 09d0
    ldr r0,[r4,#0x0]                         @ 080d8c36 2068
    lsls r0,r0,#0x10    @ 080d8c38 0004
    lsrs r0,r0,#0x14    @ 080d8c3a 000d
    lsls r0,r0,#0x1    @ 080d8c3c 4000
    ldr r1, DAT_080d8cb8                     @ 080d8c3e 1e49
    adds r0,r0,r1    @ 080d8c40 4018
    movs r1,#0x10    @ 080d8c42 1021
    ldrb r2,[r0,#0x1]                        @ 080d8c44 4278
    orrs r1,r2    @ 080d8c46 1143
    strb r1,[r0,#0x1]                        @ 080d8c48 4170
LAB_080d8c4a:
    movs r0,#0x1    @ 080d8c4a 0120
    add r9,r0                                @ 080d8c4c 8144
    adds r4,#0x4    @ 080d8c4e 0434
    adds r6,#0x1    @ 080d8c50 0136
LAB_080d8c52:
    ldr r0,[r5,#0x0]                         @ 080d8c52 2868
    lsls r0,r0,#0x19    @ 080d8c54 4006
    lsrs r0,r0,#0x19    @ 080d8c56 400e
    bl get_pack_info_attr2                   @ 080d8c58 03f074ff
    cmp r6,r0                                @ 080d8c5c 8642
    bcc LAB_080d8c20                         @ 080d8c5e dfd3
    .hword 0x4645    @ 080d8c60 4546
    adds r0,r7,#0x0    @ 080d8c62 381c
    .hword 0x4651    @ 080d8c64 5146
    ldrh r1,[r1,#0xa]                        @ 080d8c66 4989
    cmp r0,r1                                @ 080d8c68 8842
    bcc LAB_080d8c0e                         @ 080d8c6a d0d3
LAB_080d8c6c:
    .hword 0x4652    @ 080d8c6c 5246
    ldr r0,[r2,#0xc]                         @ 080d8c6e d068
    bl deduct_money_clamped                  @ 080d8c70 20f06ef9
    bl init_puzzle_wram_and_checksum         @ 080d8c74 20f0f8ff
    bl init_puzzle_wram_then_copy            @ 080d8c78 21f006f8
    ldr r1, DAT_080d8cbc                     @ 080d8c7c 0f49
    add r1,r10                               @ 080d8c7e 5144
    movs r0,#0x0    @ 080d8c80 0020
    strh r0,[r1,#0x0]                        @ 080d8c82 0880
    movs r1,#0xdf    @ 080d8c84 df21
    lsls r1,r1,#0x3    @ 080d8c86 c900
    add r1,r10                               @ 080d8c88 5144
    ldr r0, DAT_080d8cc0                     @ 080d8c8a 0d48
    add r0,r10                               @ 080d8c8c 5044
    ldr r0,[r0,#0x0]                         @ 080d8c8e 0068
    str r0,[r1,#0x0]                         @ 080d8c90 0860
    movs r0,#0xf0    @ 080d8c92 f020
    lsls r0,r0,#0x6    @ 080d8c94 8001
    movs r0,#0x3c    @ 080d8c96 3c20
    .hword 0x4651    @ 080d8c98 5146
    strh r0,[r1,#0x22]                       @ 080d8c9a 4884
    movs r0,#0x0    @ 080d8c9c 0020
    bl tick_overlay_animation_step           @ 080d8c9e 04f0a1fc
    ldr r1, DAT_080d8cc4                     @ 080d8ca2 0849
    movs r0,#0x5    @ 080d8ca4 0520
    strh r0,[r1,#0x10]                       @ 080d8ca6 0882
    movs r0,#0x1    @ 080d8ca8 0120
    pop {r3,r4,r5}                           @ 080d8caa 38bc
    .hword 0x4698    @ 080d8cac 9846
    .hword 0x46a1    @ 080d8cae a146
    .hword 0x46aa    @ 080d8cb0 aa46
    pop {r4,r5,r6,r7}                        @ 080d8cb2 f0bc
    pop {r1}                                 @ 080d8cb4 02bc
    bx r1                                    @ 080d8cb6 0847
DAT_080d8cb8:
    .word  0x02000006                     @ 080d8cb8 06000002
DAT_080d8cbc:
    .word  0x000006ee                     @ 080d8cbc ee060000
DAT_080d8cc0:
    .word  0x000006f4                     @ 080d8cc0 f4060000
DAT_080d8cc4:
    .word  pack_ui_state                  @ 080d8cc4 50580003

@ Called each frame during the pack card deal delay phase by the frame driver, decrementing the deal delay timer and advancing state when it reaches zero. Reads pack_ui_state[+0x22] (deal delay count), decrements by 1 and writes back; if the count decrements to 0 (lsls r0,#0x10; cmp r0,#0 zero detection), writes pack_ui_state[+0x4]=6 to advance to the next state and returns 1; otherwise returns 0. Calls tick_overlay_animation_step(0) each frame to advance the overlay animation.
@ 
@ Constants:
@ - DEAL_COUNTER_OFFSET = +0x22 (ldrh/strh at [r1,#0x22])
@ - NEXT_STATE = 6 (strh r0,[r1,#0x4] = 6)
@ - pack_ui_state base = 0x03005850
tick_pack_deal_countdown:
    push {r4,lr}                             @ 080d8cc8 10b5
    ldr r0, DAT_080d8cf4                     @ 080d8cca 0a48
    adds r1,r0,#0x0    @ 080d8ccc 011c
    adds r1,#0xc    @ 080d8cce 0c31
    movs r4,#0x0    @ 080d8cd0 0024
    ldrh r0,[r1,#0x22]                       @ 080d8cd2 488c
    subs r0,#0x1    @ 080d8cd4 0138
    strh r0,[r1,#0x22]                       @ 080d8cd6 4884
    lsls r0,r0,#0x10    @ 080d8cd8 0004
    cmp r0,#0x0                              @ 080d8cda 0028
    bne LAB_080d8ce4                         @ 080d8cdc 02d1
    movs r0,#0x6    @ 080d8cde 0620
    strh r0,[r1,#0x4]                        @ 080d8ce0 8880
    movs r4,#0x1    @ 080d8ce2 0124
LAB_080d8ce4:
    movs r0,#0x0    @ 080d8ce4 0020
    bl tick_overlay_animation_step           @ 080d8ce6 04f07dfc
    adds r0,r4,#0x0    @ 080d8cea 201c
    pop {r4}                                 @ 080d8cec 10bc
    pop {r1}                                 @ 080d8cee 02bc
    bx r1                                    @ 080d8cf0 0847
    .zero  0x2
DAT_080d8cf4:
    .word  pack_ui_state                  @ 080d8cf4 50580003

@ Called during the pack scene fade-out end phase by the frame driver (indeg=0, Sub-type A). Calls tick_overlay_animation_step(1) to advance the overlay fade-out animation; if the animation completes this frame (returns 1), reads DISPCNT (0x04000000) and clears bit12 (AND with 0xffffefff), writes back to DISPCNT to disable an OBJ/BG display layer; then writes pack_ui_state[+0x10]=7 to advance the state machine. Returns 0 (animation in progress) or 1 (complete; Sub-case E r4 passthrough).
@ 
@ Constants:
@ - DISPCNT_MASK = 0xffffefff (DAT_080d8d24, clears bit12)
@ - DISPCNT = 0x80<<0x13 = 0x04000000
@ - NEXT_STATE = 7 (strh 7,[pack_ui_state,#0x10])
@ - ANIM_MODE = 1 (tick_overlay_animation_step(1) = fade-out mode)
tick_pack_overlay_fadeout:
    push {r4,lr}                             @ 080d8cf8 10b5
    movs r4,#0x0    @ 080d8cfa 0024
    movs r0,#0x1    @ 080d8cfc 0120
    bl tick_overlay_animation_step           @ 080d8cfe 04f071fc
    cmp r0,#0x1                              @ 080d8d02 0128
    bne LAB_080d8d1a                         @ 080d8d04 09d1
    movs r2,#0x80    @ 080d8d06 8022
    lsls r2,r2,#0x13    @ 080d8d08 d204
    ldr r0, DAT_080d8d24                     @ 080d8d0a 0648
    ldrh r1,[r2,#0x0]                        @ 080d8d0c 1188
    ands r0,r1    @ 080d8d0e 0840
    strh r0,[r2,#0x0]                        @ 080d8d10 1080
    ldr r1, DAT_080d8d28                     @ 080d8d12 0549
    movs r0,#0x7    @ 080d8d14 0720
    strh r0,[r1,#0x10]                       @ 080d8d16 0882
    movs r4,#0x1    @ 080d8d18 0124
LAB_080d8d1a:
    adds r0,r4,#0x0    @ 080d8d1a 201c
    pop {r4}                                 @ 080d8d1c 10bc
    pop {r1}                                 @ 080d8d1e 02bc
    bx r1                                    @ 080d8d20 0847
    .zero  0x2
DAT_080d8d24:
    .word  0xffffefff                     @ 080d8d24 ffefffff
DAT_080d8d28:
    .word  pack_ui_state                  @ 080d8d28 50580003

@ Writes initialization flags for the pack card-flip display scene. Sets pack_ui_state[+0xe]=3 (step counter initial value), then clears bits 0..1 of pack_ui_state[0x724+0x0] (INIT_BIT cleared = animation not yet initialized). Returns 1. Called via indirect function-pointer table by duel_puzzle scene dispatcher as scene-switch init action.
@ 
@ Constants:
@ - pack_ui_state=0x03005850
@ - CARD_STATE_OFFSET=0x724 // offset to card state struct within pack_ui_state
@ - STEP_INIT=3 // initial step counter value written to [+0xe]
@ - INIT_BIT_MASK=0x3 // bit0..1: initialization flags (cleared)
set_pack_card_state_init_flag:
    ldr r0, DAT_080d8d44                     @ 080d8d2c 0548
    movs r1,#0x3    @ 080d8d2e 0321
    strh r1,[r0,#0xe]                        @ 080d8d30 c181
    ldr r1, DAT_080d8d48                     @ 080d8d32 0549
    adds r0,r0,r1    @ 080d8d34 4018
    movs r1,#0x3    @ 080d8d36 0321
    rsbs r1,r1,#0    @ 080d8d38 4942
    ldrb r2,[r0,#0x0]                        @ 080d8d3a 0278
    ands r1,r2    @ 080d8d3c 1140
    strb r1,[r0,#0x0]                        @ 080d8d3e 0170
    movs r0,#0x1    @ 080d8d40 0120
    bx lr                                    @ 080d8d42 7047
DAT_080d8d44:
    .word  pack_ui_state                  @ 080d8d44 50580003
DAT_080d8d48:
    .word  0x00000724                     @ 080d8d48 24070000

@ Duel-puzzle scene frame-step driver. Reads current step from pack_ui_state+0xc[+0x4], looks up handler in fn-ptr table 0x09e49480, calls it via invoke_r0. If handler returns nonzero, increments step counter. Returns 0 while running, 1 when step ends or scene complete (null ptr). Symmetric to tick_pack_card_select_step (0x080d8504); uses different table (0x09e49480 vs 0x09e49438). FUN_080db448 case 2.
@ 
@ Constants:
@ - FN_TABLE=0x09e49480 // duel_puzzle scene step fn-ptr table
@ - pack_ui_state=0x03005850
tick_pack_duel_puzzle_step:
    push {r4,lr}                             @ 080d8d4c 10b5
    ldr r0, DAT_080d8d74                     @ 080d8d4e 0948
    adds r4,r0,#0x0    @ 080d8d50 041c
    adds r4,#0xc    @ 080d8d52 0c34
    ldr r1, DAT_080d8d78                     @ 080d8d54 0849
    ldrh r2,[r4,#0x4]                        @ 080d8d56 a288
    lsls r0,r2,#0x2    @ 080d8d58 9000
    adds r0,r0,r1    @ 080d8d5a 4018
    ldr r0,[r0,#0x0]                         @ 080d8d5c 0068
    cmp r0,#0x0                              @ 080d8d5e 0028
    beq LAB_080d8d7c                         @ 080d8d60 0cd0
    bl invoke_r0                             @ 080d8d62 35f031fc
    cmp r0,#0x0                              @ 080d8d66 0028
    beq LAB_080d8d70                         @ 080d8d68 02d0
    ldrh r0,[r4,#0x4]                        @ 080d8d6a a088
    adds r0,#0x1    @ 080d8d6c 0130
    strh r0,[r4,#0x4]                        @ 080d8d6e a080
LAB_080d8d70:
    movs r0,#0x0    @ 080d8d70 0020
    b LAB_080d8d7e                           @ 080d8d72 04e0
DAT_080d8d74:
    .word  pack_ui_state                  @ 080d8d74 50580003
DAT_080d8d78:
    .word  0x09e49480                     @ 080d8d78 8094e409
LAB_080d8d7c:
    movs r0,#0x1    @ 080d8d7c 0120
LAB_080d8d7e:
    pop {r4}                                 @ 080d8d7e 10bc
    pop {r1}                                 @ 080d8d80 02bc
    bx r1                                    @ 080d8d82 0847

@ pack-banner: BG0CNT=0x1C00, BG2CNT=0x1E0D, 清空 VRAM screenblocks
pack_list_bg_setup:
    push {r4,lr}                             @ 080d8d84 10b5
    ldr r1, PTR_BG0CNT_080d8dc8              @ 080d8d86 1049
    movs r0,#0xe0    @ 080d8d88 e020
    lsls r0,r0,#0x5    @ 080d8d8a 4001
    strh r0,[r1,#0x0]                        @ 080d8d8c 0880
    adds r1,#0x4    @ 080d8d8e 0431
    ldr r0, DAT_080d8dcc                     @ 080d8d90 0e48
    strh r0,[r1,#0x0]                        @ 080d8d92 0880
    movs r0,#0xc0    @ 080d8d94 c020
    lsls r0,r0,#0x13    @ 080d8d96 c004
    movs r1,#0x80    @ 080d8d98 8021
    lsls r1,r1,#0x7    @ 080d8d9a c901
    bl zero_fill_halfword_wrapper            @ 080d8d9c 1cf07cf8
    ldr r0, DAT_080d8dd0                     @ 080d8da0 0b48
    movs r4,#0x80    @ 080d8da2 8024
    lsls r4,r4,#0x4    @ 080d8da4 2401
    adds r1,r4,#0x0    @ 080d8da6 211c
    bl zero_fill_halfword_wrapper            @ 080d8da8 1cf076f8
    ldr r0, DAT_080d8dd4                     @ 080d8dac 0948
    movs r1,#0x80    @ 080d8dae 8021
    lsls r1,r1,#0x5    @ 080d8db0 4901
    bl zero_fill_halfword_wrapper            @ 080d8db2 1cf071f8
    ldr r0, DAT_080d8dd8                     @ 080d8db6 0848
    adds r1,r4,#0x0    @ 080d8db8 211c
    bl zero_fill_halfword_wrapper            @ 080d8dba 1cf06df8
    bl reset_all_bg_scroll_regs_and_shadows  @ 080d8dbe 1cf063fe
    pop {r4}                                 @ 080d8dc2 10bc
    pop {r0}                                 @ 080d8dc4 01bc
    bx r0                                    @ 080d8dc6 0047
PTR_BG0CNT_080d8dc8:
    .word  BG0CNT                         @ 080d8dc8 08000004
DAT_080d8dcc:
    .word  0x00001e0d                     @ 080d8dcc 0d1e0000
DAT_080d8dd0:
    .word  0x0600e000                     @ 080d8dd0 00e00006
DAT_080d8dd4:
    .word  0x0600d000                     @ 080d8dd4 00d00006
DAT_080d8dd8:
    .word  0x0600f000                     @ 080d8dd8 00f00006

@ pack-banner: 返回当前可见 pack 数 (clamp 1..5)
pack_visible_count:
    ldr r0, DAT_080d8df4                     @ 080d8ddc 0548
    ldrh r1,[r0,#0x14]                       @ 080d8dde 818a
    ldrh r2,[r0,#0x2a]                       @ 080d8de0 428d
    subs r0,r1,r2    @ 080d8de2 881a
    cmp r0,#0x1                              @ 080d8de4 0128
    bge LAB_080d8dea                         @ 080d8de6 00da
    movs r0,#0x1    @ 080d8de8 0120
LAB_080d8dea:
    cmp r0,#0x5                              @ 080d8dea 0528
    ble LAB_080d8df0                         @ 080d8dec 00dd
    movs r0,#0x5    @ 080d8dee 0520
LAB_080d8df0:
    bx lr                                    @ 080d8df0 7047
    .zero  0x2
DAT_080d8df4:
    .word  pack_ui_state                  @ 080d8df4 50580003

@ Computes pixel X coordinate for a pack slot in the horizontal scroll area based on pack_visible_count and slot index r0. When pack_visible_count==5 uses wide spacing: base=0x2b00, step=0x2680; otherwise uses narrow: base=0xba00/(count+1), step=0x1b00. Result X = (base + index * step) >> 8, distributing pack icons evenly across screen width.
@ 
@ Constants:
@ - WIDE_BASE=0x2b00 // 5-pack mode base offset (0xac<<6)
@ - WIDE_STEP=0x2680 // 5-pack mode step (0x9a00/4)
@ - NARROW_DIVISOR=0xba00 // non-5-pack numerator
@ - NARROW_BASE_ADD=0x1b00 // non-5-pack base addend (0xd8<<5)
@ - SHIFT=8 // final result right shift 8 bits to pixels
compute_pack_slot_scroll_x:
    push {r4,r5,lr}                          @ 080d8df8 30b5
    adds r4,r0,#0x0    @ 080d8dfa 041c
    bl pack_visible_count                    @ 080d8dfc fff7eeff
    adds r1,r0,#0x0    @ 080d8e00 011c
    subs r0,r1,#0x1    @ 080d8e02 481e
    cmp r0,r4                                @ 080d8e04 a042
    bls LAB_080d8e0a                         @ 080d8e06 00d9
    adds r0,r4,#0x0    @ 080d8e08 201c
LAB_080d8e0a:
    adds r4,r0,#0x0    @ 080d8e0a 041c
    cmp r1,#0x5                              @ 080d8e0c 0529
    bne LAB_080d8e20                         @ 080d8e0e 07d1
    movs r5,#0xac    @ 080d8e10 ac25
    lsls r5,r5,#0x6    @ 080d8e12 ad01
    movs r0,#0x9a    @ 080d8e14 9a20
    lsls r0,r0,#0x8    @ 080d8e16 0002
    movs r1,#0x4    @ 080d8e18 0421
    bl bios_div                              @ 080d8e1a 35f0effa
    b LAB_080d8e30                           @ 080d8e1e 07e0
LAB_080d8e20:
    movs r0,#0xba    @ 080d8e20 ba20
    lsls r0,r0,#0x8    @ 080d8e22 0002
    adds r1,#0x1    @ 080d8e24 0131
    bl bios_div                              @ 080d8e26 35f0e9fa
    movs r1,#0xd8    @ 080d8e2a d821
    lsls r1,r1,#0x5    @ 080d8e2c 4901
    adds r5,r0,r1    @ 080d8e2e 4518
LAB_080d8e30:
    muls r0,r4    @ 080d8e30 6043
    adds r0,r5,r0    @ 080d8e32 2818
    lsrs r0,r0,#0x8    @ 080d8e34 000a
    pop {r4,r5}                              @ 080d8e36 30bc
    pop {r1}                                 @ 080d8e38 02bc
    bx r1                                    @ 080d8e3a 0847

@ Returns vertical pixel Y coordinate for a pack icon based on direction parameter r0. r0=0 returns 0x28=40 (upper area), r0=1 returns 0x78=120 (lower area). Values >=2 use the same 0x28 path. Used in OAM attr0 Y field to position pack icons vertically on screen.
@ 
@ Constants:
@ - Y_TOP=0x28 // 40 pixels: upper pack icon Y coordinate
@ - Y_BOT=0x78 // 120 pixels: lower pack icon Y coordinate
get_pack_icon_y_by_dir:
    cmp r0,#0x0                              @ 080d8e3c 0028
    beq LAB_080d8e44                         @ 080d8e3e 01d0
    cmp r0,#0x1                              @ 080d8e40 0128
    beq LAB_080d8e48                         @ 080d8e42 01d0
LAB_080d8e44:
    movs r0,#0x28    @ 080d8e44 2820
    b LAB_080d8e4a                           @ 080d8e46 00e0
LAB_080d8e48:
    movs r0,#0x78    @ 080d8e48 7820
LAB_080d8e4a:
    bx lr                                    @ 080d8e4a 7047

@ Updates pixel X scroll coordinates for all visible pack slots in the pack-select UI. Reads pack_ui_state+0xc layout, iterates pack_visible_count slots. For each slot calls compute_pack_slot_scroll_x(slot_i) and writes result to slot[+0x2]. Also sets slot[+0x4]=pack_y_value and slot[+0xe]=0x100 (disable affine). Called by pack list scene state machine each frame to refresh slot positions.
@ 
@ Constants:
@ - pack_ui_state=0x03005850
@ - SLOT_STRIDE=0x20 // each slot struct is 32 bytes
@ - OBJ_ATTR_DISABLE=0x0100 // written to slot[+0xe]: OAM attr1 disable-affine bit
@ - SLOT_Y_OFFSET=0x50 // movs r0,#0x50 -> r8, default Y value
update_pack_slot_scroll_positions:
    push {r4,r5,r6,r7,lr}                    @ 080d8e4c f0b5
    .hword 0x4647    @ 080d8e4e 4746
    push {r7}                                @ 080d8e50 80b4
    ldr r1, DAT_080d8e94                     @ 080d8e52 1049
    adds r1,#0xc    @ 080d8e54 0c31
    ldrh r2,[r1,#0x1e]                       @ 080d8e56 ca8b
    lsls r0,r2,#0x5    @ 080d8e58 5001
    adds r0,#0x44    @ 080d8e5a 4430
    adds r4,r0,r1    @ 080d8e5c 4418
    bl pack_visible_count                    @ 080d8e5e fff7bdff
    adds r6,r0,#0x0    @ 080d8e62 061c
    movs r5,#0x0    @ 080d8e64 0025
    cmp r5,r6                                @ 080d8e66 b542
    bcs LAB_080d8e88                         @ 080d8e68 0ed2
    movs r0,#0x50    @ 080d8e6a 5020
    .hword 0x4680    @ 080d8e6c 8046
    movs r7,#0x80    @ 080d8e6e 8027
    lsls r7,r7,#0x1    @ 080d8e70 7f00
LAB_080d8e72:
    adds r0,r5,#0x0    @ 080d8e72 281c
    bl compute_pack_slot_scroll_x            @ 080d8e74 fff7c0ff
    strh r0,[r4,#0x2]                        @ 080d8e78 6080
    .hword 0x4642    @ 080d8e7a 4246
    strh r2,[r4,#0x4]                        @ 080d8e7c a280
    strh r7,[r4,#0xe]                        @ 080d8e7e e781
    adds r4,#0x20    @ 080d8e80 2034
    adds r5,#0x1    @ 080d8e82 0135
    cmp r5,r6                                @ 080d8e84 b542
    bcc LAB_080d8e72                         @ 080d8e86 f4d3
LAB_080d8e88:
    pop {r3}                                 @ 080d8e88 08bc
    .hword 0x4698    @ 080d8e8a 9846
    pop {r4,r5,r6,r7}                        @ 080d8e8c f0bc
    pop {r0}                                 @ 080d8e8e 01bc
    bx r0                                    @ 080d8e90 0047
    .zero  0x2
DAT_080d8e94:
    .word  pack_ui_state                  @ 080d8e94 50580003

@ pack-banner: 逐 pack 初始化 (banner tile + name text + detail)
pack_entry_init:
    push {r4,r5,r6,lr}                       @ 080d8e98 70b5
    adds r1,r0,#0x0    @ 080d8e9a 011c
    ldr r2, DAT_080d8ef8                     @ 080d8e9c 164a
    adds r2,#0xc    @ 080d8e9e 0c32
    ldr r4, DAT_080d8efc                     @ 080d8ea0 164c
    movs r0,#0x8    @ 080d8ea2 0820
    rsbs r0,r0,#0    @ 080d8ea4 4042
    ands r4,r0    @ 080d8ea6 0440
    ldrh r0,[r2,#0x1e]                       @ 080d8ea8 d08b
    lsls r5,r0,#0x5    @ 080d8eaa 4501
    adds r5,#0x44    @ 080d8eac 4435
    adds r5,r5,r2    @ 080d8eae ad18
    lsls r0,r1,#0x5    @ 080d8eb0 4801
    adds r5,r5,r0    @ 080d8eb2 2d18
    ldr r6, DAT_080d8f00                     @ 080d8eb4 124e
    adds r0,r1,#0x0    @ 080d8eb6 081c
    muls r0,r6    @ 080d8eb8 7043
    adds r4,r4,r0    @ 080d8eba 2418
    ldrh r0,[r5,#0x0]                        @ 080d8ebc 2888
    bl pack_banner_obj_setup                 @ 080d8ebe 00f043f8
    adds r0,r4,#0x0    @ 080d8ec2 201c
    adds r1,r6,#0x0    @ 080d8ec4 311c
    bl zero_fill_halfword_wrapper            @ 080d8ec6 1bf0e7ff
    adds r0,r4,#0x0    @ 080d8eca 201c
    adds r0,#0x8    @ 080d8ecc 0830
    ldrh r1,[r5,#0x0]                        @ 080d8ece 2988
    bl pack_name_text_render                 @ 080d8ed0 02f076fe
    strh r0,[r4,#0x0]                        @ 080d8ed4 2080
    ldr r0, DAT_080d8f04                     @ 080d8ed6 0b48
    adds r4,r4,r0    @ 080d8ed8 2418
    ldrh r1,[r5,#0x0]                        @ 080d8eda 2988
    adds r0,r4,#0x0    @ 080d8edc 201c
    bl render_pack_label_name_to_sprite_vram @ 080d8ede 03f02ff8
    movs r0,#0xd0    @ 080d8ee2 d020
    lsls r0,r0,#0x2    @ 080d8ee4 8000
    adds r4,r4,r0    @ 080d8ee6 2418
    ldrh r1,[r5,#0x0]                        @ 080d8ee8 2988
    ldrh r2,[r5,#0x1a]                       @ 080d8eea 6a8b
    adds r0,r4,#0x0    @ 080d8eec 201c
    bl render_pack_card_count_to_sprite_vram @ 080d8eee 03f0d3f8
    pop {r4,r5,r6}                           @ 080d8ef2 70bc
    pop {r0}                                 @ 080d8ef4 01bc
    bx r0                                    @ 080d8ef6 0047
DAT_080d8ef8:
    .word  pack_ui_state                  @ 080d8ef8 50580003
DAT_080d8efc:
    .word  0x02029eb7                     @ 080d8efc b79e0202
DAT_080d8f00:
    .word  0x00001288                     @ 080d8f00 88120000
DAT_080d8f04:
    .word  0x00000c08                     @ 080d8f04 080c0000

@ pack-banner: 从 0x09CCE2B0/C0/D0 加载 BG tilemap + BG palette
pack_list_tilemap_load:
    push {lr}                                @ 080d8f08 00b5
    ldr r0, DAT_080d8f30                     @ 080d8f0a 0948
    ldr r0,[r0,#0x4]                         @ 080d8f0c 4068
    ldr r1, DAT_080d8f34                     @ 080d8f0e 0949
    bl bios_huff_uncomp                      @ 080d8f10 35f082fa
    ldr r0, DAT_080d8f38                     @ 080d8f14 0848
    ldr r0,[r0,#0x4]                         @ 080d8f16 4068
    ldr r1, DAT_080d8f3c                     @ 080d8f18 0849
    bl bios_huff_uncomp                      @ 080d8f1a 35f07dfa
    ldr r0, DAT_080d8f40                     @ 080d8f1e 0848
    ldr r1, DAT_080d8f44                     @ 080d8f20 0849
    ldr r1,[r1,#0x4]                         @ 080d8f22 4968
    movs r2,#0x20    @ 080d8f24 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d8f26 1bf0efff
    pop {r0}                                 @ 080d8f2a 01bc
    bx r0                                    @ 080d8f2c 0047
    .zero  0x2
DAT_080d8f30:
    .word  0x09cce2b0                     @ 080d8f30 b0e2cc09
DAT_080d8f34:
    .word  0x0600d000                     @ 080d8f34 00d00006
DAT_080d8f38:
    .word  0x09cce2d0                     @ 080d8f38 d0e2cc09
DAT_080d8f3c:
    .word  0x0600f000                     @ 080d8f3c 00f00006
DAT_080d8f40:
    .word  0x050001a0                     @ 080d8f40 a0010005
DAT_080d8f44:
    .word  0x09cce2c0                     @ 080d8f44 c0e2cc09

@ pack-banner: 按 slot 计算 OBJ VRAM 地址, 调 pack_banner_tile_copy
pack_banner_obj_setup:
    push {r4,r5,r6,lr}                       @ 080d8f48 70b5
    adds r6,r0,#0x0    @ 080d8f4a 061c
    adds r4,r1,#0x0    @ 080d8f4c 0c1c
    ldr r5, DAT_080d8f80                     @ 080d8f4e 0c4d
    cmp r4,#0x4                              @ 080d8f50 042c
    bls LAB_080d8f56                         @ 080d8f52 00d9
    movs r4,#0x4    @ 080d8f54 0424
LAB_080d8f56:
    adds r0,r4,#0x0    @ 080d8f56 201c
    movs r1,#0x4    @ 080d8f58 0421
    bl get_bios_div_remainder                @ 080d8f5a 35f051fa
    lsls r0,r0,#0x8    @ 080d8f5e 0002
    adds r5,r0,r5    @ 080d8f60 4519
    adds r0,r4,#0x0    @ 080d8f62 201c
    movs r1,#0x4    @ 080d8f64 0421
    bl bios_div                              @ 080d8f66 35f049fa
    lsls r0,r0,#0xd    @ 080d8f6a 4003
    adds r5,r5,r0    @ 080d8f6c 2d18
    adds r0,r6,#0x0    @ 080d8f6e 301c
    adds r1,r5,#0x0    @ 080d8f70 291c
    movs r2,#0x0    @ 080d8f72 0022
    movs r3,#0x1    @ 080d8f74 0123
    bl pack_banner_tile_copy                 @ 080d8f76 02f073fc
    pop {r4,r5,r6}                           @ 080d8f7a 70bc
    pop {r0}                                 @ 080d8f7c 01bc
    bx r0                                    @ 080d8f7e 0047
DAT_080d8f80:
    .word  0x06014000                     @ 080d8f80 00400106

@ pack-banner: EWRAM 记录 → BG VRAM 0x06000240, 含 pack cost
pack_detail_bg_tile_load:
    push {r4,r5,lr}                          @ 080d8f84 30b5
    adds r2,r0,#0x0    @ 080d8f86 021c
    ldr r0, DAT_080d8f9c                     @ 080d8f88 0448
    adds r5,r0,#0x0    @ 080d8f8a 051c
    adds r5,#0xc    @ 080d8f8c 0c35
    ldr r0, DAT_080d8fa0                     @ 080d8f8e 0448
    cmp r2,r0                                @ 080d8f90 8242
    bne LAB_080d8fa8                         @ 080d8f92 09d1
    ldr r0, DAT_080d8fa4                     @ 080d8f94 0348
    bl zero_fill_pack_obj_vram_region        @ 080d8f96 02f00bfe
    b LAB_080d8fd6                           @ 080d8f9a 1ce0
DAT_080d8f9c:
    .word  pack_ui_state                  @ 080d8f9c 50580003
DAT_080d8fa0:
    .word  0x0000ffff                     @ 080d8fa0 ffff0000
DAT_080d8fa4:
    .word  0x06000240                     @ 080d8fa4 40020006
LAB_080d8fa8:
    ldr r1, DAT_080d8fdc                     @ 080d8fa8 0c49
    movs r0,#0x8    @ 080d8faa 0820
    rsbs r0,r0,#0    @ 080d8fac 4042
    ands r1,r0    @ 080d8fae 0140
    ldr r0, DAT_080d8fe0                     @ 080d8fb0 0b48
    muls r0,r2    @ 080d8fb2 5043
    adds r1,r1,r0    @ 080d8fb4 0918
    ldrh r0,[r1,#0x0]                        @ 080d8fb6 0888
    movs r4,#0x0    @ 080d8fb8 0024
    strh r0,[r5,#0x10]                       @ 080d8fba 2882
    adds r1,#0x8    @ 080d8fbc 0831
    ldr r0, DAT_080d8fe4                     @ 080d8fbe 0948
    movs r2,#0xc0    @ 080d8fc0 c022
    lsls r2,r2,#0x4    @ 080d8fc2 1201
    bl copy_words_aligned                    @ 080d8fc4 1bf084ff
    strh r4,[r5,#0x12]                       @ 080d8fc8 6c82
    ldr r0, DAT_080d8fe8                     @ 080d8fca 0748
    movs r1,#0x12    @ 080d8fcc 1221
    movs r2,#0xf    @ 080d8fce 0f22
    movs r3,#0x0    @ 080d8fd0 0023
    bl write_pack_obj_tile_strip             @ 080d8fd2 02f059fe
LAB_080d8fd6:
    pop {r4,r5}                              @ 080d8fd6 30bc
    pop {r0}                                 @ 080d8fd8 01bc
    bx r0                                    @ 080d8fda 0047
DAT_080d8fdc:
    .word  0x02029eb7                     @ 080d8fdc b79e0202
DAT_080d8fe0:
    .word  0x00001288                     @ 080d8fe0 88120000
DAT_080d8fe4:
    .word  0x06000240                     @ 080d8fe4 40020006
DAT_080d8fe8:
    .word  0x0600e000                     @ 080d8fe8 00e00006

@ Called by the pack scene scroll frame driver (0x080d9c38) each frame to update the scroll angle field and conditionally rewrite the OBJ tile strip. Reads pack_ui_state[+0x10] angle value; if >0x1e, uses bits[15:8] of [+0x12] as the reference phase; otherwise phase is 0. Adds 8 to [+0x12] and takes modulo 0x3000 via bios_div_remainder, writing back to [+0x12]; if the resulting phase byte (bits[15:8]) differs from the saved reference phase, calls write_pack_obj_tile_strip(0x0600e000, 0x12, 0xf) to write 15 columns of OBJ tiles. Returns void (Pattern B: pop{r0};bx r0, no independent r0 write).
@ 
@ Constants:
@ - ANGLE_THRESHOLD = 0x1e (cmp r0,#0x1e = 30 frame threshold)
@ - ANGLE_STEP = 8 (adds r0,#0x8 = per-frame step)
@ - ANGLE_MOD = 0xc0<<6 = 0x3000 (movs r1,#0xc0; lsls r1,#6; 192<<6=12288=0x3000)
@ - OBJ_VRAM_BASE = 0x0600e000 (DAT_080d903c)
@ - TILE_START = 0x12 (movs r1,#0x12)
@ - TILE_COUNT = 0xf (movs r2,#0xf)
@ - ANGLE_OFFSET = +0x12 (ldrh/strh [r4,#0x12])
@ - COUNT_OFFSET = +0x10 (ldrh [r4,#0x10])
tick_pack_scroll_angle_strip:
    push {r4,r5,lr}                          @ 080d8fec 30b5
    ldr r0, DAT_080d9000                     @ 080d8fee 0448
    adds r4,r0,#0x0    @ 080d8ff0 041c
    adds r4,#0xc    @ 080d8ff2 0c34
    ldrh r0,[r4,#0x10]                       @ 080d8ff4 208a
    cmp r0,#0x1e                             @ 080d8ff6 1e28
    bls LAB_080d9004                         @ 080d8ff8 04d9
    ldrh r0,[r4,#0x12]                       @ 080d8ffa 608a
    lsrs r5,r0,#0x8    @ 080d8ffc 050a
    b LAB_080d9008                           @ 080d8ffe 03e0
DAT_080d9000:
    .word  pack_ui_state                  @ 080d9000 50580003
LAB_080d9004:
    movs r5,#0x0    @ 080d9004 0025
    ldrh r0,[r4,#0x12]                       @ 080d9006 608a
LAB_080d9008:
    adds r0,#0x8    @ 080d9008 0830
    strh r0,[r4,#0x12]                       @ 080d900a 6082
    ldrh r0,[r4,#0x12]                       @ 080d900c 608a
    movs r1,#0xc0    @ 080d900e c021
    lsls r1,r1,#0x6    @ 080d9010 8901
    bl get_bios_div_remainder                @ 080d9012 35f0f5f9
    strh r0,[r4,#0x12]                       @ 080d9016 6082
    ldrh r4,[r4,#0x10]                       @ 080d9018 248a
    cmp r4,#0x1e                             @ 080d901a 1e2c
    bls LAB_080d9024                         @ 080d901c 02d9
    lsls r0,r0,#0x10    @ 080d901e 0004
    lsrs r3,r0,#0x18    @ 080d9020 030e
    b LAB_080d9026                           @ 080d9022 00e0
LAB_080d9024:
    movs r3,#0x0    @ 080d9024 0023
LAB_080d9026:
    cmp r5,r3                                @ 080d9026 9d42
    beq LAB_080d9034                         @ 080d9028 04d0
    ldr r0, DAT_080d903c                     @ 080d902a 0448
    movs r1,#0x12    @ 080d902c 1221
    movs r2,#0xf    @ 080d902e 0f22
    bl write_pack_obj_tile_strip             @ 080d9030 02f02afe
LAB_080d9034:
    pop {r4,r5}                              @ 080d9034 30bc
    pop {r0}                                 @ 080d9036 01bc
    bx r0                                    @ 080d9038 0047
    .zero  0x2
DAT_080d903c:
    .word  0x0600e000                     @ 080d903c 00e00006

@ Writes pack banner graphic tiles to OBJ VRAM row A (base 0x06000e40). If r0=0xffff (invalid slot), calls zero_fill_pack_obj_vram_row_a to clear the region. Otherwise computes source offset as 0x02029eb7 + slot_id*0x1288 + 0x0c08, calls copy_words_aligned to copy 0xd0*4=0x340 bytes of tile data, then calls fill_pack_obj_tile_region_13col (tile_id=0x72, cols=15) to write background fill tiles.
@ 
@ Constants:
@ - VRAM_ROW_A=0x06000e40 // OBJ VRAM row A base address
@ - SRC_BASE=0x02029eb7 // EWRAM pack graphic source data base
@ - SLOT_STRIDE=0x1288 // per-slot graphic data stride
@ - SRC_OFFSET=0x0c08 // intra-slot source offset for row A
@ - WORD_COUNT=0x340 // bytes to copy (0xd0 words)
@ - FILL_TILE=0x72 // tile ID passed to fill_pack_obj_tile_region_13col
@ - FILL_COLS=0xf // number of columns to fill
render_pack_banner_tile_row_a:
    push {lr}                                @ 080d9040 00b5
    adds r2,r0,#0x0    @ 080d9042 021c
    ldr r0, DAT_080d9054                     @ 080d9044 0348
    cmp r2,r0                                @ 080d9046 8242
    bne LAB_080d905c                         @ 080d9048 08d1
    ldr r0, DAT_080d9058                     @ 080d904a 0348
    bl zero_fill_pack_obj_vram_row_a         @ 080d904c 02f070ff
    b LAB_080d9082                           @ 080d9050 17e0
    .zero  0x2
DAT_080d9054:
    .word  0x0000ffff                     @ 080d9054 ffff0000
DAT_080d9058:
    .word  0x06000e40                     @ 080d9058 400e0006
LAB_080d905c:
    ldr r1, DAT_080d9088                     @ 080d905c 0a49
    movs r0,#0x8    @ 080d905e 0820
    rsbs r0,r0,#0    @ 080d9060 4042
    ands r1,r0    @ 080d9062 0140
    ldr r0, DAT_080d908c                     @ 080d9064 0948
    muls r0,r2    @ 080d9066 5043
    adds r1,r1,r0    @ 080d9068 0918
    ldr r0, DAT_080d9090                     @ 080d906a 0948
    adds r1,r1,r0    @ 080d906c 0918
    ldr r0, DAT_080d9094                     @ 080d906e 0948
    movs r2,#0xd0    @ 080d9070 d022
    lsls r2,r2,#0x2    @ 080d9072 9200
    bl copy_words_aligned                    @ 080d9074 1bf02cff
    ldr r0, DAT_080d9098                     @ 080d9078 0748
    movs r1,#0x72    @ 080d907a 7221
    movs r2,#0xf    @ 080d907c 0f22
    bl fill_pack_obj_tile_region_13col       @ 080d907e 02f0ebff
LAB_080d9082:
    pop {r0}                                 @ 080d9082 01bc
    bx r0                                    @ 080d9084 0047
    .zero  0x2
DAT_080d9088:
    .word  0x02029eb7                     @ 080d9088 b79e0202
DAT_080d908c:
    .word  0x00001288                     @ 080d908c 88120000
DAT_080d9090:
    .word  0x00000c08                     @ 080d9090 080c0000
DAT_080d9094:
    .word  0x06000e40                     @ 080d9094 400e0006
DAT_080d9098:
    .word  0x0600e084                     @ 080d9098 84e00006

@ Writes pack banner graphic tiles to OBJ VRAM row B (base 0x06001180). Fully symmetric to render_pack_banner_tile_row_a (0x080d9040): if r0=0xffff calls zero_fill_pack_obj_vram_row_b; otherwise computes source as 0x02029eb7 + slot_id*0x1288 + 0x0f48, copies 0x340 bytes via copy_words_aligned, then calls fill_pack_obj_tile_region_13col_b (tile_id=0x8c, cols=15).
@ 
@ Constants:
@ - VRAM_ROW_B=0x06001180 // OBJ VRAM row B base address
@ - SRC_BASE=0x02029eb7 // EWRAM pack graphic source data base
@ - SLOT_STRIDE=0x1288 // per-slot graphic data stride
@ - SRC_OFFSET_B=0x0f48 // intra-slot source offset for row B
@ - WORD_COUNT=0x340 // bytes to copy
@ - FILL_TILE=0x8c // tile ID passed to fill_pack_obj_tile_region_13col_b
@ - FILL_COLS=0xf // number of columns to fill
render_pack_banner_tile_row_b:
    push {lr}                                @ 080d909c 00b5
    adds r2,r0,#0x0    @ 080d909e 021c
    ldr r0, DAT_080d90b0                     @ 080d90a0 0348
    cmp r2,r0                                @ 080d90a2 8242
    bne LAB_080d90b8                         @ 080d90a4 08d1
    ldr r0, DAT_080d90b4                     @ 080d90a6 0348
    bl zero_fill_pack_obj_vram_row_b         @ 080d90a8 02f0eeff
    b LAB_080d90de                           @ 080d90ac 17e0
    .zero  0x2
DAT_080d90b0:
    .word  0x0000ffff                     @ 080d90b0 ffff0000
DAT_080d90b4:
    .word  0x06001180                     @ 080d90b4 80110006
LAB_080d90b8:
    ldr r1, DAT_080d90e4                     @ 080d90b8 0a49
    movs r0,#0x8    @ 080d90ba 0820
    rsbs r0,r0,#0    @ 080d90bc 4042
    ands r1,r0    @ 080d90be 0140
    ldr r0, DAT_080d90e8                     @ 080d90c0 0948
    muls r0,r2    @ 080d90c2 5043
    adds r1,r1,r0    @ 080d90c4 0918
    movs r2,#0xd0    @ 080d90c6 d022
    lsls r2,r2,#0x2    @ 080d90c8 9200
    ldr r0, DAT_080d90ec                     @ 080d90ca 0848
    adds r1,r1,r0    @ 080d90cc 0918
    ldr r0, DAT_080d90f0                     @ 080d90ce 0848
    bl copy_words_aligned                    @ 080d90d0 1bf0fefe
    ldr r0, DAT_080d90f4                     @ 080d90d4 0748
    movs r1,#0x8c    @ 080d90d6 8c21
    movs r2,#0xf    @ 080d90d8 0f22
    bl fill_pack_obj_tile_region_13col_b     @ 080d90da 03f06df8
LAB_080d90de:
    pop {r0}                                 @ 080d90de 01bc
    bx r0                                    @ 080d90e0 0047
    .zero  0x2
DAT_080d90e4:
    .word  0x02029eb7                     @ 080d90e4 b79e0202
DAT_080d90e8:
    .word  0x00001288                     @ 080d90e8 88120000
DAT_080d90ec:
    .word  0x00000f48                     @ 080d90ec 480f0000
DAT_080d90f0:
    .word  0x06001180                     @ 080d90f0 80110006
DAT_080d90f4:
    .word  0x0600e09e                     @ 080d90f4 9ee00006

@ Writes pack detail panel card-attribute graphics to OBJ VRAM info region (base 0x060014c0). If r0=0xffff calls zero_fill_pack_info_obj_vram to clear; otherwise calls render_pack_card_stat_byte_to_sprite to render card attribute byte as sprite data, then calls fill_pack_obj_tile_region_17col (tile_id=0xa6, cols=15) to write background fill. Third member of pack OBJ VRAM write cluster (row_a + row_b + info).
@ 
@ Constants:
@ - VRAM_INFO=0x060014c0 // pack info OBJ VRAM base address
@ - FILL_TILE=0xa6 // tile ID passed to fill_pack_obj_tile_region_17col
@ - FILL_COLS=0xf // number of columns to fill
render_pack_info_stat_tile_row:
    push {lr}                                @ 080d90f8 00b5
    ldr r1, DAT_080d9108                     @ 080d90fa 0349
    cmp r0,r1                                @ 080d90fc 8842
    bne LAB_080d9110                         @ 080d90fe 07d1
    ldr r0, DAT_080d910c                     @ 080d9100 0248
    bl zero_fill_pack_info_obj_vram          @ 080d9102 03f071f8
    b LAB_080d9120                           @ 080d9106 0be0
DAT_080d9108:
    .word  0x0000ffff                     @ 080d9108 ffff0000
DAT_080d910c:
    .word  0x060014c0                     @ 080d910c c0140006
LAB_080d9110:
    ldr r0, DAT_080d9124                     @ 080d9110 0448
    bl render_pack_card_stat_byte_to_sprite  @ 080d9112 03f071f8
    ldr r0, DAT_080d9128                     @ 080d9116 0448
    movs r1,#0xa6    @ 080d9118 a621
    movs r2,#0xf    @ 080d911a 0f22
    bl fill_pack_obj_tile_region_17col       @ 080d911c 03f006f9
LAB_080d9120:
    pop {r0}                                 @ 080d9120 01bc
    bx r0                                    @ 080d9122 0047
DAT_080d9124:
    .word  0x060014c0                     @ 080d9124 c0140006
DAT_080d9128:
    .word  0x0600e404                     @ 080d9128 04e40006

@ Called by pack_list_page_init during pack shop page init. Iterates all visible pack slots (pack_visible_count), for each slot with count > 0 renders the stock number to BG tile VRAM. First zeros two OBJ VRAM regions (0x06017ac0 and 0x06017ac0+0x400) and IWRAM state bytes ([0x02006ed0+0x15], [+0x08], [+0x14]), then sets up font_jp config and calls render_decimal_digits_jp x2 (two digit rows), finally write_line_buf_to_bg_tile_vram commits to BG.
@ 
@ Constants:
@ - OBJ_VRAM_BASE=0x06017ac0 // digit graphic OBJ VRAM start
@ - OBJ_VRAM_STRIDE=0x400 // second region offset (0x80<<3=0x400)
@ - STATE_ADDR=0x02006ed0 // IWRAM font state struct base
@ - TILE_BASE_HALFWORD=0x8002 // digit tile render parameter
render_pack_slot_counts_to_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 080d912c f0b5
    ldr r4, DAT_080d91cc                     @ 080d912e 274c
    adds r4,#0xc    @ 080d9130 0c34
    bl pack_visible_count                    @ 080d9132 fff753fe
    adds r7,r0,#0x0    @ 080d9136 071c
    ldrh r1,[r4,#0x1e]                       @ 080d9138 e18b
    lsls r0,r1,#0x5    @ 080d913a 4801
    adds r0,#0x44    @ 080d913c 4430
    adds r5,r0,r4    @ 080d913e 0519
    ldr r6, DAT_080d91d0                     @ 080d9140 234e
    ldr r2, DAT_080d91d4                     @ 080d9142 244a
    movs r0,#0x2    @ 080d9144 0220
    rsbs r0,r0,#0    @ 080d9146 4042
    ldrb r3,[r2,#0x15]                       @ 080d9148 537d
    ands r0,r3    @ 080d914a 1840
    strb r0,[r2,#0x15]                       @ 080d914c 5075
    movs r1,#0x3    @ 080d914e 0321
    rsbs r1,r1,#0    @ 080d9150 4942
    ldrb r0,[r2,#0x8]                        @ 080d9152 107a
    ands r1,r0    @ 080d9154 0140
    strb r1,[r2,#0x8]                        @ 080d9156 1172
    movs r0,#0x7d    @ 080d9158 7d20
    rsbs r0,r0,#0    @ 080d915a 4042
    ldrb r3,[r2,#0x14]                       @ 080d915c 137d
    ands r0,r3    @ 080d915e 1840
    strb r0,[r2,#0x14]                       @ 080d9160 1075
    ldr r0, PTR_font_jp_base_table_080d91d8  @ 080d9162 1d48
    lsls r1,r1,#0x1f    @ 080d9164 c907
    lsrs r1,r1,#0x1f    @ 080d9166 c90f
    lsls r1,r1,#0x3    @ 080d9168 c900
    adds r1,r1,r0    @ 080d916a 0918
    ldr r0,[r1,#0x0]                         @ 080d916c 0868
    str r0,[r2,#0x4]                         @ 080d916e 5060
    movs r4,#0xa0    @ 080d9170 a024
    lsls r4,r4,#0x1    @ 080d9172 6400
    adds r0,r6,#0x0    @ 080d9174 301c
    adds r1,r4,#0x0    @ 080d9176 211c
    bl zero_fill_halfword_wrapper            @ 080d9178 1bf08efe
    movs r0,#0x80    @ 080d917c 8020
    lsls r0,r0,#0x3    @ 080d917e c000
    adds r0,r6,r0    @ 080d9180 3018
    adds r1,r4,#0x0    @ 080d9182 211c
    bl zero_fill_halfword_wrapper            @ 080d9184 1bf088fe
    movs r4,#0x0    @ 080d9188 0024
    cmp r4,r7                                @ 080d918a bc42
    bcs LAB_080d91c6                         @ 080d918c 1bd2
LAB_080d918e:
    ldrh r0,[r5,#0x18]                       @ 080d918e 288b
    cmp r0,#0x0                              @ 080d9190 0028
    beq LAB_080d91bc                         @ 080d9192 13d0
    movs r0,#0x2    @ 080d9194 0220
    movs r1,#0x2    @ 080d9196 0221
    bl setup_line_buf_pos_and_font           @ 080d9198 17f00cfd
    ldrh r3,[r5,#0x18]                       @ 080d919c 2b8b
    movs r0,#0x8    @ 080d919e 0820
    movs r1,#0x2    @ 080d91a0 0221
    ldr r2, DAT_080d91dc                     @ 080d91a2 0e4a
    bl render_decimal_digits_jp              @ 080d91a4 19f072fd
    ldrh r3,[r5,#0x18]                       @ 080d91a8 2b8b
    movs r0,#0x8    @ 080d91aa 0820
    movs r1,#0x2    @ 080d91ac 0221
    movs r2,#0x6    @ 080d91ae 0622
    bl render_decimal_digits_jp              @ 080d91b0 19f06cfd
    adds r0,r6,#0x0    @ 080d91b4 301c
    movs r1,#0x0    @ 080d91b6 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d91b8 1af00cfb
LAB_080d91bc:
    adds r6,#0x40    @ 080d91bc 4036
    adds r5,#0x20    @ 080d91be 2035
    adds r4,#0x1    @ 080d91c0 0134
    cmp r4,r7                                @ 080d91c2 bc42
    bcc LAB_080d918e                         @ 080d91c4 e3d3
LAB_080d91c6:
    pop {r4,r5,r6,r7}                        @ 080d91c6 f0bc
    pop {r0}                                 @ 080d91c8 01bc
    bx r0                                    @ 080d91ca 0047
DAT_080d91cc:
    .word  pack_ui_state                  @ 080d91cc 50580003
DAT_080d91d0:
    .word  0x06017ac0                     @ 080d91d0 c07a0106
DAT_080d91d4:
    .word  0x02006ed0                     @ 080d91d4 d06e0002
PTR_font_jp_base_table_080d91d8:
    .word  font_jp_base_table             @ 080d91d8 54f8e509
DAT_080d91dc:
    .word  0x00008002                     @ 080d91dc 02800000

@ Called during pack list page initialization and rendering by two callers (0x080d971c = pack_list_page_init; 0x080da974 contains tick_overlay_animation_step/init_pack_scroll_animation). Calls render_pack_label_str13f1_to_bg_vram(0x350) to render the first label string to BG VRAM; calls render_pack_label_str1390_to_bg_vram(0x390) to render the second label string; finally calls copy_pack_card_palette_to_obj_pal(0xb) to copy the card palette to OBJ palette slot 11. Sibling of render_pack_info_label_sprites_and_palette (0x080d713c) with different render offsets (0x350/0x390 vs 0x140/0x180).
@ 
@ Constants:
@ - LABEL_VRAM_OFFSET_0 = 0xd4<<2 = 0x350 (first label render offset)
@ - LABEL_VRAM_OFFSET_1 = 0x350+0x40 = 0x390 (second label render offset)
@ - OBJ_PAL_SLOT = 0xb
render_pack_list_label_sprites_and_palette:
    push {r4,lr}                             @ 080d91e0 10b5
    movs r4,#0xd4    @ 080d91e2 d424
    lsls r4,r4,#0x2    @ 080d91e4 a400
    adds r0,r4,#0x0    @ 080d91e6 201c
    bl render_pack_label_str13f1_to_bg_vram  @ 080d91e8 03f072fb
    adds r4,#0x40    @ 080d91ec 4034
    adds r0,r4,#0x0    @ 080d91ee 201c
    bl render_pack_label_str1390_to_bg_vram  @ 080d91f0 03f09afb
    movs r0,#0xb    @ 080d91f4 0b20
    bl copy_pack_card_palette_to_obj_pal     @ 080d91f6 03f0f9f9
    pop {r4}                                 @ 080d91fa 10bc
    pop {r0}                                 @ 080d91fc 01bc
    bx r0                                    @ 080d91fe 0047

@ Writes a square-form pack-banner OBJ entry into OAM. r0=tile_index, r1=y_half_packed (high16=Y_top, low16=Y_bot), r2=dir_flags. Computes column/row offsets from tile_index mod/div 4, clamps dir_flags to [0..3], assembles attr0/attr1/attr2, calls write_oam_entry_with_tile_inc. Symmetric sibling to write_pack_banner_oam_entry_stacked (0x080d925c) which uses write_pack_obj_attr_by_dir_stacked.
@ 
@ Constants:
@ - OAM_BASE=0x000080c0 // OAM attr0/attr1 base value
@ - TILE_DIV=4 // tile_index mod/div base
@ - Y_ADJUST=-0x10 // Y coordinate adjustment
@ - Y_ADJUST2=-0x20 // high Y adjustment
write_pack_banner_oam_entry_sq:
    push {r4,r5,r6,r7,lr}                    @ 080d9200 f0b5
    adds r6,r0,#0x0    @ 080d9202 061c
    adds r4,r1,#0x0    @ 080d9204 0c1c
    adds r7,r2,#0x0    @ 080d9206 171c
    movs r1,#0x4    @ 080d9208 0421
    bl get_bios_div_remainder                @ 080d920a 35f0f9f8
    adds r5,r0,#0x0    @ 080d920e 051c
    adds r0,r6,#0x0    @ 080d9210 301c
    movs r1,#0x4    @ 080d9212 0421
    bl bios_div                              @ 080d9214 35f0f2f8
    lsls r5,r5,#0x3    @ 080d9218 ed00
    lsls r0,r0,#0x8    @ 080d921a 0002
    movs r1,#0x80    @ 080d921c 8021
    lsls r1,r1,#0x2    @ 080d921e 8900
    adds r0,r0,r1    @ 080d9220 4018
    adds r5,r5,r0    @ 080d9222 2d18
    adds r0,r4,#0x0    @ 080d9224 201c
    subs r0,#0x10    @ 080d9226 1038
    lsls r0,r0,#0x10    @ 080d9228 0004
    lsrs r3,r0,#0x10    @ 080d922a 030c
    lsrs r4,r4,#0x10    @ 080d922c 240c
    subs r4,#0x20    @ 080d922e 203c
    lsls r4,r4,#0x10    @ 080d9230 2404
    lsrs r0,r4,#0x10    @ 080d9232 200c
    cmp r7,#0x3                              @ 080d9234 032f
    bls LAB_080d923a                         @ 080d9236 00d9
    movs r7,#0x3    @ 080d9238 0327
LAB_080d923a:
    lsls r0,r0,#0x10    @ 080d923a 0004
    orrs r3,r0    @ 080d923c 0343
    ldr r1, DAT_080d9258                     @ 080d923e 0649
    lsls r2,r7,#0xa    @ 080d9240 ba02
    lsrs r0,r5,#0x1    @ 080d9242 6808
    orrs r2,r0    @ 080d9244 0243
    lsls r2,r2,#0x10    @ 080d9246 1204
    lsrs r2,r2,#0x10    @ 080d9248 120c
    adds r0,r3,#0x0    @ 080d924a 181c
    bl write_oam_entry_with_tile_inc         @ 080d924c 1df000f9
    pop {r4,r5,r6,r7}                        @ 080d9250 f0bc
    pop {r0}                                 @ 080d9252 01bc
    bx r0                                    @ 080d9254 0047
    .zero  0x2
DAT_080d9258:
    .word  0x000080c0                     @ 080d9258 c0800000

@ Writes a stacked-form pack-banner OBJ entry into OAM. r0=tile_index, r1=y_packed (low16=Y_top, high16=Y_bot), r2=oam_attr1 (skip guard + forwarded), r3=dir_flags. Skips if tile_index % 4 == 0. Otherwise computes attr0/attr1/attr2, calls write_pack_obj_attr_by_dir_stacked. r2 loaded from slot struct+0xe (OAM attr1 field, typical value 0x0100=disable-affine); used as cmp r4,#0 skip gate then forwarded via lsls r3,r4,#0x10. Symmetric sibling to write_pack_banner_oam_entry_sq (0x080d9200).
@ 
@ Constants:
@ - OAM_BASE=0x000080c0 // OAM attribute base value
@ - TILE_DIV=4 // tile mod/div base
write_pack_banner_oam_entry_stacked:
    push {r4,r5,r6,r7,lr}                    @ 080d925c f0b5
    .hword 0x4647    @ 080d925e 4746
    push {r7}                                @ 080d9260 80b4
    adds r5,r0,#0x0    @ 080d9262 051c
    adds r7,r1,#0x0    @ 080d9264 0f1c
    .hword 0x4690    @ 080d9266 9046
    adds r6,r3,#0x0    @ 080d9268 1e1c
    movs r1,#0x4    @ 080d926a 0421
    bl get_bios_div_remainder                @ 080d926c 35f0c8f8
    adds r4,r0,#0x0    @ 080d9270 041c
    adds r0,r5,#0x0    @ 080d9272 281c
    movs r1,#0x4    @ 080d9274 0421
    bl bios_div                              @ 080d9276 35f0c1f8
    lsls r4,r4,#0x3    @ 080d927a e400
    lsls r0,r0,#0x8    @ 080d927c 0002
    movs r1,#0x80    @ 080d927e 8021
    lsls r1,r1,#0x2    @ 080d9280 8900
    adds r0,r0,r1    @ 080d9282 4018
    adds r3,r4,r0    @ 080d9284 2318
    .hword 0x4644    @ 080d9286 4446
    cmp r4,#0x0                              @ 080d9288 002c
    beq LAB_080d92b6                         @ 080d928a 14d0
    cmp r6,#0x3                              @ 080d928c 032e
    bls LAB_080d9292                         @ 080d928e 00d9
    movs r6,#0x3    @ 080d9290 0326
LAB_080d9292:
    adds r0,r7,#0x0    @ 080d9292 381c
    subs r0,#0x10    @ 080d9294 1038
    lsls r0,r0,#0x10    @ 080d9296 0004
    lsrs r0,r0,#0x10    @ 080d9298 000c
    lsrs r1,r7,#0x10    @ 080d929a 390c
    subs r1,#0x20    @ 080d929c 2039
    lsls r1,r1,#0x10    @ 080d929e 0904
    orrs r0,r1    @ 080d92a0 0843
    ldr r1, DAT_080d92c0                     @ 080d92a2 0749
    lsls r2,r6,#0xa    @ 080d92a4 b202
    lsrs r3,r3,#0x1    @ 080d92a6 5b08
    orrs r2,r3    @ 080d92a8 1a43
    lsls r2,r2,#0x10    @ 080d92aa 1204
    lsrs r2,r2,#0x10    @ 080d92ac 120c
    .hword 0x4644    @ 080d92ae 4446
    lsls r3,r4,#0x10    @ 080d92b0 2304
    bl write_pack_obj_attr_by_dir_stacked    @ 080d92b2 1df00bfd
LAB_080d92b6:
    pop {r3}                                 @ 080d92b6 08bc
    .hword 0x4698    @ 080d92b8 9846
    pop {r4,r5,r6,r7}                        @ 080d92ba f0bc
    pop {r0}                                 @ 080d92bc 01bc
    bx r0                                    @ 080d92be 0047
DAT_080d92c0:
    .word  0x000080c0                     @ 080d92c0 c0800000

@ Called by pack list page frame drivers (indeg=17), iterates all visible pack slots and dispatches OAM writes based on each slot's attr field at [+0xe]. r0 = dir_flags [0..3], clamped then stored as r8=0x100 (sq type sentinel). Calls pack_visible_count to get visible slot count r7; for each slot (stepping 0x20 bytes) reads [r4+0xe]: 0 = skip; equal to 0x100 = calls write_pack_banner_oam_entry_sq(slot_idx, oam_attr, dir_flags); otherwise calls write_pack_banner_oam_entry_stacked(slot_idx, oam_attr, attr0xe, dir_flags). Returns void (Pattern B: pop{r0};bx r0).
@ 
@ Constants:
@ - DIR_FLAGS_MAX = 3 (cmp r6,#3; bls = clamp upper bound)
@ - SQ_SENTINEL = 0x80<<1 = 0x100 (movs r0,#0x80; lsls r0,#1; mov r8,r0 = sq type attr sentinel)
@ - SLOT_STRUCT_STRIDE = 0x20 (adds r4,#0x20 per slot)
@ - ATTR0E_OFFSET = 0xe (ldrsh r0,[r4,r1] r1=#0xe)
write_pack_banner_oam_for_all_slots:
    push {r4,r5,r6,r7,lr}                    @ 080d92c4 f0b5
    .hword 0x4647    @ 080d92c6 4746
    push {r7}                                @ 080d92c8 80b4
    adds r6,r0,#0x0    @ 080d92ca 061c
    ldr r1, DAT_080d9310                     @ 080d92cc 1049
    adds r1,#0xc    @ 080d92ce 0c31
    ldrh r2,[r1,#0x1e]                       @ 080d92d0 ca8b
    lsls r0,r2,#0x5    @ 080d92d2 5001
    adds r0,#0x44    @ 080d92d4 4430
    adds r4,r0,r1    @ 080d92d6 4418
    cmp r6,#0x3                              @ 080d92d8 032e
    bls LAB_080d92de                         @ 080d92da 00d9
    movs r6,#0x3    @ 080d92dc 0326
LAB_080d92de:
    bl pack_visible_count                    @ 080d92de fff77dfd
    adds r7,r0,#0x0    @ 080d92e2 071c
    movs r5,#0x0    @ 080d92e4 0025
    cmp r5,r7                                @ 080d92e6 bd42
    bcs LAB_080d9330                         @ 080d92e8 22d2
    movs r0,#0x80    @ 080d92ea 8020
    lsls r0,r0,#0x1    @ 080d92ec 4000
    .hword 0x4680    @ 080d92ee 8046
LAB_080d92f0:
    movs r1,#0xe    @ 080d92f0 0e21
    ldrsh r0,[r4,r1]                         @ 080d92f2 605e
    cmp r0,#0x0                              @ 080d92f4 0028
    beq LAB_080d9328                         @ 080d92f6 17d0
    cmp r0,r8                                @ 080d92f8 4045
    bne LAB_080d9314                         @ 080d92fa 0bd1
    ldrh r2,[r4,#0x4]                        @ 080d92fc a288
    lsls r1,r2,#0x10    @ 080d92fe 1104
    ldrh r0,[r4,#0x2]                        @ 080d9300 6088
    orrs r1,r0    @ 080d9302 0143
    adds r0,r5,#0x0    @ 080d9304 281c
    adds r2,r6,#0x0    @ 080d9306 321c
    bl write_pack_banner_oam_entry_sq        @ 080d9308 fff77aff
    b LAB_080d9328                           @ 080d930c 0ce0
    .zero  0x2
DAT_080d9310:
    .word  pack_ui_state                  @ 080d9310 50580003
LAB_080d9314:
    ldrh r2,[r4,#0x4]                        @ 080d9314 a288
    lsls r1,r2,#0x10    @ 080d9316 1104
    ldrh r0,[r4,#0x2]                        @ 080d9318 6088
    orrs r1,r0    @ 080d931a 0143
    movs r0,#0xe    @ 080d931c 0e20
    ldrsh r2,[r4,r0]                         @ 080d931e 225e
    adds r0,r5,#0x0    @ 080d9320 281c
    adds r3,r6,#0x0    @ 080d9322 331c
    bl write_pack_banner_oam_entry_stacked   @ 080d9324 fff79aff
LAB_080d9328:
    adds r4,#0x20    @ 080d9328 2034
    adds r5,#0x1    @ 080d932a 0135
    cmp r5,r7                                @ 080d932c bd42
    bcc LAB_080d92f0                         @ 080d932e dfd3
LAB_080d9330:
    pop {r3}                                 @ 080d9330 08bc
    .hword 0x4698    @ 080d9332 9846
    pop {r4,r5,r6,r7}                        @ 080d9334 f0bc
    pop {r0}                                 @ 080d9336 01bc
    bx r0                                    @ 080d9338 0047
    .zero  0x2

@ 每帧渲染拆包卡槽的高亮脉动 OAM 动画. r0 入参为渲染模式 (clamp 到 [0..3]). 读 pack_ui_state+0xc[+0x1e] 当前页索引算工作结构, 取 pack_visible_count 得可见卡数 (存 r9 作循环上界). 维护脉动计数 [+0x22] 在 0..0x1d 间循环递增, 据其前/后半段经 bios_div 算出正弦式偏移量. 对每个可见槽 (r9 个), 若槽 [+0x1c] bit0 活动则以 8.8 定点缩放 0x4080 (1.0) 调 write_pack_obj_attr_by_dir_split 写 OAM 仿射属性 (按方向拆分). 随后两次调 rotate_pixel_hue_in_buffer 对像素缓冲做色相旋转产生脉动光效, 并在 [+0x1e] 页非零时调 compute_pack_slot_scroll_x 取滚动 X. 供拆包场景多个帧驱动状态处理器 (10 个 caller) 每帧调用.
render_pack_card_highlight_pulse_by_mode:
    push {r4,r5,r6,r7,lr}                    @ 080d933c f0b5
    .hword 0x4657    @ 080d933e 5746
    .hword 0x464e    @ 080d9340 4e46
    .hword 0x4645    @ 080d9342 4546
    push {r5,r6,r7}                          @ 080d9344 e0b4
    .hword 0x4682    @ 080d9346 8246
    ldr r0, DAT_080d9394                     @ 080d9348 1248
    adds r6,r0,#0x0    @ 080d934a 061c
    adds r6,#0xc    @ 080d934c 0c36
    ldrh r1,[r6,#0x1e]                       @ 080d934e f18b
    lsls r0,r1,#0x5    @ 080d9350 4801
    adds r0,#0x44    @ 080d9352 4430
    adds r4,r0,r6    @ 080d9354 8419
    .hword 0x4652    @ 080d9356 5246
    cmp r2,#0x3                              @ 080d9358 032a
    bls LAB_080d9360                         @ 080d935a 01d9
    movs r3,#0x3    @ 080d935c 0323
    .hword 0x469a    @ 080d935e 9a46
LAB_080d9360:
    bl pack_visible_count                    @ 080d9360 fff73cfd
    .hword 0x4681    @ 080d9364 8146
    ldrh r0,[r6,#0x22]                       @ 080d9366 708c
    adds r0,#0x1    @ 080d9368 0130
    strh r0,[r6,#0x22]                       @ 080d936a 7084
    lsls r0,r0,#0x10    @ 080d936c 0004
    lsrs r0,r0,#0x10    @ 080d936e 000c
    cmp r0,#0x1d                             @ 080d9370 1d28
    bls LAB_080d9378                         @ 080d9372 01d9
    movs r0,#0x0    @ 080d9374 0020
    strh r0,[r6,#0x22]                       @ 080d9376 7084
LAB_080d9378:
    ldrh r0,[r6,#0x22]                       @ 080d9378 708c
    cmp r0,#0xe                              @ 080d937a 0e28
    bhi LAB_080d9398                         @ 080d937c 0cd8
    lsls r0,r0,#0x6    @ 080d937e 8001
    movs r1,#0xf    @ 080d9380 0f21
    bl bios_div                              @ 080d9382 35f03bf8
    movs r2,#0x80    @ 080d9386 8022
    lsls r2,r2,#0x1    @ 080d9388 5200
    adds r1,r2,#0x0    @ 080d938a 111c
    subs r1,r1,r0    @ 080d938c 091a
    lsls r1,r1,#0x10    @ 080d938e 0904
    lsrs r7,r1,#0x10    @ 080d9390 0f0c
    b LAB_080d93aa                           @ 080d9392 0ae0
DAT_080d9394:
    .word  pack_ui_state                  @ 080d9394 50580003
LAB_080d9398:
    ldrh r0,[r6,#0x22]                       @ 080d9398 708c
    subs r0,#0xf    @ 080d939a 0f38
    lsls r0,r0,#0x6    @ 080d939c 8001
    movs r1,#0xf    @ 080d939e 0f21
    bl bios_div                              @ 080d93a0 35f02cf8
    adds r0,#0xc0    @ 080d93a4 c030
    lsls r0,r0,#0x10    @ 080d93a6 0004
    lsrs r7,r0,#0x10    @ 080d93a8 070c
LAB_080d93aa:
    movs r5,#0x0    @ 080d93aa 0025
    cmp r5,r9                                @ 080d93ac 4d45
    bcs LAB_080d93f2                         @ 080d93ae 20d2
    .hword 0x4653    @ 080d93b0 5346
    lsls r0,r3,#0xa    @ 080d93b2 9802
    ldr r2, DAT_080d9428                     @ 080d93b4 1c4a
    adds r1,r2,#0x0    @ 080d93b6 111c
    orrs r0,r1    @ 080d93b8 0843
    lsls r0,r0,#0x10    @ 080d93ba 0004
    .hword 0x4680    @ 080d93bc 8046
    lsls r0,r7,#0x10    @ 080d93be 3804
    asrs r7,r0,#0x10    @ 080d93c0 0714
LAB_080d93c2:
    movs r0,#0x1    @ 080d93c2 0120
    ldrb r3,[r4,#0x1c]                       @ 080d93c4 237f
    ands r0,r3    @ 080d93c6 1840
    cmp r0,#0x0                              @ 080d93c8 0028
    beq LAB_080d93ea                         @ 080d93ca 0ed0
    ldrh r0,[r4,#0x2]                        @ 080d93cc 6088
    subs r0,#0x10    @ 080d93ce 1038
    ldrh r1,[r4,#0x4]                        @ 080d93d0 a188
    subs r1,#0x2e    @ 080d93d2 2e39
    lsls r0,r0,#0x10    @ 080d93d4 0004
    lsrs r0,r0,#0x10    @ 080d93d6 000c
    lsls r1,r1,#0x10    @ 080d93d8 0904
    orrs r0,r1    @ 080d93da 0843
    movs r1,#0x81    @ 080d93dc 8121
    lsls r1,r1,#0x7    @ 080d93de c901
    .hword 0x4643    @ 080d93e0 4346
    lsrs r2,r3,#0x10    @ 080d93e2 1a0c
    lsls r3,r7,#0x10    @ 080d93e4 3b04
    bl write_pack_obj_attr_by_dir_split      @ 080d93e6 1df081fa
LAB_080d93ea:
    adds r4,#0x20    @ 080d93ea 2034
    adds r5,#0x1    @ 080d93ec 0135
    cmp r5,r9                                @ 080d93ee 4d45
    bcc LAB_080d93c2                         @ 080d93f0 e7d3
LAB_080d93f2:
    ldr r0, DAT_080d942c                     @ 080d93f2 0e48
    ldr r4,[r0,#0x8]                         @ 080d93f4 8468
    adds r4,#0x12    @ 080d93f6 1234
    ldr r5, DAT_080d9430                     @ 080d93f8 0d4d
    ldrh r0,[r6,#0x22]                       @ 080d93fa 708c
    lsls r1,r0,#0x1    @ 080d93fc 4100
    adds r1,r1,r0    @ 080d93fe 0918
    lsls r0,r1,#0x4    @ 080d9400 0801
    subs r0,r0,r1    @ 080d9402 401a
    lsls r0,r0,#0x3    @ 080d9404 c000
    movs r1,#0x1e    @ 080d9406 1e21
    bl bios_div                              @ 080d9408 34f0f8ff
    adds r2,r0,#0x0    @ 080d940c 021c
    rsbs r2,r2,#0    @ 080d940e 5242
    lsls r2,r2,#0x10    @ 080d9410 1204
    movs r0,#0x7    @ 080d9412 0720
    orrs r2,r0    @ 080d9414 0243
    adds r0,r4,#0x0    @ 080d9416 201c
    adds r1,r5,#0x0    @ 080d9418 291c
    bl rotate_pixel_hue_in_buffer            @ 080d941a 04f037fb
    ldrh r1,[r6,#0x22]                       @ 080d941e 718c
    cmp r1,#0xe                              @ 080d9420 0e29
    bhi LAB_080d9434                         @ 080d9422 07d8
    lsls r0,r1,#0x3    @ 080d9424 c800
    b LAB_080d943c                           @ 080d9426 09e0
DAT_080d9428:
    .word  0x0000e30c                     @ 080d9428 0ce30000
DAT_080d942c:
    .word  0x09ce824c                     @ 080d942c 4c82ce09
DAT_080d9430:
    .word  0x050003d2                     @ 080d9430 d2030005
LAB_080d9434:
    movs r0,#0x1e    @ 080d9434 1e20
    ldrh r2,[r6,#0x22]                       @ 080d9436 728c
    subs r0,r0,r2    @ 080d9438 801a
    lsls r0,r0,#0x3    @ 080d943a c000
LAB_080d943c:
    movs r1,#0xf    @ 080d943c 0f21
    bl bios_div                              @ 080d943e 34f0ddff
    lsls r0,r0,#0x10    @ 080d9442 0004
    lsrs r7,r0,#0x10    @ 080d9444 070c
    ldr r0, DAT_080d94f4                     @ 080d9446 2b48
    ldr r4,[r0,#0x10]                        @ 080d9448 0469
    adds r4,#0x8    @ 080d944a 0834
    ldr r5, DAT_080d94f8                     @ 080d944c 2a4d
    ldrh r3,[r6,#0x22]                       @ 080d944e 738c
    lsls r1,r3,#0x1    @ 080d9450 5900
    adds r1,r1,r3    @ 080d9452 c918
    lsls r0,r1,#0x4    @ 080d9454 0801
    subs r0,r0,r1    @ 080d9456 401a
    lsls r0,r0,#0x3    @ 080d9458 c000
    movs r1,#0x1e    @ 080d945a 1e21
    bl bios_div                              @ 080d945c 34f0ceff
    adds r2,r0,#0x0    @ 080d9460 021c
    lsls r2,r2,#0x10    @ 080d9462 1204
    movs r0,#0xc    @ 080d9464 0c20
    orrs r2,r0    @ 080d9466 0243
    adds r0,r4,#0x0    @ 080d9468 201c
    adds r1,r5,#0x0    @ 080d946a 291c
    bl rotate_pixel_hue_in_buffer            @ 080d946c 04f00efb
    ldrh r0,[r6,#0x1e]                       @ 080d9470 f08b
    cmp r0,#0x0                              @ 080d9472 0028
    beq LAB_080d94aa                         @ 080d9474 19d0
    movs r0,#0x0    @ 080d9476 0020
    bl compute_pack_slot_scroll_x            @ 080d9478 fff7befc
    subs r0,#0x20    @ 080d947c 2038
    lsls r0,r0,#0x10    @ 080d947e 0004
    asrs r0,r0,#0x10    @ 080d9480 0014
    lsls r1,r7,#0x10    @ 080d9482 3904
    asrs r1,r1,#0x10    @ 080d9484 0914
    subs r0,r0,r1    @ 080d9486 401a
    lsls r0,r0,#0x10    @ 080d9488 0004
    lsrs r0,r0,#0x10    @ 080d948a 000c
    movs r1,#0x90    @ 080d948c 9021
    lsls r1,r1,#0xf    @ 080d948e c903
    orrs r0,r1    @ 080d9490 0843
    .hword 0x4651    @ 080d9492 5146
    lsls r2,r1,#0xa    @ 080d9494 8a02
    ldr r3, DAT_080d94fc                     @ 080d9496 194b
    adds r1,r3,#0x0    @ 080d9498 191c
    orrs r2,r1    @ 080d949a 0a43
    lsls r2,r2,#0x10    @ 080d949c 1204
    lsrs r2,r2,#0x10    @ 080d949e 120c
    movs r3,#0x80    @ 080d94a0 8023
    lsls r3,r3,#0x5    @ 080d94a2 5b01
    movs r1,#0x40    @ 080d94a4 4021
    bl write_oam_entry_with_slot_check       @ 080d94a6 1df0a5f9
LAB_080d94aa:
    ldrh r0,[r6,#0x1e]                       @ 080d94aa f08b
    add r0,r9                                @ 080d94ac 4844
    ldrh r6,[r6,#0x8]                        @ 080d94ae 3689
    cmp r0,r6                                @ 080d94b0 b042
    bcs LAB_080d94e6                         @ 080d94b2 18d2
    .hword 0x4648    @ 080d94b4 4846
    subs r0,#0x1    @ 080d94b6 0138
    bl compute_pack_slot_scroll_x            @ 080d94b8 fff79efc
    adds r0,#0x10    @ 080d94bc 1030
    lsls r0,r0,#0x10    @ 080d94be 0004
    asrs r0,r0,#0x10    @ 080d94c0 0014
    lsls r1,r7,#0x10    @ 080d94c2 3904
    asrs r1,r1,#0x10    @ 080d94c4 0914
    adds r0,r0,r1    @ 080d94c6 4018
    lsls r0,r0,#0x10    @ 080d94c8 0004
    lsrs r0,r0,#0x10    @ 080d94ca 000c
    movs r1,#0x90    @ 080d94cc 9021
    lsls r1,r1,#0xf    @ 080d94ce c903
    orrs r0,r1    @ 080d94d0 0843
    .hword 0x4651    @ 080d94d2 5146
    lsls r2,r1,#0xa    @ 080d94d4 8a02
    ldr r3, DAT_080d94fc                     @ 080d94d6 094b
    adds r1,r3,#0x0    @ 080d94d8 191c
    orrs r2,r1    @ 080d94da 0a43
    lsls r2,r2,#0x10    @ 080d94dc 1204
    lsrs r2,r2,#0x10    @ 080d94de 120c
    movs r1,#0x40    @ 080d94e0 4021
    bl write_oam_entry_from_packed_args      @ 080d94e2 1cf043fe
LAB_080d94e6:
    pop {r3,r4,r5}                           @ 080d94e6 38bc
    .hword 0x4698    @ 080d94e8 9846
    .hword 0x46a1    @ 080d94ea a146
    .hword 0x46aa    @ 080d94ec aa46
    pop {r4,r5,r6,r7}                        @ 080d94ee f0bc
    pop {r0}                                 @ 080d94f0 01bc
    bx r0                                    @ 080d94f2 0047
DAT_080d94f4:
    .word  0x09ce824c                     @ 080d94f4 4c82ce09
DAT_080d94f8:
    .word  0x05000388                     @ 080d94f8 88030005
DAT_080d94fc:
    .word  0x0000c34c                     @ 080d94fc 4cc30000

@ In the pack shop scene, writes 4 icon sprite OAM entries for the pack slot at direction index r0. Increments and wraps pack_ui_state[+0xc+0x24] frame animation index (0..4), looks up tile ID from animation frame table (0x09e49508), then calls write_oam_entry_from_packed_args for 4 OAM entries (icon body x3 + border x1). Exit via pop{r0}; bx r0, r0 has no semantic.
@ 
@ Constants:
@ - ANIM_TABLE=0x09e49508 // pack icon animation frame tile table
@ - OAM_ATTR0_BASE=0x00700090 // 1st OAM entry attr0+attr1
@ - ANIM_FRAME_MAX=5 // animation frame count (0..4)
@ - OAM_ATTR2_MASK=0x0000a000 // 0xa0<<8: OAM attr2 (1st entry)
render_pack_icon_oam_entries:
    push {r4,r5,r6,r7,lr}                    @ 080d9500 f0b5
    adds r4,r0,#0x0    @ 080d9502 041c
    ldr r0, DAT_080d95a8                     @ 080d9504 2848
    adds r3,r0,#0x0    @ 080d9506 031c
    adds r3,#0xc    @ 080d9508 0c33
    ldrh r0,[r3,#0x24]                       @ 080d950a 988c
    adds r0,#0x1    @ 080d950c 0130
    strh r0,[r3,#0x24]                       @ 080d950e 9884
    movs r2,#0x0    @ 080d9510 0022
    ldr r1, DAT_080d95ac                     @ 080d9512 2649
    lsls r0,r0,#0x10    @ 080d9514 0004
    lsrs r0,r0,#0x10    @ 080d9516 000c
    adds r5,r1,#0x0    @ 080d9518 0d1c
    ldr r6, DAT_080d95b0                     @ 080d951a 254e
    ldrh r1,[r5,#0x2]                        @ 080d951c 6988
    cmp r1,r0                                @ 080d951e 8142
    bhi LAB_080d9534                         @ 080d9520 08d8
    adds r0,r5,#0x0    @ 080d9522 281c
LAB_080d9524:
    adds r0,#0x4    @ 080d9524 0430
    adds r2,#0x1    @ 080d9526 0132
    cmp r2,#0x4                              @ 080d9528 042a
    bhi LAB_080d9538                         @ 080d952a 05d8
    ldrh r7,[r0,#0x2]                        @ 080d952c 4788
    ldrh r1,[r3,#0x24]                       @ 080d952e 998c
    cmp r7,r1                                @ 080d9530 8f42
    bls LAB_080d9524                         @ 080d9532 f7d9
LAB_080d9534:
    cmp r2,#0x4                              @ 080d9534 042a
    bls LAB_080d953e                         @ 080d9536 02d9
LAB_080d9538:
    movs r0,#0x0    @ 080d9538 0020
    strh r0,[r3,#0x24]                       @ 080d953a 9884
    movs r2,#0x0    @ 080d953c 0022
LAB_080d953e:
    ldr r0, DAT_080d95b4                     @ 080d953e 1d48
    lsls r4,r4,#0xa    @ 080d9540 a402
    lsls r1,r2,#0x2    @ 080d9542 9100
    adds r1,r1,r5    @ 080d9544 4919
    ldrh r1,[r1,#0x0]                        @ 080d9546 0988
    lsls r1,r1,#0x1    @ 080d9548 4900
    adds r1,r1,r6    @ 080d954a 8919
    movs r3,#0xa0    @ 080d954c a023
    lsls r3,r3,#0x8    @ 080d954e 1b02
    adds r2,r3,#0x0    @ 080d9550 1a1c
    ldrh r1,[r1,#0x0]                        @ 080d9552 0988
    orrs r2,r1    @ 080d9554 0a43
    orrs r2,r4    @ 080d9556 2243
    lsls r2,r2,#0x10    @ 080d9558 1204
    lsrs r2,r2,#0x10    @ 080d955a 120c
    movs r1,#0x40    @ 080d955c 4021
    bl write_oam_entry_from_packed_args      @ 080d955e 1cf005fe
    ldr r0, DAT_080d95b8                     @ 080d9562 1548
    movs r5,#0x81    @ 080d9564 8125
    lsls r5,r5,#0x7    @ 080d9566 ed01
    ldr r7, DAT_080d95bc                     @ 080d9568 144f
    adds r1,r7,#0x0    @ 080d956a 391c
    adds r2,r4,#0x0    @ 080d956c 221c
    orrs r2,r1    @ 080d956e 0a43
    lsls r2,r2,#0x10    @ 080d9570 1204
    lsrs r2,r2,#0x10    @ 080d9572 120c
    adds r1,r5,#0x0    @ 080d9574 291c
    bl write_oam_entry_from_packed_args      @ 080d9576 1cf0f9fd
    ldr r0, DAT_080d95c0                     @ 080d957a 1148
    ldr r2, DAT_080d95c4                     @ 080d957c 114a
    adds r1,r2,#0x0    @ 080d957e 111c
    adds r2,r4,#0x0    @ 080d9580 221c
    orrs r2,r1    @ 080d9582 0a43
    lsls r2,r2,#0x10    @ 080d9584 1204
    lsrs r2,r2,#0x10    @ 080d9586 120c
    adds r1,r5,#0x0    @ 080d9588 291c
    bl write_oam_entry_from_packed_args      @ 080d958a 1cf0effd
    ldr r0, DAT_080d95c8                     @ 080d958e 0e48
    ldr r3, DAT_080d95cc                     @ 080d9590 0e4b
    adds r1,r3,#0x0    @ 080d9592 191c
    orrs r4,r1    @ 080d9594 0c43
    lsls r4,r4,#0x10    @ 080d9596 2404
    lsrs r4,r4,#0x10    @ 080d9598 240c
    movs r1,#0x40    @ 080d959a 4021
    adds r2,r4,#0x0    @ 080d959c 221c
    bl write_oam_entry_from_packed_args      @ 080d959e 1cf0e5fd
    pop {r4,r5,r6,r7}                        @ 080d95a2 f0bc
    pop {r0}                                 @ 080d95a4 01bc
    bx r0                                    @ 080d95a6 0047
DAT_080d95a8:
    .word  pack_ui_state                  @ 080d95a8 50580003
DAT_080d95ac:
    .word  0x09e49508                     @ 080d95ac 0895e409
DAT_080d95b0:
    .word  0x09e49500                     @ 080d95b0 0095e409
DAT_080d95b4:
    .word  0x00700090                     @ 080d95b4 90007000
DAT_080d95b8:
    .word  0x007000a0                     @ 080d95b8 a0007000
DAT_080d95bc:
    .word  0x0000f3cc                     @ 080d95bc ccf30000
DAT_080d95c0:
    .word  0x007000c0                     @ 080d95c0 c0007000
DAT_080d95c4:
    .word  0x0000f3d0                     @ 080d95c4 d0f30000
DAT_080d95c8:
    .word  0x007000e0                     @ 080d95c8 e0007000
DAT_080d95cc:
    .word  0x0000f3d4                     @ 080d95cc d4f30000

@ Renders left/right arrow OBJ entries for the pack-list selection UI. r0=dir_index [0..3, clamped]. Iterates pack_visible_count visible slots; for each slot with slot[+0x18]!=0 (valid), calls compute_pack_slot_scroll_x for X coordinate, writes X-4 into attr0, combines dir_index<<10 (priority) with tile_id for attr1/attr2, calls write_oam_entry_from_packed_args. Works with the banner highlight-box OAM writer to display pack-select arrows.
@ 
@ Constants:
@ - SLOT_STRIDE=0x20 // slot struct stride
@ - DIR_MAX=3 // max dir_index (clamp)
@ - OBJ_TILE_BASE=0x000003d6 // arrow tile base (DAT_080d964c)
@ - ATTR0_FLAG=0x5c0000 // 0xb8<<15: OBJ attr0 size/shape high bits
@ - X_OFFSET=-4 // X coordinate adjustment
render_pack_slot_arrow_oam:
    push {r4,r5,r6,r7,lr}                    @ 080d95d0 f0b5
    .hword 0x464f    @ 080d95d2 4f46
    .hword 0x4646    @ 080d95d4 4646
    push {r6,r7}                             @ 080d95d6 c0b4
    adds r5,r0,#0x0    @ 080d95d8 051c
    ldr r4, DAT_080d9648                     @ 080d95da 1b4c
    adds r4,#0xc    @ 080d95dc 0c34
    bl pack_visible_count                    @ 080d95de fff7fdfb
    .hword 0x4680    @ 080d95e2 8046
    ldrh r1,[r4,#0x1e]                       @ 080d95e4 e18b
    lsls r0,r1,#0x5    @ 080d95e6 4801
    adds r0,#0x44    @ 080d95e8 4430
    adds r6,r0,r4    @ 080d95ea 0619
    ldr r7, DAT_080d964c                     @ 080d95ec 174f
    cmp r5,#0x3                              @ 080d95ee 032d
    bls LAB_080d95f4                         @ 080d95f0 00d9
    movs r5,#0x3    @ 080d95f2 0325
LAB_080d95f4:
    movs r4,#0x0    @ 080d95f4 0024
    cmp r4,r8                                @ 080d95f6 4445
    bcs LAB_080d963c                         @ 080d95f8 20d2
    movs r2,#0xb8    @ 080d95fa b822
    lsls r2,r2,#0xf    @ 080d95fc d203
    .hword 0x4691    @ 080d95fe 9146
    lsls r5,r5,#0xa    @ 080d9600 ad02
LAB_080d9602:
    ldrh r0,[r6,#0x18]                       @ 080d9602 308b
    cmp r0,#0x0                              @ 080d9604 0028
    beq LAB_080d962e                         @ 080d9606 12d0
    adds r0,r4,#0x0    @ 080d9608 201c
    bl compute_pack_slot_scroll_x            @ 080d960a fff7f5fb
    subs r0,#0x4    @ 080d960e 0438
    lsls r0,r0,#0x10    @ 080d9610 0004
    lsrs r0,r0,#0x10    @ 080d9612 000c
    .hword 0x4649    @ 080d9614 4946
    orrs r0,r1    @ 080d9616 0843
    movs r2,#0xb0    @ 080d9618 b022
    lsls r2,r2,#0x8    @ 080d961a 1202
    adds r1,r2,#0x0    @ 080d961c 111c
    adds r2,r7,#0x0    @ 080d961e 3a1c
    orrs r2,r1    @ 080d9620 0a43
    orrs r2,r5    @ 080d9622 2a43
    lsls r2,r2,#0x10    @ 080d9624 1204
    lsrs r2,r2,#0x10    @ 080d9626 120c
    movs r1,#0x40    @ 080d9628 4021
    bl write_oam_entry_from_packed_args      @ 080d962a 1cf09ffd
LAB_080d962e:
    adds r0,r7,#0x2    @ 080d962e b81c
    lsls r0,r0,#0x10    @ 080d9630 0004
    lsrs r7,r0,#0x10    @ 080d9632 070c
    adds r6,#0x20    @ 080d9634 2036
    adds r4,#0x1    @ 080d9636 0134
    cmp r4,r8                                @ 080d9638 4445
    bcc LAB_080d9602                         @ 080d963a e2d3
LAB_080d963c:
    pop {r3,r4}                              @ 080d963c 18bc
    .hword 0x4698    @ 080d963e 9846
    .hword 0x46a1    @ 080d9640 a146
    pop {r4,r5,r6,r7}                        @ 080d9642 f0bc
    pop {r0}                                 @ 080d9644 01bc
    bx r0                                    @ 080d9646 0047
DAT_080d9648:
    .word  pack_ui_state                  @ 080d9648 50580003
DAT_080d964c:
    .word  0x000003d6                     @ 080d964c d6030000

@ Renders the selection-highlight OBJ (two stacked layers) for the currently highlighted pack slot. r0=dir_index [0..3], clamped. Computes tile_base=0xd4<<2=0x350, uses DAT_080d9688 (attr0=0x0044, attr1=0x0090) and DAT_080d9690 (second layer attr), calls render_overlay_oam_sprite_tiled twice. Second call uses tile_base+0x40=0x390. dir_flags=dir_index<<10 encodes OAM priority.
@ 
@ Constants:
@ - TILE_BASE=0x350 // 0xd4<<2: highlight frame tile start
@ - TILE_BASE2=0x390 // 0x350+0x40: second layer tile start
@ - OAM_ATTR0_0=0x00900044 // layer 0: attr0(y=0x44)|attr1(x=0x90)
@ - OAM_ATTR0_1=0x0090fff4 // layer 1: x=0xfff4=-12 offset
@ - DIR_MAX=3 // dir_index clamp maximum
render_pack_slot_highlight_oam:
    push {r4,r5,r6,r7,lr}                    @ 080d9650 f0b5
    adds r6,r0,#0x0    @ 080d9652 061c
    movs r7,#0xd4    @ 080d9654 d427
    lsls r7,r7,#0x2    @ 080d9656 bf00
    cmp r6,#0x3                              @ 080d9658 032e
    bls LAB_080d965e                         @ 080d965a 00d9
    movs r6,#0x3    @ 080d965c 0326
LAB_080d965e:
    ldr r0, DAT_080d9688                     @ 080d965e 0a48
    ldr r5, DAT_080d968c                     @ 080d9660 0a4d
    movs r4,#0xb0    @ 080d9662 b024
    lsls r4,r4,#0xc    @ 080d9664 2403
    adds r2,r7,#0x0    @ 080d9666 3a1c
    orrs r2,r4    @ 080d9668 2243
    adds r1,r5,#0x0    @ 080d966a 291c
    adds r3,r6,#0x0    @ 080d966c 331c
    bl render_overlay_oam_sprite_tiled       @ 080d966e 04f07ff8
    adds r7,#0x40    @ 080d9672 4037
    ldr r0, DAT_080d9690                     @ 080d9674 0648
    orrs r7,r4    @ 080d9676 2743
    adds r1,r5,#0x0    @ 080d9678 291c
    adds r2,r7,#0x0    @ 080d967a 3a1c
    adds r3,r6,#0x0    @ 080d967c 331c
    bl render_overlay_oam_sprite_tiled       @ 080d967e 04f077f8
    pop {r4,r5,r6,r7}                        @ 080d9682 f0bc
    pop {r0}                                 @ 080d9684 01bc
    bx r0                                    @ 080d9686 0047
DAT_080d9688:
    .word  0x00900044                     @ 080d9688 44009000
DAT_080d968c:
    .word  0x0002000d                     @ 080d968c 0d000200
DAT_080d9690:
    .word  0x0090fff4                     @ 080d9690 f4ff9000

@ Called on the pack list page initialization path (indeg=0, Sub-type A). Reads pack_ui_state[+0x724] bit0; if 0, jumps directly to scroll reset phase. If set, iterates pack_ui_state[+0x50] slot list (0x20 bytes per slot), searching for a slot where [slot+0]==[+0x20] (match); on hit, computes page row offset via get_bios_div_remainder(slot_idx, 5), writes [+0x18]=scroll_page_pos and [+0x1e]=slot_idx-scroll_page_pos; if no match, both fields are cleared. Then calls set_pack_scroll_step_mode, recompute_pack_selection_totals, and init_overlay_struct_and_palette(pack_ui_state+0x6c4, 0x0200af20, 0, 0xf, 6). Returns fixed 1 (Sub-case E, pop{r1};bx r1).
@ 
@ Constants:
@ - FLAG_OFFSET = 0x724 (DAT_080d96d4 = pack_ui_state+0x724 = init control flag)
@ - FLAG_BIT0 = 0x1 (ands r0,r1 with #1 = scroll-position flag)
@ - SLOT_LIST_OFFSET = 0x50 (adds r1,#0x50 = slot list start offset)
@ - SLOT_STRIDE = 0x20 (adds r1,#0x20 per slot)
@ - SCROLL_PAGE_SIZE = 5 (get_bios_div_remainder(idx, 5) = 5 slots per page)
@ - SCROLL_POS_OFFSET = 0x18 (strh [r5,#0x18] = page scroll position)
@ - SCROLL_IDX_OFFSET = 0x1e (strh [r5,#0x1e] = selected slot relative to page start)
@ - SCROLL_STEP_OFFSET = 0x1a (strh 0,[r5,#0x1a] = clear scroll step count)
@ - OVERLAY_PALETTE_BASE = 0x0200af20 (DAT_080d9718 = EWRAM overlay palette)
@ - OVERLAY_STRUCT_OFFSET = 0x6c4 (DAT_080d9714 = pack_ui_state+0x6c4 = overlay struct)
@ - OVERLAY_PALETTE_COUNT = 0xf (movs r3,#0xf)
@ - OVERLAY_PARAM5 = 6 (str r2,[sp,#0] with r2=#6 = 5th argument)
init_pack_list_scroll_to_selected_slot:
    push {r4,r5,lr}                          @ 080d9694 30b5
    sub sp,#0x4                              @ 080d9696 81b0
    ldr r2, DAT_080d96d0                     @ 080d9698 0d4a
    adds r5,r2,#0x0    @ 080d969a 151c
    adds r5,#0xc    @ 080d969c 0c35
    ldr r0, DAT_080d96d4                     @ 080d969e 0d48
    adds r1,r2,r0    @ 080d96a0 1118
    movs r0,#0x1    @ 080d96a2 0120
    ldrb r1,[r1,#0x0]                        @ 080d96a4 0978
    ands r0,r1    @ 080d96a6 0840
    cmp r0,#0x0                              @ 080d96a8 0028
    beq LAB_080d96ec                         @ 080d96aa 1fd0
    adds r1,r2,#0x0    @ 080d96ac 111c
    adds r1,#0x50    @ 080d96ae 5031
    movs r4,#0x0    @ 080d96b0 0024
    ldrh r0,[r5,#0x8]                        @ 080d96b2 2889
    cmp r4,r0                                @ 080d96b4 8442
    bcs LAB_080d96e0                         @ 080d96b6 13d2
LAB_080d96b8:
    ldrh r2,[r1,#0x0]                        @ 080d96b8 0a88
    ldrh r3,[r5,#0x20]                       @ 080d96ba 2b8c
    cmp r2,r3                                @ 080d96bc 9a42
    bne LAB_080d96d8                         @ 080d96be 0bd1
    adds r0,r4,#0x0    @ 080d96c0 201c
    movs r1,#0x5    @ 080d96c2 0521
    bl get_bios_div_remainder                @ 080d96c4 34f09cfe
    strh r0,[r5,#0x18]                       @ 080d96c8 2883
    subs r0,r4,r0    @ 080d96ca 201a
    strh r0,[r5,#0x1e]                       @ 080d96cc e883
    b LAB_080d96e0                           @ 080d96ce 07e0
DAT_080d96d0:
    .word  pack_ui_state                  @ 080d96d0 50580003
DAT_080d96d4:
    .word  0x00000724                     @ 080d96d4 24070000
LAB_080d96d8:
    adds r1,#0x20    @ 080d96d8 2031
    adds r4,#0x1    @ 080d96da 0134
    cmp r4,r0                                @ 080d96dc 8442
    bcc LAB_080d96b8                         @ 080d96de ebd3
LAB_080d96e0:
    ldrh r0,[r5,#0x8]                        @ 080d96e0 2889
    cmp r4,r0                                @ 080d96e2 8442
    bne LAB_080d96ec                         @ 080d96e4 02d1
    movs r0,#0x0    @ 080d96e6 0020
    strh r0,[r5,#0x1e]                       @ 080d96e8 e883
    strh r0,[r5,#0x18]                       @ 080d96ea 2883
LAB_080d96ec:
    movs r0,#0x0    @ 080d96ec 0020
    strh r0,[r5,#0x1a]                       @ 080d96ee 6883
    bl set_pack_scroll_step_mode             @ 080d96f0 fbf742f9
    bl recompute_pack_selection_totals       @ 080d96f4 02f028f8
    ldr r1, DAT_080d9714                     @ 080d96f8 0649
    adds r0,r5,r1    @ 080d96fa 6818
    ldr r1, DAT_080d9718                     @ 080d96fc 0649
    movs r2,#0x6    @ 080d96fe 0622
    str r2,[sp,#0x0]                         @ 080d9700 0092
    movs r2,#0x0    @ 080d9702 0022
    movs r3,#0xf    @ 080d9704 0f23
    bl init_overlay_struct_and_palette       @ 080d9706 03f04ffe
    movs r0,#0x1    @ 080d970a 0120
    add sp,#0x4                              @ 080d970c 01b0
    pop {r4,r5}                              @ 080d970e 30bc
    pop {r1}                                 @ 080d9710 02bc
    bx r1                                    @ 080d9712 0847
DAT_080d9714:
    .word  0x000006c4                     @ 080d9714 c4060000
DAT_080d9718:
    .word  0x0200af20                     @ 080d9718 20af0002

@ pack-banner: 卡包列表页初始化, 函数指针表 0x09E4948C[11]
pack_list_page_init:
    push {r4,r5,r6,lr}                       @ 080d971c 70b5
    sub sp,#0xc                              @ 080d971e 83b0
    ldr r0, DAT_080d974c                     @ 080d9720 0a48
    adds r6,r0,#0x0    @ 080d9722 061c
    adds r6,#0xc    @ 080d9724 0c36
    bl pack_list_bg_setup                    @ 080d9726 fff72dfb
    bl pack_list_tilemap_load                @ 080d972a fff7edfb
    movs r0,#0xc2    @ 080d972e c220
    lsls r0,r0,#0x2    @ 080d9730 8000
    str r0,[sp,#0x0]                         @ 080d9732 0090
    adds r0,#0x8    @ 080d9734 0830
    str r0,[sp,#0x4]                         @ 080d9736 0190
    movs r0,#0x1    @ 080d9738 0120
    rsbs r0,r0,#0    @ 080d973a 4042
    str r0,[sp,#0x8]                         @ 080d973c 0290
    .hword 0x4668    @ 080d973e 6846
    movs r1,#0xd    @ 080d9740 0d21
    bl load_pack_card_tiles_to_vram          @ 080d9742 faf75bff
    movs r4,#0x0    @ 080d9746 0024
    b LAB_080d9758                           @ 080d9748 06e0
    .zero  0x2
DAT_080d974c:
    .word  pack_ui_state                  @ 080d974c 50580003
LAB_080d9750:
    adds r0,r4,#0x0    @ 080d9750 201c
    bl pack_entry_init                       @ 080d9752 fff7a1fb
    adds r4,#0x1    @ 080d9756 0134
LAB_080d9758:
    bl pack_visible_count                    @ 080d9758 fff740fb
    cmp r4,r0                                @ 080d975c 8442
    bcc LAB_080d9750                         @ 080d975e f7d3
    ldr r0, DAT_080d97ec                     @ 080d9760 2248
    ldr r1, PTR_pack_banner_obj_palette_080d97f0 @ 080d9762 2349
    movs r2,#0x90    @ 080d9764 9022
    lsls r2,r2,#0x1    @ 080d9766 5200
    bl copy_memory_dma3_with_cpu_fallback    @ 080d9768 1bf0cefb
    bl render_pack_slot_counts_to_bg_vram    @ 080d976c fff7defc
    movs r0,#0xc3    @ 080d9770 c320
    lsls r0,r0,#0x2    @ 080d9772 8000
    movs r1,#0xe    @ 080d9774 0e21
    bl load_pack_card_tile_row_to_obj_vram   @ 080d9776 02f0fffd
    movs r0,#0xd3    @ 080d977a d320
    lsls r0,r0,#0x2    @ 080d977c 8000
    movs r1,#0xc    @ 080d977e 0c21
    bl load_pack_card_tile_row_to_obj_vram_b @ 080d9780 02f01afe
    bl render_pack_list_label_sprites_and_palette @ 080d9784 fff72cfd
    ldr r0, DAT_080d97f4                     @ 080d9788 1a48
    movs r1,#0xa    @ 080d978a 0a21
    bl load_pack_multi_card_tiles_to_obj_vram @ 080d978c 02f054fe
    ldr r2, DAT_080d97f8                     @ 080d9790 194a
    movs r0,#0x2    @ 080d9792 0220
    rsbs r0,r0,#0    @ 080d9794 4042
    ldrb r1,[r2,#0x15]                       @ 080d9796 517d
    ands r0,r1    @ 080d9798 0840
    strb r0,[r2,#0x15]                       @ 080d979a 5075
    movs r1,#0x3    @ 080d979c 0321
    rsbs r1,r1,#0    @ 080d979e 4942
    ldrb r3,[r2,#0x8]                        @ 080d97a0 137a
    ands r1,r3    @ 080d97a2 1940
    strb r1,[r2,#0x8]                        @ 080d97a4 1172
    movs r0,#0x7d    @ 080d97a6 7d20
    rsbs r0,r0,#0    @ 080d97a8 4042
    ldrb r3,[r2,#0x14]                       @ 080d97aa 137d
    ands r0,r3    @ 080d97ac 1840
    strb r0,[r2,#0x14]                       @ 080d97ae 1075
    ldr r0, PTR_font_jp_base_table_080d97fc  @ 080d97b0 1248
    lsls r1,r1,#0x1f    @ 080d97b2 c907
    lsrs r1,r1,#0x1f    @ 080d97b4 c90f
    lsls r1,r1,#0x3    @ 080d97b6 c900
    adds r1,r1,r0    @ 080d97b8 0918
    ldr r0,[r1,#0x0]                         @ 080d97ba 0868
    str r0,[r2,#0x4]                         @ 080d97bc 5060
    ldr r5, DAT_080d9800                     @ 080d97be 104d
    movs r4,#0xa0    @ 080d97c0 a024
    lsls r4,r4,#0x1    @ 080d97c2 6400
    adds r0,r5,#0x0    @ 080d97c4 281c
    adds r1,r4,#0x0    @ 080d97c6 211c
    bl zero_fill_halfword_wrapper            @ 080d97c8 1bf066fb
    movs r0,#0x80    @ 080d97cc 8020
    lsls r0,r0,#0x3    @ 080d97ce c000
    adds r0,r5,r0    @ 080d97d0 2818
    adds r1,r4,#0x0    @ 080d97d2 211c
    bl zero_fill_halfword_wrapper            @ 080d97d4 1bf060fb
    ldr r0, DAT_080d9804                     @ 080d97d8 0a48
    ldr r1, DAT_080d9808                     @ 080d97da 0b49
    adds r4,r0,r1    @ 080d97dc 4418
    movs r0,#0x7    @ 080d97de 0720
    ldrb r3,[r4,#0x0]                        @ 080d97e0 2378
    ands r0,r3    @ 080d97e2 1840
    cmp r0,#0x0                              @ 080d97e4 0028
    bne LAB_080d9810                         @ 080d97e6 13d1
    ldr r0, DAT_080d980c                     @ 080d97e8 0848
    b LAB_080d9812                           @ 080d97ea 12e0
DAT_080d97ec:
    .word  0x05000200                     @ 080d97ec 00020005
PTR_pack_banner_obj_palette_080d97f0:
    .word  pack_banner_obj_palette        @ 080d97f0 40045108
DAT_080d97f4:
    .word  0x09e49500                     @ 080d97f4 0095e409
DAT_080d97f8:
    .word  0x02006ed0                     @ 080d97f8 d06e0002
PTR_font_jp_base_table_080d97fc:
    .word  font_jp_base_table             @ 080d97fc 54f8e509
DAT_080d9800:
    .word  0x06017980                     @ 080d9800 80790106
DAT_080d9804:
    .word  0x02000000                     @ 080d9804 00000002
DAT_080d9808:
    .word  0x00006c2c                     @ 080d9808 2c6c0000
DAT_080d980c:
    .word  0x000013f8                     @ 080d980c f8130000
LAB_080d9810:
    ldr r0, DAT_080d9888                     @ 080d9810 1d48
LAB_080d9812:
    bl game_str_id_to_row                    @ 080d9812 1bf001fb
    ldr r2, PTR_game_str_pointer_table_080d988c @ 080d9816 1d4a
    lsls r0,r0,#0x10    @ 080d9818 0004
    lsrs r0,r0,#0x10    @ 080d981a 000c
    lsls r1,r0,#0x1    @ 080d981c 4100
    adds r1,r1,r0    @ 080d981e 0918
    lsls r1,r1,#0x1    @ 080d9820 4900
    ldrb r4,[r4,#0x0]                        @ 080d9822 2478
    lsls r0,r4,#0x1d    @ 080d9824 6007
    lsrs r0,r0,#0x1d    @ 080d9826 400f
    adds r1,r1,r0    @ 080d9828 0918
    lsls r1,r1,#0x2    @ 080d982a 8900
    adds r1,r1,r2    @ 080d982c 8918
    ldr r1,[r1,#0x0]                         @ 080d982e 0968
    ldr r0, PTR_game_str_ja_080d9890         @ 080d9830 1748
    adds r4,r1,r0    @ 080d9832 0c18
    movs r0,#0xa    @ 080d9834 0a20
    movs r1,#0x2    @ 080d9836 0221
    bl setup_line_buf_pos_and_font           @ 080d9838 17f0bcf9
    ldr r2, DAT_080d9894                     @ 080d983c 154a
    movs r0,#0x1    @ 080d983e 0120
    movs r1,#0x4    @ 080d9840 0421
    adds r3,r4,#0x0    @ 080d9842 231c
    bl text_render_wrapper                   @ 080d9844 19f01af9
    movs r0,#0x1    @ 080d9848 0120
    movs r1,#0x4    @ 080d984a 0421
    movs r2,#0x7    @ 080d984c 0722
    adds r3,r4,#0x0    @ 080d984e 231c
    bl text_render_wrapper                   @ 080d9850 19f014f9
    adds r0,r5,#0x0    @ 080d9854 281c
    movs r1,#0x0    @ 080d9856 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d9858 19f0bcff
    ldr r0, DAT_080d9898                     @ 080d985c 0e48
    ldr r1, DAT_080d989c                     @ 080d985e 0f49
    movs r2,#0x20    @ 080d9860 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d9862 1bf051fb
    movs r0,#0xe3    @ 080d9866 e320
    lsls r0,r0,#0x3    @ 080d9868 c000
    adds r1,r6,r0    @ 080d986a 3118
    movs r0,#0x1    @ 080d986c 0120
    ldrb r1,[r1,#0x0]                        @ 080d986e 0978
    ands r0,r1    @ 080d9870 0840
    cmp r0,#0x0                              @ 080d9872 0028
    bne LAB_080d987c                         @ 080d9874 02d1
    ldr r1, DAT_080d98a0                     @ 080d9876 0a49
    movs r0,#0x2    @ 080d9878 0220
    strh r0,[r1,#0x10]                       @ 080d987a 0882
LAB_080d987c:
    movs r0,#0x1    @ 080d987c 0120
    add sp,#0xc                              @ 080d987e 03b0
    pop {r4,r5,r6}                           @ 080d9880 70bc
    pop {r1}                                 @ 080d9882 02bc
    bx r1                                    @ 080d9884 0847
    .zero  0x2
DAT_080d9888:
    .word  0x00000642                     @ 080d9888 42060000
PTR_game_str_pointer_table_080d988c:
    .word  game_str_pointer_table         @ 080d988c 400f0008
PTR_game_str_ja_080d9890:
    .word  game_str_ja                    @ 080d9890 109cdb09
DAT_080d9894:
    .word  0x00008008                     @ 080d9894 08800000
DAT_080d9898:
    .word  0x050001e0                     @ 080d9898 e0010005
DAT_080d989c:
    .word  0x09ccd290                     @ 080d989c 90d2cc09
DAT_080d98a0:
    .word  pack_ui_state                  @ 080d98a0 50580003

@ 拆包卡槽滚入到位后的帧渲染. 取 pack_visible_count 得可见卡数 (r6). 若 pack_ui_state+0x724 状态字 bit1 未置位 (首次进入), 则置 DISPCNT bit12 (0x1000) 开启 OBJ 显示, 调 update_pack_slot_scroll_positions 同步滚动位置, 并为每个可见槽初始化精灵插值字段 ([+0x6]/[+0x8] 目标, [+0xa]/[+0xc] 源, [+0xe] 缩放 0x400, [+0x10] 帧计数 8/12/...), 然后将 [+0x724] bit1 置位标记已初始化. 之后每帧对每个槽递减 [+0x10] 计数并经 bios_div 做线性插值更新 [+0x2]/[+0x4] 位置与 [+0xe] 缩放, 计数归零时调 sync_state_and_init_sprite(4). 最后递减 pack_ui_state+0xc[+0x6] 帧计数, 透传调 write_pack_banner_oam_for_all_slots(0) 重绘横幅 OAM. 供拆包滚入状态机帧驱动.
render_pack_slots_after_scroll_in:
    push {r4,r5,r6,r7,lr}                    @ 080d98a4 f0b5
    .hword 0x464f    @ 080d98a6 4f46
    .hword 0x4646    @ 080d98a8 4646
    push {r6,r7}                             @ 080d98aa c0b4
    ldr r4, DAT_080d9954                     @ 080d98ac 294c
    adds r7,r4,#0x0    @ 080d98ae 271c
    adds r7,#0xc    @ 080d98b0 0c37
    movs r0,#0x0    @ 080d98b2 0020
    .hword 0x4681    @ 080d98b4 8146
    bl pack_visible_count                    @ 080d98b6 fff791fa
    adds r6,r0,#0x0    @ 080d98ba 061c
    ldr r1, DAT_080d9958                     @ 080d98bc 2649
    adds r4,r4,r1    @ 080d98be 6418
    movs r0,#0x2    @ 080d98c0 0220
    ldrb r4,[r4,#0x0]                        @ 080d98c2 2478
    ands r0,r4    @ 080d98c4 2040
    cmp r0,#0x0                              @ 080d98c6 0028
    bne LAB_080d992c                         @ 080d98c8 30d1
    movs r2,#0x80    @ 080d98ca 8022
    lsls r2,r2,#0x13    @ 080d98cc d204
    movs r0,#0x80    @ 080d98ce 8020
    lsls r0,r0,#0x5    @ 080d98d0 4001
    ldrh r1,[r2,#0x0]                        @ 080d98d2 1188
    orrs r0,r1    @ 080d98d4 0843
    strh r0,[r2,#0x0]                        @ 080d98d6 1080
    bl update_pack_slot_scroll_positions     @ 080d98d8 fff7b8fa
    ldrh r2,[r7,#0x1e]                       @ 080d98dc fa8b
    lsls r0,r2,#0x5    @ 080d98de 5001
    adds r0,#0x44    @ 080d98e0 4430
    adds r4,r0,r7    @ 080d98e2 c419
    movs r5,#0x0    @ 080d98e4 0025
    lsls r3,r6,#0x2    @ 080d98e6 b300
    cmp r9,r6                                @ 080d98e8 b145
    bcs LAB_080d9918                         @ 080d98ea 15d2
    movs r0,#0x78    @ 080d98ec 7820
    .hword 0x4680    @ 080d98ee 8046
    movs r1,#0x50    @ 080d98f0 5021
    .hword 0x468c    @ 080d98f2 8c46
    movs r2,#0x80    @ 080d98f4 8022
    lsls r2,r2,#0x3    @ 080d98f6 d200
    movs r1,#0x8    @ 080d98f8 0821
LAB_080d98fa:
    .hword 0x4640    @ 080d98fa 4046
    strh r0,[r4,#0x6]                        @ 080d98fc e080
    .hword 0x4660    @ 080d98fe 6046
    strh r0,[r4,#0x8]                        @ 080d9900 2081
    ldrh r0,[r4,#0x2]                        @ 080d9902 6088
    strh r0,[r4,#0xa]                        @ 080d9904 6081
    ldrh r0,[r4,#0x4]                        @ 080d9906 a088
    strh r0,[r4,#0xc]                        @ 080d9908 a081
    strh r2,[r4,#0xe]                        @ 080d990a e281
    str r1,[r4,#0x10]                        @ 080d990c 2161
    adds r4,#0x20    @ 080d990e 2034
    adds r1,#0x4    @ 080d9910 0431
    adds r5,#0x1    @ 080d9912 0135
    cmp r5,r6                                @ 080d9914 b542
    bcc LAB_080d98fa                         @ 080d9916 f0d3
LAB_080d9918:
    adds r0,r3,#0x0    @ 080d9918 181c
    adds r0,#0x8    @ 080d991a 0830
    strh r0,[r7,#0x6]                        @ 080d991c f880
    movs r2,#0xe3    @ 080d991e e322
    lsls r2,r2,#0x3    @ 080d9920 d200
    adds r1,r7,r2    @ 080d9922 b918
    movs r0,#0x2    @ 080d9924 0220
    ldrb r3,[r1,#0x0]                        @ 080d9926 0b78
    orrs r0,r3    @ 080d9928 1843
    strb r0,[r1,#0x0]                        @ 080d992a 0870
LAB_080d992c:
    ldrh r1,[r7,#0x1e]                       @ 080d992c f98b
    lsls r0,r1,#0x5    @ 080d992e 4801
    adds r0,#0x44    @ 080d9930 4430
    adds r4,r7,r0    @ 080d9932 3c18
    movs r5,#0x0    @ 080d9934 0025
    cmp r5,r6                                @ 080d9936 b542
    bcs LAB_080d99ca                         @ 080d9938 47d2
LAB_080d993a:
    ldr r0,[r4,#0x10]                        @ 080d993a 2069
    subs r2,r0,#0x1    @ 080d993c 421e
    str r2,[r4,#0x10]                        @ 080d993e 2261
    cmp r2,#0x7                              @ 080d9940 072a
    ble LAB_080d995c                         @ 080d9942 0bdd
    ldrh r0,[r4,#0x6]                        @ 080d9944 e088
    movs r1,#0x0    @ 080d9946 0021
    strh r0,[r4,#0x2]                        @ 080d9948 6080
    ldrh r0,[r4,#0x8]                        @ 080d994a 2089
    strh r0,[r4,#0x4]                        @ 080d994c a080
    strh r1,[r4,#0xe]                        @ 080d994e e181
    b LAB_080d99b6                           @ 080d9950 31e0
    .zero  0x2
DAT_080d9954:
    .word  pack_ui_state                  @ 080d9954 50580003
DAT_080d9958:
    .word  0x00000724                     @ 080d9958 24070000
LAB_080d995c:
    cmp r2,#0x0                              @ 080d995c 002a
    bge LAB_080d996e                         @ 080d995e 06da
    ldrh r0,[r4,#0xa]                        @ 080d9960 6089
    strh r0,[r4,#0x2]                        @ 080d9962 6080
    ldrh r0,[r4,#0xc]                        @ 080d9964 a089
    strh r0,[r4,#0x4]                        @ 080d9966 a080
    movs r0,#0x80    @ 080d9968 8020
    lsls r0,r0,#0x1    @ 080d996a 4000
    b LAB_080d99b4                           @ 080d996c 22e0
LAB_080d996e:
    movs r3,#0x6    @ 080d996e 0623
    ldrsh r0,[r4,r3]                         @ 080d9970 e05e
    movs r3,#0xa    @ 080d9972 0a23
    ldrsh r1,[r4,r3]                         @ 080d9974 e15e
    subs r0,r0,r1    @ 080d9976 401a
    muls r0,r2    @ 080d9978 5043
    movs r1,#0x8    @ 080d997a 0821
    bl bios_div                              @ 080d997c 34f03efd
    ldrh r1,[r4,#0xa]                        @ 080d9980 6189
    adds r0,r1,r0    @ 080d9982 0818
    strh r0,[r4,#0x2]                        @ 080d9984 6080
    movs r2,#0x8    @ 080d9986 0822
    ldrsh r1,[r4,r2]                         @ 080d9988 a15e
    movs r3,#0xc    @ 080d998a 0c23
    ldrsh r0,[r4,r3]                         @ 080d998c e05e
    subs r1,r1,r0    @ 080d998e 091a
    ldr r0,[r4,#0x10]                        @ 080d9990 2069
    muls r0,r1    @ 080d9992 4843
    movs r1,#0x8    @ 080d9994 0821
    bl bios_div                              @ 080d9996 34f031fd
    ldrh r1,[r4,#0xc]                        @ 080d999a a189
    adds r0,r1,r0    @ 080d999c 0818
    strh r0,[r4,#0x4]                        @ 080d999e a080
    ldr r1,[r4,#0x10]                        @ 080d99a0 2169
    lsls r0,r1,#0x1    @ 080d99a2 4800
    adds r0,r0,r1    @ 080d99a4 4018
    lsls r0,r0,#0x8    @ 080d99a6 0002
    movs r1,#0x8    @ 080d99a8 0821
    bl bios_div                              @ 080d99aa 34f027fd
    movs r2,#0x80    @ 080d99ae 8022
    lsls r2,r2,#0x1    @ 080d99b0 5200
    adds r0,r0,r2    @ 080d99b2 8018
LAB_080d99b4:
    strh r0,[r4,#0xe]                        @ 080d99b4 e081
LAB_080d99b6:
    ldr r0,[r4,#0x10]                        @ 080d99b6 2069
    cmp r0,#0x0                              @ 080d99b8 0028
    bne LAB_080d99c2                         @ 080d99ba 02d1
    movs r0,#0x4    @ 080d99bc 0420
    bl sync_state_and_init_sprite            @ 080d99be 20f079f8
LAB_080d99c2:
    adds r4,#0x20    @ 080d99c2 2034
    adds r5,#0x1    @ 080d99c4 0135
    cmp r5,r6                                @ 080d99c6 b542
    bcc LAB_080d993a                         @ 080d99c8 b7d3
LAB_080d99ca:
    ldrh r0,[r7,#0x6]                        @ 080d99ca f888
    subs r0,#0x1    @ 080d99cc 0138
    strh r0,[r7,#0x6]                        @ 080d99ce f880
    lsls r0,r0,#0x10    @ 080d99d0 0004
    cmp r0,#0x0                              @ 080d99d2 0028
    bge LAB_080d99ea                         @ 080d99d4 09da
    movs r3,#0xe3    @ 080d99d6 e323
    lsls r3,r3,#0x3    @ 080d99d8 db00
    adds r1,r7,r3    @ 080d99da f918
    movs r0,#0x3    @ 080d99dc 0320
    rsbs r0,r0,#0    @ 080d99de 4042
    ldrb r2,[r1,#0x0]                        @ 080d99e0 0a78
    ands r0,r2    @ 080d99e2 1040
    strb r0,[r1,#0x0]                        @ 080d99e4 0870
    movs r3,#0x1    @ 080d99e6 0123
    .hword 0x4699    @ 080d99e8 9946
LAB_080d99ea:
    movs r0,#0x0    @ 080d99ea 0020
    bl write_pack_banner_oam_for_all_slots   @ 080d99ec fff76afc
    .hword 0x4648    @ 080d99f0 4846
    pop {r3,r4}                              @ 080d99f2 18bc
    .hword 0x4698    @ 080d99f4 9846
    .hword 0x46a1    @ 080d99f6 a146
    pop {r4,r5,r6,r7}                        @ 080d99f8 f0bc
    pop {r1}                                 @ 080d99fa 02bc
    bx r1                                    @ 080d99fc 0847
    .zero  0x2

@ 拆包卡片详情画面的整屏渲染. 调 update_pack_slot_scroll_positions 同步槽位置, 以 OBJ VRAM 基址 0x6000000 调 render_pack_draw_counter_to_sprite_vram 画抽卡计数, 用 write_pack_name_oam_tile_sequence(0xffff, 0, 0xf) 铺卡名 OAM 图块序列. 然后对当前卡 (0xffff 占位) 与 pack_ui_state+0xc[+0x18] 选中卡各调一次 pack_detail_bg_tile_load / render_pack_banner_tile_row_a / render_pack_banner_tile_row_b / render_pack_info_stat_tile_row 加载详情 BG 图块与横幅/统计行. 随后配置 BG3CNT/BG0CNT/BG1CNT (清低 2 位优先级后分别 |=1/|=2) 与 BG 滚动寄存器, 设 pack_ui_state+0xc[+0x6] 帧计数 := 0x14. 最后若 [+0x724] bit0 置位则调 write_pack_banner_oam_for_all_slots(0). 供拆包详情画面渲染状态机调用.
render_pack_card_detail_full_screen:
    push {r4,r5,r6,lr}                       @ 080d9a00 70b5
    ldr r6, DAT_080d9ac4                     @ 080d9a02 304e
    adds r5,r6,#0x0    @ 080d9a04 351c
    adds r5,#0xc    @ 080d9a06 0c35
    movs r4,#0xc0    @ 080d9a08 c024
    lsls r4,r4,#0x13    @ 080d9a0a e404
    bl update_pack_slot_scroll_positions     @ 080d9a0c fff71efa
    adds r0,r4,#0x0    @ 080d9a10 201c
    bl render_pack_draw_counter_to_sprite_vram @ 080d9a12 02f027f8
    ldr r0, DAT_080d9ac8                     @ 080d9a16 2c48
    movs r1,#0x0    @ 080d9a18 0021
    movs r2,#0xf    @ 080d9a1a 0f22
    bl write_pack_name_oam_tile_sequence     @ 080d9a1c 02f0b0f8
    ldr r4, DAT_080d9acc                     @ 080d9a20 2a4c
    adds r0,r4,#0x0    @ 080d9a22 201c
    bl pack_detail_bg_tile_load              @ 080d9a24 fff7aefa
    ldrh r0,[r5,#0x18]                       @ 080d9a28 288b
    bl pack_detail_bg_tile_load              @ 080d9a2a fff7abfa
    adds r0,r4,#0x0    @ 080d9a2e 201c
    bl render_pack_banner_tile_row_a         @ 080d9a30 fff706fb
    ldrh r0,[r5,#0x18]                       @ 080d9a34 288b
    bl render_pack_banner_tile_row_a         @ 080d9a36 fff703fb
    adds r0,r4,#0x0    @ 080d9a3a 201c
    bl render_pack_banner_tile_row_b         @ 080d9a3c fff72efb
    ldrh r0,[r5,#0x18]                       @ 080d9a40 288b
    bl render_pack_banner_tile_row_b         @ 080d9a42 fff72bfb
    adds r0,r4,#0x0    @ 080d9a46 201c
    bl render_pack_info_stat_tile_row        @ 080d9a48 fff756fb
    ldrh r0,[r5,#0x18]                       @ 080d9a4c 288b
    bl render_pack_info_stat_tile_row        @ 080d9a4e fff753fb
    ldr r1, PTR_BG3CNT_080d9ad0              @ 080d9a52 1f49
    ldrh r2,[r1,#0x0]                        @ 080d9a54 0a88
    ldr r3, DAT_080d9ad4                     @ 080d9a56 1f4b
    adds r0,r3,#0x0    @ 080d9a58 181c
    ands r0,r2    @ 080d9a5a 1040
    strh r0,[r1,#0x0]                        @ 080d9a5c 0880
    ldrh r0,[r1,#0x0]                        @ 080d9a5e 0888
    strh r0,[r1,#0x0]                        @ 080d9a60 0880
    ldr r2, PTR_BG0CNT_080d9ad8              @ 080d9a62 1d4a
    ldrh r1,[r2,#0x0]                        @ 080d9a64 1188
    adds r0,r3,#0x0    @ 080d9a66 181c
    ands r0,r1    @ 080d9a68 0840
    strh r0,[r2,#0x0]                        @ 080d9a6a 1080
    ldrh r0,[r2,#0x0]                        @ 080d9a6c 1088
    movs r1,#0x1    @ 080d9a6e 0121
    orrs r0,r1    @ 080d9a70 0843
    strh r0,[r2,#0x0]                        @ 080d9a72 1080
    ldr r1, PTR_BG1CNT_080d9adc              @ 080d9a74 1949
    ldrh r2,[r1,#0x0]                        @ 080d9a76 0a88
    adds r0,r3,#0x0    @ 080d9a78 181c
    ands r0,r2    @ 080d9a7a 1040
    strh r0,[r1,#0x0]                        @ 080d9a7c 0880
    ldrh r0,[r1,#0x0]                        @ 080d9a7e 0888
    movs r2,#0x2    @ 080d9a80 0222
    orrs r0,r2    @ 080d9a82 1043
    strh r0,[r1,#0x0]                        @ 080d9a84 0880
    adds r1,#0x2    @ 080d9a86 0231
    ldrh r0,[r1,#0x0]                        @ 080d9a88 0888
    ands r3,r0    @ 080d9a8a 0340
    strh r3,[r1,#0x0]                        @ 080d9a8c 0b80
    ldrh r0,[r1,#0x0]                        @ 080d9a8e 0888
    orrs r0,r2    @ 080d9a90 1043
    strh r0,[r1,#0x0]                        @ 080d9a92 0880
    adds r1,#0x44    @ 080d9a94 4431
    ldr r2, DAT_080d9ae0                     @ 080d9a96 124a
    adds r0,r2,#0x0    @ 080d9a98 101c
    strh r0,[r1,#0x0]                        @ 080d9a9a 0880
    adds r1,#0x2    @ 080d9a9c 0231
    movs r0,#0x10    @ 080d9a9e 1020
    strh r0,[r1,#0x0]                        @ 080d9aa0 0880
    movs r0,#0x14    @ 080d9aa2 1420
    strh r0,[r5,#0x6]                        @ 080d9aa4 e880
    ldr r0, DAT_080d9ae4                     @ 080d9aa6 0f48
    adds r6,r6,r0    @ 080d9aa8 3618
    movs r0,#0x1    @ 080d9aaa 0120
    ldrb r6,[r6,#0x0]                        @ 080d9aac 3678
    ands r0,r6    @ 080d9aae 3040
    cmp r0,#0x0                              @ 080d9ab0 0028
    beq LAB_080d9aba                         @ 080d9ab2 02d0
    movs r0,#0x0    @ 080d9ab4 0020
    bl write_pack_banner_oam_for_all_slots   @ 080d9ab6 fff705fc
LAB_080d9aba:
    movs r0,#0x1    @ 080d9aba 0120
    pop {r4,r5,r6}                           @ 080d9abc 70bc
    pop {r1}                                 @ 080d9abe 02bc
    bx r1                                    @ 080d9ac0 0847
    .zero  0x2
DAT_080d9ac4:
    .word  pack_ui_state                  @ 080d9ac4 50580003
DAT_080d9ac8:
    .word  0x0600e426                     @ 080d9ac8 26e40006
DAT_080d9acc:
    .word  0x0000ffff                     @ 080d9acc ffff0000
PTR_BG3CNT_080d9ad0:
    .word  BG3CNT                         @ 080d9ad0 0e000004
DAT_080d9ad4:
    .word  0x0000fffc                     @ 080d9ad4 fcff0000
PTR_BG0CNT_080d9ad8:
    .word  BG0CNT                         @ 080d9ad8 08000004
PTR_BG1CNT_080d9adc:
    .word  BG1CNT                         @ 080d9adc 0a000004
DAT_080d9ae0:
    .word  0x00001748                     @ 080d9ae0 48170000
DAT_080d9ae4:
    .word  0x00000724                     @ 080d9ae4 24070000

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 4.
@ Single-frame driver for the pack list scene scroll-start fade-in. First writes DISPCNT=0x1d00
@ (BG0-BG3+OBJ all enabled). Reads frame counter [+0x6] from pack_ui_state+0xc and decrements;
@ if count>0 and <=0x13: computes BLDALPHA blend value via bios_div(count*0x10, 0x14) and writes
@ register. When count<=0: configures BG0CNT (priority 1), BG1CNT (priority 1), BG3CNT (priority 3),
@ writes BLDCNT=0x3f3f, BLDALPHA=0x1010, sets r4=1. Calls compute_pack_slot_scroll_x([+0x18]),
@ set_pack_scroll_start_pos(r0, 0x50); based on pack_ui_state+0x718 bit0: calls
@ render_pack_card_sprite_by_flip_state(0) + write_pack_banner_oam_for_all_slots(0 or 3);
@ calls render_pack_slot_highlight_oam(1 or 2). Returns r4 (0=animating, 1=complete; Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080d9b1c)
@ Returns: r0=u8 (0=fade-in in progress, 1=complete; Sub-case E adds r0,r4 @ 080d9c06)
@ Side effects:
@   [DISPCNT] (0x04000000): := 0x1d00
@   [BLDALPHA] (0x04000052): linear update while count>0, final 0x1010
@   [BG0CNT] (0x04000008): cleared then |= 1 (on complete)
@   [BG3CNT] (0x0400000e): cleared then |= 3 (on complete)
@   [BLDCNT] (0x04000050): final 0x3f3f
@   [pack_ui_state+0xc+0x6]: -=1 each frame
@ Constants:
@   pack_ui_state = 0x03005850
@   DISPCNT = 0x04000000, DISPCNT_VAL = 0x1d00
@   BLDALPHA_DIV = 0x14
@   BG0CNT = 0x04000008, BG3CNT = 0x0400000e
@   BLDCNT = 0x04000050, BLDCNT_FINAL = 0x3f3f, BLDALPHA_FINAL = 0x1010
@   SCROLL_Y = 0x50
tick_pack_list_scroll_fadein:
    push {r4,r5,lr}                          @ 080d9ae8 30b5
    ldr r0, DAT_080d9b1c                     @ 080d9aea 0c48
    adds r5,r0,#0x0    @ 080d9aec 051c
    adds r5,#0xc    @ 080d9aee 0c35
    movs r4,#0x0    @ 080d9af0 0024
    movs r1,#0x80    @ 080d9af2 8021
    lsls r1,r1,#0x13    @ 080d9af4 c904
    movs r0,#0xe8    @ 080d9af6 e820
    lsls r0,r0,#0x5    @ 080d9af8 4001
    strh r0,[r1,#0x0]                        @ 080d9afa 0880
    ldrh r1,[r5,#0x6]                        @ 080d9afc e988
    subs r1,#0x1    @ 080d9afe 0139
    strh r1,[r5,#0x6]                        @ 080d9b00 e980
    lsls r0,r1,#0x10    @ 080d9b02 0804
    asrs r2,r0,#0x10    @ 080d9b04 0214
    cmp r2,#0x0                              @ 080d9b06 002a
    ble LAB_080d9b12                         @ 080d9b08 03dd
    movs r3,#0x6    @ 080d9b0a 0623
    ldrsh r0,[r5,r3]                         @ 080d9b0c e85e
    cmp r0,#0x13                             @ 080d9b0e 1328
    bgt LAB_080d9b20                         @ 080d9b10 06dc
LAB_080d9b12:
    adds r0,r1,#0x0    @ 080d9b12 081c
    cmp r2,#0x0                              @ 080d9b14 002a
    bge LAB_080d9b22                         @ 080d9b16 04da
    movs r0,#0x0    @ 080d9b18 0020
    b LAB_080d9b22                           @ 080d9b1a 02e0
DAT_080d9b1c:
    .word  pack_ui_state                  @ 080d9b1c 50580003
LAB_080d9b20:
    movs r0,#0x14    @ 080d9b20 1420
LAB_080d9b22:
    strh r0,[r5,#0x6]                        @ 080d9b22 e880
    lsls r0,r0,#0x10    @ 080d9b24 0004
    cmp r0,#0x0                              @ 080d9b26 0028
    ble LAB_080d9b50                         @ 080d9b28 12dd
    movs r1,#0x6    @ 080d9b2a 0621
    ldrsh r0,[r5,r1]                         @ 080d9b2c 685e
    lsls r0,r0,#0x4    @ 080d9b2e 0001
    movs r1,#0x14    @ 080d9b30 1421
    bl bios_div                              @ 080d9b32 34f063fc
    ldr r3, PTR_BLDALPHA_080d9b4c            @ 080d9b36 054b
    lsls r2,r0,#0x18    @ 080d9b38 0206
    lsrs r2,r2,#0x18    @ 080d9b3a 120e
    movs r1,#0x10    @ 080d9b3c 1021
    subs r1,r1,r0    @ 080d9b3e 091a
    lsls r1,r1,#0x18    @ 080d9b40 0906
    lsrs r1,r1,#0x10    @ 080d9b42 090c
    orrs r2,r1    @ 080d9b44 0a43
    strh r2,[r3,#0x0]                        @ 080d9b46 1a80
    b LAB_080d9ba4                           @ 080d9b48 2ce0
    .zero  0x2
PTR_BLDALPHA_080d9b4c:
    .word  BLDALPHA                       @ 080d9b4c 52000004
LAB_080d9b50:
    ldr r1, PTR_BG0CNT_080d9bd0              @ 080d9b50 1f49
    ldrh r2,[r1,#0x0]                        @ 080d9b52 0a88
    ldr r3, DAT_080d9bd4                     @ 080d9b54 1f4b
    adds r0,r3,#0x0    @ 080d9b56 181c
    ands r0,r2    @ 080d9b58 1040
    strh r0,[r1,#0x0]                        @ 080d9b5a 0880
    ldrh r0,[r1,#0x0]                        @ 080d9b5c 0888
    strh r0,[r1,#0x0]                        @ 080d9b5e 0880
    adds r1,#0x2    @ 080d9b60 0231
    ldrh r2,[r1,#0x0]                        @ 080d9b62 0a88
    adds r0,r3,#0x0    @ 080d9b64 181c
    ands r0,r2    @ 080d9b66 1040
    strh r0,[r1,#0x0]                        @ 080d9b68 0880
    ldrh r0,[r1,#0x0]                        @ 080d9b6a 0888
    movs r4,#0x1    @ 080d9b6c 0124
    orrs r0,r4    @ 080d9b6e 2043
    strh r0,[r1,#0x0]                        @ 080d9b70 0880
    adds r1,#0x2    @ 080d9b72 0231
    ldrh r2,[r1,#0x0]                        @ 080d9b74 0a88
    adds r0,r3,#0x0    @ 080d9b76 181c
    ands r0,r2    @ 080d9b78 1040
    strh r0,[r1,#0x0]                        @ 080d9b7a 0880
    ldrh r0,[r1,#0x0]                        @ 080d9b7c 0888
    orrs r0,r4    @ 080d9b7e 2043
    strh r0,[r1,#0x0]                        @ 080d9b80 0880
    ldr r2, PTR_BG3CNT_080d9bd8              @ 080d9b82 154a
    ldrh r0,[r2,#0x0]                        @ 080d9b84 1088
    ands r3,r0    @ 080d9b86 0340
    strh r3,[r2,#0x0]                        @ 080d9b88 1380
    ldrh r0,[r2,#0x0]                        @ 080d9b8a 1088
    movs r1,#0x3    @ 080d9b8c 0321
    orrs r0,r1    @ 080d9b8e 0843
    strh r0,[r2,#0x0]                        @ 080d9b90 1080
    ldr r1, PTR_BLDCNT_080d9bdc              @ 080d9b92 1249
    ldr r2, DAT_080d9be0                     @ 080d9b94 124a
    adds r0,r2,#0x0    @ 080d9b96 101c
    strh r0,[r1,#0x0]                        @ 080d9b98 0880
    adds r1,#0x2    @ 080d9b9a 0231
    ldr r3, DAT_080d9be4                     @ 080d9b9c 114b
    adds r0,r3,#0x0    @ 080d9b9e 181c
    strh r0,[r1,#0x0]                        @ 080d9ba0 0880
    movs r4,#0x1    @ 080d9ba2 0124
LAB_080d9ba4:
    ldrh r0,[r5,#0x18]                       @ 080d9ba4 288b
    bl compute_pack_slot_scroll_x            @ 080d9ba6 fff727f9
    movs r1,#0x50    @ 080d9baa 5021
    bl set_pack_scroll_start_pos             @ 080d9bac faf7c8fe
    movs r0,#0xe3    @ 080d9bb0 e320
    lsls r0,r0,#0x3    @ 080d9bb2 c000
    adds r1,r5,r0    @ 080d9bb4 2918
    movs r0,#0x1    @ 080d9bb6 0120
    ldrb r1,[r1,#0x0]                        @ 080d9bb8 0978
    ands r0,r1    @ 080d9bba 0840
    cmp r0,#0x0                              @ 080d9bbc 0028
    beq LAB_080d9be8                         @ 080d9bbe 13d0
    movs r0,#0x0    @ 080d9bc0 0020
    bl render_pack_card_sprite_by_flip_state @ 080d9bc2 faf771fd
    movs r0,#0x0    @ 080d9bc6 0020
    bl write_pack_banner_oam_for_all_slots   @ 080d9bc8 fff77cfb
    b LAB_080d9bf4                           @ 080d9bcc 12e0
    .zero  0x2
PTR_BG0CNT_080d9bd0:
    .word  BG0CNT                         @ 080d9bd0 08000004
DAT_080d9bd4:
    .word  0x0000fffc                     @ 080d9bd4 fcff0000
PTR_BG3CNT_080d9bd8:
    .word  BG3CNT                         @ 080d9bd8 0e000004
PTR_BLDCNT_080d9bdc:
    .word  BLDCNT                         @ 080d9bdc 50000004
DAT_080d9be0:
    .word  0x00003f3f                     @ 080d9be0 3f3f0000
DAT_080d9be4:
    .word  0x00001010                     @ 080d9be4 10100000
LAB_080d9be8:
    movs r0,#0x0    @ 080d9be8 0020
    bl render_pack_card_sprite_by_flip_state @ 080d9bea faf75dfd
    movs r0,#0x3    @ 080d9bee 0320
    bl write_pack_banner_oam_for_all_slots   @ 080d9bf0 fff768fb
LAB_080d9bf4:
    movs r1,#0x6    @ 080d9bf4 0621
    ldrsh r0,[r5,r1]                         @ 080d9bf6 685e
    movs r1,#0x1    @ 080d9bf8 0121
    cmp r0,#0x1                              @ 080d9bfa 0128
    ble LAB_080d9c00                         @ 080d9bfc 00dd
    movs r1,#0x2    @ 080d9bfe 0221
LAB_080d9c00:
    adds r0,r1,#0x0    @ 080d9c00 081c
    bl render_pack_slot_highlight_oam        @ 080d9c02 fff725fd
    adds r0,r4,#0x0    @ 080d9c06 201c
    pop {r4,r5}                              @ 080d9c08 30bc
    pop {r1}                                 @ 080d9c0a 02bc
    bx r1                                    @ 080d9c0c 0847
    .zero  0x2

@ Scrolls the pack-select UI to center the currently selected slot. Sets pack_ui_state+0xc[+0x1a]=1 (scroll_active) and [+0x18]=1 (dir=down). Calls set_pack_scroll_step_mode to configure step size, reads [+0x18] for direction, calls get_pack_icon_y_by_dir to get target Y (=0x78=120), then calls init_pack_scroll_animation(y=0x98, step=4) to start the animation. Called from pack list scene input handler.
@ 
@ Constants:
@ - pack_ui_state=0x03005850
@ - SCROLL_ACTIVE=1 // [+0x1a] scroll activation flag
@ - DIR_DOWN=1 // [+0x18] scroll direction: 1=down
@ - SCROLL_TARGET_Y=0x98 // init_pack_scroll_animation r1 argument
@ - SCROLL_STEP=4 // init_pack_scroll_animation r2 argument
init_pack_slot_scroll_to_center:
    push {r4,lr}                             @ 080d9c10 10b5
    ldr r4, DAT_080d9c34                     @ 080d9c12 084c
    adds r4,#0xc    @ 080d9c14 0c34
    movs r0,#0x1    @ 080d9c16 0120
    strh r0,[r4,#0x1a]                       @ 080d9c18 6083
    strh r0,[r4,#0x18]                       @ 080d9c1a 2083
    bl set_pack_scroll_step_mode             @ 080d9c1c faf7acfe
    ldrh r0,[r4,#0x18]                       @ 080d9c20 208b
    bl get_pack_icon_y_by_dir                @ 080d9c22 fff70bf9
    movs r1,#0x98    @ 080d9c26 9821
    movs r2,#0x4    @ 080d9c28 0422
    bl init_pack_scroll_animation            @ 080d9c2a faf7adfe
    pop {r4}                                 @ 080d9c2e 10bc
    pop {r0}                                 @ 080d9c30 01bc
    bx r0                                    @ 080d9c32 0047
DAT_080d9c34:
    .word  pack_ui_state                  @ 080d9c34 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 5.
@ Core input+scroll frame driver for the pack list page (194 lines). Each frame reads
@ pack_visible_count (r3=total) and gPrng+0x148 input bit-field. Branches on bit1/bit0/bit4/
@ bit5/bit7/bit6/bit8: bit1=DOWN (next slot/scroll), bit0=UP (prev slot/scroll),
@ bit4=DOWN_FAST (right fast), bit5=UP_FAST (left fast), bit7=B key (cancel, calls
@ init_pack_slot_scroll_to_center), bit6=A key (confirm, calls create_pack_name_text_overlay,
@ sets step:=0x12), bit8=cancel. Each direction branch updates [+0x18] direction/slot, calls
@ compute_pack_slot_scroll_x or get_pack_icon_y_by_dir + init_pack_scroll_animation +
@ sync_state_and_init_sprite, clears pack_ui_state+0x724 bit5. On exit: if [+0x1a]=0, refreshes
@ [+0x20]=current card id + calls tick_pack_scroll_angle_strip + render_pack_icon_oam_entries;
@ unconditionally calls render_pack_card_sprite_by_flip_state(0), render_pack_slot_arrow_oam(0),
@ render_pack_card_highlight_pulse_by_mode(0), render_pack_slot_highlight_oam(1),
@ write_pack_banner_oam_for_all_slots(3). Returns r6 (0=no state change, 1=state changed).
@ 
@ Params: none (r0 immediately clobbered by ldr r4,DAT_080d9c90)
@ Returns: r0=u8 (0=continue, 1=state changed; Sub-case E adds r0,r6 @ 080d9ff0)
@ Side effects:
@   [pack_ui_state+0xc+0x18]: updated slot direction/index
@   [pack_ui_state+0xc+0x1a]: scroll active flag
@   [pack_ui_state+0xc+0x20]: := current card id (if [+0x1a]=0)
@   [pack_ui_state+0xc+0x4]: := 0x12 (on A-key confirm)
@   [pack_ui_state+0x724] byte: bit5 cleared
@ Constants:
@   pack_ui_state = 0x03005850
@   INPUT_FIELD = 0x148
@   SLOT_ENTRY_STRIDE = 0x20, SLOT_ENTRY_BASE_OFF = 0x44
@   SCROLL_Y = 0x98, SCROLL_X_BASE = 0x50
@   STATE_FLAGS_OFFSET = 0x724
@   NEXT_STATE_A_KEY = 0x12
tick_pack_list_navigation:
    push {r4,r5,r6,lr}                       @ 080d9c38 70b5
    ldr r4, DAT_080d9c90                     @ 080d9c3a 154c
    adds r5,r4,#0x0    @ 080d9c3c 251c
    adds r5,#0xc    @ 080d9c3e 0c35
    movs r6,#0x0    @ 080d9c40 0026
    bl pack_visible_count                    @ 080d9c42 fff7cbf8
    adds r3,r0,#0x0    @ 080d9c46 031c
    ldr r0, PTR_gPrng_080d9c94               @ 080d9c48 1248
    movs r1,#0xa4    @ 080d9c4a a421
    lsls r1,r1,#0x1    @ 080d9c4c 4900
    adds r0,r0,r1    @ 080d9c4e 4018
    ldrh r1,[r0,#0x0]                        @ 080d9c50 0188
    movs r0,#0x2    @ 080d9c52 0220
    ands r0,r1    @ 080d9c54 0840
    cmp r0,#0x0                              @ 080d9c56 0028
    beq LAB_080d9cec                         @ 080d9c58 48d0
    ldrh r0,[r5,#0x1a]                       @ 080d9c5a 688b
    cmp r0,#0x0                              @ 080d9c5c 0028
    bne LAB_080d9c9c                         @ 080d9c5e 1dd1
    movs r0,#0x1    @ 080d9c60 0120
    strh r0,[r5,#0x1a]                       @ 080d9c62 6883
    strh r6,[r5,#0x18]                       @ 080d9c64 2e83
    bl set_pack_scroll_step_mode             @ 080d9c66 faf787fe
    ldrh r0,[r5,#0x18]                       @ 080d9c6a 288b
    bl get_pack_icon_y_by_dir                @ 080d9c6c fff7e6f8
    movs r1,#0x98    @ 080d9c70 9821
    movs r2,#0x4    @ 080d9c72 0422
    bl init_pack_scroll_animation            @ 080d9c74 faf788fe
    movs r0,#0x1    @ 080d9c78 0120
    bl sync_state_and_init_sprite            @ 080d9c7a 1ff01bff
    ldr r2, DAT_080d9c98                     @ 080d9c7e 064a
    adds r1,r4,r2    @ 080d9c80 a118
    movs r0,#0x21    @ 080d9c82 2120
    rsbs r0,r0,#0    @ 080d9c84 4042
    ldrb r2,[r1,#0x0]                        @ 080d9c86 0a78
    ands r0,r2    @ 080d9c88 1040
    strb r0,[r1,#0x0]                        @ 080d9c8a 0870
    movs r0,#0x5    @ 080d9c8c 0520
    b LAB_080d9f86                           @ 080d9c8e 7ae1
DAT_080d9c90:
    .word  pack_ui_state                  @ 080d9c90 50580003
PTR_gPrng_080d9c94:
    .word  gPrng                          @ 080d9c94 40000003
DAT_080d9c98:
    .word  0x00000724                     @ 080d9c98 24070000
LAB_080d9c9c:
    ldrh r0,[r5,#0x18]                       @ 080d9c9c 288b
    cmp r0,#0x0                              @ 080d9c9e 0028
    beq LAB_080d9cd0                         @ 080d9ca0 16d0
    strh r6,[r5,#0x18]                       @ 080d9ca2 2e83
    movs r0,#0x0    @ 080d9ca4 0020
    bl get_pack_icon_y_by_dir                @ 080d9ca6 fff7c9f8
    movs r1,#0x98    @ 080d9caa 9821
    movs r2,#0x8    @ 080d9cac 0822
    bl init_pack_scroll_animation            @ 080d9cae faf76bfe
    movs r0,#0x1    @ 080d9cb2 0120
    bl sync_state_and_init_sprite            @ 080d9cb4 1ff0fefe
    ldr r0, DAT_080d9ccc                     @ 080d9cb8 0448
    adds r1,r4,r0    @ 080d9cba 2118
    movs r0,#0x21    @ 080d9cbc 2120
    rsbs r0,r0,#0    @ 080d9cbe 4042
    ldrb r2,[r1,#0x0]                        @ 080d9cc0 0a78
    ands r0,r2    @ 080d9cc2 1040
    strb r0,[r1,#0x0]                        @ 080d9cc4 0870
    movs r0,#0x5    @ 080d9cc6 0520
    b LAB_080d9f86                           @ 080d9cc8 5de1
    .zero  0x2
DAT_080d9ccc:
    .word  0x00000724                     @ 080d9ccc 24070000
LAB_080d9cd0:
    movs r0,#0x1    @ 080d9cd0 0120
    bl sync_state_and_init_sprite            @ 080d9cd2 1ff0effe
    ldr r1, DAT_080d9ce8                     @ 080d9cd6 0449
    adds r0,r4,r1    @ 080d9cd8 6018
    movs r1,#0x21    @ 080d9cda 2121
    rsbs r1,r1,#0    @ 080d9cdc 4942
    ldrb r2,[r0,#0x0]                        @ 080d9cde 0278
    ands r1,r2    @ 080d9ce0 1140
    strb r1,[r0,#0x0]                        @ 080d9ce2 0170
    movs r0,#0xb    @ 080d9ce4 0b20
    b LAB_080d9f86                           @ 080d9ce6 4ee1
DAT_080d9ce8:
    .word  0x00000724                     @ 080d9ce8 24070000
LAB_080d9cec:
    movs r0,#0x1    @ 080d9cec 0120
    ands r0,r1    @ 080d9cee 0840
    cmp r0,#0x0                              @ 080d9cf0 0028
    beq LAB_080d9d5c                         @ 080d9cf2 33d0
    ldrh r0,[r5,#0x1a]                       @ 080d9cf4 688b
    cmp r0,#0x0                              @ 080d9cf6 0028
    bne LAB_080d9d18                         @ 080d9cf8 0ed1
    movs r0,#0x24    @ 080d9cfa 2420
    bl sync_state_and_init_sprite            @ 080d9cfc 1ff0dafe
    ldr r1, DAT_080d9d14                     @ 080d9d00 0449
    adds r0,r4,r1    @ 080d9d02 6018
    movs r1,#0x21    @ 080d9d04 2121
    rsbs r1,r1,#0    @ 080d9d06 4942
    ldrb r2,[r0,#0x0]                        @ 080d9d08 0278
    ands r1,r2    @ 080d9d0a 1140
    strb r1,[r0,#0x0]                        @ 080d9d0c 0170
    movs r0,#0xa    @ 080d9d0e 0a20
    b LAB_080d9f86                           @ 080d9d10 39e1
    .zero  0x2
DAT_080d9d14:
    .word  0x00000724                     @ 080d9d14 24070000
LAB_080d9d18:
    ldrh r0,[r5,#0x18]                       @ 080d9d18 288b
    cmp r0,#0x0                              @ 080d9d1a 0028
    beq LAB_080d9d40                         @ 080d9d1c 10d0
    cmp r0,#0x1                              @ 080d9d1e 0128
    beq LAB_080d9d24                         @ 080d9d20 00d0
    b LAB_080d9f8a                           @ 080d9d22 32e1
LAB_080d9d24:
    movs r0,#0x24    @ 080d9d24 2420
    bl sync_state_and_init_sprite            @ 080d9d26 1ff0c5fe
    ldr r1, DAT_080d9d3c                     @ 080d9d2a 0449
    adds r0,r4,r1    @ 080d9d2c 6018
    movs r1,#0x21    @ 080d9d2e 2121
    rsbs r1,r1,#0    @ 080d9d30 4942
    ldrb r2,[r0,#0x0]                        @ 080d9d32 0278
    ands r1,r2    @ 080d9d34 1140
    strb r1,[r0,#0x0]                        @ 080d9d36 0170
    movs r0,#0xc    @ 080d9d38 0c20
    b LAB_080d9f86                           @ 080d9d3a 24e1
DAT_080d9d3c:
    .word  0x00000724                     @ 080d9d3c 24070000
LAB_080d9d40:
    movs r0,#0x1    @ 080d9d40 0120
    bl sync_state_and_init_sprite            @ 080d9d42 1ff0b7fe
    ldr r1, DAT_080d9d58                     @ 080d9d46 0449
    adds r0,r4,r1    @ 080d9d48 6018
    movs r1,#0x21    @ 080d9d4a 2121
    rsbs r1,r1,#0    @ 080d9d4c 4942
    ldrb r2,[r0,#0x0]                        @ 080d9d4e 0278
    ands r1,r2    @ 080d9d50 1140
    strb r1,[r0,#0x0]                        @ 080d9d52 0170
    movs r0,#0xb    @ 080d9d54 0b20
    b LAB_080d9f86                           @ 080d9d56 16e1
DAT_080d9d58:
    .word  0x00000724                     @ 080d9d58 24070000
LAB_080d9d5c:
    movs r0,#0x10    @ 080d9d5c 1020
    ands r0,r1    @ 080d9d5e 0840
    cmp r0,#0x0                              @ 080d9d60 0028
    beq LAB_080d9e24                         @ 080d9d62 5fd0
    ldrh r0,[r5,#0x1a]                       @ 080d9d64 688b
    cmp r0,#0x0                              @ 080d9d66 0028
    bne LAB_080d9ddc                         @ 080d9d68 38d1
    ldrh r1,[r5,#0x18]                       @ 080d9d6a 298b
    subs r0,r3,#0x1    @ 080d9d6c 581e
    cmp r1,r0                                @ 080d9d6e 8142
    bcs LAB_080d9da0                         @ 080d9d70 16d2
    adds r0,r1,#0x1    @ 080d9d72 481c
    strh r0,[r5,#0x18]                       @ 080d9d74 2883
    ldrh r0,[r5,#0x18]                       @ 080d9d76 288b
    bl compute_pack_slot_scroll_x            @ 080d9d78 fff73ef8
    movs r1,#0x50    @ 080d9d7c 5021
    movs r2,#0x8    @ 080d9d7e 0822
    bl init_pack_scroll_animation            @ 080d9d80 faf702fe
    movs r0,#0x0    @ 080d9d84 0020
    bl sync_state_and_init_sprite            @ 080d9d86 1ff095fe
    ldr r0, DAT_080d9d9c                     @ 080d9d8a 0448
    adds r1,r4,r0    @ 080d9d8c 2118
    movs r0,#0x21    @ 080d9d8e 2120
    rsbs r0,r0,#0    @ 080d9d90 4042
    ldrb r2,[r1,#0x0]                        @ 080d9d92 0a78
    ands r0,r2    @ 080d9d94 1040
    strb r0,[r1,#0x0]                        @ 080d9d96 0870
    movs r0,#0x5    @ 080d9d98 0520
    b LAB_080d9f86                           @ 080d9d9a f4e0
DAT_080d9d9c:
    .word  0x00000724                     @ 080d9d9c 24070000
LAB_080d9da0:
    ldrh r2,[r5,#0x1e]                       @ 080d9da0 ea8b
    adds r0,r2,r1    @ 080d9da2 5018
    adds r0,#0x1    @ 080d9da4 0130
    ldrh r1,[r5,#0x8]                        @ 080d9da6 2989
    cmp r0,r1                                @ 080d9da8 8842
    bge LAB_080d9dd0                         @ 080d9daa 11da
    ldr r2, DAT_080d9dcc                     @ 080d9dac 074a
    adds r4,r4,r2    @ 080d9dae a418
    movs r0,#0x4    @ 080d9db0 0420
    ldrb r1,[r4,#0x0]                        @ 080d9db2 2178
    orrs r0,r1    @ 080d9db4 0843
    strb r0,[r4,#0x0]                        @ 080d9db6 2070
    movs r0,#0x0    @ 080d9db8 0020
    bl sync_state_and_init_sprite            @ 080d9dba 1ff07bfe
    movs r0,#0x21    @ 080d9dbe 2120
    rsbs r0,r0,#0    @ 080d9dc0 4042
    ldrb r2,[r4,#0x0]                        @ 080d9dc2 2278
    ands r0,r2    @ 080d9dc4 1040
    strb r0,[r4,#0x0]                        @ 080d9dc6 2070
    movs r0,#0x7    @ 080d9dc8 0720
    b LAB_080d9f86                           @ 080d9dca dce0
DAT_080d9dcc:
    .word  0x00000724                     @ 080d9dcc 24070000
LAB_080d9dd0:
    ldr r0, DAT_080d9dd8                     @ 080d9dd0 0148
    adds r4,r4,r0    @ 080d9dd2 2418
    movs r0,#0x20    @ 080d9dd4 2020
    b LAB_080d9f42                           @ 080d9dd6 b4e0
DAT_080d9dd8:
    .word  0x00000724                     @ 080d9dd8 24070000
LAB_080d9ddc:
    cmp r0,#0x1                              @ 080d9ddc 0128
    beq LAB_080d9de2                         @ 080d9dde 00d0
    b LAB_080d9f8a                           @ 080d9de0 d3e0
LAB_080d9de2:
    ldrh r0,[r5,#0x18]                       @ 080d9de2 288b
    cmp r0,#0x0                              @ 080d9de4 0028
    bne LAB_080d9e18                         @ 080d9de6 17d1
    adds r0,#0x1    @ 080d9de8 0130
    strh r0,[r5,#0x18]                       @ 080d9dea 2883
    ldrh r0,[r5,#0x18]                       @ 080d9dec 288b
    bl get_pack_icon_y_by_dir                @ 080d9dee fff725f8
    movs r1,#0x98    @ 080d9df2 9821
    movs r2,#0x8    @ 080d9df4 0822
    bl init_pack_scroll_animation            @ 080d9df6 faf7c7fd
    movs r0,#0x0    @ 080d9dfa 0020
    bl sync_state_and_init_sprite            @ 080d9dfc 1ff05afe
    ldr r0, DAT_080d9e14                     @ 080d9e00 0448
    adds r1,r4,r0    @ 080d9e02 2118
    movs r0,#0x21    @ 080d9e04 2120
    rsbs r0,r0,#0    @ 080d9e06 4042
    ldrb r2,[r1,#0x0]                        @ 080d9e08 0a78
    ands r0,r2    @ 080d9e0a 1040
    strb r0,[r1,#0x0]                        @ 080d9e0c 0870
    movs r0,#0x5    @ 080d9e0e 0520
    b LAB_080d9f86                           @ 080d9e10 b9e0
    .zero  0x2
DAT_080d9e14:
    .word  0x00000724                     @ 080d9e14 24070000
LAB_080d9e18:
    ldr r0, DAT_080d9e20                     @ 080d9e18 0148
    adds r4,r4,r0    @ 080d9e1a 2418
    movs r0,#0x20    @ 080d9e1c 2020
    b LAB_080d9f42                           @ 080d9e1e 90e0
DAT_080d9e20:
    .word  0x00000724                     @ 080d9e20 24070000
LAB_080d9e24:
    movs r2,#0x20    @ 080d9e24 2022
    adds r0,r2,#0x0    @ 080d9e26 101c
    ands r0,r1    @ 080d9e28 0840
    cmp r0,#0x0                              @ 080d9e2a 0028
    beq LAB_080d9ecc                         @ 080d9e2c 4ed0
    ldrh r0,[r5,#0x1a]                       @ 080d9e2e 688b
    cmp r0,#0x0                              @ 080d9e30 0028
    bne LAB_080d9e94                         @ 080d9e32 2fd1
    ldrh r0,[r5,#0x18]                       @ 080d9e34 288b
    cmp r0,#0x0                              @ 080d9e36 0028
    beq LAB_080d9e68                         @ 080d9e38 16d0
    subs r0,#0x1    @ 080d9e3a 0138
    strh r0,[r5,#0x18]                       @ 080d9e3c 2883
    ldrh r0,[r5,#0x18]                       @ 080d9e3e 288b
    bl compute_pack_slot_scroll_x            @ 080d9e40 fef7daff
    movs r1,#0x50    @ 080d9e44 5021
    movs r2,#0x8    @ 080d9e46 0822
    bl init_pack_scroll_animation            @ 080d9e48 faf79efd
    movs r0,#0x0    @ 080d9e4c 0020
    bl sync_state_and_init_sprite            @ 080d9e4e 1ff031fe
    ldr r0, DAT_080d9e64                     @ 080d9e52 0448
    adds r1,r4,r0    @ 080d9e54 2118
    movs r0,#0x21    @ 080d9e56 2120
    rsbs r0,r0,#0    @ 080d9e58 4042
    ldrb r2,[r1,#0x0]                        @ 080d9e5a 0a78
    ands r0,r2    @ 080d9e5c 1040
    strb r0,[r1,#0x0]                        @ 080d9e5e 0870
    movs r0,#0x5    @ 080d9e60 0520
    b LAB_080d9f86                           @ 080d9e62 90e0
DAT_080d9e64:
    .word  0x00000724                     @ 080d9e64 24070000
LAB_080d9e68:
    ldrh r0,[r5,#0x1e]                       @ 080d9e68 e88b
    cmp r0,#0x4                              @ 080d9e6a 0428
    bls LAB_080d9f3c                         @ 080d9e6c 66d9
    ldr r1, DAT_080d9e90                     @ 080d9e6e 0849
    adds r4,r4,r1    @ 080d9e70 6418
    movs r0,#0x5    @ 080d9e72 0520
    rsbs r0,r0,#0    @ 080d9e74 4042
    ldrb r2,[r4,#0x0]                        @ 080d9e76 2278
    ands r0,r2    @ 080d9e78 1040
    strb r0,[r4,#0x0]                        @ 080d9e7a 2070
    movs r0,#0x0    @ 080d9e7c 0020
    bl sync_state_and_init_sprite            @ 080d9e7e 1ff019fe
    movs r0,#0x21    @ 080d9e82 2120
    rsbs r0,r0,#0    @ 080d9e84 4042
    ldrb r1,[r4,#0x0]                        @ 080d9e86 2178
    ands r0,r1    @ 080d9e88 0840
    strb r0,[r4,#0x0]                        @ 080d9e8a 2070
    movs r0,#0x7    @ 080d9e8c 0720
    b LAB_080d9f86                           @ 080d9e8e 7ae0
DAT_080d9e90:
    .word  0x00000724                     @ 080d9e90 24070000
LAB_080d9e94:
    cmp r0,#0x1                              @ 080d9e94 0128
    bne LAB_080d9f8a                         @ 080d9e96 78d1
    ldrh r0,[r5,#0x18]                       @ 080d9e98 288b
    cmp r0,#0x0                              @ 080d9e9a 0028
    beq LAB_080d9f3c                         @ 080d9e9c 4ed0
    subs r0,#0x1    @ 080d9e9e 0138
    strh r0,[r5,#0x18]                       @ 080d9ea0 2883
    ldrh r0,[r5,#0x18]                       @ 080d9ea2 288b
    bl get_pack_icon_y_by_dir                @ 080d9ea4 fef7caff
    movs r1,#0x98    @ 080d9ea8 9821
    movs r2,#0x8    @ 080d9eaa 0822
    bl init_pack_scroll_animation            @ 080d9eac faf76cfd
    movs r0,#0x0    @ 080d9eb0 0020
    bl sync_state_and_init_sprite            @ 080d9eb2 1ff0fffd
    ldr r0, DAT_080d9ec8                     @ 080d9eb6 0448
    adds r1,r4,r0    @ 080d9eb8 2118
    movs r0,#0x21    @ 080d9eba 2120
    rsbs r0,r0,#0    @ 080d9ebc 4042
    ldrb r2,[r1,#0x0]                        @ 080d9ebe 0a78
    ands r0,r2    @ 080d9ec0 1040
    strb r0,[r1,#0x0]                        @ 080d9ec2 0870
    movs r0,#0x5    @ 080d9ec4 0520
    b LAB_080d9f86                           @ 080d9ec6 5ee0
DAT_080d9ec8:
    .word  0x00000724                     @ 080d9ec8 24070000
LAB_080d9ecc:
    movs r0,#0x80    @ 080d9ecc 8020
    ands r0,r1    @ 080d9ece 0840
    cmp r0,#0x0                              @ 080d9ed0 0028
    beq LAB_080d9efc                         @ 080d9ed2 13d0
    ldrh r0,[r5,#0x1a]                       @ 080d9ed4 688b
    cmp r0,#0x0                              @ 080d9ed6 0028
    bne LAB_080d9f3c                         @ 080d9ed8 30d1
    movs r0,#0x0    @ 080d9eda 0020
    bl sync_state_and_init_sprite            @ 080d9edc 1ff0eafd
    ldr r1, DAT_080d9ef8                     @ 080d9ee0 0549
    adds r0,r4,r1    @ 080d9ee2 6018
    movs r1,#0x21    @ 080d9ee4 2121
    rsbs r1,r1,#0    @ 080d9ee6 4942
    ldrb r2,[r0,#0x0]                        @ 080d9ee8 0278
    ands r1,r2    @ 080d9eea 1140
    strb r1,[r0,#0x0]                        @ 080d9eec 0170
    bl init_pack_slot_scroll_to_center       @ 080d9eee fff78ffe
    movs r0,#0x5    @ 080d9ef2 0520
    b LAB_080d9f86                           @ 080d9ef4 47e0
    .zero  0x2
DAT_080d9ef8:
    .word  0x00000724                     @ 080d9ef8 24070000
LAB_080d9efc:
    movs r0,#0x40    @ 080d9efc 4020
    ands r0,r1    @ 080d9efe 0840
    cmp r0,#0x0                              @ 080d9f00 0028
    beq LAB_080d9f60                         @ 080d9f02 2dd0
    ldrh r0,[r5,#0x1a]                       @ 080d9f04 688b
    cmp r0,#0x1                              @ 080d9f06 0128
    bne LAB_080d9f3c                         @ 080d9f08 18d1
    lsrs r0,r3,#0x1    @ 080d9f0a 5808
    strh r0,[r5,#0x18]                       @ 080d9f0c 2883
    strh r6,[r5,#0x1a]                       @ 080d9f0e 6e83
    ldrh r0,[r5,#0x18]                       @ 080d9f10 288b
    bl compute_pack_slot_scroll_x            @ 080d9f12 fef771ff
    movs r1,#0x50    @ 080d9f16 5021
    movs r2,#0x4    @ 080d9f18 0422
    bl init_pack_scroll_animation            @ 080d9f1a faf735fd
    movs r0,#0x0    @ 080d9f1e 0020
    bl sync_state_and_init_sprite            @ 080d9f20 1ff0c8fd
    ldr r2, DAT_080d9f38                     @ 080d9f24 044a
    adds r1,r4,r2    @ 080d9f26 a118
    movs r0,#0x21    @ 080d9f28 2120
    rsbs r0,r0,#0    @ 080d9f2a 4042
    ldrb r2,[r1,#0x0]                        @ 080d9f2c 0a78
    ands r0,r2    @ 080d9f2e 1040
    strb r0,[r1,#0x0]                        @ 080d9f30 0870
    movs r0,#0x5    @ 080d9f32 0520
    b LAB_080d9f86                           @ 080d9f34 27e0
    .zero  0x2
DAT_080d9f38:
    .word  0x00000724                     @ 080d9f38 24070000
LAB_080d9f3c:
    ldr r0, DAT_080d9f5c                     @ 080d9f3c 0748
    adds r4,r4,r0    @ 080d9f3e 2418
    adds r0,r2,#0x0    @ 080d9f40 101c
LAB_080d9f42:
    ldrb r1,[r4,#0x0]                        @ 080d9f42 2178
    ands r0,r1    @ 080d9f44 0840
    cmp r0,#0x0                              @ 080d9f46 0028
    bne LAB_080d9f8a                         @ 080d9f48 1fd1
    movs r0,#0x2    @ 080d9f4a 0220
    bl sync_state_and_init_sprite            @ 080d9f4c 1ff0b2fd
    movs r0,#0x20    @ 080d9f50 2020
    ldrb r2,[r4,#0x0]                        @ 080d9f52 2278
    orrs r0,r2    @ 080d9f54 1043
    strb r0,[r4,#0x0]                        @ 080d9f56 2070
    b LAB_080d9f8a                           @ 080d9f58 17e0
    .zero  0x2
DAT_080d9f5c:
    .word  0x00000724                     @ 080d9f5c 24070000
LAB_080d9f60:
    movs r0,#0x80    @ 080d9f60 8020
    lsls r0,r0,#0x1    @ 080d9f62 4000
    ands r0,r1    @ 080d9f64 0840
    cmp r0,#0x0                              @ 080d9f66 0028
    beq LAB_080d9f8a                         @ 080d9f68 0fd0
    ldrh r0,[r5,#0x1a]                       @ 080d9f6a 688b
    cmp r0,#0x0                              @ 080d9f6c 0028
    bne LAB_080d9f8a                         @ 080d9f6e 0cd1
    ldrh r1,[r5,#0x1e]                       @ 080d9f70 e98b
    lsls r0,r1,#0x5    @ 080d9f72 4801
    adds r0,#0x44    @ 080d9f74 4430
    adds r0,r0,r5    @ 080d9f76 4019
    ldrh r2,[r5,#0x18]                       @ 080d9f78 2a8b
    lsls r1,r2,#0x5    @ 080d9f7a 5101
    adds r0,r0,r1    @ 080d9f7c 4018
    ldrh r0,[r0,#0x0]                        @ 080d9f7e 0088
    bl create_pack_name_text_overlay         @ 080d9f80 02f054fc
    movs r0,#0x12    @ 080d9f84 1220
LAB_080d9f86:
    strh r0,[r5,#0x4]                        @ 080d9f86 a880
    movs r6,#0x1    @ 080d9f88 0126
LAB_080d9f8a:
    cmp r6,#0x1                              @ 080d9f8a 012e
    beq LAB_080d9fa0                         @ 080d9f8c 08d0
    ldr r0, PTR_gPrng_080d9ff8               @ 080d9f8e 1a48
    movs r2,#0xa3    @ 080d9f90 a322
    lsls r2,r2,#0x1    @ 080d9f92 5200
    adds r1,r0,r2    @ 080d9f94 8118
    movs r0,#0xf0    @ 080d9f96 f020
    ldrh r1,[r1,#0x0]                        @ 080d9f98 0988
    ands r0,r1    @ 080d9f9a 0840
    cmp r0,#0x0                              @ 080d9f9c 0028
    bne LAB_080d9fb0                         @ 080d9f9e 07d1
LAB_080d9fa0:
    movs r0,#0xe3    @ 080d9fa0 e320
    lsls r0,r0,#0x3    @ 080d9fa2 c000
    adds r1,r5,r0    @ 080d9fa4 2918
    movs r0,#0x21    @ 080d9fa6 2120
    rsbs r0,r0,#0    @ 080d9fa8 4042
    ldrb r2,[r1,#0x0]                        @ 080d9faa 0a78
    ands r0,r2    @ 080d9fac 1040
    strb r0,[r1,#0x0]                        @ 080d9fae 0870
LAB_080d9fb0:
    ldrh r0,[r5,#0x1a]                       @ 080d9fb0 688b
    cmp r0,#0x0                              @ 080d9fb2 0028
    bne LAB_080d9fd2                         @ 080d9fb4 0dd1
    ldrh r1,[r5,#0x1e]                       @ 080d9fb6 e98b
    lsls r0,r1,#0x5    @ 080d9fb8 4801
    adds r0,#0x44    @ 080d9fba 4430
    adds r0,r5,r0    @ 080d9fbc 2818
    ldrh r2,[r5,#0x18]                       @ 080d9fbe 2a8b
    lsls r1,r2,#0x5    @ 080d9fc0 5101
    adds r0,r0,r1    @ 080d9fc2 4018
    ldrh r0,[r0,#0x0]                        @ 080d9fc4 0088
    strh r0,[r5,#0x20]                       @ 080d9fc6 2884
    bl tick_pack_scroll_angle_strip          @ 080d9fc8 fff710f8
    movs r0,#0x0    @ 080d9fcc 0020
    bl render_pack_icon_oam_entries          @ 080d9fce fff797fa
LAB_080d9fd2:
    movs r0,#0x0    @ 080d9fd2 0020
    bl render_pack_card_sprite_by_flip_state @ 080d9fd4 faf768fb
    movs r0,#0x0    @ 080d9fd8 0020
    bl render_pack_slot_arrow_oam            @ 080d9fda fff7f9fa
    movs r0,#0x0    @ 080d9fde 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080d9fe0 fff7acf9
    movs r0,#0x1    @ 080d9fe4 0120
    bl render_pack_slot_highlight_oam        @ 080d9fe6 fff733fb
    movs r0,#0x3    @ 080d9fea 0320
    bl write_pack_banner_oam_for_all_slots   @ 080d9fec fff76af9
    adds r0,r6,#0x0    @ 080d9ff0 301c
    pop {r4,r5,r6}                           @ 080d9ff2 70bc
    pop {r1}                                 @ 080d9ff4 02bc
    bx r1                                    @ 080d9ff6 0847
PTR_gPrng_080d9ff8:
    .word  gPrng                          @ 080d9ff8 40000003

@ 拆包卡槽 "收拢" 滚动布局帧. 取 pack_visible_count 得可见卡数 (r6). 若 pack_ui_state+0x724 状态字 bit1 未置位 (首次进入), 调 update_pack_slot_scroll_positions 同步, 并为每个可见槽设置插值: 据 [+0x724] bit2 选两种目标 X (0xffe0 或居中偏移), 缩放目标 0x100, 帧计数 [+0x10] 按槽序号偏置 8. 之后对各槽递减 [+0x10] 计数并经 bios_div 线性插值更新 [+0x2]/[+0x4]/[+0xe]. 然后对 0xffff 占位卡调 pack_detail_bg_tile_load / render_pack_banner_tile_row_a/b 重绘详情, 设帧计数 [+0x6] := 8 与 [+0x724] bit1. 供拆包收拢滚动状态机帧驱动.
layout_pack_slots_scroll_collapsed:
    push {r4,r5,r6,r7,lr}                    @ 080d9ffc f0b5
    .hword 0x4657    @ 080d9ffe 5746
    .hword 0x464e    @ 080da000 4e46
    .hword 0x4645    @ 080da002 4546
    push {r5,r6,r7}                          @ 080da004 e0b4
    ldr r0, DAT_080da070                     @ 080da006 1a48
    .hword 0x4680    @ 080da008 8046
    .hword 0x4647    @ 080da00a 4746
    adds r7,#0xc    @ 080da00c 0c37
    bl pack_visible_count                    @ 080da00e fef7e5fe
    adds r6,r0,#0x0    @ 080da012 061c
    movs r1,#0x0    @ 080da014 0021
    .hword 0x468a    @ 080da016 8a46
    ldr r1, DAT_080da074                     @ 080da018 1649
    add r1,r8                                @ 080da01a 4144
    movs r0,#0x2    @ 080da01c 0220
    ldrb r1,[r1,#0x0]                        @ 080da01e 0978
    ands r0,r1    @ 080da020 0840
    cmp r0,#0x0                              @ 080da022 0028
    bne LAB_080da0be                         @ 080da024 4bd1
    bl update_pack_slot_scroll_positions     @ 080da026 fef711ff
    ldrh r2,[r7,#0x1e]                       @ 080da02a fa8b
    lsls r0,r2,#0x5    @ 080da02c 5001
    adds r0,#0x44    @ 080da02e 4430
    adds r4,r0,r7    @ 080da030 c419
    movs r5,#0x0    @ 080da032 0025
    lsls r3,r6,#0x1    @ 080da034 7300
    .hword 0x4699    @ 080da036 9946
    cmp r10,r6                               @ 080da038 b245
    bcs LAB_080da096                         @ 080da03a 2cd2
    ldr r3, DAT_080da074                     @ 080da03c 0d4b
    add r3,r8                                @ 080da03e 4344
    ldr r0, DAT_080da078                     @ 080da040 0d48
    .hword 0x4680    @ 080da042 8046
    movs r2,#0x50    @ 080da044 5022
LAB_080da046:
    ldrh r0,[r4,#0x2]                        @ 080da046 6088
    strh r0,[r4,#0x6]                        @ 080da048 e080
    ldrh r0,[r4,#0x4]                        @ 080da04a a088
    strh r0,[r4,#0x8]                        @ 080da04c 2081
    movs r0,#0x80    @ 080da04e 8020
    lsls r0,r0,#0x1    @ 080da050 4000
    strh r0,[r4,#0xe]                        @ 080da052 e081
    movs r0,#0x4    @ 080da054 0420
    ldrb r1,[r3,#0x0]                        @ 080da056 1978
    ands r0,r1    @ 080da058 0840
    cmp r0,#0x0                              @ 080da05a 0028
    beq LAB_080da07c                         @ 080da05c 0ed0
    .hword 0x4640    @ 080da05e 4046
    strh r0,[r4,#0xa]                        @ 080da060 6081
    strh r2,[r4,#0xc]                        @ 080da062 a281
    lsls r0,r5,#0x1    @ 080da064 6800
    adds r0,#0x8    @ 080da066 0830
    str r0,[r4,#0x10]                        @ 080da068 2061
    adds r1,r5,#0x1    @ 080da06a 691c
    b LAB_080da08e                           @ 080da06c 0fe0
    .zero  0x2
DAT_080da070:
    .word  pack_ui_state                  @ 080da070 50580003
DAT_080da074:
    .word  0x00000724                     @ 080da074 24070000
DAT_080da078:
    .word  0x0000ffe0                     @ 080da078 e0ff0000
LAB_080da07c:
    movs r0,#0x88    @ 080da07c 8820
    lsls r0,r0,#0x1    @ 080da07e 4000
    strh r0,[r4,#0xa]                        @ 080da080 6081
    strh r2,[r4,#0xc]                        @ 080da082 a281
    adds r1,r5,#0x1    @ 080da084 691c
    subs r0,r6,r1    @ 080da086 701a
    lsls r0,r0,#0x1    @ 080da088 4000
    adds r0,#0x8    @ 080da08a 0830
    str r0,[r4,#0x10]                        @ 080da08c 2061
LAB_080da08e:
    adds r4,#0x20    @ 080da08e 2034
    adds r5,r1,#0x0    @ 080da090 0d1c
    cmp r5,r6                                @ 080da092 b542
    bcc LAB_080da046                         @ 080da094 d7d3
LAB_080da096:
    ldr r4, DAT_080da0e0                     @ 080da096 124c
    adds r0,r4,#0x0    @ 080da098 201c
    bl pack_detail_bg_tile_load              @ 080da09a fef773ff
    adds r0,r4,#0x0    @ 080da09e 201c
    bl render_pack_banner_tile_row_a         @ 080da0a0 fef7ceff
    adds r0,r4,#0x0    @ 080da0a4 201c
    bl render_pack_banner_tile_row_b         @ 080da0a6 fef7f9ff
    .hword 0x4648    @ 080da0aa 4846
    adds r0,#0x8    @ 080da0ac 0830
    strh r0,[r7,#0x6]                        @ 080da0ae f880
    movs r2,#0xe3    @ 080da0b0 e322
    lsls r2,r2,#0x3    @ 080da0b2 d200
    adds r1,r7,r2    @ 080da0b4 b918
    movs r0,#0x2    @ 080da0b6 0220
    ldrb r3,[r1,#0x0]                        @ 080da0b8 0b78
    orrs r0,r3    @ 080da0ba 1843
    strb r0,[r1,#0x0]                        @ 080da0bc 0870
LAB_080da0be:
    ldrh r1,[r7,#0x1e]                       @ 080da0be f98b
    lsls r0,r1,#0x5    @ 080da0c0 4801
    adds r0,#0x44    @ 080da0c2 4430
    adds r4,r7,r0    @ 080da0c4 3c18
    movs r5,#0x0    @ 080da0c6 0025
    cmp r5,r6                                @ 080da0c8 b542
    bcs LAB_080da12a                         @ 080da0ca 2ed2
LAB_080da0cc:
    ldr r0,[r4,#0x10]                        @ 080da0cc 2069
    subs r2,r0,#0x1    @ 080da0ce 421e
    str r2,[r4,#0x10]                        @ 080da0d0 2261
    cmp r2,#0x7                              @ 080da0d2 072a
    ble LAB_080da0e4                         @ 080da0d4 06dd
    ldrh r0,[r4,#0x6]                        @ 080da0d6 e088
    strh r0,[r4,#0x2]                        @ 080da0d8 6080
    ldrh r0,[r4,#0x8]                        @ 080da0da 2089
    b LAB_080da120                           @ 080da0dc 20e0
    .zero  0x2
DAT_080da0e0:
    .word  0x0000ffff                     @ 080da0e0 ffff0000
LAB_080da0e4:
    cmp r2,#0x0                              @ 080da0e4 002a
    bge LAB_080da0f0                         @ 080da0e6 03da
    ldrh r0,[r4,#0xa]                        @ 080da0e8 6089
    strh r0,[r4,#0x2]                        @ 080da0ea 6080
    ldrh r0,[r4,#0xc]                        @ 080da0ec a089
    b LAB_080da120                           @ 080da0ee 17e0
LAB_080da0f0:
    movs r3,#0x6    @ 080da0f0 0623
    ldrsh r0,[r4,r3]                         @ 080da0f2 e05e
    movs r3,#0xa    @ 080da0f4 0a23
    ldrsh r1,[r4,r3]                         @ 080da0f6 e15e
    subs r0,r0,r1    @ 080da0f8 401a
    muls r0,r2    @ 080da0fa 5043
    movs r1,#0x8    @ 080da0fc 0821
    bl bios_div                              @ 080da0fe 34f07df9
    ldrh r1,[r4,#0xa]                        @ 080da102 6189
    adds r0,r1,r0    @ 080da104 0818
    strh r0,[r4,#0x2]                        @ 080da106 6080
    movs r2,#0x8    @ 080da108 0822
    ldrsh r1,[r4,r2]                         @ 080da10a a15e
    movs r3,#0xc    @ 080da10c 0c23
    ldrsh r0,[r4,r3]                         @ 080da10e e05e
    subs r1,r1,r0    @ 080da110 091a
    ldr r0,[r4,#0x10]                        @ 080da112 2069
    muls r0,r1    @ 080da114 4843
    movs r1,#0x8    @ 080da116 0821
    bl bios_div                              @ 080da118 34f070f9
    ldrh r1,[r4,#0xc]                        @ 080da11c a189
    adds r0,r1,r0    @ 080da11e 0818
LAB_080da120:
    strh r0,[r4,#0x4]                        @ 080da120 a080
    adds r4,#0x20    @ 080da122 2034
    adds r5,#0x1    @ 080da124 0135
    cmp r5,r6                                @ 080da126 b542
    bcc LAB_080da0cc                         @ 080da128 d0d3
LAB_080da12a:
    ldrh r0,[r7,#0x6]                        @ 080da12a f888
    subs r0,#0x1    @ 080da12c 0138
    strh r0,[r7,#0x6]                        @ 080da12e f880
    movs r0,#0x1    @ 080da130 0120
    bl render_pack_slot_highlight_oam        @ 080da132 fff78dfa
    movs r0,#0x3    @ 080da136 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da138 fff7c4f8
    movs r2,#0x6    @ 080da13c 0622
    ldrsh r0,[r7,r2]                         @ 080da13e b85e
    cmp r0,#0x0                              @ 080da140 0028
    bge LAB_080da184                         @ 080da142 1fda
    movs r3,#0xe3    @ 080da144 e323
    lsls r3,r3,#0x3    @ 080da146 db00
    adds r1,r7,r3    @ 080da148 f918
    movs r0,#0x4    @ 080da14a 0420
    ldrb r1,[r1,#0x0]                        @ 080da14c 0978
    ands r0,r1    @ 080da14e 0840
    cmp r0,#0x0                              @ 080da150 0028
    beq LAB_080da15a                         @ 080da152 02d0
    ldrh r1,[r7,#0x1e]                       @ 080da154 f98b
    adds r0,r1,r6    @ 080da156 8819
    b LAB_080da15e                           @ 080da158 01e0
LAB_080da15a:
    ldrh r0,[r7,#0x1e]                       @ 080da15a f88b
    subs r0,#0x5    @ 080da15c 0538
LAB_080da15e:
    strh r0,[r7,#0x1e]                       @ 080da15e f883
    bl pack_visible_count                    @ 080da160 fef73cfe
    bl render_pack_slot_counts_to_bg_vram    @ 080da164 fef7e2ff
    movs r0,#0x0    @ 080da168 0020
    strh r0,[r7,#0x6]                        @ 080da16a f880
    movs r2,#0xe3    @ 080da16c e322
    lsls r2,r2,#0x3    @ 080da16e d200
    adds r1,r7,r2    @ 080da170 b918
    subs r0,#0x3    @ 080da172 0338
    ldrb r3,[r1,#0x0]                        @ 080da174 0b78
    ands r0,r3    @ 080da176 1840
    strb r0,[r1,#0x0]                        @ 080da178 0870
    ldr r1, DAT_080da194                     @ 080da17a 0649
    movs r0,#0x8    @ 080da17c 0820
    strh r0,[r1,#0x10]                       @ 080da17e 0882
    movs r0,#0x1    @ 080da180 0120
    .hword 0x4682    @ 080da182 8246
LAB_080da184:
    .hword 0x4650    @ 080da184 5046
    pop {r3,r4,r5}                           @ 080da186 38bc
    .hword 0x4698    @ 080da188 9846
    .hword 0x46a1    @ 080da18a a146
    .hword 0x46aa    @ 080da18c aa46
    pop {r4,r5,r6,r7}                        @ 080da18e f0bc
    pop {r1}                                 @ 080da190 02bc
    bx r1                                    @ 080da192 0847
DAT_080da194:
    .word  pack_ui_state                  @ 080da194 50580003

@ Called by the pack slot initialization frame driver (indeg=0, Sub-type A), advances one slot's initialization per frame and renders the highlight. Reads pack_ui_state+0xc[+6] (current slot index), calls pack_entry_init(slot_idx) to initialize that slot, then increments [+6] by 1 and writes back. If the new slot index >= pack_visible_count (all slots complete), writes [+4]=9 to advance the state machine and sets r6=1. Finally calls render_pack_slot_highlight_oam(1) to update the slot highlight OAM. Returns r6: 0 (slots still pending) or 1 (all slots complete; Sub-case E pop{r1};bx r1).
@ 
@ Constants:
@ - SLOT_IDX_OFFSET = 0x6 (ldrsh/strh [r5,#0x6] = current slot index field)
@ - NEXT_STATE = 9 (strh 9,[r5,#0x4] = advance state when all slots done)
@ - HIGHLIGHT_MODE = 1 (render_pack_slot_highlight_oam(1) = highlight mode parameter)
advance_pack_entry_with_slot_highlight:
    push {r4,r5,r6,lr}                       @ 080da198 70b5
    ldr r0, DAT_080da1d4                     @ 080da19a 0e48
    adds r5,r0,#0x0    @ 080da19c 051c
    adds r5,#0xc    @ 080da19e 0c35
    movs r6,#0x0    @ 080da1a0 0026
    bl pack_visible_count                    @ 080da1a2 fef71bfe
    adds r4,r0,#0x0    @ 080da1a6 041c
    movs r1,#0x6    @ 080da1a8 0621
    ldrsh r0,[r5,r1]                         @ 080da1aa 685e
    bl pack_entry_init                       @ 080da1ac fef774fe
    ldrh r0,[r5,#0x6]                        @ 080da1b0 e888
    adds r0,#0x1    @ 080da1b2 0130
    strh r0,[r5,#0x6]                        @ 080da1b4 e880
    movs r1,#0x6    @ 080da1b6 0621
    ldrsh r0,[r5,r1]                         @ 080da1b8 685e
    cmp r0,r4                                @ 080da1ba a042
    bcc LAB_080da1c4                         @ 080da1bc 02d3
    movs r0,#0x9    @ 080da1be 0920
    strh r0,[r5,#0x4]                        @ 080da1c0 a880
    movs r6,#0x1    @ 080da1c2 0126
LAB_080da1c4:
    movs r0,#0x1    @ 080da1c4 0120
    bl render_pack_slot_highlight_oam        @ 080da1c6 fff743fa
    adds r0,r6,#0x0    @ 080da1ca 301c
    pop {r4,r5,r6}                           @ 080da1cc 70bc
    pop {r1}                                 @ 080da1ce 02bc
    bx r1                                    @ 080da1d0 0847
    .zero  0x2
DAT_080da1d4:
    .word  pack_ui_state                  @ 080da1d4 50580003

@ 拆包卡槽 "展开" 滚动布局帧. 取 pack_visible_count 得可见卡数 (r6). 若 pack_ui_state+0x724 状态字 bit1 未置位 (首次进入), 调 update_pack_slot_scroll_positions 同步, 并为每个可见槽设置插值: 据 [+0x724] bit2 选目标 X (0x110 或 0xffe0 反向展开), Y 目标 0x50, 帧计数 [+0x10] 按槽序号偏置 8, 同时把当前 [+0x6]/[+0x8] 拷为源 [+0xa]/[+0xc]. 之后对各槽递减 [+0x10] 计数并经 bios_div 线性插值更新 [+0x2]/[+0x4], 计数归零时调 sync_state_and_init_sprite(4) 并清 [+0x724] bit0/bit5. 帧计数 [+0x6] 归负时据 bit2 调整选中卡 [+0x18] (加 r6 或减 5), 调 compute_pack_slot_scroll_x 与 set_pack_scroll_start_pos(_, 0x50), 设 [+0x10] 状态 := 6. 透传调 render_pack_slot_highlight_oam(1) 与 write_pack_banner_oam_for_all_slots(3). 供拆包展开滚动状态机帧驱动.
layout_pack_slots_scroll_fanned:
    push {r4,r5,r6,r7,lr}                    @ 080da1d8 f0b5
    .hword 0x464f    @ 080da1da 4f46
    .hword 0x4646    @ 080da1dc 4646
    push {r6,r7}                             @ 080da1de c0b4
    ldr r7, DAT_080da240                     @ 080da1e0 174f
    movs r0,#0xc    @ 080da1e2 0c20
    adds r0,r0,r7    @ 080da1e4 c019
    .hword 0x4680    @ 080da1e6 8046
    bl pack_visible_count                    @ 080da1e8 fef7f8fd
    adds r6,r0,#0x0    @ 080da1ec 061c
    movs r1,#0x0    @ 080da1ee 0021
    .hword 0x4689    @ 080da1f0 8946
    ldr r2, DAT_080da244                     @ 080da1f2 144a
    adds r1,r7,r2    @ 080da1f4 b918
    movs r0,#0x2    @ 080da1f6 0220
    ldrb r1,[r1,#0x0]                        @ 080da1f8 0978
    ands r0,r1    @ 080da1fa 0840
    cmp r0,#0x0                              @ 080da1fc 0028
    bne LAB_080da28e                         @ 080da1fe 46d1
    bl update_pack_slot_scroll_positions     @ 080da200 fef724fe
    .hword 0x4643    @ 080da204 4346
    ldrh r3,[r3,#0x1e]                       @ 080da206 db8b
    lsls r0,r3,#0x5    @ 080da208 5801
    adds r0,#0x44    @ 080da20a 4430
    .hword 0x4641    @ 080da20c 4146
    adds r4,r0,r1    @ 080da20e 4418
    movs r5,#0x0    @ 080da210 0025
    lsls r2,r6,#0x1    @ 080da212 7200
    .hword 0x4694    @ 080da214 9446
    cmp r9,r6                                @ 080da216 b145
    bcs LAB_080da278                         @ 080da218 2ed2
    ldr r0, DAT_080da244                     @ 080da21a 0a48
    adds r3,r7,r0    @ 080da21c 3b18
    movs r2,#0x50    @ 080da21e 5022
    ldr r7, DAT_080da248                     @ 080da220 094f
LAB_080da222:
    movs r0,#0x4    @ 080da222 0420
    ldrb r1,[r3,#0x0]                        @ 080da224 1978
    ands r0,r1    @ 080da226 0840
    cmp r0,#0x0                              @ 080da228 0028
    beq LAB_080da24c                         @ 080da22a 0fd0
    movs r0,#0x88    @ 080da22c 8820
    lsls r0,r0,#0x1    @ 080da22e 4000
    strh r0,[r4,#0x6]                        @ 080da230 e080
    strh r2,[r4,#0x8]                        @ 080da232 2281
    lsls r0,r5,#0x1    @ 080da234 6800
    adds r0,#0x8    @ 080da236 0830
    str r0,[r4,#0x10]                        @ 080da238 2061
    adds r1,r5,#0x1    @ 080da23a 691c
    b LAB_080da25a                           @ 080da23c 0de0
    .zero  0x2
DAT_080da240:
    .word  pack_ui_state                  @ 080da240 50580003
DAT_080da244:
    .word  0x00000724                     @ 080da244 24070000
DAT_080da248:
    .word  0x0000ffe0                     @ 080da248 e0ff0000
LAB_080da24c:
    strh r7,[r4,#0x6]                        @ 080da24c e780
    strh r2,[r4,#0x8]                        @ 080da24e 2281
    adds r1,r5,#0x1    @ 080da250 691c
    subs r0,r6,r1    @ 080da252 701a
    lsls r0,r0,#0x1    @ 080da254 4000
    adds r0,#0x8    @ 080da256 0830
    str r0,[r4,#0x10]                        @ 080da258 2061
LAB_080da25a:
    ldrh r0,[r4,#0x2]                        @ 080da25a 6088
    strh r0,[r4,#0xa]                        @ 080da25c 6081
    ldrh r0,[r4,#0x4]                        @ 080da25e a088
    strh r0,[r4,#0xc]                        @ 080da260 a081
    ldrh r0,[r4,#0x6]                        @ 080da262 e088
    strh r0,[r4,#0x2]                        @ 080da264 6080
    ldrh r0,[r4,#0x8]                        @ 080da266 2089
    strh r0,[r4,#0x4]                        @ 080da268 a080
    movs r0,#0x80    @ 080da26a 8020
    lsls r0,r0,#0x1    @ 080da26c 4000
    strh r0,[r4,#0xe]                        @ 080da26e e081
    adds r4,#0x20    @ 080da270 2034
    adds r5,r1,#0x0    @ 080da272 0d1c
    cmp r5,r6                                @ 080da274 b542
    bcc LAB_080da222                         @ 080da276 d4d3
LAB_080da278:
    .hword 0x4660    @ 080da278 6046
    adds r0,#0x8    @ 080da27a 0830
    .hword 0x4642    @ 080da27c 4246
    strh r0,[r2,#0x6]                        @ 080da27e d080
    movs r1,#0xe3    @ 080da280 e321
    lsls r1,r1,#0x3    @ 080da282 c900
    add r1,r8                                @ 080da284 4144
    movs r0,#0x2    @ 080da286 0220
    ldrb r3,[r1,#0x0]                        @ 080da288 0b78
    orrs r0,r3    @ 080da28a 1843
    strb r0,[r1,#0x0]                        @ 080da28c 0870
LAB_080da28e:
    .hword 0x4641    @ 080da28e 4146
    ldrh r1,[r1,#0x1e]                       @ 080da290 c98b
    lsls r0,r1,#0x5    @ 080da292 4801
    adds r0,#0x44    @ 080da294 4430
    .hword 0x4642    @ 080da296 4246
    adds r4,r2,r0    @ 080da298 1418
    movs r5,#0x0    @ 080da29a 0025
    cmp r5,r6                                @ 080da29c b542
    bcs LAB_080da316                         @ 080da29e 3ad2
    movs r7,#0xe3    @ 080da2a0 e327
    lsls r7,r7,#0x3    @ 080da2a2 ff00
    add r7,r8                                @ 080da2a4 4744
LAB_080da2a6:
    ldr r0,[r4,#0x10]                        @ 080da2a6 2069
    subs r2,r0,#0x1    @ 080da2a8 421e
    str r2,[r4,#0x10]                        @ 080da2aa 2261
    cmp r2,#0x7                              @ 080da2ac 072a
    ble LAB_080da2b8                         @ 080da2ae 03dd
    ldrh r0,[r4,#0x6]                        @ 080da2b0 e088
    strh r0,[r4,#0x2]                        @ 080da2b2 6080
    ldrh r0,[r4,#0x8]                        @ 080da2b4 2089
    b LAB_080da2f4                           @ 080da2b6 1de0
LAB_080da2b8:
    cmp r2,#0x0                              @ 080da2b8 002a
    bge LAB_080da2c4                         @ 080da2ba 03da
    ldrh r0,[r4,#0xa]                        @ 080da2bc 6089
    strh r0,[r4,#0x2]                        @ 080da2be 6080
    ldrh r0,[r4,#0xc]                        @ 080da2c0 a089
    b LAB_080da2f4                           @ 080da2c2 17e0
LAB_080da2c4:
    movs r3,#0x6    @ 080da2c4 0623
    ldrsh r0,[r4,r3]                         @ 080da2c6 e05e
    movs r3,#0xa    @ 080da2c8 0a23
    ldrsh r1,[r4,r3]                         @ 080da2ca e15e
    subs r0,r0,r1    @ 080da2cc 401a
    muls r0,r2    @ 080da2ce 5043
    movs r1,#0x8    @ 080da2d0 0821
    bl bios_div                              @ 080da2d2 34f093f8
    ldrh r1,[r4,#0xa]                        @ 080da2d6 6189
    adds r0,r1,r0    @ 080da2d8 0818
    strh r0,[r4,#0x2]                        @ 080da2da 6080
    movs r2,#0x8    @ 080da2dc 0822
    ldrsh r1,[r4,r2]                         @ 080da2de a15e
    movs r3,#0xc    @ 080da2e0 0c23
    ldrsh r0,[r4,r3]                         @ 080da2e2 e05e
    subs r1,r1,r0    @ 080da2e4 091a
    ldr r0,[r4,#0x10]                        @ 080da2e6 2069
    muls r0,r1    @ 080da2e8 4843
    movs r1,#0x8    @ 080da2ea 0821
    bl bios_div                              @ 080da2ec 34f086f8
    ldrh r1,[r4,#0xc]                        @ 080da2f0 a189
    adds r0,r1,r0    @ 080da2f2 0818
LAB_080da2f4:
    strh r0,[r4,#0x4]                        @ 080da2f4 a080
    ldr r0,[r4,#0x10]                        @ 080da2f6 2069
    cmp r0,#0x0                              @ 080da2f8 0028
    bne LAB_080da30e                         @ 080da2fa 08d1
    movs r0,#0x4    @ 080da2fc 0420
    bl sync_state_and_init_sprite            @ 080da2fe 1ff0d9fb
    movs r2,#0x21    @ 080da302 2122
    rsbs r2,r2,#0    @ 080da304 5242
    adds r0,r2,#0x0    @ 080da306 101c
    ldrb r3,[r7,#0x0]                        @ 080da308 3b78
    ands r0,r3    @ 080da30a 1840
    strb r0,[r7,#0x0]                        @ 080da30c 3870
LAB_080da30e:
    adds r4,#0x20    @ 080da30e 2034
    adds r5,#0x1    @ 080da310 0135
    cmp r5,r6                                @ 080da312 b542
    bcc LAB_080da2a6                         @ 080da314 c7d3
LAB_080da316:
    .hword 0x4641    @ 080da316 4146
    ldrh r0,[r1,#0x6]                        @ 080da318 c888
    subs r0,#0x1    @ 080da31a 0138
    strh r0,[r1,#0x6]                        @ 080da31c c880
    lsls r0,r0,#0x10    @ 080da31e 0004
    cmp r0,#0x0                              @ 080da320 0028
    bge LAB_080da36a                         @ 080da322 22da
    movs r1,#0xe3    @ 080da324 e321
    lsls r1,r1,#0x3    @ 080da326 c900
    add r1,r8                                @ 080da328 4144
    movs r0,#0x4    @ 080da32a 0420
    ldrb r1,[r1,#0x0]                        @ 080da32c 0978
    ands r0,r1    @ 080da32e 0840
    cmp r0,#0x0                              @ 080da330 0028
    beq LAB_080da33c                         @ 080da332 03d0
    movs r0,#0x0    @ 080da334 0020
    .hword 0x4642    @ 080da336 4246
    strh r0,[r2,#0x18]                       @ 080da338 1083
    b LAB_080da342                           @ 080da33a 02e0
LAB_080da33c:
    subs r0,r6,#0x1    @ 080da33c 701e
    .hword 0x4643    @ 080da33e 4346
    strh r0,[r3,#0x18]                       @ 080da340 1883
LAB_080da342:
    .hword 0x4641    @ 080da342 4146
    ldrh r0,[r1,#0x18]                       @ 080da344 088b
    bl compute_pack_slot_scroll_x            @ 080da346 fef757fd
    movs r1,#0x50    @ 080da34a 5021
    bl set_pack_scroll_start_pos             @ 080da34c faf7f8fa
    movs r1,#0xe3    @ 080da350 e321
    lsls r1,r1,#0x3    @ 080da352 c900
    add r1,r8                                @ 080da354 4144
    movs r0,#0x3    @ 080da356 0320
    rsbs r0,r0,#0    @ 080da358 4042
    ldrb r2,[r1,#0x0]                        @ 080da35a 0a78
    ands r0,r2    @ 080da35c 1040
    strb r0,[r1,#0x0]                        @ 080da35e 0870
    ldr r1, DAT_080da384                     @ 080da360 0849
    movs r0,#0x6    @ 080da362 0620
    strh r0,[r1,#0x10]                       @ 080da364 0882
    movs r3,#0x1    @ 080da366 0123
    .hword 0x4699    @ 080da368 9946
LAB_080da36a:
    movs r0,#0x1    @ 080da36a 0120
    bl render_pack_slot_highlight_oam        @ 080da36c fff770f9
    movs r0,#0x3    @ 080da370 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da372 fef7a7ff
    .hword 0x4648    @ 080da376 4846
    pop {r3,r4}                              @ 080da378 18bc
    .hword 0x4698    @ 080da37a 9846
    .hword 0x46a1    @ 080da37c a146
    pop {r4,r5,r6,r7}                        @ 080da37e f0bc
    pop {r1}                                 @ 080da380 02bc
    bx r1                                    @ 080da382 0847
DAT_080da384:
    .word  pack_ui_state                  @ 080da384 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 6.
@ Drives the pack list page selected-slot scroll interpolation animation. Calls
@ tick_pack_scroll_interp_step (r5=return value); if complete (r5==1): reads [+0x1a]
@ scroll_active flag, calls set_pack_scroll_step_mode(0) if 0 or set_pack_scroll_step_mode(1)
@ if 1; loads sentinel slot id=0xffff, calls pack_detail_bg_tile_load + render_pack_banner_tile_row_a
@ + render_pack_banner_tile_row_b, writes [+0x10]:=6 to advance state machine. Unconditionally
@ calls render_pack_card_sprite_by_flip_state(0); if [+0x1a]=0 calls render_pack_icon_oam_entries(0);
@ calls render_pack_slot_arrow_oam(0), render_pack_card_highlight_pulse_by_mode(0),
@ render_pack_slot_highlight_oam(1), write_pack_banner_oam_for_all_slots(3).
@ Returns r5 (Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080da3a8)
@ Returns: r0=u8 (0=scrolling, 1=complete; Sub-case E adds r0,r5 @ 080da3fe)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 6 (on complete)
@ Constants:
@   pack_ui_state = 0x03005850
@   SENTINEL_SLOT_ID = 0xffff
@   NEXT_STATE = 6
tick_pack_list_scroll_interp:
    push {r4,r5,r6,lr}                       @ 080da388 70b5
    ldr r0, DAT_080da3a8                     @ 080da38a 0748
    adds r6,r0,#0x0    @ 080da38c 061c
    adds r6,#0xc    @ 080da38e 0c36
    bl tick_pack_scroll_interp_step          @ 080da390 faf79afa
    adds r5,r0,#0x0    @ 080da394 051c
    cmp r5,#0x1                              @ 080da396 012d
    bne LAB_080da3d4                         @ 080da398 1cd1
    ldrh r0,[r6,#0x1a]                       @ 080da39a 708b
    cmp r0,#0x0                              @ 080da39c 0028
    beq LAB_080da3ac                         @ 080da39e 05d0
    cmp r0,#0x1                              @ 080da3a0 0128
    beq LAB_080da3b4                         @ 080da3a2 07d0
    b LAB_080da3ba                           @ 080da3a4 09e0
    .zero  0x2
DAT_080da3a8:
    .word  pack_ui_state                  @ 080da3a8 50580003
LAB_080da3ac:
    movs r0,#0x0    @ 080da3ac 0020
    bl set_pack_scroll_step_mode             @ 080da3ae faf7e3fa
    b LAB_080da3ba                           @ 080da3b2 02e0
LAB_080da3b4:
    movs r0,#0x1    @ 080da3b4 0120
    bl set_pack_scroll_step_mode             @ 080da3b6 faf7dffa
LAB_080da3ba:
    ldr r4, DAT_080da408                     @ 080da3ba 134c
    adds r0,r4,#0x0    @ 080da3bc 201c
    bl pack_detail_bg_tile_load              @ 080da3be fef7e1fd
    adds r0,r4,#0x0    @ 080da3c2 201c
    bl render_pack_banner_tile_row_a         @ 080da3c4 fef73cfe
    adds r0,r4,#0x0    @ 080da3c8 201c
    bl render_pack_banner_tile_row_b         @ 080da3ca fef767fe
    ldr r1, DAT_080da40c                     @ 080da3ce 0f49
    movs r0,#0x6    @ 080da3d0 0620
    strh r0,[r1,#0x10]                       @ 080da3d2 0882
LAB_080da3d4:
    movs r0,#0x0    @ 080da3d4 0020
    bl render_pack_card_sprite_by_flip_state @ 080da3d6 faf767f9
    ldrh r0,[r6,#0x1a]                       @ 080da3da 708b
    cmp r0,#0x0                              @ 080da3dc 0028
    bne LAB_080da3e6                         @ 080da3de 02d1
    movs r0,#0x0    @ 080da3e0 0020
    bl render_pack_icon_oam_entries          @ 080da3e2 fff78df8
LAB_080da3e6:
    movs r0,#0x0    @ 080da3e6 0020
    bl render_pack_slot_arrow_oam            @ 080da3e8 fff7f2f8
    movs r0,#0x0    @ 080da3ec 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080da3ee fef7a5ff
    movs r0,#0x1    @ 080da3f2 0120
    bl render_pack_slot_highlight_oam        @ 080da3f4 fff72cf9
    movs r0,#0x3    @ 080da3f8 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da3fa fef763ff
    adds r0,r5,#0x0    @ 080da3fe 281c
    pop {r4,r5,r6}                           @ 080da400 70bc
    pop {r1}                                 @ 080da402 02bc
    bx r1                                    @ 080da404 0847
    .zero  0x2
DAT_080da408:
    .word  0x0000ffff                     @ 080da408 ffff0000
DAT_080da40c:
    .word  pack_ui_state                  @ 080da40c 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 7.
@ Per-frame renderer for pack list page banner (pack cover) graphics. Reads [+0x1a]
@ scroll_active; if 0: uses [+0x18] (selected slot index) to call pack_detail_bg_tile_load +
@ render_pack_banner_tile_row_a + render_pack_banner_tile_row_b to refresh background details,
@ and calls render_pack_card_sprite_by_flip_state(0). If [+0x1a]=0: calls
@ render_pack_icon_oam_entries(0). Unconditionally calls render_pack_slot_arrow_oam(0),
@ render_pack_card_highlight_pulse_by_mode(0), render_pack_slot_highlight_oam(1),
@ write_pack_banner_oam_for_all_slots(3). Writes [+0x4]:=4 to advance state machine.
@ Returns fixed 1 (movs r0,#1 @ 080da45e; Sub-case E pop{r1};bx r1).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080da468)
@ Returns: r0=u8 1 (step-complete flag)
@ Side effects:
@   [pack_ui_state+0xc+0x4] := 4 (state-machine step advance)
@ Constants:
@   pack_ui_state = 0x03005850
@   NEXT_STATE = 4
tick_pack_list_banner_tiles:
    push {r4,lr}                             @ 080da410 10b5
    ldr r0, DAT_080da468                     @ 080da412 1548
    adds r4,r0,#0x0    @ 080da414 041c
    adds r4,#0xc    @ 080da416 0c34
    ldrh r0,[r4,#0x1a]                       @ 080da418 608b
    cmp r0,#0x0                              @ 080da41a 0028
    bne LAB_080da442                         @ 080da41c 11d1
    ldrh r0,[r4,#0x18]                       @ 080da41e 208b
    bl pack_detail_bg_tile_load              @ 080da420 fef7b0fd
    ldrh r0,[r4,#0x18]                       @ 080da424 208b
    bl render_pack_banner_tile_row_a         @ 080da426 fef70bfe
    ldrh r0,[r4,#0x18]                       @ 080da42a 208b
    bl render_pack_banner_tile_row_b         @ 080da42c fef736fe
    movs r0,#0x0    @ 080da430 0020
    bl render_pack_card_sprite_by_flip_state @ 080da432 faf739f9
    ldrh r0,[r4,#0x1a]                       @ 080da436 608b
    cmp r0,#0x0                              @ 080da438 0028
    bne LAB_080da442                         @ 080da43a 02d1
    movs r0,#0x0    @ 080da43c 0020
    bl render_pack_icon_oam_entries          @ 080da43e fff75ff8
LAB_080da442:
    movs r0,#0x0    @ 080da442 0020
    bl render_pack_slot_arrow_oam            @ 080da444 fff7c4f8
    movs r0,#0x0    @ 080da448 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080da44a fef777ff
    movs r0,#0x1    @ 080da44e 0120
    bl render_pack_slot_highlight_oam        @ 080da450 fff7fef8
    movs r0,#0x3    @ 080da454 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da456 fef735ff
    movs r0,#0x4    @ 080da45a 0420
    strh r0,[r4,#0x4]                        @ 080da45c a080
    movs r0,#0x1    @ 080da45e 0120
    pop {r4}                                 @ 080da460 10bc
    pop {r1}                                 @ 080da462 02bc
    bx r1                                    @ 080da464 0847
    .zero  0x2
DAT_080da468:
    .word  pack_ui_state                  @ 080da468 50580003

@ 拆包卡槽 "聚焦居中" 滚动布局帧. 取 pack_visible_count 得可见卡数 (r7). 若 pack_ui_state+0x724 状态字 bit1 未置位 (首次进入), 以选中卡 [+0x18] 为中心, 把序号小于它的槽目标 X 减 0xf0 (左移出屏), 大于它的加 0xf0 (右移出屏), 设步进计数 [+0x10] := 5, 并把 [+0x1c] 同步为 [+0x18]. 然后配置 BG3CNT/BG0CNT/BG1CNT (清优先级低 2 位后分别 |=1/|=2) 与 BG 滚动寄存器 (0x1748/0x1000), 设帧计数 [+0x6] := 0xa, 置 [+0x724] bit1. 之后每帧据帧计数符号: 计数>0 时经 bios_div 用 BLDALPHA 做淡入淡出并对选中槽线性插值 Y; 计数<=0 时禁用 BG 图层并据 BLDCNT 收尾. 透传调 render_pack_slot_highlight_oam(2) 与 write_pack_banner_oam_for_all_slots(3). 供拆包聚焦居中状态机帧驱动.
layout_pack_slots_scroll_centered:
    push {r4,r5,r6,r7,lr}                    @ 080da46c f0b5
    .hword 0x4647    @ 080da46e 4746
    push {r7}                                @ 080da470 80b4
    ldr r4, DAT_080da4b4                     @ 080da472 104c
    adds r6,r4,#0x0    @ 080da474 261c
    adds r6,#0xc    @ 080da476 0c36
    bl pack_visible_count                    @ 080da478 fef7b0fc
    adds r7,r0,#0x0    @ 080da47c 071c
    movs r0,#0x0    @ 080da47e 0020
    .hword 0x4680    @ 080da480 8046
    ldr r1, DAT_080da4b8                     @ 080da482 0d49
    adds r4,r4,r1    @ 080da484 6418
    movs r0,#0x2    @ 080da486 0220
    ldrb r4,[r4,#0x0]                        @ 080da488 2478
    ands r0,r4    @ 080da48a 2040
    cmp r0,#0x0                              @ 080da48c 0028
    bne LAB_080da542                         @ 080da48e 58d1
    ldrh r2,[r6,#0x1e]                       @ 080da490 f28b
    lsls r0,r2,#0x5    @ 080da492 5001
    adds r0,#0x44    @ 080da494 4430
    adds r4,r0,r6    @ 080da496 8419
    movs r5,#0x0    @ 080da498 0025
    cmp r8,r7                                @ 080da49a b845
    bcs LAB_080da4dc                         @ 080da49c 1ed2
    movs r2,#0x5    @ 080da49e 0522
LAB_080da4a0:
    ldrh r0,[r6,#0x18]                       @ 080da4a0 308b
    cmp r5,r0                                @ 080da4a2 8542
    bcs LAB_080da4bc                         @ 080da4a4 0ad2
    ldrh r0,[r4,#0x2]                        @ 080da4a6 6088
    strh r0,[r4,#0x6]                        @ 080da4a8 e080
    ldrh r1,[r4,#0x4]                        @ 080da4aa a188
    strh r1,[r4,#0x8]                        @ 080da4ac 2181
    subs r0,#0xf0    @ 080da4ae f038
    b LAB_080da4ca                           @ 080da4b0 0be0
    .zero  0x2
DAT_080da4b4:
    .word  pack_ui_state                  @ 080da4b4 50580003
DAT_080da4b8:
    .word  0x00000724                     @ 080da4b8 24070000
LAB_080da4bc:
    cmp r5,r0                                @ 080da4bc 8542
    bls LAB_080da4d0                         @ 080da4be 07d9
    ldrh r0,[r4,#0x2]                        @ 080da4c0 6088
    strh r0,[r4,#0x6]                        @ 080da4c2 e080
    ldrh r1,[r4,#0x4]                        @ 080da4c4 a188
    strh r1,[r4,#0x8]                        @ 080da4c6 2181
    adds r0,#0xf0    @ 080da4c8 f030
LAB_080da4ca:
    strh r0,[r4,#0xa]                        @ 080da4ca 6081
    strh r1,[r4,#0xc]                        @ 080da4cc a181
    str r2,[r4,#0x10]                        @ 080da4ce 2261
LAB_080da4d0:
    ldrh r0,[r6,#0x18]                       @ 080da4d0 308b
    strh r0,[r6,#0x1c]                       @ 080da4d2 b083
    adds r4,#0x20    @ 080da4d4 2034
    adds r5,#0x1    @ 080da4d6 0135
    cmp r5,r7                                @ 080da4d8 bd42
    bcc LAB_080da4a0                         @ 080da4da e1d3
LAB_080da4dc:
    ldr r1, PTR_BG3CNT_080da5a0              @ 080da4dc 3049
    ldrh r2,[r1,#0x0]                        @ 080da4de 0a88
    ldr r3, DAT_080da5a4                     @ 080da4e0 304b
    adds r0,r3,#0x0    @ 080da4e2 181c
    ands r0,r2    @ 080da4e4 1040
    strh r0,[r1,#0x0]                        @ 080da4e6 0880
    ldrh r0,[r1,#0x0]                        @ 080da4e8 0888
    strh r0,[r1,#0x0]                        @ 080da4ea 0880
    ldr r2, PTR_BG0CNT_080da5a8              @ 080da4ec 2e4a
    ldrh r1,[r2,#0x0]                        @ 080da4ee 1188
    adds r0,r3,#0x0    @ 080da4f0 181c
    ands r0,r1    @ 080da4f2 0840
    strh r0,[r2,#0x0]                        @ 080da4f4 1080
    ldrh r0,[r2,#0x0]                        @ 080da4f6 1088
    movs r1,#0x1    @ 080da4f8 0121
    orrs r0,r1    @ 080da4fa 0843
    strh r0,[r2,#0x0]                        @ 080da4fc 1080
    ldr r1, PTR_BG1CNT_080da5ac              @ 080da4fe 2b49
    ldrh r2,[r1,#0x0]                        @ 080da500 0a88
    adds r0,r3,#0x0    @ 080da502 181c
    ands r0,r2    @ 080da504 1040
    strh r0,[r1,#0x0]                        @ 080da506 0880
    ldrh r0,[r1,#0x0]                        @ 080da508 0888
    movs r2,#0x2    @ 080da50a 0222
    orrs r0,r2    @ 080da50c 1043
    strh r0,[r1,#0x0]                        @ 080da50e 0880
    adds r1,#0x2    @ 080da510 0231
    ldrh r0,[r1,#0x0]                        @ 080da512 0888
    ands r3,r0    @ 080da514 0340
    strh r3,[r1,#0x0]                        @ 080da516 0b80
    ldrh r0,[r1,#0x0]                        @ 080da518 0888
    orrs r0,r2    @ 080da51a 1043
    strh r0,[r1,#0x0]                        @ 080da51c 0880
    adds r1,#0x44    @ 080da51e 4431
    ldr r3, DAT_080da5b0                     @ 080da520 234b
    adds r0,r3,#0x0    @ 080da522 181c
    strh r0,[r1,#0x0]                        @ 080da524 0880
    adds r1,#0x2    @ 080da526 0231
    movs r2,#0x80    @ 080da528 8022
    lsls r2,r2,#0x5    @ 080da52a 5201
    adds r0,r2,#0x0    @ 080da52c 101c
    strh r0,[r1,#0x0]                        @ 080da52e 0880
    movs r0,#0xa    @ 080da530 0a20
    strh r0,[r6,#0x6]                        @ 080da532 f080
    movs r3,#0xe3    @ 080da534 e323
    lsls r3,r3,#0x3    @ 080da536 db00
    adds r1,r6,r3    @ 080da538 f118
    movs r0,#0x2    @ 080da53a 0220
    ldrb r2,[r1,#0x0]                        @ 080da53c 0a78
    orrs r0,r2    @ 080da53e 1043
    strb r0,[r1,#0x0]                        @ 080da540 0870
LAB_080da542:
    ldrh r0,[r6,#0x6]                        @ 080da542 f088
    subs r0,#0x1    @ 080da544 0138
    strh r0,[r6,#0x6]                        @ 080da546 f080
    lsls r0,r0,#0x10    @ 080da548 0004
    asrs r0,r0,#0x10    @ 080da54a 0014
    cmp r0,#0x0                              @ 080da54c 0028
    bge LAB_080da554                         @ 080da54e 01da
    movs r3,#0x1    @ 080da550 0123
    .hword 0x4698    @ 080da552 9846
LAB_080da554:
    cmp r0,#0x0                              @ 080da554 0028
    ble LAB_080da5fe                         @ 080da556 52dd
    movs r1,#0x6    @ 080da558 0621
    ldrsh r0,[r6,r1]                         @ 080da55a 705e
    lsls r0,r0,#0x4    @ 080da55c 0001
    movs r1,#0xa    @ 080da55e 0a21
    bl bios_div                              @ 080da560 33f04cff
    adds r5,r0,#0x0    @ 080da564 051c
    ldr r2, PTR_BLDALPHA_080da5b4            @ 080da566 134a
    movs r0,#0x10    @ 080da568 1020
    subs r0,r0,r5    @ 080da56a 401b
    lsls r0,r0,#0x18    @ 080da56c 0006
    lsrs r0,r0,#0x18    @ 080da56e 000e
    lsls r1,r5,#0x18    @ 080da570 2906
    lsrs r1,r1,#0x10    @ 080da572 090c
    orrs r0,r1    @ 080da574 0843
    strh r0,[r2,#0x0]                        @ 080da576 1080
    ldrh r2,[r6,#0x1e]                       @ 080da578 f28b
    lsls r0,r2,#0x5    @ 080da57a 5001
    adds r0,#0x44    @ 080da57c 4430
    adds r4,r6,r0    @ 080da57e 3418
    movs r5,#0x0    @ 080da580 0025
    cmp r5,r7                                @ 080da582 bd42
    bcs LAB_080da656                         @ 080da584 67d2
LAB_080da586:
    ldrh r3,[r6,#0x18]                       @ 080da586 338b
    cmp r5,r3                                @ 080da588 9d42
    bne LAB_080da5b8                         @ 080da58a 15d1
    movs r1,#0x6    @ 080da58c 0621
    ldrsh r0,[r6,r1]                         @ 080da58e 705e
    lsls r0,r0,#0x7    @ 080da590 c001
    movs r1,#0xa    @ 080da592 0a21
    bl bios_div                              @ 080da594 33f032ff
    adds r0,#0x80    @ 080da598 8030
    strh r0,[r4,#0xe]                        @ 080da59a e081
    b LAB_080da5f4                           @ 080da59c 2ae0
    .zero  0x2
PTR_BG3CNT_080da5a0:
    .word  BG3CNT                         @ 080da5a0 0e000004
DAT_080da5a4:
    .word  0x0000fffc                     @ 080da5a4 fcff0000
PTR_BG0CNT_080da5a8:
    .word  BG0CNT                         @ 080da5a8 08000004
PTR_BG1CNT_080da5ac:
    .word  BG1CNT                         @ 080da5ac 0a000004
DAT_080da5b0:
    .word  0x00001748                     @ 080da5b0 48170000
PTR_BLDALPHA_080da5b4:
    .word  BLDALPHA                       @ 080da5b4 52000004
LAB_080da5b8:
    ldr r2,[r4,#0x10]                        @ 080da5b8 2269
    cmp r2,#0x0                              @ 080da5ba 002a
    ble LAB_080da5f4                         @ 080da5bc 1add
    subs r2,#0x1    @ 080da5be 013a
    str r2,[r4,#0x10]                        @ 080da5c0 2261
    movs r3,#0x6    @ 080da5c2 0623
    ldrsh r0,[r4,r3]                         @ 080da5c4 e05e
    movs r3,#0xa    @ 080da5c6 0a23
    ldrsh r1,[r4,r3]                         @ 080da5c8 e15e
    subs r0,r0,r1    @ 080da5ca 401a
    muls r0,r2    @ 080da5cc 5043
    movs r1,#0x5    @ 080da5ce 0521
    bl bios_div                              @ 080da5d0 33f014ff
    ldrh r1,[r4,#0xa]                        @ 080da5d4 6189
    adds r0,r1,r0    @ 080da5d6 0818
    strh r0,[r4,#0x2]                        @ 080da5d8 6080
    movs r2,#0x8    @ 080da5da 0822
    ldrsh r1,[r4,r2]                         @ 080da5dc a15e
    movs r3,#0xc    @ 080da5de 0c23
    ldrsh r0,[r4,r3]                         @ 080da5e0 e05e
    subs r1,r1,r0    @ 080da5e2 091a
    ldr r0,[r4,#0x10]                        @ 080da5e4 2069
    muls r0,r1    @ 080da5e6 4843
    movs r1,#0x5    @ 080da5e8 0521
    bl bios_div                              @ 080da5ea 33f007ff
    ldrh r1,[r4,#0xc]                        @ 080da5ee a189
    adds r0,r1,r0    @ 080da5f0 0818
    strh r0,[r4,#0x4]                        @ 080da5f2 a080
LAB_080da5f4:
    adds r4,#0x20    @ 080da5f4 2034
    adds r5,#0x1    @ 080da5f6 0135
    cmp r5,r7                                @ 080da5f8 bd42
    bcc LAB_080da586                         @ 080da5fa c4d3
    b LAB_080da656                           @ 080da5fc 2be0
LAB_080da5fe:
    ldr r1, PTR_BG0CNT_080da6a0              @ 080da5fe 2849
    ldrh r2,[r1,#0x0]                        @ 080da600 0a88
    ldr r3, DAT_080da6a4                     @ 080da602 284b
    adds r0,r3,#0x0    @ 080da604 181c
    ands r0,r2    @ 080da606 1040
    strh r0,[r1,#0x0]                        @ 080da608 0880
    ldrh r0,[r1,#0x0]                        @ 080da60a 0888
    strh r0,[r1,#0x0]                        @ 080da60c 0880
    adds r1,#0x2    @ 080da60e 0231
    ldrh r2,[r1,#0x0]                        @ 080da610 0a88
    adds r0,r3,#0x0    @ 080da612 181c
    ands r0,r2    @ 080da614 1040
    strh r0,[r1,#0x0]                        @ 080da616 0880
    ldrh r0,[r1,#0x0]                        @ 080da618 0888
    movs r4,#0x1    @ 080da61a 0124
    orrs r0,r4    @ 080da61c 2043
    strh r0,[r1,#0x0]                        @ 080da61e 0880
    adds r1,#0x2    @ 080da620 0231
    ldrh r2,[r1,#0x0]                        @ 080da622 0a88
    adds r0,r3,#0x0    @ 080da624 181c
    ands r0,r2    @ 080da626 1040
    strh r0,[r1,#0x0]                        @ 080da628 0880
    ldrh r0,[r1,#0x0]                        @ 080da62a 0888
    orrs r0,r4    @ 080da62c 2043
    strh r0,[r1,#0x0]                        @ 080da62e 0880
    ldr r2, PTR_BG3CNT_080da6a8              @ 080da630 1d4a
    ldrh r0,[r2,#0x0]                        @ 080da632 1088
    ands r3,r0    @ 080da634 0340
    strh r3,[r2,#0x0]                        @ 080da636 1380
    ldrh r0,[r2,#0x0]                        @ 080da638 1088
    movs r1,#0x3    @ 080da63a 0321
    orrs r0,r1    @ 080da63c 0843
    strh r0,[r2,#0x0]                        @ 080da63e 1080
    ldr r1, PTR_BLDCNT_080da6ac              @ 080da640 1a49
    movs r0,#0x3f    @ 080da642 3f20
    strh r0,[r1,#0x0]                        @ 080da644 0880
    adds r1,#0x2    @ 080da646 0231
    ldr r2, DAT_080da6b0                     @ 080da648 194a
    adds r0,r2,#0x0    @ 080da64a 101c
    strh r0,[r1,#0x0]                        @ 080da64c 0880
    subs r1,#0x52    @ 080da64e 5239
    movs r0,#0x80    @ 080da650 8020
    lsls r0,r0,#0x4    @ 080da652 0001
    strh r0,[r1,#0x0]                        @ 080da654 0880
LAB_080da656:
    .hword 0x4643    @ 080da656 4346
    cmp r3,#0x1                              @ 080da658 012b
    bne LAB_080da686                         @ 080da65a 14d1
    strh r3,[r6,#0x2]                        @ 080da65c 7380
    movs r0,#0xe3    @ 080da65e e320
    lsls r0,r0,#0x3    @ 080da660 c000
    adds r1,r6,r0    @ 080da662 3118
    movs r0,#0x3    @ 080da664 0320
    rsbs r0,r0,#0    @ 080da666 4042
    ldrb r2,[r1,#0x0]                        @ 080da668 0a78
    ands r0,r2    @ 080da66a 1040
    strb r0,[r1,#0x0]                        @ 080da66c 0870
    ldrh r3,[r6,#0x1e]                       @ 080da66e f38b
    ldrh r2,[r6,#0x18]                       @ 080da670 328b
    adds r0,r3,r2    @ 080da672 9818
    strh r0,[r6,#0x32]                       @ 080da674 7086
    movs r0,#0x2    @ 080da676 0220
    rsbs r0,r0,#0    @ 080da678 4042
    ldrb r3,[r1,#0x0]                        @ 080da67a 0b78
    ands r0,r3    @ 080da67c 1840
    strb r0,[r1,#0x0]                        @ 080da67e 0870
    ldr r1, DAT_080da6b4                     @ 080da680 0c49
    movs r0,#0x13    @ 080da682 1320
    strh r0,[r1,#0x10]                       @ 080da684 0882
LAB_080da686:
    movs r0,#0x2    @ 080da686 0220
    bl render_pack_slot_highlight_oam        @ 080da688 fef7e2ff
    movs r0,#0x3    @ 080da68c 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da68e fef719fe
    .hword 0x4640    @ 080da692 4046
    pop {r3}                                 @ 080da694 08bc
    .hword 0x4698    @ 080da696 9846
    pop {r4,r5,r6,r7}                        @ 080da698 f0bc
    pop {r1}                                 @ 080da69a 02bc
    bx r1                                    @ 080da69c 0847
    .zero  0x2
PTR_BG0CNT_080da6a0:
    .word  BG0CNT                         @ 080da6a0 08000004
DAT_080da6a4:
    .word  0x0000fffc                     @ 080da6a4 fcff0000
PTR_BG3CNT_080da6a8:
    .word  BG3CNT                         @ 080da6a8 0e000004
PTR_BLDCNT_080da6ac:
    .word  BLDCNT                         @ 080da6ac 50000004
DAT_080da6b0:
    .word  0x00001010                     @ 080da6b0 10100000
DAT_080da6b4:
    .word  pack_ui_state                  @ 080da6b4 50580003

@ 拆包卡槽 "滚出/关闭" 滚动布局帧. 取 pack_visible_count 得可见卡数 (r6), 算帧计数初值 r6*2+8. 若 pack_ui_state+0x724 状态字 bit1 未置位 (首次进入), 调 update_pack_slot_scroll_positions 同步, 为每个可见槽设目标 X 0x78, Y 0x50, 缩放 0x100, 帧计数 [+0x10] 按槽序号递减偏置. 然后配置 BG3CNT/BG0CNT/BG1CNT (清优先级后 BG0|=1, BG1|=2) 与 BG 滚动寄存器 (0x1748/0x1000), 置 [+0x724] bit1. 之后每帧对各槽递减 [+0x10] 经 bios_div 线性插值 [+0x2]/[+0x4]/[+0xe]. 帧计数 [+0x6] 归负后据 bios_div 用 BLDALPHA 做整屏淡出, 计数<=0 时设 [+0x2]:=4, 禁用 BG0-3 图层, 写 BLDCNT 0x3f3f/BLDALPHA 0x1010 收尾, 清 [+0x724] bit0/bit1, 设 pack_ui_state[0x10] 状态 := 0x13. 透传调 render_pack_slot_highlight_oam(1) 与 write_pack_banner_oam_for_all_slots(3). 供拆包关闭滚出状态机帧驱动.
layout_pack_slots_scroll_out:
    push {r4,r5,r6,r7,lr}                    @ 080da6b8 f0b5
    .hword 0x464f    @ 080da6ba 4f46
    .hword 0x4646    @ 080da6bc 4646
    push {r6,r7}                             @ 080da6be c0b4
    ldr r4, DAT_080da7b8                     @ 080da6c0 3d4c
    adds r7,r4,#0x0    @ 080da6c2 271c
    adds r7,#0xc    @ 080da6c4 0c37
    movs r0,#0x0    @ 080da6c6 0020
    .hword 0x4681    @ 080da6c8 8146
    bl pack_visible_count                    @ 080da6ca fef787fb
    adds r6,r0,#0x0    @ 080da6ce 061c
    lsls r0,r6,#0x1    @ 080da6d0 7000
    adds r0,#0x8    @ 080da6d2 0830
    .hword 0x4680    @ 080da6d4 8046
    cmp r0,#0x0                              @ 080da6d6 0028
    bne LAB_080da6de                         @ 080da6d8 01d1
    movs r1,#0x1    @ 080da6da 0121
    .hword 0x4688    @ 080da6dc 8846
LAB_080da6de:
    ldr r2, DAT_080da7bc                     @ 080da6de 374a
    adds r1,r4,r2    @ 080da6e0 a118
    movs r0,#0x2    @ 080da6e2 0220
    ldrb r1,[r1,#0x0]                        @ 080da6e4 0978
    ands r0,r1    @ 080da6e6 0840
    cmp r0,#0x0                              @ 080da6e8 0028
    bne LAB_080da78e                         @ 080da6ea 50d1
    bl update_pack_slot_scroll_positions     @ 080da6ec fef7aefb
    ldrh r3,[r7,#0x1e]                       @ 080da6f0 fb8b
    lsls r0,r3,#0x5    @ 080da6f2 5801
    adds r0,#0x44    @ 080da6f4 4430
    adds r4,r0,r7    @ 080da6f6 c419
    movs r5,#0x0    @ 080da6f8 0025
    cmp r9,r6                                @ 080da6fa b145
    bcs LAB_080da728                         @ 080da6fc 14d2
    movs r0,#0x78    @ 080da6fe 7820
    .hword 0x4684    @ 080da700 8446
    movs r3,#0x50    @ 080da702 5023
    movs r2,#0x80    @ 080da704 8022
    lsls r2,r2,#0x1    @ 080da706 5200
    lsls r0,r6,#0x1    @ 080da708 7000
    adds r1,r0,#0x6    @ 080da70a 811d
LAB_080da70c:
    ldrh r0,[r4,#0x2]                        @ 080da70c 6088
    strh r0,[r4,#0x6]                        @ 080da70e e080
    ldrh r0,[r4,#0x4]                        @ 080da710 a088
    strh r0,[r4,#0x8]                        @ 080da712 2081
    .hword 0x4660    @ 080da714 6046
    strh r0,[r4,#0xa]                        @ 080da716 6081
    strh r3,[r4,#0xc]                        @ 080da718 a381
    strh r2,[r4,#0xe]                        @ 080da71a e281
    str r1,[r4,#0x10]                        @ 080da71c 2161
    adds r4,#0x20    @ 080da71e 2034
    subs r1,#0x2    @ 080da720 0239
    adds r5,#0x1    @ 080da722 0135
    cmp r5,r6                                @ 080da724 b542
    bcc LAB_080da70c                         @ 080da726 f1d3
LAB_080da728:
    .hword 0x4641    @ 080da728 4146
    strh r1,[r7,#0x6]                        @ 080da72a f980
    ldr r1, PTR_BG3CNT_080da7c0              @ 080da72c 2449
    ldrh r2,[r1,#0x0]                        @ 080da72e 0a88
    ldr r3, DAT_080da7c4                     @ 080da730 244b
    adds r0,r3,#0x0    @ 080da732 181c
    ands r0,r2    @ 080da734 1040
    strh r0,[r1,#0x0]                        @ 080da736 0880
    ldrh r0,[r1,#0x0]                        @ 080da738 0888
    strh r0,[r1,#0x0]                        @ 080da73a 0880
    ldr r2, PTR_BG0CNT_080da7c8              @ 080da73c 224a
    ldrh r1,[r2,#0x0]                        @ 080da73e 1188
    adds r0,r3,#0x0    @ 080da740 181c
    ands r0,r1    @ 080da742 0840
    strh r0,[r2,#0x0]                        @ 080da744 1080
    ldrh r0,[r2,#0x0]                        @ 080da746 1088
    movs r1,#0x1    @ 080da748 0121
    orrs r0,r1    @ 080da74a 0843
    strh r0,[r2,#0x0]                        @ 080da74c 1080
    ldr r1, PTR_BG1CNT_080da7cc              @ 080da74e 1f49
    ldrh r2,[r1,#0x0]                        @ 080da750 0a88
    adds r0,r3,#0x0    @ 080da752 181c
    ands r0,r2    @ 080da754 1040
    strh r0,[r1,#0x0]                        @ 080da756 0880
    ldrh r0,[r1,#0x0]                        @ 080da758 0888
    movs r2,#0x2    @ 080da75a 0222
    orrs r0,r2    @ 080da75c 1043
    strh r0,[r1,#0x0]                        @ 080da75e 0880
    adds r1,#0x2    @ 080da760 0231
    ldrh r0,[r1,#0x0]                        @ 080da762 0888
    ands r3,r0    @ 080da764 0340
    strh r3,[r1,#0x0]                        @ 080da766 0b80
    ldrh r0,[r1,#0x0]                        @ 080da768 0888
    orrs r0,r2    @ 080da76a 1043
    strh r0,[r1,#0x0]                        @ 080da76c 0880
    adds r1,#0x44    @ 080da76e 4431
    ldr r2, DAT_080da7d0                     @ 080da770 174a
    adds r0,r2,#0x0    @ 080da772 101c
    strh r0,[r1,#0x0]                        @ 080da774 0880
    adds r1,#0x2    @ 080da776 0231
    movs r3,#0x80    @ 080da778 8023
    lsls r3,r3,#0x5    @ 080da77a 5b01
    adds r0,r3,#0x0    @ 080da77c 181c
    strh r0,[r1,#0x0]                        @ 080da77e 0880
    movs r0,#0xe3    @ 080da780 e320
    lsls r0,r0,#0x3    @ 080da782 c000
    adds r1,r7,r0    @ 080da784 3918
    movs r0,#0x2    @ 080da786 0220
    ldrb r2,[r1,#0x0]                        @ 080da788 0a78
    orrs r0,r2    @ 080da78a 1043
    strb r0,[r1,#0x0]                        @ 080da78c 0870
LAB_080da78e:
    ldrh r3,[r7,#0x1e]                       @ 080da78e fb8b
    lsls r0,r3,#0x5    @ 080da790 5801
    adds r0,#0x44    @ 080da792 4430
    adds r4,r7,r0    @ 080da794 3c18
    movs r5,#0x0    @ 080da796 0025
    cmp r5,r6                                @ 080da798 b542
    bcs LAB_080da836                         @ 080da79a 4cd2
LAB_080da79c:
    ldr r0,[r4,#0x10]                        @ 080da79c 2069
    subs r2,r0,#0x1    @ 080da79e 421e
    str r2,[r4,#0x10]                        @ 080da7a0 2261
    cmp r2,#0x7                              @ 080da7a2 072a
    ble LAB_080da7d4                         @ 080da7a4 16dd
    ldrh r0,[r4,#0x6]                        @ 080da7a6 e088
    strh r0,[r4,#0x2]                        @ 080da7a8 6080
    ldrh r0,[r4,#0x8]                        @ 080da7aa 2089
    strh r0,[r4,#0x4]                        @ 080da7ac a080
    movs r0,#0x80    @ 080da7ae 8020
    lsls r0,r0,#0x1    @ 080da7b0 4000
    strh r0,[r4,#0xe]                        @ 080da7b2 e081
    b LAB_080da82e                           @ 080da7b4 3be0
    .zero  0x2
DAT_080da7b8:
    .word  pack_ui_state                  @ 080da7b8 50580003
DAT_080da7bc:
    .word  0x00000724                     @ 080da7bc 24070000
PTR_BG3CNT_080da7c0:
    .word  BG3CNT                         @ 080da7c0 0e000004
DAT_080da7c4:
    .word  0x0000fffc                     @ 080da7c4 fcff0000
PTR_BG0CNT_080da7c8:
    .word  BG0CNT                         @ 080da7c8 08000004
PTR_BG1CNT_080da7cc:
    .word  BG1CNT                         @ 080da7cc 0a000004
DAT_080da7d0:
    .word  0x00001748                     @ 080da7d0 48170000
LAB_080da7d4:
    cmp r2,#0x0                              @ 080da7d4 002a
    bge LAB_080da7e4                         @ 080da7d6 05da
    ldrh r0,[r4,#0xa]                        @ 080da7d8 6089
    movs r1,#0x0    @ 080da7da 0021
    strh r0,[r4,#0x2]                        @ 080da7dc 6080
    ldrh r0,[r4,#0xc]                        @ 080da7de a089
    strh r0,[r4,#0x4]                        @ 080da7e0 a080
    b LAB_080da82c                           @ 080da7e2 23e0
LAB_080da7e4:
    movs r1,#0x6    @ 080da7e4 0621
    ldrsh r0,[r4,r1]                         @ 080da7e6 605e
    movs r3,#0xa    @ 080da7e8 0a23
    ldrsh r1,[r4,r3]                         @ 080da7ea e15e
    subs r0,r0,r1    @ 080da7ec 401a
    muls r0,r2    @ 080da7ee 5043
    movs r1,#0x8    @ 080da7f0 0821
    bl bios_div                              @ 080da7f2 33f003fe
    ldrh r1,[r4,#0xa]                        @ 080da7f6 6189
    adds r0,r1,r0    @ 080da7f8 0818
    strh r0,[r4,#0x2]                        @ 080da7fa 6080
    movs r2,#0x8    @ 080da7fc 0822
    ldrsh r1,[r4,r2]                         @ 080da7fe a15e
    movs r3,#0xc    @ 080da800 0c23
    ldrsh r0,[r4,r3]                         @ 080da802 e05e
    subs r1,r1,r0    @ 080da804 091a
    ldr r0,[r4,#0x10]                        @ 080da806 2069
    muls r0,r1    @ 080da808 4843
    movs r1,#0x8    @ 080da80a 0821
    bl bios_div                              @ 080da80c 33f0f6fd
    ldrh r1,[r4,#0xc]                        @ 080da810 a189
    adds r0,r1,r0    @ 080da812 0818
    strh r0,[r4,#0x4]                        @ 080da814 a080
    ldr r1,[r4,#0x10]                        @ 080da816 2169
    lsls r0,r1,#0x1    @ 080da818 4800
    adds r0,r0,r1    @ 080da81a 4018
    lsls r0,r0,#0x8    @ 080da81c 0002
    movs r1,#0x8    @ 080da81e 0821
    bl bios_div                              @ 080da820 33f0ecfd
    movs r2,#0x80    @ 080da824 8022
    lsls r2,r2,#0x3    @ 080da826 d200
    adds r1,r2,#0x0    @ 080da828 111c
    subs r1,r1,r0    @ 080da82a 091a
LAB_080da82c:
    strh r1,[r4,#0xe]                        @ 080da82c e181
LAB_080da82e:
    adds r4,#0x20    @ 080da82e 2034
    adds r5,#0x1    @ 080da830 0135
    cmp r5,r6                                @ 080da832 b542
    bcc LAB_080da79c                         @ 080da834 b2d3
LAB_080da836:
    ldrh r0,[r7,#0x6]                        @ 080da836 f888
    subs r0,#0x1    @ 080da838 0138
    strh r0,[r7,#0x6]                        @ 080da83a f880
    lsls r0,r0,#0x10    @ 080da83c 0004
    cmp r0,#0x0                              @ 080da83e 0028
    ble LAB_080da86c                         @ 080da840 14dd
    movs r3,#0x6    @ 080da842 0623
    ldrsh r0,[r7,r3]                         @ 080da844 f85e
    lsls r0,r0,#0x4    @ 080da846 0001
    .hword 0x4641    @ 080da848 4146
    bl bios_div                              @ 080da84a 33f0d7fd
    movs r2,#0x10    @ 080da84e 1022
    subs r2,r2,r0    @ 080da850 121a
    ldr r3, PTR_BLDALPHA_080da868            @ 080da852 054b
    lsls r1,r2,#0x18    @ 080da854 1106
    lsrs r1,r1,#0x18    @ 080da856 090e
    movs r0,#0x10    @ 080da858 1020
    subs r0,r0,r2    @ 080da85a 801a
    lsls r0,r0,#0x18    @ 080da85c 0006
    lsrs r0,r0,#0x10    @ 080da85e 000c
    orrs r1,r0    @ 080da860 0143
    strh r1,[r3,#0x0]                        @ 080da862 1980
    b LAB_080da876                           @ 080da864 07e0
    .zero  0x2
PTR_BLDALPHA_080da868:
    .word  BLDALPHA                       @ 080da868 52000004
LAB_080da86c:
    movs r1,#0x80    @ 080da86c 8021
    lsls r1,r1,#0x13    @ 080da86e c904
    movs r0,#0x80    @ 080da870 8020
    lsls r0,r0,#0x4    @ 080da872 0001
    strh r0,[r1,#0x0]                        @ 080da874 0880
LAB_080da876:
    movs r1,#0x6    @ 080da876 0621
    ldrsh r0,[r7,r1]                         @ 080da878 785e
    cmp r0,#0x0                              @ 080da87a 0028
    bge LAB_080da8ee                         @ 080da87c 37da
    movs r0,#0x4    @ 080da87e 0420
    strh r0,[r7,#0x2]                        @ 080da880 7880
    ldr r1, PTR_BG0CNT_080da908              @ 080da882 2149
    ldrh r2,[r1,#0x0]                        @ 080da884 0a88
    ldr r3, DAT_080da90c                     @ 080da886 214b
    adds r0,r3,#0x0    @ 080da888 181c
    ands r0,r2    @ 080da88a 1040
    strh r0,[r1,#0x0]                        @ 080da88c 0880
    ldrh r0,[r1,#0x0]                        @ 080da88e 0888
    strh r0,[r1,#0x0]                        @ 080da890 0880
    adds r1,#0x2    @ 080da892 0231
    ldrh r2,[r1,#0x0]                        @ 080da894 0a88
    adds r0,r3,#0x0    @ 080da896 181c
    ands r0,r2    @ 080da898 1040
    strh r0,[r1,#0x0]                        @ 080da89a 0880
    ldrh r0,[r1,#0x0]                        @ 080da89c 0888
    movs r4,#0x1    @ 080da89e 0124
    orrs r0,r4    @ 080da8a0 2043
    strh r0,[r1,#0x0]                        @ 080da8a2 0880
    adds r1,#0x2    @ 080da8a4 0231
    ldrh r2,[r1,#0x0]                        @ 080da8a6 0a88
    adds r0,r3,#0x0    @ 080da8a8 181c
    ands r0,r2    @ 080da8aa 1040
    strh r0,[r1,#0x0]                        @ 080da8ac 0880
    ldrh r0,[r1,#0x0]                        @ 080da8ae 0888
    orrs r0,r4    @ 080da8b0 2043
    strh r0,[r1,#0x0]                        @ 080da8b2 0880
    ldr r2, PTR_BG3CNT_080da910              @ 080da8b4 164a
    ldrh r0,[r2,#0x0]                        @ 080da8b6 1088
    ands r3,r0    @ 080da8b8 0340
    strh r3,[r2,#0x0]                        @ 080da8ba 1380
    ldrh r0,[r2,#0x0]                        @ 080da8bc 1088
    movs r1,#0x3    @ 080da8be 0321
    orrs r0,r1    @ 080da8c0 0843
    strh r0,[r2,#0x0]                        @ 080da8c2 1080
    ldr r1, PTR_BLDCNT_080da914              @ 080da8c4 1349
    ldr r2, DAT_080da918                     @ 080da8c6 144a
    adds r0,r2,#0x0    @ 080da8c8 101c
    strh r0,[r1,#0x0]                        @ 080da8ca 0880
    adds r1,#0x2    @ 080da8cc 0231
    ldr r3, DAT_080da91c                     @ 080da8ce 134b
    adds r0,r3,#0x0    @ 080da8d0 181c
    strh r0,[r1,#0x0]                        @ 080da8d2 0880
    movs r0,#0xe3    @ 080da8d4 e320
    lsls r0,r0,#0x3    @ 080da8d6 c000
    adds r1,r7,r0    @ 080da8d8 3918
    movs r0,#0x3    @ 080da8da 0320
    rsbs r0,r0,#0    @ 080da8dc 4042
    ldrb r2,[r1,#0x0]                        @ 080da8de 0a78
    ands r0,r2    @ 080da8e0 1040
    strb r0,[r1,#0x0]                        @ 080da8e2 0870
    ldr r1, DAT_080da920                     @ 080da8e4 0e49
    movs r0,#0x13    @ 080da8e6 1320
    strh r0,[r1,#0x10]                       @ 080da8e8 0882
    movs r3,#0x1    @ 080da8ea 0123
    .hword 0x4699    @ 080da8ec 9946
LAB_080da8ee:
    movs r0,#0x1    @ 080da8ee 0120
    bl render_pack_slot_highlight_oam        @ 080da8f0 fef7aefe
    movs r0,#0x3    @ 080da8f4 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da8f6 fef7e5fc
    .hword 0x4648    @ 080da8fa 4846
    pop {r3,r4}                              @ 080da8fc 18bc
    .hword 0x4698    @ 080da8fe 9846
    .hword 0x46a1    @ 080da900 a146
    pop {r4,r5,r6,r7}                        @ 080da902 f0bc
    pop {r1}                                 @ 080da904 02bc
    bx r1                                    @ 080da906 0847
PTR_BG0CNT_080da908:
    .word  BG0CNT                         @ 080da908 08000004
DAT_080da90c:
    .word  0x0000fffc                     @ 080da90c fcff0000
PTR_BG3CNT_080da910:
    .word  BG3CNT                         @ 080da910 0e000004
PTR_BLDCNT_080da914:
    .word  BLDCNT                         @ 080da914 50000004
DAT_080da918:
    .word  0x00003f3f                     @ 080da918 3f3f0000
DAT_080da91c:
    .word  0x00001010                     @ 080da91c 10100000
DAT_080da920:
    .word  pack_ui_state                  @ 080da920 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0xd.
@ Calls render_pack_selection_label_to_bg_vram(0x350, 0x390) to render the list page selection
@ label to BG VRAM. If render completes (returns 1): writes [+0x1a]:=1, [+0x18]:=1, sets next
@ step=0xd; otherwise sets next step=0xe. Unconditionally calls render_pack_card_sprite_by_flip_state(0),
@ render_pack_slot_arrow_oam(0), render_pack_card_highlight_pulse_by_mode(0),
@ render_pack_slot_highlight_oam(1), write_pack_banner_oam_for_all_slots(3).
@ Returns fixed 1 (movs r0,#1 @ 080da96a; Sub-case E pop{r1};bx r1).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080da944)
@ Returns: r0=u8 1 (step-complete flag)
@ Side effects:
@   [pack_ui_state+0xc+0x1a] := 1 (on render-complete path)
@   [pack_ui_state+0xc+0x18] := 1 (on render-complete path)
@   [pack_ui_state+0xc+0x4] := 0xd or 0xe (step index)
@ Constants:
@   pack_ui_state = 0x03005850
@   LABEL_X = 0x350
@   LABEL_Y = 0x390
@   NEXT_STATE_DONE = 0xd
@   NEXT_STATE_CONT = 0xe
tick_pack_list_label_vram:
    push {r4,lr}                             @ 080da924 10b5
    ldr r0, DAT_080da944                     @ 080da926 0748
    adds r4,r0,#0x0    @ 080da928 041c
    adds r4,#0xc    @ 080da92a 0c34
    movs r0,#0xd4    @ 080da92c d420
    lsls r0,r0,#0x2    @ 080da92e 8000
    movs r1,#0xe4    @ 080da930 e421
    lsls r1,r1,#0x2    @ 080da932 8900
    bl render_pack_selection_label_to_bg_vram @ 080da934 01f0c2fe
    cmp r0,#0x1                              @ 080da938 0128
    bne LAB_080da948                         @ 080da93a 05d1
    strh r0,[r4,#0x1a]                       @ 080da93c 6083
    strh r0,[r4,#0x18]                       @ 080da93e 2083
    movs r0,#0xd    @ 080da940 0d20
    b LAB_080da94a                           @ 080da942 02e0
DAT_080da944:
    .word  pack_ui_state                  @ 080da944 50580003
LAB_080da948:
    movs r0,#0xe    @ 080da948 0e20
LAB_080da94a:
    strh r0,[r4,#0x4]                        @ 080da94a a080
    movs r0,#0x0    @ 080da94c 0020
    bl render_pack_card_sprite_by_flip_state @ 080da94e f9f7abfe
    movs r0,#0x0    @ 080da952 0020
    bl render_pack_slot_arrow_oam            @ 080da954 fef73cfe
    movs r0,#0x0    @ 080da958 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080da95a fef7effc
    movs r0,#0x1    @ 080da95e 0120
    bl render_pack_slot_highlight_oam        @ 080da960 fef776fe
    movs r0,#0x3    @ 080da964 0320
    bl write_pack_banner_oam_for_all_slots   @ 080da966 fef7adfc
    movs r0,#0x1    @ 080da96a 0120
    pop {r4}                                 @ 080da96c 10bc
    pop {r1}                                 @ 080da96e 02bc
    bx r1                                    @ 080da970 0847
    .zero  0x2

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0xe.
@ Per-frame handler for vertical (up/down) input on the pack list page. First calls
@ tick_overlay_animation_step(0) to advance overlay. Reads gPrng+0x1d0 scene type [+0x1c]=2
@ to confirm; checks gPrng+0x148 bit1 (DOWN): if [+0x18]=1, clears direction and calls
@ init_pack_scroll_animation(down), sets step=0x10; else sets step=0x10 and calls
@ render_pack_list_label_sprites_and_palette. Checks bit0 (UP): based on [+0x18] state,
@ determines upward scroll params or clears [+0x724] bit. Checks bit4/bit5 for fast up/down.
@ All input branches set r6=1. On exit based on r6: clears [+0x718] bit5; unconditionally calls
@ render_pack_card_sprite_by_flip_state(0), render_pack_slot_arrow_oam(0),
@ render_pack_card_highlight_pulse_by_mode(0), render_pack_slot_highlight_oam(1),
@ write_pack_banner_oam_for_all_slots(3). Returns r6 (Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r4,DAT_080da9d0)
@ Returns: r0=u8 (0=no input, 1=input handled; Sub-case E adds r0,r6 @ 080dab14)
@ Side effects:
@   [pack_ui_state+0xc+0x18]: direction/slot updated
@   [pack_ui_state+0xc+0x4]: := 0xf or 0x10 or 0x11 (step advance)
@   [pack_ui_state+0x724] byte: bit5 cleared
@   [pack_ui_state+0x718] byte: bit5 cleared (r6=0 path)
@ Constants:
@   pack_ui_state = 0x03005850
@   INPUT_FIELD = 0x148
@   SCROLL_Y = 0x98, SCROLL_STEP = 8
@   NEXT_STEP_UP = 0xf, NEXT_STEP_DOWN = 0x10, NEXT_STEP_CONFIRM = 0x11
@   STATE_FLAGS_OFFSET = 0x724, SPRITE_CTRL_OFFSET = 0x718
tick_pack_list_input_vertical:
    push {r4,r5,r6,lr}                       @ 080da974 70b5
    ldr r4, DAT_080da9d0                     @ 080da976 164c
    adds r5,r4,#0x0    @ 080da978 251c
    adds r5,#0xc    @ 080da97a 0c35
    movs r6,#0x0    @ 080da97c 0026
    movs r0,#0x0    @ 080da97e 0020
    bl tick_overlay_animation_step           @ 080da980 02f030fe
    ldr r2, PTR_gPrng_080da9d4               @ 080da984 134a
    movs r1,#0xe8    @ 080da986 e821
    lsls r1,r1,#0x1    @ 080da988 4900
    adds r0,r2,r1    @ 080da98a 5018
    ldr r0,[r0,#0x0]                         @ 080da98c 0068
    ldrh r1,[r0,#0x1c]                       @ 080da98e 818b
    cmp r1,#0x2                              @ 080da990 0229
    beq LAB_080da996                         @ 080da992 00d0
    b LAB_080daad0                           @ 080da994 9ce0
LAB_080da996:
    movs r3,#0xa4    @ 080da996 a423
    lsls r3,r3,#0x1    @ 080da998 5b00
    adds r0,r2,r3    @ 080da99a d018
    ldrh r2,[r0,#0x0]                        @ 080da99c 0288
    ands r1,r2    @ 080da99e 1140
    cmp r1,#0x0                              @ 080da9a0 0029
    beq LAB_080da9f8                         @ 080da9a2 29d0
    ldrh r0,[r5,#0x18]                       @ 080da9a4 288b
    cmp r0,#0x1                              @ 080da9a6 0128
    bne LAB_080da9dc                         @ 080da9a8 18d1
    strh r6,[r5,#0x18]                       @ 080da9aa 2e83
    movs r0,#0x0    @ 080da9ac 0020
    bl get_pack_icon_y_by_dir                @ 080da9ae fef745fa
    movs r1,#0x98    @ 080da9b2 9821
    movs r2,#0x8    @ 080da9b4 0822
    bl init_pack_scroll_animation            @ 080da9b6 f9f7e7ff
    movs r0,#0x1    @ 080da9ba 0120
    bl sync_state_and_init_sprite            @ 080da9bc 1ff07af8
    ldr r2, DAT_080da9d8                     @ 080da9c0 054a
    adds r1,r4,r2    @ 080da9c2 a118
    movs r0,#0x21    @ 080da9c4 2120
    rsbs r0,r0,#0    @ 080da9c6 4042
    ldrb r3,[r1,#0x0]                        @ 080da9c8 0b78
    ands r0,r3    @ 080da9ca 1840
    b LAB_080daaa4                           @ 080da9cc 6ae0
    .zero  0x2
DAT_080da9d0:
    .word  pack_ui_state                  @ 080da9d0 50580003
PTR_gPrng_080da9d4:
    .word  gPrng                          @ 080da9d4 40000003
DAT_080da9d8:
    .word  0x00000724                     @ 080da9d8 24070000
LAB_080da9dc:
    movs r0,#0x10    @ 080da9dc 1020
    strh r0,[r5,#0x4]                        @ 080da9de a880
    movs r0,#0x1    @ 080da9e0 0120
    strh r0,[r5,#0x18]                       @ 080da9e2 2883
    bl render_pack_list_label_sprites_and_palette @ 080da9e4 fef7fcfb
    movs r0,#0x1    @ 080da9e8 0120
    bl sync_state_and_init_sprite            @ 080da9ea 1ff063f8
    ldr r0, DAT_080da9f4                     @ 080da9ee 0148
    adds r1,r4,r0    @ 080da9f0 2118
    b LAB_080daa1c                           @ 080da9f2 13e0
DAT_080da9f4:
    .word  0x00000724                     @ 080da9f4 24070000
LAB_080da9f8:
    movs r1,#0x1    @ 080da9f8 0121
    adds r0,r1,#0x0    @ 080da9fa 081c
    ands r0,r2    @ 080da9fc 1040
    cmp r0,#0x0                              @ 080da9fe 0028
    beq LAB_080daa50                         @ 080daa00 26d0
    ldrh r0,[r5,#0x18]                       @ 080daa02 288b
    cmp r0,#0x0                              @ 080daa04 0028
    bne LAB_080daa30                         @ 080daa06 13d1
    movs r0,#0x10    @ 080daa08 1020
    strh r0,[r5,#0x4]                        @ 080daa0a a880
    strh r1,[r5,#0x18]                       @ 080daa0c 2983
    bl render_pack_list_label_sprites_and_palette @ 080daa0e fef7e7fb
    movs r0,#0x1    @ 080daa12 0120
    bl sync_state_and_init_sprite            @ 080daa14 1ff04ef8
    ldr r3, DAT_080daa2c                     @ 080daa18 044b
    adds r1,r4,r3    @ 080daa1a e118
LAB_080daa1c:
    movs r0,#0x21    @ 080daa1c 2120
    rsbs r0,r0,#0    @ 080daa1e 4042
    ldrb r2,[r1,#0x0]                        @ 080daa20 0a78
    ands r0,r2    @ 080daa22 1040
    strb r0,[r1,#0x0]                        @ 080daa24 0870
    movs r6,#0x1    @ 080daa26 0126
    b LAB_080daad0                           @ 080daa28 52e0
    .zero  0x2
DAT_080daa2c:
    .word  0x00000724                     @ 080daa2c 24070000
LAB_080daa30:
    cmp r0,#0x1                              @ 080daa30 0128
    bne LAB_080daad0                         @ 080daa32 4dd1
    movs r0,#0x24    @ 080daa34 2420
    bl sync_state_and_init_sprite            @ 080daa36 1ff03df8
    ldr r3, DAT_080daa4c                     @ 080daa3a 044b
    adds r0,r4,r3    @ 080daa3c e018
    movs r1,#0x21    @ 080daa3e 2121
    rsbs r1,r1,#0    @ 080daa40 4942
    ldrb r2,[r0,#0x0]                        @ 080daa42 0278
    ands r1,r2    @ 080daa44 1140
    strb r1,[r0,#0x0]                        @ 080daa46 0170
    movs r0,#0x11    @ 080daa48 1120
    b LAB_080daaa8                           @ 080daa4a 2de0
DAT_080daa4c:
    .word  0x00000724                     @ 080daa4c 24070000
LAB_080daa50:
    movs r0,#0x10    @ 080daa50 1020
    ands r0,r2    @ 080daa52 1040
    cmp r0,#0x0                              @ 080daa54 0028
    beq LAB_080daa70                         @ 080daa56 0bd0
    ldrh r0,[r5,#0x18]                       @ 080daa58 288b
    cmp r0,#0x0                              @ 080daa5a 0028
    bne LAB_080daa62                         @ 080daa5c 01d1
    adds r0,#0x1    @ 080daa5e 0130
    b LAB_080daa82                           @ 080daa60 0fe0
LAB_080daa62:
    ldr r3, DAT_080daa6c                     @ 080daa62 024b
    adds r4,r4,r3    @ 080daa64 e418
    movs r0,#0x20    @ 080daa66 2020
    b LAB_080daaba                           @ 080daa68 27e0
    .zero  0x2
DAT_080daa6c:
    .word  0x00000724                     @ 080daa6c 24070000
LAB_080daa70:
    movs r1,#0x20    @ 080daa70 2021
    adds r0,r1,#0x0    @ 080daa72 081c
    ands r0,r2    @ 080daa74 1040
    cmp r0,#0x0                              @ 080daa76 0028
    beq LAB_080daad0                         @ 080daa78 2ad0
    ldrh r0,[r5,#0x18]                       @ 080daa7a 288b
    cmp r0,#0x0                              @ 080daa7c 0028
    beq LAB_080daab4                         @ 080daa7e 19d0
    subs r0,#0x1    @ 080daa80 0138
LAB_080daa82:
    strh r0,[r5,#0x18]                       @ 080daa82 2883
    ldrh r0,[r5,#0x18]                       @ 080daa84 288b
    bl get_pack_icon_y_by_dir                @ 080daa86 fef7d9f9
    movs r1,#0x98    @ 080daa8a 9821
    movs r2,#0x8    @ 080daa8c 0822
    bl init_pack_scroll_animation            @ 080daa8e f9f77bff
    movs r0,#0x0    @ 080daa92 0020
    bl sync_state_and_init_sprite            @ 080daa94 1ff00ef8
    ldr r3, DAT_080daab0                     @ 080daa98 054b
    adds r1,r4,r3    @ 080daa9a e118
    movs r0,#0x21    @ 080daa9c 2120
    rsbs r0,r0,#0    @ 080daa9e 4042
    ldrb r2,[r1,#0x0]                        @ 080daaa0 0a78
    ands r0,r2    @ 080daaa2 1040
LAB_080daaa4:
    strb r0,[r1,#0x0]                        @ 080daaa4 0870
    movs r0,#0xf    @ 080daaa6 0f20
LAB_080daaa8:
    strh r0,[r5,#0x4]                        @ 080daaa8 a880
    movs r6,#0x1    @ 080daaaa 0126
    b LAB_080daad0                           @ 080daaac 10e0
    .zero  0x2
DAT_080daab0:
    .word  0x00000724                     @ 080daab0 24070000
LAB_080daab4:
    ldr r3, DAT_080dab1c                     @ 080daab4 194b
    adds r4,r4,r3    @ 080daab6 e418
    adds r0,r1,#0x0    @ 080daab8 081c
LAB_080daaba:
    ldrb r1,[r4,#0x0]                        @ 080daaba 2178
    ands r0,r1    @ 080daabc 0840
    cmp r0,#0x0                              @ 080daabe 0028
    bne LAB_080daad0                         @ 080daac0 06d1
    movs r0,#0x2    @ 080daac2 0220
    bl sync_state_and_init_sprite            @ 080daac4 1ef0f6ff
    movs r0,#0x20    @ 080daac8 2020
    ldrb r2,[r4,#0x0]                        @ 080daaca 2278
    orrs r0,r2    @ 080daacc 1043
    strb r0,[r4,#0x0]                        @ 080daace 2070
LAB_080daad0:
    cmp r6,#0x1                              @ 080daad0 012e
    beq LAB_080daae6                         @ 080daad2 08d0
    ldr r0, PTR_gPrng_080dab20               @ 080daad4 1248
    movs r3,#0xa3    @ 080daad6 a323
    lsls r3,r3,#0x1    @ 080daad8 5b00
    adds r1,r0,r3    @ 080daada c118
    movs r0,#0xf0    @ 080daadc f020
    ldrh r1,[r1,#0x0]                        @ 080daade 0988
    ands r0,r1    @ 080daae0 0840
    cmp r0,#0x0                              @ 080daae2 0028
    bne LAB_080daaf6                         @ 080daae4 07d1
LAB_080daae6:
    movs r0,#0xe3    @ 080daae6 e320
    lsls r0,r0,#0x3    @ 080daae8 c000
    adds r1,r5,r0    @ 080daaea 2918
    movs r0,#0x21    @ 080daaec 2120
    rsbs r0,r0,#0    @ 080daaee 4042
    ldrb r2,[r1,#0x0]                        @ 080daaf0 0a78
    ands r0,r2    @ 080daaf2 1040
    strb r0,[r1,#0x0]                        @ 080daaf4 0870
LAB_080daaf6:
    movs r0,#0x0    @ 080daaf6 0020
    bl render_pack_card_sprite_by_flip_state @ 080daaf8 f9f7d6fd
    movs r0,#0x0    @ 080daafc 0020
    bl render_pack_slot_arrow_oam            @ 080daafe fef767fd
    movs r0,#0x0    @ 080dab02 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080dab04 fef71afc
    movs r0,#0x1    @ 080dab08 0120
    bl render_pack_slot_highlight_oam        @ 080dab0a fef7a1fd
    movs r0,#0x3    @ 080dab0e 0320
    bl write_pack_banner_oam_for_all_slots   @ 080dab10 fef7d8fb
    adds r0,r6,#0x0    @ 080dab14 301c
    pop {r4,r5,r6}                           @ 080dab16 70bc
    pop {r1}                                 @ 080dab18 02bc
    bx r1                                    @ 080dab1a 0847
DAT_080dab1c:
    .word  0x00000724                     @ 080dab1c 24070000
PTR_gPrng_080dab20:
    .word  gPrng                          @ 080dab20 40000003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0xf.
@ Per-frame handler that checks A-key confirm input and advances the pack list page state.
@ Reads gPrng+0x1d0 scene type [+0x1c]=2 to confirm; checks gPrng+0x148 bit0 (confirm key).
@ If confirm key pressed: calls sync_state_and_init_sprite(0x24), writes [+0x10]:=0x10 to
@ advance state machine, sets r4=1. Unconditionally calls tick_overlay_animation_step(0),
@ render_pack_card_sprite_by_flip_state(0), render_pack_slot_arrow_oam(0),
@ render_pack_card_highlight_pulse_by_mode(0), render_pack_slot_highlight_oam(1),
@ write_pack_banner_oam_for_all_slots(3). Returns r4 (0=waiting, 1=confirmed; Sub-case E).
@ 
@ Params: none (r4 initialized internally via movs r4,#0)
@ Returns: r0=u8 (0=waiting, 1=confirmed; Sub-case E adds r0,r4 @ 080dab7a)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 0x10 (on confirm-key path)
@ Constants:
@   pack_ui_state = 0x03005850
@   NEXT_STATE = 0x10
@   SPRITE_INIT_CODE = 0x24
tick_pack_list_confirm_input:
    push {r4,lr}                             @ 080dab24 10b5
    movs r4,#0x0    @ 080dab26 0024
    ldr r1, PTR_gPrng_080dab84               @ 080dab28 1649
    movs r2,#0xe8    @ 080dab2a e822
    lsls r2,r2,#0x1    @ 080dab2c 5200
    adds r0,r1,r2    @ 080dab2e 8818
    ldr r0,[r0,#0x0]                         @ 080dab30 0068
    ldrh r0,[r0,#0x1c]                       @ 080dab32 808b
    cmp r0,#0x2                              @ 080dab34 0228
    bne LAB_080dab56                         @ 080dab36 0ed1
    movs r0,#0xa4    @ 080dab38 a420
    lsls r0,r0,#0x1    @ 080dab3a 4000
    adds r1,r1,r0    @ 080dab3c 0918
    movs r0,#0x1    @ 080dab3e 0120
    ldrh r1,[r1,#0x0]                        @ 080dab40 0988
    ands r0,r1    @ 080dab42 0840
    cmp r0,#0x0                              @ 080dab44 0028
    beq LAB_080dab56                         @ 080dab46 06d0
    movs r0,#0x24    @ 080dab48 2420
    bl sync_state_and_init_sprite            @ 080dab4a 1ef0b3ff
    ldr r1, DAT_080dab88                     @ 080dab4e 0e49
    movs r0,#0x10    @ 080dab50 1020
    strh r0,[r1,#0x10]                       @ 080dab52 0882
    movs r4,#0x1    @ 080dab54 0124
LAB_080dab56:
    movs r0,#0x0    @ 080dab56 0020
    bl tick_overlay_animation_step           @ 080dab58 02f044fd
    movs r0,#0x0    @ 080dab5c 0020
    bl render_pack_card_sprite_by_flip_state @ 080dab5e f9f7a3fd
    movs r0,#0x0    @ 080dab62 0020
    bl render_pack_slot_arrow_oam            @ 080dab64 fef734fd
    movs r0,#0x0    @ 080dab68 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080dab6a fef7e7fb
    movs r0,#0x1    @ 080dab6e 0120
    bl render_pack_slot_highlight_oam        @ 080dab70 fef76efd
    movs r0,#0x3    @ 080dab74 0320
    bl write_pack_banner_oam_for_all_slots   @ 080dab76 fef7a5fb
    adds r0,r4,#0x0    @ 080dab7a 201c
    pop {r4}                                 @ 080dab7c 10bc
    pop {r1}                                 @ 080dab7e 02bc
    bx r1                                    @ 080dab80 0847
    .zero  0x2
PTR_gPrng_080dab84:
    .word  gPrng                          @ 080dab84 40000003
DAT_080dab88:
    .word  pack_ui_state                  @ 080dab88 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0x10.
@ Drives the pack list page vertical scroll interpolation. Calls tick_pack_scroll_interp_step
@ (r4=return value); calls tick_overlay_animation_step(0); unconditionally calls
@ render_pack_card_sprite_by_flip_state(0), render_pack_slot_arrow_oam(0),
@ render_pack_card_highlight_pulse_by_mode(0), render_pack_slot_highlight_oam(1),
@ write_pack_banner_oam_for_all_slots(3). If scroll complete (r4==1): writes [+0x10]:=0xd
@ to advance state machine. Returns r4 (Sub-case E).
@ 
@ Params: none (no APCS input)
@ Returns: r0=u8 (0=scrolling, 1=complete; Sub-case E adds r0,r4 @ 080dabc2)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 0xd (on scroll-complete path)
@ Constants:
@   pack_ui_state = 0x03005850
@   NEXT_STATE = 0xd
tick_pack_list_scroll_interp_vertical:
    push {r4,lr}                             @ 080dab8c 10b5
    bl tick_pack_scroll_interp_step          @ 080dab8e f9f79bfe
    adds r4,r0,#0x0    @ 080dab92 041c
    movs r0,#0x0    @ 080dab94 0020
    bl tick_overlay_animation_step           @ 080dab96 02f025fd
    movs r0,#0x0    @ 080dab9a 0020
    bl render_pack_card_sprite_by_flip_state @ 080dab9c f9f784fd
    movs r0,#0x0    @ 080daba0 0020
    bl render_pack_slot_arrow_oam            @ 080daba2 fef715fd
    movs r0,#0x0    @ 080daba6 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080daba8 fef7c8fb
    movs r0,#0x1    @ 080dabac 0120
    bl render_pack_slot_highlight_oam        @ 080dabae fef74ffd
    movs r0,#0x3    @ 080dabb2 0320
    bl write_pack_banner_oam_for_all_slots   @ 080dabb4 fef786fb
    cmp r4,#0x1                              @ 080dabb8 012c
    bne LAB_080dabc2                         @ 080dabba 02d1
    ldr r1, DAT_080dabcc                     @ 080dabbc 0349
    movs r0,#0xd    @ 080dabbe 0d20
    strh r0,[r1,#0x10]                       @ 080dabc0 0882
LAB_080dabc2:
    adds r0,r4,#0x0    @ 080dabc2 201c
    pop {r4}                                 @ 080dabc4 10bc
    pop {r1}                                 @ 080dabc6 02bc
    bx r1                                    @ 080dabc8 0847
    .zero  0x2
DAT_080dabcc:
    .word  pack_ui_state                  @ 080dabcc 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0x11.
@ One-shot scroll triggered after overlay animation completes on the pack list page. Calls
@ tick_overlay_animation_step(1) to advance overlay (r5=return value); if complete (r5==1):
@ reads [+0x18], calls get_pack_icon_y_by_dir to get target Y, calls
@ init_pack_scroll_animation(y, 0x98, mode=1), then blocks in tick_pack_scroll_interp_step loop
@ until scroll complete, writes [+0x10]:=4 to advance state machine. Unconditionally calls
@ render_pack_slot_arrow_oam(0), render_pack_card_highlight_pulse_by_mode(0),
@ render_pack_slot_highlight_oam(1), write_pack_banner_oam_for_all_slots(3).
@ Returns r5 (Sub-case E).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080dac20)
@ Returns: r0=u8 (0=overlay animating, 1=complete; Sub-case E adds r0,r5 @ 080dac18)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 4 (on complete)
@ Constants:
@   pack_ui_state = 0x03005850
@   SCROLL_Y = 0x98, SCROLL_MODE = 1
@   NEXT_STATE = 4
tick_pack_list_overlay_scroll:
    push {r4,r5,lr}                          @ 080dabd0 30b5
    ldr r0, DAT_080dac20                     @ 080dabd2 1348
    adds r4,r0,#0x0    @ 080dabd4 041c
    adds r4,#0xc    @ 080dabd6 0c34
    movs r0,#0x1    @ 080dabd8 0120
    bl tick_overlay_animation_step           @ 080dabda 02f003fd
    adds r5,r0,#0x0    @ 080dabde 051c
    cmp r5,#0x1                              @ 080dabe0 012d
    bne LAB_080dac00                         @ 080dabe2 0dd1
    ldrh r0,[r4,#0x18]                       @ 080dabe4 208b
    bl get_pack_icon_y_by_dir                @ 080dabe6 fef729f9
    movs r1,#0x98    @ 080dabea 9821
    movs r2,#0x1    @ 080dabec 0122
    bl init_pack_scroll_animation            @ 080dabee f9f7cbfe
LAB_080dabf2:
    bl tick_pack_scroll_interp_step          @ 080dabf2 f9f769fe
    cmp r0,#0x0                              @ 080dabf6 0028
    beq LAB_080dabf2                         @ 080dabf8 fbd0
    ldr r1, DAT_080dac20                     @ 080dabfa 0949
    movs r0,#0x4    @ 080dabfc 0420
    strh r0,[r1,#0x10]                       @ 080dabfe 0882
LAB_080dac00:
    movs r0,#0x0    @ 080dac00 0020
    bl render_pack_slot_arrow_oam            @ 080dac02 fef7e5fc
    movs r0,#0x0    @ 080dac06 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080dac08 fef798fb
    movs r0,#0x1    @ 080dac0c 0120
    bl render_pack_slot_highlight_oam        @ 080dac0e fef71ffd
    movs r0,#0x3    @ 080dac12 0320
    bl write_pack_banner_oam_for_all_slots   @ 080dac14 fef756fb
    adds r0,r5,#0x0    @ 080dac18 281c
    pop {r4,r5}                              @ 080dac1a 30bc
    pop {r1}                                 @ 080dac1c 02bc
    bx r1                                    @ 080dac1e 0847
DAT_080dac20:
    .word  pack_ui_state                  @ 080dac20 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0x12.
@ Executes BG fade-in animation for the pack list page. On first entry (pack_ui_state+0x724
@ bit1 not set): clears BG3CNT low 2 bits, sets BG0CNT/BG1CNT/BG2CNT priorities 1/2/3, writes
@ BLDCNT=0x1748, BLDALPHA:=0x1000, sets frame counter [+0x6]:=0xa, sets bit1. Each frame
@ decrements [+0x6]; while counter>0: interpolates BLDALPHA linearly via bios_div(count*0x10/0xa);
@ when counter<=0: restores BG priorities, writes BLDCNT=0x3f3f, BLDALPHA=0x1010, r6=0, writes
@ [+0x2]:=2, clears [+0x718] bit0/bit2, writes [+0x10]:=0x13 to advance state machine.
@ Calls render_pack_slot_highlight_oam(r6+1), render_pack_card_highlight_pulse_by_mode(r6),
@ write_pack_banner_oam_for_all_slots(r6+3). Returns r8 (0=animating, 1=complete; Sub-case E,
@ .hword 0x4640 mov r0,r8 @ 080dad82).
@ 
@ Params: none (r0 immediately clobbered; r8 initialized to 0 via movs r1,#0;mov r8,r1 @ 080dac30)
@ Returns: r0=u8 (0=animating, 1=complete; Sub-case E mov r0,r8 @ 080dad82)
@ Side effects:
@   [BG3CNT] (0x0400000e): cleared & 0xfffc
@   [BG0CNT] (0x04000008): cleared then |= 1
@   [BG1CNT] (0x0400000a): cleared then |= 2
@   [BG2CNT] (0x0400000c): cleared then |= 2
@   [BLDCNT] (0x04000050): := 0x1748 (init) or 0x3f3f (final)
@   [BLDALPHA] (0x04000052): linear interpolation each frame, final 0x1010
@   [DISPCNT] (0x04000000): |= 0x800
@   [pack_ui_state+0xc+0x6] := 0xa
@   [pack_ui_state+0x724] |= 0x2
@   [pack_ui_state+0xc+0x2] := 2 (on complete)
@   [pack_ui_state+0xc+0x10] := 0x13 (on complete)
@   [pack_ui_state+0x718] byte: &= ~0xfd (on complete)
@ Constants:
@   pack_ui_state = 0x03005850
@   STATE_FLAGS_OFFSET = 0x724
@   FADE_FRAMES = 0xa
@   DISPCNT = 0x04000000, OBJ_TILE_MAP_1D_BIT = 0x800
@   BG3CNT = 0x0400000e, BG0CNT = 0x04000008, BG1CNT = 0x0400000a
@   BLDCNT = 0x04000050, BLDCNT_VAL_INIT = 0x1748, BLDCNT_VAL_FINAL = 0x3f3f
@   BLDALPHA = 0x04000052, BLDALPHA_INIT = 0x1000, BLDALPHA_FINAL = 0x1010
@   NEXT_STATE = 0x13
tick_pack_list_fadein_bg:
    push {r4,r5,r6,r7,lr}                    @ 080dac24 f0b5
    .hword 0x4647    @ 080dac26 4746
    push {r7}                                @ 080dac28 80b4
    ldr r0, DAT_080dacd8                     @ 080dac2a 2b48
    adds r5,r0,#0x0    @ 080dac2c 051c
    adds r5,#0xc    @ 080dac2e 0c35
    movs r1,#0x0    @ 080dac30 0021
    .hword 0x4688    @ 080dac32 8846
    movs r6,#0x1    @ 080dac34 0126
    ldr r2, DAT_080dacdc                     @ 080dac36 294a
    adds r7,r0,r2    @ 080dac38 8718
    ldrb r4,[r7,#0x0]                        @ 080dac3a 3c78
    movs r0,#0x2    @ 080dac3c 0220
    ands r0,r4    @ 080dac3e 2040
    cmp r0,#0x0                              @ 080dac40 0028
    bne LAB_080daca2                         @ 080dac42 2ed1
    ldr r1, PTR_BG3CNT_080dace0              @ 080dac44 2649
    ldrh r2,[r1,#0x0]                        @ 080dac46 0a88
    ldr r3, DAT_080dace4                     @ 080dac48 264b
    adds r0,r3,#0x0    @ 080dac4a 181c
    ands r0,r2    @ 080dac4c 1040
    strh r0,[r1,#0x0]                        @ 080dac4e 0880
    ldrh r0,[r1,#0x0]                        @ 080dac50 0888
    strh r0,[r1,#0x0]                        @ 080dac52 0880
    ldr r2, PTR_BG0CNT_080dace8              @ 080dac54 244a
    ldrh r1,[r2,#0x0]                        @ 080dac56 1188
    adds r0,r3,#0x0    @ 080dac58 181c
    ands r0,r1    @ 080dac5a 0840
    strh r0,[r2,#0x0]                        @ 080dac5c 1080
    ldrh r0,[r2,#0x0]                        @ 080dac5e 1088
    movs r1,#0x1    @ 080dac60 0121
    orrs r0,r1    @ 080dac62 0843
    strh r0,[r2,#0x0]                        @ 080dac64 1080
    ldr r1, PTR_BG1CNT_080dacec              @ 080dac66 2149
    ldrh r2,[r1,#0x0]                        @ 080dac68 0a88
    adds r0,r3,#0x0    @ 080dac6a 181c
    ands r0,r2    @ 080dac6c 1040
    strh r0,[r1,#0x0]                        @ 080dac6e 0880
    ldrh r0,[r1,#0x0]                        @ 080dac70 0888
    movs r2,#0x2    @ 080dac72 0222
    orrs r0,r2    @ 080dac74 1043
    strh r0,[r1,#0x0]                        @ 080dac76 0880
    adds r1,#0x2    @ 080dac78 0231
    ldrh r0,[r1,#0x0]                        @ 080dac7a 0888
    ands r3,r0    @ 080dac7c 0340
    strh r3,[r1,#0x0]                        @ 080dac7e 0b80
    ldrh r0,[r1,#0x0]                        @ 080dac80 0888
    orrs r0,r2    @ 080dac82 1043
    strh r0,[r1,#0x0]                        @ 080dac84 0880
    adds r1,#0x44    @ 080dac86 4431
    ldr r2, DAT_080dacf0                     @ 080dac88 194a
    adds r0,r2,#0x0    @ 080dac8a 101c
    strh r0,[r1,#0x0]                        @ 080dac8c 0880
    adds r1,#0x2    @ 080dac8e 0231
    movs r2,#0x80    @ 080dac90 8022
    lsls r2,r2,#0x5    @ 080dac92 5201
    adds r0,r2,#0x0    @ 080dac94 101c
    strh r0,[r1,#0x0]                        @ 080dac96 0880
    movs r0,#0xa    @ 080dac98 0a20
    strh r0,[r5,#0x6]                        @ 080dac9a e880
    movs r0,#0x2    @ 080dac9c 0220
    orrs r0,r4    @ 080dac9e 2043
    strb r0,[r7,#0x0]                        @ 080daca0 3870
LAB_080daca2:
    ldrh r0,[r5,#0x6]                        @ 080daca2 e888
    subs r0,#0x1    @ 080daca4 0138
    strh r0,[r5,#0x6]                        @ 080daca6 e880
    lsls r0,r0,#0x10    @ 080daca8 0004
    asrs r0,r0,#0x10    @ 080dacaa 0014
    cmp r0,#0x0                              @ 080dacac 0028
    bge LAB_080dacb4                         @ 080dacae 01da
    movs r1,#0x1    @ 080dacb0 0121
    .hword 0x4688    @ 080dacb2 8846
LAB_080dacb4:
    cmp r0,#0x0                              @ 080dacb4 0028
    ble LAB_080dacf8                         @ 080dacb6 1fdd
    movs r2,#0x6    @ 080dacb8 0622
    ldrsh r0,[r5,r2]                         @ 080dacba a85e
    lsls r0,r0,#0x4    @ 080dacbc 0001
    movs r1,#0xa    @ 080dacbe 0a21
    bl bios_div                              @ 080dacc0 33f09cfb
    ldr r2, PTR_BLDALPHA_080dacf4            @ 080dacc4 0b4a
    movs r1,#0x10    @ 080dacc6 1021
    subs r1,r1,r0    @ 080dacc8 091a
    lsls r1,r1,#0x18    @ 080dacca 0906
    lsrs r1,r1,#0x18    @ 080daccc 090e
    lsls r0,r0,#0x18    @ 080dacce 0006
    lsrs r0,r0,#0x10    @ 080dacd0 000c
    orrs r1,r0    @ 080dacd2 0143
    strh r1,[r2,#0x0]                        @ 080dacd4 1180
    b LAB_080dad52                           @ 080dacd6 3ce0
DAT_080dacd8:
    .word  pack_ui_state                  @ 080dacd8 50580003
DAT_080dacdc:
    .word  0x00000724                     @ 080dacdc 24070000
PTR_BG3CNT_080dace0:
    .word  BG3CNT                         @ 080dace0 0e000004
DAT_080dace4:
    .word  0x0000fffc                     @ 080dace4 fcff0000
PTR_BG0CNT_080dace8:
    .word  BG0CNT                         @ 080dace8 08000004
PTR_BG1CNT_080dacec:
    .word  BG1CNT                         @ 080dacec 0a000004
DAT_080dacf0:
    .word  0x00001748                     @ 080dacf0 48170000
PTR_BLDALPHA_080dacf4:
    .word  BLDALPHA                       @ 080dacf4 52000004
LAB_080dacf8:
    ldr r1, PTR_BG0CNT_080dad90              @ 080dacf8 2549
    ldrh r2,[r1,#0x0]                        @ 080dacfa 0a88
    ldr r3, DAT_080dad94                     @ 080dacfc 254b
    adds r0,r3,#0x0    @ 080dacfe 181c
    ands r0,r2    @ 080dad00 1040
    strh r0,[r1,#0x0]                        @ 080dad02 0880
    ldrh r0,[r1,#0x0]                        @ 080dad04 0888
    strh r0,[r1,#0x0]                        @ 080dad06 0880
    adds r1,#0x2    @ 080dad08 0231
    ldrh r2,[r1,#0x0]                        @ 080dad0a 0a88
    adds r0,r3,#0x0    @ 080dad0c 181c
    ands r0,r2    @ 080dad0e 1040
    strh r0,[r1,#0x0]                        @ 080dad10 0880
    ldrh r0,[r1,#0x0]                        @ 080dad12 0888
    movs r4,#0x1    @ 080dad14 0124
    orrs r0,r4    @ 080dad16 2043
    strh r0,[r1,#0x0]                        @ 080dad18 0880
    adds r1,#0x2    @ 080dad1a 0231
    ldrh r2,[r1,#0x0]                        @ 080dad1c 0a88
    adds r0,r3,#0x0    @ 080dad1e 181c
    ands r0,r2    @ 080dad20 1040
    strh r0,[r1,#0x0]                        @ 080dad22 0880
    ldrh r0,[r1,#0x0]                        @ 080dad24 0888
    orrs r0,r4    @ 080dad26 2043
    strh r0,[r1,#0x0]                        @ 080dad28 0880
    ldr r2, PTR_BG3CNT_080dad98              @ 080dad2a 1b4a
    ldrh r0,[r2,#0x0]                        @ 080dad2c 1088
    ands r3,r0    @ 080dad2e 0340
    strh r3,[r2,#0x0]                        @ 080dad30 1380
    ldrh r0,[r2,#0x0]                        @ 080dad32 1088
    movs r1,#0x3    @ 080dad34 0321
    orrs r0,r1    @ 080dad36 0843
    strh r0,[r2,#0x0]                        @ 080dad38 1080
    movs r6,#0x0    @ 080dad3a 0026
    ldr r1, PTR_BLDCNT_080dad9c              @ 080dad3c 1749
    movs r0,#0x3f    @ 080dad3e 3f20
    strh r0,[r1,#0x0]                        @ 080dad40 0880
    adds r1,#0x2    @ 080dad42 0231
    ldr r2, DAT_080dada0                     @ 080dad44 164a
    adds r0,r2,#0x0    @ 080dad46 101c
    strh r0,[r1,#0x0]                        @ 080dad48 0880
    subs r1,#0x52    @ 080dad4a 5239
    movs r0,#0x80    @ 080dad4c 8020
    lsls r0,r0,#0x4    @ 080dad4e 0001
    strh r0,[r1,#0x0]                        @ 080dad50 0880
LAB_080dad52:
    .hword 0x4640    @ 080dad52 4046
    cmp r0,#0x1                              @ 080dad54 0128
    bne LAB_080dad70                         @ 080dad56 0bd1
    movs r0,#0x2    @ 080dad58 0220
    strh r0,[r5,#0x2]                        @ 080dad5a 6880
    movs r2,#0xe3    @ 080dad5c e322
    lsls r2,r2,#0x3    @ 080dad5e d200
    adds r1,r5,r2    @ 080dad60 a918
    subs r0,#0x5    @ 080dad62 0538
    ldrb r2,[r1,#0x0]                        @ 080dad64 0a78
    ands r0,r2    @ 080dad66 1040
    strb r0,[r1,#0x0]                        @ 080dad68 0870
    ldr r1, DAT_080dada4                     @ 080dad6a 0e49
    movs r0,#0x13    @ 080dad6c 1320
    strh r0,[r1,#0x10]                       @ 080dad6e 0882
LAB_080dad70:
    adds r0,r6,#0x1    @ 080dad70 701c
    bl render_pack_slot_highlight_oam        @ 080dad72 fef76dfc
    adds r0,r6,#0x0    @ 080dad76 301c
    bl render_pack_card_highlight_pulse_by_mode @ 080dad78 fef7e0fa
    adds r0,r6,#0x3    @ 080dad7c f01c
    bl write_pack_banner_oam_for_all_slots   @ 080dad7e fef7a1fa
    .hword 0x4640    @ 080dad82 4046
    pop {r3}                                 @ 080dad84 08bc
    .hword 0x4698    @ 080dad86 9846
    pop {r4,r5,r6,r7}                        @ 080dad88 f0bc
    pop {r1}                                 @ 080dad8a 02bc
    bx r1                                    @ 080dad8c 0847
    .zero  0x2
PTR_BG0CNT_080dad90:
    .word  BG0CNT                         @ 080dad90 08000004
DAT_080dad94:
    .word  0x0000fffc                     @ 080dad94 fcff0000
PTR_BG3CNT_080dad98:
    .word  BG3CNT                         @ 080dad98 0e000004
PTR_BLDCNT_080dad9c:
    .word  BLDCNT                         @ 080dad9c 50000004
DAT_080dada0:
    .word  0x00001010                     @ 080dada0 10100000
DAT_080dada4:
    .word  pack_ui_state                  @ 080dada4 50580003

@ Called via step-table dispatch from tick_pack_list_scene_step (0x080dae44), step index 0x13.
@ Per-frame driver for the pack list page overlay animation. Reads gPrng+0x146 (high byte:
@ lsrs r1,r0,#8 + bics r0,r1) to derive tick_overlay_animation_step parameter (0 or 1);
@ if overlay animation completes (returns 1): writes pack_ui_state+0xc[+0x10]:=4 to advance
@ state machine. Unconditionally calls render_pack_card_sprite_by_flip_state(0),
@ render_pack_slot_arrow_oam(0), render_pack_card_highlight_pulse_by_mode(0),
@ render_pack_slot_highlight_oam(1), write_pack_banner_oam_for_all_slots(3).
@ Returns r4 (Sub-case E).
@ 
@ Params: none (r0 loaded internally from PTR_gPrng)
@ Returns: r0=u8 (0=animating, 1=complete; Sub-case E adds r0,r4 @ 080dade8)
@ Side effects:
@   [pack_ui_state+0xc+0x10] := 4 (on overlay-complete path)
@ Constants:
@   pack_ui_state = 0x03005850
@   INPUT_FIELD_HI = 0x146
@   NEXT_STATE = 4
tick_pack_list_overlay_anim:
    push {r4,lr}                             @ 080dada8 10b5
    ldr r0, PTR_gPrng_080dadf0               @ 080dadaa 1148
    movs r1,#0xa3    @ 080dadac a321
    lsls r1,r1,#0x1    @ 080dadae 4900
    adds r0,r0,r1    @ 080dadb0 4018
    ldrh r0,[r0,#0x0]                        @ 080dadb2 0088
    lsrs r1,r0,#0x8    @ 080dadb4 010a
    movs r0,#0x1    @ 080dadb6 0120
    bics r0,r1    @ 080dadb8 8843
    bl tick_overlay_animation_step           @ 080dadba 02f013fc
    adds r4,r0,#0x0    @ 080dadbe 041c
    cmp r4,#0x1                              @ 080dadc0 012c
    bne LAB_080dadca                         @ 080dadc2 02d1
    ldr r1, DAT_080dadf4                     @ 080dadc4 0b49
    movs r0,#0x4    @ 080dadc6 0420
    strh r0,[r1,#0x10]                       @ 080dadc8 0882
LAB_080dadca:
    movs r0,#0x0    @ 080dadca 0020
    bl render_pack_card_sprite_by_flip_state @ 080dadcc f9f76cfc
    movs r0,#0x0    @ 080dadd0 0020
    bl render_pack_slot_arrow_oam            @ 080dadd2 fef7fdfb
    movs r0,#0x0    @ 080dadd6 0020
    bl render_pack_card_highlight_pulse_by_mode @ 080dadd8 fef7b0fa
    movs r0,#0x1    @ 080daddc 0120
    bl render_pack_slot_highlight_oam        @ 080dadde fef737fc
    movs r0,#0x3    @ 080dade2 0320
    bl write_pack_banner_oam_for_all_slots   @ 080dade4 fef76efa
    adds r0,r4,#0x0    @ 080dade8 201c
    pop {r4}                                 @ 080dadea 10bc
    pop {r1}                                 @ 080dadec 02bc
    bx r1                                    @ 080dadee 0847
PTR_gPrng_080dadf0:
    .word  gPrng                          @ 080dadf0 40000003
DAT_080dadf4:
    .word  pack_ui_state                  @ 080dadf4 50580003

@ Called every frame in pack shop page; manages countdown timer for pack entry reveal animation. If pack_ui_state[0x724] bit1 (activated flag) is 0, initializes countdown to 5 and sets bit1; each frame decrements [+0xc+0x6] counter by 1; when it reaches 0, clears bits[1:0] and returns 1 (animation done), otherwise returns 0 (still counting).
@ 
@ Constants:
@ - FLAG_OFFSET=0x724 // pack_ui_state flag byte offset (bit1 = activated)
@ - TIMER_FIELD=0x6 // counter field offset within pack_ui_state+0xc
@ - INIT_COUNT=5 // reveal animation frame countdown init value
@ - BIT_ACTIVE=0x02 // activated flag bit1
@ - BIT_PAIR=0x03 // mask to clear bits[1:0]
tick_pack_entry_reveal_timer:
    push {r4,lr}                             @ 080dadf8 10b5
    ldr r0, DAT_080dae3c                     @ 080dadfa 1048
    adds r2,r0,#0x0    @ 080dadfc 021c
    adds r2,#0xc    @ 080dadfe 0c32
    movs r4,#0x0    @ 080dae00 0024
    ldr r1, DAT_080dae40                     @ 080dae02 0f49
    adds r3,r0,r1    @ 080dae04 4318
    ldrb r1,[r3,#0x0]                        @ 080dae06 1978
    movs r0,#0x2    @ 080dae08 0220
    ands r0,r1    @ 080dae0a 0840
    cmp r0,#0x0                              @ 080dae0c 0028
    bne LAB_080dae1a                         @ 080dae0e 04d1
    movs r0,#0x5    @ 080dae10 0520
    strh r0,[r2,#0x6]                        @ 080dae12 d080
    movs r0,#0x2    @ 080dae14 0220
    orrs r0,r1    @ 080dae16 0843
    strb r0,[r3,#0x0]                        @ 080dae18 1870
LAB_080dae1a:
    ldrh r0,[r2,#0x6]                        @ 080dae1a d088
    subs r0,#0x1    @ 080dae1c 0138
    strh r0,[r2,#0x6]                        @ 080dae1e d080
    lsls r0,r0,#0x10    @ 080dae20 0004
    cmp r0,#0x0                              @ 080dae22 0028
    bgt LAB_080dae32                         @ 080dae24 05dc
    movs r0,#0x3    @ 080dae26 0320
    rsbs r0,r0,#0    @ 080dae28 4042
    ldrb r1,[r3,#0x0]                        @ 080dae2a 1978
    ands r0,r1    @ 080dae2c 0840
    strb r0,[r3,#0x0]                        @ 080dae2e 1870
    movs r4,#0x1    @ 080dae30 0124
LAB_080dae32:
    adds r0,r4,#0x0    @ 080dae32 201c
    pop {r4}                                 @ 080dae34 10bc
    pop {r1}                                 @ 080dae36 02bc
    bx r1                                    @ 080dae38 0847
    .zero  0x2
DAT_080dae3c:
    .word  pack_ui_state                  @ 080dae3c 50580003
DAT_080dae40:
    .word  0x00000724                     @ 080dae40 24070000

@ Pack list page scene frame-step driver. Reads current step from pack_ui_state+0xc[+0x4], looks up handler in fn-ptr table 0x09e494a8, calls via invoke_r0. If handler returns nonzero, increments step counter. Returns 0 while running, 1 when step ends (null ptr). Symmetric to tick_pack_card_select_step (0x080d8504) and tick_pack_duel_puzzle_step (0x080d8d4c). FUN_080db448 case 0.
@ 
@ Constants:
@ - FN_TABLE=0x09e494a8 // pack list page step fn-ptr table
@ - pack_ui_state=0x03005850
tick_pack_list_scene_step:
    push {r4,lr}                             @ 080dae44 10b5
    ldr r0, DAT_080dae6c                     @ 080dae46 0948
    adds r4,r0,#0x0    @ 080dae48 041c
    adds r4,#0xc    @ 080dae4a 0c34
    ldr r1, DAT_080dae70                     @ 080dae4c 0849
    ldrh r2,[r4,#0x4]                        @ 080dae4e a288
    lsls r0,r2,#0x2    @ 080dae50 9000
    adds r0,r0,r1    @ 080dae52 4018
    ldr r0,[r0,#0x0]                         @ 080dae54 0068
    cmp r0,#0x0                              @ 080dae56 0028
    beq LAB_080dae74                         @ 080dae58 0cd0
    bl invoke_r0                             @ 080dae5a 33f0b5fb
    cmp r0,#0x0                              @ 080dae5e 0028
    beq LAB_080dae68                         @ 080dae60 02d0
    ldrh r0,[r4,#0x4]                        @ 080dae62 a088
    adds r0,#0x1    @ 080dae64 0130
    strh r0,[r4,#0x4]                        @ 080dae66 a080
LAB_080dae68:
    movs r0,#0x0    @ 080dae68 0020
    b LAB_080dae76                           @ 080dae6a 04e0
DAT_080dae6c:
    .word  pack_ui_state                  @ 080dae6c 50580003
DAT_080dae70:
    .word  0x09e494a8                     @ 080dae70 a894e409
LAB_080dae74:
    movs r0,#0x1    @ 080dae74 0120
LAB_080dae76:
    pop {r4}                                 @ 080dae76 10bc
    pop {r1}                                 @ 080dae78 02bc
    bx r1                                    @ 080dae7a 0847

@ Returns total card count for the given pack slot ID r0. For r0 in [0x2d..0x32] (45..50) reads from pack_ui_state+0xc internal fields ([+0x26]..[+0x30]); outside this range reads pack_info_table[r0*16+4] standard count. Input r0 is clamped to [0..50]. Used as base data for pack list scroll and OAM layout calculations.
@ 
@ Constants:
@ - PACK_ID_MAX=0x32 // 50: max pack ID (clamp)
@ - CASE_MIN=0x2d // 45: special pack ID lower bound
@ - UI_FIELD_BASE=0x26 // pack_ui_state+0xc first special count field offset
@ - PACK_INFO_CARD_COUNT_OFF=4 // card count field offset in pack_info_table entry
get_pack_total_card_count:
    adds r1,r0,#0x0    @ 080dae7c 011c
    ldr r0, DAT_080dae9c                     @ 080dae7e 0748
    adds r2,r0,#0x0    @ 080dae80 021c
    adds r2,#0xc    @ 080dae82 0c32
    cmp r1,#0x32                             @ 080dae84 3229
    bls LAB_080dae8a                         @ 080dae86 00d9
    movs r1,#0x32    @ 080dae88 3221
LAB_080dae8a:
    adds r0,r1,#0x0    @ 080dae8a 081c
    subs r0,#0x2d    @ 080dae8c 2d38
    cmp r0,#0x5                              @ 080dae8e 0528
    bhi switchD_080dae9a__default            @ 080dae90 14d8
    lsls r0,r0,#0x2    @ 080dae92 8000
    ldr r1, DAT_080daea0                     @ 080dae94 0249
    adds r0,r0,r1    @ 080dae96 4018
    ldr r0,[r0,#0x0]                         @ 080dae98 0068
switchD_080dae9a__switchD:
    .hword 0x4687    @ 080dae9a 8746
DAT_080dae9c:
    .word  pack_ui_state                  @ 080dae9c 50580003
DAT_080daea0:
    .word  0x080daea4                     @ 080daea0 a4ae0d08
switchD_080dae9a__switchdataD_080daea4:
    .word  0x080daecc                     @ 080daea4 ccae0d08
    .word  0x080daed0                     @ 080daea8 d0ae0d08
    .word  0x080daed4                     @ 080daeac d4ae0d08
    .word  0x080daed8                     @ 080daeb0 d8ae0d08
    .word  0x080daedc                     @ 080daeb4 dcae0d08
PTR_caseD_32_080daeb8:
    .word  0x080daee0                     @ 080daeb8 e0ae0d08
switchD_080dae9a__default:
    ldr r0, PTR_pack_info_table_080daec8     @ 080daebc 0248
    lsls r1,r1,#0x4    @ 080daebe 0901
    adds r1,r1,r0    @ 080daec0 0918
    ldrh r0,[r1,#0x4]                        @ 080daec2 8888
    b LAB_080daee2                           @ 080daec4 0de0
    .zero  0x2
PTR_pack_info_table_080daec8:
    .word  pack_info_table                @ 080daec8 e8e2e509
switchD_080dae9a__caseD_2d:
    ldrh r0,[r2,#0x26]                       @ 080daecc d08c
    b LAB_080daee2                           @ 080daece 08e0
switchD_080dae9a__caseD_2e:
    ldrh r0,[r2,#0x28]                       @ 080daed0 108d
    b LAB_080daee2                           @ 080daed2 06e0
switchD_080dae9a__caseD_2f:
    ldrh r0,[r2,#0x2a]                       @ 080daed4 508d
    b LAB_080daee2                           @ 080daed6 04e0
switchD_080dae9a__caseD_30:
    ldrh r0,[r2,#0x2c]                       @ 080daed8 908d
    b LAB_080daee2                           @ 080daeda 02e0
switchD_080dae9a__caseD_31:
    ldrh r0,[r2,#0x2e]                       @ 080daedc d08d
    b LAB_080daee2                           @ 080daede 00e0
switchD_080dae9a__caseD_32:
    ldrh r0,[r2,#0x30]                       @ 080daee0 108e
LAB_080daee2:
    bx lr                                    @ 080daee2 7047

@ Given pack ID r1 and card internal ID r0 (icid), checks if the card matches the filter type for pack_ui_state filter r1. Dispatches via switch(r1-0x2d): case 0x2d/0x2e checks card_stats_table[icid] attribute field for 0 or 1 (attribute filter); case 0x2f checks card type enum (==3 returns 1); case 0x30/0x31 checks race field (==0x17 or 0x16 returns 1); case 0x32 unconditionally returns 1. Default returns 0. Used by callers iterating pack cards to count matching cards.
@ 
@ Constants:
@ - FILTER_BASE=0x2d // 45: minimum filter pack_id
@ - ATTR_DARK=0 // case 0x2d: card attribute == 0 (DARK)
@ - ATTR_LIGHT=1 // case 0x2e: card attribute == 1 (LIGHT)
@ - TYPE_RITUAL=3 // case 0x2f: card type == 3 (Ritual)
@ - RACE_AQUA=0x17 // case 0x30: card race == 0x17 (Aqua, =23)
@ - RACE_WARRIOR=0x16 // case 0x31: card race == 0x16 (Warrior, =22)
@ - CARD_STATS_STRIDE=0xb // card_stats_table entry stride (11 halfwords)
check_pack_card_slot_filter:
    push {r4,lr}                             @ 080daee4 10b5
    adds r3,r0,#0x0    @ 080daee6 031c
    adds r0,r1,#0x0    @ 080daee8 081c
    subs r0,#0x2d    @ 080daeea 2d38
    cmp r0,#0x5                              @ 080daeec 0528
    bhi switchD_080daef8__default            @ 080daeee 13d8
    lsls r0,r0,#0x2    @ 080daef0 8000
    ldr r1, DAT_080daefc                     @ 080daef2 0249
    adds r0,r0,r1    @ 080daef4 4018
    ldr r0,[r0,#0x0]                         @ 080daef6 0068
switchD_080daef8__switchD:
    .hword 0x4687    @ 080daef8 8746
    .zero  0x2
DAT_080daefc:
    .word  0x080daf00                     @ 080daefc 00af0d08
switchD_080daef8__switchdataD_080daf00:
    .word  0x080daf1c                     @ 080daf00 1caf0d08
    .word  0x080daf38                     @ 080daf04 38af0d08
    .word  0x080daf54                     @ 080daf08 54af0d08
    .word  0x080daf80                     @ 080daf0c 80af0d08
    .word  0x080daf9c                     @ 080daf10 9caf0d08
    .word  0x080dafbc                     @ 080daf14 bcaf0d08
switchD_080daef8__default:
    movs r0,#0x0    @ 080daf18 0020
    b LAB_080dafbe                           @ 080daf1a 50e0
switchD_080daef8__caseD_2d:
    movs r2,#0x0    @ 080daf1c 0022
    ldr r1, PTR_card_stats_table_080daf34    @ 080daf1e 0549
    movs r0,#0xb    @ 080daf20 0b20
    muls r0,r3    @ 080daf22 5843
    adds r0,#0x8    @ 080daf24 0830
    lsls r0,r0,#0x1    @ 080daf26 4000
    adds r0,r0,r1    @ 080daf28 4018
    ldrh r0,[r0,#0x0]                        @ 080daf2a 0088
    cmp r0,#0x0                              @ 080daf2c 0028
    bne LAB_080dafb2                         @ 080daf2e 40d1
    b LAB_080dafb0                           @ 080daf30 3ee0
    .zero  0x2
PTR_card_stats_table_080daf34:
    .word  card_stats_table               @ 080daf34 b8698109
switchD_080daef8__caseD_2e:
    movs r2,#0x0    @ 080daf38 0022
    ldr r1, PTR_card_stats_table_080daf50    @ 080daf3a 0549
    movs r0,#0xb    @ 080daf3c 0b20
    muls r0,r3    @ 080daf3e 5843
    adds r0,#0x8    @ 080daf40 0830
    lsls r0,r0,#0x1    @ 080daf42 4000
    adds r0,r0,r1    @ 080daf44 4018
    ldrh r0,[r0,#0x0]                        @ 080daf46 0088
    cmp r0,#0x1                              @ 080daf48 0128
    bne LAB_080dafb2                         @ 080daf4a 32d1
    b LAB_080dafb0                           @ 080daf4c 30e0
    .zero  0x2
PTR_card_stats_table_080daf50:
    .word  card_stats_table               @ 080daf50 b8698109
switchD_080daef8__caseD_2f:
    movs r4,#0x0    @ 080daf54 0024
    ldr r2, DAT_080daf78                     @ 080daf56 084a
    ldr r1, PTR_card_stats_table_080daf7c    @ 080daf58 0849
    movs r0,#0xb    @ 080daf5a 0b20
    muls r0,r3    @ 080daf5c 5843
    adds r0,#0x8    @ 080daf5e 0830
    lsls r0,r0,#0x1    @ 080daf60 4000
    adds r0,r0,r1    @ 080daf62 4018
    ldrh r0,[r0,#0x0]                        @ 080daf64 0088
    lsls r0,r0,#0x2    @ 080daf66 8000
    adds r0,r0,r2    @ 080daf68 8018
    ldr r0,[r0,#0x0]                         @ 080daf6a 0068
    cmp r0,#0x3                              @ 080daf6c 0328
    bne LAB_080daf72                         @ 080daf6e 00d1
    movs r4,#0x1    @ 080daf70 0124
LAB_080daf72:
    adds r0,r4,#0x0    @ 080daf72 201c
    b LAB_080dafbe                           @ 080daf74 23e0
    .zero  0x2
DAT_080daf78:
    .word  0x09e4f1c4                     @ 080daf78 c4f1e409
PTR_card_stats_table_080daf7c:
    .word  card_stats_table               @ 080daf7c b8698109
switchD_080daef8__caseD_30:
    movs r2,#0x0    @ 080daf80 0022
    ldr r1, PTR_card_stats_table_080daf98    @ 080daf82 0549
    movs r0,#0xb    @ 080daf84 0b20
    muls r0,r3    @ 080daf86 5843
    adds r0,#0x6    @ 080daf88 0630
    lsls r0,r0,#0x1    @ 080daf8a 4000
    adds r0,r0,r1    @ 080daf8c 4018
    ldrh r0,[r0,#0x0]                        @ 080daf8e 0088
    cmp r0,#0x17                             @ 080daf90 1728
    bne LAB_080dafb2                         @ 080daf92 0ed1
    b LAB_080dafb0                           @ 080daf94 0ce0
    .zero  0x2
PTR_card_stats_table_080daf98:
    .word  card_stats_table               @ 080daf98 b8698109
switchD_080daef8__caseD_31:
    movs r2,#0x0    @ 080daf9c 0022
    ldr r1, PTR_card_stats_table_080dafb8    @ 080daf9e 0649
    movs r0,#0xb    @ 080dafa0 0b20
    muls r0,r3    @ 080dafa2 5843
    adds r0,#0x6    @ 080dafa4 0630
    lsls r0,r0,#0x1    @ 080dafa6 4000
    adds r0,r0,r1    @ 080dafa8 4018
    ldrh r0,[r0,#0x0]                        @ 080dafaa 0088
    cmp r0,#0x16                             @ 080dafac 1628
    bne LAB_080dafb2                         @ 080dafae 00d1
LAB_080dafb0:
    movs r2,#0x1    @ 080dafb0 0122
LAB_080dafb2:
    adds r0,r2,#0x0    @ 080dafb2 101c
    b LAB_080dafbe                           @ 080dafb4 03e0
    .zero  0x2
PTR_card_stats_table_080dafb8:
    .word  card_stats_table               @ 080dafb8 b8698109
switchD_080daef8__caseD_32:
    movs r0,#0x1    @ 080dafbc 0120
LAB_080dafbe:
    pop {r4}                                 @ 080dafbe 10bc
    pop {r1}                                 @ 080dafc0 02bc
    bx r1                                    @ 080dafc2 0847

@ Reads challenge clear stats from EWRAM [0x02000000+0x6e34..0x6eb8], takes pairwise max, aggregates into output struct. Calls get_total_challenge_cleared_count for total, then writes 5 halfword stat fields (+0,+2,+4,+6,+8) into r5 output struct. Called by pack_080db4f4 when presenting clear stat summary. Side effects limited to output struct writes; EWRAM source fields unchanged.
@ 
@ Constants:
@ CHALLENGE_STATS_BASE = 0x02000000+0x6e34
@ CHALLENGE_STATS_END  = 0x02000000+0x6eb8
@ 
@ Params: r0=challenge_stats_out* out_ptr
@ Return: r0=u16 max_stat_value (Sub-case E passthrough; last max value, written to [r5+0xe] before exit)
aggregate_challenge_clear_stats:
    push {r4,r5,lr}                          @ 080dafc4 30b5
    adds r5,r0,#0x0    @ 080dafc6 051c
    ldr r4, DAT_080db158                     @ 080dafc8 634c
    ldr r1, DAT_080db15c                     @ 080dafca 6449
    adds r0,r4,r1    @ 080dafcc 6018
    ldrh r0,[r0,#0x0]                        @ 080dafce 0088
    str r0,[r5,#0x0]                         @ 080dafd0 2860
    bl get_total_challenge_cleared_count     @ 080dafd2 49f767fc
    strh r0,[r5,#0x4]                        @ 080dafd6 a880
    ldr r2, DAT_080db160                     @ 080dafd8 614a
    adds r0,r4,r2    @ 080dafda a018
    ldrh r0,[r0,#0x0]                        @ 080dafdc 0088
    lsls r0,r0,#0x14    @ 080dafde 0005
    lsrs r1,r0,#0x14    @ 080dafe0 010d
    adds r2,#0x4    @ 080dafe2 0432
    adds r0,r4,r2    @ 080dafe4 a018
    ldrh r0,[r0,#0x0]                        @ 080dafe6 0088
    lsls r0,r0,#0x14    @ 080dafe8 0005
    lsrs r0,r0,#0x14    @ 080dafea 000d
    cmp r0,r1                                @ 080dafec 8842
    bls LAB_080daff2                         @ 080dafee 00d9
    adds r0,r1,#0x0    @ 080daff0 081c
LAB_080daff2:
    adds r1,r0,#0x0    @ 080daff2 011c
    ldr r2, DAT_080db164                     @ 080daff4 5b4a
    adds r0,r4,r2    @ 080daff6 a018
    ldrh r0,[r0,#0x0]                        @ 080daff8 0088
    lsls r0,r0,#0x14    @ 080daffa 0005
    lsrs r0,r0,#0x14    @ 080daffc 000d
    cmp r0,r1                                @ 080daffe 8842
    bls LAB_080db004                         @ 080db000 00d9
    adds r0,r1,#0x0    @ 080db002 081c
LAB_080db004:
    adds r1,r0,#0x0    @ 080db004 011c
    ldr r2, DAT_080db168                     @ 080db006 584a
    adds r0,r4,r2    @ 080db008 a018
    ldrh r0,[r0,#0x0]                        @ 080db00a 0088
    lsls r0,r0,#0x14    @ 080db00c 0005
    lsrs r0,r0,#0x14    @ 080db00e 000d
    cmp r0,r1                                @ 080db010 8842
    bls LAB_080db016                         @ 080db012 00d9
    adds r0,r1,#0x0    @ 080db014 081c
LAB_080db016:
    adds r1,r0,#0x0    @ 080db016 011c
    ldr r2, DAT_080db16c                     @ 080db018 544a
    adds r0,r4,r2    @ 080db01a a018
    ldrh r0,[r0,#0x0]                        @ 080db01c 0088
    lsls r0,r0,#0x14    @ 080db01e 0005
    lsrs r0,r0,#0x14    @ 080db020 000d
    cmp r0,r1                                @ 080db022 8842
    bls LAB_080db028                         @ 080db024 00d9
    adds r0,r1,#0x0    @ 080db026 081c
LAB_080db028:
    strh r0,[r5,#0x6]                        @ 080db028 e880
    ldr r1, DAT_080db170                     @ 080db02a 5149
    adds r0,r4,r1    @ 080db02c 6018
    ldrh r0,[r0,#0x0]                        @ 080db02e 0088
    lsls r0,r0,#0x14    @ 080db030 0005
    lsrs r1,r0,#0x14    @ 080db032 010d
    ldr r2, DAT_080db174                     @ 080db034 4f4a
    adds r0,r4,r2    @ 080db036 a018
    ldrh r0,[r0,#0x0]                        @ 080db038 0088
    lsls r0,r0,#0x14    @ 080db03a 0005
    lsrs r0,r0,#0x14    @ 080db03c 000d
    cmp r0,r1                                @ 080db03e 8842
    bls LAB_080db044                         @ 080db040 00d9
    adds r0,r1,#0x0    @ 080db042 081c
LAB_080db044:
    adds r1,r0,#0x0    @ 080db044 011c
    ldr r2, DAT_080db178                     @ 080db046 4c4a
    adds r0,r4,r2    @ 080db048 a018
    ldrh r0,[r0,#0x0]                        @ 080db04a 0088
    lsls r0,r0,#0x14    @ 080db04c 0005
    lsrs r0,r0,#0x14    @ 080db04e 000d
    cmp r0,r1                                @ 080db050 8842
    bls LAB_080db056                         @ 080db052 00d9
    adds r0,r1,#0x0    @ 080db054 081c
LAB_080db056:
    adds r1,r0,#0x0    @ 080db056 011c
    movs r2,#0xdd    @ 080db058 dd22
    lsls r2,r2,#0x7    @ 080db05a d201
    adds r0,r4,r2    @ 080db05c a018
    ldrh r0,[r0,#0x0]                        @ 080db05e 0088
    lsls r0,r0,#0x14    @ 080db060 0005
    lsrs r0,r0,#0x14    @ 080db062 000d
    cmp r0,r1                                @ 080db064 8842
    bls LAB_080db06a                         @ 080db066 00d9
    adds r0,r1,#0x0    @ 080db068 081c
LAB_080db06a:
    adds r1,r0,#0x0    @ 080db06a 011c
    ldr r2, DAT_080db17c                     @ 080db06c 434a
    adds r0,r4,r2    @ 080db06e a018
    ldrh r0,[r0,#0x0]                        @ 080db070 0088
    lsls r0,r0,#0x14    @ 080db072 0005
    lsrs r0,r0,#0x14    @ 080db074 000d
    cmp r0,r1                                @ 080db076 8842
    bls LAB_080db07c                         @ 080db078 00d9
    adds r0,r1,#0x0    @ 080db07a 081c
LAB_080db07c:
    strh r0,[r5,#0x8]                        @ 080db07c 2881
    ldr r1, DAT_080db180                     @ 080db07e 4049
    adds r0,r4,r1    @ 080db080 6018
    ldrh r0,[r0,#0x0]                        @ 080db082 0088
    lsls r0,r0,#0x14    @ 080db084 0005
    lsrs r1,r0,#0x14    @ 080db086 010d
    ldr r2, DAT_080db184                     @ 080db088 3e4a
    adds r0,r4,r2    @ 080db08a a018
    ldrh r0,[r0,#0x0]                        @ 080db08c 0088
    lsls r0,r0,#0x14    @ 080db08e 0005
    lsrs r0,r0,#0x14    @ 080db090 000d
    cmp r0,r1                                @ 080db092 8842
    bls LAB_080db098                         @ 080db094 00d9
    adds r0,r1,#0x0    @ 080db096 081c
LAB_080db098:
    adds r1,r0,#0x0    @ 080db098 011c
    ldr r2, DAT_080db188                     @ 080db09a 3b4a
    adds r0,r4,r2    @ 080db09c a018
    ldrh r0,[r0,#0x0]                        @ 080db09e 0088
    lsls r0,r0,#0x14    @ 080db0a0 0005
    lsrs r0,r0,#0x14    @ 080db0a2 000d
    cmp r0,r1                                @ 080db0a4 8842
    bls LAB_080db0aa                         @ 080db0a6 00d9
    adds r0,r1,#0x0    @ 080db0a8 081c
LAB_080db0aa:
    adds r1,r0,#0x0    @ 080db0aa 011c
    ldr r2, DAT_080db18c                     @ 080db0ac 374a
    adds r0,r4,r2    @ 080db0ae a018
    ldrh r0,[r0,#0x0]                        @ 080db0b0 0088
    lsls r0,r0,#0x14    @ 080db0b2 0005
    lsrs r0,r0,#0x14    @ 080db0b4 000d
    cmp r0,r1                                @ 080db0b6 8842
    bls LAB_080db0bc                         @ 080db0b8 00d9
    adds r0,r1,#0x0    @ 080db0ba 081c
LAB_080db0bc:
    adds r1,r0,#0x0    @ 080db0bc 011c
    ldr r2, DAT_080db190                     @ 080db0be 344a
    adds r0,r4,r2    @ 080db0c0 a018
    ldrh r0,[r0,#0x0]                        @ 080db0c2 0088
    lsls r0,r0,#0x14    @ 080db0c4 0005
    lsrs r0,r0,#0x14    @ 080db0c6 000d
    cmp r0,r1                                @ 080db0c8 8842
    bls LAB_080db0ce                         @ 080db0ca 00d9
    adds r0,r1,#0x0    @ 080db0cc 081c
LAB_080db0ce:
    strh r0,[r5,#0xa]                        @ 080db0ce 6881
    ldr r1, DAT_080db194                     @ 080db0d0 3049
    adds r0,r4,r1    @ 080db0d2 6018
    ldrh r0,[r0,#0x0]                        @ 080db0d4 0088
    lsls r0,r0,#0x14    @ 080db0d6 0005
    lsrs r1,r0,#0x14    @ 080db0d8 010d
    ldr r2, DAT_080db198                     @ 080db0da 2f4a
    adds r0,r4,r2    @ 080db0dc a018
    ldrh r0,[r0,#0x0]                        @ 080db0de 0088
    lsls r0,r0,#0x14    @ 080db0e0 0005
    lsrs r0,r0,#0x14    @ 080db0e2 000d
    cmp r0,r1                                @ 080db0e4 8842
    bls LAB_080db0ea                         @ 080db0e6 00d9
    adds r0,r1,#0x0    @ 080db0e8 081c
LAB_080db0ea:
    adds r1,r0,#0x0    @ 080db0ea 011c
    ldr r2, DAT_080db19c                     @ 080db0ec 2b4a
    adds r0,r4,r2    @ 080db0ee a018
    ldrh r0,[r0,#0x0]                        @ 080db0f0 0088
    lsls r0,r0,#0x14    @ 080db0f2 0005
    lsrs r0,r0,#0x14    @ 080db0f4 000d
    cmp r0,r1                                @ 080db0f6 8842
    bls LAB_080db0fc                         @ 080db0f8 00d9
    adds r0,r1,#0x0    @ 080db0fa 081c
LAB_080db0fc:
    adds r1,r0,#0x0    @ 080db0fc 011c
    ldr r2, DAT_080db1a0                     @ 080db0fe 284a
    adds r0,r4,r2    @ 080db100 a018
    ldrh r0,[r0,#0x0]                        @ 080db102 0088
    lsls r0,r0,#0x14    @ 080db104 0005
    lsrs r0,r0,#0x14    @ 080db106 000d
    cmp r0,r1                                @ 080db108 8842
    bls LAB_080db10e                         @ 080db10a 00d9
    adds r0,r1,#0x0    @ 080db10c 081c
LAB_080db10e:
    adds r1,r0,#0x0    @ 080db10e 011c
    ldr r2, DAT_080db1a4                     @ 080db110 244a
    adds r0,r4,r2    @ 080db112 a018
    ldrh r0,[r0,#0x0]                        @ 080db114 0088
    lsls r0,r0,#0x14    @ 080db116 0005
    lsrs r0,r0,#0x14    @ 080db118 000d
    cmp r0,r1                                @ 080db11a 8842
    bls LAB_080db120                         @ 080db11c 00d9
    adds r0,r1,#0x0    @ 080db11e 081c
LAB_080db120:
    strh r0,[r5,#0xc]                        @ 080db120 a881
    ldr r1, DAT_080db1a8                     @ 080db122 2149
    adds r0,r4,r1    @ 080db124 6018
    ldrh r0,[r0,#0x0]                        @ 080db126 0088
    lsls r0,r0,#0x14    @ 080db128 0005
    lsrs r1,r0,#0x14    @ 080db12a 010d
    ldr r2, DAT_080db1ac                     @ 080db12c 1f4a
    adds r0,r4,r2    @ 080db12e a018
    ldrh r0,[r0,#0x0]                        @ 080db130 0088
    lsls r0,r0,#0x14    @ 080db132 0005
    lsrs r0,r0,#0x14    @ 080db134 000d
    cmp r0,r1                                @ 080db136 8842
    bls LAB_080db13c                         @ 080db138 00d9
    adds r0,r1,#0x0    @ 080db13a 081c
LAB_080db13c:
    adds r1,r0,#0x0    @ 080db13c 011c
    ldr r2, DAT_080db1b0                     @ 080db13e 1c4a
    adds r0,r4,r2    @ 080db140 a018
    ldrh r0,[r0,#0x0]                        @ 080db142 0088
    lsls r0,r0,#0x14    @ 080db144 0005
    lsrs r0,r0,#0x14    @ 080db146 000d
    cmp r0,r1                                @ 080db148 8842
    bls LAB_080db14e                         @ 080db14a 00d9
    adds r0,r1,#0x0    @ 080db14c 081c
LAB_080db14e:
    strh r0,[r5,#0xe]                        @ 080db14e e881
    pop {r4,r5}                              @ 080db150 30bc
    pop {r0}                                 @ 080db152 01bc
    bx r0                                    @ 080db154 0047
    .zero  0x2
DAT_080db158:
    .word  0x02000000                     @ 080db158 00000002
DAT_080db15c:
    .word  0x00006e34                     @ 080db15c 346e0000
DAT_080db160:
    .word  0x00006e60                     @ 080db160 606e0000
DAT_080db164:
    .word  0x00006e68                     @ 080db164 686e0000
DAT_080db168:
    .word  0x00006e6c                     @ 080db168 6c6e0000
DAT_080db16c:
    .word  0x00006e70                     @ 080db16c 706e0000
DAT_080db170:
    .word  0x00006e74                     @ 080db170 746e0000
DAT_080db174:
    .word  0x00006e78                     @ 080db174 786e0000
DAT_080db178:
    .word  0x00006e7c                     @ 080db178 7c6e0000
DAT_080db17c:
    .word  0x00006e84                     @ 080db17c 846e0000
DAT_080db180:
    .word  0x00006e88                     @ 080db180 886e0000
DAT_080db184:
    .word  0x00006e8c                     @ 080db184 8c6e0000
DAT_080db188:
    .word  0x00006e90                     @ 080db188 906e0000
DAT_080db18c:
    .word  0x00006e94                     @ 080db18c 946e0000
DAT_080db190:
    .word  0x00006e98                     @ 080db190 986e0000
DAT_080db194:
    .word  0x00006e9c                     @ 080db194 9c6e0000
DAT_080db198:
    .word  0x00006ea0                     @ 080db198 a06e0000
DAT_080db19c:
    .word  0x00006ea4                     @ 080db19c a46e0000
DAT_080db1a0:
    .word  0x00006ea8                     @ 080db1a0 a86e0000
DAT_080db1a4:
    .word  0x00006eac                     @ 080db1a4 ac6e0000
DAT_080db1a8:
    .word  0x00006eb0                     @ 080db1a8 b06e0000
DAT_080db1ac:
    .word  0x00006eb4                     @ 080db1ac b46e0000
DAT_080db1b0:
    .word  0x00006eb8                     @ 080db1b0 b86e0000

@ Checks whether the player meets the purchase prerequisites for a given pack slot. r0=pack_id [0..50], r1=ptr to player stats struct. Uses a switch table (0x50 entries at 0x080db1d0) indexed by pack_id: early packs (case 0..0xa) are always purchasable (r4=1); specific packs check player stats fields (win count, card count, etc.) against thresholds. Finally calls test_card_flag_bit__080f9a60 for card-flag check. Returns 1 if eligible, 0 otherwise.
@ 
@ Constants:
@ - PACK_ID_MAX=0x32 // maximum valid pack ID (50)
@ - THRESHOLD_B=0x2 // case_b: player_stats[+6] > 2
@ - THRESHOLD_C=0 // case_c: player_stats[+8] > 0
check_pack_slot_purchase_eligible:
    push {r4,lr}                             @ 080db1b4 10b5
    adds r3,r0,#0x0    @ 080db1b6 031c
    adds r2,r1,#0x0    @ 080db1b8 0a1c
    movs r4,#0x0    @ 080db1ba 0024
    cmp r3,#0x32                             @ 080db1bc 322b
    bls LAB_080db1c2                         @ 080db1be 00d9
    b switchD_080db1ca__default              @ 080db1c0 c8e0
LAB_080db1c2:
    lsls r0,r3,#0x2    @ 080db1c2 9800
    ldr r1, DAT_080db1cc                     @ 080db1c4 0149
    adds r0,r0,r1    @ 080db1c6 4018
    ldr r0,[r0,#0x0]                         @ 080db1c8 0068
switchD_080db1ca__switchD:
    .hword 0x4687    @ 080db1ca 8746
DAT_080db1cc:
    .word  0x080db1d0                     @ 080db1cc d0b10d08
switchD_080db1ca__switchdataD_080db1d0:
    .word  0x080db352                     @ 080db1d0 52b30d08
    .word  0x080db352                     @ 080db1d4 52b30d08
    .word  0x080db352                     @ 080db1d8 52b30d08
    .word  0x080db352                     @ 080db1dc 52b30d08
    .word  0x080db352                     @ 080db1e0 52b30d08
    .word  0x080db352                     @ 080db1e4 52b30d08
    .word  0x080db352                     @ 080db1e8 52b30d08
    .word  0x080db352                     @ 080db1ec 52b30d08
    .word  0x080db352                     @ 080db1f0 52b30d08
    .word  0x080db352                     @ 080db1f4 52b30d08
    .word  0x080db352                     @ 080db1f8 52b30d08
    .word  0x080db29c                     @ 080db1fc 9cb20d08
    .word  0x080db2a4                     @ 080db200 a4b20d08
    .word  0x080db2ac                     @ 080db204 acb20d08
    .word  0x080db2b4                     @ 080db208 b4b20d08
    .word  0x080db2bc                     @ 080db20c bcb20d08
    .word  0x080db2c4                     @ 080db210 c4b20d08
    .word  0x080db2cc                     @ 080db214 ccb20d08
    .word  0x080db2d4                     @ 080db218 d4b20d08
    .word  0x080db2dc                     @ 080db21c dcb20d08
    .word  0x080db2e4                     @ 080db220 e4b20d08
    .word  0x080db2e4                     @ 080db224 e4b20d08
    .word  0x080db2a4                     @ 080db228 a4b20d08
    .word  0x080db2ec                     @ 080db22c ecb20d08
    .word  0x080db29c                     @ 080db230 9cb20d08
    .word  0x080db2f4                     @ 080db234 f4b20d08
    .word  0x080db29c                     @ 080db238 9cb20d08
    .word  0x080db2f4                     @ 080db23c f4b20d08
    .word  0x080db2a4                     @ 080db240 a4b20d08
    .word  0x080db2ec                     @ 080db244 ecb20d08
    .word  0x080db2ec                     @ 080db248 ecb20d08
    .word  0x080db29c                     @ 080db24c 9cb20d08
    .word  0x080db2f4                     @ 080db250 f4b20d08
    .word  0x080db2fc                     @ 080db254 fcb20d08
    .word  0x080db304                     @ 080db258 04b30d08
    .word  0x080db29c                     @ 080db25c 9cb20d08
    .word  0x080db2cc                     @ 080db260 ccb20d08
    .word  0x080db30c                     @ 080db264 0cb30d08
    .word  0x080db314                     @ 080db268 14b30d08
    .word  0x080db314                     @ 080db26c 14b30d08
    .word  0x080db31c                     @ 080db270 1cb30d08
    .word  0x080db2dc                     @ 080db274 dcb20d08
    .word  0x080db31c                     @ 080db278 1cb30d08
    .word  0x080db2d4                     @ 080db27c d4b20d08
    .word  0x080db324                     @ 080db280 24b30d08
    .word  0x080db32c                     @ 080db284 2cb30d08
    .word  0x080db334                     @ 080db288 34b30d08
    .word  0x080db334                     @ 080db28c 34b30d08
    .word  0x080db33c                     @ 080db290 3cb30d08
    .word  0x080db344                     @ 080db294 44b30d08
    .word  0x080db34c                     @ 080db298 4cb30d08
switchD_080db1ca__caseD_b:
    ldrh r2,[r2,#0x6]                        @ 080db29c d288
    cmp r2,#0x2                              @ 080db29e 022a
    bls switchD_080db1ca__default            @ 080db2a0 58d9
    b switchD_080db1ca__caseD_0              @ 080db2a2 56e0
switchD_080db1ca__caseD_c:
    ldrh r0,[r2,#0x8]                        @ 080db2a4 1089
    cmp r0,#0x0                              @ 080db2a6 0028
    beq switchD_080db1ca__default            @ 080db2a8 54d0
    b switchD_080db1ca__caseD_0              @ 080db2aa 52e0
switchD_080db1ca__caseD_d:
    ldrh r0,[r2,#0xa]                        @ 080db2ac 5089
    cmp r0,#0x0                              @ 080db2ae 0028
    beq switchD_080db1ca__default            @ 080db2b0 50d0
    b switchD_080db1ca__caseD_0              @ 080db2b2 4ee0
switchD_080db1ca__caseD_e:
    ldrh r2,[r2,#0xa]                        @ 080db2b4 5289
    cmp r2,#0x2                              @ 080db2b6 022a
    bls switchD_080db1ca__default            @ 080db2b8 4cd9
    b switchD_080db1ca__caseD_0              @ 080db2ba 4ae0
switchD_080db1ca__caseD_f:
    ldrh r0,[r2,#0xc]                        @ 080db2bc 9089
    cmp r0,#0x0                              @ 080db2be 0028
    beq switchD_080db1ca__default            @ 080db2c0 48d0
    b switchD_080db1ca__caseD_0              @ 080db2c2 46e0
switchD_080db1ca__caseD_10:
    ldrh r2,[r2,#0xc]                        @ 080db2c4 9289
    cmp r2,#0x2                              @ 080db2c6 022a
    bls switchD_080db1ca__default            @ 080db2c8 44d9
    b switchD_080db1ca__caseD_0              @ 080db2ca 42e0
switchD_080db1ca__caseD_11:
    ldrh r2,[r2,#0xc]                        @ 080db2cc 9289
    cmp r2,#0x4                              @ 080db2ce 042a
    bls switchD_080db1ca__default            @ 080db2d0 40d9
    b switchD_080db1ca__caseD_0              @ 080db2d2 3ee0
switchD_080db1ca__caseD_12:
    ldr r0,[r2,#0x0]                         @ 080db2d4 1068
    cmp r0,#0xe                              @ 080db2d6 0e28
    bls switchD_080db1ca__default            @ 080db2d8 3cd9
    b switchD_080db1ca__caseD_0              @ 080db2da 3ae0
switchD_080db1ca__caseD_13:
    ldr r0,[r2,#0x0]                         @ 080db2dc 1068
    cmp r0,#0x13                             @ 080db2de 1328
    bls switchD_080db1ca__default            @ 080db2e0 38d9
    b switchD_080db1ca__caseD_0              @ 080db2e2 36e0
switchD_080db1ca__caseD_14:
    ldrh r2,[r2,#0x4]                        @ 080db2e4 9288
    cmp r2,#0x3b                             @ 080db2e6 3b2a
    bls switchD_080db1ca__default            @ 080db2e8 34d9
    b switchD_080db1ca__caseD_0              @ 080db2ea 32e0
switchD_080db1ca__caseD_17:
    ldrh r2,[r2,#0x4]                        @ 080db2ec 9288
    cmp r2,#0x40                             @ 080db2ee 402a
    bls switchD_080db1ca__default            @ 080db2f0 30d9
    b switchD_080db1ca__caseD_0              @ 080db2f2 2ee0
switchD_080db1ca__caseD_19:
    ldrh r2,[r2,#0x4]                        @ 080db2f4 9288
    cmp r2,#0x36                             @ 080db2f6 362a
    bls switchD_080db1ca__default            @ 080db2f8 2cd9
    b switchD_080db1ca__caseD_0              @ 080db2fa 2ae0
switchD_080db1ca__caseD_21:
    ldrh r2,[r2,#0x4]                        @ 080db2fc 9288
    cmp r2,#0x1d                             @ 080db2fe 1d2a
    bls switchD_080db1ca__default            @ 080db300 28d9
    b switchD_080db1ca__caseD_0              @ 080db302 26e0
switchD_080db1ca__caseD_22:
    ldrh r2,[r2,#0x4]                        @ 080db304 9288
    cmp r2,#0x13                             @ 080db306 132a
    bls switchD_080db1ca__default            @ 080db308 24d9
    b switchD_080db1ca__caseD_0              @ 080db30a 22e0
switchD_080db1ca__caseD_25:
    ldrh r2,[r2,#0x4]                        @ 080db30c 9288
    cmp r2,#0x54                             @ 080db30e 542a
    bls switchD_080db1ca__default            @ 080db310 20d9
    b switchD_080db1ca__caseD_0              @ 080db312 1ee0
switchD_080db1ca__caseD_26:
    ldr r0,[r2,#0x0]                         @ 080db314 1068
    cmp r0,#0x7                              @ 080db316 0728
    bls switchD_080db1ca__default            @ 080db318 1cd9
    b switchD_080db1ca__caseD_0              @ 080db31a 1ae0
switchD_080db1ca__caseD_28:
    ldr r0,[r2,#0x0]                         @ 080db31c 1068
    cmp r0,#0xb                              @ 080db31e 0b28
    bls switchD_080db1ca__default            @ 080db320 18d9
    b switchD_080db1ca__caseD_0              @ 080db322 16e0
switchD_080db1ca__caseD_2c:
    ldrh r2,[r2,#0x4]                        @ 080db324 9288
    cmp r2,#0x4a                             @ 080db326 4a2a
    bls switchD_080db1ca__default            @ 080db328 14d9
    b switchD_080db1ca__caseD_0              @ 080db32a 12e0
switchD_080db1ca__caseD_2d:
    ldrh r2,[r2,#0x4]                        @ 080db32c 9288
    cmp r2,#0x9                              @ 080db32e 092a
    bls switchD_080db1ca__default            @ 080db330 10d9
    b switchD_080db1ca__caseD_0              @ 080db332 0ee0
switchD_080db1ca__caseD_2e:
    ldrh r2,[r2,#0x4]                        @ 080db334 9288
    cmp r2,#0x45                             @ 080db336 452a
    bls switchD_080db1ca__default            @ 080db338 0cd9
    b switchD_080db1ca__caseD_0              @ 080db33a 0ae0
switchD_080db1ca__caseD_30:
    ldrh r2,[r2,#0x4]                        @ 080db33c 9288
    cmp r2,#0x4f                             @ 080db33e 4f2a
    bls switchD_080db1ca__default            @ 080db340 08d9
    b switchD_080db1ca__caseD_0              @ 080db342 06e0
switchD_080db1ca__caseD_31:
    ldrh r2,[r2,#0x4]                        @ 080db344 9288
    cmp r2,#0x59                             @ 080db346 592a
    bls switchD_080db1ca__default            @ 080db348 04d9
    b switchD_080db1ca__caseD_0              @ 080db34a 02e0
switchD_080db1ca__caseD_32:
    ldrh r2,[r2,#0x4]                        @ 080db34c 9288
    cmp r2,#0x63                             @ 080db34e 632a
    bls switchD_080db1ca__default            @ 080db350 00d9
switchD_080db1ca__caseD_0:
    movs r4,#0x1    @ 080db352 0124
switchD_080db1ca__default:
    adds r0,r3,#0x0    @ 080db354 181c
    bl test_card_flag_bit__080f9a60          @ 080db356 1ef083fb
    cmp r0,#0x1                              @ 080db35a 0128
    bne LAB_080db360                         @ 080db35c 00d1
    movs r4,#0x1    @ 080db35e 0124
LAB_080db360:
    adds r0,r4,#0x0    @ 080db360 201c
    pop {r4}                                 @ 080db362 10bc
    pop {r1}                                 @ 080db364 02bc
    bx r1                                    @ 080db366 0847

@ Called via step-table dispatch from tick_pack_animation_step (0x080dc884), step index 0.
@ Executes selection state initialization when entering the pack scene. First calls
@ zero_fill_halfword_wrapper(pack_ui_state+0xc, 0x71c) to clear the first 0x71c/2 halfwords
@ of the struct. Then iterates over all enabled cards in card_stats_table to classify by type:
@ card type 0x16 (spell) -> [+0x2e]++; 0x17 (trap) -> [+0x2c]++; if pack_type_table[pack<<2]=3
@ (ritual) -> [+0x2a]++; if monster_type=1 -> [+0x28]++; else -> [+0x26]++. After loop reads
@ 0x095b7cca[0] (owned card count) and writes to [+0x30]. Calls build_pack_slot_selection_list
@ to build slot selection list, then reset_pack_scene_display to reset display state.
@ Returns fixed 1 (movs r0,#1 @ 080db40c; Sub-case E pop{r1};bx r1).
@ 
@ Params: none (r0 immediately clobbered by ldr r0,DAT_080db3a4)
@ Returns: r0=u8 1 (step-complete flag)
@ Side effects:
@   [pack_ui_state+0xc .. +0xc+0x71c]: zero-filled
@   [pack_ui_state+0xc+0x2e] += 1 per spell card
@   [pack_ui_state+0xc+0x2c] += 1 per trap card
@   [pack_ui_state+0xc+0x2a] += 1 per ritual-pack card
@   [pack_ui_state+0xc+0x28] += 1 per monster-type-1 card
@   [pack_ui_state+0xc+0x26] += 1 per other card
@   [pack_ui_state+0xc+0x30] := owned_card_count
@ Constants:
@   pack_ui_state = 0x03005850
@   ZERO_FILL_SIZE = 0x71c
@   CARD_COUNT_PTR = 0x095b7cca
@   card_stats_table = 0x098169b8
@   pack_type_table = 0x09e4f1c4
@   CARD_TYPE_SPELL = 0x16
@   CARD_TYPE_TRAP = 0x17
@   PACK_TYPE_RITUAL = 3
init_pack_scene_selection_state:
    push {r4,r5,r6,lr}                       @ 080db368 70b5
    ldr r0, DAT_080db3a4                     @ 080db36a 0e48
    adds r4,r0,#0x0    @ 080db36c 041c
    adds r4,#0xc    @ 080db36e 0c34
    ldr r1, DAT_080db3a8                     @ 080db370 0d49
    adds r0,r4,#0x0    @ 080db372 201c
    bl zero_fill_halfword_wrapper            @ 080db374 19f090fd
    movs r2,#0x1    @ 080db378 0122
    ldr r0, DAT_080db3ac                     @ 080db37a 0c48
    ldrh r0,[r0,#0x0]                        @ 080db37c 0088
    cmp r2,r0                                @ 080db37e 8242
    bhi LAB_080db3fe                         @ 080db380 3dd8
    ldr r3, PTR_card_stats_table_080db3b0    @ 080db382 0b4b
    ldr r6, DAT_080db3b4                     @ 080db384 0b4e
    adds r5,r0,#0x0    @ 080db386 051c
LAB_080db388:
    movs r0,#0xb    @ 080db388 0b20
    adds r1,r2,#0x0    @ 080db38a 111c
    muls r1,r0    @ 080db38c 4143
    adds r0,r1,#0x6    @ 080db38e 881d
    lsls r0,r0,#0x1    @ 080db390 4000
    adds r0,r0,r3    @ 080db392 c018
    ldrh r0,[r0,#0x0]                        @ 080db394 0088
    cmp r0,#0x16                             @ 080db396 1628
    bne LAB_080db3b8                         @ 080db398 0ed1
    ldrh r0,[r4,#0x2e]                       @ 080db39a e08d
    adds r0,#0x1    @ 080db39c 0130
    strh r0,[r4,#0x2e]                       @ 080db39e e085
    b LAB_080db3f8                           @ 080db3a0 2ae0
    .zero  0x2
DAT_080db3a4:
    .word  pack_ui_state                  @ 080db3a4 50580003
DAT_080db3a8:
    .word  0x0000071c                     @ 080db3a8 1c070000
DAT_080db3ac:
    .word  0x095b7cca                     @ 080db3ac ca7c5b09
PTR_card_stats_table_080db3b0:
    .word  card_stats_table               @ 080db3b0 b8698109
DAT_080db3b4:
    .word  0x09e4f1c4                     @ 080db3b4 c4f1e409
LAB_080db3b8:
    cmp r0,#0x17                             @ 080db3b8 1728
    bne LAB_080db3c4                         @ 080db3ba 03d1
    ldrh r0,[r4,#0x2c]                       @ 080db3bc a08d
    adds r0,#0x1    @ 080db3be 0130
    strh r0,[r4,#0x2c]                       @ 080db3c0 a085
    b LAB_080db3f8                           @ 080db3c2 19e0
LAB_080db3c4:
    adds r0,r1,#0x0    @ 080db3c4 081c
    adds r0,#0x8    @ 080db3c6 0830
    lsls r0,r0,#0x1    @ 080db3c8 4000
    adds r0,r0,r3    @ 080db3ca c018
    ldrh r1,[r0,#0x0]                        @ 080db3cc 0188
    lsls r0,r1,#0x2    @ 080db3ce 8800
    adds r0,r0,r6    @ 080db3d0 8019
    ldr r0,[r0,#0x0]                         @ 080db3d2 0068
    cmp r0,#0x3                              @ 080db3d4 0328
    bne LAB_080db3e0                         @ 080db3d6 03d1
    ldrh r0,[r4,#0x2a]                       @ 080db3d8 608d
    adds r0,#0x1    @ 080db3da 0130
    strh r0,[r4,#0x2a]                       @ 080db3dc 6085
    b LAB_080db3f8                           @ 080db3de 0be0
LAB_080db3e0:
    adds r0,r1,#0x0    @ 080db3e0 081c
    cmp r0,#0x1                              @ 080db3e2 0128
    bne LAB_080db3ee                         @ 080db3e4 03d1
    ldrh r0,[r4,#0x28]                       @ 080db3e6 208d
    adds r0,#0x1    @ 080db3e8 0130
    strh r0,[r4,#0x28]                       @ 080db3ea 2085
    b LAB_080db3f8                           @ 080db3ec 04e0
LAB_080db3ee:
    cmp r0,#0x0                              @ 080db3ee 0028
    bne LAB_080db3f8                         @ 080db3f0 02d1
    ldrh r0,[r4,#0x26]                       @ 080db3f2 e08c
    adds r0,#0x1    @ 080db3f4 0130
    strh r0,[r4,#0x26]                       @ 080db3f6 e084
LAB_080db3f8:
    adds r2,#0x1    @ 080db3f8 0132
    cmp r2,r5                                @ 080db3fa aa42
    bls LAB_080db388                         @ 080db3fc c4d9
LAB_080db3fe:
    ldr r0, DAT_080db414                     @ 080db3fe 0548
    ldrh r0,[r0,#0x0]                        @ 080db400 0088
    strh r0,[r4,#0x30]                       @ 080db402 2086
    bl build_pack_slot_selection_list        @ 080db404 00f076f8
    bl reset_pack_scene_display              @ 080db408 02f09ef9
    movs r0,#0x1    @ 080db40c 0120
    pop {r4,r5,r6}                           @ 080db40e 70bc
    pop {r1}                                 @ 080db410 02bc
    bx r1                                    @ 080db412 0847
DAT_080db414:
    .word  0x095b7cca                     @ 080db414 ca7c5b09

@ Init entry for the pack card detail view when the pack scene transitions to the card detail display layer. Calls reset_pack_scene_and_bg_scroll to clear the unpack UI display state and zero all BG scroll shadow registers, then calls load_pack_detail_bg3_tileset to load the card detail background tileset into BG3. Returns fixed 1 to notify the caller that the step is complete. Used as a step handler function by the pack scene state machine when switching to the card detail display layer.
init_pack_card_detail_view:
    push {lr}                                @ 080db418 00b5
    bl reset_pack_scene_and_bg_scroll        @ 080db41a 00f019fa
    bl load_pack_detail_bg3_tileset          @ 080db41e 00f0edfa
    movs r0,#0x1    @ 080db422 0120
    pop {r1}                                 @ 080db424 02bc
    bx r1                                    @ 080db426 0847

@ Single-frame driver for pack shop fadeout animation on exit. Writes 0x0800 to DISPCNT (0x04000000) to keep only BG3 visible, then calls tick_blend_step_by_delta with delta=4 to advance blend fadeout by one frame. Returns 1 if fadeout complete; otherwise 0.
@ 
@ Constants:
@ - DISPCNT=0x04000000 // GBA display control register
@ - DISPCNT_BG3_ONLY=0x0800 // bit11=BG3 enable, all other bits clear
@ - BLEND_DELTA=4 // blend step per frame
tick_pack_fadeout_step:
    push {lr}                                @ 080db428 00b5
    movs r0,#0x80    @ 080db42a 8020
    lsls r0,r0,#0x13    @ 080db42c c004
    movs r1,#0x80    @ 080db42e 8021
    lsls r1,r1,#0x4    @ 080db430 0901
    strh r1,[r0,#0x0]                        @ 080db432 0180
    movs r0,#0x4    @ 080db434 0420
    bl tick_blend_step_by_delta              @ 080db436 1af03ffa
    cmp r0,#0x1                              @ 080db43a 0128
    beq LAB_080db442                         @ 080db43c 01d0
    movs r0,#0x0    @ 080db43e 0020
    b LAB_080db444                           @ 080db440 00e0
LAB_080db442:
    movs r0,#0x1    @ 080db442 0120
LAB_080db444:
    pop {r1}                                 @ 080db444 02bc
    bx r1                                    @ 080db446 0847

@ Top-level pack-shop scene state dispatcher. Reads pack_ui_state+0xc[+0x0] (state_id), switches: 0->tick_pack_list_scene_step, 1->tick_pack_card_select_step, 2->tick_pack_duel_puzzle_step, 3->pack detail handler. Calls selected handler via invoke_r1. If handler returns nonzero: state_id:=[+0x2] (next_state), next_state:=0, step:=0. Returns 1 when state_id==4 (exit signal), else 0.
@ 
@ Constants:
@ - pack_ui_state=0x03005850
@ - STATE_PACK_LIST=0 // pack list page
@ - STATE_CARD_SELECT=1 // card select page
@ - STATE_DUEL_PUZZLE=2 // duel puzzle result page
@ - STATE_PACK_DETAIL=3 // pack detail page
@ - STATE_EXIT=4 // exit signal
dispatch_pack_shop_scene_by_state:
    push {r4,r5,lr}                          @ 080db448 30b5
    ldr r0, DAT_080db464                     @ 080db44a 0648
    adds r4,r0,#0x0    @ 080db44c 041c
    adds r4,#0xc    @ 080db44e 0c34
    movs r1,#0x0    @ 080db450 0021
    movs r5,#0x0    @ 080db452 0025
    ldrh r0,[r0,#0xc]                        @ 080db454 8089
    cmp r0,#0x1                              @ 080db456 0128
    beq LAB_080db47c                         @ 080db458 10d0
    cmp r0,#0x1                              @ 080db45a 0128
    bgt LAB_080db468                         @ 080db45c 04dc
    cmp r0,#0x0                              @ 080db45e 0028
    beq LAB_080db472                         @ 080db460 07d0
    b LAB_080db48e                           @ 080db462 14e0
DAT_080db464:
    .word  pack_ui_state                  @ 080db464 50580003
LAB_080db468:
    cmp r0,#0x2                              @ 080db468 0228
    beq LAB_080db484                         @ 080db46a 0bd0
    cmp r0,#0x3                              @ 080db46c 0328
    beq LAB_080db48c                         @ 080db46e 0dd0
    b LAB_080db48e                           @ 080db470 0de0
LAB_080db472:
    ldr r1, DAT_080db478                     @ 080db472 0149
    b LAB_080db48e                           @ 080db474 0be0
    .zero  0x2
DAT_080db478:
    .word  0x080dae45                     @ 080db478 45ae0d08
LAB_080db47c:
    ldr r1, DAT_080db480                     @ 080db47c 0049
    b LAB_080db48e                           @ 080db47e 06e0
DAT_080db480:
    .word  0x080d8505                     @ 080db480 05850d08
LAB_080db484:
    ldr r1, DAT_080db488                     @ 080db484 0049
    b LAB_080db48e                           @ 080db486 02e0
DAT_080db488:
    .word  0x080d8d4d                     @ 080db488 4d8d0d08
LAB_080db48c:
    ldr r1, DAT_080db4b8                     @ 080db48c 0a49
LAB_080db48e:
    cmp r1,#0x0                              @ 080db48e 0029
    beq LAB_080db4a6                         @ 080db490 09d0
    bl invoke_r1                             @ 080db492 33f09bf8
    cmp r0,#0x0                              @ 080db496 0028
    beq LAB_080db4a6                         @ 080db498 05d0
    ldrh r0,[r4,#0x2]                        @ 080db49a 6088
    movs r1,#0x0    @ 080db49c 0021
    strh r0,[r4,#0x0]                        @ 080db49e 2080
    movs r0,#0x4    @ 080db4a0 0420
    strh r0,[r4,#0x2]                        @ 080db4a2 6080
    strh r1,[r4,#0x4]                        @ 080db4a4 a180
LAB_080db4a6:
    ldrh r4,[r4,#0x0]                        @ 080db4a6 2488
    cmp r4,#0x4                              @ 080db4a8 042c
    bne LAB_080db4ae                         @ 080db4aa 00d1
    movs r5,#0x1    @ 080db4ac 0125
LAB_080db4ae:
    adds r0,r5,#0x0    @ 080db4ae 281c
    pop {r4,r5}                              @ 080db4b0 30bc
    pop {r1}                                 @ 080db4b2 02bc
    bx r1                                    @ 080db4b4 0847
    .zero  0x2
DAT_080db4b8:
    .word  0x080d7015                     @ 080db4b8 15700d08

@ Single-frame driver for pack shop scene fadein animation on entry. Writes 0x0800 to DISPCNT (0x04000000) to keep only BG3 visible, then calls start_blend_fadein_with_target with delta=4 to advance fadein by one frame. When fadein completes (returns 1), clears DISPCNT to 0 and returns 1; otherwise returns 0. Symmetric counterpart to tick_pack_fadeout_step (0x080db428).
@ 
@ Constants:
@ - DISPCNT=0x04000000 // GBA display control register
@ - DISPCNT_BG3_ONLY=0x0800 // bit11=BG3 enable
@ - BLEND_DELTA=4 // blend step per frame
tick_pack_fadein_step:
    push {r4,lr}                             @ 080db4bc 10b5
    movs r4,#0x80    @ 080db4be 8024
    lsls r4,r4,#0x13    @ 080db4c0 e404
    movs r0,#0x80    @ 080db4c2 8020
    lsls r0,r0,#0x4    @ 080db4c4 0001
    strh r0,[r4,#0x0]                        @ 080db4c6 2080
    movs r0,#0x4    @ 080db4c8 0420
    bl start_blend_fadein_with_target        @ 080db4ca 1af0b9f9
    cmp r0,#0x1                              @ 080db4ce 0128
    beq LAB_080db4d6                         @ 080db4d0 01d0
    movs r0,#0x0    @ 080db4d2 0020
    b LAB_080db4dc                           @ 080db4d4 02e0
LAB_080db4d6:
    movs r0,#0x0    @ 080db4d6 0020
    strh r0,[r4,#0x0]                        @ 080db4d8 2080
    movs r0,#0x1    @ 080db4da 0120
LAB_080db4dc:
    pop {r4}                                 @ 080db4dc 10bc
    pop {r1}                                 @ 080db4de 02bc
    bx r1                                    @ 080db4e0 0847
    .zero  0x2

@ Clears pack_ui_state[+0x6] (step counter reset), returns 1. Leaf function, two effective instructions. Called via indirect_table by the pack shop scene state machine (same hub as dispatch_pack_shop_scene_by_state) as a scene init/reset action.
@ 
@ Constants:
@ - pack_ui_state=0x03005850
@ - STEP_FIELD_OFF=0x6 // pack_ui_state[+0x6] := 0
clear_pack_shop_scene_step:
    ldr r1, DAT_080db4f0                     @ 080db4e4 0249
    movs r0,#0x0    @ 080db4e6 0020
    strh r0,[r1,#0x6]                        @ 080db4e8 c880
    movs r0,#0x1    @ 080db4ea 0120
    bx lr                                    @ 080db4ec 7047
    .zero  0x2
DAT_080db4f0:
    .word  pack_ui_state                  @ 080db4f0 50580003

@ Builds the pack slot selection list state. Iterates all pack slots (index 1..total_card_count, upper bound from 0x095b7cca[0] total card count field), for each slot passing check_pack_slot_purchase_eligible, reads get_pack_total_card_count to verify non-zero card count, calls test_card_flag_bit to check unlock status, and writes slot ID/owned count/unlock flag into the pack_ui_state+0xc selection list array (0x20 bytes per entry). Calls aggregate_challenge_clear_stats to aggregate challenge clear stats, then writes list length and two ROM function pointers to fixed offsets after the loop. Called by the pack card info page scene (enter_pack_card_info_page 0x080d6fbc / check_pack_slot_purchase_eligible 0x080db368).
build_pack_slot_selection_list:
    push {r4,r5,r6,r7,lr}                    @ 080db4f4 f0b5
    sub sp,#0x10                             @ 080db4f6 84b0
    ldr r0, DAT_080db534                     @ 080db4f8 0e48
    adds r6,r0,#0x0    @ 080db4fa 061c
    adds r6,#0xc    @ 080db4fc 0c36
    movs r4,#0x1    @ 080db4fe 0124
    ldr r3, DAT_080db538                     @ 080db500 0d4b
    ldr r0, DAT_080db53c                     @ 080db502 0e48
    adds r7,r0,#0x0    @ 080db504 071c
    ldrh r0,[r7,#0x0]                        @ 080db506 3888
    cmp r4,r0                                @ 080db508 8442
    bhi LAB_080db55c                         @ 080db50a 27d8
    movs r5,#0xf    @ 080db50c 0f25
    ldr r1, DAT_080db540                     @ 080db50e 0c49
    .hword 0x468c    @ 080db510 8c46
LAB_080db512:
    adds r1,r4,#0x0    @ 080db512 211c
    ands r1,r5    @ 080db514 2940
    movs r0,#0x80    @ 080db516 8020
    lsls r0,r0,#0x9    @ 080db518 4002
    lsls r0,r1    @ 080db51a 8840
    lsrs r2,r0,#0x10    @ 080db51c 020c
    lsls r1,r4,#0x1    @ 080db51e 6100
    add r1,r12                               @ 080db520 6144
    adds r0,r5,#0x0    @ 080db522 281c
    ldrb r1,[r1,#0x0]                        @ 080db524 0978
    ands r0,r1    @ 080db526 0840
    cmp r0,#0x0                              @ 080db528 0028
    beq LAB_080db544                         @ 080db52a 0bd0
    adds r0,r2,#0x0    @ 080db52c 101c
    ldrh r2,[r3,#0x0]                        @ 080db52e 1a88
    orrs r0,r2    @ 080db530 1043
    b LAB_080db548                           @ 080db532 09e0
DAT_080db534:
    .word  pack_ui_state                  @ 080db534 50580003
DAT_080db538:
    .word  0x020363c0                     @ 080db538 c0630302
DAT_080db53c:
    .word  0x095b7cca                     @ 080db53c ca7c5b09
DAT_080db540:
    .word  0x02000006                     @ 080db540 06000002
LAB_080db544:
    ldrh r0,[r3,#0x0]                        @ 080db544 1888
    bics r0,r2    @ 080db546 9043
LAB_080db548:
    strh r0,[r3,#0x0]                        @ 080db548 1880
    adds r4,#0x1    @ 080db54a 0134
    adds r0,r4,#0x0    @ 080db54c 201c
    ands r0,r5    @ 080db54e 2840
    cmp r0,#0x0                              @ 080db550 0028
    bne LAB_080db556                         @ 080db552 00d1
    adds r3,#0x2    @ 080db554 0233
LAB_080db556:
    ldrh r0,[r7,#0x0]                        @ 080db556 3888
    cmp r4,r0                                @ 080db558 8442
    bls LAB_080db512                         @ 080db55a dad9
LAB_080db55c:
    adds r4,r6,#0x0    @ 080db55c 341c
    adds r4,#0x44    @ 080db55e 4434
    movs r0,#0x0    @ 080db560 0020
    strh r0,[r6,#0x8]                        @ 080db562 3081
    strh r0,[r6,#0xa]                        @ 080db564 7081
    str r0,[r6,#0xc]                         @ 080db566 f060
    .hword 0x4668    @ 080db568 6846
    bl aggregate_challenge_clear_stats       @ 080db56a fff72bfd
    movs r5,#0x0    @ 080db56e 0025
LAB_080db570:
    adds r0,r5,#0x0    @ 080db570 281c
    .hword 0x4669    @ 080db572 6946
    bl check_pack_slot_purchase_eligible     @ 080db574 fff71efe
    cmp r0,#0x1                              @ 080db578 0128
    bne LAB_080db5bc                         @ 080db57a 1fd1
    adds r0,r5,#0x0    @ 080db57c 281c
    bl get_pack_total_card_count             @ 080db57e fff77dfc
    lsls r0,r0,#0x10    @ 080db582 0004
    cmp r0,#0x0                              @ 080db584 0028
    beq LAB_080db5bc                         @ 080db586 19d0
    movs r0,#0x0    @ 080db588 0020
    strh r5,[r4,#0x0]                        @ 080db58a 2580
    str r0,[r4,#0x14]                        @ 080db58c 6061
    strh r0,[r4,#0x18]                       @ 080db58e 2083
    adds r0,r5,#0x0    @ 080db590 281c
    bl test_card_flag_bit__080f9a60          @ 080db592 1ef065fa
    movs r1,#0x0    @ 080db596 0021
    cmp r0,#0x0                              @ 080db598 0028
    bne LAB_080db59e                         @ 080db59a 00d1
    movs r1,#0x1    @ 080db59c 0121
LAB_080db59e:
    movs r2,#0x2    @ 080db59e 0222
    rsbs r2,r2,#0    @ 080db5a0 5242
    adds r0,r2,#0x0    @ 080db5a2 101c
    ldrb r2,[r4,#0x1c]                       @ 080db5a4 227f
    ands r0,r2    @ 080db5a6 1040
    orrs r0,r1    @ 080db5a8 0843
    strb r0,[r4,#0x1c]                       @ 080db5aa 2077
    ldrh r0,[r4,#0x0]                        @ 080db5ac 2088
    bl count_owned_cards_in_pack_slot        @ 080db5ae 00f025f8
    strh r0,[r4,#0x1a]                       @ 080db5b2 6083
    ldrh r0,[r6,#0x8]                        @ 080db5b4 3089
    adds r0,#0x1    @ 080db5b6 0130
    strh r0,[r6,#0x8]                        @ 080db5b8 3081
    adds r4,#0x20    @ 080db5ba 2034
LAB_080db5bc:
    adds r5,#0x1    @ 080db5bc 0135
    cmp r5,#0x32                             @ 080db5be 322d
    bls LAB_080db570                         @ 080db5c0 d6d9
    ldr r0, DAT_080db5f0                     @ 080db5c2 0b48
    adds r1,r6,r0    @ 080db5c4 3118
    movs r0,#0x0    @ 080db5c6 0020
    strh r0,[r1,#0x0]                        @ 080db5c8 0880
    movs r1,#0xde    @ 080db5ca de21
    lsls r1,r1,#0x3    @ 080db5cc c900
    adds r0,r6,r1    @ 080db5ce 7018
    ldr r1, DAT_080db5f4                     @ 080db5d0 0849
    str r1,[r0,#0x0]                         @ 080db5d2 0160
    ldr r2, DAT_080db5f8                     @ 080db5d4 084a
    adds r0,r6,r2    @ 080db5d6 b018
    str r1,[r0,#0x0]                         @ 080db5d8 0160
    movs r0,#0xe3    @ 080db5da e320
    lsls r0,r0,#0x3    @ 080db5dc c000
    adds r1,r6,r0    @ 080db5de 3118
    movs r0,#0x1    @ 080db5e0 0120
    ldrb r2,[r1,#0x0]                        @ 080db5e2 0a78
    orrs r0,r2    @ 080db5e4 1043
    strb r0,[r1,#0x0]                        @ 080db5e6 0870
    add sp,#0x10                             @ 080db5e8 04b0
    pop {r4,r5,r6,r7}                        @ 080db5ea f0bc
    pop {r0}                                 @ 080db5ec 01bc
    bx r0                                    @ 080db5ee 0047
DAT_080db5f0:
    .word  0x000006ec                     @ 080db5f0 ec060000
DAT_080db5f4:
    .word  0x02029eb0                     @ 080db5f4 b09e0202
DAT_080db5f8:
    .word  0x000006f4                     @ 080db5f8 f4060000

@ Counts how many cards in the specified pack slot (r0=pack_id [0..50]) the player currently owns. If pack has a fixed card list (pack_info_table[r0*16+0xc] != 0), iterates each card entry, calls internal_card_id_to_card_id, checks the card-ownership bitmap at 0x020363c0. If list is empty (filter pack), iterates all cards using check_pack_card_slot_filter and does the same bitmap check. Returns r0 = owned card count.
@ 
@ Constants:
@ - pack_info_table=0x09e5e2e8 // pack info table base
@ - CARD_OWN_BITMAP=0x020363c0 // EWRAM card ownership bitmap base
@ - CARD_OWN_BIT_STRIDE=0x10 // 16 cards per group (lsrs r0,r5,#4 + lsls*2 = word index)
@ - OWN_BIT_MASK=0x1 // ownership flag bit
count_owned_cards_in_pack_slot:
    push {r4,r5,r6,r7,lr}                    @ 080db5fc f0b5
    .hword 0x4647    @ 080db5fe 4746
    push {r7}                                @ 080db600 80b4
    adds r7,r0,#0x0    @ 080db602 071c
    lsls r0,r7,#0x4    @ 080db604 3801
    ldr r1, PTR_pack_info_table_080db61c     @ 080db606 0549
    adds r0,r0,r1    @ 080db608 4018
    ldr r4,[r0,#0xc]                         @ 080db60a c468
    movs r6,#0x0    @ 080db60c 0026
    cmp r4,#0x0                              @ 080db60e 002c
    beq LAB_080db664                         @ 080db610 28d0
    movs r5,#0x0    @ 080db612 0025
    ldr r0, DAT_080db620                     @ 080db614 0248
    .hword 0x4680    @ 080db616 8046
    b LAB_080db654                           @ 080db618 1ce0
    .zero  0x2
PTR_pack_info_table_080db61c:
    .word  pack_info_table                @ 080db61c e8e2e509
DAT_080db620:
    .word  0x020363c0                     @ 080db620 c0630302
LAB_080db624:
    ldrh r0,[r4,#0x0]                        @ 080db624 2088
    bl internal_card_id_to_card_id           @ 080db626 13f0a1f8
    lsls r0,r0,#0x10    @ 080db62a 0004
    lsrs r0,r0,#0x10    @ 080db62c 000c
    movs r1,#0x3    @ 080db62e 0321
    ldrh r2,[r4,#0x2]                        @ 080db630 6288
    ands r1,r2    @ 080db632 1140
    adds r0,r0,r1    @ 080db634 4018
    lsrs r2,r0,#0x4    @ 080db636 0209
    lsls r2,r2,#0x1    @ 080db638 5200
    add r2,r8                                @ 080db63a 4244
    movs r1,#0xf    @ 080db63c 0f21
    ands r0,r1    @ 080db63e 0840
    ldrh r2,[r2,#0x0]                        @ 080db640 1288
    asrs r2,r0    @ 080db642 0241
    adds r0,r2,#0x0    @ 080db644 101c
    movs r1,#0x1    @ 080db646 0121
    ands r0,r1    @ 080db648 0840
    cmp r0,#0x1                              @ 080db64a 0128
    bne LAB_080db650                         @ 080db64c 00d1
    adds r6,#0x1    @ 080db64e 0136
LAB_080db650:
    adds r4,#0x4    @ 080db650 0434
    adds r5,#0x1    @ 080db652 0135
LAB_080db654:
    adds r0,r7,#0x0    @ 080db654 381c
    bl get_pack_total_card_count             @ 080db656 fff711fc
    lsls r0,r0,#0x10    @ 080db65a 0004
    lsrs r0,r0,#0x10    @ 080db65c 000c
    cmp r5,r0                                @ 080db65e 8542
    bcc LAB_080db624                         @ 080db660 e0d3
    b LAB_080db6a4                           @ 080db662 1fe0
LAB_080db664:
    movs r5,#0x1    @ 080db664 0125
    ldr r0, DAT_080db6b0                     @ 080db666 1248
    ldrh r0,[r0,#0x0]                        @ 080db668 0088
    cmp r5,r0                                @ 080db66a 8542
    bhi LAB_080db6a4                         @ 080db66c 1ad8
    ldr r4, DAT_080db6b4                     @ 080db66e 114c
LAB_080db670:
    adds r0,r5,#0x0    @ 080db670 281c
    adds r1,r7,#0x0    @ 080db672 391c
    bl check_pack_card_slot_filter           @ 080db674 fff736fc
    adds r2,r0,#0x0    @ 080db678 021c
    cmp r2,#0x1                              @ 080db67a 012a
    bne LAB_080db69a                         @ 080db67c 0dd1
    lsrs r0,r5,#0x4    @ 080db67e 2809
    lsls r0,r0,#0x1    @ 080db680 4000
    adds r0,r0,r4    @ 080db682 0019
    movs r1,#0xf    @ 080db684 0f21
    ands r1,r5    @ 080db686 2940
    ldrh r0,[r0,#0x0]                        @ 080db688 0088
    asrs r0,r1    @ 080db68a 0841
    adds r1,r0,#0x0    @ 080db68c 011c
    ands r1,r2    @ 080db68e 1140
    rsbs r0,r1,#0    @ 080db690 4842
    orrs r0,r1    @ 080db692 0843
    cmp r0,#0x0                              @ 080db694 0028
    bge LAB_080db69a                         @ 080db696 00da
    adds r6,#0x1    @ 080db698 0136
LAB_080db69a:
    adds r5,#0x1    @ 080db69a 0135
    ldr r0, DAT_080db6b0                     @ 080db69c 0448
    ldrh r0,[r0,#0x0]                        @ 080db69e 0088
    cmp r5,r0                                @ 080db6a0 8542
    bls LAB_080db670                         @ 080db6a2 e5d9
LAB_080db6a4:
    adds r0,r6,#0x0    @ 080db6a4 301c
    pop {r3}                                 @ 080db6a6 08bc
    .hword 0x4698    @ 080db6a8 9846
    pop {r4,r5,r6,r7}                        @ 080db6aa f0bc
    pop {r1}                                 @ 080db6ac 02bc
    bx r1                                    @ 080db6ae 0847
DAT_080db6b0:
    .word  0x095b7cca                     @ 080db6b0 ca7c5b09
DAT_080db6b4:
    .word  0x020363c0                     @ 080db6b4 c0630302

@ Called when player increases purchase quantity for a pack slot. r0=slot_index, r1=delta. Reads pack_info_table[slot_id*16] for unit price (r2) and ratio (r3). Adds r1 to pack_ui_state[+0xc+0xa] (selected count), adds price*delta to [+0xc+0xc] (selected total price), and adds (ratio+1)*delta to pack_ui_state[0xdf8] (global selected card count). Symmetric counterpart to decrement_pack_slot_selection_count (0x080db700).
@ 
@ Constants:
@ - PACK_INFO_STRIDE=0x10 // pack_info_table entry stride (16 bytes)
@ - UI_COUNT_OFF=0xa // selected count field in pack_ui_state+0xc (halfword)
@ - UI_PRICE_OFF=0xc // selected total price field (word)
@ - TOTAL_CARD_OFF=0xdf8 // global selected card count field (halfword)
increment_pack_slot_selection_count:
    push {r4,r5,r6,lr}                       @ 080db6b8 70b5
    ldr r5, DAT_080db6f8                     @ 080db6ba 0f4d
    adds r4,r5,#0x0    @ 080db6bc 2c1c
    adds r4,#0xc    @ 080db6be 0c34
    lsls r0,r0,#0x5    @ 080db6c0 4001
    adds r0,#0x44    @ 080db6c2 4430
    adds r0,r0,r4    @ 080db6c4 0019
    ldr r2, PTR_pack_info_table_080db6fc     @ 080db6c6 0d4a
    ldrh r0,[r0,#0x0]                        @ 080db6c8 0088
    lsls r0,r0,#0x4    @ 080db6ca 0001
    adds r0,r0,r2    @ 080db6cc 8018
    ldrh r2,[r0,#0x0]                        @ 080db6ce 0288
    ldrh r3,[r0,#0x2]                        @ 080db6d0 4388
    ldrh r6,[r4,#0xa]                        @ 080db6d2 6689
    adds r0,r6,r1    @ 080db6d4 7018
    strh r0,[r4,#0xa]                        @ 080db6d6 6081
    muls r2,r1    @ 080db6d8 4a43
    ldr r0,[r4,#0xc]                         @ 080db6da e068
    adds r0,r0,r2    @ 080db6dc 8018
    str r0,[r4,#0xc]                         @ 080db6de e060
    movs r0,#0xdf    @ 080db6e0 df20
    lsls r0,r0,#0x3    @ 080db6e2 c000
    adds r5,r5,r0    @ 080db6e4 2d18
    adds r3,#0x1    @ 080db6e6 0133
    adds r0,r1,#0x0    @ 080db6e8 081c
    muls r0,r3    @ 080db6ea 5843
    ldrh r1,[r5,#0x0]                        @ 080db6ec 2988
    adds r0,r1,r0    @ 080db6ee 0818
    strh r0,[r5,#0x0]                        @ 080db6f0 2880
    pop {r4,r5,r6}                           @ 080db6f2 70bc
    pop {r0}                                 @ 080db6f4 01bc
    bx r0                                    @ 080db6f6 0047
DAT_080db6f8:
    .word  pack_ui_state                  @ 080db6f8 50580003
PTR_pack_info_table_080db6fc:
    .word  pack_info_table                @ 080db6fc e8e2e509

@ Called when player decreases purchase quantity for a pack slot. r0=slot_index, r1=delta. Reads pack_info_table[slot_id*16] for unit price (r2) and ratio (r3). Subtracts r1 from pack_ui_state[+0xc+0xa] (selected count), subtracts price*delta from [+0xc+0xc] (selected total price), subtracts (ratio+1)*delta from pack_ui_state[0xdf8] (global card count). Symmetric counterpart to increment_pack_slot_selection_count (0x080db6b8).
@ 
@ Constants:
@ - PACK_INFO_STRIDE=0x10 // pack_info_table entry stride (16 bytes)
@ - UI_COUNT_OFF=0xa // selected count field
@ - UI_PRICE_OFF=0xc // selected total price field
@ - TOTAL_CARD_OFF=0xdf8 // global selected card count field
decrement_pack_slot_selection_count:
    push {r4,r5,r6,lr}                       @ 080db700 70b5
    ldr r5, DAT_080db740                     @ 080db702 0f4d
    adds r4,r5,#0x0    @ 080db704 2c1c
    adds r4,#0xc    @ 080db706 0c34
    lsls r0,r0,#0x5    @ 080db708 4001
    adds r0,#0x44    @ 080db70a 4430
    adds r0,r0,r4    @ 080db70c 0019
    ldr r2, PTR_pack_info_table_080db744     @ 080db70e 0d4a
    ldrh r0,[r0,#0x0]                        @ 080db710 0088
    lsls r0,r0,#0x4    @ 080db712 0001
    adds r0,r0,r2    @ 080db714 8018
    ldrh r2,[r0,#0x0]                        @ 080db716 0288
    ldrh r3,[r0,#0x2]                        @ 080db718 4388
    ldrh r6,[r4,#0xa]                        @ 080db71a 6689
    subs r0,r6,r1    @ 080db71c 701a
    strh r0,[r4,#0xa]                        @ 080db71e 6081
    muls r2,r1    @ 080db720 4a43
    ldr r0,[r4,#0xc]                         @ 080db722 e068
    subs r0,r0,r2    @ 080db724 801a
    str r0,[r4,#0xc]                         @ 080db726 e060
    movs r0,#0xdf    @ 080db728 df20
    lsls r0,r0,#0x3    @ 080db72a c000
    adds r5,r5,r0    @ 080db72c 2d18
    adds r3,#0x1    @ 080db72e 0133
    adds r0,r1,#0x0    @ 080db730 081c
    muls r0,r3    @ 080db732 5843
    ldrh r1,[r5,#0x0]                        @ 080db734 2988
    subs r0,r1,r0    @ 080db736 081a
    strh r0,[r5,#0x0]                        @ 080db738 2880
    pop {r4,r5,r6}                           @ 080db73a 70bc
    pop {r0}                                 @ 080db73c 01bc
    bx r0                                    @ 080db73e 0047
DAT_080db740:
    .word  pack_ui_state                  @ 080db740 50580003
PTR_pack_info_table_080db744:
    .word  pack_info_table                @ 080db744 e8e2e509

@ Recomputes all three pack selection totals from scratch. Zeroes pack_ui_state[+0xc+0xa] (total selected count), [+0xc+0xc] (total price), and [+0x6f8] (global card count), then iterates over [+8] slots, reads pack_info_table for price and ratio, and re-accumulates all three fields. Called after external modification of purchase quantities to restore field consistency.
@ 
@ Constants:
@ - UI_COUNT_OFF=0xa // selected count field (halfword)
@ - UI_PRICE_OFF=0xc // selected total price field (word)
@ - TOTAL_CARD_OFF=0x6f8 // global selected card count (halfword; 0xdf<<3=0x6f8)
@ - PACK_INFO_STRIDE=0x10 // pack_info_table entry stride (16 bytes)
recompute_pack_selection_totals:
    push {r4,r5,r6,r7,lr}                    @ 080db748 f0b5
    .hword 0x4647    @ 080db74a 4746
    push {r7}                                @ 080db74c 80b4
    ldr r2, DAT_080db7bc                     @ 080db74e 1b4a
    adds r3,r2,#0x0    @ 080db750 131c
    adds r3,#0xc    @ 080db752 0c33
    adds r4,r2,#0x0    @ 080db754 141c
    adds r4,#0x50    @ 080db756 5034
    movs r0,#0x0    @ 080db758 0020
    strh r0,[r3,#0xa]                        @ 080db75a 5881
    str r0,[r3,#0xc]                         @ 080db75c d860
    movs r5,#0xdf    @ 080db75e df25
    lsls r5,r5,#0x3    @ 080db760 ed00
    adds r1,r2,r5    @ 080db762 5119
    strh r0,[r1,#0x0]                        @ 080db764 0880
    movs r6,#0x0    @ 080db766 0026
    ldrh r7,[r3,#0x8]                        @ 080db768 1f89
    cmp r6,r7                                @ 080db76a be42
    bcs LAB_080db7b0                         @ 080db76c 20d2
    ldr r0, PTR_pack_info_table_080db7c0     @ 080db76e 1448
    .hword 0x4684    @ 080db770 8446
    adds r1,r5,#0x0    @ 080db772 291c
    adds r1,r1,r2    @ 080db774 8918
    .hword 0x4688    @ 080db776 8846
LAB_080db778:
    ldrh r2,[r4,#0x0]                        @ 080db778 2288
    lsls r0,r2,#0x4    @ 080db77a 1001
    add r0,r12                               @ 080db77c 6044
    ldrh r1,[r0,#0x0]                        @ 080db77e 0188
    ldrh r2,[r0,#0x2]                        @ 080db780 4288
    ldrh r5,[r3,#0xa]                        @ 080db782 5d89
    ldrh r7,[r4,#0x18]                       @ 080db784 278b
    adds r0,r5,r7    @ 080db786 e819
    strh r0,[r3,#0xa]                        @ 080db788 5881
    ldrh r0,[r4,#0x18]                       @ 080db78a 208b
    muls r1,r0    @ 080db78c 4143
    ldr r0,[r3,#0xc]                         @ 080db78e d868
    adds r0,r0,r1    @ 080db790 4018
    str r0,[r3,#0xc]                         @ 080db792 d860
    adds r2,#0x1    @ 080db794 0132
    ldrh r1,[r4,#0x18]                       @ 080db796 218b
    adds r0,r1,#0x0    @ 080db798 081c
    muls r0,r2    @ 080db79a 5043
    .hword 0x4642    @ 080db79c 4246
    ldrh r2,[r2,#0x0]                        @ 080db79e 1288
    adds r0,r2,r0    @ 080db7a0 1018
    .hword 0x4645    @ 080db7a2 4546
    strh r0,[r5,#0x0]                        @ 080db7a4 2880
    adds r4,#0x20    @ 080db7a6 2034
    adds r6,#0x1    @ 080db7a8 0136
    ldrh r7,[r3,#0x8]                        @ 080db7aa 1f89
    cmp r6,r7                                @ 080db7ac be42
    bcc LAB_080db778                         @ 080db7ae e3d3
LAB_080db7b0:
    pop {r3}                                 @ 080db7b0 08bc
    .hword 0x4698    @ 080db7b2 9846
    pop {r4,r5,r6,r7}                        @ 080db7b4 f0bc
    pop {r0}                                 @ 080db7b6 01bc
    bx r0                                    @ 080db7b8 0047
    .zero  0x2
DAT_080db7bc:
    .word  pack_ui_state                  @ 080db7bc 50580003
PTR_pack_info_table_080db7c0:
    .word  pack_info_table                @ 080db7c0 e8e2e509

@ Called when player adjusts pack purchase quantity; validates that new total card count does not exceed limit 0x5fff (24575). Reads pack_info_table[slot*16+2] ratio, computes candidate total = pack_ui_state[0xdf8] + (ratio+1)*r1. If over limit, calls game_str_id_to_row(0x13f5) to find the over-limit warning text and displays it via text_overlay_create; returns 0 (fail). Otherwise returns 1 (allow purchase).
@ 
@ Constants:
@ - LIMIT_MAX=0x5fff // 24575: single purchase total card count limit
@ - STR_ID=0x13f5 // 5109: purchase limit warning string
@ - TEXT_POS=0x0010001e // x=16, y=30: warning text position
@ - LANG_FLAG_OFF=0x6c2c // IWRAM language flag offset
enforce_pack_purchase_limit:
    push {r4,lr}                             @ 080db7c4 10b5
    ldr r2, DAT_080db824                     @ 080db7c6 174a
    lsls r0,r0,#0x5    @ 080db7c8 4001
    adds r0,r0,r2    @ 080db7ca 8018
    adds r0,#0x50    @ 080db7cc 5030
    ldr r3, PTR_pack_info_table_080db828     @ 080db7ce 164b
    ldrh r0,[r0,#0x0]                        @ 080db7d0 0088
    lsls r0,r0,#0x4    @ 080db7d2 0001
    adds r0,r0,r3    @ 080db7d4 c018
    movs r3,#0xdf    @ 080db7d6 df23
    lsls r3,r3,#0x3    @ 080db7d8 db00
    adds r2,r2,r3    @ 080db7da d218
    ldrh r0,[r0,#0x2]                        @ 080db7dc 4088
    adds r0,#0x1    @ 080db7de 0130
    muls r0,r1    @ 080db7e0 4843
    ldrh r2,[r2,#0x0]                        @ 080db7e2 1288
    adds r0,r2,r0    @ 080db7e4 1018
    ldr r1, DAT_080db82c                     @ 080db7e6 1149
    cmp r0,r1                                @ 080db7e8 8842
    bls LAB_080db848                         @ 080db7ea 2dd9
    ldr r4, DAT_080db830                     @ 080db7ec 104c
    ldr r0, DAT_080db834                     @ 080db7ee 1148
    bl game_str_id_to_row                    @ 080db7f0 19f012fb
    ldr r2, PTR_game_str_pointer_table_080db838 @ 080db7f4 104a
    lsls r0,r0,#0x10    @ 080db7f6 0004
    lsrs r0,r0,#0x10    @ 080db7f8 000c
    lsls r1,r0,#0x1    @ 080db7fa 4100
    adds r1,r1,r0    @ 080db7fc 0918
    lsls r1,r1,#0x1    @ 080db7fe 4900
    ldr r0, DAT_080db83c                     @ 080db800 0e48
    ldr r3, DAT_080db840                     @ 080db802 0f4b
    adds r0,r0,r3    @ 080db804 c018
    ldrb r0,[r0,#0x0]                        @ 080db806 0078
    lsls r0,r0,#0x1d    @ 080db808 4007
    lsrs r0,r0,#0x1d    @ 080db80a 400f
    adds r1,r1,r0    @ 080db80c 0918
    lsls r1,r1,#0x2    @ 080db80e 8900
    adds r1,r1,r2    @ 080db810 8918
    ldr r2,[r1,#0x0]                         @ 080db812 0a68
    ldr r0, PTR_game_str_ja_080db844         @ 080db814 0b48
    adds r2,r2,r0    @ 080db816 1218
    adds r0,r4,#0x0    @ 080db818 201c
    movs r1,#0x0    @ 080db81a 0021
    bl text_overlay_create                   @ 080db81c 01f08efe
    movs r0,#0x0    @ 080db820 0020
    b LAB_080db84a                           @ 080db822 12e0
DAT_080db824:
    .word  pack_ui_state                  @ 080db824 50580003
PTR_pack_info_table_080db828:
    .word  pack_info_table                @ 080db828 e8e2e509
DAT_080db82c:
    .word  0x00005fff                     @ 080db82c ff5f0000
DAT_080db830:
    .word  0x0010001e                     @ 080db830 1e001000
DAT_080db834:
    .word  0x000013f5                     @ 080db834 f5130000
PTR_game_str_pointer_table_080db838:
    .word  game_str_pointer_table         @ 080db838 400f0008
DAT_080db83c:
    .word  0x02000000                     @ 080db83c 00000002
DAT_080db840:
    .word  0x00006c2c                     @ 080db840 2c6c0000
PTR_game_str_ja_080db844:
    .word  game_str_ja                    @ 080db844 109cdb09
LAB_080db848:
    movs r0,#0x1    @ 080db848 0120
LAB_080db84a:
    pop {r4}                                 @ 080db84a 10bc
    pop {r1}                                 @ 080db84c 02bc
    bx r1                                    @ 080db84e 0847

@ Pack scene dual-reset entry point. Calls reset_pack_scene_display to clear pack UI display state, then calls reset_all_bg_scroll_regs_and_shadows to zero all BG scroll registers and shadows. Called by pack_080db418 (pack scene state machine) when a full display layer reset is needed. No parameters, no return value (Pattern B void).
@ 
@ Constants: (no non-trivial literals)
@ 
@ Params: r0=void
@ Return: void (pop {r0}; bx r0 = Pattern B VOID)
reset_pack_scene_and_bg_scroll:
    push {lr}                                @ 080db850 00b5
    bl reset_pack_scene_display              @ 080db852 01f079ff
    bl reset_all_bg_scroll_regs_and_shadows  @ 080db856 1af017f9
    pop {r0}                                 @ 080db85a 01bc
    bx r0                                    @ 080db85c 0047
    .zero  0x2

@ pack-banner: ROM 指针表 0x09CCE960[id] → OBJ VRAM, mode 1=2D stride
pack_banner_tile_copy:
    push {r4,r5,r6,r7,lr}                    @ 080db860 f0b5
    .hword 0x4647    @ 080db862 4746
    push {r7}                                @ 080db864 80b4
    adds r4,r1,#0x0    @ 080db866 0c1c
    .hword 0x4690    @ 080db868 9046
    lsls r6,r2,#0x8    @ 080db86a 1602
    movs r2,#0xff    @ 080db86c ff22
    lsls r2,r2,#0x8    @ 080db86e 1202
    adds r1,r2,#0x0    @ 080db870 111c
    ands r6,r1    @ 080db872 0e40
    movs r2,#0xff    @ 080db874 ff22
    .hword 0x4641    @ 080db876 4146
    ands r1,r2    @ 080db878 1140
    orrs r6,r1    @ 080db87a 0e43
    ldr r2, PTR_pack_banner_ptr_table_080db8b4 @ 080db87c 0d4a
    lsls r1,r0,#0x2    @ 080db87e 8100
    adds r1,r1,r2    @ 080db880 8918
    ldr r1,[r1,#0x0]                         @ 080db882 0968
    cmp r3,#0x0                              @ 080db884 002b
    bne LAB_080db8bc                         @ 080db886 19d1
    movs r2,#0x80    @ 080db888 8022
    lsls r2,r2,#0x4    @ 080db88a 1201
    adds r0,r4,#0x0    @ 080db88c 201c
    bl copy_memory_dma3_with_cpu_fallback    @ 080db88e 19f03bfb
    .hword 0x4640    @ 080db892 4046
    cmp r0,#0x0                              @ 080db894 0028
    beq LAB_080db904                         @ 080db896 35d0
    adds r1,r4,#0x0    @ 080db898 211c
    movs r2,#0x0    @ 080db89a 0022
    ldr r3, DAT_080db8b8                     @ 080db89c 064b
LAB_080db89e:
    ldrh r0,[r1,#0x0]                        @ 080db89e 0888
    cmp r0,#0x0                              @ 080db8a0 0028
    beq LAB_080db8a8                         @ 080db8a2 01d0
    adds r0,r6,r0    @ 080db8a4 3018
    strh r0,[r1,#0x0]                        @ 080db8a6 0880
LAB_080db8a8:
    adds r1,#0x2    @ 080db8a8 0231
    adds r2,#0x1    @ 080db8aa 0132
    cmp r2,r3                                @ 080db8ac 9a42
    bls LAB_080db89e                         @ 080db8ae f6d9
    b LAB_080db904                           @ 080db8b0 28e0
    .zero  0x2
PTR_pack_banner_ptr_table_080db8b4:
    .word  pack_banner_ptr_table          @ 080db8b4 60e9cc09
DAT_080db8b8:
    .word  0x000003ff                     @ 080db8b8 ff030000
LAB_080db8bc:
    adds r7,r1,#0x0    @ 080db8bc 0f1c
    movs r5,#0x0    @ 080db8be 0025
LAB_080db8c0:
    adds r0,r4,#0x0    @ 080db8c0 201c
    adds r1,r7,#0x0    @ 080db8c2 391c
    movs r2,#0x80    @ 080db8c4 8022
    lsls r2,r2,#0x1    @ 080db8c6 5200
    bl copy_memory_dma3_with_cpu_fallback    @ 080db8c8 19f01efb
    .hword 0x4641    @ 080db8cc 4146
    cmp r1,#0x0                              @ 080db8ce 0029
    beq LAB_080db8f0                         @ 080db8d0 0ed0
    movs r2,#0x0    @ 080db8d2 0022
    adds r1,r5,#0x1    @ 080db8d4 691c
LAB_080db8d6:
    ldrh r0,[r4,#0x0]                        @ 080db8d6 2088
    cmp r0,#0x0                              @ 080db8d8 0028
    beq LAB_080db8e0                         @ 080db8da 01d0
    adds r0,r6,r0    @ 080db8dc 3018
    strh r0,[r4,#0x0]                        @ 080db8de 2080
LAB_080db8e0:
    adds r4,#0x2    @ 080db8e0 0234
    adds r2,#0x1    @ 080db8e2 0132
    cmp r2,#0x7f                             @ 080db8e4 7f2a
    bls LAB_080db8d6                         @ 080db8e6 f6d9
    movs r2,#0xc0    @ 080db8e8 c022
    lsls r2,r2,#0x2    @ 080db8ea 9200
    adds r4,r4,r2    @ 080db8ec a418
    b LAB_080db8f8                           @ 080db8ee 03e0
LAB_080db8f0:
    movs r0,#0x80    @ 080db8f0 8020
    lsls r0,r0,#0x3    @ 080db8f2 c000
    adds r4,r4,r0    @ 080db8f4 2418
    adds r1,r5,#0x1    @ 080db8f6 691c
LAB_080db8f8:
    movs r2,#0x80    @ 080db8f8 8022
    lsls r2,r2,#0x1    @ 080db8fa 5200
    adds r7,r7,r2    @ 080db8fc bf18
    adds r5,r1,#0x0    @ 080db8fe 0d1c
    cmp r5,#0x7                              @ 080db900 072d
    bls LAB_080db8c0                         @ 080db902 ddd9
LAB_080db904:
    pop {r3}                                 @ 080db904 08bc
    .hword 0x4698    @ 080db906 9846
    pop {r4,r5,r6,r7}                        @ 080db908 f0bc
    pop {r0}                                 @ 080db90a 01bc
    bx r0                                    @ 080db90c 0047
    .zero  0x2

@ Copies the medium card frame graphic for the given card (r0=icid/frame_idx) from ROM to OBJ VRAM destination (r1=VRAM dst ptr). r2=palette byte offset, r3=0 for single DMA+palette fixup; r3!=0 for 6-segment mode, each segment DMA copies 0x100 bytes + palette fixup, advancing vram dst by 0x300 bytes. In JAPAN mode (IWRAM[0x02006c2c] low 3 bits nonzero) uses alternate card_image_index entry. After copy, adds palette offset r2 to nonzero pixels.
@ 
@ Constants:
@ - CARD_IMAGE_INDEX=card_image_index // card image index table (0x095b5c00)
@ - CARD_FRAME_DATA=card_medium_frame_tile_data // medium frame graphic base (0x08fbc080)
@ - FRAME_SIZE_SINGLE=0x600 // 0xc0<<3 bytes: single-segment mode size
@ - FRAME_SEGMENTS=6 // r3!=0: 6 segments, each 0x100 halfwords
@ - LANG_FLAG=0x02000000+0x6c2c // IWRAM language flag address
copy_card_medium_frame_to_obj_vram:
    push {r4,r5,r6,r7,lr}                    @ 080db910 f0b5
    .hword 0x4647    @ 080db912 4746
    push {r7}                                @ 080db914 80b4
    adds r4,r1,#0x0    @ 080db916 0c1c
    .hword 0x4690    @ 080db918 9046
    lsls r7,r2,#0x8    @ 080db91a 1702
    movs r2,#0xff    @ 080db91c ff22
    lsls r2,r2,#0x8    @ 080db91e 1202
    adds r1,r2,#0x0    @ 080db920 111c
    ands r7,r1    @ 080db922 0f40
    movs r2,#0xff    @ 080db924 ff22
    .hword 0x4641    @ 080db926 4146
    ands r1,r2    @ 080db928 1140
    orrs r7,r1    @ 080db92a 0f43
    ldr r6, PTR_card_image_index_080db990    @ 080db92c 184e
    lsls r2,r0,#0x1    @ 080db92e 4200
    movs r5,#0x0    @ 080db930 0025
    ldr r0, DAT_080db994                     @ 080db932 1848
    ldrh r0,[r0,#0x0]                        @ 080db934 0088
    lsrs r0,r0,#0x8    @ 080db936 000a
    cmp r0,#0x4a                             @ 080db938 4a28
    bne LAB_080db94c                         @ 080db93a 07d1
    ldr r1, DAT_080db998                     @ 080db93c 1649
    ldr r0, DAT_080db99c                     @ 080db93e 1748
    adds r1,r1,r0    @ 080db940 0918
    movs r0,#0x7    @ 080db942 0720
    ldrb r1,[r1,#0x0]                        @ 080db944 0978
    ands r0,r1    @ 080db946 0840
    cmp r0,#0x0                              @ 080db948 0028
    beq LAB_080db94e                         @ 080db94a 00d0
LAB_080db94c:
    movs r5,#0x1    @ 080db94c 0125
LAB_080db94e:
    orrs r2,r5    @ 080db94e 2a43
    lsls r0,r2,#0x1    @ 080db950 5000
    adds r0,r6,r0    @ 080db952 3018
    ldrh r2,[r0,#0x0]                        @ 080db954 0288
    lsls r1,r2,#0x1    @ 080db956 5100
    adds r1,r1,r2    @ 080db958 8918
    lsls r1,r1,#0x9    @ 080db95a 4902
    ldr r0, PTR_card_medium_frame_tile_data_080db9a0 @ 080db95c 1048
    adds r1,r1,r0    @ 080db95e 0918
    cmp r3,#0x0                              @ 080db960 002b
    bne LAB_080db9a8                         @ 080db962 21d1
    movs r2,#0xc0    @ 080db964 c022
    lsls r2,r2,#0x3    @ 080db966 d200
    adds r0,r4,#0x0    @ 080db968 201c
    bl copy_memory_dma3_with_cpu_fallback    @ 080db96a 19f0cdfa
    .hword 0x4640    @ 080db96e 4046
    cmp r0,#0x0                              @ 080db970 0028
    beq LAB_080db9f0                         @ 080db972 3dd0
    adds r1,r4,#0x0    @ 080db974 211c
    movs r2,#0x0    @ 080db976 0022
    ldr r3, DAT_080db9a4                     @ 080db978 0a4b
LAB_080db97a:
    ldrh r0,[r1,#0x0]                        @ 080db97a 0888
    cmp r0,#0x0                              @ 080db97c 0028
    beq LAB_080db984                         @ 080db97e 01d0
    adds r0,r7,r0    @ 080db980 3818
    strh r0,[r1,#0x0]                        @ 080db982 0880
LAB_080db984:
    adds r1,#0x2    @ 080db984 0231
    adds r2,#0x1    @ 080db986 0132
    cmp r2,r3                                @ 080db988 9a42
    bls LAB_080db97a                         @ 080db98a f6d9
    b LAB_080db9f0                           @ 080db98c 30e0
    .zero  0x2
PTR_card_image_index_080db990:
    .word  card_image_index               @ 080db990 005c5b09
DAT_080db994:
    .word  0x080000ae                     @ 080db994 ae000008
DAT_080db998:
    .word  0x02000000                     @ 080db998 00000002
DAT_080db99c:
    .word  0x00006c2c                     @ 080db99c 2c6c0000
PTR_card_medium_frame_tile_data_080db9a0:
    .word  card_medium_frame_tile_data    @ 080db9a0 80c0fb08
DAT_080db9a4:
    .word  0x000002ff                     @ 080db9a4 ff020000
LAB_080db9a8:
    adds r6,r1,#0x0    @ 080db9a8 0e1c
    movs r5,#0x0    @ 080db9aa 0025
LAB_080db9ac:
    adds r0,r4,#0x0    @ 080db9ac 201c
    adds r1,r6,#0x0    @ 080db9ae 311c
    movs r2,#0x80    @ 080db9b0 8022
    lsls r2,r2,#0x1    @ 080db9b2 5200
    bl copy_memory_dma3_with_cpu_fallback    @ 080db9b4 19f0a8fa
    .hword 0x4641    @ 080db9b8 4146
    cmp r1,#0x0                              @ 080db9ba 0029
    beq LAB_080db9dc                         @ 080db9bc 0ed0
    movs r2,#0x0    @ 080db9be 0022
    adds r1,r5,#0x1    @ 080db9c0 691c
LAB_080db9c2:
    ldrh r0,[r4,#0x0]                        @ 080db9c2 2088
    cmp r0,#0x0                              @ 080db9c4 0028
    beq LAB_080db9cc                         @ 080db9c6 01d0
    adds r0,r7,r0    @ 080db9c8 3818
    strh r0,[r4,#0x0]                        @ 080db9ca 2080
LAB_080db9cc:
    adds r4,#0x2    @ 080db9cc 0234
    adds r2,#0x1    @ 080db9ce 0132
    cmp r2,#0x7f                             @ 080db9d0 7f2a
    bls LAB_080db9c2                         @ 080db9d2 f6d9
    movs r2,#0xc0    @ 080db9d4 c022
    lsls r2,r2,#0x2    @ 080db9d6 9200
    adds r4,r4,r2    @ 080db9d8 a418
    b LAB_080db9e4                           @ 080db9da 03e0
LAB_080db9dc:
    movs r0,#0x80    @ 080db9dc 8020
    lsls r0,r0,#0x3    @ 080db9de c000
    adds r4,r4,r0    @ 080db9e0 2418
    adds r1,r5,#0x1    @ 080db9e2 691c
LAB_080db9e4:
    movs r2,#0x80    @ 080db9e4 8022
    lsls r2,r2,#0x1    @ 080db9e6 5200
    adds r6,r6,r2    @ 080db9e8 b618
    adds r5,r1,#0x0    @ 080db9ea 0d1c
    cmp r5,#0x5                              @ 080db9ec 052d
    bls LAB_080db9ac                         @ 080db9ee ddd9
LAB_080db9f0:
    pop {r3}                                 @ 080db9f0 08bc
    .hword 0x4698    @ 080db9f2 9846
    pop {r4,r5,r6,r7}                        @ 080db9f4 f0bc
    pop {r0}                                 @ 080db9f6 01bc
    bx r0                                    @ 080db9f8 0047
    .zero  0x2

@ Called during pack shop detail page init; sets BG3 parameters and decompresses graphic data from ROM. Writes 0x1f0f to BG3CNT (0x0400000e) (priority=3, charbase=block3=0xC000, 16-color, mapbase=block31=0xF800, 256x256). Clears BG3 tilemap (0x0600c000, 32 halfwords). Decompresses ROM[0x09cce2b0]->VRAM[0x0600c020] (tilemap) and ROM[0x09cce2d0]->VRAM[0x0600f800] (tile data) via bios_huff_uncomp. DMA copies palette ROM[0x09cce2c0]->BG palette[0x050001c0] (0x20 halfwords).
@ 
@ Constants:
@ - BG3CNT=0x0400000e // GBA BG3 control register
@ - BG3CNT_VAL=0x1f0f // priority=3, charbase=3, mapbase=31, 256x256
@ - TILEMAP_BASE=0x0600c000 // BG3 tilemap VRAM start
@ - TILE_BASE=0x0600f800 // BG3 tile data VRAM
@ - PALETTE_DST=0x050001c0 // BG palette destination (slot 14)
load_pack_detail_bg3_tileset:
    push {lr}                                @ 080db9fc 00b5
    ldr r1, PTR_BG3CNT_080dba30              @ 080db9fe 0c49
    ldr r0, DAT_080dba34                     @ 080dba00 0c48
    strh r0,[r1,#0x0]                        @ 080dba02 0880
    ldr r0, DAT_080dba38                     @ 080dba04 0c48
    movs r1,#0x20    @ 080dba06 2021
    bl zero_fill_halfword_wrapper            @ 080dba08 19f046fa
    ldr r0, DAT_080dba3c                     @ 080dba0c 0b48
    ldr r0,[r0,#0x0]                         @ 080dba0e 0068
    ldr r1, DAT_080dba40                     @ 080dba10 0b49
    bl bios_huff_uncomp                      @ 080dba12 32f001fd
    ldr r0, DAT_080dba44                     @ 080dba16 0b48
    ldr r0,[r0,#0x0]                         @ 080dba18 0068
    ldr r1, DAT_080dba48                     @ 080dba1a 0b49
    bl bios_huff_uncomp                      @ 080dba1c 32f0fcfc
    ldr r0, DAT_080dba4c                     @ 080dba20 0a48
    ldr r1, DAT_080dba50                     @ 080dba22 0b49
    ldr r1,[r1,#0x0]                         @ 080dba24 0968
    movs r2,#0x20    @ 080dba26 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dba28 19f06efa
    pop {r0}                                 @ 080dba2c 01bc
    bx r0                                    @ 080dba2e 0047
PTR_BG3CNT_080dba30:
    .word  BG3CNT                         @ 080dba30 0e000004
DAT_080dba34:
    .word  0x00001f0f                     @ 080dba34 0f1f0000
DAT_080dba38:
    .word  0x0600c000                     @ 080dba38 00c00006
DAT_080dba3c:
    .word  0x09cce2b0                     @ 080dba3c b0e2cc09
DAT_080dba40:
    .word  0x0600c020                     @ 080dba40 20c00006
DAT_080dba44:
    .word  0x09cce2d0                     @ 080dba44 d0e2cc09
DAT_080dba48:
    .word  0x0600f800                     @ 080dba48 00f80006
DAT_080dba4c:
    .word  0x050001c0                     @ 080dba4c c0010005
DAT_080dba50:
    .word  0x09cce2c0                     @ 080dba50 c0e2cc09
    .byte  0x00, 0xb5, 0x90, 0x21, 0x89, 0x00, 0x19, 0xf0, 0x1d, 0xfa, 0x01, 0xbc, 0x00, 0x47, 0x00, 0x00

@ Called in pack shop stat display area; renders the lifetime draw count stored at IWRAM[0x02006c38] (max 0x5f5e0ff=99,999,999) as digit graphics to sprite VRAM slot r0. Calls setup_line_buf_pos_and_font(9,2), configures [0x02006ed0] font state, calls render_decimal_digits_jp twice (two digit rows), queries stat label text via game_str_id_to_row(0x138f), renders via render_text_with_u16_width, then commit_line_buffer_to_sprite_vram(r0, 0) writes to VRAM.
@ 
@ Constants:
@ - DRAW_COUNT_ADDR=0x02006c38 // IWRAM lifetime draw total (pity counter)
@ - DRAW_COUNT_MAX=0x05f5e0ff // 99,999,999: display clamp
@ - STR_ID=0x138f // 5007: stat label string ID
@ - STATE_ADDR=0x02006ed0 // IWRAM font state struct base
render_pack_draw_counter_to_sprite_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dba64 f0b5
    .hword 0x4657    @ 080dba66 5746
    .hword 0x464e    @ 080dba68 4e46
    .hword 0x4645    @ 080dba6a 4546
    push {r5,r6,r7}                          @ 080dba6c e0b4
    adds r7,r0,#0x0    @ 080dba6e 071c
    ldr r5, DAT_080dbb54                     @ 080dba70 384d
    ldr r1, DAT_080dbb58                     @ 080dba72 3949
    adds r0,r5,r1    @ 080dba74 6818
    ldr r4,[r0,#0x0]                         @ 080dba76 0468
    ldr r0, DAT_080dbb5c                     @ 080dba78 3848
    cmp r4,r0                                @ 080dba7a 8442
    bls LAB_080dba80                         @ 080dba7c 00d9
    adds r4,r0,#0x0    @ 080dba7e 041c
LAB_080dba80:
    movs r0,#0x9    @ 080dba80 0920
    movs r1,#0x2    @ 080dba82 0221
    bl setup_line_buf_pos_and_font           @ 080dba84 15f096f8
    ldr r2, DAT_080dbb60                     @ 080dba88 354a
    movs r0,#0x2    @ 080dba8a 0220
    rsbs r0,r0,#0    @ 080dba8c 4042
    ldrb r3,[r2,#0x15]                       @ 080dba8e 537d
    ands r0,r3    @ 080dba90 1840
    strb r0,[r2,#0x15]                       @ 080dba92 5075
    movs r1,#0x2    @ 080dba94 0221
    ldrb r0,[r2,#0x8]                        @ 080dba96 107a
    orrs r1,r0    @ 080dba98 0143
    strb r1,[r2,#0x8]                        @ 080dba9a 1172
    movs r0,#0x7d    @ 080dba9c 7d20
    rsbs r0,r0,#0    @ 080dba9e 4042
    ldrb r3,[r2,#0x14]                       @ 080dbaa0 137d
    ands r0,r3    @ 080dbaa2 1840
    strb r0,[r2,#0x14]                       @ 080dbaa4 1075
    ldr r3, PTR_font_jp_base_table_080dbb64  @ 080dbaa6 2f4b
    lsls r0,r1,#0x1e    @ 080dbaa8 8807
    lsrs r0,r0,#0x1f    @ 080dbaaa c00f
    lsls r0,r0,#0x2    @ 080dbaac 8000
    lsls r1,r1,#0x1f    @ 080dbaae c907
    lsrs r1,r1,#0x1f    @ 080dbab0 c90f
    lsls r1,r1,#0x3    @ 080dbab2 c900
    adds r0,r0,r1    @ 080dbab4 4018
    adds r0,r0,r3    @ 080dbab6 c018
    ldr r0,[r0,#0x0]                         @ 080dbab8 0068
    str r0,[r2,#0x4]                         @ 080dbaba 5060
    ldr r0, DAT_080dbb68                     @ 080dbabc 2a48
    .hword 0x4681    @ 080dbabe 8146
    movs r0,#0x34    @ 080dbac0 3420
    movs r1,#0x3    @ 080dbac2 0321
    .hword 0x464a    @ 080dbac4 4a46
    adds r3,r4,#0x0    @ 080dbac6 231c
    bl render_decimal_digits_jp              @ 080dbac8 17f0e0f8
    ldr r1, DAT_080dbb6c                     @ 080dbacc 2749
    .hword 0x468a    @ 080dbace 8a46
    movs r0,#0x34    @ 080dbad0 3420
    movs r1,#0x3    @ 080dbad2 0321
    .hword 0x4652    @ 080dbad4 5246
    adds r3,r4,#0x0    @ 080dbad6 231c
    bl render_decimal_digits_jp              @ 080dbad8 17f0d8f8
    ldr r6, DAT_080dbb70                     @ 080dbadc 244e
    adds r0,r6,#0x0    @ 080dbade 301c
    bl game_str_id_to_row                    @ 080dbae0 19f09af9
    ldr r2, PTR_game_str_pointer_table_080dbb74 @ 080dbae4 234a
    .hword 0x4690    @ 080dbae6 9046
    lsls r0,r0,#0x10    @ 080dbae8 0004
    lsrs r0,r0,#0x10    @ 080dbaea 000c
    lsls r1,r0,#0x1    @ 080dbaec 4100
    adds r1,r1,r0    @ 080dbaee 0918
    lsls r1,r1,#0x1    @ 080dbaf0 4900
    ldr r3, DAT_080dbb78                     @ 080dbaf2 214b
    adds r5,r5,r3    @ 080dbaf4 ed18
    ldrb r2,[r5,#0x0]                        @ 080dbaf6 2a78
    lsls r0,r2,#0x1d    @ 080dbaf8 5007
    lsrs r0,r0,#0x1d    @ 080dbafa 400f
    adds r1,r1,r0    @ 080dbafc 0918
    lsls r1,r1,#0x2    @ 080dbafe 8900
    add r1,r8                                @ 080dbb00 4144
    ldr r3,[r1,#0x0]                         @ 080dbb02 0b68
    ldr r4, PTR_game_str_ja_080dbb7c         @ 080dbb04 1d4c
    adds r3,r3,r4    @ 080dbb06 1b19
    movs r0,#0x3a    @ 080dbb08 3a20
    movs r1,#0x3    @ 080dbb0a 0321
    .hword 0x464a    @ 080dbb0c 4a46
    bl render_text_with_u16_width            @ 080dbb0e 17f08df8
    adds r0,r6,#0x0    @ 080dbb12 301c
    bl game_str_id_to_row                    @ 080dbb14 19f080f9
    lsls r0,r0,#0x10    @ 080dbb18 0004
    lsrs r0,r0,#0x10    @ 080dbb1a 000c
    lsls r1,r0,#0x1    @ 080dbb1c 4100
    adds r1,r1,r0    @ 080dbb1e 0918
    lsls r1,r1,#0x1    @ 080dbb20 4900
    ldrb r5,[r5,#0x0]                        @ 080dbb22 2d78
    lsls r0,r5,#0x1d    @ 080dbb24 6807
    lsrs r0,r0,#0x1d    @ 080dbb26 400f
    adds r1,r1,r0    @ 080dbb28 0918
    lsls r1,r1,#0x2    @ 080dbb2a 8900
    add r1,r8                                @ 080dbb2c 4144
    ldr r3,[r1,#0x0]                         @ 080dbb2e 0b68
    adds r3,r3,r4    @ 080dbb30 1b19
    movs r0,#0x3a    @ 080dbb32 3a20
    movs r1,#0x3    @ 080dbb34 0321
    .hword 0x4652    @ 080dbb36 5246
    bl render_text_with_u16_width            @ 080dbb38 17f078f8
    adds r0,r7,#0x0    @ 080dbb3c 381c
    movs r1,#0x0    @ 080dbb3e 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dbb40 17f084f9
    pop {r3,r4,r5}                           @ 080dbb44 38bc
    .hword 0x4698    @ 080dbb46 9846
    .hword 0x46a1    @ 080dbb48 a146
    .hword 0x46aa    @ 080dbb4a aa46
    pop {r4,r5,r6,r7}                        @ 080dbb4c f0bc
    pop {r0}                                 @ 080dbb4e 01bc
    bx r0                                    @ 080dbb50 0047
    .zero  0x2
DAT_080dbb54:
    .word  0x02000000                     @ 080dbb54 00000002
DAT_080dbb58:
    .word  0x00006c38                     @ 080dbb58 386c0000
DAT_080dbb5c:
    .word  0x05f5e0ff                     @ 080dbb5c ffe0f505
DAT_080dbb60:
    .word  0x02006ed0                     @ 080dbb60 d06e0002
PTR_font_jp_base_table_080dbb64:
    .word  font_jp_base_table             @ 080dbb64 54f8e509
DAT_080dbb68:
    .word  0x00008108                     @ 080dbb68 08810000
DAT_080dbb6c:
    .word  0x00000107                     @ 080dbb6c 07010000
DAT_080dbb70:
    .word  0x0000138f                     @ 080dbb70 8f130000
PTR_game_str_pointer_table_080dbb74:
    .word  game_str_pointer_table         @ 080dbb74 400f0008
DAT_080dbb78:
    .word  0x00006c2c                     @ 080dbb78 2c6c0000
PTR_game_str_ja_080dbb7c:
    .word  game_str_ja                    @ 080dbb7c 109cdb09

@ Writes tile index sequence for pack name display region to OAM. r0=OAM dst ptr, r1=tile start index, r2=palette index (low 4 bits). Computes r5=(r2&0xf)<<12 as OAM attr2 palette field mask, then writes 2 rows x 9 tiles to OAM: outer loop 2 (rows), inner loop 9 (cols), each strh r5|r4 to [r3], r4 increments tile index; row gap 0x2e bytes between rows.
@ 
@ Constants:
@ - TILES_PER_ROW=9 // 9 tiles per row (inner loop 0..8)
@ - ROWS=2 // 2 rows (outer loop)
@ - ROW_GAP=0x2e // row end pointer skip (bytes)
@ - PAL_SHIFT=12 // palette index at attr2 bit[15:12]
write_pack_name_oam_tile_sequence:
    push {r4,r5,lr}                          @ 080dbb80 30b5
    adds r3,r0,#0x0    @ 080dbb82 031c
    adds r4,r1,#0x0    @ 080dbb84 0c1c
    lsls r2,r2,#0x1c    @ 080dbb86 1207
    lsrs r5,r2,#0x10    @ 080dbb88 150c
    movs r0,#0x0    @ 080dbb8a 0020
LAB_080dbb8c:
    movs r1,#0x0    @ 080dbb8c 0021
    adds r2,r0,#0x1    @ 080dbb8e 421c
LAB_080dbb90:
    adds r0,r5,#0x0    @ 080dbb90 281c
    orrs r0,r4    @ 080dbb92 2043
    strh r0,[r3,#0x0]                        @ 080dbb94 1880
    adds r4,#0x1    @ 080dbb96 0134
    adds r3,#0x2    @ 080dbb98 0233
    adds r1,#0x1    @ 080dbb9a 0131
    cmp r1,#0x8                              @ 080dbb9c 0829
    bls LAB_080dbb90                         @ 080dbb9e f7d9
    adds r3,#0x2e    @ 080dbba0 2e33
    adds r0,r2,#0x0    @ 080dbba2 101c
    cmp r0,#0x1                              @ 080dbba4 0128
    bls LAB_080dbb8c                         @ 080dbba6 f1d9
    pop {r4,r5}                              @ 080dbba8 30bc
    pop {r0}                                 @ 080dbbaa 01bc
    bx r0                                    @ 080dbbac 0047
    .zero  0x2

@ Zeros OBJ VRAM region specified by caller-set r0 via zero_fill_halfword_wrapper. No parameters; r1 is fixed at 0xc0<<4=0xc00 (0xc00 halfwords = 6 KB). Called before pack graphic switch to clear old graphic data and prevent visual artifacts.
@ 
@ Constants:
@ - ZERO_COUNT=0xc00 // 0xc0<<4: number of halfwords to zero (= 6 KB)
zero_fill_pack_obj_vram_region:
    push {lr}                                @ 080dbbb0 00b5
    movs r1,#0xc0    @ 080dbbb2 c021
    lsls r1,r1,#0x4    @ 080dbbb4 0901
    bl zero_fill_halfword_wrapper            @ 080dbbb6 19f06ff9
    pop {r0}                                 @ 080dbbba 01bc
    bx r0                                    @ 080dbbbc 0047
    .zero  0x2

@ pack-banner: ROM 0x09E5E2E8 查包名, text_render_wrapper x2
pack_name_text_render:
    push {r4,r5,r6,lr}                       @ 080dbbc0 70b5
    adds r6,r0,#0x0    @ 080dbbc2 061c
    ldr r0, PTR_pack_info_table_080dbc64     @ 080dbbc4 2748
    lsls r1,r1,#0x4    @ 080dbbc6 0901
    adds r1,r1,r0    @ 080dbbc8 0918
    ldrh r0,[r1,#0x6]                        @ 080dbbca c888
    bl game_str_id_to_row                    @ 080dbbcc 19f024f9
    ldr r2, PTR_game_str_pointer_table_080dbc68 @ 080dbbd0 254a
    lsls r0,r0,#0x10    @ 080dbbd2 0004
    lsrs r0,r0,#0x10    @ 080dbbd4 000c
    lsls r1,r0,#0x1    @ 080dbbd6 4100
    adds r1,r1,r0    @ 080dbbd8 0918
    lsls r1,r1,#0x1    @ 080dbbda 4900
    ldr r0, DAT_080dbc6c                     @ 080dbbdc 2348
    ldr r3, DAT_080dbc70                     @ 080dbbde 244b
    adds r0,r0,r3    @ 080dbbe0 c018
    ldrb r0,[r0,#0x0]                        @ 080dbbe2 0078
    lsls r0,r0,#0x1d    @ 080dbbe4 4007
    lsrs r0,r0,#0x1d    @ 080dbbe6 400f
    adds r1,r1,r0    @ 080dbbe8 0918
    lsls r1,r1,#0x2    @ 080dbbea 8900
    adds r1,r1,r2    @ 080dbbec 8918
    ldr r5,[r1,#0x0]                         @ 080dbbee 0d68
    ldr r0, PTR_game_str_ja_080dbc74         @ 080dbbf0 2048
    adds r5,r5,r0    @ 080dbbf2 2d18
    movs r0,#0x30    @ 080dbbf4 3020
    movs r1,#0x2    @ 080dbbf6 0221
    bl setup_line_buf_pos_and_font           @ 080dbbf8 14f0dcff
    ldr r2, DAT_080dbc78                     @ 080dbbfc 1e4a
    movs r0,#0x2    @ 080dbbfe 0220
    rsbs r0,r0,#0    @ 080dbc00 4042
    ldrb r1,[r2,#0x15]                       @ 080dbc02 517d
    ands r0,r1    @ 080dbc04 0840
    strb r0,[r2,#0x15]                       @ 080dbc06 5075
    movs r1,#0x2    @ 080dbc08 0221
    ldrb r3,[r2,#0x8]                        @ 080dbc0a 137a
    orrs r1,r3    @ 080dbc0c 1943
    strb r1,[r2,#0x8]                        @ 080dbc0e 1172
    movs r0,#0x7d    @ 080dbc10 7d20
    rsbs r0,r0,#0    @ 080dbc12 4042
    ldrb r3,[r2,#0x14]                       @ 080dbc14 137d
    ands r0,r3    @ 080dbc16 1840
    strb r0,[r2,#0x14]                       @ 080dbc18 1075
    ldr r3, PTR_font_jp_base_table_080dbc7c  @ 080dbc1a 184b
    lsls r0,r1,#0x1e    @ 080dbc1c 8807
    lsrs r0,r0,#0x1f    @ 080dbc1e c00f
    lsls r0,r0,#0x2    @ 080dbc20 8000
    lsls r1,r1,#0x1f    @ 080dbc22 c907
    lsrs r1,r1,#0x1f    @ 080dbc24 c90f
    lsls r1,r1,#0x3    @ 080dbc26 c900
    adds r0,r0,r1    @ 080dbc28 4018
    adds r0,r0,r3    @ 080dbc2a c018
    ldr r0,[r0,#0x0]                         @ 080dbc2c 0068
    str r0,[r2,#0x4]                         @ 080dbc2e 5060
    adds r0,r5,#0x0    @ 080dbc30 281c
    bl measure_string_pixel_width            @ 080dbc32 14f01ffb
    adds r4,r0,#0x0    @ 080dbc36 041c
    adds r4,#0x8    @ 080dbc38 0834
    asrs r4,r4,#0x3    @ 080dbc3a e410
    ldr r2, DAT_080dbc80                     @ 080dbc3c 104a
    movs r0,#0x1    @ 080dbc3e 0120
    movs r1,#0x2    @ 080dbc40 0221
    adds r3,r5,#0x0    @ 080dbc42 2b1c
    bl text_render_wrapper                   @ 080dbc44 16f01aff
    ldr r2, DAT_080dbc84                     @ 080dbc48 0e4a
    movs r0,#0x1    @ 080dbc4a 0120
    movs r1,#0x2    @ 080dbc4c 0221
    adds r3,r5,#0x0    @ 080dbc4e 2b1c
    bl text_render_wrapper                   @ 080dbc50 16f014ff
    adds r0,r6,#0x0    @ 080dbc54 301c
    movs r1,#0x0    @ 080dbc56 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dbc58 17f0f8f8
    adds r0,r4,#0x0    @ 080dbc5c 201c
    pop {r4,r5,r6}                           @ 080dbc5e 70bc
    pop {r1}                                 @ 080dbc60 02bc
    bx r1                                    @ 080dbc62 0847
PTR_pack_info_table_080dbc64:
    .word  pack_info_table                @ 080dbc64 e8e2e509
PTR_game_str_pointer_table_080dbc68:
    .word  game_str_pointer_table         @ 080dbc68 400f0008
DAT_080dbc6c:
    .word  0x02000000                     @ 080dbc6c 00000002
DAT_080dbc70:
    .word  0x00006c2c                     @ 080dbc70 2c6c0000
PTR_game_str_ja_080dbc74:
    .word  game_str_ja                    @ 080dbc74 109cdb09
DAT_080dbc78:
    .word  0x02006ed0                     @ 080dbc78 d06e0002
PTR_font_jp_base_table_080dbc7c:
    .word  font_jp_base_table             @ 080dbc7c 54f8e509
DAT_080dbc80:
    .word  0x00008108                     @ 080dbc80 08810000
DAT_080dbc84:
    .word  0x00000107                     @ 080dbc84 07010000

@ Writes a contiguous tile-index strip for pack graphics into OBJ VRAM. r0=dst_ptr, r1=start_tile, r2=palette_flags, r3=tile_row_base_offset. Shifts r2 left 0xc to get OBJ palette bank field. Computes column offset as start_tile % 0x30. Outer loop runs 2 iterations (2 strips), inner loop runs 0x20 iterations (32 tiles), writes strh tile index to [r4,#0], increments tile number and wraps at row end. Called by pack banner and pack detail VRAM fill paths.
@ 
@ Constants:
@ - STRIP_TILES=0x20 // 32 tiles per strip
@ - ROW_WIDTH=0x30 // 48: tile row width (OBJ VRAM 64x64 tile mode)
@ - PAL_SHIFT=0xc // r6 = r2<<0xc: OBJ attr2 palette bank field
write_pack_obj_tile_strip:
    push {r4,r5,r6,r7,lr}                    @ 080dbc88 f0b5
    .hword 0x464f    @ 080dbc8a 4f46
    .hword 0x4646    @ 080dbc8c 4646
    push {r6,r7}                             @ 080dbc8e c0b4
    adds r4,r0,#0x0    @ 080dbc90 041c
    .hword 0x4688    @ 080dbc92 8846
    .hword 0x4699    @ 080dbc94 9946
    lsls r2,r2,#0x1c    @ 080dbc96 1207
    lsrs r6,r2,#0x10    @ 080dbc98 160c
    .hword 0x4648    @ 080dbc9a 4846
    movs r1,#0x30    @ 080dbc9c 3021
    bl get_bios_div_remainder                @ 080dbc9e 32f0affb
    movs r2,#0x0    @ 080dbca2 0022
LAB_080dbca4:
    lsls r0,r2,#0x1    @ 080dbca4 5000
    adds r0,r0,r2    @ 080dbca6 8018
    lsls r0,r0,#0x4    @ 080dbca8 0001
    add r0,r9                                @ 080dbcaa 4844
    lsls r0,r0,#0x10    @ 080dbcac 0004
    lsrs r1,r0,#0x10    @ 080dbcae 010c
    movs r3,#0x0    @ 080dbcb0 0023
    adds r2,#0x1    @ 080dbcb2 0132
    lsls r0,r2,#0x1    @ 080dbcb4 5000
    adds r0,r0,r2    @ 080dbcb6 8018
    lsls r5,r0,#0x4    @ 080dbcb8 0501
LAB_080dbcba:
    .hword 0x4647    @ 080dbcba 4746
    adds r0,r1,r7    @ 080dbcbc c819
    orrs r0,r6    @ 080dbcbe 3043
    strh r0,[r4,#0x0]                        @ 080dbcc0 2080
    adds r0,r1,#0x1    @ 080dbcc2 481c
    lsls r0,r0,#0x10    @ 080dbcc4 0004
    lsrs r1,r0,#0x10    @ 080dbcc6 010c
    cmp r1,r5                                @ 080dbcc8 a942
    bne LAB_080dbcd4                         @ 080dbcca 03d1
    adds r0,r1,#0x0    @ 080dbccc 081c
    subs r0,#0x30    @ 080dbcce 3038
    lsls r0,r0,#0x10    @ 080dbcd0 0004
    lsrs r1,r0,#0x10    @ 080dbcd2 010c
LAB_080dbcd4:
    adds r4,#0x2    @ 080dbcd4 0234
    adds r3,#0x1    @ 080dbcd6 0133
    cmp r3,#0x1f                             @ 080dbcd8 1f2b
    bls LAB_080dbcba                         @ 080dbcda eed9
    cmp r2,#0x1                              @ 080dbcdc 012a
    bls LAB_080dbca4                         @ 080dbcde e1d9
    pop {r3,r4}                              @ 080dbce0 18bc
    .hword 0x4698    @ 080dbce2 9846
    .hword 0x46a1    @ 080dbce4 a146
    pop {r4,r5,r6,r7}                        @ 080dbce6 f0bc
    pop {r0}                                 @ 080dbce8 01bc
    bx r0                                    @ 080dbcea 0047

@ Identical function to zero_fill_pack_obj_vram_region (0x080dbbb0): calls zero_fill_halfword_wrapper(r0, 0xc00) to zero 6 KB of OBJ VRAM. Differs only in caller -- comes from FUN_080d4de4 (pack banner init function) which computes the pack banner OBJ VRAM region target address.
@ 
@ Constants:
@ - ZERO_COUNT=0xc00 // 0xc0<<4: number of halfwords to zero (= 6 KB)
zero_fill_pack_obj_vram_region_alt:
    push {lr}                                @ 080dbcec 00b5
    movs r1,#0xc0    @ 080dbcee c021
    lsls r1,r1,#0x4    @ 080dbcf0 0901
    bl zero_fill_halfword_wrapper            @ 080dbcf2 19f0d1f8
    pop {r0}                                 @ 080dbcf6 01bc
    bx r0                                    @ 080dbcf8 0047
    .zero  0x2

@ In pack shop card slot display, renders card name string to OBJ VRAM sprite line buffer and returns width in tiles. Caller selects VRAM target slot before calling; r0=VRAM dst, r1=card name string ptr, r2=render_mode. Calls select_charset_then_load_name for the string (charset from IWRAM language flag [0x02000000+0x6c2c]), then setup_line_buf_pos_and_font sets font context. Branches on r4(=r2): mode==0 renders color-0, mode==2 small text, mode==3 large text, mode>3 uses 0x100|r6 attr. Finally text_render_wrapper writes to line buffer, commit_line_buffer_to_sprite_vram flushes to VRAM. Returns r7 = (pixel_width+8)>>3 (tile width).
@ 
@ Constants:
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // charset/language flag
@ - FONT_CTX=0x02006ed0 // font context base
@ - OBJ_ATTR_BASE=0x00008108 // OBJ attribute constant
@ - TILE_WIDTH_SHIFT=3 // pixel->tile: (w+8)>>3
render_pack_card_name_to_sprite:
    push {r4,r5,r6,r7,lr}                    @ 080dbcfc f0b5
    .hword 0x464f    @ 080dbcfe 4f46
    .hword 0x4646    @ 080dbd00 4646
    push {r6,r7}                             @ 080dbd02 c0b4
    .hword 0x4680    @ 080dbd04 8046
    adds r0,r1,#0x0    @ 080dbd06 081c
    adds r4,r2,#0x0    @ 080dbd08 141c
    movs r6,#0x7    @ 080dbd0a 0726
    ldr r1, DAT_080dbd7c                     @ 080dbd0c 1b49
    ldr r2, DAT_080dbd80                     @ 080dbd0e 1c4a
    adds r1,r1,r2    @ 080dbd10 8918
    ldrb r1,[r1,#0x0]                        @ 080dbd12 0978
    lsls r1,r1,#0x1d    @ 080dbd14 4907
    lsrs r1,r1,#0x1d    @ 080dbd16 490f
    bl select_charset_then_load_name         @ 080dbd18 12f048fd
    adds r5,r0,#0x0    @ 080dbd1c 051c
    movs r0,#0x30    @ 080dbd1e 3020
    movs r1,#0x2    @ 080dbd20 0221
    bl setup_line_buf_pos_and_font           @ 080dbd22 14f047ff
    ldr r2, DAT_080dbd84                     @ 080dbd26 174a
    movs r0,#0x2    @ 080dbd28 0220
    rsbs r0,r0,#0    @ 080dbd2a 4042
    ldrb r3,[r2,#0x15]                       @ 080dbd2c 537d
    ands r0,r3    @ 080dbd2e 1840
    strb r0,[r2,#0x15]                       @ 080dbd30 5075
    movs r1,#0x2    @ 080dbd32 0221
    ldrb r0,[r2,#0x8]                        @ 080dbd34 107a
    orrs r1,r0    @ 080dbd36 0143
    strb r1,[r2,#0x8]                        @ 080dbd38 1172
    movs r0,#0x7d    @ 080dbd3a 7d20
    rsbs r0,r0,#0    @ 080dbd3c 4042
    ldrb r3,[r2,#0x14]                       @ 080dbd3e 137d
    ands r0,r3    @ 080dbd40 1840
    strb r0,[r2,#0x14]                       @ 080dbd42 1075
    ldr r3, PTR_font_jp_base_table_080dbd88  @ 080dbd44 104b
    lsls r0,r1,#0x1e    @ 080dbd46 8807
    lsrs r0,r0,#0x1f    @ 080dbd48 c00f
    lsls r0,r0,#0x2    @ 080dbd4a 8000
    lsls r1,r1,#0x1f    @ 080dbd4c c907
    lsrs r1,r1,#0x1f    @ 080dbd4e c90f
    lsls r1,r1,#0x3    @ 080dbd50 c900
    adds r0,r0,r1    @ 080dbd52 4018
    adds r0,r0,r3    @ 080dbd54 c018
    ldr r0,[r0,#0x0]                         @ 080dbd56 0068
    str r0,[r2,#0x4]                         @ 080dbd58 5060
    adds r0,r5,#0x0    @ 080dbd5a 281c
    bl measure_string_pixel_width            @ 080dbd5c 14f08afa
    adds r0,#0x8    @ 080dbd60 0830
    asrs r7,r0,#0x3    @ 080dbd62 c710
    cmp r4,#0x0                              @ 080dbd64 002c
    beq LAB_080dbd74                         @ 080dbd66 05d0
    ldr r2, DAT_080dbd8c                     @ 080dbd68 084a
    movs r0,#0x1    @ 080dbd6a 0120
    movs r1,#0x2    @ 080dbd6c 0221
    adds r3,r5,#0x0    @ 080dbd6e 2b1c
    bl text_render_wrapper                   @ 080dbd70 16f084fe
LAB_080dbd74:
    cmp r4,#0x2                              @ 080dbd74 022c
    bne LAB_080dbd90                         @ 080dbd76 0bd1
    movs r6,#0xd    @ 080dbd78 0d26
    b LAB_080dbd9e                           @ 080dbd7a 10e0
DAT_080dbd7c:
    .word  0x02000000                     @ 080dbd7c 00000002
DAT_080dbd80:
    .word  0x00006c2c                     @ 080dbd80 2c6c0000
DAT_080dbd84:
    .word  0x02006ed0                     @ 080dbd84 d06e0002
PTR_font_jp_base_table_080dbd88:
    .word  font_jp_base_table             @ 080dbd88 54f8e509
DAT_080dbd8c:
    .word  0x00008108                     @ 080dbd8c 08810000
LAB_080dbd90:
    cmp r4,#0x3                              @ 080dbd90 032c
    bne LAB_080dbd98                         @ 080dbd92 01d1
    movs r6,#0x9    @ 080dbd94 0926
    b LAB_080dbd9e                           @ 080dbd96 02e0
LAB_080dbd98:
    cmp r4,#0x3                              @ 080dbd98 032c
    bls LAB_080dbd9e                         @ 080dbd9a 00d9
    movs r6,#0xf    @ 080dbd9c 0f26
LAB_080dbd9e:
    movs r1,#0x80    @ 080dbd9e 8021
    lsls r1,r1,#0x1    @ 080dbda0 4900
    adds r0,r1,#0x0    @ 080dbda2 081c
    orrs r6,r0    @ 080dbda4 0643
    movs r0,#0x1    @ 080dbda6 0120
    movs r1,#0x2    @ 080dbda8 0221
    adds r2,r6,#0x0    @ 080dbdaa 321c
    adds r3,r5,#0x0    @ 080dbdac 2b1c
    bl text_render_wrapper                   @ 080dbdae 16f065fe
    .hword 0x4640    @ 080dbdb2 4046
    movs r1,#0x0    @ 080dbdb4 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dbdb6 17f049f8
    cmp r4,#0x3                              @ 080dbdba 032c
    bls LAB_080dbe00                         @ 080dbdbc 20d9
    .hword 0x4641    @ 080dbdbe 4146
    movs r2,#0x0    @ 080dbdc0 0022
    movs r0,#0x30    @ 080dbdc2 3020
    subs r0,r0,r7    @ 080dbdc4 c01b
    lsls r0,r0,#0x5    @ 080dbdc6 4001
    .hword 0x4684    @ 080dbdc8 8446
    ldr r3, DAT_080dbe10                     @ 080dbdca 114b
    .hword 0x4698    @ 080dbdcc 9846
LAB_080dbdce:
    movs r0,#0x0    @ 080dbdce 0020
    adds r2,#0x1    @ 080dbdd0 0132
    .hword 0x4691    @ 080dbdd2 9146
    cmp r0,r7                                @ 080dbdd4 b842
    bcs LAB_080dbdf8                         @ 080dbdd6 0fd2
    .hword 0x4645    @ 080dbdd8 4546
LAB_080dbdda:
    adds r3,r5,#0x0    @ 080dbdda 2b1c
    adds r4,r0,#0x1    @ 080dbddc 441c
    movs r2,#0xf    @ 080dbdde 0f22
LAB_080dbde0:
    ldrh r0,[r3,#0x0]                        @ 080dbde0 1888
    ldrh r6,[r1,#0x0]                        @ 080dbde2 0e88
    ands r0,r6    @ 080dbde4 3040
    strh r0,[r1,#0x0]                        @ 080dbde6 0880
    adds r1,#0x2    @ 080dbde8 0231
    adds r3,#0x2    @ 080dbdea 0233
    subs r2,#0x1    @ 080dbdec 013a
    cmp r2,#0x0                              @ 080dbdee 002a
    bge LAB_080dbde0                         @ 080dbdf0 f6da
    adds r0,r4,#0x0    @ 080dbdf2 201c
    cmp r0,r7                                @ 080dbdf4 b842
    bcc LAB_080dbdda                         @ 080dbdf6 f0d3
LAB_080dbdf8:
    add r1,r12                               @ 080dbdf8 6144
    .hword 0x464a    @ 080dbdfa 4a46
    cmp r2,#0x1                              @ 080dbdfc 012a
    ble LAB_080dbdce                         @ 080dbdfe e6dd
LAB_080dbe00:
    adds r0,r7,#0x0    @ 080dbe00 381c
    pop {r3,r4}                              @ 080dbe02 18bc
    .hword 0x4698    @ 080dbe04 9846
    .hword 0x46a1    @ 080dbe06 a146
    pop {r4,r5,r6,r7}                        @ 080dbe08 f0bc
    pop {r1}                                 @ 080dbe0a 02bc
    bx r1                                    @ 080dbe0c 0847
    .zero  0x2
DAT_080dbe10:
    .word  0x09e49538                     @ 080dbe10 3895e409

@ Writes palette-encoded tile attribute halfwords to a pack shop BG tile row buffer.
@ r0=VRAM dst, r1=base_attr, r2=packed_extra (high nibble=color_index encoded <<0x1c>>0x10), r3=extra_modifier.
@ Uses bios_div(0x30=48) to compute row offset; outer loop 0..1 (2 rows), inner loop 0..0x1f (32 cols), strh each entry.
@ Called by FUN_080d4de4 and FUN_080d4fa4 during pack shop init to fill card slot BG tile row data.
@ 
@ Constants:
@ - COLS=32 // inner loop cmp #0x1f bls -> 0..0x1f
@ - ROWS=2 // outer loop cmp #0x1 bls -> 0..1
@ - DIV_MOD=0x30 // bios_div divisor for row spacing offset
@ - COLOR_SHIFT=0x1c // palette bank encoding left-shift count
@ 
@ Inputs: r0=u16* dst_vram, r1=u16 base_attr, r2=u32 packed_extra, r3=u16 extra_modifier
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [dst_vram + 0..0x3f] written with tile attribute halfwords (2 rows x 32 cols)
fill_pack_bg_tile_row_with_palette:
    push {r4,r5,r6,r7,lr}                    @ 080dbe14 f0b5
    .hword 0x464f    @ 080dbe16 4f46
    .hword 0x4646    @ 080dbe18 4646
    push {r6,r7}                             @ 080dbe1a c0b4
    adds r4,r0,#0x0    @ 080dbe1c 041c
    .hword 0x4688    @ 080dbe1e 8846
    .hword 0x4699    @ 080dbe20 9946
    lsls r2,r2,#0x1c    @ 080dbe22 1207
    lsrs r6,r2,#0x10    @ 080dbe24 160c
    .hword 0x4648    @ 080dbe26 4846
    movs r1,#0x30    @ 080dbe28 3021
    bl get_bios_div_remainder                @ 080dbe2a 32f0e9fa
    movs r2,#0x0    @ 080dbe2e 0022
LAB_080dbe30:
    lsls r0,r2,#0x1    @ 080dbe30 5000
    adds r0,r0,r2    @ 080dbe32 8018
    lsls r0,r0,#0x4    @ 080dbe34 0001
    add r0,r9                                @ 080dbe36 4844
    lsls r0,r0,#0x10    @ 080dbe38 0004
    lsrs r1,r0,#0x10    @ 080dbe3a 010c
    movs r3,#0x0    @ 080dbe3c 0023
    adds r2,#0x1    @ 080dbe3e 0132
    lsls r0,r2,#0x1    @ 080dbe40 5000
    adds r0,r0,r2    @ 080dbe42 8018
    lsls r5,r0,#0x4    @ 080dbe44 0501
LAB_080dbe46:
    .hword 0x4647    @ 080dbe46 4746
    adds r0,r1,r7    @ 080dbe48 c819
    orrs r0,r6    @ 080dbe4a 3043
    strh r0,[r4,#0x0]                        @ 080dbe4c 2080
    adds r0,r1,#0x1    @ 080dbe4e 481c
    lsls r0,r0,#0x10    @ 080dbe50 0004
    lsrs r1,r0,#0x10    @ 080dbe52 010c
    cmp r1,r5                                @ 080dbe54 a942
    bne LAB_080dbe60                         @ 080dbe56 03d1
    adds r0,r1,#0x0    @ 080dbe58 081c
    subs r0,#0x30    @ 080dbe5a 3038
    lsls r0,r0,#0x10    @ 080dbe5c 0004
    lsrs r1,r0,#0x10    @ 080dbe5e 010c
LAB_080dbe60:
    adds r4,#0x2    @ 080dbe60 0234
    adds r3,#0x1    @ 080dbe62 0133
    cmp r3,#0x1f                             @ 080dbe64 1f2b
    bls LAB_080dbe46                         @ 080dbe66 eed9
    cmp r2,#0x1                              @ 080dbe68 012a
    bls LAB_080dbe30                         @ 080dbe6a e1d9
    pop {r3,r4}                              @ 080dbe6c 18bc
    .hword 0x4698    @ 080dbe6e 9846
    .hword 0x46a1    @ 080dbe70 a146
    pop {r4,r5,r6,r7}                        @ 080dbe72 f0bc
    pop {r0}                                 @ 080dbe74 01bc
    bx r0                                    @ 080dbe76 0047

@ Copies base palette from ROM 0x09ccd290, then generates 4 GBA RGB555 values at HSV hue steps (hue=0/0x2d/0x5a/0x87, sat=0xff, val=0xff), writing to dst+0x12/+0x14/+0x16/+0x18, then appends white 0x7fff at dst+0x1a. Called by pack_banner_080d566c (pack cover display) when initializing cover HSV gradient palette. Returns palette write end pointer (Sub-case E).
@ 
@ Constants:
@ ROM_PAL_BASE = 0x09ccd290
@ HUE_STEP_0   = 0x00
@ HUE_STEP_1   = 0x2d
@ HUE_STEP_2   = 0x5a
@ HUE_STEP_3   = 0x87
@ SAT_FULL     = 0xff
@ VAL_FULL     = 0xff
@ WHITE_RGB555 = 0x7fff
@ 
@ Params: r0=u16* dst_palette_ptr
@ Return: r0=u16* end_ptr (Sub-case E passthrough)
generate_hsv_palette_strip:
    push {r4,r5,lr}                          @ 080dbe78 30b5
    adds r4,r0,#0x0    @ 080dbe7a 041c
    ldr r1, DAT_080dbeb4                     @ 080dbe7c 0d49
    movs r2,#0x20    @ 080dbe7e 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dbe80 19f042f8
    adds r4,#0x12    @ 080dbe84 1234
    movs r5,#0x9    @ 080dbe86 0925
LAB_080dbe88:
    adds r1,r5,#0x0    @ 080dbe88 291c
    subs r1,#0x9    @ 080dbe8a 0939
    movs r0,#0xb4    @ 080dbe8c b420
    muls r0,r1    @ 080dbe8e 4843
    movs r1,#0x4    @ 080dbe90 0421
    bl bios_div                              @ 080dbe92 32f0b3fa
    movs r1,#0xff    @ 080dbe96 ff21
    movs r2,#0xff    @ 080dbe98 ff22
    bl convert_hsv_to_gba_rgb555             @ 080dbe9a 01f071fd
    strh r0,[r4,#0x0]                        @ 080dbe9e 2080
    adds r4,#0x2    @ 080dbea0 0234
    adds r5,#0x1    @ 080dbea2 0135
    cmp r5,#0xc                              @ 080dbea4 0c2d
    bls LAB_080dbe88                         @ 080dbea6 efd9
    ldr r1, DAT_080dbeb8                     @ 080dbea8 0349
    adds r0,r1,#0x0    @ 080dbeaa 081c
    strh r0,[r4,#0x0]                        @ 080dbeac 2080
    pop {r4,r5}                              @ 080dbeae 30bc
    pop {r0}                                 @ 080dbeb0 01bc
    bx r0                                    @ 080dbeb2 0047
DAT_080dbeb4:
    .word  0x09ccd290                     @ 080dbeb4 90d2cc09
DAT_080dbeb8:
    .word  0x00007fff                     @ 080dbeb8 ff7f0000

@ Generates a hue gradient strip for the pack scene cover palette. Writes to the palette buffer (r0, from offset +0x12), iterating 9..12 (4 times). Each iteration uses bios_div to map the index to hue H (uniformly distributed in 0..0xb4), then passes fixed S=0xff/V=0xff to convert_hsv_to_gba_rgb555 to produce a GBA RGB555 halfword. After the loop writes sentinel 0x7fff (white). Then computes a saturation compression factor from r1 (base hue/saturation input [0..0x168]): if r1 <= 0xb3 use forward bios_div, else reflect from 0x168-r1. Calls scale_pixel_saturation_in_buffer to apply per-pixel saturation scaling across the buffer. Called by tick_pack_name_scroll_strip_row0 (0x080d4fa4) on the cover HSV palette refresh path.
fill_pack_palette_hue_gradient:
    push {r4,r5,r6,lr}                       @ 080dbebc 70b5
    sub sp,#0x4                              @ 080dbebe 81b0
    adds r4,r0,#0x0    @ 080dbec0 041c
    adds r6,r1,#0x0    @ 080dbec2 0e1c
    adds r4,#0x12    @ 080dbec4 1234
    movs r5,#0x9    @ 080dbec6 0925
LAB_080dbec8:
    adds r1,r5,#0x0    @ 080dbec8 291c
    subs r1,#0x9    @ 080dbeca 0939
    movs r0,#0xb4    @ 080dbecc b420
    muls r0,r1    @ 080dbece 4843
    movs r1,#0x4    @ 080dbed0 0421
    bl bios_div                              @ 080dbed2 32f093fa
    adds r0,r6,r0    @ 080dbed6 3018
    movs r1,#0xb4    @ 080dbed8 b421
    lsls r1,r1,#0x1    @ 080dbeda 4900
    bl get_bios_div_remainder                @ 080dbedc 32f090fa
    movs r1,#0xff    @ 080dbee0 ff21
    movs r2,#0xff    @ 080dbee2 ff22
    bl convert_hsv_to_gba_rgb555             @ 080dbee4 01f04cfd
    strh r0,[r4,#0x0]                        @ 080dbee8 2080
    adds r4,#0x2    @ 080dbeea 0234
    adds r5,#0x1    @ 080dbeec 0135
    cmp r5,#0xc                              @ 080dbeee 0c2d
    bls LAB_080dbec8                         @ 080dbef0 ead9
    ldr r1, DAT_080dbf08                     @ 080dbef2 0549
    .hword 0x4668    @ 080dbef4 6846
    strh r1,[r0,#0x0]                        @ 080dbef6 0180
    cmp r6,#0xb3                             @ 080dbef8 b32e
    bgt LAB_080dbf0c                         @ 080dbefa 07dc
    lsls r0,r6,#0x7    @ 080dbefc f001
    movs r1,#0x80    @ 080dbefe 8021
    bl bios_div                              @ 080dbf00 32f07cfa
    b LAB_080dbf1a                           @ 080dbf04 09e0
    .zero  0x2
DAT_080dbf08:
    .word  0x00007fff                     @ 080dbf08 ff7f0000
LAB_080dbf0c:
    movs r0,#0xb4    @ 080dbf0c b420
    lsls r0,r0,#0x1    @ 080dbf0e 4000
    subs r0,r0,r6    @ 080dbf10 801b
    lsls r0,r0,#0x7    @ 080dbf12 c001
    movs r1,#0x80    @ 080dbf14 8021
    bl bios_div                              @ 080dbf16 32f071fa
LAB_080dbf1a:
    lsls r2,r0,#0x10    @ 080dbf1a 0204
    movs r0,#0x1    @ 080dbf1c 0120
    orrs r2,r0    @ 080dbf1e 0243
    .hword 0x4668    @ 080dbf20 6846
    adds r1,r4,#0x0    @ 080dbf22 211c
    bl scale_pixel_saturation_in_buffer      @ 080dbf24 01f01efe
    add sp,#0x4                              @ 080dbf28 01b0
    pop {r4,r5,r6}                           @ 080dbf2a 70bc
    pop {r0}                                 @ 080dbf2c 01bc
    bx r0                                    @ 080dbf2e 0047

@ Zeros the first OBJ VRAM row buffer group in the pack shop (0x340 halfwords = 0x680 bytes). Called by caller 0x080d4e8c on pack card slot init to clear the specified OBJ VRAM region before rendering. Function body: single bl zero_fill_halfword_wrapper with r1=0x340.
@ 
@ Constants:
@ - FILL_COUNT=0xd0<<2=0x340 // halfwords to zero per call
zero_fill_pack_obj_vram_row_a:
    push {lr}                                @ 080dbf30 00b5
    movs r1,#0xd0    @ 080dbf32 d021
    lsls r1,r1,#0x2    @ 080dbf34 8900
    bl zero_fill_halfword_wrapper            @ 080dbf36 18f0afff
    pop {r0}                                 @ 080dbf3a 01bc
    bx r0                                    @ 080dbf3c 0047
    .zero  0x2

@ Formats the pack name string for the given pack slot and renders it to the OBJ VRAM sprite line buffer.
@ r0=VRAM dst addr, r1=pack_index [0..4]. Uses game_str_id=0x13f9 to look up the pack name string via game_str_pointer_table; reads language flag at [0x02000000+0x6c2c] low 3 bits to select string branch. Reads pack_info_table[r1*16] halfword field as format parameter, calls expand_format_decimal_width_to_buf to format pack name width into stack buffer. Then calls setup_line_buf_pos_and_font + text_render_wrapper twice (two color layers) and finally commit_line_buffer_to_sprite_vram.
@ Called by FUN_080d4e8c (pack slot init path) and FUN_080d8e98 (pack slot refresh).
@ 
@ Constants:
@ - GAME_STR_ID=0x13f9 // pack name string ID
@ - PACK_INFO_STRIDE=0x10 // pack_info_table entry size
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language selection byte
@ - X_RALIGN_BASE=0x66 // right-align base x = 0x66 - pixel_width
@ - FONT_IDX=2
@ 
@ Inputs: r0=u16* dst_vram, r1=u8 pack_index [0..4]
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [OBJ VRAM via commit_line_buffer_to_sprite_vram]; [0x02006ed0+0x8/0x14] font control bytes updated
render_pack_label_name_to_sprite_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dbf40 f0b5
    .hword 0x4647    @ 080dbf42 4746
    push {r7}                                @ 080dbf44 80b4
    sub sp,#0x44                             @ 080dbf46 91b0
    .hword 0x4680    @ 080dbf48 8046
    adds r4,r1,#0x0    @ 080dbf4a 0c1c
    ldr r0, DAT_080dbf94                     @ 080dbf4c 1148
    bl game_str_id_to_row                    @ 080dbf4e 18f063ff
    ldr r2, PTR_game_str_pointer_table_080dbf98 @ 080dbf52 114a
    lsls r0,r0,#0x10    @ 080dbf54 0004
    lsrs r0,r0,#0x10    @ 080dbf56 000c
    lsls r1,r0,#0x1    @ 080dbf58 4100
    adds r1,r1,r0    @ 080dbf5a 0918
    lsls r1,r1,#0x1    @ 080dbf5c 4900
    ldr r0, DAT_080dbf9c                     @ 080dbf5e 0f48
    ldr r3, DAT_080dbfa0                     @ 080dbf60 0f4b
    adds r0,r0,r3    @ 080dbf62 c018
    ldrb r0,[r0,#0x0]                        @ 080dbf64 0078
    lsls r0,r0,#0x1d    @ 080dbf66 4007
    lsrs r0,r0,#0x1d    @ 080dbf68 400f
    adds r1,r1,r0    @ 080dbf6a 0918
    lsls r1,r1,#0x2    @ 080dbf6c 8900
    adds r1,r1,r2    @ 080dbf6e 8918
    ldr r1,[r1,#0x0]                         @ 080dbf70 0968
    ldr r0, PTR_game_str_ja_080dbfa4         @ 080dbf72 0c48
    adds r1,r1,r0    @ 080dbf74 0918
    ldr r0, PTR_pack_info_table_080dbfa8     @ 080dbf76 0c48
    lsls r4,r4,#0x4    @ 080dbf78 2401
    adds r4,r4,r0    @ 080dbf7a 2418
    ldrh r2,[r4,#0x0]                        @ 080dbf7c 2288
    movs r0,#0x1    @ 080dbf7e 0120
    str r0,[sp,#0x0]                         @ 080dbf80 0090
    add r0,sp,#0x4                           @ 080dbf82 01a8
    movs r3,#0x0    @ 080dbf84 0023
    bl expand_format_decimal_width_to_buf    @ 080dbf86 19f081f9
    movs r6,#0x0    @ 080dbf8a 0026
    ldr r5, DAT_080dbfac                     @ 080dbf8c 074d
    ldr r7, PTR_font_jp_base_table_080dbfb0  @ 080dbf8e 084f
    b LAB_080dbfb8                           @ 080dbf90 12e0
    .zero  0x2
DAT_080dbf94:
    .word  0x000013f9                     @ 080dbf94 f9130000
PTR_game_str_pointer_table_080dbf98:
    .word  game_str_pointer_table         @ 080dbf98 400f0008
DAT_080dbf9c:
    .word  0x02000000                     @ 080dbf9c 00000002
DAT_080dbfa0:
    .word  0x00006c2c                     @ 080dbfa0 2c6c0000
PTR_game_str_ja_080dbfa4:
    .word  game_str_ja                    @ 080dbfa4 109cdb09
PTR_pack_info_table_080dbfa8:
    .word  pack_info_table                @ 080dbfa8 e8e2e509
DAT_080dbfac:
    .word  0x02006ed0                     @ 080dbfac d06e0002
PTR_font_jp_base_table_080dbfb0:
    .word  font_jp_base_table             @ 080dbfb0 54f8e509
LAB_080dbfb4:
    cmp r6,#0x0                              @ 080dbfb4 002e
    beq LAB_080dc014                         @ 080dbfb6 2dd0
LAB_080dbfb8:
    movs r0,#0x0    @ 080dbfb8 0020
    cmp r6,#0x0                              @ 080dbfba 002e
    bne LAB_080dbfc0                         @ 080dbfbc 00d1
    movs r0,#0x1    @ 080dbfbe 0120
LAB_080dbfc0:
    adds r6,r0,#0x0    @ 080dbfc0 061c
    movs r0,#0xd    @ 080dbfc2 0d20
    movs r1,#0x2    @ 080dbfc4 0221
    bl setup_line_buf_pos_and_font           @ 080dbfc6 14f0f5fd
    movs r1,#0x2    @ 080dbfca 0221
    rsbs r1,r1,#0    @ 080dbfcc 4942
    adds r0,r1,#0x0    @ 080dbfce 081c
    ldrb r2,[r5,#0x15]                       @ 080dbfd0 6a7d
    ands r0,r2    @ 080dbfd2 1040
    strb r0,[r5,#0x15]                       @ 080dbfd4 6875
    lsls r0,r6,#0x1    @ 080dbfd6 7000
    movs r3,#0x3    @ 080dbfd8 0323
    rsbs r3,r3,#0    @ 080dbfda 5b42
    adds r1,r3,#0x0    @ 080dbfdc 191c
    ldrb r2,[r5,#0x8]                        @ 080dbfde 2a7a
    ands r1,r2    @ 080dbfe0 1140
    orrs r1,r0    @ 080dbfe2 0143
    strb r1,[r5,#0x8]                        @ 080dbfe4 2972
    subs r3,#0x7a    @ 080dbfe6 7a3b
    adds r0,r3,#0x0    @ 080dbfe8 181c
    ldrb r2,[r5,#0x14]                       @ 080dbfea 2a7d
    ands r0,r2    @ 080dbfec 1040
    strb r0,[r5,#0x14]                       @ 080dbfee 2875
    lsls r0,r1,#0x1e    @ 080dbff0 8807
    lsrs r0,r0,#0x1f    @ 080dbff2 c00f
    lsls r0,r0,#0x2    @ 080dbff4 8000
    lsls r1,r1,#0x1f    @ 080dbff6 c907
    lsrs r1,r1,#0x1f    @ 080dbff8 c90f
    lsls r1,r1,#0x3    @ 080dbffa c900
    adds r0,r0,r1    @ 080dbffc 4018
    adds r0,r0,r7    @ 080dbffe c019
    ldr r0,[r0,#0x0]                         @ 080dc000 0068
    str r0,[r5,#0x4]                         @ 080dc002 6860
    add r0,sp,#0x4                           @ 080dc004 01a8
    bl measure_string_pixel_width            @ 080dc006 14f035f9
    movs r1,#0x66    @ 080dc00a 6621
    subs r1,r1,r0    @ 080dc00c 091a
    asrs r4,r1,#0x1    @ 080dc00e 4c10
    cmp r4,#0x0                              @ 080dc010 002c
    blt LAB_080dbfb4                         @ 080dc012 cfdb
LAB_080dc014:
    movs r3,#0x80    @ 080dc014 8023
    rsbs r3,r3,#0    @ 080dc016 5b42
    adds r0,r3,#0x0    @ 080dc018 181c
    adds r2,r6,#0x0    @ 080dc01a 321c
    orrs r2,r0    @ 080dc01c 0243
    lsls r2,r2,#0x18    @ 080dc01e 1206
    lsrs r2,r2,#0x10    @ 080dc020 120c
    movs r0,#0x8    @ 080dc022 0820
    orrs r2,r0    @ 080dc024 0243
    adds r0,r4,#0x0    @ 080dc026 201c
    movs r1,#0x3    @ 080dc028 0321
    add r3,sp,#0x4                           @ 080dc02a 01ab
    bl text_render_wrapper                   @ 080dc02c 16f026fd
    lsls r0,r6,#0x18    @ 080dc030 3006
    movs r2,#0xe0    @ 080dc032 e022
    lsls r2,r2,#0xb    @ 080dc034 d202
    orrs r2,r0    @ 080dc036 0243
    lsrs r2,r2,#0x10    @ 080dc038 120c
    adds r0,r4,#0x0    @ 080dc03a 201c
    movs r1,#0x3    @ 080dc03c 0321
    add r3,sp,#0x4                           @ 080dc03e 01ab
    bl text_render_wrapper                   @ 080dc040 16f01cfd
    .hword 0x4640    @ 080dc044 4046
    movs r1,#0x0    @ 080dc046 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dc048 16f000ff
    add sp,#0x44                             @ 080dc04c 11b0
    pop {r3}                                 @ 080dc04e 08bc
    .hword 0x4698    @ 080dc050 9846
    pop {r4,r5,r6,r7}                        @ 080dc052 f0bc
    pop {r0}                                 @ 080dc054 01bc
    bx r0                                    @ 080dc056 0047

@ Writes 2 rows x 13 cols of halfword tile attribute data to pack shop OBJ VRAM. Called by pack slot init; r0=VRAM dst, r1=base_attr, r2=color_index. Extracts r2 low 4 bits, shifts to OBJ palette bank encoding (<<0x1c>>0x10), then writes 2x13 halfwords (inner loop cmp #0xc bls; outer loop cmp #0x1 bls), row skip 0x26 bytes.
@ 
@ Constants:
@ - COLS=13 // inner loop 0..12 (13 columns)
@ - ROWS=2 // outer loop 0..1 (2 rows)
@ - ROW_SKIP=0x26 // row inter-stride bytes
@ - COLOR_SHIFT=0x1c // palette bank encoding shift
fill_pack_obj_tile_region_13col:
    push {r4,r5,lr}                          @ 080dc058 30b5
    adds r3,r0,#0x0    @ 080dc05a 031c
    adds r4,r1,#0x0    @ 080dc05c 0c1c
    lsls r2,r2,#0x1c    @ 080dc05e 1207
    lsrs r5,r2,#0x10    @ 080dc060 150c
    movs r0,#0x0    @ 080dc062 0020
LAB_080dc064:
    movs r1,#0x0    @ 080dc064 0021
    adds r2,r0,#0x1    @ 080dc066 421c
LAB_080dc068:
    adds r0,r5,#0x0    @ 080dc068 281c
    orrs r0,r4    @ 080dc06a 2043
    strh r0,[r3,#0x0]                        @ 080dc06c 1880
    adds r4,#0x1    @ 080dc06e 0134
    adds r3,#0x2    @ 080dc070 0233
    adds r1,#0x1    @ 080dc072 0131
    cmp r1,#0xc                              @ 080dc074 0c29
    bls LAB_080dc068                         @ 080dc076 f7d9
    adds r3,#0x26    @ 080dc078 2633
    adds r0,r2,#0x0    @ 080dc07a 101c
    cmp r0,#0x1                              @ 080dc07c 0128
    bls LAB_080dc064                         @ 080dc07e f1d9
    pop {r4,r5}                              @ 080dc080 30bc
    pop {r0}                                 @ 080dc082 01bc
    bx r0                                    @ 080dc084 0047
    .zero  0x2

@ Zeros the second OBJ VRAM row buffer group in the pack shop (0x340 halfwords = 0x680 bytes). Called by caller 0x080d4e48 on pack slot second-path init to clear the target OBJ VRAM region. Structure is fully symmetric to zero_fill_pack_obj_vram_row_a (0x080dbf30), differing only in caller.
@ 
@ Constants:
@ - FILL_COUNT=0xd0<<2=0x340 // halfwords to zero
zero_fill_pack_obj_vram_row_b:
    push {lr}                                @ 080dc088 00b5
    movs r1,#0xd0    @ 080dc08a d021
    lsls r1,r1,#0x2    @ 080dc08c 8900
    bl zero_fill_halfword_wrapper            @ 080dc08e 18f003ff
    pop {r0}                                 @ 080dc092 01bc
    bx r0                                    @ 080dc094 0047
    .zero  0x2

@ Formats the owned card count percentage for the given pack slot and renders it to the OBJ VRAM sprite line buffer.
@ r0=VRAM dst addr, r1=pack_index [0..4], r2=selected_count [0..total_count] (owned card count).
@ Uses game_str_id=0x13ee format string; calls get_pack_total_card_count(r1) to get total_count; computes selected_count/total_count*100 clamped to [1..99] or 100 (full collection).
@ Calls expand_format_decimal_width_to_buf, then setup_line_buf_pos_and_font + text_render_wrapper twice, finally commit_line_buffer_to_sprite_vram.
@ Called by FUN_080d4e48 and FUN_080d8e98.
@ 
@ Constants:
@ - GAME_STR_ID=0x13ee // pack card count format string ID
@ - PCT_MAX=0x64=100 // percentage upper limit
@ - PCT_MIN=1 // percentage lower limit (at least 1%)
@ - PCT_FULL=0x64=100 // displayed when all cards owned or total==0
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language selection byte
@ - FONT_IDX=2
@ 
@ Inputs: r0=u16* dst_vram, r1=u8 pack_index [0..4], r2=u16 selected_count [0..total_count]
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [OBJ VRAM via commit_line_buffer_to_sprite_vram]; [0x02006ed0+0x8/0x14/0x15] font control bytes
render_pack_card_count_to_sprite_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dc098 f0b5
    .hword 0x4647    @ 080dc09a 4746
    push {r7}                                @ 080dc09c 80b4
    sub sp,#0x44                             @ 080dc09e 91b0
    .hword 0x4680    @ 080dc0a0 8046
    adds r4,r1,#0x0    @ 080dc0a2 0c1c
    adds r5,r2,#0x0    @ 080dc0a4 151c
    ldr r0, DAT_080dc0e8                     @ 080dc0a6 1048
    bl game_str_id_to_row                    @ 080dc0a8 18f0b6fe
    ldr r2, PTR_game_str_pointer_table_080dc0ec @ 080dc0ac 0f4a
    lsls r0,r0,#0x10    @ 080dc0ae 0004
    lsrs r0,r0,#0x10    @ 080dc0b0 000c
    lsls r1,r0,#0x1    @ 080dc0b2 4100
    adds r1,r1,r0    @ 080dc0b4 0918
    lsls r1,r1,#0x1    @ 080dc0b6 4900
    ldr r0, DAT_080dc0f0                     @ 080dc0b8 0d48
    ldr r3, DAT_080dc0f4                     @ 080dc0ba 0e4b
    adds r0,r0,r3    @ 080dc0bc c018
    ldrb r0,[r0,#0x0]                        @ 080dc0be 0078
    lsls r0,r0,#0x1d    @ 080dc0c0 4007
    lsrs r0,r0,#0x1d    @ 080dc0c2 400f
    adds r1,r1,r0    @ 080dc0c4 0918
    lsls r1,r1,#0x2    @ 080dc0c6 8900
    adds r1,r1,r2    @ 080dc0c8 8918
    ldr r1,[r1,#0x0]                         @ 080dc0ca 0968
    ldr r0, PTR_game_str_ja_080dc0f8         @ 080dc0cc 0a48
    adds r6,r1,r0    @ 080dc0ce 0e18
    movs r7,#0x1    @ 080dc0d0 0127
    adds r0,r4,#0x0    @ 080dc0d2 201c
    bl get_pack_total_card_count             @ 080dc0d4 fef7d2fe
    lsls r0,r0,#0x10    @ 080dc0d8 0004
    lsrs r1,r0,#0x10    @ 080dc0da 010c
    cmp r5,r1                                @ 080dc0dc 8d42
    beq LAB_080dc118                         @ 080dc0de 1bd0
    cmp r5,#0x0                              @ 080dc0e0 002d
    bne LAB_080dc0fc                         @ 080dc0e2 0bd1
    movs r2,#0x0    @ 080dc0e4 0022
    b LAB_080dc11a                           @ 080dc0e6 18e0
DAT_080dc0e8:
    .word  0x000013ee                     @ 080dc0e8 ee130000
PTR_game_str_pointer_table_080dc0ec:
    .word  game_str_pointer_table         @ 080dc0ec 400f0008
DAT_080dc0f0:
    .word  0x02000000                     @ 080dc0f0 00000002
DAT_080dc0f4:
    .word  0x00006c2c                     @ 080dc0f4 2c6c0000
PTR_game_str_ja_080dc0f8:
    .word  game_str_ja                    @ 080dc0f8 109cdb09
LAB_080dc0fc:
    cmp r1,#0x0                              @ 080dc0fc 0029
    beq LAB_080dc118                         @ 080dc0fe 0bd0
    movs r0,#0x64    @ 080dc100 6420
    muls r0,r5    @ 080dc102 6843
    bl bios_div                              @ 080dc104 32f07af9
    adds r2,r0,#0x0    @ 080dc108 021c
    cmp r2,#0x1                              @ 080dc10a 012a
    bcs LAB_080dc110                         @ 080dc10c 00d2
    movs r2,#0x1    @ 080dc10e 0122
LAB_080dc110:
    cmp r2,#0x63                             @ 080dc110 632a
    bls LAB_080dc11a                         @ 080dc112 02d9
    movs r2,#0x63    @ 080dc114 6322
    b LAB_080dc11a                           @ 080dc116 00e0
LAB_080dc118:
    movs r2,#0x64    @ 080dc118 6422
LAB_080dc11a:
    movs r0,#0x1    @ 080dc11a 0120
    str r0,[sp,#0x0]                         @ 080dc11c 0090
    add r0,sp,#0x4                           @ 080dc11e 01a8
    adds r1,r6,#0x0    @ 080dc120 311c
    movs r3,#0x0    @ 080dc122 0023
    bl expand_format_decimal_width_to_buf    @ 080dc124 19f0b2f8
    movs r0,#0xd    @ 080dc128 0d20
    movs r1,#0x2    @ 080dc12a 0221
    bl setup_line_buf_pos_and_font           @ 080dc12c 14f042fd
    ldr r2, DAT_080dc1b0                     @ 080dc130 1f4a
    movs r0,#0x2    @ 080dc132 0220
    rsbs r0,r0,#0    @ 080dc134 4042
    ldrb r1,[r2,#0x15]                       @ 080dc136 517d
    ands r0,r1    @ 080dc138 0840
    strb r0,[r2,#0x15]                       @ 080dc13a 5075
    lsls r0,r7,#0x1    @ 080dc13c 7800
    movs r1,#0x3    @ 080dc13e 0321
    rsbs r1,r1,#0    @ 080dc140 4942
    ldrb r3,[r2,#0x8]                        @ 080dc142 137a
    ands r1,r3    @ 080dc144 1940
    orrs r1,r0    @ 080dc146 0143
    strb r1,[r2,#0x8]                        @ 080dc148 1172
    movs r0,#0x7d    @ 080dc14a 7d20
    rsbs r0,r0,#0    @ 080dc14c 4042
    ldrb r3,[r2,#0x14]                       @ 080dc14e 137d
    ands r0,r3    @ 080dc150 1840
    strb r0,[r2,#0x14]                       @ 080dc152 1075
    ldr r3, PTR_font_jp_base_table_080dc1b4  @ 080dc154 174b
    lsls r0,r1,#0x1e    @ 080dc156 8807
    lsrs r0,r0,#0x1f    @ 080dc158 c00f
    lsls r0,r0,#0x2    @ 080dc15a 8000
    lsls r1,r1,#0x1f    @ 080dc15c c907
    lsrs r1,r1,#0x1f    @ 080dc15e c90f
    lsls r1,r1,#0x3    @ 080dc160 c900
    adds r0,r0,r1    @ 080dc162 4018
    adds r0,r0,r3    @ 080dc164 c018
    ldr r0,[r0,#0x0]                         @ 080dc166 0068
    str r0,[r2,#0x4]                         @ 080dc168 5060
    add r0,sp,#0x4                           @ 080dc16a 01a8
    bl measure_string_pixel_width            @ 080dc16c 14f082f8
    movs r4,#0x66    @ 080dc170 6624
    subs r4,r4,r0    @ 080dc172 241a
    lsrs r4,r4,#0x1    @ 080dc174 6408
    movs r0,#0x80    @ 080dc176 8020
    adds r2,r7,#0x0    @ 080dc178 3a1c
    orrs r2,r0    @ 080dc17a 0243
    lsls r2,r2,#0x8    @ 080dc17c 1202
    movs r0,#0x8    @ 080dc17e 0820
    orrs r2,r0    @ 080dc180 0243
    adds r0,r4,#0x0    @ 080dc182 201c
    movs r1,#0x3    @ 080dc184 0321
    add r3,sp,#0x4                           @ 080dc186 01ab
    bl text_render_wrapper                   @ 080dc188 16f078fc
    lsls r2,r7,#0x8    @ 080dc18c 3a02
    movs r0,#0x7    @ 080dc18e 0720
    orrs r2,r0    @ 080dc190 0243
    adds r0,r4,#0x0    @ 080dc192 201c
    movs r1,#0x3    @ 080dc194 0321
    add r3,sp,#0x4                           @ 080dc196 01ab
    bl text_render_wrapper                   @ 080dc198 16f070fc
    .hword 0x4640    @ 080dc19c 4046
    movs r1,#0x0    @ 080dc19e 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dc1a0 16f054fe
    add sp,#0x44                             @ 080dc1a4 11b0
    pop {r3}                                 @ 080dc1a6 08bc
    .hword 0x4698    @ 080dc1a8 9846
    pop {r4,r5,r6,r7}                        @ 080dc1aa f0bc
    pop {r0}                                 @ 080dc1ac 01bc
    bx r0                                    @ 080dc1ae 0047
DAT_080dc1b0:
    .word  0x02006ed0                     @ 080dc1b0 d06e0002
PTR_font_jp_base_table_080dc1b4:
    .word  font_jp_base_table             @ 080dc1b4 54f8e509

@ Writes 2 rows x 13 cols of halfword tile attributes to pack shop second OBJ VRAM slot. Called by caller 0x080d4e48; r0=VRAM dst, r1=base_attr, r2=color_index. Structure fully symmetric to fill_pack_obj_tile_region_13col (0x080dc058): same double loop (outer 2 rows, inner 13 cols), same color_index shift encoding (<<0x1c >>0x10), same row_skip=0x26. Differs only in caller-supplied VRAM target address.
@ 
@ Constants:
@ - COLS=13 // inner loop cmp #0xc bls -> 13
@ - ROWS=2 // outer loop cmp #0x1 bls -> 2
@ - ROW_SKIP=0x26 // row stride bytes
@ - COLOR_SHIFT=0x1c // palette bank encoding shift
fill_pack_obj_tile_region_13col_b:
    push {r4,r5,lr}                          @ 080dc1b8 30b5
    adds r3,r0,#0x0    @ 080dc1ba 031c
    adds r4,r1,#0x0    @ 080dc1bc 0c1c
    lsls r2,r2,#0x1c    @ 080dc1be 1207
    lsrs r5,r2,#0x10    @ 080dc1c0 150c
    movs r0,#0x0    @ 080dc1c2 0020
LAB_080dc1c4:
    movs r1,#0x0    @ 080dc1c4 0021
    adds r2,r0,#0x1    @ 080dc1c6 421c
LAB_080dc1c8:
    adds r0,r5,#0x0    @ 080dc1c8 281c
    orrs r0,r4    @ 080dc1ca 2043
    strh r0,[r3,#0x0]                        @ 080dc1cc 1880
    adds r4,#0x1    @ 080dc1ce 0134
    adds r3,#0x2    @ 080dc1d0 0233
    adds r1,#0x1    @ 080dc1d2 0131
    cmp r1,#0xc                              @ 080dc1d4 0c29
    bls LAB_080dc1c8                         @ 080dc1d6 f7d9
    adds r3,#0x26    @ 080dc1d8 2633
    adds r0,r2,#0x0    @ 080dc1da 101c
    cmp r0,#0x1                              @ 080dc1dc 0128
    bls LAB_080dc1c4                         @ 080dc1de f1d9
    pop {r4,r5}                              @ 080dc1e0 30bc
    pop {r0}                                 @ 080dc1e2 01bc
    bx r0                                    @ 080dc1e4 0047
    .zero  0x2

@ Zeros pack info page OBJ VRAM large region (0x440 halfwords = 0x880 bytes). Called by caller 0x080d715c when switching pack info page; clears corresponding OBJ VRAM region to remove previous frame residual. Function body: r1=0x88<<3=0x440, bl zero_fill_halfword_wrapper, void return.
@ 
@ Constants:
@ - FILL_COUNT=0x88<<3=0x440 // halfwords to zero (= 0x880 bytes)
zero_fill_pack_info_obj_vram:
    push {lr}                                @ 080dc1e8 00b5
    movs r1,#0x88    @ 080dc1ea 8821
    lsls r1,r1,#0x3    @ 080dc1ec c900
    bl zero_fill_halfword_wrapper            @ 080dc1ee 18f053fe
    pop {r0}                                 @ 080dc1f2 01bc
    bx r0                                    @ 080dc1f4 0047
    .zero  0x2

@ Formats pack card stat byte as text and renders it right-aligned to OBJ VRAM sprite line buffer. Called by pack info page (callers game_str_080d715c and game_str_080d90f8) when displaying card stat info. Uses game_str_id=0x13ef for first string row and 0x138f for suffix; reads stat byte from pack_ui_state+0x18, calls format_decimal_byte_to_buf, appends suffix via append_text_to_buf_end, sets up font at x=0x11, renders main and second color layers via text_render_wrapper, then right-aligns at x=0x82-pixel_width with two more renders; finally commit_line_buffer_to_sprite_vram outputs to r10's OBJ VRAM address.
@ 
@ Constants:
@ - GAME_STR_ID_VALUE=0x13ef // stat value format string ID
@ - GAME_STR_ID_SUFFIX=0x138f // suffix string ID
@ - X_OFFSET=0x11 // render start x
@ - X_RALIGN_BASE=0x82 // right-align base: x = 0x82 - pixel_width
@ - FONT_IDX=2
render_pack_card_stat_byte_to_sprite:
    push {r4,r5,r6,lr}                       @ 080dc1f8 70b5
    .hword 0x4656    @ 080dc1fa 5646
    .hword 0x464d    @ 080dc1fc 4d46
    .hword 0x4644    @ 080dc1fe 4446
    push {r4,r5,r6}                          @ 080dc200 70b4
    sub sp,#0x60                             @ 080dc202 98b0
    .hword 0x4682    @ 080dc204 8246
    ldr r5, DAT_080dc300                     @ 080dc206 3e4d
    adds r5,#0xc    @ 080dc208 0c35
    ldr r0, DAT_080dc304                     @ 080dc20a 3e48
    bl game_str_id_to_row                    @ 080dc20c 18f004fe
    ldr r1, PTR_game_str_pointer_table_080dc308 @ 080dc210 3d49
    .hword 0x4689    @ 080dc212 8946
    lsls r0,r0,#0x10    @ 080dc214 0004
    lsrs r0,r0,#0x10    @ 080dc216 000c
    lsls r1,r0,#0x1    @ 080dc218 4100
    adds r1,r1,r0    @ 080dc21a 0918
    lsls r1,r1,#0x1    @ 080dc21c 4900
    ldr r4, DAT_080dc30c                     @ 080dc21e 3b4c
    ldr r2, DAT_080dc310                     @ 080dc220 3b4a
    adds r4,r4,r2    @ 080dc222 a418
    ldrb r3,[r4,#0x0]                        @ 080dc224 2378
    lsls r0,r3,#0x1d    @ 080dc226 5807
    lsrs r0,r0,#0x1d    @ 080dc228 400f
    adds r1,r1,r0    @ 080dc22a 0918
    lsls r1,r1,#0x2    @ 080dc22c 8900
    add r1,r9                                @ 080dc22e 4944
    ldr r1,[r1,#0x0]                         @ 080dc230 0968
    .hword 0x4688    @ 080dc232 8846
    ldr r6, PTR_game_str_ja_080dc314         @ 080dc234 374e
    add r8,r6                                @ 080dc236 b044
    ldr r0, DAT_080dc318                     @ 080dc238 3748
    bl game_str_id_to_row                    @ 080dc23a 18f0edfd
    lsls r0,r0,#0x10    @ 080dc23e 0004
    lsrs r0,r0,#0x10    @ 080dc240 000c
    lsls r1,r0,#0x1    @ 080dc242 4100
    adds r1,r1,r0    @ 080dc244 0918
    lsls r1,r1,#0x1    @ 080dc246 4900
    ldrb r4,[r4,#0x0]                        @ 080dc248 2478
    lsls r0,r4,#0x1d    @ 080dc24a 6007
    lsrs r0,r0,#0x1d    @ 080dc24c 400f
    adds r1,r1,r0    @ 080dc24e 0918
    lsls r1,r1,#0x2    @ 080dc250 8900
    add r1,r9                                @ 080dc252 4944
    ldr r4,[r1,#0x0]                         @ 080dc254 0c68
    adds r4,r4,r6    @ 080dc256 a419
    .hword 0x4669    @ 080dc258 6946
    movs r0,#0x0    @ 080dc25a 0020
    strb r0,[r1,#0x0]                        @ 080dc25c 0870
    ldr r1,[r5,#0xc]                         @ 080dc25e e968
    .hword 0x4668    @ 080dc260 6846
    bl format_decimal_byte_to_buf            @ 080dc262 18f045ff
    .hword 0x4668    @ 080dc266 6846
    adds r1,r4,#0x0    @ 080dc268 211c
    bl append_text_to_buf_end                @ 080dc26a 18f0fffe
    movs r0,#0x11    @ 080dc26e 1120
    movs r1,#0x2    @ 080dc270 0221
    bl setup_line_buf_pos_and_font           @ 080dc272 14f09ffc
    ldr r2, DAT_080dc31c                     @ 080dc276 294a
    movs r0,#0x2    @ 080dc278 0220
    rsbs r0,r0,#0    @ 080dc27a 4042
    ldrb r1,[r2,#0x15]                       @ 080dc27c 517d
    ands r0,r1    @ 080dc27e 0840
    strb r0,[r2,#0x15]                       @ 080dc280 5075
    movs r1,#0x2    @ 080dc282 0221
    ldrb r3,[r2,#0x8]                        @ 080dc284 137a
    orrs r1,r3    @ 080dc286 1943
    strb r1,[r2,#0x8]                        @ 080dc288 1172
    movs r0,#0x7d    @ 080dc28a 7d20
    rsbs r0,r0,#0    @ 080dc28c 4042
    ldrb r3,[r2,#0x14]                       @ 080dc28e 137d
    ands r0,r3    @ 080dc290 1840
    strb r0,[r2,#0x14]                       @ 080dc292 1075
    ldr r3, PTR_font_jp_base_table_080dc320  @ 080dc294 224b
    lsls r0,r1,#0x1e    @ 080dc296 8807
    lsrs r0,r0,#0x1f    @ 080dc298 c00f
    lsls r0,r0,#0x2    @ 080dc29a 8000
    lsls r1,r1,#0x1f    @ 080dc29c c907
    lsrs r1,r1,#0x1f    @ 080dc29e c90f
    lsls r1,r1,#0x3    @ 080dc2a0 c900
    adds r0,r0,r1    @ 080dc2a2 4018
    adds r0,r0,r3    @ 080dc2a4 c018
    ldr r0,[r0,#0x0]                         @ 080dc2a6 0068
    str r0,[r2,#0x4]                         @ 080dc2a8 5060
    ldr r6, DAT_080dc324                     @ 080dc2aa 1e4e
    movs r0,#0x2    @ 080dc2ac 0220
    movs r1,#0x3    @ 080dc2ae 0321
    adds r2,r6,#0x0    @ 080dc2b0 321c
    .hword 0x4643    @ 080dc2b2 4346
    bl text_render_wrapper                   @ 080dc2b4 16f0e2fb
    ldr r5, DAT_080dc328                     @ 080dc2b8 1b4d
    movs r0,#0x2    @ 080dc2ba 0220
    movs r1,#0x3    @ 080dc2bc 0321
    adds r2,r5,#0x0    @ 080dc2be 2a1c
    .hword 0x4643    @ 080dc2c0 4346
    bl text_render_wrapper                   @ 080dc2c2 16f0dbfb
    .hword 0x4668    @ 080dc2c6 6846
    bl measure_string_pixel_width            @ 080dc2c8 13f0d4ff
    movs r4,#0x82    @ 080dc2cc 8224
    subs r4,r4,r0    @ 080dc2ce 241a
    adds r0,r4,#0x0    @ 080dc2d0 201c
    movs r1,#0x3    @ 080dc2d2 0321
    adds r2,r6,#0x0    @ 080dc2d4 321c
    .hword 0x466b    @ 080dc2d6 6b46
    bl text_render_wrapper                   @ 080dc2d8 16f0d0fb
    adds r0,r4,#0x0    @ 080dc2dc 201c
    movs r1,#0x3    @ 080dc2de 0321
    adds r2,r5,#0x0    @ 080dc2e0 2a1c
    .hword 0x466b    @ 080dc2e2 6b46
    bl text_render_wrapper                   @ 080dc2e4 16f0cafb
    .hword 0x4650    @ 080dc2e8 5046
    movs r1,#0x0    @ 080dc2ea 0021
    bl commit_line_buffer_to_sprite_vram     @ 080dc2ec 16f0aefd
    add sp,#0x60                             @ 080dc2f0 18b0
    pop {r3,r4,r5}                           @ 080dc2f2 38bc
    .hword 0x4698    @ 080dc2f4 9846
    .hword 0x46a1    @ 080dc2f6 a146
    .hword 0x46aa    @ 080dc2f8 aa46
    pop {r4,r5,r6}                           @ 080dc2fa 70bc
    pop {r0}                                 @ 080dc2fc 01bc
    bx r0                                    @ 080dc2fe 0047
DAT_080dc300:
    .word  pack_ui_state                  @ 080dc300 50580003
DAT_080dc304:
    .word  0x000013ef                     @ 080dc304 ef130000
PTR_game_str_pointer_table_080dc308:
    .word  game_str_pointer_table         @ 080dc308 400f0008
DAT_080dc30c:
    .word  0x02000000                     @ 080dc30c 00000002
DAT_080dc310:
    .word  0x00006c2c                     @ 080dc310 2c6c0000
PTR_game_str_ja_080dc314:
    .word  game_str_ja                    @ 080dc314 109cdb09
DAT_080dc318:
    .word  0x0000138f                     @ 080dc318 8f130000
DAT_080dc31c:
    .word  0x02006ed0                     @ 080dc31c d06e0002
PTR_font_jp_base_table_080dc320:
    .word  font_jp_base_table             @ 080dc320 54f8e509
DAT_080dc324:
    .word  0x00008108                     @ 080dc324 08810000
DAT_080dc328:
    .word  0x00000107                     @ 080dc328 07010000

@ Writes 2 rows x 17 cols of halfword tile attributes to pack shop OBJ VRAM. Called by FUN_080d71bc during pack info page OBJ layout init; r0=VRAM dst, r1=base_attr, r2=color_index. Structure symmetric to fill_pack_obj_tile_region_13col but different column count (inner loop cmp #0x10 bls -> 17 cols) and row skip (adds r3,#0x1e).
@ 
@ Constants:
@ - COLS=17 // inner loop cmp #0x10 bls -> 17 cols [0..16]
@ - ROWS=2 // outer loop cmp #0x1 bls -> 2 rows [0..1]
@ - ROW_SKIP=0x1e // row inter-stride bytes
@ - COLOR_SHIFT=0x1c // palette bank encoding shift
fill_pack_obj_tile_region_17col:
    push {r4,r5,lr}                          @ 080dc32c 30b5
    adds r3,r0,#0x0    @ 080dc32e 031c
    adds r4,r1,#0x0    @ 080dc330 0c1c
    lsls r2,r2,#0x1c    @ 080dc332 1207
    lsrs r5,r2,#0x10    @ 080dc334 150c
    movs r0,#0x0    @ 080dc336 0020
LAB_080dc338:
    movs r1,#0x0    @ 080dc338 0021
    adds r2,r0,#0x1    @ 080dc33a 421c
LAB_080dc33c:
    adds r0,r5,#0x0    @ 080dc33c 281c
    orrs r0,r4    @ 080dc33e 2043
    strh r0,[r3,#0x0]                        @ 080dc340 1880
    adds r4,#0x1    @ 080dc342 0134
    adds r3,#0x2    @ 080dc344 0233
    adds r1,#0x1    @ 080dc346 0131
    cmp r1,#0x10                             @ 080dc348 1029
    bls LAB_080dc33c                         @ 080dc34a f7d9
    adds r3,#0x1e    @ 080dc34c 1e33
    adds r0,r2,#0x0    @ 080dc34e 101c
    cmp r0,#0x1                              @ 080dc350 0128
    bls LAB_080dc338                         @ 080dc352 f1d9
    pop {r4,r5}                              @ 080dc354 30bc
    pop {r0}                                 @ 080dc356 01bc
    bx r0                                    @ 080dc358 0047
    .zero  0x2

@ Writes 2 rows x 17 cols of palette-bank-encoded halfword tile region to specified VRAM address (leaf function, no push/pop). Only caller FUN_080d71bc on pack info page init, r0==1 branch calls this. r1 is encoded via lsls r1,r1,#0x1c; lsrs r1,r1,#0x10, then written as fixed halfword value; r2 at entry is immediately overwritten by movs r2,#0x0 (local row counter, not APCS parameter). Symmetric to fill_pack_obj_tile_region_17col (0x080dc32c).
@ 
@ Constants:
@ - COLS=17 // inner loop cmp #0x10 bls -> [0..16]
@ - ROWS=2 // outer loop cmp #0x1 bls -> [0..1]
@ - ROW_SKIP=0x1e // row inter-stride bytes
fill_pack_obj_tile_row_17col_leaf:
    lsls r1,r1,#0x1c    @ 080dc35c 0907
    lsrs r1,r1,#0x10    @ 080dc35e 090c
    movs r3,#0x0    @ 080dc360 0023
LAB_080dc362:
    movs r2,#0x0    @ 080dc362 0022
    adds r3,#0x1    @ 080dc364 0133
LAB_080dc366:
    strh r1,[r0,#0x0]                        @ 080dc366 0180
    adds r0,#0x2    @ 080dc368 0230
    adds r2,#0x1    @ 080dc36a 0132
    cmp r2,#0x10                             @ 080dc36c 102a
    bls LAB_080dc366                         @ 080dc36e fad9
    adds r0,#0x1e    @ 080dc370 1e30
    cmp r3,#0x1                              @ 080dc372 012b
    bls LAB_080dc362                         @ 080dc374 f5d9
    bx lr                                    @ 080dc376 7047

@ Copies card tile row data from ROM to pack shop OBJ VRAM at specified slot, and optionally copies the palette. r0=card_slot_index (VRAM offset r0<<5, written to 0x06010000+r0*32), r1=pal_slot_index. Calls tile_2d_row_copy (4x2 tiles) with tile ptr from ROM_TILE_TABLE[+0x8]; if r1<=0xf, DMA copies ROM palette [0x09ce824c+0x8] (0x20 bytes) to 0x05000200+r1*0x20.
@ 
@ Constants:
@ - OBJ_VRAM_BASE=0x06010000 // OBJ tile VRAM base
@ - ROM_TILE_TABLE=0x09ce822c // ROM card tile pointer table
@ - ROM_PAL_TABLE=0x09ce824c // ROM card palette table
@ - OBJ_PAL_BASE=0x05000200 // OBJ palette VRAM base
@ - PAL_LIMIT=0xf // r1 > 0xf skips palette copy
load_pack_card_tile_row_to_obj_vram:
    push {r4,lr}                             @ 080dc378 10b5
    adds r4,r1,#0x0    @ 080dc37a 0c1c
    lsls r0,r0,#0x5    @ 080dc37c 4001
    ldr r1, DAT_080dc3a8                     @ 080dc37e 0a49
    adds r0,r0,r1    @ 080dc380 4018
    ldr r1, DAT_080dc3ac                     @ 080dc382 0a49
    ldr r1,[r1,#0x8]                         @ 080dc384 8968
    movs r2,#0x4    @ 080dc386 0422
    movs r3,#0x2    @ 080dc388 0223
    bl tile_2d_row_copy                      @ 080dc38a 1bf0a3f8
    cmp r4,#0xf                              @ 080dc38e 0f2c
    bhi LAB_080dc3a2                         @ 080dc390 07d8
    lsls r0,r4,#0x5    @ 080dc392 6001
    ldr r1, DAT_080dc3b0                     @ 080dc394 0649
    adds r0,r0,r1    @ 080dc396 4018
    ldr r1, DAT_080dc3b4                     @ 080dc398 0649
    ldr r1,[r1,#0x8]                         @ 080dc39a 8968
    movs r2,#0x20    @ 080dc39c 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc39e 18f0b3fd
LAB_080dc3a2:
    pop {r4}                                 @ 080dc3a2 10bc
    pop {r0}                                 @ 080dc3a4 01bc
    bx r0                                    @ 080dc3a6 0047
DAT_080dc3a8:
    .word  0x06010000                     @ 080dc3a8 00000106
DAT_080dc3ac:
    .word  0x09ce822c                     @ 080dc3ac 2c82ce09
DAT_080dc3b0:
    .word  0x05000200                     @ 080dc3b0 00020005
DAT_080dc3b4:
    .word  0x09ce824c                     @ 080dc3b4 4c82ce09

@ Copies card tile row data (second field offset) from ROM to pack shop OBJ VRAM slot, optionally copying palette. Only caller pack_list_page_init (0x080d971c). Structure fully symmetric to load_pack_card_tile_row_to_obj_vram (0x080dc378); differs only in ROM pointer table offset [r1,#0x10] (vs #0x8), and tile_2d_row_copy parameters 2x2 (vs 4x2).
@ 
@ Constants:
@ - OBJ_VRAM_BASE=0x06010000
@ - ROM_TILE_TABLE=0x09ce822c // offset +0x10 = second field
@ - ROM_PAL_TABLE=0x09ce824c // offset +0x10
@ - OBJ_PAL_BASE=0x05000200
@ - PAL_LIMIT=0xf
load_pack_card_tile_row_to_obj_vram_b:
    push {r4,lr}                             @ 080dc3b8 10b5
    adds r4,r1,#0x0    @ 080dc3ba 0c1c
    lsls r0,r0,#0x5    @ 080dc3bc 4001
    ldr r1, DAT_080dc3e8                     @ 080dc3be 0a49
    adds r0,r0,r1    @ 080dc3c0 4018
    ldr r1, DAT_080dc3ec                     @ 080dc3c2 0a49
    ldr r1,[r1,#0x10]                        @ 080dc3c4 0969
    movs r2,#0x2    @ 080dc3c6 0222
    movs r3,#0x2    @ 080dc3c8 0223
    bl tile_2d_row_copy                      @ 080dc3ca 1bf083f8
    cmp r4,#0xf                              @ 080dc3ce 0f2c
    bhi LAB_080dc3e2                         @ 080dc3d0 07d8
    lsls r0,r4,#0x5    @ 080dc3d2 6001
    ldr r1, DAT_080dc3f0                     @ 080dc3d4 0649
    adds r0,r0,r1    @ 080dc3d6 4018
    ldr r1, DAT_080dc3f4                     @ 080dc3d8 0649
    ldr r1,[r1,#0x10]                        @ 080dc3da 0969
    movs r2,#0x20    @ 080dc3dc 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc3de 18f093fd
LAB_080dc3e2:
    pop {r4}                                 @ 080dc3e2 10bc
    pop {r0}                                 @ 080dc3e4 01bc
    bx r0                                    @ 080dc3e6 0047
DAT_080dc3e8:
    .word  0x06010000                     @ 080dc3e8 00000106
DAT_080dc3ec:
    .word  0x09ce822c                     @ 080dc3ec 2c82ce09
DAT_080dc3f0:
    .word  0x05000200                     @ 080dc3f0 00020005
DAT_080dc3f4:
    .word  0x09ce824c                     @ 080dc3f4 4c82ce09

@ Copies card tile row data (third field offset) from ROM to pack shop OBJ VRAM slot, optionally copying palette. Only caller FUN_080d733c (pack banner page render). Structure symmetric to siblings; reads offset [r1,#0xc] (third field), tile_2d_row_copy parameters 4x4 tiles.
@ 
@ Constants:
@ - OBJ_VRAM_BASE=0x06010000
@ - ROM_TILE_TABLE=0x09ce822c // offset +0xc = third field
@ - ROM_PAL_TABLE=0x09ce824c // offset +0xc
@ - OBJ_PAL_BASE=0x05000200
@ - PAL_LIMIT=0xf
load_pack_card_tile_row_to_obj_vram_c:
    push {r4,lr}                             @ 080dc3f8 10b5
    adds r4,r1,#0x0    @ 080dc3fa 0c1c
    lsls r0,r0,#0x5    @ 080dc3fc 4001
    ldr r1, DAT_080dc428                     @ 080dc3fe 0a49
    adds r0,r0,r1    @ 080dc400 4018
    ldr r1, DAT_080dc42c                     @ 080dc402 0a49
    ldr r1,[r1,#0xc]                         @ 080dc404 c968
    movs r2,#0x4    @ 080dc406 0422
    movs r3,#0x4    @ 080dc408 0423
    bl tile_2d_row_copy                      @ 080dc40a 1bf063f8
    cmp r4,#0xf                              @ 080dc40e 0f2c
    bhi LAB_080dc422                         @ 080dc410 07d8
    lsls r0,r4,#0x5    @ 080dc412 6001
    ldr r1, DAT_080dc430                     @ 080dc414 0649
    adds r0,r0,r1    @ 080dc416 4018
    ldr r1, DAT_080dc434                     @ 080dc418 0649
    ldr r1,[r1,#0xc]                         @ 080dc41a c968
    movs r2,#0x20    @ 080dc41c 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc41e 18f073fd
LAB_080dc422:
    pop {r4}                                 @ 080dc422 10bc
    pop {r0}                                 @ 080dc424 01bc
    bx r0                                    @ 080dc426 0047
DAT_080dc428:
    .word  0x06010000                     @ 080dc428 00000106
DAT_080dc42c:
    .word  0x09ce822c                     @ 080dc42c 2c82ce09
DAT_080dc430:
    .word  0x05000200                     @ 080dc430 00020005
DAT_080dc434:
    .word  0x09ce824c                     @ 080dc434 4c82ce09

@ Batch copies tile data for 3 cards from ROM to OBJ VRAM, optionally copying palette. Only caller pack_list_page_init (0x080d971c); r0=ptr to array of 3 OBJ attr halfwords, r1=sprite_col_index. Loops 3 times (r5 0..2): reads OBJ attr halfword, *0x20 for VRAM offset, fetches ROM tile ptr from [0x09ce822c+0x14]+r5*0x80, calls tile_2d_row_copy(2x2). After loop, if r6<=0xf DMA copies palette from [0x09ce824c+0x14] to 0x05000200+r6*0x20.
@ 
@ Constants:
@ - ROM_TILE_TABLE=0x09ce822c // offset +0x14 = fourth field
@ - ROM_PAL_TABLE=0x09ce824c // offset +0x14
@ - OBJ_VRAM_BASE=0x06010000
@ - OBJ_PAL_BASE=0x05000200
@ - CARD_COUNT=3 // loop cmp r5,#2 bls -> [0..2]
@ - TILE_SLOT_STRIDE=0x80 // per-card tile slot interval
load_pack_multi_card_tiles_to_obj_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dc438 f0b5
    adds r6,r1,#0x0    @ 080dc43a 0e1c
    movs r5,#0x0    @ 080dc43c 0025
    ldr r7, DAT_080dc47c                     @ 080dc43e 0f4f
    adds r4,r0,#0x0    @ 080dc440 041c
LAB_080dc442:
    ldrh r1,[r4,#0x0]                        @ 080dc442 2188
    lsls r0,r1,#0x5    @ 080dc444 4801
    ldr r1, DAT_080dc480                     @ 080dc446 0e49
    adds r0,r0,r1    @ 080dc448 4018
    lsls r2,r5,#0x7    @ 080dc44a ea01
    ldr r1,[r7,#0x14]                        @ 080dc44c 7969
    adds r1,r1,r2    @ 080dc44e 8918
    movs r2,#0x2    @ 080dc450 0222
    movs r3,#0x2    @ 080dc452 0223
    bl tile_2d_row_copy                      @ 080dc454 1bf03ef8
    adds r4,#0x2    @ 080dc458 0234
    adds r5,#0x1    @ 080dc45a 0135
    cmp r5,#0x2                              @ 080dc45c 022d
    bls LAB_080dc442                         @ 080dc45e f0d9
    cmp r6,#0xf                              @ 080dc460 0f2e
    bhi LAB_080dc474                         @ 080dc462 07d8
    lsls r0,r6,#0x5    @ 080dc464 7001
    ldr r1, DAT_080dc484                     @ 080dc466 0749
    adds r0,r0,r1    @ 080dc468 4018
    ldr r1, DAT_080dc488                     @ 080dc46a 0749
    ldr r1,[r1,#0x14]                        @ 080dc46c 4969
    movs r2,#0x20    @ 080dc46e 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc470 18f04afd
LAB_080dc474:
    pop {r4,r5,r6,r7}                        @ 080dc474 f0bc
    pop {r0}                                 @ 080dc476 01bc
    bx r0                                    @ 080dc478 0047
    .zero  0x2
DAT_080dc47c:
    .word  0x09ce822c                     @ 080dc47c 2c82ce09
DAT_080dc480:
    .word  0x06010000                     @ 080dc480 00000106
DAT_080dc484:
    .word  0x05000200                     @ 080dc484 00020005
DAT_080dc488:
    .word  0x09ce824c                     @ 080dc488 4c82ce09

@ Maps card animation type code to pack_ui_state AOB (animation object) context variant and initializes it. Only caller FUN_080d5318 (scene_pack) on card slot anim init; r0=type_code (1/2/other), r1=aob_ctx_ptr (from pack_ui_state+0x70c), r2=anm_entry_id. Maps type_code to anm_variant (0 for type=1, 1 for type=2, 2 for other), then calls init_aob_ctx_with_anm_entry(r0=aob_ctx_ptr, r1=anm_variant, r2=0).
@ 
@ Constants:
@ - TYPE_1->anm_variant=0
@ - TYPE_2->anm_variant=1
@ - TYPE_OTHER->anm_variant=2
@ - PACK_UI_STATE_AOB_OFFSET=0x70c // pack_ui_state AOB ctx offset
dispatch_pack_card_aob_by_type:
    push {lr}                                @ 080dc48c 00b5
    adds r2,r1,#0x0    @ 080dc48e 0a1c
    cmp r0,#0x1                              @ 080dc490 0128
    beq LAB_080dc49c                         @ 080dc492 03d0
    cmp r0,#0x2                              @ 080dc494 0228
    beq LAB_080dc4a0                         @ 080dc496 03d0
    movs r1,#0x2    @ 080dc498 0221
    b LAB_080dc4a2                           @ 080dc49a 02e0
LAB_080dc49c:
    movs r1,#0x0    @ 080dc49c 0021
    b LAB_080dc4a2                           @ 080dc49e 00e0
LAB_080dc4a0:
    movs r1,#0x1    @ 080dc4a0 0121
LAB_080dc4a2:
    adds r0,r2,#0x0    @ 080dc4a2 101c
    movs r2,#0x0    @ 080dc4a4 0022
    bl init_aob_ctx_with_anm_entry           @ 080dc4a6 1bf0cffc
    pop {r0}                                 @ 080dc4aa 01bc
    bx r0                                    @ 080dc4ac 0047
    .zero  0x2

@ Initializes pack shop card slot AOB (animation object) context from ROM pattern section data and sets attribute flags. Only caller FUN_080d50e4 (scene_pack) on pack home init; r0=sprite_id (u16, written to AOB ctx +0x10), r1=anm_variant, r2=aob_ctx_ptr. Fetches ROM ptnsect ptr from 0x09ce826c+0x1c, calls init_aob_ctx_from_ptnsect; then clears bits[2:1] of [aob_ctx_ptr+0x13] and sets bit1 (mode=1), writes sprite_id to [aob_ctx_ptr+0x10].
@ 
@ Constants:
@ - ROM_PTNSECT_TABLE=0x09ce826c // offset +0x1c = AOB ptnsect ptr
@ - ATTR_CLEAR_MASK=~0x6 // clear bits[2:1]
@ - ATTR_MODE_BIT=0x2 // bit1 = mode flag
init_pack_card_slot_aob_from_ptn:
    push {r4,r5,lr}                          @ 080dc4b0 30b5
    adds r5,r0,#0x0    @ 080dc4b2 051c
    adds r4,r2,#0x0    @ 080dc4b4 141c
    ldr r0, DAT_080dc4e8                     @ 080dc4b6 0c48
    ldr r3,[r0,#0x1c]                        @ 080dc4b8 c369
    lsls r2,r5,#0x10    @ 080dc4ba 2a04
    lsrs r2,r2,#0x10    @ 080dc4bc 120c
    lsls r1,r1,#0x10    @ 080dc4be 0904
    orrs r2,r1    @ 080dc4c0 0a43
    adds r0,r4,#0x0    @ 080dc4c2 201c
    adds r1,r3,#0x0    @ 080dc4c4 191c
    movs r3,#0x1    @ 080dc4c6 0123
    bl init_aob_ctx_from_ptnsect             @ 080dc4c8 1bf06cfc
    movs r0,#0x1    @ 080dc4cc 0120
    ldrb r1,[r4,#0x13]                       @ 080dc4ce e17c
    orrs r0,r1    @ 080dc4d0 0843
    movs r1,#0x7    @ 080dc4d2 0721
    rsbs r1,r1,#0    @ 080dc4d4 4942
    ands r0,r1    @ 080dc4d6 0840
    movs r1,#0x2    @ 080dc4d8 0221
    orrs r0,r1    @ 080dc4da 0843
    strb r0,[r4,#0x13]                       @ 080dc4dc e074
    strh r5,[r4,#0x10]                       @ 080dc4de 2582
    pop {r4,r5}                              @ 080dc4e0 30bc
    pop {r0}                                 @ 080dc4e2 01bc
    bx r0                                    @ 080dc4e4 0047
    .zero  0x2
DAT_080dc4e8:
    .word  0x09ce826c                     @ 080dc4e8 6c82ce09

@ Writes pack card tile row data (fifth field, extended) in multi-row mode to OBJ VRAM, optionally copies palette. Only caller FUN_080d50e4 (scene_pack) on pack home init. r0=card_slot_index (VRAM offset slot*32), r1=palette slot. Fetches ROM tile ptr from 0x09ce822c+0x1c (fifth field), calls write_tile_rows_to_vram_by_mode(r0=VRAM_dst, r1=tile_ptr, r2=8_cols, r3=6_rows, [sp]=0x10_rows). If r1<=0xf DMA copies palette.
@ 
@ Constants:
@ - OBJ_VRAM_BASE=0x06010000
@ - ROM_TILE_TABLE=0x09ce822c // offset +0x1c = fifth field
@ - ROM_PAL_TABLE=0x09ce824c // offset +0x1c
@ - OBJ_PAL_BASE=0x05000200
@ - MODE_ROWS_SP=0x10 // stack parameter row_count_mode
@ - TILE_COLS=8; TILE_ROWS=6
write_pack_card_tile_rows_to_obj_vram:
    push {r4,lr}                             @ 080dc4ec 10b5
    sub sp,#0x4                              @ 080dc4ee 81b0
    adds r4,r1,#0x0    @ 080dc4f0 0c1c
    lsls r0,r0,#0x5    @ 080dc4f2 4001
    ldr r1, DAT_080dc524                     @ 080dc4f4 0b49
    adds r0,r0,r1    @ 080dc4f6 4018
    ldr r1, DAT_080dc528                     @ 080dc4f8 0b49
    ldr r1,[r1,#0x1c]                        @ 080dc4fa c969
    movs r2,#0x10    @ 080dc4fc 1022
    str r2,[sp,#0x0]                         @ 080dc4fe 0092
    movs r2,#0x8    @ 080dc500 0822
    movs r3,#0x6    @ 080dc502 0623
    bl write_tile_rows_to_vram_by_mode       @ 080dc504 1bf010f8
    cmp r4,#0xf                              @ 080dc508 0f2c
    bhi LAB_080dc51c                         @ 080dc50a 07d8
    lsls r0,r4,#0x5    @ 080dc50c 6001
    ldr r1, DAT_080dc52c                     @ 080dc50e 0749
    adds r0,r0,r1    @ 080dc510 4018
    ldr r1, DAT_080dc530                     @ 080dc512 0749
    ldr r1,[r1,#0x1c]                        @ 080dc514 c969
    movs r2,#0x20    @ 080dc516 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc518 18f0f6fc
LAB_080dc51c:
    add sp,#0x4                              @ 080dc51c 01b0
    pop {r4}                                 @ 080dc51e 10bc
    pop {r0}                                 @ 080dc520 01bc
    bx r0                                    @ 080dc522 0047
DAT_080dc524:
    .word  0x06010000                     @ 080dc524 00000106
DAT_080dc528:
    .word  0x09ce822c                     @ 080dc528 2c82ce09
DAT_080dc52c:
    .word  0x05000200                     @ 080dc52c 00020005
DAT_080dc530:
    .word  0x09ce824c                     @ 080dc530 4c82ce09

@ Advances pack card AOB (animation object) one frame and renders to OAM. Only caller FUN_080d5334 (scene_pack) in pack anim tick; r0=oam_dest_ptr, r1=y_attr (u8 [0..255]), r2=aob_ctx_ptr. Calls tick_aob_frame_counter(aob_ctx_ptr) to advance frame, extracts r1 low 8 bits as y_coord, calls render_aob_frame_to_oam(aob_ctx_ptr, oam_dest_ptr, 0, y_coord) to write current frame data to OAM shadow.
tick_pack_card_aob_frame:
    push {r4,r5,r6,lr}                       @ 080dc534 70b5
    adds r4,r0,#0x0    @ 080dc536 041c
    adds r5,r1,#0x0    @ 080dc538 0d1c
    adds r6,r2,#0x0    @ 080dc53a 161c
    adds r0,r6,#0x0    @ 080dc53c 301c
    bl tick_aob_frame_counter                @ 080dc53e 1bf0e3fc
    lsls r5,r5,#0x18    @ 080dc542 2d06
    lsrs r5,r5,#0x18    @ 080dc544 2d0e
    adds r0,r6,#0x0    @ 080dc546 301c
    adds r1,r4,#0x0    @ 080dc548 211c
    movs r2,#0x0    @ 080dc54a 0022
    adds r3,r5,#0x0    @ 080dc54c 2b1c
    bl render_aob_frame_to_oam               @ 080dc54e 1bf057fd
    pop {r4,r5,r6}                           @ 080dc552 70bc
    pop {r0}                                 @ 080dc554 01bc
    bx r0                                    @ 080dc556 0047

@ Zeros two adjacent OBJ line buffer slots in pack shop BG tile VRAM, then renders label text to BG tile VRAM. Called by 11 callers during pack sub-scene init (banner/info/list); r0=bg_tile_dest, r1=text_str_ptr (may be NULL). Zeros r0 and r0+0x400 slots (0x1a0 halfwords each) via zero_fill_halfword_wrapper; if r1==0 skips text render; otherwise setup_line_buf_pos_and_font + measure_string_pixel_width + centered text_render_wrapper + write_line_buf_to_bg_tile_vram renders the label.
@ 
@ Constants:
@ - FILL_COUNT=0xd0<<1=0x1a0 // halfwords per slot zero fill
@ - SLOT_STRIDE=0x80<<3=0x400 // two-slot gap
@ - X_CENTER_BASE=0x68 // centering: (0x68-width)/2
@ - RENDER_ATTR=0x107 // text render color attr
render_pack_label_to_bg_tile_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dc558 f0b5
    adds r7,r0,#0x0    @ 080dc55a 071c
    adds r6,r1,#0x0    @ 080dc55c 0e1c
    adds r4,r7,#0x0    @ 080dc55e 3c1c
    movs r5,#0x0    @ 080dc560 0025
LAB_080dc562:
    adds r0,r4,#0x0    @ 080dc562 201c
    movs r1,#0xd0    @ 080dc564 d021
    lsls r1,r1,#0x1    @ 080dc566 4900
    bl zero_fill_halfword_wrapper            @ 080dc568 18f096fc
    movs r0,#0x80    @ 080dc56c 8020
    lsls r0,r0,#0x3    @ 080dc56e c000
    adds r4,r4,r0    @ 080dc570 2418
    adds r5,#0x1    @ 080dc572 0135
    cmp r5,#0x1                              @ 080dc574 012d
    bls LAB_080dc562                         @ 080dc576 f4d9
    cmp r6,#0x0                              @ 080dc578 002e
    beq LAB_080dc5d8                         @ 080dc57a 2dd0
    movs r0,#0xd    @ 080dc57c 0d20
    movs r1,#0x2    @ 080dc57e 0221
    bl setup_line_buf_pos_and_font           @ 080dc580 14f018fb
    ldr r2, DAT_080dc5e0                     @ 080dc584 164a
    movs r0,#0x2    @ 080dc586 0220
    rsbs r0,r0,#0    @ 080dc588 4042
    ldrb r1,[r2,#0x15]                       @ 080dc58a 517d
    ands r0,r1    @ 080dc58c 0840
    strb r0,[r2,#0x15]                       @ 080dc58e 5075
    movs r1,#0x2    @ 080dc590 0221
    ldrb r3,[r2,#0x8]                        @ 080dc592 137a
    orrs r1,r3    @ 080dc594 1943
    strb r1,[r2,#0x8]                        @ 080dc596 1172
    movs r0,#0x7d    @ 080dc598 7d20
    rsbs r0,r0,#0    @ 080dc59a 4042
    ldrb r3,[r2,#0x14]                       @ 080dc59c 137d
    ands r0,r3    @ 080dc59e 1840
    strb r0,[r2,#0x14]                       @ 080dc5a0 1075
    ldr r3, PTR_font_jp_base_table_080dc5e4  @ 080dc5a2 104b
    lsls r0,r1,#0x1e    @ 080dc5a4 8807
    lsrs r0,r0,#0x1f    @ 080dc5a6 c00f
    lsls r0,r0,#0x2    @ 080dc5a8 8000
    lsls r1,r1,#0x1f    @ 080dc5aa c907
    lsrs r1,r1,#0x1f    @ 080dc5ac c90f
    lsls r1,r1,#0x3    @ 080dc5ae c900
    adds r0,r0,r1    @ 080dc5b0 4018
    adds r0,r0,r3    @ 080dc5b2 c018
    ldr r0,[r0,#0x0]                         @ 080dc5b4 0068
    str r0,[r2,#0x4]                         @ 080dc5b6 5060
    adds r0,r6,#0x0    @ 080dc5b8 301c
    bl measure_string_pixel_width            @ 080dc5ba 13f05bfe
    adds r1,r0,#0x0    @ 080dc5be 011c
    movs r0,#0x68    @ 080dc5c0 6820
    subs r0,r0,r1    @ 080dc5c2 401a
    lsrs r0,r0,#0x1    @ 080dc5c4 4008
    ldr r2, DAT_080dc5e8                     @ 080dc5c6 084a
    movs r1,#0x3    @ 080dc5c8 0321
    adds r3,r6,#0x0    @ 080dc5ca 331c
    bl text_render_wrapper                   @ 080dc5cc 16f056fa
    adds r0,r7,#0x0    @ 080dc5d0 381c
    movs r1,#0x0    @ 080dc5d2 0021
    bl write_line_buf_to_bg_tile_vram        @ 080dc5d4 17f0fef8
LAB_080dc5d8:
    pop {r4,r5,r6,r7}                        @ 080dc5d8 f0bc
    pop {r0}                                 @ 080dc5da 01bc
    bx r0                                    @ 080dc5dc 0047
    .zero  0x2
DAT_080dc5e0:
    .word  0x02006ed0                     @ 080dc5e0 d06e0002
PTR_font_jp_base_table_080dc5e4:
    .word  font_jp_base_table             @ 080dc5e4 54f8e509
DAT_080dc5e8:
    .word  0x00000107                     @ 080dc5e8 07010000

@ Copies ROM pack card palette data to OBJ palette VRAM at specified slot. 4 callers (pack shop init/page switch paths); r0=pal_slot_index ([0..0xf]). If r0>0xf skips. Computes 0x05000200+r0*0x20 as OBJ palette destination, copies 0x20 bytes (16-color palette) from ROM table 0x09ccd290 via copy_memory_dma3_with_cpu_fallback.
@ 
@ Constants:
@ - OBJ_PAL_BASE=0x05000200 // OBJ palette VRAM base
@ - ROM_PAL_DATA=0x09ccd290 // ROM palette data
@ - PAL_SIZE=0x20 // 32 bytes = 16 colors
@ - PAL_LIMIT=0xf // valid slot range [0..15]
copy_pack_card_palette_to_obj_pal:
    push {lr}                                @ 080dc5ec 00b5
    cmp r0,#0xf                              @ 080dc5ee 0f28
    bhi LAB_080dc600                         @ 080dc5f0 06d8
    lsls r0,r0,#0x5    @ 080dc5f2 4001
    ldr r1, DAT_080dc604                     @ 080dc5f4 0349
    adds r0,r0,r1    @ 080dc5f6 4018
    ldr r1, DAT_080dc608                     @ 080dc5f8 0349
    movs r2,#0x20    @ 080dc5fa 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dc5fc 18f084fc
LAB_080dc600:
    pop {r0}                                 @ 080dc600 01bc
    bx r0                                    @ 080dc602 0047
DAT_080dc604:
    .word  0x05000200                     @ 080dc604 00020005
DAT_080dc608:
    .word  0x09ccd290                     @ 080dc608 90d2cc09

@ Renders the pack label string A (game_str_id=0x13f8) to BG VRAM at the tile row for the given pack slot.
@ r0=pack_index [0..4]; internally computes VRAM dst = 0x06010000 + r0*0x20.
@ Looks up game_str_id=0x13f8 in game_str_pointer_table using language flag at [0x02000000+0x6c2c] low 3 bits; calls render_pack_label_to_bg_tile_vram(dst, str_ptr).
@ indeg=0 (dead code / unreferenced; grep ".word 0x080dc60d" -> 0 hits). Sibling of render_pack_label_text_b_to_bg_vram (0x080dc664).
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM tile destination base
@ - PACK_ENTRY_STRIDE=0x20 // per-pack tile stride (r0<<5)
@ - GAME_STR_ID=0x13f8 // pack label string A ID
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language byte
@ 
@ Inputs: r0=u8 pack_index [0..4]
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + pack_index*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_text_a_to_bg_vram:
    push {r4,lr}                             @ 080dc60c 10b5
    adds r4,r0,#0x0    @ 080dc60e 041c
    lsls r4,r4,#0x5    @ 080dc610 6401
    ldr r0, DAT_080dc64c                     @ 080dc612 0e48
    adds r4,r4,r0    @ 080dc614 2418
    ldr r0, DAT_080dc650                     @ 080dc616 0e48
    bl game_str_id_to_row                    @ 080dc618 18f0fefb
    ldr r2, PTR_game_str_pointer_table_080dc654 @ 080dc61c 0d4a
    lsls r0,r0,#0x10    @ 080dc61e 0004
    lsrs r0,r0,#0x10    @ 080dc620 000c
    lsls r1,r0,#0x1    @ 080dc622 4100
    adds r1,r1,r0    @ 080dc624 0918
    lsls r1,r1,#0x1    @ 080dc626 4900
    ldr r0, DAT_080dc658                     @ 080dc628 0b48
    ldr r3, DAT_080dc65c                     @ 080dc62a 0c4b
    adds r0,r0,r3    @ 080dc62c c018
    ldrb r0,[r0,#0x0]                        @ 080dc62e 0078
    lsls r0,r0,#0x1d    @ 080dc630 4007
    lsrs r0,r0,#0x1d    @ 080dc632 400f
    adds r1,r1,r0    @ 080dc634 0918
    lsls r1,r1,#0x2    @ 080dc636 8900
    adds r1,r1,r2    @ 080dc638 8918
    ldr r1,[r1,#0x0]                         @ 080dc63a 0968
    ldr r0, PTR_game_str_ja_080dc660         @ 080dc63c 0848
    adds r1,r1,r0    @ 080dc63e 0918
    adds r0,r4,#0x0    @ 080dc640 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dc642 fff789ff
    pop {r4}                                 @ 080dc646 10bc
    pop {r0}                                 @ 080dc648 01bc
    bx r0                                    @ 080dc64a 0047
DAT_080dc64c:
    .word  0x06010000                     @ 080dc64c 00000106
DAT_080dc650:
    .word  0x000013f8                     @ 080dc650 f8130000
PTR_game_str_pointer_table_080dc654:
    .word  game_str_pointer_table         @ 080dc654 400f0008
DAT_080dc658:
    .word  0x02000000                     @ 080dc658 00000002
DAT_080dc65c:
    .word  0x00006c2c                     @ 080dc65c 2c6c0000
PTR_game_str_ja_080dc660:
    .word  game_str_ja                    @ 080dc660 109cdb09

@ Renders the pack label string B (game_str_id=0x13f9) to BG VRAM at the tile row for the given pack slot.
@ r0=pack_index [0..4]; internally computes VRAM dst = 0x06010000 + r0*0x20.
@ Looks up game_str_id=0x13f9 in game_str_pointer_table using language flag; calls render_pack_label_to_bg_tile_vram(dst, str_ptr).
@ Structurally symmetric to render_pack_label_text_a_to_bg_vram (0x080dc60c); differs only in game_str_id (0x13f9 vs 0x13f8).
@ indeg=0 (dead code; grep ".word 0x080dc665" -> 0 hits).
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM tile destination base
@ - PACK_ENTRY_STRIDE=0x20 // per-pack tile stride
@ - GAME_STR_ID=0x13f9 // pack label string B ID
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language byte
@ 
@ Inputs: r0=u8 pack_index [0..4]
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + pack_index*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_text_b_to_bg_vram:
    push {r4,lr}                             @ 080dc664 10b5
    adds r4,r0,#0x0    @ 080dc666 041c
    lsls r4,r4,#0x5    @ 080dc668 6401
    ldr r0, DAT_080dc6a4                     @ 080dc66a 0e48
    adds r4,r4,r0    @ 080dc66c 2418
    ldr r0, DAT_080dc6a8                     @ 080dc66e 0e48
    bl game_str_id_to_row                    @ 080dc670 18f0d2fb
    ldr r2, PTR_game_str_pointer_table_080dc6ac @ 080dc674 0d4a
    lsls r0,r0,#0x10    @ 080dc676 0004
    lsrs r0,r0,#0x10    @ 080dc678 000c
    lsls r1,r0,#0x1    @ 080dc67a 4100
    adds r1,r1,r0    @ 080dc67c 0918
    lsls r1,r1,#0x1    @ 080dc67e 4900
    ldr r0, DAT_080dc6b0                     @ 080dc680 0b48
    ldr r3, DAT_080dc6b4                     @ 080dc682 0c4b
    adds r0,r0,r3    @ 080dc684 c018
    ldrb r0,[r0,#0x0]                        @ 080dc686 0078
    lsls r0,r0,#0x1d    @ 080dc688 4007
    lsrs r0,r0,#0x1d    @ 080dc68a 400f
    adds r1,r1,r0    @ 080dc68c 0918
    lsls r1,r1,#0x2    @ 080dc68e 8900
    adds r1,r1,r2    @ 080dc690 8918
    ldr r1,[r1,#0x0]                         @ 080dc692 0968
    ldr r0, PTR_game_str_ja_080dc6b8         @ 080dc694 0848
    adds r1,r1,r0    @ 080dc696 0918
    adds r0,r4,#0x0    @ 080dc698 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dc69a fff75dff
    pop {r4}                                 @ 080dc69e 10bc
    pop {r0}                                 @ 080dc6a0 01bc
    bx r0                                    @ 080dc6a2 0047
DAT_080dc6a4:
    .word  0x06010000                     @ 080dc6a4 00000106
DAT_080dc6a8:
    .word  0x000013f9                     @ 080dc6a8 f9130000
PTR_game_str_pointer_table_080dc6ac:
    .word  game_str_pointer_table         @ 080dc6ac 400f0008
DAT_080dc6b0:
    .word  0x02000000                     @ 080dc6b0 00000002
DAT_080dc6b4:
    .word  0x00006c2c                     @ 080dc6b4 2c6c0000
PTR_game_str_ja_080dc6b8:
    .word  game_str_ja                    @ 080dc6b8 109cdb09

@ Renders the purchase-state label for the current pack selection to BG VRAM; creates a warning overlay if DP balance is insufficient.
@ r0=target_vram_x (callee-save r9), r1=vram_param (callee-save r10).
@ Calls recompute_pack_selection_totals to update pack_ui_state+0xc totals. Reads [+0xa] selected count: if 0, uses game_str_id=0x13f4 ("no selection"); else compares selected amount against DP balance at [0x02000000+0x6c38+4]: if sufficient uses game_str_id=0x13f2, if insufficient uses game_str_id=0x13f3 and calls text_overlay_create for a warning dialog.
@ Finally calls render_pack_label_to_bg_tile_vram to write the label tile. Called by FUN_080d7ef4 (pack shop render) and FUN_080da924 (pack selection tick).
@ 
@ Constants:
@ - GAME_STR_ID_EMPTY=0x13f4 // no pack selected
@ - GAME_STR_ID_OK=0x13f2 // purchase possible
@ - GAME_STR_ID_NG=0x13f3 // insufficient DP
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language flag
@ - DP_BALANCE=[0x02000000+0x6c38+4] // current DP balance
@ - OVERLAY_SIZE=0x0010001e // dialog size (w=0x10, h=0x1e)
@ - GAME_STR_ID_LINE2=0x7d2 // dialog second line
@ - GAME_STR_ID_LINE3=0x7d3 // dialog third line
@ 
@ Inputs: r0=u16 target_vram_x, r1=u16 vram_param
@ Returns: r0=u8 (0=no dialog created, 1=warning dialog created) via pop {r1}; bx r1 (Sub-case E)
@ Side effects: [BG VRAM 0x06010000+offset via render_pack_label_to_bg_tile_vram]; [text_overlay_create] if DP insufficient; [pack_ui_state+0xc via recompute_pack_selection_totals]
render_pack_selection_label_to_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dc6bc f0b5
    .hword 0x4657    @ 080dc6be 5746
    .hword 0x464e    @ 080dc6c0 4e46
    .hword 0x4645    @ 080dc6c2 4546
    push {r5,r6,r7}                          @ 080dc6c4 e0b4
    .hword 0x4681    @ 080dc6c6 8146
    .hword 0x468a    @ 080dc6c8 8a46
    ldr r0, DAT_080dc6f8                     @ 080dc6ca 0b48
    adds r5,r0,#0x0    @ 080dc6cc 051c
    adds r5,#0xc    @ 080dc6ce 0c35
    movs r7,#0x0    @ 080dc6d0 0027
    bl recompute_pack_selection_totals       @ 080dc6d2 fff739f8
    ldrh r0,[r5,#0xa]                        @ 080dc6d6 6889
    cmp r0,#0x0                              @ 080dc6d8 0028
    bne LAB_080dc70c                         @ 080dc6da 17d1
    ldr r0, DAT_080dc6fc                     @ 080dc6dc 0748
    bl game_str_id_to_row                    @ 080dc6de 18f09bfb
    ldr r2, PTR_game_str_pointer_table_080dc700 @ 080dc6e2 074a
    lsls r0,r0,#0x10    @ 080dc6e4 0004
    lsrs r0,r0,#0x10    @ 080dc6e6 000c
    lsls r1,r0,#0x1    @ 080dc6e8 4100
    adds r1,r1,r0    @ 080dc6ea 0918
    lsls r1,r1,#0x1    @ 080dc6ec 4900
    ldr r0, DAT_080dc704                     @ 080dc6ee 0548
    ldr r3, DAT_080dc708                     @ 080dc6f0 054b
    adds r0,r0,r3    @ 080dc6f2 c018
    b LAB_080dc730                           @ 080dc6f4 1ce0
    .zero  0x2
DAT_080dc6f8:
    .word  pack_ui_state                  @ 080dc6f8 50580003
DAT_080dc6fc:
    .word  0x000013f4                     @ 080dc6fc f4130000
PTR_game_str_pointer_table_080dc700:
    .word  game_str_pointer_table         @ 080dc700 400f0008
DAT_080dc704:
    .word  0x02000000                     @ 080dc704 00000002
DAT_080dc708:
    .word  0x00006c2c                     @ 080dc708 2c6c0000
LAB_080dc70c:
    ldr r4, DAT_080dc744                     @ 080dc70c 0d4c
    ldr r1, DAT_080dc748                     @ 080dc70e 0e49
    adds r0,r4,r1    @ 080dc710 6018
    ldr r1,[r0,#0x0]                         @ 080dc712 0168
    ldr r0,[r5,#0xc]                         @ 080dc714 e868
    cmp r1,r0                                @ 080dc716 8142
    bcs LAB_080dc75c                         @ 080dc718 20d2
    ldr r0, DAT_080dc74c                     @ 080dc71a 0c48
    bl game_str_id_to_row                    @ 080dc71c 18f07cfb
    ldr r2, PTR_game_str_pointer_table_080dc750 @ 080dc720 0b4a
    lsls r0,r0,#0x10    @ 080dc722 0004
    lsrs r0,r0,#0x10    @ 080dc724 000c
    lsls r1,r0,#0x1    @ 080dc726 4100
    adds r1,r1,r0    @ 080dc728 0918
    lsls r1,r1,#0x1    @ 080dc72a 4900
    ldr r3, DAT_080dc754                     @ 080dc72c 094b
    adds r0,r4,r3    @ 080dc72e e018
LAB_080dc730:
    ldrb r0,[r0,#0x0]                        @ 080dc730 0078
    lsls r0,r0,#0x1d    @ 080dc732 4007
    lsrs r0,r0,#0x1d    @ 080dc734 400f
    adds r1,r1,r0    @ 080dc736 0918
    lsls r1,r1,#0x2    @ 080dc738 8900
    adds r1,r1,r2    @ 080dc73a 8918
    ldr r1,[r1,#0x0]                         @ 080dc73c 0968
    ldr r0, PTR_game_str_ja_080dc758         @ 080dc73e 0648
    adds r2,r1,r0    @ 080dc740 0a18
    b LAB_080dc786                           @ 080dc742 20e0
DAT_080dc744:
    .word  0x02000000                     @ 080dc744 00000002
DAT_080dc748:
    .word  0x00006c38                     @ 080dc748 386c0000
DAT_080dc74c:
    .word  0x000013f2                     @ 080dc74c f2130000
PTR_game_str_pointer_table_080dc750:
    .word  game_str_pointer_table         @ 080dc750 400f0008
DAT_080dc754:
    .word  0x00006c2c                     @ 080dc754 2c6c0000
PTR_game_str_ja_080dc758:
    .word  game_str_ja                    @ 080dc758 109cdb09
LAB_080dc75c:
    ldr r0, DAT_080dc808                     @ 080dc75c 2a48
    bl game_str_id_to_row                    @ 080dc75e 18f05bfb
    ldr r2, PTR_game_str_pointer_table_080dc80c @ 080dc762 2a4a
    lsls r0,r0,#0x10    @ 080dc764 0004
    lsrs r0,r0,#0x10    @ 080dc766 000c
    lsls r1,r0,#0x1    @ 080dc768 4100
    adds r1,r1,r0    @ 080dc76a 0918
    lsls r1,r1,#0x1    @ 080dc76c 4900
    ldr r3, DAT_080dc810                     @ 080dc76e 284b
    adds r0,r4,r3    @ 080dc770 e018
    ldrb r0,[r0,#0x0]                        @ 080dc772 0078
    lsls r0,r0,#0x1d    @ 080dc774 4007
    lsrs r0,r0,#0x1d    @ 080dc776 400f
    adds r1,r1,r0    @ 080dc778 0918
    lsls r1,r1,#0x2    @ 080dc77a 8900
    adds r1,r1,r2    @ 080dc77c 8918
    ldr r1,[r1,#0x0]                         @ 080dc77e 0968
    ldr r0, PTR_game_str_ja_080dc814         @ 080dc780 2448
    adds r2,r1,r0    @ 080dc782 0a18
    movs r7,#0x1    @ 080dc784 0127
LAB_080dc786:
    ldr r0, DAT_080dc818                     @ 080dc786 2448
    movs r1,#0x0    @ 080dc788 0021
    bl text_overlay_create                   @ 080dc78a 00f0d7fe
    cmp r7,#0x1                              @ 080dc78e 012f
    bne LAB_080dc7f8                         @ 080dc790 32d1
    ldr r0, DAT_080dc81c                     @ 080dc792 2248
    bl game_str_id_to_row                    @ 080dc794 18f040fb
    ldr r1, PTR_game_str_pointer_table_080dc80c @ 080dc798 1c49
    .hword 0x4688    @ 080dc79a 8846
    lsls r0,r0,#0x10    @ 080dc79c 0004
    lsrs r0,r0,#0x10    @ 080dc79e 000c
    lsls r1,r0,#0x1    @ 080dc7a0 4100
    adds r1,r1,r0    @ 080dc7a2 0918
    lsls r1,r1,#0x1    @ 080dc7a4 4900
    ldr r4, DAT_080dc820                     @ 080dc7a6 1e4c
    ldr r2, DAT_080dc810                     @ 080dc7a8 194a
    adds r4,r4,r2    @ 080dc7aa a418
    ldrb r3,[r4,#0x0]                        @ 080dc7ac 2378
    lsls r0,r3,#0x1d    @ 080dc7ae 5807
    lsrs r0,r0,#0x1d    @ 080dc7b0 400f
    adds r1,r1,r0    @ 080dc7b2 0918
    lsls r1,r1,#0x2    @ 080dc7b4 8900
    add r1,r8                                @ 080dc7b6 4144
    ldr r0,[r1,#0x0]                         @ 080dc7b8 0868
    ldr r6, PTR_game_str_ja_080dc814         @ 080dc7ba 164e
    adds r2,r0,r6    @ 080dc7bc 8219
    .hword 0x4649    @ 080dc7be 4946
    lsls r0,r1,#0x5    @ 080dc7c0 4801
    ldr r5, DAT_080dc824                     @ 080dc7c2 184d
    adds r0,r0,r5    @ 080dc7c4 4019
    adds r1,r2,#0x0    @ 080dc7c6 111c
    bl render_pack_label_to_bg_tile_vram     @ 080dc7c8 fff7c6fe
    ldr r0, DAT_080dc828                     @ 080dc7cc 1648
    bl game_str_id_to_row                    @ 080dc7ce 18f023fb
    lsls r0,r0,#0x10    @ 080dc7d2 0004
    lsrs r0,r0,#0x10    @ 080dc7d4 000c
    lsls r1,r0,#0x1    @ 080dc7d6 4100
    adds r1,r1,r0    @ 080dc7d8 0918
    lsls r1,r1,#0x1    @ 080dc7da 4900
    ldrb r4,[r4,#0x0]                        @ 080dc7dc 2478
    lsls r0,r4,#0x1d    @ 080dc7de 6007
    lsrs r0,r0,#0x1d    @ 080dc7e0 400f
    adds r1,r1,r0    @ 080dc7e2 0918
    lsls r1,r1,#0x2    @ 080dc7e4 8900
    add r1,r8                                @ 080dc7e6 4144
    ldr r0,[r1,#0x0]                         @ 080dc7e8 0868
    adds r2,r0,r6    @ 080dc7ea 8219
    .hword 0x4653    @ 080dc7ec 5346
    lsls r0,r3,#0x5    @ 080dc7ee 5801
    adds r0,r0,r5    @ 080dc7f0 4019
    adds r1,r2,#0x0    @ 080dc7f2 111c
    bl render_pack_label_to_bg_tile_vram     @ 080dc7f4 fff7b0fe
LAB_080dc7f8:
    adds r0,r7,#0x0    @ 080dc7f8 381c
    pop {r3,r4,r5}                           @ 080dc7fa 38bc
    .hword 0x4698    @ 080dc7fc 9846
    .hword 0x46a1    @ 080dc7fe a146
    .hword 0x46aa    @ 080dc800 aa46
    pop {r4,r5,r6,r7}                        @ 080dc802 f0bc
    pop {r1}                                 @ 080dc804 02bc
    bx r1                                    @ 080dc806 0847
DAT_080dc808:
    .word  0x000013f3                     @ 080dc808 f3130000
PTR_game_str_pointer_table_080dc80c:
    .word  game_str_pointer_table         @ 080dc80c 400f0008
DAT_080dc810:
    .word  0x00006c2c                     @ 080dc810 2c6c0000
PTR_game_str_ja_080dc814:
    .word  game_str_ja                    @ 080dc814 109cdb09
DAT_080dc818:
    .word  0x0010001e                     @ 080dc818 1e001000
DAT_080dc81c:
    .word  0x000007d2                     @ 080dc81c d2070000
DAT_080dc820:
    .word  0x02000000                     @ 080dc820 00000002
DAT_080dc824:
    .word  0x06010000                     @ 080dc824 00000106
DAT_080dc828:
    .word  0x000007d3                     @ 080dc828 d3070000

@ Looks up pack name string from pack sequence number and creates a text overlay layer. Only caller pack_080d9c38 (font_jp; game_str; pack) on pack scene switch; r0=pack_index. Reads pack_info_table[r0*16+8] for game_str_id, calls game_str_id_to_row, computes string pointer via game_str_pointer_table + language flag; finally calls text_overlay_create(bg_tile_base=0x06010000, str_ptr, 0, {0x10, 0x1e}) to display pack name.
@ 
@ Constants:
@ - PACK_INFO_STRIDE=0x10 // pack_info_table entry stride (16 bytes)
@ - PACK_STR_OFFSET=0x8 // game_str_id field offset in entry
@ - IWRAM_LANG_FLAG=[0x02000000+0x6c2c] // language flag
@ - OVERLAY_PARAMS={w=0x10, h=0x1e} // text overlay size parameters
create_pack_name_text_overlay:
    push {lr}                                @ 080dc82c 00b5
    ldr r1, PTR_pack_info_table_080dc86c     @ 080dc82e 0f49
    lsls r0,r0,#0x4    @ 080dc830 0001
    adds r0,r0,r1    @ 080dc832 4018
    ldrh r0,[r0,#0x8]                        @ 080dc834 0089
    bl game_str_id_to_row                    @ 080dc836 18f0effa
    ldr r2, PTR_game_str_pointer_table_080dc870 @ 080dc83a 0d4a
    lsls r0,r0,#0x10    @ 080dc83c 0004
    lsrs r0,r0,#0x10    @ 080dc83e 000c
    lsls r1,r0,#0x1    @ 080dc840 4100
    adds r1,r1,r0    @ 080dc842 0918
    lsls r1,r1,#0x1    @ 080dc844 4900
    ldr r0, DAT_080dc874                     @ 080dc846 0b48
    ldr r3, DAT_080dc878                     @ 080dc848 0b4b
    adds r0,r0,r3    @ 080dc84a c018
    ldrb r0,[r0,#0x0]                        @ 080dc84c 0078
    lsls r0,r0,#0x1d    @ 080dc84e 4007
    lsrs r0,r0,#0x1d    @ 080dc850 400f
    adds r1,r1,r0    @ 080dc852 0918
    lsls r1,r1,#0x2    @ 080dc854 8900
    adds r1,r1,r2    @ 080dc856 8918
    ldr r2,[r1,#0x0]                         @ 080dc858 0a68
    ldr r0, PTR_game_str_ja_080dc87c         @ 080dc85a 0848
    adds r2,r2,r0    @ 080dc85c 1218
    ldr r0, DAT_080dc880                     @ 080dc85e 0848
    movs r1,#0x0    @ 080dc860 0021
    bl text_overlay_create                   @ 080dc862 00f06bfe
    pop {r0}                                 @ 080dc866 01bc
    bx r0                                    @ 080dc868 0047
    .zero  0x2
PTR_pack_info_table_080dc86c:
    .word  pack_info_table                @ 080dc86c e8e2e509
PTR_game_str_pointer_table_080dc870:
    .word  game_str_pointer_table         @ 080dc870 400f0008
DAT_080dc874:
    .word  0x02000000                     @ 080dc874 00000002
DAT_080dc878:
    .word  0x00006c2c                     @ 080dc878 2c6c0000
PTR_game_str_ja_080dc87c:
    .word  game_str_ja                    @ 080dc87c 109cdb09
DAT_080dc880:
    .word  0x0010001e                     @ 080dc880 1e001000

@ Advances one step of the pack animation/display sequence.
@ Reads the current animation frame index from pack_ui_state+0x4; dispatches to the current frame handler via indirect function table at 0x09e4951c (4 bytes per entry) using invoke_r0. If the handler returns non-zero (frame complete), increments the frame index. If the next function pointer is NULL (sequence end, ldrh==0 -> LAB_080dc8b0), returns 1 (sequence finished); otherwise returns 0 (in progress).
@ Called exclusively by FUN_080ddd5c (pack display state machine main loop) each frame.
@ 
@ Constants:
@ - PACK_UI_STATE=0x03005850 // pack_ui_state base
@ - ANIM_STEP_IDX_OFFSET=0x4 // current animation frame index (halfword)
@ - FUNC_TABLE=0x09e4951c // indirect function table (ROM)
@ 
@ Inputs: void (no APCS params; ldr r4, pack_ui_state loaded internally)
@ Returns: r0=u8 (0=animation in progress, 1=sequence ended or table empty)
@ Side effects: [pack_ui_state+0x4] += 1 when frame completes
tick_pack_animation_step:
    push {r4,lr}                             @ 080dc884 10b5
    ldr r4, DAT_080dc8a8                     @ 080dc886 084c
    ldr r1, DAT_080dc8ac                     @ 080dc888 0849
    ldrh r2,[r4,#0x4]                        @ 080dc88a a288
    lsls r0,r2,#0x2    @ 080dc88c 9000
    adds r0,r0,r1    @ 080dc88e 4018
    ldr r0,[r0,#0x0]                         @ 080dc890 0068
    cmp r0,#0x0                              @ 080dc892 0028
    beq LAB_080dc8b0                         @ 080dc894 0cd0
    bl invoke_r0                             @ 080dc896 31f097fe
    cmp r0,#0x0                              @ 080dc89a 0028
    beq LAB_080dc8a4                         @ 080dc89c 02d0
    ldrh r0,[r4,#0x4]                        @ 080dc89e a088
    adds r0,#0x1    @ 080dc8a0 0130
    strh r0,[r4,#0x4]                        @ 080dc8a2 a080
LAB_080dc8a4:
    movs r0,#0x0    @ 080dc8a4 0020
    b LAB_080dc8b2                           @ 080dc8a6 04e0
DAT_080dc8a8:
    .word  pack_ui_state                  @ 080dc8a8 50580003
DAT_080dc8ac:
    .word  0x09e4951c                     @ 080dc8ac 1c95e409
LAB_080dc8b0:
    movs r0,#0x1    @ 080dc8b0 0120
LAB_080dc8b2:
    pop {r4}                                 @ 080dc8b2 10bc
    pop {r1}                                 @ 080dc8b4 02bc
    bx r1                                    @ 080dc8b6 0847

@ Renders the default (null) pack label to BG tile VRAM for the given pack index.
@ r0=pack_index [0..4] (constrained by FUN_080d511c cmp r1,#0x4); computes VRAM dst = 0x06010000 + r0*0x20; passes r1=0 (null str_ptr) to render_pack_label_to_bg_tile_vram.
@ Serves as the default case handler of the FUN_080d511c switch dispatcher (case > 4).
@ Body is minimal: lsls #5 + ldr base + adds + bl + pop {r0};bx r0.
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM tile destination base
@ - PACK_STRIDE=0x20 // per-pack tile stride (r0<<5)
@ 
@ Inputs: r0=u8 pack_index [0..4]
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + pack_index*0x20 via render_pack_label_to_bg_tile_vram] default (null) label tile written
render_pack_label_default_to_bg_vram:
    push {lr}                                @ 080dc8b8 00b5
    lsls r0,r0,#0x5    @ 080dc8ba 4001
    ldr r1, DAT_080dc8cc                     @ 080dc8bc 0349
    adds r0,r0,r1    @ 080dc8be 4018
    movs r1,#0x0    @ 080dc8c0 0021
    bl render_pack_label_to_bg_tile_vram     @ 080dc8c2 fff749fe
    pop {r0}                                 @ 080dc8c6 01bc
    bx r0                                    @ 080dc8c8 0047
    .zero  0x2
DAT_080dc8cc:
    .word  0x06010000                     @ 080dc8cc 00000106

@ Renders the pack label string for game_str_id=0x13f1 to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..848]; internally computes VRAM dst = 0x06010000 + r0*0x20.
@ Looks up game_str_id=0x13f1 in game_str_pointer_table using language flag at [0x02000000+0x6c2c] low 3 bits; calls render_pack_label_to_bg_tile_vram.
@ Called by FUN_080d713c (pack info page render; passes r0=0x140=320) and FUN_080d91e0 (pack info render; passes r0=0x350=848). Paired with render_pack_label_str1390_to_bg_vram (0x080dc928) in both callers.
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x13f1 // pack label string ID
@ 
@ Inputs: r0=u16 tile_row_base [0..848] (observed: 0x140=320 from FUN_080d713c, 0x350=848 from FUN_080d91e0)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str13f1_to_bg_vram:
    push {r4,lr}                             @ 080dc8d0 10b5
    adds r4,r0,#0x0    @ 080dc8d2 041c
    lsls r4,r4,#0x5    @ 080dc8d4 6401
    ldr r0, DAT_080dc910                     @ 080dc8d6 0e48
    adds r4,r4,r0    @ 080dc8d8 2418
    ldr r0, DAT_080dc914                     @ 080dc8da 0e48
    bl game_str_id_to_row                    @ 080dc8dc 18f09cfa
    ldr r2, PTR_game_str_pointer_table_080dc918 @ 080dc8e0 0d4a
    lsls r0,r0,#0x10    @ 080dc8e2 0004
    lsrs r0,r0,#0x10    @ 080dc8e4 000c
    lsls r1,r0,#0x1    @ 080dc8e6 4100
    adds r1,r1,r0    @ 080dc8e8 0918
    lsls r1,r1,#0x1    @ 080dc8ea 4900
    ldr r0, DAT_080dc91c                     @ 080dc8ec 0b48
    ldr r3, DAT_080dc920                     @ 080dc8ee 0c4b
    adds r0,r0,r3    @ 080dc8f0 c018
    ldrb r0,[r0,#0x0]                        @ 080dc8f2 0078
    lsls r0,r0,#0x1d    @ 080dc8f4 4007
    lsrs r0,r0,#0x1d    @ 080dc8f6 400f
    adds r1,r1,r0    @ 080dc8f8 0918
    lsls r1,r1,#0x2    @ 080dc8fa 8900
    adds r1,r1,r2    @ 080dc8fc 8918
    ldr r1,[r1,#0x0]                         @ 080dc8fe 0968
    ldr r0, PTR_game_str_ja_080dc924         @ 080dc900 0848
    adds r1,r1,r0    @ 080dc902 0918
    adds r0,r4,#0x0    @ 080dc904 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dc906 fff727fe
    pop {r4}                                 @ 080dc90a 10bc
    pop {r0}                                 @ 080dc90c 01bc
    bx r0                                    @ 080dc90e 0047
DAT_080dc910:
    .word  0x06010000                     @ 080dc910 00000106
DAT_080dc914:
    .word  0x000013f1                     @ 080dc914 f1130000
PTR_game_str_pointer_table_080dc918:
    .word  game_str_pointer_table         @ 080dc918 400f0008
DAT_080dc91c:
    .word  0x02000000                     @ 080dc91c 00000002
DAT_080dc920:
    .word  0x00006c2c                     @ 080dc920 2c6c0000
PTR_game_str_ja_080dc924:
    .word  game_str_ja                    @ 080dc924 109cdb09

@ Renders the pack label string for game_str_id=0x1390 to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..912]; VRAM dst = 0x06010000 + r0*0x20.
@ Looks up game_str_id=0x1390 in game_str_pointer_table using language flag; calls render_pack_label_to_bg_tile_vram.
@ Called by FUN_080d511c (case 3), FUN_080d713c (pack info render; passes r0=0x180=384), and FUN_080d91e0 (pack info render; passes r0=0x390=912).
@ Paired with render_pack_label_str13f1_to_bg_vram (0x080dc8d0) in FUN_080d713c and FUN_080d91e0.
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x1390 // pack label string ID
@ 
@ Inputs: r0=u16 tile_row_base [0..912] (observed: 0x180=384 from FUN_080d713c, 0x390=912 from FUN_080d91e0, 0x280=640/0x28d=653 from FUN_080d511c)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str1390_to_bg_vram:
    push {r4,lr}                             @ 080dc928 10b5
    adds r4,r0,#0x0    @ 080dc92a 041c
    lsls r4,r4,#0x5    @ 080dc92c 6401
    ldr r0, DAT_080dc968                     @ 080dc92e 0e48
    adds r4,r4,r0    @ 080dc930 2418
    ldr r0, DAT_080dc96c                     @ 080dc932 0e48
    bl game_str_id_to_row                    @ 080dc934 18f070fa
    ldr r2, PTR_game_str_pointer_table_080dc970 @ 080dc938 0d4a
    lsls r0,r0,#0x10    @ 080dc93a 0004
    lsrs r0,r0,#0x10    @ 080dc93c 000c
    lsls r1,r0,#0x1    @ 080dc93e 4100
    adds r1,r1,r0    @ 080dc940 0918
    lsls r1,r1,#0x1    @ 080dc942 4900
    ldr r0, DAT_080dc974                     @ 080dc944 0b48
    ldr r3, DAT_080dc978                     @ 080dc946 0c4b
    adds r0,r0,r3    @ 080dc948 c018
    ldrb r0,[r0,#0x0]                        @ 080dc94a 0078
    lsls r0,r0,#0x1d    @ 080dc94c 4007
    lsrs r0,r0,#0x1d    @ 080dc94e 400f
    adds r1,r1,r0    @ 080dc950 0918
    lsls r1,r1,#0x2    @ 080dc952 8900
    adds r1,r1,r2    @ 080dc954 8918
    ldr r1,[r1,#0x0]                         @ 080dc956 0968
    ldr r0, PTR_game_str_ja_080dc97c         @ 080dc958 0848
    adds r1,r1,r0    @ 080dc95a 0918
    adds r0,r4,#0x0    @ 080dc95c 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dc95e fff7fbfd
    pop {r4}                                 @ 080dc962 10bc
    pop {r0}                                 @ 080dc964 01bc
    bx r0                                    @ 080dc966 0047
DAT_080dc968:
    .word  0x06010000                     @ 080dc968 00000106
DAT_080dc96c:
    .word  0x00001390                     @ 080dc96c 90130000
PTR_game_str_pointer_table_080dc970:
    .word  game_str_pointer_table         @ 080dc970 400f0008
DAT_080dc974:
    .word  0x02000000                     @ 080dc974 00000002
DAT_080dc978:
    .word  0x00006c2c                     @ 080dc978 2c6c0000
PTR_game_str_ja_080dc97c:
    .word  game_str_ja                    @ 080dc97c 109cdb09

@ Renders the pack label string for game_str_id=0x13fa to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..653]; VRAM dst = 0x06010000 + r0*0x20.
@ Dispatched by FUN_080d511c switch dispatcher (case 0). Structurally symmetric to all siblings in the switch-case pack label render cluster.
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x13fa // pack label string ID
@ 
@ Inputs: r0=u16 tile_row_base [0..653] (FUN_080d511c passes r2=0x28d=653 or 0x280=640; caller-set fixed value)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str13fa_to_bg_vram:
    push {r4,lr}                             @ 080dc980 10b5
    adds r4,r0,#0x0    @ 080dc982 041c
    lsls r4,r4,#0x5    @ 080dc984 6401
    ldr r0, DAT_080dc9c0                     @ 080dc986 0e48
    adds r4,r4,r0    @ 080dc988 2418
    ldr r0, DAT_080dc9c4                     @ 080dc98a 0e48
    bl game_str_id_to_row                    @ 080dc98c 18f044fa
    ldr r2, PTR_game_str_pointer_table_080dc9c8 @ 080dc990 0d4a
    lsls r0,r0,#0x10    @ 080dc992 0004
    lsrs r0,r0,#0x10    @ 080dc994 000c
    lsls r1,r0,#0x1    @ 080dc996 4100
    adds r1,r1,r0    @ 080dc998 0918
    lsls r1,r1,#0x1    @ 080dc99a 4900
    ldr r0, DAT_080dc9cc                     @ 080dc99c 0b48
    ldr r3, DAT_080dc9d0                     @ 080dc99e 0c4b
    adds r0,r0,r3    @ 080dc9a0 c018
    ldrb r0,[r0,#0x0]                        @ 080dc9a2 0078
    lsls r0,r0,#0x1d    @ 080dc9a4 4007
    lsrs r0,r0,#0x1d    @ 080dc9a6 400f
    adds r1,r1,r0    @ 080dc9a8 0918
    lsls r1,r1,#0x2    @ 080dc9aa 8900
    adds r1,r1,r2    @ 080dc9ac 8918
    ldr r1,[r1,#0x0]                         @ 080dc9ae 0968
    ldr r0, PTR_game_str_ja_080dc9d4         @ 080dc9b0 0848
    adds r1,r1,r0    @ 080dc9b2 0918
    adds r0,r4,#0x0    @ 080dc9b4 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dc9b6 fff7cffd
    pop {r4}                                 @ 080dc9ba 10bc
    pop {r0}                                 @ 080dc9bc 01bc
    bx r0                                    @ 080dc9be 0047
DAT_080dc9c0:
    .word  0x06010000                     @ 080dc9c0 00000106
DAT_080dc9c4:
    .word  0x000013fa                     @ 080dc9c4 fa130000
PTR_game_str_pointer_table_080dc9c8:
    .word  game_str_pointer_table         @ 080dc9c8 400f0008
DAT_080dc9cc:
    .word  0x02000000                     @ 080dc9cc 00000002
DAT_080dc9d0:
    .word  0x00006c2c                     @ 080dc9d0 2c6c0000
PTR_game_str_ja_080dc9d4:
    .word  game_str_ja                    @ 080dc9d4 109cdb09

@ Renders the pack label string for game_str_id=0x13fb to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..653]; VRAM dst = 0x06010000 + r0*0x20.
@ Dispatched by FUN_080d511c switch dispatcher (case 1). Structurally symmetric to all siblings in the switch-case pack label render cluster.
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x13fb // pack label string ID
@ 
@ Inputs: r0=u16 tile_row_base [0..653] (FUN_080d511c passes r2=0x28d=653 or 0x280=640; caller-set fixed value)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str13fb_to_bg_vram:
    push {r4,lr}                             @ 080dc9d8 10b5
    adds r4,r0,#0x0    @ 080dc9da 041c
    lsls r4,r4,#0x5    @ 080dc9dc 6401
    ldr r0, DAT_080dca18                     @ 080dc9de 0e48
    adds r4,r4,r0    @ 080dc9e0 2418
    ldr r0, DAT_080dca1c                     @ 080dc9e2 0e48
    bl game_str_id_to_row                    @ 080dc9e4 18f018fa
    ldr r2, PTR_game_str_pointer_table_080dca20 @ 080dc9e8 0d4a
    lsls r0,r0,#0x10    @ 080dc9ea 0004
    lsrs r0,r0,#0x10    @ 080dc9ec 000c
    lsls r1,r0,#0x1    @ 080dc9ee 4100
    adds r1,r1,r0    @ 080dc9f0 0918
    lsls r1,r1,#0x1    @ 080dc9f2 4900
    ldr r0, DAT_080dca24                     @ 080dc9f4 0b48
    ldr r3, DAT_080dca28                     @ 080dc9f6 0c4b
    adds r0,r0,r3    @ 080dc9f8 c018
    ldrb r0,[r0,#0x0]                        @ 080dc9fa 0078
    lsls r0,r0,#0x1d    @ 080dc9fc 4007
    lsrs r0,r0,#0x1d    @ 080dc9fe 400f
    adds r1,r1,r0    @ 080dca00 0918
    lsls r1,r1,#0x2    @ 080dca02 8900
    adds r1,r1,r2    @ 080dca04 8918
    ldr r1,[r1,#0x0]                         @ 080dca06 0968
    ldr r0, PTR_game_str_ja_080dca2c         @ 080dca08 0848
    adds r1,r1,r0    @ 080dca0a 0918
    adds r0,r4,#0x0    @ 080dca0c 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dca0e fff7a3fd
    pop {r4}                                 @ 080dca12 10bc
    pop {r0}                                 @ 080dca14 01bc
    bx r0                                    @ 080dca16 0047
DAT_080dca18:
    .word  0x06010000                     @ 080dca18 00000106
DAT_080dca1c:
    .word  0x000013fb                     @ 080dca1c fb130000
PTR_game_str_pointer_table_080dca20:
    .word  game_str_pointer_table         @ 080dca20 400f0008
DAT_080dca24:
    .word  0x02000000                     @ 080dca24 00000002
DAT_080dca28:
    .word  0x00006c2c                     @ 080dca28 2c6c0000
PTR_game_str_ja_080dca2c:
    .word  game_str_ja                    @ 080dca2c 109cdb09

@ Renders the pack label string for game_str_id=0x7ee to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..653]; VRAM dst = 0x06010000 + r0*0x20.
@ Dispatched by FUN_080d511c switch dispatcher (case 2). Structurally symmetric to all siblings; differs only in game_str_id=0x7ee (lower ID range compared to 0x13xx series).
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x7ee // pack label string ID (low-range string segment)
@ 
@ Inputs: r0=u16 tile_row_base [0..653] (FUN_080d511c passes r2=0x28d=653 or 0x280=640; caller-set fixed value)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str7ee_to_bg_vram:
    push {r4,lr}                             @ 080dca30 10b5
    adds r4,r0,#0x0    @ 080dca32 041c
    lsls r4,r4,#0x5    @ 080dca34 6401
    ldr r0, DAT_080dca70                     @ 080dca36 0e48
    adds r4,r4,r0    @ 080dca38 2418
    ldr r0, DAT_080dca74                     @ 080dca3a 0e48
    bl game_str_id_to_row                    @ 080dca3c 18f0ecf9
    ldr r2, PTR_game_str_pointer_table_080dca78 @ 080dca40 0d4a
    lsls r0,r0,#0x10    @ 080dca42 0004
    lsrs r0,r0,#0x10    @ 080dca44 000c
    lsls r1,r0,#0x1    @ 080dca46 4100
    adds r1,r1,r0    @ 080dca48 0918
    lsls r1,r1,#0x1    @ 080dca4a 4900
    ldr r0, DAT_080dca7c                     @ 080dca4c 0b48
    ldr r3, DAT_080dca80                     @ 080dca4e 0c4b
    adds r0,r0,r3    @ 080dca50 c018
    ldrb r0,[r0,#0x0]                        @ 080dca52 0078
    lsls r0,r0,#0x1d    @ 080dca54 4007
    lsrs r0,r0,#0x1d    @ 080dca56 400f
    adds r1,r1,r0    @ 080dca58 0918
    lsls r1,r1,#0x2    @ 080dca5a 8900
    adds r1,r1,r2    @ 080dca5c 8918
    ldr r1,[r1,#0x0]                         @ 080dca5e 0968
    ldr r0, PTR_game_str_ja_080dca84         @ 080dca60 0848
    adds r1,r1,r0    @ 080dca62 0918
    adds r0,r4,#0x0    @ 080dca64 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dca66 fff777fd
    pop {r4}                                 @ 080dca6a 10bc
    pop {r0}                                 @ 080dca6c 01bc
    bx r0                                    @ 080dca6e 0047
DAT_080dca70:
    .word  0x06010000                     @ 080dca70 00000106
DAT_080dca74:
    .word  0x000007ee                     @ 080dca74 ee070000
PTR_game_str_pointer_table_080dca78:
    .word  game_str_pointer_table         @ 080dca78 400f0008
DAT_080dca7c:
    .word  0x02000000                     @ 080dca7c 00000002
DAT_080dca80:
    .word  0x00006c2c                     @ 080dca80 2c6c0000
PTR_game_str_ja_080dca84:
    .word  game_str_ja                    @ 080dca84 109cdb09

@ Renders the pack label string for game_str_id=0x7ef to BG VRAM at the tile row specified by tile_row_base.
@ r0=tile_row_base [0..653]; VRAM dst = 0x06010000 + r0*0x20.
@ Dispatched by FUN_080d511c switch dispatcher (case 4). Forms a 0x7ee/0x7ef string pair with render_pack_label_str7ee_to_bg_vram (0x080dca30).
@ 
@ Constants:
@ - VRAM_BASE=0x06010000 // BG VRAM base
@ - PACK_STRIDE=0x20 // tile stride
@ - GAME_STR_ID=0x7ef // pack label string ID (low-range string, paired with 0x7ee)
@ 
@ Inputs: r0=u16 tile_row_base [0..653] (FUN_080d511c passes r2=0x28d=653 or 0x280=640; caller-set fixed value)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x06010000 + tile_row_base*0x20 via render_pack_label_to_bg_tile_vram] tile data written
render_pack_label_str7ef_to_bg_vram:
    push {r4,lr}                             @ 080dca88 10b5
    adds r4,r0,#0x0    @ 080dca8a 041c
    lsls r4,r4,#0x5    @ 080dca8c 6401
    ldr r0, DAT_080dcac8                     @ 080dca8e 0e48
    adds r4,r4,r0    @ 080dca90 2418
    ldr r0, DAT_080dcacc                     @ 080dca92 0e48
    bl game_str_id_to_row                    @ 080dca94 18f0c0f9
    ldr r2, PTR_game_str_pointer_table_080dcad0 @ 080dca98 0d4a
    lsls r0,r0,#0x10    @ 080dca9a 0004
    lsrs r0,r0,#0x10    @ 080dca9c 000c
    lsls r1,r0,#0x1    @ 080dca9e 4100
    adds r1,r1,r0    @ 080dcaa0 0918
    lsls r1,r1,#0x1    @ 080dcaa2 4900
    ldr r0, DAT_080dcad4                     @ 080dcaa4 0b48
    ldr r3, DAT_080dcad8                     @ 080dcaa6 0c4b
    adds r0,r0,r3    @ 080dcaa8 c018
    ldrb r0,[r0,#0x0]                        @ 080dcaaa 0078
    lsls r0,r0,#0x1d    @ 080dcaac 4007
    lsrs r0,r0,#0x1d    @ 080dcaae 400f
    adds r1,r1,r0    @ 080dcab0 0918
    lsls r1,r1,#0x2    @ 080dcab2 8900
    adds r1,r1,r2    @ 080dcab4 8918
    ldr r1,[r1,#0x0]                         @ 080dcab6 0968
    ldr r0, PTR_game_str_ja_080dcadc         @ 080dcab8 0848
    adds r1,r1,r0    @ 080dcaba 0918
    adds r0,r4,#0x0    @ 080dcabc 201c
    bl render_pack_label_to_bg_tile_vram     @ 080dcabe fff74bfd
    pop {r4}                                 @ 080dcac2 10bc
    pop {r0}                                 @ 080dcac4 01bc
    bx r0                                    @ 080dcac6 0047
DAT_080dcac8:
    .word  0x06010000                     @ 080dcac8 00000106
DAT_080dcacc:
    .word  0x000007ef                     @ 080dcacc ef070000
PTR_game_str_pointer_table_080dcad0:
    .word  game_str_pointer_table         @ 080dcad0 400f0008
DAT_080dcad4:
    .word  0x02000000                     @ 080dcad4 00000002
DAT_080dcad8:
    .word  0x00006c2c                     @ 080dcad8 2c6c0000
PTR_game_str_ja_080dcadc:
    .word  game_str_ja                    @ 080dcadc 109cdb09

@ Sets bit in pack slot bitmap (base=0x020363c0) for the given slot code. r0 high 4 bits = slot index, low 4 bits = bit offset within halfword. Loads halfword at bitmap_base + slot_index*2, ORs in (1 << bit_index), writes back. Called by pack scene render loop to mark revealed/selected card slots.
@ 
@ Constants:
@ - 0x020363c0: pack slot bitmap base (IWRAM)
@ - 0xf: low nibble mask (bit index within halfword, [0..15])
set_pack_slot_flag_bit:
    ldr r1, DAT_080dcaf8                     @ 080dcae0 0549
    lsrs r2,r0,#0x4    @ 080dcae2 0209
    lsls r2,r2,#0x1    @ 080dcae4 5200
    adds r2,r2,r1    @ 080dcae6 5218
    movs r1,#0xf    @ 080dcae8 0f21
    ands r1,r0    @ 080dcaea 0140
    movs r0,#0x1    @ 080dcaec 0120
    lsls r0,r1    @ 080dcaee 8840
    ldrh r1,[r2,#0x0]                        @ 080dcaf0 1188
    orrs r0,r1    @ 080dcaf2 0843
    strh r0,[r2,#0x0]                        @ 080dcaf4 1080
    bx lr                                    @ 080dcaf6 7047
DAT_080dcaf8:
    .word  0x020363c0                     @ 080dcaf8 c0630302
    ROM_INCBIN 0xdcafc, 0x48

@ Reads halfword field at offset +0x2 from the specified pack_info_table entry. r0=pack_index; function shifts by *16 to get entry offset, loads halfword at +0x2 and returns it. Callers use the result as a bitfield: one caller compares to 5 (random path), another extracts low 4 bits as a sub-field.
@ 
@ Constants:
@ - pack_info_table: pack info table base (ROM 0x09e5e2e8)
@ - 0x10: pack_info entry size (16 bytes)
@ - +0x2: halfword field offset within entry
get_pack_info_attr2:
    ldr r1, PTR_pack_info_table_080dcb50     @ 080dcb44 0249
    lsls r0,r0,#0x4    @ 080dcb46 0001
    adds r0,r0,r1    @ 080dcb48 4018
    ldrh r0,[r0,#0x2]                        @ 080dcb4a 4088
    bx lr                                    @ 080dcb4c 7047
    .zero  0x2
PTR_pack_info_table_080dcb50:
    .word  pack_info_table                @ 080dcb50 e8e2e509

@ Copies text overlay dialog BG tile data from ROM to VRAM and configures BG display parameters. r0=(height<<16)|width defines dialog size; fetches current overlay object ptr from gPrng+0x1d0; reads BG field and BGxCNT register to determine tile/map base; calls copy_memory_dma3_with_cpu_fallback multiple times to write tile rows to VRAM; finally zero_fill_halfword_wrapper clears boundary. Called by text_overlay_create and FUN_080dd464 as BG init phase.
@ 
@ Constants:
@ - gPrng+0x1d0: current overlay object ptr (IWRAM overlay struct ptr)
@ - 0x09cede5c: overlay BG tile source data table base (ROM)
@ - BG0CNT=0x04000008: BG0 control register
@ - 0x000003ff: tilemap entry count (1023 tiles)
load_overlay_bg_tiles_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dcb54 f0b5
    .hword 0x4657    @ 080dcb56 5746
    .hword 0x464e    @ 080dcb58 4e46
    .hword 0x4645    @ 080dcb5a 4546
    push {r5,r6,r7}                          @ 080dcb5c e0b4
    sub sp,#0x20                             @ 080dcb5e 88b0
    adds r5,r0,#0x0    @ 080dcb60 051c
    ldr r0, PTR_gPrng_080dcd6c               @ 080dcb62 8248
    movs r1,#0xe8    @ 080dcb64 e821
    lsls r1,r1,#0x1    @ 080dcb66 4900
    adds r0,r0,r1    @ 080dcb68 4018
    ldr r0,[r0,#0x0]                         @ 080dcb6a 0068
    .hword 0x4682    @ 080dcb6c 8246
    cmp r0,#0x0                              @ 080dcb6e 0028
    bne LAB_080dcb74                         @ 080dcb70 00d1
    b LAB_080dcd5a                           @ 080dcb72 f2e0
LAB_080dcb74:
    ldr r1, DAT_080dcd70                     @ 080dcb74 7e49
    ldrh r2,[r0,#0x8]                        @ 080dcb76 0289
    lsls r0,r2,#0x2    @ 080dcb78 9000
    adds r0,r0,r1    @ 080dcb7a 4018
    ldr r0,[r0,#0x0]                         @ 080dcb7c 0068
    .hword 0x4680    @ 080dcb7e 8046
    .hword 0x4653    @ 080dcb80 5346
    ldrb r3,[r3,#0x3]                        @ 080dcb82 db78
    lsls r1,r3,#0x18    @ 080dcb84 1906
    lsrs r0,r1,#0x1e    @ 080dcb86 880f
    lsls r0,r0,#0x1    @ 080dcb88 4000
    ldr r4, PTR_BG0CNT_080dcd74              @ 080dcb8a 7a4c
    adds r0,r0,r4    @ 080dcb8c 0019
    ldrh r0,[r0,#0x0]                        @ 080dcb8e 0088
    movs r4,#0xc    @ 080dcb90 0c24
    ands r4,r0    @ 080dcb92 0440
    lsls r4,r4,#0xc    @ 080dcb94 2403
    .hword 0x4656    @ 080dcb96 5646
    ldrh r6,[r6,#0x2]                        @ 080dcb98 7688
    lsls r0,r6,#0x12    @ 080dcb9a b004
    lsrs r0,r0,#0xd    @ 080dcb9c 400b
    movs r2,#0xc0    @ 080dcb9e c022
    lsls r2,r2,#0x13    @ 080dcba0 d204
    adds r0,r0,r2    @ 080dcba2 8018
    adds r4,r4,r0    @ 080dcba4 2418
    lsrs r1,r1,#0x1e    @ 080dcba6 890f
    lsls r1,r1,#0x1    @ 080dcba8 4900
    ldr r3, PTR_BG0CNT_080dcd74              @ 080dcbaa 724b
    adds r1,r1,r3    @ 080dcbac c918
    ldrh r0,[r1,#0x0]                        @ 080dcbae 0888
    movs r1,#0xf8    @ 080dcbb0 f821
    lsls r1,r1,#0x5    @ 080dcbb2 4901
    ands r1,r0    @ 080dcbb4 0140
    lsls r1,r1,#0x3    @ 080dcbb6 c900
    .hword 0x4656    @ 080dcbb8 5646
    ldrh r6,[r6,#0x6]                        @ 080dcbba f688
    lsls r0,r6,#0x1    @ 080dcbbc 7000
    adds r0,r0,r2    @ 080dcbbe 8018
    adds r7,r1,r0    @ 080dcbc0 0f18
    .hword 0x4651    @ 080dcbc2 5146
    ldrh r1,[r1,#0x4]                        @ 080dcbc4 8988
    lsls r0,r1,#0x1c    @ 080dcbc6 0807
    lsrs r0,r0,#0x10    @ 080dcbc8 000c
    .hword 0x4681    @ 080dcbca 8146
    .hword 0x4641    @ 080dcbcc 4146
    adds r1,#0x80    @ 080dcbce 8031
    adds r0,r4,#0x0    @ 080dcbd0 201c
    movs r2,#0x20    @ 080dcbd2 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcbd4 18f098f9
    adds r0,r4,#0x0    @ 080dcbd8 201c
    adds r0,#0x20    @ 080dcbda 2030
    lsls r2,r5,#0x10    @ 080dcbdc 2a04
    str r2,[sp,#0x0]                         @ 080dcbde 0092
    lsrs r6,r2,#0x10    @ 080dcbe0 160c
    subs r6,#0x2    @ 080dcbe2 023e
    lsrs r5,r5,#0x10    @ 080dcbe4 2d0c
    str r5,[sp,#0x4]                         @ 080dcbe6 0195
    subs r5,#0x2    @ 080dcbe8 023d
    adds r3,r6,#0x0    @ 080dcbea 331c
    muls r3,r5    @ 080dcbec 6b43
    str r3,[sp,#0x8]                         @ 080dcbee 0293
    adds r2,r3,#0x0    @ 080dcbf0 1a1c
    subs r2,#0x1    @ 080dcbf2 013a
    lsls r2,r2,#0x5    @ 080dcbf4 5201
    adds r1,r4,#0x0    @ 080dcbf6 211c
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcbf8 18f086f9
    lsls r5,r5,#0x5    @ 080dcbfc 6d01
    adds r0,r6,#0x0    @ 080dcbfe 301c
    muls r0,r5    @ 080dcc00 6843
    adds r4,r4,r0    @ 080dcc02 2418
    adds r0,r4,#0x0    @ 080dcc04 201c
    .hword 0x4641    @ 080dcc06 4146
    movs r2,#0x80    @ 080dcc08 8022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcc0a 18f07df9
    movs r5,#0xa0    @ 080dcc0e a025
    add r8,r5                                @ 080dcc10 a844
    adds r4,#0x80    @ 080dcc12 8034
    adds r0,r4,#0x0    @ 080dcc14 201c
    .hword 0x4641    @ 080dcc16 4146
    movs r2,#0x80    @ 080dcc18 8022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcc1a 18f075f9
    adds r4,#0x80    @ 080dcc1e 8034
    adds r0,r4,#0x0    @ 080dcc20 201c
    movs r1,#0x20    @ 080dcc22 2021
    bl zero_fill_halfword_wrapper            @ 080dcc24 18f038f9
    .hword 0x4656    @ 080dcc28 5646
    ldrh r6,[r6,#0x2]                        @ 080dcc2a 7688
    lsls r0,r6,#0x12    @ 080dcc2c b004
    lsrs r1,r0,#0x12    @ 080dcc2e 810c
    .hword 0x468c    @ 080dcc30 8c46
    adds r0,r1,#0x0    @ 080dcc32 081c
    ldr r2,[sp,#0x8]                         @ 080dcc34 029a
    adds r0,r0,r2    @ 080dcc36 8018
    lsls r0,r0,#0x10    @ 080dcc38 0004
    lsrs r2,r0,#0x10    @ 080dcc3a 020c
    .hword 0x4653    @ 080dcc3c 5346
    ldrb r3,[r3,#0x3]                        @ 080dcc3e db78
    lsrs r0,r3,#0x6    @ 080dcc40 9809
    lsls r0,r0,#0x1    @ 080dcc42 4000
    ldr r4, PTR_BG0CNT_080dcd74              @ 080dcc44 4b4c
    adds r0,r0,r4    @ 080dcc46 0019
    ldrh r0,[r0,#0x0]                        @ 080dcc48 0088
    movs r5,#0xf8    @ 080dcc4a f825
    lsls r5,r5,#0x5    @ 080dcc4c 6d01
    ands r5,r0    @ 080dcc4e 0540
    lsls r6,r5,#0x3    @ 080dcc50 ee00
    movs r0,#0xc0    @ 080dcc52 c020
    lsls r0,r0,#0x13    @ 080dcc54 c004
    adds r1,r6,r0    @ 080dcc56 3118
    movs r3,#0x0    @ 080dcc58 0023
    ldr r4, DAT_080dcd78                     @ 080dcc5a 474c
    ldr r5,[sp,#0x0]                         @ 080dcc5c 009d
    .hword 0x46aa    @ 080dcc5e aa46
    ldr r5,[sp,#0x4]                         @ 080dcc60 019d
    adds r0,r2,#0x0    @ 080dcc62 101c
    adds r0,#0x8    @ 080dcc64 0830
    .hword 0x464e    @ 080dcc66 4e46
    orrs r0,r6    @ 080dcc68 3043
LAB_080dcc6a:
    strh r0,[r1,#0x0]                        @ 080dcc6a 0880
    adds r1,#0x2    @ 080dcc6c 0231
    adds r3,#0x1    @ 080dcc6e 0133
    cmp r3,r4                                @ 080dcc70 a342
    bls LAB_080dcc6a                         @ 080dcc72 fad9
    adds r0,r2,#0x0    @ 080dcc74 101c
    adds r1,r0,#0x1    @ 080dcc76 411c
    lsls r1,r1,#0x10    @ 080dcc78 0904
    lsrs r2,r1,#0x10    @ 080dcc7a 0a0c
    .hword 0x4649    @ 080dcc7c 4946
    orrs r0,r1    @ 080dcc7e 0843
    strh r0,[r7,#0x0]                        @ 080dcc80 3880
    adds r7,#0x2    @ 080dcc82 0237
    movs r3,#0x1    @ 080dcc84 0123
    .hword 0x4654    @ 080dcc86 5446
    lsrs r0,r4,#0x10    @ 080dcc88 200c
    subs r0,#0x1    @ 080dcc8a 0138
    cmp r3,r0                                @ 080dcc8c 8342
    bcs LAB_080dcca0                         @ 080dcc8e 07d2
    adds r1,r2,#0x0    @ 080dcc90 111c
    .hword 0x464e    @ 080dcc92 4e46
    orrs r1,r6    @ 080dcc94 3143
LAB_080dcc96:
    strh r1,[r7,#0x0]                        @ 080dcc96 3980
    adds r7,#0x2    @ 080dcc98 0237
    adds r3,#0x1    @ 080dcc9a 0133
    cmp r3,r0                                @ 080dcc9c 8342
    bcc LAB_080dcc96                         @ 080dcc9e fad3
LAB_080dcca0:
    adds r0,r2,#0x1    @ 080dcca0 501c
    lsls r0,r0,#0x10    @ 080dcca2 0004
    lsrs r2,r0,#0x10    @ 080dcca4 020c
    adds r1,r2,#0x0    @ 080dcca6 111c
    adds r0,r1,#0x1    @ 080dcca8 481c
    lsls r0,r0,#0x10    @ 080dccaa 0004
    lsrs r2,r0,#0x10    @ 080dccac 020c
    .hword 0x4648    @ 080dccae 4846
    orrs r1,r0    @ 080dccb0 0143
    strh r1,[r7,#0x0]                        @ 080dccb2 3980
    adds r7,#0x2    @ 080dccb4 0237
    .hword 0x4651    @ 080dccb6 5146
    lsrs r3,r1,#0x10    @ 080dccb8 0b0c
    movs r0,#0x20    @ 080dccba 2020
    subs r0,r0,r3    @ 080dccbc c01a
    lsls r4,r0,#0x1    @ 080dccbe 4400
    adds r7,r7,r4    @ 080dccc0 3f19
    movs r1,#0x1    @ 080dccc2 0121
    subs r0,r5,#0x1    @ 080dccc4 681e
    cmp r1,r0                                @ 080dccc6 8142
    bcs LAB_080dcd1c                         @ 080dccc8 28d2
    .hword 0x4655    @ 080dccca 5546
    str r5,[sp,#0x18]                        @ 080dcccc 0695
    subs r3,#0x1    @ 080dccce 013b
    str r3,[sp,#0x1c]                        @ 080dccd0 0793
    adds r6,r2,#0x1    @ 080dccd2 561c
    .hword 0x464b    @ 080dccd4 4b46
    orrs r6,r3    @ 080dccd6 1e43
    str r4,[sp,#0x14]                        @ 080dccd8 0594
    .hword 0x4680    @ 080dccda 8046
LAB_080dccdc:
    adds r0,r2,#0x0    @ 080dccdc 101c
    .hword 0x464c    @ 080dccde 4c46
    orrs r0,r4    @ 080dcce0 2043
    strh r0,[r7,#0x0]                        @ 080dcce2 3880
    adds r7,#0x2    @ 080dcce4 0237
    movs r3,#0x1    @ 080dcce6 0123
    adds r5,r1,#0x1    @ 080dcce8 4d1c
    ldr r0,[sp,#0x1c]                        @ 080dccea 0798
    cmp r3,r0                                @ 080dccec 8342
    bcs LAB_080dcd0e                         @ 080dccee 0ed2
    ldr r1,[sp,#0x18]                        @ 080dccf0 0699
    lsrs r0,r1,#0x10    @ 080dccf2 080c
    subs r4,r0,#0x1    @ 080dccf4 441e
LAB_080dccf6:
    .hword 0x4661    @ 080dccf6 6146
    adds r0,r1,#0x1    @ 080dccf8 481c
    lsls r0,r0,#0x10    @ 080dccfa 0004
    lsrs r0,r0,#0x10    @ 080dccfc 000c
    .hword 0x4684    @ 080dccfe 8446
    .hword 0x4648    @ 080dcd00 4846
    orrs r1,r0    @ 080dcd02 0143
    strh r1,[r7,#0x0]                        @ 080dcd04 3980
    adds r7,#0x2    @ 080dcd06 0237
    adds r3,#0x1    @ 080dcd08 0133
    cmp r3,r4                                @ 080dcd0a a342
    bcc LAB_080dccf6                         @ 080dcd0c f3d3
LAB_080dcd0e:
    strh r6,[r7,#0x0]                        @ 080dcd0e 3e80
    adds r7,#0x2    @ 080dcd10 0237
    ldr r1,[sp,#0x14]                        @ 080dcd12 0599
    adds r7,r7,r1    @ 080dcd14 7f18
    adds r1,r5,#0x0    @ 080dcd16 291c
    cmp r1,r8                                @ 080dcd18 4145
    bcc LAB_080dccdc                         @ 080dcd1a dfd3
LAB_080dcd1c:
    adds r0,r2,#0x2    @ 080dcd1c 901c
    lsls r0,r0,#0x10    @ 080dcd1e 0004
    lsrs r2,r0,#0x10    @ 080dcd20 020c
    adds r1,r2,#0x0    @ 080dcd22 111c
    adds r0,r1,#0x1    @ 080dcd24 481c
    lsls r0,r0,#0x10    @ 080dcd26 0004
    lsrs r2,r0,#0x10    @ 080dcd28 020c
    .hword 0x464b    @ 080dcd2a 4b46
    orrs r1,r3    @ 080dcd2c 1943
    strh r1,[r7,#0x0]                        @ 080dcd2e 3980
    adds r7,#0x2    @ 080dcd30 0237
    movs r3,#0x1    @ 080dcd32 0123
    .hword 0x4654    @ 080dcd34 5446
    lsrs r0,r4,#0x10    @ 080dcd36 200c
    subs r0,#0x1    @ 080dcd38 0138
    cmp r3,r0                                @ 080dcd3a 8342
    bcs LAB_080dcd4e                         @ 080dcd3c 07d2
    adds r1,r2,#0x0    @ 080dcd3e 111c
    .hword 0x464d    @ 080dcd40 4d46
    orrs r1,r5    @ 080dcd42 2943
LAB_080dcd44:
    strh r1,[r7,#0x0]                        @ 080dcd44 3980
    adds r7,#0x2    @ 080dcd46 0237
    adds r3,#0x1    @ 080dcd48 0133
    cmp r3,r0                                @ 080dcd4a 8342
    bcc LAB_080dcd44                         @ 080dcd4c fad3
LAB_080dcd4e:
    adds r0,r2,#0x1    @ 080dcd4e 501c
    lsls r0,r0,#0x10    @ 080dcd50 0004
    lsrs r0,r0,#0x10    @ 080dcd52 000c
    .hword 0x464e    @ 080dcd54 4e46
    orrs r0,r6    @ 080dcd56 3043
    strh r0,[r7,#0x0]                        @ 080dcd58 3880
LAB_080dcd5a:
    add sp,#0x20                             @ 080dcd5a 08b0
    pop {r3,r4,r5}                           @ 080dcd5c 38bc
    .hword 0x4698    @ 080dcd5e 9846
    .hword 0x46a1    @ 080dcd60 a146
    .hword 0x46aa    @ 080dcd62 aa46
    pop {r4,r5,r6,r7}                        @ 080dcd64 f0bc
    pop {r0}                                 @ 080dcd66 01bc
    bx r0                                    @ 080dcd68 0047
    .zero  0x2
PTR_gPrng_080dcd6c:
    .word  gPrng                          @ 080dcd6c 40000003
DAT_080dcd70:
    .word  0x09cede5c                     @ 080dcd70 5cdece09
PTR_BG0CNT_080dcd74:
    .word  BG0CNT                         @ 080dcd74 08000004
DAT_080dcd78:
    .word  0x000003ff                     @ 080dcd78 ff030000

@ Variant of load_overlay_bg_tiles_to_vram: writes overlay dialog BG tile data to a different group of VRAM addresses. Fetches overlay object ptr from gPrng+0x1d0; if NULL returns immediately; uses fixed destinations 0x06010000/0x06010020/0x06010040, copies multiple 0x20-byte tile rows. Called by text_overlay_create (BG mode=0 branch) and FUN_080dd464; forms _alt pair with load_overlay_bg_tiles_to_vram (0x080dcb54).
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct ptr
@ - 0x09cede5c: overlay tile source data table (ROM)
@ - 0x06010000: VRAM OBJ tile slot 0 (32 bytes)
@ - 0x06010020: VRAM OBJ tile slot 1 (32 bytes)
@ - 0x06010040: VRAM OBJ tile slot 2 (32 bytes)
load_overlay_bg_tiles_to_vram_alt:
    push {r4,r5,r6,r7,lr}                    @ 080dcd7c f0b5
    .hword 0x4657    @ 080dcd7e 5746
    .hword 0x464e    @ 080dcd80 4e46
    .hword 0x4645    @ 080dcd82 4546
    push {r5,r6,r7}                          @ 080dcd84 e0b4
    .hword 0x4682    @ 080dcd86 8246
    ldr r0, PTR_gPrng_080dcebc               @ 080dcd88 4c48
    movs r1,#0xe8    @ 080dcd8a e821
    lsls r1,r1,#0x1    @ 080dcd8c 4900
    adds r0,r0,r1    @ 080dcd8e 4018
    ldr r2,[r0,#0x0]                         @ 080dcd90 0268
    cmp r2,#0x0                              @ 080dcd92 002a
    bne LAB_080dcd98                         @ 080dcd94 00d1
    b LAB_080dceac                           @ 080dcd96 89e0
LAB_080dcd98:
    ldr r1, DAT_080dcec0                     @ 080dcd98 4949
    ldrh r3,[r2,#0x8]                        @ 080dcd9a 1389
    lsls r0,r3,#0x2    @ 080dcd9c 9800
    adds r0,r0,r1    @ 080dcd9e 4018
    ldr r6,[r0,#0x0]                         @ 080dcda0 0668
    ldrh r2,[r2,#0x2]                        @ 080dcda2 5288
    lsls r4,r2,#0x12    @ 080dcda4 9404
    lsrs r4,r4,#0xd    @ 080dcda6 640b
    ldr r0, DAT_080dcec4                     @ 080dcda8 4648
    adds r7,r4,r0    @ 080dcdaa 2718
    adds r0,r7,#0x0    @ 080dcdac 381c
    adds r1,r6,#0x0    @ 080dcdae 311c
    movs r2,#0x20    @ 080dcdb0 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcdb2 18f0a9f8
    adds r6,#0x20    @ 080dcdb6 2036
    ldr r1, DAT_080dcec8                     @ 080dcdb8 4349
    adds r7,r4,r1    @ 080dcdba 6718
    adds r0,r7,#0x0    @ 080dcdbc 381c
    adds r1,r6,#0x0    @ 080dcdbe 311c
    movs r2,#0x20    @ 080dcdc0 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcdc2 18f0a1f8
    ldr r3, DAT_080dcecc                     @ 080dcdc6 414b
    adds r4,r4,r3    @ 080dcdc8 e418
    .hword 0x4650    @ 080dcdca 5046
    lsls r0,r0,#0x10    @ 080dcdcc 0004
    .hword 0x4681    @ 080dcdce 8146
    lsrs r0,r0,#0x10    @ 080dcdd0 000c
    .hword 0x4680    @ 080dcdd2 8046
    .hword 0x4645    @ 080dcdd4 4546
    subs r5,#0x3    @ 080dcdd6 033d
    lsls r5,r5,#0x5    @ 080dcdd8 6d01
    adds r0,r4,#0x0    @ 080dcdda 201c
    adds r1,r7,#0x0    @ 080dcddc 391c
    adds r2,r5,#0x0    @ 080dcdde 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcde0 18f092f8
    adds r6,#0x20    @ 080dcde4 2036
    .hword 0x4644    @ 080dcde6 4446
    subs r4,#0x2    @ 080dcde8 023c
    lsls r4,r4,#0x5    @ 080dcdea 6401
    adds r7,r7,r4    @ 080dcdec 3f19
    adds r0,r7,#0x0    @ 080dcdee 381c
    adds r1,r6,#0x0    @ 080dcdf0 311c
    movs r2,#0x20    @ 080dcdf2 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcdf4 18f088f8
    adds r6,#0x20    @ 080dcdf8 2036
    movs r0,#0x21    @ 080dcdfa 2120
    .hword 0x4641    @ 080dcdfc 4146
    subs r0,r0,r1    @ 080dcdfe 401a
    lsls r0,r0,#0x5    @ 080dce00 4001
    adds r7,r7,r0    @ 080dce02 3f18
    adds r0,r7,#0x0    @ 080dce04 381c
    adds r1,r6,#0x0    @ 080dce06 311c
    movs r2,#0x20    @ 080dce08 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce0a 18f07df8
    adds r6,#0x20    @ 080dce0e 2036
    adds r7,#0x20    @ 080dce10 2037
    adds r0,r7,#0x0    @ 080dce12 381c
    adds r1,r6,#0x0    @ 080dce14 311c
    movs r2,#0x20    @ 080dce16 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce18 18f076f8
    adds r0,r7,#0x0    @ 080dce1c 381c
    adds r0,#0x20    @ 080dce1e 2030
    adds r1,r7,#0x0    @ 080dce20 391c
    adds r2,r5,#0x0    @ 080dce22 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce24 18f070f8
    adds r6,#0x20    @ 080dce28 2036
    adds r7,r7,r4    @ 080dce2a 3f19
    adds r0,r7,#0x0    @ 080dce2c 381c
    adds r1,r6,#0x0    @ 080dce2e 311c
    movs r2,#0x20    @ 080dce30 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce32 18f069f8
    .hword 0x4640    @ 080dce36 4046
    subs r0,#0x1    @ 080dce38 0138
    lsls r0,r0,#0x5    @ 080dce3a 4001
    subs r7,r7,r0    @ 080dce3c 3f1a
    movs r5,#0x2    @ 080dce3e 0225
    .hword 0x4653    @ 080dce40 5346
    lsrs r0,r3,#0x10    @ 080dce42 180c
    subs r0,#0x1    @ 080dce44 0138
    .hword 0x46ca    @ 080dce46 ca46
    cmp r5,r0                                @ 080dce48 8542
    bcs LAB_080dce68                         @ 080dce4a 0dd2
    .hword 0x4681    @ 080dce4c 8146
LAB_080dce4e:
    movs r0,#0x80    @ 080dce4e 8020
    lsls r0,r0,#0x3    @ 080dce50 c000
    adds r4,r7,r0    @ 080dce52 3c18
    adds r0,r4,#0x0    @ 080dce54 201c
    adds r1,r7,#0x0    @ 080dce56 391c
    .hword 0x4643    @ 080dce58 4346
    lsls r2,r3,#0x5    @ 080dce5a 5a01
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce5c 18f054f8
    adds r7,r4,#0x0    @ 080dce60 271c
    adds r5,#0x1    @ 080dce62 0135
    cmp r5,r9                                @ 080dce64 4d45
    bcc LAB_080dce4e                         @ 080dce66 f2d3
LAB_080dce68:
    adds r6,#0x20    @ 080dce68 2036
    movs r0,#0x80    @ 080dce6a 8020
    lsls r0,r0,#0x3    @ 080dce6c c000
    adds r7,r7,r0    @ 080dce6e 3f18
    adds r0,r7,#0x0    @ 080dce70 381c
    adds r1,r6,#0x0    @ 080dce72 311c
    movs r2,#0x20    @ 080dce74 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce76 18f047f8
    adds r6,#0x20    @ 080dce7a 2036
    adds r7,#0x20    @ 080dce7c 2037
    adds r0,r7,#0x0    @ 080dce7e 381c
    adds r1,r6,#0x0    @ 080dce80 311c
    movs r2,#0x20    @ 080dce82 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce84 18f040f8
    adds r0,r7,#0x0    @ 080dce88 381c
    adds r0,#0x20    @ 080dce8a 2030
    .hword 0x4651    @ 080dce8c 5146
    lsrs r4,r1,#0x10    @ 080dce8e 0c0c
    subs r2,r4,#0x3    @ 080dce90 e21e
    lsls r2,r2,#0x5    @ 080dce92 5201
    adds r1,r7,#0x0    @ 080dce94 391c
    bl copy_memory_dma3_with_cpu_fallback    @ 080dce96 18f037f8
    adds r6,#0x20    @ 080dce9a 2036
    subs r4,#0x2    @ 080dce9c 023c
    lsls r4,r4,#0x5    @ 080dce9e 6401
    adds r7,r7,r4    @ 080dcea0 3f19
    adds r0,r7,#0x0    @ 080dcea2 381c
    adds r1,r6,#0x0    @ 080dcea4 311c
    movs r2,#0x20    @ 080dcea6 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dcea8 18f02ef8
LAB_080dceac:
    pop {r3,r4,r5}                           @ 080dceac 38bc
    .hword 0x4698    @ 080dceae 9846
    .hword 0x46a1    @ 080dceb0 a146
    .hword 0x46aa    @ 080dceb2 aa46
    pop {r4,r5,r6,r7}                        @ 080dceb4 f0bc
    pop {r0}                                 @ 080dceb6 01bc
    bx r0                                    @ 080dceb8 0047
    .zero  0x2
PTR_gPrng_080dcebc:
    .word  gPrng                          @ 080dcebc 40000003
DAT_080dcec0:
    .word  0x09cede5c                     @ 080dcec0 5cdece09
DAT_080dcec4:
    .word  0x06010000                     @ 080dcec4 00000106
DAT_080dcec8:
    .word  0x06010020                     @ 080dcec8 20000106
DAT_080dcecc:
    .word  0x06010040                     @ 080dcecc 40000106

@ Renders a JP text string to the BG VRAM area of the current text overlay layer.
@ Reads overlay_ptr from gPrng+0x1d0; returns void if null or if overlay[+0x18] is null.
@ Determines font width modifier (2 or 4) from overlay[+0x14] flags bit1; reads overlay[+0xe/+0x10] as content area width/height (each minus 2); calls setup_line_buf_font_with_align_and_slot.
@ Manipulates 0x02006ed0 font control bytes (bit0..2 orrs/ands). Calls render_jp_string_nowrap_with_offset for the JP string; uses return width for horizontal centering. Calls text_render_wrapper twice. Updates overlay scroll field at overlay[+0xa]. Finally calls blit_tile_nibble_row_msb or blit_tile_nibble_row_lsb based on flags bit0 to write to BG tile VRAM.
@ Called by FUN_080dd4ac (overlay size update) and text_overlay_create.
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct pointer (gPrng+0xe8*2)
@ - 0x02006ed0: line buffer font control struct base
@ - 0x06010420: blit_tile_nibble_row_lsb default target base (DAT_080dd06c)
@ - 0x000003ff: tile index mask (DAT_080dd040)
@ - 0xfffff003: tile clear mask (DAT_080dd044)
@ 
@ Inputs: r0=const char* str_ptr (stored at [sp+0x4])
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [0x02006ed0+0x8/0x14/0x15] font control bytes; [overlay+0xa] tile index scroll field; [BG tile VRAM via blit_tile_nibble_row_msb/lsb]
render_overlay_text_to_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 080dced0 f0b5
    .hword 0x4657    @ 080dced2 5746
    .hword 0x464e    @ 080dced4 4e46
    .hword 0x4645    @ 080dced6 4546
    push {r5,r6,r7}                          @ 080dced8 e0b4
    sub sp,#0x8                              @ 080dceda 82b0
    str r0,[sp,#0x4]                         @ 080dcedc 0190
    ldr r0, PTR_gPrng_080dd034               @ 080dcede 5548
    movs r1,#0xe8    @ 080dcee0 e821
    lsls r1,r1,#0x1    @ 080dcee2 4900
    adds r0,r0,r1    @ 080dcee4 4018
    ldr r7,[r0,#0x0]                         @ 080dcee6 0768
    cmp r7,#0x0                              @ 080dcee8 002f
    bne LAB_080dceee                         @ 080dceea 00d1
    b LAB_080dd05c                           @ 080dceec b6e0
LAB_080dceee:
    ldr r1,[r7,#0x14]                        @ 080dceee 7969
    lsrs r4,r1,#0x1    @ 080dcef0 4c08
    movs r2,#0x1    @ 080dcef2 0122
    ands r4,r2    @ 080dcef4 1440
    movs r0,#0x2    @ 080dcef6 0220
    ands r1,r0    @ 080dcef8 0140
    movs r5,#0x2    @ 080dcefa 0225
    cmp r1,#0x0                              @ 080dcefc 0029
    beq LAB_080dcf02                         @ 080dcefe 00d0
    movs r5,#0x4    @ 080dcf00 0425
LAB_080dcf02:
    ldr r0,[r7,#0x18]                        @ 080dcf02 b869
    cmp r0,#0x0                              @ 080dcf04 0028
    bne LAB_080dcf0a                         @ 080dcf06 00d1
    b LAB_080dd05c                           @ 080dcf08 a8e0
LAB_080dcf0a:
    ldrh r0,[r7,#0xe]                        @ 080dcf0a f889
    subs r0,#0x2    @ 080dcf0c 0238
    ldrh r1,[r7,#0x10]                       @ 080dcf0e 398a
    subs r1,#0x2    @ 080dcf10 0239
    movs r2,#0x1    @ 080dcf12 0122
    adds r3,r5,#0x0    @ 080dcf14 2b1c
    bl setup_line_buf_font_with_align_and_slot @ 080dcf16 13f01bff
    ldr r6, DAT_080dd038                     @ 080dcf1a 474e
    movs r1,#0x1    @ 080dcf1c 0121
    ldrb r0,[r6,#0x15]                       @ 080dcf1e 707d
    orrs r0,r1    @ 080dcf20 0843
    strb r0,[r6,#0x15]                       @ 080dcf22 7075
    adds r0,r4,#0x0    @ 080dcf24 201c
    ands r0,r1    @ 080dcf26 0840
    lsls r0,r0,#0x1    @ 080dcf28 4000
    movs r1,#0x3    @ 080dcf2a 0321
    rsbs r1,r1,#0    @ 080dcf2c 4942
    ldrb r3,[r6,#0x8]                        @ 080dcf2e 337a
    ands r1,r3    @ 080dcf30 1940
    orrs r1,r0    @ 080dcf32 0143
    strb r1,[r6,#0x8]                        @ 080dcf34 3172
    lsls r2,r5,#0x2    @ 080dcf36 aa00
    movs r0,#0x7d    @ 080dcf38 7d20
    rsbs r0,r0,#0    @ 080dcf3a 4042
    ldrb r3,[r6,#0x14]                       @ 080dcf3c 337d
    ands r0,r3    @ 080dcf3e 1840
    orrs r0,r2    @ 080dcf40 1043
    strb r0,[r6,#0x14]                       @ 080dcf42 3075
    ldr r2, PTR_font_jp_base_table_080dd03c  @ 080dcf44 3d4a
    lsls r0,r1,#0x1e    @ 080dcf46 8807
    lsrs r0,r0,#0x1f    @ 080dcf48 c00f
    lsls r0,r0,#0x2    @ 080dcf4a 8000
    lsls r1,r1,#0x1f    @ 080dcf4c c907
    lsrs r1,r1,#0x1f    @ 080dcf4e c90f
    lsls r1,r1,#0x3    @ 080dcf50 c900
    adds r0,r0,r1    @ 080dcf52 4018
    adds r0,r0,r2    @ 080dcf54 8018
    ldr r0,[r0,#0x0]                         @ 080dcf56 0068
    str r0,[r6,#0x4]                         @ 080dcf58 7060
    lsls r4,r4,#0x18    @ 080dcf5a 2406
    .hword 0x46a2    @ 080dcf5c a246
    .hword 0x4650    @ 080dcf5e 5046
    lsrs r0,r0,#0x10    @ 080dcf60 000c
    .hword 0x4682    @ 080dcf62 8246
    movs r0,#0x8    @ 080dcf64 0820
    .hword 0x4654    @ 080dcf66 5446
    orrs r4,r0    @ 080dcf68 0443
    movs r1,#0x1    @ 080dcf6a 0121
    str r1,[sp,#0x0]                         @ 080dcf6c 0091
    movs r0,#0x1    @ 080dcf6e 0120
    adds r2,r4,#0x0    @ 080dcf70 221c
    ldr r3,[sp,#0x4]                         @ 080dcf72 019b
    bl render_jp_string_nowrap_with_offset   @ 080dcf74 15f074fd
    ldrh r2,[r7,#0xe]                        @ 080dcf78 fa89
    subs r2,#0x2    @ 080dcf7a 023a
    lsls r2,r2,#0x3    @ 080dcf7c d200
    lsls r1,r0,#0x10    @ 080dcf7e 0104
    lsrs r1,r1,#0x10    @ 080dcf80 090c
    subs r2,r2,r1    @ 080dcf82 521a
    asrs r2,r2,#0x1    @ 080dcf84 5210
    .hword 0x4690    @ 080dcf86 9046
    ldrh r5,[r7,#0x10]                       @ 080dcf88 3d8a
    subs r5,#0x2    @ 080dcf8a 023d
    lsls r5,r5,#0x3    @ 080dcf8c ed00
    lsrs r0,r0,#0x10    @ 080dcf8e 000c
    subs r5,r5,r0    @ 080dcf90 2d1a
    asrs r5,r5,#0x1    @ 080dcf92 6d10
    movs r3,#0x41    @ 080dcf94 4123
    rsbs r3,r3,#0    @ 080dcf96 5b42
    .hword 0x4699    @ 080dcf98 9946
    .hword 0x4648    @ 080dcf9a 4846
    ldrb r1,[r6,#0x15]                       @ 080dcf9c 717d
    ands r0,r1    @ 080dcf9e 0840
    strb r0,[r6,#0x15]                       @ 080dcfa0 7075
    .hword 0x4640    @ 080dcfa2 4046
    adds r0,#0x1    @ 080dcfa4 0130
    adds r1,r5,#0x1    @ 080dcfa6 691c
    adds r2,r4,#0x0    @ 080dcfa8 221c
    ldr r3,[sp,#0x4]                         @ 080dcfaa 019b
    bl text_render_wrapper                   @ 080dcfac 15f066fd
    movs r0,#0x40    @ 080dcfb0 4020
    ldrb r2,[r6,#0x15]                       @ 080dcfb2 727d
    orrs r0,r2    @ 080dcfb4 1043
    strb r0,[r6,#0x15]                       @ 080dcfb6 7075
    ldrh r2,[r6,#0xa]                        @ 080dcfb8 7289
    lsls r1,r2,#0x14    @ 080dcfba 1105
    lsrs r1,r1,#0x16    @ 080dcfbc 890d
    subs r1,#0x1    @ 080dcfbe 0139
    ldr r3, DAT_080dd040                     @ 080dcfc0 1f4b
    ands r1,r3    @ 080dcfc2 1940
    lsls r1,r1,#0x2    @ 080dcfc4 8900
    ldr r4, DAT_080dd044                     @ 080dcfc6 1f4c
    adds r0,r4,#0x0    @ 080dcfc8 201c
    ands r0,r2    @ 080dcfca 1040
    orrs r0,r1    @ 080dcfcc 0843
    strh r0,[r6,#0xa]                        @ 080dcfce 7081
    movs r0,#0x7    @ 080dcfd0 0720
    .hword 0x4651    @ 080dcfd2 5146
    orrs r1,r0    @ 080dcfd4 0143
    .hword 0x468a    @ 080dcfd6 8a46
    .hword 0x4640    @ 080dcfd8 4046
    adds r1,r5,#0x0    @ 080dcfda 291c
    .hword 0x4652    @ 080dcfdc 5246
    ldr r3,[sp,#0x4]                         @ 080dcfde 019b
    bl text_render_wrapper                   @ 080dcfe0 15f04cfd
    ldrh r1,[r6,#0xa]                        @ 080dcfe4 7189
    lsls r0,r1,#0x14    @ 080dcfe6 0805
    lsrs r0,r0,#0x16    @ 080dcfe8 800d
    adds r0,#0x1    @ 080dcfea 0130
    ldr r2, DAT_080dd040                     @ 080dcfec 144a
    ands r0,r2    @ 080dcfee 1040
    lsls r0,r0,#0x2    @ 080dcff0 8000
    ands r4,r1    @ 080dcff2 0c40
    orrs r4,r0    @ 080dcff4 0443
    strh r4,[r6,#0xa]                        @ 080dcff6 7481
    ldrb r3,[r6,#0x15]                       @ 080dcff8 737d
    .hword 0x4648    @ 080dcffa 4846
    ands r3,r0    @ 080dcffc 0340
    strb r3,[r6,#0x15]                       @ 080dcffe 7375
    ldr r0,[r7,#0x14]                        @ 080dd000 7869
    movs r1,#0x1    @ 080dd002 0121
    ands r0,r1    @ 080dd004 0840
    cmp r0,#0x0                              @ 080dd006 0028
    beq LAB_080dd04c                         @ 080dd008 20d0
    ldrb r2,[r7,#0x3]                        @ 080dd00a fa78
    lsrs r0,r2,#0x6    @ 080dd00c 9009
    lsls r0,r0,#0x1    @ 080dd00e 4000
    ldr r1, PTR_BG0CNT_080dd048              @ 080dd010 0d49
    adds r0,r0,r1    @ 080dd012 4018
    ldrh r1,[r0,#0x0]                        @ 080dd014 0188
    movs r0,#0xc    @ 080dd016 0c20
    ands r0,r1    @ 080dd018 0840
    lsls r0,r0,#0xc    @ 080dd01a 0003
    ldrh r7,[r7,#0x2]                        @ 080dd01c 7f88
    lsls r1,r7,#0x12    @ 080dd01e b904
    lsrs r1,r1,#0xd    @ 080dd020 490b
    movs r2,#0xc0    @ 080dd022 c022
    lsls r2,r2,#0x13    @ 080dd024 d204
    adds r1,r1,r2    @ 080dd026 8918
    adds r0,r0,r1    @ 080dd028 4018
    movs r1,#0x0    @ 080dd02a 0021
    bl blit_tile_nibble_row_msb              @ 080dd02c 16f056fa
    b LAB_080dd05c                           @ 080dd030 14e0
    .zero  0x2
PTR_gPrng_080dd034:
    .word  gPrng                          @ 080dd034 40000003
DAT_080dd038:
    .word  0x02006ed0                     @ 080dd038 d06e0002
PTR_font_jp_base_table_080dd03c:
    .word  font_jp_base_table             @ 080dd03c 54f8e509
DAT_080dd040:
    .word  0x000003ff                     @ 080dd040 ff030000
DAT_080dd044:
    .word  0xfffff003                     @ 080dd044 03f0ffff
PTR_BG0CNT_080dd048:
    .word  BG0CNT                         @ 080dd048 08000004
LAB_080dd04c:
    ldrh r7,[r7,#0x2]                        @ 080dd04c 7f88
    lsls r0,r7,#0x12    @ 080dd04e b804
    lsrs r0,r0,#0xd    @ 080dd050 400b
    ldr r3, DAT_080dd06c                     @ 080dd052 064b
    adds r0,r0,r3    @ 080dd054 c018
    movs r1,#0x0    @ 080dd056 0021
    bl blit_tile_nibble_row_lsb              @ 080dd058 16f048ff
LAB_080dd05c:
    add sp,#0x8                              @ 080dd05c 02b0
    pop {r3,r4,r5}                           @ 080dd05e 38bc
    .hword 0x4698    @ 080dd060 9846
    .hword 0x46a1    @ 080dd062 a146
    .hword 0x46aa    @ 080dd064 aa46
    pop {r4,r5,r6,r7}                        @ 080dd066 f0bc
    pop {r0}                                 @ 080dd068 01bc
    bx r0                                    @ 080dd06a 0047
DAT_080dd06c:
    .word  0x06010420                     @ 080dd06c 20040106

@ Measures the pixel width and height of a JP string under the current overlay font and returns the result packed.
@ Reads overlay_ptr from gPrng+0x1d0; returns 0 if null. Reads overlay[+0x14] flags bit1 to determine font width (2 or 4). Uses r1=text_area_width and r2=text_area_height (each minus 2) to call setup_line_buf_font_with_align_and_slot. Manipulates 0x02006ed0 font control bytes. Updates overlay[+0xa] tile index field. Calls render_jp_string_nowrap to render the JP string and get pixel dimensions. Converts pixel width to tile count via (px+8)>>3, height likewise, returns (tile_h+2) | ((tile_w+2)<<16).
@ Called exclusively by text_overlay_create (FUN_080dd53c) which passes: r1=overlay[+0xa]=text_area_width (low16 of packed size), r2=overlay[+0xc]=text_area_height (high16 of packed size).
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct pointer
@ - 0x02006ed0: line buffer font control base
@ - 0x000003ff: tile index mask (DAT_080dd15c)
@ - 0xfffff003: tile clear mask (DAT_080dd160)
@ 
@ Inputs: r0=u32 packed_xy (scroll position, callee-save via mov r8,r0), r1=u16 text_area_width [0..30] (tiles, from overlay[+0xa]), r2=u16 text_area_height [0..16] (tiles, from overlay[+0xc])
@ Returns: r0=u32 packed (tile_height+2) | ((tile_width+2)<<16); 0 if overlay is null (pop {r1}; bx r1, Sub-case E)
@ Side effects: [0x02006ed0+0x8/0x14/0x15] font control bytes; [overlay+0xa] tile index field (two strh updates)
measure_overlay_text_dimensions:
    push {r4,r5,r6,r7,lr}                    @ 080dd070 f0b5
    .hword 0x4647    @ 080dd072 4746
    push {r7}                                @ 080dd074 80b4
    .hword 0x4680    @ 080dd076 8046
    adds r3,r1,#0x0    @ 080dd078 0b1c
    ldr r0, PTR_gPrng_080dd08c               @ 080dd07a 0448
    movs r1,#0xe8    @ 080dd07c e821
    lsls r1,r1,#0x1    @ 080dd07e 4900
    adds r0,r0,r1    @ 080dd080 4018
    ldr r0,[r0,#0x0]                         @ 080dd082 0068
    cmp r0,#0x0                              @ 080dd084 0028
    bne LAB_080dd090                         @ 080dd086 03d1
    movs r0,#0x0    @ 080dd088 0020
    b LAB_080dd148                           @ 080dd08a 5de0
PTR_gPrng_080dd08c:
    .word  gPrng                          @ 080dd08c 40000003
LAB_080dd090:
    ldr r0,[r0,#0x14]                        @ 080dd090 4069
    lsrs r7,r0,#0x1    @ 080dd092 4708
    movs r1,#0x1    @ 080dd094 0121
    ands r7,r1    @ 080dd096 0f40
    movs r1,#0x2    @ 080dd098 0221
    ands r0,r1    @ 080dd09a 0840
    movs r4,#0x2    @ 080dd09c 0224
    cmp r0,#0x0                              @ 080dd09e 0028
    beq LAB_080dd0a4                         @ 080dd0a0 00d0
    movs r4,#0x4    @ 080dd0a2 0424
LAB_080dd0a4:
    subs r0,r3,#0x2    @ 080dd0a4 981e
    subs r1,r2,#0x2    @ 080dd0a6 911e
    movs r2,#0x1    @ 080dd0a8 0122
    adds r3,r4,#0x0    @ 080dd0aa 231c
    bl setup_line_buf_font_with_align_and_slot @ 080dd0ac 13f050fe
    ldr r5, DAT_080dd154                     @ 080dd0b0 284d
    movs r1,#0x1    @ 080dd0b2 0121
    ldrb r0,[r5,#0x15]                       @ 080dd0b4 687d
    orrs r0,r1    @ 080dd0b6 0843
    strb r0,[r5,#0x15]                       @ 080dd0b8 6875
    adds r0,r7,#0x0    @ 080dd0ba 381c
    ands r0,r1    @ 080dd0bc 0840
    lsls r0,r0,#0x1    @ 080dd0be 4000
    movs r1,#0x3    @ 080dd0c0 0321
    rsbs r1,r1,#0    @ 080dd0c2 4942
    ldrb r2,[r5,#0x8]                        @ 080dd0c4 2a7a
    ands r1,r2    @ 080dd0c6 1140
    orrs r1,r0    @ 080dd0c8 0143
    strb r1,[r5,#0x8]                        @ 080dd0ca 2972
    lsls r2,r4,#0x2    @ 080dd0cc a200
    movs r0,#0x7d    @ 080dd0ce 7d20
    rsbs r0,r0,#0    @ 080dd0d0 4042
    ldrb r3,[r5,#0x14]                       @ 080dd0d2 2b7d
    ands r0,r3    @ 080dd0d4 1840
    orrs r0,r2    @ 080dd0d6 1043
    strb r0,[r5,#0x14]                       @ 080dd0d8 2875
    ldr r2, PTR_font_jp_base_table_080dd158  @ 080dd0da 1f4a
    lsls r0,r1,#0x1e    @ 080dd0dc 8807
    lsrs r0,r0,#0x1f    @ 080dd0de c00f
    lsls r0,r0,#0x2    @ 080dd0e0 8000
    lsls r1,r1,#0x1f    @ 080dd0e2 c907
    lsrs r1,r1,#0x1f    @ 080dd0e4 c90f
    lsls r1,r1,#0x3    @ 080dd0e6 c900
    adds r0,r0,r1    @ 080dd0e8 4018
    adds r0,r0,r2    @ 080dd0ea 8018
    ldr r0,[r0,#0x0]                         @ 080dd0ec 0068
    str r0,[r5,#0x4]                         @ 080dd0ee 6860
    ldrh r2,[r5,#0xa]                        @ 080dd0f0 6a89
    lsls r1,r2,#0x14    @ 080dd0f2 1105
    lsrs r1,r1,#0x16    @ 080dd0f4 890d
    subs r1,#0x1    @ 080dd0f6 0139
    ldr r0, DAT_080dd15c                     @ 080dd0f8 1848
    adds r6,r0,#0x0    @ 080dd0fa 061c
    ands r1,r6    @ 080dd0fc 3140
    lsls r1,r1,#0x2    @ 080dd0fe 8900
    ldr r4, DAT_080dd160                     @ 080dd100 174c
    adds r0,r4,#0x0    @ 080dd102 201c
    ands r0,r2    @ 080dd104 1040
    orrs r0,r1    @ 080dd106 0843
    strh r0,[r5,#0xa]                        @ 080dd108 6881
    lsls r0,r7,#0x18    @ 080dd10a 3806
    movs r2,#0xe0    @ 080dd10c e022
    lsls r2,r2,#0xb    @ 080dd10e d202
    orrs r2,r0    @ 080dd110 0243
    lsrs r2,r2,#0x10    @ 080dd112 120c
    movs r0,#0x0    @ 080dd114 0020
    movs r1,#0x0    @ 080dd116 0021
    .hword 0x4643    @ 080dd118 4346
    bl render_jp_string_nowrap               @ 080dd11a 15f093fc
    adds r1,r0,#0x0    @ 080dd11e 011c
    ldrh r2,[r5,#0xa]                        @ 080dd120 6a89
    lsls r0,r2,#0x14    @ 080dd122 1005
    lsrs r0,r0,#0x16    @ 080dd124 800d
    adds r0,#0x1    @ 080dd126 0130
    ands r0,r6    @ 080dd128 3040
    lsls r0,r0,#0x2    @ 080dd12a 8000
    ands r4,r2    @ 080dd12c 1440
    orrs r4,r0    @ 080dd12e 0443
    strh r4,[r5,#0xa]                        @ 080dd130 6c81
    lsls r0,r1,#0x10    @ 080dd132 0804
    lsrs r0,r0,#0x10    @ 080dd134 000c
    adds r0,#0x8    @ 080dd136 0830
    asrs r0,r0,#0x3    @ 080dd138 c010
    lsrs r1,r1,#0x10    @ 080dd13a 090c
    adds r1,#0x8    @ 080dd13c 0831
    asrs r1,r1,#0x3    @ 080dd13e c910
    adds r0,#0x2    @ 080dd140 0230
    adds r1,#0x2    @ 080dd142 0231
    lsls r1,r1,#0x10    @ 080dd144 0904
    orrs r0,r1    @ 080dd146 0843
LAB_080dd148:
    pop {r3}                                 @ 080dd148 08bc
    .hword 0x4698    @ 080dd14a 9846
    pop {r4,r5,r6,r7}                        @ 080dd14c f0bc
    pop {r1}                                 @ 080dd14e 02bc
    bx r1                                    @ 080dd150 0847
    .zero  0x2
DAT_080dd154:
    .word  0x02006ed0                     @ 080dd154 d06e0002
PTR_font_jp_base_table_080dd158:
    .word  font_jp_base_table             @ 080dd158 54f8e509
DAT_080dd15c:
    .word  0x000003ff                     @ 080dd15c ff030000
DAT_080dd160:
    .word  0xfffff003                     @ 080dd160 03f0ffff

@ Renders overlay object as a stretched OAM sprite sequence. r0=scroll_x_offset, r1=scroll_y_offset. Fetches overlay object from gPrng+0x1d0; validates [+0x18] reference; computes OAM column distribution via binary search for POT level from [+0x10] width field; calls write_oam_entry_from_packed_args per column to write OAM attributes. Returns immediately if overlay uninitialized or has no data. Called by FUN_080dd748 when BG mode=0.
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct ptr
@ - gPrng+0x1bc: overlay active flag
@ - 0x09e49558: overlay tile/frame data table (ROM)
@ - 0x0000ffff: empty tile marker
render_overlay_oam_sprite_stretched:
    push {r4,r5,r6,r7,lr}                    @ 080dd164 f0b5
    .hword 0x4657    @ 080dd166 5746
    .hword 0x464e    @ 080dd168 4e46
    .hword 0x4645    @ 080dd16a 4546
    push {r5,r6,r7}                          @ 080dd16c e0b4
    sub sp,#0x10                             @ 080dd16e 84b0
    str r0,[sp,#0x0]                         @ 080dd170 0090
    ldr r2, PTR_gPrng_080dd21c               @ 080dd172 2a4a
    movs r3,#0xe8    @ 080dd174 e823
    lsls r3,r3,#0x1    @ 080dd176 5b00
    adds r0,r2,r3    @ 080dd178 d018
    ldr r7,[r0,#0x0]                         @ 080dd17a 0768
    cmp r7,#0x0                              @ 080dd17c 002f
    bne LAB_080dd182                         @ 080dd17e 00d1
    b LAB_080dd2bc                           @ 080dd180 9ce0
LAB_080dd182:
    movs r4,#0xde    @ 080dd182 de24
    lsls r4,r4,#0x1    @ 080dd184 6400
    adds r0,r2,r4    @ 080dd186 1019
    ldr r0,[r0,#0x0]                         @ 080dd188 0068
    cmp r0,#0x0                              @ 080dd18a 0028
    bne LAB_080dd190                         @ 080dd18c 00d1
    b LAB_080dd2bc                           @ 080dd18e 95e0
LAB_080dd190:
    movs r0,#0x3    @ 080dd190 0320
    .hword 0x4680    @ 080dd192 8046
    ldrh r2,[r7,#0x10]                       @ 080dd194 3a8a
    .hword 0x4691    @ 080dd196 9146
    ldrh r3,[r7,#0x26]                       @ 080dd198 fb8c
    lsls r0,r3,#0x10    @ 080dd19a 1804
    asrs r0,r0,#0x18    @ 080dd19c 0016
    adds r0,r1,r0    @ 080dd19e 0818
    lsls r1,r2,#0x2    @ 080dd1a0 9100
    subs r0,r0,r1    @ 080dd1a2 401a
    str r0,[sp,#0x8]                         @ 080dd1a4 0290
    cmp r2,#0x0                              @ 080dd1a6 002a
    bgt LAB_080dd1ac                         @ 080dd1a8 00dc
    b LAB_080dd2bc                           @ 080dd1aa 87e0
LAB_080dd1ac:
    movs r0,#0x1    @ 080dd1ac 0120
    .hword 0x4644    @ 080dd1ae 4446
    lsls r0,r4    @ 080dd1b0 a040
    ldrh r3,[r7,#0x26]                       @ 080dd1b2 fb8c
    ldrh r1,[r7,#0xe]                        @ 080dd1b4 f989
    cmp r9,r0                                @ 080dd1b6 8145
    bge LAB_080dd1cc                         @ 080dd1b8 08da
    movs r2,#0x1    @ 080dd1ba 0122
LAB_080dd1bc:
    movs r0,#0x1    @ 080dd1bc 0120
    rsbs r0,r0,#0    @ 080dd1be 4042
    add r8,r0                                @ 080dd1c0 8044
    adds r0,r2,#0x0    @ 080dd1c2 101c
    .hword 0x4644    @ 080dd1c4 4446
    lsls r0,r4    @ 080dd1c6 a040
    cmp r9,r0                                @ 080dd1c8 8145
    blt LAB_080dd1bc                         @ 080dd1ca f7db
LAB_080dd1cc:
    movs r6,#0x3    @ 080dd1cc 0326
    adds r5,r1,#0x0    @ 080dd1ce 0d1c
    lsls r0,r3,#0x18    @ 080dd1d0 1806
    asrs r0,r0,#0x18    @ 080dd1d2 0016
    ldr r1,[sp,#0x0]                         @ 080dd1d4 0099
    adds r0,r1,r0    @ 080dd1d6 0818
    lsls r1,r5,#0x2    @ 080dd1d8 a900
    subs r0,r0,r1    @ 080dd1da 401a
    str r0,[sp,#0x4]                         @ 080dd1dc 0190
    cmp r5,#0x0                              @ 080dd1de 002d
    ble LAB_080dd2a2                         @ 080dd1e0 5fdd
    .hword 0x4642    @ 080dd1e2 4246
    lsls r2,r2,#0x2    @ 080dd1e4 9200
    .hword 0x4692    @ 080dd1e6 9246
LAB_080dd1e8:
    movs r0,#0x1    @ 080dd1e8 0120
    lsls r0,r6    @ 080dd1ea b040
    cmp r5,r0                                @ 080dd1ec 8542
    bge LAB_080dd1fc                         @ 080dd1ee 05da
    movs r1,#0x1    @ 080dd1f0 0121
LAB_080dd1f2:
    subs r6,#0x1    @ 080dd1f2 013e
    adds r0,r1,#0x0    @ 080dd1f4 081c
    lsls r0,r6    @ 080dd1f6 b040
    cmp r5,r0                                @ 080dd1f8 8542
    blt LAB_080dd1f2                         @ 080dd1fa fadb
LAB_080dd1fc:
    ldr r4, DAT_080dd220                     @ 080dd1fc 084c
    ldr r3, DAT_080dd224                     @ 080dd1fe 094b
    .hword 0x4640    @ 080dd200 4046
    lsls r2,r0,#0x2    @ 080dd202 8200
LAB_080dd204:
    adds r0,r2,r6    @ 080dd204 9019
    lsls r0,r0,#0x1    @ 080dd206 4000
    adds r0,r0,r4    @ 080dd208 0019
    adds r1,r2,#0x0    @ 080dd20a 111c
    ldrh r0,[r0,#0x0]                        @ 080dd20c 0088
    cmp r0,r3                                @ 080dd20e 9842
    bne LAB_080dd23e                         @ 080dd210 15d1
    cmp r6,#0x1                              @ 080dd212 012e
    ble LAB_080dd228                         @ 080dd214 08dd
    subs r6,#0x1    @ 080dd216 013e
    b LAB_080dd204                           @ 080dd218 f4e7
    .zero  0x2
PTR_gPrng_080dd21c:
    .word  gPrng                          @ 080dd21c 40000003
DAT_080dd220:
    .word  0x09e49558                     @ 080dd220 5895e409
DAT_080dd224:
    .word  0x0000ffff                     @ 080dd224 ffff0000
LAB_080dd228:
    .hword 0x4642    @ 080dd228 4246
    cmp r2,#0x1                              @ 080dd22a 012a
    ble LAB_080dd23e                         @ 080dd22c 07dd
    subs r2,r1,#0x4    @ 080dd22e 0a1f
    movs r0,#0x4    @ 080dd230 0420
    rsbs r0,r0,#0    @ 080dd232 4042
    add r10,r0                               @ 080dd234 8244
    movs r1,#0x1    @ 080dd236 0121
    rsbs r1,r1,#0    @ 080dd238 4942
    add r8,r1                                @ 080dd23a 8844
    b LAB_080dd204                           @ 080dd23c e2e7
LAB_080dd23e:
    .hword 0x4642    @ 080dd23e 4246
    lsls r0,r2,#0x3    @ 080dd240 d000
    ldr r3,[sp,#0x8]                         @ 080dd242 029b
    adds r0,r3,r0    @ 080dd244 1818
    cmp r0,#0x0                              @ 080dd246 0028
    blt LAB_080dd290                         @ 080dd248 22db
    cmp r3,#0x9f                             @ 080dd24a 9f2b
    bgt LAB_080dd290                         @ 080dd24c 20dc
    ldr r4,[sp,#0x4]                         @ 080dd24e 019c
    lsls r0,r4,#0x10    @ 080dd250 2004
    lsrs r0,r0,#0x10    @ 080dd252 000c
    lsls r1,r3,#0x10    @ 080dd254 1904
    orrs r0,r1    @ 080dd256 0843
    .hword 0x4652    @ 080dd258 5246
    adds r1,r2,r6    @ 080dd25a 9119
    lsls r1,r1,#0x1    @ 080dd25c 4900
    ldr r3, DAT_080dd2cc                     @ 080dd25e 1b4b
    adds r1,r1,r3    @ 080dd260 c918
    ldrh r1,[r1,#0x0]                        @ 080dd262 0988
    ldrh r4,[r7,#0x4]                        @ 080dd264 bc88
    lsls r2,r4,#0xc    @ 080dd266 2203
    ldrh r4,[r7,#0x0]                        @ 080dd268 3c88
    lsls r3,r4,#0xa    @ 080dd26a a302
    orrs r2,r3    @ 080dd26c 1a43
    ldrh r3,[r7,#0x2]                        @ 080dd26e 7b88
    lsls r4,r3,#0x12    @ 080dd270 9c04
    lsrs r4,r4,#0x12    @ 080dd272 a40c
    .hword 0x46a4    @ 080dd274 a446
    .hword 0x464b    @ 080dd276 4b46
    ldrh r4,[r7,#0x10]                       @ 080dd278 3c8a
    subs r3,r4,r3    @ 080dd27a e31a
    lsls r3,r3,#0x5    @ 080dd27c 5b01
    add r12,r3                               @ 080dd27e 9c44
    ldrh r4,[r7,#0xe]                        @ 080dd280 fc89
    add r4,r12                               @ 080dd282 6444
    subs r4,r4,r5    @ 080dd284 641b
    orrs r2,r4    @ 080dd286 2243
    lsls r2,r2,#0x10    @ 080dd288 1204
    lsrs r2,r2,#0x10    @ 080dd28a 120c
    bl write_oam_entry_from_packed_args      @ 080dd28c 18f06eff
LAB_080dd290:
    movs r0,#0x1    @ 080dd290 0120
    lsls r0,r6    @ 080dd292 b040
    subs r5,r5,r0    @ 080dd294 2d1a
    lsls r0,r0,#0x3    @ 080dd296 c000
    ldr r4,[sp,#0x4]                         @ 080dd298 019c
    adds r4,r4,r0    @ 080dd29a 2418
    str r4,[sp,#0x4]                         @ 080dd29c 0194
    cmp r5,#0x0                              @ 080dd29e 002d
    bgt LAB_080dd1e8                         @ 080dd2a0 a2dc
LAB_080dd2a2:
    movs r0,#0x1    @ 080dd2a2 0120
    .hword 0x4641    @ 080dd2a4 4146
    lsls r0,r1    @ 080dd2a6 8840
    .hword 0x464a    @ 080dd2a8 4a46
    subs r2,r2,r0    @ 080dd2aa 121a
    .hword 0x4691    @ 080dd2ac 9146
    lsls r0,r0,#0x3    @ 080dd2ae c000
    ldr r3,[sp,#0x8]                         @ 080dd2b0 029b
    adds r3,r3,r0    @ 080dd2b2 1b18
    str r3,[sp,#0x8]                         @ 080dd2b4 0293
    cmp r2,#0x0                              @ 080dd2b6 002a
    ble LAB_080dd2bc                         @ 080dd2b8 00dd
    b LAB_080dd1ac                           @ 080dd2ba 77e7
LAB_080dd2bc:
    add sp,#0x10                             @ 080dd2bc 04b0
    pop {r3,r4,r5}                           @ 080dd2be 38bc
    .hword 0x4698    @ 080dd2c0 9846
    .hword 0x46a1    @ 080dd2c2 a146
    .hword 0x46aa    @ 080dd2c4 aa46
    pop {r4,r5,r6,r7}                        @ 080dd2c6 f0bc
    pop {r0}                                 @ 080dd2c8 01bc
    bx r0                                    @ 080dd2ca 0047
DAT_080dd2cc:
    .word  0x09e49558                     @ 080dd2cc 5895e409

@ Sets BG horizontal/vertical scroll register offsets for overlay object. r0=scroll_x, r1=scroll_y. Fetches overlay ptr from gPrng+0x1d0; reads BG index from overlay flags bits[7:6]; computes BGxHOFS/BGxVOFS register offsets; writes computed scroll values; also reads BGxCNT tile/map base and writes back modified BGxCNT, sets DISPCNT BG bit. Called by FUN_080dd748 when BG mode != 0.
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct ptr
@ - BG0HOFS=0x04000010: BG0 horizontal scroll
@ - BG0VOFS=0x04000012: BG0 vertical scroll
@ - BG0CNT=0x04000008: BG0 control
@ - DISPCNT=0x04000000: display control
@ - 0x0000fffc: BGxCNT mask (clear tile base bits)
apply_overlay_bg_scroll_offset:
    push {r4,r5,r6,lr}                       @ 080dd2d0 70b5
    adds r3,r0,#0x0    @ 080dd2d2 031c
    adds r5,r1,#0x0    @ 080dd2d4 0d1c
    ldr r0, PTR_gPrng_080dd364               @ 080dd2d6 2348
    movs r1,#0xe8    @ 080dd2d8 e821
    lsls r1,r1,#0x1    @ 080dd2da 4900
    adds r0,r0,r1    @ 080dd2dc 4018
    ldr r4,[r0,#0x0]                         @ 080dd2de 0468
    cmp r4,#0x0                              @ 080dd2e0 002c
    beq LAB_080dd35e                         @ 080dd2e2 3cd0
    ldrb r6,[r4,#0x3]                        @ 080dd2e4 e678
    lsrs r2,r6,#0x6    @ 080dd2e6 b209
    lsls r2,r2,#0x2    @ 080dd2e8 9200
    ldr r0, PTR_BG0HOFS_080dd368             @ 080dd2ea 1f48
    adds r2,r2,r0    @ 080dd2ec 1218
    ldrh r0,[r4,#0xe]                        @ 080dd2ee e089
    lsls r1,r0,#0x2    @ 080dd2f0 8100
    ldrh r6,[r4,#0x26]                       @ 080dd2f2 e68c
    lsls r0,r6,#0x10    @ 080dd2f4 3004
    asrs r0,r0,#0x18    @ 080dd2f6 0016
    adds r0,r0,r3    @ 080dd2f8 c018
    subs r1,r1,r0    @ 080dd2fa 091a
    strh r1,[r2,#0x0]                        @ 080dd2fc 1180
    ldrb r0,[r4,#0x3]                        @ 080dd2fe e078
    lsrs r2,r0,#0x6    @ 080dd300 8209
    lsls r2,r2,#0x2    @ 080dd302 9200
    ldr r0, PTR_BG0VOFS_080dd36c             @ 080dd304 1948
    adds r2,r2,r0    @ 080dd306 1218
    ldrh r3,[r4,#0x10]                       @ 080dd308 238a
    lsls r1,r3,#0x2    @ 080dd30a 9900
    ldrh r6,[r4,#0x26]                       @ 080dd30c e68c
    lsls r0,r6,#0x18    @ 080dd30e 3006
    asrs r0,r0,#0x18    @ 080dd310 0016
    adds r0,r0,r5    @ 080dd312 4019
    subs r1,r1,r0    @ 080dd314 091a
    strh r1,[r2,#0x0]                        @ 080dd316 1180
    ldrb r1,[r4,#0x3]                        @ 080dd318 e178
    lsls r0,r1,#0x18    @ 080dd31a 0806
    lsrs r1,r0,#0x1e    @ 080dd31c 810f
    lsls r1,r1,#0x1    @ 080dd31e 4900
    ldr r3, PTR_BG0CNT_080dd370              @ 080dd320 134b
    adds r1,r1,r3    @ 080dd322 c918
    lsrs r0,r0,#0x1e    @ 080dd324 800f
    lsls r0,r0,#0x1    @ 080dd326 4000
    adds r0,r0,r3    @ 080dd328 c018
    ldrh r2,[r0,#0x0]                        @ 080dd32a 0288
    ldr r0, DAT_080dd374                     @ 080dd32c 1148
    ands r0,r2    @ 080dd32e 1040
    strh r0,[r1,#0x0]                        @ 080dd330 0880
    ldrb r2,[r4,#0x3]                        @ 080dd332 e278
    lsls r0,r2,#0x18    @ 080dd334 1006
    lsrs r1,r0,#0x1e    @ 080dd336 810f
    lsls r1,r1,#0x1    @ 080dd338 4900
    adds r1,r1,r3    @ 080dd33a c918
    lsrs r0,r0,#0x1e    @ 080dd33c 800f
    lsls r0,r0,#0x1    @ 080dd33e 4000
    adds r0,r0,r3    @ 080dd340 c018
    ldrh r0,[r0,#0x0]                        @ 080dd342 0088
    ldrh r3,[r4,#0x0]                        @ 080dd344 2388
    orrs r0,r3    @ 080dd346 1843
    strh r0,[r1,#0x0]                        @ 080dd348 0880
    movs r2,#0x80    @ 080dd34a 8022
    lsls r2,r2,#0x13    @ 080dd34c d204
    ldrb r4,[r4,#0x3]                        @ 080dd34e e478
    lsrs r1,r4,#0x6    @ 080dd350 a109
    adds r1,#0x8    @ 080dd352 0831
    movs r0,#0x1    @ 080dd354 0120
    lsls r0,r1    @ 080dd356 8840
    ldrh r1,[r2,#0x0]                        @ 080dd358 1188
    orrs r0,r1    @ 080dd35a 0843
    strh r0,[r2,#0x0]                        @ 080dd35c 1080
LAB_080dd35e:
    pop {r4,r5,r6}                           @ 080dd35e 70bc
    pop {r0}                                 @ 080dd360 01bc
    bx r0                                    @ 080dd362 0047
PTR_gPrng_080dd364:
    .word  gPrng                          @ 080dd364 40000003
PTR_BG0HOFS_080dd368:
    .word  BG0HOFS                        @ 080dd368 10000004
PTR_BG0VOFS_080dd36c:
    .word  BG0VOFS                        @ 080dd36c 12000004
PTR_BG0CNT_080dd370:
    .word  BG0CNT                         @ 080dd370 08000004
DAT_080dd374:
    .word  0x0000fffc                     @ 080dd374 fcff0000

@ Copies overlay tile row data to destination address and appends palette data. r0=dst VRAM addr, r1=tile_row_index. Multiplies row index by 4 to get offset, looks up 0x09cede60 ROM table to fetch source tile row ptr, calls copy_bytes_by_halfword to copy 0x20 bytes of tile data; then appends 0x10 bytes from 0x09ccd292 palette data via copy_memory_dma3_with_cpu_fallback. Called by text_overlay_create and multiple overlay display functions.
@ 
@ Constants:
@ - 0x09cede60: overlay tile row pointer table (ROM), 4 bytes per ptr
@ - 0x09ccd292: overlay palette/attribute data (ROM)
@ - 0x20: tile row data size (32 bytes)
@ - 0x10: palette/attribute block size (16 bytes)
copy_overlay_tile_row_to_palette:
    push {r4,lr}                             @ 080dd378 10b5
    adds r4,r0,#0x0    @ 080dd37a 041c
    lsls r1,r1,#0x10    @ 080dd37c 0904
    ldr r0, DAT_080dd3a0                     @ 080dd37e 0848
    lsrs r1,r1,#0xe    @ 080dd380 890b
    adds r1,r1,r0    @ 080dd382 0918
    ldr r1,[r1,#0x0]                         @ 080dd384 0968
    adds r0,r4,#0x0    @ 080dd386 201c
    movs r2,#0x20    @ 080dd388 2022
    bl copy_bytes_by_halfword                @ 080dd38a 17f08bfd
    adds r4,#0x2    @ 080dd38e 0234
    ldr r1, DAT_080dd3a4                     @ 080dd390 0449
    adds r0,r4,#0x0    @ 080dd392 201c
    movs r2,#0x10    @ 080dd394 1022
    bl copy_memory_dma3_with_cpu_fallback    @ 080dd396 17f0b7fd
    pop {r4}                                 @ 080dd39a 10bc
    pop {r0}                                 @ 080dd39c 01bc
    bx r0                                    @ 080dd39e 0047
DAT_080dd3a0:
    .word  0x09cede60                     @ 080dd3a0 60dece09
DAT_080dd3a4:
    .word  0x09ccd292                     @ 080dd3a4 92d2cc09

@ Initializes a text overlay struct and selects the palette source based on mode_flags.
@ r0=overlay_ptr (written to gPrng+0x1d0), r1=ewram_ctx_ptr, r2=tile_attr (low 14 bits), r3=tile_row_index [0..15] (written to [overlay+0x4]; all 6 observed callsites pass movs r3,#0xf=15), [sp+0x14]=mode_flags.
@ Steps: (1) store r0 in gPrng+0x1d0; (2) zero_fill_halfword_wrapper clears 0x28 halfwords of overlay struct; (3) clear [overlay+0x3] bits[7:6], write tile_attr low 14 bits to [overlay+0x2], write tile_row_index to [overlay+0x4], clear [overlay+0x8]; (4) if mode_flags bit0 set: copy from OBJ palette 0x05000200 + tile_row_index*0x20 via copy_overlay_tile_row_to_palette; else copy from ROM table; (5) store ewram_ctx_ptr to [overlay+0x18], call store_ewram_ctx_ptr_and_clear_mode_flags; (6) store mode_flags to [overlay+0x14].
@ Called by FUN_080d5604 / FUN_080d72f8 / FUN_080d87d0 / FUN_080d9694 and others.
@ 
@ Constants:
@ - gPrng+0x1d0: global overlay pointer slot (gPrng+0xe8<<1)
@ - 0x05000200: OBJ palette base + 0x200 (palette source when mode_flags bit0=1)
@ - 0x00003fff: tile_attr low 14 bits mask (DAT_080dd400)
@ - 0xffffc000: tile_attr clear mask (DAT_080dd404)
@ - ZERO_LEN=0x28 // zero_fill_halfword_wrapper clears this many halfwords
@ 
@ Inputs: r0=void* overlay_ptr, r1=void* ewram_ctx_ptr, r2=u16 tile_attr [0..0x3fff], r3=u16 tile_row_index [0..15], [sp+0x14]=u32 mode_flags
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [gPrng+0x1d0]:=overlay_ptr; [overlay_ptr+0x0..0x4f] cleared; [overlay_ptr+0x2/0x4/0x8/0x14/0x18] written; [OBJ palette via copy_overlay_tile_row_to_palette]; [via store_ewram_ctx_ptr_and_clear_mode_flags]
init_overlay_struct_and_palette:
    push {r4,r5,r6,r7,lr}                    @ 080dd3a8 f0b5
    adds r5,r0,#0x0    @ 080dd3aa 051c
    adds r7,r1,#0x0    @ 080dd3ac 0f1c
    adds r4,r2,#0x0    @ 080dd3ae 141c
    adds r6,r3,#0x0    @ 080dd3b0 1e1c
    ldr r0, PTR_gPrng_080dd3fc               @ 080dd3b2 1248
    movs r1,#0xe8    @ 080dd3b4 e821
    lsls r1,r1,#0x1    @ 080dd3b6 4900
    adds r0,r0,r1    @ 080dd3b8 4018
    str r5,[r0,#0x0]                         @ 080dd3ba 0560
    adds r0,r5,#0x0    @ 080dd3bc 281c
    movs r1,#0x28    @ 080dd3be 2821
    bl zero_fill_halfword_wrapper            @ 080dd3c0 17f06afd
    movs r0,#0x3f    @ 080dd3c4 3f20
    ldrb r2,[r5,#0x3]                        @ 080dd3c6 ea78
    ands r0,r2    @ 080dd3c8 1040
    strb r0,[r5,#0x3]                        @ 080dd3ca e870
    ldr r1, DAT_080dd400                     @ 080dd3cc 0c49
    ands r1,r4    @ 080dd3ce 2140
    ldr r0, DAT_080dd404                     @ 080dd3d0 0c48
    ldrh r2,[r5,#0x2]                        @ 080dd3d2 6a88
    ands r0,r2    @ 080dd3d4 1040
    orrs r0,r1    @ 080dd3d6 0843
    strh r0,[r5,#0x2]                        @ 080dd3d8 6880
    movs r0,#0x0    @ 080dd3da 0020
    strh r6,[r5,#0x4]                        @ 080dd3dc ae80
    strh r0,[r5,#0x8]                        @ 080dd3de 2881
    movs r0,#0x1    @ 080dd3e0 0120
    ldr r1,[sp,#0x14]                        @ 080dd3e2 0599
    ands r0,r1    @ 080dd3e4 0840
    cmp r0,#0x0                              @ 080dd3e6 0028
    beq LAB_080dd408                         @ 080dd3e8 0ed0
    lsls r0,r6,#0x5    @ 080dd3ea 7001
    movs r2,#0xa0    @ 080dd3ec a022
    lsls r2,r2,#0x13    @ 080dd3ee d204
    adds r0,r0,r2    @ 080dd3f0 8018
    movs r1,#0x0    @ 080dd3f2 0021
    bl copy_overlay_tile_row_to_palette      @ 080dd3f4 fff7c0ff
    b LAB_080dd414                           @ 080dd3f8 0ce0
    .zero  0x2
PTR_gPrng_080dd3fc:
    .word  gPrng                          @ 080dd3fc 40000003
DAT_080dd400:
    .word  0x00003fff                     @ 080dd400 ff3f0000
DAT_080dd404:
    .word  0xffffc000                     @ 080dd404 00c0ffff
LAB_080dd408:
    lsls r0,r6,#0x5    @ 080dd408 7001
    ldr r1, DAT_080dd42c                     @ 080dd40a 0849
    adds r0,r0,r1    @ 080dd40c 4018
    movs r1,#0x0    @ 080dd40e 0021
    bl copy_overlay_tile_row_to_palette      @ 080dd410 fff7b2ff
LAB_080dd414:
    str r7,[r5,#0x18]                        @ 080dd414 af61
    cmp r7,#0x0                              @ 080dd416 002f
    beq LAB_080dd420                         @ 080dd418 02d0
    adds r0,r7,#0x0    @ 080dd41a 381c
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 080dd41c 16f040ff
LAB_080dd420:
    ldr r2,[sp,#0x14]                        @ 080dd420 059a
    str r2,[r5,#0x14]                        @ 080dd422 6a61
    pop {r4,r5,r6,r7}                        @ 080dd424 f0bc
    pop {r0}                                 @ 080dd426 01bc
    bx r0                                    @ 080dd428 0047
    .zero  0x2
DAT_080dd42c:
    .word  0x05000200                     @ 080dd42c 00020005

@ Updates the scroll/direction bits and tile attribute extra field of the current text overlay struct.
@ r0=packed_flags (low 2 bits written to [overlay+0x3] bits[7:6]), r1=packed_attr_extra (low 16 bits written to [overlay+0x6]).
@ Reads overlay_ptr from gPrng+0x1d0; if null returns void. Otherwise: clears [overlay+0x3] bits[7:6] using mask 0x3f, ORs in r0 low 2 bits shifted left 6; stores r1 low 16 bits to [overlay+0x6].
@ indeg=0 (dead code; grep ".word 0x080dd431" -> 0 hits).
@ 
@ Constants:
@ - gPrng+0x1d0: global overlay pointer slot
@ - 0x3f: [overlay+0x3] bits[7:6] clear mask
@ - DIR_BITS_SHIFT=6 // r0 low 2 bits shifted to bits[7:6]
@ 
@ Inputs: r0=u16 packed_flags (low 2 bits = scroll dir/mode), r1=u16 packed_attr_extra (written to [overlay+0x6])
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [overlay+0x3] bits[7:6] := r0 low 2 bits; [overlay+0x6] := r1 low 16 bits
update_overlay_scroll_and_attr:
    push {r4,lr}                             @ 080dd430 10b5
    lsls r0,r0,#0x10    @ 080dd432 0004
    lsrs r3,r0,#0x10    @ 080dd434 030c
    lsls r1,r1,#0x10    @ 080dd436 0904
    lsrs r4,r1,#0x10    @ 080dd438 0c0c
    ldr r0, DWORD_080dd460                   @ 080dd43a 0948
    movs r1,#0xe8    @ 080dd43c e821
    lsls r1,r1,#0x1    @ 080dd43e 4900
    adds r0,r0,r1    @ 080dd440 4018
    ldr r2,[r0,#0x0]                         @ 080dd442 0268
    cmp r2,#0x0                              @ 080dd444 002a
    beq LAB_080dd45a                         @ 080dd446 08d0
    movs r1,#0x3    @ 080dd448 0321
    ands r1,r3    @ 080dd44a 1940
    lsls r1,r1,#0x6    @ 080dd44c 8901
    movs r0,#0x3f    @ 080dd44e 3f20
    ldrb r3,[r2,#0x3]                        @ 080dd450 d378
    ands r0,r3    @ 080dd452 1840
    orrs r0,r1    @ 080dd454 0843
    strb r0,[r2,#0x3]                        @ 080dd456 d070
    strh r4,[r2,#0x6]                        @ 080dd458 d480
LAB_080dd45a:
    pop {r4}                                 @ 080dd45a 10bc
    pop {r0}                                 @ 080dd45c 01bc
    bx r0                                    @ 080dd45e 0047
DWORD_080dd460:
    .word  gPrng                          @ 080dd460 40000003

@ Refreshes the current text overlay palette row data to OBJ palette VRAM.
@ Reads overlay_ptr from gPrng+0x1d0; returns void if null. Reads [overlay+0x14] flags bit0: if bit0=1 copies from OBJ palette VRAM at 0x05000200 + tile_row_idx*0x20; if bit0=0 copies from BG/OBJ palette base 0x05000200 (DAT_080dd4a8). Both paths read [overlay+0x4] as tile_row_idx and compute the palette row address. Called exclusively by FUN_080d6d30 (pack frame driver) each frame.
@ 
@ Constants:
@ - gPrng+0x1d0: global overlay struct pointer
@ - 0x05000200: OBJ palette base + 0x200 (DAT_080dd4a8); python: 0xa0<<19=0x5000000+0x200=0x5000200
@ - PALETTE_STRIDE=0x20 // tile_row_idx*0x20 = palette row byte offset
@ 
@ Inputs: void (no params; ldr r0, gPrng loaded internally)
@ Returns: void (pop {r0}; bx r0)
@ Side effects: [OBJ palette 0x05000200 + tile_row_idx*0x20 via copy_overlay_tile_row_to_palette] palette row written
refresh_overlay_palette_row:
    push {lr}                                @ 080dd464 00b5
    ldr r0, PTR_gPrng_080dd490               @ 080dd466 0a48
    movs r1,#0xe8    @ 080dd468 e821
    lsls r1,r1,#0x1    @ 080dd46a 4900
    adds r0,r0,r1    @ 080dd46c 4018
    ldr r2,[r0,#0x0]                         @ 080dd46e 0268
    cmp r2,#0x0                              @ 080dd470 002a
    beq LAB_080dd4a2                         @ 080dd472 16d0
    ldr r0,[r2,#0x14]                        @ 080dd474 5069
    movs r1,#0x1    @ 080dd476 0121
    ands r0,r1    @ 080dd478 0840
    cmp r0,#0x0                              @ 080dd47a 0028
    beq LAB_080dd494                         @ 080dd47c 0ad0
    ldrh r2,[r2,#0x4]                        @ 080dd47e 9288
    lsls r0,r2,#0x5    @ 080dd480 5001
    movs r1,#0xa0    @ 080dd482 a021
    lsls r1,r1,#0x13    @ 080dd484 c904
    adds r0,r0,r1    @ 080dd486 4018
    movs r1,#0x0    @ 080dd488 0021
    bl copy_overlay_tile_row_to_palette      @ 080dd48a fff775ff
    b LAB_080dd4a2                           @ 080dd48e 08e0
PTR_gPrng_080dd490:
    .word  gPrng                          @ 080dd490 40000003
LAB_080dd494:
    ldrh r2,[r2,#0x4]                        @ 080dd494 9288
    lsls r0,r2,#0x5    @ 080dd496 5001
    ldr r1, DAT_080dd4a8                     @ 080dd498 0349
    adds r0,r0,r1    @ 080dd49a 4018
    movs r1,#0x0    @ 080dd49c 0021
    bl copy_overlay_tile_row_to_palette      @ 080dd49e fff76bff
LAB_080dd4a2:
    pop {r0}                                 @ 080dd4a2 01bc
    bx r0                                    @ 080dd4a4 0047
    .zero  0x2
DAT_080dd4a8:
    .word  0x05000200                     @ 080dd4a8 00020005

@ Overlay frame render entry. Reads overlay state struct pointer from gPrng+0x1d0; if non-null writes frame size fields ([+0xe]/[+0xa]=r0 low16, [+0x10]/[+0xc]=r0 high16), selects normal or alt tile path based on [+0x14] bit0. Each path: palette row update (copy_overlay_tile_row_to_palette), BG tile load (load_overlay_bg_tiles_to_vram or _alt), overlay text render (render_overlay_text_to_bg_vram). Finally zeroes [+0x1c] and calls tick_overlay_animation_step.
@ 
@ Constants:
@ OVERLAY_PTR_OFF = 0x1d0
@ FRAME_W_OFF     = 0xa
@ FRAME_H_OFF     = 0xc
@ FRAME_WE_OFF    = 0xe
@ FRAME_HE_OFF    = 0x10
@ MODE_FLAG_OFF   = 0x14
@ PAL_ROW_OFF     = 0x8
@ ANIM_FLAG_OFF   = 0x1c
@ 
@ Params: r0=u32 packed_size (bits[31:16]=height, bits[15:0]=width); r1=u16 palette_row_index; r2=const char* text_ptr
@ Return: r0=u32 tick_result (Sub-case E passthrough of tick_overlay_animation_step return)
render_overlay_frame_with_palette_and_text:
    push {r4,r5,r6,r7,lr}                    @ 080dd4ac f0b5
    adds r6,r0,#0x0    @ 080dd4ae 061c
    adds r5,r1,#0x0    @ 080dd4b0 0d1c
    adds r7,r2,#0x0    @ 080dd4b2 171c
    ldr r0, PTR_gPrng_080dd500               @ 080dd4b4 1248
    movs r1,#0xe8    @ 080dd4b6 e821
    lsls r1,r1,#0x1    @ 080dd4b8 4900
    adds r0,r0,r1    @ 080dd4ba 4018
    ldr r4,[r0,#0x0]                         @ 080dd4bc 0468
    cmp r4,#0x0                              @ 080dd4be 002c
    beq LAB_080dd530                         @ 080dd4c0 36d0
    strh r6,[r4,#0xe]                        @ 080dd4c2 e681
    strh r6,[r4,#0xa]                        @ 080dd4c4 6681
    lsrs r0,r6,#0x10    @ 080dd4c6 300c
    strh r0,[r4,#0x10]                       @ 080dd4c8 2082
    strh r0,[r4,#0xc]                        @ 080dd4ca a081
    ldr r0,[r4,#0x14]                        @ 080dd4cc 6069
    movs r1,#0x1    @ 080dd4ce 0121
    ands r0,r1    @ 080dd4d0 0840
    cmp r0,#0x0                              @ 080dd4d2 0028
    beq LAB_080dd504                         @ 080dd4d4 16d0
    ldrh r0,[r4,#0x8]                        @ 080dd4d6 2089
    cmp r5,r0                                @ 080dd4d8 8542
    beq LAB_080dd4f0                         @ 080dd4da 09d0
    ldrh r1,[r4,#0x4]                        @ 080dd4dc a188
    lsls r0,r1,#0x5    @ 080dd4de 4801
    movs r1,#0xa0    @ 080dd4e0 a021
    lsls r1,r1,#0x13    @ 080dd4e2 c904
    adds r0,r0,r1    @ 080dd4e4 4018
    lsls r1,r5,#0x10    @ 080dd4e6 2904
    lsrs r1,r1,#0x10    @ 080dd4e8 090c
    bl copy_overlay_tile_row_to_palette      @ 080dd4ea fff745ff
    strh r5,[r4,#0x8]                        @ 080dd4ee 2581
LAB_080dd4f0:
    adds r0,r6,#0x0    @ 080dd4f0 301c
    bl load_overlay_bg_tiles_to_vram         @ 080dd4f2 fff72ffb
    adds r0,r7,#0x0    @ 080dd4f6 381c
    bl render_overlay_text_to_bg_vram        @ 080dd4f8 fff7eafc
    b LAB_080dd528                           @ 080dd4fc 14e0
    .zero  0x2
PTR_gPrng_080dd500:
    .word  gPrng                          @ 080dd500 40000003
LAB_080dd504:
    ldrh r0,[r4,#0x8]                        @ 080dd504 2089
    cmp r5,r0                                @ 080dd506 8542
    beq LAB_080dd51c                         @ 080dd508 08d0
    ldrh r1,[r4,#0x4]                        @ 080dd50a a188
    lsls r0,r1,#0x5    @ 080dd50c 4801
    ldr r1, DAT_080dd538                     @ 080dd50e 0a49
    adds r0,r0,r1    @ 080dd510 4018
    lsls r1,r5,#0x10    @ 080dd512 2904
    lsrs r1,r1,#0x10    @ 080dd514 090c
    bl copy_overlay_tile_row_to_palette      @ 080dd516 fff72fff
    strh r5,[r4,#0x8]                        @ 080dd51a 2581
LAB_080dd51c:
    adds r0,r6,#0x0    @ 080dd51c 301c
    bl load_overlay_bg_tiles_to_vram_alt     @ 080dd51e fff72dfc
    adds r0,r7,#0x0    @ 080dd522 381c
    bl render_overlay_text_to_bg_vram        @ 080dd524 fff7d4fc
LAB_080dd528:
    movs r0,#0x0    @ 080dd528 0020
    strh r0,[r4,#0x1c]                       @ 080dd52a a083
    bl tick_overlay_animation_step           @ 080dd52c 00f05af8
LAB_080dd530:
    pop {r4,r5,r6,r7}                        @ 080dd530 f0bc
    pop {r0}                                 @ 080dd532 01bc
    bx r0                                    @ 080dd534 0047
    .zero  0x2
DAT_080dd538:
    .word  0x05000200                     @ 080dd538 00020005

@ 通用模态文本对话框/提示创建. 入参: r0 = (height<<16) | width, r1 = flags, r2 = char *text. 把 size split 写进内部 struct 的 [+0xa]/[+0xc], 再调 FUN_080dd070 计算并存 [+0xe]/[+0x10], 最后 FUN_080dcb54/FUN_080dced0 完成绘制. 被 13+ pack/save/dialog game_str 函数共用.
text_overlay_create:
    push {r4,r5,r6,r7,lr}                    @ 080dd53c f0b5
    .hword 0x4647    @ 080dd53e 4746
    push {r7}                                @ 080dd540 80b4
    adds r6,r0,#0x0    @ 080dd542 061c
    adds r7,r1,#0x0    @ 080dd544 0f1c
    .hword 0x4690    @ 080dd546 9046
    ldr r0, PTR_gPrng_080dd5a4               @ 080dd548 1648
    movs r1,#0xe8    @ 080dd54a e821
    lsls r1,r1,#0x1    @ 080dd54c 4900
    adds r0,r0,r1    @ 080dd54e 4018
    ldr r4,[r0,#0x0]                         @ 080dd550 0468
    cmp r4,#0x0                              @ 080dd552 002c
    beq LAB_080dd5d4                         @ 080dd554 3ed0
    strh r6,[r4,#0xa]                        @ 080dd556 6681
    lsrs r0,r6,#0x10    @ 080dd558 300c
    strh r0,[r4,#0xc]                        @ 080dd55a a081
    ldrh r1,[r4,#0xa]                        @ 080dd55c 6189
    ldrh r2,[r4,#0xc]                        @ 080dd55e a289
    .hword 0x4640    @ 080dd560 4046
    bl measure_overlay_text_dimensions       @ 080dd562 fff785fd
    adds r5,r0,#0x0    @ 080dd566 051c
    adds r6,r5,#0x0    @ 080dd568 2e1c
    strh r5,[r4,#0xe]                        @ 080dd56a e581
    lsrs r0,r5,#0x10    @ 080dd56c 280c
    strh r0,[r4,#0x10]                       @ 080dd56e 2082
    ldr r0,[r4,#0x14]                        @ 080dd570 6069
    movs r1,#0x1    @ 080dd572 0121
    ands r0,r1    @ 080dd574 0840
    cmp r0,#0x0                              @ 080dd576 0028
    beq LAB_080dd5a8                         @ 080dd578 16d0
    ldrh r0,[r4,#0x8]                        @ 080dd57a 2089
    cmp r7,r0                                @ 080dd57c 8742
    beq LAB_080dd594                         @ 080dd57e 09d0
    ldrh r1,[r4,#0x4]                        @ 080dd580 a188
    lsls r0,r1,#0x5    @ 080dd582 4801
    movs r1,#0xa0    @ 080dd584 a021
    lsls r1,r1,#0x13    @ 080dd586 c904
    adds r0,r0,r1    @ 080dd588 4018
    lsls r1,r7,#0x10    @ 080dd58a 3904
    lsrs r1,r1,#0x10    @ 080dd58c 090c
    bl copy_overlay_tile_row_to_palette      @ 080dd58e fff7f3fe
    strh r7,[r4,#0x8]                        @ 080dd592 2781
LAB_080dd594:
    adds r0,r5,#0x0    @ 080dd594 281c
    bl load_overlay_bg_tiles_to_vram         @ 080dd596 fff7ddfa
    .hword 0x4640    @ 080dd59a 4046
    bl render_overlay_text_to_bg_vram        @ 080dd59c fff798fc
    b LAB_080dd5cc                           @ 080dd5a0 14e0
    .zero  0x2
PTR_gPrng_080dd5a4:
    .word  gPrng                          @ 080dd5a4 40000003
LAB_080dd5a8:
    ldrh r0,[r4,#0x8]                        @ 080dd5a8 2089
    cmp r7,r0                                @ 080dd5aa 8742
    beq LAB_080dd5c0                         @ 080dd5ac 08d0
    ldrh r1,[r4,#0x4]                        @ 080dd5ae a188
    lsls r0,r1,#0x5    @ 080dd5b0 4801
    ldr r1, DAT_080dd5e0                     @ 080dd5b2 0b49
    adds r0,r0,r1    @ 080dd5b4 4018
    lsls r1,r7,#0x10    @ 080dd5b6 3904
    lsrs r1,r1,#0x10    @ 080dd5b8 090c
    bl copy_overlay_tile_row_to_palette      @ 080dd5ba fff7ddfe
    strh r7,[r4,#0x8]                        @ 080dd5be 2781
LAB_080dd5c0:
    adds r0,r6,#0x0    @ 080dd5c0 301c
    bl load_overlay_bg_tiles_to_vram_alt     @ 080dd5c2 fff7dbfb
    .hword 0x4640    @ 080dd5c6 4046
    bl render_overlay_text_to_bg_vram        @ 080dd5c8 fff782fc
LAB_080dd5cc:
    movs r0,#0x0    @ 080dd5cc 0020
    strh r0,[r4,#0x1c]                       @ 080dd5ce a083
    bl tick_overlay_animation_step           @ 080dd5d0 00f008f8
LAB_080dd5d4:
    pop {r3}                                 @ 080dd5d4 08bc
    .hword 0x4698    @ 080dd5d6 9846
    pop {r4,r5,r6,r7}                        @ 080dd5d8 f0bc
    pop {r0}                                 @ 080dd5da 01bc
    bx r0                                    @ 080dd5dc 0047
    .zero  0x2
DAT_080dd5e0:
    .word  0x05000200                     @ 080dd5e0 00020005

@ Advances the current text overlay animation state machine by one step.
@ Reads overlay_ptr from gPrng+0x1d0; returns 1 if null. Dispatches via switch([overlay+0x1c] step_counter [0..4]):
@ - case 0 (enter): writes 0x78 frames to [+0x20], computes initial x position to [+0x22] (flags bit3 determines indent range 0..0xf or 1)
@ - case 1 (fade-in): decrements [+0x1e] frame countdown; interpolates x position to [+0x22] using bios_div
@ - case 2 (wait/condition): checks flags bits and frame markers to decide next action
@ - case 3 (fade-out): decrements [+0x1e]; reverse-interpolates x position
@ - case 4 (done): clears [+0x1c], returns 1
@ - default path: based on [overlay+0x14] bit0 calls apply_overlay_bg_scroll_offset or render_overlay_oam_sprite_stretched; returns 0
@ r0=update_flag [0..1]: if 1 sets [overlay+0x24] bit0 in default path.
@ Called by 28+ pack/overlay frame driver functions; central hub for overlay animation progression.
@ 
@ Constants:
@ - gPrng+0x1d0: overlay struct pointer
@ - ANIM_DURATION=0x78=120 // initial frame count written at case 0
@ - INTERP_STEPS=0xf=15 // interpolation divisor for bios_div
@ - STEP_BASE=0x50 // x interpolation base offset (case 1: lsls r0,r1,#0x2; adds #0x50)
@ 
@ Inputs: r0=u8 update_flag [0..1]
@ Returns: r0=u8 (0=animation in progress, 1=animation complete or overlay null) via pop {r1}; bx r1 (Sub-case E)
@ Side effects: [overlay+0x1c] step_counter; [overlay+0x1e] frame_countdown; [overlay+0x20] anim_duration; [overlay+0x22] x_pos; [overlay+0x24] bit0/bit1; [BG scroll/OAM via apply_overlay_bg_scroll_offset/render_overlay_oam_sprite_stretched]
tick_overlay_animation_step:
    push {r4,r5,lr}                          @ 080dd5e4 30b5
    adds r5,r0,#0x0    @ 080dd5e6 051c
    ldr r2, PTR_gPrng_080dd5fc               @ 080dd5e8 044a
    movs r1,#0xe8    @ 080dd5ea e821
    lsls r1,r1,#0x1    @ 080dd5ec 4900
    adds r0,r2,r1    @ 080dd5ee 5018
    ldr r4,[r0,#0x0]                         @ 080dd5f0 0468
    cmp r4,#0x0                              @ 080dd5f2 002c
    bne LAB_080dd600                         @ 080dd5f4 04d1
    movs r0,#0x1    @ 080dd5f6 0120
    b LAB_080dd740                           @ 080dd5f8 a2e0
    .zero  0x2
PTR_gPrng_080dd5fc:
    .word  gPrng                          @ 080dd5fc 40000003
LAB_080dd600:
    ldrh r0,[r4,#0x1c]                       @ 080dd600 a08b
    cmp r0,#0x4                              @ 080dd602 0428
    bls LAB_080dd608                         @ 080dd604 00d9
    b switchD_080dd610__default              @ 080dd606 80e0
LAB_080dd608:
    lsls r0,r0,#0x2    @ 080dd608 8000
    ldr r1, DAT_080dd614                     @ 080dd60a 0249
    adds r0,r0,r1    @ 080dd60c 4018
    ldr r0,[r0,#0x0]                         @ 080dd60e 0068
switchD_080dd610__switchD:
    .hword 0x4687    @ 080dd610 8746
    .zero  0x2
DAT_080dd614:
    .word  0x080dd618                     @ 080dd614 18d60d08
switchD_080dd610__switchdataD_080dd618:
    .word  0x080dd62c                     @ 080dd618 2cd60d08
    .word  0x080dd658                     @ 080dd61c 58d60d08
    .word  0x080dd678                     @ 080dd620 78d60d08
    .word  0x080dd6d0                     @ 080dd624 d0d60d08
    .word  0x080dd702                     @ 080dd628 02d70d08
switchD_080dd610__caseD_0:
    movs r0,#0x78    @ 080dd62c 7820
    strh r0,[r4,#0x20]                       @ 080dd62e 2084
    ldrh r2,[r4,#0x10]                       @ 080dd630 228a
    lsls r0,r2,#0x2    @ 080dd632 9000
    adds r0,#0xa0    @ 080dd634 a030
    strh r0,[r4,#0x22]                       @ 080dd636 6084
    ldr r0,[r4,#0x14]                        @ 080dd638 6069
    movs r1,#0x8    @ 080dd63a 0821
    ands r0,r1    @ 080dd63c 0840
    movs r1,#0xf    @ 080dd63e 0f21
    cmp r0,#0x0                              @ 080dd640 0028
    beq LAB_080dd646                         @ 080dd642 00d0
    movs r1,#0x1    @ 080dd644 0121
LAB_080dd646:
    strh r1,[r4,#0x1e]                       @ 080dd646 e183
    adds r0,r4,#0x0    @ 080dd648 201c
    adds r0,#0x24    @ 080dd64a 2430
    movs r1,#0x2    @ 080dd64c 0221
    rsbs r1,r1,#0    @ 080dd64e 4942
    ldrb r2,[r0,#0x0]                        @ 080dd650 0278
    ands r1,r2    @ 080dd652 1140
    strb r1,[r0,#0x0]                        @ 080dd654 0170
    b LAB_080dd6fa                           @ 080dd656 50e0
switchD_080dd610__caseD_1:
    ldrh r0,[r4,#0x1e]                       @ 080dd658 e08b
    subs r0,#0x1    @ 080dd65a 0138
    strh r0,[r4,#0x1e]                       @ 080dd65c e083
    movs r0,#0x78    @ 080dd65e 7820
    strh r0,[r4,#0x20]                       @ 080dd660 2084
    ldrh r1,[r4,#0x10]                       @ 080dd662 218a
    lsls r0,r1,#0x2    @ 080dd664 8800
    adds r0,#0x50    @ 080dd666 5030
    ldrh r2,[r4,#0x1e]                       @ 080dd668 e28b
    muls r0,r2    @ 080dd66a 5043
    movs r1,#0xf    @ 080dd66c 0f21
    bl bios_div                              @ 080dd66e 30f0c5fe
    adds r0,#0x50    @ 080dd672 5030
    strh r0,[r4,#0x22]                       @ 080dd674 6084
    b LAB_080dd6f4                           @ 080dd676 3de0
switchD_080dd610__caseD_2:
    ldr r0,[r4,#0x14]                        @ 080dd678 6069
    movs r1,#0x4    @ 080dd67a 0421
    ands r0,r1    @ 080dd67c 0840
    cmp r0,#0x0                              @ 080dd67e 0028
    bne LAB_080dd6a4                         @ 080dd680 10d1
    movs r0,#0xa4    @ 080dd682 a420
    lsls r0,r0,#0x1    @ 080dd684 4000
    adds r1,r2,r0    @ 080dd686 1118
    movs r0,#0x1    @ 080dd688 0120
    ldrh r1,[r1,#0x0]                        @ 080dd68a 0988
    ands r0,r1    @ 080dd68c 0840
    cmp r0,#0x0                              @ 080dd68e 0028
    bne LAB_080dd6b2                         @ 080dd690 0fd1
    movs r0,#0xa3    @ 080dd692 a320
    lsls r0,r0,#0x1    @ 080dd694 4000
    adds r1,r2,r0    @ 080dd696 1118
    subs r0,#0x46    @ 080dd698 4638
    ldrh r1,[r1,#0x0]                        @ 080dd69a 0988
    ands r0,r1    @ 080dd69c 0840
    cmp r0,#0x0                              @ 080dd69e 0028
    bne LAB_080dd6b2                         @ 080dd6a0 07d1
    b switchD_080dd610__default              @ 080dd6a2 32e0
LAB_080dd6a4:
    adds r1,r4,#0x0    @ 080dd6a4 211c
    adds r1,#0x24    @ 080dd6a6 2431
    movs r0,#0x1    @ 080dd6a8 0120
    ldrb r1,[r1,#0x0]                        @ 080dd6aa 0978
    ands r0,r1    @ 080dd6ac 0840
    cmp r0,#0x0                              @ 080dd6ae 0028
    beq switchD_080dd610__default            @ 080dd6b0 2bd0
LAB_080dd6b2:
    ldr r0,[r4,#0x14]                        @ 080dd6b2 6069
    movs r1,#0x8    @ 080dd6b4 0821
    ands r0,r1    @ 080dd6b6 0840
    movs r1,#0xf    @ 080dd6b8 0f21
    cmp r0,#0x0                              @ 080dd6ba 0028
    beq LAB_080dd6c0                         @ 080dd6bc 00d0
    movs r1,#0x1    @ 080dd6be 0121
LAB_080dd6c0:
    strh r1,[r4,#0x1e]                       @ 080dd6c0 e183
    adds r0,r4,#0x0    @ 080dd6c2 201c
    adds r0,#0x24    @ 080dd6c4 2430
    movs r1,#0x1    @ 080dd6c6 0121
    ldrb r2,[r0,#0x0]                        @ 080dd6c8 0278
    orrs r1,r2    @ 080dd6ca 1143
    strb r1,[r0,#0x0]                        @ 080dd6cc 0170
    b LAB_080dd6fa                           @ 080dd6ce 14e0
switchD_080dd610__caseD_3:
    ldrh r0,[r4,#0x1e]                       @ 080dd6d0 e08b
    subs r0,#0x1    @ 080dd6d2 0138
    strh r0,[r4,#0x1e]                       @ 080dd6d4 e083
    movs r0,#0x78    @ 080dd6d6 7820
    strh r0,[r4,#0x20]                       @ 080dd6d8 2084
    ldrh r1,[r4,#0x10]                       @ 080dd6da 218a
    lsls r0,r1,#0x2    @ 080dd6dc 8800
    adds r0,#0x50    @ 080dd6de 5030
    ldrh r2,[r4,#0x1e]                       @ 080dd6e0 e28b
    muls r0,r2    @ 080dd6e2 5043
    movs r1,#0xf    @ 080dd6e4 0f21
    bl bios_div                              @ 080dd6e6 30f089fe
    ldrh r2,[r4,#0x10]                       @ 080dd6ea 228a
    lsls r1,r2,#0x2    @ 080dd6ec 9100
    subs r0,#0xa0    @ 080dd6ee a038
    subs r1,r1,r0    @ 080dd6f0 091a
    strh r1,[r4,#0x22]                       @ 080dd6f2 6184
LAB_080dd6f4:
    ldrh r0,[r4,#0x1e]                       @ 080dd6f4 e08b
    cmp r0,#0x0                              @ 080dd6f6 0028
    bne switchD_080dd610__default            @ 080dd6f8 07d1
LAB_080dd6fa:
    ldrh r0,[r4,#0x1c]                       @ 080dd6fa a08b
    adds r0,#0x1    @ 080dd6fc 0130
    strh r0,[r4,#0x1c]                       @ 080dd6fe a083
    b switchD_080dd610__default              @ 080dd700 03e0
switchD_080dd610__caseD_4:
    movs r0,#0x0    @ 080dd702 0020
    strh r0,[r4,#0x1c]                       @ 080dd704 a083
    movs r0,#0x1    @ 080dd706 0120
    b LAB_080dd740                           @ 080dd708 1ae0
switchD_080dd610__default:
    cmp r5,#0x1                              @ 080dd70a 012d
    bne LAB_080dd71a                         @ 080dd70c 05d1
    adds r1,r4,#0x0    @ 080dd70e 211c
    adds r1,#0x24    @ 080dd710 2431
    movs r0,#0x1    @ 080dd712 0120
    ldrb r2,[r1,#0x0]                        @ 080dd714 0a78
    orrs r0,r2    @ 080dd716 1043
    strb r0,[r1,#0x0]                        @ 080dd718 0870
LAB_080dd71a:
    ldr r0,[r4,#0x14]                        @ 080dd71a 6069
    movs r1,#0x1    @ 080dd71c 0121
    ands r0,r1    @ 080dd71e 0840
    cmp r0,#0x0                              @ 080dd720 0028
    beq LAB_080dd732                         @ 080dd722 06d0
    movs r1,#0x20    @ 080dd724 2021
    ldrsh r0,[r4,r1]                         @ 080dd726 605e
    movs r2,#0x22    @ 080dd728 2222
    ldrsh r1,[r4,r2]                         @ 080dd72a a15e
    bl apply_overlay_bg_scroll_offset        @ 080dd72c fff7d0fd
    b LAB_080dd73e                           @ 080dd730 05e0
LAB_080dd732:
    movs r1,#0x20    @ 080dd732 2021
    ldrsh r0,[r4,r1]                         @ 080dd734 605e
    movs r2,#0x22    @ 080dd736 2222
    ldrsh r1,[r4,r2]                         @ 080dd738 a15e
    bl render_overlay_oam_sprite_stretched   @ 080dd73a fff713fd
LAB_080dd73e:
    movs r0,#0x0    @ 080dd73e 0020
LAB_080dd740:
    pop {r4,r5}                              @ 080dd740 30bc
    pop {r1}                                 @ 080dd742 02bc
    bx r1                                    @ 080dd744 0847
    .zero  0x2

@ Called on pack scene entry; clears DISPCNT(0x04000000):=0 to disable all layers, then calls reset_affine_bg_matrix_and_scroll/reset_display_and_obj_vram/reset_all_bg_scroll_regs_and_shadows to reset BG matrices and scroll shadow registers, finally calls zero_fill_halfword_wrapper to zero VRAM 0x06000000..+0x18000*2 (covers all BG+OBJ tile area, ~192KB).
@ Constants: DISPCNT=0x04000000, VRAM_BASE=0x06000000, VRAM_CLEAR_COUNT=0x18000.
@ Inputs: void. Returns: void (pop {r0}; bx r0).
@ Side effects: [DISPCNT]:=0; full VRAM zeroed.
reset_pack_scene_display:
    push {lr}                                @ 080dd748 00b5
    movs r1,#0x80    @ 080dd74a 8021
    lsls r1,r1,#0x13    @ 080dd74c c904
    movs r0,#0x0    @ 080dd74e 0020
    strh r0,[r1,#0x0]                        @ 080dd750 0880
    bl reset_affine_bg_matrix_and_scroll     @ 080dd752 10f083fb
    movs r0,#0x0    @ 080dd756 0020
    bl reset_display_and_obj_vram            @ 080dd758 19f08cff
    bl reset_all_bg_scroll_regs_and_shadows  @ 080dd75c 18f094f9
    movs r0,#0xc0    @ 080dd760 c020
    lsls r0,r0,#0x13    @ 080dd762 c004
    movs r1,#0xc0    @ 080dd764 c021
    lsls r1,r1,#0x9    @ 080dd766 4902
    bl zero_fill_halfword_wrapper            @ 080dd768 17f096fb
    pop {r0}                                 @ 080dd76c 01bc
    bx r0                                    @ 080dd76e 0047

@ Renders overlay object as a tiled OAM sprite sequence (supports multiple rows and columns). Packed parameters: r0=packed xy (y<<16|x), r1=packed wh (height<<16|width), r2=packed attrs (palette<<16|tile_base), r3=ctx_ptr. Unpacks parameters, looks up POT level from 0x09e49558 tile frame table, calls write_oam_entry_from_packed_args per row per col. Called by multiple pack/scene render functions.
@ 
@ Constants:
@ - 0x09e49558: overlay tile frame data table (ROM)
@ - 0x0000ffff: empty tile sentinel
render_overlay_oam_sprite_tiled:
    push {r4,r5,r6,r7,lr}                    @ 080dd770 f0b5
    .hword 0x4657    @ 080dd772 5746
    .hword 0x464e    @ 080dd774 4e46
    .hword 0x4645    @ 080dd776 4546
    push {r5,r6,r7}                          @ 080dd778 e0b4
    sub sp,#0x38                             @ 080dd77a 8eb0
    str r3,[sp,#0x0]                         @ 080dd77c 0093
    movs r3,#0x0    @ 080dd77e 0023
    .hword 0x469a    @ 080dd780 9a46
    lsls r3,r0,#0x10    @ 080dd782 0304
    lsrs r3,r3,#0x10    @ 080dd784 1b0c
    str r3,[sp,#0x4]                         @ 080dd786 0193
    lsls r3,r1,#0x10    @ 080dd788 0b04
    lsrs r3,r3,#0x10    @ 080dd78a 1b0c
    str r3,[sp,#0x8]                         @ 080dd78c 0293
    lsrs r1,r1,#0x10    @ 080dd78e 090c
    str r1,[sp,#0xc]                         @ 080dd790 0391
    lsls r1,r2,#0x10    @ 080dd792 1104
    lsrs r1,r1,#0x10    @ 080dd794 090c
    str r1,[sp,#0x10]                        @ 080dd796 0491
    lsrs r2,r2,#0x10    @ 080dd798 120c
    str r2,[sp,#0x14]                        @ 080dd79a 0592
    movs r6,#0x3    @ 080dd79c 0326
    ldr r7,[sp,#0xc]                         @ 080dd79e 039f
    .hword 0x46b8    @ 080dd7a0 b846
    lsrs r0,r0,#0x10    @ 080dd7a2 000c
    str r0,[sp,#0x18]                        @ 080dd7a4 0690
    .hword 0x4640    @ 080dd7a6 4046
    cmp r0,#0x0                              @ 080dd7a8 0028
    ble LAB_080dd89e                         @ 080dd7aa 78dd
LAB_080dd7ac:
    movs r0,#0x1    @ 080dd7ac 0120
    lsls r0,r6    @ 080dd7ae b040
    cmp r8,r0                                @ 080dd7b0 8045
    bge LAB_080dd7c0                         @ 080dd7b2 05da
    movs r1,#0x1    @ 080dd7b4 0121
LAB_080dd7b6:
    subs r6,#0x1    @ 080dd7b6 013e
    adds r0,r1,#0x0    @ 080dd7b8 081c
    lsls r0,r6    @ 080dd7ba b040
    cmp r8,r0                                @ 080dd7bc 8045
    blt LAB_080dd7b6                         @ 080dd7be fadb
LAB_080dd7c0:
    movs r4,#0x3    @ 080dd7c0 0324
    ldr r5,[sp,#0x8]                         @ 080dd7c2 029d
    ldr r1,[sp,#0x4]                         @ 080dd7c4 0199
    .hword 0x4689    @ 080dd7c6 8946
    cmp r5,#0x0                              @ 080dd7c8 002d
    ble LAB_080dd888                         @ 080dd7ca 5ddd
    ldr r2,[sp,#0x18]                        @ 080dd7cc 069a
    lsls r2,r2,#0x10    @ 080dd7ce 1204
    str r2,[sp,#0x30]                        @ 080dd7d0 0c92
    ldr r3,[sp,#0x14]                        @ 080dd7d2 059b
    lsls r3,r3,#0xc    @ 080dd7d4 1b03
    str r3,[sp,#0x2c]                        @ 080dd7d6 0b93
    ldr r7,[sp,#0x0]                         @ 080dd7d8 009f
    lsls r7,r7,#0xa    @ 080dd7da bf02
    str r7,[sp,#0x28]                        @ 080dd7dc 0a97
    lsls r0,r6,#0x2    @ 080dd7de b000
    str r0,[sp,#0x34]                        @ 080dd7e0 0d90
    ldr r1,[sp,#0xc]                         @ 080dd7e2 0399
    .hword 0x4642    @ 080dd7e4 4246
    subs r0,r1,r2    @ 080dd7e6 881a
    lsls r0,r0,#0x4    @ 080dd7e8 0001
    str r0,[sp,#0x1c]                        @ 080dd7ea 0790
LAB_080dd7ec:
    movs r0,#0x1    @ 080dd7ec 0120
    lsls r0,r4    @ 080dd7ee a040
    .hword 0x464f    @ 080dd7f0 4f46
    lsls r3,r7,#0x10    @ 080dd7f2 3b04
    ldr r1,[sp,#0x8]                         @ 080dd7f4 0299
    subs r1,r1,r5    @ 080dd7f6 491b
    str r1,[sp,#0x24]                        @ 080dd7f8 0991
    .hword 0x4652    @ 080dd7fa 5246
    adds r2,#0x1    @ 080dd7fc 0132
    str r2,[sp,#0x20]                        @ 080dd7fe 0892
    cmp r5,r0                                @ 080dd800 8542
    bge LAB_080dd810                         @ 080dd802 05da
    movs r1,#0x1    @ 080dd804 0121
LAB_080dd806:
    subs r4,#0x1    @ 080dd806 013c
    adds r0,r1,#0x0    @ 080dd808 081c
    lsls r0,r4    @ 080dd80a a040
    cmp r5,r0                                @ 080dd80c 8542
    blt LAB_080dd806                         @ 080dd80e fadb
LAB_080dd810:
    ldr r7, DAT_080dd830                     @ 080dd810 074f
    .hword 0x46ba    @ 080dd812 ba46
    ldr r0, DAT_080dd834                     @ 080dd814 0748
    .hword 0x4684    @ 080dd816 8446
    lsls r2,r6,#0x2    @ 080dd818 b200
LAB_080dd81a:
    adds r0,r4,r2    @ 080dd81a a018
    lsls r0,r0,#0x1    @ 080dd81c 4000
    add r0,r10                               @ 080dd81e 5044
    adds r1,r2,#0x0    @ 080dd820 111c
    ldrh r0,[r0,#0x0]                        @ 080dd822 0088
    cmp r0,r12                               @ 080dd824 6045
    bne LAB_080dd848                         @ 080dd826 0fd1
    cmp r4,#0x1                              @ 080dd828 012c
    ble LAB_080dd838                         @ 080dd82a 05dd
    subs r4,#0x1    @ 080dd82c 013c
    b LAB_080dd81a                           @ 080dd82e f4e7
DAT_080dd830:
    .word  0x09e49558                     @ 080dd830 5895e409
DAT_080dd834:
    .word  0x0000ffff                     @ 080dd834 ffff0000
LAB_080dd838:
    cmp r6,#0x1                              @ 080dd838 012e
    ble LAB_080dd848                         @ 080dd83a 05dd
    subs r2,r1,#0x4    @ 080dd83c 0a1f
    ldr r1,[sp,#0x34]                        @ 080dd83e 0d99
    subs r1,#0x4    @ 080dd840 0439
    str r1,[sp,#0x34]                        @ 080dd842 0d91
    subs r6,#0x1    @ 080dd844 013e
    b LAB_080dd81a                           @ 080dd846 e8e7
LAB_080dd848:
    lsrs r0,r3,#0x10    @ 080dd848 180c
    ldr r2,[sp,#0x30]                        @ 080dd84a 0c9a
    orrs r0,r2    @ 080dd84c 1043
    ldr r3,[sp,#0x34]                        @ 080dd84e 0d9b
    adds r1,r4,r3    @ 080dd850 e118
    lsls r1,r1,#0x1    @ 080dd852 4900
    ldr r7, DAT_080dd8b0                     @ 080dd854 164f
    adds r1,r1,r7    @ 080dd856 c919
    ldrh r1,[r1,#0x0]                        @ 080dd858 0988
    ldr r2,[sp,#0x2c]                        @ 080dd85a 0b9a
    ldr r3,[sp,#0x28]                        @ 080dd85c 0a9b
    orrs r2,r3    @ 080dd85e 1a43
    ldr r7,[sp,#0x10]                        @ 080dd860 049f
    ldr r3,[sp,#0x24]                        @ 080dd862 099b
    adds r7,r7,r3    @ 080dd864 ff18
    .hword 0x46ba    @ 080dd866 ba46
    ldr r3,[sp,#0x1c]                        @ 080dd868 079b
    add r3,r10                               @ 080dd86a 5344
    orrs r2,r3    @ 080dd86c 1a43
    lsls r2,r2,#0x10    @ 080dd86e 1204
    lsrs r2,r2,#0x10    @ 080dd870 120c
    bl write_oam_entry_from_packed_args      @ 080dd872 18f07bfc
    ldr r7,[sp,#0x20]                        @ 080dd876 089f
    .hword 0x46ba    @ 080dd878 ba46
    movs r0,#0x1    @ 080dd87a 0120
    lsls r0,r4    @ 080dd87c a040
    subs r5,r5,r0    @ 080dd87e 2d1a
    lsls r0,r0,#0x3    @ 080dd880 c000
    add r9,r0                                @ 080dd882 8144
    cmp r5,#0x0                              @ 080dd884 002d
    bgt LAB_080dd7ec                         @ 080dd886 b1dc
LAB_080dd888:
    movs r0,#0x1    @ 080dd888 0120
    lsls r0,r6    @ 080dd88a b040
    .hword 0x4641    @ 080dd88c 4146
    subs r1,r1,r0    @ 080dd88e 091a
    .hword 0x4688    @ 080dd890 8846
    lsls r0,r0,#0x3    @ 080dd892 c000
    ldr r2,[sp,#0x18]                        @ 080dd894 069a
    adds r2,r2,r0    @ 080dd896 1218
    str r2,[sp,#0x18]                        @ 080dd898 0692
    cmp r1,#0x0                              @ 080dd89a 0029
    bgt LAB_080dd7ac                         @ 080dd89c 86dc
LAB_080dd89e:
    .hword 0x4650    @ 080dd89e 5046
    add sp,#0x38                             @ 080dd8a0 0eb0
    pop {r3,r4,r5}                           @ 080dd8a2 38bc
    .hword 0x4698    @ 080dd8a4 9846
    .hword 0x46a1    @ 080dd8a6 a146
    .hword 0x46aa    @ 080dd8a8 aa46
    pop {r4,r5,r6,r7}                        @ 080dd8aa f0bc
    pop {r1}                                 @ 080dd8ac 02bc
    bx r1                                    @ 080dd8ae 0847
DAT_080dd8b0:
    .word  0x09e49558                     @ 080dd8b0 5895e409

@ Decomposes a packed GBA 15-bit color value into R/G/B channels and computes channel max/mid values. r0=packed color (GBA RGB555: bit[4:0]=R, bit[9:5]=G, bit[14:10]=B). Extracts three channels, finds max, uses bios_div to compute interpolation ratio if two channels are equal; writes results to r2/r3 output slots. Called by color interpolation functions for overlay fade effects.
@ 
@ Constants:
@ - 0x1f: GBA color channel 5-bit mask
@ - 0x3e0=0xf8<<2: G channel mask (bits[9:5])
@ - 0x7c00=0xf8<<7: B channel mask (bits[14:10])
decode_overlay_color_channels:
    push {r4,r5,r6,r7,lr}                    @ 080dd8b4 f0b5
    .hword 0x4657    @ 080dd8b6 5746
    .hword 0x464e    @ 080dd8b8 4e46
    .hword 0x4645    @ 080dd8ba 4546
    push {r5,r6,r7}                          @ 080dd8bc e0b4
    .hword 0x468a    @ 080dd8be 8a46
    .hword 0x4691    @ 080dd8c0 9146
    .hword 0x4698    @ 080dd8c2 9846
    lsls r0,r0,#0x10    @ 080dd8c4 0004
    lsrs r0,r0,#0x10    @ 080dd8c6 000c
    movs r1,#0x1f    @ 080dd8c8 1f21
    ands r1,r0    @ 080dd8ca 0140
    lsls r6,r1,#0x3    @ 080dd8cc ce00
    movs r1,#0xf8    @ 080dd8ce f821
    lsls r1,r1,#0x2    @ 080dd8d0 8900
    ands r1,r0    @ 080dd8d2 0140
    lsrs r5,r1,#0x2    @ 080dd8d4 8d08
    movs r1,#0xf8    @ 080dd8d6 f821
    lsls r1,r1,#0x7    @ 080dd8d8 c901
    ands r1,r0    @ 080dd8da 0140
    lsrs r4,r1,#0x7    @ 080dd8dc cc09
    adds r0,r5,#0x0    @ 080dd8de 281c
    cmp r5,r6                                @ 080dd8e0 b542
    bge LAB_080dd8e6                         @ 080dd8e2 00da
    adds r0,r6,#0x0    @ 080dd8e4 301c
LAB_080dd8e6:
    adds r1,r4,#0x0    @ 080dd8e6 211c
    cmp r4,r0                                @ 080dd8e8 8442
    bge LAB_080dd8ee                         @ 080dd8ea 00da
    adds r1,r0,#0x0    @ 080dd8ec 011c
LAB_080dd8ee:
    .hword 0x4640    @ 080dd8ee 4046
    str r1,[r0,#0x0]                         @ 080dd8f0 0160
    adds r2,r5,#0x0    @ 080dd8f2 2a1c
    cmp r5,r6                                @ 080dd8f4 b542
    ble LAB_080dd8fa                         @ 080dd8f6 00dd
    adds r2,r6,#0x0    @ 080dd8f8 321c
LAB_080dd8fa:
    adds r0,r4,#0x0    @ 080dd8fa 201c
    cmp r4,r2                                @ 080dd8fc 9442
    ble LAB_080dd902                         @ 080dd8fe 00dd
    adds r0,r2,#0x0    @ 080dd900 101c
LAB_080dd902:
    subs r7,r1,r0    @ 080dd902 0f1a
    cmp r1,#0x0                              @ 080dd904 0029
    beq LAB_080dd912                         @ 080dd906 04d0
    lsls r0,r7,#0x8    @ 080dd908 3802
    subs r0,r0,r7    @ 080dd90a c01b
    bl bios_div                              @ 080dd90c 30f076fd
    b LAB_080dd914                           @ 080dd910 00e0
LAB_080dd912:
    movs r0,#0x0    @ 080dd912 0020
LAB_080dd914:
    .hword 0x4649    @ 080dd914 4946
    str r0,[r1,#0x0]                         @ 080dd916 0860
    movs r1,#0x0    @ 080dd918 0021
    cmp r0,#0x0                              @ 080dd91a 0028
    beq LAB_080dd96e                         @ 080dd91c 27d0
    .hword 0x4642    @ 080dd91e 4246
    ldr r3,[r2,#0x0]                         @ 080dd920 1368
    cmp r6,r3                                @ 080dd922 9e42
    bne LAB_080dd934                         @ 080dd924 06d1
    subs r0,r5,r4    @ 080dd926 281b
    lsls r0,r0,#0x8    @ 080dd928 0002
    adds r1,r7,#0x0    @ 080dd92a 391c
    bl bios_div                              @ 080dd92c 30f066fd
    adds r1,r0,#0x0    @ 080dd930 011c
    b LAB_080dd95c                           @ 080dd932 13e0
LAB_080dd934:
    cmp r5,r3                                @ 080dd934 9d42
    bne LAB_080dd948                         @ 080dd936 07d1
    subs r0,r4,r6    @ 080dd938 a01b
    lsls r0,r0,#0x8    @ 080dd93a 0002
    adds r1,r7,#0x0    @ 080dd93c 391c
    bl bios_div                              @ 080dd93e 30f05dfd
    movs r2,#0x80    @ 080dd942 8022
    lsls r2,r2,#0x2    @ 080dd944 9200
    b LAB_080dd95a                           @ 080dd946 08e0
LAB_080dd948:
    cmp r4,r3                                @ 080dd948 9c42
    bne LAB_080dd95c                         @ 080dd94a 07d1
    subs r0,r6,r5    @ 080dd94c 701b
    lsls r0,r0,#0x8    @ 080dd94e 0002
    adds r1,r7,#0x0    @ 080dd950 391c
    bl bios_div                              @ 080dd952 30f053fd
    movs r2,#0x80    @ 080dd956 8022
    lsls r2,r2,#0x3    @ 080dd958 d200
LAB_080dd95a:
    adds r1,r0,r2    @ 080dd95a 8118
LAB_080dd95c:
    lsls r0,r1,#0x4    @ 080dd95c 0801
    subs r0,r0,r1    @ 080dd95e 401a
    lsls r1,r0,#0x2    @ 080dd960 8100
    asrs r1,r1,#0x8    @ 080dd962 0912
    cmp r1,#0x0                              @ 080dd964 0029
    bge LAB_080dd96e                         @ 080dd966 02da
    movs r0,#0xb4    @ 080dd968 b420
    lsls r0,r0,#0x1    @ 080dd96a 4000
    adds r1,r1,r0    @ 080dd96c 0918
LAB_080dd96e:
    .hword 0x4652    @ 080dd96e 5246
    str r1,[r2,#0x0]                         @ 080dd970 1160
    pop {r3,r4,r5}                           @ 080dd972 38bc
    .hword 0x4698    @ 080dd974 9846
    .hword 0x46a1    @ 080dd976 a146
    .hword 0x46aa    @ 080dd978 aa46
    pop {r4,r5,r6,r7}                        @ 080dd97a f0bc
    pop {r0}                                 @ 080dd97c 01bc
    bx r0                                    @ 080dd97e 0047

@ Converts HSV (hue/saturation/value) color to GBA RGB555 packed format.
@ r0=hue_phase [0..0x167] (divided by 0x168 to get 6-sector index 0..5), r1=saturation [0..0xff], r2=value [0..0xff].
@ Computes p/q/t intermediate values, dispatches R/G/B channel assignments via switch(sector 0..5), normalizes via bios_div, and packs as GBA 15-bit color (R[4:0], G[9:5], B[14:10]).
@ Called by overlay color fade/HSV-rotation paths to generate per-frame color animation.
@ Constants: HUE_PERIOD=0x168=360, SATURATION_MAX=0xb4=180, VALUE_MAX=0xff=255, RGB_CHANNEL_BITS=0x1f, G_SHIFT=5, B_SHIFT=10.
@ Inputs: r0=u16 hue_phase, r1=u8 saturation, r2=u8 value. Returns: r0=u16 packed GBA RGB555.
@ Side effects: none (pure computation).
convert_hsv_to_gba_rgb555:
    push {r4,r5,r6,r7,lr}                    @ 080dd980 f0b5
    .hword 0x4657    @ 080dd982 5746
    .hword 0x464e    @ 080dd984 4e46
    .hword 0x4645    @ 080dd986 4546
    push {r5,r6,r7}                          @ 080dd988 e0b4
    sub sp,#0x4                              @ 080dd98a 81b0
    adds r4,r0,#0x0    @ 080dd98c 041c
    .hword 0x4688    @ 080dd98e 8846
    adds r7,r2,#0x0    @ 080dd990 171c
    movs r0,#0x0    @ 080dd992 0020
    .hword 0x4682    @ 080dd994 8246
    lsls r0,r4,#0x1    @ 080dd996 6000
    adds r0,r0,r4    @ 080dd998 0019
    lsls r0,r0,#0x1    @ 080dd99a 4000
    movs r1,#0xb4    @ 080dd99c b421
    lsls r1,r1,#0x1    @ 080dd99e 4900
    bl get_bios_div_remainder                @ 080dd9a0 30f02efd
    adds r5,r0,#0x0    @ 080dd9a4 051c
    lsls r4,r4,#0x8    @ 080dd9a6 2402
    adds r0,r4,#0x0    @ 080dd9a8 201c
    movs r1,#0x3c    @ 080dd9aa 3c21
    bl bios_div                              @ 080dd9ac 30f026fd
    asrs r0,r0,#0x8    @ 080dd9b0 0012
    str r0,[sp,#0x0]                         @ 080dd9b2 0090
    movs r4,#0xff    @ 080dd9b4 ff24
    .hword 0x4641    @ 080dd9b6 4146
    subs r0,r4,r1    @ 080dd9b8 601a
    muls r0,r7    @ 080dd9ba 7843
    movs r1,#0xff    @ 080dd9bc ff21
    bl bios_div                              @ 080dd9be 30f01dfd
    adds r6,r0,#0x0    @ 080dd9c2 061c
    .hword 0x4640    @ 080dd9c4 4046
    muls r0,r5    @ 080dd9c6 6843
    movs r1,#0xb4    @ 080dd9c8 b421
    lsls r1,r1,#0x1    @ 080dd9ca 4900
    bl bios_div                              @ 080dd9cc 30f016fd
    subs r0,r4,r0    @ 080dd9d0 201a
    muls r0,r7    @ 080dd9d2 7843
    movs r1,#0xff    @ 080dd9d4 ff21
    bl bios_div                              @ 080dd9d6 30f011fd
    .hword 0x4681    @ 080dd9da 8146
    movs r2,#0xb4    @ 080dd9dc b422
    lsls r2,r2,#0x1    @ 080dd9de 5200
    subs r5,r2,r5    @ 080dd9e0 551b
    .hword 0x4640    @ 080dd9e2 4046
    muls r0,r5    @ 080dd9e4 6843
    adds r1,r2,#0x0    @ 080dd9e6 111c
    bl bios_div                              @ 080dd9e8 30f008fd
    subs r4,r4,r0    @ 080dd9ec 241a
    adds r0,r7,#0x0    @ 080dd9ee 381c
    muls r0,r4    @ 080dd9f0 6043
    movs r1,#0xff    @ 080dd9f2 ff21
    bl bios_div                              @ 080dd9f4 30f002fd
    adds r3,r0,#0x0    @ 080dd9f8 031c
    ldr r0,[sp,#0x0]                         @ 080dd9fa 0098
    cmp r0,#0x5                              @ 080dd9fc 0528
    bhi switchD_080dda08__default            @ 080dd9fe 2bd8
    lsls r0,r0,#0x2    @ 080dda00 8000
    ldr r1, DAT_080dda0c                     @ 080dda02 0249
    adds r0,r0,r1    @ 080dda04 4018
    ldr r0,[r0,#0x0]                         @ 080dda06 0068
switchD_080dda08__switchD:
    .hword 0x4687    @ 080dda08 8746
    .zero  0x2
DAT_080dda0c:
    .word  0x080dda10                     @ 080dda0c 10da0d08
switchD_080dda08__switchdataD_080dda10:
    .word  0x080dda28                     @ 080dda10 28da0d08
    .word  0x080dda30                     @ 080dda14 30da0d08
    .word  0x080dda38                     @ 080dda18 38da0d08
    .word  0x080dda40                     @ 080dda1c 40da0d08
    .word  0x080dda48                     @ 080dda20 48da0d08
    .word  0x080dda50                     @ 080dda24 50da0d08
switchD_080dda08__caseD_0:
    adds r0,r7,#0x0    @ 080dda28 381c
    adds r2,r3,#0x0    @ 080dda2a 1a1c
    .hword 0x46b2    @ 080dda2c b246
    b LAB_080dda5c                           @ 080dda2e 15e0
switchD_080dda08__caseD_1:
    .hword 0x4648    @ 080dda30 4846
    adds r2,r7,#0x0    @ 080dda32 3a1c
    .hword 0x46b2    @ 080dda34 b246
    b LAB_080dda5c                           @ 080dda36 11e0
switchD_080dda08__caseD_2:
    adds r0,r6,#0x0    @ 080dda38 301c
    adds r2,r7,#0x0    @ 080dda3a 3a1c
    .hword 0x469a    @ 080dda3c 9a46
    b LAB_080dda5c                           @ 080dda3e 0de0
switchD_080dda08__caseD_3:
    adds r0,r6,#0x0    @ 080dda40 301c
    .hword 0x464a    @ 080dda42 4a46
    .hword 0x46ba    @ 080dda44 ba46
    b LAB_080dda5c                           @ 080dda46 09e0
switchD_080dda08__caseD_4:
    adds r0,r3,#0x0    @ 080dda48 181c
    adds r2,r6,#0x0    @ 080dda4a 321c
    .hword 0x46ba    @ 080dda4c ba46
    b LAB_080dda5c                           @ 080dda4e 05e0
switchD_080dda08__caseD_5:
    adds r0,r7,#0x0    @ 080dda50 381c
    adds r2,r6,#0x0    @ 080dda52 321c
    .hword 0x46ca    @ 080dda54 ca46
    b LAB_080dda5c                           @ 080dda56 01e0
switchD_080dda08__default:
    movs r0,#0x0    @ 080dda58 0020
    movs r2,#0x0    @ 080dda5a 0022
LAB_080dda5c:
    asrs r0,r0,#0x3    @ 080dda5c c010
    movs r1,#0x1f    @ 080dda5e 1f21
    ands r0,r1    @ 080dda60 0840
    lsls r1,r2,#0x2    @ 080dda62 9100
    movs r3,#0xf8    @ 080dda64 f823
    lsls r3,r3,#0x2    @ 080dda66 9b00
    adds r2,r3,#0x0    @ 080dda68 1a1c
    ands r1,r2    @ 080dda6a 1140
    orrs r0,r1    @ 080dda6c 0843
    .hword 0x4652    @ 080dda6e 5246
    lsls r1,r2,#0x7    @ 080dda70 d101
    movs r3,#0xf8    @ 080dda72 f823
    lsls r3,r3,#0x7    @ 080dda74 db01
    adds r2,r3,#0x0    @ 080dda76 1a1c
    ands r1,r2    @ 080dda78 1140
    orrs r0,r1    @ 080dda7a 0843
    add sp,#0x4                              @ 080dda7c 01b0
    pop {r3,r4,r5}                           @ 080dda7e 38bc
    .hword 0x4698    @ 080dda80 9846
    .hword 0x46a1    @ 080dda82 a146
    .hword 0x46aa    @ 080dda84 aa46
    pop {r4,r5,r6,r7}                        @ 080dda86 f0bc
    pop {r1}                                 @ 080dda88 02bc
    bx r1                                    @ 080dda8a 0847

@ Per-pixel HSV hue rotation. Iterates over pixel_count pixels (r2 low16): for each pixel calls decode_overlay_color_channels to decode RGB channels, adds r7 to hue and wraps modulo 0x168 (full hue cycle), calls convert_hsv_to_gba_rgb555 to convert back, writes to dst buffer. Called by pack_080d5470 and pack_080d933c on pack cover hue rotation animation frames.
@ 
@ Constants:
@ HUE_CYCLE  = 0x168
@ COUNT_MASK = 0xffff
@ 
@ Params: r0=const u16* src_ptr; r1=u16* dst_ptr; r2=u32 packed_count_hue (bits[15:0]=pixel_count [0..0xffff]; bits[31:16]=hue_shift_base)
@ Return: r0=u16* dst_end_ptr (Sub-case E passthrough)
rotate_pixel_hue_in_buffer:
    push {r4,r5,r6,r7,lr}                    @ 080dda8c f0b5
    sub sp,#0xc                              @ 080dda8e 83b0
    adds r6,r0,#0x0    @ 080dda90 061c
    adds r5,r1,#0x0    @ 080dda92 0d1c
    lsls r0,r2,#0x10    @ 080dda94 1004
    lsrs r0,r0,#0x10    @ 080dda96 000c
    lsrs r7,r2,#0x10    @ 080dda98 170c
    cmp r0,#0x0                              @ 080dda9a 0028
    beq LAB_080ddace                         @ 080dda9c 17d0
    adds r4,r0,#0x0    @ 080dda9e 041c
LAB_080ddaa0:
    ldrh r0,[r6,#0x0]                        @ 080ddaa0 3088
    .hword 0x4669    @ 080ddaa2 6946
    add r2,sp,#0x4                           @ 080ddaa4 01aa
    add r3,sp,#0x8                           @ 080ddaa6 02ab
    bl decode_overlay_color_channels         @ 080ddaa8 fff704ff
    ldr r0,[sp,#0x0]                         @ 080ddaac 0098
    adds r0,r0,r7    @ 080ddaae c019
    movs r1,#0xb4    @ 080ddab0 b421
    lsls r1,r1,#0x1    @ 080ddab2 4900
    bl get_bios_div_remainder                @ 080ddab4 30f0a4fc
    str r0,[sp,#0x0]                         @ 080ddab8 0090
    ldr r1,[sp,#0x4]                         @ 080ddaba 0199
    ldr r2,[sp,#0x8]                         @ 080ddabc 029a
    bl convert_hsv_to_gba_rgb555             @ 080ddabe fff75fff
    strh r0,[r5,#0x0]                        @ 080ddac2 2880
    adds r6,#0x2    @ 080ddac4 0236
    adds r5,#0x2    @ 080ddac6 0235
    subs r4,#0x1    @ 080ddac8 013c
    cmp r4,#0x0                              @ 080ddaca 002c
    bne LAB_080ddaa0                         @ 080ddacc e8d1
LAB_080ddace:
    add sp,#0xc                              @ 080ddace 03b0
    pop {r4,r5,r6,r7}                        @ 080ddad0 f0bc
    pop {r0}                                 @ 080ddad2 01bc
    bx r0                                    @ 080ddad4 0047
    .zero  0x2

@ Per-pixel brightness normalization/scaling. Symmetric structure with rotate_pixel_hue_in_buffer but processes the value (brightness) channel: decodes each pixel, finds max of RGB channels, scales val channel so brightest pixel reaches BRIGHT_FULL=0x100, converts back to GBA RGB555 and writes. r8=0x100 is an internal constant (asm 080ddaf0: movs r0,#0x80; lsls r0,#0x1; mov r8,r0), not caller-set. Called by pack_banner_080d46a8 during cover image brightness equalization.
@ 
@ Constants:
@ BRIGHT_FULL = 0x100
@ 
@ Params: r0=const u16* src_ptr; r1=u16* dst_ptr; r2=u32 packed_count (bits[15:0]=pixel_count [0..0xffff])
@ Return: r0=u16* dst_end_ptr (Sub-case E passthrough)
scale_pixel_brightness_in_buffer:
    push {r4,r5,r6,r7,lr}                    @ 080ddad8 f0b5
    .hword 0x4657    @ 080ddada 5746
    .hword 0x464e    @ 080ddadc 4e46
    .hword 0x4645    @ 080ddade 4546
    push {r5,r6,r7}                          @ 080ddae0 e0b4
    sub sp,#0xc                              @ 080ddae2 83b0
    adds r6,r0,#0x0    @ 080ddae4 061c
    .hword 0x4689    @ 080ddae6 8946
    lsls r0,r2,#0x10    @ 080ddae8 1004
    lsrs r7,r0,#0x10    @ 080ddaea 070c
    lsrs r2,r2,#0x10    @ 080ddaec 120c
    .hword 0x4692    @ 080ddaee 9246
    movs r0,#0x80    @ 080ddaf0 8020
    lsls r0,r0,#0x1    @ 080ddaf2 4000
    .hword 0x4680    @ 080ddaf4 8046
    adds r5,r6,#0x0    @ 080ddaf6 351c
    cmp r7,#0x0                              @ 080ddaf8 002f
    beq LAB_080ddb1a                         @ 080ddafa 0ed0
    adds r4,r7,#0x0    @ 080ddafc 3c1c
LAB_080ddafe:
    ldrh r0,[r5,#0x0]                        @ 080ddafe 2888
    .hword 0x4669    @ 080ddb00 6946
    add r2,sp,#0x4                           @ 080ddb02 01aa
    add r3,sp,#0x8                           @ 080ddb04 02ab
    bl decode_overlay_color_channels         @ 080ddb06 fff7d5fe
    ldr r0,[sp,#0x4]                         @ 080ddb0a 0198
    cmp r0,r8                                @ 080ddb0c 4045
    bge LAB_080ddb12                         @ 080ddb0e 00da
    .hword 0x4680    @ 080ddb10 8046
LAB_080ddb12:
    adds r5,#0x2    @ 080ddb12 0235
    subs r4,#0x1    @ 080ddb14 013c
    cmp r4,#0x0                              @ 080ddb16 002c
    bne LAB_080ddafe                         @ 080ddb18 f1d1
LAB_080ddb1a:
    .hword 0x4651    @ 080ddb1a 5146
    .hword 0x4640    @ 080ddb1c 4046
    muls r0,r1    @ 080ddb1e 4843
    asrs r5,r0,#0x8    @ 080ddb20 0512
    cmp r7,#0x0                              @ 080ddb22 002f
    beq LAB_080ddb52                         @ 080ddb24 15d0
    adds r4,r7,#0x0    @ 080ddb26 3c1c
LAB_080ddb28:
    ldrh r0,[r6,#0x0]                        @ 080ddb28 3088
    .hword 0x4669    @ 080ddb2a 6946
    add r2,sp,#0x4                           @ 080ddb2c 01aa
    add r3,sp,#0x8                           @ 080ddb2e 02ab
    bl decode_overlay_color_channels         @ 080ddb30 fff7c0fe
    ldr r1,[sp,#0x4]                         @ 080ddb34 0199
    subs r1,r1,r5    @ 080ddb36 491b
    str r1,[sp,#0x4]                         @ 080ddb38 0191
    ldr r0,[sp,#0x0]                         @ 080ddb3a 0098
    ldr r2,[sp,#0x8]                         @ 080ddb3c 029a
    bl convert_hsv_to_gba_rgb555             @ 080ddb3e fff71fff
    .hword 0x4649    @ 080ddb42 4946
    strh r0,[r1,#0x0]                        @ 080ddb44 0880
    adds r6,#0x2    @ 080ddb46 0236
    movs r0,#0x2    @ 080ddb48 0220
    add r9,r0                                @ 080ddb4a 8144
    subs r4,#0x1    @ 080ddb4c 013c
    cmp r4,#0x0                              @ 080ddb4e 002c
    bne LAB_080ddb28                         @ 080ddb50 ead1
LAB_080ddb52:
    add sp,#0xc                              @ 080ddb52 03b0
    pop {r3,r4,r5}                           @ 080ddb54 38bc
    .hword 0x4698    @ 080ddb56 9846
    .hword 0x46a1    @ 080ddb58 a146
    .hword 0x46aa    @ 080ddb5a aa46
    pop {r4,r5,r6,r7}                        @ 080ddb5c f0bc
    pop {r0}                                 @ 080ddb5e 01bc
    bx r0                                    @ 080ddb60 0047
    .zero  0x2

@ Per-pixel saturation processing variant. Part of HSV processing trio with rotate_pixel_hue_in_buffer and scale_pixel_brightness_in_buffer. Operates on the saturation channel: decodes each source pixel, adjusts saturation parameter, converts back to GBA RGB555 and writes to dst. Called by FUN_080dbebc (pack scene palette path) during cover HSV saturation adjustment.
@ 
@ Constants:
@ SAT_FULL = 0x100
@ 
@ Params: r0=const u16* src_ptr; r1=u16* dst_ptr; r2=u32 packed_count (bits[15:0]=pixel_count [0..0xffff])
@ Return: r0=u16* dst_end_ptr (Sub-case E passthrough)
scale_pixel_saturation_in_buffer:
    push {r4,r5,r6,r7,lr}                    @ 080ddb64 f0b5
    .hword 0x4657    @ 080ddb66 5746
    .hword 0x464e    @ 080ddb68 4e46
    .hword 0x4645    @ 080ddb6a 4546
    push {r5,r6,r7}                          @ 080ddb6c e0b4
    sub sp,#0xc                              @ 080ddb6e 83b0
    adds r6,r0,#0x0    @ 080ddb70 061c
    .hword 0x4689    @ 080ddb72 8946
    lsls r0,r2,#0x10    @ 080ddb74 1004
    lsrs r7,r0,#0x10    @ 080ddb76 070c
    lsrs r2,r2,#0x10    @ 080ddb78 120c
    .hword 0x4692    @ 080ddb7a 9246
    movs r0,#0x80    @ 080ddb7c 8020
    lsls r0,r0,#0x1    @ 080ddb7e 4000
    .hword 0x4680    @ 080ddb80 8046
    adds r5,r6,#0x0    @ 080ddb82 351c
    cmp r7,#0x0                              @ 080ddb84 002f
    beq LAB_080ddba6                         @ 080ddb86 0ed0
    adds r4,r7,#0x0    @ 080ddb88 3c1c
LAB_080ddb8a:
    ldrh r0,[r5,#0x0]                        @ 080ddb8a 2888
    .hword 0x4669    @ 080ddb8c 6946
    add r2,sp,#0x4                           @ 080ddb8e 01aa
    add r3,sp,#0x8                           @ 080ddb90 02ab
    bl decode_overlay_color_channels         @ 080ddb92 fff78ffe
    ldr r0,[sp,#0x8]                         @ 080ddb96 0298
    cmp r0,r8                                @ 080ddb98 4045
    bge LAB_080ddb9e                         @ 080ddb9a 00da
    .hword 0x4680    @ 080ddb9c 8046
LAB_080ddb9e:
    adds r5,#0x2    @ 080ddb9e 0235
    subs r4,#0x1    @ 080ddba0 013c
    cmp r4,#0x0                              @ 080ddba2 002c
    bne LAB_080ddb8a                         @ 080ddba4 f1d1
LAB_080ddba6:
    .hword 0x4651    @ 080ddba6 5146
    .hword 0x4640    @ 080ddba8 4046
    muls r0,r1    @ 080ddbaa 4843
    asrs r5,r0,#0x8    @ 080ddbac 0512
    cmp r7,#0x0                              @ 080ddbae 002f
    beq LAB_080ddbde                         @ 080ddbb0 15d0
    adds r4,r7,#0x0    @ 080ddbb2 3c1c
LAB_080ddbb4:
    ldrh r0,[r6,#0x0]                        @ 080ddbb4 3088
    .hword 0x4669    @ 080ddbb6 6946
    add r2,sp,#0x4                           @ 080ddbb8 01aa
    add r3,sp,#0x8                           @ 080ddbba 02ab
    bl decode_overlay_color_channels         @ 080ddbbc fff77afe
    ldr r2,[sp,#0x8]                         @ 080ddbc0 029a
    subs r2,r2,r5    @ 080ddbc2 521b
    str r2,[sp,#0x8]                         @ 080ddbc4 0292
    ldr r0,[sp,#0x0]                         @ 080ddbc6 0098
    ldr r1,[sp,#0x4]                         @ 080ddbc8 0199
    bl convert_hsv_to_gba_rgb555             @ 080ddbca fff7d9fe
    .hword 0x4649    @ 080ddbce 4946
    strh r0,[r1,#0x0]                        @ 080ddbd0 0880
    adds r6,#0x2    @ 080ddbd2 0236
    movs r0,#0x2    @ 080ddbd4 0220
    add r9,r0                                @ 080ddbd6 8144
    subs r4,#0x1    @ 080ddbd8 013c
    cmp r4,#0x0                              @ 080ddbda 002c
    bne LAB_080ddbb4                         @ 080ddbdc ead1
LAB_080ddbde:
    add sp,#0xc                              @ 080ddbde 03b0
    pop {r3,r4,r5}                           @ 080ddbe0 38bc
    .hword 0x4698    @ 080ddbe2 9846
    .hword 0x46a1    @ 080ddbe4 a146
    .hword 0x46aa    @ 080ddbe6 aa46
    pop {r4,r5,r6,r7}                        @ 080ddbe8 f0bc
    pop {r0}                                 @ 080ddbea 01bc
    bx r0                                    @ 080ddbec 0047
    .zero  0x2

@ Single bx lr release no-op stub. Called by FUN_080ddbf8 (pack page dispatcher) when pack_slot state is 1 (not 0 or 2). Placeholder handler for pack page state machine; no side effects.
return_void_pack_page_stub_a:
    bx lr                                    @ 080ddbf0 7047
    .zero  0x2

@ Single bx lr release no-op stub. Called by FUN_080ddbf8 (pack page dispatcher) on second state check, condition symmetric to return_void_pack_page_stub_a. Another placeholder handler for pack page state machine; no side effects.
return_void_pack_page_stub_b:
    bx lr                                    @ 080ddbf4 7047
    .zero  0x2

@ Per-frame driver for the pack scene page state machine. r0=function_table_ptr (ROM function pointer table base, e.g. 0x09e49578/0x09e49588/0x09e49598 for exchange_dp/password pages).
@ Reads current page slot_index from gPrng+0x204 bits[7:6], looks up the step handler pointer; if non-null calls invoke_r0; on non-zero return marks step complete: increments slot_index and clears gPrng+0x204/0x206/0x207/0x208 state bits and pack_ui_state+0x8 bit1. If slot_index is 0 or 2 calls return_void_pack_page_stub_a/b to skip. Returns 0=step in progress, 1=null pointer (sequence end).
@ Constants: gPrng=0x03000040, SLOT_INDEX_BITS=bits[7:6] of gPrng+0x204, pack_ui_state=0x03005850.
@ Inputs: r0=ptr function_table_ptr. Returns: r0=u32 (0=in progress, 1=sequence ended).
@ Side effects: [gPrng+0x204/0x206/0x207/0x208] state bits cleared on step complete; [pack_ui_state+0x8] bit1 cleared.
tick_pack_page_step:
    push {r4,r5,r6,lr}                       @ 080ddbf8 70b5
    adds r6,r0,#0x0    @ 080ddbfa 061c
    ldr r0, PTR_gPrng_080ddca4               @ 080ddbfc 2948
    movs r1,#0x81    @ 080ddbfe 8121
    lsls r1,r1,#0x2    @ 080ddc00 8900
    adds r0,r0,r1    @ 080ddc02 4018
    ldrh r0,[r0,#0x0]                        @ 080ddc04 0088
    lsls r0,r0,#0x12    @ 080ddc06 8004
    lsrs r1,r0,#0x18    @ 080ddc08 010e
    lsls r0,r1,#0x2    @ 080ddc0a 8800
    adds r0,r0,r6    @ 080ddc0c 8019
    ldr r0,[r0,#0x0]                         @ 080ddc0e 0068
    cmp r0,#0x0                              @ 080ddc10 0028
    beq LAB_080ddcbc                         @ 080ddc12 53d0
    cmp r1,#0x0                              @ 080ddc14 0029
    beq LAB_080ddc20                         @ 080ddc16 03d0
    cmp r1,#0x2                              @ 080ddc18 0229
    beq LAB_080ddc20                         @ 080ddc1a 01d0
    bl return_void_pack_page_stub_a          @ 080ddc1c fff7e8ff
LAB_080ddc20:
    ldr r5, PTR_gPrng_080ddca4               @ 080ddc20 204d
    movs r2,#0x81    @ 080ddc22 8122
    lsls r2,r2,#0x2    @ 080ddc24 9200
    adds r4,r5,r2    @ 080ddc26 ac18
    ldrh r1,[r4,#0x0]                        @ 080ddc28 2188
    lsls r0,r1,#0x12    @ 080ddc2a 8804
    lsrs r0,r0,#0x18    @ 080ddc2c 000e
    lsls r0,r0,#0x2    @ 080ddc2e 8000
    adds r0,r0,r6    @ 080ddc30 8019
    ldr r0,[r0,#0x0]                         @ 080ddc32 0068
    bl invoke_r0                             @ 080ddc34 30f0c8fc
    cmp r0,#0x0                              @ 080ddc38 0028
    beq LAB_080ddc8e                         @ 080ddc3a 28d0
    ldrh r3,[r4,#0x0]                        @ 080ddc3c 2388
    lsls r1,r3,#0x12    @ 080ddc3e 9904
    lsrs r1,r1,#0x18    @ 080ddc40 090e
    adds r1,#0x1    @ 080ddc42 0131
    movs r0,#0xff    @ 080ddc44 ff20
    ands r1,r0    @ 080ddc46 0140
    lsls r1,r1,#0x6    @ 080ddc48 8901
    ldr r2, DAT_080ddca8                     @ 080ddc4a 174a
    adds r0,r2,#0x0    @ 080ddc4c 101c
    ands r0,r3    @ 080ddc4e 1840
    orrs r0,r1    @ 080ddc50 0843
    strh r0,[r4,#0x0]                        @ 080ddc52 2080
    ldr r0,[r4,#0x0]                         @ 080ddc54 2068
    ldr r1, DAT_080ddcac                     @ 080ddc56 1549
    ands r0,r1    @ 080ddc58 0840
    str r0,[r4,#0x0]                         @ 080ddc5a 2060
    ldr r1, DAT_080ddcb0                     @ 080ddc5c 1449
    adds r0,r5,r1    @ 080ddc5e 6818
    ldrh r1,[r0,#0x0]                        @ 080ddc60 0188
    ands r2,r1    @ 080ddc62 0a40
    strh r2,[r0,#0x0]                        @ 080ddc64 0280
    ldr r2, DAT_080ddcb4                     @ 080ddc66 134a
    adds r1,r5,r2    @ 080ddc68 a918
    movs r0,#0x3f    @ 080ddc6a 3f20
    ldrb r2,[r1,#0x0]                        @ 080ddc6c 0a78
    ands r0,r2    @ 080ddc6e 1040
    strb r0,[r1,#0x0]                        @ 080ddc70 0870
    movs r0,#0x82    @ 080ddc72 8220
    lsls r0,r0,#0x2    @ 080ddc74 8000
    adds r1,r5,r0    @ 080ddc76 2918
    movs r0,#0x40    @ 080ddc78 4020
    rsbs r0,r0,#0    @ 080ddc7a 4042
    ldrb r2,[r1,#0x0]                        @ 080ddc7c 0a78
    ands r0,r2    @ 080ddc7e 1040
    strb r0,[r1,#0x0]                        @ 080ddc80 0870
    ldr r1, DAT_080ddcb8                     @ 080ddc82 0d49
    movs r0,#0x2    @ 080ddc84 0220
    rsbs r0,r0,#0    @ 080ddc86 4042
    ldrb r2,[r1,#0x8]                        @ 080ddc88 0a7a
    ands r0,r2    @ 080ddc8a 1040
    strb r0,[r1,#0x8]                        @ 080ddc8c 0872
LAB_080ddc8e:
    ldrh r4,[r4,#0x0]                        @ 080ddc8e 2488
    lsls r0,r4,#0x12    @ 080ddc90 a004
    lsrs r0,r0,#0x18    @ 080ddc92 000e
    cmp r0,#0x0                              @ 080ddc94 0028
    beq LAB_080ddca0                         @ 080ddc96 03d0
    cmp r0,#0x2                              @ 080ddc98 0228
    beq LAB_080ddca0                         @ 080ddc9a 01d0
    bl return_void_pack_page_stub_b          @ 080ddc9c fff7aaff
LAB_080ddca0:
    movs r0,#0x0    @ 080ddca0 0020
    b LAB_080ddcbe                           @ 080ddca2 0ce0
PTR_gPrng_080ddca4:
    .word  gPrng                          @ 080ddca4 40000003
DAT_080ddca8:
    .word  0xffffc03f                     @ 080ddca8 3fc0ffff
DAT_080ddcac:
    .word  0xffc03fff                     @ 080ddcac ff3fc0ff
DAT_080ddcb0:
    .word  0x00000206                     @ 080ddcb0 06020000
DAT_080ddcb4:
    .word  0x00000207                     @ 080ddcb4 07020000
DAT_080ddcb8:
    .word  pack_ui_state                  @ 080ddcb8 50580003
LAB_080ddcbc:
    movs r0,#0x1    @ 080ddcbc 0120
LAB_080ddcbe:
    pop {r4,r5,r6}                           @ 080ddcbe 70bc
    pop {r1}                                 @ 080ddcc0 02bc
    bx r1                                    @ 080ddcc2 0847

@ Pack scene full initialization. Zero-fills pack_ui_state+0xc for 0x1ca halfwords (bios_cpu_set fill mode), calls reset_display_and_obj_vram, calls reset_pack_scene_display, calls store_ewram_ctx_ptr_and_clear_mode_flags(0x0200af20) to bind EWRAM context and clear mode flags, writes gPrng+0x174=0x1001 to initialize PRNG-linked field, clears pack_ui_state bit range. Returns 1 on completion. Called by FUN_080ddd1c and FUN_080ddd3c (pack scene entry/reset paths).
@ 
@ Constants:
@ ZERO_RANGE_COUNT = 0x1ca
@ EWRAM_CTX_PTR   = 0x0200af20
@ PRNG_INIT_OFF   = 0x174
@ PRNG_INIT_VAL   = 0x1001
@ 
@ Params: r0=void
@ Return: r0=1 (fixed success flag; Sub-case E: pop {r4}; pop {r1}; bx r1)
init_pack_scene_full_state:
    push {r4,lr}                             @ 080ddcc4 10b5
    ldr r4, DAT_080ddd08                     @ 080ddcc6 104c
    movs r1,#0xe5    @ 080ddcc8 e521
    lsls r1,r1,#0x3    @ 080ddcca c900
    adds r0,r4,#0x0    @ 080ddccc 201c
    bl zero_fill_halfword_wrapper            @ 080ddcce 17f0e3f8
    ldr r0, DAT_080ddd0c                     @ 080ddcd2 0e48
    bl reset_display_and_obj_vram            @ 080ddcd4 19f0cefc
    bl reset_pack_scene_display              @ 080ddcd8 fff736fd
    ldr r0, DAT_080ddd10                     @ 080ddcdc 0c48
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 080ddcde 16f0dffa
    ldr r0, PTR_gPrng_080ddd14               @ 080ddce2 0c48
    movs r1,#0xba    @ 080ddce4 ba21
    lsls r1,r1,#0x1    @ 080ddce6 4900
    adds r0,r0,r1    @ 080ddce8 4018
    movs r2,#0x0    @ 080ddcea 0022
    ldr r1, DAT_080ddd18                     @ 080ddcec 0a49
    strh r1,[r0,#0x0]                        @ 080ddcee 0180
    strh r2,[r4,#0x2]                        @ 080ddcf0 6280
    strh r2,[r4,#0x4]                        @ 080ddcf2 a280
    movs r0,#0x3    @ 080ddcf4 0320
    rsbs r0,r0,#0    @ 080ddcf6 4042
    ldrb r1,[r4,#0x8]                        @ 080ddcf8 217a
    ands r0,r1    @ 080ddcfa 0840
    strb r0,[r4,#0x8]                        @ 080ddcfc 2072
    movs r0,#0x1    @ 080ddcfe 0120
    pop {r4}                                 @ 080ddd00 10bc
    pop {r1}                                 @ 080ddd02 02bc
    bx r1                                    @ 080ddd04 0847
    .zero  0x2
DAT_080ddd08:
    .word  pack_ui_state                  @ 080ddd08 50580003
DAT_080ddd0c:
    .word  0x02035fb0                     @ 080ddd0c b05f0302
DAT_080ddd10:
    .word  0x0200af20                     @ 080ddd10 20af0002
PTR_gPrng_080ddd14:
    .word  gPrng                          @ 080ddd14 40000003
DAT_080ddd18:
    .word  0x00001001                     @ 080ddd18 01100000

@ Init entry to enter the pack scene from the card pack list. Calls init_pack_scene_full_state to perform a full pack_ui_state zero-clear, VRAM reset, EWRAM bind, and PRNG init. Then writes pack_ui_state+0x2 (next-state field) := 1 (enter list page state) and sets pack_ui_state+0x8 bit1 (mode flag). Returns fixed 1 to notify the state machine that the step is complete. Forms a symmetric sibling with enter_pack_scene_from_shop (0x080ddd3c); the difference is the next-state value and mode bit semantics.
enter_pack_scene_from_list:
    push {r4,lr}                             @ 080ddd1c 10b5
    ldr r4, DAT_080ddd38                     @ 080ddd1e 064c
    bl init_pack_scene_full_state            @ 080ddd20 fff7d0ff
    movs r0,#0x1    @ 080ddd24 0120
    strh r0,[r4,#0x2]                        @ 080ddd26 6080
    movs r0,#0x2    @ 080ddd28 0220
    ldrb r1,[r4,#0x8]                        @ 080ddd2a 217a
    orrs r0,r1    @ 080ddd2c 0843
    strb r0,[r4,#0x8]                        @ 080ddd2e 2072
    movs r0,#0x1    @ 080ddd30 0120
    pop {r4}                                 @ 080ddd32 10bc
    pop {r1}                                 @ 080ddd34 02bc
    bx r1                                    @ 080ddd36 0847
DAT_080ddd38:
    .word  pack_ui_state                  @ 080ddd38 50580003

@ Init entry to enter the pack scene from the card shop. Forms a symmetric sibling with enter_pack_scene_from_list (0x080ddd1c); both call init_pack_scene_full_state for a full scene init. After init, writes pack_ui_state+0x2 := 2 (enter shop/purchase page state) and sets pack_ui_state+0x8 bit1. Returns fixed 1. The two entry points differ only in the next-state value: from_list writes NEXT_STATE=1; from_shop writes NEXT_STATE=2.
enter_pack_scene_from_shop:
    push {r4,lr}                             @ 080ddd3c 10b5
    ldr r4, DAT_080ddd58                     @ 080ddd3e 064c
    bl init_pack_scene_full_state            @ 080ddd40 fff7c0ff
    movs r0,#0x2    @ 080ddd44 0220
    strh r0,[r4,#0x2]                        @ 080ddd46 6080
    ldrb r1,[r4,#0x8]                        @ 080ddd48 217a
    orrs r0,r1    @ 080ddd4a 0843
    strb r0,[r4,#0x8]                        @ 080ddd4c 2072
    movs r0,#0x1    @ 080ddd4e 0120
    pop {r4}                                 @ 080ddd50 10bc
    pop {r1}                                 @ 080ddd52 02bc
    bx r1                                    @ 080ddd54 0847
    .zero  0x2
DAT_080ddd58:
    .word  pack_ui_state                  @ 080ddd58 50580003

@ Pack scene page state machine main dispatch function. callgraph indeg=0 (grep ".word 0x080ddd5d" 0 hits).
@ Reads current page step index [0..3] from pack_ui_state+0x2; dispatches to step handler via ROM function pointer table 0x09e495a8 (4 entries) through invoke_r0; if pointer is null returns 1. On step return==1 (step complete): clears pack_ui_state+0x4, checks pack_ui_state+0x8 bit1; if set writes terminal index 3 to pack_ui_state+0x2 and 3 to pack_ui_state+0x6 (history); else restores pack_ui_state+0x2 from pack_ui_state+0x6. Reads back [+0x2]; returns 1 if ==3, else 0.
@ Constants: pack_ui_state=0x03005850, FUNC_TABLE=0x09e495a8, TERMINAL_STATE=3.
@ Inputs: void (r0 overwritten by ldr r4, DAT at entry). Returns: r0=u32 (1=page sequence complete/step==3, 0=in progress).
@ Side effects: [pack_ui_state+0x2]: new step index written; [pack_ui_state+0x4]:=0 on step complete; [pack_ui_state+0x6]: 3 written on terminal.
dispatch_pack_page_state:
    push {r4,lr}                             @ 080ddd5c 10b5
    ldr r4, DAT_080ddd8c                     @ 080ddd5e 0b4c
    ldr r1, DAT_080ddd90                     @ 080ddd60 0b49
    ldrh r2,[r4,#0x2]                        @ 080ddd62 6288
    lsls r0,r2,#0x2    @ 080ddd64 9000
    adds r0,r0,r1    @ 080ddd66 4018
    ldr r0,[r0,#0x0]                         @ 080ddd68 0068
    cmp r0,#0x0                              @ 080ddd6a 0028
    beq LAB_080ddda6                         @ 080ddd6c 1bd0
    bl invoke_r0                             @ 080ddd6e 30f02bfc
    cmp r0,#0x1                              @ 080ddd72 0128
    bne LAB_080ddd9c                         @ 080ddd74 12d1
    movs r0,#0x0    @ 080ddd76 0020
    strh r0,[r4,#0x4]                        @ 080ddd78 a080
    movs r0,#0x2    @ 080ddd7a 0220
    ldrb r1,[r4,#0x8]                        @ 080ddd7c 217a
    ands r0,r1    @ 080ddd7e 0840
    cmp r0,#0x0                              @ 080ddd80 0028
    beq LAB_080ddd94                         @ 080ddd82 07d0
    movs r0,#0x3    @ 080ddd84 0320
    strh r0,[r4,#0x2]                        @ 080ddd86 6080
    b LAB_080ddd9a                           @ 080ddd88 07e0
    .zero  0x2
DAT_080ddd8c:
    .word  pack_ui_state                  @ 080ddd8c 50580003
DAT_080ddd90:
    .word  0x09e495a8                     @ 080ddd90 a895e409
LAB_080ddd94:
    ldrh r0,[r4,#0x6]                        @ 080ddd94 e088
    strh r0,[r4,#0x2]                        @ 080ddd96 6080
    movs r0,#0x3    @ 080ddd98 0320
LAB_080ddd9a:
    strh r0,[r4,#0x6]                        @ 080ddd9a e080
LAB_080ddd9c:
    ldrh r4,[r4,#0x2]                        @ 080ddd9c 6488
    cmp r4,#0x3                              @ 080ddd9e 032c
    beq LAB_080ddda6                         @ 080ddda0 01d0
    movs r0,#0x0    @ 080ddda2 0020
    b LAB_080ddda8                           @ 080ddda4 00e0
LAB_080ddda6:
    movs r0,#0x1    @ 080ddda6 0120
LAB_080ddda8:
    pop {r4}                                 @ 080ddda8 10bc
    pop {r1}                                 @ 080dddaa 02bc
    bx r1                                    @ 080dddac 0847
    .byte  0x00, 0x00, 0x01, 0x20, 0x70, 0x47

@ Single-line trampoline: loads function pointer from ROM address 0x09e49578, forwards to tick_pack_page_step. Body is very short (ldr + bl + return), decoupling ROM function table from tick_pack_page_step call site. indeg=0, no callgraph caller; dead code or fn-ptr table entry. No parameters, no independent return value (Sub-case E: pop {r1}; bx r1, r0 passthrough of tick_pack_page_step return).
@ 
@ Constants:
@ ROM_FN_PTR = 0x09e49578
@ 
@ Params: r0=void (internal ldr at 080dddb6 sets r0=0x09e49578; caller passes nothing)
@ Return: r0=tick_pack_page_step return value (Sub-case E passthrough)
invoke_pack_page_step_from_rom_ptr:
    push {lr}                                @ 080dddb4 00b5
    ldr r0, DWORD_080dddc0                   @ 080dddb6 0248
    bl tick_pack_page_step                   @ 080dddb8 fff71eff
    pop {r1}                                 @ 080dddbc 02bc
    bx r1                                    @ 080dddbe 0847
DWORD_080dddc0:
    .word  0x09e49578                     @ 080dddc0 7895e409
enter_exchange_dp_page:
    push {lr}                                @ 080dddc4 00b5
    ldr r0, DWORD_080dddd0                   @ 080dddc6 0248
    bl tick_pack_page_step                   @ 080dddc8 fff716ff
    pop {r1}                                 @ 080dddcc 02bc
    bx r1                                    @ 080dddce 0847
DWORD_080dddd0:
    .word  0x09e49588                     @ 080dddd0 8895e409
enter_password_input_page:
    push {lr}                                @ 080dddd4 00b5
    ldr r0, DWORD_080ddde0                   @ 080dddd6 0248
    bl tick_pack_page_step                   @ 080dddd8 fff70eff
    pop {r1}                                 @ 080ddddc 02bc
    bx r1                                    @ 080dddde 0847
DWORD_080ddde0:
    .word  0x09e49598                     @ 080ddde0 9895e409
    ROM_INCBIN 0xddde4, 0x70
    lsls r0,r0,#0x2    @ 080dde54 8000
    lsls r1,r1,#0x1f    @ 080dde56 c907
    lsrs r1,r1,#0x1f    @ 080dde58 c90f
    lsls r1,r1,#0x3    @ 080dde5a c900
    adds r0,r0,r1    @ 080dde5c 4018
    adds r0,r0,r3    @ 080dde5e c018
    ldr r0,[r0,#0x0]                         @ 080dde60 0068
    str r0,[r2,#0x4]                         @ 080dde62 5060
    ldr r4, DAT_080ddec0                     @ 080dde64 164c
    ldr r0, DAT_080ddec4                     @ 080dde66 1748
    ldr r3,[r0,#0x0]                         @ 080dde68 0368
    movs r0,#0x20    @ 080dde6a 2020
    movs r1,#0x10    @ 080dde6c 1021
    adds r2,r4,#0x0    @ 080dde6e 221c
    bl text_render_wrapper                   @ 080dde70 14f004fe
    ldr r0, DAT_080ddec8                     @ 080dde74 1448
    ldr r3,[r0,#0x0]                         @ 080dde76 0368
    movs r0,#0x20    @ 080dde78 2020
    movs r1,#0x20    @ 080dde7a 2021
    adds r2,r4,#0x0    @ 080dde7c 221c
    bl text_render_wrapper                   @ 080dde7e 14f0fdfd
    movs r0,#0xc0    @ 080dde82 c020
    lsls r0,r0,#0x13    @ 080dde84 c004
    movs r1,#0x0    @ 080dde86 0021
    bl write_line_buf_to_bg_tile_vram        @ 080dde88 15f0a4fc
    ldr r1, DAT_080ddecc                     @ 080dde8c 0f49
    movs r0,#0x0    @ 080dde8e 0020
    ldr r2, DAT_080dded0                     @ 080dde90 0f4a
LAB_080dde92:
    strh r0,[r1,#0x0]                        @ 080dde92 0880
    adds r0,#0x1    @ 080dde94 0130
    adds r1,#0x2    @ 080dde96 0231
    cmp r0,r2                                @ 080dde98 9042
    bls LAB_080dde92                         @ 080dde9a fad9
    movs r0,#0xa0    @ 080dde9c a020
    lsls r0,r0,#0x13    @ 080dde9e c004
    ldr r1, DAT_080dded4                     @ 080ddea0 0c49
    movs r2,#0x20    @ 080ddea2 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080ddea4 17f030f8
    bl apply_blend_fadeout_flat              @ 080ddea8 17f092fc
    movs r0,#0x1    @ 080ddeac 0120
    pop {r4}                                 @ 080ddeae 10bc
    pop {r1}                                 @ 080ddeb0 02bc
    bx r1                                    @ 080ddeb2 0847
    .word  BG0CNT                         @ 080ddeb4 08000004
    .word  0x02006ed0                     @ 080ddeb8 d06e0002
    .word  font_jp_base_table             @ 080ddebc 54f8e509
DAT_080ddec0:
    .word  0x00000107                     @ 080ddec0 07010000
DAT_080ddec4:
    .word  0x09e5e618                     @ 080ddec4 18e6e509
DAT_080ddec8:
    .word  0x09e5e61c                     @ 080ddec8 1ce6e509
DAT_080ddecc:
    .word  0x0600e000                     @ 080ddecc 00e00006
DAT_080dded0:
    .word  0x000003ff                     @ 080dded0 ff030000
DAT_080dded4:
    .word  0x09ccd290                     @ 080dded4 90d2cc09

@ Pack exchange/password page state machine step 2: enable display layers and advance fadein by one frame. Writes 0x1100 to DISPCNT (0x04000000) to enable BG0+BG1+OBJ layers; calls tick_blend_step_by_delta(r0=4) to advance fadein; returns 1 when animation complete, 0 while in progress. Item 2 in ROM dispatch table 0x09e495d8.
@ 
@ Constants:
@ - DISPCNT=0x04000000: GBA display control register (0x80<<0x13)
@ - 0x1100: DISPCNT write value (BG0+BG1+OBJ enable; 0x88<<5=0x1100)
@ - 4: tick_blend_step_by_delta delta
tick_pack_exchange_fadein_step:
    push {lr}                                @ 080dded8 00b5
    movs r0,#0x80    @ 080ddeda 8020
    lsls r0,r0,#0x13    @ 080ddedc c004
    movs r1,#0x88    @ 080ddede 8821
    lsls r1,r1,#0x5    @ 080ddee0 4901
    strh r1,[r0,#0x0]                        @ 080ddee2 0180
    movs r0,#0x4    @ 080ddee4 0420
    bl tick_blend_step_by_delta              @ 080ddee6 17f0e7fc
    cmp r0,#0x1                              @ 080ddeea 0128
    beq LAB_080ddef2                         @ 080ddeec 01d0
    movs r0,#0x0    @ 080ddeee 0020
    b LAB_080ddef4                           @ 080ddef0 00e0
LAB_080ddef2:
    movs r0,#0x1    @ 080ddef2 0120
LAB_080ddef4:
    pop {r1}                                 @ 080ddef4 02bc
    bx r1                                    @ 080ddef6 0847

@ Pack exchange/password page state machine step 3: handle input and update selection cursor OAM. Reads gPrng+0x148 (key state field) bit7=0x80 -> A confirm, bit6=0x40 -> B cancel. A key: sets [pack_ui_state+0xc+0x2]=1 (selected); B key: clears to 0. Uses [+0x2] state (0/1) to choose cursor size (0x10/0x20 pixels) and calls write_oam_entry_from_packed_args to write cursor OAM. Re-reads gPrng+0x148: bit0=1 -> step complete (return 1); bit1=2 -> sets [+0x4] bit0 then return 1; else return 0. Item 3 in ROM dispatch table 0x09e495d8.
@ 
@ Constants:
@ - gPrng+0x148: input key state field (IWRAM)
@ - 0x80: A key pressed mask
@ - 0x40: B key pressed mask
@ - 0x10/0x20: cursor OAM height pixel values
tick_pack_exchange_input_step:
    push {r4,lr}                             @ 080ddef8 10b5
    ldr r0, DAT_080ddf34                     @ 080ddefa 0e48
    adds r4,r0,#0x0    @ 080ddefc 041c
    adds r4,#0xc    @ 080ddefe 0c34
    movs r1,#0x0    @ 080ddf00 0021
    ldr r0, PTR_gPrng_080ddf38               @ 080ddf02 0d48
    movs r3,#0xa4    @ 080ddf04 a423
    lsls r3,r3,#0x1    @ 080ddf06 5b00
    adds r2,r0,r3    @ 080ddf08 c218
    movs r0,#0x80    @ 080ddf0a 8020
    ldrh r3,[r2,#0x0]                        @ 080ddf0c 1388
    ands r0,r3    @ 080ddf0e 1840
    cmp r0,#0x0                              @ 080ddf10 0028
    beq LAB_080ddf18                         @ 080ddf12 01d0
    movs r0,#0x1    @ 080ddf14 0120
    strh r0,[r4,#0x2]                        @ 080ddf16 6080
LAB_080ddf18:
    movs r0,#0x40    @ 080ddf18 4020
    ldrh r2,[r2,#0x0]                        @ 080ddf1a 1288
    ands r0,r2    @ 080ddf1c 1040
    cmp r0,#0x0                              @ 080ddf1e 0028
    beq LAB_080ddf24                         @ 080ddf20 00d0
    strh r1,[r4,#0x2]                        @ 080ddf22 6180
LAB_080ddf24:
    ldrh r0,[r4,#0x2]                        @ 080ddf24 6088
    cmp r0,#0x0                              @ 080ddf26 0028
    beq LAB_080ddf2e                         @ 080ddf28 01d0
    cmp r0,#0x1                              @ 080ddf2a 0128
    beq LAB_080ddf3c                         @ 080ddf2c 06d0
LAB_080ddf2e:
    movs r1,#0x10    @ 080ddf2e 1021
    b LAB_080ddf3e                           @ 080ddf30 05e0
    .zero  0x2
DAT_080ddf34:
    .word  pack_ui_state                  @ 080ddf34 50580003
PTR_gPrng_080ddf38:
    .word  gPrng                          @ 080ddf38 40000003
LAB_080ddf3c:
    movs r1,#0x20    @ 080ddf3c 2021
LAB_080ddf3e:
    lsls r0,r1,#0x10    @ 080ddf3e 0804
    movs r1,#0x8    @ 080ddf40 0821
    orrs r0,r1    @ 080ddf42 0843
    movs r1,#0x0    @ 080ddf44 0021
    movs r2,#0x1    @ 080ddf46 0122
    bl write_oam_entry_from_packed_args      @ 080ddf48 18f010f9
    ldr r0, PTR_gPrng_080ddf6c               @ 080ddf4c 0748
    movs r1,#0xa4    @ 080ddf4e a421
    lsls r1,r1,#0x1    @ 080ddf50 4900
    adds r0,r0,r1    @ 080ddf52 4018
    ldrh r1,[r0,#0x0]                        @ 080ddf54 0188
    movs r0,#0x1    @ 080ddf56 0120
    ands r0,r1    @ 080ddf58 0840
    cmp r0,#0x0                              @ 080ddf5a 0028
    bne LAB_080ddf78                         @ 080ddf5c 0cd1
    movs r0,#0x2    @ 080ddf5e 0220
    ands r0,r1    @ 080ddf60 0840
    cmp r0,#0x0                              @ 080ddf62 0028
    bne LAB_080ddf70                         @ 080ddf64 04d1
    movs r0,#0x0    @ 080ddf66 0020
    b LAB_080ddf7a                           @ 080ddf68 07e0
    .zero  0x2
PTR_gPrng_080ddf6c:
    .word  gPrng                          @ 080ddf6c 40000003
LAB_080ddf70:
    movs r0,#0x1    @ 080ddf70 0120
    ldrb r3,[r4,#0x4]                        @ 080ddf72 2379
    orrs r0,r3    @ 080ddf74 1843
    strb r0,[r4,#0x4]                        @ 080ddf76 2071
LAB_080ddf78:
    movs r0,#0x1    @ 080ddf78 0120
LAB_080ddf7a:
    pop {r4}                                 @ 080ddf7a 10bc
    pop {r1}                                 @ 080ddf7c 02bc
    bx r1                                    @ 080ddf7e 0847

@ Pack exchange/password page state machine step 4: advance fadeout animation frame and clear DISPCNT when complete. Calls start_blend_fadein_with_target(r0=4) to advance fadeout; returns 1 when complete: writes DISPCNT=0 (turn off all display layers), returns 1; otherwise returns 0. Item 4 in ROM dispatch table 0x09e495d8.
@ 
@ Constants:
@ - 4: blend delta
@ - DISPCNT=0x04000000: GBA display control (0x80<<0x13)
tick_pack_exchange_fadeout_step:
    push {lr}                                @ 080ddf80 00b5
    movs r0,#0x4    @ 080ddf82 0420
    bl start_blend_fadein_with_target        @ 080ddf84 17f05cfc
    cmp r0,#0x1                              @ 080ddf88 0128
    beq LAB_080ddf90                         @ 080ddf8a 01d0
    movs r0,#0x0    @ 080ddf8c 0020
    b LAB_080ddf9a                           @ 080ddf8e 04e0
LAB_080ddf90:
    movs r1,#0x80    @ 080ddf90 8021
    lsls r1,r1,#0x13    @ 080ddf92 c904
    movs r0,#0x0    @ 080ddf94 0020
    strh r0,[r1,#0x0]                        @ 080ddf96 0880
    movs r0,#0x1    @ 080ddf98 0120
LAB_080ddf9a:
    pop {r1}                                 @ 080ddf9a 02bc
    bx r1                                    @ 080ddf9c 0847
    .zero  0x2

@ Pack exchange/password page state machine step 5: update pack_ui_state with selection result and signal completion. Reads [pack_ui_state+0xc+0x4] bit0 (B cancel flag); if set writes [pack_ui_state+0x6]=3 (cancel); otherwise checks [+0x2] select state: 0 -> [+0x6]=1 (skip); 1 -> [+0x6]=2 (confirm). Returns 1 (step complete, state machine exits). Item 5 in ROM dispatch table 0x09e495d8.
@ 
@ Constants:
@ - pack_ui_state=0x03005850: IWRAM pack state base
@ - [pack_ui_state+0xc+0x4] bit0: B cancel flag
@ - [pack_ui_state+0x6]: page result field (1=skip, 2=confirm, 3=cancel)
finalize_pack_exchange_page_state:
    push {r4,lr}                             @ 080ddfa0 10b5
    ldr r1, DAT_080ddfc0                     @ 080ddfa2 0749
    adds r2,r1,#0x0    @ 080ddfa4 0a1c
    adds r2,#0xc    @ 080ddfa6 0c32
    movs r3,#0x1    @ 080ddfa8 0123
    adds r0,r3,#0x0    @ 080ddfaa 181c
    ldrb r4,[r2,#0x4]                        @ 080ddfac 1479
    ands r0,r4    @ 080ddfae 2040
    cmp r0,#0x0                              @ 080ddfb0 0028
    bne LAB_080ddfcc                         @ 080ddfb2 0bd1
    ldrh r0,[r2,#0x2]                        @ 080ddfb4 5088
    cmp r0,#0x0                              @ 080ddfb6 0028
    beq LAB_080ddfc4                         @ 080ddfb8 04d0
    cmp r0,#0x1                              @ 080ddfba 0128
    beq LAB_080ddfc8                         @ 080ddfbc 04d0
    b LAB_080ddfd0                           @ 080ddfbe 07e0
DAT_080ddfc0:
    .word  pack_ui_state                  @ 080ddfc0 50580003
LAB_080ddfc4:
    strh r3,[r1,#0x6]                        @ 080ddfc4 cb80
    b LAB_080ddfd0                           @ 080ddfc6 03e0
LAB_080ddfc8:
    movs r0,#0x2    @ 080ddfc8 0220
    b LAB_080ddfce                           @ 080ddfca 00e0
LAB_080ddfcc:
    movs r0,#0x3    @ 080ddfcc 0320
LAB_080ddfce:
    strh r0,[r1,#0x6]                        @ 080ddfce c880
LAB_080ddfd0:
    movs r0,#0x1    @ 080ddfd0 0120
    pop {r4}                                 @ 080ddfd2 10bc
    pop {r1}                                 @ 080ddfd4 02bc
    bx r1                                    @ 080ddfd6 0847

@ Pack exchange/password page sub-state-machine dispatch. Called each frame by a step handler of the pack main state machine (0x080ddd5c via indirect table).
@ Reads sub-step index from pack_ui_state+0x4; dispatches via ROM function pointer table 0x09e495d8; returns 1 if pointer is null (sub-sequence complete). On non-zero return from step function increments pack_ui_state+0x4 sub-step index. Returns 0 if sub-sequence still in progress.
@ Constants: pack_ui_state=0x03005850, FUNC_TABLE=0x09e495d8.
@ Inputs: void (r0 overwritten by ldr at entry). Returns: r0=u32 (1=sub-sequence complete/null ptr, 0=in progress).
@ Side effects: [pack_ui_state+0x4]: sub-step index +1 on step complete.
dispatch_pack_exchange_substep:
    push {r4,lr}                             @ 080ddfd8 10b5
    ldr r1, DAT_080ddffc                     @ 080ddfda 0849
    ldr r4, DAT_080de000                     @ 080ddfdc 084c
    ldrh r2,[r4,#0x4]                        @ 080ddfde a288
    lsls r0,r2,#0x2    @ 080ddfe0 9000
    adds r0,r0,r1    @ 080ddfe2 4018
    ldr r0,[r0,#0x0]                         @ 080ddfe4 0068
    cmp r0,#0x0                              @ 080ddfe6 0028
    beq LAB_080de004                         @ 080ddfe8 0cd0
    bl invoke_r0                             @ 080ddfea 30f0edfa
    cmp r0,#0x0                              @ 080ddfee 0028
    beq LAB_080ddff8                         @ 080ddff0 02d0
    ldrh r0,[r4,#0x4]                        @ 080ddff2 a088
    adds r0,#0x1    @ 080ddff4 0130
    strh r0,[r4,#0x4]                        @ 080ddff6 a080
LAB_080ddff8:
    movs r0,#0x0    @ 080ddff8 0020
    b LAB_080de006                           @ 080ddffa 04e0
DAT_080ddffc:
    .word  0x09e495d8                     @ 080ddffc d895e409
DAT_080de000:
    .word  pack_ui_state                  @ 080de000 50580003
LAB_080de004:
    movs r0,#0x1    @ 080de004 0120
LAB_080de006:
    pop {r4}                                 @ 080de006 10bc
    pop {r1}                                 @ 080de008 02bc
    bx r1                                    @ 080de00a 0847

@ Copies pack palette data from ROM to BG palette VRAM for slot index 0/1/2. r0=slot_index, clamped to 2 if out of range. Computes target 0x05000200+slot*0x20, copies 32 bytes from ROM table 0x09cebf30 (pack palette per-slot entry) via DMA. Then copies 16 additional bytes from 0x09ccd292 to 0x05000202+slot*0x20. Called by pack scene init on slot 0/1/2 transitions.
@ 
@ Constants:
@ - 0x05000200: GBA BG palette area start (pack slot 0)
@ - 0x09cebf30: pack palette data table (ROM, 0x20 bytes per slot)
@ - 0x09ccd292: supplementary palette/attribute data (ROM, 0x10 bytes)
@ - 0x20: palette slot size (32 bytes = 16 colors)
load_pack_palette_by_slot:
    push {r4,lr}                             @ 080de00c 10b5
    adds r1,r0,#0x0    @ 080de00e 011c
    movs r4,#0x1    @ 080de010 0124
    cmp r1,#0x2                              @ 080de012 0229
    bls LAB_080de018                         @ 080de014 00d9
    movs r1,#0x2    @ 080de016 0221
LAB_080de018:
    cmp r1,#0x1                              @ 080de018 0129
    beq LAB_080de026                         @ 080de01a 04d0
    cmp r1,#0x1                              @ 080de01c 0129
    bcc LAB_080de02c                         @ 080de01e 05d3
    cmp r1,#0x2                              @ 080de020 0229
    beq LAB_080de02a                         @ 080de022 02d0
    b LAB_080de02c                           @ 080de024 02e0
LAB_080de026:
    movs r4,#0x2    @ 080de026 0224
    b LAB_080de02c                           @ 080de028 00e0
LAB_080de02a:
    movs r4,#0x3    @ 080de02a 0324
LAB_080de02c:
    lsls r4,r4,#0x5    @ 080de02c 6401
    ldr r0, DAT_080de054                     @ 080de02e 0948
    adds r0,r4,r0    @ 080de030 2018
    ldr r2, DAT_080de058                     @ 080de032 094a
    lsls r1,r1,#0x2    @ 080de034 8900
    adds r1,r1,r2    @ 080de036 8918
    ldr r1,[r1,#0x0]                         @ 080de038 0968
    movs r2,#0x20    @ 080de03a 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080de03c 16f064ff
    ldr r0, DAT_080de05c                     @ 080de040 0648
    adds r4,r4,r0    @ 080de042 2418
    ldr r1, DAT_080de060                     @ 080de044 0649
    adds r0,r4,#0x0    @ 080de046 201c
    movs r2,#0x10    @ 080de048 1022
    bl copy_memory_dma3_with_cpu_fallback    @ 080de04a 16f05dff
    pop {r4}                                 @ 080de04e 10bc
    pop {r0}                                 @ 080de050 01bc
    bx r0                                    @ 080de052 0047
DAT_080de054:
    .word  0x05000200                     @ 080de054 00020005
DAT_080de058:
    .word  0x09cebf30                     @ 080de058 30bfce09
DAT_080de05c:
    .word  0x05000202                     @ 080de05c 02020005
DAT_080de060:
    .word  0x09ccd292                     @ 080de060 92d2cc09

@ Encodes pack slot index (0-7) as packed OAM attr value.
@ r0 = slot_index [0..7], clamped to 7 if out of range.
@ Computes y-coord: slot_index << 0x14 + 0xe400000 -> extract high to screen y.
@ Computes x-coord: fixed base 0xc0<<0xe = 0x0300000.
@ Returns r0 = (x_attr << 16) | y_attr packed OAM attribute pair.
@ Called by multiple scene_pack render functions to determine OAM sprite x/y attrs.
@ 
@ Constants:
@ - 0x7: slot_index upper bound (clamp to 7)
@ - 0xe4<<0xe = 0x0390000: OAM y base offset
@ - 0xc0<<0xe = 0x0300000: OAM x base (fixed)
encode_pack_slot_oam_attr:
    cmp r0,#0x7                              @ 080de064 0728
    bls LAB_080de06a                         @ 080de066 00d9
    movs r0,#0x7    @ 080de068 0720
LAB_080de06a:
    lsls r0,r0,#0x14    @ 080de06a 0005
    movs r1,#0xe4    @ 080de06c e421
    lsls r1,r1,#0xe    @ 080de06e 8903
    adds r0,r0,r1    @ 080de070 4018
    lsrs r0,r0,#0x10    @ 080de072 000c
    movs r1,#0xc0    @ 080de074 c021
    lsls r1,r1,#0xe    @ 080de076 8903
    orrs r0,r1    @ 080de078 0843
    bx lr                                    @ 080de07a 7047

@ Maps pack card grid slot index (0..10, clamped at 10) to OAM screen pixel coordinates; returns packed word (low16=x, high16=y).
@ Biases input by +9, computes col=(input+9)%5 and row=(input+9 % 10)/5. x=col*24+0x22, y=row*0x1a+0x54.
@ Called by multiple pack scene OAM render paths to determine slot pixel position.
@ Constants: SLOT_INDEX_MAX=10, SLOT_BIAS=9, COL_MODULUS=5, ROW_DIVISOR=10, ROW_DIVISOR2=5, X_STEP=24, X_BASE=0x22=34, Y_STEP=0x1a=26, Y_BASE=0x54=84.
@ Inputs: r0=u8 slot_index [0..10]. Returns: r0=u32 packed_oam_xy (high16=y_pixel, low16=x_pixel).
@ Side effects: none (pure computation).
compute_pack_grid_slot_oam_xy:
    push {r4,r5,lr}                          @ 080de07c 30b5
    cmp r0,#0xa                              @ 080de07e 0a28
    bls LAB_080de084                         @ 080de080 00d9
    movs r0,#0xa    @ 080de082 0a20
LAB_080de084:
    adds r5,r0,#0x0    @ 080de084 051c
    adds r5,#0x9    @ 080de086 0935
    adds r0,r5,#0x0    @ 080de088 281c
    movs r1,#0x5    @ 080de08a 0521
    bl get_bios_div_remainder                @ 080de08c 30f0b8f9
    lsls r4,r0,#0x1    @ 080de090 4400
    adds r4,r4,r0    @ 080de092 2418
    lsls r4,r4,#0x3    @ 080de094 e400
    adds r4,#0x22    @ 080de096 2234
    adds r0,r5,#0x0    @ 080de098 281c
    movs r1,#0xa    @ 080de09a 0a21
    bl get_bios_div_remainder                @ 080de09c 30f0b0f9
    movs r1,#0x5    @ 080de0a0 0521
    bl bios_div                              @ 080de0a2 30f0abf9
    movs r1,#0x1a    @ 080de0a6 1a21
    muls r0,r1    @ 080de0a8 4843
    adds r0,#0x54    @ 080de0aa 5430
    lsls r4,r4,#0x10    @ 080de0ac 2404
    lsrs r4,r4,#0x10    @ 080de0ae 240c
    lsls r0,r0,#0x10    @ 080de0b0 0004
    orrs r4,r0    @ 080de0b2 0443
    adds r0,r4,#0x0    @ 080de0b4 201c
    pop {r4,r5}                              @ 080de0b6 30bc
    pop {r1}                                 @ 080de0b8 02bc
    bx r1                                    @ 080de0ba 0847

@ Encodes pack confirm state boolean as OAM attr packed value.
@ r0 = is_confirmed (0=no, nonzero=yes).
@ rsbs r1,r0,#0; orrs r1,r0 -> r1 = sign(r0) (r0!=0 -> 1); extract bit31 as [0..1] flag.
@ Computes: flag * 0x19 + 0x55 = target y position (0=0x55, 1=0x6e); python: 1*0x19+0x55=0x6e.
@ Returns r0 = (y_attr << 0x10) | 0xa3 (low 8 bits x attr).
@ Called by pack scene confirm button OAM render path.
@ 
@ Constants:
@ - 0x55: y base (is_confirmed=0, unselected position)
@ - 0x6e: y offset result (is_confirmed=1, 0x55+0x19=0x6e; python: hex(0x19+0x55)='0x6e')
@ - 0x19: y step factor (r1*2+r1=r1*3; *8=r1*24; +r1=r1*25=r1*0x19)
@ - 0xa3: OAM low 8-bit x attr (movs r1,#0xa3; orrs r0,r1 -> low 8 bits)
encode_pack_confirm_oam_attr:
    rsbs r1,r0,#0    @ 080de0bc 4142
    orrs r1,r0    @ 080de0be 0143
    lsrs r1,r1,#0x1f    @ 080de0c0 c90f
    lsls r0,r1,#0x1    @ 080de0c2 4800
    adds r0,r0,r1    @ 080de0c4 4018
    lsls r0,r0,#0x3    @ 080de0c6 c000
    adds r0,r0,r1    @ 080de0c8 4018
    adds r0,#0x55    @ 080de0ca 5530
    lsls r0,r0,#0x10    @ 080de0cc 0004
    movs r1,#0xa3    @ 080de0ce a321
    orrs r0,r1    @ 080de0d0 0843
    bx lr                                    @ 080de0d2 7047

@ Computes OAM attr0 y-coord field for a pack preview slot (r0=slot_index [0..2]).
@ Clamps index to 2 if out of range.
@ Formula: y = slot*5 << 4 + 8 = slot*80 + 8 (pixel y), return 32-bit packed value 0x920000 | y16.
@ Multiple pack card-slot draw functions call this with fixed constants 0/1/2.
@ 
@ Constants:
@ - SLOT_Y_STEP = 80 (per-slot y spacing)
@ - SLOT_Y_BASE = 8 (first slot y offset)
@ - OAM_ATTR_HIGH = 0x920000 (attr0/attr2 upper field: flip+size flags)
compute_pack_slot_oam_y_attr:
    adds r1,r0,#0x0    @ 080de0d4 011c
    cmp r1,#0x2                              @ 080de0d6 0229
    bls LAB_080de0dc                         @ 080de0d8 00d9
    movs r1,#0x2    @ 080de0da 0221
LAB_080de0dc:
    lsls r0,r1,#0x2    @ 080de0dc 8800
    adds r0,r0,r1    @ 080de0de 4018
    lsls r0,r0,#0x4    @ 080de0e0 0001
    adds r0,#0x8    @ 080de0e2 0830
    lsls r0,r0,#0x10    @ 080de0e4 0004
    lsrs r0,r0,#0x10    @ 080de0e6 000c
    movs r1,#0x92    @ 080de0e8 9221
    lsls r1,r1,#0x10    @ 080de0ea 0904
    orrs r0,r1    @ 080de0ec 0843
    bx lr                                    @ 080de0ee 7047

@ Computes pack slot OAM tile index and attr word from (r0=tile_x, r1=size_mode).
@ size_mode=3: appends 0x30000 (priority/palette flag); size_mode=2: returns fixed tile 0x20000.
@ Otherwise if tile_x==5 takes special path; else generates r1*5+r0+1 as tile index.
@ Used for multi-size pack display scene OAM config.
@ Callers typically read x/y from pack_ui_state animation sub-struct [+0] and [+2] signed shorts.
@ 
@ Constants:
@ - OAM_PRIO3_MASK = 0x30000 (size_mode=3 high flag)
@ - OAM_PRIO2_MASK = 0x20000 (size_mode=2 high flag)
@ - OAM_ALT_TILE_BASE = 0x10000 (tile_x==5 special path flag)
@ - TILE_X_SPECIAL = 5 (tile_x value triggering special path)
compute_pack_slot_oam_tile_attr:
    adds r2,r0,#0x0    @ 080de0f0 021c
    cmp r1,#0x3                              @ 080de0f2 0329
    bne LAB_080de100                         @ 080de0f4 04d1
    lsls r0,r2,#0x10    @ 080de0f6 1004
    lsrs r0,r0,#0x10    @ 080de0f8 000c
    movs r1,#0xc0    @ 080de0fa c021
    lsls r1,r1,#0xa    @ 080de0fc 8902
    b LAB_080de124                           @ 080de0fe 11e0
LAB_080de100:
    cmp r1,#0x2                              @ 080de100 0229
    bne LAB_080de10a                         @ 080de102 02d1
    movs r0,#0x80    @ 080de104 8020
    lsls r0,r0,#0xa    @ 080de106 8002
    b LAB_080de126                           @ 080de108 0de0
LAB_080de10a:
    cmp r2,#0x5                              @ 080de10a 052a
    beq LAB_080de11c                         @ 080de10c 06d0
    lsls r0,r1,#0x2    @ 080de10e 8800
    adds r0,r0,r1    @ 080de110 4018
    adds r0,r2,r0    @ 080de112 1018
    adds r0,#0x1    @ 080de114 0130
    lsls r0,r0,#0x10    @ 080de116 0004
    lsrs r0,r0,#0x10    @ 080de118 000c
    b LAB_080de126                           @ 080de11a 04e0
LAB_080de11c:
    lsls r0,r1,#0x10    @ 080de11c 0804
    lsrs r0,r0,#0x10    @ 080de11e 000c
    movs r1,#0x80    @ 080de120 8021
    lsls r1,r1,#0x9    @ 080de122 4902
LAB_080de124:
    orrs r0,r1    @ 080de124 0843
LAB_080de126:
    bx lr                                    @ 080de126 7047

@ Pack OAM attribute compute dispatcher. Input r0 is packed (high16=type_code, low16=slot_data); dispatches by type_code: 0=compute_pack_grid_slot_oam_xy (grid slot XY), 1=encode_pack_confirm_oam_attr (confirm button attr) minus 1, 2=fixed return 0x0091008f (specific OAM attr constant), 3=compute_pack_slot_oam_y_attr (slot Y attr) minus 1, other=return 0. Called by multiple pack scene OAM write functions when building pack slot OAM attributes.
@ 
@ Constants:
@ TYPE_GRID_XY      = 0
@ TYPE_CONFIRM_ATTR = 1
@ TYPE_FIXED_ATTR   = 2
@ TYPE_SLOT_Y_ATTR  = 3
@ FIXED_OAM_ATTR    = 0x0091008f
@ 
@ Params: r0=u32 packed_type_slot (bits[31:16]=type_code [0..3]; bits[15:0]=slot_data passed to callees)
@ Return: r0=u32 oam_attr (type0=XY packed; type1=confirm_attr-1; type2=0x0091008f; type3=y_attr-1; other=0; Sub-case E)
compute_pack_oam_attr_by_type:
    push {lr}                                @ 080de128 00b5
    lsrs r1,r0,#0x10    @ 080de12a 010c
    lsls r0,r0,#0x10    @ 080de12c 0004
    lsrs r0,r0,#0x10    @ 080de12e 000c
    cmp r1,#0x1                              @ 080de130 0129
    beq LAB_080de14a                         @ 080de132 0ad0
    cmp r1,#0x1                              @ 080de134 0129
    bcc LAB_080de144                         @ 080de136 05d3
    cmp r1,#0x2                              @ 080de138 0229
    beq LAB_080de150                         @ 080de13a 09d0
    cmp r1,#0x3                              @ 080de13c 0329
    beq LAB_080de158                         @ 080de13e 0bd0
    movs r0,#0x0    @ 080de140 0020
    b LAB_080de15e                           @ 080de142 0ce0
LAB_080de144:
    bl compute_pack_grid_slot_oam_xy         @ 080de144 fff79aff
    b LAB_080de15e                           @ 080de148 09e0
LAB_080de14a:
    bl encode_pack_confirm_oam_attr          @ 080de14a fff7b7ff
    b LAB_080de15c                           @ 080de14e 05e0
LAB_080de150:
    ldr r0, DAT_080de154                     @ 080de150 0048
    b LAB_080de15e                           @ 080de152 04e0
DAT_080de154:
    .word  0x0091008f                     @ 080de154 8f009100
LAB_080de158:
    bl compute_pack_slot_oam_y_attr          @ 080de158 fff7bcff
LAB_080de15c:
    subs r0,#0x1    @ 080de15c 0138
LAB_080de15e:
    pop {r1}                                 @ 080de15e 02bc
    bx r1                                    @ 080de160 0847
    .zero  0x2

@ Updates the OAM attribute pair for the selected pack slot in pack_ui_state (two tile attribute groups + coordinates). Reads current x/y coordinates from pack_ui_state+0xc+0x44 (OAM animation substructure), calls compute_pack_slot_oam_tile_attr to compute tile attributes, then calls compute_pack_oam_attr_by_type for type attributes; writes results to [+0x44+0x4]/[+0x44+0x6]/[+0x44+0x0]/[+0x44+0x2]. If r1==2, overwrites [+0x44+0x0] with 5 (special type override). Applies the same logic a second time to write [+0x44+0x8]/[+0x44+0xa], and writes fixed value 7 to [+0x44+0xc]/[+0x44+0xe]. Conditionally writes the high 16 bits of r6 to [+0x44+0x10]. Called by multiple pack scene OAM refresh paths.
update_pack_slot_oam_attr_pair:
    push {r4,r5,r6,r7,lr}                    @ 080de164 f0b5
    adds r5,r0,#0x0    @ 080de166 051c
    adds r4,r1,#0x0    @ 080de168 0c1c
    ldr r0, DAT_080de1c4                     @ 080de16a 1648
    adds r7,r0,#0x0    @ 080de16c 071c
    adds r7,#0x44    @ 080de16e 4437
    movs r1,#0x0    @ 080de170 0021
    ldrsh r0,[r7,r1]                         @ 080de172 785e
    movs r2,#0x2    @ 080de174 0222
    ldrsh r1,[r7,r2]                         @ 080de176 b95e
    bl compute_pack_slot_oam_tile_attr       @ 080de178 fff7baff
    adds r6,r0,#0x0    @ 080de17c 061c
    bl compute_pack_oam_attr_by_type         @ 080de17e fff7d3ff
    strh r0,[r7,#0x4]                        @ 080de182 b880
    lsrs r0,r0,#0x10    @ 080de184 000c
    strh r0,[r7,#0x6]                        @ 080de186 f880
    strh r5,[r7,#0x0]                        @ 080de188 3d80
    strh r4,[r7,#0x2]                        @ 080de18a 7c80
    lsls r4,r4,#0x10    @ 080de18c 2404
    asrs r4,r4,#0x10    @ 080de18e 2414
    cmp r4,#0x2                              @ 080de190 022c
    bne LAB_080de198                         @ 080de192 01d1
    movs r0,#0x5    @ 080de194 0520
    strh r0,[r7,#0x0]                        @ 080de196 3880
LAB_080de198:
    movs r1,#0x0    @ 080de198 0021
    ldrsh r0,[r7,r1]                         @ 080de19a 785e
    movs r2,#0x2    @ 080de19c 0222
    ldrsh r1,[r7,r2]                         @ 080de19e b95e
    bl compute_pack_slot_oam_tile_attr       @ 080de1a0 fff7a6ff
    adds r6,r0,#0x0    @ 080de1a4 061c
    bl compute_pack_oam_attr_by_type         @ 080de1a6 fff7bfff
    strh r0,[r7,#0x8]                        @ 080de1aa 3881
    lsrs r0,r0,#0x10    @ 080de1ac 000c
    strh r0,[r7,#0xa]                        @ 080de1ae 7881
    movs r0,#0x7    @ 080de1b0 0720
    strh r0,[r7,#0xc]                        @ 080de1b2 b881
    strh r0,[r7,#0xe]                        @ 080de1b4 f881
    lsrs r0,r6,#0x10    @ 080de1b6 300c
    cmp r0,#0x2                              @ 080de1b8 0228
    beq LAB_080de1be                         @ 080de1ba 00d0
    strh r0,[r7,#0x10]                       @ 080de1bc 3882
LAB_080de1be:
    pop {r4,r5,r6,r7}                        @ 080de1be f0bc
    pop {r0}                                 @ 080de1c0 01bc
    bx r0                                    @ 080de1c2 0047
DAT_080de1c4:
    .word  pack_ui_state                  @ 080de1c4 50580003

@ Per-frame countdown driver for a single pack slot animation frame. No APCS inputs.
@ Checks gPrng+0x148 bit0; if set, ORs pack_ui_state+0x140 bit3 (OAM update request flag).
@ Decrements pack_ui_state+0x52 (animation countdown); when countdown reaches 0: clears [+0x48..0x50] (5 OAM attr halfwords), recomputes tile attr via compute_pack_slot_oam_tile_attr and writes to [+0x54], sets r2=1. Returns r2 (0=countdown in progress, 1=countdown elapsed this frame).
@ Constants: pack_ui_state=0x03005850, gPrng=0x03000040, ANIM_STRUCT_OFFSET=0x44, COUNTDOWN_FIELD_OFFSET=0xe, KEY_STATE_OFFSET=0x148, OAM_REQUEST_OFFSET=0x140, OAM_REQUEST_BIT=0x8.
@ Inputs: void (r0 overwritten by ldr r3,DAT at entry). Returns: r0=u32 (0=countdown in progress, 1=countdown reached zero).
@ Side effects: [pack_ui_state+0x140] bit3 set conditionally; [pack_ui_state+0x52] decremented; [pack_ui_state+0x48..0x50]:=0 and [+0x54] recomputed on zero.
tick_pack_slot_anim_frame:
    push {r4,lr}                             @ 080de1c8 10b5
    ldr r3, DAT_080de224                     @ 080de1ca 164b
    adds r4,r3,#0x0    @ 080de1cc 1c1c
    adds r4,#0x44    @ 080de1ce 4434
    movs r2,#0x0    @ 080de1d0 0022
    ldr r1, PTR_gPrng_080de228               @ 080de1d2 1549
    movs r0,#0xa4    @ 080de1d4 a420
    lsls r0,r0,#0x1    @ 080de1d6 4000
    adds r1,r1,r0    @ 080de1d8 0918
    movs r0,#0x1    @ 080de1da 0120
    ldrh r1,[r1,#0x0]                        @ 080de1dc 0988
    ands r0,r1    @ 080de1de 0840
    cmp r0,#0x0                              @ 080de1e0 0028
    beq LAB_080de1f2                         @ 080de1e2 06d0
    movs r0,#0xa0    @ 080de1e4 a020
    lsls r0,r0,#0x1    @ 080de1e6 4000
    adds r1,r3,r0    @ 080de1e8 1918
    movs r0,#0x8    @ 080de1ea 0820
    ldrb r3,[r1,#0x0]                        @ 080de1ec 0b78
    orrs r0,r3    @ 080de1ee 1843
    strb r0,[r1,#0x0]                        @ 080de1f0 0870
LAB_080de1f2:
    ldrh r0,[r4,#0xe]                        @ 080de1f2 e089
    subs r0,#0x1    @ 080de1f4 0138
    strh r0,[r4,#0xe]                        @ 080de1f6 e081
    lsls r0,r0,#0x10    @ 080de1f8 0004
    cmp r0,#0x0                              @ 080de1fa 0028
    bne LAB_080de21a                         @ 080de1fc 0dd1
    strh r2,[r4,#0x4]                        @ 080de1fe a280
    strh r2,[r4,#0x6]                        @ 080de200 e280
    strh r2,[r4,#0x8]                        @ 080de202 2281
    strh r2,[r4,#0xa]                        @ 080de204 6281
    strh r2,[r4,#0xc]                        @ 080de206 a281
    movs r1,#0x0    @ 080de208 0021
    ldrsh r0,[r4,r1]                         @ 080de20a 605e
    movs r2,#0x2    @ 080de20c 0222
    ldrsh r1,[r4,r2]                         @ 080de20e a15e
    bl compute_pack_slot_oam_tile_attr       @ 080de210 fff76eff
    lsrs r0,r0,#0x10    @ 080de214 000c
    strh r0,[r4,#0x10]                       @ 080de216 2082
    movs r2,#0x1    @ 080de218 0122
LAB_080de21a:
    adds r0,r2,#0x0    @ 080de21a 101c
    pop {r4}                                 @ 080de21c 10bc
    pop {r1}                                 @ 080de21e 02bc
    bx r1                                    @ 080de220 0847
    .zero  0x2
DAT_080de224:
    .word  pack_ui_state                  @ 080de224 50580003
PTR_gPrng_080de228:
    .word  gPrng                          @ 080de228 40000003

@ Updates pack_ui_state OAM attribute sub-struct at offset 0x30 with new slot coordinates.
@ r0=slot_x (new column position, written to [+0x30]), r1=slot_y (new row position, written to [+0x32] via r8).
@ Reads old x/y from pack_ui_state+0x30, calls encode_pack_slot_oam_attr to encode OAM xy attr word, splits result into [+0x34]/[+0x36]; writes r0 to [+0x30] and r8 to [+0x32]; reads new x/y, calls encode_pack_slot_oam_attr again, writes to [+0x38]/[+0x3a]; writes fixed value 7 to [+0x3c] and [+0x3e].
@ Called by pack scene OAM render path to refresh slot OAM during animation.
@ Constants: pack_ui_state=0x03005850, SLOT_SUBSTRUCT_OFFSET=0x30, OAM_FIXED_ATTR=7.
@ Inputs: r0=s16 slot_x [1..7], r1=s16 slot_y [-32768..32767]. Returns: void (pop {r0}; bx r0).
@ Side effects: [pack_ui_state+0x30..0x3e]: x/y fields and OAM attr words updated.
update_pack_slot_oam_attrs:
    push {r4,r5,r6,lr}                       @ 080de22c 70b5
    .hword 0x4646    @ 080de22e 4646
    push {r6}                                @ 080de230 40b4
    adds r6,r0,#0x0    @ 080de232 061c
    .hword 0x4688    @ 080de234 8846
    ldr r5, DAT_080de278                     @ 080de236 104d
    adds r4,r5,#0x0    @ 080de238 2c1c
    adds r4,#0x30    @ 080de23a 3034
    movs r1,#0x30    @ 080de23c 3021
    ldrsh r0,[r5,r1]                         @ 080de23e 685e
    movs r2,#0x2    @ 080de240 0222
    ldrsh r1,[r4,r2]                         @ 080de242 a15e
    bl encode_pack_slot_oam_attr             @ 080de244 fff70eff
    strh r0,[r4,#0x4]                        @ 080de248 a080
    lsrs r0,r0,#0x10    @ 080de24a 000c
    strh r0,[r4,#0x6]                        @ 080de24c e080
    strh r6,[r5,#0x30]                       @ 080de24e 2e86
    .hword 0x4640    @ 080de250 4046
    strh r0,[r4,#0x2]                        @ 080de252 6080
    movs r1,#0x30    @ 080de254 3021
    ldrsh r0,[r5,r1]                         @ 080de256 685e
    movs r2,#0x2    @ 080de258 0222
    ldrsh r1,[r4,r2]                         @ 080de25a a15e
    bl encode_pack_slot_oam_attr             @ 080de25c fff702ff
    strh r0,[r4,#0x8]                        @ 080de260 2081
    lsrs r0,r0,#0x10    @ 080de262 000c
    strh r0,[r4,#0xa]                        @ 080de264 6081
    movs r0,#0x7    @ 080de266 0720
    strh r0,[r4,#0xc]                        @ 080de268 a081
    strh r0,[r4,#0xe]                        @ 080de26a e081
    pop {r3}                                 @ 080de26c 08bc
    .hword 0x4698    @ 080de26e 9846
    pop {r4,r5,r6}                           @ 080de270 70bc
    pop {r0}                                 @ 080de272 01bc
    bx r0                                    @ 080de274 0047
    .zero  0x2
DAT_080de278:
    .word  pack_ui_state                  @ 080de278 50580003

@ Huffman-decompresses two compressed GFX streams for the pack scene and DMA-copies palette to PAL RAM.
@ First ROM stream (0x09ceb930) decompressed to OBJ VRAM 0x06004020.
@ Second stream (0x09ceb938) decompressed to BG VRAM 0x0600e000.
@ Then reads 0x40 bytes palette from ROM 0x09ceb934 via copy_memory_dma3_with_cpu_fallback to PAL RAM 0x050001c0 (obj palette slots 28-31).
@ No parameters; called once by pack scene init path on scene entry.
@ 
@ Constants:
@ - ROM_GFX_A = 0x09ceb930 (OBJ tiles huffman compressed data pointer table entry)
@ - VRAM_OBJ_DST = 0x06004020 (OBJ VRAM decompress destination)
@ - ROM_GFX_B = 0x09ceb938 (BG tiles huffman compressed data pointer table entry)
@ - VRAM_BG_DST = 0x0600e000 (BG VRAM decompress destination)
@ - ROM_PAL = 0x09ceb934 (palette source address)
@ - PAL_DST = 0x050001c0 (PAL RAM destination)
@ - PAL_SIZE = 0x40 (bytes copied = 32 colors * 2 bytes)
decompress_pack_scene_gfx:
    push {lr}                                @ 080de27c 00b5
    ldr r0, DAT_080de2a4                     @ 080de27e 0948
    ldr r0,[r0,#0x0]                         @ 080de280 0068
    ldr r1, DAT_080de2a8                     @ 080de282 0949
    bl bios_huff_uncomp                      @ 080de284 30f0c8f8
    ldr r0, DAT_080de2ac                     @ 080de288 0848
    ldr r0,[r0,#0x0]                         @ 080de28a 0068
    ldr r1, DAT_080de2b0                     @ 080de28c 0849
    bl bios_huff_uncomp                      @ 080de28e 30f0c3f8
    ldr r0, DAT_080de2b4                     @ 080de292 0848
    ldr r1, DAT_080de2b8                     @ 080de294 0849
    ldr r1,[r1,#0x0]                         @ 080de296 0968
    movs r2,#0x40    @ 080de298 4022
    bl copy_memory_dma3_with_cpu_fallback    @ 080de29a 16f035fe
    pop {r0}                                 @ 080de29e 01bc
    bx r0                                    @ 080de2a0 0047
    .zero  0x2
DAT_080de2a4:
    .word  0x09ceb930                     @ 080de2a4 30b9ce09
DAT_080de2a8:
    .word  0x06004020                     @ 080de2a8 20400006
DAT_080de2ac:
    .word  0x09ceb938                     @ 080de2ac 38b9ce09
DAT_080de2b0:
    .word  0x0600e000                     @ 080de2b0 00e00006
DAT_080de2b4:
    .word  0x050001c0                     @ 080de2b4 c0010005
DAT_080de2b8:
    .word  0x09ceb934                     @ 080de2b8 34b9ce09

@ Renders current pack name text and price digits to OBJ VRAM / sprite line buffer.
@ Reads pack count from pack_ui_state (capped at 0x5f5e0ff), selects font via font_jp_base_table,
@ calls render_decimal_digits_jp for quantity, then render_text_with_u16_width for pack name string.
@ Calls zero_fill_halfword_wrapper to clear OAM tile region, commit_line_buffer_to_sprite_vram to commit.
@ Finally writes tile index sequence (10 slots x 2 rows) to OAM map region 0x0600f8e8.
@ Entry r0 is an offset (stored to r8 via .hword 0x4680); no other explicit APCS params.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (IWRAM pack scene state base)
@ - PACK_COUNT_OFFSET = 0x6c38 (pack count field offset within pack_ui_state)
@ - MAX_PACK_COUNT = 0x5f5e0ff (count clamp upper bound)
@ - OAM_TILE_BUF = 0x0600f8e8 (OAM tile map write region)
@ - STR_ID_PACK_NAME = 0x0000138f (pack name string ID)
render_pack_info_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080de2bc f0b5
    .hword 0x4647    @ 080de2be 4746
    push {r7}                                @ 080de2c0 80b4
    sub sp,#0x4                              @ 080de2c2 81b0
    ldr r1, DAT_080de3b8                     @ 080de2c4 3c49
    ldr r0, DAT_080de3bc                     @ 080de2c6 3d48
    .hword 0x4680    @ 080de2c8 8046
    ldr r0, DAT_080de3c0                     @ 080de2ca 3d48
    add r0,r8                                @ 080de2cc 4044
    ldr r4,[r0,#0x0]                         @ 080de2ce 0468
    ldr r0, DAT_080de3c4                     @ 080de2d0 3c48
    cmp r4,r0                                @ 080de2d2 8442
    bls LAB_080de2d8                         @ 080de2d4 00d9
    adds r4,r0,#0x0    @ 080de2d6 041c
LAB_080de2d8:
    movs r2,#0xc0    @ 080de2d8 c022
    lsls r2,r2,#0x13    @ 080de2da d204
    movs r3,#0x8a    @ 080de2dc 8a23
    lsls r3,r3,#0x1    @ 080de2de 5b00
    adds r0,r1,r3    @ 080de2e0 c818
    ldrh r1,[r0,#0x0]                        @ 080de2e2 0188
    lsls r0,r1,#0x5    @ 080de2e4 4801
    adds r2,r0,r2    @ 080de2e6 8218
    str r2,[sp,#0x0]                         @ 080de2e8 0092
    ldr r6, DAT_080de3c8                     @ 080de2ea 374e
    adds r7,r1,#0x0    @ 080de2ec 0f1c
    ldr r2, DAT_080de3cc                     @ 080de2ee 374a
    movs r0,#0x2    @ 080de2f0 0220
    rsbs r0,r0,#0    @ 080de2f2 4042
    ldrb r1,[r2,#0x15]                       @ 080de2f4 517d
    ands r0,r1    @ 080de2f6 0840
    strb r0,[r2,#0x15]                       @ 080de2f8 5075
    movs r1,#0x3    @ 080de2fa 0321
    rsbs r1,r1,#0    @ 080de2fc 4942
    ldrb r3,[r2,#0x8]                        @ 080de2fe 137a
    ands r1,r3    @ 080de300 1940
    strb r1,[r2,#0x8]                        @ 080de302 1172
    movs r0,#0x7d    @ 080de304 7d20
    rsbs r0,r0,#0    @ 080de306 4042
    ldrb r3,[r2,#0x14]                       @ 080de308 137d
    ands r0,r3    @ 080de30a 1840
    strb r0,[r2,#0x14]                       @ 080de30c 1075
    ldr r0, PTR_font_jp_base_table_080de3d0  @ 080de30e 3048
    lsls r1,r1,#0x1f    @ 080de310 c907
    lsrs r1,r1,#0x1f    @ 080de312 c90f
    lsls r1,r1,#0x3    @ 080de314 c900
    adds r1,r1,r0    @ 080de316 0918
    ldr r0,[r1,#0x0]                         @ 080de318 0868
    str r0,[r2,#0x4]                         @ 080de31a 5060
    movs r0,#0xa    @ 080de31c 0a20
    movs r1,#0x2    @ 080de31e 0221
    bl setup_line_buf_pos_and_font           @ 080de320 12f048fc
    ldr r5, DAT_080de3d4                     @ 080de324 2b4d
    movs r0,#0x32    @ 080de326 3220
    movs r1,#0x3    @ 080de328 0321
    adds r2,r5,#0x0    @ 080de32a 2a1c
    adds r3,r4,#0x0    @ 080de32c 231c
    bl render_decimal_digits_jp              @ 080de32e 14f0adfc
    movs r0,#0x32    @ 080de332 3220
    movs r1,#0x3    @ 080de334 0321
    movs r2,#0x7    @ 080de336 0722
    adds r3,r4,#0x0    @ 080de338 231c
    bl render_decimal_digits_jp              @ 080de33a 14f0a7fc
    ldr r0, DAT_080de3d8                     @ 080de33e 2648
    bl game_str_id_to_row                    @ 080de340 16f06afd
    ldr r2, PTR_game_str_pointer_table_080de3dc @ 080de344 254a
    lsls r0,r0,#0x10    @ 080de346 0004
    lsrs r0,r0,#0x10    @ 080de348 000c
    lsls r1,r0,#0x1    @ 080de34a 4100
    adds r1,r1,r0    @ 080de34c 0918
    lsls r1,r1,#0x1    @ 080de34e 4900
    ldr r0, DAT_080de3e0                     @ 080de350 2348
    add r0,r8                                @ 080de352 4044
    ldrb r0,[r0,#0x0]                        @ 080de354 0078
    lsls r0,r0,#0x1d    @ 080de356 4007
    lsrs r0,r0,#0x1d    @ 080de358 400f
    adds r1,r1,r0    @ 080de35a 0918
    lsls r1,r1,#0x2    @ 080de35c 8900
    adds r1,r1,r2    @ 080de35e 8918
    ldr r4,[r1,#0x0]                         @ 080de360 0c68
    ldr r0, PTR_game_str_ja_080de3e4         @ 080de362 2048
    adds r4,r4,r0    @ 080de364 2418
    movs r0,#0x38    @ 080de366 3820
    movs r1,#0x3    @ 080de368 0321
    adds r2,r5,#0x0    @ 080de36a 2a1c
    adds r3,r4,#0x0    @ 080de36c 231c
    bl render_text_with_u16_width            @ 080de36e 14f05dfc
    movs r0,#0x38    @ 080de372 3820
    movs r1,#0x3    @ 080de374 0321
    movs r2,#0x7    @ 080de376 0722
    adds r3,r4,#0x0    @ 080de378 231c
    bl render_text_with_u16_width            @ 080de37a 14f057fc
    movs r1,#0xa0    @ 080de37e a021
    lsls r1,r1,#0x2    @ 080de380 8900
    ldr r0,[sp,#0x0]                         @ 080de382 0098
    bl zero_fill_halfword_wrapper            @ 080de384 16f088fd
    ldr r0,[sp,#0x0]                         @ 080de388 0098
    movs r1,#0x0    @ 080de38a 0021
    bl commit_line_buffer_to_sprite_vram     @ 080de38c 14f05efd
    movs r1,#0x0    @ 080de390 0021
LAB_080de392:
    movs r0,#0x0    @ 080de392 0020
    adds r1,#0x1    @ 080de394 0131
LAB_080de396:
    strh r7,[r6,#0x0]                        @ 080de396 3780
    adds r7,#0x1    @ 080de398 0137
    adds r6,#0x2    @ 080de39a 0236
    adds r0,#0x1    @ 080de39c 0130
    cmp r0,#0x9                              @ 080de39e 0928
    bls LAB_080de396                         @ 080de3a0 f9d9
    adds r6,#0x2c    @ 080de3a2 2c36
    cmp r1,#0x1                              @ 080de3a4 0129
    bls LAB_080de392                         @ 080de3a6 f4d9
    movs r0,#0x14    @ 080de3a8 1420
    add sp,#0x4                              @ 080de3aa 01b0
    pop {r3}                                 @ 080de3ac 08bc
    .hword 0x4698    @ 080de3ae 9846
    pop {r4,r5,r6,r7}                        @ 080de3b0 f0bc
    pop {r1}                                 @ 080de3b2 02bc
    bx r1                                    @ 080de3b4 0847
    .zero  0x2
DAT_080de3b8:
    .word  pack_ui_state                  @ 080de3b8 50580003
DAT_080de3bc:
    .word  0x02000000                     @ 080de3bc 00000002
DAT_080de3c0:
    .word  0x00006c38                     @ 080de3c0 386c0000
DAT_080de3c4:
    .word  0x05f5e0ff                     @ 080de3c4 ffe0f505
DAT_080de3c8:
    .word  0x0600f8e8                     @ 080de3c8 e8f80006
DAT_080de3cc:
    .word  0x02006ed0                     @ 080de3cc d06e0002
PTR_font_jp_base_table_080de3d0:
    .word  font_jp_base_table             @ 080de3d0 54f8e509
DAT_080de3d4:
    .word  0x00008008                     @ 080de3d4 08800000
DAT_080de3d8:
    .word  0x0000138f                     @ 080de3d8 8f130000
PTR_game_str_pointer_table_080de3dc:
    .word  game_str_pointer_table         @ 080de3dc 400f0008
DAT_080de3e0:
    .word  0x00006c2c                     @ 080de3e0 2c6c0000
PTR_game_str_ja_080de3e4:
    .word  game_str_ja                    @ 080de3e4 109cdb09

@ Pack card list screen render main function. Initializes font, renders pack name text (game_str_id 0x1389), iterates all card slots rendering grid numbers, card info, confirm button labels. Finally calls render_pack_info_to_vram for pack summary info and DMAs palette to VRAM. Function body ~420 asm lines with 10+ named callees. Called by font_jp_080dfc18 (pack list page frame driver) when a full list redraw is needed.
@ 
@ Constants:
@ PACK_NAME_STR_ID = 0x1389
@ CONFIRM_LABEL_1  = 0x138a
@ 
@ Params: r0=void (first instruction ldr r0,DAT_080de720 clobbers r0; caller value discarded)
@ Return: r0=u32 result (Sub-case E passthrough of last callee return)
render_pack_card_list_screen:
    push {r4,r5,r6,r7,lr}                    @ 080de3e8 f0b5
    .hword 0x4657    @ 080de3ea 5746
    .hword 0x464e    @ 080de3ec 4e46
    .hword 0x4645    @ 080de3ee 4546
    push {r5,r6,r7}                          @ 080de3f0 e0b4
    sub sp,#0x4                              @ 080de3f2 81b0
    ldr r0, DAT_080de720                     @ 080de3f4 ca48
    str r0,[sp,#0x0]                         @ 080de3f6 0090
    movs r1,#0x1    @ 080de3f8 0121
    .hword 0x468a    @ 080de3fa 8a46
    ldr r2, DAT_080de724                     @ 080de3fc c94a
    movs r0,#0x2    @ 080de3fe 0220
    rsbs r0,r0,#0    @ 080de400 4042
    ldrb r3,[r2,#0x15]                       @ 080de402 537d
    ands r0,r3    @ 080de404 1840
    strb r0,[r2,#0x15]                       @ 080de406 5075
    movs r1,#0x2    @ 080de408 0221
    ldrb r0,[r2,#0x8]                        @ 080de40a 107a
    orrs r1,r0    @ 080de40c 0143
    strb r1,[r2,#0x8]                        @ 080de40e 1172
    movs r0,#0x7d    @ 080de410 7d20
    rsbs r0,r0,#0    @ 080de412 4042
    ldrb r3,[r2,#0x14]                       @ 080de414 137d
    ands r0,r3    @ 080de416 1840
    strb r0,[r2,#0x14]                       @ 080de418 1075
    ldr r3, PTR_font_jp_base_table_080de728  @ 080de41a c34b
    lsls r0,r1,#0x1e    @ 080de41c 8807
    lsrs r0,r0,#0x1f    @ 080de41e c00f
    lsls r0,r0,#0x2    @ 080de420 8000
    lsls r1,r1,#0x1f    @ 080de422 c907
    lsrs r1,r1,#0x1f    @ 080de424 c90f
    lsls r1,r1,#0x3    @ 080de426 c900
    adds r0,r0,r1    @ 080de428 4018
    adds r0,r0,r3    @ 080de42a c018
    ldr r0,[r0,#0x0]                         @ 080de42c 0068
    str r0,[r2,#0x4]                         @ 080de42e 5060
    movs r0,#0x20    @ 080de430 2020
    movs r1,#0x2    @ 080de432 0221
    bl setup_line_buf_pos_and_font           @ 080de434 12f0befb
    ldr r0, DAT_080de72c                     @ 080de438 bc48
    bl game_str_id_to_row                    @ 080de43a 16f0edfc
    ldr r2, PTR_game_str_pointer_table_080de730 @ 080de43e bc4a
    lsls r0,r0,#0x10    @ 080de440 0004
    lsrs r0,r0,#0x10    @ 080de442 000c
    lsls r1,r0,#0x1    @ 080de444 4100
    adds r1,r1,r0    @ 080de446 0918
    lsls r1,r1,#0x1    @ 080de448 4900
    ldr r0, DAT_080de734                     @ 080de44a ba48
    ldr r3, DAT_080de738                     @ 080de44c ba4b
    adds r0,r0,r3    @ 080de44e c018
    ldrb r0,[r0,#0x0]                        @ 080de450 0078
    lsls r0,r0,#0x1d    @ 080de452 4007
    lsrs r0,r0,#0x1d    @ 080de454 400f
    adds r1,r1,r0    @ 080de456 0918
    lsls r1,r1,#0x2    @ 080de458 8900
    adds r1,r1,r2    @ 080de45a 8918
    ldr r1,[r1,#0x0]                         @ 080de45c 0968
    ldr r0, PTR_game_str_ja_080de73c         @ 080de45e b748
    adds r1,r1,r0    @ 080de460 0918
    .hword 0x4689    @ 080de462 8946
    .hword 0x4648    @ 080de464 4846
    bl measure_string_pixel_width            @ 080de466 11f005ff
    adds r7,r0,#0x0    @ 080de46a 071c
    movs r0,#0xf0    @ 080de46c f020
    subs r0,r0,r7    @ 080de46e c01b
    asrs r5,r0,#0x1    @ 080de470 4510
    adds r0,r5,#0x1    @ 080de472 681c
    movs r2,#0x84    @ 080de474 8422
    lsls r2,r2,#0x1    @ 080de476 5200
    movs r1,#0x3    @ 080de478 0321
    .hword 0x464b    @ 080de47a 4b46
    bl text_render_wrapper                   @ 080de47c 14f0fefa
    ldr r2, DAT_080de740                     @ 080de480 af4a
    adds r0,r5,#0x0    @ 080de482 281c
    movs r1,#0x2    @ 080de484 0221
    .hword 0x464b    @ 080de486 4b46
    bl text_render_wrapper                   @ 080de488 14f0f8fa
    movs r4,#0x80    @ 080de48c 8024
    lsls r4,r4,#0x4    @ 080de48e 2401
    ldr r0,[sp,#0x0]                         @ 080de490 0098
    adds r1,r4,#0x0    @ 080de492 211c
    bl zero_fill_halfword_wrapper            @ 080de494 16f000fd
    ldr r0,[sp,#0x0]                         @ 080de498 0098
    movs r1,#0x0    @ 080de49a 0021
    bl commit_line_buffer_to_sprite_vram     @ 080de49c 14f0d6fc
    ldr r0,[sp,#0x0]                         @ 080de4a0 0098
    adds r0,r0,r4    @ 080de4a2 0019
    str r0,[sp,#0x0]                         @ 080de4a4 0090
    ldr r0, DAT_080de744                     @ 080de4a6 a748
    movs r1,#0x3f    @ 080de4a8 3f21
    .hword 0x4688    @ 080de4aa 8846
LAB_080de4ac:
    .hword 0x4652    @ 080de4ac 5246
    strh r2,[r0,#0x0]                        @ 080de4ae 0280
    adds r0,#0x2    @ 080de4b0 0230
    movs r3,#0x1    @ 080de4b2 0123
    add r10,r3                               @ 080de4b4 9a44
    movs r1,#0x1    @ 080de4b6 0121
    rsbs r1,r1,#0    @ 080de4b8 4942
    add r8,r1                                @ 080de4ba 8844
    .hword 0x4642    @ 080de4bc 4246
    cmp r2,#0x0                              @ 080de4be 002a
    bge LAB_080de4ac                         @ 080de4c0 f4da
    .hword 0x4698    @ 080de4c2 9846
    movs r3,#0x90    @ 080de4c4 9023
    lsls r3,r3,#0x1    @ 080de4c6 5b00
    .hword 0x4699    @ 080de4c8 9946
LAB_080de4ca:
    movs r0,#0x3    @ 080de4ca 0320
    movs r1,#0x3    @ 080de4cc 0321
    bl setup_line_buf_pos_and_font           @ 080de4ce 12f071fb
    .hword 0x4640    @ 080de4d2 4046
    bl compute_pack_grid_slot_oam_xy         @ 080de4d4 fff7d2fd
    adds r7,r0,#0x0    @ 080de4d8 071c
    movs r1,#0x7    @ 080de4da 0721
    ands r0,r1    @ 080de4dc 0840
    adds r5,r0,#0x1    @ 080de4de 451c
    lsrs r4,r7,#0x10    @ 080de4e0 3c0c
    adds r0,r4,#0x0    @ 080de4e2 201c
    ands r0,r1    @ 080de4e4 0840
    adds r6,r0,#0x3    @ 080de4e6 c61c
    .hword 0x4640    @ 080de4e8 4046
    movs r1,#0xa    @ 080de4ea 0a21
    bl get_bios_div_remainder                @ 080de4ec 2ff088ff
    adds r3,r0,#0x0    @ 080de4f0 031c
    adds r0,r5,#0x0    @ 080de4f2 281c
    adds r1,r6,#0x0    @ 080de4f4 311c
    ldr r2, DAT_080de748                     @ 080de4f6 944a
    bl render_decimal_digits_jp_signed       @ 080de4f8 14f0a8fb
    .hword 0x4640    @ 080de4fc 4046
    movs r1,#0xa    @ 080de4fe 0a21
    bl get_bios_div_remainder                @ 080de500 2ff07eff
    adds r3,r0,#0x0    @ 080de504 031c
    adds r0,r5,#0x0    @ 080de506 281c
    adds r1,r6,#0x0    @ 080de508 311c
    ldr r2, DAT_080de740                     @ 080de50a 8d4a
    bl render_decimal_digits_jp_signed       @ 080de50c 14f09efb
    ldr r0,[sp,#0x0]                         @ 080de510 0098
    .hword 0x4649    @ 080de512 4946
    bl zero_fill_halfword_wrapper            @ 080de514 16f0c0fc
    ldr r0,[sp,#0x0]                         @ 080de518 0098
    movs r1,#0x0    @ 080de51a 0021
    bl commit_line_buffer_to_sprite_vram     @ 080de51c 14f096fc
    ldr r2,[sp,#0x0]                         @ 080de520 009a
    add r2,r9                                @ 080de522 4a44
    str r2,[sp,#0x0]                         @ 080de524 0092
    lsls r0,r7,#0x10    @ 080de526 3804
    lsrs r0,r0,#0x13    @ 080de528 c00c
    lsls r0,r0,#0x1    @ 080de52a 4000
    ldr r3, DAT_080de744                     @ 080de52c 854b
    adds r0,r3,r0    @ 080de52e 1818
    lsrs r4,r4,#0x3    @ 080de530 e408
    lsls r4,r4,#0x6    @ 080de532 a401
    adds r0,r0,r4    @ 080de534 0019
    .hword 0x4644    @ 080de536 4446
    adds r4,#0x1    @ 080de538 0134
    movs r6,#0x2    @ 080de53a 0226
LAB_080de53c:
    movs r5,#0x2    @ 080de53c 0225
LAB_080de53e:
    .hword 0x4651    @ 080de53e 5146
    strh r1,[r0,#0x0]                        @ 080de540 0180
    adds r0,#0x2    @ 080de542 0230
    movs r2,#0x1    @ 080de544 0122
    add r10,r2                               @ 080de546 9244
    subs r5,#0x1    @ 080de548 013d
    cmp r5,#0x0                              @ 080de54a 002d
    bge LAB_080de53e                         @ 080de54c f7da
    adds r0,#0x3a    @ 080de54e 3a30
    subs r6,#0x1    @ 080de550 013e
    cmp r6,#0x0                              @ 080de552 002e
    bge LAB_080de53c                         @ 080de554 f2da
    .hword 0x46a0    @ 080de556 a046
    cmp r4,#0xa                              @ 080de558 0a2c
    ble LAB_080de4ca                         @ 080de55a b6dd
    ldr r2, DAT_080de724                     @ 080de55c 714a
    movs r0,#0x2    @ 080de55e 0220
    rsbs r0,r0,#0    @ 080de560 4042
    ldrb r3,[r2,#0x15]                       @ 080de562 537d
    ands r0,r3    @ 080de564 1840
    strb r0,[r2,#0x15]                       @ 080de566 5075
    movs r1,#0x3    @ 080de568 0321
    rsbs r1,r1,#0    @ 080de56a 4942
    ldrb r0,[r2,#0x8]                        @ 080de56c 107a
    ands r1,r0    @ 080de56e 0140
    strb r1,[r2,#0x8]                        @ 080de570 1172
    movs r0,#0x7d    @ 080de572 7d20
    rsbs r0,r0,#0    @ 080de574 4042
    ldrb r3,[r2,#0x14]                       @ 080de576 137d
    ands r0,r3    @ 080de578 1840
    strb r0,[r2,#0x14]                       @ 080de57a 1075
    ldr r0, PTR_font_jp_base_table_080de728  @ 080de57c 6a48
    lsls r1,r1,#0x1f    @ 080de57e c907
    lsrs r1,r1,#0x1f    @ 080de580 c90f
    lsls r1,r1,#0x3    @ 080de582 c900
    adds r1,r1,r0    @ 080de584 0918
    ldr r0,[r1,#0x0]                         @ 080de586 0868
    str r0,[r2,#0x4]                         @ 080de588 5060
    ldr r0, DAT_080de74c                     @ 080de58a 7048
    bl game_str_id_to_row                    @ 080de58c 16f044fc
    ldr r2, PTR_game_str_pointer_table_080de730 @ 080de590 674a
    lsls r0,r0,#0x10    @ 080de592 0004
    lsrs r0,r0,#0x10    @ 080de594 000c
    lsls r1,r0,#0x1    @ 080de596 4100
    adds r1,r1,r0    @ 080de598 0918
    lsls r1,r1,#0x1    @ 080de59a 4900
    ldr r0, DAT_080de734                     @ 080de59c 6548
    ldr r3, DAT_080de738                     @ 080de59e 664b
    adds r0,r0,r3    @ 080de5a0 c018
    ldrb r0,[r0,#0x0]                        @ 080de5a2 0078
    lsls r0,r0,#0x1d    @ 080de5a4 4007
    lsrs r0,r0,#0x1d    @ 080de5a6 400f
    adds r1,r1,r0    @ 080de5a8 0918
    lsls r1,r1,#0x2    @ 080de5aa 8900
    adds r1,r1,r2    @ 080de5ac 8918
    ldr r1,[r1,#0x0]                         @ 080de5ae 0968
    ldr r0, PTR_game_str_ja_080de73c         @ 080de5b0 6248
    adds r1,r1,r0    @ 080de5b2 0918
    .hword 0x4689    @ 080de5b4 8946
    .hword 0x4648    @ 080de5b6 4846
    bl measure_string_pixel_width            @ 080de5b8 11f05cfe
    movs r1,#0x30    @ 080de5bc 3021
    subs r1,r1,r0    @ 080de5be 091a
    asrs r7,r1,#0x1    @ 080de5c0 4f10
    movs r0,#0x7    @ 080de5c2 0720
    movs r1,#0x3    @ 080de5c4 0321
    bl setup_line_buf_pos_and_font           @ 080de5c6 12f0f5fa
    movs r0,#0x1    @ 080de5ca 0120
    bl encode_pack_confirm_oam_attr          @ 080de5cc fff776fd
    .hword 0x4680    @ 080de5d0 8046
    movs r1,#0x7    @ 080de5d2 0721
    ands r0,r1    @ 080de5d4 0840
    adds r5,r0,r7    @ 080de5d6 c519
    .hword 0x4640    @ 080de5d8 4046
    lsrs r4,r0,#0x10    @ 080de5da 040c
    adds r0,r4,#0x0    @ 080de5dc 201c
    ands r0,r1    @ 080de5de 0840
    adds r6,r0,#0x3    @ 080de5e0 c61c
    ldr r2, DAT_080de750                     @ 080de5e2 5b4a
    adds r0,r5,#0x0    @ 080de5e4 281c
    adds r1,r6,#0x0    @ 080de5e6 311c
    .hword 0x464b    @ 080de5e8 4b46
    bl text_render_wrapper                   @ 080de5ea 14f047fa
    adds r0,r5,#0x0    @ 080de5ee 281c
    adds r1,r6,#0x0    @ 080de5f0 311c
    movs r2,#0x7    @ 080de5f2 0722
    .hword 0x464b    @ 080de5f4 4b46
    bl text_render_wrapper                   @ 080de5f6 14f041fa
    movs r5,#0xa8    @ 080de5fa a825
    lsls r5,r5,#0x2    @ 080de5fc ad00
    ldr r0,[sp,#0x0]                         @ 080de5fe 0098
    adds r1,r5,#0x0    @ 080de600 291c
    bl zero_fill_halfword_wrapper            @ 080de602 16f049fc
    ldr r0,[sp,#0x0]                         @ 080de606 0098
    movs r1,#0x0    @ 080de608 0021
    bl commit_line_buffer_to_sprite_vram     @ 080de60a 14f01ffc
    ldr r1,[sp,#0x0]                         @ 080de60e 0099
    adds r1,r1,r5    @ 080de610 4919
    str r1,[sp,#0x0]                         @ 080de612 0091
    .hword 0x4642    @ 080de614 4246
    lsls r0,r2,#0x10    @ 080de616 1004
    lsrs r0,r0,#0x13    @ 080de618 c00c
    lsls r0,r0,#0x1    @ 080de61a 4000
    ldr r3, DAT_080de744                     @ 080de61c 494b
    adds r0,r3,r0    @ 080de61e 1818
    lsrs r4,r4,#0x3    @ 080de620 e408
    lsls r4,r4,#0x6    @ 080de622 a401
    adds r0,r0,r4    @ 080de624 0019
    movs r6,#0x2    @ 080de626 0226
LAB_080de628:
    movs r5,#0x6    @ 080de628 0625
LAB_080de62a:
    .hword 0x4651    @ 080de62a 5146
    strh r1,[r0,#0x0]                        @ 080de62c 0180
    adds r0,#0x2    @ 080de62e 0230
    movs r2,#0x1    @ 080de630 0122
    add r10,r2                               @ 080de632 9244
    subs r5,#0x1    @ 080de634 013d
    cmp r5,#0x0                              @ 080de636 002d
    bge LAB_080de62a                         @ 080de638 f7da
    adds r0,#0x32    @ 080de63a 3230
    subs r6,#0x1    @ 080de63c 013e
    cmp r6,#0x0                              @ 080de63e 002e
    bge LAB_080de628                         @ 080de640 f2da
    ldr r0, DAT_080de754                     @ 080de642 4448
    bl game_str_id_to_row                    @ 080de644 16f0e8fb
    ldr r2, PTR_game_str_pointer_table_080de730 @ 080de648 394a
    lsls r0,r0,#0x10    @ 080de64a 0004
    lsrs r0,r0,#0x10    @ 080de64c 000c
    lsls r1,r0,#0x1    @ 080de64e 4100
    adds r1,r1,r0    @ 080de650 0918
    lsls r1,r1,#0x1    @ 080de652 4900
    ldr r0, DAT_080de734                     @ 080de654 3748
    ldr r3, DAT_080de738                     @ 080de656 384b
    adds r0,r0,r3    @ 080de658 c018
    ldrb r0,[r0,#0x0]                        @ 080de65a 0078
    lsls r0,r0,#0x1d    @ 080de65c 4007
    lsrs r0,r0,#0x1d    @ 080de65e 400f
    adds r1,r1,r0    @ 080de660 0918
    lsls r1,r1,#0x2    @ 080de662 8900
    adds r1,r1,r2    @ 080de664 8918
    ldr r1,[r1,#0x0]                         @ 080de666 0968
    ldr r0, PTR_game_str_ja_080de73c         @ 080de668 3448
    adds r1,r1,r0    @ 080de66a 0918
    .hword 0x4689    @ 080de66c 8946
    .hword 0x4648    @ 080de66e 4846
    bl measure_string_pixel_width            @ 080de670 11f000fe
    movs r1,#0x30    @ 080de674 3021
    subs r1,r1,r0    @ 080de676 091a
    asrs r7,r1,#0x1    @ 080de678 4f10
    movs r0,#0x7    @ 080de67a 0720
    movs r1,#0x3    @ 080de67c 0321
    bl setup_line_buf_pos_and_font           @ 080de67e 12f099fa
    movs r0,#0x0    @ 080de682 0020
    bl encode_pack_confirm_oam_attr          @ 080de684 fff71afd
    .hword 0x4680    @ 080de688 8046
    movs r1,#0x7    @ 080de68a 0721
    ands r0,r1    @ 080de68c 0840
    adds r5,r0,r7    @ 080de68e c519
    .hword 0x4640    @ 080de690 4046
    lsrs r4,r0,#0x10    @ 080de692 040c
    adds r0,r4,#0x0    @ 080de694 201c
    ands r0,r1    @ 080de696 0840
    adds r6,r0,#0x3    @ 080de698 c61c
    ldr r2, DAT_080de758                     @ 080de69a 2f4a
    adds r0,r5,#0x0    @ 080de69c 281c
    adds r1,r6,#0x0    @ 080de69e 311c
    .hword 0x464b    @ 080de6a0 4b46
    bl text_render_wrapper                   @ 080de6a2 14f0ebf9
    ldr r2, DAT_080de740                     @ 080de6a6 264a
    adds r0,r5,#0x0    @ 080de6a8 281c
    adds r1,r6,#0x0    @ 080de6aa 311c
    .hword 0x464b    @ 080de6ac 4b46
    bl text_render_wrapper                   @ 080de6ae 14f0e5f9
    movs r1,#0xa8    @ 080de6b2 a821
    lsls r1,r1,#0x2    @ 080de6b4 8900
    ldr r0,[sp,#0x0]                         @ 080de6b6 0098
    bl zero_fill_halfword_wrapper            @ 080de6b8 16f0eefb
    ldr r0,[sp,#0x0]                         @ 080de6bc 0098
    movs r1,#0x0    @ 080de6be 0021
    bl commit_line_buffer_to_sprite_vram     @ 080de6c0 14f0c4fb
    .hword 0x4641    @ 080de6c4 4146
    lsls r0,r1,#0x10    @ 080de6c6 0804
    lsrs r0,r0,#0x13    @ 080de6c8 c00c
    lsls r0,r0,#0x1    @ 080de6ca 4000
    ldr r2, DAT_080de744                     @ 080de6cc 1d4a
    adds r0,r2,r0    @ 080de6ce 1018
    lsrs r4,r4,#0x3    @ 080de6d0 e408
    lsls r4,r4,#0x6    @ 080de6d2 a401
    adds r0,r0,r4    @ 080de6d4 0019
    movs r6,#0x0    @ 080de6d6 0026
LAB_080de6d8:
    adds r1,r6,#0x1    @ 080de6d8 711c
    movs r5,#0x6    @ 080de6da 0625
LAB_080de6dc:
    .hword 0x4653    @ 080de6dc 5346
    strh r3,[r0,#0x0]                        @ 080de6de 0380
    adds r0,#0x2    @ 080de6e0 0230
    movs r2,#0x1    @ 080de6e2 0122
    add r10,r2                               @ 080de6e4 9244
    subs r5,#0x1    @ 080de6e6 013d
    cmp r5,#0x0                              @ 080de6e8 002d
    bge LAB_080de6dc                         @ 080de6ea f7da
    adds r0,#0x32    @ 080de6ec 3230
    adds r6,r1,#0x0    @ 080de6ee 0e1c
    cmp r6,#0x2                              @ 080de6f0 022e
    ble LAB_080de6d8                         @ 080de6f2 f1dd
    ldr r3, DAT_080de75c                     @ 080de6f4 194b
    movs r1,#0x84    @ 080de6f6 8421
    lsls r1,r1,#0x1    @ 080de6f8 4900
    adds r0,r3,r1    @ 080de6fa 5818
    .hword 0x4652    @ 080de6fc 5246
    strh r2,[r0,#0x0]                        @ 080de6fe 0280
    bl render_pack_info_to_vram              @ 080de700 fff7dcfd
    movs r0,#0xa0    @ 080de704 a020
    lsls r0,r0,#0x13    @ 080de706 c004
    ldr r1, DAT_080de760                     @ 080de708 1549
    movs r2,#0x20    @ 080de70a 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080de70c 16f0fcfb
    add sp,#0x4                              @ 080de710 01b0
    pop {r3,r4,r5}                           @ 080de712 38bc
    .hword 0x4698    @ 080de714 9846
    .hword 0x46a1    @ 080de716 a146
    .hword 0x46aa    @ 080de718 aa46
    pop {r4,r5,r6,r7}                        @ 080de71a f0bc
    pop {r0}                                 @ 080de71c 01bc
    bx r0                                    @ 080de71e 0047
DAT_080de720:
    .word  0x06000020                     @ 080de720 20000006
DAT_080de724:
    .word  0x02006ed0                     @ 080de724 d06e0002
PTR_font_jp_base_table_080de728:
    .word  font_jp_base_table             @ 080de728 54f8e509
DAT_080de72c:
    .word  0x00001389                     @ 080de72c 89130000
PTR_game_str_pointer_table_080de730:
    .word  game_str_pointer_table         @ 080de730 400f0008
DAT_080de734:
    .word  0x02000000                     @ 080de734 00000002
DAT_080de738:
    .word  0x00006c2c                     @ 080de738 2c6c0000
PTR_game_str_ja_080de73c:
    .word  game_str_ja                    @ 080de73c 109cdb09
DAT_080de740:
    .word  0x00000107                     @ 080de740 07010000
DAT_080de744:
    .word  0x0600f800                     @ 080de744 00f80006
DAT_080de748:
    .word  0x0000810f                     @ 080de748 0f810000
DAT_080de74c:
    .word  0x00001007                     @ 080de74c 07100000
DAT_080de750:
    .word  0x00008008                     @ 080de750 08800000
DAT_080de754:
    .word  0x00001008                     @ 080de754 08100000
DAT_080de758:
    .word  0x00008108                     @ 080de758 08810000
DAT_080de75c:
    .word  0x0300585c                     @ 080de75c 5c580003
DAT_080de760:
    .word  0x09ccd290                     @ 080de760 90d2cc09

@ Renders pack card thumbnail grid to OBJ VRAM.
@ r0=data_src_ptr, r1=packed_xy1 (lo16=x1, hi16=row_count), r2=packed_xy2 (lo16=x2, hi16=col_stride), r3=step_count.
@ First calls zero_fill_halfword_wrapper to clear target VRAM buffer.
@ Then iterates in 2D loop over card grid, reading each card tile ID from EWRAM card data (0x0200af20),
@ writing tile data to OBJ VRAM 0x06008040 region.
@ Outer loop by row (hi16 of r2), inner loop by column (hi16 of r1).
@ 
@ Constants:
@ - EWRAM_CARD_GRID = 0x0200af20 (EWRAM card grid data start)
@ - OBJ_VRAM_GRID = 0x06008040 (OBJ VRAM card grid write region)
render_pack_card_grid_to_obj_vram:
    push {r4,r5,r6,r7,lr}                    @ 080de764 f0b5
    .hword 0x4657    @ 080de766 5746
    .hword 0x464e    @ 080de768 4e46
    .hword 0x4645    @ 080de76a 4546
    push {r5,r6,r7}                          @ 080de76c e0b4
    sub sp,#0x2c                             @ 080de76e 8bb0
    adds r5,r0,#0x0    @ 080de770 051c
    adds r4,r3,#0x0    @ 080de772 1c1c
    lsls r0,r2,#0x10    @ 080de774 1004
    lsrs r0,r0,#0x10    @ 080de776 000c
    .hword 0x4682    @ 080de778 8246
    lsrs r2,r2,#0x10    @ 080de77a 120c
    str r2,[sp,#0x0]                         @ 080de77c 0092
    lsls r0,r1,#0x10    @ 080de77e 0804
    lsrs r0,r0,#0x10    @ 080de780 000c
    str r0,[sp,#0x4]                         @ 080de782 0190
    lsrs r1,r1,#0x10    @ 080de784 090c
    str r1,[sp,#0x8]                         @ 080de786 0291
    .hword 0x4656    @ 080de788 5646
    adds r6,#0x1    @ 080de78a 0136
    adds r0,r2,#0x0    @ 080de78c 101c
    adds r0,#0x1    @ 080de78e 0130
    lsls r0,r0,#0x3    @ 080de790 c000
    adds r1,r6,#0x0    @ 080de792 311c
    muls r1,r0    @ 080de794 4143
    lsls r1,r1,#0x3    @ 080de796 c900
    ldr r0, DAT_080de918                     @ 080de798 5f48
    bl zero_fill_halfword_wrapper            @ 080de79a 16f07dfb
    lsls r4,r4,#0x4    @ 080de79e 2401
    movs r2,#0x7    @ 080de7a0 0722
    ldr r1,[sp,#0x4]                         @ 080de7a2 0199
    ands r1,r2    @ 080de7a4 1140
    ldr r0, DAT_080de918                     @ 080de7a6 5c48
    adds r1,r1,r0    @ 080de7a8 0918
    ldr r0,[sp,#0x8]                         @ 080de7aa 0298
    ands r0,r2    @ 080de7ac 1040
    lsls r0,r0,#0x3    @ 080de7ae c000
    muls r0,r6    @ 080de7b0 7043
    adds r1,r1,r0    @ 080de7b2 0918
    movs r2,#0x0    @ 080de7b4 0022
    ldr r3,[sp,#0x0]                         @ 080de7b6 009b
    cmp r2,r3                                @ 080de7b8 9a42
    bcs LAB_080de832                         @ 080de7ba 3ad2
    str r6,[sp,#0x24]                        @ 080de7bc 0996
    .hword 0x4657    @ 080de7be 5746
    lsls r7,r7,#0x3    @ 080de7c0 ff00
    .hword 0x46bc    @ 080de7c2 bc46
    lsls r0,r6,#0x6    @ 080de7c4 b001
    str r0,[sp,#0x10]                        @ 080de7c6 0490
LAB_080de7c8:
    movs r3,#0x0    @ 080de7c8 0023
    adds r2,#0x1    @ 080de7ca 0132
    .hword 0x4691    @ 080de7cc 9146
    cmp r3,r10                               @ 080de7ce 5345
    bcs LAB_080de822                         @ 080de7d0 27d2
    ldr r2,[sp,#0x24]                        @ 080de7d2 099a
    lsls r2,r2,#0x6    @ 080de7d4 9201
    .hword 0x4690    @ 080de7d6 9046
LAB_080de7d8:
    movs r0,#0x0    @ 080de7d8 0020
    adds r3,#0x1    @ 080de7da 0133
    str r3,[sp,#0x28]                        @ 080de7dc 0a93
LAB_080de7de:
    adds r6,r0,#0x1    @ 080de7de 461c
    movs r2,#0x3    @ 080de7e0 0322
LAB_080de7e2:
    movs r0,#0xf    @ 080de7e2 0f20
    ldrb r3,[r5,#0x0]                        @ 080de7e4 2b78
    ands r0,r3    @ 080de7e6 1840
    cmp r0,#0x0                              @ 080de7e8 0028
    beq LAB_080de7f0                         @ 080de7ea 01d0
    adds r0,r0,r4    @ 080de7ec 0019
    strb r0,[r1,#0x0]                        @ 080de7ee 0870
LAB_080de7f0:
    adds r1,#0x1    @ 080de7f0 0131
    movs r0,#0xf0    @ 080de7f2 f020
    ldrb r7,[r5,#0x0]                        @ 080de7f4 2f78
    ands r0,r7    @ 080de7f6 3840
    lsls r0,r0,#0x18    @ 080de7f8 0006
    cmp r0,#0x0                              @ 080de7fa 0028
    beq LAB_080de804                         @ 080de7fc 02d0
    lsrs r0,r0,#0x1c    @ 080de7fe 000f
    adds r0,r0,r4    @ 080de800 0019
    strb r0,[r1,#0x0]                        @ 080de802 0870
LAB_080de804:
    adds r1,#0x1    @ 080de804 0131
    adds r5,#0x1    @ 080de806 0135
    subs r2,#0x1    @ 080de808 013a
    cmp r2,#0x0                              @ 080de80a 002a
    bge LAB_080de7e2                         @ 080de80c e9da
    add r1,r12                               @ 080de80e 6144
    adds r0,r6,#0x0    @ 080de810 301c
    cmp r0,#0x7                              @ 080de812 0728
    ble LAB_080de7de                         @ 080de814 e3dd
    .hword 0x4640    @ 080de816 4046
    subs r1,r1,r0    @ 080de818 091a
    adds r1,#0x8    @ 080de81a 0831
    ldr r3,[sp,#0x28]                        @ 080de81c 0a9b
    cmp r3,r10                               @ 080de81e 5345
    bcc LAB_080de7d8                         @ 080de820 dad3
LAB_080de822:
    .hword 0x4662    @ 080de822 6246
    subs r1,r1,r2    @ 080de824 891a
    ldr r3,[sp,#0x10]                        @ 080de826 049b
    adds r1,r1,r3    @ 080de828 c918
    .hword 0x464a    @ 080de82a 4a46
    ldr r7,[sp,#0x0]                         @ 080de82c 009f
    cmp r2,r7                                @ 080de82e ba42
    bcc LAB_080de7c8                         @ 080de830 cad3
LAB_080de832:
    .hword 0x46d0    @ 080de832 d046
    movs r1,#0x7    @ 080de834 0721
    ldr r0,[sp,#0x4]                         @ 080de836 0198
    ands r0,r1    @ 080de838 0840
    cmp r0,#0x0                              @ 080de83a 0028
    beq LAB_080de842                         @ 080de83c 01d0
    movs r0,#0x1    @ 080de83e 0120
    add r8,r0                                @ 080de840 8044
LAB_080de842:
    ldr r2,[sp,#0x0]                         @ 080de842 009a
    str r2,[sp,#0xc]                         @ 080de844 0392
    ldr r0,[sp,#0x8]                         @ 080de846 0298
    ands r0,r1    @ 080de848 0840
    cmp r0,#0x0                              @ 080de84a 0028
    beq LAB_080de854                         @ 080de84c 02d0
    adds r3,r2,#0x0    @ 080de84e 131c
    adds r3,#0x1    @ 080de850 0133
    str r3,[sp,#0xc]                         @ 080de852 0393
LAB_080de854:
    ldr r5, DAT_080de918                     @ 080de854 304d
    ldr r7,[sp,#0x4]                         @ 080de856 019f
    lsrs r0,r7,#0x3    @ 080de858 f808
    ldr r1,[sp,#0x8]                         @ 080de85a 0299
    lsrs r2,r1,#0x3    @ 080de85c ca08
    lsls r1,r2,#0x3    @ 080de85e d100
    subs r1,r1,r2    @ 080de860 891a
    lsls r1,r1,#0x1    @ 080de862 4900
    adds r0,r0,r1    @ 080de864 4018
    lsls r0,r0,#0x6    @ 080de866 8001
    ldr r2, DAT_080de91c                     @ 080de868 2c4a
    adds r1,r0,r2    @ 080de86a 8118
    movs r2,#0x0    @ 080de86c 0022
    ldr r3,[sp,#0xc]                         @ 080de86e 039b
    cmp r2,r3                                @ 080de870 9a42
    bge LAB_080de908                         @ 080de872 49da
    .hword 0x4657    @ 080de874 5746
    adds r7,#0x1    @ 080de876 0137
    str r7,[sp,#0x24]                        @ 080de878 0997
    .hword 0x4640    @ 080de87a 4046
    lsls r0,r0,#0x3    @ 080de87c c000
    str r0,[sp,#0x20]                        @ 080de87e 0890
    lsls r3,r7,#0x6    @ 080de880 bb01
    str r3,[sp,#0x18]                        @ 080de882 0693
    movs r0,#0xe    @ 080de884 0e20
    .hword 0x4647    @ 080de886 4746
    subs r0,r0,r7    @ 080de888 c01b
    lsls r0,r0,#0x6    @ 080de88a 8001
    str r0,[sp,#0x1c]                        @ 080de88c 0790
LAB_080de88e:
    movs r3,#0x0    @ 080de88e 0023
    adds r2,#0x1    @ 080de890 0132
    .hword 0x4691    @ 080de892 9146
    cmp r3,r8                                @ 080de894 4345
    bge LAB_080de8f4                         @ 080de896 2dda
    .hword 0x4650    @ 080de898 5046
    lsls r0,r0,#0x3    @ 080de89a c000
    .hword 0x4684    @ 080de89c 8446
    ldr r2,[sp,#0x24]                        @ 080de89e 099a
    lsls r2,r2,#0x6    @ 080de8a0 9201
    str r2,[sp,#0x14]                        @ 080de8a2 0592
LAB_080de8a4:
    movs r0,#0x0    @ 080de8a4 0020
    adds r3,#0x1    @ 080de8a6 0133
    str r3,[sp,#0x28]                        @ 080de8a8 0a93
LAB_080de8aa:
    adds r6,r0,#0x1    @ 080de8aa 461c
    movs r2,#0x3    @ 080de8ac 0322
LAB_080de8ae:
    ldr r4, DAT_080de920                     @ 080de8ae 1c4c
    movs r3,#0x0    @ 080de8b0 0023
    ldrb r0,[r5,#0x0]                        @ 080de8b2 2878
    cmp r0,#0x0                              @ 080de8b4 0028
    beq LAB_080de8bc                         @ 080de8b6 01d0
    subs r4,#0xff    @ 080de8b8 ff3c
    adds r3,r0,#0x0    @ 080de8ba 031c
LAB_080de8bc:
    adds r5,#0x1    @ 080de8bc 0135
    ldrb r0,[r5,#0x0]                        @ 080de8be 2878
    cmp r0,#0x0                              @ 080de8c0 0028
    beq LAB_080de8ce                         @ 080de8c2 04d0
    movs r0,#0xff    @ 080de8c4 ff20
    ands r4,r0    @ 080de8c6 0440
    ldrb r7,[r5,#0x0]                        @ 080de8c8 2f78
    lsls r0,r7,#0x8    @ 080de8ca 3802
    orrs r3,r0    @ 080de8cc 0343
LAB_080de8ce:
    adds r5,#0x1    @ 080de8ce 0135
    ldrh r0,[r1,#0x0]                        @ 080de8d0 0888
    ands r4,r0    @ 080de8d2 0440
    orrs r3,r4    @ 080de8d4 2343
    strh r3,[r1,#0x0]                        @ 080de8d6 0b80
    adds r1,#0x2    @ 080de8d8 0231
    subs r2,#0x1    @ 080de8da 013a
    cmp r2,#0x0                              @ 080de8dc 002a
    bge LAB_080de8ae                         @ 080de8de e6da
    add r5,r12                               @ 080de8e0 6544
    adds r0,r6,#0x0    @ 080de8e2 301c
    cmp r0,#0x7                              @ 080de8e4 0728
    ble LAB_080de8aa                         @ 080de8e6 e0dd
    ldr r2,[sp,#0x14]                        @ 080de8e8 059a
    subs r5,r5,r2    @ 080de8ea ad1a
    adds r5,#0x8    @ 080de8ec 0835
    ldr r3,[sp,#0x28]                        @ 080de8ee 0a9b
    cmp r3,r8                                @ 080de8f0 4345
    blt LAB_080de8a4                         @ 080de8f2 d7db
LAB_080de8f4:
    ldr r3,[sp,#0x20]                        @ 080de8f4 089b
    subs r5,r5,r3    @ 080de8f6 ed1a
    ldr r7,[sp,#0x18]                        @ 080de8f8 069f
    adds r5,r5,r7    @ 080de8fa ed19
    ldr r0,[sp,#0x1c]                        @ 080de8fc 0798
    adds r1,r1,r0    @ 080de8fe 0918
    .hword 0x464a    @ 080de900 4a46
    ldr r3,[sp,#0xc]                         @ 080de902 039b
    cmp r2,r3                                @ 080de904 9a42
    blt LAB_080de88e                         @ 080de906 c2db
LAB_080de908:
    add sp,#0x2c                             @ 080de908 0bb0
    pop {r3,r4,r5}                           @ 080de90a 38bc
    .hword 0x4698    @ 080de90c 9846
    .hword 0x46a1    @ 080de90e a146
    .hword 0x46aa    @ 080de910 aa46
    pop {r4,r5,r6,r7}                        @ 080de912 f0bc
    pop {r0}                                 @ 080de914 01bc
    bx r0                                    @ 080de916 0047
DAT_080de918:
    .word  0x0200af20                     @ 080de918 20af0002
DAT_080de91c:
    .word  0x06008040                     @ 080de91c 40800006
DAT_080de920:
    .word  0x0000ffff                     @ 080de920 ffff0000

@ Pack card list scene main state machine dispatch. Called each frame by pack scene hub.
@ r0=ctx_val (stored in r7 for case functions). Reads step index from pack_ui_state+0xc (0x0300585c); if index > 5 calls store_pack_selection_to_state (returns 1 via parent epilogue). Otherwise dispatches via ROM function pointer table 0x080de954 (6 entries, bx r15 tail-call) for cases 0..5 covering pack card list sub-flows (init/card-select/confirm/exit etc.).
@ Constants: pack_ui_state+0xc (0x0300585c+2=step_index), FUNC_TABLE=0x080de954, TERMINAL_STATE=5.
@ Inputs: r0=u32 ctx_val. Returns: r0=u32 (out-of-bounds state>5 path: store_pack_selection_to_state writes r0=1 via parent epilogue; normal dispatch case path: 0=sub-step in progress, 1=sub-step complete; symmetric with dispatch_pack_page_state).
@ Side effects: [pack_ui_state+0xc step field] modified by case functions or store_pack_selection_to_state.
dispatch_pack_card_list_scene:
    push {r4,r5,r6,r7,lr}                    @ 080de924 f0b5
    .hword 0x4657    @ 080de926 5746
    .hword 0x464e    @ 080de928 4e46
    .hword 0x4645    @ 080de92a 4546
    push {r5,r6,r7}                          @ 080de92c e0b4
    sub sp,#0x38                             @ 080de92e 8eb0
    adds r7,r0,#0x0    @ 080de930 071c
    movs r0,#0x0    @ 080de932 0020
    str r0,[sp,#0x0]                         @ 080de934 0090
    ldr r1, DAT_080de94c                     @ 080de936 0549
    ldrh r0,[r1,#0x2]                        @ 080de938 4888
    cmp r0,#0x5                              @ 080de93a 0528
    bls LAB_080de942                         @ 080de93c 01d9
    bl store_pack_selection_to_state         @ 080de93e 00f0b5fc
LAB_080de942:
    lsls r0,r0,#0x2    @ 080de942 8000
    ldr r1, DAT_080de950                     @ 080de944 0249
    adds r0,r0,r1    @ 080de946 4018
    ldr r0,[r0,#0x0]                         @ 080de948 0068
    .hword 0x4687    @ 080de94a 8746
DAT_080de94c:
    .word  0x0300585c                     @ 080de94c 5c580003
DAT_080de950:
    .word  0x080de954                     @ 080de950 54e90d08
PTR_DAT_080de954:
    .word  0x080de96c                     @ 080de954 6ce90d08
    .word  0x080de9d0                     @ 080de958 d0e90d08
    .word  0x080dec28                     @ 080de95c 28ec0d08
    .word  0x080ded74                     @ 080de960 74ed0d08
    .word  0x080def34                     @ 080de964 34ef0d08
    .word  0x080df078                     @ 080de968 78f00d08
DAT_080de96c:
    ROM_INCBIN 0xde96c, 0x940

@ Inline exit fragment: writes parent-frame sp[0] pack selection result to pack_ui_state+0xe, returns 1.
@ No independent push/pop; inherits parent function 080de924 stack frame.
@ Parent stores pack type code at sp[0] on entry; this fragment reads it via .hword 0x466a (mov r2,sp) + ldrh,
@ writes to pack_ui_state+0xe (selection result field), then runs parent-frame epilogue.
@ Triggered when parent function 080de924 switch has [pack_ui_state+2] > 5 (0x080de93e bl site).
@ 
@ Constants:
@ - PACK_UI_STATE_BASE = 0x0300585c (= pack_ui_state + 0xc, sub-struct offset)
@ - PACK_SELECT_FIELD = +0x2 (strh target = pack_ui_state+0xe, pack selection result field)
store_pack_selection_to_state:
    .hword 0x466a    @ 080df2ac 6a46
    ldrh r3,[r2,#0x0]                        @ 080df2ae 1388
    ldr r2, DAT_080df2cc                     @ 080df2b0 064a
    strh r3,[r2,#0x2]                        @ 080df2b2 5380
    movs r4,#0x1    @ 080df2b4 0124
    str r4,[sp,#0x0]                         @ 080df2b6 0094
    ldr r0,[sp,#0x0]                         @ 080df2b8 0098
    add sp,#0x38                             @ 080df2ba 0eb0
    pop {r3,r4,r5}                           @ 080df2bc 38bc
    .hword 0x4698    @ 080df2be 9846
    .hword 0x46a1    @ 080df2c0 a146
    .hword 0x46aa    @ 080df2c2 aa46
    pop {r4,r5,r6,r7}                        @ 080df2c4 f0bc
    pop {r1}                                 @ 080df2c6 02bc
    bx r1                                    @ 080df2c8 0847
    .zero  0x2
DAT_080df2cc:
    .word  0x0300585c                     @ 080df2cc 5c580003

@ Renders ATK values of 10 pack cards as JP digit tiles and writes to BG VRAM.
@ No parameters. Selects font from pack_ui_state (IWRAM 0x02006ed0 display state struct).
@ Loops 10 times (r4=0..9), reads each card ATK from ROM ATK table (0x09cebf64, 0x40 bytes/entry),
@ copies tile template via tile_2d_row_copy, sets position via setup_line_buf_pos_and_font,
@ draws signed decimal via render_decimal_digits_jp_signed, writes row to BG VRAM 0x06012000.
@ After index 9, copies one extra tail row to 0x060113a0.
@ 
@ Constants:
@ - FONT_STATE_BASE = 0x02006ed0 (IWRAM font/display state struct base)
@ - ROM_PACK_ATK_TABLE = 0x09cebf64 (ROM pack ATK data table, 0x40 bytes/entry)
@ - BG_VRAM_DIGITS = 0x06012000 (BG VRAM ATK digit row write base)
@ - BG_VRAM_TAIL = 0x060113a0 (last row tile copy destination)
@ - LOOP_COUNT = 10 ([0..9], cmp r4,#9; bls)
render_pack_card_atk_rows_to_bg:
    push {r4,r5,r6,lr}                       @ 080df2d0 70b5
    ldr r2, DAT_080df350                     @ 080df2d2 1f4a
    movs r0,#0x2    @ 080df2d4 0220
    rsbs r0,r0,#0    @ 080df2d6 4042
    ldrb r1,[r2,#0x15]                       @ 080df2d8 517d
    ands r0,r1    @ 080df2da 0840
    strb r0,[r2,#0x15]                       @ 080df2dc 5075
    movs r1,#0x2    @ 080df2de 0221
    ldrb r3,[r2,#0x8]                        @ 080df2e0 137a
    orrs r1,r3    @ 080df2e2 1943
    strb r1,[r2,#0x8]                        @ 080df2e4 1172
    movs r0,#0x7d    @ 080df2e6 7d20
    rsbs r0,r0,#0    @ 080df2e8 4042
    ldrb r3,[r2,#0x14]                       @ 080df2ea 137d
    ands r0,r3    @ 080df2ec 1840
    strb r0,[r2,#0x14]                       @ 080df2ee 1075
    ldr r3, PTR_font_jp_base_table_080df354  @ 080df2f0 184b
    lsls r0,r1,#0x1e    @ 080df2f2 8807
    lsrs r0,r0,#0x1f    @ 080df2f4 c00f
    lsls r0,r0,#0x2    @ 080df2f6 8000
    lsls r1,r1,#0x1f    @ 080df2f8 c907
    lsrs r1,r1,#0x1f    @ 080df2fa c90f
    lsls r1,r1,#0x3    @ 080df2fc c900
    adds r0,r0,r1    @ 080df2fe 4018
    adds r0,r0,r3    @ 080df300 c018
    ldr r0,[r0,#0x0]                         @ 080df302 0068
    str r0,[r2,#0x4]                         @ 080df304 5060
    ldr r5, DAT_080df358                     @ 080df306 144d
    movs r4,#0x0    @ 080df308 0024
LAB_080df30a:
    ldr r6, DAT_080df35c                     @ 080df30a 144e
    ldr r1,[r6,#0xc]                         @ 080df30c f168
    adds r0,r5,#0x0    @ 080df30e 281c
    movs r2,#0x2    @ 080df310 0222
    movs r3,#0x2    @ 080df312 0223
    bl tile_2d_row_copy                      @ 080df314 18f0def8
    movs r0,#0x2    @ 080df318 0220
    movs r1,#0x2    @ 080df31a 0221
    bl setup_line_buf_pos_and_font           @ 080df31c 11f04afc
    movs r0,#0x1    @ 080df320 0120
    movs r1,#0x3    @ 080df322 0321
    ldr r2, DAT_080df360                     @ 080df324 0e4a
    adds r3,r4,#0x0    @ 080df326 231c
    bl render_decimal_digits_jp_signed       @ 080df328 13f090fc
    adds r0,r5,#0x0    @ 080df32c 281c
    movs r1,#0x0    @ 080df32e 0021
    bl write_line_buf_to_bg_tile_vram        @ 080df330 14f050fa
    adds r5,#0x40    @ 080df334 4035
    adds r4,#0x1    @ 080df336 0134
    cmp r4,#0x9                              @ 080df338 092c
    bls LAB_080df30a                         @ 080df33a e6d9
    ldr r0, DAT_080df364                     @ 080df33c 0948
    ldr r1,[r6,#0x10]                        @ 080df33e 3169
    movs r2,#0x2    @ 080df340 0222
    movs r3,#0x2    @ 080df342 0223
    bl tile_2d_row_copy                      @ 080df344 18f0c6f8
    pop {r4,r5,r6}                           @ 080df348 70bc
    pop {r0}                                 @ 080df34a 01bc
    bx r0                                    @ 080df34c 0047
    .zero  0x2
DAT_080df350:
    .word  0x02006ed0                     @ 080df350 d06e0002
PTR_font_jp_base_table_080df354:
    .word  font_jp_base_table             @ 080df354 54f8e509
DAT_080df358:
    .word  0x06012000                     @ 080df358 00200106
DAT_080df35c:
    .word  0x09cebf64                     @ 080df35c 64bfce09
DAT_080df360:
    .word  0x00000107                     @ 080df360 07010000
DAT_080df364:
    .word  0x060113a0                     @ 080df364 a0130106

