@ ==== 15_equip_target_summon_zoom.s ====
@ 装备目标选择 + 召唤资格 + 卡牌放大 OAM 网格
.thumb
@ 装备目标选择核心函数, 优先选择卡牌在 eligible_set 内的槽位, 失败后多级回退. 入口 r0=player_id (.hword 0x4680=mov r8,r0), r1=slot_bitmap (sp[0x50]), r2=eligible_set 指针 (sp[0x54]). 第一阶段: 收集 bitmap 中全部 [0..10] 槽位候选, Fisher-Yates shuffle; 遍历每个候选从 gP1LifePoints slot word 提取 card_icid, 调用 check_card_id_in_eligible_set 命中则立即返回该 slot_idx. 第二阶段 (chain=3 特殊逻辑): 检查 [gP1LifePoints+0x1cf4]==3 且 [+0x1ce8]==r8; 满足时重新扫 bitmap 找可激活槽 (check_slot_card_activatable), 调用 find_best_scored_slot_from_bitmap 并按 LP 阈值 (0xaf*8=0x578) 判断; 若分数满足返回. 第三阶段: 调用 find_best_scored_slot_from_bitmap(mode=1) 再次尝试; 最终 fallback 调用 sample_random_monster_slot_with_field9_filter. Side effects: 无外部写入. Constants: CHAIN_LIMIT=3, LP_THRESHOLD=0x578, GY=gP1LifePoints, SLOT_MAX=10.
select_equip_target_slot_with_eligibility_check:
    push {r4,r5,r6,r7,lr}                    @ 080b5348 f0b5
    .hword 0x4657    @ 080b534a 5746
    .hword 0x464e    @ 080b534c 4e46
    .hword 0x4645    @ 080b534e 4546
    push {r5,r6,r7}                          @ 080b5350 e0b4
    sub sp,#0x60                             @ 080b5352 98b0
    .hword 0x4680    @ 080b5354 8046
    str r1,[sp,#0x50]                        @ 080b5356 1491
    str r2,[sp,#0x54]                        @ 080b5358 1592
    movs r0,#0x0    @ 080b535a 0020
    .hword 0x4681    @ 080b535c 8146
    movs r5,#0x0    @ 080b535e 0025
    .hword 0x4641    @ 080b5360 4146
    lsls r2,r1,#0x4    @ 080b5362 0a01
    movs r4,#0x1    @ 080b5364 0124
    str r2,[sp,#0x5c]                        @ 080b5366 1792
    .hword 0x466b    @ 080b5368 6b46
LAB_080b536a:
    adds r1,r2,r5    @ 080b536a 5119
    adds r0,r4,#0x0    @ 080b536c 201c
    lsls r0,r1    @ 080b536e 8840
    ldr r1,[sp,#0x50]                        @ 080b5370 1499
    ands r0,r1    @ 080b5372 0840
    cmp r0,#0x0                              @ 080b5374 0028
    beq LAB_080b537e                         @ 080b5376 02d0
    stmia r3!,{r5}                           @ 080b5378 20c3
    movs r0,#0x1    @ 080b537a 0120
    add r9,r0                                @ 080b537c 8144
LAB_080b537e:
    adds r5,#0x1    @ 080b537e 0135
    cmp r5,#0xa                              @ 080b5380 0a2d
    ble LAB_080b536a                         @ 080b5382 f2dd
    .hword 0x464d    @ 080b5384 4d46
    subs r5,#0x1    @ 080b5386 013d
    cmp r5,#0x0                              @ 080b5388 002d
    ble LAB_080b53ae                         @ 080b538a 10dd
    lsls r0,r5,#0x2    @ 080b538c a800
    .hword 0x4669    @ 080b538e 6946
    adds r4,r0,r1    @ 080b5390 4418
LAB_080b5392:
    adds r0,r5,#0x1    @ 080b5392 681c
    bl sample_prng_scaled                    @ 080b5394 dff766f9
    ldr r2,[r4,#0x0]                         @ 080b5398 2268
    lsls r0,r0,#0x2    @ 080b539a 8000
    .hword 0x466b    @ 080b539c 6b46
    adds r1,r3,r0    @ 080b539e 1918
    ldr r0,[r1,#0x0]                         @ 080b53a0 0868
    str r0,[r4,#0x0]                         @ 080b53a2 2060
    str r2,[r1,#0x0]                         @ 080b53a4 0a60
    subs r4,#0x4    @ 080b53a6 043c
    subs r5,#0x1    @ 080b53a8 013d
    cmp r5,#0x0                              @ 080b53aa 002d
    bgt LAB_080b5392                         @ 080b53ac f1dc
LAB_080b53ae:
    movs r5,#0x0    @ 080b53ae 0025
    cmp r5,r9                                @ 080b53b0 4d45
    bge LAB_080b5402                         @ 080b53b2 26da
    ldr r7, PTR_gP1LifePoints_080b5494       @ 080b53b4 374f
    movs r0,#0x1    @ 080b53b6 0120
    .hword 0x4682    @ 080b53b8 8246
    .hword 0x4641    @ 080b53ba 4146
    ands r1,r0    @ 080b53bc 0140
    .hword 0x466e    @ 080b53be 6e46
    ldr r0, DAT_080b5498                     @ 080b53c0 3548
    adds r2,r1,#0x0    @ 080b53c2 0a1c
    muls r2,r0    @ 080b53c4 4243
    str r2,[sp,#0x58]                        @ 080b53c6 1692
LAB_080b53c8:
    ldr r4,[r6,#0x0]                         @ 080b53c8 3468
    lsls r0,r4,#0x2    @ 080b53ca a000
    adds r0,r0,r4    @ 080b53cc 0019
    lsls r0,r0,#0x2    @ 080b53ce 8000
    ldr r3,[sp,#0x58]                        @ 080b53d0 169b
    adds r1,r0,r3    @ 080b53d2 c118
    adds r0,r7,#0x0    @ 080b53d4 381c
    adds r0,#0x40    @ 080b53d6 4030
    adds r0,r1,r0    @ 080b53d8 0818
    ldr r0,[r0,#0x0]                         @ 080b53da 0068
    lsrs r0,r0,#0x7    @ 080b53dc c009
    .hword 0x4652    @ 080b53de 5246
    ands r0,r2    @ 080b53e0 1040
    cmp r0,#0x0                              @ 080b53e2 0028
    beq LAB_080b53fa                         @ 080b53e4 09d0
    ldr r3, DAT_080b549c                     @ 080b53e6 2d4b
    adds r0,r1,r3    @ 080b53e8 c818
    ldr r0,[r0,#0x0]                         @ 080b53ea 0068
    lsls r0,r0,#0x13    @ 080b53ec c004
    lsrs r0,r0,#0x13    @ 080b53ee c00c
    ldr r1,[sp,#0x54]                        @ 080b53f0 1599
    bl check_card_id_in_eligible_set         @ 080b53f2 faf79ff8
    cmp r0,#0x0                              @ 080b53f6 0028
    bne LAB_080b54a8                         @ 080b53f8 56d1
LAB_080b53fa:
    adds r6,#0x4    @ 080b53fa 0436
    adds r5,#0x1    @ 080b53fc 0135
    cmp r5,r9                                @ 080b53fe 4d45
    blt LAB_080b53c8                         @ 080b5400 e2db
LAB_080b5402:
    ldr r1, PTR_gP1LifePoints_080b5494       @ 080b5402 2449
    ldr r2, DAT_080b54a0                     @ 080b5404 264a
    adds r0,r1,r2    @ 080b5406 8818
    ldr r0,[r0,#0x0]                         @ 080b5408 0068
    cmp r0,#0x3                              @ 080b540a 0328
    bne LAB_080b5478                         @ 080b540c 34d1
    ldr r3, DAT_080b54a4                     @ 080b540e 254b
    adds r0,r1,r3    @ 080b5410 c818
    ldr r0,[r0,#0x0]                         @ 080b5412 0068
    cmp r0,r8                                @ 080b5414 4045
    bne LAB_080b5478                         @ 080b5416 2fd1
    movs r6,#0x0    @ 080b5418 0026
    movs r5,#0x0    @ 080b541a 0025
LAB_080b541c:
    ldr r1,[sp,#0x5c]                        @ 080b541c 1799
    adds r0,r1,r5    @ 080b541e 4819
    movs r4,#0x1    @ 080b5420 0124
    lsls r4,r0    @ 080b5422 8440
    ldr r0,[sp,#0x50]                        @ 080b5424 1498
    ands r0,r4    @ 080b5426 2040
    cmp r0,#0x0                              @ 080b5428 0028
    beq LAB_080b543c                         @ 080b542a 07d0
    .hword 0x4640    @ 080b542c 4046
    adds r1,r5,#0x0    @ 080b542e 291c
    movs r2,#0x1    @ 080b5430 0122
    bl check_slot_card_activatable           @ 080b5432 7ff7bdfa
    cmp r0,#0x0                              @ 080b5436 0028
    beq LAB_080b543c                         @ 080b5438 00d0
    orrs r6,r4    @ 080b543a 2643
LAB_080b543c:
    adds r5,#0x1    @ 080b543c 0135
    cmp r5,#0xa                              @ 080b543e 0a2d
    ble LAB_080b541c                         @ 080b5440 ecdd
    .hword 0x4640    @ 080b5442 4046
    adds r1,r6,#0x0    @ 080b5444 311c
    movs r2,#0x1    @ 080b5446 0122
    movs r3,#0x0    @ 080b5448 0023
    bl find_best_scored_slot_from_bitmap     @ 080b544a fff75dfc
    adds r5,r0,#0x0    @ 080b544e 051c
    cmp r5,#0x0                              @ 080b5450 002d
    blt LAB_080b5478                         @ 080b5452 11db
    add r4,sp,#0x2c                          @ 080b5454 0bac
    .hword 0x4640    @ 080b5456 4046
    adds r1,r5,#0x0    @ 080b5458 291c
    adds r2,r4,#0x0    @ 080b545a 221c
    bl dispatch_zone_slot_score_by_player_flag @ 080b545c f6f7d2fd
    ldr r2, PTR_gP1LifePoints_080b5494       @ 080b5460 0c4a
    movs r1,#0x1    @ 080b5462 0121
    .hword 0x4643    @ 080b5464 4346
    subs r0,r1,r3    @ 080b5466 c81a
    ands r0,r1    @ 080b5468 0840
    ldr r1, DAT_080b5498                     @ 080b546a 0b49
    muls r0,r1    @ 080b546c 4843
    adds r0,r0,r2    @ 080b546e 8018
    ldr r1,[r4,#0x14]                        @ 080b5470 6169
    ldr r0,[r0,#0x0]                         @ 080b5472 0068
    cmp r1,r0                                @ 080b5474 8142
    bge LAB_080b54ac                         @ 080b5476 19da
LAB_080b5478:
    .hword 0x4640    @ 080b5478 4046
    ldr r1,[sp,#0x50]                        @ 080b547a 1499
    movs r2,#0x1    @ 080b547c 0122
    movs r3,#0x1    @ 080b547e 0123
    bl find_best_scored_slot_from_bitmap     @ 080b5480 fff742fc
    adds r5,r0,#0x0    @ 080b5484 051c
    cmp r5,#0x0                              @ 080b5486 002d
    bge LAB_080b54ac                         @ 080b5488 10da
    .hword 0x4640    @ 080b548a 4046
    ldr r1,[sp,#0x50]                        @ 080b548c 1499
    bl sample_random_monster_slot_with_field9_filter @ 080b548e fff77ffe
    b LAB_080b54ae                           @ 080b5492 0ce0
PTR_gP1LifePoints_080b5494:
    .word  gP1LifePoints                  @ 080b5494 e0c40102
DAT_080b5498:
    .word  0x00000868                     @ 080b5498 68080000
DAT_080b549c:
    .word  0x0201c510                     @ 080b549c 10c50102
DAT_080b54a0:
    .word  0x00001cf4                     @ 080b54a0 f41c0000
DAT_080b54a4:
    .word  0x00001ce8                     @ 080b54a4 e81c0000
LAB_080b54a8:
    adds r0,r4,#0x0    @ 080b54a8 201c
    b LAB_080b54ae                           @ 080b54aa 00e0
LAB_080b54ac:
    adds r0,r5,#0x0    @ 080b54ac 281c
LAB_080b54ae:
    add sp,#0x60                             @ 080b54ae 18b0
    pop {r3,r4,r5}                           @ 080b54b0 38bc
    .hword 0x4698    @ 080b54b2 9846
    .hword 0x46a1    @ 080b54b4 a146
    .hword 0x46aa    @ 080b54b6 aa46
    pop {r4,r5,r6,r7}                        @ 080b54b8 f0bc
    pop {r1}                                 @ 080b54ba 02bc
    bx r1                                    @ 080b54bc 0847
    .zero  0x2

@ Filters slot_bitmap candidates by check_card_id_in_eligible_set whitelist, then picks best slot via find_best_scored_slot_from_bitmap or random via sample_random_slot_from_bitmap. Simplified variant of select_equip_target_slot_full (0x080b55ac): only whitelist-set-match phase. r0=player_id (-> sp[0x2c]), r1=slot_bitmap (-> r10 via .hword 0x468a=mov r10,r1). Phase 1: enumerate slots in bitmap to stack buffer; Fisher-Yates shuffle if count>1. Phase 2: check each candidate via check_card_id_in_eligible_set -> call find_best_scored_slot_from_bitmap; fallback to sample_random_slot_from_bitmap if result<0. Called by FUN_080b5d98, FUN_080b6c08, FUN_080b70ac on equip target selection path. Params: r0=player_id [0..1], r1=slot_bitmap [0..0x7ff]. Returns r0=s32 best_slot_idx [0..10] or -1. Side effects: none (pure computation). Constants: SLOT_MAX=10, gDuelFieldSlots=0x0201c510, player_stride=0x868.
select_equip_target_slot_by_eligible_set:
    push {r4,r5,r6,r7,lr}                    @ 080b54c0 f0b5
    .hword 0x4657    @ 080b54c2 5746
    .hword 0x464e    @ 080b54c4 4e46
    .hword 0x4645    @ 080b54c6 4546
    push {r5,r6,r7}                          @ 080b54c8 e0b4
    sub sp,#0x38                             @ 080b54ca 8eb0
    str r0,[sp,#0x2c]                        @ 080b54cc 0b90
    .hword 0x468a    @ 080b54ce 8a46
    movs r0,#0x0    @ 080b54d0 0020
    .hword 0x4680    @ 080b54d2 8046
    movs r7,#0x0    @ 080b54d4 0027
    movs r5,#0x0    @ 080b54d6 0025
    ldr r1,[sp,#0x2c]                        @ 080b54d8 0b99
    lsls r2,r1,#0x4    @ 080b54da 0a01
    movs r4,#0x1    @ 080b54dc 0124
    str r2,[sp,#0x34]                        @ 080b54de 0d92
    .hword 0x466b    @ 080b54e0 6b46
LAB_080b54e2:
    adds r1,r2,r5    @ 080b54e2 5119
    adds r0,r4,#0x0    @ 080b54e4 201c
    lsls r0,r1    @ 080b54e6 8840
    .hword 0x4651    @ 080b54e8 5146
    ands r0,r1    @ 080b54ea 0840
    cmp r0,#0x0                              @ 080b54ec 0028
    beq LAB_080b54f4                         @ 080b54ee 01d0
    stmia r3!,{r5}                           @ 080b54f0 20c3
    adds r7,#0x1    @ 080b54f2 0137
LAB_080b54f4:
    adds r5,#0x1    @ 080b54f4 0135
    cmp r5,#0xa                              @ 080b54f6 0a2d
    ble LAB_080b54e2                         @ 080b54f8 f3dd
    subs r5,r7,#0x1    @ 080b54fa 7d1e
    cmp r5,#0x0                              @ 080b54fc 002d
    ble LAB_080b5522                         @ 080b54fe 10dd
    lsls r0,r5,#0x2    @ 080b5500 a800
    .hword 0x466a    @ 080b5502 6a46
    adds r4,r0,r2    @ 080b5504 8418
LAB_080b5506:
    adds r0,r5,#0x1    @ 080b5506 681c
    bl sample_prng_scaled                    @ 080b5508 dff7acf8
    ldr r2,[r4,#0x0]                         @ 080b550c 2268
    lsls r0,r0,#0x2    @ 080b550e 8000
    .hword 0x466b    @ 080b5510 6b46
    adds r1,r3,r0    @ 080b5512 1918
    ldr r0,[r1,#0x0]                         @ 080b5514 0868
    str r0,[r4,#0x0]                         @ 080b5516 2060
    str r2,[r1,#0x0]                         @ 080b5518 0a60
    subs r4,#0x4    @ 080b551a 043c
    subs r5,#0x1    @ 080b551c 013d
    cmp r5,#0x0                              @ 080b551e 002d
    bgt LAB_080b5506                         @ 080b5520 f1dc
LAB_080b5522:
    cmp r7,#0x0                              @ 080b5522 002f
    ble LAB_080b5572                         @ 080b5524 25dd
    movs r0,#0x1    @ 080b5526 0120
    .hword 0x4681    @ 080b5528 8146
    ldr r0,[sp,#0x2c]                        @ 080b552a 0b98
    .hword 0x4649    @ 080b552c 4946
    ands r0,r1    @ 080b552e 0840
    .hword 0x466e    @ 080b5530 6e46
    ldr r1, DAT_080b55a4                     @ 080b5532 1c49
    adds r2,r0,#0x0    @ 080b5534 021c
    muls r2,r1    @ 080b5536 4a43
    str r2,[sp,#0x30]                        @ 080b5538 0c92
    adds r5,r7,#0x0    @ 080b553a 3d1c
LAB_080b553c:
    ldr r4,[r6,#0x0]                         @ 080b553c 3468
    lsls r0,r4,#0x2    @ 080b553e a000
    adds r0,r0,r4    @ 080b5540 0019
    lsls r0,r0,#0x2    @ 080b5542 8000
    ldr r3,[sp,#0x30]                        @ 080b5544 0c9b
    adds r0,r0,r3    @ 080b5546 c018
    ldr r1, DAT_080b55a8                     @ 080b5548 1749
    adds r0,r0,r1    @ 080b554a 4018
    ldr r0,[r0,#0x0]                         @ 080b554c 0068
    lsls r0,r0,#0x13    @ 080b554e c004
    lsrs r0,r0,#0x13    @ 080b5550 c00c
    movs r1,#0x0    @ 080b5552 0021
    bl check_card_id_in_eligible_set         @ 080b5554 f9f7eeff
    cmp r0,#0x0                              @ 080b5558 0028
    beq LAB_080b556a                         @ 080b555a 06d0
    ldr r0,[sp,#0x34]                        @ 080b555c 0d98
    adds r1,r0,r4    @ 080b555e 0119
    .hword 0x4648    @ 080b5560 4846
    lsls r0,r1    @ 080b5562 8840
    .hword 0x4641    @ 080b5564 4146
    orrs r1,r0    @ 080b5566 0143
    .hword 0x4688    @ 080b5568 8846
LAB_080b556a:
    adds r6,#0x4    @ 080b556a 0436
    subs r5,#0x1    @ 080b556c 013d
    cmp r5,#0x0                              @ 080b556e 002d
    bne LAB_080b553c                         @ 080b5570 e4d1
LAB_080b5572:
    .hword 0x4652    @ 080b5572 5246
    .hword 0x4643    @ 080b5574 4346
    eors r2,r3    @ 080b5576 5a40
    .hword 0x4690    @ 080b5578 9046
    movs r3,#0x1    @ 080b557a 0123
    rsbs r3,r3,#0    @ 080b557c 5b42
    ldr r0,[sp,#0x2c]                        @ 080b557e 0b98
    .hword 0x4641    @ 080b5580 4146
    adds r2,r3,#0x0    @ 080b5582 1a1c
    bl find_best_scored_slot_from_bitmap     @ 080b5584 fff7c0fb
    cmp r0,#0x0                              @ 080b5588 0028
    bge LAB_080b5594                         @ 080b558a 03da
    ldr r0,[sp,#0x2c]                        @ 080b558c 0b98
    .hword 0x4651    @ 080b558e 5146
    bl sample_random_slot_from_bitmap        @ 080b5590 fff7bafd
LAB_080b5594:
    add sp,#0x38                             @ 080b5594 0eb0
    pop {r3,r4,r5}                           @ 080b5596 38bc
    .hword 0x4698    @ 080b5598 9846
    .hword 0x46a1    @ 080b559a a146
    .hword 0x46aa    @ 080b559c aa46
    pop {r4,r5,r6,r7}                        @ 080b559e f0bc
    pop {r1}                                 @ 080b55a0 02bc
    bx r1                                    @ 080b55a2 0847
DAT_080b55a4:
    .word  0x00000868                     @ 080b55a4 68080000
DAT_080b55a8:
    .word  0x0201c510                     @ 080b55a8 10c50102

@ 装备目标选择完整版本, 对 bitmap 中所有候选槽位执行 4 轮类型/卡牌属性过滤后选出最优槽. 入口 r0=player_id (.hword 0x4682=mov r10,r0), r1=slot_bitmap (sp[0x50]), r2=mode (sp[0x54]), r3=equip_card_slot. 第一阶段: Fisher-Yates shuffle 全部 [0..10] 候选; 调用 check_slot_equip_eligibility_by_type 过滤; 过滤 field5<=6 (非高等级) 且有装备放置类型 (check_card_has_equip_placement_type) 且 field7 匹配的槽; 通过特定白名单卡牌 ID 检查 (0x11e4/0x0fd6/0x17e9/0x1874/0x1521/0x1798/0x14f3/0x163f). 第二阶段: 4 轮 count_equip_chain_default_flags 检查 (card_ids: 0x149d/0x1286/0x13f3/0x14b2). 第三阶段: check_card_id_in_eligible_set 白名单过滤 + orrs 构建 eligible_bitmap; 调用 find_best_scored_slot_from_bitmap 取最优; 若 mode!=0 则检查 LP 阈值 (0xaf*8=0x578); 最终 fallback 调用 sample_random_slot_from_bitmap. Side effects: 无外部写入. Constants: SLOT_MAX=10, LP_THR=0x578, CARD_WL=[0x11e4,0x0fd6,0x14f3,0x163f,0x17e9,0x1521,0x1798,0x1874,0x149d,0x1286,0x13f3,0x14b2].
select_equip_target_slot_full:
    push {r4,r5,r6,r7,lr}                    @ 080b55ac f0b5
    .hword 0x4657    @ 080b55ae 5746
    .hword 0x464e    @ 080b55b0 4e46
    .hword 0x4645    @ 080b55b2 4546
    push {r5,r6,r7}                          @ 080b55b4 e0b4
    sub sp,#0x74                             @ 080b55b6 9db0
    .hword 0x4682    @ 080b55b8 8246
    str r1,[sp,#0x50]                        @ 080b55ba 1491
    str r2,[sp,#0x54]                        @ 080b55bc 1592
    movs r0,#0x0    @ 080b55be 0020
    str r0,[sp,#0x58]                        @ 080b55c0 1690
    movs r1,#0x0    @ 080b55c2 0021
    str r1,[sp,#0x5c]                        @ 080b55c4 1791
    movs r6,#0x0    @ 080b55c6 0026
    .hword 0x4653    @ 080b55c8 5346
    lsls r2,r3,#0x4    @ 080b55ca 1a01
    movs r4,#0x1    @ 080b55cc 0124
    str r2,[sp,#0x70]                        @ 080b55ce 1c92
    .hword 0x466b    @ 080b55d0 6b46
LAB_080b55d2:
    adds r1,r2,r6    @ 080b55d2 9119
    adds r0,r4,#0x0    @ 080b55d4 201c
    lsls r0,r1    @ 080b55d6 8840
    ldr r1,[sp,#0x50]                        @ 080b55d8 1499
    ands r0,r1    @ 080b55da 0840
    cmp r0,#0x0                              @ 080b55dc 0028
    beq LAB_080b55e8                         @ 080b55de 03d0
    stmia r3!,{r6}                           @ 080b55e0 40c3
    ldr r0,[sp,#0x5c]                        @ 080b55e2 1798
    adds r0,#0x1    @ 080b55e4 0130
    str r0,[sp,#0x5c]                        @ 080b55e6 1790
LAB_080b55e8:
    adds r6,#0x1    @ 080b55e8 0136
    cmp r6,#0xa                              @ 080b55ea 0a2e
    ble LAB_080b55d2                         @ 080b55ec f1dd
    ldr r6,[sp,#0x5c]                        @ 080b55ee 179e
    subs r6,#0x1    @ 080b55f0 013e
    cmp r6,#0x0                              @ 080b55f2 002e
    ble LAB_080b5618                         @ 080b55f4 10dd
    lsls r0,r6,#0x2    @ 080b55f6 b000
    .hword 0x4669    @ 080b55f8 6946
    adds r4,r0,r1    @ 080b55fa 4418
LAB_080b55fc:
    adds r0,r6,#0x1    @ 080b55fc 701c
    bl sample_prng_scaled                    @ 080b55fe dff731f8
    ldr r2,[r4,#0x0]                         @ 080b5602 2268
    lsls r0,r0,#0x2    @ 080b5604 8000
    .hword 0x466b    @ 080b5606 6b46
    adds r1,r3,r0    @ 080b5608 1918
    ldr r0,[r1,#0x0]                         @ 080b560a 0868
    str r0,[r4,#0x0]                         @ 080b560c 2060
    str r2,[r1,#0x0]                         @ 080b560e 0a60
    subs r4,#0x4    @ 080b5610 043c
    subs r6,#0x1    @ 080b5612 013e
    cmp r6,#0x0                              @ 080b5614 002e
    bgt LAB_080b55fc                         @ 080b5616 f1dc
LAB_080b5618:
    movs r6,#0x0    @ 080b5618 0026
    ldr r0,[sp,#0x5c]                        @ 080b561a 1798
    cmp r6,r0                                @ 080b561c 8642
    bge LAB_080b563e                         @ 080b561e 0eda
    .hword 0x466d    @ 080b5620 6d46
LAB_080b5622:
    ldr r4,[r5,#0x0]                         @ 080b5622 2c68
    .hword 0x4650    @ 080b5624 5046
    adds r1,r4,#0x0    @ 080b5626 211c
    movs r2,#0x1    @ 080b5628 0122
    bl check_slot_equip_eligibility_by_type  @ 080b562a 80f7f3fc
    cmp r0,r10                               @ 080b562e 5045
    beq LAB_080b5634                         @ 080b5630 00d0
    b LAB_080b58d2                           @ 080b5632 4ee1
LAB_080b5634:
    adds r5,#0x4    @ 080b5634 0435
    adds r6,#0x1    @ 080b5636 0136
    ldr r1,[sp,#0x5c]                        @ 080b5638 1799
    cmp r6,r1                                @ 080b563a 8e42
    blt LAB_080b5622                         @ 080b563c f1db
LAB_080b563e:
    movs r6,#0x0    @ 080b563e 0026
    ldr r2,[sp,#0x5c]                        @ 080b5640 179a
    cmp r6,r2                                @ 080b5642 9642
    blt LAB_080b5648                         @ 080b5644 00db
    b LAB_080b574e                           @ 080b5646 82e0
LAB_080b5648:
    ldr r3, PTR_gP1LifePoints_080b56a4       @ 080b5648 164b
    str r3,[sp,#0x60]                        @ 080b564a 1893
    .hword 0x4650    @ 080b564c 5046
    movs r1,#0x1    @ 080b564e 0121
    ands r0,r1    @ 080b5650 0840
    str r3,[sp,#0x6c]                        @ 080b5652 1b93
    ldr r3, DAT_080b56a8                     @ 080b5654 144b
    adds r2,r0,#0x0    @ 080b5656 021c
    muls r2,r3    @ 080b5658 5a43
    str r2,[sp,#0x64]                        @ 080b565a 1992
LAB_080b565c:
    lsls r0,r6,#0x2    @ 080b565c b000
    add r0,sp                                @ 080b565e 6844
    ldr r0,[r0,#0x0]                         @ 080b5660 0068
    .hword 0x4681    @ 080b5662 8146
    lsls r0,r0,#0x2    @ 080b5664 8000
    add r0,r9                                @ 080b5666 4844
    lsls r0,r0,#0x2    @ 080b5668 8000
    ldr r2,[sp,#0x64]                        @ 080b566a 199a
    adds r1,r0,r2    @ 080b566c 8118
    ldr r0,[sp,#0x60]                        @ 080b566e 1898
    adds r0,#0x40    @ 080b5670 4030
    adds r0,r1,r0    @ 080b5672 0818
    ldr r0,[r0,#0x0]                         @ 080b5674 0068
    lsrs r0,r0,#0x5    @ 080b5676 4009
    movs r3,#0x1    @ 080b5678 0123
    ands r0,r3    @ 080b567a 1840
    cmp r0,#0x0                              @ 080b567c 0028
    bne LAB_080b5746                         @ 080b567e 62d1
    ldr r2, DAT_080b56ac                     @ 080b5680 0a4a
    adds r0,r1,r2    @ 080b5682 8818
    ldr r0,[r0,#0x0]                         @ 080b5684 0068
    lsls r0,r0,#0x13    @ 080b5686 c004
    lsrs r1,r0,#0x13    @ 080b5688 c10c
    ldr r0, DAT_080b56b0                     @ 080b568a 0948
    cmp r1,r0                                @ 080b568c 8142
    bgt LAB_080b56bc                         @ 080b568e 15dc
    subs r0,#0x1    @ 080b5690 0138
    cmp r1,r0                                @ 080b5692 8142
    bge LAB_080b56c8                         @ 080b5694 18da
    ldr r0, DAT_080b56b4                     @ 080b5696 0748
    cmp r1,r0                                @ 080b5698 8142
    beq LAB_080b56c8                         @ 080b569a 15d0
    ldr r0, DAT_080b56b8                     @ 080b569c 0648
    cmp r1,r0                                @ 080b569e 8142
    beq LAB_080b56c8                         @ 080b56a0 12d0
    b LAB_080b5746                           @ 080b56a2 50e0
PTR_gP1LifePoints_080b56a4:
    .word  gP1LifePoints                  @ 080b56a4 e0c40102
DAT_080b56a8:
    .word  0x00000868                     @ 080b56a8 68080000
DAT_080b56ac:
    .word  0x0201c510                     @ 080b56ac 10c50102
DAT_080b56b0:
    .word  0x000017e9                     @ 080b56b0 e9170000
DAT_080b56b4:
    .word  0x00001521                     @ 080b56b4 21150000
DAT_080b56b8:
    .word  0x00001798                     @ 080b56b8 98170000
LAB_080b56bc:
    ldr r0, DAT_080b578c                     @ 080b56bc 3348
    cmp r1,r0                                @ 080b56be 8142
    bgt LAB_080b5746                         @ 080b56c0 41dc
    subs r0,#0x1    @ 080b56c2 0138
    cmp r1,r0                                @ 080b56c4 8142
    blt LAB_080b5746                         @ 080b56c6 3edb
LAB_080b56c8:
    movs r7,#0x0    @ 080b56c8 0027
    ldr r2, DAT_080b5790                     @ 080b56ca 314a
    ldr r1,[sp,#0x6c]                        @ 080b56cc 1b99
    adds r1,#0xc    @ 080b56ce 0c31
    ldr r3,[sp,#0x64]                        @ 080b56d0 199b
    adds r0,r3,r1    @ 080b56d2 5818
    ldr r0,[r0,#0x0]                         @ 080b56d4 0068
    cmp r7,r0                                @ 080b56d6 8742
    bcs LAB_080b5746                         @ 080b56d8 35d2
    movs r0,#0x1    @ 080b56da 0120
    .hword 0x4653    @ 080b56dc 5346
    ands r3,r0    @ 080b56de 0340
    .hword 0x4698    @ 080b56e0 9846
    .hword 0x4649    @ 080b56e2 4946
    lsls r0,r1,#0x2    @ 080b56e4 8800
    add r0,r9                                @ 080b56e6 4844
    lsls r0,r0,#0x2    @ 080b56e8 8000
    str r0,[sp,#0x68]                        @ 080b56ea 1a90
LAB_080b56ec:
    lsls r0,r7,#0x2    @ 080b56ec b800
    .hword 0x4645    @ 080b56ee 4546
    muls r5,r2    @ 080b56f0 5543
    adds r0,r0,r5    @ 080b56f2 4019
    ldr r2, DAT_080b5794                     @ 080b56f4 274a
    adds r0,r0,r2    @ 080b56f6 8018
    ldr r0,[r0,#0x0]                         @ 080b56f8 0068
    lsls r0,r0,#0x13    @ 080b56fa c004
    lsrs r4,r0,#0x13    @ 080b56fc c40c
    adds r0,r4,#0x0    @ 080b56fe 201c
    bl get_card_extended_stat_field5         @ 080b5700 39f0a6fb
    cmp r0,#0x6                              @ 080b5704 0628
    ble LAB_080b5732                         @ 080b5706 14dd
    adds r0,r4,#0x0    @ 080b5708 201c
    bl check_card_has_equip_placement_type   @ 080b570a 96f7a5f9
    cmp r0,#0x0                              @ 080b570e 0028
    bne LAB_080b5732                         @ 080b5710 0fd1
    adds r0,r4,#0x0    @ 080b5712 201c
    bl get_card_extended_stat_field7         @ 080b5714 39f086fb
    adds r4,r0,#0x0    @ 080b5718 041c
    ldr r3,[sp,#0x68]                        @ 080b571a 1a9b
    adds r0,r3,r5    @ 080b571c 5819
    ldr r1, DAT_080b5798                     @ 080b571e 1e49
    adds r0,r0,r1    @ 080b5720 4018
    ldr r0,[r0,#0x0]                         @ 080b5722 0068
    lsls r0,r0,#0x13    @ 080b5724 c004
    lsrs r0,r0,#0x13    @ 080b5726 c00c
    bl get_card_extended_stat_field7         @ 080b5728 39f07cfb
    cmp r4,r0                                @ 080b572c 8442
    bne LAB_080b5732                         @ 080b572e 00d1
    b LAB_080b58ce                           @ 080b5730 cde0
LAB_080b5732:
    adds r7,#0x1    @ 080b5732 0137
    ldr r2, DAT_080b5790                     @ 080b5734 164a
    .hword 0x4640    @ 080b5736 4046
    muls r0,r2    @ 080b5738 5043
    ldr r1,[sp,#0x60]                        @ 080b573a 1899
    adds r1,#0xc    @ 080b573c 0c31
    adds r0,r0,r1    @ 080b573e 4018
    ldr r0,[r0,#0x0]                         @ 080b5740 0068
    cmp r7,r0                                @ 080b5742 8742
    bcc LAB_080b56ec                         @ 080b5744 d2d3
LAB_080b5746:
    adds r6,#0x1    @ 080b5746 0136
    ldr r2,[sp,#0x5c]                        @ 080b5748 179a
    cmp r6,r2                                @ 080b574a 9642
    blt LAB_080b565c                         @ 080b574c 86db
LAB_080b574e:
    movs r6,#0x0    @ 080b574e 0026
    ldr r3,[sp,#0x5c]                        @ 080b5750 179b
    cmp r6,r3                                @ 080b5752 9e42
    bge LAB_080b57c6                         @ 080b5754 37da
    movs r0,#0x1    @ 080b5756 0120
    .hword 0x4651    @ 080b5758 5146
    ands r0,r1    @ 080b575a 0840
    ldr r1, DAT_080b5790                     @ 080b575c 0c49
    adds r5,r0,#0x0    @ 080b575e 051c
    muls r5,r1    @ 080b5760 4d43
    ldr r4, DAT_080b579c                     @ 080b5762 0e4c
    .hword 0x466b    @ 080b5764 6b46
LAB_080b5766:
    ldr r2,[r3,#0x0]                         @ 080b5766 1a68
    lsls r0,r2,#0x2    @ 080b5768 9000
    adds r0,r0,r2    @ 080b576a 8018
    lsls r0,r0,#0x2    @ 080b576c 8000
    adds r0,r0,r5    @ 080b576e 4019
    ldr r1, DAT_080b5798                     @ 080b5770 0949
    adds r0,r0,r1    @ 080b5772 4018
    ldr r0,[r0,#0x0]                         @ 080b5774 0068
    lsls r0,r0,#0x13    @ 080b5776 c004
    lsrs r1,r0,#0x13    @ 080b5778 c10c
    cmp r1,r4                                @ 080b577a a142
    beq LAB_080b57b0                         @ 080b577c 18d0
    cmp r1,r4                                @ 080b577e a142
    bgt LAB_080b57a4                         @ 080b5780 10dc
    ldr r0, DAT_080b57a0                     @ 080b5782 0748
    cmp r1,r0                                @ 080b5784 8142
    beq LAB_080b57b0                         @ 080b5786 13d0
    b LAB_080b57bc                           @ 080b5788 18e0
    .zero  0x2
DAT_080b578c:
    .word  0x00001874                     @ 080b578c 74180000
DAT_080b5790:
    .word  0x00000868                     @ 080b5790 68080000
DAT_080b5794:
    .word  0x0201c600                     @ 080b5794 00c60102
DAT_080b5798:
    .word  0x0201c510                     @ 080b5798 10c50102
DAT_080b579c:
    .word  0x000011e4                     @ 080b579c e4110000
DAT_080b57a0:
    .word  0x00000fd6                     @ 080b57a0 d60f0000
LAB_080b57a4:
    ldr r0, DAT_080b57b4                     @ 080b57a4 0348
    cmp r1,r0                                @ 080b57a6 8142
    beq LAB_080b57b0                         @ 080b57a8 02d0
    ldr r0, DAT_080b57b8                     @ 080b57aa 0348
    cmp r1,r0                                @ 080b57ac 8142
    bne LAB_080b57bc                         @ 080b57ae 05d1
LAB_080b57b0:
    adds r0,r2,#0x0    @ 080b57b0 101c
    b LAB_080b58d8                           @ 080b57b2 91e0
DAT_080b57b4:
    .word  0x000014f3                     @ 080b57b4 f3140000
DAT_080b57b8:
    .word  0x0000163f                     @ 080b57b8 3f160000
LAB_080b57bc:
    adds r3,#0x4    @ 080b57bc 0433
    adds r6,#0x1    @ 080b57be 0136
    ldr r2,[sp,#0x5c]                        @ 080b57c0 179a
    cmp r6,r2                                @ 080b57c2 9642
    blt LAB_080b5766                         @ 080b57c4 cfdb
LAB_080b57c6:
    movs r6,#0x0    @ 080b57c6 0026
    ldr r3,[sp,#0x5c]                        @ 080b57c8 179b
    cmp r6,r3                                @ 080b57ca 9e42
    bge LAB_080b5814                         @ 080b57cc 22da
    .hword 0x466d    @ 080b57ce 6d46
LAB_080b57d0:
    ldr r4,[r5,#0x0]                         @ 080b57d0 2c68
    .hword 0x4650    @ 080b57d2 5046
    adds r1,r4,#0x0    @ 080b57d4 211c
    ldr r2, DAT_080b58a8                     @ 080b57d6 344a
    bl count_equip_chain_default_flags       @ 080b57d8 79f7dcfd
    cmp r0,#0x0                              @ 080b57dc 0028
    bne LAB_080b58d2                         @ 080b57de 78d1
    .hword 0x4650    @ 080b57e0 5046
    adds r1,r4,#0x0    @ 080b57e2 211c
    ldr r2, DAT_080b58ac                     @ 080b57e4 314a
    bl count_equip_chain_default_flags       @ 080b57e6 79f7d5fd
    cmp r0,#0x0                              @ 080b57ea 0028
    bne LAB_080b58d2                         @ 080b57ec 71d1
    .hword 0x4650    @ 080b57ee 5046
    adds r1,r4,#0x0    @ 080b57f0 211c
    ldr r2, DAT_080b58b0                     @ 080b57f2 2f4a
    bl count_equip_chain_default_flags       @ 080b57f4 79f7cefd
    cmp r0,#0x0                              @ 080b57f8 0028
    bne LAB_080b58d2                         @ 080b57fa 6ad1
    .hword 0x4650    @ 080b57fc 5046
    adds r1,r4,#0x0    @ 080b57fe 211c
    ldr r2, DAT_080b58b4                     @ 080b5800 2c4a
    bl count_equip_chain_default_flags       @ 080b5802 79f7c7fd
    cmp r0,#0x0                              @ 080b5806 0028
    bne LAB_080b58d2                         @ 080b5808 63d1
    adds r5,#0x4    @ 080b580a 0435
    adds r6,#0x1    @ 080b580c 0136
    ldr r0,[sp,#0x5c]                        @ 080b580e 1798
    cmp r6,r0                                @ 080b5810 8642
    blt LAB_080b57d0                         @ 080b5812 dddb
LAB_080b5814:
    ldr r1,[sp,#0x5c]                        @ 080b5814 1799
    cmp r1,#0x0                              @ 080b5816 0029
    ble LAB_080b5860                         @ 080b5818 22dd
    movs r7,#0x1    @ 080b581a 0127
    .hword 0x4650    @ 080b581c 5046
    ands r0,r7    @ 080b581e 3840
    .hword 0x466d    @ 080b5820 6d46
    ldr r1, DAT_080b58b8                     @ 080b5822 2549
    adds r2,r0,#0x0    @ 080b5824 021c
    muls r2,r1    @ 080b5826 4a43
    .hword 0x4690    @ 080b5828 9046
    ldr r6,[sp,#0x5c]                        @ 080b582a 179e
LAB_080b582c:
    ldr r4,[r5,#0x0]                         @ 080b582c 2c68
    lsls r0,r4,#0x2    @ 080b582e a000
    adds r0,r0,r4    @ 080b5830 0019
    lsls r0,r0,#0x2    @ 080b5832 8000
    add r0,r8                                @ 080b5834 4044
    ldr r1, DAT_080b58bc                     @ 080b5836 2149
    adds r0,r0,r1    @ 080b5838 4018
    ldr r0,[r0,#0x0]                         @ 080b583a 0068
    lsls r0,r0,#0x13    @ 080b583c c004
    lsrs r0,r0,#0x13    @ 080b583e c00c
    movs r1,#0x0    @ 080b5840 0021
    bl check_card_id_in_eligible_set         @ 080b5842 f9f777fe
    cmp r0,#0x0                              @ 080b5846 0028
    beq LAB_080b5858                         @ 080b5848 06d0
    ldr r3,[sp,#0x70]                        @ 080b584a 1c9b
    adds r1,r3,r4    @ 080b584c 1919
    adds r0,r7,#0x0    @ 080b584e 381c
    lsls r0,r1    @ 080b5850 8840
    ldr r1,[sp,#0x58]                        @ 080b5852 1699
    orrs r1,r0    @ 080b5854 0143
    str r1,[sp,#0x58]                        @ 080b5856 1691
LAB_080b5858:
    adds r5,#0x4    @ 080b5858 0435
    subs r6,#0x1    @ 080b585a 013e
    cmp r6,#0x0                              @ 080b585c 002e
    bne LAB_080b582c                         @ 080b585e e5d1
LAB_080b5860:
    ldr r2,[sp,#0x50]                        @ 080b5860 149a
    ldr r3,[sp,#0x58]                        @ 080b5862 169b
    eors r2,r3    @ 080b5864 5a40
    str r2,[sp,#0x58]                        @ 080b5866 1692
    movs r3,#0x1    @ 080b5868 0123
    rsbs r3,r3,#0    @ 080b586a 5b42
    .hword 0x4650    @ 080b586c 5046
    adds r1,r2,#0x0    @ 080b586e 111c
    adds r2,r3,#0x0    @ 080b5870 1a1c
    bl find_best_scored_slot_from_bitmap     @ 080b5872 fff749fa
    adds r6,r0,#0x0    @ 080b5876 061c
    ldr r0,[sp,#0x54]                        @ 080b5878 1598
    cmp r0,#0x0                              @ 080b587a 0028
    beq LAB_080b58c0                         @ 080b587c 20d0
    cmp r6,#0x0                              @ 080b587e 002e
    blt LAB_080b58a0                         @ 080b5880 0edb
    add r4,sp,#0x2c                          @ 080b5882 0bac
    .hword 0x4650    @ 080b5884 5046
    adds r1,r6,#0x0    @ 080b5886 311c
    adds r2,r4,#0x0    @ 080b5888 221c
    bl dispatch_zone_slot_score_by_player_flag @ 080b588a f6f7bbfb
    ldr r1,[r4,#0x18]                        @ 080b588e a169
    ldr r0,[r4,#0x14]                        @ 080b5890 6069
    cmp r1,r0                                @ 080b5892 8142
    bge LAB_080b5898                         @ 080b5894 00da
    adds r1,r0,#0x0    @ 080b5896 011c
LAB_080b5898:
    movs r0,#0xaf    @ 080b5898 af20
    lsls r0,r0,#0x3    @ 080b589a c000
    cmp r1,r0                                @ 080b589c 8142
    ble LAB_080b58d6                         @ 080b589e 1add
LAB_080b58a0:
    movs r0,#0x1    @ 080b58a0 0120
    rsbs r0,r0,#0    @ 080b58a2 4042
    b LAB_080b58d8                           @ 080b58a4 18e0
    .zero  0x2
DAT_080b58a8:
    .word  0x0000149d                     @ 080b58a8 9d140000
DAT_080b58ac:
    .word  0x00001286                     @ 080b58ac 86120000
DAT_080b58b0:
    .word  0x000013f3                     @ 080b58b0 f3130000
DAT_080b58b4:
    .word  0x000014b2                     @ 080b58b4 b2140000
DAT_080b58b8:
    .word  0x00000868                     @ 080b58b8 68080000
DAT_080b58bc:
    .word  0x0201c510                     @ 080b58bc 10c50102
LAB_080b58c0:
    cmp r6,#0x0                              @ 080b58c0 002e
    bge LAB_080b58d6                         @ 080b58c2 08da
    .hword 0x4650    @ 080b58c4 5046
    ldr r1,[sp,#0x50]                        @ 080b58c6 1499
    bl sample_random_slot_from_bitmap        @ 080b58c8 fff71efc
    b LAB_080b58d8                           @ 080b58cc 04e0
LAB_080b58ce:
    .hword 0x4648    @ 080b58ce 4846
    b LAB_080b58d8                           @ 080b58d0 02e0
LAB_080b58d2:
    adds r0,r4,#0x0    @ 080b58d2 201c
    b LAB_080b58d8                           @ 080b58d4 00e0
LAB_080b58d6:
    adds r0,r6,#0x0    @ 080b58d6 301c
LAB_080b58d8:
    add sp,#0x74                             @ 080b58d8 1db0
    pop {r3,r4,r5}                           @ 080b58da 38bc
    .hword 0x4698    @ 080b58dc 9846
    .hword 0x46a1    @ 080b58de a146
    .hword 0x46aa    @ 080b58e0 aa46
    pop {r4,r5,r6,r7}                        @ 080b58e2 f0bc
    pop {r1}                                 @ 080b58e4 02bc
    bx r1                                    @ 080b58e6 0847

@ 扫描指定玩家侧手牌 (gP1LifePoints+player*0x868+0xc 读手牌数量), 对每张手牌依次执行多层筛选: (1) FUN_0810e5d4 基本资格; (2) get_card_extended_stat_field5<=4 或 check_card_has_equip_placement_type; (3) check_card_id_placement_allowed; (4) check_card_effect_activation_eligible_by_id; (5) type==0x3 时调 sample_prng_scaled. 返回最佳候选手牌索引 (r7) 或 -1. Constants: gP1LifePoints base, hand_count_offset=0xc, player_stride=0x868.
scan_hand_for_best_equip_target_slot:
    push {r4,r5,r6,r7,lr}                    @ 080b58e8 f0b5
    .hword 0x4657    @ 080b58ea 5746
    .hword 0x464e    @ 080b58ec 4e46
    .hword 0x4645    @ 080b58ee 4546
    push {r5,r6,r7}                          @ 080b58f0 e0b4
    sub sp,#0x24                             @ 080b58f2 89b0
    .hword 0x4681    @ 080b58f4 8146
    str r1,[sp,#0x0]                         @ 080b58f6 0091
    str r2,[sp,#0x4]                         @ 080b58f8 0192
    str r3,[sp,#0x8]                         @ 080b58fa 0293
    movs r0,#0x1    @ 080b58fc 0120
    rsbs r0,r0,#0    @ 080b58fe 4042
    str r0,[sp,#0xc]                         @ 080b5900 0390
    .hword 0x4682    @ 080b5902 8246
    str r0,[sp,#0x14]                        @ 080b5904 0590
    str r0,[sp,#0x10]                        @ 080b5906 0490
    str r0,[sp,#0x18]                        @ 080b5908 0690
    movs r7,#0x0    @ 080b590a 0027
    ldr r0, PTR_gP1LifePoints_080b59a0       @ 080b590c 2448
    movs r1,#0x1    @ 080b590e 0121
    .hword 0x464a    @ 080b5910 4a46
    ands r1,r2    @ 080b5912 1140
    ldr r3, DAT_080b59a4                     @ 080b5914 234b
    adds r2,r1,#0x0    @ 080b5916 0a1c
    muls r2,r3    @ 080b5918 5a43
    adds r0,#0xc    @ 080b591a 0c30
    adds r0,r2,r0    @ 080b591c 1018
    ldr r0,[r0,#0x0]                         @ 080b591e 0068
    cmp r7,r0                                @ 080b5920 8742
    bcc LAB_080b5926                         @ 080b5922 00d3
    b LAB_080b5a32                           @ 080b5924 85e0
LAB_080b5926:
    str r1,[sp,#0x20]                        @ 080b5926 0891
    str r2,[sp,#0x1c]                        @ 080b5928 0792
LAB_080b592a:
    .hword 0x4648    @ 080b592a 4846
    movs r1,#0xb    @ 080b592c 0b21
    adds r2,r7,#0x0    @ 080b592e 3a1c
    ldr r3,[sp,#0x0]                         @ 080b5930 009b
    bl invoke_r3                             @ 080b5932 58f04ffe
    cmp r0,#0x0                              @ 080b5936 0028
    beq LAB_080b5a20                         @ 080b5938 72d0
    lsls r0,r7,#0x2    @ 080b593a b800
    ldr r1,[sp,#0x20]                        @ 080b593c 0899
    ldr r2, DAT_080b59a4                     @ 080b593e 194a
    adds r6,r1,#0x0    @ 080b5940 0e1c
    muls r6,r2    @ 080b5942 5643
    adds r0,r0,r6    @ 080b5944 8019
    ldr r3, DAT_080b59a8                     @ 080b5946 184b
    .hword 0x4698    @ 080b5948 9846
    add r0,r8                                @ 080b594a 4044
    ldr r0,[r0,#0x0]                         @ 080b594c 0068
    lsls r0,r0,#0x13    @ 080b594e c004
    lsrs r5,r0,#0x13    @ 080b5950 c50c
    adds r0,r5,#0x0    @ 080b5952 281c
    bl get_card_extended_stat_field5         @ 080b5954 39f07cfa
    cmp r0,#0x4                              @ 080b5958 0428
    ble LAB_080b598c                         @ 080b595a 17dd
    adds r0,r5,#0x0    @ 080b595c 281c
    bl check_card_has_equip_placement_type   @ 080b595e 96f77bf8
    cmp r0,#0x0                              @ 080b5962 0028
    bne LAB_080b598c                         @ 080b5964 12d1
    .hword 0x4650    @ 080b5966 5046
    cmp r0,#0x0                              @ 080b5968 0028
    blt LAB_080b598a                         @ 080b596a 0edb
    adds r0,r5,#0x0    @ 080b596c 281c
    bl get_card_extended_stat_field5         @ 080b596e 39f06ffa
    adds r4,r0,#0x0    @ 080b5972 041c
    .hword 0x4651    @ 080b5974 5146
    lsls r0,r1,#0x2    @ 080b5976 8800
    adds r0,r0,r6    @ 080b5978 8019
    add r0,r8                                @ 080b597a 4044
    ldr r0,[r0,#0x0]                         @ 080b597c 0068
    lsls r0,r0,#0x13    @ 080b597e c004
    lsrs r0,r0,#0x13    @ 080b5980 c00c
    bl get_card_extended_stat_field5         @ 080b5982 39f065fa
    cmp r4,r0                                @ 080b5986 8442
    ble LAB_080b598c                         @ 080b5988 00dd
LAB_080b598a:
    .hword 0x46ba    @ 080b598a ba46
LAB_080b598c:
    ldr r0, DAT_080b59ac                     @ 080b598c 0748
    cmp r5,r0                                @ 080b598e 8542
    beq LAB_080b59d0                         @ 080b5990 1ed0
    cmp r5,r0                                @ 080b5992 8542
    bgt LAB_080b59b4                         @ 080b5994 0edc
    ldr r0, DAT_080b59b0                     @ 080b5996 0648
    cmp r5,r0                                @ 080b5998 8542
    beq LAB_080b59cc                         @ 080b599a 17d0
    b LAB_080b59d4                           @ 080b599c 1ae0
    .zero  0x2
PTR_gP1LifePoints_080b59a0:
    .word  gP1LifePoints                  @ 080b59a0 e0c40102
DAT_080b59a4:
    .word  0x00000868                     @ 080b59a4 68080000
DAT_080b59a8:
    .word  0x0201c600                     @ 080b59a8 00c60102
DAT_080b59ac:
    .word  0x0000179a                     @ 080b59ac 9a170000
DAT_080b59b0:
    .word  0x00001181                     @ 080b59b0 81110000
LAB_080b59b4:
    ldr r0, DAT_080b59c8                     @ 080b59b4 0448
    cmp r5,r0                                @ 080b59b6 8542
    bne LAB_080b59bc                         @ 080b59b8 00d1
    b LAB_080b5abc                           @ 080b59ba 7fe0
LAB_080b59bc:
    adds r0,#0x7f    @ 080b59bc 7f30
    cmp r5,r0                                @ 080b59be 8542
    bne LAB_080b59c4                         @ 080b59c0 00d1
    b LAB_080b5abc                           @ 080b59c2 7be0
LAB_080b59c4:
    b LAB_080b59d4                           @ 080b59c4 06e0
    .zero  0x2
DAT_080b59c8:
    .word  0x0000197f                     @ 080b59c8 7f190000
LAB_080b59cc:
    str r7,[sp,#0x10]                        @ 080b59cc 0497
    b LAB_080b59e2                           @ 080b59ce 08e0
LAB_080b59d0:
    str r7,[sp,#0xc]                         @ 080b59d0 0397
    b LAB_080b59e2                           @ 080b59d2 06e0
LAB_080b59d4:
    adds r0,r5,#0x0    @ 080b59d4 281c
    ldr r1,[sp,#0x4]                         @ 080b59d6 0199
    movs r2,#0x1    @ 080b59d8 0122
    bl check_card_id_placement_allowed       @ 080b59da f7f75dff
    cmp r0,#0x0                              @ 080b59de 0028
    bne LAB_080b5abc                         @ 080b59e0 6cd1
LAB_080b59e2:
    adds r2,r5,#0x0    @ 080b59e2 2a1c
    .hword 0x4648    @ 080b59e4 4846
    movs r1,#0x1    @ 080b59e6 0121
    bl check_card_effect_activation_eligible_by_id @ 080b59e8 f7f722f9
    cmp r0,#0x0                              @ 080b59ec 0028
    bne LAB_080b5a0e                         @ 080b59ee 0ed1
    adds r0,r5,#0x0    @ 080b59f0 281c
    bl get_card_type_bits_by_internal_id     @ 080b59f2 39f0d3fa
    cmp r0,#0x3                              @ 080b59f6 0328
    bne LAB_080b5a0e                         @ 080b59f8 09d1
    ldr r2,[sp,#0x14]                        @ 080b59fa 059a
    cmp r2,#0x0                              @ 080b59fc 002a
    blt LAB_080b5a0a                         @ 080b59fe 04db
    movs r0,#0x2    @ 080b5a00 0220
    bl sample_prng_scaled                    @ 080b5a02 def72ffe
    cmp r0,#0x0                              @ 080b5a06 0028
    beq LAB_080b5a20                         @ 080b5a08 0ad0
LAB_080b5a0a:
    str r7,[sp,#0x14]                        @ 080b5a0a 0597
    b LAB_080b5a20                           @ 080b5a0c 08e0
LAB_080b5a0e:
    ldr r3,[sp,#0x18]                        @ 080b5a0e 069b
    cmp r3,#0x0                              @ 080b5a10 002b
    blt LAB_080b5a1e                         @ 080b5a12 04db
    movs r0,#0x2    @ 080b5a14 0220
    bl sample_prng_scaled                    @ 080b5a16 def725fe
    cmp r0,#0x0                              @ 080b5a1a 0028
    beq LAB_080b5a20                         @ 080b5a1c 00d0
LAB_080b5a1e:
    str r7,[sp,#0x18]                        @ 080b5a1e 0697
LAB_080b5a20:
    adds r7,#0x1    @ 080b5a20 0137
    ldr r0, PTR_gP1LifePoints_080b5a64       @ 080b5a22 1048
    adds r0,#0xc    @ 080b5a24 0c30
    ldr r1,[sp,#0x1c]                        @ 080b5a26 0799
    adds r0,r1,r0    @ 080b5a28 0818
    ldr r0,[r0,#0x0]                         @ 080b5a2a 0068
    cmp r7,r0                                @ 080b5a2c 8742
    bcs LAB_080b5a32                         @ 080b5a2e 00d2
    b LAB_080b592a                           @ 080b5a30 7be7
LAB_080b5a32:
    ldr r1, DAT_080b5a68                     @ 080b5a32 0d49
    .hword 0x4648    @ 080b5a34 4846
    bl find_zone_slot_idx_allowed_for_card   @ 080b5a36 82f729f8
    movs r4,#0x1    @ 080b5a3a 0124
    rsbs r4,r4,#0    @ 080b5a3c 6442
    cmp r0,r4                                @ 080b5a3e a042
    bgt LAB_080b5a5a                         @ 080b5a40 0bdc
    ldr r1, DAT_080b5a6c                     @ 080b5a42 0a49
    .hword 0x4648    @ 080b5a44 4846
    bl find_zone_slot_idx_allowed_for_card   @ 080b5a46 82f721f8
    cmp r0,r4                                @ 080b5a4a a042
    bgt LAB_080b5a5a                         @ 080b5a4c 05dc
    ldr r1, DAT_080b5a70                     @ 080b5a4e 0849
    .hword 0x4648    @ 080b5a50 4846
    bl scan_spell_zone_for_equip_target_by_id @ 080b5a52 fff70bf9
    cmp r0,#0x0                              @ 080b5a56 0028
    beq LAB_080b5a74                         @ 080b5a58 0cd0
LAB_080b5a5a:
    .hword 0x4652    @ 080b5a5a 5246
    cmp r2,#0x0                              @ 080b5a5c 002a
    blt LAB_080b5a74                         @ 080b5a5e 09db
    .hword 0x4650    @ 080b5a60 5046
    b LAB_080b5ac4                           @ 080b5a62 2fe0
PTR_gP1LifePoints_080b5a64:
    .word  gP1LifePoints                  @ 080b5a64 e0c40102
DAT_080b5a68:
    .word  0x000012ea                     @ 080b5a68 ea120000
DAT_080b5a6c:
    .word  0x00001366                     @ 080b5a6c 66130000
DAT_080b5a70:
    .word  0x0000137d                     @ 080b5a70 7d130000
LAB_080b5a74:
    ldr r1, DAT_080b5a9c                     @ 080b5a74 0949
    .hword 0x4648    @ 080b5a76 4846
    bl count_extra_deck_cards_by_id          @ 080b5a78 81f730fb
    cmp r0,#0x0                              @ 080b5a7c 0028
    beq LAB_080b5a92                         @ 080b5a7e 08d0
    ldr r0, PTR_gP1LifePoints_080b5aa0       @ 080b5a80 0748
    ldr r3, DAT_080b5aa4                     @ 080b5a82 084b
    adds r0,r0,r3    @ 080b5a84 c018
    ldr r0,[r0,#0x0]                         @ 080b5a86 0068
    cmp r0,#0x5                              @ 080b5a88 0528
    beq LAB_080b5a92                         @ 080b5a8a 02d0
    ldr r0,[sp,#0xc]                         @ 080b5a8c 0398
    cmp r0,#0x0                              @ 080b5a8e 0028
    bge LAB_080b5ac4                         @ 080b5a90 18da
LAB_080b5a92:
    ldr r1,[sp,#0x10]                        @ 080b5a92 0499
    cmp r1,#0x0                              @ 080b5a94 0029
    blt LAB_080b5aa8                         @ 080b5a96 07db
    adds r0,r1,#0x0    @ 080b5a98 081c
    b LAB_080b5ac4                           @ 080b5a9a 13e0
DAT_080b5a9c:
    .word  0x0000179a                     @ 080b5a9c 9a170000
PTR_gP1LifePoints_080b5aa0:
    .word  gP1LifePoints                  @ 080b5aa0 e0c40102
DAT_080b5aa4:
    .word  0x00001cf4                     @ 080b5aa4 f41c0000
LAB_080b5aa8:
    ldr r2,[sp,#0x14]                        @ 080b5aa8 059a
    cmp r2,#0x0                              @ 080b5aaa 002a
    blt LAB_080b5ab2                         @ 080b5aac 01db
    adds r0,r2,#0x0    @ 080b5aae 101c
    b LAB_080b5ac4                           @ 080b5ab0 08e0
LAB_080b5ab2:
    ldr r3,[sp,#0x8]                         @ 080b5ab2 029b
    cmp r3,#0x0                              @ 080b5ab4 002b
    bne LAB_080b5ac0                         @ 080b5ab6 03d1
    ldr r0,[sp,#0x18]                        @ 080b5ab8 0698
    b LAB_080b5ac4                           @ 080b5aba 03e0
LAB_080b5abc:
    adds r0,r7,#0x0    @ 080b5abc 381c
    b LAB_080b5ac4                           @ 080b5abe 01e0
LAB_080b5ac0:
    movs r0,#0x1    @ 080b5ac0 0120
    rsbs r0,r0,#0    @ 080b5ac2 4042
LAB_080b5ac4:
    add sp,#0x24                             @ 080b5ac4 09b0
    pop {r3,r4,r5}                           @ 080b5ac6 38bc
    .hword 0x4698    @ 080b5ac8 9846
    .hword 0x46a1    @ 080b5aca a146
    .hword 0x46aa    @ 080b5acc aa46
    pop {r4,r5,r6,r7}                        @ 080b5ace f0bc
    pop {r1}                                 @ 080b5ad0 02bc
    bx r1                                    @ 080b5ad2 0847

@ Equip target random slot scan function. r0=effect_node_ptr (equip zone entry pointer), r1=player_id [0..1]. Builds 11-element slot index array [10..0] on stack; uses sample_prng_scaled for Fisher-Yates shuffle. Then performs two-player sweep (own player first, then opponent): for each shuffled slot index calls invoke_effect_node_handler_3arg(effect_node_ptr, player, slot_idx); if non-zero, calls enqueue_equip_slot_sprite_with_code_rotation and returns 1. Both sweeps fail -> return 0. Called by FUN_080b6be0 (equip target BST dispatch failure/default path) at LAB_080b6bf2.
@ 
@ Constants:
@ - SLOT_COUNT = 11 (slot index range [0..10])
@ - PLAYER_COUNT = 2
find_equip_target_by_random_order:
    push {r4,r5,r6,r7,lr}                    @ 080b5ad4 f0b5
    .hword 0x4647    @ 080b5ad6 4746
    push {r7}                                @ 080b5ad8 80b4
    sub sp,#0x2c                             @ 080b5ada 8bb0
    .hword 0x4680    @ 080b5adc 8046
    adds r7,r1,#0x0    @ 080b5ade 0f1c
    movs r6,#0xa    @ 080b5ae0 0a26
    add r0,sp,#0x28                          @ 080b5ae2 0aa8
LAB_080b5ae4:
    str r6,[r0,#0x0]                         @ 080b5ae4 0660
    subs r0,#0x4    @ 080b5ae6 0438
    subs r6,#0x1    @ 080b5ae8 013e
    cmp r6,#0x0                              @ 080b5aea 002e
    bge LAB_080b5ae4                         @ 080b5aec fada
    movs r6,#0xa    @ 080b5aee 0a26
    add r4,sp,#0x28                          @ 080b5af0 0aac
LAB_080b5af2:
    adds r0,r6,#0x1    @ 080b5af2 701c
    bl sample_prng_scaled                    @ 080b5af4 def7b6fd
    ldr r2,[r4,#0x0]                         @ 080b5af8 2268
    lsls r0,r0,#0x2    @ 080b5afa 8000
    .hword 0x466b    @ 080b5afc 6b46
    adds r1,r3,r0    @ 080b5afe 1918
    ldr r0,[r1,#0x0]                         @ 080b5b00 0868
    str r0,[r4,#0x0]                         @ 080b5b02 2060
    str r2,[r1,#0x0]                         @ 080b5b04 0a60
    subs r4,#0x4    @ 080b5b06 043c
    subs r6,#0x1    @ 080b5b08 013e
    cmp r6,#0x0                              @ 080b5b0a 002e
    bgt LAB_080b5af2                         @ 080b5b0c f1dc
    movs r6,#0x0    @ 080b5b0e 0026
LAB_080b5b10:
    movs r5,#0x0    @ 080b5b10 0025
    .hword 0x466c    @ 080b5b12 6c46
LAB_080b5b14:
    ldr r2,[r4,#0x0]                         @ 080b5b14 2268
    .hword 0x4640    @ 080b5b16 4046
    adds r1,r7,#0x0    @ 080b5b18 391c
    bl invoke_effect_node_handler_3arg       @ 080b5b1a daf765fd
    cmp r0,#0x0                              @ 080b5b1e 0028
    beq LAB_080b5b30                         @ 080b5b20 06d0
    ldr r2,[r4,#0x0]                         @ 080b5b22 2268
    .hword 0x4640    @ 080b5b24 4046
    adds r1,r7,#0x0    @ 080b5b26 391c
    bl enqueue_equip_slot_sprite_with_code_rotation @ 080b5b28 cbf7b8f8
    movs r0,#0x1    @ 080b5b2c 0120
    b LAB_080b5b44                           @ 080b5b2e 09e0
LAB_080b5b30:
    adds r4,#0x4    @ 080b5b30 0434
    adds r5,#0x1    @ 080b5b32 0135
    cmp r5,#0xa                              @ 080b5b34 0a2d
    ble LAB_080b5b14                         @ 080b5b36 eddd
    movs r0,#0x1    @ 080b5b38 0120
    eors r7,r0    @ 080b5b3a 4740
    adds r6,#0x1    @ 080b5b3c 0136
    cmp r6,#0x1                              @ 080b5b3e 012e
    ble LAB_080b5b10                         @ 080b5b40 e6dd
    movs r0,#0x0    @ 080b5b42 0020
LAB_080b5b44:
    add sp,#0x2c                             @ 080b5b44 0bb0
    pop {r3}                                 @ 080b5b46 08bc
    .hword 0x4698    @ 080b5b48 9846
    pop {r4,r5,r6,r7}                        @ 080b5b4a f0bc
    pop {r1}                                 @ 080b5b4c 02bc
    bx r1                                    @ 080b5b4e 0847

@ indeg=0 (no direct bl callers); grep .word 0x080b5b51 asm/all.s -> not found; reachable only via runtime fn-ptr dispatch. r0=player_id, r1=slot_idx. Computes gDuelFieldSlots+player_id&1*0x868+slot_idx*0x14 -> slot ptr; reads slot[0] bits[12:0]=card_id (->r4); reads ldrh[slot+8]=equip_count. If equip_count!=0 AND card_id==Ameba (0x118a): returns 3 (max tier, equipped Ameba). Else: calls check_card_field8_is_9(card_id); if field8==9 returns 2 (removed state). Else: calls check_card_id_in_effect_target_whitelist(card_id); if in whitelist returns 1. Default: returns 0.
@ 
@ Inputs: r0=player_id [0..1], r1=slot_idx [0..9]
@ Outputs: r0=u32 score_tier (3=Ameba+equipped, 2=field8==9, 1=whitelist, 0=default)
@ Side effects: none (read-only)
@ Constants: player_stride=0x868, slot_stride=0x14, gDuelFieldSlots=0x0201c510, Ameba=0x118a, TIER_MAX=3, TIER_REMOVED=2, TIER_WHITELIST=1, TIER_DEFAULT=0
classify_equip_target_slot_score_tier:
    push {r4,lr}                             @ 080b5b50 10b5
    movs r3,#0x1    @ 080b5b52 0123
    ands r3,r0    @ 080b5b54 0340
    lsls r2,r1,#0x2    @ 080b5b56 8a00
    adds r2,r2,r1    @ 080b5b58 5218
    lsls r2,r2,#0x2    @ 080b5b5a 9200
    ldr r0, DAT_080b5b7c                     @ 080b5b5c 0748
    muls r0,r3    @ 080b5b5e 5843
    adds r2,r2,r0    @ 080b5b60 1218
    ldr r0, DAT_080b5b80                     @ 080b5b62 0748
    adds r2,r2,r0    @ 080b5b64 1218
    ldr r0,[r2,#0x0]                         @ 080b5b66 1068
    lsls r0,r0,#0x13    @ 080b5b68 c004
    lsrs r4,r0,#0x13    @ 080b5b6a c40c
    ldrh r0,[r2,#0x8]                        @ 080b5b6c 1089
    cmp r0,#0x0                              @ 080b5b6e 0028
    beq LAB_080b5b88                         @ 080b5b70 0ad0
    ldr r0, DAT_080b5b84                     @ 080b5b72 0448
    cmp r4,r0                                @ 080b5b74 8442
    bne LAB_080b5b88                         @ 080b5b76 07d1
    movs r0,#0x3    @ 080b5b78 0320
    b LAB_080b5ba6                           @ 080b5b7a 14e0
DAT_080b5b7c:
    .word  0x00000868                     @ 080b5b7c 68080000
DAT_080b5b80:
    .word  0x0201c510                     @ 080b5b80 10c50102
DAT_080b5b84:
    .word  0x0000118a                     @ 080b5b84 8a110000
LAB_080b5b88:
    adds r0,r4,#0x0    @ 080b5b88 201c
    bl check_card_field8_is_9                @ 080b5b8a 95f731f9
    cmp r0,#0x0                              @ 080b5b8e 0028
    beq LAB_080b5b96                         @ 080b5b90 01d0
    movs r0,#0x2    @ 080b5b92 0220
    b LAB_080b5ba6                           @ 080b5b94 07e0
LAB_080b5b96:
    adds r0,r4,#0x0    @ 080b5b96 201c
    bl check_card_id_in_effect_target_whitelist @ 080b5b98 f7f7d2fb
    cmp r0,#0x0                              @ 080b5b9c 0028
    bne LAB_080b5ba4                         @ 080b5b9e 01d1
    movs r0,#0x0    @ 080b5ba0 0020
    b LAB_080b5ba6                           @ 080b5ba2 00e0
LAB_080b5ba4:
    movs r0,#0x1    @ 080b5ba4 0120
LAB_080b5ba6:
    pop {r4}                                 @ 080b5ba6 10bc
    pop {r1}                                 @ 080b5ba8 02bc
    bx r1                                    @ 080b5baa 0847

@ Equip target slot comparator. Called from FUN_080b5d98 (equip target slot dispatch hub) as a function pointer passed to find_best_slot_from_bitmap_by_comparator. Scores candidate slots for equip eligibility. Inputs: r0=player_id bit0, r1=slot_idx. Computes slot entry address (gDuelFieldSlots + player*0x868 + slot*0x14), extracts card_id (bits[12:0]), calls get_card_field_summon_restriction. If restriction==0 AND slot[+0x8]==0 (no equip chain attached), returns 1 (eligible); otherwise returns 0. Selects monster slots with no summon restriction and no attached equip chain state. Side effects: none.
@ 
@ Constants:
@ - gDuelFieldSlots=0x0201c510
@ - player_stride=0x868
@ - slot_entry_size=0x14 (20 bytes)
@ - slot_field8_offset=+0x8 (chain/equip count halfword)
score_slot_by_no_summon_restriction:
    push {r4,r5,lr}                          @ 080b5bac 30b5
    movs r5,#0x0    @ 080b5bae 0025
    movs r2,#0x1    @ 080b5bb0 0122
    ands r2,r0    @ 080b5bb2 0240
    lsls r0,r1,#0x2    @ 080b5bb4 8800
    adds r0,r0,r1    @ 080b5bb6 4018
    lsls r0,r0,#0x2    @ 080b5bb8 8000
    ldr r1, DAT_080b5be4                     @ 080b5bba 0a49
    muls r1,r2    @ 080b5bbc 5143
    adds r0,r0,r1    @ 080b5bbe 4018
    ldr r1, DAT_080b5be8                     @ 080b5bc0 0949
    adds r4,r0,r1    @ 080b5bc2 4418
    ldr r0,[r4,#0x0]                         @ 080b5bc4 2068
    lsls r0,r0,#0x13    @ 080b5bc6 c004
    lsrs r0,r0,#0x13    @ 080b5bc8 c00c
    bl get_card_field_summon_restriction     @ 080b5bca 95f793fc
    cmp r0,#0x0                              @ 080b5bce 0028
    beq LAB_080b5bda                         @ 080b5bd0 03d0
    ldrh r0,[r4,#0x8]                        @ 080b5bd2 2089
    cmp r0,#0x0                              @ 080b5bd4 0028
    bne LAB_080b5bda                         @ 080b5bd6 00d1
    movs r5,#0x1    @ 080b5bd8 0125
LAB_080b5bda:
    adds r0,r5,#0x0    @ 080b5bda 281c
    pop {r4,r5}                              @ 080b5bdc 30bc
    pop {r1}                                 @ 080b5bde 02bc
    bx r1                                    @ 080b5be0 0847
    .zero  0x2
DAT_080b5be4:
    .word  0x00000868                     @ 080b5be4 68080000
DAT_080b5be8:
    .word  0x0201c510                     @ 080b5be8 10c50102

@ Equip target slot comparator (variant). Called from FUN_080b5d98 (equip target slot dispatch hub) as function pointer stored at DAT_080b69dc/DAT_080b6b6c, passed to find_best_slot_from_bitmap_by_comparator. Inputs: r0=player_id bit0, r1=slot_idx. Computes slot entry address, extracts card_id, calls get_card_field_summon_restriction. If restriction==0, returns 0. If restriction!=0, reads slot[+0x8] halfword, applies rsbs/orrs/lsrs #0x1f to extract sign bit (0 if zero, 1 if nonzero) as score. Result: restriction nonzero AND slot[+0x8] nonzero -> 1; restriction nonzero but slot[+0x8]==0 -> 0; no restriction -> 0. Side effects: none.
@ 
@ Constants:
@ - gDuelFieldSlots=0x0201c510
@ - player_stride=0x868
@ - slot_entry_size=0x14
@ - slot_field8_offset=+0x8
score_slot_by_equip_chain_presence:
    push {r4,r5,lr}                          @ 080b5bec 30b5
    movs r5,#0x0    @ 080b5bee 0025
    movs r2,#0x1    @ 080b5bf0 0122
    ands r2,r0    @ 080b5bf2 0240
    lsls r0,r1,#0x2    @ 080b5bf4 8800
    adds r0,r0,r1    @ 080b5bf6 4018
    lsls r0,r0,#0x2    @ 080b5bf8 8000
    ldr r1, DAT_080b5c24                     @ 080b5bfa 0a49
    muls r1,r2    @ 080b5bfc 5143
    adds r0,r0,r1    @ 080b5bfe 4018
    ldr r1, DAT_080b5c28                     @ 080b5c00 0949
    adds r4,r0,r1    @ 080b5c02 4418
    ldr r0,[r4,#0x0]                         @ 080b5c04 2068
    lsls r0,r0,#0x13    @ 080b5c06 c004
    lsrs r0,r0,#0x13    @ 080b5c08 c00c
    bl get_card_field_summon_restriction     @ 080b5c0a 95f773fc
    cmp r0,#0x0                              @ 080b5c0e 0028
    beq LAB_080b5c1a                         @ 080b5c10 03d0
    ldrh r1,[r4,#0x8]                        @ 080b5c12 2189
    rsbs r0,r1,#0    @ 080b5c14 4842
    orrs r0,r1    @ 080b5c16 0843
    lsrs r5,r0,#0x1f    @ 080b5c18 c50f
LAB_080b5c1a:
    adds r0,r5,#0x0    @ 080b5c1a 281c
    pop {r4,r5}                              @ 080b5c1c 30bc
    pop {r1}                                 @ 080b5c1e 02bc
    bx r1                                    @ 080b5c20 0847
    .zero  0x2
DAT_080b5c24:
    .word  0x00000868                     @ 080b5c24 68080000
DAT_080b5c28:
    .word  0x0201c510                     @ 080b5c28 10c50102

@ Equip target slot comparator (equip placement type check). Called from FUN_080b5d98 (0x080b5d98, equip target slot dispatch hub) as function pointer stored at DAT_080b655c (0x080b5c2d), passed to find_best_slot_from_bitmap_by_comparator. Inputs: r0=player_id bit0, r1=slot_idx. Computes slot entry address, extracts card_id (bits[12:0]), calls get_card_extended_stat_field5. If field5 > 4 -> returns 1. If field5 <= 4: calls check_card_has_equip_placement_type; if nonzero -> returns 1; else -> returns 0. Selects slots where field5>4 or where the card has a specific equip placement type. Side effects: none.
@ 
@ Constants:
@ - gDuelFieldSlots=0x0201c510
@ - player_stride=0x868
@ - slot_entry_size=0x14
@ - FIELD5_EQUIP_THRESHOLD=4
score_slot_by_equip_type_eligibility:
    push {r4,r5,lr}                          @ 080b5c2c 30b5
    movs r2,#0x1    @ 080b5c2e 0122
    ands r2,r0    @ 080b5c30 0240
    lsls r0,r1,#0x2    @ 080b5c32 8800
    adds r0,r0,r1    @ 080b5c34 4018
    lsls r0,r0,#0x2    @ 080b5c36 8000
    ldr r1, DAT_080b5c68                     @ 080b5c38 0b49
    muls r1,r2    @ 080b5c3a 5143
    adds r0,r0,r1    @ 080b5c3c 4018
    ldr r1, DAT_080b5c6c                     @ 080b5c3e 0b49
    adds r0,r0,r1    @ 080b5c40 4018
    ldr r0,[r0,#0x0]                         @ 080b5c42 0068
    lsls r0,r0,#0x13    @ 080b5c44 c004
    lsrs r4,r0,#0x13    @ 080b5c46 c40c
    movs r5,#0x0    @ 080b5c48 0025
    adds r0,r4,#0x0    @ 080b5c4a 201c
    bl get_card_extended_stat_field5         @ 080b5c4c 39f000f9
    cmp r0,#0x4                              @ 080b5c50 0428
    bgt LAB_080b5c5e                         @ 080b5c52 04dc
    adds r0,r4,#0x0    @ 080b5c54 201c
    bl check_card_has_equip_placement_type   @ 080b5c56 95f7fffe
    cmp r0,#0x0                              @ 080b5c5a 0028
    beq LAB_080b5c60                         @ 080b5c5c 00d0
LAB_080b5c5e:
    movs r5,#0x1    @ 080b5c5e 0125
LAB_080b5c60:
    adds r0,r5,#0x0    @ 080b5c60 281c
    pop {r4,r5}                              @ 080b5c62 30bc
    pop {r1}                                 @ 080b5c64 02bc
    bx r1                                    @ 080b5c66 0847
DAT_080b5c68:
    .word  0x00000868                     @ 080b5c68 68080000
DAT_080b5c6c:
    .word  0x0201c510                     @ 080b5c6c 10c50102

@ Equip target slot scorer (field5 + zone boundary constraints). Called from FUN_080b5d98 (0x080b5d98, equip target slot dispatch hub) as function pointer stored at DAT_080b7234 (0x080b5c71), passed to find_best_slot_from_bitmap_by_comparator. r0=player_id, r1=slot_idx, r2=sp-passed context (score bound parameters from parent frame). Calls get_slot_field5_score(duelState->field0, duelState->field1c) for reference score; calls dispatch_zone_slot_score_by_player_flag(player, slot, sp_arg) for slot score; computes delta=slot_score-(field5_score-1), clamped to [0,0]. If zone active bit is 0 -> returns 0. If card_type bits[31:19]==0x9ce00000 marker -> adds 1. Returns adjusted score. Side effects: none.
@ 
@ Constants:
@ - gDuelFieldSlots=0x0201c510 (DAT_080b5cd0)
@ - gDuelState=0x0201bb90 (DAT_080b5cc8)
@ - player_stride=0x868 (DAT_080b5ccc)
@ - MARKER=0x9ce00000 (DAT_080b5cd4, card_type marker check)
score_slot_by_field5_and_zone_bounds:
    push {r4,r5,r6,lr}                       @ 080b5c70 70b5
    sub sp,#0x24                             @ 080b5c72 89b0
    adds r5,r0,#0x0    @ 080b5c74 051c
    adds r4,r1,#0x0    @ 080b5c76 0c1c
    ldr r1, DAT_080b5cc8                     @ 080b5c78 1349
    ldr r0,[r1,#0x0]                         @ 080b5c7a 0868
    ldr r1,[r1,#0x1c]                        @ 080b5c7c c969
    bl get_slot_field5_score                 @ 080b5c7e 84f76bfe
    adds r6,r0,#0x0    @ 080b5c82 061c
    adds r0,r5,#0x0    @ 080b5c84 281c
    adds r1,r4,#0x0    @ 080b5c86 211c
    .hword 0x466a    @ 080b5c88 6a46
    bl dispatch_zone_slot_score_by_player_flag @ 080b5c8a f6f7bbf9
    movs r2,#0x1    @ 080b5c8e 0122
    ands r2,r5    @ 080b5c90 2a40
    lsls r0,r4,#0x2    @ 080b5c92 a000
    adds r0,r0,r4    @ 080b5c94 0019
    lsls r0,r0,#0x2    @ 080b5c96 8000
    ldr r1, DAT_080b5ccc                     @ 080b5c98 0c49
    muls r1,r2    @ 080b5c9a 5143
    adds r0,r0,r1    @ 080b5c9c 4018
    ldr r1, DAT_080b5cd0                     @ 080b5c9e 0c49
    adds r3,r0,r1    @ 080b5ca0 4318
    ldrh r0,[r3,#0x6]                        @ 080b5ca2 d888
    cmp r0,#0x0                              @ 080b5ca4 0028
    beq LAB_080b5cd8                         @ 080b5ca6 17d0
    subs r1,r6,#0x1    @ 080b5ca8 711e
    ldr r0,[sp,#0x18]                        @ 080b5caa 0698
    subs r0,r0,r1    @ 080b5cac 401a
    cmp r0,#0x0                              @ 080b5cae 0028
    ble LAB_080b5cb4                         @ 080b5cb0 00dd
    movs r0,#0x0    @ 080b5cb2 0020
LAB_080b5cb4:
    adds r2,r0,#0x1    @ 080b5cb4 421c
    ldr r0,[r3,#0x0]                         @ 080b5cb6 1868
    lsls r0,r0,#0x13    @ 080b5cb8 c004
    ldr r1, DAT_080b5cd4                     @ 080b5cba 0649
    cmp r0,r1                                @ 080b5cbc 8842
    beq LAB_080b5cc2                         @ 080b5cbe 00d0
    adds r2,#0x1    @ 080b5cc0 0132
LAB_080b5cc2:
    adds r0,r2,#0x0    @ 080b5cc2 101c
    b LAB_080b5cde                           @ 080b5cc4 0be0
    .zero  0x2
DAT_080b5cc8:
    .word  0x0201bb90                     @ 080b5cc8 90bb0102
DAT_080b5ccc:
    .word  0x00000868                     @ 080b5ccc 68080000
DAT_080b5cd0:
    .word  0x0201c510                     @ 080b5cd0 10c50102
DAT_080b5cd4:
    .word  0x9ce00000                     @ 080b5cd4 0000e09c
LAB_080b5cd8:
    ldr r0,[sp,#0x14]                        @ 080b5cd8 0598
    subs r0,r0,r6    @ 080b5cda 801b
    lsls r0,r0,#0x1    @ 080b5cdc 4000
LAB_080b5cde:
    add sp,#0x24                             @ 080b5cde 09b0
    pop {r4,r5,r6}                           @ 080b5ce0 70bc
    pop {r1}                                 @ 080b5ce2 02bc
    bx r1                                    @ 080b5ce4 0847
    .zero  0x2

@ Equip target slot scorer (zone lock + slot type). Called from FUN_080b5d98 (0x080b5d98) as function pointer stored at DAT_080b6bb8 (0x080b5ce9), passed to find_best_slot_from_bitmap_by_comparator. r0=player_id, r1=slot_idx. Computes slot address (gP1LifePoints + player*0x868 + slot*0x14 + 0x40), reads zone state dword, checks bit7 (lsrs #0x7, ands #1): if bit7 nonzero (zone locked) -> returns 0. Otherwise: slot_idx<=4 -> returns 2 (monster zone); slot_idx>4 -> returns 1 (spell/trap zone). Locked zones not eligible; monster zones (<=4) preferred over spell/trap zones (>4). Side effects: none.
@ 
@ Constants:
@ - gP1LifePoints=0x0201c4e0 (PTR_gP1LifePoints_080b5d10)
@ - player_stride=0x868 (DAT_080b5d14)
@ - zone_entry_size=0x14
@ - zone_base_offset=0x40
@ - ZONE_LOCK_BIT=bit7 of zone dword
@ - SCORE_MONSTER_ZONE=2, SCORE_SPELL_ZONE=1, SCORE_LOCKED=0
@ - SLOT_IDX_MONSTER_MAX=4
score_slot_by_zone_lock_and_type:
    push {r4,r5,lr}                          @ 080b5ce8 30b5
    adds r5,r1,#0x0    @ 080b5cea 0d1c
    ldr r3, PTR_gP1LifePoints_080b5d10       @ 080b5cec 084b
    lsls r1,r5,#0x2    @ 080b5cee a900
    adds r1,r1,r5    @ 080b5cf0 4919
    lsls r1,r1,#0x2    @ 080b5cf2 8900
    movs r4,#0x1    @ 080b5cf4 0124
    ands r0,r4    @ 080b5cf6 2040
    ldr r2, DAT_080b5d14                     @ 080b5cf8 064a
    muls r0,r2    @ 080b5cfa 5043
    adds r1,r1,r0    @ 080b5cfc 0918
    adds r3,#0x40    @ 080b5cfe 4033
    adds r1,r1,r3    @ 080b5d00 c918
    ldr r0,[r1,#0x0]                         @ 080b5d02 0868
    lsrs r0,r0,#0x7    @ 080b5d04 c009
    ands r0,r4    @ 080b5d06 2040
    cmp r0,#0x0                              @ 080b5d08 0028
    beq LAB_080b5d18                         @ 080b5d0a 05d0
    movs r0,#0x0    @ 080b5d0c 0020
    b LAB_080b5d20                           @ 080b5d0e 07e0
PTR_gP1LifePoints_080b5d10:
    .word  gP1LifePoints                  @ 080b5d10 e0c40102
DAT_080b5d14:
    .word  0x00000868                     @ 080b5d14 68080000
LAB_080b5d18:
    movs r0,#0x1    @ 080b5d18 0120
    cmp r5,#0x4                              @ 080b5d1a 042d
    bgt LAB_080b5d20                         @ 080b5d1c 00dc
    movs r0,#0x2    @ 080b5d1e 0220
LAB_080b5d20:
    pop {r4,r5}                              @ 080b5d20 30bc
    pop {r1}                                 @ 080b5d22 02bc
    bx r1                                    @ 080b5d24 0847
    .zero  0x2

@ Searches equip zone slot_idx for an evolution target card ID for the given player.
@ Called via fn-ptr table DAT_080b701c (0x080b5d29) from FUN_080b5d98 equip target slot dispatch hub.
@ r0=player_id bit0, r1=slot_idx [0..10].
@ Computes gDuelEffectZones + player*0x868 + slot_idx*0x14, loads slot DWORD,
@ extracts 13-bit card_id via lsls/lsrs #0x13 -> r4.
@ Calls check_card_id_is_effect_monster_type_b(r4); if 0 (not evolution type) -> return 0.
@ Calls get_card_evolution_target_ids(r4) -> r0=count, r1=ptr to target ID array.
@ If r4 >= max_target_id (already at max evolution) -> return 0.
@ Tries find_zone_slot_idx_allowed_for_card(player) >= 0; then
@ find_card_pair_in_player_deck_list(player, max_target_id) >= 0.
@ Either success -> return max_target_id; both fail -> return 0.
@ 
@ Constants:
@ - gDuelEffectZones=0x0201c510 (DAT_080b5d88)
@ - player_stride=0x868 (DAT_080b5d84)
@ - CARD_ID_BITS=13 (lsls/lsrs #0x13)
find_evolution_target_for_equip_slot_card:
    push {r4,r5,r6,lr}                       @ 080b5d28 70b5
    sub sp,#0x8                              @ 080b5d2a 82b0
    adds r6,r0,#0x0    @ 080b5d2c 061c
    movs r2,#0x1    @ 080b5d2e 0122
    ands r2,r6    @ 080b5d30 3240
    lsls r0,r1,#0x2    @ 080b5d32 8800
    adds r0,r0,r1    @ 080b5d34 4018
    lsls r0,r0,#0x2    @ 080b5d36 8000
    ldr r1, DAT_080b5d84                     @ 080b5d38 1249
    muls r1,r2    @ 080b5d3a 5143
    adds r0,r0,r1    @ 080b5d3c 4018
    ldr r1, DAT_080b5d88                     @ 080b5d3e 1249
    adds r0,r0,r1    @ 080b5d40 4018
    ldr r0,[r0,#0x0]                         @ 080b5d42 0068
    lsls r0,r0,#0x13    @ 080b5d44 c004
    lsrs r4,r0,#0x13    @ 080b5d46 c40c
    adds r0,r4,#0x0    @ 080b5d48 201c
    bl check_card_id_is_effect_monster_type_b @ 080b5d4a 95f7cbf9
    cmp r0,#0x0                              @ 080b5d4e 0028
    beq LAB_080b5d8c                         @ 080b5d50 1cd0
    adds r0,r4,#0x0    @ 080b5d52 201c
    .hword 0x4669    @ 080b5d54 6946
    bl get_card_evolution_target_ids         @ 080b5d56 95f717fb
    subs r0,#0x1    @ 080b5d5a 0138
    lsls r0,r0,#0x2    @ 080b5d5c 8000
    .hword 0x4669    @ 080b5d5e 6946
    adds r5,r0,r1    @ 080b5d60 4518
    ldr r1,[r5,#0x0]                         @ 080b5d62 2968
    cmp r4,r1                                @ 080b5d64 8c42
    bge LAB_080b5d8c                         @ 080b5d66 11da
    adds r0,r6,#0x0    @ 080b5d68 301c
    bl find_zone_slot_idx_allowed_for_card   @ 080b5d6a 81f78ffe
    cmp r0,#0x0                              @ 080b5d6e 0028
    bge LAB_080b5d7e                         @ 080b5d70 05da
    ldr r1,[r5,#0x0]                         @ 080b5d72 2968
    adds r0,r6,#0x0    @ 080b5d74 301c
    bl find_card_pair_in_player_deck_list    @ 080b5d76 7bf79ffc
    cmp r0,#0x0                              @ 080b5d7a 0028
    blt LAB_080b5d8c                         @ 080b5d7c 06db
LAB_080b5d7e:
    ldr r0,[r5,#0x0]                         @ 080b5d7e 2868
    b LAB_080b5d8e                           @ 080b5d80 05e0
    .zero  0x2
DAT_080b5d84:
    .word  0x00000868                     @ 080b5d84 68080000
DAT_080b5d88:
    .word  0x0201c510                     @ 080b5d88 10c50102
LAB_080b5d8c:
    movs r0,#0x0    @ 080b5d8c 0020
LAB_080b5d8e:
    add sp,#0x8                              @ 080b5d8e 02b0
    pop {r4,r5,r6}                           @ 080b5d90 70bc
    pop {r1}                                 @ 080b5d92 02bc
    bx r1                                    @ 080b5d94 0847
    .zero  0x2

@ 装备效果目标选择主调度器. r0=装备区指针, r1=区域位图, r2=effect_strategy_code 三参数驱动. 入口调 query_equip_zone_bitmap_with_effect_guard 过滤位图; 若全空直接走失败出口 restore_equip_dispatch_frame(r0=1). 对 r2 做大型 BST 分派 (约 20 个 case), 每个 case 调用对应 exec_equip_target_by_* / select_equip_target_* 片段执行具体策略: 包括 field5/field6/field7 分值扫描, chain-effect 匹配, side-bitmap 测试, zone-lock 检查, comparator 函数指针等. 成功 case 末调 enqueue_equip_slot_sprite_success (r0=1) 后汇聚到 restore_equip_dispatch_frame; 失败 case 调 FUN_080b6be0 后同一出口. 8 个调用者均位于 equip activation 显示状态机中 (tick_equip_activation_display_3state 等).
select_equip_target_slot_by_effect_strategy:
    push {r4,r5,r6,r7,lr}                    @ 080b5d98 f0b5
    .hword 0x4657    @ 080b5d9a 5746
    .hword 0x464e    @ 080b5d9c 4e46
    .hword 0x4645    @ 080b5d9e 4546
    push {r5,r6,r7}                          @ 080b5da0 e0b4
    sub sp,#0x2c                             @ 080b5da2 8bb0
    adds r6,r0,#0x0    @ 080b5da4 061c
    adds r5,r1,#0x0    @ 080b5da6 0d1c
    adds r4,r2,#0x0    @ 080b5da8 141c
    bl query_equip_zone_bitmap_with_effect_guard @ 080b5daa daf75ffc
    .hword 0x4681    @ 080b5dae 8146
    cmp r0,#0x0                              @ 080b5db0 0028
    bne LAB_080b5dba                         @ 080b5db2 02d1
    movs r0,#0x1    @ 080b5db4 0120
    bl restore_equip_dispatch_frame          @ 080b5db6 00f01fff
LAB_080b5dba:
    ldr r0, DAT_080b5e20                     @ 080b5dba 1948
    .hword 0x4682    @ 080b5dbc 8246
    ldrb r2,[r6,#0x2]                        @ 080b5dbe b278
    lsls r3,r2,#0x1f    @ 080b5dc0 d307
    lsrs r1,r3,#0x1f    @ 080b5dc2 d90f
    ldrb r7,[r6,#0x3]                        @ 080b5dc4 f778
    lsls r0,r7,#0x19    @ 080b5dc6 7806
    lsrs r0,r0,#0x1f    @ 080b5dc8 c00f
    eors r1,r0    @ 080b5dca 4140
    .hword 0x4650    @ 080b5dcc 5046
    str r1,[r0,#0x0]                         @ 080b5dce 0160
    ldr r0, DAT_080b5e24                     @ 080b5dd0 1448
    .hword 0x4690    @ 080b5dd2 9046
    cmp r4,r0                                @ 080b5dd4 8442
    bne LAB_080b5dda                         @ 080b5dd6 00d1
    b LAB_080b64d2                           @ 080b5dd8 7be3
LAB_080b5dda:
    cmp r4,r0                                @ 080b5dda 8442
    ble LAB_080b5de0                         @ 080b5ddc 00dd
    b LAB_080b604c                           @ 080b5dde 35e1
LAB_080b5de0:
    ldr r0, DAT_080b5e28                     @ 080b5de0 1148
    cmp r4,r0                                @ 080b5de2 8442
    bne LAB_080b5dea                         @ 080b5de4 01d1
    bl exec_equip_target_by_field5_score_scan @ 080b5de6 00f0fffc
LAB_080b5dea:
    cmp r4,r0                                @ 080b5dea 8442
    ble LAB_080b5df0                         @ 080b5dec 00dd
    b LAB_080b5f08                           @ 080b5dee 8be0
LAB_080b5df0:
    subs r0,#0xb7    @ 080b5df0 b738
    cmp r4,r0                                @ 080b5df2 8442
    bne LAB_080b5df8                         @ 080b5df4 00d1
    b LAB_080b64d2                           @ 080b5df6 6ce3
LAB_080b5df8:
    cmp r4,r0                                @ 080b5df8 8442
    bgt LAB_080b5e80                         @ 080b5dfa 41dc
    ldr r0, DAT_080b5e2c                     @ 080b5dfc 0b48
    cmp r4,r0                                @ 080b5dfe 8442
    bne LAB_080b5e04                         @ 080b5e00 00d1
    b LAB_080b6314                           @ 080b5e02 87e2
LAB_080b5e04:
    cmp r4,r0                                @ 080b5e04 8442
    bgt LAB_080b5e4c                         @ 080b5e06 21dc
    subs r0,#0xe5    @ 080b5e08 e538
    cmp r4,r0                                @ 080b5e0a 8442
    bne LAB_080b5e10                         @ 080b5e0c 00d1
    b LAB_080b64d2                           @ 080b5e0e 60e3
LAB_080b5e10:
    cmp r4,r0                                @ 080b5e10 8442
    bgt LAB_080b5e30                         @ 080b5e12 0ddc
    subs r0,#0x24    @ 080b5e14 2438
    cmp r4,r0                                @ 080b5e16 8442
    bne LAB_080b5e1c                         @ 080b5e18 00d1
    b LAB_080b64d2                           @ 080b5e1a 5ae3
LAB_080b5e1c:
    adds r0,#0xb    @ 080b5e1c 0b30
    b LAB_080b62f6                           @ 080b5e1e 6ae2
DAT_080b5e20:
    .word  0x0201afe0                     @ 080b5e20 e0af0102
DAT_080b5e24:
    .word  0x000014cb                     @ 080b5e24 cb140000
DAT_080b5e28:
    .word  0x0000130a                     @ 080b5e28 0a130000
DAT_080b5e2c:
    .word  0x00001103                     @ 080b5e2c 03110000
LAB_080b5e30:
    ldr r0, DAT_080b5e40                     @ 080b5e30 0348
    cmp r4,r0                                @ 080b5e32 8442
    bne LAB_080b5e38                         @ 080b5e34 00d1
    b LAB_080b6394                           @ 080b5e36 ade2
LAB_080b5e38:
    cmp r4,r0                                @ 080b5e38 8442
    bgt LAB_080b5e44                         @ 080b5e3a 03dc
    subs r0,#0x4d    @ 080b5e3c 4d38
    b LAB_080b62f6                           @ 080b5e3e 5ae2
DAT_080b5e40:
    .word  0x000010d3                     @ 080b5e40 d3100000
LAB_080b5e44:
    ldr r0, DAT_080b5e48                     @ 080b5e44 0048
    b LAB_080b62da                           @ 080b5e46 48e2
DAT_080b5e48:
    .word  0x000010e6                     @ 080b5e48 e6100000
LAB_080b5e4c:
    ldr r0, DAT_080b5e60                     @ 080b5e4c 0448
    cmp r4,r0                                @ 080b5e4e 8442
    bgt LAB_080b5e64                         @ 080b5e50 08dc
    subs r0,#0x1    @ 080b5e52 0138
    cmp r4,r0                                @ 080b5e54 8442
    blt LAB_080b5e5a                         @ 080b5e56 00db
    b LAB_080b64d2                           @ 080b5e58 3be3
LAB_080b5e5a:
    subs r0,#0x1f    @ 080b5e5a 1f38
    b LAB_080b62f6                           @ 080b5e5c 4be2
    .zero  0x2
DAT_080b5e60:
    .word  0x0000119b                     @ 080b5e60 9b110000
LAB_080b5e64:
    ldr r0, DAT_080b5e74                     @ 080b5e64 0348
    cmp r4,r0                                @ 080b5e66 8442
    bne LAB_080b5e6c                         @ 080b5e68 00d1
    b LAB_080b651a                           @ 080b5e6a 56e3
LAB_080b5e6c:
    cmp r4,r0                                @ 080b5e6c 8442
    bgt LAB_080b5e78                         @ 080b5e6e 03dc
    subs r0,#0x64    @ 080b5e70 6438
    b LAB_080b6306                           @ 080b5e72 48e2
DAT_080b5e74:
    .word  0x00001227                     @ 080b5e74 27120000
LAB_080b5e78:
    ldr r0, DAT_080b5e7c                     @ 080b5e78 0048
    b LAB_080b603e                           @ 080b5e7a e0e0
DAT_080b5e7c:
    .word  0x00001243                     @ 080b5e7c 43120000
LAB_080b5e80:
    ldr r0, DAT_080b5ea4                     @ 080b5e80 0848
    cmp r4,r0                                @ 080b5e82 8442
    bne LAB_080b5e88                         @ 080b5e84 00d1
    b LAB_080b64d2                           @ 080b5e86 24e3
LAB_080b5e88:
    cmp r4,r0                                @ 080b5e88 8442
    bgt LAB_080b5ec0                         @ 080b5e8a 19dc
    subs r0,#0x14    @ 080b5e8c 1438
    cmp r4,r0                                @ 080b5e8e 8442
    bne LAB_080b5e94                         @ 080b5e90 00d1
    b LAB_080b651a                           @ 080b5e92 42e3
LAB_080b5e94:
    cmp r4,r0                                @ 080b5e94 8442
    bgt LAB_080b5ea8                         @ 080b5e96 07dc
    subs r0,#0x4    @ 080b5e98 0438
    cmp r4,r0                                @ 080b5e9a 8442
    bne LAB_080b5ea0                         @ 080b5e9c 00d1
    b LAB_080b65d4                           @ 080b5e9e 99e3
LAB_080b5ea0:
    adds r0,#0x1    @ 080b5ea0 0130
    b LAB_080b6306                           @ 080b5ea2 30e2
DAT_080b5ea4:
    .word  0x00001298                     @ 080b5ea4 98120000
LAB_080b5ea8:
    ldr r0, DAT_080b5ebc                     @ 080b5ea8 0448
    cmp r4,r0                                @ 080b5eaa 8442
    bne LAB_080b5eb0                         @ 080b5eac 00d1
    b LAB_080b65d4                           @ 080b5eae 91e3
LAB_080b5eb0:
    cmp r4,r0                                @ 080b5eb0 8442
    bge LAB_080b5eb8                         @ 080b5eb2 01da
    bl select_equip_target_for_opponent_random @ 080b5eb4 00f094fe
LAB_080b5eb8:
    adds r0,#0x4    @ 080b5eb8 0430
    b LAB_080b612e                           @ 080b5eba 38e1
DAT_080b5ebc:
    .word  0x0000128a                     @ 080b5ebc 8a120000
LAB_080b5ec0:
    ldr r0, DAT_080b5eec                     @ 080b5ec0 0a48
    cmp r4,r0                                @ 080b5ec2 8442
    bgt LAB_080b5ef8                         @ 080b5ec4 18dc
    subs r0,#0x1    @ 080b5ec6 0138
    cmp r4,r0                                @ 080b5ec8 8442
    blt LAB_080b5ed0                         @ 080b5eca 01db
    bl exec_equip_target_by_active_side_bitmap @ 080b5ecc 00f070fc
LAB_080b5ed0:
    subs r0,#0xb    @ 080b5ed0 0b38
    cmp r4,r0                                @ 080b5ed2 8442
    bne LAB_080b5ed8                         @ 080b5ed4 00d1
    b LAB_080b64d2                           @ 080b5ed6 fce2
LAB_080b5ed8:
    cmp r4,r0                                @ 080b5ed8 8442
    bgt LAB_080b5ef0                         @ 080b5eda 09dc
    subs r0,#0x2b    @ 080b5edc 2b38
    cmp r4,r0                                @ 080b5ede 8442
    bne LAB_080b5ee6                         @ 080b5ee0 01d1
    bl exec_equip_target_by_best_field7_score @ 080b5ee2 00f03bfc
LAB_080b5ee6:
    bl select_equip_target_for_opponent_random @ 080b5ee6 00f07bfe
    .zero  0x2
DAT_080b5eec:
    .word  0x000012f2                     @ 080b5eec f2120000
LAB_080b5ef0:
    ldr r0, DAT_080b5ef4                     @ 080b5ef0 0048
    b LAB_080b62f6                           @ 080b5ef2 00e2
DAT_080b5ef4:
    .word  0x000012eb                     @ 080b5ef4 eb120000
LAB_080b5ef8:
    ldr r0, DAT_080b5f04                     @ 080b5ef8 0248
    cmp r4,r0                                @ 080b5efa 8442
    bne LAB_080b5f00                         @ 080b5efc 00d1
    b LAB_080b64d2                           @ 080b5efe e8e2
LAB_080b5f00:
    adds r0,#0x4    @ 080b5f00 0430
    b LAB_080b6306                           @ 080b5f02 00e2
DAT_080b5f04:
    .word  0x000012f8                     @ 080b5f04 f8120000
LAB_080b5f08:
    ldr r0, DAT_080b5f40                     @ 080b5f08 0d48
    cmp r4,r0                                @ 080b5f0a 8442
    bne LAB_080b5f10                         @ 080b5f0c 00d1
    b LAB_080b6394                           @ 080b5f0e 41e2
LAB_080b5f10:
    cmp r4,r0                                @ 080b5f10 8442
    bgt LAB_080b5f98                         @ 080b5f12 41dc
    subs r0,#0x9c    @ 080b5f14 9c38
    cmp r4,r0                                @ 080b5f16 8442
    bgt LAB_080b5f54                         @ 080b5f18 1cdc
    subs r0,#0x2    @ 080b5f1a 0238
    cmp r4,r0                                @ 080b5f1c 8442
    blt LAB_080b5f22                         @ 080b5f1e 00db
    b LAB_080b64d2                           @ 080b5f20 d7e2
LAB_080b5f22:
    subs r0,#0x21    @ 080b5f22 2138
    cmp r4,r0                                @ 080b5f24 8442
    bgt LAB_080b5f44                         @ 080b5f26 0ddc
    subs r0,#0x1    @ 080b5f28 0138
    cmp r4,r0                                @ 080b5f2a 8442
    blt LAB_080b5f32                         @ 080b5f2c 01db
    bl exec_equip_target_by_active_side_bitmap @ 080b5f2e 00f03ffc
LAB_080b5f32:
    subs r0,#0x7    @ 080b5f32 0738
    cmp r4,r0                                @ 080b5f34 8442
    bne LAB_080b5f3a                         @ 080b5f36 00d1
    b LAB_080b651a                           @ 080b5f38 efe2
LAB_080b5f3a:
    adds r0,#0x4    @ 080b5f3a 0430
    b LAB_080b5fbc                           @ 080b5f3c 3ee0
    .zero  0x2
DAT_080b5f40:
    .word  0x000013e9                     @ 080b5f40 e9130000
LAB_080b5f44:
    ldr r0, DAT_080b5f50                     @ 080b5f44 0248
    cmp r4,r0                                @ 080b5f46 8442
    bne LAB_080b5f4c                         @ 080b5f48 00d1
    b LAB_080b6496                           @ 080b5f4a a4e2
LAB_080b5f4c:
    adds r0,#0x3    @ 080b5f4c 0330
    b LAB_080b603e                           @ 080b5f4e 76e0
DAT_080b5f50:
    .word  0x0000132d                     @ 080b5f50 2d130000
LAB_080b5f54:
    ldr r0, DAT_080b5f6c                     @ 080b5f54 0548
    cmp r4,r0                                @ 080b5f56 8442
    bne LAB_080b5f5c                         @ 080b5f58 00d1
    b LAB_080b64d2                           @ 080b5f5a bae2
LAB_080b5f5c:
    cmp r4,r0                                @ 080b5f5c 8442
    bgt LAB_080b5f70                         @ 080b5f5e 07dc
    subs r0,#0x26    @ 080b5f60 2638
    cmp r4,r0                                @ 080b5f62 8442
    bne LAB_080b5f68                         @ 080b5f64 00d1
    b LAB_080b6368                           @ 080b5f66 ffe1
LAB_080b5f68:
    adds r0,#0x1a    @ 080b5f68 1a30
    b LAB_080b62f6                           @ 080b5f6a c4e1
DAT_080b5f6c:
    .word  0x00001388                     @ 080b5f6c 88130000
LAB_080b5f70:
    ldr r0, DAT_080b5f8c                     @ 080b5f70 0648
    cmp r4,r0                                @ 080b5f72 8442
    bne LAB_080b5f78                         @ 080b5f74 00d1
    b LAB_080b65d4                           @ 080b5f76 2de3
LAB_080b5f78:
    cmp r4,r0                                @ 080b5f78 8442
    bgt LAB_080b5f90                         @ 080b5f7a 09dc
    subs r0,#0x4    @ 080b5f7c 0438
    cmp r4,r0                                @ 080b5f7e 8442
    bne LAB_080b5f86                         @ 080b5f80 01d1
    bl exec_equip_target_select_opponent_first @ 080b5f82 00f0bbfc
LAB_080b5f86:
    bl select_equip_target_for_opponent_random @ 080b5f86 00f02bfe
    .zero  0x2
DAT_080b5f8c:
    .word  0x00001391                     @ 080b5f8c 91130000
LAB_080b5f90:
    ldr r0, DAT_080b5f94                     @ 080b5f90 0048
    b LAB_080b6306                           @ 080b5f92 b8e1
DAT_080b5f94:
    .word  0x000013b0                     @ 080b5f94 b0130000
LAB_080b5f98:
    ldr r0, DAT_080b5fc8                     @ 080b5f98 0b48
    cmp r4,r0                                @ 080b5f9a 8442
    bne LAB_080b5fa2                         @ 080b5f9c 01d1
    bl exec_equip_target_select_opponent_first @ 080b5f9e 00f0adfc
LAB_080b5fa2:
    cmp r4,r0                                @ 080b5fa2 8442
    bgt LAB_080b5ff4                         @ 080b5fa4 26dc
    subs r0,#0x55    @ 080b5fa6 5538
    cmp r4,r0                                @ 080b5fa8 8442
    bne LAB_080b5fae                         @ 080b5faa 00d1
    b LAB_080b6368                           @ 080b5fac dce1
LAB_080b5fae:
    cmp r4,r0                                @ 080b5fae 8442
    bgt LAB_080b5fcc                         @ 080b5fb0 0cdc
    subs r0,#0x35    @ 080b5fb2 3538
    cmp r4,r0                                @ 080b5fb4 8442
    bne LAB_080b5fba                         @ 080b5fb6 00d1
    b LAB_080b65d4                           @ 080b5fb8 0ce3
LAB_080b5fba:
    adds r0,#0x13    @ 080b5fba 1330
LAB_080b5fbc:
    cmp r4,r0                                @ 080b5fbc 8442
    bne LAB_080b5fc4                         @ 080b5fbe 01d1
    bl exec_equip_target_fallback_to_field_side @ 080b5fc0 00f098fc
LAB_080b5fc4:
    bl select_equip_target_for_opponent_random @ 080b5fc4 00f00cfe
DAT_080b5fc8:
    .word  0x00001475                     @ 080b5fc8 75140000
LAB_080b5fcc:
    ldr r0, DAT_080b5fdc                     @ 080b5fcc 0348
    cmp r4,r0                                @ 080b5fce 8442
    bne LAB_080b5fd4                         @ 080b5fd0 00d1
    b LAB_080b651a                           @ 080b5fd2 a2e2
LAB_080b5fd4:
    cmp r4,r0                                @ 080b5fd4 8442
    bgt LAB_080b5fe0                         @ 080b5fd6 03dc
    subs r0,#0x38    @ 080b5fd8 3838
    b LAB_080b62f6                           @ 080b5fda 8ce1
DAT_080b5fdc:
    .word  0x00001466                     @ 080b5fdc 66140000
LAB_080b5fe0:
    ldr r0, DAT_080b5ff0                     @ 080b5fe0 0348
    cmp r4,r0                                @ 080b5fe2 8442
    bne LAB_080b5fea                         @ 080b5fe4 01d1
    bl exec_equip_target_select_by_direction_bit @ 080b5fe6 00f0a9fc
LAB_080b5fea:
    bl select_equip_target_for_opponent_random @ 080b5fea 00f0f9fd
    .zero  0x2
DAT_080b5ff0:
    .word  0x0000146b                     @ 080b5ff0 6b140000
LAB_080b5ff4:
    ldr r0, DAT_080b6014                     @ 080b5ff4 0748
    cmp r4,r0                                @ 080b5ff6 8442
    bne LAB_080b5ffe                         @ 080b5ff8 01d1
    bl exec_equip_target_fallback_to_field_side @ 080b5ffa 00f07bfc
LAB_080b5ffe:
    cmp r4,r0                                @ 080b5ffe 8442
    bgt LAB_080b6028                         @ 080b6000 12dc
    subs r0,#0x8    @ 080b6002 0838
    cmp r4,r0                                @ 080b6004 8442
    bne LAB_080b600a                         @ 080b6006 00d1
    b LAB_080b65d4                           @ 080b6008 e4e2
LAB_080b600a:
    cmp r4,r0                                @ 080b600a 8442
    bgt LAB_080b6018                         @ 080b600c 04dc
    subs r0,#0x7    @ 080b600e 0738
    b LAB_080b62f6                           @ 080b6010 71e1
    .zero  0x2
DAT_080b6014:
    .word  0x0000148d                     @ 080b6014 8d140000
LAB_080b6018:
    ldr r0, DAT_080b6024                     @ 080b6018 0248
    cmp r4,r0                                @ 080b601a 8442
    bne LAB_080b6020                         @ 080b601c 00d1
    b LAB_080b65d4                           @ 080b601e d9e2
LAB_080b6020:
    bl select_equip_target_for_opponent_random @ 080b6020 00f0defd
DAT_080b6024:
    .word  0x00001487                     @ 080b6024 87140000
LAB_080b6028:
    ldr r0, DAT_080b6038                     @ 080b6028 0348
    cmp r4,r0                                @ 080b602a 8442
    bne LAB_080b6030                         @ 080b602c 00d1
    b LAB_080b6314                           @ 080b602e 71e1
LAB_080b6030:
    cmp r4,r0                                @ 080b6030 8442
    bgt LAB_080b603c                         @ 080b6032 03dc
    subs r0,#0x20    @ 080b6034 2038
    b LAB_080b61e4                           @ 080b6036 d5e0
DAT_080b6038:
    .word  0x000014b2                     @ 080b6038 b2140000
LAB_080b603c:
    ldr r0, DAT_080b6048                     @ 080b603c 0248
LAB_080b603e:
    cmp r4,r0                                @ 080b603e 8442
    bne LAB_080b6044                         @ 080b6040 00d1
    b LAB_080b6314                           @ 080b6042 67e1
LAB_080b6044:
    bl select_equip_target_for_opponent_random @ 080b6044 00f0ccfd
DAT_080b6048:
    .word  0x000014be                     @ 080b6048 be140000
LAB_080b604c:
    ldr r0, DAT_080b6090                     @ 080b604c 1048
    cmp r4,r0                                @ 080b604e 8442
    bne LAB_080b6054                         @ 080b6050 00d1
    b LAB_080b651a                           @ 080b6052 62e2
LAB_080b6054:
    cmp r4,r0                                @ 080b6054 8442
    ble LAB_080b605a                         @ 080b6056 00dd
    b LAB_080b61b0                           @ 080b6058 aae0
LAB_080b605a:
    subs r0,#0xe2    @ 080b605a e238
    cmp r4,r0                                @ 080b605c 8442
    bne LAB_080b6062                         @ 080b605e 00d1
    b LAB_080b651a                           @ 080b6060 5be2
LAB_080b6062:
    cmp r4,r0                                @ 080b6062 8442
    bgt LAB_080b6114                         @ 080b6064 56dc
    subs r0,#0xb1    @ 080b6066 b138
    cmp r4,r0                                @ 080b6068 8442
    bne LAB_080b6070                         @ 080b606a 01d1
    bl exec_equip_target_by_chain_effect_with_field_check @ 080b606c 00f029fd
LAB_080b6070:
    cmp r4,r0                                @ 080b6070 8442
    bgt LAB_080b60b8                         @ 080b6072 21dc
    subs r0,#0x4d    @ 080b6074 4d38
    cmp r4,r0                                @ 080b6076 8442
    bne LAB_080b607c                         @ 080b6078 00d1
    b LAB_080b6314                           @ 080b607a 4be1
LAB_080b607c:
    cmp r4,r0                                @ 080b607c 8442
    bgt LAB_080b6094                         @ 080b607e 09dc
    subs r0,#0x18    @ 080b6080 1838
    cmp r4,r0                                @ 080b6082 8442
    bne LAB_080b608a                         @ 080b6084 01d1
    bl exec_equip_target_by_chain_effect_with_field_check @ 080b6086 00f01cfd
LAB_080b608a:
    adds r0,#0xe    @ 080b608a 0e30
    b LAB_080b62f6                           @ 080b608c 33e1
    .zero  0x2
DAT_080b6090:
    .word  0x000016cb                     @ 080b6090 cb160000
LAB_080b6094:
    ldr r0, DAT_080b60b4                     @ 080b6094 0748
    cmp r4,r0                                @ 080b6096 8442
    bge LAB_080b609e                         @ 080b6098 01da
    bl select_equip_target_for_opponent_random @ 080b609a 00f0a1fd
LAB_080b609e:
    adds r0,#0x1    @ 080b609e 0130
    cmp r4,r0                                @ 080b60a0 8442
    bgt LAB_080b60a6                         @ 080b60a2 00dc
    b LAB_080b64d2                           @ 080b60a4 15e2
LAB_080b60a6:
    adds r0,#0xc    @ 080b60a6 0c30
    cmp r4,r0                                @ 080b60a8 8442
    bne LAB_080b60ae                         @ 080b60aa 00d1
    b LAB_080b6560                           @ 080b60ac 58e2
LAB_080b60ae:
    bl select_equip_target_for_opponent_random @ 080b60ae 00f097fd
    .zero  0x2
DAT_080b60b4:
    .word  0x0000152a                     @ 080b60b4 2a150000
LAB_080b60b8:
    ldr r0, DAT_080b60d4                     @ 080b60b8 0648
    cmp r4,r0                                @ 080b60ba 8442
    bne LAB_080b60c0                         @ 080b60bc 00d1
    b LAB_080b64d2                           @ 080b60be 08e2
LAB_080b60c0:
    cmp r4,r0                                @ 080b60c0 8442
    bgt LAB_080b60ec                         @ 080b60c2 13dc
    subs r0,#0x27    @ 080b60c4 2738
    cmp r4,r0                                @ 080b60c6 8442
    bne LAB_080b60cc                         @ 080b60c8 00d1
    b exec_equip_target_by_field5_score_scan @ 080b60ca 8de3
LAB_080b60cc:
    cmp r4,r0                                @ 080b60cc 8442
    bgt LAB_080b60d8                         @ 080b60ce 03dc
    subs r0,#0x15    @ 080b60d0 1538
    b LAB_080b62f6                           @ 080b60d2 10e1
DAT_080b60d4:
    .word  0x000015a8                     @ 080b60d4 a8150000
LAB_080b60d8:
    ldr r0, DAT_080b60e8                     @ 080b60d8 0348
    cmp r4,r0                                @ 080b60da 8442
    bne LAB_080b60e2                         @ 080b60dc 01d1
    bl exec_equip_target_by_comparator_field5_scored @ 080b60de 00f059fd
LAB_080b60e2:
    bl select_equip_target_for_opponent_random @ 080b60e2 00f07dfd
    .zero  0x2
DAT_080b60e8:
    .word  0x0000158e                     @ 080b60e8 8e150000
LAB_080b60ec:
    ldr r0, DAT_080b60fc                     @ 080b60ec 0348
    cmp r4,r0                                @ 080b60ee 8442
    bne LAB_080b60f4                         @ 080b60f0 00d1
    b LAB_080b64d2                           @ 080b60f2 eee1
LAB_080b60f4:
    cmp r4,r0                                @ 080b60f4 8442
    bgt LAB_080b6100                         @ 080b60f6 03dc
    subs r0,#0x3    @ 080b60f8 0338
    b LAB_080b62f6                           @ 080b60fa fce0
DAT_080b60fc:
    .word  0x000015b4                     @ 080b60fc b4150000
LAB_080b6100:
    ldr r0, DAT_080b6110                     @ 080b6100 0348
    cmp r4,r0                                @ 080b6102 8442
    bne LAB_080b610a                         @ 080b6104 01d1
    bl exec_equip_target_by_effect_chain_match @ 080b6106 00f02cfc
LAB_080b610a:
    bl select_equip_target_for_opponent_random @ 080b610a 00f069fd
    .zero  0x2
DAT_080b6110:
    .word  0x000015b8                     @ 080b6110 b8150000
LAB_080b6114:
    ldr r0, DAT_080b6144                     @ 080b6114 0b48
    cmp r4,r0                                @ 080b6116 8442
    bne LAB_080b611c                         @ 080b6118 00d1
    b LAB_080b651a                           @ 080b611a fee1
LAB_080b611c:
    cmp r4,r0                                @ 080b611c 8442
    bgt LAB_080b6164                         @ 080b611e 21dc
    subs r0,#0x44    @ 080b6120 4438
    cmp r4,r0                                @ 080b6122 8442
    bne LAB_080b6128                         @ 080b6124 00d1
    b LAB_080b6614                           @ 080b6126 75e2
LAB_080b6128:
    cmp r4,r0                                @ 080b6128 8442
    bgt LAB_080b6148                         @ 080b612a 0ddc
    subs r0,#0x18    @ 080b612c 1838
LAB_080b612e:
    cmp r4,r0                                @ 080b612e 8442
    ble LAB_080b6136                         @ 080b6130 01dd
    bl select_equip_target_for_opponent_random @ 080b6132 00f055fd
LAB_080b6136:
    subs r0,#0x1    @ 080b6136 0138
    cmp r4,r0                                @ 080b6138 8442
    bge LAB_080b6140                         @ 080b613a 01da
    bl select_equip_target_for_opponent_random @ 080b613c 00f050fd
LAB_080b6140:
    b LAB_080b64d2                           @ 080b6140 c7e1
    .zero  0x2
DAT_080b6144:
    .word  0x00001656                     @ 080b6144 56160000
LAB_080b6148:
    ldr r0, DAT_080b6158                     @ 080b6148 0348
    cmp r4,r0                                @ 080b614a 8442
    bne LAB_080b6150                         @ 080b614c 00d1
    b LAB_080b64d2                           @ 080b614e c0e1
LAB_080b6150:
    cmp r4,r0                                @ 080b6150 8442
    bgt LAB_080b615c                         @ 080b6152 03dc
    subs r0,#0x7    @ 080b6154 0738
    b LAB_080b62f6                           @ 080b6156 cee0
DAT_080b6158:
    .word  0x0000161e                     @ 080b6158 1e160000
LAB_080b615c:
    ldr r0, DAT_080b6160                     @ 080b615c 0048
    b LAB_080b6252                           @ 080b615e 78e0
DAT_080b6160:
    .word  0x00001624                     @ 080b6160 24160000
LAB_080b6164:
    ldr r0, DAT_080b6188                     @ 080b6164 0848
    cmp r4,r0                                @ 080b6166 8442
    bne LAB_080b616c                         @ 080b6168 00d1
    b LAB_080b657c                           @ 080b616a 07e2
LAB_080b616c:
    cmp r4,r0                                @ 080b616c 8442
    bgt LAB_080b6194                         @ 080b616e 11dc
    subs r0,#0x21    @ 080b6170 2138
    cmp r4,r0                                @ 080b6172 8442
    bne LAB_080b6178                         @ 080b6174 00d1
    b LAB_080b64d2                           @ 080b6176 ace1
LAB_080b6178:
    cmp r4,r0                                @ 080b6178 8442
    bgt LAB_080b618c                         @ 080b617a 07dc
    subs r0,#0x6    @ 080b617c 0638
    cmp r4,r0                                @ 080b617e 8442
    bne LAB_080b6184                         @ 080b6180 00d1
    b LAB_080b6672                           @ 080b6182 76e2
LAB_080b6184:
    bl select_equip_target_for_opponent_random @ 080b6184 00f02cfd
DAT_080b6188:
    .word  0x00001690                     @ 080b6188 90160000
LAB_080b618c:
    ldr r0, DAT_080b6190                     @ 080b618c 0048
    b LAB_080b6306                           @ 080b618e bae0
DAT_080b6190:
    .word  0x00001685                     @ 080b6190 85160000
LAB_080b6194:
    ldr r0, DAT_080b61a4                     @ 080b6194 0348
    cmp r4,r0                                @ 080b6196 8442
    bne LAB_080b619c                         @ 080b6198 00d1
    b LAB_080b651a                           @ 080b619a bee1
LAB_080b619c:
    cmp r4,r0                                @ 080b619c 8442
    bgt LAB_080b61a8                         @ 080b619e 03dc
    subs r0,#0x17    @ 080b61a0 1738
    b LAB_080b6212                           @ 080b61a2 36e0
DAT_080b61a4:
    .word  0x000016ab                     @ 080b61a4 ab160000
LAB_080b61a8:
    ldr r0, DAT_080b61ac                     @ 080b61a8 0048
    b LAB_080b6306                           @ 080b61aa ace0
DAT_080b61ac:
    .word  0x000016ba                     @ 080b61ac ba160000
LAB_080b61b0:
    ldr r0, DAT_080b61f0                     @ 080b61b0 0f48
    cmp r4,r0                                @ 080b61b2 8442
    bne LAB_080b61ba                         @ 080b61b4 01d1
    bl exec_equip_target_by_chain_effect_type_mask @ 080b61b6 00f05bfc
LAB_080b61ba:
    cmp r4,r0                                @ 080b61ba 8442
    bgt LAB_080b6268                         @ 080b61bc 54dc
    subs r0,#0xfe    @ 080b61be fe38
    cmp r4,r0                                @ 080b61c0 8442
    bgt LAB_080b6224                         @ 080b61c2 2fdc
    subs r0,#0x1    @ 080b61c4 0138
    cmp r4,r0                                @ 080b61c6 8442
    blt LAB_080b61cc                         @ 080b61c8 00db
    b LAB_080b64d2                           @ 080b61ca 82e1
LAB_080b61cc:
    subs r0,#0x34    @ 080b61cc 3438
    cmp r4,r0                                @ 080b61ce 8442
    bne LAB_080b61d4                         @ 080b61d0 00d1
    b LAB_080b64d2                           @ 080b61d2 7ee1
LAB_080b61d4:
    cmp r4,r0                                @ 080b61d4 8442
    bgt LAB_080b61f4                         @ 080b61d6 0ddc
    subs r0,#0x4a    @ 080b61d8 4a38
    cmp r4,r0                                @ 080b61da 8442
    bne LAB_080b61e2                         @ 080b61dc 01d1
    bl exec_equip_target_by_field6_score_and_effect @ 080b61de 00f029fc
LAB_080b61e2:
    adds r0,#0x15    @ 080b61e2 1530
LAB_080b61e4:
    cmp r4,r0                                @ 080b61e4 8442
    bne LAB_080b61ea                         @ 080b61e6 00d1
    b exec_equip_target_by_active_side_bitmap @ 080b61e8 e2e2
LAB_080b61ea:
    bl select_equip_target_for_opponent_random @ 080b61ea 00f0f9fc
    .zero  0x2
DAT_080b61f0:
    .word  0x0000184b                     @ 080b61f0 4b180000
LAB_080b61f4:
    ldr r0, DAT_080b620c                     @ 080b61f4 0548
    cmp r4,r0                                @ 080b61f6 8442
    bne LAB_080b61fc                         @ 080b61f8 00d1
    b LAB_080b651a                           @ 080b61fa 8ee1
LAB_080b61fc:
    cmp r4,r0                                @ 080b61fc 8442
    bgt LAB_080b6210                         @ 080b61fe 07dc
    subs r0,#0xd    @ 080b6200 0d38
    cmp r4,r0                                @ 080b6202 8442
    bne LAB_080b6208                         @ 080b6204 00d1
    b LAB_080b653c                           @ 080b6206 99e1
LAB_080b6208:
    bl select_equip_target_for_opponent_random @ 080b6208 00f0eafc
DAT_080b620c:
    .word  0x00001727                     @ 080b620c 27170000
LAB_080b6210:
    ldr r0, DAT_080b6220                     @ 080b6210 0348
LAB_080b6212:
    cmp r4,r0                                @ 080b6212 8442
    bne LAB_080b621a                         @ 080b6214 01d1
    bl exec_equip_target_by_comparator_then_scored_fallback @ 080b6216 00f09bfc
LAB_080b621a:
    bl select_equip_target_for_opponent_random @ 080b621a 00f0e1fc
    .zero  0x2
DAT_080b6220:
    .word  0x0000172a                     @ 080b6220 2a170000
LAB_080b6224:
    ldr r0, DAT_080b6240                     @ 080b6224 0648
    cmp r4,r0                                @ 080b6226 8442
    bne LAB_080b622c                         @ 080b6228 00d1
    b LAB_080b64d2                           @ 080b622a 52e1
LAB_080b622c:
    cmp r4,r0                                @ 080b622c 8442
    bgt LAB_080b6244                         @ 080b622e 09dc
    subs r0,#0x4c    @ 080b6230 4c38
    cmp r4,r0                                @ 080b6232 8442
    bne LAB_080b623a                         @ 080b6234 01d1
    bl exec_equip_target_by_comparator_then_scored_fallback @ 080b6236 00f08bfc
LAB_080b623a:
    adds r0,#0xc    @ 080b623a 0c30
    b LAB_080b62f6                           @ 080b623c 5be0
    .zero  0x2
DAT_080b6240:
    .word  0x000017da                     @ 080b6240 da170000
LAB_080b6244:
    ldr r0, DAT_080b625c                     @ 080b6244 0548
    cmp r4,r0                                @ 080b6246 8442
    bne LAB_080b624c                         @ 080b6248 00d1
    b LAB_080b6394                           @ 080b624a a3e0
LAB_080b624c:
    cmp r4,r0                                @ 080b624c 8442
    bgt LAB_080b6260                         @ 080b624e 07dc
    subs r0,#0x46    @ 080b6250 4638
LAB_080b6252:
    cmp r4,r0                                @ 080b6252 8442
    bne LAB_080b6258                         @ 080b6254 00d1
    b LAB_080b6614                           @ 080b6256 dde1
LAB_080b6258:
    bl select_equip_target_for_opponent_random @ 080b6258 00f0c2fc
DAT_080b625c:
    .word  0x00001842                     @ 080b625c 42180000
LAB_080b6260:
    ldr r0, DAT_080b6264                     @ 080b6260 0048
    b LAB_080b6306                           @ 080b6262 50e0
DAT_080b6264:
    .word  0x00001844                     @ 080b6264 44180000
LAB_080b6268:
    ldr r0, DAT_080b628c                     @ 080b6268 0848
    cmp r4,r0                                @ 080b626a 8442
    bne LAB_080b6270                         @ 080b626c 00d1
    b LAB_080b64d2                           @ 080b626e 30e1
LAB_080b6270:
    cmp r4,r0                                @ 080b6270 8442
    bgt LAB_080b62b4                         @ 080b6272 1fdc
    subs r0,#0x32    @ 080b6274 3238
    cmp r4,r0                                @ 080b6276 8442
    bne LAB_080b627c                         @ 080b6278 00d1
    b LAB_080b668c                           @ 080b627a 07e2
LAB_080b627c:
    cmp r4,r0                                @ 080b627c 8442
    bgt LAB_080b6290                         @ 080b627e 07dc
    subs r0,#0x36    @ 080b6280 3638
    cmp r4,r0                                @ 080b6282 8442
    bne LAB_080b6288                         @ 080b6284 00d1
    b LAB_080b6652                           @ 080b6286 e4e1
LAB_080b6288:
    adds r0,#0x1b    @ 080b6288 1b30
    b LAB_080b6306                           @ 080b628a 3ce0
DAT_080b628c:
    .word  0x000018bb                     @ 080b628c bb180000
LAB_080b6290:
    ldr r0, DAT_080b62a8                     @ 080b6290 0548
    cmp r4,r0                                @ 080b6292 8442
    bne LAB_080b6298                         @ 080b6294 00d1
    b LAB_080b6614                           @ 080b6296 bde1
LAB_080b6298:
    cmp r4,r0                                @ 080b6298 8442
    bgt LAB_080b62ac                         @ 080b629a 07dc
    subs r0,#0x9    @ 080b629c 0938
    cmp r4,r0                                @ 080b629e 8442
    bne LAB_080b62a4                         @ 080b62a0 00d1
    b LAB_080b69c4                           @ 080b62a2 8fe3
LAB_080b62a4:
    bl select_equip_target_for_opponent_random @ 080b62a4 00f09cfc
DAT_080b62a8:
    .word  0x00001893                     @ 080b62a8 93180000
LAB_080b62ac:
    ldr r0, DAT_080b62b0                     @ 080b62ac 0048
    b LAB_080b6306                           @ 080b62ae 2ae0
DAT_080b62b0:
    .word  0x000018ba                     @ 080b62b0 ba180000
LAB_080b62b4:
    ldr r0, DAT_080b62d4                     @ 080b62b4 0748
    cmp r4,r0                                @ 080b62b6 8442
    bne LAB_080b62bc                         @ 080b62b8 00d1
    b exec_equip_target_by_active_side_bitmap @ 080b62ba 79e2
LAB_080b62bc:
    cmp r4,r0                                @ 080b62bc 8442
    bgt LAB_080b62e8                         @ 080b62be 13dc
    subs r0,#0x3d    @ 080b62c0 3d38
    cmp r4,r0                                @ 080b62c2 8442
    bne LAB_080b62ca                         @ 080b62c4 01d1
    bl exec_equip_target_by_comparator_field5_scored @ 080b62c6 00f065fc
LAB_080b62ca:
    cmp r4,r0                                @ 080b62ca 8442
    bgt LAB_080b62d8                         @ 080b62cc 04dc
    subs r0,#0x2a    @ 080b62ce 2a38
    b LAB_080b6306                           @ 080b62d0 19e0
    .zero  0x2
DAT_080b62d4:
    .word  0x0000192d                     @ 080b62d4 2d190000
LAB_080b62d8:
    ldr r0, DAT_080b62e4                     @ 080b62d8 0248
LAB_080b62da:
    cmp r4,r0                                @ 080b62da 8442
    bne LAB_080b62e0                         @ 080b62dc 00d1
    b exec_equip_target_by_field5_score_scan @ 080b62de 83e2
LAB_080b62e0:
    bl select_equip_target_for_opponent_random @ 080b62e0 00f07efc
DAT_080b62e4:
    .word  0x00001913                     @ 080b62e4 13190000
LAB_080b62e8:
    ldr r0, DAT_080b6300                     @ 080b62e8 0548
    cmp r4,r0                                @ 080b62ea 8442
    bne LAB_080b62f0                         @ 080b62ec 00d1
    b LAB_080b69e0                           @ 080b62ee 77e3
LAB_080b62f0:
    cmp r4,r0                                @ 080b62f0 8442
    bgt LAB_080b6304                         @ 080b62f2 07dc
    subs r0,#0x16    @ 080b62f4 1638
LAB_080b62f6:
    cmp r4,r0                                @ 080b62f6 8442
    bne LAB_080b62fc                         @ 080b62f8 00d1
    b LAB_080b64d2                           @ 080b62fa eae0
LAB_080b62fc:
    bl select_equip_target_for_opponent_random @ 080b62fc 00f070fc
DAT_080b6300:
    .word  0x00001978                     @ 080b6300 78190000
LAB_080b6304:
    ldr r0, DAT_080b6310                     @ 080b6304 0248
LAB_080b6306:
    cmp r4,r0                                @ 080b6306 8442
    bne LAB_080b630c                         @ 080b6308 00d1
    b LAB_080b651a                           @ 080b630a 06e1
LAB_080b630c:
    bl select_equip_target_for_opponent_random @ 080b630c 00f068fc
DAT_080b6310:
    .word  0x000019db                     @ 080b6310 db190000
LAB_080b6314:
    ldr r2, DWORD_080b6344                   @ 080b6314 0b4a
    .hword 0x4641    @ 080b6316 4146
    lsls r0,r1,#0x1f    @ 080b6318 c807
    lsrs r0,r0,#0x1f    @ 080b631a c00f
    movs r4,#0x1    @ 080b631c 0124
    subs r0,r4,r0    @ 080b631e 201a
    ldr r3,[r2,#0x0]                         @ 080b6320 1368
    cmp r3,r0                                @ 080b6322 8342
    bne LAB_080b6348                         @ 080b6324 10d1
    lsls r1,r3,#0x4    @ 080b6326 1901
    ldr r2,[r2,#0x1c]                        @ 080b6328 d269
    adds r1,r1,r2    @ 080b632a 8918
    adds r0,r4,#0x0    @ 080b632c 201c
    lsls r0,r1    @ 080b632e 8840
    .hword 0x464f    @ 080b6330 4f46
    ands r0,r7    @ 080b6332 3840
    cmp r0,#0x0                              @ 080b6334 0028
    bne LAB_080b633c                         @ 080b6336 01d1
    bl select_equip_target_for_opponent_random @ 080b6338 00f052fc
LAB_080b633c:
    adds r0,r6,#0x0    @ 080b633c 301c
    adds r1,r3,#0x0    @ 080b633e 191c
    bl enqueue_equip_slot_sprite_success     @ 080b6340 00f04afc
DWORD_080b6344:
    .word  0x0201bb90                     @ 080b6344 90bb0102
LAB_080b6348:
    ldr r3,[r2,#0x4]                         @ 080b6348 5368
    lsls r1,r3,#0x4    @ 080b634a 1901
    ldr r2,[r2,#0x20]                        @ 080b634c 126a
    adds r1,r1,r2    @ 080b634e 8918
    adds r0,r4,#0x0    @ 080b6350 201c
    lsls r0,r1    @ 080b6352 8840
    .hword 0x4649    @ 080b6354 4946
    ands r0,r1    @ 080b6356 0840
    cmp r0,#0x0                              @ 080b6358 0028
    bne LAB_080b6360                         @ 080b635a 01d1
    bl select_equip_target_for_opponent_random @ 080b635c 00f040fc
LAB_080b6360:
    adds r0,r6,#0x0    @ 080b6360 301c
    adds r1,r3,#0x0    @ 080b6362 191c
    bl enqueue_equip_slot_sprite_success     @ 080b6364 00f038fc
LAB_080b6368:
    ldr r0, DWORD_080b6390                   @ 080b6368 0948
    ldr r1,[r0,#0x4]                         @ 080b636a 4168
    lsls r1,r1,#0x4    @ 080b636c 0901
    ldr r2,[r0,#0x20]                        @ 080b636e 026a
    adds r1,r1,r2    @ 080b6370 8918
    movs r0,#0x1    @ 080b6372 0120
    lsls r0,r1    @ 080b6374 8840
    .hword 0x464b    @ 080b6376 4b46
    ands r0,r3    @ 080b6378 1840
    cmp r0,#0x0                              @ 080b637a 0028
    bne LAB_080b6382                         @ 080b637c 01d1
    bl select_equip_target_for_opponent_random @ 080b637e 00f02ffc
LAB_080b6382:
    .hword 0x4647    @ 080b6382 4746
    lsls r1,r7,#0x1f    @ 080b6384 f907
    lsrs r1,r1,#0x1f    @ 080b6386 c90f
    adds r0,r6,#0x0    @ 080b6388 301c
    bl enqueue_equip_slot_sprite_success     @ 080b638a 00f025fc
    movs r0,r0    @ 080b638e 0000
DWORD_080b6390:
    .word  0x0201bb90                     @ 080b6390 90bb0102
LAB_080b6394:
    .hword 0x4640    @ 080b6394 4046
    lsls r5,r0,#0x1f    @ 080b6396 c507
    lsrs r7,r5,#0x1f    @ 080b6398 ef0f
    ldrh r1,[r6,#0x0]                        @ 080b639a 3188
    ldr r0, DAT_080b63c0                     @ 080b639c 0848
    cmp r1,r0                                @ 080b639e 8142
    bgt LAB_080b63c8                         @ 080b63a0 12dc
    subs r0,#0x1    @ 080b63a2 0138
    cmp r1,r0                                @ 080b63a4 8142
    bge LAB_080b6428                         @ 080b63a6 3fda
    ldr r0, DAT_080b63c4                     @ 080b63a8 0648
    cmp r1,r0                                @ 080b63aa 8142
    beq LAB_080b63fc                         @ 080b63ac 26d0
    cmp r1,r0                                @ 080b63ae 8142
    blt LAB_080b645c                         @ 080b63b0 54db
    adds r0,#0xd7    @ 080b63b2 d730
    cmp r1,r0                                @ 080b63b4 8142
    bgt LAB_080b645c                         @ 080b63b6 51dc
    subs r0,#0x1    @ 080b63b8 0138
    cmp r1,r0                                @ 080b63ba 8142
    blt LAB_080b645c                         @ 080b63bc 4edb
    b LAB_080b6428                           @ 080b63be 33e0
DAT_080b63c0:
    .word  0x000013ea                     @ 080b63c0 ea130000
DAT_080b63c4:
    .word  0x00001237                     @ 080b63c4 37120000
LAB_080b63c8:
    ldr r0, DAT_080b63e0                     @ 080b63c8 0548
    cmp r1,r0                                @ 080b63ca 8142
    beq LAB_080b6428                         @ 080b63cc 2cd0
    cmp r1,r0                                @ 080b63ce 8142
    bgt LAB_080b63e8                         @ 080b63d0 0adc
    ldr r0, DAT_080b63e4                     @ 080b63d2 0448
    cmp r1,r0                                @ 080b63d4 8142
    beq LAB_080b6428                         @ 080b63d6 27d0
    adds r0,#0xaa    @ 080b63d8 aa30
    cmp r1,r0                                @ 080b63da 8142
    beq LAB_080b6428                         @ 080b63dc 24d0
    b LAB_080b645c                           @ 080b63de 3de0
DAT_080b63e0:
    .word  0x00001842                     @ 080b63e0 42180000
DAT_080b63e4:
    .word  0x000013f3                     @ 080b63e4 f3130000
LAB_080b63e8:
    ldr r0, DWORD_080b63f8                   @ 080b63e8 0348
    cmp r1,r0                                @ 080b63ea 8142
    beq LAB_080b6428                         @ 080b63ec 1cd0
    adds r0,#0xaf    @ 080b63ee af30
    cmp r1,r0                                @ 080b63f0 8142
    beq LAB_080b6434                         @ 080b63f2 1fd0
    b LAB_080b645c                           @ 080b63f4 32e0
    .zero  0x2
DWORD_080b63f8:
    .word  0x000018d1                     @ 080b63f8 d1180000
LAB_080b63fc:
    ldr r3, PTR_gP1LifePoints_080b6420       @ 080b63fc 084b
    movs r4,#0x1    @ 080b63fe 0124
    lsrs r0,r5,#0x1f    @ 080b6400 e80f
    ldr r2, DAT_080b6424                     @ 080b6402 084a
    adds r1,r0,#0x0    @ 080b6404 011c
    muls r1,r2    @ 080b6406 5143
    adds r1,r1,r3    @ 080b6408 c918
    subs r0,r4,r0    @ 080b640a 201a
    ands r0,r4    @ 080b640c 2040
    muls r0,r2    @ 080b640e 5043
    adds r0,r0,r3    @ 080b6410 c018
    ldr r1,[r1,#0x0]                         @ 080b6412 0968
    ldr r0,[r0,#0x0]                         @ 080b6414 0068
    cmp r1,r0                                @ 080b6416 8142
    ble LAB_080b645c                         @ 080b6418 20dd
    lsrs r0,r5,#0x1f    @ 080b641a e80f
    subs r7,r4,r0    @ 080b641c 271a
    b LAB_080b645c                           @ 080b641e 1de0
PTR_gP1LifePoints_080b6420:
    .word  gP1LifePoints                  @ 080b6420 e0c40102
DAT_080b6424:
    .word  0x00000868                     @ 080b6424 68080000
LAB_080b6428:
    .hword 0x4641    @ 080b6428 4146
    lsls r0,r1,#0x1f    @ 080b642a c807
    lsrs r0,r0,#0x1f    @ 080b642c c00f
    movs r1,#0x1    @ 080b642e 0121
    subs r7,r1,r0    @ 080b6430 0f1a
    b LAB_080b645c                           @ 080b6432 13e0
LAB_080b6434:
    ldr r2, DAT_080b6458                     @ 080b6434 084a
    lsrs r0,r5,#0x1f    @ 080b6436 e80f
    ldr r1,[r2,#0x4]                         @ 080b6438 5168
    cmp r1,r0                                @ 080b643a 8142
    bne LAB_080b645c                         @ 080b643c 0ed1
    lsls r1,r1,#0x4    @ 080b643e 0901
    ldr r2,[r2,#0x20]                        @ 080b6440 126a
    adds r1,r1,r2    @ 080b6442 8918
    movs r0,#0x1    @ 080b6444 0120
    lsls r0,r1    @ 080b6446 8840
    .hword 0x464b    @ 080b6448 4b46
    ands r0,r3    @ 080b644a 1840
    cmp r0,#0x0                              @ 080b644c 0028
    beq LAB_080b645c                         @ 080b644e 05d0
    lsrs r1,r5,#0x1f    @ 080b6450 e90f
    adds r0,r6,#0x0    @ 080b6452 301c
    b enqueue_equip_slot_sprite_success      @ 080b6454 c0e3
    .zero  0x2
DAT_080b6458:
    .word  0x0201bb90                     @ 080b6458 90bb0102
LAB_080b645c:
    movs r5,#0x1    @ 080b645c 0125
    rsbs r5,r5,#0    @ 080b645e 6d42
    adds r0,r6,#0x0    @ 080b6460 301c
    adds r1,r7,#0x0    @ 080b6462 391c
    adds r2,r5,#0x0    @ 080b6464 2a1c
    movs r3,#0x1    @ 080b6466 0123
    bl find_best_equip_target_slot_scored    @ 080b6468 f8f75afe
    adds r2,r0,#0x0    @ 080b646c 021c
    cmp r2,#0x0                              @ 080b646e 002a
    blt LAB_080b6478                         @ 080b6470 02db
    adds r0,r6,#0x0    @ 080b6472 301c
    adds r1,r7,#0x0    @ 080b6474 391c
    b enqueue_equip_slot_sprite_success      @ 080b6476 afe3
LAB_080b6478:
    movs r0,#0x1    @ 080b6478 0120
    subs r4,r0,r7    @ 080b647a c41b
    adds r0,r6,#0x0    @ 080b647c 301c
    adds r1,r4,#0x0    @ 080b647e 211c
    adds r2,r5,#0x0    @ 080b6480 2a1c
    movs r3,#0x1    @ 080b6482 0123
    bl find_best_equip_target_slot_scored    @ 080b6484 f8f74cfe
    adds r2,r0,#0x0    @ 080b6488 021c
    cmp r2,#0x0                              @ 080b648a 002a
    bge LAB_080b6490                         @ 080b648c 00da
    b select_equip_target_for_opponent_random @ 080b648e a7e3
LAB_080b6490:
    adds r0,r6,#0x0    @ 080b6490 301c
    adds r1,r4,#0x0    @ 080b6492 211c
    b enqueue_equip_slot_sprite_success      @ 080b6494 a0e3
LAB_080b6496:
    ldr r4, PTR_gP1LifePoints_080b64f4       @ 080b6496 174c
    ldr r7, DAT_080b64f8                     @ 080b6498 174f
    adds r0,r4,r7    @ 080b649a e019
    lsrs r1,r3,#0x1f    @ 080b649c d90f
    ldr r2,[r0,#0x0]                         @ 080b649e 0268
    cmp r2,r1                                @ 080b64a0 8a42
    beq LAB_080b64ae                         @ 080b64a2 04d0
    ldr r1, DAT_080b64fc                     @ 080b64a4 1549
    adds r0,r4,r1    @ 080b64a6 6018
    ldr r0,[r0,#0x0]                         @ 080b64a8 0068
    cmp r0,#0x5                              @ 080b64aa 0528
    beq LAB_080b64be                         @ 080b64ac 07d0
LAB_080b64ae:
    lsrs r0,r3,#0x1f    @ 080b64ae d80f
    cmp r2,r0                                @ 080b64b0 8242
    bne LAB_080b64d2                         @ 080b64b2 0ed1
    ldr r3, DAT_080b64fc                     @ 080b64b4 114b
    adds r0,r4,r3    @ 080b64b6 e018
    ldr r0,[r0,#0x0]                         @ 080b64b8 0068
    cmp r0,#0x1                              @ 080b64ba 0128
    bhi LAB_080b64d2                         @ 080b64bc 09d8
LAB_080b64be:
    ldrb r7,[r6,#0x2]                        @ 080b64be b778
    lsls r0,r7,#0x1f    @ 080b64c0 f807
    lsrs r0,r0,#0x1f    @ 080b64c2 c00f
    ldr r1, DAT_080b6500                     @ 080b64c4 0e49
    bl find_equip_slot_by_card_id            @ 080b64c6 7bf7f5ff
    adds r4,r0,#0x0    @ 080b64ca 041c
    cmp r4,#0x0                              @ 080b64cc 002c
    blt LAB_080b64d2                         @ 080b64ce 00db
    b LAB_080b6bce                           @ 080b64d0 7de3
LAB_080b64d2:
    ldrb r1,[r6,#0x2]                        @ 080b64d2 b178
    lsls r0,r1,#0x1f    @ 080b64d4 c807
    lsrs r0,r0,#0x1f    @ 080b64d6 c00f
    movs r5,#0x1    @ 080b64d8 0125
    subs r0,r5,r0    @ 080b64da 281a
    .hword 0x4649    @ 080b64dc 4946
    movs r2,#0x1    @ 080b64de 0122
    bl select_equip_target_slot_with_eligibility_check @ 080b64e0 fef732ff
    adds r4,r0,#0x0    @ 080b64e4 041c
    cmp r4,#0x0                              @ 080b64e6 002c
    blt LAB_080b6504                         @ 080b64e8 0cdb
    ldrb r3,[r6,#0x2]                        @ 080b64ea b378
    lsls r1,r3,#0x1f    @ 080b64ec d907
    lsrs r1,r1,#0x1f    @ 080b64ee c90f
    subs r1,r5,r1    @ 080b64f0 691a
    b LAB_080b6bd4                           @ 080b64f2 6fe3
PTR_gP1LifePoints_080b64f4:
    .word  gP1LifePoints                  @ 080b64f4 e0c40102
DAT_080b64f8:
    .word  0x00001ce8                     @ 080b64f8 e81c0000
DAT_080b64fc:
    .word  0x00001cf4                     @ 080b64fc f41c0000
DAT_080b6500:
    .word  0x00001539                     @ 080b6500 39150000
LAB_080b6504:
    ldrb r7,[r6,#0x2]                        @ 080b6504 b778
    lsls r0,r7,#0x1f    @ 080b6506 f807
    lsrs r0,r0,#0x1f    @ 080b6508 c00f
    .hword 0x4649    @ 080b650a 4946
    bl select_equip_target_slot_by_eligible_set @ 080b650c fef7d8ff
    adds r4,r0,#0x0    @ 080b6510 041c
    cmp r4,#0x0                              @ 080b6512 002c
    bge LAB_080b6518                         @ 080b6514 00da
    b select_equip_target_for_opponent_random @ 080b6516 63e3
LAB_080b6518:
    b LAB_080b6bce                           @ 080b6518 59e3
LAB_080b651a:
    ldrb r1,[r6,#0x2]                        @ 080b651a b178
    lsls r0,r1,#0x1f    @ 080b651c c807
    lsrs r0,r0,#0x1f    @ 080b651e c00f
    movs r5,#0x1    @ 080b6520 0125
    subs r0,r5,r0    @ 080b6522 281a
    .hword 0x4649    @ 080b6524 4946
    movs r2,#0x0    @ 080b6526 0022
    bl select_equip_target_slot_with_eligibility_check @ 080b6528 fef70eff
    adds r4,r0,#0x0    @ 080b652c 041c
    cmp r4,#0x0                              @ 080b652e 002c
    blt LAB_080b6504                         @ 080b6530 e8db
    ldrb r3,[r6,#0x2]                        @ 080b6532 b378
    lsls r1,r3,#0x1f    @ 080b6534 d907
    lsrs r1,r1,#0x1f    @ 080b6536 c90f
    subs r1,r5,r1    @ 080b6538 691a
    b LAB_080b6bd4                           @ 080b653a 4be3
LAB_080b653c:
    lsrs r0,r3,#0x1f    @ 080b653c d80f
    movs r5,#0x1    @ 080b653e 0125
    subs r0,r5,r0    @ 080b6540 281a
    ldr r2, DAT_080b655c                     @ 080b6542 064a
    .hword 0x4649    @ 080b6544 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b6546 fef70ffd
    adds r4,r0,#0x0    @ 080b654a 041c
    cmp r4,#0x0                              @ 080b654c 002c
    bge LAB_080b6552                         @ 080b654e 00da
    b select_equip_target_for_opponent_random @ 080b6550 46e3
LAB_080b6552:
    ldrb r3,[r6,#0x2]                        @ 080b6552 b378
    lsls r1,r3,#0x1f    @ 080b6554 d907
    lsrs r1,r1,#0x1f    @ 080b6556 c90f
    subs r1,r5,r1    @ 080b6558 691a
    b LAB_080b6bd4                           @ 080b655a 3be3
DAT_080b655c:
    .word  0x080b5c2d                     @ 080b655c 2d5c0b08
LAB_080b6560:
    lsrs r0,r3,#0x1f    @ 080b6560 d80f
    ldr r2, DAT_080b6578                     @ 080b6562 054a
    .hword 0x4649    @ 080b6564 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b6566 fef7fffc
    adds r4,r0,#0x0    @ 080b656a 041c
    cmp r4,#0x0                              @ 080b656c 002c
    bge LAB_080b6572                         @ 080b656e 00da
    b select_equip_target_for_opponent_random @ 080b6570 36e3
LAB_080b6572:
    ldrb r7,[r6,#0x2]                        @ 080b6572 b778
    lsls r1,r7,#0x1f    @ 080b6574 f907
    b LAB_080b6bd2                           @ 080b6576 2ce3
DAT_080b6578:
    .word  0x080b5bad                     @ 080b6578 ad5b0b08
LAB_080b657c:
    ldr r0, PTR_gP1LifePoints_080b65a8       @ 080b657c 0a48
    ldr r1, DAT_080b65ac                     @ 080b657e 0b49
    adds r0,r0,r1    @ 080b6580 4018
    lsrs r1,r3,#0x1f    @ 080b6582 d90f
    ldr r0,[r0,#0x0]                         @ 080b6584 0068
    cmp r0,r1                                @ 080b6586 8842
    beq LAB_080b65b0                         @ 080b6588 12d0
    adds r0,r1,#0x0    @ 080b658a 081c
    lsls r0,r0,#0x4    @ 080b658c 0001
    lsls r2,r2,#0x1a    @ 080b658e 9206
    lsrs r1,r2,#0x1b    @ 080b6590 d10e
    adds r0,r0,r1    @ 080b6592 4018
    movs r1,#0x1    @ 080b6594 0121
    lsls r1,r0    @ 080b6596 8140
    .hword 0x464f    @ 080b6598 4f46
    ands r1,r7    @ 080b659a 3940
    cmp r1,#0x0                              @ 080b659c 0029
    beq LAB_080b65b0                         @ 080b659e 07d0
    lsrs r1,r3,#0x1f    @ 080b65a0 d90f
    lsrs r2,r2,#0x1b    @ 080b65a2 d20e
    adds r0,r6,#0x0    @ 080b65a4 301c
    b enqueue_equip_slot_sprite_success      @ 080b65a6 17e3
PTR_gP1LifePoints_080b65a8:
    .word  gP1LifePoints                  @ 080b65a8 e0c40102
DAT_080b65ac:
    .word  0x00001ce8                     @ 080b65ac e81c0000
LAB_080b65b0:
    ldrb r0,[r6,#0x2]                        @ 080b65b0 b078
    lsls r1,r0,#0x1f    @ 080b65b2 c107
    lsrs r1,r1,#0x1f    @ 080b65b4 c90f
    movs r0,#0x1    @ 080b65b6 0120
    rsbs r0,r0,#0    @ 080b65b8 4042
    str r0,[sp,#0x0]                         @ 080b65ba 0090
    adds r0,r6,#0x0    @ 080b65bc 301c
    movs r2,#0x1    @ 080b65be 0122
    movs r3,#0x1    @ 080b65c0 0123
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b65c2 fef7b3fc
    adds r4,r0,#0x0    @ 080b65c6 041c
    cmp r4,#0x0                              @ 080b65c8 002c
    bge LAB_080b65ce                         @ 080b65ca 00da
    b select_equip_target_for_opponent_random @ 080b65cc 08e3
LAB_080b65ce:
    ldrb r3,[r6,#0x2]                        @ 080b65ce b378
    lsls r1,r3,#0x1f    @ 080b65d0 d907
    b LAB_080b6bd2                           @ 080b65d2 fee2
LAB_080b65d4:
    .hword 0x4647    @ 080b65d4 4746
    lsls r0,r7,#0x1f    @ 080b65d6 f807
    lsrs r0,r0,#0x1f    @ 080b65d8 c00f
    movs r7,#0x1    @ 080b65da 0127
    subs r4,r7,r0    @ 080b65dc 3c1a
    movs r5,#0x1    @ 080b65de 0125
    rsbs r5,r5,#0    @ 080b65e0 6d42
    str r5,[sp,#0x0]                         @ 080b65e2 0095
    adds r0,r6,#0x0    @ 080b65e4 301c
    adds r1,r4,#0x0    @ 080b65e6 211c
    movs r2,#0x1    @ 080b65e8 0122
    movs r3,#0x1    @ 080b65ea 0123
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b65ec fef79efc
    adds r2,r0,#0x0    @ 080b65f0 021c
    cmp r2,#0x0                              @ 080b65f2 002a
    bge LAB_080b660e                         @ 080b65f4 0bda
    subs r4,r7,r4    @ 080b65f6 3c1b
    str r5,[sp,#0x0]                         @ 080b65f8 0095
    adds r0,r6,#0x0    @ 080b65fa 301c
    adds r1,r4,#0x0    @ 080b65fc 211c
    adds r2,r5,#0x0    @ 080b65fe 2a1c
    adds r3,r5,#0x0    @ 080b6600 2b1c
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b6602 fef793fc
    adds r2,r0,#0x0    @ 080b6606 021c
    cmp r2,#0x0                              @ 080b6608 002a
    bge LAB_080b660e                         @ 080b660a 00da
    b select_equip_target_for_opponent_random @ 080b660c e8e2
LAB_080b660e:
    adds r0,r6,#0x0    @ 080b660e 301c
    adds r1,r4,#0x0    @ 080b6610 211c
    b enqueue_equip_slot_sprite_success      @ 080b6612 e1e2
LAB_080b6614:
    .hword 0x4641    @ 080b6614 4146
    lsls r0,r1,#0x1f    @ 080b6616 c807
    lsrs r5,r0,#0x1f    @ 080b6618 c50f
    movs r7,#0x1    @ 080b661a 0127
    rsbs r7,r7,#0    @ 080b661c 7f42
    str r7,[sp,#0x0]                         @ 080b661e 0097
    adds r0,r6,#0x0    @ 080b6620 301c
    adds r1,r5,#0x0    @ 080b6622 291c
    movs r2,#0x1    @ 080b6624 0122
    movs r3,#0x1    @ 080b6626 0123
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b6628 fef780fc
    adds r4,r0,#0x0    @ 080b662c 041c
    cmp r4,#0x0                              @ 080b662e 002c
    bge LAB_080b664c                         @ 080b6630 0cda
    movs r0,#0x1    @ 080b6632 0120
    subs r5,r0,r5    @ 080b6634 451b
    str r7,[sp,#0x0]                         @ 080b6636 0097
    adds r0,r6,#0x0    @ 080b6638 301c
    adds r1,r5,#0x0    @ 080b663a 291c
    adds r2,r7,#0x0    @ 080b663c 3a1c
    adds r3,r7,#0x0    @ 080b663e 3b1c
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b6640 fef774fc
    adds r4,r0,#0x0    @ 080b6644 041c
    cmp r4,#0x0                              @ 080b6646 002c
    bge LAB_080b664c                         @ 080b6648 00da
    b select_equip_target_for_opponent_random @ 080b664a c9e2
LAB_080b664c:
    adds r0,r6,#0x0    @ 080b664c 301c
    adds r1,r5,#0x0    @ 080b664e 291c
    b LAB_080b6bd6                           @ 080b6650 c1e2
LAB_080b6652:
    lsrs r1,r3,#0x1f    @ 080b6652 d90f
    movs r0,#0x1    @ 080b6654 0120
    rsbs r0,r0,#0    @ 080b6656 4042
    str r0,[sp,#0x0]                         @ 080b6658 0090
    adds r0,r6,#0x0    @ 080b665a 301c
    movs r2,#0x1    @ 080b665c 0122
    movs r3,#0x0    @ 080b665e 0023
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b6660 fef764fc
    adds r4,r0,#0x0    @ 080b6664 041c
    cmp r4,#0x0                              @ 080b6666 002c
    bge LAB_080b666c                         @ 080b6668 00da
    b select_equip_target_for_opponent_random @ 080b666a b9e2
LAB_080b666c:
    ldrb r3,[r6,#0x2]                        @ 080b666c b378
    lsls r1,r3,#0x1f    @ 080b666e d907
    b LAB_080b6bd2                           @ 080b6670 afe2
LAB_080b6672:
    lsrs r0,r3,#0x1f    @ 080b6672 d80f
    movs r2,#0x1    @ 080b6674 0122
    rsbs r2,r2,#0    @ 080b6676 5242
    .hword 0x4649    @ 080b6678 4946
    bl find_scored_slot_from_bitmap_with_field6_filter @ 080b667a fef7e1fb
    adds r4,r0,#0x0    @ 080b667e 041c
    cmp r4,#0x0                              @ 080b6680 002c
    bge LAB_080b6686                         @ 080b6682 00da
    b select_equip_target_for_opponent_random @ 080b6684 ace2
LAB_080b6686:
    ldrb r7,[r6,#0x2]                        @ 080b6686 b778
    lsls r1,r7,#0x1f    @ 080b6688 f907
    b LAB_080b6bd2                           @ 080b668a a2e2
LAB_080b668c:
    movs r0,#0x0    @ 080b668c 0020
    .hword 0x4682    @ 080b668e 8246
    .hword 0x4680    @ 080b6690 8046
    movs r5,#0x1    @ 080b6692 0125
    movs r7,#0x0    @ 080b6694 0027
LAB_080b6696:
    ldrb r1,[r6,#0x2]                        @ 080b6696 b178
    lsls r3,r1,#0x1f    @ 080b6698 cb07
    lsrs r1,r3,#0x1f    @ 080b669a d90f
    lsls r1,r1,#0x4    @ 080b669c 0901
    add r1,r8                                @ 080b669e 4144
    adds r0,r5,#0x0    @ 080b66a0 281c
    lsls r0,r1    @ 080b66a2 8840
    .hword 0x4649    @ 080b66a4 4946
    ands r0,r1    @ 080b66a6 0840
    cmp r0,#0x0                              @ 080b66a8 0028
    beq LAB_080b6710                         @ 080b66aa 31d0
    ldr r0, PTR_gP1LifePoints_080b6750       @ 080b66ac 2848
    .hword 0x4684    @ 080b66ae 8446
    lsrs r1,r3,#0x1f    @ 080b66b0 d90f
    adds r0,r5,#0x0    @ 080b66b2 281c
    ands r0,r1    @ 080b66b4 0840
    ldr r4, DAT_080b6754                     @ 080b66b6 274c
    muls r0,r4    @ 080b66b8 6043
    adds r0,r7,r0    @ 080b66ba 3818
    ldr r1, DAT_080b6758                     @ 080b66bc 2649
    adds r0,r0,r1    @ 080b66be 4018
    ldr r2,[r0,#0x0]                         @ 080b66c0 0268
    lsrs r2,r2,#0x16    @ 080b66c2 920d
    ands r2,r5    @ 080b66c4 2a40
    lsrs r1,r3,#0x1f    @ 080b66c6 d90f
    adds r0,r5,#0x0    @ 080b66c8 281c
    ands r0,r1    @ 080b66ca 0840
    muls r0,r4    @ 080b66cc 6043
    adds r0,r7,r0    @ 080b66ce 3818
    ldr r1, DAT_080b6758                     @ 080b66d0 2149
    adds r0,r0,r1    @ 080b66d2 4018
    ldr r0,[r0,#0x0]                         @ 080b66d4 0068
    lsrs r0,r0,#0x17    @ 080b66d6 c00d
    ands r0,r5    @ 080b66d8 2840
    cmn r2,r0                                @ 080b66da c242
    beq LAB_080b6710                         @ 080b66dc 18d0
    lsrs r1,r3,#0x1f    @ 080b66de d90f
    adds r0,r5,#0x0    @ 080b66e0 281c
    ands r0,r1    @ 080b66e2 0840
    muls r0,r4    @ 080b66e4 6043
    adds r0,r7,r0    @ 080b66e6 3818
    .hword 0x4661    @ 080b66e8 6146
    adds r1,#0x30    @ 080b66ea 3031
    adds r0,r0,r1    @ 080b66ec 4018
    ldr r0,[r0,#0x0]                         @ 080b66ee 0068
    lsls r0,r0,#0x13    @ 080b66f0 c004
    lsrs r0,r0,#0x13    @ 080b66f2 c00c
    bl check_card_has_equip_placement_type   @ 080b66f4 95f7b0f9
    cmp r0,#0x0                              @ 080b66f8 0028
    bne LAB_080b6710                         @ 080b66fa 09d1
    ldrb r3,[r6,#0x2]                        @ 080b66fc b378
    lsls r0,r3,#0x1f    @ 080b66fe d807
    lsrs r0,r0,#0x1f    @ 080b6700 c00f
    lsls r0,r0,#0x4    @ 080b6702 0001
    add r0,r8                                @ 080b6704 4044
    adds r1,r5,#0x0    @ 080b6706 291c
    lsls r1,r0    @ 080b6708 8140
    .hword 0x4650    @ 080b670a 5046
    orrs r0,r1    @ 080b670c 0843
    .hword 0x4682    @ 080b670e 8246
LAB_080b6710:
    adds r7,#0x14    @ 080b6710 1437
    movs r1,#0x1    @ 080b6712 0121
    add r8,r1                                @ 080b6714 8844
    .hword 0x4643    @ 080b6716 4346
    cmp r3,#0xa                              @ 080b6718 0a2b
    ble LAB_080b6696                         @ 080b671a bcdd
    ldrb r7,[r6,#0x2]                        @ 080b671c b778
    lsls r0,r7,#0x1f    @ 080b671e f807
    lsrs r0,r0,#0x1f    @ 080b6720 c00f
    .hword 0x4651    @ 080b6722 5146
    movs r2,#0x1    @ 080b6724 0122
    movs r3,#0x0    @ 080b6726 0023
    bl find_best_scored_slot_from_bitmap     @ 080b6728 fef7eefa
    adds r4,r0,#0x0    @ 080b672c 041c
    cmp r4,#0x0                              @ 080b672e 002c
    bge LAB_080b674a                         @ 080b6730 0bda
    ldrb r1,[r6,#0x2]                        @ 080b6732 b178
    lsls r0,r1,#0x1f    @ 080b6734 c807
    lsrs r0,r0,#0x1f    @ 080b6736 c00f
    .hword 0x4649    @ 080b6738 4946
    movs r2,#0x1    @ 080b673a 0122
    movs r3,#0x0    @ 080b673c 0023
    bl find_best_scored_slot_from_bitmap     @ 080b673e fef7e3fa
    adds r4,r0,#0x0    @ 080b6742 041c
    cmp r4,#0x0                              @ 080b6744 002c
    bge LAB_080b674a                         @ 080b6746 00da
    b select_equip_target_for_opponent_random @ 080b6748 4ae2
LAB_080b674a:
    ldrb r3,[r6,#0x2]                        @ 080b674a b378
    lsls r1,r3,#0x1f    @ 080b674c d907
    b LAB_080b6bd2                           @ 080b674e 40e2
PTR_gP1LifePoints_080b6750:
    .word  gP1LifePoints                  @ 080b6750 e0c40102
DAT_080b6754:
    .word  0x00000868                     @ 080b6754 68080000
DAT_080b6758:
    .word  0x0201c520                     @ 080b6758 20c50102

@ Equip target selection case fragment (best field7 score strategy). Inlined in FUN_080b5d98 (0x080b5d98) BST dispatch body; no independent push/pop frame. Uses parent frame registers: r6=equip_card_zone_ptr, r7=work_score (initialized to -1), r8=equip_zone_bitmap. Iterates slots [0..4]: for each bitmap-set slot checks equip_zone bit offset (player_bit determines range); if set, calls get_slot_field7_score(player, slot) and updates best score into r7. After loop if best score < 0 -> jumps to FUN_080b6be0 (failure exit). Otherwise determines target player and best_slot, tail-jumps to FUN_080b6bd8 (success: calls FUN_08080c9c + returns 1). Side effects: via FUN_080b6bd8 -> FUN_08080c9c writes equip target reference.
@ 
@ Constants:
@ - SLOT_LOOP_MAX=4 (cmp r4,#0x4)
@ - score_init=-1 (rsbs r3,r3,#0 from movs r3,#1)
exec_equip_target_by_best_field7_score:
    movs r3,#0x1    @ 080b675c 0123
    rsbs r3,r3,#0    @ 080b675e 5b42
    adds r7,r3,#0x0    @ 080b6760 1f1c
    movs r4,#0x0    @ 080b6762 0024
    movs r5,#0x1    @ 080b6764 0125
LAB_080b6766:
    ldrb r0,[r6,#0x2]                        @ 080b6766 b078
    lsls r2,r0,#0x1f    @ 080b6768 c207
    lsrs r0,r2,#0x1f    @ 080b676a d00f
    subs r0,r5,r0    @ 080b676c 281a
    lsls r0,r0,#0x4    @ 080b676e 0001
    adds r0,r0,r4    @ 080b6770 0019
    adds r1,r5,#0x0    @ 080b6772 291c
    lsls r1,r0    @ 080b6774 8140
    .hword 0x4648    @ 080b6776 4846
    ands r1,r0    @ 080b6778 0140
    cmp r1,#0x0                              @ 080b677a 0029
    beq LAB_080b6794                         @ 080b677c 0ad0
    lsrs r0,r2,#0x1f    @ 080b677e d00f
    subs r0,r5,r0    @ 080b6780 281a
    adds r1,r4,#0x0    @ 080b6782 211c
    str r3,[sp,#0x28]                        @ 080b6784 0a93
    bl get_slot_field7_score                 @ 080b6786 84f7f1f8
    ldr r3,[sp,#0x28]                        @ 080b678a 0a9b
    cmp r0,r7                                @ 080b678c b842
    ble LAB_080b6794                         @ 080b678e 01dd
    adds r7,r0,#0x0    @ 080b6790 071c
    adds r3,r4,#0x0    @ 080b6792 231c
LAB_080b6794:
    adds r4,#0x1    @ 080b6794 0134
    cmp r4,#0x4                              @ 080b6796 042c
    ble LAB_080b6766                         @ 080b6798 e5dd
    cmp r3,#0x0                              @ 080b679a 002b
    bge LAB_080b67a0                         @ 080b679c 00da
    b select_equip_target_for_opponent_random @ 080b679e 1fe2
LAB_080b67a0:
    ldrb r1,[r6,#0x2]                        @ 080b67a0 b178
    lsls r0,r1,#0x1f    @ 080b67a2 c807
    lsrs r0,r0,#0x1f    @ 080b67a4 c00f
    movs r1,#0x1    @ 080b67a6 0121
    subs r1,r1,r0    @ 080b67a8 091a
    adds r0,r6,#0x0    @ 080b67aa 301c
    adds r2,r3,#0x0    @ 080b67ac 1a1c
    b enqueue_equip_slot_sprite_success      @ 080b67ae 13e2

@ Equip target selection case fragment (active side bitmap test strategy). Inlined in FUN_080b5d98 (0x080b5d98) dispatch body. No independent frame; uses parent frame r6=equip_card_zone_ptr, r3=card_id_or_flag, r7=working_flag. Reads gDuelState (DAT_080b67c4=0x0201bb90); r3 bit31 selects opponent player (field0) vs self (field1c) attack_bitmap. Extracts r7 bit31 = slot_sub_index as column; computes bit_pos = column*16 + slot. Checks attack_bitmap at that bit: if set -> determines player_id and column then tail-jumps to FUN_080b6bd4 (success path); else -> tail-jumps to LAB_080b6bf2 (failure path -> calls FUN_080b5ad4 + epilogue). Side effects: via success path, writes equip target.
@ 
@ Constants:
@ - gDuelState=0x0201bb90 (DAT_080b67c4)
@ - column_stride=16 (lsls r1,#0x4)
exec_equip_target_by_active_side_bitmap:
    ldr r2, DAT_080b67c4                     @ 080b67b0 044a
    .hword 0x4643    @ 080b67b2 4346
    lsls r0,r3,#0x1f    @ 080b67b4 d807
    lsrs r0,r0,#0x1f    @ 080b67b6 c00f
    ldr r1,[r2,#0x0]                         @ 080b67b8 1168
    cmp r1,r0                                @ 080b67ba 8142
    bne LAB_080b67c8                         @ 080b67bc 04d1
    ldr r4,[r2,#0x1c]                        @ 080b67be d469
    b LAB_080b67ca                           @ 080b67c0 03e0
    .zero  0x2
DAT_080b67c4:
    .word  0x0201bb90                     @ 080b67c4 90bb0102
LAB_080b67c8:
    ldr r4,[r2,#0x20]                        @ 080b67c8 146a
LAB_080b67ca:
    .hword 0x4647    @ 080b67ca 4746
    lsls r2,r7,#0x1f    @ 080b67cc fa07
    lsrs r1,r2,#0x1f    @ 080b67ce d10f
    lsls r1,r1,#0x4    @ 080b67d0 0901
    adds r1,r1,r4    @ 080b67d2 0919
    movs r0,#0x1    @ 080b67d4 0120
    lsls r0,r1    @ 080b67d6 8840
    .hword 0x4649    @ 080b67d8 4946
    ands r0,r1    @ 080b67da 0840
    cmp r0,#0x0                              @ 080b67dc 0028
    beq LAB_080b67e4                         @ 080b67de 01d0
    lsrs r1,r2,#0x1f    @ 080b67e0 d10f
    b LAB_080b6bd4                           @ 080b67e2 f7e1
LAB_080b67e4:
    lsrs r1,r2,#0x1f    @ 080b67e4 d10f
    b LAB_080b6bf2                           @ 080b67e6 04e2

@ Equip target selection case fragment (field5 score scan strategy). Inlined in FUN_080b5d98 (0x080b5d98). No independent frame; parent frame r6=equip_card_zone_ptr, r10=gDuelFieldSlots offset base. Iterates monster slots [0..4]: for each slot reads active bit (bits[31:19]) checking if card present; if active and slot[+6]==0, calls get_slot_field5_score(player, slot) and tracks best score into r7. If after scan r7==0 (no valid slot) -> calls find_best_scored_slot_for_player_with_gate fallback. Finally clears slot[+6] low 5 bits (mask ~0x1d), then iterates bitmap [0..4] updating target; success tail-jumps to FUN_080b6bd4; failure tail-jumps to FUN_080b6be0. Side effects: strb -> slot[+6] (clears low 5 equip-gate flag bits).
@ 
@ Constants:
@ - gDuelFieldSlots=0x0201c510 (DAT_080b683c)
@ - player_stride=0x868 (DAT_080b6840)
@ - slot_entry_size=0x14 (adds r5,#0x14 in loop)
@ - SLOT_COUNT=5 (loop r4=0..4)
@ - SLOT_FIELD6_CLEAR_MASK=~0x1d=0xe2
exec_equip_target_by_field5_score_scan:
    movs r7,#0x0    @ 080b67e8 0027
    movs r4,#0x0    @ 080b67ea 0024
    ldr r3, DAT_080b683c                     @ 080b67ec 134b
    .hword 0x469a    @ 080b67ee 9a46
    movs r5,#0x0    @ 080b67f0 0025
LAB_080b67f2:
    .hword 0x4640    @ 080b67f2 4046
    lsls r2,r0,#0x1f    @ 080b67f4 c207
    lsrs r1,r2,#0x1f    @ 080b67f6 d10f
    movs r0,#0x1    @ 080b67f8 0120
    ands r0,r1    @ 080b67fa 0840
    ldr r1, DAT_080b6840                     @ 080b67fc 1049
    muls r0,r1    @ 080b67fe 4843
    adds r0,r5,r0    @ 080b6800 2818
    add r0,r10                               @ 080b6802 5044
    ldr r0,[r0,#0x0]                         @ 080b6804 0068
    lsls r0,r0,#0x13    @ 080b6806 c004
    cmp r0,#0x0                              @ 080b6808 0028
    beq LAB_080b684c                         @ 080b680a 1fd0
    lsrs r1,r2,#0x1f    @ 080b680c d10f
    movs r0,#0x1    @ 080b680e 0120
    ands r0,r1    @ 080b6810 0840
    ldr r3, DAT_080b6840                     @ 080b6812 0b4b
    muls r0,r3    @ 080b6814 5843
    adds r0,r5,r0    @ 080b6816 2818
    add r0,r10                               @ 080b6818 5044
    ldrh r0,[r0,#0x6]                        @ 080b681a c088
    cmp r0,#0x0                              @ 080b681c 0028
    bne LAB_080b684c                         @ 080b681e 15d1
    adds r0,r1,#0x0    @ 080b6820 081c
    adds r1,r4,#0x0    @ 080b6822 211c
    bl get_slot_field5_score                 @ 080b6824 84f798f8
    cmp r7,r0                                @ 080b6828 8742
    bgt LAB_080b6844                         @ 080b682a 0bdc
    ldrb r7,[r6,#0x2]                        @ 080b682c b778
    lsls r0,r7,#0x1f    @ 080b682e f807
    lsrs r0,r0,#0x1f    @ 080b6830 c00f
    adds r1,r4,#0x0    @ 080b6832 211c
    bl get_slot_field5_score                 @ 080b6834 84f790f8
    b LAB_080b6846                           @ 080b6838 05e0
    .zero  0x2
DAT_080b683c:
    .word  0x0201c510                     @ 080b683c 10c50102
DAT_080b6840:
    .word  0x00000868                     @ 080b6840 68080000
LAB_080b6844:
    adds r0,r7,#0x0    @ 080b6844 381c
LAB_080b6846:
    adds r7,r0,#0x0    @ 080b6846 071c
    ldrb r0,[r6,#0x2]                        @ 080b6848 b078
    .hword 0x4680    @ 080b684a 8046
LAB_080b684c:
    adds r5,#0x14    @ 080b684c 1435
    adds r4,#0x1    @ 080b684e 0134
    cmp r4,#0x4                              @ 080b6850 042c
    ble LAB_080b67f2                         @ 080b6852 cedd
    cmp r7,#0x0                              @ 080b6854 002f
    bne LAB_080b686e                         @ 080b6856 0ad1
    ldrb r3,[r6,#0x2]                        @ 080b6858 b378
    lsls r1,r3,#0x1f    @ 080b685a d907
    lsrs r0,r1,#0x1f    @ 080b685c c80f
    adds r1,r0,#0x0    @ 080b685e 011c
    movs r2,#0x1    @ 080b6860 0122
    rsbs r2,r2,#0    @ 080b6862 5242
    str r7,[sp,#0x0]                         @ 080b6864 0097
    movs r3,#0x1    @ 080b6866 0123
    bl find_best_scored_slot_for_player_with_gate @ 080b6868 f8f758fb
    adds r7,r0,#0x0    @ 080b686c 071c
LAB_080b686e:
    movs r0,#0x1d    @ 080b686e 1d20
    rsbs r0,r0,#0    @ 080b6870 4042
    ldrb r1,[r6,#0x6]                        @ 080b6872 b179
    ands r0,r1    @ 080b6874 0840
    strb r0,[r6,#0x6]                        @ 080b6876 b071
    movs r4,#0x0    @ 080b6878 0024
    movs r5,#0x1    @ 080b687a 0125
    movs r3,#0x0    @ 080b687c 0023
LAB_080b687e:
    ldrb r0,[r6,#0x2]                        @ 080b687e b078
    lsls r2,r0,#0x1f    @ 080b6880 c207
    lsrs r0,r2,#0x1f    @ 080b6882 d00f
    subs r0,r5,r0    @ 080b6884 281a
    lsls r0,r0,#0x4    @ 080b6886 0001
    adds r0,r0,r4    @ 080b6888 0019
    adds r1,r5,#0x0    @ 080b688a 291c
    lsls r1,r0    @ 080b688c 8140
    .hword 0x4648    @ 080b688e 4846
    ands r1,r0    @ 080b6890 0140
    cmp r1,#0x0                              @ 080b6892 0029
    beq LAB_080b68ea                         @ 080b6894 29d0
    lsrs r0,r2,#0x1f    @ 080b6896 d00f
    subs r0,r5,r0    @ 080b6898 281a
    adds r1,r4,#0x0    @ 080b689a 211c
    add r2,sp,#0x4                           @ 080b689c 01aa
    str r3,[sp,#0x28]                        @ 080b689e 0a93
    bl dispatch_zone_slot_score_by_player_flag @ 080b68a0 f5f7b0fb
    ldrb r1,[r6,#0x2]                        @ 080b68a4 b178
    lsls r2,r1,#0x1f    @ 080b68a6 ca07
    lsrs r0,r2,#0x1f    @ 080b68a8 d00f
    subs r0,r5,r0    @ 080b68aa 281a
    ands r0,r5    @ 080b68ac 2840
    ldr r1, DAT_080b68d4                     @ 080b68ae 0949
    muls r0,r1    @ 080b68b0 4843
    ldr r3,[sp,#0x28]                        @ 080b68b2 0a9b
    adds r0,r3,r0    @ 080b68b4 1818
    ldr r1, DAT_080b68d8                     @ 080b68b6 0849
    adds r0,r0,r1    @ 080b68b8 4018
    ldrh r0,[r0,#0x6]                        @ 080b68ba c088
    cmp r0,#0x0                              @ 080b68bc 0028
    bne LAB_080b68dc                         @ 080b68be 0dd1
    ldr r0,[sp,#0x18]                        @ 080b68c0 0698
    cmp r0,r7                                @ 080b68c2 b842
    blt LAB_080b68ea                         @ 080b68c4 11db
    ldr r0,[sp,#0x1c]                        @ 080b68c6 0798
    cmp r0,r7                                @ 080b68c8 b842
    bge LAB_080b68ea                         @ 080b68ca 0eda
    lsrs r1,r2,#0x1f    @ 080b68cc d10f
    subs r1,r5,r1    @ 080b68ce 691a
    b LAB_080b6bd4                           @ 080b68d0 80e1
    .zero  0x2
DAT_080b68d4:
    .word  0x00000868                     @ 080b68d4 68080000
DAT_080b68d8:
    .word  0x0201c510                     @ 080b68d8 10c50102
LAB_080b68dc:
    ldr r0,[sp,#0x1c]                        @ 080b68dc 0798
    cmp r0,r7                                @ 080b68de b842
    blt LAB_080b68ea                         @ 080b68e0 03db
    ldr r0,[sp,#0x18]                        @ 080b68e2 0698
    cmp r0,r7                                @ 080b68e4 b842
    bge LAB_080b68ea                         @ 080b68e6 00da
    b LAB_080b6bbc                           @ 080b68e8 68e1
LAB_080b68ea:
    adds r3,#0x14    @ 080b68ea 1433
    adds r4,#0x1    @ 080b68ec 0134
    cmp r4,#0x4                              @ 080b68ee 042c
    ble LAB_080b687e                         @ 080b68f0 c5dd
    b select_equip_target_for_opponent_random @ 080b68f2 75e1

@ Equip target selection case fragment (simple side jump). Inlined in FUN_080b5d98 (0x080b5d98). Minimal fragment: mov r3,r8 (r3=r8, bitmap/flag); extracts r3 bit31 = player_side; tail-jumps to LAB_080b6bf2 (calls FUN_080b5ad4(equip_slot, computed_player) + epilogue). This case does not call any select_equip function; directly passes current equip slot to default handler FUN_080b5ad4 for target initialization, using r3=r8 bit31 to determine opposing player_id. Side effects: via FUN_080b5ad4, writes target reference.
@ 
@ Constants:
@ - (none; 3-instruction fragment)
exec_equip_target_fallback_to_field_side:
    .hword 0x4643    @ 080b68f4 4346
    lsls r1,r3,#0x1f    @ 080b68f6 d907
    lsrs r1,r1,#0x1f    @ 080b68f8 c90f
    b LAB_080b6bf2                           @ 080b68fa 7ae1

@ Inline exit fragment within FUN_080b5d98 equip target dispatch hub: opponent-first selection strategy.
@ Jumped to from multiple card_id dispatch branches in the hub.
@ Parent frame registers: r6=player_id, r8=equip_zone_ptr ([+2] bit0=player_side).
@ Extracts equip zone player from r8 bit0; computes opponent = 1 - player.
@ Sets r5=-1 (rsbs, gate_param), stores as 5th stack arg.
@ Calls find_best_slot_from_equip_bitmap_with_gate(r6, opponent, mode=1, gate=-1).
@ If slot found (result >= 0) -> b FUN_080b6bd8 (commit equip target).
@ If not found: flips to self side, retries find_best_slot_from_equip_bitmap_with_gate.
@ Both fail -> b FUN_080b6be0 (fail exit).
@ Opponent-first strategy biases equip effect toward negative impact on opponent.
@ 
@ Constants:
@ - gate_param=-1 (rsbs r5,#0)
@ - mode=1 (movs r5,#1)
exec_equip_target_select_opponent_first:
    .hword 0x4647    @ 080b68fc 4746
    lsls r0,r7,#0x1f    @ 080b68fe f807
    lsrs r0,r0,#0x1f    @ 080b6900 c00f
    movs r7,#0x1    @ 080b6902 0127
    subs r4,r7,r0    @ 080b6904 3c1a
    movs r5,#0x1    @ 080b6906 0125
    rsbs r5,r5,#0    @ 080b6908 6d42
    str r5,[sp,#0x0]                         @ 080b690a 0095
    adds r0,r6,#0x0    @ 080b690c 301c
    adds r1,r4,#0x0    @ 080b690e 211c
    movs r2,#0x1    @ 080b6910 0122
    movs r3,#0x0    @ 080b6912 0023
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b6914 fef70afb
    adds r2,r0,#0x0    @ 080b6918 021c
    cmp r2,#0x0                              @ 080b691a 002a
    bge LAB_080b6936                         @ 080b691c 0bda
    subs r4,r7,r4    @ 080b691e 3c1b
    str r5,[sp,#0x0]                         @ 080b6920 0095
    adds r0,r6,#0x0    @ 080b6922 301c
    adds r1,r4,#0x0    @ 080b6924 211c
    movs r2,#0x1    @ 080b6926 0122
    movs r3,#0x0    @ 080b6928 0023
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b692a fef7fffa
    adds r2,r0,#0x0    @ 080b692e 021c
    cmp r2,#0x0                              @ 080b6930 002a
    bge LAB_080b6936                         @ 080b6932 00da
    b select_equip_target_for_opponent_random @ 080b6934 54e1
LAB_080b6936:
    adds r0,r6,#0x0    @ 080b6936 301c
    adds r1,r4,#0x0    @ 080b6938 211c
    b enqueue_equip_slot_sprite_success      @ 080b693a 4de1

@ Inline exit fragment within FUN_080b5d98 equip target dispatch hub: direction-bit-driven target selection.
@ Jumped to from a specific card_id branch at 0x080b5fe6 in the hub.
@ Parent frame: r6=player_id, r3=direction_source (bit31 = sign bit), r8=equip_zone_bitmap.
@ Extracts r3 bit31 via lsrs #0x1f as direction; computes r1 = 1 - direction (flipped side).
@ Sets r2=-1 (rsbs, gate_param), stores as 5th stack arg.
@ Calls find_best_slot_from_equip_bitmap_with_gate(r6, r1, mode=1, gate=1).
@ If slot found (r4 >= 0): extracts self player from r6[+2] bit0, opponent = 1-self;
@ then b LAB_080b6bd4 (success + target commit).
@ If not found: b FUN_080b6be0 (fail exit).
@ Unlike exec_equip_target_select_opponent_first (0x080b68fc), no fallback retry.
@ 
@ Constants:
@ - gate_param=-1 (rsbs r2,#0)
@ - mode=1 (movs r3,#1)
@ - direction = r3_parent >> 31 (sign bit)
exec_equip_target_select_by_direction_bit:
    lsrs r1,r3,#0x1f    @ 080b693c d90f
    movs r5,#0x1    @ 080b693e 0125
    subs r1,r5,r1    @ 080b6940 691a
    movs r2,#0x1    @ 080b6942 0122
    rsbs r2,r2,#0    @ 080b6944 5242
    str r2,[sp,#0x0]                         @ 080b6946 0092
    adds r0,r6,#0x0    @ 080b6948 301c
    movs r3,#0x1    @ 080b694a 0123
    bl find_best_slot_from_equip_bitmap_with_gate @ 080b694c fef7eefa
    adds r4,r0,#0x0    @ 080b6950 041c
    cmp r4,#0x0                              @ 080b6952 002c
    bge LAB_080b6958                         @ 080b6954 00da
    b select_equip_target_for_opponent_random @ 080b6956 43e1
LAB_080b6958:
    ldrb r0,[r6,#0x2]                        @ 080b6958 b078
    lsls r1,r0,#0x1f    @ 080b695a c107
    lsrs r1,r1,#0x1f    @ 080b695c c90f
    subs r1,r5,r1    @ 080b695e 691a
    b LAB_080b6bd4                           @ 080b6960 38e1

@ Equip target selection case fragment (effect chain entry match strategy). Inlined in FUN_080b5d98 (0x080b5d98). Parent frame r5=effect_chain_entry_ptr (may be 0). If r5==0 -> fails to FUN_080b6be0. Otherwise: reads r2 (from parent, equip zone bit0), takes [r5+0x2] bit0 = chain_player_bit, compares both player_id bit0: if same -> fails. Checks [r5+0x4] bits[18:16] (lsls #0xe/lsrs #0x1d) whether > 0 (link_count); if <=0 -> fails. If valid: iterates links [0..link_count-1], for each reads effect slot side+type via read_effect_slot_side_and_type; if side matches player_id AND type<=4 AND bitmap bit (side<<4|type) is set -> tail-jumps to LAB_080b6bc2 (success). Loop ends without hit -> fails. Side effects: via success path, writes target.
@ 
@ Constants:
@ - EFFECT_TYPE_MAX=4 (cmp r2,#0x4)
@ - link_count_field=[r5+0x4] bits[18:16]
exec_equip_target_by_effect_chain_match:
    cmp r5,#0x0                              @ 080b6962 002d
    bne LAB_080b6968                         @ 080b6964 00d1
    b select_equip_target_for_opponent_random @ 080b6966 3be1
LAB_080b6968:
    movs r0,#0x1    @ 080b6968 0120
    adds r1,r0,#0x0    @ 080b696a 011c
    ldrb r3,[r5,#0x2]                        @ 080b696c ab78
    ands r1,r3    @ 080b696e 1940
    ands r0,r2    @ 080b6970 1040
    cmp r1,r0                                @ 080b6972 8142
    bne LAB_080b6978                         @ 080b6974 00d1
    b select_equip_target_for_opponent_random @ 080b6976 33e1
LAB_080b6978:
    movs r4,#0x0    @ 080b6978 0024
    ldr r0,[r5,#0x4]                         @ 080b697a 6868
    lsls r0,r0,#0xe    @ 080b697c 8003
    lsrs r0,r0,#0x1d    @ 080b697e 400f
    cmp r4,r0                                @ 080b6980 8442
    blt LAB_080b6986                         @ 080b6982 00db
    b select_equip_target_for_opponent_random @ 080b6984 2ce1
LAB_080b6986:
    adds r0,r5,#0x0    @ 080b6986 281c
    adds r1,r4,#0x0    @ 080b6988 211c
    bl read_effect_slot_side_and_type        @ 080b698a caf7eff9
    lsls r1,r0,#0x18    @ 080b698e 0106
    lsrs r3,r1,#0x18    @ 080b6990 0b0e
    lsls r0,r0,#0x10    @ 080b6992 0004
    lsrs r2,r0,#0x18    @ 080b6994 020e
    ldrb r7,[r6,#0x2]                        @ 080b6996 b778
    lsls r0,r7,#0x1f    @ 080b6998 f807
    lsrs r0,r0,#0x1f    @ 080b699a c00f
    cmp r3,r0                                @ 080b699c 8342
    bne LAB_080b69b6                         @ 080b699e 0ad1
    cmp r2,#0x4                              @ 080b69a0 042a
    bgt LAB_080b69b6                         @ 080b69a2 08dc
    lsls r1,r3,#0x4    @ 080b69a4 1901
    adds r1,r1,r2    @ 080b69a6 8918
    movs r0,#0x1    @ 080b69a8 0120
    lsls r0,r1    @ 080b69aa 8840
    .hword 0x4649    @ 080b69ac 4946
    ands r0,r1    @ 080b69ae 0840
    cmp r0,#0x0                              @ 080b69b0 0028
    beq LAB_080b69b6                         @ 080b69b2 00d0
    b LAB_080b6bc2                           @ 080b69b4 05e1
LAB_080b69b6:
    adds r4,#0x1    @ 080b69b6 0134
    ldr r0,[r5,#0x4]                         @ 080b69b8 6868
    lsls r0,r0,#0xe    @ 080b69ba 8003
    lsrs r0,r0,#0x1d    @ 080b69bc 400f
    cmp r4,r0                                @ 080b69be 8442
    blt LAB_080b6986                         @ 080b69c0 e1db
    b select_equip_target_for_opponent_random @ 080b69c2 0de1
LAB_080b69c4:
    lsrs r0,r3,#0x1f    @ 080b69c4 d80f
    ldr r2, DAT_080b69dc                     @ 080b69c6 054a
    .hword 0x4649    @ 080b69c8 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b69ca fef7cdfa
    adds r4,r0,#0x0    @ 080b69ce 041c
    cmp r4,#0x0                              @ 080b69d0 002c
    bge LAB_080b69d6                         @ 080b69d2 00da
    b select_equip_target_for_opponent_random @ 080b69d4 04e1
LAB_080b69d6:
    ldrb r3,[r6,#0x2]                        @ 080b69d6 b378
    lsls r1,r3,#0x1f    @ 080b69d8 d907
    b LAB_080b6bd2                           @ 080b69da fae0
DAT_080b69dc:
    .word  0x080b5bed                     @ 080b69dc ed5b0b08
LAB_080b69e0:
    movs r4,#0x0    @ 080b69e0 0024
    movs r7,#0x1    @ 080b69e2 0127
    movs r5,#0x0    @ 080b69e4 0025
LAB_080b69e6:
    ldrb r0,[r6,#0x2]                        @ 080b69e6 b078
    lsls r3,r0,#0x1f    @ 080b69e8 c307
    lsrs r1,r3,#0x1f    @ 080b69ea d90f
    lsls r1,r1,#0x4    @ 080b69ec 0901
    adds r1,r1,r4    @ 080b69ee 0919
    adds r0,r7,#0x0    @ 080b69f0 381c
    lsls r0,r1    @ 080b69f2 8840
    .hword 0x4649    @ 080b69f4 4946
    ands r0,r1    @ 080b69f6 0840
    cmp r0,#0x0                              @ 080b69f8 0028
    beq LAB_080b6a20                         @ 080b69fa 11d0
    lsrs r0,r3,#0x1f    @ 080b69fc d80f
    ldrh r1,[r6,#0x0]                        @ 080b69fe 3188
    adds r3,r0,#0x0    @ 080b6a00 031c
    adds r2,r7,#0x0    @ 080b6a02 3a1c
    ands r2,r3    @ 080b6a04 1a40
    ldr r3, DAT_080b6a2c                     @ 080b6a06 094b
    muls r2,r3    @ 080b6a08 5a43
    adds r2,r5,r2    @ 080b6a0a aa18
    ldr r3, DAT_080b6a30                     @ 080b6a0c 084b
    adds r2,r2,r3    @ 080b6a0e d218
    ldr r2,[r2,#0x0]                         @ 080b6a10 1268
    lsls r2,r2,#0x13    @ 080b6a12 d204
    lsrs r2,r2,#0x13    @ 080b6a14 d20c
    bl dispatch_effect_handler_by_card_id    @ 080b6a16 d7f74bf8
    cmp r0,#0x0                              @ 080b6a1a 0028
    beq LAB_080b6a20                         @ 080b6a1c 00d0
    b LAB_080b6bc8                           @ 080b6a1e d3e0
LAB_080b6a20:
    adds r5,#0x14    @ 080b6a20 1435
    adds r4,#0x1    @ 080b6a22 0134
    cmp r4,#0x4                              @ 080b6a24 042c
    ble LAB_080b69e6                         @ 080b6a26 dedd
    b select_equip_target_for_opponent_random @ 080b6a28 dae0
    .zero  0x2
DAT_080b6a2c:
    .word  0x00000868                     @ 080b6a2c 68080000
DAT_080b6a30:
    .word  0x0201c510                     @ 080b6a30 10c50102

@ Equip target selection case fragment (field6 score + effect activation check). Inlined in FUN_080b5d98 (0x080b5d98). Parent frame r7=bitmap, r10=gDuelFieldSlots + player_offset. Initial r4=0 (slot_idx), r5 = 0x0cc<<1 + r10 = offset 0x198 in slot table. Iterates slots [0..4]: checks r7 (bitmap, mov r7,r9) bit (player_bit*16+slot) whether set; if set and [r5,#0]=link_count>1: calls get_slot_field6_score(player, slot); if score nonzero -> success tail-jump to LAB_080b6bce. No hit -> failure tail-jump to FUN_080b6be0. Side effects: via success path, writes target.
@ 
@ Constants:
@ - slot_bitmap_offset=0x198 (0xcc<<1=0x198 in gDuelFieldSlots area)
@ - LINK_COUNT_MIN=2 (cmp r0,#0x1; bls -> skip if <=1)
@ - SLOT_COUNT=5 (loop r4=0..4)
exec_equip_target_by_field6_score_and_effect:
    movs r4,#0x0    @ 080b6a34 0024
    movs r5,#0xcc    @ 080b6a36 cc25
    lsls r5,r5,#0x1    @ 080b6a38 6d00
    add r5,r10                               @ 080b6a3a 5544
LAB_080b6a3c:
    ldrb r3,[r6,#0x2]                        @ 080b6a3c b378
    lsls r2,r3,#0x1f    @ 080b6a3e da07
    lsrs r1,r2,#0x1f    @ 080b6a40 d10f
    lsls r1,r1,#0x4    @ 080b6a42 0901
    adds r1,r1,r4    @ 080b6a44 0919
    movs r0,#0x1    @ 080b6a46 0120
    lsls r0,r1    @ 080b6a48 8840
    .hword 0x464f    @ 080b6a4a 4f46
    ands r0,r7    @ 080b6a4c 3840
    cmp r0,#0x0                              @ 080b6a4e 0028
    beq LAB_080b6a66                         @ 080b6a50 09d0
    ldr r0,[r5,#0x0]                         @ 080b6a52 2868
    cmp r0,#0x1                              @ 080b6a54 0128
    bls LAB_080b6a66                         @ 080b6a56 06d9
    lsrs r0,r2,#0x1f    @ 080b6a58 d00f
    adds r1,r4,#0x0    @ 080b6a5a 211c
    bl get_slot_field6_score                 @ 080b6a5c 83f790ff
    cmp r0,#0x0                              @ 080b6a60 0028
    beq LAB_080b6a66                         @ 080b6a62 00d0
    b LAB_080b6bce                           @ 080b6a64 b3e0
LAB_080b6a66:
    adds r5,#0x4    @ 080b6a66 0435
    adds r4,#0x1    @ 080b6a68 0134
    cmp r4,#0x4                              @ 080b6a6a 042c
    ble LAB_080b6a3c                         @ 080b6a6c e6dd
    b select_equip_target_for_opponent_random @ 080b6a6e b7e0

@ Equip target selection case fragment (effect chain type mask match). Inlined in FUN_080b5d98 (0x080b5d98). Parent frame r5=effect_chain_entry_ptr, r6=equip_card_zone_ptr. If r5==0 -> jumps to failure path LAB_080b6aba. Checks [r5+0x4] bits[22:20] (lsls #0xa -> 0xe0, lsrs #0x8 -> 0x80 mask for 0x80000) -> whether equals 0x8000 (specific effect type flag); no match -> fails. Calls read_effect_slot_side_and_type(r5, 0) twice: first takes type byte (bits[23:16]), checks <=0xa; second takes side (bits[31:24]) and type, builds bit_key=(side<<4)|type, checks bitmap (r9) at that bit: if set -> success, tail-jumps to FUN_080b6bd8. Side effects: via success path, writes target.
@ 
@ Constants:
@ - CHAIN_MASK=0x38000 (0xe0<<0xa; applied to [r5+4])
@ - CHAIN_FLAG=0x8000 (0x80<<0x8; target value after mask: bits[17:15]==0b001)
@ - type_max=0xa (cmp r0,#0xa; bhi -> skip)
exec_equip_target_by_chain_effect_type_mask:
    cmp r5,#0x0                              @ 080b6a70 002d
    beq LAB_080b6aba                         @ 080b6a72 22d0
    ldr r0,[r5,#0x4]                         @ 080b6a74 6868
    movs r1,#0xe0    @ 080b6a76 e021
    lsls r1,r1,#0xa    @ 080b6a78 8902
    ands r0,r1    @ 080b6a7a 0840
    movs r1,#0x80    @ 080b6a7c 8021
    lsls r1,r1,#0x8    @ 080b6a7e 0902
    cmp r0,r1                                @ 080b6a80 8842
    bne LAB_080b6aba                         @ 080b6a82 1ad1
    adds r0,r5,#0x0    @ 080b6a84 281c
    movs r1,#0x0    @ 080b6a86 0021
    bl read_effect_slot_side_and_type        @ 080b6a88 caf770f9
    lsls r0,r0,#0x10    @ 080b6a8c 0004
    lsrs r0,r0,#0x18    @ 080b6a8e 000e
    cmp r0,#0xa                              @ 080b6a90 0a28
    bhi LAB_080b6aba                         @ 080b6a92 12d8
    adds r0,r5,#0x0    @ 080b6a94 281c
    movs r1,#0x0    @ 080b6a96 0021
    bl read_effect_slot_side_and_type        @ 080b6a98 caf768f9
    lsls r1,r0,#0x18    @ 080b6a9c 0106
    lsrs r3,r1,#0x18    @ 080b6a9e 0b0e
    lsls r0,r0,#0x10    @ 080b6aa0 0004
    lsrs r2,r0,#0x18    @ 080b6aa2 020e
    lsls r1,r3,#0x4    @ 080b6aa4 1901
    adds r1,r1,r2    @ 080b6aa6 8918
    movs r0,#0x1    @ 080b6aa8 0120
    lsls r0,r1    @ 080b6aaa 8840
    .hword 0x4649    @ 080b6aac 4946
    ands r0,r1    @ 080b6aae 0840
    cmp r0,#0x0                              @ 080b6ab0 0028
    beq LAB_080b6aba                         @ 080b6ab2 02d0
    adds r0,r6,#0x0    @ 080b6ab4 301c
    adds r1,r3,#0x0    @ 080b6ab6 191c
    b enqueue_equip_slot_sprite_success      @ 080b6ab8 8ee0
LAB_080b6aba:
    ldrb r3,[r6,#0x2]                        @ 080b6aba b378
    lsls r1,r3,#0x1f    @ 080b6abc d907
    lsrs r1,r1,#0x1f    @ 080b6abe c90f
    b LAB_080b6bf2                           @ 080b6ac0 97e0

@ Equip target selection case fragment (effect chain type mask + zone type check). Inlined in FUN_080b5d98 (0x080b5d98). Highly symmetric with exec_equip_target_by_chain_effect_type_mask (080b6a70): checks r5=effect_chain_entry_ptr; same [r5+4] bits[22:20] check; same read_effect_slot_side_and_type calls; but uses r7 bitmap (mov r7,r9) instead of r9 directly. After bitmap check fails, enters additional zone_type check path (ldrh[r6+2] bits[12:2], cmp 0x480/0x4c0): if zone_type is 0x480 or 0x4c0 -> also checks gDuelState bitmap (DAT_080b6b4c=0x0201bb90) against player_id; on match at some branches -> jumps to FUN_080b6b50 (comparator fallback); final success -> jumps to FUN_080b6bd8. Side effects: via success path, writes target.
@ 
@ Constants:
@ - gDuelState=0x0201bb90 (DAT_080b6b4c)
@ - ZONE_TYPE_EQUIP_A=0x480 (0x90<<0x3=0x480)
@ - ZONE_TYPE_EQUIP_B=0x4c0 (0x480+0x40)
@ - type_max=0xa
exec_equip_target_by_chain_effect_with_field_check:
    cmp r5,#0x0                              @ 080b6ac2 002d
    beq LAB_080b6b0c                         @ 080b6ac4 22d0
    ldr r0,[r5,#0x4]                         @ 080b6ac6 6868
    movs r1,#0xe0    @ 080b6ac8 e021
    lsls r1,r1,#0xa    @ 080b6aca 8902
    ands r0,r1    @ 080b6acc 0840
    movs r1,#0x80    @ 080b6ace 8021
    lsls r1,r1,#0x8    @ 080b6ad0 0902
    cmp r0,r1                                @ 080b6ad2 8842
    bne LAB_080b6b0c                         @ 080b6ad4 1ad1
    adds r0,r5,#0x0    @ 080b6ad6 281c
    movs r1,#0x0    @ 080b6ad8 0021
    bl read_effect_slot_side_and_type        @ 080b6ada caf747f9
    lsls r0,r0,#0x10    @ 080b6ade 0004
    lsrs r0,r0,#0x18    @ 080b6ae0 000e
    cmp r0,#0xa                              @ 080b6ae2 0a28
    bhi LAB_080b6b0c                         @ 080b6ae4 12d8
    adds r0,r5,#0x0    @ 080b6ae6 281c
    movs r1,#0x0    @ 080b6ae8 0021
    bl read_effect_slot_side_and_type        @ 080b6aea caf73ff9
    lsls r1,r0,#0x18    @ 080b6aee 0106
    lsrs r3,r1,#0x18    @ 080b6af0 0b0e
    lsls r0,r0,#0x10    @ 080b6af2 0004
    lsrs r2,r0,#0x18    @ 080b6af4 020e
    lsls r1,r3,#0x4    @ 080b6af6 1901
    adds r1,r1,r2    @ 080b6af8 8918
    movs r0,#0x1    @ 080b6afa 0120
    lsls r0,r1    @ 080b6afc 8840
    .hword 0x464f    @ 080b6afe 4f46
    ands r0,r7    @ 080b6b00 3840
    cmp r0,#0x0                              @ 080b6b02 0028
    beq LAB_080b6b0c                         @ 080b6b04 02d0
    adds r0,r6,#0x0    @ 080b6b06 301c
    adds r1,r3,#0x0    @ 080b6b08 191c
    b enqueue_equip_slot_sprite_success      @ 080b6b0a 65e0
LAB_080b6b0c:
    movs r1,#0xfc    @ 080b6b0c fc21
    lsls r1,r1,#0x4    @ 080b6b0e 0901
    ldrh r0,[r6,#0x2]                        @ 080b6b10 7088
    ands r1,r0    @ 080b6b12 0140
    movs r0,#0x90    @ 080b6b14 9020
    lsls r0,r0,#0x3    @ 080b6b16 c000
    cmp r1,r0                                @ 080b6b18 8142
    beq LAB_080b6b22                         @ 080b6b1a 02d0
    adds r0,#0x40    @ 080b6b1c 4030
    cmp r1,r0                                @ 080b6b1e 8142
    bne exec_equip_target_by_comparator_then_scored_fallback @ 080b6b20 16d1
LAB_080b6b22:
    ldr r2, DAT_080b6b4c                     @ 080b6b22 0a4a
    ldrb r1,[r6,#0x2]                        @ 080b6b24 b178
    lsls r0,r1,#0x1f    @ 080b6b26 c807
    lsrs r0,r0,#0x1f    @ 080b6b28 c00f
    movs r4,#0x1    @ 080b6b2a 0124
    subs r0,r4,r0    @ 080b6b2c 201a
    ldr r3,[r2,#0x0]                         @ 080b6b2e 1368
    cmp r3,r0                                @ 080b6b30 8342
    bne exec_equip_target_by_comparator_then_scored_fallback @ 080b6b32 0dd1
    lsls r1,r3,#0x4    @ 080b6b34 1901
    ldr r2,[r2,#0x1c]                        @ 080b6b36 d269
    adds r1,r1,r2    @ 080b6b38 8918
    adds r0,r4,#0x0    @ 080b6b3a 201c
    lsls r0,r1    @ 080b6b3c 8840
    .hword 0x464f    @ 080b6b3e 4f46
    ands r0,r7    @ 080b6b40 3840
    cmp r0,#0x0                              @ 080b6b42 0028
    beq exec_equip_target_by_comparator_then_scored_fallback @ 080b6b44 04d0
    adds r0,r6,#0x0    @ 080b6b46 301c
    adds r1,r3,#0x0    @ 080b6b48 191c
    b enqueue_equip_slot_sprite_success      @ 080b6b4a 45e0
DAT_080b6b4c:
    .word  0x0201bb90                     @ 080b6b4c 90bb0102

@ Equip target selection case fragment (comparator function + scored fallback). Inlined in FUN_080b5d98 (0x080b5d98); also tail-called from FUN_080b6ac2. Parent frame r6=equip_card_zone_ptr, r9=equip_zone_bitmap. Computes player_id = 1 - [r6+2] bit0; calls find_best_slot_from_bitmap_by_comparator(player, r9_bitmap, comparator=DAT_080b6b6c=0x080b5bed); if result >=0 -> success path LAB_080b6bd2 -> FUN_080b6bd8; if <0 -> fallback: computes player (1-player_bit), calls find_best_scored_slot_from_bitmap(player, bitmap, 1, 0) with r9=bitmap; if still <0 -> FUN_080b6be0 (fail). Side effects: via success path, writes target.
@ 
@ Constants:
@ - comparator_fn=0x080b5bed (DAT_080b6b6c, score_slot_by_equip_chain_presence THUMB ptr)
exec_equip_target_by_comparator_then_scored_fallback:
    ldrb r1,[r6,#0x2]                        @ 080b6b50 b178
    lsls r0,r1,#0x1f    @ 080b6b52 c807
    lsrs r0,r0,#0x1f    @ 080b6b54 c00f
    ldr r2, DAT_080b6b6c                     @ 080b6b56 054a
    .hword 0x4649    @ 080b6b58 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b6b5a fef705fa
    adds r4,r0,#0x0    @ 080b6b5e 041c
    cmp r4,#0x0                              @ 080b6b60 002c
    blt LAB_080b6b70                         @ 080b6b62 05db
    ldrb r3,[r6,#0x2]                        @ 080b6b64 b378
    lsls r1,r3,#0x1f    @ 080b6b66 d907
    b LAB_080b6bd2                           @ 080b6b68 33e0
    .zero  0x2
DAT_080b6b6c:
    .word  0x080b5bed                     @ 080b6b6c ed5b0b08
LAB_080b6b70:
    ldrb r7,[r6,#0x2]                        @ 080b6b70 b778
    lsls r0,r7,#0x1f    @ 080b6b72 f807
    lsrs r0,r0,#0x1f    @ 080b6b74 c00f
    movs r5,#0x1    @ 080b6b76 0125
    subs r0,r5,r0    @ 080b6b78 281a
    .hword 0x4649    @ 080b6b7a 4946
    movs r2,#0x1    @ 080b6b7c 0122
    movs r3,#0x0    @ 080b6b7e 0023
    bl find_best_scored_slot_from_bitmap     @ 080b6b80 fef7c2f8
    adds r4,r0,#0x0    @ 080b6b84 041c
    cmp r4,#0x0                              @ 080b6b86 002c
    blt select_equip_target_for_opponent_random @ 080b6b88 2adb
    ldrb r0,[r6,#0x2]                        @ 080b6b8a b078
    lsls r1,r0,#0x1f    @ 080b6b8c c107
    lsrs r1,r1,#0x1f    @ 080b6b8e c90f
    subs r1,r5,r1    @ 080b6b90 691a
    b LAB_080b6bd4                           @ 080b6b92 1fe0

@ Equip target selection case fragment (field5 comparator strategy). Inlined in FUN_080b5d98 (0x080b5d98); bl entry at 0x080b60de and 0x080b62c6. Parent frame r6=equip_card_zone_ptr, r9=equip_zone_bitmap. Computes player_id = 1 - [r6+2] bit0; calls find_best_slot_from_bitmap_by_comparator(player, bitmap, comparator=DAT_080b6bb8=0x080b5ce9 = score_slot_by_zone_lock_and_type THUMB ptr); if >=0 -> LAB_080b6bd4 success; if <0 -> FUN_080b6be0 fail. Side effects: via success path, writes target.
@ 
@ Constants:
@ - comparator_fn=0x080b5ce9 (DAT_080b6bb8, score_slot_by_zone_lock_and_type THUMB ptr)
exec_equip_target_by_comparator_field5_scored:
    ldrb r1,[r6,#0x2]                        @ 080b6b94 b178
    lsls r0,r1,#0x1f    @ 080b6b96 c807
    lsrs r0,r0,#0x1f    @ 080b6b98 c00f
    movs r5,#0x1    @ 080b6b9a 0125
    subs r0,r5,r0    @ 080b6b9c 281a
    ldr r2, DAT_080b6bb8                     @ 080b6b9e 064a
    .hword 0x4649    @ 080b6ba0 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b6ba2 fef7e1f9
    adds r4,r0,#0x0    @ 080b6ba6 041c
    cmp r4,#0x0                              @ 080b6ba8 002c
    blt select_equip_target_for_opponent_random @ 080b6baa 19db
    ldrb r3,[r6,#0x2]                        @ 080b6bac b378
    lsls r1,r3,#0x1f    @ 080b6bae d907
    lsrs r1,r1,#0x1f    @ 080b6bb0 c90f
    subs r1,r5,r1    @ 080b6bb2 691a
    b LAB_080b6bd4                           @ 080b6bb4 0ee0
    .zero  0x2
DAT_080b6bb8:
    .word  0x080b5ce9                     @ 080b6bb8 e95c0b08
LAB_080b6bbc:
    lsrs r1,r2,#0x1f    @ 080b6bbc d10f
    subs r1,r5,r1    @ 080b6bbe 691a
    b LAB_080b6bd4                           @ 080b6bc0 08e0
LAB_080b6bc2:
    adds r0,r6,#0x0    @ 080b6bc2 301c
    adds r1,r3,#0x0    @ 080b6bc4 191c
    b enqueue_equip_slot_sprite_success      @ 080b6bc6 07e0
LAB_080b6bc8:
    ldrb r7,[r6,#0x2]                        @ 080b6bc8 b778
    lsls r1,r7,#0x1f    @ 080b6bca f907
    b LAB_080b6bd2                           @ 080b6bcc 01e0
LAB_080b6bce:
    ldrb r0,[r6,#0x2]                        @ 080b6bce b078
    lsls r1,r0,#0x1f    @ 080b6bd0 c107
LAB_080b6bd2:
    lsrs r1,r1,#0x1f    @ 080b6bd2 c90f
LAB_080b6bd4:
    adds r0,r6,#0x0    @ 080b6bd4 301c
LAB_080b6bd6:
    adds r2,r4,#0x0    @ 080b6bd6 221c

@ Equip sprite enqueue success exit stub. No independent inputs (r0/r1/r2 passed through from caller FUN_080b5d98 equip target BST dispatch context). Calls enqueue_equip_slot_sprite_with_code_rotation to enqueue equip sprite rotation animation, sets r0=1, then branches to restore_equip_dispatch_frame at shared exit frame. Serves as the convergence tail-jump point for multiple success branches of FUN_080b5d98; symmetric to failure exit FUN_080b6be0.
@ 
@ Constants:
@ - SUCCESS_CODE = 1 (fixed return value, movs r0,#1)
enqueue_equip_slot_sprite_success:
    bl enqueue_equip_slot_sprite_with_code_rotation @ 080b6bd8 caf760f8
    movs r0,#0x1    @ 080b6bdc 0120
    b restore_equip_dispatch_frame           @ 080b6bde 0be0

@ 装备目标选择的默认随机分支片段. 属于 commit_equip_target_slot_by_card_id 卡牌 ID 分派树的兜底路径: 从父帧继承的 r6 (装备效果节点指针) 读 [r6+2] bit0 与 [r6+3] bit6 异或得到出战玩家, 再用 1 减得到对手玩家编号, 然后以对手编号转调 find_equip_target_by_random_order(zone_ptr, opponent_player) 在对手场上随机扫描装备目标槽. 无独立 prologue, 复用父函数寄存器并经 restore_equip_dispatch_frame 退出.
select_equip_target_for_opponent_random:
    ldrb r1,[r6,#0x2]                        @ 080b6be0 b178
    lsls r2,r1,#0x1f    @ 080b6be2 ca07
    lsrs r2,r2,#0x1f    @ 080b6be4 d20f
    ldrb r3,[r6,#0x3]                        @ 080b6be6 f378
    lsls r0,r3,#0x19    @ 080b6be8 5806
    lsrs r0,r0,#0x1f    @ 080b6bea c00f
    eors r2,r0    @ 080b6bec 4240
    movs r1,#0x1    @ 080b6bee 0121
    subs r1,r1,r2    @ 080b6bf0 891a
LAB_080b6bf2:
    adds r0,r6,#0x0    @ 080b6bf2 301c
    bl find_equip_target_by_random_order     @ 080b6bf4 fef76eff

@ Shared function epilogue frame (shared by FUN_080b5d98 and FUN_080b6c08). Restores sp+0x2c, pops {r3,r4,r5} to restore r8/r9/r10 (via mov r8,r3 / mov r9,r4 / mov r10,r5), then pops {r4,r5,r6,r7}, finally pops {r1}; bx r1 to return. All case fragments in success (FUN_080b6bd8 -> movs r0,#1) or failure (FUN_080b6be0 -> FUN_080b5ad4) paths converge here. r0=1 (success) or r0=0 (fallback from FUN_080b6be0 path) is set by preceding code; this function does not modify r0. Side effects: restores caller-saved r4-r10.
@ 
@ Constants:
@ - sp_frame_size=0x2c
restore_equip_dispatch_frame:
    add sp,#0x2c                             @ 080b6bf8 0bb0
    pop {r3,r4,r5}                           @ 080b6bfa 38bc
    .hword 0x4698    @ 080b6bfc 9846
    .hword 0x46a1    @ 080b6bfe a146
    .hword 0x46aa    @ 080b6c00 aa46
    pop {r4,r5,r6,r7}                        @ 080b6c02 f0bc
    pop {r1}                                 @ 080b6c04 02bc
    bx r1                                    @ 080b6c06 0847

@ Equip card target slot commit function. Entry: r0=player_id, r1=card_id, r2=slot_predicate_fn_ptr. Writes player_id to global state [0x0201afe0] and [gP1LifePoints+0x1d64], then calls build_equip_zone_bitmap_for_player(r2) to generate candidate bitmap (stored in r9). Then uses multi-level BST (cmp/bgt tree) on r1=card_id to dispatch each special equip card to a different target search strategy: select_equip_target_slot_with_eligibility_check / select_equip_target_slot_full / select_equip_target_slot_by_eligible_set / find_best_scored_slot_from_bitmap / find_best_slot_from_bitmap_by_comparator / sample_random_slot_from_bitmap / eval_equip_chain_score_for_slot + dispatch_effect_handler_by_card_id / check_card_type_is_spell. On success: calls init_duel_zone_target_slot_refs(zone_ptr, slot_idx, 0, 0xb) to commit target reference. Called by FUN_08096a4c/FUN_08096ab0 after checking equip activation state flag ([0x0201e2a0+player*4+8]==1). Exit via pop {r0}; bx r0 (Pattern B, void return).
@ 
@ Constants:
@ - EQUIP_PLAYER_STATE=0x0201afe0
@ - PLAYER_FIELD_OFFSET=0x1d64 (gP1LifePoints+0x1d64)
@ - EQUIP_ZONE_BASE=0x0201b290, PLAYER_STRIDE=0x868 (offset 0x484 into base)
@ - card_id_dispatch_tree: 0x1702=Anti-Aircraft Flower, 0x140b=Insect Imitation, 0x1254=Widespread Ruin, 0x11f0=Greenkappa, 0x0fff=Catapult Turtle, 0x1391=Riryoku, 0x13fc=Multiplication of Ants, 0x140a=Shift, 0x151e=Last Turn, 0x14c5=Throwstone Unit, 0x164b=Guardian Ceal, 0x169b=Checkmate, 0x17f5=Level Up!, 0x1715=Ultra Evolution Pill, 0x17e1=Ultimate Baseball Kid, 0x17ec=Hade-Hane, 0x17f2=Hammer Shot, 0x18ca=Gift of the Martyr, 0x187e=Release Restraint, 0x188c=Deck Devastation Virus, 0x192a=Spiritual Wind Art - Miyabi, 0x19a5=Raviel Lord of Phantasms, 0x19b5=Attack Reflector Unit, 0x15a3=Metamorphosis, 0x1927=Spiritual Earth Art - Kurogane, 0x1147=gap/reserved
@ - gDuelFieldSlots=0x0201c510
@ - EQUIP_ZONE_TYPE=0xb
commit_equip_target_slot_by_card_id:
    push {r4,r5,r6,r7,lr}                    @ 080b6c08 f0b5
    .hword 0x4657    @ 080b6c0a 5746
    .hword 0x464e    @ 080b6c0c 4e46
    .hword 0x4645    @ 080b6c0e 4546
    push {r5,r6,r7}                          @ 080b6c10 e0b4
    adds r6,r0,#0x0    @ 080b6c12 061c
    adds r4,r1,#0x0    @ 080b6c14 0c1c
    adds r1,r2,#0x0    @ 080b6c16 111c
    ldr r0, DAT_080b6c70                     @ 080b6c18 1548
    ldr r2, DAT_080b6c74                     @ 080b6c1a 164a
    adds r0,r0,r2    @ 080b6c1c 8018
    ldr r0,[r0,#0x0]                         @ 080b6c1e 0068
    bl build_equip_zone_bitmap_for_player    @ 080b6c20 d9f754fd
    .hword 0x4681    @ 080b6c24 8146
    ldr r0, DAT_080b6c78                     @ 080b6c26 1448
    str r6,[r0,#0x0]                         @ 080b6c28 0660
    ldr r0, PTR_gP1LifePoints_080b6c7c       @ 080b6c2a 1448
    ldr r1, DAT_080b6c80                     @ 080b6c2c 1449
    adds r0,r0,r1    @ 080b6c2e 4018
    str r6,[r0,#0x0]                         @ 080b6c30 0660
    ldr r0, DAT_080b6c84                     @ 080b6c32 1448
    cmp r4,r0                                @ 080b6c34 8442
    bne LAB_080b6c3a                         @ 080b6c36 00d1
    b LAB_080b6f60                           @ 080b6c38 92e1
LAB_080b6c3a:
    cmp r4,r0                                @ 080b6c3a 8442
    ble LAB_080b6c40                         @ 080b6c3c 00dd
    b LAB_080b6d5e                           @ 080b6c3e 8ee0
LAB_080b6c40:
    ldr r0, DAT_080b6c88                     @ 080b6c40 1148
    cmp r4,r0                                @ 080b6c42 8442
    bne LAB_080b6c48                         @ 080b6c44 00d1
    b LAB_080b6e68                           @ 080b6c46 0fe1
LAB_080b6c48:
    cmp r4,r0                                @ 080b6c48 8442
    bgt LAB_080b6ce0                         @ 080b6c4a 49dc
    ldr r0, DAT_080b6c8c                     @ 080b6c4c 0f48
    cmp r4,r0                                @ 080b6c4e 8442
    bne LAB_080b6c54                         @ 080b6c50 00d1
    b LAB_080b6f92                           @ 080b6c52 9ee1
LAB_080b6c54:
    cmp r4,r0                                @ 080b6c54 8442
    bgt LAB_080b6ca8                         @ 080b6c56 27dc
    ldr r0, DAT_080b6c90                     @ 080b6c58 0d48
    cmp r4,r0                                @ 080b6c5a 8442
    bne LAB_080b6c60                         @ 080b6c5c 00d1
    b LAB_080b6f92                           @ 080b6c5e 98e1
LAB_080b6c60:
    cmp r4,r0                                @ 080b6c60 8442
    bgt LAB_080b6c98                         @ 080b6c62 19dc
    cmp r4,#0x1                              @ 080b6c64 012c
    bne LAB_080b6c6a                         @ 080b6c66 00d1
    b LAB_080b6f60                           @ 080b6c68 7ae1
LAB_080b6c6a:
    ldr r0, DAT_080b6c94                     @ 080b6c6a 0a48
    b LAB_080b6e5a                           @ 080b6c6c f5e0
    .zero  0x2
DAT_080b6c70:
    .word  0x0201b290                     @ 080b6c70 90b20102
DAT_080b6c74:
    .word  0x00000484                     @ 080b6c74 84040000
DAT_080b6c78:
    .word  0x0201afe0                     @ 080b6c78 e0af0102
PTR_gP1LifePoints_080b6c7c:
    .word  gP1LifePoints                  @ 080b6c7c e0c40102
DAT_080b6c80:
    .word  0x00001d64                     @ 080b6c80 641d0000
DAT_080b6c84:
    .word  0x00001702                     @ 080b6c84 02170000
DAT_080b6c88:
    .word  0x0000140b                     @ 080b6c88 0b140000
DAT_080b6c8c:
    .word  0x00001254                     @ 080b6c8c 54120000
DAT_080b6c90:
    .word  0x00001147                     @ 080b6c90 47110000
DAT_080b6c94:
    .word  0x00000fff                     @ 080b6c94 ff0f0000
LAB_080b6c98:
    ldr r0, DAT_080b6ca4                     @ 080b6c98 0248
    cmp r4,r0                                @ 080b6c9a 8442
    bne LAB_080b6ca0                         @ 080b6c9c 00d1
    b LAB_080b6f92                           @ 080b6c9e 78e1
LAB_080b6ca0:
    adds r0,#0x4b    @ 080b6ca0 4b30
    b LAB_080b6e5a                           @ 080b6ca2 dae0
DAT_080b6ca4:
    .word  0x000011f0                     @ 080b6ca4 f0110000
LAB_080b6ca8:
    ldr r0, DAT_080b6cc0                     @ 080b6ca8 0548
    cmp r4,r0                                @ 080b6caa 8442
    bne LAB_080b6cb0                         @ 080b6cac 00d1
    b LAB_080b6fd6                           @ 080b6cae 92e1
LAB_080b6cb0:
    cmp r4,r0                                @ 080b6cb0 8442
    bgt LAB_080b6cc4                         @ 080b6cb2 07dc
    subs r0,#0xcc    @ 080b6cb4 cc38
    cmp r4,r0                                @ 080b6cb6 8442
    bne LAB_080b6cbc                         @ 080b6cb8 00d1
    b LAB_080b6f60                           @ 080b6cba 51e1
LAB_080b6cbc:
    adds r0,#0x1e    @ 080b6cbc 1e30
    b LAB_080b6e12                           @ 080b6cbe a8e0
DAT_080b6cc0:
    .word  0x00001391                     @ 080b6cc0 91130000
LAB_080b6cc4:
    ldr r0, DAT_080b6cd4                     @ 080b6cc4 0348
    cmp r4,r0                                @ 080b6cc6 8442
    bne LAB_080b6ccc                         @ 080b6cc8 00d1
    b LAB_080b6f60                           @ 080b6cca 49e1
LAB_080b6ccc:
    cmp r4,r0                                @ 080b6ccc 8442
    bgt LAB_080b6cd8                         @ 080b6cce 03dc
    subs r0,#0x54    @ 080b6cd0 5438
    b LAB_080b6e5a                           @ 080b6cd2 c2e0
DAT_080b6cd4:
    .word  0x000013fc                     @ 080b6cd4 fc130000
LAB_080b6cd8:
    ldr r0, DAT_080b6cdc                     @ 080b6cd8 0048
    b LAB_080b6d02                           @ 080b6cda 12e0
DAT_080b6cdc:
    .word  0x0000140a                     @ 080b6cdc 0a140000
LAB_080b6ce0:
    ldr r0, DAT_080b6d0c                     @ 080b6ce0 0a48
    cmp r4,r0                                @ 080b6ce2 8442
    bne LAB_080b6ce8                         @ 080b6ce4 00d1
    b LAB_080b6fd6                           @ 080b6ce6 76e1
LAB_080b6ce8:
    cmp r4,r0                                @ 080b6ce8 8442
    bgt LAB_080b6d20                         @ 080b6cea 19dc
    subs r0,#0x94    @ 080b6cec 9438
    cmp r4,r0                                @ 080b6cee 8442
    bne LAB_080b6cf4                         @ 080b6cf0 00d1
    b LAB_080b6fe4                           @ 080b6cf2 77e1
LAB_080b6cf4:
    cmp r4,r0                                @ 080b6cf4 8442
    bgt LAB_080b6d10                         @ 080b6cf6 0bdc
    subs r0,#0x1a    @ 080b6cf8 1a38
    cmp r4,r0                                @ 080b6cfa 8442
    bne LAB_080b6d00                         @ 080b6cfc 00d1
    b LAB_080b6f92                           @ 080b6cfe 48e1
LAB_080b6d00:
    adds r0,#0x6    @ 080b6d00 0630
LAB_080b6d02:
    cmp r4,r0                                @ 080b6d02 8442
    bne LAB_080b6d08                         @ 080b6d04 00d1
    b LAB_080b6fe4                           @ 080b6d06 6de1
LAB_080b6d08:
    b LAB_080b7020                           @ 080b6d08 8ae1
    .zero  0x2
DAT_080b6d0c:
    .word  0x0000151e                     @ 080b6d0c 1e150000
LAB_080b6d10:
    ldr r0, DAT_080b6d1c                     @ 080b6d10 0248
    cmp r4,r0                                @ 080b6d12 8442
    bne LAB_080b6d18                         @ 080b6d14 00d1
    b LAB_080b6f60                           @ 080b6d16 23e1
LAB_080b6d18:
    adds r0,#0x1f    @ 080b6d18 1f30
    b LAB_080b6e5a                           @ 080b6d1a 9ee0
DAT_080b6d1c:
    .word  0x000014c5                     @ 080b6d1c c5140000
LAB_080b6d20:
    ldr r0, DAT_080b6d40                     @ 080b6d20 0748
    cmp r4,r0                                @ 080b6d22 8442
    bne LAB_080b6d28                         @ 080b6d24 00d1
    b LAB_080b6f60                           @ 080b6d26 1be1
LAB_080b6d28:
    cmp r4,r0                                @ 080b6d28 8442
    bgt LAB_080b6d44                         @ 080b6d2a 0bdc
    subs r0,#0xbf    @ 080b6d2c bf38
    cmp r4,r0                                @ 080b6d2e 8442
    bne LAB_080b6d34                         @ 080b6d30 00d1
    b LAB_080b6f60                           @ 080b6d32 15e1
LAB_080b6d34:
    adds r0,#0x17    @ 080b6d34 1730
    cmp r4,r0                                @ 080b6d36 8442
    bne LAB_080b6d3c                         @ 080b6d38 00d1
    b LAB_080b6f26                           @ 080b6d3a f4e0
LAB_080b6d3c:
    b LAB_080b7020                           @ 080b6d3c 70e1
    .zero  0x2
DAT_080b6d40:
    .word  0x0000164b                     @ 080b6d40 4b160000
LAB_080b6d44:
    ldr r0, DAT_080b6d54                     @ 080b6d44 0348
    cmp r4,r0                                @ 080b6d46 8442
    bne LAB_080b6d4c                         @ 080b6d48 00d1
    b LAB_080b6f60                           @ 080b6d4a 09e1
LAB_080b6d4c:
    cmp r4,r0                                @ 080b6d4c 8442
    bgt LAB_080b6d58                         @ 080b6d4e 03dc
    subs r0,#0x1e    @ 080b6d50 1e38
    b LAB_080b6e5a                           @ 080b6d52 82e0
DAT_080b6d54:
    .word  0x0000169b                     @ 080b6d54 9b160000
LAB_080b6d58:
    movs r0,#0xb5    @ 080b6d58 b520
    lsls r0,r0,#0x5    @ 080b6d5a 4001
    b LAB_080b6e5a                           @ 080b6d5c 7de0
LAB_080b6d5e:
    ldr r0, DAT_080b6d90                     @ 080b6d5e 0c48
    cmp r4,r0                                @ 080b6d60 8442
    bne LAB_080b6d66                         @ 080b6d62 00d1
    b LAB_080b700e                           @ 080b6d64 53e1
LAB_080b6d66:
    cmp r4,r0                                @ 080b6d66 8442
    bgt LAB_080b6ddc                         @ 080b6d68 38dc
    subs r0,#0xa2    @ 080b6d6a a238
    cmp r4,r0                                @ 080b6d6c 8442
    bne LAB_080b6d72                         @ 080b6d6e 00d1
    b LAB_080b6f60                           @ 080b6d70 f6e0
LAB_080b6d72:
    cmp r4,r0                                @ 080b6d72 8442
    bgt LAB_080b6da4                         @ 080b6d74 16dc
    subs r0,#0x40    @ 080b6d76 4038
    cmp r4,r0                                @ 080b6d78 8442
    bne LAB_080b6d7e                         @ 080b6d7a 00d1
    b LAB_080b6f60                           @ 080b6d7c f0e0
LAB_080b6d7e:
    cmp r4,r0                                @ 080b6d7e 8442
    bgt LAB_080b6d94                         @ 080b6d80 08dc
    subs r0,#0xb    @ 080b6d82 0b38
    cmp r4,r0                                @ 080b6d84 8442
    bne LAB_080b6d8a                         @ 080b6d86 00d1
    b LAB_080b6f60                           @ 080b6d88 eae0
LAB_080b6d8a:
    adds r0,#0x9    @ 080b6d8a 0930
    b LAB_080b6e12                           @ 080b6d8c 41e0
    .zero  0x2
DAT_080b6d90:
    .word  0x000017f5                     @ 080b6d90 f5170000
LAB_080b6d94:
    ldr r0, DAT_080b6da0                     @ 080b6d94 0248
    cmp r4,r0                                @ 080b6d96 8442
    bne LAB_080b6d9c                         @ 080b6d98 00d1
    b LAB_080b6f60                           @ 080b6d9a e1e0
LAB_080b6d9c:
    adds r0,#0x23    @ 080b6d9c 2330
    b LAB_080b6e12                           @ 080b6d9e 38e0
DAT_080b6da0:
    .word  0x00001715                     @ 080b6da0 15170000
LAB_080b6da4:
    ldr r0, DAT_080b6dbc                     @ 080b6da4 0548
    cmp r4,r0                                @ 080b6da6 8442
    bne LAB_080b6dac                         @ 080b6da8 00d1
    b LAB_080b6f60                           @ 080b6daa d9e0
LAB_080b6dac:
    cmp r4,r0                                @ 080b6dac 8442
    bgt LAB_080b6dc0                         @ 080b6dae 07dc
    subs r0,#0x79    @ 080b6db0 7938
    cmp r4,r0                                @ 080b6db2 8442
    bne LAB_080b6db8                         @ 080b6db4 00d1
    b LAB_080b6f60                           @ 080b6db6 d3e0
LAB_080b6db8:
    adds r0,#0x33    @ 080b6db8 3330
    b LAB_080b6e5a                           @ 080b6dba 4ee0
DAT_080b6dbc:
    .word  0x000017e1                     @ 080b6dbc e1170000
LAB_080b6dc0:
    ldr r0, DAT_080b6dd0                     @ 080b6dc0 0348
    cmp r4,r0                                @ 080b6dc2 8442
    bne LAB_080b6dc8                         @ 080b6dc4 00d1
    b LAB_080b6fb4                           @ 080b6dc6 f5e0
LAB_080b6dc8:
    cmp r4,r0                                @ 080b6dc8 8442
    bgt LAB_080b6dd4                         @ 080b6dca 03dc
    subs r0,#0x2    @ 080b6dcc 0238
    b LAB_080b6e12                           @ 080b6dce 20e0
DAT_080b6dd0:
    .word  0x000017ec                     @ 080b6dd0 ec170000
LAB_080b6dd4:
    ldr r0, DAT_080b6dd8                     @ 080b6dd4 0048
    b LAB_080b6e12                           @ 080b6dd6 1ce0
DAT_080b6dd8:
    .word  0x000017f2                     @ 080b6dd8 f2170000
LAB_080b6ddc:
    ldr r0, DAT_080b6e00                     @ 080b6ddc 0848
    cmp r4,r0                                @ 080b6dde 8442
    bne LAB_080b6de4                         @ 080b6de0 00d1
    b LAB_080b6f60                           @ 080b6de2 bde0
LAB_080b6de4:
    cmp r4,r0                                @ 080b6de4 8442
    bgt LAB_080b6e28                         @ 080b6de6 1fdc
    subs r0,#0x75    @ 080b6de8 7538
    cmp r4,r0                                @ 080b6dea 8442
    bne LAB_080b6df0                         @ 080b6dec 00d1
    b LAB_080b6f60                           @ 080b6dee b7e0
LAB_080b6df0:
    cmp r4,r0                                @ 080b6df0 8442
    bgt LAB_080b6e04                         @ 080b6df2 07dc
    subs r0,#0x47    @ 080b6df4 4738
    cmp r4,r0                                @ 080b6df6 8442
    bne LAB_080b6dfc                         @ 080b6df8 00d1
    b LAB_080b6f60                           @ 080b6dfa b1e0
LAB_080b6dfc:
    adds r0,#0x27    @ 080b6dfc 2730
    b LAB_080b6e5a                           @ 080b6dfe 2ce0
DAT_080b6e00:
    .word  0x000018ca                     @ 080b6e00 ca180000
LAB_080b6e04:
    ldr r0, DAT_080b6e1c                     @ 080b6e04 0548
    cmp r4,r0                                @ 080b6e06 8442
    bne LAB_080b6e0c                         @ 080b6e08 00d1
    b LAB_080b6f60                           @ 080b6e0a a9e0
LAB_080b6e0c:
    cmp r4,r0                                @ 080b6e0c 8442
    bgt LAB_080b6e20                         @ 080b6e0e 07dc
    subs r0,#0x6    @ 080b6e10 0638
LAB_080b6e12:
    cmp r4,r0                                @ 080b6e12 8442
    bne LAB_080b6e18                         @ 080b6e14 00d1
    b LAB_080b6f92                           @ 080b6e16 bce0
LAB_080b6e18:
    b LAB_080b7020                           @ 080b6e18 02e1
    .zero  0x2
DAT_080b6e1c:
    .word  0x0000187e                     @ 080b6e1c 7e180000
LAB_080b6e20:
    ldr r0, DAT_080b6e24                     @ 080b6e20 0048
    b LAB_080b6e5a                           @ 080b6e22 1ae0
DAT_080b6e24:
    .word  0x0000188c                     @ 080b6e24 8c180000
LAB_080b6e28:
    ldr r0, DAT_080b6e40                     @ 080b6e28 0548
    cmp r4,r0                                @ 080b6e2a 8442
    bgt LAB_080b6e44                         @ 080b6e2c 0adc
    subs r0,#0x2    @ 080b6e2e 0238
    cmp r4,r0                                @ 080b6e30 8442
    blt LAB_080b6e36                         @ 080b6e32 00db
    b LAB_080b6f60                           @ 080b6e34 94e0
LAB_080b6e36:
    subs r0,#0x1    @ 080b6e36 0138
    cmp r4,r0                                @ 080b6e38 8442
    beq LAB_080b6e68                         @ 080b6e3a 15d0
    b LAB_080b7020                           @ 080b6e3c f0e0
    .zero  0x2
DAT_080b6e40:
    .word  0x0000192a                     @ 080b6e40 2a190000
LAB_080b6e44:
    ldr r0, DAT_080b6e54                     @ 080b6e44 0348
    cmp r4,r0                                @ 080b6e46 8442
    bne LAB_080b6e4c                         @ 080b6e48 00d1
    b LAB_080b6f60                           @ 080b6e4a 89e0
LAB_080b6e4c:
    cmp r4,r0                                @ 080b6e4c 8442
    bgt LAB_080b6e58                         @ 080b6e4e 03dc
    subs r0,#0x4e    @ 080b6e50 4e38
    b LAB_080b6e5a                           @ 080b6e52 02e0
DAT_080b6e54:
    .word  0x000019a5                     @ 080b6e54 a5190000
LAB_080b6e58:
    ldr r0, DAT_080b6e64                     @ 080b6e58 0248
LAB_080b6e5a:
    cmp r4,r0                                @ 080b6e5a 8442
    bne LAB_080b6e60                         @ 080b6e5c 00d1
    b LAB_080b6f60                           @ 080b6e5e 7fe0
LAB_080b6e60:
    b LAB_080b7020                           @ 080b6e60 dee0
    .zero  0x2
DAT_080b6e64:
    .word  0x000019b5                     @ 080b6e64 b5190000
LAB_080b6e68:
    ldr r0, DAT_080b6e7c                     @ 080b6e68 0448
    cmp r4,r0                                @ 080b6e6a 8442
    beq LAB_080b6f26                         @ 080b6e6c 5bd0
    cmp r4,r0                                @ 080b6e6e 8442
    bgt LAB_080b6e84                         @ 080b6e70 08dc
    ldr r0, DAT_080b6e80                     @ 080b6e72 0348
    cmp r4,r0                                @ 080b6e74 8442
    beq LAB_080b6ef4                         @ 080b6e76 3dd0
    b LAB_080b6f60                           @ 080b6e78 72e0
    .zero  0x2
DAT_080b6e7c:
    .word  0x000015a3                     @ 080b6e7c a3150000
DAT_080b6e80:
    .word  0x0000140b                     @ 080b6e80 0b140000
LAB_080b6e84:
    ldr r0, DAT_080b6ee8                     @ 080b6e84 1848
    cmp r4,r0                                @ 080b6e86 8442
    bne LAB_080b6f60                         @ 080b6e88 6ad1
    movs r5,#0x0    @ 080b6e8a 0025
    lsls r7,r6,#0x4    @ 080b6e8c 3701
    movs r4,#0x1    @ 080b6e8e 0124
    adds r0,r6,#0x0    @ 080b6e90 301c
    ands r0,r4    @ 080b6e92 2040
    .hword 0x46a8    @ 080b6e94 a846
    ldr r1, DAT_080b6eec                     @ 080b6e96 1549
    adds r2,r0,#0x0    @ 080b6e98 021c
    muls r2,r1    @ 080b6e9a 4a43
    .hword 0x4692    @ 080b6e9c 9246
LAB_080b6e9e:
    adds r1,r7,r5    @ 080b6e9e 7919
    adds r0,r4,#0x0    @ 080b6ea0 201c
    lsls r0,r1    @ 080b6ea2 8840
    .hword 0x4649    @ 080b6ea4 4946
    ands r0,r1    @ 080b6ea6 0840
    cmp r0,#0x0                              @ 080b6ea8 0028
    beq LAB_080b6edc                         @ 080b6eaa 17d0
    ldr r3, PTR_gP1LifePoints_080b6ef0       @ 080b6eac 104b
    .hword 0x4642    @ 080b6eae 4246
    add r2,r10                               @ 080b6eb0 5244
    adds r0,r3,#0x0    @ 080b6eb2 181c
    adds r0,#0x40    @ 080b6eb4 4030
    adds r0,r2,r0    @ 080b6eb6 1018
    ldr r0,[r0,#0x0]                         @ 080b6eb8 0068
    lsrs r1,r0,#0x16    @ 080b6eba 810d
    ands r1,r4    @ 080b6ebc 2140
    lsrs r0,r0,#0x17    @ 080b6ebe c00d
    ands r0,r4    @ 080b6ec0 2040
    cmn r1,r0                                @ 080b6ec2 c142
    beq LAB_080b6edc                         @ 080b6ec4 0ad0
    adds r0,r3,#0x0    @ 080b6ec6 181c
    adds r0,#0x30    @ 080b6ec8 3030
    adds r0,r2,r0    @ 080b6eca 1018
    ldr r0,[r0,#0x0]                         @ 080b6ecc 0068
    lsls r0,r0,#0x13    @ 080b6ece c004
    lsrs r0,r0,#0x13    @ 080b6ed0 c00c
    bl get_card_extended_stat_field5         @ 080b6ed2 37f0bdff
    cmp r0,#0x4                              @ 080b6ed6 0428
    bgt LAB_080b6edc                         @ 080b6ed8 00dc
    b LAB_080b7036                           @ 080b6eda ace0
LAB_080b6edc:
    movs r2,#0x14    @ 080b6edc 1422
    add r8,r2                                @ 080b6ede 9044
    adds r5,#0x1    @ 080b6ee0 0135
    cmp r5,#0x4                              @ 080b6ee2 042d
    ble LAB_080b6e9e                         @ 080b6ee4 dbdd
    b LAB_080b6f60                           @ 080b6ee6 3be0
DAT_080b6ee8:
    .word  0x00001927                     @ 080b6ee8 27190000
DAT_080b6eec:
    .word  0x00000868                     @ 080b6eec 68080000
PTR_gP1LifePoints_080b6ef0:
    .word  gP1LifePoints                  @ 080b6ef0 e0c40102
LAB_080b6ef4:
    movs r5,#0x0    @ 080b6ef4 0025
    lsls r7,r6,#0x4    @ 080b6ef6 3701
LAB_080b6ef8:
    adds r1,r7,r5    @ 080b6ef8 7919
    movs r0,#0x1    @ 080b6efa 0120
    lsls r0,r1    @ 080b6efc 8840
    .hword 0x4649    @ 080b6efe 4946
    ands r0,r1    @ 080b6f00 0840
    cmp r0,#0x0                              @ 080b6f02 0028
    beq LAB_080b6f1e                         @ 080b6f04 0bd0
    adds r0,r6,#0x0    @ 080b6f06 301c
    adds r1,r5,#0x0    @ 080b6f08 291c
    bl eval_equip_chain_score_for_slot       @ 080b6f0a 83f74dfd
    adds r2,r0,#0x0    @ 080b6f0e 021c
    adds r0,r6,#0x0    @ 080b6f10 301c
    adds r1,r4,#0x0    @ 080b6f12 211c
    bl dispatch_effect_handler_by_card_id    @ 080b6f14 d6f7ccfd
    cmp r0,#0x0                              @ 080b6f18 0028
    beq LAB_080b6f1e                         @ 080b6f1a 00d0
    b LAB_080b7036                           @ 080b6f1c 8be0
LAB_080b6f1e:
    adds r5,#0x1    @ 080b6f1e 0135
    cmp r5,#0x4                              @ 080b6f20 042d
    ble LAB_080b6ef8                         @ 080b6f22 e9dd
    b LAB_080b6f60                           @ 080b6f24 1ce0
LAB_080b6f26:
    movs r5,#0x0    @ 080b6f26 0025
    lsls r7,r6,#0x4    @ 080b6f28 3701
    movs r2,#0x1    @ 080b6f2a 0122
    .hword 0x4690    @ 080b6f2c 9046
    adds r0,r6,#0x0    @ 080b6f2e 301c
    ands r0,r2    @ 080b6f30 1040
    ldr r1, DAT_080b6f78                     @ 080b6f32 1149
    adds r4,r0,#0x0    @ 080b6f34 041c
    muls r4,r1    @ 080b6f36 4c43
LAB_080b6f38:
    adds r1,r7,r5    @ 080b6f38 7919
    .hword 0x4640    @ 080b6f3a 4046
    lsls r0,r1    @ 080b6f3c 8840
    .hword 0x4649    @ 080b6f3e 4946
    ands r0,r1    @ 080b6f40 0840
    cmp r0,#0x0                              @ 080b6f42 0028
    beq LAB_080b6f58                         @ 080b6f44 08d0
    ldr r0, DAT_080b6f7c                     @ 080b6f46 0d48
    adds r0,r4,r0    @ 080b6f48 2018
    ldr r0,[r0,#0x0]                         @ 080b6f4a 0068
    lsls r0,r0,#0x13    @ 080b6f4c c004
    lsrs r0,r0,#0x13    @ 080b6f4e c00c
    bl check_card_type_is_spell              @ 080b6f50 93f73aff
    cmp r0,#0x0                              @ 080b6f54 0028
    beq LAB_080b7036                         @ 080b6f56 6ed0
LAB_080b6f58:
    adds r4,#0x14    @ 080b6f58 1434
    adds r5,#0x1    @ 080b6f5a 0135
    cmp r5,#0x4                              @ 080b6f5c 042d
    ble LAB_080b6f38                         @ 080b6f5e ebdd
LAB_080b6f60:
    movs r0,#0x1    @ 080b6f60 0120
    subs r4,r0,r6    @ 080b6f62 841b
    adds r0,r4,#0x0    @ 080b6f64 201c
    .hword 0x4649    @ 080b6f66 4946
    movs r2,#0x0    @ 080b6f68 0022
    bl select_equip_target_slot_with_eligibility_check @ 080b6f6a fef7edf9
    adds r5,r0,#0x0    @ 080b6f6e 051c
    cmp r5,#0x0                              @ 080b6f70 002d
    blt LAB_080b6f80                         @ 080b6f72 05db
    adds r0,r4,#0x0    @ 080b6f74 201c
    b LAB_080b7038                           @ 080b6f76 5fe0
DAT_080b6f78:
    .word  0x00000868                     @ 080b6f78 68080000
DAT_080b6f7c:
    .word  0x0201c510                     @ 080b6f7c 10c50102
LAB_080b6f80:
    adds r0,r6,#0x0    @ 080b6f80 301c
    .hword 0x4649    @ 080b6f82 4946
    movs r2,#0x0    @ 080b6f84 0022
    bl select_equip_target_slot_full         @ 080b6f86 fef711fb
LAB_080b6f8a:
    adds r5,r0,#0x0    @ 080b6f8a 051c
    cmp r5,#0x0                              @ 080b6f8c 002d
    blt LAB_080b7020                         @ 080b6f8e 47db
    b LAB_080b7036                           @ 080b6f90 51e0
LAB_080b6f92:
    movs r0,#0x1    @ 080b6f92 0120
    subs r4,r0,r6    @ 080b6f94 841b
    adds r0,r4,#0x0    @ 080b6f96 201c
    .hword 0x4649    @ 080b6f98 4946
    movs r2,#0x1    @ 080b6f9a 0122
    bl select_equip_target_slot_with_eligibility_check @ 080b6f9c fef7d4f9
    adds r5,r0,#0x0    @ 080b6fa0 051c
    cmp r5,#0x0                              @ 080b6fa2 002d
    blt LAB_080b6faa                         @ 080b6fa4 01db
    adds r0,r4,#0x0    @ 080b6fa6 201c
    b LAB_080b7038                           @ 080b6fa8 46e0
LAB_080b6faa:
    adds r0,r6,#0x0    @ 080b6faa 301c
    .hword 0x4649    @ 080b6fac 4946
    bl select_equip_target_slot_by_eligible_set @ 080b6fae fef787fa
    b LAB_080b6f8a                           @ 080b6fb2 eae7
LAB_080b6fb4:
    movs r0,#0x1    @ 080b6fb4 0120
    subs r4,r0,r6    @ 080b6fb6 841b
    adds r0,r4,#0x0    @ 080b6fb8 201c
    .hword 0x4649    @ 080b6fba 4946
    movs r2,#0x0    @ 080b6fbc 0022
    bl select_equip_target_slot_with_eligibility_check @ 080b6fbe fef7c3f9
    adds r5,r0,#0x0    @ 080b6fc2 051c
    cmp r5,#0x0                              @ 080b6fc4 002d
    blt LAB_080b6fcc                         @ 080b6fc6 01db
    adds r0,r4,#0x0    @ 080b6fc8 201c
    b LAB_080b7038                           @ 080b6fca 35e0
LAB_080b6fcc:
    adds r0,r6,#0x0    @ 080b6fcc 301c
    .hword 0x4649    @ 080b6fce 4946
    bl select_equip_target_slot_by_eligible_set @ 080b6fd0 fef776fa
    b LAB_080b6f8a                           @ 080b6fd4 d9e7
LAB_080b6fd6:
    adds r0,r6,#0x0    @ 080b6fd6 301c
    .hword 0x4649    @ 080b6fd8 4946
    movs r2,#0x1    @ 080b6fda 0122
    movs r3,#0x0    @ 080b6fdc 0023
    bl find_best_scored_slot_from_bitmap     @ 080b6fde fdf793fe
    b LAB_080b6f8a                           @ 080b6fe2 d2e7
LAB_080b6fe4:
    movs r0,#0x1    @ 080b6fe4 0120
    subs r4,r0,r6    @ 080b6fe6 841b
    movs r3,#0x1    @ 080b6fe8 0123
    rsbs r3,r3,#0    @ 080b6fea 5b42
    adds r0,r4,#0x0    @ 080b6fec 201c
    .hword 0x4649    @ 080b6fee 4946
    adds r2,r3,#0x0    @ 080b6ff0 1a1c
    bl find_best_scored_slot_from_bitmap     @ 080b6ff2 fdf789fe
    adds r5,r0,#0x0    @ 080b6ff6 051c
    cmp r5,#0x0                              @ 080b6ff8 002d
    blt LAB_080b7000                         @ 080b6ffa 01db
    adds r0,r4,#0x0    @ 080b6ffc 201c
    b LAB_080b7038                           @ 080b6ffe 1be0
LAB_080b7000:
    adds r0,r6,#0x0    @ 080b7000 301c
    .hword 0x4649    @ 080b7002 4946
    movs r2,#0x1    @ 080b7004 0122
    movs r3,#0x1    @ 080b7006 0123
    bl find_best_scored_slot_from_bitmap     @ 080b7008 fdf77efe
    b LAB_080b6f8a                           @ 080b700c bde7
LAB_080b700e:
    ldr r2, DAT_080b701c                     @ 080b700e 034a
    adds r0,r6,#0x0    @ 080b7010 301c
    .hword 0x4649    @ 080b7012 4946
    bl find_best_slot_from_bitmap_by_comparator @ 080b7014 fdf7a8ff
    b LAB_080b6f8a                           @ 080b7018 b7e7
    .zero  0x2
DAT_080b701c:
    .word  0x080b5d29                     @ 080b701c 295d0b08
LAB_080b7020:
    movs r0,#0x1    @ 080b7020 0120
    subs r4,r0,r6    @ 080b7022 841b
    adds r0,r4,#0x0    @ 080b7024 201c
    .hword 0x4649    @ 080b7026 4946
    bl sample_random_slot_from_bitmap        @ 080b7028 fef76ef8
    adds r5,r0,#0x0    @ 080b702c 051c
    cmp r5,#0x0                              @ 080b702e 002d
    blt LAB_080b7044                         @ 080b7030 08db
    adds r0,r4,#0x0    @ 080b7032 201c
    b LAB_080b7038                           @ 080b7034 00e0
LAB_080b7036:
    adds r0,r6,#0x0    @ 080b7036 301c
LAB_080b7038:
    adds r1,r5,#0x0    @ 080b7038 291c
    movs r2,#0x0    @ 080b703a 0022
    movs r3,#0xb    @ 080b703c 0b23
    bl init_duel_zone_target_slot_refs       @ 080b703e dff7e9fe
    b LAB_080b705e                           @ 080b7042 0ce0
LAB_080b7044:
    adds r0,r6,#0x0    @ 080b7044 301c
    .hword 0x4649    @ 080b7046 4946
    bl sample_random_slot_from_bitmap        @ 080b7048 fef75ef8
    adds r5,r0,#0x0    @ 080b704c 051c
    cmp r5,#0x0                              @ 080b704e 002d
    blt LAB_080b705e                         @ 080b7050 05db
    adds r0,r6,#0x0    @ 080b7052 301c
    adds r1,r5,#0x0    @ 080b7054 291c
    movs r2,#0x0    @ 080b7056 0022
    movs r3,#0xb    @ 080b7058 0b23
    bl init_duel_zone_target_slot_refs       @ 080b705a dff7dbfe
LAB_080b705e:
    pop {r3,r4,r5}                           @ 080b705e 38bc
    .hword 0x4698    @ 080b7060 9846
    .hword 0x46a1    @ 080b7062 a146
    .hword 0x46aa    @ 080b7064 aa46
    pop {r4,r5,r6,r7}                        @ 080b7066 f0bc
    pop {r0}                                 @ 080b7068 01bc
    bx r0                                    @ 080b706a 0047

@ Enumerates all (player, slot) pairs over 2 players x 11 slots; calls predicate fn for each; sets bit 1<<(player*16+slot) in r6 if predicate returns nonzero; returns accumulated bitmap. r0=predicate_fn_ptr (-> r8 via .hword 0x4680=mov r8,r0). Each iteration: calls FUN_0810e5e8 (bx r8) with r0=player, r1=slot, r2=0. indeg=1, caller=FUN_080b70ac (card_ids, duel_field tags). Params: r0=predicate_fn ptr (fn(player_id, slot_idx, 0)->bool, stored in r8). Returns r0=u32 slot_bitmap (bit (player*16+slot) set if predicate true). Side effects: none (predicate may have read-only access). Constants: PLAYER_COUNT=2, SLOT_MAX=10, bit_pos=player*16+slot.
build_slot_bitmap_by_predicate:
    push {r4,r5,r6,r7,lr}                    @ 080b706c f0b5
    .hword 0x4647    @ 080b706e 4746
    push {r7}                                @ 080b7070 80b4
    .hword 0x4680    @ 080b7072 8046
    movs r6,#0x0    @ 080b7074 0026
    movs r5,#0x0    @ 080b7076 0025
LAB_080b7078:
    movs r4,#0x0    @ 080b7078 0024
    adds r7,r5,#0x1    @ 080b707a 6f1c
LAB_080b707c:
    adds r0,r5,#0x0    @ 080b707c 281c
    adds r1,r4,#0x0    @ 080b707e 211c
    movs r2,#0x0    @ 080b7080 0022
    bl invoke_r8                             @ 080b7082 57f0b1fa
    cmp r0,#0x0                              @ 080b7086 0028
    beq LAB_080b7094                         @ 080b7088 04d0
    lsls r1,r5,#0x4    @ 080b708a 2901
    adds r1,r1,r4    @ 080b708c 0919
    movs r0,#0x1    @ 080b708e 0120
    lsls r0,r1    @ 080b7090 8840
    orrs r6,r0    @ 080b7092 0643
LAB_080b7094:
    adds r4,#0x1    @ 080b7094 0134
    cmp r4,#0xa                              @ 080b7096 0a2c
    ble LAB_080b707c                         @ 080b7098 f0dd
    adds r5,r7,#0x0    @ 080b709a 3d1c
    cmp r5,#0x1                              @ 080b709c 012d
    ble LAB_080b7078                         @ 080b709e ebdd
    adds r0,r6,#0x0    @ 080b70a0 301c
    pop {r3}                                 @ 080b70a2 08bc
    .hword 0x4698    @ 080b70a4 9846
    pop {r4,r5,r6,r7}                        @ 080b70a6 f0bc
    pop {r1}                                 @ 080b70a8 02bc
    bx r1                                    @ 080b70aa 0847

@ Dispatches equip target slot selection logic by equip card_id (r1->r5). Writes player_id (r0->r7) to 0x0201afe0 and [gP1LifePoints+0x1d64]. Calls build_slot_bitmap_by_predicate(r2) -> candidate bitmap (r8). Multi-level cmp tree on r5 (card_id: 0x1578/0x12dc/0x139c/0x142a/0x1544/0x16df/0x1678/0x1888/0x1764 etc) dispatches to per-case handler calling eval_best_slot_score_by_lp_and_attr or select_equip_target_slot_by_eligible_set or select_equip_target_slot_full. indeg=26 (C_util_high), widely called by duel_field equip activation path. Params: r0=player_id [0..1] -> r7, r1=card_id [0..0x1fff] -> r5, r2=slot_predicate_fn ptr (passed to build_slot_bitmap_by_predicate). Returns r0=s32 best_slot_idx [0..10] or -1. Side effects: [0x0201afe0]:=r0 (player_id); [gP1LifePoints+0x1d64]:=r0. Constants: ACTIVE_ZONE_PLAYER_FIELD_OFFSET=0x1d64, gEquipPlayerState=0x0201afe0, card_id_dispatch_table=[0x1578,0x12dc,0x139c,0x142a,0x1544,0x16df,0x1678,0x1888,0x1764,...].
select_equip_target_slot_by_card_id:
    push {r4,r5,r6,r7,lr}                    @ 080b70ac f0b5
    .hword 0x4657    @ 080b70ae 5746
    .hword 0x464e    @ 080b70b0 4e46
    .hword 0x4645    @ 080b70b2 4546
    push {r5,r6,r7}                          @ 080b70b4 e0b4
    sub sp,#0x14                             @ 080b70b6 85b0
    adds r7,r0,#0x0    @ 080b70b8 071c
    adds r5,r1,#0x0    @ 080b70ba 0d1c
    str r2,[sp,#0x0]                         @ 080b70bc 0092
    ldr r0, DAT_080b70fc                     @ 080b70be 0f48
    str r7,[r0,#0x0]                         @ 080b70c0 0760
    ldr r4, PTR_gP1LifePoints_080b7100       @ 080b70c2 0f4c
    ldr r1, DAT_080b7104                     @ 080b70c4 0f49
    adds r0,r4,r1    @ 080b70c6 6018
    str r7,[r0,#0x0]                         @ 080b70c8 0760
    adds r0,r2,#0x0    @ 080b70ca 101c
    bl build_slot_bitmap_by_predicate        @ 080b70cc fff7ceff
    .hword 0x4680    @ 080b70d0 8046
    ldr r0, DAT_080b7108                     @ 080b70d2 0d48
    adds r6,r4,#0x0    @ 080b70d4 261c
    cmp r5,r0                                @ 080b70d6 8542
    bne LAB_080b70dc                         @ 080b70d8 00d1
    b LAB_080b7294                           @ 080b70da dbe0
LAB_080b70dc:
    cmp r5,r0                                @ 080b70dc 8542
    bgt LAB_080b7148                         @ 080b70de 33dc
    ldr r0, DAT_080b710c                     @ 080b70e0 0a48
    cmp r5,r0                                @ 080b70e2 8542
    bne LAB_080b70e8                         @ 080b70e4 00d1
    b LAB_080b7294                           @ 080b70e6 d5e0
LAB_080b70e8:
    cmp r5,r0                                @ 080b70e8 8542
    bgt LAB_080b7116                         @ 080b70ea 14dc
    cmp r5,#0x2                              @ 080b70ec 022d
    bne LAB_080b70f2                         @ 080b70ee 00d1
    b LAB_080b71e4                           @ 080b70f0 78e0
LAB_080b70f2:
    cmp r5,#0x2                              @ 080b70f2 022d
    bgt LAB_080b7110                         @ 080b70f4 0cdc
    cmp r5,#0x1                              @ 080b70f6 012d
    beq LAB_080b71b4                         @ 080b70f8 5cd0
    b LAB_080b734c                           @ 080b70fa 27e1
DAT_080b70fc:
    .word  0x0201afe0                     @ 080b70fc e0af0102
PTR_gP1LifePoints_080b7100:
    .word  gP1LifePoints                  @ 080b7100 e0c40102
DAT_080b7104:
    .word  0x00001d64                     @ 080b7104 641d0000
DAT_080b7108:
    .word  0x00001578                     @ 080b7108 78150000
DAT_080b710c:
    .word  0x000012dc                     @ 080b710c dc120000
LAB_080b7110:
    cmp r5,#0x3                              @ 080b7110 032d
    beq LAB_080b7200                         @ 080b7112 75d0
    b LAB_080b734c                           @ 080b7114 1ae1
LAB_080b7116:
    ldr r0, DAT_080b7128                     @ 080b7116 0448
    cmp r5,r0                                @ 080b7118 8542
    bne LAB_080b711e                         @ 080b711a 00d1
    b LAB_080b721c                           @ 080b711c 7ee0
LAB_080b711e:
    cmp r5,r0                                @ 080b711e 8542
    bgt LAB_080b712c                         @ 080b7120 04dc
    subs r0,#0x71    @ 080b7122 7138
    b LAB_080b7172                           @ 080b7124 25e0
    .zero  0x2
DAT_080b7128:
    .word  0x0000139c                     @ 080b7128 9c130000
LAB_080b712c:
    ldr r0, DAT_080b7140                     @ 080b712c 0448
    cmp r5,r0                                @ 080b712e 8542
    bne LAB_080b7134                         @ 080b7130 00d1
    b LAB_080b7266                           @ 080b7132 98e0
LAB_080b7134:
    ldr r0, DAT_080b7144                     @ 080b7134 0348
    cmp r5,r0                                @ 080b7136 8542
    bne LAB_080b713c                         @ 080b7138 00d1
    b LAB_080b7238                           @ 080b713a 7de0
LAB_080b713c:
    b LAB_080b734c                           @ 080b713c 06e1
    .zero  0x2
DAT_080b7140:
    .word  0x0000142a                     @ 080b7140 2a140000
DAT_080b7144:
    .word  0x00001544                     @ 080b7144 44150000
LAB_080b7148:
    ldr r0, DAT_080b7164                     @ 080b7148 0648
    cmp r5,r0                                @ 080b714a 8542
    bne LAB_080b7150                         @ 080b714c 00d1
    b LAB_080b7294                           @ 080b714e a1e0
LAB_080b7150:
    cmp r5,r0                                @ 080b7150 8542
    bgt LAB_080b717c                         @ 080b7152 13dc
    subs r0,#0xec    @ 080b7154 ec38
    cmp r5,r0                                @ 080b7156 8542
    beq LAB_080b7238                         @ 080b7158 6ed0
    cmp r5,r0                                @ 080b715a 8542
    bgt LAB_080b7168                         @ 080b715c 04dc
    subs r0,#0x17    @ 080b715e 1738
    b LAB_080b7172                           @ 080b7160 07e0
    .zero  0x2
DAT_080b7164:
    .word  0x000016df                     @ 080b7164 df160000
LAB_080b7168:
    ldr r0, DAT_080b7178                     @ 080b7168 0348
    cmp r5,r0                                @ 080b716a 8542
    bne LAB_080b7170                         @ 080b716c 00d1
    b LAB_080b72c2                           @ 080b716e a8e0
LAB_080b7170:
    adds r0,#0x5b    @ 080b7170 5b30
LAB_080b7172:
    cmp r5,r0                                @ 080b7172 8542
    beq LAB_080b71e4                         @ 080b7174 36d0
    b LAB_080b734c                           @ 080b7176 e9e0
DAT_080b7178:
    .word  0x00001678                     @ 080b7178 78160000
LAB_080b717c:
    ldr r0, DAT_080b7190                     @ 080b717c 0448
    cmp r5,r0                                @ 080b717e 8542
    beq LAB_080b71e4                         @ 080b7180 30d0
    cmp r5,r0                                @ 080b7182 8542
    bgt LAB_080b7198                         @ 080b7184 08dc
    ldr r0, DAT_080b7194                     @ 080b7186 0348
    cmp r5,r0                                @ 080b7188 8542
    bne LAB_080b718e                         @ 080b718a 00d1
    b LAB_080b7294                           @ 080b718c 82e0
LAB_080b718e:
    b LAB_080b734c                           @ 080b718e dde0
DAT_080b7190:
    .word  0x00001888                     @ 080b7190 88180000
DAT_080b7194:
    .word  0x00001764                     @ 080b7194 64170000
LAB_080b7198:
    ldr r0, DAT_080b71ac                     @ 080b7198 0448
    cmp r5,r0                                @ 080b719a 8542
    bne LAB_080b71a0                         @ 080b719c 00d1
    b LAB_080b72c2                           @ 080b719e 90e0
LAB_080b71a0:
    ldr r0, DAT_080b71b0                     @ 080b71a0 0348
    cmp r5,r0                                @ 080b71a2 8542
    bne LAB_080b71a8                         @ 080b71a4 00d1
    b LAB_080b72dc                           @ 080b71a6 99e0
LAB_080b71a8:
    b LAB_080b734c                           @ 080b71a8 d0e0
    .zero  0x2
DAT_080b71ac:
    .word  0x00001889                     @ 080b71ac 89180000
DAT_080b71b0:
    .word  0x0000198d                     @ 080b71b0 8d190000
LAB_080b71b4:
    subs r4,r5,r7    @ 080b71b4 ec1b
    adds r0,r4,#0x0    @ 080b71b6 201c
    .hword 0x4641    @ 080b71b8 4146
    movs r2,#0x0    @ 080b71ba 0022
    bl select_equip_target_slot_with_eligibility_check @ 080b71bc fef7c4f8
    adds r1,r0,#0x0    @ 080b71c0 011c
    cmp r1,#0x0                              @ 080b71c2 0029
    blt LAB_080b71cc                         @ 080b71c4 02db
    adds r0,r4,#0x0    @ 080b71c6 201c
    movs r2,#0x0    @ 080b71c8 0022
    b LAB_080b73da                           @ 080b71ca 06e1
LAB_080b71cc:
    adds r0,r7,#0x0    @ 080b71cc 381c
    .hword 0x4641    @ 080b71ce 4146
    movs r2,#0x0    @ 080b71d0 0022
    bl select_equip_target_slot_full         @ 080b71d2 fef7ebf9
    adds r1,r0,#0x0    @ 080b71d6 011c
    cmp r1,#0x0                              @ 080b71d8 0029
    bge LAB_080b71de                         @ 080b71da 00da
    b LAB_080b734c                           @ 080b71dc b6e0
LAB_080b71de:
    adds r0,r7,#0x0    @ 080b71de 381c
    movs r2,#0x0    @ 080b71e0 0022
    b LAB_080b73da                           @ 080b71e2 fae0
LAB_080b71e4:
    adds r0,r7,#0x0    @ 080b71e4 381c
    ldr r1,[sp,#0x0]                         @ 080b71e6 0099
    movs r2,#0x1    @ 080b71e8 0122
    movs r3,#0x0    @ 080b71ea 0023
    bl scan_hand_for_best_equip_target_slot  @ 080b71ec fef77cfb
    adds r4,r0,#0x0    @ 080b71f0 041c
    cmp r4,#0x0                              @ 080b71f2 002c
    bge LAB_080b71f8                         @ 080b71f4 00da
    b LAB_080b734c                           @ 080b71f6 a9e0
LAB_080b71f8:
    adds r0,r7,#0x0    @ 080b71f8 381c
    movs r1,#0xb    @ 080b71fa 0b21
    adds r2,r4,#0x0    @ 080b71fc 221c
    b LAB_080b73da                           @ 080b71fe ece0
LAB_080b7200:
    adds r0,r7,#0x0    @ 080b7200 381c
    ldr r1,[sp,#0x0]                         @ 080b7202 0099
    movs r2,#0x0    @ 080b7204 0022
    movs r3,#0x0    @ 080b7206 0023
    bl scan_hand_for_best_equip_target_slot  @ 080b7208 fef76efb
    adds r4,r0,#0x0    @ 080b720c 041c
    cmp r4,#0x0                              @ 080b720e 002c
    bge LAB_080b7214                         @ 080b7210 00da
    b LAB_080b734c                           @ 080b7212 9be0
LAB_080b7214:
    adds r0,r7,#0x0    @ 080b7214 381c
    movs r1,#0xb    @ 080b7216 0b21
    adds r2,r4,#0x0    @ 080b7218 221c
    b LAB_080b73da                           @ 080b721a dee0
LAB_080b721c:
    ldr r2, DAT_080b7234                     @ 080b721c 054a
    adds r0,r7,#0x0    @ 080b721e 381c
    .hword 0x4641    @ 080b7220 4146
    bl find_best_slot_from_bitmap_by_comparator @ 080b7222 fdf7a1fe
    adds r1,r0,#0x0    @ 080b7226 011c
    cmp r1,#0x0                              @ 080b7228 0029
    bge LAB_080b722e                         @ 080b722a 00da
    b LAB_080b734c                           @ 080b722c 8ee0
LAB_080b722e:
    adds r0,r7,#0x0    @ 080b722e 381c
    movs r2,#0x0    @ 080b7230 0022
    b LAB_080b73da                           @ 080b7232 d2e0
DAT_080b7234:
    .word  0x080b5c71                     @ 080b7234 715c0b08
LAB_080b7238:
    movs r0,#0x1    @ 080b7238 0120
    subs r4,r0,r7    @ 080b723a c41b
    adds r0,r4,#0x0    @ 080b723c 201c
    .hword 0x4641    @ 080b723e 4146
    movs r2,#0x1    @ 080b7240 0122
    bl select_equip_target_slot_with_eligibility_check @ 080b7242 fef781f8
    adds r1,r0,#0x0    @ 080b7246 011c
    cmp r1,#0x0                              @ 080b7248 0029
    blt LAB_080b7252                         @ 080b724a 02db
    adds r0,r4,#0x0    @ 080b724c 201c
    movs r2,#0x0    @ 080b724e 0022
    b LAB_080b73da                           @ 080b7250 c3e0
LAB_080b7252:
    adds r0,r7,#0x0    @ 080b7252 381c
    .hword 0x4641    @ 080b7254 4146
    bl select_equip_target_slot_by_eligible_set @ 080b7256 fef733f9
    adds r1,r0,#0x0    @ 080b725a 011c
    cmp r1,#0x0                              @ 080b725c 0029
    blt LAB_080b734c                         @ 080b725e 75db
    adds r0,r7,#0x0    @ 080b7260 381c
    movs r2,#0x0    @ 080b7262 0022
    b LAB_080b73da                           @ 080b7264 b9e0
LAB_080b7266:
    ldr r2, DAT_080b727c                     @ 080b7266 054a
    adds r0,r7,#0x0    @ 080b7268 381c
    .hword 0x4641    @ 080b726a 4146
    bl find_best_slot_from_bitmap_by_comparator @ 080b726c fdf77cfe
    adds r1,r0,#0x0    @ 080b7270 011c
    cmp r1,#0x0                              @ 080b7272 0029
    blt LAB_080b7280                         @ 080b7274 04db
    adds r0,r7,#0x0    @ 080b7276 381c
    movs r2,#0x0    @ 080b7278 0022
    b LAB_080b73da                           @ 080b727a aee0
DAT_080b727c:
    .word  0x080b5b51                     @ 080b727c 515b0b08
LAB_080b7280:
    adds r0,r7,#0x0    @ 080b7280 381c
    .hword 0x4641    @ 080b7282 4146
    bl select_equip_target_slot_by_eligible_set @ 080b7284 fef71cf9
    adds r1,r0,#0x0    @ 080b7288 011c
    cmp r1,#0x0                              @ 080b728a 0029
    blt LAB_080b734c                         @ 080b728c 5edb
    adds r0,r7,#0x0    @ 080b728e 381c
    movs r2,#0x0    @ 080b7290 0022
    b LAB_080b73da                           @ 080b7292 a2e0
LAB_080b7294:
    movs r0,#0x1    @ 080b7294 0120
    subs r4,r0,r7    @ 080b7296 c41b
    adds r0,r4,#0x0    @ 080b7298 201c
    .hword 0x4641    @ 080b729a 4146
    movs r2,#0x0    @ 080b729c 0022
    bl select_equip_target_slot_with_eligibility_check @ 080b729e fef753f8
    adds r1,r0,#0x0    @ 080b72a2 011c
    cmp r1,#0x0                              @ 080b72a4 0029
    blt LAB_080b72ae                         @ 080b72a6 02db
    adds r0,r4,#0x0    @ 080b72a8 201c
    movs r2,#0x0    @ 080b72aa 0022
    b LAB_080b73da                           @ 080b72ac 95e0
LAB_080b72ae:
    adds r0,r7,#0x0    @ 080b72ae 381c
    .hword 0x4641    @ 080b72b0 4146
    bl select_equip_target_slot_by_eligible_set @ 080b72b2 fef705f9
    adds r1,r0,#0x0    @ 080b72b6 011c
    cmp r1,#0x0                              @ 080b72b8 0029
    blt LAB_080b734c                         @ 080b72ba 47db
    adds r0,r7,#0x0    @ 080b72bc 381c
    movs r2,#0x0    @ 080b72be 0022
    b LAB_080b73da                           @ 080b72c0 8be0
LAB_080b72c2:
    adds r0,r7,#0x0    @ 080b72c2 381c
    ldr r1,[sp,#0x0]                         @ 080b72c4 0099
    movs r2,#0x1    @ 080b72c6 0122
    movs r3,#0x1    @ 080b72c8 0123
    bl eval_best_slot_score_by_lp_and_attr   @ 080b72ca fdf785fe
    adds r4,r0,#0x0    @ 080b72ce 041c
    cmp r4,#0x0                              @ 080b72d0 002c
    blt LAB_080b734c                         @ 080b72d2 3bdb
    adds r0,r7,#0x0    @ 080b72d4 381c
    movs r1,#0xb    @ 080b72d6 0b21
    adds r2,r4,#0x0    @ 080b72d8 221c
    b LAB_080b73da                           @ 080b72da 7ee0
LAB_080b72dc:
    movs r4,#0x0    @ 080b72dc 0024
    movs r1,#0x1    @ 080b72de 0121
    ands r1,r7    @ 080b72e0 3940
    ldr r2, DAT_080b7344                     @ 080b72e2 184a
    adds r0,r1,#0x0    @ 080b72e4 081c
    muls r0,r2    @ 080b72e6 5043
    adds r3,r6,#0x0    @ 080b72e8 331c
    adds r3,#0xc    @ 080b72ea 0c33
    adds r0,r0,r3    @ 080b72ec c018
    ldr r0,[r0,#0x0]                         @ 080b72ee 0068
    cmp r4,r0                                @ 080b72f0 8442
    bcs LAB_080b733e                         @ 080b72f2 24d2
    adds r6,r1,#0x0    @ 080b72f4 0e1c
    .hword 0x4698    @ 080b72f6 9846
LAB_080b72f8:
    lsls r1,r4,#0x2    @ 080b72f8 a100
    adds r0,r6,#0x0    @ 080b72fa 301c
    muls r0,r2    @ 080b72fc 5043
    adds r1,r1,r0    @ 080b72fe 0918
    ldr r0, DAT_080b7348                     @ 080b7300 1148
    adds r1,r1,r0    @ 080b7302 0918
    ldr r0,[r1,#0x0]                         @ 080b7304 0868
    lsls r0,r0,#0x13    @ 080b7306 c004
    lsrs r5,r0,#0x13    @ 080b7308 c50c
    adds r2,r5,#0x0    @ 080b730a 2a1c
    adds r0,r7,#0x0    @ 080b730c 381c
    movs r1,#0x1    @ 080b730e 0121
    bl check_card_effect_activation_eligible_by_id @ 080b7310 f5f78efc
    cmp r0,#0x0                              @ 080b7314 0028
    bne LAB_080b732e                         @ 080b7316 0ad1
    adds r0,r5,#0x0    @ 080b7318 281c
    bl get_card_type_bits_by_internal_id     @ 080b731a 37f03ffe
    cmp r0,#0x2                              @ 080b731e 0228
    ble LAB_080b732e                         @ 080b7320 05dd
    adds r0,r5,#0x0    @ 080b7322 281c
    movs r1,#0x0    @ 080b7324 0021
    bl check_card_id_in_eligible_set         @ 080b7326 f8f705f9
    cmp r0,#0x0                              @ 080b732a 0028
    beq LAB_080b73cc                         @ 080b732c 4ed0
LAB_080b732e:
    adds r4,#0x1    @ 080b732e 0134
    ldr r2, DAT_080b7344                     @ 080b7330 044a
    adds r0,r6,#0x0    @ 080b7332 301c
    muls r0,r2    @ 080b7334 5043
    add r0,r8                                @ 080b7336 4044
    ldr r0,[r0,#0x0]                         @ 080b7338 0068
    cmp r4,r0                                @ 080b733a 8442
    bcc LAB_080b72f8                         @ 080b733c dcd3
LAB_080b733e:
    bl zero_duel_lp_display_counters         @ 080b733e dff7c5fd
    b LAB_080b73fa                           @ 080b7342 5ae0
DAT_080b7344:
    .word  0x00000868                     @ 080b7344 68080000
DAT_080b7348:
    .word  0x0201c600                     @ 080b7348 00c60102
LAB_080b734c:
    movs r3,#0x0    @ 080b734c 0023
    ldr r6, PTR_gP1LifePoints_080b73c4       @ 080b734e 1d4e
    movs r0,#0x1    @ 080b7350 0120
    .hword 0x4682    @ 080b7352 8246
    adds r0,r7,#0x0    @ 080b7354 381c
    .hword 0x4651    @ 080b7356 5146
    ands r0,r1    @ 080b7358 0840
    ldr r1, DAT_080b73c8                     @ 080b735a 1b49
    muls r1,r0    @ 080b735c 4143
    adds r6,#0xc    @ 080b735e 0c36
    .hword 0x46b1    @ 080b7360 b146
    add r1,r9                                @ 080b7362 4944
    str r1,[sp,#0x8]                         @ 080b7364 0291
    str r0,[sp,#0x4]                         @ 080b7366 0190
LAB_080b7368:
    adds r4,r7,#0x0    @ 080b7368 3c1c
    cmp r3,#0x0                              @ 080b736a 002b
    bne LAB_080b7372                         @ 080b736c 01d1
    .hword 0x4656    @ 080b736e 5646
    eors r4,r6    @ 080b7370 7440
LAB_080b7372:
    movs r5,#0x0    @ 080b7372 0025
    ldr r1,[sp,#0x8]                         @ 080b7374 0299
    ldr r0,[r1,#0x0]                         @ 080b7376 0868
    cmp r5,r0                                @ 080b7378 8542
    bcs LAB_080b73a4                         @ 080b737a 13d2
    ldr r0, DAT_080b73c8                     @ 080b737c 1248
    ldr r6,[sp,#0x4]                         @ 080b737e 019e
    muls r0,r6    @ 080b7380 7043
    add r0,r9                                @ 080b7382 4844
    str r0,[sp,#0x10]                        @ 080b7384 0490
LAB_080b7386:
    adds r0,r4,#0x0    @ 080b7386 201c
    movs r1,#0xb    @ 080b7388 0b21
    adds r2,r5,#0x0    @ 080b738a 2a1c
    str r3,[sp,#0xc]                         @ 080b738c 0393
    ldr r6,[sp,#0x0]                         @ 080b738e 009e
    bl invoke_r6                             @ 080b7390 57f026f9
    ldr r3,[sp,#0xc]                         @ 080b7394 039b
    cmp r0,#0x0                              @ 080b7396 0028
    bne LAB_080b73d4                         @ 080b7398 1cd1
    adds r5,#0x1    @ 080b739a 0135
    ldr r1,[sp,#0x10]                        @ 080b739c 0499
    ldr r0,[r1,#0x0]                         @ 080b739e 0868
    cmp r5,r0                                @ 080b73a0 8542
    bcc LAB_080b7386                         @ 080b73a2 f0d3
LAB_080b73a4:
    adds r3,#0x1    @ 080b73a4 0133
    cmp r3,#0x1                              @ 080b73a6 012b
    ble LAB_080b7368                         @ 080b73a8 dedd
    movs r0,#0x1    @ 080b73aa 0120
    subs r4,r0,r7    @ 080b73ac c41b
    adds r0,r4,#0x0    @ 080b73ae 201c
    .hword 0x4641    @ 080b73b0 4146
    bl sample_random_slot_from_bitmap        @ 080b73b2 fdf7a9fe
    adds r1,r0,#0x0    @ 080b73b6 011c
    cmp r1,#0x0                              @ 080b73b8 0029
    blt LAB_080b73e2                         @ 080b73ba 12db
    adds r0,r4,#0x0    @ 080b73bc 201c
    movs r2,#0x0    @ 080b73be 0022
    b LAB_080b73da                           @ 080b73c0 0be0
    .zero  0x2
PTR_gP1LifePoints_080b73c4:
    .word  gP1LifePoints                  @ 080b73c4 e0c40102
DAT_080b73c8:
    .word  0x00000868                     @ 080b73c8 68080000
LAB_080b73cc:
    adds r0,r7,#0x0    @ 080b73cc 381c
    movs r1,#0xb    @ 080b73ce 0b21
    adds r2,r4,#0x0    @ 080b73d0 221c
    b LAB_080b73da                           @ 080b73d2 02e0
LAB_080b73d4:
    adds r0,r4,#0x0    @ 080b73d4 201c
    movs r1,#0xb    @ 080b73d6 0b21
    adds r2,r5,#0x0    @ 080b73d8 2a1c
LAB_080b73da:
    movs r3,#0xb    @ 080b73da 0b23
    bl init_duel_zone_target_slot_refs       @ 080b73dc dff71afd
    b LAB_080b73fa                           @ 080b73e0 0be0
LAB_080b73e2:
    adds r0,r7,#0x0    @ 080b73e2 381c
    .hword 0x4641    @ 080b73e4 4146
    bl sample_random_slot_from_bitmap        @ 080b73e6 fdf78ffe
    adds r1,r0,#0x0    @ 080b73ea 011c
    cmp r1,#0x0                              @ 080b73ec 0029
    blt LAB_080b73fa                         @ 080b73ee 04db
    adds r0,r7,#0x0    @ 080b73f0 381c
    movs r2,#0x0    @ 080b73f2 0022
    movs r3,#0xb    @ 080b73f4 0b23
    bl init_duel_zone_target_slot_refs       @ 080b73f6 dff70dfd
LAB_080b73fa:
    add sp,#0x14                             @ 080b73fa 05b0
    pop {r3,r4,r5}                           @ 080b73fc 38bc
    .hword 0x4698    @ 080b73fe 9846
    .hword 0x46a1    @ 080b7400 a146
    .hword 0x46aa    @ 080b7402 aa46
    pop {r4,r5,r6,r7}                        @ 080b7404 f0bc
    pop {r0}                                 @ 080b7406 01bc
    bx r0                                    @ 080b7408 0047
    .zero  0x2

@ Scans player hand and field card lists for equip-activatable cards, initializing target slot refs.
@ Called by FUN_080x08069e40 in switch case 0x7f (equip activation trigger path), r0=player_side.
@ First writes player_id to [0x0201afe0] (duel active player marker).
@ Three scan rounds:
@ (1) Iterates gDuelFieldSlots2 (0x0201c600, extra card list) matching special IDs:
@     0x13b5=Moisture Creature, 0x154b=Gilford the Lightning, 0x1905=Dark Dreadroute and adjacent IDs.
@     On match: eval_card_placement_flags_default for placement bit,
@     eval_card_activation_score_with_lp_threshold for score,
@     then init_duel_zone_target_slot_refs(player, 0xb, slot, mode=4 or 6).
@ (2) Iterates main card list (gP1LifePoints+0xc = hand count); checks summon restriction
@     and placement flags; init_duel_zone_target_slot_refs for eligible hand cards.
@ (3) Extends to second player view with similar checks.
@ Returns void (pop {r0}; bx r0 -> r0 overwritten with saved LR).
@ 
@ Constants:
@ - gDuelActivePlayer=0x0201afe0 (DAT_080b7470)
@ - gP1LifePoints=0x0201c4e0 (PTR_gP1LifePoints_080b7474)
@ - gDuelFieldSlots2=0x0201c600
@ - player_stride=0x868
@ - CARD_Moisture_Creature=0x13b5
@ - CARD_Gilford_the_Lightning=0x154b
@ - CARD_Dark_Dreadroute=0x1905
@ - TARGET_MODE_A=4, TARGET_MODE_B=6
@ - ZONE_TYPE=0xb
scan_hand_and_field_cards_for_equip_activation:
    push {r4,r5,r6,r7,lr}                    @ 080b740c f0b5
    .hword 0x4657    @ 080b740e 5746
    .hword 0x464e    @ 080b7410 4e46
    .hword 0x4645    @ 080b7412 4546
    push {r5,r6,r7}                          @ 080b7414 e0b4
    sub sp,#0x4                              @ 080b7416 81b0
    adds r6,r0,#0x0    @ 080b7418 061c
    ldr r0, DAT_080b7470                     @ 080b741a 1548
    str r6,[r0,#0x0]                         @ 080b741c 0660
    movs r7,#0x0    @ 080b741e 0027
    ldr r1, PTR_gP1LifePoints_080b7474       @ 080b7420 1449
    movs r2,#0x1    @ 080b7422 0122
    ands r2,r6    @ 080b7424 3240
    ldr r3, DAT_080b7478                     @ 080b7426 144b
    adds r0,r2,#0x0    @ 080b7428 101c
    muls r0,r3    @ 080b742a 5843
    adds r4,r1,#0x0    @ 080b742c 0c1c
    adds r4,#0xc    @ 080b742e 0c34
    adds r0,r0,r4    @ 080b7430 0019
    ldr r0,[r0,#0x0]                         @ 080b7432 0068
    cmp r7,r0                                @ 080b7434 8742
    bcs LAB_080b7502                         @ 080b7436 64d2
    .hword 0x4690    @ 080b7438 9046
    adds r0,r1,#0x0    @ 080b743a 081c
    movs r1,#0x90    @ 080b743c 9021
    lsls r1,r1,#0x1    @ 080b743e 4900
    adds r0,r0,r1    @ 080b7440 4018
    .hword 0x4682    @ 080b7442 8246
    movs r2,#0x0    @ 080b7444 0022
    .hword 0x46a1    @ 080b7446 a146
LAB_080b7448:
    .hword 0x4640    @ 080b7448 4046
    muls r0,r3    @ 080b744a 5843
    adds r0,r2,r0    @ 080b744c 1018
    ldr r1, DAT_080b747c                     @ 080b744e 0b49
    adds r0,r0,r1    @ 080b7450 4018
    ldr r0,[r0,#0x0]                         @ 080b7452 0068
    lsls r0,r0,#0x13    @ 080b7454 c004
    lsrs r4,r0,#0x13    @ 080b7456 c40c
    ldr r0, DAT_080b7480                     @ 080b7458 0948
    cmp r4,r0                                @ 080b745a 8442
    beq LAB_080b7490                         @ 080b745c 18d0
    cmp r4,r0                                @ 080b745e 8442
    bgt LAB_080b7484                         @ 080b7460 10dc
    subs r0,#0x2d    @ 080b7462 2d38
    cmp r4,r0                                @ 080b7464 8442
    bgt LAB_080b74f0                         @ 080b7466 43dc
    subs r0,#0x2    @ 080b7468 0238
    cmp r4,r0                                @ 080b746a 8442
    blt LAB_080b74f0                         @ 080b746c 40db
    b LAB_080b7490                           @ 080b746e 0fe0
DAT_080b7470:
    .word  0x0201afe0                     @ 080b7470 e0af0102
PTR_gP1LifePoints_080b7474:
    .word  gP1LifePoints                  @ 080b7474 e0c40102
DAT_080b7478:
    .word  0x00000868                     @ 080b7478 68080000
DAT_080b747c:
    .word  0x0201c600                     @ 080b747c 00c60102
DAT_080b7480:
    .word  0x000013b5                     @ 080b7480 b5130000
LAB_080b7484:
    ldr r0, DAT_080b74e4                     @ 080b7484 1748
    cmp r4,r0                                @ 080b7486 8442
    beq LAB_080b7490                         @ 080b7488 02d0
    ldr r0, DAT_080b74e8                     @ 080b748a 1748
    cmp r4,r0                                @ 080b748c 8442
    bne LAB_080b74f0                         @ 080b748e 2fd1
LAB_080b7490:
    ldr r0, DAT_080b74ec                     @ 080b7490 1648
    .hword 0x4641    @ 080b7492 4146
    muls r1,r0    @ 080b7494 4143
    adds r0,r1,#0x0    @ 080b7496 081c
    adds r0,r2,r0    @ 080b7498 1018
    add r0,r10                               @ 080b749a 5044
    ldr r0,[r0,#0x0]                         @ 080b749c 0068
    lsls r1,r0,#0x2    @ 080b749e 8100
    lsrs r1,r1,#0x18    @ 080b74a0 090e
    lsls r1,r1,#0x1    @ 080b74a2 4900
    lsls r0,r0,#0x12    @ 080b74a4 8004
    lsrs r0,r0,#0x1f    @ 080b74a6 c00f
    adds r1,r1,r0    @ 080b74a8 0918
    adds r0,r6,#0x0    @ 080b74aa 301c
    str r2,[sp,#0x0]                         @ 080b74ac 0092
    bl eval_card_placement_flags_default     @ 080b74ae edf7f1f8
    adds r5,r0,#0x0    @ 080b74b2 051c
    ldr r2,[sp,#0x0]                         @ 080b74b4 009a
    cmp r5,#0x0                              @ 080b74b6 002d
    beq LAB_080b74f0                         @ 080b74b8 1ad0
    adds r0,r6,#0x0    @ 080b74ba 301c
    adds r1,r4,#0x0    @ 080b74bc 211c
    movs r2,#0x0    @ 080b74be 0022
    movs r3,#0x0    @ 080b74c0 0023
    bl eval_card_activation_score_with_lp_threshold @ 080b74c2 f5f73df8
    adds r1,r0,#0x0    @ 080b74c6 011c
    cmp r1,#0x0                              @ 080b74c8 0029
    beq LAB_080b74dc                         @ 080b74ca 07d0
    movs r0,#0x40    @ 080b74cc 4020
    ands r0,r5    @ 080b74ce 2840
    cmp r0,#0x0                              @ 080b74d0 0028
    bne LAB_080b74d6                         @ 080b74d2 00d1
    movs r1,#0x0    @ 080b74d4 0021
LAB_080b74d6:
    cmp r1,#0x0                              @ 080b74d6 0029
    beq LAB_080b74dc                         @ 080b74d8 00d0
    b LAB_080b765e                           @ 080b74da c0e0
LAB_080b74dc:
    movs r0,#0x10    @ 080b74dc 1020
    ands r0,r5    @ 080b74de 2840
    b LAB_080b7658                           @ 080b74e0 bae0
    .zero  0x2
DAT_080b74e4:
    .word  0x0000154b                     @ 080b74e4 4b150000
DAT_080b74e8:
    .word  0x00001905                     @ 080b74e8 05190000
DAT_080b74ec:
    .word  0x00000868                     @ 080b74ec 68080000
LAB_080b74f0:
    adds r2,#0x4    @ 080b74f0 0432
    adds r7,#0x1    @ 080b74f2 0137
    ldr r3, DAT_080b7564                     @ 080b74f4 1b4b
    .hword 0x4640    @ 080b74f6 4046
    muls r0,r3    @ 080b74f8 5843
    add r0,r9                                @ 080b74fa 4844
    ldr r0,[r0,#0x0]                         @ 080b74fc 0068
    cmp r7,r0                                @ 080b74fe 8742
    bcc LAB_080b7448                         @ 080b7500 a2d3
LAB_080b7502:
    movs r7,#0x0    @ 080b7502 0027
    movs r1,#0x1    @ 080b7504 0121
    ands r1,r6    @ 080b7506 3140
    ldr r2, DAT_080b7564                     @ 080b7508 164a
    adds r0,r1,#0x0    @ 080b750a 081c
    muls r0,r2    @ 080b750c 5043
    ldr r3, PTR_gP1LifePoints_080b7568       @ 080b750e 164b
    adds r3,#0xc    @ 080b7510 0c33
    adds r0,r0,r3    @ 080b7512 c018
    ldr r0,[r0,#0x0]                         @ 080b7514 0068
    cmp r7,r0                                @ 080b7516 8742
    bcs LAB_080b7580                         @ 080b7518 32d2
    adds r5,r1,#0x0    @ 080b751a 0d1c
    .hword 0x4698    @ 080b751c 9846
LAB_080b751e:
    lsls r1,r7,#0x2    @ 080b751e b900
    adds r0,r5,#0x0    @ 080b7520 281c
    muls r0,r2    @ 080b7522 5043
    adds r1,r1,r0    @ 080b7524 0918
    ldr r0, DAT_080b756c                     @ 080b7526 1148
    adds r4,r1,r0    @ 080b7528 0c18
    ldr r0,[r4,#0x0]                         @ 080b752a 2068
    lsls r0,r0,#0x13    @ 080b752c c004
    lsrs r0,r0,#0x13    @ 080b752e c00c
    bl get_card_field_summon_restriction     @ 080b7530 93f7e0ff
    cmp r0,#0x0                              @ 080b7534 0028
    beq LAB_080b7570                         @ 080b7536 1bd0
    ldr r0,[r4,#0x0]                         @ 080b7538 2068
    lsls r1,r0,#0x2    @ 080b753a 8100
    lsrs r1,r1,#0x18    @ 080b753c 090e
    lsls r1,r1,#0x1    @ 080b753e 4900
    lsls r0,r0,#0x12    @ 080b7540 8004
    lsrs r0,r0,#0x1f    @ 080b7542 c00f
    adds r1,r1,r0    @ 080b7544 0918
    adds r0,r6,#0x0    @ 080b7546 301c
    bl eval_card_placement_flags_default     @ 080b7548 edf7a4f8
    movs r1,#0x40    @ 080b754c 4021
    ands r1,r0    @ 080b754e 0140
    cmp r1,#0x0                              @ 080b7550 0029
    beq LAB_080b7570                         @ 080b7552 0dd0
    adds r0,r6,#0x0    @ 080b7554 301c
    movs r1,#0xb    @ 080b7556 0b21
    adds r2,r7,#0x0    @ 080b7558 3a1c
    movs r3,#0x6    @ 080b755a 0623
    bl init_duel_zone_target_slot_refs       @ 080b755c dff75afc
    b LAB_080b7690                           @ 080b7560 96e0
    .zero  0x2
DAT_080b7564:
    .word  0x00000868                     @ 080b7564 68080000
PTR_gP1LifePoints_080b7568:
    .word  gP1LifePoints                  @ 080b7568 e0c40102
DAT_080b756c:
    .word  0x0201c600                     @ 080b756c 00c60102
LAB_080b7570:
    adds r7,#0x1    @ 080b7570 0137
    ldr r2, DAT_080b7674                     @ 080b7572 404a
    adds r0,r5,#0x0    @ 080b7574 281c
    muls r0,r2    @ 080b7576 5043
    add r0,r8                                @ 080b7578 4044
    ldr r0,[r0,#0x0]                         @ 080b757a 0068
    cmp r7,r0                                @ 080b757c 8742
    bcc LAB_080b751e                         @ 080b757e ced3
LAB_080b7580:
    movs r7,#0x0    @ 080b7580 0027
    movs r1,#0x1    @ 080b7582 0121
    ands r1,r6    @ 080b7584 3140
    ldr r2, DAT_080b7674                     @ 080b7586 3b4a
    adds r0,r1,#0x0    @ 080b7588 081c
    muls r0,r2    @ 080b758a 5043
    ldr r3, PTR_gP1LifePoints_080b7678       @ 080b758c 3a4b
    adds r3,#0xc    @ 080b758e 0c33
    adds r0,r0,r3    @ 080b7590 c018
    ldr r0,[r0,#0x0]                         @ 080b7592 0068
    cmp r7,r0                                @ 080b7594 8742
    bcs LAB_080b75e2                         @ 080b7596 24d2
    .hword 0x4688    @ 080b7598 8846
    .hword 0x4699    @ 080b759a 9946
LAB_080b759c:
    lsls r1,r7,#0x2    @ 080b759c b900
    .hword 0x4640    @ 080b759e 4046
    muls r0,r2    @ 080b75a0 5043
    adds r1,r1,r0    @ 080b75a2 0918
    ldr r0, DAT_080b767c                     @ 080b75a4 3548
    adds r4,r1,r0    @ 080b75a6 0c18
    ldr r0,[r4,#0x0]                         @ 080b75a8 2068
    lsls r0,r0,#0x13    @ 080b75aa c004
    lsrs r5,r0,#0x13    @ 080b75ac c50c
    adds r0,r5,#0x0    @ 080b75ae 281c
    bl get_card_extended_stat_field5         @ 080b75b0 37f04efc
    cmp r0,#0x4                              @ 080b75b4 0428
    ble LAB_080b75d2                         @ 080b75b6 0cdd
    ldr r0,[r4,#0x0]                         @ 080b75b8 2068
    lsls r1,r0,#0x2    @ 080b75ba 8100
    lsrs r1,r1,#0x18    @ 080b75bc 090e
    lsls r1,r1,#0x1    @ 080b75be 4900
    lsls r0,r0,#0x12    @ 080b75c0 8004
    lsrs r0,r0,#0x1f    @ 080b75c2 c00f
    adds r1,r1,r0    @ 080b75c4 0918
    adds r0,r6,#0x0    @ 080b75c6 301c
    bl eval_card_placement_flags_default     @ 080b75c8 edf764f8
    adds r4,r0,#0x0    @ 080b75cc 041c
    cmp r4,#0x0                              @ 080b75ce 002c
    bne LAB_080b7634                         @ 080b75d0 30d1
LAB_080b75d2:
    adds r7,#0x1    @ 080b75d2 0137
    ldr r2, DAT_080b7674                     @ 080b75d4 274a
    .hword 0x4640    @ 080b75d6 4046
    muls r0,r2    @ 080b75d8 5043
    add r0,r9                                @ 080b75da 4844
    ldr r0,[r0,#0x0]                         @ 080b75dc 0068
    cmp r7,r0                                @ 080b75de 8742
    bcc LAB_080b759c                         @ 080b75e0 dcd3
LAB_080b75e2:
    movs r7,#0x0    @ 080b75e2 0027
    movs r2,#0x1    @ 080b75e4 0122
    ands r2,r6    @ 080b75e6 3240
    ldr r3, DAT_080b7674                     @ 080b75e8 224b
    adds r0,r2,#0x0    @ 080b75ea 101c
    muls r0,r3    @ 080b75ec 5843
    ldr r1, PTR_gP1LifePoints_080b7678       @ 080b75ee 2249
    adds r1,#0xc    @ 080b75f0 0c31
    adds r0,r0,r1    @ 080b75f2 4018
    ldr r0,[r0,#0x0]                         @ 080b75f4 0068
    cmp r7,r0                                @ 080b75f6 8742
    bcs LAB_080b7690                         @ 080b75f8 4ad2
    .hword 0x4690    @ 080b75fa 9046
    .hword 0x4689    @ 080b75fc 8946
LAB_080b75fe:
    lsls r1,r7,#0x2    @ 080b75fe b900
    .hword 0x4640    @ 080b7600 4046
    muls r0,r3    @ 080b7602 5843
    adds r1,r1,r0    @ 080b7604 0918
    ldr r0, DAT_080b767c                     @ 080b7606 1d48
    adds r4,r1,r0    @ 080b7608 0c18
    ldr r0,[r4,#0x0]                         @ 080b760a 2068
    lsls r0,r0,#0x13    @ 080b760c c004
    lsrs r5,r0,#0x13    @ 080b760e c50c
    adds r0,r5,#0x0    @ 080b7610 281c
    bl check_card_field5_is_nonzero          @ 080b7612 93f799fb
    cmp r0,#0x0                              @ 080b7616 0028
    beq LAB_080b7680                         @ 080b7618 32d0
    ldr r0,[r4,#0x0]                         @ 080b761a 2068
    lsls r1,r0,#0x2    @ 080b761c 8100
    lsrs r1,r1,#0x18    @ 080b761e 090e
    lsls r1,r1,#0x1    @ 080b7620 4900
    lsls r0,r0,#0x12    @ 080b7622 8004
    lsrs r0,r0,#0x1f    @ 080b7624 c00f
    adds r1,r1,r0    @ 080b7626 0918
    adds r0,r6,#0x0    @ 080b7628 301c
    bl eval_card_placement_flags_default     @ 080b762a edf733f8
    adds r4,r0,#0x0    @ 080b762e 041c
    cmp r4,#0x0                              @ 080b7630 002c
    beq LAB_080b7680                         @ 080b7632 25d0
LAB_080b7634:
    adds r0,r6,#0x0    @ 080b7634 301c
    adds r1,r5,#0x0    @ 080b7636 291c
    movs r2,#0x0    @ 080b7638 0022
    movs r3,#0x0    @ 080b763a 0023
    bl eval_card_activation_score_with_lp_threshold @ 080b763c f4f780ff
    adds r1,r0,#0x0    @ 080b7640 011c
    cmp r1,#0x0                              @ 080b7642 0029
    beq LAB_080b7654                         @ 080b7644 06d0
    movs r0,#0x40    @ 080b7646 4020
    ands r0,r4    @ 080b7648 2040
    cmp r0,#0x0                              @ 080b764a 0028
    bne LAB_080b7650                         @ 080b764c 00d1
    movs r1,#0x0    @ 080b764e 0021
LAB_080b7650:
    cmp r1,#0x0                              @ 080b7650 0029
    bne LAB_080b765e                         @ 080b7652 04d1
LAB_080b7654:
    movs r0,#0x10    @ 080b7654 1020
    ands r0,r4    @ 080b7656 2040
LAB_080b7658:
    cmp r0,#0x0                              @ 080b7658 0028
    bne LAB_080b765e                         @ 080b765a 00d1
    movs r1,#0x1    @ 080b765c 0121
LAB_080b765e:
    movs r3,#0x4    @ 080b765e 0423
    cmp r1,#0x0                              @ 080b7660 0029
    beq LAB_080b7666                         @ 080b7662 00d0
    movs r3,#0x6    @ 080b7664 0623
LAB_080b7666:
    adds r0,r6,#0x0    @ 080b7666 301c
    movs r1,#0xb    @ 080b7668 0b21
    adds r2,r7,#0x0    @ 080b766a 3a1c
    bl init_duel_zone_target_slot_refs       @ 080b766c dff7d2fb
    b LAB_080b7690                           @ 080b7670 0ee0
    .zero  0x2
DAT_080b7674:
    .word  0x00000868                     @ 080b7674 68080000
PTR_gP1LifePoints_080b7678:
    .word  gP1LifePoints                  @ 080b7678 e0c40102
DAT_080b767c:
    .word  0x0201c600                     @ 080b767c 00c60102
LAB_080b7680:
    adds r7,#0x1    @ 080b7680 0137
    ldr r3, DAT_080b76a0                     @ 080b7682 074b
    .hword 0x4640    @ 080b7684 4046
    muls r0,r3    @ 080b7686 5843
    add r0,r9                                @ 080b7688 4844
    ldr r0,[r0,#0x0]                         @ 080b768a 0068
    cmp r7,r0                                @ 080b768c 8742
    bcc LAB_080b75fe                         @ 080b768e b6d3
LAB_080b7690:
    add sp,#0x4                              @ 080b7690 01b0
    pop {r3,r4,r5}                           @ 080b7692 38bc
    .hword 0x4698    @ 080b7694 9846
    .hword 0x46a1    @ 080b7696 a146
    .hword 0x46aa    @ 080b7698 aa46
    pop {r4,r5,r6,r7}                        @ 080b769a f0bc
    pop {r0}                                 @ 080b769c 01bc
    bx r0                                    @ 080b769e 0047
DAT_080b76a0:
    .word  0x00000868                     @ 080b76a0 68080000
    .byte  0x01, 0x20, 0x70, 0x47

@ Checks if the opponent side has any active effect nodes.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit from [r0+2] bit0; computes opponent = 1 - player_bit.
@ Calls count_effect_node_activations_by_zone(opponent).
@ Returns 1 if count > 0 (opponent has active effect nodes), 0 otherwise.
@ Used to determine if opponent is in an active effect state before triggering own equip/effect.
@ Symmetric counterpart to check_self_effect_node_active (0x080b76c8):
@ that function passes player_bit (self), this function passes 1-player_bit (opponent).
check_opponent_effect_node_active:
    push {lr}                                @ 080b76a8 00b5
    ldrb r1,[r0,#0x2]                        @ 080b76aa 8178
    lsls r2,r1,#0x1f    @ 080b76ac ca07
    lsrs r2,r2,#0x1f    @ 080b76ae d20f
    movs r1,#0x1    @ 080b76b0 0121
    subs r1,r1,r2    @ 080b76b2 891a
    bl count_effect_node_activations_by_zone @ 080b76b4 d9f79ef8
    movs r1,#0x0    @ 080b76b8 0021
    cmp r0,#0x0                              @ 080b76ba 0028
    ble LAB_080b76c0                         @ 080b76bc 00dd
    movs r1,#0x1    @ 080b76be 0121
LAB_080b76c0:
    adds r0,r1,#0x0    @ 080b76c0 081c
    pop {r1}                                 @ 080b76c2 02bc
    bx r1                                    @ 080b76c4 0847
    .zero  0x2

@ Checks if the self side has any active effect nodes.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit from [r0+2] bit0 (no flip).
@ Calls count_effect_node_activations_by_zone(player_bit).
@ Returns 1 if count > 0, 0 otherwise.
@ Symmetric counterpart to check_opponent_effect_node_active (0x080b76a8):
@ 76a8 passes opponent side (1-player_bit), this function passes self (player_bit).
@ Near-identical variant: check_self_effect_node_active_b (0x080b7760) uses bne instead of ble.
check_self_effect_node_active:
    push {lr}                                @ 080b76c8 00b5
    ldrb r2,[r0,#0x2]                        @ 080b76ca 8278
    lsls r1,r2,#0x1f    @ 080b76cc d107
    lsrs r1,r1,#0x1f    @ 080b76ce c90f
    bl count_effect_node_activations_by_zone @ 080b76d0 d9f790f8
    movs r1,#0x0    @ 080b76d4 0021
    cmp r0,#0x0                              @ 080b76d6 0028
    ble LAB_080b76dc                         @ 080b76d8 00dd
    movs r1,#0x1    @ 080b76da 0121
LAB_080b76dc:
    adds r0,r1,#0x0    @ 080b76dc 081c
    pop {r1}                                 @ 080b76de 02bc
    bx r1                                    @ 080b76e0 0847
    .zero  0x2

@ Checks if a card zone has sufficient pair slot count for activation eligibility.
@ r0=zone_ptr (struct[+0]=card_id halfword, struct[+2]=player_bits and type bits[5:1]).
@ Extracts player_bit and card_id, calls count_slot_card_pair_allowed_for_card(player, card_id) -> count.
@ Extracts type from [r0+2] bits[5:1] (lsls #0x1a / lsrs #0x1b).
@ If type <= 10 (standard zone): requires count > 1 (strict threshold, subs r0,r2,#1 > 0).
@ If type > 10 (extended zone): requires count > 0 (relaxed threshold).
@ Returns 1 if sufficient pair slots, 0 otherwise.
@ Called by FUN_080b7f64 (0x080b7f64) and 0x080bad6c for compound pair eligibility checks.
@ 
@ Constants:
@ - TYPE_THRESHOLD=10 (cmp r0,#0xa)
@ - COUNT_THRESHOLD=1 (subs r0,r2,#1 for strict check)
@ - type_field=[r0+2] bits[5:1]
check_card_pair_slot_count_eligible:
    push {r4,lr}                             @ 080b76e4 10b5
    adds r4,r0,#0x0    @ 080b76e6 041c
    ldrb r1,[r4,#0x2]                        @ 080b76e8 a178
    lsls r0,r1,#0x1f    @ 080b76ea c807
    lsrs r0,r0,#0x1f    @ 080b76ec c00f
    ldrh r1,[r4,#0x0]                        @ 080b76ee 2188
    bl count_slot_card_pair_allowed_for_card @ 080b76f0 7bf744fc
    adds r2,r0,#0x0    @ 080b76f4 021c
    ldrb r4,[r4,#0x2]                        @ 080b76f6 a478
    lsls r0,r4,#0x1a    @ 080b76f8 a006
    lsrs r0,r0,#0x1b    @ 080b76fa c00e
    cmp r0,#0xa                              @ 080b76fc 0a28
    bhi LAB_080b770a                         @ 080b76fe 04d8
    movs r1,#0x0    @ 080b7700 0021
    subs r0,r2,#0x1    @ 080b7702 501e
    cmp r0,#0x0                              @ 080b7704 0028
    bgt LAB_080b7712                         @ 080b7706 04dc
    b LAB_080b7710                           @ 080b7708 02e0
LAB_080b770a:
    movs r1,#0x0    @ 080b770a 0021
    cmp r2,#0x0                              @ 080b770c 002a
    bgt LAB_080b7712                         @ 080b770e 00dc
LAB_080b7710:
    movs r1,#0x1    @ 080b7710 0121
LAB_080b7712:
    adds r0,r1,#0x0    @ 080b7712 081c
    pop {r4}                                 @ 080b7714 10bc
    pop {r1}                                 @ 080b7716 02bc
    bx r1                                    @ 080b7718 0847
    .zero  0x2

@ Checks if the effect handler for a zone entry returns a positive (nonzero) result.
@ r0=zone_ptr (struct[+0]=card_id halfword, struct[+2] bit0=player_side).
@ Extracts player_bit -> r4; card_id -> r5.
@ Calls lookup_slot_display_value_by_card_id(card_id) -> r2 (display value).
@ Calls dispatch_effect_handler_by_card_id(player, card_id, display_value).
@ Returns 1 if result > 0, 0 if result <= 0.
@ Used to determine if a specific card's effect handler reports a valid activation state.
@ Side effects depend on dispatch_effect_handler_by_card_id internal behavior.
check_effect_handler_result_nonzero:
    push {r4,r5,lr}                          @ 080b771c 30b5
    ldrb r1,[r0,#0x2]                        @ 080b771e 8178
    lsls r4,r1,#0x1f    @ 080b7720 cc07
    lsrs r4,r4,#0x1f    @ 080b7722 e40f
    ldrh r5,[r0,#0x0]                        @ 080b7724 0588
    bl lookup_slot_display_value_by_card_id  @ 080b7726 caf751f9
    adds r2,r0,#0x0    @ 080b772a 021c
    adds r0,r4,#0x0    @ 080b772c 201c
    adds r1,r5,#0x0    @ 080b772e 291c
    bl dispatch_effect_handler_by_card_id    @ 080b7730 d6f7bef9
    movs r1,#0x0    @ 080b7734 0021
    cmp r0,#0x0                              @ 080b7736 0028
    ble LAB_080b773c                         @ 080b7738 00dd
    movs r1,#0x1    @ 080b773a 0121
LAB_080b773c:
    adds r0,r1,#0x0    @ 080b773c 081c
    pop {r4,r5}                              @ 080b773e 30bc
    pop {r1}                                 @ 080b7740 02bc
    bx r1                                    @ 080b7742 0847

@ Checks if the player's hand contains an available equip target, using zone_ptr to identify the player.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit from [r0+2] bit0 via lsls/lsrs.
@ Calls check_hand_equip_target_available(player_bit).
@ Normalizes result to 0/1 bool.
@ Thin wrapper around check_hand_equip_target_available; auto-extracts player_side from zone struct.
check_hand_equip_target_available_for_zone:
    push {lr}                                @ 080b7744 00b5
    ldrb r0,[r0,#0x2]                        @ 080b7746 8078
    lsls r0,r0,#0x1f    @ 080b7748 c007
    lsrs r0,r0,#0x1f    @ 080b774a c00f
    bl check_hand_equip_target_available     @ 080b774c f8f738f9
    cmp r0,#0x0                              @ 080b7750 0028
    beq LAB_080b7758                         @ 080b7752 01d0
    movs r0,#0x1    @ 080b7754 0120
    b LAB_080b775a                           @ 080b7756 00e0
LAB_080b7758:
    movs r0,#0x0    @ 080b7758 0020
LAB_080b775a:
    pop {r1}                                 @ 080b775a 02bc
    bx r1                                    @ 080b775c 0847
    .zero  0x2

@ Checks if the self side has active effect nodes (variant B).
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Identical behavior to check_self_effect_node_active (0x080b76c8):
@ extracts player_bit from [r0+2] bit0, calls count_effect_node_activations_by_zone(player_bit),
@ returns 1 if count > 0, else 0.
@ Difference from 0x080b76c8: uses bne (count!=0 -> 1) instead of ble (count<=0 -> 0 path).
@ Equivalent for non-negative counts; two independently compiled variants of same predicate.
check_self_effect_node_active_b:
    push {lr}                                @ 080b7760 00b5
    ldrb r2,[r0,#0x2]                        @ 080b7762 8278
    lsls r1,r2,#0x1f    @ 080b7764 d107
    lsrs r1,r1,#0x1f    @ 080b7766 c90f
    bl count_effect_node_activations_by_zone @ 080b7768 d9f744f8
    movs r1,#0x0    @ 080b776c 0021
    cmp r0,#0x0                              @ 080b776e 0028
    bne LAB_080b7774                         @ 080b7770 00d1
    movs r1,#0x1    @ 080b7772 0121
LAB_080b7774:
    adds r0,r1,#0x0    @ 080b7774 081c
    pop {r1}                                 @ 080b7776 02bc
    bx r1                                    @ 080b7778 0847
    .zero  0x2

@ Thin adapter: extracts player_id from zone_ptr then forwards to check_effect_zone_or_pair_slot_available. Used when caller holds zone_ptr (with [+2] bit0 = player_side field) instead of calling the inner function that takes a scalar player_id parameter. Logic: ldrb [r0+2] -> lsls/lsrs #0x1f extract bit0 -> bl check_effect_zone_or_pair_slot_available; r0 transparently passes through inner return value.
check_effect_zone_available_from_zone_ptr:
    push {lr}                                @ 080b777c 00b5
    ldrb r0,[r0,#0x2]                        @ 080b777e 8078
    lsls r0,r0,#0x1f    @ 080b7780 c007
    lsrs r0,r0,#0x1f    @ 080b7782 c00f
    bl check_effect_zone_or_pair_slot_available @ 080b7784 f6f706f8
    pop {r1}                                 @ 080b7788 02bc
    bx r1                                    @ 080b778a 0847

@ Checks if activation slots are available for Dark Room of Nightmare (0x159b).
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit. Uses DWORD_080b77ac=0x159b (Dark Room of Nightmare icid, cid=1183).
@ First calls count_available_effect_zones(player, 0x159b, mode=-1):
@ if count > 0 -> return 1 immediately.
@ If no effect zone slot: calls count_valid_monster_pair_slots(player, 0x159b) -> r4
@ and count_zone_card_pair_allowed_for_card(player, 0x159b) -> r0.
@ Uses cmn r4,r0: if r4+r0 != 0 (either has slots) -> return 1, else return 0.
@ Used by AI to confirm Dark Room of Nightmare has required field conditions for activation.
@ 
@ Constants:
@ - CARD_Dark_Room_of_Nightmare=0x159b (DWORD_080b77ac, cid=1183)
@ - mode=-1 (rsbs r2,r2,#0)
check_dark_room_activation_slots_available:
    push {r4,r5,r6,lr}                       @ 080b778c 70b5
    adds r5,r0,#0x0    @ 080b778e 051c
    ldrb r1,[r5,#0x2]                        @ 080b7790 a978
    lsls r0,r1,#0x1f    @ 080b7792 c807
    lsrs r0,r0,#0x1f    @ 080b7794 c00f
    ldr r6, DWORD_080b77ac                   @ 080b7796 054e
    movs r2,#0x1    @ 080b7798 0122
    rsbs r2,r2,#0    @ 080b779a 5242
    adds r1,r6,#0x0    @ 080b779c 311c
    bl count_available_effect_zones          @ 080b779e 7af759ff
    cmp r0,#0x0                              @ 080b77a2 0028
    beq LAB_080b77b0                         @ 080b77a4 04d0
    movs r0,#0x1    @ 080b77a6 0120
    b LAB_080b77d4                           @ 080b77a8 14e0
    .zero  0x2
DWORD_080b77ac:
    .word  0x0000159b                     @ 080b77ac 9b150000
LAB_080b77b0:
    ldrb r1,[r5,#0x2]                        @ 080b77b0 a978
    lsls r0,r1,#0x1f    @ 080b77b2 c807
    lsrs r0,r0,#0x1f    @ 080b77b4 c00f
    adds r1,r6,#0x0    @ 080b77b6 311c
    bl count_valid_monster_pair_slots        @ 080b77b8 80f738f9
    adds r4,r0,#0x0    @ 080b77bc 041c
    ldrb r5,[r5,#0x2]                        @ 080b77be ad78
    lsls r0,r5,#0x1f    @ 080b77c0 e807
    lsrs r0,r0,#0x1f    @ 080b77c2 c00f
    adds r1,r6,#0x0    @ 080b77c4 311c
    bl count_zone_card_pair_allowed_for_card @ 080b77c6 7af75df9
    movs r1,#0x0    @ 080b77ca 0021
    cmn r4,r0                                @ 080b77cc c442
    bne LAB_080b77d2                         @ 080b77ce 00d1
    movs r1,#0x1    @ 080b77d0 0121
LAB_080b77d2:
    adds r0,r1,#0x0    @ 080b77d2 081c
LAB_080b77d4:
    pop {r4,r5,r6}                           @ 080b77d4 70bc
    pop {r1}                                 @ 080b77d6 02bc
    bx r1                                    @ 080b77d8 0847
    .zero  0x2

@ Checks if self zone score is better than opponent (score advantage check).
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit, calls compare_zone_max_scores_by_player(player_bit).
@ Returns 1 if result > 0 (self max score higher than opponent), else 0.
@ Used by AI to determine score advantage when deciding whether to activate trap/spell effects.
check_zone_score_advantage_for_self:
    push {lr}                                @ 080b77dc 00b5
    ldrb r0,[r0,#0x2]                        @ 080b77de 8078
    lsls r0,r0,#0x1f    @ 080b77e0 c007
    lsrs r0,r0,#0x1f    @ 080b77e2 c00f
    bl compare_zone_max_scores_by_player     @ 080b77e4 f7f7f6fa
    movs r1,#0x0    @ 080b77e8 0021
    cmp r0,#0x0                              @ 080b77ea 0028
    ble LAB_080b77f0                         @ 080b77ec 00dd
    movs r1,#0x1    @ 080b77ee 0121
LAB_080b77f0:
    adds r0,r1,#0x0    @ 080b77f0 081c
    pop {r1}                                 @ 080b77f2 02bc
    bx r1                                    @ 080b77f4 0847
    .zero  0x2

@ Checks if self LP is behind by more than 500 points compared to opponent (LP disadvantage threshold check).
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit from [r0+2] bit0.
@ Computes self LP base: gP1LifePoints + player*0x868; reads self LP value.
@ Computes opponent LP base: gP1LifePoints + (1-player)*0x868; reads opponent LP value.
@ Adds 500 (0xfa<<1 = 0x1f4) to self LP: if opponent LP < (self LP + 500)
@ (i.e. self LP is behind by more than 500) -> returns 1, else returns 0.
@ Note: bge branch keeps r5=0 when opponent LP >= self LP+500; else r5=1.
@ Used by AI to trigger special effects when self is at LP disadvantage exceeding 500.
@ 
@ Constants:
@ - LP_MARGIN=500 (0xfa*2 = 0x1f4)
@ - gP1LifePoints=0x0201c4e0 (DWORD_080b7830)
@ - player_stride=0x868 (DWORD_080b7834)
check_self_lp_advantage_by_500_margin:
    push {r4,r5,lr}                          @ 080b77f8 30b5
    movs r5,#0x0    @ 080b77fa 0025
    ldr r4, DWORD_080b7830                   @ 080b77fc 0c4c
    ldrb r0,[r0,#0x2]                        @ 080b77fe 8078
    lsls r2,r0,#0x1f    @ 080b7800 c207
    lsrs r1,r2,#0x1f    @ 080b7802 d10f
    movs r0,#0x1    @ 080b7804 0120
    subs r1,r0,r1    @ 080b7806 411a
    ands r1,r0    @ 080b7808 0140
    ldr r3, DWORD_080b7834                   @ 080b780a 0a4b
    muls r1,r3    @ 080b780c 5943
    adds r1,r1,r4    @ 080b780e 0919
    lsrs r2,r2,#0x1f    @ 080b7810 d20f
    ands r0,r2    @ 080b7812 1040
    muls r0,r3    @ 080b7814 5843
    adds r0,r0,r4    @ 080b7816 0019
    ldr r0,[r0,#0x0]                         @ 080b7818 0068
    movs r2,#0xfa    @ 080b781a fa22
    lsls r2,r2,#0x1    @ 080b781c 5200
    adds r0,r0,r2    @ 080b781e 8018
    ldr r1,[r1,#0x0]                         @ 080b7820 0968
    cmp r1,r0                                @ 080b7822 8142
    bge LAB_080b7828                         @ 080b7824 00da
    movs r5,#0x1    @ 080b7826 0125
LAB_080b7828:
    adds r0,r5,#0x0    @ 080b7828 281c
    pop {r4,r5}                              @ 080b782a 30bc
    pop {r1}                                 @ 080b782c 02bc
    bx r1                                    @ 080b782e 0847
DWORD_080b7830:
    .word  gP1LifePoints                  @ 080b7830 e0c40102
DWORD_080b7834:
    .word  0x00000868                     @ 080b7834 68080000

@ Checks if opponent has more than 1 active equip slot.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit, computes opponent = 1 - player_bit.
@ Calls count_equip_slots_active_only(opponent).
@ Returns 1 if count > 1, 0 if count <= 1.
@ Used by AI to determine if opponent equip count reaches threshold to trigger a special effect
@ (more than 1 equip required for activation).
@ 
@ Constants:
@ - EQUIP_COUNT_THRESHOLD=1 (cmp r0,#1; ble -> count<=1 -> return 0)
check_opponent_equip_count_exceeds_one:
    push {lr}                                @ 080b7838 00b5
    ldrb r0,[r0,#0x2]                        @ 080b783a 8078
    lsls r1,r0,#0x1f    @ 080b783c c107
    lsrs r1,r1,#0x1f    @ 080b783e c90f
    movs r0,#0x1    @ 080b7840 0120
    subs r0,r0,r1    @ 080b7842 401a
    bl count_equip_slots_active_only         @ 080b7844 7cf760f9
    movs r1,#0x0    @ 080b7848 0021
    cmp r0,#0x1                              @ 080b784a 0128
    ble LAB_080b7850                         @ 080b784c 00dd
    movs r1,#0x1    @ 080b784e 0121
LAB_080b7850:
    adds r0,r1,#0x0    @ 080b7850 081c
    pop {r1}                                 @ 080b7852 02bc
    bx r1                                    @ 080b7854 0847
    .zero  0x2

@ Checks if opponent monster zone has any equip whitelist cards.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit, computes opponent = 1 - player_bit.
@ Calls count_equip_whitelist_cards_in_monster_zone(opponent).
@ Returns 1 if count > 0, 0 otherwise.
@ Used together with check_opponent_equip_count_exceeds_one (0x080b7838) and similar predicates
@ as combined activation condition gate checks.
check_opponent_equip_whitelist_cards_present:
    push {lr}                                @ 080b7858 00b5
    ldrb r0,[r0,#0x2]                        @ 080b785a 8078
    lsls r1,r0,#0x1f    @ 080b785c c107
    lsrs r1,r1,#0x1f    @ 080b785e c90f
    movs r0,#0x1    @ 080b7860 0120
    subs r0,r0,r1    @ 080b7862 401a
    bl count_equip_whitelist_cards_in_monster_zone @ 080b7864 f7f762ff
    movs r1,#0x0    @ 080b7868 0021
    cmp r0,#0x0                              @ 080b786a 0028
    ble LAB_080b7870                         @ 080b786c 00dd
    movs r1,#0x1    @ 080b786e 0121
LAB_080b7870:
    adds r0,r1,#0x0    @ 080b7870 081c
    pop {r1}                                 @ 080b7872 02bc
    bx r1                                    @ 080b7874 0847
    .zero  0x2

@ Checks equip activation eligibility for Premature Burial (0x1366) or Call of the Haunted (0x137d).
@ r0=zone_ptr -> r4 (struct[+2] bit0=player_side).
@ First checks if Premature Burial already equipped in self zone via find_equip_slot_by_card_id(player, 0x1366);
@ if slot >= 0 -> return 1 immediately (already present shortcut).
@ Then: if opponent has no monsters (count_occupied_monster_zones(opponent)==0) -> return 0.
@ If self has no monsters -> return 0.
@ If opponent has no active equips (count_equip_slots_active_only(opponent)==0) -> return 0.
@ Then: find_equip_slot_by_card_id(player, 0x137d) for Call of the Haunted slot -> r1.
@ If r1 < 0 -> return 0.
@ Calls find_equip_chain_pair_across_field(player) -> packed_slot_pair.
@ Checks packed_pair bits[15:0] != 0xFFFF (valid pair).
@ Checks associated slot card_id != 0x0fd6 (Sangan) and != 0x11e4 (Witch of the Black Forest).
@ All checks pass -> return 1, any fail -> return 0.
@ 
@ Constants:
@ - CARD_Premature_Burial=0x1366 (DWORD_080b7910, cid=773)
@ - CARD_Call_of_the_Haunted=0x137d (DWORD_080b7914, cid=793)
@ - INVALID_SLOT=0xffff
@ - CARD_Sangan=0x0fd6 (cid=53)
@ - CARD_Witch_of_the_Black_Forest=0x11e4 (cid=477)
@ - gDuelEffectZones=0x0201c510
@ - player_stride=0x868
check_premature_burial_or_coth_equip_eligible:
    push {r4,r5,lr}                          @ 080b7878 30b5
    adds r4,r0,#0x0    @ 080b787a 041c
    ldrb r1,[r4,#0x2]                        @ 080b787c a178
    lsls r0,r1,#0x1f    @ 080b787e c807
    lsrs r0,r0,#0x1f    @ 080b7880 c00f
    ldr r1, DWORD_080b7910                   @ 080b7882 2349
    bl find_equip_slot_by_card_id            @ 080b7884 7af716fe
    cmp r0,#0x0                              @ 080b7888 0028
    bge LAB_080b790a                         @ 080b788a 3eda
    ldrb r1,[r4,#0x2]                        @ 080b788c a178
    lsls r0,r1,#0x1f    @ 080b788e c807
    lsrs r0,r0,#0x1f    @ 080b7890 c00f
    movs r5,#0x1    @ 080b7892 0125
    subs r0,r5,r0    @ 080b7894 281a
    bl count_occupied_monster_zones          @ 080b7896 7bf777fc
    cmp r0,#0x0                              @ 080b789a 0028
    bne LAB_080b78bc                         @ 080b789c 0ed1
    ldrb r1,[r4,#0x2]                        @ 080b789e a178
    lsls r0,r1,#0x1f    @ 080b78a0 c807
    lsrs r0,r0,#0x1f    @ 080b78a2 c00f
    bl count_occupied_monster_zones          @ 080b78a4 7bf770fc
    cmp r0,#0x0                              @ 080b78a8 0028
    beq LAB_080b78bc                         @ 080b78aa 07d0
    ldrb r1,[r4,#0x2]                        @ 080b78ac a178
    lsls r0,r1,#0x1f    @ 080b78ae c807
    lsrs r0,r0,#0x1f    @ 080b78b0 c00f
    subs r0,r5,r0    @ 080b78b2 281a
    bl count_equip_slots_active_only         @ 080b78b4 7cf728f9
    cmp r0,#0x0                              @ 080b78b8 0028
    bgt LAB_080b790a                         @ 080b78ba 26dc
LAB_080b78bc:
    ldrb r1,[r4,#0x2]                        @ 080b78bc a178
    lsls r0,r1,#0x1f    @ 080b78be c807
    lsrs r0,r0,#0x1f    @ 080b78c0 c00f
    ldr r1, DWORD_080b7914                   @ 080b78c2 1449
    bl find_equip_slot_by_card_id            @ 080b78c4 7af7f6fd
    adds r1,r0,#0x0    @ 080b78c8 011c
    cmp r1,#0x0                              @ 080b78ca 0029
    blt LAB_080b792c                         @ 080b78cc 2edb
    ldrb r4,[r4,#0x2]                        @ 080b78ce a478
    lsls r0,r4,#0x1f    @ 080b78d0 e007
    lsrs r0,r0,#0x1f    @ 080b78d2 c00f
    bl find_equip_chain_pair_across_field    @ 080b78d4 77f7d4fe
    lsls r1,r0,#0x10    @ 080b78d8 0104
    lsrs r2,r1,#0x10    @ 080b78da 0a0c
    ldr r0, DWORD_080b7918                   @ 080b78dc 0e48
    cmp r2,r0                                @ 080b78de 8242
    beq LAB_080b790a                         @ 080b78e0 13d0
    movs r0,#0x1    @ 080b78e2 0120
    ands r2,r0    @ 080b78e4 0240
    lsrs r1,r1,#0x18    @ 080b78e6 090e
    lsls r0,r1,#0x2    @ 080b78e8 8800
    adds r0,r0,r1    @ 080b78ea 4018
    lsls r0,r0,#0x2    @ 080b78ec 8000
    ldr r1, DWORD_080b791c                   @ 080b78ee 0b49
    muls r1,r2    @ 080b78f0 5143
    adds r0,r0,r1    @ 080b78f2 4018
    ldr r1, DWORD_080b7920                   @ 080b78f4 0a49
    adds r0,r0,r1    @ 080b78f6 4018
    ldr r0,[r0,#0x0]                         @ 080b78f8 0068
    lsls r0,r0,#0x13    @ 080b78fa c004
    lsrs r1,r0,#0x13    @ 080b78fc c10c
    ldr r0, DWORD_080b7924                   @ 080b78fe 0948
    cmp r1,r0                                @ 080b7900 8142
    beq LAB_080b790a                         @ 080b7902 02d0
    ldr r0, DWORD_080b7928                   @ 080b7904 0848
    cmp r1,r0                                @ 080b7906 8142
    bne LAB_080b792c                         @ 080b7908 10d1
LAB_080b790a:
    movs r0,#0x1    @ 080b790a 0120
    b LAB_080b792e                           @ 080b790c 0fe0
    .zero  0x2
DWORD_080b7910:
    .word  0x00001366                     @ 080b7910 66130000
DWORD_080b7914:
    .word  0x0000137d                     @ 080b7914 7d130000
DWORD_080b7918:
    .word  0x0000ffff                     @ 080b7918 ffff0000
DWORD_080b791c:
    .word  0x00000868                     @ 080b791c 68080000
DWORD_080b7920:
    .word  0x0201c510                     @ 080b7920 10c50102
DWORD_080b7924:
    .word  0x00000fd6                     @ 080b7924 d60f0000
DWORD_080b7928:
    .word  0x000011e4                     @ 080b7928 e4110000
LAB_080b792c:
    movs r0,#0x0    @ 080b792c 0020
LAB_080b792e:
    pop {r4,r5}                              @ 080b792e 30bc
    pop {r1}                                 @ 080b7930 02bc
    bx r1                                    @ 080b7932 0847

@ Checks if equip activation is valid under field-wide level restriction cards.
@ r0=zone_ptr -> r5 (struct[+2] bit0=player_side).
@ Extracts player_bit; opponent = 1 - player_bit.
@ Step 1: count_equip_slots_active_only(opponent) -> r6; if r6==0 -> return 0.
@ Step 2: count_equip_whitelist_cards_in_monster_zone for both sides; self > opponent count -> return 1.
@ If r6 > 1 and self active equip count >= opponent: continue to core check.
@ Core: check_equip_effect_zone_preconditions(self) -> 0 then return 0.
@ count_field_copies_of_card(0x140e=Gravity Bind) and count_field_copies_of_card(0x17a6=Level Limit Area B).
@ If neither is on field -> return 0.
@ find_best_activatable_slot_score_for_player(self, -1, 0) -> r4=score.
@ Compare r4 against LP threshold and lower bound 0x095f (2399).
@ If in range: compare_zone_max_scores_by_player; <= 0 -> fail; > 0 -> return 1.
@ 
@ Constants:
@ - CARD_Gravity_Bind=0x140e (cid=889)
@ - CARD_Level_Limit_Area_B=0x17a6 (cid=1596)
@ - SCORE_LOWER_BOUND=0x095f=2399
@ - gP1LifePoints=0x0201c4e0
@ - player_stride=0x868
check_equip_activation_valid_under_level_restriction:
    push {r4,r5,r6,lr}                       @ 080b7934 70b5
    adds r5,r0,#0x0    @ 080b7936 051c
    ldrb r1,[r5,#0x2]                        @ 080b7938 a978
    lsls r0,r1,#0x1f    @ 080b793a c807
    lsrs r0,r0,#0x1f    @ 080b793c c00f
    movs r4,#0x1    @ 080b793e 0124
    subs r0,r4,r0    @ 080b7940 201a
    bl count_equip_slots_active_only         @ 080b7942 7cf7e1f8
    adds r6,r0,#0x0    @ 080b7946 061c
    cmp r6,#0x0                              @ 080b7948 002e
    beq LAB_080b79f0                         @ 080b794a 51d0
    ldrb r1,[r5,#0x2]                        @ 080b794c a978
    lsls r0,r1,#0x1f    @ 080b794e c807
    lsrs r0,r0,#0x1f    @ 080b7950 c00f
    subs r0,r4,r0    @ 080b7952 201a
    bl count_equip_whitelist_cards_in_monster_zone @ 080b7954 f7f7eafe
    adds r4,r0,#0x0    @ 080b7958 041c
    ldrb r1,[r5,#0x2]                        @ 080b795a a978
    lsls r0,r1,#0x1f    @ 080b795c c807
    lsrs r0,r0,#0x1f    @ 080b795e c00f
    bl count_equip_whitelist_cards_in_monster_zone @ 080b7960 f7f7e4fe
    cmp r4,r0                                @ 080b7964 8442
    bgt LAB_080b79d6                         @ 080b7966 36dc
    cmp r6,#0x1                              @ 080b7968 012e
    ble LAB_080b797a                         @ 080b796a 06dd
    ldrb r1,[r5,#0x2]                        @ 080b796c a978
    lsls r0,r1,#0x1f    @ 080b796e c807
    lsrs r0,r0,#0x1f    @ 080b7970 c00f
    bl count_equip_slots_active_only         @ 080b7972 7cf7c9f8
    cmp r6,r0                                @ 080b7976 8642
    bgt LAB_080b79d6                         @ 080b7978 2ddc
LAB_080b797a:
    ldrb r1,[r5,#0x2]                        @ 080b797a a978
    lsls r0,r1,#0x1f    @ 080b797c c807
    lsrs r0,r0,#0x1f    @ 080b797e c00f
    bl check_equip_effect_zone_preconditions @ 080b7980 dff706fc
    cmp r0,#0x0                              @ 080b7984 0028
    beq LAB_080b79f0                         @ 080b7986 33d0
    ldr r0, DWORD_080b79dc                   @ 080b7988 1448
    bl count_field_copies_of_card            @ 080b798a 7af707ff
    cmp r0,#0x0                              @ 080b798e 0028
    bne LAB_080b799c                         @ 080b7990 04d1
    ldr r0, DWORD_080b79e0                   @ 080b7992 1348
    bl count_field_copies_of_card            @ 080b7994 7af702ff
    cmp r0,#0x0                              @ 080b7998 0028
    beq LAB_080b79f0                         @ 080b799a 29d0
LAB_080b799c:
    ldrb r1,[r5,#0x2]                        @ 080b799c a978
    lsls r0,r1,#0x1f    @ 080b799e c807
    lsrs r0,r0,#0x1f    @ 080b79a0 c00f
    movs r1,#0x1    @ 080b79a2 0121
    rsbs r1,r1,#0    @ 080b79a4 4942
    movs r2,#0x0    @ 080b79a6 0022
    bl find_best_activatable_slot_score_for_player @ 080b79a8 f4f73efb
    adds r4,r0,#0x0    @ 080b79ac 041c
    ldr r2, DWORD_080b79e4                   @ 080b79ae 0d4a
    ldrb r5,[r5,#0x2]                        @ 080b79b0 ad78
    lsls r3,r5,#0x1f    @ 080b79b2 eb07
    lsrs r0,r3,#0x1f    @ 080b79b4 d80f
    movs r1,#0x1    @ 080b79b6 0121
    eors r0,r1    @ 080b79b8 4840
    ldr r1, DWORD_080b79e8                   @ 080b79ba 0b49
    muls r0,r1    @ 080b79bc 4843
    adds r0,r0,r2    @ 080b79be 8018
    ldr r0,[r0,#0x0]                         @ 080b79c0 0068
    cmp r4,r0                                @ 080b79c2 8442
    bge LAB_080b79cc                         @ 080b79c4 02da
    ldr r0, DWORD_080b79ec                   @ 080b79c6 0948
    cmp r4,r0                                @ 080b79c8 8442
    ble LAB_080b79f0                         @ 080b79ca 11dd
LAB_080b79cc:
    lsrs r0,r3,#0x1f    @ 080b79cc d80f
    bl compare_zone_max_scores_by_player     @ 080b79ce f7f701fa
    cmp r0,#0x0                              @ 080b79d2 0028
    ble LAB_080b79f0                         @ 080b79d4 0cdd
LAB_080b79d6:
    movs r0,#0x1    @ 080b79d6 0120
    b LAB_080b79f2                           @ 080b79d8 0be0
    .zero  0x2
DWORD_080b79dc:
    .word  0x0000140e                     @ 080b79dc 0e140000
DWORD_080b79e0:
    .word  0x000017a6                     @ 080b79e0 a6170000
DWORD_080b79e4:
    .word  gP1LifePoints                  @ 080b79e4 e0c40102
DWORD_080b79e8:
    .word  0x00000868                     @ 080b79e8 68080000
DWORD_080b79ec:
    .word  0x0000095f                     @ 080b79ec 5f090000
LAB_080b79f0:
    movs r0,#0x0    @ 080b79f0 0020
LAB_080b79f2:
    pop {r4,r5,r6}                           @ 080b79f2 70bc
    pop {r1}                                 @ 080b79f4 02bc
    bx r1                                    @ 080b79f6 0847

@ Equip activation eligibility predicate; iterates 5 effect node slots (index 0..4), calls invoke_effect_node_handler_3arg for each; if handler returns non-zero and node count > 1, calls get_slot_field6_score to verify non-zero score; first passing slot returns 1, all fail returns 0. Used in AI decision layer to determine whether any favorable activatable effect node exists.
@ 
@ Constants:
@ - BASE = 0x0201afe0 (gDuelEffectZones base)
@ - NODE_STRIDE = 0x4 (r6 advances +4 per iteration)
@ - SLOT_COUNT = 5 ([0..4])
@ - MIN_NODE_COUNT = 2 (cmp r0,#1; bls -> needs > 1)
check_effect_node_eligible_in_any_slot_with_field6_score:
    push {r4,r5,r6,lr}                       @ 080b79f8 70b5
    adds r5,r0,#0x0    @ 080b79fa 051c
    movs r4,#0x0    @ 080b79fc 0024
    ldr r0, DWORD_080b7a34                   @ 080b79fe 0d48
    movs r1,#0xcc    @ 080b7a00 cc21
    lsls r1,r1,#0x1    @ 080b7a02 4900
    adds r6,r0,r1    @ 080b7a04 4618
LAB_080b7a06:
    ldrb r0,[r5,#0x2]                        @ 080b7a06 a878
    lsls r1,r0,#0x1f    @ 080b7a08 c107
    lsrs r1,r1,#0x1f    @ 080b7a0a c90f
    adds r0,r5,#0x0    @ 080b7a0c 281c
    adds r2,r4,#0x0    @ 080b7a0e 221c
    bl invoke_effect_node_handler_3arg       @ 080b7a10 d8f7eafd
    cmp r0,#0x0                              @ 080b7a14 0028
    beq LAB_080b7a38                         @ 080b7a16 0fd0
    ldr r0,[r6,#0x0]                         @ 080b7a18 3068
    cmp r0,#0x1                              @ 080b7a1a 0128
    bls LAB_080b7a38                         @ 080b7a1c 0cd9
    ldrb r1,[r5,#0x2]                        @ 080b7a1e a978
    lsls r0,r1,#0x1f    @ 080b7a20 c807
    lsrs r0,r0,#0x1f    @ 080b7a22 c00f
    adds r1,r4,#0x0    @ 080b7a24 211c
    bl get_slot_field6_score                 @ 080b7a26 82f7abff
    cmp r0,#0x0                              @ 080b7a2a 0028
    beq LAB_080b7a38                         @ 080b7a2c 04d0
    movs r0,#0x1    @ 080b7a2e 0120
    b LAB_080b7a42                           @ 080b7a30 07e0
    .zero  0x2
DWORD_080b7a34:
    .word  0x0201afe0                     @ 080b7a34 e0af0102
LAB_080b7a38:
    adds r6,#0x4    @ 080b7a38 0436
    adds r4,#0x1    @ 080b7a3a 0134
    cmp r4,#0x4                              @ 080b7a3c 042c
    ble LAB_080b7a06                         @ 080b7a3e e2dd
    movs r0,#0x0    @ 080b7a40 0020
LAB_080b7a42:
    pop {r4,r5,r6}                           @ 080b7a42 70bc
    pop {r1}                                 @ 080b7a44 02bc
    bx r1                                    @ 080b7a46 0847

@ Checks if opponent zone has any active cards with mode=1.
@ r0=zone_ptr (struct[+2] bit0=player_side).
@ Extracts player_bit; computes opponent = 1 - player_bit.
@ Sets mode=1 (movs r1,#1), calls count_active_cards_in_zone_by_player(opponent, mode=1).
@ Returns 1 if count > 0, 0 otherwise.
@ Part of the equip activation pre-condition predicate group alongside other check_opponent_* functions.
@ 
@ Constants:
@ - MODE=1 (movs r1,#1)
check_opponent_active_zone_cards_present:
    push {lr}                                @ 080b7a48 00b5
    ldrb r0,[r0,#0x2]                        @ 080b7a4a 8078
    lsls r1,r0,#0x1f    @ 080b7a4c c107
    lsrs r1,r1,#0x1f    @ 080b7a4e c90f
    movs r0,#0x1    @ 080b7a50 0120
    subs r0,r0,r1    @ 080b7a52 401a
    movs r1,#0x1    @ 080b7a54 0121
    bl count_active_cards_in_zone_by_player  @ 080b7a56 7bf78bfc
    cmp r0,#0x0                              @ 080b7a5a 0028
    beq LAB_080b7a62                         @ 080b7a5c 01d0
    movs r0,#0x1    @ 080b7a5e 0120
    b LAB_080b7a64                           @ 080b7a60 00e0
LAB_080b7a62:
    movs r0,#0x0    @ 080b7a62 0020
LAB_080b7a64:
    pop {r1}                                 @ 080b7a64 02bc
    bx r1                                    @ 080b7a66 0847
    ROM_INCBIN 0xb7a68, 0x4fc

@ Equip activation dual-gate eligibility predicate; first validates card pair slot count via check_card_pair_slot_count_eligible, then validates opponent side has chain field matching slots via count_slots_with_chain_field_match > 0. Called in equip activation decision when evaluating "pair slot + chain condition". If check_card_pair_slot_count_eligible returns 0 -> return 0; otherwise computes opponent player_id = 1 - player_id, calls count_slots_with_chain_field_match(opponent, 0, 1) > 0 to return 1. No external writes; pure predicate.
check_equip_eligible_with_pair_slot_and_chain_gate:
    push {r4,r5,lr}                          @ 080b7f64 30b5
    adds r4,r0,#0x0    @ 080b7f66 041c
    movs r5,#0x0    @ 080b7f68 0025
    bl check_card_pair_slot_count_eligible   @ 080b7f6a fff7bbfb
    cmp r0,#0x0                              @ 080b7f6e 0028
    beq LAB_080b7f8a                         @ 080b7f70 0bd0
    ldrb r4,[r4,#0x2]                        @ 080b7f72 a478
    lsls r1,r4,#0x1f    @ 080b7f74 e107
    lsrs r1,r1,#0x1f    @ 080b7f76 c90f
    movs r0,#0x1    @ 080b7f78 0120
    subs r0,r0,r1    @ 080b7f7a 401a
    movs r1,#0x0    @ 080b7f7c 0021
    movs r2,#0x1    @ 080b7f7e 0122
    bl count_slots_with_chain_field_match    @ 080b7f80 7bf788f9
    cmp r0,#0x0                              @ 080b7f84 0028
    ble LAB_080b7f8a                         @ 080b7f86 00dd
    movs r5,#0x1    @ 080b7f88 0125
LAB_080b7f8a:
    adds r0,r5,#0x0    @ 080b7f8a 281c
    pop {r4,r5}                              @ 080b7f8c 30bc
    pop {r1}                                 @ 080b7f8e 02bc
    bx r1                                    @ 080b7f90 0847
    .zero  0x2

@ Predicate: returns 1 if the player's monster zone has at least one vacancy (slot_count > 1), else 0. Extracts player_id from zone_ptr->byte[2] bit0, calls count_available_monster_slots(1-player_id). Returns via pop{r1}+bx r1 (Sub-case E). Used as a precondition check before equip card placement or activation.
@ 
@ Constants:
@ - VACANCY_THRESHOLD = 1 (slot_count > 1 -> has_vacancy=1)
@ 
@ Inputs: r0=ptr zone_ptr (field zone ptr, byte[2] bit0=player_id)
@ Returns: r0=u32 has_vacancy (1=has vacancy, 0=no vacancy)
@ Side effects: none (read-only)
check_monster_zone_has_vacancy:
    push {lr}                                @ 080b7f94 00b5
    ldrb r0,[r0,#0x2]                        @ 080b7f96 8078
    lsls r1,r0,#0x1f    @ 080b7f98 c107
    lsrs r1,r1,#0x1f    @ 080b7f9a c90f
    movs r0,#0x1    @ 080b7f9c 0120
    subs r0,r0,r1    @ 080b7f9e 401a
    bl count_available_monster_slots         @ 080b7fa0 7bf70afb
    movs r1,#0x0    @ 080b7fa4 0021
    cmp r0,#0x1                              @ 080b7fa6 0128
    ble LAB_080b7fac                         @ 080b7fa8 00dd
    movs r1,#0x1    @ 080b7faa 0121
LAB_080b7fac:
    adds r0,r1,#0x0    @ 080b7fac 081c
    pop {r1}                                 @ 080b7fae 02bc
    bx r1                                    @ 080b7fb0 0847
    .zero  0x2

@ Checks whether opponent LP <= 500 (LP_THRESHOLD_LOW) or own LP > 1500 (LP_THRESHOLD_HIGH). Extracts player_id from zone_ptr->byte[2] bit0, computes opponent_id=1-player_id. Loads gP1LifePoints[opponent_id*0x868] for opponent LP; if <= 500 returns 1. If > 500, loads own LP and tests > 1500; sets flag=1 if true. Returns OR of both checks via pop{r1}+bx r1 (Sub-case E).
@ 
@ Constants:
@ - gP1LifePoints = 0x0201c4e0 (DWORD_080b7fd8)
@ - PLAYER_STRIDE = 0x868 (0x00000868, DWORD_080b7fdc)
@ - LP_THRESHOLD_LOW = 0x1f4 (500, movs r0,#0xfa; lsls r0,r0,#1)
@ - LP_THRESHOLD_HIGH = 0x5dc (1500, DWORD_080b8000)
@ 
@ Inputs: r0=ptr zone_ptr (field zone ptr, byte[2] bit0=player_id)
@ Returns: r0=u32 flag (1=LP threshold condition met, 0=not met)
@ Side effects: none (read-only)
check_lp_below_lp_threshold:
    push {r4,r5,r6,lr}                       @ 080b7fb4 70b5
    ldr r6, DWORD_080b7fd8                   @ 080b7fb6 084e
    ldrb r0,[r0,#0x2]                        @ 080b7fb8 8078
    lsls r3,r0,#0x1f    @ 080b7fba c307
    lsrs r0,r3,#0x1f    @ 080b7fbc d80f
    movs r2,#0x1    @ 080b7fbe 0122
    subs r0,r2,r0    @ 080b7fc0 101a
    ands r0,r2    @ 080b7fc2 1040
    ldr r4, DWORD_080b7fdc                   @ 080b7fc4 054c
    muls r0,r4    @ 080b7fc6 6043
    adds r0,r0,r6    @ 080b7fc8 8019
    ldr r1,[r0,#0x0]                         @ 080b7fca 0168
    movs r0,#0xfa    @ 080b7fcc fa20
    lsls r0,r0,#0x1    @ 080b7fce 4000
    cmp r1,r0                                @ 080b7fd0 8142
    bgt LAB_080b7fe0                         @ 080b7fd2 05dc
    movs r0,#0x1    @ 080b7fd4 0120
    b LAB_080b7ff8                           @ 080b7fd6 0fe0
DWORD_080b7fd8:
    .word  gP1LifePoints                  @ 080b7fd8 e0c40102
DWORD_080b7fdc:
    .word  0x00000868                     @ 080b7fdc 68080000
LAB_080b7fe0:
    movs r5,#0x0    @ 080b7fe0 0025
    lsrs r1,r3,#0x1f    @ 080b7fe2 d90f
    adds r0,r2,#0x0    @ 080b7fe4 101c
    ands r0,r1    @ 080b7fe6 0840
    muls r0,r4    @ 080b7fe8 6043
    adds r0,r0,r6    @ 080b7fea 8019
    ldr r1,[r0,#0x0]                         @ 080b7fec 0168
    ldr r0, DWORD_080b8000                   @ 080b7fee 0448
    cmp r1,r0                                @ 080b7ff0 8142
    ble LAB_080b7ff6                         @ 080b7ff2 00dd
    movs r5,#0x1    @ 080b7ff4 0125
LAB_080b7ff6:
    adds r0,r5,#0x0    @ 080b7ff6 281c
LAB_080b7ff8:
    pop {r4,r5,r6}                           @ 080b7ff8 70bc
    pop {r1}                                 @ 080b7ffa 02bc
    bx r1                                    @ 080b7ffc 0847
    .zero  0x2
DWORD_080b8000:
    .word  0x000005dc                     @ 080b8000 dc050000
    ROM_INCBIN 0xb8004, 0x8bc
    movs r0,#0x1    @ 080b88c0 0120
    bx lr                                    @ 080b88c2 7047

@ Checks whether a hand equip target with bonus value greater than 6 exists (sibling FUN_080babd4 uses threshold 4). Entry r0=equip_card_zone_ptr. Precondition: calls count_equip_placements_with_chain_check(opponent_player, 0, 1) > 0; else returns 0 immediately. Also checks gP1LifePoints[player_id*0x868+0x11c] bit17; if set returns 0. Calls scan_hand_for_best_equip_target_slot(fn_ptr=0x080b88c1, 1, 1) to get candidate hand slot; if -1 returns 0. Inner loop iterates hand slots [0..hand_count-1]: for each card checks check_card_field5_is_nonzero==0 AND check_card_has_equip_placement_type==0 AND count_available_monster_slots > 0; if all pass calls eval_equip_bonus_for_slot; if > 6 -> calls resolve_equip_target_slot_for_player; found -> returns 1. If eval_equip_bonus_for_slot is in 4..6 range also returns 1 (secondary path). No match -> returns 0. indeg=0; fn_ptr 0x080b88c1 (points to 0x080b88c0, not this function) used via DAT_080b89e8 by scan_hand_for_best_equip_target_slot.
@ 
@ Constants:
@ - LP_BLOCK_BIT=bit17 of [gP1LifePoints+player_id*0x868+0x11c]
@ - BONUS_HIGH_THRESHOLD=6 (eval_equip_bonus_for_slot > 6 -> resolve)
@ - BONUS_LOW_THRESHOLD=4 (eval_equip_bonus_for_slot > 4 -> also return 1)
@ - PLAYER_STRIDE=0x868
@ - gP1LifePoints=0x0201c4e0
@ - HAND_ZONE_BASE=0x0201c4ec (DAT_080b8a20)
check_hand_equip_target_meets_bonus_6:
    push {r4,r5,r6,r7,lr}                    @ 080b88c4 f0b5
    .hword 0x4657    @ 080b88c6 5746
    .hword 0x464e    @ 080b88c8 4e46
    .hword 0x4645    @ 080b88ca 4546
    push {r5,r6,r7}                          @ 080b88cc e0b4
    sub sp,#0x4                              @ 080b88ce 81b0
    adds r6,r0,#0x0    @ 080b88d0 061c
    ldrb r1,[r6,#0x2]                        @ 080b88d2 b178
    lsls r0,r1,#0x1f    @ 080b88d4 c807
    lsrs r0,r0,#0x1f    @ 080b88d6 c00f
    movs r5,#0x1    @ 080b88d8 0125
    subs r0,r5,r0    @ 080b88da 281a
    movs r1,#0x0    @ 080b88dc 0021
    movs r2,#0x1    @ 080b88de 0122
    bl count_equip_placements_with_chain_check @ 080b88e0 7af7eaff
    cmp r0,#0x0                              @ 080b88e4 0028
    bgt LAB_080b88ea                         @ 080b88e6 00dc
    b LAB_080b8a0c                           @ 080b88e8 90e0
LAB_080b88ea:
    ldr r4, PTR_gP1LifePoints_080b89e0       @ 080b88ea 3d4c
    ldrb r3,[r6,#0x2]                        @ 080b88ec b378
    lsls r2,r3,#0x1f    @ 080b88ee da07
    lsrs r1,r2,#0x1f    @ 080b88f0 d10f
    adds r0,r5,#0x0    @ 080b88f2 281c
    ands r0,r1    @ 080b88f4 0840
    ldr r1, DAT_080b89e4                     @ 080b88f6 3b49
    .hword 0x4688    @ 080b88f8 8846
    .hword 0x4643    @ 080b88fa 4346
    muls r3,r0    @ 080b88fc 4343
    adds r0,r3,#0x0    @ 080b88fe 181c
    movs r3,#0x8e    @ 080b8900 8e23
    lsls r3,r3,#0x1    @ 080b8902 5b00
    adds r1,r4,r3    @ 080b8904 e118
    adds r0,r0,r1    @ 080b8906 4018
    ldr r0,[r0,#0x0]                         @ 080b8908 0068
    lsrs r0,r0,#0x11    @ 080b890a 400c
    ands r0,r5    @ 080b890c 2840
    cmp r0,#0x0                              @ 080b890e 0028
    bne LAB_080b8a0c                         @ 080b8910 7cd1
    lsrs r0,r2,#0x1f    @ 080b8912 d00f
    ldr r1, DAT_080b89e8                     @ 080b8914 3449
    movs r2,#0x1    @ 080b8916 0122
    movs r3,#0x1    @ 080b8918 0123
    bl scan_hand_for_best_equip_target_slot  @ 080b891a fcf7e5ff
    str r0,[sp,#0x0]                         @ 080b891e 0090
    cmp r0,#0x0                              @ 080b8920 0028
    blt LAB_080b8a0c                         @ 080b8922 73db
    movs r7,#0x0    @ 080b8924 0027
    ldrb r2,[r6,#0x2]                        @ 080b8926 b278
    lsls r1,r2,#0x1f    @ 080b8928 d107
    lsrs r1,r1,#0x1f    @ 080b892a c90f
    adds r0,r5,#0x0    @ 080b892c 281c
    ands r0,r1    @ 080b892e 0840
    .hword 0x4641    @ 080b8930 4146
    muls r1,r0    @ 080b8932 4143
    adds r0,r1,#0x0    @ 080b8934 081c
    adds r1,r4,#0x0    @ 080b8936 211c
    adds r1,#0xc    @ 080b8938 0c31
    adds r0,r0,r1    @ 080b893a 4018
    ldr r0,[r0,#0x0]                         @ 080b893c 0068
    cmp r7,r0                                @ 080b893e 8742
    bcs LAB_080b8a0c                         @ 080b8940 64d2
    movs r3,#0x1    @ 080b8942 0123
    .hword 0x4699    @ 080b8944 9946
    movs r0,#0x90    @ 080b8946 9020
    lsls r0,r0,#0x1    @ 080b8948 4000
    adds r0,r0,r4    @ 080b894a 0019
    .hword 0x4682    @ 080b894c 8246
LAB_080b894e:
    lsls r0,r2,#0x1f    @ 080b894e d007
    lsrs r0,r0,#0x1f    @ 080b8950 c00f
    .hword 0x4649    @ 080b8952 4946
    ands r1,r0    @ 080b8954 0140
    lsls r5,r7,#0x2    @ 080b8956 bd00
    .hword 0x4640    @ 080b8958 4046
    muls r0,r1    @ 080b895a 4843
    adds r0,r5,r0    @ 080b895c 2818
    add r0,r10                               @ 080b895e 5044
    ldr r0,[r0,#0x0]                         @ 080b8960 0068
    lsls r0,r0,#0x13    @ 080b8962 c004
    lsrs r4,r0,#0x13    @ 080b8964 c40c
    ldr r1,[sp,#0x0]                         @ 080b8966 0099
    cmp r7,r1                                @ 080b8968 8f42
    beq LAB_080b89f0                         @ 080b896a 41d0
    adds r0,r4,#0x0    @ 080b896c 201c
    bl check_card_field5_is_nonzero          @ 080b896e 92f7ebf9
    cmp r0,#0x0                              @ 080b8972 0028
    beq LAB_080b89f0                         @ 080b8974 3cd0
    adds r0,r4,#0x0    @ 080b8976 201c
    bl check_card_has_equip_placement_type   @ 080b8978 93f76ef8
    cmp r0,#0x0                              @ 080b897c 0028
    bne LAB_080b89f0                         @ 080b897e 37d1
    ldrb r2,[r6,#0x2]                        @ 080b8980 b278
    lsls r0,r2,#0x1f    @ 080b8982 d007
    lsrs r0,r0,#0x1f    @ 080b8984 c00f
    bl count_available_monster_slots         @ 080b8986 7af717fe
    cmp r0,#0x0                              @ 080b898a 0028
    beq LAB_080b89f0                         @ 080b898c 30d0
    ldrb r0,[r6,#0x2]                        @ 080b898e b078
    lsls r3,r0,#0x1f    @ 080b8990 c307
    lsrs r0,r3,#0x1f    @ 080b8992 d80f
    adds r2,r0,#0x0    @ 080b8994 021c
    .hword 0x4649    @ 080b8996 4946
    ands r1,r2    @ 080b8998 1140
    .hword 0x4642    @ 080b899a 4246
    muls r2,r1    @ 080b899c 4a43
    adds r1,r2,#0x0    @ 080b899e 111c
    adds r1,r5,r1    @ 080b89a0 6918
    add r1,r10                               @ 080b89a2 5144
    ldr r1,[r1,#0x0]                         @ 080b89a4 0968
    lsls r1,r1,#0x2    @ 080b89a6 8900
    lsrs r1,r1,#0x18    @ 080b89a8 090e
    lsls r1,r1,#0x1    @ 080b89aa 4900
    adds r3,r0,#0x0    @ 080b89ac 031c
    .hword 0x464a    @ 080b89ae 4a46
    ands r2,r3    @ 080b89b0 1a40
    .hword 0x4643    @ 080b89b2 4346
    muls r3,r2    @ 080b89b4 5343
    adds r2,r3,#0x0    @ 080b89b6 1a1c
    adds r2,r5,r2    @ 080b89b8 aa18
    add r2,r10                               @ 080b89ba 5244
    ldr r2,[r2,#0x0]                         @ 080b89bc 1268
    lsls r2,r2,#0x12    @ 080b89be 9204
    lsrs r2,r2,#0x1f    @ 080b89c0 d20f
    adds r1,r1,r2    @ 080b89c2 8918
    bl eval_equip_bonus_for_slot             @ 080b89c4 7ef7f4fe
    cmp r0,#0x6                              @ 080b89c8 0628
    ble LAB_080b89ec                         @ 080b89ca 0fdd
    ldrb r1,[r6,#0x2]                        @ 080b89cc b178
    lsls r0,r1,#0x1f    @ 080b89ce c807
    lsrs r0,r0,#0x1f    @ 080b89d0 c00f
    movs r1,#0x1    @ 080b89d2 0121
    bl resolve_equip_target_slot_for_player  @ 080b89d4 f4f76afd
    cmp r0,#0x0                              @ 080b89d8 0028
    blt LAB_080b89f0                         @ 080b89da 09db
LAB_080b89dc:
    movs r0,#0x1    @ 080b89dc 0120
    b LAB_080b8a0e                           @ 080b89de 16e0
PTR_gP1LifePoints_080b89e0:
    .word  gP1LifePoints                  @ 080b89e0 e0c40102
DAT_080b89e4:
    .word  0x00000868                     @ 080b89e4 68080000
DAT_080b89e8:
    .word  0x080b88c1                     @ 080b89e8 c1880b08
LAB_080b89ec:
    cmp r0,#0x4                              @ 080b89ec 0428
    bgt LAB_080b89dc                         @ 080b89ee f5dc
LAB_080b89f0:
    adds r7,#0x1    @ 080b89f0 0137
    ldrb r2,[r6,#0x2]                        @ 080b89f2 b278
    lsls r1,r2,#0x1f    @ 080b89f4 d107
    lsrs r1,r1,#0x1f    @ 080b89f6 c90f
    .hword 0x4648    @ 080b89f8 4846
    ands r0,r1    @ 080b89fa 0840
    .hword 0x4643    @ 080b89fc 4346
    muls r3,r0    @ 080b89fe 4343
    adds r0,r3,#0x0    @ 080b8a00 181c
    ldr r1, DAT_080b8a20                     @ 080b8a02 0749
    adds r0,r0,r1    @ 080b8a04 4018
    ldr r0,[r0,#0x0]                         @ 080b8a06 0068
    cmp r7,r0                                @ 080b8a08 8742
    bcc LAB_080b894e                         @ 080b8a0a a0d3
LAB_080b8a0c:
    movs r0,#0x0    @ 080b8a0c 0020
LAB_080b8a0e:
    add sp,#0x4                              @ 080b8a0e 01b0
    pop {r3,r4,r5}                           @ 080b8a10 38bc
    .hword 0x4698    @ 080b8a12 9846
    .hword 0x46a1    @ 080b8a14 a146
    .hword 0x46aa    @ 080b8a16 aa46
    pop {r4,r5,r6,r7}                        @ 080b8a18 f0bc
    pop {r1}                                 @ 080b8a1a 02bc
    bx r1                                    @ 080b8a1c 0847
    .zero  0x2
DAT_080b8a20:
    .word  0x0201c4ec                     @ 080b8a20 ecc40102

@ Compares equip card owner vs opponent occupied monster zone counts; returns 1 if owner has more. Entry r0=equip_card_zone_ptr; extracts player_id from [r0+2] bit0. Calls count_occupied_monster_zones(1-player_id) -> r5 (opponent count); then calls count_occupied_monster_zones(player_id) -> r0 (self count). If r5 < r0 (opponent < self) returns 1; otherwise returns 0. Used as precondition predicate for equip AI target selection: equip attack value is maximized when self has more monsters than opponent. indeg=0; no direct bl callers.
@ 
@ Constants:
@ - (none beyond APCS calling convention)
check_equip_owner_has_more_occupied_monster_zones:
    push {r4,r5,lr}                          @ 080b8a24 30b5
    adds r4,r0,#0x0    @ 080b8a26 041c
    ldrb r0,[r4,#0x2]                        @ 080b8a28 a078
    lsls r1,r0,#0x1f    @ 080b8a2a c107
    lsrs r1,r1,#0x1f    @ 080b8a2c c90f
    movs r0,#0x1    @ 080b8a2e 0120
    subs r0,r0,r1    @ 080b8a30 401a
    bl count_occupied_monster_zones          @ 080b8a32 7af7a9fb
    adds r5,r0,#0x0    @ 080b8a36 051c
    ldrb r4,[r4,#0x2]                        @ 080b8a38 a478
    lsls r0,r4,#0x1f    @ 080b8a3a e007
    lsrs r0,r0,#0x1f    @ 080b8a3c c00f
    bl count_occupied_monster_zones          @ 080b8a3e 7af7a3fb
    movs r1,#0x0    @ 080b8a42 0021
    cmp r5,r0                                @ 080b8a44 8542
    bge LAB_080b8a4a                         @ 080b8a46 00da
    movs r1,#0x1    @ 080b8a48 0121
LAB_080b8a4a:
    adds r0,r1,#0x0    @ 080b8a4a 081c
    pop {r4,r5}                              @ 080b8a4c 30bc
    pop {r1}                                 @ 080b8a4e 02bc
    bx r1                                    @ 080b8a50 0847
    ROM_INCBIN 0xb8a52, 0x2182

@ Checks whether a hand equip target with bonus value greater than 4 exists (sibling FUN_080b88c4 uses threshold 6, also has count_equip_placements precondition). Entry r0=equip_card_zone_ptr. Checks gP1LifePoints[player_id*0x868+0x11c] bit17; if set (equip activation blocked) returns 0. Inner loop counter r8 iterates [0..hand_count-1] (r8 initialized to 0 at LAB_080bac10, not a caller-set parameter). For each hand card: checks check_card_field5_is_nonzero==0 AND check_card_has_equip_placement_type==0; if both pass calls eval_equip_bonus_for_slot; if > 4 -> returns 1. Loop ends without match -> returns 0. Looser than check_hand_equip_target_meets_bonus_6: no count_equip_placements precondition, no count_available_monster_slots check, no resolve_equip_target_slot_for_player. indeg=0; no direct bl callers.
@ 
@ Constants:
@ - BONUS_THRESHOLD=4 (eval_equip_bonus_for_slot > 4 -> return 1)
@ - LP_BLOCK_BIT=bit17 of [gP1LifePoints+player_id*0x868+0x11c]
@ - PLAYER_STRIDE=0x868
@ - gP1LifePoints=0x0201c4e0 (PTR_gP1LifePoints_080bac04)
@ - HAND_ZONE_BASE=0x0201c4ec (DAT_080bacc8)
check_hand_equip_target_meets_bonus_4:
    push {r4,r5,r6,r7,lr}                    @ 080babd4 f0b5
    .hword 0x4657    @ 080babd6 5746
    .hword 0x464e    @ 080babd8 4e46
    .hword 0x4645    @ 080babda 4546
    push {r5,r6,r7}                          @ 080babdc e0b4
    adds r6,r0,#0x0    @ 080babde 061c
    ldr r3, PTR_gP1LifePoints_080bac04       @ 080babe0 084b
    ldrb r0,[r6,#0x2]                        @ 080babe2 b078
    lsls r5,r0,#0x1f    @ 080babe4 c507
    movs r2,#0x1    @ 080babe6 0122
    lsrs r0,r5,#0x1f    @ 080babe8 e80f
    ldr r4, DAT_080bac08                     @ 080babea 074c
    muls r0,r4    @ 080babec 6043
    movs r7,#0x8e    @ 080babee 8e27
    lsls r7,r7,#0x1    @ 080babf0 7f00
    adds r1,r3,r7    @ 080babf2 d919
    adds r0,r0,r1    @ 080babf4 4018
    ldr r0,[r0,#0x0]                         @ 080babf6 0068
    lsrs r0,r0,#0x11    @ 080babf8 400c
    ands r0,r2    @ 080babfa 1040
    cmp r0,#0x0                              @ 080babfc 0028
    beq LAB_080bac10                         @ 080babfe 07d0
    b LAB_080bacb6                           @ 080bac00 59e0
    .zero  0x2
PTR_gP1LifePoints_080bac04:
    .word  gP1LifePoints                  @ 080bac04 e0c40102
DAT_080bac08:
    .word  0x00000868                     @ 080bac08 68080000
LAB_080bac0c:
    movs r0,#0x1    @ 080bac0c 0120
    b LAB_080bacb8                           @ 080bac0e 53e0
LAB_080bac10:
    movs r0,#0x0    @ 080bac10 0020
    .hword 0x4680    @ 080bac12 8046
    lsrs r0,r5,#0x1f    @ 080bac14 e80f
    ands r2,r0    @ 080bac16 0240
    adds r0,r2,#0x0    @ 080bac18 101c
    muls r0,r4    @ 080bac1a 6043
    adds r1,r3,#0x0    @ 080bac1c 191c
    adds r1,#0xc    @ 080bac1e 0c31
    adds r0,r0,r1    @ 080bac20 4018
    ldr r0,[r0,#0x0]                         @ 080bac22 0068
    cmp r8,r0                                @ 080bac24 8045
    bcs LAB_080bacb6                         @ 080bac26 46d2
    movs r7,#0x1    @ 080bac28 0127
    .hword 0x46b9    @ 080bac2a b946
    adds r7,r4,#0x0    @ 080bac2c 271c
    movs r0,#0x90    @ 080bac2e 9020
    lsls r0,r0,#0x1    @ 080bac30 4000
    adds r0,r0,r3    @ 080bac32 c018
    .hword 0x4682    @ 080bac34 8246
LAB_080bac36:
    ldrb r1,[r6,#0x2]                        @ 080bac36 b178
    lsls r0,r1,#0x1f    @ 080bac38 c807
    lsrs r0,r0,#0x1f    @ 080bac3a c00f
    .hword 0x4649    @ 080bac3c 4946
    ands r1,r0    @ 080bac3e 0140
    .hword 0x4640    @ 080bac40 4046
    lsls r5,r0,#0x2    @ 080bac42 8500
    adds r0,r1,#0x0    @ 080bac44 081c
    muls r0,r7    @ 080bac46 7843
    adds r0,r5,r0    @ 080bac48 2818
    add r0,r10                               @ 080bac4a 5044
    ldr r0,[r0,#0x0]                         @ 080bac4c 0068
    lsls r0,r0,#0x13    @ 080bac4e c004
    lsrs r4,r0,#0x13    @ 080bac50 c40c
    adds r0,r4,#0x0    @ 080bac52 201c
    bl check_card_field5_is_nonzero          @ 080bac54 90f778f8
    cmp r0,#0x0                              @ 080bac58 0028
    beq LAB_080bac9c                         @ 080bac5a 1fd0
    adds r0,r4,#0x0    @ 080bac5c 201c
    bl check_card_has_equip_placement_type   @ 080bac5e 90f7fbfe
    cmp r0,#0x0                              @ 080bac62 0028
    bne LAB_080bac9c                         @ 080bac64 1ad1
    ldrb r1,[r6,#0x2]                        @ 080bac66 b178
    lsls r3,r1,#0x1f    @ 080bac68 cb07
    lsrs r0,r3,#0x1f    @ 080bac6a d80f
    adds r2,r0,#0x0    @ 080bac6c 021c
    .hword 0x4649    @ 080bac6e 4946
    ands r1,r2    @ 080bac70 1140
    muls r1,r7    @ 080bac72 7943
    adds r1,r5,r1    @ 080bac74 6918
    add r1,r10                               @ 080bac76 5144
    ldr r1,[r1,#0x0]                         @ 080bac78 0968
    lsls r1,r1,#0x2    @ 080bac7a 8900
    lsrs r1,r1,#0x18    @ 080bac7c 090e
    lsls r1,r1,#0x1    @ 080bac7e 4900
    adds r3,r0,#0x0    @ 080bac80 031c
    .hword 0x464a    @ 080bac82 4a46
    ands r2,r3    @ 080bac84 1a40
    muls r2,r7    @ 080bac86 7a43
    adds r2,r5,r2    @ 080bac88 aa18
    add r2,r10                               @ 080bac8a 5244
    ldr r2,[r2,#0x0]                         @ 080bac8c 1268
    lsls r2,r2,#0x12    @ 080bac8e 9204
    lsrs r2,r2,#0x1f    @ 080bac90 d20f
    adds r1,r1,r2    @ 080bac92 8918
    bl eval_equip_bonus_for_slot             @ 080bac94 7cf78cfd
    cmp r0,#0x4                              @ 080bac98 0428
    bgt LAB_080bac0c                         @ 080bac9a b7dc
LAB_080bac9c:
    movs r0,#0x1    @ 080bac9c 0120
    add r8,r0                                @ 080bac9e 8044
    ldrb r0,[r6,#0x2]                        @ 080baca0 b078
    lsls r1,r0,#0x1f    @ 080baca2 c107
    lsrs r1,r1,#0x1f    @ 080baca4 c90f
    .hword 0x4648    @ 080baca6 4846
    ands r0,r1    @ 080baca8 0840
    muls r0,r7    @ 080bacaa 7843
    ldr r1, DAT_080bacc8                     @ 080bacac 0649
    adds r0,r0,r1    @ 080bacae 4018
    ldr r0,[r0,#0x0]                         @ 080bacb0 0068
    cmp r8,r0                                @ 080bacb2 8045
    bcc LAB_080bac36                         @ 080bacb4 bfd3
LAB_080bacb6:
    movs r0,#0x0    @ 080bacb6 0020
LAB_080bacb8:
    pop {r3,r4,r5}                           @ 080bacb8 38bc
    .hword 0x4698    @ 080bacba 9846
    .hword 0x46a1    @ 080bacbc a146
    .hword 0x46aa    @ 080bacbe aa46
    pop {r4,r5,r6,r7}                        @ 080bacc0 f0bc
    pop {r1}                                 @ 080bacc2 02bc
    bx r1                                    @ 080bacc4 0847
    .zero  0x2
DAT_080bacc8:
    .word  0x0201c4ec                     @ 080bacc8 ecc40102
    ROM_INCBIN 0xbaccc, 0x30

@ Wrapper that calls count_occupied_monster_zones then discards the result and returns 0. Extracts player_id from zone_ptr->byte[2] bit0 via lsls/lsrs #0x1f. Calls count_occupied_monster_zones(player_id); ignores return value; movs r0,#0 fixes return to 0. Exits via pop{r1}+bx r1 (Sub-case E). For callsites that need zone_ptr as entry param but only need the count side-effect.
@ 
@ Constants:
@ - (no non-trivial literals)
@ 
@ Inputs: r0=ptr zone_ptr (field zone ptr, byte[2] bit0=player_id)
@ Returns: r0=u32 0 (fixed)
@ Side effects: calls count_occupied_monster_zones(player_id); result unused
invoke_count_occupied_monster_zones:
    push {lr}                                @ 080bacfc 00b5
    ldrb r0,[r0,#0x2]                        @ 080bacfe 8078
    lsls r0,r0,#0x1f    @ 080bad00 c007
    lsrs r0,r0,#0x1f    @ 080bad02 c00f
    bl count_occupied_monster_zones          @ 080bad04 78f740fa
    movs r0,#0x0    @ 080bad08 0020
    pop {r1}                                 @ 080bad0a 02bc
    bx r1                                    @ 080bad0c 0847
    .zero  0x2

@ Checks whether the opponent's LP is below the threshold (occupied_zone_count * 300). Sums both players' occupied field zone counts via count_occupied_all_field_zones(0) and (1), adds fields at gP1LifePoints+0xc and +0x874, multiplies total by 300 (shift chain). Loads opponent LP via opponent_id*0x868 offset; returns 1 if LP <= total*300, else 0. Exits via pop{r1}+bx r1 (Sub-case E).
@ 
@ Constants:
@ - gP1LifePoints = 0x0201c4e0 (DWORD_080bad60)
@ - FIELD_COUNT_OFFSET_A = 0xc (gP1LifePoints+0xc extra count field A)
@ - FIELD_COUNT_OFFSET_B = 0x874 (gP1LifePoints+0x874, DWORD_080bad64)
@ - PLAYER_STRIDE = 0x868 (DWORD_080bad68)
@ - LP_FACTOR = 300 (lsls+adds+lsls-subs multiply chain)
@ 
@ Inputs: r0=ptr zone_ptr (field zone ptr, byte[2] bit0=player_id)
@ Returns: r0=u32 flag (1=LP <= zone_count*300, 0=LP sufficient)
@ Side effects: none (read-only)
check_lp_below_zone_count_threshold:
    push {r4,r5,r6,lr}                       @ 080bad10 70b5
    adds r5,r0,#0x0    @ 080bad12 051c
    movs r0,#0x0    @ 080bad14 0020
    bl count_occupied_all_field_zones        @ 080bad16 78f7f9f9
    adds r4,r0,#0x0    @ 080bad1a 041c
    movs r0,#0x1    @ 080bad1c 0120
    bl count_occupied_all_field_zones        @ 080bad1e 78f7f5f9
    adds r4,r4,r0    @ 080bad22 2418
    ldr r3, DWORD_080bad60                   @ 080bad24 0e4b
    ldr r0,[r3,#0xc]                         @ 080bad26 d868
    adds r4,r4,r0    @ 080bad28 2418
    ldr r1, DWORD_080bad64                   @ 080bad2a 0e49
    adds r0,r3,r1    @ 080bad2c 5818
    ldr r0,[r0,#0x0]                         @ 080bad2e 0068
    adds r4,r4,r0    @ 080bad30 2418
    movs r6,#0x0    @ 080bad32 0026
    ldrb r5,[r5,#0x2]                        @ 080bad34 ad78
    lsls r0,r5,#0x1f    @ 080bad36 e807
    lsrs r0,r0,#0x1f    @ 080bad38 c00f
    movs r1,#0x1    @ 080bad3a 0121
    eors r0,r1    @ 080bad3c 4840
    ldr r1, DWORD_080bad68                   @ 080bad3e 0a49
    adds r2,r0,#0x0    @ 080bad40 021c
    muls r2,r1    @ 080bad42 4a43
    adds r2,r2,r3    @ 080bad44 d218
    lsls r0,r4,#0x2    @ 080bad46 a000
    adds r0,r0,r4    @ 080bad48 0019
    lsls r1,r0,#0x4    @ 080bad4a 0101
    subs r1,r1,r0    @ 080bad4c 091a
    lsls r1,r1,#0x2    @ 080bad4e 8900
    ldr r0,[r2,#0x0]                         @ 080bad50 1068
    cmp r0,r1                                @ 080bad52 8842
    bgt LAB_080bad58                         @ 080bad54 00dc
    movs r6,#0x1    @ 080bad56 0126
LAB_080bad58:
    adds r0,r6,#0x0    @ 080bad58 301c
    pop {r4,r5,r6}                           @ 080bad5a 70bc
    pop {r1}                                 @ 080bad5c 02bc
    bx r1                                    @ 080bad5e 0847
DWORD_080bad60:
    .word  gP1LifePoints                  @ 080bad60 e0c40102
DWORD_080bad64:
    .word  0x00000874                     @ 080bad64 74080000
DWORD_080bad68:
    .word  0x00000868                     @ 080bad68 68080000

@ Equip activation eligibility predicate; routes between two validation paths based on zone_ptr[+3] bits[5:4] flag. Path A (flags==0): delegates to check_card_pair_slot_count_eligible for card pair slot count check. Path B (flags!=0): iterates 5 effect zone slots [0..4] checking: (1) slot card_id upper 13 bits non-zero (valid card); (2) slot [+8] == 0 (unoccupied); (3) specific bit7 flag == 1. All satisfied -> return 1; no match after iteration -> return 0. No external writes; pure predicate.
@ 
@ Constants:
@ - SLOT_FLAG_MASK = 0x30 (bits[5:4] of zone_ptr[+3])
@ - SLOT_COUNT = 5 ([0..4])
@ - gDuelEffectZones = 0x0201c510
@ - PLAYER_STRIDE = 0x868
check_equip_eligible_by_slot_flag_or_pair_count:
    push {r4,r5,r6,r7,lr}                    @ 080bad6c f0b5
    .hword 0x4647    @ 080bad6e 4746
    push {r7}                                @ 080bad70 80b4
    adds r2,r0,#0x0    @ 080bad72 021c
    movs r0,#0x30    @ 080bad74 3020
    ldrb r3,[r2,#0x3]                        @ 080bad76 d378
    ands r0,r3    @ 080bad78 1840
    cmp r0,#0x0                              @ 080bad7a 0028
    bne LAB_080bad8a                         @ 080bad7c 05d1
    adds r0,r2,#0x0    @ 080bad7e 101c
    bl check_card_pair_slot_count_eligible   @ 080bad80 fcf7b0fc
    b LAB_080bade2                           @ 080bad84 2de0
LAB_080bad86:
    movs r0,#0x1    @ 080bad86 0120
    b LAB_080bade2                           @ 080bad88 2be0
LAB_080bad8a:
    movs r6,#0x0    @ 080bad8a 0026
    ldr r7, DWORD_080badec                   @ 080bad8c 174f
    ldrb r2,[r2,#0x2]                        @ 080bad8e 9278
    lsls r3,r2,#0x1f    @ 080bad90 d307
    movs r4,#0x1    @ 080bad92 0124
    ldr r5, DWORD_080badf0                   @ 080bad94 164d
    .hword 0x46b8    @ 080bad96 b846
    movs r0,#0x10    @ 080bad98 1020
    adds r0,r0,r7    @ 080bad9a c019
    .hword 0x4684    @ 080bad9c 8446
    movs r2,#0x0    @ 080bad9e 0022
LAB_080bada0:
    lsrs r1,r3,#0x1f    @ 080bada0 d90f
    adds r0,r4,#0x0    @ 080bada2 201c
    ands r0,r1    @ 080bada4 0840
    muls r0,r5    @ 080bada6 6843
    adds r0,r2,r0    @ 080bada8 1018
    add r0,r8                                @ 080badaa 4044
    ldr r0,[r0,#0x0]                         @ 080badac 0068
    lsls r0,r0,#0x13    @ 080badae c004
    cmp r0,#0x0                              @ 080badb0 0028
    beq LAB_080badd8                         @ 080badb2 11d0
    adds r0,r4,#0x0    @ 080badb4 201c
    ands r0,r1    @ 080badb6 0840
    muls r0,r5    @ 080badb8 6843
    adds r0,r2,r0    @ 080badba 1018
    adds r0,r0,r7    @ 080badbc c019
    ldrh r0,[r0,#0x8]                        @ 080badbe 0089
    cmp r0,#0x0                              @ 080badc0 0028
    bne LAB_080badd8                         @ 080badc2 09d1
    adds r0,r4,#0x0    @ 080badc4 201c
    ands r0,r1    @ 080badc6 0840
    muls r0,r5    @ 080badc8 6843
    adds r0,r2,r0    @ 080badca 1018
    add r0,r12                               @ 080badcc 6044
    ldr r0,[r0,#0x0]                         @ 080badce 0068
    lsrs r0,r0,#0x7    @ 080badd0 c009
    ands r0,r4    @ 080badd2 2040
    cmp r0,#0x0                              @ 080badd4 0028
    bne LAB_080bad86                         @ 080badd6 d6d1
LAB_080badd8:
    adds r2,#0x14    @ 080badd8 1432
    adds r6,#0x1    @ 080badda 0136
    cmp r6,#0x4                              @ 080baddc 042e
    ble LAB_080bada0                         @ 080badde dfdd
    movs r0,#0x0    @ 080bade0 0020
LAB_080bade2:
    pop {r3}                                 @ 080bade2 08bc
    .hword 0x4698    @ 080bade4 9846
    pop {r4,r5,r6,r7}                        @ 080bade6 f0bc
    pop {r1}                                 @ 080bade8 02bc
    bx r1                                    @ 080badea 0847
DWORD_080badec:
    .word  0x0201c510                     @ 080badec 10c50102
DWORD_080badf0:
    .word  0x00000868                     @ 080badf0 68080000

@ Equip activation composite eligibility predicate for Rapid-Fire Magician (0x1964) and Dark Eradicator Warlock (0x1982) special effect zone availability check. Flow: (1) calls dispatch_equip_lp_delta_by_card_id to compute LP delta for both players into stack; (2) reads own current LP + delta; if <= 0 returns 1 (LP insufficient -> effect available); (3) calls count_available_effect_zones(opponent, 0x1964, -1); non-zero -> return 1; (4) calls count_available_effect_zones(self, 0x1982, -1); non-zero -> return 1; (5) both zero -> return 0. Used by AI to evaluate equip activation for these two specific spell caster cards.
@ 
@ Constants:
@ - CARD_Rapid_Fire_Magician = 0x1964
@ - CARD_Dark_Eradicator_Warlock = 0x1982
@ - gP1LifePoints = 0x0201c4e0
@ - PLAYER_STRIDE = 0x868
@ - mode = -1 (rsbs r4,r4,#0)
check_equip_effect_zone_eligible_for_rapid_fire_and_warlock:
    push {r4,r5,lr}                          @ 080badf4 30b5
    sub sp,#0x8                              @ 080badf6 82b0
    adds r5,r0,#0x0    @ 080badf8 051c
    .hword 0x4669    @ 080badfa 6946
    bl dispatch_equip_lp_delta_by_card_id    @ 080badfc a9f740fd
    ldr r3, PTR_gP1LifePoints_080bae50       @ 080bae00 134b
    ldrb r0,[r5,#0x2]                        @ 080bae02 a878
    lsls r4,r0,#0x1f    @ 080bae04 c407
    lsrs r1,r4,#0x1f    @ 080bae06 e10f
    movs r0,#0x1    @ 080bae08 0120
    subs r1,r0,r1    @ 080bae0a 411a
    ands r1,r0    @ 080bae0c 0140
    ldr r2, DAT_080bae54                     @ 080bae0e 114a
    muls r2,r1    @ 080bae10 4a43
    adds r2,r2,r3    @ 080bae12 d218
    lsrs r1,r4,#0x1f    @ 080bae14 e10f
    subs r0,r0,r1    @ 080bae16 401a
    lsls r0,r0,#0x2    @ 080bae18 8000
    add r0,sp                                @ 080bae1a 6844
    ldr r1,[r2,#0x0]                         @ 080bae1c 1168
    ldr r0,[r0,#0x0]                         @ 080bae1e 0068
    adds r1,r1,r0    @ 080bae20 0918
    cmp r1,#0x0                              @ 080bae22 0029
    ble LAB_080bae60                         @ 080bae24 1cdd
    lsrs r0,r4,#0x1f    @ 080bae26 e00f
    ldr r1, DAT_080bae58                     @ 080bae28 0b49
    movs r4,#0x1    @ 080bae2a 0124
    rsbs r4,r4,#0    @ 080bae2c 6442
    adds r2,r4,#0x0    @ 080bae2e 221c
    bl count_available_effect_zones          @ 080bae30 77f710fc
    cmp r0,#0x0                              @ 080bae34 0028
    bne LAB_080bae60                         @ 080bae36 13d1
    ldrb r5,[r5,#0x2]                        @ 080bae38 ad78
    lsls r0,r5,#0x1f    @ 080bae3a e807
    lsrs r0,r0,#0x1f    @ 080bae3c c00f
    ldr r1, DAT_080bae5c                     @ 080bae3e 0749
    adds r2,r4,#0x0    @ 080bae40 221c
    bl count_available_effect_zones          @ 080bae42 77f707fc
    cmp r0,#0x0                              @ 080bae46 0028
    bne LAB_080bae60                         @ 080bae48 0ad1
    movs r0,#0x0    @ 080bae4a 0020
    b LAB_080bae62                           @ 080bae4c 09e0
    .zero  0x2
PTR_gP1LifePoints_080bae50:
    .word  gP1LifePoints                  @ 080bae50 e0c40102
DAT_080bae54:
    .word  0x00000868                     @ 080bae54 68080000
DAT_080bae58:
    .word  0x00001964                     @ 080bae58 64190000
DAT_080bae5c:
    .word  0x00001982                     @ 080bae5c 82190000
LAB_080bae60:
    movs r0,#0x1    @ 080bae60 0120
LAB_080bae62:
    add sp,#0x8                              @ 080bae62 02b0
    pop {r4,r5}                              @ 080bae64 30bc
    pop {r1}                                 @ 080bae66 02bc
    bx r1                                    @ 080bae68 0847
    .zero  0x2

@ Determines player_side and zone_id from get_card_extended_stat_field6 value (0x16 -> zone_id=0x17d4; 0x17 -> zone_id=0x17c6; default -> zone_id=0x1771). Calls count_available_effect_zones(player_side, zone_id, -1); if count > 0 returns 1 (slot available); else falls back to check_card_special_summon_eligible_full (FUN_0805bcf0). r0=ptr card_slot_ptr. Returns u32: 1=summon eligible, 0=not. Constants: field6_vals=0x16/0x17, zone_ids=0x17d4/0x17c6/0x1771, quota=-1. Callers: FUN_080b499c, FUN_080baed0 (duel_field activation eval chain).
check_card_summon_eligible_by_field6:
    push {r4,lr}                             @ 080bae6c 10b5
    adds r4,r0,#0x0    @ 080bae6e 041c
    ldrh r0,[r4,#0x0]                        @ 080bae70 2088
    bl get_card_extended_stat_field6         @ 080bae72 33f0c1ff
    cmp r0,#0x16                             @ 080bae76 1628
    bne LAB_080bae8c                         @ 080bae78 08d1
    ldrb r0,[r4,#0x2]                        @ 080bae7a a078
    lsls r1,r0,#0x1f    @ 080bae7c c107
    lsrs r1,r1,#0x1f    @ 080bae7e c90f
    movs r0,#0x1    @ 080bae80 0120
    subs r0,r0,r1    @ 080bae82 401a
    ldr r1, DAT_080bae88                     @ 080bae84 0049
    b LAB_080baeb0                           @ 080bae86 13e0
DAT_080bae88:
    .word  0x000017d4                     @ 080bae88 d4170000
LAB_080bae8c:
    ldrh r0,[r4,#0x0]                        @ 080bae8c 2088
    bl get_card_extended_stat_field6         @ 080bae8e 33f0b3ff
    cmp r0,#0x17                             @ 080bae92 1728
    bne LAB_080baea8                         @ 080bae94 08d1
    ldrb r0,[r4,#0x2]                        @ 080bae96 a078
    lsls r1,r0,#0x1f    @ 080bae98 c107
    lsrs r1,r1,#0x1f    @ 080bae9a c90f
    movs r0,#0x1    @ 080bae9c 0120
    subs r0,r0,r1    @ 080bae9e 401a
    ldr r1, DAT_080baea4                     @ 080baea0 0049
    b LAB_080baeb0                           @ 080baea2 05e0
DAT_080baea4:
    .word  0x000017c6                     @ 080baea4 c6170000
LAB_080baea8:
    ldrb r1,[r4,#0x2]                        @ 080baea8 a178
    lsls r0,r1,#0x1f    @ 080baeaa c807
    lsrs r0,r0,#0x1f    @ 080baeac c00f
    ldr r1, DAT_080baec0                     @ 080baeae 0449
LAB_080baeb0:
    movs r2,#0x1    @ 080baeb0 0122
    rsbs r2,r2,#0    @ 080baeb2 5242
    bl count_available_effect_zones          @ 080baeb4 77f7cefb
    cmp r0,#0x0                              @ 080baeb8 0028
    beq LAB_080baec4                         @ 080baeba 03d0
    movs r0,#0x1    @ 080baebc 0120
    b LAB_080baeca                           @ 080baebe 04e0
DAT_080baec0:
    .word  0x00001771                     @ 080baec0 71170000
LAB_080baec4:
    adds r0,r4,#0x0    @ 080baec4 201c
    bl check_card_special_summon_eligible_full @ 080baec6 a0f713ff
LAB_080baeca:
    pop {r4}                                 @ 080baeca 10bc
    pop {r1}                                 @ 080baecc 02bc
    bx r1                                    @ 080baece 0847

@ 被 FUN_080bb35c (scan_all_effect_zone_entries_for_equip_activation) 以及另一 sibling 调用 (indeg>=2). 入口 r0=player_id [0..1], r1=entry_ptr (指向 0x09e483b0 pool 的一个 8 字节条目; entry[0]=target_card_id). 函数体: (1) 从 entry[0] 读 target_card_id -> 内部 r9; (2) 以 r8=player_id&1 和 r10=1 为内部循环控制量, 遍历 gDuelFieldSlots[player*0x868] slot 0..0xa (11 个格): 对每格检查 slot[0].bits[12..0]==r9 (card_id 匹配); (3) 匹配时: 检查 slot[+0x10].bit5=0 (非已激活), bit1=0 (非锁定); memset 0x18 字节到 sp 局部区; 写 OAM attr (r2=entry[+4]=sprite_ptr: attr0/attr1/attr2 位域操作); (4) 检查 slot[+8]: 非 0 则调用 eval_equip_activation_for_slot, 否则调用 check_card_zone_activation_blocked; (5) 若通过: check_card_summon_eligible_by_field6; FUN_0810e5d0 (equip chain validation); (6) 成功路径: init_duel_zone_target_slot_refs; 写 [gP1LifePoints+0x1c44]:=player_id / [gP1LifePoints+0x1c38]:=3; 返回 1. 失败路径返回 0. Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, gP1LifePoints=0x0201c4e0, LOOP_MAX=0xa.
try_activate_equip_for_matching_slot:
    push {r4,r5,r6,r7,lr}                    @ 080baed0 f0b5
    .hword 0x4657    @ 080baed2 5746
    .hword 0x464e    @ 080baed4 4e46
    .hword 0x4645    @ 080baed6 4546
    push {r5,r6,r7}                          @ 080baed8 e0b4
    sub sp,#0x20                             @ 080baeda 88b0
    adds r6,r0,#0x0    @ 080baedc 061c
    str r1,[sp,#0x18]                        @ 080baede 0691
    ldr r0,[r1,#0x0]                         @ 080baee0 0868
    .hword 0x4681    @ 080baee2 8146
    movs r7,#0x0    @ 080baee4 0027
    .hword 0x46b0    @ 080baee6 b046
    .hword 0x4641    @ 080baee8 4146
    movs r2,#0x1    @ 080baeea 0122
    ands r1,r2    @ 080baeec 1140
    .hword 0x4688    @ 080baeee 8846
    .hword 0x466c    @ 080baef0 6c46
    .hword 0x4643    @ 080baef2 4346
    str r3,[sp,#0x1c]                        @ 080baef4 0793
    movs r0,#0x0    @ 080baef6 0020
    .hword 0x4682    @ 080baef8 8246
LAB_080baefa:
    ldr r0, DAT_080baf94                     @ 080baefa 2648
    .hword 0x4641    @ 080baefc 4146
    muls r1,r0    @ 080baefe 4143
    adds r0,r1,#0x0    @ 080baf00 081c
    .hword 0x4652    @ 080baf02 5246
    adds r1,r2,r0    @ 080baf04 1118
    ldr r3, DAT_080baf98                     @ 080baf06 244b
    adds r5,r1,r3    @ 080baf08 cd18
    ldr r0,[r5,#0x0]                         @ 080baf0a 2868
    lsls r0,r0,#0x13    @ 080baf0c c004
    lsrs r0,r0,#0x13    @ 080baf0e c00c
    cmp r0,r9                                @ 080baf10 4845
    bne LAB_080bafca                         @ 080baf12 5ad1
    ldr r2, DAT_080baf9c                     @ 080baf14 214a
    adds r0,r1,r2    @ 080baf16 8818
    ldr r1,[r0,#0x0]                         @ 080baf18 0168
    lsrs r0,r1,#0x5    @ 080baf1a 4809
    movs r3,#0x1    @ 080baf1c 0123
    ands r0,r3    @ 080baf1e 1840
    cmp r0,#0x0                              @ 080baf20 0028
    bne LAB_080bafca                         @ 080baf22 52d1
    lsrs r0,r1,#0x1    @ 080baf24 4808
    ands r0,r3    @ 080baf26 1840
    cmp r0,#0x0                              @ 080baf28 0028
    bne LAB_080bafca                         @ 080baf2a 4ed1
    .hword 0x4668    @ 080baf2c 6846
    movs r1,#0x0    @ 080baf2e 0021
    movs r2,#0x18    @ 080baf30 1822
    bl memset                                @ 080baf32 53f043fd
    .hword 0x4648    @ 080baf36 4846
    strh r0,[r4,#0x0]                        @ 080baf38 2080
    ldrb r1,[r4,#0x2]                        @ 080baf3a a178
    movs r2,#0x2    @ 080baf3c 0222
    rsbs r2,r2,#0    @ 080baf3e 5242
    adds r0,r2,#0x0    @ 080baf40 101c
    ands r1,r0    @ 080baf42 0140
    ldr r3,[sp,#0x1c]                        @ 080baf44 079b
    orrs r1,r3    @ 080baf46 1943
    movs r0,#0x1f    @ 080baf48 1f20
    adds r2,r7,#0x0    @ 080baf4a 3a1c
    ands r2,r0    @ 080baf4c 0240
    lsls r2,r2,#0x1    @ 080baf4e 5200
    movs r3,#0x3f    @ 080baf50 3f23
    rsbs r3,r3,#0    @ 080baf52 5b42
    adds r0,r3,#0x0    @ 080baf54 181c
    ands r1,r0    @ 080baf56 0140
    orrs r1,r2    @ 080baf58 1143
    strb r1,[r4,#0x2]                        @ 080baf5a a170
    ldrb r0,[r4,#0x3]                        @ 080baf5c e078
    movs r2,#0x41    @ 080baf5e 4122
    rsbs r2,r2,#0    @ 080baf60 5242
    adds r1,r2,#0x0    @ 080baf62 111c
    ands r0,r1    @ 080baf64 0840
    strb r0,[r4,#0x3]                        @ 080baf66 e070
    ldr r0,[r5,#0x0]                         @ 080baf68 2868
    lsls r1,r0,#0x2    @ 080baf6a 8100
    lsrs r1,r1,#0x18    @ 080baf6c 090e
    lsls r1,r1,#0x1    @ 080baf6e 4900
    lsls r0,r0,#0x12    @ 080baf70 8004
    lsrs r0,r0,#0x1f    @ 080baf72 c00f
    orrs r1,r0    @ 080baf74 0143
    lsls r1,r1,#0x6    @ 080baf76 8901
    ldr r3, DAT_080bafa0                     @ 080baf78 094b
    adds r0,r3,#0x0    @ 080baf7a 181c
    ldrh r2,[r4,#0x4]                        @ 080baf7c a288
    ands r0,r2    @ 080baf7e 1040
    orrs r0,r1    @ 080baf80 0843
    strh r0,[r4,#0x4]                        @ 080baf82 a080
    ldrh r0,[r5,#0x8]                        @ 080baf84 2889
    cmp r0,#0x0                              @ 080baf86 0028
    beq LAB_080bafa4                         @ 080baf88 0cd0
    .hword 0x4668    @ 080baf8a 6846
    movs r1,#0x0    @ 080baf8c 0021
    bl eval_equip_activation_for_slot        @ 080baf8e 9ff727fa
    b LAB_080bafac                           @ 080baf92 0be0
DAT_080baf94:
    .word  0x00000868                     @ 080baf94 68080000
DAT_080baf98:
    .word  0x0201c510                     @ 080baf98 10c50102
DAT_080baf9c:
    .word  0x0201c520                     @ 080baf9c 20c50102
DAT_080bafa0:
    .word  0xffff803f                     @ 080bafa0 3f80ffff
LAB_080bafa4:
    .hword 0x4668    @ 080bafa4 6846
    movs r1,#0x0    @ 080bafa6 0021
    bl check_card_zone_activation_blocked    @ 080bafa8 9ff7e2fa
LAB_080bafac:
    cmp r0,#0x0                              @ 080bafac 0028
    beq LAB_080bafca                         @ 080bafae 0cd0
    .hword 0x4668    @ 080bafb0 6846
    bl check_card_summon_eligible_by_field6  @ 080bafb2 fff75bff
    cmp r0,#0x0                              @ 080bafb6 0028
    bne LAB_080bafca                         @ 080bafb8 07d1
    ldr r3,[sp,#0x18]                        @ 080bafba 069b
    ldr r2,[r3,#0x4]                         @ 080bafbc 5a68
    .hword 0x4668    @ 080bafbe 6846
    movs r1,#0x0    @ 080bafc0 0021
    bl invoke_r2                             @ 080bafc2 53f005fb
    cmp r0,#0x0                              @ 080bafc6 0028
    bne LAB_080bb0b8                         @ 080bafc8 76d1
LAB_080bafca:
    movs r0,#0x14    @ 080bafca 1420
    add r10,r0                               @ 080bafcc 8244
    adds r7,#0x1    @ 080bafce 0137
    cmp r7,#0xa                              @ 080bafd0 0a2f
    ble LAB_080baefa                         @ 080bafd2 92dd
    ldr r2,[sp,#0x18]                        @ 080bafd4 069a
    ldr r1,[r2,#0x0]                         @ 080bafd6 1168
    adds r0,r6,#0x0    @ 080bafd8 301c
    bl find_zone_slot_idx_allowed_for_card   @ 080bafda 7cf757fd
    adds r5,r0,#0x0    @ 080bafde 051c
    cmp r5,#0x0                              @ 080bafe0 002d
    bge LAB_080bafe6                         @ 080bafe2 00da
    b LAB_080bb0e4                           @ 080bafe4 7ee0
LAB_080bafe6:
    adds r0,r6,#0x0    @ 080bafe6 301c
    bl check_effect_zone_available_for_player @ 080bafe8 f4f7aafc
    cmp r0,#0x0                              @ 080bafec 0028
    beq LAB_080bb0e4                         @ 080bafee 79d0
    .hword 0x4668    @ 080baff0 6846
    movs r1,#0x0    @ 080baff2 0021
    movs r2,#0x18    @ 080baff4 1822
    bl memset                                @ 080baff6 53f0e1fc
    .hword 0x466a    @ 080baffa 6a46
    movs r3,#0x1    @ 080baffc 0123
    .hword 0x4698    @ 080baffe 9846
    adds r0,r6,#0x0    @ 080bb000 301c
    ands r0,r3    @ 080bb002 1840
    lsls r3,r5,#0x2    @ 080bb004 ab00
    ldr r1, DAT_080bb0a4                     @ 080bb006 2749
    muls r0,r1    @ 080bb008 4843
    adds r3,r3,r0    @ 080bb00a 1b18
    ldr r7, DAT_080bb0a8                     @ 080bb00c 264f
    adds r3,r3,r7    @ 080bb00e db19
    ldr r0,[r3,#0x0]                         @ 080bb010 1868
    lsls r0,r0,#0x13    @ 080bb012 c004
    lsrs r0,r0,#0x13    @ 080bb014 c00c
    strh r0,[r2,#0x0]                        @ 080bb016 1080
    .hword 0x466c    @ 080bb018 6c46
    movs r0,#0x1    @ 080bb01a 0120
    adds r1,r6,#0x0    @ 080bb01c 311c
    ands r1,r0    @ 080bb01e 0140
    ldrb r2,[r4,#0x2]                        @ 080bb020 a278
    movs r0,#0x2    @ 080bb022 0220
    rsbs r0,r0,#0    @ 080bb024 4042
    ands r0,r2    @ 080bb026 1040
    orrs r0,r1    @ 080bb028 0843
    strb r0,[r4,#0x2]                        @ 080bb02a a070
    .hword 0x466a    @ 080bb02c 6a46
    movs r1,#0x3f    @ 080bb02e 3f21
    rsbs r1,r1,#0    @ 080bb030 4942
    ands r0,r1    @ 080bb032 0840
    movs r1,#0x16    @ 080bb034 1621
    orrs r0,r1    @ 080bb036 0843
    strb r0,[r2,#0x2]                        @ 080bb038 9070
    ldrb r1,[r2,#0x3]                        @ 080bb03a d178
    movs r0,#0x41    @ 080bb03c 4120
    rsbs r0,r0,#0    @ 080bb03e 4042
    ands r0,r1    @ 080bb040 0840
    strb r0,[r2,#0x3]                        @ 080bb042 d070
    ldr r0,[r3,#0x0]                         @ 080bb044 1868
    lsls r1,r0,#0x2    @ 080bb046 8100
    lsrs r1,r1,#0x18    @ 080bb048 090e
    lsls r1,r1,#0x1    @ 080bb04a 4900
    lsls r0,r0,#0x12    @ 080bb04c 8004
    lsrs r0,r0,#0x1f    @ 080bb04e c00f
    orrs r1,r0    @ 080bb050 0143
    lsls r1,r1,#0x6    @ 080bb052 8901
    ldr r0, DAT_080bb0ac                     @ 080bb054 1548
    ldrh r3,[r2,#0x4]                        @ 080bb056 9388
    ands r0,r3    @ 080bb058 1840
    orrs r0,r1    @ 080bb05a 0843
    strh r0,[r2,#0x4]                        @ 080bb05c 9080
    .hword 0x4668    @ 080bb05e 6846
    movs r1,#0x0    @ 080bb060 0021
    bl check_card_zone_activation_blocked    @ 080bb062 9ff785fa
    cmp r0,#0x0                              @ 080bb066 0028
    beq LAB_080bb0e4                         @ 080bb068 3cd0
    .hword 0x4668    @ 080bb06a 6846
    bl check_card_summon_eligible_by_field6  @ 080bb06c fff7fefe
    cmp r0,#0x0                              @ 080bb070 0028
    bne LAB_080bb0e4                         @ 080bb072 37d1
    ldr r0,[sp,#0x18]                        @ 080bb074 0698
    ldr r2,[r0,#0x4]                         @ 080bb076 4268
    .hword 0x4668    @ 080bb078 6846
    movs r1,#0x0    @ 080bb07a 0021
    bl invoke_r2                             @ 080bb07c 53f0a8fa
    cmp r0,#0x0                              @ 080bb080 0028
    beq LAB_080bb0e4                         @ 080bb082 2fd0
    ldr r1, DAT_080bb0b0                     @ 080bb084 0a49
    adds r0,r7,r1    @ 080bb086 7818
    str r6,[r0,#0x0]                         @ 080bb088 0660
    adds r0,r6,#0x0    @ 080bb08a 301c
    movs r1,#0xb    @ 080bb08c 0b21
    adds r2,r5,#0x0    @ 080bb08e 2a1c
    movs r3,#0x3    @ 080bb090 0323
    bl init_duel_zone_target_slot_refs       @ 080bb092 dbf7bffe
    ldr r2, DAT_080bb0b4                     @ 080bb096 074a
    adds r0,r7,r2    @ 080bb098 b818
    .hword 0x4643    @ 080bb09a 4346
    str r3,[r0,#0x0]                         @ 080bb09c 0360
    movs r0,#0x1    @ 080bb09e 0120
    b LAB_080bb0e6                           @ 080bb0a0 21e0
    .zero  0x2
DAT_080bb0a4:
    .word  0x00000868                     @ 080bb0a4 68080000
DAT_080bb0a8:
    .word  0x0201c600                     @ 080bb0a8 00c60102
DAT_080bb0ac:
    .word  0xffff803f                     @ 080bb0ac 3f80ffff
DAT_080bb0b0:
    .word  0x00001c44                     @ 080bb0b0 441c0000
DAT_080bb0b4:
    .word  0x00001c38                     @ 080bb0b4 381c0000
LAB_080bb0b8:
    ldr r4, PTR_gP1LifePoints_080bb0d8       @ 080bb0b8 074c
    ldr r1, DAT_080bb0dc                     @ 080bb0ba 0849
    adds r0,r4,r1    @ 080bb0bc 6018
    str r6,[r0,#0x0]                         @ 080bb0be 0660
    adds r0,r6,#0x0    @ 080bb0c0 301c
    adds r1,r7,#0x0    @ 080bb0c2 391c
    movs r2,#0x0    @ 080bb0c4 0022
    movs r3,#0x3    @ 080bb0c6 0323
    bl init_duel_zone_target_slot_refs       @ 080bb0c8 dbf7a4fe
    ldr r2, DAT_080bb0e0                     @ 080bb0cc 044a
    adds r4,r4,r2    @ 080bb0ce a418
    movs r0,#0x1    @ 080bb0d0 0120
    str r0,[r4,#0x0]                         @ 080bb0d2 2060
    b LAB_080bb0e6                           @ 080bb0d4 07e0
    .zero  0x2
PTR_gP1LifePoints_080bb0d8:
    .word  gP1LifePoints                  @ 080bb0d8 e0c40102
DAT_080bb0dc:
    .word  0x00001d64                     @ 080bb0dc 641d0000
DAT_080bb0e0:
    .word  0x00001d58                     @ 080bb0e0 581d0000
LAB_080bb0e4:
    movs r0,#0x0    @ 080bb0e4 0020
LAB_080bb0e6:
    add sp,#0x20                             @ 080bb0e6 08b0
    pop {r3,r4,r5}                           @ 080bb0e8 38bc
    .hword 0x4698    @ 080bb0ea 9846
    .hword 0x46a1    @ 080bb0ec a146
    .hword 0x46aa    @ 080bb0ee aa46
    pop {r4,r5,r6,r7}                        @ 080bb0f0 f0bc
    pop {r1}                                 @ 080bb0f2 02bc
    bx r1                                    @ 080bb0f4 0847
    .zero  0x2

@ Finds equip slots satisfying effect count condition for a player. r0=player_key -> r5 (bit0=player_id); r1=zone_count -> [sp,#0]. Internal counter r8=0 (not a caller input; movs r0,#0; .hword 0x4680=mov r8,r0). Reads gP1LifePoints+player_stride+0xc (zone_limit, via r4=0x90*2=0x120 offset); if r8>=zone_limit returns 1 (no slots available). Loop (base r7=gP1LifePoints+0x120+player_id*0x868): reads each sub-slot [r7+0x0] dword, extracts card_id (lsls/lsrs 0x13); calls check_card_field5_is_nonzero(card_id); if 0 jumps to LAB_080bb2ac (slot has no field5). Else: large switch on card_id (0x1488, 0x127d, 0x1578 etc), each case calls dispatch_effect_handler_by_card_id or enqueue_sprite_attr variant. Callers: FUN_080bb2d4, FUN_080bc54c (player 0), FUN_080bc5d4 (player 1). Params: r0=u32 player_key (bit0=player_id [0..1]); r1=u32 zone_count -> [sp,#0]. Returns r0=u32 0=found+processed, 1=no available slot or condition not met. Side effects: OAM sprite attr buffer + effect handling via case callees. Constants: CARD_ID=0x1488 (Gilasaurus); CARD_ID=0x127d (Manga Ryu-Ran); CARD_ID=0x1578 (Lava Golem).
find_equip_slot_by_player_and_zone_count:
    push {r4,r5,r6,r7,lr}                    @ 080bb0f8 f0b5
    .hword 0x4657    @ 080bb0fa 5746
    .hword 0x464e    @ 080bb0fc 4e46
    .hword 0x4645    @ 080bb0fe 4546
    push {r5,r6,r7}                          @ 080bb100 e0b4
    sub sp,#0x8                              @ 080bb102 82b0
    adds r5,r0,#0x0    @ 080bb104 051c
    str r1,[sp,#0x0]                         @ 080bb106 0091
    movs r0,#0x0    @ 080bb108 0020
    .hword 0x4680    @ 080bb10a 8046
    ldr r1, PTR_gP1LifePoints_080bb164       @ 080bb10c 1549
    movs r0,#0x1    @ 080bb10e 0120
    ands r0,r5    @ 080bb110 2840
    ldr r4, DAT_080bb168                     @ 080bb112 154c
    adds r2,r0,#0x0    @ 080bb114 021c
    muls r2,r4    @ 080bb116 6243
    adds r0,r1,#0x0    @ 080bb118 081c
    adds r0,#0xc    @ 080bb11a 0c30
    adds r3,r2,r0    @ 080bb11c 1318
    ldr r0,[r3,#0x0]                         @ 080bb11e 1868
    cmp r8,r0                                @ 080bb120 8045
    bcc LAB_080bb126                         @ 080bb122 00d3
    b LAB_080bb2c0                           @ 080bb124 cce0
LAB_080bb126:
    .hword 0x46a2    @ 080bb126 a246
    movs r4,#0x90    @ 080bb128 9024
    lsls r4,r4,#0x1    @ 080bb12a 6400
    adds r0,r1,r4    @ 080bb12c 0819
    adds r7,r2,r0    @ 080bb12e 1718
    movs r0,#0x0    @ 080bb130 0020
    .hword 0x4681    @ 080bb132 8146
    str r3,[sp,#0x4]                         @ 080bb134 0193
LAB_080bb136:
    ldr r0,[r7,#0x0]                         @ 080bb136 3868
    lsls r0,r0,#0x13    @ 080bb138 c004
    lsrs r4,r0,#0x13    @ 080bb13a c40c
    adds r0,r4,#0x0    @ 080bb13c 201c
    bl check_card_field5_is_nonzero          @ 080bb13e 8ff703fe
    cmp r0,#0x0                              @ 080bb142 0028
    bne LAB_080bb148                         @ 080bb144 00d1
    b LAB_080bb2ac                           @ 080bb146 b1e0
LAB_080bb148:
    movs r6,#0x1    @ 080bb148 0126
    ldr r0, DAT_080bb16c                     @ 080bb14a 0848
    cmp r4,r0                                @ 080bb14c 8442
    beq LAB_080bb200                         @ 080bb14e 57d0
    cmp r4,r0                                @ 080bb150 8442
    bgt LAB_080bb174                         @ 080bb152 0fdc
    ldr r0, DAT_080bb170                     @ 080bb154 0648
    cmp r4,r0                                @ 080bb156 8442
    blt LAB_080bb244                         @ 080bb158 74db
    adds r0,#0x2    @ 080bb15a 0230
    cmp r4,r0                                @ 080bb15c 8442
    ble LAB_080bb20e                         @ 080bb15e 56dd
    adds r0,#0x26    @ 080bb160 2630
    b LAB_080bb180                           @ 080bb162 0de0
PTR_gP1LifePoints_080bb164:
    .word  gP1LifePoints                  @ 080bb164 e0c40102
DAT_080bb168:
    .word  0x00000868                     @ 080bb168 68080000
DAT_080bb16c:
    .word  0x00001488                     @ 080bb16c 88140000
DAT_080bb170:
    .word  0x0000127d                     @ 080bb170 7d120000
LAB_080bb174:
    ldr r0, DAT_080bb188                     @ 080bb174 0448
    cmp r4,r0                                @ 080bb176 8442
    beq LAB_080bb1b2                         @ 080bb178 1bd0
    cmp r4,r0                                @ 080bb17a 8442
    bgt LAB_080bb18c                         @ 080bb17c 06dc
    subs r0,#0x2e    @ 080bb17e 2e38
LAB_080bb180:
    cmp r4,r0                                @ 080bb180 8442
    beq LAB_080bb20e                         @ 080bb182 44d0
    b LAB_080bb244                           @ 080bb184 5ee0
    .zero  0x2
DAT_080bb188:
    .word  0x00001578                     @ 080bb188 78150000
LAB_080bb18c:
    ldr r0, DAT_080bb19c                     @ 080bb18c 0348
    cmp r4,r0                                @ 080bb18e 8442
    beq LAB_080bb1a0                         @ 080bb190 06d0
    adds r0,#0xf1    @ 080bb192 f130
    cmp r4,r0                                @ 080bb194 8442
    beq LAB_080bb234                         @ 080bb196 4dd0
    b LAB_080bb244                           @ 080bb198 54e0
    .zero  0x2
DAT_080bb19c:
    .word  0x000018b4                     @ 080bb19c b4180000
LAB_080bb1a0:
    adds r0,r5,#0x0    @ 080bb1a0 281c
    adds r1,r4,#0x0    @ 080bb1a2 211c
    movs r2,#0x0    @ 080bb1a4 0022
    bl dispatch_effect_handler_by_card_id    @ 080bb1a6 d2f783fc
    movs r6,#0x0    @ 080bb1aa 0026
    cmp r0,#0x3                              @ 080bb1ac 0328
    ble LAB_080bb244                         @ 080bb1ae 49dd
    b LAB_080bb248                           @ 080bb1b0 4ae0
LAB_080bb1b2:
    movs r6,#0x0    @ 080bb1b2 0026
    movs r1,#0x1    @ 080bb1b4 0121
    subs r4,r1,r5    @ 080bb1b6 4c1b
    adds r0,r4,#0x0    @ 080bb1b8 201c
    ands r0,r1    @ 080bb1ba 0840
    .hword 0x4651    @ 080bb1bc 5146
    muls r1,r0    @ 080bb1be 4143
    adds r0,r1,#0x0    @ 080bb1c0 081c
    ldr r1, PTR_gP1LifePoints_080bb1f8       @ 080bb1c2 0d49
    adds r0,r0,r1    @ 080bb1c4 4018
    ldr r1,[r0,#0x0]                         @ 080bb1c6 0168
    movs r0,#0xfa    @ 080bb1c8 fa20
    lsls r0,r0,#0x2    @ 080bb1ca 8000
    cmp r1,r0                                @ 080bb1cc 8142
    ble LAB_080bb248                         @ 080bb1ce 3bdd
    adds r0,r5,#0x0    @ 080bb1d0 281c
    movs r1,#0x0    @ 080bb1d2 0021
    movs r2,#0x1    @ 080bb1d4 0122
    movs r3,#0x0    @ 080bb1d6 0023
    bl count_equip_slots_matching_whitelist  @ 080bb1d8 78f79efc
    cmp r0,#0x0                              @ 080bb1dc 0028
    bgt LAB_080bb248                         @ 080bb1de 33dc
    adds r0,r5,#0x0    @ 080bb1e0 281c
    adds r1,r4,#0x0    @ 080bb1e2 211c
    bl sum_all_slot_scores_for_player        @ 080bb1e4 f4f7c6f8
    ldr r1, DAT_080bb1fc                     @ 080bb1e8 0449
    cmp r0,r1                                @ 080bb1ea 8842
    ble LAB_080bb244                         @ 080bb1ec 2add
    adds r0,r5,#0x0    @ 080bb1ee 281c
    bl count_occupied_monster_zones          @ 080bb1f0 77f7caff
    b LAB_080bb208                           @ 080bb1f4 08e0
    .zero  0x2
PTR_gP1LifePoints_080bb1f8:
    .word  gP1LifePoints                  @ 080bb1f8 e0c40102
DAT_080bb1fc:
    .word  0x00000bb7                     @ 080bb1fc b70b0000
LAB_080bb200:
    subs r0,r6,r5    @ 080bb200 701b
    bl count_hand_cards_with_field5          @ 080bb202 7cf783f8
    movs r6,#0x0    @ 080bb206 0026
LAB_080bb208:
    cmp r0,#0x0                              @ 080bb208 0028
    bne LAB_080bb244                         @ 080bb20a 1bd1
    b LAB_080bb248                           @ 080bb20c 1ce0
LAB_080bb20e:
    movs r6,#0x0    @ 080bb20e 0026
    ldr r4,[sp,#0x0]                         @ 080bb210 009c
    cmp r4,#0x0                              @ 080bb212 002c
    beq LAB_080bb244                         @ 080bb214 16d0
    ldr r0,[r7,#0x0]                         @ 080bb216 3868
    lsls r1,r0,#0x2    @ 080bb218 8100
    lsrs r1,r1,#0x18    @ 080bb21a 090e
    lsls r1,r1,#0x1    @ 080bb21c 4900
    lsls r0,r0,#0x12    @ 080bb21e 8004
    lsrs r0,r0,#0x1f    @ 080bb220 c00f
    adds r1,r1,r0    @ 080bb222 0918
    adds r0,r5,#0x0    @ 080bb224 281c
    movs r2,#0x1    @ 080bb226 0122
    bl score_equip_targets_for_monster_slot  @ 080bb228 f2f77afa
    rsbs r1,r0,#0    @ 080bb22c 4142
    orrs r1,r0    @ 080bb22e 0143
    lsrs r6,r1,#0x1f    @ 080bb230 ce0f
    b LAB_080bb244                           @ 080bb232 07e0
LAB_080bb234:
    adds r0,r5,#0x0    @ 080bb234 281c
    adds r1,r4,#0x0    @ 080bb236 211c
    bl count_slot_card_pair_allowed_for_card @ 080bb238 77f7a0fe
    movs r6,#0x0    @ 080bb23c 0026
    cmp r0,#0x0                              @ 080bb23e 0028
    bne LAB_080bb244                         @ 080bb240 00d1
    movs r6,#0x1    @ 080bb242 0126
LAB_080bb244:
    cmp r6,#0x0                              @ 080bb244 002e
    beq LAB_080bb2ac                         @ 080bb246 31d0
LAB_080bb248:
    movs r6,#0x1    @ 080bb248 0126
    adds r0,r5,#0x0    @ 080bb24a 281c
    ands r0,r6    @ 080bb24c 3040
    .hword 0x4651    @ 080bb24e 5146
    muls r1,r0    @ 080bb250 4143
    adds r0,r1,#0x0    @ 080bb252 081c
    add r0,r9                                @ 080bb254 4844
    ldr r4, DAT_080bb29c                     @ 080bb256 114c
    adds r0,r0,r4    @ 080bb258 0019
    ldr r0,[r0,#0x0]                         @ 080bb25a 0068
    lsls r1,r0,#0x2    @ 080bb25c 8100
    lsrs r1,r1,#0x18    @ 080bb25e 090e
    lsls r1,r1,#0x1    @ 080bb260 4900
    lsls r0,r0,#0x12    @ 080bb262 8004
    lsrs r0,r0,#0x1f    @ 080bb264 c00f
    adds r1,r1,r0    @ 080bb266 0918
    adds r0,r5,#0x0    @ 080bb268 281c
    bl eval_equip_target_slot_flags          @ 080bb26a e9f743fc
    cmp r0,#0x0                              @ 080bb26e 0028
    beq LAB_080bb2ac                         @ 080bb270 1cd0
    ldr r1, DAT_080bb2a0                     @ 080bb272 0b49
    adds r0,r4,r1    @ 080bb274 6018
    str r5,[r0,#0x0]                         @ 080bb276 0560
    adds r0,r5,#0x0    @ 080bb278 281c
    movs r1,#0xb    @ 080bb27a 0b21
    .hword 0x4642    @ 080bb27c 4246
    movs r3,#0x2    @ 080bb27e 0223
    bl init_duel_zone_target_slot_refs       @ 080bb280 dbf7c8fd
    ldr r1, DAT_080bb2a4                     @ 080bb284 0749
    adds r0,r4,r1    @ 080bb286 6018
    str r6,[r0,#0x0]                         @ 080bb288 0660
    ldr r0, DAT_080bb2a8                     @ 080bb28a 0748
    movs r4,#0xc0    @ 080bb28c c024
    lsls r4,r4,#0x1    @ 080bb28e 6400
    adds r0,r0,r4    @ 080bb290 0019
    movs r1,#0x0    @ 080bb292 0021
    str r1,[r0,#0x0]                         @ 080bb294 0160
    movs r0,#0x1    @ 080bb296 0120
    b LAB_080bb2c2                           @ 080bb298 13e0
    .zero  0x2
DAT_080bb29c:
    .word  0x0201c600                     @ 080bb29c 00c60102
DAT_080bb2a0:
    .word  0x00001c44                     @ 080bb2a0 441c0000
DAT_080bb2a4:
    .word  0x00001c38                     @ 080bb2a4 381c0000
DAT_080bb2a8:
    .word  0x0201afe0                     @ 080bb2a8 e0af0102
LAB_080bb2ac:
    adds r7,#0x4    @ 080bb2ac 0437
    movs r0,#0x4    @ 080bb2ae 0420
    add r9,r0                                @ 080bb2b0 8144
    movs r1,#0x1    @ 080bb2b2 0121
    add r8,r1                                @ 080bb2b4 8844
    ldr r4,[sp,#0x4]                         @ 080bb2b6 019c
    ldr r0,[r4,#0x0]                         @ 080bb2b8 2068
    cmp r8,r0                                @ 080bb2ba 8045
    bcs LAB_080bb2c0                         @ 080bb2bc 00d2
    b LAB_080bb136                           @ 080bb2be 3ae7
LAB_080bb2c0:
    movs r0,#0x0    @ 080bb2c0 0020
LAB_080bb2c2:
    add sp,#0x8                              @ 080bb2c2 02b0
    pop {r3,r4,r5}                           @ 080bb2c4 38bc
    .hword 0x4698    @ 080bb2c6 9846
    .hword 0x46a1    @ 080bb2c8 a146
    .hword 0x46aa    @ 080bb2ca aa46
    pop {r4,r5,r6,r7}                        @ 080bb2cc f0bc
    pop {r1}                                 @ 080bb2ce 02bc
    bx r1                                    @ 080bb2d0 0847
    .zero  0x2

@ Indirectly called by tick_duel_field_ai_state_machine (0x080bc71c, duel_field state machine driver, indeg=1) via function pointer table, no APCS parameters. Reads phase field at [0x0201afe0+0x8] and dispatches on three phases: phase=0 -> iterates equip slot table at 0x09e481e8 (stride=8, up to 0x38=56 entries), calls try_activate_equip_for_matching_slot until a hit, returns 0; phase=1 -> calls dispatch_equip_activation_full_sequence; phase=2 -> calls find_equip_slot_by_player_and_zone_count. Each successful path increments [0x0201afe0+0x8] by 1 (advances phase). All paths failing returns 1. Inputs: none (r0 immediately overwritten by ldr r0,PTR_gP1LifePoints; player_id from gP1LifePoints+0x1ce8). Returns: r0=u32 bool (0=activation chain in progress, 1=all paths exhausted/wait next cycle). Side effects: [0x0201afe0+0x8] phase counter +1 per path; indirect effects via callee activation functions. Constants: equip_slot_table=0x09e481e8 (equip slot table base, stride=8, count=56), ai_ctrl_block=0x0201afe0 (AI control block base), phase_field_offset=0x8, table_max=0x38 (56 iterations).
dispatch_field_spell_equip_ai_by_phase:
    push {r4,r5,r6,lr}                       @ 080bb2d4 70b5
    ldr r0, PTR_gP1LifePoints_080bb2f0       @ 080bb2d6 0648
    ldr r1, DAT_080bb2f4                     @ 080bb2d8 0649
    adds r0,r0,r1    @ 080bb2da 4018
    ldr r6,[r0,#0x0]                         @ 080bb2dc 0668
    ldr r0, DAT_080bb2f8                     @ 080bb2de 0648
    ldr r0,[r0,#0x8]                         @ 080bb2e0 8068
    cmp r0,#0x1                              @ 080bb2e2 0128
    beq LAB_080bb31c                         @ 080bb2e4 1ad0
    cmp r0,#0x1                              @ 080bb2e6 0128
    bcc LAB_080bb2fc                         @ 080bb2e8 08d3
    cmp r0,#0x2                              @ 080bb2ea 0228
    beq LAB_080bb32e                         @ 080bb2ec 1fd0
    b LAB_080bb350                           @ 080bb2ee 2fe0
PTR_gP1LifePoints_080bb2f0:
    .word  gP1LifePoints                  @ 080bb2f0 e0c40102
DAT_080bb2f4:
    .word  0x00001ce8                     @ 080bb2f4 e81c0000
DAT_080bb2f8:
    .word  0x0201afe0                     @ 080bb2f8 e0af0102
LAB_080bb2fc:
    movs r5,#0x0    @ 080bb2fc 0025
    ldr r4, DAT_080bb340                     @ 080bb2fe 104c
LAB_080bb300:
    adds r0,r6,#0x0    @ 080bb300 301c
    adds r1,r4,#0x0    @ 080bb302 211c
    bl try_activate_equip_for_matching_slot  @ 080bb304 fff7e4fd
    cmp r0,#0x0                              @ 080bb308 0028
    bne LAB_080bb33a                         @ 080bb30a 16d1
    adds r4,#0x8    @ 080bb30c 0834
    adds r5,#0x1    @ 080bb30e 0135
    cmp r5,#0x38                             @ 080bb310 382d
    bls LAB_080bb300                         @ 080bb312 f5d9
    ldr r1, DAT_080bb344                     @ 080bb314 0b49
    ldr r0,[r1,#0x8]                         @ 080bb316 8868
    adds r0,#0x1    @ 080bb318 0130
    str r0,[r1,#0x8]                         @ 080bb31a 8860
LAB_080bb31c:
    adds r0,r6,#0x0    @ 080bb31c 301c
    bl dispatch_equip_activation_full_sequence @ 080bb31e 00f079f8
    cmp r0,#0x0                              @ 080bb322 0028
    bne LAB_080bb33a                         @ 080bb324 09d1
    ldr r1, DAT_080bb344                     @ 080bb326 0749
    ldr r0,[r1,#0x8]                         @ 080bb328 8868
    adds r0,#0x1    @ 080bb32a 0130
    str r0,[r1,#0x8]                         @ 080bb32c 8860
LAB_080bb32e:
    adds r0,r6,#0x0    @ 080bb32e 301c
    movs r1,#0x0    @ 080bb330 0021
    bl find_equip_slot_by_player_and_zone_count @ 080bb332 fff7e1fe
    cmp r0,#0x0                              @ 080bb336 0028
    beq LAB_080bb348                         @ 080bb338 06d0
LAB_080bb33a:
    movs r0,#0x0    @ 080bb33a 0020
    b LAB_080bb352                           @ 080bb33c 09e0
    .zero  0x2
DAT_080bb340:
    .word  0x09e481e8                     @ 080bb340 e881e409
DAT_080bb344:
    .word  0x0201afe0                     @ 080bb344 e0af0102
LAB_080bb348:
    ldr r1, DAT_080bb358                     @ 080bb348 0349
    ldr r0,[r1,#0x8]                         @ 080bb34a 8868
    adds r0,#0x1    @ 080bb34c 0130
    str r0,[r1,#0x8]                         @ 080bb34e 8860
LAB_080bb350:
    movs r0,#0x1    @ 080bb350 0120
LAB_080bb352:
    pop {r4,r5,r6}                           @ 080bb352 70bc
    pop {r1}                                 @ 080bb354 02bc
    bx r1                                    @ 080bb356 0847
DAT_080bb358:
    .word  0x0201afe0                     @ 080bb358 e0af0102

@ 被 FUN_080bc22c (toon world equip AI 决策) 以 r0=player_id 调用 (indeg=1, @ 080bc2d6). 入口 r0=player_id [0..1]. 遍历固定 ROM 常量池 0x09e483b0: 以 r4=0..0xa4 (165 次, 步长 8 字节) 计算 entry_ptr=0x09e483b0+r4*8; 调用 try_activate_equip_for_matching_slot(player, entry_ptr); 若返回 1 (找到匹配并激活成功) 立即返回 1; 全部条目失败则返回 0. 纯扫描器, 外部写入通过 callee 副作用传播. Constants: ENTRY_POOL_BASE=0x09e483b0, ENTRY_SIZE=8, ENTRY_COUNT=0xa4+1=165.
scan_all_effect_zone_entries_for_equip_activation:
    push {r4,r5,lr}                          @ 080bb35c 30b5
    adds r5,r0,#0x0    @ 080bb35e 051c
    movs r4,#0x0    @ 080bb360 0024
LAB_080bb362:
    lsls r1,r4,#0x3    @ 080bb362 e100
    ldr r0, DAT_080bb378                     @ 080bb364 0448
    adds r1,r1,r0    @ 080bb366 0918
    adds r0,r5,#0x0    @ 080bb368 281c
    bl try_activate_equip_for_matching_slot  @ 080bb36a fff7b1fd
    cmp r0,#0x0                              @ 080bb36e 0028
    beq LAB_080bb37c                         @ 080bb370 04d0
    movs r0,#0x1    @ 080bb372 0120
    b LAB_080bb384                           @ 080bb374 06e0
    .zero  0x2
DAT_080bb378:
    .word  0x09e483b0                     @ 080bb378 b083e409
LAB_080bb37c:
    adds r4,#0x1    @ 080bb37c 0134
    cmp r4,#0xa4                             @ 080bb37e a42c
    bls LAB_080bb362                         @ 080bb380 efd9
    movs r0,#0x0    @ 080bb382 0020
LAB_080bb384:
    pop {r4,r5}                              @ 080bb384 30bc
    pop {r1}                                 @ 080bb386 02bc
    bx r1                                    @ 080bb388 0847
    .zero  0x2

@ 被 FUN_08097828 (switchD case_1, 0x08097958) 和 FUN_080bc698 调用 (indeg=2). 入口 r6=r0=player_side, r7=r1=retry_flag. 两阶段扫描 effect zone 表: Phase 1 (r4=[0..2]): gEffectZoneTable_A=0x09e488d8 基址 (stride=8) 调用 try_activate_equip_for_matching_slot; 若命中立即返回 1. Phase 1 无命中: retry_flag==0 -> Phase 2; retry_flag!=0 -> 返回 0. Phase 2 (r4=[0..4]): gEffectZoneTable_B=0x09e488f0 基址再次调用; 命中返回 1. 全部失败返回 0. Side effects: 通过 try_activate_equip_for_matching_slot 间接触发装备激活副作用. Constants: gEffectZoneTable_A=0x09e488d8, gEffectZoneTable_B=0x09e488f0, stride=8, phase1_max=2, phase2_max=4.
try_activate_equip_via_two_tables:
    push {r4,r5,r6,r7,lr}                    @ 080bb38c f0b5
    adds r6,r0,#0x0    @ 080bb38e 061c
    adds r7,r1,#0x0    @ 080bb390 0f1c
    movs r4,#0x0    @ 080bb392 0024
    ldr r5, DAT_080bb3b0                     @ 080bb394 064d
LAB_080bb396:
    adds r0,r6,#0x0    @ 080bb396 301c
    adds r1,r5,#0x0    @ 080bb398 291c
    bl try_activate_equip_for_matching_slot  @ 080bb39a fff799fd
    cmp r0,#0x0                              @ 080bb39e 0028
    bne LAB_080bb3b4                         @ 080bb3a0 08d1
    adds r5,#0x8    @ 080bb3a2 0835
    adds r4,#0x1    @ 080bb3a4 0134
    cmp r4,#0x2                              @ 080bb3a6 022c
    bls LAB_080bb396                         @ 080bb3a8 f5d9
    cmp r7,#0x0                              @ 080bb3aa 002f
    beq LAB_080bb3b8                         @ 080bb3ac 04d0
    b LAB_080bb3d0                           @ 080bb3ae 0fe0
DAT_080bb3b0:
    .word  0x09e488d8                     @ 080bb3b0 d888e409
LAB_080bb3b4:
    movs r0,#0x1    @ 080bb3b4 0120
    b LAB_080bb3d2                           @ 080bb3b6 0ce0
LAB_080bb3b8:
    movs r4,#0x0    @ 080bb3b8 0024
    ldr r5, DAT_080bb3d8                     @ 080bb3ba 074d
LAB_080bb3bc:
    adds r0,r6,#0x0    @ 080bb3bc 301c
    adds r1,r5,#0x0    @ 080bb3be 291c
    bl try_activate_equip_for_matching_slot  @ 080bb3c0 fff786fd
    cmp r0,#0x0                              @ 080bb3c4 0028
    bne LAB_080bb3b4                         @ 080bb3c6 f5d1
    adds r5,#0x8    @ 080bb3c8 0835
    adds r4,#0x1    @ 080bb3ca 0134
    cmp r4,#0x4                              @ 080bb3cc 042c
    bls LAB_080bb3bc                         @ 080bb3ce f5d9
LAB_080bb3d0:
    movs r0,#0x0    @ 080bb3d0 0020
LAB_080bb3d2:
    pop {r4,r5,r6,r7}                        @ 080bb3d2 f0bc
    pop {r1}                                 @ 080bb3d4 02bc
    bx r1                                    @ 080bb3d6 0847
DAT_080bb3d8:
    .word  0x09e488f0                     @ 080bb3d8 f088e409

@ Scans up to 0xce effect zone entries (base=0x09e48918, stride=8) for player r0. For each entry: check_card_field5_is_nonzero; if valid call check_normal_summon_eligible_for_slot(player, entry, 0). Returns u32: 1=any effect zone card passes normal summon eligibility, 0=none. r0=u32 player_id [0..1]. Constants: effect_zone_base=0x09e48918, max_entries=0xce, entry_stride=8.
check_normal_summon_eligible_for_any_effect_zone:
    push {r4,r5,r6,lr}                       @ 080bb3dc 70b5
    adds r6,r0,#0x0    @ 080bb3de 061c
    movs r5,#0x0    @ 080bb3e0 0025
    ldr r4, DAT_080bb400                     @ 080bb3e2 074c
LAB_080bb3e4:
    ldr r0,[r4,#0x0]                         @ 080bb3e4 2068
    bl check_card_field5_is_nonzero          @ 080bb3e6 8ff7affc
    cmp r0,#0x0                              @ 080bb3ea 0028
    beq LAB_080bb404                         @ 080bb3ec 0ad0
    adds r0,r6,#0x0    @ 080bb3ee 301c
    adds r1,r4,#0x0    @ 080bb3f0 211c
    movs r2,#0x0    @ 080bb3f2 0022
    bl check_normal_summon_eligible_for_slot @ 080bb3f4 f9f7d2fa
    cmp r0,#0x0                              @ 080bb3f8 0028
    beq LAB_080bb404                         @ 080bb3fa 03d0
    movs r0,#0x1    @ 080bb3fc 0120
    b LAB_080bb40e                           @ 080bb3fe 06e0
DAT_080bb400:
    .word  0x09e48918                     @ 080bb400 1889e409
LAB_080bb404:
    adds r4,#0x8    @ 080bb404 0834
    adds r5,#0x1    @ 080bb406 0135
    cmp r5,#0xce                             @ 080bb408 ce2d
    bls LAB_080bb3e4                         @ 080bb40a ebd9
    movs r0,#0x0    @ 080bb40c 0020
LAB_080bb40e:
    pop {r4,r5,r6}                           @ 080bb40e 70bc
    pop {r1}                                 @ 080bb410 02bc
    bx r1                                    @ 080bb412 0847

@ 被 FUN_080bc168 (0x080bc2be/0x080bc592/0x080bc610) 及 FUN_080bb31e 调用 (indeg>=4). 入口 r6=r0=player_side. 大型装备激活全流程分派器. 首先线性扫描 effect_zone_base=0x09e48918 (stride=8, 上界 0xce) 调用 try_activate_equip_for_matching_slot; 命中立即返回 1. 扫描无命中后依次: (D) dispatch_effect_handler_by_card_id(player,0xfffe,0xd) -> get_duel_activation_zone_id > 0 -> get_activation_zone_card_type_field(0) -> find_card_pair_in_player_deck_list -> dispatch_to_effect_handler_by_card_type; (E) dispatch_effect_handler_by_card_id(player,0xfffe,0xe) -> find_deck_slot_by_card_pair_match -> dispatch_to_effect_handler_by_card_type; (C) dispatch_effect_handler_by_card_id(player,0xfffe,0xc) -> 内层循环 r7=[0..zone_count] 调用 get_activation_zone_card_type_field(r7) 进行 BST (0x15ab/0x15f9/0x15fa) -> count_equip_slots_matching_whitelist/count_monster_slots_by_chain_head_id -> get_effect_slot_entry_ptr x2 -> dispatch_to_effect_handler_by_card_type. 若全部失败: count_field_copies_of_card(0x166c) > 0 返回 1. 最后大型 monster_zone+field_spell 循环. 返回 r0=u32 success (1=激活成功, 0=无). Side effects: 通过 try_activate_equip_for_matching_slot/dispatch_to_effect_handler_by_card_type 写 gDuelBattleState; 通过 enqueue_equip_slot_bitmap_update 写 OAM bitmap. Constants: effect_zone_base=0x09e48918, max_entries=0xce=206, entry_stride=8, card_id_mask=0xfffe, dispatch_types=[0xc/0xd/0xe], gDuelFieldSlots=0x0201c510.
dispatch_equip_activation_full_sequence:
    push {r4,r5,r6,r7,lr}                    @ 080bb414 f0b5
    .hword 0x4657    @ 080bb416 5746
    .hword 0x464e    @ 080bb418 4e46
    .hword 0x4645    @ 080bb41a 4546
    push {r5,r6,r7}                          @ 080bb41c e0b4
    sub sp,#0x20                             @ 080bb41e 88b0
    adds r6,r0,#0x0    @ 080bb420 061c
    movs r7,#0x0    @ 080bb422 0027
    ldr r4, DAT_080bb488                     @ 080bb424 184c
LAB_080bb426:
    adds r0,r6,#0x0    @ 080bb426 301c
    adds r1,r4,#0x0    @ 080bb428 211c
    bl try_activate_equip_for_matching_slot  @ 080bb42a fff751fd
    cmp r0,#0x0                              @ 080bb42e 0028
    beq LAB_080bb434                         @ 080bb430 00d0
    b LAB_080bb59a                           @ 080bb432 b2e0
LAB_080bb434:
    adds r4,#0x8    @ 080bb434 0834
    adds r7,#0x1    @ 080bb436 0137
    cmp r7,#0xce                             @ 080bb438 ce2f
    bls LAB_080bb426                         @ 080bb43a f4d9
    ldr r1, DAT_080bb48c                     @ 080bb43c 1349
    adds r0,r6,#0x0    @ 080bb43e 301c
    movs r2,#0xd    @ 080bb440 0d22
    bl dispatch_effect_handler_by_card_id    @ 080bb442 d2f735fb
    cmp r0,#0x0                              @ 080bb446 0028
    beq LAB_080bb4a0                         @ 080bb448 2ad0
    bl get_duel_activation_zone_id           @ 080bb44a d8f763ff
    cmp r0,#0x0                              @ 080bb44e 0028
    ble LAB_080bb4a0                         @ 080bb450 26dd
    movs r0,#0x0    @ 080bb452 0020
    bl get_activation_zone_card_type_field   @ 080bb454 d8f764ff
    adds r4,r0,#0x0    @ 080bb458 041c
    adds r0,r6,#0x0    @ 080bb45a 301c
    adds r1,r4,#0x0    @ 080bb45c 211c
    bl find_card_pair_in_player_deck_list    @ 080bb45e 76f72bf9
    cmp r0,#0x0                              @ 080bb462 0028
    blt LAB_080bb498                         @ 080bb464 18db
    movs r1,#0x1    @ 080bb466 0121
    ands r1,r6    @ 080bb468 3140
    lsls r2,r0,#0x2    @ 080bb46a 8200
    ldr r0, DAT_080bb490                     @ 080bb46c 0848
    muls r0,r1    @ 080bb46e 4843
    adds r2,r2,r0    @ 080bb470 1218
    ldr r0, DAT_080bb494                     @ 080bb472 0848
    adds r2,r2,r0    @ 080bb474 1218
    ldr r1,[r2,#0x0]                         @ 080bb476 1168
    lsls r0,r1,#0x2    @ 080bb478 8800
    lsrs r0,r0,#0x18    @ 080bb47a 000e
    lsls r0,r0,#0x1    @ 080bb47c 4000
    lsls r1,r1,#0x12    @ 080bb47e 8904
    lsrs r1,r1,#0x1f    @ 080bb480 c90f
    adds r2,r0,r1    @ 080bb482 4218
    b LAB_080bb49a                           @ 080bb484 09e0
    .zero  0x2
DAT_080bb488:
    .word  0x09e48918                     @ 080bb488 1889e409
DAT_080bb48c:
    .word  0x0000fffe                     @ 080bb48c feff0000
DAT_080bb490:
    .word  0x00000868                     @ 080bb490 68080000
DAT_080bb494:
    .word  0x0201c740                     @ 080bb494 40c70102
LAB_080bb498:
    movs r2,#0x0    @ 080bb498 0022
LAB_080bb49a:
    adds r0,r6,#0x0    @ 080bb49a 301c
    adds r1,r4,#0x0    @ 080bb49c 211c
    b LAB_080bb596                           @ 080bb49e 7ae0
LAB_080bb4a0:
    ldr r1, DAT_080bb4ec                     @ 080bb4a0 1249
    adds r0,r6,#0x0    @ 080bb4a2 301c
    movs r2,#0xe    @ 080bb4a4 0e22
    bl dispatch_effect_handler_by_card_id    @ 080bb4a6 d2f703fb
    cmp r0,#0x0                              @ 080bb4aa 0028
    beq LAB_080bb500                         @ 080bb4ac 28d0
    bl get_duel_activation_zone_id           @ 080bb4ae d8f731ff
    cmp r0,#0x0                              @ 080bb4b2 0028
    ble LAB_080bb500                         @ 080bb4b4 24dd
    movs r0,#0x0    @ 080bb4b6 0020
    bl get_activation_zone_card_type_field   @ 080bb4b8 d8f732ff
    adds r4,r0,#0x0    @ 080bb4bc 041c
    adds r0,r6,#0x0    @ 080bb4be 301c
    adds r1,r4,#0x0    @ 080bb4c0 211c
    bl find_deck_slot_by_card_pair_match     @ 080bb4c2 7bf7b5fd
    cmp r0,#0x0                              @ 080bb4c6 0028
    blt LAB_080bb4f8                         @ 080bb4c8 16db
    movs r1,#0x1    @ 080bb4ca 0121
    ands r1,r6    @ 080bb4cc 3140
    lsls r2,r0,#0x2    @ 080bb4ce 8200
    ldr r0, DAT_080bb4f0                     @ 080bb4d0 0748
    muls r0,r1    @ 080bb4d2 4843
    adds r2,r2,r0    @ 080bb4d4 1218
    ldr r0, DAT_080bb4f4                     @ 080bb4d6 0748
    adds r2,r2,r0    @ 080bb4d8 1218
    ldr r1,[r2,#0x0]                         @ 080bb4da 1168
    lsls r0,r1,#0x2    @ 080bb4dc 8800
    lsrs r0,r0,#0x18    @ 080bb4de 000e
    lsls r0,r0,#0x1    @ 080bb4e0 4000
    lsls r1,r1,#0x12    @ 080bb4e2 8904
    lsrs r1,r1,#0x1f    @ 080bb4e4 c90f
    adds r2,r0,r1    @ 080bb4e6 4218
    b LAB_080bb4fa                           @ 080bb4e8 07e0
    .zero  0x2
DAT_080bb4ec:
    .word  0x0000fffe                     @ 080bb4ec feff0000
DAT_080bb4f0:
    .word  0x00000868                     @ 080bb4f0 68080000
DAT_080bb4f4:
    .word  0x0201c8f8                     @ 080bb4f4 f8c80102
LAB_080bb4f8:
    movs r2,#0x0    @ 080bb4f8 0022
LAB_080bb4fa:
    adds r0,r6,#0x0    @ 080bb4fa 301c
    adds r1,r4,#0x0    @ 080bb4fc 211c
    b LAB_080bb596                           @ 080bb4fe 4ae0
LAB_080bb500:
    ldr r1, DAT_080bb514                     @ 080bb500 0449
    adds r0,r6,#0x0    @ 080bb502 301c
    movs r2,#0xc    @ 080bb504 0c22
    bl dispatch_effect_handler_by_card_id    @ 080bb506 d2f7d3fa
    cmp r0,#0x0                              @ 080bb50a 0028
    beq LAB_080bb5a8                         @ 080bb50c 4cd0
    movs r7,#0x0    @ 080bb50e 0027
    b LAB_080bb5a0                           @ 080bb510 46e0
    .zero  0x2
DAT_080bb514:
    .word  0x0000fffe                     @ 080bb514 feff0000
LAB_080bb518:
    adds r0,r7,#0x0    @ 080bb518 381c
    bl get_activation_zone_card_type_field   @ 080bb51a d8f701ff
    adds r5,r0,#0x0    @ 080bb51e 051c
    movs r1,#0x1    @ 080bb520 0121
    ldr r0, DAT_080bb534                     @ 080bb522 0448
    cmp r5,r0                                @ 080bb524 8542
    beq LAB_080bb54c                         @ 080bb526 11d0
    cmp r5,r0                                @ 080bb528 8542
    bgt LAB_080bb538                         @ 080bb52a 05dc
    subs r0,#0x48    @ 080bb52c 4838
    cmp r5,r0                                @ 080bb52e 8542
    beq LAB_080bb544                         @ 080bb530 08d0
    b LAB_080bb570                           @ 080bb532 1de0
DAT_080bb534:
    .word  0x000015f9                     @ 080bb534 f9150000
LAB_080bb538:
    ldr r0, DAT_080bb540                     @ 080bb538 0148
    cmp r5,r0                                @ 080bb53a 8542
    beq LAB_080bb560                         @ 080bb53c 10d0
    b LAB_080bb570                           @ 080bb53e 17e0
DAT_080bb540:
    .word  0x000015fa                     @ 080bb540 fa150000
LAB_080bb544:
    subs r0,r1,r6    @ 080bb544 881b
    movs r1,#0x1    @ 080bb546 0121
    movs r2,#0x0    @ 080bb548 0022
    b LAB_080bb552                           @ 080bb54a 02e0
LAB_080bb54c:
    subs r0,r1,r6    @ 080bb54c 881b
    movs r1,#0x0    @ 080bb54e 0021
    movs r2,#0x1    @ 080bb550 0122
LAB_080bb552:
    movs r3,#0x1    @ 080bb552 0123
    bl count_equip_slots_matching_whitelist  @ 080bb554 78f7e0fa
    movs r1,#0x0    @ 080bb558 0021
    cmp r0,#0x0                              @ 080bb55a 0028
    ble LAB_080bb570                         @ 080bb55c 08dd
    b LAB_080bb574                           @ 080bb55e 09e0
LAB_080bb560:
    subs r0,r1,r6    @ 080bb560 881b
    movs r1,#0x0    @ 080bb562 0021
    bl count_monster_slots_by_chain_head_id  @ 080bb564 77f7e6fe
    movs r1,#0x0    @ 080bb568 0021
    cmp r0,#0x0                              @ 080bb56a 0028
    ble LAB_080bb570                         @ 080bb56c 00dd
    movs r1,#0x1    @ 080bb56e 0121
LAB_080bb570:
    cmp r1,#0x0                              @ 080bb570 0029
    beq LAB_080bb59e                         @ 080bb572 14d0
LAB_080bb574:
    adds r0,r7,#0x0    @ 080bb574 381c
    bl get_effect_slot_entry_ptr             @ 080bb576 d8f7b9fe
    adds r4,r0,#0x0    @ 080bb57a 041c
    adds r0,r7,#0x0    @ 080bb57c 381c
    bl get_effect_slot_entry_ptr             @ 080bb57e d8f7b5fe
    ldr r2,[r4,#0x0]                         @ 080bb582 2268
    lsls r2,r2,#0x2    @ 080bb584 9200
    lsrs r2,r2,#0x18    @ 080bb586 120e
    lsls r2,r2,#0x1    @ 080bb588 5200
    ldr r0,[r0,#0x0]                         @ 080bb58a 0068
    lsls r0,r0,#0x12    @ 080bb58c 8004
    lsrs r0,r0,#0x1f    @ 080bb58e c00f
    adds r2,r2,r0    @ 080bb590 1218
    adds r0,r6,#0x0    @ 080bb592 301c
    adds r1,r5,#0x0    @ 080bb594 291c
LAB_080bb596:
    bl dispatch_to_effect_handler_by_card_type @ 080bb596 dbf7dbfd
LAB_080bb59a:
    movs r0,#0x1    @ 080bb59a 0120
    b LAB_080bb99a                           @ 080bb59c fde1
LAB_080bb59e:
    adds r7,#0x1    @ 080bb59e 0137
LAB_080bb5a0:
    bl get_duel_activation_zone_id           @ 080bb5a0 d8f7b8fe
    cmp r7,r0                                @ 080bb5a4 8742
    blt LAB_080bb518                         @ 080bb5a6 b7db
LAB_080bb5a8:
    ldr r0, DAT_080bb5b4                     @ 080bb5a8 0248
    bl count_field_copies_of_card            @ 080bb5aa 77f7f7f8
    cmp r0,#0x0                              @ 080bb5ae 0028
    beq LAB_080bb5e0                         @ 080bb5b0 16d0
    b LAB_080bb998                           @ 080bb5b2 f1e1
DAT_080bb5b4:
    .word  0x0000166c                     @ 080bb5b4 6c160000
LAB_080bb5b8:
    ldr r0, PTR_gP1LifePoints_080bb5d4       @ 080bb5b8 0648
    ldr r2, DAT_080bb5d8                     @ 080bb5ba 074a
    adds r1,r0,r2    @ 080bb5bc 8118
    str r6,[r1,#0x0]                         @ 080bb5be 0e60
    ldr r3, DAT_080bb5dc                     @ 080bb5c0 064b
    adds r0,r0,r3    @ 080bb5c2 c018
    movs r1,#0x1    @ 080bb5c4 0121
    str r1,[r0,#0x0]                         @ 080bb5c6 0160
    adds r0,r6,#0x0    @ 080bb5c8 301c
    adds r1,r7,#0x0    @ 080bb5ca 391c
    movs r2,#0x0    @ 080bb5cc 0022
    movs r3,#0x9    @ 080bb5ce 0923
    b LAB_080bb8ee                           @ 080bb5d0 8de1
    .zero  0x2
PTR_gP1LifePoints_080bb5d4:
    .word  gP1LifePoints                  @ 080bb5d4 e0c40102
DAT_080bb5d8:
    .word  0x00001d64                     @ 080bb5d8 641d0000
DAT_080bb5dc:
    .word  0x00001d58                     @ 080bb5dc 581d0000
LAB_080bb5e0:
    movs r7,#0x0    @ 080bb5e0 0027
    movs r0,#0x1    @ 080bb5e2 0120
    .hword 0x4682    @ 080bb5e4 8246
    adds r0,r6,#0x0    @ 080bb5e6 301c
    .hword 0x4651    @ 080bb5e8 5146
    ands r0,r1    @ 080bb5ea 0840
    ldr r1, DAT_080bb664                     @ 080bb5ec 1d49
    adds r2,r0,#0x0    @ 080bb5ee 021c
    muls r2,r1    @ 080bb5f0 4a43
    ldr r1, DAT_080bb668                     @ 080bb5f2 1d49
    str r0,[sp,#0x18]                        @ 080bb5f4 0690
    adds r0,r1,#0x0    @ 080bb5f6 081c
    subs r0,#0x24    @ 080bb5f8 2438
    adds r0,r2,r0    @ 080bb5fa 1018
    str r0,[sp,#0x1c]                        @ 080bb5fc 0790
    adds r2,r2,r1    @ 080bb5fe 5218
    .hword 0x4690    @ 080bb600 9046
    .hword 0x466d    @ 080bb602 6d46
LAB_080bb604:
    .hword 0x4642    @ 080bb604 4246
    ldr r0,[r2,#0x0]                         @ 080bb606 1068
    lsls r0,r0,#0x13    @ 080bb608 c004
    lsrs r4,r0,#0x13    @ 080bb60a c40c
    adds r0,r6,#0x0    @ 080bb60c 301c
    adds r1,r7,#0x0    @ 080bb60e 391c
    bl check_slot_field_action_eligibility   @ 080bb610 78f7a2fe
    cmp r0,#0x0                              @ 080bb614 0028
    bne LAB_080bb61a                         @ 080bb616 00d1
    b LAB_080bb98c                           @ 080bb618 b8e1
LAB_080bb61a:
    adds r0,r6,#0x0    @ 080bb61a 301c
    adds r1,r7,#0x0    @ 080bb61c 391c
    bl check_field_spell_slot_placeable      @ 080bb61e 78f7dfff
    cmp r0,#0x0                              @ 080bb622 0028
    bne LAB_080bb628                         @ 080bb624 00d1
    b LAB_080bb854                           @ 080bb626 15e1
LAB_080bb628:
    movs r1,#0x0    @ 080bb628 0021
    ldr r0, DAT_080bb66c                     @ 080bb62a 1048
    cmp r4,r0                                @ 080bb62c 8442
    bgt LAB_080bb700                         @ 080bb62e 67dc
    subs r0,#0x1    @ 080bb630 0138
    cmp r4,r0                                @ 080bb632 8442
    blt LAB_080bb638                         @ 080bb634 00db
    b LAB_080bb794                           @ 080bb636 ade0
LAB_080bb638:
    movs r0,#0x90    @ 080bb638 9020
    lsls r0,r0,#0x5    @ 080bb63a 4001
    cmp r4,r0                                @ 080bb63c 8442
    bne LAB_080bb642                         @ 080bb63e 00d1
    b LAB_080bb794                           @ 080bb640 a8e0
LAB_080bb642:
    cmp r4,r0                                @ 080bb642 8442
    bgt LAB_080bb6a8                         @ 080bb644 30dc
    subs r0,#0x3d    @ 080bb646 3d38
    cmp r4,r0                                @ 080bb648 8442
    bne LAB_080bb64e                         @ 080bb64a 00d1
    b LAB_080bb794                           @ 080bb64c a2e0
LAB_080bb64e:
    cmp r4,r0                                @ 080bb64e 8442
    bgt LAB_080bb67c                         @ 080bb650 14dc
    ldr r0, DAT_080bb670                     @ 080bb652 0748
    cmp r4,r0                                @ 080bb654 8442
    bne LAB_080bb65a                         @ 080bb656 00d1
    b LAB_080bb794                           @ 080bb658 9ce0
LAB_080bb65a:
    cmp r4,r0                                @ 080bb65a 8442
    bgt LAB_080bb674                         @ 080bb65c 0adc
    subs r0,#0x8c    @ 080bb65e 8c38
    b LAB_080bb76e                           @ 080bb660 85e0
    .zero  0x2
DAT_080bb664:
    .word  0x00000868                     @ 080bb664 68080000
DAT_080bb668:
    .word  0x0201c510                     @ 080bb668 10c50102
DAT_080bb66c:
    .word  0x000014ce                     @ 080bb66c ce140000
DAT_080bb670:
    .word  0x00001086                     @ 080bb670 86100000
LAB_080bb674:
    ldr r0, DAT_080bb678                     @ 080bb674 0048
    b LAB_080bb76e                           @ 080bb676 7ae0
DAT_080bb678:
    .word  0x0000119b                     @ 080bb678 9b110000
LAB_080bb67c:
    ldr r0, DAT_080bb694                     @ 080bb67c 0548
    cmp r4,r0                                @ 080bb67e 8442
    bne LAB_080bb684                         @ 080bb680 00d1
    b LAB_080bb818                           @ 080bb682 c9e0
LAB_080bb684:
    cmp r4,r0                                @ 080bb684 8442
    bgt LAB_080bb698                         @ 080bb686 07dc
    subs r0,#0x18    @ 080bb688 1838
    cmp r4,r0                                @ 080bb68a 8442
    bne LAB_080bb690                         @ 080bb68c 00d1
    b LAB_080bb82e                           @ 080bb68e cee0
LAB_080bb690:
    b LAB_080bb828                           @ 080bb690 cae0
    .zero  0x2
DAT_080bb694:
    .word  0x000011f0                     @ 080bb694 f0110000
LAB_080bb698:
    ldr r0, DAT_080bb6a4                     @ 080bb698 0248
    cmp r4,r0                                @ 080bb69a 8442
    bne LAB_080bb6a0                         @ 080bb69c 00d1
    b LAB_080bb80e                           @ 080bb69e b6e0
LAB_080bb6a0:
    b LAB_080bb828                           @ 080bb6a0 c2e0
    .zero  0x2
DAT_080bb6a4:
    .word  0x000011f5                     @ 080bb6a4 f5110000
LAB_080bb6a8:
    ldr r0, DAT_080bb6c4                     @ 080bb6a8 0648
    cmp r4,r0                                @ 080bb6aa 8442
    bne LAB_080bb6b0                         @ 080bb6ac 00d1
    b LAB_080bb804                           @ 080bb6ae a9e0
LAB_080bb6b0:
    cmp r4,r0                                @ 080bb6b0 8442
    bgt LAB_080bb6d8                         @ 080bb6b2 11dc
    subs r0,#0xc8    @ 080bb6b4 c838
    cmp r4,r0                                @ 080bb6b6 8442
    bne LAB_080bb6bc                         @ 080bb6b8 00d1
    b LAB_080bb82e                           @ 080bb6ba b8e0
LAB_080bb6bc:
    cmp r4,r0                                @ 080bb6bc 8442
    bgt LAB_080bb6c8                         @ 080bb6be 03dc
    subs r0,#0x7a    @ 080bb6c0 7a38
    b LAB_080bb76e                           @ 080bb6c2 54e0
DAT_080bb6c4:
    .word  0x00001369                     @ 080bb6c4 69130000
LAB_080bb6c8:
    ldr r0, DAT_080bb6d4                     @ 080bb6c8 0248
    cmp r4,r0                                @ 080bb6ca 8442
    bne LAB_080bb6d0                         @ 080bb6cc 00d1
    b LAB_080bb804                           @ 080bb6ce 99e0
LAB_080bb6d0:
    b LAB_080bb828                           @ 080bb6d0 aae0
    .zero  0x2
DAT_080bb6d4:
    .word  0x00001331                     @ 080bb6d4 31130000
LAB_080bb6d8:
    ldr r0, DAT_080bb6e8                     @ 080bb6d8 0348
    cmp r4,r0                                @ 080bb6da 8442
    beq LAB_080bb794                         @ 080bb6dc 5ad0
    cmp r4,r0                                @ 080bb6de 8442
    bgt LAB_080bb6ec                         @ 080bb6e0 04dc
    subs r0,#0x5    @ 080bb6e2 0538
    b LAB_080bb76e                           @ 080bb6e4 43e0
    .zero  0x2
DAT_080bb6e8:
    .word  0x000013b0                     @ 080bb6e8 b0130000
LAB_080bb6ec:
    ldr r0, DAT_080bb6fc                     @ 080bb6ec 0348
    cmp r4,r0                                @ 080bb6ee 8442
    beq LAB_080bb794                         @ 080bb6f0 50d0
    adds r0,#0x76    @ 080bb6f2 7630
    cmp r4,r0                                @ 080bb6f4 8442
    bne LAB_080bb6fa                         @ 080bb6f6 00d1
    b LAB_080bb818                           @ 080bb6f8 8ee0
LAB_080bb6fa:
    b LAB_080bb828                           @ 080bb6fa 95e0
DAT_080bb6fc:
    .word  0x00001413                     @ 080bb6fc 13140000
LAB_080bb700:
    movs r0,#0xbf    @ 080bb700 bf20
    lsls r0,r0,#0x5    @ 080bb702 4001
    cmp r4,r0                                @ 080bb704 8442
    beq LAB_080bb794                         @ 080bb706 45d0
    cmp r4,r0                                @ 080bb708 8442
    bgt LAB_080bb74c                         @ 080bb70a 1fdc
    ldr r0, DAT_080bb72c                     @ 080bb70c 0748
    cmp r4,r0                                @ 080bb70e 8442
    bne LAB_080bb714                         @ 080bb710 00d1
    b LAB_080bb82e                           @ 080bb712 8ce0
LAB_080bb714:
    cmp r4,r0                                @ 080bb714 8442
    bgt LAB_080bb730                         @ 080bb716 0bdc
    subs r0,#0x9    @ 080bb718 0938
    cmp r4,r0                                @ 080bb71a 8442
    bge LAB_080bb720                         @ 080bb71c 00da
    b LAB_080bb828                           @ 080bb71e 83e0
LAB_080bb720:
    adds r0,#0x1    @ 080bb720 0130
    cmp r4,r0                                @ 080bb722 8442
    ble LAB_080bb794                         @ 080bb724 36dd
    adds r0,#0x3    @ 080bb726 0330
    b LAB_080bb76e                           @ 080bb728 21e0
    .zero  0x2
DAT_080bb72c:
    .word  0x00001533                     @ 080bb72c 33150000
LAB_080bb730:
    ldr r0, DAT_080bb740                     @ 080bb730 0348
    cmp r4,r0                                @ 080bb732 8442
    bne LAB_080bb738                         @ 080bb734 00d1
    b LAB_080bb82e                           @ 080bb736 7ae0
LAB_080bb738:
    cmp r4,r0                                @ 080bb738 8442
    bgt LAB_080bb744                         @ 080bb73a 03dc
    subs r0,#0x40    @ 080bb73c 4038
    b LAB_080bb76e                           @ 080bb73e 16e0
DAT_080bb740:
    .word  0x000016fa                     @ 080bb740 fa160000
LAB_080bb744:
    ldr r0, DAT_080bb748                     @ 080bb744 0048
    b LAB_080bb76e                           @ 080bb746 12e0
DAT_080bb748:
    .word  0x0000179a                     @ 080bb748 9a170000
LAB_080bb74c:
    ldr r0, DAT_080bb768                     @ 080bb74c 0648
    cmp r4,r0                                @ 080bb74e 8442
    bgt LAB_080bb778                         @ 080bb750 12dc
    subs r0,#0x1    @ 080bb752 0138
    cmp r4,r0                                @ 080bb754 8442
    bge LAB_080bb794                         @ 080bb756 1dda
    subs r0,#0x43    @ 080bb758 4338
    cmp r4,r0                                @ 080bb75a 8442
    beq LAB_080bb794                         @ 080bb75c 1ad0
    cmp r4,r0                                @ 080bb75e 8442
    bgt LAB_080bb76c                         @ 080bb760 04dc
    subs r0,#0x9    @ 080bb762 0938
    b LAB_080bb76e                           @ 080bb764 03e0
    .zero  0x2
DAT_080bb768:
    .word  0x000018bb                     @ 080bb768 bb180000
LAB_080bb76c:
    ldr r0, DAT_080bb774                     @ 080bb76c 0148
LAB_080bb76e:
    cmp r4,r0                                @ 080bb76e 8442
    beq LAB_080bb794                         @ 080bb770 10d0
    b LAB_080bb828                           @ 080bb772 59e0
DAT_080bb774:
    .word  0x000018b5                     @ 080bb774 b5180000
LAB_080bb778:
    ldr r0, DAT_080bb78c                     @ 080bb778 0448
    cmp r4,r0                                @ 080bb77a 8442
    blt LAB_080bb828                         @ 080bb77c 54db
    adds r0,#0x3    @ 080bb77e 0330
    cmp r4,r0                                @ 080bb780 8442
    ble LAB_080bb794                         @ 080bb782 07dd
    ldr r0, DAT_080bb790                     @ 080bb784 0248
    cmp r4,r0                                @ 080bb786 8442
    bne LAB_080bb828                         @ 080bb788 4ed1
    b LAB_080bb82e                           @ 080bb78a 50e0
DAT_080bb78c:
    .word  0x000018bf                     @ 080bb78c bf180000
DAT_080bb790:
    .word  0x000019f1                     @ 080bb790 f1190000
LAB_080bb794:
    .hword 0x4668    @ 080bb794 6846
    movs r1,#0x0    @ 080bb796 0021
    movs r2,#0x18    @ 080bb798 1822
    bl memset                                @ 080bb79a 53f00ff9
    ldrb r1,[r5,#0x2]                        @ 080bb79e a978
    movs r3,#0x2    @ 080bb7a0 0223
    rsbs r3,r3,#0    @ 080bb7a2 5b42
    adds r0,r3,#0x0    @ 080bb7a4 181c
    ands r1,r0    @ 080bb7a6 0140
    ldr r0,[sp,#0x18]                        @ 080bb7a8 0698
    orrs r1,r0    @ 080bb7aa 0143
    movs r0,#0x1f    @ 080bb7ac 1f20
    adds r2,r7,#0x0    @ 080bb7ae 3a1c
    ands r2,r0    @ 080bb7b0 0240
    lsls r2,r2,#0x1    @ 080bb7b2 5200
    subs r3,#0x3d    @ 080bb7b4 3d3b
    adds r0,r3,#0x0    @ 080bb7b6 181c
    ands r1,r0    @ 080bb7b8 0140
    orrs r1,r2    @ 080bb7ba 1143
    strb r1,[r5,#0x2]                        @ 080bb7bc a970
    strh r4,[r5,#0x0]                        @ 080bb7be 2c80
    .hword 0x4641    @ 080bb7c0 4146
    ldr r0,[r1,#0x0]                         @ 080bb7c2 0868
    lsls r1,r0,#0x2    @ 080bb7c4 8100
    lsrs r1,r1,#0x18    @ 080bb7c6 090e
    lsls r1,r1,#0x1    @ 080bb7c8 4900
    lsls r0,r0,#0x12    @ 080bb7ca 8004
    lsrs r0,r0,#0x1f    @ 080bb7cc c00f
    orrs r1,r0    @ 080bb7ce 0143
    lsls r1,r1,#0x6    @ 080bb7d0 8901
    ldr r2, DAT_080bb800                     @ 080bb7d2 0b4a
    adds r0,r2,#0x0    @ 080bb7d4 101c
    ldrh r3,[r5,#0x4]                        @ 080bb7d6 ab88
    ands r0,r3    @ 080bb7d8 1840
    orrs r0,r1    @ 080bb7da 0843
    strh r0,[r5,#0x4]                        @ 080bb7dc a880
    ldrb r1,[r5,#0x3]                        @ 080bb7de e978
    movs r2,#0x31    @ 080bb7e0 3122
    rsbs r2,r2,#0    @ 080bb7e2 5242
    adds r0,r2,#0x0    @ 080bb7e4 101c
    ands r1,r0    @ 080bb7e6 0140
    movs r0,#0x10    @ 080bb7e8 1020
    orrs r1,r0    @ 080bb7ea 0143
    strb r1,[r5,#0x3]                        @ 080bb7ec e970
    .hword 0x4668    @ 080bb7ee 6846
    .hword 0x4653    @ 080bb7f0 5346
    subs r1,r3,r6    @ 080bb7f2 991b
    bl count_effect_node_activations_by_zone @ 080bb7f4 d4f7feff
    movs r1,#0x0    @ 080bb7f8 0021
    cmp r0,#0x0                              @ 080bb7fa 0028
    ble LAB_080bb828                         @ 080bb7fc 14dd
    b LAB_080bb82e                           @ 080bb7fe 16e0
DAT_080bb800:
    .word  0xffff803f                     @ 080bb800 3f80ffff
LAB_080bb804:
    adds r0,r6,#0x0    @ 080bb804 301c
    bl compare_zone_max_scores_by_player     @ 080bb806 f3f7e5fa
    lsrs r1,r0,#0x1f    @ 080bb80a c10f
    b LAB_080bb828                           @ 080bb80c 0ce0
LAB_080bb80e:
    ldr r2,[sp,#0x1c]                        @ 080bb80e 079a
    ldr r0,[r2,#0x0]                         @ 080bb810 1068
    cmp r0,#0x4                              @ 080bb812 0428
    bhi LAB_080bb828                         @ 080bb814 08d8
    b LAB_080bb82e                           @ 080bb816 0ae0
LAB_080bb818:
    .hword 0x4653    @ 080bb818 5346
    subs r0,r3,r6    @ 080bb81a 981b
    bl count_equip_slots_active_only         @ 080bb81c 78f774f9
    movs r1,#0x0    @ 080bb820 0021
    cmp r0,#0x1                              @ 080bb822 0128
    ble LAB_080bb828                         @ 080bb824 00dd
    movs r1,#0x1    @ 080bb826 0121
LAB_080bb828:
    cmp r1,#0x0                              @ 080bb828 0029
    bne LAB_080bb82e                         @ 080bb82a 00d1
    b LAB_080bb98c                           @ 080bb82c aee0
LAB_080bb82e:
    ldr r1, PTR_gP1LifePoints_080bb848       @ 080bb82e 0649
    ldr r2, DAT_080bb84c                     @ 080bb830 064a
    adds r0,r1,r2    @ 080bb832 8818
    str r6,[r0,#0x0]                         @ 080bb834 0660
    .hword 0x4653    @ 080bb836 5346
    ldr r0, DAT_080bb850                     @ 080bb838 0548
    str r3,[r0,#0x0]                         @ 080bb83a 0360
    adds r0,r6,#0x0    @ 080bb83c 301c
    adds r1,r7,#0x0    @ 080bb83e 391c
    movs r2,#0x0    @ 080bb840 0022
    movs r3,#0x5    @ 080bb842 0523
    b LAB_080bb8ee                           @ 080bb844 53e0
    .zero  0x2
PTR_gP1LifePoints_080bb848:
    .word  gP1LifePoints                  @ 080bb848 e0c40102
DAT_080bb84c:
    .word  0x00001d64                     @ 080bb84c 641d0000
DAT_080bb850:
    .word  0x0201e238                     @ 080bb850 38e20102
LAB_080bb854:
    .hword 0x4641    @ 080bb854 4146
    ldrh r0,[r1,#0x6]                        @ 080bb856 c888
    cmp r0,#0x0                              @ 080bb858 0028
    beq LAB_080bb908                         @ 080bb85a 55d0
    movs r2,#0x0    @ 080bb85c 0022
    .hword 0x4691    @ 080bb85e 9146
    ldr r0, DAT_080bb8f4                     @ 080bb860 2448
    cmp r4,r0                                @ 080bb862 8442
    bne LAB_080bb8d2                         @ 080bb864 35d1
    .hword 0x4668    @ 080bb866 6846
    movs r1,#0x0    @ 080bb868 0021
    movs r2,#0x18    @ 080bb86a 1822
    bl memset                                @ 080bb86c 53f0a6f8
    ldrb r1,[r5,#0x2]                        @ 080bb870 a978
    movs r3,#0x2    @ 080bb872 0223
    rsbs r3,r3,#0    @ 080bb874 5b42
    adds r0,r3,#0x0    @ 080bb876 181c
    ands r1,r0    @ 080bb878 0140
    ldr r0,[sp,#0x18]                        @ 080bb87a 0698
    orrs r1,r0    @ 080bb87c 0143
    movs r0,#0x1f    @ 080bb87e 1f20
    adds r2,r7,#0x0    @ 080bb880 3a1c
    ands r2,r0    @ 080bb882 0240
    lsls r2,r2,#0x1    @ 080bb884 5200
    subs r3,#0x3d    @ 080bb886 3d3b
    adds r0,r3,#0x0    @ 080bb888 181c
    ands r1,r0    @ 080bb88a 0140
    orrs r1,r2    @ 080bb88c 1143
    strb r1,[r5,#0x2]                        @ 080bb88e a970
    strh r4,[r5,#0x0]                        @ 080bb890 2c80
    .hword 0x4641    @ 080bb892 4146
    ldr r0,[r1,#0x0]                         @ 080bb894 0868
    lsls r1,r0,#0x2    @ 080bb896 8100
    lsrs r1,r1,#0x18    @ 080bb898 090e
    lsls r1,r1,#0x1    @ 080bb89a 4900
    lsls r0,r0,#0x12    @ 080bb89c 8004
    lsrs r0,r0,#0x1f    @ 080bb89e c00f
    orrs r1,r0    @ 080bb8a0 0143
    lsls r1,r1,#0x6    @ 080bb8a2 8901
    ldr r2, DAT_080bb8f8                     @ 080bb8a4 144a
    adds r0,r2,#0x0    @ 080bb8a6 101c
    ldrh r3,[r5,#0x4]                        @ 080bb8a8 ab88
    ands r0,r3    @ 080bb8aa 1840
    orrs r0,r1    @ 080bb8ac 0843
    strh r0,[r5,#0x4]                        @ 080bb8ae a880
    ldrb r1,[r5,#0x3]                        @ 080bb8b0 e978
    movs r2,#0x31    @ 080bb8b2 3122
    rsbs r2,r2,#0    @ 080bb8b4 5242
    adds r0,r2,#0x0    @ 080bb8b6 101c
    ands r1,r0    @ 080bb8b8 0140
    movs r0,#0x10    @ 080bb8ba 1020
    orrs r1,r0    @ 080bb8bc 0143
    strb r1,[r5,#0x3]                        @ 080bb8be e970
    .hword 0x4668    @ 080bb8c0 6846
    .hword 0x4653    @ 080bb8c2 5346
    subs r1,r3,r6    @ 080bb8c4 991b
    bl count_effect_node_activations_by_zone @ 080bb8c6 d4f795ff
    cmp r0,#0x0                              @ 080bb8ca 0028
    ble LAB_080bb8d2                         @ 080bb8cc 01dd
    movs r0,#0x1    @ 080bb8ce 0120
    .hword 0x4681    @ 080bb8d0 8146
LAB_080bb8d2:
    .hword 0x4649    @ 080bb8d2 4946
    cmp r1,#0x0                              @ 080bb8d4 0029
    beq LAB_080bb98c                         @ 080bb8d6 59d0
    ldr r2, PTR_gP1LifePoints_080bb8fc       @ 080bb8d8 084a
    ldr r3, DAT_080bb900                     @ 080bb8da 094b
    adds r0,r2,r3    @ 080bb8dc d018
    str r6,[r0,#0x0]                         @ 080bb8de 0660
    .hword 0x4650    @ 080bb8e0 5046
    ldr r1, DAT_080bb904                     @ 080bb8e2 0849
    str r0,[r1,#0x0]                         @ 080bb8e4 0860
    adds r0,r6,#0x0    @ 080bb8e6 301c
    adds r1,r7,#0x0    @ 080bb8e8 391c
    movs r2,#0x0    @ 080bb8ea 0022
    movs r3,#0x8    @ 080bb8ec 0823
LAB_080bb8ee:
    bl init_duel_zone_target_slot_refs       @ 080bb8ee dbf791fa
    b LAB_080bb59a                           @ 080bb8f2 52e6
DAT_080bb8f4:
    .word  0x00001005                     @ 080bb8f4 05100000
DAT_080bb8f8:
    .word  0xffff803f                     @ 080bb8f8 3f80ffff
PTR_gP1LifePoints_080bb8fc:
    .word  gP1LifePoints                  @ 080bb8fc e0c40102
DAT_080bb900:
    .word  0x00001d64                     @ 080bb900 641d0000
DAT_080bb904:
    .word  0x0201e238                     @ 080bb904 38e20102
LAB_080bb908:
    movs r2,#0x0    @ 080bb908 0022
    .hword 0x4691    @ 080bb90a 9146
    ldr r0, DAT_080bb9ac                     @ 080bb90c 2748
    cmp r4,r0                                @ 080bb90e 8442
    beq LAB_080bb918                         @ 080bb910 02d0
    ldr r0, DAT_080bb9b0                     @ 080bb912 2748
    cmp r4,r0                                @ 080bb914 8442
    bne LAB_080bb984                         @ 080bb916 35d1
LAB_080bb918:
    .hword 0x4668    @ 080bb918 6846
    movs r1,#0x0    @ 080bb91a 0021
    movs r2,#0x18    @ 080bb91c 1822
    bl memset                                @ 080bb91e 53f04df8
    ldrb r1,[r5,#0x2]                        @ 080bb922 a978
    movs r3,#0x2    @ 080bb924 0223
    rsbs r3,r3,#0    @ 080bb926 5b42
    adds r0,r3,#0x0    @ 080bb928 181c
    ands r1,r0    @ 080bb92a 0140
    ldr r0,[sp,#0x18]                        @ 080bb92c 0698
    orrs r1,r0    @ 080bb92e 0143
    movs r0,#0x1f    @ 080bb930 1f20
    adds r2,r7,#0x0    @ 080bb932 3a1c
    ands r2,r0    @ 080bb934 0240
    lsls r2,r2,#0x1    @ 080bb936 5200
    subs r3,#0x3d    @ 080bb938 3d3b
    adds r0,r3,#0x0    @ 080bb93a 181c
    ands r1,r0    @ 080bb93c 0140
    orrs r1,r2    @ 080bb93e 1143
    strb r1,[r5,#0x2]                        @ 080bb940 a970
    strh r4,[r5,#0x0]                        @ 080bb942 2c80
    .hword 0x4641    @ 080bb944 4146
    ldr r0,[r1,#0x0]                         @ 080bb946 0868
    lsls r1,r0,#0x2    @ 080bb948 8100
    lsrs r1,r1,#0x18    @ 080bb94a 090e
    lsls r1,r1,#0x1    @ 080bb94c 4900
    lsls r0,r0,#0x12    @ 080bb94e 8004
    lsrs r0,r0,#0x1f    @ 080bb950 c00f
    orrs r1,r0    @ 080bb952 0143
    lsls r1,r1,#0x6    @ 080bb954 8901
    ldr r2, DAT_080bb9b4                     @ 080bb956 174a
    adds r0,r2,#0x0    @ 080bb958 101c
    ldrh r3,[r5,#0x4]                        @ 080bb95a ab88
    ands r0,r3    @ 080bb95c 1840
    orrs r0,r1    @ 080bb95e 0843
    strh r0,[r5,#0x4]                        @ 080bb960 a880
    ldrb r1,[r5,#0x3]                        @ 080bb962 e978
    movs r2,#0x31    @ 080bb964 3122
    rsbs r2,r2,#0    @ 080bb966 5242
    adds r0,r2,#0x0    @ 080bb968 101c
    ands r1,r0    @ 080bb96a 0140
    movs r0,#0x10    @ 080bb96c 1020
    orrs r1,r0    @ 080bb96e 0143
    strb r1,[r5,#0x3]                        @ 080bb970 e970
    .hword 0x4668    @ 080bb972 6846
    .hword 0x4653    @ 080bb974 5346
    subs r1,r3,r6    @ 080bb976 991b
    bl count_effect_node_activations_by_zone @ 080bb978 d4f73cff
    cmp r0,#0x0                              @ 080bb97c 0028
    ble LAB_080bb984                         @ 080bb97e 01dd
    movs r0,#0x1    @ 080bb980 0120
    .hword 0x4681    @ 080bb982 8146
LAB_080bb984:
    .hword 0x4649    @ 080bb984 4946
    cmp r1,#0x0                              @ 080bb986 0029
    beq LAB_080bb98c                         @ 080bb988 00d0
    b LAB_080bb5b8                           @ 080bb98a 15e6
LAB_080bb98c:
    movs r2,#0x14    @ 080bb98c 1422
    add r8,r2                                @ 080bb98e 9044
    adds r7,#0x1    @ 080bb990 0137
    cmp r7,#0x4                              @ 080bb992 042f
    bgt LAB_080bb998                         @ 080bb994 00dc
    b LAB_080bb604                           @ 080bb996 35e6
LAB_080bb998:
    movs r0,#0x0    @ 080bb998 0020
LAB_080bb99a:
    add sp,#0x20                             @ 080bb99a 08b0
    pop {r3,r4,r5}                           @ 080bb99c 38bc
    .hword 0x4698    @ 080bb99e 9846
    .hword 0x46a1    @ 080bb9a0 a146
    .hword 0x46aa    @ 080bb9a2 aa46
    pop {r4,r5,r6,r7}                        @ 080bb9a4 f0bc
    pop {r1}                                 @ 080bb9a6 02bc
    bx r1                                    @ 080bb9a8 0847
    .zero  0x2
DAT_080bb9ac:
    .word  0x0000101e                     @ 080bb9ac 1e100000
DAT_080bb9b0:
    .word  0x00001868                     @ 080bb9b0 68180000
DAT_080bb9b4:
    .word  0xffff803f                     @ 080bb9b4 3f80ffff

@ Indirectly called by tick_duel_field_ai_state_machine (0x080bc71c, duel_field state machine driver, indeg=1) via function pointer table, no APCS parameters. More complex AI decision path than dispatch_field_spell_equip_ai_by_phase: reads [0x0201afe0+0x8] phase field. Phase=0: iterates equip candidate pool (base 0x09e48f90, step=8, max 0x45=69 entries), calls try_activate_equip_for_matching_slot. Phase=1: calls count_available_field_zones_for_player (requires >=2), validates no field spell node / effect zone available / equivalence conditions; for each candidate slot runs: check_card_field5_is_nonzero + check_lp_exceeds_spell_copy_threshold + check_dual_field_slot_owner_mismatch + check_field_spell_b_placeable + get_card_extended_stat_field6/field9; on pass calls init_duel_zone_target_slot_refs. Phase=2: calls find_equip_slot_by_player_and_zone_count. Returns 0=candidate registered for activation, 1=no valid candidate. Inputs: none (r0 overwritten; player_id from gP1LifePoints+0x1ce8). Returns: r0=u32 bool (0=candidate registered, 1=no candidate this cycle). Side effects: [0x0201afe0+0x8]:=old+1 (phase advance); [gP1LifePoints+0x1d64]:=player_id; [gP1LifePoints+0x1d58]:=1 (activation ready flag); target slot refs written via init_duel_zone_target_slot_refs. Constants: equip_pool_base=0x09e48f90 (equip candidate pool base, stride=8, max=0x45=69), ai_ctrl_block=0x0201afe0, phase_field_offset=0x8, ready_flag_offset=0x1d58 (activation ready flag, set to 1), target_player_offset=0x1d64.
eval_field_spell_equip_activation_candidate:
    push {r4,r5,r6,r7,lr}                    @ 080bb9b8 f0b5
    .hword 0x4657    @ 080bb9ba 5746
    .hword 0x464e    @ 080bb9bc 4e46
    .hword 0x4645    @ 080bb9be 4546
    push {r5,r6,r7}                          @ 080bb9c0 e0b4
    sub sp,#0x4                              @ 080bb9c2 81b0
    ldr r0, PTR_gP1LifePoints_080bb9dc       @ 080bb9c4 0548
    ldr r1, DAT_080bb9e0                     @ 080bb9c6 0649
    adds r0,r0,r1    @ 080bb9c8 4018
    ldr r6,[r0,#0x0]                         @ 080bb9ca 0668
    ldr r0, DAT_080bb9e4                     @ 080bb9cc 0548
    ldr r0,[r0,#0x8]                         @ 080bb9ce 8068
    cmp r0,#0x0                              @ 080bb9d0 0028
    beq LAB_080bb9ee                         @ 080bb9d2 0cd0
    cmp r0,#0x1                              @ 080bb9d4 0128
    beq LAB_080bba10                         @ 080bb9d6 1bd0
    b LAB_080bbbe4                           @ 080bb9d8 04e1
    .zero  0x2
PTR_gP1LifePoints_080bb9dc:
    .word  gP1LifePoints                  @ 080bb9dc e0c40102
DAT_080bb9e0:
    .word  0x00001ce8                     @ 080bb9e0 e81c0000
DAT_080bb9e4:
    .word  0x0201afe0                     @ 080bb9e4 e0af0102
LAB_080bb9e8:
    ldr r0,[sp,#0x0]                         @ 080bb9e8 0098
    .hword 0x4682    @ 080bb9ea 8246
    b LAB_080bbb7c                           @ 080bb9ec c6e0
LAB_080bb9ee:
    movs r7,#0x0    @ 080bb9ee 0027
    ldr r4, DAT_080bbb28                     @ 080bb9f0 4d4c
LAB_080bb9f2:
    adds r0,r6,#0x0    @ 080bb9f2 301c
    adds r1,r4,#0x0    @ 080bb9f4 211c
    bl try_activate_equip_for_matching_slot  @ 080bb9f6 fff76bfa
    cmp r0,#0x0                              @ 080bb9fa 0028
    beq LAB_080bba00                         @ 080bb9fc 00d0
    b LAB_080bbbcc                           @ 080bb9fe e5e0
LAB_080bba00:
    adds r4,#0x8    @ 080bba00 0834
    adds r7,#0x1    @ 080bba02 0137
    cmp r7,#0x45                             @ 080bba04 452f
    bls LAB_080bb9f2                         @ 080bba06 f4d9
    ldr r1, DAT_080bbb2c                     @ 080bba08 4849
    ldr r0,[r1,#0x8]                         @ 080bba0a 8868
    adds r0,#0x1    @ 080bba0c 0130
    str r0,[r1,#0x8]                         @ 080bba0e 8860
LAB_080bba10:
    adds r0,r6,#0x0    @ 080bba10 301c
    bl count_available_field_zones_for_player @ 080bba12 78f717f9
    cmp r0,#0x1                              @ 080bba16 0128
    bgt LAB_080bba1c                         @ 080bba18 00dc
    b LAB_080bbbe4                           @ 080bba1a e3e0
LAB_080bba1c:
    adds r0,r6,#0x0    @ 080bba1c 301c
    bl check_zone_has_no_field_spell_node    @ 080bba1e 7ff79fff
    cmp r0,#0x0                              @ 080bba22 0028
    bne LAB_080bba28                         @ 080bba24 00d1
    b LAB_080bbbe4                           @ 080bba26 dde0
LAB_080bba28:
    adds r0,r6,#0x0    @ 080bba28 301c
    bl check_effect_zone_available_for_player @ 080bba2a f3f789ff
    cmp r0,#0x0                              @ 080bba2e 0028
    bne LAB_080bba34                         @ 080bba30 00d1
    b LAB_080bbbe4                           @ 080bba32 d7e0
LAB_080bba34:
    movs r3,#0x0    @ 080bba34 0023
    movs r1,#0x1    @ 080bba36 0121
    rsbs r1,r1,#0    @ 080bba38 4942
    .hword 0x468a    @ 080bba3a 8a46
    .hword 0x4650    @ 080bba3c 5046
    str r0,[sp,#0x0]                         @ 080bba3e 0090
    movs r4,#0x1    @ 080bba40 0124
    adds r0,r6,#0x0    @ 080bba42 301c
    ands r0,r4    @ 080bba44 2040
    ldr r2, DAT_080bbb30                     @ 080bba46 3a4a
    ldr r1, DAT_080bbb34                     @ 080bba48 3a49
    muls r0,r1    @ 080bba4a 4843
    adds r0,r0,r2    @ 080bba4c 8018
    adds r1,r0,#0x0    @ 080bba4e 011c
    adds r1,#0x64    @ 080bba50 6431
    movs r7,#0x5    @ 080bba52 0527
LAB_080bba54:
    ldr r0,[r1,#0x0]                         @ 080bba54 0868
    lsls r0,r0,#0x13    @ 080bba56 c004
    cmp r0,#0x0                              @ 080bba58 0028
    beq LAB_080bba6e                         @ 080bba5a 08d0
    ldrh r0,[r1,#0x8]                        @ 080bba5c 0889
    cmp r0,#0x0                              @ 080bba5e 0028
    bne LAB_080bba6e                         @ 080bba60 05d1
    ldr r0,[r1,#0x10]                        @ 080bba62 0869
    lsrs r0,r0,#0x14    @ 080bba64 000d
    ands r0,r4    @ 080bba66 2040
    cmp r0,#0x0                              @ 080bba68 0028
    beq LAB_080bba6e                         @ 080bba6a 00d0
    adds r3,#0x1    @ 080bba6c 0133
LAB_080bba6e:
    adds r1,#0x14    @ 080bba6e 1431
    subs r7,#0x1    @ 080bba70 013f
    cmp r7,#0x0                              @ 080bba72 002f
    bge LAB_080bba54                         @ 080bba74 eeda
    cmp r3,#0x1                              @ 080bba76 012b
    ble LAB_080bba7c                         @ 080bba78 00dd
    b LAB_080bbbe4                           @ 080bba7a b3e0
LAB_080bba7c:
    movs r7,#0x0    @ 080bba7c 0027
    ldr r0, PTR_gP1LifePoints_080bbb38       @ 080bba7e 2e48
    movs r2,#0x1    @ 080bba80 0122
    ands r2,r6    @ 080bba82 3240
    ldr r3, DAT_080bbb34                     @ 080bba84 2b4b
    adds r1,r2,#0x0    @ 080bba86 111c
    muls r1,r3    @ 080bba88 5943
    adds r4,r0,#0x0    @ 080bba8a 041c
    adds r4,#0xc    @ 080bba8c 0c34
    adds r1,r1,r4    @ 080bba8e 0919
    ldr r0,[r1,#0x0]                         @ 080bba90 0868
    cmp r7,r0                                @ 080bba92 8742
    bcs LAB_080bbb7c                         @ 080bba94 72d2
    .hword 0x4690    @ 080bba96 9046
    movs r1,#0x0    @ 080bba98 0021
    .hword 0x4689    @ 080bba9a 8946
LAB_080bba9c:
    .hword 0x4640    @ 080bba9c 4046
    muls r0,r3    @ 080bba9e 5843
    add r0,r9                                @ 080bbaa0 4844
    ldr r1, DAT_080bbb3c                     @ 080bbaa2 2649
    adds r0,r0,r1    @ 080bbaa4 4018
    ldr r0,[r0,#0x0]                         @ 080bbaa6 0068
    lsls r0,r0,#0x13    @ 080bbaa8 c004
    lsrs r4,r0,#0x13    @ 080bbaaa c40c
    adds r0,r4,#0x0    @ 080bbaac 201c
    bl check_card_field5_is_nonzero          @ 080bbaae 8ff74bf9
    cmp r0,#0x0                              @ 080bbab2 0028
    bne LAB_080bbb66                         @ 080bbab4 57d1
    adds r0,r6,#0x0    @ 080bbab6 301c
    adds r1,r4,#0x0    @ 080bbab8 211c
    bl check_lp_exceeds_spell_copy_threshold @ 080bbaba 7ff729ff
    cmp r0,#0x0                              @ 080bbabe 0028
    beq LAB_080bbb66                         @ 080bbac0 51d0
    adds r1,r4,#0x0    @ 080bbac2 211c
    adds r0,r6,#0x0    @ 080bbac4 301c
    bl check_dual_field_slot_owner_mismatch  @ 080bbac6 f3f773fc
    cmp r0,#0x0                              @ 080bbaca 0028
    beq LAB_080bbb66                         @ 080bbacc 4bd0
    adds r0,r4,#0x0    @ 080bbace 201c
    bl check_field_spell_b_placeable         @ 080bbad0 74f794ff
    cmp r0,#0x0                              @ 080bbad4 0028
    bne LAB_080bbb66                         @ 080bbad6 46d1
    movs r5,#0x1    @ 080bbad8 0125
    adds r0,r4,#0x0    @ 080bbada 201c
    bl get_card_extended_stat_field6         @ 080bbadc 33f08cf9
    cmp r0,#0x16                             @ 080bbae0 1628
    bne LAB_080bbafc                         @ 080bbae2 0bd1
    movs r5,#0x0    @ 080bbae4 0025
    adds r0,r4,#0x0    @ 080bbae6 201c
    bl get_card_extended_stat_field9         @ 080bbae8 33f0c8f9
    cmp r0,#0x5                              @ 080bbaec 0528
    beq LAB_080bbafa                         @ 080bbaee 04d0
    ldr r0, DAT_080bbb40                     @ 080bbaf0 1348
    bl count_field_copies_of_card            @ 080bbaf2 76f753fe
    cmp r0,#0x0                              @ 080bbaf6 0028
    beq LAB_080bbafc                         @ 080bbaf8 00d0
LAB_080bbafa:
    movs r5,#0x1    @ 080bbafa 0125
LAB_080bbafc:
    ldr r0, DAT_080bbb34                     @ 080bbafc 0d48
    .hword 0x4641    @ 080bbafe 4146
    muls r1,r0    @ 080bbb00 4143
    adds r0,r1,#0x0    @ 080bbb02 081c
    add r0,r9                                @ 080bbb04 4844
    ldr r1, DAT_080bbb3c                     @ 080bbb06 0d49
    adds r0,r0,r1    @ 080bbb08 4018
    ldr r0,[r0,#0x0]                         @ 080bbb0a 0068
    lsls r0,r0,#0x12    @ 080bbb0c 8004
    lsrs r0,r0,#0x1f    @ 080bbb0e c00f
    cmp r0,r6                                @ 080bbb10 b042
    beq LAB_080bbb16                         @ 080bbb12 00d0
    movs r5,#0x0    @ 080bbb14 0025
LAB_080bbb16:
    ldr r0, DAT_080bbb44                     @ 080bbb16 0b48
    cmp r4,r0                                @ 080bbb18 8442
    beq LAB_080bbb58                         @ 080bbb1a 1dd0
    cmp r4,r0                                @ 080bbb1c 8442
    bgt LAB_080bbb4c                         @ 080bbb1e 15dc
    ldr r0, DAT_080bbb48                     @ 080bbb20 0948
    cmp r4,r0                                @ 080bbb22 8442
    beq LAB_080bbb58                         @ 080bbb24 18d0
    b LAB_080bbb5e                           @ 080bbb26 1ae0
DAT_080bbb28:
    .word  0x09e48f90                     @ 080bbb28 908fe409
DAT_080bbb2c:
    .word  0x0201afe0                     @ 080bbb2c e0af0102
DAT_080bbb30:
    .word  0x0201c510                     @ 080bbb30 10c50102
DAT_080bbb34:
    .word  0x00000868                     @ 080bbb34 68080000
PTR_gP1LifePoints_080bbb38:
    .word  gP1LifePoints                  @ 080bbb38 e0c40102
DAT_080bbb3c:
    .word  0x0201c600                     @ 080bbb3c 00c60102
DAT_080bbb40:
    .word  0x0000049c                     @ 080bbb40 9c040000
DAT_080bbb44:
    .word  0x0000131e                     @ 080bbb44 1e130000
DAT_080bbb48:
    .word  0x000010dd                     @ 080bbb48 dd100000
LAB_080bbb4c:
    ldr r0, DAT_080bbb54                     @ 080bbb4c 0148
    cmp r4,r0                                @ 080bbb4e 8442
    beq LAB_080bbb5c                         @ 080bbb50 04d0
    b LAB_080bbb5e                           @ 080bbb52 04e0
DAT_080bbb54:
    .word  0x0000138f                     @ 080bbb54 8f130000
LAB_080bbb58:
    movs r5,#0x1    @ 080bbb58 0125
    b LAB_080bbb5e                           @ 080bbb5a 00e0
LAB_080bbb5c:
    movs r5,#0x0    @ 080bbb5c 0025
LAB_080bbb5e:
    str r7,[sp,#0x0]                         @ 080bbb5e 0097
    cmp r5,#0x0                              @ 080bbb60 002d
    beq LAB_080bbb66                         @ 080bbb62 00d0
    b LAB_080bb9e8                           @ 080bbb64 40e7
LAB_080bbb66:
    movs r0,#0x4    @ 080bbb66 0420
    add r9,r0                                @ 080bbb68 8144
    adds r7,#0x1    @ 080bbb6a 0137
    ldr r3, DAT_080bbbd0                     @ 080bbb6c 184b
    .hword 0x4640    @ 080bbb6e 4046
    muls r0,r3    @ 080bbb70 5843
    ldr r1, DAT_080bbbd4                     @ 080bbb72 1849
    adds r0,r0,r1    @ 080bbb74 4018
    ldr r0,[r0,#0x0]                         @ 080bbb76 0068
    cmp r7,r0                                @ 080bbb78 8742
    bcc LAB_080bba9c                         @ 080bbb7a 8fd3
LAB_080bbb7c:
    .hword 0x4650    @ 080bbb7c 5046
    cmp r0,#0x0                              @ 080bbb7e 0028
    bge LAB_080bbbb0                         @ 080bbb80 16da
    ldr r1,[sp,#0x0]                         @ 080bbb82 0099
    cmp r1,#0x0                              @ 080bbb84 0029
    blt LAB_080bbbaa                         @ 080bbb86 10db
    adds r0,r6,#0x0    @ 080bbb88 301c
    bl count_equip_slots_active_only         @ 080bbb8a 77f7bdff
    cmp r0,#0x0                              @ 080bbb8e 0028
    bne LAB_080bbbaa                         @ 080bbb90 0bd1
    ldr r2, PTR_gP1LifePoints_080bbbd8       @ 080bbb92 114a
    movs r0,#0x1    @ 080bbb94 0120
    ands r0,r6    @ 080bbb96 3040
    ldr r1, DAT_080bbbd0                     @ 080bbb98 0d49
    muls r0,r1    @ 080bbb9a 4843
    adds r2,#0xc    @ 080bbb9c 0c32
    adds r0,r0,r2    @ 080bbb9e 8018
    ldr r0,[r0,#0x0]                         @ 080bbba0 0068
    cmp r0,#0x4                              @ 080bbba2 0428
    bls LAB_080bbbaa                         @ 080bbba4 01d9
    ldr r0,[sp,#0x0]                         @ 080bbba6 0098
    .hword 0x4682    @ 080bbba8 8246
LAB_080bbbaa:
    .hword 0x4651    @ 080bbbaa 5146
    cmp r1,#0x0                              @ 080bbbac 0029
    blt LAB_080bbbe4                         @ 080bbbae 19db
LAB_080bbbb0:
    ldr r4, PTR_gP1LifePoints_080bbbd8       @ 080bbbb0 094c
    ldr r1, DAT_080bbbdc                     @ 080bbbb2 0a49
    adds r0,r4,r1    @ 080bbbb4 6018
    str r6,[r0,#0x0]                         @ 080bbbb6 0660
    adds r0,r6,#0x0    @ 080bbbb8 301c
    movs r1,#0xb    @ 080bbbba 0b21
    .hword 0x4652    @ 080bbbbc 5246
    movs r3,#0x7    @ 080bbbbe 0723
    bl init_duel_zone_target_slot_refs       @ 080bbbc0 dbf728f9
    ldr r0, DAT_080bbbe0                     @ 080bbbc4 0648
    adds r4,r4,r0    @ 080bbbc6 2418
    movs r0,#0x1    @ 080bbbc8 0120
    str r0,[r4,#0x0]                         @ 080bbbca 2060
LAB_080bbbcc:
    movs r0,#0x0    @ 080bbbcc 0020
    b LAB_080bbbe6                           @ 080bbbce 0ae0
DAT_080bbbd0:
    .word  0x00000868                     @ 080bbbd0 68080000
DAT_080bbbd4:
    .word  0x0201c4ec                     @ 080bbbd4 ecc40102
PTR_gP1LifePoints_080bbbd8:
    .word  gP1LifePoints                  @ 080bbbd8 e0c40102
DAT_080bbbdc:
    .word  0x00001d64                     @ 080bbbdc 641d0000
DAT_080bbbe0:
    .word  0x00001d58                     @ 080bbbe0 581d0000
LAB_080bbbe4:
    movs r0,#0x1    @ 080bbbe4 0120
LAB_080bbbe6:
    add sp,#0x4                              @ 080bbbe6 01b0
    pop {r3,r4,r5}                           @ 080bbbe8 38bc
    .hword 0x4698    @ 080bbbea 9846
    .hword 0x46a1    @ 080bbbec a146
    .hword 0x46aa    @ 080bbbee aa46
    pop {r4,r5,r6,r7}                        @ 080bbbf0 f0bc
    pop {r1}                                 @ 080bbbf2 02bc
    bx r1                                    @ 080bbbf4 0847
    .zero  0x2

@ 由字段咒文放置处理器 FUN_080bbde8 调用 (indeg=1). 入口 r0=player_id -> r7, r1=slot_idx [0..9] -> r6. 先 check_field_spell_slot_placeable(r7, r6); 不可放置返回 0. 计算 gDuelFieldSlots[player*0x868+slot*0x14] 条目; 提取低 13 位 icid -> r5. 多段阈值 binary-search cmp 链: icid=0x0ffa/0x11c3/0x13ab/0x13b0/0x152b/0x152e/0x16ba/0x18bb -> memset + count_effect_node_activations_by_zone (返回 0 或 restriction code); icid=0x11f5 -> slot_count<=5 返回 0 or 1; icid=0x16fa/0x19f1 -> 返回 1; 其余 -> get_card_field_summon_restriction. Side effects: via count_effect_node_activations_by_zone: [0x0201b290+0x4bc] 清零; zone 激活. Constants: ICID_THRESHOLD=0x152b, ICID_SLOT_COUNT_CHECK=0x11f5, player_stride=0x868, slot_size=0x14, gDuelFieldSlots=0x0201c510.
check_field_spell_icid_summon_restriction:
    push {r4,r5,r6,r7,lr}                    @ 080bbbf8 f0b5
    .hword 0x4647    @ 080bbbfa 4746
    push {r7}                                @ 080bbbfc 80b4
    sub sp,#0x18                             @ 080bbbfe 86b0
    adds r7,r0,#0x0    @ 080bbc00 071c
    adds r6,r1,#0x0    @ 080bbc02 0e1c
    bl check_field_spell_slot_placeable      @ 080bbc04 78f7ecfc
    cmp r0,#0x0                              @ 080bbc08 0028
    bne LAB_080bbc0e                         @ 080bbc0a 00d1
    b LAB_080bbdda                           @ 080bbc0c e5e0
LAB_080bbc0e:
    movs r0,#0x1    @ 080bbc0e 0120
    .hword 0x4684    @ 080bbc10 8446
    adds r2,r7,#0x0    @ 080bbc12 3a1c
    ands r2,r0    @ 080bbc14 0240
    lsls r3,r6,#0x2    @ 080bbc16 b300
    adds r0,r3,r6    @ 080bbc18 9819
    lsls r0,r0,#0x2    @ 080bbc1a 8000
    ldr r1, DAT_080bbc5c                     @ 080bbc1c 0f49
    muls r2,r1    @ 080bbc1e 4a43
    adds r0,r0,r2    @ 080bbc20 8018
    ldr r4, DAT_080bbc60                     @ 080bbc22 0f4c
    adds r0,r0,r4    @ 080bbc24 0019
    ldr r0,[r0,#0x0]                         @ 080bbc26 0068
    lsls r0,r0,#0x13    @ 080bbc28 c004
    lsrs r5,r0,#0x13    @ 080bbc2a c50c
    ldr r0, DAT_080bbc64                     @ 080bbc2c 0d48
    .hword 0x4698    @ 080bbc2e 9846
    cmp r5,r0                                @ 080bbc30 8542
    bgt LAB_080bbcb0                         @ 080bbc32 3ddc
    subs r0,#0x1    @ 080bbc34 0138
    cmp r5,r0                                @ 080bbc36 8542
    blt LAB_080bbc3c                         @ 080bbc38 00db
    b LAB_080bbd30                           @ 080bbc3a 79e0
LAB_080bbc3c:
    ldr r0, DAT_080bbc68                     @ 080bbc3c 0a48
    cmp r5,r0                                @ 080bbc3e 8542
    beq LAB_080bbd1c                         @ 080bbc40 6cd0
    cmp r5,r0                                @ 080bbc42 8542
    bgt LAB_080bbc84                         @ 080bbc44 1edc
    subs r0,#0x5a    @ 080bbc46 5a38
    cmp r5,r0                                @ 080bbc48 8542
    beq LAB_080bbd30                         @ 080bbc4a 71d0
    cmp r5,r0                                @ 080bbc4c 8542
    bgt LAB_080bbc70                         @ 080bbc4e 0fdc
    ldr r0, DAT_080bbc6c                     @ 080bbc50 0648
    cmp r5,r0                                @ 080bbc52 8542
    beq LAB_080bbd30                         @ 080bbc54 6cd0
    adds r0,#0x8c    @ 080bbc56 8c30
    b LAB_080bbd00                           @ 080bbc58 52e0
    .zero  0x2
DAT_080bbc5c:
    .word  0x00000868                     @ 080bbc5c 68080000
DAT_080bbc60:
    .word  0x0201c510                     @ 080bbc60 10c50102
DAT_080bbc64:
    .word  0x0000152b                     @ 080bbc64 2b150000
DAT_080bbc68:
    .word  0x000011f5                     @ 080bbc68 f5110000
DAT_080bbc6c:
    .word  0x00000ffa                     @ 080bbc6c fa0f0000
LAB_080bbc70:
    ldr r0, DAT_080bbc80                     @ 080bbc70 0348
    cmp r5,r0                                @ 080bbc72 8542
    beq LAB_080bbd30                         @ 080bbc74 5cd0
    adds r0,#0x2d    @ 080bbc76 2d30
    cmp r5,r0                                @ 080bbc78 8542
    bne LAB_080bbc7e                         @ 080bbc7a 00d1
    b LAB_080bbdc0                           @ 080bbc7c a0e0
LAB_080bbc7e:
    b LAB_080bbdd2                           @ 080bbc7e a8e0
DAT_080bbc80:
    .word  0x000011c3                     @ 080bbc80 c3110000
LAB_080bbc84:
    ldr r0, DAT_080bbc9c                     @ 080bbc84 0548
    cmp r5,r0                                @ 080bbc86 8542
    beq LAB_080bbd30                         @ 080bbc88 52d0
    cmp r5,r0                                @ 080bbc8a 8542
    bgt LAB_080bbca0                         @ 080bbc8c 08dc
    movs r0,#0x90    @ 080bbc8e 9020
    lsls r0,r0,#0x5    @ 080bbc90 4001
    cmp r5,r0                                @ 080bbc92 8542
    beq LAB_080bbd30                         @ 080bbc94 4cd0
    adds r0,#0x27    @ 080bbc96 2730
    b LAB_080bbd00                           @ 080bbc98 32e0
    .zero  0x2
DAT_080bbc9c:
    .word  0x000013ab                     @ 080bbc9c ab130000
LAB_080bbca0:
    ldr r0, DAT_080bbcac                     @ 080bbca0 0248
    cmp r5,r0                                @ 080bbca2 8542
    beq LAB_080bbd30                         @ 080bbca4 44d0
    adds r0,#0x63    @ 080bbca6 6330
    b LAB_080bbd00                           @ 080bbca8 2ae0
    .zero  0x2
DAT_080bbcac:
    .word  0x000013b0                     @ 080bbcac b0130000
LAB_080bbcb0:
    movs r0,#0xbf    @ 080bbcb0 bf20
    lsls r0,r0,#0x5    @ 080bbcb2 4001
    cmp r5,r0                                @ 080bbcb4 8542
    beq LAB_080bbd30                         @ 080bbcb6 3bd0
    cmp r5,r0                                @ 080bbcb8 8542
    bgt LAB_080bbcec                         @ 080bbcba 17dc
    ldr r0, DAT_080bbcd4                     @ 080bbcbc 0548
    cmp r5,r0                                @ 080bbcbe 8542
    beq LAB_080bbd30                         @ 080bbcc0 36d0
    cmp r5,r0                                @ 080bbcc2 8542
    bgt LAB_080bbcdc                         @ 080bbcc4 0adc
    ldr r0, DAT_080bbcd8                     @ 080bbcc6 0448
    cmp r5,r0                                @ 080bbcc8 8542
    beq LAB_080bbd30                         @ 080bbcca 31d0
    adds r0,#0x5    @ 080bbccc 0530
    cmp r5,r0                                @ 080bbcce 8542
    beq LAB_080bbd12                         @ 080bbcd0 1fd0
    b LAB_080bbdd2                           @ 080bbcd2 7ee0
DAT_080bbcd4:
    .word  0x000016ba                     @ 080bbcd4 ba160000
DAT_080bbcd8:
    .word  0x0000152e                     @ 080bbcd8 2e150000
LAB_080bbcdc:
    ldr r0, DAT_080bbce8                     @ 080bbcdc 0248
    cmp r5,r0                                @ 080bbcde 8542
    beq LAB_080bbd12                         @ 080bbce0 17d0
    adds r0,#0xa0    @ 080bbce2 a030
    b LAB_080bbd00                           @ 080bbce4 0ce0
    .zero  0x2
DAT_080bbce8:
    .word  0x000016fa                     @ 080bbce8 fa160000
LAB_080bbcec:
    ldr r0, DAT_080bbd08                     @ 080bbcec 0648
    cmp r5,r0                                @ 080bbcee 8542
    bgt LAB_080bbd0c                         @ 080bbcf0 0cdc
    subs r0,#0x1    @ 080bbcf2 0138
    cmp r5,r0                                @ 080bbcf4 8542
    bge LAB_080bbd30                         @ 080bbcf6 1bda
    subs r0,#0x4c    @ 080bbcf8 4c38
    cmp r5,r0                                @ 080bbcfa 8542
    beq LAB_080bbd30                         @ 080bbcfc 18d0
    adds r0,#0x9    @ 080bbcfe 0930
LAB_080bbd00:
    cmp r5,r0                                @ 080bbd00 8542
    beq LAB_080bbd30                         @ 080bbd02 15d0
    b LAB_080bbdd2                           @ 080bbd04 65e0
    .zero  0x2
DAT_080bbd08:
    .word  0x000018bb                     @ 080bbd08 bb180000
LAB_080bbd0c:
    ldr r0, DAT_080bbd18                     @ 080bbd0c 0248
    cmp r5,r0                                @ 080bbd0e 8542
    bne LAB_080bbdd2                         @ 080bbd10 5fd1
LAB_080bbd12:
    movs r0,#0x1    @ 080bbd12 0120
    b LAB_080bbddc                           @ 080bbd14 62e0
    .zero  0x2
DAT_080bbd18:
    .word  0x000019f1                     @ 080bbd18 f1190000
LAB_080bbd1c:
    movs r1,#0x0    @ 080bbd1c 0021
    adds r0,r4,#0x0    @ 080bbd1e 201c
    subs r0,#0x24    @ 080bbd20 2438
    adds r0,r2,r0    @ 080bbd22 1018
    ldr r0,[r0,#0x0]                         @ 080bbd24 0068
    cmp r0,#0x5                              @ 080bbd26 0528
    bhi LAB_080bbd2c                         @ 080bbd28 00d8
    movs r1,#0x1    @ 080bbd2a 0121
LAB_080bbd2c:
    adds r0,r1,#0x0    @ 080bbd2c 081c
    b LAB_080bbddc                           @ 080bbd2e 55e0
LAB_080bbd30:
    .hword 0x4668    @ 080bbd30 6846
    movs r1,#0x0    @ 080bbd32 0021
    movs r2,#0x18    @ 080bbd34 1822
    bl memset                                @ 080bbd36 52f041fe
    .hword 0x466b    @ 080bbd3a 6b46
    movs r0,#0x1    @ 080bbd3c 0120
    adds r1,r7,#0x0    @ 080bbd3e 391c
    ands r1,r0    @ 080bbd40 0140
    ldrb r2,[r3,#0x2]                        @ 080bbd42 9a78
    movs r0,#0x2    @ 080bbd44 0220
    rsbs r0,r0,#0    @ 080bbd46 4042
    ands r0,r2    @ 080bbd48 1040
    orrs r0,r1    @ 080bbd4a 0843
    strb r0,[r3,#0x2]                        @ 080bbd4c 9870
    movs r2,#0x1f    @ 080bbd4e 1f22
    adds r1,r6,#0x0    @ 080bbd50 311c
    ands r1,r2    @ 080bbd52 1140
    lsls r1,r1,#0x1    @ 080bbd54 4900
    movs r2,#0x3f    @ 080bbd56 3f22
    rsbs r2,r2,#0    @ 080bbd58 5242
    ands r0,r2    @ 080bbd5a 1040
    orrs r0,r1    @ 080bbd5c 0843
    strb r0,[r3,#0x2]                        @ 080bbd5e 9870
    .hword 0x4668    @ 080bbd60 6846
    strh r5,[r0,#0x0]                        @ 080bbd62 0580
    .hword 0x466c    @ 080bbd64 6c46
    movs r1,#0x1    @ 080bbd66 0121
    adds r3,r7,#0x0    @ 080bbd68 3b1c
    ands r3,r1    @ 080bbd6a 0b40
    .hword 0x4642    @ 080bbd6c 4246
    adds r0,r2,r6    @ 080bbd6e 9019
    lsls r0,r0,#0x2    @ 080bbd70 8000
    ldr r2, DAT_080bbdb4                     @ 080bbd72 104a
    muls r2,r3    @ 080bbd74 5a43
    adds r0,r0,r2    @ 080bbd76 8018
    ldr r2, DAT_080bbdb8                     @ 080bbd78 0f4a
    adds r0,r0,r2    @ 080bbd7a 8018
    ldr r0,[r0,#0x0]                         @ 080bbd7c 0068
    lsls r2,r0,#0x2    @ 080bbd7e 8200
    lsrs r2,r2,#0x18    @ 080bbd80 120e
    lsls r2,r2,#0x1    @ 080bbd82 5200
    lsls r0,r0,#0x12    @ 080bbd84 8004
    lsrs r0,r0,#0x1f    @ 080bbd86 c00f
    orrs r2,r0    @ 080bbd88 0243
    lsls r2,r2,#0x6    @ 080bbd8a 9201
    ldr r0, DAT_080bbdbc                     @ 080bbd8c 0b48
    ldrh r3,[r4,#0x4]                        @ 080bbd8e a388
    ands r0,r3    @ 080bbd90 1840
    orrs r0,r2    @ 080bbd92 1043
    strh r0,[r4,#0x4]                        @ 080bbd94 a080
    .hword 0x466b    @ 080bbd96 6b46
    ldrb r2,[r3,#0x3]                        @ 080bbd98 da78
    movs r0,#0x31    @ 080bbd9a 3120
    rsbs r0,r0,#0    @ 080bbd9c 4042
    ands r0,r2    @ 080bbd9e 1040
    movs r2,#0x10    @ 080bbda0 1022
    orrs r0,r2    @ 080bbda2 1043
    strb r0,[r3,#0x3]                        @ 080bbda4 d870
    subs r1,r1,r7    @ 080bbda6 c91b
    .hword 0x4668    @ 080bbda8 6846
    bl count_effect_node_activations_by_zone @ 080bbdaa d4f723fd
    cmp r0,#0x0                              @ 080bbdae 0028
    bne LAB_080bbdd2                         @ 080bbdb0 0fd1
    b LAB_080bbdda                           @ 080bbdb2 12e0
DAT_080bbdb4:
    .word  0x00000868                     @ 080bbdb4 68080000
DAT_080bbdb8:
    .word  0x0201c510                     @ 080bbdb8 10c50102
DAT_080bbdbc:
    .word  0xffff803f                     @ 080bbdbc 3f80ffff
LAB_080bbdc0:
    .hword 0x4661    @ 080bbdc0 6146
    subs r0,r1,r7    @ 080bbdc2 c81b
    movs r1,#0x0    @ 080bbdc4 0021
    movs r2,#0x1    @ 080bbdc6 0122
    movs r3,#0x1    @ 080bbdc8 0123
    bl count_equip_slots_matching_whitelist  @ 080bbdca 77f7a5fe
    cmp r0,#0x1                              @ 080bbdce 0128
    ble LAB_080bbdda                         @ 080bbdd0 03dd
LAB_080bbdd2:
    adds r0,r5,#0x0    @ 080bbdd2 281c
    bl get_card_field_summon_restriction     @ 080bbdd4 8ff78efb
    b LAB_080bbddc                           @ 080bbdd8 00e0
LAB_080bbdda:
    movs r0,#0x0    @ 080bbdda 0020
LAB_080bbddc:
    add sp,#0x18                             @ 080bbddc 06b0
    pop {r3}                                 @ 080bbdde 08bc
    .hword 0x4698    @ 080bbde0 9846
    pop {r4,r5,r6,r7}                        @ 080bbde2 f0bc
    pop {r1}                                 @ 080bbde4 02bc
    bx r1                                    @ 080bbde6 0847

@ 由 score_equip_slot_placement_for_ai 的调用方 hub 调用 (indeg>=2), 为场地魔法卡的装备效果完成目标选择和初始化. 入口 r0=player_id (.hword 0x4680=mov r8,r0), r1=equip_card_slot (sp[0xc]), r2=mode (sp[0x10]). 从 gDuelFieldSlots (0x0201c600) 读取 r1 指定槽的 card word, 提取 card_icid (bits[12:0]) 存 sp[0x14], 提取面向/位置复合值传给 score_equip_slot_placement_for_ai 获取 score; 调用 check_field_spell_card_placeable_strict 确认可放置性. 主循环 (score 次迭代): 对每个候选调用 eval_equip_target_slot_with_score; 返回 -1 则整体返回 -1; target_player==r8 时调用 check_field_spell_icid_summon_restriction 和 init_equip_sub_entry_fields_from_slot; 否则调用 check_equip_cards_share_field7 过滤. 完成后写 [gP1LifePoints+0x1d64] 和 [+0x1d68], 读 equip 数据写 [+0x1d48], 调用 apply_equip_entry_sprite_from_slot_context, 清零 [0x0201b160]. 返回 1=成功, 0=不可放置, -1=无目标. Side effects: [gP1LifePoints+0x1d64/0x1d68] := 0 (equip slot context), [gP1LifePoints+0x1d48] := equip card data, [0x0201b160] := 0 (global state flag). Constants: GY=gDuelFieldSlots=0x0201c600, GP1=gP1LifePoints, STRIDE=0x868, STATE_FLAG=0x0201b160.
execute_field_spell_equip_placement:
    push {r4,r5,r6,r7,lr}                    @ 080bbde8 f0b5
    .hword 0x4657    @ 080bbdea 5746
    .hword 0x464e    @ 080bbdec 4e46
    .hword 0x4645    @ 080bbdee 4546
    push {r5,r6,r7}                          @ 080bbdf0 e0b4
    sub sp,#0x1c                             @ 080bbdf2 87b0
    .hword 0x4680    @ 080bbdf4 8046
    str r1,[sp,#0xc]                         @ 080bbdf6 0391
    str r2,[sp,#0x10]                        @ 080bbdf8 0492
    movs r0,#0x1    @ 080bbdfa 0120
    .hword 0x4641    @ 080bbdfc 4146
    ands r0,r1    @ 080bbdfe 0840
    ldr r2,[sp,#0xc]                         @ 080bbe00 039a
    lsls r1,r2,#0x2    @ 080bbe02 9100
    ldr r2, DAT_080bbe64                     @ 080bbe04 174a
    muls r0,r2    @ 080bbe06 5043
    adds r1,r1,r0    @ 080bbe08 0918
    ldr r0, DAT_080bbe68                     @ 080bbe0a 1748
    adds r1,r1,r0    @ 080bbe0c 0918
    ldr r0,[r1,#0x0]                         @ 080bbe0e 0868
    lsls r1,r0,#0x13    @ 080bbe10 c104
    lsrs r1,r1,#0x13    @ 080bbe12 c90c
    str r1,[sp,#0x14]                        @ 080bbe14 0591
    lsls r1,r0,#0x2    @ 080bbe16 8100
    lsrs r1,r1,#0x18    @ 080bbe18 090e
    lsls r1,r1,#0x1    @ 080bbe1a 4900
    lsls r0,r0,#0x12    @ 080bbe1c 8004
    lsrs r0,r0,#0x1f    @ 080bbe1e c00f
    adds r1,r1,r0    @ 080bbe20 0918
    .hword 0x4640    @ 080bbe22 4046
    ldr r2,[sp,#0x10]                        @ 080bbe24 049a
    bl score_equip_slot_placement_for_ai     @ 080bbe26 f1f713fc
    str r0,[sp,#0x18]                        @ 080bbe2a 0690
    .hword 0x4640    @ 080bbe2c 4046
    bl check_field_spell_card_placeable_strict @ 080bbe2e 7ff7e1fd
    cmp r0,#0x0                              @ 080bbe32 0028
    bne LAB_080bbe3a                         @ 080bbe34 01d1
    movs r0,#0x1    @ 080bbe36 0120
    str r0,[sp,#0x10]                        @ 080bbe38 0490
LAB_080bbe3a:
    movs r1,#0x0    @ 080bbe3a 0021
    .hword 0x468a    @ 080bbe3c 8a46
    ldr r2,[sp,#0x18]                        @ 080bbe3e 069a
    cmp r10,r2                               @ 080bbe40 9245
    bge LAB_080bbeba                         @ 080bbe42 3ada
    add r7,sp,#0x4                           @ 080bbe44 01af
LAB_080bbe46:
    add r0,sp,#0x4                           @ 080bbe46 01a8
    str r0,[sp,#0x0]                         @ 080bbe48 0090
    .hword 0x4640    @ 080bbe4a 4046
    ldr r1,[sp,#0x14]                        @ 080bbe4c 0599
    movs r2,#0x0    @ 080bbe4e 0022
    .hword 0x4653    @ 080bbe50 5346
    bl eval_equip_target_slot_with_score     @ 080bbe52 f1f75dfb
    adds r5,r0,#0x0    @ 080bbe56 051c
    movs r0,#0x1    @ 080bbe58 0120
    rsbs r0,r0,#0    @ 080bbe5a 4042
    cmp r5,r0                                @ 080bbe5c 8542
    bne LAB_080bbe6c                         @ 080bbe5e 05d1
    adds r0,r5,#0x0    @ 080bbe60 281c
    b LAB_080bbf14                           @ 080bbe62 57e0
DAT_080bbe64:
    .word  0x00000868                     @ 080bbe64 68080000
DAT_080bbe68:
    .word  0x0201c600                     @ 080bbe68 00c60102
LAB_080bbe6c:
    lsls r0,r5,#0x18    @ 080bbe6c 2806
    lsrs r1,r0,#0x18    @ 080bbe6e 010e
    .hword 0x4681    @ 080bbe70 8146
    lsls r6,r5,#0x10    @ 080bbe72 2e04
    cmp r8,r1                                @ 080bbe74 8845
    bne LAB_080bbe92                         @ 080bbe76 0cd1
    lsrs r4,r6,#0x18    @ 080bbe78 340e
    .hword 0x4640    @ 080bbe7a 4046
    adds r1,r4,#0x0    @ 080bbe7c 211c
    bl check_field_spell_icid_summon_restriction @ 080bbe7e fff7bbfe
    cmp r0,#0x0                              @ 080bbe82 0028
    beq LAB_080bbe92                         @ 080bbe84 05d0
    .hword 0x4640    @ 080bbe86 4046
    adds r1,r4,#0x0    @ 080bbe88 211c
    bl init_equip_sub_entry_fields_from_slot @ 080bbe8a eff70fff
    movs r0,#0x0    @ 080bbe8e 0020
    b LAB_080bbf14                           @ 080bbe90 40e0
LAB_080bbe92:
    .hword 0x4649    @ 080bbe92 4946
    lsrs r2,r1,#0x18    @ 080bbe94 0a0e
    lsrs r3,r6,#0x18    @ 080bbe96 330e
    .hword 0x4640    @ 080bbe98 4046
    ldr r1,[sp,#0x14]                        @ 080bbe9a 0599
    bl check_equip_cards_share_field7        @ 080bbe9c 77f7a8fc
    cmp r0,#0x0                              @ 080bbea0 0028
    beq LAB_080bbeac                         @ 080bbea2 03d0
    strh r5,[r7,#0x0]                        @ 080bbea4 3d80
    adds r7,#0x2    @ 080bbea6 0237
    movs r2,#0x1    @ 080bbea8 0122
    add r10,r2                               @ 080bbeaa 9244
LAB_080bbeac:
    strh r5,[r7,#0x0]                        @ 080bbeac 3d80
    adds r7,#0x2    @ 080bbeae 0237
    movs r0,#0x1    @ 080bbeb0 0120
    add r10,r0                               @ 080bbeb2 8244
    ldr r1,[sp,#0x18]                        @ 080bbeb4 0699
    cmp r10,r1                               @ 080bbeb6 8a45
    blt LAB_080bbe46                         @ 080bbeb8 c5db
LAB_080bbeba:
    ldr r3, PTR_gP1LifePoints_080bbf24       @ 080bbeba 1a4b
    ldr r2, DAT_080bbf28                     @ 080bbebc 1a4a
    adds r0,r3,r2    @ 080bbebe 9818
    .hword 0x4641    @ 080bbec0 4146
    str r1,[r0,#0x0]                         @ 080bbec2 0160
    adds r2,#0x4    @ 080bbec4 0432
    adds r0,r3,r2    @ 080bbec6 9818
    str r1,[r0,#0x0]                         @ 080bbec8 0160
    ldr r0, DAT_080bbf2c                     @ 080bbeca 1848
    adds r4,r3,r0    @ 080bbecc 1c18
    movs r0,#0x1    @ 080bbece 0120
    ands r0,r1    @ 080bbed0 0840
    ldr r2,[sp,#0xc]                         @ 080bbed2 039a
    lsls r1,r2,#0x2    @ 080bbed4 9100
    ldr r2, DAT_080bbf30                     @ 080bbed6 164a
    muls r0,r2    @ 080bbed8 5043
    adds r1,r1,r0    @ 080bbeda 0918
    movs r0,#0x90    @ 080bbedc 9020
    lsls r0,r0,#0x1    @ 080bbede 4000
    adds r3,r3,r0    @ 080bbee0 1b18
    adds r1,r1,r3    @ 080bbee2 c918
    ldr r1,[r1,#0x0]                         @ 080bbee4 0968
    lsls r0,r1,#0x2    @ 080bbee6 8800
    lsrs r0,r0,#0x18    @ 080bbee8 000e
    lsls r0,r0,#0x1    @ 080bbeea 4000
    lsls r1,r1,#0x12    @ 080bbeec 8904
    lsrs r1,r1,#0x1f    @ 080bbeee c90f
    adds r0,r0,r1    @ 080bbef0 4018
    str r0,[r4,#0x0]                         @ 080bbef2 2060
    movs r0,#0x0    @ 080bbef4 0020
    ldr r1,[sp,#0x10]                        @ 080bbef6 0499
    cmp r1,#0x0                              @ 080bbef8 0029
    bne LAB_080bbefe                         @ 080bbefa 00d1
    movs r0,#0x1    @ 080bbefc 0120
LAB_080bbefe:
    movs r1,#0x0    @ 080bbefe 0021
    movs r2,#0x1    @ 080bbf00 0122
    bl apply_equip_entry_sprite_from_slot_context @ 080bbf02 eaf719f8
    ldr r0, DAT_080bbf34                     @ 080bbf06 0b48
    movs r2,#0xc0    @ 080bbf08 c022
    lsls r2,r2,#0x1    @ 080bbf0a 5200
    adds r0,r0,r2    @ 080bbf0c 8018
    movs r1,#0x0    @ 080bbf0e 0021
    str r1,[r0,#0x0]                         @ 080bbf10 0160
    movs r0,#0x1    @ 080bbf12 0120
LAB_080bbf14:
    add sp,#0x1c                             @ 080bbf14 07b0
    pop {r3,r4,r5}                           @ 080bbf16 38bc
    .hword 0x4698    @ 080bbf18 9846
    .hword 0x46a1    @ 080bbf1a a146
    .hword 0x46aa    @ 080bbf1c aa46
    pop {r4,r5,r6,r7}                        @ 080bbf1e f0bc
    pop {r1}                                 @ 080bbf20 02bc
    bx r1                                    @ 080bbf22 0847
PTR_gP1LifePoints_080bbf24:
    .word  gP1LifePoints                  @ 080bbf24 e0c40102
DAT_080bbf28:
    .word  0x00001d64                     @ 080bbf28 641d0000
DAT_080bbf2c:
    .word  0x00001d48                     @ 080bbf2c 481d0000
DAT_080bbf30:
    .word  0x00000868                     @ 080bbf30 68080000
DAT_080bbf34:
    .word  0x0201afe0                     @ 080bbf34 e0af0102

@ 被 FUN_080bc22c 调用 (indeg>=1, 在 toon world equip 决策链上). 入口 r0=player_id [0..1]. 逻辑: (1) 调用 check_field_spell_card_placeable_strict(player); 失败直接返回 0; (2) 检查 gP1LifePoints[player*0x868+0xc] > 0 (LP 基础检查); (3) 以 r8=0 (loop counter), r9=0 (entry scan 基准) 遍历 gDuelFieldSlots2 (0x0201c600) 条目: 提取 card_id 和 field7_type; 调用 eval_card_placement_flags_default(player, card_type, card_id); 对返回 flags 的 bit4 检查; (4) 对匹配卡牌按 BST 分派 card_id 到多条路径: count_occupied_monster_zones / count_equip_slots_active_only / count_equip_placements_with_chain_check / count_slot_card_pair_allowed_for_card / check_any_pair_slot_available_for_card / count_equippable_slots_for_card / dispatch_effect_handler_by_card_id; 各路径设置 r10 位标志; (5) 通过路径: 写 [gP1LifePoints+0x1d64] := player_id, [gP1LifePoints+0x1d68] := player_id; 构建 OAM slot attr; 调用 apply_equip_entry_sprite_from_slot_context; 返回 1. 失败返回 0. Constants: gP1LifePoints=0x0201c4e0, gDuelFieldSlots2=0x0201c600, player_stride=0x868, card_id_set=[0x13b5, 0x147b, 0x154b, 0x16ec, 0x1870, 0x185d, 0x1905, 0x18cd].
check_field_spell_equip_placement_eligible:
    push {r4,r5,r6,r7,lr}                    @ 080bbf38 f0b5
    .hword 0x4657    @ 080bbf3a 5746
    .hword 0x464e    @ 080bbf3c 4e46
    .hword 0x4645    @ 080bbf3e 4546
    push {r5,r6,r7}                          @ 080bbf40 e0b4
    adds r5,r0,#0x0    @ 080bbf42 051c
    bl check_field_spell_card_placeable_strict @ 080bbf44 7ff756fd
    cmp r0,#0x0                              @ 080bbf48 0028
    bne LAB_080bbf4e                         @ 080bbf4a 00d1
    b LAB_080bc14e                           @ 080bbf4c ffe0
LAB_080bbf4e:
    movs r0,#0x0    @ 080bbf4e 0020
    .hword 0x4681    @ 080bbf50 8146
    ldr r3, PTR_gP1LifePoints_080bbfcc       @ 080bbf52 1e4b
    movs r1,#0x1    @ 080bbf54 0121
    ands r1,r5    @ 080bbf56 2940
    ldr r2, DAT_080bbfd0                     @ 080bbf58 1d4a
    adds r0,r1,#0x0    @ 080bbf5a 081c
    muls r0,r2    @ 080bbf5c 5043
    adds r4,r3,#0x0    @ 080bbf5e 1c1c
    adds r4,#0xc    @ 080bbf60 0c34
    adds r0,r0,r4    @ 080bbf62 0019
    ldr r0,[r0,#0x0]                         @ 080bbf64 0068
    cmp r9,r0                                @ 080bbf66 8145
    bcc LAB_080bbf6c                         @ 080bbf68 00d3
    b LAB_080bc14e                           @ 080bbf6a f0e0
LAB_080bbf6c:
    adds r7,r1,#0x0    @ 080bbf6c 0f1c
    movs r1,#0x0    @ 080bbf6e 0021
    .hword 0x4688    @ 080bbf70 8846
LAB_080bbf72:
    adds r6,r7,#0x0    @ 080bbf72 3e1c
    muls r6,r2    @ 080bbf74 5643
    .hword 0x4642    @ 080bbf76 4246
    adds r0,r2,r6    @ 080bbf78 9019
    ldr r1, DAT_080bbfd4                     @ 080bbf7a 1649
    adds r0,r0,r1    @ 080bbf7c 4018
    ldr r0,[r0,#0x0]                         @ 080bbf7e 0068
    lsls r1,r0,#0x13    @ 080bbf80 c104
    lsrs r4,r1,#0x13    @ 080bbf82 cc0c
    lsls r1,r0,#0x2    @ 080bbf84 8100
    lsrs r1,r1,#0x18    @ 080bbf86 090e
    lsls r1,r1,#0x1    @ 080bbf88 4900
    lsls r0,r0,#0x12    @ 080bbf8a 8004
    lsrs r0,r0,#0x1f    @ 080bbf8c c00f
    adds r1,r1,r0    @ 080bbf8e 0918
    adds r0,r5,#0x0    @ 080bbf90 281c
    bl eval_card_placement_flags_default     @ 080bbf92 e8f77ffb
    movs r1,#0x10    @ 080bbf96 1021
    ands r1,r0    @ 080bbf98 0140
    cmp r1,#0x0                              @ 080bbf9a 0029
    bne LAB_080bbfa0                         @ 080bbf9c 00d1
    b LAB_080bc134                           @ 080bbf9e c9e0
LAB_080bbfa0:
    movs r2,#0x0    @ 080bbfa0 0022
    .hword 0x4692    @ 080bbfa2 9246
    ldr r0, DAT_080bbfd8                     @ 080bbfa4 0c48
    cmp r4,r0                                @ 080bbfa6 8442
    beq LAB_080bc034                         @ 080bbfa8 44d0
    cmp r4,r0                                @ 080bbfaa 8442
    bgt LAB_080bbfec                         @ 080bbfac 1edc
    ldr r0, DAT_080bbfdc                     @ 080bbfae 0b48
    cmp r4,r0                                @ 080bbfb0 8442
    beq LAB_080bc03e                         @ 080bbfb2 44d0
    cmp r4,r0                                @ 080bbfb4 8442
    bgt LAB_080bbfe0                         @ 080bbfb6 13dc
    subs r0,#0x2d    @ 080bbfb8 2d38
    cmp r4,r0                                @ 080bbfba 8442
    ble LAB_080bbfc0                         @ 080bbfbc 00dd
    b LAB_080bc0e0                           @ 080bbfbe 8fe0
LAB_080bbfc0:
    subs r0,#0x2    @ 080bbfc0 0238
    cmp r4,r0                                @ 080bbfc2 8442
    bge LAB_080bbfc8                         @ 080bbfc4 00da
    b LAB_080bc0e0                           @ 080bbfc6 8be0
LAB_080bbfc8:
    b LAB_080bc0e6                           @ 080bbfc8 8de0
    .zero  0x2
PTR_gP1LifePoints_080bbfcc:
    .word  gP1LifePoints                  @ 080bbfcc e0c40102
DAT_080bbfd0:
    .word  0x00000868                     @ 080bbfd0 68080000
DAT_080bbfd4:
    .word  0x0201c600                     @ 080bbfd4 00c60102
DAT_080bbfd8:
    .word  0x0000154b                     @ 080bbfd8 4b150000
DAT_080bbfdc:
    .word  0x000013b5                     @ 080bbfdc b5130000
LAB_080bbfe0:
    ldr r0, DAT_080bbfe8                     @ 080bbfe0 0148
    cmp r4,r0                                @ 080bbfe2 8442
    beq LAB_080bc024                         @ 080bbfe4 1ed0
    b LAB_080bc0e0                           @ 080bbfe6 7be0
DAT_080bbfe8:
    .word  0x0000147b                     @ 080bbfe8 7b140000
LAB_080bbfec:
    ldr r1, DAT_080bc004                     @ 080bbfec 0549
    cmp r4,r1                                @ 080bbfee 8c42
    beq LAB_080bc0a0                         @ 080bbff0 56d0
    cmp r4,r1                                @ 080bbff2 8c42
    bgt LAB_080bc010                         @ 080bbff4 0cdc
    ldr r0, DAT_080bc008                     @ 080bbff6 0448
    cmp r4,r0                                @ 080bbff8 8442
    beq LAB_080bc0e6                         @ 080bbffa 74d0
    ldr r0, DAT_080bc00c                     @ 080bbffc 0348
    cmp r4,r0                                @ 080bbffe 8442
    beq LAB_080bc0c0                         @ 080bc000 5ed0
    b LAB_080bc0e0                           @ 080bc002 6de0
DAT_080bc004:
    .word  0x00001870                     @ 080bc004 70180000
DAT_080bc008:
    .word  0x000016ec                     @ 080bc008 ec160000
DAT_080bc00c:
    .word  0x0000185d                     @ 080bc00c 5d180000
LAB_080bc010:
    ldr r0, DAT_080bc020                     @ 080bc010 0348
    cmp r4,r0                                @ 080bc012 8442
    beq LAB_080bc05a                         @ 080bc014 21d0
    adds r0,#0xb7    @ 080bc016 b730
    cmp r4,r0                                @ 080bc018 8442
    beq LAB_080bc068                         @ 080bc01a 25d0
    b LAB_080bc0e0                           @ 080bc01c 60e0
    .zero  0x2
DAT_080bc020:
    .word  0x00001905                     @ 080bc020 05190000
LAB_080bc024:
    ldr r1, DAT_080bc030                     @ 080bc024 0249
    adds r0,r1,r6    @ 080bc026 8819
    ldr r0,[r0,#0x0]                         @ 080bc028 0068
    cmp r0,#0x1                              @ 080bc02a 0128
    bne LAB_080bc0e0                         @ 080bc02c 58d1
    b LAB_080bc0e6                           @ 080bc02e 5ae0
DAT_080bc030:
    .word  0x0201c4ec                     @ 080bc030 ecc40102
LAB_080bc034:
    movs r2,#0x1    @ 080bc034 0122
    subs r0,r2,r5    @ 080bc036 501b
    bl count_occupied_monster_zones          @ 080bc038 77f7a6f8
    b LAB_080bc046                           @ 080bc03c 03e0
LAB_080bc03e:
    movs r1,#0x1    @ 080bc03e 0121
    subs r0,r1,r5    @ 080bc040 481b
    bl count_equip_slots_active_only         @ 080bc042 77f761fd
LAB_080bc046:
    cmp r0,#0x0                              @ 080bc046 0028
    beq LAB_080bc0e0                         @ 080bc048 4ad0
    adds r0,r5,#0x0    @ 080bc04a 281c
    adds r1,r4,#0x0    @ 080bc04c 211c
    movs r2,#0x1    @ 080bc04e 0122
    bl count_equip_placements_with_chain_check @ 080bc050 77f732fc
    cmp r0,#0x2                              @ 080bc054 0228
    ble LAB_080bc0e0                         @ 080bc056 43dd
    b LAB_080bc0e6                           @ 080bc058 45e0
LAB_080bc05a:
    adds r0,r5,#0x0    @ 080bc05a 281c
    adds r1,r4,#0x0    @ 080bc05c 211c
    bl count_slot_card_pair_allowed_for_card @ 080bc05e 76f78dff
    cmp r0,#0x0                              @ 080bc062 0028
    bne LAB_080bc0e0                         @ 080bc064 3cd1
    b LAB_080bc0e6                           @ 080bc066 3ee0
LAB_080bc068:
    adds r0,r5,#0x0    @ 080bc068 281c
    bl count_slot_card_pair_allowed_for_card @ 080bc06a 76f787ff
    cmp r0,#0x0                              @ 080bc06e 0028
    bne LAB_080bc0e6                         @ 080bc070 39d1
    adds r0,r5,#0x0    @ 080bc072 281c
    ldr r1, DAT_080bc094                     @ 080bc074 0749
    bl check_any_pair_slot_available_for_card @ 080bc076 f3f74dfc
    cmp r0,#0x0                              @ 080bc07a 0028
    beq LAB_080bc0e0                         @ 080bc07c 30d0
    adds r0,r5,#0x0    @ 080bc07e 281c
    ldr r1, DAT_080bc098                     @ 080bc080 0549
    bl check_any_pair_slot_available_for_card @ 080bc082 f3f747fc
    cmp r0,#0x0                              @ 080bc086 0028
    bne LAB_080bc0e6                         @ 080bc088 2dd1
    adds r0,r5,#0x0    @ 080bc08a 281c
    ldr r1, DAT_080bc09c                     @ 080bc08c 0349
    bl check_any_pair_slot_available_for_card @ 080bc08e f3f741fc
    b LAB_080bc0b4                           @ 080bc092 0fe0
DAT_080bc094:
    .word  0x000018f6                     @ 080bc094 f6180000
DAT_080bc098:
    .word  0x000012e5                     @ 080bc098 e5120000
DAT_080bc09c:
    .word  0x000018fe                     @ 080bc09c fe180000
LAB_080bc0a0:
    adds r0,r5,#0x0    @ 080bc0a0 281c
    adds r1,r4,#0x0    @ 080bc0a2 211c
    bl count_slot_card_pair_allowed_for_card @ 080bc0a4 76f76aff
    cmp r0,#0x0                              @ 080bc0a8 0028
    bne LAB_080bc0e6                         @ 080bc0aa 1cd1
    adds r0,r5,#0x0    @ 080bc0ac 281c
    ldr r1, DAT_080bc0bc                     @ 080bc0ae 0349
    bl count_slot_card_pair_allowed_for_card @ 080bc0b0 76f764ff
LAB_080bc0b4:
    cmp r0,#0x0                              @ 080bc0b4 0028
    beq LAB_080bc0e0                         @ 080bc0b6 13d0
    b LAB_080bc0e6                           @ 080bc0b8 15e0
    .zero  0x2
DAT_080bc0bc:
    .word  0x000018f6                     @ 080bc0bc f6180000
LAB_080bc0c0:
    adds r0,r5,#0x0    @ 080bc0c0 281c
    movs r1,#0x1    @ 080bc0c2 0121
    rsbs r1,r1,#0    @ 080bc0c4 4942
    bl count_equippable_slots_for_card       @ 080bc0c6 77f787fc
    cmp r0,#0x0                              @ 080bc0ca 0028
    beq LAB_080bc0e0                         @ 080bc0cc 08d0
    adds r0,r5,#0x0    @ 080bc0ce 281c
    adds r1,r4,#0x0    @ 080bc0d0 211c
    movs r2,#0x0    @ 080bc0d2 0022
    bl dispatch_effect_handler_by_card_id    @ 080bc0d4 d1f7ecfc
    rsbs r1,r0,#0    @ 080bc0d8 4142
    orrs r1,r0    @ 080bc0da 0143
    lsrs r1,r1,#0x1f    @ 080bc0dc c90f
    .hword 0x468a    @ 080bc0de 8a46
LAB_080bc0e0:
    .hword 0x4652    @ 080bc0e0 5246
    cmp r2,#0x0                              @ 080bc0e2 002a
    beq LAB_080bc134                         @ 080bc0e4 26d0
LAB_080bc0e6:
    ldr r1, PTR_gP1LifePoints_080bc120       @ 080bc0e6 0e49
    ldr r2, DAT_080bc124                     @ 080bc0e8 0e4a
    adds r0,r1,r2    @ 080bc0ea 8818
    str r5,[r0,#0x0]                         @ 080bc0ec 0560
    adds r2,#0x4    @ 080bc0ee 0432
    adds r0,r1,r2    @ 080bc0f0 8818
    str r5,[r0,#0x0]                         @ 080bc0f2 0560
    ldr r0, DAT_080bc128                     @ 080bc0f4 0c48
    muls r0,r7    @ 080bc0f6 7843
    add r0,r8                                @ 080bc0f8 4044
    ldr r1, DAT_080bc12c                     @ 080bc0fa 0c49
    adds r0,r0,r1    @ 080bc0fc 4018
    ldr r1,[r0,#0x0]                         @ 080bc0fe 0168
    lsls r0,r1,#0x2    @ 080bc100 8800
    lsrs r0,r0,#0x18    @ 080bc102 000e
    lsls r0,r0,#0x1    @ 080bc104 4000
    lsls r1,r1,#0x12    @ 080bc106 8904
    lsrs r1,r1,#0x1f    @ 080bc108 c90f
    adds r0,r0,r1    @ 080bc10a 4018
    ldr r2, DAT_080bc130                     @ 080bc10c 084a
    str r0,[r2,#0x0]                         @ 080bc10e 1060
    movs r0,#0x1    @ 080bc110 0120
    movs r1,#0x0    @ 080bc112 0021
    movs r2,#0x1    @ 080bc114 0122
    bl apply_equip_entry_sprite_from_slot_context @ 080bc116 e9f70fff
    movs r0,#0x1    @ 080bc11a 0120
    b LAB_080bc150                           @ 080bc11c 18e0
    .zero  0x2
PTR_gP1LifePoints_080bc120:
    .word  gP1LifePoints                  @ 080bc120 e0c40102
DAT_080bc124:
    .word  0x00001d64                     @ 080bc124 641d0000
DAT_080bc128:
    .word  0x00000868                     @ 080bc128 68080000
DAT_080bc12c:
    .word  0x0201c600                     @ 080bc12c 00c60102
DAT_080bc130:
    .word  0x0201e228                     @ 080bc130 28e20102
LAB_080bc134:
    movs r0,#0x4    @ 080bc134 0420
    add r8,r0                                @ 080bc136 8044
    movs r1,#0x1    @ 080bc138 0121
    add r9,r1                                @ 080bc13a 8944
    ldr r2, DAT_080bc160                     @ 080bc13c 084a
    adds r0,r7,#0x0    @ 080bc13e 381c
    muls r0,r2    @ 080bc140 5043
    ldr r1, DAT_080bc164                     @ 080bc142 0849
    adds r0,r0,r1    @ 080bc144 4018
    ldr r0,[r0,#0x0]                         @ 080bc146 0068
    cmp r9,r0                                @ 080bc148 8145
    bcs LAB_080bc14e                         @ 080bc14a 00d2
    b LAB_080bbf72                           @ 080bc14c 11e7
LAB_080bc14e:
    movs r0,#0x0    @ 080bc14e 0020
LAB_080bc150:
    pop {r3,r4,r5}                           @ 080bc150 38bc
    .hword 0x4698    @ 080bc152 9846
    .hword 0x46a1    @ 080bc154 a146
    .hword 0x46aa    @ 080bc156 aa46
    pop {r4,r5,r6,r7}                        @ 080bc158 f0bc
    pop {r1}                                 @ 080bc15a 02bc
    bx r1                                    @ 080bc15c 0847
    .zero  0x2
DAT_080bc160:
    .word  0x00000868                     @ 080bc160 68080000
DAT_080bc164:
    .word  0x0201c4ec                     @ 080bc164 ecc40102

@ 被 dispatch_equip_field_scan_sequence (0x080bc592 内) 及上级循环调用 (indeg>=2). 入口 r4=sp[0x1ce8]=player_side (从 gP1LifePoints+0x1ce8 读取). 读 gDuelBattleState (0x0201afe0)[+0x8]=field_state [0..4]; 超出范围跳默认返回. 5-case switch: case_0: 清零 [+0x180]; toon_flag 检查 -> check_player_lp_exceeds_toon_world_cost + check_field_spell_card_placeable_strict/check_field_spell_group_placeable -> count_available_effect_zones -> find_best_equip_target_slot_for_player x2; 成功: gDuelBattleState[+8]++; 失败同. case_1: compare_zone_max_scores_by_player -> compute_equip_zone_score_with_cache; 失败: [+0xc]=0+[+8]++. case_2: dispatch_equip_activation_full_sequence -> 若成功 [+8]=0; 失败 [+8]++. case_3: scan_all_effect_zone_entries_for_equip_activation -> 成功 [+8]=0; 失败 [+8]++. case_4: 大型 monster_zone+field_spell slot 扫描循环. 返回 r0=u32 (sub-call 返回值或 [+8]++ 后的 advance 值). Side effects: [gDuelBattleState+0x8]+=1 (field_state advance) 或 :=0 (reset on success); [gDuelBattleState+0xc]:=0 (case_1 失败); [gDuelBattleState+0x180]:=0 (case_0 清零缓存). Constants: gDuelBattleState=0x0201afe0, gP1LifePoints=0x0201c4e0, field_state_offset=0x8, toon_flag_offset=0x1cec.
dispatch_equip_activation_by_field_state:
    push {r4,r5,r6,lr}                       @ 080bc168 70b5
    sub sp,#0x4                              @ 080bc16a 81b0
    ldr r0, PTR_gP1LifePoints_080bc18c       @ 080bc16c 0748
    ldr r2, DAT_080bc190                     @ 080bc16e 084a
    adds r1,r0,r2    @ 080bc170 8118
    ldr r4,[r1,#0x0]                         @ 080bc172 0c68
    ldr r1, DAT_080bc194                     @ 080bc174 0749
    ldr r2,[r1,#0x8]                         @ 080bc176 8a68
    adds r6,r0,#0x0    @ 080bc178 061c
    adds r3,r1,#0x0    @ 080bc17a 0b1c
    cmp r2,#0x4                              @ 080bc17c 042a
    bls LAB_080bc182                         @ 080bc17e 00d9
    b switchD_080bc18a__default              @ 080bc180 fce0
LAB_080bc182:
    lsls r0,r2,#0x2    @ 080bc182 9000
    ldr r1, DAT_080bc198                     @ 080bc184 0449
    adds r0,r0,r1    @ 080bc186 4018
    ldr r0,[r0,#0x0]                         @ 080bc188 0068
switchD_080bc18a__switchD:
    .hword 0x4687    @ 080bc18a 8746
PTR_gP1LifePoints_080bc18c:
    .word  gP1LifePoints                  @ 080bc18c e0c40102
DAT_080bc190:
    .word  0x00001ce8                     @ 080bc190 e81c0000
DAT_080bc194:
    .word  0x0201afe0                     @ 080bc194 e0af0102
DAT_080bc198:
    .word  0x080bc19c                     @ 080bc198 9cc10b08
switchD_080bc18a__switchdataD_080bc19c:
    .word  0x080bc1b0                     @ 080bc19c b0c10b08
    .word  0x080bc298                     @ 080bc1a0 98c20b08
    .word  0x080bc2bc                     @ 080bc1a4 bcc20b08
    .word  0x080bc2d4                     @ 080bc1a8 d4c20b08
    .word  0x080bc2f8                     @ 080bc1ac f8c20b08
switchD_080bc18a__caseD_0:
    movs r0,#0xc0    @ 080bc1b0 c020
    lsls r0,r0,#0x1    @ 080bc1b2 4000
    adds r1,r3,r0    @ 080bc1b4 1918
    movs r0,#0x0    @ 080bc1b6 0020
    str r0,[r1,#0x0]                         @ 080bc1b8 0860
    ldr r1, DAT_080bc21c                     @ 080bc1ba 1849
    adds r0,r6,r1    @ 080bc1bc 7018
    ldr r0,[r0,#0x0]                         @ 080bc1be 0068
    cmp r0,#0x0                              @ 080bc1c0 0028
    bne LAB_080bc1c6                         @ 080bc1c2 00d1
    b switchD_080bc18a__default              @ 080bc1c4 dae0
LAB_080bc1c6:
    movs r5,#0x1    @ 080bc1c6 0125
    adds r0,r4,#0x0    @ 080bc1c8 201c
    ands r0,r5    @ 080bc1ca 2840
    ldr r1, DAT_080bc220                     @ 080bc1cc 1449
    muls r0,r1    @ 080bc1ce 4843
    movs r2,#0x8e    @ 080bc1d0 8e22
    lsls r2,r2,#0x1    @ 080bc1d2 5200
    adds r1,r6,r2    @ 080bc1d4 b118
    adds r0,r0,r1    @ 080bc1d6 4018
    ldr r0,[r0,#0x0]                         @ 080bc1d8 0068
    lsrs r0,r0,#0x11    @ 080bc1da 400c
    ands r0,r5    @ 080bc1dc 2840
    cmp r0,#0x0                              @ 080bc1de 0028
    bne LAB_080bc212                         @ 080bc1e0 17d1
    adds r0,r4,#0x0    @ 080bc1e2 201c
    bl check_player_lp_exceeds_toon_world_cost @ 080bc1e4 f0f704fd
    cmp r0,#0x0                              @ 080bc1e8 0028
    beq LAB_080bc212                         @ 080bc1ea 12d0
    adds r0,r4,#0x0    @ 080bc1ec 201c
    bl check_field_spell_card_placeable_strict @ 080bc1ee 7ff701fc
    cmp r0,#0x0                              @ 080bc1f2 0028
    bne LAB_080bc200                         @ 080bc1f4 04d1
    adds r0,r4,#0x0    @ 080bc1f6 201c
    bl check_field_spell_group_placeable     @ 080bc1f8 7ff7c2fb
    cmp r0,#0x0                              @ 080bc1fc 0028
    beq LAB_080bc212                         @ 080bc1fe 08d0
LAB_080bc200:
    subs r0,r5,r4    @ 080bc200 281b
    ldr r1, DAT_080bc224                     @ 080bc202 0849
    movs r5,#0x1    @ 080bc204 0125
    rsbs r5,r5,#0    @ 080bc206 6d42
    adds r2,r5,#0x0    @ 080bc208 2a1c
    bl count_available_effect_zones          @ 080bc20a 76f723fa
    cmp r0,#0x0                              @ 080bc20e 0028
    ble LAB_080bc22c                         @ 080bc210 0cdd
LAB_080bc212:
    ldr r1, DAT_080bc228                     @ 080bc212 0549
    ldr r0,[r1,#0x8]                         @ 080bc214 8868
    adds r0,#0x1    @ 080bc216 0130
    b LAB_080bc370                           @ 080bc218 aae0
    .zero  0x2
DAT_080bc21c:
    .word  0x00001cec                     @ 080bc21c ec1c0000
DAT_080bc220:
    .word  0x00000868                     @ 080bc220 68080000
DAT_080bc224:
    .word  0x00001102                     @ 080bc224 02110000
DAT_080bc228:
    .word  0x0201afe0                     @ 080bc228 e0af0102
LAB_080bc22c:
    adds r0,r4,#0x0    @ 080bc22c 201c
    bl check_field_spell_equip_placement_eligible @ 080bc22e fff783fe
    cmp r0,#0x0                              @ 080bc232 0028
    beq LAB_080bc238                         @ 080bc234 00d0
    b LAB_080bc372                           @ 080bc236 9ce0
LAB_080bc238:
    adds r0,r4,#0x0    @ 080bc238 201c
    bl check_field_spell_card_placeable_strict @ 080bc23a 7ff7dbfb
    cmp r0,#0x0                              @ 080bc23e 0028
    beq LAB_080bc28c                         @ 080bc240 24d0
    adds r0,r4,#0x0    @ 080bc242 201c
    movs r1,#0x1    @ 080bc244 0121
    bl resolve_equip_target_slot_for_player  @ 080bc246 f1f731f9
    cmp r0,#0x0                              @ 080bc24a 0028
    blt LAB_080bc254                         @ 080bc24c 02db
    adds r0,r4,#0x0    @ 080bc24e 201c
    movs r1,#0x1    @ 080bc250 0121
    b LAB_080bc262                           @ 080bc252 06e0
LAB_080bc254:
    adds r0,r4,#0x0    @ 080bc254 201c
    bl compute_equip_zone_score_with_cache   @ 080bc256 f4f79ffe
    cmp r0,#0x0                              @ 080bc25a 0028
    beq LAB_080bc268                         @ 080bc25c 04d0
    adds r0,r4,#0x0    @ 080bc25e 201c
    movs r1,#0x0    @ 080bc260 0021
LAB_080bc262:
    bl find_best_equip_target_slot_for_player @ 080bc262 f4f757ff
    adds r5,r0,#0x0    @ 080bc266 051c
LAB_080bc268:
    movs r0,#0x1    @ 080bc268 0120
    rsbs r0,r0,#0    @ 080bc26a 4042
    cmp r5,r0                                @ 080bc26c 8542
    bne LAB_080bc27a                         @ 080bc26e 04d1
    adds r0,r4,#0x0    @ 080bc270 201c
    adds r1,r5,#0x0    @ 080bc272 291c
    bl find_best_equip_target_slot_for_player @ 080bc274 f4f74eff
    adds r5,r0,#0x0    @ 080bc278 051c
LAB_080bc27a:
    cmp r5,#0x0                              @ 080bc27a 002d
    blt LAB_080bc28c                         @ 080bc27c 06db
    adds r0,r4,#0x0    @ 080bc27e 201c
    adds r1,r5,#0x0    @ 080bc280 291c
    movs r2,#0x0    @ 080bc282 0022
    bl execute_field_spell_equip_placement   @ 080bc284 fff7b0fd
    cmp r0,#0x0                              @ 080bc288 0028
    beq LAB_080bc372                         @ 080bc28a 72d0
LAB_080bc28c:
    ldr r1, DAT_080bc294                     @ 080bc28c 0149
    ldr r0,[r1,#0x8]                         @ 080bc28e 8868
    adds r0,#0x1    @ 080bc290 0130
    b LAB_080bc370                           @ 080bc292 6de0
DAT_080bc294:
    .word  0x0201afe0                     @ 080bc294 e0af0102
switchD_080bc18a__caseD_1:
    adds r0,r4,#0x0    @ 080bc298 201c
    bl compare_zone_max_scores_by_player     @ 080bc29a f2f79bfd
    cmp r0,#0x0                              @ 080bc29e 0028
    blt LAB_080bc2ac                         @ 080bc2a0 04db
    adds r0,r4,#0x0    @ 080bc2a2 201c
    bl compute_equip_zone_score_with_cache   @ 080bc2a4 f4f778fe
    cmp r0,#0x0                              @ 080bc2a8 0028
    bne switchD_080bc18a__default            @ 080bc2aa 67d1
LAB_080bc2ac:
    ldr r1, DAT_080bc2b8                     @ 080bc2ac 0249
    movs r0,#0x0    @ 080bc2ae 0020
    str r0,[r1,#0xc]                         @ 080bc2b0 c860
    ldr r0,[r1,#0x8]                         @ 080bc2b2 8868
    adds r0,#0x1    @ 080bc2b4 0130
    b LAB_080bc370                           @ 080bc2b6 5be0
DAT_080bc2b8:
    .word  0x0201afe0                     @ 080bc2b8 e0af0102
switchD_080bc18a__caseD_2:
    adds r0,r4,#0x0    @ 080bc2bc 201c
    bl dispatch_equip_activation_full_sequence @ 080bc2be fff7a9f8
    cmp r0,#0x0                              @ 080bc2c2 0028
    bne LAB_080bc2de                         @ 080bc2c4 0bd1
    ldr r1, DAT_080bc2d0                     @ 080bc2c6 0249
    ldr r0,[r1,#0x8]                         @ 080bc2c8 8868
    adds r0,#0x1    @ 080bc2ca 0130
    b LAB_080bc370                           @ 080bc2cc 50e0
    .zero  0x2
DAT_080bc2d0:
    .word  0x0201afe0                     @ 080bc2d0 e0af0102
switchD_080bc18a__caseD_3:
    adds r0,r4,#0x0    @ 080bc2d4 201c
    bl scan_all_effect_zone_entries_for_equip_activation @ 080bc2d6 fff741f8
    cmp r0,#0x0                              @ 080bc2da 0028
    beq LAB_080bc2ec                         @ 080bc2dc 06d0
LAB_080bc2de:
    ldr r1, DAT_080bc2e8                     @ 080bc2de 0249
    movs r0,#0x0    @ 080bc2e0 0020
    str r0,[r1,#0x8]                         @ 080bc2e2 8860
    b LAB_080bc37e                           @ 080bc2e4 4be0
    .zero  0x2
DAT_080bc2e8:
    .word  0x0201afe0                     @ 080bc2e8 e0af0102
LAB_080bc2ec:
    ldr r1, DAT_080bc2f4                     @ 080bc2ec 0149
    ldr r0,[r1,#0x8]                         @ 080bc2ee 8868
    adds r0,#0x1    @ 080bc2f0 0130
    b LAB_080bc370                           @ 080bc2f2 3de0
DAT_080bc2f4:
    .word  0x0201afe0                     @ 080bc2f4 e0af0102
switchD_080bc18a__caseD_4:
    adds r0,r4,#0x0    @ 080bc2f8 201c
    bl check_player_lp_exceeds_toon_world_cost @ 080bc2fa f0f779fc
    cmp r0,#0x0                              @ 080bc2fe 0028
    beq LAB_080bc334                         @ 080bc300 18d0
    ldr r2, PTR_gP1LifePoints_080bc33c       @ 080bc302 0e4a
    movs r3,#0x1    @ 080bc304 0123
    adds r0,r4,#0x0    @ 080bc306 201c
    ands r0,r3    @ 080bc308 1840
    ldr r1, DAT_080bc340                     @ 080bc30a 0d49
    muls r0,r1    @ 080bc30c 4843
    movs r1,#0x8e    @ 080bc30e 8e21
    lsls r1,r1,#0x1    @ 080bc310 4900
    adds r2,r2,r1    @ 080bc312 5218
    adds r0,r0,r2    @ 080bc314 8018
    ldr r0,[r0,#0x0]                         @ 080bc316 0068
    lsrs r0,r0,#0x11    @ 080bc318 400c
    ands r0,r3    @ 080bc31a 1840
    cmp r0,#0x0                              @ 080bc31c 0028
    bne LAB_080bc334                         @ 080bc31e 09d1
    adds r0,r4,#0x0    @ 080bc320 201c
    bl check_field_spell_card_placeable_strict @ 080bc322 7ff767fb
    cmp r0,#0x0                              @ 080bc326 0028
    bne LAB_080bc348                         @ 080bc328 0ed1
    adds r0,r4,#0x0    @ 080bc32a 201c
    bl check_field_spell_group_placeable     @ 080bc32c 7ff728fb
    cmp r0,#0x0                              @ 080bc330 0028
    bne LAB_080bc348                         @ 080bc332 09d1
LAB_080bc334:
    ldr r1, DAT_080bc344                     @ 080bc334 0349
    ldr r0,[r1,#0x8]                         @ 080bc336 8868
    adds r0,#0x1    @ 080bc338 0130
    b LAB_080bc370                           @ 080bc33a 19e0
PTR_gP1LifePoints_080bc33c:
    .word  gP1LifePoints                  @ 080bc33c e0c40102
DAT_080bc340:
    .word  0x00000868                     @ 080bc340 68080000
DAT_080bc344:
    .word  0x0201afe0                     @ 080bc344 e0af0102
LAB_080bc348:
    adds r0,r4,#0x0    @ 080bc348 201c
    .hword 0x4669    @ 080bc34a 6946
    bl select_equip_placement_slot_with_score @ 080bc34c f5f7f6f8
    adds r1,r0,#0x0    @ 080bc350 011c
    cmp r1,#0x0                              @ 080bc352 0029
    blt switchD_080bc18a__default            @ 080bc354 12db
    ldr r0,[sp,#0x0]                         @ 080bc356 0098
    cmp r0,#0x0                              @ 080bc358 0028
    bne switchD_080bc18a__default            @ 080bc35a 0fd1
    adds r0,r4,#0x0    @ 080bc35c 201c
    movs r2,#0x0    @ 080bc35e 0022
    bl execute_field_spell_equip_placement   @ 080bc360 fff742fd
    cmp r0,#0x0                              @ 080bc364 0028
    beq LAB_080bc372                         @ 080bc366 04d0
    cmp r0,#0x0                              @ 080bc368 0028
    ble switchD_080bc18a__default            @ 080bc36a 07dd
    ldr r1, DAT_080bc378                     @ 080bc36c 0249
    movs r0,#0x1    @ 080bc36e 0120
LAB_080bc370:
    str r0,[r1,#0x8]                         @ 080bc370 8860
LAB_080bc372:
    movs r0,#0x0    @ 080bc372 0020
    b LAB_080bc37e                           @ 080bc374 03e0
    .zero  0x2
DAT_080bc378:
    .word  0x0201afe0                     @ 080bc378 e0af0102
switchD_080bc18a__default:
    movs r0,#0x1    @ 080bc37c 0120
LAB_080bc37e:
    add sp,#0x4                              @ 080bc37e 01b0
    pop {r4,r5,r6}                           @ 080bc380 70bc
    pop {r1}                                 @ 080bc382 02bc
    bx r1                                    @ 080bc384 0847
    .zero  0x2

@ 被 toon world AI 决策入口调用 (indeg 待确认). 无 APCS 参数: player_id 从 gP1LifePoints[+0x1ce8] 读取 (以 ldr r5,PTR_gP1LifePoints; ldr r1,DAT_0x1ce8; adds r0,r5,r1; ldr r4,[r0] 方式读取). 函数体: (1) 读 0x0201afe0[+8] (duel battle state 字段); 非 0 则返回 1 (战斗状态下不允许放置); (2) 调用 check_player_lp_exceeds_toon_world_cost(player); 不满足则跳到 fail; (3) 读 gP1LifePoints[player*0x868+0x11c] bit17 (toon world 相关标志); 若置位则 fail; (4) 调用 check_field_spell_card_placeable_strict 或 check_field_spell_group_placeable(player); 至少一个通过才继续; (5) 调用 select_equip_placement_slot_with_score(player, sp) 选最优格; 返回 -1 则 fail; (6) 调用 execute_field_spell_equip_placement; 失败则 fail; (7) fail 路径: [0x0201afe0+8] += 1 (计数器递增); 所有路径返回 0. 成功路径 (execute_field_spell_equip_placement 成功) 也返回 0. 非成功分支 (战斗状态) 返回 1. Constants: gP1LifePoints=0x0201c4e0, player_offset_in=0x1ce8, battle_state_ptr=0x0201afe0, player_stride=0x868, toon_flag_bit17_word_offset=0x11c.
try_execute_toon_world_equip_placement:
    push {r4,r5,lr}                          @ 080bc388 30b5
    sub sp,#0x4                              @ 080bc38a 81b0
    ldr r5, PTR_gP1LifePoints_080bc3fc       @ 080bc38c 1b4d
    ldr r1, DAT_080bc400                     @ 080bc38e 1c49
    adds r0,r5,r1    @ 080bc390 6818
    ldr r4,[r0,#0x0]                         @ 080bc392 0468
    ldr r0, DAT_080bc404                     @ 080bc394 1b48
    ldr r0,[r0,#0x8]                         @ 080bc396 8068
    cmp r0,#0x0                              @ 080bc398 0028
    bne LAB_080bc40c                         @ 080bc39a 37d1
    adds r0,r4,#0x0    @ 080bc39c 201c
    bl check_player_lp_exceeds_toon_world_cost @ 080bc39e f0f727fc
    cmp r0,#0x0                              @ 080bc3a2 0028
    beq LAB_080bc3f0                         @ 080bc3a4 24d0
    movs r2,#0x1    @ 080bc3a6 0122
    adds r0,r4,#0x0    @ 080bc3a8 201c
    ands r0,r2    @ 080bc3aa 1040
    ldr r1, DAT_080bc408                     @ 080bc3ac 1649
    muls r0,r1    @ 080bc3ae 4843
    movs r3,#0x8e    @ 080bc3b0 8e23
    lsls r3,r3,#0x1    @ 080bc3b2 5b00
    adds r1,r5,r3    @ 080bc3b4 e918
    adds r0,r0,r1    @ 080bc3b6 4018
    ldr r0,[r0,#0x0]                         @ 080bc3b8 0068
    lsrs r0,r0,#0x11    @ 080bc3ba 400c
    ands r0,r2    @ 080bc3bc 1040
    cmp r0,#0x0                              @ 080bc3be 0028
    bne LAB_080bc3f0                         @ 080bc3c0 16d1
    adds r0,r4,#0x0    @ 080bc3c2 201c
    bl check_field_spell_card_placeable_strict @ 080bc3c4 7ff716fb
    cmp r0,#0x0                              @ 080bc3c8 0028
    bne LAB_080bc3d6                         @ 080bc3ca 04d1
    adds r0,r4,#0x0    @ 080bc3cc 201c
    bl check_field_spell_group_placeable     @ 080bc3ce 7ff7d7fa
    cmp r0,#0x0                              @ 080bc3d2 0028
    beq LAB_080bc3f0                         @ 080bc3d4 0cd0
LAB_080bc3d6:
    adds r0,r4,#0x0    @ 080bc3d6 201c
    .hword 0x4669    @ 080bc3d8 6946
    bl select_equip_placement_slot_with_score @ 080bc3da f5f7aff8
    adds r1,r0,#0x0    @ 080bc3de 011c
    cmp r1,#0x0                              @ 080bc3e0 0029
    blt LAB_080bc3f0                         @ 080bc3e2 05db
    ldr r2,[sp,#0x0]                         @ 080bc3e4 009a
    adds r0,r4,#0x0    @ 080bc3e6 201c
    bl execute_field_spell_equip_placement   @ 080bc3e8 fff7fefc
    cmp r0,#0x0                              @ 080bc3ec 0028
    beq LAB_080bc3f8                         @ 080bc3ee 03d0
LAB_080bc3f0:
    ldr r1, DAT_080bc404                     @ 080bc3f0 0449
    ldr r0,[r1,#0x8]                         @ 080bc3f2 8868
    adds r0,#0x1    @ 080bc3f4 0130
    str r0,[r1,#0x8]                         @ 080bc3f6 8860
LAB_080bc3f8:
    movs r0,#0x0    @ 080bc3f8 0020
    b LAB_080bc40e                           @ 080bc3fa 08e0
PTR_gP1LifePoints_080bc3fc:
    .word  gP1LifePoints                  @ 080bc3fc e0c40102
DAT_080bc400:
    .word  0x00001ce8                     @ 080bc400 e81c0000
DAT_080bc404:
    .word  0x0201afe0                     @ 080bc404 e0af0102
DAT_080bc408:
    .word  0x00000868                     @ 080bc408 68080000
LAB_080bc40c:
    movs r0,#0x1    @ 080bc40c 0120
LAB_080bc40e:
    add sp,#0x4                              @ 080bc40e 01b0
    pop {r4,r5}                              @ 080bc410 30bc
    pop {r1}                                 @ 080bc412 02bc
    bx r1                                    @ 080bc414 0847
    .zero  0x2

@ Evaluates equip slot target eligibility and executes activation if conditions met. r0=player_side [0..1] -> r5; r1=slot_idx [0..4] -> r6; r2=check_mode (0=slot_binding_check, non-0=full_validity_check). If r2==0: reads [0x0201afe0+r6*4+0x198] to confirm slot binding; if non-zero sets r4=-1. If r2!=0: calls check_equip_card_valid_for_target_slot(r5, r6, 0); if not -1 sets r4=0 (passed). Then: calls check_slot_field_action_eligibility(r5, r6); if 0 returns 0. If passed: extended checks (check_field_spell_last_warrior_placeable, check_card_stat_field8_is_6, check_field_spell_neo_daedalus_group_placeable, check_toon_world_equip_present; count_field_copies_of_card for 0x15fb/0x197b); all pass: calls apply_slot_equip_activation_with_sprite(r5, r6, 0, 0). Returns 1=activation executed, 0=conditions not met. Callers: FUN_080bc54c (player 0), FUN_080bc5d4 (player 1). Params: r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]; r2=u32 check_mode (0=binding, non-0=full). Returns r0=u32 1=activated, 0=not met. Side effects: via apply_slot_equip_activation_with_sprite: OAM sprite + equip activation state; via init_equip_sub_entry_fields_from_slot: equip sub-entry fields. Constants: CARD_ID=0x15fb (Final Attack Orders); CARD_ID=0x197b (Level Limit - Area A).
eval_equip_slot_target_eligibility_full:
    push {r4,r5,r6,lr}                       @ 080bc418 70b5
    sub sp,#0x4                              @ 080bc41a 81b0
    adds r5,r0,#0x0    @ 080bc41c 051c
    adds r6,r1,#0x0    @ 080bc41e 0e1c
    movs r4,#0x1    @ 080bc420 0124
    rsbs r4,r4,#0    @ 080bc422 6442
    cmp r2,#0x0                              @ 080bc424 002a
    bne LAB_080bc43c                         @ 080bc426 09d1
    ldr r0, DAT_080bc4b0                     @ 080bc428 2148
    lsls r1,r6,#0x2    @ 080bc42a b100
    movs r2,#0xcc    @ 080bc42c cc22
    lsls r2,r2,#0x1    @ 080bc42e 5200
    adds r0,r0,r2    @ 080bc430 8018
    adds r1,r1,r0    @ 080bc432 0918
    ldr r0,[r1,#0x0]                         @ 080bc434 0868
    cmp r0,#0x0                              @ 080bc436 0028
    beq LAB_080bc43c                         @ 080bc438 00d0
    movs r4,#0x0    @ 080bc43a 0024
LAB_080bc43c:
    movs r0,#0x1    @ 080bc43c 0120
    rsbs r0,r0,#0    @ 080bc43e 4042
    cmp r4,r0                                @ 080bc440 8442
    bne LAB_080bc44e                         @ 080bc442 04d1
    adds r0,r5,#0x0    @ 080bc444 281c
    adds r1,r6,#0x0    @ 080bc446 311c
    bl check_equip_card_valid_for_target_slot @ 080bc448 eff7e8fe
    adds r4,r0,#0x0    @ 080bc44c 041c
LAB_080bc44e:
    adds r0,r5,#0x0    @ 080bc44e 281c
    adds r1,r6,#0x0    @ 080bc450 311c
    bl check_slot_field_action_eligibility   @ 080bc452 77f781ff
    cmp r0,#0x0                              @ 080bc456 0028
    beq LAB_080bc540                         @ 080bc458 72d0
    cmp r4,#0x0                              @ 080bc45a 002c
    bne LAB_080bc4e0                         @ 080bc45c 40d1
    movs r2,#0x1    @ 080bc45e 0122
    ands r2,r5    @ 080bc460 2a40
    lsls r0,r6,#0x2    @ 080bc462 b000
    adds r0,r0,r6    @ 080bc464 8019
    lsls r0,r0,#0x2    @ 080bc466 8000
    ldr r1, DAT_080bc4b4                     @ 080bc468 1249
    muls r1,r2    @ 080bc46a 5143
    adds r0,r0,r1    @ 080bc46c 4018
    ldr r1, DAT_080bc4b8                     @ 080bc46e 1249
    adds r4,r0,r1    @ 080bc470 4418
    ldrh r0,[r4,#0x8]                        @ 080bc472 2089
    cmp r0,#0x0                              @ 080bc474 0028
    bne LAB_080bc4bc                         @ 080bc476 21d1
    adds r0,r5,#0x0    @ 080bc478 281c
    bl check_field_spell_last_warrior_placeable @ 080bc47a 7ff70dfb
    cmp r0,#0x0                              @ 080bc47e 0028
    beq LAB_080bc540                         @ 080bc480 5ed0
    ldr r0,[r4,#0x0]                         @ 080bc482 2068
    lsls r0,r0,#0x13    @ 080bc484 c004
    lsrs r0,r0,#0x13    @ 080bc486 c00c
    bl check_card_stat_field8_is_6           @ 080bc488 8ef7bcfc
    cmp r0,#0x0                              @ 080bc48c 0028
    beq LAB_080bc4a4                         @ 080bc48e 09d0
    adds r0,r5,#0x0    @ 080bc490 281c
    bl check_field_spell_neo_daedalus_group_placeable @ 080bc492 7ff773fb
    cmp r0,#0x0                              @ 080bc496 0028
    beq LAB_080bc540                         @ 080bc498 52d0
    adds r0,r5,#0x0    @ 080bc49a 281c
    bl check_toon_world_equip_present        @ 080bc49c 76f7f4fd
    cmp r0,#0x0                              @ 080bc4a0 0028
    beq LAB_080bc540                         @ 080bc4a2 4dd0
LAB_080bc4a4:
    adds r0,r5,#0x0    @ 080bc4a4 281c
    adds r1,r6,#0x0    @ 080bc4a6 311c
    bl init_equip_sub_entry_fields_from_slot @ 080bc4a8 eff700fc
    movs r0,#0x1    @ 080bc4ac 0120
    b LAB_080bc542                           @ 080bc4ae 48e0
DAT_080bc4b0:
    .word  0x0201afe0                     @ 080bc4b0 e0af0102
DAT_080bc4b4:
    .word  0x00000868                     @ 080bc4b4 68080000
DAT_080bc4b8:
    .word  0x0201c510                     @ 080bc4b8 10c50102
LAB_080bc4bc:
    ldrh r0,[r4,#0x6]                        @ 080bc4bc e088
    cmp r0,#0x0                              @ 080bc4be 0028
    beq LAB_080bc540                         @ 080bc4c0 3ed0
    ldr r0, DAT_080bc4dc                     @ 080bc4c2 0648
    bl count_field_copies_of_card            @ 080bc4c4 76f76af9
    cmp r0,#0x0                              @ 080bc4c8 0028
    beq LAB_080bc51c                         @ 080bc4ca 27d0
    adds r0,r5,#0x0    @ 080bc4cc 281c
    adds r1,r6,#0x0    @ 080bc4ce 311c
    bl eval_equip_chain_score_for_slot       @ 080bc4d0 7ef76afa
    cmp r0,#0x3                              @ 080bc4d4 0328
    bgt LAB_080bc540                         @ 080bc4d6 33dc
    b LAB_080bc51c                           @ 080bc4d8 20e0
    .zero  0x2
DAT_080bc4dc:
    .word  0x000017a6                     @ 080bc4dc a6170000
LAB_080bc4e0:
    cmp r4,#0x1                              @ 080bc4e0 012c
    bne LAB_080bc540                         @ 080bc4e2 2dd1
    ands r4,r5    @ 080bc4e4 2c40
    lsls r0,r6,#0x2    @ 080bc4e6 b000
    adds r0,r0,r6    @ 080bc4e8 8019
    lsls r0,r0,#0x2    @ 080bc4ea 8000
    ldr r1, DAT_080bc530                     @ 080bc4ec 1049
    muls r1,r4    @ 080bc4ee 6143
    adds r0,r0,r1    @ 080bc4f0 4018
    ldr r1, DAT_080bc534                     @ 080bc4f2 1049
    adds r0,r0,r1    @ 080bc4f4 4018
    ldrh r0,[r0,#0x6]                        @ 080bc4f6 c088
    cmp r0,#0x0                              @ 080bc4f8 0028
    bne LAB_080bc540                         @ 080bc4fa 21d1
    ldr r0, DAT_080bc538                     @ 080bc4fc 0e48
    bl count_field_copies_of_card            @ 080bc4fe 76f74df9
    cmp r0,#0x0                              @ 080bc502 0028
    bne LAB_080bc540                         @ 080bc504 1cd1
    ldr r0, DAT_080bc53c                     @ 080bc506 0d48
    bl count_field_copies_of_card            @ 080bc508 76f748f9
    cmp r0,#0x0                              @ 080bc50c 0028
    beq LAB_080bc51c                         @ 080bc50e 05d0
    adds r0,r5,#0x0    @ 080bc510 281c
    adds r1,r6,#0x0    @ 080bc512 311c
    bl eval_equip_chain_score_for_slot       @ 080bc514 7ef748fa
    cmp r0,#0x3                              @ 080bc518 0328
    ble LAB_080bc540                         @ 080bc51a 11dd
LAB_080bc51c:
    movs r0,#0x1    @ 080bc51c 0120
    str r0,[sp,#0x0]                         @ 080bc51e 0090
    adds r0,r5,#0x0    @ 080bc520 281c
    adds r1,r6,#0x0    @ 080bc522 311c
    movs r2,#0x0    @ 080bc524 0022
    movs r3,#0x0    @ 080bc526 0023
    bl apply_slot_equip_activation_with_sprite @ 080bc528 87f75afa
    movs r0,#0x1    @ 080bc52c 0120
    b LAB_080bc542                           @ 080bc52e 08e0
DAT_080bc530:
    .word  0x00000868                     @ 080bc530 68080000
DAT_080bc534:
    .word  0x0201c510                     @ 080bc534 10c50102
DAT_080bc538:
    .word  0x000015fb                     @ 080bc538 fb150000
DAT_080bc53c:
    .word  0x0000197b                     @ 080bc53c 7b190000
LAB_080bc540:
    movs r0,#0x0    @ 080bc540 0020
LAB_080bc542:
    add sp,#0x4                              @ 080bc542 01b0
    pop {r4,r5,r6}                           @ 080bc544 70bc
    pop {r1}                                 @ 080bc546 02bc
    bx r1                                    @ 080bc548 0847
    .zero  0x2

@ Equip activation state machine driver for player 0 (P1 side). No APCS input params; reads gP1LifePoints+0x1ce8 -> r5 (equip player_side); loads 0x0201afe0 (equip control struct) -> r4; reads [r4+0x8] (state code). State dispatch: 0 (bcc)=reads [gP1LifePoints+0x1cf4] (zone_count), if <=2 calls find_equip_slot_by_player_and_zone_count(r5, 0); if returns 0 increments [r4+0x8]; then calls dispatch_equip_activation_full_sequence(r5), if success increments [r4+0x8]. 1 (beq LAB_080bc590)=calls dispatch_equip_activation_full_sequence(r5), fail->0. 2 (beq LAB_080bc5ac)=calls compute_equip_zone_score_with_cache(r5), loops slot [0..4] calling eval_equip_slot_target_eligibility_full(r5, slot, mode=0). 3+=returns 1. Called exclusively by FUN_080bc71c (duel_field, indeg=1). Params: none. Returns r0=u32 0=state machine running/fail, 1=terminated/success. Side effects: [0x0201afe0+0x8]:=counter+1; activation and sprite via callees.
run_equip_activation_state_machine_p1:
    push {r4,r5,lr}                          @ 080bc54c 30b5
    ldr r1, PTR_gP1LifePoints_080bc568       @ 080bc54e 0649
    ldr r2, DAT_080bc56c                     @ 080bc550 064a
    adds r0,r1,r2    @ 080bc552 8818
    ldr r5,[r0,#0x0]                         @ 080bc554 0568
    ldr r4, DAT_080bc570                     @ 080bc556 064c
    ldr r0,[r4,#0x8]                         @ 080bc558 a068
    cmp r0,#0x1                              @ 080bc55a 0128
    beq LAB_080bc590                         @ 080bc55c 18d0
    cmp r0,#0x1                              @ 080bc55e 0128
    bcc LAB_080bc574                         @ 080bc560 08d3
    cmp r0,#0x2                              @ 080bc562 0228
    beq LAB_080bc5ac                         @ 080bc564 22d0
    b LAB_080bc5c8                           @ 080bc566 2fe0
PTR_gP1LifePoints_080bc568:
    .word  gP1LifePoints                  @ 080bc568 e0c40102
DAT_080bc56c:
    .word  0x00001ce8                     @ 080bc56c e81c0000
DAT_080bc570:
    .word  0x0201afe0                     @ 080bc570 e0af0102
LAB_080bc574:
    ldr r2, DAT_080bc5a0                     @ 080bc574 0a4a
    adds r0,r1,r2    @ 080bc576 8818
    ldr r0,[r0,#0x0]                         @ 080bc578 0068
    cmp r0,#0x2                              @ 080bc57a 0228
    bhi LAB_080bc5c8                         @ 080bc57c 24d8
    adds r0,r5,#0x0    @ 080bc57e 281c
    movs r1,#0x0    @ 080bc580 0021
    bl find_equip_slot_by_player_and_zone_count @ 080bc582 fef7b9fd
    cmp r0,#0x0                              @ 080bc586 0028
    bne LAB_080bc59a                         @ 080bc588 07d1
    ldr r0,[r4,#0x8]                         @ 080bc58a a068
    adds r0,#0x1    @ 080bc58c 0130
    str r0,[r4,#0x8]                         @ 080bc58e a060
LAB_080bc590:
    adds r0,r5,#0x0    @ 080bc590 281c
    bl dispatch_equip_activation_full_sequence @ 080bc592 fef73fff
    cmp r0,#0x0                              @ 080bc596 0028
    beq LAB_080bc5a4                         @ 080bc598 04d0
LAB_080bc59a:
    movs r0,#0x0    @ 080bc59a 0020
    b LAB_080bc5ca                           @ 080bc59c 15e0
    .zero  0x2
DAT_080bc5a0:
    .word  0x00001cf4                     @ 080bc5a0 f41c0000
LAB_080bc5a4:
    ldr r1, DAT_080bc5d0                     @ 080bc5a4 0a49
    ldr r0,[r1,#0x8]                         @ 080bc5a6 8868
    adds r0,#0x1    @ 080bc5a8 0130
    str r0,[r1,#0x8]                         @ 080bc5aa 8860
LAB_080bc5ac:
    adds r0,r5,#0x0    @ 080bc5ac 281c
    bl compute_equip_zone_score_with_cache   @ 080bc5ae f4f7f3fc
    movs r4,#0x0    @ 080bc5b2 0024
LAB_080bc5b4:
    adds r0,r5,#0x0    @ 080bc5b4 281c
    adds r1,r4,#0x0    @ 080bc5b6 211c
    movs r2,#0x0    @ 080bc5b8 0022
    bl eval_equip_slot_target_eligibility_full @ 080bc5ba fff72dff
    cmp r0,#0x0                              @ 080bc5be 0028
    bne LAB_080bc59a                         @ 080bc5c0 ebd1
    adds r4,#0x1    @ 080bc5c2 0134
    cmp r4,#0x4                              @ 080bc5c4 042c
    ble LAB_080bc5b4                         @ 080bc5c6 f5dd
LAB_080bc5c8:
    movs r0,#0x1    @ 080bc5c8 0120
LAB_080bc5ca:
    pop {r4,r5}                              @ 080bc5ca 30bc
    pop {r1}                                 @ 080bc5cc 02bc
    bx r1                                    @ 080bc5ce 0847
DAT_080bc5d0:
    .word  0x0201afe0                     @ 080bc5d0 e0af0102

@ Equip activation state machine driver for player 1 (P2 side). Structurally symmetric to run_equip_activation_state_machine_p1 (0x080bc54c); differences: state 0 calls find_equip_slot_by_player_and_zone_count(r5, zone_count=1) (P1 uses zone_count=0); state 2 calls eval_equip_slot_target_eligibility_full(r5, slot, mode=1) (P1 uses mode=0). No APCS input params; reads gP1LifePoints+0x1ce8 -> r5 (player_side); loads 0x0201afe0 -> r4; reads [r4+0x8] dispatch. Called exclusively by FUN_080bc71c (duel_field, indeg=1). Params: none. Returns r0=u32 0=running/fail, 1=terminated/success. Side effects: [0x0201afe0+0x8]:=counter+1; activation and sprite via callees.
run_equip_activation_state_machine_p2:
    push {r4,r5,lr}                          @ 080bc5d4 30b5
    ldr r0, PTR_gP1LifePoints_080bc5f0       @ 080bc5d6 0648
    ldr r1, DAT_080bc5f4                     @ 080bc5d8 0649
    adds r0,r0,r1    @ 080bc5da 4018
    ldr r5,[r0,#0x0]                         @ 080bc5dc 0568
    ldr r4, DAT_080bc5f8                     @ 080bc5de 064c
    ldr r0,[r4,#0x8]                         @ 080bc5e0 a068
    cmp r0,#0x1                              @ 080bc5e2 0128
    beq LAB_080bc60e                         @ 080bc5e4 13d0
    cmp r0,#0x1                              @ 080bc5e6 0128
    bcc LAB_080bc5fc                         @ 080bc5e8 08d3
    cmp r0,#0x2                              @ 080bc5ea 0228
    beq LAB_080bc624                         @ 080bc5ec 1ad0
    b LAB_080bc63a                           @ 080bc5ee 24e0
PTR_gP1LifePoints_080bc5f0:
    .word  gP1LifePoints                  @ 080bc5f0 e0c40102
DAT_080bc5f4:
    .word  0x00001ce8                     @ 080bc5f4 e81c0000
DAT_080bc5f8:
    .word  0x0201afe0                     @ 080bc5f8 e0af0102
LAB_080bc5fc:
    adds r0,r5,#0x0    @ 080bc5fc 281c
    movs r1,#0x1    @ 080bc5fe 0121
    bl find_equip_slot_by_player_and_zone_count @ 080bc600 fef77afd
    cmp r0,#0x0                              @ 080bc604 0028
    bne LAB_080bc618                         @ 080bc606 07d1
    ldr r0,[r4,#0x8]                         @ 080bc608 a068
    adds r0,#0x1    @ 080bc60a 0130
    str r0,[r4,#0x8]                         @ 080bc60c a060
LAB_080bc60e:
    adds r0,r5,#0x0    @ 080bc60e 281c
    bl dispatch_equip_activation_full_sequence @ 080bc610 fef700ff
    cmp r0,#0x0                              @ 080bc614 0028
    beq LAB_080bc61c                         @ 080bc616 01d0
LAB_080bc618:
    movs r0,#0x0    @ 080bc618 0020
    b LAB_080bc63c                           @ 080bc61a 0fe0
LAB_080bc61c:
    ldr r1, DAT_080bc644                     @ 080bc61c 0949
    ldr r0,[r1,#0x8]                         @ 080bc61e 8868
    adds r0,#0x1    @ 080bc620 0130
    str r0,[r1,#0x8]                         @ 080bc622 8860
LAB_080bc624:
    movs r4,#0x0    @ 080bc624 0024
LAB_080bc626:
    adds r0,r5,#0x0    @ 080bc626 281c
    adds r1,r4,#0x0    @ 080bc628 211c
    movs r2,#0x1    @ 080bc62a 0122
    bl eval_equip_slot_target_eligibility_full @ 080bc62c fff7f4fe
    cmp r0,#0x0                              @ 080bc630 0028
    bne LAB_080bc618                         @ 080bc632 f1d1
    adds r4,#0x1    @ 080bc634 0134
    cmp r4,#0x4                              @ 080bc636 042c
    ble LAB_080bc626                         @ 080bc638 f5dd
LAB_080bc63a:
    movs r0,#0x1    @ 080bc63a 0120
LAB_080bc63c:
    pop {r4,r5}                              @ 080bc63c 30bc
    pop {r1}                                 @ 080bc63e 02bc
    bx r1                                    @ 080bc640 0847
    .zero  0x2
DAT_080bc644:
    .word  0x0201afe0                     @ 080bc644 e0af0102

@ Dispatches equip activation phase handling by state code. Reads gP1LifePoints+0x1ce8 (equip activation player_side) -> r4; loads 0x0201afe0 (equip activation control struct) -> r5; reads [r5+0x8] (state code); dispatches: 0=check_equip_effect_zone_preconditions + check_equip_slot_activation_blocked_by_chain + eval_equip_monster_zone_score_full + try_activate_equip_via_two_tables (clears [gP1LifePoints+0x1d28/0x1d2c], increments [r5+0x8]); 1=submit_lp_bar_sprite_row_by_type(3,0) + [r5+0x8]++; 2=advance_equip_display_phase_via_table(r4) -- if returns non-zero [r5+0x8]++; 3=FUN_0809be70(r4) -- if returns 0 [r5+0x8]++; 4+=enqueue_sprite_attr_record(0x10/0x8010,...) + returns 1. Called exclusively by FUN_080bc71c (duel_field, indeg=1). Params: none. Returns r0=u32 0 (state machine running) / 1 (terminated/complete). Side effects: [gP1LifePoints+0x1d28]:=0; [gP1LifePoints+0x1d2c]:=0 (state 0 path); [0x0201afe0+0x8]:=counter+1; OAM sprite attr buffer via enqueue_sprite_attr_record / submit_lp_bar_sprite_row_by_type.
dispatch_equip_activation_phase_by_state:
    push {r4,r5,r6,lr}                       @ 080bc648 70b5
    ldr r6, PTR_gP1LifePoints_080bc668       @ 080bc64a 074e
    ldr r1, DAT_080bc66c                     @ 080bc64c 0749
    adds r0,r6,r1    @ 080bc64e 7018
    ldr r4,[r0,#0x0]                         @ 080bc650 0468
    ldr r5, DAT_080bc670                     @ 080bc652 074d
    ldr r0,[r5,#0x8]                         @ 080bc654 a868
    cmp r0,#0x1                              @ 080bc656 0128
    beq LAB_080bc6cc                         @ 080bc658 38d0
    cmp r0,#0x1                              @ 080bc65a 0128
    bcc LAB_080bc674                         @ 080bc65c 0ad3
    cmp r0,#0x2                              @ 080bc65e 0228
    beq LAB_080bc6d6                         @ 080bc660 39d0
    cmp r0,#0x3                              @ 080bc662 0328
    beq LAB_080bc6f8                         @ 080bc664 48d0
    b LAB_080bc714                           @ 080bc666 55e0
PTR_gP1LifePoints_080bc668:
    .word  gP1LifePoints                  @ 080bc668 e0c40102
DAT_080bc66c:
    .word  0x00001ce8                     @ 080bc66c e81c0000
DAT_080bc670:
    .word  0x0201afe0                     @ 080bc670 e0af0102
LAB_080bc674:
    adds r0,r4,#0x0    @ 080bc674 201c
    bl check_equip_effect_zone_preconditions @ 080bc676 daf78bfd
    cmp r0,#0x0                              @ 080bc67a 0028
    beq LAB_080bc70a                         @ 080bc67c 45d0
    adds r0,r4,#0x0    @ 080bc67e 201c
    bl check_equip_slot_activation_blocked_by_chain @ 080bc680 daf7fafd
    cmp r0,#0x0                              @ 080bc684 0028
    beq LAB_080bc694                         @ 080bc686 05d0
    adds r0,r4,#0x0    @ 080bc688 201c
    movs r1,#0x0    @ 080bc68a 0021
    bl eval_equip_monster_zone_score_full    @ 080bc68c f4f7acfc
    cmp r0,#0x0                              @ 080bc690 0028
    beq LAB_080bc70a                         @ 080bc692 3ad0
LAB_080bc694:
    adds r0,r4,#0x0    @ 080bc694 201c
    movs r1,#0x1    @ 080bc696 0121
    bl try_activate_equip_via_two_tables     @ 080bc698 fef778fe
    adds r2,r0,#0x0    @ 080bc69c 021c
    cmp r2,#0x0                              @ 080bc69e 002a
    bne LAB_080bc714                         @ 080bc6a0 38d1
    ldr r0, PTR_gP1LifePoints_080bc6bc       @ 080bc6a2 0648
    ldr r3, DAT_080bc6c0                     @ 080bc6a4 064b
    adds r1,r0,r3    @ 080bc6a6 c118
    str r2,[r1,#0x0]                         @ 080bc6a8 0a60
    ldr r1, DAT_080bc6c4                     @ 080bc6aa 0649
    adds r0,r0,r1    @ 080bc6ac 4018
    str r2,[r0,#0x0]                         @ 080bc6ae 0260
    ldr r1, DAT_080bc6c8                     @ 080bc6b0 0549
    ldr r0,[r1,#0x8]                         @ 080bc6b2 8868
    adds r0,#0x1    @ 080bc6b4 0130
    str r0,[r1,#0x8]                         @ 080bc6b6 8860
    b LAB_080bc714                           @ 080bc6b8 2ce0
    .zero  0x2
PTR_gP1LifePoints_080bc6bc:
    .word  gP1LifePoints                  @ 080bc6bc e0c40102
DAT_080bc6c0:
    .word  0x00001d28                     @ 080bc6c0 281d0000
DAT_080bc6c4:
    .word  0x00001d2c                     @ 080bc6c4 2c1d0000
DAT_080bc6c8:
    .word  0x0201afe0                     @ 080bc6c8 e0af0102
LAB_080bc6cc:
    movs r0,#0x3    @ 080bc6cc 0320
    movs r1,#0x0    @ 080bc6ce 0021
    bl submit_lp_bar_sprite_row_by_type      @ 080bc6d0 c8f726fe
    b LAB_080bc6ea                           @ 080bc6d4 09e0
LAB_080bc6d6:
    adds r0,r4,#0x0    @ 080bc6d6 201c
    bl advance_equip_display_phase_via_table @ 080bc6d8 dff7cafb
    cmp r0,#0x0                              @ 080bc6dc 0028
    beq LAB_080bc714                         @ 080bc6de 19d0
    ldr r3, DAT_080bc6f4                     @ 080bc6e0 044b
    adds r0,r6,r3    @ 080bc6e2 f018
    ldr r0,[r0,#0x0]                         @ 080bc6e4 0068
    cmp r0,#0x0                              @ 080bc6e6 0028
    bne LAB_080bc70a                         @ 080bc6e8 0fd1
LAB_080bc6ea:
    ldr r0,[r5,#0x8]                         @ 080bc6ea a868
    adds r0,#0x1    @ 080bc6ec 0130
    str r0,[r5,#0x8]                         @ 080bc6ee a860
    b LAB_080bc714                           @ 080bc6f0 10e0
    .zero  0x2
DAT_080bc6f4:
    .word  0x00001d30                     @ 080bc6f4 301d0000
LAB_080bc6f8:
    movs r0,#0x10    @ 080bc6f8 1020
    cmp r4,#0x0                              @ 080bc6fa 002c
    beq LAB_080bc700                         @ 080bc6fc 00d0
    ldr r0, DAT_080bc710                     @ 080bc6fe 0448
LAB_080bc700:
    movs r1,#0x0    @ 080bc700 0021
    movs r2,#0x0    @ 080bc702 0022
    movs r3,#0x0    @ 080bc704 0023
    bl enqueue_sprite_attr_record            @ 080bc706 7ff711fb
LAB_080bc70a:
    movs r0,#0x1    @ 080bc70a 0120
    b LAB_080bc716                           @ 080bc70c 03e0
    .zero  0x2
DAT_080bc710:
    .word  0x00008010                     @ 080bc710 10800000
LAB_080bc714:
    movs r0,#0x0    @ 080bc714 0020
LAB_080bc716:
    pop {r4,r5,r6}                           @ 080bc716 70bc
    pop {r1}                                 @ 080bc718 02bc
    bx r1                                    @ 080bc71a 0847

@ Called by tick_duel_field_spell_activation_state (0x0809e168, duel_field large state dispatcher, indeg=1). Reads global AI control block [0x0201afe0]: [+0] stores player index (from gP1LifePoints+0x1ce8), [+4] is current state_id. If state_id==0 and gP1LifePoints+0x1cf4==4, forces state_id=7 (special init branch). Fetches function pointer from jump table 0x09e5ab5c at state_id*4, calls via bx r0 (dispatch_via_ptr through FUN_0810e5c8). If sub-state handler returns 1 (advance): clears [0x0201afe0+8/c], increments state_id, checks gP1LifePoints+0x1d30==0 (cycle-complete condition) -> returns 0; otherwise returns 1 (outer loop continues waiting). Returns: r0=u32 bool (0=this AI cycle still needs ticking, 1=this cycle's state complete). Side effects: [0x0201afe0+0x0]:=player, [0x0201afe0+0x4]:=state_id (or 7), [0x0201afe0+0x8]:=0, [0x0201afe0+0xc]:=0. Constants: ai_ctrl_block=0x0201afe0 ([+0]=player,[+4]=state_id,[+8]=phase,[+c]=misc), jump_table=0x09e5ab5c (state_id dispatch table), special_state_id=7 (forced when gP1LifePoints+0x1cf4==4), init_condition_val=4, cycle_done_offset=0x1d30.
tick_duel_field_ai_state_machine:
    push {r4,lr}                             @ 080bc71c 10b5
    ldr r1, DAT_080bc774                     @ 080bc71e 1549
    ldr r2, PTR_gP1LifePoints_080bc778       @ 080bc720 154a
    ldr r3, DAT_080bc77c                     @ 080bc722 164b
    adds r0,r2,r3    @ 080bc724 d018
    ldr r0,[r0,#0x0]                         @ 080bc726 0068
    str r0,[r1,#0x0]                         @ 080bc728 0860
    ldr r0,[r1,#0x4]                         @ 080bc72a 4868
    adds r4,r1,#0x0    @ 080bc72c 0c1c
    cmp r0,#0x0                              @ 080bc72e 0028
    bne LAB_080bc740                         @ 080bc730 06d1
    ldr r1, DAT_080bc780                     @ 080bc732 1349
    adds r0,r2,r1    @ 080bc734 5018
    ldr r0,[r0,#0x0]                         @ 080bc736 0068
    cmp r0,#0x4                              @ 080bc738 0428
    bne LAB_080bc740                         @ 080bc73a 01d1
    movs r0,#0x7    @ 080bc73c 0720
    str r0,[r4,#0x4]                         @ 080bc73e 6060
LAB_080bc740:
    ldr r1, DAT_080bc784                     @ 080bc740 1049
    ldr r0,[r4,#0x4]                         @ 080bc742 6068
    lsls r0,r0,#0x2    @ 080bc744 8000
    adds r0,r0,r1    @ 080bc746 4018
    ldr r0,[r0,#0x0]                         @ 080bc748 0068
    cmp r0,#0x0                              @ 080bc74a 0028
    beq LAB_080bc78c                         @ 080bc74c 1ed0
    bl invoke_r0                             @ 080bc74e 51f03bff
    cmp r0,#0x0                              @ 080bc752 0028
    beq LAB_080bc76e                         @ 080bc754 0bd0
    movs r0,#0x0    @ 080bc756 0020
    str r0,[r4,#0x8]                         @ 080bc758 a060
    str r0,[r4,#0xc]                         @ 080bc75a e060
    ldr r0,[r4,#0x4]                         @ 080bc75c 6068
    adds r0,#0x1    @ 080bc75e 0130
    str r0,[r4,#0x4]                         @ 080bc760 6060
    ldr r0, PTR_gP1LifePoints_080bc778       @ 080bc762 0548
    ldr r3, DAT_080bc788                     @ 080bc764 084b
    adds r0,r0,r3    @ 080bc766 c018
    ldr r0,[r0,#0x0]                         @ 080bc768 0068
    cmp r0,#0x0                              @ 080bc76a 0028
    bne LAB_080bc78c                         @ 080bc76c 0ed1
LAB_080bc76e:
    movs r0,#0x0    @ 080bc76e 0020
    b LAB_080bc78e                           @ 080bc770 0de0
    .zero  0x2
DAT_080bc774:
    .word  0x0201afe0                     @ 080bc774 e0af0102
PTR_gP1LifePoints_080bc778:
    .word  gP1LifePoints                  @ 080bc778 e0c40102
DAT_080bc77c:
    .word  0x00001ce8                     @ 080bc77c e81c0000
DAT_080bc780:
    .word  0x00001cf4                     @ 080bc780 f41c0000
DAT_080bc784:
    .word  0x09e5ab5c                     @ 080bc784 5cabe509
DAT_080bc788:
    .word  0x00001d30                     @ 080bc788 301d0000
LAB_080bc78c:
    movs r0,#0x1    @ 080bc78c 0120
LAB_080bc78e:
    pop {r4}                                 @ 080bc78e 10bc
    pop {r1}                                 @ 080bc790 02bc
    bx r1                                    @ 080bc792 0847

@ Initialises duel_field slot AOB context structure (DAT_080bc7d4, zero_len=0x6c halfwords=0xd8 bytes) for dispatch_card_display_op cases 0x01 and 0x21. Calls zero_fill_by_halfword(base, 0x6c), writes r0->[base+4], r1->[base+8], r2 (via mov r8,r2 / mov r0,r8)->[base+c]. Sets [base+0] bit0 (init done). Reads gP1LifePoints player bit, ORs 0x4, writes to external ctrl byte. r0=ptr arg_data; r1=ptr arg_target; r2=ptr arg_extra (saved via r8). Returns void. Constants: base_struct=DAT_080bc7d4, zero_len=0x6c halfwords=0xd8 bytes, player_flag_bit=0x4.
init_field_slot_aob_ctx_a:
    push {r4,r5,r6,lr}                       @ 080bc794 70b5
    .hword 0x4646    @ 080bc796 4646
    push {r6}                                @ 080bc798 40b4
    adds r5,r0,#0x0    @ 080bc79a 051c
    adds r6,r1,#0x0    @ 080bc79c 0e1c
    .hword 0x4690    @ 080bc79e 9046
    ldr r4, DAT_080bc7d4                     @ 080bc7a0 0c4c
    adds r0,r4,#0x0    @ 080bc7a2 201c
    movs r1,#0x6c    @ 080bc7a4 6c21
    bl zero_fill_by_halfword                 @ 080bc7a6 38f065fb
    str r5,[r4,#0x4]                         @ 080bc7aa 6560
    str r6,[r4,#0x8]                         @ 080bc7ac a660
    .hword 0x4640    @ 080bc7ae 4046
    str r0,[r4,#0xc]                         @ 080bc7b0 e060
    movs r0,#0x1    @ 080bc7b2 0120
    ldrb r1,[r4,#0x0]                        @ 080bc7b4 2178
    orrs r0,r1    @ 080bc7b6 0843
    strb r0,[r4,#0x0]                        @ 080bc7b8 2070
    ldr r1, DAT_080bc7d8                     @ 080bc7ba 0749
    ldr r2, DAT_080bc7dc                     @ 080bc7bc 074a
    adds r1,r1,r2    @ 080bc7be 8918
    movs r0,#0x4    @ 080bc7c0 0420
    ldrb r2,[r1,#0x0]                        @ 080bc7c2 0a78
    orrs r0,r2    @ 080bc7c4 1043
    strb r0,[r1,#0x0]                        @ 080bc7c6 0870
    pop {r3}                                 @ 080bc7c8 08bc
    .hword 0x4698    @ 080bc7ca 9846
    pop {r4,r5,r6}                           @ 080bc7cc 70bc
    pop {r0}                                 @ 080bc7ce 01bc
    bx r0                                    @ 080bc7d0 0047
    .zero  0x2
DAT_080bc7d4:
    .word  gBannerState                   @ 080bc7d4 c0fe0102
DAT_080bc7d8:
    .word  0x02023130                     @ 080bc7d8 30310202
DAT_080bc7dc:
    .word  0x00000215                     @ 080bc7dc 15020000

@ 给定 BGR555 调色板条目指针 (r0), 目标颜色 (r1, u16), 混合步数 (r2, u16, clamp 至 0x10), 对 R/G/B 各 5 bit 分量执行线性插值混合 (delta*blend_steps/16), 写回 PAL RAM. 由 banner_anim_state_machine / play_ui_effect_04 / FUN_080bd0a8 等 8 个 caller 调用. Constants: COMPONENT_MASK=0x1f, BLEND_DIVISOR=16, PAL_VRAM_BASE=0x05000200, BLEND_MAX_STEPS=0x10.
blend_palette_entry_toward_target:
    push {r4,r5,r6,r7,lr}                    @ 080bc7e0 f0b5
    adds r7,r0,#0x0    @ 080bc7e2 071c
    lsls r1,r1,#0x10    @ 080bc7e4 0904
    lsls r2,r2,#0x10    @ 080bc7e6 1204
    lsrs r5,r2,#0x10    @ 080bc7e8 150c
    lsrs r1,r1,#0xb    @ 080bc7ea c90a
    ldr r0, DAT_080bc87c                     @ 080bc7ec 2348
    adds r6,r1,r0    @ 080bc7ee 0e18
    cmp r5,#0x10                             @ 080bc7f0 102d
    bls LAB_080bc7f6                         @ 080bc7f2 00d9
    movs r5,#0x10    @ 080bc7f4 1025
LAB_080bc7f6:
    movs r4,#0x1f    @ 080bc7f6 1f24
    movs r0,#0xf    @ 080bc7f8 0f20
    .hword 0x4684    @ 080bc7fa 8446
LAB_080bc7fc:
    ldrh r0,[r7,#0x0]                        @ 080bc7fc 3888
    adds r2,r4,#0x0    @ 080bc7fe 221c
    ands r2,r0    @ 080bc800 0240
    lsls r0,r0,#0x10    @ 080bc802 0004
    lsrs r3,r0,#0x15    @ 080bc804 430d
    ands r3,r4    @ 080bc806 2340
    lsrs r1,r0,#0x1a    @ 080bc808 810e
    ands r1,r4    @ 080bc80a 2140
    subs r0,r4,r2    @ 080bc80c a01a
    muls r0,r5    @ 080bc80e 6843
    cmp r0,#0x0                              @ 080bc810 0028
    bge LAB_080bc816                         @ 080bc812 00da
    adds r0,#0xf    @ 080bc814 0f30
LAB_080bc816:
    asrs r0,r0,#0x4    @ 080bc816 0011
    adds r0,r2,r0    @ 080bc818 1018
    lsls r0,r0,#0x18    @ 080bc81a 0006
    lsrs r2,r0,#0x18    @ 080bc81c 020e
    subs r0,r4,r3    @ 080bc81e e01a
    muls r0,r5    @ 080bc820 6843
    cmp r0,#0x0                              @ 080bc822 0028
    bge LAB_080bc828                         @ 080bc824 00da
    adds r0,#0xf    @ 080bc826 0f30
LAB_080bc828:
    asrs r0,r0,#0x4    @ 080bc828 0011
    adds r0,r3,r0    @ 080bc82a 1818
    lsls r0,r0,#0x18    @ 080bc82c 0006
    lsrs r3,r0,#0x18    @ 080bc82e 030e
    subs r0,r4,r1    @ 080bc830 601a
    muls r0,r5    @ 080bc832 6843
    cmp r0,#0x0                              @ 080bc834 0028
    bge LAB_080bc83a                         @ 080bc836 00da
    adds r0,#0xf    @ 080bc838 0f30
LAB_080bc83a:
    asrs r0,r0,#0x4    @ 080bc83a 0011
    adds r0,r1,r0    @ 080bc83c 0818
    lsls r0,r0,#0x18    @ 080bc83e 0006
    lsrs r1,r0,#0x18    @ 080bc840 010e
    cmp r2,#0x1f                             @ 080bc842 1f2a
    bls LAB_080bc848                         @ 080bc844 00d9
    movs r2,#0x1f    @ 080bc846 1f22
LAB_080bc848:
    cmp r3,#0x1f                             @ 080bc848 1f2b
    bls LAB_080bc84e                         @ 080bc84a 00d9
    movs r3,#0x1f    @ 080bc84c 1f23
LAB_080bc84e:
    cmp r1,#0x1f                             @ 080bc84e 1f29
    bls LAB_080bc854                         @ 080bc850 00d9
    movs r1,#0x1f    @ 080bc852 1f21
LAB_080bc854:
    ands r1,r4    @ 080bc854 2140
    lsls r1,r1,#0xa    @ 080bc856 8902
    ands r3,r4    @ 080bc858 2340
    lsls r0,r3,#0x5    @ 080bc85a 5801
    orrs r1,r0    @ 080bc85c 0143
    ands r2,r4    @ 080bc85e 2240
    orrs r2,r1    @ 080bc860 0a43
    strh r2,[r6,#0x0]                        @ 080bc862 3280
    adds r6,#0x2    @ 080bc864 0236
    adds r7,#0x2    @ 080bc866 0237
    movs r0,#0x1    @ 080bc868 0120
    rsbs r0,r0,#0    @ 080bc86a 4042
    add r12,r0                               @ 080bc86c 8444
    .hword 0x4660    @ 080bc86e 6046
    cmp r0,#0x0                              @ 080bc870 0028
    bge LAB_080bc7fc                         @ 080bc872 c3da
    pop {r4,r5,r6,r7}                        @ 080bc874 f0bc
    pop {r0}                                 @ 080bc876 01bc
    bx r0                                    @ 080bc878 0047
    .zero  0x2
DAT_080bc87c:
    .word  0x05000200                     @ 080bc87c 00020005

@ demo 'shuen' (終焉) 过场动画播放协调器. 6-step 顺序状态机 on [gBannerState+0x10]: step 0=等帧 (FUN_080cca5c) / step 1=BG/palette setup (FUN_0801b7e8) / step 2=fs_load 资源 (FUN_0801ba4c) / step 3=播放 demo_shuen_state_machine / step 4=HUD 刷新 + refresh_duel_field_zone_info (强制推进) / step 5=等帧收尾 (FUN_080cca38) / default=cleanup (与 banner_anim_state_machine 同清理协议: 清 gBannerState[+0x0] bit1 + [0x02023345] bit0,2). 返回 1=busy / 0=done. 唯一 caller: play_ui_effect (FUN_0801ef94) case 0x3c (effect_id=0x3c). 推测是 shuen victory anim, 等 runtime 验证.
play_demo_shuen:
    push {lr}                                @ 080bc880 00b5
    ldr r1, DAT_080bc894                     @ 080bc882 0449
    ldrb r0,[r1,#0x10]                       @ 080bc884 087c
    cmp r0,#0x5                              @ 080bc886 0528
    bhi switchD_080bc892__default            @ 080bc888 32d8
    lsls r0,r0,#0x2    @ 080bc88a 8000
    ldr r1, DAT_080bc898                     @ 080bc88c 0249
    adds r0,r0,r1    @ 080bc88e 4018
    ldr r0,[r0,#0x0]                         @ 080bc890 0068
switchD_080bc892__switchD:
    .hword 0x4687    @ 080bc892 8746
DAT_080bc894:
    .word  gBannerState                   @ 080bc894 c0fe0102
DAT_080bc898:
    .word  0x080bc89c                     @ 080bc898 9cc80b08
switchD_080bc892__switchdataD_080bc89c:
    .word  0x080bc8b4                     @ 080bc89c b4c80b08
    .word  0x080bc8ba                     @ 080bc8a0 bac80b08
    .word  0x080bc8c0                     @ 080bc8a4 c0c80b08
    .word  0x080bc8c6                     @ 080bc8a8 c6c80b08
    .word  0x080bc8cc                     @ 080bc8ac ccc80b08
    .word  0x080bc8d6                     @ 080bc8b0 d6c80b08
switchD_080bc892__caseD_0:
    bl tick_duel_field_fadein_step           @ 080bc8b4 10f0d2f8
    b LAB_080bc8da                           @ 080bc8b8 0fe0
switchD_080bc892__caseD_1:
    bl init_demo_shuen_display_state         @ 080bc8ba 5ef795ff
    b LAB_080bc8da                           @ 080bc8be 0ce0
switchD_080bc892__caseD_2:
    bl load_shuen_obj_resource_slot0         @ 080bc8c0 5ff7c4f8
    b LAB_080bc8da                           @ 080bc8c4 09e0
switchD_080bc892__caseD_3:
    bl demo_shuen_state_machine              @ 080bc8c6 5ff71ffa
    b LAB_080bc8da                           @ 080bc8ca 06e0
switchD_080bc892__caseD_4:
    bl init_duel_field_vram_layout           @ 080bc8cc 10f01af8
    bl refresh_duel_field_zone_info          @ 080bc8d0 0ff01cfb
    b LAB_080bc8de                           @ 080bc8d4 03e0
switchD_080bc892__caseD_5:
    bl tick_duel_field_fadeout_step          @ 080bc8d6 10f0aff8
LAB_080bc8da:
    cmp r0,#0x0                              @ 080bc8da 0028
    beq LAB_080bc8e6                         @ 080bc8dc 03d0
LAB_080bc8de:
    ldr r1, DAT_080bc8ec                     @ 080bc8de 0349
    ldrb r0,[r1,#0x10]                       @ 080bc8e0 087c
    adds r0,#0x1    @ 080bc8e2 0130
    strb r0,[r1,#0x10]                       @ 080bc8e4 0874
LAB_080bc8e6:
    movs r0,#0x1    @ 080bc8e6 0120
    b LAB_080bc90c                           @ 080bc8e8 10e0
    .zero  0x2
DAT_080bc8ec:
    .word  gBannerState                   @ 080bc8ec c0fe0102
switchD_080bc892__default:
    movs r0,#0x2    @ 080bc8f0 0220
    rsbs r0,r0,#0    @ 080bc8f2 4042
    ldrb r2,[r1,#0x0]                        @ 080bc8f4 0a78
    ands r0,r2    @ 080bc8f6 1040
    strb r0,[r1,#0x0]                        @ 080bc8f8 0870
    ldr r1, DAT_080bc910                     @ 080bc8fa 0549
    ldr r0, DAT_080bc914                     @ 080bc8fc 0548
    adds r1,r1,r0    @ 080bc8fe 0918
    movs r0,#0x5    @ 080bc900 0520
    rsbs r0,r0,#0    @ 080bc902 4042
    ldrb r2,[r1,#0x0]                        @ 080bc904 0a78
    ands r0,r2    @ 080bc906 1040
    strb r0,[r1,#0x0]                        @ 080bc908 0870
    movs r0,#0x0    @ 080bc90a 0020
LAB_080bc90c:
    pop {r1}                                 @ 080bc90c 02bc
    bx r1                                    @ 080bc90e 0847
DAT_080bc910:
    .word  0x02023130                     @ 080bc910 30310202
DAT_080bc914:
    .word  0x00000215                     @ 080bc914 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x3b 子状态机, 待详细分析.
play_ui_effect_3b:
    push {r4,r5,r6,r7,lr}                    @ 080bc918 f0b5
    .hword 0x464f    @ 080bc91a 4f46
    .hword 0x4646    @ 080bc91c 4646
    push {r6,r7}                             @ 080bc91e c0b4
    ldr r1, DAT_080bc93c                     @ 080bc920 0649
    ldrb r7,[r1,#0xc]                        @ 080bc922 0f7b
    ldrb r3,[r1,#0xd]                        @ 080bc924 4b7b
    ldrb r0,[r1,#0x10]                       @ 080bc926 087c
    adds r2,r1,#0x0    @ 080bc928 0a1c
    cmp r0,#0xb                              @ 080bc92a 0b28
    bls LAB_080bc930                         @ 080bc92c 00d9
    b LAB_080bcba4                           @ 080bc92e 39e1
LAB_080bc930:
    lsls r0,r0,#0x2    @ 080bc930 8000
    ldr r1, DAT_080bc940                     @ 080bc932 0349
    adds r0,r0,r1    @ 080bc934 4018
    ldr r0,[r0,#0x0]                         @ 080bc936 0068
switchD_080bc938__switchD:
    .hword 0x4687    @ 080bc938 8746
    .zero  0x2
DAT_080bc93c:
    .word  gBannerState                   @ 080bc93c c0fe0102
DAT_080bc940:
    .word  0x080bc944                     @ 080bc940 44c90b08
switchD_080bc938__switchdataD_080bc944:
    .word  0x080bc974                     @ 080bc944 74c90b08
    .word  0x080bca78                     @ 080bc948 78ca0b08
    .word  0x080bca84                     @ 080bc94c 84ca0b08
    .word  0x080bcab8                     @ 080bc950 b8ca0b08
    .word  0x080bcb04                     @ 080bc954 04cb0b08
    .word  0x080bcb2c                     @ 080bc958 2ccb0b08
    .word  0x080bcb68                     @ 080bc95c 68cb0b08
    .word  0x080bcb6e                     @ 080bc960 6ecb0b08
    .word  0x080bcb74                     @ 080bc964 74cb0b08
    .word  0x080bcb7a                     @ 080bc968 7acb0b08
    .word  0x080bcb80                     @ 080bc96c 80cb0b08
    .word  0x080bcb8a                     @ 080bc970 8acb0b08
switchD_080bc938__caseD_0:
    cmp r3,#0x0                              @ 080bc974 002b
    beq LAB_080bc97e                         @ 080bc976 02d0
    movs r0,#0x6    @ 080bc978 0620
    strb r0,[r2,#0x10]                       @ 080bc97a 1074
    b LAB_080bcb9a                           @ 080bc97c 0de1
LAB_080bc97e:
    ldr r0, DAT_080bca44                     @ 080bc97e 3148
    ldr r1, DAT_080bca48                     @ 080bc980 3149
    movs r2,#0x20    @ 080bc982 2022
    bl copy_bytes_by_halfword                @ 080bc984 38f08efa
    ldr r4, DAT_080bca4c                     @ 080bc988 304c
    ldr r1, DAT_080bca50                     @ 080bc98a 3149
    adds r0,r4,#0x0    @ 080bc98c 201c
    movs r2,#0x1f    @ 080bc98e 1f22
    movs r3,#0x12    @ 080bc990 1223
    bl tile_2d_row_copy                      @ 080bc992 3af09ffd
    ldr r0, DAT_080bca54                     @ 080bc996 2f48
    ldrh r0,[r0,#0x0]                        @ 080bc998 0088
    lsrs r0,r0,#0x8    @ 080bc99a 000a
    cmp r0,#0x4a                             @ 080bc99c 4a28
    bne LAB_080bc9bc                         @ 080bc99e 0dd1
    ldr r1, DAT_080bca58                     @ 080bc9a0 2d49
    ldr r0, DAT_080bca5c                     @ 080bc9a2 2e48
    adds r1,r1,r0    @ 080bc9a4 0918
    movs r0,#0x7    @ 080bc9a6 0720
    ldrb r1,[r1,#0x0]                        @ 080bc9a8 0978
    ands r0,r1    @ 080bc9aa 0840
    cmp r0,#0x0                              @ 080bc9ac 0028
    bne LAB_080bc9bc                         @ 080bc9ae 05d1
    ldr r1, DAT_080bca60                     @ 080bc9b0 2b49
    adds r0,r4,#0x0    @ 080bc9b2 201c
    movs r2,#0x14    @ 080bc9b4 1422
    movs r3,#0xc    @ 080bc9b6 0c23
    bl tile_2d_row_copy                      @ 080bc9b8 3af08cfd
LAB_080bc9bc:
    ldr r6, DAT_080bca64                     @ 080bc9bc 294e
    ldr r2, DAT_080bca68                     @ 080bc9be 2a4a
    .hword 0x4690    @ 080bc9c0 9046
    ldr r3, DAT_080bca6c                     @ 080bc9c2 2a4b
    .hword 0x4699    @ 080bc9c4 9946
    adds r0,r6,#0x0    @ 080bc9c6 301c
    .hword 0x4641    @ 080bc9c8 4146
    .hword 0x464a    @ 080bc9ca 4a46
    movs r3,#0x1    @ 080bc9cc 0123
    bl init_aob_ctx_from_ptnsect             @ 080bc9ce 3bf0e9f9
    movs r5,#0x1    @ 080bc9d2 0125
    ldrb r0,[r6,#0x13]                       @ 080bc9d4 f07c
    orrs r0,r5    @ 080bc9d6 2843
    strb r0,[r6,#0x13]                       @ 080bc9d8 f074
    adds r0,r6,#0x0    @ 080bc9da 301c
    movs r1,#0x0    @ 080bc9dc 0021
    movs r2,#0x0    @ 080bc9de 0022
    bl init_aob_ctx_with_anm_entry           @ 080bc9e0 3bf032fa
    adds r4,r6,#0x0    @ 080bc9e4 341c
    adds r4,#0x14    @ 080bc9e6 1434
    adds r0,r4,#0x0    @ 080bc9e8 201c
    .hword 0x4641    @ 080bc9ea 4146
    .hword 0x464a    @ 080bc9ec 4a46
    movs r3,#0x1    @ 080bc9ee 0123
    bl init_aob_ctx_from_ptnsect             @ 080bc9f0 3bf0d8f9
    ldrb r0,[r4,#0x13]                       @ 080bc9f4 e07c
    orrs r5,r0    @ 080bc9f6 0543
    strb r5,[r4,#0x13]                       @ 080bc9f8 e574
    adds r1,r7,#0x1    @ 080bc9fa 791c
    adds r0,r4,#0x0    @ 080bc9fc 201c
    movs r2,#0x0    @ 080bc9fe 0022
    bl init_aob_ctx_with_anm_entry           @ 080bca00 3bf022fa
    ldr r1, PTR_WIN0H_080bca70               @ 080bca04 1a49
    ldr r2, DAT_080bca74                     @ 080bca06 1b4a
    adds r0,r2,#0x0    @ 080bca08 101c
    strh r0,[r1,#0x0]                        @ 080bca0a 0880
    adds r1,#0x4    @ 080bca0c 0431
    movs r0,#0x90    @ 080bca0e 9020
    strh r0,[r1,#0x0]                        @ 080bca10 0880
    adds r1,#0x4    @ 080bca12 0431
    movs r0,#0x3f    @ 080bca14 3f20
    strh r0,[r1,#0x0]                        @ 080bca16 0880
    adds r1,#0x2    @ 080bca18 0231
    movs r0,#0x1f    @ 080bca1a 1f20
    strh r0,[r1,#0x0]                        @ 080bca1c 0880
    adds r1,#0xa    @ 080bca1e 0a31
    movs r0,#0x0    @ 080bca20 0020
    strh r0,[r1,#0x0]                        @ 080bca22 0880
    subs r1,#0x4    @ 080bca24 0439
    movs r0,#0xef    @ 080bca26 ef20
    strh r0,[r1,#0x0]                        @ 080bca28 0880
    movs r2,#0x80    @ 080bca2a 8022
    lsls r2,r2,#0x13    @ 080bca2c d204
    ldrh r0,[r2,#0x0]                        @ 080bca2e 1088
    movs r3,#0x80    @ 080bca30 8023
    lsls r3,r3,#0x6    @ 080bca32 9b01
    adds r1,r3,#0x0    @ 080bca34 191c
    orrs r0,r1    @ 080bca36 0843
    strh r0,[r2,#0x0]                        @ 080bca38 1080
    subs r6,#0x1c    @ 080bca3a 1c3e
    ldrb r0,[r6,#0x10]                       @ 080bca3c 307c
    adds r0,#0x1    @ 080bca3e 0130
    strb r0,[r6,#0x10]                       @ 080bca40 3074
    b LAB_080bcb9a                           @ 080bca42 aae0
DAT_080bca44:
    .word  0x05000260                     @ 080bca44 60020005
DAT_080bca48:
    .word  0x0990ca5c                     @ 080bca48 5cca9009
DAT_080bca4c:
    .word  0x06013800                     @ 080bca4c 00380106
DAT_080bca50:
    .word  0x0990ca7c                     @ 080bca50 7cca9009
DAT_080bca54:
    .word  0x080000ae                     @ 080bca54 ae000008
DAT_080bca58:
    .word  0x02000000                     @ 080bca58 00000002
DAT_080bca5c:
    .word  0x00006c2c                     @ 080bca5c 2c6c0000
DAT_080bca60:
    .word  0x0991103c                     @ 080bca60 3c109109
DAT_080bca64:
    .word  0x0201fedc                     @ 080bca64 dcfe0102
DAT_080bca68:
    .word  0x0990c4ac                     @ 080bca68 acc49009
DAT_080bca6c:
    .word  0x01c00003                     @ 080bca6c 0300c001
PTR_WIN0H_080bca70:
    .word  WIN0H                          @ 080bca70 40000004
DAT_080bca74:
    .word  0x000028f0                     @ 080bca74 f0280000
switchD_080bc938__caseD_1:
    ldr r1, PTR_BLDY_080bca80                @ 080bca78 0149
    ldrb r0,[r2,#0x11]                       @ 080bca7a 507c
    strh r0,[r1,#0x0]                        @ 080bca7c 0880
    b LAB_080bcb0e                           @ 080bca7e 46e0
PTR_BLDY_080bca80:
    .word  BLDY                           @ 080bca80 54000004
switchD_080bc938__caseD_2:
    ldr r4, DAT_080bcab0                     @ 080bca84 0a4c
    ldr r1, DAT_080bcab4                     @ 080bca86 0b49
    adds r0,r4,#0x0    @ 080bca88 201c
    movs r2,#0x0    @ 080bca8a 0022
    movs r3,#0x0    @ 080bca8c 0023
    bl render_aob_frame_to_oam               @ 080bca8e 3bf0b7fa
    adds r0,r4,#0x0    @ 080bca92 201c
    bl tick_aob_frame_counter                @ 080bca94 3bf038fa
    cmp r0,#0x0                              @ 080bca98 0028
    beq LAB_080bca9e                         @ 080bca9a 00d0
    b LAB_080bcb9a                           @ 080bca9c 7de0
LAB_080bca9e:
    adds r1,r4,#0x0    @ 080bca9e 211c
    subs r1,#0x1c    @ 080bcaa0 1c39
    ldrb r0,[r1,#0x10]                       @ 080bcaa2 087c
    adds r0,#0x1    @ 080bcaa4 0130
    strb r0,[r1,#0x10]                       @ 080bcaa6 0874
    movs r0,#0xc    @ 080bcaa8 0c20
    bl sync_state_and_init_sprite            @ 080bcaaa 3df003f8
    b LAB_080bcb9a                           @ 080bcaae 74e0
DAT_080bcab0:
    .word  0x0201fedc                     @ 080bcab0 dcfe0102
DAT_080bcab4:
    .word  0x0028006d                     @ 080bcab4 6d002800
switchD_080bc938__caseD_3:
    ldr r4, DAT_080bcaf0                     @ 080bcab8 0d4c
    ldr r1, DAT_080bcaf4                     @ 080bcaba 0e49
    adds r0,r4,#0x0    @ 080bcabc 201c
    movs r2,#0x0    @ 080bcabe 0022
    movs r3,#0x0    @ 080bcac0 0023
    bl render_aob_frame_to_oam               @ 080bcac2 3bf09dfa
    adds r0,r4,#0x0    @ 080bcac6 201c
    bl tick_aob_frame_counter                @ 080bcac8 3bf01efa
    adds r2,r0,#0x0    @ 080bcacc 021c
    cmp r2,#0x0                              @ 080bcace 002a
    bne LAB_080bcb9a                         @ 080bcad0 63d1
    adds r1,r4,#0x0    @ 080bcad2 211c
    subs r1,#0x30    @ 080bcad4 3039
    ldrb r0,[r1,#0x11]                       @ 080bcad6 487c
    adds r0,#0x1    @ 080bcad8 0130
    strb r0,[r1,#0x11]                       @ 080bcada 4874
    lsls r0,r0,#0x18    @ 080bcadc 0006
    lsrs r0,r0,#0x18    @ 080bcade 000e
    cmp r0,#0x3                              @ 080bcae0 0328
    bls LAB_080bcaf8                         @ 080bcae2 09d9
    ldrb r0,[r1,#0x10]                       @ 080bcae4 087c
    adds r0,#0x1    @ 080bcae6 0130
    strb r0,[r1,#0x10]                       @ 080bcae8 0874
    strb r2,[r1,#0x11]                       @ 080bcaea 4a74
    b LAB_080bcb9a                           @ 080bcaec 55e0
    .zero  0x2
DAT_080bcaf0:
    .word  0x0201fef0                     @ 080bcaf0 f0fe0102
DAT_080bcaf4:
    .word  0x0028006d                     @ 080bcaf4 6d002800
LAB_080bcaf8:
    adds r1,r7,#0x1    @ 080bcaf8 791c
    adds r0,r4,#0x0    @ 080bcafa 201c
    movs r2,#0x0    @ 080bcafc 0022
    bl init_aob_ctx_with_anm_entry           @ 080bcafe 3bf0a3f9
    b LAB_080bcb9a                           @ 080bcb02 4ae0
switchD_080bc938__caseD_4:
    ldr r0, PTR_BLDY_080bcb28                @ 080bcb04 0848
    movs r1,#0x8    @ 080bcb06 0821
    ldrb r3,[r2,#0x11]                       @ 080bcb08 537c
    subs r1,r1,r3    @ 080bcb0a c91a
    strh r1,[r0,#0x0]                        @ 080bcb0c 0180
LAB_080bcb0e:
    ldrb r0,[r2,#0x11]                       @ 080bcb0e 507c
    adds r0,#0x1    @ 080bcb10 0130
    strb r0,[r2,#0x11]                       @ 080bcb12 5074
    lsls r0,r0,#0x18    @ 080bcb14 0006
    lsrs r0,r0,#0x18    @ 080bcb16 000e
    cmp r0,#0x8                              @ 080bcb18 0828
    bls LAB_080bcb9a                         @ 080bcb1a 3ed9
    ldrb r0,[r2,#0x10]                       @ 080bcb1c 107c
    adds r0,#0x1    @ 080bcb1e 0130
    strb r0,[r2,#0x10]                       @ 080bcb20 1074
    movs r0,#0x0    @ 080bcb22 0020
    strb r0,[r2,#0x11]                       @ 080bcb24 5074
    b LAB_080bcb9a                           @ 080bcb26 38e0
PTR_BLDY_080bcb28:
    .word  BLDY                           @ 080bcb28 54000004
switchD_080bc938__caseD_5:
    bl disable_blend_and_clear_step          @ 080bcb2c 38f052fd
    movs r2,#0x80    @ 080bcb30 8022
    lsls r2,r2,#0x13    @ 080bcb32 d204
    ldrh r1,[r2,#0x0]                        @ 080bcb34 1188
    ldr r0, DAT_080bcb58                     @ 080bcb36 0848
    ands r0,r1    @ 080bcb38 0840
    strh r0,[r2,#0x0]                        @ 080bcb3a 1080
    ldr r1, DAT_080bcb5c                     @ 080bcb3c 0749
    ldrb r0,[r1,#0x10]                       @ 080bcb3e 087c
    adds r0,#0x1    @ 080bcb40 0130
    strb r0,[r1,#0x10]                       @ 080bcb42 0874
    movs r0,#0x2    @ 080bcb44 0220
    rsbs r0,r0,#0    @ 080bcb46 4042
    ldrb r2,[r1,#0x0]                        @ 080bcb48 0a78
    ands r0,r2    @ 080bcb4a 1040
    strb r0,[r1,#0x0]                        @ 080bcb4c 0870
    ldr r1, DAT_080bcb60                     @ 080bcb4e 0449
    ldr r3, DAT_080bcb64                     @ 080bcb50 044b
    adds r1,r1,r3    @ 080bcb52 c918
    b switchD_080bc938__default              @ 080bcb54 2ee0
    .zero  0x2
DAT_080bcb58:
    .word  0x0000dfff                     @ 080bcb58 ffdf0000
DAT_080bcb5c:
    .word  gBannerState                   @ 080bcb5c c0fe0102
DAT_080bcb60:
    .word  0x02023130                     @ 080bcb60 30310202
DAT_080bcb64:
    .word  0x00000215                     @ 080bcb64 15020000
switchD_080bc938__caseD_6:
    bl tick_duel_field_fadein_step           @ 080bcb68 0ff078ff
    b LAB_080bcb8e                           @ 080bcb6c 0fe0
switchD_080bc938__caseD_7:
    bl reset_gl_display_state                @ 080bcb6e 5ff79dfb
    b LAB_080bcb8e                           @ 080bcb72 0ce0
switchD_080bc938__caseD_8:
    bl load_vija_obj_resource_gated          @ 080bcb74 5ff7cafc
    b LAB_080bcb8e                           @ 080bcb78 09e0
switchD_080bc938__caseD_9:
    bl run_vija_scene_state_machine          @ 080bcb7a 5ff7c1ff
    b LAB_080bcb8e                           @ 080bcb7e 06e0
switchD_080bc938__caseD_a:
    bl init_duel_field_vram_layout           @ 080bcb80 0ff0c0fe
    bl refresh_duel_field_zone_info          @ 080bcb84 0ff0c2f9
    b LAB_080bcb92                           @ 080bcb88 03e0
switchD_080bc938__caseD_b:
    bl tick_duel_field_fadeout_step          @ 080bcb8a 0ff055ff
LAB_080bcb8e:
    cmp r0,#0x0                              @ 080bcb8e 0028
    beq LAB_080bcb9a                         @ 080bcb90 03d0
LAB_080bcb92:
    ldr r1, DAT_080bcba0                     @ 080bcb92 0349
    ldrb r0,[r1,#0x10]                       @ 080bcb94 087c
    adds r0,#0x1    @ 080bcb96 0130
    strb r0,[r1,#0x10]                       @ 080bcb98 0874
LAB_080bcb9a:
    movs r0,#0x1    @ 080bcb9a 0120
    b LAB_080bcbc0                           @ 080bcb9c 10e0
    .zero  0x2
DAT_080bcba0:
    .word  gBannerState                   @ 080bcba0 c0fe0102
LAB_080bcba4:
    movs r0,#0x2    @ 080bcba4 0220
    rsbs r0,r0,#0    @ 080bcba6 4042
    ldrb r3,[r1,#0x0]                        @ 080bcba8 0b78
    ands r0,r3    @ 080bcbaa 1840
    strb r0,[r1,#0x0]                        @ 080bcbac 0870
    ldr r1, DAT_080bcbcc                     @ 080bcbae 0749
    ldr r0, DAT_080bcbd0                     @ 080bcbb0 0748
    adds r1,r1,r0    @ 080bcbb2 0918
switchD_080bc938__default:
    movs r0,#0x5    @ 080bcbb4 0520
    rsbs r0,r0,#0    @ 080bcbb6 4042
    ldrb r2,[r1,#0x0]                        @ 080bcbb8 0a78
    ands r0,r2    @ 080bcbba 1040
    strb r0,[r1,#0x0]                        @ 080bcbbc 0870
    movs r0,#0x0    @ 080bcbbe 0020
LAB_080bcbc0:
    pop {r3,r4}                              @ 080bcbc0 18bc
    .hword 0x4698    @ 080bcbc2 9846
    .hword 0x46a1    @ 080bcbc4 a146
    pop {r4,r5,r6,r7}                        @ 080bcbc6 f0bc
    pop {r1}                                 @ 080bcbc8 02bc
    bx r1                                    @ 080bcbca 0847
DAT_080bcbcc:
    .word  0x02023130                     @ 080bcbcc 30310202
DAT_080bcbd0:
    .word  0x00000215                     @ 080bcbd0 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x3a 子状态机, 待详细分析.
play_ui_effect_3a:
    push {lr}                                @ 080bcbd4 00b5
    ldr r1, DAT_080bcbe8                     @ 080bcbd6 0449
    ldrb r0,[r1,#0x10]                       @ 080bcbd8 087c
    cmp r0,#0x5                              @ 080bcbda 0528
    bhi switchD_080bcbe6__default            @ 080bcbdc 32d8
    lsls r0,r0,#0x2    @ 080bcbde 8000
    ldr r1, DAT_080bcbec                     @ 080bcbe0 0249
    adds r0,r0,r1    @ 080bcbe2 4018
    ldr r0,[r0,#0x0]                         @ 080bcbe4 0068
switchD_080bcbe6__switchD:
    .hword 0x4687    @ 080bcbe6 8746
DAT_080bcbe8:
    .word  gBannerState                   @ 080bcbe8 c0fe0102
DAT_080bcbec:
    .word  0x080bcbf0                     @ 080bcbec f0cb0b08
switchD_080bcbe6__switchdataD_080bcbf0:
    .word  0x080bcc08                     @ 080bcbf0 08cc0b08
    .word  0x080bcc0e                     @ 080bcbf4 0ecc0b08
    .word  0x080bcc14                     @ 080bcbf8 14cc0b08
    .word  0x080bcc1a                     @ 080bcbfc 1acc0b08
    .word  0x080bcc20                     @ 080bcc00 20cc0b08
    .word  0x080bcc2a                     @ 080bcc04 2acc0b08
switchD_080bcbe6__caseD_0:
    bl tick_duel_field_fadein_step           @ 080bcc08 0ff028ff
    b LAB_080bcc2e                           @ 080bcc0c 0fe0
switchD_080bcbe6__caseD_1:
    bl reset_display_and_gl_state            @ 080bcc0e 56f77ffc
    b LAB_080bcc2e                           @ 080bcc12 0ce0
switchD_080bcbe6__caseD_2:
    bl load_demo_obj_resource_slot0          @ 080bcc14 56f7bafe
    b LAB_080bcc2e                           @ 080bcc18 09e0
switchD_080bcbe6__caseD_3:
    bl tick_demo_scene_state_machine         @ 080bcc1a 56f7dbff
    b LAB_080bcc2e                           @ 080bcc1e 06e0
switchD_080bcbe6__caseD_4:
    bl init_duel_field_vram_layout           @ 080bcc20 0ff070fe
    bl refresh_duel_field_zone_info          @ 080bcc24 0ff072f9
    b LAB_080bcc32                           @ 080bcc28 03e0
switchD_080bcbe6__caseD_5:
    bl tick_duel_field_fadeout_step          @ 080bcc2a 0ff005ff
LAB_080bcc2e:
    cmp r0,#0x0                              @ 080bcc2e 0028
    beq LAB_080bcc3a                         @ 080bcc30 03d0
LAB_080bcc32:
    ldr r1, DAT_080bcc40                     @ 080bcc32 0349
    ldrb r0,[r1,#0x10]                       @ 080bcc34 087c
    adds r0,#0x1    @ 080bcc36 0130
    strb r0,[r1,#0x10]                       @ 080bcc38 0874
LAB_080bcc3a:
    movs r0,#0x1    @ 080bcc3a 0120
    b LAB_080bcc60                           @ 080bcc3c 10e0
    .zero  0x2
DAT_080bcc40:
    .word  gBannerState                   @ 080bcc40 c0fe0102
switchD_080bcbe6__default:
    movs r0,#0x2    @ 080bcc44 0220
    rsbs r0,r0,#0    @ 080bcc46 4042
    ldrb r2,[r1,#0x0]                        @ 080bcc48 0a78
    ands r0,r2    @ 080bcc4a 1040
    strb r0,[r1,#0x0]                        @ 080bcc4c 0870
    ldr r1, DAT_080bcc64                     @ 080bcc4e 0549
    ldr r0, DAT_080bcc68                     @ 080bcc50 0548
    adds r1,r1,r0    @ 080bcc52 0918
    movs r0,#0x5    @ 080bcc54 0520
    rsbs r0,r0,#0    @ 080bcc56 4042
    ldrb r2,[r1,#0x0]                        @ 080bcc58 0a78
    ands r0,r2    @ 080bcc5a 1040
    strb r0,[r1,#0x0]                        @ 080bcc5c 0870
    movs r0,#0x0    @ 080bcc5e 0020
LAB_080bcc60:
    pop {r1}                                 @ 080bcc60 02bc
    bx r1                                    @ 080bcc62 0847
DAT_080bcc64:
    .word  0x02023130                     @ 080bcc64 30310202
DAT_080bcc68:
    .word  0x00000215                     @ 080bcc68 15020000

@ banner 动画帧状态机 tick 分派器. 读取 gBannerState[+0x11] (byte, 状态索引 [0..8]), 超出范围则跳转到默认 handler (LAB_080bd09c). 在范围内则以 state*4 查找跳转表 (switchD_080bcc8e__switchdataD_080bcc98, 9 个 entry: 0x080bccbc..0x080bd080), 通过 bx 跳入对应 handler. 每个 case 处理一种 banner 动画阶段 (初始化/过渡/显示/退出等). case 0 (0x080bccbc): 进一步判断 r2 (= gBannerState 基址) [+0x1/+0x2] 字段决定子 case. 3 个 caller 均属相同 banner/display/palette/vram 场景 (FUN_080bd0a8, FUN_080bd3f4, FUN_080bd660), 均为 banner 状态机的外层 tick 循环调用本函数推进一帧. Constants: gBannerState (0x0201fec0): banner 全局状态结构基址; gBannerState[+0x11]: 主状态索引 [0..8]; 0x8 = 最大合法状态; switchD_080bcc8e__switchdataD_080bcc98: 9-entry 跳转表; r7 = 0x18 / r5 = 0x30: 参数常量 (传递给 sub-handler).
dispatch_banner_anim_tick_by_state:
    push {r4,r5,r6,r7,lr}                    @ 080bcc6c f0b5
    .hword 0x4647    @ 080bcc6e 4746
    push {r7}                                @ 080bcc70 80b4
    ldr r0, DAT_080bcc90                     @ 080bcc72 0748
    ldr r1,[r0,#0x8]                         @ 080bcc74 8168
    .hword 0x4688    @ 080bcc76 8846
    movs r7,#0x18    @ 080bcc78 1827
    movs r5,#0x30    @ 080bcc7a 3025
    ldrb r1,[r0,#0x11]                       @ 080bcc7c 417c
    adds r2,r0,#0x0    @ 080bcc7e 021c
    cmp r1,#0x8                              @ 080bcc80 0829
    bls LAB_080bcc86                         @ 080bcc82 00d9
switchD_080bcc8e__default:
    b LAB_080bd09c                           @ 080bcc84 0ae2
LAB_080bcc86:
    lsls r0,r1,#0x2    @ 080bcc86 8800
    ldr r1, DAT_080bcc94                     @ 080bcc88 0249
    adds r0,r0,r1    @ 080bcc8a 4018
    ldr r0,[r0,#0x0]                         @ 080bcc8c 0068
switchD_080bcc8e__switchD:
    .hword 0x4687    @ 080bcc8e 8746
DAT_080bcc90:
    .word  gBannerState                   @ 080bcc90 c0fe0102
DAT_080bcc94:
    .word  0x080bcc98                     @ 080bcc94 98cc0b08
switchD_080bcc8e__switchdataD_080bcc98:
    .word  0x080bccbc                     @ 080bcc98 bccc0b08
    .word  0x080bcd90                     @ 080bcc9c 90cd0b08
    .word  0x080bcdf8                     @ 080bcca0 f8cd0b08
    .word  0x080bce00                     @ 080bcca4 00ce0b08
    .word  0x080bce68                     @ 080bcca8 68ce0b08
    .word  0x080bcf1c                     @ 080bccac 1ccf0b08
    .word  0x080bcfac                     @ 080bccb0 accf0b08
    .word  0x080bcffc                     @ 080bccb4 fccf0b08
    .word  0x080bd080                     @ 080bccb8 80d00b08
switchD_080bcc8e__caseD_0:
    .hword 0x4642    @ 080bccbc 4246
    cmp r2,#0x1                              @ 080bccbe 012a
    beq LAB_080bccc8                         @ 080bccc0 02d0
    cmp r2,#0x2                              @ 080bccc2 022a
    beq LAB_080bccf4                         @ 080bccc4 16d0
    b LAB_080bcd0c                           @ 080bccc6 21e0
LAB_080bccc8:
    ldr r0, DAT_080bcce4                     @ 080bccc8 0648
    ldr r3, DAT_080bcce8                     @ 080bccca 074b
    adds r0,r0,r3    @ 080bcccc c018
    ldrb r0,[r0,#0x0]                        @ 080bccce 0078
    lsls r0,r0,#0x1d    @ 080bccd0 4007
    lsrs r0,r0,#0x1d    @ 080bccd2 400f
    lsls r1,r0,#0x1    @ 080bccd4 4100
    adds r1,r1,r0    @ 080bccd6 0918
    lsls r1,r1,#0xb    @ 080bccd8 c902
    ldr r0, DAT_080bccec                     @ 080bccda 0448
    adds r4,r1,r0    @ 080bccdc 0c18
    ldr r3, DAT_080bccf0                     @ 080bccde 044b
    b LAB_080bcd0c                           @ 080bcce0 14e0
    .zero  0x2
DAT_080bcce4:
    .word  0x02000000                     @ 080bcce4 00000002
DAT_080bcce8:
    .word  0x00006c2c                     @ 080bcce8 2c6c0000
DAT_080bccec:
    .word  0x0993b6dc                     @ 080bccec dcb69309
DAT_080bccf0:
    .word  0x0993b6bc                     @ 080bccf0 bcb69309
LAB_080bccf4:
    ldr r0, DAT_080bcd70                     @ 080bccf4 1e48
    ldr r4, DAT_080bcd74                     @ 080bccf6 1f4c
    adds r0,r0,r4    @ 080bccf8 0019
    ldrb r0,[r0,#0x0]                        @ 080bccfa 0078
    lsls r0,r0,#0x1d    @ 080bccfc 4007
    lsrs r0,r0,#0x1d    @ 080bccfe 400f
    lsls r1,r0,#0x1    @ 080bcd00 4100
    adds r1,r1,r0    @ 080bcd02 0918
    lsls r1,r1,#0xb    @ 080bcd04 c902
    ldr r0, DAT_080bcd78                     @ 080bcd06 1c48
    adds r4,r1,r0    @ 080bcd08 0c18
    ldr r3, DAT_080bcd7c                     @ 080bcd0a 1c4b
LAB_080bcd0c:
    ldr r0, DAT_080bcd80                     @ 080bcd0c 1c48
    adds r1,r3,#0x0    @ 080bcd0e 191c
    movs r2,#0x20    @ 080bcd10 2022
    bl copy_bytes_by_halfword                @ 080bcd12 38f0c7f8
    ldr r0, DAT_080bcd84                     @ 080bcd16 1b48
    adds r1,r4,#0x0    @ 080bcd18 211c
    movs r2,#0x18    @ 080bcd1a 1822
    movs r3,#0x8    @ 080bcd1c 0823
    bl tile_2d_row_copy                      @ 080bcd1e 3af0d9fb
    ldr r1, PTR_BLDCNT_080bcd88              @ 080bcd22 1949
    movs r2,#0xfd    @ 080bcd24 fd22
    lsls r2,r2,#0x6    @ 080bcd26 9201
    adds r0,r2,#0x0    @ 080bcd28 101c
    strh r0,[r1,#0x0]                        @ 080bcd2a 0880
    adds r1,#0x2    @ 080bcd2c 0231
    movs r0,#0x10    @ 080bcd2e 1020
    strh r0,[r1,#0x0]                        @ 080bcd30 0880
    movs r4,#0x0    @ 080bcd32 0024
    lsls r6,r5,#0x10    @ 080bcd34 2e04
    adds r5,r7,#0x0    @ 080bcd36 3d1c
LAB_080bcd38:
    adds r0,r5,#0x0    @ 080bcd38 281c
    orrs r0,r6    @ 080bcd3a 3043
    lsls r2,r4,#0x3    @ 080bcd3c e200
    movs r3,#0x80    @ 080bcd3e 8023
    lsls r3,r3,#0x2    @ 080bcd40 9b00
    adds r2,r2,r3    @ 080bcd42 d218
    movs r3,#0xc0    @ 080bcd44 c023
    lsls r3,r3,#0x6    @ 080bcd46 9b01
    adds r1,r3,#0x0    @ 080bcd48 191c
    orrs r2,r1    @ 080bcd4a 0a43
    lsls r2,r2,#0x10    @ 080bcd4c 1204
    lsrs r2,r2,#0x10    @ 080bcd4e 120c
    movs r1,#0xc0    @ 080bcd50 c021
    bl write_oam_entry_from_packed_args      @ 080bcd52 39f00bfa
    adds r5,#0x40    @ 080bcd56 4035
    adds r4,#0x1    @ 080bcd58 0134
    cmp r4,#0x2                              @ 080bcd5a 022c
    ble LAB_080bcd38                         @ 080bcd5c ecdd
    ldr r0, DAT_080bcd8c                     @ 080bcd5e 0b48
    movs r1,#0x0    @ 080bcd60 0021
    strh r1,[r0,#0x12]                       @ 080bcd62 4182
    ldrb r1,[r0,#0x11]                       @ 080bcd64 417c
    adds r1,#0x1    @ 080bcd66 0131
    strb r1,[r0,#0x11]                       @ 080bcd68 4174
LAB_080bcd6a:
    movs r0,#0x1    @ 080bcd6a 0120
    b LAB_080bd09e                           @ 080bcd6c 97e1
    .zero  0x2
DAT_080bcd70:
    .word  0x02000000                     @ 080bcd70 00000002
DAT_080bcd74:
    .word  0x00006c2c                     @ 080bcd74 2c6c0000
DAT_080bcd78:
    .word  0x099446fc                     @ 080bcd78 fc469409
DAT_080bcd7c:
    .word  0x099446dc                     @ 080bcd7c dc469409
DAT_080bcd80:
    .word  0x05000280                     @ 080bcd80 80020005
DAT_080bcd84:
    .word  0x06016000                     @ 080bcd84 00600106
PTR_BLDCNT_080bcd88:
    .word  BLDCNT                         @ 080bcd88 50000004
DAT_080bcd8c:
    .word  gBannerState                   @ 080bcd8c c0fe0102
switchD_080bcc8e__caseD_1:
    ldr r3, PTR_BLDALPHA_080bcdf0            @ 080bcd90 174b
    ldrb r1,[r2,#0x12]                       @ 080bcd92 917c
    lsls r2,r1,#0x1    @ 080bcd94 4a00
    movs r0,#0x10    @ 080bcd96 1020
    subs r0,r0,r2    @ 080bcd98 801a
    lsls r0,r0,#0x18    @ 080bcd9a 0006
    lsrs r0,r0,#0x18    @ 080bcd9c 000e
    lsls r1,r1,#0x19    @ 080bcd9e 4906
    lsrs r1,r1,#0x10    @ 080bcda0 090c
    orrs r0,r1    @ 080bcda2 0843
    strh r0,[r3,#0x0]                        @ 080bcda4 1880
    movs r4,#0x0    @ 080bcda6 0024
    lsls r6,r5,#0x10    @ 080bcda8 2e04
    adds r5,r7,#0x0    @ 080bcdaa 3d1c
LAB_080bcdac:
    adds r0,r5,#0x0    @ 080bcdac 281c
    orrs r0,r6    @ 080bcdae 3043
    lsls r2,r4,#0x3    @ 080bcdb0 e200
    movs r1,#0x80    @ 080bcdb2 8021
    lsls r1,r1,#0x2    @ 080bcdb4 8900
    adds r2,r2,r1    @ 080bcdb6 5218
    movs r3,#0xc0    @ 080bcdb8 c023
    lsls r3,r3,#0x6    @ 080bcdba 9b01
    adds r1,r3,#0x0    @ 080bcdbc 191c
    orrs r2,r1    @ 080bcdbe 0a43
    lsls r2,r2,#0x10    @ 080bcdc0 1204
    lsrs r2,r2,#0x10    @ 080bcdc2 120c
    movs r1,#0x98    @ 080bcdc4 9821
    lsls r1,r1,#0x3    @ 080bcdc6 c900
    bl write_oam_entry_from_packed_args      @ 080bcdc8 39f0d0f9
    adds r5,#0x40    @ 080bcdcc 4035
    adds r4,#0x1    @ 080bcdce 0134
    cmp r4,#0x2                              @ 080bcdd0 022c
    ble LAB_080bcdac                         @ 080bcdd2 ebdd
    ldr r1, DAT_080bcdf4                     @ 080bcdd4 0749
    ldrh r0,[r1,#0x12]                       @ 080bcdd6 488a
    adds r0,#0x1    @ 080bcdd8 0130
    strh r0,[r1,#0x12]                       @ 080bcdda 4882
    lsls r0,r0,#0x10    @ 080bcddc 0004
    lsrs r0,r0,#0x10    @ 080bcdde 000c
    cmp r0,#0x8                              @ 080bcde0 0828
    bls LAB_080bcd6a                         @ 080bcde2 c2d9
    ldrb r0,[r1,#0x11]                       @ 080bcde4 487c
    adds r0,#0x1    @ 080bcde6 0130
    strb r0,[r1,#0x11]                       @ 080bcde8 4874
    movs r0,#0x0    @ 080bcdea 0020
    strh r0,[r1,#0x12]                       @ 080bcdec 4882
    b LAB_080bcd6a                           @ 080bcdee bce7
PTR_BLDALPHA_080bcdf0:
    .word  BLDALPHA                       @ 080bcdf0 52000004
DAT_080bcdf4:
    .word  gBannerState                   @ 080bcdf4 c0fe0102
switchD_080bcc8e__caseD_2:
    ldrb r0,[r2,#0x11]                       @ 080bcdf8 507c
    adds r0,#0x1    @ 080bcdfa 0130
    strb r0,[r2,#0x11]                       @ 080bcdfc 5074
    b LAB_080bcd6a                           @ 080bcdfe b4e7
switchD_080bcc8e__caseD_3:
    ldr r3, PTR_BLDALPHA_080bce60            @ 080bce00 174b
    ldrb r1,[r2,#0x12]                       @ 080bce02 917c
    lsls r2,r1,#0x1    @ 080bce04 4a00
    lsls r1,r1,#0x19    @ 080bce06 4906
    lsrs r1,r1,#0x18    @ 080bce08 090e
    movs r0,#0x10    @ 080bce0a 1020
    subs r0,r0,r2    @ 080bce0c 801a
    lsls r0,r0,#0x18    @ 080bce0e 0006
    lsrs r0,r0,#0x10    @ 080bce10 000c
    orrs r1,r0    @ 080bce12 0143
    strh r1,[r3,#0x0]                        @ 080bce14 1980
    movs r4,#0x0    @ 080bce16 0024
    lsls r6,r5,#0x10    @ 080bce18 2e04
    adds r5,r7,#0x0    @ 080bce1a 3d1c
LAB_080bce1c:
    adds r0,r5,#0x0    @ 080bce1c 281c
    orrs r0,r6    @ 080bce1e 3043
    lsls r2,r4,#0x3    @ 080bce20 e200
    movs r1,#0xc0    @ 080bce22 c021
    lsls r1,r1,#0x2    @ 080bce24 8900
    adds r2,r2,r1    @ 080bce26 5218
    movs r3,#0x80    @ 080bce28 8023
    lsls r3,r3,#0x7    @ 080bce2a db01
    adds r1,r3,#0x0    @ 080bce2c 191c
    orrs r2,r1    @ 080bce2e 0a43
    lsls r2,r2,#0x10    @ 080bce30 1204
    lsrs r2,r2,#0x10    @ 080bce32 120c
    movs r1,#0x98    @ 080bce34 9821
    lsls r1,r1,#0x3    @ 080bce36 c900
    bl write_oam_entry_from_packed_args      @ 080bce38 39f098f9
    adds r5,#0x40    @ 080bce3c 4035
    adds r4,#0x1    @ 080bce3e 0134
    cmp r4,#0x2                              @ 080bce40 022c
    ble LAB_080bce1c                         @ 080bce42 ebdd
    ldr r1, DAT_080bce64                     @ 080bce44 0749
    ldrh r0,[r1,#0x12]                       @ 080bce46 488a
    adds r0,#0x1    @ 080bce48 0130
    strh r0,[r1,#0x12]                       @ 080bce4a 4882
    lsls r0,r0,#0x10    @ 080bce4c 0004
    lsrs r0,r0,#0x10    @ 080bce4e 000c
    cmp r0,#0x8                              @ 080bce50 0828
    bls LAB_080bcd6a                         @ 080bce52 8ad9
    ldrb r0,[r1,#0x11]                       @ 080bce54 487c
    adds r0,#0x1    @ 080bce56 0130
    strb r0,[r1,#0x11]                       @ 080bce58 4874
    movs r0,#0x0    @ 080bce5a 0020
    strh r0,[r1,#0x12]                       @ 080bce5c 4882
    b LAB_080bcd6a                           @ 080bce5e 84e7
PTR_BLDALPHA_080bce60:
    .word  BLDALPHA                       @ 080bce60 52000004
DAT_080bce64:
    .word  gBannerState                   @ 080bce64 c0fe0102
switchD_080bcc8e__caseD_4:
    movs r4,#0x0    @ 080bce68 0024
    lsls r6,r5,#0x10    @ 080bce6a 2e04
    adds r5,r7,#0x0    @ 080bce6c 3d1c
LAB_080bce6e:
    adds r0,r5,#0x0    @ 080bce6e 281c
    orrs r0,r6    @ 080bce70 3043
    lsls r2,r4,#0x3    @ 080bce72 e200
    movs r1,#0xc0    @ 080bce74 c021
    lsls r1,r1,#0x2    @ 080bce76 8900
    adds r2,r2,r1    @ 080bce78 5218
    movs r3,#0x80    @ 080bce7a 8023
    lsls r3,r3,#0x7    @ 080bce7c db01
    adds r1,r3,#0x0    @ 080bce7e 191c
    orrs r2,r1    @ 080bce80 0a43
    lsls r2,r2,#0x10    @ 080bce82 1204
    lsrs r2,r2,#0x10    @ 080bce84 120c
    movs r1,#0xc0    @ 080bce86 c021
    bl write_oam_entry_from_packed_args      @ 080bce88 39f070f9
    adds r5,#0x40    @ 080bce8c 4035
    adds r4,#0x1    @ 080bce8e 0134
    cmp r4,#0x2                              @ 080bce90 022c
    ble LAB_080bce6e                         @ 080bce92 ecdd
    ldr r1, DAT_080bcee4                     @ 080bce94 1349
    ldrh r0,[r1,#0x12]                       @ 080bce96 488a
    adds r0,#0x1    @ 080bce98 0130
    strh r0,[r1,#0x12]                       @ 080bce9a 4882
    lsls r0,r0,#0x10    @ 080bce9c 0004
    lsrs r0,r0,#0x10    @ 080bce9e 000c
    cmp r0,#0x20                             @ 080bcea0 2028
    bhi LAB_080bcea6                         @ 080bcea2 00d8
    b LAB_080bcd6a                           @ 080bcea4 61e7
LAB_080bcea6:
    ldrb r0,[r1,#0x11]                       @ 080bcea6 487c
    adds r0,#0x1    @ 080bcea8 0130
    strb r0,[r1,#0x11]                       @ 080bceaa 4874
    movs r0,#0x0    @ 080bceac 0020
    strh r0,[r1,#0x12]                       @ 080bceae 4882
    ldr r1, DAT_080bcee8                     @ 080bceb0 0d49
    ldr r4, DAT_080bceec                     @ 080bceb2 0e4c
    adds r1,r1,r4    @ 080bceb4 0919
    movs r0,#0x8    @ 080bceb6 0820
    ldrb r2,[r1,#0x0]                        @ 080bceb8 0a78
    orrs r0,r2    @ 080bceba 1043
    strb r0,[r1,#0x0]                        @ 080bcebc 0870
    ldr r1, PTR_WIN0H_080bcef0               @ 080bcebe 0c49
    movs r0,#0xf0    @ 080bcec0 f020
    strh r0,[r1,#0x0]                        @ 080bcec2 0880
    adds r1,#0x4    @ 080bcec4 0431
    movs r0,#0xa0    @ 080bcec6 a020
    strh r0,[r1,#0x0]                        @ 080bcec8 0880
    adds r1,#0x4    @ 080bceca 0431
    movs r0,#0x1f    @ 080bcecc 1f20
    strh r0,[r1,#0x0]                        @ 080bcece 0880
    adds r1,#0x2    @ 080bced0 0231
    movs r0,#0x3f    @ 080bced2 3f20
    strh r0,[r1,#0x0]                        @ 080bced4 0880
    .hword 0x4643    @ 080bced6 4346
    cmp r3,#0x1                              @ 080bced8 012b
    bne LAB_080bcef4                         @ 080bceda 0bd1
    adds r1,#0x6    @ 080bcedc 0631
    movs r0,#0xaf    @ 080bcede af20
    b LAB_080bcef8                           @ 080bcee0 0ae0
    .zero  0x2
DAT_080bcee4:
    .word  gBannerState                   @ 080bcee4 c0fe0102
DAT_080bcee8:
    .word  0x02023130                     @ 080bcee8 30310202
DAT_080bceec:
    .word  0x00000215                     @ 080bceec 15020000
PTR_WIN0H_080bcef0:
    .word  WIN0H                          @ 080bcef0 40000004
LAB_080bcef4:
    ldr r1, PTR_BLDCNT_080bcf14              @ 080bcef4 0749
    movs r0,#0xef    @ 080bcef6 ef20
LAB_080bcef8:
    strh r0,[r1,#0x0]                        @ 080bcef8 0880
    ldr r1, PTR_BLDY_080bcf18                @ 080bcefa 0749
    movs r0,#0x10    @ 080bcefc 1020
    strh r0,[r1,#0x0]                        @ 080bcefe 0880
    movs r2,#0x80    @ 080bcf00 8022
    lsls r2,r2,#0x13    @ 080bcf02 d204
    ldrh r0,[r2,#0x0]                        @ 080bcf04 1088
    movs r4,#0x80    @ 080bcf06 8024
    lsls r4,r4,#0x6    @ 080bcf08 a401
    adds r1,r4,#0x0    @ 080bcf0a 211c
    orrs r0,r1    @ 080bcf0c 0843
    strh r0,[r2,#0x0]                        @ 080bcf0e 1080
    b LAB_080bcd6a                           @ 080bcf10 2be7
    .zero  0x2
PTR_BLDCNT_080bcf14:
    .word  BLDCNT                         @ 080bcf14 50000004
PTR_BLDY_080bcf18:
    .word  BLDY                           @ 080bcf18 54000004
switchD_080bcc8e__caseD_5:
    movs r4,#0x0    @ 080bcf1c 0024
    lsls r6,r5,#0x10    @ 080bcf1e 2e04
    adds r5,r7,#0x0    @ 080bcf20 3d1c
LAB_080bcf22:
    adds r0,r5,#0x0    @ 080bcf22 281c
    orrs r0,r6    @ 080bcf24 3043
    lsls r2,r4,#0x3    @ 080bcf26 e200
    movs r1,#0xc0    @ 080bcf28 c021
    lsls r1,r1,#0x2    @ 080bcf2a 8900
    adds r2,r2,r1    @ 080bcf2c 5218
    movs r3,#0x80    @ 080bcf2e 8023
    lsls r3,r3,#0x7    @ 080bcf30 db01
    adds r1,r3,#0x0    @ 080bcf32 191c
    orrs r2,r1    @ 080bcf34 0a43
    lsls r2,r2,#0x10    @ 080bcf36 1204
    lsrs r2,r2,#0x10    @ 080bcf38 120c
    movs r1,#0xc0    @ 080bcf3a c021
    bl write_oam_entry_from_packed_args      @ 080bcf3c 39f016f9
    adds r5,#0x40    @ 080bcf40 4035
    adds r4,#0x1    @ 080bcf42 0134
    cmp r4,#0x2                              @ 080bcf44 022c
    ble LAB_080bcf22                         @ 080bcf46 ecdd
    ldr r2, PTR_WIN0V_080bcfa0               @ 080bcf48 154a
    ldr r3, DAT_080bcfa4                     @ 080bcf4a 164b
    ldrh r4,[r3,#0x12]                       @ 080bcf4c 5c8a
    lsls r1,r4,#0x2    @ 080bcf4e a100
    adds r1,r1,r4    @ 080bcf50 0919
    movs r4,#0x60    @ 080bcf52 6024
    rsbs r4,r4,#0    @ 080bcf54 6442
    adds r0,r4,#0x0    @ 080bcf56 201c
    subs r0,r0,r1    @ 080bcf58 401a
    lsls r0,r0,#0x18    @ 080bcf5a 0006
    lsrs r0,r0,#0x18    @ 080bcf5c 000e
    lsls r1,r1,#0x18    @ 080bcf5e 0906
    lsrs r1,r1,#0x10    @ 080bcf60 090c
    orrs r0,r1    @ 080bcf62 0843
    strh r0,[r2,#0x0]                        @ 080bcf64 1080
    ldrh r0,[r3,#0x12]                       @ 080bcf66 588a
    adds r0,#0x1    @ 080bcf68 0130
    strh r0,[r3,#0x12]                       @ 080bcf6a 5882
    lsls r0,r0,#0x10    @ 080bcf6c 0004
    lsrs r0,r0,#0x10    @ 080bcf6e 000c
    cmp r0,#0x10                             @ 080bcf70 1028
    bhi LAB_080bcf76                         @ 080bcf72 00d8
    b LAB_080bcd6a                           @ 080bcf74 f9e6
LAB_080bcf76:
    ldrb r0,[r3,#0x11]                       @ 080bcf76 587c
    adds r0,#0x1    @ 080bcf78 0130
    strb r0,[r3,#0x11]                       @ 080bcf7a 5874
    movs r0,#0x0    @ 080bcf7c 0020
    strh r0,[r3,#0x12]                       @ 080bcf7e 5882
    movs r1,#0x80    @ 080bcf80 8021
    lsls r1,r1,#0x13    @ 080bcf82 c904
    movs r2,#0x80    @ 080bcf84 8022
    lsls r2,r2,#0x5    @ 080bcf86 5201
    adds r0,r2,#0x0    @ 080bcf88 101c
    strh r0,[r1,#0x0]                        @ 080bcf8a 0880
    .hword 0x4643    @ 080bcf8c 4346
    cmp r3,#0x1                              @ 080bcf8e 012b
    beq LAB_080bcf94                         @ 080bcf90 00d0
    b LAB_080bcd6a                           @ 080bcf92 eae6
LAB_080bcf94:
    movs r1,#0xa0    @ 080bcf94 a021
    lsls r1,r1,#0x13    @ 080bcf96 c904
    ldr r4, DAT_080bcfa8                     @ 080bcf98 034c
    adds r0,r4,#0x0    @ 080bcf9a 201c
    strh r0,[r1,#0x0]                        @ 080bcf9c 0880
    b LAB_080bcd6a                           @ 080bcf9e e4e6
PTR_WIN0V_080bcfa0:
    .word  WIN0V                          @ 080bcfa0 44000004
DAT_080bcfa4:
    .word  gBannerState                   @ 080bcfa4 c0fe0102
DAT_080bcfa8:
    .word  0x00007fff                     @ 080bcfa8 ff7f0000
switchD_080bcc8e__caseD_6:
    movs r4,#0x0    @ 080bcfac 0024
    lsls r6,r5,#0x10    @ 080bcfae 2e04
    adds r5,r7,#0x0    @ 080bcfb0 3d1c
LAB_080bcfb2:
    adds r0,r5,#0x0    @ 080bcfb2 281c
    orrs r0,r6    @ 080bcfb4 3043
    lsls r2,r4,#0x3    @ 080bcfb6 e200
    movs r1,#0xc0    @ 080bcfb8 c021
    lsls r1,r1,#0x2    @ 080bcfba 8900
    adds r2,r2,r1    @ 080bcfbc 5218
    movs r3,#0x80    @ 080bcfbe 8023
    lsls r3,r3,#0x7    @ 080bcfc0 db01
    adds r1,r3,#0x0    @ 080bcfc2 191c
    orrs r2,r1    @ 080bcfc4 0a43
    lsls r2,r2,#0x10    @ 080bcfc6 1204
    lsrs r2,r2,#0x10    @ 080bcfc8 120c
    movs r1,#0xc0    @ 080bcfca c021
    bl write_oam_entry_from_packed_args      @ 080bcfcc 39f0cef8
    adds r5,#0x40    @ 080bcfd0 4035
    adds r4,#0x1    @ 080bcfd2 0134
    cmp r4,#0x2                              @ 080bcfd4 022c
    ble LAB_080bcfb2                         @ 080bcfd6 ecdd
    ldr r1, DAT_080bcff8                     @ 080bcfd8 0749
    ldrh r0,[r1,#0x12]                       @ 080bcfda 488a
    adds r0,#0x1    @ 080bcfdc 0130
    strh r0,[r1,#0x12]                       @ 080bcfde 4882
    lsls r0,r0,#0x10    @ 080bcfe0 0004
    lsrs r0,r0,#0x10    @ 080bcfe2 000c
    cmp r0,#0x20                             @ 080bcfe4 2028
    bhi LAB_080bcfea                         @ 080bcfe6 00d8
    b LAB_080bcd6a                           @ 080bcfe8 bfe6
LAB_080bcfea:
    ldrb r0,[r1,#0x11]                       @ 080bcfea 487c
    adds r0,#0x1    @ 080bcfec 0130
    strb r0,[r1,#0x11]                       @ 080bcfee 4874
    movs r0,#0x0    @ 080bcff0 0020
    strh r0,[r1,#0x12]                       @ 080bcff2 4882
    b LAB_080bcd6a                           @ 080bcff4 b9e6
    .zero  0x2
DAT_080bcff8:
    .word  gBannerState                   @ 080bcff8 c0fe0102
switchD_080bcc8e__caseD_7:
    movs r4,#0x0    @ 080bcffc 0024
    lsls r6,r5,#0x10    @ 080bcffe 2e04
    movs r0,#0x80    @ 080bd000 8020
    lsls r0,r0,#0x1    @ 080bd002 4000
    .hword 0x4680    @ 080bd004 8046
    adds r5,r7,#0x0    @ 080bd006 3d1c
LAB_080bd008:
    adds r0,r5,#0x0    @ 080bd008 281c
    orrs r0,r6    @ 080bd00a 3043
    lsls r2,r4,#0x3    @ 080bd00c e200
    movs r1,#0xc0    @ 080bd00e c021
    lsls r1,r1,#0x2    @ 080bd010 8900
    adds r2,r2,r1    @ 080bd012 5218
    movs r3,#0x80    @ 080bd014 8023
    lsls r3,r3,#0x7    @ 080bd016 db01
    adds r1,r3,#0x0    @ 080bd018 191c
    orrs r2,r1    @ 080bd01a 0a43
    lsls r2,r2,#0x10    @ 080bd01c 1204
    lsrs r2,r2,#0x10    @ 080bd01e 120c
    .hword 0x4694    @ 080bd020 9446
    ldr r7, DAT_080bd074                     @ 080bd022 144f
    ldrh r1,[r7,#0x12]                       @ 080bd024 798a
    lsls r3,r1,#0x5    @ 080bd026 4b01
    .hword 0x4642    @ 080bd028 4246
    subs r3,r2,r3    @ 080bd02a d31a
    lsls r3,r3,#0x10    @ 080bd02c 1b04
    lsrs r3,r3,#0x10    @ 080bd02e 1b0c
    lsls r1,r1,#0x8    @ 080bd030 0902
    add r1,r8                                @ 080bd032 4144
    lsls r1,r1,#0x10    @ 080bd034 0904
    orrs r3,r1    @ 080bd036 0b43
    movs r1,#0xc0    @ 080bd038 c021
    .hword 0x4662    @ 080bd03a 6246
    bl write_pack_obj_attr_by_dir            @ 080bd03c 39f04efd
    adds r5,#0x40    @ 080bd040 4035
    adds r4,#0x1    @ 080bd042 0134
    cmp r4,#0x2                              @ 080bd044 022c
    ble LAB_080bd008                         @ 080bd046 dfdd
    ldrh r0,[r7,#0x12]                       @ 080bd048 788a
    adds r0,#0x1    @ 080bd04a 0130
    movs r2,#0x0    @ 080bd04c 0022
    strh r0,[r7,#0x12]                       @ 080bd04e 7882
    lsls r0,r0,#0x10    @ 080bd050 0004
    lsrs r0,r0,#0x10    @ 080bd052 000c
    cmp r0,#0x8                              @ 080bd054 0828
    bhi LAB_080bd05a                         @ 080bd056 00d8
    b LAB_080bcd6a                           @ 080bd058 87e6
LAB_080bd05a:
    ldrb r0,[r7,#0x11]                       @ 080bd05a 787c
    adds r0,#0x1    @ 080bd05c 0130
    strb r0,[r7,#0x11]                       @ 080bd05e 7874
    strh r2,[r7,#0x12]                       @ 080bd060 7a82
    ldr r1, PTR_BLDCNT_080bd078              @ 080bd062 0549
    movs r0,#0xff    @ 080bd064 ff20
    strh r0,[r1,#0x0]                        @ 080bd066 0880
    ldr r0, PTR_BLDY_080bd07c                @ 080bd068 0448
    strh r2,[r0,#0x0]                        @ 080bd06a 0280
    bl request_sound_engine_code10           @ 080bd06c 3cf068fd
    b LAB_080bcd6a                           @ 080bd070 7be6
    .zero  0x2
DAT_080bd074:
    .word  gBannerState                   @ 080bd074 c0fe0102
PTR_BLDCNT_080bd078:
    .word  BLDCNT                         @ 080bd078 50000004
PTR_BLDY_080bd07c:
    .word  BLDY                           @ 080bd07c 54000004
switchD_080bcc8e__caseD_8:
    movs r0,#0x1    @ 080bd080 0120
    bl start_blend_fadein_with_target        @ 080bd082 38f0ddfb
    cmp r0,#0x0                              @ 080bd086 0028
    bne LAB_080bd08c                         @ 080bd088 00d1
    b LAB_080bcd6a                           @ 080bd08a 6ee6
LAB_080bd08c:
    ldr r1, DAT_080bd098                     @ 080bd08c 0249
    ldrb r0,[r1,#0x11]                       @ 080bd08e 487c
    adds r0,#0x1    @ 080bd090 0130
    strb r0,[r1,#0x11]                       @ 080bd092 4874
    b LAB_080bcd6a                           @ 080bd094 69e6
    .zero  0x2
DAT_080bd098:
    .word  gBannerState                   @ 080bd098 c0fe0102
LAB_080bd09c:
    movs r0,#0x0    @ 080bd09c 0020
LAB_080bd09e:
    pop {r3}                                 @ 080bd09e 08bc
    .hword 0x4698    @ 080bd0a0 9846
    pop {r4,r5,r6,r7}                        @ 080bd0a2 f0bc
    pop {r1}                                 @ 080bd0a4 02bc
    bx r1                                    @ 080bd0a6 0847

@ banner/pack 场景主帧状态机 tick 分派器. 读取 gBannerState[+0x10] (byte, 主场景状态索引 [0..8]), 超出范围则跳转 switchD_080bd0c8__caseD_7 (默认处理). 在范围内则以 state*4 查找 9-entry 跳转表 (switchD_080bd0c8__switchdataD_080bd0d4, entry: 0x080bd0f8..0x080bd3ac), 通过 bx 跳入对应 case handler. 与 dispatch_banner_anim_tick_by_state (0x080bcc6c) 对称: 0x080bcc6c 读 gBannerState[+0x11] (sub-state), 本函数读 gBannerState[+0x10] (main-state). 两函数配合构成双层状态机. 入口: .hword 0x4647=mov r7,r8; movs r0,#0x18 -> r8=0x18; movs r5,#0x30 初始化参数常量. 唯一 caller: play_ui_effect (0x0801ef94) - 游戏顶层 UI 效果循环调用本函数推进每帧. case 0 (0x080bd0f8): 执行 copy_bytes_by_halfword 复制数据, 读取场景 type 字段 gPrng+0x3d0. Constants: gBannerState (0x0201fec0): banner 全局状态结构基址; gBannerState[+0x10]: 主场景状态索引 [0..8]; 0x18 / 0x30: case handler 初始参数常量 (r8 / r5); switchD_080bd0c8__switchdataD_080bd0d4: 9-entry 跳转表.
dispatch_banner_scene_tick_by_state:
    push {r4,r5,r6,r7,lr}                    @ 080bd0a8 f0b5
    .hword 0x4647    @ 080bd0aa 4746
    push {r7}                                @ 080bd0ac 80b4
    movs r0,#0x18    @ 080bd0ae 1820
    .hword 0x4680    @ 080bd0b0 8046
    movs r5,#0x30    @ 080bd0b2 3025
    ldr r0, DAT_080bd0cc                     @ 080bd0b4 0548
    ldrb r1,[r0,#0x10]                       @ 080bd0b6 017c
    adds r7,r0,#0x0    @ 080bd0b8 071c
    cmp r1,#0x8                              @ 080bd0ba 0829
    bls LAB_080bd0c0                         @ 080bd0bc 00d9
    b switchD_080bd0c8__caseD_7              @ 080bd0be 81e1
LAB_080bd0c0:
    lsls r0,r1,#0x2    @ 080bd0c0 8800
    ldr r1, DAT_080bd0d0                     @ 080bd0c2 0349
    adds r0,r0,r1    @ 080bd0c4 4018
    ldr r0,[r0,#0x0]                         @ 080bd0c6 0068
switchD_080bd0c8__switchD:
    .hword 0x4687    @ 080bd0c8 8746
    .zero  0x2
DAT_080bd0cc:
    .word  gBannerState                   @ 080bd0cc c0fe0102
DAT_080bd0d0:
    .word  0x080bd0d4                     @ 080bd0d0 d4d00b08
switchD_080bd0c8__switchdataD_080bd0d4:
    .word  0x080bd0f8                     @ 080bd0d4 f8d00b08
    .word  0x080bd16c                     @ 080bd0d8 6cd10b08
    .word  0x080bd1f8                     @ 080bd0dc f8d10b08
    .word  0x080bd254                     @ 080bd0e0 54d20b08
    .word  0x080bd2b8                     @ 080bd0e4 b8d20b08
    .word  0x080bd348                     @ 080bd0e8 48d30b08
    .word  0x080bd394                     @ 080bd0ec 94d30b08
    .word  0x080bd3c4                     @ 080bd0f0 c4d30b08
    .word  0x080bd3ac                     @ 080bd0f4 acd30b08
switchD_080bd0c8__caseD_0:
    ldr r1, DAT_080bd134                     @ 080bd0f8 0e49
    ldr r2, DAT_080bd138                     @ 080bd0fa 0f4a
    adds r1,r1,r2    @ 080bd0fc 8918
    movs r0,#0x1    @ 080bd0fe 0120
    ldrb r3,[r1,#0x0]                        @ 080bd100 0b78
    orrs r0,r3    @ 080bd102 1843
    strb r0,[r1,#0x0]                        @ 080bd104 0870
    ldr r0, DAT_080bd13c                     @ 080bd106 0d48
    ldr r1, DAT_080bd140                     @ 080bd108 0d49
    movs r2,#0x20    @ 080bd10a 2022
    bl copy_bytes_by_halfword                @ 080bd10c 37f0cafe
    ldr r0, DAT_080bd144                     @ 080bd110 0c48
    ldr r1, DAT_080bd148                     @ 080bd112 0d49
    adds r0,r0,r1    @ 080bd114 4018
    ldrb r0,[r0,#0x0]                        @ 080bd116 0078
    lsls r1,r0,#0x1d    @ 080bd118 4107
    lsrs r1,r1,#0x1d    @ 080bd11a 490f
    lsls r0,r1,#0x1    @ 080bd11c 4800
    adds r0,r0,r1    @ 080bd11e 4018
    lsls r1,r0,#0xb    @ 080bd120 c102
    ldr r0, PTR_gP1LifePoints_080bd14c       @ 080bd122 0a48
    movs r2,#0xe8    @ 080bd124 e822
    lsls r2,r2,#0x5    @ 080bd126 5201
    adds r0,r0,r2    @ 080bd128 8018
    ldr r0,[r0,#0x0]                         @ 080bd12a 0068
    cmp r0,#0x0                              @ 080bd12c 0028
    beq LAB_080bd154                         @ 080bd12e 11d0
    ldr r0, DAT_080bd150                     @ 080bd130 0748
    b LAB_080bd156                           @ 080bd132 10e0
DAT_080bd134:
    .word  0x02023130                     @ 080bd134 30310202
DAT_080bd138:
    .word  0x0000021e                     @ 080bd138 1e020000
DAT_080bd13c:
    .word  0x05000260                     @ 080bd13c 60020005
DAT_080bd140:
    .word  0x098d20a4                     @ 080bd140 a4208d09
DAT_080bd144:
    .word  0x02000000                     @ 080bd144 00000002
DAT_080bd148:
    .word  0x00006c2c                     @ 080bd148 2c6c0000
PTR_gP1LifePoints_080bd14c:
    .word  gP1LifePoints                  @ 080bd14c e0c40102
DAT_080bd150:
    .word  0x098e40e4                     @ 080bd150 e4408e09
LAB_080bd154:
    ldr r0, DAT_080bd164                     @ 080bd154 0348
LAB_080bd156:
    adds r1,r1,r0    @ 080bd156 0918
    ldr r0, DAT_080bd168                     @ 080bd158 0348
    movs r2,#0x18    @ 080bd15a 1822
    movs r3,#0x8    @ 080bd15c 0823
    bl tile_2d_row_copy                      @ 080bd15e 3af0b9f9
    b LAB_080bd3b4                           @ 080bd162 27e1
DAT_080bd164:
    .word  0x098d20c4                     @ 080bd164 c4208d09
DAT_080bd168:
    .word  0x06014000                     @ 080bd168 00400106
switchD_080bd0c8__caseD_1:
    ldrb r0,[r7,#0x11]                       @ 080bd16c 787c
    movs r1,#0x8    @ 080bd16e 0821
    subs r1,r1,r0    @ 080bd170 091a
    lsls r1,r1,#0x14    @ 080bd172 0905
    lsrs r1,r1,#0x10    @ 080bd174 090c
    ldr r6, DAT_080bd1ec                     @ 080bd176 1d4e
    lsls r0,r0,#0x1    @ 080bd178 4000
    adds r0,r0,r6    @ 080bd17a 8019
    .hword 0x4643    @ 080bd17c 4346
    ldrh r0,[r0,#0x0]                        @ 080bd17e 0088
    subs r0,r3,r0    @ 080bd180 181a
    movs r2,#0x80    @ 080bd182 8022
    lsls r2,r2,#0x2    @ 080bd184 9200
    adds r0,r0,r2    @ 080bd186 8018
    lsls r5,r5,#0x10    @ 080bd188 2d04
    orrs r0,r5    @ 080bd18a 2843
    movs r2,#0xc8    @ 080bd18c c822
    lsls r2,r2,#0x6    @ 080bd18e 9201
    movs r4,#0x80    @ 080bd190 8024
    lsls r4,r4,#0x1    @ 080bd192 6400
    subs r4,r4,r1    @ 080bd194 641a
    lsls r4,r4,#0x10    @ 080bd196 2404
    movs r1,#0xc0    @ 080bd198 c021
    adds r3,r4,#0x0    @ 080bd19a 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd19c 39f0a6fb
    .hword 0x4640    @ 080bd1a0 4046
    adds r0,#0x40    @ 080bd1a2 4030
    orrs r0,r5    @ 080bd1a4 2843
    ldr r2, DAT_080bd1f0                     @ 080bd1a6 124a
    movs r1,#0xc0    @ 080bd1a8 c021
    adds r3,r4,#0x0    @ 080bd1aa 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd1ac 39f09efb
    ldrb r3,[r7,#0x11]                       @ 080bd1b0 7b7c
    lsls r0,r3,#0x1    @ 080bd1b2 5800
    adds r0,r0,r6    @ 080bd1b4 8019
    ldrh r0,[r0,#0x0]                        @ 080bd1b6 0088
    adds r0,#0x80    @ 080bd1b8 8030
    add r0,r8                                @ 080bd1ba 4044
    orrs r0,r5    @ 080bd1bc 2843
    ldr r2, DAT_080bd1f4                     @ 080bd1be 0d4a
    movs r1,#0xc0    @ 080bd1c0 c021
    adds r3,r4,#0x0    @ 080bd1c2 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd1c4 39f092fb
    ldrb r0,[r7,#0x11]                       @ 080bd1c8 787c
    adds r0,#0x1    @ 080bd1ca 0130
    strb r0,[r7,#0x11]                       @ 080bd1cc 7874
    lsls r0,r0,#0x18    @ 080bd1ce 0006
    lsrs r0,r0,#0x18    @ 080bd1d0 000e
    cmp r0,#0x7                              @ 080bd1d2 0728
    bhi LAB_080bd1d8                         @ 080bd1d4 00d8
    b LAB_080bd324                           @ 080bd1d6 a5e0
LAB_080bd1d8:
    ldrb r0,[r7,#0x10]                       @ 080bd1d8 387c
    adds r0,#0x1    @ 080bd1da 0130
    strb r0,[r7,#0x10]                       @ 080bd1dc 3874
    movs r0,#0x0    @ 080bd1de 0020
    strb r0,[r7,#0x11]                       @ 080bd1e0 7874
    movs r0,#0x22    @ 080bd1e2 2220
    bl sync_state_and_init_sprite            @ 080bd1e4 3cf066fc
    b LAB_080bd324                           @ 080bd1e8 9ce0
    .zero  0x2
DAT_080bd1ec:
    .word  0x09e491c0                     @ 080bd1ec c091e409
DAT_080bd1f0:
    .word  0x00003208                     @ 080bd1f0 08320000
DAT_080bd1f4:
    .word  0x00003210                     @ 080bd1f4 10320000
switchD_080bd0c8__caseD_2:
    ldr r0, DAT_080bd24c                     @ 080bd1f8 1448
    ldrb r2,[r7,#0x11]                       @ 080bd1fa 7a7c
    movs r1,#0x3    @ 080bd1fc 0321
    bl blend_palette_entry_toward_target     @ 080bd1fe fff7effa
    movs r4,#0x0    @ 080bd202 0024
    lsls r5,r5,#0x10    @ 080bd204 2d04
    .hword 0x4646    @ 080bd206 4646
LAB_080bd208:
    adds r0,r6,#0x0    @ 080bd208 301c
    orrs r0,r5    @ 080bd20a 2843
    lsls r2,r4,#0x3    @ 080bd20c e200
    movs r1,#0x80    @ 080bd20e 8021
    lsls r1,r1,#0x2    @ 080bd210 8900
    adds r2,r2,r1    @ 080bd212 5218
    movs r3,#0xc0    @ 080bd214 c023
    lsls r3,r3,#0x6    @ 080bd216 9b01
    adds r1,r3,#0x0    @ 080bd218 191c
    orrs r2,r1    @ 080bd21a 0a43
    lsls r2,r2,#0x10    @ 080bd21c 1204
    lsrs r2,r2,#0x10    @ 080bd21e 120c
    movs r1,#0xc0    @ 080bd220 c021
    bl write_oam_entry_from_packed_args      @ 080bd222 38f0a3ff
    adds r6,#0x40    @ 080bd226 4036
    adds r4,#0x1    @ 080bd228 0134
    cmp r4,#0x2                              @ 080bd22a 022c
    ble LAB_080bd208                         @ 080bd22c ecdd
    ldr r2, DAT_080bd250                     @ 080bd22e 084a
    ldrb r0,[r2,#0x11]                       @ 080bd230 507c
    adds r1,r0,#0x1    @ 080bd232 411c
    strb r1,[r2,#0x11]                       @ 080bd234 5174
    lsls r0,r0,#0x18    @ 080bd236 0006
    lsrs r0,r0,#0x18    @ 080bd238 000e
    cmp r0,#0xf                              @ 080bd23a 0f28
    bls LAB_080bd324                         @ 080bd23c 72d9
    ldrb r0,[r2,#0x10]                       @ 080bd23e 107c
    adds r0,#0x1    @ 080bd240 0130
    movs r1,#0x0    @ 080bd242 0021
    strb r0,[r2,#0x10]                       @ 080bd244 1074
    strb r1,[r2,#0x11]                       @ 080bd246 5174
    b LAB_080bd324                           @ 080bd248 6ce0
    .zero  0x2
DAT_080bd24c:
    .word  0x098d20a4                     @ 080bd24c a4208d09
DAT_080bd250:
    .word  gBannerState                   @ 080bd250 c0fe0102
switchD_080bd0c8__caseD_3:
    ldr r0, DAT_080bd2b0                     @ 080bd254 1648
    movs r2,#0x10    @ 080bd256 1022
    ldrb r7,[r7,#0x11]                       @ 080bd258 7f7c
    subs r2,r2,r7    @ 080bd25a d21b
    lsls r2,r2,#0x10    @ 080bd25c 1204
    lsrs r2,r2,#0x10    @ 080bd25e 120c
    movs r1,#0x3    @ 080bd260 0321
    bl blend_palette_entry_toward_target     @ 080bd262 fff7bdfa
    movs r4,#0x0    @ 080bd266 0024
    lsls r5,r5,#0x10    @ 080bd268 2d04
    .hword 0x4646    @ 080bd26a 4646
LAB_080bd26c:
    adds r0,r6,#0x0    @ 080bd26c 301c
    orrs r0,r5    @ 080bd26e 2843
    lsls r2,r4,#0x3    @ 080bd270 e200
    movs r1,#0x80    @ 080bd272 8021
    lsls r1,r1,#0x2    @ 080bd274 8900
    adds r2,r2,r1    @ 080bd276 5218
    movs r3,#0xc0    @ 080bd278 c023
    lsls r3,r3,#0x6    @ 080bd27a 9b01
    adds r1,r3,#0x0    @ 080bd27c 191c
    orrs r2,r1    @ 080bd27e 0a43
    lsls r2,r2,#0x10    @ 080bd280 1204
    lsrs r2,r2,#0x10    @ 080bd282 120c
    movs r1,#0xc0    @ 080bd284 c021
    bl write_oam_entry_from_packed_args      @ 080bd286 38f071ff
    adds r6,#0x40    @ 080bd28a 4036
    adds r4,#0x1    @ 080bd28c 0134
    cmp r4,#0x2                              @ 080bd28e 022c
    ble LAB_080bd26c                         @ 080bd290 ecdd
    ldr r2, DAT_080bd2b4                     @ 080bd292 084a
    ldrb r0,[r2,#0x11]                       @ 080bd294 507c
    adds r1,r0,#0x1    @ 080bd296 411c
    strb r1,[r2,#0x11]                       @ 080bd298 5174
    lsls r0,r0,#0x18    @ 080bd29a 0006
    lsrs r0,r0,#0x18    @ 080bd29c 000e
    cmp r0,#0xf                              @ 080bd29e 0f28
    bls LAB_080bd324                         @ 080bd2a0 40d9
    ldrb r0,[r2,#0x10]                       @ 080bd2a2 107c
    adds r0,#0x1    @ 080bd2a4 0130
    movs r1,#0x0    @ 080bd2a6 0021
    strb r0,[r2,#0x10]                       @ 080bd2a8 1074
    strb r1,[r2,#0x11]                       @ 080bd2aa 5174
    b LAB_080bd324                           @ 080bd2ac 3ae0
    .zero  0x2
DAT_080bd2b0:
    .word  0x098d20a4                     @ 080bd2b0 a4208d09
DAT_080bd2b4:
    .word  gBannerState                   @ 080bd2b4 c0fe0102
switchD_080bd0c8__caseD_4:
    movs r4,#0x0    @ 080bd2b8 0024
    lsls r5,r5,#0x10    @ 080bd2ba 2d04
    .hword 0x4646    @ 080bd2bc 4646
LAB_080bd2be:
    adds r0,r6,#0x0    @ 080bd2be 301c
    orrs r0,r5    @ 080bd2c0 2843
    lsls r2,r4,#0x3    @ 080bd2c2 e200
    movs r1,#0x80    @ 080bd2c4 8021
    lsls r1,r1,#0x2    @ 080bd2c6 8900
    adds r2,r2,r1    @ 080bd2c8 5218
    movs r3,#0xc0    @ 080bd2ca c023
    lsls r3,r3,#0x6    @ 080bd2cc 9b01
    adds r1,r3,#0x0    @ 080bd2ce 191c
    orrs r2,r1    @ 080bd2d0 0a43
    lsls r2,r2,#0x10    @ 080bd2d2 1204
    lsrs r2,r2,#0x10    @ 080bd2d4 120c
    movs r1,#0xc0    @ 080bd2d6 c021
    bl write_oam_entry_from_packed_args      @ 080bd2d8 38f048ff
    adds r6,#0x40    @ 080bd2dc 4036
    adds r4,#0x1    @ 080bd2de 0134
    cmp r4,#0x2                              @ 080bd2e0 022c
    ble LAB_080bd2be                         @ 080bd2e2 ecdd
    ldr r4, DAT_080bd328                     @ 080bd2e4 104c
    ldrb r0,[r4,#0x11]                       @ 080bd2e6 607c
    adds r1,r0,#0x1    @ 080bd2e8 411c
    strb r1,[r4,#0x11]                       @ 080bd2ea 6174
    lsls r0,r0,#0x18    @ 080bd2ec 0006
    lsrs r0,r0,#0x18    @ 080bd2ee 000e
    cmp r0,#0x3f                             @ 080bd2f0 3f28
    bls LAB_080bd324                         @ 080bd2f2 17d9
    bl disable_blend_and_clear_step          @ 080bd2f4 38f06ef9
    ldr r1, PTR_gPrng_080bd32c               @ 080bd2f8 0c49
    ldr r0, DAT_080bd330                     @ 080bd2fa 0d48
    adds r1,r1,r0    @ 080bd2fc 0918
    movs r0,#0x1    @ 080bd2fe 0120
    ldrb r1,[r1,#0x0]                        @ 080bd300 0978
    ands r0,r1    @ 080bd302 0840
    cmp r0,#0x0                              @ 080bd304 0028
    beq LAB_080bd334                         @ 080bd306 15d0
    movs r0,#0x1    @ 080bd308 0120
    bl compute_duel_zone_dir_for_player      @ 080bd30a 0ff0c3f9
    cmp r0,#0x2                              @ 080bd30e 0228
    beq LAB_080bd31a                         @ 080bd310 03d0
    cmp r0,#0x2                              @ 080bd312 0228
    bgt LAB_080bd334                         @ 080bd314 0edc
    cmp r0,#0x1                              @ 080bd316 0128
    bne LAB_080bd334                         @ 080bd318 0cd1
LAB_080bd31a:
    str r0,[r4,#0x8]                         @ 080bd31a a060
    movs r1,#0x0    @ 080bd31c 0021
    movs r0,#0x8    @ 080bd31e 0820
    strb r0,[r4,#0x10]                       @ 080bd320 2074
    strb r1,[r4,#0x11]                       @ 080bd322 6174
LAB_080bd324:
    movs r0,#0x1    @ 080bd324 0120
    b LAB_080bd3e0                           @ 080bd326 5be0
DAT_080bd328:
    .word  gBannerState                   @ 080bd328 c0fe0102
PTR_gPrng_080bd32c:
    .word  gPrng                          @ 080bd32c 40000003
DAT_080bd330:
    .word  0x0000023f                     @ 080bd330 3f020000
LAB_080bd334:
    bl request_sound_engine_code10           @ 080bd334 3cf004fc
    ldr r1, DAT_080bd344                     @ 080bd338 0249
    ldrb r0,[r1,#0x10]                       @ 080bd33a 087c
    adds r0,#0x1    @ 080bd33c 0130
    strb r0,[r1,#0x10]                       @ 080bd33e 0874
    b LAB_080bd324                           @ 080bd340 f0e7
    .zero  0x2
DAT_080bd344:
    .word  gBannerState                   @ 080bd344 c0fe0102
switchD_080bd0c8__caseD_5:
    movs r4,#0x0    @ 080bd348 0024
    lsls r5,r5,#0x10    @ 080bd34a 2d04
    .hword 0x4646    @ 080bd34c 4646
LAB_080bd34e:
    adds r0,r6,#0x0    @ 080bd34e 301c
    orrs r0,r5    @ 080bd350 2843
    lsls r2,r4,#0x3    @ 080bd352 e200
    movs r1,#0x80    @ 080bd354 8021
    lsls r1,r1,#0x2    @ 080bd356 8900
    adds r2,r2,r1    @ 080bd358 5218
    movs r3,#0xc0    @ 080bd35a c023
    lsls r3,r3,#0x6    @ 080bd35c 9b01
    adds r1,r3,#0x0    @ 080bd35e 191c
    orrs r2,r1    @ 080bd360 0a43
    lsls r2,r2,#0x10    @ 080bd362 1204
    lsrs r2,r2,#0x10    @ 080bd364 120c
    movs r1,#0xc0    @ 080bd366 c021
    bl write_oam_entry_from_packed_args      @ 080bd368 38f000ff
    adds r6,#0x40    @ 080bd36c 4036
    adds r4,#0x1    @ 080bd36e 0134
    cmp r4,#0x2                              @ 080bd370 022c
    ble LAB_080bd34e                         @ 080bd372 ecdd
    movs r0,#0x2    @ 080bd374 0220
    bl start_blend_fade_with_evy             @ 080bd376 38f0d7fa
    cmp r0,#0x0                              @ 080bd37a 0028
    beq LAB_080bd324                         @ 080bd37c d2d0
    movs r1,#0x80    @ 080bd37e 8021
    lsls r1,r1,#0x13    @ 080bd380 c904
    movs r0,#0x0    @ 080bd382 0020
    strh r0,[r1,#0x0]                        @ 080bd384 0880
    ldr r1, DAT_080bd390                     @ 080bd386 0249
    ldrb r0,[r1,#0x10]                       @ 080bd388 087c
    adds r0,#0x1    @ 080bd38a 0130
    strb r0,[r1,#0x10]                       @ 080bd38c 0874
    b LAB_080bd324                           @ 080bd38e c9e7
DAT_080bd390:
    .word  gBannerState                   @ 080bd390 c0fe0102
switchD_080bd0c8__caseD_6:
    movs r0,#0x2    @ 080bd394 0220
    bl advance_blend_evy_step                @ 080bd396 38f003fb
    cmp r0,#0x0                              @ 080bd39a 0028
    beq LAB_080bd324                         @ 080bd39c c2d0
    ldr r1, DAT_080bd3a8                     @ 080bd39e 0249
    ldrb r0,[r1,#0x10]                       @ 080bd3a0 087c
    adds r0,#0x1    @ 080bd3a2 0130
    strb r0,[r1,#0x10]                       @ 080bd3a4 0874
    b LAB_080bd324                           @ 080bd3a6 bde7
DAT_080bd3a8:
    .word  gBannerState                   @ 080bd3a8 c0fe0102
switchD_080bd0c8__caseD_8:
    bl dispatch_banner_anim_tick_by_state    @ 080bd3ac fff75efc
    cmp r0,#0x0                              @ 080bd3b0 0028
    bne LAB_080bd324                         @ 080bd3b2 b7d1
LAB_080bd3b4:
    ldr r1, DAT_080bd3c0                     @ 080bd3b4 0249
    ldrb r0,[r1,#0x10]                       @ 080bd3b6 087c
    adds r0,#0x1    @ 080bd3b8 0130
    strb r0,[r1,#0x10]                       @ 080bd3ba 0874
    b LAB_080bd324                           @ 080bd3bc b2e7
    .zero  0x2
DAT_080bd3c0:
    .word  gBannerState                   @ 080bd3c0 c0fe0102
switchD_080bd0c8__caseD_7:
    movs r0,#0x2    @ 080bd3c4 0220
    rsbs r0,r0,#0    @ 080bd3c6 4042
    ldrb r1,[r7,#0x0]                        @ 080bd3c8 3978
    ands r0,r1    @ 080bd3ca 0840
    strb r0,[r7,#0x0]                        @ 080bd3cc 3870
    ldr r1, DAT_080bd3ec                     @ 080bd3ce 0749
    ldr r2, DAT_080bd3f0                     @ 080bd3d0 074a
    adds r1,r1,r2    @ 080bd3d2 8918
    movs r0,#0x5    @ 080bd3d4 0520
    rsbs r0,r0,#0    @ 080bd3d6 4042
    ldrb r3,[r1,#0x0]                        @ 080bd3d8 0b78
    ands r0,r3    @ 080bd3da 1840
    strb r0,[r1,#0x0]                        @ 080bd3dc 0870
    movs r0,#0x0    @ 080bd3de 0020
LAB_080bd3e0:
    pop {r3}                                 @ 080bd3e0 08bc
    .hword 0x4698    @ 080bd3e2 9846
    pop {r4,r5,r6,r7}                        @ 080bd3e4 f0bc
    pop {r1}                                 @ 080bd3e6 02bc
    bx r1                                    @ 080bd3e8 0847
    .zero  0x2
DAT_080bd3ec:
    .word  0x02023130                     @ 080bd3ec 30310202
DAT_080bd3f0:
    .word  0x00000215                     @ 080bd3f0 15020000

@ 由 play_ui_effect (0x0801ef94) 调用. 读取 gBannerState (0x0201feC0, 偏移 +0x10 字节) 作为 switch 索引 [0..8], 共 9 个 case (case 4..7 合并为同一分支). 每个 case 执行对应帧阶段操作: case 0 设置 VRAM/palette 标志并拷贝调色板数据, 按 LP 状态选择 tile 源; case 1 更新 banner 贴图行偏移并调 tile_2d_row_copy; 后续 case 逐步完成 banner 动画帧推进. 函数通过 high-register callee-save (.hword 0x4647=mov r7,r0; .hword 0x4680=mov r8,r0) 保存 gBannerState 指针和输入参数供 switch 各分支复用. Constants: gBannerState=0x0201feC0, VRAM_BG_BASE=0x06014000, PALETTE_SRC_0=0x05000260, ROM_PALETTE_A=0x098db0c4, ROM_PALETTE_B=0x098ed0e4.
tick_banner_display_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 080bd3f4 f0b5
    .hword 0x4647    @ 080bd3f6 4746
    push {r7}                                @ 080bd3f8 80b4
    movs r0,#0x18    @ 080bd3fa 1820
    .hword 0x4680    @ 080bd3fc 8046
    movs r5,#0x30    @ 080bd3fe 3025
    ldr r0, DAT_080bd418                     @ 080bd400 0548
    ldrb r1,[r0,#0x10]                       @ 080bd402 017c
    adds r7,r0,#0x0    @ 080bd404 071c
    cmp r1,#0x8                              @ 080bd406 0829
    bls LAB_080bd40c                         @ 080bd408 00d9
    b switchD_080bd414__caseD_4              @ 080bd40a 11e1
LAB_080bd40c:
    lsls r0,r1,#0x2    @ 080bd40c 8800
    ldr r1, DAT_080bd41c                     @ 080bd40e 0349
    adds r0,r0,r1    @ 080bd410 4018
    ldr r0,[r0,#0x0]                         @ 080bd412 0068
switchD_080bd414__switchD:
    .hword 0x4687    @ 080bd414 8746
    .zero  0x2
DAT_080bd418:
    .word  gBannerState                   @ 080bd418 c0fe0102
DAT_080bd41c:
    .word  0x080bd420                     @ 080bd41c 20d40b08
switchD_080bd414__switchdataD_080bd420:
    .word  0x080bd444                     @ 080bd420 44d40b08
    .word  0x080bd4b8                     @ 080bd424 b8d40b08
    .word  0x080bd53c                     @ 080bd428 3cd50b08
    .word  0x080bd5c8                     @ 080bd42c c8d50b08
    .word  0x080bd630                     @ 080bd430 30d60b08
    .word  0x080bd630                     @ 080bd434 30d60b08
    .word  0x080bd630                     @ 080bd438 30d60b08
    .word  0x080bd630                     @ 080bd43c 30d60b08
    .word  0x080bd618                     @ 080bd440 18d60b08
switchD_080bd414__caseD_0:
    ldr r1, DAT_080bd480                     @ 080bd444 0e49
    ldr r2, DAT_080bd484                     @ 080bd446 0f4a
    adds r1,r1,r2    @ 080bd448 8918
    movs r0,#0x1    @ 080bd44a 0120
    ldrb r3,[r1,#0x0]                        @ 080bd44c 0b78
    orrs r0,r3    @ 080bd44e 1843
    strb r0,[r1,#0x0]                        @ 080bd450 0870
    ldr r0, DAT_080bd488                     @ 080bd452 0d48
    ldr r1, DAT_080bd48c                     @ 080bd454 0d49
    movs r2,#0x20    @ 080bd456 2022
    bl copy_bytes_by_halfword                @ 080bd458 37f024fd
    ldr r0, DAT_080bd490                     @ 080bd45c 0c48
    ldr r1, DAT_080bd494                     @ 080bd45e 0d49
    adds r0,r0,r1    @ 080bd460 4018
    ldrb r0,[r0,#0x0]                        @ 080bd462 0078
    lsls r1,r0,#0x1d    @ 080bd464 4107
    lsrs r1,r1,#0x1d    @ 080bd466 490f
    lsls r0,r1,#0x1    @ 080bd468 4800
    adds r0,r0,r1    @ 080bd46a 4018
    lsls r1,r0,#0xb    @ 080bd46c c102
    ldr r0, PTR_gP1LifePoints_080bd498       @ 080bd46e 0a48
    movs r2,#0xe8    @ 080bd470 e822
    lsls r2,r2,#0x5    @ 080bd472 5201
    adds r0,r0,r2    @ 080bd474 8018
    ldr r0,[r0,#0x0]                         @ 080bd476 0068
    cmp r0,#0x0                              @ 080bd478 0028
    beq LAB_080bd4a0                         @ 080bd47a 11d0
    ldr r0, DAT_080bd49c                     @ 080bd47c 0748
    b LAB_080bd4a2                           @ 080bd47e 10e0
DAT_080bd480:
    .word  0x02023130                     @ 080bd480 30310202
DAT_080bd484:
    .word  0x0000021e                     @ 080bd484 1e020000
DAT_080bd488:
    .word  0x05000260                     @ 080bd488 60020005
DAT_080bd48c:
    .word  0x098db0c4                     @ 080bd48c c4b08d09
DAT_080bd490:
    .word  0x02000000                     @ 080bd490 00000002
DAT_080bd494:
    .word  0x00006c2c                     @ 080bd494 2c6c0000
PTR_gP1LifePoints_080bd498:
    .word  gP1LifePoints                  @ 080bd498 e0c40102
DAT_080bd49c:
    .word  0x098ed0e4                     @ 080bd49c e4d08e09
LAB_080bd4a0:
    ldr r0, DAT_080bd4b0                     @ 080bd4a0 0348
LAB_080bd4a2:
    adds r1,r1,r0    @ 080bd4a2 0918
    ldr r0, DAT_080bd4b4                     @ 080bd4a4 0348
    movs r2,#0x18    @ 080bd4a6 1822
    movs r3,#0x8    @ 080bd4a8 0823
    bl tile_2d_row_copy                      @ 080bd4aa 3af013f8
    b LAB_080bd620                           @ 080bd4ae b7e0
DAT_080bd4b0:
    .word  0x098db0e4                     @ 080bd4b0 e4b08d09
DAT_080bd4b4:
    .word  0x06014000                     @ 080bd4b4 00400106
switchD_080bd414__caseD_1:
    ldrb r0,[r7,#0x11]                       @ 080bd4b8 787c
    movs r4,#0x10    @ 080bd4ba 1024
    subs r4,r4,r0    @ 080bd4bc 241a
    lsls r4,r4,#0x14    @ 080bd4be 2405
    ldr r6, DAT_080bd530                     @ 080bd4c0 1b4e
    lsls r0,r0,#0x1    @ 080bd4c2 4000
    adds r0,r0,r6    @ 080bd4c4 8019
    ldrh r0,[r0,#0x0]                        @ 080bd4c6 0088
    add r0,r8                                @ 080bd4c8 4044
    movs r3,#0x80    @ 080bd4ca 8023
    lsls r3,r3,#0x2    @ 080bd4cc 9b00
    adds r0,r0,r3    @ 080bd4ce c018
    lsls r5,r5,#0x10    @ 080bd4d0 2d04
    orrs r0,r5    @ 080bd4d2 2843
    movs r2,#0xc8    @ 080bd4d4 c822
    lsls r2,r2,#0x6    @ 080bd4d6 9201
    movs r1,#0x80    @ 080bd4d8 8021
    lsls r1,r1,#0x11    @ 080bd4da 4904
    adds r4,r4,r1    @ 080bd4dc 6418
    movs r1,#0xc0    @ 080bd4de c021
    adds r3,r4,#0x0    @ 080bd4e0 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd4e2 39f003fa
    .hword 0x4640    @ 080bd4e6 4046
    adds r0,#0x40    @ 080bd4e8 4030
    orrs r0,r5    @ 080bd4ea 2843
    ldr r2, DAT_080bd534                     @ 080bd4ec 114a
    movs r1,#0xc0    @ 080bd4ee c021
    adds r3,r4,#0x0    @ 080bd4f0 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd4f2 39f0fbf9
    ldrb r2,[r7,#0x11]                       @ 080bd4f6 7a7c
    lsls r0,r2,#0x1    @ 080bd4f8 5000
    adds r0,r0,r6    @ 080bd4fa 8019
    ldrh r0,[r0,#0x0]                        @ 080bd4fc 0088
    subs r0,#0x80    @ 080bd4fe 8038
    .hword 0x4643    @ 080bd500 4346
    subs r0,r3,r0    @ 080bd502 181a
    orrs r0,r5    @ 080bd504 2843
    ldr r2, DAT_080bd538                     @ 080bd506 0c4a
    movs r1,#0xc0    @ 080bd508 c021
    adds r3,r4,#0x0    @ 080bd50a 231c
    bl write_pack_obj_attr_by_dir_split      @ 080bd50c 39f0eef9
    ldrb r0,[r7,#0x11]                       @ 080bd510 787c
    adds r0,#0x1    @ 080bd512 0130
    strb r0,[r7,#0x11]                       @ 080bd514 7874
    lsls r0,r0,#0x18    @ 080bd516 0006
    lsrs r0,r0,#0x18    @ 080bd518 000e
    cmp r0,#0xf                              @ 080bd51a 0f28
    bls LAB_080bd5a8                         @ 080bd51c 44d9
    ldrb r0,[r7,#0x10]                       @ 080bd51e 387c
    adds r0,#0x1    @ 080bd520 0130
    strb r0,[r7,#0x10]                       @ 080bd522 3874
    movs r0,#0x0    @ 080bd524 0020
    strb r0,[r7,#0x11]                       @ 080bd526 7874
    movs r0,#0x23    @ 080bd528 2320
    bl sync_state_and_init_sprite            @ 080bd52a 3cf0c3fa
    b LAB_080bd5a8                           @ 080bd52e 3be0
DAT_080bd530:
    .word  0x09e491d0                     @ 080bd530 d091e409
DAT_080bd534:
    .word  0x00003208                     @ 080bd534 08320000
DAT_080bd538:
    .word  0x00003210                     @ 080bd538 10320000
switchD_080bd414__caseD_2:
    movs r4,#0x0    @ 080bd53c 0024
    lsls r5,r5,#0x10    @ 080bd53e 2d04
    .hword 0x4646    @ 080bd540 4646
LAB_080bd542:
    adds r0,r6,#0x0    @ 080bd542 301c
    orrs r0,r5    @ 080bd544 2843
    lsls r2,r4,#0x3    @ 080bd546 e200
    movs r1,#0x80    @ 080bd548 8021
    lsls r1,r1,#0x2    @ 080bd54a 8900
    adds r2,r2,r1    @ 080bd54c 5218
    movs r3,#0xc0    @ 080bd54e c023
    lsls r3,r3,#0x6    @ 080bd550 9b01
    adds r1,r3,#0x0    @ 080bd552 191c
    orrs r2,r1    @ 080bd554 0a43
    lsls r2,r2,#0x10    @ 080bd556 1204
    lsrs r2,r2,#0x10    @ 080bd558 120c
    movs r1,#0xc0    @ 080bd55a c021
    bl write_oam_entry_from_packed_args      @ 080bd55c 38f006fe
    adds r6,#0x40    @ 080bd560 4036
    adds r4,#0x1    @ 080bd562 0134
    cmp r4,#0x2                              @ 080bd564 022c
    ble LAB_080bd542                         @ 080bd566 ecdd
    ldr r4, DAT_080bd5ac                     @ 080bd568 104c
    ldrb r0,[r4,#0x11]                       @ 080bd56a 607c
    adds r1,r0,#0x1    @ 080bd56c 411c
    strb r1,[r4,#0x11]                       @ 080bd56e 6174
    lsls r0,r0,#0x18    @ 080bd570 0006
    lsrs r0,r0,#0x18    @ 080bd572 000e
    cmp r0,#0x57                             @ 080bd574 5728
    bls LAB_080bd5a8                         @ 080bd576 17d9
    bl disable_blend_and_clear_step          @ 080bd578 38f02cf8
    ldr r1, PTR_gPrng_080bd5b0               @ 080bd57c 0c49
    ldr r0, DAT_080bd5b4                     @ 080bd57e 0d48
    adds r1,r1,r0    @ 080bd580 0918
    movs r0,#0x1    @ 080bd582 0120
    ldrb r1,[r1,#0x0]                        @ 080bd584 0978
    ands r0,r1    @ 080bd586 0840
    cmp r0,#0x0                              @ 080bd588 0028
    beq LAB_080bd5b8                         @ 080bd58a 15d0
    movs r0,#0x2    @ 080bd58c 0220
    bl compute_duel_zone_dir_for_player      @ 080bd58e 0ff081f8
    cmp r0,#0x2                              @ 080bd592 0228
    beq LAB_080bd59e                         @ 080bd594 03d0
    cmp r0,#0x2                              @ 080bd596 0228
    bgt LAB_080bd5b8                         @ 080bd598 0edc
    cmp r0,#0x1                              @ 080bd59a 0128
    bne LAB_080bd5b8                         @ 080bd59c 0cd1
LAB_080bd59e:
    str r0,[r4,#0x8]                         @ 080bd59e a060
    movs r1,#0x0    @ 080bd5a0 0021
    movs r0,#0x8    @ 080bd5a2 0820
    strb r0,[r4,#0x10]                       @ 080bd5a4 2074
    strb r1,[r4,#0x11]                       @ 080bd5a6 6174
LAB_080bd5a8:
    movs r0,#0x1    @ 080bd5a8 0120
    b LAB_080bd64c                           @ 080bd5aa 4fe0
DAT_080bd5ac:
    .word  gBannerState                   @ 080bd5ac c0fe0102
PTR_gPrng_080bd5b0:
    .word  gPrng                          @ 080bd5b0 40000003
DAT_080bd5b4:
    .word  0x0000023f                     @ 080bd5b4 3f020000
LAB_080bd5b8:
    ldr r1, DAT_080bd5c4                     @ 080bd5b8 0249
    ldrb r0,[r1,#0x10]                       @ 080bd5ba 087c
    adds r0,#0x1    @ 080bd5bc 0130
    strb r0,[r1,#0x10]                       @ 080bd5be 0874
    b LAB_080bd5a8                           @ 080bd5c0 f2e7
    .zero  0x2
DAT_080bd5c4:
    .word  gBannerState                   @ 080bd5c4 c0fe0102
switchD_080bd414__caseD_3:
    movs r4,#0x0    @ 080bd5c8 0024
    lsls r5,r5,#0x10    @ 080bd5ca 2d04
    .hword 0x4646    @ 080bd5cc 4646
LAB_080bd5ce:
    adds r0,r6,#0x0    @ 080bd5ce 301c
    orrs r0,r5    @ 080bd5d0 2843
    lsls r2,r4,#0x3    @ 080bd5d2 e200
    movs r1,#0x80    @ 080bd5d4 8021
    lsls r1,r1,#0x2    @ 080bd5d6 8900
    adds r2,r2,r1    @ 080bd5d8 5218
    movs r3,#0xc0    @ 080bd5da c023
    lsls r3,r3,#0x6    @ 080bd5dc 9b01
    adds r1,r3,#0x0    @ 080bd5de 191c
    orrs r2,r1    @ 080bd5e0 0a43
    lsls r2,r2,#0x10    @ 080bd5e2 1204
    lsrs r2,r2,#0x10    @ 080bd5e4 120c
    movs r1,#0xc0    @ 080bd5e6 c021
    bl write_oam_entry_from_packed_args      @ 080bd5e8 38f0c0fd
    adds r6,#0x40    @ 080bd5ec 4036
    adds r4,#0x1    @ 080bd5ee 0134
    cmp r4,#0x2                              @ 080bd5f0 022c
    ble LAB_080bd5ce                         @ 080bd5f2 ecdd
    movs r0,#0x2    @ 080bd5f4 0220
    bl start_blend_fadein_with_target        @ 080bd5f6 38f023f9
    cmp r0,#0x0                              @ 080bd5fa 0028
    beq LAB_080bd5a8                         @ 080bd5fc d4d0
    bl request_sound_engine_code10           @ 080bd5fe 3cf09ffa
    movs r1,#0x80    @ 080bd602 8021
    lsls r1,r1,#0x13    @ 080bd604 c904
    movs r0,#0x0    @ 080bd606 0020
    strh r0,[r1,#0x0]                        @ 080bd608 0880
    ldr r1, DAT_080bd614                     @ 080bd60a 0249
    ldrb r0,[r1,#0x10]                       @ 080bd60c 087c
    adds r0,#0x1    @ 080bd60e 0130
    strb r0,[r1,#0x10]                       @ 080bd610 0874
    b LAB_080bd5a8                           @ 080bd612 c9e7
DAT_080bd614:
    .word  gBannerState                   @ 080bd614 c0fe0102
switchD_080bd414__caseD_8:
    bl dispatch_banner_anim_tick_by_state    @ 080bd618 fff728fb
    cmp r0,#0x0                              @ 080bd61c 0028
    bne LAB_080bd5a8                         @ 080bd61e c3d1
LAB_080bd620:
    ldr r1, DAT_080bd62c                     @ 080bd620 0249
    ldrb r0,[r1,#0x10]                       @ 080bd622 087c
    adds r0,#0x1    @ 080bd624 0130
    strb r0,[r1,#0x10]                       @ 080bd626 0874
    b LAB_080bd5a8                           @ 080bd628 bee7
    .zero  0x2
DAT_080bd62c:
    .word  gBannerState                   @ 080bd62c c0fe0102
switchD_080bd414__caseD_4:
    movs r0,#0x2    @ 080bd630 0220
    rsbs r0,r0,#0    @ 080bd632 4042
    ldrb r1,[r7,#0x0]                        @ 080bd634 3978
    ands r0,r1    @ 080bd636 0840
    strb r0,[r7,#0x0]                        @ 080bd638 3870
    ldr r1, DAT_080bd658                     @ 080bd63a 0749
    ldr r2, DAT_080bd65c                     @ 080bd63c 074a
    adds r1,r1,r2    @ 080bd63e 8918
    movs r0,#0x5    @ 080bd640 0520
    rsbs r0,r0,#0    @ 080bd642 4042
    ldrb r3,[r1,#0x0]                        @ 080bd644 0b78
    ands r0,r3    @ 080bd646 1840
    strb r0,[r1,#0x0]                        @ 080bd648 0870
    movs r0,#0x0    @ 080bd64a 0020
LAB_080bd64c:
    pop {r3}                                 @ 080bd64c 08bc
    .hword 0x4698    @ 080bd64e 9846
    pop {r4,r5,r6,r7}                        @ 080bd650 f0bc
    pop {r1}                                 @ 080bd652 02bc
    bx r1                                    @ 080bd654 0847
    .zero  0x2
DAT_080bd658:
    .word  0x02023130                     @ 080bd658 30310202
DAT_080bd65c:
    .word  0x00000215                     @ 080bd65c 15020000

@ 驱动 duel puzzle (场景 scene_duel_puzzle) 的 banner 状态机, 每帧由 play_ui_effect (0x0801ef94) 调用. 读 gBannerState[+0x10] (u8 phase [0..8]) 驱动 switch 9 cases. case 0: 置 gDuelFieldCtx[+0x21e] bit0, 从 [gPrng+0x6c2c] 读 bit[4:0] 计算 player side, 以 side*3<<11 得 tile 偏移加 ROM 基址 (0x098f6104), copy_bytes_by_halfword 拷贝调色板 (src 0x098f60e4 to 0x05000260, 0x20 halfwords), tile_2d_row_copy 写 VRAM 0x06014000 (0x18 tiles x 8 rows), phase++. case 1 (sin 动画): 每帧从 rom_sin_table_q8 读 OAM y 坐标 (sin[gBannerState[+0x12]]*0x70/256), 循环写 3 OAM entries (tile 0xc0 attr), 计时 0x20 帧 phase++. case 2..7: 各阶段推进 OAM 动画 (垂直摆动 / 写 gBannerState[+0x8]). case 8: 切换下一动画 via sync_state_and_init_sprite + compute_duel_zone_dir_for_player 判 player. default: 置 gBannerState[+0x19] bit1 反转, return 0. 返回 1=进行中 / 0=完成. Constants: gBannerState=0x0201fec0, rom_sin_table_q8=0x09e5f8f0, tile_src=0x098f60e4, VRAM=0x06014000.
tick_duel_puzzle_banner_state_machine:
    push {r4,r5,r6,lr}                       @ 080bd660 70b5
    movs r5,#0x18    @ 080bd662 1825
    ldr r1, DAT_080bd698                     @ 080bd664 0c49
    ldr r2, DAT_080bd69c                     @ 080bd666 0d4a
    movs r0,#0x7f    @ 080bd668 7f20
    ldrh r3,[r2,#0x12]                       @ 080bd66a 538a
    ands r0,r3    @ 080bd66c 1840
    lsls r0,r0,#0x1    @ 080bd66e 4000
    adds r0,r0,r1    @ 080bd670 4018
    movs r3,#0x0    @ 080bd672 0023
    ldrsh r1,[r0,r3]                         @ 080bd674 c15e
    movs r0,#0x70    @ 080bd676 7020
    muls r0,r1    @ 080bd678 4843
    cmp r0,#0x0                              @ 080bd67a 0028
    bge LAB_080bd680                         @ 080bd67c 00da
    adds r0,#0xff    @ 080bd67e ff30
LAB_080bd680:
    lsls r0,r0,#0x8    @ 080bd680 0002
    lsrs r3,r0,#0x10    @ 080bd682 030c
    ldrb r0,[r2,#0x10]                       @ 080bd684 107c
    cmp r0,#0x8                              @ 080bd686 0828
    bls LAB_080bd68c                         @ 080bd688 00d9
    b switchD_080bd694__caseD_4              @ 080bd68a dbe0
LAB_080bd68c:
    lsls r0,r0,#0x2    @ 080bd68c 8000
    ldr r1, DAT_080bd6a0                     @ 080bd68e 0449
    adds r0,r0,r1    @ 080bd690 4018
    ldr r0,[r0,#0x0]                         @ 080bd692 0068
switchD_080bd694__switchD:
    .hword 0x4687    @ 080bd694 8746
    .zero  0x2
DAT_080bd698:
    .word  rom_sin_table_q8               @ 080bd698 f0f8e509
DAT_080bd69c:
    .word  gBannerState                   @ 080bd69c c0fe0102
DAT_080bd6a0:
    .word  0x080bd6a4                     @ 080bd6a0 a4d60b08
switchD_080bd694__switchdataD_080bd6a4:
    .word  0x080bd6c8                     @ 080bd6a4 c8d60b08
    .word  0x080bd724                     @ 080bd6a8 24d70b08
    .word  0x080bd77c                     @ 080bd6ac 7cd70b08
    .word  0x080bd808                     @ 080bd6b0 08d80b08
    .word  0x080bd844                     @ 080bd6b4 44d80b08
    .word  0x080bd844                     @ 080bd6b8 44d80b08
    .word  0x080bd844                     @ 080bd6bc 44d80b08
    .word  0x080bd844                     @ 080bd6c0 44d80b08
    .word  0x080bd82c                     @ 080bd6c4 2cd80b08
switchD_080bd694__caseD_0:
    ldr r1, DAT_080bd704                     @ 080bd6c8 0e49
    ldr r0, DAT_080bd708                     @ 080bd6ca 0f48
    adds r1,r1,r0    @ 080bd6cc 0918
    movs r0,#0x1    @ 080bd6ce 0120
    ldrb r2,[r1,#0x0]                        @ 080bd6d0 0a78
    orrs r0,r2    @ 080bd6d2 1043
    strb r0,[r1,#0x0]                        @ 080bd6d4 0870
    ldr r0, DAT_080bd70c                     @ 080bd6d6 0d48
    ldr r3, DAT_080bd710                     @ 080bd6d8 0d4b
    adds r0,r0,r3    @ 080bd6da c018
    ldrb r0,[r0,#0x0]                        @ 080bd6dc 0078
    lsls r0,r0,#0x1d    @ 080bd6de 4007
    lsrs r0,r0,#0x1d    @ 080bd6e0 400f
    lsls r4,r0,#0x1    @ 080bd6e2 4400
    adds r4,r4,r0    @ 080bd6e4 2418
    lsls r4,r4,#0xb    @ 080bd6e6 e402
    ldr r0, DAT_080bd714                     @ 080bd6e8 0a48
    adds r4,r4,r0    @ 080bd6ea 2418
    ldr r0, DAT_080bd718                     @ 080bd6ec 0a48
    ldr r1, DAT_080bd71c                     @ 080bd6ee 0b49
    movs r2,#0x20    @ 080bd6f0 2022
    bl copy_bytes_by_halfword                @ 080bd6f2 37f0d7fb
    ldr r0, DAT_080bd720                     @ 080bd6f6 0a48
    adds r1,r4,#0x0    @ 080bd6f8 211c
    movs r2,#0x18    @ 080bd6fa 1822
    movs r3,#0x8    @ 080bd6fc 0823
    bl tile_2d_row_copy                      @ 080bd6fe 39f0e9fe
    b LAB_080bd834                           @ 080bd702 97e0
DAT_080bd704:
    .word  0x02023130                     @ 080bd704 30310202
DAT_080bd708:
    .word  0x0000021e                     @ 080bd708 1e020000
DAT_080bd70c:
    .word  0x02000000                     @ 080bd70c 00000002
DAT_080bd710:
    .word  0x00006c2c                     @ 080bd710 2c6c0000
DAT_080bd714:
    .word  0x098f6104                     @ 080bd714 04618f09
DAT_080bd718:
    .word  0x05000260                     @ 080bd718 60020005
DAT_080bd71c:
    .word  0x098f60e4                     @ 080bd71c e4608f09
DAT_080bd720:
    .word  0x06014000                     @ 080bd720 00400106
switchD_080bd694__caseD_1:
    movs r4,#0x0    @ 080bd724 0024
    movs r1,#0xe0    @ 080bd726 e021
    lsls r1,r1,#0x1    @ 080bd728 4900
    adds r0,r3,r1    @ 080bd72a 5818
    lsls r6,r0,#0x10    @ 080bd72c 0604
LAB_080bd72e:
    adds r0,r5,#0x0    @ 080bd72e 281c
    orrs r0,r6    @ 080bd730 3043
    lsls r2,r4,#0x3    @ 080bd732 e200
    movs r3,#0x80    @ 080bd734 8023
    lsls r3,r3,#0x2    @ 080bd736 9b00
    adds r2,r2,r3    @ 080bd738 d218
    movs r3,#0xc0    @ 080bd73a c023
    lsls r3,r3,#0x6    @ 080bd73c 9b01
    adds r1,r3,#0x0    @ 080bd73e 191c
    orrs r2,r1    @ 080bd740 0a43
    lsls r2,r2,#0x10    @ 080bd742 1204
    lsrs r2,r2,#0x10    @ 080bd744 120c
    movs r1,#0xc0    @ 080bd746 c021
    bl write_oam_entry_from_packed_args      @ 080bd748 38f010fd
    adds r5,#0x40    @ 080bd74c 4035
    adds r4,#0x1    @ 080bd74e 0134
    cmp r4,#0x2                              @ 080bd750 022c
    ble LAB_080bd72e                         @ 080bd752 ecdd
    ldr r1, DAT_080bd778                     @ 080bd754 0849
    ldrh r0,[r1,#0x12]                       @ 080bd756 488a
    adds r0,#0x3    @ 080bd758 0330
    strh r0,[r1,#0x12]                       @ 080bd75a 4882
    lsls r0,r0,#0x10    @ 080bd75c 0004
    lsrs r0,r0,#0x10    @ 080bd75e 000c
    cmp r0,#0x20                             @ 080bd760 2028
    bls LAB_080bd7e8                         @ 080bd762 41d9
    movs r0,#0x0    @ 080bd764 0020
    strh r0,[r1,#0x12]                       @ 080bd766 4882
    ldrb r0,[r1,#0x10]                       @ 080bd768 087c
    adds r0,#0x1    @ 080bd76a 0130
    strb r0,[r1,#0x10]                       @ 080bd76c 0874
    movs r0,#0x23    @ 080bd76e 2320
    bl sync_state_and_init_sprite            @ 080bd770 3cf0a0f9
    b LAB_080bd7e8                           @ 080bd774 38e0
    .zero  0x2
DAT_080bd778:
    .word  gBannerState                   @ 080bd778 c0fe0102
switchD_080bd694__caseD_2:
    movs r4,#0x0    @ 080bd77c 0024
    movs r0,#0x30    @ 080bd77e 3020
    lsls r6,r0,#0x10    @ 080bd780 0604
LAB_080bd782:
    adds r0,r5,#0x0    @ 080bd782 281c
    orrs r0,r6    @ 080bd784 3043
    lsls r2,r4,#0x3    @ 080bd786 e200
    movs r1,#0x80    @ 080bd788 8021
    lsls r1,r1,#0x2    @ 080bd78a 8900
    adds r2,r2,r1    @ 080bd78c 5218
    movs r3,#0xc0    @ 080bd78e c023
    lsls r3,r3,#0x6    @ 080bd790 9b01
    adds r1,r3,#0x0    @ 080bd792 191c
    orrs r2,r1    @ 080bd794 0a43
    lsls r2,r2,#0x10    @ 080bd796 1204
    lsrs r2,r2,#0x10    @ 080bd798 120c
    movs r1,#0xc0    @ 080bd79a c021
    bl write_oam_entry_from_packed_args      @ 080bd79c 38f0e6fc
    adds r5,#0x40    @ 080bd7a0 4035
    adds r4,#0x1    @ 080bd7a2 0134
    cmp r4,#0x2                              @ 080bd7a4 022c
    ble LAB_080bd782                         @ 080bd7a6 ecdd
    ldr r4, DAT_080bd7ec                     @ 080bd7a8 104c
    ldrh r0,[r4,#0x12]                       @ 080bd7aa 608a
    adds r0,#0x1    @ 080bd7ac 0130
    movs r5,#0x0    @ 080bd7ae 0025
    strh r0,[r4,#0x12]                       @ 080bd7b0 6082
    lsls r0,r0,#0x10    @ 080bd7b2 0004
    lsrs r0,r0,#0x10    @ 080bd7b4 000c
    cmp r0,#0x40                             @ 080bd7b6 4028
    bls LAB_080bd7e8                         @ 080bd7b8 16d9
    bl disable_blend_and_clear_step          @ 080bd7ba 37f00bff
    ldr r1, PTR_gPrng_080bd7f0               @ 080bd7be 0c49
    ldr r0, DAT_080bd7f4                     @ 080bd7c0 0c48
    adds r1,r1,r0    @ 080bd7c2 0918
    movs r0,#0x1    @ 080bd7c4 0120
    ldrb r1,[r1,#0x0]                        @ 080bd7c6 0978
    ands r0,r1    @ 080bd7c8 0840
    cmp r0,#0x0                              @ 080bd7ca 0028
    beq LAB_080bd7f8                         @ 080bd7cc 14d0
    movs r0,#0x3    @ 080bd7ce 0320
    bl compute_duel_zone_dir_for_player      @ 080bd7d0 0ef060ff
    cmp r0,#0x2                              @ 080bd7d4 0228
    beq LAB_080bd7e0                         @ 080bd7d6 03d0
    cmp r0,#0x2                              @ 080bd7d8 0228
    bgt LAB_080bd7f8                         @ 080bd7da 0ddc
    cmp r0,#0x1                              @ 080bd7dc 0128
    bne LAB_080bd7f8                         @ 080bd7de 0bd1
LAB_080bd7e0:
    str r0,[r4,#0x8]                         @ 080bd7e0 a060
    movs r0,#0x8    @ 080bd7e2 0820
    strb r0,[r4,#0x10]                       @ 080bd7e4 2074
    strb r5,[r4,#0x11]                       @ 080bd7e6 6574
LAB_080bd7e8:
    movs r0,#0x1    @ 080bd7e8 0120
    b LAB_080bd860                           @ 080bd7ea 39e0
DAT_080bd7ec:
    .word  gBannerState                   @ 080bd7ec c0fe0102
PTR_gPrng_080bd7f0:
    .word  gPrng                          @ 080bd7f0 40000003
DAT_080bd7f4:
    .word  0x0000023f                     @ 080bd7f4 3f020000
LAB_080bd7f8:
    ldr r1, DAT_080bd804                     @ 080bd7f8 0249
    ldrb r0,[r1,#0x10]                       @ 080bd7fa 087c
    adds r0,#0x1    @ 080bd7fc 0130
    strb r0,[r1,#0x10]                       @ 080bd7fe 0874
    b LAB_080bd7e8                           @ 080bd800 f2e7
    .zero  0x2
DAT_080bd804:
    .word  gBannerState                   @ 080bd804 c0fe0102
switchD_080bd694__caseD_3:
    movs r0,#0x2    @ 080bd808 0220
    bl start_blend_fadein_with_target        @ 080bd80a 38f019f8
    cmp r0,#0x0                              @ 080bd80e 0028
    beq LAB_080bd7e8                         @ 080bd810 ead0
    bl request_sound_engine_code10           @ 080bd812 3cf095f9
    movs r1,#0x80    @ 080bd816 8021
    lsls r1,r1,#0x13    @ 080bd818 c904
    movs r0,#0x0    @ 080bd81a 0020
    strh r0,[r1,#0x0]                        @ 080bd81c 0880
    ldr r1, DAT_080bd828                     @ 080bd81e 0249
    ldrb r0,[r1,#0x10]                       @ 080bd820 087c
    adds r0,#0x1    @ 080bd822 0130
    strb r0,[r1,#0x10]                       @ 080bd824 0874
    b LAB_080bd7e8                           @ 080bd826 dfe7
DAT_080bd828:
    .word  gBannerState                   @ 080bd828 c0fe0102
switchD_080bd694__caseD_8:
    bl dispatch_banner_anim_tick_by_state    @ 080bd82c fff71efa
    cmp r0,#0x0                              @ 080bd830 0028
    bne LAB_080bd7e8                         @ 080bd832 d9d1
LAB_080bd834:
    ldr r1, DAT_080bd840                     @ 080bd834 0249
    ldrb r0,[r1,#0x10]                       @ 080bd836 087c
    adds r0,#0x1    @ 080bd838 0130
    strb r0,[r1,#0x10]                       @ 080bd83a 0874
    b LAB_080bd7e8                           @ 080bd83c d4e7
    .zero  0x2
DAT_080bd840:
    .word  gBannerState                   @ 080bd840 c0fe0102
switchD_080bd694__caseD_4:
    movs r0,#0x2    @ 080bd844 0220
    rsbs r0,r0,#0    @ 080bd846 4042
    ldrb r1,[r2,#0x0]                        @ 080bd848 1178
    ands r0,r1    @ 080bd84a 0840
    strb r0,[r2,#0x0]                        @ 080bd84c 1070
    ldr r1, DAT_080bd868                     @ 080bd84e 0649
    ldr r2, DAT_080bd86c                     @ 080bd850 064a
    adds r1,r1,r2    @ 080bd852 8918
    movs r0,#0x5    @ 080bd854 0520
    rsbs r0,r0,#0    @ 080bd856 4042
    ldrb r3,[r1,#0x0]                        @ 080bd858 0b78
    ands r0,r3    @ 080bd85a 1840
    strb r0,[r1,#0x0]                        @ 080bd85c 0870
    movs r0,#0x0    @ 080bd85e 0020
LAB_080bd860:
    pop {r4,r5,r6}                           @ 080bd860 70bc
    pop {r1}                                 @ 080bd862 02bc
    bx r1                                    @ 080bd864 0847
    .zero  0x2
DAT_080bd868:
    .word  0x02023130                     @ 080bd868 30310202
DAT_080bd86c:
    .word  0x00000215                     @ 080bd86c 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x30 子状态机, 待详细分析.
play_ui_effect_30:
    push {r4,r5,r6,r7,lr}                    @ 080bd870 f0b5
    movs r7,#0x2c    @ 080bd872 2c27
    movs r5,#0x28    @ 080bd874 2825
    ldr r4, DAT_080bd88c                     @ 080bd876 054c
    ldrb r0,[r4,#0x10]                       @ 080bd878 207c
    adds r2,r4,#0x0    @ 080bd87a 221c
    cmp r0,#0x4                              @ 080bd87c 0428
    bls LAB_080bd882                         @ 080bd87e 00d9
switchD_080bd88a__default:
    b LAB_080bda4c                           @ 080bd880 e4e0
LAB_080bd882:
    lsls r0,r0,#0x2    @ 080bd882 8000
    ldr r1, DAT_080bd890                     @ 080bd884 0249
    adds r0,r0,r1    @ 080bd886 4018
    ldr r0,[r0,#0x0]                         @ 080bd888 0068
switchD_080bd88a__switchD:
    .hword 0x4687    @ 080bd88a 8746
DAT_080bd88c:
    .word  gBannerState                   @ 080bd88c c0fe0102
DAT_080bd890:
    .word  0x080bd894                     @ 080bd890 94d80b08
switchD_080bd88a__switchdataD_080bd894:
    .word  0x080bd8a8                     @ 080bd894 a8d80b08
    .word  0x080bd920                     @ 080bd898 20d90b08
    .word  0x080bd988                     @ 080bd89c 88d90b08
    .word  0x080bd9d4                     @ 080bd8a0 d4d90b08
    .word  0x080bda40                     @ 080bd8a4 40da0b08
switchD_080bd88a__caseD_0:
    ldr r1, DAT_080bd8f8                     @ 080bd8a8 1349
    ldr r0, DAT_080bd8fc                     @ 080bd8aa 1448
    adds r1,r1,r0    @ 080bd8ac 0918
    movs r0,#0x1    @ 080bd8ae 0120
    ldrb r2,[r1,#0x0]                        @ 080bd8b0 0a78
    orrs r0,r2    @ 080bd8b2 1043
    strb r0,[r1,#0x0]                        @ 080bd8b4 0870
    ldr r0, DAT_080bd900                     @ 080bd8b6 1248
    ldr r1, DAT_080bd904                     @ 080bd8b8 1249
    movs r2,#0x20    @ 080bd8ba 2022
    bl copy_bytes_by_halfword                @ 080bd8bc 37f0f2fa
    ldr r0, DAT_080bd908                     @ 080bd8c0 1148
    ldr r1, DAT_080bd90c                     @ 080bd8c2 1249
    ldr r3, DAT_080bd910                     @ 080bd8c4 124b
    adds r1,r1,r3    @ 080bd8c6 c918
    ldrb r1,[r1,#0x0]                        @ 080bd8c8 0978
    lsls r2,r1,#0x1d    @ 080bd8ca 4a07
    lsrs r2,r2,#0x1d    @ 080bd8cc 520f
    lsls r1,r2,#0x1    @ 080bd8ce 5100
    adds r1,r1,r2    @ 080bd8d0 8918
    lsls r1,r1,#0xb    @ 080bd8d2 c902
    ldr r2, DAT_080bd914                     @ 080bd8d4 0f4a
    adds r1,r1,r2    @ 080bd8d6 8918
    movs r2,#0x18    @ 080bd8d8 1822
    movs r3,#0x8    @ 080bd8da 0823
    bl tile_2d_row_copy                      @ 080bd8dc 39f0fafd
    ldr r1, PTR_BLDCNT_080bd918              @ 080bd8e0 0d49
    movs r2,#0xfd    @ 080bd8e2 fd22
    lsls r2,r2,#0x6    @ 080bd8e4 9201
    adds r0,r2,#0x0    @ 080bd8e6 101c
    strh r0,[r1,#0x0]                        @ 080bd8e8 0880
    ldr r1, DAT_080bd91c                     @ 080bd8ea 0c49
    ldrb r0,[r1,#0x10]                       @ 080bd8ec 087c
    adds r0,#0x1    @ 080bd8ee 0130
    strb r0,[r1,#0x10]                       @ 080bd8f0 0874
LAB_080bd8f2:
    movs r0,#0x1    @ 080bd8f2 0120
    b LAB_080bda6c                           @ 080bd8f4 bae0
    .zero  0x2
DAT_080bd8f8:
    .word  0x02023130                     @ 080bd8f8 30310202
DAT_080bd8fc:
    .word  0x0000021e                     @ 080bd8fc 1e020000
DAT_080bd900:
    .word  0x05000260                     @ 080bd900 60020005
DAT_080bd904:
    .word  0x098ff104                     @ 080bd904 04f18f09
DAT_080bd908:
    .word  0x06014000                     @ 080bd908 00400106
DAT_080bd90c:
    .word  0x02000000                     @ 080bd90c 00000002
DAT_080bd910:
    .word  0x00006c2c                     @ 080bd910 2c6c0000
DAT_080bd914:
    .word  0x098ff124                     @ 080bd914 24f18f09
PTR_BLDCNT_080bd918:
    .word  BLDCNT                         @ 080bd918 50000004
DAT_080bd91c:
    .word  gBannerState                   @ 080bd91c c0fe0102
switchD_080bd88a__caseD_1:
    ldr r3, PTR_BLDALPHA_080bd980            @ 080bd920 174b
    ldrb r1,[r2,#0x11]                       @ 080bd922 517c
    lsls r2,r1,#0x1    @ 080bd924 4a00
    lsls r1,r1,#0x19    @ 080bd926 4906
    lsrs r1,r1,#0x18    @ 080bd928 090e
    movs r0,#0x10    @ 080bd92a 1020
    subs r0,r0,r2    @ 080bd92c 801a
    lsls r0,r0,#0x18    @ 080bd92e 0006
    lsrs r0,r0,#0x10    @ 080bd930 000c
    orrs r1,r0    @ 080bd932 0143
    strh r1,[r3,#0x0]                        @ 080bd934 1980
    movs r4,#0x0    @ 080bd936 0024
    lsls r6,r5,#0x10    @ 080bd938 2e04
    adds r5,r7,#0x0    @ 080bd93a 3d1c
LAB_080bd93c:
    adds r0,r5,#0x0    @ 080bd93c 281c
    orrs r0,r6    @ 080bd93e 3043
    lsls r2,r4,#0x3    @ 080bd940 e200
    movs r3,#0x80    @ 080bd942 8023
    lsls r3,r3,#0x2    @ 080bd944 9b00
    adds r2,r2,r3    @ 080bd946 d218
    movs r3,#0xc0    @ 080bd948 c023
    lsls r3,r3,#0x6    @ 080bd94a 9b01
    adds r1,r3,#0x0    @ 080bd94c 191c
    orrs r2,r1    @ 080bd94e 0a43
    lsls r2,r2,#0x10    @ 080bd950 1204
    lsrs r2,r2,#0x10    @ 080bd952 120c
    movs r1,#0x98    @ 080bd954 9821
    lsls r1,r1,#0x3    @ 080bd956 c900
    bl write_oam_entry_from_packed_args      @ 080bd958 38f008fc
    adds r5,#0x40    @ 080bd95c 4035
    adds r4,#0x1    @ 080bd95e 0134
    cmp r4,#0x2                              @ 080bd960 022c
    ble LAB_080bd93c                         @ 080bd962 ebdd
    ldr r1, DAT_080bd984                     @ 080bd964 0749
    ldrb r0,[r1,#0x11]                       @ 080bd966 487c
    adds r0,#0x1    @ 080bd968 0130
    strb r0,[r1,#0x11]                       @ 080bd96a 4874
    lsls r0,r0,#0x18    @ 080bd96c 0006
    lsrs r0,r0,#0x18    @ 080bd96e 000e
    cmp r0,#0x8                              @ 080bd970 0828
    bls LAB_080bd8f2                         @ 080bd972 bed9
    ldrb r0,[r1,#0x10]                       @ 080bd974 087c
    adds r0,#0x1    @ 080bd976 0130
    strb r0,[r1,#0x10]                       @ 080bd978 0874
    movs r0,#0x0    @ 080bd97a 0020
    strb r0,[r1,#0x11]                       @ 080bd97c 4874
    b LAB_080bd8f2                           @ 080bd97e b8e7
PTR_BLDALPHA_080bd980:
    .word  BLDALPHA                       @ 080bd980 52000004
DAT_080bd984:
    .word  gBannerState                   @ 080bd984 c0fe0102
switchD_080bd88a__caseD_2:
    movs r4,#0x0    @ 080bd988 0024
    lsls r6,r5,#0x10    @ 080bd98a 2e04
    adds r5,r7,#0x0    @ 080bd98c 3d1c
LAB_080bd98e:
    adds r0,r5,#0x0    @ 080bd98e 281c
    orrs r0,r6    @ 080bd990 3043
    lsls r2,r4,#0x3    @ 080bd992 e200
    movs r1,#0x80    @ 080bd994 8021
    lsls r1,r1,#0x2    @ 080bd996 8900
    adds r2,r2,r1    @ 080bd998 5218
    movs r3,#0xc0    @ 080bd99a c023
    lsls r3,r3,#0x6    @ 080bd99c 9b01
    adds r1,r3,#0x0    @ 080bd99e 191c
    orrs r2,r1    @ 080bd9a0 0a43
    lsls r2,r2,#0x10    @ 080bd9a2 1204
    lsrs r2,r2,#0x10    @ 080bd9a4 120c
    movs r1,#0xc0    @ 080bd9a6 c021
    bl write_oam_entry_from_packed_args      @ 080bd9a8 38f0e0fb
    adds r5,#0x40    @ 080bd9ac 4035
    adds r4,#0x1    @ 080bd9ae 0134
    cmp r4,#0x2                              @ 080bd9b0 022c
    ble LAB_080bd98e                         @ 080bd9b2 ecdd
    ldr r1, DAT_080bd9d0                     @ 080bd9b4 0649
    ldrb r0,[r1,#0x11]                       @ 080bd9b6 487c
    adds r0,#0x1    @ 080bd9b8 0130
    strb r0,[r1,#0x11]                       @ 080bd9ba 4874
    lsls r0,r0,#0x18    @ 080bd9bc 0006
    lsrs r0,r0,#0x18    @ 080bd9be 000e
    cmp r0,#0x40                             @ 080bd9c0 4028
    bls LAB_080bd8f2                         @ 080bd9c2 96d9
    ldrb r0,[r1,#0x10]                       @ 080bd9c4 087c
    adds r0,#0x1    @ 080bd9c6 0130
    strb r0,[r1,#0x10]                       @ 080bd9c8 0874
    movs r0,#0x0    @ 080bd9ca 0020
    strb r0,[r1,#0x11]                       @ 080bd9cc 4874
    b LAB_080bd8f2                           @ 080bd9ce 90e7
DAT_080bd9d0:
    .word  gBannerState                   @ 080bd9d0 c0fe0102
switchD_080bd88a__caseD_3:
    ldr r3, PTR_BLDALPHA_080bda38            @ 080bd9d4 184b
    ldrb r1,[r2,#0x11]                       @ 080bd9d6 517c
    lsls r2,r1,#0x1    @ 080bd9d8 4a00
    movs r0,#0x10    @ 080bd9da 1020
    subs r0,r0,r2    @ 080bd9dc 801a
    lsls r0,r0,#0x18    @ 080bd9de 0006
    lsrs r0,r0,#0x18    @ 080bd9e0 000e
    lsls r1,r1,#0x19    @ 080bd9e2 4906
    lsrs r1,r1,#0x10    @ 080bd9e4 090c
    orrs r0,r1    @ 080bd9e6 0843
    strh r0,[r3,#0x0]                        @ 080bd9e8 1880
    movs r4,#0x0    @ 080bd9ea 0024
    lsls r6,r5,#0x10    @ 080bd9ec 2e04
    adds r5,r7,#0x0    @ 080bd9ee 3d1c
LAB_080bd9f0:
    adds r0,r5,#0x0    @ 080bd9f0 281c
    orrs r0,r6    @ 080bd9f2 3043
    lsls r2,r4,#0x3    @ 080bd9f4 e200
    movs r1,#0x80    @ 080bd9f6 8021
    lsls r1,r1,#0x2    @ 080bd9f8 8900
    adds r2,r2,r1    @ 080bd9fa 5218
    movs r3,#0xc0    @ 080bd9fc c023
    lsls r3,r3,#0x6    @ 080bd9fe 9b01
    adds r1,r3,#0x0    @ 080bda00 191c
    orrs r2,r1    @ 080bda02 0a43
    lsls r2,r2,#0x10    @ 080bda04 1204
    lsrs r2,r2,#0x10    @ 080bda06 120c
    movs r1,#0x98    @ 080bda08 9821
    lsls r1,r1,#0x3    @ 080bda0a c900
    bl write_oam_entry_from_packed_args      @ 080bda0c 38f0aefb
    adds r5,#0x40    @ 080bda10 4035
    adds r4,#0x1    @ 080bda12 0134
    cmp r4,#0x2                              @ 080bda14 022c
    ble LAB_080bd9f0                         @ 080bda16 ebdd
    ldr r1, DAT_080bda3c                     @ 080bda18 0849
    ldrb r0,[r1,#0x11]                       @ 080bda1a 487c
    adds r0,#0x1    @ 080bda1c 0130
    strb r0,[r1,#0x11]                       @ 080bda1e 4874
    lsls r0,r0,#0x18    @ 080bda20 0006
    lsrs r0,r0,#0x18    @ 080bda22 000e
    cmp r0,#0x8                              @ 080bda24 0828
    bhi LAB_080bda2a                         @ 080bda26 00d8
    b LAB_080bd8f2                           @ 080bda28 63e7
LAB_080bda2a:
    ldrb r0,[r1,#0x10]                       @ 080bda2a 087c
    adds r0,#0x1    @ 080bda2c 0130
    strb r0,[r1,#0x10]                       @ 080bda2e 0874
    movs r0,#0x0    @ 080bda30 0020
    strb r0,[r1,#0x11]                       @ 080bda32 4874
    b LAB_080bd8f2                           @ 080bda34 5de7
    .zero  0x2
PTR_BLDALPHA_080bda38:
    .word  BLDALPHA                       @ 080bda38 52000004
DAT_080bda3c:
    .word  gBannerState                   @ 080bda3c c0fe0102
switchD_080bd88a__caseD_4:
    ldrb r0,[r2,#0x10]                       @ 080bda40 107c
    adds r0,#0x1    @ 080bda42 0130
    movs r1,#0x0    @ 080bda44 0021
    strb r0,[r2,#0x10]                       @ 080bda46 1074
    strb r1,[r2,#0x11]                       @ 080bda48 5174
    b LAB_080bd8f2                           @ 080bda4a 52e7
LAB_080bda4c:
    bl disable_blend_and_clear_step          @ 080bda4c 37f0c2fd
    movs r0,#0x2    @ 080bda50 0220
    rsbs r0,r0,#0    @ 080bda52 4042
    ldrb r1,[r4,#0x0]                        @ 080bda54 2178
    ands r0,r1    @ 080bda56 0840
    strb r0,[r4,#0x0]                        @ 080bda58 2070
    ldr r1, DAT_080bda74                     @ 080bda5a 0649
    ldr r2, DAT_080bda78                     @ 080bda5c 064a
    adds r1,r1,r2    @ 080bda5e 8918
    movs r0,#0x5    @ 080bda60 0520
    rsbs r0,r0,#0    @ 080bda62 4042
    ldrb r3,[r1,#0x0]                        @ 080bda64 0b78
    ands r0,r3    @ 080bda66 1840
    strb r0,[r1,#0x0]                        @ 080bda68 0870
    movs r0,#0x0    @ 080bda6a 0020
LAB_080bda6c:
    pop {r4,r5,r6,r7}                        @ 080bda6c f0bc
    pop {r1}                                 @ 080bda6e 02bc
    bx r1                                    @ 080bda70 0847
    .zero  0x2
DAT_080bda74:
    .word  0x02023130                     @ 080bda74 30310202
DAT_080bda78:
    .word  0x00000215                     @ 080bda78 15020000

@ pack banner 子状态机 A, 与 tick_pack_banner_state_machine_b (0x080bdbb4) 结构完全对称, 同为 play_ui_effect_0b 唯一调用路径的两个变体之一. 使用不同 ROM palette 地址: case 0 copy_bytes_by_halfword src=0x098cc0a4 (vs B 的 0x098c9064); case 2 blend 源=0x098c9064 (两者共用). switch 覆盖 phase [0..4]: case 0 = palette+tile init+BLDCNT/BLDALPHA+phase++; case 1 = 直接 phase++; case 2 = blend + OAM 2 entries (tile 0x40c0, x=0x4c, y 每次+0x40); case 3 = 计时后 gBannerState[+0x10]++ (32+1=0x21 帧触发 sync_state_and_init_sprite); case 4 = 直接 phase++. default = disable_blend + return 0. Constants: gBannerState=0x0201fec0, BLDCNT=0x04000050, BLDALPHA=0x04000052, pal_init_src=0x098cc0a4, pal_blend_src=0x098c9064, pal_dst=0x05000260, tile_vram=0x06014000, OAM_tile=0x40c0, x_base=0x4c.
tick_pack_banner_state_machine_a:
    push {r4,r5,r6,lr}                       @ 080bda7c 70b5
    ldr r0, DAT_080bda94                     @ 080bda7e 0548
    ldrb r1,[r0,#0x10]                       @ 080bda80 017c
    adds r2,r0,#0x0    @ 080bda82 021c
    cmp r1,#0x4                              @ 080bda84 0429
    bls LAB_080bda8a                         @ 080bda86 00d9
switchD_080bda92__default:
    b LAB_080bdba8                           @ 080bda88 8ee0
LAB_080bda8a:
    lsls r0,r1,#0x2    @ 080bda8a 8800
    ldr r1, DAT_080bda98                     @ 080bda8c 0249
    adds r0,r0,r1    @ 080bda8e 4018
    ldr r0,[r0,#0x0]                         @ 080bda90 0068
switchD_080bda92__switchD:
    .hword 0x4687    @ 080bda92 8746
DAT_080bda94:
    .word  gBannerState                   @ 080bda94 c0fe0102
DAT_080bda98:
    .word  0x080bda9c                     @ 080bda98 9cda0b08
switchD_080bda92__switchdataD_080bda9c:
    .word  0x080bdab0                     @ 080bda9c b0da0b08
    .word  0x080bdba0                     @ 080bdaa0 a0db0b08
    .word  0x080bdb1c                     @ 080bdaa4 1cdb0b08
    .word  0x080bdba0                     @ 080bdaa8 a0db0b08
    .word  0x080bdba0                     @ 080bdaac a0db0b08
switchD_080bda92__caseD_0:
    ldr r0, DAT_080bdaf8                     @ 080bdab0 1148
    ldr r1, DAT_080bdafc                     @ 080bdab2 1249
    adds r0,r0,r1    @ 080bdab4 4018
    ldrb r0,[r0,#0x0]                        @ 080bdab6 0078
    lsls r4,r0,#0x1d    @ 080bdab8 4407
    lsrs r4,r4,#0x11    @ 080bdaba 640c
    ldr r0, DAT_080bdb00                     @ 080bdabc 1048
    adds r4,r4,r0    @ 080bdabe 2418
    ldr r0, DAT_080bdb04                     @ 080bdac0 1048
    ldr r1, DAT_080bdb08                     @ 080bdac2 1149
    movs r2,#0x20    @ 080bdac4 2022
    bl copy_bytes_by_halfword                @ 080bdac6 37f0edf9
    ldr r0, DAT_080bdb0c                     @ 080bdaca 1048
    adds r1,r4,#0x0    @ 080bdacc 211c
    movs r2,#0x10    @ 080bdace 1022
    movs r3,#0x8    @ 080bdad0 0823
    bl tile_2d_row_copy                      @ 080bdad2 39f0fffc
    bl disable_blend_and_clear_step          @ 080bdad6 37f07dfd
    ldr r1, PTR_BLDCNT_080bdb10              @ 080bdada 0d49
    movs r2,#0xfd    @ 080bdadc fd22
    lsls r2,r2,#0x6    @ 080bdade 9201
    adds r0,r2,#0x0    @ 080bdae0 101c
    strh r0,[r1,#0x0]                        @ 080bdae2 0880
    ldr r0, PTR_BLDALPHA_080bdb14            @ 080bdae4 0b48
    movs r1,#0x0    @ 080bdae6 0021
    strh r1,[r0,#0x0]                        @ 080bdae8 0180
    ldr r0, DAT_080bdb18                     @ 080bdaea 0b48
    strb r1,[r0,#0x11]                       @ 080bdaec 4174
    ldrb r1,[r0,#0x10]                       @ 080bdaee 017c
    adds r1,#0x1    @ 080bdaf0 0131
    strb r1,[r0,#0x10]                       @ 080bdaf2 0174
LAB_080bdaf4:
    movs r0,#0x1    @ 080bdaf4 0120
    b LAB_080bdbae                           @ 080bdaf6 5ae0
DAT_080bdaf8:
    .word  0x02000000                     @ 080bdaf8 00000002
DAT_080bdafc:
    .word  0x00006c2c                     @ 080bdafc 2c6c0000
DAT_080bdb00:
    .word  0x098cc0a4                     @ 080bdb00 a4c08c09
DAT_080bdb04:
    .word  0x05000260                     @ 080bdb04 60020005
DAT_080bdb08:
    .word  0x098cc084                     @ 080bdb08 84c08c09
DAT_080bdb0c:
    .word  0x06014000                     @ 080bdb0c 00400106
PTR_BLDCNT_080bdb10:
    .word  BLDCNT                         @ 080bdb10 50000004
PTR_BLDALPHA_080bdb14:
    .word  BLDALPHA                       @ 080bdb14 52000004
DAT_080bdb18:
    .word  gBannerState                   @ 080bdb18 c0fe0102
switchD_080bda92__caseD_2:
    ldrb r0,[r2,#0x11]                       @ 080bdb1c 507c
    cmp r0,#0x10                             @ 080bdb1e 1028
    bhi LAB_080bdb4c                         @ 080bdb20 14d8
    cmp r0,#0x8                              @ 080bdb22 0828
    bhi LAB_080bdb38                         @ 080bdb24 08d8
    ldr r0, DAT_080bdb34                     @ 080bdb26 0348
    ldrb r2,[r2,#0x11]                       @ 080bdb28 527c
    lsls r2,r2,#0x1    @ 080bdb2a 5200
    movs r1,#0x3    @ 080bdb2c 0321
    bl blend_palette_entry_toward_target     @ 080bdb2e fef757fe
    b LAB_080bdb4c                           @ 080bdb32 0be0
DAT_080bdb34:
    .word  0x098c9064                     @ 080bdb34 64908c09
LAB_080bdb38:
    ldr r0, DAT_080bdb98                     @ 080bdb38 1748
    ldrb r2,[r2,#0x11]                       @ 080bdb3a 527c
    lsls r1,r2,#0x1    @ 080bdb3c 5100
    movs r2,#0x20    @ 080bdb3e 2022
    subs r2,r2,r1    @ 080bdb40 521a
    lsls r2,r2,#0x10    @ 080bdb42 1204
    lsrs r2,r2,#0x10    @ 080bdb44 120c
    movs r1,#0x3    @ 080bdb46 0321
    bl blend_palette_entry_toward_target     @ 080bdb48 fef74afe
LAB_080bdb4c:
    movs r5,#0x0    @ 080bdb4c 0025
    movs r0,#0x28    @ 080bdb4e 2820
    lsls r6,r0,#0x10    @ 080bdb50 0604
    movs r4,#0x4c    @ 080bdb52 4c24
LAB_080bdb54:
    adds r0,r4,#0x0    @ 080bdb54 201c
    orrs r0,r6    @ 080bdb56 3043
    lsls r2,r5,#0x3    @ 080bdb58 ea00
    movs r3,#0x80    @ 080bdb5a 8023
    lsls r3,r3,#0x2    @ 080bdb5c 9b00
    adds r2,r2,r3    @ 080bdb5e d218
    movs r3,#0xc0    @ 080bdb60 c023
    lsls r3,r3,#0x6    @ 080bdb62 9b01
    adds r1,r3,#0x0    @ 080bdb64 191c
    orrs r2,r1    @ 080bdb66 0a43
    lsls r2,r2,#0x10    @ 080bdb68 1204
    lsrs r2,r2,#0x10    @ 080bdb6a 120c
    movs r1,#0xc0    @ 080bdb6c c021
    bl write_oam_entry_from_packed_args      @ 080bdb6e 38f0fdfa
    adds r4,#0x40    @ 080bdb72 4034
    adds r5,#0x1    @ 080bdb74 0135
    cmp r5,#0x1                              @ 080bdb76 012d
    ble LAB_080bdb54                         @ 080bdb78 ecdd
    ldr r1, DAT_080bdb9c                     @ 080bdb7a 0849
    ldrb r0,[r1,#0x11]                       @ 080bdb7c 487c
    adds r0,#0x1    @ 080bdb7e 0130
    strb r0,[r1,#0x11]                       @ 080bdb80 4874
    lsls r0,r0,#0x18    @ 080bdb82 0006
    lsrs r0,r0,#0x18    @ 080bdb84 000e
    cmp r0,#0x1f                             @ 080bdb86 1f28
    bls LAB_080bdaf4                         @ 080bdb88 b4d9
    ldrb r0,[r1,#0x10]                       @ 080bdb8a 087c
    adds r0,#0x1    @ 080bdb8c 0130
    strb r0,[r1,#0x10]                       @ 080bdb8e 0874
    movs r0,#0x0    @ 080bdb90 0020
    strb r0,[r1,#0x11]                       @ 080bdb92 4874
    b LAB_080bdaf4                           @ 080bdb94 aee7
    .zero  0x2
DAT_080bdb98:
    .word  0x098c9064                     @ 080bdb98 64908c09
DAT_080bdb9c:
    .word  gBannerState                   @ 080bdb9c c0fe0102
switchD_080bda92__caseD_1:
    ldrb r0,[r2,#0x10]                       @ 080bdba0 107c
    adds r0,#0x1    @ 080bdba2 0130
    strb r0,[r2,#0x10]                       @ 080bdba4 1074
    b LAB_080bdaf4                           @ 080bdba6 a5e7
LAB_080bdba8:
    bl disable_blend_and_clear_step          @ 080bdba8 37f014fd
    movs r0,#0x0    @ 080bdbac 0020
LAB_080bdbae:
    pop {r4,r5,r6}                           @ 080bdbae 70bc
    pop {r1}                                 @ 080bdbb0 02bc
    bx r1                                    @ 080bdbb2 0847

@ pack banner 子状态机 B, 驱动 pack banner 淡入/OAM 动画序列. 读 gBannerState[+0x10] (u8 phase [0..4]) 通过 switch-dispatch 5 cases 执行. case 0: 从 [gPrng+0x6c2c] 读出 player bit[4:0] 计算 tile VRAM 地址 0x06014000 偏移, copy_bytes_by_halfword 拷贝调色板 (src 0x098c9064 to 0x05000260, 0x20 halfwords), tile_2d_row_copy 写 VRAM, disable_blend_and_clear_step, 写 BLDCNT=0xbf40 / BLDALPHA=0, 清 gBannerState[+0x11], phase++. case 1: 直接 phase++. case 2: blend_palette_entry_toward_target (淡入, step=[+0x11]*2, max=0x20), OAM 2 entries loop (tile 0x40c0, x=0x4c, y 每次+0x40), 计时 0x1f 帧后 phase++. case 3: 计时后触发 sync_state_and_init_sprite (code=0x23) + phase++. case 4: 直接 phase++. 默认 (phase>4): disable_blend_and_clear_step 后返回 0. 返回 1=进行中 / 0=完成. Constants: gBannerState=0x0201fec0, BLDCNT=0x04000050, BLDALPHA=0x04000052, pal_src=0x098c9064, pal_dst=0x05000260, tile_vram=0x06014000, OAM_tile=0x40c0, OAM_attr=0xc0c0, x_base=0x4c.
tick_pack_banner_state_machine_b:
    push {r4,r5,r6,lr}                       @ 080bdbb4 70b5
    ldr r0, DAT_080bdbcc                     @ 080bdbb6 0548
    ldrb r1,[r0,#0x10]                       @ 080bdbb8 017c
    adds r2,r0,#0x0    @ 080bdbba 021c
    cmp r1,#0x4                              @ 080bdbbc 0429
    bls LAB_080bdbc2                         @ 080bdbbe 00d9
switchD_080bdbca__default:
    b LAB_080bdcf0                           @ 080bdbc0 96e0
LAB_080bdbc2:
    lsls r0,r1,#0x2    @ 080bdbc2 8800
    ldr r1, DAT_080bdbd0                     @ 080bdbc4 0249
    adds r0,r0,r1    @ 080bdbc6 4018
    ldr r0,[r0,#0x0]                         @ 080bdbc8 0068
switchD_080bdbca__switchD:
    .hword 0x4687    @ 080bdbca 8746
DAT_080bdbcc:
    .word  gBannerState                   @ 080bdbcc c0fe0102
DAT_080bdbd0:
    .word  0x080bdbd4                     @ 080bdbd0 d4db0b08
switchD_080bdbca__switchdataD_080bdbd4:
    .word  0x080bdbe8                     @ 080bdbd4 e8db0b08
    .word  0x080bdcdc                     @ 080bdbd8 dcdc0b08
    .word  0x080bdc54                     @ 080bdbdc 54dc0b08
    .word  0x080bdcdc                     @ 080bdbe0 dcdc0b08
    .word  0x080bdce8                     @ 080bdbe4 e8dc0b08
switchD_080bdbca__caseD_0:
    ldr r0, DAT_080bdc30                     @ 080bdbe8 1148
    ldr r1, DAT_080bdc34                     @ 080bdbea 1249
    adds r0,r0,r1    @ 080bdbec 4018
    ldrb r0,[r0,#0x0]                        @ 080bdbee 0078
    lsls r4,r0,#0x1d    @ 080bdbf0 4407
    lsrs r4,r4,#0x12    @ 080bdbf2 a40c
    ldr r0, DAT_080bdc38                     @ 080bdbf4 1048
    adds r4,r4,r0    @ 080bdbf6 2418
    ldr r0, DAT_080bdc3c                     @ 080bdbf8 1048
    ldr r1, DAT_080bdc40                     @ 080bdbfa 1149
    movs r2,#0x20    @ 080bdbfc 2022
    bl copy_bytes_by_halfword                @ 080bdbfe 37f051f9
    ldr r0, DAT_080bdc44                     @ 080bdc02 1048
    adds r1,r4,#0x0    @ 080bdc04 211c
    movs r2,#0x10    @ 080bdc06 1022
    movs r3,#0x4    @ 080bdc08 0423
    bl tile_2d_row_copy                      @ 080bdc0a 39f063fc
    bl disable_blend_and_clear_step          @ 080bdc0e 37f0e1fc
    ldr r1, PTR_BLDCNT_080bdc48              @ 080bdc12 0d49
    movs r2,#0xfd    @ 080bdc14 fd22
    lsls r2,r2,#0x6    @ 080bdc16 9201
    adds r0,r2,#0x0    @ 080bdc18 101c
    strh r0,[r1,#0x0]                        @ 080bdc1a 0880
    ldr r0, PTR_BLDALPHA_080bdc4c            @ 080bdc1c 0b48
    movs r1,#0x0    @ 080bdc1e 0021
    strh r1,[r0,#0x0]                        @ 080bdc20 0180
    ldr r0, DAT_080bdc50                     @ 080bdc22 0b48
    strb r1,[r0,#0x11]                       @ 080bdc24 4174
    ldrb r1,[r0,#0x10]                       @ 080bdc26 017c
    adds r1,#0x1    @ 080bdc28 0131
    strb r1,[r0,#0x10]                       @ 080bdc2a 0174
LAB_080bdc2c:
    movs r0,#0x1    @ 080bdc2c 0120
    b LAB_080bdcf6                           @ 080bdc2e 62e0
DAT_080bdc30:
    .word  0x02000000                     @ 080bdc30 00000002
DAT_080bdc34:
    .word  0x00006c2c                     @ 080bdc34 2c6c0000
DAT_080bdc38:
    .word  0x098c9084                     @ 080bdc38 84908c09
DAT_080bdc3c:
    .word  0x05000260                     @ 080bdc3c 60020005
DAT_080bdc40:
    .word  0x098c9064                     @ 080bdc40 64908c09
DAT_080bdc44:
    .word  0x06014000                     @ 080bdc44 00400106
PTR_BLDCNT_080bdc48:
    .word  BLDCNT                         @ 080bdc48 50000004
PTR_BLDALPHA_080bdc4c:
    .word  BLDALPHA                       @ 080bdc4c 52000004
DAT_080bdc50:
    .word  gBannerState                   @ 080bdc50 c0fe0102
switchD_080bdbca__caseD_2:
    ldrb r0,[r2,#0x11]                       @ 080bdc54 507c
    cmp r0,#0x10                             @ 080bdc56 1028
    bhi LAB_080bdc84                         @ 080bdc58 14d8
    cmp r0,#0x8                              @ 080bdc5a 0828
    bhi LAB_080bdc70                         @ 080bdc5c 08d8
    ldr r0, DAT_080bdc6c                     @ 080bdc5e 0348
    ldrb r2,[r2,#0x11]                       @ 080bdc60 527c
    lsls r2,r2,#0x1    @ 080bdc62 5200
    movs r1,#0x3    @ 080bdc64 0321
    bl blend_palette_entry_toward_target     @ 080bdc66 fef7bbfd
    b LAB_080bdc84                           @ 080bdc6a 0be0
DAT_080bdc6c:
    .word  0x098c9064                     @ 080bdc6c 64908c09
LAB_080bdc70:
    ldr r0, DAT_080bdcd0                     @ 080bdc70 1748
    ldrb r2,[r2,#0x11]                       @ 080bdc72 527c
    lsls r1,r2,#0x1    @ 080bdc74 5100
    movs r2,#0x20    @ 080bdc76 2022
    subs r2,r2,r1    @ 080bdc78 521a
    lsls r2,r2,#0x10    @ 080bdc7a 1204
    lsrs r2,r2,#0x10    @ 080bdc7c 120c
    movs r1,#0x3    @ 080bdc7e 0321
    bl blend_palette_entry_toward_target     @ 080bdc80 fef7aefd
LAB_080bdc84:
    movs r5,#0x0    @ 080bdc84 0025
    movs r0,#0x38    @ 080bdc86 3820
    lsls r6,r0,#0x10    @ 080bdc88 0604
    movs r4,#0x4c    @ 080bdc8a 4c24
LAB_080bdc8c:
    adds r0,r4,#0x0    @ 080bdc8c 201c
    orrs r0,r6    @ 080bdc8e 3043
    lsls r2,r5,#0x3    @ 080bdc90 ea00
    movs r3,#0x80    @ 080bdc92 8023
    lsls r3,r3,#0x2    @ 080bdc94 9b00
    adds r2,r2,r3    @ 080bdc96 d218
    movs r3,#0xc0    @ 080bdc98 c023
    lsls r3,r3,#0x6    @ 080bdc9a 9b01
    adds r1,r3,#0x0    @ 080bdc9c 191c
    orrs r2,r1    @ 080bdc9e 0a43
    lsls r2,r2,#0x10    @ 080bdca0 1204
    lsrs r2,r2,#0x10    @ 080bdca2 120c
    ldr r1, DAT_080bdcd4                     @ 080bdca4 0b49
    bl write_oam_entry_from_packed_args      @ 080bdca6 38f061fa
    adds r4,#0x40    @ 080bdcaa 4034
    adds r5,#0x1    @ 080bdcac 0135
    cmp r5,#0x1                              @ 080bdcae 012d
    ble LAB_080bdc8c                         @ 080bdcb0 ecdd
    ldr r1, DAT_080bdcd8                     @ 080bdcb2 0949
    ldrb r0,[r1,#0x11]                       @ 080bdcb4 487c
    adds r0,#0x1    @ 080bdcb6 0130
    strb r0,[r1,#0x11]                       @ 080bdcb8 4874
    lsls r0,r0,#0x18    @ 080bdcba 0006
    lsrs r0,r0,#0x18    @ 080bdcbc 000e
    cmp r0,#0x1f                             @ 080bdcbe 1f28
    bls LAB_080bdc2c                         @ 080bdcc0 b4d9
    ldrb r0,[r1,#0x10]                       @ 080bdcc2 087c
    adds r0,#0x1    @ 080bdcc4 0130
    strb r0,[r1,#0x10]                       @ 080bdcc6 0874
    movs r0,#0x0    @ 080bdcc8 0020
    strb r0,[r1,#0x11]                       @ 080bdcca 4874
    b LAB_080bdc2c                           @ 080bdccc aee7
    .zero  0x2
DAT_080bdcd0:
    .word  0x098c9064                     @ 080bdcd0 64908c09
DAT_080bdcd4:
    .word  0x000040c0                     @ 080bdcd4 c0400000
DAT_080bdcd8:
    .word  gBannerState                   @ 080bdcd8 c0fe0102
switchD_080bdbca__caseD_1:
    ldrb r0,[r2,#0x10]                       @ 080bdcdc 107c
    adds r0,#0x1    @ 080bdcde 0130
    movs r1,#0x0    @ 080bdce0 0021
    strb r0,[r2,#0x10]                       @ 080bdce2 1074
    strb r1,[r2,#0x11]                       @ 080bdce4 5174
    b LAB_080bdc2c                           @ 080bdce6 a1e7
switchD_080bdbca__caseD_4:
    ldrb r0,[r2,#0x10]                       @ 080bdce8 107c
    adds r0,#0x1    @ 080bdcea 0130
    strb r0,[r2,#0x10]                       @ 080bdcec 1074
    b LAB_080bdc2c                           @ 080bdcee 9de7
LAB_080bdcf0:
    bl disable_blend_and_clear_step          @ 080bdcf0 37f070fc
    movs r0,#0x0    @ 080bdcf4 0020
LAB_080bdcf6:
    pop {r4,r5,r6}                           @ 080bdcf6 70bc
    pop {r1}                                 @ 080bdcf8 02bc
    bx r1                                    @ 080bdcfa 0847

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x04 子状态机, 待详细分析.
play_ui_effect_04:
    push {r4,r5,r6,r7,lr}                    @ 080bdcfc f0b5
    .hword 0x4647    @ 080bdcfe 4746
    push {r7}                                @ 080bdd00 80b4
    ldr r0, DAT_080bdd1c                     @ 080bdd02 0648
    ldrh r2,[r0,#0x8]                        @ 080bdd04 0289
    ldrb r1,[r0,#0x10]                       @ 080bdd06 017c
    adds r4,r0,#0x0    @ 080bdd08 041c
    cmp r1,#0x5                              @ 080bdd0a 0529
    bls LAB_080bdd10                         @ 080bdd0c 00d9
switchD_080bdd18__default:
    b LAB_080bdf30                           @ 080bdd0e 0fe1
LAB_080bdd10:
    lsls r0,r1,#0x2    @ 080bdd10 8800
    ldr r1, DAT_080bdd20                     @ 080bdd12 0349
    adds r0,r0,r1    @ 080bdd14 4018
    ldr r0,[r0,#0x0]                         @ 080bdd16 0068
switchD_080bdd18__switchD:
    .hword 0x4687    @ 080bdd18 8746
    .zero  0x2
DAT_080bdd1c:
    .word  gBannerState                   @ 080bdd1c c0fe0102
DAT_080bdd20:
    .word  0x080bdd24                     @ 080bdd20 24dd0b08
switchD_080bdd18__switchdataD_080bdd24:
    .word  0x080bdd3c                     @ 080bdd24 3cdd0b08
    .word  0x080bdde4                     @ 080bdd28 e4dd0b08
    .word  0x080bddf8                     @ 080bdd2c f8dd0b08
    .word  0x080bde34                     @ 080bdd30 34de0b08
    .word  0x080bded4                     @ 080bdd34 d4de0b08
    .word  0x080bdf0c                     @ 080bdd38 0cdf0b08
switchD_080bdd18__caseD_0:
    ldr r0, DAT_080bddb8                     @ 080bdd3c 1e48
    ldr r1, DAT_080bddbc                     @ 080bdd3e 1f49
    adds r0,r0,r1    @ 080bdd40 4018
    ldrb r0,[r0,#0x0]                        @ 080bdd42 0078
    lsls r0,r0,#0x1d    @ 080bdd44 4007
    lsrs r0,r0,#0x1d    @ 080bdd46 400f
    lsls r4,r0,#0x3    @ 080bdd48 c400
    adds r4,r4,r0    @ 080bdd4a 2418
    lsls r4,r4,#0xb    @ 080bdd4c e402
    lsls r0,r2,#0x1    @ 080bdd4e 5000
    adds r0,r0,r2    @ 080bdd50 8018
    lsls r0,r0,#0xa    @ 080bdd52 8002
    ldr r1, DAT_080bddc0                     @ 080bdd54 1a49
    adds r0,r0,r1    @ 080bdd56 4018
    adds r4,r4,r0    @ 080bdd58 2418
    ldr r0, DAT_080bddc4                     @ 080bdd5a 1a48
    ldr r1, DAT_080bddc8                     @ 080bdd5c 1a49
    movs r2,#0x20    @ 080bdd5e 2022
    bl copy_bytes_by_halfword                @ 080bdd60 37f0a0f8
    ldr r0, DAT_080bddcc                     @ 080bdd64 1948
    adds r1,r4,#0x0    @ 080bdd66 211c
    movs r2,#0x18    @ 080bdd68 1822
    movs r3,#0x4    @ 080bdd6a 0423
    bl tile_2d_row_copy                      @ 080bdd6c 39f0b2fb
    bl disable_blend_and_clear_step          @ 080bdd70 37f030fc
    ldr r1, PTR_WIN0H_080bddd0               @ 080bdd74 1649
    ldr r2, DAT_080bddd4                     @ 080bdd76 174a
    adds r0,r2,#0x0    @ 080bdd78 101c
    strh r0,[r1,#0x0]                        @ 080bdd7a 0880
    adds r1,#0x4    @ 080bdd7c 0431
    ldr r3, DAT_080bddd8                     @ 080bdd7e 164b
    adds r0,r3,#0x0    @ 080bdd80 181c
    strh r0,[r1,#0x0]                        @ 080bdd82 0880
    adds r1,#0x4    @ 080bdd84 0431
    movs r0,#0x3f    @ 080bdd86 3f20
    strh r0,[r1,#0x0]                        @ 080bdd88 0880
    adds r1,#0x2    @ 080bdd8a 0231
    movs r0,#0x1f    @ 080bdd8c 1f20
    strh r0,[r1,#0x0]                        @ 080bdd8e 0880
    movs r2,#0x80    @ 080bdd90 8022
    lsls r2,r2,#0x13    @ 080bdd92 d204
    ldrh r0,[r2,#0x0]                        @ 080bdd94 1088
    movs r3,#0x80    @ 080bdd96 8023
    lsls r3,r3,#0x6    @ 080bdd98 9b01
    adds r1,r3,#0x0    @ 080bdd9a 191c
    orrs r0,r1    @ 080bdd9c 0843
    strh r0,[r2,#0x0]                        @ 080bdd9e 1080
    ldrh r1,[r2,#0x0]                        @ 080bdda0 1188
    ldr r0, DAT_080bdddc                     @ 080bdda2 0e48
    ands r0,r1    @ 080bdda4 0840
    strh r0,[r2,#0x0]                        @ 080bdda6 1080
    ldr r0, DAT_080bdde0                     @ 080bdda8 0d48
    movs r1,#0x0    @ 080bddaa 0021
    strb r1,[r0,#0x11]                       @ 080bddac 4174
    ldrb r1,[r0,#0x10]                       @ 080bddae 017c
    adds r1,#0x1    @ 080bddb0 0131
    strb r1,[r0,#0x10]                       @ 080bddb2 0174
LAB_080bddb4:
    movs r0,#0x1    @ 080bddb4 0120
    b LAB_080bdf94                           @ 080bddb6 ede0
DAT_080bddb8:
    .word  0x02000000                     @ 080bddb8 00000002
DAT_080bddbc:
    .word  0x00006c2c                     @ 080bddbc 2c6c0000
DAT_080bddc0:
    .word  0x098ae064                     @ 080bddc0 64e08a09
DAT_080bddc4:
    .word  0x05000260                     @ 080bddc4 60020005
DAT_080bddc8:
    .word  0x098ae044                     @ 080bddc8 44e08a09
DAT_080bddcc:
    .word  0x06014000                     @ 080bddcc 00400106
PTR_WIN0H_080bddd0:
    .word  WIN0H                          @ 080bddd0 40000004
DAT_080bddd4:
    .word  0x000028f0                     @ 080bddd4 f0280000
DAT_080bddd8:
    .word  0x00004848                     @ 080bddd8 48480000
DAT_080bdddc:
    .word  0x00003fff                     @ 080bdddc ff3f0000
DAT_080bdde0:
    .word  gBannerState                   @ 080bdde0 c0fe0102
switchD_080bdd18__caseD_1:
    ldr r1, PTR_BLDCNT_080bddf4              @ 080bdde4 0349
    movs r0,#0xef    @ 080bdde6 ef20
    strh r0,[r1,#0x0]                        @ 080bdde8 0880
    adds r1,#0x4    @ 080bddea 0431
    movs r0,#0x8    @ 080bddec 0820
    strh r0,[r1,#0x0]                        @ 080bddee 0880
    b LAB_080bdf00                           @ 080bddf0 86e0
    .zero  0x2
PTR_BLDCNT_080bddf4:
    .word  BLDCNT                         @ 080bddf4 50000004
switchD_080bdd18__caseD_2:
    ldr r3, PTR_WIN0V_080bde30               @ 080bddf8 0d4b
    ldrb r0,[r4,#0x11]                       @ 080bddfa 607c
    lsls r2,r0,#0x1    @ 080bddfc 4200
    adds r2,r2,r0    @ 080bddfe 1218
    lsls r2,r2,#0x1    @ 080bde00 5200
    adds r1,r2,#0x0    @ 080bde02 111c
    adds r1,#0x48    @ 080bde04 4831
    lsls r1,r1,#0x18    @ 080bde06 0906
    lsrs r1,r1,#0x18    @ 080bde08 090e
    movs r0,#0x48    @ 080bde0a 4820
    subs r0,r0,r2    @ 080bde0c 801a
    lsls r0,r0,#0x18    @ 080bde0e 0006
    lsrs r0,r0,#0x10    @ 080bde10 000c
    orrs r1,r0    @ 080bde12 0143
    strh r1,[r3,#0x0]                        @ 080bde14 1980
    ldrb r0,[r4,#0x11]                       @ 080bde16 607c
    adds r0,#0x1    @ 080bde18 0130
    strb r0,[r4,#0x11]                       @ 080bde1a 6074
    lsls r0,r0,#0x18    @ 080bde1c 0006
    lsrs r0,r0,#0x18    @ 080bde1e 000e
    cmp r0,#0x4                              @ 080bde20 0428
    bls LAB_080bddb4                         @ 080bde22 c7d9
    ldrb r0,[r4,#0x10]                       @ 080bde24 207c
    adds r0,#0x1    @ 080bde26 0130
    strb r0,[r4,#0x10]                       @ 080bde28 2074
    movs r0,#0x0    @ 080bde2a 0020
    strb r0,[r4,#0x11]                       @ 080bde2c 6074
    b LAB_080bddb4                           @ 080bde2e c1e7
PTR_WIN0V_080bde30:
    .word  WIN0V                          @ 080bde30 44000004
switchD_080bdd18__caseD_3:
    ldrb r0,[r4,#0x11]                       @ 080bde34 607c
    cmp r0,#0x10                             @ 080bde36 1028
    bhi LAB_080bde64                         @ 080bde38 14d8
    cmp r0,#0x8                              @ 080bde3a 0828
    bhi LAB_080bde50                         @ 080bde3c 08d8
    ldr r0, DAT_080bde4c                     @ 080bde3e 0348
    ldrb r4,[r4,#0x11]                       @ 080bde40 647c
    lsls r2,r4,#0x1    @ 080bde42 6200
    movs r1,#0x3    @ 080bde44 0321
    bl blend_palette_entry_toward_target     @ 080bde46 fef7cbfc
    b LAB_080bde64                           @ 080bde4a 0be0
DAT_080bde4c:
    .word  0x098ae044                     @ 080bde4c 44e08a09
LAB_080bde50:
    ldr r0, DAT_080bdec4                     @ 080bde50 1c48
    ldrb r4,[r4,#0x11]                       @ 080bde52 647c
    lsls r1,r4,#0x1    @ 080bde54 6100
    movs r2,#0x20    @ 080bde56 2022
    subs r2,r2,r1    @ 080bde58 521a
    lsls r2,r2,#0x10    @ 080bde5a 1204
    lsrs r2,r2,#0x10    @ 080bde5c 120c
    movs r1,#0x3    @ 080bde5e 0321
    bl blend_palette_entry_toward_target     @ 080bde60 fef7befc
LAB_080bde64:
    movs r7,#0x0    @ 080bde64 0027
    movs r0,#0x38    @ 080bde66 3820
    lsls r0,r0,#0x10    @ 080bde68 0004
    .hword 0x4680    @ 080bde6a 8046
    movs r6,#0x2c    @ 080bde6c 2c26
LAB_080bde6e:
    adds r5,r6,#0x0    @ 080bde6e 351c
    .hword 0x4641    @ 080bde70 4146
    orrs r5,r1    @ 080bde72 0d43
    lsls r4,r7,#0x3    @ 080bde74 fc00
    movs r2,#0x80    @ 080bde76 8022
    lsls r2,r2,#0x2    @ 080bde78 9200
    adds r4,r4,r2    @ 080bde7a a418
    movs r3,#0xc0    @ 080bde7c c023
    lsls r3,r3,#0x6    @ 080bde7e 9b01
    adds r0,r3,#0x0    @ 080bde80 181c
    orrs r4,r0    @ 080bde82 0443
    lsls r4,r4,#0x10    @ 080bde84 2404
    lsrs r4,r4,#0x10    @ 080bde86 240c
    adds r0,r5,#0x0    @ 080bde88 281c
    ldr r1, DAT_080bdec8                     @ 080bde8a 0f49
    adds r2,r4,#0x0    @ 080bde8c 221c
    bl write_oam_entry_from_packed_args      @ 080bde8e 38f06df9
    adds r0,r5,#0x0    @ 080bde92 281c
    ldr r1, DAT_080bdecc                     @ 080bde94 0d49
    adds r2,r4,#0x0    @ 080bde96 221c
    bl write_oam_entry_from_packed_args      @ 080bde98 38f068f9
    adds r6,#0x40    @ 080bde9c 4036
    adds r7,#0x1    @ 080bde9e 0137
    cmp r7,#0x2                              @ 080bdea0 022f
    ble LAB_080bde6e                         @ 080bdea2 e4dd
    ldr r1, DAT_080bded0                     @ 080bdea4 0a49
    ldrb r0,[r1,#0x11]                       @ 080bdea6 487c
    adds r0,#0x1    @ 080bdea8 0130
    strb r0,[r1,#0x11]                       @ 080bdeaa 4874
    lsls r0,r0,#0x18    @ 080bdeac 0006
    lsrs r0,r0,#0x18    @ 080bdeae 000e
    cmp r0,#0x1f                             @ 080bdeb0 1f28
    bhi LAB_080bdeb6                         @ 080bdeb2 00d8
    b LAB_080bddb4                           @ 080bdeb4 7ee7
LAB_080bdeb6:
    ldrb r0,[r1,#0x10]                       @ 080bdeb6 087c
    adds r0,#0x1    @ 080bdeb8 0130
    strb r0,[r1,#0x10]                       @ 080bdeba 0874
    movs r0,#0x0    @ 080bdebc 0020
    strb r0,[r1,#0x11]                       @ 080bdebe 4874
    b LAB_080bddb4                           @ 080bdec0 78e7
    .zero  0x2
DAT_080bdec4:
    .word  0x098ae044                     @ 080bdec4 44e08a09
DAT_080bdec8:
    .word  0x000048c0                     @ 080bdec8 c0480000
DAT_080bdecc:
    .word  0x000040c0                     @ 080bdecc c0400000
DAT_080bded0:
    .word  gBannerState                   @ 080bded0 c0fe0102
switchD_080bdd18__caseD_4:
    ldr r2, PTR_WIN0V_080bdf08               @ 080bded4 0c4a
    ldrb r1,[r4,#0x11]                       @ 080bded6 617c
    lsls r0,r1,#0x1    @ 080bded8 4800
    adds r0,r0,r1    @ 080bdeda 4018
    lsls r0,r0,#0x1    @ 080bdedc 4000
    movs r1,#0x60    @ 080bdede 6021
    subs r1,r1,r0    @ 080bdee0 091a
    lsls r1,r1,#0x18    @ 080bdee2 0906
    lsrs r1,r1,#0x18    @ 080bdee4 090e
    adds r0,#0x30    @ 080bdee6 3030
    lsls r0,r0,#0x18    @ 080bdee8 0006
    lsrs r0,r0,#0x10    @ 080bdeea 000c
    orrs r1,r0    @ 080bdeec 0143
    strh r1,[r2,#0x0]                        @ 080bdeee 1180
    ldrb r0,[r4,#0x11]                       @ 080bdef0 607c
    adds r0,#0x1    @ 080bdef2 0130
    strb r0,[r4,#0x11]                       @ 080bdef4 6074
    lsls r0,r0,#0x18    @ 080bdef6 0006
    lsrs r0,r0,#0x18    @ 080bdef8 000e
    cmp r0,#0x4                              @ 080bdefa 0428
    bhi LAB_080bdf00                         @ 080bdefc 00d8
    b LAB_080bddb4                           @ 080bdefe 59e7
LAB_080bdf00:
    ldrb r0,[r4,#0x10]                       @ 080bdf00 207c
    adds r0,#0x1    @ 080bdf02 0130
    strb r0,[r4,#0x10]                       @ 080bdf04 2074
    b LAB_080bddb4                           @ 080bdf06 55e7
PTR_WIN0V_080bdf08:
    .word  WIN0V                          @ 080bdf08 44000004
switchD_080bdd18__caseD_5:
    bl disable_blend_and_clear_step          @ 080bdf0c 37f062fb
    movs r2,#0x80    @ 080bdf10 8022
    lsls r2,r2,#0x13    @ 080bdf12 d204
    ldrh r1,[r2,#0x0]                        @ 080bdf14 1188
    ldr r0, DAT_080bdf28                     @ 080bdf16 0448
    ands r0,r1    @ 080bdf18 0840
    strh r0,[r2,#0x0]                        @ 080bdf1a 1080
    ldr r1, DAT_080bdf2c                     @ 080bdf1c 0349
    ldrb r0,[r1,#0x10]                       @ 080bdf1e 087c
    adds r0,#0x1    @ 080bdf20 0130
    strb r0,[r1,#0x10]                       @ 080bdf22 0874
    b LAB_080bddb4                           @ 080bdf24 46e7
    .zero  0x2
DAT_080bdf28:
    .word  0x0000dfff                     @ 080bdf28 ffdf0000
DAT_080bdf2c:
    .word  gBannerState                   @ 080bdf2c c0fe0102
LAB_080bdf30:
    cmp r2,#0x0                              @ 080bdf30 002a
    bne LAB_080bdf6c                         @ 080bdf32 1bd1
    ldr r3, PTR_gP1LifePoints_080bdf5c       @ 080bdf34 094b
    ldr r2, DAT_080bdf60                     @ 080bdf36 0a4a
    adds r0,r3,r2    @ 080bdf38 9818
    ldr r1, DAT_080bdf64                     @ 080bdf3a 0a49
    ldr r2,[r0,#0x0]                         @ 080bdf3c 0268
    ldr r0,[r1,#0x4]                         @ 080bdf3e 4868
    cmp r2,r0                                @ 080bdf40 8242
    bne LAB_080bdf6c                         @ 080bdf42 13d1
    movs r1,#0xe8    @ 080bdf44 e821
    lsls r1,r1,#0x5    @ 080bdf46 4901
    adds r0,r3,r1    @ 080bdf48 5818
    ldr r0,[r0,#0x0]                         @ 080bdf4a 0068
    cmp r0,#0x0                              @ 080bdf4c 0028
    bne LAB_080bdf6c                         @ 080bdf4e 0dd1
    ldr r1, DAT_080bdf68                     @ 080bdf50 0549
    movs r0,#0x8    @ 080bdf52 0820
    ldrb r2,[r1,#0x0]                        @ 080bdf54 0a78
    orrs r0,r2    @ 080bdf56 1043
    b LAB_080bdf76                           @ 080bdf58 0de0
    .zero  0x2
PTR_gP1LifePoints_080bdf5c:
    .word  gP1LifePoints                  @ 080bdf5c e0c40102
DAT_080bdf60:
    .word  0x00001ce8                     @ 080bdf60 e81c0000
DAT_080bdf64:
    .word  0x0201e2a0                     @ 080bdf64 a0e20102
DAT_080bdf68:
    .word  0x0201ff30                     @ 080bdf68 30ff0102
LAB_080bdf6c:
    ldr r1, DAT_080bdfa0                     @ 080bdf6c 0c49
    movs r0,#0x9    @ 080bdf6e 0920
    rsbs r0,r0,#0    @ 080bdf70 4042
    ldrb r3,[r1,#0x0]                        @ 080bdf72 0b78
    ands r0,r3    @ 080bdf74 1840
LAB_080bdf76:
    strb r0,[r1,#0x0]                        @ 080bdf76 0870
    movs r0,#0x2    @ 080bdf78 0220
    rsbs r0,r0,#0    @ 080bdf7a 4042
    ldrb r1,[r4,#0x0]                        @ 080bdf7c 2178
    ands r0,r1    @ 080bdf7e 0840
    strb r0,[r4,#0x0]                        @ 080bdf80 2070
    ldr r1, DAT_080bdfa4                     @ 080bdf82 0849
    ldr r2, DAT_080bdfa8                     @ 080bdf84 084a
    adds r1,r1,r2    @ 080bdf86 8918
    movs r0,#0x5    @ 080bdf88 0520
    rsbs r0,r0,#0    @ 080bdf8a 4042
    ldrb r3,[r1,#0x0]                        @ 080bdf8c 0b78
    ands r0,r3    @ 080bdf8e 1840
    strb r0,[r1,#0x0]                        @ 080bdf90 0870
    movs r0,#0x0    @ 080bdf92 0020
LAB_080bdf94:
    pop {r3}                                 @ 080bdf94 08bc
    .hword 0x4698    @ 080bdf96 9846
    pop {r4,r5,r6,r7}                        @ 080bdf98 f0bc
    pop {r1}                                 @ 080bdf9a 02bc
    bx r1                                    @ 080bdf9c 0847
    .zero  0x2
DAT_080bdfa0:
    .word  0x0201ff30                     @ 080bdfa0 30ff0102
DAT_080bdfa4:
    .word  0x02023130                     @ 080bdfa4 30310202
DAT_080bdfa8:
    .word  0x00000215                     @ 080bdfa8 15020000

@ banner 出/入场动画状态机 (7-state on [gBannerState+0x10]); 阶段: 0=init (载 palette/tiles, 启 BG3), 1-2=fade-in (BLDY 渐增 7+64f), 3-5=fade-out (BLDY 渐减 + 文本切换 8+64+8f), 6=teardown (关 BG3); sub-counter 在 [gBannerState+0x11]; 返回 1=busy / 0=done. 唯一 caller: play_ui_effect (FUN_0801ef94) case 1 (effect_id=1).
banner_anim_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 080bdfac f0b5
    .hword 0x4657    @ 080bdfae 5746
    .hword 0x464e    @ 080bdfb0 4e46
    .hword 0x4645    @ 080bdfb2 4546
    push {r5,r6,r7}                          @ 080bdfb4 e0b4
    sub sp,#0x8                              @ 080bdfb6 82b0
    ldr r5, DAT_080bdfd0                     @ 080bdfb8 054d  -- r5 = &gBannerState (0x0201FEC0)
    ldrb r0,[r5,#0x10]                       @ 080bdfba 287c  -- r0 = main state (gBannerState[+0x10])
    adds r3,r5,#0x0    @ 080bdfbc 2b1c
    cmp r0,#0x6                              @ 080bdfbe 0628  -- state > 6 -> default (DONE cleanup, return 0)
    bls LAB_080bdfc4                         @ 080bdfc0 00d9
switchD_080bdfcc__default:
    b LAB_080be5bc                           @ 080bdfc2 fbe2
LAB_080bdfc4:
    lsls r0,r0,#0x2    @ 080bdfc4 8000
    ldr r1, DAT_080bdfd4                     @ 080bdfc6 0349
    adds r0,r0,r1    @ 080bdfc8 4018
    ldr r0,[r0,#0x0]                         @ 080bdfca 0068  -- switch dispatch: pc = jump_table[state] (table @ 0x080bdfd8)
switchD_080bdfcc__switchD:
    .hword 0x4687    @ 080bdfcc 8746
    .zero  0x2
DAT_080bdfd0:
    .word  gBannerState                   @ 080bdfd0 c0fe0102
DAT_080bdfd4:
    .word  0x080bdfd8                     @ 080bdfd4 d8df0b08
switchD_080bdfcc__switchdataD_080bdfd8:
    .word  0x080bdff4                     @ 080bdfd8 f4df0b08
    .word  0x080be130                     @ 080bdfdc 30e10b08
    .word  0x080be204                     @ 080bdfe0 04e20b08
    .word  0x080be26c                     @ 080bdfe4 6ce20b08
    .word  0x080be404                     @ 080bdfe8 04e40b08
    .word  0x080be4a0                     @ 080bdfec a0e40b08
    .word  0x080be598                     @ 080bdff0 98e50b08
switchD_080bdfcc__caseD_0:
    ldr r0, DAT_080be06c                     @ 080bdff4 1d48  -- case 0 INIT (1 帧): 载 banner palette/tile (lang-dep, gSettings 低3bit), 设 WINOUT, 启 BG3
    ldr r1, DAT_080be070                     @ 080bdff6 1e49
    movs r2,#0x20    @ 080bdff8 2022
    bl copy_bytes_by_halfword                @ 080bdffa 36f053ff
    ldr r1, DAT_080be074                     @ 080bdffe 1d49
    adds r1,#0x36    @ 080be000 3631
    movs r0,#0x40    @ 080be002 4020
    ldrb r1,[r1,#0x0]                        @ 080be004 0978
    ands r0,r1    @ 080be006 0840
    cmp r0,#0x0                              @ 080be008 0028
    bne LAB_080be094                         @ 080be00a 43d1
    ldr r0, DAT_080be078                     @ 080be00c 1a48
    ldr r4, DAT_080be07c                     @ 080be00e 1b4c
    ldr r1, DAT_080be080                     @ 080be010 1b49
    adds r4,r4,r1    @ 080be012 6418
    ldrb r3,[r4,#0x0]                        @ 080be014 2378
    lsls r2,r3,#0x1d    @ 080be016 5a07
    lsrs r2,r2,#0x1d    @ 080be018 520f
    lsls r1,r2,#0x3    @ 080be01a d100
    adds r1,r1,r2    @ 080be01c 8918
    lsls r1,r1,#0xb    @ 080be01e c902
    ldr r5, DAT_080be084                     @ 080be020 184d
    adds r1,r1,r5    @ 080be022 4919
    movs r2,#0x18    @ 080be024 1822
    movs r3,#0x4    @ 080be026 0423
    bl tile_2d_row_copy                      @ 080be028 39f054fa
    ldr r0, DAT_080be088                     @ 080be02c 1648
    ldr r1, PTR_gPrng_080be08c               @ 080be02e 1749
    ldr r3, DAT_080be090                     @ 080be030 174b
    adds r2,r1,r3    @ 080be032 ca18
    ldrb r2,[r2,#0x0]                        @ 080be034 1278
    lsrs r3,r2,#0x1    @ 080be036 5308
    movs r2,#0x90    @ 080be038 9022
    lsls r2,r2,#0x2    @ 080be03a 9200
    adds r1,r1,r2    @ 080be03c 8918
    movs r2,#0x1    @ 080be03e 0122
    ldrb r1,[r1,#0x0]                        @ 080be040 0978
    ands r2,r1    @ 080be042 0a40
    lsls r2,r2,#0x7    @ 080be044 d201
    orrs r2,r3    @ 080be046 1a43
    adds r2,#0x1    @ 080be048 0132
    lsls r1,r2,#0x1    @ 080be04a 5100
    adds r1,r1,r2    @ 080be04c 8918
    lsls r1,r1,#0xa    @ 080be04e 8902
    ldrb r4,[r4,#0x0]                        @ 080be050 2478
    lsls r3,r4,#0x1d    @ 080be052 6307
    lsrs r3,r3,#0x1d    @ 080be054 5b0f
    lsls r2,r3,#0x3    @ 080be056 da00
    adds r2,r2,r3    @ 080be058 d218
    lsls r2,r2,#0xb    @ 080be05a d202
    adds r2,r2,r5    @ 080be05c 5219
    adds r1,r1,r2    @ 080be05e 8918
    movs r2,#0x18    @ 080be060 1822
    movs r3,#0x4    @ 080be062 0423
    bl tile_2d_row_copy                      @ 080be064 39f036fa
    b LAB_080be0b4                           @ 080be068 24e0
    .zero  0x2
DAT_080be06c:
    .word  0x05000260                     @ 080be06c 60020005
DAT_080be070:
    .word  0x0992069c                     @ 080be070 9c069209
DAT_080be074:
    .word  0x02023360                     @ 080be074 60330202
DAT_080be078:
    .word  0x06014000                     @ 080be078 00400106
DAT_080be07c:
    .word  0x02000000                     @ 080be07c 00000002
DAT_080be080:
    .word  0x00006c2c                     @ 080be080 2c6c0000
DAT_080be084:
    .word  0x099206bc                     @ 080be084 bc069209
DAT_080be088:
    .word  0x06015000                     @ 080be088 00500106
PTR_gPrng_080be08c:
    .word  gPrng                          @ 080be08c 40000003
DAT_080be090:
    .word  0x0000023f                     @ 080be090 3f020000
LAB_080be094:
    ldr r0, DAT_080be108                     @ 080be094 1c48
    ldr r1, DAT_080be10c                     @ 080be096 1d49
    ldr r3, DAT_080be110                     @ 080be098 1d4b
    adds r1,r1,r3    @ 080be09a c918
    ldrb r1,[r1,#0x0]                        @ 080be09c 0978
    lsls r2,r1,#0x1d    @ 080be09e 4a07
    lsrs r2,r2,#0x1d    @ 080be0a0 520f
    lsls r1,r2,#0x3    @ 080be0a2 d100
    adds r1,r1,r2    @ 080be0a4 8918
    lsls r1,r1,#0xb    @ 080be0a6 c902
    ldr r2, DAT_080be114                     @ 080be0a8 1a4a
    adds r1,r1,r2    @ 080be0aa 8918
    movs r2,#0x18    @ 080be0ac 1822
    movs r3,#0x8    @ 080be0ae 0823
    bl tile_2d_row_copy                      @ 080be0b0 39f010fa
LAB_080be0b4:
    ldr r0, DAT_080be118                     @ 080be0b4 1848
    ldr r1, DAT_080be11c                     @ 080be0b6 1949
    movs r2,#0x20    @ 080be0b8 2022
    bl copy_bytes_by_halfword                @ 080be0ba 36f0f3fe
    ldr r0, DAT_080be120                     @ 080be0be 1848
    ldr r1, DAT_080be10c                     @ 080be0c0 1249
    ldr r2, DAT_080be110                     @ 080be0c2 134a
    adds r1,r1,r2    @ 080be0c4 8918
    ldrb r1,[r1,#0x0]                        @ 080be0c6 0978
    lsls r2,r1,#0x1d    @ 080be0c8 4a07
    lsrs r2,r2,#0x1d    @ 080be0ca 520f
    lsls r1,r2,#0x1    @ 080be0cc 5100
    adds r1,r1,r2    @ 080be0ce 8918
    lsls r1,r1,#0xb    @ 080be0d0 c902
    ldr r2, DAT_080be124                     @ 080be0d2 144a
    adds r1,r1,r2    @ 080be0d4 8918
    movs r2,#0x18    @ 080be0d6 1822
    movs r3,#0x8    @ 080be0d8 0823
    bl tile_2d_row_copy                      @ 080be0da 39f0fbf9
    bl disable_blend_and_clear_step          @ 080be0de 37f079fa
    ldr r1, PTR_WINOUT_080be128              @ 080be0e2 1149
    ldr r3, DAT_080be12c                     @ 080be0e4 114b
    adds r0,r3,#0x0    @ 080be0e6 181c
    strh r0,[r1,#0x0]                        @ 080be0e8 0880
    adds r1,#0xa    @ 080be0ea 0a31
    movs r0,#0x0    @ 080be0ec 0020
    strh r0,[r1,#0x0]                        @ 080be0ee 0880
    subs r1,#0x4    @ 080be0f0 0439
    movs r0,#0xff    @ 080be0f2 ff20
    strh r0,[r1,#0x0]                        @ 080be0f4 0880
    movs r2,#0x80    @ 080be0f6 8022
    lsls r2,r2,#0x13    @ 080be0f8 d204
    ldrh r0,[r2,#0x0]                        @ 080be0fa 1088
    movs r3,#0x80    @ 080be0fc 8023
    lsls r3,r3,#0x8    @ 080be0fe 1b02
    adds r1,r3,#0x0    @ 080be100 191c
    orrs r0,r1    @ 080be102 0843
    b LAB_080be5a6                           @ 080be104 4fe2
    .zero  0x2
DAT_080be108:
    .word  0x06014000                     @ 080be108 00400106
DAT_080be10c:
    .word  0x02000000                     @ 080be10c 00000002
DAT_080be110:
    .word  0x00006c2c                     @ 080be110 2c6c0000
DAT_080be114:
    .word  0x099236bc                     @ 080be114 bc369209
DAT_080be118:
    .word  0x05000280                     @ 080be118 80020005
DAT_080be11c:
    .word  0x098a5024                     @ 080be11c 24508a09
DAT_080be120:
    .word  0x06016000                     @ 080be120 00600106
DAT_080be124:
    .word  0x098a5044                     @ 080be124 44508a09
PTR_WINOUT_080be128:
    .word  WINOUT                         @ 080be128 4a000004
DAT_080be12c:
    .word  0x00001f3f                     @ 080be12c 3f1f0000
switchD_080bdfcc__caseD_1:
    movs r0,#0xe    @ 080be130 0e20  -- case 1 FADE_IN_A (7 帧): 3行x4次 FUN_080f616c, 末尾 BLDY = sub-counter
    .hword 0x4681    @ 080be132 8146
    movs r1,#0x0    @ 080be134 0021
    .hword 0x4688    @ 080be136 8846
    ldr r7, DAT_080be1f4                     @ 080be138 2e4f
    movs r6,#0x18    @ 080be13a 1826
    ldr r2, DAT_080be1f8                     @ 080be13c 2e4a
    .hword 0x4692    @ 080be13e 9246
LAB_080be140:
    ldrb r3,[r7,#0x11]                       @ 080be140 7b7c
    .hword 0x4648    @ 080be142 4846
    muls r0,r3    @ 080be144 5843
    movs r1,#0xf0    @ 080be146 f021
    lsls r1,r1,#0x1    @ 080be148 4900
    adds r0,r0,r1    @ 080be14a 4018
    lsls r0,r0,#0x10    @ 080be14c 0004
    orrs r0,r6    @ 080be14e 3043
    .hword 0x4642    @ 080be150 4246
    lsls r4,r2,#0x3    @ 080be152 d400
    movs r3,#0x80    @ 080be154 8023
    lsls r3,r3,#0x2    @ 080be156 9b00
    adds r5,r4,r3    @ 080be158 e518
    movs r1,#0xc0    @ 080be15a c021
    lsls r1,r1,#0x6    @ 080be15c 8901
    orrs r5,r1    @ 080be15e 0d43
    lsls r5,r5,#0x10    @ 080be160 2d04
    lsrs r5,r5,#0x10    @ 080be162 2d0c
    ldr r1, DAT_080be1fc                     @ 080be164 2549
    adds r2,r5,#0x0    @ 080be166 2a1c
    bl write_oam_entry_from_packed_args      @ 080be168 38f000f8
    ldrb r2,[r7,#0x11]                       @ 080be16c 7a7c
    .hword 0x4648    @ 080be16e 4846
    muls r0,r2    @ 080be170 5043
    movs r3,#0xa8    @ 080be172 a823
    lsls r3,r3,#0x2    @ 080be174 9b00
    subs r0,r3,r0    @ 080be176 181a
    lsls r0,r0,#0x10    @ 080be178 0004
    orrs r0,r6    @ 080be17a 3043
    movs r1,#0xa0    @ 080be17c a021
    lsls r1,r1,#0x2    @ 080be17e 8900
    adds r4,r4,r1    @ 080be180 6418
    movs r2,#0xc0    @ 080be182 c022
    lsls r2,r2,#0x6    @ 080be184 9201
    orrs r4,r2    @ 080be186 1443
    lsls r4,r4,#0x10    @ 080be188 2404
    lsrs r4,r4,#0x10    @ 080be18a 240c
    ldr r1, DAT_080be1fc                     @ 080be18c 1b49
    adds r2,r4,#0x0    @ 080be18e 221c
    bl write_oam_entry_from_packed_args      @ 080be190 37f0ecff
    ldrb r3,[r7,#0x11]                       @ 080be194 7b7c
    .hword 0x4648    @ 080be196 4846
    muls r0,r3    @ 080be198 5843
    movs r1,#0xf0    @ 080be19a f021
    lsls r1,r1,#0x1    @ 080be19c 4900
    adds r0,r0,r1    @ 080be19e 4018
    lsls r0,r0,#0x10    @ 080be1a0 0004
    orrs r0,r6    @ 080be1a2 3043
    .hword 0x4651    @ 080be1a4 5146
    adds r2,r5,#0x0    @ 080be1a6 2a1c
    bl write_oam_entry_from_packed_args      @ 080be1a8 37f0e0ff
    ldrb r2,[r7,#0x11]                       @ 080be1ac 7a7c
    .hword 0x4648    @ 080be1ae 4846
    muls r0,r2    @ 080be1b0 5043
    movs r3,#0xa8    @ 080be1b2 a823
    lsls r3,r3,#0x2    @ 080be1b4 9b00
    subs r0,r3,r0    @ 080be1b6 181a
    lsls r0,r0,#0x10    @ 080be1b8 0004
    orrs r0,r6    @ 080be1ba 3043
    .hword 0x4651    @ 080be1bc 5146
    adds r2,r4,#0x0    @ 080be1be 221c
    bl write_oam_entry_from_packed_args      @ 080be1c0 37f0d4ff
    adds r6,#0x40    @ 080be1c4 4036
    movs r0,#0x1    @ 080be1c6 0120
    add r8,r0                                @ 080be1c8 8044
    .hword 0x4641    @ 080be1ca 4146
    cmp r1,#0x2                              @ 080be1cc 0229
    ble LAB_080be140                         @ 080be1ce b7dd
    ldr r1, PTR_BLDY_080be200                @ 080be1d0 0b49
    ldr r2, DAT_080be1f4                     @ 080be1d2 084a
    ldrb r0,[r2,#0x11]                       @ 080be1d4 507c
    strh r0,[r1,#0x0]                        @ 080be1d6 0880
    ldrb r0,[r2,#0x11]                       @ 080be1d8 507c
    adds r0,#0x1    @ 080be1da 0130
    strb r0,[r2,#0x11]                       @ 080be1dc 5074  -- gBannerState[+0x11]++ (sub-counter)
    lsls r0,r0,#0x18    @ 080be1de 0006
    lsrs r0,r0,#0x18    @ 080be1e0 000e
    cmp r0,#0x6                              @ 080be1e2 0628
    bhi LAB_080be1e8                         @ 080be1e4 00d8
    b LAB_080be5b0                           @ 080be1e6 e3e1
LAB_080be1e8:
    ldrb r0,[r2,#0x10]                       @ 080be1e8 107c
    adds r0,#0x1    @ 080be1ea 0130
    strb r0,[r2,#0x10]                       @ 080be1ec 1074  -- gBannerState[+0x10]++; gBannerState[+0x11] = 0 (满 7 帧, 进 case 2)
    movs r0,#0x0    @ 080be1ee 0020
    strb r0,[r2,#0x11]                       @ 080be1f0 5074
    b LAB_080be5b0                           @ 080be1f2 dde1
DAT_080be1f4:
    .word  gBannerState                   @ 080be1f4 c0fe0102
DAT_080be1f8:
    .word  0x000040c0                     @ 080be1f8 c0400000
DAT_080be1fc:
    .word  0x000048c0                     @ 080be1fc c0480000
PTR_BLDY_080be200:
    .word  BLDY                           @ 080be200 54000004
switchD_080bdfcc__caseD_2:
    movs r7,#0x30    @ 080be204 3027  -- case 2 DISPLAY (64 帧): 3行x2次 FUN_080f616c, 持续显示无 BLDY 调整
    movs r2,#0x0    @ 080be206 0022
    .hword 0x4690    @ 080be208 9046
    movs r6,#0x18    @ 080be20a 1826
LAB_080be20c:
    lsls r5,r7,#0x10    @ 080be20c 3d04
    orrs r5,r6    @ 080be20e 3543
    .hword 0x4643    @ 080be210 4346
    lsls r4,r3,#0x3    @ 080be212 dc00
    movs r0,#0x80    @ 080be214 8020
    lsls r0,r0,#0x2    @ 080be216 8000
    adds r4,r4,r0    @ 080be218 2418
    movs r1,#0xc0    @ 080be21a c021
    lsls r1,r1,#0x6    @ 080be21c 8901
    adds r0,r1,#0x0    @ 080be21e 081c
    orrs r4,r0    @ 080be220 0443
    lsls r4,r4,#0x10    @ 080be222 2404
    lsrs r4,r4,#0x10    @ 080be224 240c
    adds r0,r5,#0x0    @ 080be226 281c
    movs r1,#0x8c    @ 080be228 8c21
    lsls r1,r1,#0x4    @ 080be22a 0901
    adds r2,r4,#0x0    @ 080be22c 221c
    bl write_oam_entry_from_packed_args      @ 080be22e 37f09dff
    adds r0,r5,#0x0    @ 080be232 281c
    movs r1,#0xc0    @ 080be234 c021
    adds r2,r4,#0x0    @ 080be236 221c
    bl write_oam_entry_from_packed_args      @ 080be238 37f098ff
    adds r6,#0x40    @ 080be23c 4036
    movs r2,#0x1    @ 080be23e 0122
    add r8,r2                                @ 080be240 9044
    .hword 0x4643    @ 080be242 4346
    cmp r3,#0x2                              @ 080be244 022b
    ble LAB_080be20c                         @ 080be246 e1dd
    ldr r1, DAT_080be268                     @ 080be248 0749
    ldrb r0,[r1,#0x11]                       @ 080be24a 487c
    adds r0,#0x1    @ 080be24c 0130
    strb r0,[r1,#0x11]                       @ 080be24e 4874
    lsls r0,r0,#0x18    @ 080be250 0006
    lsrs r0,r0,#0x18    @ 080be252 000e
    cmp r0,#0x3f                             @ 080be254 3f28
    bhi LAB_080be25a                         @ 080be256 00d8
    b LAB_080be5b0                           @ 080be258 aae1
LAB_080be25a:
    ldrb r0,[r1,#0x10]                       @ 080be25a 087c
    adds r0,#0x1    @ 080be25c 0130
    strb r0,[r1,#0x10]                       @ 080be25e 0874
    movs r0,#0x0    @ 080be260 0020
    strb r0,[r1,#0x11]                       @ 080be262 4874
    b LAB_080be5b0                           @ 080be264 a4e1
    .zero  0x2
DAT_080be268:
    .word  gBannerState                   @ 080be268 c0fe0102
switchD_080bdfcc__caseD_3:
    movs r0,#0x1b    @ 080be26c 1b20  -- case 3 FADE_OUT_A (8 帧): 3行x8次 FUN_080f616c (复杂坐标), 末尾 bl FUN_080f9ab4(8)
    .hword 0x4681    @ 080be26e 8146
    movs r1,#0x0    @ 080be270 0021
    .hword 0x4688    @ 080be272 8846
    movs r2,#0x80    @ 080be274 8022
    lsls r2,r2,#0x2    @ 080be276 9200
    .hword 0x4692    @ 080be278 9246
    movs r3,#0xf0    @ 080be27a f023
    str r3,[sp,#0x0]                         @ 080be27c 0093
    subs r0,#0xdb    @ 080be27e db38
    str r0,[sp,#0x4]                         @ 080be280 0190
LAB_080be282:
    ldr r1, DAT_080be3f8                     @ 080be282 5d49
    ldrb r1,[r1,#0x11]                       @ 080be284 497c
    .hword 0x4648    @ 080be286 4846
    muls r0,r1    @ 080be288 4843
    ldr r2,[sp,#0x4]                         @ 080be28a 019a
    adds r0,r0,r2    @ 080be28c 8018
    add r0,r10                               @ 080be28e 5044
    movs r3,#0xc0    @ 080be290 c023
    lsls r3,r3,#0xe    @ 080be292 9b03
    orrs r0,r3    @ 080be294 1843
    .hword 0x4641    @ 080be296 4146
    lsls r7,r1,#0x3    @ 080be298 cf00
    movs r2,#0xc0    @ 080be29a c022
    lsls r2,r2,#0x2    @ 080be29c 9200
    adds r5,r7,r2    @ 080be29e bd18
    movs r3,#0x80    @ 080be2a0 8023
    lsls r3,r3,#0x7    @ 080be2a2 db01
    orrs r5,r3    @ 080be2a4 1d43
    lsls r5,r5,#0x10    @ 080be2a6 2d04
    lsrs r5,r5,#0x10    @ 080be2a8 2d0c
    ldr r1, DAT_080be3fc                     @ 080be2aa 5449
    adds r2,r5,#0x0    @ 080be2ac 2a1c
    bl write_oam_entry_from_packed_args      @ 080be2ae 37f05dff
    ldr r1, DAT_080be3f8                     @ 080be2b2 5149
    ldrb r1,[r1,#0x11]                       @ 080be2b4 497c
    .hword 0x4648    @ 080be2b6 4846
    muls r0,r1    @ 080be2b8 4843
    ldr r2,[sp,#0x0]                         @ 080be2ba 009a
    subs r0,r2,r0    @ 080be2bc 101a
    add r0,r10                               @ 080be2be 5044
    movs r3,#0xa0    @ 080be2c0 a023
    lsls r3,r3,#0xf    @ 080be2c2 db03
    orrs r0,r3    @ 080be2c4 1843
    movs r1,#0xe0    @ 080be2c6 e021
    lsls r1,r1,#0x2    @ 080be2c8 8900
    adds r4,r7,r1    @ 080be2ca 7c18
    movs r2,#0x80    @ 080be2cc 8022
    lsls r2,r2,#0x7    @ 080be2ce d201
    orrs r4,r2    @ 080be2d0 1443
    lsls r4,r4,#0x10    @ 080be2d2 2404
    lsrs r4,r4,#0x10    @ 080be2d4 240c
    ldr r1, DAT_080be3fc                     @ 080be2d6 4949
    adds r2,r4,#0x0    @ 080be2d8 221c
    bl write_oam_entry_from_packed_args      @ 080be2da 37f047ff
    ldr r3, DAT_080be3f8                     @ 080be2de 464b
    ldrb r3,[r3,#0x11]                       @ 080be2e0 5b7c
    .hword 0x4648    @ 080be2e2 4846
    muls r0,r3    @ 080be2e4 5843
    ldr r1,[sp,#0x4]                         @ 080be2e6 0199
    adds r0,r0,r1    @ 080be2e8 4018
    add r0,r10                               @ 080be2ea 5044
    movs r2,#0xc0    @ 080be2ec c022
    lsls r2,r2,#0xe    @ 080be2ee 9203
    orrs r0,r2    @ 080be2f0 1043
    ldr r1, DAT_080be400                     @ 080be2f2 4349
    adds r2,r5,#0x0    @ 080be2f4 2a1c
    bl write_oam_entry_from_packed_args      @ 080be2f6 37f039ff
    ldr r3, DAT_080be3f8                     @ 080be2fa 3f4b
    ldrb r3,[r3,#0x11]                       @ 080be2fc 5b7c
    .hword 0x4648    @ 080be2fe 4846
    muls r0,r3    @ 080be300 5843
    ldr r1,[sp,#0x0]                         @ 080be302 0099
    subs r0,r1,r0    @ 080be304 081a
    add r0,r10                               @ 080be306 5044
    movs r2,#0xa0    @ 080be308 a022
    lsls r2,r2,#0xf    @ 080be30a d203
    orrs r0,r2    @ 080be30c 1043
    ldr r1, DAT_080be400                     @ 080be30e 3c49
    adds r2,r4,#0x0    @ 080be310 221c
    bl write_oam_entry_from_packed_args      @ 080be312 37f02bff
    movs r1,#0x8    @ 080be316 0821
    ldr r3, DAT_080be3f8                     @ 080be318 374b
    ldrb r3,[r3,#0x11]                       @ 080be31a 5b7c
    subs r0,r1,r3    @ 080be31c c81a
    .hword 0x4649    @ 080be31e 4946
    muls r1,r0    @ 080be320 4143
    adds r0,r1,#0x0    @ 080be322 081c
    ldr r2,[sp,#0x0]                         @ 080be324 009a
    subs r0,r2,r0    @ 080be326 101a
    add r0,r10                               @ 080be328 5044
    movs r3,#0xc0    @ 080be32a c023
    lsls r3,r3,#0xe    @ 080be32c 9b03
    orrs r0,r3    @ 080be32e 1843
    .hword 0x4651    @ 080be330 5146
    adds r5,r7,r1    @ 080be332 7d18
    movs r2,#0xc0    @ 080be334 c022
    lsls r2,r2,#0x6    @ 080be336 9201
    adds r6,r2,#0x0    @ 080be338 161c
    orrs r5,r6    @ 080be33a 3543
    lsls r5,r5,#0x10    @ 080be33c 2d04
    lsrs r5,r5,#0x10    @ 080be33e 2d0c
    ldr r1, DAT_080be3fc                     @ 080be340 2e49
    adds r2,r5,#0x0    @ 080be342 2a1c
    bl write_oam_entry_from_packed_args      @ 080be344 37f012ff
    movs r1,#0x8    @ 080be348 0821
    ldr r3, DAT_080be3f8                     @ 080be34a 2b4b
    ldrb r3,[r3,#0x11]                       @ 080be34c 5b7c
    subs r0,r1,r3    @ 080be34e c81a
    .hword 0x4649    @ 080be350 4946
    muls r1,r0    @ 080be352 4143
    adds r0,r1,#0x0    @ 080be354 081c
    ldr r2,[sp,#0x4]                         @ 080be356 019a
    adds r0,r0,r2    @ 080be358 8018
    add r0,r10                               @ 080be35a 5044
    movs r3,#0xa0    @ 080be35c a023
    lsls r3,r3,#0xf    @ 080be35e db03
    orrs r0,r3    @ 080be360 1843
    movs r1,#0xa0    @ 080be362 a021
    lsls r1,r1,#0x2    @ 080be364 8900
    adds r4,r7,r1    @ 080be366 7c18
    orrs r4,r6    @ 080be368 3443
    lsls r4,r4,#0x10    @ 080be36a 2404
    lsrs r4,r4,#0x10    @ 080be36c 240c
    ldr r1, DAT_080be3fc                     @ 080be36e 2349
    adds r2,r4,#0x0    @ 080be370 221c
    bl write_oam_entry_from_packed_args      @ 080be372 37f0fbfe
    movs r3,#0x8    @ 080be376 0823
    ldr r2, DAT_080be3f8                     @ 080be378 1f4a
    ldrb r2,[r2,#0x11]                       @ 080be37a 527c
    subs r0,r3,r2    @ 080be37c 981a
    .hword 0x464b    @ 080be37e 4b46
    muls r3,r0    @ 080be380 4343
    adds r0,r3,#0x0    @ 080be382 181c
    ldr r1,[sp,#0x0]                         @ 080be384 0099
    subs r0,r1,r0    @ 080be386 081a
    add r0,r10                               @ 080be388 5044
    movs r2,#0xc0    @ 080be38a c022
    lsls r2,r2,#0xe    @ 080be38c 9203
    orrs r0,r2    @ 080be38e 1043
    ldr r1, DAT_080be400                     @ 080be390 1b49
    adds r2,r5,#0x0    @ 080be392 2a1c
    bl write_oam_entry_from_packed_args      @ 080be394 37f0eafe
    movs r1,#0x8    @ 080be398 0821
    ldr r3, DAT_080be3f8                     @ 080be39a 174b
    ldrb r3,[r3,#0x11]                       @ 080be39c 5b7c
    subs r0,r1,r3    @ 080be39e c81a
    .hword 0x4649    @ 080be3a0 4946
    muls r1,r0    @ 080be3a2 4143
    adds r0,r1,#0x0    @ 080be3a4 081c
    ldr r2,[sp,#0x4]                         @ 080be3a6 019a
    adds r0,r0,r2    @ 080be3a8 8018
    add r0,r10                               @ 080be3aa 5044
    movs r3,#0xa0    @ 080be3ac a023
    lsls r3,r3,#0xf    @ 080be3ae db03
    orrs r0,r3    @ 080be3b0 1843
    ldr r1, DAT_080be400                     @ 080be3b2 1349
    adds r2,r4,#0x0    @ 080be3b4 221c
    bl write_oam_entry_from_packed_args      @ 080be3b6 37f0d9fe
    ldr r0,[sp,#0x0]                         @ 080be3ba 0098
    adds r0,#0x40    @ 080be3bc 4030
    str r0,[sp,#0x0]                         @ 080be3be 0090
    ldr r1,[sp,#0x4]                         @ 080be3c0 0199
    adds r1,#0x40    @ 080be3c2 4031
    str r1,[sp,#0x4]                         @ 080be3c4 0191
    movs r2,#0x1    @ 080be3c6 0122
    add r8,r2                                @ 080be3c8 9044
    .hword 0x4643    @ 080be3ca 4346
    cmp r3,#0x2                              @ 080be3cc 022b
    bgt LAB_080be3d2                         @ 080be3ce 00dc
    b LAB_080be282                           @ 080be3d0 57e7
LAB_080be3d2:
    ldr r4, DAT_080be3f8                     @ 080be3d2 094c
    ldrb r0,[r4,#0x11]                       @ 080be3d4 607c
    adds r0,#0x1    @ 080be3d6 0130
    strb r0,[r4,#0x11]                       @ 080be3d8 6074
    lsls r0,r0,#0x18    @ 080be3da 0006
    lsrs r0,r0,#0x18    @ 080be3dc 000e
    cmp r0,#0x7                              @ 080be3de 0728
    bhi LAB_080be3e4                         @ 080be3e0 00d8
    b LAB_080be5b0                           @ 080be3e2 e5e0
LAB_080be3e4:
    movs r0,#0x8    @ 080be3e4 0820
    bl sync_state_and_init_sprite            @ 080be3e6 3bf065fb
    ldrb r0,[r4,#0x10]                       @ 080be3ea 207c
    adds r0,#0x1    @ 080be3ec 0130
    strb r0,[r4,#0x10]                       @ 080be3ee 2074
    movs r0,#0x0    @ 080be3f0 0020
    strb r0,[r4,#0x11]                       @ 080be3f2 6074
    b LAB_080be5b0                           @ 080be3f4 dce0
    .zero  0x2
DAT_080be3f8:
    .word  gBannerState                   @ 080be3f8 c0fe0102
DAT_080be3fc:
    .word  0x000048c0                     @ 080be3fc c0480000
DAT_080be400:
    .word  0x000040c0                     @ 080be400 c0400000
switchD_080bdfcc__caseD_4:
    movs r7,#0x30    @ 080be404 3027  -- case 4 TEXT_TRANSITION (64 帧): 前16帧 fade-in 文本, 16~32帧反向 fade-out
    adds r1,r3,#0x0    @ 080be406 191c
    ldrb r0,[r1,#0x11]                       @ 080be408 487c
    cmp r0,#0x20                             @ 080be40a 2028
    bhi LAB_080be436                         @ 080be40c 13d8
    cmp r0,#0x10                             @ 080be40e 1028
    bhi LAB_080be424                         @ 080be410 08d8
    ldr r0, DAT_080be420                     @ 080be412 0348
    ldrb r2,[r1,#0x11]                       @ 080be414 4a7c
    movs r1,#0x4    @ 080be416 0421
    bl blend_palette_entry_toward_target     @ 080be418 fef7e2f9
    b LAB_080be436                           @ 080be41c 0be0
    .zero  0x2
DAT_080be420:
    .word  0x098a5024                     @ 080be420 24508a09
LAB_080be424:
    ldr r0, DAT_080be498                     @ 080be424 1c48
    movs r2,#0x20    @ 080be426 2022
    ldrb r3,[r3,#0x11]                       @ 080be428 5b7c
    subs r2,r2,r3    @ 080be42a d21a
    lsls r2,r2,#0x10    @ 080be42c 1204
    lsrs r2,r2,#0x10    @ 080be42e 120c
    movs r1,#0x4    @ 080be430 0421
    bl blend_palette_entry_toward_target     @ 080be432 fef7d5f9
LAB_080be436:
    movs r0,#0x0    @ 080be436 0020
    .hword 0x4680    @ 080be438 8046
    lsls r7,r7,#0x10    @ 080be43a 3f04
    movs r6,#0x18    @ 080be43c 1826
LAB_080be43e:
    adds r5,r6,#0x0    @ 080be43e 351c
    orrs r5,r7    @ 080be440 3d43
    .hword 0x4641    @ 080be442 4146
    lsls r4,r1,#0x3    @ 080be444 cc00
    movs r2,#0xc0    @ 080be446 c022
    lsls r2,r2,#0x2    @ 080be448 9200
    adds r4,r4,r2    @ 080be44a a418
    movs r3,#0x80    @ 080be44c 8023
    lsls r3,r3,#0x7    @ 080be44e db01
    adds r0,r3,#0x0    @ 080be450 181c
    orrs r4,r0    @ 080be452 0443
    lsls r4,r4,#0x10    @ 080be454 2404
    lsrs r4,r4,#0x10    @ 080be456 240c
    adds r0,r5,#0x0    @ 080be458 281c
    movs r1,#0x8c    @ 080be45a 8c21
    lsls r1,r1,#0x4    @ 080be45c 0901
    adds r2,r4,#0x0    @ 080be45e 221c
    bl write_oam_entry_from_packed_args      @ 080be460 37f084fe
    adds r0,r5,#0x0    @ 080be464 281c
    movs r1,#0xc0    @ 080be466 c021
    adds r2,r4,#0x0    @ 080be468 221c
    bl write_oam_entry_from_packed_args      @ 080be46a 37f07ffe
    adds r6,#0x40    @ 080be46e 4036
    movs r0,#0x1    @ 080be470 0120
    add r8,r0                                @ 080be472 8044
    .hword 0x4641    @ 080be474 4146
    cmp r1,#0x2                              @ 080be476 0229
    ble LAB_080be43e                         @ 080be478 e1dd
    ldr r1, DAT_080be49c                     @ 080be47a 0849
    ldrb r0,[r1,#0x11]                       @ 080be47c 487c
    adds r0,#0x1    @ 080be47e 0130
    strb r0,[r1,#0x11]                       @ 080be480 4874
    lsls r0,r0,#0x18    @ 080be482 0006
    lsrs r0,r0,#0x18    @ 080be484 000e
    cmp r0,#0x3f                             @ 080be486 3f28
    bhi LAB_080be48c                         @ 080be488 00d8
    b LAB_080be5b0                           @ 080be48a 91e0
LAB_080be48c:
    ldrb r0,[r1,#0x10]                       @ 080be48c 087c
    adds r0,#0x1    @ 080be48e 0130
    strb r0,[r1,#0x10]                       @ 080be490 0874
    movs r0,#0x0    @ 080be492 0020
    strb r0,[r1,#0x11]                       @ 080be494 4874
    b LAB_080be5b0                           @ 080be496 8be0
DAT_080be498:
    .word  0x098a5024                     @ 080be498 24508a09
DAT_080be49c:
    .word  gBannerState                   @ 080be49c c0fe0102
switchD_080bdfcc__caseD_5:
    movs r2,#0x1b    @ 080be4a0 1b22  -- case 5 FADE_OUT_B (8 帧): 3行x4次 FUN_080f616c, 末尾 BLDY = (8 - sub-counter)
    .hword 0x4691    @ 080be4a2 9146
    movs r3,#0x0    @ 080be4a4 0023
    .hword 0x4698    @ 080be4a6 9846
    movs r0,#0x80    @ 080be4a8 8020
    lsls r0,r0,#0x2    @ 080be4aa 8000
    .hword 0x4682    @ 080be4ac 8246
    movs r7,#0xc0    @ 080be4ae c027
    rsbs r7,r7,#0    @ 080be4b0 7f42
    movs r6,#0xf0    @ 080be4b2 f026
LAB_080be4b4:
    movs r2,#0x8    @ 080be4b4 0822
    ldr r1, DAT_080be588                     @ 080be4b6 3449
    ldrb r1,[r1,#0x11]                       @ 080be4b8 497c
    subs r0,r2,r1    @ 080be4ba 501a
    .hword 0x464a    @ 080be4bc 4a46
    muls r2,r0    @ 080be4be 4243
    adds r0,r2,#0x0    @ 080be4c0 101c
    subs r0,r6,r0    @ 080be4c2 301a
    add r0,r10                               @ 080be4c4 5044
    movs r3,#0xc0    @ 080be4c6 c023
    lsls r3,r3,#0xe    @ 080be4c8 9b03
    orrs r0,r3    @ 080be4ca 1843
    .hword 0x4641    @ 080be4cc 4146
    lsls r5,r1,#0x3    @ 080be4ce cd00
    movs r2,#0xc0    @ 080be4d0 c022
    lsls r2,r2,#0x2    @ 080be4d2 9200
    adds r4,r5,r2    @ 080be4d4 ac18
    movs r3,#0x80    @ 080be4d6 8023
    lsls r3,r3,#0x7    @ 080be4d8 db01
    orrs r4,r3    @ 080be4da 1c43
    lsls r4,r4,#0x10    @ 080be4dc 2404
    lsrs r4,r4,#0x10    @ 080be4de 240c
    ldr r1, DAT_080be58c                     @ 080be4e0 2a49
    adds r2,r4,#0x0    @ 080be4e2 221c
    bl write_oam_entry_from_packed_args      @ 080be4e4 37f042fe
    movs r2,#0x8    @ 080be4e8 0822
    ldr r1, DAT_080be588                     @ 080be4ea 2749
    ldrb r1,[r1,#0x11]                       @ 080be4ec 497c
    subs r0,r2,r1    @ 080be4ee 501a
    .hword 0x464a    @ 080be4f0 4a46
    muls r2,r0    @ 080be4f2 4243
    adds r0,r2,#0x0    @ 080be4f4 101c
    subs r0,r6,r0    @ 080be4f6 301a
    add r0,r10                               @ 080be4f8 5044
    movs r3,#0xc0    @ 080be4fa c023
    lsls r3,r3,#0xe    @ 080be4fc 9b03
    orrs r0,r3    @ 080be4fe 1843
    ldr r1, DAT_080be590                     @ 080be500 2349
    adds r2,r4,#0x0    @ 080be502 221c
    bl write_oam_entry_from_packed_args      @ 080be504 37f032fe
    movs r2,#0x8    @ 080be508 0822
    ldr r1, DAT_080be588                     @ 080be50a 1f49
    ldrb r1,[r1,#0x11]                       @ 080be50c 497c
    subs r0,r2,r1    @ 080be50e 501a
    .hword 0x464a    @ 080be510 4a46
    muls r2,r0    @ 080be512 4243
    adds r0,r2,#0x0    @ 080be514 101c
    adds r0,r0,r7    @ 080be516 c019
    add r0,r10                               @ 080be518 5044
    movs r3,#0xa0    @ 080be51a a023
    lsls r3,r3,#0xf    @ 080be51c db03
    orrs r0,r3    @ 080be51e 1843
    movs r1,#0xe0    @ 080be520 e021
    lsls r1,r1,#0x2    @ 080be522 8900
    adds r4,r5,r1    @ 080be524 6c18
    movs r2,#0x80    @ 080be526 8022
    lsls r2,r2,#0x7    @ 080be528 d201
    orrs r4,r2    @ 080be52a 1443
    lsls r4,r4,#0x10    @ 080be52c 2404
    lsrs r4,r4,#0x10    @ 080be52e 240c
    ldr r1, DAT_080be58c                     @ 080be530 1649
    adds r2,r4,#0x0    @ 080be532 221c
    bl write_oam_entry_from_packed_args      @ 080be534 37f01afe
    movs r1,#0x8    @ 080be538 0821
    ldr r3, DAT_080be588                     @ 080be53a 134b
    ldrb r3,[r3,#0x11]                       @ 080be53c 5b7c
    subs r0,r1,r3    @ 080be53e c81a
    .hword 0x4649    @ 080be540 4946
    muls r1,r0    @ 080be542 4143
    adds r0,r1,#0x0    @ 080be544 081c
    adds r0,r0,r7    @ 080be546 c019
    add r0,r10                               @ 080be548 5044
    movs r2,#0xa0    @ 080be54a a022
    lsls r2,r2,#0xf    @ 080be54c d203
    orrs r0,r2    @ 080be54e 1043
    ldr r1, DAT_080be590                     @ 080be550 0f49
    adds r2,r4,#0x0    @ 080be552 221c
    bl write_oam_entry_from_packed_args      @ 080be554 37f00afe
    adds r7,#0x40    @ 080be558 4037
    adds r6,#0x40    @ 080be55a 4036
    movs r3,#0x1    @ 080be55c 0123
    add r8,r3                                @ 080be55e 9844
    .hword 0x4640    @ 080be560 4046
    cmp r0,#0x2                              @ 080be562 0228
    ble LAB_080be4b4                         @ 080be564 a6dd
    ldr r0, PTR_BLDY_080be594                @ 080be566 0b48
    ldr r2, DAT_080be588                     @ 080be568 074a
    movs r1,#0x8    @ 080be56a 0821
    ldrb r3,[r2,#0x11]                       @ 080be56c 537c
    subs r1,r1,r3    @ 080be56e c91a
    strh r1,[r0,#0x0]                        @ 080be570 0180
    ldrb r0,[r2,#0x11]                       @ 080be572 507c
    adds r0,#0x1    @ 080be574 0130
    strb r0,[r2,#0x11]                       @ 080be576 5074
    lsls r0,r0,#0x18    @ 080be578 0006
    lsrs r0,r0,#0x18    @ 080be57a 000e
    cmp r0,#0x7                              @ 080be57c 0728
    bls LAB_080be5b0                         @ 080be57e 17d9
    ldrb r0,[r2,#0x10]                       @ 080be580 107c
    adds r0,#0x1    @ 080be582 0130
    strb r0,[r2,#0x10]                       @ 080be584 1074
    b LAB_080be5b0                           @ 080be586 13e0
DAT_080be588:
    .word  gBannerState                   @ 080be588 c0fe0102
DAT_080be58c:
    .word  0x000048c0                     @ 080be58c c0480000
DAT_080be590:
    .word  0x000040c0                     @ 080be590 c0400000
PTR_BLDY_080be594:
    .word  BLDY                           @ 080be594 54000004
switchD_080bdfcc__caseD_6:
    bl disable_blend_and_clear_step          @ 080be598 37f01cf8  -- case 6 TEARDOWN (1 帧): bl FUN_080f55d4(); DISPCNT &= 0x1FFF (清 BG3 enable)
    movs r2,#0x80    @ 080be59c 8022
    lsls r2,r2,#0x13    @ 080be59e d204
    ldrh r1,[r2,#0x0]                        @ 080be5a0 1188
    ldr r0, DAT_080be5b4                     @ 080be5a2 0448
    ands r0,r1    @ 080be5a4 0840
LAB_080be5a6:
    strh r0,[r2,#0x0]                        @ 080be5a6 1080  -- case 0 / case 6 共用: 写 DISPCNT, gBannerState[+0x10]++
    ldr r1, DAT_080be5b8                     @ 080be5a8 0349
    ldrb r0,[r1,#0x10]                       @ 080be5aa 087c
    adds r0,#0x1    @ 080be5ac 0130
    strb r0,[r1,#0x10]                       @ 080be5ae 0874  -- gBannerState[+0x10]++ (推进主状态)
LAB_080be5b0:
    movs r0,#0x1    @ 080be5b0 0120  -- LAB_080be5b0: r0 = 1 (busy, 状态机继续运行)
    b LAB_080be5e8                           @ 080be5b2 19e0
DAT_080be5b4:
    .word  0x00001fff                     @ 080be5b4 ff1f0000
DAT_080be5b8:
    .word  gBannerState                   @ 080be5b8 c0fe0102
LAB_080be5bc:
    ldr r4, DAT_080be5f8                     @ 080be5bc 0e4c  -- default DONE: 读 [0x02023350+0x220] 调 FUN_080f9adc(); 清 gBannerState[+0x0] bit1; 清 [0x02023350+0x215] bit0,2
    movs r1,#0x88    @ 080be5be 8821
    lsls r1,r1,#0x2    @ 080be5c0 8900
    adds r0,r4,r1    @ 080be5c2 6018
    ldrh r0,[r0,#0x0]                        @ 080be5c4 0088
    lsls r0,r0,#0x16    @ 080be5c6 8005
    lsrs r0,r0,#0x18    @ 080be5c8 000e
    bl set_channel_if_changed                @ 080be5ca 3bf087fa
    movs r0,#0x2    @ 080be5ce 0220
    rsbs r0,r0,#0    @ 080be5d0 4042
    ldrb r2,[r5,#0x0]                        @ 080be5d2 2a78
    ands r0,r2    @ 080be5d4 1040
    strb r0,[r5,#0x0]                        @ 080be5d6 2870
    ldr r3, DAT_080be5fc                     @ 080be5d8 084b
    adds r4,r4,r3    @ 080be5da e418
    movs r0,#0x5    @ 080be5dc 0520
    rsbs r0,r0,#0    @ 080be5de 4042
    ldrb r1,[r4,#0x0]                        @ 080be5e0 2178
    ands r0,r1    @ 080be5e2 0840
    strb r0,[r4,#0x0]                        @ 080be5e4 2070
    movs r0,#0x0    @ 080be5e6 0020  -- r0 = 0 (done)
LAB_080be5e8:
    add sp,#0x8                              @ 080be5e8 02b0  -- epilogue: 返回 r0 (1=busy / 0=done)
    pop {r3,r4,r5}                           @ 080be5ea 38bc
    .hword 0x4698    @ 080be5ec 9846
    .hword 0x46a1    @ 080be5ee a146
    .hword 0x46aa    @ 080be5f0 aa46
    pop {r4,r5,r6,r7}                        @ 080be5f2 f0bc
    pop {r1}                                 @ 080be5f4 02bc
    bx r1                                    @ 080be5f6 0847
DAT_080be5f8:
    .word  0x02023130                     @ 080be5f8 30310202
DAT_080be5fc:
    .word  0x00000215                     @ 080be5fc 15020000

@ pack 场景 banner 状态机驱动器, 读取 gBannerState[+0x10] (当前状态 0-4), 通过 switch 跳转到 5 个子状态处理函数, 协调 pack 开包 banner 动画全流程 (含 display/window/blend/palette/vram). 唯一调用方: play_ui_effect (0x0801ef94, scene_pack). Constants: gBannerState_OFFSET=0x10, CASE_COUNT=5, OBJ_PAL_HIGH_MASK=0xe000.
tick_banner_pack_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 080be600 f0b5
    .hword 0x4657    @ 080be602 5746
    .hword 0x464e    @ 080be604 4e46
    .hword 0x4645    @ 080be606 4546
    push {r5,r6,r7}                          @ 080be608 e0b4
    sub sp,#0x4                              @ 080be60a 81b0
    movs r4,#0x30    @ 080be60c 3024
    movs r0,#0xd    @ 080be60e 0d20
    .hword 0x4680    @ 080be610 8046
    ldr r5, DAT_080be628                     @ 080be612 054d
    ldrb r0,[r5,#0x10]                       @ 080be614 287c
    adds r3,r5,#0x0    @ 080be616 2b1c
    cmp r0,#0x4                              @ 080be618 0428
    bls LAB_080be61e                         @ 080be61a 00d9
switchD_080be626__default:
    b LAB_080be978                           @ 080be61c ace1
LAB_080be61e:
    lsls r0,r0,#0x2    @ 080be61e 8000
    ldr r1, DAT_080be62c                     @ 080be620 0249
    adds r0,r0,r1    @ 080be622 4018
    ldr r0,[r0,#0x0]                         @ 080be624 0068
switchD_080be626__switchD:
    .hword 0x4687    @ 080be626 8746
DAT_080be628:
    .word  gBannerState                   @ 080be628 c0fe0102
DAT_080be62c:
    .word  0x080be630                     @ 080be62c 30e60b08
switchD_080be626__switchdataD_080be630:
    .word  0x080be644                     @ 080be630 44e60b08
    .word  0x080be6b8                     @ 080be634 b8e60b08
    .word  0x080be7b8                     @ 080be638 b8e70b08
    .word  0x080be84c                     @ 080be63c 4ce80b08
    .word  0x080be954                     @ 080be640 54e90b08
switchD_080be626__caseD_0:
    ldr r0, DAT_080be698                     @ 080be644 1448
    ldr r1, DAT_080be69c                     @ 080be646 1549
    adds r0,r0,r1    @ 080be648 4018
    ldrb r0,[r0,#0x0]                        @ 080be64a 0078
    lsls r0,r0,#0x1d    @ 080be64c 4007
    lsrs r0,r0,#0x1d    @ 080be64e 400f
    lsls r4,r0,#0x1    @ 080be650 4400
    adds r4,r4,r0    @ 080be652 2418
    lsls r4,r4,#0xb    @ 080be654 e402
    ldr r0, DAT_080be6a0                     @ 080be656 1248
    adds r4,r4,r0    @ 080be658 2418
    ldr r0, DAT_080be6a4                     @ 080be65a 1248
    ldr r1, DAT_080be6a8                     @ 080be65c 1249
    movs r2,#0x20    @ 080be65e 2022
    bl copy_bytes_by_halfword                @ 080be660 36f020fc
    ldr r0, DAT_080be6ac                     @ 080be664 1148
    adds r1,r4,#0x0    @ 080be666 211c
    movs r2,#0x18    @ 080be668 1822
    movs r3,#0x8    @ 080be66a 0823
    bl tile_2d_row_copy                      @ 080be66c 38f032ff
    bl disable_blend_and_clear_step          @ 080be670 36f0b0ff
    ldr r1, PTR_WINOUT_080be6b0              @ 080be674 0e49
    ldr r2, DAT_080be6b4                     @ 080be676 0f4a
    adds r0,r2,#0x0    @ 080be678 101c
    strh r0,[r1,#0x0]                        @ 080be67a 0880
    adds r1,#0xa    @ 080be67c 0a31
    movs r0,#0x0    @ 080be67e 0020
    strh r0,[r1,#0x0]                        @ 080be680 0880
    subs r1,#0x4    @ 080be682 0439
    movs r0,#0xff    @ 080be684 ff20
    strh r0,[r1,#0x0]                        @ 080be686 0880
    movs r2,#0x80    @ 080be688 8022
    lsls r2,r2,#0x13    @ 080be68a d204
    ldrh r0,[r2,#0x0]                        @ 080be68c 1088
    movs r3,#0x80    @ 080be68e 8023
    lsls r3,r3,#0x8    @ 080be690 1b02
    adds r1,r3,#0x0    @ 080be692 191c
    orrs r0,r1    @ 080be694 0843
    b LAB_080be962                           @ 080be696 64e1
DAT_080be698:
    .word  0x02000000                     @ 080be698 00000002
DAT_080be69c:
    .word  0x00006c2c                     @ 080be69c 2c6c0000
DAT_080be6a0:
    .word  0x098a5044                     @ 080be6a0 44508a09
DAT_080be6a4:
    .word  0x05000260                     @ 080be6a4 60020005
DAT_080be6a8:
    .word  0x098a5024                     @ 080be6a8 24508a09
DAT_080be6ac:
    .word  0x06014000                     @ 080be6ac 00400106
PTR_WINOUT_080be6b0:
    .word  WINOUT                         @ 080be6b0 4a000004
DAT_080be6b4:
    .word  0x00001f3f                     @ 080be6b4 3f1f0000
switchD_080be626__caseD_1:
    adds r0,r4,#0x0    @ 080be6b8 201c
    adds r0,#0x20    @ 080be6ba 2030
    str r0,[sp,#0x0]                         @ 080be6bc 0090
    movs r1,#0x80    @ 080be6be 8021
    lsls r1,r1,#0x2    @ 080be6c0 8900
    .hword 0x468a    @ 080be6c2 8a46
    lsls r6,r4,#0x10    @ 080be6c4 2604
    .hword 0x46d1    @ 080be6c6 d146
    movs r5,#0xc0    @ 080be6c8 c025
    rsbs r5,r5,#0    @ 080be6ca 6d42
    movs r7,#0x2    @ 080be6cc 0227
LAB_080be6ce:
    ldr r2, DAT_080be7a8                     @ 080be6ce 364a
    ldrb r2,[r2,#0x11]                       @ 080be6d0 527c
    lsls r0,r2,#0x1    @ 080be6d2 5000
    .hword 0x4643    @ 080be6d4 4346
    muls r3,r0    @ 080be6d6 4343
    adds r0,r3,#0x0    @ 080be6d8 181c
    adds r0,r0,r5    @ 080be6da 4019
    add r0,r10                               @ 080be6dc 5044
    orrs r0,r6    @ 080be6de 3043
    movs r2,#0xc0    @ 080be6e0 c022
    lsls r2,r2,#0x6    @ 080be6e2 9201
    adds r1,r2,#0x0    @ 080be6e4 111c
    .hword 0x464c    @ 080be6e6 4c46
    orrs r4,r1    @ 080be6e8 0c43
    lsls r4,r4,#0x10    @ 080be6ea 2404
    lsrs r4,r4,#0x10    @ 080be6ec 240c
    ldr r1, DAT_080be7ac                     @ 080be6ee 2f49
    adds r2,r4,#0x0    @ 080be6f0 221c
    bl write_oam_entry_from_packed_args      @ 080be6f2 37f03bfd
    ldr r3, DAT_080be7a8                     @ 080be6f6 2c4b
    ldrb r3,[r3,#0x11]                       @ 080be6f8 5b7c
    lsls r0,r3,#0x1    @ 080be6fa 5800
    .hword 0x4641    @ 080be6fc 4146
    muls r1,r0    @ 080be6fe 4143
    adds r0,r1,#0x0    @ 080be700 081c
    adds r0,r0,r5    @ 080be702 4019
    add r0,r10                               @ 080be704 5044
    orrs r0,r6    @ 080be706 3043
    ldr r1, DAT_080be7b0                     @ 080be708 2949
    adds r2,r4,#0x0    @ 080be70a 221c
    bl write_oam_entry_from_packed_args      @ 080be70c 37f02efd
    movs r2,#0x8    @ 080be710 0822
    add r9,r2                                @ 080be712 9144
    adds r5,#0x40    @ 080be714 4035
    subs r7,#0x1    @ 080be716 013f
    cmp r7,#0x0                              @ 080be718 002f
    bge LAB_080be6ce                         @ 080be71a d8da
    movs r7,#0x0    @ 080be71c 0027
    ldr r3, DAT_080be7a8                     @ 080be71e 224b
    .hword 0x469a    @ 080be720 9a46
    movs r0,#0x80    @ 080be722 8020
    lsls r0,r0,#0x2    @ 080be724 8000
    .hword 0x4681    @ 080be726 8146
    ldr r1,[sp,#0x0]                         @ 080be728 0099
    lsls r6,r1,#0x10    @ 080be72a 0e04
    movs r5,#0xf0    @ 080be72c f025
LAB_080be72e:
    .hword 0x4652    @ 080be72e 5246
    ldrb r2,[r2,#0x11]                       @ 080be730 527c
    lsls r0,r2,#0x1    @ 080be732 5000
    .hword 0x4643    @ 080be734 4346
    muls r3,r0    @ 080be736 4343
    adds r0,r3,#0x0    @ 080be738 181c
    subs r0,r5,r0    @ 080be73a 281a
    add r0,r9                                @ 080be73c 4844
    orrs r0,r6    @ 080be73e 3043
    lsls r4,r7,#0x3    @ 080be740 fc00
    movs r1,#0xa0    @ 080be742 a021
    lsls r1,r1,#0x2    @ 080be744 8900
    adds r4,r4,r1    @ 080be746 6418
    movs r2,#0xc0    @ 080be748 c022
    lsls r2,r2,#0x6    @ 080be74a 9201
    adds r1,r2,#0x0    @ 080be74c 111c
    orrs r4,r1    @ 080be74e 0c43
    lsls r4,r4,#0x10    @ 080be750 2404
    lsrs r4,r4,#0x10    @ 080be752 240c
    ldr r1, DAT_080be7ac                     @ 080be754 1549
    adds r2,r4,#0x0    @ 080be756 221c
    bl write_oam_entry_from_packed_args      @ 080be758 37f008fd
    .hword 0x4653    @ 080be75c 5346
    ldrb r3,[r3,#0x11]                       @ 080be75e 5b7c
    lsls r0,r3,#0x1    @ 080be760 5800
    .hword 0x4641    @ 080be762 4146
    muls r1,r0    @ 080be764 4143
    adds r0,r1,#0x0    @ 080be766 081c
    subs r0,r5,r0    @ 080be768 281a
    add r0,r9                                @ 080be76a 4844
    orrs r0,r6    @ 080be76c 3043
    ldr r1, DAT_080be7b0                     @ 080be76e 1049
    adds r2,r4,#0x0    @ 080be770 221c
    bl write_oam_entry_from_packed_args      @ 080be772 37f0fbfc
    adds r5,#0x40    @ 080be776 4035
    adds r7,#0x1    @ 080be778 0137
    cmp r7,#0x2                              @ 080be77a 022f
    ble LAB_080be72e                         @ 080be77c d7dd
    ldr r1, PTR_BLDY_080be7b4                @ 080be77e 0d49
    ldr r4, DAT_080be7a8                     @ 080be780 094c
    ldrb r0,[r4,#0x11]                       @ 080be782 607c
    strh r0,[r1,#0x0]                        @ 080be784 0880
    ldrb r0,[r4,#0x11]                       @ 080be786 607c
    adds r0,#0x1    @ 080be788 0130
    strb r0,[r4,#0x11]                       @ 080be78a 6074
    lsls r0,r0,#0x18    @ 080be78c 0006
    lsrs r0,r0,#0x18    @ 080be78e 000e
    cmp r0,#0x7                              @ 080be790 0728
    bhi LAB_080be796                         @ 080be792 00d8
    b LAB_080be96c                           @ 080be794 eae0
LAB_080be796:
    movs r0,#0x8    @ 080be796 0820
    bl sync_state_and_init_sprite            @ 080be798 3bf08cf9
    ldrb r0,[r4,#0x10]                       @ 080be79c 207c
    adds r0,#0x1    @ 080be79e 0130
    strb r0,[r4,#0x10]                       @ 080be7a0 2074
    movs r0,#0x0    @ 080be7a2 0020
    strb r0,[r4,#0x11]                       @ 080be7a4 6074
    b LAB_080be96c                           @ 080be7a6 e1e0
DAT_080be7a8:
    .word  gBannerState                   @ 080be7a8 c0fe0102
DAT_080be7ac:
    .word  0x000048c0                     @ 080be7ac c0480000
DAT_080be7b0:
    .word  0x000040c0                     @ 080be7b0 c0400000
PTR_BLDY_080be7b4:
    .word  BLDY                           @ 080be7b4 54000004
switchD_080be626__caseD_2:
    adds r1,r3,#0x0    @ 080be7b8 191c
    ldrb r0,[r1,#0x11]                       @ 080be7ba 487c
    cmp r0,#0x20                             @ 080be7bc 2028
    bhi LAB_080be7e6                         @ 080be7be 12d8
    cmp r0,#0x10                             @ 080be7c0 1028
    bhi LAB_080be7d4                         @ 080be7c2 07d8
    ldr r0, DAT_080be7d0                     @ 080be7c4 0248
    ldrb r2,[r1,#0x11]                       @ 080be7c6 4a7c
    movs r1,#0x3    @ 080be7c8 0321
    bl blend_palette_entry_toward_target     @ 080be7ca fef709f8
    b LAB_080be7e6                           @ 080be7ce 0ae0
DAT_080be7d0:
    .word  0x098a5024                     @ 080be7d0 24508a09
LAB_080be7d4:
    ldr r0, DAT_080be844                     @ 080be7d4 1b48
    movs r2,#0x20    @ 080be7d6 2022
    ldrb r3,[r3,#0x11]                       @ 080be7d8 5b7c
    subs r2,r2,r3    @ 080be7da d21a
    lsls r2,r2,#0x10    @ 080be7dc 1204
    lsrs r2,r2,#0x10    @ 080be7de 120c
    movs r1,#0x3    @ 080be7e0 0321
    bl blend_palette_entry_toward_target     @ 080be7e2 fdf7fdff
LAB_080be7e6:
    movs r7,#0x0    @ 080be7e6 0027
    lsls r4,r4,#0x10    @ 080be7e8 2404
    .hword 0x46a0    @ 080be7ea a046
    movs r6,#0x18    @ 080be7ec 1826
LAB_080be7ee:
    adds r5,r6,#0x0    @ 080be7ee 351c
    .hword 0x4642    @ 080be7f0 4246
    orrs r5,r2    @ 080be7f2 1543
    lsls r4,r7,#0x3    @ 080be7f4 fc00
    movs r3,#0x80    @ 080be7f6 8023
    lsls r3,r3,#0x2    @ 080be7f8 9b00
    adds r4,r4,r3    @ 080be7fa e418
    movs r1,#0xc0    @ 080be7fc c021
    lsls r1,r1,#0x6    @ 080be7fe 8901
    adds r0,r1,#0x0    @ 080be800 081c
    orrs r4,r0    @ 080be802 0443
    lsls r4,r4,#0x10    @ 080be804 2404
    lsrs r4,r4,#0x10    @ 080be806 240c
    adds r0,r5,#0x0    @ 080be808 281c
    movs r1,#0x8c    @ 080be80a 8c21
    lsls r1,r1,#0x4    @ 080be80c 0901
    adds r2,r4,#0x0    @ 080be80e 221c
    bl write_oam_entry_from_packed_args      @ 080be810 37f0acfc
    adds r0,r5,#0x0    @ 080be814 281c
    movs r1,#0xc0    @ 080be816 c021
    adds r2,r4,#0x0    @ 080be818 221c
    bl write_oam_entry_from_packed_args      @ 080be81a 37f0a7fc
    adds r6,#0x40    @ 080be81e 4036
    adds r7,#0x1    @ 080be820 0137
    cmp r7,#0x2                              @ 080be822 022f
    ble LAB_080be7ee                         @ 080be824 e3dd
    ldr r1, DAT_080be848                     @ 080be826 0849
    ldrb r0,[r1,#0x11]                       @ 080be828 487c
    adds r0,#0x1    @ 080be82a 0130
    strb r0,[r1,#0x11]                       @ 080be82c 4874
    lsls r0,r0,#0x18    @ 080be82e 0006
    lsrs r0,r0,#0x18    @ 080be830 000e
    cmp r0,#0x3f                             @ 080be832 3f28
    bhi LAB_080be838                         @ 080be834 00d8
    b LAB_080be96c                           @ 080be836 99e0
LAB_080be838:
    ldrb r0,[r1,#0x10]                       @ 080be838 087c
    adds r0,#0x1    @ 080be83a 0130
    strb r0,[r1,#0x10]                       @ 080be83c 0874
    movs r0,#0x0    @ 080be83e 0020
    strb r0,[r1,#0x11]                       @ 080be840 4874
    b LAB_080be96c                           @ 080be842 93e0
DAT_080be844:
    .word  0x098a5024                     @ 080be844 24508a09
DAT_080be848:
    .word  gBannerState                   @ 080be848 c0fe0102
switchD_080be626__caseD_3:
    adds r2,r4,#0x0    @ 080be84c 221c
    adds r2,#0x20    @ 080be84e 2032
    str r2,[sp,#0x0]                         @ 080be850 0092
    movs r3,#0x80    @ 080be852 8023
    lsls r3,r3,#0x2    @ 080be854 9b00
    .hword 0x469a    @ 080be856 9a46
    lsls r6,r4,#0x10    @ 080be858 2604
    .hword 0x46d1    @ 080be85a d146
    movs r5,#0xf0    @ 080be85c f025
    movs r7,#0x2    @ 080be85e 0227
LAB_080be860:
    ldr r1, DAT_080be944                     @ 080be860 3849
    ldrb r1,[r1,#0x11]                       @ 080be862 497c
    lsls r0,r1,#0x1    @ 080be864 4800
    movs r2,#0x10    @ 080be866 1022
    subs r0,r2,r0    @ 080be868 101a
    .hword 0x4643    @ 080be86a 4346
    muls r3,r0    @ 080be86c 4343
    adds r0,r3,#0x0    @ 080be86e 181c
    subs r0,r5,r0    @ 080be870 281a
    add r0,r10                               @ 080be872 5044
    orrs r0,r6    @ 080be874 3043
    movs r2,#0xc0    @ 080be876 c022
    lsls r2,r2,#0x6    @ 080be878 9201
    adds r1,r2,#0x0    @ 080be87a 111c
    .hword 0x464c    @ 080be87c 4c46
    orrs r4,r1    @ 080be87e 0c43
    lsls r4,r4,#0x10    @ 080be880 2404
    lsrs r4,r4,#0x10    @ 080be882 240c
    ldr r1, DAT_080be948                     @ 080be884 3049
    adds r2,r4,#0x0    @ 080be886 221c
    bl write_oam_entry_from_packed_args      @ 080be888 37f070fc
    ldr r3, DAT_080be944                     @ 080be88c 2d4b
    ldrb r3,[r3,#0x11]                       @ 080be88e 5b7c
    lsls r0,r3,#0x1    @ 080be890 5800
    movs r1,#0x10    @ 080be892 1021
    subs r0,r1,r0    @ 080be894 081a
    .hword 0x4642    @ 080be896 4246
    muls r2,r0    @ 080be898 4243
    adds r0,r2,#0x0    @ 080be89a 101c
    subs r0,r5,r0    @ 080be89c 281a
    add r0,r10                               @ 080be89e 5044
    orrs r0,r6    @ 080be8a0 3043
    ldr r1, DAT_080be94c                     @ 080be8a2 2a49
    adds r2,r4,#0x0    @ 080be8a4 221c
    bl write_oam_entry_from_packed_args      @ 080be8a6 37f061fc
    movs r3,#0x8    @ 080be8aa 0823
    add r9,r3                                @ 080be8ac 9944
    adds r5,#0x40    @ 080be8ae 4035
    subs r7,#0x1    @ 080be8b0 013f
    cmp r7,#0x0                              @ 080be8b2 002f
    bge LAB_080be860                         @ 080be8b4 d4da
    movs r7,#0x0    @ 080be8b6 0027
    movs r0,#0x10    @ 080be8b8 1020
    .hword 0x4682    @ 080be8ba 8246
    movs r1,#0x80    @ 080be8bc 8021
    lsls r1,r1,#0x2    @ 080be8be 8900
    .hword 0x4689    @ 080be8c0 8946
    ldr r2,[sp,#0x0]                         @ 080be8c2 009a
    lsls r6,r2,#0x10    @ 080be8c4 1604
    movs r5,#0xc0    @ 080be8c6 c025
    rsbs r5,r5,#0    @ 080be8c8 6d42
LAB_080be8ca:
    ldr r3, DAT_080be944                     @ 080be8ca 1e4b
    ldrb r3,[r3,#0x11]                       @ 080be8cc 5b7c
    lsls r0,r3,#0x1    @ 080be8ce 5800
    .hword 0x4651    @ 080be8d0 5146
    subs r0,r1,r0    @ 080be8d2 081a
    .hword 0x4642    @ 080be8d4 4246
    muls r2,r0    @ 080be8d6 4243
    adds r0,r2,#0x0    @ 080be8d8 101c
    adds r0,r0,r5    @ 080be8da 4019
    add r0,r9                                @ 080be8dc 4844
    orrs r0,r6    @ 080be8de 3043
    lsls r4,r7,#0x3    @ 080be8e0 fc00
    movs r3,#0xa0    @ 080be8e2 a023
    lsls r3,r3,#0x2    @ 080be8e4 9b00
    adds r4,r4,r3    @ 080be8e6 e418
    movs r2,#0xc0    @ 080be8e8 c022
    lsls r2,r2,#0x6    @ 080be8ea 9201
    adds r1,r2,#0x0    @ 080be8ec 111c
    orrs r4,r1    @ 080be8ee 0c43
    lsls r4,r4,#0x10    @ 080be8f0 2404
    lsrs r4,r4,#0x10    @ 080be8f2 240c
    ldr r1, DAT_080be948                     @ 080be8f4 1449
    adds r2,r4,#0x0    @ 080be8f6 221c
    bl write_oam_entry_from_packed_args      @ 080be8f8 37f038fc
    ldr r3, DAT_080be944                     @ 080be8fc 114b
    ldrb r3,[r3,#0x11]                       @ 080be8fe 5b7c
    lsls r0,r3,#0x1    @ 080be900 5800
    .hword 0x4651    @ 080be902 5146
    subs r0,r1,r0    @ 080be904 081a
    .hword 0x4642    @ 080be906 4246
    muls r2,r0    @ 080be908 4243
    adds r0,r2,#0x0    @ 080be90a 101c
    adds r0,r0,r5    @ 080be90c 4019
    add r0,r9                                @ 080be90e 4844
    orrs r0,r6    @ 080be910 3043
    ldr r1, DAT_080be94c                     @ 080be912 0e49
    adds r2,r4,#0x0    @ 080be914 221c
    bl write_oam_entry_from_packed_args      @ 080be916 37f029fc
    adds r5,#0x40    @ 080be91a 4035
    adds r7,#0x1    @ 080be91c 0137
    cmp r7,#0x2                              @ 080be91e 022f
    ble LAB_080be8ca                         @ 080be920 d3dd
    ldr r0, PTR_BLDY_080be950                @ 080be922 0b48
    ldr r2, DAT_080be944                     @ 080be924 074a
    movs r1,#0x8    @ 080be926 0821
    ldrb r3,[r2,#0x11]                       @ 080be928 537c
    subs r1,r1,r3    @ 080be92a c91a
    strh r1,[r0,#0x0]                        @ 080be92c 0180
    ldrb r0,[r2,#0x11]                       @ 080be92e 507c
    adds r0,#0x1    @ 080be930 0130
    strb r0,[r2,#0x11]                       @ 080be932 5074
    lsls r0,r0,#0x18    @ 080be934 0006
    lsrs r0,r0,#0x18    @ 080be936 000e
    cmp r0,#0x7                              @ 080be938 0728
    bls LAB_080be96c                         @ 080be93a 17d9
    ldrb r0,[r2,#0x10]                       @ 080be93c 107c
    adds r0,#0x1    @ 080be93e 0130
    strb r0,[r2,#0x10]                       @ 080be940 1074
    b LAB_080be96c                           @ 080be942 13e0
DAT_080be944:
    .word  gBannerState                   @ 080be944 c0fe0102
DAT_080be948:
    .word  0x000048c0                     @ 080be948 c0480000
DAT_080be94c:
    .word  0x000040c0                     @ 080be94c c0400000
PTR_BLDY_080be950:
    .word  BLDY                           @ 080be950 54000004
switchD_080be626__caseD_4:
    bl disable_blend_and_clear_step          @ 080be954 36f03efe
    movs r2,#0x80    @ 080be958 8022
    lsls r2,r2,#0x13    @ 080be95a d204
    ldrh r1,[r2,#0x0]                        @ 080be95c 1188
    ldr r0, DAT_080be970                     @ 080be95e 0448
    ands r0,r1    @ 080be960 0840
LAB_080be962:
    strh r0,[r2,#0x0]                        @ 080be962 1080
    ldr r1, DAT_080be974                     @ 080be964 0349
    ldrb r0,[r1,#0x10]                       @ 080be966 087c
    adds r0,#0x1    @ 080be968 0130
    strb r0,[r1,#0x10]                       @ 080be96a 0874
LAB_080be96c:
    movs r0,#0x1    @ 080be96c 0120
    b LAB_080be9a4                           @ 080be96e 19e0
DAT_080be970:
    .word  0x00001fff                     @ 080be970 ff1f0000
DAT_080be974:
    .word  gBannerState                   @ 080be974 c0fe0102
LAB_080be978:
    ldr r4, DAT_080be9b4                     @ 080be978 0e4c
    movs r1,#0x88    @ 080be97a 8821
    lsls r1,r1,#0x2    @ 080be97c 8900
    adds r0,r4,r1    @ 080be97e 6018
    ldrh r0,[r0,#0x0]                        @ 080be980 0088
    lsls r0,r0,#0x16    @ 080be982 8005
    lsrs r0,r0,#0x18    @ 080be984 000e
    bl set_channel_if_changed                @ 080be986 3bf0a9f8
    movs r0,#0x2    @ 080be98a 0220
    rsbs r0,r0,#0    @ 080be98c 4042
    ldrb r2,[r5,#0x0]                        @ 080be98e 2a78
    ands r0,r2    @ 080be990 1040
    strb r0,[r5,#0x0]                        @ 080be992 2870
    ldr r3, DAT_080be9b8                     @ 080be994 084b
    adds r4,r4,r3    @ 080be996 e418
    movs r0,#0x5    @ 080be998 0520
    rsbs r0,r0,#0    @ 080be99a 4042
    ldrb r1,[r4,#0x0]                        @ 080be99c 2178
    ands r0,r1    @ 080be99e 0840
    strb r0,[r4,#0x0]                        @ 080be9a0 2070
    movs r0,#0x0    @ 080be9a2 0020
LAB_080be9a4:
    add sp,#0x4                              @ 080be9a4 01b0
    pop {r3,r4,r5}                           @ 080be9a6 38bc
    .hword 0x4698    @ 080be9a8 9846
    .hword 0x46a1    @ 080be9aa a146
    .hword 0x46aa    @ 080be9ac aa46
    pop {r4,r5,r6,r7}                        @ 080be9ae f0bc
    pop {r1}                                 @ 080be9b0 02bc
    bx r1                                    @ 080be9b2 0847
DAT_080be9b4:
    .word  0x02023130                     @ 080be9b4 30310202
DAT_080be9b8:
    .word  0x00000215                     @ 080be9b8 15020000

@ pack card shop entry: loads AOB (All-Or-Bust) sprite GFX based on mode parameter r0 in {0,5,7,8}. Copies palette (32 bytes) to BG palette slot 0x050002a0, then calls tile_2d_row_copy to write tile data to OBJ VRAM 0x06014000. Initializes AOB animation context at 0x0201fedc via init_aob_ctx_from_ptnsect + init_aob_ctx_with_anm_entry. Sets context flags [+0x13] |= 0x11, [+0xe] := 0x2. Returns r0=1 on success; r0=0 if mode not in {0,5,7,8}.
@ 
@ Constants:
@ - OBJ_VRAM_TILE_BASE = 0x06014000 (OBJ tile VRAM)
@ - BG_PAL_SLOT = 0x050002a0 (BG palette pack banner slot)
@ - AOB_CTX_BASE = 0x0201fedc (pack AOB animation context)
@ - ROM_TILE_MODE0 = 0x098a3100 (mode0 tile ROM source; tile height r6=0xc)
@ - ROM_PAL_MODE0 = 0x098a4900 (mode0 palette ROM source)
@ - ROM_TILE_MODE5 = 0x098a17d8 (mode5 tile ROM source; tile height r6=0xc)
@ - ROM_PAL_MODE5 = 0x098a2fd8 (mode5 palette ROM source)
@ - ROM_TILE_MODE7 = 0x0989f670 (mode7 tile ROM source; tile height r6=0x10)
@ - ROM_PAL_MODE7 = 0x098a1670 (mode7 palette ROM source)
@ - ROM_TILE_MODE8 = 0x098a3100 (mode8 tile ROM source; tile height r6=0xc)
@ - ROM_PAL_MODE8 = 0x098a4920 (mode8 palette ROM source)
@ - FLAG_VIS = 0x11 (visible flag combination)
@ - MODE_BYTE = 0x2 (animation mode number)
load_pack_aob_gfx_by_mode:
    push {r4,r5,r6,r7,lr}                    @ 080be9bc f0b5
    adds r7,r1,#0x0    @ 080be9be 0f1c
    cmp r0,#0x5                              @ 080be9c0 0528
    beq LAB_080be9f0                         @ 080be9c2 15d0
    cmp r0,#0x5                              @ 080be9c4 0528
    bgt LAB_080be9ce                         @ 080be9c6 02dc
    cmp r0,#0x0                              @ 080be9c8 0028
    beq LAB_080be9d8                         @ 080be9ca 05d0
    b LAB_080bea38                           @ 080be9cc 34e0
LAB_080be9ce:
    cmp r0,#0x7                              @ 080be9ce 0728
    beq LAB_080bea08                         @ 080be9d0 1ad0
    cmp r0,#0x8                              @ 080be9d2 0828
    beq LAB_080bea20                         @ 080be9d4 24d0
    b LAB_080bea38                           @ 080be9d6 2fe0
LAB_080be9d8:
    movs r6,#0xc    @ 080be9d8 0c26
    ldr r4, DAT_080be9e4                     @ 080be9da 024c
    ldr r1, DAT_080be9e8                     @ 080be9dc 0249
    ldr r5, DAT_080be9ec                     @ 080be9de 034d
    b LAB_080bea3c                           @ 080be9e0 2ce0
    .zero  0x2
DAT_080be9e4:
    .word  0x098a3100                     @ 080be9e4 00318a09
DAT_080be9e8:
    .word  0x098a4900                     @ 080be9e8 00498a09
DAT_080be9ec:
    .word  0x098a4940                     @ 080be9ec 40498a09
LAB_080be9f0:
    movs r6,#0xc    @ 080be9f0 0c26
    ldr r4, DAT_080be9fc                     @ 080be9f2 024c
    ldr r1, DAT_080bea00                     @ 080be9f4 0249
    ldr r5, DAT_080bea04                     @ 080be9f6 034d
    b LAB_080bea3c                           @ 080be9f8 20e0
    .zero  0x2
DAT_080be9fc:
    .word  0x098a17d8                     @ 080be9fc d8178a09
DAT_080bea00:
    .word  0x098a2fd8                     @ 080bea00 d82f8a09
DAT_080bea04:
    .word  0x098a2ff8                     @ 080bea04 f82f8a09
LAB_080bea08:
    movs r6,#0x10    @ 080bea08 1026
    ldr r4, DAT_080bea14                     @ 080bea0a 024c
    ldr r1, DAT_080bea18                     @ 080bea0c 0249
    ldr r5, DAT_080bea1c                     @ 080bea0e 034d
    b LAB_080bea3c                           @ 080bea10 14e0
    .zero  0x2
DAT_080bea14:
    .word  0x0989f670                     @ 080bea14 70f68909
DAT_080bea18:
    .word  0x098a1670                     @ 080bea18 70168a09
DAT_080bea1c:
    .word  0x098a1690                     @ 080bea1c 90168a09
LAB_080bea20:
    movs r6,#0xc    @ 080bea20 0c26
    ldr r4, DAT_080bea2c                     @ 080bea22 024c
    ldr r1, DAT_080bea30                     @ 080bea24 0249
    ldr r5, DAT_080bea34                     @ 080bea26 034d
    b LAB_080bea3c                           @ 080bea28 08e0
    .zero  0x2
DAT_080bea2c:
    .word  0x098a3100                     @ 080bea2c 00318a09
DAT_080bea30:
    .word  0x098a4920                     @ 080bea30 20498a09
DAT_080bea34:
    .word  0x098a4940                     @ 080bea34 40498a09
LAB_080bea38:
    movs r0,#0x0    @ 080bea38 0020
    b LAB_080bea7c                           @ 080bea3a 1fe0
LAB_080bea3c:
    ldr r0, DAT_080bea84                     @ 080bea3c 1148
    movs r2,#0x20    @ 080bea3e 2022
    bl copy_bytes_by_halfword                @ 080bea40 36f030fa
    ldr r0, DAT_080bea88                     @ 080bea44 1048
    adds r1,r4,#0x0    @ 080bea46 211c
    movs r2,#0x10    @ 080bea48 1022
    adds r3,r6,#0x0    @ 080bea4a 331c
    bl tile_2d_row_copy                      @ 080bea4c 38f042fd
    ldr r4, DAT_080bea8c                     @ 080bea50 0e4c
    ldr r2, DAT_080bea90                     @ 080bea52 0f4a
    adds r0,r4,#0x0    @ 080bea54 201c
    adds r1,r5,#0x0    @ 080bea56 291c
    movs r3,#0x1    @ 080bea58 0123
    bl init_aob_ctx_from_ptnsect             @ 080bea5a 39f0a3f9
    movs r0,#0x1    @ 080bea5e 0120
    ldrb r1,[r4,#0x13]                       @ 080bea60 e17c
    orrs r0,r1    @ 080bea62 0843
    movs r1,#0x10    @ 080bea64 1021
    orrs r0,r1    @ 080bea66 0843
    strb r0,[r4,#0x13]                       @ 080bea68 e074
    movs r0,#0x2    @ 080bea6a 0220
    strb r0,[r4,#0xe]                        @ 080bea6c a073
    lsls r1,r7,#0x10    @ 080bea6e 3904
    lsrs r1,r1,#0x10    @ 080bea70 090c
    adds r0,r4,#0x0    @ 080bea72 201c
    movs r2,#0x0    @ 080bea74 0022
    bl init_aob_ctx_with_anm_entry           @ 080bea76 39f0e7f9
    movs r0,#0x1    @ 080bea7a 0120
LAB_080bea7c:
    pop {r4,r5,r6,r7}                        @ 080bea7c f0bc
    pop {r1}                                 @ 080bea7e 02bc
    bx r1                                    @ 080bea80 0847
    .zero  0x2
DAT_080bea84:
    .word  0x050002a0                     @ 080bea84 a0020005
DAT_080bea88:
    .word  0x06014000                     @ 080bea88 00400106
DAT_080bea8c:
    .word  0x0201fedc                     @ 080bea8c dcfe0102
DAT_080bea90:
    .word  0x02000005                     @ 080bea90 05000002

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x15 子状态机, 待详细分析.
play_ui_effect_15:
    push {r4,r5,r6,r7,lr}                    @ 080bea94 f0b5
    .hword 0x4657    @ 080bea96 5746
    .hword 0x464e    @ 080bea98 4e46
    .hword 0x4645    @ 080bea9a 4546
    push {r5,r6,r7}                          @ 080bea9c e0b4
    sub sp,#0x1c                             @ 080bea9e 87b0
    ldr r7, DAT_080beae8                     @ 080beaa0 114f
    movs r0,#0x0    @ 080beaa2 0020
    str r0,[sp,#0x10]                        @ 080beaa4 0490
    ldr r1,[r7,#0x4]                         @ 080beaa6 7968
    .hword 0x4688    @ 080beaa8 8846
    ldrh r2,[r7,#0x4]                        @ 080beaaa ba88
    .hword 0x4692    @ 080beaac 9246
    .hword 0x4650    @ 080beaae 5046
    movs r1,#0xd    @ 080beab0 0d21
    movs r2,#0x0    @ 080beab2 0022
    bl get_field_slot_tile_vram_addr         @ 080beab4 04f06cfe
    str r0,[sp,#0x14]                        @ 080beab8 0590
    .hword 0x4640    @ 080beaba 4046
    movs r1,#0xd    @ 080beabc 0d21
    movs r2,#0x0    @ 080beabe 0022
    bl resolve_zone_oam_base_coords_by_type  @ 080beac0 04f074fd
    subs r1,r0,#0x4    @ 080beac4 011f
    lsls r1,r1,#0x10    @ 080beac6 0904
    lsrs r1,r1,#0x10    @ 080beac8 090c
    .hword 0x4689    @ 080beaca 8946
    lsrs r0,r0,#0x10    @ 080beacc 000c
    subs r0,#0x4    @ 080beace 0438
    lsls r0,r0,#0x10    @ 080bead0 0004
    lsrs r0,r0,#0x10    @ 080bead2 000c
    str r0,[sp,#0x18]                        @ 080bead4 0690
    ldrb r4,[r7,#0x10]                       @ 080bead6 3c7c
    cmp r4,#0x1                              @ 080bead8 012c
    bne LAB_080beade                         @ 080beada 00d1
    b LAB_080bec5c                           @ 080beadc bee0
LAB_080beade:
    cmp r4,#0x1                              @ 080beade 012c
    bgt LAB_080beaec                         @ 080beae0 04dc
    cmp r4,#0x0                              @ 080beae2 002c
    beq LAB_080beafa                         @ 080beae4 09d0
    b LAB_080beda8                           @ 080beae6 5fe1
DAT_080beae8:
    .word  gBannerState                   @ 080beae8 c0fe0102
LAB_080beaec:
    cmp r4,#0x2                              @ 080beaec 022c
    bne LAB_080beaf2                         @ 080beaee 00d1
    b LAB_080bed24                           @ 080beaf0 18e1
LAB_080beaf2:
    cmp r4,#0x3                              @ 080beaf2 032c
    bne LAB_080beaf8                         @ 080beaf4 00d1
    b LAB_080bed90                           @ 080beaf6 4be1
LAB_080beaf8:
    b LAB_080beda8                           @ 080beaf8 56e1
LAB_080beafa:
    ldr r5, DAT_080bebe0                     @ 080beafa 394d
    ldr r4, DAT_080bebe4                     @ 080beafc 394c
    adds r5,r5,r4    @ 080beafe 2d19
    ldrb r2,[r5,#0x0]                        @ 080beb00 2a78
    lsls r0,r2,#0x19    @ 080beb02 5006
    lsrs r0,r0,#0x1f    @ 080beb04 c00f
    movs r1,#0x1    @ 080beb06 0121
    subs r1,r1,r0    @ 080beb08 091a
    movs r0,#0x1    @ 080beb0a 0120
    ands r1,r0    @ 080beb0c 0140
    lsls r1,r1,#0x6    @ 080beb0e 8901
    movs r0,#0x41    @ 080beb10 4120
    rsbs r0,r0,#0    @ 080beb12 4042
    ands r0,r2    @ 080beb14 1040
    orrs r0,r1    @ 080beb16 0843
    strb r0,[r5,#0x0]                        @ 080beb18 2870
    movs r4,#0x1    @ 080beb1a 0124
    .hword 0x4640    @ 080beb1c 4046
    ands r0,r4    @ 080beb1e 2040
    ldr r1, DAT_080bebe8                     @ 080beb20 3149
    adds r7,r0,#0x0    @ 080beb22 071c
    muls r7,r1    @ 080beb24 4f43
    ldr r0, DAT_080bebec                     @ 080beb26 3148
    .hword 0x4681    @ 080beb28 8146
    adds r6,r7,r0    @ 080beb2a 3e18
    ldr r1,[r6,#0x0]                         @ 080beb2c 3168
    lsls r0,r1,#0x2    @ 080beb2e 8800
    lsrs r0,r0,#0x18    @ 080beb30 000e
    lsls r0,r0,#0x1    @ 080beb32 4000
    lsls r1,r1,#0x12    @ 080beb34 8904
    lsrs r1,r1,#0x1f    @ 080beb36 c90f
    adds r0,r0,r1    @ 080beb38 4018
    bl ensure_card_id_cache_entry            @ 080beb3a 0df0c5fe
    ldrb r2,[r5,#0x0]                        @ 080beb3e 2a78
    lsls r1,r2,#0x19    @ 080beb40 5106
    lsrs r1,r1,#0x1f    @ 080beb42 c90f
    subs r4,r4,r1    @ 080beb44 641a
    movs r3,#0x80    @ 080beb46 8023
    lsls r3,r3,#0x2    @ 080beb48 9b00
    adds r1,r4,#0x0    @ 080beb4a 211c
    movs r2,#0x0    @ 080beb4c 0022
    bl load_card_list_small_image            @ 080beb4e 04f035fc
    ldr r1,[r6,#0x0]                         @ 080beb52 3168
    lsls r0,r1,#0x2    @ 080beb54 8800
    lsrs r0,r0,#0x18    @ 080beb56 000e
    lsls r0,r0,#0x1    @ 080beb58 4000
    lsls r1,r1,#0x12    @ 080beb5a 8904
    lsrs r1,r1,#0x1f    @ 080beb5c c90f
    adds r0,r0,r1    @ 080beb5e 4018
    bl ensure_card_id_cache_entry            @ 080beb60 0df0b2fe
    ldrb r5,[r5,#0x0]                        @ 080beb64 2d78
    lsls r1,r5,#0x19    @ 080beb66 6906
    lsrs r1,r1,#0x1f    @ 080beb68 c90f
    movs r3,#0x82    @ 080beb6a 8223
    lsls r3,r3,#0x2    @ 080beb6c 9b00
    movs r2,#0x0    @ 080beb6e 0022
    bl load_card_list_small_image            @ 080beb70 04f024fc
    ldr r0, DAT_080bebf0                     @ 080beb74 1e48
    add r0,r9                                @ 080beb76 4844
    adds r0,r7,r0    @ 080beb78 3818
    ldr r0,[r0,#0x0]                         @ 080beb7a 0068
    cmp r0,#0x0                              @ 080beb7c 0028
    beq LAB_080bec0c                         @ 080beb7e 45d0
    .hword 0x4640    @ 080beb80 4046
    movs r1,#0xd    @ 080beb82 0d21
    movs r2,#0x1    @ 080beb84 0122
    bl get_zone_card_attribute_by_type       @ 080beb86 7cf747fd
    cmp r0,#0x0                              @ 080beb8a 0028
    beq LAB_080bec08                         @ 080beb8c 3cd0
    .hword 0x4648    @ 080beb8e 4846
    adds r0,#0x4    @ 080beb90 0430
    adds r0,r7,r0    @ 080beb92 3818
    ldr r1,[r0,#0x0]                         @ 080beb94 0168
    lsls r0,r1,#0x2    @ 080beb96 8800
    lsrs r0,r0,#0x18    @ 080beb98 000e
    lsls r0,r0,#0x1    @ 080beb9a 4000
    lsls r1,r1,#0x12    @ 080beb9c 8904
    lsrs r1,r1,#0x1f    @ 080beb9e c90f
    adds r0,r0,r1    @ 080beba0 4018
    bl ensure_card_id_cache_entry            @ 080beba2 0df091fe
    ldr r4, PTR_card_image_index_080bebf4    @ 080beba6 134c
    lsls r2,r0,#0x1    @ 080beba8 4200
    movs r3,#0x0    @ 080bebaa 0023
    ldr r0, DAT_080bebf8                     @ 080bebac 1248
    ldrh r0,[r0,#0x0]                        @ 080bebae 0088
    lsrs r0,r0,#0x8    @ 080bebb0 000a
    cmp r0,#0x4a                             @ 080bebb2 4a28
    bne LAB_080bebc6                         @ 080bebb4 07d1
    ldr r1, DAT_080bebfc                     @ 080bebb6 1149
    ldr r0, DAT_080bec00                     @ 080bebb8 1148
    adds r1,r1,r0    @ 080bebba 0918
    movs r0,#0x7    @ 080bebbc 0720
    ldrb r1,[r1,#0x0]                        @ 080bebbe 0978
    ands r0,r1    @ 080bebc0 0840
    cmp r0,#0x0                              @ 080bebc2 0028
    beq LAB_080bebc8                         @ 080bebc4 00d0
LAB_080bebc6:
    movs r3,#0x1    @ 080bebc6 0123
LAB_080bebc8:
    orrs r2,r3    @ 080bebc8 1a43
    lsls r0,r2,#0x1    @ 080bebca 5000
    adds r0,r4,r0    @ 080bebcc 2018
    ldrh r2,[r0,#0x0]                        @ 080bebce 0288
    lsls r1,r2,#0x3    @ 080bebd0 d100
    adds r1,r1,r2    @ 080bebd2 8918
    lsls r1,r1,#0x7    @ 080bebd4 c901
    ldr r0, PTR_card_mini_frame_tile_data_080bec04 @ 080bebd6 0b48
    adds r1,r1,r0    @ 080bebd8 0918
    str r1,[sp,#0x10]                        @ 080bebda 0491
    b LAB_080bec0c                           @ 080bebdc 16e0
    .zero  0x2
DAT_080bebe0:
    .word  0x02023130                     @ 080bebe0 30310202
DAT_080bebe4:
    .word  0x00000215                     @ 080bebe4 15020000
DAT_080bebe8:
    .word  0x00000868                     @ 080bebe8 68080000
DAT_080bebec:
    .word  0x0201c740                     @ 080bebec 40c70102
DAT_080bebf0:
    .word  0xfffffdb0                     @ 080bebf0 b0fdffff
PTR_card_image_index_080bebf4:
    .word  card_image_index               @ 080bebf4 005c5b09
DAT_080bebf8:
    .word  0x080000ae                     @ 080bebf8 ae000008
DAT_080bebfc:
    .word  0x02000000                     @ 080bebfc 00000002
DAT_080bec00:
    .word  0x00006c2c                     @ 080bec00 2c6c0000
PTR_card_mini_frame_tile_data_080bec04:
    .word  card_mini_frame_tile_data      @ 080bec04 80623209
LAB_080bec08:
    ldr r4, DAT_080bec34                     @ 080bec08 0a4c
    str r4,[sp,#0x10]                        @ 080bec0a 0494
LAB_080bec0c:
    ldr r0,[sp,#0x10]                        @ 080bec0c 0498
    cmp r0,#0x0                              @ 080bec0e 0028
    beq LAB_080bec38                         @ 080bec10 12d0
    ldr r2,[sp,#0x14]                        @ 080bec12 059a
    adds r1,r0,#0x0    @ 080bec14 011c
    movs r3,#0x90    @ 080bec16 9023
    lsls r3,r3,#0x1    @ 080bec18 5b00
LAB_080bec1a:
    ldrh r4,[r1,#0x0]                        @ 080bec1a 0c88
    lsrs r0,r4,#0x8    @ 080bec1c 200a
    lsls r0,r0,#0x8    @ 080bec1e 0002
    ldrb r4,[r1,#0x0]                        @ 080bec20 0c78
    orrs r0,r4    @ 080bec22 2043
    strh r0,[r2,#0x0]                        @ 080bec24 1080
    adds r2,#0x2    @ 080bec26 0232
    adds r1,#0x2    @ 080bec28 0231
    subs r3,#0x1    @ 080bec2a 013b
    cmp r3,#0x0                              @ 080bec2c 002b
    bne LAB_080bec1a                         @ 080bec2e f4d1
    b LAB_080bec46                           @ 080bec30 09e0
    .zero  0x2
DAT_080bec34:
    .word  0x0984fbcc                     @ 080bec34 ccfb8409
LAB_080bec38:
    .hword 0x4641    @ 080bec38 4146
    lsls r0,r1,#0x10    @ 080bec3a 0804
    lsrs r0,r0,#0x10    @ 080bec3c 000c
    movs r1,#0xd    @ 080bec3e 0d21
    movs r2,#0x0    @ 080bec40 0022
    bl update_field_slot_tile_display        @ 080bec42 04f01dfe
LAB_080bec46:
    movs r0,#0x3    @ 080bec46 0320
    bl sync_state_and_init_sprite            @ 080bec48 3af034ff
    ldr r1, DAT_080bec58                     @ 080bec4c 0249
    ldrb r0,[r1,#0x10]                       @ 080bec4e 087c
    adds r0,#0x1    @ 080bec50 0130
    strb r0,[r1,#0x10]                       @ 080bec52 0874
LAB_080bec54:
    movs r0,#0x1    @ 080bec54 0120
    b LAB_080bedc6                           @ 080bec56 b6e0
DAT_080bec58:
    .word  gBannerState                   @ 080bec58 c0fe0102
LAB_080bec5c:
    movs r2,#0x80    @ 080bec5c 8022
    lsls r2,r2,#0x2    @ 080bec5e 9200
    .hword 0x4692    @ 080bec60 9246
    ldr r1, DAT_080bed18                     @ 080bec62 2d49
    .hword 0x4668    @ 080bec64 6846
    movs r2,#0xa    @ 080bec66 0a22
    bl memcpy                                @ 080bec68 4ff078fe
    movs r5,#0x0    @ 080bec6c 0025
    ldrb r0,[r7,#0x11]                       @ 080bec6e 787c
    cmp r0,#0x1                              @ 080bec70 0128
    bls LAB_080bec7a                         @ 080bec72 02d9
    movs r1,#0x82    @ 080bec74 8221
    lsls r1,r1,#0x2    @ 080bec76 8900
    .hword 0x468a    @ 080bec78 8a46
LAB_080bec7a:
    ldr r0, DAT_080bed1c                     @ 080bec7a 2848
    ldr r0,[r0,#0x4]                         @ 080bec7c 4068
    eors r0,r4    @ 080bec7e 6040
    cmp r8,r0                                @ 080bec80 8045
    bne LAB_080bec86                         @ 080bec82 00d1
    movs r5,#0x40    @ 080bec84 4025
LAB_080bec86:
    ldr r2, DAT_080bed20                     @ 080bec86 264a
    .hword 0x4690    @ 080bec88 9046
    ldrb r4,[r7,#0x11]                       @ 080bec8a 7c7c
    lsls r0,r4,#0x1    @ 080bec8c 6000
    add r0,sp                                @ 080bec8e 6844
    ldrh r0,[r0,#0x0]                        @ 080bec90 0088
    lsls r0,r0,#0x2    @ 080bec92 8000
    movs r6,#0x7f    @ 080bec94 7f26
    ands r0,r6    @ 080bec96 3040
    lsls r0,r0,#0x1    @ 080bec98 4000
    add r0,r8                                @ 080bec9a 4044
    ldrh r2,[r0,#0x0]                        @ 080bec9c 0288
    lsls r1,r2,#0x2    @ 080bec9e 9100
    adds r1,r2,r1    @ 080beca0 5118
    movs r4,#0x80    @ 080beca2 8024
    lsls r4,r4,#0x1    @ 080beca4 6400
    adds r1,r1,r4    @ 080beca6 0919
    adds r0,r5,#0x0    @ 080beca8 281c
    ands r0,r6    @ 080becaa 3040
    lsls r0,r0,#0x1    @ 080becac 4000
    add r0,r8                                @ 080becae 4044
    movs r2,#0x0    @ 080becb0 0022
    ldrsh r0,[r0,r2]                         @ 080becb2 805e
    adds r2,r0,#0x0    @ 080becb4 021c
    muls r2,r1    @ 080becb6 4a43
    adds r0,r5,#0x0    @ 080becb8 281c
    adds r0,#0x20    @ 080becba 2030
    ands r0,r6    @ 080becbc 3040
    lsls r0,r0,#0x1    @ 080becbe 4000
    add r0,r8                                @ 080becc0 4044
    movs r4,#0x0    @ 080becc2 0024
    ldrsh r3,[r0,r4]                         @ 080becc4 035f
    adds r4,r3,#0x0    @ 080becc6 1c1c
    muls r4,r1    @ 080becc8 4c43
    adds r5,#0x40    @ 080becca 4035
    ands r5,r6    @ 080beccc 3540
    lsls r5,r5,#0x1    @ 080becce 6d00
    add r5,r8                                @ 080becd0 4544
    ldr r1,[sp,#0x18]                        @ 080becd2 0699
    lsls r0,r1,#0x10    @ 080becd4 0804
    .hword 0x4649    @ 080becd6 4946
    orrs r1,r0    @ 080becd8 0143
    .hword 0x4689    @ 080becda 8946
    .hword 0x4650    @ 080becdc 5046
    lsls r1,r0,#0xf    @ 080becde c103
    movs r0,#0x80    @ 080bece0 8020
    orrs r1,r0    @ 080bece2 0143
    lsls r2,r2,#0x8    @ 080bece4 1202
    lsrs r2,r2,#0x10    @ 080bece6 120c
    lsls r4,r4,#0x8    @ 080bece8 2402
    lsrs r4,r4,#0x10    @ 080becea 240c
    lsls r4,r4,#0x10    @ 080becec 2404
    orrs r2,r4    @ 080becee 2243
    lsls r3,r3,#0x10    @ 080becf0 1b04
    lsrs r3,r3,#0x10    @ 080becf2 1b0c
    ldrh r5,[r5,#0x0]                        @ 080becf4 2d88
    lsls r0,r5,#0x10    @ 080becf6 2804
    orrs r3,r0    @ 080becf8 0343
    .hword 0x4648    @ 080becfa 4846
    bl write_oam_sprite_entry_by_flip_mode   @ 080becfc 38f0f4fa
    ldrb r0,[r7,#0x11]                       @ 080bed00 787c
    adds r1,r0,#0x1    @ 080bed02 411c
    strb r1,[r7,#0x11]                       @ 080bed04 7974
    lsls r0,r0,#0x18    @ 080bed06 0006
    lsrs r0,r0,#0x18    @ 080bed08 000e
    cmp r0,#0x3                              @ 080bed0a 0328
    bls LAB_080bec54                         @ 080bed0c a2d9
    ldrb r0,[r7,#0x10]                       @ 080bed0e 387c
    adds r0,#0x1    @ 080bed10 0130
    strb r0,[r7,#0x10]                       @ 080bed12 3874
    b LAB_080bec54                           @ 080bed14 9ee7
    .zero  0x2
DAT_080bed18:
    .word  0x09e491f0                     @ 080bed18 f091e409
DAT_080bed1c:
    .word  0x0201e2a0                     @ 080bed1c a0e20102
DAT_080bed20:
    .word  rom_sin_table_q8               @ 080bed20 f0f8e509
LAB_080bed24:
    ldr r6, PTR_gP1LifePoints_080bed7c       @ 080bed24 154e
    movs r4,#0x1    @ 080bed26 0124
    .hword 0x4641    @ 080bed28 4146
    ands r4,r1    @ 080bed2a 0c40
    ldr r0, DAT_080bed80                     @ 080bed2c 1448
    adds r5,r4,#0x0    @ 080bed2e 251c
    muls r5,r0    @ 080bed30 4543
    adds r0,r6,#0x0    @ 080bed32 301c
    adds r0,#0x10    @ 080bed34 1030
    adds r0,r5,r0    @ 080bed36 2818
    ldrh r2,[r0,#0x0]                        @ 080bed38 0288
    .hword 0x4650    @ 080bed3a 5046
    movs r1,#0xd    @ 080bed3c 0d21
    bl render_field_zone_card_tile_by_type   @ 080bed3e 04f05dfe
    ldr r1, DAT_080bed84                     @ 080bed42 1049
    ldr r2, DAT_080bed88                     @ 080bed44 104a
    adds r1,r1,r2    @ 080bed46 8918
    movs r0,#0x40    @ 080bed48 4020
    ldrb r1,[r1,#0x0]                        @ 080bed4a 0978
    ands r0,r1    @ 080bed4c 0840
    cmp r0,#0x0                              @ 080bed4e 0028
    beq LAB_080beda0                         @ 080bed50 26d0
    movs r1,#0x98    @ 080bed52 9821
    lsls r1,r1,#0x2    @ 080bed54 8900
    adds r0,r6,r1    @ 080bed56 7018
    adds r0,r5,r0    @ 080bed58 2818
    ldr r1,[r0,#0x0]                         @ 080bed5a 0168
    lsls r0,r1,#0x2    @ 080bed5c 8800
    lsrs r0,r0,#0x18    @ 080bed5e 000e
    lsls r0,r0,#0x1    @ 080bed60 4000
    lsls r1,r1,#0x12    @ 080bed62 8904
    lsrs r1,r1,#0x1f    @ 080bed64 c90f
    adds r0,r0,r1    @ 080bed66 4018
    ldr r1, DAT_080bed8c                     @ 080bed68 0849
    orrs r4,r1    @ 080bed6a 0c43
    str r4,[sp,#0xc]                         @ 080bed6c 0394
    bl ensure_card_id_cache_entry            @ 080bed6e 0df0abfd
    add r1,sp,#0xc                           @ 080bed72 03a9
    movs r2,#0x1    @ 080bed74 0122
    bl render_large_card_display_by_mode     @ 080bed76 0cf029fa
    b LAB_080beda0                           @ 080bed7a 11e0
PTR_gP1LifePoints_080bed7c:
    .word  gP1LifePoints                  @ 080bed7c e0c40102
DAT_080bed80:
    .word  0x00000868                     @ 080bed80 68080000
DAT_080bed84:
    .word  0x02023130                     @ 080bed84 30310202
DAT_080bed88:
    .word  0x00000215                     @ 080bed88 15020000
DAT_080bed8c:
    .word  0x0000401a                     @ 080bed8c 1a400000
LAB_080bed90:
    ldrh r0,[r7,#0x12]                       @ 080bed90 788a
    adds r0,#0x1    @ 080bed92 0130
    strh r0,[r7,#0x12]                       @ 080bed94 7882
    lsls r0,r0,#0x10    @ 080bed96 0004
    lsrs r0,r0,#0x10    @ 080bed98 000c
    cmp r0,#0x1f                             @ 080bed9a 1f28
    bhi LAB_080beda0                         @ 080bed9c 00d8
    b LAB_080bec54                           @ 080bed9e 59e7
LAB_080beda0:
    ldrb r0,[r7,#0x10]                       @ 080beda0 387c
    adds r0,#0x1    @ 080beda2 0130
    strb r0,[r7,#0x10]                       @ 080beda4 3874
    b LAB_080bec54                           @ 080beda6 55e7
LAB_080beda8:
    ldr r1, DAT_080bedd8                     @ 080beda8 0b49
    movs r0,#0x2    @ 080bedaa 0220
    rsbs r0,r0,#0    @ 080bedac 4042
    ldrb r2,[r1,#0x0]                        @ 080bedae 0a78
    ands r0,r2    @ 080bedb0 1040
    strb r0,[r1,#0x0]                        @ 080bedb2 0870
    ldr r1, DAT_080beddc                     @ 080bedb4 0949
    ldr r4, DAT_080bede0                     @ 080bedb6 0a4c
    adds r1,r1,r4    @ 080bedb8 0919
    movs r0,#0x5    @ 080bedba 0520
    rsbs r0,r0,#0    @ 080bedbc 4042
    ldrb r2,[r1,#0x0]                        @ 080bedbe 0a78
    ands r0,r2    @ 080bedc0 1040
    strb r0,[r1,#0x0]                        @ 080bedc2 0870
    movs r0,#0x0    @ 080bedc4 0020
LAB_080bedc6:
    add sp,#0x1c                             @ 080bedc6 07b0
    pop {r3,r4,r5}                           @ 080bedc8 38bc
    .hword 0x4698    @ 080bedca 9846
    .hword 0x46a1    @ 080bedcc a146
    .hword 0x46aa    @ 080bedce aa46
    pop {r4,r5,r6,r7}                        @ 080bedd0 f0bc
    pop {r1}                                 @ 080bedd2 02bc
    bx r1                                    @ 080bedd4 0847
    .zero  0x2
DAT_080bedd8:
    .word  gBannerState                   @ 080bedd8 c0fe0102
DAT_080beddc:
    .word  0x02023130                     @ 080beddc 30310202
DAT_080bede0:
    .word  0x00000215                     @ 080bede0 15020000

@ pack card shop AOB animation state machine tick, called every frame. Reads phase byte [gBannerState+0x10] and dispatches on 0/1/other:
@ - phase>=2: clears [+0x0] bit1 flag; writes 0x02023130+0x215 bitmask; returns 0.
@ - phase=0: loads ROM palette+tiles to 0x050002a0/0x06014000; initializes AOB context (gBannerState+0x1c); calls sync_state_and_init_sprite; if r6==0xb syncs player LP delta and calls refresh_player_field_slot_tiles + update_zone_oam_card_count_tag; advances phase+1; returns 1.
@ - phase=1: switch dispatch on r6 (0..0xf) selects animation frame coords; calls transform_zone_oam_coords_by_player; render_aob_frame_to_oam; tick_aob_frame_counter; if frame counter reaches 0 advances phase+1; returns 1.
@ 
@ Constants:
@ - gBannerState = 0x0201fec0 (pack banner state struct)
@ - BG_PAL_DST = 0x050002a0, OBJ_TILE_DST = 0x06014000 (VRAM write targets)
@ - ZONE_TYPE_B = 0xb (zone type triggering LP sync)
@ - gP1LifePoints = 0x0201c4e0, PLAYER_STRIDE = 0x868 (LP struct)
tick_pack_banner_aob_phase:
    push {r4,r5,r6,r7,lr}                    @ 080bede4 f0b5
    .hword 0x4647    @ 080bede6 4746
    push {r7}                                @ 080bede8 80b4
    ldr r5, DAT_080bee1c                     @ 080bedea 0c4d
    ldr r7,[r5,#0x4]                         @ 080bedec 6f68
    ldrb r6,[r5,#0x8]                        @ 080bedee 2e7a
    ldrb r4,[r5,#0x9]                        @ 080bedf0 6c7a
    movs r0,#0x0    @ 080bedf2 0020
    .hword 0x4680    @ 080bedf4 8046
    ldrb r1,[r5,#0x10]                       @ 080bedf6 297c
    cmp r1,#0x0                              @ 080bedf8 0029
    beq LAB_080bee28                         @ 080bedfa 15d0
    cmp r1,#0x1                              @ 080bedfc 0129
    beq LAB_080beef4                         @ 080bedfe 79d0
    subs r0,#0x2    @ 080bee00 0238
    ldrb r1,[r5,#0x0]                        @ 080bee02 2978
    ands r0,r1    @ 080bee04 0840
    strb r0,[r5,#0x0]                        @ 080bee06 2870
    ldr r1, DAT_080bee20                     @ 080bee08 0549
    ldr r2, DAT_080bee24                     @ 080bee0a 064a
    adds r1,r1,r2    @ 080bee0c 8918
    movs r0,#0x5    @ 080bee0e 0520
    rsbs r0,r0,#0    @ 080bee10 4042
    ldrb r2,[r1,#0x0]                        @ 080bee12 0a78
    ands r0,r2    @ 080bee14 1040
    strb r0,[r1,#0x0]                        @ 080bee16 0870
    movs r0,#0x0    @ 080bee18 0020
    b LAB_080befac                           @ 080bee1a c7e0
DAT_080bee1c:
    .word  gBannerState                   @ 080bee1c c0fe0102
DAT_080bee20:
    .word  0x02023130                     @ 080bee20 30310202
DAT_080bee24:
    .word  0x00000215                     @ 080bee24 15020000
LAB_080bee28:
    cmp r6,#0x9                              @ 080bee28 092e
    bgt LAB_080bee44                         @ 080bee2a 0bdc
    movs r2,#0x1    @ 080bee2c 0122
    ands r2,r7    @ 080bee2e 3a40
    lsls r0,r6,#0x2    @ 080bee30 b000
    adds r0,r0,r6    @ 080bee32 8019
    lsls r0,r0,#0x2    @ 080bee34 8000
    ldr r1, DAT_080beecc                     @ 080bee36 2549
    muls r1,r2    @ 080bee38 5143
    adds r0,r0,r1    @ 080bee3a 4018
    ldr r1, DAT_080beed0                     @ 080bee3c 2449
    adds r0,r0,r1    @ 080bee3e 4018
    ldrh r0,[r0,#0x6]                        @ 080bee40 c088
    .hword 0x4680    @ 080bee42 8046
LAB_080bee44:
    ldr r0, DAT_080beed4                     @ 080bee44 2348
    ldr r1, DAT_080beed8                     @ 080bee46 2449
    movs r2,#0x20    @ 080bee48 2022
    bl copy_bytes_by_halfword                @ 080bee4a 36f02bf8
    ldr r0, DAT_080beedc                     @ 080bee4e 2348
    ldr r1, DAT_080beee0                     @ 080bee50 2349
    movs r2,#0x10    @ 080bee52 1022
    movs r3,#0xc    @ 080bee54 0c23
    bl tile_2d_row_copy                      @ 080bee56 38f03dfb
    adds r4,r5,#0x0    @ 080bee5a 2c1c
    adds r4,#0x1c    @ 080bee5c 1c34
    ldr r1, DAT_080beee4                     @ 080bee5e 2149
    ldr r2, DAT_080beee8                     @ 080bee60 214a
    adds r0,r4,#0x0    @ 080bee62 201c
    movs r3,#0x1    @ 080bee64 0123
    bl init_aob_ctx_from_ptnsect             @ 080bee66 38f09dff
    movs r0,#0x1    @ 080bee6a 0120
    ldrb r1,[r4,#0x13]                       @ 080bee6c e17c
    orrs r0,r1    @ 080bee6e 0843
    strb r0,[r4,#0x13]                       @ 080bee70 e074
    .hword 0x4641    @ 080bee72 4146
    adds r0,r4,#0x0    @ 080bee74 201c
    movs r2,#0x0    @ 080bee76 0022
    bl init_aob_ctx_with_anm_entry           @ 080bee78 38f0e6ff
    ldrb r0,[r5,#0x10]                       @ 080bee7c 287c
    adds r0,#0x1    @ 080bee7e 0130
    strb r0,[r5,#0x10]                       @ 080bee80 2874
    movs r0,#0x6    @ 080bee82 0620
    bl sync_state_and_init_sprite            @ 080bee84 3af016fe
    cmp r6,#0xb                              @ 080bee88 0b2e
    beq LAB_080bee8e                         @ 080bee8a 00d0
    b LAB_080befaa                           @ 080bee8c 8de0
LAB_080bee8e:
    ldr r2, PTR_gP1LifePoints_080beeec       @ 080bee8e 174a
    movs r0,#0x1    @ 080bee90 0120
    ands r0,r7    @ 080bee92 3840
    ldr r1, DAT_080beecc                     @ 080bee94 0d49
    muls r1,r0    @ 080bee96 4143
    adds r2,#0xc    @ 080bee98 0c32
    adds r1,r1,r2    @ 080bee9a 8918
    ldr r2, DAT_080beef0                     @ 080bee9c 144a
    lsls r3,r7,#0x1    @ 080bee9e 7b00
    adds r0,r2,#0x0    @ 080beea0 101c
    adds r0,#0x4c    @ 080beea2 4c30
    adds r5,r3,r0    @ 080beea4 1d18
    ldrh r4,[r5,#0x0]                        @ 080beea6 2c88
    ldr r1,[r1,#0x0]                         @ 080beea8 0968
    subs r0,r1,r4    @ 080beeaa 081b
    cmp r0,#0x7                              @ 080beeac 0728
    bhi LAB_080beeb8                         @ 080beeae 03d8
    cmp r1,#0x7                              @ 080beeb0 0729
    bls LAB_080beeb8                         @ 080beeb2 01d9
    subs r0,r4,#0x1    @ 080beeb4 601e
    strh r0,[r5,#0x0]                        @ 080beeb6 2880
LAB_080beeb8:
    adds r0,r2,#0x0    @ 080beeb8 101c
    adds r0,#0x4c    @ 080beeba 4c30
    adds r0,r3,r0    @ 080beebc 1818
    ldrh r1,[r0,#0x0]                        @ 080beebe 0188
    adds r0,r7,#0x0    @ 080beec0 381c
    bl refresh_player_field_slot_tiles       @ 080beec2 05f0adf9
    bl update_zone_oam_card_count_tag        @ 080beec6 07f061fc
    b LAB_080befaa                           @ 080beeca 6ee0
DAT_080beecc:
    .word  0x00000868                     @ 080beecc 68080000
DAT_080beed0:
    .word  0x0201c510                     @ 080beed0 10c50102
DAT_080beed4:
    .word  0x050002a0                     @ 080beed4 a0020005
DAT_080beed8:
    .word  0x098a2fd8                     @ 080beed8 d82f8a09
DAT_080beedc:
    .word  0x06014000                     @ 080beedc 00400106
DAT_080beee0:
    .word  0x098a17d8                     @ 080beee0 d8178a09
DAT_080beee4:
    .word  0x098a2ff8                     @ 080beee4 f82f8a09
DAT_080beee8:
    .word  0x02000005                     @ 080beee8 05000002
PTR_gP1LifePoints_080beeec:
    .word  gP1LifePoints                  @ 080beeec e0c40102
DAT_080beef0:
    .word  0x02023130                     @ 080beef0 30310202
LAB_080beef4:
    movs r5,#0x0    @ 080beef4 0025
    ldr r0, DAT_080bef14                     @ 080beef6 0748
    ldr r0,[r0,#0x4]                         @ 080beef8 4068
    eors r0,r1    @ 080beefa 4840
    cmp r7,r0                                @ 080beefc 8742
    bne LAB_080bef02                         @ 080beefe 00d1
    movs r5,#0x1    @ 080bef00 0125
LAB_080bef02:
    adds r3,r6,#0x0    @ 080bef02 331c
    adds r2,r4,#0x0    @ 080bef04 221c
    cmp r3,#0xf                              @ 080bef06 0f2b
    bhi switchD_080bef12__default            @ 080bef08 36d8
    lsls r0,r3,#0x2    @ 080bef0a 9800
    ldr r1, DAT_080bef18                     @ 080bef0c 0249
    adds r0,r0,r1    @ 080bef0e 4018
    ldr r0,[r0,#0x0]                         @ 080bef10 0068
switchD_080bef12__switchD:
    .hword 0x4687    @ 080bef12 8746
DAT_080bef14:
    .word  0x0201e2a0                     @ 080bef14 a0e20102
DAT_080bef18:
    .word  0x080bef1c                     @ 080bef18 1cef0b08
switchD_080bef12__switchdataD_080bef1c:
    .word  0x080bef5c                     @ 080bef1c 5cef0b08
    .word  0x080bef5c                     @ 080bef20 5cef0b08
    .word  0x080bef5c                     @ 080bef24 5cef0b08
    .word  0x080bef5c                     @ 080bef28 5cef0b08
    .word  0x080bef5c                     @ 080bef2c 5cef0b08
    .word  0x080bef62                     @ 080bef30 62ef0b08
    .word  0x080bef62                     @ 080bef34 62ef0b08
    .word  0x080bef62                     @ 080bef38 62ef0b08
    .word  0x080bef62                     @ 080bef3c 62ef0b08
    .word  0x080bef62                     @ 080bef40 62ef0b08
    .word  0x080bef68                     @ 080bef44 68ef0b08
    .word  0x080bef6c                     @ 080bef48 6cef0b08
    .word  0x080bef68                     @ 080bef4c 68ef0b08
    .word  0x080bef68                     @ 080bef50 68ef0b08
    .word  0x080bef68                     @ 080bef54 68ef0b08
    .word  0x080bef68                     @ 080bef58 68ef0b08
switchD_080bef12__caseD_0:
    movs r3,#0x0    @ 080bef5c 0023
    adds r2,r6,#0x0    @ 080bef5e 321c
    b switchD_080bef12__default              @ 080bef60 0ae0
switchD_080bef12__caseD_5:
    movs r3,#0x5    @ 080bef62 0523
    subs r2,r4,#0x5    @ 080bef64 621f
    b switchD_080bef12__default              @ 080bef66 07e0
switchD_080bef12__caseD_a:
    movs r2,#0x0    @ 080bef68 0022
    b switchD_080bef12__default              @ 080bef6a 05e0
switchD_080bef12__caseD_b:
    ldr r0, DAT_080befb8                     @ 080bef6c 1248
    lsls r1,r7,#0x1    @ 080bef6e 7900
    adds r0,#0x4c    @ 080bef70 4c30
    adds r1,r1,r0    @ 080bef72 0918
    ldrh r1,[r1,#0x0]                        @ 080bef74 0988
    subs r2,r4,r1    @ 080bef76 621a
switchD_080bef12__default:
    adds r0,r5,#0x0    @ 080bef78 281c
    adds r1,r3,#0x0    @ 080bef7a 191c
    bl transform_zone_oam_coords_by_player   @ 080bef7c 07f040fc
    ldr r4, DAT_080befbc                     @ 080bef80 0e4c
    lsls r1,r0,#0x10    @ 080bef82 0104
    lsrs r1,r1,#0x10    @ 080bef84 090c
    lsrs r0,r0,#0x10    @ 080bef86 000c
    lsls r0,r0,#0x10    @ 080bef88 0004
    orrs r1,r0    @ 080bef8a 0143
    adds r0,r4,#0x0    @ 080bef8c 201c
    movs r2,#0x0    @ 080bef8e 0022
    movs r3,#0x0    @ 080bef90 0023
    bl render_aob_frame_to_oam               @ 080bef92 39f035f8
    adds r0,r4,#0x0    @ 080bef96 201c
    bl tick_aob_frame_counter                @ 080bef98 38f0b6ff
    cmp r0,#0x0                              @ 080bef9c 0028
    bne LAB_080befaa                         @ 080bef9e 04d1
    adds r1,r4,#0x0    @ 080befa0 211c
    subs r1,#0x1c    @ 080befa2 1c39
    ldrb r0,[r1,#0x10]                       @ 080befa4 087c
    adds r0,#0x1    @ 080befa6 0130
    strb r0,[r1,#0x10]                       @ 080befa8 0874
LAB_080befaa:
    movs r0,#0x1    @ 080befaa 0120
LAB_080befac:
    pop {r3}                                 @ 080befac 08bc
    .hword 0x4698    @ 080befae 9846
    pop {r4,r5,r6,r7}                        @ 080befb0 f0bc
    pop {r1}                                 @ 080befb2 02bc
    bx r1                                    @ 080befb4 0847
    .zero  0x2
DAT_080befb8:
    .word  0x02023130                     @ 080befb8 30310202
DAT_080befbc:
    .word  0x0201fedc                     @ 080befbc dcfe0102

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x17 子状态机, 待详细分析.
play_ui_effect_17:
    push {r4,r5,r6,r7,lr}                    @ 080befc0 f0b5
    sub sp,#0x4                              @ 080befc2 81b0
    ldr r0, DAT_080befe4                     @ 080befc4 0748
    ldr r5,[r0,#0x4]                         @ 080befc6 4568
    ldrb r6,[r0,#0x8]                        @ 080befc8 067a
    ldrb r4,[r0,#0x9]                        @ 080befca 447a
    ldr r3,[r0,#0xc]                         @ 080befcc c368
    ldrb r1,[r0,#0x10]                       @ 080befce 017c
    adds r7,r0,#0x0    @ 080befd0 071c
    cmp r1,#0x1                              @ 080befd2 0129
    bne LAB_080befd8                         @ 080befd4 00d1
    b LAB_080bf130                           @ 080befd6 abe0
LAB_080befd8:
    cmp r1,#0x1                              @ 080befd8 0129
    bgt LAB_080befe8                         @ 080befda 05dc
    cmp r1,#0x0                              @ 080befdc 0029
    beq LAB_080beff0                         @ 080befde 07d0
    b LAB_080bf1fa                           @ 080befe0 0be1
    .zero  0x2
DAT_080befe4:
    .word  gBannerState                   @ 080befe4 c0fe0102
LAB_080befe8:
    cmp r1,#0x2                              @ 080befe8 0229
    bne LAB_080befee                         @ 080befea 00d1
    b LAB_080bf1ee                           @ 080befec ffe0
LAB_080befee:
    b LAB_080bf1fa                           @ 080befee 04e1
LAB_080beff0:
    cmp r3,#0x0                              @ 080beff0 002b
    bne LAB_080beff6                         @ 080beff2 00d1
    b LAB_080bf118                           @ 080beff4 90e0
LAB_080beff6:
    cmp r6,#0xf                              @ 080beff6 0f2e
    bls LAB_080beffc                         @ 080beff8 00d9
    b switchD_080bf004__default              @ 080beffa 78e0
LAB_080beffc:
    lsls r0,r6,#0x2    @ 080beffc b000
    ldr r1, DAT_080bf008                     @ 080beffe 0249
    adds r0,r0,r1    @ 080bf000 4018
    ldr r0,[r0,#0x0]                         @ 080bf002 0068
switchD_080bf004__switchD:
    .hword 0x4687    @ 080bf004 8746
    .zero  0x2
DAT_080bf008:
    .word  0x080bf00c                     @ 080bf008 0cf00b08
switchD_080bf004__switchdataD_080bf00c:
    .word  0x080bf04c                     @ 080bf00c 4cf00b08
    .word  0x080bf04c                     @ 080bf010 4cf00b08
    .word  0x080bf04c                     @ 080bf014 4cf00b08
    .word  0x080bf04c                     @ 080bf018 4cf00b08
    .word  0x080bf04c                     @ 080bf01c 4cf00b08
    .word  0x080bf04c                     @ 080bf020 4cf00b08
    .word  0x080bf04c                     @ 080bf024 4cf00b08
    .word  0x080bf04c                     @ 080bf028 4cf00b08
    .word  0x080bf04c                     @ 080bf02c 4cf00b08
    .word  0x080bf04c                     @ 080bf030 4cf00b08
    .word  0x080bf04c                     @ 080bf034 4cf00b08
    .word  0x080bf070                     @ 080bf038 70f00b08
    .word  0x080bf0d0                     @ 080bf03c d0f00b08
    .word  0x080bf088                     @ 080bf040 88f00b08
    .word  0x080bf0a0                     @ 080bf044 a0f00b08
    .word  0x080bf0b8                     @ 080bf048 b8f00b08
switchD_080bf004__caseD_0:
    movs r2,#0x1    @ 080bf04c 0122
    ands r2,r5    @ 080bf04e 2a40
    adds r1,r6,r4    @ 080bf050 3119
    lsls r0,r1,#0x2    @ 080bf052 8800
    adds r0,r0,r1    @ 080bf054 4018
    lsls r0,r0,#0x2    @ 080bf056 8000
    ldr r1, DAT_080bf068                     @ 080bf058 0349
    muls r1,r2    @ 080bf05a 5143
    adds r0,r0,r1    @ 080bf05c 4018
    ldr r1, DAT_080bf06c                     @ 080bf05e 0349
    adds r0,r0,r1    @ 080bf060 4018
    ldr r1,[r0,#0x0]                         @ 080bf062 0168
    b LAB_080bf0e2                           @ 080bf064 3de0
    .zero  0x2
DAT_080bf068:
    .word  0x00000868                     @ 080bf068 68080000
DAT_080bf06c:
    .word  0x0201c510                     @ 080bf06c 10c50102
switchD_080bf004__caseD_b:
    movs r0,#0x1    @ 080bf070 0120
    ands r0,r5    @ 080bf072 2840
    lsls r1,r4,#0x2    @ 080bf074 a100
    ldr r2, DAT_080bf080                     @ 080bf076 024a
    muls r0,r2    @ 080bf078 5043
    adds r1,r1,r0    @ 080bf07a 0918
    ldr r0, DAT_080bf084                     @ 080bf07c 0148
    b LAB_080bf0de                           @ 080bf07e 2ee0
DAT_080bf080:
    .word  0x00000868                     @ 080bf080 68080000
DAT_080bf084:
    .word  0x0201c600                     @ 080bf084 00c60102
switchD_080bf004__caseD_d:
    movs r0,#0x1    @ 080bf088 0120
    ands r0,r5    @ 080bf08a 2840
    lsls r1,r4,#0x2    @ 080bf08c a100
    ldr r2, DAT_080bf098                     @ 080bf08e 024a
    muls r0,r2    @ 080bf090 5043
    adds r1,r1,r0    @ 080bf092 0918
    ldr r0, DAT_080bf09c                     @ 080bf094 0148
    b LAB_080bf0de                           @ 080bf096 22e0
DAT_080bf098:
    .word  0x00000868                     @ 080bf098 68080000
DAT_080bf09c:
    .word  0x0201c740                     @ 080bf09c 40c70102
switchD_080bf004__caseD_e:
    movs r0,#0x1    @ 080bf0a0 0120
    ands r0,r5    @ 080bf0a2 2840
    lsls r1,r4,#0x2    @ 080bf0a4 a100
    ldr r2, DAT_080bf0b0                     @ 080bf0a6 024a
    muls r0,r2    @ 080bf0a8 5043
    adds r1,r1,r0    @ 080bf0aa 0918
    ldr r0, DAT_080bf0b4                     @ 080bf0ac 0148
    b LAB_080bf0de                           @ 080bf0ae 16e0
DAT_080bf0b0:
    .word  0x00000868                     @ 080bf0b0 68080000
DAT_080bf0b4:
    .word  0x0201c8f8                     @ 080bf0b4 f8c80102
switchD_080bf004__caseD_f:
    movs r0,#0x1    @ 080bf0b8 0120
    ands r0,r5    @ 080bf0ba 2840
    lsls r1,r4,#0x2    @ 080bf0bc a100
    ldr r2, DAT_080bf0c8                     @ 080bf0be 024a
    muls r0,r2    @ 080bf0c0 5043
    adds r1,r1,r0    @ 080bf0c2 0918
    ldr r0, DAT_080bf0cc                     @ 080bf0c4 0148
    b LAB_080bf0de                           @ 080bf0c6 0ae0
DAT_080bf0c8:
    .word  0x00000868                     @ 080bf0c8 68080000
DAT_080bf0cc:
    .word  0x0201cab0                     @ 080bf0cc b0ca0102
switchD_080bf004__caseD_c:
    movs r0,#0x1    @ 080bf0d0 0120
    ands r0,r5    @ 080bf0d2 2840
    lsls r1,r4,#0x2    @ 080bf0d4 a100
    ldr r2, DAT_080bf124                     @ 080bf0d6 134a
    muls r0,r2    @ 080bf0d8 5043
    adds r1,r1,r0    @ 080bf0da 0918
    ldr r0, DAT_080bf128                     @ 080bf0dc 1248
LAB_080bf0de:
    adds r1,r1,r0    @ 080bf0de 0918
    ldr r1,[r1,#0x0]                         @ 080bf0e0 0968
LAB_080bf0e2:
    lsls r0,r1,#0x2    @ 080bf0e2 8800
    lsrs r0,r0,#0x18    @ 080bf0e4 000e
    lsls r0,r0,#0x1    @ 080bf0e6 4000
    lsls r1,r1,#0x12    @ 080bf0e8 8904
    lsrs r1,r1,#0x1f    @ 080bf0ea c90f
    adds r2,r0,r1    @ 080bf0ec 4218
switchD_080bf004__default:
    movs r0,#0x1    @ 080bf0ee 0120
    ands r5,r0    @ 080bf0f0 0540
    movs r0,#0x1f    @ 080bf0f2 1f20
    ands r6,r0    @ 080bf0f4 0640
    lsls r0,r6,#0x1    @ 080bf0f6 7000
    orrs r5,r0    @ 080bf0f8 0543
    movs r0,#0xff    @ 080bf0fa ff20
    ands r0,r4    @ 080bf0fc 2040
    lsls r0,r0,#0x6    @ 080bf0fe 8001
    orrs r5,r0    @ 080bf100 0543
    movs r0,#0x80    @ 080bf102 8020
    lsls r0,r0,#0x7    @ 080bf104 c001
    orrs r5,r0    @ 080bf106 0543
    str r5,[sp,#0x0]                         @ 080bf108 0095
    adds r0,r2,#0x0    @ 080bf10a 101c
    bl ensure_card_id_cache_entry            @ 080bf10c 0df0dcfb
    .hword 0x4669    @ 080bf110 6946
    movs r2,#0x1    @ 080bf112 0122
    bl render_large_card_display_by_mode     @ 080bf114 0cf05af8
LAB_080bf118:
    ldr r1, DAT_080bf12c                     @ 080bf118 0449
    ldrb r0,[r1,#0x10]                       @ 080bf11a 087c
    adds r0,#0x1    @ 080bf11c 0130
    strb r0,[r1,#0x10]                       @ 080bf11e 0874
LAB_080bf120:
    movs r0,#0x1    @ 080bf120 0120
    b LAB_080bf216                           @ 080bf122 78e0
DAT_080bf124:
    .word  0x00000868                     @ 080bf124 68080000
DAT_080bf128:
    .word  0x0201c880                     @ 080bf128 80c80102
DAT_080bf12c:
    .word  gBannerState                   @ 080bf12c c0fe0102
LAB_080bf130:
    cmp r6,#0xf                              @ 080bf130 0f2e
    bhi switchD_080bf13c__default            @ 080bf132 45d8
    lsls r0,r6,#0x2    @ 080bf134 b000
    ldr r1, DAT_080bf140                     @ 080bf136 0249
    adds r0,r0,r1    @ 080bf138 4018
    ldr r0,[r0,#0x0]                         @ 080bf13a 0068
switchD_080bf13c__switchD:
    .hword 0x4687    @ 080bf13c 8746
    .zero  0x2
DAT_080bf140:
    .word  0x080bf144                     @ 080bf140 44f10b08
switchD_080bf13c__switchdataD_080bf144:
    .word  0x080bf184                     @ 080bf144 84f10b08
    .word  0x080bf184                     @ 080bf148 84f10b08
    .word  0x080bf184                     @ 080bf14c 84f10b08
    .word  0x080bf184                     @ 080bf150 84f10b08
    .word  0x080bf184                     @ 080bf154 84f10b08
    .word  0x080bf18a                     @ 080bf158 8af10b08
    .word  0x080bf18a                     @ 080bf15c 8af10b08
    .word  0x080bf18a                     @ 080bf160 8af10b08
    .word  0x080bf18a                     @ 080bf164 8af10b08
    .word  0x080bf18a                     @ 080bf168 8af10b08
    .word  0x080bf1be                     @ 080bf16c bef10b08
    .word  0x080bf190                     @ 080bf170 90f10b08
    .word  0x080bf1be                     @ 080bf174 bef10b08
    .word  0x080bf1be                     @ 080bf178 bef10b08
    .word  0x080bf1be                     @ 080bf17c bef10b08
    .word  0x080bf1be                     @ 080bf180 bef10b08
switchD_080bf13c__caseD_0:
    adds r4,r6,#0x0    @ 080bf184 341c
    movs r6,#0x0    @ 080bf186 0026
    b switchD_080bf13c__default              @ 080bf188 1ae0
switchD_080bf13c__caseD_5:
    subs r4,r6,#0x5    @ 080bf18a 741f
    movs r6,#0x5    @ 080bf18c 0526
    b switchD_080bf13c__default              @ 080bf18e 17e0
switchD_080bf13c__caseD_b:
    movs r6,#0xb    @ 080bf190 0b26
    ldr r0, DAT_080bf1b0                     @ 080bf192 0748
    lsls r1,r5,#0x1    @ 080bf194 6900
    adds r0,#0x4c    @ 080bf196 4c30
    adds r1,r1,r0    @ 080bf198 0918
    ldrh r2,[r1,#0x0]                        @ 080bf19a 0a88
    cmp r2,r4                                @ 080bf19c a242
    bgt LAB_080bf1b4                         @ 080bf19e 09dc
    adds r0,r2,#0x7    @ 080bf1a0 d01d
    subs r3,r4,r2    @ 080bf1a2 a31a
    cmp r0,r4                                @ 080bf1a4 a042
    bgt LAB_080bf1ba                         @ 080bf1a6 08dc
    movs r3,#0x6    @ 080bf1a8 0623
    subs r0,r4,#0x6    @ 080bf1aa a01f
    b LAB_080bf1b8                           @ 080bf1ac 04e0
    .zero  0x2
DAT_080bf1b0:
    .word  0x02023130                     @ 080bf1b0 30310202
LAB_080bf1b4:
    movs r3,#0x0    @ 080bf1b4 0023
    subs r0,r2,r4    @ 080bf1b6 101b
LAB_080bf1b8:
    strh r0,[r1,#0x0]                        @ 080bf1b8 0880
LAB_080bf1ba:
    adds r4,r3,#0x0    @ 080bf1ba 1c1c
    b switchD_080bf13c__default              @ 080bf1bc 00e0
switchD_080bf13c__caseD_a:
    movs r4,#0x0    @ 080bf1be 0024
switchD_080bf13c__default:
    ldrh r0,[r7,#0x12]                       @ 080bf1c0 788a
    movs r1,#0x3    @ 080bf1c2 0321
    bl __umodsi3                             @ 080bf1c4 4ff046fb
    adds r3,r0,#0x0    @ 080bf1c8 031c
    lsls r3,r3,#0x10    @ 080bf1ca 1b04
    lsrs r3,r3,#0x10    @ 080bf1cc 1b0c
    adds r0,r5,#0x0    @ 080bf1ce 281c
    adds r1,r6,#0x0    @ 080bf1d0 311c
    adds r2,r4,#0x0    @ 080bf1d2 221c
    bl set_zone_oam_coords_by_player         @ 080bf1d4 07f0e2fb
    ldrh r0,[r7,#0x12]                       @ 080bf1d8 788a
    adds r0,#0x1    @ 080bf1da 0130
    strh r0,[r7,#0x12]                       @ 080bf1dc 7882
    lsls r0,r0,#0x10    @ 080bf1de 0004
    lsrs r0,r0,#0x10    @ 080bf1e0 000c
    cmp r0,#0x1f                             @ 080bf1e2 1f28
    bls LAB_080bf120                         @ 080bf1e4 9cd9
    ldrb r0,[r7,#0x10]                       @ 080bf1e6 387c
    adds r0,#0x1    @ 080bf1e8 0130
    strb r0,[r7,#0x10]                       @ 080bf1ea 3874
    b LAB_080bf120                           @ 080bf1ec 98e7
LAB_080bf1ee:
    bl refresh_duel_field_zone_info          @ 080bf1ee 0cf08dfe
    ldrb r0,[r7,#0x10]                       @ 080bf1f2 387c
    adds r0,#0x1    @ 080bf1f4 0130
    strb r0,[r7,#0x10]                       @ 080bf1f6 3874
    b LAB_080bf120                           @ 080bf1f8 92e7
LAB_080bf1fa:
    movs r0,#0x2    @ 080bf1fa 0220
    rsbs r0,r0,#0    @ 080bf1fc 4042
    ldrb r1,[r7,#0x0]                        @ 080bf1fe 3978
    ands r0,r1    @ 080bf200 0840
    strb r0,[r7,#0x0]                        @ 080bf202 3870
    ldr r1, DAT_080bf220                     @ 080bf204 0649
    ldr r2, DAT_080bf224                     @ 080bf206 074a
    adds r1,r1,r2    @ 080bf208 8918
    movs r0,#0x5    @ 080bf20a 0520
    rsbs r0,r0,#0    @ 080bf20c 4042
    ldrb r2,[r1,#0x0]                        @ 080bf20e 0a78
    ands r0,r2    @ 080bf210 1040
    strb r0,[r1,#0x0]                        @ 080bf212 0870
    movs r0,#0x0    @ 080bf214 0020
LAB_080bf216:
    add sp,#0x4                              @ 080bf216 01b0
    pop {r4,r5,r6,r7}                        @ 080bf218 f0bc
    pop {r1}                                 @ 080bf21a 02bc
    bx r1                                    @ 080bf21c 0847
    .zero  0x2
DAT_080bf220:
    .word  0x02023130                     @ 080bf220 30310202
DAT_080bf224:
    .word  0x00000215                     @ 080bf224 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x11 子状态机, 待详细分析.
play_ui_effect_11:
    push {r4,r5,r6,r7,lr}                    @ 080bf228 f0b5
    ldr r2, DAT_080bf250                     @ 080bf22a 094a
    ldr r6,[r2,#0x4]                         @ 080bf22c 5668
    ldr r4,[r2,#0x8]                         @ 080bf22e 9468
    ldr r3, DAT_080bf254                     @ 080bf230 084b
    lsls r0,r6,#0x1    @ 080bf232 7000
    adds r1,r3,#0x0    @ 080bf234 191c
    adds r1,#0x4c    @ 080bf236 4c31
    adds r0,r0,r1    @ 080bf238 4018
    ldrh r1,[r0,#0x0]                        @ 080bf23a 0188
    adds r5,r2,#0x0    @ 080bf23c 151c
    cmp r1,r4                                @ 080bf23e a142
    bgt LAB_080bf258                         @ 080bf240 0adc
    adds r0,r1,#0x7    @ 080bf242 c81d
    movs r7,#0x6    @ 080bf244 0627
    cmp r0,r4                                @ 080bf246 a042
    ble LAB_080bf25a                         @ 080bf248 07dd
    subs r7,r4,r1    @ 080bf24a 671a
    b LAB_080bf25a                           @ 080bf24c 05e0
    .zero  0x2
DAT_080bf250:
    .word  gBannerState                   @ 080bf250 c0fe0102
DAT_080bf254:
    .word  0x02023130                     @ 080bf254 30310202
LAB_080bf258:
    movs r7,#0x0    @ 080bf258 0027
LAB_080bf25a:
    ldrb r0,[r5,#0x10]                       @ 080bf25a 287c
    cmp r0,#0x0                              @ 080bf25c 0028
    beq LAB_080bf284                         @ 080bf25e 11d0
    cmp r0,#0x1                              @ 080bf260 0128
    beq LAB_080bf294                         @ 080bf262 17d0
    movs r0,#0x2    @ 080bf264 0220
    rsbs r0,r0,#0    @ 080bf266 4042
    ldrb r1,[r5,#0x0]                        @ 080bf268 2978
    ands r0,r1    @ 080bf26a 0840
    strb r0,[r5,#0x0]                        @ 080bf26c 2870
    ldr r2, DAT_080bf280                     @ 080bf26e 044a
    adds r1,r3,r2    @ 080bf270 9918
    movs r0,#0x5    @ 080bf272 0520
    rsbs r0,r0,#0    @ 080bf274 4042
    ldrb r2,[r1,#0x0]                        @ 080bf276 0a78
    ands r0,r2    @ 080bf278 1040
    strb r0,[r1,#0x0]                        @ 080bf27a 0870
    movs r0,#0x0    @ 080bf27c 0020
    b LAB_080bf2c4                           @ 080bf27e 21e0
DAT_080bf280:
    .word  0x00000215                     @ 080bf280 15020000
LAB_080bf284:
    adds r0,r6,#0x0    @ 080bf284 301c
    movs r1,#0xb    @ 080bf286 0b21
    adds r2,r4,#0x0    @ 080bf288 221c
    bl render_duel_field_zone_info           @ 080bf28a 0cf085fb
    ldrb r0,[r5,#0x10]                       @ 080bf28e 287c
    adds r0,#0x1    @ 080bf290 0130
    strb r0,[r5,#0x10]                       @ 080bf292 2874
LAB_080bf294:
    ldr r4, DAT_080bf2cc                     @ 080bf294 0d4c
    ldrh r0,[r4,#0x12]                       @ 080bf296 608a
    movs r1,#0x3    @ 080bf298 0321
    bl __umodsi3                             @ 080bf29a 4ff0dbfa
    adds r3,r0,#0x0    @ 080bf29e 031c
    lsls r3,r3,#0x10    @ 080bf2a0 1b04
    lsrs r3,r3,#0x10    @ 080bf2a2 1b0c
    adds r0,r6,#0x0    @ 080bf2a4 301c
    movs r1,#0xb    @ 080bf2a6 0b21
    adds r2,r7,#0x0    @ 080bf2a8 3a1c
    bl set_zone_oam_coords_by_player         @ 080bf2aa 07f077fb
    ldrh r0,[r4,#0x12]                       @ 080bf2ae 608a
    adds r0,#0x1    @ 080bf2b0 0130
    strh r0,[r4,#0x12]                       @ 080bf2b2 6082
    lsls r0,r0,#0x10    @ 080bf2b4 0004
    lsrs r0,r0,#0x10    @ 080bf2b6 000c
    cmp r0,#0x3f                             @ 080bf2b8 3f28
    bls LAB_080bf2c2                         @ 080bf2ba 02d9
    ldrb r0,[r4,#0x10]                       @ 080bf2bc 207c
    adds r0,#0x1    @ 080bf2be 0130
    strb r0,[r4,#0x10]                       @ 080bf2c0 2074
LAB_080bf2c2:
    movs r0,#0x1    @ 080bf2c2 0120
LAB_080bf2c4:
    pop {r4,r5,r6,r7}                        @ 080bf2c4 f0bc
    pop {r1}                                 @ 080bf2c6 02bc
    bx r1                                    @ 080bf2c8 0847
    .zero  0x2
DAT_080bf2cc:
    .word  gBannerState                   @ 080bf2cc c0fe0102

@ 将十进制数值分解为各位数字并写入 OAM 影子缓冲区 (用于 LP/数值显示). r1 = number (待渲染的十进制整数, [0..8000] LP 值); r2 = player_flag {0,1} (保存到 r8). Y 位置: gBannerState[+0x14] * 8 + 0x70 = 屏幕 Y 坐标. X 起始: 基于 gBannerState[+0x14] * 8 + 0x70 区间 (r6), 每位数字向左偏移 0xc 像素. digit tile = 0x204 + digit * 2 (tile 基址 0x81*4=0x204 起, 每个数字占 2 tile). flag 字段: 读 DAT_0x0201e2a0[+0x4] bit0 XOR 1 -> 若非零则 r1 |= 0x80 (palette 或 flip bit). 循环: r5 % 10 = 当前最低位数字 -> 写入 OAM; r5 /= 10; 重复直到 r5 == 0. 最后再写一次末位确保 0 不被跳过. 调用 write_oam_entry_from_packed_args (已命名) 写入 OAM. 唯一 caller: play_ui_effect_0e (0x080bf394, vram/scene_duel_field/duel_field). Constants: gBannerState (0x0201fec0)[+0x14]: Y/X 位置参数 byte; DAT_080bf368 = gBannerState; DAT_080bf36c = 0x0201e2a0 (struct); 0x204 = 0x81*4: digit tile 基址; 0xc: 每个数字 X 间距; 0x70: Y 基准偏移; 0x80: palette/flip flag bit; 0xa: 十进制 mod/div 基数; 0x202: 某 OAM attr 常量 (DAT_080bf390).
draw_number_digits_to_oam:
    push {r4,r5,r6,r7,lr}                    @ 080bf2d0 f0b5
    .hword 0x4657    @ 080bf2d2 5746
    .hword 0x464e    @ 080bf2d4 4e46
    .hword 0x4645    @ 080bf2d6 4546
    push {r5,r6,r7}                          @ 080bf2d8 e0b4
    adds r5,r1,#0x0    @ 080bf2da 0d1c
    .hword 0x4690    @ 080bf2dc 9046
    ldr r1, DAT_080bf368                     @ 080bf2de 2249
    ldrb r1,[r1,#0x14]                       @ 080bf2e0 097d
    lsls r1,r1,#0x3    @ 080bf2e2 c900
    adds r6,r1,#0x0    @ 080bf2e4 0e1c
    adds r6,#0x70    @ 080bf2e6 7036
    ldr r1, DAT_080bf36c                     @ 080bf2e8 2049
    ldr r1,[r1,#0x4]                         @ 080bf2ea 4968
    movs r2,#0x1    @ 080bf2ec 0122
    eors r1,r2    @ 080bf2ee 5140
    eors r0,r1    @ 080bf2f0 4840
    rsbs r1,r0,#0    @ 080bf2f2 4142
    orrs r1,r0    @ 080bf2f4 0143
    asrs r1,r1,#0x1f    @ 080bf2f6 c917
    movs r0,#0x80    @ 080bf2f8 8020
    ands r1,r0    @ 080bf2fa 0140
    adds r0,r5,#0x0    @ 080bf2fc 281c
    cmp r5,#0x0                              @ 080bf2fe 002d
    beq LAB_080bf304                         @ 080bf300 00d0
    movs r0,#0x1    @ 080bf302 0120
LAB_080bf304:
    .hword 0x4682    @ 080bf304 8246
    lsls r7,r1,#0x10    @ 080bf306 0f04
    movs r0,#0x2    @ 080bf308 0220
    .hword 0x4641    @ 080bf30a 4146
    subs r0,r0,r1    @ 080bf30c 401a
    lsls r0,r0,#0xc    @ 080bf30e 0003
    .hword 0x4681    @ 080bf310 8146
LAB_080bf312:
    adds r4,r6,#0x0    @ 080bf312 341c
    orrs r4,r7    @ 080bf314 3c43
    adds r0,r5,#0x0    @ 080bf316 281c
    movs r1,#0xa    @ 080bf318 0a21
    bl __modsi3                              @ 080bf31a 4ff0bff9
    adds r2,r0,#0x0    @ 080bf31e 021c
    lsls r2,r2,#0x1    @ 080bf320 5200
    movs r0,#0x81    @ 080bf322 8120
    lsls r0,r0,#0x2    @ 080bf324 8000
    adds r2,r2,r0    @ 080bf326 1218
    .hword 0x4649    @ 080bf328 4946
    orrs r2,r1    @ 080bf32a 0a43
    lsls r2,r2,#0x10    @ 080bf32c 1204
    lsrs r2,r2,#0x10    @ 080bf32e 120c
    adds r0,r4,#0x0    @ 080bf330 201c
    movs r1,#0x40    @ 080bf332 4021
    bl write_oam_entry_from_packed_args      @ 080bf334 36f01aff
    subs r6,#0xc    @ 080bf338 0c3e
    adds r0,r5,#0x0    @ 080bf33a 281c
    movs r1,#0xa    @ 080bf33c 0a21
    bl __divsi3                              @ 080bf33e 4ff061f9
    adds r5,r0,#0x0    @ 080bf342 051c
    cmp r5,#0x0                              @ 080bf344 002d
    bgt LAB_080bf312                         @ 080bf346 e4dc
    .hword 0x4652    @ 080bf348 5246
    cmp r2,#0x0                              @ 080bf34a 002a
    beq LAB_080bf380                         @ 080bf34c 18d0
    adds r1,r6,#0x0    @ 080bf34e 311c
    orrs r1,r7    @ 080bf350 3943
    movs r0,#0x2    @ 080bf352 0220
    .hword 0x4642    @ 080bf354 4246
    subs r0,r0,r2    @ 080bf356 801a
    lsls r2,r0,#0xc    @ 080bf358 0203
    .hword 0x4640    @ 080bf35a 4046
    cmp r0,#0x0                              @ 080bf35c 0028
    beq LAB_080bf370                         @ 080bf35e 07d0
    movs r0,#0x80    @ 080bf360 8020
    lsls r0,r0,#0x2    @ 080bf362 8000
    b LAB_080bf372                           @ 080bf364 05e0
    .zero  0x2
DAT_080bf368:
    .word  gBannerState                   @ 080bf368 c0fe0102
DAT_080bf36c:
    .word  0x0201e2a0                     @ 080bf36c a0e20102
LAB_080bf370:
    ldr r0, DAT_080bf390                     @ 080bf370 0748
LAB_080bf372:
    orrs r2,r0    @ 080bf372 0243
    lsls r0,r2,#0x10    @ 080bf374 1004
    lsrs r2,r0,#0x10    @ 080bf376 020c
    adds r0,r1,#0x0    @ 080bf378 081c
    movs r1,#0x40    @ 080bf37a 4021
    bl write_oam_entry_from_packed_args      @ 080bf37c 36f0f6fe
LAB_080bf380:
    pop {r3,r4,r5}                           @ 080bf380 38bc
    .hword 0x4698    @ 080bf382 9846
    .hword 0x46a1    @ 080bf384 a146
    .hword 0x46aa    @ 080bf386 aa46
    pop {r4,r5,r6,r7}                        @ 080bf388 f0bc
    pop {r0}                                 @ 080bf38a 01bc
    bx r0                                    @ 080bf38c 0047
    .zero  0x2
DAT_080bf390:
    .word  0x00000202                     @ 080bf390 02020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x0e 子状态机, 待详细分析.
play_ui_effect_0e:
    push {r4,r5,r6,r7,lr}                    @ 080bf394 f0b5
    .hword 0x464f    @ 080bf396 4f46
    .hword 0x4646    @ 080bf398 4646
    push {r6,r7}                             @ 080bf39a c0b4
    sub sp,#0x4                              @ 080bf39c 81b0
    ldr r0, DAT_080bf3dc                     @ 080bf39e 0f48
    ldr r7,[r0,#0x4]                         @ 080bf3a0 4768
    ldr r6,[r0,#0x8]                         @ 080bf3a2 8668
    adds r4,r0,#0x0    @ 080bf3a4 041c
    cmp r6,#0x0                              @ 080bf3a6 002e
    bge LAB_080bf3ac                         @ 080bf3a8 00da
    rsbs r6,r6,#0    @ 080bf3aa 7642
LAB_080bf3ac:
    ldrb r0,[r4,#0xc]                        @ 080bf3ac 207b
    movs r5,#0x0    @ 080bf3ae 0025
    movs r3,#0x0    @ 080bf3b0 0023
    .hword 0x4698    @ 080bf3b2 9846
    ldrb r1,[r4,#0xd]                        @ 080bf3b4 617b
    cmp r1,#0x4                              @ 080bf3b6 0429
    bne LAB_080bf3be                         @ 080bf3b8 01d1
    movs r2,#0x1    @ 080bf3ba 0122
    .hword 0x4690    @ 080bf3bc 9046
LAB_080bf3be:
    cmp r6,#0x0                              @ 080bf3be 002e
    bne LAB_080bf3c4                         @ 080bf3c0 00d1
    b LAB_080bf56e                           @ 080bf3c2 d4e0
LAB_080bf3c4:
    cmp r0,#0x0                              @ 080bf3c4 0028
    beq LAB_080bf3ca                         @ 080bf3c6 00d0
    b LAB_080bf56e                           @ 080bf3c8 d1e0
LAB_080bf3ca:
    ldrb r0,[r4,#0x10]                       @ 080bf3ca 207c
    cmp r0,#0x1                              @ 080bf3cc 0128
    beq LAB_080bf434                         @ 080bf3ce 31d0
    cmp r0,#0x1                              @ 080bf3d0 0128
    bgt LAB_080bf3e0                         @ 080bf3d2 05dc
    cmp r0,#0x0                              @ 080bf3d4 0028
    beq LAB_080bf3ec                         @ 080bf3d6 09d0
    b LAB_080bf56e                           @ 080bf3d8 c9e0
    .zero  0x2
DAT_080bf3dc:
    .word  gBannerState                   @ 080bf3dc c0fe0102
LAB_080bf3e0:
    cmp r0,#0x2                              @ 080bf3e0 0228
    beq LAB_080bf45a                         @ 080bf3e2 3ad0
    cmp r0,#0x3                              @ 080bf3e4 0328
    bne LAB_080bf3ea                         @ 080bf3e6 00d1
    b LAB_080bf54c                           @ 080bf3e8 b0e0
LAB_080bf3ea:
    b LAB_080bf56e                           @ 080bf3ea c0e0
LAB_080bf3ec:
    ldr r0, DAT_080bf428                     @ 080bf3ec 0e48
    ldr r1, DAT_080bf42c                     @ 080bf3ee 0f49
    movs r2,#0x18    @ 080bf3f0 1822
    movs r3,#0x2    @ 080bf3f2 0223
    bl tile_2d_row_copy                      @ 080bf3f4 38f06ef8
    adds r4,r6,#0x0    @ 080bf3f8 341c
LAB_080bf3fa:
    adds r0,r4,#0x0    @ 080bf3fa 201c
    movs r1,#0xa    @ 080bf3fc 0a21
    bl __udivsi3                             @ 080bf3fe 4ff0edf9
    adds r4,r0,#0x0    @ 080bf402 041c
    adds r5,#0x1    @ 080bf404 0135
    cmp r4,#0x0                              @ 080bf406 002c
    bne LAB_080bf3fa                         @ 080bf408 f7d1
    ldr r4, DAT_080bf430                     @ 080bf40a 094c
    adds r0,r5,#0x1    @ 080bf40c 681c
    strb r0,[r4,#0x14]                       @ 080bf40e 2075
    adds r0,r7,#0x0    @ 080bf410 381c
    adds r1,r6,#0x0    @ 080bf412 311c
    .hword 0x4642    @ 080bf414 4246
    bl draw_number_digits_to_oam             @ 080bf416 fff75bff
    ldrb r0,[r4,#0x10]                       @ 080bf41a 207c
    adds r0,#0x1    @ 080bf41c 0130
    strb r0,[r4,#0x10]                       @ 080bf41e 2074
    movs r0,#0x20    @ 080bf420 2020
    strb r0,[r4,#0x11]                       @ 080bf422 6074
LAB_080bf424:
    movs r0,#0x1    @ 080bf424 0120
    b LAB_080bf58a                           @ 080bf426 b0e0
DAT_080bf428:
    .word  0x06014000                     @ 080bf428 00400106
DAT_080bf42c:
    .word  0x09851ffc                     @ 080bf42c fc1f8509
DAT_080bf430:
    .word  gBannerState                   @ 080bf430 c0fe0102
LAB_080bf434:
    adds r0,r7,#0x0    @ 080bf434 381c
    adds r1,r6,#0x0    @ 080bf436 311c
    .hword 0x4642    @ 080bf438 4246
    str r3,[sp,#0x0]                         @ 080bf43a 0093
    bl draw_number_digits_to_oam             @ 080bf43c fff748ff
    ldrh r0,[r4,#0x12]                       @ 080bf440 608a
    adds r0,#0x1    @ 080bf442 0130
    strh r0,[r4,#0x12]                       @ 080bf444 6082
    lsls r0,r0,#0x10    @ 080bf446 0004
    lsrs r0,r0,#0x10    @ 080bf448 000c
    ldr r3,[sp,#0x0]                         @ 080bf44a 009b
    cmp r0,#0x2                              @ 080bf44c 0228
    bls LAB_080bf424                         @ 080bf44e e9d9
    strh r3,[r4,#0x12]                       @ 080bf450 6382
    ldrb r0,[r4,#0x10]                       @ 080bf452 207c
    adds r0,#0x1    @ 080bf454 0130
    strb r0,[r4,#0x10]                       @ 080bf456 2074
    b LAB_080bf424                           @ 080bf458 e4e7
LAB_080bf45a:
    .hword 0x4640    @ 080bf45a 4046
    cmp r0,#0x0                              @ 080bf45c 0028
    beq LAB_080bf468                         @ 080bf45e 03d0
    movs r0,#0x26    @ 080bf460 2620
    bl sync_state_and_init_sprite            @ 080bf462 3af027fb
    b LAB_080bf46e                           @ 080bf466 02e0
LAB_080bf468:
    movs r0,#0x25    @ 080bf468 2520
    bl sync_state_and_init_sprite            @ 080bf46a 3af023fb
LAB_080bf46e:
    movs r3,#0x1    @ 080bf46e 0123
    ldr r1, DAT_080bf49c                     @ 080bf470 0a49
    ldrb r0,[r1,#0x11]                       @ 080bf472 487c
    cmp r0,#0x0                              @ 080bf474 0028
    beq LAB_080bf47c                         @ 080bf476 01d0
    subs r0,#0x1    @ 080bf478 0138
    strb r0,[r1,#0x11]                       @ 080bf47a 4874
LAB_080bf47c:
    ldr r5,[r1,#0x18]                        @ 080bf47c 8d69
    ldr r2, PTR_gP1LifePoints_080bf4a0       @ 080bf47e 084a
    adds r0,r7,#0x0    @ 080bf480 381c
    ands r0,r3    @ 080bf482 1840
    ldr r1, DAT_080bf4a4                     @ 080bf484 0749
    muls r0,r1    @ 080bf486 4843
    adds r0,r0,r2    @ 080bf488 8018
    ldr r0,[r0,#0x0]                         @ 080bf48a 0068
    .hword 0x4691    @ 080bf48c 9146
    cmp r6,r0                                @ 080bf48e 8642
    ble LAB_080bf498                         @ 080bf490 02dd
    .hword 0x4641    @ 080bf492 4146
    cmp r1,#0x0                              @ 080bf494 0029
    beq LAB_080bf4a8                         @ 080bf496 07d0
LAB_080bf498:
    subs r4,r6,r5    @ 080bf498 741b
    b LAB_080bf4aa                           @ 080bf49a 06e0
DAT_080bf49c:
    .word  gBannerState                   @ 080bf49c c0fe0102
PTR_gP1LifePoints_080bf4a0:
    .word  gP1LifePoints                  @ 080bf4a0 e0c40102
DAT_080bf4a4:
    .word  0x00000868                     @ 080bf4a4 68080000
LAB_080bf4a8:
    subs r4,r0,r5    @ 080bf4a8 441b
LAB_080bf4aa:
    cmp r5,r6                                @ 080bf4aa b542
    bls LAB_080bf4b0                         @ 080bf4ac 00d9
    movs r4,#0x0    @ 080bf4ae 0024
LAB_080bf4b0:
    cmp r3,#0x0                              @ 080bf4b0 002b
    beq LAB_080bf524                         @ 080bf4b2 37d0
    movs r1,#0x1    @ 080bf4b4 0121
    cmp r1,r4                                @ 080bf4b6 a142
    bcs LAB_080bf4c4                         @ 080bf4b8 04d2
LAB_080bf4ba:
    lsls r0,r1,#0x2    @ 080bf4ba 8800
    adds r0,r0,r1    @ 080bf4bc 4018
    lsls r1,r0,#0x1    @ 080bf4be 4100
    cmp r1,r4                                @ 080bf4c0 a142
    bcc LAB_080bf4ba                         @ 080bf4c2 fad3
LAB_080bf4c4:
    adds r0,r1,#0x0    @ 080bf4c4 081c
    movs r1,#0xa    @ 080bf4c6 0a21
    bl __udivsi3                             @ 080bf4c8 4ff088f9
    adds r1,r0,#0x0    @ 080bf4cc 011c
    cmp r1,#0x9                              @ 080bf4ce 0929
    bhi LAB_080bf4d4                         @ 080bf4d0 00d8
    movs r1,#0xa    @ 080bf4d2 0a21
LAB_080bf4d4:
    adds r5,r5,r1    @ 080bf4d4 6d18
    cmp r5,r6                                @ 080bf4d6 b542
    bls LAB_080bf4dc                         @ 080bf4d8 00d9
    adds r5,r6,#0x0    @ 080bf4da 351c
LAB_080bf4dc:
    .hword 0x4642    @ 080bf4dc 4246
    cmp r2,#0x0                              @ 080bf4de 002a
    beq LAB_080bf4fc                         @ 080bf4e0 0cd0
    movs r0,#0x1    @ 080bf4e2 0120
    ands r0,r7    @ 080bf4e4 3840
    ldr r1, DAT_080bf4f8                     @ 080bf4e6 0449
    muls r0,r1    @ 080bf4e8 4843
    add r0,r9                                @ 080bf4ea 4844
    ldr r1,[r0,#0x0]                         @ 080bf4ec 0168
    adds r1,r1,r5    @ 080bf4ee 4919
    adds r0,r7,#0x0    @ 080bf4f0 381c
    bl write_lp_digit_tiles_to_vram          @ 080bf4f2 0bf081f8
    b LAB_080bf524                           @ 080bf4f6 15e0
DAT_080bf4f8:
    .word  0x00000868                     @ 080bf4f8 68080000
LAB_080bf4fc:
    movs r0,#0x1    @ 080bf4fc 0120
    ands r0,r7    @ 080bf4fe 3840
    ldr r1, DAT_080bf518                     @ 080bf500 0549
    muls r0,r1    @ 080bf502 4843
    add r0,r9                                @ 080bf504 4844
    ldr r0,[r0,#0x0]                         @ 080bf506 0068
    cmp r0,r5                                @ 080bf508 a842
    bcs LAB_080bf51c                         @ 080bf50a 07d2
    adds r0,r7,#0x0    @ 080bf50c 381c
    movs r1,#0x0    @ 080bf50e 0021
    bl write_lp_digit_tiles_to_vram          @ 080bf510 0bf072f8
    adds r5,r6,#0x0    @ 080bf514 351c
    b LAB_080bf524                           @ 080bf516 05e0
DAT_080bf518:
    .word  0x00000868                     @ 080bf518 68080000
LAB_080bf51c:
    subs r1,r0,r5    @ 080bf51c 411b
    adds r0,r7,#0x0    @ 080bf51e 381c
    bl write_lp_digit_tiles_to_vram          @ 080bf520 0bf06af8
LAB_080bf524:
    subs r4,r6,r5    @ 080bf524 741b
    cmp r5,r6                                @ 080bf526 b542
    bls LAB_080bf52c                         @ 080bf528 00d9
    movs r4,#0x0    @ 080bf52a 0024
LAB_080bf52c:
    adds r0,r7,#0x0    @ 080bf52c 381c
    adds r1,r6,#0x0    @ 080bf52e 311c
    .hword 0x4642    @ 080bf530 4246
    bl draw_number_digits_to_oam             @ 080bf532 fff7cdfe
    ldr r1, DAT_080bf548                     @ 080bf536 0449
    str r5,[r1,#0x18]                        @ 080bf538 8d61
    cmp r4,#0x0                              @ 080bf53a 002c
    beq LAB_080bf540                         @ 080bf53c 00d0
    b LAB_080bf424                           @ 080bf53e 71e7
LAB_080bf540:
    ldrb r0,[r1,#0x10]                       @ 080bf540 087c
    adds r0,#0x1    @ 080bf542 0130
    strb r0,[r1,#0x10]                       @ 080bf544 0874
    b LAB_080bf424                           @ 080bf546 6de7
DAT_080bf548:
    .word  gBannerState                   @ 080bf548 c0fe0102
LAB_080bf54c:
    adds r0,r7,#0x0    @ 080bf54c 381c
    adds r1,r6,#0x0    @ 080bf54e 311c
    .hword 0x4642    @ 080bf550 4246
    bl draw_number_digits_to_oam             @ 080bf552 fff7bdfe
    ldrb r0,[r4,#0x11]                       @ 080bf556 607c
    subs r0,#0x1    @ 080bf558 0138
    strb r0,[r4,#0x11]                       @ 080bf55a 6074
    lsls r0,r0,#0x18    @ 080bf55c 0006
    lsrs r0,r0,#0x18    @ 080bf55e 000e
    cmp r0,#0xff                             @ 080bf560 ff28
    beq LAB_080bf566                         @ 080bf562 00d0
    b LAB_080bf424                           @ 080bf564 5ee7
LAB_080bf566:
    ldrb r0,[r4,#0x10]                       @ 080bf566 207c
    adds r0,#0x1    @ 080bf568 0130
    strb r0,[r4,#0x10]                       @ 080bf56a 2074
    b LAB_080bf424                           @ 080bf56c 5ae7
LAB_080bf56e:
    movs r0,#0x2    @ 080bf56e 0220
    rsbs r0,r0,#0    @ 080bf570 4042
    ldrb r1,[r4,#0x0]                        @ 080bf572 2178
    ands r0,r1    @ 080bf574 0840
    strb r0,[r4,#0x0]                        @ 080bf576 2070
    ldr r1, DAT_080bf598                     @ 080bf578 0749
    ldr r2, DAT_080bf59c                     @ 080bf57a 084a
    adds r1,r1,r2    @ 080bf57c 8918
    movs r0,#0x5    @ 080bf57e 0520
    rsbs r0,r0,#0    @ 080bf580 4042
    ldrb r2,[r1,#0x0]                        @ 080bf582 0a78
    ands r0,r2    @ 080bf584 1040
    strb r0,[r1,#0x0]                        @ 080bf586 0870
    movs r0,#0x0    @ 080bf588 0020
LAB_080bf58a:
    add sp,#0x4                              @ 080bf58a 01b0
    pop {r3,r4}                              @ 080bf58c 18bc
    .hword 0x4698    @ 080bf58e 9846
    .hword 0x46a1    @ 080bf590 a146
    pop {r4,r5,r6,r7}                        @ 080bf592 f0bc
    pop {r1}                                 @ 080bf594 02bc
    bx r1                                    @ 080bf596 0847
DAT_080bf598:
    .word  0x02023130                     @ 080bf598 30310202
DAT_080bf59c:
    .word  0x00000215                     @ 080bf59c 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x38 子状态机, 待详细分析.
play_ui_effect_38:
    push {r4,r5,r6,lr}                       @ 080bf5a0 70b5
    ldr r2, DAT_080bf5e0                     @ 080bf5a2 0f4a
    ldr r5,[r2,#0x4]                         @ 080bf5a4 5568
    ldr r6,[r2,#0xc]                         @ 080bf5a6 d668
    ldr r1, DAT_080bf5e4                     @ 080bf5a8 0e49
    movs r0,#0x7f    @ 080bf5aa 7f20
    ldrb r3,[r2,#0x11]                       @ 080bf5ac 537c
    ands r0,r3    @ 080bf5ae 1840
    lsls r0,r0,#0x1    @ 080bf5b0 4000
    adds r0,r0,r1    @ 080bf5b2 4018
    movs r3,#0x0    @ 080bf5b4 0023
    ldrsh r1,[r0,r3]                         @ 080bf5b6 c15e
    movs r0,#0x78    @ 080bf5b8 7820
    ldrh r3,[r2,#0x12]                       @ 080bf5ba 538a
    asrs r0,r3    @ 080bf5bc 1841
    muls r0,r1    @ 080bf5be 4843
    adds r3,r2,#0x0    @ 080bf5c0 131c
    cmp r0,#0x0                              @ 080bf5c2 0028
    bge LAB_080bf5c8                         @ 080bf5c4 00da
    adds r0,#0xff    @ 080bf5c6 ff30
LAB_080bf5c8:
    lsls r0,r0,#0x8    @ 080bf5c8 0002
    lsrs r4,r0,#0x10    @ 080bf5ca 040c
    ldrb r0,[r2,#0x10]                       @ 080bf5cc 107c
    cmp r0,#0x5                              @ 080bf5ce 0528
    bls LAB_080bf5d4                         @ 080bf5d0 00d9
switchD_080bf5dc__default:
    b LAB_080bf7cc                           @ 080bf5d2 fbe0
LAB_080bf5d4:
    lsls r0,r0,#0x2    @ 080bf5d4 8000
    ldr r1, DAT_080bf5e8                     @ 080bf5d6 0449
    adds r0,r0,r1    @ 080bf5d8 4018
    ldr r0,[r0,#0x0]                         @ 080bf5da 0068
switchD_080bf5dc__switchD:
    .hword 0x4687    @ 080bf5dc 8746
    .zero  0x2
DAT_080bf5e0:
    .word  gBannerState                   @ 080bf5e0 c0fe0102
DAT_080bf5e4:
    .word  rom_sin_table_q8               @ 080bf5e4 f0f8e509
DAT_080bf5e8:
    .word  0x080bf5ec                     @ 080bf5e8 ecf50b08
switchD_080bf5dc__switchdataD_080bf5ec:
    .word  0x080bf604                     @ 080bf5ec 04f60b08
    .word  0x080bf6c8                     @ 080bf5f0 c8f60b08
    .word  0x080bf6f4                     @ 080bf5f4 f4f60b08
    .word  0x080bf75c                     @ 080bf5f8 5cf70b08
    .word  0x080bf790                     @ 080bf5fc 90f70b08
    .word  0x080bf7b0                     @ 080bf600 b0f70b08
switchD_080bf5dc__caseD_0:
    ldr r0, DAT_080bf69c                     @ 080bf604 2548
    ldr r4, DAT_080bf6a0                     @ 080bf606 264c
    adds r1,r4,#0x0    @ 080bf608 211c
    movs r2,#0x10    @ 080bf60a 1022
    movs r3,#0x10    @ 080bf60c 1023
    bl tile_2d_row_copy                      @ 080bf60e 37f061ff
    ldr r0, DAT_080bf6a4                     @ 080bf612 2448
    movs r1,#0x80    @ 080bf614 8021
    lsls r1,r1,#0x6    @ 080bf616 8901
    adds r4,r4,r1    @ 080bf618 6418
    adds r1,r4,#0x0    @ 080bf61a 211c
    movs r2,#0x10    @ 080bf61c 1022
    movs r3,#0xe    @ 080bf61e 0e23
    bl tile_2d_row_copy                      @ 080bf620 37f058ff
    ldr r2, DAT_080bf6a8                     @ 080bf624 204a
    ldr r0, DAT_080bf6ac                     @ 080bf626 2148
    ldr r0,[r0,#0x4]                         @ 080bf628 4068
    movs r1,#0x1    @ 080bf62a 0121
    eors r0,r1    @ 080bf62c 4840
    cmp r5,r0                                @ 080bf62e 8542
    bne LAB_080bf634                         @ 080bf630 00d1
    adds r2,#0x40    @ 080bf632 4032
LAB_080bf634:
    ldr r0, DAT_080bf6b0                     @ 080bf634 1e48
    adds r1,r2,#0x0    @ 080bf636 111c
    movs r2,#0x40    @ 080bf638 4022
    bl copy_bytes_by_halfword                @ 080bf63a 35f033fc
    ldr r4, DAT_080bf6b4                     @ 080bf63e 1d4c
    ldr r1, DAT_080bf6b8                     @ 080bf640 1d49
    ldr r2, DAT_080bf6bc                     @ 080bf642 1e4a
    adds r0,r4,#0x0    @ 080bf644 201c
    movs r3,#0x1    @ 080bf646 0123
    bl init_aob_ctx_from_ptnsect             @ 080bf648 38f0acfb
    movs r0,#0x1    @ 080bf64c 0120
    ldrb r2,[r4,#0x13]                       @ 080bf64e e27c
    orrs r0,r2    @ 080bf650 1043
    movs r1,#0x20    @ 080bf652 2021
    orrs r0,r1    @ 080bf654 0843
    strb r0,[r4,#0x13]                       @ 080bf656 e074
    adds r0,r4,#0x0    @ 080bf658 201c
    movs r1,#0x0    @ 080bf65a 0021
    movs r2,#0x1    @ 080bf65c 0122
    bl init_aob_ctx_with_anm_entry           @ 080bf65e 38f0f3fb
    ldr r1, PTR_WIN0H_080bf6c0               @ 080bf662 1749
    ldr r3, DAT_080bf6c4                     @ 080bf664 174b
    adds r0,r3,#0x0    @ 080bf666 181c
    strh r0,[r1,#0x0]                        @ 080bf668 0880
    adds r1,#0x4    @ 080bf66a 0431
    movs r0,#0x90    @ 080bf66c 9020
    strh r0,[r1,#0x0]                        @ 080bf66e 0880
    adds r1,#0x4    @ 080bf670 0431
    movs r0,#0x3f    @ 080bf672 3f20
    strh r0,[r1,#0x0]                        @ 080bf674 0880
    adds r1,#0x2    @ 080bf676 0231
    movs r0,#0x1f    @ 080bf678 1f20
    strh r0,[r1,#0x0]                        @ 080bf67a 0880
    adds r1,#0x6    @ 080bf67c 0631
    movs r0,#0xcc    @ 080bf67e cc20
    strh r0,[r1,#0x0]                        @ 080bf680 0880
    adds r1,#0x4    @ 080bf682 0431
    movs r0,#0x0    @ 080bf684 0020
    strh r0,[r1,#0x0]                        @ 080bf686 0880
    movs r2,#0x80    @ 080bf688 8022
    lsls r2,r2,#0x13    @ 080bf68a d204
    ldrh r0,[r2,#0x0]                        @ 080bf68c 1088
    movs r3,#0x80    @ 080bf68e 8023
    lsls r3,r3,#0x6    @ 080bf690 9b01
    adds r1,r3,#0x0    @ 080bf692 191c
    orrs r0,r1    @ 080bf694 0843
    strh r0,[r2,#0x0]                        @ 080bf696 1080
    subs r4,#0x1c    @ 080bf698 1c3c
    b LAB_080bf74e                           @ 080bf69a 58e0
DAT_080bf69c:
    .word  0x06014000                     @ 080bf69c 00400106
DAT_080bf6a0:
    .word  0x09899e08                     @ 080bf6a0 089e8909
DAT_080bf6a4:
    .word  0x06014200                     @ 080bf6a4 00420106
DAT_080bf6a8:
    .word  0x0989da08                     @ 080bf6a8 08da8909
DAT_080bf6ac:
    .word  0x0201e2a0                     @ 080bf6ac a0e20102
DAT_080bf6b0:
    .word  0x05000260                     @ 080bf6b0 60020005
DAT_080bf6b4:
    .word  0x0201fedc                     @ 080bf6b4 dcfe0102
DAT_080bf6b8:
    .word  0x0989da88                     @ 080bf6b8 88da8909
DAT_080bf6bc:
    .word  0x02000003                     @ 080bf6bc 03000002
PTR_WIN0H_080bf6c0:
    .word  WIN0H                          @ 080bf6c0 40000004
DAT_080bf6c4:
    .word  0x000028f0                     @ 080bf6c4 f0280000
switchD_080bf5dc__caseD_1:
    ldr r1, PTR_BLDY_080bf6f0                @ 080bf6c8 0949
    ldrh r2,[r3,#0x12]                       @ 080bf6ca 5a8a
    lsls r0,r2,#0x1    @ 080bf6cc 5000
    strh r0,[r1,#0x0]                        @ 080bf6ce 0880
    ldrh r0,[r3,#0x12]                       @ 080bf6d0 588a
    adds r0,#0x1    @ 080bf6d2 0130
    strh r0,[r3,#0x12]                       @ 080bf6d4 5882
    lsls r0,r0,#0x10    @ 080bf6d6 0004
    lsrs r0,r0,#0x10    @ 080bf6d8 000c
    cmp r0,#0x4                              @ 080bf6da 0428
    bls LAB_080bf7c2                         @ 080bf6dc 71d9
    movs r0,#0x0    @ 080bf6de 0020
    strh r0,[r3,#0x12]                       @ 080bf6e0 5882
    ldrb r0,[r3,#0x10]                       @ 080bf6e2 187c
    adds r0,#0x1    @ 080bf6e4 0130
    strb r0,[r3,#0x10]                       @ 080bf6e6 1874
    movs r0,#0x20    @ 080bf6e8 2020
    strb r0,[r3,#0x11]                       @ 080bf6ea 5874
    b LAB_080bf7c2                           @ 080bf6ec 69e0
    .zero  0x2
PTR_BLDY_080bf6f0:
    .word  BLDY                           @ 080bf6f0 54000004
switchD_080bf5dc__caseD_2:
    ldr r5, DAT_080bf758                     @ 080bf6f4 184d
    movs r1,#0x96    @ 080bf6f6 9621
    lsls r1,r1,#0x2    @ 080bf6f8 8900
    subs r1,r1,r4    @ 080bf6fa 091b
    lsls r1,r1,#0x10    @ 080bf6fc 0904
    movs r0,#0x7c    @ 080bf6fe 7c20
    orrs r1,r0    @ 080bf700 0143
    adds r0,r5,#0x0    @ 080bf702 281c
    movs r2,#0x0    @ 080bf704 0022
    movs r3,#0x0    @ 080bf706 0023
    bl render_aob_frame_to_oam               @ 080bf708 38f07afc
    adds r0,r5,#0x0    @ 080bf70c 281c
    bl tick_aob_frame_counter                @ 080bf70e 38f0fbfb
    adds r4,r5,#0x0    @ 080bf712 2c1c
    subs r4,#0x1c    @ 080bf714 1c3c
    ldrb r0,[r4,#0x11]                       @ 080bf716 607c
    adds r0,#0x3    @ 080bf718 0330
    strb r0,[r4,#0x11]                       @ 080bf71a 6074
    lsls r0,r0,#0x18    @ 080bf71c 0006
    lsrs r0,r0,#0x18    @ 080bf71e 000e
    cmp r0,#0x40                             @ 080bf720 4028
    bls LAB_080bf7c2                         @ 080bf722 4ed9
    movs r0,#0x1e    @ 080bf724 1e20
    bl sync_state_and_init_sprite            @ 080bf726 3af0c5f9
    movs r0,#0x0    @ 080bf72a 0020
    strb r0,[r4,#0x11]                       @ 080bf72c 6074
    ldrh r0,[r4,#0x12]                       @ 080bf72e 608a
    cmp r0,#0x0                              @ 080bf730 0028
    bne LAB_080bf740                         @ 080bf732 05d1
    lsls r1,r6,#0x10    @ 080bf734 3104
    lsrs r1,r1,#0x10    @ 080bf736 090c
    adds r0,r5,#0x0    @ 080bf738 281c
    movs r2,#0x0    @ 080bf73a 0022
    bl init_aob_ctx_with_anm_entry           @ 080bf73c 38f084fb
LAB_080bf740:
    ldrh r0,[r4,#0x12]                       @ 080bf740 608a
    adds r0,#0x1    @ 080bf742 0130
    strh r0,[r4,#0x12]                       @ 080bf744 6082
    lsls r0,r0,#0x10    @ 080bf746 0004
    lsrs r0,r0,#0x10    @ 080bf748 000c
    cmp r0,#0x1                              @ 080bf74a 0128
    bls LAB_080bf7c2                         @ 080bf74c 39d9
LAB_080bf74e:
    ldrb r0,[r4,#0x10]                       @ 080bf74e 207c
    adds r0,#0x1    @ 080bf750 0130
    strb r0,[r4,#0x10]                       @ 080bf752 2074
    b LAB_080bf7c2                           @ 080bf754 35e0
    .zero  0x2
DAT_080bf758:
    .word  0x0201fedc                     @ 080bf758 dcfe0102
switchD_080bf5dc__caseD_3:
    ldr r4, DAT_080bf788                     @ 080bf75c 0a4c
    ldr r1, DAT_080bf78c                     @ 080bf75e 0b49
    adds r0,r4,#0x0    @ 080bf760 201c
    movs r2,#0x0    @ 080bf762 0022
    movs r3,#0x0    @ 080bf764 0023
    bl render_aob_frame_to_oam               @ 080bf766 38f04bfc
    adds r0,r4,#0x0    @ 080bf76a 201c
    bl tick_aob_frame_counter                @ 080bf76c 38f0ccfb
    adds r2,r0,#0x0    @ 080bf770 021c
    cmp r2,#0x0                              @ 080bf772 002a
    bne LAB_080bf7c2                         @ 080bf774 25d1
    adds r0,r4,#0x0    @ 080bf776 201c
    subs r0,#0x1c    @ 080bf778 1c38
    ldrb r1,[r0,#0x10]                       @ 080bf77a 017c
    adds r1,#0x1    @ 080bf77c 0131
    strb r1,[r0,#0x10]                       @ 080bf77e 0174
    strb r2,[r0,#0x11]                       @ 080bf780 4274
    strh r2,[r0,#0x12]                       @ 080bf782 4282
    b LAB_080bf7c2                           @ 080bf784 1de0
    .zero  0x2
DAT_080bf788:
    .word  0x0201fedc                     @ 080bf788 dcfe0102
DAT_080bf78c:
    .word  0x0058007c                     @ 080bf78c 7c005800
switchD_080bf5dc__caseD_4:
    ldr r2, PTR_BLDY_080bf7ac                @ 080bf790 064a
    ldrh r0,[r3,#0x12]                       @ 080bf792 588a
    lsls r1,r0,#0x1    @ 080bf794 4100
    movs r0,#0x8    @ 080bf796 0820
    subs r0,r0,r1    @ 080bf798 401a
    strh r0,[r2,#0x0]                        @ 080bf79a 1080
    ldrh r0,[r3,#0x12]                       @ 080bf79c 588a
    adds r0,#0x1    @ 080bf79e 0130
    strh r0,[r3,#0x12]                       @ 080bf7a0 5882
    lsls r0,r0,#0x10    @ 080bf7a2 0004
    lsrs r0,r0,#0x10    @ 080bf7a4 000c
    cmp r0,#0x4                              @ 080bf7a6 0428
    bls LAB_080bf7c2                         @ 080bf7a8 0bd9
    b LAB_080bf7bc                           @ 080bf7aa 07e0
PTR_BLDY_080bf7ac:
    .word  BLDY                           @ 080bf7ac 54000004
switchD_080bf5dc__caseD_5:
    movs r2,#0x80    @ 080bf7b0 8022
    lsls r2,r2,#0x13    @ 080bf7b2 d204
    ldrh r1,[r2,#0x0]                        @ 080bf7b4 1188
    ldr r0, DAT_080bf7c8                     @ 080bf7b6 0448
    ands r0,r1    @ 080bf7b8 0840
    strh r0,[r2,#0x0]                        @ 080bf7ba 1080
LAB_080bf7bc:
    ldrb r0,[r3,#0x10]                       @ 080bf7bc 187c
    adds r0,#0x1    @ 080bf7be 0130
    strb r0,[r3,#0x10]                       @ 080bf7c0 1874
LAB_080bf7c2:
    movs r0,#0x1    @ 080bf7c2 0120
    b LAB_080bf7e8                           @ 080bf7c4 10e0
    .zero  0x2
DAT_080bf7c8:
    .word  0x0000dfff                     @ 080bf7c8 ffdf0000
LAB_080bf7cc:
    movs r0,#0x2    @ 080bf7cc 0220
    rsbs r0,r0,#0    @ 080bf7ce 4042
    ldrb r1,[r2,#0x0]                        @ 080bf7d0 1178
    ands r0,r1    @ 080bf7d2 0840
    strb r0,[r2,#0x0]                        @ 080bf7d4 1070
    ldr r1, DAT_080bf7f0                     @ 080bf7d6 0649
    ldr r2, DAT_080bf7f4                     @ 080bf7d8 064a
    adds r1,r1,r2    @ 080bf7da 8918
    movs r0,#0x5    @ 080bf7dc 0520
    rsbs r0,r0,#0    @ 080bf7de 4042
    ldrb r3,[r1,#0x0]                        @ 080bf7e0 0b78
    ands r0,r3    @ 080bf7e2 1840
    strb r0,[r1,#0x0]                        @ 080bf7e4 0870
    movs r0,#0x0    @ 080bf7e6 0020
LAB_080bf7e8:
    pop {r4,r5,r6}                           @ 080bf7e8 70bc
    pop {r1}                                 @ 080bf7ea 02bc
    bx r1                                    @ 080bf7ec 0847
    .zero  0x2
DAT_080bf7f0:
    .word  0x02023130                     @ 080bf7f0 30310202
DAT_080bf7f4:
    .word  0x00000215                     @ 080bf7f4 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x37 子状态机, 待详细分析.
play_ui_effect_37:
    push {r4,r5,r6,r7,lr}                    @ 080bf7f8 f0b5
    .hword 0x4657    @ 080bf7fa 5746
    .hword 0x464e    @ 080bf7fc 4e46
    .hword 0x4645    @ 080bf7fe 4546
    push {r5,r6,r7}                          @ 080bf800 e0b4
    sub sp,#0x10                             @ 080bf802 84b0
    ldr r1, DAT_080bf82c                     @ 080bf804 0949
    ldrb r6,[r1,#0x4]                        @ 080bf806 0e79
    ldrb r0,[r1,#0x8]                        @ 080bf808 087a
    .hword 0x4681    @ 080bf80a 8146
    ldrb r2,[r1,#0x9]                        @ 080bf80c 4a7a
    str r2,[sp,#0x0]                         @ 080bf80e 0092
    ldrh r3,[r1,#0xc]                        @ 080bf810 8b89
    str r3,[sp,#0x4]                         @ 080bf812 0193
    movs r4,#0x0    @ 080bf814 0024
    str r4,[sp,#0x8]                         @ 080bf816 0294
    ldrb r0,[r1,#0x10]                       @ 080bf818 087c
    adds r4,r1,#0x0    @ 080bf81a 0c1c
    cmp r0,#0x4                              @ 080bf81c 0428
    bls LAB_080bf822                         @ 080bf81e 00d9
switchD_080bf82a__default:
    b LAB_080bfdd8                           @ 080bf820 dae2
LAB_080bf822:
    lsls r0,r0,#0x2    @ 080bf822 8000
    ldr r1, DAT_080bf830                     @ 080bf824 0249
    adds r0,r0,r1    @ 080bf826 4018
    ldr r0,[r0,#0x0]                         @ 080bf828 0068
switchD_080bf82a__switchD:
    .hword 0x4687    @ 080bf82a 8746
DAT_080bf82c:
    .word  gBannerState                   @ 080bf82c c0fe0102
DAT_080bf830:
    .word  0x080bf834                     @ 080bf830 34f80b08
switchD_080bf82a__switchdataD_080bf834:
    .word  0x080bf848                     @ 080bf834 48f80b08
    .word  0x080bfc2c                     @ 080bf838 2cfc0b08
    .word  0x080bfc5c                     @ 080bf83c 5cfc0b08
    .word  0x080bfd7e                     @ 080bf840 7efd0b08
    .word  0x080bfda4                     @ 080bf844 a4fd0b08
switchD_080bf82a__caseD_0:
    ldr r0, DAT_080bf898                     @ 080bf848 1348
    ldr r1, DAT_080bf89c                     @ 080bf84a 1449
    movs r2,#0x10    @ 080bf84c 1022
    movs r3,#0x10    @ 080bf84e 1023
    bl tile_2d_row_copy                      @ 080bf850 37f040fe
    ldr r0, DAT_080bf8a0                     @ 080bf854 1248
    ldr r1, DAT_080bf8a4                     @ 080bf856 1349
    movs r2,#0x40    @ 080bf858 4022
    bl copy_bytes_by_halfword                @ 080bf85a 35f023fb
    movs r7,#0x0    @ 080bf85e 0027
    cmp r7,r9                                @ 080bf860 4f45
    bge LAB_080bf8f0                         @ 080bf862 45da
    movs r5,#0x0    @ 080bf864 0025
LAB_080bf866:
    ldr r0, DAT_080bf8a8                     @ 080bf866 1048
    adds r4,r5,r0    @ 080bf868 2c18
    adds r0,r4,#0x0    @ 080bf86a 201c
    ldr r1, DAT_080bf8ac                     @ 080bf86c 0f49
    ldr r2, DAT_080bf8b0                     @ 080bf86e 104a
    movs r3,#0x1    @ 080bf870 0123
    bl init_aob_ctx_from_ptnsect             @ 080bf872 38f097fa
    movs r0,#0x1    @ 080bf876 0120
    ldrb r1,[r4,#0x13]                       @ 080bf878 e17c
    orrs r0,r1    @ 080bf87a 0843
    strb r0,[r4,#0x13]                       @ 080bf87c e074
    ldr r2,[sp,#0x0]                         @ 080bf87e 009a
    cmp r2,#0x0                              @ 080bf880 002a
    beq LAB_080bf8ba                         @ 080bf882 1ad0
    ldr r0,[sp,#0x4]                         @ 080bf884 0198
    asrs r0,r7    @ 080bf886 3841
    movs r1,#0x1    @ 080bf888 0121
    ands r0,r1    @ 080bf88a 0840
    cmp r0,#0x0                              @ 080bf88c 0028
    bne LAB_080bf8b4                         @ 080bf88e 11d1
    adds r0,r4,#0x0    @ 080bf890 201c
    movs r1,#0x3    @ 080bf892 0321
    b LAB_080bf8ca                           @ 080bf894 19e0
    .zero  0x2
DAT_080bf898:
    .word  0x06014000                     @ 080bf898 00400106
DAT_080bf89c:
    .word  0x098977f8                     @ 080bf89c f8778909
DAT_080bf8a0:
    .word  0x05000300                     @ 080bf8a0 00030005
DAT_080bf8a4:
    .word  0x098997f8                     @ 080bf8a4 f8978909
DAT_080bf8a8:
    .word  0x0201fedc                     @ 080bf8a8 dcfe0102
DAT_080bf8ac:
    .word  0x09899838                     @ 080bf8ac 38988909
DAT_080bf8b0:
    .word  0x02000007                     @ 080bf8b0 07000002
LAB_080bf8b4:
    adds r0,r4,#0x0    @ 080bf8b4 201c
    movs r1,#0x0    @ 080bf8b6 0021
    b LAB_080bf8ca                           @ 080bf8b8 07e0
LAB_080bf8ba:
    ldr r0,[sp,#0x4]                         @ 080bf8ba 0198
    asrs r0,r7    @ 080bf8bc 3841
    movs r1,#0x1    @ 080bf8be 0121
    ands r0,r1    @ 080bf8c0 0840
    cmp r0,#0x0                              @ 080bf8c2 0028
    bne LAB_080bf8d2                         @ 080bf8c4 05d1
    adds r0,r4,#0x0    @ 080bf8c6 201c
    movs r1,#0x2    @ 080bf8c8 0221
LAB_080bf8ca:
    movs r2,#0x0    @ 080bf8ca 0022
    bl init_aob_ctx_with_anm_entry           @ 080bf8cc 38f0bcfa
    b LAB_080bf8dc                           @ 080bf8d0 04e0
LAB_080bf8d2:
    adds r0,r4,#0x0    @ 080bf8d2 201c
    movs r1,#0x1    @ 080bf8d4 0121
    movs r2,#0x0    @ 080bf8d6 0022
    bl init_aob_ctx_with_anm_entry           @ 080bf8d8 38f0b6fa
LAB_080bf8dc:
    ldr r1, DAT_080bf960                     @ 080bf8dc 2049
    adds r1,r5,r1    @ 080bf8de 6918
    movs r0,#0x20    @ 080bf8e0 2020
    ldrb r3,[r1,#0x13]                       @ 080bf8e2 cb7c
    orrs r0,r3    @ 080bf8e4 1843
    strb r0,[r1,#0x13]                       @ 080bf8e6 c874
    adds r5,#0x14    @ 080bf8e8 1435
    adds r7,#0x1    @ 080bf8ea 0137
    cmp r7,r9                                @ 080bf8ec 4f45
    blt LAB_080bf866                         @ 080bf8ee badb
LAB_080bf8f0:
    ldr r0, DAT_080bf964                     @ 080bf8f0 1c48
    movs r1,#0x0    @ 080bf8f2 0021
    movs r2,#0x8    @ 080bf8f4 0822
    movs r3,#0x4    @ 080bf8f6 0423
    bl tile_2d_row_copy                      @ 080bf8f8 37f0ecfd
    movs r0,#0x8    @ 080bf8fc 0820
    movs r1,#0x4    @ 080bf8fe 0421
    movs r2,#0x1    @ 080bf900 0122
    movs r3,#0x0    @ 080bf902 0023
    bl setup_line_buf_with_font_and_align    @ 080bf904 31f0dcf9
    ldr r2, DAT_080bf968                     @ 080bf908 174a
    ldr r0, DAT_080bf96c                     @ 080bf90a 1848
    ldr r4, DAT_080bf970                     @ 080bf90c 184c
    adds r0,r0,r4    @ 080bf90e 0019
    movs r3,#0x7    @ 080bf910 0723
    ldrb r0,[r0,#0x0]                        @ 080bf912 0078
    ands r3,r0    @ 080bf914 0340
    rsbs r1,r3,#0    @ 080bf916 5942
    lsrs r1,r1,#0x1f    @ 080bf918 c90f
    movs r0,#0x2    @ 080bf91a 0220
    rsbs r0,r0,#0    @ 080bf91c 4042
    ldrb r4,[r2,#0x8]                        @ 080bf91e 147a
    ands r0,r4    @ 080bf920 2040
    orrs r0,r1    @ 080bf922 0843
    movs r1,#0x3    @ 080bf924 0321
    rsbs r1,r1,#0    @ 080bf926 4942
    ands r0,r1    @ 080bf928 0840
    strb r0,[r2,#0x8]                        @ 080bf92a 1072
    ldr r1, PTR_font_jp_base_table_080bf974  @ 080bf92c 1149
    lsls r0,r0,#0x1f    @ 080bf92e c007
    lsrs r0,r0,#0x1f    @ 080bf930 c00f
    lsls r0,r0,#0x3    @ 080bf932 c000
    adds r0,r0,r1    @ 080bf934 4018
    ldr r0,[r0,#0x0]                         @ 080bf936 0068
    str r0,[r2,#0x4]                         @ 080bf938 5060
    movs r0,#0x40    @ 080bf93a 4020
    ldrb r1,[r2,#0x15]                       @ 080bf93c 517d
    orrs r0,r1    @ 080bf93e 0843
    strb r0,[r2,#0x15]                       @ 080bf940 5075
    cmp r3,#0x1                              @ 080bf942 012b
    beq LAB_080bf998                         @ 080bf944 28d0
    cmp r3,#0x2                              @ 080bf946 022b
    beq LAB_080bf990                         @ 080bf948 22d0
    cmp r3,#0x3                              @ 080bf94a 032b
    beq LAB_080bf988                         @ 080bf94c 1cd0
    cmp r3,#0x4                              @ 080bf94e 042b
    beq LAB_080bf980                         @ 080bf950 16d0
    ldr r0, DAT_080bf978                     @ 080bf952 0948
    cmp r3,#0x5                              @ 080bf954 052b
    bne LAB_080bf99a                         @ 080bf956 20d1
    ldr r2, DAT_080bf97c                     @ 080bf958 084a
    adds r0,r0,r2    @ 080bf95a 8018
    b LAB_080bf99a                           @ 080bf95c 1de0
    .zero  0x2
DAT_080bf960:
    .word  0x0201fedc                     @ 080bf960 dcfe0102
DAT_080bf964:
    .word  0x06014200                     @ 080bf964 00420106
DAT_080bf968:
    .word  0x02006ed0                     @ 080bf968 d06e0002
DAT_080bf96c:
    .word  0x02000000                     @ 080bf96c 00000002
DAT_080bf970:
    .word  0x00006c2c                     @ 080bf970 2c6c0000
PTR_font_jp_base_table_080bf974:
    .word  font_jp_base_table             @ 080bf974 54f8e509
DAT_080bf978:
    .word  0x09dbd7f2                     @ 080bf978 f2d7db09
DAT_080bf97c:
    .word  0x0003a90e                     @ 080bf97c 0ea90300
LAB_080bf980:
    ldr r0, DAT_080bf984                     @ 080bf980 0048
    b LAB_080bf99a                           @ 080bf982 0ae0
DAT_080bf984:
    .word  0x09dec2e6                     @ 080bf984 e6c2de09
LAB_080bf988:
    ldr r0, DAT_080bf98c                     @ 080bf988 0048
    b LAB_080bf99a                           @ 080bf98a 06e0
DAT_080bf98c:
    .word  0x09ddffea                     @ 080bf98c eaffdd09
LAB_080bf990:
    ldr r0, DAT_080bf994                     @ 080bf990 0048
    b LAB_080bf99a                           @ 080bf992 02e0
DAT_080bf994:
    .word  0x09dd3d0e                     @ 080bf994 0e3ddd09
LAB_080bf998:
    ldr r0, DAT_080bf9e4                     @ 080bf998 1248
LAB_080bf99a:
    bl measure_string_pixel_width            @ 080bf99a 30f06bfc
    adds r4,r0,#0x0    @ 080bf99e 041c
    movs r0,#0x40    @ 080bf9a0 4020
    subs r0,r0,r4    @ 080bf9a2 001b
    lsrs r1,r0,#0x1f    @ 080bf9a4 c10f
    adds r0,r0,r1    @ 080bf9a6 4018
    asrs r0,r0,#0x1    @ 080bf9a8 4010
    adds r5,r0,#0x2    @ 080bf9aa 851c
    ldr r0, DAT_080bf9e8                     @ 080bf9ac 0e48
    ldr r0,[r0,#0x4]                         @ 080bf9ae 4068
    movs r1,#0x1    @ 080bf9b0 0121
    eors r0,r1    @ 080bf9b2 4840
    ldr r2, DAT_080bf9ec                     @ 080bf9b4 0d4a
    cmp r6,r0                                @ 080bf9b6 8642
    bne LAB_080bf9bc                         @ 080bf9b8 00d1
    adds r2,#0x1    @ 080bf9ba 0132
LAB_080bf9bc:
    ldr r0, DAT_080bf9f0                     @ 080bf9bc 0c48
    ldr r3, DAT_080bf9f4                     @ 080bf9be 0d4b
    adds r0,r0,r3    @ 080bf9c0 c018
    movs r1,#0x7    @ 080bf9c2 0721
    ldrb r0,[r0,#0x0]                        @ 080bf9c4 0078
    ands r1,r0    @ 080bf9c6 0140
    cmp r1,#0x1                              @ 080bf9c8 0129
    beq LAB_080bfa18                         @ 080bf9ca 25d0
    cmp r1,#0x2                              @ 080bf9cc 0229
    beq LAB_080bfa10                         @ 080bf9ce 1fd0
    cmp r1,#0x3                              @ 080bf9d0 0329
    beq LAB_080bfa08                         @ 080bf9d2 19d0
    cmp r1,#0x4                              @ 080bf9d4 0429
    beq LAB_080bfa00                         @ 080bf9d6 13d0
    ldr r3, DAT_080bf9f8                     @ 080bf9d8 074b
    cmp r1,#0x5                              @ 080bf9da 0529
    bne LAB_080bfa1a                         @ 080bf9dc 1dd1
    ldr r0, DAT_080bf9fc                     @ 080bf9de 0748
    adds r3,r3,r0    @ 080bf9e0 1b18
    b LAB_080bfa1a                           @ 080bf9e2 1ae0
DAT_080bf9e4:
    .word  0x09dc884c                     @ 080bf9e4 4c88dc09
DAT_080bf9e8:
    .word  0x0201e2a0                     @ 080bf9e8 a0e20102
DAT_080bf9ec:
    .word  0x00008001                     @ 080bf9ec 01800000
DAT_080bf9f0:
    .word  0x02000000                     @ 080bf9f0 00000002
DAT_080bf9f4:
    .word  0x00006c2c                     @ 080bf9f4 2c6c0000
DAT_080bf9f8:
    .word  0x09dbd7f2                     @ 080bf9f8 f2d7db09
DAT_080bf9fc:
    .word  0x0003a90e                     @ 080bf9fc 0ea90300
LAB_080bfa00:
    ldr r3, DAT_080bfa04                     @ 080bfa00 004b
    b LAB_080bfa1a                           @ 080bfa02 0ae0
DAT_080bfa04:
    .word  0x09dec2e6                     @ 080bfa04 e6c2de09
LAB_080bfa08:
    ldr r3, DAT_080bfa0c                     @ 080bfa08 004b
    b LAB_080bfa1a                           @ 080bfa0a 06e0
DAT_080bfa0c:
    .word  0x09ddffea                     @ 080bfa0c eaffdd09
LAB_080bfa10:
    ldr r3, DAT_080bfa14                     @ 080bfa10 004b
    b LAB_080bfa1a                           @ 080bfa12 02e0
DAT_080bfa14:
    .word  0x09dd3d0e                     @ 080bfa14 0e3ddd09
LAB_080bfa18:
    ldr r3, DAT_080bfa58                     @ 080bfa18 0f4b
LAB_080bfa1a:
    adds r0,r5,#0x0    @ 080bfa1a 281c
    movs r1,#0x2    @ 080bfa1c 0221
    bl text_render_wrapper                   @ 080bfa1e 33f02df8
    movs r0,#0x40    @ 080bfa22 4020
    subs r0,r0,r4    @ 080bfa24 001b
    lsrs r1,r0,#0x1f    @ 080bfa26 c10f
    adds r0,r0,r1    @ 080bfa28 4018
    asrs r0,r0,#0x1    @ 080bfa2a 4010
    adds r2,r0,#0x2    @ 080bfa2c 821c
    ldr r0, DAT_080bfa5c                     @ 080bfa2e 0b48
    ldr r1, DAT_080bfa60                     @ 080bfa30 0b49
    adds r0,r0,r1    @ 080bfa32 4018
    movs r1,#0x7    @ 080bfa34 0721
    ldrb r0,[r0,#0x0]                        @ 080bfa36 0078
    ands r1,r0    @ 080bfa38 0140
    cmp r1,#0x1                              @ 080bfa3a 0129
    beq LAB_080bfa84                         @ 080bfa3c 22d0
    cmp r1,#0x2                              @ 080bfa3e 0229
    beq LAB_080bfa7c                         @ 080bfa40 1cd0
    cmp r1,#0x3                              @ 080bfa42 0329
    beq LAB_080bfa74                         @ 080bfa44 16d0
    cmp r1,#0x4                              @ 080bfa46 0429
    beq LAB_080bfa6c                         @ 080bfa48 10d0
    ldr r3, DAT_080bfa64                     @ 080bfa4a 064b
    cmp r1,#0x5                              @ 080bfa4c 0529
    bne LAB_080bfa86                         @ 080bfa4e 1ad1
    ldr r4, DAT_080bfa68                     @ 080bfa50 054c
    adds r3,r3,r4    @ 080bfa52 1b19
    b LAB_080bfa86                           @ 080bfa54 17e0
    .zero  0x2
DAT_080bfa58:
    .word  0x09dc884c                     @ 080bfa58 4c88dc09
DAT_080bfa5c:
    .word  0x02000000                     @ 080bfa5c 00000002
DAT_080bfa60:
    .word  0x00006c2c                     @ 080bfa60 2c6c0000
DAT_080bfa64:
    .word  0x09dbd7f2                     @ 080bfa64 f2d7db09
DAT_080bfa68:
    .word  0x0003a90e                     @ 080bfa68 0ea90300
LAB_080bfa6c:
    ldr r3, DAT_080bfa70                     @ 080bfa6c 004b
    b LAB_080bfa86                           @ 080bfa6e 0ae0
DAT_080bfa70:
    .word  0x09dec2e6                     @ 080bfa70 e6c2de09
LAB_080bfa74:
    ldr r3, DAT_080bfa78                     @ 080bfa74 004b
    b LAB_080bfa86                           @ 080bfa76 06e0
DAT_080bfa78:
    .word  0x09ddffea                     @ 080bfa78 eaffdd09
LAB_080bfa7c:
    ldr r3, DAT_080bfa80                     @ 080bfa7c 004b
    b LAB_080bfa86                           @ 080bfa7e 02e0
DAT_080bfa80:
    .word  0x09dd3d0e                     @ 080bfa80 0e3ddd09
LAB_080bfa84:
    ldr r3, DAT_080bfab8                     @ 080bfa84 0c4b
LAB_080bfa86:
    adds r0,r2,#0x0    @ 080bfa86 101c
    movs r1,#0x2    @ 080bfa88 0221
    movs r2,#0x7    @ 080bfa8a 0722
    bl text_render_wrapper                   @ 080bfa8c 32f0f6ff
    ldr r0, DAT_080bfabc                     @ 080bfa90 0a48
    ldr r1, DAT_080bfac0                     @ 080bfa92 0b49
    adds r0,r0,r1    @ 080bfa94 4018
    movs r1,#0x7    @ 080bfa96 0721
    ldrb r0,[r0,#0x0]                        @ 080bfa98 0078
    ands r1,r0    @ 080bfa9a 0140
    cmp r1,#0x1                              @ 080bfa9c 0129
    beq LAB_080bfae4                         @ 080bfa9e 21d0
    cmp r1,#0x2                              @ 080bfaa0 0229
    beq LAB_080bfadc                         @ 080bfaa2 1bd0
    cmp r1,#0x3                              @ 080bfaa4 0329
    beq LAB_080bfad4                         @ 080bfaa6 15d0
    cmp r1,#0x4                              @ 080bfaa8 0429
    beq LAB_080bfacc                         @ 080bfaaa 0fd0
    ldr r0, DAT_080bfac4                     @ 080bfaac 0548
    cmp r1,#0x5                              @ 080bfaae 0529
    bne LAB_080bfae6                         @ 080bfab0 19d1
    ldr r2, DAT_080bfac8                     @ 080bfab2 054a
    adds r0,r0,r2    @ 080bfab4 8018
    b LAB_080bfae6                           @ 080bfab6 16e0
DAT_080bfab8:
    .word  0x09dc884c                     @ 080bfab8 4c88dc09
DAT_080bfabc:
    .word  0x02000000                     @ 080bfabc 00000002
DAT_080bfac0:
    .word  0x00006c2c                     @ 080bfac0 2c6c0000
DAT_080bfac4:
    .word  0x09dbd7e8                     @ 080bfac4 e8d7db09
DAT_080bfac8:
    .word  0x0003a90c                     @ 080bfac8 0ca90300
LAB_080bfacc:
    ldr r0, DAT_080bfad0                     @ 080bfacc 0048
    b LAB_080bfae6                           @ 080bface 0ae0
DAT_080bfad0:
    .word  0x09dec2de                     @ 080bfad0 dec2de09
LAB_080bfad4:
    ldr r0, DAT_080bfad8                     @ 080bfad4 0048
    b LAB_080bfae6                           @ 080bfad6 06e0
DAT_080bfad8:
    .word  0x09ddffe0                     @ 080bfad8 e0ffdd09
LAB_080bfadc:
    ldr r0, DAT_080bfae0                     @ 080bfadc 0048
    b LAB_080bfae6                           @ 080bfade 02e0
DAT_080bfae0:
    .word  0x09dd3d04                     @ 080bfae0 043ddd09
LAB_080bfae4:
    ldr r0, DAT_080bfb30                     @ 080bfae4 1248
LAB_080bfae6:
    bl measure_string_pixel_width            @ 080bfae6 30f0c5fb
    adds r4,r0,#0x0    @ 080bfaea 041c
    movs r0,#0x40    @ 080bfaec 4020
    subs r0,r0,r4    @ 080bfaee 001b
    lsrs r1,r0,#0x1f    @ 080bfaf0 c10f
    adds r0,r0,r1    @ 080bfaf2 4018
    asrs r0,r0,#0x1    @ 080bfaf4 4010
    adds r5,r0,#0x2    @ 080bfaf6 851c
    ldr r0, DAT_080bfb34                     @ 080bfaf8 0e48
    ldr r0,[r0,#0x4]                         @ 080bfafa 4068
    movs r1,#0x1    @ 080bfafc 0121
    eors r0,r1    @ 080bfafe 4840
    ldr r2, DAT_080bfb38                     @ 080bfb00 0d4a
    cmp r6,r0                                @ 080bfb02 8642
    bne LAB_080bfb08                         @ 080bfb04 00d1
    adds r2,#0x1    @ 080bfb06 0132
LAB_080bfb08:
    ldr r0, DAT_080bfb3c                     @ 080bfb08 0c48
    ldr r3, DAT_080bfb40                     @ 080bfb0a 0d4b
    adds r0,r0,r3    @ 080bfb0c c018
    movs r1,#0x7    @ 080bfb0e 0721
    ldrb r0,[r0,#0x0]                        @ 080bfb10 0078
    ands r1,r0    @ 080bfb12 0140
    cmp r1,#0x1                              @ 080bfb14 0129
    beq LAB_080bfb64                         @ 080bfb16 25d0
    cmp r1,#0x2                              @ 080bfb18 0229
    beq LAB_080bfb5c                         @ 080bfb1a 1fd0
    cmp r1,#0x3                              @ 080bfb1c 0329
    beq LAB_080bfb54                         @ 080bfb1e 19d0
    cmp r1,#0x4                              @ 080bfb20 0429
    beq LAB_080bfb4c                         @ 080bfb22 13d0
    ldr r3, DAT_080bfb44                     @ 080bfb24 074b
    cmp r1,#0x5                              @ 080bfb26 0529
    bne LAB_080bfb66                         @ 080bfb28 1dd1
    ldr r0, DAT_080bfb48                     @ 080bfb2a 0748
    adds r3,r3,r0    @ 080bfb2c 1b18
    b LAB_080bfb66                           @ 080bfb2e 1ae0
DAT_080bfb30:
    .word  0x09dc8842                     @ 080bfb30 4288dc09
DAT_080bfb34:
    .word  0x0201e2a0                     @ 080bfb34 a0e20102
DAT_080bfb38:
    .word  0x00008001                     @ 080bfb38 01800000
DAT_080bfb3c:
    .word  0x02000000                     @ 080bfb3c 00000002
DAT_080bfb40:
    .word  0x00006c2c                     @ 080bfb40 2c6c0000
DAT_080bfb44:
    .word  0x09dbd7e8                     @ 080bfb44 e8d7db09
DAT_080bfb48:
    .word  0x0003a90c                     @ 080bfb48 0ca90300
LAB_080bfb4c:
    ldr r3, DAT_080bfb50                     @ 080bfb4c 004b
    b LAB_080bfb66                           @ 080bfb4e 0ae0
DAT_080bfb50:
    .word  0x09dec2de                     @ 080bfb50 dec2de09
LAB_080bfb54:
    ldr r3, DAT_080bfb58                     @ 080bfb54 004b
    b LAB_080bfb66                           @ 080bfb56 06e0
DAT_080bfb58:
    .word  0x09ddffe0                     @ 080bfb58 e0ffdd09
LAB_080bfb5c:
    ldr r3, DAT_080bfb60                     @ 080bfb5c 004b
    b LAB_080bfb66                           @ 080bfb5e 02e0
DAT_080bfb60:
    .word  0x09dd3d04                     @ 080bfb60 043ddd09
LAB_080bfb64:
    ldr r3, DAT_080bfba4                     @ 080bfb64 0f4b
LAB_080bfb66:
    adds r0,r5,#0x0    @ 080bfb66 281c
    movs r1,#0x12    @ 080bfb68 1221
    bl text_render_wrapper                   @ 080bfb6a 32f087ff
    movs r0,#0x40    @ 080bfb6e 4020
    subs r0,r0,r4    @ 080bfb70 001b
    lsrs r1,r0,#0x1f    @ 080bfb72 c10f
    adds r0,r0,r1    @ 080bfb74 4018
    asrs r0,r0,#0x1    @ 080bfb76 4010
    adds r2,r0,#0x2    @ 080bfb78 821c
    ldr r0, DAT_080bfba8                     @ 080bfb7a 0b48
    ldr r1, DAT_080bfbac                     @ 080bfb7c 0b49
    adds r0,r0,r1    @ 080bfb7e 4018
    movs r1,#0x7    @ 080bfb80 0721
    ldrb r0,[r0,#0x0]                        @ 080bfb82 0078
    ands r1,r0    @ 080bfb84 0140
    cmp r1,#0x1                              @ 080bfb86 0129
    beq LAB_080bfbd0                         @ 080bfb88 22d0
    cmp r1,#0x2                              @ 080bfb8a 0229
    beq LAB_080bfbc8                         @ 080bfb8c 1cd0
    cmp r1,#0x3                              @ 080bfb8e 0329
    beq LAB_080bfbc0                         @ 080bfb90 16d0
    cmp r1,#0x4                              @ 080bfb92 0429
    beq LAB_080bfbb8                         @ 080bfb94 10d0
    ldr r3, DAT_080bfbb0                     @ 080bfb96 064b
    cmp r1,#0x5                              @ 080bfb98 0529
    bne LAB_080bfbd2                         @ 080bfb9a 1ad1
    ldr r4, DAT_080bfbb4                     @ 080bfb9c 054c
    adds r3,r3,r4    @ 080bfb9e 1b19
    b LAB_080bfbd2                           @ 080bfba0 17e0
    .zero  0x2
DAT_080bfba4:
    .word  0x09dc8842                     @ 080bfba4 4288dc09
DAT_080bfba8:
    .word  0x02000000                     @ 080bfba8 00000002
DAT_080bfbac:
    .word  0x00006c2c                     @ 080bfbac 2c6c0000
DAT_080bfbb0:
    .word  0x09dbd7e8                     @ 080bfbb0 e8d7db09
DAT_080bfbb4:
    .word  0x0003a90c                     @ 080bfbb4 0ca90300
LAB_080bfbb8:
    ldr r3, DAT_080bfbbc                     @ 080bfbb8 004b
    b LAB_080bfbd2                           @ 080bfbba 0ae0
DAT_080bfbbc:
    .word  0x09dec2de                     @ 080bfbbc dec2de09
LAB_080bfbc0:
    ldr r3, DAT_080bfbc4                     @ 080bfbc0 004b
    b LAB_080bfbd2                           @ 080bfbc2 06e0
DAT_080bfbc4:
    .word  0x09ddffe0                     @ 080bfbc4 e0ffdd09
LAB_080bfbc8:
    ldr r3, DAT_080bfbcc                     @ 080bfbc8 004b
    b LAB_080bfbd2                           @ 080bfbca 02e0
DAT_080bfbcc:
    .word  0x09dd3d04                     @ 080bfbcc 043ddd09
LAB_080bfbd0:
    ldr r3, DAT_080bfc1c                     @ 080bfbd0 124b
LAB_080bfbd2:
    adds r0,r2,#0x0    @ 080bfbd2 101c
    movs r1,#0x12    @ 080bfbd4 1221
    movs r2,#0x7    @ 080bfbd6 0722
    bl text_render_wrapper                   @ 080bfbd8 32f050ff
    ldr r0, DAT_080bfc20                     @ 080bfbdc 1048
    movs r1,#0x0    @ 080bfbde 0021
    bl write_line_buf_to_bg_tile_vram        @ 080bfbe0 33f0f8fd
    ldr r1, PTR_WIN0H_080bfc24               @ 080bfbe4 0f49
    ldr r2, DAT_080bfc28                     @ 080bfbe6 104a
    adds r0,r2,#0x0    @ 080bfbe8 101c
    strh r0,[r1,#0x0]                        @ 080bfbea 0880
    adds r1,#0x4    @ 080bfbec 0431
    movs r0,#0x90    @ 080bfbee 9020
    strh r0,[r1,#0x0]                        @ 080bfbf0 0880
    adds r1,#0x4    @ 080bfbf2 0431
    movs r0,#0x3f    @ 080bfbf4 3f20
    strh r0,[r1,#0x0]                        @ 080bfbf6 0880
    adds r1,#0x2    @ 080bfbf8 0231
    movs r0,#0x1f    @ 080bfbfa 1f20
    strh r0,[r1,#0x0]                        @ 080bfbfc 0880
    adds r1,#0x6    @ 080bfbfe 0631
    movs r0,#0xcc    @ 080bfc00 cc20
    strh r0,[r1,#0x0]                        @ 080bfc02 0880
    adds r1,#0x4    @ 080bfc04 0431
    movs r0,#0x0    @ 080bfc06 0020
    strh r0,[r1,#0x0]                        @ 080bfc08 0880
    movs r2,#0x80    @ 080bfc0a 8022
    lsls r2,r2,#0x13    @ 080bfc0c d204
    ldrh r0,[r2,#0x0]                        @ 080bfc0e 1088
    movs r3,#0x80    @ 080bfc10 8023
    lsls r3,r3,#0x6    @ 080bfc12 9b01
    adds r1,r3,#0x0    @ 080bfc14 191c
    orrs r0,r1    @ 080bfc16 0843
    b LAB_080bfdba                           @ 080bfc18 cfe0
    .zero  0x2
DAT_080bfc1c:
    .word  0x09dc8842                     @ 080bfc1c 4288dc09
DAT_080bfc20:
    .word  0x06014200                     @ 080bfc20 00420106
PTR_WIN0H_080bfc24:
    .word  WIN0H                          @ 080bfc24 40000004
DAT_080bfc28:
    .word  0x000028f0                     @ 080bfc28 f0280000
switchD_080bf82a__caseD_1:
    ldr r1, PTR_BLDY_080bfc58                @ 080bfc2c 0a49
    ldrh r2,[r4,#0x12]                       @ 080bfc2e 628a
    lsls r0,r2,#0x1    @ 080bfc30 5000
    strh r0,[r1,#0x0]                        @ 080bfc32 0880
    ldrh r0,[r4,#0x12]                       @ 080bfc34 608a
    adds r0,#0x1    @ 080bfc36 0130
    strh r0,[r4,#0x12]                       @ 080bfc38 6082
    lsls r0,r0,#0x10    @ 080bfc3a 0004
    lsrs r0,r0,#0x10    @ 080bfc3c 000c
    cmp r0,#0x4                              @ 080bfc3e 0428
    bhi LAB_080bfc44                         @ 080bfc40 00d8
    b LAB_080bfd7a                           @ 080bfc42 9ae0
LAB_080bfc44:
    movs r0,#0x1f    @ 080bfc44 1f20
    bl sync_state_and_init_sprite            @ 080bfc46 39f035ff
    movs r0,#0x0    @ 080bfc4a 0020
    strh r0,[r4,#0x12]                       @ 080bfc4c 6082
    ldrb r0,[r4,#0x10]                       @ 080bfc4e 207c
    adds r0,#0x1    @ 080bfc50 0130
    strb r0,[r4,#0x10]                       @ 080bfc52 2074
    b LAB_080bfd7a                           @ 080bfc54 91e0
    .zero  0x2
PTR_BLDY_080bfc58:
    .word  BLDY                           @ 080bfc58 54000004
switchD_080bf82a__caseD_2:
    ldr r2, DAT_080bfd10                     @ 080bfc5c 2c4a
    ldr r0,[r4,#0x18]                        @ 080bfc5e a069
    movs r1,#0x7f    @ 080bfc60 7f21
    ands r0,r1    @ 080bfc62 0840
    lsls r0,r0,#0x1    @ 080bfc64 4000
    adds r0,r0,r2    @ 080bfc66 8018
    movs r3,#0x0    @ 080bfc68 0023
    ldrsh r1,[r0,r3]                         @ 080bfc6a c15e
    lsls r0,r1,#0x2    @ 080bfc6c 8800
    adds r0,r0,r1    @ 080bfc6e 4018
    lsls r0,r0,#0x4    @ 080bfc70 0001
    cmp r0,#0x0                              @ 080bfc72 0028
    bge LAB_080bfc78                         @ 080bfc74 00da
    adds r0,#0xff    @ 080bfc76 ff30
LAB_080bfc78:
    asrs r0,r0,#0x8    @ 080bfc78 0012
    str r0,[sp,#0xc]                         @ 080bfc7a 0390
    movs r7,#0x0    @ 080bfc7c 0027
    cmp r7,r9                                @ 080bfc7e 4f45
    bge LAB_080bfd46                         @ 080bfc80 61da
    movs r0,#0x92    @ 080bfc82 9220
    lsls r0,r0,#0x2    @ 080bfc84 8000
    ldr r4,[sp,#0xc]                         @ 080bfc86 039c
    subs r4,r0,r4    @ 080bfc88 041b
    .hword 0x46a2    @ 080bfc8a a246
LAB_080bfc8c:
    .hword 0x4649    @ 080bfc8c 4946
    adds r1,#0x1    @ 080bfc8e 0131
    movs r0,#0xc8    @ 080bfc90 c820
    bl __divsi3                              @ 080bfc92 4ef0b7fc
    adds r5,r7,#0x1    @ 080bfc96 7d1c
    adds r6,r0,#0x0    @ 080bfc98 061c
    muls r6,r5    @ 080bfc9a 6e43
    adds r1,r6,#0x0    @ 080bfc9c 311c
    adds r1,#0x18    @ 080bfc9e 1831
    lsls r4,r7,#0x2    @ 080bfca0 bc00
    adds r4,r4,r7    @ 080bfca2 e419
    lsls r4,r4,#0x2    @ 080bfca4 a400
    ldr r0, DAT_080bfd14                     @ 080bfca6 1b48
    adds r4,r4,r0    @ 080bfca8 2418
    movs r0,#0x96    @ 080bfcaa 9620
    lsls r0,r0,#0x2    @ 080bfcac 8000
    ldr r2,[sp,#0xc]                         @ 080bfcae 039a
    subs r0,r0,r2    @ 080bfcb0 801a
    lsls r0,r0,#0x10    @ 080bfcb2 0004
    orrs r1,r0    @ 080bfcb4 0143
    adds r0,r4,#0x0    @ 080bfcb6 201c
    movs r2,#0x0    @ 080bfcb8 0022
    movs r3,#0x0    @ 080bfcba 0023
    bl render_aob_frame_to_oam               @ 080bfcbc 38f0a0f9
    adds r0,r4,#0x0    @ 080bfcc0 201c
    bl tick_aob_frame_counter                @ 080bfcc2 38f021f9
    .hword 0x46a8    @ 080bfcc6 a846
    cmp r0,#0x0                              @ 080bfcc8 0028
    beq LAB_080bfcd0                         @ 080bfcca 01d0
    movs r3,#0x1    @ 080bfccc 0123
    str r3,[sp,#0x8]                         @ 080bfcce 0293
LAB_080bfcd0:
    ldr r4,[sp,#0x8]                         @ 080bfcd0 029c
    cmp r4,#0x0                              @ 080bfcd2 002c
    bne LAB_080bfd40                         @ 080bfcd4 34d1
    ldr r0,[sp,#0x4]                         @ 080bfcd6 0198
    asrs r0,r7    @ 080bfcd8 3841
    movs r1,#0x1    @ 080bfcda 0121
    ands r0,r1    @ 080bfcdc 0840
    ldr r1,[sp,#0x0]                         @ 080bfcde 0099
    cmp r0,r1                                @ 080bfce0 8842
    bne LAB_080bfd18                         @ 080bfce2 19d1
    movs r5,#0x0    @ 080bfce4 0025
    .hword 0x4652    @ 080bfce6 5246
    lsls r7,r2,#0x10    @ 080bfce8 1704
    adds r4,r6,#0x0    @ 080bfcea 341c
    adds r4,#0x8    @ 080bfcec 0834
LAB_080bfcee:
    adds r0,r4,#0x0    @ 080bfcee 201c
    orrs r0,r7    @ 080bfcf0 3843
    lsls r2,r5,#0x12    @ 080bfcf2 aa04
    movs r3,#0x94    @ 080bfcf4 9423
    lsls r3,r3,#0x12    @ 080bfcf6 9b04
    adds r2,r2,r3    @ 080bfcf8 d218
    lsrs r2,r2,#0x10    @ 080bfcfa 120c
    movs r1,#0x81    @ 080bfcfc 8121
    lsls r1,r1,#0x7    @ 080bfcfe c901
    bl write_oam_entry_from_packed_args      @ 080bfd00 36f034fa
    adds r4,#0x20    @ 080bfd04 2034
    adds r5,#0x1    @ 080bfd06 0135
    cmp r5,#0x1                              @ 080bfd08 012d
    ble LAB_080bfcee                         @ 080bfd0a f0dd
    b LAB_080bfd40                           @ 080bfd0c 18e0
    .zero  0x2
DAT_080bfd10:
    .word  rom_sin_table_q8               @ 080bfd10 f0f8e509
DAT_080bfd14:
    .word  0x0201fedc                     @ 080bfd14 dcfe0102
LAB_080bfd18:
    movs r5,#0x0    @ 080bfd18 0025
    .hword 0x4654    @ 080bfd1a 5446
    lsls r7,r4,#0x10    @ 080bfd1c 2704
    adds r4,r6,#0x0    @ 080bfd1e 341c
    adds r4,#0x8    @ 080bfd20 0834
LAB_080bfd22:
    adds r0,r4,#0x0    @ 080bfd22 201c
    orrs r0,r7    @ 080bfd24 3843
    lsls r2,r5,#0x12    @ 080bfd26 aa04
    movs r1,#0x84    @ 080bfd28 8421
    lsls r1,r1,#0x12    @ 080bfd2a 8904
    adds r2,r2,r1    @ 080bfd2c 5218
    lsrs r2,r2,#0x10    @ 080bfd2e 120c
    movs r1,#0x81    @ 080bfd30 8121
    lsls r1,r1,#0x7    @ 080bfd32 c901
    bl write_oam_entry_from_packed_args      @ 080bfd34 36f01afa
    adds r4,#0x20    @ 080bfd38 2034
    adds r5,#0x1    @ 080bfd3a 0135
    cmp r5,#0x1                              @ 080bfd3c 012d
    ble LAB_080bfd22                         @ 080bfd3e f0dd
LAB_080bfd40:
    .hword 0x4647    @ 080bfd40 4746
    cmp r7,r9                                @ 080bfd42 4f45
    blt LAB_080bfc8c                         @ 080bfd44 a2db
LAB_080bfd46:
    ldr r0, DAT_080bfd54                     @ 080bfd46 0348
    ldr r1,[r0,#0x18]                        @ 080bfd48 8169
    adds r4,r0,#0x0    @ 080bfd4a 041c
    cmp r1,#0x3f                             @ 080bfd4c 3f29
    bgt LAB_080bfd58                         @ 080bfd4e 03dc
    adds r0,r1,#0x3    @ 080bfd50 c81c
    b LAB_080bfd5a                           @ 080bfd52 02e0
DAT_080bfd54:
    .word  gBannerState                   @ 080bfd54 c0fe0102
LAB_080bfd58:
    movs r0,#0x40    @ 080bfd58 4020
LAB_080bfd5a:
    str r0,[r4,#0x18]                        @ 080bfd5a a061
    ldr r2,[sp,#0x8]                         @ 080bfd5c 029a
    cmp r2,#0x0                              @ 080bfd5e 002a
    bne LAB_080bfd68                         @ 080bfd60 02d1
    ldrb r0,[r4,#0x11]                       @ 080bfd62 607c
    adds r0,#0x1    @ 080bfd64 0130
    strb r0,[r4,#0x11]                       @ 080bfd66 6074
LAB_080bfd68:
    ldrb r3,[r4,#0x11]                       @ 080bfd68 637c
    cmp r3,#0x3f                             @ 080bfd6a 3f2b
    bls LAB_080bfd74                         @ 080bfd6c 02d9
    ldrb r0,[r4,#0x10]                       @ 080bfd6e 207c
    adds r0,#0x1    @ 080bfd70 0130
    strb r0,[r4,#0x10]                       @ 080bfd72 2074
LAB_080bfd74:
    ldrb r0,[r4,#0x14]                       @ 080bfd74 207d
    adds r0,#0x1    @ 080bfd76 0130
    strb r0,[r4,#0x14]                       @ 080bfd78 2075
LAB_080bfd7a:
    movs r0,#0x1    @ 080bfd7a 0120
    b LAB_080bfdf4                           @ 080bfd7c 3ae0
switchD_080bf82a__caseD_3:
    ldr r2, PTR_BLDY_080bfda0                @ 080bfd7e 084a
    ldrh r0,[r4,#0x12]                       @ 080bfd80 608a
    lsls r1,r0,#0x1    @ 080bfd82 4100
    movs r0,#0x8    @ 080bfd84 0820
    subs r0,r0,r1    @ 080bfd86 401a
    strh r0,[r2,#0x0]                        @ 080bfd88 1080
    ldrh r0,[r4,#0x12]                       @ 080bfd8a 608a
    adds r0,#0x1    @ 080bfd8c 0130
    strh r0,[r4,#0x12]                       @ 080bfd8e 6082
    lsls r0,r0,#0x10    @ 080bfd90 0004
    lsrs r0,r0,#0x10    @ 080bfd92 000c
    cmp r0,#0x4                              @ 080bfd94 0428
    bls LAB_080bfd7a                         @ 080bfd96 f0d9
    ldrb r0,[r4,#0x10]                       @ 080bfd98 207c
    adds r0,#0x1    @ 080bfd9a 0130
    strb r0,[r4,#0x10]                       @ 080bfd9c 2074
    b LAB_080bfd7a                           @ 080bfd9e ece7
PTR_BLDY_080bfda0:
    .word  BLDY                           @ 080bfda0 54000004
switchD_080bf82a__caseD_4:
    ldr r0, DAT_080bfdc8                     @ 080bfda4 0848
    ldr r1, DAT_080bfdcc                     @ 080bfda6 0949
    movs r2,#0x80    @ 080bfda8 8022
    lsls r2,r2,#0x1    @ 080bfdaa 5200
    bl copy_bytes_by_halfword                @ 080bfdac 35f07af8
    movs r2,#0x80    @ 080bfdb0 8022
    lsls r2,r2,#0x13    @ 080bfdb2 d204
    ldrh r1,[r2,#0x0]                        @ 080bfdb4 1188
    ldr r0, DAT_080bfdd0                     @ 080bfdb6 0648
    ands r0,r1    @ 080bfdb8 0840
LAB_080bfdba:
    strh r0,[r2,#0x0]                        @ 080bfdba 1080
    ldr r1, DAT_080bfdd4                     @ 080bfdbc 0549
    ldrb r0,[r1,#0x10]                       @ 080bfdbe 087c
    adds r0,#0x1    @ 080bfdc0 0130
    strb r0,[r1,#0x10]                       @ 080bfdc2 0874
    b LAB_080bfd7a                           @ 080bfdc4 d9e7
    .zero  0x2
DAT_080bfdc8:
    .word  0x05000300                     @ 080bfdc8 00030005
DAT_080bfdcc:
    .word  0x08510460                     @ 080bfdcc 60045108
DAT_080bfdd0:
    .word  0x0000dfff                     @ 080bfdd0 ffdf0000
DAT_080bfdd4:
    .word  gBannerState                   @ 080bfdd4 c0fe0102
LAB_080bfdd8:
    movs r0,#0x2    @ 080bfdd8 0220
    rsbs r0,r0,#0    @ 080bfdda 4042
    ldrb r2,[r1,#0x0]                        @ 080bfddc 0a78
    ands r0,r2    @ 080bfdde 1040
    strb r0,[r1,#0x0]                        @ 080bfde0 0870
    ldr r1, DAT_080bfe04                     @ 080bfde2 0849
    ldr r3, DAT_080bfe08                     @ 080bfde4 084b
    adds r1,r1,r3    @ 080bfde6 c918
    movs r0,#0x5    @ 080bfde8 0520
    rsbs r0,r0,#0    @ 080bfdea 4042
    ldrb r4,[r1,#0x0]                        @ 080bfdec 0c78
    ands r0,r4    @ 080bfdee 2040
    strb r0,[r1,#0x0]                        @ 080bfdf0 0870
    movs r0,#0x0    @ 080bfdf2 0020
LAB_080bfdf4:
    add sp,#0x10                             @ 080bfdf4 04b0
    pop {r3,r4,r5}                           @ 080bfdf6 38bc
    .hword 0x4698    @ 080bfdf8 9846
    .hword 0x46a1    @ 080bfdfa a146
    .hword 0x46aa    @ 080bfdfc aa46
    pop {r4,r5,r6,r7}                        @ 080bfdfe f0bc
    pop {r1}                                 @ 080bfe00 02bc
    bx r1                                    @ 080bfe02 0847
DAT_080bfe04:
    .word  0x02023130                     @ 080bfe04 30310202
DAT_080bfe08:
    .word  0x00000215                     @ 080bfe08 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x05 子状态机, 待详细分析.
play_ui_effect_05:
    push {r4,r5,r6,lr}                       @ 080bfe0c 70b5
    ldr r5, DAT_080bfe2c                     @ 080bfe0e 074d
    ldr r6,[r5,#0x4]                         @ 080bfe10 6e68
    ldr r0, PTR_gP1LifePoints_080bfe30       @ 080bfe12 0748
    ldr r1, DAT_080bfe34                     @ 080bfe14 0749
    adds r0,r0,r1    @ 080bfe16 4018
    ldr r0,[r0,#0x0]                         @ 080bfe18 0068
    cmp r0,#0x0                              @ 080bfe1a 0028
    bne LAB_080bfe38                         @ 080bfe1c 0cd1
    movs r0,#0x2    @ 080bfe1e 0220
    rsbs r0,r0,#0    @ 080bfe20 4042
    ldrb r2,[r5,#0x0]                        @ 080bfe22 2a78
    ands r0,r2    @ 080bfe24 1040
    strb r0,[r5,#0x0]                        @ 080bfe26 2870
    b LAB_080bff0c                           @ 080bfe28 70e0
    .zero  0x2
DAT_080bfe2c:
    .word  gBannerState                   @ 080bfe2c c0fe0102
PTR_gP1LifePoints_080bfe30:
    .word  gP1LifePoints                  @ 080bfe30 e0c40102
DAT_080bfe34:
    .word  0x00001cec                     @ 080bfe34 ec1c0000
LAB_080bfe38:
    ldrb r0,[r5,#0x10]                       @ 080bfe38 287c
    cmp r0,#0x0                              @ 080bfe3a 0028
    beq LAB_080bfe60                         @ 080bfe3c 10d0
    cmp r0,#0x1                              @ 080bfe3e 0128
    beq LAB_080bfebc                         @ 080bfe40 3cd0
    ldr r3, DAT_080bfe58                     @ 080bfe42 054b
    movs r2,#0x0    @ 080bfe44 0022
    ldr r0, DAT_080bfe5c                     @ 080bfe46 0548
    ldr r0,[r0,#0x4]                         @ 080bfe48 4068
    movs r1,#0x1    @ 080bfe4a 0121
    eors r0,r1    @ 080bfe4c 4840
    cmp r6,r0                                @ 080bfe4e 8642
    bne LAB_080bfee4                         @ 080bfe50 48d1
    movs r2,#0x1    @ 080bfe52 0122
    b LAB_080bfee4                           @ 080bfe54 46e0
    .zero  0x2
DAT_080bfe58:
    .word  0x020230f8                     @ 080bfe58 f8300202
DAT_080bfe5c:
    .word  0x0201e2a0                     @ 080bfe5c a0e20102
LAB_080bfe60:
    ldr r0, DAT_080bfea8                     @ 080bfe60 1148
    ldr r1, DAT_080bfeac                     @ 080bfe62 1249
    movs r2,#0x10    @ 080bfe64 1022
    movs r3,#0x4    @ 080bfe66 0423
    bl tile_2d_row_copy                      @ 080bfe68 37f034fb
    adds r4,r5,#0x0    @ 080bfe6c 2c1c
    adds r4,#0x1c    @ 080bfe6e 1c34
    ldr r1, DAT_080bfeb0                     @ 080bfe70 0f49
    ldr r2, DAT_080bfeb4                     @ 080bfe72 104a
    adds r0,r4,#0x0    @ 080bfe74 201c
    movs r3,#0x1    @ 080bfe76 0123
    bl init_aob_ctx_from_ptnsect             @ 080bfe78 37f094ff
    movs r0,#0x1    @ 080bfe7c 0120
    ldrb r1,[r4,#0x13]                       @ 080bfe7e e17c
    orrs r0,r1    @ 080bfe80 0843
    strb r0,[r4,#0x13]                       @ 080bfe82 e074
    movs r1,#0x0    @ 080bfe84 0021
    ldr r0, DAT_080bfeb8                     @ 080bfe86 0c48
    ldr r0,[r0,#0x4]                         @ 080bfe88 4068
    cmp r6,r0                                @ 080bfe8a 8642
    bne LAB_080bfe90                         @ 080bfe8c 00d1
    movs r1,#0x1    @ 080bfe8e 0121
LAB_080bfe90:
    adds r0,r4,#0x0    @ 080bfe90 201c
    movs r2,#0x0    @ 080bfe92 0022
    bl init_aob_ctx_with_anm_entry           @ 080bfe94 37f0d8ff
    ldrb r0,[r5,#0x10]                       @ 080bfe98 287c
    adds r0,#0x1    @ 080bfe9a 0130
    strb r0,[r5,#0x10]                       @ 080bfe9c 2874
    movs r0,#0x9    @ 080bfe9e 0920
    bl sync_state_and_init_sprite            @ 080bfea0 39f008fe
LAB_080bfea4:
    movs r0,#0x1    @ 080bfea4 0120
    b LAB_080bff1e                           @ 080bfea6 3ae0
DAT_080bfea8:
    .word  0x06014000                     @ 080bfea8 00400106
DAT_080bfeac:
    .word  0x0989eda8                     @ 080bfeac a8ed8909
DAT_080bfeb0:
    .word  0x0989f5a8                     @ 080bfeb0 a8f58909
DAT_080bfeb4:
    .word  0x02000002                     @ 080bfeb4 02000002
DAT_080bfeb8:
    .word  0x0201e2a0                     @ 080bfeb8 a0e20102
LAB_080bfebc:
    adds r4,r5,#0x0    @ 080bfebc 2c1c
    adds r4,#0x1c    @ 080bfebe 1c34
    ldr r1, DAT_080bfee0                     @ 080bfec0 0749
    adds r0,r4,#0x0    @ 080bfec2 201c
    movs r2,#0x0    @ 080bfec4 0022
    movs r3,#0x0    @ 080bfec6 0023
    bl render_aob_frame_to_oam               @ 080bfec8 38f09af8
    adds r0,r4,#0x0    @ 080bfecc 201c
    bl tick_aob_frame_counter                @ 080bfece 38f01bf8
    cmp r0,#0x0                              @ 080bfed2 0028
    bne LAB_080bfea4                         @ 080bfed4 e6d1
    ldrb r0,[r5,#0x10]                       @ 080bfed6 287c
    adds r0,#0x1    @ 080bfed8 0130
    strb r0,[r5,#0x10]                       @ 080bfeda 2874
    b LAB_080bfea4                           @ 080bfedc e2e7
    .zero  0x2
DAT_080bfee0:
    .word  0x0038007c                     @ 080bfee0 7c003800
LAB_080bfee4:
    adds r0,r3,#0x0    @ 080bfee4 181c
    adds r1,r2,#0x0    @ 080bfee6 111c
    movs r2,#0x1    @ 080bfee8 0122
    bl init_aob_ctx_with_anm_entry           @ 080bfeea 37f0adff
    ldr r1, PTR_gPrng_080bff24               @ 080bfeee 0d49
    movs r2,#0x85    @ 080bfef0 8522
    lsls r2,r2,#0x2    @ 080bfef2 9200
    adds r1,r1,r2    @ 080bfef4 8918
    ldr r0,[r1,#0x0]                         @ 080bfef6 0868
    movs r2,#0x80    @ 080bfef8 8022
    lsls r2,r2,#0x18    @ 080bfefa 1206
    ands r0,r2    @ 080bfefc 1040
    str r0,[r1,#0x0]                         @ 080bfefe 0860
    ldr r1, DAT_080bff28                     @ 080bff00 0949
    movs r0,#0x2    @ 080bff02 0220
    rsbs r0,r0,#0    @ 080bff04 4042
    ldrb r2,[r1,#0x0]                        @ 080bff06 0a78
    ands r0,r2    @ 080bff08 1040
    strb r0,[r1,#0x0]                        @ 080bff0a 0870
LAB_080bff0c:
    ldr r1, DAT_080bff2c                     @ 080bff0c 0749
    ldr r0, DAT_080bff30                     @ 080bff0e 0848
    adds r1,r1,r0    @ 080bff10 0918
    movs r0,#0x5    @ 080bff12 0520
    rsbs r0,r0,#0    @ 080bff14 4042
    ldrb r2,[r1,#0x0]                        @ 080bff16 0a78
    ands r0,r2    @ 080bff18 1040
    strb r0,[r1,#0x0]                        @ 080bff1a 0870
    movs r0,#0x0    @ 080bff1c 0020
LAB_080bff1e:
    pop {r4,r5,r6}                           @ 080bff1e 70bc
    pop {r1}                                 @ 080bff20 02bc
    bx r1                                    @ 080bff22 0847
PTR_gPrng_080bff24:
    .word  gPrng                          @ 080bff24 40000003
DAT_080bff28:
    .word  gBannerState                   @ 080bff28 c0fe0102
DAT_080bff2c:
    .word  0x02023130                     @ 080bff2c 30310202
DAT_080bff30:
    .word  0x00000215                     @ 080bff30 15020000

@ 将 r0 (nibble_packed, u16, 含 4 个 nibble 调色板索引) 的每个 nibble 加上 r1 (palette_offset, u8) 后截断至 nibble, 重新打包为 16 位输出. 由 render_card_image_to_vram 4 次调用, 用于卡图调色板索引批量偏移. 纯叶子函数, 无外部副作用. Constants: NIBBLE_MASK=0x0f0f, UPPER_NIBBLE_MASK=0xf0.
repack_nibbles_with_palette_offset:
    push {r4,lr}                             @ 080bff34 10b5
    adds r4,r0,#0x0    @ 080bff36 041c
    lsls r4,r4,#0x10    @ 080bff38 2404
    lsrs r4,r4,#0x10    @ 080bff3a 240c
    lsls r1,r1,#0x18    @ 080bff3c 0906
    lsrs r1,r1,#0x18    @ 080bff3e 090e
    movs r2,#0xf0    @ 080bff40 f022
    ands r2,r4    @ 080bff42 2240
    lsrs r2,r2,#0x4    @ 080bff44 1209
    lsrs r3,r4,#0xc    @ 080bff46 230b
    adds r2,r2,r1    @ 080bff48 5218
    lsls r2,r2,#0x18    @ 080bff4a 1206
    adds r3,r3,r1    @ 080bff4c 5b18
    lsls r3,r3,#0x18    @ 080bff4e 1b06
    ldr r0, DAT_080bff68                     @ 080bff50 0548
    ands r0,r4    @ 080bff52 2040
    lsrs r2,r2,#0x14    @ 080bff54 120d
    orrs r0,r2    @ 080bff56 1043
    lsrs r3,r3,#0xc    @ 080bff58 1b0b
    orrs r0,r3    @ 080bff5a 1843
    lsls r0,r0,#0x10    @ 080bff5c 0004
    lsrs r0,r0,#0x10    @ 080bff5e 000c
    pop {r4}                                 @ 080bff60 10bc
    pop {r1}                                 @ 080bff62 02bc
    bx r1                                    @ 080bff64 0847
    .zero  0x2
DAT_080bff68:
    .word  0x00000f0f                     @ 080bff68 0f0f0000

@ 从 ROM 卡图数据表按 card_idx (r0) 和 VRAM 目标槽位 (r1) 加载卡图 tile 和调色板到 VRAM. 4 次调用 repack_nibbles_with_palette_offset 转换调色板索引后写入 PAL RAM (0x05000200), 再将 tile 数据复制到 BG VRAM (0x060148c0 + slot_offset); 外层循环 11 行 x 0x4f halfword. 唯一调用方: FUN_080c05b4. Constants: VRAM_CARD_TILE_BASE=0x060148c0, PAL_RAM_BASE=0x05000200, TILE_ROW_HALFWORDS=0x4f, OUTER_LOOP_COUNT=0xa.
render_card_image_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 080bff6c f0b5
    .hword 0x4657    @ 080bff6e 5746
    .hword 0x464e    @ 080bff70 4e46
    .hword 0x4645    @ 080bff72 4546
    push {r5,r6,r7}                          @ 080bff74 e0b4
    sub sp,#0xc                              @ 080bff76 83b0
    lsls r0,r0,#0x10    @ 080bff78 0004
    lsrs r4,r0,#0x10    @ 080bff7a 040c
    lsls r1,r1,#0x10    @ 080bff7c 0904
    lsrs r1,r1,#0x10    @ 080bff7e 090c
    str r1,[sp,#0x0]                         @ 080bff80 0091
    lsls r2,r2,#0x10    @ 080bff82 1204
    lsrs r6,r2,#0x10    @ 080bff84 160c
    ldr r5, PTR_card_image_index_080c00cc    @ 080bff86 514d
    lsls r2,r4,#0x1    @ 080bff88 6200
    movs r3,#0x0    @ 080bff8a 0023
    ldr r0, DAT_080c00d0                     @ 080bff8c 5048
    ldrh r0,[r0,#0x0]                        @ 080bff8e 0088
    lsrs r0,r0,#0x8    @ 080bff90 000a
    .hword 0x46a8    @ 080bff92 a846
    cmp r0,#0x4a                             @ 080bff94 4a28
    bne LAB_080bffa8                         @ 080bff96 07d1
    ldr r1, DAT_080c00d4                     @ 080bff98 4e49
    ldr r0, DAT_080c00d8                     @ 080bff9a 4f48
    adds r1,r1,r0    @ 080bff9c 0918
    movs r0,#0x7    @ 080bff9e 0720
    ldrb r1,[r1,#0x0]                        @ 080bffa0 0978
    ands r0,r1    @ 080bffa2 0840
    cmp r0,#0x0                              @ 080bffa4 0028
    beq LAB_080bffaa                         @ 080bffa6 00d0
LAB_080bffa8:
    movs r3,#0x1    @ 080bffa8 0123
LAB_080bffaa:
    orrs r2,r3    @ 080bffaa 1a43
    lsls r0,r2,#0x1    @ 080bffac 5000
    adds r0,r5,r0    @ 080bffae 2818
    ldrh r2,[r0,#0x0]                        @ 080bffb0 0288
    lsls r1,r2,#0x2    @ 080bffb2 9100
    adds r1,r1,r2    @ 080bffb4 8918
    lsls r0,r1,#0x4    @ 080bffb6 0801
    subs r0,r0,r1    @ 080bffb8 401a
    lsls r0,r0,#0x6    @ 080bffba 8001
    ldr r1, PTR_card_image_tiles_080c00dc    @ 080bffbc 4749
    adds r7,r0,r1    @ 080bffbe 4718
    ldr r0, DAT_080c00e0                     @ 080bffc0 4748
    .hword 0x4681    @ 080bffc2 8146
    lsls r0,r6,#0x5    @ 080bffc4 7001
    ldr r1, DAT_080c00e4                     @ 080bffc6 4749
    adds r5,r0,r1    @ 080bffc8 4518
    lsls r2,r4,#0x1    @ 080bffca 6200
    movs r3,#0x0    @ 080bffcc 0023
    ldr r0, DAT_080c00d0                     @ 080bffce 4048
    ldrh r0,[r0,#0x0]                        @ 080bffd0 0088
    lsrs r0,r0,#0x8    @ 080bffd2 000a
    cmp r0,#0x4a                             @ 080bffd4 4a28
    bne LAB_080bffe8                         @ 080bffd6 07d1
    ldr r1, DAT_080c00d4                     @ 080bffd8 3e49
    ldr r0, DAT_080c00d8                     @ 080bffda 3f48
    adds r1,r1,r0    @ 080bffdc 0918
    movs r0,#0x7    @ 080bffde 0720
    ldrb r1,[r1,#0x0]                        @ 080bffe0 0978
    ands r0,r1    @ 080bffe2 0840
    cmp r0,#0x0                              @ 080bffe4 0028
    beq LAB_080bffea                         @ 080bffe6 00d0
LAB_080bffe8:
    movs r3,#0x1    @ 080bffe8 0123
LAB_080bffea:
    orrs r2,r3    @ 080bffea 1a43
    lsls r0,r2,#0x1    @ 080bffec 5000
    add r0,r8                                @ 080bffee 4044
    ldrh r0,[r0,#0x0]                        @ 080bfff0 0088
    lsls r1,r0,#0x7    @ 080bfff2 c101
    ldr r0, PTR_card_image_palettes_080c00e8 @ 080bfff4 3c48
    adds r1,r1,r0    @ 080bfff6 0918
    adds r0,r5,#0x0    @ 080bfff8 281c
    movs r2,#0x80    @ 080bfffa 8022
    bl copy_bytes_by_halfword                @ 080bfffc 34f052ff
    movs r3,#0x1    @ 080c0000 0123
    lsls r0,r6,#0x18    @ 080c0002 3006
    lsrs r0,r0,#0x18    @ 080c0004 000e
    .hword 0x4680    @ 080c0006 8046
LAB_080c0008:
    lsls r1,r3,#0x5    @ 080c0008 5901
    str r1,[sp,#0x8]                         @ 080c000a 0291
    adds r3,#0x1    @ 080c000c 0133
    str r3,[sp,#0x4]                         @ 080c000e 0193
    movs r2,#0x4f    @ 080c0010 4f22
    .hword 0x4692    @ 080c0012 9246
LAB_080c0014:
    ldrh r5,[r7,#0x0]                        @ 080c0014 3d88
    ldrh r4,[r7,#0x2]                        @ 080c0016 7c88
    ldrh r6,[r7,#0x4]                        @ 080c0018 be88
    adds r0,r5,#0x0    @ 080c001a 281c
    movs r1,#0x3f    @ 080c001c 3f21
    ands r0,r1    @ 080c001e 0840
    adds r1,r5,#0x0    @ 080c0020 291c
    movs r2,#0xfc    @ 080c0022 fc22
    lsls r2,r2,#0x4    @ 080c0024 1201
    ands r1,r2    @ 080c0026 1140
    lsls r1,r1,#0x2    @ 080c0028 8900
    orrs r0,r1    @ 080c002a 0843
    .hword 0x4641    @ 080c002c 4146
    bl repack_nibbles_with_palette_offset    @ 080c002e fff781ff
    .hword 0x4649    @ 080c0032 4946
    strh r0,[r1,#0x0]                        @ 080c0034 0880
    lsrs r5,r5,#0xc    @ 080c0036 2d0b
    movs r1,#0x3    @ 080c0038 0321
    adds r0,r4,#0x0    @ 080c003a 201c
    ands r0,r1    @ 080c003c 0840
    lsls r0,r0,#0x4    @ 080c003e 0001
    orrs r5,r0    @ 080c0040 0543
    movs r0,#0xfc    @ 080c0042 fc20
    ands r0,r4    @ 080c0044 2040
    lsls r0,r0,#0x6    @ 080c0046 8001
    orrs r5,r0    @ 080c0048 0543
    adds r0,r5,#0x0    @ 080c004a 281c
    .hword 0x4641    @ 080c004c 4146
    bl repack_nibbles_with_palette_offset    @ 080c004e fff771ff
    .hword 0x464a    @ 080c0052 4a46
    strh r0,[r2,#0x2]                        @ 080c0054 5080
    lsrs r4,r4,#0x8    @ 080c0056 240a
    adds r0,r4,#0x0    @ 080c0058 201c
    movs r1,#0x3f    @ 080c005a 3f21
    ands r0,r1    @ 080c005c 0840
    lsrs r4,r4,#0x6    @ 080c005e a409
    movs r2,#0xf    @ 080c0060 0f22
    adds r1,r6,#0x0    @ 080c0062 311c
    ands r1,r2    @ 080c0064 1140
    lsls r1,r1,#0x2    @ 080c0066 8900
    orrs r4,r1    @ 080c0068 0c43
    lsls r4,r4,#0x8    @ 080c006a 2402
    orrs r0,r4    @ 080c006c 2043
    .hword 0x4641    @ 080c006e 4146
    bl repack_nibbles_with_palette_offset    @ 080c0070 fff760ff
    .hword 0x464a    @ 080c0074 4a46
    strh r0,[r2,#0x4]                        @ 080c0076 9080
    lsrs r6,r6,#0x4    @ 080c0078 3609
    adds r0,r6,#0x0    @ 080c007a 301c
    movs r1,#0x3f    @ 080c007c 3f21
    ands r0,r1    @ 080c007e 0840
    movs r2,#0xfc    @ 080c0080 fc22
    lsls r2,r2,#0x4    @ 080c0082 1201
    ands r6,r2    @ 080c0084 1640
    lsls r6,r6,#0x2    @ 080c0086 b600
    orrs r0,r6    @ 080c0088 3043
    .hword 0x4641    @ 080c008a 4146
    bl repack_nibbles_with_palette_offset    @ 080c008c fff752ff
    .hword 0x4649    @ 080c0090 4946
    strh r0,[r1,#0x6]                        @ 080c0092 c880
    adds r7,#0x6    @ 080c0094 0637
    movs r2,#0x8    @ 080c0096 0822
    add r9,r2                                @ 080c0098 9144
    movs r0,#0x1    @ 080c009a 0120
    rsbs r0,r0,#0    @ 080c009c 4042
    add r10,r0                               @ 080c009e 8244
    .hword 0x4651    @ 080c00a0 5146
    cmp r1,#0x0                              @ 080c00a2 0029
    bge LAB_080c0014                         @ 080c00a4 b6da
    ldr r2,[sp,#0x0]                         @ 080c00a6 009a
    ldr r1,[sp,#0x8]                         @ 080c00a8 0299
    adds r0,r2,r1    @ 080c00aa 5018
    lsls r0,r0,#0x5    @ 080c00ac 4001
    ldr r2, DAT_080c00ec                     @ 080c00ae 0f4a
    adds r2,r2,r0    @ 080c00b0 1218
    .hword 0x4691    @ 080c00b2 9146
    ldr r3,[sp,#0x4]                         @ 080c00b4 019b
    cmp r3,#0xa                              @ 080c00b6 0a2b
    ble LAB_080c0008                         @ 080c00b8 a6dd
    add sp,#0xc                              @ 080c00ba 03b0
    pop {r3,r4,r5}                           @ 080c00bc 38bc
    .hword 0x4698    @ 080c00be 9846
    .hword 0x46a1    @ 080c00c0 a146
    .hword 0x46aa    @ 080c00c2 aa46
    pop {r4,r5,r6,r7}                        @ 080c00c4 f0bc
    pop {r0}                                 @ 080c00c6 01bc
    bx r0                                    @ 080c00c8 0047
    .zero  0x2
PTR_card_image_index_080c00cc:
    .word  card_image_index               @ 080c00cc 005c5b09
DAT_080c00d0:
    .word  0x080000ae                     @ 080c00d0 ae000008
DAT_080c00d4:
    .word  0x02000000                     @ 080c00d4 00000002
DAT_080c00d8:
    .word  0x00006c2c                     @ 080c00d8 2c6c0000
PTR_card_image_tiles_080c00dc:
    .word  card_image_tiles               @ 080c00dc 40065108
DAT_080c00e0:
    .word  0x060148c0                     @ 080c00e0 c0480106
DAT_080c00e4:
    .word  0x05000200                     @ 080c00e4 00020005
PTR_card_image_palettes_080c00e8:
    .word  card_image_palettes            @ 080c00e8 c0764c08
DAT_080c00ec:
    .word  0x06010000                     @ 080c00ec 00000106

@ 渲染卡牌名称到 BG tile VRAM. 唯一调用方: FUN_080c05b4 (card image 显示页 hub). 调用 init_line_buf_with_jp_font_flag (r0=0xe, r1=2) 建立 JP 字体上下文, 读 EWRAM 字体方向标志选择字体基址, 调用 render_card_name_to_line_buf (card_idx) 渲染到 line buffer, 检查 card_stats_table type 字段 (offset 6, 与 0x16 比较) 选择竖排/横排字体映射表, 最后调用 write_line_buf_to_bg_tile_vram 写入 VRAM. Constants: CARD_STATS_TYPE_FIELD=6, CARD_TYPE_VERTICAL_LIMIT=0x16.
draw_card_name_to_bg_tile_vram:
    push {r4,lr}                             @ 080c00f0 10b5
    adds r4,r0,#0x0    @ 080c00f2 041c
    lsls r4,r4,#0x10    @ 080c00f4 2404
    lsrs r4,r4,#0x10    @ 080c00f6 240c
    movs r0,#0xe    @ 080c00f8 0e20
    movs r1,#0x2    @ 080c00fa 0221
    bl init_line_buf_with_jp_font_flag       @ 080c00fc 30f05afe
    ldr r2, DAT_080c0160                     @ 080c0100 174a
    ldr r0, DAT_080c0164                     @ 080c0102 1848
    ldr r1, DAT_080c0168                     @ 080c0104 1849
    adds r0,r0,r1    @ 080c0106 4018
    movs r1,#0x7    @ 080c0108 0721
    ldrb r0,[r0,#0x0]                        @ 080c010a 0078
    ands r1,r0    @ 080c010c 0140
    rsbs r1,r1,#0    @ 080c010e 4942
    lsrs r1,r1,#0x1f    @ 080c0110 c90f
    movs r0,#0x2    @ 080c0112 0220
    rsbs r0,r0,#0    @ 080c0114 4042
    ldrb r3,[r2,#0x8]                        @ 080c0116 137a
    ands r0,r3    @ 080c0118 1840
    orrs r0,r1    @ 080c011a 0843
    movs r1,#0x2    @ 080c011c 0221
    orrs r0,r1    @ 080c011e 0843
    strb r0,[r2,#0x8]                        @ 080c0120 1072
    ldr r3, PTR_font_jp_base_table_080c016c  @ 080c0122 124b
    lsls r1,r0,#0x1e    @ 080c0124 8107
    lsrs r1,r1,#0x1f    @ 080c0126 c90f
    lsls r1,r1,#0x2    @ 080c0128 8900
    lsls r0,r0,#0x1f    @ 080c012a c007
    lsrs r0,r0,#0x1f    @ 080c012c c00f
    lsls r0,r0,#0x3    @ 080c012e c000
    adds r1,r1,r0    @ 080c0130 0918
    adds r1,r1,r3    @ 080c0132 c918
    ldr r0,[r1,#0x0]                         @ 080c0134 0868
    str r0,[r2,#0x4]                         @ 080c0136 5060
    adds r0,r4,#0x0    @ 080c0138 201c
    bl render_card_name_to_line_buf          @ 080c013a 5df7e9f9
    ldr r1, PTR_card_stats_table_080c0170    @ 080c013e 0c49
    movs r0,#0xb    @ 080c0140 0b20
    muls r0,r4    @ 080c0142 6043
    adds r0,#0x6    @ 080c0144 0630
    lsls r0,r0,#0x1    @ 080c0146 4000
    adds r0,r0,r1    @ 080c0148 4018
    ldr r1, DAT_080c0174                     @ 080c014a 0a49
    ldrh r0,[r0,#0x0]                        @ 080c014c 0088
    cmp r0,#0x16                             @ 080c014e 1628
    bhi LAB_080c0154                         @ 080c0150 00d8
    ldr r1, DAT_080c0178                     @ 080c0152 0949
LAB_080c0154:
    ldr r0, DAT_080c017c                     @ 080c0154 0948
    bl write_line_buf_to_bg_tile_vram        @ 080c0156 33f03dfb
    pop {r4}                                 @ 080c015a 10bc
    pop {r0}                                 @ 080c015c 01bc
    bx r0                                    @ 080c015e 0047
DAT_080c0160:
    .word  0x02006ed0                     @ 080c0160 d06e0002
DAT_080c0164:
    .word  0x02000000                     @ 080c0164 00000002
DAT_080c0168:
    .word  0x00006c2c                     @ 080c0168 2c6c0000
PTR_font_jp_base_table_080c016c:
    .word  font_jp_base_table             @ 080c016c 54f8e509
PTR_card_stats_table_080c0170:
    .word  card_stats_table               @ 080c0170 b8698109
DAT_080c0174:
    .word  0x00000707                     @ 080c0174 07070000
DAT_080c0178:
    .word  0x00000808                     @ 080c0178 08080000
DAT_080c017c:
    .word  0x06013c40                     @ 080c017c 403c0106

@ 从 card_stats_table 按 card_idx (r0) 读取 ATK (offset 3) / DEF (offset 4), 调用 init_line_buf_with_jp_font_flag (r0=0xe, r1=2) 建立 JP 字体上下文, 检查 ATK 有效性后选择渲染路径: 等级文字 (lookup_level_glyph_index + render_card_level_text_to_buf) 或 ATK/DEF 数字 (render_atk_def_digits_to_buf), 最后调用 write_line_buf_to_bg_tile_vram 写入 BG tile VRAM. 唯一调用方: FUN_080c05b4 (card image 显示页 hub). Constants: CARD_STATS_FIELD_ATK=3, CARD_STATS_FIELD_DEF=4, INVALID_STAT_SENTINEL=0xffff, ENTRY_STRIDE=0xb.
draw_card_atkdef_label_to_vram:
    push {r4,r5,r6,lr}                       @ 080c0180 70b5
    lsls r0,r0,#0x10    @ 080c0182 0004
    lsrs r4,r0,#0x10    @ 080c0184 040c
    ldr r3, PTR_card_stats_table_080c01dc    @ 080c0186 154b
    movs r0,#0xb    @ 080c0188 0b20
    adds r1,r4,#0x0    @ 080c018a 211c
    muls r1,r0    @ 080c018c 4143
    adds r0,r1,#0x3    @ 080c018e c81c
    lsls r0,r0,#0x1    @ 080c0190 4000
    adds r0,r0,r3    @ 080c0192 c018
    ldr r2, DAT_080c01e0                     @ 080c0194 124a
    movs r6,#0x0    @ 080c0196 0026
    ldrh r5,[r0,#0x0]                        @ 080c0198 0588
    cmp r5,r2                                @ 080c019a 9542
    beq LAB_080c01a0                         @ 080c019c 00d0
    ldrh r6,[r0,#0x0]                        @ 080c019e 0688
LAB_080c01a0:
    adds r0,r1,#0x4    @ 080c01a0 081d
    lsls r0,r0,#0x1    @ 080c01a2 4000
    adds r0,r0,r3    @ 080c01a4 c018
    movs r5,#0x0    @ 080c01a6 0025
    ldrh r1,[r0,#0x0]                        @ 080c01a8 0188
    cmp r1,r2                                @ 080c01aa 9142
    beq LAB_080c01b0                         @ 080c01ac 00d0
    ldrh r5,[r0,#0x0]                        @ 080c01ae 0588
LAB_080c01b0:
    movs r0,#0xe    @ 080c01b0 0e20
    movs r1,#0x2    @ 080c01b2 0221
    bl init_line_buf_with_jp_font_flag       @ 080c01b4 30f0fefd
    adds r0,r4,#0x0    @ 080c01b8 201c
    bl check_card_atk_in_valid_range         @ 080c01ba 2ff0fff8
    cmp r0,#0x0                              @ 080c01be 0028
    beq LAB_080c01e4                         @ 080c01c0 10d0
    adds r0,r4,#0x0    @ 080c01c2 201c
    bl lookup_level_glyph_index              @ 080c01c4 2ff046f9
    movs r1,#0x1    @ 080c01c8 0121
    rsbs r1,r1,#0    @ 080c01ca 4942
    cmp r0,r1                                @ 080c01cc 8842
    beq LAB_080c01ec                         @ 080c01ce 0dd0
    adds r0,r4,#0x0    @ 080c01d0 201c
    bl lookup_level_glyph_index              @ 080c01d2 2ff03ff9
    bl render_card_level_text_to_buf         @ 080c01d6 5df72bfb
    b LAB_080c01ec                           @ 080c01da 07e0
PTR_card_stats_table_080c01dc:
    .word  card_stats_table               @ 080c01dc b8698109
DAT_080c01e0:
    .word  0x0000ffff                     @ 080c01e0 ffff0000
LAB_080c01e4:
    adds r0,r6,#0x0    @ 080c01e4 301c
    adds r1,r5,#0x0    @ 080c01e6 291c
    bl render_atk_def_digits_to_buf          @ 080c01e8 5df790fa
LAB_080c01ec:
    ldr r0, DAT_080c01fc                     @ 080c01ec 0348
    ldr r1, DAT_080c0200                     @ 080c01ee 0449
    bl write_line_buf_to_bg_tile_vram        @ 080c01f0 33f0f0fa
    pop {r4,r5,r6}                           @ 080c01f4 70bc
    pop {r0}                                 @ 080c01f6 01bc
    bx r0                                    @ 080c01f8 0047
    .zero  0x2
DAT_080c01fc:
    .word  0x06017840                     @ 080c01fc 40780106
DAT_080c0200:
    .word  0x00000808                     @ 080c0200 08080000

@ 在 BG tile VRAM 指定二维坐标 (tile_x=r0, tile_y=r1) 写入单个 nibble (r2=palette_nibble, r3=vram_row_base). 将坐标转换为 VRAM halfword 地址 (VRAM_BASE=0x06010000, 行步进 0x400 halfword), 根据 tile_y 奇偶确定写高/低 nibble, 修改 halfword 后写回. 被 write_nibble_sequence_to_bg_tiles 两次调用. Constants: VRAM_BG_TILE_BASE=0x06010000, TILE_ROW_STRIDE=0x400, NIBBLE_HIGH_MASK=0xff00, NIBBLE_LOW_MASK=0x00ff.
write_nibble_to_bg_tile_cell:
    push {r4,r5,r6,lr}                       @ 080c0204 70b5
    adds r5,r0,#0x0    @ 080c0206 051c
    adds r4,r1,#0x0    @ 080c0208 0c1c
    lsls r2,r2,#0x18    @ 080c020a 1206
    lsrs r2,r2,#0x18    @ 080c020c 120e
    adds r6,r2,#0x0    @ 080c020e 161c
    lsls r3,r3,#0x10    @ 080c0210 1b04
    lsrs r3,r3,#0xb    @ 080c0212 db0a
    ldr r0, DAT_080c025c                     @ 080c0214 1148
    adds r3,r3,r0    @ 080c0216 1b18
    adds r0,r4,#0x0    @ 080c0218 201c
    cmp r4,#0x0                              @ 080c021a 002c
    bge LAB_080c0220                         @ 080c021c 00da
    adds r0,r4,#0x7    @ 080c021e e01d
LAB_080c0220:
    asrs r0,r0,#0x3    @ 080c0220 c010
    lsls r1,r0,#0xa    @ 080c0222 8102
    adds r3,r3,r1    @ 080c0224 5b18
    lsls r0,r0,#0x3    @ 080c0226 c000
    subs r0,r4,r0    @ 080c0228 201a
    lsls r0,r0,#0x3    @ 080c022a c000
    adds r3,r3,r0    @ 080c022c 1b18
    adds r1,r5,#0x0    @ 080c022e 291c
    cmp r5,#0x0                              @ 080c0230 002d
    bge LAB_080c0236                         @ 080c0232 00da
    adds r1,r5,#0x7    @ 080c0234 e91d
LAB_080c0236:
    asrs r1,r1,#0x3    @ 080c0236 c910
    lsls r0,r1,#0x6    @ 080c0238 8801
    adds r3,r3,r0    @ 080c023a 1b18
    lsrs r0,r5,#0x1f    @ 080c023c e80f
    adds r0,r5,r0    @ 080c023e 2818
    asrs r0,r0,#0x1    @ 080c0240 4010
    lsls r1,r1,#0x2    @ 080c0242 8900
    subs r0,r0,r1    @ 080c0244 401a
    lsls r0,r0,#0x1    @ 080c0246 4000
    adds r3,r3,r0    @ 080c0248 1b18
    movs r0,#0x1    @ 080c024a 0120
    ands r0,r5    @ 080c024c 2840
    cmp r0,#0x0                              @ 080c024e 0028
    beq LAB_080c0260                         @ 080c0250 06d0
    lsls r0,r2,#0x8    @ 080c0252 1002
    ldrb r1,[r3,#0x0]                        @ 080c0254 1978
    orrs r0,r1    @ 080c0256 0843
    b LAB_080c026a                           @ 080c0258 07e0
    .zero  0x2
DAT_080c025c:
    .word  0x06010000                     @ 080c025c 00000106
LAB_080c0260:
    movs r0,#0xff    @ 080c0260 ff20
    lsls r0,r0,#0x8    @ 080c0262 0002
    ldrh r1,[r3,#0x0]                        @ 080c0264 1988
    ands r0,r1    @ 080c0266 0840
    orrs r0,r6    @ 080c0268 3043
LAB_080c026a:
    strh r0,[r3,#0x0]                        @ 080c026a 1880
    pop {r4,r5,r6}                           @ 080c026c 70bc
    pop {r0}                                 @ 080c026e 01bc
    bx r0                                    @ 080c0270 0047
    .zero  0x2

@ 从 packed nibble 字节数组 (r2) 中逐字节读取双 nibble, 对每个非零 nibble 调用 write_nibble_to_bg_tile_cell 写入对应 BG tile VRAM 坐标. 外层循环 8 槽 (r7: 0..7), 内层循环 nibble 序列 (r8, 步进 -1), 坐标由 r0 (packed: lo16=tile_x_even [6..80], hi16=inner_row_base [5..6]) 和 r1 (vram_row_param) 驱动. 被 FUN_080c0310 和 FUN_080c05b4 调用. Constants: OUTER_LOOP_COUNT=8, NIBBLE_LOW_MASK=0x0f, NIBBLE_HIGH_MASK=0xf0.
write_nibble_sequence_to_bg_tiles:
    push {r4,r5,r6,r7,lr}                    @ 080c0274 f0b5
    .hword 0x4657    @ 080c0276 5746
    .hword 0x464e    @ 080c0278 4e46
    .hword 0x4645    @ 080c027a 4546
    push {r5,r6,r7}                          @ 080c027c e0b4
    sub sp,#0xc                              @ 080c027e 83b0
    adds r6,r2,#0x0    @ 080c0280 161c
    lsls r1,r1,#0x10    @ 080c0282 0904
    lsrs r1,r1,#0x10    @ 080c0284 090c
    str r1,[sp,#0x0]                         @ 080c0286 0091
    lsls r3,r3,#0x18    @ 080c0288 1b06
    lsls r1,r0,#0x10    @ 080c028a 0104
    lsrs r1,r1,#0x10    @ 080c028c 090c
    str r1,[sp,#0x4]                         @ 080c028e 0191
    lsrs r0,r0,#0x10    @ 080c0290 000c
    .hword 0x4682    @ 080c0292 8246
    movs r7,#0x0    @ 080c0294 0027
    lsrs r3,r3,#0x14    @ 080c0296 1b0d
    .hword 0x4699    @ 080c0298 9946
LAB_080c029a:
    adds r0,r7,#0x1    @ 080c029a 781c
    str r0,[sp,#0x8]                         @ 080c029c 0290
    ldr r5,[sp,#0x4]                         @ 080c029e 019d
    adds r5,#0x1    @ 080c02a0 0135
    ldr r4,[sp,#0x4]                         @ 080c02a2 019c
    movs r1,#0x3    @ 080c02a4 0321
    .hword 0x4688    @ 080c02a6 8846
LAB_080c02a8:
    movs r0,#0xf    @ 080c02a8 0f20
    ldrb r3,[r6,#0x0]                        @ 080c02aa 3378
    ands r0,r3    @ 080c02ac 1840
    cmp r0,#0x0                              @ 080c02ae 0028
    beq LAB_080c02c6                         @ 080c02b0 09d0
    .hword 0x4649    @ 080c02b2 4946
    orrs r0,r1    @ 080c02b4 0843
    lsls r0,r0,#0x18    @ 080c02b6 0006
    lsrs r2,r0,#0x18    @ 080c02b8 020e
    adds r0,r4,#0x0    @ 080c02ba 201c
    .hword 0x4653    @ 080c02bc 5346
    adds r1,r3,r7    @ 080c02be d919
    ldr r3,[sp,#0x0]                         @ 080c02c0 009b
    bl write_nibble_to_bg_tile_cell          @ 080c02c2 fff79fff
LAB_080c02c6:
    movs r0,#0xf0    @ 080c02c6 f020
    ldrb r1,[r6,#0x0]                        @ 080c02c8 3178
    ands r0,r1    @ 080c02ca 0840
    lsls r0,r0,#0x18    @ 080c02cc 0006
    cmp r0,#0x0                              @ 080c02ce 0028
    beq LAB_080c02e8                         @ 080c02d0 0ad0
    lsrs r0,r0,#0x1c    @ 080c02d2 000f
    .hword 0x464b    @ 080c02d4 4b46
    orrs r0,r3    @ 080c02d6 1843
    lsls r0,r0,#0x18    @ 080c02d8 0006
    lsrs r2,r0,#0x18    @ 080c02da 020e
    adds r0,r5,#0x0    @ 080c02dc 281c
    .hword 0x4653    @ 080c02de 5346
    adds r1,r3,r7    @ 080c02e0 d919
    ldr r3,[sp,#0x0]                         @ 080c02e2 009b
    bl write_nibble_to_bg_tile_cell          @ 080c02e4 fff78eff
LAB_080c02e8:
    adds r6,#0x1    @ 080c02e8 0136
    adds r5,#0x2    @ 080c02ea 0235
    adds r4,#0x2    @ 080c02ec 0234
    movs r0,#0x1    @ 080c02ee 0120
    rsbs r0,r0,#0    @ 080c02f0 4042
    add r8,r0                                @ 080c02f2 8044
    .hword 0x4641    @ 080c02f4 4146
    cmp r1,#0x0                              @ 080c02f6 0029
    bge LAB_080c02a8                         @ 080c02f8 d6da
    ldr r7,[sp,#0x8]                         @ 080c02fa 029f
    cmp r7,#0x7                              @ 080c02fc 072f
    ble LAB_080c029a                         @ 080c02fe ccdd
    add sp,#0xc                              @ 080c0300 03b0
    pop {r3,r4,r5}                           @ 080c0302 38bc
    .hword 0x4698    @ 080c0304 9846
    .hword 0x46a1    @ 080c0306 a146
    .hword 0x46aa    @ 080c0308 aa46
    pop {r4,r5,r6,r7}                        @ 080c030a f0bc
    pop {r0}                                 @ 080c030c 01bc
    bx r0                                    @ 080c030e 0047

@ BG tile VRAM nibble dual-row writer: 4x bl write_nibble_sequence_to_bg_tiles, stride 0x20 per row, 2x2 tile block. VRAM base 0x06010000 (DAT_080c03e8). Caller: render_card_display_with_type_gfx (ATK/DEF nibble rows).
write_nibble_row_pair_to_bg_tiles:
    push {r4,r5,r6,r7,lr}                    @ 080c0310 f0b5
    .hword 0x4657    @ 080c0312 5746
    .hword 0x464e    @ 080c0314 4e46
    .hword 0x4645    @ 080c0316 4546
    push {r5,r6,r7}                          @ 080c0318 e0b4
    adds r6,r0,#0x0    @ 080c031a 061c
    .hword 0x4689    @ 080c031c 8946
    .hword 0x4690    @ 080c031e 9046
    .hword 0x469a    @ 080c0320 9a46
    .hword 0x4648    @ 080c0322 4846
    lsls r0,r0,#0x10    @ 080c0324 0004
    lsrs r0,r0,#0x10    @ 080c0326 000c
    .hword 0x4681    @ 080c0328 8146
    .hword 0x4650    @ 080c032a 5046
    lsls r0,r0,#0x18    @ 080c032c 0006
    lsrs r0,r0,#0x18    @ 080c032e 000e
    .hword 0x4682    @ 080c0330 8246
    lsls r4,r6,#0x10    @ 080c0332 3404
    lsrs r4,r4,#0x10    @ 080c0334 240c
    lsrs r6,r6,#0x10    @ 080c0336 360c
    lsls r5,r6,#0x10    @ 080c0338 3504
    adds r0,r4,#0x0    @ 080c033a 201c
    orrs r0,r5    @ 080c033c 2843
    .hword 0x4649    @ 080c033e 4946
    .hword 0x4653    @ 080c0340 5346
    bl write_nibble_sequence_to_bg_tiles     @ 080c0342 fff797ff
    movs r0,#0x20    @ 080c0346 2020
    add r8,r0                                @ 080c0348 8044
    adds r7,r4,#0x0    @ 080c034a 271c
    adds r7,#0x8    @ 080c034c 0837
    orrs r5,r7    @ 080c034e 3d43
    adds r0,r5,#0x0    @ 080c0350 281c
    .hword 0x4649    @ 080c0352 4946
    .hword 0x4642    @ 080c0354 4246
    .hword 0x4653    @ 080c0356 5346
    bl write_nibble_sequence_to_bg_tiles     @ 080c0358 fff78cff
    movs r0,#0x20    @ 080c035c 2020
    add r8,r0                                @ 080c035e 8044
    adds r6,#0x8    @ 080c0360 0836
    lsls r6,r6,#0x10    @ 080c0362 3604
    orrs r4,r6    @ 080c0364 3443
    adds r0,r4,#0x0    @ 080c0366 201c
    .hword 0x4649    @ 080c0368 4946
    .hword 0x4642    @ 080c036a 4246
    .hword 0x4653    @ 080c036c 5346
    bl write_nibble_sequence_to_bg_tiles     @ 080c036e fff781ff
    movs r0,#0x20    @ 080c0372 2020
    add r8,r0                                @ 080c0374 8044
    orrs r7,r6    @ 080c0376 3743
    adds r0,r7,#0x0    @ 080c0378 381c
    .hword 0x4649    @ 080c037a 4946
    .hword 0x4642    @ 080c037c 4246
    .hword 0x4653    @ 080c037e 5346
    bl write_nibble_sequence_to_bg_tiles     @ 080c0380 fff778ff
    pop {r3,r4,r5}                           @ 080c0384 38bc
    .hword 0x4698    @ 080c0386 9846
    .hword 0x46a1    @ 080c0388 a146
    .hword 0x46aa    @ 080c038a aa46
    pop {r4,r5,r6,r7}                        @ 080c038c f0bc
    pop {r0}                                 @ 080c038e 01bc
    bx r0                                    @ 080c0390 0047
    .zero  0x2

@ Card frame nibble tile copy to OBJ/BG VRAM by palette offset. r1>>11=type selects 0x06010000 BG or 0x05000200 PAL VRAM. Tail-jumps to LAB_080c0598 (no independent return). Caller: render_card_display_with_type_gfx.
copy_card_frame_nibbles_to_palette_vram:
    push {r4,r5,r6,r7,lr}                    @ 080c0394 f0b5
    .hword 0x4657    @ 080c0396 5746
    .hword 0x464e    @ 080c0398 4e46
    .hword 0x4645    @ 080c039a 4546
    push {r5,r6,r7}                          @ 080c039c e0b4
    sub sp,#0x8                              @ 080c039e 82b0
    adds r4,r2,#0x0    @ 080c03a0 141c
    lsls r0,r0,#0x10    @ 080c03a2 0004
    lsrs r0,r0,#0x10    @ 080c03a4 000c
    .hword 0x4680    @ 080c03a6 8046
    lsls r1,r1,#0x10    @ 080c03a8 0904
    ldrh r0,[r4,#0x0]                        @ 080c03aa 2088
    lsls r2,r0,#0x1    @ 080c03ac 4200
    adds r3,r2,#0x0    @ 080c03ae 131c
    adds r3,#0x8    @ 080c03b0 0833
    adds r3,r4,r3    @ 080c03b2 e318
    adds r0,r2,#0x0    @ 080c03b4 101c
    adds r0,#0x10    @ 080c03b6 1030
    adds r0,r4,r0    @ 080c03b8 2018
    str r0,[sp,#0x0]                         @ 080c03ba 0090
    lsrs r1,r1,#0xb    @ 080c03bc c90a
    ldr r7, DAT_080c03e8                     @ 080c03be 0a4f
    adds r7,r7,r1    @ 080c03c0 7f18
    .hword 0x46ba    @ 080c03c2 ba46
    ldrh r3,[r3,#0x0]                        @ 080c03c4 1b88
    lsls r0,r3,#0x5    @ 080c03c6 5801
    ldr r1,[sp,#0x0]                         @ 080c03c8 0099
    adds r0,r1,r0    @ 080c03ca 0818
    str r0,[sp,#0x4]                         @ 080c03cc 0190
    adds r0,#0x8    @ 080c03ce 0830
    .hword 0x4681    @ 080c03d0 8146
    .hword 0x4643    @ 080c03d2 4346
    lsls r0,r3,#0x1    @ 080c03d4 5800
    ldr r7, DAT_080c03ec                     @ 080c03d6 054f
    adds r0,r0,r7    @ 080c03d8 c019
    adds r4,#0x8    @ 080c03da 0834
    adds r1,r4,#0x0    @ 080c03dc 211c
    bl copy_bytes_by_halfword                @ 080c03de 34f061fd
    movs r7,#0x0    @ 080c03e2 0027
    b LAB_080c0598                           @ 080c03e4 d8e0
    .zero  0x2
DAT_080c03e8:
    .word  0x06010000                     @ 080c03e8 00000106
DAT_080c03ec:
    .word  0x05000200                     @ 080c03ec 00020005
LAB_080c03f0:
    .hword 0x4649    @ 080c03f0 4946
    ldrh r0,[r1,#0x0]                        @ 080c03f2 0888
    movs r2,#0x2    @ 080c03f4 0222
    add r9,r2                                @ 080c03f6 9144
    .hword 0x464b    @ 080c03f8 4b46
    ldrh r1,[r3,#0x0]                        @ 080c03fa 1988
    add r9,r2                                @ 080c03fc 9144
    movs r6,#0x3f    @ 080c03fe 3f26
    ands r6,r0    @ 080c0400 0640
    lsrs r2,r0,#0x8    @ 080c0402 020a
    ldr r0, DAT_080c0430                     @ 080c0404 0a48
    ands r0,r1    @ 080c0406 0840
    lsls r0,r0,#0x5    @ 080c0408 4001
    ldr r3,[sp,#0x0]                         @ 080c040a 009b
    adds r5,r3,r0    @ 080c040c 1d18
    movs r0,#0xc0    @ 080c040e c020
    lsls r0,r0,#0x4    @ 080c0410 0001
    ands r1,r0    @ 080c0412 0140
    lsrs r1,r1,#0xa    @ 080c0414 890a
    adds r3,r1,#0x0    @ 080c0416 0b1c
    lsls r6,r6,#0x6    @ 080c0418 b601
    lsls r0,r2,#0x1a    @ 080c041a 9006
    lsrs r2,r0,#0x10    @ 080c041c 020c
    cmp r1,#0x1                              @ 080c041e 0129
    beq LAB_080c0482                         @ 080c0420 2fd0
    cmp r1,#0x1                              @ 080c0422 0129
    bgt LAB_080c0434                         @ 080c0424 06dc
    cmp r1,#0x0                              @ 080c0426 0029
    beq LAB_080c0442                         @ 080c0428 0bd0
    adds r6,r7,#0x1    @ 080c042a 7e1c
    b LAB_080c0596                           @ 080c042c b3e0
    .zero  0x2
DAT_080c0430:
    .word  0x000003ff                     @ 080c0430 ff030000
LAB_080c0434:
    cmp r3,#0x2                              @ 080c0434 022b
    beq LAB_080c04ea                         @ 080c0436 58d0
    cmp r3,#0x3                              @ 080c0438 032b
    bne LAB_080c043e                         @ 080c043a 00d1
    b LAB_080c054c                           @ 080c043c 86e0
LAB_080c043e:
    adds r6,r7,#0x1    @ 080c043e 7e1c
    b LAB_080c0596                           @ 080c0440 a9e0
LAB_080c0442:
    .hword 0x4651    @ 080c0442 5146
    adds r0,r1,r6    @ 080c0444 8819
    adds r6,r7,#0x1    @ 080c0446 7e1c
    adds r3,r0,r2    @ 080c0448 8318
    movs r4,#0x1f    @ 080c044a 1f24
LAB_080c044c:
    movs r1,#0x0    @ 080c044c 0021
    ldrb r0,[r5,#0x0]                        @ 080c044e 2878
    adds r2,r0,#0x0    @ 080c0450 021c
    movs r7,#0xf0    @ 080c0452 f027
    ands r0,r7    @ 080c0454 3840
    lsls r0,r0,#0x18    @ 080c0456 0006
    cmp r0,#0x0                              @ 080c0458 0028
    beq LAB_080c0464                         @ 080c045a 03d0
    lsrs r0,r0,#0x1c    @ 080c045c 000f
    add r0,r8                                @ 080c045e 4044
    lsls r0,r0,#0x18    @ 080c0460 0006
    lsrs r1,r0,#0x10    @ 080c0462 010c
LAB_080c0464:
    movs r0,#0xf    @ 080c0464 0f20
    ands r0,r2    @ 080c0466 1040
    cmp r0,#0x0                              @ 080c0468 0028
    beq LAB_080c0474                         @ 080c046a 03d0
    add r0,r8                                @ 080c046c 4044
    orrs r1,r0    @ 080c046e 0143
    lsls r0,r1,#0x10    @ 080c0470 0804
    lsrs r1,r0,#0x10    @ 080c0472 010c
LAB_080c0474:
    strh r1,[r3,#0x0]                        @ 080c0474 1980
    adds r5,#0x1    @ 080c0476 0135
    adds r3,#0x2    @ 080c0478 0233
    subs r4,#0x1    @ 080c047a 013c
    cmp r4,#0x0                              @ 080c047c 002c
    bge LAB_080c044c                         @ 080c047e e5da
    b LAB_080c0596                           @ 080c0480 89e0
LAB_080c0482:
    movs r0,#0x6    @ 080c0482 0620
    .hword 0x4684    @ 080c0484 8446
    movs r4,#0x0    @ 080c0486 0024
    .hword 0x4651    @ 080c0488 5146
    adds r0,r1,r6    @ 080c048a 8819
    adds r6,r7,#0x1    @ 080c048c 7e1c
    adds r7,r0,r2    @ 080c048e 8718
LAB_080c0490:
    movs r3,#0x0    @ 080c0490 0023
    ldrb r0,[r5,#0x0]                        @ 080c0492 2878
    adds r1,r0,#0x0    @ 080c0494 011c
    movs r2,#0xf0    @ 080c0496 f022
    ands r0,r2    @ 080c0498 1040
    lsls r0,r0,#0x18    @ 080c049a 0006
    cmp r0,#0x0                              @ 080c049c 0028
    beq LAB_080c04a8                         @ 080c049e 03d0
    lsrs r0,r0,#0x1c    @ 080c04a0 000f
    add r0,r8                                @ 080c04a2 4044
    lsls r0,r0,#0x18    @ 080c04a4 0006
    lsrs r3,r0,#0x10    @ 080c04a6 030c
LAB_080c04a8:
    movs r0,#0xf    @ 080c04a8 0f20
    ands r0,r1    @ 080c04aa 0840
    cmp r0,#0x0                              @ 080c04ac 0028
    beq LAB_080c04b8                         @ 080c04ae 03d0
    add r0,r8                                @ 080c04b0 4044
    orrs r3,r0    @ 080c04b2 0343
    lsls r0,r3,#0x10    @ 080c04b4 1804
    lsrs r3,r0,#0x10    @ 080c04b6 030c
LAB_080c04b8:
    .hword 0x4660    @ 080c04b8 6046
    adds r2,r7,r0    @ 080c04ba 3a18
    lsls r0,r4,#0x1    @ 080c04bc 6000
    subs r2,r2,r0    @ 080c04be 121a
    lsrs r1,r3,#0x8    @ 080c04c0 190a
    lsls r0,r3,#0x18    @ 080c04c2 1806
    lsrs r0,r0,#0x10    @ 080c04c4 000c
    orrs r1,r0    @ 080c04c6 0143
    strh r1,[r2,#0x0]                        @ 080c04c8 1180
    adds r5,#0x1    @ 080c04ca 0135
    adds r0,r4,#0x0    @ 080c04cc 201c
    cmp r4,#0x0                              @ 080c04ce 002c
    bge LAB_080c04d4                         @ 080c04d0 00da
    adds r0,r4,#0x3    @ 080c04d2 e01c
LAB_080c04d4:
    asrs r0,r0,#0x2    @ 080c04d4 8010
    lsls r0,r0,#0x2    @ 080c04d6 8000
    subs r0,r4,r0    @ 080c04d8 201a
    cmp r0,#0x3                              @ 080c04da 0328
    bne LAB_080c04e2                         @ 080c04dc 01d1
    movs r1,#0x10    @ 080c04de 1021
    add r12,r1                               @ 080c04e0 8c44
LAB_080c04e2:
    adds r4,#0x1    @ 080c04e2 0134
    cmp r4,#0x1f                             @ 080c04e4 1f2c
    ble LAB_080c0490                         @ 080c04e6 d3dd
    b LAB_080c0596                           @ 080c04e8 55e0
LAB_080c04ea:
    movs r3,#0x38    @ 080c04ea 3823
    .hword 0x469c    @ 080c04ec 9c46
    movs r4,#0x0    @ 080c04ee 0024
    .hword 0x4651    @ 080c04f0 5146
    adds r0,r1,r6    @ 080c04f2 8819
    adds r6,r7,#0x1    @ 080c04f4 7e1c
    adds r2,r0,r2    @ 080c04f6 8218
LAB_080c04f8:
    movs r3,#0x0    @ 080c04f8 0023
    ldrb r0,[r5,#0x0]                        @ 080c04fa 2878
    adds r1,r0,#0x0    @ 080c04fc 011c
    movs r7,#0xf0    @ 080c04fe f027
    ands r0,r7    @ 080c0500 3840
    lsls r0,r0,#0x18    @ 080c0502 0006
    cmp r0,#0x0                              @ 080c0504 0028
    beq LAB_080c0510                         @ 080c0506 03d0
    lsrs r0,r0,#0x1c    @ 080c0508 000f
    add r0,r8                                @ 080c050a 4044
    lsls r0,r0,#0x18    @ 080c050c 0006
    lsrs r3,r0,#0x10    @ 080c050e 030c
LAB_080c0510:
    movs r0,#0xf    @ 080c0510 0f20
    ands r0,r1    @ 080c0512 0840
    cmp r0,#0x0                              @ 080c0514 0028
    beq LAB_080c0520                         @ 080c0516 03d0
    add r0,r8                                @ 080c0518 4044
    orrs r3,r0    @ 080c051a 0343
    lsls r0,r3,#0x10    @ 080c051c 1804
    lsrs r3,r0,#0x10    @ 080c051e 030c
LAB_080c0520:
    lsls r0,r4,#0x1    @ 080c0520 6000
    .hword 0x4667    @ 080c0522 6746
    adds r1,r2,r7    @ 080c0524 d119
    adds r0,r0,r1    @ 080c0526 4018
    strh r3,[r0,#0x0]                        @ 080c0528 0380
    adds r5,#0x1    @ 080c052a 0135
    adds r0,r4,#0x0    @ 080c052c 201c
    cmp r4,#0x0                              @ 080c052e 002c
    bge LAB_080c0534                         @ 080c0530 00da
    adds r0,r4,#0x3    @ 080c0532 e01c
LAB_080c0534:
    asrs r0,r0,#0x2    @ 080c0534 8010
    lsls r0,r0,#0x2    @ 080c0536 8000
    subs r0,r4,r0    @ 080c0538 201a
    cmp r0,#0x3                              @ 080c053a 0328
    bne LAB_080c0544                         @ 080c053c 02d1
    movs r0,#0x10    @ 080c053e 1020
    rsbs r0,r0,#0    @ 080c0540 4042
    add r12,r0                               @ 080c0542 8444
LAB_080c0544:
    adds r4,#0x1    @ 080c0544 0134
    cmp r4,#0x1f                             @ 080c0546 1f2c
    ble LAB_080c04f8                         @ 080c0548 d6dd
    b LAB_080c0596                           @ 080c054a 24e0
LAB_080c054c:
    movs r4,#0x1f    @ 080c054c 1f24
    .hword 0x4651    @ 080c054e 5146
    adds r0,r1,r6    @ 080c0550 8819
    adds r6,r7,#0x1    @ 080c0552 7e1c
    adds r0,r0,r2    @ 080c0554 8018
    adds r2,r0,#0x0    @ 080c0556 021c
    adds r2,#0x3e    @ 080c0558 3e32
LAB_080c055a:
    movs r3,#0x0    @ 080c055a 0023
    ldrb r0,[r5,#0x0]                        @ 080c055c 2878
    adds r1,r0,#0x0    @ 080c055e 011c
    movs r7,#0xf0    @ 080c0560 f027
    ands r0,r7    @ 080c0562 3840
    lsls r0,r0,#0x18    @ 080c0564 0006
    cmp r0,#0x0                              @ 080c0566 0028
    beq LAB_080c0572                         @ 080c0568 03d0
    lsrs r0,r0,#0x1c    @ 080c056a 000f
    add r0,r8                                @ 080c056c 4044
    lsls r0,r0,#0x18    @ 080c056e 0006
    lsrs r3,r0,#0x10    @ 080c0570 030c
LAB_080c0572:
    movs r0,#0xf    @ 080c0572 0f20
    ands r0,r1    @ 080c0574 0840
    cmp r0,#0x0                              @ 080c0576 0028
    beq LAB_080c0582                         @ 080c0578 03d0
    add r0,r8                                @ 080c057a 4044
    orrs r3,r0    @ 080c057c 0343
    lsls r0,r3,#0x10    @ 080c057e 1804
    lsrs r3,r0,#0x10    @ 080c0580 030c
LAB_080c0582:
    lsrs r1,r3,#0x8    @ 080c0582 190a
    lsls r0,r3,#0x18    @ 080c0584 1806
    lsrs r0,r0,#0x10    @ 080c0586 000c
    orrs r1,r0    @ 080c0588 0143
    strh r1,[r2,#0x0]                        @ 080c058a 1180
    adds r5,#0x1    @ 080c058c 0135
    subs r2,#0x2    @ 080c058e 023a
    subs r4,#0x1    @ 080c0590 013c
    cmp r4,#0x0                              @ 080c0592 002c
    bge LAB_080c055a                         @ 080c0594 e1da
LAB_080c0596:
    adds r7,r6,#0x0    @ 080c0596 371c
LAB_080c0598:
    ldr r0,[sp,#0x4]                         @ 080c0598 0198
    ldrh r0,[r0,#0x0]                        @ 080c059a 0088
    cmp r7,r0                                @ 080c059c 8742
    bge LAB_080c05a2                         @ 080c059e 00da
    b LAB_080c03f0                           @ 080c05a0 26e7
LAB_080c05a2:
    add sp,#0x8                              @ 080c05a2 02b0
    pop {r3,r4,r5}                           @ 080c05a4 38bc
    .hword 0x4698    @ 080c05a6 9846
    .hword 0x46a1    @ 080c05a8 a146
    .hword 0x46aa    @ 080c05aa aa46
    pop {r4,r5,r6,r7}                        @ 080c05ac f0bc
    pop {r0}                                 @ 080c05ae 01bc
    bx r0                                    @ 080c05b0 0047
    .zero  0x2

@ Full card display render: card image + ATK/DEF nibble tiles + name label + type icon. Reads card_stats_table[card_id*11]. Dispatches on card_type 0x16/0x17 (fusion/ritual frame). Callers: play_ui_effect_33, play_ui_effect_34.
render_card_display_with_type_gfx:
    push {r4,r5,r6,r7,lr}                    @ 080c05b4 f0b5
    .hword 0x464f    @ 080c05b6 4f46
    .hword 0x4646    @ 080c05b8 4646
    push {r6,r7}                             @ 080c05ba c0b4
    adds r6,r0,#0x0    @ 080c05bc 061c
    ldr r2, PTR_card_stats_table_080c060c    @ 080c05be 134a
    movs r0,#0xb    @ 080c05c0 0b20
    adds r1,r6,#0x0    @ 080c05c2 311c
    muls r1,r0    @ 080c05c4 4143
    adds r0,r1,#0x7    @ 080c05c6 c81d
    lsls r0,r0,#0x1    @ 080c05c8 4000
    adds r0,r0,r2    @ 080c05ca 8018
    ldrh r0,[r0,#0x0]                        @ 080c05cc 0088
    .hword 0x4681    @ 080c05ce 8146
    adds r0,r1,#0x6    @ 080c05d0 881d
    lsls r0,r0,#0x1    @ 080c05d2 4000
    adds r0,r0,r2    @ 080c05d4 8018
    ldrh r5,[r0,#0x0]                        @ 080c05d6 0588
    adds r0,r1,#0x5    @ 080c05d8 481d
    lsls r0,r0,#0x1    @ 080c05da 4000
    adds r0,r0,r2    @ 080c05dc 8018
    ldrh r7,[r0,#0x0]                        @ 080c05de 0788
    adds r1,#0x9    @ 080c05e0 0931
    lsls r1,r1,#0x1    @ 080c05e2 4900
    adds r1,r1,r2    @ 080c05e4 8918
    ldrh r1,[r1,#0x0]                        @ 080c05e6 0988
    .hword 0x4688    @ 080c05e8 8846
    lsls r0,r6,#0x10    @ 080c05ea 3004
    lsrs r0,r0,#0x10    @ 080c05ec 000c
    ldr r1, DAT_080c0610                     @ 080c05ee 0849
    movs r2,#0x9    @ 080c05f0 0922
    bl render_card_image_to_vram             @ 080c05f2 fff7bbfc
    cmp r5,#0x17                             @ 080c05f6 172d
    bgt LAB_080c0618                         @ 080c05f8 0edc
    cmp r5,#0x16                             @ 080c05fa 162d
    blt LAB_080c0618                         @ 080c05fc 0cdb
    movs r1,#0xe1    @ 080c05fe e121
    lsls r1,r1,#0x1    @ 080c0600 4900
    ldr r2, DAT_080c0614                     @ 080c0602 044a
    movs r0,#0xd0    @ 080c0604 d020
    bl copy_card_frame_nibbles_to_palette_vram @ 080c0606 fff7c5fe
    b LAB_080c0624                           @ 080c060a 0be0
PTR_card_stats_table_080c060c:
    .word  card_stats_table               @ 080c060c b8698109
DAT_080c0610:
    .word  0x00000246                     @ 080c0610 46020000
DAT_080c0614:
    .word  0x0984b994                     @ 080c0614 94b98409
LAB_080c0618:
    movs r1,#0xe1    @ 080c0618 e121
    lsls r1,r1,#0x1    @ 080c061a 4900
    ldr r2, DAT_080c0688                     @ 080c061c 1a4a
    movs r0,#0xd0    @ 080c061e d020
    bl copy_card_frame_nibbles_to_palette_vram @ 080c0620 fff7b8fe
LAB_080c0624:
    ldr r4, DAT_080c068c                     @ 080c0624 194c
    lsls r0,r6,#0x10    @ 080c0626 3004
    lsrs r6,r0,#0x10    @ 080c0628 060c
    adds r0,r6,#0x0    @ 080c062a 301c
    bl resolve_card_type_icon_ptr            @ 080c062c 2ef04efe
    adds r1,r0,#0x0    @ 080c0630 011c
    adds r0,r4,#0x0    @ 080c0632 201c
    movs r2,#0x20    @ 080c0634 2022
    bl copy_bytes_by_halfword                @ 080c0636 34f035fc
    adds r0,r6,#0x0    @ 080c063a 301c
    bl draw_card_name_to_bg_tile_vram        @ 080c063c fff758fd
    cmp r5,#0x16                             @ 080c0640 162d
    beq LAB_080c06c8                         @ 080c0642 41d0
    cmp r5,#0x16                             @ 080c0644 162d
    bgt LAB_080c06a0                         @ 080c0646 2bdc
    cmp r5,#0x14                             @ 080c0648 142d
    ble LAB_080c064e                         @ 080c064a 00dd
    b LAB_080c0750                           @ 080c064c 80e0
LAB_080c064e:
    cmp r5,#0x1                              @ 080c064e 012d
    bge LAB_080c0654                         @ 080c0650 00da
    b LAB_080c0750                           @ 080c0652 7de0
LAB_080c0654:
    ldr r0, DAT_080c0690                     @ 080c0654 0e48
    .hword 0x464c    @ 080c0656 4c46
    subs r4,#0x1    @ 080c0658 013c
    lsls r1,r4,#0x5    @ 080c065a 6101
    ldr r2, DAT_080c0694                     @ 080c065c 0d4a
    adds r1,r1,r2    @ 080c065e 8918
    movs r2,#0x20    @ 080c0660 2022
    bl copy_bytes_by_halfword                @ 080c0662 34f01ffc
    ldr r0, DAT_080c0698                     @ 080c0666 0c48
    movs r1,#0xeb    @ 080c0668 eb21
    lsls r1,r1,#0x1    @ 080c066a 4900
    lsls r4,r4,#0x7    @ 080c066c e401
    ldr r2, DAT_080c069c                     @ 080c066e 0b4a
    adds r4,r4,r2    @ 080c0670 a418
    adds r2,r4,#0x0    @ 080c0672 221c
    movs r3,#0xe    @ 080c0674 0e23
    bl write_nibble_row_pair_to_bg_tiles     @ 080c0676 fff74bfe
    adds r0,r6,#0x0    @ 080c067a 301c
    bl draw_card_atkdef_label_to_vram        @ 080c067c fff780fd
    movs r4,#0x0    @ 080c0680 0024
    cmp r4,r7                                @ 080c0682 bc42
    bge LAB_080c0750                         @ 080c0684 64da
    b LAB_080c0728                           @ 080c0686 4fe0
DAT_080c0688:
    .word  0x0984a3fc                     @ 080c0688 fca38409
DAT_080c068c:
    .word  0x050003a0                     @ 080c068c a0030005
DAT_080c0690:
    .word  0x050003c0                     @ 080c0690 c0030005
DAT_080c0694:
    .word  0x0984dd6c                     @ 080c0694 6cdd8409
DAT_080c0698:
    .word  0x00060006                     @ 080c0698 06000600
DAT_080c069c:
    .word  0x0984d8ec                     @ 080c069c ecd88409
LAB_080c06a0:
    cmp r5,#0x17                             @ 080c06a0 172d
    bne LAB_080c0750                         @ 080c06a2 55d1
    ldr r0, DAT_080c06b8                     @ 080c06a4 0448
    ldr r1, DAT_080c06bc                     @ 080c06a6 0549
    movs r2,#0x20    @ 080c06a8 2022
    bl copy_bytes_by_halfword                @ 080c06aa 34f0fbfb
    ldr r0, DAT_080c06c0                     @ 080c06ae 0448
    movs r1,#0xeb    @ 080c06b0 eb21
    lsls r1,r1,#0x1    @ 080c06b2 4900
    ldr r2, DAT_080c06c4                     @ 080c06b4 034a
    b LAB_080c06da                           @ 080c06b6 10e0
DAT_080c06b8:
    .word  0x050003c0                     @ 080c06b8 c0030005
DAT_080c06bc:
    .word  0x0984de6c                     @ 080c06bc 6cde8409
DAT_080c06c0:
    .word  0x00060006                     @ 080c06c0 06000600
DAT_080c06c4:
    .word  0x0984dcec                     @ 080c06c4 ecdc8409
LAB_080c06c8:
    ldr r0, DAT_080c0708                     @ 080c06c8 0f48
    ldr r1, DAT_080c070c                     @ 080c06ca 1049
    movs r2,#0x20    @ 080c06cc 2022
    bl copy_bytes_by_halfword                @ 080c06ce 34f0e9fb
    ldr r0, DAT_080c0710                     @ 080c06d2 0f48
    movs r1,#0xeb    @ 080c06d4 eb21
    lsls r1,r1,#0x1    @ 080c06d6 4900
    ldr r2, DAT_080c0714                     @ 080c06d8 0e4a
LAB_080c06da:
    movs r3,#0xe    @ 080c06da 0e23
    bl write_nibble_row_pair_to_bg_tiles     @ 080c06dc fff718fe
    .hword 0x4640    @ 080c06e0 4046
    cmp r0,#0x0                              @ 080c06e2 0028
    beq LAB_080c0750                         @ 080c06e4 34d0
    ldr r0, DAT_080c0718                     @ 080c06e6 0c48
    ldr r1, DAT_080c071c                     @ 080c06e8 0c49
    movs r2,#0x20    @ 080c06ea 2022
    bl copy_bytes_by_halfword                @ 080c06ec 34f0dafb
    ldr r0, DAT_080c0720                     @ 080c06f0 0b48
    movs r1,#0x81    @ 080c06f2 8121
    lsls r1,r1,#0x2    @ 080c06f4 8900
    .hword 0x4642    @ 080c06f6 4246
    subs r2,#0x1    @ 080c06f8 013a
    lsls r2,r2,#0x5    @ 080c06fa 5201
    ldr r3, DAT_080c0724                     @ 080c06fc 094b
    adds r2,r2,r3    @ 080c06fe d218
    movs r3,#0xf    @ 080c0700 0f23
    bl write_nibble_sequence_to_bg_tiles     @ 080c0702 fff7b7fd
    b LAB_080c0750                           @ 080c0706 23e0
DAT_080c0708:
    .word  0x050003c0                     @ 080c0708 c0030005
DAT_080c070c:
    .word  0x0984de4c                     @ 080c070c 4cde8409
DAT_080c0710:
    .word  0x00060006                     @ 080c0710 06000600
DAT_080c0714:
    .word  0x0984dc6c                     @ 080c0714 6cdc8409
DAT_080c0718:
    .word  0x050003e0                     @ 080c0718 e0030005
DAT_080c071c:
    .word  0x0984f52c                     @ 080c071c 2cf58409
DAT_080c0720:
    .word  0x00050050                     @ 080c0720 50000500
DAT_080c0724:
    .word  0x0984f46c                     @ 080c0724 6cf48409
LAB_080c0728:
    movs r0,#0x8    @ 080c0728 0820
    cmp r7,#0xa                              @ 080c072a 0a2f
    bls LAB_080c0730                         @ 080c072c 00d9
    movs r0,#0x7    @ 080c072e 0720
LAB_080c0730:
    adds r1,r4,#0x0    @ 080c0730 211c
    muls r1,r0    @ 080c0732 4143
    movs r0,#0x55    @ 080c0734 5520
    subs r0,r0,r1    @ 080c0736 401a
    movs r1,#0xc0    @ 080c0738 c021
    lsls r1,r1,#0xb    @ 080c073a c902
    orrs r0,r1    @ 080c073c 0843
    movs r1,#0x81    @ 080c073e 8121
    lsls r1,r1,#0x2    @ 080c0740 8900
    ldr r2, DAT_080c075c                     @ 080c0742 064a
    movs r3,#0x0    @ 080c0744 0023
    bl write_nibble_sequence_to_bg_tiles     @ 080c0746 fff795fd
    adds r4,#0x1    @ 080c074a 0134
    cmp r4,r7                                @ 080c074c bc42
    blt LAB_080c0728                         @ 080c074e ebdb
LAB_080c0750:
    pop {r3,r4}                              @ 080c0750 18bc
    .hword 0x4698    @ 080c0752 9846
    .hword 0x46a1    @ 080c0754 a146
    pop {r4,r5,r6,r7}                        @ 080c0756 f0bc
    pop {r0}                                 @ 080c0758 01bc
    bx r0                                    @ 080c075a 0047
DAT_080c075c:
    .word  0x09ccd2d0                     @ 080c075c d0d2cc09

@ 将卡图 tile 以 5x4 网格形式写入 OAM, 被 play_ui_effect_33/34 调用. 根据 r0 (tile_offset_sign, 0 或 1) 计算 OAM attr bit7 (0x400 掩码), 对 5 行 x 4 列 OAM 条目循环调用 write_oam_entry_with_tile_inc, 每行 tile 步进 0x20, 每列 attr 步进 4. r1 在入口第一条指令 (rsbs r1,r0,#0) 被覆盖, 不是独立参数. Constants: GRID_COLS=4, GRID_ROWS=5, TILE_ROW_STEP=0x20, ATTR_STEP=4, OAM_ATTR_MASK=0x400.
write_card_image_oam_grid:
    push {r4,r5,r6,r7,lr}                    @ 080c0760 f0b5
    .hword 0x4657    @ 080c0762 5746
    .hword 0x464e    @ 080c0764 4e46
    .hword 0x4645    @ 080c0766 4546
    push {r5,r6,r7}                          @ 080c0768 e0b4
    sub sp,#0x4                              @ 080c076a 81b0
    rsbs r1,r0,#0    @ 080c076c 4142
    orrs r1,r0    @ 080c076e 0143
    asrs r1,r1,#0x1f    @ 080c0770 c917
    .hword 0x468a    @ 080c0772 8a46
    movs r0,#0x80    @ 080c0774 8020
    lsls r0,r0,#0x3    @ 080c0776 c000
    ands r1,r0    @ 080c0778 0140
    .hword 0x468a    @ 080c077a 8a46
    movs r5,#0x0    @ 080c077c 0025
LAB_080c077e:
    movs r3,#0x80    @ 080c077e 8023
    cmp r5,#0x4                              @ 080c0780 042d
    bne LAB_080c0788                         @ 080c0782 01d1
    movs r3,#0x81    @ 080c0784 8123
    lsls r3,r3,#0x7    @ 080c0786 db01
LAB_080c0788:
    movs r6,#0x0    @ 080c0788 0026
    lsls r2,r5,#0x15    @ 080c078a 6a05
    .hword 0x4690    @ 080c078c 9046
    lsls r0,r5,#0x6    @ 080c078e a801
    adds r1,r5,#0x1    @ 080c0790 691c
    .hword 0x4689    @ 080c0792 8946
    adds r4,r0,#0x0    @ 080c0794 041c
    adds r4,#0xe1    @ 080c0796 e134
    movs r7,#0x54    @ 080c0798 5427
LAB_080c079a:
    cmp r6,#0x3                              @ 080c079a 032e
    bne LAB_080c07a6                         @ 080c079c 03d1
    ldr r3, DAT_080c07e0                     @ 080c079e 104b
    cmp r5,#0x4                              @ 080c07a0 042d
    bne LAB_080c07a6                         @ 080c07a2 00d1
    movs r3,#0x40    @ 080c07a4 4023
LAB_080c07a6:
    adds r0,r7,#0x0    @ 080c07a6 381c
    .hword 0x4642    @ 080c07a8 4246
    orrs r0,r2    @ 080c07aa 1043
    adds r1,r3,#0x0    @ 080c07ac 191c
    .hword 0x4652    @ 080c07ae 5246
    orrs r1,r2    @ 080c07b0 1143
    lsls r2,r4,#0x10    @ 080c07b2 2204
    lsrs r2,r2,#0x10    @ 080c07b4 120c
    str r3,[sp,#0x0]                         @ 080c07b6 0093
    bl write_oam_entry_with_tile_inc         @ 080c07b8 35f04afe
    adds r4,#0x4    @ 080c07bc 0434
    adds r7,#0x20    @ 080c07be 2037
    adds r6,#0x1    @ 080c07c0 0136
    ldr r3,[sp,#0x0]                         @ 080c07c2 009b
    cmp r6,#0x3                              @ 080c07c4 032e
    ble LAB_080c079a                         @ 080c07c6 e8dd
    .hword 0x464d    @ 080c07c8 4d46
    cmp r5,#0x4                              @ 080c07ca 042d
    ble LAB_080c077e                         @ 080c07cc d7dd
    add sp,#0x4                              @ 080c07ce 01b0
    pop {r3,r4,r5}                           @ 080c07d0 38bc
    .hword 0x4698    @ 080c07d2 9846
    .hword 0x46a1    @ 080c07d4 a146
    .hword 0x46aa    @ 080c07d6 aa46
    pop {r4,r5,r6,r7}                        @ 080c07d8 f0bc
    pop {r0}                                 @ 080c07da 01bc
    bx r0                                    @ 080c07dc 0047
    .zero  0x2
DAT_080c07e0:
    .word  0x00008080                     @ 080c07e0 80800000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x33 子状态机, 待详细分析.
play_ui_effect_33:
    push {r4,r5,r6,r7,lr}                    @ 080c07e4 f0b5
    .hword 0x4657    @ 080c07e6 5746
    .hword 0x464e    @ 080c07e8 4e46
    .hword 0x4645    @ 080c07ea 4546
    push {r5,r6,r7}                          @ 080c07ec e0b4
    ldr r4, DAT_080c080c                     @ 080c07ee 074c
    ldr r0,[r4,#0xc]                         @ 080c07f0 e068
    bl ensure_card_id_cache_entry            @ 080c07f2 0cf069f8
    adds r2,r0,#0x0    @ 080c07f6 021c
    ldrb r0,[r4,#0x10]                       @ 080c07f8 207c
    cmp r0,#0x5                              @ 080c07fa 0528
    bls LAB_080c0800                         @ 080c07fc 00d9
switchD_080c0808__default:
    b LAB_080c0a48                           @ 080c07fe 23e1
LAB_080c0800:
    lsls r0,r0,#0x2    @ 080c0800 8000
    ldr r1, DAT_080c0810                     @ 080c0802 0349
    adds r0,r0,r1    @ 080c0804 4018
    ldr r0,[r0,#0x0]                         @ 080c0806 0068
switchD_080c0808__switchD:
    .hword 0x4687    @ 080c0808 8746
    .zero  0x2
DAT_080c080c:
    .word  gBannerState                   @ 080c080c c0fe0102
DAT_080c0810:
    .word  0x080c0814                     @ 080c0810 14080c08
switchD_080c0808__switchdataD_080c0814:
    .word  0x080c082c                     @ 080c0814 2c080c08
    .word  0x080c0880                     @ 080c0818 80080c08
    .word  0x080c0974                     @ 080c081c 74090c08
    .word  0x080c0998                     @ 080c0820 98090c08
    .word  0x080c09d4                     @ 080c0824 d4090c08
    .word  0x080c0a14                     @ 080c0828 140a0c08
switchD_080c0808__caseD_0:
    adds r0,r2,#0x0    @ 080c082c 101c
    bl render_card_display_with_type_gfx     @ 080c082e fff7c1fe
    bl disable_blend_and_clear_step          @ 080c0832 34f0cffe
    ldr r1, PTR_WIN0H_080c0874               @ 080c0836 0f49
    ldr r2, DAT_080c0878                     @ 080c0838 0f4a
    adds r0,r2,#0x0    @ 080c083a 101c
    strh r0,[r1,#0x0]                        @ 080c083c 0880
    adds r1,#0x4    @ 080c083e 0431
    ldr r3, DAT_080c087c                     @ 080c0840 0e4b
    adds r0,r3,#0x0    @ 080c0842 181c
    strh r0,[r1,#0x0]                        @ 080c0844 0880
    adds r1,#0x4    @ 080c0846 0431
    movs r0,#0x3f    @ 080c0848 3f20
    strh r0,[r1,#0x0]                        @ 080c084a 0880
    adds r1,#0x2    @ 080c084c 0231
    movs r0,#0x1f    @ 080c084e 1f20
    strh r0,[r1,#0x0]                        @ 080c0850 0880
    adds r1,#0x6    @ 080c0852 0631
    movs r2,#0xfd    @ 080c0854 fd22
    lsls r2,r2,#0x6    @ 080c0856 9201
    adds r0,r2,#0x0    @ 080c0858 101c
    strh r0,[r1,#0x0]                        @ 080c085a 0880
    adds r1,#0x4    @ 080c085c 0431
    movs r0,#0x0    @ 080c085e 0020
    strh r0,[r1,#0x0]                        @ 080c0860 0880
    movs r2,#0x80    @ 080c0862 8022
    lsls r2,r2,#0x13    @ 080c0864 d204
    ldrh r0,[r2,#0x0]                        @ 080c0866 1088
    movs r3,#0x80    @ 080c0868 8023
    lsls r3,r3,#0x6    @ 080c086a 9b01
    adds r1,r3,#0x0    @ 080c086c 191c
    orrs r0,r1    @ 080c086e 0843
    b LAB_080c0a2a                           @ 080c0870 dbe0
    .zero  0x2
PTR_WIN0H_080c0874:
    .word  WIN0H                          @ 080c0874 40000004
DAT_080c0878:
    .word  0x00005abe                     @ 080c0878 be5a0000
DAT_080c087c:
    .word  0x0000028e                     @ 080c087c 8e020000
switchD_080c0808__caseD_1:
    movs r0,#0x54    @ 080c0880 5420
    .hword 0x4680    @ 080c0882 8046
    movs r7,#0x8    @ 080c0884 0827
    movs r1,#0x81    @ 080c0886 8121
    lsls r1,r1,#0x7    @ 080c0888 c901
    .hword 0x468a    @ 080c088a 8a46
LAB_080c088c:
    movs r2,#0x8    @ 080c088c 0822
    subs r0,r2,r7    @ 080c088e d01b
    ldr r3, DAT_080c0968                     @ 080c0890 354b
    .hword 0x4699    @ 080c0892 9946
    ldrh r1,[r3,#0x12]                       @ 080c0894 598a
    muls r0,r1    @ 080c0896 4843
    cmp r0,#0x0                              @ 080c0898 0028
    bge LAB_080c089e                         @ 080c089a 00da
    adds r0,#0xf    @ 080c089c 0f30
LAB_080c089e:
    asrs r0,r0,#0x4    @ 080c089e 0011
    movs r2,#0x8    @ 080c08a0 0822
    subs r0,r2,r0    @ 080c08a2 101a
    subs r6,r0,r7    @ 080c08a4 c61b
    ldr r2, DAT_080c096c                     @ 080c08a6 314a
    lsls r1,r1,#0x1    @ 080c08a8 4900
    movs r0,#0x7f    @ 080c08aa 7f20
    ands r1,r0    @ 080c08ac 0140
    lsls r1,r1,#0x1    @ 080c08ae 4900
    adds r1,r1,r2    @ 080c08b0 8918
    lsls r2,r7,#0x4    @ 080c08b2 3a01
    movs r0,#0x80    @ 080c08b4 8020
    subs r0,r0,r2    @ 080c08b6 801a
    ldrh r1,[r1,#0x0]                        @ 080c08b8 0988
    muls r1,r0    @ 080c08ba 4143
    cmp r1,#0x0                              @ 080c08bc 0029
    bge LAB_080c08c2                         @ 080c08be 00da
    adds r1,#0xff    @ 080c08c0 ff31
LAB_080c08c2:
    asrs r4,r1,#0x8    @ 080c08c2 0c12
    .hword 0x4643    @ 080c08c4 4346
    adds r0,r3,r6    @ 080c08c6 9819
    movs r1,#0x80    @ 080c08c8 8021
    subs r4,r1,r4    @ 080c08ca 0c1b
    lsls r4,r4,#0x10    @ 080c08cc 2404
    orrs r0,r4    @ 080c08ce 2043
    lsls r5,r7,#0x5    @ 080c08d0 7d01
    adds r2,r5,#0x0    @ 080c08d2 2a1c
    adds r2,#0xe1    @ 080c08d4 e132
    lsls r2,r2,#0x10    @ 080c08d6 1204
    lsrs r2,r2,#0x10    @ 080c08d8 120c
    movs r1,#0x40    @ 080c08da 4021
    bl write_oam_entry_with_tile_inc         @ 080c08dc 35f0b8fd
    adds r0,r6,#0x0    @ 080c08e0 301c
    subs r0,#0x60    @ 080c08e2 6038
    .hword 0x4642    @ 080c08e4 4246
    subs r0,r2,r0    @ 080c08e6 101a
    orrs r0,r4    @ 080c08e8 2043
    adds r2,r5,#0x0    @ 080c08ea 2a1c
    adds r2,#0xed    @ 080c08ec ed32
    lsls r2,r2,#0x10    @ 080c08ee 1204
    lsrs r2,r2,#0x10    @ 080c08f0 120c
    movs r1,#0x40    @ 080c08f2 4021
    bl write_oam_entry_with_tile_inc         @ 080c08f4 35f0acfd
    adds r0,r6,#0x0    @ 080c08f8 301c
    adds r0,#0x10    @ 080c08fa 1030
    add r0,r8                                @ 080c08fc 4044
    orrs r0,r4    @ 080c08fe 2043
    adds r2,r5,#0x0    @ 080c0900 2a1c
    adds r2,#0xe3    @ 080c0902 e332
    lsls r2,r2,#0x10    @ 080c0904 1204
    lsrs r2,r2,#0x10    @ 080c0906 120c
    .hword 0x4651    @ 080c0908 5146
    bl write_oam_entry_with_tile_inc         @ 080c090a 35f0a1fd
    adds r0,r6,#0x0    @ 080c090e 301c
    subs r0,#0x40    @ 080c0910 4038
    .hword 0x4643    @ 080c0912 4346
    subs r0,r3,r0    @ 080c0914 181a
    orrs r0,r4    @ 080c0916 2043
    adds r2,r5,#0x0    @ 080c0918 2a1c
    adds r2,#0xe9    @ 080c091a e932
    lsls r2,r2,#0x10    @ 080c091c 1204
    lsrs r2,r2,#0x10    @ 080c091e 120c
    .hword 0x4651    @ 080c0920 5146
    bl write_oam_entry_with_tile_inc         @ 080c0922 35f095fd
    .hword 0x4640    @ 080c0926 4046
    adds r0,#0x30    @ 080c0928 3030
    orrs r0,r4    @ 080c092a 2043
    adds r2,r5,#0x0    @ 080c092c 2a1c
    adds r2,#0xe7    @ 080c092e e732
    lsls r2,r2,#0x10    @ 080c0930 1204
    lsrs r2,r2,#0x10    @ 080c0932 120c
    movs r1,#0x40    @ 080c0934 4021
    bl write_oam_entry_with_tile_inc         @ 080c0936 35f08bfd
    subs r7,#0x1    @ 080c093a 013f
    cmp r7,#0x0                              @ 080c093c 002f
    bge LAB_080c088c                         @ 080c093e a5da
    .hword 0x4649    @ 080c0940 4946
    ldrh r0,[r1,#0x12]                       @ 080c0942 488a
    adds r0,#0x1    @ 080c0944 0130
    strh r0,[r1,#0x12]                       @ 080c0946 4882
    lsls r0,r0,#0x10    @ 080c0948 0004
    lsrs r0,r0,#0x10    @ 080c094a 000c
    cmp r0,#0xf                              @ 080c094c 0f28
    bls LAB_080c0a08                         @ 080c094e 5bd9
    bl disable_blend_and_clear_step          @ 080c0950 34f040fe
    ldr r1, PTR_BLDCNT_080c0970              @ 080c0954 0649
    movs r0,#0x90    @ 080c0956 9020
    strh r0,[r1,#0x0]                        @ 080c0958 0880
    movs r0,#0x0    @ 080c095a 0020
    .hword 0x464a    @ 080c095c 4a46
    strh r0,[r2,#0x12]                       @ 080c095e 5082
    ldrb r0,[r2,#0x10]                       @ 080c0960 107c
    adds r0,#0x1    @ 080c0962 0130
    strb r0,[r2,#0x10]                       @ 080c0964 1074
    b LAB_080c0a08                           @ 080c0966 4fe0
DAT_080c0968:
    .word  gBannerState                   @ 080c0968 c0fe0102
DAT_080c096c:
    .word  rom_sin_table_q8               @ 080c096c f0f8e509
PTR_BLDCNT_080c0970:
    .word  BLDCNT                         @ 080c0970 50000004
switchD_080c0808__caseD_2:
    movs r0,#0x5    @ 080c0974 0520
    movs r1,#0x90    @ 080c0976 9021
    bl tick_blend_step_with_bldcnt           @ 080c0978 34f076fe
    cmp r0,#0x0                              @ 080c097c 0028
    beq LAB_080c098e                         @ 080c097e 06d0
    ldr r1, DAT_080c0994                     @ 080c0980 0449
    ldrb r0,[r1,#0x10]                       @ 080c0982 087c
    adds r0,#0x1    @ 080c0984 0130
    strb r0,[r1,#0x10]                       @ 080c0986 0874
    movs r0,#0x21    @ 080c0988 2120
    bl sync_state_and_init_sprite            @ 080c098a 39f093f8
LAB_080c098e:
    movs r0,#0x0    @ 080c098e 0020
    b LAB_080c0a04                           @ 080c0990 38e0
    .zero  0x2
DAT_080c0994:
    .word  gBannerState                   @ 080c0994 c0fe0102
switchD_080c0808__caseD_3:
    movs r0,#0x5    @ 080c0998 0520
    movs r1,#0x90    @ 080c099a 9021
    bl clamp_blend_counter_to_target         @ 080c099c 34f02efe
    cmp r0,#0x0                              @ 080c09a0 0028
    beq LAB_080c09c8                         @ 080c09a2 11d0
    ldr r2, DAT_080c09cc                     @ 080c09a4 094a
    ldrh r0,[r2,#0x12]                       @ 080c09a6 508a
    adds r0,#0x1    @ 080c09a8 0130
    strh r0,[r2,#0x12]                       @ 080c09aa 5082
    lsls r0,r0,#0x10    @ 080c09ac 0004
    lsrs r0,r0,#0x10    @ 080c09ae 000c
    cmp r0,#0xf                              @ 080c09b0 0f28
    bls LAB_080c09c8                         @ 080c09b2 09d9
    movs r0,#0x0    @ 080c09b4 0020
    strh r0,[r2,#0x12]                       @ 080c09b6 5082
    ldr r1, PTR_BLDCNT_080c09d0              @ 080c09b8 0549
    movs r3,#0xfd    @ 080c09ba fd23
    lsls r3,r3,#0x6    @ 080c09bc 9b01
    adds r0,r3,#0x0    @ 080c09be 181c
    strh r0,[r1,#0x0]                        @ 080c09c0 0880
    ldrb r0,[r2,#0x10]                       @ 080c09c2 107c
    adds r0,#0x1    @ 080c09c4 0130
    strb r0,[r2,#0x10]                       @ 080c09c6 1074
LAB_080c09c8:
    movs r0,#0x0    @ 080c09c8 0020
    b LAB_080c0a04                           @ 080c09ca 1be0
DAT_080c09cc:
    .word  gBannerState                   @ 080c09cc c0fe0102
PTR_BLDCNT_080c09d0:
    .word  BLDCNT                         @ 080c09d0 50000004
switchD_080c0808__caseD_4:
    ldr r4, DAT_080c0a0c                     @ 080c09d4 0d4c
    ldrh r0,[r4,#0x12]                       @ 080c09d6 608a
    lsrs r1,r0,#0x1    @ 080c09d8 4108
    ldr r3, PTR_BLDALPHA_080c0a10            @ 080c09da 0d4b
    lsls r2,r1,#0x2    @ 080c09dc 8a00
    movs r0,#0x10    @ 080c09de 1020
    subs r0,r0,r2    @ 080c09e0 801a
    lsls r0,r0,#0x18    @ 080c09e2 0006
    lsrs r0,r0,#0x18    @ 080c09e4 000e
    lsls r1,r1,#0x1a    @ 080c09e6 8906
    lsrs r1,r1,#0x10    @ 080c09e8 090c
    orrs r0,r1    @ 080c09ea 0843
    strh r0,[r3,#0x0]                        @ 080c09ec 1880
    ldrh r0,[r4,#0x12]                       @ 080c09ee 608a
    adds r0,#0x1    @ 080c09f0 0130
    strh r0,[r4,#0x12]                       @ 080c09f2 6082
    lsls r0,r0,#0x10    @ 080c09f4 0004
    lsrs r0,r0,#0x10    @ 080c09f6 000c
    cmp r0,#0x7                              @ 080c09f8 0728
    bls LAB_080c0a02                         @ 080c09fa 02d9
    ldrb r0,[r4,#0x10]                       @ 080c09fc 207c
    adds r0,#0x1    @ 080c09fe 0130
    strb r0,[r4,#0x10]                       @ 080c0a00 2074
LAB_080c0a02:
    movs r0,#0x1    @ 080c0a02 0120
LAB_080c0a04:
    bl write_card_image_oam_grid             @ 080c0a04 fff7acfe
LAB_080c0a08:
    movs r0,#0x1    @ 080c0a08 0120
    b LAB_080c0a68                           @ 080c0a0a 2de0
DAT_080c0a0c:
    .word  gBannerState                   @ 080c0a0c c0fe0102
PTR_BLDALPHA_080c0a10:
    .word  BLDALPHA                       @ 080c0a10 52000004
switchD_080c0808__caseD_5:
    ldr r0, DAT_080c0a38                     @ 080c0a14 0848
    ldr r1, DAT_080c0a3c                     @ 080c0a16 0949
    movs r2,#0x80    @ 080c0a18 8022
    lsls r2,r2,#0x1    @ 080c0a1a 5200
    bl copy_bytes_by_halfword                @ 080c0a1c 34f042fa
    movs r2,#0x80    @ 080c0a20 8022
    lsls r2,r2,#0x13    @ 080c0a22 d204
    ldrh r1,[r2,#0x0]                        @ 080c0a24 1188
    ldr r0, DAT_080c0a40                     @ 080c0a26 0648
    ands r0,r1    @ 080c0a28 0840
LAB_080c0a2a:
    strh r0,[r2,#0x0]                        @ 080c0a2a 1080
    ldr r1, DAT_080c0a44                     @ 080c0a2c 0549
    ldrb r0,[r1,#0x10]                       @ 080c0a2e 087c
    adds r0,#0x1    @ 080c0a30 0130
    strb r0,[r1,#0x10]                       @ 080c0a32 0874
    b LAB_080c0a08                           @ 080c0a34 e8e7
    .zero  0x2
DAT_080c0a38:
    .word  0x05000300                     @ 080c0a38 00030005
DAT_080c0a3c:
    .word  0x08510460                     @ 080c0a3c 60045108
DAT_080c0a40:
    .word  0x0000dfff                     @ 080c0a40 ffdf0000
DAT_080c0a44:
    .word  gBannerState                   @ 080c0a44 c0fe0102
LAB_080c0a48:
    bl disable_blend_and_clear_step          @ 080c0a48 34f0c4fd
    movs r0,#0x2    @ 080c0a4c 0220
    rsbs r0,r0,#0    @ 080c0a4e 4042
    ldrb r1,[r4,#0x0]                        @ 080c0a50 2178
    ands r0,r1    @ 080c0a52 0840
    strb r0,[r4,#0x0]                        @ 080c0a54 2070
    ldr r1, DAT_080c0a78                     @ 080c0a56 0849
    ldr r2, DAT_080c0a7c                     @ 080c0a58 084a
    adds r1,r1,r2    @ 080c0a5a 8918
    movs r0,#0x5    @ 080c0a5c 0520
    rsbs r0,r0,#0    @ 080c0a5e 4042
    ldrb r3,[r1,#0x0]                        @ 080c0a60 0b78
    ands r0,r3    @ 080c0a62 1840
    strb r0,[r1,#0x0]                        @ 080c0a64 0870
    movs r0,#0x0    @ 080c0a66 0020
LAB_080c0a68:
    pop {r3,r4,r5}                           @ 080c0a68 38bc
    .hword 0x4698    @ 080c0a6a 9846
    .hword 0x46a1    @ 080c0a6c a146
    .hword 0x46aa    @ 080c0a6e aa46
    pop {r4,r5,r6,r7}                        @ 080c0a70 f0bc
    pop {r1}                                 @ 080c0a72 02bc
    bx r1                                    @ 080c0a74 0847
    .zero  0x2
DAT_080c0a78:
    .word  0x02023130                     @ 080c0a78 30310202
DAT_080c0a7c:
    .word  0x00000215                     @ 080c0a7c 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x34 子状态机, 待详细分析.
play_ui_effect_34:
    push {r4,r5,lr}                          @ 080c0a80 30b5
    ldr r4, DAT_080c0aa0                     @ 080c0a82 074c
    ldr r0,[r4,#0x8]                         @ 080c0a84 a068
    bl ensure_card_id_cache_entry            @ 080c0a86 0bf01fff
    adds r2,r0,#0x0    @ 080c0a8a 021c
    ldrb r0,[r4,#0x10]                       @ 080c0a8c 207c
    cmp r0,#0x5                              @ 080c0a8e 0528
    bls LAB_080c0a94                         @ 080c0a90 00d9
switchD_080c0a9c__default:
    b LAB_080c0c40                           @ 080c0a92 d5e0
LAB_080c0a94:
    lsls r0,r0,#0x2    @ 080c0a94 8000
    ldr r1, DAT_080c0aa4                     @ 080c0a96 0349
    adds r0,r0,r1    @ 080c0a98 4018
    ldr r0,[r0,#0x0]                         @ 080c0a9a 0068
switchD_080c0a9c__switchD:
    .hword 0x4687    @ 080c0a9c 8746
    .zero  0x2
DAT_080c0aa0:
    .word  gBannerState                   @ 080c0aa0 c0fe0102
DAT_080c0aa4:
    .word  0x080c0aa8                     @ 080c0aa4 a80a0c08
switchD_080c0a9c__switchdataD_080c0aa8:
    .word  0x080c0ac0                     @ 080c0aa8 c00a0c08
    .word  0x080c0b1c                     @ 080c0aac 1c0b0c08
    .word  0x080c0b6c                     @ 080c0ab0 6c0b0c08
    .word  0x080c0b90                     @ 080c0ab4 900b0c08
    .word  0x080c0bcc                     @ 080c0ab8 cc0b0c08
    .word  0x080c0c0c                     @ 080c0abc 0c0c0c08
switchD_080c0a9c__caseD_0:
    adds r0,r2,#0x0    @ 080c0ac0 101c
    bl render_card_display_with_type_gfx     @ 080c0ac2 fff777fd
    bl disable_blend_and_clear_step          @ 080c0ac6 34f085fd
    ldr r1, PTR_BLDALPHA_080c0b10            @ 080c0aca 1149
    movs r2,#0x80    @ 080c0acc 8022
    lsls r2,r2,#0x5    @ 080c0ace 5201
    adds r0,r2,#0x0    @ 080c0ad0 101c
    strh r0,[r1,#0x0]                        @ 080c0ad2 0880
    subs r1,#0x12    @ 080c0ad4 1239
    ldr r3, DAT_080c0b14                     @ 080c0ad6 0f4b
    adds r0,r3,#0x0    @ 080c0ad8 181c
    strh r0,[r1,#0x0]                        @ 080c0ada 0880
    adds r1,#0x4    @ 080c0adc 0431
    ldr r2, DAT_080c0b18                     @ 080c0ade 0e4a
    adds r0,r2,#0x0    @ 080c0ae0 101c
    strh r0,[r1,#0x0]                        @ 080c0ae2 0880
    adds r1,#0x4    @ 080c0ae4 0431
    movs r0,#0x3f    @ 080c0ae6 3f20
    strh r0,[r1,#0x0]                        @ 080c0ae8 0880
    adds r1,#0x2    @ 080c0aea 0231
    movs r0,#0x1f    @ 080c0aec 1f20
    strh r0,[r1,#0x0]                        @ 080c0aee 0880
    adds r1,#0x6    @ 080c0af0 0631
    movs r3,#0xfd    @ 080c0af2 fd23
    lsls r3,r3,#0x6    @ 080c0af4 9b01
    adds r0,r3,#0x0    @ 080c0af6 181c
    strh r0,[r1,#0x0]                        @ 080c0af8 0880
    adds r1,#0x4    @ 080c0afa 0431
    movs r0,#0x0    @ 080c0afc 0020
    strh r0,[r1,#0x0]                        @ 080c0afe 0880
    movs r2,#0x80    @ 080c0b00 8022
    lsls r2,r2,#0x13    @ 080c0b02 d204
    ldrh r0,[r2,#0x0]                        @ 080c0b04 1088
    movs r3,#0x80    @ 080c0b06 8023
    lsls r3,r3,#0x6    @ 080c0b08 9b01
    adds r1,r3,#0x0    @ 080c0b0a 191c
    orrs r0,r1    @ 080c0b0c 0843
    b LAB_080c0c22                           @ 080c0b0e 88e0
PTR_BLDALPHA_080c0b10:
    .word  BLDALPHA                       @ 080c0b10 52000004
DAT_080c0b14:
    .word  0x00005abe                     @ 080c0b14 be5a0000
DAT_080c0b18:
    .word  0x0000028e                     @ 080c0b18 8e020000
switchD_080c0a9c__caseD_1:
    ldr r5, DAT_080c0b60                     @ 080c0b1c 104d
    ldrh r0,[r5,#0x12]                       @ 080c0b1e 688a
    lsrs r4,r0,#0x1    @ 080c0b20 4408
    ldr r3, PTR_BLDALPHA_080c0b64            @ 080c0b22 104b
    lsls r2,r4,#0x2    @ 080c0b24 a200
    lsls r1,r4,#0x1a    @ 080c0b26 a106
    lsrs r1,r1,#0x18    @ 080c0b28 090e
    movs r0,#0x10    @ 080c0b2a 1020
    subs r0,r0,r2    @ 080c0b2c 801a
    lsls r0,r0,#0x18    @ 080c0b2e 0006
    lsrs r0,r0,#0x10    @ 080c0b30 000c
    orrs r1,r0    @ 080c0b32 0143
    strh r1,[r3,#0x0]                        @ 080c0b34 1980
    movs r0,#0x1    @ 080c0b36 0120
    bl write_card_image_oam_grid             @ 080c0b38 fff712fe
    ldrh r0,[r5,#0x12]                       @ 080c0b3c 688a
    adds r0,#0x1    @ 080c0b3e 0130
    strh r0,[r5,#0x12]                       @ 080c0b40 6882
    lsls r0,r0,#0x10    @ 080c0b42 0004
    lsrs r0,r0,#0x10    @ 080c0b44 000c
    cmp r0,#0x7                              @ 080c0b46 0728
    bls LAB_080c0c00                         @ 080c0b48 5ad9
    bl disable_blend_and_clear_step          @ 080c0b4a 34f043fd
    ldr r1, PTR_BLDCNT_080c0b68              @ 080c0b4e 0649
    movs r0,#0x90    @ 080c0b50 9020
    strh r0,[r1,#0x0]                        @ 080c0b52 0880
    movs r0,#0x0    @ 080c0b54 0020
    strh r0,[r5,#0x12]                       @ 080c0b56 6882
    ldrb r0,[r5,#0x10]                       @ 080c0b58 287c
    adds r0,#0x1    @ 080c0b5a 0130
    strb r0,[r5,#0x10]                       @ 080c0b5c 2874
    b LAB_080c0c00                           @ 080c0b5e 4fe0
DAT_080c0b60:
    .word  gBannerState                   @ 080c0b60 c0fe0102
PTR_BLDALPHA_080c0b64:
    .word  BLDALPHA                       @ 080c0b64 52000004
PTR_BLDCNT_080c0b68:
    .word  BLDCNT                         @ 080c0b68 50000004
switchD_080c0a9c__caseD_2:
    movs r0,#0x5    @ 080c0b6c 0520
    movs r1,#0x90    @ 080c0b6e 9021
    bl tick_blend_step_with_bldcnt           @ 080c0b70 34f07afd
    cmp r0,#0x0                              @ 080c0b74 0028
    beq LAB_080c0b86                         @ 080c0b76 06d0
    ldr r1, DAT_080c0b8c                     @ 080c0b78 0449
    ldrb r0,[r1,#0x10]                       @ 080c0b7a 087c
    adds r0,#0x1    @ 080c0b7c 0130
    strb r0,[r1,#0x10]                       @ 080c0b7e 0874
    movs r0,#0x21    @ 080c0b80 2120
    bl sync_state_and_init_sprite            @ 080c0b82 38f097ff
LAB_080c0b86:
    movs r0,#0x0    @ 080c0b86 0020
    b LAB_080c0bfc                           @ 080c0b88 38e0
    .zero  0x2
DAT_080c0b8c:
    .word  gBannerState                   @ 080c0b8c c0fe0102
switchD_080c0a9c__caseD_3:
    movs r0,#0x5    @ 080c0b90 0520
    movs r1,#0x90    @ 080c0b92 9021
    bl clamp_blend_counter_to_target         @ 080c0b94 34f032fd
    cmp r0,#0x0                              @ 080c0b98 0028
    beq LAB_080c0bc0                         @ 080c0b9a 11d0
    ldr r2, DAT_080c0bc4                     @ 080c0b9c 094a
    ldrh r0,[r2,#0x12]                       @ 080c0b9e 508a
    adds r0,#0x1    @ 080c0ba0 0130
    strh r0,[r2,#0x12]                       @ 080c0ba2 5082
    lsls r0,r0,#0x10    @ 080c0ba4 0004
    lsrs r0,r0,#0x10    @ 080c0ba6 000c
    cmp r0,#0xf                              @ 080c0ba8 0f28
    bls LAB_080c0bc0                         @ 080c0baa 09d9
    movs r0,#0x0    @ 080c0bac 0020
    strh r0,[r2,#0x12]                       @ 080c0bae 5082
    ldr r1, PTR_BLDCNT_080c0bc8              @ 080c0bb0 0549
    movs r3,#0xfd    @ 080c0bb2 fd23
    lsls r3,r3,#0x6    @ 080c0bb4 9b01
    adds r0,r3,#0x0    @ 080c0bb6 181c
    strh r0,[r1,#0x0]                        @ 080c0bb8 0880
    ldrb r0,[r2,#0x10]                       @ 080c0bba 107c
    adds r0,#0x1    @ 080c0bbc 0130
    strb r0,[r2,#0x10]                       @ 080c0bbe 1074
LAB_080c0bc0:
    movs r0,#0x0    @ 080c0bc0 0020
    b LAB_080c0bfc                           @ 080c0bc2 1be0
DAT_080c0bc4:
    .word  gBannerState                   @ 080c0bc4 c0fe0102
PTR_BLDCNT_080c0bc8:
    .word  BLDCNT                         @ 080c0bc8 50000004
switchD_080c0a9c__caseD_4:
    ldr r3, DAT_080c0c04                     @ 080c0bcc 0d4b
    ldrh r0,[r3,#0x12]                       @ 080c0bce 588a
    lsrs r4,r0,#0x1    @ 080c0bd0 4408
    ldr r2, PTR_BLDALPHA_080c0c08            @ 080c0bd2 0d4a
    lsls r1,r4,#0x2    @ 080c0bd4 a100
    movs r0,#0x10    @ 080c0bd6 1020
    subs r0,r0,r1    @ 080c0bd8 401a
    lsls r0,r0,#0x18    @ 080c0bda 0006
    lsrs r0,r0,#0x18    @ 080c0bdc 000e
    lsls r1,r4,#0x1a    @ 080c0bde a106
    lsrs r1,r1,#0x10    @ 080c0be0 090c
    orrs r0,r1    @ 080c0be2 0843
    strh r0,[r2,#0x0]                        @ 080c0be4 1080
    ldrh r0,[r3,#0x12]                       @ 080c0be6 588a
    adds r0,#0x1    @ 080c0be8 0130
    strh r0,[r3,#0x12]                       @ 080c0bea 5882
    lsls r0,r0,#0x10    @ 080c0bec 0004
    lsrs r0,r0,#0x10    @ 080c0bee 000c
    cmp r0,#0x7                              @ 080c0bf0 0728
    bls LAB_080c0bfa                         @ 080c0bf2 02d9
    ldrb r0,[r3,#0x10]                       @ 080c0bf4 187c
    adds r0,#0x1    @ 080c0bf6 0130
    strb r0,[r3,#0x10]                       @ 080c0bf8 1874
LAB_080c0bfa:
    movs r0,#0x1    @ 080c0bfa 0120
LAB_080c0bfc:
    bl write_card_image_oam_grid             @ 080c0bfc fff7b0fd
LAB_080c0c00:
    movs r0,#0x1    @ 080c0c00 0120
    b LAB_080c0c60                           @ 080c0c02 2de0
DAT_080c0c04:
    .word  gBannerState                   @ 080c0c04 c0fe0102
PTR_BLDALPHA_080c0c08:
    .word  BLDALPHA                       @ 080c0c08 52000004
switchD_080c0a9c__caseD_5:
    ldr r0, DAT_080c0c30                     @ 080c0c0c 0848
    ldr r1, DAT_080c0c34                     @ 080c0c0e 0949
    movs r2,#0x80    @ 080c0c10 8022
    lsls r2,r2,#0x1    @ 080c0c12 5200
    bl copy_bytes_by_halfword                @ 080c0c14 34f046f9
    movs r2,#0x80    @ 080c0c18 8022
    lsls r2,r2,#0x13    @ 080c0c1a d204
    ldrh r1,[r2,#0x0]                        @ 080c0c1c 1188
    ldr r0, DAT_080c0c38                     @ 080c0c1e 0648
    ands r0,r1    @ 080c0c20 0840
LAB_080c0c22:
    strh r0,[r2,#0x0]                        @ 080c0c22 1080
    ldr r1, DAT_080c0c3c                     @ 080c0c24 0549
    ldrb r0,[r1,#0x10]                       @ 080c0c26 087c
    adds r0,#0x1    @ 080c0c28 0130
    strb r0,[r1,#0x10]                       @ 080c0c2a 0874
    b LAB_080c0c00                           @ 080c0c2c e8e7
    .zero  0x2
DAT_080c0c30:
    .word  0x05000300                     @ 080c0c30 00030005
DAT_080c0c34:
    .word  0x08510460                     @ 080c0c34 60045108
DAT_080c0c38:
    .word  0x0000dfff                     @ 080c0c38 ffdf0000
DAT_080c0c3c:
    .word  gBannerState                   @ 080c0c3c c0fe0102
LAB_080c0c40:
    bl disable_blend_and_clear_step          @ 080c0c40 34f0c8fc
    movs r0,#0x2    @ 080c0c44 0220
    rsbs r0,r0,#0    @ 080c0c46 4042
    ldrb r1,[r4,#0x0]                        @ 080c0c48 2178
    ands r0,r1    @ 080c0c4a 0840
    strb r0,[r4,#0x0]                        @ 080c0c4c 2070
    ldr r1, DAT_080c0c68                     @ 080c0c4e 0649
    ldr r2, DAT_080c0c6c                     @ 080c0c50 064a
    adds r1,r1,r2    @ 080c0c52 8918
    movs r0,#0x5    @ 080c0c54 0520
    rsbs r0,r0,#0    @ 080c0c56 4042
    ldrb r3,[r1,#0x0]                        @ 080c0c58 0b78
    ands r0,r3    @ 080c0c5a 1840
    strb r0,[r1,#0x0]                        @ 080c0c5c 0870
    movs r0,#0x0    @ 080c0c5e 0020
LAB_080c0c60:
    pop {r4,r5}                              @ 080c0c60 30bc
    pop {r1}                                 @ 080c0c62 02bc
    bx r1                                    @ 080c0c64 0847
    .zero  0x2
DAT_080c0c68:
    .word  0x02023130                     @ 080c0c68 30310202
DAT_080c0c6c:
    .word  0x00000215                     @ 080c0c6c 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x20 子状态机, 待详细分析.
play_ui_effect_20:
    push {r4,r5,r6,r7,lr}                    @ 080c0c70 f0b5
    .hword 0x4657    @ 080c0c72 5746
    .hword 0x464e    @ 080c0c74 4e46
    .hword 0x4645    @ 080c0c76 4546
    push {r5,r6,r7}                          @ 080c0c78 e0b4
    ldr r4, DAT_080c0cbc                     @ 080c0c7a 104c
    subs r4,#0x4    @ 080c0c7c 043c
    ldr r6,[r4,#0x8]                         @ 080c0c7e a668
    ldr r7,[r4,#0xc]                         @ 080c0c80 e768
    movs r0,#0x7c    @ 080c0c82 7c20
    .hword 0x4681    @ 080c0c84 8146
    movs r5,#0x30    @ 080c0c86 3025
    movs r1,#0x80    @ 080c0c88 8021
    lsls r1,r1,#0x2    @ 080c0c8a 8900
    .hword 0x4688    @ 080c0c8c 8846
    adds r0,r7,#0x0    @ 080c0c8e 381c
    bl ensure_card_id_cache_entry            @ 080c0c90 0bf01afe
    .hword 0x4682    @ 080c0c94 8246
    cmp r7,#0x0                              @ 080c0c96 002f
    bne LAB_080c0ca8                         @ 080c0c98 06d1
    lsls r0,r6,#0x10    @ 080c0c9a 3004
    lsrs r0,r0,#0x10    @ 080c0c9c 000c
    bl internal_card_id_to_card_id           @ 080c0c9e 2df065fd
    lsls r0,r0,#0x10    @ 080c0ca2 0004
    lsrs r0,r0,#0x10    @ 080c0ca4 000c
    .hword 0x4682    @ 080c0ca6 8246
LAB_080c0ca8:
    ldrb r0,[r4,#0x10]                       @ 080c0ca8 207c
    cmp r0,#0x6                              @ 080c0caa 0628
    bls LAB_080c0cb0                         @ 080c0cac 00d9
switchD_080c0cb8__default:
    b LAB_080c0f04                           @ 080c0cae 29e1
LAB_080c0cb0:
    lsls r0,r0,#0x2    @ 080c0cb0 8000
    ldr r1, DAT_080c0cc0                     @ 080c0cb2 0349
    adds r0,r0,r1    @ 080c0cb4 4018
    ldr r0,[r0,#0x0]                         @ 080c0cb6 0068
switchD_080c0cb8__switchD:
    .hword 0x4687    @ 080c0cb8 8746
    .zero  0x2
DAT_080c0cbc:
    .word  0x0201fec4                     @ 080c0cbc c4fe0102
DAT_080c0cc0:
    .word  0x080c0cc4                     @ 080c0cc0 c40c0c08
switchD_080c0cb8__switchdataD_080c0cc4:
    .word  0x080c0ce0                     @ 080c0cc4 e00c0c08
    .word  0x080c0da4                     @ 080c0cc8 a40d0c08
    .word  0x080c0dd4                     @ 080c0ccc d40d0c08
    .word  0x080c0e20                     @ 080c0cd0 200e0c08
    .word  0x080c0e6c                     @ 080c0cd4 6c0e0c08
    .word  0x080c0eac                     @ 080c0cd8 ac0e0c08
    .word  0x080c0edc                     @ 080c0cdc dc0e0c08
switchD_080c0cb8__caseD_0:
    .hword 0x4652    @ 080c0ce0 5246
    lsls r0,r2,#0x10    @ 080c0ce2 1004
    lsrs r0,r0,#0x10    @ 080c0ce4 000c
    movs r1,#0x80    @ 080c0ce6 8021
    lsls r1,r1,#0x2    @ 080c0ce8 8900
    bl blit_card_frame_tile_row_to_vram      @ 080c0cea 02f01bf8
    ldr r0, DAT_080c0d7c                     @ 080c0cee 2348
    ldr r1, DAT_080c0d80                     @ 080c0cf0 2349
    movs r2,#0x10    @ 080c0cf2 1022
    movs r3,#0x2    @ 080c0cf4 0223
    bl tile_2d_row_copy                      @ 080c0cf6 36f0edfb
    ldr r4, DAT_080c0d84                     @ 080c0cfa 224c
    ldr r1, DAT_080c0d88                     @ 080c0cfc 2249
    movs r2,#0x82    @ 080c0cfe 8222
    lsls r2,r2,#0x12    @ 080c0d00 9204
    adds r0,r4,#0x0    @ 080c0d02 201c
    movs r3,#0x1    @ 080c0d04 0123
    bl init_aob_ctx_from_ptnsect             @ 080c0d06 37f04df8
    movs r0,#0x1    @ 080c0d0a 0120
    ldrb r3,[r4,#0x13]                       @ 080c0d0c e37c
    orrs r0,r3    @ 080c0d0e 1843
    strb r0,[r4,#0x13]                       @ 080c0d10 e074
    adds r0,r4,#0x0    @ 080c0d12 201c
    movs r1,#0x0    @ 080c0d14 0021
    movs r2,#0x0    @ 080c0d16 0022
    bl init_aob_ctx_with_anm_entry           @ 080c0d18 37f096f8
    ldr r1, PTR_WIN0H_080c0d8c               @ 080c0d1c 1b49
    ldr r2, DAT_080c0d90                     @ 080c0d1e 1c4a
    adds r0,r2,#0x0    @ 080c0d20 101c
    strh r0,[r1,#0x0]                        @ 080c0d22 0880
    ldr r2, PTR_WIN0V_080c0d94               @ 080c0d24 1b4a
    adds r1,r5,#0x0    @ 080c0d26 291c
    adds r1,#0x38    @ 080c0d28 3831
    lsls r1,r1,#0x18    @ 080c0d2a 0906
    lsrs r1,r1,#0x18    @ 080c0d2c 090e
    adds r0,r5,#0x0    @ 080c0d2e 281c
    subs r0,#0x8    @ 080c0d30 0838
    lsls r0,r0,#0x18    @ 080c0d32 0006
    lsrs r0,r0,#0x10    @ 080c0d34 000c
    orrs r1,r0    @ 080c0d36 0143
    strh r1,[r2,#0x0]                        @ 080c0d38 1180
    ldr r1, PTR_WININ_080c0d98               @ 080c0d3a 1749
    movs r0,#0x3f    @ 080c0d3c 3f20
    strh r0,[r1,#0x0]                        @ 080c0d3e 0880
    adds r1,#0x2    @ 080c0d40 0231
    movs r0,#0x1f    @ 080c0d42 1f20
    strh r0,[r1,#0x0]                        @ 080c0d44 0880
    adds r1,#0x6    @ 080c0d46 0631
    movs r0,#0xef    @ 080c0d48 ef20
    strh r0,[r1,#0x0]                        @ 080c0d4a 0880
    adds r1,#0x4    @ 080c0d4c 0431
    movs r0,#0x0    @ 080c0d4e 0020
    strh r0,[r1,#0x0]                        @ 080c0d50 0880
    subs r2,#0x44    @ 080c0d52 443a
    ldrh r0,[r2,#0x0]                        @ 080c0d54 1088
    movs r3,#0x80    @ 080c0d56 8023
    lsls r3,r3,#0x6    @ 080c0d58 9b01
    adds r1,r3,#0x0    @ 080c0d5a 191c
    orrs r0,r1    @ 080c0d5c 0843
    strh r0,[r2,#0x0]                        @ 080c0d5e 1080
    movs r0,#0x40    @ 080c0d60 4020
    ldr r1, DAT_080c0d9c                     @ 080c0d62 0e49
    ldrb r1,[r1,#0x1]                        @ 080c0d64 4978
    orrs r0,r1    @ 080c0d66 0843
    ldr r2, DAT_080c0d9c                     @ 080c0d68 0c4a
    strb r0,[r2,#0x1]                        @ 080c0d6a 5070
    ldr r0, DAT_080c0da0                     @ 080c0d6c 0c48
    strh r7,[r0,#0x8]                        @ 080c0d6e 0781
    .hword 0x4650    @ 080c0d70 5046
    ldr r1, DAT_080c0d9c                     @ 080c0d72 0a49
    movs r2,#0x1    @ 080c0d74 0122
    bl render_large_card_display_by_mode     @ 080c0d76 0af029fa
    b LAB_080c0ef0                           @ 080c0d7a b9e0
DAT_080c0d7c:
    .word  0x06014100                     @ 080c0d7c 00410106
DAT_080c0d80:
    .word  0x098a4a48                     @ 080c0d80 484a8a09
DAT_080c0d84:
    .word  0x0201fedc                     @ 080c0d84 dcfe0102
DAT_080c0d88:
    .word  0x098a4e48                     @ 080c0d88 484e8a09
PTR_WIN0H_080c0d8c:
    .word  WIN0H                          @ 080c0d8c 40000004
DAT_080c0d90:
    .word  0x000028f0                     @ 080c0d90 f0280000
PTR_WIN0V_080c0d94:
    .word  WIN0V                          @ 080c0d94 44000004
PTR_WININ_080c0d98:
    .word  WININ                          @ 080c0d98 48000004
DAT_080c0d9c:
    .word  0x0201fec4                     @ 080c0d9c c4fe0102
DAT_080c0da0:
    .word  0x02023130                     @ 080c0da0 30310202
switchD_080c0cb8__caseD_1:
    ldr r1, PTR_BLDY_080c0dcc                @ 080c0da4 0949
    ldr r2, DAT_080c0dd0                     @ 080c0da6 0a4a
    ldrb r3,[r2,#0x11]                       @ 080c0da8 537c
    lsls r0,r3,#0x1    @ 080c0daa 5800
    strh r0,[r1,#0x0]                        @ 080c0dac 0880
    ldrb r0,[r2,#0x11]                       @ 080c0dae 507c
    adds r0,#0x1    @ 080c0db0 0130
    strb r0,[r2,#0x11]                       @ 080c0db2 5074
    lsls r0,r0,#0x18    @ 080c0db4 0006
    lsrs r0,r0,#0x18    @ 080c0db6 000e
    cmp r0,#0x4                              @ 080c0db8 0428
    bhi LAB_080c0dbe                         @ 080c0dba 00d8
    b LAB_080c0ef8                           @ 080c0dbc 9ce0
LAB_080c0dbe:
    ldrb r0,[r2,#0x10]                       @ 080c0dbe 107c
    adds r0,#0x1    @ 080c0dc0 0130
    strb r0,[r2,#0x10]                       @ 080c0dc2 1074
    movs r0,#0x0    @ 080c0dc4 0020
    strb r0,[r2,#0x11]                       @ 080c0dc6 5074
    b LAB_080c0ef8                           @ 080c0dc8 96e0
    .zero  0x2
PTR_BLDY_080c0dcc:
    .word  BLDY                           @ 080c0dcc 54000004
DAT_080c0dd0:
    .word  gBannerState                   @ 080c0dd0 c0fe0102
switchD_080c0cb8__caseD_2:
    lsls r0,r5,#0x10    @ 080c0dd4 2804
    .hword 0x4649    @ 080c0dd6 4946
    orrs r0,r1    @ 080c0dd8 0843
    .hword 0x4643    @ 080c0dda 4346
    lsrs r2,r3,#0x1    @ 080c0ddc 5a08
    movs r1,#0x80    @ 080c0dde 8021
    bl write_oam_entry_with_tile_inc         @ 080c0de0 35f036fb
    .hword 0x4642    @ 080c0de4 4246
    adds r2,#0x80    @ 080c0de6 8032
    adds r5,#0x20    @ 080c0de8 2035
    lsls r0,r5,#0x10    @ 080c0dea 2804
    .hword 0x4649    @ 080c0dec 4946
    orrs r0,r1    @ 080c0dee 0843
    movs r1,#0x81    @ 080c0df0 8121
    lsls r1,r1,#0x7    @ 080c0df2 c901
    lsrs r2,r2,#0x1    @ 080c0df4 5208
    bl write_oam_entry_with_tile_inc         @ 080c0df6 35f02bfb
    ldr r1, DAT_080c0e1c                     @ 080c0dfa 0849
    ldrb r0,[r1,#0x11]                       @ 080c0dfc 487c
    adds r0,#0x1    @ 080c0dfe 0130
    strb r0,[r1,#0x11]                       @ 080c0e00 4874
    lsls r0,r0,#0x18    @ 080c0e02 0006
    lsrs r0,r0,#0x18    @ 080c0e04 000e
    cmp r0,#0x10                             @ 080c0e06 1028
    bls LAB_080c0ef8                         @ 080c0e08 76d9
    movs r0,#0x0    @ 080c0e0a 0020
    strb r0,[r1,#0x11]                       @ 080c0e0c 4874
    ldrb r0,[r1,#0x10]                       @ 080c0e0e 087c
    adds r0,#0x1    @ 080c0e10 0130
    strb r0,[r1,#0x10]                       @ 080c0e12 0874
    movs r0,#0xa    @ 080c0e14 0a20
    bl sync_state_and_init_sprite            @ 080c0e16 38f04dfe
    b LAB_080c0ef8                           @ 080c0e1a 6de0
DAT_080c0e1c:
    .word  gBannerState                   @ 080c0e1c c0fe0102
switchD_080c0cb8__caseD_3:
    ldr r6, DAT_080c0e68                     @ 080c0e20 114e
    lsls r4,r5,#0x10    @ 080c0e22 2c04
    .hword 0x464a    @ 080c0e24 4a46
    orrs r4,r2    @ 080c0e26 1443
    adds r0,r6,#0x0    @ 080c0e28 301c
    adds r1,r4,#0x0    @ 080c0e2a 211c
    movs r2,#0x0    @ 080c0e2c 0022
    movs r3,#0x0    @ 080c0e2e 0023
    bl render_aob_frame_to_oam               @ 080c0e30 37f0e6f8
    .hword 0x4643    @ 080c0e34 4346
    lsrs r2,r3,#0x1    @ 080c0e36 5a08
    adds r0,r4,#0x0    @ 080c0e38 201c
    movs r1,#0x80    @ 080c0e3a 8021
    bl write_oam_entry_with_tile_inc         @ 080c0e3c 35f008fb
    .hword 0x4642    @ 080c0e40 4246
    adds r2,#0x80    @ 080c0e42 8032
    adds r5,#0x20    @ 080c0e44 2035
    lsls r0,r5,#0x10    @ 080c0e46 2804
    .hword 0x4649    @ 080c0e48 4946
    orrs r0,r1    @ 080c0e4a 0843
    movs r1,#0x81    @ 080c0e4c 8121
    lsls r1,r1,#0x7    @ 080c0e4e c901
    lsrs r2,r2,#0x1    @ 080c0e50 5208
    bl write_oam_entry_with_tile_inc         @ 080c0e52 35f0fdfa
    adds r0,r6,#0x0    @ 080c0e56 301c
    bl tick_aob_frame_counter                @ 080c0e58 37f056f8
    cmp r0,#0x0                              @ 080c0e5c 0028
    bne LAB_080c0ef8                         @ 080c0e5e 4bd1
    adds r1,r6,#0x0    @ 080c0e60 311c
    subs r1,#0x1c    @ 080c0e62 1c39
    b LAB_080c0ef2                           @ 080c0e64 45e0
    .zero  0x2
DAT_080c0e68:
    .word  0x0201fedc                     @ 080c0e68 dcfe0102
switchD_080c0cb8__caseD_4:
    lsls r0,r5,#0x10    @ 080c0e6c 2804
    .hword 0x464a    @ 080c0e6e 4a46
    orrs r0,r2    @ 080c0e70 1043
    .hword 0x4643    @ 080c0e72 4346
    lsrs r2,r3,#0x1    @ 080c0e74 5a08
    movs r1,#0x80    @ 080c0e76 8021
    bl write_oam_entry_with_tile_inc         @ 080c0e78 35f0eafa
    .hword 0x4642    @ 080c0e7c 4246
    adds r2,#0x80    @ 080c0e7e 8032
    adds r5,#0x20    @ 080c0e80 2035
    lsls r0,r5,#0x10    @ 080c0e82 2804
    .hword 0x4649    @ 080c0e84 4946
    orrs r0,r1    @ 080c0e86 0843
    movs r1,#0x81    @ 080c0e88 8121
    lsls r1,r1,#0x7    @ 080c0e8a c901
    lsrs r2,r2,#0x1    @ 080c0e8c 5208
    bl write_oam_entry_with_tile_inc         @ 080c0e8e 35f0dffa
    ldr r1, DAT_080c0ea8                     @ 080c0e92 0549
    ldrb r0,[r1,#0x11]                       @ 080c0e94 487c
    adds r0,#0x1    @ 080c0e96 0130
    strb r0,[r1,#0x11]                       @ 080c0e98 4874
    lsls r0,r0,#0x18    @ 080c0e9a 0006
    lsrs r0,r0,#0x18    @ 080c0e9c 000e
    cmp r0,#0x10                             @ 080c0e9e 1028
    bls LAB_080c0ef8                         @ 080c0ea0 2ad9
    movs r0,#0x0    @ 080c0ea2 0020
    strb r0,[r1,#0x11]                       @ 080c0ea4 4874
    b LAB_080c0ef2                           @ 080c0ea6 24e0
DAT_080c0ea8:
    .word  gBannerState                   @ 080c0ea8 c0fe0102
switchD_080c0cb8__caseD_5:
    ldr r2, PTR_BLDY_080c0ed4                @ 080c0eac 094a
    ldr r3, DAT_080c0ed8                     @ 080c0eae 0a4b
    ldrb r0,[r3,#0x11]                       @ 080c0eb0 587c
    lsls r1,r0,#0x1    @ 080c0eb2 4100
    movs r0,#0x8    @ 080c0eb4 0820
    subs r0,r0,r1    @ 080c0eb6 401a
    strh r0,[r2,#0x0]                        @ 080c0eb8 1080
    ldrb r0,[r3,#0x11]                       @ 080c0eba 587c
    adds r0,#0x1    @ 080c0ebc 0130
    strb r0,[r3,#0x11]                       @ 080c0ebe 5874
    lsls r0,r0,#0x18    @ 080c0ec0 0006
    lsrs r0,r0,#0x18    @ 080c0ec2 000e
    cmp r0,#0x4                              @ 080c0ec4 0428
    bls LAB_080c0ef8                         @ 080c0ec6 17d9
    ldrb r0,[r3,#0x10]                       @ 080c0ec8 187c
    adds r0,#0x1    @ 080c0eca 0130
    strb r0,[r3,#0x10]                       @ 080c0ecc 1874
    movs r0,#0x0    @ 080c0ece 0020
    strb r0,[r3,#0x11]                       @ 080c0ed0 5874
    b LAB_080c0ef8                           @ 080c0ed2 11e0
PTR_BLDY_080c0ed4:
    .word  BLDY                           @ 080c0ed4 54000004
DAT_080c0ed8:
    .word  gBannerState                   @ 080c0ed8 c0fe0102
switchD_080c0cb8__caseD_6:
    movs r2,#0x80    @ 080c0edc 8022
    lsls r2,r2,#0x13    @ 080c0ede d204
    ldrh r1,[r2,#0x0]                        @ 080c0ee0 1188
    ldr r0, DAT_080c0efc                     @ 080c0ee2 0648
    ands r0,r1    @ 080c0ee4 0840
    strh r0,[r2,#0x0]                        @ 080c0ee6 1080
    bl disable_blend_and_clear_step          @ 080c0ee8 34f074fb
    bl refresh_duel_field_zone_info          @ 080c0eec 0bf00ef8
LAB_080c0ef0:
    ldr r1, DAT_080c0f00                     @ 080c0ef0 0349
LAB_080c0ef2:
    ldrb r0,[r1,#0x10]                       @ 080c0ef2 087c
    adds r0,#0x1    @ 080c0ef4 0130
    strb r0,[r1,#0x10]                       @ 080c0ef6 0874
LAB_080c0ef8:
    movs r0,#0x1    @ 080c0ef8 0120
    b LAB_080c0f20                           @ 080c0efa 11e0
DAT_080c0efc:
    .word  0x0000dfff                     @ 080c0efc ffdf0000
DAT_080c0f00:
    .word  gBannerState                   @ 080c0f00 c0fe0102
LAB_080c0f04:
    movs r0,#0x2    @ 080c0f04 0220
    rsbs r0,r0,#0    @ 080c0f06 4042
    ldrb r1,[r4,#0x0]                        @ 080c0f08 2178
    ands r0,r1    @ 080c0f0a 0840
    strb r0,[r4,#0x0]                        @ 080c0f0c 2070
    ldr r1, DAT_080c0f30                     @ 080c0f0e 0849
    ldr r2, DAT_080c0f34                     @ 080c0f10 084a
    adds r1,r1,r2    @ 080c0f12 8918
    movs r0,#0x5    @ 080c0f14 0520
    rsbs r0,r0,#0    @ 080c0f16 4042
    ldrb r3,[r1,#0x0]                        @ 080c0f18 0b78
    ands r0,r3    @ 080c0f1a 1840
    strb r0,[r1,#0x0]                        @ 080c0f1c 0870
    movs r0,#0x0    @ 080c0f1e 0020
LAB_080c0f20:
    pop {r3,r4,r5}                           @ 080c0f20 38bc
    .hword 0x4698    @ 080c0f22 9846
    .hword 0x46a1    @ 080c0f24 a146
    .hword 0x46aa    @ 080c0f26 aa46
    pop {r4,r5,r6,r7}                        @ 080c0f28 f0bc
    pop {r1}                                 @ 080c0f2a 02bc
    bx r1                                    @ 080c0f2c 0847
    .zero  0x2
DAT_080c0f30:
    .word  0x02023130                     @ 080c0f30 30310202
DAT_080c0f34:
    .word  0x00000215                     @ 080c0f34 15020000

@ 占位名 - play_ui_effect (FUN_0801ef94) case 0x21 子状态机, 待详细分析.
play_ui_effect_21:
    push {r4,r5,r6,r7,lr}                    @ 080c0f38 f0b5
    .hword 0x464f    @ 080c0f3a 4f46
    .hword 0x4646    @ 080c0f3c 4646
    push {r6,r7}                             @ 080c0f3e c0b4
    ldr r7, DAT_080c0f94                     @ 080c0f40 144f
    ldr r4,[r7,#0x4]                         @ 080c0f42 7c68
    ldr r5,[r7,#0x8]                         @ 080c0f44 bd68
    ldr r6,[r7,#0xc]                         @ 080c0f46 fe68
    adds r0,r4,#0x0    @ 080c0f48 201c
    adds r1,r5,#0x0    @ 080c0f4a 291c
    adds r2,r6,#0x0    @ 080c0f4c 321c
    bl get_zone_slot_entity_ref_by_type      @ 080c0f4e 7af72bfa
    .hword 0x4680    @ 080c0f52 8046
    adds r0,r4,#0x0    @ 080c0f54 201c
    adds r1,r5,#0x0    @ 080c0f56 291c
    adds r2,r6,#0x0    @ 080c0f58 321c
    bl get_zone_slot_card_ref_by_type        @ 080c0f5a 7af7a9fa
    adds r4,r0,#0x0    @ 080c0f5e 041c
    bl ensure_card_id_cache_entry            @ 080c0f60 0bf0b2fc
    adds r2,r0,#0x0    @ 080c0f64 021c
    movs r5,#0x7c    @ 080c0f66 7c25
    movs r6,#0x30    @ 080c0f68 3026
    movs r0,#0x80    @ 080c0f6a 8020
    lsls r0,r0,#0x2    @ 080c0f6c 8000
    .hword 0x4681    @ 080c0f6e 8146
    cmp r4,#0x0                              @ 080c0f70 002c
    bne LAB_080c0f82                         @ 080c0f72 06d1
    .hword 0x4641    @ 080c0f74 4146
    lsls r0,r1,#0x10    @ 080c0f76 0804
    lsrs r0,r0,#0x10    @ 080c0f78 000c
    bl internal_card_id_to_card_id           @ 080c0f7a 2df0f7fb
    lsls r0,r0,#0x10    @ 080c0f7e 0004
    lsrs r2,r0,#0x10    @ 080c0f80 020c
LAB_080c0f82:
    ldrb r0,[r7,#0x10]                       @ 080c0f82 387c
    cmp r0,#0x6                              @ 080c0f84 0628
    bls LAB_080c0f8a                         @ 080c0f86 00d9
switchD_080c0f92__default:
    b LAB_080c121c                           @ 080c0f88 48e1
LAB_080c0f8a:
    lsls r0,r0,#0x2    @ 080c0f8a 8000
    ldr r1, DAT_080c0f98                     @ 080c0f8c 0249
    adds r0,r0,r1    @ 080c0f8e 4018
    ldr r0,[r0,#0x0]                         @ 080c0f90 0068
switchD_080c0f92__switchD:
    .hword 0x4687    @ 080c0f92 8746
DAT_080c0f94:
    .word  gBannerState                   @ 080c0f94 c0fe0102
DAT_080c0f98:
    .word  0x080c0f9c                     @ 080c0f98 9c0f0c08
switchD_080c0f92__switchdataD_080c0f9c:
    .word  0x080c0fb8                     @ 080c0f9c b80f0c08
    .word  0x080c108c                     @ 080c0fa0 8c100c08
    .word  0x080c10b8                     @ 080c0fa4 b8100c08
    .word  0x080c1100                     @ 080c0fa8 00110c08
    .word  0x080c1168                     @ 080c0fac 68110c08
    .word  0x080c11c0                     @ 080c0fb0 c0110c08
    .word  0x080c11f4                     @ 080c0fb4 f4110c08
switchD_080c0f92__caseD_0:
    lsls r0,r2,#0x10    @ 080c0fb8 1004
    lsrs r0,r0,#0x10    @ 080c0fba 000c
    movs r1,#0x80    @ 080c0fbc 8021
    lsls r1,r1,#0x2    @ 080c0fbe 8900
    bl blit_card_frame_tile_row_to_vram      @ 080c0fc0 01f0b0fe
    ldr r7, DAT_080c1070                     @ 080c0fc4 2a4f
    ldr r5, DAT_080c1074                     @ 080c0fc6 2b4d
    adds r0,r7,#0x0    @ 080c0fc8 381c
    movs r1,#0x0    @ 080c0fca 0021
    movs r2,#0x8    @ 080c0fcc 0822
    movs r3,#0x4    @ 080c0fce 0423
    bl tile_2d_row_copy                      @ 080c0fd0 36f080fa
    movs r0,#0x0    @ 080c0fd4 0020
    movs r2,#0x38    @ 080c0fd6 3822
    adds r2,r2,r6    @ 080c0fd8 9219
    .hword 0x4690    @ 080c0fda 9046
    subs r6,#0x8    @ 080c0fdc 083e
    .hword 0x46b1    @ 080c0fde b146
    ldr r3, DAT_080c1078                     @ 080c0fe0 254b
    .hword 0x469c    @ 080c0fe2 9c46
LAB_080c0fe4:
    adds r6,r0,#0x1    @ 080c0fe4 461c
    adds r3,r7,#0x0    @ 080c0fe6 3b1c
    movs r4,#0x7f    @ 080c0fe8 7f24
LAB_080c0fea:
    ldrb r1,[r5,#0x0]                        @ 080c0fea 2978
    ldrh r0,[r5,#0x0]                        @ 080c0fec 2888
    lsrs r2,r0,#0x8    @ 080c0fee 020a
    cmp r1,#0x0                              @ 080c0ff0 0029
    beq LAB_080c0ffc                         @ 080c0ff2 03d0
    adds r0,r1,#0x0    @ 080c0ff4 081c
    adds r0,#0x70    @ 080c0ff6 7030
    lsls r0,r0,#0x18    @ 080c0ff8 0006
    lsrs r1,r0,#0x18    @ 080c0ffa 010e
LAB_080c0ffc:
    cmp r2,#0x0                              @ 080c0ffc 002a
    beq LAB_080c1008                         @ 080c0ffe 03d0
    adds r0,r2,#0x0    @ 080c1000 101c
    adds r0,#0x70    @ 080c1002 7030
    lsls r0,r0,#0x18    @ 080c1004 0006
    lsrs r2,r0,#0x18    @ 080c1006 020e
LAB_080c1008:
    lsls r0,r2,#0x8    @ 080c1008 1002
    orrs r1,r0    @ 080c100a 0143
    strh r1,[r3,#0x0]                        @ 080c100c 1980
    adds r5,#0x2    @ 080c100e 0235
    adds r3,#0x2    @ 080c1010 0233
    subs r4,#0x1    @ 080c1012 013c
    cmp r4,#0x0                              @ 080c1014 002c
    bge LAB_080c0fea                         @ 080c1016 e8da
    movs r1,#0x80    @ 080c1018 8021
    lsls r1,r1,#0x3    @ 080c101a c900
    adds r7,r7,r1    @ 080c101c 7f18
    adds r0,r6,#0x0    @ 080c101e 301c
    cmp r0,#0x3                              @ 080c1020 0328
    ble LAB_080c0fe4                         @ 080c1022 dfdd
    ldr r1, PTR_WIN0H_080c107c               @ 080c1024 1549
    ldr r2, DAT_080c1080                     @ 080c1026 164a
    adds r0,r2,#0x0    @ 080c1028 101c
    strh r0,[r1,#0x0]                        @ 080c102a 0880
    ldr r2, PTR_WIN0V_080c1084               @ 080c102c 154a
    .hword 0x4643    @ 080c102e 4346
    lsls r1,r3,#0x18    @ 080c1030 1906
    lsrs r1,r1,#0x18    @ 080c1032 090e
    .hword 0x464f    @ 080c1034 4f46
    lsls r0,r7,#0x18    @ 080c1036 3806
    lsrs r0,r0,#0x10    @ 080c1038 000c
    orrs r1,r0    @ 080c103a 0143
    strh r1,[r2,#0x0]                        @ 080c103c 1180
    ldr r1, PTR_WININ_080c1088               @ 080c103e 1249
    movs r0,#0x3f    @ 080c1040 3f20
    strh r0,[r1,#0x0]                        @ 080c1042 0880
    adds r1,#0x2    @ 080c1044 0231
    movs r0,#0x1f    @ 080c1046 1f20
    strh r0,[r1,#0x0]                        @ 080c1048 0880
    adds r1,#0x6    @ 080c104a 0631
    movs r0,#0xef    @ 080c104c ef20
    strh r0,[r1,#0x0]                        @ 080c104e 0880
    adds r1,#0x4    @ 080c1050 0431
    movs r0,#0x0    @ 080c1052 0020
    strh r0,[r1,#0x0]                        @ 080c1054 0880
    subs r2,#0x44    @ 080c1056 443a
    ldrh r0,[r2,#0x0]                        @ 080c1058 1088
    movs r3,#0x80    @ 080c105a 8023
    lsls r3,r3,#0x6    @ 080c105c 9b01
    adds r1,r3,#0x0    @ 080c105e 191c
    orrs r0,r1    @ 080c1060 0843
    strh r0,[r2,#0x0]                        @ 080c1062 1080
    .hword 0x4667    @ 080c1064 6746
    ldrb r0,[r7,#0x10]                       @ 080c1066 387c
    adds r0,#0x1    @ 080c1068 0130
    strb r0,[r7,#0x10]                       @ 080c106a 3874
LAB_080c106c:
    movs r0,#0x1    @ 080c106c 0120
    b LAB_080c1238                           @ 080c106e e3e0
DAT_080c1070:
    .word  0x06014100                     @ 080c1070 00410106
DAT_080c1074:
    .word  0x098973f8                     @ 080c1074 f8738909
DAT_080c1078:
    .word  gBannerState                   @ 080c1078 c0fe0102
PTR_WIN0H_080c107c:
    .word  WIN0H                          @ 080c107c 40000004
DAT_080c1080:
    .word  0x000028f0                     @ 080c1080 f0280000
PTR_WIN0V_080c1084:
    .word  WIN0V                          @ 080c1084 44000004
PTR_WININ_080c1088:
    .word  WININ                          @ 080c1088 48000004
switchD_080c0f92__caseD_1:
    ldr r1, PTR_BLDY_080c10b0                @ 080c108c 0849
    ldr r2, DAT_080c10b4                     @ 080c108e 094a
    ldrb r3,[r2,#0x11]                       @ 080c1090 537c
    lsls r0,r3,#0x1    @ 080c1092 5800
    strh r0,[r1,#0x0]                        @ 080c1094 0880
    ldrb r0,[r2,#0x11]                       @ 080c1096 507c
    adds r0,#0x1    @ 080c1098 0130
    strb r0,[r2,#0x11]                       @ 080c109a 5074
    lsls r0,r0,#0x18    @ 080c109c 0006
    lsrs r0,r0,#0x18    @ 080c109e 000e
    cmp r0,#0x4                              @ 080c10a0 0428
    bls LAB_080c106c                         @ 080c10a2 e3d9
    ldrb r0,[r2,#0x10]                       @ 080c10a4 107c
    adds r0,#0x1    @ 080c10a6 0130
    strb r0,[r2,#0x10]                       @ 080c10a8 1074
    movs r0,#0x0    @ 080c10aa 0020
    strb r0,[r2,#0x11]                       @ 080c10ac 5074
    b LAB_080c106c                           @ 080c10ae dde7
PTR_BLDY_080c10b0:
    .word  BLDY                           @ 080c10b0 54000004
DAT_080c10b4:
    .word  gBannerState                   @ 080c10b4 c0fe0102
switchD_080c0f92__caseD_2:
    lsls r0,r6,#0x10    @ 080c10b8 3004
    orrs r0,r5    @ 080c10ba 2843
    .hword 0x464f    @ 080c10bc 4f46
    lsrs r2,r7,#0x1    @ 080c10be 7a08
    movs r1,#0x80    @ 080c10c0 8021
    bl write_oam_entry_with_tile_inc         @ 080c10c2 35f0c5f9
    .hword 0x464a    @ 080c10c6 4a46
    adds r2,#0x80    @ 080c10c8 8032
    adds r6,#0x20    @ 080c10ca 2036
    lsls r0,r6,#0x10    @ 080c10cc 3004
    orrs r0,r5    @ 080c10ce 2843
    movs r1,#0x81    @ 080c10d0 8121
    lsls r1,r1,#0x7    @ 080c10d2 c901
    lsrs r2,r2,#0x1    @ 080c10d4 5208
    bl write_oam_entry_with_tile_inc         @ 080c10d6 35f0bbf9
    ldr r1, DAT_080c10fc                     @ 080c10da 0849
    ldrb r0,[r1,#0x11]                       @ 080c10dc 487c
    adds r0,#0x1    @ 080c10de 0130
    strb r0,[r1,#0x11]                       @ 080c10e0 4874
    lsls r0,r0,#0x18    @ 080c10e2 0006
    lsrs r0,r0,#0x18    @ 080c10e4 000e
    cmp r0,#0x10                             @ 080c10e6 1028
    bls LAB_080c106c                         @ 080c10e8 c0d9
    movs r0,#0x0    @ 080c10ea 0020
    strb r0,[r1,#0x11]                       @ 080c10ec 4874
    ldrb r0,[r1,#0x10]                       @ 080c10ee 087c
    adds r0,#0x1    @ 080c10f0 0130
    strb r0,[r1,#0x10]                       @ 080c10f2 0874
    movs r0,#0xf    @ 080c10f4 0f20
    bl sync_state_and_init_sprite            @ 080c10f6 38f0ddfc
    b LAB_080c106c                           @ 080c10fa b7e7
DAT_080c10fc:
    .word  gBannerState                   @ 080c10fc c0fe0102
switchD_080c0f92__caseD_3:
    ldr r4, DAT_080c1164                     @ 080c1100 184c
    ldrb r3,[r4,#0x11]                       @ 080c1102 637c
    lsls r0,r3,#0x1    @ 080c1104 5800
    movs r1,#0x20    @ 080c1106 2021
    subs r1,r1,r0    @ 080c1108 091a
    lsls r3,r3,#0x13    @ 080c110a db04
    adds r0,r6,#0x0    @ 080c110c 301c
    adds r0,#0x8    @ 080c110e 0830
    lsls r0,r0,#0x10    @ 080c1110 0004
    orrs r0,r5    @ 080c1112 2843
    movs r2,#0x82    @ 080c1114 8222
    lsls r2,r2,#0x1    @ 080c1116 5200
    movs r7,#0x80    @ 080c1118 8027
    lsls r7,r7,#0x10    @ 080c111a 3f04
    adds r3,r3,r7    @ 080c111c db19
    orrs r3,r1    @ 080c111e 0b43
    movs r1,#0x80    @ 080c1120 8021
    bl write_pack_obj_attr_by_dir_stacked    @ 080c1122 35f0d3fd
    lsls r0,r6,#0x10    @ 080c1126 3004
    orrs r0,r5    @ 080c1128 2843
    .hword 0x4649    @ 080c112a 4946
    lsrs r2,r1,#0x1    @ 080c112c 4a08
    movs r1,#0x80    @ 080c112e 8021
    bl write_oam_entry_with_tile_inc         @ 080c1130 35f08ef9
    .hword 0x464a    @ 080c1134 4a46
    adds r2,#0x80    @ 080c1136 8032
    adds r6,#0x20    @ 080c1138 2036
    lsls r0,r6,#0x10    @ 080c113a 3004
    orrs r0,r5    @ 080c113c 2843
    movs r1,#0x81    @ 080c113e 8121
    lsls r1,r1,#0x7    @ 080c1140 c901
    lsrs r2,r2,#0x1    @ 080c1142 5208
    bl write_oam_entry_with_tile_inc         @ 080c1144 35f084f9
    ldrb r0,[r4,#0x11]                       @ 080c1148 607c
    adds r0,#0x1    @ 080c114a 0130
    strb r0,[r4,#0x11]                       @ 080c114c 6074
    lsls r0,r0,#0x18    @ 080c114e 0006
    lsrs r0,r0,#0x18    @ 080c1150 000e
    cmp r0,#0x10                             @ 080c1152 1028
    bls LAB_080c106c                         @ 080c1154 8ad9
    movs r0,#0x0    @ 080c1156 0020
    strb r0,[r4,#0x11]                       @ 080c1158 6074
    ldrb r0,[r4,#0x10]                       @ 080c115a 207c
    adds r0,#0x1    @ 080c115c 0130
    strb r0,[r4,#0x10]                       @ 080c115e 2074
    b LAB_080c106c                           @ 080c1160 84e7
    .zero  0x2
DAT_080c1164:
    .word  gBannerState                   @ 080c1164 c0fe0102
switchD_080c0f92__caseD_4:
    adds r0,r6,#0x0    @ 080c1168 301c
    adds r0,#0x8    @ 080c116a 0830
    lsls r0,r0,#0x10    @ 080c116c 0004
    orrs r0,r5    @ 080c116e 2843
    movs r2,#0x82    @ 080c1170 8222
    lsls r2,r2,#0x1    @ 080c1172 5200
    movs r1,#0x80    @ 080c1174 8021
    bl write_oam_entry_with_tile_inc         @ 080c1176 35f06bf9
    lsls r0,r6,#0x10    @ 080c117a 3004
    orrs r0,r5    @ 080c117c 2843
    .hword 0x464b    @ 080c117e 4b46
    lsrs r2,r3,#0x1    @ 080c1180 5a08
    movs r1,#0x80    @ 080c1182 8021
    bl write_oam_entry_with_tile_inc         @ 080c1184 35f064f9
    .hword 0x464a    @ 080c1188 4a46
    adds r2,#0x80    @ 080c118a 8032
    adds r6,#0x20    @ 080c118c 2036
    lsls r0,r6,#0x10    @ 080c118e 3004
    orrs r0,r5    @ 080c1190 2843
    movs r1,#0x81    @ 080c1192 8121
    lsls r1,r1,#0x7    @ 080c1194 c901
    lsrs r2,r2,#0x1    @ 080c1196 5208
    bl write_oam_entry_with_tile_inc         @ 080c1198 35f05af9
    ldr r1, DAT_080c11bc                     @ 080c119c 0749
    ldrb r0,[r1,#0x11]                       @ 080c119e 487c
    adds r0,#0x1    @ 080c11a0 0130
    strb r0,[r1,#0x11]                       @ 080c11a2 4874
    lsls r0,r0,#0x18    @ 080c11a4 0006
    lsrs r0,r0,#0x18    @ 080c11a6 000e
    cmp r0,#0x10                             @ 080c11a8 1028
    bhi LAB_080c11ae                         @ 080c11aa 00d8
    b LAB_080c106c                           @ 080c11ac 5ee7
LAB_080c11ae:
    movs r0,#0x0    @ 080c11ae 0020
    strb r0,[r1,#0x11]                       @ 080c11b0 4874
    ldrb r0,[r1,#0x10]                       @ 080c11b2 087c
    adds r0,#0x1    @ 080c11b4 0130
    strb r0,[r1,#0x10]                       @ 080c11b6 0874
    b LAB_080c106c                           @ 080c11b8 58e7
    .zero  0x2
DAT_080c11bc:
    .word  gBannerState                   @ 080c11bc c0fe0102
switchD_080c0f92__caseD_5:
    ldr r2, PTR_BLDY_080c11ec                @ 080c11c0 0a4a
    ldr r3, DAT_080c11f0                     @ 080c11c2 0b4b
    ldrb r7,[r3,#0x11]                       @ 080c11c4 5f7c
    lsls r1,r7,#0x1    @ 080c11c6 7900
    movs r0,#0x8    @ 080c11c8 0820
    subs r0,r0,r1    @ 080c11ca 401a
    strh r0,[r2,#0x0]                        @ 080c11cc 1080
    ldrb r0,[r3,#0x11]                       @ 080c11ce 587c
    adds r0,#0x1    @ 080c11d0 0130
    strb r0,[r3,#0x11]                       @ 080c11d2 5874
    lsls r0,r0,#0x18    @ 080c11d4 0006
    lsrs r0,r0,#0x18    @ 080c11d6 000e
    cmp r0,#0x4                              @ 080c11d8 0428
    bhi LAB_080c11de                         @ 080c11da 00d8
    b LAB_080c106c                           @ 080c11dc 46e7
LAB_080c11de:
    ldrb r0,[r3,#0x10]                       @ 080c11de 187c
    adds r0,#0x1    @ 080c11e0 0130
    strb r0,[r3,#0x10]                       @ 080c11e2 1874
    movs r0,#0x0    @ 080c11e4 0020
    strb r0,[r3,#0x11]                       @ 080c11e6 5874
    b LAB_080c106c                           @ 080c11e8 40e7
    .zero  0x2
PTR_BLDY_080c11ec:
    .word  BLDY                           @ 080c11ec 54000004
DAT_080c11f0:
    .word  gBannerState                   @ 080c11f0 c0fe0102
switchD_080c0f92__caseD_6:
    movs r2,#0x80    @ 080c11f4 8022
    lsls r2,r2,#0x13    @ 080c11f6 d204
    ldrh r1,[r2,#0x0]                        @ 080c11f8 1188
    ldr r0, DAT_080c1214                     @ 080c11fa 0648
    ands r0,r1    @ 080c11fc 0840
    strh r0,[r2,#0x0]                        @ 080c11fe 1080
    bl disable_blend_and_clear_step          @ 080c1200 34f0e8f9
    bl refresh_duel_field_zone_info          @ 080c1204 0af082fe
    ldr r1, DAT_080c1218                     @ 080c1208 0349
    ldrb r0,[r1,#0x10]                       @ 080c120a 087c
    adds r0,#0x1    @ 080c120c 0130
    strb r0,[r1,#0x10]                       @ 080c120e 0874
    b LAB_080c106c                           @ 080c1210 2ce7
    .zero  0x2
DAT_080c1214:
    .word  0x0000dfff                     @ 080c1214 ffdf0000
DAT_080c1218:
    .word  gBannerState                   @ 080c1218 c0fe0102
LAB_080c121c:
    movs r0,#0x2    @ 080c121c 0220
    rsbs r0,r0,#0    @ 080c121e 4042
    ldrb r1,[r7,#0x0]                        @ 080c1220 3978
    ands r0,r1    @ 080c1222 0840
    strb r0,[r7,#0x0]                        @ 080c1224 3870
    ldr r1, DAT_080c1244                     @ 080c1226 0749
    ldr r2, DAT_080c1248                     @ 080c1228 074a
    adds r1,r1,r2    @ 080c122a 8918
    movs r0,#0x5    @ 080c122c 0520
    rsbs r0,r0,#0    @ 080c122e 4042
    ldrb r3,[r1,#0x0]                        @ 080c1230 0b78
    ands r0,r3    @ 080c1232 1840
    strb r0,[r1,#0x0]                        @ 080c1234 0870
    movs r0,#0x0    @ 080c1236 0020
LAB_080c1238:
    pop {r3,r4}                              @ 080c1238 18bc
    .hword 0x4698    @ 080c123a 9846
    .hword 0x46a1    @ 080c123c a146
    pop {r4,r5,r6,r7}                        @ 080c123e f0bc
    pop {r1}                                 @ 080c1240 02bc
    bx r1                                    @ 080c1242 0847
DAT_080c1244:
    .word  0x02023130                     @ 080c1244 30310202
DAT_080c1248:
    .word  0x00000215                     @ 080c1248 15020000

@ 为卡牌缩放/展示 UI 效果计算并写入 OAM sprite 网格. 由 play_ui_effect_25 和 play_ui_effect_23 调用, 处理 pack UI 场景中卡牌放大动画的 OAM 布局. 入口: r0=player_side / r1=base_y_or_param / r2=tile_ptr_base / r3=packed (low16=clamp_max [0..0x3e7], hi16=sign_flag). 计算动画帧所需的 sprite 网格尺寸 (通过 __divsi3 / __modsi3 反复计算行列数), 对每个子精灵调用 write_oam_entry_from_packed_args 及 write_oam_entry_with_slot_check (FUN_080f67f4) 完成 OAM 写入. 关键常量: clamp_max=0x3e7 (最大列数), step=10 (% 10 折行), OAM tile pair 0x061a/0x0215 (pack banner OAM 属性). 函数体含 __divsi3/__modsi3 调用, 是计算量较重的 OAM layout 函数.
render_card_zoom_oam_sprite_grid:
    push {r4,r5,r6,r7,lr}                    @ 080c124c f0b5
    .hword 0x4657    @ 080c124e 5746
    .hword 0x464e    @ 080c1250 4e46
    .hword 0x4645    @ 080c1252 4546
    push {r5,r6,r7}                          @ 080c1254 e0b4
    sub sp,#0x2c                             @ 080c1256 8bb0
    str r0,[sp,#0x0]                         @ 080c1258 0090
    lsls r0,r3,#0x10    @ 080c125a 1804
    lsrs r0,r0,#0x10    @ 080c125c 000c
    str r0,[sp,#0x8]                         @ 080c125e 0290
    asrs r3,r3,#0x10    @ 080c1260 1b14
    str r3,[sp,#0xc]                         @ 080c1262 0393
    movs r0,#0x1    @ 080c1264 0120
    str r0,[sp,#0x10]                        @ 080c1266 0490
    ldr r0, DAT_080c1290                     @ 080c1268 0948
    ldr r3,[sp,#0x8]                         @ 080c126a 029b
    cmp r3,r0                                @ 080c126c 8342
    ble LAB_080c1272                         @ 080c126e 00dd
    str r0,[sp,#0x8]                         @ 080c1270 0290
LAB_080c1272:
    movs r4,#0xa    @ 080c1272 0a24
    adds r0,r2,#0x0    @ 080c1274 101c
    adds r0,#0x30    @ 080c1276 3030
    str r0,[sp,#0x24]                        @ 080c1278 0990
    adds r1,#0x8    @ 080c127a 0831
    str r1,[sp,#0x14]                        @ 080c127c 0591
    lsls r1,r2,#0x10    @ 080c127e 1104
    str r1,[sp,#0x18]                        @ 080c1280 0691
    adds r3,r2,#0x0    @ 080c1282 131c
    adds r3,#0x20    @ 080c1284 2033
    str r3,[sp,#0x1c]                        @ 080c1286 0793
    adds r2,#0x28    @ 080c1288 2832
    str r2,[sp,#0x20]                        @ 080c128a 0892
    b LAB_080c12a0                           @ 080c128c 08e0
    .zero  0x2
DAT_080c1290:
    .word  0x000003e7                     @ 080c1290 e7030000
LAB_080c1294:
    ldr r0,[sp,#0x10]                        @ 080c1294 0498
    adds r0,#0x1    @ 080c1296 0130
    str r0,[sp,#0x10]                        @ 080c1298 0490
    lsls r0,r4,#0x2    @ 080c129a a000
    adds r0,r0,r4    @ 080c129c 0019
    lsls r4,r0,#0x1    @ 080c129e 4400
LAB_080c12a0:
    ldr r0,[sp,#0x8]                         @ 080c12a0 0298
    adds r1,r4,#0x0    @ 080c12a2 211c
    bl __divsi3                              @ 080c12a4 4df0aef9
    cmp r0,#0x0                              @ 080c12a8 0028
    bgt LAB_080c1294                         @ 080c12aa f3dc
    ldr r1,[sp,#0x10]                        @ 080c12ac 0499
    lsls r0,r1,#0x1    @ 080c12ae 4800
    adds r0,r0,r1    @ 080c12b0 4018
    lsls r2,r0,#0x2    @ 080c12b2 8200
    adds r1,r2,#0x0    @ 080c12b4 111c
    adds r1,#0x10    @ 080c12b6 1031
    movs r3,#0xc8    @ 080c12b8 c823
    subs r0,r3,r1    @ 080c12ba 581a
    asrs r0,r0,#0x1    @ 080c12bc 4010
    adds r0,#0x28    @ 080c12be 2830
    str r0,[sp,#0x4]                         @ 080c12c0 0190
    adds r0,r1,#0x0    @ 080c12c2 081c
    cmp r1,#0x0                              @ 080c12c4 0029
    bge LAB_080c12cc                         @ 080c12c6 01da
    adds r0,r2,#0x0    @ 080c12c8 101c
    adds r0,#0x17    @ 080c12ca 1730
LAB_080c12cc:
    asrs r0,r0,#0x3    @ 080c12cc c010
    .hword 0x4680    @ 080c12ce 8046
    movs r0,#0x7    @ 080c12d0 0720
    ands r1,r0    @ 080c12d2 0140
    cmp r1,#0x0                              @ 080c12d4 0029
    beq LAB_080c12dc                         @ 080c12d6 01d0
    movs r2,#0x1    @ 080c12d8 0122
    add r8,r2                                @ 080c12da 9044
LAB_080c12dc:
    .hword 0x4640    @ 080c12dc 4046
    cmp r0,#0x5                              @ 080c12de 0528
    bgt LAB_080c12e6                         @ 080c12e0 01dc
    movs r1,#0x6    @ 080c12e2 0621
    .hword 0x4688    @ 080c12e4 8846
LAB_080c12e6:
    .hword 0x4642    @ 080c12e6 4246
    lsls r4,r2,#0x3    @ 080c12e8 d400
    subs r4,r3,r4    @ 080c12ea 1c1b
    asrs r4,r4,#0x1    @ 080c12ec 6410
    adds r7,r4,#0x0    @ 080c12ee 271c
    adds r7,#0x28    @ 080c12f0 2837
    ldr r3,[sp,#0x24]                        @ 080c12f2 099b
    lsls r5,r3,#0x10    @ 080c12f4 1d04
    adds r0,r7,#0x0    @ 080c12f6 381c
    orrs r0,r5    @ 080c12f8 2843
    ldr r6, DAT_080c1320                     @ 080c12fa 094e
    movs r1,#0x0    @ 080c12fc 0021
    adds r2,r6,#0x0    @ 080c12fe 321c
    bl write_oam_entry_from_packed_args      @ 080c1300 34f034ff
    .hword 0x4640    @ 080c1304 4046
    subs r0,#0x1    @ 080c1306 0138
    lsls r0,r0,#0x3    @ 080c1308 c000
    adds r0,r7,r0    @ 080c130a 3818
    orrs r0,r5    @ 080c130c 2843
    movs r3,#0x80    @ 080c130e 8023
    lsls r3,r3,#0x5    @ 080c1310 5b01
    movs r1,#0x0    @ 080c1312 0021
    adds r2,r6,#0x0    @ 080c1314 321c
    bl write_oam_entry_with_slot_check       @ 080c1316 35f06dfa
    movs r3,#0x2    @ 080c131a 0223
    adds r7,#0x8    @ 080c131c 0837
    b LAB_080c1372                           @ 080c131e 28e0
DAT_080c1320:
    .word  0x0000061a                     @ 080c1320 1a060000
LAB_080c1324:
    adds r1,r3,#0x0    @ 080c1324 191c
    str r3,[sp,#0x28]                        @ 080c1326 0a93
    bl __divsi3                              @ 080c1328 4df06cf9
    movs r1,#0x0    @ 080c132c 0021
    ldr r3,[sp,#0x28]                        @ 080c132e 0a9b
    cmp r3,#0x2                              @ 080c1330 022b
    bne LAB_080c1338                         @ 080c1332 01d1
    movs r1,#0x80    @ 080c1334 8021
    lsls r1,r1,#0x7    @ 080c1336 c901
LAB_080c1338:
    adds r2,r0,#0x0    @ 080c1338 021c
    muls r2,r3    @ 080c133a 5a43
    .hword 0x4692    @ 080c133c 9246
    asrs r2,r3,#0x1    @ 080c133e 5a10
    .hword 0x4691    @ 080c1340 9146
    cmp r0,#0x0                              @ 080c1342 0028
    ble LAB_080c1368                         @ 080c1344 10dd
    adds r4,r0,#0x0    @ 080c1346 041c
    ldr r0,[sp,#0x24]                        @ 080c1348 0998
    lsls r6,r0,#0x10    @ 080c134a 0604
    lsls r5,r1,#0x10    @ 080c134c 0d04
LAB_080c134e:
    adds r0,r7,#0x0    @ 080c134e 381c
    orrs r0,r6    @ 080c1350 3043
    lsrs r1,r5,#0x10    @ 080c1352 290c
    ldr r2, DAT_080c1404                     @ 080c1354 2b4a
    str r3,[sp,#0x28]                        @ 080c1356 0a93
    bl write_oam_entry_from_packed_args      @ 080c1358 34f008ff
    ldr r3,[sp,#0x28]                        @ 080c135c 0a9b
    lsls r0,r3,#0x3    @ 080c135e d800
    adds r7,r7,r0    @ 080c1360 3f18
    subs r4,#0x1    @ 080c1362 013c
    cmp r4,#0x0                              @ 080c1364 002c
    bne LAB_080c134e                         @ 080c1366 f2d1
LAB_080c1368:
    .hword 0x4641    @ 080c1368 4146
    .hword 0x4652    @ 080c136a 5246
    subs r1,r1,r2    @ 080c136c 891a
    .hword 0x4688    @ 080c136e 8846
    .hword 0x464b    @ 080c1370 4b46
LAB_080c1372:
    .hword 0x4640    @ 080c1372 4046
    subs r0,#0x2    @ 080c1374 0238
    cmp r0,#0x0                              @ 080c1376 0028
    bgt LAB_080c1324                         @ 080c1378 d4dc
    ldr r3,[sp,#0x14]                        @ 080c137a 059b
    ldr r0,[sp,#0x18]                        @ 080c137c 0698
    orrs r3,r0    @ 080c137e 0343
    str r3,[sp,#0x18]                        @ 080c1380 0693
    movs r2,#0xa0    @ 080c1382 a022
    lsls r2,r2,#0x3    @ 080c1384 d200
    adds r0,r3,#0x0    @ 080c1386 181c
    movs r1,#0x80    @ 080c1388 8021
    bl write_oam_entry_with_tile_inc         @ 080c138a 35f061f8
    ldr r1,[sp,#0x1c]                        @ 080c138e 0799
    lsls r0,r1,#0x10    @ 080c1390 0804
    ldr r2,[sp,#0x14]                        @ 080c1392 059a
    orrs r2,r0    @ 080c1394 0243
    str r2,[sp,#0x14]                        @ 080c1396 0592
    movs r1,#0x81    @ 080c1398 8121
    lsls r1,r1,#0x7    @ 080c139a c901
    movs r2,#0xa8    @ 080c139c a822
    lsls r2,r2,#0x3    @ 080c139e d200
    ldr r0,[sp,#0x14]                        @ 080c13a0 0598
    bl write_oam_entry_with_tile_inc         @ 080c13a2 35f055f8
    ldr r3,[sp,#0x20]                        @ 080c13a6 089b
    lsls r0,r3,#0x10    @ 080c13a8 1804
    ldr r1,[sp,#0x4]                         @ 080c13aa 0199
    orrs r0,r1    @ 080c13ac 0843
    ldr r2, DAT_080c1408                     @ 080c13ae 164a
    ldr r3,[sp,#0xc]                         @ 080c13b0 039b
    cmp r3,#0x1                              @ 080c13b2 012b
    ble LAB_080c13b8                         @ 080c13b4 00dd
    ldr r2, DAT_080c140c                     @ 080c13b6 154a
LAB_080c13b8:
    movs r1,#0x40    @ 080c13b8 4021
    bl write_oam_entry_from_packed_args      @ 080c13ba 34f0d7fe
    ldr r0,[sp,#0x10]                        @ 080c13be 0498
    cmp r0,#0x0                              @ 080c13c0 0028
    ble LAB_080c1438                         @ 080c13c2 39dd
    adds r1,r0,#0x0    @ 080c13c4 011c
    subs r1,#0x1    @ 080c13c6 0139
    movs r6,#0x0    @ 080c13c8 0026
    lsls r0,r1,#0x1    @ 080c13ca 4800
    adds r0,r0,r1    @ 080c13cc 4018
    lsls r0,r0,#0x2    @ 080c13ce 8000
    adds r0,#0x10    @ 080c13d0 1030
    ldr r1,[sp,#0x4]                         @ 080c13d2 0199
    adds r7,r1,r0    @ 080c13d4 0f18
    ldr r5,[sp,#0x10]                        @ 080c13d6 049d
LAB_080c13d8:
    subs r4,r7,r6    @ 080c13d8 bc1b
    ldr r2,[sp,#0x20]                        @ 080c13da 089a
    lsls r0,r2,#0x10    @ 080c13dc 1004
    orrs r4,r0    @ 080c13de 0443
    ldr r0,[sp,#0x8]                         @ 080c13e0 0298
    movs r1,#0xa    @ 080c13e2 0a21
    bl __modsi3                              @ 080c13e4 4df05af9
    lsls r0,r0,#0x1    @ 080c13e8 4000
    movs r3,#0x93    @ 080c13ea 9323
    lsls r3,r3,#0x2    @ 080c13ec 9b00
    adds r2,r0,r3    @ 080c13ee c218
    ldr r0, DAT_080c1410                     @ 080c13f0 0748
    ldr r0,[r0,#0x4]                         @ 080c13f2 4068
    movs r1,#0x1    @ 080c13f4 0121
    eors r0,r1    @ 080c13f6 4840
    ldr r1,[sp,#0x0]                         @ 080c13f8 0099
    cmp r1,r0                                @ 080c13fa 8142
    bne LAB_080c1414                         @ 080c13fc 0ad1
    movs r0,#0x80    @ 080c13fe 8020
    lsls r0,r0,#0x6    @ 080c1400 8001
    b LAB_080c1418                           @ 080c1402 09e0
DAT_080c1404:
    .word  0x0000061b                     @ 080c1404 1b060000
DAT_080c1408:
    .word  0x00001218                     @ 080c1408 18120000
DAT_080c140c:
    .word  0x00002218                     @ 080c140c 18220000
DAT_080c1410:
    .word  0x0201e2a0                     @ 080c1410 a0e20102
LAB_080c1414:
    movs r0,#0x80    @ 080c1414 8020
    lsls r0,r0,#0x5    @ 080c1416 4001
LAB_080c1418:
    orrs r2,r0    @ 080c1418 0243
    lsls r0,r2,#0x10    @ 080c141a 1004
    lsrs r2,r0,#0x10    @ 080c141c 020c
    adds r0,r4,#0x0    @ 080c141e 201c
    movs r1,#0x40    @ 080c1420 4021
    bl write_oam_entry_from_packed_args      @ 080c1422 34f0a3fe
    ldr r0,[sp,#0x8]                         @ 080c1426 0298
    movs r1,#0xa    @ 080c1428 0a21
    bl __divsi3                              @ 080c142a 4df0ebf8
    str r0,[sp,#0x8]                         @ 080c142e 0290
    adds r6,#0xc    @ 080c1430 0c36
    subs r5,#0x1    @ 080c1432 013d
    cmp r5,#0x0                              @ 080c1434 002d
    bne LAB_080c13d8                         @ 080c1436 cfd1
LAB_080c1438:
    add sp,#0x2c                             @ 080c1438 0bb0
    pop {r3,r4,r5}                           @ 080c143a 38bc
    .hword 0x4698    @ 080c143c 9846
    .hword 0x46a1    @ 080c143e a146
    .hword 0x46aa    @ 080c1440 aa46
    pop {r4,r5,r6,r7}                        @ 080c1442 f0bc
    pop {r0}                                 @ 080c1444 01bc
    bx r0                                    @ 080c1446 0047

