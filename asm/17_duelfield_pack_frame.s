@ ==== 17_duelfield_pack_frame.s ====
@ duel 场地刷新 + zone 卡动画 OAM + pack 卡静态帧
.thumb
@ render_duel_field_zone_info 的 state-driven wrapper. 读 gPageState [+0x210] u16 packed (bit7=player_flag, low7=mode, high7=sub_idx), 若 mode==0xb 则 sub_idx 经 gPageState[+0x4c+player*2] 的 lookup 表重映射. 调 render_duel_field_zone_info(player, mode, sub_idx). 无入参/无返回值. 用途: 光标 hover 决斗场 zone 改变后, 此函数按当前 state 重渲染. 14 个 caller 跨 PageManager / scene loader / banner 等.
refresh_duel_field_zone_info:
    push {r4,r5,r6,r7,lr}                    @ 080cbf0c f0b5
    ldr r7, DAT_080cbf54                     @ 080cbf0e 114f  -- r7 = &gPageState (0x02023130)
    movs r1,#0x84    @ 080cbf10 8421
    lsls r1,r1,#0x2    @ 080cbf12 8900
    adds r0,r7,r1    @ 080cbf14 7818  -- r0 = &gPageState[+0x210] (0x02023340) - packed render-target
    ldrh r3,[r0,#0x0]                        @ 080cbf16 0388  -- r3 = packed u16 (bit7=player_flag, low7=mode, high7=sub_idx)
    adds r2,r3,#0x0    @ 080cbf18 1a1c
    movs r0,#0x80    @ 080cbf1a 8020
    ands r0,r2    @ 080cbf1c 1040
    lsls r0,r0,#0x18    @ 080cbf1e 0006
    lsrs r4,r0,#0x1f    @ 080cbf20 c40f  -- r4 = r6 = (r3 >> 7) & 1 = player_flag
    adds r6,r4,#0x0    @ 080cbf22 261c
    movs r1,#0x7f    @ 080cbf24 7f21
    adds r0,r1,#0x0    @ 080cbf26 081c
    ands r0,r2    @ 080cbf28 1040  -- r5 = r3 & 0x7f = mode
    adds r5,r0,#0x0    @ 080cbf2a 051c
    lsrs r2,r3,#0x8    @ 080cbf2c 1a0a
    ands r2,r1    @ 080cbf2e 0a40  -- r2 = (r3 >> 8) & 0x7f = sub_idx
    cmp r5,#0xb                              @ 080cbf30 0b2d  -- 若 mode == 0xb (special): sub_idx 经 player-specific lookup 表重映射
    bne LAB_080cbf44                         @ 080cbf32 07d1
    lsls r0,r4,#0x1    @ 080cbf34 6000
    adds r1,r7,#0x0    @ 080cbf36 391c
    adds r1,#0x4c    @ 080cbf38 4c31
    adds r0,r0,r1    @ 080cbf3a 4018  -- lookup: gPageState[+0x4c + player_flag*2] (u16)
    ldrh r0,[r0,#0x0]                        @ 080cbf3c 0088
    adds r0,r0,r2    @ 080cbf3e 8018  -- sub_idx = lookup_value + (r3>>8)&0x7f, 截断到 u16
    lsls r0,r0,#0x10    @ 080cbf40 0004
    lsrs r2,r0,#0x10    @ 080cbf42 020c
LAB_080cbf44:
    adds r0,r6,#0x0    @ 080cbf44 301c
    adds r1,r5,#0x0    @ 080cbf46 291c
    bl render_duel_field_zone_info           @ 080cbf48 fff726fd  -- render_duel_field_zone_info(player_flag, mode, sub_idx)
    pop {r4,r5,r6,r7}                        @ 080cbf4c f0bc
    pop {r0}                                 @ 080cbf4e 01bc
    bx r0                                    @ 080cbf50 0047  -- epilogue (无返回值)
    .zero  0x2
DAT_080cbf54:
    .word  0x02023130                     @ 080cbf54 30310202

@ Builds complete duel field zone display state for dispatch_card_display_op case 0x32. Zero-fills gDuelZoneState (0x02020160, 0x2f5c halfwords=0x5eb8 bytes). Extracts zone_id from r0[7:0], writes <<13 into [base+0x2f50][20:13], sets [base+0x2f51] bit0, sets ctrl [0x02023345] bit2. Calls get_duel_activation_zone_id, decodes zone class bits, writes [base+0x2f57]/[base+0x2f58] zone category fields. Inner loop: for each slot calls ensure_card_id_cache_entry + find_zone_descriptor_by_slot_id + eval_slot_score_entry_full; reads ATK/DEF/level from card_stats_table via ldmia/stmia. r0=u8 zone_descriptor [0..0xff]. Returns void. Constants: gDuelZoneState=0x02020160, gDuelActivation=0x0201e2a0, zero_len=0x2f5c halfwords.
build_field_zone_display_state:
    push {r4,r5,r6,r7,lr}                    @ 080cbf58 f0b5
    .hword 0x4657    @ 080cbf5a 5746
    .hword 0x464e    @ 080cbf5c 4e46
    .hword 0x4645    @ 080cbf5e 4546
    push {r5,r6,r7}                          @ 080cbf60 e0b4
    sub sp,#0x130                            @ 080cbf62 ccb0
    adds r4,r0,#0x0    @ 080cbf64 041c
    ldr r5, DAT_080cc088                     @ 080cbf66 484d
    ldr r1, DAT_080cc08c                     @ 080cbf68 4849
    adds r0,r5,#0x0    @ 080cbf6a 281c
    bl zero_fill_by_halfword                 @ 080cbf6c 28f082ff
    ldr r0, DAT_080cc090                     @ 080cbf70 4748
    adds r2,r5,r0    @ 080cbf72 2a18
    lsls r4,r4,#0x10    @ 080cbf74 2404
    lsrs r4,r4,#0x10    @ 080cbf76 240c
    movs r0,#0xff    @ 080cbf78 ff20
    ands r4,r0    @ 080cbf7a 0440
    lsls r4,r4,#0xd    @ 080cbf7c 6403
    ldr r0,[r2,#0x0]                         @ 080cbf7e 1068
    ldr r1, DAT_080cc094                     @ 080cbf80 4449
    ands r0,r1    @ 080cbf82 0840
    orrs r0,r4    @ 080cbf84 2043
    str r0,[r2,#0x0]                         @ 080cbf86 1060
    ldr r2, DAT_080cc098                     @ 080cbf88 434a
    adds r1,r5,r2    @ 080cbf8a a918
    movs r0,#0x1    @ 080cbf8c 0120
    ldrb r3,[r1,#0x0]                        @ 080cbf8e 0b78
    orrs r0,r3    @ 080cbf90 1843
    strb r0,[r1,#0x0]                        @ 080cbf92 0870
    ldr r1, DAT_080cc09c                     @ 080cbf94 4149
    ldr r6, DAT_080cc0a0                     @ 080cbf96 424e
    adds r1,r1,r6    @ 080cbf98 8919
    movs r0,#0x4    @ 080cbf9a 0420
    ldrb r2,[r1,#0x0]                        @ 080cbf9c 0a78
    orrs r0,r2    @ 080cbf9e 1043
    strb r0,[r1,#0x0]                        @ 080cbfa0 0870
    bl get_duel_activation_zone_id           @ 080cbfa2 c8f7b7f9
    lsls r0,r0,#0x10    @ 080cbfa6 0004
    lsrs r2,r0,#0x10    @ 080cbfa8 020c
    movs r1,#0x7    @ 080cbfaa 0721
    ands r2,r1    @ 080cbfac 0a40
    ldr r3, DAT_080cc0a4                     @ 080cbfae 3d4b
    adds r1,r5,r3    @ 080cbfb0 e918
    lsls r2,r2,#0x5    @ 080cbfb2 5201
    movs r3,#0x1f    @ 080cbfb4 1f23
    adds r4,r3,#0x0    @ 080cbfb6 1c1c
    ldrb r6,[r1,#0x0]                        @ 080cbfb8 0e78
    ands r4,r6    @ 080cbfba 3440
    orrs r4,r2    @ 080cbfbc 1443
    strb r4,[r1,#0x0]                        @ 080cbfbe 0c70
    lsrs r0,r0,#0x13    @ 080cbfc0 c00c
    ldr r1, DAT_080cc0a8                     @ 080cbfc2 3949
    adds r2,r5,r1    @ 080cbfc4 6a18
    ands r0,r3    @ 080cbfc6 1840
    movs r1,#0x20    @ 080cbfc8 2021
    rsbs r1,r1,#0    @ 080cbfca 4942
    ldrb r6,[r2,#0x0]                        @ 080cbfcc 1678
    ands r1,r6    @ 080cbfce 3140
    orrs r1,r0    @ 080cbfd0 0143
    strb r1,[r2,#0x0]                        @ 080cbfd2 1170
    lsrs r4,r4,#0x5    @ 080cbfd4 6409
    adds r0,r3,#0x0    @ 080cbfd6 181c
    ands r0,r1    @ 080cbfd8 0840
    lsls r0,r0,#0x3    @ 080cbfda c000
    orrs r0,r4    @ 080cbfdc 2043
    lsls r0,r0,#0x5    @ 080cbfde 4001
    ldr r1, DAT_080cc0ac                     @ 080cbfe0 3249
    ldrh r6,[r2,#0x0]                        @ 080cbfe2 1688
    ands r1,r6    @ 080cbfe4 3140
    orrs r1,r0    @ 080cbfe6 0143
    strh r1,[r2,#0x0]                        @ 080cbfe8 1180
    movs r0,#0x0    @ 080cbfea 0020
    .hword 0x4682    @ 080cbfec 8246
    ldrb r1,[r2,#0x0]                        @ 080cbfee 1178
    ands r3,r1    @ 080cbff0 0b40
    lsls r3,r3,#0x3    @ 080cbff2 db00
    orrs r3,r4    @ 080cbff4 2343
    cmp r3,#0x0                              @ 080cbff6 002b
    bne LAB_080cbffc                         @ 080cbff8 00d1
    b LAB_080cc14e                           @ 080cbffa a8e0
LAB_080cbffc:
    ldr r2, DAT_080cc088                     @ 080cbffc 224a
    str r2,[sp,#0x124]                       @ 080cbffe 4992
    movs r3,#0x0    @ 080cc000 0023
    str r3,[sp,#0x128]                       @ 080cc002 4a93
    ldr r5, DAT_080cc0b0                     @ 080cc004 2a4d
    str r5,[sp,#0x12c]                       @ 080cc006 4b95
    add r7,sp,#0x100                         @ 080cc008 40af
LAB_080cc00a:
    .hword 0x4656    @ 080cc00a 5646
    lsls r1,r6,#0x1    @ 080cc00c 7100
    ldr r2, DAT_080cc088                     @ 080cc00e 1e4a
    movs r3,#0xa0    @ 080cc010 a023
    lsls r3,r3,#0x6    @ 080cc012 9b01
    adds r0,r2,r3    @ 080cc014 d018
    adds r0,r1,r0    @ 080cc016 0818
    strh r6,[r0,#0x0]                        @ 080cc018 0680
    ldr r5, DAT_080cc0b4                     @ 080cc01a 264d
    adds r1,r1,r5    @ 080cc01c 4919
    .hword 0x4656    @ 080cc01e 5646
    strh r6,[r1,#0x0]                        @ 080cc020 0e80
    ldr r1,[sp,#0x12c]                       @ 080cc022 4b99
    ldr r0,[r1,#0x0]                         @ 080cc024 0868
    lsls r4,r0,#0x2    @ 080cc026 8400
    lsrs r4,r4,#0x18    @ 080cc028 240e
    lsls r4,r4,#0x1    @ 080cc02a 6400
    lsls r0,r0,#0x12    @ 080cc02c 8004
    lsrs r0,r0,#0x1f    @ 080cc02e c00f
    adds r4,r4,r0    @ 080cc030 2418
    adds r0,r4,#0x0    @ 080cc032 201c
    bl ensure_card_id_cache_entry            @ 080cc034 00f048fc
    adds r5,r0,#0x0    @ 080cc038 051c
    adds r0,r4,#0x0    @ 080cc03a 201c
    bl find_zone_descriptor_by_slot_id       @ 080cc03c 64f7d4fe
    adds r4,r0,#0x0    @ 080cc040 041c
    lsls r0,r4,#0x18    @ 080cc042 2006
    lsrs r1,r0,#0x18    @ 080cc044 010e
    .hword 0x4689    @ 080cc046 8946
    lsls r0,r4,#0x10    @ 080cc048 2004
    lsrs r0,r0,#0x18    @ 080cc04a 000e
    adds r6,r0,#0x0    @ 080cc04c 061c
    lsrs r2,r4,#0x10    @ 080cc04e 220c
    .hword 0x4690    @ 080cc050 9046
    cmp r5,#0x0                              @ 080cc052 002d
    bne LAB_080cc070                         @ 080cc054 0cd1
    lsls r4,r0,#0x8    @ 080cc056 0402
    orrs r4,r1    @ 080cc058 0c43
    movs r0,#0x80    @ 080cc05a 8020
    lsls r0,r0,#0xd    @ 080cc05c 4003
    orrs r4,r0    @ 080cc05e 0443
    ldr r3,[sp,#0x12c]                       @ 080cc060 4b9b
    ldrh r3,[r3,#0x0]                        @ 080cc062 1b88
    lsls r0,r3,#0x13    @ 080cc064 d804
    lsrs r0,r0,#0x13    @ 080cc066 c00c
    bl internal_card_id_to_card_id           @ 080cc068 22f080fb
    lsls r0,r0,#0x10    @ 080cc06c 0004
    lsrs r5,r0,#0x10    @ 080cc06e 050c
LAB_080cc070:
    cmp r6,#0xa                              @ 080cc070 0a2e
    bgt LAB_080cc0b8                         @ 080cc072 21dc
    cmp r6,#0x0                              @ 080cc074 002e
    blt LAB_080cc0b8                         @ 080cc076 1fdb
    .hword 0x4640    @ 080cc078 4046
    adds r1,r6,r0    @ 080cc07a 3118
    .hword 0x4648    @ 080cc07c 4846
    adds r2,r7,#0x0    @ 080cc07e 3a1c
    bl eval_slot_score_entry_full            @ 080cc080 6bf71eff
    str r5,[r7,#0x0]                         @ 080cc084 3d60
    b LAB_080cc104                           @ 080cc086 3de0
DAT_080cc088:
    .word  0x02020160                     @ 080cc088 60010202
DAT_080cc08c:
    .word  0x00002f5c                     @ 080cc08c 5c2f0000
DAT_080cc090:
    .word  0x00002f50                     @ 080cc090 502f0000
DAT_080cc094:
    .word  0xffe01fff                     @ 080cc094 ff1fe0ff
DAT_080cc098:
    .word  0x00002f51                     @ 080cc098 512f0000
DAT_080cc09c:
    .word  0x02023130                     @ 080cc09c 30310202
DAT_080cc0a0:
    .word  0x00000215                     @ 080cc0a0 15020000
DAT_080cc0a4:
    .word  0x00002f57                     @ 080cc0a4 572f0000
DAT_080cc0a8:
    .word  0x00002f58                     @ 080cc0a8 582f0000
DAT_080cc0ac:
    .word  0xffffe01f                     @ 080cc0ac 1fe0ffff
DAT_080cc0b0:
    .word  0x0201e500                     @ 080cc0b0 00e50102
DAT_080cc0b4:
    .word  0x02022d60                     @ 080cc0b4 602d0202
LAB_080cc0b8:
    str r5,[r7,#0x0]                         @ 080cc0b8 3d60
    movs r0,#0xb    @ 080cc0ba 0b20
    adds r2,r5,#0x0    @ 080cc0bc 2a1c
    muls r2,r0    @ 080cc0be 4243
    adds r0,r2,#0x6    @ 080cc0c0 901d
    lsls r0,r0,#0x1    @ 080cc0c2 4000
    ldr r1, PTR_card_stats_table_080cc174    @ 080cc0c4 2b49
    adds r0,r0,r1    @ 080cc0c6 4018
    ldrh r0,[r0,#0x0]                        @ 080cc0c8 0088
    str r0,[r7,#0x4]                         @ 080cc0ca 7860
    adds r0,r2,#0x7    @ 080cc0cc d01d
    lsls r0,r0,#0x1    @ 080cc0ce 4000
    adds r0,r0,r1    @ 080cc0d0 4018
    ldrh r1,[r0,#0x0]                        @ 080cc0d2 0188
    str r1,[r7,#0x8]                         @ 080cc0d4 b960
    movs r0,#0x1    @ 080cc0d6 0120
    lsls r0,r1    @ 080cc0d8 8840
    str r0,[r7,#0xc]                         @ 080cc0da f860
    adds r0,r2,#0x5    @ 080cc0dc 501d
    lsls r0,r0,#0x1    @ 080cc0de 4000
    ldr r3, PTR_card_stats_table_080cc174    @ 080cc0e0 244b
    adds r0,r0,r3    @ 080cc0e2 c018
    ldrh r0,[r0,#0x0]                        @ 080cc0e4 0088
    str r0,[r7,#0x10]                        @ 080cc0e6 3861
    adds r0,r2,#0x3    @ 080cc0e8 d01c
    lsls r0,r0,#0x1    @ 080cc0ea 4000
    adds r0,r0,r3    @ 080cc0ec c018
    movs r5,#0x0    @ 080cc0ee 0025
    ldrsh r1,[r0,r5]                         @ 080cc0f0 415f
    str r1,[r7,#0x14]                        @ 080cc0f2 7961
    adds r2,#0x4    @ 080cc0f4 0432
    lsls r2,r2,#0x1    @ 080cc0f6 5200
    adds r2,r2,r3    @ 080cc0f8 d218
    movs r6,#0x0    @ 080cc0fa 0026
    ldrsh r0,[r2,r6]                         @ 080cc0fc 905f
    str r0,[r7,#0x18]                        @ 080cc0fe b861
    str r1,[r7,#0x1c]                        @ 080cc100 f961
    str r0,[r7,#0x20]                        @ 080cc102 3862
LAB_080cc104:
    ldr r1,[sp,#0x124]                       @ 080cc104 4999
    add r0,sp,#0x100                         @ 080cc106 40a8
    ldmia r0!,{r2,r3,r5}                     @ 080cc108 2cc8
    stmia r1!,{r2,r3,r5}                     @ 080cc10a 2cc1
    ldmia r0!,{r2,r3,r6}                     @ 080cc10c 4cc8
    stmia r1!,{r2,r3,r6}                     @ 080cc10e 4cc1
    ldmia r0!,{r2,r5,r6}                     @ 080cc110 64c8
    stmia r1!,{r2,r5,r6}                     @ 080cc112 64c1
    ldr r0, DAT_080cc178                     @ 080cc114 1848
    adds r0,#0x24    @ 080cc116 2430
    ldr r3,[sp,#0x128]                       @ 080cc118 4a9b
    adds r0,r3,r0    @ 080cc11a 1818
    str r4,[r0,#0x0]                         @ 080cc11c 0460
    ldr r5,[sp,#0x124]                       @ 080cc11e 499d
    adds r5,#0x28    @ 080cc120 2835
    str r5,[sp,#0x124]                       @ 080cc122 4995
    adds r3,#0x28    @ 080cc124 2833
    str r3,[sp,#0x128]                       @ 080cc126 4a93
    ldr r6,[sp,#0x12c]                       @ 080cc128 4b9e
    adds r6,#0x4    @ 080cc12a 0436
    str r6,[sp,#0x12c]                       @ 080cc12c 4b96
    movs r0,#0x1    @ 080cc12e 0120
    add r10,r0                               @ 080cc130 8244
    ldr r1, DAT_080cc178                     @ 080cc132 1149
    ldr r2, DAT_080cc17c                     @ 080cc134 114a
    adds r0,r1,r2    @ 080cc136 8818
    ldrb r0,[r0,#0x0]                        @ 080cc138 0078
    lsrs r1,r0,#0x5    @ 080cc13a 4109
    movs r0,#0x1f    @ 080cc13c 1f20
    ldr r3, DAT_080cc180                     @ 080cc13e 104b
    ldrb r3,[r3,#0x0]                        @ 080cc140 1b78
    ands r0,r3    @ 080cc142 1840
    lsls r0,r0,#0x3    @ 080cc144 c000
    orrs r0,r1    @ 080cc146 0843
    cmp r10,r0                               @ 080cc148 8245
    bge LAB_080cc14e                         @ 080cc14a 00da
    b LAB_080cc00a                           @ 080cc14c 5de7
LAB_080cc14e:
    ldr r4, DAT_080cc184                     @ 080cc14e 0d4c
    ldr r1,[r4,#0x4]                         @ 080cc150 6168
    cmp r1,#0x4                              @ 080cc152 0429
    bhi LAB_080cc194                         @ 080cc154 1ed8
    subs r0,r1,#0x1    @ 080cc156 481e
    lsls r3,r0,#0x1    @ 080cc158 4300
    ldr r5, DAT_080cc188                     @ 080cc15a 0b4d
    adds r2,r3,r5    @ 080cc15c 5a19
    ldr r0, DAT_080cc18c                     @ 080cc15e 0b48
    ldr r0,[r0,#0x4]                         @ 080cc160 4068
    movs r1,#0x1    @ 080cc162 0121
    eors r0,r1    @ 080cc164 4840
    ldr r1,[r4,#0x0]                         @ 080cc166 2168
    cmp r1,r0                                @ 080cc168 8142
    bne LAB_080cc170                         @ 080cc16a 01d1
    ldr r6, DAT_080cc190                     @ 080cc16c 084e
    adds r2,r3,r6    @ 080cc16e 9a19
LAB_080cc170:
    adds r0,r2,#0x0    @ 080cc170 101c
    b LAB_080cc1de                           @ 080cc172 34e0
PTR_card_stats_table_080cc174:
    .word  card_stats_table               @ 080cc174 b8698109
DAT_080cc178:
    .word  0x02020160                     @ 080cc178 60010202
DAT_080cc17c:
    .word  0x00002f57                     @ 080cc17c 572f0000
DAT_080cc180:
    .word  0x020230b8                     @ 080cc180 b8300202
DAT_080cc184:
    .word  0x0201e4f0                     @ 080cc184 f0e40102
DAT_080cc188:
    .word  0x00000246                     @ 080cc188 46020000
DAT_080cc18c:
    .word  0x0201e2a0                     @ 080cc18c a0e20102
DAT_080cc190:
    .word  0x00000247                     @ 080cc190 47020000
LAB_080cc194:
    cmp r1,#0x5                              @ 080cc194 0529
    bne LAB_080cc1a0                         @ 080cc196 03d1
    ldr r0, DAT_080cc19c                     @ 080cc198 0048
    b LAB_080cc1de                           @ 080cc19a 20e0
DAT_080cc19c:
    .word  0x0000024e                     @ 080cc19c 4e020000
LAB_080cc1a0:
    adds r0,r1,#0x0    @ 080cc1a0 081c
    subs r0,#0x8    @ 080cc1a2 0838
    cmp r0,#0x1e                             @ 080cc1a4 1e28
    bhi LAB_080cc1b8                         @ 080cc1a6 07d8
    movs r0,#0x94    @ 080cc1a8 9420
    lsls r0,r0,#0x2    @ 080cc1aa 8000
    bl resolve_game_str_ptr                  @ 080cc1ac 22f052fd
    adds r1,r0,#0x0    @ 080cc1b0 011c
    ldr r2,[r4,#0x4]                         @ 080cc1b2 6268
    subs r2,#0x6    @ 080cc1b4 063a
    b LAB_080cc1cc                           @ 080cc1b6 09e0
LAB_080cc1b8:
    adds r0,r1,#0x0    @ 080cc1b8 081c
    subs r0,#0x29    @ 080cc1ba 2938
    cmp r0,#0x1e                             @ 080cc1bc 1e28
    bhi LAB_080cc1dc                         @ 080cc1be 0dd8
    ldr r0, DAT_080cc1d8                     @ 080cc1c0 0548
    bl resolve_game_str_ptr                  @ 080cc1c2 22f047fd
    adds r1,r0,#0x0    @ 080cc1c6 011c
    ldr r2,[r4,#0x4]                         @ 080cc1c8 6268
    subs r2,#0x27    @ 080cc1ca 273a
LAB_080cc1cc:
    .hword 0x4668    @ 080cc1cc 6846
    bl expand_format_decimal_to_buf          @ 080cc1ce 29f02bf8
    .hword 0x466c    @ 080cc1d2 6c46
    b LAB_080cc1e4                           @ 080cc1d4 06e0
    .zero  0x2
DAT_080cc1d8:
    .word  0x00000251                     @ 080cc1d8 51020000
LAB_080cc1dc:
    ldr r0, DAT_080cc200                     @ 080cc1dc 0848
LAB_080cc1de:
    bl resolve_game_str_ptr                  @ 080cc1de 22f039fd
    adds r4,r0,#0x0    @ 080cc1e2 041c
LAB_080cc1e4:
    cmp r4,#0x0                              @ 080cc1e4 002c
    beq LAB_080cc1f0                         @ 080cc1e6 03d0
    ldr r0, DAT_080cc204                     @ 080cc1e8 0648
    adds r1,r4,#0x0    @ 080cc1ea 211c
    bl copy_cstr_to_buf                      @ 080cc1ec 28f032ff
LAB_080cc1f0:
    add sp,#0x130                            @ 080cc1f0 4cb0
    pop {r3,r4,r5}                           @ 080cc1f2 38bc
    .hword 0x4698    @ 080cc1f4 9846
    .hword 0x46a1    @ 080cc1f6 a146
    .hword 0x46aa    @ 080cc1f8 aa46
    pop {r4,r5,r6,r7}                        @ 080cc1fa f0bc
    pop {r0}                                 @ 080cc1fc 01bc
    bx r0                                    @ 080cc1fe 0047
DAT_080cc200:
    .word  0x0000024f                     @ 080cc200 4f020000
DAT_080cc204:
    .word  0x02022fac                     @ 080cc204 ac2f0202

@ Renders zone card detail panel and advances state counter. Called by tick_zone_display_frame (0x080cc528) in zone frame tick. Body: push {lr}; bl render_zone_card_detail_panel (no params); ldr gDuelCtx+0x2f4d; ldrb state; adds #1; strb state+1; movs r0,#1; pop bx. Fixed return 1. Side effects: strb gDuelCtx+0x2f4d (state counter +1). Constants: gDuelCtx=0x02020160, state_offset=0x2f4d.
tick_zone_detail_render_step:
    push {lr}                                @ 080cc208 00b5
    bl render_zone_card_detail_panel         @ 080cc20a 04f04bfb
    ldr r0, DWORD_080cc220                   @ 080cc20e 0448
    ldr r1, DWORD_080cc224                   @ 080cc210 0449
    adds r0,r0,r1    @ 080cc212 4018
    ldrb r1,[r0,#0x0]                        @ 080cc214 0178
    adds r1,#0x1    @ 080cc216 0131
    strb r1,[r0,#0x0]                        @ 080cc218 0170
    movs r0,#0x1    @ 080cc21a 0120
    pop {r1}                                 @ 080cc21c 02bc
    bx r1                                    @ 080cc21e 0847
DWORD_080cc220:
    .word  0x02020160                     @ 080cc220 60010202
DWORD_080cc224:
    .word  0x00002f4d                     @ 080cc224 4d2f0000

@ Dispatches zone detail panel single-frame tick by animation type state. Called by tick_zone_display_frame (0x080cc528) in zone frame total dispatcher. Reads gDuelCtx+0x2f53/0x2f54 type_combined (bits[7:5]<<3 | bits[4:0]); type>0 and <=5 selects ROM ptr table 0x0988b434; type==0 selects 0x0988b178. Reads gDuelCtx+0x2f4d as sub_state; if sub_state in [0..6]: computes VRAM row 0x0600f00a+((8-sub_state)<<6), calls apply_palette_offset_to_tile_row twice (palette row writes); sub_state++ strb; returns 0. If sub_state>6: reads gDuelCtx+0x2f55/0x2f56 type_combined2 for second dispatch: 0->dispatch_zone_card_display_by_mode; nonzero->same with check_zone_slot_attr_visible. Side effects: strb gDuelCtx+0x2f4d (+1); VRAM 0x0600f00a palette row writes. Constants: gDuelCtx=0x02020160, VRAM_base=0x0600f00a, table_hi=0x0988b434, table_lo=0x0988b178, sub_state_offset=0x2f4d.
tick_zone_detail_panel_by_anim_state:
    push {r4,r5,r6,r7,lr}                    @ 080cc228 f0b5
    sub sp,#0x4                              @ 080cc22a 81b0
    ldr r1, DWORD_080cc25c                   @ 080cc22c 0b49
    ldr r2, DWORD_080cc260                   @ 080cc22e 0c4a
    adds r0,r1,r2    @ 080cc230 8818
    ldrb r0,[r0,#0x0]                        @ 080cc232 0078
    lsrs r3,r0,#0x5    @ 080cc234 4309
    ldr r0, DWORD_080cc264                   @ 080cc236 0b48
    adds r2,r1,r0    @ 080cc238 0a18
    movs r4,#0x1f    @ 080cc23a 1f24
    adds r0,r4,#0x0    @ 080cc23c 201c
    ldrb r2,[r2,#0x0]                        @ 080cc23e 1278
    ands r0,r2    @ 080cc240 1040
    lsls r0,r0,#0x3    @ 080cc242 c000
    orrs r0,r3    @ 080cc244 1843
    adds r3,r1,#0x0    @ 080cc246 0b1c
    cmp r0,#0x0                              @ 080cc248 0028
    beq LAB_080cc26c                         @ 080cc24a 0fd0
    ldr r1, DWORD_080cc268                   @ 080cc24c 0649
    adds r0,r3,r1    @ 080cc24e 5818
    ldrh r0,[r0,#0x0]                        @ 080cc250 0088
    lsls r0,r0,#0x13    @ 080cc252 c004
    lsrs r0,r0,#0x18    @ 080cc254 000e
    cmp r0,#0x5                              @ 080cc256 0528
    bgt LAB_080cc286                         @ 080cc258 15dc
    b LAB_080cc298                           @ 080cc25a 1de0
DWORD_080cc25c:
    .word  0x02020160                     @ 080cc25c 60010202
DWORD_080cc260:
    .word  0x00002f53                     @ 080cc260 532f0000
DWORD_080cc264:
    .word  0x00002f54                     @ 080cc264 542f0000
DWORD_080cc268:
    .word  0x00002f58                     @ 080cc268 582f0000
LAB_080cc26c:
    ldr r2, DWORD_080cc28c                   @ 080cc26c 074a
    adds r0,r3,r2    @ 080cc26e 9818
    ldrb r0,[r0,#0x0]                        @ 080cc270 0078
    lsrs r2,r0,#0x5    @ 080cc272 4209
    ldr r0, DWORD_080cc290                   @ 080cc274 0648
    adds r1,r3,r0    @ 080cc276 1918
    adds r0,r4,#0x0    @ 080cc278 201c
    ldrb r1,[r1,#0x0]                        @ 080cc27a 0978
    ands r0,r1    @ 080cc27c 0840
    lsls r0,r0,#0x3    @ 080cc27e c000
    orrs r0,r2    @ 080cc280 1043
    cmp r0,#0x5                              @ 080cc282 0528
    ble LAB_080cc298                         @ 080cc284 08dd
LAB_080cc286:
    ldr r6, DWORD_080cc294                   @ 080cc286 034e
    b LAB_080cc29a                           @ 080cc288 07e0
    .zero  0x2
DWORD_080cc28c:
    .word  0x00002f57                     @ 080cc28c 572f0000
DWORD_080cc290:
    .word  0x00002f58                     @ 080cc290 582f0000
DWORD_080cc294:
    .word  0x0988b434                     @ 080cc294 34b48809
LAB_080cc298:
    ldr r6, DWORD_080cc2f8                   @ 080cc298 174e
LAB_080cc29a:
    ldr r1, DWORD_080cc2fc                   @ 080cc29a 1849
    adds r7,r3,r1    @ 080cc29c 5f18
    ldrb r2,[r7,#0x0]                        @ 080cc29e 3a78
    adds r0,r2,#0x0    @ 080cc2a0 101c
    cmp r0,#0x6                              @ 080cc2a2 0628
    bgt LAB_080cc308                         @ 080cc2a4 30dc
    cmp r0,#0x0                              @ 080cc2a6 0028
    blt LAB_080cc308                         @ 080cc2a8 2edb
    movs r0,#0x8    @ 080cc2aa 0820
    subs r0,r0,r2    @ 080cc2ac 801a
    lsls r0,r0,#0x10    @ 080cc2ae 0004
    lsrs r0,r0,#0xa    @ 080cc2b0 800a
    ldr r1, DWORD_080cc300                   @ 080cc2b2 1349
    adds r0,r0,r1    @ 080cc2b4 4018
    adds r2,#0x1    @ 080cc2b6 0132
    lsls r2,r2,#0x18    @ 080cc2b8 1206
    movs r5,#0x19    @ 080cc2ba 1925
    lsrs r2,r2,#0x10    @ 080cc2bc 120c
    orrs r2,r5    @ 080cc2be 2a43
    movs r4,#0xc3    @ 080cc2c0 c324
    lsls r4,r4,#0x1    @ 080cc2c2 6400
    str r4,[sp,#0x0]                         @ 080cc2c4 0094
    adds r1,r6,#0x0    @ 080cc2c6 311c
    movs r3,#0xb    @ 080cc2c8 0b23
    bl apply_palette_offset_to_tile_row      @ 080cc2ca 22f06df8
    ldr r0, DWORD_080cc304                   @ 080cc2ce 0d48
    ldrb r2,[r7,#0x0]                        @ 080cc2d0 3a78
    movs r1,#0xd    @ 080cc2d2 0d21
    subs r1,r1,r2    @ 080cc2d4 891a
    movs r3,#0x32    @ 080cc2d6 3223
    muls r1,r3    @ 080cc2d8 5943
    adds r1,r6,r1    @ 080cc2da 7118
    adds r2,#0x1    @ 080cc2dc 0132
    lsls r2,r2,#0x18    @ 080cc2de 1206
    lsrs r2,r2,#0x10    @ 080cc2e0 120c
    orrs r2,r5    @ 080cc2e2 2a43
    str r4,[sp,#0x0]                         @ 080cc2e4 0094
    movs r3,#0xb    @ 080cc2e6 0b23
    bl apply_palette_offset_to_tile_row      @ 080cc2e8 22f05ef8
    ldrb r0,[r7,#0x0]                        @ 080cc2ec 3878
    adds r0,#0x1    @ 080cc2ee 0130
    strb r0,[r7,#0x0]                        @ 080cc2f0 3870
    movs r0,#0x0    @ 080cc2f2 0020
    b LAB_080cc332                           @ 080cc2f4 1de0
    .zero  0x2
DWORD_080cc2f8:
    .word  0x0988b178                     @ 080cc2f8 78b18809
DWORD_080cc2fc:
    .word  0x00002f4d                     @ 080cc2fc 4d2f0000
DWORD_080cc300:
    .word  0x0600f00a                     @ 080cc300 0af00006
DWORD_080cc304:
    .word  0x0600f24a                     @ 080cc304 4af20006
LAB_080cc308:
    ldr r2, DWORD_080cc33c                   @ 080cc308 0c4a
    adds r0,r3,r2    @ 080cc30a 9818
    ldr r0,[r0,#0x0]                         @ 080cc30c 0068
    lsls r0,r0,#0xb    @ 080cc30e c002
    lsrs r4,r0,#0x18    @ 080cc310 040e
    adds r2,#0x2    @ 080cc312 0232
    adds r1,r3,r2    @ 080cc314 9918
    ldrh r1,[r1,#0x0]                        @ 080cc316 0988
    lsls r1,r1,#0x13    @ 080cc318 c904
    lsrs r2,r1,#0x18    @ 080cc31a 0a0e
    adds r4,r4,r2    @ 080cc31c a418
    lsrs r0,r0,#0x18    @ 080cc31e 000e
    adds r1,r2,#0x0    @ 080cc320 111c
    adds r0,r0,r1    @ 080cc322 4018
    bl check_zone_slot_attr_visible          @ 080cc324 04f02efa
    adds r1,r0,#0x0    @ 080cc328 011c
    adds r0,r4,#0x0    @ 080cc32a 201c
    bl dispatch_zone_card_display_by_mode    @ 080cc32c 04f074fa
    movs r0,#0x1    @ 080cc330 0120
LAB_080cc332:
    add sp,#0x4                              @ 080cc332 01b0
    pop {r4,r5,r6,r7}                        @ 080cc334 f0bc
    pop {r1}                                 @ 080cc336 02bc
    bx r1                                    @ 080cc338 0847
    .zero  0x2
DWORD_080cc33c:
    .word  0x00002f54                     @ 080cc33c 542f0000

@ Bool-invert wrapper around tick_zone_card_list_view; propagates result upward. Called by tick_zone_display_frame (0x080cc528) in zone frame tick dispatcher. Body: push {lr}; bl tick_zone_card_list_view (FUN_080d2ef4); cmp r0,#0 beq LAB_080cc34e -> r0==0 returns 1 (pending); r0!=0 returns 0 (done). Converts tick_zone_card_list_view result (nonzero=done/exit) to 'is_pending' semantics (0=done, 1=continue). Side effects: none (only propagates return value). Constants: none.
invert_zone_tick_result:
    push {lr}                                @ 080cc340 00b5
    bl tick_zone_card_list_view              @ 080cc342 06f0d7fd
    cmp r0,#0x0                              @ 080cc346 0028
    beq LAB_080cc34e                         @ 080cc348 01d0
    movs r0,#0x0    @ 080cc34a 0020
    b LAB_080cc350                           @ 080cc34c 00e0
LAB_080cc34e:
    movs r0,#0x1    @ 080cc34e 0120
LAB_080cc350:
    pop {r1}                                 @ 080cc350 02bc
    bx r1                                    @ 080cc352 0847

@ Single-frame update of zone field info panel: animation tile writes and field info render. Called by tick_zone_display_frame (0x080cc528). Reads gPrng+0x1886*2 tile control bits: bit7=flip flag (r9), bits[6:0]=r7, bits[14:8]=r6. Reads gDuelCtx+0x2f53/0x2f54 type_combined; selects ROM table 0x0988b434 or 0x0988b178. Reads gDuelCtx+0x2f4d sub_state: 0->double loop strh #0 clearing VRAM 0x0600f00a block; 1..6->calls apply_palette_offset_to_tile_row twice per step; 7->calls render_duel_field_zone_info + copy_bytes_by_halfword (0x050002e0 <- 0x0985329c, 0x20 bytes). Each case sub_state++ strb. Returns 0 or 1. Side effects: strb gDuelCtx+0x2f4d; strh VRAM 0x0600f00a area (zero or palette); OBJ PAL 0x050002e0 += 0x20 bytes (state 7 path). Constants: gDuelCtx=0x02020160, state_offset=0x2f4d, VRAM_base=0x0600f00a, OBJ_PAL_dst=0x050002e0, pal_src=0x0985329c.
tick_zone_field_info_panel:
    push {r4,r5,r6,r7,lr}                    @ 080cc354 f0b5
    .hword 0x4657    @ 080cc356 5746
    .hword 0x464e    @ 080cc358 4e46
    .hword 0x4645    @ 080cc35a 4546
    push {r5,r6,r7}                          @ 080cc35c e0b4
    sub sp,#0x4                              @ 080cc35e 81b0
    ldr r5, DWORD_080cc3b4                   @ 080cc360 144d
    ldr r0, DWORD_080cc3b8                   @ 080cc362 1548
    movs r1,#0x84    @ 080cc364 8421
    lsls r1,r1,#0x2    @ 080cc366 8900
    adds r0,r0,r1    @ 080cc368 4018
    ldrh r2,[r0,#0x0]                        @ 080cc36a 0288
    adds r1,r2,#0x0    @ 080cc36c 111c
    movs r0,#0x80    @ 080cc36e 8020
    ands r0,r1    @ 080cc370 0840
    lsls r0,r0,#0x18    @ 080cc372 0006
    lsrs r0,r0,#0x1f    @ 080cc374 c00f
    .hword 0x4681    @ 080cc376 8146
    movs r0,#0x7f    @ 080cc378 7f20
    adds r7,r0,#0x0    @ 080cc37a 071c
    ands r7,r1    @ 080cc37c 0f40
    lsrs r6,r2,#0x8    @ 080cc37e 160a
    ands r6,r0    @ 080cc380 0640
    ldr r1, DWORD_080cc3bc                   @ 080cc382 0e49
    ldr r2, DWORD_080cc3c0                   @ 080cc384 0e4a
    adds r0,r1,r2    @ 080cc386 8818
    ldrb r0,[r0,#0x0]                        @ 080cc388 0078
    lsrs r3,r0,#0x5    @ 080cc38a 4309
    ldr r0, DWORD_080cc3c4                   @ 080cc38c 0d48
    adds r2,r1,r0    @ 080cc38e 0a18
    movs r4,#0x1f    @ 080cc390 1f24
    adds r0,r4,#0x0    @ 080cc392 201c
    ldrb r2,[r2,#0x0]                        @ 080cc394 1278
    ands r0,r2    @ 080cc396 1040
    lsls r0,r0,#0x3    @ 080cc398 c000
    orrs r0,r3    @ 080cc39a 1843
    .hword 0x4688    @ 080cc39c 8846
    cmp r0,#0x0                              @ 080cc39e 0028
    beq LAB_080cc3cc                         @ 080cc3a0 14d0
    ldr r0, DWORD_080cc3c8                   @ 080cc3a2 0948
    add r0,r8                                @ 080cc3a4 4044
    ldrh r0,[r0,#0x0]                        @ 080cc3a6 0088
    lsls r0,r0,#0x13    @ 080cc3a8 c004
    lsrs r0,r0,#0x18    @ 080cc3aa 000e
    cmp r0,#0x5                              @ 080cc3ac 0528
    bgt LAB_080cc3e6                         @ 080cc3ae 1adc
    b LAB_080cc3f8                           @ 080cc3b0 22e0
    .zero  0x2
DWORD_080cc3b4:
    .word  0x0600f00a                     @ 080cc3b4 0af00006
DWORD_080cc3b8:
    .word  0x02023130                     @ 080cc3b8 30310202
DWORD_080cc3bc:
    .word  0x02020160                     @ 080cc3bc 60010202
DWORD_080cc3c0:
    .word  0x00002f53                     @ 080cc3c0 532f0000
DWORD_080cc3c4:
    .word  0x00002f54                     @ 080cc3c4 542f0000
DWORD_080cc3c8:
    .word  0x00002f58                     @ 080cc3c8 582f0000
LAB_080cc3cc:
    ldr r0, DWORD_080cc3ec                   @ 080cc3cc 0748
    add r0,r8                                @ 080cc3ce 4044
    ldrb r0,[r0,#0x0]                        @ 080cc3d0 0078
    lsrs r2,r0,#0x5    @ 080cc3d2 4209
    ldr r1, DWORD_080cc3f0                   @ 080cc3d4 0649
    add r1,r8                                @ 080cc3d6 4144
    adds r0,r4,#0x0    @ 080cc3d8 201c
    ldrb r1,[r1,#0x0]                        @ 080cc3da 0978
    ands r0,r1    @ 080cc3dc 0840
    lsls r0,r0,#0x3    @ 080cc3de c000
    orrs r0,r2    @ 080cc3e0 1043
    cmp r0,#0x5                              @ 080cc3e2 0528
    ble LAB_080cc3f8                         @ 080cc3e4 08dd
LAB_080cc3e6:
    ldr r1, DWORD_080cc3f4                   @ 080cc3e6 0349
    .hword 0x468a    @ 080cc3e8 8a46
    b LAB_080cc3fc                           @ 080cc3ea 07e0
DWORD_080cc3ec:
    .word  0x00002f57                     @ 080cc3ec 572f0000
DWORD_080cc3f0:
    .word  0x00002f58                     @ 080cc3f0 582f0000
DWORD_080cc3f4:
    .word  0x0988b434                     @ 080cc3f4 34b48809
LAB_080cc3f8:
    ldr r2, DWORD_080cc410                   @ 080cc3f8 054a
    .hword 0x4692    @ 080cc3fa 9246
LAB_080cc3fc:
    ldr r4, DWORD_080cc414                   @ 080cc3fc 054c
    add r4,r8                                @ 080cc3fe 4444
    ldrb r0,[r4,#0x0]                        @ 080cc400 2078
    cmp r0,#0x6                              @ 080cc402 0628
    bgt LAB_080cc418                         @ 080cc404 08dc
    cmp r0,#0x1                              @ 080cc406 0128
    bge LAB_080cc43a                         @ 080cc408 17da
    cmp r0,#0x0                              @ 080cc40a 0028
    beq LAB_080cc41e                         @ 080cc40c 07d0
    b LAB_080cc514                           @ 080cc40e 81e0
DWORD_080cc410:
    .word  0x0988b178                     @ 080cc410 78b18809
DWORD_080cc414:
    .word  0x00002f4d                     @ 080cc414 4d2f0000
LAB_080cc418:
    cmp r0,#0x7                              @ 080cc418 0728
    beq LAB_080cc4ec                         @ 080cc41a 67d0
    b LAB_080cc514                           @ 080cc41c 7ae0
LAB_080cc41e:
    movs r3,#0x0    @ 080cc41e 0023
    movs r2,#0x1    @ 080cc420 0122
LAB_080cc422:
    adds r1,r5,#0x0    @ 080cc422 291c
    adds r1,#0x40    @ 080cc424 4031
    adds r0,r5,#0x0    @ 080cc426 281c
    adds r0,#0x30    @ 080cc428 3030
LAB_080cc42a:
    strh r3,[r0,#0x0]                        @ 080cc42a 0380
    subs r0,#0x2    @ 080cc42c 0238
    cmp r0,r5                                @ 080cc42e a842
    bge LAB_080cc42a                         @ 080cc430 fbda
    adds r5,r1,#0x0    @ 080cc432 0d1c
    subs r2,#0x1    @ 080cc434 013a
    cmp r2,#0x0                              @ 080cc436 002a
    bge LAB_080cc422                         @ 080cc438 f3da
LAB_080cc43a:
    ldr r7, DWORD_080cc4dc                   @ 080cc43a 284f
    ldr r0, DWORD_080cc4e0                   @ 080cc43c 2848
    adds r5,r7,r0    @ 080cc43e 3d18
    ldrb r2,[r5,#0x0]                        @ 080cc440 2a78
    adds r0,r2,#0x3    @ 080cc442 d01c
    lsls r0,r0,#0x6    @ 080cc444 8001
    ldr r6, DWORD_080cc4e4                   @ 080cc446 274e
    adds r0,r0,r6    @ 080cc448 8019
    movs r4,#0x6    @ 080cc44a 0624
    subs r2,r4,r2    @ 080cc44c a21a
    lsls r2,r2,#0x18    @ 080cc44e 1206
    movs r1,#0x19    @ 080cc450 1921
    .hword 0x4689    @ 080cc452 8946
    lsrs r2,r2,#0x10    @ 080cc454 120c
    .hword 0x4649    @ 080cc456 4946
    orrs r2,r1    @ 080cc458 0a43
    movs r1,#0xc3    @ 080cc45a c321
    lsls r1,r1,#0x1    @ 080cc45c 4900
    .hword 0x4688    @ 080cc45e 8846
    str r1,[sp,#0x0]                         @ 080cc460 0091
    .hword 0x4651    @ 080cc462 5146
    movs r3,#0xb    @ 080cc464 0b23
    bl apply_palette_offset_to_tile_row      @ 080cc466 21f09fff
    ldr r0, DWORD_080cc4e8                   @ 080cc46a 1f48
    ldrb r3,[r5,#0x0]                        @ 080cc46c 2b78
    adds r2,r3,#0x7    @ 080cc46e da1d
    movs r1,#0x32    @ 080cc470 3221
    muls r1,r2    @ 080cc472 5143
    add r1,r10                               @ 080cc474 5144
    subs r4,r4,r3    @ 080cc476 e41a
    lsls r4,r4,#0x18    @ 080cc478 2406
    lsrs r4,r4,#0x10    @ 080cc47a 240c
    .hword 0x464a    @ 080cc47c 4a46
    orrs r4,r2    @ 080cc47e 1443
    .hword 0x4642    @ 080cc480 4246
    str r2,[sp,#0x0]                         @ 080cc482 0092
    adds r2,r4,#0x0    @ 080cc484 221c
    movs r3,#0xb    @ 080cc486 0b23
    bl apply_palette_offset_to_tile_row      @ 080cc488 21f08eff
    ldrb r1,[r5,#0x0]                        @ 080cc48c 2978
    adds r0,r1,#0x2    @ 080cc48e 881c
    lsls r0,r0,#0x6    @ 080cc490 8001
    adds r3,r0,r6    @ 080cc492 8319
    movs r0,#0xf    @ 080cc494 0f20
    subs r0,r0,r1    @ 080cc496 401a
    lsls r0,r0,#0x10    @ 080cc498 0004
    lsrs r0,r0,#0xa    @ 080cc49a 800a
    adds r0,r0,r6    @ 080cc49c 8019
    movs r2,#0x0    @ 080cc49e 0022
    .hword 0x46b8    @ 080cc4a0 b846
    movs r7,#0x0    @ 080cc4a2 0027
LAB_080cc4a4:
    adds r6,r2,#0x1    @ 080cc4a4 561c
    adds r4,r3,#0x0    @ 080cc4a6 1c1c
    adds r4,#0x40    @ 080cc4a8 4034
    adds r5,r0,#0x0    @ 080cc4aa 051c
    adds r5,#0x40    @ 080cc4ac 4035
    adds r1,r0,#0x0    @ 080cc4ae 011c
    adds r0,r3,#0x0    @ 080cc4b0 181c
    movs r2,#0x18    @ 080cc4b2 1822
LAB_080cc4b4:
    strh r7,[r0,#0x0]                        @ 080cc4b4 0780
    strh r7,[r1,#0x0]                        @ 080cc4b6 0f80
    adds r1,#0x2    @ 080cc4b8 0231
    adds r0,#0x2    @ 080cc4ba 0230
    subs r2,#0x1    @ 080cc4bc 013a
    cmp r2,#0x0                              @ 080cc4be 002a
    bge LAB_080cc4b4                         @ 080cc4c0 f8da
    adds r3,r4,#0x0    @ 080cc4c2 231c
    adds r0,r5,#0x0    @ 080cc4c4 281c
    adds r2,r6,#0x0    @ 080cc4c6 321c
    cmp r2,#0x0                              @ 080cc4c8 002a
    ble LAB_080cc4a4                         @ 080cc4ca ebdd
    ldr r1, DWORD_080cc4e0                   @ 080cc4cc 0449
    add r1,r8                                @ 080cc4ce 4144
    ldrb r0,[r1,#0x0]                        @ 080cc4d0 0878
    adds r0,#0x1    @ 080cc4d2 0130
    strb r0,[r1,#0x0]                        @ 080cc4d4 0870
    movs r0,#0x0    @ 080cc4d6 0020
    b LAB_080cc516                           @ 080cc4d8 1de0
    .zero  0x2
DWORD_080cc4dc:
    .word  0x02020160                     @ 080cc4dc 60010202
DWORD_080cc4e0:
    .word  0x00002f4d                     @ 080cc4e0 4d2f0000
DWORD_080cc4e4:
    .word  0x0600f00a                     @ 080cc4e4 0af00006
DWORD_080cc4e8:
    .word  0x0600f24a                     @ 080cc4e8 4af20006
LAB_080cc4ec:
    .hword 0x4648    @ 080cc4ec 4846
    adds r1,r7,#0x0    @ 080cc4ee 391c
    adds r2,r6,#0x0    @ 080cc4f0 321c
    bl render_duel_field_zone_info           @ 080cc4f2 fff751fa
    ldr r0, DWORD_080cc50c                   @ 080cc4f6 0548
    ldr r1, DWORD_080cc510                   @ 080cc4f8 0549
    movs r2,#0x20    @ 080cc4fa 2022
    bl copy_bytes_by_halfword                @ 080cc4fc 28f0d2fc
    ldrb r0,[r4,#0x0]                        @ 080cc500 2078
    adds r0,#0x1    @ 080cc502 0130
    strb r0,[r4,#0x0]                        @ 080cc504 2070
    movs r0,#0x0    @ 080cc506 0020
    b LAB_080cc516                           @ 080cc508 05e0
    .zero  0x2
DWORD_080cc50c:
    .word  0x050002e0                     @ 080cc50c e0020005
DWORD_080cc510:
    .word  0x0985329c                     @ 080cc510 9c328509
LAB_080cc514:
    movs r0,#0x1    @ 080cc514 0120
LAB_080cc516:
    add sp,#0x4                              @ 080cc516 01b0
    pop {r3,r4,r5}                           @ 080cc518 38bc
    .hword 0x4698    @ 080cc51a 9846
    .hword 0x46a1    @ 080cc51c a146
    .hword 0x46aa    @ 080cc51e aa46
    pop {r4,r5,r6,r7}                        @ 080cc520 f0bc
    pop {r1}                                 @ 080cc522 02bc
    bx r1                                    @ 080cc524 0847
    .zero  0x2

@ Top-level zone display frame tick dispatcher; selects one sub-system per frame based on gDuelCtx animation state. Called by FUN_0801e984 (scene main dispatcher). Flow: (1) checks gP1LifePoints+0x1d08 (LP alive); if nonzero reads gPrng+0x85*4 random value, divides by 0x3c=60; if quotient>0xb3=179 sets gPrng+0x23130+0x222 bits |= 0x4. (2) reads gDuelCtx+0x2f4c (animation selector) and dispatches: 0->sort_zone_oam_entries_to_vram + advance state; 1->tick_zone_detail_render_step (0x080cc208); 2->tick_zone_detail_panel_by_anim_state (0x080cc228); 3..6->tick_zone_field_info_panel (0x080cc354); 7->invert_zone_tick_result (0x080cc340). (3) calls sort_zone_oam_entries_to_vram at end. Returns 0 or 1. Side effects: strb gDuelCtx+0x2f4c (selector advance); strb gDuelCtx+0x2f4d; strb gPrng bits (random LP effect); gDuelCtx+0x2f51 &= ~2; gDuelCtx+0x2f52 &= ~5. Constants: gDuelCtx=0x02020160, selector_offset=0x2f4c, gP1LifePoints_LP_offset=0x1d08, gPrng_rand_offset=0x85*4=0x214, rand_threshold=0xb3=179, rand_div=0x3c=60, LP_flag_offset=0x23130+0x222.
tick_zone_display_frame:
    push {r4,r5,lr}                          @ 080cc528 30b5
    ldr r0, PTR_gP1LifePoints_080cc59c       @ 080cc52a 1c48
    ldr r1, DAT_080cc5a0                     @ 080cc52c 1c49
    adds r0,r0,r1    @ 080cc52e 4018
    ldr r0,[r0,#0x0]                         @ 080cc530 0068
    cmp r0,#0x0                              @ 080cc532 0028
    beq LAB_080cc562                         @ 080cc534 15d0
    ldr r0, PTR_gPrng_080cc5a4               @ 080cc536 1b48
    movs r2,#0x85    @ 080cc538 8522
    lsls r2,r2,#0x2    @ 080cc53a 9200
    adds r0,r0,r2    @ 080cc53c 8018
    ldr r0,[r0,#0x0]                         @ 080cc53e 0068
    lsls r0,r0,#0x1    @ 080cc540 4000
    lsrs r0,r0,#0x1    @ 080cc542 4008
    movs r1,#0x3c    @ 080cc544 3c21
    bl __divsi3                              @ 080cc546 42f05df8
    cmp r0,#0xb3                             @ 080cc54a b328
    ble LAB_080cc562                         @ 080cc54c 09dd
    ldr r0, DAT_080cc5a8                     @ 080cc54e 1648
    ldr r1, DAT_080cc5ac                     @ 080cc550 1649
    adds r0,r0,r1    @ 080cc552 4018
    movs r1,#0xd    @ 080cc554 0d21
    rsbs r1,r1,#0    @ 080cc556 4942
    ldrb r2,[r0,#0x0]                        @ 080cc558 0278
    ands r1,r2    @ 080cc55a 1140
    movs r2,#0x4    @ 080cc55c 0422
    orrs r1,r2    @ 080cc55e 1143
    strb r1,[r0,#0x0]                        @ 080cc560 0170
LAB_080cc562:
    ldr r1, DAT_080cc5b0                     @ 080cc562 1349
    ldr r5, DAT_080cc5b4                     @ 080cc564 134d
    ldr r0, DAT_080cc5b8                     @ 080cc566 1448
    adds r4,r5,r0    @ 080cc568 2c18
    ldrb r2,[r4,#0x0]                        @ 080cc56a 2278
    lsls r0,r2,#0x2    @ 080cc56c 9000
    adds r0,r0,r1    @ 080cc56e 4018
    ldr r0,[r0,#0x0]                         @ 080cc570 0068
    cmp r0,#0x0                              @ 080cc572 0028
    beq LAB_080cc5c0                         @ 080cc574 24d0
    bl invoke_r0                             @ 080cc576 42f027f8
    cmp r0,#0x0                              @ 080cc57a 0028
    beq LAB_080cc592                         @ 080cc57c 09d0
    ldrb r0,[r4,#0x0]                        @ 080cc57e 2078
    adds r0,#0x1    @ 080cc580 0130
    movs r1,#0x0    @ 080cc582 0021
    strb r0,[r4,#0x0]                        @ 080cc584 2070
    ldr r2, DAT_080cc5bc                     @ 080cc586 0d4a
    adds r0,r5,r2    @ 080cc588 a818
    strb r1,[r0,#0x0]                        @ 080cc58a 0170
    adds r2,#0x1    @ 080cc58c 0132
    adds r0,r5,r2    @ 080cc58e a818
    strb r1,[r0,#0x0]                        @ 080cc590 0170
LAB_080cc592:
    bl sort_zone_oam_entries_to_vram         @ 080cc592 00f041f8
    movs r0,#0x0    @ 080cc596 0020
    b LAB_080cc5e0                           @ 080cc598 22e0
    .zero  0x2
PTR_gP1LifePoints_080cc59c:
    .word  gP1LifePoints                  @ 080cc59c e0c40102
DAT_080cc5a0:
    .word  0x00001d08                     @ 080cc5a0 081d0000
PTR_gPrng_080cc5a4:
    .word  gPrng                          @ 080cc5a4 40000003
DAT_080cc5a8:
    .word  0x02023130                     @ 080cc5a8 30310202
DAT_080cc5ac:
    .word  0x00000222                     @ 080cc5ac 22020000
DAT_080cc5b0:
    .word  0x09e5abc8                     @ 080cc5b0 c8abe509
DAT_080cc5b4:
    .word  0x02020160                     @ 080cc5b4 60010202
DAT_080cc5b8:
    .word  0x00002f4c                     @ 080cc5b8 4c2f0000
DAT_080cc5bc:
    .word  0x00002f4d                     @ 080cc5bc 4d2f0000
LAB_080cc5c0:
    ldr r0, DAT_080cc5e8                     @ 080cc5c0 0948
    adds r1,r5,r0    @ 080cc5c2 2918
    movs r0,#0x2    @ 080cc5c4 0220
    rsbs r0,r0,#0    @ 080cc5c6 4042
    ldrb r2,[r1,#0x0]                        @ 080cc5c8 0a78
    ands r0,r2    @ 080cc5ca 1040
    strb r0,[r1,#0x0]                        @ 080cc5cc 0870
    ldr r1, DAT_080cc5ec                     @ 080cc5ce 0749
    ldr r0, DAT_080cc5f0                     @ 080cc5d0 0748
    adds r1,r1,r0    @ 080cc5d2 0918
    movs r0,#0x5    @ 080cc5d4 0520
    rsbs r0,r0,#0    @ 080cc5d6 4042
    ldrb r2,[r1,#0x0]                        @ 080cc5d8 0a78
    ands r0,r2    @ 080cc5da 1040
    strb r0,[r1,#0x0]                        @ 080cc5dc 0870
    movs r0,#0x1    @ 080cc5de 0120
LAB_080cc5e0:
    pop {r4,r5}                              @ 080cc5e0 30bc
    pop {r1}                                 @ 080cc5e2 02bc
    bx r1                                    @ 080cc5e4 0847
    .zero  0x2
DAT_080cc5e8:
    .word  0x00002f51                     @ 080cc5e8 512f0000
DAT_080cc5ec:
    .word  0x02023130                     @ 080cc5ec 30310202
DAT_080cc5f0:
    .word  0x00000215                     @ 080cc5f0 15020000

@ qsort comparator for sort_zone_oam_entries_to_vram. Compares two 9-byte zone OAM entry structs by draw priority: extracts bits[3:2] of byte[+5] from each entry (lsls #0x1c; lsrs #0x1e) as the priority field; if unequal returns the difference; if equal uses byte[+8] as tiebreak key. qsort sorts ascending so lower priority values render first.
@ 
@ Constants:
@ - PRIORITY_SHIFT = 0x1c (left shift to extract bits[3:2])
@ - PRIORITY_MASK_SHIFT = 0x1e (right shift to [1:0])
@ - TIEBREAK_OFFSET = 0x8 (secondary sort field byte offset)
@ - PRIORITY_OFFSET = 0x5 (primary sort field byte offset)
compare_zone_oam_entry_by_priority:
    push {r4,lr}                             @ 080cc5f4 10b5
    adds r2,r0,#0x0    @ 080cc5f6 021c
    adds r3,r1,#0x0    @ 080cc5f8 0b1c
    ldrb r0,[r2,#0x5]                        @ 080cc5fa 5079
    lsls r1,r0,#0x1c    @ 080cc5fc 0107
    lsrs r1,r1,#0x1e    @ 080cc5fe 890f
    ldrb r4,[r3,#0x5]                        @ 080cc600 5c79
    lsls r0,r4,#0x1c    @ 080cc602 2007
    lsrs r0,r0,#0x1e    @ 080cc604 800f
    subs r0,r1,r0    @ 080cc606 081a
    cmp r0,#0x0                              @ 080cc608 0028
    bne LAB_080cc612                         @ 080cc60a 02d1
    ldrb r2,[r2,#0x8]                        @ 080cc60c 127a
    ldrb r3,[r3,#0x8]                        @ 080cc60e 1b7a
    subs r0,r2,r3    @ 080cc610 d01a
LAB_080cc612:
    pop {r4}                                 @ 080cc612 10bc
    pop {r1}                                 @ 080cc614 02bc
    bx r1                                    @ 080cc616 0847

@ Collect active zone OAM sprite entries from gPrng sprite table into a stack buffer, sort them with qsort, then write back to OAM mirror at 0x030001fc. No parameters. Steps: alloc sp-=0x600; read count from gPrng+0x1bc+0x400; collect 9-byte entries (ldmia+str/strb) to sp buffer; qsort(sp_buf, count, 0xc, compare_fn=0x080cc5f5); write back 6 bytes/entry via copy_bytes_by_halfword to OAM[entry*8]. Side effects: writes [0x030001fc+entry*8] for each active OAM entry. Constants: gPrng_sprite_table=gPrng+0x1bc, count_offset=0x400, entry_copy_size=9, qsort_stride=0xc, oam_target=0x030001fc, write_bytes=6, sp_frame=0x600.
sort_zone_oam_entries_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080cc618 f0b5
    ldr r4, DAT_080cc684                     @ 080cc61a 1a4c
    add sp,r4                                @ 080cc61c a544
    ldr r0, PTR_gPrng_080cc688               @ 080cc61e 1a48
    movs r1,#0xde    @ 080cc620 de21
    lsls r1,r1,#0x1    @ 080cc622 4900
    adds r0,r0,r1    @ 080cc624 4018
    ldr r1,[r0,#0x0]                         @ 080cc626 0168
    movs r2,#0x80    @ 080cc628 8022
    lsls r2,r2,#0x3    @ 080cc62a d200
    adds r0,r1,r2    @ 080cc62c 8818
    ldrb r6,[r0,#0x0]                        @ 080cc62e 0678
    movs r4,#0x0    @ 080cc630 0024
    ldr r3, DAT_080cc68c                     @ 080cc632 164b
    cmp r4,r6                                @ 080cc634 b442
    bge LAB_080cc64c                         @ 080cc636 09da
    .hword 0x466a    @ 080cc638 6a46
    adds r5,r1,#0x0    @ 080cc63a 0d1c
LAB_080cc63c:
    ldmia r5!,{r0,r1}                        @ 080cc63c 03cd
    str r0,[r2,#0x0]                         @ 080cc63e 1060
    str r1,[r2,#0x4]                         @ 080cc640 5160
    strb r4,[r2,#0x8]                        @ 080cc642 1472
    adds r2,#0xc    @ 080cc644 0c32
    adds r4,#0x1    @ 080cc646 0134
    cmp r4,r6                                @ 080cc648 b442
    blt LAB_080cc63c                         @ 080cc64a f7db
LAB_080cc64c:
    .hword 0x4668    @ 080cc64c 6846
    adds r1,r6,#0x0    @ 080cc64e 311c
    movs r2,#0xc    @ 080cc650 0c22
    bl qsort                                 @ 080cc652 42f0ddf9
    movs r4,#0x0    @ 080cc656 0024
    cmp r4,r6                                @ 080cc658 b442
    bge LAB_080cc676                         @ 080cc65a 0cda
    ldr r7, DAT_080cc690                     @ 080cc65c 0c4f
    .hword 0x466d    @ 080cc65e 6d46
LAB_080cc660:
    lsls r1,r4,#0x3    @ 080cc660 e100
    ldr r0,[r7,#0x0]                         @ 080cc662 3868
    adds r0,r0,r1    @ 080cc664 4018
    adds r1,r5,#0x0    @ 080cc666 291c
    movs r2,#0x6    @ 080cc668 0622
    bl copy_bytes_by_halfword                @ 080cc66a 28f01bfc
    adds r5,#0xc    @ 080cc66e 0c35
    adds r4,#0x1    @ 080cc670 0134
    cmp r4,r6                                @ 080cc672 b442
    blt LAB_080cc660                         @ 080cc674 f4db
LAB_080cc676:
    movs r3,#0xc0    @ 080cc676 c023
    lsls r3,r3,#0x3    @ 080cc678 db00
    add sp,r3                                @ 080cc67a 9d44
    pop {r4,r5,r6,r7}                        @ 080cc67c f0bc
    pop {r0}                                 @ 080cc67e 01bc
    bx r0                                    @ 080cc680 0047
    .zero  0x2
DAT_080cc684:
    .word  0xfffffa00                     @ 080cc684 00faffff
PTR_gPrng_080cc688:
    .word  gPrng                          @ 080cc688 40000003
DAT_080cc68c:
    .word  0x080cc5f5                     @ 080cc68c f5c50c08
DAT_080cc690:
    .word  0x030001fc                     @ 080cc690 fc010003

@ 计算决斗场地指定玩家的区域方向状态码. r0 = player_side [1..2] (1=玩家1, 2=玩家2). 通过 gP1LifePoints 表 (stride=0x868) 索引当前玩家的 zone 子结构, 读取 zone_type 字段 (位于 player_struct + 0x2c + team_flag*0x868). 若 zone_type == 8 (特殊类型): 直接按 player_side 返回 1 (r6==1) 或 2 (r6==2). 否则扫描 gPrng+0x23f (gPrng+0x23f..0x23f+count, byte 数组), 统计值为 1 的项数 (dir 加减). 再扫描 gPrng+0x241 (gPrng+0x241..+count), 同样统计. 将 count 值与 gPrng+0x240 bit0<<7 组合形成方向因子, 若结果 > 1 -> 返回 1 (正向); < -1 -> 返回 2 (反向); == 0 则检查 gPrng+0x240 bit6 决定返回 0 (停止) 或 3 (中性). 3 个 caller (FUN_080bd0a8, FUN_080bd3f4, FUN_080bd660) 均为 banner/display 场景帧 tick 函数. Constants: gP1LifePoints (0x0201c4e0): 玩家结构数组基址 (stride=0x868); 0x868: 玩家结构步长; 0x2c: zone_info 偏移; gPrng+0x23f (DAT=0x23f): zone byte 数组起点; gPrng+0x241 (DAT=0x241): 第二数组起点; gPrng+0x240: 方向标志字节; 返回值: 0=停止/中性待定, 1=正向, 2=反向, 3=中性激活.
compute_duel_zone_dir_for_player:
    push {r4,r5,r6,r7,lr}                    @ 080cc694 f0b5
    adds r6,r0,#0x0    @ 080cc696 061c
    movs r4,#0x0    @ 080cc698 0024
    cmp r6,#0x2                              @ 080cc69a 022e
    bne LAB_080cc6b4                         @ 080cc69c 0ad1
    ldr r2, PTR_gP1LifePoints_080cc6ac       @ 080cc69e 034a
    ldr r3, DAT_080cc6b0                     @ 080cc6a0 034b
    ldr r1,[r3,#0x4]                         @ 080cc6a2 5968
    movs r0,#0x1    @ 080cc6a4 0120
    bics r0,r1    @ 080cc6a6 8843
    b LAB_080cc6be                           @ 080cc6a8 09e0
    .zero  0x2
PTR_gP1LifePoints_080cc6ac:
    .word  gP1LifePoints                  @ 080cc6ac e0c40102
DAT_080cc6b0:
    .word  0x0201e2a0                     @ 080cc6b0 a0e20102
LAB_080cc6b4:
    ldr r2, PTR_gP1LifePoints_080cc710       @ 080cc6b4 164a
    ldr r3, DAT_080cc714                     @ 080cc6b6 174b
    ldr r0,[r3,#0x4]                         @ 080cc6b8 5868
    movs r1,#0x1    @ 080cc6ba 0121
    ands r0,r1    @ 080cc6bc 0840
LAB_080cc6be:
    ldr r1, DAT_080cc718                     @ 080cc6be 1649
    muls r0,r1    @ 080cc6c0 4843
    adds r2,#0x2c    @ 080cc6c2 2c32
    adds r0,r0,r2    @ 080cc6c4 8018
    ldr r0,[r0,#0x0]                         @ 080cc6c6 0068
    .hword 0x469c    @ 080cc6c8 9c46
    cmp r0,#0x8                              @ 080cc6ca 0828
    bne LAB_080cc6da                         @ 080cc6cc 05d1
    cmp r6,#0x1                              @ 080cc6ce 012e
    bne LAB_080cc6d4                         @ 080cc6d0 00d1
    b LAB_080cc824                           @ 080cc6d2 a7e0
LAB_080cc6d4:
    cmp r6,#0x2                              @ 080cc6d4 022e
    bne LAB_080cc6da                         @ 080cc6d6 00d1
    b LAB_080cc82c                           @ 080cc6d8 a8e0
LAB_080cc6da:
    movs r5,#0x0    @ 080cc6da 0025
    ldr r1, PTR_gPrng_080cc71c               @ 080cc6dc 0f49
    ldr r2, DAT_080cc720                     @ 080cc6de 104a
    adds r0,r1,r2    @ 080cc6e0 8818
    ldrb r0,[r0,#0x0]                        @ 080cc6e2 0078
    lsrs r3,r0,#0x1    @ 080cc6e4 4308
    movs r0,#0x90    @ 080cc6e6 9020
    lsls r0,r0,#0x2    @ 080cc6e8 8000
    adds r2,r1,r0    @ 080cc6ea 0a18
    movs r0,#0x1    @ 080cc6ec 0120
    ldrb r2,[r2,#0x0]                        @ 080cc6ee 1278
    ands r0,r2    @ 080cc6f0 1040
    lsls r0,r0,#0x7    @ 080cc6f2 c001
    orrs r0,r3    @ 080cc6f4 1843
    adds r7,r1,#0x0    @ 080cc6f6 0f1c
    cmp r5,r0                                @ 080cc6f8 8542
    bge LAB_080cc734                         @ 080cc6fa 1bda
    ldr r1, DAT_080cc724                     @ 080cc6fc 0949
    adds r2,r7,r1    @ 080cc6fe 7a18
    adds r1,r0,#0x0    @ 080cc700 011c
LAB_080cc702:
    adds r0,r5,r2    @ 080cc702 a818
    ldrb r0,[r0,#0x0]                        @ 080cc704 0078
    cmp r0,#0x1                              @ 080cc706 0128
    beq LAB_080cc728                         @ 080cc708 0ed0
    cmp r0,#0x2                              @ 080cc70a 0228
    beq LAB_080cc72c                         @ 080cc70c 0ed0
    b LAB_080cc72e                           @ 080cc70e 0ee0
PTR_gP1LifePoints_080cc710:
    .word  gP1LifePoints                  @ 080cc710 e0c40102
DAT_080cc714:
    .word  0x0201e2a0                     @ 080cc714 a0e20102
DAT_080cc718:
    .word  0x00000868                     @ 080cc718 68080000
PTR_gPrng_080cc71c:
    .word  gPrng                          @ 080cc71c 40000003
DAT_080cc720:
    .word  0x0000023f                     @ 080cc720 3f020000
DAT_080cc724:
    .word  0x00000241                     @ 080cc724 41020000
LAB_080cc728:
    adds r4,#0x1    @ 080cc728 0134
    b LAB_080cc72e                           @ 080cc72a 00e0
LAB_080cc72c:
    subs r4,#0x1    @ 080cc72c 013c
LAB_080cc72e:
    adds r5,#0x1    @ 080cc72e 0135
    cmp r5,r1                                @ 080cc730 8d42
    blt LAB_080cc702                         @ 080cc732 e6db
LAB_080cc734:
    cmp r6,#0x1                              @ 080cc734 012e
    beq LAB_080cc73e                         @ 080cc736 02d0
    cmp r6,#0x2                              @ 080cc738 022e
    beq LAB_080cc742                         @ 080cc73a 02d0
    b LAB_080cc744                           @ 080cc73c 02e0
LAB_080cc73e:
    adds r4,#0x1    @ 080cc73e 0134
    b LAB_080cc744                           @ 080cc740 00e0
LAB_080cc742:
    subs r4,#0x1    @ 080cc742 013c
LAB_080cc744:
    ldr r2, DAT_080cc7f8                     @ 080cc744 2c4a
    adds r0,r7,r2    @ 080cc746 b818
    ldrb r0,[r0,#0x0]                        @ 080cc748 0078
    lsrs r2,r0,#0x1    @ 080cc74a 4208
    movs r0,#0x90    @ 080cc74c 9020
    lsls r0,r0,#0x2    @ 080cc74e 8000
    adds r1,r7,r0    @ 080cc750 3918
    movs r0,#0x1    @ 080cc752 0120
    ldrb r1,[r1,#0x0]                        @ 080cc754 0978
    ands r0,r1    @ 080cc756 0840
    lsls r1,r0,#0x7    @ 080cc758 c101
    orrs r1,r2    @ 080cc75a 1143
    muls r4,r1    @ 080cc75c 4c43
    cmp r4,#0x1                              @ 080cc75e 012c
    bgt LAB_080cc824                         @ 080cc760 60dc
    movs r0,#0x1    @ 080cc762 0120
    rsbs r0,r0,#0    @ 080cc764 4042
    cmp r4,r0                                @ 080cc766 8442
    blt LAB_080cc82c                         @ 080cc768 60db
    cmp r1,#0x1                              @ 080cc76a 0129
    bhi LAB_080cc834                         @ 080cc76c 62d8
    movs r0,#0x8a    @ 080cc76e 8a20
    lsls r0,r0,#0x2    @ 080cc770 8000
    add r0,r12                               @ 080cc772 6044
    ldr r0,[r0,#0x0]                         @ 080cc774 0068
    cmp r0,#0x9                              @ 080cc776 0928
    beq LAB_080cc7c4                         @ 080cc778 24d0
    ldr r5, DAT_080cc7fc                     @ 080cc77a 204d
    adds r0,r5,#0x0    @ 080cc77c 281c
    adds r0,#0x37    @ 080cc77e 3730
    ldrb r0,[r0,#0x0]                        @ 080cc780 0078
    lsls r4,r0,#0x19    @ 080cc782 4406
    lsrs r0,r4,#0x1b    @ 080cc784 e00e
    lsls r1,r0,#0x2    @ 080cc786 8100
    adds r1,r1,r0    @ 080cc788 0918
    lsls r0,r1,#0x4    @ 080cc78a 0801
    subs r0,r0,r1    @ 080cc78c 401a
    lsls r0,r0,#0x2    @ 080cc78e 8000
    cmp r0,#0x0                              @ 080cc790 0028
    beq LAB_080cc7b6                         @ 080cc792 10d0
    movs r1,#0x84    @ 080cc794 8421
    lsls r1,r1,#0x2    @ 080cc796 8900
    adds r0,r7,r1    @ 080cc798 7818
    ldr r0,[r0,#0x0]                         @ 080cc79a 0068
    lsls r0,r0,#0x1    @ 080cc79c 4000
    lsrs r0,r0,#0x1    @ 080cc79e 4008
    movs r1,#0x3c    @ 080cc7a0 3c21
    bl __divsi3                              @ 080cc7a2 41f02fff
    lsrs r1,r4,#0x1b    @ 080cc7a6 e10e
    lsls r2,r1,#0x2    @ 080cc7a8 8a00
    adds r2,r2,r1    @ 080cc7aa 5218
    lsls r1,r2,#0x4    @ 080cc7ac 1101
    subs r1,r1,r2    @ 080cc7ae 891a
    lsls r1,r1,#0x2    @ 080cc7b0 8900
    cmp r0,r1                                @ 080cc7b2 8842
    bge LAB_080cc7c4                         @ 080cc7b4 06da
LAB_080cc7b6:
    adds r1,r5,#0x0    @ 080cc7b6 291c
    adds r1,#0x36    @ 080cc7b8 3631
    movs r0,#0x40    @ 080cc7ba 4020
    ldrb r1,[r1,#0x0]                        @ 080cc7bc 0978
    ands r0,r1    @ 080cc7be 0840
    cmp r0,#0x0                              @ 080cc7c0 0028
    beq LAB_080cc830                         @ 080cc7c2 35d0
LAB_080cc7c4:
    movs r4,#0x0    @ 080cc7c4 0024
    movs r5,#0x0    @ 080cc7c6 0025
    ldr r2, DAT_080cc7f8                     @ 080cc7c8 0b4a
    adds r0,r7,r2    @ 080cc7ca b818
    ldrb r0,[r0,#0x0]                        @ 080cc7cc 0078
    lsrs r2,r0,#0x1    @ 080cc7ce 4208
    movs r0,#0x90    @ 080cc7d0 9020
    lsls r0,r0,#0x2    @ 080cc7d2 8000
    adds r1,r7,r0    @ 080cc7d4 3918
    movs r0,#0x1    @ 080cc7d6 0120
    ldrb r1,[r1,#0x0]                        @ 080cc7d8 0978
    ands r0,r1    @ 080cc7da 0840
    lsls r0,r0,#0x7    @ 080cc7dc c001
    orrs r0,r2    @ 080cc7de 1043
    cmp r4,r0                                @ 080cc7e0 8442
    bge LAB_080cc810                         @ 080cc7e2 15da
    ldr r2, DAT_080cc800                     @ 080cc7e4 064a
    adds r1,r7,r2    @ 080cc7e6 b918
    adds r2,r0,#0x0    @ 080cc7e8 021c
LAB_080cc7ea:
    adds r0,r5,r1    @ 080cc7ea 6818
    ldrb r0,[r0,#0x0]                        @ 080cc7ec 0078
    cmp r0,#0x1                              @ 080cc7ee 0128
    beq LAB_080cc804                         @ 080cc7f0 08d0
    cmp r0,#0x2                              @ 080cc7f2 0228
    beq LAB_080cc808                         @ 080cc7f4 08d0
    b LAB_080cc80a                           @ 080cc7f6 08e0
DAT_080cc7f8:
    .word  0x0000023f                     @ 080cc7f8 3f020000
DAT_080cc7fc:
    .word  0x02023360                     @ 080cc7fc 60330202
DAT_080cc800:
    .word  0x00000241                     @ 080cc800 41020000
LAB_080cc804:
    adds r4,#0x1    @ 080cc804 0134
    b LAB_080cc80a                           @ 080cc806 00e0
LAB_080cc808:
    subs r4,#0x1    @ 080cc808 013c
LAB_080cc80a:
    adds r5,#0x1    @ 080cc80a 0135
    cmp r5,r2                                @ 080cc80c 9542
    blt LAB_080cc7ea                         @ 080cc80e ecdb
LAB_080cc810:
    cmp r6,#0x1                              @ 080cc810 012e
    beq LAB_080cc81a                         @ 080cc812 02d0
    cmp r6,#0x2                              @ 080cc814 022e
    beq LAB_080cc81e                         @ 080cc816 02d0
    b LAB_080cc820                           @ 080cc818 02e0
LAB_080cc81a:
    adds r4,#0x1    @ 080cc81a 0134
    b LAB_080cc820                           @ 080cc81c 00e0
LAB_080cc81e:
    subs r4,#0x1    @ 080cc81e 013c
LAB_080cc820:
    cmp r4,#0x0                              @ 080cc820 002c
    ble LAB_080cc828                         @ 080cc822 01dd
LAB_080cc824:
    movs r0,#0x1    @ 080cc824 0120
    b LAB_080cc836                           @ 080cc826 06e0
LAB_080cc828:
    cmp r4,#0x0                              @ 080cc828 002c
    bge LAB_080cc834                         @ 080cc82a 03da
LAB_080cc82c:
    movs r0,#0x2    @ 080cc82c 0220
    b LAB_080cc836                           @ 080cc82e 02e0
LAB_080cc830:
    movs r0,#0x0    @ 080cc830 0020
    b LAB_080cc836                           @ 080cc832 00e0
LAB_080cc834:
    movs r0,#0x3    @ 080cc834 0320
LAB_080cc836:
    pop {r4,r5,r6,r7}                        @ 080cc836 f0bc
    pop {r1}                                 @ 080cc838 02bc
    bx r1                                    @ 080cc83a 0847

@ Clears all duel_puzzle scene display buffers and resets audio state, serving as the second stage of scene reset. Called by run_campaign_step26_init_duel_puzzle_scene (0x0802752c) and FUN_0801fec0 (duel_puzzle main loop). Calls zero_fill_by_halfword 8 times on EWRAM display buffers (card OAM entry cache, UI effect area, banner state area, etc.). Then calls request_sound_engine_code10 to reset audio engine. Finally clears gPrng+0x214 (gPrng[0x85]) bit31, which controls duel scene music track selection flag.
@ 
@ Constants:
@ - clear_region_1=0x0201ff60 (0x80*4=0x200 halfwords)
@ - clear_region_2=0x02023130 (0x8a*4=0x228 halfwords)
@ - gUIEffectState=0x02023110 (0x1c*2=0x38 halfwords)
@ - clear_region_4=0x0201f440 (0xa2*16=0xa20 halfwords)
@ - clear_region_5=0x0201ff30 (0x2c*2=0x58 halfwords)
@ - clear_region_6=0x02020160 (0x2f5c halfwords)
@ - gBannerState=0x0201fec0 (0x6c*2=0xd8 halfwords)
@ - clear_region_8=0x0201fe60 (0x5c*2=0xb8 halfwords)
@ - gPrng+0x214=gPrng[0x85] bit31 (music track flag, cleared to 0)
@ - music_flag_mask=0x80000000
zero_duel_scene_display_buffers:
    push {lr}                                @ 080cc83c 00b5
    ldr r0, DAT_080cc8a0                     @ 080cc83e 1848
    movs r1,#0x80    @ 080cc840 8021
    lsls r1,r1,#0x2    @ 080cc842 8900
    bl zero_fill_by_halfword                 @ 080cc844 28f016fb
    ldr r0, DAT_080cc8a4                     @ 080cc848 1648
    movs r1,#0x8a    @ 080cc84a 8a21
    lsls r1,r1,#0x2    @ 080cc84c 8900
    bl zero_fill_by_halfword                 @ 080cc84e 28f011fb
    ldr r0, DAT_080cc8a8                     @ 080cc852 1548
    movs r1,#0x1c    @ 080cc854 1c21
    bl zero_fill_by_halfword                 @ 080cc856 28f00dfb
    ldr r0, DAT_080cc8ac                     @ 080cc85a 1448
    movs r1,#0xa2    @ 080cc85c a221
    lsls r1,r1,#0x4    @ 080cc85e 0901
    bl zero_fill_by_halfword                 @ 080cc860 28f008fb
    ldr r0, DAT_080cc8b0                     @ 080cc864 1248
    movs r1,#0x2c    @ 080cc866 2c21
    bl zero_fill_by_halfword                 @ 080cc868 28f004fb
    ldr r0, DAT_080cc8b4                     @ 080cc86c 1148
    ldr r1, DAT_080cc8b8                     @ 080cc86e 1249
    bl zero_fill_by_halfword                 @ 080cc870 28f000fb
    ldr r0, DAT_080cc8bc                     @ 080cc874 1148
    movs r1,#0x6c    @ 080cc876 6c21
    bl zero_fill_by_halfword                 @ 080cc878 28f0fcfa
    ldr r0, DAT_080cc8c0                     @ 080cc87c 1048
    movs r1,#0x5c    @ 080cc87e 5c21
    bl zero_fill_by_halfword                 @ 080cc880 28f0f8fa
    bl request_sound_engine_code10           @ 080cc884 2df05cf9
    ldr r1, PTR_gPrng_080cc8c4               @ 080cc888 0e49
    movs r0,#0x85    @ 080cc88a 8520
    lsls r0,r0,#0x2    @ 080cc88c 8000
    adds r1,r1,r0    @ 080cc88e 0918
    ldr r0,[r1,#0x0]                         @ 080cc890 0868
    movs r2,#0x80    @ 080cc892 8022
    lsls r2,r2,#0x18    @ 080cc894 1206
    ands r0,r2    @ 080cc896 1040
    str r0,[r1,#0x0]                         @ 080cc898 0860
    pop {r0}                                 @ 080cc89a 01bc
    bx r0                                    @ 080cc89c 0047
    .zero  0x2
DAT_080cc8a0:
    .word  0x0201ff60                     @ 080cc8a0 60ff0102
DAT_080cc8a4:
    .word  0x02023130                     @ 080cc8a4 30310202
DAT_080cc8a8:
    .word  gUIEffectState                 @ 080cc8a8 10310202
DAT_080cc8ac:
    .word  0x0201f440                     @ 080cc8ac 40f40102
DAT_080cc8b0:
    .word  0x0201ff30                     @ 080cc8b0 30ff0102
DAT_080cc8b4:
    .word  0x02020160                     @ 080cc8b4 60010202
DAT_080cc8b8:
    .word  0x00002f5c                     @ 080cc8b8 5c2f0000
DAT_080cc8bc:
    .word  gBannerState                   @ 080cc8bc c0fe0102
DAT_080cc8c0:
    .word  0x0201fe60                     @ 080cc8c0 60fe0102
PTR_gPrng_080cc8c4:
    .word  gPrng                          @ 080cc8c4 40000003

@ Ensure cache entry at 0x0201ff60+r0*2 is filled; if zero, load from hand table and write. Flow: r4=0x0201ff60+r0*2 (cache slot ptr); ldrh [r4]; nonzero (cached) -> return. Otherwise: base=gP1LifePoints+r0*4+0x87*32 (=gP1LifePoints+r0*4+0x10e0); ldrh card_word=[base]; card_id=bits[12:0]; bl internal_card_id_to_card_id(card_id); lsls/lsrs truncate to 16 bits; strh card_id,[r4] (write cache slot). No explicit r0 return. Used to cache current hand/slot card_id for UI display layer, avoiding repeat decode. Constants: cache_base=0x0201ff60, cache_stride=2 (u16/entry), gP1LifePoints=0x0201c4e0, hand_base_offset=0x87*32=0x10e0, card_id_mask=0x1fff.
ensure_card_id_cache_entry:
    push {r4,lr}                             @ 080cc8c8 10b5
    adds r2,r0,#0x0    @ 080cc8ca 021c
    ldr r1, DAT_080cc8fc                     @ 080cc8cc 0b49
    lsls r0,r2,#0x1    @ 080cc8ce 5000
    adds r4,r0,r1    @ 080cc8d0 4418
    ldrh r0,[r4,#0x0]                        @ 080cc8d2 2088
    cmp r0,#0x0                              @ 080cc8d4 0028
    bne LAB_080cc8f4                         @ 080cc8d6 0dd1
    ldr r1, PTR_gP1LifePoints_080cc900       @ 080cc8d8 0949
    lsls r0,r2,#0x2    @ 080cc8da 9000
    adds r0,r0,r1    @ 080cc8dc 4018
    movs r1,#0x87    @ 080cc8de 8721
    lsls r1,r1,#0x5    @ 080cc8e0 4901
    adds r0,r0,r1    @ 080cc8e2 4018
    ldrh r0,[r0,#0x0]                        @ 080cc8e4 0088
    lsls r0,r0,#0x13    @ 080cc8e6 c004
    lsrs r0,r0,#0x13    @ 080cc8e8 c00c
    bl internal_card_id_to_card_id           @ 080cc8ea 21f03fff
    lsls r0,r0,#0x10    @ 080cc8ee 0004
    lsrs r0,r0,#0x10    @ 080cc8f0 000c
    strh r0,[r4,#0x0]                        @ 080cc8f2 2080
LAB_080cc8f4:
    pop {r4}                                 @ 080cc8f4 10bc
    pop {r1}                                 @ 080cc8f6 02bc
    bx r1                                    @ 080cc8f8 0847
    .zero  0x2
DAT_080cc8fc:
    .word  0x0201ff60                     @ 080cc8fc 60ff0102
PTR_gP1LifePoints_080cc900:
    .word  gP1LifePoints                  @ 080cc900 e0c40102

@ duel field 场地 VRAM 完整初始化 hub, 被 play_demo_shuen / play_ui_effect_3b/3a / FUN_0801fec0 等 8 个调用方共享. 依次: (1) zero_fill_by_halfword 清空 VRAM OBJ tile 区; (2) store_ewram_ctx_ptr_and_clear_mode_flags; (3) reset_display_and_obj_vram; (4) apply_blend_fadeout_flat; (5) reset_all_bg_scroll_regs_and_shadows; (6) 设置 gPrng[0xba*2]=1; (7) 配置 BG0-3CNT 四寄存器; (8) 复制多组 tile/screen 数据; (9) init_duel_field_lp_aob_ctx; (10) 条件性复制 tile; (11) write_palette_tile_row_to_vram; (12) init_duel_field_tile_indices + redraw_all_field_slot_tiles; (13) strh DISPCNT. Constants: BG0CNT=0x1f08, BG1CNT=0x1f09, BG2CNT=0x1d82, BG3CNT=0x1c0b.
init_duel_field_vram_layout:
    push {r4,r5,lr}                          @ 080cc904 30b5
    movs r0,#0xc0    @ 080cc906 c020
    lsls r0,r0,#0x13    @ 080cc908 c004
    movs r1,#0xc0    @ 080cc90a c021
    lsls r1,r1,#0x9    @ 080cc90c 4902
    bl zero_fill_by_halfword                 @ 080cc90e 28f0b1fa
    ldr r0, DAT_080cc9e0                     @ 080cc912 3348
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 080cc914 27f0c4fc
    ldr r0, DAT_080cc9e4                     @ 080cc918 3248
    bl reset_display_and_obj_vram            @ 080cc91a 2af0abfe
    bl apply_blend_fadeout_flat              @ 080cc91e 28f057ff
    bl reset_all_bg_scroll_regs_and_shadows  @ 080cc922 29f0b1f8
    movs r5,#0x80    @ 080cc926 8025
    lsls r5,r5,#0x13    @ 080cc928 ed04
    movs r0,#0x0    @ 080cc92a 0020
    strh r0,[r5,#0x0]                        @ 080cc92c 2880
    ldr r0, PTR_gPrng_080cc9e8               @ 080cc92e 2e48
    movs r1,#0xba    @ 080cc930 ba21
    lsls r1,r1,#0x1    @ 080cc932 4900
    adds r0,r0,r1    @ 080cc934 4018
    movs r1,#0x1    @ 080cc936 0121
    strh r1,[r0,#0x0]                        @ 080cc938 0180
    ldr r1, PTR_BG0CNT_080cc9ec              @ 080cc93a 2c49
    ldr r2, DAT_080cc9f0                     @ 080cc93c 2c4a
    adds r0,r2,#0x0    @ 080cc93e 101c
    strh r0,[r1,#0x0]                        @ 080cc940 0880
    adds r1,#0x2    @ 080cc942 0231
    subs r2,#0xff    @ 080cc944 ff3a
    adds r0,r2,#0x0    @ 080cc946 101c
    strh r0,[r1,#0x0]                        @ 080cc948 0880
    adds r1,#0x2    @ 080cc94a 0231
    subs r2,#0x87    @ 080cc94c 873a
    adds r0,r2,#0x0    @ 080cc94e 101c
    strh r0,[r1,#0x0]                        @ 080cc950 0880
    adds r1,#0x2    @ 080cc952 0231
    ldr r2, DAT_080cc9f4                     @ 080cc954 274a
    adds r0,r2,#0x0    @ 080cc956 101c
    strh r0,[r1,#0x0]                        @ 080cc958 0880
    ldr r0, DAT_080cc9f8                     @ 080cc95a 2748
    ldr r1, PTR_hud_gap_tiles_080cc9fc       @ 080cc95c 2749
    movs r2,#0x8    @ 080cc95e 0822
    movs r3,#0x4    @ 080cc960 0423
    bl tile_2d_row_copy                      @ 080cc962 2af0b7fd
    ldr r0, DAT_080cca00                     @ 080cc966 2648
    ldr r1, DAT_080cca04                     @ 080cc968 2649
    movs r2,#0x2    @ 080cc96a 0222
    movs r3,#0x1    @ 080cc96c 0123
    bl tile_2d_row_copy                      @ 080cc96e 2af0b1fd
    ldr r0, DAT_080cca08                     @ 080cc972 2548
    ldr r1, DAT_080cca0c                     @ 080cc974 2549
    movs r2,#0x3    @ 080cc976 0322
    movs r3,#0x1    @ 080cc978 0123
    bl tile_2d_row_copy                      @ 080cc97a 2af0abfd
    ldr r0, DAT_080cca10                     @ 080cc97e 2448
    ldr r1, DAT_080cca14                     @ 080cc980 2449
    movs r2,#0x20    @ 080cc982 2022
    bl copy_bytes_by_halfword                @ 080cc984 28f08efa
    bl init_duel_field_lp_aob_ctx            @ 080cc988 fbf708ff
    ldr r4, DAT_080cca18                     @ 080cc98c 224c
    ldr r0, DAT_080cca1c                     @ 080cc98e 2348
    adds r1,r4,r0    @ 080cc990 2118
    movs r0,#0x10    @ 080cc992 1020
    ldrb r1,[r1,#0x0]                        @ 080cc994 0978
    ands r0,r1    @ 080cc996 0840
    cmp r0,#0x0                              @ 080cc998 0028
    beq LAB_080cc9be                         @ 080cc99a 10d0
    ldr r0, DAT_080cca20                     @ 080cc99c 2048
    ldr r1, DAT_080cca24                     @ 080cc99e 2149
    movs r2,#0x4    @ 080cc9a0 0422
    movs r3,#0x1    @ 080cc9a2 0123
    bl tile_2d_row_copy                      @ 080cc9a4 2af096fd
    ldr r0, DAT_080cca28                     @ 080cc9a8 1f48
    ldr r1, DAT_080cca2c                     @ 080cc9aa 2049
    movs r2,#0x1    @ 080cc9ac 0122
    movs r3,#0x1    @ 080cc9ae 0123
    bl tile_2d_row_copy                      @ 080cc9b0 2af090fd
    ldr r0, DAT_080cca30                     @ 080cc9b4 1e48
    ldr r1, DAT_080cca34                     @ 080cc9b6 1f49
    movs r2,#0x20    @ 080cc9b8 2022
    bl copy_bytes_by_halfword                @ 080cc9ba 28f073fa
LAB_080cc9be:
    movs r0,#0x0    @ 080cc9be 0020
    strh r0,[r4,#0x8]                        @ 080cc9c0 2081
    bl write_palette_tile_row_to_vram        @ 080cc9c2 f6f771fe
    bl init_duel_field_tile_indices          @ 080cc9c6 fdf791ff
    bl redraw_all_field_slot_tiles           @ 080cc9ca f8f79bf9
    ldrh r0,[r5,#0x0]                        @ 080cc9ce 2888
    movs r2,#0xf8    @ 080cc9d0 f822
    lsls r2,r2,#0x5    @ 080cc9d2 5201
    adds r1,r2,#0x0    @ 080cc9d4 111c
    orrs r0,r1    @ 080cc9d6 0843
    strh r0,[r5,#0x0]                        @ 080cc9d8 2880
    pop {r4,r5}                              @ 080cc9da 30bc
    pop {r0}                                 @ 080cc9dc 01bc
    bx r0                                    @ 080cc9de 0047
DAT_080cc9e0:
    .word  0x02029eb0                     @ 080cc9e0 b09e0202
DAT_080cc9e4:
    .word  0x0203eeb0                     @ 080cc9e4 b0ee0302
PTR_gPrng_080cc9e8:
    .word  gPrng                          @ 080cc9e8 40000003
PTR_BG0CNT_080cc9ec:
    .word  BG0CNT                         @ 080cc9ec 08000004
DAT_080cc9f0:
    .word  0x00001f08                     @ 080cc9f0 081f0000
DAT_080cc9f4:
    .word  0x00001c0b                     @ 080cc9f4 0b1c0000
DAT_080cc9f8:
    .word  0x06010040                     @ 080cc9f8 40000106
PTR_hud_gap_tiles_080cc9fc:
    .word  hud_gap_tiles                  @ 080cc9fc fc158509
DAT_080cca00:
    .word  0x06010400                     @ 080cca00 00040106
DAT_080cca04:
    .word  0x098525fc                     @ 080cca04 fc258509
DAT_080cca08:
    .word  0x06011f60                     @ 080cca08 601f0106
DAT_080cca0c:
    .word  0x0985337c                     @ 080cca0c 7c338509
DAT_080cca10:
    .word  0x050002e0                     @ 080cca10 e0020005
DAT_080cca14:
    .word  0x0985329c                     @ 080cca14 9c328509
DAT_080cca18:
    .word  0x02023130                     @ 080cca18 30310202
DAT_080cca1c:
    .word  0x00000215                     @ 080cca1c 15020000
DAT_080cca20:
    .word  0x06013400                     @ 080cca20 00340106
DAT_080cca24:
    .word  0x099082a4                     @ 080cca24 a4829009
DAT_080cca28:
    .word  0x06010800                     @ 080cca28 00080106
DAT_080cca2c:
    .word  0x09ccd2d0                     @ 080cca2c d0d2cc09
DAT_080cca30:
    .word  0x05000260                     @ 080cca30 60020005
DAT_080cca34:
    .word  0x09850c5c                     @ 080cca34 5c0c8509

@ 在 duel field 状态机收尾步骤中被 8 个 caller 调用 (play_demo_shuen / play_ui_effect_3b/3a / FUN_0801fec0 等). 先将 EWRAM 标志字节 [0x02023345] bit1 置 1 (激活淡出信号), 然后以步进量 2 调用 tick_blend_step_by_delta 推进混合淡出过渡. 无参数; 返回 tick_blend_step_by_delta 的返回值 (0=进行中, 1=完成). Constants: EWRAM_FLAG_ADDR=0x02023345, BLEND_STEP_DELTA=2, FLAG_BIT1=0x2.
tick_duel_field_fadeout_step:
    push {lr}                                @ 080cca38 00b5
    ldr r0, DAT_080cca54                     @ 080cca3a 0648
    ldr r1, DAT_080cca58                     @ 080cca3c 0649
    adds r0,r0,r1    @ 080cca3e 4018
    movs r1,#0x2    @ 080cca40 0221
    ldrb r2,[r0,#0x0]                        @ 080cca42 0278
    orrs r1,r2    @ 080cca44 1143
    strb r1,[r0,#0x0]                        @ 080cca46 0170
    movs r0,#0x2    @ 080cca48 0220
    bl tick_blend_step_by_delta              @ 080cca4a 28f035ff
    pop {r1}                                 @ 080cca4e 02bc
    bx r1                                    @ 080cca50 0847
    .zero  0x2
DAT_080cca54:
    .word  0x02023130                     @ 080cca54 30310202
DAT_080cca58:
    .word  0x00000215                     @ 080cca58 15020000

@ 与 tick_duel_field_fadeout_step (0x080cca38) 构成对称函数对, 被 10 个 caller 共享. 先将 EWRAM 标志字节 [0x02023345] bits[1:0] 同时清零 (ands ~0x3=0xFC), 然后以步进量 2 调用 start_blend_fadein_with_target 开始混合淡入过渡. 无参数; 返回 start_blend_fadein_with_target 的返回值. Constants: EWRAM_FLAG_ADDR=0x02023345, BLEND_STEP_DELTA=2, FLAG_CLEAR_MASK=0xFC.
tick_duel_field_fadein_step:
    push {lr}                                @ 080cca5c 00b5
    ldr r0, DAT_080cca78                     @ 080cca5e 0648
    ldr r1, DAT_080cca7c                     @ 080cca60 0649
    adds r0,r0,r1    @ 080cca62 4018
    movs r1,#0x3    @ 080cca64 0321
    rsbs r1,r1,#0    @ 080cca66 4942
    ldrb r2,[r0,#0x0]                        @ 080cca68 0278
    ands r1,r2    @ 080cca6a 1140
    strb r1,[r0,#0x0]                        @ 080cca6c 0170
    movs r0,#0x2    @ 080cca6e 0220
    bl start_blend_fadein_with_target        @ 080cca70 28f0e6fe
    pop {r1}                                 @ 080cca74 02bc
    bx r1                                    @ 080cca76 0847
DAT_080cca78:
    .word  0x02023130                     @ 080cca78 30310202
DAT_080cca7c:
    .word  0x00000215                     @ 080cca7c 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x03 子状态机, 待详细分析.
play_ui_effect_03:
    push {r4,r5,r6,r7,lr}                    @ 080cca80 f0b5
    movs r5,#0x0    @ 080cca82 0025
    ldr r0, PTR_gP1LifePoints_080cca94       @ 080cca84 0348
    ldr r1, DAT_080cca98                     @ 080cca86 0449
    adds r0,r0,r1    @ 080cca88 4018
    ldr r0,[r0,#0x0]                         @ 080cca8a 0068
    cmp r0,#0x0                              @ 080cca8c 0028
    bne LAB_080cca9c                         @ 080cca8e 05d1
LAB_080cca90:
    movs r0,#0x0    @ 080cca90 0020
    b LAB_080ccdee                           @ 080cca92 ace1
PTR_gP1LifePoints_080cca94:
    .word  gP1LifePoints                  @ 080cca94 e0c40102
DAT_080cca98:
    .word  0x00001d50                     @ 080cca98 501d0000
LAB_080cca9c:
    ldr r0, DAT_080ccab4                     @ 080cca9c 0548
    ldrb r2,[r0,#0x0]                        @ 080cca9e 0278
    adds r4,r0,#0x0    @ 080ccaa0 041c
    cmp r2,#0x4                              @ 080ccaa2 042a
    bls LAB_080ccaa8                         @ 080ccaa4 00d9
    b switchD_080ccab0__default              @ 080ccaa6 a1e1
LAB_080ccaa8:
    lsls r0,r2,#0x2    @ 080ccaa8 9000
    ldr r1, DAT_080ccab8                     @ 080ccaaa 0349
    adds r0,r0,r1    @ 080ccaac 4018
    ldr r0,[r0,#0x0]                         @ 080ccaae 0068
switchD_080ccab0__switchD:
    .hword 0x4687    @ 080ccab0 8746
    .zero  0x2
DAT_080ccab4:
    .word  0x02023130                     @ 080ccab4 30310202
DAT_080ccab8:
    .word  0x080ccabc                     @ 080ccab8 bcca0c08
switchD_080ccab0__switchdataD_080ccabc:
    .word  0x080ccad0                     @ 080ccabc d0ca0c08
    .word  0x080cccc4                     @ 080ccac0 c4cc0c08
    .word  0x080cccdc                     @ 080ccac4 dccc0c08
    .word  0x080cccfc                     @ 080ccac8 fccc0c08
    .word  0x080ccd64                     @ 080ccacc 64cd0c08
switchD_080ccab0__caseD_0:
    bl get_lp_display_anim_counter           @ 080ccad0 c9f750ff
    cmp r0,#0x1                              @ 080ccad4 0128
    bne LAB_080ccae6                         @ 080ccad6 06d1
    ldr r1, DAT_080ccb5c                     @ 080ccad8 2049
    movs r0,#0x8    @ 080ccada 0820
    ldrb r1,[r1,#0x0]                        @ 080ccadc 0978
    ands r0,r1    @ 080ccade 0840
    cmp r0,#0x0                              @ 080ccae0 0028
    beq LAB_080ccae6                         @ 080ccae2 00d0
    movs r5,#0x1    @ 080ccae4 0125
LAB_080ccae6:
    ldr r2, PTR_gPrng_080ccb60               @ 080ccae6 1e4a
    movs r3,#0xa3    @ 080ccae8 a323
    lsls r3,r3,#0x1    @ 080ccaea 5b00
    adds r1,r2,r3    @ 080ccaec d118
    movs r0,#0x4    @ 080ccaee 0420
    ldrh r1,[r1,#0x0]                        @ 080ccaf0 0988
    ands r0,r1    @ 080ccaf2 0840
    adds r4,r2,#0x0    @ 080ccaf4 141c
    cmp r0,#0x0                              @ 080ccaf6 0028
    beq LAB_080ccb2a                         @ 080ccaf8 17d0
    movs r0,#0xa4    @ 080ccafa a420
    lsls r0,r0,#0x1    @ 080ccafc 4000
    adds r1,r4,r0    @ 080ccafe 2118
    adds r0,#0xb8    @ 080ccb00 b830
    ldrh r1,[r1,#0x0]                        @ 080ccb02 0988
    ands r0,r1    @ 080ccb04 0840
    cmp r0,#0x0                              @ 080ccb06 0028
    beq LAB_080ccb2a                         @ 080ccb08 0fd0
    ldr r2, DAT_080ccb64                     @ 080ccb0a 164a
    ldr r1, DAT_080ccb68                     @ 080ccb0c 1649
    adds r2,r2,r1    @ 080ccb0e 5218
    ldrb r3,[r2,#0x0]                        @ 080ccb10 1378
    lsls r0,r3,#0x1e    @ 080ccb12 9807
    lsrs r0,r0,#0x1f    @ 080ccb14 c00f
    movs r1,#0x1    @ 080ccb16 0121
    subs r1,r1,r0    @ 080ccb18 091a
    movs r0,#0x1    @ 080ccb1a 0120
    ands r1,r0    @ 080ccb1c 0140
    lsls r1,r1,#0x1    @ 080ccb1e 4900
    movs r0,#0x3    @ 080ccb20 0320
    rsbs r0,r0,#0    @ 080ccb22 4042
    ands r0,r3    @ 080ccb24 1840
    orrs r0,r1    @ 080ccb26 0843
    strb r0,[r2,#0x0]                        @ 080ccb28 1070
LAB_080ccb2a:
    movs r2,#0xa4    @ 080ccb2a a422
    lsls r2,r2,#0x1    @ 080ccb2c 5200
    adds r7,r4,r2    @ 080ccb2e a718
    ldrh r1,[r7,#0x0]                        @ 080ccb30 3988
    movs r0,#0x1    @ 080ccb32 0120
    ands r0,r1    @ 080ccb34 0840
    cmp r0,#0x0                              @ 080ccb36 0028
    bne LAB_080ccb3e                         @ 080ccb38 01d1
    cmp r5,#0x0                              @ 080ccb3a 002d
    beq LAB_080ccb80                         @ 080ccb3c 20d0
LAB_080ccb3e:
    bl init_zone_oam_ctx_by_type             @ 080ccb3e f8f74dfd
    ldr r4, DAT_080ccb5c                     @ 080ccb42 064c
    ldr r0,[r4,#0x4]                         @ 080ccb44 6068
    cmp r0,#0x0                              @ 080ccb46 0028
    bne LAB_080ccb6c                         @ 080ccb48 10d1
    movs r0,#0x2    @ 080ccb4a 0220
    bl sync_state_and_init_sprite            @ 080ccb4c 2cf0b2ff
    movs r0,#0x2    @ 080ccb50 0220
    rsbs r0,r0,#0    @ 080ccb52 4042
    ldrb r3,[r4,#0x0]                        @ 080ccb54 2378
    ands r0,r3    @ 080ccb56 1840
    strb r0,[r4,#0x0]                        @ 080ccb58 2070
    b switchD_080ccab0__default              @ 080ccb5a 47e1
DAT_080ccb5c:
    .word  0x0201ff30                     @ 080ccb5c 30ff0102
PTR_gPrng_080ccb60:
    .word  gPrng                          @ 080ccb60 40000003
DAT_080ccb64:
    .word  0x02023130                     @ 080ccb64 30310202
DAT_080ccb68:
    .word  0x0000021e                     @ 080ccb68 1e020000
LAB_080ccb6c:
    ldr r1, DAT_080ccb7c                     @ 080ccb6c 0349
    movs r0,#0x1    @ 080ccb6e 0120
    strb r0,[r1,#0x0]                        @ 080ccb70 0870
    movs r0,#0x24    @ 080ccb72 2420
    bl sync_state_and_init_sprite            @ 080ccb74 2cf09eff
    b switchD_080ccab0__default              @ 080ccb78 38e1
    .zero  0x2
DAT_080ccb7c:
    .word  0x02023130                     @ 080ccb7c 30310202
LAB_080ccb80:
    movs r0,#0x2    @ 080ccb80 0220
    ands r0,r1    @ 080ccb82 0840
    cmp r0,#0x0                              @ 080ccb84 0028
    beq LAB_080ccba8                         @ 080ccb86 0fd0
    ldr r2, DAT_080ccba4                     @ 080ccb88 064a
    ldrb r1,[r2,#0x0]                        @ 080ccb8a 1178
    movs r0,#0x4    @ 080ccb8c 0420
    ands r0,r1    @ 080ccb8e 0840
    cmp r0,#0x0                              @ 080ccb90 0028
    bne LAB_080ccb9c                         @ 080ccb92 03d1
    movs r0,#0x3    @ 080ccb94 0320
    rsbs r0,r0,#0    @ 080ccb96 4042
    ands r0,r1    @ 080ccb98 0840
    strb r0,[r2,#0x0]                        @ 080ccb9a 1070
LAB_080ccb9c:
    bl zero_duel_lp_display_counters         @ 080ccb9c caf796f9
    b switchD_080ccab0__default              @ 080ccba0 24e1
    .zero  0x2
DAT_080ccba4:
    .word  0x0201fe60                     @ 080ccba4 60fe0102
LAB_080ccba8:
    ldr r4, DAT_080ccbdc                     @ 080ccba8 0c4c
    movs r0,#0x84    @ 080ccbaa 8420
    lsls r0,r0,#0x2    @ 080ccbac 8000
    adds r6,r4,r0    @ 080ccbae 2618
    ldrh r0,[r6,#0x0]                        @ 080ccbb0 3088
    bl apply_zone_cursor_step                @ 080ccbb2 faf7dbfa
    bl setup_zone_oam_entry_by_field_slot    @ 080ccbb6 f8f745fc
    bl render_duel_field_slot_oam_grid       @ 080ccbba fbf775ff
    movs r1,#0x87    @ 080ccbbe 8721
    lsls r1,r1,#0x2    @ 080ccbc0 8900
    adds r0,r4,r1    @ 080ccbc2 6018
    ldrh r5,[r0,#0x0]                        @ 080ccbc4 0588
    cmp r5,#0x0                              @ 080ccbc6 002d
    beq LAB_080ccbe4                         @ 080ccbc8 0cd0
    ldr r2, DAT_080ccbe0                     @ 080ccbca 054a
    adds r0,r4,r2    @ 080ccbcc a018
    movs r1,#0x10    @ 080ccbce 1021
    ldrb r3,[r0,#0x0]                        @ 080ccbd0 0378
    orrs r1,r3    @ 080ccbd2 1943
    strb r1,[r0,#0x0]                        @ 080ccbd4 0170
    movs r0,#0x2    @ 080ccbd6 0220
    strb r0,[r4,#0x0]                        @ 080ccbd8 2070
    b switchD_080ccab0__default              @ 080ccbda 07e1
DAT_080ccbdc:
    .word  0x02023130                     @ 080ccbdc 30310202
DAT_080ccbe0:
    .word  0x00000222                     @ 080ccbe0 22020000
LAB_080ccbe4:
    movs r0,#0x8    @ 080ccbe4 0820
    ldrh r7,[r7,#0x0]                        @ 080ccbe6 3f88
    ands r0,r7    @ 080ccbe8 3840
    cmp r0,#0x0                              @ 080ccbea 0028
    beq LAB_080ccc28                         @ 080ccbec 1cd0
    ldrh r0,[r6,#0x0]                        @ 080ccbee 3088
    bl check_zone_card_id_cache_valid        @ 080ccbf0 faf744fa
    cmp r0,#0x0                              @ 080ccbf4 0028
    beq LAB_080ccc28                         @ 080ccbf6 17d0
    ldr r0, DAT_080ccc1c                     @ 080ccbf8 0848
    adds r0,#0x29    @ 080ccbfa 2930
    strb r5,[r0,#0x0]                        @ 080ccbfc 0570
    ldr r0, DAT_080ccc20                     @ 080ccbfe 0848
    adds r1,r4,r0    @ 080ccc00 2118
    movs r0,#0x4    @ 080ccc02 0420
    ldrb r2,[r1,#0x0]                        @ 080ccc04 0a78
    orrs r0,r2    @ 080ccc06 1043
    strb r0,[r1,#0x0]                        @ 080ccc08 0870
    ldr r3, DAT_080ccc24                     @ 080ccc0a 064b
    adds r1,r4,r3    @ 080ccc0c e118
    movs r0,#0x10    @ 080ccc0e 1020
    ldrb r2,[r1,#0x0]                        @ 080ccc10 0a78
    orrs r0,r2    @ 080ccc12 1043
    strb r0,[r1,#0x0]                        @ 080ccc14 0870
    movs r0,#0x3    @ 080ccc16 0320
    strb r0,[r4,#0x0]                        @ 080ccc18 2070
    b switchD_080ccab0__default              @ 080ccc1a e7e0
DAT_080ccc1c:
    .word  0x0201ff30                     @ 080ccc1c 30ff0102
DAT_080ccc20:
    .word  0x00000215                     @ 080ccc20 15020000
DAT_080ccc24:
    .word  0x00000222                     @ 080ccc24 22020000
LAB_080ccc28:
    ldr r1, PTR_gPrng_080ccc5c               @ 080ccc28 0c49
    movs r3,#0xa4    @ 080ccc2a a423
    lsls r3,r3,#0x1    @ 080ccc2c 5b00
    adds r1,r1,r3    @ 080ccc2e c918
    movs r0,#0x4    @ 080ccc30 0420
    ldrh r1,[r1,#0x0]                        @ 080ccc32 0988
    ands r0,r1    @ 080ccc34 0840
    cmp r0,#0x0                              @ 080ccc36 0028
    beq LAB_080ccc64                         @ 080ccc38 14d0
    ldr r2, DAT_080ccc60                     @ 080ccc3a 094a
    movs r1,#0x88    @ 080ccc3c 8821
    lsls r1,r1,#0x2    @ 080ccc3e 8900
    adds r0,r2,r1    @ 080ccc40 5018
    ldr r0,[r0,#0x0]                         @ 080ccc42 0068
    movs r1,#0xff    @ 080ccc44 ff21
    lsls r1,r1,#0xa    @ 080ccc46 8902
    ands r0,r1    @ 080ccc48 0840
    movs r1,#0x80    @ 080ccc4a 8021
    lsls r1,r1,#0x5    @ 080ccc4c 4901
    cmp r0,r1                                @ 080ccc4e 8842
    bne LAB_080ccc64                         @ 080ccc50 08d1
    movs r1,#0x0    @ 080ccc52 0021
    movs r0,#0x4    @ 080ccc54 0420
    strb r0,[r2,#0x0]                        @ 080ccc56 1070
    strb r1,[r2,#0x1]                        @ 080ccc58 5170
    b switchD_080ccab0__default              @ 080ccc5a c7e0
PTR_gPrng_080ccc5c:
    .word  gPrng                          @ 080ccc5c 40000003
DAT_080ccc60:
    .word  0x02023130                     @ 080ccc60 30310202
LAB_080ccc64:
    bl get_lp_display_anim_counter           @ 080ccc64 c9f786fe
    cmp r0,#0x1                              @ 080ccc68 0128
    beq LAB_080ccc6e                         @ 080ccc6a 00d0
    b LAB_080cca90                           @ 080ccc6c 10e7
LAB_080ccc6e:
    ldr r0, DAT_080cccb8                     @ 080ccc6e 1248
    movs r2,#0x84    @ 080ccc70 8422
    lsls r2,r2,#0x2    @ 080ccc72 9200
    adds r0,r0,r2    @ 080ccc74 8018
    ldrh r2,[r0,#0x0]                        @ 080ccc76 0288
    movs r1,#0x80    @ 080ccc78 8021
    adds r0,r2,#0x0    @ 080ccc7a 101c
    ands r0,r1    @ 080ccc7c 0840
    lsls r0,r0,#0x18    @ 080ccc7e 0006
    lsrs r3,r0,#0x1f    @ 080ccc80 c30f
    movs r0,#0x7f    @ 080ccc82 7f20
    ands r2,r0    @ 080ccc84 0240
    ldr r1, PTR_gPrng_080cccbc               @ 080ccc86 0d49
    movs r0,#0xa4    @ 080ccc88 a420
    lsls r0,r0,#0x1    @ 080ccc8a 4000
    adds r1,r1,r0    @ 080ccc8c 0918
    subs r0,#0x48    @ 080ccc8e 4838
    ldrh r1,[r1,#0x0]                        @ 080ccc90 0988
    ands r0,r1    @ 080ccc92 0840
    cmp r0,#0x0                              @ 080ccc94 0028
    bne LAB_080ccc9a                         @ 080ccc96 00d1
    b LAB_080cca90                           @ 080ccc98 fae6
LAB_080ccc9a:
    ldr r0, DAT_080cccc0                     @ 080ccc9a 0948
    ldr r0,[r0,#0x4]                         @ 080ccc9c 4068
    cmp r3,r0                                @ 080ccc9e 8342
    beq LAB_080ccca4                         @ 080ccca0 00d0
    b LAB_080cca90                           @ 080ccca2 f5e6
LAB_080ccca4:
    cmp r2,#0xd                              @ 080ccca4 0d2a
    beq LAB_080cccaa                         @ 080ccca6 00d0
    b LAB_080cca90                           @ 080ccca8 f2e6
LAB_080cccaa:
    adds r0,r3,#0x0    @ 080cccaa 181c
    movs r1,#0xd    @ 080cccac 0d21
    movs r2,#0x0    @ 080cccae 0022
    movs r3,#0xc    @ 080cccb0 0c23
    bl init_duel_zone_target_slot_refs       @ 080cccb2 caf7aff8
    b LAB_080cca90                           @ 080cccb6 ebe6
DAT_080cccb8:
    .word  0x02023130                     @ 080cccb8 30310202
PTR_gPrng_080cccbc:
    .word  gPrng                          @ 080cccbc 40000003
DAT_080cccc0:
    .word  0x0201e2a0                     @ 080cccc0 a0e20102
switchD_080ccab0__caseD_1:
    bl tick_card_sprite_oam_phase_dispatch   @ 080cccc4 f9f774fc
    cmp r0,#0x0                              @ 080cccc8 0028
    bne LAB_080cccce                         @ 080cccca 00d1
    b switchD_080ccab0__default              @ 080ccccc 8ee0
LAB_080cccce:
    ldr r1, DAT_080cccd8                     @ 080cccce 0249
    movs r0,#0x0    @ 080cccd0 0020
    strb r0,[r1,#0x0]                        @ 080cccd2 0870
    b LAB_080ccdee                           @ 080cccd4 8be0
    .zero  0x2
DAT_080cccd8:
    .word  0x02023130                     @ 080cccd8 30310202
switchD_080ccab0__caseD_2:
    bl advance_card_display_effect_step      @ 080cccdc fcf7daff
    cmp r0,#0x0                              @ 080ccce0 0028
    bne LAB_080ccce6                         @ 080ccce2 00d1
    b switchD_080ccab0__default              @ 080ccce4 82e0
LAB_080ccce6:
    ldr r2, DAT_080cccf4                     @ 080ccce6 034a
    ldr r3, DAT_080cccf8                     @ 080ccce8 034b
    adds r1,r2,r3    @ 080cccea d118
    movs r0,#0x11    @ 080cccec 1120
    rsbs r0,r0,#0    @ 080cccee 4042
    b LAB_080ccd46                           @ 080cccf0 29e0
    .zero  0x2
DAT_080cccf4:
    .word  0x02023130                     @ 080cccf4 30310202
DAT_080cccf8:
    .word  0x00000222                     @ 080cccf8 22020000
switchD_080ccab0__caseD_3:
    ldr r0, PTR_gPrng_080ccd54               @ 080cccfc 1548
    movs r1,#0x85    @ 080cccfe 8521
    lsls r1,r1,#0x2    @ 080ccd00 8900
    adds r0,r0,r1    @ 080ccd02 4018
    ldr r0,[r0,#0x0]                         @ 080ccd04 0068
    lsls r0,r0,#0x1    @ 080ccd06 4000
    lsrs r0,r0,#0x1    @ 080ccd08 4008
    movs r1,#0x3c    @ 080ccd0a 3c21
    bl __divsi3                              @ 080ccd0c 41f07afc
    cmp r0,#0xb3                             @ 080ccd10 b328
    ble LAB_080ccd26                         @ 080ccd12 08dd
    ldr r2, DAT_080ccd58                     @ 080ccd14 104a
    adds r0,r4,r2    @ 080ccd16 a018
    movs r1,#0xd    @ 080ccd18 0d21
    rsbs r1,r1,#0    @ 080ccd1a 4942
    ldrb r3,[r0,#0x0]                        @ 080ccd1c 0378
    ands r1,r3    @ 080ccd1e 1940
    movs r2,#0x4    @ 080ccd20 0422
    orrs r1,r2    @ 080ccd22 1143
    strb r1,[r0,#0x0]                        @ 080ccd24 0170
LAB_080ccd26:
    bl dispatch_duel_zone_pair_to_oam        @ 080ccd26 f9f7c7fb
    cmp r0,#0x0                              @ 080ccd2a 0028
    beq switchD_080ccab0__default            @ 080ccd2c 5ed0
    ldr r2, DAT_080ccd5c                     @ 080ccd2e 0b4a
    ldr r0, DAT_080ccd58                     @ 080ccd30 0948
    adds r1,r2,r0    @ 080ccd32 1118
    movs r0,#0x11    @ 080ccd34 1120
    rsbs r0,r0,#0    @ 080ccd36 4042
    ldrb r3,[r1,#0x0]                        @ 080ccd38 0b78
    ands r0,r3    @ 080ccd3a 1840
    strb r0,[r1,#0x0]                        @ 080ccd3c 0870
    ldr r0, DAT_080ccd60                     @ 080ccd3e 0848
    adds r1,r2,r0    @ 080ccd40 1118
    movs r0,#0x5    @ 080ccd42 0520
    rsbs r0,r0,#0    @ 080ccd44 4042
LAB_080ccd46:
    ldrb r3,[r1,#0x0]                        @ 080ccd46 0b78
    ands r0,r3    @ 080ccd48 1840
    strb r0,[r1,#0x0]                        @ 080ccd4a 0870
    movs r0,#0x0    @ 080ccd4c 0020
    strb r0,[r2,#0x0]                        @ 080ccd4e 1070
    b LAB_080ccdee                           @ 080ccd50 4de0
    .zero  0x2
PTR_gPrng_080ccd54:
    .word  gPrng                          @ 080ccd54 40000003
DAT_080ccd58:
    .word  0x00000222                     @ 080ccd58 22020000
DAT_080ccd5c:
    .word  0x02023130                     @ 080ccd5c 30310202
DAT_080ccd60:
    .word  0x00000215                     @ 080ccd60 15020000
switchD_080ccab0__caseD_4:
    ldrb r0,[r4,#0x1]                        @ 080ccd64 6078
    cmp r0,#0x1                              @ 080ccd66 0128
    beq LAB_080ccdac                         @ 080ccd68 20d0
    cmp r0,#0x1                              @ 080ccd6a 0128
    bgt LAB_080ccd74                         @ 080ccd6c 02dc
    cmp r0,#0x0                              @ 080ccd6e 0028
    beq LAB_080ccd7e                         @ 080ccd70 05d0
    b LAB_080ccde4                           @ 080ccd72 37e0
LAB_080ccd74:
    cmp r0,#0x2                              @ 080ccd74 0228
    beq LAB_080ccdb2                         @ 080ccd76 1cd0
    cmp r0,#0x3                              @ 080ccd78 0328
    beq LAB_080ccdd4                         @ 080ccd7a 2bd0
    b LAB_080ccde4                           @ 080ccd7c 32e0
LAB_080ccd7e:
    bl tick_duel_field_fadein_step           @ 080ccd7e fff76dfe
    cmp r0,#0x0                              @ 080ccd82 0028
    beq switchD_080ccab0__default            @ 080ccd84 32d0
    ldr r0, DAT_080ccda4                     @ 080ccd86 0748
    adds r1,r4,r0    @ 080ccd88 2118
    movs r0,#0x4    @ 080ccd8a 0420
    ldrb r2,[r1,#0x0]                        @ 080ccd8c 0a78
    orrs r0,r2    @ 080ccd8e 1043
    strb r0,[r1,#0x0]                        @ 080ccd90 0870
    ldr r0, PTR_gPrng_080ccda8               @ 080ccd92 0548
    movs r3,#0x8f    @ 080ccd94 8f23
    lsls r3,r3,#0x2    @ 080ccd96 9b00
    adds r0,r0,r3    @ 080ccd98 c018
    ldrh r0,[r0,#0x0]                        @ 080ccd9a 0088
    bl init_card_name_result_screen          @ 080ccd9c 5ff764ff
    b LAB_080ccddc                           @ 080ccda0 1ce0
    .zero  0x2
DAT_080ccda4:
    .word  0x00000215                     @ 080ccda4 15020000
PTR_gPrng_080ccda8:
    .word  gPrng                          @ 080ccda8 40000003
LAB_080ccdac:
    bl tick_scene_blend_fade_sequence        @ 080ccdac 60f712f9
    b LAB_080ccdd8                           @ 080ccdb0 12e0
LAB_080ccdb2:
    bl init_duel_field_vram_layout           @ 080ccdb2 fff7a7fd
    bl refresh_duel_field_zone_info          @ 080ccdb6 fff7a9f8
    bl refresh_zone_effect_buff_cache        @ 080ccdba fbf7b9ff
    ldr r1, DAT_080ccdd0                     @ 080ccdbe 0449
    adds r0,r4,r1    @ 080ccdc0 6018
    movs r1,#0x5    @ 080ccdc2 0521
    rsbs r1,r1,#0    @ 080ccdc4 4942
    ldrb r2,[r0,#0x0]                        @ 080ccdc6 0278
    ands r1,r2    @ 080ccdc8 1140
    strb r1,[r0,#0x0]                        @ 080ccdca 0170
    b LAB_080ccddc                           @ 080ccdcc 06e0
    .zero  0x2
DAT_080ccdd0:
    .word  0x00000215                     @ 080ccdd0 15020000
LAB_080ccdd4:
    bl tick_duel_field_fadeout_step          @ 080ccdd4 fff730fe
LAB_080ccdd8:
    cmp r0,#0x0                              @ 080ccdd8 0028
    beq switchD_080ccab0__default            @ 080ccdda 07d0
LAB_080ccddc:
    ldrb r0,[r4,#0x1]                        @ 080ccddc 6078
    adds r0,#0x1    @ 080ccdde 0130
    strb r0,[r4,#0x1]                        @ 080ccde0 6070
    b switchD_080ccab0__default              @ 080ccde2 03e0
LAB_080ccde4:
    movs r0,#0x0    @ 080ccde4 0020
    strb r0,[r4,#0x0]                        @ 080ccde6 2070
    strb r0,[r4,#0x1]                        @ 080ccde8 6070
    b LAB_080ccdee                           @ 080ccdea 00e0
switchD_080ccab0__default:
    movs r0,#0x1    @ 080ccdec 0120
LAB_080ccdee:
    pop {r4,r5,r6,r7}                        @ 080ccdee f0bc
    pop {r1}                                 @ 080ccdf0 02bc
    bx r1                                    @ 080ccdf2 0847

@ Called by tick_duel_field_main_frame (0x0801e984). Top-level dispatch for duel field OAM rendering. Reads [0x02023130+0x215] bits 1 and 0: if bit1 nonzero and bit0 zero, checks bit4 to conditionally call render_field_aob_slot_oam_row (FUN_080c8e6c). Reads [0x02023130+0x215] bit0 and 0x0201ff30 bit0 as dual guard; if both zero continues. Reads gP1LifePoints+0x1cf4: if==3 calls render_aob_zone_slot_oam (FUN_080c8c58). Unconditionally calls render_duel_field_zone_oam_grid (FUN_080c8d68) and render_lp_zone_oam_full (FUN_080ca42c). Checks bit0 on two flags: if both zero calls render_field_zone_mini_card_tiles. Checks bit3: if zero calls render_player_zone_active_oam (FUN_080c8870). Exit: void (push {lr} only).
@ 
@ Constants:
@ - BASE=0x02023130 (IWRAM duel field state)
@ - RENDER_FLAG_OFFSET=0x215 (multi-purpose flag byte)
@ - BIT0=mask LP/AOB render
@ - BIT1=mask LP render
@ - BIT2=mask AOB zone
@ - BIT3=mask player zone active indicator
@ - BIT4=enable AOB slot row render
@ - SECOND_GUARD=0x0201ff30 (bit0=global mask)
@ - LP_STATE_FIELD=gP1LifePoints+0x1cf4 (value==3 -> AOB zone)
render_duel_field_oam_all:
    push {lr}                                @ 080ccdf4 00b5
    ldr r0, DAT_080cce98                     @ 080ccdf6 2848
    ldr r1, DAT_080cce9c                     @ 080ccdf8 2849
    adds r0,r0,r1    @ 080ccdfa 4018
    ldrb r3,[r0,#0x0]                        @ 080ccdfc 0378
    movs r0,#0x2    @ 080ccdfe 0220
    ands r0,r3    @ 080cce00 1840
    cmp r0,#0x0                              @ 080cce02 0028
    beq LAB_080cce94                         @ 080cce04 46d0
    ldr r1, DAT_080ccea0                     @ 080cce06 2649
    movs r2,#0x1    @ 080cce08 0122
    adds r0,r2,#0x0    @ 080cce0a 101c
    ldrb r1,[r1,#0x0]                        @ 080cce0c 0978
    ands r0,r1    @ 080cce0e 0840
    cmp r0,#0x0                              @ 080cce10 0028
    bne LAB_080cce2c                         @ 080cce12 0bd1
    ldr r1, DAT_080ccea4                     @ 080cce14 2349
    adds r0,r2,#0x0    @ 080cce16 101c
    ldrb r1,[r1,#0x0]                        @ 080cce18 0978
    ands r0,r1    @ 080cce1a 0840
    cmp r0,#0x0                              @ 080cce1c 0028
    bne LAB_080cce2c                         @ 080cce1e 05d1
    movs r0,#0x10    @ 080cce20 1020
    ands r0,r3    @ 080cce22 1840
    cmp r0,#0x0                              @ 080cce24 0028
    beq LAB_080cce2c                         @ 080cce26 01d0
    bl render_field_aob_slot_oam_row         @ 080cce28 fcf720f8
LAB_080cce2c:
    ldr r0, PTR_gP1LifePoints_080ccea8       @ 080cce2c 1e48
    ldr r1, DAT_080cceac                     @ 080cce2e 1f49
    adds r0,r0,r1    @ 080cce30 4018
    ldr r0,[r0,#0x0]                         @ 080cce32 0068
    cmp r0,#0x3                              @ 080cce34 0328
    bne LAB_080cce3c                         @ 080cce36 01d1
    bl render_aob_zone_slot_oam              @ 080cce38 fbf70eff
LAB_080cce3c:
    ldr r2, DAT_080cce98                     @ 080cce3c 164a
    ldr r0, DAT_080cce9c                     @ 080cce3e 1748
    adds r1,r2,r0    @ 080cce40 1118
    movs r0,#0x4    @ 080cce42 0420
    ldrb r1,[r1,#0x0]                        @ 080cce44 0978
    ands r0,r1    @ 080cce46 0840
    cmp r0,#0x0                              @ 080cce48 0028
    bne LAB_080cce56                         @ 080cce4a 04d1
    ldrb r0,[r2,#0xa]                        @ 080cce4c 907a
    cmp r0,#0x0                              @ 080cce4e 0028
    beq LAB_080cce56                         @ 080cce50 01d0
    bl render_deck_zone_count_oam            @ 080cce52 fcf7e1f9
LAB_080cce56:
    bl render_duel_field_zone_oam_grid       @ 080cce56 fbf787ff
    bl render_lp_zone_oam_full               @ 080cce5a fdf7e7fa
    ldr r1, DAT_080ccea0                     @ 080cce5e 1049
    movs r2,#0x1    @ 080cce60 0122
    adds r0,r2,#0x0    @ 080cce62 101c
    ldrb r1,[r1,#0x0]                        @ 080cce64 0978
    ands r0,r1    @ 080cce66 0840
    cmp r0,#0x0                              @ 080cce68 0028
    bne LAB_080cce80                         @ 080cce6a 09d1
    ldr r1, DAT_080cceb0                     @ 080cce6c 1049
    ldr r0, DAT_080cceb4                     @ 080cce6e 1148
    adds r1,r1,r0    @ 080cce70 0918
    adds r0,r2,#0x0    @ 080cce72 101c
    ldrb r1,[r1,#0x0]                        @ 080cce74 0978
    ands r0,r1    @ 080cce76 0840
    cmp r0,#0x0                              @ 080cce78 0028
    bne LAB_080cce80                         @ 080cce7a 01d1
    bl render_field_zone_mini_card_tiles     @ 080cce7c f6f768fe
LAB_080cce80:
    ldr r1, DAT_080cce98                     @ 080cce80 0549
    ldr r0, DAT_080cce9c                     @ 080cce82 0648
    adds r1,r1,r0    @ 080cce84 0918
    movs r0,#0x8    @ 080cce86 0820
    ldrb r1,[r1,#0x0]                        @ 080cce88 0978
    ands r0,r1    @ 080cce8a 0840
    cmp r0,#0x0                              @ 080cce8c 0028
    bne LAB_080cce94                         @ 080cce8e 01d1
    bl render_player_zone_active_oam         @ 080cce90 fbf7eefc
LAB_080cce94:
    pop {r0}                                 @ 080cce94 01bc
    bx r0                                    @ 080cce96 0047
DAT_080cce98:
    .word  0x02023130                     @ 080cce98 30310202
DAT_080cce9c:
    .word  0x00000215                     @ 080cce9c 15020000
DAT_080ccea0:
    .word  0x0201f440                     @ 080ccea0 40f40102
DAT_080ccea4:
    .word  0x0201ff30                     @ 080ccea4 30ff0102
PTR_gP1LifePoints_080ccea8:
    .word  gP1LifePoints                  @ 080ccea8 e0c40102
DAT_080cceac:
    .word  0x00001cf4                     @ 080cceac f41c0000
DAT_080cceb0:
    .word  0x02020160                     @ 080cceb0 60010202
DAT_080cceb4:
    .word  0x00002f51                     @ 080cceb4 512f0000

@ Initialize BG tile VRAM for choice label display variant case 8 (eighth option). Writes tile map entries for the eighth choice label position in the card choice UI. No APCS params; reads choice_display_state from globals. Returns void. Side effects: BG map VRAM written for choice label case 8. Sibling: init_choice_label_vram_case1.
init_choice_label_vram_case8:
    push {lr}                                @ 080cceb8 00b5
    ldr r0, DAT_080ccf18                     @ 080cceba 1748
    movs r1,#0x80    @ 080ccebc 8021
    lsls r1,r1,#0x7    @ 080ccebe c901
    bl zero_fill_by_halfword                 @ 080ccec0 27f0d8ff
    ldr r0, DAT_080ccf1c                     @ 080ccec4 1548
    ldr r1, DAT_080ccf20                     @ 080ccec6 1649
    movs r2,#0x1    @ 080ccec8 0122
    movs r3,#0x1    @ 080cceca 0123
    bl tile_2d_row_copy                      @ 080ccecc 2af002fb
    ldr r3, DAT_080ccf24                     @ 080cced0 144b
    ldr r1, DAT_080ccf28                     @ 080cced2 1549
    adds r0,r3,r1    @ 080cced4 5818
    ldrb r0,[r0,#0x0]                        @ 080cced6 0078
    lsrs r2,r0,#0x1    @ 080cced8 4208
    ldr r0, DAT_080ccf2c                     @ 080cceda 1448
    adds r1,r3,r0    @ 080ccedc 1918
    movs r0,#0x1    @ 080ccede 0120
    ldrb r1,[r1,#0x0]                        @ 080ccee0 0978
    ands r0,r1    @ 080ccee2 0840
    lsls r0,r0,#0x7    @ 080ccee4 c001
    orrs r0,r2    @ 080ccee6 1043
    cmp r0,#0x0                              @ 080ccee8 0028
    bne LAB_080ccfc8                         @ 080cceea 6dd1
    ldr r1, DAT_080ccf30                     @ 080cceec 1049
    adds r3,r3,r1    @ 080cceee 5b18
    ldr r0, DAT_080ccf34                     @ 080ccef0 1048
    ldr r1, DAT_080ccf38                     @ 080ccef2 1149
    adds r0,r0,r1    @ 080ccef4 4018
    movs r2,#0x7    @ 080ccef6 0722
    ldrb r0,[r0,#0x0]                        @ 080ccef8 0078
    ands r2,r0    @ 080ccefa 0240
    cmp r2,#0x1                              @ 080ccefc 012a
    beq LAB_080ccf5c                         @ 080ccefe 2dd0
    cmp r2,#0x2                              @ 080ccf00 022a
    beq LAB_080ccf54                         @ 080ccf02 27d0
    cmp r2,#0x3                              @ 080ccf04 032a
    beq LAB_080ccf4c                         @ 080ccf06 21d0
    cmp r2,#0x4                              @ 080ccf08 042a
    beq LAB_080ccf44                         @ 080ccf0a 1bd0
    ldr r1, DAT_080ccf3c                     @ 080ccf0c 0b49
    cmp r2,#0x5                              @ 080ccf0e 052a
    bne LAB_080ccf5e                         @ 080ccf10 25d1
    ldr r0, DAT_080ccf40                     @ 080ccf12 0b48
    adds r1,r1,r0    @ 080ccf14 0918
    b LAB_080ccf5e                           @ 080ccf16 22e0
DAT_080ccf18:
    .word  0x06014000                     @ 080ccf18 00400106
DAT_080ccf1c:
    .word  0x06010c00                     @ 080ccf1c 000c0106
DAT_080ccf20:
    .word  0x0988ab18                     @ 080ccf20 18ab8809
DAT_080ccf24:
    .word  0x0201f440                     @ 080ccf24 40f40102
DAT_080ccf28:
    .word  0x00000a17                     @ 080ccf28 170a0000
DAT_080ccf2c:
    .word  0x00000a18                     @ 080ccf2c 180a0000
DAT_080ccf30:
    .word  0x00000201                     @ 080ccf30 01020000
DAT_080ccf34:
    .word  0x02000000                     @ 080ccf34 00000002
DAT_080ccf38:
    .word  0x00006c2c                     @ 080ccf38 2c6c0000
DAT_080ccf3c:
    .word  0x09dbd7cc                     @ 080ccf3c ccd7db09
DAT_080ccf40:
    .word  0x0003a910                     @ 080ccf40 10a90300
LAB_080ccf44:
    ldr r1, DAT_080ccf48                     @ 080ccf44 0049
    b LAB_080ccf5e                           @ 080ccf46 0ae0
DAT_080ccf48:
    .word  0x09dec2c6                     @ 080ccf48 c6c2de09
LAB_080ccf4c:
    ldr r1, DAT_080ccf50                     @ 080ccf4c 0049
    b LAB_080ccf5e                           @ 080ccf4e 06e0
DAT_080ccf50:
    .word  0x09ddffc8                     @ 080ccf50 c8ffdd09
LAB_080ccf54:
    ldr r1, DAT_080ccf58                     @ 080ccf54 0049
    b LAB_080ccf5e                           @ 080ccf56 02e0
DAT_080ccf58:
    .word  0x09dd3cec                     @ 080ccf58 ec3cdd09
LAB_080ccf5c:
    ldr r1, DAT_080ccf90                     @ 080ccf5c 0c49
LAB_080ccf5e:
    adds r0,r3,#0x0    @ 080ccf5e 181c
    bl copy_cstr_to_buf                      @ 080ccf60 28f078f8
    ldr r3, DAT_080ccf94                     @ 080ccf64 0b4b
    ldr r0, DAT_080ccf98                     @ 080ccf66 0c48
    ldr r1, DAT_080ccf9c                     @ 080ccf68 0c49
    adds r0,r0,r1    @ 080ccf6a 4018
    movs r2,#0x7    @ 080ccf6c 0722
    ldrb r0,[r0,#0x0]                        @ 080ccf6e 0078
    ands r2,r0    @ 080ccf70 0240
    cmp r2,#0x1                              @ 080ccf72 012a
    beq LAB_080ccfc0                         @ 080ccf74 24d0
    cmp r2,#0x2                              @ 080ccf76 022a
    beq LAB_080ccfb8                         @ 080ccf78 1ed0
    cmp r2,#0x3                              @ 080ccf7a 032a
    beq LAB_080ccfb0                         @ 080ccf7c 18d0
    cmp r2,#0x4                              @ 080ccf7e 042a
    beq LAB_080ccfa8                         @ 080ccf80 12d0
    ldr r1, DAT_080ccfa0                     @ 080ccf82 0749
    cmp r2,#0x5                              @ 080ccf84 052a
    bne LAB_080ccfc2                         @ 080ccf86 1cd1
    ldr r0, DAT_080ccfa4                     @ 080ccf88 0648
    adds r1,r1,r0    @ 080ccf8a 0918
    b LAB_080ccfc2                           @ 080ccf8c 19e0
    .zero  0x2
DAT_080ccf90:
    .word  0x09dc882a                     @ 080ccf90 2a88dc09
DAT_080ccf94:
    .word  0x0201f841                     @ 080ccf94 41f80102
DAT_080ccf98:
    .word  0x02000000                     @ 080ccf98 00000002
DAT_080ccf9c:
    .word  0x00006c2c                     @ 080ccf9c 2c6c0000
DAT_080ccfa0:
    .word  0x09dbd7d4                     @ 080ccfa0 d4d7db09
DAT_080ccfa4:
    .word  0x0003a90e                     @ 080ccfa4 0ea90300
LAB_080ccfa8:
    ldr r1, DAT_080ccfac                     @ 080ccfa8 0049
    b LAB_080ccfc2                           @ 080ccfaa 0ae0
DAT_080ccfac:
    .word  0x09dec2cc                     @ 080ccfac ccc2de09
LAB_080ccfb0:
    ldr r1, DAT_080ccfb4                     @ 080ccfb0 0049
    b LAB_080ccfc2                           @ 080ccfb2 06e0
DAT_080ccfb4:
    .word  0x09ddffce                     @ 080ccfb4 ceffdd09
LAB_080ccfb8:
    ldr r1, DAT_080ccfbc                     @ 080ccfb8 0049
    b LAB_080ccfc2                           @ 080ccfba 02e0
DAT_080ccfbc:
    .word  0x09dd3cf2                     @ 080ccfbc f23cdd09
LAB_080ccfc0:
    ldr r1, DAT_080ccfd8                     @ 080ccfc0 0549
LAB_080ccfc2:
    adds r0,r3,#0x0    @ 080ccfc2 181c
    bl copy_cstr_to_buf                      @ 080ccfc4 28f046f8
LAB_080ccfc8:
    ldr r0, DAT_080ccfdc                     @ 080ccfc8 0448
    ldr r1, DAT_080ccfe0                     @ 080ccfca 0549
    adds r0,r0,r1    @ 080ccfcc 4018
    movs r1,#0x8    @ 080ccfce 0821
    strb r1,[r0,#0x0]                        @ 080ccfd0 0170
    pop {r0}                                 @ 080ccfd2 01bc
    bx r0                                    @ 080ccfd4 0047
    .zero  0x2
DAT_080ccfd8:
    .word  0x09dc8830                     @ 080ccfd8 3088dc09
DAT_080ccfdc:
    .word  0x0201f440                     @ 080ccfdc 40f40102
DAT_080ccfe0:
    .word  0x00000a01                     @ 080ccfe0 010a0000

@ 由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). 与 080d04dc 结构完全对称: 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); 设置语言模式标志 (STATE+0x8 bit[1..2]); 从 font_jp_base_table 取字体基址; 以 STATE_DATA (0x0201f441) 为源调用 render_jp_string_to_tile_line 两次 (循环 r6 in [0..1], 步进 0x200 字节); 完成后 write_line_buf_to_bg_tile_vram 刷新到 BG tile VRAM (0x06014000). 两函数共用同一 STATE_BASE (0x02006ed0) / STATE_DATA (0x0201f441) / VRAM / 字体配置, 仅写入的 STATE 字段偏移略有差异. Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, VRAM_BG=0x06014000, FONT_SIZE=0x200, LOOP_RANGE=[0..1].
render_jp_two_line_text_to_bg_vram_alt:
    push {r4,r5,r6,r7,lr}                    @ 080ccfe4 f0b5
    .hword 0x4657    @ 080ccfe6 5746
    .hword 0x464e    @ 080ccfe8 4e46
    .hword 0x4645    @ 080ccfea 4546
    push {r5,r6,r7}                          @ 080ccfec e0b4
    sub sp,#0x4                              @ 080ccfee 81b0
    movs r0,#0x2    @ 080ccff0 0220
    .hword 0x4682    @ 080ccff2 8246
    movs r6,#0x0    @ 080ccff4 0026
    movs r0,#0x17    @ 080ccff6 1720
    movs r1,#0x10    @ 080ccff8 1021
    movs r2,#0x1    @ 080ccffa 0122
    movs r3,#0x2    @ 080ccffc 0223
    bl setup_line_buf_with_font_and_align    @ 080ccffe 23f05ffe
    ldr r2, DAT_080cd0c0                     @ 080cd002 2f4a
    ldr r0, DAT_080cd0c4                     @ 080cd004 2f48
    ldr r1, DAT_080cd0c8                     @ 080cd006 3049
    adds r0,r0,r1    @ 080cd008 4018
    movs r1,#0x7    @ 080cd00a 0721
    ldrb r0,[r0,#0x0]                        @ 080cd00c 0078
    ands r1,r0    @ 080cd00e 0140
    rsbs r1,r1,#0    @ 080cd010 4942
    lsrs r1,r1,#0x1f    @ 080cd012 c90f
    movs r0,#0x2    @ 080cd014 0220
    rsbs r0,r0,#0    @ 080cd016 4042
    ldrb r3,[r2,#0x8]                        @ 080cd018 137a
    ands r0,r3    @ 080cd01a 1840
    orrs r0,r1    @ 080cd01c 0843
    movs r1,#0x2    @ 080cd01e 0221
    orrs r0,r1    @ 080cd020 0843
    strb r0,[r2,#0x8]                        @ 080cd022 1072
    ldr r3, PTR_font_jp_base_table_080cd0cc  @ 080cd024 294b
    lsls r1,r0,#0x1e    @ 080cd026 8107
    lsrs r1,r1,#0x1f    @ 080cd028 c90f
    lsls r1,r1,#0x2    @ 080cd02a 8900
    lsls r0,r0,#0x1f    @ 080cd02c c007
    lsrs r0,r0,#0x1f    @ 080cd02e c00f
    lsls r0,r0,#0x3    @ 080cd030 c000
    adds r1,r1,r0    @ 080cd032 0918
    adds r1,r1,r3    @ 080cd034 c918
    ldr r0,[r1,#0x0]                         @ 080cd036 0868
    str r0,[r2,#0x4]                         @ 080cd038 5060
    movs r0,#0x40    @ 080cd03a 4020
    ldrb r1,[r2,#0x15]                       @ 080cd03c 517d
    orrs r0,r1    @ 080cd03e 0843
    strb r0,[r2,#0x15]                       @ 080cd040 5075
    ldr r4, DAT_080cd0d0                     @ 080cd042 234c
    str r6,[sp,#0x0]                         @ 080cd044 0096
    movs r0,#0x2    @ 080cd046 0220
    movs r1,#0x2    @ 080cd048 0221
    adds r2,r4,#0x0    @ 080cd04a 221c
    movs r3,#0xc    @ 080cd04c 0c23
    bl render_jp_string_to_tile_line         @ 080cd04e faf737fb
    adds r5,r0,#0x0    @ 080cd052 051c
    subs r3,r4,#0x1    @ 080cd054 631e
    .hword 0x4699    @ 080cd056 9946
    .hword 0x46b0    @ 080cd058 b046
    movs r0,#0x80    @ 080cd05a 8020
    lsls r0,r0,#0x2    @ 080cd05c 8000
    adds r4,r4,r0    @ 080cd05e 2418
LAB_080cd060:
    lsls r0,r6,#0x1    @ 080cd060 7000
    ldr r7, DAT_080cd0d4                     @ 080cd062 1c4f
    add r7,r9                                @ 080cd064 4f44
    adds r0,r0,r7    @ 080cd066 c019
    strh r5,[r0,#0x0]                        @ 080cd068 0580
    .hword 0x4641    @ 080cd06a 4146
    str r1,[sp,#0x0]                         @ 080cd06c 0091
    .hword 0x4650    @ 080cd06e 5046
    adds r0,#0xc    @ 080cd070 0c30
    adds r1,r5,#0x0    @ 080cd072 291c
    adds r2,r4,#0x0    @ 080cd074 221c
    movs r3,#0xc    @ 080cd076 0c23
    bl render_jp_string_to_tile_line         @ 080cd078 faf722fb
    adds r5,r0,#0x0    @ 080cd07c 051c
    movs r3,#0x80    @ 080cd07e 8023
    lsls r3,r3,#0x2    @ 080cd080 9b00
    adds r4,r4,r3    @ 080cd082 e418
    adds r6,#0x1    @ 080cd084 0136
    cmp r6,#0x1                              @ 080cd086 012e
    ble LAB_080cd060                         @ 080cd088 eadd
    subs r5,#0x2    @ 080cd08a 023d
    ldr r0, DAT_080cd0d8                     @ 080cd08c 1248
    movs r1,#0x0    @ 080cd08e 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cd090 26f0a0fb
    adds r5,#0x10    @ 080cd094 1035
    adds r0,r5,#0x0    @ 080cd096 281c
    cmp r5,#0x0                              @ 080cd098 002d
    bge LAB_080cd09e                         @ 080cd09a 00da
    adds r0,r5,#0x7    @ 080cd09c e81d
LAB_080cd09e:
    asrs r6,r0,#0x3    @ 080cd09e c610
    movs r0,#0x7    @ 080cd0a0 0720
    ands r0,r5    @ 080cd0a2 2840
    cmp r0,#0x0                              @ 080cd0a4 0028
    beq LAB_080cd0aa                         @ 080cd0a6 00d0
    adds r6,#0x1    @ 080cd0a8 0136
LAB_080cd0aa:
    subs r0,r7,#0x1    @ 080cd0aa 781e
    strb r6,[r0,#0x0]                        @ 080cd0ac 0670
    add sp,#0x4                              @ 080cd0ae 01b0
    pop {r3,r4,r5}                           @ 080cd0b0 38bc
    .hword 0x4698    @ 080cd0b2 9846
    .hword 0x46a1    @ 080cd0b4 a146
    .hword 0x46aa    @ 080cd0b6 aa46
    pop {r4,r5,r6,r7}                        @ 080cd0b8 f0bc
    pop {r0}                                 @ 080cd0ba 01bc
    bx r0                                    @ 080cd0bc 0047
    .zero  0x2
DAT_080cd0c0:
    .word  0x02006ed0                     @ 080cd0c0 d06e0002
DAT_080cd0c4:
    .word  0x02000000                     @ 080cd0c4 00000002
DAT_080cd0c8:
    .word  0x00006c2c                     @ 080cd0c8 2c6c0000
PTR_font_jp_base_table_080cd0cc:
    .word  font_jp_base_table             @ 080cd0cc 54f8e509
DAT_080cd0d0:
    .word  0x0201f441                     @ 080cd0d0 41f40102
DAT_080cd0d4:
    .word  0x00000a04                     @ 080cd0d4 040a0000
DAT_080cd0d8:
    .word  0x06014000                     @ 080cd0d8 00400106

@ Card-list OAM row render branch for cost_bar variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 8. Nearly byte-identical to render_card_list_oam_row_by_pack_slot (0x080d05e4); differs only in literal pool constants (different DAT offsets). Reads gFontState[0x0a03] row count; OAM Y=(10-row/2)*8. Reads gFontState[0x0a1b] bits[1:0] slot_state [0..1]; if >1 skips. For state 0..1: reads gFontState[0x0a0e] halfword*2 as x_index (lsls #1); subtracts 0x17, adds gFontState[0x0a04] halfword for Y adjust. Calls write_oam_entry_from_packed_args (slot=0x60, attr0=0x34). No APCS inputs. Constants: ROW_OFFSET=0x0a03; SLOT_STATE_OFFSET=0x0a1b [0..1]; X_INDEX_OFFSET=0x0a0e; Y_ADJUST_OFFSET=0x0a04; ATTR0=0x34; OAM_SLOT=0x60.
render_card_list_oam_row_by_cost_bar:
    push {r4,r5,lr}                          @ 080cd0dc 30b5
    ldr r3, DAT_080cd128                     @ 080cd0de 124b
    ldr r1, DAT_080cd12c                     @ 080cd0e0 1249
    adds r0,r3,r1    @ 080cd0e2 5818
    ldrb r0,[r0,#0x0]                        @ 080cd0e4 0078
    lsrs r1,r0,#0x1    @ 080cd0e6 4108
    movs r0,#0xa    @ 080cd0e8 0a20
    subs r0,r0,r1    @ 080cd0ea 401a
    lsls r4,r0,#0x3    @ 080cd0ec c400
    ldr r5, DAT_080cd130                     @ 080cd0ee 104d
    adds r0,r3,r5    @ 080cd0f0 5819
    ldrb r0,[r0,#0x0]                        @ 080cd0f2 0078
    lsrs r0,r0,#0x1    @ 080cd0f4 4008
    movs r1,#0x3    @ 080cd0f6 0321
    ands r0,r1    @ 080cd0f8 0840
    cmp r0,#0x1                              @ 080cd0fa 0128
    bhi LAB_080cd120                         @ 080cd0fc 10d8
    movs r2,#0x34    @ 080cd0fe 3422
    ldr r1, DAT_080cd134                     @ 080cd100 0c49
    adds r0,r3,r1    @ 080cd102 5818
    ldrh r0,[r0,#0x0]                        @ 080cd104 0088
    lsls r0,r0,#0x1    @ 080cd106 4000
    subs r5,#0x17    @ 080cd108 173d
    adds r1,r3,r5    @ 080cd10a 5919
    adds r0,r0,r1    @ 080cd10c 4018
    ldrh r0,[r0,#0x0]                        @ 080cd10e 0088
    adds r0,r0,r4    @ 080cd110 0019
    adds r0,#0x1    @ 080cd112 0130
    lsls r0,r0,#0x10    @ 080cd114 0004
    orrs r0,r2    @ 080cd116 1043
    movs r1,#0x0    @ 080cd118 0021
    movs r2,#0x60    @ 080cd11a 6022
    bl write_oam_entry_from_packed_args      @ 080cd11c 29f026f8
LAB_080cd120:
    pop {r4,r5}                              @ 080cd120 30bc
    pop {r0}                                 @ 080cd122 01bc
    bx r0                                    @ 080cd124 0047
    .zero  0x2
DAT_080cd128:
    .word  0x0201f440                     @ 080cd128 40f40102
DAT_080cd12c:
    .word  0x00000a03                     @ 080cd12c 030a0000
DAT_080cd130:
    .word  0x00000a1b                     @ 080cd130 1b0a0000
DAT_080cd134:
    .word  0x00000a14                     @ 080cd134 140a0000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Computes OAM Y from gFontState+0x0a03 card_row_count byte: Y=(10-count/2)*8. Calls write_card_list_oam_row_strip(r0=0x30, r1=Y, r2=0x1fc, r3=count). Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch: (0) checks gPrng+0x148 bits[7:6] (mask 0xc0): if nonzero, decrements gFontState+0x0a14 halfword by 1, calls sync_state_and_init_sprite(0); (1) checks gPrng+0x148 bit0: if nonzero, reads LP from gP1LifePoints+0x3d40, writes gFontState+0x0a14 halfword (1-LP_val), calls sync_state_and_init_sprite(0x24); bit1 nonzero: calls sync_state_and_init_sprite(2); (2) state>=2: nibble loop increment on gFontState+0x0a1b/0x0a1c byte pair; returns 1 if nibble>0x1f else 0. Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; STATE_OFFSET=0x0a18; LP_OFFSET=0x0a14; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; LP_ADDR=gP1LifePoints+0x3d40; BITS_LP=0xc0.
render_card_list_oam_row_by_lp_counter:
    push {r4,r5,r6,r7,lr}                    @ 080cd138 f0b5
    .hword 0x4647    @ 080cd13a 4746
    push {r7}                                @ 080cd13c 80b4
    ldr r4, DAT_080cd16c                     @ 080cd13e 0b4c
    ldr r1, DAT_080cd170                     @ 080cd140 0b49
    adds r0,r4,r1    @ 080cd142 6018
    ldrb r3,[r0,#0x0]                        @ 080cd144 0378
    lsrs r0,r3,#0x1    @ 080cd146 5808
    movs r1,#0xa    @ 080cd148 0a21
    subs r1,r1,r0    @ 080cd14a 091a
    lsls r1,r1,#0x3    @ 080cd14c c900
    movs r2,#0xfe    @ 080cd14e fe22
    lsls r2,r2,#0x1    @ 080cd150 5200
    movs r0,#0x30    @ 080cd152 3020
    bl write_card_list_oam_row_strip         @ 080cd154 faf7ecf9
    ldr r2, DAT_080cd174                     @ 080cd158 064a
    adds r5,r4,r2    @ 080cd15a a518
    ldr r3,[r5,#0x0]                         @ 080cd15c 2b68
    lsls r0,r3,#0xf    @ 080cd15e d803
    lsrs r7,r0,#0x18    @ 080cd160 070e
    cmp r7,#0x0                              @ 080cd162 002f
    beq LAB_080cd178                         @ 080cd164 08d0
    cmp r7,#0x1                              @ 080cd166 012f
    beq LAB_080cd1f4                         @ 080cd168 44d0
    b LAB_080cd244                           @ 080cd16a 6be0
DAT_080cd16c:
    .word  0x0201f440                     @ 080cd16c 40f40102
DAT_080cd170:
    .word  0x00000a03                     @ 080cd170 030a0000
DAT_080cd174:
    .word  0x00000a18                     @ 080cd174 180a0000
LAB_080cd178:
    ldr r0, PTR_gPrng_080cd1a0               @ 080cd178 0948
    movs r6,#0xa4    @ 080cd17a a426
    lsls r6,r6,#0x1    @ 080cd17c 7600
    adds r0,r0,r6    @ 080cd17e 8019
    ldrh r1,[r0,#0x0]                        @ 080cd180 0188
    movs r0,#0xc0    @ 080cd182 c020
    ands r0,r1    @ 080cd184 0840
    cmp r0,#0x0                              @ 080cd186 0028
    beq LAB_080cd1a8                         @ 080cd188 0ed0
    ldr r0, DAT_080cd1a4                     @ 080cd18a 0648
    adds r1,r4,r0    @ 080cd18c 2118
    movs r0,#0x1    @ 080cd18e 0120
    ldrh r2,[r1,#0x0]                        @ 080cd190 0a88
    subs r0,r0,r2    @ 080cd192 801a
    strh r0,[r1,#0x0]                        @ 080cd194 0880
    movs r0,#0x0    @ 080cd196 0020
    bl sync_state_and_init_sprite            @ 080cd198 2cf08cfc
    b LAB_080cd244                           @ 080cd19c 52e0
    .zero  0x2
PTR_gPrng_080cd1a0:
    .word  gPrng                          @ 080cd1a0 40000003
DAT_080cd1a4:
    .word  0x00000a14                     @ 080cd1a4 140a0000
LAB_080cd1a8:
    movs r2,#0x1    @ 080cd1a8 0122
    adds r0,r2,#0x0    @ 080cd1aa 101c
    ands r0,r1    @ 080cd1ac 0840
    cmp r0,#0x0                              @ 080cd1ae 0028
    beq LAB_080cd1e4                         @ 080cd1b0 18d0
    ldr r0, PTR_gP1LifePoints_080cd1d8       @ 080cd1b2 0948
    movs r6,#0xea    @ 080cd1b4 ea26
    lsls r6,r6,#0x5    @ 080cd1b6 7601
    adds r0,r0,r6    @ 080cd1b8 8019
    ldr r6, DAT_080cd1dc                     @ 080cd1ba 084e
    adds r1,r4,r6    @ 080cd1bc a119
    ldrh r1,[r1,#0x0]                        @ 080cd1be 0988
    subs r1,r2,r1    @ 080cd1c0 511a
    str r1,[r0,#0x0]                         @ 080cd1c2 0160
    ldr r0, DAT_080cd1e0                     @ 080cd1c4 0648
    ands r0,r3    @ 080cd1c6 1840
    movs r1,#0x80    @ 080cd1c8 8021
    lsls r1,r1,#0x2    @ 080cd1ca 8900
    orrs r0,r1    @ 080cd1cc 0843
    str r0,[r5,#0x0]                         @ 080cd1ce 2860
    movs r0,#0x24    @ 080cd1d0 2420
    bl sync_state_and_init_sprite            @ 080cd1d2 2cf06ffc
    b LAB_080cd244                           @ 080cd1d6 35e0
PTR_gP1LifePoints_080cd1d8:
    .word  gP1LifePoints                  @ 080cd1d8 e0c40102
DAT_080cd1dc:
    .word  0x00000a14                     @ 080cd1dc 140a0000
DAT_080cd1e0:
    .word  0xfffe01ff                     @ 080cd1e0 ff01feff
LAB_080cd1e4:
    movs r0,#0x2    @ 080cd1e4 0220
    ands r0,r1    @ 080cd1e6 0840
    cmp r0,#0x0                              @ 080cd1e8 0028
    beq LAB_080cd244                         @ 080cd1ea 2bd0
    movs r0,#0x2    @ 080cd1ec 0220
    bl sync_state_and_init_sprite            @ 080cd1ee 2cf061fc
    b LAB_080cd244                           @ 080cd1f2 27e0
LAB_080cd1f4:
    ldr r0, DAT_080cd23c                     @ 080cd1f4 1148
    adds r0,r0,r4    @ 080cd1f6 0019
    .hword 0x4680    @ 080cd1f8 8046
    ldrb r6,[r0,#0x0]                        @ 080cd1fa 0678
    lsrs r0,r6,#0x1    @ 080cd1fc 7008
    ldr r1, DAT_080cd240                     @ 080cd1fe 1049
    adds r4,r4,r1    @ 080cd200 6418
    adds r3,r7,#0x0    @ 080cd202 3b1c
    ldrb r2,[r4,#0x0]                        @ 080cd204 2278
    ands r3,r2    @ 080cd206 1340
    lsls r3,r3,#0x7    @ 080cd208 db01
    orrs r3,r0    @ 080cd20a 0343
    adds r2,r3,#0x1    @ 080cd20c 5a1c
    movs r1,#0x7f    @ 080cd20e 7f21
    ands r1,r2    @ 080cd210 1140
    lsls r1,r1,#0x1    @ 080cd212 4900
    movs r5,#0x1    @ 080cd214 0125
    adds r0,r7,#0x0    @ 080cd216 381c
    ands r0,r6    @ 080cd218 3040
    orrs r0,r1    @ 080cd21a 0843
    .hword 0x4646    @ 080cd21c 4646
    strb r0,[r6,#0x0]                        @ 080cd21e 3070
    lsrs r2,r2,#0x7    @ 080cd220 d209
    ands r2,r7    @ 080cd222 3a40
    ands r2,r5    @ 080cd224 2a40
    movs r0,#0x2    @ 080cd226 0220
    rsbs r0,r0,#0    @ 080cd228 4042
    ldrb r1,[r4,#0x0]                        @ 080cd22a 2178
    ands r0,r1    @ 080cd22c 0840
    orrs r0,r2    @ 080cd22e 1043
    strb r0,[r4,#0x0]                        @ 080cd230 2070
    cmp r3,#0x1f                             @ 080cd232 1f2b
    bls LAB_080cd244                         @ 080cd234 06d9
    movs r0,#0x1    @ 080cd236 0120
    b LAB_080cd246                           @ 080cd238 05e0
    .zero  0x2
DAT_080cd23c:
    .word  0x00000a1b                     @ 080cd23c 1b0a0000
DAT_080cd240:
    .word  0x00000a1c                     @ 080cd240 1c0a0000
LAB_080cd244:
    movs r0,#0x0    @ 080cd244 0020
LAB_080cd246:
    pop {r3}                                 @ 080cd246 08bc
    .hword 0x4698    @ 080cd248 9846
    pop {r4,r5,r6,r7}                        @ 080cd24a f0bc
    pop {r1}                                 @ 080cd24c 02bc
    bx r1                                    @ 080cd24e 0847

@ 由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. 函数入口将 r0 低 16 位 (r5=u16_lo) 和高 16 位 (r4=u16_hi) 分别提取作为 palette index 和 tile 偏移参数. 首先 zero_fill_by_halfword 清零 BG tile VRAM 区域 (0x06014000, 0x80<<0x7=0x4000 halfword = 0x8000 字节); 然后依次调用 copy_bytes_by_halfword (0x05000260 palette) 和三次 tile_2d_row_copy 将 card tile 数据从 ROM 复制到 VRAM. 之后读取状态结构体的 palette/tile 字段, 计算 OBJ palette index 并循环写入 BG tile 中调色板编号字段. Constants: VRAM_BG_BASE=0x06014000, PALETTE_SRC=0x05000260, ROM_TILE_SRC_A=0x0988aad8, ROM_TILE_SRC_B=0x0988a7d8, ROM_TILE_SRC_C=0x0988ab58, STATE_BASE=0x0201f440, PALETTE_IDX_MASK=0xfffff00f, LOOP_END=5.
init_field_bg_tile_vram_layout:
    push {r4,r5,r6,r7,lr}                    @ 080cd250 f0b5
    lsls r1,r0,#0x10    @ 080cd252 0104
    lsrs r5,r1,#0x10    @ 080cd254 0d0c
    lsrs r4,r0,#0x10    @ 080cd256 040c
    ldr r0, DAT_080cd2fc                     @ 080cd258 2848
    movs r1,#0x80    @ 080cd25a 8021
    lsls r1,r1,#0x7    @ 080cd25c c901
    bl zero_fill_by_halfword                 @ 080cd25e 27f009fe
    ldr r0, DAT_080cd300                     @ 080cd262 2748
    ldr r1, DAT_080cd304                     @ 080cd264 2749
    movs r2,#0x20    @ 080cd266 2022
    bl copy_bytes_by_halfword                @ 080cd268 27f01cfe
    ldr r0, DAT_080cd308                     @ 080cd26c 2648
    ldr r1, DAT_080cd30c                     @ 080cd26e 2749
    movs r2,#0x2    @ 080cd270 0222
    movs r3,#0xc    @ 080cd272 0c23
    bl tile_2d_row_copy                      @ 080cd274 2af02ef9
    ldr r0, DAT_080cd310                     @ 080cd278 2548
    ldr r1, DAT_080cd314                     @ 080cd27a 2649
    movs r2,#0x4    @ 080cd27c 0422
    movs r3,#0x4    @ 080cd27e 0423
    bl tile_2d_row_copy                      @ 080cd280 2af028f9
    ldr r0, DAT_080cd318                     @ 080cd284 2448
    ldr r1, DAT_080cd31c                     @ 080cd286 2549
    movs r2,#0x1    @ 080cd288 0122
    movs r3,#0x1    @ 080cd28a 0123
    bl tile_2d_row_copy                      @ 080cd28c 2af022f9
    ldr r3, DAT_080cd320                     @ 080cd290 234b
    ldr r1, DAT_080cd324                     @ 080cd292 2449
    adds r0,r3,r1    @ 080cd294 5818
    ldrb r0,[r0,#0x0]                        @ 080cd296 0078
    lsrs r2,r0,#0x1    @ 080cd298 4208
    ldr r0, DAT_080cd328                     @ 080cd29a 2348
    adds r1,r3,r0    @ 080cd29c 1918
    movs r0,#0x1    @ 080cd29e 0120
    ldrb r1,[r1,#0x0]                        @ 080cd2a0 0978
    ands r0,r1    @ 080cd2a2 0840
    lsls r0,r0,#0x7    @ 080cd2a4 c001
    orrs r0,r2    @ 080cd2a6 1043
    cmp r0,#0x0                              @ 080cd2a8 0028
    bne LAB_080cd2f6                         @ 080cd2aa 24d1
    ldr r2, DAT_080cd32c                     @ 080cd2ac 1f4a
    adds r1,r3,r2    @ 080cd2ae 9918
    strb r4,[r1,#0x0]                        @ 080cd2b0 0c70
    adds r2,#0x4    @ 080cd2b2 0432
    adds r0,r3,r2    @ 080cd2b4 9818
    strh r5,[r0,#0x0]                        @ 080cd2b6 0580
    movs r0,#0x0    @ 080cd2b8 0020
    .hword 0x469c    @ 080cd2ba 9c46
    ldrb r5,[r1,#0x0]                        @ 080cd2bc 0d78
    ldr r4, DAT_080cd330                     @ 080cd2be 1c4c
    add r4,r12                               @ 080cd2c0 6444
    movs r6,#0x1    @ 080cd2c2 0126
    ldr r7, DAT_080cd334                     @ 080cd2c4 1b4f
LAB_080cd2c6:
    adds r3,r0,#0x1    @ 080cd2c6 431c
    adds r0,r5,#0x0    @ 080cd2c8 281c
    asrs r0,r3    @ 080cd2ca 1841
    ands r0,r6    @ 080cd2cc 3040
    cmp r0,#0x0                              @ 080cd2ce 0028
    beq LAB_080cd2e8                         @ 080cd2d0 0ad0
    ldrh r2,[r4,#0x0]                        @ 080cd2d2 2288
    lsls r1,r2,#0x14    @ 080cd2d4 1105
    lsrs r1,r1,#0x18    @ 080cd2d6 090e
    adds r1,#0x1    @ 080cd2d8 0131
    movs r0,#0xff    @ 080cd2da ff20
    ands r1,r0    @ 080cd2dc 0140
    lsls r1,r1,#0x4    @ 080cd2de 0901
    adds r0,r7,#0x0    @ 080cd2e0 381c
    ands r0,r2    @ 080cd2e2 1040
    orrs r0,r1    @ 080cd2e4 0843
    strh r0,[r4,#0x0]                        @ 080cd2e6 2080
LAB_080cd2e8:
    adds r0,r3,#0x0    @ 080cd2e8 181c
    cmp r0,#0x5                              @ 080cd2ea 0528
    ble LAB_080cd2c6                         @ 080cd2ec ebdd
    ldr r1, DAT_080cd338                     @ 080cd2ee 1249
    add r1,r12                               @ 080cd2f0 6144
    movs r0,#0x9    @ 080cd2f2 0920
    strb r0,[r1,#0x0]                        @ 080cd2f4 0870
LAB_080cd2f6:
    pop {r4,r5,r6,r7}                        @ 080cd2f6 f0bc
    pop {r0}                                 @ 080cd2f8 01bc
    bx r0                                    @ 080cd2fa 0047
DAT_080cd2fc:
    .word  0x06014000                     @ 080cd2fc 00400106
DAT_080cd300:
    .word  0x05000260                     @ 080cd300 60020005
DAT_080cd304:
    .word  0x0988aad8                     @ 080cd304 d8aa8809
DAT_080cd308:
    .word  0x060153c0                     @ 080cd308 c0530106
DAT_080cd30c:
    .word  0x0988a7d8                     @ 080cd30c d8a78809
DAT_080cd310:
    .word  0x06016b40                     @ 080cd310 406b0106
DAT_080cd314:
    .word  0x0988ab58                     @ 080cd314 58ab8809
DAT_080cd318:
    .word  0x06010c00                     @ 080cd318 000c0106
DAT_080cd31c:
    .word  0x0988ad58                     @ 080cd31c 58ad8809
DAT_080cd320:
    .word  0x0201f440                     @ 080cd320 40f40102
DAT_080cd324:
    .word  0x00000a17                     @ 080cd324 170a0000
DAT_080cd328:
    .word  0x00000a18                     @ 080cd328 180a0000
DAT_080cd32c:
    .word  0x00000a02                     @ 080cd32c 020a0000
DAT_080cd330:
    .word  0x00000a0e                     @ 080cd330 0e0a0000
DAT_080cd334:
    .word  0xfffff00f                     @ 080cd334 0ff0ffff
DAT_080cd338:
    .word  0x00000a01                     @ 080cd338 010a0000

@ Render the card name string into BG tile VRAM for the card info name row. Looks up card name JP string via resolve_game_str_ptr(card_id), calls render_jp_string_to_tile_line then write_line_buf_to_bg_tile_vram. r0: card_id [0..0x19b7]; r1: bg_tile_dest ptr; r2: x_col [0..29]; r3: y_row [0..23]. Returns void. Side effects: BG tile VRAM name row written.
render_card_name_label_to_bg:
    push {r4,r5,r6,r7,lr}                    @ 080cd33c f0b5
    .hword 0x4647    @ 080cd33e 4746
    push {r7}                                @ 080cd340 80b4
    sub sp,#0x4                              @ 080cd342 81b0
    movs r6,#0x0    @ 080cd344 0026
    movs r0,#0x17    @ 080cd346 1720
    movs r1,#0x10    @ 080cd348 1021
    movs r2,#0x1    @ 080cd34a 0122
    movs r3,#0x2    @ 080cd34c 0223
    bl setup_line_buf_with_font_and_align    @ 080cd34e 23f0b7fc
    ldr r2, DAT_080cd42c                     @ 080cd352 364a
    ldr r0, DAT_080cd430                     @ 080cd354 3648
    ldr r1, DAT_080cd434                     @ 080cd356 3749
    adds r0,r0,r1    @ 080cd358 4018
    movs r1,#0x7    @ 080cd35a 0721
    ldrb r0,[r0,#0x0]                        @ 080cd35c 0078
    ands r1,r0    @ 080cd35e 0140
    rsbs r1,r1,#0    @ 080cd360 4942
    lsrs r1,r1,#0x1f    @ 080cd362 c90f
    movs r0,#0x2    @ 080cd364 0220
    rsbs r0,r0,#0    @ 080cd366 4042
    ldrb r3,[r2,#0x8]                        @ 080cd368 137a
    ands r0,r3    @ 080cd36a 1840
    orrs r0,r1    @ 080cd36c 0843
    movs r1,#0x2    @ 080cd36e 0221
    orrs r0,r1    @ 080cd370 0843
    strb r0,[r2,#0x8]                        @ 080cd372 1072
    ldr r3, PTR_font_jp_base_table_080cd438  @ 080cd374 304b
    lsls r1,r0,#0x1e    @ 080cd376 8107
    lsrs r1,r1,#0x1f    @ 080cd378 c90f
    lsls r1,r1,#0x2    @ 080cd37a 8900
    lsls r0,r0,#0x1f    @ 080cd37c c007
    lsrs r0,r0,#0x1f    @ 080cd37e c00f
    lsls r0,r0,#0x3    @ 080cd380 c000
    adds r1,r1,r0    @ 080cd382 0918
    adds r1,r1,r3    @ 080cd384 c918
    ldr r0,[r1,#0x0]                         @ 080cd386 0868
    str r0,[r2,#0x4]                         @ 080cd388 5060
    movs r0,#0x40    @ 080cd38a 4020
    ldrb r1,[r2,#0x15]                       @ 080cd38c 517d
    orrs r0,r1    @ 080cd38e 0843
    strb r0,[r2,#0x15]                       @ 080cd390 5075
    ldr r4, DAT_080cd43c                     @ 080cd392 2a4c
    str r6,[sp,#0x0]                         @ 080cd394 0096
    movs r0,#0x2    @ 080cd396 0220
    movs r1,#0x2    @ 080cd398 0221
    adds r2,r4,#0x0    @ 080cd39a 221c
    movs r3,#0xc    @ 080cd39c 0c23
    bl render_jp_string_to_tile_line         @ 080cd39e faf78ff9
    adds r5,r0,#0x0    @ 080cd3a2 051c
    ldr r0, DAT_080cd440                     @ 080cd3a4 2648
    movs r1,#0x0    @ 080cd3a6 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cd3a8 26f014fa
    adds r1,r5,#0x3    @ 080cd3ac e91c
    ldr r2, DAT_080cd444                     @ 080cd3ae 254a
    adds r0,r4,r2    @ 080cd3b0 a018
    strh r1,[r0,#0x0]                        @ 080cd3b2 0180
    adds r5,#0x14    @ 080cd3b4 1435
    ldr r3, DAT_080cd448                     @ 080cd3b6 244b
    adds r0,r4,r3    @ 080cd3b8 e018
    ldrb r3,[r0,#0x0]                        @ 080cd3ba 0378
    ldr r0, DAT_080cd44c                     @ 080cd3bc 2348
    adds r4,r4,r0    @ 080cd3be 2418
    ldrb r2,[r4,#0x0]                        @ 080cd3c0 2278
    lsls r1,r2,#0x1c    @ 080cd3c2 1107
    lsrs r1,r1,#0x1c    @ 080cd3c4 090f
    adds r0,r3,#0x0    @ 080cd3c6 181c
    asrs r0,r1    @ 080cd3c8 0841
    movs r1,#0x1    @ 080cd3ca 0121
    ands r0,r1    @ 080cd3cc 0840
    cmp r0,#0x0                              @ 080cd3ce 0028
    bne LAB_080cd402                         @ 080cd3d0 17d1
    .hword 0x46a0    @ 080cd3d2 a046
    subs r1,#0x11    @ 080cd3d4 1139
    .hword 0x468c    @ 080cd3d6 8c46
    adds r4,r3,#0x0    @ 080cd3d8 1c1c
    adds r3,r2,#0x0    @ 080cd3da 131c
    movs r7,#0xf    @ 080cd3dc 0f27
    movs r6,#0x1    @ 080cd3de 0126
LAB_080cd3e0:
    lsls r0,r3,#0x1c    @ 080cd3e0 1807
    lsrs r0,r0,#0x1c    @ 080cd3e2 000f
    adds r0,#0x1    @ 080cd3e4 0130
    ands r0,r7    @ 080cd3e6 3840
    .hword 0x4662    @ 080cd3e8 6246
    ands r2,r3    @ 080cd3ea 1a40
    orrs r2,r0    @ 080cd3ec 0243
    adds r3,r2,#0x0    @ 080cd3ee 131c
    lsls r1,r2,#0x1c    @ 080cd3f0 1107
    lsrs r1,r1,#0x1c    @ 080cd3f2 090f
    adds r0,r4,#0x0    @ 080cd3f4 201c
    asrs r0,r1    @ 080cd3f6 0841
    ands r0,r6    @ 080cd3f8 3040
    cmp r0,#0x0                              @ 080cd3fa 0028
    beq LAB_080cd3e0                         @ 080cd3fc f0d0
    .hword 0x4643    @ 080cd3fe 4346
    strb r2,[r3,#0x0]                        @ 080cd400 1a70
LAB_080cd402:
    adds r5,#0x10    @ 080cd402 1035
    adds r0,r5,#0x0    @ 080cd404 281c
    cmp r5,#0x0                              @ 080cd406 002d
    bge LAB_080cd40c                         @ 080cd408 00da
    adds r0,r5,#0x7    @ 080cd40a e81d
LAB_080cd40c:
    asrs r6,r0,#0x3    @ 080cd40c c610
    movs r0,#0x7    @ 080cd40e 0720
    ands r0,r5    @ 080cd410 2840
    cmp r0,#0x0                              @ 080cd412 0028
    beq LAB_080cd418                         @ 080cd414 00d0
    adds r6,#0x1    @ 080cd416 0136
LAB_080cd418:
    ldr r0, DAT_080cd450                     @ 080cd418 0d48
    ldr r1, DAT_080cd444                     @ 080cd41a 0a49
    adds r0,r0,r1    @ 080cd41c 4018
    strb r6,[r0,#0x0]                        @ 080cd41e 0670
    add sp,#0x4                              @ 080cd420 01b0
    pop {r3}                                 @ 080cd422 08bc
    .hword 0x4698    @ 080cd424 9846
    pop {r4,r5,r6,r7}                        @ 080cd426 f0bc
    pop {r0}                                 @ 080cd428 01bc
    bx r0                                    @ 080cd42a 0047
DAT_080cd42c:
    .word  0x02006ed0                     @ 080cd42c d06e0002
DAT_080cd430:
    .word  0x02000000                     @ 080cd430 00000002
DAT_080cd434:
    .word  0x00006c2c                     @ 080cd434 2c6c0000
PTR_font_jp_base_table_080cd438:
    .word  font_jp_base_table             @ 080cd438 54f8e509
DAT_080cd43c:
    .word  0x0201f441                     @ 080cd43c 41f40102
DAT_080cd440:
    .word  0x06014000                     @ 080cd440 00400106
DAT_080cd444:
    .word  0x00000a03                     @ 080cd444 030a0000
DAT_080cd448:
    .word  0x00000a01                     @ 080cd448 010a0000
DAT_080cd44c:
    .word  0x00000a0d                     @ 080cd44c 0d0a0000
DAT_080cd450:
    .word  0x0201f440                     @ 080cd450 40f40102

@ Card-list OAM row render branch for single_slot variant. Sibling of render_card_list_oam_row_by_dual_slot (0x080cdba8); called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 9. Same callee set (__divsi3 x2, write_oam_entry_from_packed_args x2, write_oam_entry_with_slot_check x3+). Key differences from dual_slot: divisor=0xb8=184 (vs 0xc8=200); OAM Y base = y_coord+0x2a=42 (vs +0x1c=28); extra condition fields at DAT+0x0a14/0x0a18/0x0a1c determine 4th OAM entry (write_oam_entry_from_packed_args attr2=0x80). gFontState base loaded internally into r10; no APCS inputs. Constants: CARD_REG_OFFSET=0x0201fe4e; DIVISOR=0xb8; OAM_Y_BASE=+0x2a; SLOT_STATE_OFFSET=0x0a1b; ATTR2_EXTRA=0x80; OAM_SLOT=0x60.
render_card_list_oam_row_by_single_slot:
    push {r4,r5,r6,r7,lr}                    @ 080cd454 f0b5
    .hword 0x4657    @ 080cd456 5746
    .hword 0x464e    @ 080cd458 4e46
    .hword 0x4645    @ 080cd45a 4546
    push {r5,r6,r7}                          @ 080cd45c e0b4
    sub sp,#0x8                              @ 080cd45e 82b0
    ldr r0, DAT_080cd5b8                     @ 080cd460 5548
    .hword 0x4682    @ 080cd462 8246
    ldr r0, DAT_080cd5bc                     @ 080cd464 5548
    add r0,r10                               @ 080cd466 5044
    ldrh r0,[r0,#0x0]                        @ 080cd468 0088
    lsls r4,r0,#0x14    @ 080cd46a 0405
    lsrs r1,r4,#0x18    @ 080cd46c 210e
    lsls r1,r1,#0x1    @ 080cd46e 4900
    movs r0,#0xb8    @ 080cd470 b820
    bl __divsi3                              @ 080cd472 41f0c7f8
    adds r7,r0,#0x0    @ 080cd476 071c
    adds r7,#0x2a    @ 080cd478 2a37
    ldr r0, DAT_080cd5c0                     @ 080cd47a 5148
    add r0,r10                               @ 080cd47c 5044
    ldrb r0,[r0,#0x0]                        @ 080cd47e 0078
    lsrs r1,r0,#0x1    @ 080cd480 4108
    movs r0,#0xa    @ 080cd482 0a20
    subs r0,r0,r1    @ 080cd484 401a
    lsls r0,r0,#0x3    @ 080cd486 c000
    ldr r1, DAT_080cd5c4                     @ 080cd488 4e49
    add r1,r10                               @ 080cd48a 5144
    ldrh r1,[r1,#0x0]                        @ 080cd48c 0988
    adds r1,r1,r0    @ 080cd48e 0918
    str r1,[sp,#0x4]                         @ 080cd490 0191
    adds r1,#0x1    @ 080cd492 0131
    str r1,[sp,#0x0]                         @ 080cd494 0091
    lsrs r4,r4,#0x18    @ 080cd496 240e
    movs r0,#0xb8    @ 080cd498 b820
    adds r1,r4,#0x0    @ 080cd49a 211c
    bl __divsi3                              @ 080cd49c 41f0b2f8
    .hword 0x4681    @ 080cd4a0 8146
    ldr r0, DAT_080cd5c8                     @ 080cd4a2 4948
    add r0,r10                               @ 080cd4a4 5044
    ldrb r0,[r0,#0x0]                        @ 080cd4a6 0078
    lsrs r0,r0,#0x1    @ 080cd4a8 4008
    movs r1,#0x3    @ 080cd4aa 0321
    ands r0,r1    @ 080cd4ac 0840
    cmp r0,#0x1                              @ 080cd4ae 0128
    bhi LAB_080cd570                         @ 080cd4b0 5ed8
    ldr r0, PTR_gPrng_080cd5cc               @ 080cd4b2 4648
    movs r1,#0x83    @ 080cd4b4 8321
    lsls r1,r1,#0x2    @ 080cd4b6 8900
    adds r0,r0,r1    @ 080cd4b8 4018
    ldrh r0,[r0,#0x0]                        @ 080cd4ba 0088
    lsrs r5,r0,#0x4    @ 080cd4bc 0509
    movs r0,#0x1    @ 080cd4be 0120
    ands r5,r0    @ 080cd4c0 0540
    ldr r2, DAT_080cd5d0                     @ 080cd4c2 434a
    add r2,r10                               @ 080cd4c4 5244
    .hword 0x4690    @ 080cd4c6 9046
    ldrh r3,[r2,#0x0]                        @ 080cd4c8 1388
    .hword 0x4648    @ 080cd4ca 4846
    muls r0,r3    @ 080cd4cc 5843
    adds r0,r7,r0    @ 080cd4ce 3818
    adds r6,r5,#0x5    @ 080cd4d0 6e1d
    subs r0,r0,r6    @ 080cd4d2 801b
    ldr r1,[sp,#0x0]                         @ 080cd4d4 0099
    subs r4,r1,r6    @ 080cd4d6 8c1b
    lsls r4,r4,#0x10    @ 080cd4d8 2404
    orrs r0,r4    @ 080cd4da 2043
    movs r1,#0x0    @ 080cd4dc 0021
    movs r2,#0x60    @ 080cd4de 6022
    bl write_oam_entry_from_packed_args      @ 080cd4e0 28f044fe
    .hword 0x4642    @ 080cd4e4 4246
    ldrh r2,[r2,#0x0]                        @ 080cd4e6 1288
    .hword 0x4648    @ 080cd4e8 4846
    muls r0,r2    @ 080cd4ea 5043
    adds r0,r7,r0    @ 080cd4ec 3818
    adds r5,#0xd    @ 080cd4ee 0d35
    adds r0,r0,r5    @ 080cd4f0 4019
    orrs r0,r4    @ 080cd4f2 2043
    movs r3,#0x80    @ 080cd4f4 8023
    lsls r3,r3,#0x5    @ 080cd4f6 5b01
    movs r1,#0x0    @ 080cd4f8 0021
    movs r2,#0x60    @ 080cd4fa 6022
    bl write_oam_entry_with_slot_check       @ 080cd4fc 29f07af9
    .hword 0x4643    @ 080cd500 4346
    ldrh r3,[r3,#0x0]                        @ 080cd502 1b88
    .hword 0x4648    @ 080cd504 4846
    muls r0,r3    @ 080cd506 5843
    adds r0,r7,r0    @ 080cd508 3818
    subs r0,r0,r6    @ 080cd50a 801b
    ldr r1,[sp,#0x0]                         @ 080cd50c 0099
    adds r4,r1,r5    @ 080cd50e 4c19
    lsls r4,r4,#0x10    @ 080cd510 2404
    orrs r0,r4    @ 080cd512 2043
    movs r3,#0x80    @ 080cd514 8023
    lsls r3,r3,#0x6    @ 080cd516 9b01
    movs r1,#0x0    @ 080cd518 0021
    movs r2,#0x60    @ 080cd51a 6022
    bl write_oam_entry_with_slot_check       @ 080cd51c 29f06af9
    .hword 0x4642    @ 080cd520 4246
    ldrh r2,[r2,#0x0]                        @ 080cd522 1288
    .hword 0x4648    @ 080cd524 4846
    muls r0,r2    @ 080cd526 5043
    adds r0,r7,r0    @ 080cd528 3818
    adds r0,r0,r5    @ 080cd52a 4019
    orrs r0,r4    @ 080cd52c 2043
    movs r3,#0xc0    @ 080cd52e c023
    lsls r3,r3,#0x6    @ 080cd530 9b01
    movs r1,#0x0    @ 080cd532 0021
    movs r2,#0x60    @ 080cd534 6022
    bl write_oam_entry_with_slot_check       @ 080cd536 29f05df9
    ldr r0, DAT_080cd5d4                     @ 080cd53a 2648
    add r0,r10                               @ 080cd53c 5044
    ldrh r0,[r0,#0x0]                        @ 080cd53e 0088
    cmp r0,#0x0                              @ 080cd540 0028
    beq LAB_080cd570                         @ 080cd542 15d0
    ldr r0, DAT_080cd5d8                     @ 080cd544 2448
    add r0,r10                               @ 080cd546 5044
    ldrh r0,[r0,#0x0]                        @ 080cd548 0088
    cmp r0,#0x1                              @ 080cd54a 0128
    bls LAB_080cd570                         @ 080cd54c 10d9
    ldr r0, DAT_080cd5dc                     @ 080cd54e 2348
    add r0,r10                               @ 080cd550 5044
    ldrh r0,[r0,#0x0]                        @ 080cd552 0088
    subs r0,#0x1    @ 080cd554 0138
    .hword 0x464b    @ 080cd556 4b46
    muls r3,r0    @ 080cd558 4343
    adds r0,r3,#0x0    @ 080cd55a 181c
    adds r0,r7,r0    @ 080cd55c 3818
    subs r0,#0x8    @ 080cd55e 0838
    ldr r1,[sp,#0x4]                         @ 080cd560 0199
    subs r1,#0x7    @ 080cd562 0739
    lsls r1,r1,#0x10    @ 080cd564 0904
    orrs r0,r1    @ 080cd566 0843
    ldr r2, DAT_080cd5e0                     @ 080cd568 1d4a
    movs r1,#0x80    @ 080cd56a 8021
    bl write_oam_entry_from_packed_args      @ 080cd56c 28f0fefd
LAB_080cd570:
    movs r2,#0x0    @ 080cd570 0022
    ldr r5, DAT_080cd5e4                     @ 080cd572 1c4d
LAB_080cd574:
    adds r4,r2,#0x1    @ 080cd574 541c
    ldrb r0,[r5,#0x0]                        @ 080cd576 2878
    asrs r0,r4    @ 080cd578 2041
    movs r1,#0x1    @ 080cd57a 0121
    ands r0,r1    @ 080cd57c 0840
    cmp r0,#0x0                              @ 080cd57e 0028
    beq LAB_080cd5a2                         @ 080cd580 0fd0
    ldr r1,[sp,#0x0]                         @ 080cd582 0099
    lsls r0,r1,#0x10    @ 080cd584 0804
    orrs r0,r7    @ 080cd586 3843
    lsls r2,r2,#0x6    @ 080cd588 9201
    ldr r3, DAT_080cd5e8                     @ 080cd58a 174b
    adds r2,r2,r3    @ 080cd58c d218
    movs r3,#0xc0    @ 080cd58e c023
    lsls r3,r3,#0x6    @ 080cd590 9b01
    adds r1,r3,#0x0    @ 080cd592 191c
    orrs r2,r1    @ 080cd594 0a43
    lsls r2,r2,#0x10    @ 080cd596 1204
    lsrs r2,r2,#0x10    @ 080cd598 120c
    movs r1,#0x40    @ 080cd59a 4021
    bl write_oam_entry_from_packed_args      @ 080cd59c 28f0e6fd
    add r7,r9                                @ 080cd5a0 4f44
LAB_080cd5a2:
    adds r2,r4,#0x0    @ 080cd5a2 221c
    cmp r2,#0x5                              @ 080cd5a4 052a
    ble LAB_080cd574                         @ 080cd5a6 e5dd
    add sp,#0x8                              @ 080cd5a8 02b0
    pop {r3,r4,r5}                           @ 080cd5aa 38bc
    .hword 0x4698    @ 080cd5ac 9846
    .hword 0x46a1    @ 080cd5ae a146
    .hword 0x46aa    @ 080cd5b0 aa46
    pop {r4,r5,r6,r7}                        @ 080cd5b2 f0bc
    pop {r0}                                 @ 080cd5b4 01bc
    bx r0                                    @ 080cd5b6 0047
DAT_080cd5b8:
    .word  0x0201f440                     @ 080cd5b8 40f40102
DAT_080cd5bc:
    .word  0x00000a0e                     @ 080cd5bc 0e0a0000
DAT_080cd5c0:
    .word  0x00000a03                     @ 080cd5c0 030a0000
DAT_080cd5c4:
    .word  0x00000a04                     @ 080cd5c4 040a0000
DAT_080cd5c8:
    .word  0x00000a1b                     @ 080cd5c8 1b0a0000
PTR_gPrng_080cd5cc:
    .word  gPrng                          @ 080cd5cc 40000003
DAT_080cd5d0:
    .word  0x00000a14                     @ 080cd5d0 140a0000
DAT_080cd5d4:
    .word  0x00000a08                     @ 080cd5d4 080a0000
DAT_080cd5d8:
    .word  0x00000a06                     @ 080cd5d8 060a0000
DAT_080cd5dc:
    .word  0x00000a0a                     @ 080cd5dc 0a0a0000
DAT_080cd5e0:
    .word  0x0000035a                     @ 080cd5e0 5a030000
DAT_080cd5e4:
    .word  0x0201fe42                     @ 080cd5e4 42fe0102
DAT_080cd5e8:
    .word  0x0000029e                     @ 080cd5e8 9e020000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. state=0: reads gPrng+0x148, tests bit5(0x20)/bit4(0x10)/bit0 in sequence; each path executes nibble-decrement mod-16 loop on gFontState+0x0a0e byte until corresponding bit in gFontState+0x0a02 is hit; on success writes gFontState+0x0a14 halfword -1 or +1, calls sync_state_and_init_sprite(0). state=1: reads gPrng+0x148 bit0 -> LP update (gP1LifePoints+0x3d40, strh 1-halfword). state>=2: nibble loop increment on 0x0a1b/0x0a1c (same logic as 080cd138). Key difference from 080cd138: state=0 uses nibble rotation (0x0a0e nibble mask 0xf, subs #1 & 0xf) rather than LP counter decrement. Constants: OAM_SLOT=0x30; Y_BASE=10; NIBBLE_OFFSET=0x0a0e; MASK_BIT5=0x20; MASK_BIT4=0x10; MASK_BIT0=0x01.
render_card_list_oam_row_by_nibble_rotate:
    push {r4,r5,r6,r7,lr}                    @ 080cd5ec f0b5
    .hword 0x4647    @ 080cd5ee 4746
    push {r7}                                @ 080cd5f0 80b4
    ldr r4, DAT_080cd624                     @ 080cd5f2 0c4c
    ldr r1, DAT_080cd628                     @ 080cd5f4 0c49
    adds r0,r4,r1    @ 080cd5f6 6018
    ldrb r3,[r0,#0x0]                        @ 080cd5f8 0378
    lsrs r0,r3,#0x1    @ 080cd5fa 5808
    movs r1,#0xa    @ 080cd5fc 0a21
    subs r1,r1,r0    @ 080cd5fe 091a
    lsls r1,r1,#0x3    @ 080cd600 c900
    movs r2,#0xfe    @ 080cd602 fe22
    lsls r2,r2,#0x1    @ 080cd604 5200
    movs r0,#0x30    @ 080cd606 3020
    bl write_card_list_oam_row_strip         @ 080cd608 f9f792ff
    ldr r2, DAT_080cd62c                     @ 080cd60c 074a
    adds r0,r4,r2    @ 080cd60e a018
    ldr r0,[r0,#0x0]                         @ 080cd610 0068
    lsls r0,r0,#0xf    @ 080cd612 c003
    lsrs r7,r0,#0x18    @ 080cd614 070e
    cmp r7,#0x0                              @ 080cd616 002f
    beq LAB_080cd630                         @ 080cd618 0ad0
    cmp r7,#0x1                              @ 080cd61a 012f
    bne LAB_080cd620                         @ 080cd61c 00d1
    b LAB_080cd814                           @ 080cd61e f9e0
LAB_080cd620:
    b LAB_080cd864                           @ 080cd620 20e1
    .zero  0x2
DAT_080cd624:
    .word  0x0201f440                     @ 080cd624 40f40102
DAT_080cd628:
    .word  0x00000a03                     @ 080cd628 030a0000
DAT_080cd62c:
    .word  0x00000a18                     @ 080cd62c 180a0000
LAB_080cd630:
    ldr r0, PTR_gPrng_080cd694               @ 080cd630 1848
    movs r3,#0xa4    @ 080cd632 a423
    lsls r3,r3,#0x1    @ 080cd634 5b00
    adds r0,r0,r3    @ 080cd636 c018
    ldrh r1,[r0,#0x0]                        @ 080cd638 0188
    movs r0,#0x20    @ 080cd63a 2020
    ands r0,r1    @ 080cd63c 0840
    cmp r0,#0x0                              @ 080cd63e 0028
    beq LAB_080cd6a4                         @ 080cd640 30d0
    ldr r1, DAT_080cd698                     @ 080cd642 1549
    adds r0,r4,r1    @ 080cd644 6018
    ldrb r6,[r0,#0x0]                        @ 080cd646 0678
    ldr r2, DAT_080cd69c                     @ 080cd648 144a
    adds r5,r4,r2    @ 080cd64a a518
    movs r7,#0xf    @ 080cd64c 0f27
    movs r3,#0x10    @ 080cd64e 1023
    rsbs r3,r3,#0    @ 080cd650 5b42
LAB_080cd652:
    ldrb r2,[r5,#0x0]                        @ 080cd652 2a78
    lsls r1,r2,#0x1c    @ 080cd654 1107
    lsrs r1,r1,#0x1c    @ 080cd656 090f
    subs r1,#0x1    @ 080cd658 0139
    ands r1,r7    @ 080cd65a 3940
    adds r0,r3,#0x0    @ 080cd65c 181c
    ands r0,r2    @ 080cd65e 1040
    orrs r0,r1    @ 080cd660 0843
    strb r0,[r5,#0x0]                        @ 080cd662 2870
    adds r0,r6,#0x0    @ 080cd664 301c
    asrs r0,r1    @ 080cd666 0841
    movs r1,#0x1    @ 080cd668 0121
    ands r0,r1    @ 080cd66a 0840
    cmp r0,#0x0                              @ 080cd66c 0028
    beq LAB_080cd652                         @ 080cd66e f0d0
    ldr r3, DAT_080cd6a0                     @ 080cd670 0b4b
    adds r1,r4,r3    @ 080cd672 e118
    ldrh r0,[r1,#0x0]                        @ 080cd674 0888
    cmp r0,#0x0                              @ 080cd676 0028
    bne LAB_080cd686                         @ 080cd678 05d1
    ldr r2, DAT_080cd69c                     @ 080cd67a 084a
    adds r0,r4,r2    @ 080cd67c a018
    ldrh r3,[r0,#0x0]                        @ 080cd67e 0388
    lsrs r0,r3,#0x4    @ 080cd680 1809
    lsls r0,r0,#0x18    @ 080cd682 0006
    lsrs r0,r0,#0x18    @ 080cd684 000e
LAB_080cd686:
    subs r0,#0x1    @ 080cd686 0138
LAB_080cd688:
    strh r0,[r1,#0x0]                        @ 080cd688 0880
    movs r0,#0x0    @ 080cd68a 0020
    bl sync_state_and_init_sprite            @ 080cd68c 2cf012fa
    b LAB_080cd864                           @ 080cd690 e8e0
    .zero  0x2
PTR_gPrng_080cd694:
    .word  gPrng                          @ 080cd694 40000003
DAT_080cd698:
    .word  0x00000a02                     @ 080cd698 020a0000
DAT_080cd69c:
    .word  0x00000a0e                     @ 080cd69c 0e0a0000
DAT_080cd6a0:
    .word  0x00000a14                     @ 080cd6a0 140a0000
LAB_080cd6a4:
    movs r0,#0x10    @ 080cd6a4 1020
    ands r0,r1    @ 080cd6a6 0840
    cmp r0,#0x0                              @ 080cd6a8 0028
    beq LAB_080cd704                         @ 080cd6aa 2bd0
    ldr r1, DAT_080cd6f4                     @ 080cd6ac 1149
    adds r0,r4,r1    @ 080cd6ae 6018
    ldrb r6,[r0,#0x0]                        @ 080cd6b0 0678
    ldr r2, DAT_080cd6f8                     @ 080cd6b2 114a
    adds r5,r4,r2    @ 080cd6b4 a518
    movs r7,#0xf    @ 080cd6b6 0f27
    movs r3,#0x10    @ 080cd6b8 1023
    rsbs r3,r3,#0    @ 080cd6ba 5b42
LAB_080cd6bc:
    ldrb r2,[r5,#0x0]                        @ 080cd6bc 2a78
    lsls r1,r2,#0x1c    @ 080cd6be 1107
    lsrs r1,r1,#0x1c    @ 080cd6c0 090f
    adds r1,#0x1    @ 080cd6c2 0131
    ands r1,r7    @ 080cd6c4 3940
    adds r0,r3,#0x0    @ 080cd6c6 181c
    ands r0,r2    @ 080cd6c8 1040
    orrs r0,r1    @ 080cd6ca 0843
    strb r0,[r5,#0x0]                        @ 080cd6cc 2870
    adds r0,r6,#0x0    @ 080cd6ce 301c
    asrs r0,r1    @ 080cd6d0 0841
    movs r1,#0x1    @ 080cd6d2 0121
    ands r0,r1    @ 080cd6d4 0840
    cmp r0,#0x0                              @ 080cd6d6 0028
    beq LAB_080cd6bc                         @ 080cd6d8 f0d0
    ldr r3, DAT_080cd6fc                     @ 080cd6da 084b
    adds r1,r4,r3    @ 080cd6dc e118
    ldrh r2,[r1,#0x0]                        @ 080cd6de 0a88
    subs r3,#0x6    @ 080cd6e0 063b
    adds r0,r4,r3    @ 080cd6e2 e018
    ldrh r0,[r0,#0x0]                        @ 080cd6e4 0088
    lsls r0,r0,#0x14    @ 080cd6e6 0005
    lsrs r0,r0,#0x18    @ 080cd6e8 000e
    subs r0,#0x1    @ 080cd6ea 0138
    cmp r2,r0                                @ 080cd6ec 8242
    bne LAB_080cd700                         @ 080cd6ee 07d1
    movs r0,#0x0    @ 080cd6f0 0020
    b LAB_080cd688                           @ 080cd6f2 c9e7
DAT_080cd6f4:
    .word  0x00000a02                     @ 080cd6f4 020a0000
DAT_080cd6f8:
    .word  0x00000a0e                     @ 080cd6f8 0e0a0000
DAT_080cd6fc:
    .word  0x00000a14                     @ 080cd6fc 140a0000
LAB_080cd700:
    adds r0,r2,#0x1    @ 080cd700 501c
    b LAB_080cd688                           @ 080cd702 c1e7
LAB_080cd704:
    movs r0,#0x1    @ 080cd704 0120
    ands r0,r1    @ 080cd706 0840
    cmp r0,#0x0                              @ 080cd708 0028
    beq LAB_080cd7e8                         @ 080cd70a 6dd0
    ldr r0, DAT_080cd734                     @ 080cd70c 0948
    adds r2,r4,r0    @ 080cd70e 2218
    ldrh r1,[r2,#0x0]                        @ 080cd710 1188
    adds r0,#0xa    @ 080cd712 0a30
    adds r3,r4,r0    @ 080cd714 2318
    ldrh r0,[r3,#0x0]                        @ 080cd716 1888
    adds r0,#0x1    @ 080cd718 0130
    cmp r1,r0                                @ 080cd71a 8142
    bne LAB_080cd73c                         @ 080cd71c 0ed1
    strh r7,[r2,#0x0]                        @ 080cd71e 1780
    ldr r2, DAT_080cd738                     @ 080cd720 054a
    adds r1,r4,r2    @ 080cd722 a118
    ldrh r0,[r1,#0x0]                        @ 080cd724 0888
    subs r0,#0x1    @ 080cd726 0138
    strh r0,[r1,#0x0]                        @ 080cd728 0880
LAB_080cd72a:
    movs r0,#0x1    @ 080cd72a 0120
    bl sync_state_and_init_sprite            @ 080cd72c 2cf0c2f9
    b LAB_080cd864                           @ 080cd730 98e0
    .zero  0x2
DAT_080cd734:
    .word  0x00000a0a                     @ 080cd734 0a0a0000
DAT_080cd738:
    .word  0x00000a08                     @ 080cd738 080a0000
LAB_080cd73c:
    ldr r0, DAT_080cd750                     @ 080cd73c 0448
    adds r1,r4,r0    @ 080cd73e 2118
    ldrh r0,[r1,#0x0]                        @ 080cd740 0888
    adds r0,#0x1    @ 080cd742 0130
    strh r0,[r1,#0x0]                        @ 080cd744 0880
    ldrh r2,[r3,#0x0]                        @ 080cd746 1a88
    adds r2,#0x1    @ 080cd748 0132
    movs r0,#0x0    @ 080cd74a 0020
    b LAB_080cd756                           @ 080cd74c 03e0
    .zero  0x2
DAT_080cd750:
    .word  0x00000a08                     @ 080cd750 080a0000
LAB_080cd754:
    adds r0,r5,#0x0    @ 080cd754 281c
LAB_080cd756:
    adds r5,r0,#0x1    @ 080cd756 451c
    cmp r0,#0x5                              @ 080cd758 0528
    bgt LAB_080cd772                         @ 080cd75a 0adc
    ldr r1, DAT_080cd7b8                     @ 080cd75c 1649
    adds r0,r4,r1    @ 080cd75e 6018
    ldrb r0,[r0,#0x0]                        @ 080cd760 0078
    asrs r0,r5    @ 080cd762 2841
    movs r1,#0x1    @ 080cd764 0121
    ands r0,r1    @ 080cd766 0840
    cmp r0,#0x0                              @ 080cd768 0028
    beq LAB_080cd76e                         @ 080cd76a 00d0
    subs r2,#0x1    @ 080cd76c 013a
LAB_080cd76e:
    cmp r2,#0x0                              @ 080cd76e 002a
    bne LAB_080cd754                         @ 080cd770 f0d1
LAB_080cd772:
    ldr r2, DAT_080cd7bc                     @ 080cd772 124a
    adds r1,r4,r2    @ 080cd774 a118
    ldr r3, DAT_080cd7c0                     @ 080cd776 124b
    adds r0,r4,r3    @ 080cd778 e018
    ldrh r1,[r1,#0x0]                        @ 080cd77a 0988
    ldrh r0,[r0,#0x0]                        @ 080cd77c 0088
    cmp r1,r0                                @ 080cd77e 8142
    bne LAB_080cd7d4                         @ 080cd780 28d1
    ldr r0, DAT_080cd7c4                     @ 080cd782 1048
    adds r2,r4,r0    @ 080cd784 2218
    movs r0,#0x1    @ 080cd786 0120
    adds r1,r0,#0x0    @ 080cd788 011c
    ldrh r2,[r2,#0x0]                        @ 080cd78a 1288
    lsls r1,r2    @ 080cd78c 9140
    lsls r0,r5    @ 080cd78e a840
    orrs r1,r0    @ 080cd790 0143
    ldr r0, PTR_gP1LifePoints_080cd7c8       @ 080cd792 0d48
    movs r2,#0xea    @ 080cd794 ea22
    lsls r2,r2,#0x5    @ 080cd796 5201
    adds r0,r0,r2    @ 080cd798 8018
    str r1,[r0,#0x0]                         @ 080cd79a 0160
    ldr r0, DAT_080cd7cc                     @ 080cd79c 0b48
    adds r3,r4,r0    @ 080cd79e 2318
    ldr r2,[r3,#0x0]                         @ 080cd7a0 1a68
    lsls r1,r2,#0xf    @ 080cd7a2 d103
    lsrs r1,r1,#0x18    @ 080cd7a4 090e
    adds r1,#0x1    @ 080cd7a6 0131
    movs r0,#0xff    @ 080cd7a8 ff20
    ands r1,r0    @ 080cd7aa 0140
    lsls r1,r1,#0x9    @ 080cd7ac 4902
    ldr r0, DAT_080cd7d0                     @ 080cd7ae 0848
    ands r0,r2    @ 080cd7b0 1040
    orrs r0,r1    @ 080cd7b2 0843
    str r0,[r3,#0x0]                         @ 080cd7b4 1860
    b LAB_080cd7da                           @ 080cd7b6 10e0
DAT_080cd7b8:
    .word  0x00000a02                     @ 080cd7b8 020a0000
DAT_080cd7bc:
    .word  0x00000a08                     @ 080cd7bc 080a0000
DAT_080cd7c0:
    .word  0x00000a06                     @ 080cd7c0 060a0000
DAT_080cd7c4:
    .word  0x00000a0a                     @ 080cd7c4 0a0a0000
PTR_gP1LifePoints_080cd7c8:
    .word  gP1LifePoints                  @ 080cd7c8 e0c40102
DAT_080cd7cc:
    .word  0x00000a18                     @ 080cd7cc 180a0000
DAT_080cd7d0:
    .word  0xfffe01ff                     @ 080cd7d0 ff01feff
LAB_080cd7d4:
    ldr r1, DAT_080cd7e4                     @ 080cd7d4 0349
    adds r0,r4,r1    @ 080cd7d6 6018
    strh r5,[r0,#0x0]                        @ 080cd7d8 0580
LAB_080cd7da:
    movs r0,#0x24    @ 080cd7da 2420
    bl sync_state_and_init_sprite            @ 080cd7dc 2cf06af9
    b LAB_080cd864                           @ 080cd7e0 40e0
    .zero  0x2
DAT_080cd7e4:
    .word  0x00000a0a                     @ 080cd7e4 0a0a0000
LAB_080cd7e8:
    movs r0,#0x2    @ 080cd7e8 0220
    ands r0,r1    @ 080cd7ea 0840
    cmp r0,#0x0                              @ 080cd7ec 0028
    beq LAB_080cd864                         @ 080cd7ee 39d0
    ldr r3, DAT_080cd808                     @ 080cd7f0 054b
    adds r2,r4,r3    @ 080cd7f2 e218
    ldrh r1,[r2,#0x0]                        @ 080cd7f4 1188
    cmp r1,#0x0                              @ 080cd7f6 0029
    beq LAB_080cd80c                         @ 080cd7f8 08d0
    adds r3,#0x2    @ 080cd7fa 0233
    adds r0,r4,r3    @ 080cd7fc e018
    strh r7,[r0,#0x0]                        @ 080cd7fe 0780
    subs r0,r1,#0x1    @ 080cd800 481e
    strh r0,[r2,#0x0]                        @ 080cd802 1080
    b LAB_080cd72a                           @ 080cd804 91e7
    .zero  0x2
DAT_080cd808:
    .word  0x00000a08                     @ 080cd808 080a0000
LAB_080cd80c:
    movs r0,#0x2    @ 080cd80c 0220
    bl sync_state_and_init_sprite            @ 080cd80e 2cf051f9
    b LAB_080cd864                           @ 080cd812 27e0
LAB_080cd814:
    ldr r0, DAT_080cd85c                     @ 080cd814 1148
    adds r0,r0,r4    @ 080cd816 0019
    .hword 0x4680    @ 080cd818 8046
    ldrb r6,[r0,#0x0]                        @ 080cd81a 0678
    lsrs r0,r6,#0x1    @ 080cd81c 7008
    ldr r1, DAT_080cd860                     @ 080cd81e 1049
    adds r4,r4,r1    @ 080cd820 6418
    adds r3,r7,#0x0    @ 080cd822 3b1c
    ldrb r2,[r4,#0x0]                        @ 080cd824 2278
    ands r3,r2    @ 080cd826 1340
    lsls r3,r3,#0x7    @ 080cd828 db01
    orrs r3,r0    @ 080cd82a 0343
    adds r2,r3,#0x1    @ 080cd82c 5a1c
    movs r1,#0x7f    @ 080cd82e 7f21
    ands r1,r2    @ 080cd830 1140
    lsls r1,r1,#0x1    @ 080cd832 4900
    movs r5,#0x1    @ 080cd834 0125
    adds r0,r7,#0x0    @ 080cd836 381c
    ands r0,r6    @ 080cd838 3040
    orrs r0,r1    @ 080cd83a 0843
    .hword 0x4641    @ 080cd83c 4146
    strb r0,[r1,#0x0]                        @ 080cd83e 0870
    lsrs r2,r2,#0x7    @ 080cd840 d209
    ands r2,r7    @ 080cd842 3a40
    ands r2,r5    @ 080cd844 2a40
    movs r0,#0x2    @ 080cd846 0220
    rsbs r0,r0,#0    @ 080cd848 4042
    ldrb r1,[r4,#0x0]                        @ 080cd84a 2178
    ands r0,r1    @ 080cd84c 0840
    orrs r0,r2    @ 080cd84e 1043
    strb r0,[r4,#0x0]                        @ 080cd850 2070
    cmp r3,#0x1f                             @ 080cd852 1f2b
    bls LAB_080cd864                         @ 080cd854 06d9
    movs r0,#0x1    @ 080cd856 0120
    b LAB_080cd866                           @ 080cd858 05e0
    .zero  0x2
DAT_080cd85c:
    .word  0x00000a1b                     @ 080cd85c 1b0a0000
DAT_080cd860:
    .word  0x00000a1c                     @ 080cd860 1c0a0000
LAB_080cd864:
    movs r0,#0x0    @ 080cd864 0020
LAB_080cd866:
    pop {r3}                                 @ 080cd866 08bc
    .hword 0x4698    @ 080cd868 9846
    pop {r4,r5,r6,r7}                        @ 080cd86a f0bc
    pop {r1}                                 @ 080cd86c 02bc
    bx r1                                    @ 080cd86e 0847

@ 由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). 与 080cda6c 结构高度对称, 但末尾使用直接行列计算而非 nibble 循环. 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); 设置语言模式 (STATE+0x8); 从 font_jp_base_table 取字体基址; 调用 render_jp_string_to_tile_line; 调用 write_line_buf_to_bg_tile_vram 写 BG VRAM. 然后检查状态字段 (STATE+0x0a16/0x0a17 双标志), 若均为 0: 将 render 返回值 r4-1 作为 tile_width 写入 STATE+0x0a03 halfword; 再计算 tile_row (r4+0x10 除以 8) 和 tile_col (r4+0x10 & 7), 若有余则 tile_row+1, 最终写入 STATE+0x0a02 byte. Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, OFFSET_TILE_WIDTH=0x0a03, OFFSET_TILE_ROW=0x0a02, VRAM_BG=0x06014000, OFFSET_FLAG_A=0x0a16, OFFSET_FLAG_B=0x0a17, TILE_ALIGN=8.
render_jp_label_row_with_tile_pos:
    push {r4,r5,r6,r7,lr}                    @ 080cd870 f0b5
    sub sp,#0x4                              @ 080cd872 81b0
    movs r6,#0x0    @ 080cd874 0026
    movs r0,#0x17    @ 080cd876 1720
    movs r1,#0x10    @ 080cd878 1021
    movs r2,#0x1    @ 080cd87a 0122
    movs r3,#0x2    @ 080cd87c 0223
    bl setup_line_buf_with_font_and_align    @ 080cd87e 23f01ffa
    ldr r2, DAT_080cd924                     @ 080cd882 284a
    ldr r0, DAT_080cd928                     @ 080cd884 2848
    ldr r1, DAT_080cd92c                     @ 080cd886 2949
    adds r0,r0,r1    @ 080cd888 4018
    movs r7,#0x7    @ 080cd88a 0727
    adds r1,r7,#0x0    @ 080cd88c 391c
    ldrb r0,[r0,#0x0]                        @ 080cd88e 0078
    ands r1,r0    @ 080cd890 0140
    rsbs r1,r1,#0    @ 080cd892 4942
    lsrs r1,r1,#0x1f    @ 080cd894 c90f
    movs r0,#0x2    @ 080cd896 0220
    rsbs r0,r0,#0    @ 080cd898 4042
    ldrb r3,[r2,#0x8]                        @ 080cd89a 137a
    ands r0,r3    @ 080cd89c 1840
    orrs r0,r1    @ 080cd89e 0843
    movs r1,#0x2    @ 080cd8a0 0221
    orrs r0,r1    @ 080cd8a2 0843
    strb r0,[r2,#0x8]                        @ 080cd8a4 1072
    ldr r3, PTR_font_jp_base_table_080cd930  @ 080cd8a6 224b
    lsls r1,r0,#0x1e    @ 080cd8a8 8107
    lsrs r1,r1,#0x1f    @ 080cd8aa c90f
    lsls r1,r1,#0x2    @ 080cd8ac 8900
    lsls r0,r0,#0x1f    @ 080cd8ae c007
    lsrs r0,r0,#0x1f    @ 080cd8b0 c00f
    lsls r0,r0,#0x3    @ 080cd8b2 c000
    adds r1,r1,r0    @ 080cd8b4 0918
    adds r1,r1,r3    @ 080cd8b6 c918
    ldr r0,[r1,#0x0]                         @ 080cd8b8 0868
    str r0,[r2,#0x4]                         @ 080cd8ba 5060
    movs r0,#0x40    @ 080cd8bc 4020
    ldrb r1,[r2,#0x15]                       @ 080cd8be 517d
    orrs r0,r1    @ 080cd8c0 0843
    strb r0,[r2,#0x15]                       @ 080cd8c2 5075
    ldr r5, DAT_080cd934                     @ 080cd8c4 1b4d
    str r6,[sp,#0x0]                         @ 080cd8c6 0096
    movs r0,#0x2    @ 080cd8c8 0220
    movs r1,#0x2    @ 080cd8ca 0221
    adds r2,r5,#0x0    @ 080cd8cc 2a1c
    movs r3,#0xc    @ 080cd8ce 0c23
    bl render_jp_string_to_tile_line         @ 080cd8d0 f9f7f6fe
    adds r4,r0,#0x0    @ 080cd8d4 041c
    subs r1,r4,#0x1    @ 080cd8d6 611e
    ldr r2, DAT_080cd938                     @ 080cd8d8 174a
    adds r0,r5,r2    @ 080cd8da a818
    strh r1,[r0,#0x0]                        @ 080cd8dc 0180
    subs r4,#0x2    @ 080cd8de 023c
    ldr r0, DAT_080cd93c                     @ 080cd8e0 1648
    movs r1,#0x0    @ 080cd8e2 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cd8e4 25f076ff
    ldr r3, DAT_080cd940                     @ 080cd8e8 154b
    adds r0,r5,r3    @ 080cd8ea e818
    ldrb r0,[r0,#0x0]                        @ 080cd8ec 0078
    lsrs r2,r0,#0x1    @ 080cd8ee 4208
    ldr r0, DAT_080cd944                     @ 080cd8f0 1448
    adds r1,r5,r0    @ 080cd8f2 2918
    movs r0,#0x1    @ 080cd8f4 0120
    ldrb r1,[r1,#0x0]                        @ 080cd8f6 0978
    ands r0,r1    @ 080cd8f8 0840
    lsls r0,r0,#0x7    @ 080cd8fa c001
    orrs r0,r2    @ 080cd8fc 1043
    cmp r0,#0x0                              @ 080cd8fe 0028
    bne LAB_080cd91c                         @ 080cd900 0cd1
    adds r4,#0x10    @ 080cd902 1034
    adds r0,r4,#0x0    @ 080cd904 201c
    cmp r4,#0x0                              @ 080cd906 002c
    bge LAB_080cd90c                         @ 080cd908 00da
    adds r0,r4,#0x7    @ 080cd90a e01d
LAB_080cd90c:
    asrs r6,r0,#0x3    @ 080cd90c c610
    ands r4,r7    @ 080cd90e 3c40
    cmp r4,#0x0                              @ 080cd910 002c
    beq LAB_080cd916                         @ 080cd912 00d0
    adds r6,#0x1    @ 080cd914 0136
LAB_080cd916:
    ldr r1, DAT_080cd948                     @ 080cd916 0c49
    adds r0,r5,r1    @ 080cd918 6818
    strb r6,[r0,#0x0]                        @ 080cd91a 0670
LAB_080cd91c:
    add sp,#0x4                              @ 080cd91c 01b0
    pop {r4,r5,r6,r7}                        @ 080cd91e f0bc
    pop {r0}                                 @ 080cd920 01bc
    bx r0                                    @ 080cd922 0047
DAT_080cd924:
    .word  0x02006ed0                     @ 080cd924 d06e0002
DAT_080cd928:
    .word  0x02000000                     @ 080cd928 00000002
DAT_080cd92c:
    .word  0x00006c2c                     @ 080cd92c 2c6c0000
PTR_font_jp_base_table_080cd930:
    .word  font_jp_base_table             @ 080cd930 54f8e509
DAT_080cd934:
    .word  0x0201f441                     @ 080cd934 41f40102
DAT_080cd938:
    .word  0x00000a03                     @ 080cd938 030a0000
DAT_080cd93c:
    .word  0x06014000                     @ 080cd93c 00400106
DAT_080cd940:
    .word  0x00000a16                     @ 080cd940 160a0000
DAT_080cd944:
    .word  0x00000a17                     @ 080cd944 170a0000
DAT_080cd948:
    .word  0x00000a02                     @ 080cd948 020a0000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Shortest of the 8 sibling functions: no nibble rotate, no LP write. Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. Reads gPrng+0x148 (=gPrng+0xa4*2) low 2 bits: if bit0=1 or bit1=1, calls sync_state_and_init_sprite(0x24), returns 1; else returns 0. Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; FLAG_OFFSET=gPrng+0x148; MASK_BITS12=0x3; SYNC_OP=0x24.
render_card_list_oam_row_by_flag_check:
    push {lr}                                @ 080cd94c 00b5
    ldr r0, DAT_080cd98c                     @ 080cd94e 0f48
    ldr r1, DAT_080cd990                     @ 080cd950 0f49
    adds r0,r0,r1    @ 080cd952 4018
    ldrb r3,[r0,#0x0]                        @ 080cd954 0378
    lsrs r0,r3,#0x1    @ 080cd956 5808
    movs r1,#0xa    @ 080cd958 0a21
    subs r1,r1,r0    @ 080cd95a 091a
    lsls r1,r1,#0x3    @ 080cd95c c900
    movs r2,#0xfe    @ 080cd95e fe22
    lsls r2,r2,#0x1    @ 080cd960 5200
    movs r0,#0x30    @ 080cd962 3020
    bl write_card_list_oam_row_strip         @ 080cd964 f9f7e4fd
    ldr r0, PTR_gPrng_080cd994               @ 080cd968 0a48
    movs r1,#0xa4    @ 080cd96a a421
    lsls r1,r1,#0x1    @ 080cd96c 4900
    adds r0,r0,r1    @ 080cd96e 4018
    ldrh r1,[r0,#0x0]                        @ 080cd970 0188
    movs r0,#0x1    @ 080cd972 0120
    ands r0,r1    @ 080cd974 0840
    cmp r0,#0x0                              @ 080cd976 0028
    bne LAB_080cd982                         @ 080cd978 03d1
    movs r0,#0x2    @ 080cd97a 0220
    ands r0,r1    @ 080cd97c 0840
    cmp r0,#0x0                              @ 080cd97e 0028
    beq LAB_080cd998                         @ 080cd980 0ad0
LAB_080cd982:
    movs r0,#0x24    @ 080cd982 2420
    bl sync_state_and_init_sprite            @ 080cd984 2cf096f8
    movs r0,#0x1    @ 080cd988 0120
    b LAB_080cd99a                           @ 080cd98a 06e0
DAT_080cd98c:
    .word  0x0201f440                     @ 080cd98c 40f40102
DAT_080cd990:
    .word  0x00000a03                     @ 080cd990 030a0000
PTR_gPrng_080cd994:
    .word  gPrng                          @ 080cd994 40000003
LAB_080cd998:
    movs r0,#0x0    @ 080cd998 0020
LAB_080cd99a:
    pop {r1}                                 @ 080cd99a 02bc
    bx r1                                    @ 080cd99c 0847
    .zero  0x2

@ Initialize palette and tile VRAM regions for the card display screen. Fills OBJ palette and BG palette with card display colors from ROM palette table; zero-fills BG tile VRAM region for text layer. No APCS params (reads display state from globals). Returns void. Side effects: OBJ palette, BG palette, BG tile VRAM written. Constants: card_palette_table_base in ROM; bios_cpu_set fill mode.
init_card_palette_and_tile_vram:
    push {r4,r5,r6,r7,lr}                    @ 080cd9a0 f0b5
    adds r5,r0,#0x0    @ 080cd9a2 051c
    ldr r0, DAT_080cda34                     @ 080cd9a4 2348
    movs r1,#0x80    @ 080cd9a6 8021
    lsls r1,r1,#0x7    @ 080cd9a8 c901
    bl zero_fill_by_halfword                 @ 080cd9aa 27f063fa
    ldr r0, DAT_080cda38                     @ 080cd9ae 2248
    ldr r1, DAT_080cda3c                     @ 080cd9b0 2249
    movs r2,#0x12    @ 080cd9b2 1222
    movs r3,#0x3    @ 080cd9b4 0323
    bl tile_2d_row_copy                      @ 080cd9b6 29f08dfd
    ldr r0, DAT_080cda40                     @ 080cd9ba 2148
    ldr r1, DAT_080cda44                     @ 080cd9bc 2149
    movs r2,#0x20    @ 080cd9be 2022
    bl copy_bytes_by_halfword                @ 080cd9c0 27f070fa
    ldr r0, DAT_080cda48                     @ 080cd9c4 2048
    ldr r1, DAT_080cda4c                     @ 080cd9c6 2149
    movs r2,#0x1    @ 080cd9c8 0122
    movs r3,#0x1    @ 080cd9ca 0123
    bl tile_2d_row_copy                      @ 080cd9cc 29f082fd
    ldr r4, DAT_080cda50                     @ 080cd9d0 1f4c
    ldr r1, DAT_080cda54                     @ 080cd9d2 2049
    adds r0,r4,r1    @ 080cd9d4 6018
    ldrb r0,[r0,#0x0]                        @ 080cd9d6 0078
    lsrs r2,r0,#0x1    @ 080cd9d8 4208
    ldr r0, DAT_080cda58                     @ 080cd9da 1f48
    adds r1,r4,r0    @ 080cd9dc 2118
    movs r0,#0x1    @ 080cd9de 0120
    ldrb r1,[r1,#0x0]                        @ 080cd9e0 0978
    ands r0,r1    @ 080cd9e2 0840
    lsls r0,r0,#0x7    @ 080cd9e4 c001
    orrs r0,r2    @ 080cd9e6 1043
    cmp r0,#0x0                              @ 080cd9e8 0028
    bne LAB_080cda24                         @ 080cd9ea 1bd1
    ldr r1, DAT_080cda5c                     @ 080cd9ec 1b49
    adds r0,r4,r1    @ 080cd9ee 6018
    strb r5,[r0,#0x0]                        @ 080cd9f0 0570
    movs r3,#0x0    @ 080cd9f2 0023
    ldrb r5,[r0,#0x0]                        @ 080cd9f4 0578
    ldr r0, DAT_080cda60                     @ 080cd9f6 1a48
    adds r4,r4,r0    @ 080cd9f8 2418
    movs r6,#0x1    @ 080cd9fa 0126
    ldr r7, DAT_080cda64                     @ 080cd9fc 194f
LAB_080cd9fe:
    adds r0,r5,#0x0    @ 080cd9fe 281c
    asrs r0,r3    @ 080cda00 1841
    ands r0,r6    @ 080cda02 3040
    cmp r0,#0x0                              @ 080cda04 0028
    beq LAB_080cda1e                         @ 080cda06 0ad0
    ldrh r2,[r4,#0x0]                        @ 080cda08 2288
    lsls r1,r2,#0x14    @ 080cda0a 1105
    lsrs r1,r1,#0x18    @ 080cda0c 090e
    adds r1,#0x1    @ 080cda0e 0131
    movs r0,#0xff    @ 080cda10 ff20
    ands r1,r0    @ 080cda12 0140
    lsls r1,r1,#0x4    @ 080cda14 0901
    adds r0,r7,#0x0    @ 080cda16 381c
    ands r0,r2    @ 080cda18 1040
    orrs r0,r1    @ 080cda1a 0843
    strh r0,[r4,#0x0]                        @ 080cda1c 2080
LAB_080cda1e:
    adds r3,#0x1    @ 080cda1e 0133
    cmp r3,#0x5                              @ 080cda20 052b
    ble LAB_080cd9fe                         @ 080cda22 ecdd
LAB_080cda24:
    ldr r0, DAT_080cda50                     @ 080cda24 0a48
    ldr r1, DAT_080cda68                     @ 080cda26 1049
    adds r0,r0,r1    @ 080cda28 4018
    movs r1,#0x4    @ 080cda2a 0421
    strb r1,[r0,#0x0]                        @ 080cda2c 0170
    pop {r4,r5,r6,r7}                        @ 080cda2e f0bc
    pop {r0}                                 @ 080cda30 01bc
    bx r0                                    @ 080cda32 0047
DAT_080cda34:
    .word  0x06014000                     @ 080cda34 00400106
DAT_080cda38:
    .word  0x06013000                     @ 080cda38 00300106
DAT_080cda3c:
    .word  0x0988a0f8                     @ 080cda3c f8a08809
DAT_080cda40:
    .word  0x050002c0                     @ 080cda40 c0020005
DAT_080cda44:
    .word  0x0988a7b8                     @ 080cda44 b8a78809
DAT_080cda48:
    .word  0x06010c00                     @ 080cda48 000c0106
DAT_080cda4c:
    .word  0x0988aaf8                     @ 080cda4c f8aa8809
DAT_080cda50:
    .word  0x0201f440                     @ 080cda50 40f40102
DAT_080cda54:
    .word  0x00000a17                     @ 080cda54 170a0000
DAT_080cda58:
    .word  0x00000a18                     @ 080cda58 180a0000
DAT_080cda5c:
    .word  0x00000a02                     @ 080cda5c 020a0000
DAT_080cda60:
    .word  0x00000a0e                     @ 080cda60 0e0a0000
DAT_080cda64:
    .word  0xfffff00f                     @ 080cda64 0ff0ffff
DAT_080cda68:
    .word  0x00000a01                     @ 080cda68 010a0000

@ 由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); 设置语言模式 (STATE_BASE+0x8); 从 font_jp_base_table 取字体基址; 调用 render_jp_string_to_tile_line 一次; 调用 write_line_buf_to_bg_tile_vram 将 JP 文字写入 VRAM. 随后检查状态字段 (STATE_BASE+0x0a16/0x0a17 双标志), 若均为 0: 计算 tile 行列位置 (asrs r0,r4,#3 行; ands r4,r7=#7 列), 将 tile_pos halfword 写入 STATE_BASE+0x0a03; 另外读状态字段 +0x0a0d (palette/tile nibble), 递增 nibble 字段并写回; 最终将 tile_row_count 写入 STATE_BASE+0x0a03-1 (base_ptr-1 字节). Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, OFFSET_FLAG_A=0x0a16, OFFSET_FLAG_B=0x0a17, OFFSET_TILE_POS=0x0a03, OFFSET_NIBBLE=0x0a0d, VRAM_BG=0x06014000, TILE_MASK=0x7.
render_jp_label_row_with_tile_count:
    push {r4,r5,r6,r7,lr}                    @ 080cda6c f0b5
    .hword 0x464f    @ 080cda6e 4f46
    .hword 0x4646    @ 080cda70 4646
    push {r6,r7}                             @ 080cda72 c0b4
    sub sp,#0x4                              @ 080cda74 81b0
    movs r6,#0x0    @ 080cda76 0026
    movs r0,#0x17    @ 080cda78 1720
    movs r1,#0x10    @ 080cda7a 1021
    movs r2,#0x1    @ 080cda7c 0122
    movs r3,#0x2    @ 080cda7e 0223
    bl setup_line_buf_with_font_and_align    @ 080cda80 23f01ef9
    ldr r2, DAT_080cdb80                     @ 080cda84 3e4a
    ldr r0, DAT_080cdb84                     @ 080cda86 3f48
    ldr r1, DAT_080cdb88                     @ 080cda88 3f49
    adds r0,r0,r1    @ 080cda8a 4018
    movs r1,#0x7    @ 080cda8c 0721
    ldrb r0,[r0,#0x0]                        @ 080cda8e 0078
    ands r1,r0    @ 080cda90 0140
    rsbs r1,r1,#0    @ 080cda92 4942
    lsrs r1,r1,#0x1f    @ 080cda94 c90f
    movs r0,#0x2    @ 080cda96 0220
    rsbs r0,r0,#0    @ 080cda98 4042
    ldrb r3,[r2,#0x8]                        @ 080cda9a 137a
    ands r0,r3    @ 080cda9c 1840
    orrs r0,r1    @ 080cda9e 0843
    movs r1,#0x2    @ 080cdaa0 0221
    orrs r0,r1    @ 080cdaa2 0843
    strb r0,[r2,#0x8]                        @ 080cdaa4 1072
    ldr r3, PTR_font_jp_base_table_080cdb8c  @ 080cdaa6 394b
    lsls r1,r0,#0x1e    @ 080cdaa8 8107
    lsrs r1,r1,#0x1f    @ 080cdaaa c90f
    lsls r1,r1,#0x2    @ 080cdaac 8900
    lsls r0,r0,#0x1f    @ 080cdaae c007
    lsrs r0,r0,#0x1f    @ 080cdab0 c00f
    lsls r0,r0,#0x3    @ 080cdab2 c000
    adds r1,r1,r0    @ 080cdab4 0918
    adds r1,r1,r3    @ 080cdab6 c918
    ldr r0,[r1,#0x0]                         @ 080cdab8 0868
    str r0,[r2,#0x4]                         @ 080cdaba 5060
    movs r0,#0x40    @ 080cdabc 4020
    ldrb r1,[r2,#0x15]                       @ 080cdabe 517d
    orrs r0,r1    @ 080cdac0 0843
    strb r0,[r2,#0x15]                       @ 080cdac2 5075
    ldr r5, DAT_080cdb90                     @ 080cdac4 324d
    str r6,[sp,#0x0]                         @ 080cdac6 0096
    movs r0,#0x2    @ 080cdac8 0220
    movs r1,#0x2    @ 080cdaca 0221
    adds r2,r5,#0x0    @ 080cdacc 2a1c
    movs r3,#0xc    @ 080cdace 0c23
    bl render_jp_string_to_tile_line         @ 080cdad0 f9f7f6fd
    adds r4,r0,#0x0    @ 080cdad4 041c
    ldr r0, DAT_080cdb94                     @ 080cdad6 2f48
    movs r1,#0x0    @ 080cdad8 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cdada 25f07bfe
    ldr r2, DAT_080cdb98                     @ 080cdade 2e4a
    adds r0,r5,r2    @ 080cdae0 a818
    ldrb r0,[r0,#0x0]                        @ 080cdae2 0078
    lsrs r2,r0,#0x1    @ 080cdae4 4208
    ldr r3, DAT_080cdb9c                     @ 080cdae6 2d4b
    adds r1,r5,r3    @ 080cdae8 e918
    movs r7,#0x1    @ 080cdaea 0127
    adds r0,r7,#0x0    @ 080cdaec 381c
    ldrb r1,[r1,#0x0]                        @ 080cdaee 0978
    ands r0,r1    @ 080cdaf0 0840
    lsls r0,r0,#0x7    @ 080cdaf2 c001
    orrs r0,r2    @ 080cdaf4 1043
    cmp r0,#0x0                              @ 080cdaf6 0028
    bne LAB_080cdb70                         @ 080cdaf8 3ad1
    adds r1,r4,#0x3    @ 080cdafa e11c
    ldr r2, DAT_080cdba0                     @ 080cdafc 284a
    adds r0,r5,r2    @ 080cdafe a818
    strh r1,[r0,#0x0]                        @ 080cdb00 0180
    adds r4,#0x1c    @ 080cdb02 1c34
    subs r3,#0x16    @ 080cdb04 163b
    adds r0,r5,r3    @ 080cdb06 e818
    ldrb r2,[r0,#0x0]                        @ 080cdb08 0278
    ldr r0, DAT_080cdba4                     @ 080cdb0a 2648
    adds r6,r5,r0    @ 080cdb0c 2e18
    ldrb r3,[r6,#0x0]                        @ 080cdb0e 3378
    lsls r1,r3,#0x1c    @ 080cdb10 1907
    lsrs r1,r1,#0x1c    @ 080cdb12 090f
    adds r0,r2,#0x0    @ 080cdb14 101c
    asrs r0,r1    @ 080cdb16 0841
    ands r0,r7    @ 080cdb18 3840
    subs r5,#0x1    @ 080cdb1a 013d
    .hword 0x46a9    @ 080cdb1c a946
    cmp r0,#0x0                              @ 080cdb1e 0028
    bne LAB_080cdb54                         @ 080cdb20 18d1
    .hword 0x46b0    @ 080cdb22 b046
    movs r1,#0x10    @ 080cdb24 1021
    rsbs r1,r1,#0    @ 080cdb26 4942
    .hword 0x468c    @ 080cdb28 8c46
    adds r5,r2,#0x0    @ 080cdb2a 151c
    adds r2,r3,#0x0    @ 080cdb2c 1a1c
    movs r7,#0xf    @ 080cdb2e 0f27
    movs r6,#0x1    @ 080cdb30 0126
LAB_080cdb32:
    lsls r0,r2,#0x1c    @ 080cdb32 1007
    lsrs r0,r0,#0x1c    @ 080cdb34 000f
    adds r0,#0x1    @ 080cdb36 0130
    ands r0,r7    @ 080cdb38 3840
    .hword 0x4663    @ 080cdb3a 6346
    ands r3,r2    @ 080cdb3c 1340
    orrs r3,r0    @ 080cdb3e 0343
    adds r2,r3,#0x0    @ 080cdb40 1a1c
    lsls r1,r3,#0x1c    @ 080cdb42 1907
    lsrs r1,r1,#0x1c    @ 080cdb44 090f
    adds r0,r5,#0x0    @ 080cdb46 281c
    asrs r0,r1    @ 080cdb48 0841
    ands r0,r6    @ 080cdb4a 3040
    cmp r0,#0x0                              @ 080cdb4c 0028
    beq LAB_080cdb32                         @ 080cdb4e f0d0
    .hword 0x4642    @ 080cdb50 4246
    strb r3,[r2,#0x0]                        @ 080cdb52 1370
LAB_080cdb54:
    adds r4,#0x10    @ 080cdb54 1034
    adds r0,r4,#0x0    @ 080cdb56 201c
    cmp r4,#0x0                              @ 080cdb58 002c
    bge LAB_080cdb5e                         @ 080cdb5a 00da
    adds r0,r4,#0x7    @ 080cdb5c e01d
LAB_080cdb5e:
    asrs r6,r0,#0x3    @ 080cdb5e c610
    movs r0,#0x7    @ 080cdb60 0720
    ands r0,r4    @ 080cdb62 2040
    cmp r0,#0x0                              @ 080cdb64 0028
    beq LAB_080cdb6a                         @ 080cdb66 00d0
    adds r6,#0x1    @ 080cdb68 0136
LAB_080cdb6a:
    ldr r0, DAT_080cdba0                     @ 080cdb6a 0d48
    add r0,r9                                @ 080cdb6c 4844
    strb r6,[r0,#0x0]                        @ 080cdb6e 0670
LAB_080cdb70:
    add sp,#0x4                              @ 080cdb70 01b0
    pop {r3,r4}                              @ 080cdb72 18bc
    .hword 0x4698    @ 080cdb74 9846
    .hword 0x46a1    @ 080cdb76 a146
    pop {r4,r5,r6,r7}                        @ 080cdb78 f0bc
    pop {r0}                                 @ 080cdb7a 01bc
    bx r0                                    @ 080cdb7c 0047
    .zero  0x2
DAT_080cdb80:
    .word  0x02006ed0                     @ 080cdb80 d06e0002
DAT_080cdb84:
    .word  0x02000000                     @ 080cdb84 00000002
DAT_080cdb88:
    .word  0x00006c2c                     @ 080cdb88 2c6c0000
PTR_font_jp_base_table_080cdb8c:
    .word  font_jp_base_table             @ 080cdb8c 54f8e509
DAT_080cdb90:
    .word  0x0201f441                     @ 080cdb90 41f40102
DAT_080cdb94:
    .word  0x06014000                     @ 080cdb94 00400106
DAT_080cdb98:
    .word  0x00000a16                     @ 080cdb98 160a0000
DAT_080cdb9c:
    .word  0x00000a17                     @ 080cdb9c 170a0000
DAT_080cdba0:
    .word  0x00000a03                     @ 080cdba0 030a0000
DAT_080cdba4:
    .word  0x00000a0d                     @ 080cdba4 0d0a0000

@ Card-list OAM row render branch for dual_slot variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 4. Uses two __divsi3 calls (divisor=0xc8=200) to convert gFontState[0x0201fe4e] halfword bits[23:16] into x_div/y_div coordinates. OAM Y base = y_coord+0x1c. Reads gFontState[0x0a1b] bits[1:0] slot_state. slot_state<=1: extracts gPrng[0x148] bit4 flip_bit; calls write_oam_entry_from_packed_args (slot=0x60) and write_oam_entry_with_slot_check (attr2=0x1000/0x2000/0x3000) for 3 OAM entries. slot_state>1: extended path with up to 6 extra OAM entries. No APCS inputs; gFontState base loaded internally via r10. Sibling of render_card_list_oam_row_by_single_slot (divisor=0xb8, Y+0x2a). Constants: CARD_REG_OFFSET=0x0201fe4e; DIVISOR=0xc8; OAM_Y_BASE=+0x1c; SLOT_STATE_OFFSET=0x0a1b; OAM_SLOT=0x60; FLIP_BIT=bit4 of gPrng[0x148]; ATTR2_A=0x1000; ATTR2_B=0x2000; ATTR2_C=0x3000.
render_card_list_oam_row_by_dual_slot:
    push {r4,r5,r6,r7,lr}                    @ 080cdba8 f0b5
    .hword 0x4657    @ 080cdbaa 5746
    .hword 0x464e    @ 080cdbac 4e46
    .hword 0x4645    @ 080cdbae 4546
    push {r5,r6,r7}                          @ 080cdbb0 e0b4
    sub sp,#0x4                              @ 080cdbb2 81b0
    ldr r0, DAT_080cdd50                     @ 080cdbb4 6648
    .hword 0x4682    @ 080cdbb6 8246
    ldr r1, DAT_080cdd54                     @ 080cdbb8 6649
    ldrh r1,[r1,#0x0]                        @ 080cdbba 0988
    lsls r4,r1,#0x14    @ 080cdbbc 0c05
    lsrs r1,r4,#0x18    @ 080cdbbe 210e
    lsls r1,r1,#0x1    @ 080cdbc0 4900
    movs r0,#0xc8    @ 080cdbc2 c820
    bl __divsi3                              @ 080cdbc4 40f01efd
    adds r7,r0,#0x0    @ 080cdbc8 071c
    adds r7,#0x1c    @ 080cdbca 1c37
    ldr r0, DAT_080cdd58                     @ 080cdbcc 6248
    add r0,r10                               @ 080cdbce 5044
    ldrb r0,[r0,#0x0]                        @ 080cdbd0 0078
    lsrs r1,r0,#0x1    @ 080cdbd2 4108
    movs r0,#0xa    @ 080cdbd4 0a20
    subs r0,r0,r1    @ 080cdbd6 401a
    lsls r0,r0,#0x3    @ 080cdbd8 c000
    ldr r1, DAT_080cdd5c                     @ 080cdbda 6049
    add r1,r10                               @ 080cdbdc 5144
    ldrh r1,[r1,#0x0]                        @ 080cdbde 0988
    adds r1,r1,r0    @ 080cdbe0 0918
    str r1,[sp,#0x0]                         @ 080cdbe2 0091
    lsrs r4,r4,#0x18    @ 080cdbe4 240e
    movs r0,#0xc8    @ 080cdbe6 c820
    adds r1,r4,#0x0    @ 080cdbe8 211c
    bl __divsi3                              @ 080cdbea 40f00bfd
    .hword 0x4681    @ 080cdbee 8146
    ldr r0, DAT_080cdd60                     @ 080cdbf0 5b48
    add r0,r10                               @ 080cdbf2 5044
    ldrb r0,[r0,#0x0]                        @ 080cdbf4 0078
    lsrs r0,r0,#0x1    @ 080cdbf6 4008
    movs r1,#0x3    @ 080cdbf8 0321
    ands r0,r1    @ 080cdbfa 0840
    cmp r0,#0x1                              @ 080cdbfc 0128
    bhi LAB_080cdc8e                         @ 080cdbfe 46d8
    ldr r0, PTR_gPrng_080cdd64               @ 080cdc00 5848
    movs r2,#0x83    @ 080cdc02 8322
    lsls r2,r2,#0x2    @ 080cdc04 9200
    adds r0,r0,r2    @ 080cdc06 8018
    ldrh r0,[r0,#0x0]                        @ 080cdc08 0088
    lsrs r5,r0,#0x4    @ 080cdc0a 0509
    movs r0,#0x1    @ 080cdc0c 0120
    ands r5,r0    @ 080cdc0e 0540
    ldr r0, DAT_080cdd68                     @ 080cdc10 5548
    add r0,r10                               @ 080cdc12 5044
    .hword 0x4680    @ 080cdc14 8046
    adds r1,r0,#0x0    @ 080cdc16 011c
    ldrh r1,[r1,#0x0]                        @ 080cdc18 0988
    .hword 0x4648    @ 080cdc1a 4846
    muls r0,r1    @ 080cdc1c 4843
    adds r0,r7,r0    @ 080cdc1e 3818
    subs r6,r5,#0x4    @ 080cdc20 2e1f
    adds r0,r0,r6    @ 080cdc22 8019
    ldr r2,[sp,#0x0]                         @ 080cdc24 009a
    adds r4,r2,r6    @ 080cdc26 9419
    lsls r4,r4,#0x10    @ 080cdc28 2404
    orrs r0,r4    @ 080cdc2a 2043
    movs r1,#0x0    @ 080cdc2c 0021
    movs r2,#0x60    @ 080cdc2e 6022
    bl write_oam_entry_from_packed_args      @ 080cdc30 28f09cfa
    .hword 0x4641    @ 080cdc34 4146
    ldrh r1,[r1,#0x0]                        @ 080cdc36 0988
    .hword 0x4648    @ 080cdc38 4846
    muls r0,r1    @ 080cdc3a 4843
    adds r0,#0x10    @ 080cdc3c 1030
    adds r0,r7,r0    @ 080cdc3e 3818
    subs r0,r0,r6    @ 080cdc40 801b
    orrs r0,r4    @ 080cdc42 2043
    movs r3,#0x80    @ 080cdc44 8023
    lsls r3,r3,#0x5    @ 080cdc46 5b01
    movs r1,#0x0    @ 080cdc48 0021
    movs r2,#0x60    @ 080cdc4a 6022
    bl write_oam_entry_with_slot_check       @ 080cdc4c 28f0d2fd
    .hword 0x4642    @ 080cdc50 4246
    ldrh r2,[r2,#0x0]                        @ 080cdc52 1288
    .hword 0x4648    @ 080cdc54 4846
    muls r0,r2    @ 080cdc56 5043
    adds r0,r7,r0    @ 080cdc58 3818
    adds r0,r0,r6    @ 080cdc5a 8019
    subs r5,#0x14    @ 080cdc5c 143d
    ldr r1,[sp,#0x0]                         @ 080cdc5e 0099
    subs r5,r1,r5    @ 080cdc60 4d1b
    lsls r5,r5,#0x10    @ 080cdc62 2d04
    orrs r0,r5    @ 080cdc64 2843
    movs r3,#0x80    @ 080cdc66 8023
    lsls r3,r3,#0x6    @ 080cdc68 9b01
    movs r1,#0x0    @ 080cdc6a 0021
    movs r2,#0x60    @ 080cdc6c 6022
    bl write_oam_entry_with_slot_check       @ 080cdc6e 28f0c1fd
    .hword 0x4642    @ 080cdc72 4246
    ldrh r2,[r2,#0x0]                        @ 080cdc74 1288
    .hword 0x4648    @ 080cdc76 4846
    muls r0,r2    @ 080cdc78 5043
    adds r0,#0x10    @ 080cdc7a 1030
    adds r0,r7,r0    @ 080cdc7c 3818
    subs r0,r0,r6    @ 080cdc7e 801b
    orrs r0,r5    @ 080cdc80 2843
    movs r3,#0xc0    @ 080cdc82 c023
    lsls r3,r3,#0x6    @ 080cdc84 9b01
    movs r1,#0x0    @ 080cdc86 0021
    movs r2,#0x60    @ 080cdc88 6022
    bl write_oam_entry_with_slot_check       @ 080cdc8a 28f0b3fd
LAB_080cdc8e:
    movs r0,#0x0    @ 080cdc8e 0020
    .hword 0x4680    @ 080cdc90 8046
    ldr r1,[sp,#0x0]                         @ 080cdc92 0099
    lsls r1,r1,#0x10    @ 080cdc94 0904
    .hword 0x468a    @ 080cdc96 8a46
    movs r2,#0xc0    @ 080cdc98 c022
    lsls r2,r2,#0x7    @ 080cdc9a d201
    adds r5,r2,#0x0    @ 080cdc9c 151c
    ldr r0,[sp,#0x0]                         @ 080cdc9e 0098
    adds r0,#0x10    @ 080cdca0 1030
    lsls r0,r0,#0x10    @ 080cdca2 0004
    .hword 0x4681    @ 080cdca4 8146
    movs r6,#0x0    @ 080cdca6 0026
LAB_080cdca8:
    ldr r1, DAT_080cdd50                     @ 080cdca8 2949
    ldr r2, DAT_080cdd6c                     @ 080cdcaa 304a
    adds r0,r1,r2    @ 080cdcac 8818
    ldrb r0,[r0,#0x0]                        @ 080cdcae 0078
    .hword 0x4641    @ 080cdcb0 4146
    asrs r0,r1    @ 080cdcb2 0841
    movs r1,#0x1    @ 080cdcb4 0121
    ands r0,r1    @ 080cdcb6 0840
    cmp r0,#0x0                              @ 080cdcb8 0028
    beq LAB_080cdd34                         @ 080cdcba 3bd0
    adds r0,r7,#0x0    @ 080cdcbc 381c
    .hword 0x4652    @ 080cdcbe 5246
    orrs r0,r2    @ 080cdcc0 1043
    movs r1,#0xc0    @ 080cdcc2 c021
    lsls r1,r1,#0x1    @ 080cdcc4 4900
    adds r2,r6,r1    @ 080cdcc6 7218
    orrs r2,r5    @ 080cdcc8 2a43
    lsls r2,r2,#0x10    @ 080cdcca 1204
    lsrs r2,r2,#0x10    @ 080cdccc 120c
    movs r1,#0x40    @ 080cdcce 4021
    bl write_oam_entry_from_packed_args      @ 080cdcd0 28f04cfa
    adds r4,r7,#0x0    @ 080cdcd4 3c1c
    adds r4,#0x10    @ 080cdcd6 1034
    adds r0,r4,#0x0    @ 080cdcd8 201c
    .hword 0x4652    @ 080cdcda 5246
    orrs r0,r2    @ 080cdcdc 1043
    movs r1,#0xc1    @ 080cdcde c121
    lsls r1,r1,#0x1    @ 080cdce0 4900
    adds r2,r6,r1    @ 080cdce2 7218
    orrs r2,r5    @ 080cdce4 2a43
    lsls r2,r2,#0x10    @ 080cdce6 1204
    lsrs r2,r2,#0x10    @ 080cdce8 120c
    movs r1,#0x80    @ 080cdcea 8021
    lsls r1,r1,#0x8    @ 080cdcec 0902
    bl write_oam_entry_from_packed_args      @ 080cdcee 28f03dfa
    adds r0,r7,#0x0    @ 080cdcf2 381c
    .hword 0x464a    @ 080cdcf4 4a46
    orrs r0,r2    @ 080cdcf6 1043
    movs r1,#0xe0    @ 080cdcf8 e021
    lsls r1,r1,#0x1    @ 080cdcfa 4900
    adds r2,r6,r1    @ 080cdcfc 7218
    orrs r2,r5    @ 080cdcfe 2a43
    lsls r2,r2,#0x10    @ 080cdd00 1204
    lsrs r2,r2,#0x10    @ 080cdd02 120c
    movs r1,#0x80    @ 080cdd04 8021
    lsls r1,r1,#0x7    @ 080cdd06 c901
    bl write_oam_entry_from_packed_args      @ 080cdd08 28f030fa
    .hword 0x464a    @ 080cdd0c 4a46
    orrs r4,r2    @ 080cdd0e 1443
    movs r0,#0xe1    @ 080cdd10 e120
    lsls r0,r0,#0x1    @ 080cdd12 4000
    adds r2,r6,r0    @ 080cdd14 3218
    orrs r2,r5    @ 080cdd16 2a43
    lsls r2,r2,#0x10    @ 080cdd18 1204
    lsrs r2,r2,#0x10    @ 080cdd1a 120c
    adds r0,r4,#0x0    @ 080cdd1c 201c
    movs r1,#0x0    @ 080cdd1e 0021
    bl write_oam_entry_from_packed_args      @ 080cdd20 28f024fa
    ldr r2, DAT_080cdd54                     @ 080cdd24 0b4a
    ldrh r2,[r2,#0x0]                        @ 080cdd26 1288
    lsls r1,r2,#0x14    @ 080cdd28 1105
    lsrs r1,r1,#0x18    @ 080cdd2a 090e
    movs r0,#0xc8    @ 080cdd2c c820
    bl __divsi3                              @ 080cdd2e 40f069fc
    adds r7,r7,r0    @ 080cdd32 3f18
LAB_080cdd34:
    adds r6,#0x3    @ 080cdd34 0336
    movs r0,#0x1    @ 080cdd36 0120
    add r8,r0                                @ 080cdd38 8044
    .hword 0x4641    @ 080cdd3a 4146
    cmp r1,#0x5                              @ 080cdd3c 0529
    ble LAB_080cdca8                         @ 080cdd3e b3dd
    add sp,#0x4                              @ 080cdd40 01b0
    pop {r3,r4,r5}                           @ 080cdd42 38bc
    .hword 0x4698    @ 080cdd44 9846
    .hword 0x46a1    @ 080cdd46 a146
    .hword 0x46aa    @ 080cdd48 aa46
    pop {r4,r5,r6,r7}                        @ 080cdd4a f0bc
    pop {r0}                                 @ 080cdd4c 01bc
    bx r0                                    @ 080cdd4e 0047
DAT_080cdd50:
    .word  0x0201f440                     @ 080cdd50 40f40102
DAT_080cdd54:
    .word  0x0201fe4e                     @ 080cdd54 4efe0102
DAT_080cdd58:
    .word  0x00000a03                     @ 080cdd58 030a0000
DAT_080cdd5c:
    .word  0x00000a04                     @ 080cdd5c 040a0000
DAT_080cdd60:
    .word  0x00000a1b                     @ 080cdd60 1b0a0000
PTR_gPrng_080cdd64:
    .word  gPrng                          @ 080cdd64 40000003
DAT_080cdd68:
    .word  0x00000a14                     @ 080cdd68 140a0000
DAT_080cdd6c:
    .word  0x00000a02                     @ 080cdd6c 020a0000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. state=0: reads gPrng+0x148; bit5=0x20: nibble-decrement on gFontState+0x0a0e (mod 16), on hit writes gFontState+0x0a14 halfword-1, sync_state_and_init_sprite(0); bit4=0x10: nibble-increment, writes halfword+1; bit0=0x1: writes gFontState+0x0a0e bits[3:0] (nibble) to gP1LifePoints+0x3d40, increments gFontState+0x0a18 bits[9:16], sync_state_and_init_sprite(0x24); bit1=0x2: compares gP1LifePoints+0x1cf4 word, on match sync_state_and_init_sprite(1) returns 1, else sync_state_and_init_sprite(2). state=1: nibble increment on 0x0a1b/0x0a1c, may also increment 0x0a18 bits[23:16]. state>=2: returns 0. Constants: OAM_SLOT=0x30; NIBBLE_OFFSET=0x0a0e; LP_FIELD=0x0a02; LP_ADDR=gP1LifePoints+0x3d40; CMP_ADDR=gP1LifePoints+0x1cf4.
render_card_list_oam_row_by_lp_nibble:
    push {r4,r5,r6,r7,lr}                    @ 080cdd70 f0b5
    .hword 0x4647    @ 080cdd72 4746
    push {r7}                                @ 080cdd74 80b4
    ldr r4, DAT_080cdda8                     @ 080cdd76 0c4c
    ldr r1, DAT_080cddac                     @ 080cdd78 0c49
    adds r0,r4,r1    @ 080cdd7a 6018
    ldrb r3,[r0,#0x0]                        @ 080cdd7c 0378
    lsrs r0,r3,#0x1    @ 080cdd7e 5808
    movs r1,#0xa    @ 080cdd80 0a21
    subs r1,r1,r0    @ 080cdd82 091a
    lsls r1,r1,#0x3    @ 080cdd84 c900
    movs r2,#0xfe    @ 080cdd86 fe22
    lsls r2,r2,#0x1    @ 080cdd88 5200
    movs r0,#0x30    @ 080cdd8a 3020
    bl write_card_list_oam_row_strip         @ 080cdd8c f9f7d0fb
    ldr r2, DAT_080cddb0                     @ 080cdd90 074a
    adds r6,r4,r2    @ 080cdd92 a618
    ldr r3,[r6,#0x0]                         @ 080cdd94 3368
    lsls r2,r3,#0xf    @ 080cdd96 da03
    lsrs r7,r2,#0x18    @ 080cdd98 170e
    cmp r7,#0x0                              @ 080cdd9a 002f
    beq LAB_080cddb4                         @ 080cdd9c 0ad0
    cmp r7,#0x1                              @ 080cdd9e 012f
    bne LAB_080cdda4                         @ 080cdda0 00d1
    b LAB_080cdf10                           @ 080cdda2 b5e0
LAB_080cdda4:
    b LAB_080cdf60                           @ 080cdda4 dce0
    .zero  0x2
DAT_080cdda8:
    .word  0x0201f440                     @ 080cdda8 40f40102
DAT_080cddac:
    .word  0x00000a03                     @ 080cddac 030a0000
DAT_080cddb0:
    .word  0x00000a18                     @ 080cddb0 180a0000
LAB_080cddb4:
    ldr r0, PTR_gPrng_080cde18               @ 080cddb4 1848
    movs r5,#0xa4    @ 080cddb6 a425
    lsls r5,r5,#0x1    @ 080cddb8 6d00
    adds r0,r0,r5    @ 080cddba 4019
    ldrh r1,[r0,#0x0]                        @ 080cddbc 0188
    movs r0,#0x20    @ 080cddbe 2020
    ands r0,r1    @ 080cddc0 0840
    cmp r0,#0x0                              @ 080cddc2 0028
    beq LAB_080cde28                         @ 080cddc4 30d0
    ldr r1, DAT_080cde1c                     @ 080cddc6 1549
    adds r0,r4,r1    @ 080cddc8 6018
    ldrb r5,[r0,#0x0]                        @ 080cddca 0578
    ldr r2, DAT_080cde20                     @ 080cddcc 144a
    adds r3,r4,r2    @ 080cddce a318
    movs r6,#0xf    @ 080cddd0 0f26
    movs r7,#0x10    @ 080cddd2 1027
    rsbs r7,r7,#0    @ 080cddd4 7f42
LAB_080cddd6:
    ldrb r2,[r3,#0x0]                        @ 080cddd6 1a78
    lsls r1,r2,#0x1c    @ 080cddd8 1107
    lsrs r1,r1,#0x1c    @ 080cddda 090f
    subs r1,#0x1    @ 080cdddc 0139
    ands r1,r6    @ 080cddde 3140
    adds r0,r7,#0x0    @ 080cdde0 381c
    ands r0,r2    @ 080cdde2 1040
    orrs r0,r1    @ 080cdde4 0843
    strb r0,[r3,#0x0]                        @ 080cdde6 1870
    adds r0,r5,#0x0    @ 080cdde8 281c
    asrs r0,r1    @ 080cddea 0841
    movs r1,#0x1    @ 080cddec 0121
    ands r0,r1    @ 080cddee 0840
    cmp r0,#0x0                              @ 080cddf0 0028
    beq LAB_080cddd6                         @ 080cddf2 f0d0
    ldr r3, DAT_080cde24                     @ 080cddf4 0b4b
    adds r1,r4,r3    @ 080cddf6 e118
    ldrh r0,[r1,#0x0]                        @ 080cddf8 0888
    cmp r0,#0x0                              @ 080cddfa 0028
    bne LAB_080cde0a                         @ 080cddfc 05d1
    ldr r5, DAT_080cde20                     @ 080cddfe 084d
    adds r0,r4,r5    @ 080cde00 6019
    ldrh r2,[r0,#0x0]                        @ 080cde02 0288
    lsrs r0,r2,#0x4    @ 080cde04 1009
    lsls r0,r0,#0x18    @ 080cde06 0006
    lsrs r0,r0,#0x18    @ 080cde08 000e
LAB_080cde0a:
    subs r0,#0x1    @ 080cde0a 0138
LAB_080cde0c:
    strh r0,[r1,#0x0]                        @ 080cde0c 0880
    movs r0,#0x0    @ 080cde0e 0020
    bl sync_state_and_init_sprite            @ 080cde10 2bf050fe
    b LAB_080cdf60                           @ 080cde14 a4e0
    .zero  0x2
PTR_gPrng_080cde18:
    .word  gPrng                          @ 080cde18 40000003
DAT_080cde1c:
    .word  0x00000a02                     @ 080cde1c 020a0000
DAT_080cde20:
    .word  0x00000a0e                     @ 080cde20 0e0a0000
DAT_080cde24:
    .word  0x00000a14                     @ 080cde24 140a0000
LAB_080cde28:
    movs r0,#0x10    @ 080cde28 1020
    ands r0,r1    @ 080cde2a 0840
    cmp r0,#0x0                              @ 080cde2c 0028
    beq LAB_080cde88                         @ 080cde2e 2bd0
    ldr r3, DAT_080cde78                     @ 080cde30 114b
    adds r0,r4,r3    @ 080cde32 e018
    ldrb r5,[r0,#0x0]                        @ 080cde34 0578
    ldr r0, DAT_080cde7c                     @ 080cde36 1148
    adds r3,r4,r0    @ 080cde38 2318
    movs r6,#0xf    @ 080cde3a 0f26
    movs r7,#0x10    @ 080cde3c 1027
    rsbs r7,r7,#0    @ 080cde3e 7f42
LAB_080cde40:
    ldrb r2,[r3,#0x0]                        @ 080cde40 1a78
    lsls r1,r2,#0x1c    @ 080cde42 1107
    lsrs r1,r1,#0x1c    @ 080cde44 090f
    adds r1,#0x1    @ 080cde46 0131
    ands r1,r6    @ 080cde48 3140
    adds r0,r7,#0x0    @ 080cde4a 381c
    ands r0,r2    @ 080cde4c 1040
    orrs r0,r1    @ 080cde4e 0843
    strb r0,[r3,#0x0]                        @ 080cde50 1870
    adds r0,r5,#0x0    @ 080cde52 281c
    asrs r0,r1    @ 080cde54 0841
    movs r1,#0x1    @ 080cde56 0121
    ands r0,r1    @ 080cde58 0840
    cmp r0,#0x0                              @ 080cde5a 0028
    beq LAB_080cde40                         @ 080cde5c f0d0
    ldr r2, DAT_080cde80                     @ 080cde5e 084a
    adds r1,r4,r2    @ 080cde60 a118
    ldrh r2,[r1,#0x0]                        @ 080cde62 0a88
    ldr r3, DAT_080cde7c                     @ 080cde64 054b
    adds r0,r4,r3    @ 080cde66 e018
    ldrh r0,[r0,#0x0]                        @ 080cde68 0088
    lsls r0,r0,#0x14    @ 080cde6a 0005
    lsrs r0,r0,#0x18    @ 080cde6c 000e
    subs r0,#0x1    @ 080cde6e 0138
    cmp r2,r0                                @ 080cde70 8242
    bne LAB_080cde84                         @ 080cde72 07d1
    movs r0,#0x0    @ 080cde74 0020
    b LAB_080cde0c                           @ 080cde76 c9e7
DAT_080cde78:
    .word  0x00000a02                     @ 080cde78 020a0000
DAT_080cde7c:
    .word  0x00000a0e                     @ 080cde7c 0e0a0000
DAT_080cde80:
    .word  0x00000a14                     @ 080cde80 140a0000
LAB_080cde84:
    adds r0,r2,#0x1    @ 080cde84 501c
    b LAB_080cde0c                           @ 080cde86 c1e7
LAB_080cde88:
    movs r5,#0x1    @ 080cde88 0125
    adds r0,r5,#0x0    @ 080cde8a 281c
    ands r0,r1    @ 080cde8c 0840
    cmp r0,#0x0                              @ 080cde8e 0028
    beq LAB_080cdecc                         @ 080cde90 1cd0
    ldr r1, PTR_gP1LifePoints_080cdec0       @ 080cde92 0b49
    movs r5,#0xea    @ 080cde94 ea25
    lsls r5,r5,#0x5    @ 080cde96 6d01
    adds r1,r1,r5    @ 080cde98 4919
    ldr r5, DAT_080cdec4                     @ 080cde9a 0a4d
    adds r0,r4,r5    @ 080cde9c 6019
    ldrb r0,[r0,#0x0]                        @ 080cde9e 0078
    lsls r0,r0,#0x1c    @ 080cdea0 0007
    lsrs r0,r0,#0x1c    @ 080cdea2 000f
    str r0,[r1,#0x0]                         @ 080cdea4 0860
    lsrs r1,r2,#0x18    @ 080cdea6 110e
    adds r1,#0x1    @ 080cdea8 0131
    movs r0,#0xff    @ 080cdeaa ff20
    ands r1,r0    @ 080cdeac 0140
    lsls r1,r1,#0x9    @ 080cdeae 4902
    ldr r0, DAT_080cdec8                     @ 080cdeb0 0548
    ands r0,r3    @ 080cdeb2 1840
    orrs r0,r1    @ 080cdeb4 0843
    str r0,[r6,#0x0]                         @ 080cdeb6 3060
    movs r0,#0x24    @ 080cdeb8 2420
    bl sync_state_and_init_sprite            @ 080cdeba 2bf0fbfd
    b LAB_080cdf60                           @ 080cdebe 4fe0
PTR_gP1LifePoints_080cdec0:
    .word  gP1LifePoints                  @ 080cdec0 e0c40102
DAT_080cdec4:
    .word  0x00000a0e                     @ 080cdec4 0e0a0000
DAT_080cdec8:
    .word  0xfffe01ff                     @ 080cdec8 ff01feff
LAB_080cdecc:
    movs r0,#0x2    @ 080cdecc 0220
    ands r0,r1    @ 080cdece 0840
    cmp r0,#0x0                              @ 080cded0 0028
    beq LAB_080cdf60                         @ 080cded2 45d0
    ldr r0, DAT_080cdefc                     @ 080cded4 0948
    adds r1,r4,r0    @ 080cded6 2118
    ldr r3, PTR_gP1LifePoints_080cdf00       @ 080cded8 094b
    ldr r2, DAT_080cdf04                     @ 080cdeda 0a4a
    adds r0,r3,r2    @ 080cdedc 9818
    ldr r2,[r0,#0x0]                         @ 080cdede 0268
    ldrb r0,[r1,#0x0]                        @ 080cdee0 0878
    asrs r0,r2    @ 080cdee2 1041
    ands r0,r5    @ 080cdee4 2840
    cmp r0,#0x0                              @ 080cdee6 0028
    beq LAB_080cdf08                         @ 080cdee8 0ed0
    movs r5,#0xea    @ 080cdeea ea25
    lsls r5,r5,#0x5    @ 080cdeec 6d01
    adds r0,r3,r5    @ 080cdeee 5819
    str r2,[r0,#0x0]                         @ 080cdef0 0260
    movs r0,#0x1    @ 080cdef2 0120
    bl sync_state_and_init_sprite            @ 080cdef4 2bf0defd
    movs r0,#0x1    @ 080cdef8 0120
    b LAB_080cdf62                           @ 080cdefa 32e0
DAT_080cdefc:
    .word  0x00000a02                     @ 080cdefc 020a0000
PTR_gP1LifePoints_080cdf00:
    .word  gP1LifePoints                  @ 080cdf00 e0c40102
DAT_080cdf04:
    .word  0x00001cf4                     @ 080cdf04 f41c0000
LAB_080cdf08:
    movs r0,#0x2    @ 080cdf08 0220
    bl sync_state_and_init_sprite            @ 080cdf0a 2bf0d3fd
    b LAB_080cdf60                           @ 080cdf0e 27e0
LAB_080cdf10:
    ldr r0, DAT_080cdf58                     @ 080cdf10 1148
    adds r0,r0,r4    @ 080cdf12 0019
    .hword 0x4680    @ 080cdf14 8046
    ldrb r6,[r0,#0x0]                        @ 080cdf16 0678
    lsrs r0,r6,#0x1    @ 080cdf18 7008
    ldr r1, DAT_080cdf5c                     @ 080cdf1a 1049
    adds r4,r4,r1    @ 080cdf1c 6418
    adds r3,r7,#0x0    @ 080cdf1e 3b1c
    ldrb r2,[r4,#0x0]                        @ 080cdf20 2278
    ands r3,r2    @ 080cdf22 1340
    lsls r3,r3,#0x7    @ 080cdf24 db01
    orrs r3,r0    @ 080cdf26 0343
    adds r2,r3,#0x1    @ 080cdf28 5a1c
    movs r1,#0x7f    @ 080cdf2a 7f21
    ands r1,r2    @ 080cdf2c 1140
    lsls r1,r1,#0x1    @ 080cdf2e 4900
    movs r5,#0x1    @ 080cdf30 0125
    adds r0,r7,#0x0    @ 080cdf32 381c
    ands r0,r6    @ 080cdf34 3040
    orrs r0,r1    @ 080cdf36 0843
    .hword 0x4641    @ 080cdf38 4146
    strb r0,[r1,#0x0]                        @ 080cdf3a 0870
    lsrs r2,r2,#0x7    @ 080cdf3c d209
    ands r2,r7    @ 080cdf3e 3a40
    ands r2,r5    @ 080cdf40 2a40
    movs r0,#0x2    @ 080cdf42 0220
    rsbs r0,r0,#0    @ 080cdf44 4042
    ldrb r5,[r4,#0x0]                        @ 080cdf46 2578
    ands r0,r5    @ 080cdf48 2840
    orrs r0,r2    @ 080cdf4a 1043
    strb r0,[r4,#0x0]                        @ 080cdf4c 2070
    cmp r3,#0x1f                             @ 080cdf4e 1f2b
    bls LAB_080cdf60                         @ 080cdf50 06d9
    movs r0,#0x1    @ 080cdf52 0120
    b LAB_080cdf62                           @ 080cdf54 05e0
    .zero  0x2
DAT_080cdf58:
    .word  0x00000a1b                     @ 080cdf58 1b0a0000
DAT_080cdf5c:
    .word  0x00000a1c                     @ 080cdf5c 1c0a0000
LAB_080cdf60:
    movs r0,#0x0    @ 080cdf60 0020
LAB_080cdf62:
    pop {r3}                                 @ 080cdf62 08bc
    .hword 0x4698    @ 080cdf64 9846
    pop {r4,r5,r6,r7}                        @ 080cdf66 f0bc
    pop {r1}                                 @ 080cdf68 02bc
    bx r1                                    @ 080cdf6a 0847

@ indeg=1, caller: FUN_080ce428 (card list OAM row by slot advance). Searches card main slot list (gFontState+0x0a06 halfword array) for next occupied slot. r0=current_slot_id [0..5] (saved to r8 as loop sentinel). Loop: increments slot_id modulo 6 via __modsi3; checks gFontState+0x0a10 flag word bit corresponding to slot; if set (occupied), scans gFontState+0x0a06 halfword list to confirm slot_id not already present. Returns r0=next occupied slot_id [0..5]. Pure read: no VRAM/OAM side-effects. Constants: SLOT_COUNT=6; FLAG_WORD_OFFSET=0x0a10; SLOT_LIST_OFFSET=0x0a06; SLOT_TABLE_OFFSET=0x0a0e.
find_next_occupied_slot_in_main_list:
    push {r4,r5,r6,r7,lr}                    @ 080cdf6c f0b5
    .hword 0x464f    @ 080cdf6e 4f46
    .hword 0x4646    @ 080cdf70 4646
    push {r6,r7}                             @ 080cdf72 c0b4
    adds r2,r0,#0x0    @ 080cdf74 021c
    .hword 0x4690    @ 080cdf76 9046
    ldr r5, DAT_080cdfe8                     @ 080cdf78 1b4d
    movs r1,#0xa1    @ 080cdf7a a121
    lsls r1,r1,#0x4    @ 080cdf7c 0901
    adds r0,r5,r1    @ 080cdf7e 6818
    ldr r7,[r0,#0x0]                         @ 080cdf80 0768
    ldr r3, DAT_080cdfec                     @ 080cdf82 1a4b
    adds r3,r3,r5    @ 080cdf84 5b19
    .hword 0x4699    @ 080cdf86 9946
    ldr r0, DAT_080cdff0                     @ 080cdf88 1948
    adds r6,r5,r0    @ 080cdf8a 2e18
LAB_080cdf8c:
    adds r2,#0x1    @ 080cdf8c 0132
    adds r0,r2,#0x0    @ 080cdf8e 101c
    movs r1,#0x6    @ 080cdf90 0621
    bl __modsi3                              @ 080cdf92 40f083fb
    adds r2,r0,#0x0    @ 080cdf96 021c
    movs r0,#0x1    @ 080cdf98 0120
    lsls r0,r2    @ 080cdf9a 9040
    ands r0,r7    @ 080cdf9c 3840
    cmp r0,#0x0                              @ 080cdf9e 0028
    beq LAB_080cdf8c                         @ 080cdfa0 f4d0
    movs r4,#0x0    @ 080cdfa2 0024
    ldrh r3,[r6,#0x0]                        @ 080cdfa4 3388
    lsls r1,r3,#0x14    @ 080cdfa6 1905
    lsrs r0,r1,#0x18    @ 080cdfa8 080e
    cmp r4,r0                                @ 080cdfaa 8442
    bge LAB_080cdfcc                         @ 080cdfac 0eda
    .hword 0x464b    @ 080cdfae 4b46
    ldrh r0,[r3,#0x0]                        @ 080cdfb0 1888
    cmp r0,r2                                @ 080cdfb2 9042
    beq LAB_080cdfcc                         @ 080cdfb4 0ad0
    adds r3,r1,#0x0    @ 080cdfb6 0b1c
    ldr r0, DAT_080cdfec                     @ 080cdfb8 0c48
    adds r1,r5,r0    @ 080cdfba 2918
LAB_080cdfbc:
    adds r1,#0x2    @ 080cdfbc 0231
    adds r4,#0x1    @ 080cdfbe 0134
    lsrs r0,r3,#0x18    @ 080cdfc0 180e
    cmp r4,r0                                @ 080cdfc2 8442
    bge LAB_080cdfcc                         @ 080cdfc4 02da
    ldrh r0,[r1,#0x0]                        @ 080cdfc6 0888
    cmp r0,r2                                @ 080cdfc8 9042
    bne LAB_080cdfbc                         @ 080cdfca f7d1
LAB_080cdfcc:
    ldrh r1,[r6,#0x0]                        @ 080cdfcc 3188
    lsls r0,r1,#0x14    @ 080cdfce 0805
    lsrs r0,r0,#0x18    @ 080cdfd0 000e
    cmp r4,r0                                @ 080cdfd2 8442
    beq LAB_080cdfda                         @ 080cdfd4 01d0
    cmp r2,r8                                @ 080cdfd6 4245
    bne LAB_080cdf8c                         @ 080cdfd8 d8d1
LAB_080cdfda:
    adds r0,r2,#0x0    @ 080cdfda 101c
    pop {r3,r4}                              @ 080cdfdc 18bc
    .hword 0x4698    @ 080cdfde 9846
    .hword 0x46a1    @ 080cdfe0 a146
    pop {r4,r5,r6,r7}                        @ 080cdfe2 f0bc
    pop {r1}                                 @ 080cdfe4 02bc
    bx r1                                    @ 080cdfe6 0847
DAT_080cdfe8:
    .word  0x0201f440                     @ 080cdfe8 40f40102
DAT_080cdfec:
    .word  0x00000a06                     @ 080cdfec 060a0000
DAT_080cdff0:
    .word  0x00000a0e                     @ 080cdff0 0e0a0000

@ indeg=1, caller: FUN_080ce428 (card list OAM row by slot advance). Symmetric to find_next_occupied_slot_in_main_list (0x080cdf6c) but operates on secondary slot table (gFontState+0x0a0e halfword table). r0=current_slot_id [0..5] (saved to r8 as sentinel). Loop: decrements slot_id via __modsi3(mod 6) in reverse; checks gFontState+0x0a10 flag word bit; on hit, scans gFontState+0x0a06 list to confirm non-duplicate. Returns r0=next occupied slot_id [0..5]. Pure read; no side-effects. Key difference from 0x080cdf6c: search table=+0x0a0e, compare list=+0x0a06 (roles swapped relative to main-list variant). Constants: SLOT_COUNT=6; FLAG_WORD_OFFSET=0x0a10; SEC_TABLE_OFFSET=0x0a0e; CMP_LIST_OFFSET=0x0a06.
find_next_occupied_slot_in_secondary_list:
    push {r4,r5,r6,r7,lr}                    @ 080cdff4 f0b5
    .hword 0x4647    @ 080cdff6 4746
    push {r7}                                @ 080cdff8 80b4
    adds r2,r0,#0x0    @ 080cdffa 021c
    .hword 0x4690    @ 080cdffc 9046
    ldr r6, DAT_080ce06c                     @ 080cdffe 1b4e
    ldr r0, DAT_080ce070                     @ 080ce000 1b48
    adds r7,r6,r0    @ 080ce002 3718
LAB_080ce004:
    movs r0,#0x5    @ 080ce004 0520
    cmp r2,#0x0                              @ 080ce006 002a
    beq LAB_080ce00c                         @ 080ce008 00d0
    subs r0,r2,#0x1    @ 080ce00a 501e
LAB_080ce00c:
    adds r2,r0,#0x0    @ 080ce00c 021c
    movs r1,#0x6    @ 080ce00e 0621
    bl __modsi3                              @ 080ce010 40f044fb
    adds r2,r0,#0x0    @ 080ce014 021c
    movs r1,#0xa1    @ 080ce016 a121
    lsls r1,r1,#0x4    @ 080ce018 0901
    adds r0,r6,r1    @ 080ce01a 7018
    movs r1,#0x1    @ 080ce01c 0121
    lsls r1,r2    @ 080ce01e 9140
    ldr r0,[r0,#0x0]                         @ 080ce020 0068
    ands r0,r1    @ 080ce022 0840
    cmp r0,#0x0                              @ 080ce024 0028
    beq LAB_080ce004                         @ 080ce026 edd0
    movs r5,#0x0    @ 080ce028 0025
    ldrh r0,[r7,#0x0]                        @ 080ce02a 3888
    lsls r1,r0,#0x14    @ 080ce02c 0105
    lsrs r0,r1,#0x18    @ 080ce02e 080e
    cmp r5,r0                                @ 080ce030 8542
    bge LAB_080ce052                         @ 080ce032 0eda
    ldr r0, DAT_080ce074                     @ 080ce034 0f48
    adds r3,r6,r0    @ 080ce036 3318
    ldrh r0,[r3,#0x0]                        @ 080ce038 1888
    cmp r0,r2                                @ 080ce03a 9042
    beq LAB_080ce052                         @ 080ce03c 09d0
    adds r4,r1,#0x0    @ 080ce03e 0c1c
    adds r1,r3,#0x0    @ 080ce040 191c
LAB_080ce042:
    adds r1,#0x2    @ 080ce042 0231
    adds r5,#0x1    @ 080ce044 0135
    lsrs r0,r4,#0x18    @ 080ce046 200e
    cmp r5,r0                                @ 080ce048 8542
    bge LAB_080ce052                         @ 080ce04a 02da
    ldrh r0,[r1,#0x0]                        @ 080ce04c 0888
    cmp r0,r2                                @ 080ce04e 9042
    bne LAB_080ce042                         @ 080ce050 f7d1
LAB_080ce052:
    ldrh r1,[r7,#0x0]                        @ 080ce052 3988
    lsls r0,r1,#0x14    @ 080ce054 0805
    lsrs r0,r0,#0x18    @ 080ce056 000e
    cmp r5,r0                                @ 080ce058 8542
    beq LAB_080ce060                         @ 080ce05a 01d0
    cmp r2,r8                                @ 080ce05c 4245
    bne LAB_080ce004                         @ 080ce05e d1d1
LAB_080ce060:
    adds r0,r2,#0x0    @ 080ce060 101c
    pop {r3}                                 @ 080ce062 08bc
    .hword 0x4698    @ 080ce064 9846
    pop {r4,r5,r6,r7}                        @ 080ce066 f0bc
    pop {r1}                                 @ 080ce068 02bc
    bx r1                                    @ 080ce06a 0847
DAT_080ce06c:
    .word  0x0201f440                     @ 080ce06c 40f40102
DAT_080ce070:
    .word  0x00000a0e                     @ 080ce070 0e0a0000
DAT_080ce074:
    .word  0x00000a06                     @ 080ce074 060a0000

@ indeg=2, callers: FUN_080c7950 (card_stats/font_jp) and FUN_080c7ea0 (display master). Initializes all VRAM/palette resources for card info display area and renders JP label. r0 packed: lo16=x_tile_col, hi16=y_tile_row, each [0..31]. Steps: (1) zero_fill_by_halfword BG tile VRAM 0x06014000 (0x4000 halfwords); (2) reads gFontState+0x0a17 JP flag bit0 and +0x0a18 flag, if both 0: copies gFontState+0x0a10 word; (3) copy_bytes_by_halfword palette A (ROM 0x09850c5c -> OBJ pal 0x05000260, 0x20 hw); (4) copy_bytes_by_halfword palette B (ROM 0x0984e30c -> OBJ pal 0x05000280, 0x20 hw); (5) tile_2d_row_copy 6 rows from ROM 0x0984de8c to BG VRAM 0x06013000; (6) tile_2d_row_copy 1 row to BG VRAM 0x06013800; (7) setup_line_buf_with_font_and_align(font=0x17, w=0x10, mode=1, align=2), game_str_id_to_row + game_str_pointer_table, text_render_wrapper, write_line_buf_to_bg_tile_vram JP label; (8) strb 0x6 to gFontState+0x0a15 (done flag). Constants: VRAM_BG=0x06014000; OBJ_PAL_A=0x05000260; OBJ_PAL_B=0x05000280; VRAM_TILE_A=0x06013000; VRAM_TILE_B=0x06013800; ROM_PAL_A=0x09850c5c; ROM_PAL_B=0x0984e30c; ROM_TILE=0x0984de8c; DONE_FLAG=6; FONT_ID=0x17.
init_card_info_display_with_jp_label:
    push {r4,r5,r6,lr}                       @ 080ce078 70b5
    lsrs r4,r0,#0x10    @ 080ce07a 040c
    lsls r0,r0,#0x10    @ 080ce07c 0004
    lsrs r6,r0,#0x10    @ 080ce07e 060c
    ldr r0, DAT_080ce1c4                     @ 080ce080 5048
    movs r1,#0x80    @ 080ce082 8021
    lsls r1,r1,#0x7    @ 080ce084 c901
    bl zero_fill_by_halfword                 @ 080ce086 26f0f5fe
    ldr r3, DAT_080ce1c8                     @ 080ce08a 4f4b
    ldr r1, DAT_080ce1cc                     @ 080ce08c 4f49
    adds r0,r3,r1    @ 080ce08e 5818
    ldrb r0,[r0,#0x0]                        @ 080ce090 0078
    lsrs r2,r0,#0x1    @ 080ce092 4208
    ldr r5, DAT_080ce1d0                     @ 080ce094 4e4d
    adds r1,r3,r5    @ 080ce096 5919
    movs r5,#0x1    @ 080ce098 0125
    adds r0,r5,#0x0    @ 080ce09a 281c
    ldrb r1,[r1,#0x0]                        @ 080ce09c 0978
    ands r0,r1    @ 080ce09e 0840
    lsls r0,r0,#0x7    @ 080ce0a0 c001
    orrs r0,r2    @ 080ce0a2 1043
    cmp r0,#0x0                              @ 080ce0a4 0028
    bne LAB_080ce0e0                         @ 080ce0a6 1bd1
    movs r1,#0xa1    @ 080ce0a8 a121
    lsls r1,r1,#0x4    @ 080ce0aa 0901
    adds r0,r3,r1    @ 080ce0ac 5818
    asrs r2,r4,#0x1    @ 080ce0ae 6210
    str r2,[r0,#0x0]                         @ 080ce0b0 0260
    ldr r0, DAT_080ce1d4                     @ 080ce0b2 4848
    adds r4,r3,r0    @ 080ce0b4 1c18
    adds r0,r5,#0x0    @ 080ce0b6 281c
    ldrh r1,[r4,#0x0]                        @ 080ce0b8 2188
    lsls r0,r1    @ 080ce0ba 8840
    ands r0,r2    @ 080ce0bc 1040
    adds r1,r3,#0x0    @ 080ce0be 191c
    cmp r0,#0x0                              @ 080ce0c0 0028
    bne LAB_080ce0da                         @ 080ce0c2 0ad1
    adds r3,r4,#0x0    @ 080ce0c4 231c
    movs r4,#0x1    @ 080ce0c6 0124
LAB_080ce0c8:
    ldrh r0,[r3,#0x0]                        @ 080ce0c8 1888
    adds r0,#0x1    @ 080ce0ca 0130
    strh r0,[r3,#0x0]                        @ 080ce0cc 1880
    adds r0,r4,#0x0    @ 080ce0ce 201c
    ldrh r5,[r3,#0x0]                        @ 080ce0d0 1d88
    lsls r0,r5    @ 080ce0d2 a840
    ands r0,r2    @ 080ce0d4 1040
    cmp r0,#0x0                              @ 080ce0d6 0028
    beq LAB_080ce0c8                         @ 080ce0d8 f6d0
LAB_080ce0da:
    ldr r2, DAT_080ce1d8                     @ 080ce0da 3f4a
    adds r0,r1,r2    @ 080ce0dc 8818
    strb r6,[r0,#0x0]                        @ 080ce0de 0670
LAB_080ce0e0:
    ldr r0, DAT_080ce1dc                     @ 080ce0e0 3e48
    ldr r1, DAT_080ce1e0                     @ 080ce0e2 3f49
    movs r2,#0x20    @ 080ce0e4 2022
    bl copy_bytes_by_halfword                @ 080ce0e6 26f0ddfe
    ldr r0, DAT_080ce1e4                     @ 080ce0ea 3e48
    ldr r1, DAT_080ce1c8                     @ 080ce0ec 3649
    ldr r3, DAT_080ce1d4                     @ 080ce0ee 394b
    adds r1,r1,r3    @ 080ce0f0 c918
    ldrh r1,[r1,#0x0]                        @ 080ce0f2 0988
    lsls r1,r1,#0x5    @ 080ce0f4 4901
    ldr r2, DAT_080ce1e8                     @ 080ce0f6 3c4a
    adds r1,r1,r2    @ 080ce0f8 8918
    movs r2,#0x20    @ 080ce0fa 2022
    bl copy_bytes_by_halfword                @ 080ce0fc 26f0d2fe
    movs r4,#0x0    @ 080ce100 0024
    ldr r5, DAT_080ce1ec                     @ 080ce102 3a4d
LAB_080ce104:
    lsls r1,r4,#0x7    @ 080ce104 e101
    ldr r0, DAT_080ce1f0                     @ 080ce106 3a48
    adds r1,r1,r0    @ 080ce108 0918
    adds r0,r5,#0x0    @ 080ce10a 281c
    movs r2,#0x2    @ 080ce10c 0222
    movs r3,#0x2    @ 080ce10e 0223
    bl tile_2d_row_copy                      @ 080ce110 29f0e0f9
    adds r5,#0x40    @ 080ce114 4035
    adds r4,#0x1    @ 080ce116 0134
    cmp r4,#0x5                              @ 080ce118 052c
    ble LAB_080ce104                         @ 080ce11a f3dd
    ldr r6, DAT_080ce1f4                     @ 080ce11c 354e
    adds r0,r6,#0x0    @ 080ce11e 301c
    movs r1,#0x0    @ 080ce120 0021
    movs r2,#0x17    @ 080ce122 1722
    movs r3,#0x2    @ 080ce124 0223
    bl tile_2d_row_copy                      @ 080ce126 29f0d5f9
    movs r0,#0x17    @ 080ce12a 1720
    movs r1,#0x2    @ 080ce12c 0221
    movs r2,#0x1    @ 080ce12e 0122
    movs r3,#0x0    @ 080ce130 0023
    bl setup_line_buf_with_font_and_align    @ 080ce132 22f0c5fd
    ldr r2, DAT_080ce1f8                     @ 080ce136 304a
    ldr r5, DAT_080ce1fc                     @ 080ce138 304d
    ldr r0, DAT_080ce200                     @ 080ce13a 3148
    adds r5,r5,r0    @ 080ce13c 2d18
    movs r1,#0x7    @ 080ce13e 0721
    ldrb r3,[r5,#0x0]                        @ 080ce140 2b78
    ands r1,r3    @ 080ce142 1940
    rsbs r1,r1,#0    @ 080ce144 4942
    lsrs r1,r1,#0x1f    @ 080ce146 c90f
    movs r0,#0x2    @ 080ce148 0220
    rsbs r0,r0,#0    @ 080ce14a 4042
    ldrb r3,[r2,#0x8]                        @ 080ce14c 137a
    ands r0,r3    @ 080ce14e 1840
    orrs r0,r1    @ 080ce150 0843
    movs r1,#0x2    @ 080ce152 0221
    orrs r0,r1    @ 080ce154 0843
    strb r0,[r2,#0x8]                        @ 080ce156 1072
    ldr r3, PTR_font_jp_base_table_080ce204  @ 080ce158 2a4b
    lsls r1,r0,#0x1e    @ 080ce15a 8107
    lsrs r1,r1,#0x1f    @ 080ce15c c90f
    lsls r1,r1,#0x2    @ 080ce15e 8900
    lsls r0,r0,#0x1f    @ 080ce160 c007
    lsrs r0,r0,#0x1f    @ 080ce162 c00f
    lsls r0,r0,#0x3    @ 080ce164 c000
    adds r1,r1,r0    @ 080ce166 0918
    adds r1,r1,r3    @ 080ce168 c918
    ldr r0,[r1,#0x0]                         @ 080ce16a 0868
    str r0,[r2,#0x4]                         @ 080ce16c 5060
    movs r0,#0x40    @ 080ce16e 4020
    ldrb r1,[r2,#0x15]                       @ 080ce170 517d
    orrs r0,r1    @ 080ce172 0843
    strb r0,[r2,#0x15]                       @ 080ce174 5075
    ldr r4, DAT_080ce1c8                     @ 080ce176 144c
    ldr r2, DAT_080ce1d4                     @ 080ce178 164a
    adds r0,r4,r2    @ 080ce17a a018
    ldrh r0,[r0,#0x0]                        @ 080ce17c 0088
    ldr r3, DAT_080ce208                     @ 080ce17e 224b
    adds r0,r0,r3    @ 080ce180 c018
    bl game_str_id_to_row                    @ 080ce182 26f049fe
    ldr r2, PTR_game_str_pointer_table_080ce20c @ 080ce186 214a
    lsls r0,r0,#0x10    @ 080ce188 0004
    lsrs r0,r0,#0x10    @ 080ce18a 000c
    lsls r1,r0,#0x1    @ 080ce18c 4100
    adds r1,r1,r0    @ 080ce18e 0918
    lsls r1,r1,#0x1    @ 080ce190 4900
    ldrb r5,[r5,#0x0]                        @ 080ce192 2d78
    lsls r0,r5,#0x1d    @ 080ce194 6807
    lsrs r0,r0,#0x1d    @ 080ce196 400f
    adds r1,r1,r0    @ 080ce198 0918
    lsls r1,r1,#0x2    @ 080ce19a 8900
    adds r1,r1,r2    @ 080ce19c 8918
    ldr r3,[r1,#0x0]                         @ 080ce19e 0b68
    ldr r0, PTR_game_str_ja_080ce210         @ 080ce1a0 1b48
    adds r3,r3,r0    @ 080ce1a2 1b18
    movs r0,#0x2    @ 080ce1a4 0220
    movs r1,#0x2    @ 080ce1a6 0221
    movs r2,#0x87    @ 080ce1a8 8722
    bl text_render_wrapper                   @ 080ce1aa 24f067fc
    adds r0,r6,#0x0    @ 080ce1ae 301c
    movs r1,#0x0    @ 080ce1b0 0021
    bl write_line_buf_to_bg_tile_vram        @ 080ce1b2 25f00ffb
    ldr r5, DAT_080ce214                     @ 080ce1b6 174d
    adds r4,r4,r5    @ 080ce1b8 6419
    movs r0,#0x6    @ 080ce1ba 0620
    strb r0,[r4,#0x0]                        @ 080ce1bc 2070
    pop {r4,r5,r6}                           @ 080ce1be 70bc
    pop {r0}                                 @ 080ce1c0 01bc
    bx r0                                    @ 080ce1c2 0047
DAT_080ce1c4:
    .word  0x06014000                     @ 080ce1c4 00400106
DAT_080ce1c8:
    .word  0x0201f440                     @ 080ce1c8 40f40102
DAT_080ce1cc:
    .word  0x00000a17                     @ 080ce1cc 170a0000
DAT_080ce1d0:
    .word  0x00000a18                     @ 080ce1d0 180a0000
DAT_080ce1d4:
    .word  0x00000a14                     @ 080ce1d4 140a0000
DAT_080ce1d8:
    .word  0x00000a02                     @ 080ce1d8 020a0000
DAT_080ce1dc:
    .word  0x05000260                     @ 080ce1dc 60020005
DAT_080ce1e0:
    .word  0x09850c5c                     @ 080ce1e0 5c0c8509
DAT_080ce1e4:
    .word  0x05000280                     @ 080ce1e4 80020005
DAT_080ce1e8:
    .word  0x0984e30c                     @ 080ce1e8 0ce38409
DAT_080ce1ec:
    .word  0x06013000                     @ 080ce1ec 00300106
DAT_080ce1f0:
    .word  0x0984de8c                     @ 080ce1f0 8cde8409
DAT_080ce1f4:
    .word  0x06013800                     @ 080ce1f4 00380106
DAT_080ce1f8:
    .word  0x02006ed0                     @ 080ce1f8 d06e0002
DAT_080ce1fc:
    .word  0x02000000                     @ 080ce1fc 00000002
DAT_080ce200:
    .word  0x00006c2c                     @ 080ce200 2c6c0000
PTR_font_jp_base_table_080ce204:
    .word  font_jp_base_table             @ 080ce204 54f8e509
DAT_080ce208:
    .word  0x00000213                     @ 080ce208 13020000
PTR_game_str_pointer_table_080ce20c:
    .word  game_str_pointer_table         @ 080ce20c 400f0008
PTR_game_str_ja_080ce210:
    .word  game_str_ja                    @ 080ce210 109cdb09
DAT_080ce214:
    .word  0x00000a01                     @ 080ce214 010a0000

@ Render a card label text string into BG tile VRAM for the card info display. Looks up label string from ROM string table, calls render_jp_string_to_tile_line then write_line_buf_to_bg_tile_vram to commit rendered glyphs. r0: label_id [0..N]; r1: bg_tile_dest ptr; r2: x_col [0..29]; r3: y_row [0..23]. Returns void. Side effects: BG tile VRAM written with label text.
render_card_label_text_to_bg:
    push {r4,r5,r6,r7,lr}                    @ 080ce218 f0b5
    sub sp,#0x4                              @ 080ce21a 81b0
    movs r6,#0x0    @ 080ce21c 0026
    movs r0,#0x17    @ 080ce21e 1720
    movs r1,#0x10    @ 080ce220 1021
    movs r2,#0x1    @ 080ce222 0122
    movs r3,#0x2    @ 080ce224 0223
    bl setup_line_buf_with_font_and_align    @ 080ce226 22f04bfd
    ldr r2, DAT_080ce2cc                     @ 080ce22a 284a
    ldr r0, DAT_080ce2d0                     @ 080ce22c 2848
    ldr r1, DAT_080ce2d4                     @ 080ce22e 2949
    adds r0,r0,r1    @ 080ce230 4018
    movs r7,#0x7    @ 080ce232 0727
    adds r1,r7,#0x0    @ 080ce234 391c
    ldrb r0,[r0,#0x0]                        @ 080ce236 0078
    ands r1,r0    @ 080ce238 0140
    rsbs r1,r1,#0    @ 080ce23a 4942
    lsrs r1,r1,#0x1f    @ 080ce23c c90f
    movs r0,#0x2    @ 080ce23e 0220
    rsbs r0,r0,#0    @ 080ce240 4042
    ldrb r3,[r2,#0x8]                        @ 080ce242 137a
    ands r0,r3    @ 080ce244 1840
    orrs r0,r1    @ 080ce246 0843
    movs r1,#0x2    @ 080ce248 0221
    orrs r0,r1    @ 080ce24a 0843
    strb r0,[r2,#0x8]                        @ 080ce24c 1072
    ldr r3, PTR_font_jp_base_table_080ce2d8  @ 080ce24e 224b
    lsls r1,r0,#0x1e    @ 080ce250 8107
    lsrs r1,r1,#0x1f    @ 080ce252 c90f
    lsls r1,r1,#0x2    @ 080ce254 8900
    lsls r0,r0,#0x1f    @ 080ce256 c007
    lsrs r0,r0,#0x1f    @ 080ce258 c00f
    lsls r0,r0,#0x3    @ 080ce25a c000
    adds r1,r1,r0    @ 080ce25c 0918
    adds r1,r1,r3    @ 080ce25e c918
    ldr r0,[r1,#0x0]                         @ 080ce260 0868
    str r0,[r2,#0x4]                         @ 080ce262 5060
    movs r0,#0x40    @ 080ce264 4020
    ldrb r1,[r2,#0x15]                       @ 080ce266 517d
    orrs r0,r1    @ 080ce268 0843
    strb r0,[r2,#0x15]                       @ 080ce26a 5075
    ldr r5, DAT_080ce2dc                     @ 080ce26c 1b4d
    str r6,[sp,#0x0]                         @ 080ce26e 0096
    movs r0,#0x2    @ 080ce270 0220
    movs r1,#0x2    @ 080ce272 0221
    adds r2,r5,#0x0    @ 080ce274 2a1c
    movs r3,#0xc    @ 080ce276 0c23
    bl render_jp_string_to_tile_line         @ 080ce278 f9f722fa
    adds r4,r0,#0x0    @ 080ce27c 041c
    adds r1,r4,#0x3    @ 080ce27e e11c
    ldr r2, DAT_080ce2e0                     @ 080ce280 174a
    adds r0,r5,r2    @ 080ce282 a818
    strh r1,[r0,#0x0]                        @ 080ce284 0180
    adds r4,#0x20    @ 080ce286 2034
    ldr r0, DAT_080ce2e4                     @ 080ce288 1648
    movs r1,#0x0    @ 080ce28a 0021
    bl write_line_buf_to_bg_tile_vram        @ 080ce28c 25f0a2fa
    adds r4,#0x18    @ 080ce290 1834
    adds r0,r4,#0x0    @ 080ce292 201c
    cmp r4,#0x0                              @ 080ce294 002c
    bge LAB_080ce29a                         @ 080ce296 00da
    adds r0,r4,#0x7    @ 080ce298 e01d
LAB_080ce29a:
    asrs r6,r0,#0x3    @ 080ce29a c610
    ands r4,r7    @ 080ce29c 3c40
    cmp r4,#0x0                              @ 080ce29e 002c
    beq LAB_080ce2a4                         @ 080ce2a0 00d0
    adds r6,#0x1    @ 080ce2a2 0136
LAB_080ce2a4:
    ldr r3, DAT_080ce2e8                     @ 080ce2a4 104b
    adds r0,r5,r3    @ 080ce2a6 e818
    ldrb r0,[r0,#0x0]                        @ 080ce2a8 0078
    lsrs r2,r0,#0x1    @ 080ce2aa 4208
    ldr r0, DAT_080ce2ec                     @ 080ce2ac 0f48
    adds r1,r5,r0    @ 080ce2ae 2918
    movs r0,#0x1    @ 080ce2b0 0120
    ldrb r1,[r1,#0x0]                        @ 080ce2b2 0978
    ands r0,r1    @ 080ce2b4 0840
    lsls r0,r0,#0x7    @ 080ce2b6 c001
    orrs r0,r2    @ 080ce2b8 1043
    cmp r0,#0x0                              @ 080ce2ba 0028
    bne LAB_080ce2c4                         @ 080ce2bc 02d1
    ldr r1, DAT_080ce2f0                     @ 080ce2be 0c49
    adds r0,r5,r1    @ 080ce2c0 6818
    strb r6,[r0,#0x0]                        @ 080ce2c2 0670
LAB_080ce2c4:
    add sp,#0x4                              @ 080ce2c4 01b0
    pop {r4,r5,r6,r7}                        @ 080ce2c6 f0bc
    pop {r0}                                 @ 080ce2c8 01bc
    bx r0                                    @ 080ce2ca 0047
DAT_080ce2cc:
    .word  0x02006ed0                     @ 080ce2cc d06e0002
DAT_080ce2d0:
    .word  0x02000000                     @ 080ce2d0 00000002
DAT_080ce2d4:
    .word  0x00006c2c                     @ 080ce2d4 2c6c0000
PTR_font_jp_base_table_080ce2d8:
    .word  font_jp_base_table             @ 080ce2d8 54f8e509
DAT_080ce2dc:
    .word  0x0201f441                     @ 080ce2dc 41f40102
DAT_080ce2e0:
    .word  0x00000a03                     @ 080ce2e0 030a0000
DAT_080ce2e4:
    .word  0x06014000                     @ 080ce2e4 00400106
DAT_080ce2e8:
    .word  0x00000a16                     @ 080ce2e8 160a0000
DAT_080ce2ec:
    .word  0x00000a17                     @ 080ce2ec 170a0000
DAT_080ce2f0:
    .word  0x00000a02                     @ 080ce2f0 020a0000

@ Card-list OAM row render branch for type_icon variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 6. Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword x_base. Reads gFontState[0x0a18] bits[23:8] (mask 0xff<<9): 0 -> icon_base=4; nonzero -> 3. Reads gFontState[0x0a1b] bits[1:0] slot_state. slot_state<=1: iterates up to slot_count (gFontState[0x0a10] halfword bits[23:16]) icons; each icon: calls write_oam_entry_from_packed_args (slot=0x40, attr0=0x1e, tile_x=(slot_idx+1)*2+x_base). slot_state>1: writes extra OAM entry (attr1=0xc0<<1). No APCS inputs. Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; TYPE_FIELD_OFFSET=0x0a18 bits[23:8]; SLOT_COUNT_OFFSET=0x0a10 bits[23:16]; SLOT_STATE_OFFSET=0x0a1b [0..1]; ATTR0_ICON=0x1e; OAM_SLOT=0x40.
render_card_list_oam_row_by_type_icon:
    push {r4,r5,r6,r7,lr}                    @ 080ce2f4 f0b5
    .hword 0x4657    @ 080ce2f6 5746
    .hword 0x464e    @ 080ce2f8 4e46
    .hword 0x4645    @ 080ce2fa 4546
    push {r5,r6,r7}                          @ 080ce2fc e0b4
    sub sp,#0x4                              @ 080ce2fe 81b0
    movs r0,#0x32    @ 080ce300 3220
    .hword 0x4681    @ 080ce302 8146
    ldr r2, DAT_080ce3dc                     @ 080ce304 354a
    ldr r1, DAT_080ce3e0                     @ 080ce306 3649
    adds r0,r2,r1    @ 080ce308 5018
    ldrb r0,[r0,#0x0]                        @ 080ce30a 0078
    lsrs r1,r0,#0x1    @ 080ce30c 4108
    movs r0,#0xa    @ 080ce30e 0a20
    subs r0,r0,r1    @ 080ce310 401a
    lsls r0,r0,#0x3    @ 080ce312 c000
    ldr r6, DAT_080ce3e4                     @ 080ce314 334e
    adds r3,r2,r6    @ 080ce316 9319
    ldrh r7,[r3,#0x0]                        @ 080ce318 1f88
    adds r5,r7,r0    @ 080ce31a 3d18
    movs r0,#0x1e    @ 080ce31c 1e20
    .hword 0x4680    @ 080ce31e 8046
    ldr r1, DAT_080ce3e8                     @ 080ce320 3149
    adds r0,r2,r1    @ 080ce322 5018
    ldr r0,[r0,#0x0]                         @ 080ce324 0068
    movs r1,#0xff    @ 080ce326 ff21
    lsls r1,r1,#0x9    @ 080ce328 4902
    ands r0,r1    @ 080ce32a 0840
    movs r6,#0x4    @ 080ce32c 0426
    .hword 0x46b2    @ 080ce32e b246
    cmp r0,#0x0                              @ 080ce330 0028
    beq LAB_080ce338                         @ 080ce332 01d0
    movs r7,#0x3    @ 080ce334 0327
    .hword 0x46ba    @ 080ce336 ba46
LAB_080ce338:
    ldr r1, DAT_080ce3ec                     @ 080ce338 2c49
    adds r0,r2,r1    @ 080ce33a 5018
    ldrb r0,[r0,#0x0]                        @ 080ce33c 0078
    lsrs r0,r0,#0x1    @ 080ce33e 4008
    movs r1,#0x3    @ 080ce340 0321
    ands r0,r1    @ 080ce342 0840
    lsls r6,r5,#0x10    @ 080ce344 2e04
    str r6,[sp,#0x0]                         @ 080ce346 0096
    cmp r0,#0x1                              @ 080ce348 0128
    bhi LAB_080ce3be                         @ 080ce34a 38d8
    movs r4,#0x0    @ 080ce34c 0024
    ldr r7, DAT_080ce3f0                     @ 080ce34e 284f
    adds r1,r2,r7    @ 080ce350 d119
    ldrh r6,[r1,#0x0]                        @ 080ce352 0e88
    lsls r0,r6,#0x14    @ 080ce354 3005
    lsrs r0,r0,#0x18    @ 080ce356 000e
    cmp r4,r0                                @ 080ce358 8442
    bge LAB_080ce3be                         @ 080ce35a 30da
    adds r6,r3,#0x0    @ 080ce35c 1e1c
LAB_080ce35e:
    lsls r0,r4,#0x4    @ 080ce35e 2001
    adds r1,r0,#0x0    @ 080ce360 011c
    adds r1,#0xb0    @ 080ce362 b031
    adds r2,r5,#0x0    @ 080ce364 2a1c
    adds r2,#0x10    @ 080ce366 1032
    ldr r7, DAT_080ce3dc                     @ 080ce368 1c4f
    ldr r3, DAT_080ce3e8                     @ 080ce36a 1f4b
    adds r0,r7,r3    @ 080ce36c f818
    ldr r0,[r0,#0x0]                         @ 080ce36e 0068
    lsls r0,r0,#0xf    @ 080ce370 c003
    lsrs r0,r0,#0x18    @ 080ce372 000e
    cmp r0,#0x2                              @ 080ce374 0228
    bls LAB_080ce38c                         @ 080ce376 09d9
    adds r0,r4,#0x1    @ 080ce378 601c
    lsls r0,r0,#0x1    @ 080ce37a 4000
    adds r0,r0,r6    @ 080ce37c 8019
    ldrh r1,[r0,#0x0]                        @ 080ce37e 0188
    .hword 0x4647    @ 080ce380 4746
    muls r7,r1    @ 080ce382 4f43
    adds r0,r7,#0x0    @ 080ce384 381c
    .hword 0x464a    @ 080ce386 4a46
    adds r1,r2,r0    @ 080ce388 1118
    adds r2,r5,#0x0    @ 080ce38a 2a1c
LAB_080ce38c:
    lsls r0,r2,#0x10    @ 080ce38c 1004
    orrs r1,r0    @ 080ce38e 0143
    adds r2,r4,#0x5    @ 080ce390 621d
    lsls r2,r2,#0xc    @ 080ce392 1203
    adds r4,#0x1    @ 080ce394 0134
    lsls r0,r4,#0x1    @ 080ce396 6000
    adds r0,r0,r6    @ 080ce398 8019
    ldrh r0,[r0,#0x0]                        @ 080ce39a 0088
    lsls r0,r0,#0x1    @ 080ce39c 4000
    movs r3,#0xc0    @ 080ce39e c023
    lsls r3,r3,#0x1    @ 080ce3a0 5b00
    adds r0,r0,r3    @ 080ce3a2 c018
    orrs r2,r0    @ 080ce3a4 0243
    lsls r2,r2,#0x10    @ 080ce3a6 1204
    lsrs r2,r2,#0x10    @ 080ce3a8 120c
    adds r0,r1,#0x0    @ 080ce3aa 081c
    movs r1,#0x40    @ 080ce3ac 4021
    bl write_oam_entry_from_packed_args      @ 080ce3ae 27f0ddfe
    ldr r7, DAT_080ce3f4                     @ 080ce3b2 104f
    ldrh r7,[r7,#0x0]                        @ 080ce3b4 3f88
    lsls r0,r7,#0x14    @ 080ce3b6 3805
    lsrs r0,r0,#0x18    @ 080ce3b8 000e
    cmp r4,r0                                @ 080ce3ba 8442
    blt LAB_080ce35e                         @ 080ce3bc cfdb
LAB_080ce3be:
    movs r4,#0x0    @ 080ce3be 0024
    ldr r7, DAT_080ce3f8                     @ 080ce3c0 0d4f
    movs r6,#0xc0    @ 080ce3c2 c026
    lsls r6,r6,#0x1    @ 080ce3c4 7600
    .hword 0x464d    @ 080ce3c6 4d46
LAB_080ce3c8:
    adds r1,r5,#0x0    @ 080ce3c8 291c
    ldr r0,[sp,#0x0]                         @ 080ce3ca 0098
    orrs r1,r0    @ 080ce3cc 0143
    ldrh r2,[r7,#0x0]                        @ 080ce3ce 3a88
    cmp r4,r2                                @ 080ce3d0 9442
    bne LAB_080ce3fc                         @ 080ce3d2 13d1
    .hword 0x4653    @ 080ce3d4 5346
    lsls r0,r3,#0xc    @ 080ce3d6 1803
    b LAB_080ce400                           @ 080ce3d8 12e0
    .zero  0x2
DAT_080ce3dc:
    .word  0x0201f440                     @ 080ce3dc 40f40102
DAT_080ce3e0:
    .word  0x00000a03                     @ 080ce3e0 030a0000
DAT_080ce3e4:
    .word  0x00000a04                     @ 080ce3e4 040a0000
DAT_080ce3e8:
    .word  0x00000a18                     @ 080ce3e8 180a0000
DAT_080ce3ec:
    .word  0x00000a1b                     @ 080ce3ec 1b0a0000
DAT_080ce3f0:
    .word  0x00000a0e                     @ 080ce3f0 0e0a0000
DAT_080ce3f4:
    .word  0x0201fe4e                     @ 080ce3f4 4efe0102
DAT_080ce3f8:
    .word  0x0201fe54                     @ 080ce3f8 54fe0102
LAB_080ce3fc:
    movs r0,#0xc0    @ 080ce3fc c020
    lsls r0,r0,#0x6    @ 080ce3fe 8001
LAB_080ce400:
    orrs r0,r6    @ 080ce400 3043
    lsls r0,r0,#0x10    @ 080ce402 0004
    lsrs r2,r0,#0x10    @ 080ce404 020c
    adds r0,r1,#0x0    @ 080ce406 081c
    movs r1,#0x40    @ 080ce408 4021
    bl write_oam_entry_from_packed_args      @ 080ce40a 27f0affe
    adds r6,#0x2    @ 080ce40e 0236
    add r5,r8                                @ 080ce410 4544
    adds r4,#0x1    @ 080ce412 0134
    cmp r4,#0x5                              @ 080ce414 052c
    ble LAB_080ce3c8                         @ 080ce416 d7dd
    add sp,#0x4                              @ 080ce418 01b0
    pop {r3,r4,r5}                           @ 080ce41a 38bc
    .hword 0x4698    @ 080ce41c 9846
    .hword 0x46a1    @ 080ce41e a146
    .hword 0x46aa    @ 080ce420 aa46
    pop {r4,r5,r6,r7}                        @ 080ce422 f0bc
    pop {r0}                                 @ 080ce424 01bc
    bx r0                                    @ 080ce426 0047

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Differs from the other 7 sibling functions: adds extra Y offset from gFontState+0x0a04 halfword on top of base Y=(10-count/2)*8, then calls write_card_list_oam_row_strip. After the icon row: 5-iteration loop writes cursor sprites via write_oam_entry_from_packed_args (OAM slot base 0x32, x=0x32 stepped). Then reads gPrng+0x148 flags for four-way dispatch: (1) bit4=1: calls find_next_occupied_slot_in_main_list, strh result to gFontState+0x0a14, sets gFontState+0x0a18 bit9, sync_state_and_init_sprite(0); (2) bit5=1: calls find_next_occupied_slot_in_secondary_list, same state update; (3) bit0=1: increments gFontState+0x0a0e nibble (bits[23:16]+1 & 0xff), copy_bytes_by_halfword ROM 0x0984e30c -> OBJ pal 0x05000280 (0x20 hw), builds LP bit-set from gFontState+0x0a06, writes to gP1LifePoints+0x3d40, sync_state_and_init_sprite(0x24); (4) else: no-op. Constants: Y_EXTRA_OFFSET=0x0a04; OAM_CURSOR_LOOP=5; OAM_CURSOR_X=0x32; FLAG_MAIN=0x10; FLAG_SEC=0x20; FLAG_LP=0x01; ROM_PAL=0x0984e30c; OBJ_PAL=0x05000280.
render_card_list_oam_row_by_slot_advance:
    push {r4,r5,r6,r7,lr}                    @ 080ce428 f0b5
    .hword 0x4647    @ 080ce42a 4746
    push {r7}                                @ 080ce42c 80b4
    ldr r4, DAT_080ce46c                     @ 080ce42e 0f4c
    ldr r1, DAT_080ce470                     @ 080ce430 0f49
    adds r0,r4,r1    @ 080ce432 6018
    ldrb r3,[r0,#0x0]                        @ 080ce434 0378
    lsrs r0,r3,#0x1    @ 080ce436 5808
    movs r1,#0xa    @ 080ce438 0a21
    subs r1,r1,r0    @ 080ce43a 091a
    lsls r1,r1,#0x3    @ 080ce43c c900
    ldr r2, DAT_080ce474                     @ 080ce43e 0d4a
    adds r0,r4,r2    @ 080ce440 a018
    ldrh r0,[r0,#0x0]                        @ 080ce442 0088
    adds r6,r0,r1    @ 080ce444 4618
    movs r2,#0xfe    @ 080ce446 fe22
    lsls r2,r2,#0x1    @ 080ce448 5200
    movs r0,#0x30    @ 080ce44a 3020
    bl write_card_list_oam_row_strip         @ 080ce44c f9f770f8
    ldr r3, DAT_080ce478                     @ 080ce450 094b
    adds r5,r4,r3    @ 080ce452 e518
    ldr r0,[r5,#0x0]                         @ 080ce454 2868
    lsls r0,r0,#0xf    @ 080ce456 c003
    lsrs r0,r0,#0x18    @ 080ce458 000e
    cmp r0,#0x1                              @ 080ce45a 0128
    bne LAB_080ce460                         @ 080ce45c 00d1
    b LAB_080ce664                           @ 080ce45e 01e1
LAB_080ce460:
    cmp r0,#0x1                              @ 080ce460 0128
    bgt LAB_080ce47c                         @ 080ce462 0bdc
    cmp r0,#0x0                              @ 080ce464 0028
    beq LAB_080ce48a                         @ 080ce466 10d0
    b LAB_080ce7e4                           @ 080ce468 bce1
    .zero  0x2
DAT_080ce46c:
    .word  0x0201f440                     @ 080ce46c 40f40102
DAT_080ce470:
    .word  0x00000a03                     @ 080ce470 030a0000
DAT_080ce474:
    .word  0x00000a04                     @ 080ce474 040a0000
DAT_080ce478:
    .word  0x00000a18                     @ 080ce478 180a0000
LAB_080ce47c:
    cmp r0,#0x2                              @ 080ce47c 0228
    bne LAB_080ce482                         @ 080ce47e 00d1
    b LAB_080ce6e4                           @ 080ce480 30e1
LAB_080ce482:
    cmp r0,#0x3                              @ 080ce482 0328
    bne LAB_080ce488                         @ 080ce484 00d1
    b LAB_080ce76c                           @ 080ce486 71e1
LAB_080ce488:
    b LAB_080ce7e4                           @ 080ce488 ace1
LAB_080ce48a:
    movs r5,#0x0    @ 080ce48a 0025
    adds r6,#0x14    @ 080ce48c 1436
    movs r4,#0x32    @ 080ce48e 3224
LAB_080ce490:
    lsls r0,r6,#0x10    @ 080ce490 3004
    orrs r0,r4    @ 080ce492 2043
    lsls r2,r5,#0x12    @ 080ce494 aa04
    movs r1,#0xe0    @ 080ce496 e021
    lsls r1,r1,#0x11    @ 080ce498 4904
    adds r2,r2,r1    @ 080ce49a 5218
    lsrs r2,r2,#0x10    @ 080ce49c 120c
    movs r1,#0x81    @ 080ce49e 8121
    lsls r1,r1,#0x7    @ 080ce4a0 c901
    bl write_oam_entry_from_packed_args      @ 080ce4a2 27f063fe
    adds r4,#0x20    @ 080ce4a6 2034
    adds r5,#0x1    @ 080ce4a8 0135
    cmp r5,#0x4                              @ 080ce4aa 042d
    ble LAB_080ce490                         @ 080ce4ac f0dd
    ldr r0, PTR_gPrng_080ce4e8               @ 080ce4ae 0e48
    movs r2,#0xa4    @ 080ce4b0 a422
    lsls r2,r2,#0x1    @ 080ce4b2 5200
    adds r0,r0,r2    @ 080ce4b4 8018
    ldrh r1,[r0,#0x0]                        @ 080ce4b6 0188
    movs r0,#0x10    @ 080ce4b8 1020
    ands r0,r1    @ 080ce4ba 0840
    cmp r0,#0x0                              @ 080ce4bc 0028
    beq LAB_080ce4fc                         @ 080ce4be 1dd0
    ldr r4, DAT_080ce4ec                     @ 080ce4c0 0a4c
    ldr r3, DAT_080ce4f0                     @ 080ce4c2 0b4b
    adds r5,r4,r3    @ 080ce4c4 e518
    ldrh r0,[r5,#0x0]                        @ 080ce4c6 2888
    bl find_next_occupied_slot_in_main_list  @ 080ce4c8 fff750fd
    strh r0,[r5,#0x0]                        @ 080ce4cc 2880
    ldr r6, DAT_080ce4f4                     @ 080ce4ce 094e
    adds r4,r4,r6    @ 080ce4d0 a419
LAB_080ce4d2:
    ldr r0,[r4,#0x0]                         @ 080ce4d2 2068
    ldr r1, DAT_080ce4f8                     @ 080ce4d4 0849
    ands r0,r1    @ 080ce4d6 0840
    movs r1,#0x80    @ 080ce4d8 8021
    lsls r1,r1,#0x2    @ 080ce4da 8900
    orrs r0,r1    @ 080ce4dc 0843
    str r0,[r4,#0x0]                         @ 080ce4de 2060
    movs r0,#0x0    @ 080ce4e0 0020
    bl sync_state_and_init_sprite            @ 080ce4e2 2bf0e7fa
    b LAB_080ce7e4                           @ 080ce4e6 7de1
PTR_gPrng_080ce4e8:
    .word  gPrng                          @ 080ce4e8 40000003
DAT_080ce4ec:
    .word  0x0201f440                     @ 080ce4ec 40f40102
DAT_080ce4f0:
    .word  0x00000a14                     @ 080ce4f0 140a0000
DAT_080ce4f4:
    .word  0x00000a18                     @ 080ce4f4 180a0000
DAT_080ce4f8:
    .word  0xfffe01ff                     @ 080ce4f8 ff01feff
LAB_080ce4fc:
    movs r0,#0x20    @ 080ce4fc 2020
    ands r0,r1    @ 080ce4fe 0840
    cmp r0,#0x0                              @ 080ce500 0028
    beq LAB_080ce524                         @ 080ce502 0fd0
    ldr r4, DAT_080ce518                     @ 080ce504 044c
    ldr r0, DAT_080ce51c                     @ 080ce506 0548
    adds r5,r4,r0    @ 080ce508 2518
    ldrh r0,[r5,#0x0]                        @ 080ce50a 2888
    bl find_next_occupied_slot_in_secondary_list @ 080ce50c fff772fd
    strh r0,[r5,#0x0]                        @ 080ce510 2880
    ldr r1, DAT_080ce520                     @ 080ce512 0349
    adds r4,r4,r1    @ 080ce514 6418
    b LAB_080ce4d2                           @ 080ce516 dce7
DAT_080ce518:
    .word  0x0201f440                     @ 080ce518 40f40102
DAT_080ce51c:
    .word  0x00000a14                     @ 080ce51c 140a0000
DAT_080ce520:
    .word  0x00000a18                     @ 080ce520 180a0000
LAB_080ce524:
    movs r0,#0x1    @ 080ce524 0120
    ands r0,r1    @ 080ce526 0840
    cmp r0,#0x0                              @ 080ce528 0028
    beq LAB_080ce620                         @ 080ce52a 79d0
    ldr r6, DAT_080ce5cc                     @ 080ce52c 274e
    ldr r2, DAT_080ce5d0                     @ 080ce52e 284a
    adds r4,r6,r2    @ 080ce530 b418
    ldrh r2,[r4,#0x0]                        @ 080ce532 2288
    lsls r1,r2,#0x14    @ 080ce534 1105
    lsrs r1,r1,#0x18    @ 080ce536 090e
    adds r1,#0x1    @ 080ce538 0131
    movs r0,#0xff    @ 080ce53a ff20
    ands r1,r0    @ 080ce53c 0140
    lsls r1,r1,#0x4    @ 080ce53e 0901
    ldr r0, DAT_080ce5d4                     @ 080ce540 2448
    ands r0,r2    @ 080ce542 1040
    orrs r0,r1    @ 080ce544 0843
    strh r0,[r4,#0x0]                        @ 080ce546 2080
    lsls r0,r0,#0x14    @ 080ce548 0005
    lsrs r0,r0,#0x18    @ 080ce54a 000e
    lsls r0,r0,#0x5    @ 080ce54c 4001
    ldr r3, DAT_080ce5d8                     @ 080ce54e 224b
    adds r0,r0,r3    @ 080ce550 c018
    ldr r1, DAT_080ce5dc                     @ 080ce552 2249
    adds r5,r6,r1    @ 080ce554 7518
    ldrh r2,[r5,#0x0]                        @ 080ce556 2a88
    lsls r1,r2,#0x5    @ 080ce558 5101
    ldr r2, DAT_080ce5e0                     @ 080ce55a 214a
    adds r1,r1,r2    @ 080ce55c 8918
    movs r2,#0x20    @ 080ce55e 2022
    bl copy_bytes_by_halfword                @ 080ce560 26f0a0fc
    ldrh r3,[r4,#0x0]                        @ 080ce564 2388
    lsls r0,r3,#0x14    @ 080ce566 1805
    lsrs r0,r0,#0x18    @ 080ce568 000e
    lsls r0,r0,#0x1    @ 080ce56a 4000
    ldr r2, DAT_080ce5e4                     @ 080ce56c 1d4a
    adds r1,r6,r2    @ 080ce56e b118
    adds r0,r0,r1    @ 080ce570 4018
    ldrh r1,[r5,#0x0]                        @ 080ce572 2988
    strh r1,[r0,#0x0]                        @ 080ce574 0180
    ldrh r4,[r4,#0x0]                        @ 080ce576 2488
    lsls r2,r4,#0x14    @ 080ce578 2205
    ldr r3, DAT_080ce5e8                     @ 080ce57a 1b4b
    adds r1,r6,r3    @ 080ce57c f118
    lsrs r0,r2,#0x18    @ 080ce57e 100e
    ldrb r1,[r1,#0x0]                        @ 080ce580 0978
    cmp r0,r1                                @ 080ce582 8842
    bne LAB_080ce5fc                         @ 080ce584 3ad1
    movs r3,#0x0    @ 080ce586 0023
    movs r5,#0x0    @ 080ce588 0025
    ldr r7, PTR_gP1LifePoints_080ce5ec       @ 080ce58a 184f
    cmp r5,r0                                @ 080ce58c 8542
    bge LAB_080ce5a8                         @ 080ce58e 0bda
    ldr r0, DAT_080ce5f0                     @ 080ce590 1748
    adds r1,r6,r0    @ 080ce592 3118
    movs r4,#0x1    @ 080ce594 0124
LAB_080ce596:
    adds r0,r4,#0x0    @ 080ce596 201c
    ldrh r6,[r1,#0x0]                        @ 080ce598 0e88
    lsls r0,r6    @ 080ce59a b040
    orrs r3,r0    @ 080ce59c 0343
    adds r1,#0x2    @ 080ce59e 0231
    adds r5,#0x1    @ 080ce5a0 0135
    lsrs r0,r2,#0x18    @ 080ce5a2 100e
    cmp r5,r0                                @ 080ce5a4 8542
    blt LAB_080ce596                         @ 080ce5a6 f6db
LAB_080ce5a8:
    movs r0,#0xea    @ 080ce5a8 ea20
    lsls r0,r0,#0x5    @ 080ce5aa 4001
    adds r1,r7,r0    @ 080ce5ac 3918
    lsls r0,r3,#0x1    @ 080ce5ae 5800
    str r0,[r1,#0x0]                         @ 080ce5b0 0860
    movs r0,#0x24    @ 080ce5b2 2420
    bl sync_state_and_init_sprite            @ 080ce5b4 2bf07efa
    ldr r2, DAT_080ce5cc                     @ 080ce5b8 044a
    ldr r1, DAT_080ce5f4                     @ 080ce5ba 0e49
    adds r2,r2,r1    @ 080ce5bc 5218
    ldr r0,[r2,#0x0]                         @ 080ce5be 1068
    ldr r1, DAT_080ce5f8                     @ 080ce5c0 0d49
    ands r0,r1    @ 080ce5c2 0840
    movs r1,#0xc0    @ 080ce5c4 c021
    lsls r1,r1,#0x3    @ 080ce5c6 c900
    b LAB_080ce612                           @ 080ce5c8 23e0
    .zero  0x2
DAT_080ce5cc:
    .word  0x0201f440                     @ 080ce5cc 40f40102
DAT_080ce5d0:
    .word  0x00000a0e                     @ 080ce5d0 0e0a0000
DAT_080ce5d4:
    .word  0xfffff00f                     @ 080ce5d4 0ff0ffff
DAT_080ce5d8:
    .word  0x05000280                     @ 080ce5d8 80020005
DAT_080ce5dc:
    .word  0x00000a14                     @ 080ce5dc 140a0000
DAT_080ce5e0:
    .word  0x0984e30c                     @ 080ce5e0 0ce38409
DAT_080ce5e4:
    .word  0x00000a04                     @ 080ce5e4 040a0000
DAT_080ce5e8:
    .word  0x00000a02                     @ 080ce5e8 020a0000
PTR_gP1LifePoints_080ce5ec:
    .word  gP1LifePoints                  @ 080ce5ec e0c40102
DAT_080ce5f0:
    .word  0x00000a06                     @ 080ce5f0 060a0000
DAT_080ce5f4:
    .word  0x00000a18                     @ 080ce5f4 180a0000
DAT_080ce5f8:
    .word  0xfffe01ff                     @ 080ce5f8 ff01feff
LAB_080ce5fc:
    ldrh r0,[r5,#0x0]                        @ 080ce5fc 2888
    bl find_next_occupied_slot_in_main_list  @ 080ce5fe fff7b5fc
    strh r0,[r5,#0x0]                        @ 080ce602 2880
    ldr r3, DAT_080ce618                     @ 080ce604 044b
    adds r2,r6,r3    @ 080ce606 f218
    ldr r0,[r2,#0x0]                         @ 080ce608 1068
    ldr r1, DAT_080ce61c                     @ 080ce60a 0449
    ands r0,r1    @ 080ce60c 0840
    movs r1,#0x80    @ 080ce60e 8021
    lsls r1,r1,#0x2    @ 080ce610 8900
LAB_080ce612:
    orrs r0,r1    @ 080ce612 0843
    str r0,[r2,#0x0]                         @ 080ce614 1060
    b LAB_080ce7e4                           @ 080ce616 e5e0
DAT_080ce618:
    .word  0x00000a18                     @ 080ce618 180a0000
DAT_080ce61c:
    .word  0xfffe01ff                     @ 080ce61c ff01feff
LAB_080ce620:
    movs r0,#0x2    @ 080ce620 0220
    ands r0,r1    @ 080ce622 0840
    cmp r0,#0x0                              @ 080ce624 0028
    bne LAB_080ce62a                         @ 080ce626 00d1
    b LAB_080ce7e4                           @ 080ce628 dce0
LAB_080ce62a:
    ldr r0, DAT_080ce658                     @ 080ce62a 0b48
    ldr r6, DAT_080ce65c                     @ 080ce62c 0b4e
    adds r3,r0,r6    @ 080ce62e 8319
    ldrh r2,[r3,#0x0]                        @ 080ce630 1a88
    movs r0,#0xff    @ 080ce632 ff20
    lsls r0,r0,#0x4    @ 080ce634 0001
    ands r0,r2    @ 080ce636 1040
    cmp r0,#0x0                              @ 080ce638 0028
    beq LAB_080ce650                         @ 080ce63a 09d0
    lsls r0,r2,#0x14    @ 080ce63c 1005
    lsrs r0,r0,#0x18    @ 080ce63e 000e
    subs r0,#0x1    @ 080ce640 0138
    movs r1,#0xff    @ 080ce642 ff21
    ands r0,r1    @ 080ce644 0840
    lsls r0,r0,#0x4    @ 080ce646 0001
    ldr r1, DAT_080ce660                     @ 080ce648 0549
    ands r1,r2    @ 080ce64a 1140
    orrs r1,r0    @ 080ce64c 0143
    strh r1,[r3,#0x0]                        @ 080ce64e 1980
LAB_080ce650:
    movs r0,#0x2    @ 080ce650 0220
    bl sync_state_and_init_sprite            @ 080ce652 2bf02ffa
    b LAB_080ce7e4                           @ 080ce656 c5e0
DAT_080ce658:
    .word  0x0201f440                     @ 080ce658 40f40102
DAT_080ce65c:
    .word  0x00000a0e                     @ 080ce65c 0e0a0000
DAT_080ce660:
    .word  0xfffff00f                     @ 080ce660 0ff0ffff
LAB_080ce664:
    ldr r0, DAT_080ce6cc                     @ 080ce664 1948
    movs r1,#0x0    @ 080ce666 0021
    movs r2,#0x17    @ 080ce668 1722
    movs r3,#0x2    @ 080ce66a 0223
    bl tile_2d_row_copy                      @ 080ce66c 28f032ff
    movs r0,#0x17    @ 080ce670 1720
    movs r1,#0x2    @ 080ce672 0221
    movs r2,#0x1    @ 080ce674 0122
    movs r3,#0x0    @ 080ce676 0023
    bl setup_line_buf_with_font_and_align    @ 080ce678 22f022fb
    ldr r2, DAT_080ce6d0                     @ 080ce67c 144a
    ldr r0, DAT_080ce6d4                     @ 080ce67e 1548
    ldr r1, DAT_080ce6d8                     @ 080ce680 1549
    adds r0,r0,r1    @ 080ce682 4018
    movs r1,#0x7    @ 080ce684 0721
    ldrb r0,[r0,#0x0]                        @ 080ce686 0078
    ands r1,r0    @ 080ce688 0140
    rsbs r1,r1,#0    @ 080ce68a 4942
    lsrs r1,r1,#0x1f    @ 080ce68c c90f
    movs r0,#0x2    @ 080ce68e 0220
    rsbs r0,r0,#0    @ 080ce690 4042
    ldrb r3,[r2,#0x8]                        @ 080ce692 137a
    ands r0,r3    @ 080ce694 1840
    orrs r0,r1    @ 080ce696 0843
    movs r1,#0x2    @ 080ce698 0221
    orrs r0,r1    @ 080ce69a 0843
    strb r0,[r2,#0x8]                        @ 080ce69c 1072
    ldr r3, PTR_font_jp_base_table_080ce6dc  @ 080ce69e 0f4b
    lsls r1,r0,#0x1e    @ 080ce6a0 8107
    lsrs r1,r1,#0x1f    @ 080ce6a2 c90f
    lsls r1,r1,#0x2    @ 080ce6a4 8900
    lsls r0,r0,#0x1f    @ 080ce6a6 c007
    lsrs r0,r0,#0x1f    @ 080ce6a8 c00f
    lsls r0,r0,#0x3    @ 080ce6aa c000
    adds r1,r1,r0    @ 080ce6ac 0918
    adds r1,r1,r3    @ 080ce6ae c918
    ldr r0,[r1,#0x0]                         @ 080ce6b0 0868
    str r0,[r2,#0x4]                         @ 080ce6b2 5060
    movs r0,#0x40    @ 080ce6b4 4020
    ldrb r6,[r2,#0x15]                       @ 080ce6b6 567d
    orrs r0,r6    @ 080ce6b8 3043
    strb r0,[r2,#0x15]                       @ 080ce6ba 5075
    ldr r0,[r5,#0x0]                         @ 080ce6bc 2868
    ldr r1, DAT_080ce6e0                     @ 080ce6be 0849
    ands r0,r1    @ 080ce6c0 0840
    movs r1,#0x80    @ 080ce6c2 8021
    lsls r1,r1,#0x3    @ 080ce6c4 c900
    orrs r0,r1    @ 080ce6c6 0843
    str r0,[r5,#0x0]                         @ 080ce6c8 2860
    b LAB_080ce7e4                           @ 080ce6ca 8be0
DAT_080ce6cc:
    .word  0x06013800                     @ 080ce6cc 00380106
DAT_080ce6d0:
    .word  0x02006ed0                     @ 080ce6d0 d06e0002
DAT_080ce6d4:
    .word  0x02000000                     @ 080ce6d4 00000002
DAT_080ce6d8:
    .word  0x00006c2c                     @ 080ce6d8 2c6c0000
PTR_font_jp_base_table_080ce6dc:
    .word  font_jp_base_table             @ 080ce6dc 54f8e509
DAT_080ce6e0:
    .word  0xfffe01ff                     @ 080ce6e0 ff01feff
LAB_080ce6e4:
    ldr r0, DAT_080ce744                     @ 080ce6e4 1748
    adds r4,r4,r0    @ 080ce6e6 2418
    ldrh r1,[r4,#0x0]                        @ 080ce6e8 2188
    ldr r2, DAT_080ce748                     @ 080ce6ea 174a
    adds r0,r1,r2    @ 080ce6ec 8818
    bl game_str_id_to_row                    @ 080ce6ee 26f093fb
    ldr r2, PTR_game_str_pointer_table_080ce74c @ 080ce6f2 164a
    lsls r0,r0,#0x10    @ 080ce6f4 0004
    lsrs r0,r0,#0x10    @ 080ce6f6 000c
    lsls r1,r0,#0x1    @ 080ce6f8 4100
    adds r1,r1,r0    @ 080ce6fa 0918
    lsls r1,r1,#0x1    @ 080ce6fc 4900
    ldr r0, DAT_080ce750                     @ 080ce6fe 1448
    ldr r3, DAT_080ce754                     @ 080ce700 144b
    adds r0,r0,r3    @ 080ce702 c018
    ldrb r0,[r0,#0x0]                        @ 080ce704 0078
    lsls r0,r0,#0x1d    @ 080ce706 4007
    lsrs r0,r0,#0x1d    @ 080ce708 400f
    adds r1,r1,r0    @ 080ce70a 0918
    lsls r1,r1,#0x2    @ 080ce70c 8900
    adds r1,r1,r2    @ 080ce70e 8918
    ldr r3,[r1,#0x0]                         @ 080ce710 0b68
    ldr r0, PTR_game_str_ja_080ce758         @ 080ce712 1148
    adds r3,r3,r0    @ 080ce714 1b18
    movs r0,#0x2    @ 080ce716 0220
    movs r1,#0x2    @ 080ce718 0221
    movs r2,#0x87    @ 080ce71a 8722
    bl text_render_wrapper                   @ 080ce71c 24f0aef9
    ldr r0, DAT_080ce75c                     @ 080ce720 0e48
    movs r1,#0x0    @ 080ce722 0021
    bl write_line_buf_to_bg_tile_vram        @ 080ce724 25f056f8
    ldr r0, DAT_080ce760                     @ 080ce728 0d48
    ldrh r4,[r4,#0x0]                        @ 080ce72a 2488
    lsls r1,r4,#0x5    @ 080ce72c 6101
    ldr r2, DAT_080ce764                     @ 080ce72e 0d4a
    adds r1,r1,r2    @ 080ce730 8918
    movs r2,#0x20    @ 080ce732 2022
    bl copy_bytes_by_halfword                @ 080ce734 26f0b6fb
    ldr r0,[r5,#0x0]                         @ 080ce738 2868
    ldr r1, DAT_080ce768                     @ 080ce73a 0b49
    ands r0,r1    @ 080ce73c 0840
    str r0,[r5,#0x0]                         @ 080ce73e 2860
    b LAB_080ce7e4                           @ 080ce740 50e0
    .zero  0x2
DAT_080ce744:
    .word  0x00000a14                     @ 080ce744 140a0000
DAT_080ce748:
    .word  0x00000213                     @ 080ce748 13020000
PTR_game_str_pointer_table_080ce74c:
    .word  game_str_pointer_table         @ 080ce74c 400f0008
DAT_080ce750:
    .word  0x02000000                     @ 080ce750 00000002
DAT_080ce754:
    .word  0x00006c2c                     @ 080ce754 2c6c0000
PTR_game_str_ja_080ce758:
    .word  game_str_ja                    @ 080ce758 109cdb09
DAT_080ce75c:
    .word  0x06013800                     @ 080ce75c 00380106
DAT_080ce760:
    .word  0x05000280                     @ 080ce760 80020005
DAT_080ce764:
    .word  0x0984e30c                     @ 080ce764 0ce38409
DAT_080ce768:
    .word  0xfffe01ff                     @ 080ce768 ff01feff
LAB_080ce76c:
    movs r5,#0x0    @ 080ce76c 0025
    adds r6,#0x14    @ 080ce76e 1436
    movs r4,#0x32    @ 080ce770 3224
LAB_080ce772:
    lsls r0,r6,#0x10    @ 080ce772 3004
    orrs r0,r4    @ 080ce774 2043
    lsls r2,r5,#0x12    @ 080ce776 aa04
    movs r1,#0xe0    @ 080ce778 e021
    lsls r1,r1,#0x11    @ 080ce77a 4904
    adds r2,r2,r1    @ 080ce77c 5218
    lsrs r2,r2,#0x10    @ 080ce77e 120c
    movs r1,#0x81    @ 080ce780 8121
    lsls r1,r1,#0x7    @ 080ce782 c901
    bl write_oam_entry_from_packed_args      @ 080ce784 27f0f2fc
    adds r4,#0x20    @ 080ce788 2034
    adds r5,#0x1    @ 080ce78a 0135
    cmp r5,#0x4                              @ 080ce78c 042d
    ble LAB_080ce772                         @ 080ce78e f0dd
    ldr r4, DAT_080ce7d8                     @ 080ce790 114c
    ldr r2, DAT_080ce7dc                     @ 080ce792 124a
    adds r2,r2,r4    @ 080ce794 1219
    .hword 0x4690    @ 080ce796 9046
    ldrb r6,[r2,#0x0]                        @ 080ce798 1678
    lsrs r0,r6,#0x1    @ 080ce79a 7008
    ldr r3, DAT_080ce7e0                     @ 080ce79c 104b
    adds r4,r4,r3    @ 080ce79e e418
    movs r5,#0x1    @ 080ce7a0 0125
    adds r2,r5,#0x0    @ 080ce7a2 2a1c
    ldrb r1,[r4,#0x0]                        @ 080ce7a4 2178
    ands r2,r1    @ 080ce7a6 0a40
    lsls r2,r2,#0x7    @ 080ce7a8 d201
    orrs r2,r0    @ 080ce7aa 0243
    adds r3,r2,#0x1    @ 080ce7ac 531c
    movs r1,#0x7f    @ 080ce7ae 7f21
    ands r1,r3    @ 080ce7b0 1940
    lsls r1,r1,#0x1    @ 080ce7b2 4900
    adds r0,r5,#0x0    @ 080ce7b4 281c
    ands r0,r6    @ 080ce7b6 3040
    orrs r0,r1    @ 080ce7b8 0843
    .hword 0x4646    @ 080ce7ba 4646
    strb r0,[r6,#0x0]                        @ 080ce7bc 3070
    lsrs r3,r3,#0x7    @ 080ce7be db09
    ands r3,r5    @ 080ce7c0 2b40
    movs r0,#0x2    @ 080ce7c2 0220
    rsbs r0,r0,#0    @ 080ce7c4 4042
    ldrb r1,[r4,#0x0]                        @ 080ce7c6 2178
    ands r0,r1    @ 080ce7c8 0840
    orrs r0,r3    @ 080ce7ca 1843
    strb r0,[r4,#0x0]                        @ 080ce7cc 2070
    cmp r2,#0x1f                             @ 080ce7ce 1f2a
    bls LAB_080ce7e4                         @ 080ce7d0 08d9
    movs r0,#0x1    @ 080ce7d2 0120
    b LAB_080ce7e6                           @ 080ce7d4 07e0
    .zero  0x2
DAT_080ce7d8:
    .word  0x0201f440                     @ 080ce7d8 40f40102
DAT_080ce7dc:
    .word  0x00000a1b                     @ 080ce7dc 1b0a0000
DAT_080ce7e0:
    .word  0x00000a1c                     @ 080ce7e0 1c0a0000
LAB_080ce7e4:
    movs r0,#0x0    @ 080ce7e4 0020
LAB_080ce7e6:
    pop {r3}                                 @ 080ce7e6 08bc
    .hword 0x4698    @ 080ce7e8 9846
    pop {r4,r5,r6,r7}                        @ 080ce7ea f0bc
    pop {r1}                                 @ 080ce7ec 02bc
    bx r1                                    @ 080ce7ee 0847

@ 由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. 首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x80<<7=0x4000 halfword). 读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的双标志: 若任一非零则跳到 LAB_080cea22 (早期退出). 若均为零则进入主循环 (r6 in [0..?]): 从 card entry 表 (0x0201e4f0 + r6*4) 读取 game_str_id (13 位), 调用 resolve_game_str_ptr 解析字符串指针; 若字符串第一字节为 0 (空串) 则清除 entry.flag[0x11] bit[6]; 否则调用渲染路径 (LAB_080ce86c) 将字符串内容写入 BG VRAM 对应区域. 函数使用 r8/r9 callee-save (.hword 0x4682/4689). Constants: VRAM_BG_BASE=0x06014000, STATE_BASE=0x0201f440, OFFSET_FLAG_A=0x0a17, OFFSET_FLAG_B=0x0a18, CARD_ENTRY_TABLE=0x0201e4f0, ENTRY_FLAG_OFF=0x11, STR_ID_MASK=0x1fff.
zero_fill_card_label_vram_if_ready:
    push {r4,r5,r6,r7,lr}                    @ 080ce7f0 f0b5
    .hword 0x4657    @ 080ce7f2 5746
    .hword 0x464e    @ 080ce7f4 4e46
    .hword 0x4645    @ 080ce7f6 4546
    push {r5,r6,r7}                          @ 080ce7f8 e0b4
    sub sp,#0x4                              @ 080ce7fa 81b0
    movs r0,#0x2    @ 080ce7fc 0220
    .hword 0x4682    @ 080ce7fe 8246
    movs r1,#0x0    @ 080ce800 0021
    .hword 0x4689    @ 080ce802 8946
    ldr r0, DAT_080ce858                     @ 080ce804 1448
    movs r1,#0x80    @ 080ce806 8021
    lsls r1,r1,#0x7    @ 080ce808 c901
    bl zero_fill_by_halfword                 @ 080ce80a 26f033fb
    ldr r1, DAT_080ce85c                     @ 080ce80e 1349
    ldr r2, DAT_080ce860                     @ 080ce810 134a
    adds r0,r1,r2    @ 080ce812 8818
    ldrb r0,[r0,#0x0]                        @ 080ce814 0078
    lsrs r2,r0,#0x1    @ 080ce816 4208
    ldr r3, DAT_080ce864                     @ 080ce818 124b
    adds r1,r1,r3    @ 080ce81a c918
    movs r0,#0x1    @ 080ce81c 0120
    ldrb r1,[r1,#0x0]                        @ 080ce81e 0978
    ands r0,r1    @ 080ce820 0840
    lsls r0,r0,#0x7    @ 080ce822 c001
    orrs r0,r2    @ 080ce824 1043
    cmp r0,#0x0                              @ 080ce826 0028
    beq LAB_080ce82c                         @ 080ce828 00d0
    b LAB_080cea22                           @ 080ce82a fae0
LAB_080ce82c:
    movs r5,#0x0    @ 080ce82c 0025
    movs r6,#0x0    @ 080ce82e 0026
LAB_080ce830:
    ldr r1, DAT_080ce868                     @ 080ce830 0d49
    lsls r0,r6,#0x2    @ 080ce832 b000
    adds r4,r0,r1    @ 080ce834 4418
    ldrh r1,[r4,#0x10]                       @ 080ce836 218a
    lsls r0,r1,#0x13    @ 080ce838 c804
    lsrs r0,r0,#0x13    @ 080ce83a c00c
    bl resolve_game_str_ptr                  @ 080ce83c 20f00afa
    adds r2,r0,#0x0    @ 080ce840 021c
    ldrb r0,[r2,#0x0]                        @ 080ce842 1078
    cmp r0,#0x0                              @ 080ce844 0028
    bne LAB_080ce86c                         @ 080ce846 11d1
    movs r2,#0x41    @ 080ce848 4122
    rsbs r2,r2,#0    @ 080ce84a 5242
    adds r0,r2,#0x0    @ 080ce84c 101c
    ldrb r3,[r4,#0x11]                       @ 080ce84e 637c
    ands r0,r3    @ 080ce850 1840
    strb r0,[r4,#0x11]                       @ 080ce852 6074
    b LAB_080ce87e                           @ 080ce854 13e0
    .zero  0x2
DAT_080ce858:
    .word  0x06014000                     @ 080ce858 00400106
DAT_080ce85c:
    .word  0x0201f440                     @ 080ce85c 40f40102
DAT_080ce860:
    .word  0x00000a17                     @ 080ce860 170a0000
DAT_080ce864:
    .word  0x00000a18                     @ 080ce864 180a0000
DAT_080ce868:
    .word  0x0201e4f0                     @ 080ce868 f0e40102
LAB_080ce86c:
    lsls r0,r6,#0x9    @ 080ce86c 7002
    ldr r1, DAT_080ce9d0                     @ 080ce86e 5849
    adds r0,r0,r1    @ 080ce870 4018
    adds r1,r2,#0x0    @ 080ce872 111c
    bl copy_cstr_to_buf                      @ 080ce874 26f0eefb
    adds r0,r5,#0x1    @ 080ce878 681c
    lsls r0,r0,#0x10    @ 080ce87a 0004
    lsrs r5,r0,#0x10    @ 080ce87c 050c
LAB_080ce87e:
    adds r6,#0x1    @ 080ce87e 0136
    cmp r6,#0x3                              @ 080ce880 032e
    ble LAB_080ce830                         @ 080ce882 d5dd
    ldr r6, DAT_080ce9d4                     @ 080ce884 534e
    ldr r0, DAT_080ce9d8                     @ 080ce886 5448
    adds r2,r6,r0    @ 080ce888 3218
    movs r0,#0xff    @ 080ce88a ff20
    ands r5,r0    @ 080ce88c 0540
    lsls r1,r5,#0x4    @ 080ce88e 2901
    ldr r0, DAT_080ce9dc                     @ 080ce890 5248
    ldrh r3,[r2,#0x0]                        @ 080ce892 1388
    ands r0,r3    @ 080ce894 1840
    orrs r0,r1    @ 080ce896 0843
    strh r0,[r2,#0x0]                        @ 080ce898 1080
    movs r0,#0x17    @ 080ce89a 1720
    movs r1,#0x10    @ 080ce89c 1021
    movs r2,#0x1    @ 080ce89e 0122
    movs r3,#0x2    @ 080ce8a0 0223
    bl setup_line_buf_with_font_and_align    @ 080ce8a2 22f00dfa
    ldr r4, DAT_080ce9e0                     @ 080ce8a6 4e4c
    ldr r5, DAT_080ce9e4                     @ 080ce8a8 4e4d
    ldr r0, DAT_080ce9e8                     @ 080ce8aa 4f48
    adds r5,r5,r0    @ 080ce8ac 2d18
    movs r1,#0x7    @ 080ce8ae 0721
    ldrb r2,[r5,#0x0]                        @ 080ce8b0 2a78
    ands r1,r2    @ 080ce8b2 1140
    rsbs r1,r1,#0    @ 080ce8b4 4942
    lsrs r1,r1,#0x1f    @ 080ce8b6 c90f
    movs r0,#0x2    @ 080ce8b8 0220
    rsbs r0,r0,#0    @ 080ce8ba 4042
    ldrb r3,[r4,#0x8]                        @ 080ce8bc 237a
    ands r0,r3    @ 080ce8be 1840
    orrs r0,r1    @ 080ce8c0 0843
    movs r1,#0x2    @ 080ce8c2 0221
    orrs r0,r1    @ 080ce8c4 0843
    strb r0,[r4,#0x8]                        @ 080ce8c6 2072
    ldr r1, PTR_font_jp_base_table_080ce9ec  @ 080ce8c8 4849
    .hword 0x4688    @ 080ce8ca 8846
    lsls r1,r0,#0x1e    @ 080ce8cc 8107
    lsrs r1,r1,#0x1f    @ 080ce8ce c90f
    lsls r1,r1,#0x2    @ 080ce8d0 8900
    lsls r0,r0,#0x1f    @ 080ce8d2 c007
    lsrs r0,r0,#0x1f    @ 080ce8d4 c00f
    lsls r0,r0,#0x3    @ 080ce8d6 c000
    adds r1,r1,r0    @ 080ce8d8 0918
    add r1,r8                                @ 080ce8da 4144
    ldr r0,[r1,#0x0]                         @ 080ce8dc 0868
    str r0,[r4,#0x4]                         @ 080ce8de 6060
    movs r0,#0x40    @ 080ce8e0 4020
    ldrb r2,[r4,#0x15]                       @ 080ce8e2 627d
    orrs r0,r2    @ 080ce8e4 1043
    strb r0,[r4,#0x15]                       @ 080ce8e6 6075
    adds r6,#0x1    @ 080ce8e8 0136
    movs r0,#0x1    @ 080ce8ea 0120
    str r0,[sp,#0x0]                         @ 080ce8ec 0090
    .hword 0x4650    @ 080ce8ee 5046
    movs r1,#0x2    @ 080ce8f0 0221
    adds r2,r6,#0x0    @ 080ce8f2 321c
    movs r3,#0xc    @ 080ce8f4 0c23
    bl render_jp_string_to_tile_line         @ 080ce8f6 f8f7e3fe
    adds r7,r0,#0x0    @ 080ce8fa 071c
    movs r3,#0xe    @ 080ce8fc 0e23
    .hword 0x469a    @ 080ce8fe 9a46
    movs r6,#0x0    @ 080ce900 0026
LAB_080ce902:
    ldr r0, DAT_080ce9f0                     @ 080ce902 3b48
    lsls r1,r6,#0x2    @ 080ce904 b100
    adds r1,r1,r0    @ 080ce906 0918
    ldrb r1,[r1,#0x11]                       @ 080ce908 497c
    lsls r0,r1,#0x19    @ 080ce90a 4806
    cmp r0,#0x0                              @ 080ce90c 0028
    bge LAB_080ce970                         @ 080ce90e 2fda
    movs r0,#0x17    @ 080ce910 1720
    movs r1,#0x10    @ 080ce912 1021
    movs r2,#0x1    @ 080ce914 0122
    movs r3,#0x2    @ 080ce916 0223
    bl setup_line_buf_with_font_and_align    @ 080ce918 22f0d2f9
    movs r1,#0x7    @ 080ce91c 0721
    ldrb r0,[r5,#0x0]                        @ 080ce91e 2878
    ands r1,r0    @ 080ce920 0140
    rsbs r1,r1,#0    @ 080ce922 4942
    lsrs r1,r1,#0x1f    @ 080ce924 c90f
    movs r2,#0x2    @ 080ce926 0222
    rsbs r2,r2,#0    @ 080ce928 5242
    adds r0,r2,#0x0    @ 080ce92a 101c
    ldrb r3,[r4,#0x8]                        @ 080ce92c 237a
    ands r0,r3    @ 080ce92e 1840
    orrs r0,r1    @ 080ce930 0843
    movs r1,#0x2    @ 080ce932 0221
    orrs r0,r1    @ 080ce934 0843
    strb r0,[r4,#0x8]                        @ 080ce936 2072
    lsls r1,r0,#0x1e    @ 080ce938 8107
    lsrs r1,r1,#0x1f    @ 080ce93a c90f
    lsls r1,r1,#0x2    @ 080ce93c 8900
    lsls r0,r0,#0x1f    @ 080ce93e c007
    lsrs r0,r0,#0x1f    @ 080ce940 c00f
    lsls r0,r0,#0x3    @ 080ce942 c000
    adds r1,r1,r0    @ 080ce944 0918
    add r1,r8                                @ 080ce946 4144
    ldr r0,[r1,#0x0]                         @ 080ce948 0868
    str r0,[r4,#0x4]                         @ 080ce94a 6060
    movs r0,#0x40    @ 080ce94c 4020
    ldrb r1,[r4,#0x15]                       @ 080ce94e 617d
    orrs r0,r1    @ 080ce950 0843
    strb r0,[r4,#0x15]                       @ 080ce952 6075
    lsls r2,r6,#0x9    @ 080ce954 7202
    ldr r0, DAT_080ce9d0                     @ 080ce956 1e48
    adds r2,r2,r0    @ 080ce958 1218
    movs r0,#0x1    @ 080ce95a 0120
    str r0,[sp,#0x0]                         @ 080ce95c 0090
    .hword 0x4650    @ 080ce95e 5046
    movs r1,#0x0    @ 080ce960 0021
    movs r3,#0xc    @ 080ce962 0c23
    bl render_jp_string_to_tile_line         @ 080ce964 f8f7acfe
    adds r7,r7,r0    @ 080ce968 3f18
    cmp r0,r9                                @ 080ce96a 4845
    ble LAB_080ce970                         @ 080ce96c 00dd
    .hword 0x4681    @ 080ce96e 8146
LAB_080ce970:
    adds r6,#0x1    @ 080ce970 0136
    cmp r6,#0x3                              @ 080ce972 032e
    ble LAB_080ce902                         @ 080ce974 c5dd
    adds r0,r7,#0x0    @ 080ce976 381c
    cmp r7,#0x0                              @ 080ce978 002f
    bge LAB_080ce97e                         @ 080ce97a 00da
    adds r0,r7,#0x7    @ 080ce97c f81d
LAB_080ce97e:
    asrs r2,r0,#0x3    @ 080ce97e c210
    movs r4,#0x7    @ 080ce980 0724
    ands r7,r4    @ 080ce982 2740
    cmp r7,#0x0                              @ 080ce984 002f
    beq LAB_080ce98a                         @ 080ce986 00d0
    adds r2,#0x1    @ 080ce988 0132
LAB_080ce98a:
    ldr r3, DAT_080ce9d4                     @ 080ce98a 124b
    ldr r0, DAT_080ce9f4                     @ 080ce98c 1948
    adds r1,r3,r0    @ 080ce98e 1918
    movs r0,#0x4    @ 080ce990 0420
    strh r0,[r1,#0x0]                        @ 080ce992 0880
    cmp r2,#0x10                             @ 080ce994 102a
    ble LAB_080cea08                         @ 080ce996 37dd
    ldr r2, DAT_080ce9f8                     @ 080ce998 174a
    adds r1,r3,r2    @ 080ce99a 9918
    movs r0,#0x1    @ 080ce99c 0120
    ldrb r2,[r1,#0x0]                        @ 080ce99e 0a78
    orrs r0,r2    @ 080ce9a0 1043
    strb r0,[r1,#0x0]                        @ 080ce9a2 0870
    .hword 0x4648    @ 080ce9a4 4846
    cmp r0,#0x0                              @ 080ce9a6 0028
    bge LAB_080ce9ac                         @ 080ce9a8 00da
    adds r0,#0x7    @ 080ce9aa 0730
LAB_080ce9ac:
    asrs r0,r0,#0x3    @ 080ce9ac c010
    ldr r2, DAT_080ce9fc                     @ 080ce9ae 134a
    adds r1,r3,r2    @ 080ce9b0 9918
    strb r0,[r1,#0x0]                        @ 080ce9b2 0870
    .hword 0x464b    @ 080ce9b4 4b46
    ands r3,r4    @ 080ce9b6 2340
    cmp r3,#0x0                              @ 080ce9b8 002b
    beq LAB_080ce9c0                         @ 080ce9ba 01d0
    adds r0,#0x1    @ 080ce9bc 0130
    strb r0,[r1,#0x0]                        @ 080ce9be 0870
LAB_080ce9c0:
    ldr r0, DAT_080cea00                     @ 080ce9c0 0f48
    ldr r1, DAT_080cea04                     @ 080ce9c2 1049
    movs r2,#0x1    @ 080ce9c4 0122
    movs r3,#0x1    @ 080ce9c6 0123
    bl tile_2d_row_copy                      @ 080ce9c8 28f084fd
    b LAB_080cea22                           @ 080ce9cc 29e0
    .zero  0x2
DAT_080ce9d0:
    .word  0x0201f641                     @ 080ce9d0 41f60102
DAT_080ce9d4:
    .word  0x0201f440                     @ 080ce9d4 40f40102
DAT_080ce9d8:
    .word  0x00000a0e                     @ 080ce9d8 0e0a0000
DAT_080ce9dc:
    .word  0xfffff00f                     @ 080ce9dc 0ff0ffff
DAT_080ce9e0:
    .word  0x02006ed0                     @ 080ce9e0 d06e0002
DAT_080ce9e4:
    .word  0x02000000                     @ 080ce9e4 00000002
DAT_080ce9e8:
    .word  0x00006c2c                     @ 080ce9e8 2c6c0000
PTR_font_jp_base_table_080ce9ec:
    .word  font_jp_base_table             @ 080ce9ec 54f8e509
DAT_080ce9f0:
    .word  0x0201e4f0                     @ 080ce9f0 f0e40102
DAT_080ce9f4:
    .word  0x00000a14                     @ 080ce9f4 140a0000
DAT_080ce9f8:
    .word  0x00000a17                     @ 080ce9f8 170a0000
DAT_080ce9fc:
    .word  0x00000a02                     @ 080ce9fc 020a0000
DAT_080cea00:
    .word  0x06010c00                     @ 080cea00 000c0106
DAT_080cea04:
    .word  0x0988ab38                     @ 080cea04 38ab8809
LAB_080cea08:
    ldr r0, DAT_080cea3c                     @ 080cea08 0c48
    adds r1,r3,r0    @ 080cea0a 1918
    movs r0,#0x2    @ 080cea0c 0220
    rsbs r0,r0,#0    @ 080cea0e 4042
    ldrb r2,[r1,#0x0]                        @ 080cea10 0a78
    ands r0,r2    @ 080cea12 1040
    strb r0,[r1,#0x0]                        @ 080cea14 0870
    ldr r0, DAT_080cea40                     @ 080cea16 0a48
    ldr r1, DAT_080cea44                     @ 080cea18 0a49
    movs r2,#0x1    @ 080cea1a 0122
    movs r3,#0x1    @ 080cea1c 0123
    bl tile_2d_row_copy                      @ 080cea1e 28f059fd
LAB_080cea22:
    ldr r0, DAT_080cea48                     @ 080cea22 0948
    ldr r3, DAT_080cea4c                     @ 080cea24 094b
    adds r0,r0,r3    @ 080cea26 c018
    movs r1,#0x3    @ 080cea28 0321
    strb r1,[r0,#0x0]                        @ 080cea2a 0170
    add sp,#0x4                              @ 080cea2c 01b0
    pop {r3,r4,r5}                           @ 080cea2e 38bc
    .hword 0x4698    @ 080cea30 9846
    .hword 0x46a1    @ 080cea32 a146
    .hword 0x46aa    @ 080cea34 aa46
    pop {r4,r5,r6,r7}                        @ 080cea36 f0bc
    pop {r0}                                 @ 080cea38 01bc
    bx r0                                    @ 080cea3a 0047
DAT_080cea3c:
    .word  0x00000a17                     @ 080cea3c 170a0000
DAT_080cea40:
    .word  0x06010c00                     @ 080cea40 000c0106
DAT_080cea44:
    .word  0x0988ab18                     @ 080cea44 18ab8809
DAT_080cea48:
    .word  0x0201f440                     @ 080cea48 40f40102
DAT_080cea4c:
    .word  0x00000a01                     @ 080cea4c 010a0000

@ 由 FUN_080c7ea0 (window/vram/display/card_data 全标签主控) 独占调用 (indeg=1). 初始化 JP 文字渲染缓冲区 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); 读取状态结构体 (0x0201f440 + 0x0a16) 的 bit[0..2] 判断当前语言/模式标志, 选择对应的 font_jp_base_table 条目; 然后循环遍历 card entry 表 (0x0201e4f0, 每条 4 字节, r5 in [0..3]) 逐条调用 render_jp_string_to_tile_line 将 JP 文字渲染到 BG tile 缓冲; 完成后调用 write_line_buf_to_bg_tile_vram 将缓冲写入 BG tile VRAM. Constants: STATE_BASE=0x0201f440, OFFSET_LANG_FLAG=0x0a16, CARD_ENTRY_TABLE=0x0201e4f0, VRAM_BG=0x06014000, LOOP_RANGE=[0..3].
render_card_entry_jp_labels_to_bg:
    push {r4,r5,r6,r7,lr}                    @ 080cea50 f0b5
    .hword 0x4657    @ 080cea52 5746
    .hword 0x464e    @ 080cea54 4e46
    .hword 0x4645    @ 080cea56 4546
    push {r5,r6,r7}                          @ 080cea58 e0b4
    sub sp,#0x4                              @ 080cea5a 81b0
    movs r0,#0x2    @ 080cea5c 0220
    .hword 0x4682    @ 080cea5e 8246
    movs r1,#0x0    @ 080cea60 0021
    .hword 0x4688    @ 080cea62 8846
    movs r0,#0x17    @ 080cea64 1720
    movs r1,#0x10    @ 080cea66 1021
    movs r2,#0x1    @ 080cea68 0122
    movs r3,#0x2    @ 080cea6a 0223
    bl setup_line_buf_with_font_and_align    @ 080cea6c 22f028f9
    ldr r2, DAT_080ceb48                     @ 080cea70 354a
    ldr r0, DAT_080ceb4c                     @ 080cea72 3648
    ldr r3, DAT_080ceb50                     @ 080cea74 364b
    adds r0,r0,r3    @ 080cea76 c018
    movs r1,#0x7    @ 080cea78 0721
    ldrb r0,[r0,#0x0]                        @ 080cea7a 0078
    ands r1,r0    @ 080cea7c 0140
    rsbs r1,r1,#0    @ 080cea7e 4942
    lsrs r1,r1,#0x1f    @ 080cea80 c90f
    movs r0,#0x2    @ 080cea82 0220
    rsbs r0,r0,#0    @ 080cea84 4042
    ldrb r7,[r2,#0x8]                        @ 080cea86 177a
    ands r0,r7    @ 080cea88 3840
    orrs r0,r1    @ 080cea8a 0843
    movs r1,#0x2    @ 080cea8c 0221
    orrs r0,r1    @ 080cea8e 0843
    strb r0,[r2,#0x8]                        @ 080cea90 1072
    ldr r3, PTR_font_jp_base_table_080ceb54  @ 080cea92 304b
    lsls r1,r0,#0x1e    @ 080cea94 8107
    lsrs r1,r1,#0x1f    @ 080cea96 c90f
    lsls r1,r1,#0x2    @ 080cea98 8900
    lsls r0,r0,#0x1f    @ 080cea9a c007
    lsrs r0,r0,#0x1f    @ 080cea9c c00f
    lsls r0,r0,#0x3    @ 080cea9e c000
    adds r1,r1,r0    @ 080ceaa0 0918
    adds r1,r1,r3    @ 080ceaa2 c918
    ldr r0,[r1,#0x0]                         @ 080ceaa4 0868
    str r0,[r2,#0x4]                         @ 080ceaa6 5060
    movs r0,#0x40    @ 080ceaa8 4020
    ldrb r1,[r2,#0x15]                       @ 080ceaaa 517d
    orrs r0,r1    @ 080ceaac 0843
    strb r0,[r2,#0x15]                       @ 080ceaae 5075
    ldr r7, DAT_080ceb58                     @ 080ceab0 294f
    .hword 0x4642    @ 080ceab2 4246
    str r2,[sp,#0x0]                         @ 080ceab4 0092
    movs r0,#0x2    @ 080ceab6 0220
    movs r1,#0x2    @ 080ceab8 0221
    adds r2,r7,#0x0    @ 080ceaba 3a1c
    movs r3,#0xc    @ 080ceabc 0c23
    bl render_jp_string_to_tile_line         @ 080ceabe f8f7fffd
    adds r4,r0,#0x0    @ 080ceac2 041c
    adds r6,r4,#0x0    @ 080ceac4 261c
    ldr r3, DAT_080ceb5c                     @ 080ceac6 254b
    adds r5,r7,r3    @ 080ceac8 fd18
    movs r0,#0x1    @ 080ceaca 0120
    .hword 0x4681    @ 080ceacc 8146
    ldrb r1,[r5,#0x0]                        @ 080ceace 2978
    ands r0,r1    @ 080cead0 0840
    cmp r0,#0x0                              @ 080cead2 0028
    bne LAB_080ceb78                         @ 080cead4 50d1
    movs r5,#0x0    @ 080cead6 0025
    movs r6,#0x0    @ 080cead8 0026
LAB_080ceada:
    ldr r0, DAT_080ceb60                     @ 080ceada 2148
    lsls r1,r5,#0x2    @ 080ceadc a900
    adds r1,r1,r0    @ 080ceade 0918
    ldrb r1,[r1,#0x11]                       @ 080ceae0 497c
    lsls r0,r1,#0x19    @ 080ceae2 4806
    cmp r0,#0x0                              @ 080ceae4 0028
    bge LAB_080ceb18                         @ 080ceae6 17da
    ldr r3, DAT_080ceb64                     @ 080ceae8 1e4b
    ldr r2, DAT_080ceb68                     @ 080ceaea 1f4a
    adds r0,r3,r2    @ 080ceaec 9818
    ldrh r7,[r0,#0x0]                        @ 080ceaee 0788
    cmp r7,#0x4                              @ 080ceaf0 042f
    bne LAB_080ceaf6                         @ 080ceaf2 00d1
    strh r5,[r0,#0x0]                        @ 080ceaf4 0580
LAB_080ceaf6:
    lsls r0,r5,#0x1    @ 080ceaf6 6800
    ldr r2, DAT_080ceb6c                     @ 080ceaf8 1c4a
    adds r1,r3,r2    @ 080ceafa 9918
    adds r0,r0,r1    @ 080ceafc 4018
    strh r4,[r0,#0x0]                        @ 080ceafe 0480
    lsls r2,r5,#0x9    @ 080ceb00 6a02
    ldr r7, DAT_080ceb70                     @ 080ceb02 1b4f
    adds r0,r3,r7    @ 080ceb04 d819
    adds r2,r2,r0    @ 080ceb06 1218
    str r6,[sp,#0x0]                         @ 080ceb08 0096
    .hword 0x4650    @ 080ceb0a 5046
    adds r0,#0xc    @ 080ceb0c 0c30
    adds r1,r4,#0x0    @ 080ceb0e 211c
    movs r3,#0xc    @ 080ceb10 0c23
    bl render_jp_string_to_tile_line         @ 080ceb12 f8f7d5fd
    adds r4,r0,#0x0    @ 080ceb16 041c
LAB_080ceb18:
    adds r5,#0x1    @ 080ceb18 0135
    cmp r5,#0x3                              @ 080ceb1a 032d
    ble LAB_080ceada                         @ 080ceb1c dddd
    subs r4,#0x2    @ 080ceb1e 023c
    ldr r0, DAT_080ceb74                     @ 080ceb20 1448
    movs r1,#0x0    @ 080ceb22 0021
    bl write_line_buf_to_bg_tile_vram        @ 080ceb24 24f056fe
    adds r4,#0x10    @ 080ceb28 1034
    adds r0,r4,#0x0    @ 080ceb2a 201c
    cmp r4,#0x0                              @ 080ceb2c 002c
    bge LAB_080ceb32                         @ 080ceb2e 00da
    adds r0,r4,#0x7    @ 080ceb30 e01d
LAB_080ceb32:
    asrs r0,r0,#0x3    @ 080ceb32 c010
    .hword 0x4680    @ 080ceb34 8046
    movs r0,#0x7    @ 080ceb36 0720
    ands r0,r4    @ 080ceb38 2040
    cmp r0,#0x0                              @ 080ceb3a 0028
    bne LAB_080ceb40                         @ 080ceb3c 00d1
    b LAB_080ceca0                           @ 080ceb3e afe0
LAB_080ceb40:
    movs r0,#0x1    @ 080ceb40 0120
    add r8,r0                                @ 080ceb42 8044
    b LAB_080ceca0                           @ 080ceb44 ace0
    .zero  0x2
DAT_080ceb48:
    .word  0x02006ed0                     @ 080ceb48 d06e0002
DAT_080ceb4c:
    .word  0x02000000                     @ 080ceb4c 00000002
DAT_080ceb50:
    .word  0x00006c2c                     @ 080ceb50 2c6c0000
PTR_font_jp_base_table_080ceb54:
    .word  font_jp_base_table             @ 080ceb54 54f8e509
DAT_080ceb58:
    .word  0x0201f441                     @ 080ceb58 41f40102
DAT_080ceb5c:
    .word  0x00000a16                     @ 080ceb5c 160a0000
DAT_080ceb60:
    .word  0x0201e4f0                     @ 080ceb60 f0e40102
DAT_080ceb64:
    .word  0x0201f440                     @ 080ceb64 40f40102
DAT_080ceb68:
    .word  0x00000a14                     @ 080ceb68 140a0000
DAT_080ceb6c:
    .word  0x00000a04                     @ 080ceb6c 040a0000
DAT_080ceb70:
    .word  0x00000201                     @ 080ceb70 01020000
DAT_080ceb74:
    .word  0x06014000                     @ 080ceb74 00400106
LAB_080ceb78:
    ldr r0, DAT_080cecd4                     @ 080ceb78 5648
    movs r1,#0x0    @ 080ceb7a 0021
    bl write_line_buf_to_bg_tile_vram        @ 080ceb7c 24f02afe
    ldrb r5,[r5,#0x0]                        @ 080ceb80 2d78
    lsrs r2,r5,#0x1    @ 080ceb82 6a08
    ldr r3, DAT_080cecd8                     @ 080ceb84 544b
    adds r1,r7,r3    @ 080ceb86 f918
    .hword 0x4648    @ 080ceb88 4846
    ldrb r1,[r1,#0x0]                        @ 080ceb8a 0978
    ands r0,r1    @ 080ceb8c 0840
    lsls r0,r0,#0x7    @ 080ceb8e c001
    orrs r0,r2    @ 080ceb90 1043
    cmp r0,#0x0                              @ 080ceb92 0028
    bne LAB_080cec04                         @ 080ceb94 36d1
    movs r5,#0x0    @ 080ceb96 0025
    subs r0,r7,#0x1    @ 080ceb98 781e
    .hword 0x4680    @ 080ceb9a 8046
    adds r3,r4,#0x0    @ 080ceb9c 231c
    adds r3,#0x18    @ 080ceb9e 1833
    ldr r2, DAT_080cecdc                     @ 080ceba0 4e4a
    ldr r0, DAT_080cece0                     @ 080ceba2 4f48
    adds r1,r7,r0    @ 080ceba4 3918
    ldr r4, DAT_080cece4                     @ 080ceba6 4f4c
LAB_080ceba8:
    strh r6,[r1,#0x0]                        @ 080ceba8 0e80
    ldrb r7,[r2,#0x11]                       @ 080cebaa 577c
    lsls r0,r7,#0x19    @ 080cebac 7806
    cmp r0,#0x0                              @ 080cebae 0028
    bge LAB_080cebbe                         @ 080cebb0 05da
    .hword 0x4647    @ 080cebb2 4746
    adds r0,r7,r4    @ 080cebb4 3819
    ldrh r7,[r0,#0x0]                        @ 080cebb6 0788
    cmp r7,#0x4                              @ 080cebb8 042f
    bne LAB_080cebbe                         @ 080cebba 00d1
    strh r5,[r0,#0x0]                        @ 080cebbc 0580
LAB_080cebbe:
    adds r2,#0x4    @ 080cebbe 0432
    adds r1,#0x2    @ 080cebc0 0231
    adds r5,#0x1    @ 080cebc2 0135
    cmp r5,#0x3                              @ 080cebc4 032d
    ble LAB_080ceba8                         @ 080cebc6 efdd
    adds r0,r3,#0x0    @ 080cebc8 181c
    cmp r0,#0x0                              @ 080cebca 0028
    bge LAB_080cebd2                         @ 080cebcc 01da
    adds r0,r6,#0x0    @ 080cebce 301c
    adds r0,#0x1f    @ 080cebd0 1f30
LAB_080cebd2:
    asrs r0,r0,#0x3    @ 080cebd2 c010
    .hword 0x4680    @ 080cebd4 8046
    movs r1,#0x7    @ 080cebd6 0721
    ands r1,r6    @ 080cebd8 3140
    cmp r1,#0x0                              @ 080cebda 0029
    beq LAB_080cebe2                         @ 080cebdc 01d0
    movs r0,#0x1    @ 080cebde 0120
    add r8,r0                                @ 080cebe0 8044
LAB_080cebe2:
    ldr r0, DAT_080cece8                     @ 080cebe2 4148
    ldr r3, DAT_080cecec                     @ 080cebe4 414b
    adds r2,r0,r3    @ 080cebe6 c218
    ldrb r7,[r2,#0x0]                        @ 080cebe8 1778
    add r8,r7                                @ 080cebea b844
    movs r0,#0x1    @ 080cebec 0120
    add r8,r0                                @ 080cebee 8044
    adds r0,r6,#0x0    @ 080cebf0 301c
    cmp r0,#0x0                              @ 080cebf2 0028
    bge LAB_080cebf8                         @ 080cebf4 00da
    adds r0,#0x7    @ 080cebf6 0730
LAB_080cebf8:
    asrs r0,r0,#0x3    @ 080cebf8 c010
    strb r0,[r2,#0x0]                        @ 080cebfa 1070
    cmp r1,#0x0                              @ 080cebfc 0029
    beq LAB_080cec04                         @ 080cebfe 01d0
    adds r0,#0x1    @ 080cec00 0130
    strb r0,[r2,#0x0]                        @ 080cec02 1070
LAB_080cec04:
    ldr r5, DAT_080cece8                     @ 080cec04 384d
    ldr r1, DAT_080cecec                     @ 080cec06 3949
    adds r7,r5,r1    @ 080cec08 6f18
    movs r1,#0x10    @ 080cec0a 1021
    ldrb r2,[r7,#0x0]                        @ 080cec0c 3a78
    subs r1,r1,r2    @ 080cec0e 891a
    movs r0,#0x17    @ 080cec10 1720
    movs r2,#0x1    @ 080cec12 0122
    movs r3,#0x2    @ 080cec14 0223
    bl setup_line_buf_with_font_and_align    @ 080cec16 22f053f8
    ldr r2, DAT_080cecf0                     @ 080cec1a 354a
    ldr r0, DAT_080cecf4                     @ 080cec1c 3548
    ldr r3, DAT_080cecf8                     @ 080cec1e 364b
    adds r0,r0,r3    @ 080cec20 c018
    movs r6,#0x7    @ 080cec22 0726
    adds r1,r6,#0x0    @ 080cec24 311c
    ldrb r0,[r0,#0x0]                        @ 080cec26 0078
    ands r1,r0    @ 080cec28 0140
    rsbs r1,r1,#0    @ 080cec2a 4942
    lsrs r1,r1,#0x1f    @ 080cec2c c90f
    movs r0,#0x2    @ 080cec2e 0220
    rsbs r0,r0,#0    @ 080cec30 4042
    ldrb r3,[r2,#0x8]                        @ 080cec32 137a
    ands r0,r3    @ 080cec34 1840
    orrs r0,r1    @ 080cec36 0843
    movs r1,#0x2    @ 080cec38 0221
    orrs r0,r1    @ 080cec3a 0843
    strb r0,[r2,#0x8]                        @ 080cec3c 1072
    ldr r3, PTR_font_jp_base_table_080cecfc  @ 080cec3e 2f4b
    lsls r1,r0,#0x1e    @ 080cec40 8107
    lsrs r1,r1,#0x1f    @ 080cec42 c90f
    lsls r1,r1,#0x2    @ 080cec44 8900
    lsls r0,r0,#0x1f    @ 080cec46 c007
    lsrs r0,r0,#0x1f    @ 080cec48 c00f
    lsls r0,r0,#0x3    @ 080cec4a c000
    adds r1,r1,r0    @ 080cec4c 0918
    adds r1,r1,r3    @ 080cec4e c918
    ldr r0,[r1,#0x0]                         @ 080cec50 0868
    str r0,[r2,#0x4]                         @ 080cec52 5060
    movs r0,#0x40    @ 080cec54 4020
    ldrb r1,[r2,#0x15]                       @ 080cec56 517d
    orrs r0,r1    @ 080cec58 0843
    strb r0,[r2,#0x15]                       @ 080cec5a 5075
    ldr r2, DAT_080cece4                     @ 080cec5c 214a
    adds r0,r5,r2    @ 080cec5e a818
    ldrh r0,[r0,#0x0]                        @ 080cec60 0088
    lsls r2,r0,#0x9    @ 080cec62 4202
    ldr r3, DAT_080ced00                     @ 080cec64 264b
    adds r0,r5,r3    @ 080cec66 e818
    adds r2,r2,r0    @ 080cec68 1218
    movs r0,#0x0    @ 080cec6a 0020
    str r0,[sp,#0x0]                         @ 080cec6c 0090
    .hword 0x4650    @ 080cec6e 5046
    movs r1,#0x2    @ 080cec70 0221
    movs r3,#0xc    @ 080cec72 0c23
    bl render_jp_string_to_tile_line         @ 080cec74 f8f724fd
    adds r4,r0,#0x0    @ 080cec78 041c
    cmp r4,#0x0                              @ 080cec7a 002c
    bge LAB_080cec80                         @ 080cec7c 00da
    adds r0,r4,#0x7    @ 080cec7e e01d
LAB_080cec80:
    asrs r0,r0,#0x3    @ 080cec80 c010
    ldr r2, DAT_080ced04                     @ 080cec82 204a
    adds r1,r5,r2    @ 080cec84 a918
    strb r0,[r1,#0x0]                        @ 080cec86 0870
    ands r4,r6    @ 080cec88 3440
    cmp r4,#0x0                              @ 080cec8a 002c
    beq LAB_080cec92                         @ 080cec8c 01d0
    adds r0,#0x1    @ 080cec8e 0130
    strb r0,[r1,#0x0]                        @ 080cec90 0870
LAB_080cec92:
    ldrb r7,[r7,#0x0]                        @ 080cec92 3f78
    lsls r0,r7,#0xa    @ 080cec94 b802
    ldr r3, DAT_080cecd4                     @ 080cec96 0f4b
    adds r0,r0,r3    @ 080cec98 c018
    movs r1,#0x0    @ 080cec9a 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cec9c 24f09afd
LAB_080ceca0:
    ldr r3, DAT_080cece8                     @ 080ceca0 114b
    ldr r7, DAT_080cecd8                     @ 080ceca2 0d4f
    adds r0,r3,r7    @ 080ceca4 d819
    ldrb r0,[r0,#0x0]                        @ 080ceca6 0078
    lsrs r2,r0,#0x1    @ 080ceca8 4208
    ldr r0, DAT_080ced08                     @ 080cecaa 1748
    adds r1,r3,r0    @ 080cecac 1918
    movs r0,#0x1    @ 080cecae 0120
    ldrb r1,[r1,#0x0]                        @ 080cecb0 0978
    ands r0,r1    @ 080cecb2 0840
    lsls r0,r0,#0x7    @ 080cecb4 c001
    orrs r0,r2    @ 080cecb6 1043
    cmp r0,#0x0                              @ 080cecb8 0028
    bne LAB_080cecc4                         @ 080cecba 03d1
    ldr r1, DAT_080cece0                     @ 080cecbc 0849
    adds r0,r3,r1    @ 080cecbe 5818
    .hword 0x4642    @ 080cecc0 4246
    strb r2,[r0,#0x0]                        @ 080cecc2 0270
LAB_080cecc4:
    add sp,#0x4                              @ 080cecc4 01b0
    pop {r3,r4,r5}                           @ 080cecc6 38bc
    .hword 0x4698    @ 080cecc8 9846
    .hword 0x46a1    @ 080cecca a146
    .hword 0x46aa    @ 080ceccc aa46
    pop {r4,r5,r6,r7}                        @ 080cecce f0bc
    pop {r0}                                 @ 080cecd0 01bc
    bx r0                                    @ 080cecd2 0047
DAT_080cecd4:
    .word  0x06014000                     @ 080cecd4 00400106
DAT_080cecd8:
    .word  0x00000a17                     @ 080cecd8 170a0000
DAT_080cecdc:
    .word  0x0201e4f0                     @ 080cecdc f0e40102
DAT_080cece0:
    .word  0x00000a03                     @ 080cece0 030a0000
DAT_080cece4:
    .word  0x00000a14                     @ 080cece4 140a0000
DAT_080cece8:
    .word  0x0201f440                     @ 080cece8 40f40102
DAT_080cecec:
    .word  0x00000a02                     @ 080cecec 020a0000
DAT_080cecf0:
    .word  0x02006ed0                     @ 080cecf0 d06e0002
DAT_080cecf4:
    .word  0x02000000                     @ 080cecf4 00000002
DAT_080cecf8:
    .word  0x00006c2c                     @ 080cecf8 2c6c0000
PTR_font_jp_base_table_080cecfc:
    .word  font_jp_base_table             @ 080cecfc 54f8e509
DAT_080ced00:
    .word  0x00000201                     @ 080ced00 01020000
DAT_080ced04:
    .word  0x00000a16                     @ 080ced04 160a0000
DAT_080ced08:
    .word  0x00000a18                     @ 080ced08 180a0000

@ Card-list OAM row render branch for cursor_slot variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 3. Reads gFontState[0x0a03] row count; OAM Y = (10-row/2)*8. Reads gFontState[0x0a1b] bits[1:0] slot_state; if >1 exits. Checks gFontState[0x0a1c] bit0 cursor active flag; if 0 checks cursor max. When active: reads gFontState[0x0a0e] halfword+r5 as Y coord (attr0=0x88); calls write_oam_entry_from_packed_args (slot=0x60). If cursor Y exceeds max: calls write_oam_entry_with_slot_check (attr2=0x4000) for overflow row. No APCS inputs. Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; SLOT_STATE_OFFSET=0x0a1b [0..1]; ACTIVE_FLAG_OFFSET=0x0a1c bit0; CURSOR_MAX_OFFSET=0x0a10; ATTR0_CURSOR=0x88; ATTR2_OVERFLOW=0x4000; OAM_SLOT=0x60.
render_card_list_oam_row_by_cursor_slot:
    push {r4,r5,r6,r7,lr}                    @ 080ced0c f0b5
    ldr r4, DAT_080ced90                     @ 080ced0e 204c
    ldr r0, DAT_080ced94                     @ 080ced10 2048
    adds r7,r4,r0    @ 080ced12 2718
    ldrb r5,[r7,#0x0]                        @ 080ced14 3d78
    lsrs r1,r5,#0x1    @ 080ced16 6908
    movs r0,#0xa    @ 080ced18 0a20
    subs r0,r0,r1    @ 080ced1a 401a
    lsls r5,r0,#0x3    @ 080ced1c c500
    adds r3,r5,#0x0    @ 080ced1e 2b1c
    ldr r1, DAT_080ced98                     @ 080ced20 1d49
    adds r0,r4,r1    @ 080ced22 6018
    ldrb r0,[r0,#0x0]                        @ 080ced24 0078
    lsrs r0,r0,#0x1    @ 080ced26 4008
    movs r1,#0x3    @ 080ced28 0321
    ands r0,r1    @ 080ced2a 0840
    cmp r0,#0x1                              @ 080ced2c 0128
    bhi LAB_080cedc6                         @ 080ced2e 4ad8
    ldr r0, DAT_080ced9c                     @ 080ced30 1a48
    adds r1,r4,r0    @ 080ced32 2118
    movs r0,#0x1    @ 080ced34 0120
    ldrb r1,[r1,#0x0]                        @ 080ced36 0978
    ands r0,r1    @ 080ced38 0840
    cmp r0,#0x0                              @ 080ced3a 0028
    beq LAB_080ceda4                         @ 080ced3c 32d0
    movs r1,#0xa1    @ 080ced3e a121
    lsls r1,r1,#0x4    @ 080ced40 0901
    adds r6,r4,r1    @ 080ced42 6618
    ldr r0,[r6,#0x0]                         @ 080ced44 3068
    cmp r0,#0x0                              @ 080ced46 0028
    beq LAB_080ced60                         @ 080ced48 0ad0
    subs r1,#0xc    @ 080ced4a 0c39
    adds r0,r4,r1    @ 080ced4c 6018
    ldrh r0,[r0,#0x0]                        @ 080ced4e 0088
    adds r0,r0,r5    @ 080ced50 4019
    lsls r0,r0,#0x10    @ 080ced52 0004
    movs r1,#0x88    @ 080ced54 8821
    orrs r0,r1    @ 080ced56 0843
    movs r1,#0x0    @ 080ced58 0021
    movs r2,#0x60    @ 080ced5a 6022
    bl write_oam_entry_from_packed_args      @ 080ced5c 27f006fa
LAB_080ced60:
    ldr r1, DAT_080ceda0                     @ 080ced60 0f49
    adds r0,r4,r1    @ 080ced62 6018
    ldrh r0,[r0,#0x0]                        @ 080ced64 0088
    lsls r0,r0,#0x14    @ 080ced66 0005
    lsrs r0,r0,#0x18    @ 080ced68 000e
    subs r0,#0x1    @ 080ced6a 0138
    ldr r1,[r6,#0x0]                         @ 080ced6c 3168
    cmp r1,r0                                @ 080ced6e 8142
    bcs LAB_080cedc6                         @ 080ced70 29d2
    ldrb r0,[r7,#0x0]                        @ 080ced72 3878
    subs r0,#0x3    @ 080ced74 0338
    lsls r0,r0,#0x3    @ 080ced76 c000
    adds r0,r5,r0    @ 080ced78 2818
    lsls r0,r0,#0x10    @ 080ced7a 0004
    movs r1,#0x88    @ 080ced7c 8821
    orrs r0,r1    @ 080ced7e 0843
    movs r3,#0x80    @ 080ced80 8023
    lsls r3,r3,#0x6    @ 080ced82 9b01
    movs r1,#0x0    @ 080ced84 0021
    movs r2,#0x60    @ 080ced86 6022
    bl write_oam_entry_with_slot_check       @ 080ced88 27f034fd
    b LAB_080cedc6                           @ 080ced8c 1be0
    .zero  0x2
DAT_080ced90:
    .word  0x0201f440                     @ 080ced90 40f40102
DAT_080ced94:
    .word  0x00000a03                     @ 080ced94 030a0000
DAT_080ced98:
    .word  0x00000a1b                     @ 080ced98 1b0a0000
DAT_080ced9c:
    .word  0x00000a17                     @ 080ced9c 170a0000
DAT_080ceda0:
    .word  0x00000a0e                     @ 080ceda0 0e0a0000
LAB_080ceda4:
    movs r2,#0x34    @ 080ceda4 3422
    ldr r5, DAT_080cedcc                     @ 080ceda6 094d
    adds r0,r4,r5    @ 080ceda8 6019
    ldrh r0,[r0,#0x0]                        @ 080cedaa 0088
    lsls r0,r0,#0x1    @ 080cedac 4000
    subs r5,#0x10    @ 080cedae 103d
    adds r1,r4,r5    @ 080cedb0 6119
    adds r0,r0,r1    @ 080cedb2 4018
    ldrh r0,[r0,#0x0]                        @ 080cedb4 0088
    adds r0,r0,r3    @ 080cedb6 c018
    adds r0,#0x2    @ 080cedb8 0230
    lsls r0,r0,#0x10    @ 080cedba 0004
    orrs r0,r2    @ 080cedbc 1043
    movs r1,#0x0    @ 080cedbe 0021
    movs r2,#0x60    @ 080cedc0 6022
    bl write_oam_entry_from_packed_args      @ 080cedc2 27f0d3f9
LAB_080cedc6:
    pop {r4,r5,r6,r7}                        @ 080cedc6 f0bc
    pop {r0}                                 @ 080cedc8 01bc
    bx r0                                    @ 080cedca 0047
DAT_080cedcc:
    .word  0x00000a14                     @ 080cedcc 140a0000

@ Card-list OAM row render branch for JP font row type. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) for a matching case. Reads gFontState[0x0a03] JP row count; OAM Y = (10 - row/2) * 8. Checks gFontState[0x0a17] bit0 (active flag); if 0 branches to shared exit LAB_080cf0b0. When active: reads gFontState[0x0a02] strip index; calls write_card_list_oam_row_strip (slot=0x30, x=0x1fc). Reads gFontState[0x0a18] bits[23:16]=state_val; four-way dispatch (state 0/1/2/3) for JP card name render frame phases. No APCS inputs; all values loaded from DAT addresses internally. Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; FLAG_OFFSET=0x0a17; STRIP_IDX_OFFSET=0x0a02; STATE_OFFSET=0x0a18; OAM_SLOT=0x30; X_BASE=0x1fc.
render_card_list_oam_row_by_jp_type:
    push {r4,r5,r6,r7,lr}                    @ 080cedd0 f0b5
    .hword 0x4657    @ 080cedd2 5746
    .hword 0x464e    @ 080cedd4 4e46
    .hword 0x4645    @ 080cedd6 4546
    push {r5,r6,r7}                          @ 080cedd8 e0b4
    sub sp,#0x4                              @ 080cedda 81b0
    ldr r4, DAT_080cee38                     @ 080ceddc 164c
    ldr r1, DAT_080cee3c                     @ 080cedde 1749
    adds r0,r4,r1    @ 080cede0 6018
    ldrb r3,[r0,#0x0]                        @ 080cede2 0378
    lsrs r1,r3,#0x1    @ 080cede4 5908
    movs r0,#0xa    @ 080cede6 0a20
    subs r0,r0,r1    @ 080cede8 401a
    lsls r5,r0,#0x3    @ 080cedea c500
    ldr r2, DAT_080cee40                     @ 080cedec 144a
    adds r1,r4,r2    @ 080cedee a118
    movs r0,#0x1    @ 080cedf0 0120
    .hword 0x4682    @ 080cedf2 8246
    movs r2,#0x1    @ 080cedf4 0122
    .hword 0x4691    @ 080cedf6 9146
    .hword 0x4648    @ 080cedf8 4846
    ldrb r1,[r1,#0x0]                        @ 080cedfa 0978
    ands r0,r1    @ 080cedfc 0840
    cmp r0,#0x0                              @ 080cedfe 0028
    bne LAB_080cee04                         @ 080cee00 00d1
    b LAB_080cf0b0                           @ 080cee02 55e1
LAB_080cee04:
    movs r6,#0xfe    @ 080cee04 fe26
    lsls r6,r6,#0x1    @ 080cee06 7600
    ldr r3, DAT_080cee44                     @ 080cee08 0e4b
    adds r3,r3,r4    @ 080cee0a 1b19
    .hword 0x4698    @ 080cee0c 9846
    ldrb r3,[r3,#0x0]                        @ 080cee0e 1b78
    adds r3,#0x2    @ 080cee10 0233
    movs r0,#0x30    @ 080cee12 3020
    adds r1,r5,#0x0    @ 080cee14 291c
    adds r2,r6,#0x0    @ 080cee16 321c
    bl write_card_list_oam_row_strip         @ 080cee18 f8f78afb
    ldr r0, DAT_080cee48                     @ 080cee1c 0a48
    adds r7,r4,r0    @ 080cee1e 2718
    ldr r0,[r7,#0x0]                         @ 080cee20 3868
    lsls r0,r0,#0xf    @ 080cee22 c003
    lsrs r0,r0,#0x18    @ 080cee24 000e
    cmp r0,#0x1                              @ 080cee26 0128
    bne LAB_080cee2c                         @ 080cee28 00d1
    b LAB_080cef50                           @ 080cee2a 91e0
LAB_080cee2c:
    cmp r0,#0x1                              @ 080cee2c 0128
    bgt LAB_080cee4c                         @ 080cee2e 0ddc
    cmp r0,#0x0                              @ 080cee30 0028
    beq LAB_080cee5a                         @ 080cee32 12d0
    b LAB_080cf238                           @ 080cee34 00e2
    .zero  0x2
DAT_080cee38:
    .word  0x0201f440                     @ 080cee38 40f40102
DAT_080cee3c:
    .word  0x00000a03                     @ 080cee3c 030a0000
DAT_080cee40:
    .word  0x00000a17                     @ 080cee40 170a0000
DAT_080cee44:
    .word  0x00000a02                     @ 080cee44 020a0000
DAT_080cee48:
    .word  0x00000a18                     @ 080cee48 180a0000
LAB_080cee4c:
    cmp r0,#0x2                              @ 080cee4c 0228
    bne LAB_080cee52                         @ 080cee4e 00d1
    b LAB_080cefe4                           @ 080cee50 c8e0
LAB_080cee52:
    cmp r0,#0x3                              @ 080cee52 0328
    bne LAB_080cee58                         @ 080cee54 00d1
    b LAB_080cf04c                           @ 080cee56 f9e0
LAB_080cee58:
    b LAB_080cf238                           @ 080cee58 eee1
LAB_080cee5a:
    ldr r1, DAT_080ceeb4                     @ 080cee5a 1649
    adds r0,r4,r1    @ 080cee5c 6018
    ldrh r0,[r0,#0x0]                        @ 080cee5e 0088
    adds r1,r0,r5    @ 080cee60 4119
    adds r1,#0x8    @ 080cee62 0831
    .hword 0x4643    @ 080cee64 4346
    ldrb r3,[r3,#0x0]                        @ 080cee66 1b78
    lsls r2,r3,#0x5    @ 080cee68 5a01
    adds r2,r2,r6    @ 080cee6a 9219
    ldr r5, DAT_080ceeb8                     @ 080cee6c 124d
    adds r0,r4,r5    @ 080cee6e 6019
    ldrb r3,[r0,#0x0]                        @ 080cee70 0378
    adds r3,#0x2    @ 080cee72 0233
    movs r0,#0x30    @ 080cee74 3020
    bl write_card_list_oam_row_strip         @ 080cee76 f8f75bfb
    ldr r0, PTR_gPrng_080ceebc               @ 080cee7a 1048
    movs r1,#0xa4    @ 080cee7c a421
    lsls r1,r1,#0x1    @ 080cee7e 4900
    adds r0,r0,r1    @ 080cee80 4018
    ldrh r1,[r0,#0x0]                        @ 080cee82 0188
    .hword 0x4648    @ 080cee84 4846
    ands r0,r1    @ 080cee86 0840
    cmp r0,#0x0                              @ 080cee88 0028
    beq LAB_080ceecc                         @ 080cee8a 1fd0
    ldr r0, PTR_gP1LifePoints_080ceec0       @ 080cee8c 0c48
    movs r2,#0xea    @ 080cee8e ea22
    lsls r2,r2,#0x5    @ 080cee90 5201
    adds r0,r0,r2    @ 080cee92 8018
    ldr r3, DAT_080ceec4                     @ 080cee94 0b4b
    adds r1,r4,r3    @ 080cee96 e118
    ldrh r1,[r1,#0x0]                        @ 080cee98 0988
    str r1,[r0,#0x0]                         @ 080cee9a 0160
    movs r0,#0x24    @ 080cee9c 2420
    bl sync_state_and_init_sprite            @ 080cee9e 2af009fe
    ldr r0,[r7,#0x0]                         @ 080ceea2 3868
    ldr r1, DAT_080ceec8                     @ 080ceea4 0849
    ands r0,r1    @ 080ceea6 0840
    movs r1,#0xc0    @ 080ceea8 c021
    lsls r1,r1,#0x3    @ 080ceeaa c900
LAB_080ceeac:
    orrs r0,r1    @ 080ceeac 0843
    str r0,[r7,#0x0]                         @ 080ceeae 3860
    b LAB_080cf238                           @ 080ceeb0 c2e1
    .zero  0x2
DAT_080ceeb4:
    .word  0x00000a04                     @ 080ceeb4 040a0000
DAT_080ceeb8:
    .word  0x00000a16                     @ 080ceeb8 160a0000
PTR_gPrng_080ceebc:
    .word  gPrng                          @ 080ceebc 40000003
PTR_gP1LifePoints_080ceec0:
    .word  gP1LifePoints                  @ 080ceec0 e0c40102
DAT_080ceec4:
    .word  0x00000a14                     @ 080ceec4 140a0000
DAT_080ceec8:
    .word  0xfffe01ff                     @ 080ceec8 ff01feff
LAB_080ceecc:
    movs r0,#0x2    @ 080ceecc 0220
    ands r0,r1    @ 080ceece 0840
    cmp r0,#0x0                              @ 080ceed0 0028
    beq LAB_080ceed8                         @ 080ceed2 01d0
LAB_080ceed4:
    movs r0,#0x2    @ 080ceed4 0220
    b LAB_080cf234                           @ 080ceed6 ade1
LAB_080ceed8:
    movs r0,#0x80    @ 080ceed8 8020
    ands r0,r1    @ 080ceeda 0840
    cmp r0,#0x0                              @ 080ceedc 0028
    beq LAB_080cef10                         @ 080ceede 17d0
    ldr r5, DAT_080cef08                     @ 080ceee0 094d
    adds r0,r4,r5    @ 080ceee2 6019
    ldrh r4,[r0,#0x0]                        @ 080ceee4 0488
    adds r4,#0x1    @ 080ceee6 0134
    cmp r4,#0x3                              @ 080ceee8 032c
    ble LAB_080ceeee                         @ 080ceeea 00dd
    b LAB_080cf238                           @ 080ceeec a4e1
LAB_080ceeee:
    ldr r1, DAT_080cef0c                     @ 080ceeee 0749
    lsls r0,r4,#0x2    @ 080ceef0 a000
    adds r1,r0,r1    @ 080ceef2 4118
LAB_080ceef4:
    ldrb r2,[r1,#0x11]                       @ 080ceef4 4a7c
    lsls r0,r2,#0x19    @ 080ceef6 5006
    cmp r0,#0x0                              @ 080ceef8 0028
    bge LAB_080ceefe                         @ 080ceefa 00da
    b LAB_080cf1f8                           @ 080ceefc 7ce1
LAB_080ceefe:
    adds r1,#0x4    @ 080ceefe 0431
    adds r4,#0x1    @ 080cef00 0134
    cmp r4,#0x3                              @ 080cef02 032c
    ble LAB_080ceef4                         @ 080cef04 f6dd
    b LAB_080cf238                           @ 080cef06 97e1
DAT_080cef08:
    .word  0x00000a14                     @ 080cef08 140a0000
DAT_080cef0c:
    .word  0x0201e4f0                     @ 080cef0c f0e40102
LAB_080cef10:
    movs r0,#0x40    @ 080cef10 4020
    ands r0,r1    @ 080cef12 0840
    cmp r0,#0x0                              @ 080cef14 0028
    bne LAB_080cef1a                         @ 080cef16 00d1
    b LAB_080cf238                           @ 080cef18 8ee1
LAB_080cef1a:
    ldr r3, DAT_080cef48                     @ 080cef1a 0b4b
    adds r0,r4,r3    @ 080cef1c e018
    ldrh r0,[r0,#0x0]                        @ 080cef1e 0088
    subs r0,#0x1    @ 080cef20 0138
    lsls r0,r0,#0x10    @ 080cef22 0004
    asrs r4,r0,#0x10    @ 080cef24 0414
    cmp r4,#0x0                              @ 080cef26 002c
    bge LAB_080cef2c                         @ 080cef28 00da
    b LAB_080cf238                           @ 080cef2a 85e1
LAB_080cef2c:
    ldr r1, DAT_080cef4c                     @ 080cef2c 0749
    lsls r0,r4,#0x2    @ 080cef2e a000
    adds r1,r0,r1    @ 080cef30 4118
LAB_080cef32:
    ldrb r5,[r1,#0x11]                       @ 080cef32 4d7c
    lsls r0,r5,#0x19    @ 080cef34 6806
    cmp r0,#0x0                              @ 080cef36 0028
    bge LAB_080cef3c                         @ 080cef38 00da
    b LAB_080cf20c                           @ 080cef3a 67e1
LAB_080cef3c:
    subs r1,#0x4    @ 080cef3c 0439
    subs r4,#0x1    @ 080cef3e 013c
    cmp r4,#0x0                              @ 080cef40 002c
    bge LAB_080cef32                         @ 080cef42 f6da
    b LAB_080cf238                           @ 080cef44 78e1
    .zero  0x2
DAT_080cef48:
    .word  0x00000a14                     @ 080cef48 140a0000
DAT_080cef4c:
    .word  0x0201e4f0                     @ 080cef4c f0e40102
LAB_080cef50:
    movs r1,#0x10    @ 080cef50 1021
    .hword 0x4640    @ 080cef52 4046
    ldrb r0,[r0,#0x0]                        @ 080cef54 0078
    subs r1,r1,r0    @ 080cef56 091a
    movs r0,#0x17    @ 080cef58 1720
    movs r2,#0x1    @ 080cef5a 0122
    movs r3,#0x2    @ 080cef5c 0223
    bl setup_line_buf_with_font_and_align    @ 080cef5e 21f0affe
    ldr r2, DAT_080cefcc                     @ 080cef62 1a4a
    ldr r0, DAT_080cefd0                     @ 080cef64 1a48
    ldr r1, DAT_080cefd4                     @ 080cef66 1b49
    adds r0,r0,r1    @ 080cef68 4018
    movs r1,#0x7    @ 080cef6a 0721
    ldrb r0,[r0,#0x0]                        @ 080cef6c 0078
    ands r1,r0    @ 080cef6e 0140
    rsbs r1,r1,#0    @ 080cef70 4942
    lsrs r1,r1,#0x1f    @ 080cef72 c90f
    .hword 0x4653    @ 080cef74 5346
    ands r1,r3    @ 080cef76 1940
    movs r0,#0x2    @ 080cef78 0220
    rsbs r0,r0,#0    @ 080cef7a 4042
    ldrb r5,[r2,#0x8]                        @ 080cef7c 157a
    ands r0,r5    @ 080cef7e 2840
    orrs r0,r1    @ 080cef80 0843
    movs r1,#0x2    @ 080cef82 0221
    orrs r0,r1    @ 080cef84 0843
    strb r0,[r2,#0x8]                        @ 080cef86 1072
    ldr r3, PTR_font_jp_base_table_080cefd8  @ 080cef88 134b
    lsls r1,r0,#0x1e    @ 080cef8a 8107
    lsrs r1,r1,#0x1f    @ 080cef8c c90f
    lsls r1,r1,#0x2    @ 080cef8e 8900
    lsls r0,r0,#0x1f    @ 080cef90 c007
    lsrs r0,r0,#0x1f    @ 080cef92 c00f
    lsls r0,r0,#0x3    @ 080cef94 c000
    adds r1,r1,r0    @ 080cef96 0918
    adds r1,r1,r3    @ 080cef98 c918
    ldr r0,[r1,#0x0]                         @ 080cef9a 0868
    str r0,[r2,#0x4]                         @ 080cef9c 5060
    movs r0,#0x40    @ 080cef9e 4020
    ldrb r1,[r2,#0x15]                       @ 080cefa0 517d
    orrs r0,r1    @ 080cefa2 0843
    strb r0,[r2,#0x15]                       @ 080cefa4 5075
    .hword 0x4642    @ 080cefa6 4246
    ldrb r1,[r2,#0x0]                        @ 080cefa8 1178
    lsls r0,r1,#0xa    @ 080cefaa 8802
    ldr r3, DAT_080cefdc                     @ 080cefac 0b4b
    adds r0,r0,r3    @ 080cefae c018
    movs r3,#0x10    @ 080cefb0 1023
    subs r3,r3,r1    @ 080cefb2 5b1a
    lsls r3,r3,#0x10    @ 080cefb4 1b04
    lsrs r3,r3,#0x10    @ 080cefb6 1b0c
    movs r1,#0x0    @ 080cefb8 0021
    movs r2,#0x17    @ 080cefba 1722
    bl tile_2d_row_copy                      @ 080cefbc 28f08afa
    ldr r0,[r7,#0x0]                         @ 080cefc0 3868
    ldr r1, DAT_080cefe0                     @ 080cefc2 0749
    ands r0,r1    @ 080cefc4 0840
    movs r1,#0x80    @ 080cefc6 8021
    lsls r1,r1,#0x3    @ 080cefc8 c900
    b LAB_080ceeac                           @ 080cefca 6fe7
DAT_080cefcc:
    .word  0x02006ed0                     @ 080cefcc d06e0002
DAT_080cefd0:
    .word  0x02000000                     @ 080cefd0 00000002
DAT_080cefd4:
    .word  0x00006c2c                     @ 080cefd4 2c6c0000
PTR_font_jp_base_table_080cefd8:
    .word  font_jp_base_table             @ 080cefd8 54f8e509
DAT_080cefdc:
    .word  0x06014000                     @ 080cefdc 00400106
DAT_080cefe0:
    .word  0xfffe01ff                     @ 080cefe0 ff01feff
LAB_080cefe4:
    ldr r5, DAT_080cf038                     @ 080cefe4 144d
    adds r0,r4,r5    @ 080cefe6 6019
    ldrh r0,[r0,#0x0]                        @ 080cefe8 0088
    lsls r2,r0,#0x9    @ 080cefea 4202
    ldr r1, DAT_080cf03c                     @ 080cefec 1349
    adds r0,r4,r1    @ 080cefee 6018
    adds r2,r2,r0    @ 080ceff0 1218
    movs r0,#0x0    @ 080ceff2 0020
    str r0,[sp,#0x0]                         @ 080ceff4 0090
    movs r0,#0x2    @ 080ceff6 0220
    movs r1,#0x2    @ 080ceff8 0221
    movs r3,#0xc    @ 080ceffa 0c23
    bl render_jp_string_to_tile_line         @ 080ceffc f8f760fb
    adds r5,r0,#0x0    @ 080cf000 051c
    .hword 0x4642    @ 080cf002 4246
    ldrb r2,[r2,#0x0]                        @ 080cf004 1278
    lsls r0,r2,#0xa    @ 080cf006 9002
    ldr r3, DAT_080cf040                     @ 080cf008 0d4b
    adds r0,r0,r3    @ 080cf00a c018
    movs r1,#0x0    @ 080cf00c 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cf00e 24f0e1fb
    adds r0,r5,#0x0    @ 080cf012 281c
    cmp r5,#0x0                              @ 080cf014 002d
    bge LAB_080cf01a                         @ 080cf016 00da
    adds r0,r5,#0x7    @ 080cf018 e81d
LAB_080cf01a:
    asrs r2,r0,#0x3    @ 080cf01a c210
    ldr r0, DAT_080cf044                     @ 080cf01c 0948
    adds r1,r4,r0    @ 080cf01e 2118
    strb r2,[r1,#0x0]                        @ 080cf020 0a70
    movs r0,#0x7    @ 080cf022 0720
    ands r0,r5    @ 080cf024 2840
    cmp r0,#0x0                              @ 080cf026 0028
    beq LAB_080cf02e                         @ 080cf028 01d0
    adds r0,r2,#0x1    @ 080cf02a 501c
    strb r0,[r1,#0x0]                        @ 080cf02c 0870
LAB_080cf02e:
    ldr r0,[r7,#0x0]                         @ 080cf02e 3868
    ldr r1, DAT_080cf048                     @ 080cf030 0549
    ands r0,r1    @ 080cf032 0840
    str r0,[r7,#0x0]                         @ 080cf034 3860
    b LAB_080cf238                           @ 080cf036 ffe0
DAT_080cf038:
    .word  0x00000a14                     @ 080cf038 140a0000
DAT_080cf03c:
    .word  0x00000201                     @ 080cf03c 01020000
DAT_080cf040:
    .word  0x06014000                     @ 080cf040 00400106
DAT_080cf044:
    .word  0x00000a16                     @ 080cf044 160a0000
DAT_080cf048:
    .word  0xfffe01ff                     @ 080cf048 ff01feff
LAB_080cf04c:
    ldr r1, DAT_080cf0a0                     @ 080cf04c 1449
    adds r0,r4,r1    @ 080cf04e 6018
    ldrh r0,[r0,#0x0]                        @ 080cf050 0088
    adds r1,r0,r5    @ 080cf052 4119
    adds r1,#0x8    @ 080cf054 0831
    .hword 0x4643    @ 080cf056 4346
    ldrb r3,[r3,#0x0]                        @ 080cf058 1b78
    lsls r2,r3,#0x5    @ 080cf05a 5a01
    adds r2,r2,r6    @ 080cf05c 9219
    ldr r5, DAT_080cf0a4                     @ 080cf05e 114d
    adds r0,r4,r5    @ 080cf060 6019
    ldrb r3,[r0,#0x0]                        @ 080cf062 0378
    adds r3,#0x2    @ 080cf064 0233
    movs r0,#0x30    @ 080cf066 3020
    bl write_card_list_oam_row_strip         @ 080cf068 f8f762fa
    ldr r0, DAT_080cf0a8                     @ 080cf06c 0e48
    adds r6,r4,r0    @ 080cf06e 2618
    ldrb r5,[r6,#0x0]                        @ 080cf070 3578
    lsrs r0,r5,#0x1    @ 080cf072 6808
    ldr r1, DAT_080cf0ac                     @ 080cf074 0d49
    adds r4,r4,r1    @ 080cf076 6418
    .hword 0x464b    @ 080cf078 4b46
    ldrb r2,[r4,#0x0]                        @ 080cf07a 2278
    ands r3,r2    @ 080cf07c 1340
    lsls r3,r3,#0x7    @ 080cf07e db01
    orrs r3,r0    @ 080cf080 0343
    adds r2,r3,#0x1    @ 080cf082 5a1c
    movs r1,#0x7f    @ 080cf084 7f21
    ands r1,r2    @ 080cf086 1140
    lsls r1,r1,#0x1    @ 080cf088 4900
    .hword 0x4648    @ 080cf08a 4846
    ands r0,r5    @ 080cf08c 2840
    orrs r0,r1    @ 080cf08e 0843
    strb r0,[r6,#0x0]                        @ 080cf090 3070
    lsrs r2,r2,#0x7    @ 080cf092 d209
    .hword 0x464d    @ 080cf094 4d46
    ands r2,r5    @ 080cf096 2a40
    .hword 0x4650    @ 080cf098 5046
    ands r2,r0    @ 080cf09a 0240
    b LAB_080cf1da                           @ 080cf09c 9de0
    .zero  0x2
DAT_080cf0a0:
    .word  0x00000a04                     @ 080cf0a0 040a0000
DAT_080cf0a4:
    .word  0x00000a16                     @ 080cf0a4 160a0000
DAT_080cf0a8:
    .word  0x00000a1b                     @ 080cf0a8 1b0a0000
DAT_080cf0ac:
    .word  0x00000a1c                     @ 080cf0ac 1c0a0000
LAB_080cf0b0:
    movs r2,#0xfe    @ 080cf0b0 fe22
    lsls r2,r2,#0x1    @ 080cf0b2 5200
    movs r0,#0x30    @ 080cf0b4 3020
    adds r1,r5,#0x0    @ 080cf0b6 291c
    bl write_card_list_oam_row_strip         @ 080cf0b8 f8f73afa
    ldr r2, DAT_080cf0d0                     @ 080cf0bc 044a
    adds r5,r4,r2    @ 080cf0be a518
    ldr r0,[r5,#0x0]                         @ 080cf0c0 2868
    lsls r0,r0,#0xf    @ 080cf0c2 c003
    lsrs r7,r0,#0x18    @ 080cf0c4 070e
    cmp r7,#0x0                              @ 080cf0c6 002f
    beq LAB_080cf0d4                         @ 080cf0c8 04d0
    cmp r7,#0x1                              @ 080cf0ca 012f
    beq LAB_080cf1ac                         @ 080cf0cc 6ed0
    b LAB_080cf238                           @ 080cf0ce b3e0
DAT_080cf0d0:
    .word  0x00000a18                     @ 080cf0d0 180a0000
LAB_080cf0d4:
    ldr r0, PTR_gPrng_080cf10c               @ 080cf0d4 0d48
    movs r3,#0xa4    @ 080cf0d6 a423
    lsls r3,r3,#0x1    @ 080cf0d8 5b00
    adds r0,r0,r3    @ 080cf0da c018
    ldrh r1,[r0,#0x0]                        @ 080cf0dc 0188
    .hword 0x4648    @ 080cf0de 4846
    ands r0,r1    @ 080cf0e0 0840
    cmp r0,#0x0                              @ 080cf0e2 0028
    beq LAB_080cf11c                         @ 080cf0e4 1ad0
    ldr r0, PTR_gP1LifePoints_080cf110       @ 080cf0e6 0a48
    movs r1,#0xea    @ 080cf0e8 ea21
    lsls r1,r1,#0x5    @ 080cf0ea 4901
    adds r0,r0,r1    @ 080cf0ec 4018
    ldr r2, DAT_080cf114                     @ 080cf0ee 094a
    adds r1,r4,r2    @ 080cf0f0 a118
    ldrh r1,[r1,#0x0]                        @ 080cf0f2 0988
    str r1,[r0,#0x0]                         @ 080cf0f4 0160
    movs r0,#0x24    @ 080cf0f6 2420
    bl sync_state_and_init_sprite            @ 080cf0f8 2af0dcfc
    ldr r0,[r5,#0x0]                         @ 080cf0fc 2868
    ldr r1, DAT_080cf118                     @ 080cf0fe 0649
    ands r0,r1    @ 080cf100 0840
    movs r1,#0x80    @ 080cf102 8021
    lsls r1,r1,#0x2    @ 080cf104 8900
    orrs r0,r1    @ 080cf106 0843
    str r0,[r5,#0x0]                         @ 080cf108 2860
    b LAB_080cf238                           @ 080cf10a 95e0
PTR_gPrng_080cf10c:
    .word  gPrng                          @ 080cf10c 40000003
PTR_gP1LifePoints_080cf110:
    .word  gP1LifePoints                  @ 080cf110 e0c40102
DAT_080cf114:
    .word  0x00000a14                     @ 080cf114 140a0000
DAT_080cf118:
    .word  0xfffe01ff                     @ 080cf118 ff01feff
LAB_080cf11c:
    movs r0,#0x2    @ 080cf11c 0220
    ands r0,r1    @ 080cf11e 0840
    cmp r0,#0x0                              @ 080cf120 0028
    beq LAB_080cf126                         @ 080cf122 00d0
    b LAB_080ceed4                           @ 080cf124 d6e6
LAB_080cf126:
    movs r0,#0x80    @ 080cf126 8020
    ands r0,r1    @ 080cf128 0840
    cmp r0,#0x0                              @ 080cf12a 0028
    beq LAB_080cf164                         @ 080cf12c 1ad0
    ldr r3, DAT_080cf158                     @ 080cf12e 0a4b
    adds r1,r4,r3    @ 080cf130 e118
    movs r4,#0x0    @ 080cf132 0024
    ldr r3, DAT_080cf15c                     @ 080cf134 094b
    ldr r5, DAT_080cf160                     @ 080cf136 0a4d
    adds r2,r5,#0x0    @ 080cf138 2a1c
LAB_080cf13a:
    ldrh r0,[r1,#0x0]                        @ 080cf13a 0888
    adds r0,#0x1    @ 080cf13c 0130
    strh r0,[r1,#0x0]                        @ 080cf13e 0880
    ands r0,r2    @ 080cf140 1040
    cmp r0,#0x3                              @ 080cf142 0328
    bls LAB_080cf148                         @ 080cf144 00d9
    strh r4,[r1,#0x0]                        @ 080cf146 0c80
LAB_080cf148:
    ldrh r5,[r1,#0x0]                        @ 080cf148 0d88
    lsls r0,r5,#0x2    @ 080cf14a a800
    adds r0,r0,r3    @ 080cf14c c018
    ldrb r0,[r0,#0x11]                       @ 080cf14e 407c
    lsls r0,r0,#0x19    @ 080cf150 4006
    cmp r0,#0x0                              @ 080cf152 0028
    bge LAB_080cf13a                         @ 080cf154 f1da
    b LAB_080cf232                           @ 080cf156 6ce0
DAT_080cf158:
    .word  0x00000a14                     @ 080cf158 140a0000
DAT_080cf15c:
    .word  0x0201e4f0                     @ 080cf15c f0e40102
DAT_080cf160:
    .word  0x0000ffff                     @ 080cf160 ffff0000
LAB_080cf164:
    movs r0,#0x40    @ 080cf164 4020
    ands r0,r1    @ 080cf166 0840
    cmp r0,#0x0                              @ 080cf168 0028
    beq LAB_080cf238                         @ 080cf16a 65d0
    ldr r0, DAT_080cf1a0                     @ 080cf16c 0c48
    adds r1,r4,r0    @ 080cf16e 2118
    ldr r4, DAT_080cf1a4                     @ 080cf170 0c4c
    ldr r2, DAT_080cf1a8                     @ 080cf172 0d4a
    adds r3,r2,#0x0    @ 080cf174 131c
    movs r2,#0x3    @ 080cf176 0322
LAB_080cf178:
    ldrh r0,[r1,#0x0]                        @ 080cf178 0888
    subs r0,#0x1    @ 080cf17a 0138
    strh r0,[r1,#0x0]                        @ 080cf17c 0880
    ands r0,r3    @ 080cf17e 1840
    lsls r0,r0,#0x10    @ 080cf180 0004
    cmp r0,#0x0                              @ 080cf182 0028
    bge LAB_080cf188                         @ 080cf184 00da
    strh r2,[r1,#0x0]                        @ 080cf186 0a80
LAB_080cf188:
    ldrh r5,[r1,#0x0]                        @ 080cf188 0d88
    lsls r0,r5,#0x2    @ 080cf18a a800
    adds r0,r0,r4    @ 080cf18c 0019
    ldrb r0,[r0,#0x11]                       @ 080cf18e 407c
    lsls r0,r0,#0x19    @ 080cf190 4006
    cmp r0,#0x0                              @ 080cf192 0028
    bge LAB_080cf178                         @ 080cf194 f0da
    movs r0,#0x0    @ 080cf196 0020
    bl sync_state_and_init_sprite            @ 080cf198 2af08cfc
    b LAB_080cf238                           @ 080cf19c 4ce0
    .zero  0x2
DAT_080cf1a0:
    .word  0x00000a14                     @ 080cf1a0 140a0000
DAT_080cf1a4:
    .word  0x0201e4f0                     @ 080cf1a4 f0e40102
DAT_080cf1a8:
    .word  0x0000ffff                     @ 080cf1a8 ffff0000
LAB_080cf1ac:
    ldr r0, DAT_080cf1f0                     @ 080cf1ac 1048
    adds r6,r4,r0    @ 080cf1ae 2618
    ldrb r5,[r6,#0x0]                        @ 080cf1b0 3578
    lsrs r0,r5,#0x1    @ 080cf1b2 6808
    ldr r1, DAT_080cf1f4                     @ 080cf1b4 0f49
    adds r4,r4,r1    @ 080cf1b6 6418
    adds r3,r7,#0x0    @ 080cf1b8 3b1c
    ldrb r2,[r4,#0x0]                        @ 080cf1ba 2278
    ands r3,r2    @ 080cf1bc 1340
    lsls r3,r3,#0x7    @ 080cf1be db01
    orrs r3,r0    @ 080cf1c0 0343
    adds r2,r3,#0x1    @ 080cf1c2 5a1c
    movs r1,#0x7f    @ 080cf1c4 7f21
    ands r1,r2    @ 080cf1c6 1140
    lsls r1,r1,#0x1    @ 080cf1c8 4900
    adds r0,r7,#0x0    @ 080cf1ca 381c
    ands r0,r5    @ 080cf1cc 2840
    orrs r0,r1    @ 080cf1ce 0843
    strb r0,[r6,#0x0]                        @ 080cf1d0 3070
    lsrs r2,r2,#0x7    @ 080cf1d2 d209
    ands r2,r7    @ 080cf1d4 3a40
    .hword 0x4655    @ 080cf1d6 5546
    ands r2,r5    @ 080cf1d8 2a40
LAB_080cf1da:
    movs r0,#0x2    @ 080cf1da 0220
    rsbs r0,r0,#0    @ 080cf1dc 4042
    ldrb r1,[r4,#0x0]                        @ 080cf1de 2178
    ands r0,r1    @ 080cf1e0 0840
    orrs r0,r2    @ 080cf1e2 1043
    strb r0,[r4,#0x0]                        @ 080cf1e4 2070
    cmp r3,#0x1f                             @ 080cf1e6 1f2b
    bls LAB_080cf238                         @ 080cf1e8 26d9
    movs r0,#0x1    @ 080cf1ea 0120
    b LAB_080cf23a                           @ 080cf1ec 25e0
    .zero  0x2
DAT_080cf1f0:
    .word  0x00000a1b                     @ 080cf1f0 1b0a0000
DAT_080cf1f4:
    .word  0x00000a1c                     @ 080cf1f4 1c0a0000
LAB_080cf1f8:
    ldr r2, DAT_080cf208                     @ 080cf1f8 034a
    movs r3,#0xa1    @ 080cf1fa a123
    lsls r3,r3,#0x4    @ 080cf1fc 1b01
    adds r1,r2,r3    @ 080cf1fe d118
    ldr r0,[r1,#0x0]                         @ 080cf200 0868
    adds r0,#0x1    @ 080cf202 0130
    b LAB_080cf218                           @ 080cf204 08e0
    .zero  0x2
DAT_080cf208:
    .word  0x0201f440                     @ 080cf208 40f40102
LAB_080cf20c:
    ldr r2, DAT_080cf24c                     @ 080cf20c 0f4a
    movs r3,#0xa1    @ 080cf20e a123
    lsls r3,r3,#0x4    @ 080cf210 1b01
    adds r1,r2,r3    @ 080cf212 d118
    ldr r0,[r1,#0x0]                         @ 080cf214 0868
    subs r0,#0x1    @ 080cf216 0138
LAB_080cf218:
    str r0,[r1,#0x0]                         @ 080cf218 0860
    ldr r5, DAT_080cf250                     @ 080cf21a 0d4d
    adds r0,r2,r5    @ 080cf21c 5019
    strh r4,[r0,#0x0]                        @ 080cf21e 0480
    ldr r0, DAT_080cf254                     @ 080cf220 0c48
    adds r2,r2,r0    @ 080cf222 1218
    ldr r0,[r2,#0x0]                         @ 080cf224 1068
    ldr r1, DAT_080cf258                     @ 080cf226 0c49
    ands r0,r1    @ 080cf228 0840
    movs r1,#0x80    @ 080cf22a 8021
    lsls r1,r1,#0x2    @ 080cf22c 8900
    orrs r0,r1    @ 080cf22e 0843
    str r0,[r2,#0x0]                         @ 080cf230 1060
LAB_080cf232:
    movs r0,#0x0    @ 080cf232 0020
LAB_080cf234:
    bl sync_state_and_init_sprite            @ 080cf234 2af03efc
LAB_080cf238:
    movs r0,#0x0    @ 080cf238 0020
LAB_080cf23a:
    add sp,#0x4                              @ 080cf23a 01b0
    pop {r3,r4,r5}                           @ 080cf23c 38bc
    .hword 0x4698    @ 080cf23e 9846
    .hword 0x46a1    @ 080cf240 a146
    .hword 0x46aa    @ 080cf242 aa46
    pop {r4,r5,r6,r7}                        @ 080cf244 f0bc
    pop {r1}                                 @ 080cf246 02bc
    bx r1                                    @ 080cf248 0847
    .zero  0x2
DAT_080cf24c:
    .word  0x0201f440                     @ 080cf24c 40f40102
DAT_080cf250:
    .word  0x00000a14                     @ 080cf250 140a0000
DAT_080cf254:
    .word  0x00000a18                     @ 080cf254 180a0000
DAT_080cf258:
    .word  0xfffe01ff                     @ 080cf258 ff01feff

@ Render a numeric card stat (ATK/DEF/LP) as decimal digits into BG tile VRAM. Calls resolve_game_str_ptr for the stat label, then render_decimal_digits_jp to rasterize the numeric value. r0: stat_type [0..N]; r1: stat_value [0..9999]; r2: bg_tile_dest ptr; r3: x_col [0..29]. Returns void. Side effects: BG tile VRAM written with decimal digit tiles.
render_card_numeric_stat_to_bg:
    push {r4,r5,lr}                          @ 080cf25c 30b5
    ldr r4, DAT_080cf30c                     @ 080cf25e 2b4c
    ldr r1, DAT_080cf310                     @ 080cf260 2b49
    adds r0,r4,r1    @ 080cf262 6018
    ldrh r0,[r0,#0x0]                        @ 080cf264 0088
    bl resolve_game_str_ptr                  @ 080cf266 1ff0f5fc
    adds r1,r0,#0x0    @ 080cf26a 011c
    ldr r2, DAT_080cf314                     @ 080cf26c 294a
    adds r0,r4,r2    @ 080cf26e a018
    ldrh r0,[r0,#0x0]                        @ 080cf270 0088
    lsls r2,r0,#0x14    @ 080cf272 0205
    lsrs r2,r2,#0x18    @ 080cf274 120e
    ldr r3, DAT_080cf318                     @ 080cf276 284b
    adds r0,r4,r3    @ 080cf278 e018
    ldrh r0,[r0,#0x0]                        @ 080cf27a 0088
    adds r2,r0,r2    @ 080cf27c 8218
    adds r0,r4,#0x0    @ 080cf27e 201c
    bl expand_format_decimal_to_buf          @ 080cf280 25f0d2ff
    movs r0,#0x19    @ 080cf284 1920
    movs r1,#0x2    @ 080cf286 0221
    movs r2,#0x1    @ 080cf288 0122
    movs r3,#0x0    @ 080cf28a 0023
    bl setup_line_buf_with_font_and_align    @ 080cf28c 21f018fd
    ldr r2, DAT_080cf31c                     @ 080cf290 224a
    ldr r0, DAT_080cf320                     @ 080cf292 2348
    ldr r1, DAT_080cf324                     @ 080cf294 2349
    adds r0,r0,r1    @ 080cf296 4018
    movs r1,#0x7    @ 080cf298 0721
    ldrb r0,[r0,#0x0]                        @ 080cf29a 0078
    ands r1,r0    @ 080cf29c 0140
    rsbs r1,r1,#0    @ 080cf29e 4942
    lsrs r1,r1,#0x1f    @ 080cf2a0 c90f
    movs r0,#0x2    @ 080cf2a2 0220
    rsbs r0,r0,#0    @ 080cf2a4 4042
    ldrb r3,[r2,#0x8]                        @ 080cf2a6 137a
    ands r0,r3    @ 080cf2a8 1840
    orrs r0,r1    @ 080cf2aa 0843
    movs r1,#0x2    @ 080cf2ac 0221
    orrs r0,r1    @ 080cf2ae 0843
    strb r0,[r2,#0x8]                        @ 080cf2b0 1072
    ldr r3, PTR_font_jp_base_table_080cf328  @ 080cf2b2 1d4b
    lsls r1,r0,#0x1e    @ 080cf2b4 8107
    lsrs r1,r1,#0x1f    @ 080cf2b6 c90f
    lsls r1,r1,#0x2    @ 080cf2b8 8900
    lsls r0,r0,#0x1f    @ 080cf2ba c007
    lsrs r0,r0,#0x1f    @ 080cf2bc c00f
    lsls r0,r0,#0x3    @ 080cf2be c000
    adds r1,r1,r0    @ 080cf2c0 0918
    adds r1,r1,r3    @ 080cf2c2 c918
    ldr r0,[r1,#0x0]                         @ 080cf2c4 0868
    str r0,[r2,#0x4]                         @ 080cf2c6 5060
    movs r0,#0x40    @ 080cf2c8 4020
    ldrb r1,[r2,#0x15]                       @ 080cf2ca 517d
    orrs r0,r1    @ 080cf2cc 0843
    strb r0,[r2,#0x15]                       @ 080cf2ce 5075
    ldr r5, DAT_080cf32c                     @ 080cf2d0 164d
    adds r0,r5,#0x0    @ 080cf2d2 281c
    movs r1,#0x0    @ 080cf2d4 0021
    movs r2,#0x19    @ 080cf2d6 1922
    movs r3,#0x2    @ 080cf2d8 0223
    bl tile_2d_row_copy                      @ 080cf2da 28f0fbf8
    adds r0,r4,#0x0    @ 080cf2de 201c
    bl measure_string_pixel_width            @ 080cf2e0 20f0c8ff
    adds r1,r0,#0x0    @ 080cf2e4 011c
    movs r0,#0xb8    @ 080cf2e6 b820
    subs r0,r0,r1    @ 080cf2e8 401a
    lsrs r1,r0,#0x1f    @ 080cf2ea c10f
    adds r0,r0,r1    @ 080cf2ec 4018
    asrs r1,r0,#0x1    @ 080cf2ee 4110
    adds r0,r1,#0x2    @ 080cf2f0 881c
    movs r1,#0x2    @ 080cf2f2 0221
    movs r2,#0x87    @ 080cf2f4 8722
    adds r3,r4,#0x0    @ 080cf2f6 231c
    bl text_render_wrapper                   @ 080cf2f8 23f0c0fb
    adds r0,r5,#0x0    @ 080cf2fc 281c
    movs r1,#0x0    @ 080cf2fe 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cf300 24f068fa
    pop {r4,r5}                              @ 080cf304 30bc
    pop {r0}                                 @ 080cf306 01bc
    bx r0                                    @ 080cf308 0047
    .zero  0x2
DAT_080cf30c:
    .word  0x0201f641                     @ 080cf30c 41f60102
DAT_080cf310:
    .word  0x00000809                     @ 080cf310 09080000
DAT_080cf314:
    .word  0x0000080d                     @ 080cf314 0d080000
DAT_080cf318:
    .word  0x00000805                     @ 080cf318 05080000
DAT_080cf31c:
    .word  0x02006ed0                     @ 080cf31c d06e0002
DAT_080cf320:
    .word  0x02000000                     @ 080cf320 00000002
DAT_080cf324:
    .word  0x00006c2c                     @ 080cf324 2c6c0000
PTR_font_jp_base_table_080cf328:
    .word  font_jp_base_table             @ 080cf328 54f8e509
DAT_080cf32c:
    .word  0x06013800                     @ 080cf32c 00380106

@ Initialize BG tile data and scroll registers for the card stat display area. Writes stat label tile indices into BG map VRAM and sets BG scroll registers to position the stat area. No APCS params (reads card_display_state from globals). Returns void. Side effects: BG map VRAM and BG scroll regs written. Constants: BG2HOFS=0x04000014, BG2VOFS=0x04000016.
init_card_stat_tile_and_scroll:
    push {r4,r5,r6,lr}                       @ 080cf330 70b5
    lsls r1,r0,#0x10    @ 080cf332 0104
    lsrs r6,r1,#0x10    @ 080cf334 0e0c
    lsrs r0,r0,#0x10    @ 080cf336 000c
    lsls r1,r0,#0x18    @ 080cf338 0106
    lsrs r5,r1,#0x18    @ 080cf33a 0d0e
    lsrs r4,r0,#0x8    @ 080cf33c 040a
    ldr r0, DAT_080cf390                     @ 080cf33e 1448
    movs r1,#0x80    @ 080cf340 8021
    lsls r1,r1,#0x7    @ 080cf342 c901
    bl zero_fill_by_halfword                 @ 080cf344 25f096fd
    ldr r0, DAT_080cf394                     @ 080cf348 1248
    ldr r1, DAT_080cf398                     @ 080cf34a 1349
    movs r2,#0x1    @ 080cf34c 0122
    movs r3,#0x1    @ 080cf34e 0123
    bl tile_2d_row_copy                      @ 080cf350 28f0c0f8
    ldr r3, DAT_080cf39c                     @ 080cf354 114b
    ldr r1, DAT_080cf3a0                     @ 080cf356 1249
    adds r0,r3,r1    @ 080cf358 5818
    ldrb r0,[r0,#0x0]                        @ 080cf35a 0078
    lsrs r2,r0,#0x1    @ 080cf35c 4208
    ldr r0, DAT_080cf3a4                     @ 080cf35e 1148
    adds r1,r3,r0    @ 080cf360 1918
    movs r0,#0x1    @ 080cf362 0120
    ldrb r1,[r1,#0x0]                        @ 080cf364 0978
    ands r0,r1    @ 080cf366 0840
    lsls r0,r0,#0x7    @ 080cf368 c001
    orrs r0,r2    @ 080cf36a 1043
    cmp r0,#0x0                              @ 080cf36c 0028
    bne LAB_080cf38a                         @ 080cf36e 0cd1
    ldr r1, DAT_080cf3a8                     @ 080cf370 0d49
    adds r0,r3,r1    @ 080cf372 5818
    strh r5,[r0,#0x0]                        @ 080cf374 0580
    adds r1,#0x2    @ 080cf376 0231
    adds r0,r3,r1    @ 080cf378 5818
    strh r4,[r0,#0x0]                        @ 080cf37a 0480
    adds r1,#0x2    @ 080cf37c 0231
    adds r0,r3,r1    @ 080cf37e 5818
    strh r6,[r0,#0x0]                        @ 080cf380 0680
    ldr r0, DAT_080cf3ac                     @ 080cf382 0a48
    adds r1,r3,r0    @ 080cf384 1918
    movs r0,#0xa    @ 080cf386 0a20
    strb r0,[r1,#0x0]                        @ 080cf388 0870
LAB_080cf38a:
    pop {r4,r5,r6}                           @ 080cf38a 70bc
    pop {r0}                                 @ 080cf38c 01bc
    bx r0                                    @ 080cf38e 0047
DAT_080cf390:
    .word  0x06014000                     @ 080cf390 00400106
DAT_080cf394:
    .word  0x06010c00                     @ 080cf394 000c0106
DAT_080cf398:
    .word  0x0988ab18                     @ 080cf398 18ab8809
DAT_080cf39c:
    .word  0x0201f440                     @ 080cf39c 40f40102
DAT_080cf3a0:
    .word  0x00000a17                     @ 080cf3a0 170a0000
DAT_080cf3a4:
    .word  0x00000a18                     @ 080cf3a4 180a0000
DAT_080cf3a8:
    .word  0x00000a06                     @ 080cf3a8 060a0000
DAT_080cf3ac:
    .word  0x00000a01                     @ 080cf3ac 010a0000

@ Render a card stat label string followed by its numeric value into BG tile VRAM. Calls render_card_label_text_to_bg for the label, then render_card_numeric_stat_to_bg for the value. r0: stat_id [0..N]; r1: stat_value [0..9999]; r2: bg_tile_dest ptr; r3: row [0..23]. Returns void. Side effects: BG tile VRAM written with label+value tiles.
render_card_stat_label_with_value:
    push {r4,r5,r6,r7,lr}                    @ 080cf3b0 f0b5
    sub sp,#0x4                              @ 080cf3b2 81b0
    movs r6,#0x0    @ 080cf3b4 0026
    movs r0,#0x17    @ 080cf3b6 1720
    movs r1,#0x10    @ 080cf3b8 1021
    movs r2,#0x1    @ 080cf3ba 0122
    movs r3,#0x2    @ 080cf3bc 0223
    bl setup_line_buf_with_font_and_align    @ 080cf3be 21f07ffc
    ldr r2, DAT_080cf468                     @ 080cf3c2 294a
    ldr r0, DAT_080cf46c                     @ 080cf3c4 2948
    ldr r1, DAT_080cf470                     @ 080cf3c6 2a49
    adds r0,r0,r1    @ 080cf3c8 4018
    movs r7,#0x7    @ 080cf3ca 0727
    adds r1,r7,#0x0    @ 080cf3cc 391c
    ldrb r0,[r0,#0x0]                        @ 080cf3ce 0078
    ands r1,r0    @ 080cf3d0 0140
    rsbs r1,r1,#0    @ 080cf3d2 4942
    lsrs r1,r1,#0x1f    @ 080cf3d4 c90f
    movs r0,#0x2    @ 080cf3d6 0220
    rsbs r0,r0,#0    @ 080cf3d8 4042
    ldrb r3,[r2,#0x8]                        @ 080cf3da 137a
    ands r0,r3    @ 080cf3dc 1840
    orrs r0,r1    @ 080cf3de 0843
    movs r1,#0x2    @ 080cf3e0 0221
    orrs r0,r1    @ 080cf3e2 0843
    strb r0,[r2,#0x8]                        @ 080cf3e4 1072
    ldr r3, PTR_font_jp_base_table_080cf474  @ 080cf3e6 234b
    lsls r1,r0,#0x1e    @ 080cf3e8 8107
    lsrs r1,r1,#0x1f    @ 080cf3ea c90f
    lsls r1,r1,#0x2    @ 080cf3ec 8900
    lsls r0,r0,#0x1f    @ 080cf3ee c007
    lsrs r0,r0,#0x1f    @ 080cf3f0 c00f
    lsls r0,r0,#0x3    @ 080cf3f2 c000
    adds r1,r1,r0    @ 080cf3f4 0918
    adds r1,r1,r3    @ 080cf3f6 c918
    ldr r0,[r1,#0x0]                         @ 080cf3f8 0868
    str r0,[r2,#0x4]                         @ 080cf3fa 5060
    movs r0,#0x40    @ 080cf3fc 4020
    ldrb r1,[r2,#0x15]                       @ 080cf3fe 517d
    orrs r0,r1    @ 080cf400 0843
    strb r0,[r2,#0x15]                       @ 080cf402 5075
    ldr r5, DAT_080cf478                     @ 080cf404 1c4d
    str r6,[sp,#0x0]                         @ 080cf406 0096
    movs r0,#0x2    @ 080cf408 0220
    movs r1,#0x2    @ 080cf40a 0221
    adds r2,r5,#0x0    @ 080cf40c 2a1c
    movs r3,#0xc    @ 080cf40e 0c23
    bl render_jp_string_to_tile_line         @ 080cf410 f8f756f9
    adds r4,r0,#0x0    @ 080cf414 041c
    adds r1,r4,#0x3    @ 080cf416 e11c
    ldr r2, DAT_080cf47c                     @ 080cf418 184a
    adds r0,r5,r2    @ 080cf41a a818
    strh r1,[r0,#0x0]                        @ 080cf41c 0180
    adds r4,#0x10    @ 080cf41e 1034
    ldr r0, DAT_080cf480                     @ 080cf420 1748
    movs r1,#0x0    @ 080cf422 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cf424 24f0d6f9
    ldr r3, DAT_080cf484                     @ 080cf428 164b
    adds r0,r5,r3    @ 080cf42a e818
    ldrb r0,[r0,#0x0]                        @ 080cf42c 0078
    lsrs r2,r0,#0x1    @ 080cf42e 4208
    ldr r0, DAT_080cf488                     @ 080cf430 1548
    adds r1,r5,r0    @ 080cf432 2918
    movs r0,#0x1    @ 080cf434 0120
    ldrb r1,[r1,#0x0]                        @ 080cf436 0978
    ands r0,r1    @ 080cf438 0840
    lsls r0,r0,#0x7    @ 080cf43a c001
    orrs r0,r2    @ 080cf43c 1043
    cmp r0,#0x0                              @ 080cf43e 0028
    bne LAB_080cf45c                         @ 080cf440 0cd1
    adds r4,#0x10    @ 080cf442 1034
    adds r0,r4,#0x0    @ 080cf444 201c
    cmp r4,#0x0                              @ 080cf446 002c
    bge LAB_080cf44c                         @ 080cf448 00da
    adds r0,r4,#0x7    @ 080cf44a e01d
LAB_080cf44c:
    asrs r6,r0,#0x3    @ 080cf44c c610
    ands r4,r7    @ 080cf44e 3c40
    cmp r4,#0x0                              @ 080cf450 002c
    beq LAB_080cf456                         @ 080cf452 00d0
    adds r6,#0x1    @ 080cf454 0136
LAB_080cf456:
    ldr r1, DAT_080cf48c                     @ 080cf456 0d49
    adds r0,r5,r1    @ 080cf458 6818
    strb r6,[r0,#0x0]                        @ 080cf45a 0670
LAB_080cf45c:
    bl render_card_numeric_stat_to_bg        @ 080cf45c fff7fefe
    add sp,#0x4                              @ 080cf460 01b0
    pop {r4,r5,r6,r7}                        @ 080cf462 f0bc
    pop {r0}                                 @ 080cf464 01bc
    bx r0                                    @ 080cf466 0047
DAT_080cf468:
    .word  0x02006ed0                     @ 080cf468 d06e0002
DAT_080cf46c:
    .word  0x02000000                     @ 080cf46c 00000002
DAT_080cf470:
    .word  0x00006c2c                     @ 080cf470 2c6c0000
PTR_font_jp_base_table_080cf474:
    .word  font_jp_base_table             @ 080cf474 54f8e509
DAT_080cf478:
    .word  0x0201f441                     @ 080cf478 41f40102
DAT_080cf47c:
    .word  0x00000a03                     @ 080cf47c 030a0000
DAT_080cf480:
    .word  0x06014000                     @ 080cf480 00400106
DAT_080cf484:
    .word  0x00000a16                     @ 080cf484 160a0000
DAT_080cf488:
    .word  0x00000a17                     @ 080cf488 170a0000
DAT_080cf48c:
    .word  0x00000a02                     @ 080cf48c 020a0000

@ Card-list OAM row render branch for animation frame variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 10 (last case). Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword as x_base. Loop r4=0..5: calls write_oam_entry_from_packed_args 6 times for strip OAM (attr0 incremented by 0x20 per step, attr1=0xe0<<0x11+tile_col, attr2=0x81<<7=0x4080). After loop: checks gFontState[0x0a1b] bits[1:0]; if <=1 extracts gPrng[0x148] bits[3:2] (range [0..3]) as delta, computes anim frame Y=0x58-delta, calls write_oam_entry_with_slot_check (attr2=0x1000). Writes one trailing write_oam_entry_from_packed_args (attr2=0). No APCS inputs. Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; STRIP_COUNT=6; SLOT_STATE_OFFSET=0x0a1b; PRNG_DELTA_MASK=bits[3:2] of gPrng[0x148] [0..3]; ATTR2_ANIM=0x1000; OAM_SLOT=0x60.
render_card_list_oam_row_by_anim_frame:
    push {r4,r5,r6,lr}                       @ 080cf490 70b5
    ldr r1, DAT_080cf518                     @ 080cf492 2149
    ldr r2, DAT_080cf51c                     @ 080cf494 214a
    adds r0,r1,r2    @ 080cf496 8818
    ldrb r0,[r0,#0x0]                        @ 080cf498 0078
    lsrs r2,r0,#0x1    @ 080cf49a 4208
    movs r0,#0xa    @ 080cf49c 0a20
    subs r0,r0,r2    @ 080cf49e 801a
    lsls r0,r0,#0x3    @ 080cf4a0 c000
    ldr r2, DAT_080cf520                     @ 080cf4a2 1f4a
    adds r1,r1,r2    @ 080cf4a4 8918
    ldrh r1,[r1,#0x0]                        @ 080cf4a6 0988
    adds r6,r1,r0    @ 080cf4a8 0e18
    movs r4,#0x0    @ 080cf4aa 0024
    movs r5,#0x30    @ 080cf4ac 3025
LAB_080cf4ae:
    lsls r0,r6,#0x10    @ 080cf4ae 3004
    orrs r0,r5    @ 080cf4b0 2843
    lsls r2,r4,#0x12    @ 080cf4b2 a204
    movs r1,#0xe0    @ 080cf4b4 e021
    lsls r1,r1,#0x11    @ 080cf4b6 4904
    adds r2,r2,r1    @ 080cf4b8 5218
    lsrs r2,r2,#0x10    @ 080cf4ba 120c
    movs r1,#0x81    @ 080cf4bc 8121
    lsls r1,r1,#0x7    @ 080cf4be c901
    bl write_oam_entry_from_packed_args      @ 080cf4c0 26f054fe
    adds r5,#0x20    @ 080cf4c4 2035
    adds r4,#0x1    @ 080cf4c6 0134
    cmp r4,#0x5                              @ 080cf4c8 052c
    ble LAB_080cf4ae                         @ 080cf4ca f0dd
    ldr r0, DAT_080cf518                     @ 080cf4cc 1248
    ldr r2, DAT_080cf524                     @ 080cf4ce 154a
    adds r0,r0,r2    @ 080cf4d0 8018
    ldrb r0,[r0,#0x0]                        @ 080cf4d2 0078
    lsrs r0,r0,#0x1    @ 080cf4d4 4008
    movs r1,#0x3    @ 080cf4d6 0321
    ands r0,r1    @ 080cf4d8 0840
    cmp r0,#0x1                              @ 080cf4da 0128
    bhi LAB_080cf512                         @ 080cf4dc 19d8
    ldr r0, PTR_gPrng_080cf528               @ 080cf4de 1248
    movs r1,#0x83    @ 080cf4e0 8321
    lsls r1,r1,#0x2    @ 080cf4e2 8900
    adds r0,r0,r1    @ 080cf4e4 4018
    movs r4,#0xf    @ 080cf4e6 0f24
    ldrh r0,[r0,#0x0]                        @ 080cf4e8 0088
    ands r4,r0    @ 080cf4ea 0440
    lsrs r4,r4,#0x2    @ 080cf4ec a408
    movs r0,#0x58    @ 080cf4ee 5820
    subs r0,r0,r4    @ 080cf4f0 001b
    adds r5,r6,#0x4    @ 080cf4f2 351d
    lsls r5,r5,#0x10    @ 080cf4f4 2d04
    orrs r0,r5    @ 080cf4f6 2843
    movs r3,#0x80    @ 080cf4f8 8023
    lsls r3,r3,#0x5    @ 080cf4fa 5b01
    movs r1,#0x0    @ 080cf4fc 0021
    movs r2,#0x60    @ 080cf4fe 6022
    bl write_oam_entry_with_slot_check       @ 080cf500 27f078f9
    adds r4,#0xbc    @ 080cf504 bc34
    orrs r4,r5    @ 080cf506 2c43
    adds r0,r4,#0x0    @ 080cf508 201c
    movs r1,#0x0    @ 080cf50a 0021
    movs r2,#0x60    @ 080cf50c 6022
    bl write_oam_entry_from_packed_args      @ 080cf50e 26f02dfe
LAB_080cf512:
    pop {r4,r5,r6}                           @ 080cf512 70bc
    pop {r0}                                 @ 080cf514 01bc
    bx r0                                    @ 080cf516 0047
DAT_080cf518:
    .word  0x0201f440                     @ 080cf518 40f40102
DAT_080cf51c:
    .word  0x00000a03                     @ 080cf51c 030a0000
DAT_080cf520:
    .word  0x00000a04                     @ 080cf520 040a0000
DAT_080cf524:
    .word  0x00000a1b                     @ 080cf524 1b0a0000
PTR_gPrng_080cf528:
    .word  gPrng                          @ 080cf528 40000003

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. state=0: reads gPrng+0x148; bit5=0x20: increments gFontState+0x0a0e halfword bits[23:16] nibble (mod 256), calls render_card_numeric_stat_to_bg, sync_state_and_init_sprite(0); bit1=0x2: sync_state_and_init_sprite(2); bit0=0x1: reads LP offset from gFontState+0x0a0e/0x0a06, writes to gP1LifePoints+0x3d40, increments gFontState+0x0a18 bits[9:16] nibble, sync_state_and_init_sprite(0x24). state=1: nibble increment on gFontState+0x0a1b/0x0a1c, if >0x1f also increments gFontState+0x0a18 bits[23:16], writes back. state>=2: returns 1. Key distinguisher: only sibling containing render_card_numeric_stat_to_bg callee (card ATK/DEF stat refresh path). Constants: OAM_SLOT=0x30; STATE_OFFSET=0x0a18; NIBBLE_B_OFFSET=0x0a1b; NIBBLE_C_OFFSET=0x0a1c; STAT_NIBBLE_OFFSET=0x0a0e.
render_card_list_oam_row_by_stat_display:
    push {r4,r5,r6,r7,lr}                    @ 080cf52c f0b5
    ldr r4, DAT_080cf564                     @ 080cf52e 0d4c
    ldr r1, DAT_080cf568                     @ 080cf530 0d49
    adds r0,r4,r1    @ 080cf532 6018
    ldrb r3,[r0,#0x0]                        @ 080cf534 0378
    lsrs r0,r3,#0x1    @ 080cf536 5808
    movs r1,#0xa    @ 080cf538 0a21
    subs r1,r1,r0    @ 080cf53a 091a
    lsls r1,r1,#0x3    @ 080cf53c c900
    movs r2,#0xfe    @ 080cf53e fe22
    lsls r2,r2,#0x1    @ 080cf540 5200
    movs r0,#0x30    @ 080cf542 3020
    bl write_card_list_oam_row_strip         @ 080cf544 f7f7f4ff
    ldr r6, DAT_080cf56c                     @ 080cf548 084e
    adds r6,r6,r4    @ 080cf54a 3619
    .hword 0x46b4    @ 080cf54c b446
    ldr r5,[r6,#0x0]                         @ 080cf54e 3568
    lsls r3,r5,#0xf    @ 080cf550 eb03
    lsrs r7,r3,#0x18    @ 080cf552 1f0e
    cmp r7,#0x0                              @ 080cf554 002f
    beq LAB_080cf570                         @ 080cf556 0bd0
    cmp r7,#0x1                              @ 080cf558 012f
    bne LAB_080cf55e                         @ 080cf55a 00d1
    b LAB_080cf668                           @ 080cf55c 84e0
LAB_080cf55e:
    movs r0,#0x1    @ 080cf55e 0120
    b LAB_080cf6c6                           @ 080cf560 b1e0
    .zero  0x2
DAT_080cf564:
    .word  0x0201f440                     @ 080cf564 40f40102
DAT_080cf568:
    .word  0x00000a03                     @ 080cf568 030a0000
DAT_080cf56c:
    .word  0x00000a18                     @ 080cf56c 180a0000
LAB_080cf570:
    ldr r0, PTR_gPrng_080cf5ac               @ 080cf570 0e48
    movs r1,#0xa4    @ 080cf572 a421
    lsls r1,r1,#0x1    @ 080cf574 4900
    adds r0,r0,r1    @ 080cf576 4018
    ldrh r1,[r0,#0x0]                        @ 080cf578 0188
    movs r0,#0x20    @ 080cf57a 2020
    ands r0,r1    @ 080cf57c 0840
    cmp r0,#0x0                              @ 080cf57e 0028
    beq LAB_080cf5b8                         @ 080cf580 1ad0
    ldr r6, DAT_080cf5b0                     @ 080cf582 0b4e
    adds r3,r4,r6    @ 080cf584 a319
    ldrh r2,[r3,#0x0]                        @ 080cf586 1a88
    movs r0,#0xff    @ 080cf588 ff20
    lsls r0,r0,#0x4    @ 080cf58a 0001
    ands r0,r2    @ 080cf58c 1040
    cmp r0,#0x0                              @ 080cf58e 0028
    bne LAB_080cf594                         @ 080cf590 00d1
    b LAB_080cf6c4                           @ 080cf592 97e0
LAB_080cf594:
    lsls r0,r2,#0x14    @ 080cf594 1005
    lsrs r0,r0,#0x18    @ 080cf596 000e
    subs r0,#0x1    @ 080cf598 0138
    movs r1,#0xff    @ 080cf59a ff21
    ands r0,r1    @ 080cf59c 0840
    lsls r0,r0,#0x4    @ 080cf59e 0001
    ldr r1, DAT_080cf5b4                     @ 080cf5a0 0449
    ands r1,r2    @ 080cf5a2 1140
    orrs r1,r0    @ 080cf5a4 0143
    strh r1,[r3,#0x0]                        @ 080cf5a6 1980
    b LAB_080cf5ee                           @ 080cf5a8 21e0
    .zero  0x2
PTR_gPrng_080cf5ac:
    .word  gPrng                          @ 080cf5ac 40000003
DAT_080cf5b0:
    .word  0x00000a0e                     @ 080cf5b0 0e0a0000
DAT_080cf5b4:
    .word  0xfffff00f                     @ 080cf5b4 0ff0ffff
LAB_080cf5b8:
    movs r0,#0x10    @ 080cf5b8 1020
    ands r0,r1    @ 080cf5ba 0840
    cmp r0,#0x0                              @ 080cf5bc 0028
    beq LAB_080cf608                         @ 080cf5be 23d0
    ldr r0, DAT_080cf5fc                     @ 080cf5c0 0e48
    adds r5,r4,r0    @ 080cf5c2 2518
    ldrh r3,[r5,#0x0]                        @ 080cf5c4 2b88
    lsls r2,r3,#0x14    @ 080cf5c6 1a05
    lsrs r0,r2,#0x18    @ 080cf5c8 100e
    ldr r6, DAT_080cf600                     @ 080cf5ca 0d4e
    adds r1,r4,r6    @ 080cf5cc a119
    ldrh r1,[r1,#0x0]                        @ 080cf5ce 0988
    adds r0,r1,r0    @ 080cf5d0 0818
    adds r6,#0x2    @ 080cf5d2 0236
    adds r1,r4,r6    @ 080cf5d4 a119
    ldrh r1,[r1,#0x0]                        @ 080cf5d6 0988
    cmp r0,r1                                @ 080cf5d8 8842
    bge LAB_080cf6c4                         @ 080cf5da 73da
    lsrs r0,r2,#0x18    @ 080cf5dc 100e
    adds r0,#0x1    @ 080cf5de 0130
    movs r1,#0xff    @ 080cf5e0 ff21
    ands r0,r1    @ 080cf5e2 0840
    lsls r0,r0,#0x4    @ 080cf5e4 0001
    ldr r1, DAT_080cf604                     @ 080cf5e6 0749
    ands r1,r3    @ 080cf5e8 1940
    orrs r1,r0    @ 080cf5ea 0143
    strh r1,[r5,#0x0]                        @ 080cf5ec 2980
LAB_080cf5ee:
    bl render_card_numeric_stat_to_bg        @ 080cf5ee fff735fe
    movs r0,#0x0    @ 080cf5f2 0020
    bl sync_state_and_init_sprite            @ 080cf5f4 2af05efa
    b LAB_080cf6c4                           @ 080cf5f8 64e0
    .zero  0x2
DAT_080cf5fc:
    .word  0x00000a0e                     @ 080cf5fc 0e0a0000
DAT_080cf600:
    .word  0x00000a06                     @ 080cf600 060a0000
DAT_080cf604:
    .word  0xfffff00f                     @ 080cf604 0ff0ffff
LAB_080cf608:
    movs r0,#0x2    @ 080cf608 0220
    ands r0,r1    @ 080cf60a 0840
    cmp r0,#0x0                              @ 080cf60c 0028
    beq LAB_080cf618                         @ 080cf60e 03d0
    movs r0,#0x2    @ 080cf610 0220
    bl sync_state_and_init_sprite            @ 080cf612 2af04ffa
    b LAB_080cf6c4                           @ 080cf616 55e0
LAB_080cf618:
    movs r0,#0x1    @ 080cf618 0120
    ands r0,r1    @ 080cf61a 0840
    cmp r0,#0x0                              @ 080cf61c 0028
    beq LAB_080cf6c4                         @ 080cf61e 51d0
    ldr r2, PTR_gP1LifePoints_080cf658       @ 080cf620 0d4a
    movs r0,#0xea    @ 080cf622 ea20
    lsls r0,r0,#0x5    @ 080cf624 4001
    adds r2,r2,r0    @ 080cf626 1218
    ldr r1, DAT_080cf65c                     @ 080cf628 0c49
    adds r0,r4,r1    @ 080cf62a 6018
    ldrh r0,[r0,#0x0]                        @ 080cf62c 0088
    lsls r0,r0,#0x14    @ 080cf62e 0005
    lsrs r0,r0,#0x18    @ 080cf630 000e
    ldr r6, DAT_080cf660                     @ 080cf632 0b4e
    adds r1,r4,r6    @ 080cf634 a119
    ldrh r1,[r1,#0x0]                        @ 080cf636 0988
    adds r0,r1,r0    @ 080cf638 0818
    str r0,[r2,#0x0]                         @ 080cf63a 1060
    lsrs r1,r3,#0x18    @ 080cf63c 190e
    adds r1,#0x1    @ 080cf63e 0131
    movs r0,#0xff    @ 080cf640 ff20
    ands r1,r0    @ 080cf642 0140
    lsls r1,r1,#0x9    @ 080cf644 4902
    ldr r0, DAT_080cf664                     @ 080cf646 0748
    ands r0,r5    @ 080cf648 2840
    orrs r0,r1    @ 080cf64a 0843
    .hword 0x4661    @ 080cf64c 6146
    str r0,[r1,#0x0]                         @ 080cf64e 0860
    movs r0,#0x24    @ 080cf650 2420
    bl sync_state_and_init_sprite            @ 080cf652 2af02ffa
    b LAB_080cf6c4                           @ 080cf656 35e0
PTR_gP1LifePoints_080cf658:
    .word  gP1LifePoints                  @ 080cf658 e0c40102
DAT_080cf65c:
    .word  0x00000a0e                     @ 080cf65c 0e0a0000
DAT_080cf660:
    .word  0x00000a06                     @ 080cf660 060a0000
DAT_080cf664:
    .word  0xfffe01ff                     @ 080cf664 ff01feff
LAB_080cf668:
    ldr r0, DAT_080cf6cc                     @ 080cf668 1848
    adds r6,r4,r0    @ 080cf66a 2618
    ldrb r5,[r6,#0x0]                        @ 080cf66c 3578
    lsrs r0,r5,#0x1    @ 080cf66e 6808
    ldr r1, DAT_080cf6d0                     @ 080cf670 1749
    adds r3,r4,r1    @ 080cf672 6318
    adds r2,r7,#0x0    @ 080cf674 3a1c
    ldrb r4,[r3,#0x0]                        @ 080cf676 1c78
    ands r2,r4    @ 080cf678 2240
    lsls r2,r2,#0x7    @ 080cf67a d201
    orrs r2,r0    @ 080cf67c 0243
    adds r2,#0x1    @ 080cf67e 0132
    movs r1,#0x7f    @ 080cf680 7f21
    ands r1,r2    @ 080cf682 1140
    lsls r1,r1,#0x1    @ 080cf684 4900
    movs r4,#0x1    @ 080cf686 0124
    adds r0,r7,#0x0    @ 080cf688 381c
    ands r0,r5    @ 080cf68a 2840
    orrs r0,r1    @ 080cf68c 0843
    strb r0,[r6,#0x0]                        @ 080cf68e 3070
    lsrs r1,r2,#0x7    @ 080cf690 d109
    ands r1,r7    @ 080cf692 3940
    ands r1,r4    @ 080cf694 2140
    movs r0,#0x2    @ 080cf696 0220
    rsbs r0,r0,#0    @ 080cf698 4042
    ldrb r6,[r3,#0x0]                        @ 080cf69a 1e78
    ands r0,r6    @ 080cf69c 3040
    orrs r0,r1    @ 080cf69e 0843
    strb r0,[r3,#0x0]                        @ 080cf6a0 1870
    movs r0,#0xff    @ 080cf6a2 ff20
    ands r2,r0    @ 080cf6a4 0240
    cmp r2,#0x1f                             @ 080cf6a6 1f2a
    bls LAB_080cf6c4                         @ 080cf6a8 0cd9
    .hword 0x4660    @ 080cf6aa 6046
    ldr r2,[r0,#0x0]                         @ 080cf6ac 0268
    lsls r1,r2,#0xf    @ 080cf6ae d103
    lsrs r1,r1,#0x18    @ 080cf6b0 090e
    adds r1,#0x1    @ 080cf6b2 0131
    movs r0,#0xff    @ 080cf6b4 ff20
    ands r1,r0    @ 080cf6b6 0140
    lsls r1,r1,#0x9    @ 080cf6b8 4902
    ldr r0, DAT_080cf6d4                     @ 080cf6ba 0648
    ands r0,r2    @ 080cf6bc 1040
    orrs r0,r1    @ 080cf6be 0843
    .hword 0x4661    @ 080cf6c0 6146
    str r0,[r1,#0x0]                         @ 080cf6c2 0860
LAB_080cf6c4:
    movs r0,#0x0    @ 080cf6c4 0020
LAB_080cf6c6:
    pop {r4,r5,r6,r7}                        @ 080cf6c6 f0bc
    pop {r1}                                 @ 080cf6c8 02bc
    bx r1                                    @ 080cf6ca 0847
DAT_080cf6cc:
    .word  0x00000a1b                     @ 080cf6cc 1b0a0000
DAT_080cf6d0:
    .word  0x00000a1c                     @ 080cf6d0 1c0a0000
DAT_080cf6d4:
    .word  0xfffe01ff                     @ 080cf6d4 ff01feff

@ Forward circular search for next occupied slot in card-list slot bitmap. r0=start_slot_idx [0..9]; returns r0=found_slot_idx. Reads gFontState[0x0a10] word; tests bit(r2) for each slot. Increments r2 each iteration; wraps at 10 via __modsi3. If wrapped back to anchor returns r4 or r4+10 based on wrap_flag. No external writes; read-only query. caller: render_card_list_oam_row_by_stat_state (0x080cfbdc) bit4 path. Constants: SLOT_BITMASK_OFFSET=0x0a10; SLOT_COUNT=10.
find_next_occupied_slot_forward:
    push {r4,r5,r6,lr}                       @ 080cf6d8 70b5
    adds r4,r0,#0x0    @ 080cf6da 041c
    adds r2,r4,#0x0    @ 080cf6dc 221c
    movs r5,#0x0    @ 080cf6de 0025
    ldr r6, DAT_080cf6e4                     @ 080cf6e0 004e
    b LAB_080cf71a                           @ 080cf6e2 1ae0
DAT_080cf6e4:
    .word  0x0201f440                     @ 080cf6e4 40f40102
LAB_080cf6e8:
    adds r2,#0xa    @ 080cf6e8 0a32
    b LAB_080cf718                           @ 080cf6ea 15e0
LAB_080cf6ec:
    subs r2,#0x9    @ 080cf6ec 093a
    adds r0,r2,#0x0    @ 080cf6ee 101c
    movs r1,#0xa    @ 080cf6f0 0a21
    bl __modsi3                              @ 080cf6f2 3ef0d3ff
    adds r2,r0,#0x0    @ 080cf6f6 021c
    adds r2,#0xa    @ 080cf6f8 0a32
    movs r1,#0xa1    @ 080cf6fa a121
    lsls r1,r1,#0x4    @ 080cf6fc 0901
    adds r0,r6,r1    @ 080cf6fe 7018
    movs r1,#0x1    @ 080cf700 0121
    lsls r1,r2    @ 080cf702 9140
    ldr r0,[r0,#0x0]                         @ 080cf704 0068
    ands r0,r1    @ 080cf706 0840
    cmp r0,#0x0                              @ 080cf708 0028
    bne LAB_080cf73c                         @ 080cf70a 17d1
    cmp r2,r4                                @ 080cf70c a242
    bne LAB_080cf71a                         @ 080cf70e 04d1
    subs r4,#0xa    @ 080cf710 0a3c
    cmp r5,#0x0                              @ 080cf712 002d
    bne LAB_080cf74a                         @ 080cf714 19d1
    subs r2,#0xa    @ 080cf716 0a3a
LAB_080cf718:
    movs r5,#0x1    @ 080cf718 0125
LAB_080cf71a:
    cmp r2,#0x9                              @ 080cf71a 092a
    bgt LAB_080cf6ec                         @ 080cf71c e6dc
    adds r2,#0x1    @ 080cf71e 0132
    adds r0,r2,#0x0    @ 080cf720 101c
    movs r1,#0xa    @ 080cf722 0a21
    bl __modsi3                              @ 080cf724 3ef0baff
    adds r2,r0,#0x0    @ 080cf728 021c
    movs r1,#0xa1    @ 080cf72a a121
    lsls r1,r1,#0x4    @ 080cf72c 0901
    adds r0,r6,r1    @ 080cf72e 7018
    movs r1,#0x1    @ 080cf730 0121
    lsls r1,r2    @ 080cf732 9140
    ldr r0,[r0,#0x0]                         @ 080cf734 0068
    ands r0,r1    @ 080cf736 0840
    cmp r0,#0x0                              @ 080cf738 0028
    beq LAB_080cf740                         @ 080cf73a 01d0
LAB_080cf73c:
    adds r0,r2,#0x0    @ 080cf73c 101c
    b LAB_080cf74c                           @ 080cf73e 05e0
LAB_080cf740:
    cmp r2,r4                                @ 080cf740 a242
    bne LAB_080cf71a                         @ 080cf742 ead1
    adds r4,#0xa    @ 080cf744 0a34
    cmp r5,#0x0                              @ 080cf746 002d
    beq LAB_080cf6e8                         @ 080cf748 ced0
LAB_080cf74a:
    adds r0,r4,#0x0    @ 080cf74a 201c
LAB_080cf74c:
    pop {r4,r5,r6}                           @ 080cf74c 70bc
    pop {r1}                                 @ 080cf74e 02bc
    bx r1                                    @ 080cf750 0847
    .zero  0x2

@ Backward circular search for next occupied slot in card-list slot bitmap. Symmetric sibling of find_next_occupied_slot_forward (0x080cf6d8). r0=start_slot_idx [0..9]; returns r0=found_slot_idx (decreasing direction). Reads gFontState[0x0a10] word; r2-- each iteration; wraps 0->9. No external writes; read-only query. caller: render_card_list_oam_row_by_stat_state (0x080cfbdc) bit5/0xc0 paths. Constants: SLOT_BITMASK_OFFSET=0x0a10; SLOT_COUNT=10.
find_next_occupied_slot_backward:
    push {r4,r5,r6,lr}                       @ 080cf754 70b5
    adds r4,r0,#0x0    @ 080cf756 041c
    adds r2,r4,#0x0    @ 080cf758 221c
    movs r5,#0x0    @ 080cf75a 0025
    ldr r6, DAT_080cf760                     @ 080cf75c 004e
    b LAB_080cf79c                           @ 080cf75e 1de0
DAT_080cf760:
    .word  0x0201f440                     @ 080cf760 40f40102
LAB_080cf764:
    adds r2,r3,#0x0    @ 080cf764 1a1c
    adds r2,#0xa    @ 080cf766 0a32
    b LAB_080cf79a                           @ 080cf768 17e0
LAB_080cf76a:
    subs r2,#0xa    @ 080cf76a 0a3a
    movs r0,#0x9    @ 080cf76c 0920
    cmp r2,#0x0                              @ 080cf76e 002a
    beq LAB_080cf774                         @ 080cf770 00d0
    subs r0,r2,#0x1    @ 080cf772 501e
LAB_080cf774:
    adds r2,r0,#0x0    @ 080cf774 021c
    adds r2,#0xa    @ 080cf776 0a32
    movs r1,#0xa1    @ 080cf778 a121
    lsls r1,r1,#0x4    @ 080cf77a 0901
    adds r0,r6,r1    @ 080cf77c 7018
    movs r1,#0x1    @ 080cf77e 0121
    lsls r1,r2    @ 080cf780 9140
    ldr r0,[r0,#0x0]                         @ 080cf782 0068
    ands r0,r1    @ 080cf784 0840
    cmp r0,#0x0                              @ 080cf786 0028
    beq LAB_080cf78e                         @ 080cf788 01d0
    adds r0,r2,#0x0    @ 080cf78a 101c
    b LAB_080cf7cc                           @ 080cf78c 1ee0
LAB_080cf78e:
    cmp r2,r4                                @ 080cf78e a242
    bne LAB_080cf79c                         @ 080cf790 04d1
    subs r4,#0xa    @ 080cf792 0a3c
    cmp r5,#0x0                              @ 080cf794 002d
    bne LAB_080cf7ca                         @ 080cf796 18d1
    subs r2,#0xa    @ 080cf798 0a3a
LAB_080cf79a:
    movs r5,#0x1    @ 080cf79a 0125
LAB_080cf79c:
    cmp r2,#0x9                              @ 080cf79c 092a
    bgt LAB_080cf76a                         @ 080cf79e e4dc
    movs r3,#0x9    @ 080cf7a0 0923
    cmp r2,#0x0                              @ 080cf7a2 002a
    beq LAB_080cf7a8                         @ 080cf7a4 00d0
    subs r3,r2,#0x1    @ 080cf7a6 531e
LAB_080cf7a8:
    adds r2,r3,#0x0    @ 080cf7a8 1a1c
    movs r1,#0xa1    @ 080cf7aa a121
    lsls r1,r1,#0x4    @ 080cf7ac 0901
    adds r0,r6,r1    @ 080cf7ae 7018
    movs r1,#0x1    @ 080cf7b0 0121
    lsls r1,r3    @ 080cf7b2 9940
    ldr r0,[r0,#0x0]                         @ 080cf7b4 0068
    ands r0,r1    @ 080cf7b6 0840
    cmp r0,#0x0                              @ 080cf7b8 0028
    beq LAB_080cf7c0                         @ 080cf7ba 01d0
    adds r0,r3,#0x0    @ 080cf7bc 181c
    b LAB_080cf7cc                           @ 080cf7be 05e0
LAB_080cf7c0:
    cmp r3,r4                                @ 080cf7c0 a342
    bne LAB_080cf79c                         @ 080cf7c2 ebd1
    adds r4,#0xa    @ 080cf7c4 0a34
    cmp r5,#0x0                              @ 080cf7c6 002d
    beq LAB_080cf764                         @ 080cf7c8 ccd0
LAB_080cf7ca:
    adds r0,r4,#0x0    @ 080cf7ca 201c
LAB_080cf7cc:
    pop {r4,r5,r6}                           @ 080cf7cc 70bc
    pop {r1}                                 @ 080cf7ce 02bc
    bx r1                                    @ 080cf7d0 0847
    .zero  0x2

@ 由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. 首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x80<<7=0x4000 halfword); 读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的 bit[0]/bit[1] 判断是否需要渲染. 若条件不满足直接跳至末尾. 满足后: 读 r4 (入口参数) 作为 stat 值, 计算显示行列位置 (modsi3/divsi3 各 1 次, 除数 0xa=10), 调用 copy_bytes_by_halfword 拷贝调色板数据两次 (来自 ROM 0x09850c5c/0x0984ee2c 到 0x05000260/0x05000280), 然后 tile_2d_row_copy 拷贝 tile 数据到 VRAM (0x06010000), 调用 setup_line_buf + render_jp (game_str) 渲染统计数字字符到 BG tile; 最后 write_line_buf_to_bg_tile_vram 写回 VRAM. 函数使用 r8/r9/r10 为 callee-save 别名. r0: s32 stat_value (caller1 080c7a74 从卡牌 ATK/DEF 字段传入; caller2 080c80da 固定传 0). Constants: VRAM_BG_CLEAR=0x06014000, STATE_BASE=0x0201f440, PAL_DST_A=0x05000260, PAL_SRC_A=0x09850c5c, PAL_DST_B=0x05000280, PAL_SRC_B=0x0984ee2c, TILE_VRAM_BASE=0x06010000, STAT_ROWS=0x13, STAT_COLS=0xa.
render_card_stat_tiles_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080cf7d4 f0b5
    .hword 0x4657    @ 080cf7d6 5746
    .hword 0x464e    @ 080cf7d8 4e46
    .hword 0x4645    @ 080cf7da 4546
    push {r5,r6,r7}                          @ 080cf7dc e0b4
    adds r4,r0,#0x0    @ 080cf7de 041c
    ldr r0, DAT_080cf9a0                     @ 080cf7e0 6f48
    movs r1,#0x80    @ 080cf7e2 8021
    lsls r1,r1,#0x7    @ 080cf7e4 c901
    bl zero_fill_by_halfword                 @ 080cf7e6 25f045fb
    ldr r3, DAT_080cf9a4                     @ 080cf7ea 6e4b
    ldr r1, DAT_080cf9a8                     @ 080cf7ec 6e49
    adds r0,r3,r1    @ 080cf7ee 5818
    ldrb r0,[r0,#0x0]                        @ 080cf7f0 0078
    lsrs r2,r0,#0x1    @ 080cf7f2 4208
    ldr r0, DAT_080cf9ac                     @ 080cf7f4 6d48
    adds r1,r3,r0    @ 080cf7f6 1918
    movs r5,#0x1    @ 080cf7f8 0125
    adds r0,r5,#0x0    @ 080cf7fa 281c
    ldrb r1,[r1,#0x0]                        @ 080cf7fc 0978
    ands r0,r1    @ 080cf7fe 0840
    lsls r0,r0,#0x7    @ 080cf800 c001
    orrs r0,r2    @ 080cf802 1043
    cmp r0,#0x0                              @ 080cf804 0028
    bne LAB_080cf852                         @ 080cf806 24d1
    movs r1,#0xa1    @ 080cf808 a121
    lsls r1,r1,#0x4    @ 080cf80a 0901
    adds r0,r3,r1    @ 080cf80c 5818
    asrs r2,r4,#0x1    @ 080cf80e 6210
    str r2,[r0,#0x0]                         @ 080cf810 0260
    ldr r0, DAT_080cf9b0                     @ 080cf812 6748
    adds r4,r3,r0    @ 080cf814 1c18
    ldrh r3,[r4,#0x0]                        @ 080cf816 2388
    lsls r1,r3,#0x14    @ 080cf818 1905
    lsrs r1,r1,#0x18    @ 080cf81a 090e
    adds r0,r5,#0x0    @ 080cf81c 281c
    lsls r0,r1    @ 080cf81e 8840
    ands r0,r2    @ 080cf820 1040
    cmp r0,#0x0                              @ 080cf822 0028
    bne LAB_080cf852                         @ 080cf824 15d1
    .hword 0x46a0    @ 080cf826 a046
    ldr r7, DAT_080cf9b4                     @ 080cf828 624f
    adds r4,r2,#0x0    @ 080cf82a 141c
    movs r6,#0xff    @ 080cf82c ff26
LAB_080cf82e:
    lsls r0,r3,#0x14    @ 080cf82e 1805
    lsrs r0,r0,#0x18    @ 080cf830 000e
    adds r0,#0x1    @ 080cf832 0130
    ands r0,r6    @ 080cf834 3040
    lsls r0,r0,#0x4    @ 080cf836 0001
    adds r2,r7,#0x0    @ 080cf838 3a1c
    ands r2,r3    @ 080cf83a 1a40
    orrs r2,r0    @ 080cf83c 0243
    adds r3,r2,#0x0    @ 080cf83e 131c
    lsls r1,r2,#0x14    @ 080cf840 1105
    lsrs r1,r1,#0x18    @ 080cf842 090e
    adds r0,r5,#0x0    @ 080cf844 281c
    lsls r0,r1    @ 080cf846 8840
    ands r0,r4    @ 080cf848 2040
    cmp r0,#0x0                              @ 080cf84a 0028
    beq LAB_080cf82e                         @ 080cf84c efd0
    .hword 0x4641    @ 080cf84e 4146
    strh r2,[r1,#0x0]                        @ 080cf850 0a80
LAB_080cf852:
    ldr r0, DAT_080cf9b8                     @ 080cf852 5948
    ldr r1, DAT_080cf9bc                     @ 080cf854 5949
    movs r2,#0x20    @ 080cf856 2022
    bl copy_bytes_by_halfword                @ 080cf858 25f024fb
    ldr r0, DAT_080cf9c0                     @ 080cf85c 5848
    ldr r1, DAT_080cf9a4                     @ 080cf85e 5149
    ldr r2, DAT_080cf9b0                     @ 080cf860 534a
    adds r1,r1,r2    @ 080cf862 8918
    ldrh r1,[r1,#0x0]                        @ 080cf864 0988
    lsls r1,r1,#0x14    @ 080cf866 0905
    lsrs r1,r1,#0x18    @ 080cf868 090e
    lsls r1,r1,#0x5    @ 080cf86a 4901
    ldr r2, DAT_080cf9c4                     @ 080cf86c 554a
    adds r1,r1,r2    @ 080cf86e 8918
    movs r2,#0x20    @ 080cf870 2022
    bl copy_bytes_by_halfword                @ 080cf872 25f017fb
    movs r5,#0x0    @ 080cf876 0025
LAB_080cf878:
    adds r0,r5,#0x0    @ 080cf878 281c
    movs r1,#0xa    @ 080cf87a 0a21
    bl __modsi3                              @ 080cf87c 3ef00eff
    adds r4,r0,#0x0    @ 080cf880 041c
    lsls r4,r4,#0x1    @ 080cf882 6400
    adds r0,r5,#0x0    @ 080cf884 281c
    movs r1,#0xa    @ 080cf886 0a21
    bl __divsi3                              @ 080cf888 3ef0bcfe
    lsls r0,r0,#0x6    @ 080cf88c 8001
    movs r3,#0xc0    @ 080cf88e c023
    lsls r3,r3,#0x1    @ 080cf890 5b00
    adds r0,r0,r3    @ 080cf892 c018
    adds r4,r4,r0    @ 080cf894 2418
    lsls r4,r4,#0x5    @ 080cf896 6401
    ldr r0, DAT_080cf9c8                     @ 080cf898 4b48
    adds r4,r4,r0    @ 080cf89a 2418
    lsls r1,r5,#0x7    @ 080cf89c e901
    ldr r0, DAT_080cf9cc                     @ 080cf89e 4b48
    adds r1,r1,r0    @ 080cf8a0 0918
    adds r0,r4,#0x0    @ 080cf8a2 201c
    movs r2,#0x2    @ 080cf8a4 0222
    movs r3,#0x2    @ 080cf8a6 0223
    bl tile_2d_row_copy                      @ 080cf8a8 27f014fe
    adds r5,#0x1    @ 080cf8ac 0135
    cmp r5,#0x13                             @ 080cf8ae 132d
    ble LAB_080cf878                         @ 080cf8b0 e2dd
    movs r0,#0x10    @ 080cf8b2 1020
    movs r1,#0x2    @ 080cf8b4 0221
    movs r2,#0x1    @ 080cf8b6 0122
    movs r3,#0x0    @ 080cf8b8 0023
    bl setup_line_buf_with_font_and_align    @ 080cf8ba 21f001fa
    ldr r2, DAT_080cf9d0                     @ 080cf8be 444a
    ldr r5, DAT_080cf9d4                     @ 080cf8c0 444d
    ldr r1, DAT_080cf9d8                     @ 080cf8c2 4549
    adds r5,r5,r1    @ 080cf8c4 6d18
    movs r1,#0x7    @ 080cf8c6 0721
    ldrb r3,[r5,#0x0]                        @ 080cf8c8 2b78
    ands r1,r3    @ 080cf8ca 1940
    rsbs r1,r1,#0    @ 080cf8cc 4942
    lsrs r1,r1,#0x1f    @ 080cf8ce c90f
    movs r0,#0x2    @ 080cf8d0 0220
    rsbs r0,r0,#0    @ 080cf8d2 4042
    ldrb r3,[r2,#0x8]                        @ 080cf8d4 137a
    ands r0,r3    @ 080cf8d6 1840
    orrs r0,r1    @ 080cf8d8 0843
    movs r1,#0x2    @ 080cf8da 0221
    orrs r0,r1    @ 080cf8dc 0843
    strb r0,[r2,#0x8]                        @ 080cf8de 1072
    ldr r3, PTR_font_jp_base_table_080cf9dc  @ 080cf8e0 3e4b
    lsls r1,r0,#0x1e    @ 080cf8e2 8107
    lsrs r1,r1,#0x1f    @ 080cf8e4 c90f
    lsls r1,r1,#0x2    @ 080cf8e6 8900
    lsls r0,r0,#0x1f    @ 080cf8e8 c007
    lsrs r0,r0,#0x1f    @ 080cf8ea c00f
    lsls r0,r0,#0x3    @ 080cf8ec c000
    adds r1,r1,r0    @ 080cf8ee 0918
    adds r1,r1,r3    @ 080cf8f0 c918
    ldr r0,[r1,#0x0]                         @ 080cf8f2 0868
    str r0,[r2,#0x4]                         @ 080cf8f4 5060
    movs r0,#0x40    @ 080cf8f6 4020
    ldrb r1,[r2,#0x15]                       @ 080cf8f8 517d
    orrs r0,r1    @ 080cf8fa 0843
    strb r0,[r2,#0x15]                       @ 080cf8fc 5075
    ldr r7, DAT_080cf9e0                     @ 080cf8fe 384f
    adds r0,r7,#0x0    @ 080cf900 381c
    movs r1,#0x0    @ 080cf902 0021
    movs r2,#0x10    @ 080cf904 1022
    movs r3,#0x2    @ 080cf906 0223
    bl tile_2d_row_copy                      @ 080cf908 27f0e4fd
    ldr r4, DAT_080cf9a4                     @ 080cf90c 254c
    ldr r2, DAT_080cf9b0                     @ 080cf90e 284a
    adds r2,r2,r4    @ 080cf910 1219
    .hword 0x4691    @ 080cf912 9146
    ldrh r3,[r2,#0x0]                        @ 080cf914 1388
    lsls r0,r3,#0x14    @ 080cf916 1805
    lsrs r0,r0,#0x18    @ 080cf918 000e
    ldr r1, DAT_080cf9e4                     @ 080cf91a 3249
    .hword 0x4688    @ 080cf91c 8846
    add r0,r8                                @ 080cf91e 4044
    bl game_str_id_to_row                    @ 080cf920 25f07afa
    ldr r2, PTR_game_str_pointer_table_080cf9e8 @ 080cf924 304a
    .hword 0x4692    @ 080cf926 9246
    lsls r0,r0,#0x10    @ 080cf928 0004
    lsrs r0,r0,#0x10    @ 080cf92a 000c
    lsls r1,r0,#0x1    @ 080cf92c 4100
    adds r1,r1,r0    @ 080cf92e 0918
    lsls r1,r1,#0x1    @ 080cf930 4900
    ldrb r3,[r5,#0x0]                        @ 080cf932 2b78
    lsls r0,r3,#0x1d    @ 080cf934 5807
    lsrs r0,r0,#0x1d    @ 080cf936 400f
    adds r1,r1,r0    @ 080cf938 0918
    lsls r1,r1,#0x2    @ 080cf93a 8900
    add r1,r10                               @ 080cf93c 5144
    ldr r3,[r1,#0x0]                         @ 080cf93e 0b68
    ldr r6, PTR_game_str_ja_080cf9ec         @ 080cf940 2a4e
    adds r3,r3,r6    @ 080cf942 9b19
    movs r0,#0x3    @ 080cf944 0320
    movs r1,#0x3    @ 080cf946 0321
    movs r2,#0x8    @ 080cf948 0822
    bl text_render_wrapper                   @ 080cf94a 23f097f8
    .hword 0x4649    @ 080cf94e 4946
    ldrh r1,[r1,#0x0]                        @ 080cf950 0988
    lsls r0,r1,#0x14    @ 080cf952 0805
    lsrs r0,r0,#0x18    @ 080cf954 000e
    add r0,r8                                @ 080cf956 4044
    bl game_str_id_to_row                    @ 080cf958 25f05efa
    lsls r0,r0,#0x10    @ 080cf95c 0004
    lsrs r0,r0,#0x10    @ 080cf95e 000c
    lsls r1,r0,#0x1    @ 080cf960 4100
    adds r1,r1,r0    @ 080cf962 0918
    lsls r1,r1,#0x1    @ 080cf964 4900
    ldrb r5,[r5,#0x0]                        @ 080cf966 2d78
    lsls r0,r5,#0x1d    @ 080cf968 6807
    lsrs r0,r0,#0x1d    @ 080cf96a 400f
    adds r1,r1,r0    @ 080cf96c 0918
    lsls r1,r1,#0x2    @ 080cf96e 8900
    add r1,r10                               @ 080cf970 5144
    ldr r3,[r1,#0x0]                         @ 080cf972 0b68
    adds r3,r3,r6    @ 080cf974 9b19
    movs r0,#0x2    @ 080cf976 0220
    movs r1,#0x2    @ 080cf978 0221
    movs r2,#0x7    @ 080cf97a 0722
    bl text_render_wrapper                   @ 080cf97c 23f07ef8
    adds r0,r7,#0x0    @ 080cf980 381c
    movs r1,#0x0    @ 080cf982 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cf984 23f026ff
    ldr r2, DAT_080cf9f0                     @ 080cf988 194a
    adds r4,r4,r2    @ 080cf98a a418
    movs r0,#0x5    @ 080cf98c 0520
    strb r0,[r4,#0x0]                        @ 080cf98e 2070
    pop {r3,r4,r5}                           @ 080cf990 38bc
    .hword 0x4698    @ 080cf992 9846
    .hword 0x46a1    @ 080cf994 a146
    .hword 0x46aa    @ 080cf996 aa46
    pop {r4,r5,r6,r7}                        @ 080cf998 f0bc
    pop {r0}                                 @ 080cf99a 01bc
    bx r0                                    @ 080cf99c 0047
    .zero  0x2
DAT_080cf9a0:
    .word  0x06014000                     @ 080cf9a0 00400106
DAT_080cf9a4:
    .word  0x0201f440                     @ 080cf9a4 40f40102
DAT_080cf9a8:
    .word  0x00000a17                     @ 080cf9a8 170a0000
DAT_080cf9ac:
    .word  0x00000a18                     @ 080cf9ac 180a0000
DAT_080cf9b0:
    .word  0x00000a0e                     @ 080cf9b0 0e0a0000
DAT_080cf9b4:
    .word  0xfffff00f                     @ 080cf9b4 0ff0ffff
DAT_080cf9b8:
    .word  0x05000260                     @ 080cf9b8 60020005
DAT_080cf9bc:
    .word  0x09850c5c                     @ 080cf9bc 5c0c8509
DAT_080cf9c0:
    .word  0x05000280                     @ 080cf9c0 80020005
DAT_080cf9c4:
    .word  0x0984ee2c                     @ 080cf9c4 2cee8409
DAT_080cf9c8:
    .word  0x06010000                     @ 080cf9c8 00000106
DAT_080cf9cc:
    .word  0x0984e42c                     @ 080cf9cc 2ce48409
DAT_080cf9d0:
    .word  0x02006ed0                     @ 080cf9d0 d06e0002
DAT_080cf9d4:
    .word  0x02000000                     @ 080cf9d4 00000002
DAT_080cf9d8:
    .word  0x00006c2c                     @ 080cf9d8 2c6c0000
PTR_font_jp_base_table_080cf9dc:
    .word  font_jp_base_table             @ 080cf9dc 54f8e509
DAT_080cf9e0:
    .word  0x06012800                     @ 080cf9e0 00280106
DAT_080cf9e4:
    .word  0x000001f5                     @ 080cf9e4 f5010000
PTR_game_str_pointer_table_080cf9e8:
    .word  game_str_pointer_table         @ 080cf9e8 400f0008
PTR_game_str_ja_080cf9ec:
    .word  game_str_ja                    @ 080cf9ec 109cdb09
DAT_080cf9f0:
    .word  0x00000a01                     @ 080cf9f0 010a0000

@ indeg=1, caller: FUN_080c7ea0 (card display state dispatch). Renders card name JP text to BG tile VRAM. Steps: (1) setup_line_buf_with_font_and_align(font=0x17, width=0x10, mode=1, align=2); (2) reads gFontState+0x0a03 x-offset and global lang flags (0x02006c2c+0x6c2c, mask 0x7 and 0x2) to determine render language mode, writes back to gFontState+0x8; (3) selects font base ptr from font_jp_base_table, writes to gFontState+0x4; (4) sets gFontState+0x15 bit6; (5) render_jp_string_to_tile_line (start=(2,2), palette=0xc, src=DAT_080cfab8=0x0201f441); (6) computes tile row count from render width (r4+0x30 asrs #3), writes to gFontState+0x0a02; (7) conditionally strb tile_row (only if gFontState+0x0a16=gFontState+0x0a17=0); (8) write_line_buf_to_bg_tile_vram to BG VRAM 0x06014000. Constants: FONT_ID=0x17; WIDTH=0x10; TILE_ROW_OFFSET=0x0a02; FLAG_A=0x0a16; FLAG_B=0x0a17; VRAM_BG=0x06014000.
render_card_name_jp_to_bg_tile_vram:
    push {r4,r5,r6,r7,lr}                    @ 080cf9f4 f0b5
    sub sp,#0x4                              @ 080cf9f6 81b0
    movs r6,#0x0    @ 080cf9f8 0026
    movs r0,#0x17    @ 080cf9fa 1720
    movs r1,#0x10    @ 080cf9fc 1021
    movs r2,#0x1    @ 080cf9fe 0122
    movs r3,#0x2    @ 080cfa00 0223
    bl setup_line_buf_with_font_and_align    @ 080cfa02 21f05df9
    ldr r2, DAT_080cfaa8                     @ 080cfa06 284a
    ldr r0, DAT_080cfaac                     @ 080cfa08 2848
    ldr r1, DAT_080cfab0                     @ 080cfa0a 2949
    adds r0,r0,r1    @ 080cfa0c 4018
    movs r7,#0x7    @ 080cfa0e 0727
    adds r1,r7,#0x0    @ 080cfa10 391c
    ldrb r0,[r0,#0x0]                        @ 080cfa12 0078
    ands r1,r0    @ 080cfa14 0140
    rsbs r1,r1,#0    @ 080cfa16 4942
    lsrs r1,r1,#0x1f    @ 080cfa18 c90f
    movs r0,#0x2    @ 080cfa1a 0220
    rsbs r0,r0,#0    @ 080cfa1c 4042
    ldrb r3,[r2,#0x8]                        @ 080cfa1e 137a
    ands r0,r3    @ 080cfa20 1840
    orrs r0,r1    @ 080cfa22 0843
    movs r1,#0x2    @ 080cfa24 0221
    orrs r0,r1    @ 080cfa26 0843
    strb r0,[r2,#0x8]                        @ 080cfa28 1072
    ldr r3, PTR_font_jp_base_table_080cfab4  @ 080cfa2a 224b
    lsls r1,r0,#0x1e    @ 080cfa2c 8107
    lsrs r1,r1,#0x1f    @ 080cfa2e c90f
    lsls r1,r1,#0x2    @ 080cfa30 8900
    lsls r0,r0,#0x1f    @ 080cfa32 c007
    lsrs r0,r0,#0x1f    @ 080cfa34 c00f
    lsls r0,r0,#0x3    @ 080cfa36 c000
    adds r1,r1,r0    @ 080cfa38 0918
    adds r1,r1,r3    @ 080cfa3a c918
    ldr r0,[r1,#0x0]                         @ 080cfa3c 0868
    str r0,[r2,#0x4]                         @ 080cfa3e 5060
    movs r0,#0x40    @ 080cfa40 4020
    ldrb r1,[r2,#0x15]                       @ 080cfa42 517d
    orrs r0,r1    @ 080cfa44 0843
    strb r0,[r2,#0x15]                       @ 080cfa46 5075
    ldr r5, DAT_080cfab8                     @ 080cfa48 1b4d
    str r6,[sp,#0x0]                         @ 080cfa4a 0096
    movs r0,#0x2    @ 080cfa4c 0220
    movs r1,#0x2    @ 080cfa4e 0221
    adds r2,r5,#0x0    @ 080cfa50 2a1c
    movs r3,#0xc    @ 080cfa52 0c23
    bl render_jp_string_to_tile_line         @ 080cfa54 f7f734fe
    adds r4,r0,#0x0    @ 080cfa58 041c
    adds r1,r4,#0x3    @ 080cfa5a e11c
    ldr r2, DAT_080cfabc                     @ 080cfa5c 174a
    adds r0,r5,r2    @ 080cfa5e a818
    strh r1,[r0,#0x0]                        @ 080cfa60 0180
    adds r4,#0x30    @ 080cfa62 3034
    ldr r0, DAT_080cfac0                     @ 080cfa64 1648
    movs r1,#0x0    @ 080cfa66 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cfa68 23f0b4fe
    adds r4,#0x18    @ 080cfa6c 1834
    adds r0,r4,#0x0    @ 080cfa6e 201c
    cmp r4,#0x0                              @ 080cfa70 002c
    bge LAB_080cfa76                         @ 080cfa72 00da
    adds r0,r4,#0x7    @ 080cfa74 e01d
LAB_080cfa76:
    asrs r6,r0,#0x3    @ 080cfa76 c610
    ands r4,r7    @ 080cfa78 3c40
    cmp r4,#0x0                              @ 080cfa7a 002c
    beq LAB_080cfa80                         @ 080cfa7c 00d0
    adds r6,#0x1    @ 080cfa7e 0136
LAB_080cfa80:
    ldr r3, DAT_080cfac4                     @ 080cfa80 104b
    adds r0,r5,r3    @ 080cfa82 e818
    ldrb r0,[r0,#0x0]                        @ 080cfa84 0078
    lsrs r2,r0,#0x1    @ 080cfa86 4208
    ldr r0, DAT_080cfac8                     @ 080cfa88 0f48
    adds r1,r5,r0    @ 080cfa8a 2918
    movs r0,#0x1    @ 080cfa8c 0120
    ldrb r1,[r1,#0x0]                        @ 080cfa8e 0978
    ands r0,r1    @ 080cfa90 0840
    lsls r0,r0,#0x7    @ 080cfa92 c001
    orrs r0,r2    @ 080cfa94 1043
    cmp r0,#0x0                              @ 080cfa96 0028
    bne LAB_080cfaa0                         @ 080cfa98 02d1
    ldr r1, DAT_080cfacc                     @ 080cfa9a 0c49
    adds r0,r5,r1    @ 080cfa9c 6818
    strb r6,[r0,#0x0]                        @ 080cfa9e 0670
LAB_080cfaa0:
    add sp,#0x4                              @ 080cfaa0 01b0
    pop {r4,r5,r6,r7}                        @ 080cfaa2 f0bc
    pop {r0}                                 @ 080cfaa4 01bc
    bx r0                                    @ 080cfaa6 0047
DAT_080cfaa8:
    .word  0x02006ed0                     @ 080cfaa8 d06e0002
DAT_080cfaac:
    .word  0x02000000                     @ 080cfaac 00000002
DAT_080cfab0:
    .word  0x00006c2c                     @ 080cfab0 2c6c0000
PTR_font_jp_base_table_080cfab4:
    .word  font_jp_base_table             @ 080cfab4 54f8e509
DAT_080cfab8:
    .word  0x0201f441                     @ 080cfab8 41f40102
DAT_080cfabc:
    .word  0x00000a03                     @ 080cfabc 030a0000
DAT_080cfac0:
    .word  0x06014000                     @ 080cfac0 00400106
DAT_080cfac4:
    .word  0x00000a16                     @ 080cfac4 160a0000
DAT_080cfac8:
    .word  0x00000a17                     @ 080cfac8 170a0000
DAT_080cfacc:
    .word  0x00000a02                     @ 080cfacc 020a0000

@ Card-list OAM row render branch for rarity_flag variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 5. Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword x_base. Reads gFontState[0x0a18] word bits[23:8] (mask=0xff<<9): 0x200 -> rarity_level=3; 0x400 -> rarity_level=4; default -> 4. Calls write_card_list_oam_row_strip (slot=0x30). Main loop r6=0..19 (20 iterations): calls write_oam_entry_from_packed_args; uses __modsi3 (mod 10) and __divsi3 (div 10) for column wrap coordinates. No APCS inputs. Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; RARITY_FIELD_OFFSET=0x0a18 bits[23:8]; RARITY_A=0x200 r7=3; RARITY_B=0x400 r7=4; STRIP_LOOP_COUNT=20; OAM_SLOT_STRIP=0x30; DIVISOR_COLS=10.
render_card_list_oam_row_by_rarity_flag:
    push {r4,r5,r6,r7,lr}                    @ 080cfad0 f0b5
    .hword 0x4657    @ 080cfad2 5746
    .hword 0x464e    @ 080cfad4 4e46
    .hword 0x4645    @ 080cfad6 4546
    push {r5,r6,r7}                          @ 080cfad8 e0b4
    ldr r2, DAT_080cfb18                     @ 080cfada 0f4a
    ldr r1, DAT_080cfb1c                     @ 080cfadc 0f49
    adds r0,r2,r1    @ 080cfade 5018
    ldrb r0,[r0,#0x0]                        @ 080cfae0 0078
    lsrs r1,r0,#0x1    @ 080cfae2 4108
    movs r0,#0xa    @ 080cfae4 0a20
    subs r0,r0,r1    @ 080cfae6 401a
    lsls r0,r0,#0x3    @ 080cfae8 c000
    ldr r3, DAT_080cfb20                     @ 080cfaea 0d4b
    adds r1,r2,r3    @ 080cfaec d118
    ldrh r1,[r1,#0x0]                        @ 080cfaee 0988
    adds r1,r1,r0    @ 080cfaf0 0918
    .hword 0x4689    @ 080cfaf2 8946
    movs r0,#0x12    @ 080cfaf4 1220
    .hword 0x4682    @ 080cfaf6 8246
    ldr r1, DAT_080cfb24                     @ 080cfaf8 0a49
    adds r2,r2,r1    @ 080cfafa 5218
    ldr r2,[r2,#0x0]                         @ 080cfafc 1268
    movs r0,#0xff    @ 080cfafe ff20
    lsls r0,r0,#0x9    @ 080cfb00 4002
    ands r2,r0    @ 080cfb02 0240
    movs r0,#0x80    @ 080cfb04 8020
    lsls r0,r0,#0x2    @ 080cfb06 8000
    cmp r2,r0                                @ 080cfb08 8242
    beq LAB_080cfb14                         @ 080cfb0a 03d0
    movs r0,#0x80    @ 080cfb0c 8020
    lsls r0,r0,#0x3    @ 080cfb0e c000
    cmp r2,r0                                @ 080cfb10 8242
    bne LAB_080cfb28                         @ 080cfb12 09d1
LAB_080cfb14:
    movs r7,#0x3    @ 080cfb14 0327
    b LAB_080cfb2a                           @ 080cfb16 08e0
DAT_080cfb18:
    .word  0x0201f440                     @ 080cfb18 40f40102
DAT_080cfb1c:
    .word  0x00000a03                     @ 080cfb1c 030a0000
DAT_080cfb20:
    .word  0x00000a04                     @ 080cfb20 040a0000
DAT_080cfb24:
    .word  0x00000a18                     @ 080cfb24 180a0000
LAB_080cfb28:
    movs r7,#0x4    @ 080cfb28 0427
LAB_080cfb2a:
    ldr r4, DAT_080cfba4                     @ 080cfb2a 1e4c
    ldr r2, DAT_080cfba8                     @ 080cfb2c 1e4a
    adds r0,r4,r2    @ 080cfb2e a018
    ldrb r3,[r0,#0x0]                        @ 080cfb30 0378
    lsrs r0,r3,#0x1    @ 080cfb32 5808
    movs r1,#0xa    @ 080cfb34 0a21
    subs r1,r1,r0    @ 080cfb36 091a
    lsls r1,r1,#0x3    @ 080cfb38 c900
    movs r2,#0xfe    @ 080cfb3a fe22
    lsls r2,r2,#0x1    @ 080cfb3c 5200
    movs r0,#0x30    @ 080cfb3e 3020
    bl write_card_list_oam_row_strip         @ 080cfb40 f7f7f6fc
    ldr r3, DAT_080cfbac                     @ 080cfb44 194b
    adds r0,r4,r3    @ 080cfb46 e018
    ldrb r0,[r0,#0x0]                        @ 080cfb48 0078
    lsrs r0,r0,#0x1    @ 080cfb4a 4008
    movs r1,#0x3    @ 080cfb4c 0321
    ands r0,r1    @ 080cfb4e 0840
    cmp r0,#0x1                              @ 080cfb50 0128
    bls LAB_080cfb56                         @ 080cfb52 00d9
    movs r7,#0x3    @ 080cfb54 0327
LAB_080cfb56:
    movs r6,#0x0    @ 080cfb56 0026
    ldr r0, DAT_080cfbb0                     @ 080cfb58 1548
    adds r0,r0,r4    @ 080cfb5a 0019
    .hword 0x4680    @ 080cfb5c 8046
LAB_080cfb5e:
    adds r0,r6,#0x0    @ 080cfb5e 301c
    movs r1,#0xa    @ 080cfb60 0a21
    bl __modsi3                              @ 080cfb62 3ef09bfd
    adds r4,r0,#0x0    @ 080cfb66 041c
    .hword 0x4655    @ 080cfb68 5546
    muls r5,r4    @ 080cfb6a 6543
    adds r5,#0x32    @ 080cfb6c 3235
    adds r0,r6,#0x0    @ 080cfb6e 301c
    movs r1,#0xa    @ 080cfb70 0a21
    bl __divsi3                              @ 080cfb72 3ef047fd
    lsls r1,r0,#0x3    @ 080cfb76 c100
    adds r1,r1,r0    @ 080cfb78 0918
    lsls r1,r1,#0x1    @ 080cfb7a 4900
    add r1,r9                                @ 080cfb7c 4944
    lsls r1,r1,#0x10    @ 080cfb7e 0904
    orrs r1,r5    @ 080cfb80 2943
    lsls r4,r4,#0x1    @ 080cfb82 6400
    movs r2,#0xc0    @ 080cfb84 c022
    lsls r2,r2,#0x1    @ 080cfb86 5200
    adds r4,r4,r2    @ 080cfb88 a418
    lsls r0,r0,#0x6    @ 080cfb8a 8001
    adds r4,r4,r0    @ 080cfb8c 2418
    .hword 0x4643    @ 080cfb8e 4346
    ldrh r3,[r3,#0x0]                        @ 080cfb90 1b88
    lsls r0,r3,#0x14    @ 080cfb92 1805
    lsrs r0,r0,#0x18    @ 080cfb94 000e
    cmp r6,r0                                @ 080cfb96 8642
    bne LAB_080cfbb4                         @ 080cfb98 0cd1
    lsls r0,r7,#0xc    @ 080cfb9a 3803
    orrs r0,r4    @ 080cfb9c 2043
    lsls r0,r0,#0x10    @ 080cfb9e 0004
    b LAB_080cfbbc                           @ 080cfba0 0ce0
    .zero  0x2
DAT_080cfba4:
    .word  0x0201f440                     @ 080cfba4 40f40102
DAT_080cfba8:
    .word  0x00000a03                     @ 080cfba8 030a0000
DAT_080cfbac:
    .word  0x00000a1b                     @ 080cfbac 1b0a0000
DAT_080cfbb0:
    .word  0x00000a0e                     @ 080cfbb0 0e0a0000
LAB_080cfbb4:
    movs r0,#0xc0    @ 080cfbb4 c020
    lsls r0,r0,#0x6    @ 080cfbb6 8001
    orrs r4,r0    @ 080cfbb8 0443
    lsls r0,r4,#0x10    @ 080cfbba 2004
LAB_080cfbbc:
    lsrs r2,r0,#0x10    @ 080cfbbc 020c
    adds r0,r1,#0x0    @ 080cfbbe 081c
    movs r1,#0x40    @ 080cfbc0 4021
    bl write_oam_entry_from_packed_args      @ 080cfbc2 26f0d3fa
    adds r6,#0x1    @ 080cfbc6 0136
    cmp r6,#0x13                             @ 080cfbc8 132e
    ble LAB_080cfb5e                         @ 080cfbca c8dd
    pop {r3,r4,r5}                           @ 080cfbcc 38bc
    .hword 0x4698    @ 080cfbce 9846
    .hword 0x46a1    @ 080cfbd0 a146
    .hword 0x46aa    @ 080cfbd2 aa46
    pop {r4,r5,r6,r7}                        @ 080cfbd4 f0bc
    pop {r0}                                 @ 080cfbd6 01bc
    bx r0                                    @ 080cfbd8 0047
    .zero  0x2

@ Card-list OAM row render branch for stat_state variant. indeg=1; caller: FUN_080c82e4 (card display master tick). Reads gFontState[0x0a03] row_count -> OAM Y; gFontState[0x0a04] x_base; gFontState[0x0a0e] slot_nibble bits[23:16]; gFontState[0x0a18] state_val bits[23:16]. Four-way dispatch on state_val: state=0: writes 4 OAM strips (write_oam_entry_from_packed_args, attr0=0x32, slot=0x60); then checks gPrng[0x148] bit4(0x10)->find_next_occupied_slot_forward+nibble write+sync; bit5(0x20)->find_next_occupied_slot_backward+nibble write+sync; bits6-7(0xc0)->mod20+find_next_occupied_slot_backward+sync; bit0(0x01)->write gP1LifePoints+0x148+sync. state=1: nibble_B/C update loop (gFontState[0x0a1b/0x0a1c]). Side effects: [gFontState+0x0a0e] nibble bits[11:4] updated; [gFontState+0x0a18] state bits updated; [gP1LifePoints+0x148] written (state=0 bit0). Constants: SLOT_NIBBLE_OFFSET=0x0a0e; STATE_OFFSET=0x0a18; OAM_STRIP_COUNT=4; ATTR0_STRIP=0x32; OAM_SLOT=0x60; WRAP_MODULO=0x14.
render_card_list_oam_row_by_stat_state:
    push {r4,r5,r6,r7,lr}                    @ 080cfbdc f0b5
    .hword 0x4647    @ 080cfbde 4746
    push {r7}                                @ 080cfbe0 80b4
    ldr r2, DAT_080cfc20                     @ 080cfbe2 0f4a
    ldr r1, DAT_080cfc24                     @ 080cfbe4 0f49
    adds r0,r2,r1    @ 080cfbe6 5018
    ldrb r0,[r0,#0x0]                        @ 080cfbe8 0078
    lsrs r1,r0,#0x1    @ 080cfbea 4108
    movs r0,#0xa    @ 080cfbec 0a20
    subs r0,r0,r1    @ 080cfbee 401a
    lsls r0,r0,#0x3    @ 080cfbf0 c000
    ldr r3, DAT_080cfc28                     @ 080cfbf2 0d4b
    adds r1,r2,r3    @ 080cfbf4 d118
    ldrh r1,[r1,#0x0]                        @ 080cfbf6 0988
    adds r3,r1,r0    @ 080cfbf8 0b18
    ldr r4, DAT_080cfc2c                     @ 080cfbfa 0c4c
    adds r6,r2,r4    @ 080cfbfc 1619
    ldrh r0,[r6,#0x0]                        @ 080cfbfe 3088
    lsls r1,r0,#0x14    @ 080cfc00 0105
    lsrs r5,r1,#0x18    @ 080cfc02 0d0e
    ldr r0, DAT_080cfc30                     @ 080cfc04 0a48
    adds r4,r2,r0    @ 080cfc06 1418
    ldr r0,[r4,#0x0]                         @ 080cfc08 2068
    lsls r0,r0,#0xf    @ 080cfc0a c003
    lsrs r0,r0,#0x18    @ 080cfc0c 000e
    cmp r0,#0x1                              @ 080cfc0e 0128
    bne LAB_080cfc14                         @ 080cfc10 00d1
    b LAB_080cfdca                           @ 080cfc12 dae0
LAB_080cfc14:
    cmp r0,#0x1                              @ 080cfc14 0128
    bgt LAB_080cfc34                         @ 080cfc16 0ddc
    cmp r0,#0x0                              @ 080cfc18 0028
    beq LAB_080cfc42                         @ 080cfc1a 12d0
    b LAB_080cff44                           @ 080cfc1c 92e1
    .zero  0x2
DAT_080cfc20:
    .word  0x0201f440                     @ 080cfc20 40f40102
DAT_080cfc24:
    .word  0x00000a03                     @ 080cfc24 030a0000
DAT_080cfc28:
    .word  0x00000a04                     @ 080cfc28 040a0000
DAT_080cfc2c:
    .word  0x00000a0e                     @ 080cfc2c 0e0a0000
DAT_080cfc30:
    .word  0x00000a18                     @ 080cfc30 180a0000
LAB_080cfc34:
    cmp r0,#0x2                              @ 080cfc34 0228
    bne LAB_080cfc3a                         @ 080cfc36 00d1
    b LAB_080cfe48                           @ 080cfc38 06e1
LAB_080cfc3a:
    cmp r0,#0x3                              @ 080cfc3a 0328
    bne LAB_080cfc40                         @ 080cfc3c 00d1
    b LAB_080cfecc                           @ 080cfc3e 45e1
LAB_080cfc40:
    b LAB_080cff44                           @ 080cfc40 80e1
LAB_080cfc42:
    movs r4,#0x0    @ 080cfc42 0024
    adds r7,r3,#0x0    @ 080cfc44 1f1c
    adds r7,#0x24    @ 080cfc46 2437
    movs r6,#0x32    @ 080cfc48 3226
LAB_080cfc4a:
    lsls r0,r7,#0x10    @ 080cfc4a 3804
    orrs r0,r6    @ 080cfc4c 3043
    lsls r2,r4,#0x12    @ 080cfc4e a204
    movs r1,#0xa0    @ 080cfc50 a021
    lsls r1,r1,#0x11    @ 080cfc52 4904
    adds r2,r2,r1    @ 080cfc54 5218
    lsrs r2,r2,#0x10    @ 080cfc56 120c
    movs r1,#0x81    @ 080cfc58 8121
    lsls r1,r1,#0x7    @ 080cfc5a c901
    bl write_oam_entry_from_packed_args      @ 080cfc5c 26f086fa
    adds r6,#0x20    @ 080cfc60 2036
    adds r4,#0x1    @ 080cfc62 0134
    cmp r4,#0x3                              @ 080cfc64 032c
    ble LAB_080cfc4a                         @ 080cfc66 f0dd
    ldr r0, PTR_gPrng_080cfcb0               @ 080cfc68 1148
    movs r2,#0xa4    @ 080cfc6a a422
    lsls r2,r2,#0x1    @ 080cfc6c 5200
    adds r0,r0,r2    @ 080cfc6e 8018
    ldrh r1,[r0,#0x0]                        @ 080cfc70 0188
    movs r0,#0x10    @ 080cfc72 1020
    ands r0,r1    @ 080cfc74 0840
    cmp r0,#0x0                              @ 080cfc76 0028
    beq LAB_080cfcc8                         @ 080cfc78 26d0
    adds r0,r5,#0x0    @ 080cfc7a 281c
    bl find_next_occupied_slot_forward       @ 080cfc7c fff72cfd
    ldr r2, DAT_080cfcb4                     @ 080cfc80 0c4a
    ldr r4, DAT_080cfcb8                     @ 080cfc82 0d4c
    adds r3,r2,r4    @ 080cfc84 1319
LAB_080cfc86:
    movs r1,#0xff    @ 080cfc86 ff21
    ands r0,r1    @ 080cfc88 0840
    lsls r0,r0,#0x4    @ 080cfc8a 0001
    ldr r1, DAT_080cfcbc                     @ 080cfc8c 0b49
    ldrh r4,[r3,#0x0]                        @ 080cfc8e 1c88
    ands r1,r4    @ 080cfc90 2140
    orrs r1,r0    @ 080cfc92 0143
    strh r1,[r3,#0x0]                        @ 080cfc94 1980
    ldr r0, DAT_080cfcc0                     @ 080cfc96 0a48
    adds r2,r2,r0    @ 080cfc98 1218
LAB_080cfc9a:
    ldr r0,[r2,#0x0]                         @ 080cfc9a 1068
    ldr r1, DAT_080cfcc4                     @ 080cfc9c 0949
    ands r0,r1    @ 080cfc9e 0840
    movs r1,#0x80    @ 080cfca0 8021
    lsls r1,r1,#0x2    @ 080cfca2 8900
    orrs r0,r1    @ 080cfca4 0843
    str r0,[r2,#0x0]                         @ 080cfca6 1060
    movs r0,#0x0    @ 080cfca8 0020
    bl sync_state_and_init_sprite            @ 080cfcaa 29f003ff
    b LAB_080cff44                           @ 080cfcae 49e1
PTR_gPrng_080cfcb0:
    .word  gPrng                          @ 080cfcb0 40000003
DAT_080cfcb4:
    .word  0x0201f440                     @ 080cfcb4 40f40102
DAT_080cfcb8:
    .word  0x00000a0e                     @ 080cfcb8 0e0a0000
DAT_080cfcbc:
    .word  0xfffff00f                     @ 080cfcbc 0ff0ffff
DAT_080cfcc0:
    .word  0x00000a18                     @ 080cfcc0 180a0000
DAT_080cfcc4:
    .word  0xfffe01ff                     @ 080cfcc4 ff01feff
LAB_080cfcc8:
    movs r0,#0x20    @ 080cfcc8 2020
    ands r0,r1    @ 080cfcca 0840
    cmp r0,#0x0                              @ 080cfccc 0028
    beq LAB_080cfce8                         @ 080cfcce 0bd0
    adds r0,r5,#0x0    @ 080cfcd0 281c
    bl find_next_occupied_slot_backward      @ 080cfcd2 fff73ffd
    ldr r2, DAT_080cfce0                     @ 080cfcd6 024a
    ldr r1, DAT_080cfce4                     @ 080cfcd8 0249
    adds r3,r2,r1    @ 080cfcda 5318
    b LAB_080cfc86                           @ 080cfcdc d3e7
    .zero  0x2
DAT_080cfce0:
    .word  0x0201f440                     @ 080cfce0 40f40102
DAT_080cfce4:
    .word  0x00000a0e                     @ 080cfce4 0e0a0000
LAB_080cfce8:
    movs r0,#0xc0    @ 080cfce8 c020
    ands r0,r1    @ 080cfcea 0840
    cmp r0,#0x0                              @ 080cfcec 0028
    beq LAB_080cfd68                         @ 080cfcee 3bd0
    adds r5,#0xa    @ 080cfcf0 0a35
    adds r0,r5,#0x0    @ 080cfcf2 281c
    movs r1,#0x14    @ 080cfcf4 1421
    bl __modsi3                              @ 080cfcf6 3ef0d1fc
    adds r5,r0,#0x0    @ 080cfcfa 051c
    ldr r4, DAT_080cfd28                     @ 080cfcfc 0a4c
    movs r1,#0xa1    @ 080cfcfe a121
    lsls r1,r1,#0x4    @ 080cfd00 0901
    adds r0,r4,r1    @ 080cfd02 6018
    movs r1,#0x1    @ 080cfd04 0121
    lsls r1,r5    @ 080cfd06 a940
    ldr r0,[r0,#0x0]                         @ 080cfd08 0068
    ands r0,r1    @ 080cfd0a 0840
    cmp r0,#0x0                              @ 080cfd0c 0028
    beq LAB_080cfd34                         @ 080cfd0e 11d0
    ldr r3, DAT_080cfd2c                     @ 080cfd10 064b
    adds r2,r4,r3    @ 080cfd12 e218
    movs r0,#0xff    @ 080cfd14 ff20
    ands r5,r0    @ 080cfd16 0540
    lsls r1,r5,#0x4    @ 080cfd18 2901
    ldr r0, DAT_080cfd30                     @ 080cfd1a 0548
    ldrh r4,[r2,#0x0]                        @ 080cfd1c 1488
    ands r0,r4    @ 080cfd1e 2040
    orrs r0,r1    @ 080cfd20 0843
    strh r0,[r2,#0x0]                        @ 080cfd22 1080
    b LAB_080cfd4e                           @ 080cfd24 13e0
    .zero  0x2
DAT_080cfd28:
    .word  0x0201f440                     @ 080cfd28 40f40102
DAT_080cfd2c:
    .word  0x00000a0e                     @ 080cfd2c 0e0a0000
DAT_080cfd30:
    .word  0xfffff00f                     @ 080cfd30 0ff0ffff
LAB_080cfd34:
    adds r0,r5,#0x0    @ 080cfd34 281c
    bl find_next_occupied_slot_backward      @ 080cfd36 fff70dfd
    ldr r1, DAT_080cfd58                     @ 080cfd3a 0749
    adds r2,r4,r1    @ 080cfd3c 6218
    movs r1,#0xff    @ 080cfd3e ff21
    ands r0,r1    @ 080cfd40 0840
    lsls r0,r0,#0x4    @ 080cfd42 0001
    ldr r1, DAT_080cfd5c                     @ 080cfd44 0549
    ldrh r3,[r2,#0x0]                        @ 080cfd46 1388
    ands r1,r3    @ 080cfd48 1940
    orrs r1,r0    @ 080cfd4a 0143
    strh r1,[r2,#0x0]                        @ 080cfd4c 1180
LAB_080cfd4e:
    ldr r2, DAT_080cfd60                     @ 080cfd4e 044a
    ldr r4, DAT_080cfd64                     @ 080cfd50 044c
    adds r2,r2,r4    @ 080cfd52 1219
    b LAB_080cfc9a                           @ 080cfd54 a1e7
    .zero  0x2
DAT_080cfd58:
    .word  0x00000a0e                     @ 080cfd58 0e0a0000
DAT_080cfd5c:
    .word  0xfffff00f                     @ 080cfd5c 0ff0ffff
DAT_080cfd60:
    .word  0x0201f440                     @ 080cfd60 40f40102
DAT_080cfd64:
    .word  0x00000a18                     @ 080cfd64 180a0000
LAB_080cfd68:
    movs r0,#0x1    @ 080cfd68 0120
    ands r0,r1    @ 080cfd6a 0840
    cmp r0,#0x0                              @ 080cfd6c 0028
    beq LAB_080cfdb8                         @ 080cfd6e 23d0
    ldr r1, PTR_gP1LifePoints_080cfda4       @ 080cfd70 0c49
    movs r0,#0xea    @ 080cfd72 ea20
    lsls r0,r0,#0x5    @ 080cfd74 4001
    adds r1,r1,r0    @ 080cfd76 0918
    ldr r4, DAT_080cfda8                     @ 080cfd78 0b4c
    ldr r2, DAT_080cfdac                     @ 080cfd7a 0c4a
    adds r0,r4,r2    @ 080cfd7c a018
    ldrh r0,[r0,#0x0]                        @ 080cfd7e 0088
    lsls r0,r0,#0x14    @ 080cfd80 0005
    lsrs r0,r0,#0x18    @ 080cfd82 000e
    adds r0,#0x1    @ 080cfd84 0130
    str r0,[r1,#0x0]                         @ 080cfd86 0860
    movs r0,#0x24    @ 080cfd88 2420
    bl sync_state_and_init_sprite            @ 080cfd8a 29f093fe
    ldr r3, DAT_080cfdb0                     @ 080cfd8e 084b
    adds r4,r4,r3    @ 080cfd90 e418
    ldr r0,[r4,#0x0]                         @ 080cfd92 2068
    ldr r1, DAT_080cfdb4                     @ 080cfd94 0749
    ands r0,r1    @ 080cfd96 0840
    movs r1,#0xc0    @ 080cfd98 c021
    lsls r1,r1,#0x3    @ 080cfd9a c900
LAB_080cfd9c:
    orrs r0,r1    @ 080cfd9c 0843
    str r0,[r4,#0x0]                         @ 080cfd9e 2060
    b LAB_080cff44                           @ 080cfda0 d0e0
    .zero  0x2
PTR_gP1LifePoints_080cfda4:
    .word  gP1LifePoints                  @ 080cfda4 e0c40102
DAT_080cfda8:
    .word  0x0201f440                     @ 080cfda8 40f40102
DAT_080cfdac:
    .word  0x00000a0e                     @ 080cfdac 0e0a0000
DAT_080cfdb0:
    .word  0x00000a18                     @ 080cfdb0 180a0000
DAT_080cfdb4:
    .word  0xfffe01ff                     @ 080cfdb4 ff01feff
LAB_080cfdb8:
    movs r0,#0x2    @ 080cfdb8 0220
    ands r0,r1    @ 080cfdba 0840
    cmp r0,#0x0                              @ 080cfdbc 0028
    bne LAB_080cfdc2                         @ 080cfdbe 00d1
    b LAB_080cff44                           @ 080cfdc0 c0e0
LAB_080cfdc2:
    movs r0,#0x2    @ 080cfdc2 0220
    bl sync_state_and_init_sprite            @ 080cfdc4 29f076fe
    b LAB_080cff44                           @ 080cfdc8 bce0
LAB_080cfdca:
    movs r0,#0x17    @ 080cfdca 1720
    movs r1,#0x2    @ 080cfdcc 0221
    movs r2,#0x1    @ 080cfdce 0122
    movs r3,#0x0    @ 080cfdd0 0023
    bl setup_line_buf_with_font_and_align    @ 080cfdd2 20f075ff
    ldr r2, DAT_080cfe30                     @ 080cfdd6 164a
    ldr r0, DAT_080cfe34                     @ 080cfdd8 1648
    ldr r1, DAT_080cfe38                     @ 080cfdda 1749
    adds r0,r0,r1    @ 080cfddc 4018
    movs r1,#0x7    @ 080cfdde 0721
    ldrb r0,[r0,#0x0]                        @ 080cfde0 0078
    ands r1,r0    @ 080cfde2 0140
    rsbs r1,r1,#0    @ 080cfde4 4942
    lsrs r1,r1,#0x1f    @ 080cfde6 c90f
    movs r0,#0x2    @ 080cfde8 0220
    rsbs r0,r0,#0    @ 080cfdea 4042
    ldrb r3,[r2,#0x8]                        @ 080cfdec 137a
    ands r0,r3    @ 080cfdee 1840
    orrs r0,r1    @ 080cfdf0 0843
    movs r1,#0x2    @ 080cfdf2 0221
    orrs r0,r1    @ 080cfdf4 0843
    strb r0,[r2,#0x8]                        @ 080cfdf6 1072
    ldr r3, PTR_font_jp_base_table_080cfe3c  @ 080cfdf8 104b
    lsls r1,r0,#0x1e    @ 080cfdfa 8107
    lsrs r1,r1,#0x1f    @ 080cfdfc c90f
    lsls r1,r1,#0x2    @ 080cfdfe 8900
    lsls r0,r0,#0x1f    @ 080cfe00 c007
    lsrs r0,r0,#0x1f    @ 080cfe02 c00f
    lsls r0,r0,#0x3    @ 080cfe04 c000
    adds r1,r1,r0    @ 080cfe06 0918
    adds r1,r1,r3    @ 080cfe08 c918
    ldr r0,[r1,#0x0]                         @ 080cfe0a 0868
    str r0,[r2,#0x4]                         @ 080cfe0c 5060
    movs r0,#0x40    @ 080cfe0e 4020
    ldrb r1,[r2,#0x15]                       @ 080cfe10 517d
    orrs r0,r1    @ 080cfe12 0843
    strb r0,[r2,#0x15]                       @ 080cfe14 5075
    ldr r0, DAT_080cfe40                     @ 080cfe16 0a48
    movs r1,#0x0    @ 080cfe18 0021
    movs r2,#0x10    @ 080cfe1a 1022
    movs r3,#0x2    @ 080cfe1c 0223
    bl tile_2d_row_copy                      @ 080cfe1e 27f059fb
    ldr r0,[r4,#0x0]                         @ 080cfe22 2068
    ldr r1, DAT_080cfe44                     @ 080cfe24 0749
    ands r0,r1    @ 080cfe26 0840
    movs r1,#0x80    @ 080cfe28 8021
    lsls r1,r1,#0x3    @ 080cfe2a c900
    b LAB_080cfd9c                           @ 080cfe2c b6e7
    .zero  0x2
DAT_080cfe30:
    .word  0x02006ed0                     @ 080cfe30 d06e0002
DAT_080cfe34:
    .word  0x02000000                     @ 080cfe34 00000002
DAT_080cfe38:
    .word  0x00006c2c                     @ 080cfe38 2c6c0000
PTR_font_jp_base_table_080cfe3c:
    .word  font_jp_base_table             @ 080cfe3c 54f8e509
DAT_080cfe40:
    .word  0x06012800                     @ 080cfe40 00280106
DAT_080cfe44:
    .word  0xfffe01ff                     @ 080cfe44 ff01feff
LAB_080cfe48:
    lsrs r0,r1,#0x18    @ 080cfe48 080e
    ldr r2, DAT_080cfea8                     @ 080cfe4a 174a
    adds r0,r0,r2    @ 080cfe4c 8018
    bl game_str_id_to_row                    @ 080cfe4e 24f0e3ff
    ldr r2, PTR_game_str_pointer_table_080cfeac @ 080cfe52 164a
    lsls r0,r0,#0x10    @ 080cfe54 0004
    lsrs r0,r0,#0x10    @ 080cfe56 000c
    lsls r1,r0,#0x1    @ 080cfe58 4100
    adds r1,r1,r0    @ 080cfe5a 0918
    lsls r1,r1,#0x1    @ 080cfe5c 4900
    ldr r0, DAT_080cfeb0                     @ 080cfe5e 1448
    ldr r3, DAT_080cfeb4                     @ 080cfe60 144b
    adds r0,r0,r3    @ 080cfe62 c018
    ldrb r0,[r0,#0x0]                        @ 080cfe64 0078
    lsls r0,r0,#0x1d    @ 080cfe66 4007
    lsrs r0,r0,#0x1d    @ 080cfe68 400f
    adds r1,r1,r0    @ 080cfe6a 0918
    lsls r1,r1,#0x2    @ 080cfe6c 8900
    adds r1,r1,r2    @ 080cfe6e 8918
    ldr r3,[r1,#0x0]                         @ 080cfe70 0b68
    ldr r0, PTR_game_str_ja_080cfeb8         @ 080cfe72 1148
    adds r3,r3,r0    @ 080cfe74 1b18
    movs r0,#0x2    @ 080cfe76 0220
    movs r1,#0x2    @ 080cfe78 0221
    movs r2,#0x87    @ 080cfe7a 8722
    bl text_render_wrapper                   @ 080cfe7c 22f0fefd
    ldr r0, DAT_080cfebc                     @ 080cfe80 0e48
    movs r1,#0x0    @ 080cfe82 0021
    bl write_line_buf_to_bg_tile_vram        @ 080cfe84 23f0a6fc
    ldr r0, DAT_080cfec0                     @ 080cfe88 0d48
    ldrh r6,[r6,#0x0]                        @ 080cfe8a 3688
    lsls r1,r6,#0x14    @ 080cfe8c 3105
    lsrs r1,r1,#0x18    @ 080cfe8e 090e
    lsls r1,r1,#0x5    @ 080cfe90 4901
    ldr r2, DAT_080cfec4                     @ 080cfe92 0c4a
    adds r1,r1,r2    @ 080cfe94 8918
    movs r2,#0x20    @ 080cfe96 2022
    bl copy_bytes_by_halfword                @ 080cfe98 25f004f8
    ldr r0,[r4,#0x0]                         @ 080cfe9c 2068
    ldr r1, DAT_080cfec8                     @ 080cfe9e 0a49
    ands r0,r1    @ 080cfea0 0840
    str r0,[r4,#0x0]                         @ 080cfea2 2060
    b LAB_080cff44                           @ 080cfea4 4ee0
    .zero  0x2
DAT_080cfea8:
    .word  0x000001f5                     @ 080cfea8 f5010000
PTR_game_str_pointer_table_080cfeac:
    .word  game_str_pointer_table         @ 080cfeac 400f0008
DAT_080cfeb0:
    .word  0x02000000                     @ 080cfeb0 00000002
DAT_080cfeb4:
    .word  0x00006c2c                     @ 080cfeb4 2c6c0000
PTR_game_str_ja_080cfeb8:
    .word  game_str_ja                    @ 080cfeb8 109cdb09
DAT_080cfebc:
    .word  0x06012800                     @ 080cfebc 00280106
DAT_080cfec0:
    .word  0x05000280                     @ 080cfec0 80020005
DAT_080cfec4:
    .word  0x0984ee2c                     @ 080cfec4 2cee8409
DAT_080cfec8:
    .word  0xfffe01ff                     @ 080cfec8 ff01feff
LAB_080cfecc:
    movs r4,#0x0    @ 080cfecc 0024
    adds r7,r3,#0x0    @ 080cfece 1f1c
    adds r7,#0x24    @ 080cfed0 2437
    movs r5,#0x32    @ 080cfed2 3225
LAB_080cfed4:
    lsls r0,r7,#0x10    @ 080cfed4 3804
    orrs r0,r5    @ 080cfed6 2843
    lsls r2,r4,#0x12    @ 080cfed8 a204
    movs r1,#0xa0    @ 080cfeda a021
    lsls r1,r1,#0x11    @ 080cfedc 4904
    adds r2,r2,r1    @ 080cfede 5218
    lsrs r2,r2,#0x10    @ 080cfee0 120c
    movs r1,#0x81    @ 080cfee2 8121
    lsls r1,r1,#0x7    @ 080cfee4 c901
    bl write_oam_entry_from_packed_args      @ 080cfee6 26f041f9
    adds r5,#0x20    @ 080cfeea 2035
    adds r4,#0x1    @ 080cfeec 0134
    cmp r4,#0x3                              @ 080cfeee 032c
    ble LAB_080cfed4                         @ 080cfef0 f0dd
    ldr r4, DAT_080cff38                     @ 080cfef2 114c
    ldr r2, DAT_080cff3c                     @ 080cfef4 114a
    adds r2,r2,r4    @ 080cfef6 1219
    .hword 0x4690    @ 080cfef8 9046
    ldrb r6,[r2,#0x0]                        @ 080cfefa 1678
    lsrs r0,r6,#0x1    @ 080cfefc 7008
    ldr r3, DAT_080cff40                     @ 080cfefe 104b
    adds r4,r4,r3    @ 080cff00 e418
    movs r5,#0x1    @ 080cff02 0125
    adds r2,r5,#0x0    @ 080cff04 2a1c
    ldrb r1,[r4,#0x0]                        @ 080cff06 2178
    ands r2,r1    @ 080cff08 0a40
    lsls r2,r2,#0x7    @ 080cff0a d201
    orrs r2,r0    @ 080cff0c 0243
    adds r3,r2,#0x1    @ 080cff0e 531c
    movs r1,#0x7f    @ 080cff10 7f21
    ands r1,r3    @ 080cff12 1940
    lsls r1,r1,#0x1    @ 080cff14 4900
    adds r0,r5,#0x0    @ 080cff16 281c
    ands r0,r6    @ 080cff18 3040
    orrs r0,r1    @ 080cff1a 0843
    .hword 0x4641    @ 080cff1c 4146
    strb r0,[r1,#0x0]                        @ 080cff1e 0870
    lsrs r3,r3,#0x7    @ 080cff20 db09
    ands r3,r5    @ 080cff22 2b40
    movs r0,#0x2    @ 080cff24 0220
    rsbs r0,r0,#0    @ 080cff26 4042
    ldrb r1,[r4,#0x0]                        @ 080cff28 2178
    ands r0,r1    @ 080cff2a 0840
    orrs r0,r3    @ 080cff2c 1843
    strb r0,[r4,#0x0]                        @ 080cff2e 2070
    cmp r2,#0x1f                             @ 080cff30 1f2a
    bls LAB_080cff44                         @ 080cff32 07d9
    movs r0,#0x1    @ 080cff34 0120
    b LAB_080cff46                           @ 080cff36 06e0
DAT_080cff38:
    .word  0x0201f440                     @ 080cff38 40f40102
DAT_080cff3c:
    .word  0x00000a1b                     @ 080cff3c 1b0a0000
DAT_080cff40:
    .word  0x00000a1c                     @ 080cff40 1c0a0000
LAB_080cff44:
    movs r0,#0x0    @ 080cff44 0020
LAB_080cff46:
    pop {r3}                                 @ 080cff46 08bc
    .hword 0x4698    @ 080cff48 9846
    pop {r4,r5,r6,r7}                        @ 080cff4a f0bc
    pop {r1}                                 @ 080cff4c 02bc
    bx r1                                    @ 080cff4e 0847

@ 由 FUN_080c7950 (vram/card_stats) 和 FUN_080c7ea0 (window/vram/display/card) 调用. 入口将 r0 低 16 位提取为 r4 (palette_index), 高 16 位提取为 r5 (tile_offset). 首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x4000 halfword). 读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的两个标志位决定是否执行后续写入; 若均为 0 则跳过. 满足后: 将 palette_index 写入状态字段 0x0a0c (halfword, 通过掩码 0x7fff/0xffff8000 保留低 15 位), 将 tile_offset (r5) 写入状态字段 0x0a0d byte (bit[6:0], mask 0x7f). 最后固定写入状态字段 0x0a01 := 7. r0: u32 packed_params (低 16 位=palette_index [0..0x7fff], 高 16 位=tile_offset [0..0x7f]). Constants: VRAM_BG_BASE=0x06014000, STATE_BASE=0x0201f440, OFFSET_FLAG_A=0x0a17, OFFSET_FLAG_B=0x0a18, MASK_15BIT_LO=0x7fff, STATE_DONE=7.
init_field_slot_tile_attrs:
    push {r4,r5,lr}                          @ 080cff50 30b5
    lsls r1,r0,#0x10    @ 080cff52 0104
    lsrs r4,r1,#0x10    @ 080cff54 0c0c
    lsrs r5,r0,#0x10    @ 080cff56 050c
    ldr r0, DAT_080cffb0                     @ 080cff58 1548
    movs r1,#0x80    @ 080cff5a 8021
    lsls r1,r1,#0x7    @ 080cff5c c901
    bl zero_fill_by_halfword                 @ 080cff5e 24f089ff
    ldr r3, DAT_080cffb4                     @ 080cff62 144b
    ldr r1, DAT_080cffb8                     @ 080cff64 1449
    adds r0,r3,r1    @ 080cff66 5818
    ldrb r0,[r0,#0x0]                        @ 080cff68 0078
    lsrs r2,r0,#0x1    @ 080cff6a 4208
    ldr r0, DAT_080cffbc                     @ 080cff6c 1348
    adds r1,r3,r0    @ 080cff6e 1918
    movs r0,#0x1    @ 080cff70 0120
    ldrb r1,[r1,#0x0]                        @ 080cff72 0978
    ands r0,r1    @ 080cff74 0840
    lsls r0,r0,#0x7    @ 080cff76 c001
    orrs r0,r2    @ 080cff78 1043
    cmp r0,#0x0                              @ 080cff7a 0028
    bne LAB_080cffa0                         @ 080cff7c 10d1
    ldr r1, DAT_080cffc0                     @ 080cff7e 1049
    adds r2,r3,r1    @ 080cff80 5a18
    ldr r1, DAT_080cffc4                     @ 080cff82 1049
    ands r1,r4    @ 080cff84 2140
    ldr r0, DAT_080cffc8                     @ 080cff86 1048
    ldrh r4,[r2,#0x0]                        @ 080cff88 1488
    ands r0,r4    @ 080cff8a 2040
    orrs r0,r1    @ 080cff8c 0843
    strh r0,[r2,#0x0]                        @ 080cff8e 1080
    ldr r0, DAT_080cffcc                     @ 080cff90 0e48
    adds r2,r3,r0    @ 080cff92 1a18
    lsls r1,r5,#0x7    @ 080cff94 e901
    movs r0,#0x7f    @ 080cff96 7f20
    ldrb r4,[r2,#0x0]                        @ 080cff98 1478
    ands r0,r4    @ 080cff9a 2040
    orrs r0,r1    @ 080cff9c 0843
    strb r0,[r2,#0x0]                        @ 080cff9e 1070
LAB_080cffa0:
    ldr r0, DAT_080cffd0                     @ 080cffa0 0b48
    adds r1,r3,r0    @ 080cffa2 1918
    movs r0,#0x7    @ 080cffa4 0720
    strb r0,[r1,#0x0]                        @ 080cffa6 0870
    pop {r4,r5}                              @ 080cffa8 30bc
    pop {r0}                                 @ 080cffaa 01bc
    bx r0                                    @ 080cffac 0047
    .zero  0x2
DAT_080cffb0:
    .word  0x06014000                     @ 080cffb0 00400106
DAT_080cffb4:
    .word  0x0201f440                     @ 080cffb4 40f40102
DAT_080cffb8:
    .word  0x00000a17                     @ 080cffb8 170a0000
DAT_080cffbc:
    .word  0x00000a18                     @ 080cffbc 180a0000
DAT_080cffc0:
    .word  0x00000a0c                     @ 080cffc0 0c0a0000
DAT_080cffc4:
    .word  0x00007fff                     @ 080cffc4 ff7f0000
DAT_080cffc8:
    .word  0xffff8000                     @ 080cffc8 0080ffff
DAT_080cffcc:
    .word  0x00000a0d                     @ 080cffcc 0d0a0000
DAT_080cffd0:
    .word  0x00000a01                     @ 080cffd0 010a0000

@ 由 FUN_080c7ea0 (window/vram/display/card_data/duel_field 全标签主控) 独占调用 (indeg=1). 综合执行以下操作: (1) 读状态字段 (0x0201f440+0x0a0c) 的卡牌 ID (15 位), 调用 ensure_card_id_cache_entry 确保卡牌数据已缓存; (2) 读下一个槽位 ID, 调用 find_zone_descriptor_by_slot_id 和 get_zone_slot_ptr 获取区域插槽指针; (3) 读插槽中卡牌 face_down bit, 与 0x4020 合并存入 sp+4; (4) 初始化 JP 文字行缓冲 (setup_line_buf_with_font_and_align); (5) 设置语言模式 flag (font_jp_base_table 查找); (6) render_jp_string_to_tile_line 渲染卡牌名称 JP 文字; (7) write_line_buf_to_bg_tile_vram 写 BG tile VRAM; (8) 两次 load_card_list_small_image 加载小图; (9) render_large_card_display_by_mode 渲染大卡图. Constants: STATE_BASE=0x0201f440, OFFSET_CARD_SLOT=0x0a0c, FLAG_FACE_DOWN=0x4020, VRAM_BG=0x06014000, gP1LifePoints_BASE=0x02023130.
render_duel_zone_card_detail_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080cffd4 f0b5
    .hword 0x4657    @ 080cffd6 5746
    .hword 0x464e    @ 080cffd8 4e46
    .hword 0x4645    @ 080cffda 4546
    push {r5,r6,r7}                          @ 080cffdc e0b4
    sub sp,#0x8                              @ 080cffde 82b0
    movs r0,#0x0    @ 080cffe0 0020
    .hword 0x4680    @ 080cffe2 8046
    ldr r5, DAT_080d0118                     @ 080cffe4 4c4d
    ldr r1, DAT_080d011c                     @ 080cffe6 4d49
    adds r1,r1,r5    @ 080cffe8 4919
    .hword 0x4689    @ 080cffea 8946
    ldrh r2,[r1,#0x0]                        @ 080cffec 0a88
    lsls r0,r2,#0x11    @ 080cffee 5004
    lsrs r0,r0,#0x11    @ 080cfff0 400c
    bl ensure_card_id_cache_entry            @ 080cfff2 fcf769fc
    adds r6,r0,#0x0    @ 080cfff6 061c
    .hword 0x464b    @ 080cfff8 4b46
    ldrh r3,[r3,#0x0]                        @ 080cfffa 1b88
    lsls r0,r3,#0x11    @ 080cfffc 5804
    lsrs r0,r0,#0x11    @ 080cfffe 400c
    bl find_zone_descriptor_by_slot_id       @ 080d0000 60f7f2fe
    adds r2,r0,#0x0    @ 080d0004 021c
    lsls r0,r2,#0x18    @ 080d0006 1006
    lsrs r0,r0,#0x18    @ 080d0008 000e
    lsls r1,r2,#0x10    @ 080d000a 1104
    lsrs r1,r1,#0x18    @ 080d000c 090e
    lsrs r2,r2,#0x10    @ 080d000e 120c
    bl get_zone_slot_ptr                     @ 080d0010 6bf750f9
    ldr r0,[r0,#0x0]                         @ 080d0014 0068
    lsls r0,r0,#0x12    @ 080d0016 8004
    movs r4,#0x1    @ 080d0018 0124
    lsrs r0,r0,#0x1f    @ 080d001a c00f
    ldr r1, DAT_080d0120                     @ 080d001c 4049
    orrs r0,r1    @ 080d001e 0843
    str r0,[sp,#0x4]                         @ 080d0020 0190
    movs r0,#0x17    @ 080d0022 1720
    movs r1,#0x10    @ 080d0024 1021
    movs r2,#0x1    @ 080d0026 0122
    movs r3,#0x2    @ 080d0028 0223
    bl setup_line_buf_with_font_and_align    @ 080d002a 20f049fe
    ldr r2, DAT_080d0124                     @ 080d002e 3d4a
    ldr r0, DAT_080d0128                     @ 080d0030 3d48
    ldr r1, DAT_080d012c                     @ 080d0032 3e49
    adds r0,r0,r1    @ 080d0034 4018
    movs r3,#0x7    @ 080d0036 0723
    .hword 0x469a    @ 080d0038 9a46
    .hword 0x4651    @ 080d003a 5146
    ldrb r0,[r0,#0x0]                        @ 080d003c 0078
    ands r1,r0    @ 080d003e 0140
    rsbs r1,r1,#0    @ 080d0040 4942
    lsrs r1,r1,#0x1f    @ 080d0042 c90f
    movs r0,#0x2    @ 080d0044 0220
    rsbs r0,r0,#0    @ 080d0046 4042
    ldrb r3,[r2,#0x8]                        @ 080d0048 137a
    ands r0,r3    @ 080d004a 1840
    orrs r0,r1    @ 080d004c 0843
    movs r1,#0x2    @ 080d004e 0221
    orrs r0,r1    @ 080d0050 0843
    strb r0,[r2,#0x8]                        @ 080d0052 1072
    ldr r3, PTR_font_jp_base_table_080d0130  @ 080d0054 364b
    lsls r1,r0,#0x1e    @ 080d0056 8107
    lsrs r1,r1,#0x1f    @ 080d0058 c90f
    lsls r1,r1,#0x2    @ 080d005a 8900
    lsls r0,r0,#0x1f    @ 080d005c c007
    lsrs r0,r0,#0x1f    @ 080d005e c00f
    lsls r0,r0,#0x3    @ 080d0060 c000
    adds r1,r1,r0    @ 080d0062 0918
    adds r1,r1,r3    @ 080d0064 c918
    ldr r0,[r1,#0x0]                         @ 080d0066 0868
    str r0,[r2,#0x4]                         @ 080d0068 5060
    movs r0,#0x40    @ 080d006a 4020
    ldrb r1,[r2,#0x15]                       @ 080d006c 517d
    orrs r0,r1    @ 080d006e 0843
    strb r0,[r2,#0x15]                       @ 080d0070 5075
    adds r2,r5,#0x1    @ 080d0072 6a1c
    .hword 0x4643    @ 080d0074 4346
    str r3,[sp,#0x0]                         @ 080d0076 0093
    movs r0,#0x2    @ 080d0078 0220
    movs r1,#0x2    @ 080d007a 0221
    movs r3,#0xc    @ 080d007c 0c23
    bl render_jp_string_to_tile_line         @ 080d007e f7f71ffb
    adds r7,r0,#0x0    @ 080d0082 071c
    ldr r0, DAT_080d0134                     @ 080d0084 2b48
    movs r1,#0x0    @ 080d0086 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d0088 23f0a4fb
    ldr r1, DAT_080d0138                     @ 080d008c 2a49
    .hword 0x464a    @ 080d008e 4a46
    ldrh r2,[r2,#0x0]                        @ 080d0090 1288
    lsls r0,r2,#0x11    @ 080d0092 5004
    lsrs r0,r0,#0x11    @ 080d0094 400c
    strh r0,[r1,#0x8]                        @ 080d0096 0881
    adds r1,r7,#0x3    @ 080d0098 f91c
    ldr r3, DAT_080d013c                     @ 080d009a 284b
    adds r0,r5,r3    @ 080d009c e818
    strh r1,[r0,#0x0]                        @ 080d009e 0180
    adds r7,#0x24    @ 080d00a0 2437
    movs r3,#0xc6    @ 080d00a2 c623
    lsls r3,r3,#0x2    @ 080d00a4 9b00
    adds r0,r6,#0x0    @ 080d00a6 301c
    movs r1,#0x1    @ 080d00a8 0121
    movs r2,#0x0    @ 080d00aa 0022
    bl load_card_list_small_image            @ 080d00ac f3f786f9
    ldr r1, DAT_080d0140                     @ 080d00b0 2349
    adds r0,r5,r1    @ 080d00b2 6818
    ldrb r0,[r0,#0x0]                        @ 080d00b4 0078
    lsrs r1,r0,#0x7    @ 080d00b6 c109
    movs r3,#0xe6    @ 080d00b8 e623
    lsls r3,r3,#0x2    @ 080d00ba 9b00
    adds r0,r6,#0x0    @ 080d00bc 301c
    movs r2,#0x1    @ 080d00be 0122
    bl load_card_list_small_image            @ 080d00c0 f3f77cf9
    adds r0,r6,#0x0    @ 080d00c4 301c
    add r1,sp,#0x4                           @ 080d00c6 01a9
    movs r2,#0x1    @ 080d00c8 0122
    bl render_large_card_display_by_mode     @ 080d00ca fbf77ff8
    ldr r2, DAT_080d0144                     @ 080d00ce 1d4a
    adds r0,r5,r2    @ 080d00d0 a818
    ldrb r0,[r0,#0x0]                        @ 080d00d2 0078
    lsrs r1,r0,#0x1    @ 080d00d4 4108
    ldr r3, DAT_080d0148                     @ 080d00d6 1c4b
    adds r0,r5,r3    @ 080d00d8 e818
    ldrb r0,[r0,#0x0]                        @ 080d00da 0078
    ands r4,r0    @ 080d00dc 0440
    lsls r4,r4,#0x7    @ 080d00de e401
    orrs r4,r1    @ 080d00e0 0c43
    cmp r4,#0x0                              @ 080d00e2 002c
    bne LAB_080d0108                         @ 080d00e4 10d1
    adds r7,#0x10    @ 080d00e6 1037
    adds r0,r7,#0x0    @ 080d00e8 381c
    cmp r7,#0x0                              @ 080d00ea 002f
    bge LAB_080d00f0                         @ 080d00ec 00da
    adds r0,r7,#0x7    @ 080d00ee f81d
LAB_080d00f0:
    asrs r0,r0,#0x3    @ 080d00f0 c010
    .hword 0x4680    @ 080d00f2 8046
    .hword 0x4650    @ 080d00f4 5046
    ands r7,r0    @ 080d00f6 0740
    cmp r7,#0x0                              @ 080d00f8 002f
    beq LAB_080d0100                         @ 080d00fa 01d0
    movs r1,#0x1    @ 080d00fc 0121
    add r8,r1                                @ 080d00fe 8844
LAB_080d0100:
    ldr r2, DAT_080d014c                     @ 080d0100 124a
    adds r0,r5,r2    @ 080d0102 a818
    .hword 0x4643    @ 080d0104 4346
    strb r3,[r0,#0x0]                        @ 080d0106 0370
LAB_080d0108:
    add sp,#0x8                              @ 080d0108 02b0
    pop {r3,r4,r5}                           @ 080d010a 38bc
    .hword 0x4698    @ 080d010c 9846
    .hword 0x46a1    @ 080d010e a146
    .hword 0x46aa    @ 080d0110 aa46
    pop {r4,r5,r6,r7}                        @ 080d0112 f0bc
    pop {r0}                                 @ 080d0114 01bc
    bx r0                                    @ 080d0116 0047
DAT_080d0118:
    .word  0x0201f440                     @ 080d0118 40f40102
DAT_080d011c:
    .word  0x00000a0c                     @ 080d011c 0c0a0000
DAT_080d0120:
    .word  0x00004020                     @ 080d0120 20400000
DAT_080d0124:
    .word  0x02006ed0                     @ 080d0124 d06e0002
DAT_080d0128:
    .word  0x02000000                     @ 080d0128 00000002
DAT_080d012c:
    .word  0x00006c2c                     @ 080d012c 2c6c0000
PTR_font_jp_base_table_080d0130:
    .word  font_jp_base_table             @ 080d0130 54f8e509
DAT_080d0134:
    .word  0x06014000                     @ 080d0134 00400106
DAT_080d0138:
    .word  0x02023130                     @ 080d0138 30310202
DAT_080d013c:
    .word  0x00000a04                     @ 080d013c 040a0000
DAT_080d0140:
    .word  0x00000a0d                     @ 080d0140 0d0a0000
DAT_080d0144:
    .word  0x00000a17                     @ 080d0144 170a0000
DAT_080d0148:
    .word  0x00000a18                     @ 080d0148 180a0000
DAT_080d014c:
    .word  0x00000a03                     @ 080d014c 030a0000

@ Card-list OAM row render branch for pack_column variant (scene_pack). Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 7. Reads gPrng[0x148] as frame count r6; reads gFontState[0x0a18] bits[23:16] as pack_col_count [0..2]; divisor = 2-pack_col_count [1..2]. First __divsi3: col_offset = r6 / (2-pack_col_count). Checks col_offset against threshold 3 (cmp r0,#3; bgt) for mod-8 check. Second __divsi3: computes second-dimension column coordinate. Outputs OAM row position via shared tail. No direct OAM write in body. No APCS inputs; r8 loaded internally from DAT. Constants: PACK_COL_OFFSET=0x0a18 bits[23:16] [0..2]; PRNG_FRAME_OFFSET=gPrng+0x148; DIVISOR_MAX=2; MOD_THRESHOLD=3.
render_card_list_oam_row_by_pack_column:
    push {r4,r5,r6,r7,lr}                    @ 080d0150 f0b5
    .hword 0x464f    @ 080d0152 4f46
    .hword 0x4646    @ 080d0154 4646
    push {r6,r7}                             @ 080d0156 c0b4
    movs r0,#0x80    @ 080d0158 8020
    lsls r0,r0,#0x1    @ 080d015a 4000
    .hword 0x4681    @ 080d015c 8146
    ldr r0, PTR_gPrng_080d01ac               @ 080d015e 1348
    movs r1,#0x83    @ 080d0160 8321
    lsls r1,r1,#0x2    @ 080d0162 8900
    adds r0,r0,r1    @ 080d0164 4018
    ldrh r6,[r0,#0x0]                        @ 080d0166 0688
    ldr r4, DAT_080d01b0                     @ 080d0168 114c
    ldr r1, DAT_080d01b4                     @ 080d016a 1249
    adds r0,r4,r1    @ 080d016c 6018
    ldr r0,[r0,#0x0]                         @ 080d016e 0068
    lsls r5,r0,#0xf    @ 080d0170 c503
    lsrs r1,r5,#0x18    @ 080d0172 290e
    movs r7,#0x2    @ 080d0174 0227
    subs r1,r7,r1    @ 080d0176 791a
    adds r0,r6,#0x0    @ 080d0178 301c
    bl __divsi3                              @ 080d017a 3ef043fa
    adds r1,r0,#0x0    @ 080d017e 011c
    .hword 0x46a0    @ 080d0180 a046
    cmp r1,#0x0                              @ 080d0182 0029
    bge LAB_080d0188                         @ 080d0184 00da
    adds r0,r1,#0x7    @ 080d0186 c81d
LAB_080d0188:
    asrs r0,r0,#0x3    @ 080d0188 c010
    lsls r0,r0,#0x3    @ 080d018a c000
    subs r0,r1,r0    @ 080d018c 081a
    cmp r0,#0x3                              @ 080d018e 0328
    ble LAB_080d01b8                         @ 080d0190 12dd
    lsrs r1,r5,#0x18    @ 080d0192 290e
    subs r1,r7,r1    @ 080d0194 791a
    adds r0,r6,#0x0    @ 080d0196 301c
    bl __divsi3                              @ 080d0198 3ef034fa
    adds r1,r0,#0x0    @ 080d019c 011c
    cmp r0,#0x0                              @ 080d019e 0028
    bge LAB_080d01a4                         @ 080d01a0 00da
    adds r1,r0,#0x7    @ 080d01a2 c11d
LAB_080d01a4:
    asrs r1,r1,#0x3    @ 080d01a4 c910
    lsls r1,r1,#0x3    @ 080d01a6 c900
    subs r1,r0,r1    @ 080d01a8 411a
    b LAB_080d01d4                           @ 080d01aa 13e0
PTR_gPrng_080d01ac:
    .word  gPrng                          @ 080d01ac 40000003
DAT_080d01b0:
    .word  0x0201f440                     @ 080d01b0 40f40102
DAT_080d01b4:
    .word  0x00000a18                     @ 080d01b4 180a0000
LAB_080d01b8:
    lsrs r1,r5,#0x18    @ 080d01b8 290e
    subs r1,r7,r1    @ 080d01ba 791a
    adds r0,r6,#0x0    @ 080d01bc 301c
    bl __divsi3                              @ 080d01be 3ef021fa
    adds r1,r0,#0x0    @ 080d01c2 011c
    cmp r1,#0x0                              @ 080d01c4 0029
    bge LAB_080d01ca                         @ 080d01c6 00da
    adds r0,r1,#0x7    @ 080d01c8 c81d
LAB_080d01ca:
    asrs r0,r0,#0x3    @ 080d01ca c010
    lsls r0,r0,#0x3    @ 080d01cc c000
    subs r0,r1,r0    @ 080d01ce 081a
    movs r1,#0x7    @ 080d01d0 0721
    subs r1,r1,r0    @ 080d01d2 091a
LAB_080d01d4:
    lsls r0,r1,#0x2    @ 080d01d4 8800
    adds r0,r0,r1    @ 080d01d6 4018
    lsls r0,r0,#0x1    @ 080d01d8 4000
    .hword 0x4649    @ 080d01da 4946
    subs r1,r1,r0    @ 080d01dc 091a
    .hword 0x4689    @ 080d01de 8946
    ldr r0, DAT_080d0234                     @ 080d01e0 1448
    add r0,r8                                @ 080d01e2 4044
    ldrh r0,[r0,#0x0]                        @ 080d01e4 0088
    cmp r0,#0x0                              @ 080d01e6 0028
    beq LAB_080d0240                         @ 080d01e8 2ad0
    ldr r6, DAT_080d0238                     @ 080d01ea 134e
    add r6,r8                                @ 080d01ec 4644
    ldrb r1,[r6,#0x0]                        @ 080d01ee 3178
    lsrs r0,r1,#0x1    @ 080d01f0 4808
    movs r4,#0xa    @ 080d01f2 0a24
    subs r0,r4,r0    @ 080d01f4 201a
    lsls r0,r0,#0x3    @ 080d01f6 c000
    ldr r5, DAT_080d023c                     @ 080d01f8 104d
    add r5,r8                                @ 080d01fa 4544
    ldrh r1,[r5,#0x0]                        @ 080d01fc 2988
    adds r0,r1,r0    @ 080d01fe 0818
    lsls r0,r0,#0x10    @ 080d0200 0004
    movs r1,#0x4a    @ 080d0202 4a21
    orrs r0,r1    @ 080d0204 0843
    movs r2,#0xc6    @ 080d0206 c622
    lsls r2,r2,#0x1    @ 080d0208 5200
    movs r1,#0x80    @ 080d020a 8021
    bl write_oam_entry_with_tile_inc         @ 080d020c 26f020f9
    ldrb r6,[r6,#0x0]                        @ 080d0210 3678
    lsrs r0,r6,#0x1    @ 080d0212 7008
    subs r4,r4,r0    @ 080d0214 241a
    lsls r4,r4,#0x3    @ 080d0216 e400
    ldrh r5,[r5,#0x0]                        @ 080d0218 2d88
    adds r4,r5,r4    @ 080d021a 2c19
    lsls r4,r4,#0x10    @ 080d021c 2404
    movs r0,#0xae    @ 080d021e ae20
    orrs r4,r0    @ 080d0220 0443
    movs r2,#0xe6    @ 080d0222 e622
    lsls r2,r2,#0x1    @ 080d0224 5200
    .hword 0x4648    @ 080d0226 4846
    lsls r3,r0,#0x10    @ 080d0228 0304
    adds r0,r4,#0x0    @ 080d022a 201c
    movs r1,#0x80    @ 080d022c 8021
    bl write_pack_obj_attr_by_dir_stacked    @ 080d022e 26f04dfd
    b LAB_080d0288                           @ 080d0232 29e0
DAT_080d0234:
    .word  0x00000a14                     @ 080d0234 140a0000
DAT_080d0238:
    .word  0x00000a03                     @ 080d0238 030a0000
DAT_080d023c:
    .word  0x00000a04                     @ 080d023c 040a0000
LAB_080d0240:
    ldr r6, DAT_080d0294                     @ 080d0240 144e
    add r6,r8                                @ 080d0242 4644
    ldrb r1,[r6,#0x0]                        @ 080d0244 3178
    lsrs r0,r1,#0x1    @ 080d0246 4808
    movs r4,#0xa    @ 080d0248 0a24
    subs r0,r4,r0    @ 080d024a 201a
    lsls r0,r0,#0x3    @ 080d024c c000
    ldr r5, DAT_080d0298                     @ 080d024e 124d
    add r5,r8                                @ 080d0250 4544
    ldrh r1,[r5,#0x0]                        @ 080d0252 2988
    adds r0,r1,r0    @ 080d0254 0818
    lsls r0,r0,#0x10    @ 080d0256 0004
    movs r1,#0x4a    @ 080d0258 4a21
    orrs r0,r1    @ 080d025a 0843
    movs r2,#0xc6    @ 080d025c c622
    lsls r2,r2,#0x1    @ 080d025e 5200
    .hword 0x4649    @ 080d0260 4946
    lsls r3,r1,#0x10    @ 080d0262 0b04
    movs r1,#0x80    @ 080d0264 8021
    bl write_pack_obj_attr_by_dir_stacked    @ 080d0266 26f031fd
    ldrb r6,[r6,#0x0]                        @ 080d026a 3678
    lsrs r0,r6,#0x1    @ 080d026c 7008
    subs r4,r4,r0    @ 080d026e 241a
    lsls r4,r4,#0x3    @ 080d0270 e400
    ldrh r5,[r5,#0x0]                        @ 080d0272 2d88
    adds r4,r5,r4    @ 080d0274 2c19
    lsls r4,r4,#0x10    @ 080d0276 2404
    movs r0,#0xae    @ 080d0278 ae20
    orrs r4,r0    @ 080d027a 0443
    movs r2,#0xe6    @ 080d027c e622
    lsls r2,r2,#0x1    @ 080d027e 5200
    adds r0,r4,#0x0    @ 080d0280 201c
    movs r1,#0x80    @ 080d0282 8021
    bl write_oam_entry_with_tile_inc         @ 080d0284 26f0e4f8
LAB_080d0288:
    pop {r3,r4}                              @ 080d0288 18bc
    .hword 0x4698    @ 080d028a 9846
    .hword 0x46a1    @ 080d028c a146
    pop {r4,r5,r6,r7}                        @ 080d028e f0bc
    pop {r0}                                 @ 080d0290 01bc
    bx r0                                    @ 080d0292 0047
DAT_080d0294:
    .word  0x00000a03                     @ 080d0294 030a0000
DAT_080d0298:
    .word  0x00000a04                     @ 080d0298 040a0000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Nearly identical structure to render_card_list_oam_row_by_lp_counter (0x080cd138). Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. state=0: reads gPrng+0x148 with mask 0x30 (bit4/5, vs 0xc0 in 080cd138); nonzero: decrements gFontState+0x0a14 halfword by 1, calls sync_state_and_init_sprite(0). state=1: reads LP from gP1LifePoints+0x3d40, writes gFontState+0x0a14 halfword (1-LP_val), sets state word bit9, calls sync_state_and_init_sprite(0x24) or (2). state>=2: nibble loop on 0x0a1b/0x0a1c; returns 1 if >0x1f else 0. Key difference from 080cd138: gPrng+0x148 check mask=0x30 (bit4/5) not 0xc0. Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; STATE_OFFSET=0x0a18; LP_OFFSET=0x0a14; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; LP_MASK=0x30.
render_card_list_oam_row_by_lp_init:
    push {r4,r5,r6,r7,lr}                    @ 080d029c f0b5
    .hword 0x4647    @ 080d029e 4746
    push {r7}                                @ 080d02a0 80b4
    ldr r4, DAT_080d02d0                     @ 080d02a2 0b4c
    ldr r1, DAT_080d02d4                     @ 080d02a4 0b49
    adds r0,r4,r1    @ 080d02a6 6018
    ldrb r3,[r0,#0x0]                        @ 080d02a8 0378
    lsrs r0,r3,#0x1    @ 080d02aa 5808
    movs r1,#0xa    @ 080d02ac 0a21
    subs r1,r1,r0    @ 080d02ae 091a
    lsls r1,r1,#0x3    @ 080d02b0 c900
    movs r2,#0xfe    @ 080d02b2 fe22
    lsls r2,r2,#0x1    @ 080d02b4 5200
    movs r0,#0x30    @ 080d02b6 3020
    bl write_card_list_oam_row_strip         @ 080d02b8 f7f73af9
    ldr r2, DAT_080d02d8                     @ 080d02bc 064a
    adds r3,r4,r2    @ 080d02be a318
    ldr r2,[r3,#0x0]                         @ 080d02c0 1a68
    lsls r0,r2,#0xf    @ 080d02c2 d003
    lsrs r7,r0,#0x18    @ 080d02c4 070e
    cmp r7,#0x0                              @ 080d02c6 002f
    beq LAB_080d02dc                         @ 080d02c8 08d0
    cmp r7,#0x1                              @ 080d02ca 012f
    beq LAB_080d0354                         @ 080d02cc 42d0
    b LAB_080d03a4                           @ 080d02ce 69e0
DAT_080d02d0:
    .word  0x0201f440                     @ 080d02d0 40f40102
DAT_080d02d4:
    .word  0x00000a03                     @ 080d02d4 030a0000
DAT_080d02d8:
    .word  0x00000a18                     @ 080d02d8 180a0000
LAB_080d02dc:
    ldr r0, PTR_gPrng_080d0304               @ 080d02dc 0948
    movs r5,#0xa4    @ 080d02de a425
    lsls r5,r5,#0x1    @ 080d02e0 6d00
    adds r0,r0,r5    @ 080d02e2 4019
    ldrh r1,[r0,#0x0]                        @ 080d02e4 0188
    movs r0,#0x30    @ 080d02e6 3020
    ands r0,r1    @ 080d02e8 0840
    cmp r0,#0x0                              @ 080d02ea 0028
    beq LAB_080d030c                         @ 080d02ec 0ed0
    ldr r0, DAT_080d0308                     @ 080d02ee 0648
    adds r1,r4,r0    @ 080d02f0 2118
    movs r0,#0x1    @ 080d02f2 0120
    ldrh r2,[r1,#0x0]                        @ 080d02f4 0a88
    subs r0,r0,r2    @ 080d02f6 801a
    strh r0,[r1,#0x0]                        @ 080d02f8 0880
    movs r0,#0x0    @ 080d02fa 0020
    bl sync_state_and_init_sprite            @ 080d02fc 29f0dafb
    b LAB_080d03a4                           @ 080d0300 50e0
    .zero  0x2
PTR_gPrng_080d0304:
    .word  gPrng                          @ 080d0304 40000003
DAT_080d0308:
    .word  0x00000a14                     @ 080d0308 140a0000
LAB_080d030c:
    movs r0,#0x1    @ 080d030c 0120
    ands r0,r1    @ 080d030e 0840
    cmp r0,#0x0                              @ 080d0310 0028
    beq LAB_080d0344                         @ 080d0312 17d0
    ldr r0, PTR_gP1LifePoints_080d0338       @ 080d0314 0848
    movs r5,#0xea    @ 080d0316 ea25
    lsls r5,r5,#0x5    @ 080d0318 6d01
    adds r0,r0,r5    @ 080d031a 4019
    ldr r5, DAT_080d033c                     @ 080d031c 074d
    adds r1,r4,r5    @ 080d031e 6119
    ldrh r1,[r1,#0x0]                        @ 080d0320 0988
    str r1,[r0,#0x0]                         @ 080d0322 0160
    ldr r0, DAT_080d0340                     @ 080d0324 0648
    ands r0,r2    @ 080d0326 1040
    movs r1,#0x80    @ 080d0328 8021
    lsls r1,r1,#0x2    @ 080d032a 8900
    orrs r0,r1    @ 080d032c 0843
    str r0,[r3,#0x0]                         @ 080d032e 1860
    movs r0,#0x24    @ 080d0330 2420
    bl sync_state_and_init_sprite            @ 080d0332 29f0bffb
    b LAB_080d03a4                           @ 080d0336 35e0
PTR_gP1LifePoints_080d0338:
    .word  gP1LifePoints                  @ 080d0338 e0c40102
DAT_080d033c:
    .word  0x00000a14                     @ 080d033c 140a0000
DAT_080d0340:
    .word  0xfffe01ff                     @ 080d0340 ff01feff
LAB_080d0344:
    movs r0,#0x2    @ 080d0344 0220
    ands r0,r1    @ 080d0346 0840
    cmp r0,#0x0                              @ 080d0348 0028
    beq LAB_080d03a4                         @ 080d034a 2bd0
    movs r0,#0x2    @ 080d034c 0220
    bl sync_state_and_init_sprite            @ 080d034e 29f0b1fb
    b LAB_080d03a4                           @ 080d0352 27e0
LAB_080d0354:
    ldr r0, DAT_080d039c                     @ 080d0354 1148
    adds r0,r0,r4    @ 080d0356 0019
    .hword 0x4680    @ 080d0358 8046
    ldrb r6,[r0,#0x0]                        @ 080d035a 0678
    lsrs r0,r6,#0x1    @ 080d035c 7008
    ldr r1, DAT_080d03a0                     @ 080d035e 1049
    adds r4,r4,r1    @ 080d0360 6418
    adds r3,r7,#0x0    @ 080d0362 3b1c
    ldrb r2,[r4,#0x0]                        @ 080d0364 2278
    ands r3,r2    @ 080d0366 1340
    lsls r3,r3,#0x7    @ 080d0368 db01
    orrs r3,r0    @ 080d036a 0343
    adds r2,r3,#0x1    @ 080d036c 5a1c
    movs r1,#0x7f    @ 080d036e 7f21
    ands r1,r2    @ 080d0370 1140
    lsls r1,r1,#0x1    @ 080d0372 4900
    movs r5,#0x1    @ 080d0374 0125
    adds r0,r7,#0x0    @ 080d0376 381c
    ands r0,r6    @ 080d0378 3040
    orrs r0,r1    @ 080d037a 0843
    .hword 0x4641    @ 080d037c 4146
    strb r0,[r1,#0x0]                        @ 080d037e 0870
    lsrs r2,r2,#0x7    @ 080d0380 d209
    ands r2,r7    @ 080d0382 3a40
    ands r2,r5    @ 080d0384 2a40
    movs r0,#0x2    @ 080d0386 0220
    rsbs r0,r0,#0    @ 080d0388 4042
    ldrb r5,[r4,#0x0]                        @ 080d038a 2578
    ands r0,r5    @ 080d038c 2840
    orrs r0,r2    @ 080d038e 1043
    strb r0,[r4,#0x0]                        @ 080d0390 2070
    cmp r3,#0x1f                             @ 080d0392 1f2b
    bls LAB_080d03a4                         @ 080d0394 06d9
    movs r0,#0x1    @ 080d0396 0120
    b LAB_080d03a6                           @ 080d0398 05e0
    .zero  0x2
DAT_080d039c:
    .word  0x00000a1b                     @ 080d039c 1b0a0000
DAT_080d03a0:
    .word  0x00000a1c                     @ 080d03a0 1c0a0000
LAB_080d03a4:
    movs r0,#0x0    @ 080d03a4 0020
LAB_080d03a6:
    pop {r3}                                 @ 080d03a6 08bc
    .hword 0x4698    @ 080d03a8 9846
    pop {r4,r5,r6,r7}                        @ 080d03aa f0bc
    pop {r1}                                 @ 080d03ac 02bc
    bx r1                                    @ 080d03ae 0847

@ Initialize BG tile VRAM for choice label display variant case 1 (first option). Writes tile map entries for the first choice label position in the card choice UI. No APCS params; reads choice_display_state from globals. Returns void. Side effects: BG map VRAM written for choice label case 1. Sibling: init_choice_label_vram_case8.
init_choice_label_vram_case1:
    push {lr}                                @ 080d03b0 00b5
    ldr r0, DAT_080d0410                     @ 080d03b2 1748
    movs r1,#0x80    @ 080d03b4 8021
    lsls r1,r1,#0x7    @ 080d03b6 c901
    bl zero_fill_by_halfword                 @ 080d03b8 24f05cfd
    ldr r0, DAT_080d0414                     @ 080d03bc 1548
    ldr r1, DAT_080d0418                     @ 080d03be 1649
    movs r2,#0x1    @ 080d03c0 0122
    movs r3,#0x1    @ 080d03c2 0123
    bl tile_2d_row_copy                      @ 080d03c4 27f086f8
    ldr r3, DAT_080d041c                     @ 080d03c8 144b
    ldr r1, DAT_080d0420                     @ 080d03ca 1549
    adds r0,r3,r1    @ 080d03cc 5818
    ldrb r0,[r0,#0x0]                        @ 080d03ce 0078
    lsrs r2,r0,#0x1    @ 080d03d0 4208
    ldr r0, DAT_080d0424                     @ 080d03d2 1448
    adds r1,r3,r0    @ 080d03d4 1918
    movs r0,#0x1    @ 080d03d6 0120
    ldrb r1,[r1,#0x0]                        @ 080d03d8 0978
    ands r0,r1    @ 080d03da 0840
    lsls r0,r0,#0x7    @ 080d03dc c001
    orrs r0,r2    @ 080d03de 1043
    cmp r0,#0x0                              @ 080d03e0 0028
    bne LAB_080d04c0                         @ 080d03e2 6dd1
    ldr r1, DAT_080d0428                     @ 080d03e4 1049
    adds r3,r3,r1    @ 080d03e6 5b18
    ldr r0, DAT_080d042c                     @ 080d03e8 1048
    ldr r1, DAT_080d0430                     @ 080d03ea 1149
    adds r0,r0,r1    @ 080d03ec 4018
    movs r2,#0x7    @ 080d03ee 0722
    ldrb r0,[r0,#0x0]                        @ 080d03f0 0078
    ands r2,r0    @ 080d03f2 0240
    cmp r2,#0x1                              @ 080d03f4 012a
    beq LAB_080d0454                         @ 080d03f6 2dd0
    cmp r2,#0x2                              @ 080d03f8 022a
    beq LAB_080d044c                         @ 080d03fa 27d0
    cmp r2,#0x3                              @ 080d03fc 032a
    beq LAB_080d0444                         @ 080d03fe 21d0
    cmp r2,#0x4                              @ 080d0400 042a
    beq LAB_080d043c                         @ 080d0402 1bd0
    ldr r1, DAT_080d0434                     @ 080d0404 0b49
    cmp r2,#0x5                              @ 080d0406 052a
    bne LAB_080d0456                         @ 080d0408 25d1
    ldr r0, DAT_080d0438                     @ 080d040a 0b48
    adds r1,r1,r0    @ 080d040c 0918
    b LAB_080d0456                           @ 080d040e 22e0
DAT_080d0410:
    .word  0x06014000                     @ 080d0410 00400106
DAT_080d0414:
    .word  0x06010c00                     @ 080d0414 000c0106
DAT_080d0418:
    .word  0x0988ab18                     @ 080d0418 18ab8809
DAT_080d041c:
    .word  0x0201f440                     @ 080d041c 40f40102
DAT_080d0420:
    .word  0x00000a17                     @ 080d0420 170a0000
DAT_080d0424:
    .word  0x00000a18                     @ 080d0424 180a0000
DAT_080d0428:
    .word  0x00000201                     @ 080d0428 01020000
DAT_080d042c:
    .word  0x02000000                     @ 080d042c 00000002
DAT_080d0430:
    .word  0x00006c2c                     @ 080d0430 2c6c0000
DAT_080d0434:
    .word  0x09dbfce6                     @ 080d0434 e6fcdb09
DAT_080d0438:
    .word  0x0003ab0e                     @ 080d0438 0eab0300
LAB_080d043c:
    ldr r1, DAT_080d0440                     @ 080d043c 0049
    b LAB_080d0456                           @ 080d043e 0ae0
DAT_080d0440:
    .word  0x09deec0a                     @ 080d0440 0aecde09
LAB_080d0444:
    ldr r1, DAT_080d0448                     @ 080d0444 0049
    b LAB_080d0456                           @ 080d0446 06e0
DAT_080d0448:
    .word  0x09de276e                     @ 080d0448 6e27de09
LAB_080d044c:
    ldr r1, DAT_080d0450                     @ 080d044c 0049
    b LAB_080d0456                           @ 080d044e 02e0
DAT_080d0450:
    .word  0x09dd63ee                     @ 080d0450 ee63dd09
LAB_080d0454:
    ldr r1, DAT_080d0488                     @ 080d0454 0c49
LAB_080d0456:
    adds r0,r3,#0x0    @ 080d0456 181c
    bl copy_cstr_to_buf                      @ 080d0458 24f0fcfd
    ldr r3, DAT_080d048c                     @ 080d045c 0b4b
    ldr r0, DAT_080d0490                     @ 080d045e 0c48
    ldr r1, DAT_080d0494                     @ 080d0460 0c49
    adds r0,r0,r1    @ 080d0462 4018
    movs r2,#0x7    @ 080d0464 0722
    ldrb r0,[r0,#0x0]                        @ 080d0466 0078
    ands r2,r0    @ 080d0468 0240
    cmp r2,#0x1                              @ 080d046a 012a
    beq LAB_080d04b8                         @ 080d046c 24d0
    cmp r2,#0x2                              @ 080d046e 022a
    beq LAB_080d04b0                         @ 080d0470 1ed0
    cmp r2,#0x3                              @ 080d0472 032a
    beq LAB_080d04a8                         @ 080d0474 18d0
    cmp r2,#0x4                              @ 080d0476 042a
    beq LAB_080d04a0                         @ 080d0478 12d0
    ldr r1, DAT_080d0498                     @ 080d047a 0749
    cmp r2,#0x5                              @ 080d047c 052a
    bne LAB_080d04ba                         @ 080d047e 1cd1
    ldr r0, DAT_080d049c                     @ 080d0480 0648
    adds r1,r1,r0    @ 080d0482 0918
    b LAB_080d04ba                           @ 080d0484 19e0
    .zero  0x2
DAT_080d0488:
    .word  0x09dcab1e                     @ 080d0488 1eabdc09
DAT_080d048c:
    .word  0x0201f841                     @ 080d048c 41f80102
DAT_080d0490:
    .word  0x02000000                     @ 080d0490 00000002
DAT_080d0494:
    .word  0x00006c2c                     @ 080d0494 2c6c0000
DAT_080d0498:
    .word  0x09dbfcec                     @ 080d0498 ecfcdb09
DAT_080d049c:
    .word  0x0003ab0c                     @ 080d049c 0cab0300
LAB_080d04a0:
    ldr r1, DAT_080d04a4                     @ 080d04a0 0049
    b LAB_080d04ba                           @ 080d04a2 0ae0
DAT_080d04a4:
    .word  0x09deec0e                     @ 080d04a4 0eecde09
LAB_080d04a8:
    ldr r1, DAT_080d04ac                     @ 080d04a8 0049
    b LAB_080d04ba                           @ 080d04aa 06e0
DAT_080d04ac:
    .word  0x09de2772                     @ 080d04ac 7227de09
LAB_080d04b0:
    ldr r1, DAT_080d04b4                     @ 080d04b0 0049
    b LAB_080d04ba                           @ 080d04b2 02e0
DAT_080d04b4:
    .word  0x09dd63f2                     @ 080d04b4 f263dd09
LAB_080d04b8:
    ldr r1, DAT_080d04d0                     @ 080d04b8 0549
LAB_080d04ba:
    adds r0,r3,#0x0    @ 080d04ba 181c
    bl copy_cstr_to_buf                      @ 080d04bc 24f0cafd
LAB_080d04c0:
    ldr r0, DAT_080d04d4                     @ 080d04c0 0448
    ldr r1, DAT_080d04d8                     @ 080d04c2 0549
    adds r0,r0,r1    @ 080d04c4 4018
    movs r1,#0x1    @ 080d04c6 0121
    strb r1,[r0,#0x0]                        @ 080d04c8 0170
    pop {r0}                                 @ 080d04ca 01bc
    bx r0                                    @ 080d04cc 0047
    .zero  0x2
DAT_080d04d0:
    .word  0x09dcab22                     @ 080d04d0 22abdc09
DAT_080d04d4:
    .word  0x0201f440                     @ 080d04d4 40f40102
DAT_080d04d8:
    .word  0x00000a01                     @ 080d04d8 010a0000

@ 由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). 与 080ccfe4 结构完全对称: 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); 设置语言模式标志 (STATE+0x8 bit[1..2]); 从 font_jp_base_table 取字体基址; 以 STATE_DATA (0x0201f441) 为源, 调用 render_jp_string_to_tile_line 两次 (循环 r6 in [0..1]), 每次偏移 0x200 字节 (0x80*4); 完成后 write_line_buf_to_bg_tile_vram 刷新到 BG tile VRAM (0x06014000). 函数使用 r8/r9 callee-save high-register 别名, 由 .hword 0x4657/464e/4645/4682 搬移. Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, VRAM_BG=0x06014000, FONT_SIZE=0x200, LOOP_RANGE=[0..1].
render_jp_two_line_text_to_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 080d04dc f0b5
    .hword 0x4657    @ 080d04de 5746
    .hword 0x464e    @ 080d04e0 4e46
    .hword 0x4645    @ 080d04e2 4546
    push {r5,r6,r7}                          @ 080d04e4 e0b4
    sub sp,#0x4                              @ 080d04e6 81b0
    movs r0,#0x2    @ 080d04e8 0220
    .hword 0x4682    @ 080d04ea 8246
    movs r6,#0x0    @ 080d04ec 0026
    movs r0,#0x17    @ 080d04ee 1720
    movs r1,#0x10    @ 080d04f0 1021
    movs r2,#0x1    @ 080d04f2 0122
    movs r3,#0x2    @ 080d04f4 0223
    bl setup_line_buf_with_font_and_align    @ 080d04f6 20f0e3fb
    ldr r2, DAT_080d05c8                     @ 080d04fa 334a
    ldr r0, DAT_080d05cc                     @ 080d04fc 3348
    ldr r1, DAT_080d05d0                     @ 080d04fe 3449
    adds r0,r0,r1    @ 080d0500 4018
    movs r1,#0x7    @ 080d0502 0721
    ldrb r0,[r0,#0x0]                        @ 080d0504 0078
    ands r1,r0    @ 080d0506 0140
    rsbs r1,r1,#0    @ 080d0508 4942
    lsrs r1,r1,#0x1f    @ 080d050a c90f
    movs r0,#0x2    @ 080d050c 0220
    rsbs r0,r0,#0    @ 080d050e 4042
    ldrb r3,[r2,#0x8]                        @ 080d0510 137a
    ands r0,r3    @ 080d0512 1840
    orrs r0,r1    @ 080d0514 0843
    movs r1,#0x2    @ 080d0516 0221
    orrs r0,r1    @ 080d0518 0843
    strb r0,[r2,#0x8]                        @ 080d051a 1072
    ldr r3, PTR_font_jp_base_table_080d05d4  @ 080d051c 2d4b
    lsls r1,r0,#0x1e    @ 080d051e 8107
    lsrs r1,r1,#0x1f    @ 080d0520 c90f
    lsls r1,r1,#0x2    @ 080d0522 8900
    lsls r0,r0,#0x1f    @ 080d0524 c007
    lsrs r0,r0,#0x1f    @ 080d0526 c00f
    lsls r0,r0,#0x3    @ 080d0528 c000
    adds r1,r1,r0    @ 080d052a 0918
    adds r1,r1,r3    @ 080d052c c918
    ldr r0,[r1,#0x0]                         @ 080d052e 0868
    str r0,[r2,#0x4]                         @ 080d0530 5060
    movs r0,#0x40    @ 080d0532 4020
    ldrb r1,[r2,#0x15]                       @ 080d0534 517d
    orrs r0,r1    @ 080d0536 0843
    strb r0,[r2,#0x15]                       @ 080d0538 5075
    ldr r4, DAT_080d05d8                     @ 080d053a 274c
    str r6,[sp,#0x0]                         @ 080d053c 0096
    movs r0,#0x2    @ 080d053e 0220
    movs r1,#0x2    @ 080d0540 0221
    adds r2,r4,#0x0    @ 080d0542 221c
    movs r3,#0xc    @ 080d0544 0c23
    bl render_jp_string_to_tile_line         @ 080d0546 f7f7bbf8
    adds r5,r0,#0x0    @ 080d054a 051c
    subs r2,r4,#0x1    @ 080d054c 621e
    .hword 0x4691    @ 080d054e 9146
    .hword 0x46b0    @ 080d0550 b046
    movs r3,#0x80    @ 080d0552 8023
    lsls r3,r3,#0x2    @ 080d0554 9b00
    adds r4,r4,r3    @ 080d0556 e418
LAB_080d0558:
    lsls r0,r6,#0x1    @ 080d0558 7000
    ldr r7, DAT_080d05dc                     @ 080d055a 204f
    add r7,r9                                @ 080d055c 4f44
    adds r0,r0,r7    @ 080d055e c019
    strh r5,[r0,#0x0]                        @ 080d0560 0580
    .hword 0x4640    @ 080d0562 4046
    str r0,[sp,#0x0]                         @ 080d0564 0090
    .hword 0x4650    @ 080d0566 5046
    adds r0,#0xc    @ 080d0568 0c30
    adds r1,r5,#0x0    @ 080d056a 291c
    adds r2,r4,#0x0    @ 080d056c 221c
    movs r3,#0xc    @ 080d056e 0c23
    bl render_jp_string_to_tile_line         @ 080d0570 f7f7a6f8
    adds r5,r0,#0x0    @ 080d0574 051c
    movs r1,#0x80    @ 080d0576 8021
    lsls r1,r1,#0x2    @ 080d0578 8900
    adds r4,r4,r1    @ 080d057a 6418
    adds r6,#0x1    @ 080d057c 0136
    cmp r6,#0x1                              @ 080d057e 012e
    ble LAB_080d0558                         @ 080d0580 eadd
    subs r5,#0x2    @ 080d0582 023d
    ldr r0, DAT_080d05e0                     @ 080d0584 1648
    movs r1,#0x0    @ 080d0586 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d0588 23f024f9
    ldrb r2,[r7,#0x13]                       @ 080d058c fa7c
    lsrs r1,r2,#0x1    @ 080d058e 5108
    movs r0,#0x1    @ 080d0590 0120
    ldrb r3,[r7,#0x14]                       @ 080d0592 3b7d
    ands r0,r3    @ 080d0594 1840
    lsls r0,r0,#0x7    @ 080d0596 c001
    orrs r0,r1    @ 080d0598 0843
    cmp r0,#0x0                              @ 080d059a 0028
    bne LAB_080d05b8                         @ 080d059c 0cd1
    adds r5,#0x10    @ 080d059e 1035
    adds r0,r5,#0x0    @ 080d05a0 281c
    cmp r5,#0x0                              @ 080d05a2 002d
    bge LAB_080d05a8                         @ 080d05a4 00da
    adds r0,r5,#0x7    @ 080d05a6 e81d
LAB_080d05a8:
    asrs r6,r0,#0x3    @ 080d05a8 c610
    movs r0,#0x7    @ 080d05aa 0720
    ands r0,r5    @ 080d05ac 2840
    cmp r0,#0x0                              @ 080d05ae 0028
    beq LAB_080d05b4                         @ 080d05b0 00d0
    adds r6,#0x1    @ 080d05b2 0136
LAB_080d05b4:
    subs r0,r7,#0x1    @ 080d05b4 781e
    strb r6,[r0,#0x0]                        @ 080d05b6 0670
LAB_080d05b8:
    add sp,#0x4                              @ 080d05b8 01b0
    pop {r3,r4,r5}                           @ 080d05ba 38bc
    .hword 0x4698    @ 080d05bc 9846
    .hword 0x46a1    @ 080d05be a146
    .hword 0x46aa    @ 080d05c0 aa46
    pop {r4,r5,r6,r7}                        @ 080d05c2 f0bc
    pop {r0}                                 @ 080d05c4 01bc
    bx r0                                    @ 080d05c6 0047
DAT_080d05c8:
    .word  0x02006ed0                     @ 080d05c8 d06e0002
DAT_080d05cc:
    .word  0x02000000                     @ 080d05cc 00000002
DAT_080d05d0:
    .word  0x00006c2c                     @ 080d05d0 2c6c0000
PTR_font_jp_base_table_080d05d4:
    .word  font_jp_base_table             @ 080d05d4 54f8e509
DAT_080d05d8:
    .word  0x0201f441                     @ 080d05d8 41f40102
DAT_080d05dc:
    .word  0x00000a04                     @ 080d05dc 040a0000
DAT_080d05e0:
    .word  0x06014000                     @ 080d05e0 00400106

@ Card-list OAM row render branch for pack_slot variant. Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 1. Reads gFontState[0x0a03] JP row count; OAM Y = (10-row/2)*8. Reads gFontState[0x0a1b] bits[1:0] pack_slot state [0..1]; if >1 skips write. For state 0..1: reads gFontState[0x0a0e] halfword*2 as x_base, subtracts 0x17, adds gFontState[0x0a04] halfword for Y. Calls write_oam_entry_from_packed_args (slot=0x60, attr0=0x34). No APCS inputs. Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; SLOT_STATE_OFFSET=0x0a1b [0..1]; X_BASE_OFFSET=0x0a0e; Y_ADJ_OFFSET=0x0a04; ATTR0=0x34; OAM_SLOT=0x60.
render_card_list_oam_row_by_pack_slot:
    push {r4,r5,lr}                          @ 080d05e4 30b5
    ldr r3, DAT_080d0630                     @ 080d05e6 124b
    ldr r1, DAT_080d0634                     @ 080d05e8 1249
    adds r0,r3,r1    @ 080d05ea 5818
    ldrb r0,[r0,#0x0]                        @ 080d05ec 0078
    lsrs r1,r0,#0x1    @ 080d05ee 4108
    movs r0,#0xa    @ 080d05f0 0a20
    subs r0,r0,r1    @ 080d05f2 401a
    lsls r4,r0,#0x3    @ 080d05f4 c400
    ldr r5, DAT_080d0638                     @ 080d05f6 104d
    adds r0,r3,r5    @ 080d05f8 5819
    ldrb r0,[r0,#0x0]                        @ 080d05fa 0078
    lsrs r0,r0,#0x1    @ 080d05fc 4008
    movs r1,#0x3    @ 080d05fe 0321
    ands r0,r1    @ 080d0600 0840
    cmp r0,#0x1                              @ 080d0602 0128
    bhi LAB_080d0628                         @ 080d0604 10d8
    movs r2,#0x34    @ 080d0606 3422
    ldr r1, DAT_080d063c                     @ 080d0608 0c49
    adds r0,r3,r1    @ 080d060a 5818
    ldrh r0,[r0,#0x0]                        @ 080d060c 0088
    lsls r0,r0,#0x1    @ 080d060e 4000
    subs r5,#0x17    @ 080d0610 173d
    adds r1,r3,r5    @ 080d0612 5919
    adds r0,r0,r1    @ 080d0614 4018
    ldrh r0,[r0,#0x0]                        @ 080d0616 0088
    adds r0,r0,r4    @ 080d0618 0019
    adds r0,#0x1    @ 080d061a 0130
    lsls r0,r0,#0x10    @ 080d061c 0004
    orrs r0,r2    @ 080d061e 1043
    movs r1,#0x0    @ 080d0620 0021
    movs r2,#0x60    @ 080d0622 6022
    bl write_oam_entry_from_packed_args      @ 080d0624 25f0a2fd
LAB_080d0628:
    pop {r4,r5}                              @ 080d0628 30bc
    pop {r0}                                 @ 080d062a 01bc
    bx r0                                    @ 080d062c 0047
    .zero  0x2
DAT_080d0630:
    .word  0x0201f440                     @ 080d0630 40f40102
DAT_080d0634:
    .word  0x00000a03                     @ 080d0634 030a0000
DAT_080d0638:
    .word  0x00000a1b                     @ 080d0638 1b0a0000
DAT_080d063c:
    .word  0x00000a14                     @ 080d063c 140a0000

@ indeg=1, caller: FUN_080c82e4 (card display master tick). Same skeleton as render_card_list_oam_row_by_lp_init (0x080d029c): computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip; reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. state=0: reads gPrng+0x148 bits[7:6] (mask 0xc0). state=1: LP counter update (gP1LifePoints+0x3d40). state>=2: reads nibble pair from gFontState+0x0a1b (nibble_A, byte) and +0x0a1c (nibble_B, byte), increments nibble_A; if nibble_A>0x1f returns 1 else 0. Key difference from 080cd138: after nibble_A increment, applies OR bit1 to nibble_B (flag nibble B logic). Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; STATE_OFFSET=0x0a18; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; LP_MASK=0xc0.
render_card_list_oam_row_by_slot_nibble:
    push {r4,r5,r6,r7,lr}                    @ 080d0640 f0b5
    .hword 0x4647    @ 080d0642 4746
    push {r7}                                @ 080d0644 80b4
    ldr r4, DAT_080d0674                     @ 080d0646 0b4c
    ldr r1, DAT_080d0678                     @ 080d0648 0b49
    adds r0,r4,r1    @ 080d064a 6018
    ldrb r3,[r0,#0x0]                        @ 080d064c 0378
    lsrs r0,r3,#0x1    @ 080d064e 5808
    movs r1,#0xa    @ 080d0650 0a21
    subs r1,r1,r0    @ 080d0652 091a
    lsls r1,r1,#0x3    @ 080d0654 c900
    movs r2,#0xfe    @ 080d0656 fe22
    lsls r2,r2,#0x1    @ 080d0658 5200
    movs r0,#0x30    @ 080d065a 3020
    bl write_card_list_oam_row_strip         @ 080d065c f6f768ff
    ldr r2, DAT_080d067c                     @ 080d0660 064a
    adds r5,r4,r2    @ 080d0662 a518
    ldr r2,[r5,#0x0]                         @ 080d0664 2a68
    lsls r0,r2,#0xf    @ 080d0666 d003
    lsrs r7,r0,#0x18    @ 080d0668 070e
    cmp r7,#0x0                              @ 080d066a 002f
    beq LAB_080d0680                         @ 080d066c 08d0
    cmp r7,#0x1                              @ 080d066e 012f
    beq LAB_080d0728                         @ 080d0670 5ad0
    b LAB_080d0778                           @ 080d0672 81e0
DAT_080d0674:
    .word  0x0201f440                     @ 080d0674 40f40102
DAT_080d0678:
    .word  0x00000a03                     @ 080d0678 030a0000
DAT_080d067c:
    .word  0x00000a18                     @ 080d067c 180a0000
LAB_080d0680:
    ldr r0, PTR_gPrng_080d06a8               @ 080d0680 0948
    movs r6,#0xa4    @ 080d0682 a426
    lsls r6,r6,#0x1    @ 080d0684 7600
    adds r0,r0,r6    @ 080d0686 8019
    ldrh r1,[r0,#0x0]                        @ 080d0688 0188
    movs r0,#0xc0    @ 080d068a c020
    ands r0,r1    @ 080d068c 0840
    cmp r0,#0x0                              @ 080d068e 0028
    beq LAB_080d06b0                         @ 080d0690 0ed0
    ldr r0, DAT_080d06ac                     @ 080d0692 0648
    adds r1,r4,r0    @ 080d0694 2118
    movs r0,#0x1    @ 080d0696 0120
    ldrh r2,[r1,#0x0]                        @ 080d0698 0a88
    subs r0,r0,r2    @ 080d069a 801a
    strh r0,[r1,#0x0]                        @ 080d069c 0880
    movs r0,#0x0    @ 080d069e 0020
    bl sync_state_and_init_sprite            @ 080d06a0 29f008fa
    b LAB_080d0778                           @ 080d06a4 68e0
    .zero  0x2
PTR_gPrng_080d06a8:
    .word  gPrng                          @ 080d06a8 40000003
DAT_080d06ac:
    .word  0x00000a14                     @ 080d06ac 140a0000
LAB_080d06b0:
    movs r3,#0x1    @ 080d06b0 0123
    adds r0,r3,#0x0    @ 080d06b2 181c
    ands r0,r1    @ 080d06b4 0840
    cmp r0,#0x0                              @ 080d06b6 0028
    beq LAB_080d06ec                         @ 080d06b8 18d0
    ldr r0, PTR_gP1LifePoints_080d06e0       @ 080d06ba 0948
    movs r6,#0xea    @ 080d06bc ea26
    lsls r6,r6,#0x5    @ 080d06be 7601
    adds r0,r0,r6    @ 080d06c0 8019
    ldr r6, DAT_080d06e4                     @ 080d06c2 084e
    adds r1,r4,r6    @ 080d06c4 a119
    ldrh r1,[r1,#0x0]                        @ 080d06c6 0988
    subs r1,r3,r1    @ 080d06c8 591a
    str r1,[r0,#0x0]                         @ 080d06ca 0160
    ldr r0, DAT_080d06e8                     @ 080d06cc 0648
    ands r0,r2    @ 080d06ce 1040
    movs r1,#0x80    @ 080d06d0 8021
    lsls r1,r1,#0x2    @ 080d06d2 8900
    orrs r0,r1    @ 080d06d4 0843
    str r0,[r5,#0x0]                         @ 080d06d6 2860
    movs r0,#0x24    @ 080d06d8 2420
    bl sync_state_and_init_sprite            @ 080d06da 29f0ebf9
    b LAB_080d0778                           @ 080d06de 4be0
PTR_gP1LifePoints_080d06e0:
    .word  gP1LifePoints                  @ 080d06e0 e0c40102
DAT_080d06e4:
    .word  0x00000a14                     @ 080d06e4 140a0000
DAT_080d06e8:
    .word  0xfffe01ff                     @ 080d06e8 ff01feff
LAB_080d06ec:
    movs r0,#0x2    @ 080d06ec 0220
    ands r0,r1    @ 080d06ee 0840
    cmp r0,#0x0                              @ 080d06f0 0028
    beq LAB_080d0778                         @ 080d06f2 41d0
    ldr r0, PTR_gP1LifePoints_080d071c       @ 080d06f4 0948
    movs r1,#0xea    @ 080d06f6 ea21
    lsls r1,r1,#0x5    @ 080d06f8 4901
    adds r0,r0,r1    @ 080d06fa 4018
    str r7,[r0,#0x0]                         @ 080d06fc 0760
    ldr r6, DAT_080d0720                     @ 080d06fe 084e
    adds r0,r4,r6    @ 080d0700 a019
    strh r3,[r0,#0x0]                        @ 080d0702 0380
    ldr r0, DAT_080d0724                     @ 080d0704 0748
    ands r0,r2    @ 080d0706 1040
    movs r1,#0x80    @ 080d0708 8021
    lsls r1,r1,#0x2    @ 080d070a 8900
    orrs r0,r1    @ 080d070c 0843
    str r0,[r5,#0x0]                         @ 080d070e 2860
    movs r0,#0x1    @ 080d0710 0120
    bl sync_state_and_init_sprite            @ 080d0712 29f0cff9
    movs r0,#0x1    @ 080d0716 0120
    b LAB_080d077a                           @ 080d0718 2fe0
    .zero  0x2
PTR_gP1LifePoints_080d071c:
    .word  gP1LifePoints                  @ 080d071c e0c40102
DAT_080d0720:
    .word  0x00000a14                     @ 080d0720 140a0000
DAT_080d0724:
    .word  0xfffe01ff                     @ 080d0724 ff01feff
LAB_080d0728:
    ldr r0, DAT_080d0770                     @ 080d0728 1148
    adds r0,r0,r4    @ 080d072a 0019
    .hword 0x4680    @ 080d072c 8046
    ldrb r6,[r0,#0x0]                        @ 080d072e 0678
    lsrs r0,r6,#0x1    @ 080d0730 7008
    ldr r1, DAT_080d0774                     @ 080d0732 1049
    adds r4,r4,r1    @ 080d0734 6418
    adds r3,r7,#0x0    @ 080d0736 3b1c
    ldrb r2,[r4,#0x0]                        @ 080d0738 2278
    ands r3,r2    @ 080d073a 1340
    lsls r3,r3,#0x7    @ 080d073c db01
    orrs r3,r0    @ 080d073e 0343
    adds r2,r3,#0x1    @ 080d0740 5a1c
    movs r1,#0x7f    @ 080d0742 7f21
    ands r1,r2    @ 080d0744 1140
    lsls r1,r1,#0x1    @ 080d0746 4900
    movs r5,#0x1    @ 080d0748 0125
    adds r0,r7,#0x0    @ 080d074a 381c
    ands r0,r6    @ 080d074c 3040
    orrs r0,r1    @ 080d074e 0843
    .hword 0x4646    @ 080d0750 4646
    strb r0,[r6,#0x0]                        @ 080d0752 3070
    lsrs r2,r2,#0x7    @ 080d0754 d209
    ands r2,r7    @ 080d0756 3a40
    ands r2,r5    @ 080d0758 2a40
    movs r0,#0x2    @ 080d075a 0220
    rsbs r0,r0,#0    @ 080d075c 4042
    ldrb r1,[r4,#0x0]                        @ 080d075e 2178
    ands r0,r1    @ 080d0760 0840
    orrs r0,r2    @ 080d0762 1043
    strb r0,[r4,#0x0]                        @ 080d0764 2070
    cmp r3,#0x1f                             @ 080d0766 1f2b
    bls LAB_080d0778                         @ 080d0768 06d9
    movs r0,#0x1    @ 080d076a 0120
    b LAB_080d077a                           @ 080d076c 05e0
    .zero  0x2
DAT_080d0770:
    .word  0x00000a1b                     @ 080d0770 1b0a0000
DAT_080d0774:
    .word  0x00000a1c                     @ 080d0774 1c0a0000
LAB_080d0778:
    movs r0,#0x0    @ 080d0778 0020
LAB_080d077a:
    pop {r3}                                 @ 080d077a 08bc
    .hword 0x4698    @ 080d077c 9846
    pop {r4,r5,r6,r7}                        @ 080d077e f0bc
    pop {r1}                                 @ 080d0780 02bc
    bx r1                                    @ 080d0782 0847

@ Check if duel field zone slot card attribute satisfies visibility condition (indeg=14). r0=slot_index; computes gDuelCtx+0x24+slot*0x28 (stride 5*8=0x28). Reads card_type byte at [addr+0]; reads phase_counter [0x0201e4f0+0x4] and active_zone_card [0x0201e2a0+0x4]. phase_counter==4: if card_type==active_zone_card -> return 0 (not visible). Otherwise: bl get_zone_card_attribute_by_type(card_type, attr_type=0xf). Returns 1=attribute satisfied (visible) / 0=not satisfied. Read-only; no side effects. Constants: DUEL_CTX=0x02020160; CARD_TYPE_OFFSET=0x24; STRUCT_STRIDE=0x28; PHASE_BASE=0x0201e4f0; ACTIVE_ZONE_BASE=0x0201e2a0; ATTR_TYPE=0xf.
check_zone_slot_attr_visible:
    push {lr}                                @ 080d0784 00b5
    adds r2,r0,#0x0    @ 080d0786 021c
    ldr r1, DAT_080d07b8                     @ 080d0788 0b49
    lsls r0,r2,#0x2    @ 080d078a 9000
    adds r0,r0,r2    @ 080d078c 8018
    lsls r0,r0,#0x3    @ 080d078e c000
    adds r1,#0x24    @ 080d0790 2431
    adds r0,r0,r1    @ 080d0792 4018
    ldrb r1,[r0,#0x0]                        @ 080d0794 0178
    adds r3,r1,#0x0    @ 080d0796 0b1c
    ldr r0, DAT_080d07bc                     @ 080d0798 0848
    ldr r0,[r0,#0x4]                         @ 080d079a 4068
    cmp r0,#0x4                              @ 080d079c 0428
    bne LAB_080d07b4                         @ 080d079e 09d1
    ldr r0, DAT_080d07c0                     @ 080d07a0 0748
    ldr r0,[r0,#0x4]                         @ 080d07a2 4068
    cmp r1,r0                                @ 080d07a4 8142
    beq LAB_080d07b4                         @ 080d07a6 05d0
    adds r0,r3,#0x0    @ 080d07a8 181c
    movs r1,#0xf    @ 080d07aa 0f21
    bl get_zone_card_attribute_by_type       @ 080d07ac 6af734ff
    cmp r0,#0x0                              @ 080d07b0 0028
    beq LAB_080d07c4                         @ 080d07b2 07d0
LAB_080d07b4:
    movs r0,#0x0    @ 080d07b4 0020
    b LAB_080d07c6                           @ 080d07b6 06e0
DAT_080d07b8:
    .word  0x02020160                     @ 080d07b8 60010202
DAT_080d07bc:
    .word  0x0201e4f0                     @ 080d07bc f0e40102
DAT_080d07c0:
    .word  0x0201e2a0                     @ 080d07c0 a0e20102
LAB_080d07c4:
    movs r0,#0x1    @ 080d07c4 0120
LAB_080d07c6:
    pop {r1}                                 @ 080d07c6 02bc
    bx r1                                    @ 080d07c8 0847
    .zero  0x2

@ Linear search in gDuelCtx+0x2e00 (gDuelCtx+0xb8*0x40) halfword array for entry matching r0. Array length read from gDuelCtx+0x2e40 (gDuelCtx+0xb9*0x40). Compares each [gDuelCtx+0x2e00+i*2] with r4 (=r0 input); sets r5=1 on match. Returns r5 (1=found, 0=not_found). Called exclusively by render_zone_card_anim_oam_with_base (0x080d136c). Side effects: read-only. Constants: gDuelCtx=0x02020160, anim_table_base=0x2e00 (0xb8*0x40), count_offset=0x2e40 (0xb9*0x40), entry_size=2.
check_zone_anim_id_in_table:
    push {r4,r5,r6,lr}                       @ 080d07cc 70b5
    adds r4,r0,#0x0    @ 080d07ce 041c
    movs r5,#0x0    @ 080d07d0 0025
    movs r2,#0x0    @ 080d07d2 0022
    ldr r0, DWORD_080d07ec                   @ 080d07d4 0548
    movs r3,#0xb9    @ 080d07d6 b923
    lsls r3,r3,#0x6    @ 080d07d8 9b01
    adds r1,r0,r3    @ 080d07da c118
    adds r3,r0,#0x0    @ 080d07dc 031c
    ldrb r1,[r1,#0x0]                        @ 080d07de 0978
    cmp r5,r1                                @ 080d07e0 8d42
    bge LAB_080d0810                         @ 080d07e2 15da
    movs r6,#0xb8    @ 080d07e4 b826
    lsls r6,r6,#0x6    @ 080d07e6 b601
    adds r0,r3,r6    @ 080d07e8 9819
    b LAB_080d0808                           @ 080d07ea 0de0
DWORD_080d07ec:
    .word  0x02020160                     @ 080d07ec 60010202
LAB_080d07f0:
    adds r2,#0x1    @ 080d07f0 0132
    movs r1,#0xb9    @ 080d07f2 b921
    lsls r1,r1,#0x6    @ 080d07f4 8901
    adds r0,r3,r1    @ 080d07f6 5818
    ldrb r0,[r0,#0x0]                        @ 080d07f8 0078
    cmp r2,r0                                @ 080d07fa 8242
    bge LAB_080d0810                         @ 080d07fc 08da
    lsls r0,r2,#0x1    @ 080d07fe 5000
    movs r6,#0xb8    @ 080d0800 b826
    lsls r6,r6,#0x6    @ 080d0802 b601
    adds r1,r3,r6    @ 080d0804 9919
    adds r0,r0,r1    @ 080d0806 4018
LAB_080d0808:
    ldrh r0,[r0,#0x0]                        @ 080d0808 0088
    cmp r0,r4                                @ 080d080a a042
    bne LAB_080d07f0                         @ 080d080c f0d1
    movs r5,#0x1    @ 080d080e 0125
LAB_080d0810:
    adds r0,r5,#0x0    @ 080d0810 281c
    pop {r4,r5,r6}                           @ 080d0812 70bc
    pop {r1}                                 @ 080d0814 02bc
    bx r1                                    @ 080d0816 0847

@ Duel field zone slot card display dispatcher by mode (indeg=5). r0=slot_index; r1=display_mode [0..1]. Step 1: compute gDuelCtx+0x24+slot*0x28 -> read card_status/card_attr/card_type bytes. Step 2: build OAM_attr0 halfword and strh to stack temp slot. Step 3: .hword 0x4684=mov r12,r0 saves slot_index; ldmia/stmia copies 9 slot words to stack. Step 4: strh 0 to [0x02023130+8] -> clear display_pending_flag. Step 5: compare r1 (display_mode): mode=0 -> if slot card_id matches gDuelCtx active_card_id: bl render_zone_card_jp_text_panel(r0=1); else bl render_large_card_display_by_mode. mode=1 -> bl render_zone_card_jp_text_panel(r0=1). No return value (void). Constants: DUEL_CTX=0x02020160; SLOT_STRIDE=0x28; CARD_STATUS_OFFSET=0x24; DISPLAY_FLAG_ADDR=0x02023130+8; MODE_LARGE=0; MODE_JP=1.
dispatch_zone_card_display_by_mode:
    push {r4,r5,r6,r7,lr}                    @ 080d0818 f0b5
    sub sp,#0x2c                             @ 080d081a 8bb0
    ldr r5, DWORD_080d0884                   @ 080d081c 194d
    lsls r2,r0,#0x2    @ 080d081e 8200
    adds r2,r2,r0    @ 080d0820 1218
    lsls r2,r2,#0x3    @ 080d0822 d200
    adds r4,r5,#0x0    @ 080d0824 2c1c
    adds r4,#0x24    @ 080d0826 2434
    adds r4,r2,r4    @ 080d0828 1419
    ldrb r6,[r4,#0x0]                        @ 080d082a 2678
    movs r0,#0x1    @ 080d082c 0120
    .hword 0x4684    @ 080d082e 8446
    adds r3,r6,#0x0    @ 080d0830 331c
    ands r3,r0    @ 080d0832 0340
    movs r0,#0x1f    @ 080d0834 1f20
    ldrb r7,[r4,#0x1]                        @ 080d0836 6778
    ands r0,r7    @ 080d0838 3840
    lsls r0,r0,#0x1    @ 080d083a 4000
    orrs r3,r0    @ 080d083c 0343
    ldrb r4,[r4,#0x2]                        @ 080d083e a478
    lsls r0,r4,#0x6    @ 080d0840 a001
    orrs r3,r0    @ 080d0842 0343
    movs r0,#0x80    @ 080d0844 8020
    lsls r0,r0,#0x7    @ 080d0846 c001
    orrs r3,r0    @ 080d0848 0343
    .hword 0x4668    @ 080d084a 6846
    strh r3,[r0,#0x0]                        @ 080d084c 0380
    ldr r0,[sp,#0x0]                         @ 080d084e 0098
    str r0,[sp,#0x28]                        @ 080d0850 0a90
    add r0,sp,#0x4                           @ 080d0852 01a8
    adds r2,r2,r5    @ 080d0854 5219
    ldmia r2!,{r3,r4,r5}                     @ 080d0856 38ca
    stmia r0!,{r3,r4,r5}                     @ 080d0858 38c0
    ldmia r2!,{r3,r4,r7}                     @ 080d085a 98ca
    stmia r0!,{r3,r4,r7}                     @ 080d085c 98c0
    ldmia r2!,{r3,r5,r7}                     @ 080d085e a8ca
    stmia r0!,{r3,r5,r7}                     @ 080d0860 a8c0
    ldr r2, DWORD_080d0888                   @ 080d0862 094a
    movs r0,#0x0    @ 080d0864 0020
    strh r0,[r2,#0x8]                        @ 080d0866 1081
    cmp r1,#0x0                              @ 080d0868 0029
    beq LAB_080d0890                         @ 080d086a 11d0
    movs r1,#0x0    @ 080d086c 0021
    ldr r0, DWORD_080d088c                   @ 080d086e 0748
    ldr r0,[r0,#0x4]                         @ 080d0870 4068
    .hword 0x4664    @ 080d0872 6446
    eors r0,r4    @ 080d0874 6040
    cmp r6,r0                                @ 080d0876 8642
    bne LAB_080d087c                         @ 080d0878 00d1
    movs r1,#0x1    @ 080d087a 0121
LAB_080d087c:
    adds r0,r1,#0x0    @ 080d087c 081c
    bl render_zone_card_jp_text_panel        @ 080d087e faf77bfa
    b LAB_080d089a                           @ 080d0882 0ae0
DWORD_080d0884:
    .word  0x02020160                     @ 080d0884 60010202
DWORD_080d0888:
    .word  0x02023130                     @ 080d0888 30310202
DWORD_080d088c:
    .word  0x0201e2a0                     @ 080d088c a0e20102
LAB_080d0890:
    ldr r0,[sp,#0x4]                         @ 080d0890 0198
    add r1,sp,#0x28                          @ 080d0892 0aa9
    movs r2,#0x1    @ 080d0894 0122
    bl render_large_card_display_by_mode     @ 080d0896 faf799fc
LAB_080d089a:
    add sp,#0x2c                             @ 080d089a 0bb0
    pop {r4,r5,r6,r7}                        @ 080d089c f0bc
    pop {r0}                                 @ 080d089e 01bc
    bx r0                                    @ 080d08a0 0047
    .zero  0x2

@ Full render pipeline for duel field selected zone card detail panel (indeg=2). 8 sequential steps: (1) copy_bytes_by_halfword(dst=0x0600b0e0, src=0x0988ad78, size=0x3e0) -> BG tile frame; (2) copy_bytes_by_halfword(dst=0x05000160, src=0x0988b158, size=0x40) -> OBJ palette; (3) setup_line_buf_with_font_and_align(font=0x1b, align=2, flag=1, param=0) -> JP font; (4) read gDuelCtx+0x6c2c+0x2e40 bits[2:0] (card_attr) -> update card_info_ctx+0x8/+0x4; (5) text_render_wrapper x2 -> render two JP card name lines; (6) zero_fill_by_halfword(0x0600bc00, 0x6c0) + commit_line_buffer_to_sprite_vram -> sprite VRAM; (7) tile_2d_row_copy x10+ for card frame sub-regions; (8) game_str_id_to_row x3 + measure_string_pixel_width -> centered card description. No APCS input (void); callee-save r7/r6/r5 via .hword 0x4657/464e/4645. Constants: BG_TILE_DST=0x0600b0e0; PAL_DST=0x05000160; SPRITE_BUF=0x0600bc00; FONT_ID=0x1b; CARD_ATTR_OFFSET=gDuelCtx+0x6c2c+0x2e40; GAME_STR_ID=0x3e9.
render_zone_card_detail_panel:
    push {r4,r5,r6,r7,lr}                    @ 080d08a4 f0b5
    .hword 0x4657    @ 080d08a6 5746
    .hword 0x464e    @ 080d08a8 4e46
    .hword 0x4645    @ 080d08aa 4546
    push {r5,r6,r7}                          @ 080d08ac e0b4
    sub sp,#0x10                             @ 080d08ae 84b0
    ldr r0, DWORD_080d0b58                   @ 080d08b0 a948
    ldr r1, DWORD_080d0b5c                   @ 080d08b2 aa49
    movs r2,#0xf8    @ 080d08b4 f822
    lsls r2,r2,#0x2    @ 080d08b6 9200
    bl copy_bytes_by_halfword                @ 080d08b8 24f0f4fa
    ldr r0, DWORD_080d0b60                   @ 080d08bc a848
    ldr r1, DWORD_080d0b64                   @ 080d08be a949
    movs r2,#0x20    @ 080d08c0 2022
    bl copy_bytes_by_halfword                @ 080d08c2 24f0effa
    movs r0,#0x1b    @ 080d08c6 1b20
    movs r1,#0x2    @ 080d08c8 0221
    movs r2,#0x1    @ 080d08ca 0122
    movs r3,#0x0    @ 080d08cc 0023
    bl setup_line_buf_with_font_and_align    @ 080d08ce 20f0f7f9
    ldr r2, DWORD_080d0b68                   @ 080d08d2 a54a
    ldr r0, DWORD_080d0b6c                   @ 080d08d4 a548
    ldr r1, DWORD_080d0b70                   @ 080d08d6 a649
    adds r0,r0,r1    @ 080d08d8 4018
    movs r1,#0x7    @ 080d08da 0721
    ldrb r0,[r0,#0x0]                        @ 080d08dc 0078
    ands r1,r0    @ 080d08de 0140
    rsbs r1,r1,#0    @ 080d08e0 4942
    lsrs r1,r1,#0x1f    @ 080d08e2 c90f
    movs r0,#0x2    @ 080d08e4 0220
    rsbs r0,r0,#0    @ 080d08e6 4042
    ldrb r3,[r2,#0x8]                        @ 080d08e8 137a
    ands r0,r3    @ 080d08ea 1840
    orrs r0,r1    @ 080d08ec 0843
    movs r1,#0x2    @ 080d08ee 0221
    orrs r0,r1    @ 080d08f0 0843
    strb r0,[r2,#0x8]                        @ 080d08f2 1072
    ldr r3, DWORD_080d0b74                   @ 080d08f4 9f4b
    lsls r1,r0,#0x1e    @ 080d08f6 8107
    lsrs r1,r1,#0x1f    @ 080d08f8 c90f
    lsls r1,r1,#0x2    @ 080d08fa 8900
    lsls r0,r0,#0x1f    @ 080d08fc c007
    lsrs r0,r0,#0x1f    @ 080d08fe c00f
    lsls r0,r0,#0x3    @ 080d0900 c000
    adds r1,r1,r0    @ 080d0902 0918
    adds r1,r1,r3    @ 080d0904 c918
    ldr r0,[r1,#0x0]                         @ 080d0906 0868
    str r0,[r2,#0x4]                         @ 080d0908 5060
    movs r0,#0x40    @ 080d090a 4020
    ldrb r1,[r2,#0x15]                       @ 080d090c 517d
    orrs r0,r1    @ 080d090e 0843
    strb r0,[r2,#0x15]                       @ 080d0910 5075
    ldr r2, DWORD_080d0b78                   @ 080d0912 994a
    ldr r4, DWORD_080d0b7c                   @ 080d0914 994c
    movs r0,#0x2    @ 080d0916 0220
    movs r1,#0x2    @ 080d0918 0221
    adds r3,r4,#0x0    @ 080d091a 231c
    bl text_render_wrapper                   @ 080d091c 22f0aef8
    movs r0,#0x2    @ 080d0920 0220
    movs r1,#0x2    @ 080d0922 0221
    movs r2,#0x7    @ 080d0924 0722
    adds r3,r4,#0x0    @ 080d0926 231c
    bl text_render_wrapper                   @ 080d0928 22f0a8f8
    ldr r4, DWORD_080d0b80                   @ 080d092c 944c
    movs r1,#0xd8    @ 080d092e d821
    lsls r1,r1,#0x3    @ 080d0930 c900
    adds r0,r4,#0x0    @ 080d0932 201c
    bl zero_fill_by_halfword                 @ 080d0934 24f09efa
    adds r0,r4,#0x0    @ 080d0938 201c
    movs r1,#0x0    @ 080d093a 0021
    bl commit_line_buffer_to_sprite_vram     @ 080d093c 22f086fa
    ldr r1, DWORD_080d0b84                   @ 080d0940 9049
    movs r0,#0xf0    @ 080d0942 f020
    lsls r0,r0,#0x1    @ 080d0944 4000
    movs r2,#0x0    @ 080d0946 0022
    .hword 0x4690    @ 080d0948 9046
LAB_080d094a:
    adds r5,r1,#0x0    @ 080d094a 0d1c
    adds r5,#0x40    @ 080d094c 4035
    .hword 0x4644    @ 080d094e 4446
    adds r4,#0x1    @ 080d0950 0134
    adds r2,r1,#0x0    @ 080d0952 0a1c
    movs r3,#0x1a    @ 080d0954 1a23
LAB_080d0956:
    adds r1,r0,#0x0    @ 080d0956 011c
    adds r0,r1,#0x1    @ 080d0958 481c
    lsls r0,r0,#0x10    @ 080d095a 0004
    lsrs r0,r0,#0x10    @ 080d095c 000c
    strh r1,[r2,#0x0]                        @ 080d095e 1180
    adds r2,#0x2    @ 080d0960 0232
    subs r3,#0x1    @ 080d0962 013b
    cmp r3,#0x0                              @ 080d0964 002b
    bge LAB_080d0956                         @ 080d0966 f6da
    adds r1,r5,#0x0    @ 080d0968 291c
    .hword 0x46a0    @ 080d096a a046
    cmp r4,#0x1                              @ 080d096c 012c
    ble LAB_080d094a                         @ 080d096e ecdd
    movs r0,#0x1c    @ 080d0970 1c20
    movs r1,#0x2    @ 080d0972 0221
    movs r2,#0x1    @ 080d0974 0122
    movs r3,#0x0    @ 080d0976 0023
    bl setup_line_buf_with_font_and_align    @ 080d0978 20f0a2f9
    ldr r2, DWORD_080d0b68                   @ 080d097c 7a4a
    ldr r6, DWORD_080d0b6c                   @ 080d097e 7b4e
    ldr r3, DWORD_080d0b70                   @ 080d0980 7b4b
    adds r6,r6,r3    @ 080d0982 f618
    movs r1,#0x7    @ 080d0984 0721
    ldrb r0,[r6,#0x0]                        @ 080d0986 3078
    ands r1,r0    @ 080d0988 0140
    rsbs r1,r1,#0    @ 080d098a 4942
    lsrs r1,r1,#0x1f    @ 080d098c c90f
    movs r0,#0x2    @ 080d098e 0220
    rsbs r0,r0,#0    @ 080d0990 4042
    ldrb r3,[r2,#0x8]                        @ 080d0992 137a
    ands r0,r3    @ 080d0994 1840
    orrs r0,r1    @ 080d0996 0843
    movs r1,#0x2    @ 080d0998 0221
    orrs r0,r1    @ 080d099a 0843
    strb r0,[r2,#0x8]                        @ 080d099c 1072
    ldr r3, DWORD_080d0b74                   @ 080d099e 754b
    lsls r1,r0,#0x1e    @ 080d09a0 8107
    lsrs r1,r1,#0x1f    @ 080d09a2 c90f
    lsls r1,r1,#0x2    @ 080d09a4 8900
    lsls r0,r0,#0x1f    @ 080d09a6 c007
    lsrs r0,r0,#0x1f    @ 080d09a8 c00f
    lsls r0,r0,#0x3    @ 080d09aa c000
    adds r1,r1,r0    @ 080d09ac 0918
    adds r1,r1,r3    @ 080d09ae c918
    ldr r0,[r1,#0x0]                         @ 080d09b0 0868
    str r0,[r2,#0x4]                         @ 080d09b2 5060
    movs r0,#0x40    @ 080d09b4 4020
    ldrb r1,[r2,#0x15]                       @ 080d09b6 517d
    orrs r0,r1    @ 080d09b8 0843
    strb r0,[r2,#0x15]                       @ 080d09ba 5075
    ldr r2, DWORD_080d0b88                   @ 080d09bc 724a
    .hword 0x4690    @ 080d09be 9046
    .hword 0x4640    @ 080d09c0 4046
    bl game_str_id_to_row                    @ 080d09c2 24f029fa
    ldr r3, DWORD_080d0b8c                   @ 080d09c6 714b
    .hword 0x4699    @ 080d09c8 9946
    lsls r0,r0,#0x10    @ 080d09ca 0004
    lsrs r0,r0,#0x10    @ 080d09cc 000c
    lsls r1,r0,#0x1    @ 080d09ce 4100
    adds r1,r1,r0    @ 080d09d0 0918
    lsls r1,r1,#0x1    @ 080d09d2 4900
    ldrb r2,[r6,#0x0]                        @ 080d09d4 3278
    lsls r0,r2,#0x1d    @ 080d09d6 5007
    lsrs r0,r0,#0x1d    @ 080d09d8 400f
    adds r1,r1,r0    @ 080d09da 0918
    lsls r1,r1,#0x2    @ 080d09dc 8900
    add r1,r9                                @ 080d09de 4944
    ldr r0,[r1,#0x0]                         @ 080d09e0 0868
    ldr r5, DWORD_080d0b90                   @ 080d09e2 6b4d
    adds r0,r0,r5    @ 080d09e4 4019
    bl measure_string_pixel_width            @ 080d09e6 1ff045fc
    movs r4,#0xc8    @ 080d09ea c824
    subs r4,r4,r0    @ 080d09ec 241a
    lsrs r0,r4,#0x1f    @ 080d09ee e00f
    adds r4,r4,r0    @ 080d09f0 2418
    asrs r4,r4,#0x1    @ 080d09f2 6410
    adds r4,#0x2    @ 080d09f4 0234
    ldr r3, DWORD_080d0b78                   @ 080d09f6 604b
    .hword 0x469a    @ 080d09f8 9a46
    .hword 0x4640    @ 080d09fa 4046
    bl game_str_id_to_row                    @ 080d09fc 24f00cfa
    lsls r0,r0,#0x10    @ 080d0a00 0004
    lsrs r0,r0,#0x10    @ 080d0a02 000c
    lsls r1,r0,#0x1    @ 080d0a04 4100
    adds r1,r1,r0    @ 080d0a06 0918
    lsls r1,r1,#0x1    @ 080d0a08 4900
    ldrb r2,[r6,#0x0]                        @ 080d0a0a 3278
    lsls r0,r2,#0x1d    @ 080d0a0c 5007
    lsrs r0,r0,#0x1d    @ 080d0a0e 400f
    adds r1,r1,r0    @ 080d0a10 0918
    lsls r1,r1,#0x2    @ 080d0a12 8900
    add r1,r9                                @ 080d0a14 4944
    ldr r3,[r1,#0x0]                         @ 080d0a16 0b68
    adds r3,r3,r5    @ 080d0a18 5b19
    adds r0,r4,#0x0    @ 080d0a1a 201c
    movs r1,#0x2    @ 080d0a1c 0221
    .hword 0x4652    @ 080d0a1e 5246
    bl text_render_wrapper                   @ 080d0a20 22f02cf8
    .hword 0x4640    @ 080d0a24 4046
    bl game_str_id_to_row                    @ 080d0a26 24f0f7f9
    lsls r0,r0,#0x10    @ 080d0a2a 0004
    lsrs r0,r0,#0x10    @ 080d0a2c 000c
    lsls r1,r0,#0x1    @ 080d0a2e 4100
    adds r1,r1,r0    @ 080d0a30 0918
    lsls r1,r1,#0x1    @ 080d0a32 4900
    ldrb r6,[r6,#0x0]                        @ 080d0a34 3678
    lsls r0,r6,#0x1d    @ 080d0a36 7007
    lsrs r0,r0,#0x1d    @ 080d0a38 400f
    adds r1,r1,r0    @ 080d0a3a 0918
    lsls r1,r1,#0x2    @ 080d0a3c 8900
    add r1,r9                                @ 080d0a3e 4944
    ldr r3,[r1,#0x0]                         @ 080d0a40 0b68
    adds r3,r3,r5    @ 080d0a42 5b19
    adds r0,r4,#0x0    @ 080d0a44 201c
    movs r1,#0x2    @ 080d0a46 0221
    movs r2,#0x7    @ 080d0a48 0722
    bl text_render_wrapper                   @ 080d0a4a 22f017f8
    ldr r4, DWORD_080d0b94                   @ 080d0a4e 514c
    adds r0,r4,#0x0    @ 080d0a50 201c
    movs r1,#0x0    @ 080d0a52 0021
    movs r2,#0x1c    @ 080d0a54 1c22
    movs r3,#0x2    @ 080d0a56 0223
    bl tile_2d_row_copy                      @ 080d0a58 26f03cfd
    adds r0,r4,#0x0    @ 080d0a5c 201c
    movs r1,#0x0    @ 080d0a5e 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d0a60 22f0b8fe
    ldr r0, DWORD_080d0b98                   @ 080d0a64 4c48
    ldr r1, DWORD_080d0b9c                   @ 080d0a66 4d49
    movs r2,#0x2    @ 080d0a68 0222
    movs r3,#0x4    @ 080d0a6a 0423
    bl tile_2d_row_copy                      @ 080d0a6c 26f032fd
    ldr r0, DWORD_080d0ba0                   @ 080d0a70 4b48
    ldr r4, DWORD_080d0ba4                   @ 080d0a72 4c4c
    adds r1,r4,#0x0    @ 080d0a74 211c
    movs r2,#0x10    @ 080d0a76 1022
    movs r3,#0x2    @ 080d0a78 0223
    bl tile_2d_row_copy                      @ 080d0a7a 26f02bfd
    ldr r0, DWORD_080d0ba8                   @ 080d0a7e 4a48
    movs r3,#0x80    @ 080d0a80 8023
    lsls r3,r3,#0x3    @ 080d0a82 db00
    adds r4,r4,r3    @ 080d0a84 e418
    adds r1,r4,#0x0    @ 080d0a86 211c
    movs r2,#0x10    @ 080d0a88 1022
    movs r3,#0x2    @ 080d0a8a 0223
    bl tile_2d_row_copy                      @ 080d0a8c 26f022fd
    ldr r0, DWORD_080d0bac                   @ 080d0a90 4648
    ldr r1, DWORD_080d0bb0                   @ 080d0a92 4749
    movs r2,#0x4    @ 080d0a94 0422
    movs r3,#0x4    @ 080d0a96 0423
    bl tile_2d_row_copy                      @ 080d0a98 26f01cfd
    ldr r0, DWORD_080d0bb4                   @ 080d0a9c 4548
    ldr r1, DWORD_080d0bb8                   @ 080d0a9e 4649
    movs r2,#0xa    @ 080d0aa0 0a22
    movs r3,#0x2    @ 080d0aa2 0223
    bl tile_2d_row_copy                      @ 080d0aa4 26f016fd
    ldr r0, DWORD_080d0bbc                   @ 080d0aa8 4448
    ldr r1, DWORD_080d0bc0                   @ 080d0aaa 4549
    movs r2,#0xa    @ 080d0aac 0a22
    movs r3,#0x2    @ 080d0aae 0223
    bl tile_2d_row_copy                      @ 080d0ab0 26f010fd
    ldr r0, DWORD_080d0bc4                   @ 080d0ab4 4348
    ldr r1, DWORD_080d0bc8                   @ 080d0ab6 4449
    movs r2,#0x4    @ 080d0ab8 0422
    movs r3,#0x4    @ 080d0aba 0423
    bl tile_2d_row_copy                      @ 080d0abc 26f00afd
    ldr r0, DWORD_080d0bcc                   @ 080d0ac0 4248
    ldr r1, DWORD_080d0bd0                   @ 080d0ac2 4349
    movs r2,#0x2    @ 080d0ac4 0222
    movs r3,#0x1    @ 080d0ac6 0123
    bl tile_2d_row_copy                      @ 080d0ac8 26f004fd
    ldr r0, DWORD_080d0bd4                   @ 080d0acc 4148
    ldr r1, DWORD_080d0bd8                   @ 080d0ace 4249
    movs r2,#0x4    @ 080d0ad0 0422
    movs r3,#0x2    @ 080d0ad2 0223
    bl tile_2d_row_copy                      @ 080d0ad4 26f0fefc
    ldr r0, DWORD_080d0bdc                   @ 080d0ad8 4048
    ldr r1, DWORD_080d0be0                   @ 080d0ada 4149
    movs r2,#0x4    @ 080d0adc 0422
    movs r3,#0x2    @ 080d0ade 0223
    bl tile_2d_row_copy                      @ 080d0ae0 26f0f8fc
    ldr r3, DWORD_080d0be4                   @ 080d0ae4 3f4b
    ldr r1, DWORD_080d0be8                   @ 080d0ae6 4049
    adds r0,r3,r1    @ 080d0ae8 5818
    ldrb r0,[r0,#0x0]                        @ 080d0aea 0078
    lsrs r2,r0,#0x5    @ 080d0aec 4209
    ldr r0, DWORD_080d0bec                   @ 080d0aee 3f48
    adds r1,r3,r0    @ 080d0af0 1918
    movs r0,#0x1f    @ 080d0af2 1f20
    ldrb r1,[r1,#0x0]                        @ 080d0af4 0978
    ands r0,r1    @ 080d0af6 0840
    lsls r0,r0,#0x3    @ 080d0af8 c000
    orrs r0,r2    @ 080d0afa 1043
    movs r1,#0x5    @ 080d0afc 0521
    str r1,[sp,#0x0]                         @ 080d0afe 0091
    cmp r0,#0x5                              @ 080d0b00 0528
    bhi LAB_080d0b06                         @ 080d0b02 00d8
    str r0,[sp,#0x0]                         @ 080d0b04 0090
LAB_080d0b06:
    ldr r2, DWORD_080d0bf0                   @ 080d0b06 3a4a
    adds r0,r3,r2    @ 080d0b08 9818
    ldr r0,[r0,#0x0]                         @ 080d0b0a 0068
    lsls r0,r0,#0xb    @ 080d0b0c c002
    lsrs r0,r0,#0x18    @ 080d0b0e 000e
    str r0,[sp,#0x4]                         @ 080d0b10 0190
    movs r0,#0x0    @ 080d0b12 0020
    .hword 0x4680    @ 080d0b14 8046
    ldr r1,[sp,#0x0]                         @ 080d0b16 0099
    cmp r8,r1                                @ 080d0b18 8845
    blt LAB_080d0b1e                         @ 080d0b1a 00db
    b LAB_080d0c6c                           @ 080d0b1c a6e0
LAB_080d0b1e:
    .hword 0x4699    @ 080d0b1e 9946
    ldr r2,[sp,#0x4]                         @ 080d0b20 019a
    lsls r1,r2,#0x1    @ 080d0b22 5100
    movs r0,#0xa0    @ 080d0b24 a020
    lsls r0,r0,#0x6    @ 080d0b26 8001
    add r0,r9                                @ 080d0b28 4844
    adds r0,r1,r0    @ 080d0b2a 0818
    str r0,[sp,#0xc]                         @ 080d0b2c 0390
    .hword 0x468a    @ 080d0b2e 8a46
LAB_080d0b30:
    movs r3,#0x1    @ 080d0b30 0123
    str r3,[sp,#0x8]                         @ 080d0b32 0293
    ldr r0, DWORD_080d0bf4                   @ 080d0b34 2f48
    add r0,r9                                @ 080d0b36 4844
    ldrb r0,[r0,#0x0]                        @ 080d0b38 0078
    lsrs r2,r0,#0x5    @ 080d0b3a 4209
    ldr r1, DWORD_080d0bf0                   @ 080d0b3c 2c49
    add r1,r9                                @ 080d0b3e 4944
    movs r0,#0x1f    @ 080d0b40 1f20
    ldrb r1,[r1,#0x0]                        @ 080d0b42 0978
    ands r0,r1    @ 080d0b44 0840
    lsls r0,r0,#0x3    @ 080d0b46 c000
    orrs r0,r2    @ 080d0b48 1043
    cmp r0,#0x0                              @ 080d0b4a 0028
    beq LAB_080d0bf8                         @ 080d0b4c 54d0
    movs r0,#0xa8    @ 080d0b4e a820
    lsls r0,r0,#0x6    @ 080d0b50 8001
    add r0,r9                                @ 080d0b52 4844
    add r0,r10                               @ 080d0b54 5044
    b LAB_080d0bfa                           @ 080d0b56 50e0
DWORD_080d0b58:
    .word  0x0600b0e0                     @ 080d0b58 e0b00006
DWORD_080d0b5c:
    .word  0x0988ad78                     @ 080d0b5c 78ad8809
DWORD_080d0b60:
    .word  0x05000160                     @ 080d0b60 60010005
DWORD_080d0b64:
    .word  0x0988b158                     @ 080d0b64 58b18809
DWORD_080d0b68:
    .word  0x02006ed0                     @ 080d0b68 d06e0002
DWORD_080d0b6c:
    .word  0x02000000                     @ 080d0b6c 00000002
DWORD_080d0b70:
    .word  0x00006c2c                     @ 080d0b70 2c6c0000
DWORD_080d0b74:
    .word  font_jp_base_table             @ 080d0b74 54f8e509
DWORD_080d0b78:
    .word  0x00008008                     @ 080d0b78 08800000
DWORD_080d0b7c:
    .word  0x02022fac                     @ 080d0b7c ac2f0202
DWORD_080d0b80:
    .word  0x0600bc00                     @ 080d0b80 00bc0006
DWORD_080d0b84:
    .word  0x0600f00a                     @ 080d0b84 0af00006
DWORD_080d0b88:
    .word  0x000003e9                     @ 080d0b88 e9030000
DWORD_080d0b8c:
    .word  game_str_pointer_table         @ 080d0b8c 400f0008
DWORD_080d0b90:
    .word  game_str_ja                    @ 080d0b90 109cdb09
DWORD_080d0b94:
    .word  0x06012c00                     @ 080d0b94 002c0106
DWORD_080d0b98:
    .word  0x060157c0                     @ 080d0b98 c0570106
DWORD_080d0b9c:
    .word  0x0988c6f0                     @ 080d0b9c f0c68809
DWORD_080d0ba0:
    .word  0x06013400                     @ 080d0ba0 00340106
DWORD_080d0ba4:
    .word  0x0988bbd0                     @ 080d0ba4 d0bb8809
DWORD_080d0ba8:
    .word  0x06013600                     @ 080d0ba8 00360106
DWORD_080d0bac:
    .word  0x06015600                     @ 080d0bac 00560106
DWORD_080d0bb0:
    .word  0x0988c7f0                     @ 080d0bb0 f0c78809
DWORD_080d0bb4:
    .word  0x06015680                     @ 080d0bb4 80560106
DWORD_080d0bb8:
    .word  0x0988c9f0                     @ 080d0bb8 f0c98809
DWORD_080d0bbc:
    .word  0x06015e80                     @ 080d0bbc 805e0106
DWORD_080d0bc0:
    .word  0x0988cc70                     @ 080d0bc0 70cc8809
DWORD_080d0bc4:
    .word  0x06013f80                     @ 080d0bc4 803f0106
DWORD_080d0bc8:
    .word  0x0988c3f0                     @ 080d0bc8 f0c38809
DWORD_080d0bcc:
    .word  0x06012800                     @ 080d0bcc 00280106
DWORD_080d0bd0:
    .word  0x0988cef0                     @ 080d0bd0 f0ce8809
DWORD_080d0bd4:
    .word  0x06014f00                     @ 080d0bd4 004f0106
DWORD_080d0bd8:
    .word  0x0988c5f0                     @ 080d0bd8 f0c58809
DWORD_080d0bdc:
    .word  0x06014f80                     @ 080d0bdc 804f0106
DWORD_080d0be0:
    .word  0x0988bad0                     @ 080d0be0 d0ba8809
DWORD_080d0be4:
    .word  0x02020160                     @ 080d0be4 60010202
DWORD_080d0be8:
    .word  0x00002f57                     @ 080d0be8 572f0000
DWORD_080d0bec:
    .word  0x00002f58                     @ 080d0bec 582f0000
DWORD_080d0bf0:
    .word  0x00002f54                     @ 080d0bf0 542f0000
DWORD_080d0bf4:
    .word  0x00002f53                     @ 080d0bf4 532f0000
LAB_080d0bf8:
    ldr r0,[sp,#0xc]                         @ 080d0bf8 0398
LAB_080d0bfa:
    ldrh r4,[r0,#0x0]                        @ 080d0bfa 0488
    ldr r7,[sp,#0x4]                         @ 080d0bfc 019f
    add r7,r8                                @ 080d0bfe 4744
    adds r0,r7,#0x0    @ 080d0c00 381c
    movs r1,#0x5    @ 080d0c02 0521
    bl __modsi3                              @ 080d0c04 3df04afd
    adds r6,r0,#0x0    @ 080d0c08 061c
    adds r0,r4,#0x0    @ 080d0c0a 201c
    bl check_zone_slot_attr_visible          @ 080d0c0c fff7bafd
    cmp r0,#0x0                              @ 080d0c10 0028
    beq LAB_080d0c18                         @ 080d0c12 01d0
    movs r1,#0x0    @ 080d0c14 0021
    str r1,[sp,#0x8]                         @ 080d0c16 0291
LAB_080d0c18:
    lsls r0,r4,#0x2    @ 080d0c18 a000
    adds r0,r0,r4    @ 080d0c1a 0019
    lsls r0,r0,#0x3    @ 080d0c1c c000
    add r0,r9                                @ 080d0c1e 4844
    ldr r5,[r0,#0x0]                         @ 080d0c20 0568
    adds r0,r6,#0x0    @ 080d0c22 301c
    movs r1,#0x3    @ 080d0c24 0321
    bl __modsi3                              @ 080d0c26 3df039fd
    adds r4,r0,#0x0    @ 080d0c2a 041c
    lsls r4,r4,#0x3    @ 080d0c2c e400
    movs r2,#0x88    @ 080d0c2e 8822
    lsls r2,r2,#0x2    @ 080d0c30 9200
    adds r4,r4,r2    @ 080d0c32 a418
    adds r0,r6,#0x0    @ 080d0c34 301c
    movs r1,#0x3    @ 080d0c36 0321
    bl __divsi3                              @ 080d0c38 3df0e4fc
    lsls r0,r0,#0x7    @ 080d0c3c c001
    adds r4,r4,r0    @ 080d0c3e 2418
    lsls r4,r4,#0x10    @ 080d0c40 2404
    lsrs r4,r4,#0x10    @ 080d0c42 240c
    adds r0,r5,#0x0    @ 080d0c44 281c
    ldr r1,[sp,#0x8]                         @ 080d0c46 0299
    movs r2,#0x0    @ 080d0c48 0022
    adds r3,r4,#0x0    @ 080d0c4a 231c
    bl load_card_list_small_image            @ 080d0c4c f2f7b6fb
    adds r0,r7,#0x0    @ 080d0c50 381c
    bl render_zone_slot_card_icon_tile       @ 080d0c52 02f0edfd
    ldr r3,[sp,#0xc]                         @ 080d0c56 039b
    adds r3,#0x2    @ 080d0c58 0233
    str r3,[sp,#0xc]                         @ 080d0c5a 0393
    movs r0,#0x2    @ 080d0c5c 0220
    add r10,r0                               @ 080d0c5e 8244
    movs r1,#0x1    @ 080d0c60 0121
    add r8,r1                                @ 080d0c62 8844
    ldr r2,[sp,#0x0]                         @ 080d0c64 009a
    cmp r8,r2                                @ 080d0c66 9045
    bge LAB_080d0c6c                         @ 080d0c68 00da
    b LAB_080d0b30                           @ 080d0c6a 61e7
LAB_080d0c6c:
    add sp,#0x10                             @ 080d0c6c 04b0
    pop {r3,r4,r5}                           @ 080d0c6e 38bc
    .hword 0x4698    @ 080d0c70 9846
    .hword 0x46a1    @ 080d0c72 a146
    .hword 0x46aa    @ 080d0c74 aa46
    pop {r4,r5,r6,r7}                        @ 080d0c76 f0bc
    pop {r0}                                 @ 080d0c78 01bc
    bx r0                                    @ 080d0c7a 0047

@ Alt variant of render_zone_card_anim_oam_frame (0x080d1088). Same: reads gDuelCtx+0x2f53/0x2f54 to synthesize type_combined. Difference: if type_combined!=0, applies 'subs r1,r0,#5' (minus-5 offset) then checks r1>0 to enter multi-column OAM write logic (LAB_080d0cf6) with col_count=0x10 and col_step=0x54. Called by render_zone_card_anim_dual_pass (0x080d1b2c) as fallback when type_combined>5. Side effects: OAM writes via write_oam_entry_from_packed_args. Constants: gDuelCtx=0x02020160, status_offset=0x2f53, low_offset=0x2f54, word_offset=0x2f58, col_count=0x10, col_step=0x54.
render_zone_card_anim_oam_frame_alt:
    push {r4,r5,r6,r7,lr}                    @ 080d0c7c f0b5
    .hword 0x4657    @ 080d0c7e 5746
    .hword 0x464e    @ 080d0c80 4e46
    .hword 0x4645    @ 080d0c82 4546
    push {r5,r6,r7}                          @ 080d0c84 e0b4
    sub sp,#0x10                             @ 080d0c86 84b0
    ldr r1, DWORD_080d0cb4                   @ 080d0c88 0a49
    ldr r2, DWORD_080d0cb8                   @ 080d0c8a 0b4a
    adds r0,r1,r2    @ 080d0c8c 8818
    ldrb r0,[r0,#0x0]                        @ 080d0c8e 0078
    lsrs r3,r0,#0x5    @ 080d0c90 4309
    ldr r4, DWORD_080d0cbc                   @ 080d0c92 0a4c
    adds r2,r1,r4    @ 080d0c94 0a19
    movs r4,#0x1f    @ 080d0c96 1f24
    adds r0,r4,#0x0    @ 080d0c98 201c
    ldrb r2,[r2,#0x0]                        @ 080d0c9a 1278
    ands r0,r2    @ 080d0c9c 1040
    lsls r0,r0,#0x3    @ 080d0c9e c000
    orrs r0,r3    @ 080d0ca0 1843
    cmp r0,#0x0                              @ 080d0ca2 0028
    beq LAB_080d0cc4                         @ 080d0ca4 0ed0
    adds r5,r1,#0x0    @ 080d0ca6 0d1c
    ldr r6, DWORD_080d0cc0                   @ 080d0ca8 054e
    adds r0,r5,r6    @ 080d0caa a819
    ldrh r0,[r0,#0x0]                        @ 080d0cac 0088
    lsls r0,r0,#0x13    @ 080d0cae c004
    lsrs r0,r0,#0x18    @ 080d0cb0 000e
    b LAB_080d0cdc                           @ 080d0cb2 13e0
DWORD_080d0cb4:
    .word  0x02020160                     @ 080d0cb4 60010202
DWORD_080d0cb8:
    .word  0x00002f53                     @ 080d0cb8 532f0000
DWORD_080d0cbc:
    .word  0x00002f54                     @ 080d0cbc 542f0000
DWORD_080d0cc0:
    .word  0x00002f58                     @ 080d0cc0 582f0000
LAB_080d0cc4:
    ldr r7, DWORD_080d0d38                   @ 080d0cc4 1c4f
    ldr r1, DWORD_080d0d3c                   @ 080d0cc6 1d49
    adds r0,r7,r1    @ 080d0cc8 7818
    ldrb r0,[r0,#0x0]                        @ 080d0cca 0078
    lsrs r2,r0,#0x5    @ 080d0ccc 4209
    ldr r3, DWORD_080d0d40                   @ 080d0cce 1c4b
    adds r1,r7,r3    @ 080d0cd0 f918
    adds r0,r4,#0x0    @ 080d0cd2 201c
    ldrb r1,[r1,#0x0]                        @ 080d0cd4 0978
    ands r0,r1    @ 080d0cd6 0840
    lsls r0,r0,#0x3    @ 080d0cd8 c000
    orrs r0,r2    @ 080d0cda 1043
LAB_080d0cdc:
    subs r1,r0,#0x5    @ 080d0cdc 411f
    ldr r4, DWORD_080d0d38                   @ 080d0cde 164c
    ldr r5, DWORD_080d0d44                   @ 080d0ce0 184d
    adds r2,r4,r5    @ 080d0ce2 6219
    ldr r0,[r2,#0x0]                         @ 080d0ce4 1068
    lsls r0,r0,#0xb    @ 080d0ce6 c002
    lsrs r0,r0,#0x18    @ 080d0ce8 000e
    str r0,[sp,#0x0]                         @ 080d0cea 0090
    movs r6,#0x10    @ 080d0cec 1026
    str r6,[sp,#0x4]                         @ 080d0cee 0196
    cmp r1,#0x0                              @ 080d0cf0 0029
    bgt LAB_080d0cf6                         @ 080d0cf2 00dc
    b LAB_080d106e                           @ 080d0cf4 bbe1
LAB_080d0cf6:
    movs r7,#0x15    @ 080d0cf6 1527
    lsls r7,r7,#0x2    @ 080d0cf8 bf00
    str r7,[sp,#0xc]                         @ 080d0cfa 0397
    cmp r0,r1                                @ 080d0cfc 8842
    bne LAB_080d0d6e                         @ 080d0cfe 36d1
    movs r0,#0x0    @ 080d0d00 0020
    str r0,[sp,#0x0]                         @ 080d0d02 0090
    adds r0,r7,#0x0    @ 080d0d04 381c
    adds r0,#0x15    @ 080d0d06 1530
    lsls r4,r0,#0x3    @ 080d0d08 c400
    movs r0,#0x15    @ 080d0d0a 1520
    adds r0,#0x2    @ 080d0d0c 0230
    lsls r5,r0,#0x3    @ 080d0d0e c500
    ldr r1, DWORD_080d0d38                   @ 080d0d10 0949
    ldr r3, DWORD_080d0d48                   @ 080d0d12 0d4b
    adds r0,r1,r3    @ 080d0d14 c818
    ldrb r0,[r0,#0x0]                        @ 080d0d16 0078
    lsrs r1,r0,#0x5    @ 080d0d18 4109
    movs r3,#0x1f    @ 080d0d1a 1f23
    adds r0,r3,#0x0    @ 080d0d1c 181c
    ldrb r2,[r2,#0x0]                        @ 080d0d1e 1278
    ands r0,r2    @ 080d0d20 1040
    lsls r0,r0,#0x3    @ 080d0d22 c000
    orrs r0,r1    @ 080d0d24 0843
    cmp r0,#0x0                              @ 080d0d26 0028
    beq LAB_080d0d4c                         @ 080d0d28 10d0
    ldr r6, DWORD_080d0d38                   @ 080d0d2a 034e
    ldr r7, DWORD_080d0d40                   @ 080d0d2c 044f
    adds r0,r6,r7    @ 080d0d2e f019
    ldrh r0,[r0,#0x0]                        @ 080d0d30 0088
    lsls r1,r0,#0x13    @ 080d0d32 c104
    lsrs r1,r1,#0x18    @ 080d0d34 090e
    b LAB_080d0d64                           @ 080d0d36 15e0
DWORD_080d0d38:
    .word  0x02020160                     @ 080d0d38 60010202
DWORD_080d0d3c:
    .word  0x00002f57                     @ 080d0d3c 572f0000
DWORD_080d0d40:
    .word  0x00002f58                     @ 080d0d40 582f0000
DWORD_080d0d44:
    .word  0x00002f54                     @ 080d0d44 542f0000
DWORD_080d0d48:
    .word  0x00002f53                     @ 080d0d48 532f0000
LAB_080d0d4c:
    ldr r1, DWORD_080d0d88                   @ 080d0d4c 0e49
    ldr r2, DWORD_080d0d8c                   @ 080d0d4e 0f4a
    adds r0,r1,r2    @ 080d0d50 8818
    ldrb r0,[r0,#0x0]                        @ 080d0d52 0078
    lsrs r2,r0,#0x5    @ 080d0d54 4209
    ldr r6, DWORD_080d0d90                   @ 080d0d56 0e4e
    adds r0,r1,r6    @ 080d0d58 8819
    adds r1,r3,#0x0    @ 080d0d5a 191c
    ldrb r0,[r0,#0x0]                        @ 080d0d5c 0078
    ands r1,r0    @ 080d0d5e 0140
    lsls r1,r1,#0x3    @ 080d0d60 c900
    orrs r1,r2    @ 080d0d62 1143
LAB_080d0d64:
    adds r0,r4,#0x0    @ 080d0d64 201c
    bl __divsi3                              @ 080d0d66 3df04dfc
    subs r5,r5,r0    @ 080d0d6a 2d1a
    str r5,[sp,#0x4]                         @ 080d0d6c 0195
LAB_080d0d6e:
    movs r7,#0x0    @ 080d0d6e 0027
    .hword 0x46ba    @ 080d0d70 ba46
    ldr r0,[sp,#0xc]                         @ 080d0d72 0398
    adds r0,#0x15    @ 080d0d74 1530
    str r0,[sp,#0x8]                         @ 080d0d76 0290
    ldr r1, DWORD_080d0d88                   @ 080d0d78 0349
    .hword 0x4689    @ 080d0d7a 8946
    adds r2,r1,#0x0    @ 080d0d7c 0a1c
    ldr r3, DWORD_080d0d90                   @ 080d0d7e 044b
    adds r2,r2,r3    @ 080d0d80 d218
    .hword 0x4690    @ 080d0d82 9046
    b LAB_080d0e2a                           @ 080d0d84 51e0
    .zero  0x2
DWORD_080d0d88:
    .word  0x02020160                     @ 080d0d88 60010202
DWORD_080d0d8c:
    .word  0x00002f57                     @ 080d0d8c 572f0000
DWORD_080d0d90:
    .word  0x00002f58                     @ 080d0d90 582f0000
LAB_080d0d94:
    ldr r0, DWORD_080d0dac                   @ 080d0d94 0548
    add r0,r9                                @ 080d0d96 4844
    ldrb r0,[r0,#0x0]                        @ 080d0d98 0078
    lsrs r0,r0,#0x5    @ 080d0d9a 4009
    movs r1,#0x1f    @ 080d0d9c 1f21
    .hword 0x4644    @ 080d0d9e 4446
    ldrb r4,[r4,#0x0]                        @ 080d0da0 2478
    ands r1,r4    @ 080d0da2 2140
    lsls r1,r1,#0x3    @ 080d0da4 c900
    orrs r1,r0    @ 080d0da6 0143
    b LAB_080d0e4c                           @ 080d0da8 50e0
    .zero  0x2
DWORD_080d0dac:
    .word  0x00002f57                     @ 080d0dac 572f0000
LAB_080d0db0:
    ldr r5,[sp,#0x0]                         @ 080d0db0 009d
    movs r6,#0x15    @ 080d0db2 1526
    adds r0,r5,#0x0    @ 080d0db4 281c
    muls r0,r6    @ 080d0db6 7043
    lsls r5,r0,#0x3    @ 080d0db8 c500
    ldr r1,[sp,#0x4]                         @ 080d0dba 0199
    adds r1,#0x28    @ 080d0dbc 2831
    .hword 0x4657    @ 080d0dbe 5746
    lsls r0,r7,#0x3    @ 080d0dc0 f800
    adds r6,r1,r0    @ 080d0dc2 0e18
    movs r0,#0x68    @ 080d0dc4 6820
    adds r0,#0x10    @ 080d0dc6 1030
    lsls r7,r0,#0x10    @ 080d0dc8 0704
    ldr r3, DWORD_080d0df4                   @ 080d0dca 0a4b
    ldr r1, DWORD_080d0df8                   @ 080d0dcc 0a49
    adds r0,r3,r1    @ 080d0dce 5818
    ldrb r0,[r0,#0x0]                        @ 080d0dd0 0078
    lsrs r2,r0,#0x5    @ 080d0dd2 4209
    ldr r4, DWORD_080d0dfc                   @ 080d0dd4 094c
    adds r1,r3,r4    @ 080d0dd6 1919
    movs r4,#0x1f    @ 080d0dd8 1f24
    adds r0,r4,#0x0    @ 080d0dda 201c
    ldrb r1,[r1,#0x0]                        @ 080d0ddc 0978
    ands r0,r1    @ 080d0dde 0840
    lsls r0,r0,#0x3    @ 080d0de0 c000
    orrs r0,r2    @ 080d0de2 1043
    cmp r0,#0x0                              @ 080d0de4 0028
    beq LAB_080d0e00                         @ 080d0de6 0bd0
    .hword 0x4640    @ 080d0de8 4046
    ldrh r0,[r0,#0x0]                        @ 080d0dea 0088
    lsls r1,r0,#0x13    @ 080d0dec c104
    lsrs r1,r1,#0x18    @ 080d0dee 090e
    b LAB_080d0e14                           @ 080d0df0 10e0
    .zero  0x2
DWORD_080d0df4:
    .word  0x02020160                     @ 080d0df4 60010202
DWORD_080d0df8:
    .word  0x00002f53                     @ 080d0df8 532f0000
DWORD_080d0dfc:
    .word  0x00002f54                     @ 080d0dfc 542f0000
LAB_080d0e00:
    ldr r1, DWORD_080d0e94                   @ 080d0e00 2449
    adds r0,r3,r1    @ 080d0e02 5818
    ldrb r0,[r0,#0x0]                        @ 080d0e04 0078
    lsrs r0,r0,#0x5    @ 080d0e06 4009
    adds r1,r4,#0x0    @ 080d0e08 211c
    .hword 0x4642    @ 080d0e0a 4246
    ldrb r2,[r2,#0x0]                        @ 080d0e0c 1278
    ands r1,r2    @ 080d0e0e 1140
    lsls r1,r1,#0x3    @ 080d0e10 c900
    orrs r1,r0    @ 080d0e12 0143
LAB_080d0e14:
    adds r0,r5,#0x0    @ 080d0e14 281c
    bl __divsi3                              @ 080d0e16 3df0f5fb
    adds r0,r6,r0    @ 080d0e1a 3018
    orrs r0,r7    @ 080d0e1c 3843
    movs r1,#0x0    @ 080d0e1e 0021
    ldr r2, DWORD_080d0e98                   @ 080d0e20 1d4a
    bl write_oam_entry_from_packed_args      @ 080d0e22 25f0a3f9
    movs r3,#0x1    @ 080d0e26 0123
    add r10,r3                               @ 080d0e28 9a44
LAB_080d0e2a:
    ldr r0, DWORD_080d0e9c                   @ 080d0e2a 1c48
    add r0,r9                                @ 080d0e2c 4844
    ldrb r0,[r0,#0x0]                        @ 080d0e2e 0078
    lsrs r2,r0,#0x5    @ 080d0e30 4209
    ldr r1, DWORD_080d0ea0                   @ 080d0e32 1b49
    add r1,r9                                @ 080d0e34 4944
    movs r0,#0x1f    @ 080d0e36 1f20
    ldrb r1,[r1,#0x0]                        @ 080d0e38 0978
    ands r0,r1    @ 080d0e3a 0840
    lsls r0,r0,#0x3    @ 080d0e3c c000
    orrs r0,r2    @ 080d0e3e 1043
    cmp r0,#0x0                              @ 080d0e40 0028
    beq LAB_080d0d94                         @ 080d0e42 a7d0
    .hword 0x4644    @ 080d0e44 4446
    ldrh r4,[r4,#0x0]                        @ 080d0e46 2488
    lsls r1,r4,#0x13    @ 080d0e48 e104
    lsrs r1,r1,#0x18    @ 080d0e4a 090e
LAB_080d0e4c:
    ldr r0,[sp,#0x8]                         @ 080d0e4c 0298
    bl __divsi3                              @ 080d0e4e 3df0d9fb
    cmp r10,r0                               @ 080d0e52 8245
    blt LAB_080d0db0                         @ 080d0e54 acdb
    ldr r0,[sp,#0xc]                         @ 080d0e56 0398
    adds r0,#0x15    @ 080d0e58 1530
    lsls r4,r0,#0x3    @ 080d0e5a c400
    ldr r5, DWORD_080d0ea4                   @ 080d0e5c 114d
    ldr r6, DWORD_080d0e9c                   @ 080d0e5e 0f4e
    adds r0,r5,r6    @ 080d0e60 a819
    ldrb r0,[r0,#0x0]                        @ 080d0e62 0078
    lsrs r2,r0,#0x5    @ 080d0e64 4209
    ldr r7, DWORD_080d0ea0                   @ 080d0e66 0e4f
    adds r1,r5,r7    @ 080d0e68 e919
    movs r3,#0x1f    @ 080d0e6a 1f23
    adds r0,r3,#0x0    @ 080d0e6c 181c
    ldrb r1,[r1,#0x0]                        @ 080d0e6e 0978
    ands r0,r1    @ 080d0e70 0840
    lsls r0,r0,#0x3    @ 080d0e72 c000
    orrs r0,r2    @ 080d0e74 1043
    cmp r0,#0x0                              @ 080d0e76 0028
    beq LAB_080d0eac                         @ 080d0e78 18d0
    ldr r1, DWORD_080d0ea8                   @ 080d0e7a 0b49
    adds r0,r5,r1    @ 080d0e7c 6818
    ldrh r0,[r0,#0x0]                        @ 080d0e7e 0088
    lsls r1,r0,#0x13    @ 080d0e80 c104
    lsrs r1,r1,#0x18    @ 080d0e82 090e
    adds r0,r4,#0x0    @ 080d0e84 201c
    bl __divsi3                              @ 080d0e86 3df0bdfb
    movs r1,#0x7    @ 080d0e8a 0721
    ands r1,r0    @ 080d0e8c 0140
    cmp r1,#0x0                              @ 080d0e8e 0029
    bne LAB_080d0ed6                         @ 080d0e90 21d1
    b LAB_080d106e                           @ 080d0e92 ece0
DWORD_080d0e94:
    .word  0x00002f57                     @ 080d0e94 572f0000
DWORD_080d0e98:
    .word  0x000022be                     @ 080d0e98 be220000
DWORD_080d0e9c:
    .word  0x00002f53                     @ 080d0e9c 532f0000
DWORD_080d0ea0:
    .word  0x00002f54                     @ 080d0ea0 542f0000
DWORD_080d0ea4:
    .word  0x02020160                     @ 080d0ea4 60010202
DWORD_080d0ea8:
    .word  0x00002f58                     @ 080d0ea8 582f0000
LAB_080d0eac:
    ldr r2, DWORD_080d0f1c                   @ 080d0eac 1b4a
    ldr r5, DWORD_080d0f20                   @ 080d0eae 1c4d
    adds r0,r2,r5    @ 080d0eb0 5019
    ldrb r0,[r0,#0x0]                        @ 080d0eb2 0078
    lsrs r2,r0,#0x5    @ 080d0eb4 4209
    ldr r6, DWORD_080d0f1c                   @ 080d0eb6 194e
    ldr r7, DWORD_080d0f24                   @ 080d0eb8 1a4f
    adds r0,r6,r7    @ 080d0eba f019
    adds r1,r3,#0x0    @ 080d0ebc 191c
    ldrb r0,[r0,#0x0]                        @ 080d0ebe 0078
    ands r1,r0    @ 080d0ec0 0140
    lsls r1,r1,#0x3    @ 080d0ec2 c900
    orrs r1,r2    @ 080d0ec4 1143
    adds r0,r4,#0x0    @ 080d0ec6 201c
    bl __divsi3                              @ 080d0ec8 3df09cfb
    movs r1,#0x7    @ 080d0ecc 0721
    ands r1,r0    @ 080d0ece 0140
    cmp r1,#0x0                              @ 080d0ed0 0029
    bne LAB_080d0ed6                         @ 080d0ed2 00d1
    b LAB_080d106e                           @ 080d0ed4 cbe0
LAB_080d0ed6:
    ldr r1,[sp,#0x0]                         @ 080d0ed6 0099
    movs r2,#0x15    @ 080d0ed8 1522
    adds r0,r1,#0x0    @ 080d0eda 081c
    muls r0,r2    @ 080d0edc 5043
    lsls r4,r0,#0x3    @ 080d0ede c400
    ldr r1,[sp,#0x4]                         @ 080d0ee0 0199
    adds r1,#0x28    @ 080d0ee2 2831
    .hword 0x4653    @ 080d0ee4 5346
    lsls r0,r3,#0x3    @ 080d0ee6 d800
    adds r5,r1,r0    @ 080d0ee8 0d18
    movs r0,#0x68    @ 080d0eea 6820
    adds r0,#0x10    @ 080d0eec 1030
    lsls r7,r0,#0x10    @ 080d0eee 0704
    ldr r6, DWORD_080d0f1c                   @ 080d0ef0 0a4e
    ldr r1, DWORD_080d0f28                   @ 080d0ef2 0d49
    adds r0,r6,r1    @ 080d0ef4 7018
    ldrb r0,[r0,#0x0]                        @ 080d0ef6 0078
    lsrs r2,r0,#0x5    @ 080d0ef8 4209
    ldr r3, DWORD_080d0f2c                   @ 080d0efa 0c4b
    adds r1,r6,r3    @ 080d0efc f118
    movs r3,#0x1f    @ 080d0efe 1f23
    adds r0,r3,#0x0    @ 080d0f00 181c
    ldrb r1,[r1,#0x0]                        @ 080d0f02 0978
    ands r0,r1    @ 080d0f04 0840
    lsls r0,r0,#0x3    @ 080d0f06 c000
    orrs r0,r2    @ 080d0f08 1043
    cmp r0,#0x0                              @ 080d0f0a 0028
    beq LAB_080d0f30                         @ 080d0f0c 10d0
    ldr r1, DWORD_080d0f24                   @ 080d0f0e 0549
    adds r0,r6,r1    @ 080d0f10 7018
    ldrh r0,[r0,#0x0]                        @ 080d0f12 0088
    lsls r1,r0,#0x13    @ 080d0f14 c104
    lsrs r1,r1,#0x18    @ 080d0f16 090e
    b LAB_080d0f4a                           @ 080d0f18 17e0
    .zero  0x2
DWORD_080d0f1c:
    .word  0x02020160                     @ 080d0f1c 60010202
DWORD_080d0f20:
    .word  0x00002f57                     @ 080d0f20 572f0000
DWORD_080d0f24:
    .word  0x00002f58                     @ 080d0f24 582f0000
DWORD_080d0f28:
    .word  0x00002f53                     @ 080d0f28 532f0000
DWORD_080d0f2c:
    .word  0x00002f54                     @ 080d0f2c 542f0000
LAB_080d0f30:
    ldr r2, DWORD_080d0f84                   @ 080d0f30 144a
    ldr r6, DWORD_080d0f88                   @ 080d0f32 154e
    adds r0,r2,r6    @ 080d0f34 9019
    ldrb r0,[r0,#0x0]                        @ 080d0f36 0078
    lsrs r2,r0,#0x5    @ 080d0f38 4209
    ldr r1, DWORD_080d0f84                   @ 080d0f3a 1249
    adds r6,#0x1    @ 080d0f3c 0136
    adds r0,r1,r6    @ 080d0f3e 8819
    adds r1,r3,#0x0    @ 080d0f40 191c
    ldrb r0,[r0,#0x0]                        @ 080d0f42 0078
    ands r1,r0    @ 080d0f44 0140
    lsls r1,r1,#0x3    @ 080d0f46 c900
    orrs r1,r2    @ 080d0f48 1143
LAB_080d0f4a:
    adds r0,r4,#0x0    @ 080d0f4a 201c
    bl __divsi3                              @ 080d0f4c 3df05afb
    adds r6,r5,r0    @ 080d0f50 2e18
    orrs r6,r7    @ 080d0f52 3e43
    ldr r0,[sp,#0xc]                         @ 080d0f54 0398
    adds r0,#0x15    @ 080d0f56 1530
    lsls r5,r0,#0x3    @ 080d0f58 c500
    ldr r7, DWORD_080d0f84                   @ 080d0f5a 0a4f
    ldr r1, DWORD_080d0f8c                   @ 080d0f5c 0b49
    adds r0,r7,r1    @ 080d0f5e 7818
    ldrb r0,[r0,#0x0]                        @ 080d0f60 0078
    lsrs r2,r0,#0x5    @ 080d0f62 4209
    ldr r3, DWORD_080d0f90                   @ 080d0f64 0a4b
    adds r1,r7,r3    @ 080d0f66 f918
    movs r3,#0x1f    @ 080d0f68 1f23
    adds r0,r3,#0x0    @ 080d0f6a 181c
    ldrb r1,[r1,#0x0]                        @ 080d0f6c 0978
    ands r0,r1    @ 080d0f6e 0840
    lsls r0,r0,#0x3    @ 080d0f70 c000
    orrs r0,r2    @ 080d0f72 1043
    cmp r0,#0x0                              @ 080d0f74 0028
    beq LAB_080d0f98                         @ 080d0f76 0fd0
    ldr r4, DWORD_080d0f94                   @ 080d0f78 064c
    adds r0,r7,r4    @ 080d0f7a 3819
    ldrh r0,[r0,#0x0]                        @ 080d0f7c 0088
    lsls r1,r0,#0x13    @ 080d0f7e c104
    lsrs r1,r1,#0x18    @ 080d0f80 090e
    b LAB_080d0fb0                           @ 080d0f82 15e0
DWORD_080d0f84:
    .word  0x02020160                     @ 080d0f84 60010202
DWORD_080d0f88:
    .word  0x00002f57                     @ 080d0f88 572f0000
DWORD_080d0f8c:
    .word  0x00002f53                     @ 080d0f8c 532f0000
DWORD_080d0f90:
    .word  0x00002f54                     @ 080d0f90 542f0000
DWORD_080d0f94:
    .word  0x00002f58                     @ 080d0f94 582f0000
LAB_080d0f98:
    ldr r1, DWORD_080d1000                   @ 080d0f98 1949
    ldr r2, DWORD_080d1004                   @ 080d0f9a 1a4a
    adds r0,r1,r2    @ 080d0f9c 8818
    ldrb r0,[r0,#0x0]                        @ 080d0f9e 0078
    lsrs r2,r0,#0x5    @ 080d0fa0 4209
    ldr r4, DWORD_080d1008                   @ 080d0fa2 194c
    adds r0,r1,r4    @ 080d0fa4 0819
    adds r1,r3,#0x0    @ 080d0fa6 191c
    ldrb r0,[r0,#0x0]                        @ 080d0fa8 0078
    ands r1,r0    @ 080d0faa 0140
    lsls r1,r1,#0x3    @ 080d0fac c900
    orrs r1,r2    @ 080d0fae 1143
LAB_080d0fb0:
    adds r0,r5,#0x0    @ 080d0fb0 281c
    bl __divsi3                              @ 080d0fb2 3df027fb
    adds r1,r0,#0x0    @ 080d0fb6 011c
    cmp r1,#0x0                              @ 080d0fb8 0029
    bge LAB_080d0fbe                         @ 080d0fba 00da
    adds r0,r1,#0x7    @ 080d0fbc c81d
LAB_080d0fbe:
    asrs r0,r0,#0x3    @ 080d0fbe c010
    lsls r0,r0,#0x3    @ 080d0fc0 c000
    subs r0,r1,r0    @ 080d0fc2 081a
    movs r1,#0x8    @ 080d0fc4 0821
    subs r0,r1,r0    @ 080d0fc6 081a
    cmp r0,#0x0                              @ 080d0fc8 0028
    bge LAB_080d0fce                         @ 080d0fca 00da
    adds r0,#0x3    @ 080d0fcc 0330
LAB_080d0fce:
    asrs r0,r0,#0x2    @ 080d0fce 8010
    ldr r7, DWORD_080d100c                   @ 080d0fd0 0e4f
    adds r4,r0,r7    @ 080d0fd2 c419
    ldr r1, DWORD_080d1000                   @ 080d0fd4 0a49
    ldr r2, DWORD_080d1010                   @ 080d0fd6 0e4a
    adds r0,r1,r2    @ 080d0fd8 8818
    ldrb r0,[r0,#0x0]                        @ 080d0fda 0078
    lsrs r2,r0,#0x5    @ 080d0fdc 4209
    ldr r3, DWORD_080d1014                   @ 080d0fde 0d4b
    adds r1,r1,r3    @ 080d0fe0 c918
    movs r3,#0x1f    @ 080d0fe2 1f23
    adds r0,r3,#0x0    @ 080d0fe4 181c
    ldrb r1,[r1,#0x0]                        @ 080d0fe6 0978
    ands r0,r1    @ 080d0fe8 0840
    lsls r0,r0,#0x3    @ 080d0fea c000
    orrs r0,r2    @ 080d0fec 1043
    cmp r0,#0x0                              @ 080d0fee 0028
    beq LAB_080d1018                         @ 080d0ff0 12d0
    ldr r7, DWORD_080d1000                   @ 080d0ff2 034f
    ldr r1, DWORD_080d1008                   @ 080d0ff4 0449
    adds r0,r7,r1    @ 080d0ff6 7818
    ldrh r0,[r0,#0x0]                        @ 080d0ff8 0088
    lsls r1,r0,#0x13    @ 080d0ffa c104
    lsrs r1,r1,#0x18    @ 080d0ffc 090e
    b LAB_080d1032                           @ 080d0ffe 18e0
DWORD_080d1000:
    .word  0x02020160                     @ 080d1000 60010202
DWORD_080d1004:
    .word  0x00002f57                     @ 080d1004 572f0000
DWORD_080d1008:
    .word  0x00002f58                     @ 080d1008 582f0000
DWORD_080d100c:
    .word  0x000002be                     @ 080d100c be020000
DWORD_080d1010:
    .word  0x00002f53                     @ 080d1010 532f0000
DWORD_080d1014:
    .word  0x00002f54                     @ 080d1014 542f0000
LAB_080d1018:
    ldr r2, DWORD_080d1080                   @ 080d1018 194a
    ldr r7, DWORD_080d1084                   @ 080d101a 1a4f
    adds r0,r2,r7    @ 080d101c d019
    ldrb r0,[r0,#0x0]                        @ 080d101e 0078
    lsrs r2,r0,#0x5    @ 080d1020 4209
    ldr r1, DWORD_080d1080                   @ 080d1022 1749
    adds r7,#0x1    @ 080d1024 0137
    adds r0,r1,r7    @ 080d1026 c819
    adds r1,r3,#0x0    @ 080d1028 191c
    ldrb r0,[r0,#0x0]                        @ 080d102a 0078
    ands r1,r0    @ 080d102c 0140
    lsls r1,r1,#0x3    @ 080d102e c900
    orrs r1,r2    @ 080d1030 1143
LAB_080d1032:
    adds r0,r5,#0x0    @ 080d1032 281c
    bl __divsi3                              @ 080d1034 3df0e6fa
    adds r1,r0,#0x0    @ 080d1038 011c
    cmp r1,#0x0                              @ 080d103a 0029
    bge LAB_080d1040                         @ 080d103c 00da
    adds r0,r1,#0x7    @ 080d103e c81d
LAB_080d1040:
    asrs r0,r0,#0x3    @ 080d1040 c010
    lsls r0,r0,#0x3    @ 080d1042 c000
    subs r0,r1,r0    @ 080d1044 081a
    movs r1,#0x8    @ 080d1046 0821
    subs r1,r1,r0    @ 080d1048 091a
    adds r0,r1,#0x0    @ 080d104a 081c
    cmp r1,#0x0                              @ 080d104c 0029
    bge LAB_080d1052                         @ 080d104e 00da
    adds r0,r1,#0x3    @ 080d1050 c81c
LAB_080d1052:
    asrs r0,r0,#0x2    @ 080d1052 8010
    lsls r0,r0,#0x2    @ 080d1054 8000
    subs r0,r1,r0    @ 080d1056 081a
    lsls r0,r0,#0x5    @ 080d1058 4001
    adds r0,r4,r0    @ 080d105a 2018
    movs r1,#0x80    @ 080d105c 8021
    lsls r1,r1,#0x6    @ 080d105e 8901
    orrs r0,r1    @ 080d1060 0843
    lsls r0,r0,#0x10    @ 080d1062 0004
    lsrs r2,r0,#0x10    @ 080d1064 020c
    adds r0,r6,#0x0    @ 080d1066 301c
    movs r1,#0x0    @ 080d1068 0021
    bl write_oam_entry_from_packed_args      @ 080d106a 25f07ff8
LAB_080d106e:
    add sp,#0x10                             @ 080d106e 04b0
    pop {r3,r4,r5}                           @ 080d1070 38bc
    .hword 0x4698    @ 080d1072 9846
    .hword 0x46a1    @ 080d1074 a146
    .hword 0x46aa    @ 080d1076 aa46
    pop {r4,r5,r6,r7}                        @ 080d1078 f0bc
    pop {r0}                                 @ 080d107a 01bc
    bx r0                                    @ 080d107c 0047
    .zero  0x2
DWORD_080d1080:
    .word  0x02020160                     @ 080d1080 60010202
DWORD_080d1084:
    .word  0x00002f57                     @ 080d1084 572f0000

@ Synthesizes type_combined from gDuelCtx+0x2f53/0x2f54 (bits[7:5]<<3 | bits[4:0]&0x1f); if type_combined==0 exits (null path). Otherwise reads gDuelCtx+0x2f58 (card zone type [0..5]) and branches into 4 OAM write paths (type 0->LAB_080d117e, 1->LAB_080d120c, 2->LAB_080d122c, 3->LAB_080d1250). Each path reads gPrng+0x83*4 halfword bits[7:4] % 3 or & 1 to generate anim frame offset, then calls write_oam_entry_from_packed_args. LAB_080d1280 reads gDuelCtx+0x2f56 halfword bits[12:5] as zone slot encoding for OAM Y coordinate (read-only). Called by render_zone_card_anim_dual_pass (0x080d1b2c) as first render pass. Side effects: OAM writes via write_oam_entry_from_packed_args + write_oam_entry_with_slot_check. Constants: gDuelCtx=0x02020160, status_offset=0x2f53, low_offset=0x2f54, word_offset=0x2f58, slot_encode_offset=0x2f56 (read-only), gPrng anim_seed_offset=0x83*4=0x20c, oam_size=0x80.
render_zone_card_anim_oam_frame:
    push {r4,r5,r6,r7,lr}                    @ 080d1088 f0b5
    .hword 0x4657    @ 080d108a 5746
    .hword 0x464e    @ 080d108c 4e46
    .hword 0x4645    @ 080d108e 4546
    push {r5,r6,r7}                          @ 080d1090 e0b4
    sub sp,#0x8                              @ 080d1092 82b0
    ldr r1, DWORD_080d10c4                   @ 080d1094 0b49
    ldr r2, DWORD_080d10c8                   @ 080d1096 0c4a
    adds r0,r1,r2    @ 080d1098 8818
    ldrb r0,[r0,#0x0]                        @ 080d109a 0078
    lsrs r3,r0,#0x5    @ 080d109c 4309
    ldr r0, DWORD_080d10cc                   @ 080d109e 0b48
    adds r2,r1,r0    @ 080d10a0 0a18
    movs r5,#0x1f    @ 080d10a2 1f25
    adds r0,r5,#0x0    @ 080d10a4 281c
    ldrb r2,[r2,#0x0]                        @ 080d10a6 1278
    ands r0,r2    @ 080d10a8 1040
    lsls r0,r0,#0x3    @ 080d10aa c000
    orrs r0,r3    @ 080d10ac 1843
    adds r4,r1,#0x0    @ 080d10ae 0c1c
    cmp r0,#0x0                              @ 080d10b0 0028
    beq LAB_080d10d4                         @ 080d10b2 0fd0
    ldr r1, DWORD_080d10d0                   @ 080d10b4 0649
    adds r0,r4,r1    @ 080d10b6 6018
    ldrh r0,[r0,#0x0]                        @ 080d10b8 0088
    lsls r0,r0,#0x13    @ 080d10ba c004
    lsrs r0,r0,#0x18    @ 080d10bc 000e
    cmp r0,#0x5                              @ 080d10be 0528
    ble LAB_080d10ee                         @ 080d10c0 15dd
    b LAB_080d1148                           @ 080d10c2 41e0
DWORD_080d10c4:
    .word  0x02020160                     @ 080d10c4 60010202
DWORD_080d10c8:
    .word  0x00002f53                     @ 080d10c8 532f0000
DWORD_080d10cc:
    .word  0x00002f54                     @ 080d10cc 542f0000
DWORD_080d10d0:
    .word  0x00002f58                     @ 080d10d0 582f0000
LAB_080d10d4:
    ldr r2, DWORD_080d1118                   @ 080d10d4 104a
    adds r0,r4,r2    @ 080d10d6 a018
    ldrb r0,[r0,#0x0]                        @ 080d10d8 0078
    lsrs r2,r0,#0x5    @ 080d10da 4209
    ldr r3, DWORD_080d111c                   @ 080d10dc 0f4b
    adds r1,r4,r3    @ 080d10de e118
    adds r0,r5,#0x0    @ 080d10e0 281c
    ldrb r1,[r1,#0x0]                        @ 080d10e2 0978
    ands r0,r1    @ 080d10e4 0840
    lsls r0,r0,#0x3    @ 080d10e6 c000
    orrs r0,r2    @ 080d10e8 1043
    cmp r0,#0x5                              @ 080d10ea 0528
    bgt LAB_080d1148                         @ 080d10ec 2cdc
LAB_080d10ee:
    ldr r1, DWORD_080d1120                   @ 080d10ee 0c49
    adds r0,r4,r1    @ 080d10f0 6018
    ldrb r0,[r0,#0x0]                        @ 080d10f2 0078
    lsrs r2,r0,#0x5    @ 080d10f4 4209
    ldr r3, DWORD_080d1124                   @ 080d10f6 0b4b
    adds r1,r4,r3    @ 080d10f8 e118
    movs r3,#0x1f    @ 080d10fa 1f23
    adds r0,r3,#0x0    @ 080d10fc 181c
    ldrb r1,[r1,#0x0]                        @ 080d10fe 0978
    ands r0,r1    @ 080d1100 0840
    lsls r0,r0,#0x3    @ 080d1102 c000
    orrs r0,r2    @ 080d1104 1043
    cmp r0,#0x0                              @ 080d1106 0028
    beq LAB_080d1128                         @ 080d1108 0ed0
    ldr r1, DWORD_080d111c                   @ 080d110a 0449
    adds r0,r4,r1    @ 080d110c 6018
    ldrh r0,[r0,#0x0]                        @ 080d110e 0088
    lsls r0,r0,#0x13    @ 080d1110 c004
    lsrs r3,r0,#0x18    @ 080d1112 030e
    b LAB_080d114a                           @ 080d1114 19e0
    .zero  0x2
DWORD_080d1118:
    .word  0x00002f57                     @ 080d1118 572f0000
DWORD_080d111c:
    .word  0x00002f58                     @ 080d111c 582f0000
DWORD_080d1120:
    .word  0x00002f53                     @ 080d1120 532f0000
DWORD_080d1124:
    .word  0x00002f54                     @ 080d1124 542f0000
LAB_080d1128:
    ldr r2, DWORD_080d1140                   @ 080d1128 054a
    adds r0,r4,r2    @ 080d112a a018
    ldrb r0,[r0,#0x0]                        @ 080d112c 0078
    lsrs r2,r0,#0x5    @ 080d112e 4209
    ldr r0, DWORD_080d1144                   @ 080d1130 0448
    adds r1,r4,r0    @ 080d1132 2118
    adds r0,r3,#0x0    @ 080d1134 181c
    ldrb r1,[r1,#0x0]                        @ 080d1136 0978
    ands r0,r1    @ 080d1138 0840
    lsls r3,r0,#0x3    @ 080d113a c300
    orrs r3,r2    @ 080d113c 1343
    b LAB_080d114a                           @ 080d113e 04e0
DWORD_080d1140:
    .word  0x00002f57                     @ 080d1140 572f0000
DWORD_080d1144:
    .word  0x00002f58                     @ 080d1144 582f0000
LAB_080d1148:
    movs r3,#0x5    @ 080d1148 0523
LAB_080d114a:
    movs r7,#0x0    @ 080d114a 0027
    movs r1,#0x0    @ 080d114c 0021
    .hword 0x468a    @ 080d114e 8a46
    movs r2,#0xa0    @ 080d1150 a022
    lsls r2,r2,#0x1    @ 080d1152 5200
    str r2,[sp,#0x4]                         @ 080d1154 0192
    str r2,[sp,#0x0]                         @ 080d1156 0092
    ldr r0, DWORD_080d1170                   @ 080d1158 0548
    adds r2,r4,r0    @ 080d115a 2218
    ldrh r1,[r2,#0x0]                        @ 080d115c 1188
    lsls r0,r1,#0x13    @ 080d115e c804
    lsrs r0,r0,#0x18    @ 080d1160 000e
    cmp r0,#0x1                              @ 080d1162 0128
    beq LAB_080d120c                         @ 080d1164 52d0
    cmp r0,#0x1                              @ 080d1166 0128
    bgt LAB_080d1174                         @ 080d1168 04dc
    cmp r0,#0x0                              @ 080d116a 0028
    beq LAB_080d117e                         @ 080d116c 07d0
    b LAB_080d1280                           @ 080d116e 87e0
DWORD_080d1170:
    .word  0x00002f54                     @ 080d1170 542f0000
LAB_080d1174:
    cmp r0,#0x2                              @ 080d1174 0228
    beq LAB_080d122c                         @ 080d1176 59d0
    cmp r0,#0x3                              @ 080d1178 0328
    beq LAB_080d1250                         @ 080d117a 69d0
    b LAB_080d1280                           @ 080d117c 80e0
LAB_080d117e:
    ldr r1, DWORD_080d11a8                   @ 080d117e 0a49
    adds r0,r4,r1    @ 080d1180 6018
    ldrb r0,[r0,#0x0]                        @ 080d1182 0078
    lsrs r1,r0,#0x5    @ 080d1184 4109
    movs r0,#0x1f    @ 080d1186 1f20
    ldrb r2,[r2,#0x0]                        @ 080d1188 1278
    ands r0,r2    @ 080d118a 1040
    lsls r0,r0,#0x3    @ 080d118c c000
    orrs r0,r1    @ 080d118e 0843
    cmp r0,#0x0                              @ 080d1190 0028
    beq LAB_080d11b2                         @ 080d1192 0ed0
    ldr r2, DWORD_080d11ac                   @ 080d1194 054a
    adds r0,r4,r2    @ 080d1196 a018
    ldrh r0,[r0,#0x0]                        @ 080d1198 0088
    lsls r1,r0,#0x13    @ 080d119a c104
    lsrs r0,r1,#0x18    @ 080d119c 080e
    cmp r0,#0x5                              @ 080d119e 0528
    bhi LAB_080d11b0                         @ 080d11a0 06d8
    adds r3,r0,#0x0    @ 080d11a2 031c
    b LAB_080d11b2                           @ 080d11a4 05e0
    .zero  0x2
DWORD_080d11a8:
    .word  0x00002f53                     @ 080d11a8 532f0000
DWORD_080d11ac:
    .word  0x00002f58                     @ 080d11ac 582f0000
LAB_080d11b0:
    movs r3,#0x5    @ 080d11b0 0523
LAB_080d11b2:
    lsls r1,r3,#0x1    @ 080d11b2 5900
    movs r0,#0xc8    @ 080d11b4 c820
    bl __divsi3                              @ 080d11b6 3df025fa
    ldr r1, DWORD_080d1200                   @ 080d11ba 1149
    ldr r3, DWORD_080d1204                   @ 080d11bc 114b
    adds r1,r1,r3    @ 080d11be c918
    ldrh r1,[r1,#0x0]                        @ 080d11c0 0988
    lsls r1,r1,#0x13    @ 080d11c2 c904
    lsrs r1,r1,#0x18    @ 080d11c4 090e
    lsls r1,r1,#0x1    @ 080d11c6 4900
    adds r1,#0x1    @ 080d11c8 0131
    adds r4,r0,#0x0    @ 080d11ca 041c
    muls r4,r1    @ 080d11cc 4c43
    adds r4,#0x18    @ 080d11ce 1834
    movs r0,#0x98    @ 080d11d0 9820
    lsls r0,r0,#0xf    @ 080d11d2 c003
    orrs r4,r0    @ 080d11d4 0443
    ldr r0, DWORD_080d1208                   @ 080d11d6 0c48
    movs r1,#0x83    @ 080d11d8 8321
    lsls r1,r1,#0x2    @ 080d11da 8900
    adds r0,r0,r1    @ 080d11dc 4018
    ldrh r0,[r0,#0x0]                        @ 080d11de 0088
    lsrs r0,r0,#0x4    @ 080d11e0 0009
    movs r1,#0x3    @ 080d11e2 0321
    bl __umodsi3                             @ 080d11e4 3df036fb
    adds r2,r0,#0x0    @ 080d11e8 021c
    lsls r2,r2,#0xc    @ 080d11ea 1203
    movs r0,#0x2    @ 080d11ec 0220
    orrs r2,r0    @ 080d11ee 0243
    lsls r2,r2,#0x10    @ 080d11f0 1204
    lsrs r2,r2,#0x10    @ 080d11f2 120c
    adds r0,r4,#0x0    @ 080d11f4 201c
    movs r1,#0x80    @ 080d11f6 8021
    bl write_oam_entry_from_packed_args      @ 080d11f8 24f0b8ff
    b LAB_080d1280                           @ 080d11fc 40e0
    .zero  0x2
DWORD_080d1200:
    .word  0x02020160                     @ 080d1200 60010202
DWORD_080d1204:
    .word  0x00002f56                     @ 080d1204 562f0000
DWORD_080d1208:
    .word  gPrng                          @ 080d1208 40000003
LAB_080d120c:
    ldr r0, DWORD_080d1224                   @ 080d120c 0548
    movs r2,#0x83    @ 080d120e 8322
    lsls r2,r2,#0x2    @ 080d1210 9200
    adds r0,r0,r2    @ 080d1212 8018
    ldrh r0,[r0,#0x0]                        @ 080d1214 0088
    lsrs r7,r0,#0x4    @ 080d1216 0709
    movs r0,#0x1    @ 080d1218 0120
    ands r7,r0    @ 080d121a 0740
    ldr r3, DWORD_080d1228                   @ 080d121c 024b
    str r3,[sp,#0x0]                         @ 080d121e 0093
    b LAB_080d1280                           @ 080d1220 2ee0
    .zero  0x2
DWORD_080d1224:
    .word  gPrng                          @ 080d1224 40000003
DWORD_080d1228:
    .word  0x00000141                     @ 080d1228 41010000
LAB_080d122c:
    ldr r0, DWORD_080d124c                   @ 080d122c 0748
    movs r1,#0x83    @ 080d122e 8321
    lsls r1,r1,#0x2    @ 080d1230 8900
    adds r0,r0,r1    @ 080d1232 4018
    ldrh r0,[r0,#0x0]                        @ 080d1234 0088
    lsrs r0,r0,#0x4    @ 080d1236 0009
    .hword 0x4682    @ 080d1238 8246
    movs r0,#0x1    @ 080d123a 0120
    .hword 0x4652    @ 080d123c 5246
    ands r2,r0    @ 080d123e 0240
    .hword 0x4692    @ 080d1240 9246
    ldr r3,[sp,#0x4]                         @ 080d1242 019b
    adds r3,#0x1    @ 080d1244 0133
    str r3,[sp,#0x4]                         @ 080d1246 0193
    b LAB_080d1280                           @ 080d1248 1ae0
    .zero  0x2
DWORD_080d124c:
    .word  gPrng                          @ 080d124c 40000003
LAB_080d1250:
    ldr r4, DWORD_080d1354                   @ 080d1250 404c
    movs r5,#0x81    @ 080d1252 8125
    lsls r5,r5,#0x7    @ 080d1254 ed01
    ldr r0, DWORD_080d1358                   @ 080d1256 4048
    movs r1,#0x83    @ 080d1258 8321
    lsls r1,r1,#0x2    @ 080d125a 8900
    adds r0,r0,r1    @ 080d125c 4018
    ldrh r0,[r0,#0x0]                        @ 080d125e 0088
    lsrs r0,r0,#0x4    @ 080d1260 0009
    movs r1,#0x3    @ 080d1262 0321
    bl __umodsi3                             @ 080d1264 3df0f6fa
    adds r2,r0,#0x0    @ 080d1268 021c
    lsls r2,r2,#0xc    @ 080d126a 1203
    movs r3,#0x9e    @ 080d126c 9e23
    lsls r3,r3,#0x2    @ 080d126e 9b00
    adds r0,r3,#0x0    @ 080d1270 181c
    orrs r2,r0    @ 080d1272 0243
    lsls r2,r2,#0x10    @ 080d1274 1204
    lsrs r2,r2,#0x10    @ 080d1276 120c
    adds r0,r4,#0x0    @ 080d1278 201c
    adds r1,r5,#0x0    @ 080d127a 291c
    bl write_oam_entry_from_packed_args      @ 080d127c 24f076ff
LAB_080d1280:
    ldr r6, DWORD_080d135c                   @ 080d1280 364e
    ldr r0, DWORD_080d1360                   @ 080d1282 3748
    adds r0,r0,r6    @ 080d1284 8019
    .hword 0x4680    @ 080d1286 8046
    ldrb r1,[r0,#0x0]                        @ 080d1288 0178
    lsrs r0,r1,#0x5    @ 080d128a 4809
    ldr r2, DWORD_080d1364                   @ 080d128c 354a
    adds r2,r2,r6    @ 080d128e 9219
    .hword 0x4691    @ 080d1290 9146
    movs r4,#0x1f    @ 080d1292 1f24
    adds r1,r4,#0x0    @ 080d1294 211c
    ldrb r3,[r2,#0x0]                        @ 080d1296 1378
    ands r1,r3    @ 080d1298 1940
    lsls r1,r1,#0x3    @ 080d129a c900
    orrs r1,r0    @ 080d129c 0143
    lsls r0,r1,#0x2    @ 080d129e 8800
    adds r0,r0,r1    @ 080d12a0 4018
    lsls r0,r0,#0x5    @ 080d12a2 4001
    movs r1,#0x6    @ 080d12a4 0621
    bl __divsi3                              @ 080d12a6 3df0adf9
    adds r1,r7,#0x0    @ 080d12aa 391c
    subs r1,#0x2c    @ 080d12ac 2c39
    subs r0,r0,r1    @ 080d12ae 401a
    movs r5,#0x20    @ 080d12b0 2025
    adds r5,#0x14    @ 080d12b2 1435
    lsls r5,r5,#0x10    @ 080d12b4 2d04
    orrs r0,r5    @ 080d12b6 2843
    movs r1,#0x0    @ 080d12b8 0021
    ldr r2,[sp,#0x0]                         @ 080d12ba 009a
    bl write_oam_entry_from_packed_args      @ 080d12bc 24f056ff
    .hword 0x4641    @ 080d12c0 4146
    ldrb r1,[r1,#0x0]                        @ 080d12c2 0978
    lsrs r0,r1,#0x5    @ 080d12c4 4809
    .hword 0x464a    @ 080d12c6 4a46
    ldrb r2,[r2,#0x0]                        @ 080d12c8 1278
    ands r4,r2    @ 080d12ca 1440
    lsls r4,r4,#0x3    @ 080d12cc e400
    orrs r4,r0    @ 080d12ce 0443
    lsls r0,r4,#0x2    @ 080d12d0 a000
    adds r0,r0,r4    @ 080d12d2 0019
    lsls r0,r0,#0x5    @ 080d12d4 4001
    movs r1,#0x6    @ 080d12d6 0621
    bl __divsi3                              @ 080d12d8 3df094f9
    adds r1,r7,#0x0    @ 080d12dc 391c
    adds r1,#0x44    @ 080d12de 4431
    adds r0,r0,r1    @ 080d12e0 4018
    orrs r0,r5    @ 080d12e2 2843
    movs r5,#0x80    @ 080d12e4 8025
    lsls r5,r5,#0x5    @ 080d12e6 6d01
    movs r1,#0x0    @ 080d12e8 0021
    ldr r2,[sp,#0x0]                         @ 080d12ea 009a
    adds r3,r5,#0x0    @ 080d12ec 2b1c
    bl write_oam_entry_with_slot_check       @ 080d12ee 25f081fa
    ldr r3, DWORD_080d1368                   @ 080d12f2 1d4b
    adds r6,r6,r3    @ 080d12f4 f618
    ldrh r0,[r6,#0x0]                        @ 080d12f6 3088
    lsls r1,r0,#0x13    @ 080d12f8 c104
    lsrs r1,r1,#0x18    @ 080d12fa 090e
    lsls r0,r1,#0x2    @ 080d12fc 8800
    adds r0,r0,r1    @ 080d12fe 4018
    lsls r0,r0,#0x5    @ 080d1300 4001
    movs r1,#0x7    @ 080d1302 0721
    bl __divsi3                              @ 080d1304 3df07ef9
    .hword 0x4651    @ 080d1308 5146
    subs r1,#0x2c    @ 080d130a 2c39
    subs r0,r0,r1    @ 080d130c 401a
    movs r4,#0x20    @ 080d130e 2024
    adds r4,#0x4    @ 080d1310 0434
    lsls r4,r4,#0x10    @ 080d1312 2404
    orrs r0,r4    @ 080d1314 2043
    movs r1,#0x0    @ 080d1316 0021
    ldr r2,[sp,#0x4]                         @ 080d1318 019a
    bl write_oam_entry_from_packed_args      @ 080d131a 24f027ff
    ldrh r6,[r6,#0x0]                        @ 080d131e 3688
    lsls r1,r6,#0x13    @ 080d1320 f104
    lsrs r1,r1,#0x18    @ 080d1322 090e
    lsls r0,r1,#0x2    @ 080d1324 8800
    adds r0,r0,r1    @ 080d1326 4018
    lsls r0,r0,#0x5    @ 080d1328 4001
    movs r1,#0x7    @ 080d132a 0721
    bl __divsi3                              @ 080d132c 3df06af9
    .hword 0x4651    @ 080d1330 5146
    adds r1,#0x44    @ 080d1332 4431
    adds r0,r0,r1    @ 080d1334 4018
    orrs r0,r4    @ 080d1336 2043
    movs r1,#0x0    @ 080d1338 0021
    ldr r2,[sp,#0x4]                         @ 080d133a 019a
    adds r3,r5,#0x0    @ 080d133c 2b1c
    bl write_oam_entry_with_slot_check       @ 080d133e 25f059fa
    add sp,#0x8                              @ 080d1342 02b0
    pop {r3,r4,r5}                           @ 080d1344 38bc
    .hword 0x4698    @ 080d1346 9846
    .hword 0x46a1    @ 080d1348 a146
    .hword 0x46aa    @ 080d134a aa46
    pop {r4,r5,r6,r7}                        @ 080d134c f0bc
    pop {r0}                                 @ 080d134e 01bc
    bx r0                                    @ 080d1350 0047
    .zero  0x2
DWORD_080d1354:
    .word  0x0080007c                     @ 080d1354 7c008000
DWORD_080d1358:
    .word  gPrng                          @ 080d1358 40000003
DWORD_080d135c:
    .word  0x02020160                     @ 080d135c 60010202
DWORD_080d1360:
    .word  0x00002f53                     @ 080d1360 532f0000
DWORD_080d1364:
    .word  0x00002f54                     @ 080d1364 542f0000
DWORD_080d1368:
    .word  0x00002f52                     @ 080d1368 522f0000

@ Base-r9 variant of render_zone_card_anim_oam_frame: prologue loads gDuelCtx (DWORD_080d13ac=0x02020160) internally into r9 via '.hword 0x4689=mov r9,r1'; does not consume APCS r1 parameter. All gDuelCtx field reads use 'add r0,r9' with fixed offsets (0x2f53/0x2f54/0x2f57/0x2f58). Also calls check_zone_anim_id_in_table (0x080d07cc) and dispatch_effect_ctx_slot_by_zone_type (0x08094398). Void, no APCS params. Side effects: OAM writes via write_oam_entry_from_packed_args; [gDuelCtx+0x2e42+slot*2] := 0 via strh at 0x080d157c (slot=modsi3(zone_slot,5)). Constants: gDuelCtx=0x02020160, base_offsets={0x2f53,0x2f54,0x2f57,0x2f58}, r9=gDuelCtx (internal load).
render_zone_card_anim_oam_with_base:
    push {r4,r5,r6,r7,lr}                    @ 080d136c f0b5
    .hword 0x4657    @ 080d136e 5746
    .hword 0x464e    @ 080d1370 4e46
    .hword 0x4645    @ 080d1372 4546
    push {r5,r6,r7}                          @ 080d1374 e0b4
    sub sp,#0x38                             @ 080d1376 8eb0
    movs r6,#0x20    @ 080d1378 2026
    ldr r1, DWORD_080d13ac                   @ 080d137a 0c49
    ldr r2, DWORD_080d13b0                   @ 080d137c 0c4a
    adds r0,r1,r2    @ 080d137e 8818
    ldrb r0,[r0,#0x0]                        @ 080d1380 0078
    lsrs r3,r0,#0x5    @ 080d1382 4309
    ldr r4, DWORD_080d13b4                   @ 080d1384 0b4c
    adds r2,r1,r4    @ 080d1386 0a19
    movs r4,#0x1f    @ 080d1388 1f24
    adds r0,r4,#0x0    @ 080d138a 201c
    ldrb r2,[r2,#0x0]                        @ 080d138c 1278
    ands r0,r2    @ 080d138e 1040
    lsls r0,r0,#0x3    @ 080d1390 c000
    orrs r0,r3    @ 080d1392 1843
    .hword 0x4689    @ 080d1394 8946
    cmp r0,#0x0                              @ 080d1396 0028
    beq LAB_080d13bc                         @ 080d1398 10d0
    ldr r0, DWORD_080d13b8                   @ 080d139a 0748
    add r0,r9                                @ 080d139c 4844
    ldrh r0,[r0,#0x0]                        @ 080d139e 0088
    lsls r0,r0,#0x13    @ 080d13a0 c004
    lsrs r0,r0,#0x18    @ 080d13a2 000e
    cmp r0,#0x5                              @ 080d13a4 0528
    ble LAB_080d13d6                         @ 080d13a6 16dd
    b LAB_080d1430                           @ 080d13a8 42e0
    .zero  0x2
DWORD_080d13ac:
    .word  0x02020160                     @ 080d13ac 60010202
DWORD_080d13b0:
    .word  0x00002f53                     @ 080d13b0 532f0000
DWORD_080d13b4:
    .word  0x00002f54                     @ 080d13b4 542f0000
DWORD_080d13b8:
    .word  0x00002f58                     @ 080d13b8 582f0000
LAB_080d13bc:
    ldr r0, DWORD_080d1400                   @ 080d13bc 1048
    add r0,r9                                @ 080d13be 4844
    ldrb r0,[r0,#0x0]                        @ 080d13c0 0078
    lsrs r2,r0,#0x5    @ 080d13c2 4209
    ldr r1, DWORD_080d1404                   @ 080d13c4 0f49
    add r1,r9                                @ 080d13c6 4944
    adds r0,r4,#0x0    @ 080d13c8 201c
    ldrb r1,[r1,#0x0]                        @ 080d13ca 0978
    ands r0,r1    @ 080d13cc 0840
    lsls r0,r0,#0x3    @ 080d13ce c000
    orrs r0,r2    @ 080d13d0 1043
    cmp r0,#0x5                              @ 080d13d2 0528
    bgt LAB_080d1430                         @ 080d13d4 2cdc
LAB_080d13d6:
    ldr r0, DWORD_080d1408                   @ 080d13d6 0c48
    add r0,r9                                @ 080d13d8 4844
    ldrb r0,[r0,#0x0]                        @ 080d13da 0078
    lsrs r2,r0,#0x5    @ 080d13dc 4209
    ldr r1, DWORD_080d140c                   @ 080d13de 0b49
    add r1,r9                                @ 080d13e0 4944
    movs r3,#0x1f    @ 080d13e2 1f23
    adds r0,r3,#0x0    @ 080d13e4 181c
    ldrb r1,[r1,#0x0]                        @ 080d13e6 0978
    ands r0,r1    @ 080d13e8 0840
    lsls r0,r0,#0x3    @ 080d13ea c000
    orrs r0,r2    @ 080d13ec 1043
    cmp r0,#0x0                              @ 080d13ee 0028
    beq LAB_080d1410                         @ 080d13f0 0ed0
    ldr r0, DWORD_080d1404                   @ 080d13f2 0448
    add r0,r9                                @ 080d13f4 4844
    ldrh r0,[r0,#0x0]                        @ 080d13f6 0088
    lsls r0,r0,#0x13    @ 080d13f8 c004
    lsrs r0,r0,#0x18    @ 080d13fa 000e
    b LAB_080d1432                           @ 080d13fc 19e0
    .zero  0x2
DWORD_080d1400:
    .word  0x00002f57                     @ 080d1400 572f0000
DWORD_080d1404:
    .word  0x00002f58                     @ 080d1404 582f0000
DWORD_080d1408:
    .word  0x00002f53                     @ 080d1408 532f0000
DWORD_080d140c:
    .word  0x00002f54                     @ 080d140c 542f0000
LAB_080d1410:
    ldr r0, DWORD_080d1428                   @ 080d1410 0548
    add r0,r9                                @ 080d1412 4844
    ldrb r0,[r0,#0x0]                        @ 080d1414 0078
    lsrs r2,r0,#0x5    @ 080d1416 4209
    ldr r1, DWORD_080d142c                   @ 080d1418 0449
    add r1,r9                                @ 080d141a 4944
    adds r0,r3,#0x0    @ 080d141c 181c
    ldrb r1,[r1,#0x0]                        @ 080d141e 0978
    ands r0,r1    @ 080d1420 0840
    lsls r0,r0,#0x3    @ 080d1422 c000
    orrs r0,r2    @ 080d1424 1043
    b LAB_080d1432                           @ 080d1426 04e0
DWORD_080d1428:
    .word  0x00002f57                     @ 080d1428 572f0000
DWORD_080d142c:
    .word  0x00002f58                     @ 080d142c 582f0000
LAB_080d1430:
    movs r0,#0x5    @ 080d1430 0520
LAB_080d1432:
    str r0,[sp,#0x20]                        @ 080d1432 0890
    ldr r0, DWORD_080d1528                   @ 080d1434 3c48
    add r0,r9                                @ 080d1436 4844
    ldr r4,[r0,#0x0]                         @ 080d1438 0468
    lsls r4,r4,#0xb    @ 080d143a e402
    lsrs r0,r4,#0x18    @ 080d143c 200e
    movs r1,#0x5    @ 080d143e 0521
    bl __umodsi3                             @ 080d1440 3df008fa
    lsls r0,r0,#0x10    @ 080d1444 0004
    lsrs r0,r0,#0x10    @ 080d1446 000c
    str r0,[sp,#0x24]                        @ 080d1448 0990
    lsrs r4,r4,#0x18    @ 080d144a 240e
    ldr r0, DWORD_080d152c                   @ 080d144c 3748
    add r0,r9                                @ 080d144e 4844
    ldrh r0,[r0,#0x0]                        @ 080d1450 0088
    lsls r0,r0,#0x13    @ 080d1452 c004
    lsrs r0,r0,#0x18    @ 080d1454 000e
    adds r4,r4,r0    @ 080d1456 2418
    .hword 0x46a0    @ 080d1458 a046
    ldr r1, DWORD_080d1530                   @ 080d145a 3549
    .hword 0x4668    @ 080d145c 6846
    movs r2,#0x10    @ 080d145e 1022
    bl memcpy                                @ 080d1460 3df07cfa
    add r4,sp,#0x10                          @ 080d1464 04ac
    ldr r1, DWORD_080d1534                   @ 080d1466 3349
    adds r0,r4,#0x0    @ 080d1468 201c
    movs r2,#0xe    @ 080d146a 0e22
    bl memcpy                                @ 080d146c 3df076fa
    movs r1,#0x0    @ 080d1470 0021
    .hword 0x468a    @ 080d1472 8a46
    .hword 0x46a1    @ 080d1474 a146
    lsls r7,r6,#0x10    @ 080d1476 3704
    adds r4,r6,#0x0    @ 080d1478 341c
    adds r4,#0x10    @ 080d147a 1034
    .hword 0x466d    @ 080d147c 6d46
    movs r6,#0x0    @ 080d147e 0026
LAB_080d1480:
    adds r0,r6,#0x0    @ 080d1480 301c
    movs r1,#0x7    @ 080d1482 0721
    bl __divsi3                              @ 080d1484 3df0bef8
    adds r0,#0x34    @ 080d1488 3430
    orrs r0,r7    @ 080d148a 3843
    .hword 0x4652    @ 080d148c 5246
    lsls r1,r2,#0x1    @ 080d148e 5100
    ldrh r3,[r5,#0x0]                        @ 080d1490 2b88
    lsls r2,r3,#0xc    @ 080d1492 1a03
    movs r3,#0xd0    @ 080d1494 d023
    lsls r3,r3,#0x1    @ 080d1496 5b00
    adds r1,r1,r3    @ 080d1498 c918
    orrs r2,r1    @ 080d149a 0a43
    lsls r2,r2,#0x10    @ 080d149c 1204
    lsrs r2,r2,#0x10    @ 080d149e 120c
    movs r1,#0x40    @ 080d14a0 4021
    bl write_oam_entry_from_packed_args      @ 080d14a2 24f063fe
    adds r5,#0x2    @ 080d14a6 0235
    adds r6,#0xa0    @ 080d14a8 a036
    movs r0,#0x1    @ 080d14aa 0120
    add r10,r0                               @ 080d14ac 8244
    .hword 0x4651    @ 080d14ae 5146
    cmp r1,#0x7                              @ 080d14b0 0729
    ble LAB_080d1480                         @ 080d14b2 e5dd
    adds r6,r4,#0x0    @ 080d14b4 261c
    movs r2,#0x0    @ 080d14b6 0022
    .hword 0x4692    @ 080d14b8 9246
    .hword 0x464c    @ 080d14ba 4c46
    movs r5,#0x0    @ 080d14bc 0025
LAB_080d14be:
    adds r0,r5,#0x0    @ 080d14be 281c
    movs r1,#0x6    @ 080d14c0 0621
    bl __divsi3                              @ 080d14c2 3df09ff8
    adds r0,#0x34    @ 080d14c6 3430
    lsls r1,r6,#0x10    @ 080d14c8 3104
    orrs r0,r1    @ 080d14ca 0843
    .hword 0x4653    @ 080d14cc 5346
    lsls r1,r3,#0x1    @ 080d14ce 5900
    ldrh r3,[r4,#0x0]                        @ 080d14d0 2388
    lsls r2,r3,#0xc    @ 080d14d2 1a03
    movs r3,#0xd8    @ 080d14d4 d823
    lsls r3,r3,#0x1    @ 080d14d6 5b00
    adds r1,r1,r3    @ 080d14d8 c918
    orrs r2,r1    @ 080d14da 0a43
    lsls r2,r2,#0x10    @ 080d14dc 1204
    lsrs r2,r2,#0x10    @ 080d14de 120c
    movs r1,#0x40    @ 080d14e0 4021
    bl write_oam_entry_from_packed_args      @ 080d14e2 24f043fe
    adds r4,#0x2    @ 080d14e6 0234
    adds r5,#0xa0    @ 080d14e8 a035
    movs r0,#0x1    @ 080d14ea 0120
    add r10,r0                               @ 080d14ec 8244
    .hword 0x4651    @ 080d14ee 5146
    cmp r1,#0x6                              @ 080d14f0 0629
    ble LAB_080d14be                         @ 080d14f2 e4dd
    ldr r3, DWORD_080d1538                   @ 080d14f4 104b
    ldr r2, DWORD_080d153c                   @ 080d14f6 114a
    adds r1,r3,r2    @ 080d14f8 9918
    movs r0,#0x4    @ 080d14fa 0420
    ldrb r1,[r1,#0x0]                        @ 080d14fc 0978
    ands r0,r1    @ 080d14fe 0840
    cmp r0,#0x0                              @ 080d1500 0028
    beq LAB_080d15c8                         @ 080d1502 61d0
    ldr r4, DWORD_080d1540                   @ 080d1504 0e4c
    adds r0,r3,r4    @ 080d1506 1819
    ldrb r0,[r0,#0x0]                        @ 080d1508 0078
    lsrs r2,r0,#0x5    @ 080d150a 4209
    ldr r0, DWORD_080d1528                   @ 080d150c 0648
    adds r1,r3,r0    @ 080d150e 1918
    movs r0,#0x1f    @ 080d1510 1f20
    ldrb r1,[r1,#0x0]                        @ 080d1512 0978
    ands r0,r1    @ 080d1514 0840
    lsls r0,r0,#0x3    @ 080d1516 c000
    orrs r0,r2    @ 080d1518 1043
    cmp r0,#0x0                              @ 080d151a 0028
    beq LAB_080d1544                         @ 080d151c 12d0
    .hword 0x4641    @ 080d151e 4146
    lsls r0,r1,#0x1    @ 080d1520 4800
    movs r2,#0xa8    @ 080d1522 a822
    lsls r2,r2,#0x6    @ 080d1524 9201
    b LAB_080d154c                           @ 080d1526 11e0
DWORD_080d1528:
    .word  0x00002f54                     @ 080d1528 542f0000
DWORD_080d152c:
    .word  0x00002f56                     @ 080d152c 562f0000
DWORD_080d1530:
    .word  0x09e493c0                     @ 080d1530 c093e409
DWORD_080d1534:
    .word  0x09e493d0                     @ 080d1534 d093e409
DWORD_080d1538:
    .word  0x02020160                     @ 080d1538 60010202
DWORD_080d153c:
    .word  0x00002f51                     @ 080d153c 512f0000
DWORD_080d1540:
    .word  0x00002f53                     @ 080d1540 532f0000
LAB_080d1544:
    .hword 0x4644    @ 080d1544 4446
    lsls r0,r4,#0x1    @ 080d1546 6000
    movs r2,#0xa0    @ 080d1548 a022
    lsls r2,r2,#0x6    @ 080d154a 9201
LAB_080d154c:
    adds r1,r3,r2    @ 080d154c 9918
    adds r0,r0,r1    @ 080d154e 4018
    ldrh r4,[r0,#0x0]                        @ 080d1550 0488
    ldr r6, DWORD_080d1610                   @ 080d1552 2f4e
    lsls r0,r4,#0x2    @ 080d1554 a000
    adds r0,r0,r4    @ 080d1556 0019
    lsls r0,r0,#0x3    @ 080d1558 c000
    adds r0,r0,r6    @ 080d155a 8019
    ldr r7,[r0,#0x0]                         @ 080d155c 0768
    .hword 0x4640    @ 080d155e 4046
    movs r1,#0x5    @ 080d1560 0521
    bl __modsi3                              @ 080d1562 3df09bf8
    adds r5,r0,#0x0    @ 080d1566 051c
    movs r3,#0x1    @ 080d1568 0123
    .hword 0x4699    @ 080d156a 9946
    .hword 0x4640    @ 080d156c 4046
    bl render_zone_slot_card_icon_tile       @ 080d156e 02f05ff9
    lsls r0,r5,#0x1    @ 080d1572 6800
    ldr r2, DWORD_080d1614                   @ 080d1574 274a
    adds r1,r6,r2    @ 080d1576 b118
    adds r0,r0,r1    @ 080d1578 4018
    movs r1,#0x0    @ 080d157a 0021
    strh r1,[r0,#0x0]                        @ 080d157c 0180
    adds r0,r4,#0x0    @ 080d157e 201c
    bl check_zone_slot_attr_visible          @ 080d1580 fff700f9
    cmp r0,#0x0                              @ 080d1584 0028
    beq LAB_080d158c                         @ 080d1586 01d0
    movs r3,#0x0    @ 080d1588 0023
    .hword 0x4699    @ 080d158a 9946
LAB_080d158c:
    adds r0,r5,#0x0    @ 080d158c 281c
    movs r1,#0x3    @ 080d158e 0321
    bl __modsi3                              @ 080d1590 3df084f8
    adds r4,r0,#0x0    @ 080d1594 041c
    lsls r4,r4,#0x3    @ 080d1596 e400
    movs r0,#0x88    @ 080d1598 8820
    lsls r0,r0,#0x2    @ 080d159a 8000
    adds r4,r4,r0    @ 080d159c 2418
    adds r0,r5,#0x0    @ 080d159e 281c
    movs r1,#0x3    @ 080d15a0 0321
    bl __divsi3                              @ 080d15a2 3df02ff8
    lsls r0,r0,#0x7    @ 080d15a6 c001
    adds r4,r4,r0    @ 080d15a8 2418
    lsls r4,r4,#0x10    @ 080d15aa 2404
    lsrs r4,r4,#0x10    @ 080d15ac 240c
    adds r0,r7,#0x0    @ 080d15ae 381c
    .hword 0x4649    @ 080d15b0 4946
    movs r2,#0x0    @ 080d15b2 0022
    adds r3,r4,#0x0    @ 080d15b4 231c
    bl load_card_list_small_image            @ 080d15b6 f1f701ff
    ldr r2, DWORD_080d1618                   @ 080d15ba 174a
    adds r1,r6,r2    @ 080d15bc b118
    movs r0,#0x5    @ 080d15be 0520
    rsbs r0,r0,#0    @ 080d15c0 4042
    ldrb r3,[r1,#0x0]                        @ 080d15c2 0b78
    ands r0,r3    @ 080d15c4 1840
    strb r0,[r1,#0x0]                        @ 080d15c6 0870
LAB_080d15c8:
    ldr r1, DWORD_080d1610                   @ 080d15c8 1149
    ldr r4, DWORD_080d1618                   @ 080d15ca 134c
    adds r1,r1,r4    @ 080d15cc 0919
    movs r0,#0x2    @ 080d15ce 0220
    ldrb r1,[r1,#0x0]                        @ 080d15d0 0978
    ands r0,r1    @ 080d15d2 0840
    cmp r0,#0x0                              @ 080d15d4 0028
    beq LAB_080d15da                         @ 080d15d6 00d0
    b LAB_080d1b02                           @ 080d15d8 93e2
LAB_080d15da:
    ldr r0,[sp,#0x20]                        @ 080d15da 0898
    cmp r0,#0x0                              @ 080d15dc 0028
    bne LAB_080d161c                         @ 080d15de 1dd1
    movs r1,#0x0    @ 080d15e0 0021
    .hword 0x468a    @ 080d15e2 8a46
    movs r5,#0xa0    @ 080d15e4 a025
    lsls r5,r5,#0xf    @ 080d15e6 ed03
    movs r4,#0x28    @ 080d15e8 2824
LAB_080d15ea:
    adds r0,r4,#0x0    @ 080d15ea 201c
    orrs r0,r5    @ 080d15ec 2843
    .hword 0x4653    @ 080d15ee 5346
    lsls r2,r3,#0x12    @ 080d15f0 9a04
    movs r1,#0xb0    @ 080d15f2 b021
    lsls r1,r1,#0x11    @ 080d15f4 4904
    adds r2,r2,r1    @ 080d15f6 5218
    lsrs r2,r2,#0x10    @ 080d15f8 120c
    movs r1,#0x81    @ 080d15fa 8121
    lsls r1,r1,#0x7    @ 080d15fc c901
    bl write_oam_entry_from_packed_args      @ 080d15fe 24f0b5fd
    adds r4,#0x20    @ 080d1602 2034
    movs r2,#0x1    @ 080d1604 0122
    add r10,r2                               @ 080d1606 9244
    .hword 0x4653    @ 080d1608 5346
    cmp r3,#0x6                              @ 080d160a 062b
    ble LAB_080d15ea                         @ 080d160c eddd
    b LAB_080d1b02                           @ 080d160e 78e2
DWORD_080d1610:
    .word  0x02020160                     @ 080d1610 60010202
DWORD_080d1614:
    .word  0x00002e42                     @ 080d1614 422e0000
DWORD_080d1618:
    .word  0x00002f51                     @ 080d1618 512f0000
LAB_080d161c:
    movs r4,#0x0    @ 080d161c 0024
    .hword 0x46a2    @ 080d161e a246
    ldr r0,[sp,#0x20]                        @ 080d1620 0898
    cmp r10,r0                               @ 080d1622 8245
    blt LAB_080d1628                         @ 080d1624 00db
    b LAB_080d1b02                           @ 080d1626 6ce2
LAB_080d1628:
    ldr r1, DWORD_080d1658                   @ 080d1628 0b49
    ldr r2, DWORD_080d165c                   @ 080d162a 0c4a
    adds r0,r1,r2    @ 080d162c 8818
    ldrb r0,[r0,#0x0]                        @ 080d162e 0078
    lsrs r2,r0,#0x5    @ 080d1630 4209
    ldr r4, DWORD_080d1660                   @ 080d1632 0b4c
    adds r3,r1,r4    @ 080d1634 0b19
    movs r0,#0x1f    @ 080d1636 1f20
    ldrb r4,[r3,#0x0]                        @ 080d1638 1c78
    ands r0,r4    @ 080d163a 2040
    lsls r0,r0,#0x3    @ 080d163c c000
    orrs r0,r2    @ 080d163e 1043
    .hword 0x4689    @ 080d1640 8946
    cmp r0,#0x0                              @ 080d1642 0028
    beq LAB_080d1664                         @ 080d1644 0ed0
    ldr r0,[r3,#0x0]                         @ 080d1646 1868
    lsls r0,r0,#0xb    @ 080d1648 c002
    lsrs r0,r0,#0x18    @ 080d164a 000e
    add r0,r10                               @ 080d164c 5044
    lsls r0,r0,#0x1    @ 080d164e 4000
    movs r1,#0xa8    @ 080d1650 a821
    lsls r1,r1,#0x6    @ 080d1652 8901
    b LAB_080d1672                           @ 080d1654 0de0
    .zero  0x2
DWORD_080d1658:
    .word  0x02020160                     @ 080d1658 60010202
DWORD_080d165c:
    .word  0x00002f53                     @ 080d165c 532f0000
DWORD_080d1660:
    .word  0x00002f54                     @ 080d1660 542f0000
LAB_080d1664:
    ldr r0,[r3,#0x0]                         @ 080d1664 1868
    lsls r0,r0,#0xb    @ 080d1666 c002
    lsrs r0,r0,#0x18    @ 080d1668 000e
    add r0,r10                               @ 080d166a 5044
    lsls r0,r0,#0x1    @ 080d166c 4000
    movs r1,#0xa0    @ 080d166e a021
    lsls r1,r1,#0x6    @ 080d1670 8901
LAB_080d1672:
    add r1,r9                                @ 080d1672 4944
    adds r0,r0,r1    @ 080d1674 4018
    ldrh r0,[r0,#0x0]                        @ 080d1676 0088
    str r0,[sp,#0x28]                        @ 080d1678 0a90
    ldr r1,[sp,#0x28]                        @ 080d167a 0a99
    lsls r0,r1,#0x2    @ 080d167c 8800
    adds r0,r0,r1    @ 080d167e 4018
    lsls r0,r0,#0x3    @ 080d1680 c000
    .hword 0x4649    @ 080d1682 4946
    adds r1,#0x24    @ 080d1684 2431
    adds r0,r0,r1    @ 080d1686 4018
    ldrb r0,[r0,#0x1]                        @ 080d1688 4078
    .hword 0x4681    @ 080d168a 8146
    ldr r2,[sp,#0x24]                        @ 080d168c 099a
    add r2,r10                               @ 080d168e 5244
    .hword 0x4690    @ 080d1690 9046
    .hword 0x4640    @ 080d1692 4046
    movs r1,#0x5    @ 080d1694 0521
    bl __modsi3                              @ 080d1696 3df001f8
    .hword 0x4680    @ 080d169a 8046
    ldr r3,[sp,#0x20]                        @ 080d169c 089b
    lsls r6,r3,#0x1    @ 080d169e 5e00
    movs r0,#0xc8    @ 080d16a0 c820
    adds r1,r6,#0x0    @ 080d16a2 311c
    bl __divsi3                              @ 080d16a4 3cf0aeff
    .hword 0x4654    @ 080d16a8 5446
    lsls r5,r4,#0x1    @ 080d16aa 6500
    adds r1,r5,#0x1    @ 080d16ac 691c
    muls r0,r1    @ 080d16ae 4843
    adds r7,r0,#0x0    @ 080d16b0 071c
    adds r7,#0x18    @ 080d16b2 1837
    movs r0,#0x98    @ 080d16b4 9820
    lsls r0,r0,#0xf    @ 080d16b6 c003
    orrs r7,r0    @ 080d16b8 0743
    .hword 0x4640    @ 080d16ba 4046
    movs r1,#0x3    @ 080d16bc 0321
    bl __modsi3                              @ 080d16be 3cf0edff
    adds r4,r0,#0x0    @ 080d16c2 041c
    lsls r4,r4,#0x3    @ 080d16c4 e400
    .hword 0x4640    @ 080d16c6 4046
    movs r1,#0x3    @ 080d16c8 0321
    bl __divsi3                              @ 080d16ca 3cf09bff
    lsls r0,r0,#0x7    @ 080d16ce c001
    movs r1,#0x88    @ 080d16d0 8821
    lsls r1,r1,#0x2    @ 080d16d2 8900
    adds r0,r0,r1    @ 080d16d4 4018
    adds r4,r4,r0    @ 080d16d6 2418
    lsls r4,r4,#0xf    @ 080d16d8 e403
    lsrs r4,r4,#0x10    @ 080d16da 240c
    adds r0,r7,#0x0    @ 080d16dc 381c
    movs r1,#0x80    @ 080d16de 8021
    adds r2,r4,#0x0    @ 080d16e0 221c
    bl write_oam_entry_with_tile_inc         @ 080d16e2 24f0b5fe
    ldr r0,[sp,#0x28]                        @ 080d16e6 0a98
    bl check_zone_anim_id_in_table           @ 080d16e8 fff770f8
    str r5,[sp,#0x30]                        @ 080d16ec 0c95
    str r6,[sp,#0x34]                        @ 080d16ee 0d96
    cmp r0,#0x0                              @ 080d16f0 0028
    beq LAB_080d1700                         @ 080d16f2 05d0
    movs r2,#0xfe    @ 080d16f4 fe22
    lsls r2,r2,#0x1    @ 080d16f6 5200
    adds r0,r7,#0x0    @ 080d16f8 381c
    movs r1,#0x80    @ 080d16fa 8021
    bl write_oam_entry_from_packed_args      @ 080d16fc 24f036fd
LAB_080d1700:
    .hword 0x4652    @ 080d1700 5246
    adds r2,#0x1    @ 080d1702 0132
    str r2,[sp,#0x2c]                        @ 080d1704 0b92
    .hword 0x464b    @ 080d1706 4b46
    cmp r3,#0x10                             @ 080d1708 102b
    bne LAB_080d170e                         @ 080d170a 00d1
    b LAB_080d1964                           @ 080d170c 2ae1
LAB_080d170e:
    ldr r0,[sp,#0x28]                        @ 080d170e 0a98
    bl dispatch_effect_ctx_slot_by_zone_type @ 080d1710 c2f742fe
    adds r5,r0,#0x0    @ 080d1714 051c
    lsrs r4,r5,#0xc    @ 080d1716 2c0b
    movs r0,#0x1    @ 080d1718 0120
    ands r4,r0    @ 080d171a 0440
    movs r7,#0x0    @ 080d171c 0027
    movs r6,#0x0    @ 080d171e 0026
    .hword 0x4648    @ 080d1720 4846
    subs r0,#0xb    @ 080d1722 0b38
    cmp r0,#0x4                              @ 080d1724 0428
    bhi LAB_080d1768                         @ 080d1726 1fd8
    lsls r0,r0,#0x2    @ 080d1728 8000
    ldr r1, PTR_PTR_080d1734                 @ 080d172a 0249
    adds r0,r0,r1    @ 080d172c 4018
    ldr r0,[r0,#0x0]                         @ 080d172e 0068
    .hword 0x4687    @ 080d1730 8746
    .zero  0x2
PTR_PTR_080d1734:
    .word  0x080d1738                     @ 080d1734 38170d08
PTR_DAT_080d1738:
    .word  0x080d174c                     @ 080d1738 4c170d08
    .word  0x080d1752                     @ 080d173c 52170d08
    .word  0x080d1756                     @ 080d1740 56170d08
    .word  0x080d175c                     @ 080d1744 5c170d08
    .word  0x080d1762                     @ 080d1748 62170d08
DAT_080d174c:
    ROM_INCBIN 0xd174c, 0x1c
LAB_080d1768:
    movs r1,#0x0    @ 080d1768 0021
    .hword 0x4689    @ 080d176a 8946
    movs r0,#0xc8    @ 080d176c c820
    ldr r1,[sp,#0x34]                        @ 080d176e 0d99
    bl __divsi3                              @ 080d1770 3cf048ff
    ldr r1,[sp,#0x30]                        @ 080d1774 0c99
    adds r1,#0x1    @ 080d1776 0131
    muls r0,r1    @ 080d1778 4843
    adds r0,#0x18    @ 080d177a 1830
    movs r1,#0x80    @ 080d177c 8021
    lsls r1,r1,#0xf    @ 080d177e c903
    orrs r0,r1    @ 080d1780 0843
    movs r1,#0x81    @ 080d1782 8121
    lsls r1,r1,#0x7    @ 080d1784 c901
    lsls r2,r4,#0x6    @ 080d1786 a201
    movs r4,#0xac    @ 080d1788 ac24
    lsls r4,r4,#0x2    @ 080d178a a400
    adds r3,r4,#0x0    @ 080d178c 231c
    adds r2,r2,r3    @ 080d178e d218
    ldr r4, DWORD_080d198c                   @ 080d1790 7e4c
    adds r3,r4,#0x0    @ 080d1792 231c
    orrs r2,r3    @ 080d1794 1a43
    lsls r2,r2,#0x10    @ 080d1796 1204
    lsrs r2,r2,#0x10    @ 080d1798 120c
    bl write_oam_entry_from_packed_args      @ 080d179a 24f0e7fc
    movs r0,#0x80    @ 080d179e 8020
    ands r0,r5    @ 080d17a0 2840
    cmp r0,#0x0                              @ 080d17a2 0028
    beq LAB_080d17cc                         @ 080d17a4 12d0
    movs r0,#0x2    @ 080d17a6 0220
    orrs r7,r0    @ 080d17a8 0743
    adds r0,r6,#0x1    @ 080d17aa 701c
    lsls r0,r0,#0x10    @ 080d17ac 0004
    lsrs r6,r0,#0x10    @ 080d17ae 060c
    ldr r0, DWORD_080d1990                   @ 080d17b0 7748
    .hword 0x4642    @ 080d17b2 4246
    lsls r1,r2,#0x1    @ 080d17b4 5100
    ldr r3, DWORD_080d1994                   @ 080d17b6 774b
    adds r0,r0,r3    @ 080d17b8 c018
    adds r1,r1,r0    @ 080d17ba 0918
    ldrh r0,[r1,#0x0]                        @ 080d17bc 0888
    cmp r0,#0x0                              @ 080d17be 0028
    bne LAB_080d17c6                         @ 080d17c0 01d1
    movs r0,#0x1    @ 080d17c2 0120
    strh r0,[r1,#0x0]                        @ 080d17c4 0880
LAB_080d17c6:
    adds r0,r6,#0x1    @ 080d17c6 701c
    lsls r0,r0,#0x10    @ 080d17c8 0004
    lsrs r6,r0,#0x10    @ 080d17ca 060c
LAB_080d17cc:
    movs r0,#0x40    @ 080d17cc 4020
    ands r0,r5    @ 080d17ce 2840
    cmp r0,#0x0                              @ 080d17d0 0028
    beq LAB_080d17f8                         @ 080d17d2 11d0
    movs r0,#0x4    @ 080d17d4 0420
    orrs r7,r0    @ 080d17d6 0743
    lsls r0,r7,#0x10    @ 080d17d8 3804
    lsrs r7,r0,#0x10    @ 080d17da 070c
    ldr r0, DWORD_080d1990                   @ 080d17dc 6c48
    .hword 0x4644    @ 080d17de 4446
    lsls r1,r4,#0x1    @ 080d17e0 6100
    ldr r2, DWORD_080d1994                   @ 080d17e2 6c4a
    adds r0,r0,r2    @ 080d17e4 8018
    adds r1,r1,r0    @ 080d17e6 0918
    ldrh r0,[r1,#0x0]                        @ 080d17e8 0888
    cmp r0,#0x0                              @ 080d17ea 0028
    bne LAB_080d17f2                         @ 080d17ec 01d1
    movs r0,#0x2    @ 080d17ee 0220
    strh r0,[r1,#0x0]                        @ 080d17f0 0880
LAB_080d17f2:
    adds r0,r6,#0x1    @ 080d17f2 701c
    lsls r0,r0,#0x10    @ 080d17f4 0004
    lsrs r6,r0,#0x10    @ 080d17f6 060c
LAB_080d17f8:
    movs r0,#0xc0    @ 080d17f8 c020
    lsls r0,r0,#0x2    @ 080d17fa 8000
    ands r0,r5    @ 080d17fc 2840
    cmp r0,#0x0                              @ 080d17fe 0028
    beq LAB_080d1826                         @ 080d1800 11d0
    movs r0,#0x8    @ 080d1802 0820
    orrs r7,r0    @ 080d1804 0743
    lsls r0,r7,#0x10    @ 080d1806 3804
    lsrs r7,r0,#0x10    @ 080d1808 070c
    ldr r0, DWORD_080d1990                   @ 080d180a 6148
    .hword 0x4643    @ 080d180c 4346
    lsls r1,r3,#0x1    @ 080d180e 5900
    ldr r4, DWORD_080d1994                   @ 080d1810 604c
    adds r0,r0,r4    @ 080d1812 0019
    adds r1,r1,r0    @ 080d1814 0918
    ldrh r0,[r1,#0x0]                        @ 080d1816 0888
    cmp r0,#0x0                              @ 080d1818 0028
    bne LAB_080d1820                         @ 080d181a 01d1
    movs r0,#0x3    @ 080d181c 0320
    strh r0,[r1,#0x0]                        @ 080d181e 0880
LAB_080d1820:
    adds r0,r6,#0x1    @ 080d1820 701c
    lsls r0,r0,#0x10    @ 080d1822 0004
    lsrs r6,r0,#0x10    @ 080d1824 060c
LAB_080d1826:
    movs r0,#0x80    @ 080d1826 8020
    lsls r0,r0,#0x3    @ 080d1828 c000
    ands r0,r5    @ 080d182a 2840
    cmp r0,#0x0                              @ 080d182c 0028
    beq LAB_080d1854                         @ 080d182e 11d0
    movs r0,#0x10    @ 080d1830 1020
    orrs r7,r0    @ 080d1832 0743
    lsls r0,r7,#0x10    @ 080d1834 3804
    lsrs r7,r0,#0x10    @ 080d1836 070c
    ldr r0, DWORD_080d1990                   @ 080d1838 5548
    .hword 0x4642    @ 080d183a 4246
    lsls r1,r2,#0x1    @ 080d183c 5100
    ldr r3, DWORD_080d1994                   @ 080d183e 554b
    adds r0,r0,r3    @ 080d1840 c018
    adds r1,r1,r0    @ 080d1842 0918
    ldrh r0,[r1,#0x0]                        @ 080d1844 0888
    cmp r0,#0x0                              @ 080d1846 0028
    bne LAB_080d184e                         @ 080d1848 01d1
    movs r0,#0x4    @ 080d184a 0420
    strh r0,[r1,#0x0]                        @ 080d184c 0880
LAB_080d184e:
    adds r0,r6,#0x1    @ 080d184e 701c
    lsls r0,r0,#0x10    @ 080d1850 0004
    lsrs r6,r0,#0x10    @ 080d1852 060c
LAB_080d1854:
    movs r0,#0x80    @ 080d1854 8020
    lsls r0,r0,#0x4    @ 080d1856 0001
    ands r0,r5    @ 080d1858 2840
    cmp r0,#0x0                              @ 080d185a 0028
    beq LAB_080d1882                         @ 080d185c 11d0
    movs r0,#0x20    @ 080d185e 2020
    orrs r7,r0    @ 080d1860 0743
    lsls r0,r7,#0x10    @ 080d1862 3804
    lsrs r7,r0,#0x10    @ 080d1864 070c
    ldr r0, DWORD_080d1990                   @ 080d1866 4a48
    .hword 0x4644    @ 080d1868 4446
    lsls r1,r4,#0x1    @ 080d186a 6100
    ldr r2, DWORD_080d1994                   @ 080d186c 494a
    adds r0,r0,r2    @ 080d186e 8018
    adds r1,r1,r0    @ 080d1870 0918
    ldrh r0,[r1,#0x0]                        @ 080d1872 0888
    cmp r0,#0x0                              @ 080d1874 0028
    bne LAB_080d187c                         @ 080d1876 01d1
    movs r0,#0x5    @ 080d1878 0520
    strh r0,[r1,#0x0]                        @ 080d187a 0880
LAB_080d187c:
    adds r0,r6,#0x1    @ 080d187c 701c
    lsls r0,r0,#0x10    @ 080d187e 0004
    lsrs r6,r0,#0x10    @ 080d1880 060c
LAB_080d1882:
    .hword 0x464b    @ 080d1882 4b46
    cmp r3,#0x0                              @ 080d1884 002b
    beq LAB_080d18c0                         @ 080d1886 1bd0
    movs r4,#0x0    @ 080d1888 0024
    cmp r7,#0x0                              @ 080d188a 002f
    bne LAB_080d1890                         @ 080d188c 00d1
    movs r4,#0x8    @ 080d188e 0824
LAB_080d1890:
    movs r0,#0xc8    @ 080d1890 c820
    ldr r1,[sp,#0x34]                        @ 080d1892 0d99
    bl __divsi3                              @ 080d1894 3cf0b6fe
    ldr r1,[sp,#0x30]                        @ 080d1898 0c99
    adds r1,#0x1    @ 080d189a 0131
    muls r0,r1    @ 080d189c 4843
    adds r1,r4,#0x0    @ 080d189e 211c
    adds r1,#0x18    @ 080d18a0 1831
    adds r0,r0,r1    @ 080d18a2 4018
    movs r1,#0x80    @ 080d18a4 8021
    lsls r1,r1,#0xf    @ 080d18a6 c903
    orrs r0,r1    @ 080d18a8 0843
    .hword 0x464c    @ 080d18aa 4c46
    lsls r2,r4,#0x1    @ 080d18ac 6200
    ldr r1, DWORD_080d1998                   @ 080d18ae 3a49
    adds r2,r2,r1    @ 080d18b0 5218
    movs r3,#0x80    @ 080d18b2 8023
    lsls r3,r3,#0x6    @ 080d18b4 9b01
    adds r1,r3,#0x0    @ 080d18b6 191c
    orrs r2,r1    @ 080d18b8 0a43
    movs r1,#0x40    @ 080d18ba 4021
    bl write_oam_entry_from_packed_args      @ 080d18bc 24f056fc
LAB_080d18c0:
    .hword 0x4654    @ 080d18c0 5446
    adds r4,#0x1    @ 080d18c2 0134
    str r4,[sp,#0x2c]                        @ 080d18c4 0b94
    cmp r7,#0x0                              @ 080d18c6 002f
    beq LAB_080d1964                         @ 080d18c8 4cd0
    movs r4,#0x8    @ 080d18ca 0824
    .hword 0x4648    @ 080d18cc 4846
    cmp r0,#0x0                              @ 080d18ce 0028
    beq LAB_080d18d4                         @ 080d18d0 00d0
    movs r4,#0x10    @ 080d18d2 1024
LAB_080d18d4:
    ldr r1, DWORD_080d1990                   @ 080d18d4 2e49
    .hword 0x4689    @ 080d18d6 8946
    .hword 0x4642    @ 080d18d8 4246
    lsls r5,r2,#0x1    @ 080d18da 5500
    adds r4,#0x18    @ 080d18dc 1834
    cmp r6,#0x1                              @ 080d18de 012e
    bls LAB_080d192e                         @ 080d18e0 25d9
    ldr r0, DWORD_080d199c                   @ 080d18e2 2e48
    movs r3,#0x83    @ 080d18e4 8323
    lsls r3,r3,#0x2    @ 080d18e6 9b00
    adds r0,r0,r3    @ 080d18e8 c018
    movs r1,#0x3f    @ 080d18ea 3f21
    ldrh r0,[r0,#0x0]                        @ 080d18ec 0088
    ands r1,r0    @ 080d18ee 0140
    cmp r1,#0x0                              @ 080d18f0 0029
    bne LAB_080d192e                         @ 080d18f2 1cd1
    ldr r0, DWORD_080d1994                   @ 080d18f4 2748
    add r0,r9                                @ 080d18f6 4844
    adds r0,r5,r0    @ 080d18f8 2818
    ldrh r0,[r0,#0x0]                        @ 080d18fa 0088
    adds r0,#0x1    @ 080d18fc 0130
    lsls r0,r0,#0x10    @ 080d18fe 0004
    lsrs r2,r0,#0x10    @ 080d1900 020c
    adds r1,r7,#0x0    @ 080d1902 391c
    asrs r1,r2    @ 080d1904 1141
    movs r0,#0x1    @ 080d1906 0120
    ands r1,r0    @ 080d1908 0140
    cmp r1,#0x0                              @ 080d190a 0029
    bne LAB_080d1926                         @ 080d190c 0bd1
    movs r1,#0x1    @ 080d190e 0121
LAB_080d1910:
    adds r0,r2,#0x1    @ 080d1910 501c
    lsls r0,r0,#0x10    @ 080d1912 0004
    lsrs r2,r0,#0x10    @ 080d1914 020c
    cmp r2,#0x5                              @ 080d1916 052a
    bls LAB_080d191c                         @ 080d1918 00d9
    movs r2,#0x1    @ 080d191a 0122
LAB_080d191c:
    adds r0,r7,#0x0    @ 080d191c 381c
    asrs r0,r2    @ 080d191e 1041
    ands r0,r1    @ 080d1920 0840
    cmp r0,#0x0                              @ 080d1922 0028
    beq LAB_080d1910                         @ 080d1924 f4d0
LAB_080d1926:
    ldr r0, DWORD_080d1994                   @ 080d1926 1b48
    add r0,r9                                @ 080d1928 4844
    adds r0,r5,r0    @ 080d192a 2818
    strh r2,[r0,#0x0]                        @ 080d192c 0280
LAB_080d192e:
    movs r0,#0xc8    @ 080d192e c820
    ldr r1,[sp,#0x34]                        @ 080d1930 0d99
    bl __divsi3                              @ 080d1932 3cf067fe
    ldr r1,[sp,#0x30]                        @ 080d1936 0c99
    adds r1,#0x1    @ 080d1938 0131
    muls r0,r1    @ 080d193a 4843
    adds r0,r0,r4    @ 080d193c 0019
    movs r1,#0x80    @ 080d193e 8021
    lsls r1,r1,#0xf    @ 080d1940 c903
    orrs r0,r1    @ 080d1942 0843
    ldr r1, DWORD_080d1994                   @ 080d1944 1349
    add r1,r9                                @ 080d1946 4944
    adds r1,r5,r1    @ 080d1948 6918
    ldrh r1,[r1,#0x0]                        @ 080d194a 0988
    lsls r2,r1,#0x1    @ 080d194c 4a00
    ldr r4, DWORD_080d19a0                   @ 080d194e 144c
    adds r2,r2,r4    @ 080d1950 1219
    movs r3,#0x80    @ 080d1952 8023
    lsls r3,r3,#0x6    @ 080d1954 9b01
    adds r1,r3,#0x0    @ 080d1956 191c
    orrs r2,r1    @ 080d1958 0a43
    lsls r2,r2,#0x10    @ 080d195a 1204
    lsrs r2,r2,#0x10    @ 080d195c 120c
    movs r1,#0x40    @ 080d195e 4021
    bl write_oam_entry_from_packed_args      @ 080d1960 24f004fc
LAB_080d1964:
    ldr r0,[sp,#0x28]                        @ 080d1964 0a98
    bl check_zone_slot_attr_visible          @ 080d1966 fef70dff
    cmp r0,#0x0                              @ 080d196a 0028
    beq LAB_080d1970                         @ 080d196c 00d0
    b LAB_080d1af6                           @ 080d196e c2e0
LAB_080d1970:
    ldr r0, DWORD_080d1990                   @ 080d1970 0748
    ldr r4, DWORD_080d19a4                   @ 080d1972 0c4c
    adds r0,r0,r4    @ 080d1974 0019
    ldrh r0,[r0,#0x0]                        @ 080d1976 0088
    lsls r0,r0,#0x13    @ 080d1978 c004
    lsrs r0,r0,#0x18    @ 080d197a 000e
    cmp r0,#0x7                              @ 080d197c 0728
    bls LAB_080d1982                         @ 080d197e 00d9
    b LAB_080d1af6                           @ 080d1980 b9e0
LAB_080d1982:
    lsls r0,r0,#0x2    @ 080d1982 8000
    ldr r1, PTR_PTR_080d19a8                 @ 080d1984 0849
    adds r0,r0,r1    @ 080d1986 4018
    ldr r0,[r0,#0x0]                         @ 080d1988 0068
    .hword 0x4687    @ 080d198a 8746
DWORD_080d198c:
    .word  0xffffa400                     @ 080d198c 00a4ffff
DWORD_080d1990:
    .word  0x02020160                     @ 080d1990 60010202
DWORD_080d1994:
    .word  0x00002e42                     @ 080d1994 422e0000
DWORD_080d1998:
    .word  0x000002b2                     @ 080d1998 b2020000
DWORD_080d199c:
    .word  gPrng                          @ 080d199c 40000003
DWORD_080d19a0:
    .word  0x000002f2                     @ 080d19a0 f2020000
DWORD_080d19a4:
    .word  0x00002f52                     @ 080d19a4 522f0000
PTR_PTR_080d19a8:
    .word  0x080d19ac                     @ 080d19a8 ac190d08
PTR_DAT_080d19ac:
    .word  0x080d19cc                     @ 080d19ac cc190d08
    .word  0x080d19cc                     @ 080d19b0 cc190d08
    .word  0x080d19f8                     @ 080d19b4 f8190d08
    .word  0x080d1a18                     @ 080d19b8 181a0d08
    .word  0x080d1a38                     @ 080d19bc 381a0d08
    .word  0x080d1a58                     @ 080d19c0 581a0d08
    .word  0x080d1a7c                     @ 080d19c4 7c1a0d08
    .word  0x080d1aba                     @ 080d19c8 ba1a0d08
DAT_080d19cc:
    ROM_INCBIN 0xd19cc, 0x12a
LAB_080d1af6:
    ldr r0,[sp,#0x2c]                        @ 080d1af6 0b98
    .hword 0x4682    @ 080d1af8 8246
    ldr r1,[sp,#0x20]                        @ 080d1afa 0899
    cmp r10,r1                               @ 080d1afc 8a45
    bge LAB_080d1b02                         @ 080d1afe 00da
    b LAB_080d1628                           @ 080d1b00 92e5
LAB_080d1b02:
    bl check_field_scroll_phase_ready        @ 080d1b02 00f06dfd
    cmp r0,#0x0                              @ 080d1b06 0028
    beq LAB_080d1b18                         @ 080d1b08 06d0
    ldr r0, DWORD_080d1b28                   @ 080d1b0a 0748
    movs r1,#0x81    @ 080d1b0c 8121
    lsls r1,r1,#0x7    @ 080d1b0e c901
    movs r2,#0x9f    @ 080d1b10 9f22
    lsls r2,r2,#0x2    @ 080d1b12 9200
    bl write_oam_entry_from_packed_args      @ 080d1b14 24f02afb
LAB_080d1b18:
    add sp,#0x38                             @ 080d1b18 0eb0
    pop {r3,r4,r5}                           @ 080d1b1a 38bc
    .hword 0x4698    @ 080d1b1c 9846
    .hword 0x46a1    @ 080d1b1e a146
    .hword 0x46aa    @ 080d1b20 aa46
    pop {r4,r5,r6,r7}                        @ 080d1b22 f0bc
    pop {r0}                                 @ 080d1b24 01bc
    bx r0                                    @ 080d1b26 0047
DWORD_080d1b28:
    .word  0x0080007c                     @ 080d1b28 7c008000

@ Zone card animation two-pass OAM render wrapper. Entry reads gDuelCtx+0x2f51 bit4: if set, returns immediately (animation inactive). Otherwise calls in sequence: render_zone_card_anim_oam_frame (0x080d1088) and render_zone_card_anim_oam_with_base (0x080d136c) for two OAM write passes. Then re-evaluates type_combined from gDuelCtx+0x2f53/0x2f54: if <=5 and gDuelCtx+0x2f58 type also satisfies condition, calls render_zone_card_anim_oam_frame_alt (0x080d0c7c) as third path. Called exclusively by FUN_080d2ef4. Side effects: OAM writes (through three sub-functions). Constants: gDuelCtx=0x02020160, active_flag_offset=0x2f51, active_bit=bit4=0x10.
render_zone_card_anim_dual_pass:
    push {r4,lr}                             @ 080d1b2c 10b5
    ldr r4, DWORD_080d1b74                   @ 080d1b2e 114c
    ldr r0, DWORD_080d1b78                   @ 080d1b30 1148
    adds r1,r4,r0    @ 080d1b32 2118
    movs r0,#0x10    @ 080d1b34 1020
    ldrb r1,[r1,#0x0]                        @ 080d1b36 0978
    ands r0,r1    @ 080d1b38 0840
    cmp r0,#0x0                              @ 080d1b3a 0028
    bne LAB_080d1ba6                         @ 080d1b3c 33d1
    bl render_zone_card_anim_oam_frame       @ 080d1b3e fff7a3fa
    bl render_zone_card_anim_oam_with_base   @ 080d1b42 fff713fc
    ldr r1, DWORD_080d1b7c                   @ 080d1b46 0d49
    adds r0,r4,r1    @ 080d1b48 6018
    ldrb r0,[r0,#0x0]                        @ 080d1b4a 0078
    lsrs r2,r0,#0x5    @ 080d1b4c 4209
    ldr r0, DWORD_080d1b80                   @ 080d1b4e 0c48
    adds r1,r4,r0    @ 080d1b50 2118
    movs r3,#0x1f    @ 080d1b52 1f23
    adds r0,r3,#0x0    @ 080d1b54 181c
    ldrb r1,[r1,#0x0]                        @ 080d1b56 0978
    ands r0,r1    @ 080d1b58 0840
    lsls r0,r0,#0x3    @ 080d1b5a c000
    orrs r0,r2    @ 080d1b5c 1043
    cmp r0,#0x0                              @ 080d1b5e 0028
    beq LAB_080d1b88                         @ 080d1b60 12d0
    ldr r1, DWORD_080d1b84                   @ 080d1b62 0849
    adds r0,r4,r1    @ 080d1b64 6018
    ldrh r0,[r0,#0x0]                        @ 080d1b66 0088
    lsls r0,r0,#0x13    @ 080d1b68 c004
    lsrs r0,r0,#0x18    @ 080d1b6a 000e
    cmp r0,#0x5                              @ 080d1b6c 0528
    bgt LAB_080d1ba2                         @ 080d1b6e 18dc
    b LAB_080d1ba6                           @ 080d1b70 19e0
    .zero  0x2
DWORD_080d1b74:
    .word  0x02020160                     @ 080d1b74 60010202
DWORD_080d1b78:
    .word  0x00002f51                     @ 080d1b78 512f0000
DWORD_080d1b7c:
    .word  0x00002f53                     @ 080d1b7c 532f0000
DWORD_080d1b80:
    .word  0x00002f54                     @ 080d1b80 542f0000
DWORD_080d1b84:
    .word  0x00002f58                     @ 080d1b84 582f0000
LAB_080d1b88:
    ldr r1, DWORD_080d1bac                   @ 080d1b88 0849
    adds r0,r4,r1    @ 080d1b8a 6018
    ldrb r0,[r0,#0x0]                        @ 080d1b8c 0078
    lsrs r2,r0,#0x5    @ 080d1b8e 4209
    ldr r0, DWORD_080d1bb0                   @ 080d1b90 0748
    adds r1,r4,r0    @ 080d1b92 2118
    adds r0,r3,#0x0    @ 080d1b94 181c
    ldrb r1,[r1,#0x0]                        @ 080d1b96 0978
    ands r0,r1    @ 080d1b98 0840
    lsls r0,r0,#0x3    @ 080d1b9a c000
    orrs r0,r2    @ 080d1b9c 1043
    cmp r0,#0x5                              @ 080d1b9e 0528
    ble LAB_080d1ba6                         @ 080d1ba0 01dd
LAB_080d1ba2:
    bl render_zone_card_anim_oam_frame_alt   @ 080d1ba2 fff76bf8
LAB_080d1ba6:
    pop {r4}                                 @ 080d1ba6 10bc
    pop {r0}                                 @ 080d1ba8 01bc
    bx r0                                    @ 080d1baa 0047
DWORD_080d1bac:
    .word  0x00002f57                     @ 080d1bac 572f0000
DWORD_080d1bb0:
    .word  0x00002f58                     @ 080d1bb0 582f0000

@ Called by tick_zone_card_anim_state (0x080d2390) at phase=2 and by FUN_080d4268 directly. Extracts bits[7:5] from gDuelCtx+0x2f53 as card_high, bits[4:0] from gDuelCtx+0x2f54 shifted left 3, ORs to form type_combined [0..6]; if >6 jumps to LAB_080d21ce (error path). Indexes PTR_DAT_080d1c10 (7-entry function pointer table), loads target into r8, tail-calls via bx r8. Side effects: indirect VRAM/OAM writes through 7 sub-handlers. Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_OFFSET=0x2f54; CARD_WORD_OFFSET=0x2f58; JUMP_TABLE_PTR=0x080d1c0c; TYPE_COUNT=7; TYPE_MASK_HIGH=bits[7:5]; TYPE_MASK_LOW=0x1f.
dispatch_zone_card_anim_by_type:
    push {r4,r5,r6,r7,lr}                    @ 080d1bb4 f0b5
    .hword 0x4657    @ 080d1bb6 5746
    .hword 0x464e    @ 080d1bb8 4e46
    .hword 0x4645    @ 080d1bba 4546
    push {r5,r6,r7}                          @ 080d1bbc e0b4
    sub sp,#0x8                              @ 080d1bbe 82b0
    movs r0,#0x1    @ 080d1bc0 0120
    str r0,[sp,#0x4]                         @ 080d1bc2 0190
    ldr r2, DWORD_080d1bf8                   @ 080d1bc4 0c4a
    ldr r3, DWORD_080d1bfc                   @ 080d1bc6 0d4b
    adds r1,r2,r3    @ 080d1bc8 d118
    ldr r0, DWORD_080d1c00                   @ 080d1bca 0d48
    ldrh r5,[r1,#0x0]                        @ 080d1bcc 0d88
    ands r0,r5    @ 080d1bce 2840
    strh r0,[r1,#0x0]                        @ 080d1bd0 0880
    ldr r1, DWORD_080d1c04                   @ 080d1bd2 0c49
    adds r0,r2,r1    @ 080d1bd4 5018
    ldrb r0,[r0,#0x0]                        @ 080d1bd6 0078
    lsrs r3,r0,#0x5    @ 080d1bd8 4309
    ldr r5, DWORD_080d1c08                   @ 080d1bda 0b4d
    adds r1,r2,r5    @ 080d1bdc 5119
    movs r0,#0x1f    @ 080d1bde 1f20
    ldrb r1,[r1,#0x0]                        @ 080d1be0 0978
    ands r0,r1    @ 080d1be2 0840
    lsls r0,r0,#0x3    @ 080d1be4 c000
    orrs r0,r3    @ 080d1be6 1843
    cmp r0,#0x6                              @ 080d1be8 0628
    bls LAB_080d1bee                         @ 080d1bea 00d9
    b LAB_080d21ce                           @ 080d1bec efe2
LAB_080d1bee:
    lsls r0,r0,#0x2    @ 080d1bee 8000
    ldr r1, PTR_PTR_080d1c0c                 @ 080d1bf0 0649
    adds r0,r0,r1    @ 080d1bf2 4018
    ldr r0,[r0,#0x0]                         @ 080d1bf4 0068
    .hword 0x4687    @ 080d1bf6 8746
DWORD_080d1bf8:
    .word  0x02020160                     @ 080d1bf8 60010202
DWORD_080d1bfc:
    .word  0x00002f58                     @ 080d1bfc 582f0000
DWORD_080d1c00:
    .word  0xffffe01f                     @ 080d1c00 1fe0ffff
DWORD_080d1c04:
    .word  0x00002f53                     @ 080d1c04 532f0000
DWORD_080d1c08:
    .word  0x00002f54                     @ 080d1c08 542f0000
PTR_PTR_080d1c0c:
    .word  0x080d1c10                     @ 080d1c0c 101c0d08
PTR_DAT_080d1c10:
    .word  0x080d1c2c                     @ 080d1c10 2c1c0d08
    .word  0x080d1dc4                     @ 080d1c14 c41d0d08
    .word  0x080d1e78                     @ 080d1c18 781e0d08
    .word  0x080d1f28                     @ 080d1c1c 281f0d08
    .word  0x080d1fd8                     @ 080d1c20 d81f0d08
    .word  0x080d2088                     @ 080d1c24 88200d08
    .word  0x080d2138                     @ 080d1c28 38210d08
DAT_080d1c2c:
    ROM_INCBIN 0xd1c2c, 0x5a2
LAB_080d21ce:
    ldr r2, DWORD_080d2210                   @ 080d21ce 104a
    ldr r5, DWORD_080d2214                   @ 080d21d0 104d
    adds r3,r2,r5    @ 080d21d2 5319
    ldr r0,[r3,#0x0]                         @ 080d21d4 1868
    ldr r1, DWORD_080d2218                   @ 080d21d6 1049
    ands r0,r1    @ 080d21d8 0840
    str r0,[r3,#0x0]                         @ 080d21da 1860
    ldr r0, DWORD_080d221c                   @ 080d21dc 0f48
    adds r1,r2,r0    @ 080d21de 1118
    ldr r0, DWORD_080d2208                   @ 080d21e0 0948
    ldrh r3,[r1,#0x0]                        @ 080d21e2 0b88
    ands r0,r3    @ 080d21e4 1840
    strh r0,[r1,#0x0]                        @ 080d21e6 0880
    adds r5,#0x4    @ 080d21e8 0435
    adds r2,r2,r5    @ 080d21ea 5219
    ldrh r2,[r2,#0x0]                        @ 080d21ec 1288
    lsls r1,r2,#0x13    @ 080d21ee d104
    lsrs r0,r1,#0x18    @ 080d21f0 080e
    cmp r0,#0x5                              @ 080d21f2 0528
    bhi LAB_080d2220                         @ 080d21f4 14d8
    adds r1,r0,#0x0    @ 080d21f6 011c
    .hword 0x4689    @ 080d21f8 8946
    b LAB_080d2224                           @ 080d21fa 13e0
    .byte  0x57, 0x2f, 0x00, 0x00, 0xb8, 0x69, 0x81, 0x09, 0xc4, 0xf1, 0xe4, 0x09
DWORD_080d2208:
    .word  0xffffe01f                     @ 080d2208 1fe0ffff
    .byte  0x60, 0x2b, 0x02, 0x02
DWORD_080d2210:
    .word  0x02020160                     @ 080d2210 60010202
DWORD_080d2214:
    .word  0x00002f54                     @ 080d2214 542f0000
DWORD_080d2218:
    .word  0xffe01fff                     @ 080d2218 ff1fe0ff
DWORD_080d221c:
    .word  0x00002f56                     @ 080d221c 562f0000
LAB_080d2220:
    movs r0,#0x5    @ 080d2220 0520
    .hword 0x4681    @ 080d2222 8146
LAB_080d2224:
    movs r6,#0x0    @ 080d2224 0026
    cmp r6,r9                                @ 080d2226 4e45
    bge LAB_080d2296                         @ 080d2228 35da
    ldr r1, DWORD_080d22c4                   @ 080d222a 2649
    .hword 0x4688    @ 080d222c 8846
    ldr r7, DWORD_080d22c8                   @ 080d222e 264f
    add r7,r8                                @ 080d2230 4744
LAB_080d2232:
    lsls r0,r6,#0x1    @ 080d2232 7000
    movs r1,#0xa8    @ 080d2234 a821
    lsls r1,r1,#0x6    @ 080d2236 8901
    add r1,r8                                @ 080d2238 4144
    adds r0,r0,r1    @ 080d223a 4018
    ldrh r4,[r0,#0x0]                        @ 080d223c 0488
    lsls r0,r4,#0x2    @ 080d223e a000
    adds r0,r0,r4    @ 080d2240 0019
    lsls r0,r0,#0x3    @ 080d2242 c000
    add r0,r8                                @ 080d2244 4044
    ldr r5,[r0,#0x0]                         @ 080d2246 0568
    adds r0,r6,#0x0    @ 080d2248 301c
    bl render_zone_slot_card_icon_tile       @ 080d224a 01f0f1fa
    movs r0,#0x0    @ 080d224e 0020
    strh r0,[r7,#0x0]                        @ 080d2250 3880
    adds r0,r4,#0x0    @ 080d2252 201c
    bl check_zone_slot_attr_visible          @ 080d2254 fef796fa
    cmp r0,#0x0                              @ 080d2258 0028
    beq LAB_080d2260                         @ 080d225a 01d0
    movs r2,#0x0    @ 080d225c 0022
    str r2,[sp,#0x4]                         @ 080d225e 0192
LAB_080d2260:
    adds r0,r6,#0x0    @ 080d2260 301c
    movs r1,#0x3    @ 080d2262 0321
    bl __modsi3                              @ 080d2264 3cf01afa
    adds r4,r0,#0x0    @ 080d2268 041c
    lsls r4,r4,#0x3    @ 080d226a e400
    movs r3,#0x88    @ 080d226c 8823
    lsls r3,r3,#0x2    @ 080d226e 9b00
    adds r4,r4,r3    @ 080d2270 e418
    adds r0,r6,#0x0    @ 080d2272 301c
    movs r1,#0x3    @ 080d2274 0321
    bl __divsi3                              @ 080d2276 3cf0c5f9
    lsls r0,r0,#0x7    @ 080d227a c001
    adds r4,r4,r0    @ 080d227c 2418
    lsls r4,r4,#0x10    @ 080d227e 2404
    lsrs r4,r4,#0x10    @ 080d2280 240c
    adds r0,r5,#0x0    @ 080d2282 281c
    ldr r1,[sp,#0x4]                         @ 080d2284 0199
    movs r2,#0x0    @ 080d2286 0022
    adds r3,r4,#0x0    @ 080d2288 231c
    bl load_card_list_small_image            @ 080d228a f1f797f8
    adds r7,#0x2    @ 080d228e 0237
    adds r6,#0x1    @ 080d2290 0136
    cmp r6,r9                                @ 080d2292 4e45
    blt LAB_080d2232                         @ 080d2294 cddb
LAB_080d2296:
    ldr r3, DWORD_080d22c4                   @ 080d2296 0b4b
    ldr r5, DWORD_080d22cc                   @ 080d2298 0c4d
    adds r0,r3,r5    @ 080d229a 5819
    ldrb r0,[r0,#0x0]                        @ 080d229c 0078
    lsrs r2,r0,#0x5    @ 080d229e 4209
    ldr r0, DWORD_080d22d0                   @ 080d22a0 0b48
    adds r1,r3,r0    @ 080d22a2 1918
    movs r4,#0x1f    @ 080d22a4 1f24
    adds r0,r4,#0x0    @ 080d22a6 201c
    ldrb r1,[r1,#0x0]                        @ 080d22a8 0978
    ands r0,r1    @ 080d22aa 0840
    lsls r0,r0,#0x3    @ 080d22ac c000
    orrs r0,r2    @ 080d22ae 1043
    cmp r0,#0x0                              @ 080d22b0 0028
    beq LAB_080d22d8                         @ 080d22b2 11d0
    ldr r1, DWORD_080d22d4                   @ 080d22b4 0749
    adds r0,r3,r1    @ 080d22b6 5818
    ldrh r0,[r0,#0x0]                        @ 080d22b8 0088
    lsls r0,r0,#0x13    @ 080d22ba c004
    lsrs r0,r0,#0x18    @ 080d22bc 000e
    cmp r0,#0x5                              @ 080d22be 0528
    bgt LAB_080d22f2                         @ 080d22c0 17dc
    b LAB_080d231c                           @ 080d22c2 2be0
DWORD_080d22c4:
    .word  0x02020160                     @ 080d22c4 60010202
DWORD_080d22c8:
    .word  0x00002e42                     @ 080d22c8 422e0000
DWORD_080d22cc:
    .word  0x00002f53                     @ 080d22cc 532f0000
DWORD_080d22d0:
    .word  0x00002f54                     @ 080d22d0 542f0000
DWORD_080d22d4:
    .word  0x00002f58                     @ 080d22d4 582f0000
LAB_080d22d8:
    ldr r2, DWORD_080d2308                   @ 080d22d8 0b4a
    adds r0,r3,r2    @ 080d22da 9818
    ldrb r0,[r0,#0x0]                        @ 080d22dc 0078
    lsrs r2,r0,#0x5    @ 080d22de 4209
    ldr r5, DWORD_080d230c                   @ 080d22e0 0a4d
    adds r1,r3,r5    @ 080d22e2 5919
    adds r0,r4,#0x0    @ 080d22e4 201c
    ldrb r1,[r1,#0x0]                        @ 080d22e6 0978
    ands r0,r1    @ 080d22e8 0840
    lsls r0,r0,#0x3    @ 080d22ea c000
    orrs r0,r2    @ 080d22ec 1043
    cmp r0,#0x5                              @ 080d22ee 0528
    ble LAB_080d231c                         @ 080d22f0 14dd
LAB_080d22f2:
    ldr r0, DWORD_080d2310                   @ 080d22f2 0748
    ldr r1, DWORD_080d2314                   @ 080d22f4 0749
    ldr r2, DWORD_080d2318                   @ 080d22f6 084a
    movs r3,#0xc3    @ 080d22f8 c323
    lsls r3,r3,#0x1    @ 080d22fa 5b00
    str r3,[sp,#0x0]                         @ 080d22fc 0093
    movs r3,#0xb    @ 080d22fe 0b23
    bl apply_palette_offset_to_tile_row      @ 080d2300 1cf052f8
    b LAB_080d232e                           @ 080d2304 13e0
    .zero  0x2
DWORD_080d2308:
    .word  0x00002f57                     @ 080d2308 572f0000
DWORD_080d230c:
    .word  0x00002f58                     @ 080d230c 582f0000
DWORD_080d2310:
    .word  0x0600f3ca                     @ 080d2310 caf30006
DWORD_080d2314:
    .word  0x0988b6be                     @ 080d2314 beb68809
DWORD_080d2318:
    .word  0x00000119                     @ 080d2318 19010000
LAB_080d231c:
    ldr r0, DWORD_080d2358                   @ 080d231c 0e48
    ldr r1, DWORD_080d235c                   @ 080d231e 0f49
    ldr r2, DWORD_080d2360                   @ 080d2320 0f4a
    movs r3,#0xc3    @ 080d2322 c323
    lsls r3,r3,#0x1    @ 080d2324 5b00
    str r3,[sp,#0x0]                         @ 080d2326 0093
    movs r3,#0xb    @ 080d2328 0b23
    bl apply_palette_offset_to_tile_row      @ 080d232a 1cf03df8
LAB_080d232e:
    ldr r2, DWORD_080d2364                   @ 080d232e 0d4a
    ldr r0, DWORD_080d2368                   @ 080d2330 0d48
    adds r1,r2,r0    @ 080d2332 1118
    movs r0,#0xff    @ 080d2334 ff20
    lsls r0,r0,#0x5    @ 080d2336 4001
    ldrh r1,[r1,#0x0]                        @ 080d2338 0988
    ands r0,r1    @ 080d233a 0840
    cmp r0,#0x0                              @ 080d233c 0028
    beq LAB_080d236c                         @ 080d233e 15d0
    movs r1,#0xa8    @ 080d2340 a821
    lsls r1,r1,#0x6    @ 080d2342 8901
    adds r0,r2,r1    @ 080d2344 5018
    ldrh r0,[r0,#0x0]                        @ 080d2346 0088
    movs r1,#0x0    @ 080d2348 0021
    ldr r2,[sp,#0x4]                         @ 080d234a 019a
    cmp r2,#0x0                              @ 080d234c 002a
    bne LAB_080d2352                         @ 080d234e 00d1
    movs r1,#0x1    @ 080d2350 0121
LAB_080d2352:
    bl dispatch_zone_card_display_by_mode    @ 080d2352 fef761fa
    b LAB_080d2376                           @ 080d2356 0ee0
DWORD_080d2358:
    .word  0x0600f3ca                     @ 080d2358 caf30006
DWORD_080d235c:
    .word  0x0988b402                     @ 080d235c 02b48809
DWORD_080d2360:
    .word  0x00000119                     @ 080d2360 19010000
DWORD_080d2364:
    .word  0x02020160                     @ 080d2364 60010202
DWORD_080d2368:
    .word  0x00002f58                     @ 080d2368 582f0000
LAB_080d236c:
    ldr r1, DWORD_080d2388                   @ 080d236c 0649
    ldr r0, DWORD_080d238c                   @ 080d236e 0748
    strh r0,[r1,#0x8]                        @ 080d2370 0881
    bl zero_card_display_vram_regions        @ 080d2372 f8f7b9fc
LAB_080d2376:
    add sp,#0x8                              @ 080d2376 02b0
    pop {r3,r4,r5}                           @ 080d2378 38bc
    .hword 0x4698    @ 080d237a 9846
    .hword 0x46a1    @ 080d237c a146
    .hword 0x46aa    @ 080d237e aa46
    pop {r4,r5,r6,r7}                        @ 080d2380 f0bc
    pop {r0}                                 @ 080d2382 01bc
    bx r0                                    @ 080d2384 0047
    .zero  0x2
DWORD_080d2388:
    .word  0x02023130                     @ 080d2388 30310202
DWORD_080d238c:
    .word  0x0000ffff                     @ 080d238c ffff0000

@ Uniquely called by advance_zone_card_anim (0x080d3820). Core state-machine tick for duel field zone card slot display. Reads phase byte [0x020230ad] (0=idle-check, 1=loading, 2=active/render). phase=1: promote to 2, return 1. phase=0: check gPrng+0x148 bit6/bit7/bit5/bit4/bit2 card attr flags; conditionally call sync_state_and_init_sprite or write gDuelCtx+0x2f54/0x2f51/0x2f4d fields. phase=2: call dispatch_zone_card_anim_by_type. All paths return r0=1 (frame-processed). Constants: DUEL_CTX=0x02020160; SCENE_PHASE_ADDR=0x020230ad; PRNG_CARD_FLAGS=gPrng+0x148; FLAG_BIT6=0x40; FLAG_BIT7=0x80; FLAG_BIT5=0x20; FLAG_BIT4=0x10; FLAG_BIT2=0x2; ATTR_OFFSET1=0x2f54; ATTR_OFFSET2=0x2f51; ATTR_OFFSET3=0x2f4d.
tick_zone_card_anim_state:
    push {r4,r5,r6,r7,lr}                    @ 080d2390 f0b5
    .hword 0x4657    @ 080d2392 5746
    .hword 0x464e    @ 080d2394 4e46
    .hword 0x4645    @ 080d2396 4546
    push {r5,r6,r7}                          @ 080d2398 e0b4
    sub sp,#0x4                              @ 080d239a 81b0
    ldr r7, DWORD_080d23b4                   @ 080d239c 054f
    ldr r1, DWORD_080d23b8                   @ 080d239e 0649
    ldrb r0,[r1,#0x0]                        @ 080d23a0 0878
    .hword 0x46b8    @ 080d23a2 b846
    cmp r0,#0x1                              @ 080d23a4 0128
    bne LAB_080d23aa                         @ 080d23a6 00d1
    b LAB_080d25a8                           @ 080d23a8 fee0
LAB_080d23aa:
    cmp r0,#0x1                              @ 080d23aa 0128
    bgt LAB_080d23bc                         @ 080d23ac 06dc
    cmp r0,#0x0                              @ 080d23ae 0028
    beq LAB_080d23c4                         @ 080d23b0 08d0
    b LAB_080d25c4                           @ 080d23b2 07e1
DWORD_080d23b4:
    .word  0x02020160                     @ 080d23b4 60010202
DWORD_080d23b8:
    .word  0x020230ad                     @ 080d23b8 ad300202
LAB_080d23bc:
    cmp r0,#0x2                              @ 080d23bc 0228
    bne LAB_080d23c2                         @ 080d23be 00d1
    b LAB_080d25ac                           @ 080d23c0 f4e0
LAB_080d23c2:
    b LAB_080d25c4                           @ 080d23c2 ffe0
LAB_080d23c4:
    ldr r2, DWORD_080d23f8                   @ 080d23c4 0c4a
    movs r3,#0xa4    @ 080d23c6 a423
    lsls r3,r3,#0x1    @ 080d23c8 5b00
    adds r0,r2,r3    @ 080d23ca d018
    ldrh r1,[r0,#0x0]                        @ 080d23cc 0188
    movs r0,#0x40    @ 080d23ce 4020
    ands r0,r1    @ 080d23d0 0840
    cmp r0,#0x0                              @ 080d23d2 0028
    beq LAB_080d241c                         @ 080d23d4 22d0
    ldr r4, DWORD_080d23fc                   @ 080d23d6 094c
    adds r1,r7,r4    @ 080d23d8 3919
    movs r0,#0xff    @ 080d23da ff20
    lsls r0,r0,#0x5    @ 080d23dc 4001
    ldrh r1,[r1,#0x0]                        @ 080d23de 0988
    ands r0,r1    @ 080d23e0 0840
    cmp r0,#0x0                              @ 080d23e2 0028
    beq LAB_080d2408                         @ 080d23e4 10d0
    ldr r1, DWORD_080d2400                   @ 080d23e6 0649
    adds r0,r7,r1    @ 080d23e8 7818
    ldr r1, DWORD_080d2404                   @ 080d23ea 0649
    ldrh r2,[r0,#0x0]                        @ 080d23ec 0288
    ands r1,r2    @ 080d23ee 1140
    movs r2,#0x40    @ 080d23f0 4022
    orrs r1,r2    @ 080d23f2 1143
    strh r1,[r0,#0x0]                        @ 080d23f4 0180
    b LAB_080d25c4                           @ 080d23f6 e5e0
DWORD_080d23f8:
    .word  gPrng                          @ 080d23f8 40000003
DWORD_080d23fc:
    .word  0x00002f58                     @ 080d23fc 582f0000
DWORD_080d2400:
    .word  0x00002f54                     @ 080d2400 542f0000
DWORD_080d2404:
    .word  0xffffe01f                     @ 080d2404 1fe0ffff
LAB_080d2408:
    movs r3,#0xa9    @ 080d2408 a923
    lsls r3,r3,#0x1    @ 080d240a 5b00
    adds r1,r2,r3    @ 080d240c d118
    movs r0,#0x1f    @ 080d240e 1f20
    ldrb r1,[r1,#0x0]                        @ 080d2410 0978
    ands r0,r1    @ 080d2412 0840
    cmp r0,#0x0                              @ 080d2414 0028
    beq LAB_080d241a                         @ 080d2416 00d0
    b LAB_080d25c4                           @ 080d2418 d4e0
LAB_080d241a:
    b LAB_080d259a                           @ 080d241a bee0
LAB_080d241c:
    movs r0,#0x80    @ 080d241c 8020
    ands r0,r1    @ 080d241e 0840
    cmp r0,#0x0                              @ 080d2420 0028
    beq LAB_080d2450                         @ 080d2422 15d0
    ldr r4, DWORD_080d2444                   @ 080d2424 074c
    adds r1,r7,r4    @ 080d2426 3919
    movs r0,#0xff    @ 080d2428 ff20
    lsls r0,r0,#0x5    @ 080d242a 4001
    ldrh r1,[r1,#0x0]                        @ 080d242c 0988
    ands r0,r1    @ 080d242e 0840
    cmp r0,#0x0                              @ 080d2430 0028
    beq LAB_080d2408                         @ 080d2432 e9d0
LAB_080d2434:
    ldr r0, DWORD_080d2448                   @ 080d2434 0448
    adds r1,r7,r0    @ 080d2436 3918
    ldr r0, DWORD_080d244c                   @ 080d2438 0448
    ldrh r2,[r1,#0x0]                        @ 080d243a 0a88
    ands r0,r2    @ 080d243c 1040
    strh r0,[r1,#0x0]                        @ 080d243e 0880
    b LAB_080d25c4                           @ 080d2440 c0e0
    .zero  0x2
DWORD_080d2444:
    .word  0x00002f58                     @ 080d2444 582f0000
DWORD_080d2448:
    .word  0x00002f54                     @ 080d2448 542f0000
DWORD_080d244c:
    .word  0xffffe01f                     @ 080d244c 1fe0ffff
LAB_080d2450:
    movs r0,#0x20    @ 080d2450 2020
    ands r0,r1    @ 080d2452 0840
    cmp r0,#0x0                              @ 080d2454 0028
    beq LAB_080d24d8                         @ 080d2456 3fd0
    ldr r4, DWORD_080d2498                   @ 080d2458 0f4c
    adds r6,r7,r4    @ 080d245a 3e19
    ldrb r3,[r6,#0x0]                        @ 080d245c 3378
    lsrs r1,r3,#0x5    @ 080d245e 5909
    ldr r0, DWORD_080d249c                   @ 080d2460 0e48
    adds r5,r7,r0    @ 080d2462 3d18
    movs r4,#0x1f    @ 080d2464 1f24
    adds r0,r4,#0x0    @ 080d2466 201c
    ldrb r2,[r5,#0x0]                        @ 080d2468 2a78
    ands r0,r2    @ 080d246a 1040
    lsls r0,r0,#0x3    @ 080d246c c000
    orrs r0,r1    @ 080d246e 0843
    cmp r0,#0x0                              @ 080d2470 0028
    beq LAB_080d24a0                         @ 080d2472 15d0
    subs r2,r0,#0x1    @ 080d2474 421e
    lsls r2,r2,#0x10    @ 080d2476 1204
    lsrs r1,r2,#0x10    @ 080d2478 110c
    movs r0,#0x7    @ 080d247a 0720
    ands r1,r0    @ 080d247c 0140
    lsls r1,r1,#0x5    @ 080d247e 4901
    adds r0,r4,#0x0    @ 080d2480 201c
    ands r0,r3    @ 080d2482 1840
    orrs r0,r1    @ 080d2484 0843
    strb r0,[r6,#0x0]                        @ 080d2486 3070
    lsrs r2,r2,#0x13    @ 080d2488 d20c
    ands r2,r4    @ 080d248a 2240
    movs r0,#0x20    @ 080d248c 2020
    rsbs r0,r0,#0    @ 080d248e 4042
    ldrb r3,[r5,#0x0]                        @ 080d2490 2b78
    ands r0,r3    @ 080d2492 1840
    orrs r0,r2    @ 080d2494 1043
    b LAB_080d24b2                           @ 080d2496 0ce0
DWORD_080d2498:
    .word  0x00002f53                     @ 080d2498 532f0000
DWORD_080d249c:
    .word  0x00002f54                     @ 080d249c 542f0000
LAB_080d24a0:
    adds r0,r4,#0x0    @ 080d24a0 201c
    ands r0,r3    @ 080d24a2 1840
    movs r1,#0xc0    @ 080d24a4 c021
    orrs r0,r1    @ 080d24a6 0843
    strb r0,[r6,#0x0]                        @ 080d24a8 3070
    movs r0,#0x20    @ 080d24aa 2020
    rsbs r0,r0,#0    @ 080d24ac 4042
    ldrb r4,[r5,#0x0]                        @ 080d24ae 2c78
    ands r0,r4    @ 080d24b0 2040
LAB_080d24b2:
    strb r0,[r5,#0x0]                        @ 080d24b2 2870
    ldr r1, DWORD_080d24d0                   @ 080d24b4 0649
    add r1,r8                                @ 080d24b6 4144
    movs r0,#0x2    @ 080d24b8 0220
    ldrb r2,[r1,#0x0]                        @ 080d24ba 0a78
    orrs r0,r2    @ 080d24bc 1043
    strb r0,[r1,#0x0]                        @ 080d24be 0870
    ldr r1, DWORD_080d24d4                   @ 080d24c0 0449
    add r1,r8                                @ 080d24c2 4144
    movs r0,#0x1    @ 080d24c4 0120
    strb r0,[r1,#0x0]                        @ 080d24c6 0870
LAB_080d24c8:
    movs r0,#0x0    @ 080d24c8 0020
    bl sync_state_and_init_sprite            @ 080d24ca 27f0f3fa
    b LAB_080d25c4                           @ 080d24ce 79e0
DWORD_080d24d0:
    .word  0x00002f51                     @ 080d24d0 512f0000
DWORD_080d24d4:
    .word  0x00002f4d                     @ 080d24d4 4d2f0000
LAB_080d24d8:
    movs r0,#0x10    @ 080d24d8 1020
    ands r0,r1    @ 080d24da 0840
    cmp r0,#0x0                              @ 080d24dc 0028
    beq LAB_080d2580                         @ 080d24de 4fd0
    ldr r3, DWORD_080d2570                   @ 080d24e0 234b
    adds r3,r3,r7    @ 080d24e2 db19
    .hword 0x4698    @ 080d24e4 9846
    ldrb r3,[r3,#0x0]                        @ 080d24e6 1b78
    lsrs r1,r3,#0x5    @ 080d24e8 5909
    ldr r4, DWORD_080d2574                   @ 080d24ea 224c
    adds r2,r7,r4    @ 080d24ec 3a19
    movs r6,#0x1f    @ 080d24ee 1f26
    adds r0,r6,#0x0    @ 080d24f0 301c
    ldrb r4,[r2,#0x0]                        @ 080d24f2 1478
    ands r0,r4    @ 080d24f4 2040
    lsls r0,r0,#0x3    @ 080d24f6 c000
    orrs r0,r1    @ 080d24f8 0843
    adds r0,#0x1    @ 080d24fa 0130
    movs r1,#0x7    @ 080d24fc 0721
    .hword 0x468a    @ 080d24fe 8a46
    adds r1,r0,#0x0    @ 080d2500 011c
    .hword 0x4654    @ 080d2502 5446
    ands r1,r4    @ 080d2504 2140
    lsls r1,r1,#0x5    @ 080d2506 4901
    adds r4,r6,#0x0    @ 080d2508 341c
    ands r4,r3    @ 080d250a 1c40
    orrs r4,r1    @ 080d250c 0c43
    .hword 0x4641    @ 080d250e 4146
    strb r4,[r1,#0x0]                        @ 080d2510 0c70
    lsrs r0,r0,#0x3    @ 080d2512 c008
    ands r0,r6    @ 080d2514 3040
    movs r3,#0x20    @ 080d2516 2023
    rsbs r3,r3,#0    @ 080d2518 5b42
    .hword 0x4699    @ 080d251a 9946
    .hword 0x464d    @ 080d251c 4d46
    ldrb r1,[r2,#0x0]                        @ 080d251e 1178
    ands r5,r1    @ 080d2520 0d40
    orrs r5,r0    @ 080d2522 0543
    strb r5,[r2,#0x0]                        @ 080d2524 1570
    lsls r1,r4,#0x18    @ 080d2526 2106
    lsrs r1,r1,#0x1d    @ 080d2528 490f
    adds r0,r6,#0x0    @ 080d252a 301c
    ands r0,r5    @ 080d252c 2840
    lsls r0,r0,#0x3    @ 080d252e c000
    orrs r0,r1    @ 080d2530 0843
    movs r1,#0x7    @ 080d2532 0721
    str r2,[sp,#0x0]                         @ 080d2534 0092
    bl __umodsi3                             @ 080d2536 3cf08df9
    lsls r0,r0,#0x10    @ 080d253a 0004
    lsrs r1,r0,#0x10    @ 080d253c 010c
    .hword 0x4653    @ 080d253e 5346
    ands r1,r3    @ 080d2540 1940
    lsls r1,r1,#0x5    @ 080d2542 4901
    ands r4,r6    @ 080d2544 3440
    orrs r4,r1    @ 080d2546 0c43
    .hword 0x4641    @ 080d2548 4146
    strb r4,[r1,#0x0]                        @ 080d254a 0c70
    lsrs r0,r0,#0x13    @ 080d254c c00c
    ands r0,r6    @ 080d254e 3040
    .hword 0x464b    @ 080d2550 4b46
    ands r5,r3    @ 080d2552 1d40
    orrs r5,r0    @ 080d2554 0543
    ldr r2,[sp,#0x0]                         @ 080d2556 009a
    strb r5,[r2,#0x0]                        @ 080d2558 1570
    ldr r4, DWORD_080d2578                   @ 080d255a 074c
    adds r1,r7,r4    @ 080d255c 3919
    movs r0,#0x2    @ 080d255e 0220
    ldrb r2,[r1,#0x0]                        @ 080d2560 0a78
    orrs r0,r2    @ 080d2562 1043
    strb r0,[r1,#0x0]                        @ 080d2564 0870
    movs r0,#0x1    @ 080d2566 0120
    ldr r3, DWORD_080d257c                   @ 080d2568 044b
    strb r0,[r3,#0x0]                        @ 080d256a 1870
    b LAB_080d24c8                           @ 080d256c ace7
    .zero  0x2
DWORD_080d2570:
    .word  0x00002f53                     @ 080d2570 532f0000
DWORD_080d2574:
    .word  0x00002f54                     @ 080d2574 542f0000
DWORD_080d2578:
    .word  0x00002f51                     @ 080d2578 512f0000
DWORD_080d257c:
    .word  0x020230ad                     @ 080d257c ad300202
LAB_080d2580:
    movs r0,#0x2    @ 080d2580 0220
    ands r0,r1    @ 080d2582 0840
    cmp r0,#0x0                              @ 080d2584 0028
    beq LAB_080d25c4                         @ 080d2586 1dd0
    ldr r4, DWORD_080d25a4                   @ 080d2588 064c
    adds r1,r7,r4    @ 080d258a 3919
    movs r0,#0xff    @ 080d258c ff20
    lsls r0,r0,#0x5    @ 080d258e 4001
    ldrh r1,[r1,#0x0]                        @ 080d2590 0988
    ands r0,r1    @ 080d2592 0840
    cmp r0,#0x0                              @ 080d2594 0028
    beq LAB_080d259a                         @ 080d2596 00d0
    b LAB_080d2434                           @ 080d2598 4ce7
LAB_080d259a:
    movs r0,#0x2    @ 080d259a 0220
    bl sync_state_and_init_sprite            @ 080d259c 27f08afa
    b LAB_080d25c4                           @ 080d25a0 10e0
    .zero  0x2
DWORD_080d25a4:
    .word  0x00002f58                     @ 080d25a4 582f0000
LAB_080d25a8:
    movs r0,#0x2    @ 080d25a8 0220
    b LAB_080d25c0                           @ 080d25aa 09e0
LAB_080d25ac:
    bl dispatch_zone_card_anim_by_type       @ 080d25ac fff702fb
    ldr r4, DWORD_080d25d8                   @ 080d25b0 094c
    adds r0,r7,r4    @ 080d25b2 3819
    movs r1,#0x3    @ 080d25b4 0321
    rsbs r1,r1,#0    @ 080d25b6 4942
    ldrb r2,[r0,#0x0]                        @ 080d25b8 0278
    ands r1,r2    @ 080d25ba 1140
    strb r1,[r0,#0x0]                        @ 080d25bc 0170
    movs r0,#0x0    @ 080d25be 0020
LAB_080d25c0:
    ldr r3, DWORD_080d25dc                   @ 080d25c0 064b
    strb r0,[r3,#0x0]                        @ 080d25c2 1870
LAB_080d25c4:
    movs r0,#0x1    @ 080d25c4 0120
    add sp,#0x4                              @ 080d25c6 01b0
    pop {r3,r4,r5}                           @ 080d25c8 38bc
    .hword 0x4698    @ 080d25ca 9846
    .hword 0x46a1    @ 080d25cc a146
    .hword 0x46aa    @ 080d25ce aa46
    pop {r4,r5,r6,r7}                        @ 080d25d0 f0bc
    pop {r1}                                 @ 080d25d2 02bc
    bx r1                                    @ 080d25d4 0847
    .zero  0x2
DWORD_080d25d8:
    .word  0x00002f51                     @ 080d25d8 512f0000
DWORD_080d25dc:
    .word  0x020230ad                     @ 080d25dc ad300202

@ Check if duel field scroll animation phase satisfies advance condition. Called by FUN_080d136c / FUN_080d2ef4 / FUN_080d4478. Reads [0x0201e4f0+0x4] (phase_counter); dispatches by range: [0..5]: return 0 (too early). [6..37]: read scroll_flag [0x02020160+0x2e40]; if 0 -> return 0, else -> return 1. [38..71]: same scroll_flag + compare against get_clamped_tile_row_count (0x08094290); if scroll_flag < clamped_count -> return 0, else -> return 1. [>71]: return 1 (phase complete). Returns 1=ready_to_advance / 0=not_ready. Callee: get_clamped_tile_row_count. Constants: PHASE_BASE=0x0201e4f0; PHASE_OFFSET=0x4; SCROLL_FLAG_ADDR=0x02024fa0 (=0x02020160+0x2e40).
check_field_scroll_phase_ready:
    push {r4,lr}                             @ 080d25e0 10b5
    ldr r0, DWORD_080d2600                   @ 080d25e2 0748
    ldr r0,[r0,#0x4]                         @ 080d25e4 4068
    cmp r0,#0x26                             @ 080d25e6 2628
    bls LAB_080d2608                         @ 080d25e8 0ed9
    cmp r0,#0x47                             @ 080d25ea 4728
    bhi LAB_080d2626                         @ 080d25ec 1bd8
    ldr r0, DWORD_080d2604                   @ 080d25ee 0548
    movs r1,#0xb9    @ 080d25f0 b921
    lsls r1,r1,#0x6    @ 080d25f2 8901
    adds r0,r0,r1    @ 080d25f4 4018
    ldrb r0,[r0,#0x0]                        @ 080d25f6 0078
    cmp r0,#0x0                              @ 080d25f8 0028
    beq LAB_080d2610                         @ 080d25fa 09d0
    b LAB_080d2626                           @ 080d25fc 13e0
    .zero  0x2
DWORD_080d2600:
    .word  0x0201e4f0                     @ 080d2600 f0e40102
DWORD_080d2604:
    .word  0x02020160                     @ 080d2604 60010202
LAB_080d2608:
    cmp r0,#0x6                              @ 080d2608 0628
    bcs LAB_080d2614                         @ 080d260a 03d2
    cmp r0,#0x1                              @ 080d260c 0128
    bcc LAB_080d2626                         @ 080d260e 0ad3
LAB_080d2610:
    movs r0,#0x0    @ 080d2610 0020
    b LAB_080d2628                           @ 080d2612 09e0
LAB_080d2614:
    ldr r0, DWORD_080d2630                   @ 080d2614 0648
    movs r1,#0xb9    @ 080d2616 b921
    lsls r1,r1,#0x6    @ 080d2618 8901
    adds r0,r0,r1    @ 080d261a 4018
    ldrb r4,[r0,#0x0]                        @ 080d261c 0478
    bl get_clamped_tile_row_count            @ 080d261e c1f737fe
    cmp r4,r0                                @ 080d2622 8442
    blt LAB_080d2610                         @ 080d2624 f4db
LAB_080d2626:
    movs r0,#0x1    @ 080d2626 0120
LAB_080d2628:
    pop {r4}                                 @ 080d2628 10bc
    pop {r1}                                 @ 080d262a 02bc
    bx r1                                    @ 080d262c 0847
    .zero  0x2
DWORD_080d2630:
    .word  0x02020160                     @ 080d2630 60010202

@ Finds and updates matching entry in gDuelCtx+0x2dfe animation queue array. Queue length read from gDuelCtx+0x2e40 (0xb9*0x40); iterates entries (entry_size=2). r1==0 (clear mode): finds [entry+2]==r4, clears [entry+2] to 0, sets r3=1. r1!=0 (shift mode): copies [entry+2] to [entry+0]. After loop, if r3!=0: gDuelCtx+0x2e40 -= 1 (decrements queue length). Returns r3 (operation success flag). Called exclusively by FUN_080d2ef4. Side effects: [gDuelCtx+0x2dfe+i*2+2] := 0 (conditional clear); [gDuelCtx+0x2e40] -= 1 (conditional decrement). Constants: gDuelCtx=0x02020160, queue_base_offset=0x2dfe, count_offset=0x2e40, entry_size=2.
update_zone_anim_queue_entry:
    push {r4,r5,r6,lr}                       @ 080d2634 70b5
    adds r4,r0,#0x0    @ 080d2636 041c
    movs r3,#0x0    @ 080d2638 0023
    movs r1,#0x0    @ 080d263a 0021
    ldr r0, DWORD_080d265c                   @ 080d263c 0748
    movs r5,#0xb9    @ 080d263e b925
    lsls r5,r5,#0x6    @ 080d2640 ad01
    adds r2,r0,r5    @ 080d2642 4219
    adds r6,r0,#0x0    @ 080d2644 061c
    ldrb r0,[r2,#0x0]                        @ 080d2646 1078
    cmp r3,r0                                @ 080d2648 8342
    bge LAB_080d2678                         @ 080d264a 15da
    adds r5,r2,#0x0    @ 080d264c 151c
    ldr r0, DWORD_080d2660                   @ 080d264e 0448
    adds r2,r6,r0    @ 080d2650 3218
LAB_080d2652:
    cmp r3,#0x0                              @ 080d2652 002b
    beq LAB_080d2664                         @ 080d2654 06d0
    ldrh r0,[r2,#0x2]                        @ 080d2656 5088
    strh r0,[r2,#0x0]                        @ 080d2658 1080
    b LAB_080d266e                           @ 080d265a 08e0
DWORD_080d265c:
    .word  0x02020160                     @ 080d265c 60010202
DWORD_080d2660:
    .word  0x00002dfe                     @ 080d2660 fe2d0000
LAB_080d2664:
    ldrh r0,[r2,#0x2]                        @ 080d2664 5088
    cmp r0,r4                                @ 080d2666 a042
    bne LAB_080d266e                         @ 080d2668 01d1
    strh r3,[r2,#0x2]                        @ 080d266a 5380
    movs r3,#0x1    @ 080d266c 0123
LAB_080d266e:
    adds r2,#0x2    @ 080d266e 0232
    adds r1,#0x1    @ 080d2670 0131
    ldrb r0,[r5,#0x0]                        @ 080d2672 2878
    cmp r1,r0                                @ 080d2674 8142
    blt LAB_080d2652                         @ 080d2676 ecdb
LAB_080d2678:
    cmp r3,#0x0                              @ 080d2678 002b
    beq LAB_080d2688                         @ 080d267a 05d0
    movs r5,#0xb9    @ 080d267c b925
    lsls r5,r5,#0x6    @ 080d267e ad01
    adds r1,r6,r5    @ 080d2680 7119
    ldrb r0,[r1,#0x0]                        @ 080d2682 0878
    subs r0,#0x1    @ 080d2684 0138
    strb r0,[r1,#0x0]                        @ 080d2686 0870
LAB_080d2688:
    adds r0,r3,#0x0    @ 080d2688 181c
    pop {r4,r5,r6}                           @ 080d268a 70bc
    pop {r1}                                 @ 080d268c 02bc
    bx r1                                    @ 080d268e 0847

@ Reads gDuelCtx+0x2f4e (subtype byte); if >6, jumps to error path (LAB_080d29f4, clears byte). Otherwise uses subtype*4 to index PTR_PTR_080d26b8 (7-entry function pointer table at 0x080d26bc), loads target function pointer into r7, and tail-calls via '.hword 0x4687=bx r7'. 7 cases cover handlers at 0x080d26d8..0x080d29f4. Complements dispatch_zone_card_anim_by_type (0x080d1bb4) which dispatches on type_combined; this dispatches on subtype. Called exclusively by FUN_080d2ef4. Side effects: indirect (by sub-handlers). Constants: gDuelCtx=0x02020160, subtype_offset=0x2f4e, jump_table=0x080d26bc, handler_count=7.
dispatch_zone_card_anim_by_subtype:
    push {r4,r5,r6,r7,lr}                    @ 080d2690 f0b5
    sub sp,#0x4                              @ 080d2692 81b0
    ldr r1, DWORD_080d26b0                   @ 080d2694 0649
    ldr r2, DWORD_080d26b4                   @ 080d2696 074a
    adds r0,r1,r2    @ 080d2698 8818
    ldrb r0,[r0,#0x0]                        @ 080d269a 0078
    adds r5,r1,#0x0    @ 080d269c 0d1c
    cmp r0,#0x6                              @ 080d269e 0628
    bls LAB_080d26a4                         @ 080d26a0 00d9
    b LAB_080d29f4                           @ 080d26a2 a7e1
LAB_080d26a4:
    lsls r0,r0,#0x2    @ 080d26a4 8000
    ldr r1, PTR_PTR_080d26b8                 @ 080d26a6 0449
    adds r0,r0,r1    @ 080d26a8 4018
    ldr r0,[r0,#0x0]                         @ 080d26aa 0068
    .hword 0x4687    @ 080d26ac 8746
    .zero  0x2
DWORD_080d26b0:
    .word  0x02020160                     @ 080d26b0 60010202
DWORD_080d26b4:
    .word  0x00002f4e                     @ 080d26b4 4e2f0000
PTR_PTR_080d26b8:
    .word  0x080d26bc                     @ 080d26b8 bc260d08
PTR_DAT_080d26bc:
    .word  0x080d26d8                     @ 080d26bc d8260d08
    .word  0x080d26e4                     @ 080d26c0 e4260d08
    .word  0x080d2764                     @ 080d26c4 64270d08
    .word  0x080d2804                     @ 080d26c8 04280d08
    .word  0x080d2848                     @ 080d26cc 48280d08
    .word  0x080d29f4                     @ 080d26d0 f4290d08
    .word  0x080d29d4                     @ 080d26d4 d4290d08
DAT_080d26d8:
    ROM_INCBIN 0xd26d8, 0x31c
LAB_080d29f4:
    ldr r3, DWORD_080d2a04                   @ 080d29f4 034b
    adds r1,r5,r3    @ 080d29f6 e918
    movs r0,#0x0    @ 080d29f8 0020
    strb r0,[r1,#0x0]                        @ 080d29fa 0870
    add sp,#0x4                              @ 080d29fc 01b0
    pop {r4,r5,r6,r7}                        @ 080d29fe f0bc
    pop {r1}                                 @ 080d2a00 02bc
    bx r1                                    @ 080d2a02 0847
DWORD_080d2a04:
    .word  0x00002f4e                     @ 080d2a04 4e2f0000

@ Called by FUN_080d2ef4 at zone card attr-code=6 branch. Symmetric partner of dispatch_zone_card_anim_by_type (0x080d1bb4) using different row-offset field. Extracts bits[7:5] from gDuelCtx+0x2f53 and bits[4:0] from gDuelCtx+0x2f54 shifted left 3 to form type_combined [0..6]; if >6 jumps to LAB_080d2c54 (error path). Uses gDuelCtx+0x2f56 (vs 0x2f58 in primary) for row offset, validates zone index from gDuelCtx+0x2f4f. Indexes PTR_DAT_080d2aa0 (7-entry table), tail-calls via bx r8. Side effects: VRAM/OAM writes through 7 sub-handlers (INCBIN 0x080d2abc..0x080d2c54). Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_OFFSET=0x2f54; ROW_OFFSET=0x2f56; ZONE_OFFSET=0x2f4f; JUMP_TABLE_PTR=0x080d2a9c; TYPE_COUNT=7; LOW_MASK=0x1f.
dispatch_zone_card_anim_by_type_alt:
    push {r4,r5,lr}                          @ 080d2a08 30b5
    ldr r1, DWORD_080d2a44                   @ 080d2a0a 0e49
    ldr r2, DWORD_080d2a48                   @ 080d2a0c 0e4a
    adds r0,r1,r2    @ 080d2a0e 8818
    ldrb r0,[r0,#0x0]                        @ 080d2a10 0078
    lsrs r2,r0,#0x5    @ 080d2a12 4209
    ldr r4, DWORD_080d2a4c                   @ 080d2a14 0d4c
    adds r3,r1,r4    @ 080d2a16 0b19
    movs r0,#0x1f    @ 080d2a18 1f20
    ldrb r4,[r3,#0x0]                        @ 080d2a1a 1c78
    ands r0,r4    @ 080d2a1c 2040
    lsls r0,r0,#0x3    @ 080d2a1e c000
    orrs r0,r2    @ 080d2a20 1043
    adds r5,r1,#0x0    @ 080d2a22 0d1c
    cmp r0,#0x0                              @ 080d2a24 0028
    beq LAB_080d2a54                         @ 080d2a26 15d0
    ldr r1,[r3,#0x0]                         @ 080d2a28 1968
    lsls r1,r1,#0xb    @ 080d2a2a c902
    lsrs r1,r1,#0x18    @ 080d2a2c 090e
    ldr r2, DWORD_080d2a50                   @ 080d2a2e 084a
    adds r0,r5,r2    @ 080d2a30 a818
    ldrh r0,[r0,#0x0]                        @ 080d2a32 0088
    lsls r0,r0,#0x13    @ 080d2a34 c004
    lsrs r0,r0,#0x18    @ 080d2a36 000e
    adds r1,r1,r0    @ 080d2a38 0918
    lsls r1,r1,#0x1    @ 080d2a3a 4900
    movs r3,#0xa8    @ 080d2a3c a823
    lsls r3,r3,#0x6    @ 080d2a3e 9b01
    adds r0,r5,r3    @ 080d2a40 e818
    b LAB_080d2a6e                           @ 080d2a42 14e0
DWORD_080d2a44:
    .word  0x02020160                     @ 080d2a44 60010202
DWORD_080d2a48:
    .word  0x00002f53                     @ 080d2a48 532f0000
DWORD_080d2a4c:
    .word  0x00002f54                     @ 080d2a4c 542f0000
DWORD_080d2a50:
    .word  0x00002f56                     @ 080d2a50 562f0000
LAB_080d2a54:
    ldr r1,[r3,#0x0]                         @ 080d2a54 1968
    lsls r1,r1,#0xb    @ 080d2a56 c902
    lsrs r1,r1,#0x18    @ 080d2a58 090e
    ldr r4, DWORD_080d2a94                   @ 080d2a5a 0e4c
    adds r0,r5,r4    @ 080d2a5c 2819
    ldrh r0,[r0,#0x0]                        @ 080d2a5e 0088
    lsls r0,r0,#0x13    @ 080d2a60 c004
    lsrs r0,r0,#0x18    @ 080d2a62 000e
    adds r1,r1,r0    @ 080d2a64 0918
    lsls r1,r1,#0x1    @ 080d2a66 4900
    movs r2,#0xa0    @ 080d2a68 a022
    lsls r2,r2,#0x6    @ 080d2a6a 9201
    adds r0,r5,r2    @ 080d2a6c a818
LAB_080d2a6e:
    adds r1,r1,r0    @ 080d2a6e 0918
    ldrh r1,[r1,#0x0]                        @ 080d2a70 0988
    lsls r0,r1,#0x2    @ 080d2a72 8800
    adds r0,r0,r1    @ 080d2a74 4018
    lsls r0,r0,#0x3    @ 080d2a76 c000
    adds r0,r0,r5    @ 080d2a78 4019
    ldr r2,[r0,#0x0]                         @ 080d2a7a 0268
    ldr r3, DWORD_080d2a98                   @ 080d2a7c 064b
    adds r1,r5,r3    @ 080d2a7e e918
    ldrb r0,[r1,#0x0]                        @ 080d2a80 0878
    cmp r0,#0x6                              @ 080d2a82 0628
    bls LAB_080d2a88                         @ 080d2a84 00d9
    b LAB_080d2c54                           @ 080d2a86 e5e0
LAB_080d2a88:
    lsls r0,r0,#0x2    @ 080d2a88 8000
    ldr r1, PTR_PTR_080d2a9c                 @ 080d2a8a 0449
    adds r0,r0,r1    @ 080d2a8c 4018
    ldr r0,[r0,#0x0]                         @ 080d2a8e 0068
    .hword 0x4687    @ 080d2a90 8746
    .zero  0x2
DWORD_080d2a94:
    .word  0x00002f56                     @ 080d2a94 562f0000
DWORD_080d2a98:
    .word  0x00002f4f                     @ 080d2a98 4f2f0000
PTR_PTR_080d2a9c:
    .word  0x080d2aa0                     @ 080d2a9c a02a0d08
PTR_DAT_080d2aa0:
    .word  0x080d2abc                     @ 080d2aa0 bc2a0d08
    .word  0x080d2b2c                     @ 080d2aa4 2c2b0d08
    .word  0x080d2b48                     @ 080d2aa8 482b0d08
    .word  0x080d2b8c                     @ 080d2aac 8c2b0d08
    .word  0x080d2bc4                     @ 080d2ab0 c42b0d08
    .word  0x080d2bf4                     @ 080d2ab4 f42b0d08
    .word  0x080d2c18                     @ 080d2ab8 182c0d08
DAT_080d2abc:
    ROM_INCBIN 0xd2abc, 0x198
LAB_080d2c54:
    movs r0,#0x0    @ 080d2c54 0020
    strb r0,[r1,#0x0]                        @ 080d2c56 0870
    pop {r4,r5}                              @ 080d2c58 30bc
    pop {r1}                                 @ 080d2c5a 02bc
    bx r1                                    @ 080d2c5c 0847
    .zero  0x2

@ 4-state machine tick for duel field zone card detail view (indeg=1). Called by FUN_080d2ef4 (duel scene outer state machine). Reads [gDuelCtx+0x2f4e] view_state byte; dispatches: state=0 (fade-in): bl tick_duel_field_fadein_step; on done: open_card_info_page_from_list, set gFontState+0x0222 bit4, strh [WIN0H=0x04000004]=0x28f0, increment view_state. state=1 (card info page): bl tick_card_info_page_by_state; on done: increment view_state. state=2 (rebuild field): read slot card_id, bl init_duel_field_vram_layout, bl render_zone_card_detail_panel (0x080d08a4), bl check_zone_slot_attr_visible (0x080d0784), bl dispatch_zone_card_display_by_mode (0x080d0818), apply_palette_offset_to_tile_row, write WIN0H/WIN0V/WININ, increment view_state; return 1. state=3 (fade-out): bl tick_duel_field_fadeout_step; on done: clear gFontState+0x0222 bits[4:0], increment view_state; return 1. other: write [gDuelCtx+0x2f4e]=0 (reset), return 0. Returns r0: 1=state_advanced / 0=waiting_or_reset. Constants: DUEL_CTX=0x02020160; VIEW_STATE_OFFSET=0x2f4e; WIN0H=0x04000004; WIN0H_VAL=0x28f0; CARD_PAGE_BUF1=0x0203eeb0; CARD_PAGE_BUF2=0x02029eb0.
tick_zone_card_detail_view:
    push {r4,r5,lr}                          @ 080d2c60 30b5
    sub sp,#0x4                              @ 080d2c62 81b0
    ldr r0, DWORD_080d2c7c                   @ 080d2c64 0548
    ldr r1, DWORD_080d2c80                   @ 080d2c66 0649
    adds r5,r0,r1    @ 080d2c68 4518
    ldrb r2,[r5,#0x0]                        @ 080d2c6a 2a78
    adds r4,r0,#0x0    @ 080d2c6c 041c
    cmp r2,#0x1                              @ 080d2c6e 012a
    beq LAB_080d2d50                         @ 080d2c70 6ed0
    cmp r2,#0x1                              @ 080d2c72 012a
    bgt LAB_080d2c84                         @ 080d2c74 06dc
    cmp r2,#0x0                              @ 080d2c76 002a
    beq LAB_080d2c90                         @ 080d2c78 0ad0
    b LAB_080d2ee0                           @ 080d2c7a 31e1
DWORD_080d2c7c:
    .word  0x02020160                     @ 080d2c7c 60010202
DWORD_080d2c80:
    .word  0x00002f4e                     @ 080d2c80 4e2f0000
LAB_080d2c84:
    cmp r2,#0x2                              @ 080d2c84 022a
    beq LAB_080d2d62                         @ 080d2c86 6cd0
    cmp r2,#0x3                              @ 080d2c88 032a
    bne LAB_080d2c8e                         @ 080d2c8a 00d1
    b LAB_080d2eb8                           @ 080d2c8c 14e1
LAB_080d2c8e:
    b LAB_080d2ee0                           @ 080d2c8e 27e1
LAB_080d2c90:
    bl tick_duel_field_fadein_step           @ 080d2c90 f9f7e4fe
    cmp r0,#0x0                              @ 080d2c94 0028
    bne LAB_080d2c9a                         @ 080d2c96 00d1
    b LAB_080d2e98                           @ 080d2c98 fee0
LAB_080d2c9a:
    ldr r2, DWORD_080d2cd0                   @ 080d2c9a 0d4a
    adds r0,r4,r2    @ 080d2c9c a018
    ldrb r0,[r0,#0x0]                        @ 080d2c9e 0078
    lsrs r1,r0,#0x5    @ 080d2ca0 4109
    ldr r3, DWORD_080d2cd4                   @ 080d2ca2 0c4b
    adds r2,r4,r3    @ 080d2ca4 e218
    movs r0,#0x1f    @ 080d2ca6 1f20
    ldrb r3,[r2,#0x0]                        @ 080d2ca8 1378
    ands r0,r3    @ 080d2caa 1840
    lsls r0,r0,#0x3    @ 080d2cac c000
    orrs r0,r1    @ 080d2cae 0843
    cmp r0,#0x0                              @ 080d2cb0 0028
    beq LAB_080d2cdc                         @ 080d2cb2 13d0
    ldr r1,[r2,#0x0]                         @ 080d2cb4 1168
    lsls r1,r1,#0xb    @ 080d2cb6 c902
    lsrs r1,r1,#0x18    @ 080d2cb8 090e
    ldr r2, DWORD_080d2cd8                   @ 080d2cba 074a
    adds r0,r4,r2    @ 080d2cbc a018
    ldrh r0,[r0,#0x0]                        @ 080d2cbe 0088
    lsls r0,r0,#0x13    @ 080d2cc0 c004
    lsrs r0,r0,#0x18    @ 080d2cc2 000e
    adds r1,r1,r0    @ 080d2cc4 0918
    lsls r1,r1,#0x1    @ 080d2cc6 4900
    movs r3,#0xa8    @ 080d2cc8 a823
    lsls r3,r3,#0x6    @ 080d2cca 9b01
    b LAB_080d2cf4                           @ 080d2ccc 12e0
    .zero  0x2
DWORD_080d2cd0:
    .word  0x00002f53                     @ 080d2cd0 532f0000
DWORD_080d2cd4:
    .word  0x00002f54                     @ 080d2cd4 542f0000
DWORD_080d2cd8:
    .word  0x00002f56                     @ 080d2cd8 562f0000
LAB_080d2cdc:
    ldr r1,[r2,#0x0]                         @ 080d2cdc 1168
    lsls r1,r1,#0xb    @ 080d2cde c902
    lsrs r1,r1,#0x18    @ 080d2ce0 090e
    ldr r2, DWORD_080d2d34                   @ 080d2ce2 144a
    adds r0,r4,r2    @ 080d2ce4 a018
    ldrh r0,[r0,#0x0]                        @ 080d2ce6 0088
    lsls r0,r0,#0x13    @ 080d2ce8 c004
    lsrs r0,r0,#0x18    @ 080d2cea 000e
    adds r1,r1,r0    @ 080d2cec 0918
    lsls r1,r1,#0x1    @ 080d2cee 4900
    movs r3,#0xa0    @ 080d2cf0 a023
    lsls r3,r3,#0x6    @ 080d2cf2 9b01
LAB_080d2cf4:
    adds r0,r4,r3    @ 080d2cf4 e018
    adds r1,r1,r0    @ 080d2cf6 0918
    ldrh r1,[r1,#0x0]                        @ 080d2cf8 0988
    ldr r4, DWORD_080d2d38                   @ 080d2cfa 0f4c
    lsls r0,r1,#0x2    @ 080d2cfc 8800
    adds r0,r0,r1    @ 080d2cfe 4018
    lsls r0,r0,#0x3    @ 080d2d00 c000
    adds r0,r0,r4    @ 080d2d02 0019
    ldrh r0,[r0,#0x0]                        @ 080d2d04 0088
    ldr r2, DWORD_080d2d3c                   @ 080d2d06 0d4a
    ldr r3, DWORD_080d2d40                   @ 080d2d08 0d4b
    movs r1,#0x0    @ 080d2d0a 0021
    bl open_card_info_page_from_list         @ 080d2d0c 4bf7f2fc
    ldr r1, DWORD_080d2d44                   @ 080d2d10 0c49
    ldr r0, DWORD_080d2d48                   @ 080d2d12 0d48
    adds r1,r1,r0    @ 080d2d14 0918
    movs r0,#0x10    @ 080d2d16 1020
    ldrb r2,[r1,#0x0]                        @ 080d2d18 0a78
    orrs r0,r2    @ 080d2d1a 1043
    strb r0,[r1,#0x0]                        @ 080d2d1c 0870
    movs r1,#0x80    @ 080d2d1e 8021
    lsls r1,r1,#0x13    @ 080d2d20 c904
    movs r0,#0x0    @ 080d2d22 0020
    strh r0,[r1,#0x0]                        @ 080d2d24 0880
    ldr r3, DWORD_080d2d4c                   @ 080d2d26 094b
    adds r4,r4,r3    @ 080d2d28 e418
    ldrb r0,[r4,#0x0]                        @ 080d2d2a 2078
    adds r0,#0x1    @ 080d2d2c 0130
    strb r0,[r4,#0x0]                        @ 080d2d2e 2070
    b LAB_080d2e98                           @ 080d2d30 b2e0
    .zero  0x2
DWORD_080d2d34:
    .word  0x00002f56                     @ 080d2d34 562f0000
DWORD_080d2d38:
    .word  0x02020160                     @ 080d2d38 60010202
DWORD_080d2d3c:
    .word  0x0203eeb0                     @ 080d2d3c b0ee0302
DWORD_080d2d40:
    .word  0x02029eb0                     @ 080d2d40 b09e0202
DWORD_080d2d44:
    .word  0x02023130                     @ 080d2d44 30310202
DWORD_080d2d48:
    .word  0x00000222                     @ 080d2d48 22020000
DWORD_080d2d4c:
    .word  0x00002f4e                     @ 080d2d4c 4e2f0000
LAB_080d2d50:
    bl tick_card_info_page_by_state          @ 080d2d50 4bf7e0fc
    cmp r0,#0x0                              @ 080d2d54 0028
    bne LAB_080d2d5a                         @ 080d2d56 00d1
    b LAB_080d2e98                           @ 080d2d58 9ee0
LAB_080d2d5a:
    ldrb r0,[r5,#0x0]                        @ 080d2d5a 2878
    adds r0,#0x1    @ 080d2d5c 0130
    strb r0,[r5,#0x0]                        @ 080d2d5e 2870
    b LAB_080d2e98                           @ 080d2d60 9ae0
LAB_080d2d62:
    ldr r1, DWORD_080d2d98                   @ 080d2d62 0d49
    adds r0,r4,r1    @ 080d2d64 6018
    ldrb r0,[r0,#0x0]                        @ 080d2d66 0078
    lsrs r1,r0,#0x5    @ 080d2d68 4109
    ldr r3, DWORD_080d2d9c                   @ 080d2d6a 0c4b
    adds r2,r4,r3    @ 080d2d6c e218
    movs r0,#0x1f    @ 080d2d6e 1f20
    ldrb r3,[r2,#0x0]                        @ 080d2d70 1378
    ands r0,r3    @ 080d2d72 1840
    lsls r0,r0,#0x3    @ 080d2d74 c000
    orrs r0,r1    @ 080d2d76 0843
    cmp r0,#0x0                              @ 080d2d78 0028
    beq LAB_080d2da4                         @ 080d2d7a 13d0
    ldr r1,[r2,#0x0]                         @ 080d2d7c 1168
    lsls r1,r1,#0xb    @ 080d2d7e c902
    lsrs r1,r1,#0x18    @ 080d2d80 090e
    ldr r2, DWORD_080d2da0                   @ 080d2d82 074a
    adds r0,r4,r2    @ 080d2d84 a018
    ldrh r0,[r0,#0x0]                        @ 080d2d86 0088
    lsls r0,r0,#0x13    @ 080d2d88 c004
    lsrs r0,r0,#0x18    @ 080d2d8a 000e
    adds r1,r1,r0    @ 080d2d8c 0918
    lsls r1,r1,#0x1    @ 080d2d8e 4900
    movs r3,#0xa8    @ 080d2d90 a823
    lsls r3,r3,#0x6    @ 080d2d92 9b01
    b LAB_080d2dbc                           @ 080d2d94 12e0
    .zero  0x2
DWORD_080d2d98:
    .word  0x00002f53                     @ 080d2d98 532f0000
DWORD_080d2d9c:
    .word  0x00002f54                     @ 080d2d9c 542f0000
DWORD_080d2da0:
    .word  0x00002f56                     @ 080d2da0 562f0000
LAB_080d2da4:
    ldr r1,[r2,#0x0]                         @ 080d2da4 1168
    lsls r1,r1,#0xb    @ 080d2da6 c902
    lsrs r1,r1,#0x18    @ 080d2da8 090e
    ldr r2, DWORD_080d2e08                   @ 080d2daa 174a
    adds r0,r4,r2    @ 080d2dac a018
    ldrh r0,[r0,#0x0]                        @ 080d2dae 0088
    lsls r0,r0,#0x13    @ 080d2db0 c004
    lsrs r0,r0,#0x18    @ 080d2db2 000e
    adds r1,r1,r0    @ 080d2db4 0918
    lsls r1,r1,#0x1    @ 080d2db6 4900
    movs r3,#0xa0    @ 080d2db8 a023
    lsls r3,r3,#0x6    @ 080d2dba 9b01
LAB_080d2dbc:
    adds r0,r4,r3    @ 080d2dbc e018
    adds r1,r1,r0    @ 080d2dbe 0918
    ldrh r4,[r1,#0x0]                        @ 080d2dc0 0c88
    bl init_duel_field_vram_layout           @ 080d2dc2 f9f79ffd
    bl render_zone_card_detail_panel         @ 080d2dc6 fdf76dfd
    adds r0,r4,#0x0    @ 080d2dca 201c
    bl check_zone_slot_attr_visible          @ 080d2dcc fdf7dafc
    adds r1,r0,#0x0    @ 080d2dd0 011c
    adds r0,r4,#0x0    @ 080d2dd2 201c
    bl dispatch_zone_card_display_by_mode    @ 080d2dd4 fdf720fd
    ldr r3, DWORD_080d2e0c                   @ 080d2dd8 0c4b
    ldr r1, DWORD_080d2e10                   @ 080d2dda 0d49
    adds r0,r3,r1    @ 080d2ddc 5818
    ldrb r0,[r0,#0x0]                        @ 080d2dde 0078
    lsrs r2,r0,#0x5    @ 080d2de0 4209
    ldr r0, DWORD_080d2e14                   @ 080d2de2 0c48
    adds r1,r3,r0    @ 080d2de4 1918
    movs r4,#0x1f    @ 080d2de6 1f24
    adds r0,r4,#0x0    @ 080d2de8 201c
    ldrb r1,[r1,#0x0]                        @ 080d2dea 0978
    ands r0,r1    @ 080d2dec 0840
    lsls r0,r0,#0x3    @ 080d2dee c000
    orrs r0,r2    @ 080d2df0 1043
    cmp r0,#0x0                              @ 080d2df2 0028
    beq LAB_080d2e1c                         @ 080d2df4 12d0
    ldr r1, DWORD_080d2e18                   @ 080d2df6 0849
    adds r0,r3,r1    @ 080d2df8 5818
    ldrh r0,[r0,#0x0]                        @ 080d2dfa 0088
    lsls r0,r0,#0x13    @ 080d2dfc c004
    lsrs r0,r0,#0x18    @ 080d2dfe 000e
    cmp r0,#0x5                              @ 080d2e00 0528
    bgt LAB_080d2e36                         @ 080d2e02 18dc
    b LAB_080d2e60                           @ 080d2e04 2ce0
    .zero  0x2
DWORD_080d2e08:
    .word  0x00002f56                     @ 080d2e08 562f0000
DWORD_080d2e0c:
    .word  0x02020160                     @ 080d2e0c 60010202
DWORD_080d2e10:
    .word  0x00002f53                     @ 080d2e10 532f0000
DWORD_080d2e14:
    .word  0x00002f54                     @ 080d2e14 542f0000
DWORD_080d2e18:
    .word  0x00002f58                     @ 080d2e18 582f0000
LAB_080d2e1c:
    ldr r2, DWORD_080d2e4c                   @ 080d2e1c 0b4a
    adds r0,r3,r2    @ 080d2e1e 9818
    ldrb r0,[r0,#0x0]                        @ 080d2e20 0078
    lsrs r2,r0,#0x5    @ 080d2e22 4209
    ldr r0, DWORD_080d2e50                   @ 080d2e24 0a48
    adds r1,r3,r0    @ 080d2e26 1918
    adds r0,r4,#0x0    @ 080d2e28 201c
    ldrb r1,[r1,#0x0]                        @ 080d2e2a 0978
    ands r0,r1    @ 080d2e2c 0840
    lsls r0,r0,#0x3    @ 080d2e2e c000
    orrs r0,r2    @ 080d2e30 1043
    cmp r0,#0x5                              @ 080d2e32 0528
    ble LAB_080d2e60                         @ 080d2e34 14dd
LAB_080d2e36:
    ldr r0, DWORD_080d2e54                   @ 080d2e36 0748
    ldr r1, DWORD_080d2e58                   @ 080d2e38 0749
    ldr r2, DWORD_080d2e5c                   @ 080d2e3a 084a
    movs r3,#0xc3    @ 080d2e3c c323
    lsls r3,r3,#0x1    @ 080d2e3e 5b00
    str r3,[sp,#0x0]                         @ 080d2e40 0093
    movs r3,#0xb    @ 080d2e42 0b23
    bl apply_palette_offset_to_tile_row      @ 080d2e44 1bf0b0fa
    b LAB_080d2e72                           @ 080d2e48 13e0
    .zero  0x2
DWORD_080d2e4c:
    .word  0x00002f57                     @ 080d2e4c 572f0000
DWORD_080d2e50:
    .word  0x00002f58                     @ 080d2e50 582f0000
DWORD_080d2e54:
    .word  0x0600f08a                     @ 080d2e54 8af00006
DWORD_080d2e58:
    .word  0x0988b434                     @ 080d2e58 34b48809
DWORD_080d2e5c:
    .word  0x00000e19                     @ 080d2e5c 190e0000
LAB_080d2e60:
    ldr r0, DWORD_080d2e9c                   @ 080d2e60 0e48
    ldr r1, DWORD_080d2ea0                   @ 080d2e62 0f49
    ldr r2, DWORD_080d2ea4                   @ 080d2e64 0f4a
    movs r3,#0xc3    @ 080d2e66 c323
    lsls r3,r3,#0x1    @ 080d2e68 5b00
    str r3,[sp,#0x0]                         @ 080d2e6a 0093
    movs r3,#0xb    @ 080d2e6c 0b23
    bl apply_palette_offset_to_tile_row      @ 080d2e6e 1bf09bfa
LAB_080d2e72:
    ldr r1, DWORD_080d2ea8                   @ 080d2e72 0d49
    ldr r2, DWORD_080d2eac                   @ 080d2e74 0d4a
    adds r0,r2,#0x0    @ 080d2e76 101c
    strh r0,[r1,#0x0]                        @ 080d2e78 0880
    adds r1,#0x4    @ 080d2e7a 0431
    movs r0,#0x90    @ 080d2e7c 9020
    strh r0,[r1,#0x0]                        @ 080d2e7e 0880
    adds r1,#0x4    @ 080d2e80 0431
    movs r0,#0x1d    @ 080d2e82 1d20
    strh r0,[r1,#0x0]                        @ 080d2e84 0880
    adds r1,#0x2    @ 080d2e86 0231
    movs r0,#0x3f    @ 080d2e88 3f20
    strh r0,[r1,#0x0]                        @ 080d2e8a 0880
    ldr r0, DWORD_080d2eb0                   @ 080d2e8c 0848
    ldr r3, DWORD_080d2eb4                   @ 080d2e8e 094b
    adds r0,r0,r3    @ 080d2e90 c018
    ldrb r1,[r0,#0x0]                        @ 080d2e92 0178
    adds r1,#0x1    @ 080d2e94 0131
    strb r1,[r0,#0x0]                        @ 080d2e96 0170
LAB_080d2e98:
    movs r0,#0x1    @ 080d2e98 0120
    b LAB_080d2ee8                           @ 080d2e9a 25e0
DWORD_080d2e9c:
    .word  0x0600f08a                     @ 080d2e9c 8af00006
DWORD_080d2ea0:
    .word  0x0988b178                     @ 080d2ea0 78b18809
DWORD_080d2ea4:
    .word  0x00000e19                     @ 080d2ea4 190e0000
DWORD_080d2ea8:
    .word  WIN0H                          @ 080d2ea8 40000004
DWORD_080d2eac:
    .word  0x000028f0                     @ 080d2eac f0280000
DWORD_080d2eb0:
    .word  0x02020160                     @ 080d2eb0 60010202
DWORD_080d2eb4:
    .word  0x00002f4e                     @ 080d2eb4 4e2f0000
LAB_080d2eb8:
    bl tick_duel_field_fadeout_step          @ 080d2eb8 f9f7befd
    cmp r0,#0x0                              @ 080d2ebc 0028
    beq LAB_080d2e98                         @ 080d2ebe ebd0
    ldr r0, DWORD_080d2ed8                   @ 080d2ec0 0548
    ldr r1, DWORD_080d2edc                   @ 080d2ec2 0649
    adds r0,r0,r1    @ 080d2ec4 4018
    movs r1,#0x11    @ 080d2ec6 1121
    rsbs r1,r1,#0    @ 080d2ec8 4942
    ldrb r2,[r0,#0x0]                        @ 080d2eca 0278
    ands r1,r2    @ 080d2ecc 1140
    strb r1,[r0,#0x0]                        @ 080d2ece 0170
    ldrb r0,[r5,#0x0]                        @ 080d2ed0 2878
    adds r0,#0x1    @ 080d2ed2 0130
    strb r0,[r5,#0x0]                        @ 080d2ed4 2870
    b LAB_080d2e98                           @ 080d2ed6 dfe7
DWORD_080d2ed8:
    .word  0x02023130                     @ 080d2ed8 30310202
DWORD_080d2edc:
    .word  0x00000222                     @ 080d2edc 22020000
LAB_080d2ee0:
    ldr r3, DWORD_080d2ef0                   @ 080d2ee0 034b
    adds r1,r4,r3    @ 080d2ee2 e118
    movs r0,#0x0    @ 080d2ee4 0020
    strb r0,[r1,#0x0]                        @ 080d2ee6 0870
LAB_080d2ee8:
    add sp,#0x4                              @ 080d2ee8 01b0
    pop {r4,r5}                              @ 080d2eea 30bc
    pop {r1}                                 @ 080d2eec 02bc
    bx r1                                    @ 080d2eee 0847
DWORD_080d2ef0:
    .word  0x00002f4e                     @ 080d2ef0 4e2f0000

@ Single-frame update of zone card list view; dispatches to sub-systems by gDuelCtx state. Called by invert_zone_tick_result (0x080cc340) in zone tick main loop. No explicit params; all state from gDuelCtx global. Flow: (1) reads gDuelCtx+0x2f53/0x2f54 type_combined (bits[7:5]<<3 | bits[4:0]); if >0 and <=5 calls dispatch_zone_card_anim_by_subtype + signal_zone_tick_done, clears gDuelCtx+0x2f54 bits (& 0xffffe01f), calls signal_zone_tick_done again. (2) type=4: calls dispatch_zone_card_anim_by_subtype; type=5: calls tick_zone_card_detail_view -> signal; type=6: calls dispatch_zone_card_anim_by_type_alt -> signal. (3) other: if gDuelCtx+0x2f54 bits[12:5] set calls render_zone_card_anim_dual_pass; type=1: advance_zone_card_anim; final calls exit_zone_tick_frame + tick_zone_card_list_state_machine (0x080d4478). Side effects: strh gDuelCtx+0x2f54 &= 0xffffe01f (multiple); signal_zone_tick_done/exit_zone_tick_frame indirect effects.
tick_zone_card_list_view:
    push {r4,r5,r6,r7,lr}                    @ 080d2ef4 f0b5
    ldr r1, DWORD_080d2f28                   @ 080d2ef6 0c49
    ldr r2, DWORD_080d2f2c                   @ 080d2ef8 0c4a
    adds r0,r1,r2    @ 080d2efa 8818
    ldrb r0,[r0,#0x0]                        @ 080d2efc 0078
    lsrs r3,r0,#0x5    @ 080d2efe 4309
    ldr r4, DWORD_080d2f30                   @ 080d2f00 0b4c
    adds r2,r1,r4    @ 080d2f02 0a19
    movs r4,#0x1f    @ 080d2f04 1f24
    adds r0,r4,#0x0    @ 080d2f06 201c
    ldrb r2,[r2,#0x0]                        @ 080d2f08 1278
    ands r0,r2    @ 080d2f0a 1040
    lsls r0,r0,#0x3    @ 080d2f0c c000
    orrs r0,r3    @ 080d2f0e 1843
    adds r7,r1,#0x0    @ 080d2f10 0f1c
    cmp r0,#0x0                              @ 080d2f12 0028
    beq LAB_080d2f38                         @ 080d2f14 10d0
    ldr r1, DWORD_080d2f34                   @ 080d2f16 0749
    adds r0,r7,r1    @ 080d2f18 7818
    ldrh r0,[r0,#0x0]                        @ 080d2f1a 0088
    lsls r0,r0,#0x13    @ 080d2f1c c004
    lsrs r0,r0,#0x18    @ 080d2f1e 000e
    cmp r0,#0x5                              @ 080d2f20 0528
    ble LAB_080d2f52                         @ 080d2f22 16dd
    b LAB_080d2fac                           @ 080d2f24 42e0
    .zero  0x2
DWORD_080d2f28:
    .word  0x02020160                     @ 080d2f28 60010202
DWORD_080d2f2c:
    .word  0x00002f53                     @ 080d2f2c 532f0000
DWORD_080d2f30:
    .word  0x00002f54                     @ 080d2f30 542f0000
DWORD_080d2f34:
    .word  0x00002f58                     @ 080d2f34 582f0000
LAB_080d2f38:
    ldr r2, DWORD_080d2f7c                   @ 080d2f38 104a
    adds r0,r7,r2    @ 080d2f3a b818
    ldrb r0,[r0,#0x0]                        @ 080d2f3c 0078
    lsrs r2,r0,#0x5    @ 080d2f3e 4209
    ldr r3, DWORD_080d2f80                   @ 080d2f40 0f4b
    adds r1,r7,r3    @ 080d2f42 f918
    adds r0,r4,#0x0    @ 080d2f44 201c
    ldrb r1,[r1,#0x0]                        @ 080d2f46 0978
    ands r0,r1    @ 080d2f48 0840
    lsls r0,r0,#0x3    @ 080d2f4a c000
    orrs r0,r2    @ 080d2f4c 1043
    cmp r0,#0x5                              @ 080d2f4e 0528
    bgt LAB_080d2fac                         @ 080d2f50 2cdc
LAB_080d2f52:
    ldr r4, DWORD_080d2f84                   @ 080d2f52 0c4c
    adds r0,r7,r4    @ 080d2f54 3819
    ldrb r0,[r0,#0x0]                        @ 080d2f56 0078
    lsrs r2,r0,#0x5    @ 080d2f58 4209
    ldr r0, DWORD_080d2f88                   @ 080d2f5a 0b48
    adds r1,r7,r0    @ 080d2f5c 3918
    movs r3,#0x1f    @ 080d2f5e 1f23
    adds r0,r3,#0x0    @ 080d2f60 181c
    ldrb r1,[r1,#0x0]                        @ 080d2f62 0978
    ands r0,r1    @ 080d2f64 0840
    lsls r0,r0,#0x3    @ 080d2f66 c000
    orrs r0,r2    @ 080d2f68 1043
    cmp r0,#0x0                              @ 080d2f6a 0028
    beq LAB_080d2f8c                         @ 080d2f6c 0ed0
    ldr r1, DWORD_080d2f80                   @ 080d2f6e 0449
    adds r0,r7,r1    @ 080d2f70 7818
    ldrh r0,[r0,#0x0]                        @ 080d2f72 0088
    lsls r0,r0,#0x13    @ 080d2f74 c004
    lsrs r6,r0,#0x18    @ 080d2f76 060e
    b LAB_080d2fae                           @ 080d2f78 19e0
    .zero  0x2
DWORD_080d2f7c:
    .word  0x00002f57                     @ 080d2f7c 572f0000
DWORD_080d2f80:
    .word  0x00002f58                     @ 080d2f80 582f0000
DWORD_080d2f84:
    .word  0x00002f53                     @ 080d2f84 532f0000
DWORD_080d2f88:
    .word  0x00002f54                     @ 080d2f88 542f0000
LAB_080d2f8c:
    ldr r2, DWORD_080d2fa4                   @ 080d2f8c 054a
    adds r0,r7,r2    @ 080d2f8e b818
    ldrb r0,[r0,#0x0]                        @ 080d2f90 0078
    lsrs r2,r0,#0x5    @ 080d2f92 4209
    ldr r4, DWORD_080d2fa8                   @ 080d2f94 044c
    adds r1,r7,r4    @ 080d2f96 3919
    adds r0,r3,#0x0    @ 080d2f98 181c
    ldrb r1,[r1,#0x0]                        @ 080d2f9a 0978
    ands r0,r1    @ 080d2f9c 0840
    lsls r6,r0,#0x3    @ 080d2f9e c600
    orrs r6,r2    @ 080d2fa0 1643
    b LAB_080d2fae                           @ 080d2fa2 04e0
DWORD_080d2fa4:
    .word  0x00002f57                     @ 080d2fa4 572f0000
DWORD_080d2fa8:
    .word  0x00002f58                     @ 080d2fa8 582f0000
LAB_080d2fac:
    movs r6,#0x5    @ 080d2fac 0526
LAB_080d2fae:
    ldr r0, DWORD_080d2fc8                   @ 080d2fae 0648
    adds r4,r7,r0    @ 080d2fb0 3c18
    ldrh r1,[r4,#0x0]                        @ 080d2fb2 2188
    lsls r0,r1,#0x13    @ 080d2fb4 c804
    lsrs r0,r0,#0x18    @ 080d2fb6 000e
    cmp r0,#0x5                              @ 080d2fb8 0528
    beq LAB_080d2ff0                         @ 080d2fba 19d0
    cmp r0,#0x5                              @ 080d2fbc 0528
    bgt LAB_080d2fcc                         @ 080d2fbe 05dc
    cmp r0,#0x4                              @ 080d2fc0 0428
    beq LAB_080d2fd2                         @ 080d2fc2 06d0
    b LAB_080d3028                           @ 080d2fc4 30e0
    .zero  0x2
DWORD_080d2fc8:
    .word  0x00002f54                     @ 080d2fc8 542f0000
LAB_080d2fcc:
    cmp r0,#0x6                              @ 080d2fcc 0628
    beq LAB_080d300c                         @ 080d2fce 1dd0
    b LAB_080d3028                           @ 080d2fd0 2ae0
LAB_080d2fd2:
    bl dispatch_zone_card_anim_by_subtype    @ 080d2fd2 fff75dfb
    cmp r0,#0x0                              @ 080d2fd6 0028
    beq LAB_080d2fde                         @ 080d2fd8 01d0
    bl signal_zone_tick_done                 @ 080d2fda 00f024fc
LAB_080d2fde:
    ldr r0, DWORD_080d2fec                   @ 080d2fde 0348
    ldrh r2,[r4,#0x0]                        @ 080d2fe0 2288
    ands r0,r2    @ 080d2fe2 1040
    strh r0,[r4,#0x0]                        @ 080d2fe4 2080
    bl signal_zone_tick_done                 @ 080d2fe6 00f01efc
    movs r0,r0    @ 080d2fea 0000
DWORD_080d2fec:
    .word  0xffffe01f                     @ 080d2fec 1fe0ffff
LAB_080d2ff0:
    bl tick_zone_card_detail_view            @ 080d2ff0 fff736fe
    cmp r0,#0x0                              @ 080d2ff4 0028
    beq LAB_080d2ffc                         @ 080d2ff6 01d0
    bl signal_zone_tick_done                 @ 080d2ff8 00f015fc
LAB_080d2ffc:
    ldr r0, DWORD_080d3008                   @ 080d2ffc 0248
    ldrh r3,[r4,#0x0]                        @ 080d2ffe 2388
    ands r0,r3    @ 080d3000 1840
    strh r0,[r4,#0x0]                        @ 080d3002 2080
    bl signal_zone_tick_done                 @ 080d3004 00f00ffc
DWORD_080d3008:
    .word  0xffffe01f                     @ 080d3008 1fe0ffff
LAB_080d300c:
    bl dispatch_zone_card_anim_by_type_alt   @ 080d300c fff7fcfc
    cmp r0,#0x0                              @ 080d3010 0028
    beq LAB_080d3018                         @ 080d3012 01d0
    bl signal_zone_tick_done                 @ 080d3014 00f007fc
LAB_080d3018:
    ldr r0, DWORD_080d3024                   @ 080d3018 0248
    ldrh r1,[r4,#0x0]                        @ 080d301a 2188
    ands r0,r1    @ 080d301c 0840
    strh r0,[r4,#0x0]                        @ 080d301e 2080
    bl signal_zone_tick_done                 @ 080d3020 00f001fc
DWORD_080d3024:
    .word  0xffffe01f                     @ 080d3024 1fe0ffff
LAB_080d3028:
    ldr r2, DWORD_080d3050                   @ 080d3028 094a
    adds r1,r7,r2    @ 080d302a b918
    movs r0,#0xff    @ 080d302c ff20
    lsls r0,r0,#0x5    @ 080d302e 4001
    ldrh r1,[r1,#0x0]                        @ 080d3030 0988
    ands r0,r1    @ 080d3032 0840
    cmp r0,#0x80                             @ 080d3034 8028
    beq LAB_080d305c                         @ 080d3036 11d0
    ldr r1, DWORD_080d3054                   @ 080d3038 0649
    ldr r3, DWORD_080d3058                   @ 080d303a 074b
    adds r1,r1,r3    @ 080d303c c918
    movs r0,#0xc    @ 080d303e 0c20
    ldrb r1,[r1,#0x0]                        @ 080d3040 0978
    ands r0,r1    @ 080d3042 0840
    cmp r0,#0x0                              @ 080d3044 0028
    beq LAB_080d305c                         @ 080d3046 09d0
LAB_080d3048:
    movs r0,#0x0    @ 080d3048 0020
    bl exit_zone_tick_frame                  @ 080d304a 00f0edfb
    movs r0,r0    @ 080d304e 0000
DWORD_080d3050:
    .word  0x00002f54                     @ 080d3050 542f0000
DWORD_080d3054:
    .word  0x02023130                     @ 080d3054 30310202
DWORD_080d3058:
    .word  0x00000222                     @ 080d3058 22020000
LAB_080d305c:
    bl render_zone_card_anim_dual_pass       @ 080d305c fef766fd
    ldr r5, DWORD_080d3084                   @ 080d3060 084d
    ldr r4, DWORD_080d3088                   @ 080d3062 094c
    adds r3,r5,r4    @ 080d3064 2b19
    ldrh r2,[r3,#0x0]                        @ 080d3066 1a88
    lsls r0,r2,#0x13    @ 080d3068 d004
    lsrs r0,r0,#0x18    @ 080d306a 000e
    cmp r0,#0x1                              @ 080d306c 0128
    bne LAB_080d3074                         @ 080d306e 01d1
    bl advance_zone_card_anim                @ 080d3070 00f0d6fb
LAB_080d3074:
    cmp r0,#0x1                              @ 080d3074 0128
    bgt LAB_080d308c                         @ 080d3076 09dc
    cmp r0,#0x0                              @ 080d3078 0028
    bne LAB_080d307e                         @ 080d307a 00d1
    b LAB_080d31dc                           @ 080d307c aee0
LAB_080d307e:
    bl signal_zone_tick_done                 @ 080d307e 00f0d2fb
    movs r0,r0    @ 080d3082 0000
DWORD_080d3084:
    .word  0x02020160                     @ 080d3084 60010202
DWORD_080d3088:
    .word  0x00002f54                     @ 080d3088 542f0000
LAB_080d308c:
    cmp r0,#0x2                              @ 080d308c 0228
    bne LAB_080d3092                         @ 080d308e 00d1
    b LAB_080d381a                           @ 080d3090 c3e3
LAB_080d3092:
    cmp r0,#0x3                              @ 080d3092 0328
    beq LAB_080d3098                         @ 080d3094 00d0
    b signal_zone_tick_done                  @ 080d3096 c6e3
LAB_080d3098:
    ldr r0, DWORD_080d30b8                   @ 080d3098 0748
    movs r1,#0xa4    @ 080d309a a421
    lsls r1,r1,#0x1    @ 080d309c 4900
    adds r0,r0,r1    @ 080d309e 4018
    ldrh r1,[r0,#0x0]                        @ 080d30a0 0188
    movs r0,#0x40    @ 080d30a2 4020
    ands r0,r1    @ 080d30a4 0840
    cmp r0,#0x0                              @ 080d30a6 0028
    beq LAB_080d30c0                         @ 080d30a8 0ad0
    ldr r0, DWORD_080d30bc                   @ 080d30aa 0448
    ands r0,r2    @ 080d30ac 1040
LAB_080d30ae:
    strh r0,[r3,#0x0]                        @ 080d30ae 1880
LAB_080d30b0:
    movs r0,#0x0    @ 080d30b0 0020
    bl sync_state_and_init_sprite            @ 080d30b2 26f0fffc
    b signal_zone_tick_done                  @ 080d30b6 b6e3
DWORD_080d30b8:
    .word  gPrng                          @ 080d30b8 40000003
DWORD_080d30bc:
    .word  0xffffe01f                     @ 080d30bc 1fe0ffff
LAB_080d30c0:
    movs r0,#0x80    @ 080d30c0 8020
    ands r0,r1    @ 080d30c2 0840
    cmp r0,#0x0                              @ 080d30c4 0028
    beq LAB_080d30d8                         @ 080d30c6 07d0
    ldr r0, DWORD_080d30d4                   @ 080d30c8 0248
    ands r0,r2    @ 080d30ca 1040
    movs r1,#0x40    @ 080d30cc 4021
    orrs r0,r1    @ 080d30ce 0843
    b LAB_080d30ae                           @ 080d30d0 ede7
    .zero  0x2
DWORD_080d30d4:
    .word  0xffffe01f                     @ 080d30d4 1fe0ffff
LAB_080d30d8:
    movs r0,#0x1    @ 080d30d8 0120
    ands r0,r1    @ 080d30da 0840
    cmp r0,#0x0                              @ 080d30dc 0028
    beq LAB_080d31c4                         @ 080d30de 71d0
    movs r4,#0x0    @ 080d30e0 0024
    movs r2,#0xb9    @ 080d30e2 b922
    lsls r2,r2,#0x6    @ 080d30e4 9201
    adds r0,r5,r2    @ 080d30e6 a818
    ldrb r3,[r0,#0x0]                        @ 080d30e8 0378
    cmp r4,r3                                @ 080d30ea 9c42
    bge LAB_080d310c                         @ 080d30ec 0eda
    adds r6,r5,#0x0    @ 080d30ee 2e1c
    adds r5,r0,#0x0    @ 080d30f0 051c
LAB_080d30f2:
    lsls r0,r4,#0x1    @ 080d30f2 6000
    movs r2,#0xb8    @ 080d30f4 b822
    lsls r2,r2,#0x6    @ 080d30f6 9201
    adds r1,r6,r2    @ 080d30f8 b118
    adds r0,r0,r1    @ 080d30fa 4018
    ldrh r0,[r0,#0x0]                        @ 080d30fc 0088
    adds r4,#0x1    @ 080d30fe 0134
    adds r1,r4,#0x0    @ 080d3100 211c
    bl set_tile_palette_index_in_buf         @ 080d3102 c1f71dfa
    ldrb r3,[r5,#0x0]                        @ 080d3106 2b78
    cmp r4,r3                                @ 080d3108 9c42
    blt LAB_080d30f2                         @ 080d310a f2db
LAB_080d310c:
    ldr r0, DWORD_080d3124                   @ 080d310c 0548
    ldr r0,[r0,#0x4]                         @ 080d310e 4068
    cmp r0,#0x6                              @ 080d3110 0628
    bne LAB_080d312c                         @ 080d3112 0bd1
    ldr r0, DWORD_080d3128                   @ 080d3114 0448
    movs r4,#0xb8    @ 080d3116 b824
    lsls r4,r4,#0x6    @ 080d3118 a401
    adds r0,r0,r4    @ 080d311a 0019
    ldrh r0,[r0,#0x0]                        @ 080d311c 0088
    bl write_effect_ctx_slot_index           @ 080d311e c1f7d7f8
    b LAB_080d319e                           @ 080d3122 3ce0
DWORD_080d3124:
    .word  0x0201e4f0                     @ 080d3124 f0e40102
DWORD_080d3128:
    .word  0x02020160                     @ 080d3128 60010202
LAB_080d312c:
    ldr r3, DWORD_080d316c                   @ 080d312c 0f4b
    ldr r1, DWORD_080d3170                   @ 080d312e 1049
    adds r0,r3,r1    @ 080d3130 5818
    ldrb r0,[r0,#0x0]                        @ 080d3132 0078
    lsrs r1,r0,#0x5    @ 080d3134 4109
    ldr r4, DWORD_080d3174                   @ 080d3136 0f4c
    adds r2,r3,r4    @ 080d3138 1a19
    movs r0,#0x1f    @ 080d313a 1f20
    ldrb r4,[r2,#0x0]                        @ 080d313c 1478
    ands r0,r4    @ 080d313e 2040
    lsls r0,r0,#0x3    @ 080d3140 c000
    orrs r0,r1    @ 080d3142 0843
    cmp r0,#0x0                              @ 080d3144 0028
    beq LAB_080d317c                         @ 080d3146 19d0
    ldr r1,[r2,#0x0]                         @ 080d3148 1168
    lsls r1,r1,#0xb    @ 080d314a c902
    lsrs r1,r1,#0x18    @ 080d314c 090e
    ldr r2, DWORD_080d3178                   @ 080d314e 0a4a
    adds r0,r3,r2    @ 080d3150 9818
    ldrh r0,[r0,#0x0]                        @ 080d3152 0088
    lsls r0,r0,#0x13    @ 080d3154 c004
    lsrs r0,r0,#0x18    @ 080d3156 000e
    adds r1,r1,r0    @ 080d3158 0918
    lsls r1,r1,#0x1    @ 080d315a 4900
    movs r4,#0xa8    @ 080d315c a824
    lsls r4,r4,#0x6    @ 080d315e a401
    adds r0,r3,r4    @ 080d3160 1819
    adds r1,r1,r0    @ 080d3162 0918
    ldrh r0,[r1,#0x0]                        @ 080d3164 0888
    bl write_effect_ctx_slot_index           @ 080d3166 c1f7b3f8
    b LAB_080d319e                           @ 080d316a 18e0
DWORD_080d316c:
    .word  0x02020160                     @ 080d316c 60010202
DWORD_080d3170:
    .word  0x00002f53                     @ 080d3170 532f0000
DWORD_080d3174:
    .word  0x00002f54                     @ 080d3174 542f0000
DWORD_080d3178:
    .word  0x00002f56                     @ 080d3178 562f0000
LAB_080d317c:
    ldr r1,[r2,#0x0]                         @ 080d317c 1168
    lsls r1,r1,#0xb    @ 080d317e c902
    lsrs r1,r1,#0x18    @ 080d3180 090e
    ldr r2, DWORD_080d31b8                   @ 080d3182 0d4a
    adds r0,r3,r2    @ 080d3184 9818
    ldrh r0,[r0,#0x0]                        @ 080d3186 0088
    lsls r0,r0,#0x13    @ 080d3188 c004
    lsrs r0,r0,#0x18    @ 080d318a 000e
    adds r1,r1,r0    @ 080d318c 0918
    lsls r1,r1,#0x1    @ 080d318e 4900
    movs r4,#0xa0    @ 080d3190 a024
    lsls r4,r4,#0x6    @ 080d3192 a401
    adds r0,r3,r4    @ 080d3194 1819
    adds r1,r1,r0    @ 080d3196 0918
    ldrh r0,[r1,#0x0]                        @ 080d3198 0888
    bl write_effect_ctx_slot_index           @ 080d319a c1f799f8
LAB_080d319e:
    ldr r0, DWORD_080d31bc                   @ 080d319e 0748
    movs r1,#0xea    @ 080d31a0 ea21
    lsls r1,r1,#0x5    @ 080d31a2 4901
    adds r0,r0,r1    @ 080d31a4 4018
    ldr r1, DWORD_080d31c0                   @ 080d31a6 0649
    movs r2,#0xb9    @ 080d31a8 b922
    lsls r2,r2,#0x6    @ 080d31aa 9201
    adds r1,r1,r2    @ 080d31ac 8918
    ldrb r1,[r1,#0x0]                        @ 080d31ae 0978
    str r1,[r0,#0x0]                         @ 080d31b0 0160
    movs r0,#0x24    @ 080d31b2 2420
    b LAB_080d37d6                           @ 080d31b4 0fe3
    .zero  0x2
DWORD_080d31b8:
    .word  0x00002f56                     @ 080d31b8 562f0000
DWORD_080d31bc:
    .word  gP1LifePoints                  @ 080d31bc e0c40102
DWORD_080d31c0:
    .word  0x02020160                     @ 080d31c0 60010202
LAB_080d31c4:
    movs r0,#0x2    @ 080d31c4 0220
    ands r0,r1    @ 080d31c6 0840
    cmp r0,#0x0                              @ 080d31c8 0028
    bne LAB_080d31ce                         @ 080d31ca 00d1
    b signal_zone_tick_done                  @ 080d31cc 2be3
LAB_080d31ce:
    ldr r0, DWORD_080d31d8                   @ 080d31ce 0248
    ands r0,r2    @ 080d31d0 1040
    strh r0,[r3,#0x0]                        @ 080d31d2 1880
    b signal_zone_tick_done                  @ 080d31d4 27e3
    .zero  0x2
DWORD_080d31d8:
    .word  0xffffe01f                     @ 080d31d8 1fe0ffff
LAB_080d31dc:
    ldr r0, DWORD_080d31fc                   @ 080d31dc 0748
    movs r4,#0xa4    @ 080d31de a424
    lsls r4,r4,#0x1    @ 080d31e0 6400
    adds r0,r0,r4    @ 080d31e2 0019
    ldrh r1,[r0,#0x0]                        @ 080d31e4 0188
    movs r0,#0x80    @ 080d31e6 8020
    lsls r0,r0,#0x2    @ 080d31e8 8000
    ands r0,r1    @ 080d31ea 0840
    cmp r0,#0x0                              @ 080d31ec 0028
    beq LAB_080d3204                         @ 080d31ee 09d0
    ldr r0, DWORD_080d3200                   @ 080d31f0 0348
    ands r0,r2    @ 080d31f2 1040
    movs r1,#0x80    @ 080d31f4 8021
    orrs r0,r1    @ 080d31f6 0843
    strh r0,[r3,#0x0]                        @ 080d31f8 1880
    b signal_zone_tick_done                  @ 080d31fa 14e3
DWORD_080d31fc:
    .word  gPrng                          @ 080d31fc 40000003
DWORD_080d3200:
    .word  0xffffe01f                     @ 080d3200 1fe0ffff
LAB_080d3204:
    movs r0,#0x80    @ 080d3204 8020
    lsls r0,r0,#0x1    @ 080d3206 4000
    ands r0,r1    @ 080d3208 0840
    cmp r0,#0x0                              @ 080d320a 0028
    beq LAB_080d3290                         @ 080d320c 40d0
    ldr r1, DWORD_080d3240                   @ 080d320e 0c49
    adds r0,r5,r1    @ 080d3210 6818
    ldrb r0,[r0,#0x0]                        @ 080d3212 0078
    lsrs r1,r0,#0x5    @ 080d3214 4109
    movs r0,#0x1f    @ 080d3216 1f20
    ldrb r2,[r3,#0x0]                        @ 080d3218 1a78
    ands r0,r2    @ 080d321a 1040
    lsls r0,r0,#0x3    @ 080d321c c000
    orrs r0,r1    @ 080d321e 0843
    cmp r0,#0x0                              @ 080d3220 0028
    beq LAB_080d3248                         @ 080d3222 11d0
    ldr r1,[r3,#0x0]                         @ 080d3224 1968
    lsls r1,r1,#0xb    @ 080d3226 c902
    lsrs r1,r1,#0x18    @ 080d3228 090e
    ldr r3, DWORD_080d3244                   @ 080d322a 064b
    adds r0,r5,r3    @ 080d322c e818
    ldrh r0,[r0,#0x0]                        @ 080d322e 0088
    lsls r0,r0,#0x13    @ 080d3230 c004
    lsrs r0,r0,#0x18    @ 080d3232 000e
    adds r1,r1,r0    @ 080d3234 0918
    lsls r1,r1,#0x1    @ 080d3236 4900
    movs r4,#0xa8    @ 080d3238 a824
    lsls r4,r4,#0x6    @ 080d323a a401
    adds r0,r5,r4    @ 080d323c 2819
    b LAB_080d3262                           @ 080d323e 10e0
DWORD_080d3240:
    .word  0x00002f53                     @ 080d3240 532f0000
DWORD_080d3244:
    .word  0x00002f56                     @ 080d3244 562f0000
LAB_080d3248:
    ldr r1,[r3,#0x0]                         @ 080d3248 1968
    lsls r1,r1,#0xb    @ 080d324a c902
    lsrs r1,r1,#0x18    @ 080d324c 090e
    ldr r2, DWORD_080d3280                   @ 080d324e 0c4a
    adds r0,r5,r2    @ 080d3250 a818
    ldrh r0,[r0,#0x0]                        @ 080d3252 0088
    lsls r0,r0,#0x13    @ 080d3254 c004
    lsrs r0,r0,#0x18    @ 080d3256 000e
    adds r1,r1,r0    @ 080d3258 0918
    lsls r1,r1,#0x1    @ 080d325a 4900
    movs r3,#0xa0    @ 080d325c a023
    lsls r3,r3,#0x6    @ 080d325e 9b01
    adds r0,r5,r3    @ 080d3260 e818
LAB_080d3262:
    adds r1,r1,r0    @ 080d3262 0918
    ldrh r0,[r1,#0x0]                        @ 080d3264 0888
    bl check_zone_slot_attr_visible          @ 080d3266 fdf78dfa
    cmp r0,#0x0                              @ 080d326a 0028
    bne LAB_080d3290                         @ 080d326c 10d1
    ldr r0, DWORD_080d3284                   @ 080d326e 0548
    ldr r4, DWORD_080d3288                   @ 080d3270 054c
    adds r0,r0,r4    @ 080d3272 0019
    ldr r1, DWORD_080d328c                   @ 080d3274 0549
    ldrh r2,[r0,#0x0]                        @ 080d3276 0288
    ands r1,r2    @ 080d3278 1140
    movs r2,#0xc0    @ 080d327a c022
    b LAB_080d37b2                           @ 080d327c 99e2
    .zero  0x2
DWORD_080d3280:
    .word  0x00002f56                     @ 080d3280 562f0000
DWORD_080d3284:
    .word  0x02020160                     @ 080d3284 60010202
DWORD_080d3288:
    .word  0x00002f54                     @ 080d3288 542f0000
DWORD_080d328c:
    .word  0xffffe01f                     @ 080d328c 1fe0ffff
LAB_080d3290:
    ldr r0, DWORD_080d32d8                   @ 080d3290 1148
    movs r3,#0xa4    @ 080d3292 a423
    lsls r3,r3,#0x1    @ 080d3294 5b00
    adds r0,r0,r3    @ 080d3296 c018
    ldrh r1,[r0,#0x0]                        @ 080d3298 0188
    movs r0,#0x8    @ 080d329a 0820
    ands r0,r1    @ 080d329c 0840
    cmp r0,#0x0                              @ 080d329e 0028
    beq LAB_080d3338                         @ 080d32a0 4ad0
    ldr r3, DWORD_080d32dc                   @ 080d32a2 0e4b
    ldr r4, DWORD_080d32e0                   @ 080d32a4 0e4c
    adds r0,r3,r4    @ 080d32a6 1819
    ldrb r0,[r0,#0x0]                        @ 080d32a8 0078
    lsrs r1,r0,#0x5    @ 080d32aa 4109
    ldr r0, DWORD_080d32e4                   @ 080d32ac 0d48
    adds r2,r3,r0    @ 080d32ae 1a18
    movs r0,#0x1f    @ 080d32b0 1f20
    ldrb r4,[r2,#0x0]                        @ 080d32b2 1478
    ands r0,r4    @ 080d32b4 2040
    lsls r0,r0,#0x3    @ 080d32b6 c000
    orrs r0,r1    @ 080d32b8 0843
    cmp r0,#0x0                              @ 080d32ba 0028
    beq LAB_080d32ec                         @ 080d32bc 16d0
    ldr r1,[r2,#0x0]                         @ 080d32be 1168
    lsls r1,r1,#0xb    @ 080d32c0 c902
    lsrs r1,r1,#0x18    @ 080d32c2 090e
    ldr r2, DWORD_080d32e8                   @ 080d32c4 084a
    adds r0,r3,r2    @ 080d32c6 9818
    ldrh r0,[r0,#0x0]                        @ 080d32c8 0088
    lsls r0,r0,#0x13    @ 080d32ca c004
    lsrs r0,r0,#0x18    @ 080d32cc 000e
    adds r1,r1,r0    @ 080d32ce 0918
    lsls r1,r1,#0x1    @ 080d32d0 4900
    movs r4,#0xa8    @ 080d32d2 a824
    lsls r4,r4,#0x6    @ 080d32d4 a401
    b LAB_080d3304                           @ 080d32d6 15e0
DWORD_080d32d8:
    .word  gPrng                          @ 080d32d8 40000003
DWORD_080d32dc:
    .word  0x02020160                     @ 080d32dc 60010202
DWORD_080d32e0:
    .word  0x00002f53                     @ 080d32e0 532f0000
DWORD_080d32e4:
    .word  0x00002f54                     @ 080d32e4 542f0000
DWORD_080d32e8:
    .word  0x00002f56                     @ 080d32e8 562f0000
LAB_080d32ec:
    ldr r1,[r2,#0x0]                         @ 080d32ec 1168
    lsls r1,r1,#0xb    @ 080d32ee c902
    lsrs r1,r1,#0x18    @ 080d32f0 090e
    ldr r2, DWORD_080d3328                   @ 080d32f2 0d4a
    adds r0,r3,r2    @ 080d32f4 9818
    ldrh r0,[r0,#0x0]                        @ 080d32f6 0088
    lsls r0,r0,#0x13    @ 080d32f8 c004
    lsrs r0,r0,#0x18    @ 080d32fa 000e
    adds r1,r1,r0    @ 080d32fc 0918
    lsls r1,r1,#0x1    @ 080d32fe 4900
    movs r4,#0xa0    @ 080d3300 a024
    lsls r4,r4,#0x6    @ 080d3302 a401
LAB_080d3304:
    adds r0,r3,r4    @ 080d3304 1819
    adds r1,r1,r0    @ 080d3306 0918
    ldrh r4,[r1,#0x0]                        @ 080d3308 0c88
    adds r0,r4,#0x0    @ 080d330a 201c
    bl check_zone_slot_attr_visible          @ 080d330c fdf73afa
    cmp r0,#0x0                              @ 080d3310 0028
    beq LAB_080d3316                         @ 080d3312 00d0
    b LAB_080d380c                           @ 080d3314 7ae2
LAB_080d3316:
    ldr r0, DWORD_080d332c                   @ 080d3316 0548
    ldr r1, DWORD_080d3330                   @ 080d3318 0549
    adds r0,r0,r1    @ 080d331a 4018
    ldr r1, DWORD_080d3334                   @ 080d331c 0549
    ldrh r2,[r0,#0x0]                        @ 080d331e 0288
    ands r1,r2    @ 080d3320 1140
    movs r2,#0xa0    @ 080d3322 a022
    b LAB_080d37b2                           @ 080d3324 45e2
    .zero  0x2
DWORD_080d3328:
    .word  0x00002f56                     @ 080d3328 562f0000
DWORD_080d332c:
    .word  0x02020160                     @ 080d332c 60010202
DWORD_080d3330:
    .word  0x00002f54                     @ 080d3330 542f0000
DWORD_080d3334:
    .word  0xffffe01f                     @ 080d3334 1fe0ffff
LAB_080d3338:
    movs r0,#0x40    @ 080d3338 4020
    ands r0,r1    @ 080d333a 0840
    cmp r0,#0x0                              @ 080d333c 0028
    beq LAB_080d335c                         @ 080d333e 0dd0
    ldr r0, DWORD_080d3350                   @ 080d3340 0348
    ldr r3, DWORD_080d3354                   @ 080d3342 044b
    adds r0,r0,r3    @ 080d3344 c018
    ldr r1, DWORD_080d3358                   @ 080d3346 0449
    ldrh r4,[r0,#0x0]                        @ 080d3348 0488
    ands r1,r4    @ 080d334a 2140
    movs r2,#0x20    @ 080d334c 2022
    b LAB_080d37b2                           @ 080d334e 30e2
DWORD_080d3350:
    .word  0x02020160                     @ 080d3350 60010202
DWORD_080d3354:
    .word  0x00002f54                     @ 080d3354 542f0000
DWORD_080d3358:
    .word  0xffffe01f                     @ 080d3358 1fe0ffff
LAB_080d335c:
    movs r0,#0x80    @ 080d335c 8020
    ands r0,r1    @ 080d335e 0840
    cmp r0,#0x0                              @ 080d3360 0028
    beq LAB_080d3398                         @ 080d3362 19d0
    bl check_field_scroll_phase_ready        @ 080d3364 fff73cf9
    cmp r0,#0x0                              @ 080d3368 0028
    beq LAB_080d337c                         @ 080d336a 07d0
    ldr r0, DWORD_080d3374                   @ 080d336c 0148
    ldr r1, DWORD_080d3378                   @ 080d336e 0249
    adds r0,r0,r1    @ 080d3370 4018
    b LAB_080d37aa                           @ 080d3372 1ae2
DWORD_080d3374:
    .word  0x02020160                     @ 080d3374 60010202
DWORD_080d3378:
    .word  0x00002f54                     @ 080d3378 542f0000
LAB_080d337c:
    ldr r0, DWORD_080d338c                   @ 080d337c 0348
    ldr r3, DWORD_080d3390                   @ 080d337e 044b
    adds r0,r0,r3    @ 080d3380 c018
    ldr r1, DWORD_080d3394                   @ 080d3382 0449
    ldrh r4,[r0,#0x0]                        @ 080d3384 0488
    ands r1,r4    @ 080d3386 2140
    movs r2,#0x40    @ 080d3388 4022
    b LAB_080d37b2                           @ 080d338a 12e2
DWORD_080d338c:
    .word  0x02020160                     @ 080d338c 60010202
DWORD_080d3390:
    .word  0x00002f54                     @ 080d3390 542f0000
DWORD_080d3394:
    .word  0xffffe01f                     @ 080d3394 1fe0ffff
LAB_080d3398:
    movs r0,#0x20    @ 080d3398 2020
    ands r0,r1    @ 080d339a 0840
    cmp r0,#0x0                              @ 080d339c 0028
    bne LAB_080d33a2                         @ 080d339e 00d1
    b LAB_080d34d8                           @ 080d33a0 9ae0
LAB_080d33a2:
    ldr r1, DWORD_080d3408                   @ 080d33a2 1949
    ldr r0, DWORD_080d340c                   @ 080d33a4 1948
    adds r4,r1,r0    @ 080d33a6 0c18
    ldr r3,[r4,#0x0]                         @ 080d33a8 2368
    ldr r0, DWORD_080d3410                   @ 080d33aa 1948
    ands r0,r3    @ 080d33ac 1840
    adds r7,r1,#0x0    @ 080d33ae 0f1c
    cmp r0,#0x0                              @ 080d33b0 0028
    bne LAB_080d33b6                         @ 080d33b2 00d1
    b signal_zone_tick_done                  @ 080d33b4 37e2
LAB_080d33b6:
    ldr r1, DWORD_080d3414                   @ 080d33b6 1749
    adds r5,r7,r1    @ 080d33b8 7d18
    ldrh r2,[r5,#0x0]                        @ 080d33ba 2a88
    movs r0,#0xff    @ 080d33bc ff20
    lsls r0,r0,#0x5    @ 080d33be 4001
    ands r0,r2    @ 080d33c0 1040
    cmp r0,#0x0                              @ 080d33c2 0028
    beq LAB_080d3448                         @ 080d33c4 40d0
    lsls r0,r2,#0x13    @ 080d33c6 d004
    lsrs r0,r0,#0x18    @ 080d33c8 000e
    subs r0,#0x1    @ 080d33ca 0138
    movs r1,#0xff    @ 080d33cc ff21
    ands r0,r1    @ 080d33ce 0840
    lsls r0,r0,#0x5    @ 080d33d0 4001
    ldr r3, DWORD_080d3418                   @ 080d33d2 114b
    ands r3,r2    @ 080d33d4 1340
    orrs r3,r0    @ 080d33d6 0343
    strh r3,[r5,#0x0]                        @ 080d33d8 2b80
    ldr r2, DWORD_080d341c                   @ 080d33da 104a
    adds r0,r7,r2    @ 080d33dc b818
    ldrb r0,[r0,#0x0]                        @ 080d33de 0078
    lsrs r1,r0,#0x5    @ 080d33e0 4109
    movs r0,#0x1f    @ 080d33e2 1f20
    ldrb r2,[r4,#0x0]                        @ 080d33e4 2278
    ands r0,r2    @ 080d33e6 1040
    lsls r0,r0,#0x3    @ 080d33e8 c000
    orrs r0,r1    @ 080d33ea 0843
    cmp r0,#0x0                              @ 080d33ec 0028
    beq LAB_080d3420                         @ 080d33ee 17d0
    ldr r0,[r4,#0x0]                         @ 080d33f0 2068
    lsls r0,r0,#0xb    @ 080d33f2 c002
    lsrs r0,r0,#0x18    @ 080d33f4 000e
    lsls r1,r3,#0x13    @ 080d33f6 d904
    lsrs r1,r1,#0x18    @ 080d33f8 090e
    adds r0,r0,r1    @ 080d33fa 4018
    lsls r0,r0,#0x1    @ 080d33fc 4000
    movs r3,#0xa8    @ 080d33fe a823
    lsls r3,r3,#0x6    @ 080d3400 9b01
    adds r1,r7,r3    @ 080d3402 f918
    b LAB_080d3434                           @ 080d3404 16e0
    .zero  0x2
DWORD_080d3408:
    .word  0x02020160                     @ 080d3408 60010202
DWORD_080d340c:
    .word  0x00002f54                     @ 080d340c 542f0000
DWORD_080d3410:
    .word  0x1fffe000                     @ 080d3410 00e0ff1f
DWORD_080d3414:
    .word  0x00002f56                     @ 080d3414 562f0000
DWORD_080d3418:
    .word  0xffffe01f                     @ 080d3418 1fe0ffff
DWORD_080d341c:
    .word  0x00002f53                     @ 080d341c 532f0000
LAB_080d3420:
    ldr r0,[r4,#0x0]                         @ 080d3420 2068
    lsls r0,r0,#0xb    @ 080d3422 c002
    lsrs r0,r0,#0x18    @ 080d3424 000e
    lsls r1,r3,#0x13    @ 080d3426 d904
    lsrs r1,r1,#0x18    @ 080d3428 090e
    adds r0,r0,r1    @ 080d342a 4018
    lsls r0,r0,#0x1    @ 080d342c 4000
    movs r4,#0xa0    @ 080d342e a024
    lsls r4,r4,#0x6    @ 080d3430 a401
    adds r1,r7,r4    @ 080d3432 3919
LAB_080d3434:
    adds r0,r0,r1    @ 080d3434 4018
    ldrh r4,[r0,#0x0]                        @ 080d3436 0488
    adds r0,r4,#0x0    @ 080d3438 201c
    bl check_zone_slot_attr_visible          @ 080d343a fdf7a3f9
    adds r1,r0,#0x0    @ 080d343e 011c
    adds r0,r4,#0x0    @ 080d3440 201c
    bl dispatch_zone_card_display_by_mode    @ 080d3442 fdf7e9f9
    b LAB_080d30b0                           @ 080d3446 33e6
LAB_080d3448:
    movs r0,#0xff    @ 080d3448 ff20
    lsls r0,r0,#0xd    @ 080d344a 4003
    ands r0,r3    @ 080d344c 1840
    cmp r0,#0x0                              @ 080d344e 0028
    bne LAB_080d3454                         @ 080d3450 00d1
    b signal_zone_tick_done                  @ 080d3452 e8e1
LAB_080d3454:
    lsls r0,r3,#0xb    @ 080d3454 d802
    lsrs r0,r0,#0x18    @ 080d3456 000e
    subs r0,#0x1    @ 080d3458 0138
    lsls r0,r0,#0x10    @ 080d345a 0004
    lsrs r0,r0,#0x10    @ 080d345c 000c
    movs r1,#0xff    @ 080d345e ff21
    ands r0,r1    @ 080d3460 0840
    lsls r0,r0,#0xd    @ 080d3462 4003
    ldr r2, DWORD_080d3498                   @ 080d3464 0c4a
    ands r2,r3    @ 080d3466 1a40
    orrs r2,r0    @ 080d3468 0243
    str r2,[r4,#0x0]                         @ 080d346a 2260
    ldr r1, DWORD_080d349c                   @ 080d346c 0b49
    adds r0,r7,r1    @ 080d346e 7818
    ldrb r0,[r0,#0x0]                        @ 080d3470 0078
    lsrs r1,r0,#0x5    @ 080d3472 4109
    movs r0,#0x1f    @ 080d3474 1f20
    ldrb r4,[r4,#0x0]                        @ 080d3476 2478
    ands r0,r4    @ 080d3478 2040
    lsls r0,r0,#0x3    @ 080d347a c000
    orrs r0,r1    @ 080d347c 0843
    cmp r0,#0x0                              @ 080d347e 0028
    beq LAB_080d34a0                         @ 080d3480 0ed0
    lsls r0,r2,#0xb    @ 080d3482 d002
    lsrs r0,r0,#0x18    @ 080d3484 000e
    ldrh r5,[r5,#0x0]                        @ 080d3486 2d88
    lsls r1,r5,#0x13    @ 080d3488 e904
    lsrs r1,r1,#0x18    @ 080d348a 090e
    adds r0,r0,r1    @ 080d348c 4018
    lsls r0,r0,#0x1    @ 080d348e 4000
    movs r2,#0xa8    @ 080d3490 a822
    lsls r2,r2,#0x6    @ 080d3492 9201
    adds r1,r7,r2    @ 080d3494 b918
    b LAB_080d34b4                           @ 080d3496 0de0
DWORD_080d3498:
    .word  0xffe01fff                     @ 080d3498 ff1fe0ff
DWORD_080d349c:
    .word  0x00002f53                     @ 080d349c 532f0000
LAB_080d34a0:
    lsls r0,r2,#0xb    @ 080d34a0 d002
    lsrs r0,r0,#0x18    @ 080d34a2 000e
    ldrh r5,[r5,#0x0]                        @ 080d34a4 2d88
    lsls r1,r5,#0x13    @ 080d34a6 e904
    lsrs r1,r1,#0x18    @ 080d34a8 090e
    adds r0,r0,r1    @ 080d34aa 4018
    lsls r0,r0,#0x1    @ 080d34ac 4000
    movs r3,#0xa0    @ 080d34ae a023
    lsls r3,r3,#0x6    @ 080d34b0 9b01
    adds r1,r7,r3    @ 080d34b2 f918
LAB_080d34b4:
    adds r0,r0,r1    @ 080d34b4 4018
    ldrh r4,[r0,#0x0]                        @ 080d34b6 0488
    ldr r1, DWORD_080d34d4                   @ 080d34b8 0649
    adds r0,r7,r1    @ 080d34ba 7818
    movs r1,#0x4    @ 080d34bc 0421
    ldrb r2,[r0,#0x0]                        @ 080d34be 0278
    orrs r1,r2    @ 080d34c0 1143
    strb r1,[r0,#0x0]                        @ 080d34c2 0170
    adds r0,r4,#0x0    @ 080d34c4 201c
    bl check_zone_slot_attr_visible          @ 080d34c6 fdf75df9
    adds r1,r0,#0x0    @ 080d34ca 011c
    adds r0,r4,#0x0    @ 080d34cc 201c
    bl dispatch_zone_card_display_by_mode    @ 080d34ce fdf7a3f9
    b LAB_080d30b0                           @ 080d34d2 ede5
DWORD_080d34d4:
    .word  0x00002f51                     @ 080d34d4 512f0000
LAB_080d34d8:
    movs r0,#0x10    @ 080d34d8 1020
    ands r0,r1    @ 080d34da 0840
    cmp r0,#0x0                              @ 080d34dc 0028
    bne LAB_080d34e2                         @ 080d34de 00d1
    b LAB_080d36e4                           @ 080d34e0 00e1
LAB_080d34e2:
    ldr r0, DWORD_080d3524                   @ 080d34e2 1048
    ldr r3, DWORD_080d3528                   @ 080d34e4 104b
    adds r1,r0,r3    @ 080d34e6 c118
    ldrh r1,[r1,#0x0]                        @ 080d34e8 0988
    lsls r1,r1,#0x13    @ 080d34ea c904
    lsrs r1,r1,#0x18    @ 080d34ec 090e
    adds r7,r0,#0x0    @ 080d34ee 071c
    subs r5,r6,#0x1    @ 080d34f0 751e
    cmp r1,r5                                @ 080d34f2 a942
    blt LAB_080d3556                         @ 080d34f4 2fdb
    ldr r4, DWORD_080d352c                   @ 080d34f6 0d4c
    adds r2,r7,r4    @ 080d34f8 3a19
    ldr r0,[r2,#0x0]                         @ 080d34fa 1068
    lsls r0,r0,#0xb    @ 080d34fc c002
    lsrs r4,r0,#0x18    @ 080d34fe 040e
    ldr r1, DWORD_080d3530                   @ 080d3500 0b49
    adds r0,r7,r1    @ 080d3502 7818
    ldrb r0,[r0,#0x0]                        @ 080d3504 0078
    lsrs r1,r0,#0x5    @ 080d3506 4109
    movs r3,#0x1f    @ 080d3508 1f23
    adds r0,r3,#0x0    @ 080d350a 181c
    ldrb r2,[r2,#0x0]                        @ 080d350c 1278
    ands r0,r2    @ 080d350e 1040
    lsls r0,r0,#0x3    @ 080d3510 c000
    orrs r0,r1    @ 080d3512 0843
    cmp r0,#0x0                              @ 080d3514 0028
    beq LAB_080d3538                         @ 080d3516 0fd0
    ldr r2, DWORD_080d3534                   @ 080d3518 064a
    adds r0,r7,r2    @ 080d351a b818
    ldrh r0,[r0,#0x0]                        @ 080d351c 0088
    lsls r0,r0,#0x13    @ 080d351e c004
    lsrs r0,r0,#0x18    @ 080d3520 000e
    b LAB_080d354e                           @ 080d3522 14e0
DWORD_080d3524:
    .word  0x02020160                     @ 080d3524 60010202
DWORD_080d3528:
    .word  0x00002f56                     @ 080d3528 562f0000
DWORD_080d352c:
    .word  0x00002f54                     @ 080d352c 542f0000
DWORD_080d3530:
    .word  0x00002f53                     @ 080d3530 532f0000
DWORD_080d3534:
    .word  0x00002f58                     @ 080d3534 582f0000
LAB_080d3538:
    ldr r1, DWORD_080d35a4                   @ 080d3538 1a49
    adds r0,r7,r1    @ 080d353a 7818
    ldrb r0,[r0,#0x0]                        @ 080d353c 0078
    lsrs r2,r0,#0x5    @ 080d353e 4209
    ldr r0, DWORD_080d35a8                   @ 080d3540 1948
    adds r1,r7,r0    @ 080d3542 3918
    adds r0,r3,#0x0    @ 080d3544 181c
    ldrb r1,[r1,#0x0]                        @ 080d3546 0978
    ands r0,r1    @ 080d3548 0840
    lsls r0,r0,#0x3    @ 080d354a c000
    orrs r0,r2    @ 080d354c 1043
LAB_080d354e:
    subs r0,#0x5    @ 080d354e 0538
    cmp r4,r0                                @ 080d3550 8442
    blt LAB_080d3556                         @ 080d3552 00db
    b signal_zone_tick_done                  @ 080d3554 67e1
LAB_080d3556:
    ldr r1, DWORD_080d35ac                   @ 080d3556 1549
    adds r4,r7,r1    @ 080d3558 7c18
    ldrh r3,[r4,#0x0]                        @ 080d355a 2388
    lsls r1,r3,#0x13    @ 080d355c d904
    lsrs r0,r1,#0x18    @ 080d355e 080e
    cmp r0,r5                                @ 080d3560 a842
    bge LAB_080d35e4                         @ 080d3562 3fda
    adds r0,#0x1    @ 080d3564 0130
    movs r1,#0xff    @ 080d3566 ff21
    ands r0,r1    @ 080d3568 0840
    lsls r0,r0,#0x5    @ 080d356a 4001
    ldr r2, DWORD_080d35b0                   @ 080d356c 104a
    ands r2,r3    @ 080d356e 1a40
    orrs r2,r0    @ 080d3570 0243
    strh r2,[r4,#0x0]                        @ 080d3572 2280
    ldr r3, DWORD_080d35b4                   @ 080d3574 0f4b
    adds r0,r7,r3    @ 080d3576 f818
    ldrb r0,[r0,#0x0]                        @ 080d3578 0078
    lsrs r1,r0,#0x5    @ 080d357a 4109
    ldr r4, DWORD_080d35b8                   @ 080d357c 0e4c
    adds r3,r7,r4    @ 080d357e 3b19
    movs r0,#0x1f    @ 080d3580 1f20
    ldrb r4,[r3,#0x0]                        @ 080d3582 1c78
    ands r0,r4    @ 080d3584 2040
    lsls r0,r0,#0x3    @ 080d3586 c000
    orrs r0,r1    @ 080d3588 0843
    cmp r0,#0x0                              @ 080d358a 0028
    beq LAB_080d35bc                         @ 080d358c 16d0
    ldr r0,[r3,#0x0]                         @ 080d358e 1868
    lsls r0,r0,#0xb    @ 080d3590 c002
    lsrs r0,r0,#0x18    @ 080d3592 000e
    lsls r1,r2,#0x13    @ 080d3594 d104
    lsrs r1,r1,#0x18    @ 080d3596 090e
    adds r0,r0,r1    @ 080d3598 4018
    lsls r0,r0,#0x1    @ 080d359a 4000
    movs r2,#0xa8    @ 080d359c a822
    lsls r2,r2,#0x6    @ 080d359e 9201
    adds r1,r7,r2    @ 080d35a0 b918
    b LAB_080d35d0                           @ 080d35a2 15e0
DWORD_080d35a4:
    .word  0x00002f57                     @ 080d35a4 572f0000
DWORD_080d35a8:
    .word  0x00002f58                     @ 080d35a8 582f0000
DWORD_080d35ac:
    .word  0x00002f56                     @ 080d35ac 562f0000
DWORD_080d35b0:
    .word  0xffffe01f                     @ 080d35b0 1fe0ffff
DWORD_080d35b4:
    .word  0x00002f53                     @ 080d35b4 532f0000
DWORD_080d35b8:
    .word  0x00002f54                     @ 080d35b8 542f0000
LAB_080d35bc:
    ldr r0,[r3,#0x0]                         @ 080d35bc 1868
    lsls r0,r0,#0xb    @ 080d35be c002
    lsrs r0,r0,#0x18    @ 080d35c0 000e
    lsls r1,r2,#0x13    @ 080d35c2 d104
    lsrs r1,r1,#0x18    @ 080d35c4 090e
    adds r0,r0,r1    @ 080d35c6 4018
    lsls r0,r0,#0x1    @ 080d35c8 4000
    movs r3,#0xa0    @ 080d35ca a023
    lsls r3,r3,#0x6    @ 080d35cc 9b01
    adds r1,r7,r3    @ 080d35ce f918
LAB_080d35d0:
    adds r0,r0,r1    @ 080d35d0 4018
    ldrh r4,[r0,#0x0]                        @ 080d35d2 0488
    adds r0,r4,#0x0    @ 080d35d4 201c
    bl check_zone_slot_attr_visible          @ 080d35d6 fdf7d5f8
    adds r1,r0,#0x0    @ 080d35da 011c
    adds r0,r4,#0x0    @ 080d35dc 201c
    bl dispatch_zone_card_display_by_mode    @ 080d35de fdf71bf9
    b LAB_080d30b0                           @ 080d35e2 65e5
LAB_080d35e4:
    ldr r4, DWORD_080d3618                   @ 080d35e4 0c4c
    adds r2,r7,r4    @ 080d35e6 3a19
    ldr r0,[r2,#0x0]                         @ 080d35e8 1068
    lsls r0,r0,#0xb    @ 080d35ea c002
    lsrs r4,r0,#0x18    @ 080d35ec 040e
    ldr r1, DWORD_080d361c                   @ 080d35ee 0b49
    adds r0,r7,r1    @ 080d35f0 7818
    ldrb r0,[r0,#0x0]                        @ 080d35f2 0078
    lsrs r1,r0,#0x5    @ 080d35f4 4109
    movs r3,#0x1f    @ 080d35f6 1f23
    adds r0,r3,#0x0    @ 080d35f8 181c
    ldrb r2,[r2,#0x0]                        @ 080d35fa 1278
    ands r0,r2    @ 080d35fc 1040
    lsls r0,r0,#0x3    @ 080d35fe c000
    orrs r0,r1    @ 080d3600 0843
    cmp r0,#0x0                              @ 080d3602 0028
    beq LAB_080d3624                         @ 080d3604 0ed0
    ldr r2, DWORD_080d3620                   @ 080d3606 064a
    adds r0,r7,r2    @ 080d3608 b818
    ldrh r0,[r0,#0x0]                        @ 080d360a 0088
    lsls r0,r0,#0x13    @ 080d360c c004
    lsrs r0,r0,#0x18    @ 080d360e 000e
    subs r0,#0x5    @ 080d3610 0538
    cmp r4,r0                                @ 080d3612 8442
    blt LAB_080d3642                         @ 080d3614 15db
    b signal_zone_tick_done                  @ 080d3616 06e1
DWORD_080d3618:
    .word  0x00002f54                     @ 080d3618 542f0000
DWORD_080d361c:
    .word  0x00002f53                     @ 080d361c 532f0000
DWORD_080d3620:
    .word  0x00002f58                     @ 080d3620 582f0000
LAB_080d3624:
    ldr r1, DWORD_080d368c                   @ 080d3624 1949
    adds r0,r7,r1    @ 080d3626 7818
    ldrb r0,[r0,#0x0]                        @ 080d3628 0078
    lsrs r2,r0,#0x5    @ 080d362a 4209
    ldr r0, DWORD_080d3690                   @ 080d362c 1848
    adds r1,r7,r0    @ 080d362e 3918
    adds r0,r3,#0x0    @ 080d3630 181c
    ldrb r1,[r1,#0x0]                        @ 080d3632 0978
    ands r0,r1    @ 080d3634 0840
    lsls r0,r0,#0x3    @ 080d3636 c000
    orrs r0,r2    @ 080d3638 1043
    subs r0,#0x5    @ 080d363a 0538
    cmp r4,r0                                @ 080d363c 8442
    blt LAB_080d3642                         @ 080d363e 00db
    b signal_zone_tick_done                  @ 080d3640 f1e0
LAB_080d3642:
    ldr r1, DWORD_080d3694                   @ 080d3642 1449
    adds r2,r7,r1    @ 080d3644 7a18
    ldr r3,[r2,#0x0]                         @ 080d3646 1368
    lsls r0,r3,#0xb    @ 080d3648 d802
    lsrs r0,r0,#0x18    @ 080d364a 000e
    adds r0,#0x1    @ 080d364c 0130
    movs r1,#0xff    @ 080d364e ff21
    ands r0,r1    @ 080d3650 0840
    lsls r0,r0,#0xd    @ 080d3652 4003
    ldr r4, DWORD_080d3698                   @ 080d3654 104c
    ands r4,r3    @ 080d3656 1c40
    orrs r4,r0    @ 080d3658 0443
    str r4,[r2,#0x0]                         @ 080d365a 1460
    ldr r3, DWORD_080d369c                   @ 080d365c 0f4b
    adds r0,r7,r3    @ 080d365e f818
    ldrb r0,[r0,#0x0]                        @ 080d3660 0078
    lsrs r1,r0,#0x5    @ 080d3662 4109
    movs r0,#0x1f    @ 080d3664 1f20
    ldrb r2,[r2,#0x0]                        @ 080d3666 1278
    ands r0,r2    @ 080d3668 1040
    lsls r0,r0,#0x3    @ 080d366a c000
    orrs r0,r1    @ 080d366c 0843
    cmp r0,#0x0                              @ 080d366e 0028
    beq LAB_080d36a4                         @ 080d3670 18d0
    lsls r1,r4,#0xb    @ 080d3672 e102
    lsrs r1,r1,#0x18    @ 080d3674 090e
    ldr r4, DWORD_080d36a0                   @ 080d3676 0a4c
    adds r0,r7,r4    @ 080d3678 3819
    ldrh r0,[r0,#0x0]                        @ 080d367a 0088
    lsls r0,r0,#0x13    @ 080d367c c004
    lsrs r0,r0,#0x18    @ 080d367e 000e
    adds r1,r1,r0    @ 080d3680 0918
    lsls r1,r1,#0x1    @ 080d3682 4900
    movs r2,#0xa8    @ 080d3684 a822
    lsls r2,r2,#0x6    @ 080d3686 9201
    adds r0,r7,r2    @ 080d3688 b818
    b LAB_080d36bc                           @ 080d368a 17e0
DWORD_080d368c:
    .word  0x00002f57                     @ 080d368c 572f0000
DWORD_080d3690:
    .word  0x00002f58                     @ 080d3690 582f0000
DWORD_080d3694:
    .word  0x00002f54                     @ 080d3694 542f0000
DWORD_080d3698:
    .word  0xffe01fff                     @ 080d3698 ff1fe0ff
DWORD_080d369c:
    .word  0x00002f53                     @ 080d369c 532f0000
DWORD_080d36a0:
    .word  0x00002f56                     @ 080d36a0 562f0000
LAB_080d36a4:
    lsls r1,r4,#0xb    @ 080d36a4 e102
    lsrs r1,r1,#0x18    @ 080d36a6 090e
    ldr r3, DWORD_080d36dc                   @ 080d36a8 0c4b
    adds r0,r7,r3    @ 080d36aa f818
    ldrh r0,[r0,#0x0]                        @ 080d36ac 0088
    lsls r0,r0,#0x13    @ 080d36ae c004
    lsrs r0,r0,#0x18    @ 080d36b0 000e
    adds r1,r1,r0    @ 080d36b2 0918
    lsls r1,r1,#0x1    @ 080d36b4 4900
    movs r4,#0xa0    @ 080d36b6 a024
    lsls r4,r4,#0x6    @ 080d36b8 a401
    adds r0,r7,r4    @ 080d36ba 3819
LAB_080d36bc:
    adds r1,r1,r0    @ 080d36bc 0918
    ldrh r4,[r1,#0x0]                        @ 080d36be 0c88
    ldr r1, DWORD_080d36e0                   @ 080d36c0 0749
    adds r0,r7,r1    @ 080d36c2 7818
    movs r1,#0x4    @ 080d36c4 0421
    ldrb r2,[r0,#0x0]                        @ 080d36c6 0278
    orrs r1,r2    @ 080d36c8 1143
    strb r1,[r0,#0x0]                        @ 080d36ca 0170
    adds r0,r4,#0x0    @ 080d36cc 201c
    bl check_zone_slot_attr_visible          @ 080d36ce fdf759f8
    adds r1,r0,#0x0    @ 080d36d2 011c
    adds r0,r4,#0x0    @ 080d36d4 201c
    bl dispatch_zone_card_display_by_mode    @ 080d36d6 fdf79ff8
    b LAB_080d30b0                           @ 080d36da e9e4
DWORD_080d36dc:
    .word  0x00002f56                     @ 080d36dc 562f0000
DWORD_080d36e0:
    .word  0x00002f51                     @ 080d36e0 512f0000
LAB_080d36e4:
    movs r3,#0x1    @ 080d36e4 0123
    ands r3,r1    @ 080d36e6 0b40
    cmp r3,#0x0                              @ 080d36e8 002b
    beq LAB_080d37c4                         @ 080d36ea 6bd0
    ldr r0, DWORD_080d3730                   @ 080d36ec 1048
    ldr r0,[r0,#0x4]                         @ 080d36ee 4068
    cmp r0,#0x5                              @ 080d36f0 0528
    bls LAB_080d37d4                         @ 080d36f2 6fd9
    cmp r0,#0x48                             @ 080d36f4 4828
    bls LAB_080d36fa                         @ 080d36f6 00d9
    b LAB_080d3048                           @ 080d36f8 a6e4
LAB_080d36fa:
    ldr r3, DWORD_080d3734                   @ 080d36fa 0e4b
    ldr r4, DWORD_080d3738                   @ 080d36fc 0e4c
    adds r0,r3,r4    @ 080d36fe 1819
    ldrb r0,[r0,#0x0]                        @ 080d3700 0078
    lsrs r1,r0,#0x5    @ 080d3702 4109
    ldr r0, DWORD_080d373c                   @ 080d3704 0d48
    adds r2,r3,r0    @ 080d3706 1a18
    movs r0,#0x1f    @ 080d3708 1f20
    ldrb r4,[r2,#0x0]                        @ 080d370a 1478
    ands r0,r4    @ 080d370c 2040
    lsls r0,r0,#0x3    @ 080d370e c000
    orrs r0,r1    @ 080d3710 0843
    cmp r0,#0x0                              @ 080d3712 0028
    beq LAB_080d3744                         @ 080d3714 16d0
    ldr r1,[r2,#0x0]                         @ 080d3716 1168
    lsls r1,r1,#0xb    @ 080d3718 c902
    lsrs r1,r1,#0x18    @ 080d371a 090e
    ldr r2, DWORD_080d3740                   @ 080d371c 084a
    adds r0,r3,r2    @ 080d371e 9818
    ldrh r0,[r0,#0x0]                        @ 080d3720 0088
    lsls r0,r0,#0x13    @ 080d3722 c004
    lsrs r0,r0,#0x18    @ 080d3724 000e
    adds r1,r1,r0    @ 080d3726 0918
    lsls r1,r1,#0x1    @ 080d3728 4900
    movs r4,#0xa8    @ 080d372a a824
    lsls r4,r4,#0x6    @ 080d372c a401
    b LAB_080d375c                           @ 080d372e 15e0
DWORD_080d3730:
    .word  0x0201e4f0                     @ 080d3730 f0e40102
DWORD_080d3734:
    .word  0x02020160                     @ 080d3734 60010202
DWORD_080d3738:
    .word  0x00002f53                     @ 080d3738 532f0000
DWORD_080d373c:
    .word  0x00002f54                     @ 080d373c 542f0000
DWORD_080d3740:
    .word  0x00002f56                     @ 080d3740 562f0000
LAB_080d3744:
    ldr r1,[r2,#0x0]                         @ 080d3744 1168
    lsls r1,r1,#0xb    @ 080d3746 c902
    lsrs r1,r1,#0x18    @ 080d3748 090e
    ldr r2, DWORD_080d3774                   @ 080d374a 0a4a
    adds r0,r3,r2    @ 080d374c 9818
    ldrh r0,[r0,#0x0]                        @ 080d374e 0088
    lsls r0,r0,#0x13    @ 080d3750 c004
    lsrs r0,r0,#0x18    @ 080d3752 000e
    adds r1,r1,r0    @ 080d3754 0918
    lsls r1,r1,#0x1    @ 080d3756 4900
    movs r4,#0xa0    @ 080d3758 a024
    lsls r4,r4,#0x6    @ 080d375a a401
LAB_080d375c:
    adds r0,r3,r4    @ 080d375c 1819
    adds r1,r1,r0    @ 080d375e 0918
    ldrh r4,[r1,#0x0]                        @ 080d3760 0c88
    adds r0,r4,#0x0    @ 080d3762 201c
    bl update_zone_anim_queue_entry          @ 080d3764 fef766ff
    cmp r0,#0x0                              @ 080d3768 0028
    beq LAB_080d3778                         @ 080d376a 05d0
LAB_080d376c:
    movs r0,#0x1    @ 080d376c 0120
    bl sync_state_and_init_sprite            @ 080d376e 26f0a1f9
    b signal_zone_tick_done                  @ 080d3772 58e0
DWORD_080d3774:
    .word  0x00002f56                     @ 080d3774 562f0000
LAB_080d3778:
    bl get_clamped_tile_row_count            @ 080d3778 c0f78afd
    ldr r5, DWORD_080d37b8                   @ 080d377c 0e4d
    movs r1,#0xb9    @ 080d377e b921
    lsls r1,r1,#0x6    @ 080d3780 8901
    adds r2,r5,r1    @ 080d3782 6a18
    ldrb r1,[r2,#0x0]                        @ 080d3784 1178
    cmp r0,r1                                @ 080d3786 8842
    ble LAB_080d380c                         @ 080d3788 40dd
    lsls r0,r1,#0x1    @ 080d378a 4800
    movs r3,#0xb8    @ 080d378c b823
    lsls r3,r3,#0x6    @ 080d378e 9b01
    adds r1,r5,r3    @ 080d3790 e918
    adds r0,r0,r1    @ 080d3792 4018
    strh r4,[r0,#0x0]                        @ 080d3794 0480
    ldrb r0,[r2,#0x0]                        @ 080d3796 1078
    adds r0,#0x1    @ 080d3798 0130
    strb r0,[r2,#0x0]                        @ 080d379a 1070
    ldrb r4,[r2,#0x0]                        @ 080d379c 1478
    bl get_clamped_tile_row_count            @ 080d379e c0f777fd
    cmp r4,r0                                @ 080d37a2 8442
    bne signal_zone_tick_done                @ 080d37a4 3fd1
    ldr r4, DWORD_080d37bc                   @ 080d37a6 054c
    adds r0,r5,r4    @ 080d37a8 2819
LAB_080d37aa:
    ldr r1, DWORD_080d37c0                   @ 080d37aa 0549
    ldrh r2,[r0,#0x0]                        @ 080d37ac 0288
    ands r1,r2    @ 080d37ae 1140
    movs r2,#0x60    @ 080d37b0 6022
LAB_080d37b2:
    orrs r1,r2    @ 080d37b2 1143
    strh r1,[r0,#0x0]                        @ 080d37b4 0180
    b signal_zone_tick_done                  @ 080d37b6 36e0
DWORD_080d37b8:
    .word  0x02020160                     @ 080d37b8 60010202
DWORD_080d37bc:
    .word  0x00002f54                     @ 080d37bc 542f0000
DWORD_080d37c0:
    .word  0xffffe01f                     @ 080d37c0 1fe0ffff
LAB_080d37c4:
    movs r0,#0x2    @ 080d37c4 0220
    ands r0,r1    @ 080d37c6 0840
    cmp r0,#0x0                              @ 080d37c8 0028
    beq signal_zone_tick_done                @ 080d37ca 2cd0
    ldr r0, DWORD_080d37dc                   @ 080d37cc 0348
    ldr r0,[r0,#0x4]                         @ 080d37ce 4068
    cmp r0,#0x5                              @ 080d37d0 0528
    bgt LAB_080d37e0                         @ 080d37d2 05dc
LAB_080d37d4:
    movs r0,#0x1    @ 080d37d4 0120
LAB_080d37d6:
    bl sync_state_and_init_sprite            @ 080d37d6 26f06df9
    b LAB_080d3048                           @ 080d37da 35e4
DWORD_080d37dc:
    .word  0x0201e4f0                     @ 080d37dc f0e40102
LAB_080d37e0:
    cmp r0,#0x48                             @ 080d37e0 4828
    bgt LAB_080d3814                         @ 080d37e2 17dc
    ldr r1, DWORD_080d3808                   @ 080d37e4 0849
    movs r4,#0xb9    @ 080d37e6 b924
    lsls r4,r4,#0x6    @ 080d37e8 a401
    adds r2,r1,r4    @ 080d37ea 0a19
    ldrb r0,[r2,#0x0]                        @ 080d37ec 1078
    cmp r0,#0x0                              @ 080d37ee 0028
    beq LAB_080d380c                         @ 080d37f0 0cd0
    ldrb r0,[r2,#0x0]                        @ 080d37f2 1078
    subs r0,#0x1    @ 080d37f4 0138
    lsls r0,r0,#0x1    @ 080d37f6 4000
    subs r4,#0x40    @ 080d37f8 403c
    adds r1,r1,r4    @ 080d37fa 0919
    adds r0,r0,r1    @ 080d37fc 4018
    strh r3,[r0,#0x0]                        @ 080d37fe 0380
    ldrb r0,[r2,#0x0]                        @ 080d3800 1078
    subs r0,#0x1    @ 080d3802 0138
    strb r0,[r2,#0x0]                        @ 080d3804 1070
    b LAB_080d376c                           @ 080d3806 b1e7
DWORD_080d3808:
    .word  0x02020160                     @ 080d3808 60010202
LAB_080d380c:
    movs r0,#0x2    @ 080d380c 0220
    bl sync_state_and_init_sprite            @ 080d380e 26f051f9
    b signal_zone_tick_done                  @ 080d3812 08e0
LAB_080d3814:
    cmp r0,#0x4c                             @ 080d3814 4c28
    ble LAB_080d380c                         @ 080d3816 f9dd
    b signal_zone_tick_done                  @ 080d3818 05e0
LAB_080d381a:
    bl tick_zone_card_list_state_machine     @ 080d381a 00f02dfe
    b exit_zone_tick_frame                   @ 080d381e 03e0

@ 2-instruction stub called by FUN_080d2ef4 at zone card slot type=1 branch. bl tick_zone_card_anim_state (0x080d2390) to advance the slot animation state machine, then b exit_zone_tick_frame (0x080d3828) to pop FUN_080d2ef4 frame and return to its caller. Inherits r0=1 (frame-processed) from tick_zone_card_anim_state unchanged. GBA inline exit-stub pattern: single operation then shared pop+bx exit.
advance_zone_card_anim:
    bl tick_zone_card_anim_state             @ 080d3820 fef7b6fd
    b exit_zone_tick_frame                   @ 080d3824 00e0

@ Shared 'return done' exit stub for FUN_080d2ef4 (duel zone card slot state dispatcher). FUN_080d2ef4 branches here (b FUN_080d3826, not bl) from at least 11 sites to signal 'this frame slot processing complete'. movs r0,#0x1 sets return value = 1 (done), then falls through to exit_zone_tick_frame (0x080d3828) to pop FUN_080d2ef4 frame and return to FUN_080cc340 (which interprets r0=1 as non-busy). Constants: DONE=1.
signal_zone_tick_done:
    movs r0,#0x1    @ 080d3826 0120

@ Shared frame exit stub for FUN_080d2ef4 (duel zone card slot state dispatcher). FUN_080d2ef4 enters via 'b FUN_080d3828' (preserving current r0) from multiple paths. 3 instructions: pop {r4,r5,r6,r7} restores FUN_080d2ef4 callee-saves; pop {r1} retrieves saved LR; bx r1 returns to FUN_080d2ef4 caller with r0 unchanged. r0 on entry = 0 (busy/waiting) or 1 (done/advanced), set by caller before branching here. FUN_080d3826 (signal_zone_tick_done) fall-through -> here; advance_zone_card_anim (0x080d3820) tail-jumps here. Standard THUMB 'shared function exit' pattern matching FUN_080d2ef4 push {r4,r5,r6,r7,lr}.
exit_zone_tick_frame:
    pop {r4,r5,r6,r7}                        @ 080d3828 f0bc
    pop {r1}                                 @ 080d382a 02bc
    bx r1                                    @ 080d382c 0847
    .zero  0x2

@ Render card icon tile for duel field zone slot to OBJ VRAM (indeg=4). r0=slot_index; reads gDuelCtx+0x2f53 card_status byte; extracts bits[7:5] (high 3) and bits[4:0] (low 5); if combined==0 -> direct write to OAM addr (zero-vector path). Else: copy slot card metadata (9 words via ldmia/stmia); compute slot_mod5 = slot_index % 5 (bl __modsi3); VRAM row offset = (slot_mod5*4 + 0x1e0) << 5; bl tile_2d_row_copy(src, row=0, width=4, height=2) -> write 4x2 icon block to OBJ VRAM 0x06010000. No return value (void); side effects: OBJ VRAM 0x06010000+row_offset written. Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_MASK=0x1f; STRIDE=0x28; MOD_DIVISOR=5; TILE_VRAM=0x06010000; TILE_WIDTH=4; TILE_HEIGHT=2.
render_zone_slot_card_icon_tile:
    push {r4,r5,r6,r7,lr}                    @ 080d3830 f0b5
    .hword 0x464f    @ 080d3832 4f46
    .hword 0x4646    @ 080d3834 4646
    push {r6,r7}                             @ 080d3836 c0b4
    sub sp,#0x24                             @ 080d3838 89b0
    .hword 0x4681    @ 080d383a 8146
    ldr r1, DWORD_080d3868                   @ 080d383c 0a49
    ldr r2, DWORD_080d386c                   @ 080d383e 0b4a
    adds r0,r1,r2    @ 080d3840 8818
    ldrb r0,[r0,#0x0]                        @ 080d3842 0078
    lsrs r3,r0,#0x5    @ 080d3844 4309
    ldr r4, DWORD_080d3870                   @ 080d3846 0a4c
    adds r2,r1,r4    @ 080d3848 0a19
    movs r0,#0x1f    @ 080d384a 1f20
    ldrb r2,[r2,#0x0]                        @ 080d384c 1278
    ands r0,r2    @ 080d384e 1040
    lsls r0,r0,#0x3    @ 080d3850 c000
    orrs r0,r3    @ 080d3852 1843
    adds r4,r1,#0x0    @ 080d3854 0c1c
    cmp r0,#0x0                              @ 080d3856 0028
    beq LAB_080d3874                         @ 080d3858 0cd0
    .hword 0x464d    @ 080d385a 4d46
    lsls r0,r5,#0x1    @ 080d385c 6800
    movs r2,#0xa8    @ 080d385e a822
    lsls r2,r2,#0x6    @ 080d3860 9201
    adds r1,r4,r2    @ 080d3862 a118
    b LAB_080d387e                           @ 080d3864 0be0
    .zero  0x2
DWORD_080d3868:
    .word  0x02020160                     @ 080d3868 60010202
DWORD_080d386c:
    .word  0x00002f53                     @ 080d386c 532f0000
DWORD_080d3870:
    .word  0x00002f54                     @ 080d3870 542f0000
LAB_080d3874:
    .hword 0x464b    @ 080d3874 4b46
    lsls r0,r3,#0x1    @ 080d3876 5800
    movs r5,#0xa0    @ 080d3878 a025
    lsls r5,r5,#0x6    @ 080d387a ad01
    adds r1,r4,r5    @ 080d387c 6119
LAB_080d387e:
    adds r0,r0,r1    @ 080d387e 4018
    ldrh r0,[r0,#0x0]                        @ 080d3880 0088
    lsls r1,r0,#0x2    @ 080d3882 8100
    adds r1,r1,r0    @ 080d3884 0918
    lsls r1,r1,#0x3    @ 080d3886 c900
    adds r1,r1,r4    @ 080d3888 0919
    ldr r6,[r1,#0x0]                         @ 080d388a 0e68
    .hword 0x4668    @ 080d388c 6846
    ldmia r1!,{r2,r3,r5}                     @ 080d388e 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3890 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3892 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3894 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3896 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3898 2cc0
    .hword 0x4648    @ 080d389a 4846
    movs r1,#0x5    @ 080d389c 0521
    bl __modsi3                              @ 080d389e 3af0fdfe
    adds r5,r0,#0x0    @ 080d38a2 051c
    lsls r7,r5,#0x2    @ 080d38a4 af00
    movs r1,#0xf0    @ 080d38a6 f021
    lsls r1,r1,#0x1    @ 080d38a8 4900
    adds r0,r7,r1    @ 080d38aa 7818
    lsls r0,r0,#0x5    @ 080d38ac 4001
    ldr r2, DWORD_080d38dc                   @ 080d38ae 0b4a
    .hword 0x4690    @ 080d38b0 9046
    add r0,r8                                @ 080d38b2 4044
    movs r1,#0x0    @ 080d38b4 0021
    movs r2,#0x4    @ 080d38b6 0422
    movs r3,#0x2    @ 080d38b8 0223
    bl tile_2d_row_copy                      @ 080d38ba 23f00bfe
    ldr r3, DWORD_080d38e0                   @ 080d38be 084b
    adds r0,r4,r3    @ 080d38c0 e018
    ldrh r0,[r0,#0x0]                        @ 080d38c2 0088
    lsls r0,r0,#0x13    @ 080d38c4 c004
    lsrs r0,r0,#0x18    @ 080d38c6 000e
    cmp r0,#0x6                              @ 080d38c8 0628
    bne LAB_080d38ce                         @ 080d38ca 00d1
    b LAB_080d3a30                           @ 080d38cc b0e0
LAB_080d38ce:
    cmp r0,#0x6                              @ 080d38ce 0628
    ble LAB_080d38e4                         @ 080d38d0 08dd
    cmp r0,#0x7                              @ 080d38d2 0728
    bne LAB_080d38d8                         @ 080d38d4 00d1
    b LAB_080d3abc                           @ 080d38d6 f1e0
LAB_080d38d8:
    b LAB_080d3b4e                           @ 080d38d8 39e1
    .zero  0x2
DWORD_080d38dc:
    .word  0x06010000                     @ 080d38dc 00000106
DWORD_080d38e0:
    .word  0x00002f52                     @ 080d38e0 522f0000
LAB_080d38e4:
    cmp r0,#0x1                              @ 080d38e4 0128
    ble LAB_080d38ea                         @ 080d38e6 00dd
    b LAB_080d3b4e                           @ 080d38e8 31e1
LAB_080d38ea:
    cmp r0,#0x0                              @ 080d38ea 0028
    bge LAB_080d38f0                         @ 080d38ec 00da
    b LAB_080d3b4e                           @ 080d38ee 2ee1
LAB_080d38f0:
    ldr r4, DWORD_080d3988                   @ 080d38f0 254c
    ldr r5, DWORD_080d398c                   @ 080d38f2 264d
    adds r4,r4,r5    @ 080d38f4 6419
    ldrb r0,[r4,#0x0]                        @ 080d38f6 2078
    lsls r1,r0,#0x1d    @ 080d38f8 4107
    lsrs r1,r1,#0x1d    @ 080d38fa 490f
    adds r0,r6,#0x0    @ 080d38fc 301c
    bl select_charset_then_load_name         @ 080d38fe 1af055ff
    adds r5,r0,#0x0    @ 080d3902 051c
    movs r0,#0x4    @ 080d3904 0420
    movs r1,#0x2    @ 080d3906 0221
    movs r2,#0x1    @ 080d3908 0122
    movs r3,#0x0    @ 080d390a 0023
    bl setup_line_buf_with_font_and_align    @ 080d390c 1df0d8f9
    ldr r2, DWORD_080d3990                   @ 080d3910 1f4a
    movs r3,#0x7    @ 080d3912 0723
    ldrb r4,[r4,#0x0]                        @ 080d3914 2478
    ands r3,r4    @ 080d3916 2340
    rsbs r1,r3,#0    @ 080d3918 5942
    lsrs r1,r1,#0x1f    @ 080d391a c90f
    movs r0,#0x2    @ 080d391c 0220
    rsbs r0,r0,#0    @ 080d391e 4042
    ldrb r4,[r2,#0x8]                        @ 080d3920 147a
    ands r0,r4    @ 080d3922 2040
    orrs r0,r1    @ 080d3924 0843
    movs r1,#0x2    @ 080d3926 0221
    orrs r0,r1    @ 080d3928 0843
    strb r0,[r2,#0x8]                        @ 080d392a 1072
    ldr r4, DWORD_080d3994                   @ 080d392c 194c
    lsls r1,r0,#0x1e    @ 080d392e 8107
    lsrs r1,r1,#0x1f    @ 080d3930 c90f
    lsls r1,r1,#0x2    @ 080d3932 8900
    lsls r0,r0,#0x1f    @ 080d3934 c007
    lsrs r0,r0,#0x1f    @ 080d3936 c00f
    lsls r0,r0,#0x3    @ 080d3938 c000
    adds r1,r1,r0    @ 080d393a 0918
    adds r1,r1,r4    @ 080d393c 0919
    ldr r0,[r1,#0x0]                         @ 080d393e 0868
    str r0,[r2,#0x4]                         @ 080d3940 5060
    movs r0,#0x40    @ 080d3942 4020
    ldrb r1,[r2,#0x15]                       @ 080d3944 517d
    orrs r0,r1    @ 080d3946 0843
    strb r0,[r2,#0x15]                       @ 080d3948 5075
    cmp r3,#0x0                              @ 080d394a 002b
    bne LAB_080d39a0                         @ 080d394c 28d1
    adds r0,r5,#0x0    @ 080d394e 281c
    bl measure_string_pixel_width            @ 080d3950 1cf090fc
    cmp r0,#0x1f                             @ 080d3954 1f28
    ble LAB_080d39aa                         @ 080d3956 28dd
    movs r6,#0x4    @ 080d3958 0426
    movs r7,#0x1    @ 080d395a 0127
LAB_080d395c:
    ldrb r2,[r5,#0x0]                        @ 080d395c 2a78
    lsls r4,r2,#0x8    @ 080d395e 1402
    ldrb r3,[r5,#0x1]                        @ 080d3960 6b78
    orrs r4,r3    @ 080d3962 1c43
    adds r0,r4,#0x0    @ 080d3964 201c
    adds r1,r6,#0x0    @ 080d3966 311c
    movs r2,#0x2    @ 080d3968 0222
    ldr r3, DWORD_080d3998                   @ 080d396a 0b4b
    bl render_glyph_jp_dual_layer            @ 080d396c 1df08aff
    adds r0,r4,#0x0    @ 080d3970 201c
    adds r1,r6,#0x0    @ 080d3972 311c
    movs r2,#0x2    @ 080d3974 0222
    ldr r3, DWORD_080d399c                   @ 080d3976 094b
    bl render_glyph_jp_dual_layer            @ 080d3978 1df084ff
    adds r5,#0x2    @ 080d397c 0235
    adds r6,#0xc    @ 080d397e 0c36
    subs r7,#0x1    @ 080d3980 013f
    cmp r7,#0x0                              @ 080d3982 002f
    bge LAB_080d395c                         @ 080d3984 eada
    b LAB_080d3a0e                           @ 080d3986 42e0
DWORD_080d3988:
    .word  0x02000000                     @ 080d3988 00000002
DWORD_080d398c:
    .word  0x00006c2c                     @ 080d398c 2c6c0000
DWORD_080d3990:
    .word  0x02006ed0                     @ 080d3990 d06e0002
DWORD_080d3994:
    .word  font_jp_base_table             @ 080d3994 54f8e509
DWORD_080d3998:
    .word  0x00008c08                     @ 080d3998 088c0000
DWORD_080d399c:
    .word  0x00000c07                     @ 080d399c 070c0000
LAB_080d39a0:
    adds r0,r5,#0x0    @ 080d39a0 281c
    bl measure_string_pixel_width            @ 080d39a2 1cf067fc
    cmp r0,#0x1f                             @ 080d39a6 1f28
    bgt LAB_080d39e8                         @ 080d39a8 1edc
LAB_080d39aa:
    adds r0,r5,#0x0    @ 080d39aa 281c
    bl measure_string_pixel_width            @ 080d39ac 1cf062fc
    movs r4,#0x20    @ 080d39b0 2024
    subs r0,r4,r0    @ 080d39b2 201a
    lsrs r1,r0,#0x1f    @ 080d39b4 c10f
    adds r0,r0,r1    @ 080d39b6 4018
    asrs r0,r0,#0x1    @ 080d39b8 4010
    subs r0,#0x1    @ 080d39ba 0138
    ldr r2, DWORD_080d39e4                   @ 080d39bc 094a
    movs r1,#0x2    @ 080d39be 0221
    adds r3,r5,#0x0    @ 080d39c0 2b1c
    bl text_render_wrapper                   @ 080d39c2 1ff05bf8
    adds r0,r5,#0x0    @ 080d39c6 281c
    bl measure_string_pixel_width            @ 080d39c8 1cf054fc
    subs r4,r4,r0    @ 080d39cc 241a
    lsrs r0,r4,#0x1f    @ 080d39ce e00f
    adds r4,r4,r0    @ 080d39d0 2418
    asrs r4,r4,#0x1    @ 080d39d2 6410
    subs r4,#0x1    @ 080d39d4 013c
    adds r0,r4,#0x0    @ 080d39d6 201c
    movs r1,#0x2    @ 080d39d8 0221
    movs r2,#0x7    @ 080d39da 0722
    adds r3,r5,#0x0    @ 080d39dc 2b1c
    bl text_render_wrapper                   @ 080d39de 1ff04df8
    b LAB_080d3a0e                           @ 080d39e2 14e0
DWORD_080d39e4:
    .word  0x00008008                     @ 080d39e4 08800000
LAB_080d39e8:
    movs r4,#0x4    @ 080d39e8 0424
    movs r7,#0x3    @ 080d39ea 0327
LAB_080d39ec:
    ldrb r0,[r5,#0x0]                        @ 080d39ec 2878
    adds r1,r4,#0x0    @ 080d39ee 211c
    movs r2,#0x2    @ 080d39f0 0222
    ldr r3, DWORD_080d3a24                   @ 080d39f2 0c4b
    bl render_glyph_jp_single_layer          @ 080d39f4 1df0d6ff
    ldrb r0,[r5,#0x0]                        @ 080d39f8 2878
    adds r1,r4,#0x0    @ 080d39fa 211c
    movs r2,#0x2    @ 080d39fc 0222
    ldr r3, DWORD_080d3a28                   @ 080d39fe 0a4b
    bl render_glyph_jp_single_layer          @ 080d3a00 1df0d0ff
    adds r5,#0x1    @ 080d3a04 0135
    adds r4,#0x6    @ 080d3a06 0634
    subs r7,#0x1    @ 080d3a08 013f
    cmp r7,#0x0                              @ 080d3a0a 002f
    bge LAB_080d39ec                         @ 080d3a0c eeda
LAB_080d3a0e:
    .hword 0x4648    @ 080d3a0e 4846
    movs r1,#0x5    @ 080d3a10 0521
    bl __modsi3                              @ 080d3a12 3af043fe
    lsls r0,r0,#0x7    @ 080d3a16 c001
    ldr r4, DWORD_080d3a2c                   @ 080d3a18 044c
    adds r0,r0,r4    @ 080d3a1a 0019
    movs r1,#0x0    @ 080d3a1c 0021
    bl write_line_buf_to_bg_tile_vram        @ 080d3a1e 1ff0d9fe
    b LAB_080d3b4e                           @ 080d3a22 94e0
DWORD_080d3a24:
    .word  0x00008c08                     @ 080d3a24 088c0000
DWORD_080d3a28:
    .word  0x00000c07                     @ 080d3a28 070c0000
DWORD_080d3a2c:
    .word  0x06013c00                     @ 080d3a2c 003c0106
LAB_080d3a30:
    ldr r0,[sp,#0x8]                         @ 080d3a30 0298
    lsls r0,r0,#0x10    @ 080d3a32 0004
    lsrs r6,r0,#0x10    @ 080d3a34 060c
    ldr r0,[sp,#0x4]                         @ 080d3a36 0198
    lsls r0,r0,#0x10    @ 080d3a38 0004
    lsrs r4,r0,#0x10    @ 080d3a3a 040c
    cmp r4,#0x17                             @ 080d3a3c 172c
    bgt LAB_080d3a7c                         @ 080d3a3e 1ddc
    cmp r4,#0x16                             @ 080d3a40 162c
    blt LAB_080d3a7c                         @ 080d3a42 1bdb
    lsls r0,r5,#0x5    @ 080d3a44 6801
    ldr r5, DWORD_080d3a6c                   @ 080d3a46 094d
    adds r0,r0,r5    @ 080d3a48 4019
    subs r4,#0xf    @ 080d3a4a 0f3c
    lsls r1,r4,#0x5    @ 080d3a4c 6101
    ldr r2, DWORD_080d3a70                   @ 080d3a4e 084a
    adds r1,r1,r2    @ 080d3a50 8918
    movs r2,#0x20    @ 080d3a52 2022
    bl copy_bytes_by_halfword                @ 080d3a54 21f026fa
    ldr r1, DWORD_080d3a74                   @ 080d3a58 0649
    adds r0,r7,r1    @ 080d3a5a 7818
    lsls r0,r0,#0x5    @ 080d3a5c 4001
    add r0,r8                                @ 080d3a5e 4044
    lsls r4,r4,#0x7    @ 080d3a60 e401
    ldr r1, DWORD_080d3a78                   @ 080d3a62 0549
    adds r4,r4,r1    @ 080d3a64 6418
    adds r1,r4,#0x0    @ 080d3a66 211c
    b LAB_080d3afa                           @ 080d3a68 47e0
    .zero  0x2
DWORD_080d3a6c:
    .word  0x05000260                     @ 080d3a6c 60020005
DWORD_080d3a70:
    .word  0x0984e30c                     @ 080d3a70 0ce38409
DWORD_080d3a74:
    .word  0x000001e1                     @ 080d3a74 e1010000
DWORD_080d3a78:
    .word  0x0984de8c                     @ 080d3a78 8cde8409
LAB_080d3a7c:
    .hword 0x4648    @ 080d3a7c 4846
    movs r1,#0x5    @ 080d3a7e 0521
    bl __modsi3                              @ 080d3a80 3af00cfe
    adds r5,r0,#0x0    @ 080d3a84 051c
    lsls r0,r5,#0x5    @ 080d3a86 6801
    ldr r2, DWORD_080d3aac                   @ 080d3a88 084a
    adds r0,r0,r2    @ 080d3a8a 8018
    subs r4,r6,#0x1    @ 080d3a8c 741e
    lsls r1,r4,#0x5    @ 080d3a8e 6101
    ldr r2, DWORD_080d3ab0                   @ 080d3a90 074a
    adds r1,r1,r2    @ 080d3a92 8918
    movs r2,#0x20    @ 080d3a94 2022
    bl copy_bytes_by_halfword                @ 080d3a96 21f005fa
    lsls r5,r5,#0x7    @ 080d3a9a ed01
    ldr r3, DWORD_080d3ab4                   @ 080d3a9c 054b
    adds r5,r5,r3    @ 080d3a9e ed18
    lsls r4,r4,#0x7    @ 080d3aa0 e401
    ldr r0, DWORD_080d3ab8                   @ 080d3aa2 0548
    adds r4,r4,r0    @ 080d3aa4 2418
    adds r0,r5,#0x0    @ 080d3aa6 281c
    adds r1,r4,#0x0    @ 080d3aa8 211c
    b LAB_080d3afa                           @ 080d3aaa 26e0
DWORD_080d3aac:
    .word  0x05000260                     @ 080d3aac 60020005
DWORD_080d3ab0:
    .word  0x0984e30c                     @ 080d3ab0 0ce38409
DWORD_080d3ab4:
    .word  0x06013c20                     @ 080d3ab4 203c0106
DWORD_080d3ab8:
    .word  0x0984de8c                     @ 080d3ab8 8cde8409
LAB_080d3abc:
    ldr r0,[sp,#0x4]                         @ 080d3abc 0198
    lsls r0,r0,#0x10    @ 080d3abe 0004
    lsrs r4,r0,#0x10    @ 080d3ac0 040c
    cmp r4,#0x17                             @ 080d3ac2 172c
    bgt LAB_080d3b18                         @ 080d3ac4 28dc
    cmp r4,#0x16                             @ 080d3ac6 162c
    blt LAB_080d3b18                         @ 080d3ac8 26db
    ldr r1, DWORD_080d3b04                   @ 080d3aca 0e49
    movs r0,#0xb    @ 080d3acc 0b20
    muls r0,r6    @ 080d3ace 7043
    adds r0,#0x9    @ 080d3ad0 0930
    lsls r0,r0,#0x1    @ 080d3ad2 4000
    adds r0,r0,r1    @ 080d3ad4 4018
    ldrh r4,[r0,#0x0]                        @ 080d3ad6 0488
    cmp r4,#0x0                              @ 080d3ad8 002c
    beq LAB_080d3b4e                         @ 080d3ada 38d0
    lsls r0,r5,#0x5    @ 080d3adc 6801
    ldr r5, DWORD_080d3b08                   @ 080d3ade 0a4d
    adds r0,r0,r5    @ 080d3ae0 4019
    ldr r1, DWORD_080d3b0c                   @ 080d3ae2 0a49
    movs r2,#0x20    @ 080d3ae4 2022
    bl copy_bytes_by_halfword                @ 080d3ae6 21f0ddf9
    ldr r1, DWORD_080d3b10                   @ 080d3aea 0949
    adds r0,r7,r1    @ 080d3aec 7818
    lsls r0,r0,#0x5    @ 080d3aee 4001
    add r0,r8                                @ 080d3af0 4044
    subs r1,r4,#0x1    @ 080d3af2 611e
    lsls r1,r1,#0x7    @ 080d3af4 c901
    ldr r2, DWORD_080d3b14                   @ 080d3af6 074a
    adds r1,r1,r2    @ 080d3af8 8918
LAB_080d3afa:
    movs r2,#0x2    @ 080d3afa 0222
    movs r3,#0x2    @ 080d3afc 0223
    bl tile_2d_row_copy                      @ 080d3afe 23f0e9fc
    b LAB_080d3b4e                           @ 080d3b02 24e0
DWORD_080d3b04:
    .word  card_stats_table               @ 080d3b04 b8698109
DWORD_080d3b08:
    .word  0x05000260                     @ 080d3b08 60020005
DWORD_080d3b0c:
    .word  0x0984f3ac                     @ 080d3b0c acf38409
DWORD_080d3b10:
    .word  0x000001e1                     @ 080d3b10 e1010000
DWORD_080d3b14:
    .word  0x0984f0ac                     @ 080d3b14 acf08409
LAB_080d3b18:
    .hword 0x4648    @ 080d3b18 4846
    movs r1,#0x5    @ 080d3b1a 0521
    bl __modsi3                              @ 080d3b1c 3af0befd
    adds r5,r0,#0x0    @ 080d3b20 051c
    lsls r0,r5,#0x5    @ 080d3b22 6801
    ldr r2, DWORD_080d3b5c                   @ 080d3b24 0d4a
    adds r0,r0,r2    @ 080d3b26 8018
    subs r4,#0x1    @ 080d3b28 013c
    lsls r1,r4,#0x5    @ 080d3b2a 6101
    ldr r2, DWORD_080d3b60                   @ 080d3b2c 0c4a
    adds r1,r1,r2    @ 080d3b2e 8918
    movs r2,#0x20    @ 080d3b30 2022
    bl copy_bytes_by_halfword                @ 080d3b32 21f0b7f9
    lsls r5,r5,#0x7    @ 080d3b36 ed01
    ldr r3, DWORD_080d3b64                   @ 080d3b38 0a4b
    adds r5,r5,r3    @ 080d3b3a ed18
    lsls r4,r4,#0x7    @ 080d3b3c e401
    ldr r0, DWORD_080d3b68                   @ 080d3b3e 0a48
    adds r4,r4,r0    @ 080d3b40 2418
    adds r0,r5,#0x0    @ 080d3b42 281c
    adds r1,r4,#0x0    @ 080d3b44 211c
    movs r2,#0x2    @ 080d3b46 0222
    movs r3,#0x2    @ 080d3b48 0223
    bl tile_2d_row_copy                      @ 080d3b4a 23f0c3fc
LAB_080d3b4e:
    add sp,#0x24                             @ 080d3b4e 09b0
    pop {r3,r4}                              @ 080d3b50 18bc
    .hword 0x4698    @ 080d3b52 9846
    .hword 0x46a1    @ 080d3b54 a146
    pop {r4,r5,r6,r7}                        @ 080d3b56 f0bc
    pop {r0}                                 @ 080d3b58 01bc
    bx r0                                    @ 080d3b5a 0047
DWORD_080d3b5c:
    .word  0x05000260                     @ 080d3b5c 60020005
DWORD_080d3b60:
    .word  0x0984ee2c                     @ 080d3b60 2cee8409
DWORD_080d3b64:
    .word  0x06013c20                     @ 080d3b64 203c0106
DWORD_080d3b68:
    .word  0x0984e42c                     @ 080d3b68 2ce48409

@ Checks visibility relationship of two zone slots and returns a sort key. Called by sort_zone_slots_by_stat_insertion (0x080d403c) and sort_zone_slots_by_stat_quicksort (0x080d4148) as comparator during sort phase. r0, r1 each u16 slot_index (zero-extended via lsls/lsrs #0x10). Calls check_zone_slot_attr_visible for slot_a first; if not visible returns 1 (sort last). Then checks slot_b; if not visible jumps to LAB_080d3be4 returns -1. Both visible: reads card_stats from gDuelCtx (0x02020160) at stride=0x28, looks up compare_table (0x09832604) via ldrh, returns difference as compare key. Side effects: read-only (gDuelCtx + ROM table). Constants: gDuelCtx=0x02020160, card_stats_stride=0x28, compare_table=0x09832604.
compare_zone_slot_visibility_pair:
    push {r4,r5,r6,lr}                       @ 080d3b6c 70b5
    lsls r0,r0,#0x10    @ 080d3b6e 0004
    lsrs r0,r0,#0x10    @ 080d3b70 000c
    lsls r1,r1,#0x10    @ 080d3b72 0904
    lsrs r4,r1,#0x10    @ 080d3b74 0c0c
    ldr r2, DAT_080d3b98                     @ 080d3b76 084a
    lsls r1,r0,#0x2    @ 080d3b78 8100
    adds r1,r1,r0    @ 080d3b7a 0918
    lsls r1,r1,#0x3    @ 080d3b7c c900
    adds r1,r1,r2    @ 080d3b7e 8918
    ldr r5,[r1,#0x0]                         @ 080d3b80 0d68
    lsls r1,r4,#0x2    @ 080d3b82 a100
    adds r1,r1,r4    @ 080d3b84 0919
    lsls r1,r1,#0x3    @ 080d3b86 c900
    adds r1,r1,r2    @ 080d3b88 8918
    ldr r6,[r1,#0x0]                         @ 080d3b8a 0e68
    bl check_zone_slot_attr_visible          @ 080d3b8c fcf7fafd
    cmp r0,#0x0                              @ 080d3b90 0028
    beq LAB_080d3b9c                         @ 080d3b92 03d0
    movs r0,#0x1    @ 080d3b94 0120
    b LAB_080d3be8                           @ 080d3b96 27e0
DAT_080d3b98:
    .word  0x02020160                     @ 080d3b98 60010202
LAB_080d3b9c:
    adds r0,r4,#0x0    @ 080d3b9c 201c
    bl check_zone_slot_attr_visible          @ 080d3b9e fcf7f1fd
    cmp r0,#0x0                              @ 080d3ba2 0028
    bne LAB_080d3be4                         @ 080d3ba4 1ed1
    ldr r3, DAT_080d3bd8                     @ 080d3ba6 0c4b
    lsls r1,r5,#0x1    @ 080d3ba8 6900
    adds r1,r1,r5    @ 080d3baa 4919
    lsls r1,r1,#0x1    @ 080d3bac 4900
    ldr r0, DAT_080d3bdc                     @ 080d3bae 0b48
    ldr r2, DAT_080d3be0                     @ 080d3bb0 0b4a
    adds r0,r0,r2    @ 080d3bb2 8018
    ldrb r0,[r0,#0x0]                        @ 080d3bb4 0078
    lsls r2,r0,#0x1d    @ 080d3bb6 4207
    lsrs r0,r2,#0x1d    @ 080d3bb8 500f
    adds r1,r1,r0    @ 080d3bba 0918
    lsls r1,r1,#0x1    @ 080d3bbc 4900
    adds r1,r1,r3    @ 080d3bbe c918
    lsls r0,r6,#0x1    @ 080d3bc0 7000
    adds r0,r0,r6    @ 080d3bc2 8019
    lsls r0,r0,#0x1    @ 080d3bc4 4000
    lsrs r2,r2,#0x1d    @ 080d3bc6 520f
    adds r0,r0,r2    @ 080d3bc8 8018
    lsls r0,r0,#0x1    @ 080d3bca 4000
    adds r0,r0,r3    @ 080d3bcc c018
    ldrh r1,[r1,#0x0]                        @ 080d3bce 0988
    ldrh r0,[r0,#0x0]                        @ 080d3bd0 0088
    subs r0,r1,r0    @ 080d3bd2 081a
    b LAB_080d3be8                           @ 080d3bd4 08e0
    .zero  0x2
DAT_080d3bd8:
    .word  0x09832604                     @ 080d3bd8 04268309
DAT_080d3bdc:
    .word  0x02000000                     @ 080d3bdc 00000002
DAT_080d3be0:
    .word  0x00006c2c                     @ 080d3be0 2c6c0000
LAB_080d3be4:
    movs r0,#0x1    @ 080d3be4 0120
    rsbs r0,r0,#0    @ 080d3be6 4042
LAB_080d3be8:
    pop {r4,r5,r6}                           @ 080d3be8 70bc
    pop {r1}                                 @ 080d3bea 02bc
    bx r1                                    @ 080d3bec 0847
    .zero  0x2

@ Zone slot comparator with card type correction; returns sort key for zone sort pipeline. Called by sort_zone_slots_by_stat_insertion (0x080d403c) and sort_zone_slots_by_stat_quicksort (0x080d4148). Symmetric with compare_zone_slot_card_stat_pair (0x080d3c8c): push {r4-r7, lr}, high-reg save (0x4657/0x464e/0x4645); calls check_zone_slot_attr_visible for each slot; both visible: ldmia batch read 24 bytes card_stats; if r1 (slot_b raw)==0x16 returns -2; if 0x17 returns -3; else computes difference via card_stats_table. Invisible path returns -4 or 0x18. Side effects: read-only (IWRAM gDuelCtx + ROM). Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3e9c, card_type_range=[0x16..0x17], slot_stride=0x28.
compare_zone_slot_stat_with_type_alt:
    push {r4,r5,r6,r7,lr}                    @ 080d3bf0 f0b5
    .hword 0x4657    @ 080d3bf2 5746
    .hword 0x464e    @ 080d3bf4 4e46
    .hword 0x4645    @ 080d3bf6 4546
    push {r5,r6,r7}                          @ 080d3bf8 e0b4
    sub sp,#0x3c                             @ 080d3bfa 8fb0
    lsls r0,r0,#0x10    @ 080d3bfc 0004
    lsrs r0,r0,#0x10    @ 080d3bfe 000c
    lsls r1,r1,#0x10    @ 080d3c00 0904
    lsrs r1,r1,#0x10    @ 080d3c02 090c
    str r0,[sp,#0x24]                        @ 080d3c04 0990
    add r0,sp,#0x24                          @ 080d3c06 09a8
    str r1,[r0,#0x4]                         @ 080d3c08 4160
    movs r7,#0x0    @ 080d3c0a 0027
    add r1,sp,#0x2c                          @ 080d3c0c 0ba9
    .hword 0x4688    @ 080d3c0e 8846
    ldr r2, DAT_080d3c2c                     @ 080d3c10 064a
    .hword 0x4691    @ 080d3c12 9146
    .hword 0x4644    @ 080d3c14 4446
    adds r6,r0,#0x0    @ 080d3c16 061c
LAB_080d3c18:
    lsls r3,r7,#0x2    @ 080d3c18 bb00
    .hword 0x469a    @ 080d3c1a 9a46
    ldr r0,[r6,#0x0]                         @ 080d3c1c 3068
    bl check_zone_slot_attr_visible          @ 080d3c1e fcf7b1fd
    cmp r0,#0x0                              @ 080d3c22 0028
    beq LAB_080d3c30                         @ 080d3c24 04d0
    movs r0,#0x4    @ 080d3c26 0420
    rsbs r0,r0,#0    @ 080d3c28 4042
    b LAB_080d3c68                           @ 080d3c2a 1de0
DAT_080d3c2c:
    .word  0x02020160                     @ 080d3c2c 60010202
LAB_080d3c30:
    ldr r0,[r6,#0x0]                         @ 080d3c30 3068
    lsls r1,r0,#0x2    @ 080d3c32 8100
    adds r1,r1,r0    @ 080d3c34 0918
    lsls r1,r1,#0x3    @ 080d3c36 c900
    .hword 0x4668    @ 080d3c38 6846
    add r1,r9                                @ 080d3c3a 4944
    ldmia r1!,{r2,r3,r5}                     @ 080d3c3c 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3c3e 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3c40 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3c42 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3c44 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3c46 2cc0
    ldr r0,[sp,#0x14]                        @ 080d3c48 0598
    str r0,[r4,#0x0]                         @ 080d3c4a 2060
    add r0,sp,#0x34                          @ 080d3c4c 0da8
    add r0,r10                               @ 080d3c4e 5044
    ldr r1,[sp,#0x4]                         @ 080d3c50 0199
    str r1,[r0,#0x0]                         @ 080d3c52 0160
    cmp r1,#0x16                             @ 080d3c54 1629
    beq LAB_080d3c5e                         @ 080d3c56 02d0
    cmp r1,#0x17                             @ 080d3c58 1729
    beq LAB_080d3c64                         @ 080d3c5a 03d0
    b LAB_080d3c6a                           @ 080d3c5c 05e0
LAB_080d3c5e:
    movs r0,#0x2    @ 080d3c5e 0220
    rsbs r0,r0,#0    @ 080d3c60 4042
    b LAB_080d3c68                           @ 080d3c62 01e0
LAB_080d3c64:
    movs r0,#0x3    @ 080d3c64 0320
    rsbs r0,r0,#0    @ 080d3c66 4042
LAB_080d3c68:
    str r0,[r4,#0x0]                         @ 080d3c68 2060
LAB_080d3c6a:
    adds r4,#0x4    @ 080d3c6a 0434
    adds r6,#0x4    @ 080d3c6c 0436
    adds r7,#0x1    @ 080d3c6e 0137
    cmp r7,#0x1                              @ 080d3c70 012f
    ble LAB_080d3c18                         @ 080d3c72 d1dd
    .hword 0x4645    @ 080d3c74 4546
    ldr r0,[r5,#0x4]                         @ 080d3c76 6868
    ldr r1,[sp,#0x2c]                        @ 080d3c78 0b99
    subs r0,r0,r1    @ 080d3c7a 401a
    add sp,#0x3c                             @ 080d3c7c 0fb0
    pop {r3,r4,r5}                           @ 080d3c7e 38bc
    .hword 0x4698    @ 080d3c80 9846
    .hword 0x46a1    @ 080d3c82 a146
    .hword 0x46aa    @ 080d3c84 aa46
    pop {r4,r5,r6,r7}                        @ 080d3c86 f0bc
    pop {r1}                                 @ 080d3c88 02bc
    bx r1                                    @ 080d3c8a 0847

@ Compares card stats of two zone slots (r0, r1 each u16 slot index, zero-extended) and returns a result code. Internal: r8=gDuelCtx, r9=card_stats_table, r10=internal DAT. Main loop 2x (r7=0,1): calls check_zone_slot_attr_visible for each slot; if visible, reads stat word (slot_id*5*8+base) via ldmia batch copy 24 bytes; compares original r1 with 0x16/0x17: 0x16 -> rsbs r0=-2; 0x17 -> rsbs r0=-3; else continue; visibility fail -> rsbs r0=-4. Sibling cluster with FUN_080d3d28 / FUN_080d3dc4; differs only in return code constants (-2/-3 vs -1/-2 vs +9). Side effects: ldmia/stmia batch writes to stack-local (not external). Constants: gDuelCtx=0x02020160, slot_stride=5*8=40, loop_count=2, sentinel_16=0x16, sentinel_17=0x17.
compare_zone_slot_card_stat_pair:
    push {r4,r5,r6,r7,lr}                    @ 080d3c8c f0b5
    .hword 0x4657    @ 080d3c8e 5746
    .hword 0x464e    @ 080d3c90 4e46
    .hword 0x4645    @ 080d3c92 4546
    push {r5,r6,r7}                          @ 080d3c94 e0b4
    sub sp,#0x3c                             @ 080d3c96 8fb0
    lsls r0,r0,#0x10    @ 080d3c98 0004
    lsrs r0,r0,#0x10    @ 080d3c9a 000c
    lsls r1,r1,#0x10    @ 080d3c9c 0904
    lsrs r1,r1,#0x10    @ 080d3c9e 090c
    str r0,[sp,#0x24]                        @ 080d3ca0 0990
    add r0,sp,#0x24                          @ 080d3ca2 09a8
    str r1,[r0,#0x4]                         @ 080d3ca4 4160
    movs r7,#0x0    @ 080d3ca6 0027
    add r1,sp,#0x2c                          @ 080d3ca8 0ba9
    .hword 0x4688    @ 080d3caa 8846
    ldr r2, DAT_080d3cc8                     @ 080d3cac 064a
    .hword 0x4691    @ 080d3cae 9146
    .hword 0x4644    @ 080d3cb0 4446
    adds r6,r0,#0x0    @ 080d3cb2 061c
LAB_080d3cb4:
    lsls r3,r7,#0x2    @ 080d3cb4 bb00
    .hword 0x469a    @ 080d3cb6 9a46
    ldr r0,[r6,#0x0]                         @ 080d3cb8 3068
    bl check_zone_slot_attr_visible          @ 080d3cba fcf763fd
    cmp r0,#0x0                              @ 080d3cbe 0028
    beq LAB_080d3ccc                         @ 080d3cc0 04d0
    movs r0,#0x4    @ 080d3cc2 0420
    rsbs r0,r0,#0    @ 080d3cc4 4042
    b LAB_080d3d04                           @ 080d3cc6 1de0
DAT_080d3cc8:
    .word  0x02020160                     @ 080d3cc8 60010202
LAB_080d3ccc:
    ldr r0,[r6,#0x0]                         @ 080d3ccc 3068
    lsls r1,r0,#0x2    @ 080d3cce 8100
    adds r1,r1,r0    @ 080d3cd0 0918
    lsls r1,r1,#0x3    @ 080d3cd2 c900
    .hword 0x4668    @ 080d3cd4 6846
    add r1,r9                                @ 080d3cd6 4944
    ldmia r1!,{r2,r3,r5}                     @ 080d3cd8 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3cda 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3cdc 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3cde 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3ce0 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3ce2 2cc0
    ldr r0,[sp,#0x18]                        @ 080d3ce4 0698
    str r0,[r4,#0x0]                         @ 080d3ce6 2060
    add r0,sp,#0x34                          @ 080d3ce8 0da8
    add r0,r10                               @ 080d3cea 5044
    ldr r1,[sp,#0x4]                         @ 080d3cec 0199
    str r1,[r0,#0x0]                         @ 080d3cee 0160
    cmp r1,#0x16                             @ 080d3cf0 1629
    beq LAB_080d3cfa                         @ 080d3cf2 02d0
    cmp r1,#0x17                             @ 080d3cf4 1729
    beq LAB_080d3d00                         @ 080d3cf6 03d0
    b LAB_080d3d06                           @ 080d3cf8 05e0
LAB_080d3cfa:
    movs r0,#0x2    @ 080d3cfa 0220
    rsbs r0,r0,#0    @ 080d3cfc 4042
    b LAB_080d3d04                           @ 080d3cfe 01e0
LAB_080d3d00:
    movs r0,#0x3    @ 080d3d00 0320
    rsbs r0,r0,#0    @ 080d3d02 4042
LAB_080d3d04:
    str r0,[r4,#0x0]                         @ 080d3d04 2060
LAB_080d3d06:
    adds r4,#0x4    @ 080d3d06 0434
    adds r6,#0x4    @ 080d3d08 0436
    adds r7,#0x1    @ 080d3d0a 0137
    cmp r7,#0x1                              @ 080d3d0c 012f
    ble LAB_080d3cb4                         @ 080d3d0e d1dd
    .hword 0x4645    @ 080d3d10 4546
    ldr r0,[r5,#0x4]                         @ 080d3d12 6868
    ldr r1,[sp,#0x2c]                        @ 080d3d14 0b99
    subs r0,r0,r1    @ 080d3d16 401a
    add sp,#0x3c                             @ 080d3d18 0fb0
    pop {r3,r4,r5}                           @ 080d3d1a 38bc
    .hword 0x4698    @ 080d3d1c 9846
    .hword 0x46a1    @ 080d3d1e a146
    .hword 0x46aa    @ 080d3d20 aa46
    pop {r4,r5,r6,r7}                        @ 080d3d22 f0bc
    pop {r1}                                 @ 080d3d24 02bc
    bx r1                                    @ 080d3d26 0847

@ Alt variant of compare_zone_slot_card_stat_pair (0x080d3c8c). Fully symmetric structure: zero-extends r0/r1, loops 2x calling check_zone_slot_attr_visible, ldmia/stmia batch 24 bytes, compares r1 with 0x16/0x17. Difference: uses different DAT constants (DAT_080d3d64=0x02020160) and different result code assignments: r1==0x16 -> rsbs r0=-1; r1==0x17 -> rsbs r0=-2 (vs 0x080d3c8c which returns -2/-3). Invisible path returns -4 identically. One of the three-member sibling cluster. Side effects: stack-local temporaries only, no external EWRAM/VRAM. Constants: same as compare_zone_slot_card_stat_pair.
compare_zone_slot_card_stat_pair_alt:
    push {r4,r5,r6,r7,lr}                    @ 080d3d28 f0b5
    .hword 0x4657    @ 080d3d2a 5746
    .hword 0x464e    @ 080d3d2c 4e46
    .hword 0x4645    @ 080d3d2e 4546
    push {r5,r6,r7}                          @ 080d3d30 e0b4
    sub sp,#0x3c                             @ 080d3d32 8fb0
    lsls r0,r0,#0x10    @ 080d3d34 0004
    lsrs r0,r0,#0x10    @ 080d3d36 000c
    lsls r1,r1,#0x10    @ 080d3d38 0904
    lsrs r1,r1,#0x10    @ 080d3d3a 090c
    str r0,[sp,#0x24]                        @ 080d3d3c 0990
    add r0,sp,#0x24                          @ 080d3d3e 09a8
    str r1,[r0,#0x4]                         @ 080d3d40 4160
    movs r7,#0x0    @ 080d3d42 0027
    add r1,sp,#0x2c                          @ 080d3d44 0ba9
    .hword 0x4688    @ 080d3d46 8846
    ldr r2, DAT_080d3d64                     @ 080d3d48 064a
    .hword 0x4691    @ 080d3d4a 9146
    .hword 0x4644    @ 080d3d4c 4446
    adds r6,r0,#0x0    @ 080d3d4e 061c
LAB_080d3d50:
    lsls r3,r7,#0x2    @ 080d3d50 bb00
    .hword 0x469a    @ 080d3d52 9a46
    ldr r0,[r6,#0x0]                         @ 080d3d54 3068
    bl check_zone_slot_attr_visible          @ 080d3d56 fcf715fd
    cmp r0,#0x0                              @ 080d3d5a 0028
    beq LAB_080d3d68                         @ 080d3d5c 04d0
    movs r0,#0x4    @ 080d3d5e 0420
    rsbs r0,r0,#0    @ 080d3d60 4042
    b LAB_080d3da0                           @ 080d3d62 1de0
DAT_080d3d64:
    .word  0x02020160                     @ 080d3d64 60010202
LAB_080d3d68:
    ldr r0,[r6,#0x0]                         @ 080d3d68 3068
    lsls r1,r0,#0x2    @ 080d3d6a 8100
    adds r1,r1,r0    @ 080d3d6c 0918
    lsls r1,r1,#0x3    @ 080d3d6e c900
    .hword 0x4668    @ 080d3d70 6846
    add r1,r9                                @ 080d3d72 4944
    ldmia r1!,{r2,r3,r5}                     @ 080d3d74 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3d76 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3d78 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3d7a 2cc0
    ldmia r1!,{r2,r3,r5}                     @ 080d3d7c 2cc9
    stmia r0!,{r2,r3,r5}                     @ 080d3d7e 2cc0
    ldr r0,[sp,#0x10]                        @ 080d3d80 0498
    str r0,[r4,#0x0]                         @ 080d3d82 2060
    add r0,sp,#0x34                          @ 080d3d84 0da8
    add r0,r10                               @ 080d3d86 5044
    ldr r1,[sp,#0x4]                         @ 080d3d88 0199
    str r1,[r0,#0x0]                         @ 080d3d8a 0160
    cmp r1,#0x16                             @ 080d3d8c 1629
    beq LAB_080d3d96                         @ 080d3d8e 02d0
    cmp r1,#0x17                             @ 080d3d90 1729
    beq LAB_080d3d9c                         @ 080d3d92 03d0
    b LAB_080d3da2                           @ 080d3d94 05e0
LAB_080d3d96:
    movs r0,#0x1    @ 080d3d96 0120
    rsbs r0,r0,#0    @ 080d3d98 4042
    b LAB_080d3da0                           @ 080d3d9a 01e0
LAB_080d3d9c:
    movs r0,#0x2    @ 080d3d9c 0220
    rsbs r0,r0,#0    @ 080d3d9e 4042
LAB_080d3da0:
    str r0,[r4,#0x0]                         @ 080d3da0 2060
LAB_080d3da2:
    adds r4,#0x4    @ 080d3da2 0434
    adds r6,#0x4    @ 080d3da4 0436
    adds r7,#0x1    @ 080d3da6 0137
    cmp r7,#0x1                              @ 080d3da8 012f
    ble LAB_080d3d50                         @ 080d3daa d1dd
    .hword 0x4645    @ 080d3dac 4546
    ldr r0,[r5,#0x4]                         @ 080d3dae 6868
    ldr r1,[sp,#0x2c]                        @ 080d3db0 0b99
    subs r0,r0,r1    @ 080d3db2 401a
    add sp,#0x3c                             @ 080d3db4 0fb0
    pop {r3,r4,r5}                           @ 080d3db6 38bc
    .hword 0x4698    @ 080d3db8 9846
    .hword 0x46a1    @ 080d3dba a146
    .hword 0x46aa    @ 080d3dbc aa46
    pop {r4,r5,r6,r7}                        @ 080d3dbe f0bc
    pop {r1}                                 @ 080d3dc0 02bc
    bx r1                                    @ 080d3dc2 0847

@ Third variant of compare_zone_slot_card_stat_pair sibling cluster. Symmetric structure; difference: 'success' path returns +9 (movs r0,#9) rather than a negative code; invisible path still returns -4. Compares r1 against 0x16/0x17; on mismatch ('win' case) at LAB_080d3e10 computes return value from card_stats_table via multi-level index add r0,r8/r9/r10 and stores to [r5]. This variant returns the 'win' status code (positive). Side effects: [r5] := 0x9 (stack-local slot write, not external EWRAM). Constants: win_code=0x9, no_vis_code=-4, sentinel_16=0x16, sentinel_17=0x17.
compare_zone_slot_card_stat_pair_win:
    push {r4,r5,r6,r7,lr}                    @ 080d3dc4 f0b5
    .hword 0x4657    @ 080d3dc6 5746
    .hword 0x464e    @ 080d3dc8 4e46
    .hword 0x4645    @ 080d3dca 4546
    push {r5,r6,r7}                          @ 080d3dcc e0b4
    sub sp,#0x10                             @ 080d3dce 84b0
    lsls r0,r0,#0x10    @ 080d3dd0 0004
    lsrs r0,r0,#0x10    @ 080d3dd2 000c
    lsls r1,r1,#0x10    @ 080d3dd4 0904
    lsrs r1,r1,#0x10    @ 080d3dd6 090c
    str r0,[sp,#0x0]                         @ 080d3dd8 0090
    str r1,[sp,#0x4]                         @ 080d3dda 0191
    movs r6,#0x0    @ 080d3ddc 0026
    add r7,sp,#0x8                           @ 080d3dde 02af
    ldr r0, DAT_080d3e04                     @ 080d3de0 0848
    .hword 0x4682    @ 080d3de2 8246
    ldr r1, PTR_card_stats_table_080d3e08    @ 080d3de4 0849
    .hword 0x4689    @ 080d3de6 8946
    adds r5,r7,#0x0    @ 080d3de8 3d1c
    ldr r0, DAT_080d3e0c                     @ 080d3dea 0848
    .hword 0x4680    @ 080d3dec 8046
LAB_080d3dee:
    lsls r0,r6,#0x2    @ 080d3dee b000
    .hword 0x4669    @ 080d3df0 6946
    adds r4,r0,r1    @ 080d3df2 4418
    ldr r0,[r4,#0x0]                         @ 080d3df4 2068
    bl check_zone_slot_attr_visible          @ 080d3df6 fcf7c5fc
    cmp r0,#0x0                              @ 080d3dfa 0028
    beq LAB_080d3e10                         @ 080d3dfc 08d0
    movs r0,#0x9    @ 080d3dfe 0920
    b LAB_080d3e2e                           @ 080d3e00 15e0
    .zero  0x2
DAT_080d3e04:
    .word  0x09e4f1c4                     @ 080d3e04 c4f1e409
PTR_card_stats_table_080d3e08:
    .word  card_stats_table               @ 080d3e08 b8698109
DAT_080d3e0c:
    .word  0x02020160                     @ 080d3e0c 60010202
LAB_080d3e10:
    ldr r1,[r4,#0x0]                         @ 080d3e10 2168
    lsls r0,r1,#0x2    @ 080d3e12 8800
    adds r0,r0,r1    @ 080d3e14 4018
    lsls r0,r0,#0x3    @ 080d3e16 c000
    add r0,r8                                @ 080d3e18 4044
    ldr r1,[r0,#0x0]                         @ 080d3e1a 0168
    movs r0,#0xb    @ 080d3e1c 0b20
    muls r0,r1    @ 080d3e1e 4843
    adds r0,#0x8    @ 080d3e20 0830
    lsls r0,r0,#0x1    @ 080d3e22 4000
    add r0,r9                                @ 080d3e24 4844
    ldrh r0,[r0,#0x0]                        @ 080d3e26 0088
    lsls r0,r0,#0x2    @ 080d3e28 8000
    add r0,r10                               @ 080d3e2a 5044
    ldr r0,[r0,#0x0]                         @ 080d3e2c 0068
LAB_080d3e2e:
    str r0,[r5,#0x0]                         @ 080d3e2e 2860
    adds r5,#0x4    @ 080d3e30 0435
    adds r6,#0x1    @ 080d3e32 0136
    cmp r6,#0x1                              @ 080d3e34 012e
    ble LAB_080d3dee                         @ 080d3e36 dadd
    ldr r0,[sp,#0x8]                         @ 080d3e38 0298
    ldr r1,[r7,#0x4]                         @ 080d3e3a 7968
    subs r0,r0,r1    @ 080d3e3c 401a
    add sp,#0x10                             @ 080d3e3e 04b0
    pop {r3,r4,r5}                           @ 080d3e40 38bc
    .hword 0x4698    @ 080d3e42 9846
    .hword 0x46a1    @ 080d3e44 a146
    .hword 0x46aa    @ 080d3e46 aa46
    pop {r4,r5,r6,r7}                        @ 080d3e48 f0bc
    pop {r1}                                 @ 080d3e4a 02bc
    bx r1                                    @ 080d3e4c 0847
    .zero  0x2

@ Zone slot comparator with ATK/DEF value correction; returns sort key. Called by sort_zone_slots_by_stat_insertion (0x080d403c) and sort_zone_slots_by_stat_quicksort (0x080d4148). Symmetric with compare_zone_slot_card_stat_pair cluster; difference: uses additional ATK/DEF offset tables (0x09e4f310 for type 0x16, 0x09e4f32c for type 0x17, 0x09e4f2ac fallback). r5 loop_count=0 init; invisible path returns 0x18. End: r0=sp[0x2c]-r7[0x4] difference returned. Side effects: read-only (IWRAM/ROM). Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3e9c, atk_table_16=0x09e4f310, atk_table_17=0x09e4f32c, fallback=0x09e4f2ac, slot_stride=0x28, loop_count=2.
compare_zone_slot_card_stat_with_atk:
    push {r4,r5,r6,r7,lr}                    @ 080d3e50 f0b5
    .hword 0x4657    @ 080d3e52 5746
    .hword 0x464e    @ 080d3e54 4e46
    .hword 0x4645    @ 080d3e56 4546
    push {r5,r6,r7}                          @ 080d3e58 e0b4
    sub sp,#0x48                             @ 080d3e5a 92b0
    lsls r0,r0,#0x10    @ 080d3e5c 0004
    lsrs r0,r0,#0x10    @ 080d3e5e 000c
    lsls r1,r1,#0x10    @ 080d3e60 0904
    lsrs r1,r1,#0x10    @ 080d3e62 090c
    movs r2,#0x0    @ 080d3e64 0022
    .hword 0x4690    @ 080d3e66 9046
    str r0,[sp,#0x24]                        @ 080d3e68 0990
    add r0,sp,#0x24                          @ 080d3e6a 09a8
    str r1,[r0,#0x4]                         @ 080d3e6c 4160
    movs r5,#0x0    @ 080d3e6e 0025
    str r5,[sp,#0x40]                        @ 080d3e70 1095
    add r7,sp,#0x2c                          @ 080d3e72 0baf
    .hword 0x46b9    @ 080d3e74 b946
    ldr r3, DAT_080d3e98                     @ 080d3e76 084b
    .hword 0x464c    @ 080d3e78 4c46
    adds r6,r0,#0x0    @ 080d3e7a 061c
    ldr r0, PTR_card_stats_table_080d3e9c    @ 080d3e7c 0748
    .hword 0x4682    @ 080d3e7e 8246
LAB_080d3e80:
    ldr r1,[sp,#0x40]                        @ 080d3e80 1099
    lsls r1,r1,#0x2    @ 080d3e82 8900
    str r1,[sp,#0x44]                        @ 080d3e84 1191
    ldr r0,[r6,#0x0]                         @ 080d3e86 3068
    str r3,[sp,#0x3c]                        @ 080d3e88 0f93
    bl check_zone_slot_attr_visible          @ 080d3e8a fcf77bfc
    ldr r3,[sp,#0x3c]                        @ 080d3e8e 0f9b
    cmp r0,#0x0                              @ 080d3e90 0028
    beq LAB_080d3ea0                         @ 080d3e92 05d0
    movs r0,#0x18    @ 080d3e94 1820
    b LAB_080d3f24                           @ 080d3e96 45e0
DAT_080d3e98:
    .word  0x09e4f284                     @ 080d3e98 84f2e409
PTR_card_stats_table_080d3e9c:
    .word  card_stats_table               @ 080d3e9c b8698109
LAB_080d3ea0:
    ldr r0,[r6,#0x0]                         @ 080d3ea0 3068
    lsls r1,r0,#0x2    @ 080d3ea2 8100
    adds r1,r1,r0    @ 080d3ea4 0918
    lsls r1,r1,#0x3    @ 080d3ea6 c900
    .hword 0x4668    @ 080d3ea8 6846
    ldr r2, DAT_080d3efc                     @ 080d3eaa 144a
    adds r1,r1,r2    @ 080d3eac 8918
    ldmia r1!,{r2,r5,r7}                     @ 080d3eae a4c9
    stmia r0!,{r2,r5,r7}                     @ 080d3eb0 a4c0
    ldmia r1!,{r2,r5,r7}                     @ 080d3eb2 a4c9
    stmia r0!,{r2,r5,r7}                     @ 080d3eb4 a4c0
    ldmia r1!,{r2,r5,r7}                     @ 080d3eb6 a4c9
    stmia r0!,{r2,r5,r7}                     @ 080d3eb8 a4c0
    ldr r0,[sp,#0x8]                         @ 080d3eba 0298
    str r0,[r4,#0x0]                         @ 080d3ebc 2060
    add r0,sp,#0x34                          @ 080d3ebe 0da8
    ldr r5,[sp,#0x44]                        @ 080d3ec0 119d
    adds r0,r5,r0    @ 080d3ec2 2818
    ldr r2,[sp,#0x4]                         @ 080d3ec4 019a
    str r2,[r0,#0x0]                         @ 080d3ec6 0260
    adds r0,r2,#0x0    @ 080d3ec8 101c
    subs r0,#0x16    @ 080d3eca 1638
    cmp r0,#0x1                              @ 080d3ecc 0128
    bhi LAB_080d3ee0                         @ 080d3ece 07d8
    ldr r1,[sp,#0x0]                         @ 080d3ed0 0099
    movs r0,#0xb    @ 080d3ed2 0b20
    muls r0,r1    @ 080d3ed4 4843
    adds r0,#0x9    @ 080d3ed6 0930
    lsls r0,r0,#0x1    @ 080d3ed8 4000
    add r0,r10                               @ 080d3eda 5044
    ldrh r0,[r0,#0x0]                        @ 080d3edc 0088
    .hword 0x4680    @ 080d3ede 8046
LAB_080d3ee0:
    cmp r2,#0x16                             @ 080d3ee0 162a
    beq LAB_080d3f04                         @ 080d3ee2 0fd0
    cmp r2,#0x17                             @ 080d3ee4 172a
    bne LAB_080d3f1c                         @ 080d3ee6 19d1
    ldr r1, DAT_080d3f00                     @ 080d3ee8 0549
    .hword 0x4647    @ 080d3eea 4746
    lsls r0,r7,#0x2    @ 080d3eec b800
    adds r0,r0,r1    @ 080d3eee 4018
    ldr r1,[r0,#0x0]                         @ 080d3ef0 0168
    adds r1,#0x7    @ 080d3ef2 0731
    ldr r0,[r3,#0x24]                        @ 080d3ef4 586a
    adds r0,r0,r1    @ 080d3ef6 4018
    b LAB_080d3f24                           @ 080d3ef8 14e0
    .zero  0x2
DAT_080d3efc:
    .word  0x02020160                     @ 080d3efc 60010202
DAT_080d3f00:
    .word  0x09e4f32c                     @ 080d3f00 2cf3e409
LAB_080d3f04:
    ldr r1, DAT_080d3f18                     @ 080d3f04 0449
    .hword 0x4642    @ 080d3f06 4246
    lsls r0,r2,#0x2    @ 080d3f08 9000
    adds r0,r0,r1    @ 080d3f0a 4018
    ldr r1,[r3,#0x20]                        @ 080d3f0c 196a
    ldr r0,[r0,#0x0]                         @ 080d3f0e 0068
    adds r1,r1,r0    @ 080d3f10 0918
    str r1,[r4,#0x0]                         @ 080d3f12 2160
    b LAB_080d3f26                           @ 080d3f14 07e0
    .zero  0x2
DAT_080d3f18:
    .word  0x09e4f310                     @ 080d3f18 10f3e409
LAB_080d3f1c:
    ldr r0,[r4,#0x0]                         @ 080d3f1c 2068
    lsls r0,r0,#0x2    @ 080d3f1e 8000
    adds r0,r0,r3    @ 080d3f20 c018
    ldr r0,[r0,#0x0]                         @ 080d3f22 0068
LAB_080d3f24:
    str r0,[r4,#0x0]                         @ 080d3f24 2060
LAB_080d3f26:
    adds r4,#0x4    @ 080d3f26 0434
    adds r6,#0x4    @ 080d3f28 0436
    ldr r5,[sp,#0x40]                        @ 080d3f2a 109d
    adds r5,#0x1    @ 080d3f2c 0135
    str r5,[sp,#0x40]                        @ 080d3f2e 1095
    cmp r5,#0x1                              @ 080d3f30 012d
    ble LAB_080d3e80                         @ 080d3f32 a5dd
    ldr r0,[sp,#0x2c]                        @ 080d3f34 0b98
    .hword 0x464f    @ 080d3f36 4f46
    ldr r1,[r7,#0x4]                         @ 080d3f38 7968
    subs r0,r0,r1    @ 080d3f3a 401a
    add sp,#0x48                             @ 080d3f3c 12b0
    pop {r3,r4,r5}                           @ 080d3f3e 38bc
    .hword 0x4698    @ 080d3f40 9846
    .hword 0x46a1    @ 080d3f42 a146
    .hword 0x46aa    @ 080d3f44 aa46
    pop {r4,r5,r6,r7}                        @ 080d3f46 f0bc
    pop {r1}                                 @ 080d3f48 02bc
    bx r1                                    @ 080d3f4a 0847

@ Zone slot comparator with level/position offset correction; returns sort key. Called by sort_zone_slots_by_stat_insertion (0x080d403c) and sort_zone_slots_by_stat_quicksort (0x080d4148). Symmetric with compare_zone_slot_card_stat_with_atk but uses different table pointer (PTR_card_stats_table@080d3f94). r3=0 init; invisible path returns 0x27 (sentinel). Type [0x16..0x17] paths query 0x09e4f310/0x09e4f32c + sp[0x38] cache; 0x17 path also reads 0x09e4f2ac[+0x5c] accumulated offset. End: r0=sp[0x2c]-r7[0x4] difference. Side effects: read-only. Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3f94, atk_table_16=0x09e4f310, atk_table_17=0x09e4f32c, fallback_table=0x09e4f2ac, return_invisible=0x27.
compare_zone_slot_card_stat_with_level:
    push {r4,r5,r6,r7,lr}                    @ 080d3f4c f0b5
    .hword 0x4657    @ 080d3f4e 5746
    .hword 0x464e    @ 080d3f50 4e46
    .hword 0x4645    @ 080d3f52 4546
    push {r5,r6,r7}                          @ 080d3f54 e0b4
    sub sp,#0x3c                             @ 080d3f56 8fb0
    lsls r0,r0,#0x10    @ 080d3f58 0004
    lsrs r0,r0,#0x10    @ 080d3f5a 000c
    lsls r1,r1,#0x10    @ 080d3f5c 0904
    lsrs r1,r1,#0x10    @ 080d3f5e 090c
    movs r2,#0x0    @ 080d3f60 0022
    str r2,[sp,#0x38]                        @ 080d3f62 0e92
    str r0,[sp,#0x24]                        @ 080d3f64 0990
    add r0,sp,#0x24                          @ 080d3f66 09a8
    str r1,[r0,#0x4]                         @ 080d3f68 4160
    movs r3,#0x0    @ 080d3f6a 0023
    add r6,sp,#0x2c                          @ 080d3f6c 0bae
    .hword 0x46b0    @ 080d3f6e b046
    ldr r7, DAT_080d3f90                     @ 080d3f70 074f
    .hword 0x46ba    @ 080d3f72 ba46
    .hword 0x4644    @ 080d3f74 4446
    adds r5,r0,#0x0    @ 080d3f76 051c
    ldr r0, PTR_card_stats_table_080d3f94    @ 080d3f78 0648
    .hword 0x4681    @ 080d3f7a 8146
LAB_080d3f7c:
    ldr r0,[r5,#0x0]                         @ 080d3f7c 2868
    str r3,[sp,#0x34]                        @ 080d3f7e 0d93
    bl check_zone_slot_attr_visible          @ 080d3f80 fcf700fc
    ldr r3,[sp,#0x34]                        @ 080d3f84 0d9b
    cmp r0,#0x0                              @ 080d3f86 0028
    beq LAB_080d3f98                         @ 080d3f88 06d0
    movs r0,#0x27    @ 080d3f8a 2720
    b LAB_080d4014                           @ 080d3f8c 42e0
    .zero  0x2
DAT_080d3f90:
    .word  0x02020160                     @ 080d3f90 60010202
PTR_card_stats_table_080d3f94:
    .word  card_stats_table               @ 080d3f94 b8698109
LAB_080d3f98:
    ldr r0,[r5,#0x0]                         @ 080d3f98 2868
    lsls r1,r0,#0x2    @ 080d3f9a 8100
    adds r1,r1,r0    @ 080d3f9c 0918
    lsls r1,r1,#0x3    @ 080d3f9e c900
    .hword 0x4668    @ 080d3fa0 6846
    add r1,r10                               @ 080d3fa2 5144
    ldmia r1!,{r2,r6,r7}                     @ 080d3fa4 c4c9
    stmia r0!,{r2,r6,r7}                     @ 080d3fa6 c4c0
    ldmia r1!,{r2,r6,r7}                     @ 080d3fa8 c4c9
    stmia r0!,{r2,r6,r7}                     @ 080d3faa c4c0
    ldmia r1!,{r2,r6,r7}                     @ 080d3fac c4c9
    stmia r0!,{r2,r6,r7}                     @ 080d3fae c4c0
    ldr r2,[sp,#0x4]                         @ 080d3fb0 019a
    str r2,[r4,#0x0]                         @ 080d3fb2 2260
    adds r0,r2,#0x0    @ 080d3fb4 101c
    subs r0,#0x16    @ 080d3fb6 1638
    cmp r0,#0x1                              @ 080d3fb8 0128
    bhi LAB_080d3fcc                         @ 080d3fba 07d8
    ldr r1,[sp,#0x0]                         @ 080d3fbc 0099
    movs r0,#0xb    @ 080d3fbe 0b20
    muls r0,r1    @ 080d3fc0 4843
    adds r0,#0x9    @ 080d3fc2 0930
    lsls r0,r0,#0x1    @ 080d3fc4 4000
    add r0,r9                                @ 080d3fc6 4844
    ldrh r0,[r0,#0x0]                        @ 080d3fc8 0088
    str r0,[sp,#0x38]                        @ 080d3fca 0e90
LAB_080d3fcc:
    cmp r2,#0x16                             @ 080d3fcc 162a
    beq LAB_080d3ff0                         @ 080d3fce 0fd0
    cmp r2,#0x17                             @ 080d3fd0 172a
    bne LAB_080d400c                         @ 080d3fd2 1bd1
    ldr r1, DAT_080d3fe8                     @ 080d3fd4 0449
    ldr r2,[sp,#0x38]                        @ 080d3fd6 0e9a
    lsls r0,r2,#0x2    @ 080d3fd8 9000
    adds r0,r0,r1    @ 080d3fda 4018
    ldr r1,[r0,#0x0]                         @ 080d3fdc 0168
    adds r1,#0x7    @ 080d3fde 0731
    ldr r6, DAT_080d3fec                     @ 080d3fe0 024e
    ldr r0,[r6,#0x5c]                        @ 080d3fe2 f06d
    adds r0,r0,r1    @ 080d3fe4 4018
    b LAB_080d4014                           @ 080d3fe6 15e0
DAT_080d3fe8:
    .word  0x09e4f32c                     @ 080d3fe8 2cf3e409
DAT_080d3fec:
    .word  0x09e4f2ac                     @ 080d3fec acf2e409
LAB_080d3ff0:
    ldr r1, DAT_080d4004                     @ 080d3ff0 0449
    ldr r7,[sp,#0x38]                        @ 080d3ff2 0e9f
    lsls r0,r7,#0x2    @ 080d3ff4 b800
    adds r0,r0,r1    @ 080d3ff6 4018
    ldr r2, DAT_080d4008                     @ 080d3ff8 034a
    ldr r1,[r2,#0x58]                        @ 080d3ffa 916d
    ldr r0,[r0,#0x0]                         @ 080d3ffc 0068
    adds r1,r1,r0    @ 080d3ffe 0918
    str r1,[r4,#0x0]                         @ 080d4000 2160
    b LAB_080d4016                           @ 080d4002 08e0
DAT_080d4004:
    .word  0x09e4f310                     @ 080d4004 10f3e409
DAT_080d4008:
    .word  0x09e4f2ac                     @ 080d4008 acf2e409
LAB_080d400c:
    lsls r0,r2,#0x2    @ 080d400c 9000
    ldr r6, DAT_080d4038                     @ 080d400e 0a4e
    adds r0,r0,r6    @ 080d4010 8019
    ldr r0,[r0,#0x0]                         @ 080d4012 0068
LAB_080d4014:
    str r0,[r4,#0x0]                         @ 080d4014 2060
LAB_080d4016:
    adds r4,#0x4    @ 080d4016 0434
    adds r5,#0x4    @ 080d4018 0435
    adds r3,#0x1    @ 080d401a 0133
    cmp r3,#0x1                              @ 080d401c 012b
    ble LAB_080d3f7c                         @ 080d401e addd
    ldr r0,[sp,#0x2c]                        @ 080d4020 0b98
    .hword 0x4647    @ 080d4022 4746
    ldr r1,[r7,#0x4]                         @ 080d4024 7968
    subs r0,r0,r1    @ 080d4026 401a
    add sp,#0x3c                             @ 080d4028 0fb0
    pop {r3,r4,r5}                           @ 080d402a 38bc
    .hword 0x4698    @ 080d402c 9846
    .hword 0x46a1    @ 080d402e a146
    .hword 0x46aa    @ 080d4030 aa46
    pop {r4,r5,r6,r7}                        @ 080d4032 f0bc
    pop {r1}                                 @ 080d4034 02bc
    bx r1                                    @ 080d4036 0847
DAT_080d4038:
    .word  0x09e4f2ac                     @ 080d4038 acf2e409

@ Insertion sort on zone slot id list; sorts slots by card stat descending. Called by sort_zone_slots_by_stat_quicksort (0x080d4148) as base case when count<=6. r0=slot_list_ptr (u16* array, 2 bytes/entry), r1=slot_count. Standard insertion sort: outer i=0..n-2; inner calls FUN_0810e5d0 (card stat comparator) for each pair; on swap: ldrh/strh exchange 2-byte slot ids. r9 (high-reg alias for gPrng+0x808 sliding ptr) used for compare table access; LAB_080d4100 performs strh swap on two halfwords. Side effects: strh writes to [gPrng+0x808+r6*2] and [gPrng+0x808+sp[0x4]] (slot id swap). Constants: gDuelCtx=0x02020160, queue_base=0x0201bcc0, queue_offset=0x808, swap_size=2, compare_fn=FUN_0810e5d0.
sort_zone_slots_by_stat_insertion:
    push {r4,r5,r6,r7,lr}                    @ 080d403c f0b5
    .hword 0x4657    @ 080d403e 5746
    .hword 0x464e    @ 080d4040 4e46
    .hword 0x4645    @ 080d4042 4546
    push {r5,r6,r7}                          @ 080d4044 e0b4
    sub sp,#0x10                             @ 080d4046 84b0
    .hword 0x4681    @ 080d4048 8146
    str r1,[sp,#0x0]                         @ 080d404a 0091
    movs r0,#0x0    @ 080d404c 0020
    subs r1,#0x1    @ 080d404e 0139
    cmp r0,r1                                @ 080d4050 8842
    bge LAB_080d4114                         @ 080d4052 5fda
    str r1,[sp,#0x8]                         @ 080d4054 0291
LAB_080d4056:
    adds r6,r0,#0x0    @ 080d4056 061c
    adds r0,r6,#0x1    @ 080d4058 701c
    .hword 0x4680    @ 080d405a 8046
    .hword 0x4645    @ 080d405c 4546
    lsls r1,r6,#0x1    @ 080d405e 7100
    str r1,[sp,#0x4]                         @ 080d4060 0191
    ldr r2,[sp,#0x0]                         @ 080d4062 009a
    cmp r8,r2                                @ 080d4064 9045
    bge LAB_080d40fc                         @ 080d4066 49da
    ldr r3, DAT_080d40dc                     @ 080d4068 1c4b
    lsls r0,r0,#0x1    @ 080d406a 4000
    .hword 0x4649    @ 080d406c 4946
    adds r7,r0,r1    @ 080d406e 4718
    movs r2,#0xb0    @ 080d4070 b022
    lsls r2,r2,#0x6    @ 080d4072 9201
    adds r2,r2,r3    @ 080d4074 d218
    .hword 0x4692    @ 080d4076 9246
LAB_080d4078:
    ldr r1, DAT_080d40e0                     @ 080d4078 1949
    adds r0,r3,r1    @ 080d407a 5818
    ldrh r0,[r0,#0x0]                        @ 080d407c 0088
    lsls r2,r0,#0x13    @ 080d407e c204
    lsrs r2,r2,#0x18    @ 080d4080 120e
    subs r2,#0x1    @ 080d4082 013a
    lsls r2,r2,#0x2    @ 080d4084 9200
    ldr r0, DAT_080d40e4                     @ 080d4086 1748
    adds r2,r2,r0    @ 080d4088 1218
    lsls r0,r6,#0x1    @ 080d408a 7000
    .hword 0x4649    @ 080d408c 4946
    adds r4,r0,r1    @ 080d408e 4418
    ldrh r0,[r4,#0x0]                        @ 080d4090 2088
    ldrh r1,[r7,#0x0]                        @ 080d4092 3988
    ldr r2,[r2,#0x0]                         @ 080d4094 1268
    str r3,[sp,#0xc]                         @ 080d4096 0393
    bl invoke_r2                             @ 080d4098 3af09afa
    adds r2,r0,#0x0    @ 080d409c 021c
    ldr r3,[sp,#0xc]                         @ 080d409e 039b
    cmp r2,#0x0                              @ 080d40a0 002a
    bne LAB_080d40c6                         @ 080d40a2 10d1
    ldrh r4,[r4,#0x0]                        @ 080d40a4 2488
    lsls r1,r4,#0x1    @ 080d40a6 6100
    add r1,r10                               @ 080d40a8 5144
    ldrh r2,[r7,#0x0]                        @ 080d40aa 3a88
    lsls r0,r2,#0x1    @ 080d40ac 5000
    add r0,r10                               @ 080d40ae 5044
    ldrh r1,[r1,#0x0]                        @ 080d40b0 0988
    ldrh r0,[r0,#0x0]                        @ 080d40b2 0088
    subs r2,r1,r0    @ 080d40b4 0a1a
    ldr r0, DAT_080d40e8                     @ 080d40b6 0c48
    adds r1,r3,r0    @ 080d40b8 1918
    movs r0,#0x8    @ 080d40ba 0820
    ldrb r1,[r1,#0x0]                        @ 080d40bc 0978
    ands r0,r1    @ 080d40be 0840
    cmp r0,#0x0                              @ 080d40c0 0028
    beq LAB_080d40d4                         @ 080d40c2 07d0
    rsbs r2,r2,#0    @ 080d40c4 5242
LAB_080d40c6:
    ldr r0, DAT_080d40e8                     @ 080d40c6 0848
    adds r1,r3,r0    @ 080d40c8 1918
    movs r0,#0x8    @ 080d40ca 0820
    ldrb r1,[r1,#0x0]                        @ 080d40cc 0978
    ands r0,r1    @ 080d40ce 0840
    cmp r0,#0x0                              @ 080d40d0 0028
    bne LAB_080d40ec                         @ 080d40d2 0bd1
LAB_080d40d4:
    cmp r2,#0x0                              @ 080d40d4 002a
    ble LAB_080d40f2                         @ 080d40d6 0cdd
    b LAB_080d40f0                           @ 080d40d8 0ae0
    .zero  0x2
DAT_080d40dc:
    .word  0x02020160                     @ 080d40dc 60010202
DAT_080d40e0:
    .word  0x00002f52                     @ 080d40e0 522f0000
DAT_080d40e4:
    .word  0x09e5abdc                     @ 080d40e4 dcabe509
DAT_080d40e8:
    .word  0x00002f51                     @ 080d40e8 512f0000
LAB_080d40ec:
    cmp r2,#0x0                              @ 080d40ec 002a
    bge LAB_080d40f2                         @ 080d40ee 00da
LAB_080d40f0:
    adds r6,r5,#0x0    @ 080d40f0 2e1c
LAB_080d40f2:
    adds r7,#0x2    @ 080d40f2 0237
    adds r5,#0x1    @ 080d40f4 0135
    ldr r1,[sp,#0x0]                         @ 080d40f6 0099
    cmp r5,r1                                @ 080d40f8 8d42
    blt LAB_080d4078                         @ 080d40fa bddb
LAB_080d40fc:
    lsls r1,r6,#0x1    @ 080d40fc 7100
    add r1,r9                                @ 080d40fe 4944
    ldrh r3,[r1,#0x0]                        @ 080d4100 0b88
    ldr r2,[sp,#0x4]                         @ 080d4102 019a
    add r2,r9                                @ 080d4104 4a44
    ldrh r0,[r2,#0x0]                        @ 080d4106 1088
    strh r0,[r1,#0x0]                        @ 080d4108 0880
    strh r3,[r2,#0x0]                        @ 080d410a 1380
    .hword 0x4640    @ 080d410c 4046
    ldr r2,[sp,#0x8]                         @ 080d410e 029a
    cmp r0,r2                                @ 080d4110 9042
    blt LAB_080d4056                         @ 080d4112 a0db
LAB_080d4114:
    add sp,#0x10                             @ 080d4114 04b0
    pop {r3,r4,r5}                           @ 080d4116 38bc
    .hword 0x4698    @ 080d4118 9846
    .hword 0x46a1    @ 080d411a a146
    .hword 0x46aa    @ 080d411c aa46
    pop {r4,r5,r6,r7}                        @ 080d411e f0bc
    pop {r0}                                 @ 080d4120 01bc
    bx r0                                    @ 080d4122 0047
    ROM_INCBIN 0xd4124, 0x24

@ Quicksort on zone slot id list; sorts slots by card stat descending. Called by setup_zone_slot_sorted_view (0x080d4268); self-recursive. r0=slot_list_ptr (u16* array), r1=slot_count saved to sp[0x8]. count<=6 delegates to sort_zone_slots_by_stat_insertion (0x080d403c); else selects pivot arr[count/2+count%2], swaps with arr[0], partitions via FUN_0810e5d0 comparator, then recurses on left/right subarrays. High-regs r7/r6/r5/r8/r9/r10 callee-saved via .hword 0x4657/0x464e/0x4645. Side effects: strh slot id swaps in-place in slot_list_ptr array. Constants: insertion_threshold=6, compare_fn=FUN_0810e5d0.
sort_zone_slots_by_stat_quicksort:
    push {r4,r5,r6,r7,lr}                    @ 080d4148 f0b5
    .hword 0x4657    @ 080d414a 5746
    .hword 0x464e    @ 080d414c 4e46
    .hword 0x4645    @ 080d414e 4546
    push {r5,r6,r7}                          @ 080d4150 e0b4
    sub sp,#0xc                              @ 080d4152 83b0
    adds r6,r0,#0x0    @ 080d4154 061c
    str r1,[sp,#0x8]                         @ 080d4156 0291
LAB_080d4158:
    ldr r0,[sp,#0x8]                         @ 080d4158 0298
    cmp r0,#0x6                              @ 080d415a 0628
    ble LAB_080d4250                         @ 080d415c 78dd
    movs r3,#0x0    @ 080d415e 0023
    asrs r0,r0,#0x1f    @ 080d4160 c017
    .hword 0x4682    @ 080d4162 8246
    ldr r1,[sp,#0x8]                         @ 080d4164 0299
    cmp r1,#0x1                              @ 080d4166 0129
    ble LAB_080d420a                         @ 080d4168 4fdd
    ldr r2, DWORD_080d41dc                   @ 080d416a 1c4a
    .hword 0x4691    @ 080d416c 9146
    adds r4,r6,#0x2    @ 080d416e b41c
    adds r5,r6,#0x0    @ 080d4170 351c
    subs r1,#0x1    @ 080d4172 0139
    .hword 0x4688    @ 080d4174 8846
LAB_080d4176:
    ldr r0, DWORD_080d41e0                   @ 080d4176 1a48
    add r0,r9                                @ 080d4178 4844
    ldrh r0,[r0,#0x0]                        @ 080d417a 0088
    lsls r2,r0,#0x13    @ 080d417c c204
    lsrs r2,r2,#0x18    @ 080d417e 120e
    subs r2,#0x1    @ 080d4180 013a
    lsls r2,r2,#0x2    @ 080d4182 9200
    ldr r7, DWORD_080d41e4                   @ 080d4184 174f
    adds r2,r2,r7    @ 080d4186 d219
    ldrh r0,[r4,#0x0]                        @ 080d4188 2088
    ldrh r1,[r6,#0x0]                        @ 080d418a 3188
    ldr r2,[r2,#0x0]                         @ 080d418c 1268
    str r3,[sp,#0x0]                         @ 080d418e 0093
    bl invoke_r2                             @ 080d4190 3af01efa
    adds r2,r0,#0x0    @ 080d4194 021c
    ldr r3,[sp,#0x0]                         @ 080d4196 009b
    cmp r2,#0x0                              @ 080d4198 002a
    bne LAB_080d41c8                         @ 080d419a 15d1
    ldrh r0,[r4,#0x0]                        @ 080d419c 2088
    lsls r2,r0,#0x1    @ 080d419e 4200
    movs r1,#0xb0    @ 080d41a0 b021
    lsls r1,r1,#0x6    @ 080d41a2 8901
    add r1,r9                                @ 080d41a4 4944
    adds r2,r2,r1    @ 080d41a6 5218
    .hword 0x4694    @ 080d41a8 9446
    ldrh r2,[r6,#0x0]                        @ 080d41aa 3288
    lsls r0,r2,#0x1    @ 080d41ac 5000
    adds r0,r0,r1    @ 080d41ae 4018
    .hword 0x4667    @ 080d41b0 6746
    ldrh r7,[r7,#0x0]                        @ 080d41b2 3f88
    ldrh r0,[r0,#0x0]                        @ 080d41b4 0088
    subs r2,r7,r0    @ 080d41b6 3a1a
    ldr r1, DWORD_080d41e8                   @ 080d41b8 0b49
    add r1,r9                                @ 080d41ba 4944
    movs r0,#0x8    @ 080d41bc 0820
    ldrb r1,[r1,#0x0]                        @ 080d41be 0978
    ands r0,r1    @ 080d41c0 0840
    cmp r0,#0x0                              @ 080d41c2 0028
    beq LAB_080d41d6                         @ 080d41c4 07d0
    rsbs r2,r2,#0    @ 080d41c6 5242
LAB_080d41c8:
    ldr r1, DWORD_080d41e8                   @ 080d41c8 0749
    add r1,r9                                @ 080d41ca 4944
    movs r0,#0x8    @ 080d41cc 0820
    ldrb r1,[r1,#0x0]                        @ 080d41ce 0978
    ands r0,r1    @ 080d41d0 0840
    cmp r0,#0x0                              @ 080d41d2 0028
    bne LAB_080d41ec                         @ 080d41d4 0ad1
LAB_080d41d6:
    cmp r2,#0x0                              @ 080d41d6 002a
    bge LAB_080d41fc                         @ 080d41d8 10da
    b LAB_080d41f0                           @ 080d41da 09e0
DWORD_080d41dc:
    .word  0x02020160                     @ 080d41dc 60010202
DWORD_080d41e0:
    .word  0x00002f52                     @ 080d41e0 522f0000
DWORD_080d41e4:
    .word  0x09e5abdc                     @ 080d41e4 dcabe509
DWORD_080d41e8:
    .word  0x00002f51                     @ 080d41e8 512f0000
LAB_080d41ec:
    cmp r2,#0x0                              @ 080d41ec 002a
    ble LAB_080d41fc                         @ 080d41ee 05dd
LAB_080d41f0:
    adds r5,#0x2    @ 080d41f0 0235
    adds r3,#0x1    @ 080d41f2 0133
    ldrh r1,[r5,#0x0]                        @ 080d41f4 2988
    ldrh r0,[r4,#0x0]                        @ 080d41f6 2088
    strh r0,[r5,#0x0]                        @ 080d41f8 2880
    strh r1,[r4,#0x0]                        @ 080d41fa 2180
LAB_080d41fc:
    adds r4,#0x2    @ 080d41fc 0234
    movs r1,#0x1    @ 080d41fe 0121
    rsbs r1,r1,#0    @ 080d4200 4942
    add r8,r1                                @ 080d4202 8844
    .hword 0x4642    @ 080d4204 4246
    cmp r2,#0x0                              @ 080d4206 002a
    bne LAB_080d4176                         @ 080d4208 b5d1
LAB_080d420a:
    ldrh r1,[r6,#0x0]                        @ 080d420a 3188
    lsls r4,r3,#0x1    @ 080d420c 5c00
    adds r2,r4,r6    @ 080d420e a219
    ldrh r0,[r2,#0x0]                        @ 080d4210 1088
    strh r0,[r6,#0x0]                        @ 080d4212 3080
    strh r1,[r2,#0x0]                        @ 080d4214 1180
    ldr r5,[sp,#0x8]                         @ 080d4216 029d
    .hword 0x4657    @ 080d4218 5746
    subs r0,r5,r7    @ 080d421a e81b
    asrs r0,r0,#0x1    @ 080d421c 4010
    cmp r3,r0                                @ 080d421e 8342
    bge LAB_080d423c                         @ 080d4220 0cda
    adds r0,r6,#0x0    @ 080d4222 301c
    adds r1,r3,#0x0    @ 080d4224 191c
    str r3,[sp,#0x0]                         @ 080d4226 0093
    bl sort_zone_slots_by_stat_quicksort     @ 080d4228 fff78eff
    adds r0,r4,#0x2    @ 080d422c a01c
    adds r6,r6,r0    @ 080d422e 3618
    adds r0,r5,#0x0    @ 080d4230 281c
    subs r0,#0x1    @ 080d4232 0138
    ldr r3,[sp,#0x0]                         @ 080d4234 009b
    subs r0,r0,r3    @ 080d4236 c01a
    str r0,[sp,#0x8]                         @ 080d4238 0290
    b LAB_080d4158                           @ 080d423a 8de7
LAB_080d423c:
    adds r0,r2,#0x2    @ 080d423c 901c
    ldr r2,[sp,#0x8]                         @ 080d423e 029a
    subs r1,r2,r3    @ 080d4240 d11a
    subs r1,#0x1    @ 080d4242 0139
    str r3,[sp,#0x0]                         @ 080d4244 0093
    bl sort_zone_slots_by_stat_quicksort     @ 080d4246 fff77fff
    ldr r3,[sp,#0x0]                         @ 080d424a 009b
    str r3,[sp,#0x8]                         @ 080d424c 0293
    b LAB_080d4158                           @ 080d424e 83e7
LAB_080d4250:
    adds r0,r6,#0x0    @ 080d4250 301c
    ldr r1,[sp,#0x8]                         @ 080d4252 0299
    bl sort_zone_slots_by_stat_insertion     @ 080d4254 fff7f2fe
    add sp,#0xc                              @ 080d4258 03b0
    pop {r3,r4,r5}                           @ 080d425a 38bc
    .hword 0x4698    @ 080d425c 9846
    .hword 0x46a1    @ 080d425e a146
    .hword 0x46aa    @ 080d4260 aa46
    pop {r4,r5,r6,r7}                        @ 080d4262 f0bc
    pop {r0}                                 @ 080d4264 01bc
    bx r0                                    @ 080d4266 0047

@ Initializes zone slot sort and triggers card icon rendering. Called by tick_zone_card_list_state_machine (0x080d4478) when state==2. No explicit input params (r0-r3 overwritten by internal loads). Flow: (1) reads gDuelCtx+0x2f52 halfword bits[12:5] (0xff<<5 mask) for active slot count; if 0 goes to sort path; else reads gDuelCtx+0x2f57/0x2f58 for type_combined and compares with count: if count<type_combined clears VRAM 0x0601f000+i*2 (strh 0). (2) reads 0x2f57/0x2f58/0x2f53/0x2f54 type_combined2; if >0 calls dispatch_zone_card_anim_by_type. (3) loop calls render_zone_slot_card_icon_tile and load_card_list_small_image for each slot. (4) clears gDuelCtx+0x2f54 bits[12:5] and 0x2f56, calls dispatch_zone_card_display_by_mode. Side effects: strh writes VRAM 0x0601f000 (zero loop); gDuelCtx+0x2f54 &= 0xffe01fff; gDuelCtx+0x2f56 &= 0xffffe01f.
setup_zone_slot_sorted_view:
    push {r4,r5,r6,r7,lr}                    @ 080d4268 f0b5
    .hword 0x4657    @ 080d426a 5746
    .hword 0x464e    @ 080d426c 4e46
    .hword 0x4645    @ 080d426e 4546
    push {r5,r6,r7}                          @ 080d4270 e0b4
    ldr r2, DWORD_080d42c8                   @ 080d4272 154a
    ldr r0, DWORD_080d42cc                   @ 080d4274 1548
    adds r1,r2,r0    @ 080d4276 1118
    movs r0,#0xff    @ 080d4278 ff20
    lsls r0,r0,#0x5    @ 080d427a 4001
    ldrh r1,[r1,#0x0]                        @ 080d427c 0988
    ands r0,r1    @ 080d427e 0840
    cmp r0,#0x0                              @ 080d4280 0028
    bne LAB_080d42d8                         @ 080d4282 29d1
    movs r5,#0x0    @ 080d4284 0025
    ldr r1, DWORD_080d42d0                   @ 080d4286 1249
    adds r4,r2,r1    @ 080d4288 5418
    ldrb r3,[r4,#0x0]                        @ 080d428a 2378
    lsrs r1,r3,#0x5    @ 080d428c 5909
    ldr r6, DWORD_080d42d4                   @ 080d428e 114e
    adds r3,r2,r6    @ 080d4290 9319
    movs r0,#0x1f    @ 080d4292 1f20
    ldrb r7,[r3,#0x0]                        @ 080d4294 1f78
    ands r0,r7    @ 080d4296 3840
    lsls r0,r0,#0x3    @ 080d4298 c000
    orrs r0,r1    @ 080d429a 0843
    cmp r5,r0                                @ 080d429c 8542
    bge LAB_080d42f8                         @ 080d429e 2bda
    adds r6,r3,#0x0    @ 080d42a0 1e1c
    movs r0,#0xa0    @ 080d42a2 a020
    lsls r0,r0,#0x6    @ 080d42a4 8001
    adds r2,r2,r0    @ 080d42a6 1218
    adds r3,r4,#0x0    @ 080d42a8 231c
    movs r4,#0x1f    @ 080d42aa 1f24
LAB_080d42ac:
    strh r5,[r2,#0x0]                        @ 080d42ac 1580
    adds r2,#0x2    @ 080d42ae 0232
    adds r5,#0x1    @ 080d42b0 0135
    ldrb r7,[r3,#0x0]                        @ 080d42b2 1f78
    lsrs r1,r7,#0x5    @ 080d42b4 7909
    adds r0,r4,#0x0    @ 080d42b6 201c
    ldrb r7,[r6,#0x0]                        @ 080d42b8 3778
    ands r0,r7    @ 080d42ba 3840
    lsls r0,r0,#0x3    @ 080d42bc c000
    orrs r0,r1    @ 080d42be 0843
    cmp r5,r0                                @ 080d42c0 8542
    blt LAB_080d42ac                         @ 080d42c2 f3db
    b LAB_080d42f8                           @ 080d42c4 18e0
    .zero  0x2
DWORD_080d42c8:
    .word  0x02020160                     @ 080d42c8 60010202
DWORD_080d42cc:
    .word  0x00002f52                     @ 080d42cc 522f0000
DWORD_080d42d0:
    .word  0x00002f57                     @ 080d42d0 572f0000
DWORD_080d42d4:
    .word  0x00002f58                     @ 080d42d4 582f0000
LAB_080d42d8:
    movs r1,#0xa0    @ 080d42d8 a021
    lsls r1,r1,#0x6    @ 080d42da 8901
    adds r0,r2,r1    @ 080d42dc 5018
    ldr r3, DWORD_080d4370                   @ 080d42de 244b
    adds r1,r2,r3    @ 080d42e0 d118
    ldrb r1,[r1,#0x0]                        @ 080d42e2 0978
    lsrs r3,r1,#0x5    @ 080d42e4 4b09
    ldr r6, DWORD_080d4374                   @ 080d42e6 234e
    adds r2,r2,r6    @ 080d42e8 9219
    movs r1,#0x1f    @ 080d42ea 1f21
    ldrb r2,[r2,#0x0]                        @ 080d42ec 1278
    ands r1,r2    @ 080d42ee 1140
    lsls r1,r1,#0x3    @ 080d42f0 c900
    orrs r1,r3    @ 080d42f2 1943
    bl sort_zone_slots_by_stat_quicksort     @ 080d42f4 fff728ff
LAB_080d42f8:
    movs r5,#0x0    @ 080d42f8 0025
    ldr r0, DWORD_080d4378                   @ 080d42fa 1f48
    ldr r7, DWORD_080d4370                   @ 080d42fc 1c4f
    adds r6,r0,r7    @ 080d42fe c619
    ldrb r1,[r6,#0x0]                        @ 080d4300 3178
    lsrs r2,r1,#0x5    @ 080d4302 4a09
    ldr r3, DWORD_080d4374                   @ 080d4304 1b4b
    adds r4,r0,r3    @ 080d4306 c418
    movs r1,#0x1f    @ 080d4308 1f21
    ldrb r7,[r4,#0x0]                        @ 080d430a 2778
    ands r1,r7    @ 080d430c 3940
    lsls r1,r1,#0x3    @ 080d430e c900
    orrs r1,r2    @ 080d4310 1143
    adds r3,r0,#0x0    @ 080d4312 031c
    cmp r5,r1                                @ 080d4314 8d42
    bge LAB_080d434e                         @ 080d4316 1ada
    movs r0,#0xb0    @ 080d4318 b020
    lsls r0,r0,#0x6    @ 080d431a 8001
    adds r0,r0,r3    @ 080d431c c018
    .hword 0x4680    @ 080d431e 8046
    .hword 0x46a1    @ 080d4320 a146
    movs r1,#0xa0    @ 080d4322 a021
    lsls r1,r1,#0x6    @ 080d4324 8901
    adds r2,r3,r1    @ 080d4326 5a18
    adds r4,r6,#0x0    @ 080d4328 341c
    movs r6,#0x1f    @ 080d432a 1f26
    .hword 0x46b2    @ 080d432c b246
LAB_080d432e:
    ldrh r7,[r2,#0x0]                        @ 080d432e 1788
    lsls r0,r7,#0x1    @ 080d4330 7800
    add r0,r8                                @ 080d4332 4044
    strh r5,[r0,#0x0]                        @ 080d4334 0580
    adds r2,#0x2    @ 080d4336 0232
    adds r5,#0x1    @ 080d4338 0135
    ldrb r0,[r4,#0x0]                        @ 080d433a 2078
    lsrs r1,r0,#0x5    @ 080d433c 4109
    .hword 0x4650    @ 080d433e 5046
    .hword 0x464e    @ 080d4340 4e46
    ldrb r6,[r6,#0x0]                        @ 080d4342 3678
    ands r0,r6    @ 080d4344 3040
    lsls r0,r0,#0x3    @ 080d4346 c000
    orrs r0,r1    @ 080d4348 0843
    cmp r5,r0                                @ 080d434a 8542
    blt LAB_080d432e                         @ 080d434c efdb
LAB_080d434e:
    ldr r7, DWORD_080d437c                   @ 080d434e 0b4f
    adds r0,r3,r7    @ 080d4350 d819
    ldrb r0,[r0,#0x0]                        @ 080d4352 0078
    lsrs r2,r0,#0x5    @ 080d4354 4209
    ldr r0, DWORD_080d4380                   @ 080d4356 0a48
    adds r1,r3,r0    @ 080d4358 1918
    movs r4,#0x1f    @ 080d435a 1f24
    adds r0,r4,#0x0    @ 080d435c 201c
    ldrb r1,[r1,#0x0]                        @ 080d435e 0978
    ands r0,r1    @ 080d4360 0840
    lsls r0,r0,#0x3    @ 080d4362 c000
    orrs r0,r2    @ 080d4364 1043
    cmp r0,#0x0                              @ 080d4366 0028
    beq LAB_080d4384                         @ 080d4368 0cd0
    bl dispatch_zone_card_anim_by_type       @ 080d436a fdf723fc
    b LAB_080d444a                           @ 080d436e 6ce0
DWORD_080d4370:
    .word  0x00002f57                     @ 080d4370 572f0000
DWORD_080d4374:
    .word  0x00002f58                     @ 080d4374 582f0000
DWORD_080d4378:
    .word  0x02020160                     @ 080d4378 60010202
DWORD_080d437c:
    .word  0x00002f53                     @ 080d437c 532f0000
DWORD_080d4380:
    .word  0x00002f54                     @ 080d4380 542f0000
LAB_080d4384:
    ldr r1, DWORD_080d4458                   @ 080d4384 3449
    adds r0,r3,r1    @ 080d4386 5818
    ldrb r0,[r0,#0x0]                        @ 080d4388 0078
    lsrs r2,r0,#0x5    @ 080d438a 4209
    ldr r6, DWORD_080d445c                   @ 080d438c 334e
    adds r1,r3,r6    @ 080d438e 9919
    adds r0,r4,#0x0    @ 080d4390 201c
    ldrb r1,[r1,#0x0]                        @ 080d4392 0978
    ands r0,r1    @ 080d4394 0840
    lsls r0,r0,#0x3    @ 080d4396 c000
    orrs r0,r2    @ 080d4398 1043
    movs r7,#0x5    @ 080d439a 0527
    .hword 0x46ba    @ 080d439c ba46
    cmp r0,#0x5                              @ 080d439e 0528
    bhi LAB_080d43a4                         @ 080d43a0 00d8
    .hword 0x4682    @ 080d43a2 8246
LAB_080d43a4:
    movs r5,#0x0    @ 080d43a4 0025
    cmp r5,r10                               @ 080d43a6 5545
    bge LAB_080d441a                         @ 080d43a8 37da
    .hword 0x4699    @ 080d43aa 9946
    ldr r0, DWORD_080d4460                   @ 080d43ac 2c48
    add r0,r9                                @ 080d43ae 4844
    .hword 0x4680    @ 080d43b0 8046
LAB_080d43b2:
    lsls r0,r5,#0x1    @ 080d43b2 6800
    movs r1,#0xa0    @ 080d43b4 a021
    lsls r1,r1,#0x6    @ 080d43b6 8901
    add r1,r9                                @ 080d43b8 4944
    adds r0,r0,r1    @ 080d43ba 4018
    ldrh r4,[r0,#0x0]                        @ 080d43bc 0488
    lsls r0,r4,#0x2    @ 080d43be a000
    adds r0,r0,r4    @ 080d43c0 0019
    lsls r0,r0,#0x3    @ 080d43c2 c000
    add r0,r9                                @ 080d43c4 4844
    ldr r6,[r0,#0x0]                         @ 080d43c6 0668
    movs r7,#0x1    @ 080d43c8 0127
    adds r0,r5,#0x0    @ 080d43ca 281c
    bl render_zone_slot_card_icon_tile       @ 080d43cc fff730fa
    movs r0,#0x0    @ 080d43d0 0020
    .hword 0x4641    @ 080d43d2 4146
    strh r0,[r1,#0x0]                        @ 080d43d4 0880
    adds r0,r4,#0x0    @ 080d43d6 201c
    bl check_zone_slot_attr_visible          @ 080d43d8 fcf7d4f9
    cmp r0,#0x0                              @ 080d43dc 0028
    beq LAB_080d43e2                         @ 080d43de 00d0
    movs r7,#0x0    @ 080d43e0 0027
LAB_080d43e2:
    adds r0,r5,#0x0    @ 080d43e2 281c
    movs r1,#0x3    @ 080d43e4 0321
    bl __modsi3                              @ 080d43e6 3af059f9
    adds r4,r0,#0x0    @ 080d43ea 041c
    lsls r4,r4,#0x3    @ 080d43ec e400
    movs r3,#0x88    @ 080d43ee 8823
    lsls r3,r3,#0x2    @ 080d43f0 9b00
    adds r4,r4,r3    @ 080d43f2 e418
    adds r0,r5,#0x0    @ 080d43f4 281c
    movs r1,#0x3    @ 080d43f6 0321
    bl __divsi3                              @ 080d43f8 3af004f9
    lsls r0,r0,#0x7    @ 080d43fc c001
    adds r4,r4,r0    @ 080d43fe 2418
    lsls r4,r4,#0x10    @ 080d4400 2404
    lsrs r4,r4,#0x10    @ 080d4402 240c
    adds r0,r6,#0x0    @ 080d4404 301c
    adds r1,r7,#0x0    @ 080d4406 391c
    movs r2,#0x0    @ 080d4408 0022
    adds r3,r4,#0x0    @ 080d440a 231c
    bl load_card_list_small_image            @ 080d440c eef7d6ff
    movs r6,#0x2    @ 080d4410 0226
    add r8,r6                                @ 080d4412 b044
    adds r5,#0x1    @ 080d4414 0135
    cmp r5,r10                               @ 080d4416 5545
    blt LAB_080d43b2                         @ 080d4418 cbdb
LAB_080d441a:
    ldr r2, DWORD_080d4464                   @ 080d441a 124a
    ldr r7, DWORD_080d4468                   @ 080d441c 124f
    adds r3,r2,r7    @ 080d441e d319
    ldr r0,[r3,#0x0]                         @ 080d4420 1868
    ldr r1, DWORD_080d446c                   @ 080d4422 1249
    ands r0,r1    @ 080d4424 0840
    str r0,[r3,#0x0]                         @ 080d4426 1860
    ldr r0, DWORD_080d4470                   @ 080d4428 1148
    adds r1,r2,r0    @ 080d442a 1118
    ldr r0, DWORD_080d4474                   @ 080d442c 1148
    ldrh r3,[r1,#0x0]                        @ 080d442e 0b88
    ands r0,r3    @ 080d4430 1840
    strh r0,[r1,#0x0]                        @ 080d4432 0880
    movs r6,#0xa0    @ 080d4434 a026
    lsls r6,r6,#0x6    @ 080d4436 b601
    adds r2,r2,r6    @ 080d4438 9219
    ldrh r4,[r2,#0x0]                        @ 080d443a 1488
    adds r0,r4,#0x0    @ 080d443c 201c
    bl check_zone_slot_attr_visible          @ 080d443e fcf7a1f9
    adds r1,r0,#0x0    @ 080d4442 011c
    adds r0,r4,#0x0    @ 080d4444 201c
    bl dispatch_zone_card_display_by_mode    @ 080d4446 fcf7e7f9
LAB_080d444a:
    pop {r3,r4,r5}                           @ 080d444a 38bc
    .hword 0x4698    @ 080d444c 9846
    .hword 0x46a1    @ 080d444e a146
    .hword 0x46aa    @ 080d4450 aa46
    pop {r4,r5,r6,r7}                        @ 080d4452 f0bc
    pop {r0}                                 @ 080d4454 01bc
    bx r0                                    @ 080d4456 0047
DWORD_080d4458:
    .word  0x00002f57                     @ 080d4458 572f0000
DWORD_080d445c:
    .word  0x00002f58                     @ 080d445c 582f0000
DWORD_080d4460:
    .word  0x00002e42                     @ 080d4460 422e0000
DWORD_080d4464:
    .word  0x02020160                     @ 080d4464 60010202
DWORD_080d4468:
    .word  0x00002f54                     @ 080d4468 542f0000
DWORD_080d446c:
    .word  0xffe01fff                     @ 080d446c ff1fe0ff
DWORD_080d4470:
    .word  0x00002f56                     @ 080d4470 562f0000
DWORD_080d4474:
    .word  0xffffe01f                     @ 080d4474 1fe0ffff

@ Single-frame update of zone card list display state machine. Called by tick_zone_card_list_view (0x080d2ef4) in zone main loop. Reads gDuelCtx+0x2f4d byte as state and dispatches: state=0: checks gPrng+0xa4*2 bit6 flag, calls check_field_scroll_phase_ready if needed, then writes gDuelCtx+0x2f54 bits[12:5]=0x60|0x20 and exits; state=1: calls setup_zone_slot_sorted_view (0x080d4268); state=2: calls setup_zone_slot_sorted_view. All paths write gDuelCtx+0x2f4d (state advance) and return 1 fixed. Side effects: strb gDuelCtx+0x2f4d (state); strh gDuelCtx+0x2f54 (display bits); strb gDuelCtx+0x2f51 bit1 (display enable). Constants: gDuelCtx=0x02020160, state_offset=0x2f4d, display_offset=0x2f54, gPrng_flag=0xa4*2=0x148, flag_bit6=0x40, flag_bit7=0x80, flag_bit5=0x20.
tick_zone_card_list_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 080d4478 f0b5
    ldr r6, DWORD_080d4494                   @ 080d447a 064e
    ldr r0, DWORD_080d4498                   @ 080d447c 0648
    adds r7,r6,r0    @ 080d447e 3718
    ldrb r0,[r7,#0x0]                        @ 080d4480 3878
    adds r3,r6,#0x0    @ 080d4482 331c
    cmp r0,#0x1                              @ 080d4484 0128
    bne LAB_080d448a                         @ 080d4486 00d1
    b LAB_080d45d4                           @ 080d4488 a4e0
LAB_080d448a:
    cmp r0,#0x1                              @ 080d448a 0128
    bgt LAB_080d449c                         @ 080d448c 06dc
    cmp r0,#0x0                              @ 080d448e 0028
    beq LAB_080d44a4                         @ 080d4490 08d0
    b LAB_080d45ee                           @ 080d4492 ace0
DWORD_080d4494:
    .word  0x02020160                     @ 080d4494 60010202
DWORD_080d4498:
    .word  0x00002f4d                     @ 080d4498 4d2f0000
LAB_080d449c:
    cmp r0,#0x2                              @ 080d449c 0228
    bne LAB_080d44a2                         @ 080d449e 00d1
    b LAB_080d45d8                           @ 080d44a0 9ae0
LAB_080d44a2:
    b LAB_080d45ee                           @ 080d44a2 a4e0
LAB_080d44a4:
    ldr r0, DWORD_080d44d4                   @ 080d44a4 0b48
    movs r1,#0xa4    @ 080d44a6 a421
    lsls r1,r1,#0x1    @ 080d44a8 4900
    adds r0,r0,r1    @ 080d44aa 4018
    ldrh r1,[r0,#0x0]                        @ 080d44ac 0188
    movs r0,#0x40    @ 080d44ae 4020
    ands r0,r1    @ 080d44b0 0840
    cmp r0,#0x0                              @ 080d44b2 0028
    beq LAB_080d44e0                         @ 080d44b4 14d0
    bl check_field_scroll_phase_ready        @ 080d44b6 fef793f8
    cmp r0,#0x0                              @ 080d44ba 0028
    bne LAB_080d44c0                         @ 080d44bc 00d1
    b LAB_080d45bc                           @ 080d44be 7de0
LAB_080d44c0:
    ldr r2, DWORD_080d44d8                   @ 080d44c0 054a
    adds r0,r6,r2    @ 080d44c2 b018
    ldr r1, DWORD_080d44dc                   @ 080d44c4 0549
    ldrh r2,[r0,#0x0]                        @ 080d44c6 0288
    ands r1,r2    @ 080d44c8 1140
    movs r2,#0x60    @ 080d44ca 6022
LAB_080d44cc:
    orrs r1,r2    @ 080d44cc 1143
    strh r1,[r0,#0x0]                        @ 080d44ce 0180
    b LAB_080d45ee                           @ 080d44d0 8de0
    .zero  0x2
DWORD_080d44d4:
    .word  gPrng                          @ 080d44d4 40000003
DWORD_080d44d8:
    .word  0x00002f54                     @ 080d44d8 542f0000
DWORD_080d44dc:
    .word  0xffffe01f                     @ 080d44dc 1fe0ffff
LAB_080d44e0:
    movs r0,#0x80    @ 080d44e0 8020
    ands r0,r1    @ 080d44e2 0840
    cmp r0,#0x0                              @ 080d44e4 0028
    beq LAB_080d4500                         @ 080d44e6 0bd0
    ldr r1, DWORD_080d44f8                   @ 080d44e8 0349
    adds r0,r6,r1    @ 080d44ea 7018
    ldr r1, DWORD_080d44fc                   @ 080d44ec 0349
    ldrh r2,[r0,#0x0]                        @ 080d44ee 0288
    ands r1,r2    @ 080d44f0 1140
    movs r2,#0x20    @ 080d44f2 2022
    b LAB_080d44cc                           @ 080d44f4 eae7
    .zero  0x2
DWORD_080d44f8:
    .word  0x00002f54                     @ 080d44f8 542f0000
DWORD_080d44fc:
    .word  0xffffe01f                     @ 080d44fc 1fe0ffff
LAB_080d4500:
    movs r0,#0x20    @ 080d4500 2020
    ands r0,r1    @ 080d4502 0840
    cmp r0,#0x0                              @ 080d4504 0028
    beq LAB_080d456c                         @ 080d4506 31d0
    ldr r0, DWORD_080d4530                   @ 080d4508 0948
    adds r5,r6,r0    @ 080d450a 3518
    ldrh r2,[r5,#0x0]                        @ 080d450c 2a88
    movs r0,#0xff    @ 080d450e ff20
    lsls r0,r0,#0x5    @ 080d4510 4001
    ands r0,r2    @ 080d4512 1040
    cmp r0,#0x0                              @ 080d4514 0028
    beq LAB_080d4538                         @ 080d4516 0fd0
    lsls r0,r2,#0x13    @ 080d4518 d004
    lsrs r0,r0,#0x18    @ 080d451a 000e
    subs r0,#0x1    @ 080d451c 0138
    movs r1,#0xff    @ 080d451e ff21
    ands r0,r1    @ 080d4520 0840
    lsls r0,r0,#0x5    @ 080d4522 4001
    ldr r1, DWORD_080d4534                   @ 080d4524 0349
    ands r1,r2    @ 080d4526 1140
    orrs r1,r0    @ 080d4528 0143
    strh r1,[r5,#0x0]                        @ 080d452a 2980
    b LAB_080d4542                           @ 080d452c 09e0
    .zero  0x2
DWORD_080d4530:
    .word  0x00002f52                     @ 080d4530 522f0000
DWORD_080d4534:
    .word  0xffffe01f                     @ 080d4534 1fe0ffff
LAB_080d4538:
    ldr r0, DWORD_080d4560                   @ 080d4538 0948
    ands r0,r2    @ 080d453a 1040
    movs r1,#0xe0    @ 080d453c e021
    orrs r0,r1    @ 080d453e 0843
    strh r0,[r5,#0x0]                        @ 080d4540 2880
LAB_080d4542:
    ldr r2, DWORD_080d4564                   @ 080d4542 084a
    adds r1,r3,r2    @ 080d4544 9918
    movs r0,#0x1    @ 080d4546 0120
    strb r0,[r1,#0x0]                        @ 080d4548 0870
    ldr r0, DWORD_080d4568                   @ 080d454a 0748
    adds r1,r3,r0    @ 080d454c 1918
LAB_080d454e:
    movs r0,#0x2    @ 080d454e 0220
    ldrb r2,[r1,#0x0]                        @ 080d4550 0a78
    orrs r0,r2    @ 080d4552 1043
    strb r0,[r1,#0x0]                        @ 080d4554 0870
    movs r0,#0x0    @ 080d4556 0020
    bl sync_state_and_init_sprite            @ 080d4558 25f0acfa
    b LAB_080d45ee                           @ 080d455c 47e0
    .zero  0x2
DWORD_080d4560:
    .word  0xffffe01f                     @ 080d4560 1fe0ffff
DWORD_080d4564:
    .word  0x00002f4d                     @ 080d4564 4d2f0000
DWORD_080d4568:
    .word  0x00002f51                     @ 080d4568 512f0000
LAB_080d456c:
    movs r0,#0x10    @ 080d456c 1020
    ands r0,r1    @ 080d456e 0840
    cmp r0,#0x0                              @ 080d4570 0028
    beq LAB_080d45b4                         @ 080d4572 1fd0
    ldr r0, DWORD_080d45a8                   @ 080d4574 0c48
    adds r5,r6,r0    @ 080d4576 3518
    ldrh r2,[r5,#0x0]                        @ 080d4578 2a88
    lsls r0,r2,#0x13    @ 080d457a d004
    lsrs r0,r0,#0x18    @ 080d457c 000e
    adds r0,#0x1    @ 080d457e 0130
    movs r4,#0xff    @ 080d4580 ff24
    ands r0,r4    @ 080d4582 2040
    lsls r0,r0,#0x5    @ 080d4584 4001
    ldr r3, DWORD_080d45ac                   @ 080d4586 094b
    adds r1,r3,#0x0    @ 080d4588 191c
    ands r1,r2    @ 080d458a 1140
    orrs r1,r0    @ 080d458c 0143
    lsrs r0,r0,#0x5    @ 080d458e 4009
    movs r2,#0x7    @ 080d4590 0722
    ands r0,r2    @ 080d4592 1040
    ands r0,r4    @ 080d4594 2040
    lsls r0,r0,#0x5    @ 080d4596 4001
    ands r1,r3    @ 080d4598 1940
    orrs r1,r0    @ 080d459a 0143
    strh r1,[r5,#0x0]                        @ 080d459c 2980
    movs r0,#0x1    @ 080d459e 0120
    strb r0,[r7,#0x0]                        @ 080d45a0 3870
    ldr r2, DWORD_080d45b0                   @ 080d45a2 034a
    adds r1,r6,r2    @ 080d45a4 b118
    b LAB_080d454e                           @ 080d45a6 d2e7
DWORD_080d45a8:
    .word  0x00002f52                     @ 080d45a8 522f0000
DWORD_080d45ac:
    .word  0xffffe01f                     @ 080d45ac 1fe0ffff
DWORD_080d45b0:
    .word  0x00002f51                     @ 080d45b0 512f0000
LAB_080d45b4:
    movs r0,#0x2    @ 080d45b4 0220
    ands r0,r1    @ 080d45b6 0840
    cmp r0,#0x0                              @ 080d45b8 0028
    beq LAB_080d45ee                         @ 080d45ba 18d0
LAB_080d45bc:
    ldr r0, DWORD_080d45cc                   @ 080d45bc 0348
    adds r1,r6,r0    @ 080d45be 3118
    ldr r0, DWORD_080d45d0                   @ 080d45c0 0348
    ldrh r2,[r1,#0x0]                        @ 080d45c2 0a88
    ands r0,r2    @ 080d45c4 1040
    strh r0,[r1,#0x0]                        @ 080d45c6 0880
    b LAB_080d45ee                           @ 080d45c8 11e0
    .zero  0x2
DWORD_080d45cc:
    .word  0x00002f54                     @ 080d45cc 542f0000
DWORD_080d45d0:
    .word  0xffffe01f                     @ 080d45d0 1fe0ffff
LAB_080d45d4:
    movs r0,#0x2    @ 080d45d4 0220
    b LAB_080d45ec                           @ 080d45d6 09e0
LAB_080d45d8:
    bl setup_zone_slot_sorted_view           @ 080d45d8 fff746fe
    ldr r1, DWORD_080d45f8                   @ 080d45dc 0649
    adds r0,r6,r1    @ 080d45de 7018
    movs r1,#0x3    @ 080d45e0 0321
    rsbs r1,r1,#0    @ 080d45e2 4942
    ldrb r2,[r0,#0x0]                        @ 080d45e4 0278
    ands r1,r2    @ 080d45e6 1140
    strb r1,[r0,#0x0]                        @ 080d45e8 0170
    movs r0,#0x0    @ 080d45ea 0020
LAB_080d45ec:
    strb r0,[r7,#0x0]                        @ 080d45ec 3870
LAB_080d45ee:
    movs r0,#0x1    @ 080d45ee 0120
    pop {r4,r5,r6,r7}                        @ 080d45f0 f0bc
    pop {r1}                                 @ 080d45f2 02bc
    bx r1                                    @ 080d45f4 0847
    .zero  0x2
DWORD_080d45f8:
    .word  0x00002f51                     @ 080d45f8 512f0000

@ pack card shop: loads up to 3 card tile images to VRAM. r0 points to 3-card-ID array (4 bytes each), r1 holds flags for internal offset. For each card_id (if <= 0x3ff): uses id*0x20 as index into ROM card tile table (0x09ce822c+) to find tile row pointer, writes via tile_2d_row_copy to OBJ VRAM 0x06010000 (slots 0/1/2). Finally DMA-copies corresponding palette (0x09ce824c table) to 0x05000200 (32 bytes). Initializes pack_ui_state scroll substruct: [+0x6b0] := r1 flags; [+0x6b2/+0x6b4] := 0; [+0xe/+0x1e] := default values.
@ 
@ Constants:
@ - OBJ_VRAM_CARD_BASE = 0x06010000 (pack card slot OBJ tile target)
@ - ROM_CARD_TILE_TABLE = 0x09ce822c (card tile ROM index table)
@ - ROM_CARD_PAL_TABLE = 0x09ce824c (card palette ROM index table)
@ - PAL_DST = 0x05000200 (palette target slot)
@ - CARD_ID_VALID_MAX = 0x3ff (valid card_id range [0..0x3ff])
@ - TILE_ENTRY_STRIDE = 0x20 (card_id to ROM table entry byte stride)
@ - pack_ui_state = 0x03005850 (IWRAM state base)
@ - SCROLL_STRUCT_OFFSET = 0x6b0 (= 0xd6 << 3, scroll substruct offset)
load_pack_card_tiles_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080d45fc f0b5
    .hword 0x4647    @ 080d45fe 4746
    push {r7}                                @ 080d4600 80b4
    adds r5,r0,#0x0    @ 080d4602 051c
    .hword 0x4688    @ 080d4604 8846
    ldr r0, DAT_080d4690                     @ 080d4606 2248
    movs r1,#0xd6    @ 080d4608 d621
    lsls r1,r1,#0x3    @ 080d460a c900
    adds r4,r0,r1    @ 080d460c 4418
    movs r7,#0x0    @ 080d460e 0027
    strh r7,[r4,#0x2]                        @ 080d4610 6780
    strh r7,[r4,#0x4]                        @ 080d4612 a780
    .hword 0x4640    @ 080d4614 4046
    strh r0,[r4,#0x1e]                       @ 080d4616 e083
    movs r0,#0x80    @ 080d4618 8020
    lsls r0,r0,#0x1    @ 080d461a 4000
    strh r0,[r4,#0xe]                        @ 080d461c e081
    ldr r0,[r5,#0x0]                         @ 080d461e 2868
    ldr r6, DAT_080d4694                     @ 080d4620 1c4e
    cmp r0,r6                                @ 080d4622 b042
    bhi LAB_080d463a                         @ 080d4624 09d8
    strh r0,[r4,#0x18]                       @ 080d4626 2083
    lsls r0,r0,#0x5    @ 080d4628 4001
    ldr r1, DAT_080d4698                     @ 080d462a 1b49
    adds r0,r0,r1    @ 080d462c 4018
    ldr r1, DAT_080d469c                     @ 080d462e 1b49
    ldr r1,[r1,#0x0]                         @ 080d4630 0968
    movs r2,#0x4    @ 080d4632 0422
    movs r3,#0x8    @ 080d4634 0823
    bl tile_2d_row_copy                      @ 080d4636 22f04dff
LAB_080d463a:
    ldr r0,[r5,#0x4]                         @ 080d463a 6868
    cmp r0,r6                                @ 080d463c b042
    bhi LAB_080d4654                         @ 080d463e 09d8
    strh r0,[r4,#0x1a]                       @ 080d4640 6083
    lsls r0,r0,#0x5    @ 080d4642 4001
    ldr r1, DAT_080d4698                     @ 080d4644 1449
    adds r0,r0,r1    @ 080d4646 4018
    ldr r1, DAT_080d469c                     @ 080d4648 1449
    ldr r1,[r1,#0x4]                         @ 080d464a 4968
    movs r2,#0xa    @ 080d464c 0a22
    movs r3,#0x2    @ 080d464e 0223
    bl tile_2d_row_copy                      @ 080d4650 22f040ff
LAB_080d4654:
    ldr r0,[r5,#0x8]                         @ 080d4654 a868
    cmp r0,r6                                @ 080d4656 b042
    bhi LAB_080d466e                         @ 080d4658 09d8
    strh r0,[r4,#0x1c]                       @ 080d465a a083
    lsls r0,r0,#0x5    @ 080d465c 4001
    ldr r1, DAT_080d4698                     @ 080d465e 0e49
    adds r0,r0,r1    @ 080d4660 4018
    ldr r1, DAT_080d469c                     @ 080d4662 0e49
    ldr r1,[r1,#0x18]                        @ 080d4664 8969
    movs r2,#0x4    @ 080d4666 0422
    movs r3,#0x6    @ 080d4668 0623
    bl tile_2d_row_copy                      @ 080d466a 22f033ff
LAB_080d466e:
    .hword 0x4641    @ 080d466e 4146
    lsls r0,r1,#0x5    @ 080d4670 4801
    ldr r1, DAT_080d46a0                     @ 080d4672 0b49
    adds r0,r0,r1    @ 080d4674 4018
    ldr r1, DAT_080d46a4                     @ 080d4676 0b49
    ldr r1,[r1,#0x0]                         @ 080d4678 0968
    movs r2,#0x20    @ 080d467a 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d467c 20f044fc
    strh r7,[r4,#0x14]                       @ 080d4680 a782
    movs r0,#0x28    @ 080d4682 2820
    strh r0,[r4,#0x16]                       @ 080d4684 e082
    pop {r3}                                 @ 080d4686 08bc
    .hword 0x4698    @ 080d4688 9846
    pop {r4,r5,r6,r7}                        @ 080d468a f0bc
    pop {r0}                                 @ 080d468c 01bc
    bx r0                                    @ 080d468e 0047
DAT_080d4690:
    .word  pack_ui_state                  @ 080d4690 50580003
DAT_080d4694:
    .word  0x000003ff                     @ 080d4694 ff030000
DAT_080d4698:
    .word  0x06010000                     @ 080d4698 00000106
DAT_080d469c:
    .word  0x09ce822c                     @ 080d469c 2c82ce09
DAT_080d46a0:
    .word  0x05000200                     @ 080d46a0 00020005
DAT_080d46a4:
    .word  0x09ce824c                     @ 080d46a4 4c82ce09

@ 拆包场景卡牌精灵的翻转/缩放 OAM 渲染入口, 由各拆包状态 tick 处理器高频调用 (indeg=34). 读取 pack_ui_state+0x6b0 工作结构的状态字 [+0]: 状态 1 与状态 2 分别取不同的卡牌尺寸 (减偏移 0x28/0x8 或 0x10/0x20) 与不同的 OBJ 属性, 默认态走第三套参数; 在栈上构造 OAM 仿射缩放矩阵 (基准 0x4080 = 8.8 定点 1.0), 调用 write_oam_entry_from_packed_args 与 write_pack_obj_attr_by_dir_split 写出精灵, 并用 bios_div 做尺寸插值后调 scale_pixel_brightness_in_buffer 调整亮度. r0 选择渲染模式/精灵组.
render_pack_card_sprite_by_flip_state:
    push {r4,r5,r6,r7,lr}                    @ 080d46a8 f0b5
    .hword 0x4657    @ 080d46aa 5746
    .hword 0x464e    @ 080d46ac 4e46
    .hword 0x4645    @ 080d46ae 4546
    push {r5,r6,r7}                          @ 080d46b0 e0b4
    sub sp,#0x1c                             @ 080d46b2 87b0
    str r0,[sp,#0x18]                        @ 080d46b4 0690
    ldr r0, DAT_080d46f8                     @ 080d46b6 1048
    movs r1,#0xd6    @ 080d46b8 d621
    lsls r1,r1,#0x3    @ 080d46ba c900
    adds r7,r0,r1    @ 080d46bc 4718
    ldrh r0,[r7,#0x0]                        @ 080d46be 3888
    cmp r0,#0x1                              @ 080d46c0 0128
    beq LAB_080d4700                         @ 080d46c2 1dd0
    cmp r0,#0x1                              @ 080d46c4 0128
    ble LAB_080d46cc                         @ 080d46c6 01dd
    cmp r0,#0x2                              @ 080d46c8 0228
    beq LAB_080d473e                         @ 080d46ca 38d0
LAB_080d46cc:
    ldrh r0,[r7,#0x2]                        @ 080d46cc 7888
    subs r0,#0x10    @ 080d46ce 1038
    lsls r0,r0,#0x10    @ 080d46d0 0004
    lsrs r0,r0,#0x10    @ 080d46d2 000c
    .hword 0x4682    @ 080d46d4 8246
    ldrh r0,[r7,#0x4]                        @ 080d46d6 b888
    subs r0,#0x20    @ 080d46d8 2038
    lsls r0,r0,#0x10    @ 080d46da 0004
    lsrs r0,r0,#0x10    @ 080d46dc 000c
    .hword 0x4680    @ 080d46de 8046
    movs r2,#0x1    @ 080d46e0 0122
    .hword 0x4691    @ 080d46e2 9146
    add r3,sp,#0x8                           @ 080d46e4 02ab
    movs r0,#0x0    @ 080d46e6 0020
    strh r0,[r3,#0x0]                        @ 080d46e8 1880
    add r2,sp,#0x10                          @ 080d46ea 04aa
    strh r0,[r2,#0x0]                        @ 080d46ec 1080
    .hword 0x4669    @ 080d46ee 6946
    ldr r0, DAT_080d46fc                     @ 080d46f0 0248
    strh r0,[r1,#0x0]                        @ 080d46f2 0880
    b LAB_080d4774                           @ 080d46f4 3ee0
    .zero  0x2
DAT_080d46f8:
    .word  pack_ui_state                  @ 080d46f8 50580003
DAT_080d46fc:
    .word  0x000080c0                     @ 080d46fc c0800000
LAB_080d4700:
    ldrh r0,[r7,#0x2]                        @ 080d4700 7888
    subs r0,#0x28    @ 080d4702 2838
    lsls r0,r0,#0x10    @ 080d4704 0004
    lsrs r0,r0,#0x10    @ 080d4706 000c
    .hword 0x4682    @ 080d4708 8246
    ldrh r0,[r7,#0x4]                        @ 080d470a b888
    subs r0,#0x8    @ 080d470c 0838
    lsls r0,r0,#0x10    @ 080d470e 0004
    lsrs r0,r0,#0x10    @ 080d4710 000c
    .hword 0x4680    @ 080d4712 8046
    movs r3,#0x3    @ 080d4714 0323
    .hword 0x4699    @ 080d4716 9946
    add r4,sp,#0x8                           @ 080d4718 02ac
    movs r2,#0x0    @ 080d471a 0022
    strh r2,[r4,#0x0]                        @ 080d471c 2280
    add r3,sp,#0x10                          @ 080d471e 04ab
    strh r2,[r3,#0x0]                        @ 080d4720 1a80
    .hword 0x4668    @ 080d4722 6846
    movs r1,#0x81    @ 080d4724 8121
    lsls r1,r1,#0x7    @ 080d4726 c901
    strh r1,[r0,#0x0]                        @ 080d4728 0180
    movs r0,#0x20    @ 080d472a 2020
    strh r0,[r4,#0x2]                        @ 080d472c 6080
    strh r2,[r3,#0x2]                        @ 080d472e 5a80
    .hword 0x4668    @ 080d4730 6846
    strh r1,[r0,#0x2]                        @ 080d4732 4180
    movs r1,#0x40    @ 080d4734 4021
    strh r1,[r4,#0x4]                        @ 080d4736 a180
    strh r2,[r3,#0x4]                        @ 080d4738 9a80
    strh r1,[r0,#0x4]                        @ 080d473a 8180
    b LAB_080d4774                           @ 080d473c 1ae0
LAB_080d473e:
    ldrh r0,[r7,#0x2]                        @ 080d473e 7888
    subs r0,#0x10    @ 080d4740 1038
    lsls r0,r0,#0x10    @ 080d4742 0004
    lsrs r0,r0,#0x10    @ 080d4744 000c
    .hword 0x4682    @ 080d4746 8246
    ldrh r0,[r7,#0x4]                        @ 080d4748 b888
    subs r0,#0x18    @ 080d474a 1838
    lsls r0,r0,#0x10    @ 080d474c 0004
    lsrs r0,r0,#0x10    @ 080d474e 000c
    .hword 0x4680    @ 080d4750 8046
    movs r4,#0x2    @ 080d4752 0224
    .hword 0x46a1    @ 080d4754 a146
    add r4,sp,#0x8                           @ 080d4756 02ac
    movs r1,#0x0    @ 080d4758 0021
    strh r1,[r4,#0x0]                        @ 080d475a 2180
    add r3,sp,#0x10                          @ 080d475c 04ab
    strh r1,[r3,#0x0]                        @ 080d475e 1980
    .hword 0x466a    @ 080d4760 6a46
    movs r0,#0x80    @ 080d4762 8020
    strh r0,[r2,#0x0]                        @ 080d4764 1080
    strh r1,[r4,#0x2]                        @ 080d4766 6180
    movs r0,#0x20    @ 080d4768 2020
    strh r0,[r3,#0x2]                        @ 080d476a 5880
    .hword 0x4669    @ 080d476c 6946
    movs r0,#0x81    @ 080d476e 8120
    lsls r0,r0,#0x7    @ 080d4770 c001
    strh r0,[r1,#0x2]                        @ 080d4772 4880
LAB_080d4774:
    movs r0,#0x80    @ 080d4774 8020
    lsls r0,r0,#0x1    @ 080d4776 4000
    ldrh r5,[r7,#0xe]                        @ 080d4778 fd89
    cmp r5,r0                                @ 080d477a 8542
    bne LAB_080d47e6                         @ 080d477c 33d1
    movs r6,#0x0    @ 080d477e 0026
    cmp r6,r9                                @ 080d4780 4e45
    bcs LAB_080d4850                         @ 080d4782 65d2
LAB_080d4784:
    lsls r2,r6,#0x1    @ 080d4784 7200
    .hword 0x466b    @ 080d4786 6b46
    adds r3,r3,r2    @ 080d4788 9b18
    adds r3,#0x8    @ 080d478a 0833
    movs r0,#0x0    @ 080d478c 0020
    ldrsh r1,[r3,r0]                         @ 080d478e 195e
    .hword 0x466c    @ 080d4790 6c46
    adds r4,r4,r2    @ 080d4792 a418
    adds r4,#0x10    @ 080d4794 1034
    movs r5,#0x0    @ 080d4796 0025
    ldrsh r0,[r4,r5]                         @ 080d4798 605f
    lsls r0,r0,#0x5    @ 080d479a 4001
    adds r1,r1,r0    @ 080d479c 0918
    lsls r1,r1,#0xd    @ 080d479e 4903
    lsrs r5,r1,#0x10    @ 080d47a0 0d0c
    ldrh r0,[r3,#0x0]                        @ 080d47a2 1888
    add r0,r10                               @ 080d47a4 5044
    lsls r0,r0,#0x10    @ 080d47a6 0004
    lsrs r0,r0,#0x10    @ 080d47a8 000c
    ldrh r1,[r4,#0x0]                        @ 080d47aa 2188
    add r1,r8                                @ 080d47ac 4144
    lsls r1,r1,#0x10    @ 080d47ae 0904
    orrs r0,r1    @ 080d47b0 0843
    .hword 0x466b    @ 080d47b2 6b46
    adds r1,r3,r2    @ 080d47b4 9918
    ldrh r1,[r1,#0x0]                        @ 080d47b6 0988
    ldrh r4,[r7,#0x1e]                       @ 080d47b8 fc8b
    lsls r2,r4,#0xc    @ 080d47ba 2203
    ldr r4,[sp,#0x18]                        @ 080d47bc 069c
    lsls r3,r4,#0xa    @ 080d47be a302
    orrs r2,r3    @ 080d47c0 1a43
    ldrh r3,[r7,#0x0]                        @ 080d47c2 3b88
    lsls r4,r3,#0x1    @ 080d47c4 5c00
    adds r3,r7,#0x0    @ 080d47c6 3b1c
    adds r3,#0x18    @ 080d47c8 1833
    adds r3,r3,r4    @ 080d47ca 1b19
    ldrh r3,[r3,#0x0]                        @ 080d47cc 1b88
    adds r3,r3,r5    @ 080d47ce 5b19
    orrs r2,r3    @ 080d47d0 1a43
    lsls r2,r2,#0x10    @ 080d47d2 1204
    lsrs r2,r2,#0x10    @ 080d47d4 120c
    bl write_oam_entry_from_packed_args      @ 080d47d6 21f0c9fc
    adds r0,r6,#0x1    @ 080d47da 701c
    lsls r0,r0,#0x10    @ 080d47dc 0004
    lsrs r6,r0,#0x10    @ 080d47de 060c
    cmp r6,r9                                @ 080d47e0 4e45
    bcc LAB_080d4784                         @ 080d47e2 cfd3
    b LAB_080d4850                           @ 080d47e4 34e0
LAB_080d47e6:
    movs r6,#0x0    @ 080d47e6 0026
    cmp r6,r9                                @ 080d47e8 4e45
    bcs LAB_080d4850                         @ 080d47ea 31d2
LAB_080d47ec:
    lsls r2,r6,#0x1    @ 080d47ec 7200
    .hword 0x466b    @ 080d47ee 6b46
    adds r3,r3,r2    @ 080d47f0 9b18
    adds r3,#0x8    @ 080d47f2 0833
    movs r4,#0x0    @ 080d47f4 0024
    ldrsh r1,[r3,r4]                         @ 080d47f6 195f
    .hword 0x466c    @ 080d47f8 6c46
    adds r4,r4,r2    @ 080d47fa a418
    adds r4,#0x10    @ 080d47fc 1034
    movs r5,#0x0    @ 080d47fe 0025
    ldrsh r0,[r4,r5]                         @ 080d4800 605f
    lsls r0,r0,#0x5    @ 080d4802 4001
    adds r1,r1,r0    @ 080d4804 0918
    lsls r1,r1,#0xd    @ 080d4806 4903
    lsrs r5,r1,#0x10    @ 080d4808 0d0c
    ldrh r0,[r3,#0x0]                        @ 080d480a 1888
    add r0,r10                               @ 080d480c 5044
    lsls r0,r0,#0x10    @ 080d480e 0004
    lsrs r0,r0,#0x10    @ 080d4810 000c
    ldrh r1,[r4,#0x0]                        @ 080d4812 2188
    add r1,r8                                @ 080d4814 4144
    lsls r1,r1,#0x10    @ 080d4816 0904
    orrs r0,r1    @ 080d4818 0843
    .hword 0x466b    @ 080d481a 6b46
    adds r1,r3,r2    @ 080d481c 9918
    ldrh r1,[r1,#0x0]                        @ 080d481e 0988
    ldrh r4,[r7,#0x1e]                       @ 080d4820 fc8b
    lsls r2,r4,#0xc    @ 080d4822 2203
    ldr r4,[sp,#0x18]                        @ 080d4824 069c
    lsls r3,r4,#0xa    @ 080d4826 a302
    orrs r2,r3    @ 080d4828 1a43
    ldrh r3,[r7,#0x0]                        @ 080d482a 3b88
    lsls r4,r3,#0x1    @ 080d482c 5c00
    adds r3,r7,#0x0    @ 080d482e 3b1c
    adds r3,#0x18    @ 080d4830 1833
    adds r3,r3,r4    @ 080d4832 1b19
    ldrh r3,[r3,#0x0]                        @ 080d4834 1b88
    adds r3,r3,r5    @ 080d4836 5b19
    orrs r2,r3    @ 080d4838 1a43
    lsls r2,r2,#0x10    @ 080d483a 1204
    lsrs r2,r2,#0x10    @ 080d483c 120c
    ldrh r4,[r7,#0xe]                        @ 080d483e fc89
    lsls r3,r4,#0x10    @ 080d4840 2304
    bl write_pack_obj_attr_by_dir_split      @ 080d4842 22f053f8
    adds r0,r6,#0x1    @ 080d4846 701c
    lsls r0,r0,#0x10    @ 080d4848 0004
    lsrs r6,r0,#0x10    @ 080d484a 060c
    cmp r6,r9                                @ 080d484c 4e45
    bcc LAB_080d47ec                         @ 080d484e cdd3
LAB_080d4850:
    ldrh r2,[r7,#0x14]                       @ 080d4850 ba8a
    adds r2,#0x1    @ 080d4852 0132
    strh r2,[r7,#0x14]                       @ 080d4854 ba82
    lsls r1,r2,#0x10    @ 080d4856 1104
    ldrh r4,[r7,#0x16]                       @ 080d4858 fc8a
    lsls r0,r4,#0x10    @ 080d485a 2004
    adds r5,r4,#0x0    @ 080d485c 251c
    cmp r1,r0                                @ 080d485e 8142
    blt LAB_080d4872                         @ 080d4860 07db
    adds r3,r2,#0x0    @ 080d4862 131c
LAB_080d4864:
    subs r2,r3,r4    @ 080d4864 1a1b
    adds r3,r2,#0x0    @ 080d4866 131c
    lsls r1,r2,#0x10    @ 080d4868 1104
    lsls r0,r4,#0x10    @ 080d486a 2004
    cmp r1,r0                                @ 080d486c 8142
    bge LAB_080d4864                         @ 080d486e f9da
    strh r2,[r7,#0x14]                       @ 080d4870 ba82
LAB_080d4872:
    lsls r0,r5,#0x10    @ 080d4872 2804
    movs r5,#0x14    @ 080d4874 1425
    ldrsh r1,[r7,r5]                         @ 080d4876 795f
    asrs r2,r0,#0x11    @ 080d4878 4214
    cmp r1,r2                                @ 080d487a 9142
    bge LAB_080d4882                         @ 080d487c 01da
    adds r0,r1,#0x0    @ 080d487e 081c
    b LAB_080d488c                           @ 080d4880 04e0
LAB_080d4882:
    movs r3,#0x16    @ 080d4882 1623
    ldrsh r0,[r7,r3]                         @ 080d4884 f85e
    movs r4,#0x14    @ 080d4886 1424
    ldrsh r1,[r7,r4]                         @ 080d4888 395f
    subs r0,r0,r1    @ 080d488a 401a
LAB_080d488c:
    lsls r0,r0,#0x8    @ 080d488c 0002
    adds r1,r2,#0x0    @ 080d488e 111c
    bl bios_div                              @ 080d4890 39f0b4fd
    lsls r0,r0,#0x10    @ 080d4894 0004
    lsrs r6,r0,#0x10    @ 080d4896 060c
    ldr r0, DAT_080d48c0                     @ 080d4898 0948
    ldr r0,[r0,#0x0]                         @ 080d489a 0068
    adds r0,#0x1c    @ 080d489c 1c30
    ldrh r7,[r7,#0x1e]                       @ 080d489e ff8b
    lsls r1,r7,#0x5    @ 080d48a0 7901
    ldr r5, DAT_080d48c4                     @ 080d48a2 084d
    adds r1,r1,r5    @ 080d48a4 4919
    lsls r2,r6,#0x10    @ 080d48a6 3204
    movs r3,#0x2    @ 080d48a8 0223
    orrs r2,r3    @ 080d48aa 1a43
    bl scale_pixel_brightness_in_buffer      @ 080d48ac 09f014f9
    add sp,#0x1c                             @ 080d48b0 07b0
    pop {r3,r4,r5}                           @ 080d48b2 38bc
    .hword 0x4698    @ 080d48b4 9846
    .hword 0x46a1    @ 080d48b6 a146
    .hword 0x46aa    @ 080d48b8 aa46
    pop {r4,r5,r6,r7}                        @ 080d48ba f0bc
    pop {r0}                                 @ 080d48bc 01bc
    bx r0                                    @ 080d48be 0047
DAT_080d48c0:
    .word  0x09ce824c                     @ 080d48c0 4c82ce09
DAT_080d48c4:
    .word  0x0500021c                     @ 080d48c4 1c020005

@ pack_ui_state scroll animation per-frame linear interpolation step. Reads remaining frame counter [pack_ui_state+0x6b0+0x10]: if already 0, returns r0=1 (done). Otherwise decrements [+0x10], interpolates x and y axes: (target - start) * remaining / total + start, writes result to current position fields [+0x2]/[+0x4]. When counter reaches 0, clears [+0x10] and [+0x12], sets r0=1 (animation complete); otherwise r0=0 (still in progress).
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - SCROLL_OFFSET = 0x6b0 (= 0xd6 << 3)
@ - +0x2/+0x4: current x/y position (s16)
@ - +0x6/+0x8: target x/y (s16)
@ - +0xa/+0xc: start x/y (s16)
@ - +0x10: remaining frame counter (s16)
@ - +0x12: total frames denominator (s16)
tick_pack_scroll_interp_step:
    push {r4,r5,lr}                          @ 080d48c8 30b5
    ldr r0, DAT_080d48e4                     @ 080d48ca 0648
    movs r1,#0xd6    @ 080d48cc d621
    lsls r1,r1,#0x3    @ 080d48ce c900
    adds r4,r0,r1    @ 080d48d0 4418
    movs r5,#0x0    @ 080d48d2 0025
    ldrh r1,[r4,#0x10]                       @ 080d48d4 218a
    movs r2,#0x10    @ 080d48d6 1022
    ldrsh r0,[r4,r2]                         @ 080d48d8 a05e
    cmp r0,#0x0                              @ 080d48da 0028
    bne LAB_080d48e8                         @ 080d48dc 04d1
    movs r0,#0x1    @ 080d48de 0120
    b LAB_080d4938                           @ 080d48e0 2ae0
    .zero  0x2
DAT_080d48e4:
    .word  pack_ui_state                  @ 080d48e4 50580003
LAB_080d48e8:
    subs r0,r1,#0x1    @ 080d48e8 481e
    strh r0,[r4,#0x10]                       @ 080d48ea 2082
    movs r1,#0x6    @ 080d48ec 0621
    ldrsh r0,[r4,r1]                         @ 080d48ee 605e
    movs r2,#0xa    @ 080d48f0 0a22
    ldrsh r1,[r4,r2]                         @ 080d48f2 a15e
    subs r0,r0,r1    @ 080d48f4 401a
    movs r2,#0x10    @ 080d48f6 1022
    ldrsh r1,[r4,r2]                         @ 080d48f8 a15e
    muls r0,r1    @ 080d48fa 4843
    movs r2,#0x12    @ 080d48fc 1222
    ldrsh r1,[r4,r2]                         @ 080d48fe a15e
    bl bios_div                              @ 080d4900 39f07cfd
    ldrh r1,[r4,#0xa]                        @ 080d4904 6189
    adds r0,r1,r0    @ 080d4906 0818
    strh r0,[r4,#0x2]                        @ 080d4908 6080
    movs r2,#0x8    @ 080d490a 0822
    ldrsh r0,[r4,r2]                         @ 080d490c a05e
    movs r2,#0xc    @ 080d490e 0c22
    ldrsh r1,[r4,r2]                         @ 080d4910 a15e
    subs r0,r0,r1    @ 080d4912 401a
    movs r2,#0x10    @ 080d4914 1022
    ldrsh r1,[r4,r2]                         @ 080d4916 a15e
    muls r0,r1    @ 080d4918 4843
    movs r2,#0x12    @ 080d491a 1222
    ldrsh r1,[r4,r2]                         @ 080d491c a15e
    bl bios_div                              @ 080d491e 39f06dfd
    ldrh r1,[r4,#0xc]                        @ 080d4922 a189
    adds r0,r1,r0    @ 080d4924 0818
    strh r0,[r4,#0x4]                        @ 080d4926 a080
    movs r2,#0x10    @ 080d4928 1022
    ldrsh r0,[r4,r2]                         @ 080d492a a05e
    cmp r0,#0x0                              @ 080d492c 0028
    bgt LAB_080d4936                         @ 080d492e 02dc
    strh r5,[r4,#0x10]                       @ 080d4930 2582
    strh r5,[r4,#0x12]                       @ 080d4932 6582
    movs r5,#0x1    @ 080d4934 0125
LAB_080d4936:
    adds r0,r5,#0x0    @ 080d4936 281c
LAB_080d4938:
    pop {r4,r5}                              @ 080d4938 30bc
    pop {r1}                                 @ 080d493a 02bc
    bx r1                                    @ 080d493c 0847
    .zero  0x2

@ Sets pack_ui_state scroll substruct start position fields. Writes r0 to [pack_ui_state+0x6b2] (scroll start x), r1 to [pack_ui_state+0x6b4] (scroll start y). Called by pack card shop before starting a new scroll animation to record the animation start coordinates.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - SCROLL_START_X_OFFSET = 0x6b2 (start x field)
@ - SCROLL_START_Y_OFFSET = 0x6b4 (start y field)
set_pack_scroll_start_pos:
    push {r4,lr}                             @ 080d4940 10b5
    ldr r2, DAT_080d4958                     @ 080d4942 054a
    ldr r4, DAT_080d495c                     @ 080d4944 054c
    adds r3,r2,r4    @ 080d4946 1319
    strh r0,[r3,#0x0]                        @ 080d4948 1880
    ldr r0, DAT_080d4960                     @ 080d494a 0548
    adds r2,r2,r0    @ 080d494c 1218
    strh r1,[r2,#0x0]                        @ 080d494e 1180
    pop {r4}                                 @ 080d4950 10bc
    pop {r0}                                 @ 080d4952 01bc
    bx r0                                    @ 080d4954 0047
    .zero  0x2
DAT_080d4958:
    .word  pack_ui_state                  @ 080d4958 50580003
DAT_080d495c:
    .word  0x000006b2                     @ 080d495c b2060000
DAT_080d4960:
    .word  0x000006b4                     @ 080d4960 b4060000
    ROM_INCBIN 0xd4964, 0x14

@ Leaf setter: writes r0 to pack_ui_state scroll substruct first halfword field [+0x6b0], controlling the scroll step mode. Called by pack scene when switching scroll animation mode (e.g. switching to constant/easing mode).
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - SCROLL_MODE_OFFSET = 0x6b0 (= 0xd6 << 3, scroll substruct first field)
set_pack_scroll_step_mode:
    ldr r1, DAT_080d4984                     @ 080d4978 0249
    movs r2,#0xd6    @ 080d497a d622
    lsls r2,r2,#0x3    @ 080d497c d200
    adds r1,r1,r2    @ 080d497e 8918
    strh r0,[r1,#0x0]                        @ 080d4980 0880
    bx lr                                    @ 080d4982 7047
DAT_080d4984:
    .word  pack_ui_state                  @ 080d4984 50580003

@ Initializes pack_ui_state scroll animation parameters. Saves current position ([+0x6b2]/[+0x6b4]) as previous frame start ([+0x6b6]/[+0x6b8]); writes r0/r1 as new target position ([+0x6ba]/[+0x6bc]); writes r2 as total frames to [+0x6c2] and copy [+0x6c0]. Called by pack scene when triggering a new card scroll animation; each call starts a linear interpolation sequence from current to target position, executed per-frame by tick_pack_scroll_interp_step.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - +0x6b2: current x (source for prev save)
@ - +0x6b4: current y (source for prev save)
@ - +0x6b6: prev x
@ - +0x6b8: prev y
@ - +0x6ba: target x (r0 input)
@ - +0x6bc: target y (r1 input)
@ - +0x6c0 (= 0xd8 << 3): total frames copy (r2)
@ - +0x6c2: total frames (r2)
init_pack_scroll_animation:
    push {r4,r5,r6,lr}                       @ 080d4988 70b5
    ldr r3, DAT_080d49c4                     @ 080d498a 0e4b
    ldr r5, DAT_080d49c8                     @ 080d498c 0e4d
    adds r4,r3,r5    @ 080d498e 5c19
    ldrh r5,[r4,#0x0]                        @ 080d4990 2588
    ldr r6, DAT_080d49cc                     @ 080d4992 0e4e
    adds r4,r3,r6    @ 080d4994 9c19
    strh r5,[r4,#0x0]                        @ 080d4996 2580
    ldr r5, DAT_080d49d0                     @ 080d4998 0d4d
    adds r4,r3,r5    @ 080d499a 5c19
    ldrh r5,[r4,#0x0]                        @ 080d499c 2588
    adds r6,#0x2    @ 080d499e 0236
    adds r4,r3,r6    @ 080d49a0 9c19
    strh r5,[r4,#0x0]                        @ 080d49a2 2580
    ldr r5, DAT_080d49d4                     @ 080d49a4 0b4d
    adds r4,r3,r5    @ 080d49a6 5c19
    strh r0,[r4,#0x0]                        @ 080d49a8 2080
    adds r6,#0x4    @ 080d49aa 0436
    adds r0,r3,r6    @ 080d49ac 9819
    strh r1,[r0,#0x0]                        @ 080d49ae 0180
    ldr r1, DAT_080d49d8                     @ 080d49b0 0949
    adds r0,r3,r1    @ 080d49b2 5818
    strh r2,[r0,#0x0]                        @ 080d49b4 0280
    movs r4,#0xd8    @ 080d49b6 d824
    lsls r4,r4,#0x3    @ 080d49b8 e400
    adds r3,r3,r4    @ 080d49ba 1b19
    strh r2,[r3,#0x0]                        @ 080d49bc 1a80
    pop {r4,r5,r6}                           @ 080d49be 70bc
    pop {r0}                                 @ 080d49c0 01bc
    bx r0                                    @ 080d49c2 0047
DAT_080d49c4:
    .word  pack_ui_state                  @ 080d49c4 50580003
DAT_080d49c8:
    .word  0x000006b2                     @ 080d49c8 b2060000
DAT_080d49cc:
    .word  0x000006b6                     @ 080d49cc b6060000
DAT_080d49d0:
    .word  0x000006b4                     @ 080d49d0 b4060000
DAT_080d49d4:
    .word  0x000006ba                     @ 080d49d4 ba060000
DAT_080d49d8:
    .word  0x000006c2                     @ 080d49d8 c2060000

@ pack scene init: sets BG control registers and zero-fills related VRAM regions. Writes BG0CNT=0x1c00 (4bpp, charblock 7), BG1CNT=0x1d86, BG2CNT=0x1e8a. Sets [gPrng+0x174] |= 0x200 (enables feature flag). Calls reset_all_bg_scroll_regs_and_shadows. Clears [pack_ui_state+0xc+0x3e]. Zero-fills 4 VRAM regions via zero_fill_halfword_wrapper: 0x06000000 (0x20 HW), 0x0600e000 (0x800 HW), 0x06004000 (0x40 HW), 0x0600e800 (0x800 HW). Called by pack main scene frame driver on entry.
@ 
@ Constants:
@ - BG0CNT = 0x04000008 (BG0 control register)
@ - BG0CNT_VAL = 0x1c00 (charblock 7, 256x256, 4bpp)
@ - BG1CNT_VAL = 0x1d86
@ - BG2CNT_VAL = 0x1e8a
@ - gPrng_FLAG_OFFSET = 0x174 (= 0xba << 1; gPrng+0x174 feature flag)
@ - FLAG_BIT = 0x200 (= 0x80 << 2)
@ - VRAM_0 = 0x06000000, VRAM_1 = 0x0600e000, VRAM_2 = 0x06004000, VRAM_3 = 0x0600e800
@ - pack_ui_state = 0x03005850
init_pack_scene_bg_and_vram:
    push {r4,r5,lr}                          @ 080d49dc 30b5
    ldr r5, DAT_080d4a40                     @ 080d49de 184d
    adds r5,#0xc    @ 080d49e0 0c35
    ldr r1, PTR_BG0CNT_080d4a44              @ 080d49e2 1849
    movs r0,#0xe0    @ 080d49e4 e020
    lsls r0,r0,#0x5    @ 080d49e6 4001
    strh r0,[r1,#0x0]                        @ 080d49e8 0880
    adds r1,#0x2    @ 080d49ea 0231
    ldr r0, DAT_080d4a48                     @ 080d49ec 1648
    strh r0,[r1,#0x0]                        @ 080d49ee 0880
    adds r1,#0x2    @ 080d49f0 0231
    adds r0,#0x87    @ 080d49f2 8730
    strh r0,[r1,#0x0]                        @ 080d49f4 0880
    ldr r0, PTR_gPrng_080d4a4c               @ 080d49f6 1548
    movs r1,#0xba    @ 080d49f8 ba21
    lsls r1,r1,#0x1    @ 080d49fa 4900
    adds r0,r0,r1    @ 080d49fc 4018
    movs r2,#0x80    @ 080d49fe 8022
    lsls r2,r2,#0x2    @ 080d4a00 9200
    adds r1,r2,#0x0    @ 080d4a02 111c
    movs r4,#0x0    @ 080d4a04 0024
    ldrh r2,[r0,#0x0]                        @ 080d4a06 0288
    orrs r1,r2    @ 080d4a08 1143
    strh r1,[r0,#0x0]                        @ 080d4a0a 0180
    bl reset_all_bg_scroll_regs_and_shadows  @ 080d4a0c 21f03cf8
    strh r4,[r5,#0x3e]                       @ 080d4a10 ec87
    movs r0,#0xc0    @ 080d4a12 c020
    lsls r0,r0,#0x13    @ 080d4a14 c004
    movs r1,#0x20    @ 080d4a16 2021
    bl zero_fill_halfword_wrapper            @ 080d4a18 20f03efa
    ldr r0, DAT_080d4a50                     @ 080d4a1c 0c48
    movs r4,#0x80    @ 080d4a1e 8024
    lsls r4,r4,#0x4    @ 080d4a20 2401
    adds r1,r4,#0x0    @ 080d4a22 211c
    bl zero_fill_halfword_wrapper            @ 080d4a24 20f038fa
    ldr r0, DAT_080d4a54                     @ 080d4a28 0a48
    movs r1,#0x40    @ 080d4a2a 4021
    bl zero_fill_halfword_wrapper            @ 080d4a2c 20f034fa
    ldr r0, DAT_080d4a58                     @ 080d4a30 0948
    adds r1,r4,#0x0    @ 080d4a32 211c
    bl zero_fill_halfword_wrapper            @ 080d4a34 20f030fa
    pop {r4,r5}                              @ 080d4a38 30bc
    pop {r0}                                 @ 080d4a3a 01bc
    bx r0                                    @ 080d4a3c 0047
    .zero  0x2
DAT_080d4a40:
    .word  pack_ui_state                  @ 080d4a40 50580003
PTR_BG0CNT_080d4a44:
    .word  BG0CNT                         @ 080d4a44 08000004
DAT_080d4a48:
    .word  0x00001d86                     @ 080d4a48 861d0000
PTR_gPrng_080d4a4c:
    .word  gPrng                          @ 080d4a4c 40000003
DAT_080d4a50:
    .word  0x0600e000                     @ 080d4a50 00e00006
DAT_080d4a54:
    .word  0x06004000                     @ 080d4a54 00400006
DAT_080d4a58:
    .word  0x0600e800                     @ 080d4a58 00e80006

@ Pack card image render dispatch hub; routes render tasks based on r1 (banner_data_ptr) and r2 (card_frame_list_ptr) presence. Called during pack UI refresh. (1) r1 != NULL: extracts pack_id low 7 bits from banner_data[+0], calls render_pack_banner_to_slot; r1 == NULL: calls render_pack_banner_to_slot with -1 to clear banner. (2) r2 != NULL: iterates card_frame entries (up to 5), calls render_pack_card_frame_to_slot per entry; r2 == NULL: calls render_pack_card_frame_to_slot(-1) for all 5 slots. (3) reads banner_data[+0] bit7: non-zero -> fill_pack_card_slots_up_to_count(banner[+1] & 0xf); zero -> loops clear_pack_card_slot_tiles [0..4]. Side effects: writes OBJ VRAM banner region and BG tilemap card frame region.
@ 
@ Constants:
@ - MAX_CARD_SLOTS = 5 (cmp r4,#4 -> [0..4])
@ - BANNER_ENABLE_BIT = 0x80 (bit7 of banner_data[+0])
@ - CARD_COUNT_MASK = 0x0f (banner_data[+1] & 0xf)
@ - PACK_ID_BITS = bits[6:0] of banner_data[+0]
dispatch_pack_card_image_render_by_state:
    push {r4,r5,r6,r7,lr}                    @ 080d4a5c f0b5
    adds r5,r0,#0x0    @ 080d4a5e 051c
    adds r6,r1,#0x0    @ 080d4a60 0e1c
    adds r7,r2,#0x0    @ 080d4a62 171c
    cmp r6,#0x0                              @ 080d4a64 002e
    beq LAB_080d4a74                         @ 080d4a66 05d0
    ldr r1,[r6,#0x0]                         @ 080d4a68 3168
    lsls r1,r1,#0x19    @ 080d4a6a 4906
    lsrs r1,r1,#0x19    @ 080d4a6c 490e
    bl render_pack_banner_to_slot            @ 080d4a6e 00f0e1fa
    b LAB_080d4a7e                           @ 080d4a72 04e0
LAB_080d4a74:
    movs r1,#0x1    @ 080d4a74 0121
    rsbs r1,r1,#0    @ 080d4a76 4942
    adds r0,r5,#0x0    @ 080d4a78 281c
    bl render_pack_banner_to_slot            @ 080d4a7a 00f0dbfa
LAB_080d4a7e:
    cmp r7,#0x0                              @ 080d4a7e 002f
    beq LAB_080d4aac                         @ 080d4a80 14d0
    movs r4,#0x0    @ 080d4a82 0024
    b LAB_080d4a96                           @ 080d4a84 07e0
LAB_080d4a86:
    ldmia r7!,{r2}                           @ 080d4a86 04cf
    lsls r2,r2,#0x10    @ 080d4a88 1204
    lsrs r2,r2,#0x14    @ 080d4a8a 120d
    adds r0,r4,#0x0    @ 080d4a8c 201c
    adds r1,r5,#0x0    @ 080d4a8e 291c
    bl render_pack_card_frame_to_slot        @ 080d4a90 00f064f9
    adds r4,#0x1    @ 080d4a94 0134
LAB_080d4a96:
    ldr r0,[r6,#0x0]                         @ 080d4a96 3068
    lsls r1,r0,#0x14    @ 080d4a98 0105
    lsrs r0,r1,#0x1c    @ 080d4a9a 080f
    cmp r0,#0x4                              @ 080d4a9c 0428
    bhi LAB_080d4aa6                         @ 080d4a9e 02d8
    cmp r4,r0                                @ 080d4aa0 8442
    bcc LAB_080d4a86                         @ 080d4aa2 f0d3
    b LAB_080d4ac0                           @ 080d4aa4 0ce0
LAB_080d4aa6:
    cmp r4,#0x4                              @ 080d4aa6 042c
    bls LAB_080d4a86                         @ 080d4aa8 edd9
    b LAB_080d4ac0                           @ 080d4aaa 09e0
LAB_080d4aac:
    movs r4,#0x0    @ 080d4aac 0024
LAB_080d4aae:
    adds r0,r4,#0x0    @ 080d4aae 201c
    adds r1,r5,#0x0    @ 080d4ab0 291c
    movs r2,#0x1    @ 080d4ab2 0122
    rsbs r2,r2,#0    @ 080d4ab4 5242
    bl render_pack_card_frame_to_slot        @ 080d4ab6 00f051f9
    adds r4,#0x1    @ 080d4aba 0134
    cmp r4,#0x4                              @ 080d4abc 042c
    bls LAB_080d4aae                         @ 080d4abe f6d9
LAB_080d4ac0:
    movs r0,#0x80    @ 080d4ac0 8020
    ldrb r1,[r6,#0x0]                        @ 080d4ac2 3178
    ands r0,r1    @ 080d4ac4 0840
    cmp r0,#0x0                              @ 080d4ac6 0028
    beq LAB_080d4ad8                         @ 080d4ac8 06d0
    movs r1,#0xf    @ 080d4aca 0f21
    ldrb r6,[r6,#0x1]                        @ 080d4acc 7678
    ands r1,r6    @ 080d4ace 3140
    adds r0,r5,#0x0    @ 080d4ad0 281c
    bl fill_pack_card_slots_up_to_count      @ 080d4ad2 00f00df8
    b LAB_080d4ae8                           @ 080d4ad6 07e0
LAB_080d4ad8:
    movs r4,#0x0    @ 080d4ad8 0024
LAB_080d4ada:
    adds r0,r4,#0x0    @ 080d4ada 201c
    adds r1,r5,#0x0    @ 080d4adc 291c
    bl clear_pack_card_slot_tiles            @ 080d4ade 00f019fa
    adds r4,#0x1    @ 080d4ae2 0134
    cmp r4,#0x4                              @ 080d4ae4 042c
    bls LAB_080d4ada                         @ 080d4ae6 f8d9
LAB_080d4ae8:
    pop {r4,r5,r6,r7}                        @ 080d4ae8 f0bc
    pop {r0}                                 @ 080d4aea 01bc
    bx r0                                    @ 080d4aec 0047
    .zero  0x2

@ Fills the first fill_count pack card BG tilemap slots with valid tile IDs and clears the rest. r0=pack_context_ptr, r1=fill_count (clamped to 5). Loops [0..fill_count-1]: calls fill_pack_card_slot_tiles(slot, pack_ctx). Then loops [fill_count..4]: calls clear_pack_card_slot_tiles(slot, pack_ctx). Called from FUN_080d4a5c (pack card image hub dispatcher) and multiple pack frame drivers to switch the displayed card count.
@ 
@ Constants:
@ - MAX_SLOT_COUNT = 5 (cmp r1,#5; bls -> clamp)
@ - LAST_SLOT_IDX = 4 (cmp r4,#4 -> clear loop bound)
@ 
@ Inputs: r0=ptr pack_context_ptr; r1=u32 fill_count [0..5]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [VRAM tilemap via fill_pack_card_slot_tiles] writes BG tilemap card slot tile IDs; [VRAM tilemap via clear_pack_card_slot_tiles] clears remaining slots
fill_pack_card_slots_up_to_count:
    push {r4,r5,r6,lr}                       @ 080d4af0 70b5
    adds r6,r0,#0x0    @ 080d4af2 061c
    adds r5,r1,#0x0    @ 080d4af4 0d1c
    cmp r5,#0x5                              @ 080d4af6 052d
    bls LAB_080d4afc                         @ 080d4af8 00d9
    movs r5,#0x5    @ 080d4afa 0525
LAB_080d4afc:
    movs r4,#0x0    @ 080d4afc 0024
    cmp r4,r5                                @ 080d4afe ac42
    bcs LAB_080d4b1c                         @ 080d4b00 0cd2
LAB_080d4b02:
    adds r0,r4,#0x0    @ 080d4b02 201c
    adds r1,r6,#0x0    @ 080d4b04 311c
    bl fill_pack_card_slot_tiles             @ 080d4b06 00f0ddf9
    adds r4,#0x1    @ 080d4b0a 0134
    cmp r4,r5                                @ 080d4b0c ac42
    bcc LAB_080d4b02                         @ 080d4b0e f8d3
    b LAB_080d4b1c                           @ 080d4b10 04e0
LAB_080d4b12:
    adds r0,r4,#0x0    @ 080d4b12 201c
    adds r1,r6,#0x0    @ 080d4b14 311c
    bl clear_pack_card_slot_tiles            @ 080d4b16 00f0fdf9
    adds r4,#0x1    @ 080d4b1a 0134
LAB_080d4b1c:
    cmp r4,#0x4                              @ 080d4b1c 042c
    bls LAB_080d4b12                         @ 080d4b1e f8d9
    pop {r4,r5,r6}                           @ 080d4b20 70bc
    pop {r0}                                 @ 080d4b22 01bc
    bx r0                                    @ 080d4b24 0047
    .zero  0x2

@ 按状态标志渲染拆包场景标签文本组. 读取 r0 指针字节 [r0+0] 的 bit7: 若为 0 则渲染 (类别 2, 子项 1) 与 (类别 1, 子项 0) 两组标签; 若 bit7 置位则先渲染 (类别 1, 子项 5), 再检查 pack_ui_state+0x724 字节的 bit3 决定渲染 (类别 2, 子项 1) 或 (类别 2, 子项 4). 全程经 dispatch_pack_label_text_render_by_category 输出文本精灵. 供拆包 UI 刷新标签时调用.
render_pack_label_text_by_flags:
    push {r4,lr}                             @ 080d4b28 10b5
    ldr r4, DAT_080d4b48                     @ 080d4b2a 074c
    movs r1,#0x80    @ 080d4b2c 8021
    ldrb r0,[r0,#0x0]                        @ 080d4b2e 0078
    ands r1,r0    @ 080d4b30 0140
    cmp r1,#0x0                              @ 080d4b32 0029
    bne LAB_080d4b4c                         @ 080d4b34 0ad1
    movs r0,#0x2    @ 080d4b36 0220
    movs r1,#0x1    @ 080d4b38 0121
    bl dispatch_pack_label_text_render_by_category @ 080d4b3a 00f0effa
    movs r0,#0x1    @ 080d4b3e 0120
    movs r1,#0x0    @ 080d4b40 0021
    bl dispatch_pack_label_text_render_by_category @ 080d4b42 00f0ebfa
    b LAB_080d4b78                           @ 080d4b46 17e0
DAT_080d4b48:
    .word  pack_ui_state                  @ 080d4b48 50580003
LAB_080d4b4c:
    movs r0,#0x1    @ 080d4b4c 0120
    movs r1,#0x5    @ 080d4b4e 0521
    bl dispatch_pack_label_text_render_by_category @ 080d4b50 00f0e4fa
    ldr r0, DAT_080d4b6c                     @ 080d4b54 0548
    adds r1,r4,r0    @ 080d4b56 2118
    movs r0,#0x8    @ 080d4b58 0820
    ldrb r1,[r1,#0x0]                        @ 080d4b5a 0978
    ands r0,r1    @ 080d4b5c 0840
    cmp r0,#0x0                              @ 080d4b5e 0028
    bne LAB_080d4b70                         @ 080d4b60 06d1
    movs r0,#0x2    @ 080d4b62 0220
    movs r1,#0x1    @ 080d4b64 0121
    bl dispatch_pack_label_text_render_by_category @ 080d4b66 00f0d9fa
    b LAB_080d4b78                           @ 080d4b6a 05e0
DAT_080d4b6c:
    .word  0x00000724                     @ 080d4b6c 24070000
LAB_080d4b70:
    movs r0,#0x2    @ 080d4b70 0220
    movs r1,#0x4    @ 080d4b72 0421
    bl dispatch_pack_label_text_render_by_category @ 080d4b74 00f0d2fa
LAB_080d4b78:
    pop {r4}                                 @ 080d4b78 10bc
    pop {r0}                                 @ 080d4b7a 01bc
    bx r0                                    @ 080d4b7c 0047
    .zero  0x2

@ 渲染拆包场景的默认标签文本对. 无条件先调 dispatch_pack_label_text_render_by_category(类别 2, 子项 3), 再调 (类别 1, 子项 2), 写出两组固定标签文本精灵. 无参数无分支, 供拆包 UI 在固定布局状态下刷新标签.
render_pack_label_text_default_pair:
    push {lr}                                @ 080d4b80 00b5
    movs r0,#0x2    @ 080d4b82 0220
    movs r1,#0x3    @ 080d4b84 0321
    bl dispatch_pack_label_text_render_by_category @ 080d4b86 00f0c9fa
    movs r0,#0x1    @ 080d4b8a 0120
    movs r1,#0x2    @ 080d4b8c 0221
    bl dispatch_pack_label_text_render_by_category @ 080d4b8e 00f0c5fa
    pop {r0}                                 @ 080d4b92 01bc
    bx r0                                    @ 080d4b94 0047
    .zero  0x2

@ 拆包场景卡牌图正向滚动动画的逐帧 tick. 读取 pack_ui_state+0xc 工作结构: 比较帧计数 [+0x1a]+2 与上限 [+0xa], 未到上限时按当前卡牌索引 [+0x6fa] 从槽数组 [+0x6fc] 取卡牌记录, 累加色板偏移后调 dispatch_pack_card_image_render_by_state 渲染该帧卡图; 到上限则以 0 参数渲染. 随后用 get_bios_div_remainder 推进动画子帧 [+0x38] (mod 4), 更新滚动位置 [+0x3a]/[+0x3c] (基于 [+0x1a]<<6), 写入状态 [+0]=8, 并将帧计数 [+0x1a] 自增 1 (正向).
tick_pack_card_image_scroll_forward:
    push {r4,r5,r6,lr}                       @ 080d4b98 70b5
    ldr r6, DAT_080d4be0                     @ 080d4b9a 114e
    adds r5,r6,#0x0    @ 080d4b9c 351c
    adds r5,#0xc    @ 080d4b9e 0c35
    ldrh r0,[r5,#0x1a]                       @ 080d4ba0 688b
    adds r0,#0x2    @ 080d4ba2 0230
    ldrh r1,[r5,#0xa]                        @ 080d4ba4 6989
    cmp r0,r1                                @ 080d4ba6 8842
    bcs LAB_080d4bec                         @ 080d4ba8 20d2
    ldr r3, DAT_080d4be4                     @ 080d4baa 0e4b
    adds r2,r6,r3    @ 080d4bac f218
    ldr r1, DAT_080d4be8                     @ 080d4bae 0e49
    adds r0,r6,r1    @ 080d4bb0 7018
    ldrh r0,[r0,#0x0]                        @ 080d4bb2 0088
    lsls r1,r0,#0x2    @ 080d4bb4 8100
    ldr r0,[r2,#0x0]                         @ 080d4bb6 1068
    adds r4,r0,r1    @ 080d4bb8 4418
    adds r3,#0x8    @ 080d4bba 0833
    adds r0,r6,r3    @ 080d4bbc f018
    ldr r2,[r0,#0x0]                         @ 080d4bbe 0268
    movs r1,#0x0    @ 080d4bc0 0021
    adds r6,#0x4c    @ 080d4bc2 4c36
LAB_080d4bc4:
    ldmia r4!,{r0}                           @ 080d4bc4 01cc
    lsls r0,r0,#0x14    @ 080d4bc6 0005
    lsrs r0,r0,#0x1c    @ 080d4bc8 000f
    lsls r0,r0,#0x2    @ 080d4bca 8000
    adds r2,r2,r0    @ 080d4bcc 1218
    adds r1,#0x1    @ 080d4bce 0131
    cmp r1,#0x1                              @ 080d4bd0 0129
    bls LAB_080d4bc4                         @ 080d4bd2 f7d9
    ldrh r0,[r5,#0x38]                       @ 080d4bd4 288f
    adds r1,r4,#0x0    @ 080d4bd6 211c
    bl dispatch_pack_card_image_render_by_state @ 080d4bd8 fff740ff
    b LAB_080d4bf8                           @ 080d4bdc 0ce0
    .zero  0x2
DAT_080d4be0:
    .word  pack_ui_state                  @ 080d4be0 50580003
DAT_080d4be4:
    .word  0x000006fc                     @ 080d4be4 fc060000
DAT_080d4be8:
    .word  0x000006fa                     @ 080d4be8 fa060000
LAB_080d4bec:
    ldrh r0,[r5,#0x38]                       @ 080d4bec 288f
    movs r1,#0x0    @ 080d4bee 0021
    movs r2,#0x0    @ 080d4bf0 0022
    bl dispatch_pack_card_image_render_by_state @ 080d4bf2 fff733ff
    adds r6,#0x4c    @ 080d4bf6 4c36
LAB_080d4bf8:
    ldrh r0,[r5,#0x38]                       @ 080d4bf8 288f
    adds r0,#0x1    @ 080d4bfa 0130
    movs r1,#0x4    @ 080d4bfc 0421
    bl get_bios_div_remainder                @ 080d4bfe 39f0fffb
    strh r0,[r5,#0x38]                       @ 080d4c02 2887
    movs r1,#0xde    @ 080d4c04 de21
    lsls r1,r1,#0x3    @ 080d4c06 c900
    adds r0,r5,r1    @ 080d4c08 6818
    ldr r3, DAT_080d4c54                     @ 080d4c0a 124b
    adds r2,r5,r3    @ 080d4c0c ea18
    ldrh r3,[r2,#0x0]                        @ 080d4c0e 1388
    lsls r1,r3,#0x2    @ 080d4c10 9900
    ldr r0,[r0,#0x0]                         @ 080d4c12 0068
    adds r4,r0,r1    @ 080d4c14 4418
    movs r0,#0xdf    @ 080d4c16 df20
    lsls r0,r0,#0x3    @ 080d4c18 c000
    adds r3,r5,r0    @ 080d4c1a 2b18
    movs r1,#0xf    @ 080d4c1c 0f21
    ldrb r4,[r4,#0x1]                        @ 080d4c1e 6478
    ands r1,r4    @ 080d4c20 2140
    lsls r1,r1,#0x2    @ 080d4c22 8900
    ldr r0,[r3,#0x0]                         @ 080d4c24 1868
    adds r0,r0,r1    @ 080d4c26 4018
    str r0,[r3,#0x0]                         @ 080d4c28 1860
    ldrh r0,[r2,#0x0]                        @ 080d4c2a 1088
    adds r0,#0x1    @ 080d4c2c 0130
    strh r0,[r2,#0x0]                        @ 080d4c2e 1080
    ldrh r1,[r5,#0x1a]                       @ 080d4c30 698b
    lsls r0,r1,#0x6    @ 080d4c32 8801
    adds r0,#0x10    @ 080d4c34 1030
    strh r0,[r5,#0x3a]                       @ 080d4c36 6887
    adds r0,r1,#0x0    @ 080d4c38 081c
    adds r0,#0x1    @ 080d4c3a 0130
    lsls r0,r0,#0x6    @ 080d4c3c 8001
    adds r0,#0x10    @ 080d4c3e 1030
    strh r0,[r5,#0x3c]                       @ 080d4c40 a887
    movs r0,#0x8    @ 080d4c42 0820
    strh r0,[r6,#0x0]                        @ 080d4c44 3080
    ldrh r0,[r5,#0x1a]                       @ 080d4c46 688b
    adds r0,#0x1    @ 080d4c48 0130
    strh r0,[r5,#0x1a]                       @ 080d4c4a 6883
    pop {r4,r5,r6}                           @ 080d4c4c 70bc
    pop {r0}                                 @ 080d4c4e 01bc
    bx r0                                    @ 080d4c50 0047
    .zero  0x2
DAT_080d4c54:
    .word  0x000006ee                     @ 080d4c54 ee060000

@ 拆包场景卡牌图反向滚动动画的逐帧 tick, 与 tick_pack_card_image_scroll_forward 镜像. 读取 pack_ui_state+0xc 工作结构: 帧计数 [+0x1a]-2 若小于 0 则以 0 参数渲染, 否则按当前卡牌索引 [+0x6fa] 从槽数组 [+0x6fc] 取卡牌记录 (反向递减色板偏移 [+0x704]) 调 dispatch_pack_card_image_render_by_state 渲染该帧卡图. 随后用 get_bios_div_remainder 推进子帧 [+0x38] (mod 4), 递减计数 [+0x6ee], 更新滚动位置 [+0x3a]/[+0x3c], 写状态 [+0]=8, 帧计数 [+0x1a] 自减 1 (反向).
tick_pack_card_image_scroll_back:
    push {r4,r5,r6,lr}                       @ 080d4c58 70b5
    ldr r4, DAT_080d4ca0                     @ 080d4c5a 114c
    adds r5,r4,#0x0    @ 080d4c5c 251c
    adds r5,#0xc    @ 080d4c5e 0c35
    ldrh r0,[r5,#0x1a]                       @ 080d4c60 688b
    subs r0,#0x2    @ 080d4c62 0238
    cmp r0,#0x0                              @ 080d4c64 0028
    blt LAB_080d4cb0                         @ 080d4c66 23db
    ldr r0, DAT_080d4ca4                     @ 080d4c68 0e48
    adds r2,r4,r0    @ 080d4c6a 2218
    ldr r1, DAT_080d4ca8                     @ 080d4c6c 0e49
    adds r0,r4,r1    @ 080d4c6e 6018
    ldrh r0,[r0,#0x0]                        @ 080d4c70 0088
    lsls r1,r0,#0x2    @ 080d4c72 8100
    ldr r0,[r2,#0x0]                         @ 080d4c74 1068
    adds r3,r0,r1    @ 080d4c76 4318
    ldr r2, DAT_080d4cac                     @ 080d4c78 0c4a
    adds r0,r4,r2    @ 080d4c7a a018
    ldr r2,[r0,#0x0]                         @ 080d4c7c 0268
    movs r1,#0x0    @ 080d4c7e 0021
    adds r4,#0x4c    @ 080d4c80 4c34
LAB_080d4c82:
    subs r3,#0x4    @ 080d4c82 043b
    movs r0,#0xf    @ 080d4c84 0f20
    ldrb r6,[r3,#0x1]                        @ 080d4c86 5e78
    ands r0,r6    @ 080d4c88 3040
    lsls r0,r0,#0x2    @ 080d4c8a 8000
    subs r2,r2,r0    @ 080d4c8c 121a
    adds r1,#0x1    @ 080d4c8e 0131
    cmp r1,#0x1                              @ 080d4c90 0129
    bls LAB_080d4c82                         @ 080d4c92 f6d9
    ldrh r0,[r5,#0x38]                       @ 080d4c94 288f
    adds r1,r3,#0x0    @ 080d4c96 191c
    bl dispatch_pack_card_image_render_by_state @ 080d4c98 fff7e0fe
    b LAB_080d4cbc                           @ 080d4c9c 0ee0
    .zero  0x2
DAT_080d4ca0:
    .word  pack_ui_state                  @ 080d4ca0 50580003
DAT_080d4ca4:
    .word  0x000006fc                     @ 080d4ca4 fc060000
DAT_080d4ca8:
    .word  0x000006fa                     @ 080d4ca8 fa060000
DAT_080d4cac:
    .word  0x00000704                     @ 080d4cac 04070000
LAB_080d4cb0:
    ldrh r0,[r5,#0x38]                       @ 080d4cb0 288f
    movs r1,#0x0    @ 080d4cb2 0021
    movs r2,#0x0    @ 080d4cb4 0022
    bl dispatch_pack_card_image_render_by_state @ 080d4cb6 fff7d1fe
    adds r4,#0x4c    @ 080d4cba 4c34
LAB_080d4cbc:
    ldrh r0,[r5,#0x38]                       @ 080d4cbc 288f
    adds r0,#0x3    @ 080d4cbe 0330
    movs r1,#0x4    @ 080d4cc0 0421
    bl get_bios_div_remainder                @ 080d4cc2 39f09dfb
    strh r0,[r5,#0x38]                       @ 080d4cc6 2887
    ldr r1, DAT_080d4d18                     @ 080d4cc8 1349
    adds r0,r5,r1    @ 080d4cca 6818
    ldrh r1,[r0,#0x0]                        @ 080d4ccc 0188
    subs r1,#0x1    @ 080d4cce 0139
    strh r1,[r0,#0x0]                        @ 080d4cd0 0180
    movs r2,#0xde    @ 080d4cd2 de22
    lsls r2,r2,#0x3    @ 080d4cd4 d200
    adds r1,r5,r2    @ 080d4cd6 a918
    ldrh r0,[r0,#0x0]                        @ 080d4cd8 0088
    lsls r2,r0,#0x2    @ 080d4cda 8200
    ldr r0,[r1,#0x0]                         @ 080d4cdc 0868
    adds r3,r0,r2    @ 080d4cde 8318
    movs r6,#0xdf    @ 080d4ce0 df26
    lsls r6,r6,#0x3    @ 080d4ce2 f600
    adds r2,r5,r6    @ 080d4ce4 aa19
    movs r1,#0xf    @ 080d4ce6 0f21
    ldrb r3,[r3,#0x1]                        @ 080d4ce8 5b78
    ands r1,r3    @ 080d4cea 1940
    lsls r1,r1,#0x2    @ 080d4cec 8900
    ldr r0,[r2,#0x0]                         @ 080d4cee 1068
    subs r0,r0,r1    @ 080d4cf0 401a
    str r0,[r2,#0x0]                         @ 080d4cf2 1060
    ldrh r1,[r5,#0x1a]                       @ 080d4cf4 698b
    lsls r0,r1,#0x6    @ 080d4cf6 8801
    adds r0,#0x10    @ 080d4cf8 1030
    strh r0,[r5,#0x3a]                       @ 080d4cfa 6887
    adds r0,r1,#0x0    @ 080d4cfc 081c
    subs r0,#0x1    @ 080d4cfe 0138
    lsls r0,r0,#0x6    @ 080d4d00 8001
    adds r0,#0x10    @ 080d4d02 1030
    strh r0,[r5,#0x3c]                       @ 080d4d04 a887
    movs r0,#0x8    @ 080d4d06 0820
    strh r0,[r4,#0x0]                        @ 080d4d08 2080
    ldrh r0,[r5,#0x1a]                       @ 080d4d0a 688b
    subs r0,#0x1    @ 080d4d0c 0138
    strh r0,[r5,#0x1a]                       @ 080d4d0e 6883
    pop {r4,r5,r6}                           @ 080d4d10 70bc
    pop {r0}                                 @ 080d4d12 01bc
    bx r0                                    @ 080d4d14 0047
    .zero  0x2
DAT_080d4d18:
    .word  0x000006ee                     @ 080d4d18 ee060000

@ Loads pack main UI BG tile graphics and palette. Reads huffman-compressed tile pointer from ROM 0x09cce2b0+0xc, decompresses to VRAM 0x0600d000; reads from 0x09cce2d0+0xc, decompresses to 0x0600f000. DMA-copies ROM 0x09cce2c0+0xc palette (32 bytes) to BG palette slot 0x050001a0. Called by pack main scene frame driver on entry; zero-parameter pure side-effect function.
@ 
@ Constants:
@ - ROM_GFX_TABLE_A = 0x09cce2b0 (pack BG tile data table A, +0xc = tile pointer)
@ - ROM_GFX_TABLE_B = 0x09cce2d0 (pack BG tile data table B)
@ - ROM_PAL_TABLE = 0x09cce2c0 (pack BG palette table, +0xc = palette pointer)
@ - VRAM_BG_TILE_A = 0x0600d000 (BG tile target region A)
@ - VRAM_BG_TILE_B = 0x0600f000 (BG tile target region B)
@ - BG_PAL_DST = 0x050001a0 (BG palette pack slot)
@ - PAL_SIZE = 0x20 (32 bytes, 16-color palette)
load_pack_bg_tiles_and_palette:
    push {lr}                                @ 080d4d1c 00b5
    ldr r0, DAT_080d4d44                     @ 080d4d1e 0948
    ldr r0,[r0,#0xc]                         @ 080d4d20 c068
    ldr r1, DAT_080d4d48                     @ 080d4d22 0949
    bl bios_huff_uncomp                      @ 080d4d24 39f078fb
    ldr r0, DAT_080d4d4c                     @ 080d4d28 0848
    ldr r0,[r0,#0xc]                         @ 080d4d2a c068
    ldr r1, DAT_080d4d50                     @ 080d4d2c 0849
    bl bios_huff_uncomp                      @ 080d4d2e 39f073fb
    ldr r0, DAT_080d4d54                     @ 080d4d32 0848
    ldr r1, DAT_080d4d58                     @ 080d4d34 0849
    ldr r1,[r1,#0xc]                         @ 080d4d36 c968
    movs r2,#0x20    @ 080d4d38 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d4d3a 20f0e5f8
    pop {r0}                                 @ 080d4d3e 01bc
    bx r0                                    @ 080d4d40 0047
    .zero  0x2
DAT_080d4d44:
    .word  0x09cce2b0                     @ 080d4d44 b0e2cc09
DAT_080d4d48:
    .word  0x0600d000                     @ 080d4d48 00d00006
DAT_080d4d4c:
    .word  0x09cce2d0                     @ 080d4d4c d0e2cc09
DAT_080d4d50:
    .word  0x0600f000                     @ 080d4d50 00f00006
DAT_080d4d54:
    .word  0x050001a0                     @ 080d4d54 a0010005
DAT_080d4d58:
    .word  0x09cce2c0                     @ 080d4d58 c0e2cc09

@ Renders a card image frame into a pack card OBJ VRAM slot. r0=slot_col, r1=row_group, r2=card_icid (signed; <0=clear). Computes dest address: ((row_group*5+slot_col)*3*0x200) + 0x06004040. If card_icid >= 0 calls copy_card_medium_frame_to_obj_vram(card_icid, dest, 0, 0); if < 0 calls zero_fill_halfword_wrapper(dest, 0x600). Called from FUN_080d4a5c (pack card image hub).
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x06004040 (DAT_080d4d84)
@ - SLOT_STRIDE = 0x200 (lsls r0,r2,#0x9 -> *512)
@ - CLEAR_SIZE = 0x600 (movs r1,#0xc0; lsls r1,r1,#3)
@ 
@ Inputs: r0=u32 slot_col [0..4]; r1=u32 row_group [0..?]; r2=s32 card_icid (<0=clear slot)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM 0x06004040+slot_offset] writes card tile data or zeros
render_pack_card_frame_to_slot:
    push {lr}                                @ 080d4d5c 00b5
    adds r3,r2,#0x0    @ 080d4d5e 131c
    lsls r2,r1,#0x2    @ 080d4d60 8a00
    adds r2,r2,r1    @ 080d4d62 5218
    adds r2,r2,r0    @ 080d4d64 1218
    lsls r0,r2,#0x1    @ 080d4d66 5000
    adds r0,r0,r2    @ 080d4d68 8018
    lsls r0,r0,#0x9    @ 080d4d6a 4002
    ldr r1, DAT_080d4d84                     @ 080d4d6c 0549
    adds r2,r0,r1    @ 080d4d6e 4218
    cmp r3,#0x0                              @ 080d4d70 002b
    blt LAB_080d4d88                         @ 080d4d72 09db
    adds r0,r3,#0x0    @ 080d4d74 181c
    adds r1,r2,#0x0    @ 080d4d76 111c
    movs r2,#0x0    @ 080d4d78 0022
    movs r3,#0x0    @ 080d4d7a 0023
    bl copy_card_medium_frame_to_obj_vram    @ 080d4d7c 06f0c8fd
    b LAB_080d4d92                           @ 080d4d80 07e0
    .zero  0x2
DAT_080d4d84:
    .word  0x06004040                     @ 080d4d84 40400006
LAB_080d4d88:
    movs r1,#0xc0    @ 080d4d88 c021
    lsls r1,r1,#0x3    @ 080d4d8a c900
    adds r0,r2,#0x0    @ 080d4d8c 101c
    bl zero_fill_halfword_wrapper            @ 080d4d8e 20f083f8
LAB_080d4d92:
    pop {r0}                                 @ 080d4d92 01bc
    bx r0                                    @ 080d4d94 0047
    .zero  0x2

@ Renders pack name string to OBJ sprite VRAM row. Caller passes r0=pack_name_ptr, r1=player_idx [0..1] during pack UI init or refresh. Flow: computes OBJ VRAM base address (0xc0<<0x13 + row_offset*0x20); calls zero_fill_pack_obj_vram_region to clear target region; calls pack_name_text_render to render name text and returns tile write count; writes count to pack_ui_state+0xc+0x10/0x12; calls write_pack_obj_tile_strip to write tile strip.
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x6000000 (movs r4,#0xc0; lsls #0x13)
@ - ROW_STRIDE = 0x20 (row_offset * 32)
@ - pack_ui_state = 0x03005850
@ - TILE_OBJ_BASE = 0x0600e000
render_pack_name_to_obj_sprite_row:
    push {r4,r5,r6,r7,lr}                    @ 080d4d98 f0b5
    adds r6,r0,#0x0    @ 080d4d9a 061c
    ldr r0, DAT_080d4ddc                     @ 080d4d9c 0f48
    adds r7,r0,#0x0    @ 080d4d9e 071c
    adds r7,#0xc    @ 080d4da0 0c37
    movs r4,#0xc0    @ 080d4da2 c024
    lsls r4,r4,#0x13    @ 080d4da4 e404
    movs r5,#0x0    @ 080d4da6 0025
    cmp r1,#0x0                              @ 080d4da8 0029
    beq LAB_080d4dae                         @ 080d4daa 00d0
    movs r5,#0xf5    @ 080d4dac f525
LAB_080d4dae:
    adds r5,#0x1    @ 080d4dae 0135
    lsls r0,r5,#0x5    @ 080d4db0 6801
    adds r4,r0,r4    @ 080d4db2 0419
    adds r0,r4,#0x0    @ 080d4db4 201c
    bl zero_fill_pack_obj_vram_region        @ 080d4db6 06f0fbfe
    adds r0,r4,#0x0    @ 080d4dba 201c
    adds r1,r6,#0x0    @ 080d4dbc 311c
    bl pack_name_text_render                 @ 080d4dbe 06f0fffe
    movs r1,#0x0    @ 080d4dc2 0021
    strh r0,[r7,#0x10]                       @ 080d4dc4 3882
    strh r1,[r7,#0x12]                       @ 080d4dc6 7982
    ldr r0, DAT_080d4de0                     @ 080d4dc8 0548
    adds r1,r5,#0x0    @ 080d4dca 291c
    movs r2,#0xf    @ 080d4dcc 0f22
    movs r3,#0x0    @ 080d4dce 0023
    bl write_pack_obj_tile_strip             @ 080d4dd0 06f05aff
    pop {r4,r5,r6,r7}                        @ 080d4dd4 f0bc
    pop {r0}                                 @ 080d4dd6 01bc
    bx r0                                    @ 080d4dd8 0047
    .zero  0x2
DAT_080d4ddc:
    .word  pack_ui_state                  @ 080d4ddc 50580003
DAT_080d4de0:
    .word  0x0600e000                     @ 080d4de0 00e00006

@ Renders card name to OBJ sprite VRAM row and updates BG palette row. Caller passes r0=pack_ctx_ptr, r1=scroll_state_ptr, r2=player_idx during pack card list refresh. Flow: computes OBJ VRAM row address (0xc0<<0x13 + row_offset*0x20); calls zero_fill_pack_obj_vram_region_alt to clear target region; clears scroll_state_ptr[+0x16]; if r0 non-null calls render_pack_card_name_to_sprite and writes return value to scroll_state_ptr[+0x14]; calls fill_pack_bg_tile_row_with_palette to fill BG palette row.
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x6000000 (0xc0 << 0x13)
@ - ROW_STRIDE = 0x20 (lsls #5)
@ - ROW_STEP = 0x95 (r2==0) or 0x8a (r2!=0)
@ - BG_BASE = 0x0600e000
@ - BG_COLS = 0xa
@ - pack_ui_state = 0x03005850
render_pack_card_name_to_sprite_row:
    push {r4,r5,r6,r7,lr}                    @ 080d4de4 f0b5
    .hword 0x4647    @ 080d4de6 4746
    push {r7}                                @ 080d4de8 80b4
    adds r6,r0,#0x0    @ 080d4dea 061c
    adds r7,r1,#0x0    @ 080d4dec 0f1c
    ldr r0, DAT_080d4e40                     @ 080d4dee 1448
    adds r0,#0xc    @ 080d4df0 0c30
    .hword 0x4680    @ 080d4df2 8046
    movs r4,#0xc0    @ 080d4df4 c024
    lsls r4,r4,#0x13    @ 080d4df6 e404
    movs r5,#0x0    @ 080d4df8 0025
    cmp r2,#0x0                              @ 080d4dfa 002a
    beq LAB_080d4e00                         @ 080d4dfc 00d0
    movs r5,#0xf5    @ 080d4dfe f525
LAB_080d4e00:
    adds r5,#0x95    @ 080d4e00 9535
    lsls r0,r5,#0x5    @ 080d4e02 6801
    adds r4,r0,r4    @ 080d4e04 0419
    adds r0,r4,#0x0    @ 080d4e06 201c
    bl zero_fill_pack_obj_vram_region_alt    @ 080d4e08 06f070ff
    movs r0,#0x0    @ 080d4e0c 0020
    .hword 0x4641    @ 080d4e0e 4146
    strh r0,[r1,#0x16]                       @ 080d4e10 c882
    cmp r6,#0x0                              @ 080d4e12 002e
    beq LAB_080d4e36                         @ 080d4e14 0fd0
    adds r0,r4,#0x0    @ 080d4e16 201c
    adds r1,r6,#0x0    @ 080d4e18 311c
    adds r2,r7,#0x0    @ 080d4e1a 3a1c
    bl render_pack_card_name_to_sprite       @ 080d4e1c 06f06eff
    .hword 0x4641    @ 080d4e20 4146
    strh r0,[r1,#0x14]                       @ 080d4e22 8882
    movs r0,#0x80    @ 080d4e24 8020
    lsls r0,r0,#0x3    @ 080d4e26 c000
    ldr r1, DAT_080d4e44                     @ 080d4e28 0649
    adds r0,r0,r1    @ 080d4e2a 4018
    adds r1,r5,#0x0    @ 080d4e2c 291c
    movs r2,#0xa    @ 080d4e2e 0a22
    movs r3,#0x0    @ 080d4e30 0023
    bl fill_pack_bg_tile_row_with_palette    @ 080d4e32 06f0efff
LAB_080d4e36:
    pop {r3}                                 @ 080d4e36 08bc
    .hword 0x4698    @ 080d4e38 9846
    pop {r4,r5,r6,r7}                        @ 080d4e3a f0bc
    pop {r0}                                 @ 080d4e3c 01bc
    bx r0                                    @ 080d4e3e 0047
DAT_080d4e40:
    .word  pack_ui_state                  @ 080d4e40 50580003
DAT_080d4e44:
    .word  0x0600e000                     @ 080d4e44 00e00006

@ Renders player-owned card count for a pack slot to OBJ sprite VRAM row. Caller passes r0=pack_ctx_ptr, r1=player_idx [0..1] during pack UI refresh. Flow: computes OBJ VRAM row address (0xc0<<0x13 + row_offset*0x20); calls count_owned_cards_in_pack_slot to get count; calls zero_fill_pack_obj_vram_row_b to clear row; calls render_pack_card_count_to_sprite_vram to render digit; calls fill_pack_obj_tile_region_13col_b(0x0600e09e, row, 0xf) to fill 13-column OBJ tile region.
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x6000000 (0xc0 << 0x13)
@ - ROW_STEP = 0x61 (player_idx==0 -> r6=0x61; player_idx!=0 -> r6=0x56)
@ - TILE_OBJ_ALT = 0x0600e09e
@ - TILE_COLS = 0xf
render_pack_owned_count_to_sprite_row:
    push {r4,r5,r6,r7,lr}                    @ 080d4e48 f0b5
    adds r7,r0,#0x0    @ 080d4e4a 071c
    movs r5,#0xc0    @ 080d4e4c c025
    lsls r5,r5,#0x13    @ 080d4e4e ed04
    movs r6,#0x0    @ 080d4e50 0026
    cmp r1,#0x0                              @ 080d4e52 0029
    beq LAB_080d4e58                         @ 080d4e54 00d0
    movs r6,#0xf5    @ 080d4e56 f526
LAB_080d4e58:
    adds r6,#0x61    @ 080d4e58 6136
    lsls r0,r6,#0x5    @ 080d4e5a 7001
    adds r5,r0,r5    @ 080d4e5c 4519
    adds r0,r7,#0x0    @ 080d4e5e 381c
    bl count_owned_cards_in_pack_slot        @ 080d4e60 06f0ccfb
    adds r4,r0,#0x0    @ 080d4e64 041c
    adds r0,r5,#0x0    @ 080d4e66 281c
    bl zero_fill_pack_obj_vram_row_b         @ 080d4e68 07f00ef9
    adds r0,r5,#0x0    @ 080d4e6c 281c
    adds r1,r7,#0x0    @ 080d4e6e 391c
    adds r2,r4,#0x0    @ 080d4e70 221c
    bl render_pack_card_count_to_sprite_vram @ 080d4e72 07f011f9
    ldr r0, DAT_080d4e88                     @ 080d4e76 0448
    adds r1,r6,#0x0    @ 080d4e78 311c
    movs r2,#0xf    @ 080d4e7a 0f22
    bl fill_pack_obj_tile_region_13col_b     @ 080d4e7c 07f09cf9
    pop {r4,r5,r6,r7}                        @ 080d4e80 f0bc
    pop {r0}                                 @ 080d4e82 01bc
    bx r0                                    @ 080d4e84 0047
    .zero  0x2
DAT_080d4e88:
    .word  0x0600e09e                     @ 080d4e88 9ee00006

@ Renders pack label name to OBJ sprite VRAM row and fills OBJ tile region. Caller passes r0=pack_ctx_ptr, r1=player_idx [0..1] during pack UI refresh. Flow: computes OBJ VRAM row address (0xc0<<0x13 + row_offset*0x20); calls zero_fill_pack_obj_vram_row_a to clear row; calls render_pack_label_name_to_sprite_vram to render label name; calls fill_pack_obj_tile_region_13col(0x0600e084, row, 0xf) to fill 13-column OBJ tile region.
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x6000000 (0xc0 << 0x13)
@ - ROW_STEP = 0x7b (player_idx==0 -> r5=0x7b; player_idx!=0 -> r5=0x70)
@ - TILE_OBJ_LABEL = 0x0600e084
@ - TILE_COLS = 0xf
render_pack_label_name_to_sprite_row:
    push {r4,r5,r6,lr}                       @ 080d4e8c 70b5
    adds r6,r0,#0x0    @ 080d4e8e 061c
    movs r4,#0xc0    @ 080d4e90 c024
    lsls r4,r4,#0x13    @ 080d4e92 e404
    movs r5,#0x0    @ 080d4e94 0025
    cmp r1,#0x0                              @ 080d4e96 0029
    beq LAB_080d4e9c                         @ 080d4e98 00d0
    movs r5,#0xf5    @ 080d4e9a f525
LAB_080d4e9c:
    adds r5,#0x7b    @ 080d4e9c 7b35
    lsls r0,r5,#0x5    @ 080d4e9e 6801
    adds r4,r0,r4    @ 080d4ea0 0419
    adds r0,r4,#0x0    @ 080d4ea2 201c
    bl zero_fill_pack_obj_vram_row_a         @ 080d4ea4 07f044f8
    adds r0,r4,#0x0    @ 080d4ea8 201c
    adds r1,r6,#0x0    @ 080d4eaa 311c
    bl render_pack_label_name_to_sprite_vram @ 080d4eac 07f048f8
    ldr r0, DAT_080d4ec0                     @ 080d4eb0 0348
    adds r1,r5,#0x0    @ 080d4eb2 291c
    movs r2,#0xf    @ 080d4eb4 0f22
    bl fill_pack_obj_tile_region_13col       @ 080d4eb6 07f0cff8
    pop {r4,r5,r6}                           @ 080d4eba 70bc
    pop {r0}                                 @ 080d4ebc 01bc
    bx r0                                    @ 080d4ebe 0047
DAT_080d4ec0:
    .word  0x0600e084                     @ 080d4ec0 84e00006

@ Fills tile IDs for a specified card slot in pack card shop BG tilemap (0x0600e80a). Uses r0 (col_group) and r1 (row_group) to compute tilemap offset: ((r1*5+r0)*24+1)*2 bytes. Loops writing 4 columns x 6 rows of tile block, tile IDs start at (r1*5+r0)*24+1 and increment consecutively. Used during card shop init to fill slot grid with valid tile IDs.
@ 
@ Constants:
@ - TILEMAP_BASE = 0x0600e80a (BG tilemap card slot region start)
@ - COLS_PER_SLOT = 4 (columns per slot [0..3])
@ - ROWS_PER_SLOT = 6 (rows per slot [0..5])
@ - TILEMAP_ROW_STRIDE = 0x40 (32 tiles * 2 bytes per row)
@ - FIRST_TILE_ID = (r1*5+r0)*24+1 (start tile ID, nonzero)
fill_pack_card_slot_tiles:
    push {r4,lr}                             @ 080d4ec4 10b5
    lsls r3,r1,#0x2    @ 080d4ec6 8b00
    adds r3,r3,r1    @ 080d4ec8 5b18
    adds r3,r3,r0    @ 080d4eca 1b18
    lsls r2,r3,#0x1    @ 080d4ecc 5a00
    adds r2,r2,r3    @ 080d4ece d218
    lsls r2,r2,#0x3    @ 080d4ed0 d200
    adds r2,#0x1    @ 080d4ed2 0132
    lsls r2,r2,#0x10    @ 080d4ed4 1204
    lsrs r3,r2,#0x10    @ 080d4ed6 130c
    lsls r1,r1,#0x3    @ 080d4ed8 c900
    adds r1,#0x1    @ 080d4eda 0131
    lsls r1,r1,#0x5    @ 080d4edc 4901
    lsls r2,r0,#0x2    @ 080d4ede 8200
    adds r2,r2,r0    @ 080d4ee0 1218
    adds r1,r1,r2    @ 080d4ee2 8918
    lsls r1,r1,#0x1    @ 080d4ee4 4900
    ldr r0, DAT_080d4f10                     @ 080d4ee6 0a48
    adds r1,r1,r0    @ 080d4ee8 0918
    movs r0,#0x0    @ 080d4eea 0020
LAB_080d4eec:
    movs r2,#0x0    @ 080d4eec 0022
    adds r4,r0,#0x1    @ 080d4eee 441c
LAB_080d4ef0:
    strh r3,[r1,#0x0]                        @ 080d4ef0 0b80
    adds r1,#0x2    @ 080d4ef2 0231
    adds r0,r3,#0x1    @ 080d4ef4 581c
    lsls r0,r0,#0x10    @ 080d4ef6 0004
    lsrs r3,r0,#0x10    @ 080d4ef8 030c
    adds r2,#0x1    @ 080d4efa 0132
    cmp r2,#0x3                              @ 080d4efc 032a
    bls LAB_080d4ef0                         @ 080d4efe f7d9
    adds r1,#0x38    @ 080d4f00 3831
    adds r0,r4,#0x0    @ 080d4f02 201c
    cmp r0,#0x5                              @ 080d4f04 0528
    bls LAB_080d4eec                         @ 080d4f06 f1d9
    pop {r4}                                 @ 080d4f08 10bc
    pop {r0}                                 @ 080d4f0a 01bc
    bx r0                                    @ 080d4f0c 0047
    .zero  0x2
DAT_080d4f10:
    .word  0x0600e80a                     @ 080d4f10 0ae80006

@ Clears tile IDs for a specified card slot in pack card shop BG tilemap (0x0600e80a), writing all-zero (transparent tile). Address calculation matches fill_pack_card_slot_tiles: r0 (col_group) and r1 (row_group) determine offset; writes 4 columns x 6 rows with fixed tile ID=0. Used to hide or refresh card slot patterns by clearing old content before refilling.
@ 
@ Constants:
@ - TILEMAP_BASE = 0x0600e80a (BG tilemap card slot region, same as fill_pack_card_slot_tiles)
@ - TILE_ID_CLEAR = 0x0 (transparent tile)
@ - COLS_PER_SLOT = 4, ROWS_PER_SLOT = 6
@ - TILEMAP_ROW_STRIDE = 0x40 (row stride)
clear_pack_card_slot_tiles:
    lsls r1,r1,#0x3    @ 080d4f14 c900
    adds r1,#0x1    @ 080d4f16 0131
    lsls r1,r1,#0x5    @ 080d4f18 4901
    lsls r2,r0,#0x2    @ 080d4f1a 8200
    adds r2,r2,r0    @ 080d4f1c 1218
    adds r1,r1,r2    @ 080d4f1e 8918
    lsls r1,r1,#0x1    @ 080d4f20 4900
    ldr r0, DAT_080d4f40                     @ 080d4f22 0748
    adds r1,r1,r0    @ 080d4f24 0918
    movs r2,#0x0    @ 080d4f26 0022
    movs r3,#0x0    @ 080d4f28 0023
LAB_080d4f2a:
    movs r0,#0x0    @ 080d4f2a 0020
    adds r2,#0x1    @ 080d4f2c 0132
LAB_080d4f2e:
    strh r3,[r1,#0x0]                        @ 080d4f2e 0b80
    adds r1,#0x2    @ 080d4f30 0231
    adds r0,#0x1    @ 080d4f32 0130
    cmp r0,#0x3                              @ 080d4f34 0328
    bls LAB_080d4f2e                         @ 080d4f36 fad9
    adds r1,#0x38    @ 080d4f38 3831
    cmp r2,#0x5                              @ 080d4f3a 052a
    bls LAB_080d4f2a                         @ 080d4f3c f5d9
    bx lr                                    @ 080d4f3e 7047
DAT_080d4f40:
    .word  0x0600e80a                     @ 080d4f40 0ae80006

@ Pack name OBJ sprite scroll strip frame tick function for row 0. Each frame: reads pack_ui_state+0xc+0x10 counter; if > 0x1e (30), reads [+0x12] current offset, advances by +8 and mods by 0xc0<<6=0x3000 (12288); else sets offset to 0. If offset changed (r5 != r3), calls write_pack_obj_tile_strip(0x0600e000, row_offset, 0xf) to update tile strip. Side effects: updates [pack_ui_state+0xc+0x12] = (old + 8) % 0x3000; conditionally writes OBJ tile strip.
@ 
@ Constants:
@ - SCROLL_THRESHOLD = 0x1e (cmp r0,#0x1e)
@ - SCROLL_STEP = 8 (adds r0,#8)
@ - SCROLL_MOD = 0x3000 (0xc0 << 6 = 12288)
@ - TILE_OBJ_BASE = 0x0600e000
@ - TILE_COLS = 0xf
@ - pack_ui_state = 0x03005850
tick_pack_name_scroll_strip_row0:
    push {r4,r5,r6,lr}                       @ 080d4f44 70b5
    ldr r1, DAT_080d4f64                     @ 080d4f46 0749
    adds r4,r1,#0x0    @ 080d4f48 0c1c
    adds r4,#0xc    @ 080d4f4a 0c34
    movs r6,#0x0    @ 080d4f4c 0026
    cmp r0,#0x0                              @ 080d4f4e 0028
    beq LAB_080d4f54                         @ 080d4f50 00d0
    movs r6,#0xf5    @ 080d4f52 f526
LAB_080d4f54:
    adds r6,#0x1    @ 080d4f54 0136
    ldrh r0,[r4,#0x10]                       @ 080d4f56 208a
    cmp r0,#0x1e                             @ 080d4f58 1e28
    bls LAB_080d4f68                         @ 080d4f5a 05d9
    ldrh r0,[r4,#0x12]                       @ 080d4f5c 608a
    lsrs r5,r0,#0x8    @ 080d4f5e 050a
    b LAB_080d4f6c                           @ 080d4f60 04e0
    .zero  0x2
DAT_080d4f64:
    .word  pack_ui_state                  @ 080d4f64 50580003
LAB_080d4f68:
    movs r5,#0x0    @ 080d4f68 0025
    ldrh r0,[r4,#0x12]                       @ 080d4f6a 608a
LAB_080d4f6c:
    adds r0,#0x8    @ 080d4f6c 0830
    strh r0,[r4,#0x12]                       @ 080d4f6e 6082
    ldrh r0,[r4,#0x12]                       @ 080d4f70 608a
    movs r1,#0xc0    @ 080d4f72 c021
    lsls r1,r1,#0x6    @ 080d4f74 8901
    bl get_bios_div_remainder                @ 080d4f76 39f043fa
    strh r0,[r4,#0x12]                       @ 080d4f7a 6082
    ldrh r4,[r4,#0x10]                       @ 080d4f7c 248a
    cmp r4,#0x1e                             @ 080d4f7e 1e2c
    bls LAB_080d4f88                         @ 080d4f80 02d9
    lsls r0,r0,#0x10    @ 080d4f82 0004
    lsrs r3,r0,#0x18    @ 080d4f84 030e
    b LAB_080d4f8a                           @ 080d4f86 00e0
LAB_080d4f88:
    movs r3,#0x0    @ 080d4f88 0023
LAB_080d4f8a:
    cmp r5,r3                                @ 080d4f8a 9d42
    beq LAB_080d4f98                         @ 080d4f8c 04d0
    ldr r0, DAT_080d4fa0                     @ 080d4f8e 0448
    adds r1,r6,#0x0    @ 080d4f90 311c
    movs r2,#0xf    @ 080d4f92 0f22
    bl write_pack_obj_tile_strip             @ 080d4f94 06f078fe
LAB_080d4f98:
    pop {r4,r5,r6}                           @ 080d4f98 70bc
    pop {r0}                                 @ 080d4f9a 01bc
    bx r0                                    @ 080d4f9c 0047
    .zero  0x2
DAT_080d4fa0:
    .word  0x0600e000                     @ 080d4fa0 00e00006

@ 拆包场景 BG 调色板色相滚动帧更新. 入口 r0 决定初始相位偏移: r0!=0 时 r6=0xf5, r0==0 时 r6=0; 再统一 +0x95. 从 pack_ui_state+0xc+0x14 读当前滚动位置 (scroll_pos), 若 >0x1e 则提取 [+0x16] 高字节为 r5 (当前 hue 行). 将 scroll_pos+8 写回, 再对 0xc0<<6=0x3000 取余 (BG tile 行数归一化). 若 r5 != r3 (当前行 vs 上一行) 则以 OBJ VRAM 行 0x0600e000+r6<<3 为目标, 宽度 0xa 调 fill_pack_bg_tile_row_with_palette 刷新调色板行. 最终计算色相梯度偏移并调 fill_pack_palette_hue_gradient 写 OBJ 调色板 0x05000140. 调用者 FUN_080d67a8 / FUN_080d6a90 在 pack 滚动卡图翻页中使用.
tick_pack_bg_palette_hue_scroll:
    push {r4,r5,r6,lr}                       @ 080d4fa4 70b5
    ldr r1, DAT_080d4fc4                     @ 080d4fa6 0749
    adds r4,r1,#0x0    @ 080d4fa8 0c1c
    adds r4,#0xc    @ 080d4faa 0c34
    movs r6,#0x0    @ 080d4fac 0026
    cmp r0,#0x0                              @ 080d4fae 0028
    beq LAB_080d4fb4                         @ 080d4fb0 00d0
    movs r6,#0xf5    @ 080d4fb2 f526
LAB_080d4fb4:
    adds r6,#0x95    @ 080d4fb4 9536
    ldrh r0,[r4,#0x14]                       @ 080d4fb6 a08a
    cmp r0,#0x1e                             @ 080d4fb8 1e28
    bls LAB_080d4fc8                         @ 080d4fba 05d9
    ldrh r0,[r4,#0x16]                       @ 080d4fbc e08a
    lsrs r5,r0,#0x8    @ 080d4fbe 050a
    b LAB_080d4fcc                           @ 080d4fc0 04e0
    .zero  0x2
DAT_080d4fc4:
    .word  pack_ui_state                  @ 080d4fc4 50580003
LAB_080d4fc8:
    movs r5,#0x0    @ 080d4fc8 0025
    ldrh r0,[r4,#0x16]                       @ 080d4fca e08a
LAB_080d4fcc:
    adds r0,#0x8    @ 080d4fcc 0830
    strh r0,[r4,#0x16]                       @ 080d4fce e082
    ldrh r0,[r4,#0x16]                       @ 080d4fd0 e08a
    movs r1,#0xc0    @ 080d4fd2 c021
    lsls r1,r1,#0x6    @ 080d4fd4 8901
    bl get_bios_div_remainder                @ 080d4fd6 39f013fa
    strh r0,[r4,#0x16]                       @ 080d4fda e082
    ldrh r1,[r4,#0x14]                       @ 080d4fdc a18a
    cmp r1,#0x1e                             @ 080d4fde 1e29
    bls LAB_080d4fe8                         @ 080d4fe0 02d9
    lsls r0,r0,#0x10    @ 080d4fe2 0004
    lsrs r3,r0,#0x18    @ 080d4fe4 030e
    b LAB_080d4fea                           @ 080d4fe6 00e0
LAB_080d4fe8:
    movs r3,#0x0    @ 080d4fe8 0023
LAB_080d4fea:
    cmp r5,r3                                @ 080d4fea 9d42
    beq LAB_080d4ffe                         @ 080d4fec 07d0
    movs r0,#0x80    @ 080d4fee 8020
    lsls r0,r0,#0x3    @ 080d4ff0 c000
    ldr r1, DAT_080d502c                     @ 080d4ff2 0e49
    adds r0,r0,r1    @ 080d4ff4 4018
    adds r1,r6,#0x0    @ 080d4ff6 311c
    movs r2,#0xa    @ 080d4ff8 0a22
    bl fill_pack_bg_tile_row_with_palette    @ 080d4ffa 06f00bff
LAB_080d4ffe:
    ldrh r0,[r4,#0x16]                       @ 080d4ffe e08a
    lsls r1,r0,#0x1    @ 080d5000 4100
    adds r1,r1,r0    @ 080d5002 0918
    lsls r0,r1,#0x4    @ 080d5004 0801
    subs r0,r0,r1    @ 080d5006 401a
    lsls r0,r0,#0x3    @ 080d5008 c000
    movs r1,#0xc0    @ 080d500a c021
    lsls r1,r1,#0x1    @ 080d500c 4900
    bl bios_div                              @ 080d500e 39f0f5f9
    adds r2,r0,#0x0    @ 080d5012 021c
    movs r1,#0xb4    @ 080d5014 b421
    lsls r1,r1,#0x1    @ 080d5016 4900
    bl get_bios_div_remainder                @ 080d5018 39f0f2f9
    adds r2,r0,#0x0    @ 080d501c 021c
    ldr r0, DAT_080d5030                     @ 080d501e 0448
    adds r1,r2,#0x0    @ 080d5020 111c
    bl fill_pack_palette_hue_gradient        @ 080d5022 06f04bff
    pop {r4,r5,r6}                           @ 080d5026 70bc
    pop {r0}                                 @ 080d5028 01bc
    bx r0                                    @ 080d502a 0047
DAT_080d502c:
    .word  0x0600e000                     @ 080d502c 00e00006
DAT_080d5030:
    .word  0x05000140                     @ 080d5030 40010005

@ Renders a pack banner image into an OBJ VRAM slot, or zeros the slot. r0=slot_idx, r1=pack_banner_ptr (signed; <0=clear). Divides slot_idx by 4 for col/row, computes dest = 0x06010000 + (col*4+row*8)*0x40. If pack_banner_ptr >= 0 calls pack_banner_tile_copy(ptr, dest, 0, 1); if < 0 loops 8 times calling zero_fill_halfword_wrapper(dest, 0x100). Called from FUN_080d4a5c (pack card image hub).
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x06010000 (DAT_080d5068)
@ - SLOT_BLOCK_SIZE = 0x40 (lsls r5,r5,#6)
@ - CLEAR_ITER = 8 (cmp r4,#7 -> 0..7)
@ - CLEAR_SIZE_PER_ITER = 0x100 halfwords (movs r1,#0x80; lsls r1,r1,#1)
@ 
@ Inputs: r0=u32 slot_idx [0..?]; r1=s32 pack_banner_ptr (<0=clear)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM 0x06010000+slot_offset] writes banner tiles or zeros
render_pack_banner_to_slot:
    push {r4,r5,r6,lr}                       @ 080d5034 70b5
    adds r4,r0,#0x0    @ 080d5036 041c
    adds r6,r1,#0x0    @ 080d5038 0e1c
    movs r1,#0x4    @ 080d503a 0421
    bl get_bios_div_remainder                @ 080d503c 39f0e0f9
    adds r5,r0,#0x0    @ 080d5040 051c
    adds r0,r4,#0x0    @ 080d5042 201c
    movs r1,#0x4    @ 080d5044 0421
    bl bios_div                              @ 080d5046 39f0d9f9
    lsls r5,r5,#0x2    @ 080d504a ad00
    lsls r0,r0,#0x3    @ 080d504c c000
    adds r5,r5,r0    @ 080d504e 2d18
    lsls r5,r5,#0x6    @ 080d5050 ad01
    ldr r0, DAT_080d5068                     @ 080d5052 0548
    adds r5,r5,r0    @ 080d5054 2d18
    cmp r6,#0x0                              @ 080d5056 002e
    blt LAB_080d506c                         @ 080d5058 08db
    adds r0,r6,#0x0    @ 080d505a 301c
    adds r1,r5,#0x0    @ 080d505c 291c
    movs r2,#0x0    @ 080d505e 0022
    movs r3,#0x1    @ 080d5060 0123
    bl pack_banner_tile_copy                 @ 080d5062 06f0fdfb
    b LAB_080d5084                           @ 080d5066 0de0
DAT_080d5068:
    .word  0x06010000                     @ 080d5068 00000106
LAB_080d506c:
    movs r4,#0x0    @ 080d506c 0024
LAB_080d506e:
    adds r0,r5,#0x0    @ 080d506e 281c
    movs r1,#0x80    @ 080d5070 8021
    lsls r1,r1,#0x1    @ 080d5072 4900
    bl zero_fill_halfword_wrapper            @ 080d5074 1ff010ff
    movs r0,#0x80    @ 080d5078 8020
    lsls r0,r0,#0x3    @ 080d507a c000
    adds r5,r5,r0    @ 080d507c 2d18
    adds r4,#0x1    @ 080d507e 0134
    cmp r4,#0x7                              @ 080d5080 072c
    bls LAB_080d506e                         @ 080d5082 f4d9
LAB_080d5084:
    pop {r4,r5,r6}                           @ 080d5084 70bc
    pop {r0}                                 @ 080d5086 01bc
    bx r0                                    @ 080d5088 0047
    .zero  0x2

@ Renders a card image frame to the pack card info page OBJ VRAM slot (base 0x06010000, different offset formula from FUN_080d5034). r0=slot_linear, r1=card_icid (signed). Computes dest = 0x06010000 + ((col*3+row*6)*0x40+0x100)*0x20 where col=slot&3, row=slot>>2. If card_icid >= 0 calls copy_card_medium_frame_to_obj_vram; if < 0 loops 6 times calling zero_fill_halfword_wrapper. Called from FUN_080d5e84 (pack card image info page driver).
@ 
@ Constants:
@ - OBJ_VRAM_BASE = 0x06010000 (DAT_080d50c0)
@ - CLEAR_ITER = 6 (cmp r5,#5 -> 0..5)
@ 
@ Inputs: r0=u32 slot_linear [0..?]; r1=s32 card_icid (<0=clear)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM 0x06010000+slot_offset] writes card tiles or zeros
render_pack_card_frame_to_info_slot:
    push {r4,r5,lr}                          @ 080d508c 30b5
    adds r3,r1,#0x0    @ 080d508e 0b1c
    movs r2,#0x3    @ 080d5090 0322
    ands r2,r0    @ 080d5092 0240
    lsls r2,r2,#0x3    @ 080d5094 d200
    lsrs r0,r0,#0x2    @ 080d5096 8008
    lsls r1,r0,#0x1    @ 080d5098 4100
    adds r1,r1,r0    @ 080d509a 0918
    lsls r1,r1,#0x6    @ 080d509c 8901
    movs r0,#0x80    @ 080d509e 8020
    lsls r0,r0,#0x1    @ 080d50a0 4000
    adds r1,r1,r0    @ 080d50a2 0918
    adds r2,r2,r1    @ 080d50a4 5218
    lsls r2,r2,#0x5    @ 080d50a6 5201
    ldr r0, DAT_080d50c0                     @ 080d50a8 0548
    adds r4,r2,r0    @ 080d50aa 1418
    cmp r3,#0x0                              @ 080d50ac 002b
    blt LAB_080d50c4                         @ 080d50ae 09db
    adds r0,r3,#0x0    @ 080d50b0 181c
    adds r1,r4,#0x0    @ 080d50b2 211c
    movs r2,#0x0    @ 080d50b4 0022
    movs r3,#0x1    @ 080d50b6 0123
    bl copy_card_medium_frame_to_obj_vram    @ 080d50b8 06f02afc
    b LAB_080d50dc                           @ 080d50bc 0ee0
    .zero  0x2
DAT_080d50c0:
    .word  0x06010000                     @ 080d50c0 00000106
LAB_080d50c4:
    movs r5,#0x0    @ 080d50c4 0025
LAB_080d50c6:
    adds r0,r4,#0x0    @ 080d50c6 201c
    movs r1,#0x80    @ 080d50c8 8021
    lsls r1,r1,#0x1    @ 080d50ca 4900
    bl zero_fill_halfword_wrapper            @ 080d50cc 1ff0e4fe
    movs r0,#0x80    @ 080d50d0 8020
    lsls r0,r0,#0x3    @ 080d50d2 c000
    adds r4,r4,r0    @ 080d50d4 2418
    adds r5,#0x1    @ 080d50d6 0135
    cmp r5,#0x5                              @ 080d50d8 052d
    bls LAB_080d50c6                         @ 080d50da f4d9
LAB_080d50dc:
    pop {r4,r5}                              @ 080d50dc 30bc
    pop {r0}                                 @ 080d50de 01bc
    bx r0                                    @ 080d50e0 0047
    .zero  0x2

@ Initializes the pack card AOB (animated object) display row tile data. Loads AOB descriptor base from pack_ui_state+0x70c. First calls write_pack_card_tile_rows_to_obj_vram(0x1c8, 0xe) to write tile row data; then loops calling init_pack_card_slot_aob_from_ptn(0x1c8, 0xe, aob_ptr) with +0x14 step per slot. Loop condition: r5 wraps to 0 (adds r5,#1; cmp r5,#0; beq). Called from pack_banner_080d566c and pack_banner_080d6d30 for pack scene card row AOB init.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d5114)
@ - AOB_DESC_OFFSET = 0x70c (DAT_080d5118)
@ - TILE_ROW_ID = 0x1c8 (movs r0,#0xe4; lsls r0,r0,#1 -> 0x1c8)
@ - TILE_ROW_COUNT = 0xe
@ - AOB_ENTRY_STRIDE = 0x14 (adds r4,#0x14)
@ 
@ Inputs: none (entry: push then ldr r4, pack_ui_state)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OBJ VRAM via write_pack_card_tile_rows_to_obj_vram] writes tile rows; [pack_ui_state+0x70c area via init_pack_card_slot_aob_from_ptn] initializes AOB descriptors
init_pack_card_aob_display_row:
    push {r4,r5,lr}                          @ 080d50e4 30b5
    ldr r4, DAT_080d5114                     @ 080d50e6 0b4c
    movs r0,#0xe4    @ 080d50e8 e420
    lsls r0,r0,#0x1    @ 080d50ea 4000
    movs r1,#0xe    @ 080d50ec 0e21
    bl write_pack_card_tile_rows_to_obj_vram @ 080d50ee 07f0fdf9
    movs r5,#0x0    @ 080d50f2 0025
    ldr r0, DAT_080d5118                     @ 080d50f4 0848
    adds r4,r4,r0    @ 080d50f6 2418
LAB_080d50f8:
    movs r0,#0xe4    @ 080d50f8 e420
    lsls r0,r0,#0x1    @ 080d50fa 4000
    movs r1,#0xe    @ 080d50fc 0e21
    adds r2,r4,#0x0    @ 080d50fe 221c
    bl init_pack_card_slot_aob_from_ptn      @ 080d5100 07f0d6f9
    adds r4,#0x14    @ 080d5104 1434
    adds r5,#0x1    @ 080d5106 0135
    cmp r5,#0x0                              @ 080d5108 002d
    beq LAB_080d50f8                         @ 080d510a f5d0
    pop {r4,r5}                              @ 080d510c 30bc
    pop {r0}                                 @ 080d510e 01bc
    bx r0                                    @ 080d5110 0047
    .zero  0x2
DAT_080d5114:
    .word  pack_ui_state                  @ 080d5114 50580003
DAT_080d5118:
    .word  0x0000070c                     @ 080d5118 0c070000

@ Pack label string render dispatch function; selects render_pack_label_str*_to_bg_vram based on r1=category [0..4] and r0=alt_mode [0..2]. Caller passes pack category index and display mode; function first adjusts base offset (r0==2: 0x28d - 0xd = 0x280), then uses r1 as jump table index (0..4 valid, else default) to dispatch to one of 6 render functions.
@ 
@ Constants:
@ - BASE_OFFSET = 0x28d (r0!=2)
@ - ALT_OFFSET = 0x280 (r0==2, subs r2,#0xd)
@ - MAX_CATEGORY = 4 (cmp r1,#4; bhi -> default)
dispatch_pack_label_text_render_by_category:
    push {lr}                                @ 080d511c 00b5
    ldr r2, DAT_080d5134                     @ 080d511e 054a
    cmp r0,#0x2                              @ 080d5120 0228
    bne LAB_080d5126                         @ 080d5122 00d1
    subs r2,#0xd    @ 080d5124 0d3a
LAB_080d5126:
    cmp r1,#0x4                              @ 080d5126 0429
    bhi switchD_080d5132__default            @ 080d5128 26d8
    lsls r0,r1,#0x2    @ 080d512a 8800
    ldr r1, PTR_switchdataD_080d513c_080d5138 @ 080d512c 0249
    adds r0,r0,r1    @ 080d512e 4018
    ldr r0,[r0,#0x0]                         @ 080d5130 0068
switchD_080d5132__switchD:
    .hword 0x4687    @ 080d5132 8746
DAT_080d5134:
    .word  0x0000028d                     @ 080d5134 8d020000
PTR_switchdataD_080d513c_080d5138:
    .word  0x080d513c                     @ 080d5138 3c510d08
switchD_080d5132__switchdataD_080d513c:
    .word  0x080d5150                     @ 080d513c 50510d08
    .word  0x080d5158                     @ 080d5140 58510d08
    .word  0x080d5168                     @ 080d5144 68510d08
    .word  0x080d5160                     @ 080d5148 60510d08
    .word  0x080d5170                     @ 080d514c 70510d08
switchD_080d5132__caseD_0:
    adds r0,r2,#0x0    @ 080d5150 101c
    bl render_pack_label_str13fa_to_bg_vram  @ 080d5152 07f015fc
    b LAB_080d517e                           @ 080d5156 12e0
switchD_080d5132__caseD_1:
    adds r0,r2,#0x0    @ 080d5158 101c
    bl render_pack_label_str13fb_to_bg_vram  @ 080d515a 07f03dfc
    b LAB_080d517e                           @ 080d515e 0ee0
switchD_080d5132__caseD_3:
    adds r0,r2,#0x0    @ 080d5160 101c
    bl render_pack_label_str1390_to_bg_vram  @ 080d5162 07f0e1fb
    b LAB_080d517e                           @ 080d5166 0ae0
switchD_080d5132__caseD_2:
    adds r0,r2,#0x0    @ 080d5168 101c
    bl render_pack_label_str7ee_to_bg_vram   @ 080d516a 07f061fc
    b LAB_080d517e                           @ 080d516e 06e0
switchD_080d5132__caseD_4:
    adds r0,r2,#0x0    @ 080d5170 101c
    bl render_pack_label_str7ef_to_bg_vram   @ 080d5172 07f089fc
    b LAB_080d517e                           @ 080d5176 02e0
switchD_080d5132__default:
    adds r0,r2,#0x0    @ 080d5178 101c
    bl render_pack_label_default_to_bg_vram  @ 080d517a 07f09dfb
LAB_080d517e:
    pop {r0}                                 @ 080d517e 01bc
    bx r0                                    @ 080d5180 0047
    .zero  0x2

@ pack card shop per-frame OAM sprite renderer for a specified card slot. r0 is the card slot/card parameter (saved to r9). Reads current frame position and count fields from pack_ui_state+0xc scroll state struct, determines visible OAM entry range, loops calling write_oam_entry_with_tile_inc to write up to 4 OAM entries to OAM shadow 0x000080c0. Internally uses r8=pack_ui_state+0xc, r9=r0 (card slot param).
@ 
@ Constants:
@ - pack_ui_state = 0x03005850
@ - SCROLL_STRUCT_OFFSET = 0xc (scroll state substruct base offset)
@ - +0xa: visible_count
@ - +0x1a: scroll/frame state field
@ - +0x3a: scroll_x_delta, +0x3c: scroll_y_delta
@ - +0x3e: frame_flag, +0x40: display state field
@ - OAM_BASE = 0x000080c0 (pack OAM shadow base)
render_pack_card_slot_oam:
    push {r4,r5,r6,r7,lr}                    @ 080d5184 f0b5
    .hword 0x464f    @ 080d5186 4f46
    .hword 0x4646    @ 080d5188 4646
    push {r6,r7}                             @ 080d518a c0b4
    .hword 0x4681    @ 080d518c 8146
    ldr r0, DAT_080d51a8                     @ 080d518e 0648
    adds r0,#0xc    @ 080d5190 0c30
    .hword 0x4680    @ 080d5192 8046
    ldrh r1,[r0,#0xa]                        @ 080d5194 4189
    subs r1,#0x1    @ 080d5196 0139
    ldrh r0,[r0,#0x1a]                       @ 080d5198 408b
    cmp r0,#0x0                              @ 080d519a 0028
    beq LAB_080d51ac                         @ 080d519c 06d0
    .hword 0x4640    @ 080d519e 4046
    ldrh r0,[r0,#0x1a]                       @ 080d51a0 408b
    cmp r0,r1                                @ 080d51a2 8842
    blt LAB_080d51b0                         @ 080d51a4 04db
    b LAB_080d51c0                           @ 080d51a6 0be0
DAT_080d51a8:
    .word  pack_ui_state                  @ 080d51a8 50580003
LAB_080d51ac:
    cmp r1,#0x0                              @ 080d51ac 0029
    ble LAB_080d51c0                         @ 080d51ae 07dd
LAB_080d51b0:
    .hword 0x4641    @ 080d51b0 4146
    ldrh r0,[r1,#0x1a]                       @ 080d51b2 488b
    movs r2,#0x0    @ 080d51b4 0022
    ldrh r3,[r1,#0xa]                        @ 080d51b6 4b89
    cmp r0,#0x0                              @ 080d51b8 0028
    beq LAB_080d51c8                         @ 080d51ba 05d0
    adds r2,r0,#0x0    @ 080d51bc 021c
    b LAB_080d51c8                           @ 080d51be 03e0
LAB_080d51c0:
    .hword 0x4642    @ 080d51c0 4246
    ldrh r0,[r2,#0xa]                        @ 080d51c2 5089
    subs r2,r0,#0x1    @ 080d51c4 421e
    adds r3,r0,#0x0    @ 080d51c6 031c
LAB_080d51c8:
    .hword 0x4640    @ 080d51c8 4046
    adds r0,#0x40    @ 080d51ca 4030
    movs r4,#0x0    @ 080d51cc 0024
    ldrsh r0,[r0,r4]                         @ 080d51ce 005f
    cmp r0,#0x0                              @ 080d51d0 0028
    beq LAB_080d51e8                         @ 080d51d2 09d0
    .hword 0x4645    @ 080d51d4 4546
    movs r6,#0x3a    @ 080d51d6 3a26
    ldrsh r1,[r5,r6]                         @ 080d51d8 a95f
    movs r4,#0x3c    @ 080d51da 3c24
    ldrsh r0,[r5,r4]                         @ 080d51dc 285f
    subs r4,r2,#0x1    @ 080d51de 541e
    cmp r1,r0                                @ 080d51e0 8142
    bge LAB_080d51ea                         @ 080d51e2 02da
    subs r4,r2,#0x2    @ 080d51e4 941e
    b LAB_080d51ea                           @ 080d51e6 00e0
LAB_080d51e8:
    subs r4,r2,#0x1    @ 080d51e8 541e
LAB_080d51ea:
    adds r1,r4,#0x1    @ 080d51ea 611c
    movs r0,#0x3    @ 080d51ec 0320
    ands r0,r1    @ 080d51ee 0840
    lsls r2,r0,#0x3    @ 080d51f0 c200
    lsls r1,r1,#0x6    @ 080d51f2 8901
    adds r1,#0x10    @ 080d51f4 1031
    .hword 0x4645    @ 080d51f6 4546
    movs r6,#0x3e    @ 080d51f8 3e26
    ldrsh r0,[r5,r6]                         @ 080d51fa a85f
    subs r7,r1,r0    @ 080d51fc 0f1a
    movs r0,#0xff    @ 080d51fe ff20
    ands r7,r0    @ 080d5200 0740
    movs r6,#0x0    @ 080d5202 0026
    cmp r4,r3                                @ 080d5204 9c42
    bge LAB_080d5252                         @ 080d5206 24da
    adds r5,r2,#0x0    @ 080d5208 151c
LAB_080d520a:
    cmp r4,#0x0                              @ 080d520a 002c
    blt LAB_080d5240                         @ 080d520c 18db
    movs r3,#0x1f    @ 080d520e 1f23
    ands r3,r5    @ 080d5210 2b40
    movs r2,#0x4    @ 080d5212 0422
    lsls r0,r6,#0x6    @ 080d5214 b001
    adds r1,r7,#0x0    @ 080d5216 391c
    subs r1,#0x10    @ 080d5218 1039
    adds r0,r0,r1    @ 080d521a 4018
    lsls r0,r0,#0x10    @ 080d521c 0004
    lsrs r0,r0,#0x10    @ 080d521e 000c
    .hword 0x4649    @ 080d5220 4946
    cmp r1,#0x3                              @ 080d5222 0329
    bls LAB_080d522a                         @ 080d5224 01d9
    movs r1,#0x3    @ 080d5226 0321
    .hword 0x4689    @ 080d5228 8946
LAB_080d522a:
    lsls r0,r0,#0x10    @ 080d522a 0004
    orrs r0,r2    @ 080d522c 1043
    .hword 0x4649    @ 080d522e 4946
    lsls r2,r1,#0xa    @ 080d5230 8a02
    lsrs r1,r3,#0x1    @ 080d5232 5908
    orrs r2,r1    @ 080d5234 0a43
    lsls r2,r2,#0x10    @ 080d5236 1204
    lsrs r2,r2,#0x10    @ 080d5238 120c
    ldr r1, DAT_080d5260                     @ 080d523a 0949
    bl write_oam_entry_with_tile_inc         @ 080d523c 21f008f9
LAB_080d5240:
    adds r4,#0x1    @ 080d5240 0134
    adds r5,#0x8    @ 080d5242 0835
    adds r6,#0x1    @ 080d5244 0136
    cmp r6,#0x3                              @ 080d5246 032e
    bgt LAB_080d5252                         @ 080d5248 03dc
    .hword 0x4642    @ 080d524a 4246
    ldrh r2,[r2,#0xa]                        @ 080d524c 5289
    cmp r4,r2                                @ 080d524e 9442
    blt LAB_080d520a                         @ 080d5250 dbdb
LAB_080d5252:
    pop {r3,r4}                              @ 080d5252 18bc
    .hword 0x4698    @ 080d5254 9846
    .hword 0x46a1    @ 080d5256 a146
    pop {r4,r5,r6,r7}                        @ 080d5258 f0bc
    pop {r0}                                 @ 080d525a 01bc
    bx r0                                    @ 080d525c 0047
    .zero  0x2
DAT_080d5260:
    .word  0x000080c0                     @ 080d5260 c0800000

@ Writes a pack card OAM sprite entry into OBJ VRAM shadow. r0=slot_linear, r1=pack_banner_ptr, r2=sprite_type [0..3]. Computes OBJ VRAM dest from slot row/col, adds 0x100 tile offset. Based on pack_banner_ptr equality test selects write_pack_obj_attr_by_dir_tall_diag or write_oam_entry_with_tile_inc; writes two OAM entries. Called by FUN_080d5f38 (pack frame driver).
@ 
@ Constants:
@ - OBJ_VRAM_TILE_OFFSET = 0x100 (movs r1,#0x80; lsls r1,r1,#0x1 -> 0x80<<1 = 0x100 tile base offset)
@ - SPRITE_TYPE_MAX = 3 (cmp r4,#3; bls -> clamp)
@ - OAM_ATTR_E0 = 0x380000 (movs r0,#0xe0; lsls r0,r0,#0xe -> 0xe0<<14 = 0x380000; python: 0xe0<<0xe == 0x380000)
@ - OAM_ATTR_B0 = 0x580000 (movs r0,#0xb0; lsls r0,r0,#0xf -> 0xb0<<15 = 0x580000; python: 0xb0<<0xf == 0x580000)
@ 
@ Inputs: r0=u32 slot_linear; r1=ptr pack_banner_ptr; r2=u32 sprite_type [0..3]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OAM shadow via write_pack_obj_attr_by_dir_tall_diag or write_oam_entry_with_tile_inc] writes OAM attr0/attr1/attr2
write_pack_obj_card_entry:
    push {r4,r5,r6,r7,lr}                    @ 080d5264 f0b5
    adds r3,r0,#0x0    @ 080d5266 031c
    adds r5,r1,#0x0    @ 080d5268 0d1c
    adds r4,r2,#0x0    @ 080d526a 141c
    movs r2,#0x3    @ 080d526c 0322
    ands r2,r3    @ 080d526e 1a40
    lsls r2,r2,#0x3    @ 080d5270 d200
    lsrs r1,r3,#0x2    @ 080d5272 9908
    lsls r0,r1,#0x1    @ 080d5274 4800
    adds r0,r0,r1    @ 080d5276 4018
    lsls r0,r0,#0x6    @ 080d5278 8001
    movs r1,#0x80    @ 080d527a 8021
    lsls r1,r1,#0x1    @ 080d527c 4900
    adds r0,r0,r1    @ 080d527e 4018
    adds r7,r2,r0    @ 080d5280 1718
    cmp r4,#0x3                              @ 080d5282 032c
    bls LAB_080d5288                         @ 080d5284 00d9
    movs r4,#0x3    @ 080d5286 0324
LAB_080d5288:
    cmp r5,#0x0                              @ 080d5288 002d
    beq LAB_080d5312                         @ 080d528a 42d0
    lsls r0,r3,#0x2    @ 080d528c 9800
    adds r0,r0,r3    @ 080d528e c018
    adds r0,#0x5    @ 080d5290 0530
    cmp r5,r1                                @ 080d5292 8d42
    beq LAB_080d52dc                         @ 080d5294 22d0
    lsls r6,r0,#0x13    @ 080d5296 c604
    lsrs r6,r6,#0x10    @ 080d5298 360c
    movs r0,#0xe0    @ 080d529a e020
    lsls r0,r0,#0xe    @ 080d529c 8003
    orrs r0,r6    @ 080d529e 3043
    lsls r4,r4,#0xa    @ 080d52a0 a402
    lsrs r2,r7,#0x1    @ 080d52a2 7a08
    orrs r2,r4    @ 080d52a4 2243
    lsls r2,r2,#0x10    @ 080d52a6 1204
    lsrs r2,r2,#0x10    @ 080d52a8 120c
    lsls r5,r5,#0x10    @ 080d52aa 2d04
    lsrs r5,r5,#0x10    @ 080d52ac 2d0c
    movs r1,#0x80    @ 080d52ae 8021
    lsls r1,r1,#0x11    @ 080d52b0 4904
    orrs r5,r1    @ 080d52b2 0d43
    movs r1,#0x80    @ 080d52b4 8021
    adds r3,r5,#0x0    @ 080d52b6 2b1c
    bl write_pack_obj_attr_by_dir_tall_diag  @ 080d52b8 21f006fe
    movs r0,#0xb0    @ 080d52bc b020
    lsls r0,r0,#0xf    @ 080d52be c003
    orrs r0,r6    @ 080d52c0 3043
    movs r1,#0x81    @ 080d52c2 8121
    lsls r1,r1,#0x7    @ 080d52c4 c901
    adds r2,r7,#0x0    @ 080d52c6 3a1c
    adds r2,#0x80    @ 080d52c8 8032
    lsrs r2,r2,#0x1    @ 080d52ca 5208
    orrs r4,r2    @ 080d52cc 1443
    lsls r4,r4,#0x10    @ 080d52ce 2404
    lsrs r4,r4,#0x10    @ 080d52d0 240c
    adds r2,r4,#0x0    @ 080d52d2 221c
    adds r3,r5,#0x0    @ 080d52d4 2b1c
    bl write_pack_obj_attr_by_dir_tall_diag  @ 080d52d6 21f0f7fd
    b LAB_080d5312                           @ 080d52da 1ae0
LAB_080d52dc:
    lsls r5,r0,#0x13    @ 080d52dc c504
    lsrs r5,r5,#0x10    @ 080d52de 2d0c
    movs r0,#0xe0    @ 080d52e0 e020
    lsls r0,r0,#0xe    @ 080d52e2 8003
    orrs r0,r5    @ 080d52e4 2843
    lsls r4,r4,#0xa    @ 080d52e6 a402
    lsrs r2,r7,#0x1    @ 080d52e8 7a08
    orrs r2,r4    @ 080d52ea 2243
    lsls r2,r2,#0x10    @ 080d52ec 1204
    lsrs r2,r2,#0x10    @ 080d52ee 120c
    movs r1,#0x80    @ 080d52f0 8021
    bl write_oam_entry_with_tile_inc         @ 080d52f2 21f0adf8
    movs r0,#0xb0    @ 080d52f6 b020
    lsls r0,r0,#0xf    @ 080d52f8 c003
    orrs r0,r5    @ 080d52fa 2843
    movs r1,#0x81    @ 080d52fc 8121
    lsls r1,r1,#0x7    @ 080d52fe c901
    adds r2,r7,#0x0    @ 080d5300 3a1c
    adds r2,#0x80    @ 080d5302 8032
    lsrs r2,r2,#0x1    @ 080d5304 5208
    orrs r4,r2    @ 080d5306 1443
    lsls r4,r4,#0x10    @ 080d5308 2404
    lsrs r4,r4,#0x10    @ 080d530a 240c
    adds r2,r4,#0x0    @ 080d530c 221c
    bl write_oam_entry_with_tile_inc         @ 080d530e 21f09ff8
LAB_080d5312:
    pop {r4,r5,r6,r7}                        @ 080d5312 f0bc
    pop {r0}                                 @ 080d5314 01bc
    bx r0                                    @ 080d5316 0047

@ Thin wrapper: loads pack_ui_state+0x70c as state_base and calls dispatch_pack_card_aob_by_type(aob_data_ptr, state_base). Entry saves r1->r0; loads pack_ui_state (DAT_080d532c) plus AOB_STATE_OFFSET 0x70c (DAT_080d5330) as state_base parameter. Automatically injects state_base. Called by pack scene tick/init functions.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d532c)
@ - AOB_STATE_OFFSET = 0x70c (DAT_080d5330)
@ 
@ Inputs: r0=ptr aob_data_ptr; r1=u32 type_code
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: passes through side effects of dispatch_pack_card_aob_by_type (AOB state update)
dispatch_pack_aob_by_type_with_state_base:
    push {lr}                                @ 080d5318 00b5
    adds r0,r1,#0x0    @ 080d531a 081c
    ldr r1, DAT_080d532c                     @ 080d531c 0349
    ldr r2, DAT_080d5330                     @ 080d531e 044a
    adds r1,r1,r2    @ 080d5320 8918
    bl dispatch_pack_card_aob_by_type        @ 080d5322 07f0b3f8
    pop {r0}                                 @ 080d5326 01bc
    bx r0                                    @ 080d5328 0047
    .zero  0x2
DAT_080d532c:
    .word  pack_ui_state                  @ 080d532c 50580003
DAT_080d5330:
    .word  0x0000070c                     @ 080d5330 0c070000

@ Thin wrapper: advances one pack card AOB animation frame. r0=slot_linear, r1=frame_type [0..3]. Computes tile_id from slot_linear (slot*5+5, extract bits), ORs with OAM upper attr 0x380000. Loads pack_ui_state+0x70c as aob_state_base. Calls tick_pack_card_aob_frame(tile_attr, aob_state_base, frame_type). Automatically injects state_base and converts slot->tile param.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d5364)
@ - AOB_STATE_OFFSET = 0x70c (DAT_080d5368)
@ - OAM_UPPER_ATTR = 0x380000 (movs r1,#0xe0; lsls r1,r1,#0xe -> 0xe0<<14 = 0x380000; python: 0xe0<<0xe == 0x380000)
@ - FRAME_TYPE_MAX = 3 (cmp r3,#3; bls -> clamp)
@ 
@ Inputs: r0=u32 slot_linear [0..?]; r1=u32 frame_type [0..3]
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: passes through tick_pack_card_aob_frame side effects (AOB frame counter/pattern update)
tick_pack_aob_frame_with_state_base:
    push {r4,lr}                             @ 080d5334 10b5
    adds r2,r0,#0x0    @ 080d5336 021c
    adds r3,r1,#0x0    @ 080d5338 0b1c
    ldr r4, DAT_080d5364                     @ 080d533a 0a4c
    cmp r3,#0x3                              @ 080d533c 032b
    bls LAB_080d5342                         @ 080d533e 00d9
    movs r3,#0x3    @ 080d5340 0323
LAB_080d5342:
    lsls r0,r2,#0x2    @ 080d5342 9000
    adds r0,r0,r2    @ 080d5344 8018
    adds r0,#0x5    @ 080d5346 0530
    lsls r0,r0,#0x13    @ 080d5348 c004
    lsrs r0,r0,#0x10    @ 080d534a 000c
    movs r1,#0xe0    @ 080d534c e021
    lsls r1,r1,#0xe    @ 080d534e 8903
    orrs r0,r1    @ 080d5350 0843
    ldr r1, DAT_080d5368                     @ 080d5352 0549
    adds r2,r4,r1    @ 080d5354 6218
    adds r1,r3,#0x0    @ 080d5356 191c
    bl tick_pack_card_aob_frame              @ 080d5358 07f0ecf8
    pop {r4}                                 @ 080d535c 10bc
    pop {r0}                                 @ 080d535e 01bc
    bx r0                                    @ 080d5360 0047
    .zero  0x2
DAT_080d5364:
    .word  pack_ui_state                  @ 080d5364 50580003
DAT_080d5368:
    .word  0x0000070c                     @ 080d5368 0c070000

@ Called each frame by pack scene state machines to drive the AOB (animation-object-block) animation frame update loop for the current pack card display row. Iterates up to (r7 offset +0x1 low 4 bits) AOB slots; for each active slot calls dispatch_pack_aob_by_type_with_state_base to set the animation type base address, then calls tick_pack_aob_frame_with_state_base to advance the frame counter. Before the frame loop, computes a BLDALPHA brightness blend value linearly from the elapsed frame counter (pack_ui_state[+0x6f0]); if the frame counter exceeds 0x48 the blend is written at full brightness (0x1000), otherwise bios_div computes the current alpha and writes it to the BLDALPHA register.
@ 
@ Constants:
@ - AOB_COUNT_MASK = 0xf (r7[+0x1] low 4 bits, AOB slot count)
@ - AOB_SLOT_STRIDE = 0x4 (4 bytes per slot, r5 step)
@ - FRAME_COUNT_OFFSET = 0xe4<<3 = 0x720 (pack_ui_state[+0x720] frame counter)
@ - FRAME_FADE_END = 0x48 (frame count upper bound; above this BLDALPHA is fixed full)
@ - FRAME_FADE_TOTAL = 0x48 (lsls #4 = 0x480 numerator for linear interpolation)
@ - BLDALPHA_FULL = 0x1000 (movs r3,#0x80; lsls r3,#5 = 0x1000)
@ - BLDALPHA_MASK = 0xff (lsls #0x18; lsrs #0x18 keeps low 8 bits eva)
@ - pack_ui_state[+0x714] = named AOB state offset base
@ - pack_ui_state[+0xc] = scroll position reference offset
tick_pack_aob_frame_loop:
    push {r4,r5,r6,r7,lr}                    @ 080d536c f0b5
    .hword 0x4647    @ 080d536e 4746
    push {r7}                                @ 080d5370 80b4
    adds r7,r0,#0x0    @ 080d5372 071c
    adds r5,r1,#0x0    @ 080d5374 0d1c
    adds r6,r2,#0x0    @ 080d5376 161c
    ldr r0, DAT_080d53c0                     @ 080d5378 1148
    movs r1,#0xc    @ 080d537a 0c21
    adds r1,r1,r0    @ 080d537c 0918
    .hword 0x4688    @ 080d537e 8846
    cmp r6,#0x3                              @ 080d5380 032e
    bls LAB_080d5386                         @ 080d5382 00d9
    movs r6,#0x3    @ 080d5384 0326
LAB_080d5386:
    movs r2,#0xe4    @ 080d5386 e422
    lsls r2,r2,#0x3    @ 080d5388 d200
    adds r1,r0,r2    @ 080d538a 8118
    ldr r0,[r1,#0x0]                         @ 080d538c 0868
    adds r0,#0x1    @ 080d538e 0130
    str r0,[r1,#0x0]                         @ 080d5390 0860
    cmp r0,#0x8f                             @ 080d5392 8f28
    ble LAB_080d539a                         @ 080d5394 01dd
    movs r0,#0x0    @ 080d5396 0020
    str r0,[r1,#0x0]                         @ 080d5398 0860
LAB_080d539a:
    ldr r1,[r1,#0x0]                         @ 080d539a 0968
    cmp r1,#0x48                             @ 080d539c 4829
    bgt LAB_080d53c8                         @ 080d539e 13dc
    movs r0,#0x48    @ 080d53a0 4820
    subs r0,r0,r1    @ 080d53a2 401a
    lsls r0,r0,#0x4    @ 080d53a4 0001
    movs r1,#0x48    @ 080d53a6 4821
    bl bios_div                              @ 080d53a8 39f028f8
    ldr r2, PTR_BLDALPHA_080d53c4            @ 080d53ac 054a
    lsls r0,r0,#0x18    @ 080d53ae 0006
    lsrs r0,r0,#0x18    @ 080d53b0 000e
    movs r3,#0x80    @ 080d53b2 8023
    lsls r3,r3,#0x5    @ 080d53b4 5b01
    adds r1,r3,#0x0    @ 080d53b6 191c
    orrs r0,r1    @ 080d53b8 0843
    strh r0,[r2,#0x0]                        @ 080d53ba 1080
    b LAB_080d53d2                           @ 080d53bc 09e0
    .zero  0x2
DAT_080d53c0:
    .word  pack_ui_state                  @ 080d53c0 50580003
PTR_BLDALPHA_080d53c4:
    .word  BLDALPHA                       @ 080d53c4 52000004
LAB_080d53c8:
    ldr r1, PTR_BLDALPHA_080d5420            @ 080d53c8 1549
    movs r2,#0x80    @ 080d53ca 8022
    lsls r2,r2,#0x5    @ 080d53cc 5201
    adds r0,r2,#0x0    @ 080d53ce 101c
    strh r0,[r1,#0x0]                        @ 080d53d0 0880
LAB_080d53d2:
    movs r4,#0x0    @ 080d53d2 0024
    movs r0,#0xf    @ 080d53d4 0f20
    ldrb r3,[r7,#0x1]                        @ 080d53d6 7b78
    ands r0,r3    @ 080d53d8 1840
    cmp r4,r0                                @ 080d53da 8442
    bge LAB_080d5414                         @ 080d53dc 1ada
LAB_080d53de:
    movs r0,#0x7    @ 080d53de 0720
    ldrb r1,[r5,#0x0]                        @ 080d53e0 2978
    ands r0,r1    @ 080d53e2 0840
    cmp r0,#0x0                              @ 080d53e4 0028
    beq LAB_080d5406                         @ 080d53e6 0ed0
    ldr r0, DAT_080d5424                     @ 080d53e8 0e48
    add r0,r8                                @ 080d53ea 4044
    ldr r0,[r0,#0x0]                         @ 080d53ec 0068
    cmp r0,#0x0                              @ 080d53ee 0028
    bne LAB_080d53fe                         @ 080d53f0 05d1
    ldr r1,[r5,#0x0]                         @ 080d53f2 2968
    lsls r1,r1,#0x1d    @ 080d53f4 4907
    lsrs r1,r1,#0x1d    @ 080d53f6 490f
    adds r0,r4,#0x0    @ 080d53f8 201c
    bl dispatch_pack_aob_by_type_with_state_base @ 080d53fa fff78dff
LAB_080d53fe:
    adds r0,r4,#0x0    @ 080d53fe 201c
    adds r1,r6,#0x0    @ 080d5400 311c
    bl tick_pack_aob_frame_with_state_base   @ 080d5402 fff797ff
LAB_080d5406:
    adds r5,#0x4    @ 080d5406 0435
    adds r4,#0x1    @ 080d5408 0134
    movs r0,#0xf    @ 080d540a 0f20
    ldrb r2,[r7,#0x1]                        @ 080d540c 7a78
    ands r0,r2    @ 080d540e 1040
    cmp r4,r0                                @ 080d5410 8442
    blt LAB_080d53de                         @ 080d5412 e4db
LAB_080d5414:
    pop {r3}                                 @ 080d5414 08bc
    .hword 0x4698    @ 080d5416 9846
    pop {r4,r5,r6,r7}                        @ 080d5418 f0bc
    pop {r0}                                 @ 080d541a 01bc
    bx r0                                    @ 080d541c 0047
    .zero  0x2
PTR_BLDALPHA_080d5420:
    .word  BLDALPHA                       @ 080d5420 52000004
DAT_080d5424:
    .word  0x00000714                     @ 080d5424 14070000

@ Called by the pack scene state machine when the AOB animation frame loop needs to be reset. First clears pack_ui_state[+0x720] (frame counter) to zero to restart the fade-in animation; then iterates over (r0 offset +0x1 low 4 bits) AOB slots, calling dispatch_pack_aob_by_type_with_state_base for each active slot (bit[2:0] != 0) to set its animation type base address. Differs from tick_pack_aob_frame_loop: this function does not call tick_pack_aob_frame_with_state_base (does not advance frames) and clears the frame counter before iterating.
@ 
@ Constants:
@ - AOB_COUNT_MASK = 0xf (r0[+0x1] low 4 bits)
@ - AOB_SLOT_STRIDE = 0x4 (4 bytes per slot)
@ - FRAME_COUNT_OFFSET = 0xe4<<3 = 0x720 (pack_ui_state[+0x720])
@ - pack_ui_state base = 0x03005850
dispatch_pack_aob_frame_loop_by_reset:
    push {r4,r5,r6,lr}                       @ 080d5428 70b5
    adds r6,r0,#0x0    @ 080d542a 061c
    adds r4,r1,#0x0    @ 080d542c 0c1c
    ldr r0, DAT_080d5440                     @ 080d542e 0448
    movs r1,#0xe4    @ 080d5430 e421
    lsls r1,r1,#0x3    @ 080d5432 c900
    adds r0,r0,r1    @ 080d5434 4018
    movs r1,#0x0    @ 080d5436 0021
    str r1,[r0,#0x0]                         @ 080d5438 0160
    movs r5,#0x0    @ 080d543a 0025
    b LAB_080d545e                           @ 080d543c 0fe0
    .zero  0x2
DAT_080d5440:
    .word  pack_ui_state                  @ 080d5440 50580003
LAB_080d5444:
    movs r0,#0x7    @ 080d5444 0720
    ldrb r1,[r4,#0x0]                        @ 080d5446 2178
    ands r0,r1    @ 080d5448 0840
    cmp r0,#0x0                              @ 080d544a 0028
    beq LAB_080d545a                         @ 080d544c 05d0
    ldr r1,[r4,#0x0]                         @ 080d544e 2168
    lsls r1,r1,#0x1d    @ 080d5450 4907
    lsrs r1,r1,#0x1d    @ 080d5452 490f
    adds r0,r5,#0x0    @ 080d5454 281c
    bl dispatch_pack_aob_by_type_with_state_base @ 080d5456 fff75fff
LAB_080d545a:
    adds r4,#0x4    @ 080d545a 0434
    adds r5,#0x1    @ 080d545c 0135
LAB_080d545e:
    movs r0,#0xf    @ 080d545e 0f20
    ldrb r1,[r6,#0x1]                        @ 080d5460 7178
    ands r0,r1    @ 080d5462 0840
    cmp r5,r0                                @ 080d5464 8542
    bcc LAB_080d5444                         @ 080d5466 edd3
    pop {r4,r5,r6}                           @ 080d5468 70bc
    pop {r0}                                 @ 080d546a 01bc
    bx r0                                    @ 080d546c 0047
    .zero  0x2

@ 拆包场景卡牌旋转/缩放精灵的 OAM 渲染, 由多个拆包动画状态调用 (indeg=9). r0 选模式 (上限钳到 3), r1 为辅助参数. 读取 pack_ui_state+0xc 工作结构, 用 get_bios_div_remainder 与 bios_div 基于循环计数 [+0x22] (0..0x1d) 计算正弦式仿射缩放系数 (0x100 减插值量), 计数前 15 帧放大, 后段缩小. 随后调 rotate_pixel_hue_in_buffer 旋转色相, write_pack_obj_attr_by_dir_split 与 render_overlay_oam_sprite_tiled 写出卡牌旋转精灵 (上下两半).
render_pack_card_spin_oam_by_mode:
    push {r4,r5,r6,r7,lr}                    @ 080d5470 f0b5
    .hword 0x4657    @ 080d5472 5746
    .hword 0x464e    @ 080d5474 4e46
    .hword 0x4645    @ 080d5476 4546
    push {r5,r6,r7}                          @ 080d5478 e0b4
    sub sp,#0x4                              @ 080d547a 81b0
    str r0,[sp,#0x0]                         @ 080d547c 0090
    .hword 0x4689    @ 080d547e 8946
    ldr r4, DAT_080d54ec                     @ 080d5480 1a4c
    adds r6,r4,#0x0    @ 080d5482 261c
    adds r6,#0xc    @ 080d5484 0c36
    ldr r0, DAT_080d54f0                     @ 080d5486 1a48
    adds r2,r4,r0    @ 080d5488 2218
    ldr r1, DAT_080d54f4                     @ 080d548a 1a49
    adds r0,r4,r1    @ 080d548c 6018
    ldrh r0,[r0,#0x0]                        @ 080d548e 0088
    lsls r1,r0,#0x2    @ 080d5490 8100
    ldr r0,[r2,#0x0]                         @ 080d5492 1068
    adds r0,r0,r1    @ 080d5494 4018
    .hword 0x4682    @ 080d5496 8246
    ldrh r0,[r6,#0x18]                       @ 080d5498 308b
    movs r1,#0x5    @ 080d549a 0521
    bl get_bios_div_remainder                @ 080d549c 38f0b0ff
    ldr r2, DAT_080d54f8                     @ 080d54a0 154a
    adds r4,r4,r2    @ 080d54a2 a418
    ldrh r1,[r6,#0x18]                       @ 080d54a4 318b
    lsls r2,r1,#0x2    @ 080d54a6 8a00
    ldr r1,[r4,#0x0]                         @ 080d54a8 2168
    adds r1,r1,r2    @ 080d54aa 8918
    lsls r0,r0,#0x2    @ 080d54ac 8000
    subs r7,r1,r0    @ 080d54ae 0f1a
    ldr r2,[sp,#0x0]                         @ 080d54b0 009a
    cmp r2,#0x3                              @ 080d54b2 032a
    bls LAB_080d54ba                         @ 080d54b4 01d9
    movs r0,#0x3    @ 080d54b6 0320
    str r0,[sp,#0x0]                         @ 080d54b8 0090
LAB_080d54ba:
    ldrh r0,[r6,#0x22]                       @ 080d54ba 708c
    adds r0,#0x1    @ 080d54bc 0130
    strh r0,[r6,#0x22]                       @ 080d54be 7084
    lsls r0,r0,#0x10    @ 080d54c0 0004
    lsrs r0,r0,#0x10    @ 080d54c2 000c
    cmp r0,#0x1d                             @ 080d54c4 1d28
    bls LAB_080d54cc                         @ 080d54c6 01d9
    movs r0,#0x0    @ 080d54c8 0020
    strh r0,[r6,#0x22]                       @ 080d54ca 7084
LAB_080d54cc:
    ldrh r1,[r6,#0x22]                       @ 080d54cc 718c
    cmp r1,#0xe                              @ 080d54ce 0e29
    bhi LAB_080d54fc                         @ 080d54d0 14d8
    lsls r0,r1,#0x6    @ 080d54d2 8801
    movs r1,#0xf    @ 080d54d4 0f21
    bl bios_div                              @ 080d54d6 38f091ff
    movs r2,#0x80    @ 080d54da 8022
    lsls r2,r2,#0x1    @ 080d54dc 5200
    adds r1,r2,#0x0    @ 080d54de 111c
    subs r1,r1,r0    @ 080d54e0 091a
    lsls r1,r1,#0x10    @ 080d54e2 0904
    lsrs r1,r1,#0x10    @ 080d54e4 090c
    .hword 0x4688    @ 080d54e6 8846
    b LAB_080d5510                           @ 080d54e8 12e0
    .zero  0x2
DAT_080d54ec:
    .word  pack_ui_state                  @ 080d54ec 50580003
DAT_080d54f0:
    .word  0x000006fc                     @ 080d54f0 fc060000
DAT_080d54f4:
    .word  0x000006fa                     @ 080d54f4 fa060000
DAT_080d54f8:
    .word  0x00000704                     @ 080d54f8 04070000
LAB_080d54fc:
    ldrh r0,[r6,#0x22]                       @ 080d54fc 708c
    subs r0,#0xf    @ 080d54fe 0f38
    lsls r0,r0,#0x6    @ 080d5500 8001
    movs r1,#0xf    @ 080d5502 0f21
    bl bios_div                              @ 080d5504 38f07aff
    adds r0,#0xc0    @ 080d5508 c030
    lsls r0,r0,#0x10    @ 080d550a 0004
    lsrs r0,r0,#0x10    @ 080d550c 000c
    .hword 0x4680    @ 080d550e 8046
LAB_080d5510:
    ldr r0, DAT_080d55c0                     @ 080d5510 2b48
    ldr r4,[r0,#0x8]                         @ 080d5512 8468
    adds r4,#0x12    @ 080d5514 1234
    ldr r5, DAT_080d55c4                     @ 080d5516 2b4d
    ldrh r0,[r6,#0x22]                       @ 080d5518 708c
    lsls r1,r0,#0x1    @ 080d551a 4100
    adds r1,r1,r0    @ 080d551c 0918
    lsls r0,r1,#0x4    @ 080d551e 0801
    subs r0,r0,r1    @ 080d5520 401a
    lsls r0,r0,#0x3    @ 080d5522 c000
    movs r1,#0x1e    @ 080d5524 1e21
    bl bios_div                              @ 080d5526 38f069ff
    adds r2,r0,#0x0    @ 080d552a 021c
    rsbs r2,r2,#0    @ 080d552c 5242
    lsls r2,r2,#0x10    @ 080d552e 1204
    movs r0,#0x7    @ 080d5530 0720
    orrs r2,r0    @ 080d5532 0243
    adds r0,r4,#0x0    @ 080d5534 201c
    adds r1,r5,#0x0    @ 080d5536 291c
    bl rotate_pixel_hue_in_buffer            @ 080d5538 08f0a8fa
    movs r0,#0x80    @ 080d553c 8020
    .hword 0x4651    @ 080d553e 5146
    ldrb r1,[r1,#0x0]                        @ 080d5540 0978
    ands r0,r1    @ 080d5542 0840
    cmp r0,#0x0                              @ 080d5544 0028
    bne LAB_080d554e                         @ 080d5546 02d1
    .hword 0x464a    @ 080d5548 4a46
    cmp r2,#0x0                              @ 080d554a 002a
    beq LAB_080d55b0                         @ 080d554c 30d0
LAB_080d554e:
    movs r4,#0x0    @ 080d554e 0024
    movs r0,#0xf    @ 080d5550 0f20
    .hword 0x4651    @ 080d5552 5146
    ldrb r1,[r1,#0x1]                        @ 080d5554 4978
    ands r0,r1    @ 080d5556 0840
    cmp r4,r0                                @ 080d5558 8442
    bcs LAB_080d55b0                         @ 080d555a 29d2
    movs r5,#0xa0    @ 080d555c a025
    lsls r5,r5,#0xe    @ 080d555e ad03
    ldr r2,[sp,#0x0]                         @ 080d5560 009a
    lsls r0,r2,#0xa    @ 080d5562 9002
    ldr r2, DAT_080d55c8                     @ 080d5564 184a
    adds r1,r2,#0x0    @ 080d5566 111c
    orrs r0,r1    @ 080d5568 0843
    lsls r6,r0,#0x10    @ 080d556a 0604
LAB_080d556c:
    movs r0,#0x8    @ 080d556c 0820
    ldrb r1,[r7,#0x0]                        @ 080d556e 3978
    ands r0,r1    @ 080d5570 0840
    cmp r0,#0x0                              @ 080d5572 0028
    beq LAB_080d559a                         @ 080d5574 11d0
    cmp r4,r9                                @ 080d5576 4c45
    bcc LAB_080d5580                         @ 080d5578 02d3
    .hword 0x464a    @ 080d557a 4a46
    cmp r2,#0x0                              @ 080d557c 002a
    bne LAB_080d559a                         @ 080d557e 0cd1
LAB_080d5580:
    lsrs r0,r5,#0x10    @ 080d5580 280c
    movs r1,#0xb8    @ 080d5582 b821
    lsls r1,r1,#0xe    @ 080d5584 8903
    orrs r0,r1    @ 080d5586 0843
    .hword 0x4642    @ 080d5588 4246
    lsls r3,r2,#0x10    @ 080d558a 1304
    asrs r3,r3,#0x10    @ 080d558c 1b14
    movs r1,#0x81    @ 080d558e 8121
    lsls r1,r1,#0x7    @ 080d5590 c901
    lsrs r2,r6,#0x10    @ 080d5592 320c
    lsls r3,r3,#0x10    @ 080d5594 1b04
    bl write_pack_obj_attr_by_dir_split      @ 080d5596 21f0a9f9
LAB_080d559a:
    adds r7,#0x4    @ 080d559a 0437
    movs r0,#0xa0    @ 080d559c a020
    lsls r0,r0,#0xe    @ 080d559e 8003
    adds r5,r5,r0    @ 080d55a0 2d18
    adds r4,#0x1    @ 080d55a2 0134
    movs r0,#0xf    @ 080d55a4 0f20
    .hword 0x4651    @ 080d55a6 5146
    ldrb r1,[r1,#0x1]                        @ 080d55a8 4978
    ands r0,r1    @ 080d55aa 0840
    cmp r4,r0                                @ 080d55ac 8442
    bcc LAB_080d556c                         @ 080d55ae ddd3
LAB_080d55b0:
    add sp,#0x4                              @ 080d55b0 01b0
    pop {r3,r4,r5}                           @ 080d55b2 38bc
    .hword 0x4698    @ 080d55b4 9846
    .hword 0x46a1    @ 080d55b6 a146
    .hword 0x46aa    @ 080d55b8 aa46
    pop {r4,r5,r6,r7}                        @ 080d55ba f0bc
    pop {r0}                                 @ 080d55bc 01bc
    bx r0                                    @ 080d55be 0047
DAT_080d55c0:
    .word  0x09ce824c                     @ 080d55c0 4c82ce09
DAT_080d55c4:
    .word  0x05000352                     @ 080d55c4 52030005
DAT_080d55c8:
    .word  0x0000a1d0                     @ 080d55c8 d0a10000

@ Renders two overlay OAM sprites (top and bottom halves) at the pack card highlight position. r0=slot_node_ptr (passed as r3 to render_overlay_oam_sprite_tiled). First call: attr0=0x00900008, oam_params=0x0002000d, tile=0x000b0280. Second call: attr0=0x00900080, tile=0x000b028d. Called frequently by pack scene frame drivers to display the current card selection highlight box.
@ 
@ Constants:
@ - SPRITE_ATTR0_TOP = 0x00900008 (DAT_080d55f0)
@ - OAM_PARAMS = 0x0002000d (DAT_080d55f4)
@ - TILE_DATA_TOP = 0x000b0280 (DAT_080d55f8)
@ - SPRITE_ATTR0_BOT = 0x00900080 (DAT_080d55fc)
@ - TILE_DATA_BOT = 0x000b028d (DAT_080d5600)
@ 
@ Inputs: r0=ptr slot_node_ptr (current selected card slot node ptr, passed as r3)
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: [OAM shadow via render_overlay_oam_sprite_tiled x2] writes highlight box OAM entries
render_pack_card_highlight_sprite:
    push {r4,r5,lr}                          @ 080d55cc 30b5
    adds r5,r0,#0x0    @ 080d55ce 051c
    ldr r0, DAT_080d55f0                     @ 080d55d0 0748
    ldr r4, DAT_080d55f4                     @ 080d55d2 084c
    ldr r2, DAT_080d55f8                     @ 080d55d4 084a
    adds r1,r4,#0x0    @ 080d55d6 211c
    adds r3,r5,#0x0    @ 080d55d8 2b1c
    bl render_overlay_oam_sprite_tiled       @ 080d55da 08f0c9f8
    ldr r0, DAT_080d55fc                     @ 080d55de 0748
    ldr r2, DAT_080d5600                     @ 080d55e0 074a
    adds r1,r4,#0x0    @ 080d55e2 211c
    adds r3,r5,#0x0    @ 080d55e4 2b1c
    bl render_overlay_oam_sprite_tiled       @ 080d55e6 08f0c3f8
    pop {r4,r5}                              @ 080d55ea 30bc
    pop {r0}                                 @ 080d55ec 01bc
    bx r0                                    @ 080d55ee 0047
DAT_080d55f0:
    .word  0x00900008                     @ 080d55f0 08009000
DAT_080d55f4:
    .word  0x0002000d                     @ 080d55f4 0d000200
DAT_080d55f8:
    .word  0x000b0280                     @ 080d55f8 80020b00
DAT_080d55fc:
    .word  0x00900080                     @ 080d55fc 80009000
DAT_080d5600:
    .word  0x000b028d                     @ 080d5600 8d020b00

@ Called by the state machine when the pack scene enters the scroll/AOB display phase, to initialize AOB display area scroll state fields. Clears three halfwords at pack_ui_state offsets +0x18, +0x1a, +0x22 (scroll position/count), and clears or initializes control fields at [+0x6fa] and [+0x724]. Then calls init_overlay_struct_and_palette with EWRAM address 0x0200af20 as the overlay base (mode=0x6, color_count=0xf, target OAM/palette area). Returns fixed value 1 indicating successful initialization.
@ 
@ Constants:
@ - pack_ui_state base = 0x03005850
@ - SCROLL_POS_OFFSET_0 = 0x18 (strh r4,[r5,#0x18])
@ - SCROLL_POS_OFFSET_1 = 0x1a (strh r4,[r5,#0x1a])
@ - SCROLL_POS_OFFSET_2 = 0x22 (strh r4,[r5,#0x22])
@ - FIELD_OFFSET_6FA = 0x6fa (DAT_080d565c)
@ - FIELD_OFFSET_704 = 0x704 (DAT_080d5660)
@ - FIELD_OFFSET_724 = 0x724 (DAT_080d5664)
@ - OVERLAY_EWRAM_BASE = 0x0200af20 (DAT_080d5668)
@ - OVERLAY_MODE = 6 (str r3,[sp,#0] where r3=0x6)
@ - OVERLAY_COLOR_COUNT = 0xf (movs r3,#0xf)
init_pack_aob_scroll_state:
    push {r4,r5,lr}                          @ 080d5604 30b5
    sub sp,#0x4                              @ 080d5606 81b0
    ldr r0, DAT_080d5658                     @ 080d5608 1348
    adds r5,r0,#0x0    @ 080d560a 051c
    adds r5,#0xc    @ 080d560c 0c35
    movs r4,#0x0    @ 080d560e 0024
    strh r4,[r5,#0x18]                       @ 080d5610 2c83
    strh r4,[r5,#0x1a]                       @ 080d5612 6c83
    strh r4,[r5,#0x22]                       @ 080d5614 6c84
    ldr r2, DAT_080d565c                     @ 080d5616 114a
    adds r1,r0,r2    @ 080d5618 8118
    strh r4,[r1,#0x0]                        @ 080d561a 0c80
    ldr r3, DAT_080d5660                     @ 080d561c 104b
    adds r2,r0,r3    @ 080d561e c218
    subs r3,#0x4    @ 080d5620 043b
    adds r1,r0,r3    @ 080d5622 c118
    ldr r1,[r1,#0x0]                         @ 080d5624 0968
    str r1,[r2,#0x0]                         @ 080d5626 1160
    ldr r1, DAT_080d5664                     @ 080d5628 0e49
    adds r2,r0,r1    @ 080d562a 4218
    movs r1,#0x9    @ 080d562c 0921
    rsbs r1,r1,#0    @ 080d562e 4942
    ldrb r3,[r2,#0x0]                        @ 080d5630 1378
    ands r1,r3    @ 080d5632 1940
    strb r1,[r2,#0x0]                        @ 080d5634 1170
    movs r1,#0xda    @ 080d5636 da21
    lsls r1,r1,#0x3    @ 080d5638 c900
    adds r0,r0,r1    @ 080d563a 4018
    ldr r1, DAT_080d5668                     @ 080d563c 0a49
    movs r2,#0xb0    @ 080d563e b022
    lsls r2,r2,#0x2    @ 080d5640 9200
    movs r3,#0x6    @ 080d5642 0623
    str r3,[sp,#0x0]                         @ 080d5644 0093
    movs r3,#0xf    @ 080d5646 0f23
    bl init_overlay_struct_and_palette       @ 080d5648 07f0aefe
    strh r4,[r5,#0x4]                        @ 080d564c ac80
    movs r0,#0x1    @ 080d564e 0120
    add sp,#0x4                              @ 080d5650 01b0
    pop {r4,r5}                              @ 080d5652 30bc
    pop {r1}                                 @ 080d5654 02bc
    bx r1                                    @ 080d5656 0847
DAT_080d5658:
    .word  pack_ui_state                  @ 080d5658 50580003
DAT_080d565c:
    .word  0x000006fa                     @ 080d565c fa060000
DAT_080d5660:
    .word  0x00000704                     @ 080d5660 04070000
DAT_080d5664:
    .word  0x00000724                     @ 080d5664 24070000
DAT_080d5668:
    .word  0x0200af20                     @ 080d5668 20af0002

@ 拆包场景的完整初始布局与渲染. 先调 init_pack_scene_bg_and_vram 与 load_pack_bg_tiles_and_palette 建立背景与 VRAM, 计算并写入卡牌起始滚动位置 [+0x3e]; 然后从当前卡牌索引 [+0x1a] 起遍历可见卡槽, 逐张调 dispatch_pack_card_image_render_by_state 渲染卡图; 接着经 copy_memory_dma3_with_cpu_fallback 拷贝图块, 渲染卡名/拥有数量/标签精灵行, 加载卡图 tile, 设置滚动起点 set_pack_scroll_start_pos(0x14) 与步进模式, 初始化 AOB 显示行与色板, 渲染两组标签文本, 最后生成 HSV 色板条. 整场景一次性铺设.
init_pack_scene_full_layout:
    push {r4,r5,r6,r7,lr}                    @ 080d566c f0b5
    .hword 0x4647    @ 080d566e 4746
    push {r7}                                @ 080d5670 80b4
    sub sp,#0xc                              @ 080d5672 83b0
    ldr r0, DAT_080d56cc                     @ 080d5674 1548
    movs r1,#0xc    @ 080d5676 0c21
    adds r1,r1,r0    @ 080d5678 0918
    .hword 0x4688    @ 080d567a 8846
    ldr r2, DAT_080d56d0                     @ 080d567c 144a
    adds r1,r0,r2    @ 080d567e 8118
    ldr r7,[r1,#0x0]                         @ 080d5680 0f68
    ldr r1, DAT_080d56d4                     @ 080d5682 1449
    adds r0,r0,r1    @ 080d5684 4018
    ldr r6,[r0,#0x0]                         @ 080d5686 0668
    bl init_pack_scene_bg_and_vram           @ 080d5688 fff7a8f9
    .hword 0x4642    @ 080d568c 4246
    ldrh r2,[r2,#0x1a]                       @ 080d568e 528b
    lsls r0,r2,#0x6    @ 080d5690 9001
    adds r0,#0x10    @ 080d5692 1030
    movs r1,#0xff    @ 080d5694 ff21
    ands r0,r1    @ 080d5696 0840
    .hword 0x4641    @ 080d5698 4146
    strh r0,[r1,#0x3e]                       @ 080d569a c887
    bl load_pack_bg_tiles_and_palette        @ 080d569c fff73efb
    .hword 0x4642    @ 080d56a0 4246
    ldrh r4,[r2,#0x1a]                       @ 080d56a2 548b
    subs r4,#0x1    @ 080d56a4 013c
    lsls r0,r4,#0x2    @ 080d56a6 a000
    adds r7,r7,r0    @ 080d56a8 3f18
    movs r5,#0x0    @ 080d56aa 0025
    ldrh r0,[r2,#0xa]                        @ 080d56ac 5089
    cmp r4,r0                                @ 080d56ae 8442
    bge LAB_080d56f4                         @ 080d56b0 20da
LAB_080d56b2:
    cmp r4,#0x0                              @ 080d56b2 002c
    blt LAB_080d56d8                         @ 080d56b4 10db
    adds r0,r5,#0x0    @ 080d56b6 281c
    adds r1,r7,#0x0    @ 080d56b8 391c
    adds r2,r6,#0x0    @ 080d56ba 321c
    bl dispatch_pack_card_image_render_by_state @ 080d56bc fff7cef9
    movs r0,#0xf    @ 080d56c0 0f20
    ldrb r1,[r7,#0x1]                        @ 080d56c2 7978
    ands r0,r1    @ 080d56c4 0840
    lsls r0,r0,#0x2    @ 080d56c6 8000
    adds r6,r6,r0    @ 080d56c8 3618
    b LAB_080d56e2                           @ 080d56ca 0ae0
DAT_080d56cc:
    .word  pack_ui_state                  @ 080d56cc 50580003
DAT_080d56d0:
    .word  0x000006fc                     @ 080d56d0 fc060000
DAT_080d56d4:
    .word  0x00000704                     @ 080d56d4 04070000
LAB_080d56d8:
    adds r0,r5,#0x0    @ 080d56d8 281c
    movs r1,#0x0    @ 080d56da 0021
    movs r2,#0x0    @ 080d56dc 0022
    bl dispatch_pack_card_image_render_by_state @ 080d56de fff7bdf9
LAB_080d56e2:
    adds r7,#0x4    @ 080d56e2 0437
    adds r4,#0x1    @ 080d56e4 0134
    adds r5,#0x1    @ 080d56e6 0135
    cmp r5,#0x2                              @ 080d56e8 022d
    bgt LAB_080d56f4                         @ 080d56ea 03dc
    .hword 0x4642    @ 080d56ec 4246
    ldrh r2,[r2,#0xa]                        @ 080d56ee 5289
    cmp r4,r2                                @ 080d56f0 9442
    blt LAB_080d56b2                         @ 080d56f2 dedb
LAB_080d56f4:
    movs r6,#0x3    @ 080d56f4 0326
    movs r0,#0x3    @ 080d56f6 0320
    .hword 0x4641    @ 080d56f8 4146
    strh r0,[r1,#0x38]                       @ 080d56fa 0887
    ldr r0, DAT_080d5838                     @ 080d56fc 4e48
    ldr r4, PTR_pack_banner_obj_palette_080d583c @ 080d56fe 4f4c
    movs r5,#0x90    @ 080d5700 9025
    lsls r5,r5,#0x1    @ 080d5702 6d00
    adds r1,r4,#0x0    @ 080d5704 211c
    adds r2,r5,#0x0    @ 080d5706 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d5708 1ff0fefb
    movs r0,#0xa0    @ 080d570c a020
    lsls r0,r0,#0x13    @ 080d570e c004
    adds r1,r4,#0x0    @ 080d5710 211c
    adds r2,r5,#0x0    @ 080d5712 2a1c
    bl copy_memory_dma3_with_cpu_fallback    @ 080d5714 1ff0f8fb
    movs r5,#0xe3    @ 080d5718 e325
    lsls r5,r5,#0x3    @ 080d571a ed00
    add r5,r8                                @ 080d571c 4544
    movs r0,#0x41    @ 080d571e 4120
    rsbs r0,r0,#0    @ 080d5720 4042
    ldrb r2,[r5,#0x0]                        @ 080d5722 2a78
    ands r0,r2    @ 080d5724 1040
    strb r0,[r5,#0x0]                        @ 080d5726 2870
    movs r0,#0xde    @ 080d5728 de20
    lsls r0,r0,#0x3    @ 080d572a c000
    add r0,r8                                @ 080d572c 4044
    ldr r7,[r0,#0x0]                         @ 080d572e 0768
    ldr r0,[r7,#0x0]                         @ 080d5730 3868
    lsls r0,r0,#0x19    @ 080d5732 4006
    lsrs r0,r0,#0x19    @ 080d5734 400e
    movs r1,#0x0    @ 080d5736 0021
    bl render_pack_name_to_obj_sprite_row    @ 080d5738 fff72efb
    ldr r4, DAT_080d5840                     @ 080d573c 404c
    add r4,r8                                @ 080d573e 4444
    movs r0,#0x3    @ 080d5740 0320
    rsbs r0,r0,#0    @ 080d5742 4042
    ldrb r1,[r4,#0x0]                        @ 080d5744 2178
    ands r0,r1    @ 080d5746 0840
    strb r0,[r4,#0x0]                        @ 080d5748 2070
    ldr r0,[r7,#0x0]                         @ 080d574a 3868
    lsls r0,r0,#0x19    @ 080d574c 4006
    lsrs r0,r0,#0x19    @ 080d574e 400e
    movs r1,#0x0    @ 080d5750 0021
    bl render_pack_owned_count_to_sprite_row @ 080d5752 fff779fb
    movs r0,#0x2    @ 080d5756 0220
    rsbs r0,r0,#0    @ 080d5758 4042
    ldrb r2,[r4,#0x0]                        @ 080d575a 2278
    ands r0,r2    @ 080d575c 1040
    strb r0,[r4,#0x0]                        @ 080d575e 2070
    ldr r0,[r7,#0x0]                         @ 080d5760 3868
    lsls r0,r0,#0x19    @ 080d5762 4006
    lsrs r0,r0,#0x19    @ 080d5764 400e
    movs r1,#0x0    @ 080d5766 0021
    bl render_pack_label_name_to_sprite_row  @ 080d5768 fff790fb
    movs r0,#0xe8    @ 080d576c e820
    lsls r0,r0,#0x1    @ 080d576e 4000
    movs r1,#0xa    @ 080d5770 0a21
    bl load_pack_card_tile_row_to_obj_vram   @ 080d5772 06f001fe
    movs r0,#0xee    @ 080d5776 ee20
    lsls r0,r0,#0x1    @ 080d5778 4000
    str r0,[sp,#0x0]                         @ 080d577a 0090
    movs r0,#0x1    @ 080d577c 0120
    rsbs r0,r0,#0    @ 080d577e 4042
    str r0,[sp,#0x4]                         @ 080d5780 0190
    movs r0,#0xec    @ 080d5782 ec20
    lsls r0,r0,#0x1    @ 080d5784 4000
    str r0,[sp,#0x8]                         @ 080d5786 0290
    .hword 0x4668    @ 080d5788 6846
    movs r1,#0x9    @ 080d578a 0921
    bl load_pack_card_tiles_to_vram          @ 080d578c fef736ff
    movs r0,#0x14    @ 080d5790 1420
    movs r1,#0x50    @ 080d5792 5021
    bl set_pack_scroll_start_pos             @ 080d5794 fff7d4f8
    movs r0,#0x0    @ 080d5798 0020
    bl set_pack_scroll_step_mode             @ 080d579a fff7edf8
    bl init_pack_card_aob_display_row        @ 080d579e fff7a1fc
    movs r0,#0xb    @ 080d57a2 0b20
    bl copy_pack_card_palette_to_obj_pal     @ 080d57a4 06f022ff
    movs r0,#0x2    @ 080d57a8 0220
    movs r1,#0x1    @ 080d57aa 0121
    bl dispatch_pack_label_text_render_by_category @ 080d57ac fff7b6fc
    movs r0,#0x1    @ 080d57b0 0120
    movs r1,#0x0    @ 080d57b2 0021
    bl dispatch_pack_label_text_render_by_category @ 080d57b4 fff7b2fc
    ldr r0, DAT_080d5844                     @ 080d57b8 2248
    ldr r1, DAT_080d5848                     @ 080d57ba 2349
    movs r2,#0x20    @ 080d57bc 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 080d57be 1ff0a3fb
    ldr r0, DAT_080d584c                     @ 080d57c2 2248
    bl generate_hsv_palette_strip            @ 080d57c4 06f058fb
    ldr r1, PTR_BG3CNT_080d5850              @ 080d57c8 2149
    ldrh r2,[r1,#0x0]                        @ 080d57ca 0a88
    ldr r3, DAT_080d5854                     @ 080d57cc 214b
    adds r0,r3,#0x0    @ 080d57ce 181c
    ands r0,r2    @ 080d57d0 1040
    strh r0,[r1,#0x0]                        @ 080d57d2 0880
    ldrh r0,[r1,#0x0]                        @ 080d57d4 0888
    strh r0,[r1,#0x0]                        @ 080d57d6 0880
    ldr r2, PTR_BG0CNT_080d5858              @ 080d57d8 1f4a
    ldrh r1,[r2,#0x0]                        @ 080d57da 1188
    adds r0,r3,#0x0    @ 080d57dc 181c
    ands r0,r1    @ 080d57de 0840
    strh r0,[r2,#0x0]                        @ 080d57e0 1080
    ldrh r0,[r2,#0x0]                        @ 080d57e2 1088
    movs r1,#0x1    @ 080d57e4 0121
    orrs r0,r1    @ 080d57e6 0843
    strh r0,[r2,#0x0]                        @ 080d57e8 1080
    ldr r1, PTR_BG1CNT_080d585c              @ 080d57ea 1c49
    ldrh r2,[r1,#0x0]                        @ 080d57ec 0a88
    adds r0,r3,#0x0    @ 080d57ee 181c
    ands r0,r2    @ 080d57f0 1040
    strh r0,[r1,#0x0]                        @ 080d57f2 0880
    ldrh r0,[r1,#0x0]                        @ 080d57f4 0888
    orrs r0,r6    @ 080d57f6 3043
    strh r0,[r1,#0x0]                        @ 080d57f8 0880
    ldr r2, PTR_BG2CNT_080d5860              @ 080d57fa 194a
    ldrh r0,[r2,#0x0]                        @ 080d57fc 1088
    ands r3,r0    @ 080d57fe 0340
    strh r3,[r2,#0x0]                        @ 080d5800 1380
    ldrh r0,[r2,#0x0]                        @ 080d5802 1088
    movs r1,#0x2    @ 080d5804 0221
    orrs r0,r1    @ 080d5806 0843
    strh r0,[r2,#0x0]                        @ 080d5808 1080
    ldr r1, PTR_BLDCNT_080d5864              @ 080d580a 1649
    ldr r2, DAT_080d5868                     @ 080d580c 164a
    adds r0,r2,#0x0    @ 080d580e 101c
    strh r0,[r1,#0x0]                        @ 080d5810 0880
    adds r1,#0x2    @ 080d5812 0231
    movs r0,#0x10    @ 080d5814 1020
    strh r0,[r1,#0x0]                        @ 080d5816 0880
    movs r0,#0x14    @ 080d5818 1420
    .hword 0x4641    @ 080d581a 4146
    strh r0,[r1,#0x6]                        @ 080d581c c880
    subs r0,#0x35    @ 080d581e 3538
    ldrb r2,[r5,#0x0]                        @ 080d5820 2a78
    ands r0,r2    @ 080d5822 1040
    strb r0,[r5,#0x0]                        @ 080d5824 2870
    ldr r1, DAT_080d586c                     @ 080d5826 1149
    movs r0,#0x1    @ 080d5828 0120
    strh r0,[r1,#0x10]                       @ 080d582a 0882
    add sp,#0xc                              @ 080d582c 03b0
    pop {r3}                                 @ 080d582e 08bc
    .hword 0x4698    @ 080d5830 9846
    pop {r4,r5,r6,r7}                        @ 080d5832 f0bc
    pop {r1}                                 @ 080d5834 02bc
    bx r1                                    @ 080d5836 0847
DAT_080d5838:
    .word  0x05000200                     @ 080d5838 00020005
PTR_pack_banner_obj_palette_080d583c:
    .word  pack_banner_obj_palette        @ 080d583c 40045108
DAT_080d5840:
    .word  0x00000719                     @ 080d5840 19070000
DAT_080d5844:
    .word  0x050001e0                     @ 080d5844 e0010005
DAT_080d5848:
    .word  0x09ccd290                     @ 080d5848 90d2cc09
DAT_080d584c:
    .word  0x05000140                     @ 080d584c 40010005
PTR_BG3CNT_080d5850:
    .word  BG3CNT                         @ 080d5850 0e000004
DAT_080d5854:
    .word  0x0000fffc                     @ 080d5854 fcff0000
PTR_BG0CNT_080d5858:
    .word  BG0CNT                         @ 080d5858 08000004
PTR_BG1CNT_080d585c:
    .word  BG1CNT                         @ 080d585c 0a000004
PTR_BG2CNT_080d5860:
    .word  BG2CNT                         @ 080d5860 0c000004
PTR_BLDCNT_080d5864:
    .word  BLDCNT                         @ 080d5864 50000004
DAT_080d5868:
    .word  0x00001748                     @ 080d5868 48170000
DAT_080d586c:
    .word  pack_ui_state                  @ 080d586c 50580003

@ 拆包场景卡片淡入混合动画帧驱动. 从 pack_ui_state+0xc 读取帧计数器 [+0x6] 并递减; 检查是否 >0x13 决定下限截断. 当计数器 >0 时: 计算 BLDALPHA = (counter<<4)/0x14 的线性插值, 写 BLDALPHA 寄存器实现淡入效果, 跳到渲染路径. 当计数器 <=0 时: 配置 BG0CNT/BG1CNT/BG2CNT/BG3CNT 的 tile-base/priority 字段 (清 0xfffc 掩码后 OR 1/2/3), 写 BLDCNT=0x3f3f/BLDALPHA=0x1010 设置最终混合, 写 pack_ui_state+0xc+0x10=2 推进状态机到下一步. 末尾无条件调 render_pack_card_highlight_sprite(1) / render_pack_card_sprite_by_flip_state(1) / render_pack_card_slot_oam(r6+3). 由 tick_pack_card_info_step (0x080d7014) 从步骤表中调用.
tick_pack_card_blend_fade_in:
    push {r4,r5,r6,r7,lr}                    @ 080d5870 f0b5
    ldr r2, DAT_080d58a8                     @ 080d5872 0d4a
    adds r4,r2,#0x0    @ 080d5874 141c
    adds r4,#0xc    @ 080d5876 0c34
    movs r5,#0x0    @ 080d5878 0025
    movs r6,#0x1    @ 080d587a 0126
    movs r1,#0x80    @ 080d587c 8021
    lsls r1,r1,#0x13    @ 080d587e c904
    movs r0,#0xf8    @ 080d5880 f820
    lsls r0,r0,#0x5    @ 080d5882 4001
    strh r0,[r1,#0x0]                        @ 080d5884 0880
    ldrh r1,[r4,#0x6]                        @ 080d5886 e188
    subs r1,#0x1    @ 080d5888 0139
    strh r1,[r4,#0x6]                        @ 080d588a e180
    lsls r0,r1,#0x10    @ 080d588c 0804
    asrs r3,r0,#0x10    @ 080d588e 0314
    adds r7,r2,#0x0    @ 080d5890 171c
    cmp r3,#0x0                              @ 080d5892 002b
    ble LAB_080d589e                         @ 080d5894 03dd
    movs r2,#0x6    @ 080d5896 0622
    ldrsh r0,[r4,r2]                         @ 080d5898 a05e
    cmp r0,#0x13                             @ 080d589a 1328
    bgt LAB_080d58ac                         @ 080d589c 06dc
LAB_080d589e:
    adds r0,r1,#0x0    @ 080d589e 081c
    cmp r3,#0x0                              @ 080d58a0 002b
    bge LAB_080d58ae                         @ 080d58a2 04da
    movs r0,#0x0    @ 080d58a4 0020
    b LAB_080d58ae                           @ 080d58a6 02e0
DAT_080d58a8:
    .word  pack_ui_state                  @ 080d58a8 50580003
LAB_080d58ac:
    movs r0,#0x14    @ 080d58ac 1420
LAB_080d58ae:
    strh r0,[r4,#0x6]                        @ 080d58ae e080
    lsls r0,r0,#0x10    @ 080d58b0 0004
    cmp r0,#0x0                              @ 080d58b2 0028
    ble LAB_080d58dc                         @ 080d58b4 12dd
    movs r1,#0x6    @ 080d58b6 0621
    ldrsh r0,[r4,r1]                         @ 080d58b8 605e
    lsls r0,r0,#0x4    @ 080d58ba 0001
    movs r1,#0x14    @ 080d58bc 1421
    bl bios_div                              @ 080d58be 38f09dfd
    ldr r3, PTR_BLDALPHA_080d58d8            @ 080d58c2 054b
    lsls r2,r0,#0x18    @ 080d58c4 0206
    lsrs r2,r2,#0x18    @ 080d58c6 120e
    movs r1,#0x10    @ 080d58c8 1021
    subs r1,r1,r0    @ 080d58ca 091a
    lsls r1,r1,#0x18    @ 080d58cc 0906
    lsrs r1,r1,#0x10    @ 080d58ce 090c
    orrs r2,r1    @ 080d58d0 0a43
    strh r2,[r3,#0x0]                        @ 080d58d2 1a80
    b LAB_080d5938                           @ 080d58d4 30e0
    .zero  0x2
PTR_BLDALPHA_080d58d8:
    .word  BLDALPHA                       @ 080d58d8 52000004
LAB_080d58dc:
    ldr r1, PTR_BG0CNT_080d5954              @ 080d58dc 1d49
    ldrh r2,[r1,#0x0]                        @ 080d58de 0a88
    ldr r3, DAT_080d5958                     @ 080d58e0 1d4b
    adds r0,r3,#0x0    @ 080d58e2 181c
    ands r0,r2    @ 080d58e4 1040
    strh r0,[r1,#0x0]                        @ 080d58e6 0880
    ldrh r0,[r1,#0x0]                        @ 080d58e8 0888
    strh r0,[r1,#0x0]                        @ 080d58ea 0880
    ldr r2, PTR_BG1CNT_080d595c              @ 080d58ec 1b4a
    ldrh r1,[r2,#0x0]                        @ 080d58ee 1188
    adds r0,r3,#0x0    @ 080d58f0 181c
    ands r0,r1    @ 080d58f2 0840
    strh r0,[r2,#0x0]                        @ 080d58f4 1080
    ldrh r0,[r2,#0x0]                        @ 080d58f6 1088
    movs r1,#0x2    @ 080d58f8 0221
    orrs r0,r1    @ 080d58fa 0843
    strh r0,[r2,#0x0]                        @ 080d58fc 1080
    adds r2,#0x2    @ 080d58fe 0232
    ldrh r1,[r2,#0x0]                        @ 080d5900 1188
    adds r0,r3,#0x0    @ 080d5902 181c
    ands r0,r1    @ 080d5904 0840
    strh r0,[r2,#0x0]                        @ 080d5906 1080
    ldrh r0,[r2,#0x0]                        @ 080d5908 1088
    movs r1,#0x1    @ 080d590a 0121
    orrs r0,r1    @ 080d590c 0843
    strh r0,[r2,#0x0]                        @ 080d590e 1080
    adds r2,#0x2    @ 080d5910 0232
    ldrh r0,[r2,#0x0]                        @ 080d5912 1088
    ands r3,r0    @ 080d5914 0340
    strh r3,[r2,#0x0]                        @ 080d5916 1380
    ldrh r0,[r2,#0x0]                        @ 080d5918 1088
    movs r1,#0x3    @ 080d591a 0321
    orrs r0,r1    @ 080d591c 0843
    strh r0,[r2,#0x0]                        @ 080d591e 1080
    movs r6,#0x0    @ 080d5920 0026
    ldr r1, PTR_BLDCNT_080d5960              @ 080d5922 0f49
    ldr r2, DAT_080d5964                     @ 080d5924 0f4a
    adds r0,r2,#0x0    @ 080d5926 101c
    strh r0,[r1,#0x0]                        @ 080d5928 0880
    adds r1,#0x2    @ 080d592a 0231
    ldr r2, DAT_080d5968                     @ 080d592c 0e4a
    adds r0,r2,#0x0    @ 080d592e 101c
    strh r0,[r1,#0x0]                        @ 080d5930 0880
    movs r0,#0x2    @ 080d5932 0220
    strh r0,[r7,#0x10]                       @ 080d5934 3882
    movs r5,#0x1    @ 080d5936 0125
LAB_080d5938:
    movs r0,#0x1    @ 080d5938 0120
    bl render_pack_card_highlight_sprite     @ 080d593a fff747fe
    movs r0,#0x1    @ 080d593e 0120
    bl render_pack_card_sprite_by_flip_state @ 080d5940 fef7b2fe
    adds r0,r6,#0x3    @ 080d5944 f01c
    bl render_pack_card_slot_oam             @ 080d5946 fff71dfc
    adds r0,r5,#0x0    @ 080d594a 281c
    pop {r4,r5,r6,r7}                        @ 080d594c f0bc
    pop {r1}                                 @ 080d594e 02bc
    bx r1                                    @ 080d5950 0847
    .zero  0x2
PTR_BG0CNT_080d5954:
    .word  BG0CNT                         @ 080d5954 08000004
DAT_080d5958:
    .word  0x0000fffc                     @ 080d5958 fcff0000
PTR_BG1CNT_080d595c:
    .word  BG1CNT                         @ 080d595c 0a000004
PTR_BLDCNT_080d5960:
    .word  BLDCNT                         @ 080d5960 50000004
DAT_080d5964:
    .word  0x00003f3f                     @ 080d5964 3f3f0000
DAT_080d5968:
    .word  0x00001010                     @ 080d5968 10100000

@ Initializes IO register set for the pack scene scroll animation. Calls init_pack_scroll_animation(pack_ui_state+0xc, 0x38, 0x50, 8); sets scroll state [+0x6]=8. Writes BLDCNT=0x2da, BLDY=0, BLDALPHA=0x1010; WIN0H/WIN1H=0xf0 (full width); WIN0V=0x1010, WIN1V=0x9090. ORs DISPCNT with WIN0_ENABLE=0x2000 and WIN1_ENABLE=0x4000. Called by FUN_080d5a08 for entering the pack card scroll display state.
@ 
@ Constants:
@ - pack_ui_state = 0x03005850 (DAT_080d59e0)
@ - SCROLL_STRUCT_OFFSET = 0xc
@ - SCROLL_PARAM_A = 0x38, SCROLL_PARAM_B = 0x50, SCROLL_PARAM_C = 8
@ - BLDCNT = 0x04000050 (PTR_BLDCNT_080d59e4)
@ - BLDCNT_VAL = 0x2da (DAT_080d59e8)
@ - BLDY = 0x04000054 (PTR_BLDY_080d59ec)
@ - WIN0H = 0x04000040 (PTR_WIN0H_080d59f8)
@ - DISPCNT = 0x04000000 (movs r2,#0x80; lsls r2,#0x13)
@ - WIN0_ENABLE = 0x2000 (movs r3,#0x80; lsls r3,#6)
@ - WIN1_ENABLE = 0x4000 (movs r3,#0x80; lsls r3,#7)
@ 
@ Inputs: none
@ Returns: void (pop{r0}+bx r0 Sub-case F)
@ Side effects: BLDCNT:=0x2da; BLDY:=0; BLDALPHA:=0x1010; WIN0H/WIN1H:=0xf0; WIN0V/WIN1V set; DISPCNT |= 0x6000
init_pack_scroll_blend_and_window_regs:
    push {r4,lr}                             @ 080d596c 10b5
    ldr r4, DAT_080d59e0                     @ 080d596e 1c4c
    adds r4,#0xc    @ 080d5970 0c34
    movs r0,#0x38    @ 080d5972 3820
    movs r1,#0x50    @ 080d5974 5021
    movs r2,#0x8    @ 080d5976 0822
    bl init_pack_scroll_animation            @ 080d5978 fff706f8
    movs r2,#0x0    @ 080d597c 0022
    movs r0,#0x8    @ 080d597e 0820
    strh r0,[r4,#0x6]                        @ 080d5980 e080
    ldr r1, PTR_BLDCNT_080d59e4              @ 080d5982 1849
    ldr r3, DAT_080d59e8                     @ 080d5984 184b
    adds r0,r3,#0x0    @ 080d5986 181c
    strh r0,[r1,#0x0]                        @ 080d5988 0880
    ldr r0, PTR_BLDY_080d59ec                @ 080d598a 1848
    strh r2,[r0,#0x0]                        @ 080d598c 0280
    adds r1,#0x2    @ 080d598e 0231
    movs r0,#0x10    @ 080d5990 1020
    strh r0,[r1,#0x0]                        @ 080d5992 0880
    subs r1,#0xa    @ 080d5994 0a39
    ldr r2, DAT_080d59f0                     @ 080d5996 164a
    adds r0,r2,#0x0    @ 080d5998 101c
    strh r0,[r1,#0x0]                        @ 080d599a 0880
    adds r1,#0x2    @ 080d599c 0231
    ldr r3, DAT_080d59f4                     @ 080d599e 154b
    adds r0,r3,#0x0    @ 080d59a0 181c
    strh r0,[r1,#0x0]                        @ 080d59a2 0880
    ldr r0, PTR_WIN0H_080d59f8               @ 080d59a4 1448
    movs r2,#0xf0    @ 080d59a6 f022
    strh r2,[r0,#0x0]                        @ 080d59a8 0280
    subs r1,#0x6    @ 080d59aa 0639
    ldr r3, DAT_080d59fc                     @ 080d59ac 134b
    adds r0,r3,#0x0    @ 080d59ae 181c
    strh r0,[r1,#0x0]                        @ 080d59b0 0880
    ldr r0, PTR_WIN1H_080d5a00               @ 080d59b2 1348
    strh r2,[r0,#0x0]                        @ 080d59b4 0280
    adds r1,#0x2    @ 080d59b6 0231
    ldr r2, DAT_080d5a04                     @ 080d59b8 124a
    adds r0,r2,#0x0    @ 080d59ba 101c
    strh r0,[r1,#0x0]                        @ 080d59bc 0880
    movs r2,#0x80    @ 080d59be 8022
    lsls r2,r2,#0x13    @ 080d59c0 d204
    ldrh r0,[r2,#0x0]                        @ 080d59c2 1088
    movs r3,#0x80    @ 080d59c4 8023
    lsls r3,r3,#0x6    @ 080d59c6 9b01
    adds r1,r3,#0x0    @ 080d59c8 191c
    orrs r0,r1    @ 080d59ca 0843
    strh r0,[r2,#0x0]                        @ 080d59cc 1080
    ldrh r0,[r2,#0x0]                        @ 080d59ce 1088
    movs r3,#0x80    @ 080d59d0 8023
    lsls r3,r3,#0x7    @ 080d59d2 db01
    adds r1,r3,#0x0    @ 080d59d4 191c
    orrs r0,r1    @ 080d59d6 0843
    strh r0,[r2,#0x0]                        @ 080d59d8 1080
    pop {r4}                                 @ 080d59da 10bc
    pop {r0}                                 @ 080d59dc 01bc
    bx r0                                    @ 080d59de 0047
DAT_080d59e0:
    .word  pack_ui_state                  @ 080d59e0 50580003
PTR_BLDCNT_080d59e4:
    .word  BLDCNT                         @ 080d59e4 50000004
DAT_080d59e8:
    .word  0x000002da                     @ 080d59e8 da020000
PTR_BLDY_080d59ec:
    .word  BLDY                           @ 080d59ec 54000004
DAT_080d59f0:
    .word  0x00003f3f                     @ 080d59f0 3f3f0000
DAT_080d59f4:
    .word  0x00003f1f                     @ 080d59f4 1f3f0000
PTR_WIN0H_080d59f8:
    .word  WIN0H                          @ 080d59f8 40000004
DAT_080d59fc:
    .word  0x00001010                     @ 080d59fc 10100000
PTR_WIN1H_080d5a00:
    .word  WIN1H                          @ 080d5a00 42000004
DAT_080d5a04:
    .word  0x00009090                     @ 080d5a04 90900000

@ 拆包场景卡片翻页滚动动画帧驱动 (带旋转精灵). 入口保存 r8/r9/r10 至高寄存器. 从 pack_ui_state 读状态: [+0x6fc] 卡组 ptr, [+0x6fa] 当前 slot_index, 取对应卡槽 flag 字节 bit7 作为方向 (r7). 检查 gPrng+0xa4*2=0x148 的 bit1: 若置位走 "向前滚动" 分支; 若清零走 "向后滚动" 或 "空闲状态" 分支. 向前分支: 若当前卡槽 bit3 未置则 sync_state(0x24) + 清 0x21 mask; 若已置则配置 BG0CNT/BG1CNT/BG3CNT + BLDCNT + 调 sync_state(0x1) 进入旋转状态. 中间判断基于 scroll_pos ([+0x1a] vs [+0xa]) 决定是否调 tick_pack_card_image_scroll_forward/back. 到达边界后调 init_pack_scroll_blend_and_window_regs 初始化窗口寄存器. 末尾调 render_pack_card_highlight_sprite + render_pack_card_spin_oam_by_mode + render_pack_card_sprite_by_flip_state + render_pack_card_slot_oam + tick_pack_name_scroll_strip_row0.
tick_pack_card_scroll_with_spin:
    push {r4,r5,r6,r7,lr}                    @ 080d5a08 f0b5
    .hword 0x4657    @ 080d5a0a 5746
    .hword 0x464e    @ 080d5a0c 4e46
    .hword 0x4645    @ 080d5a0e 4546
    push {r5,r6,r7}                          @ 080d5a10 e0b4
    ldr r4, DAT_080d5a6c                     @ 080d5a12 164c
    adds r5,r4,#0x0    @ 080d5a14 251c
    adds r5,#0xc    @ 080d5a16 0c35
    ldr r0, DAT_080d5a70                     @ 080d5a18 1548
    adds r2,r4,r0    @ 080d5a1a 2218
    ldr r1, DAT_080d5a74                     @ 080d5a1c 1549
    adds r0,r4,r1    @ 080d5a1e 6018
    ldrh r0,[r0,#0x0]                        @ 080d5a20 0088
    lsls r1,r0,#0x2    @ 080d5a22 8100
    ldr r0,[r2,#0x0]                         @ 080d5a24 1068
    adds r0,r0,r1    @ 080d5a26 4018
    .hword 0x4680    @ 080d5a28 8046
    movs r6,#0x0    @ 080d5a2a 0026
    movs r2,#0x1    @ 080d5a2c 0122
    .hword 0x4691    @ 080d5a2e 9146
    ldrb r2,[r0,#0x0]                        @ 080d5a30 0278
    lsrs r7,r2,#0x7    @ 080d5a32 d709
    .hword 0x46b2    @ 080d5a34 b246
    ldr r0, PTR_gPrng_080d5a78               @ 080d5a36 1048
    movs r1,#0xa4    @ 080d5a38 a421
    lsls r1,r1,#0x1    @ 080d5a3a 4900
    adds r0,r0,r1    @ 080d5a3c 4018
    ldrh r1,[r0,#0x0]                        @ 080d5a3e 0188
    movs r0,#0x2    @ 080d5a40 0220
    ands r0,r1    @ 080d5a42 0840
    cmp r0,#0x0                              @ 080d5a44 0028
    beq LAB_080d5b08                         @ 080d5a46 5fd0
    ldr r2, DAT_080d5a7c                     @ 080d5a48 0c4a
    adds r4,r4,r2    @ 080d5a4a a418
    movs r0,#0x8    @ 080d5a4c 0820
    ldrb r1,[r4,#0x0]                        @ 080d5a4e 2178
    ands r0,r1    @ 080d5a50 0840
    cmp r0,#0x0                              @ 080d5a52 0028
    bne LAB_080d5a80                         @ 080d5a54 14d1
    movs r0,#0x24    @ 080d5a56 2420
    bl sync_state_and_init_sprite            @ 080d5a58 24f02cf8
    movs r0,#0x21    @ 080d5a5c 2120
    rsbs r0,r0,#0    @ 080d5a5e 4042
    ldrb r2,[r4,#0x0]                        @ 080d5a60 2278
    ands r0,r2    @ 080d5a62 1040
    strb r0,[r4,#0x0]                        @ 080d5a64 2070
    movs r0,#0x7    @ 080d5a66 0720
    b LAB_080d5c3a                           @ 080d5a68 e7e0
    .zero  0x2
DAT_080d5a6c:
    .word  pack_ui_state                  @ 080d5a6c 50580003
DAT_080d5a70:
    .word  0x000006fc                     @ 080d5a70 fc060000
DAT_080d5a74:
    .word  0x000006fa                     @ 080d5a74 fa060000
PTR_gPrng_080d5a78:
    .word  gPrng                          @ 080d5a78 40000003
DAT_080d5a7c:
    .word  0x00000724                     @ 080d5a7c 24070000
LAB_080d5a80:
    ldr r1, PTR_BG3CNT_080d5af4              @ 080d5a80 1c49
    ldrh r2,[r1,#0x0]                        @ 080d5a82 0a88
    ldr r3, DAT_080d5af8                     @ 080d5a84 1c4b
    adds r0,r3,#0x0    @ 080d5a86 181c
    ands r0,r2    @ 080d5a88 1040
    strh r0,[r1,#0x0]                        @ 080d5a8a 0880
    ldrh r0,[r1,#0x0]                        @ 080d5a8c 0888
    strh r0,[r1,#0x0]                        @ 080d5a8e 0880
    ldr r2, PTR_BG0CNT_080d5afc              @ 080d5a90 1a4a
    ldrh r1,[r2,#0x0]                        @ 080d5a92 1188
    adds r0,r3,#0x0    @ 080d5a94 181c
    ands r0,r1    @ 080d5a96 0840
    strh r0,[r2,#0x0]                        @ 080d5a98 1080
    ldrh r0,[r2,#0x0]                        @ 080d5a9a 1088
    movs r1,#0x1    @ 080d5a9c 0121
    orrs r0,r1    @ 080d5a9e 0843
    strh r0,[r2,#0x0]                        @ 080d5aa0 1080
    adds r2,#0x2    @ 080d5aa2 0232
    ldrh r1,[r2,#0x0]                        @ 080d5aa4 1188
    adds r0,r3,#0x0    @ 080d5aa6 181c
    ands r0,r1    @ 080d5aa8 0840
    strh r0,[r2,#0x0]                        @ 080d5aaa 1080
    ldrh r0,[r2,#0x0]                        @ 080d5aac 1088
    movs r1,#0x3    @ 080d5aae 0321
    orrs r0,r1    @ 080d5ab0 0843
    strh r0,[r2,#0x0]                        @ 080d5ab2 1080
    adds r2,#0x2    @ 080d5ab4 0232
    ldrh r0,[r2,#0x0]                        @ 080d5ab6 1088
    ands r3,r0    @ 080d5ab8 0340
    strh r3,[r2,#0x0]                        @ 080d5aba 1380
    ldrh r0,[r2,#0x0]                        @ 080d5abc 1088
    movs r1,#0x2    @ 080d5abe 0221
    orrs r0,r1    @ 080d5ac0 0843
    strh r0,[r2,#0x0]                        @ 080d5ac2 1080
    movs r0,#0x1    @ 080d5ac4 0120
    .hword 0x4682    @ 080d5ac6 8246
    ldr r1, PTR_BLDCNT_080d5b00              @ 080d5ac8 0d49
    ldr r2, DAT_080d5b04                     @ 080d5aca 0e4a
    adds r0,r2,#0x0    @ 080d5acc 101c
    strh r0,[r1,#0x0]                        @ 080d5ace 0880
    adds r1,#0x2    @ 080d5ad0 0231
    movs r2,#0x80    @ 080d5ad2 8022
    lsls r2,r2,#0x5    @ 080d5ad4 5201
    adds r0,r2,#0x0    @ 080d5ad6 101c
    strh r0,[r1,#0x0]                        @ 080d5ad8 0880
    movs r7,#0x0    @ 080d5ada 0027
    movs r0,#0x10    @ 080d5adc 1020
    strh r0,[r5,#0x6]                        @ 080d5ade e880
    movs r0,#0x1    @ 080d5ae0 0120
    bl sync_state_and_init_sprite            @ 080d5ae2 23f0e7ff
    movs r0,#0x21    @ 080d5ae6 2120
    rsbs r0,r0,#0    @ 080d5ae8 4042
    ldrb r1,[r4,#0x0]                        @ 080d5aea 2178
    ands r0,r1    @ 080d5aec 0840
    strb r0,[r4,#0x0]                        @ 080d5aee 2070
    movs r0,#0xb    @ 080d5af0 0b20
    b LAB_080d5c3a                           @ 080d5af2 a2e0
PTR_BG3CNT_080d5af4:
    .word  BG3CNT                         @ 080d5af4 0e000004
DAT_080d5af8:
    .word  0x0000fffc                     @ 080d5af8 fcff0000
PTR_BG0CNT_080d5afc:
    .word  BG0CNT                         @ 080d5afc 08000004
PTR_BLDCNT_080d5b00:
    .word  BLDCNT                         @ 080d5b00 50000004
DAT_080d5b04:
    .word  0x00001748                     @ 080d5b04 48170000
LAB_080d5b08:
    .hword 0x4648    @ 080d5b08 4846
    ands r0,r1    @ 080d5b0a 0840
    cmp r0,#0x0                              @ 080d5b0c 0028
    beq LAB_080d5b70                         @ 080d5b0e 2fd0
    ldrh r0,[r5,#0x1a]                       @ 080d5b10 688b
    ldrh r1,[r5,#0xa]                        @ 080d5b12 6989
    cmp r0,r1                                @ 080d5b14 8842
    bcc LAB_080d5b1a                         @ 080d5b16 00d3
    b LAB_080d5c62                           @ 080d5b18 a3e0
LAB_080d5b1a:
    movs r1,#0x80    @ 080d5b1a 8021
    adds r0,r1,#0x0    @ 080d5b1c 081c
    ands r0,r2    @ 080d5b1e 1040
    cmp r0,#0x0                              @ 080d5b20 0028
    bne LAB_080d5b28                         @ 080d5b22 01d1
    movs r0,#0x5    @ 080d5b24 0520
    b LAB_080d5c3a                           @ 080d5b26 88e0
LAB_080d5b28:
    ldrh r0,[r5,#0xa]                        @ 080d5b28 6889
    subs r0,#0x1    @ 080d5b2a 0138
    ldrh r2,[r5,#0x1a]                       @ 080d5b2c 6a8b
    cmp r2,r0                                @ 080d5b2e 8242
    blt LAB_080d5b34                         @ 080d5b30 00db
    b LAB_080d5c62                           @ 080d5b32 96e0
LAB_080d5b34:
    adds r0,r1,#0x0    @ 080d5b34 081c
    .hword 0x4641    @ 080d5b36 4146
    ldrb r1,[r1,#0x4]                        @ 080d5b38 0979
    ands r0,r1    @ 080d5b3a 0840
    cmp r0,#0x0                              @ 080d5b3c 0028
    beq LAB_080d5b42                         @ 080d5b3e 00d0
    b LAB_080d5c62                           @ 080d5b40 8fe0
LAB_080d5b42:
    bl tick_pack_card_image_scroll_forward   @ 080d5b42 fff729f8
    movs r2,#0x0    @ 080d5b46 0022
    .hword 0x4691    @ 080d5b48 9146
    movs r7,#0x0    @ 080d5b4a 0027
    movs r0,#0x0    @ 080d5b4c 0020
    bl sync_state_and_init_sprite            @ 080d5b4e 23f0b1ff
    ldr r0, DAT_080d5b6c                     @ 080d5b52 0648
    adds r2,r4,r0    @ 080d5b54 2218
    movs r0,#0x21    @ 080d5b56 2120
    rsbs r0,r0,#0    @ 080d5b58 4042
    ldrb r1,[r2,#0x0]                        @ 080d5b5a 1178
    ands r0,r1    @ 080d5b5c 0840
    movs r1,#0x11    @ 080d5b5e 1121
    rsbs r1,r1,#0    @ 080d5b60 4942
    ands r0,r1    @ 080d5b62 0840
    strb r0,[r2,#0x0]                        @ 080d5b64 1070
    movs r0,#0x3    @ 080d5b66 0320
    b LAB_080d5c3a                           @ 080d5b68 67e0
    .zero  0x2
DAT_080d5b6c:
    .word  0x00000724                     @ 080d5b6c 24070000
LAB_080d5b70:
    movs r0,#0xf0    @ 080d5b70 f020
    ands r0,r1    @ 080d5b72 0840
    cmp r0,#0x0                              @ 080d5b74 0028
    beq LAB_080d5c62                         @ 080d5b76 74d0
    movs r3,#0x80    @ 080d5b78 8023
    adds r0,r3,#0x0    @ 080d5b7a 181c
    ands r0,r1    @ 080d5b7c 0840
    cmp r0,#0x0                              @ 080d5b7e 0028
    beq LAB_080d5bc4                         @ 080d5b80 20d0
    ldrh r0,[r5,#0xa]                        @ 080d5b82 6889
    subs r0,#0x1    @ 080d5b84 0138
    ldrh r2,[r5,#0x1a]                       @ 080d5b86 6a8b
    cmp r2,r0                                @ 080d5b88 8242
    bge LAB_080d5bb8                         @ 080d5b8a 15da
    bl tick_pack_card_image_scroll_forward   @ 080d5b8c fff704f8
    movs r0,#0x0    @ 080d5b90 0020
    .hword 0x4681    @ 080d5b92 8146
    movs r7,#0x0    @ 080d5b94 0027
    bl sync_state_and_init_sprite            @ 080d5b96 23f08dff
    ldr r1, DAT_080d5bb4                     @ 080d5b9a 0649
    adds r2,r4,r1    @ 080d5b9c 6218
    movs r0,#0x21    @ 080d5b9e 2120
    rsbs r0,r0,#0    @ 080d5ba0 4042
    ldrb r1,[r2,#0x0]                        @ 080d5ba2 1178
    ands r0,r1    @ 080d5ba4 0840
    movs r1,#0x11    @ 080d5ba6 1121
    rsbs r1,r1,#0    @ 080d5ba8 4942
    ands r0,r1    @ 080d5baa 0840
    strb r0,[r2,#0x0]                        @ 080d5bac 1070
    movs r0,#0x3    @ 080d5bae 0320
    b LAB_080d5c3a                           @ 080d5bb0 43e0
    .zero  0x2
DAT_080d5bb4:
    .word  0x00000724                     @ 080d5bb4 24070000
LAB_080d5bb8:
    ldr r2, DAT_080d5bc0                     @ 080d5bb8 014a
    adds r4,r4,r2    @ 080d5bba a418
    b LAB_080d5c4a                           @ 080d5bbc 45e0
    .zero  0x2
DAT_080d5bc0:
    .word  0x00000724                     @ 080d5bc0 24070000
LAB_080d5bc4:
    movs r0,#0x40    @ 080d5bc4 4020
    ands r0,r1    @ 080d5bc6 0840
    cmp r0,#0x0                              @ 080d5bc8 0028
    beq LAB_080d5c08                         @ 080d5bca 1dd0
    ldrh r0,[r5,#0x1a]                       @ 080d5bcc 688b
    cmp r0,#0x0                              @ 080d5bce 0028
    beq LAB_080d5bfc                         @ 080d5bd0 14d0
    bl tick_pack_card_image_scroll_back      @ 080d5bd2 fff741f8
    movs r0,#0x0    @ 080d5bd6 0020
    .hword 0x4681    @ 080d5bd8 8146
    movs r7,#0x0    @ 080d5bda 0027
    bl sync_state_and_init_sprite            @ 080d5bdc 23f06aff
    ldr r1, DAT_080d5bf8                     @ 080d5be0 0549
    adds r2,r4,r1    @ 080d5be2 6218
    movs r0,#0x21    @ 080d5be4 2120
    rsbs r0,r0,#0    @ 080d5be6 4042
    ldrb r1,[r2,#0x0]                        @ 080d5be8 1178
    ands r0,r1    @ 080d5bea 0840
    movs r1,#0x11    @ 080d5bec 1121
    rsbs r1,r1,#0    @ 080d5bee 4942
    ands r0,r1    @ 080d5bf0 0840
    strb r0,[r2,#0x0]                        @ 080d5bf2 1070
    movs r0,#0x3    @ 080d5bf4 0320
    b LAB_080d5c3a                           @ 080d5bf6 20e0
DAT_080d5bf8:
    .word  0x00000724                     @ 080d5bf8 24070000
LAB_080d5bfc:
    ldr r2, DAT_080d5c04                     @ 080d5bfc 014a
    adds r4,r4,r2    @ 080d5bfe a418
    b LAB_080d5c4a                           @ 080d5c00 23e0
    .zero  0x2
DAT_080d5c04:
    .word  0x00000724                     @ 080d5c04 24070000
LAB_080d5c08:
    movs r0,#0x10    @ 080d5c08 1020
    ands r0,r1    @ 080d5c0a 0840
    cmp r0,#0x0                              @ 080d5c0c 0028
    beq LAB_080d5c62                         @ 080d5c0e 28d0
    ldrh r0,[r5,#0x1a]                       @ 080d5c10 688b
    ldrh r1,[r5,#0xa]                        @ 080d5c12 6989
    cmp r0,r1                                @ 080d5c14 8842
    bcs LAB_080d5c44                         @ 080d5c16 15d2
    adds r0,r3,#0x0    @ 080d5c18 181c
    ands r0,r2    @ 080d5c1a 1040
    cmp r0,#0x0                              @ 080d5c1c 0028
    beq LAB_080d5c44                         @ 080d5c1e 11d0
    bl init_pack_scroll_blend_and_window_regs @ 080d5c20 fff7a4fe
    movs r0,#0x24    @ 080d5c24 2420
    bl sync_state_and_init_sprite            @ 080d5c26 23f045ff
    ldr r2, DAT_080d5c40                     @ 080d5c2a 054a
    adds r0,r4,r2    @ 080d5c2c a018
    movs r1,#0x21    @ 080d5c2e 2121
    rsbs r1,r1,#0    @ 080d5c30 4942
    ldrb r2,[r0,#0x0]                        @ 080d5c32 0278
    ands r1,r2    @ 080d5c34 1140
    strb r1,[r0,#0x0]                        @ 080d5c36 0170
    movs r0,#0xc    @ 080d5c38 0c20
LAB_080d5c3a:
    strh r0,[r5,#0x4]                        @ 080d5c3a a880
    movs r6,#0x1    @ 080d5c3c 0126
    b LAB_080d5c62                           @ 080d5c3e 10e0
DAT_080d5c40:
    .word  0x00000724                     @ 080d5c40 24070000
LAB_080d5c44:
    movs r0,#0xe3    @ 080d5c44 e320
    lsls r0,r0,#0x3    @ 080d5c46 c000
    adds r4,r5,r0    @ 080d5c48 2c18
LAB_080d5c4a:
    movs r0,#0x20    @ 080d5c4a 2020
    ldrb r1,[r4,#0x0]                        @ 080d5c4c 2178
    ands r0,r1    @ 080d5c4e 0840
    cmp r0,#0x0                              @ 080d5c50 0028
    bne LAB_080d5c62                         @ 080d5c52 06d1
    movs r0,#0x2    @ 080d5c54 0220
    bl sync_state_and_init_sprite            @ 080d5c56 23f02dff
    movs r0,#0x20    @ 080d5c5a 2020
    ldrb r2,[r4,#0x0]                        @ 080d5c5c 2278
    orrs r0,r2    @ 080d5c5e 1043
    strb r0,[r4,#0x0]                        @ 080d5c60 2070
LAB_080d5c62:
    cmp r6,#0x1                              @ 080d5c62 012e
    beq LAB_080d5c78                         @ 080d5c64 08d0
    ldr r0, PTR_gPrng_080d5cec               @ 080d5c66 2148
    movs r2,#0xa3    @ 080d5c68 a322
    lsls r2,r2,#0x1    @ 080d5c6a 5200
    adds r1,r0,r2    @ 080d5c6c 8118
    movs r0,#0xf0    @ 080d5c6e f020
    ldrh r1,[r1,#0x0]                        @ 080d5c70 0988
    ands r0,r1    @ 080d5c72 0840
    cmp r0,#0x0                              @ 080d5c74 0028
    bne LAB_080d5c88                         @ 080d5c76 07d1
LAB_080d5c78:
    movs r0,#0xe3    @ 080d5c78 e320
    lsls r0,r0,#0x3    @ 080d5c7a c000
    adds r1,r5,r0    @ 080d5c7c 2918
    movs r0,#0x21    @ 080d5c7e 2120
    rsbs r0,r0,#0    @ 080d5c80 4042
    ldrb r2,[r1,#0x0]                        @ 080d5c82 0a78
    ands r0,r2    @ 080d5c84 1040
    strb r0,[r1,#0x0]                        @ 080d5c86 0870
LAB_080d5c88:
    .hword 0x4654    @ 080d5c88 5446
    adds r4,#0x1    @ 080d5c8a 0134
    adds r0,r4,#0x0    @ 080d5c8c 201c
    bl render_pack_card_highlight_sprite     @ 080d5c8e fff79dfc
    .hword 0x4648    @ 080d5c92 4846
    cmp r0,#0x1                              @ 080d5c94 0128
    bne LAB_080d5ca0                         @ 080d5c96 03d1
    adds r0,r4,#0x0    @ 080d5c98 201c
    movs r1,#0x0    @ 080d5c9a 0021
    bl render_pack_card_spin_oam_by_mode     @ 080d5c9c fff7e8fb
LAB_080d5ca0:
    adds r0,r4,#0x0    @ 080d5ca0 201c
    bl render_pack_card_sprite_by_flip_state @ 080d5ca2 fef701fd
    ldrh r1,[r5,#0x1a]                       @ 080d5ca6 698b
    ldrh r2,[r5,#0xa]                        @ 080d5ca8 6a89
    cmp r1,r2                                @ 080d5caa 9142
    bcs LAB_080d5cc2                         @ 080d5cac 09d2
    cmp r7,#0x1                              @ 080d5cae 012f
    bne LAB_080d5cc2                         @ 080d5cb0 07d1
    movs r1,#0xdf    @ 080d5cb2 df21
    lsls r1,r1,#0x3    @ 080d5cb4 c900
    adds r0,r5,r1    @ 080d5cb6 6818
    ldr r1,[r0,#0x0]                         @ 080d5cb8 0168
    .hword 0x4640    @ 080d5cba 4046
    movs r2,#0x2    @ 080d5cbc 0222
    bl tick_pack_aob_frame_loop              @ 080d5cbe fff755fb
LAB_080d5cc2:
    .hword 0x4650    @ 080d5cc2 5046
    adds r0,#0x3    @ 080d5cc4 0330
    bl render_pack_card_slot_oam             @ 080d5cc6 fff75dfa
    movs r2,#0xe3    @ 080d5cca e322
    lsls r2,r2,#0x3    @ 080d5ccc d200
    adds r0,r5,r2    @ 080d5cce a818
    ldrb r0,[r0,#0x0]                        @ 080d5cd0 0078
    lsls r0,r0,#0x19    @ 080d5cd2 4006
    lsrs r0,r0,#0x1f    @ 080d5cd4 c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d5cd6 fff735f9
    adds r0,r6,#0x0    @ 080d5cda 301c
    pop {r3,r4,r5}                           @ 080d5cdc 38bc
    .hword 0x4698    @ 080d5cde 9846
    .hword 0x46a1    @ 080d5ce0 a146
    .hword 0x46aa    @ 080d5ce2 aa46
    pop {r4,r5,r6,r7}                        @ 080d5ce4 f0bc
    pop {r1}                                 @ 080d5ce6 02bc
    bx r1                                    @ 080d5ce8 0847
    .zero  0x2
PTR_gPrng_080d5cec:
    .word  gPrng                          @ 080d5cec 40000003

@ 拆包场景卡片色相滚动插值帧驱动. 从 pack_ui_state+0x4c (偏移) 读帧计数器并递减; 取 [+0x3a] - [+0x3c] (目标值 - 当前值) 差值乘以 counter, 除以 8 得到增量; 加到 [+0x3c] (当前色相位置) 并截断到 0xff 写回 [+0x3e]. 当计数器归零时: 写 pack_ui_state+0xc+0x4=4, 将 [+0x3a]/[+0x3c] 清零, 置 r6=1 返回完成. 末尾调 render_pack_card_sprite_by_flip_state(1) + render_pack_card_slot_oam(3) + tick_pack_name_scroll_strip_row0(pack_ui_state+0x724 bit6). 此为 pack 卡片展示列表页的色相插值状态处理器.
tick_pack_card_hue_scroll_interp:
    push {r4,r5,r6,r7,lr}                    @ 080d5cf0 f0b5
    ldr r7, DAT_080d5d5c                     @ 080d5cf2 1a4f
    adds r5,r7,#0x0    @ 080d5cf4 3d1c
    adds r5,#0xc    @ 080d5cf6 0c35
    movs r6,#0x0    @ 080d5cf8 0026
    adds r4,r7,#0x0    @ 080d5cfa 3c1c
    adds r4,#0x4c    @ 080d5cfc 4c34
    ldrh r0,[r4,#0x0]                        @ 080d5cfe 2088
    subs r0,#0x1    @ 080d5d00 0138
    strh r0,[r4,#0x0]                        @ 080d5d02 2080
    movs r1,#0x3a    @ 080d5d04 3a21
    ldrsh r0,[r5,r1]                         @ 080d5d06 685e
    movs r2,#0x3c    @ 080d5d08 3c22
    ldrsh r1,[r5,r2]                         @ 080d5d0a a95e
    subs r0,r0,r1    @ 080d5d0c 401a
    movs r2,#0x0    @ 080d5d0e 0022
    ldrsh r1,[r4,r2]                         @ 080d5d10 a15e
    muls r0,r1    @ 080d5d12 4843
    movs r1,#0x8    @ 080d5d14 0821
    bl bios_div                              @ 080d5d16 38f071fb
    movs r2,#0x3c    @ 080d5d1a 3c22
    ldrsh r1,[r5,r2]                         @ 080d5d1c a95e
    adds r1,r1,r0    @ 080d5d1e 0918
    movs r0,#0xff    @ 080d5d20 ff20
    ands r1,r0    @ 080d5d22 0140
    strh r1,[r5,#0x3e]                       @ 080d5d24 e987
    movs r1,#0x0    @ 080d5d26 0021
    ldrsh r0,[r4,r1]                         @ 080d5d28 605e
    cmp r0,#0x0                              @ 080d5d2a 0028
    bne LAB_080d5d38                         @ 080d5d2c 04d1
    movs r0,#0x4    @ 080d5d2e 0420
    strh r0,[r5,#0x4]                        @ 080d5d30 a880
    strh r6,[r5,#0x3a]                       @ 080d5d32 6e87
    strh r6,[r5,#0x3c]                       @ 080d5d34 ae87
    movs r6,#0x1    @ 080d5d36 0126
LAB_080d5d38:
    movs r0,#0x1    @ 080d5d38 0120
    bl render_pack_card_sprite_by_flip_state @ 080d5d3a fef7b5fc
    movs r0,#0x3    @ 080d5d3e 0320
    bl render_pack_card_slot_oam             @ 080d5d40 fff720fa
    ldr r2, DAT_080d5d60                     @ 080d5d44 064a
    adds r0,r7,r2    @ 080d5d46 b818
    ldrb r0,[r0,#0x0]                        @ 080d5d48 0078
    lsls r0,r0,#0x19    @ 080d5d4a 4006
    lsrs r0,r0,#0x1f    @ 080d5d4c c00f
    bl tick_pack_name_scroll_strip_row0      @ 080d5d4e fff7f9f8
    adds r0,r6,#0x0    @ 080d5d52 301c
    pop {r4,r5,r6,r7}                        @ 080d5d54 f0bc
    pop {r1}                                 @ 080d5d56 02bc
    bx r1                                    @ 080d5d58 0847
    .zero  0x2
DAT_080d5d5c:
    .word  pack_ui_state                  @ 080d5d5c 50580003
DAT_080d5d60:
    .word  0x00000724                     @ 080d5d60 24070000

@ 拆包场景卡片静态展示帧渲染. 入口保存 r8/r9 至高寄存器. 从 pack_ui_state [+0x6fc]/[+0x704]/[+0x6fa] 取卡组指针, 渲染状态指针和 slot_index, 组合得到当前卡槽描述符指针 r7. 读卡槽状态字节 [pack_ui_state+0x724] bit6 (toggle_dir), 取反后写入 bit6 并更新 bit0 (new_dir); 调 render_pack_name_to_obj_sprite_row 渲染卡名精灵行. 后续读 [+0x725] 字节处理 owned_count 方向位 (bit1) 和 label_name 方向位 (bit0), 分别调 render_pack_owned_count_to_sprite_row / render_pack_label_name_to_sprite_row. 最后检查 bit4 决定调 render_pack_label_text_by_flags 还是 render_pack_label_text_default_pair; 若 bit7 置位则写 BLDALPHA=0x10 并调 dispatch_pack_aob_frame_loop_by_reset. 末尾 render_pack_card_highlight_sprite(1) / render_pack_card_sprite_by_flip_state(1) / render_pack_card_slot_oam(3). 固定返回 r0=1 (写 [+0x10] 0x2/0xe 状态更新).
render_pack_card_static_frame:
    push {r4,r5,r6,r7,lr}                    @ 080d5d64 f0b5
    .hword 0x464f    @ 080d5d66 4f46
    .hword 0x4646    @ 080d5d68 4646
    push {r6,r7}                             @ 080d5d6a c0b4
    ldr r4, DAT_080d5e0c                     @ 080d5d6c 274c
    movs r0,#0xc    @ 080d5d6e 0c20
    adds r0,r0,r4    @ 080d5d70 0019
    .hword 0x4681    @ 080d5d72 8146
    ldr r1, DAT_080d5e10                     @ 080d5d74 2649
    adds r2,r4,r1    @ 080d5d76 6218
    subs r1,#0x2    @ 080d5d78 0239
    adds r0,r4,r1    @ 080d5d7a 6018
    ldrh r0,[r0,#0x0]                        @ 080d5d7c 0088
    lsls r1,r0,#0x2    @ 080d5d7e 8100
    ldr r0,[r2,#0x0]                         @ 080d5d80 1068
    adds r7,r0,r1    @ 080d5d82 4718
    ldr r1, DAT_080d5e14                     @ 080d5d84 2349
    adds r0,r4,r1    @ 080d5d86 6018
    ldr r0,[r0,#0x0]                         @ 080d5d88 0068
    .hword 0x4680    @ 080d5d8a 8046
    ldr r0, DAT_080d5e18                     @ 080d5d8c 2248
    adds r6,r4,r0    @ 080d5d8e 2618
    ldrb r2,[r6,#0x0]                        @ 080d5d90 3278
    lsls r0,r2,#0x19    @ 080d5d92 5006
    lsrs r0,r0,#0x1f    @ 080d5d94 c00f
    movs r5,#0x1    @ 080d5d96 0125
    eors r0,r5    @ 080d5d98 6840
    lsls r0,r0,#0x6    @ 080d5d9a 8001
    movs r1,#0x41    @ 080d5d9c 4121
    rsbs r1,r1,#0    @ 080d5d9e 4942
    ands r1,r2    @ 080d5da0 1140
    orrs r1,r0    @ 080d5da2 0143
    strb r1,[r6,#0x0]                        @ 080d5da4 3170
    ldr r0,[r7,#0x0]                         @ 080d5da6 3868
    lsls r0,r0,#0x19    @ 080d5da8 4006
    lsrs r0,r0,#0x19    @ 080d5daa 400e
    lsls r1,r1,#0x19    @ 080d5dac 4906
    lsrs r1,r1,#0x1f    @ 080d5dae c90f
    bl render_pack_name_to_obj_sprite_row    @ 080d5db0 fef7f2ff
    ldr r1, DAT_080d5e1c                     @ 080d5db4 1949
    adds r4,r4,r1    @ 080d5db6 6418
    ldrb r2,[r4,#0x0]                        @ 080d5db8 2278
    lsls r0,r2,#0x1e    @ 080d5dba 9007
    lsrs r0,r0,#0x1f    @ 080d5dbc c00f
    eors r0,r5    @ 080d5dbe 6840
    lsls r0,r0,#0x1    @ 080d5dc0 4000
    movs r1,#0x3    @ 080d5dc2 0321
    rsbs r1,r1,#0    @ 080d5dc4 4942
    ands r1,r2    @ 080d5dc6 1140
    orrs r1,r0    @ 080d5dc8 0143
    strb r1,[r4,#0x0]                        @ 080d5dca 2170
    ldr r0,[r7,#0x0]                         @ 080d5dcc 3868
    lsls r0,r0,#0x19    @ 080d5dce 4006
    lsrs r0,r0,#0x19    @ 080d5dd0 400e
    lsls r1,r1,#0x1e    @ 080d5dd2 8907
    lsrs r1,r1,#0x1f    @ 080d5dd4 c90f
    bl render_pack_owned_count_to_sprite_row @ 080d5dd6 fff737f8
    ldrb r2,[r4,#0x0]                        @ 080d5dda 2278
    lsls r0,r2,#0x1f    @ 080d5ddc d007
    lsrs r0,r0,#0x1f    @ 080d5dde c00f
    eors r5,r0    @ 080d5de0 4540
    movs r1,#0x2    @ 080d5de2 0221
    rsbs r1,r1,#0    @ 080d5de4 4942
    ands r1,r2    @ 080d5de6 1140
    orrs r1,r5    @ 080d5de8 2943
    strb r1,[r4,#0x0]                        @ 080d5dea 2170
    ldr r0,[r7,#0x0]                         @ 080d5dec 3868
    lsls r0,r0,#0x19    @ 080d5dee 4006
    lsrs r0,r0,#0x19    @ 080d5df0 400e
    lsls r1,r1,#0x1f    @ 080d5df2 c907
    lsrs r1,r1,#0x1f    @ 080d5df4 c90f
    bl render_pack_label_name_to_sprite_row  @ 080d5df6 fff749f8
    movs r0,#0x10    @ 080d5dfa 1020
    ldrb r6,[r6,#0x0]                        @ 080d5dfc 3678
    ands r0,r6    @ 080d5dfe 3040
    cmp r0,#0x0                              @ 080d5e00 0028
    bne LAB_080d5e20                         @ 080d5e02 0dd1
    adds r0,r7,#0x0    @ 080d5e04 381c
    bl render_pack_label_text_by_flags       @ 080d5e06 fef78ffe
    b LAB_080d5e24                           @ 080d5e0a 0be0
DAT_080d5e0c:
    .word  pack_ui_state                  @ 080d5e0c 50580003
DAT_080d5e10:
    .word  0x000006fc                     @ 080d5e10 fc060000
DAT_080d5e14:
    .word  0x00000704                     @ 080d5e14 04070000
DAT_080d5e18:
    .word  0x00000724                     @ 080d5e18 24070000
DAT_080d5e1c:
    .word  0x00000725                     @ 080d5e1c 25070000
LAB_080d5e20:
    bl render_pack_label_text_default_pair   @ 080d5e20 fef7aefe
LAB_080d5e24:
    movs r0,#0x80    @ 080d5e24 8020
    ldrb r1,[r7,#0x0]                        @ 080d5e26 3978
    ands r0,r1    @ 080d5e28 0840
    cmp r0,#0x0                              @ 080d5e2a 0028
    beq LAB_080d5e3c                         @ 080d5e2c 06d0
    ldr r1, PTR_BLDALPHA_080d5e64            @ 080d5e2e 0d49
    movs r0,#0x10    @ 080d5e30 1020
    strh r0,[r1,#0x0]                        @ 080d5e32 0880
    adds r0,r7,#0x0    @ 080d5e34 381c
    .hword 0x4641    @ 080d5e36 4146
    bl dispatch_pack_aob_frame_loop_by_reset @ 080d5e38 fff7f6fa
LAB_080d5e3c:
    movs r0,#0x1    @ 080d5e3c 0120
    bl render_pack_card_highlight_sprite     @ 080d5e3e fff7c5fb
    movs r0,#0x1    @ 080d5e42 0120
    bl render_pack_card_sprite_by_flip_state @ 080d5e44 fef730fc
    movs r0,#0x3    @ 080d5e48 0320
    bl render_pack_card_slot_oam             @ 080d5e4a fff79bf9
    movs r1,#0xe3    @ 080d5e4e e321
    lsls r1,r1,#0x3    @ 080d5e50 c900
    add r1,r9                                @ 080d5e52 4944
    movs r0,#0x10    @ 080d5e54 1020
    ldrb r1,[r1,#0x0]                        @ 080d5e56 0978
    ands r0,r1    @ 080d5e58 0840
    cmp r0,#0x0                              @ 080d5e5a 0028
    bne LAB_080d5e6c                         @ 080d5e5c 06d1
    ldr r1, DAT_080d5e68                     @ 080d5e5e 0249
    movs r0,#0x2    @ 080d5e60 0220
    b LAB_080d5e70                           @ 080d5e62 05e0
PTR_BLDALPHA_080d5e64:
    .word  BLDALPHA                       @ 080d5e64 52000004
DAT_080d5e68:
    .word  pack_ui_state                  @ 080d5e68 50580003
LAB_080d5e6c:
    ldr r1, DAT_080d5e80                     @ 080d5e6c 0449
    movs r0,#0xe    @ 080d5e6e 0e20
LAB_080d5e70:
    strh r0,[r1,#0x10]                       @ 080d5e70 0882
    movs r0,#0x1    @ 080d5e72 0120
    pop {r3,r4}                              @ 080d5e74 18bc
    .hword 0x4698    @ 080d5e76 9846
    .hword 0x46a1    @ 080d5e78 a146
    pop {r4,r5,r6,r7}                        @ 080d5e7a f0bc
    pop {r1}                                 @ 080d5e7c 02bc
    bx r1                                    @ 080d5e7e 0847
DAT_080d5e80:
    .word  pack_ui_state                  @ 080d5e80 50580003

