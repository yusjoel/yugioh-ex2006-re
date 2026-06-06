@ ==== 01_vija_scene_text.s ====
@ vija 场景状态机 + 文本渲染 + puzzle 显示派发
.thumb
@ vija scene (play_ui_effect_3b) per-frame state machine driver. No parameters; all state from IWRAM 0x02029eb0. 10-phase dispatch (phases 0-9): phase 0: init display regs (DISPCNT/BGxCNT), load BG+OBJ gfx, clear palette, init 5 OBJ slots; phase 1: check blend done, start fade-in; phase 2/3: advance blend, check affine init; phase 4: tick_all_vija_obj_anim_slots + tick_bg_scroll_anim_frame + tick_bg2_affine_anim_frame each frame; phase 5: start fade-out blend; phase 6: tick blend; phase 7: tick_all_vija_obj_anim_slots + check fade; phase 8/9: epilogue return 1. Returns r0=1 (scene done) or r0=0 (scene continue). Side-effects: DISPCNT/BG0-2CNT/palette VRAM, OAM, IWRAM state fields. Constants: VIJA_STATE=0x02029eb0, DISPCNT_INIT=0x1741, SLOT_COUNT=5.
run_vija_scene_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 0801cb00 f0b5
    sub sp,#0x18                             @ 0801cb02 86b0
    ldr r5, run_vija_scene_state_machine_gvija_state @ 0801cb04 054d
    adds r0,r5,#0x0    @ 0801cb06 281c
    adds r0,#0x8d    @ 0801cb08 8d30
    ldrb r0,[r0,#0x0]                        @ 0801cb0a 0078
    cmp r0,#0x9                              @ 0801cb0c 0928
    bls LAB_0801cb12                         @ 0801cb0e 00d9
    b switchD_0801cb1a__default              @ 0801cb10 18e2
LAB_0801cb12:
    lsls r0,r0,#0x2    @ 0801cb12 8000
    ldr r1, run_vija_scene_state_machine_switch_table_base @ 0801cb14 0249
    adds r0,r0,r1    @ 0801cb16 4018
    ldr r0,[r0,#0x0]                         @ 0801cb18 0068
switchD_0801cb1a__switchD:
    .hword 0x4687    @ 0801cb1a 8746
run_vija_scene_state_machine_gvija_state:
    .word  gVijaState                     @ 0801cb1c b09e0202  gVijaState: vija per-frame state struct base (0xc0 bytes @ EWRAM)
run_vija_scene_state_machine_switch_table_base:
    .word  0x0801cb24                     @ 0801cb20 24cb0108  ptr to 10-case switch jump table at switchdataD_0801cb24
switchD_0801cb1a__switchdataD_0801cb24:
    .word  0x0801cb4c                     @ 0801cb24 4ccb0108
    .word  0x0801cc08                     @ 0801cb28 08cc0108
    .word  0x0801cc5a                     @ 0801cb2c 5acc0108
    .word  0x0801cc7a                     @ 0801cb30 7acc0108
    .word  0x0801ccdc                     @ 0801cb34 dccc0108
    .word  0x0801cda0                     @ 0801cb38 a0cd0108
    .word  0x0801ce04                     @ 0801cb3c 04ce0108
    .word  0x0801ce48                     @ 0801cb40 48ce0108
    .word  0x0801cebc                     @ 0801cb44 bcce0108
    .word  0x0801cf30                     @ 0801cb48 30cf0108
switchD_0801cb1a__caseD_0:
    movs r0,#0x0    @ 0801cb4c 0020
    str r0,[sp,#0x0]                         @ 0801cb4e 0090
    str r0,[sp,#0x4]                         @ 0801cb50 0190
    movs r0,#0x1    @ 0801cb52 0120
    movs r1,#0x0    @ 0801cb54 0021
    movs r2,#0x1    @ 0801cb56 0122
    movs r3,#0x2    @ 0801cb58 0223
    bl load_vija_bg_gfx_by_mode              @ 0801cb5a fff793fc
    ldr r0, run_vija_scene_state_machine_vija_bg_path_pair @ 0801cb5e 2548
    ldr r1,[r0,#0x4]                         @ 0801cb60 4168
    ldr r0,[r0,#0x0]                         @ 0801cb62 0068
    str r0,[sp,#0x10]                        @ 0801cb64 0490
    str r1,[sp,#0x14]                        @ 0801cb66 0591
    movs r2,#0x0    @ 0801cb68 0022
    ldr r0, run_vija_scene_state_machine_rom_region_code_addr @ 0801cb6a 2348
    ldrh r0,[r0,#0x0]                        @ 0801cb6c 0088
    lsrs r0,r0,#0x8    @ 0801cb6e 000a
    cmp r0,#0x4a                             @ 0801cb70 4a28
    bne LAB_0801cb84                         @ 0801cb72 07d1
    ldr r1, run_vija_scene_state_machine_ewram_base @ 0801cb74 2149
    ldr r0, run_vija_scene_state_machine_gsettings_offset @ 0801cb76 2248
    adds r1,r1,r0    @ 0801cb78 0918
    movs r0,#0x7    @ 0801cb7a 0720
    ldrb r1,[r1,#0x0]                        @ 0801cb7c 0978
    ands r0,r1    @ 0801cb7e 0840
    cmp r0,#0x0                              @ 0801cb80 0028
    beq LAB_0801cb86                         @ 0801cb82 00d0
LAB_0801cb84:
    movs r2,#0x1    @ 0801cb84 0122
LAB_0801cb86:
    lsls r0,r2,#0x2    @ 0801cb86 9000
    add r1,sp,#0x10                          @ 0801cb88 04a9
    adds r0,r0,r1    @ 0801cb8a 4018
    ldr r0,[r0,#0x0]                         @ 0801cb8c 0068
    movs r1,#0x0    @ 0801cb8e 0021
    bl fs_load                               @ 0801cb90 f8f70afa
    adds r1,r5,#0x0    @ 0801cb94 291c
    adds r1,#0x88    @ 0801cb96 8831
    str r0,[r1,#0x0]                         @ 0801cb98 0860
    movs r4,#0x0    @ 0801cb9a 0024
    str r4,[sp,#0x0]                         @ 0801cb9c 0094
    str r4,[sp,#0x4]                         @ 0801cb9e 0194
    movs r0,#0x0    @ 0801cba0 0020
    movs r1,#0x0    @ 0801cba2 0021
    movs r2,#0x1    @ 0801cba4 0122
    movs r3,#0x1    @ 0801cba6 0123
    bl load_vija_bg_gfx_by_mode              @ 0801cba8 fff76cfc
    str r4,[sp,#0x0]                         @ 0801cbac 0094
    str r4,[sp,#0x4]                         @ 0801cbae 0194
    movs r0,#0x0    @ 0801cbb0 0020
    movs r1,#0x1    @ 0801cbb2 0121
    movs r2,#0x0    @ 0801cbb4 0022
    movs r3,#0x0    @ 0801cbb6 0023
    bl load_vija_bg_gfx_by_mode              @ 0801cbb8 fff764fc
    movs r1,#0x10    @ 0801cbbc 1021
    rsbs r1,r1,#0    @ 0801cbbe 4942
    movs r0,#0x3f    @ 0801cbc0 3f20
    bl gl_set_brightness                     @ 0801cbc2 f7f79bfd
    movs r0,#0x3f    @ 0801cbc6 3f20
    movs r1,#0x0    @ 0801cbc8 0021
    movs r2,#0x1e    @ 0801cbca 1e22
    bl gl_set_blend2_level                   @ 0801cbcc f7f704fe
    movs r2,#0x80    @ 0801cbd0 8022
    lsls r2,r2,#0x13    @ 0801cbd2 d204
    movs r3,#0x80    @ 0801cbd4 8023
    lsls r3,r3,#0x2    @ 0801cbd6 9b00
    ldr r0, run_vija_scene_state_machine_dispcnt_obj_en_mask_a @ 0801cbd8 0a48
    ldrh r1,[r2,#0x0]                        @ 0801cbda 1188
    ands r0,r1    @ 0801cbdc 0840
    orrs r0,r3    @ 0801cbde 1843
    strh r0,[r2,#0x0]                        @ 0801cbe0 1080
    movs r0,#0x2    @ 0801cbe2 0220
    bl set_channel_if_changed                @ 0801cbe4 dcf07aff
    adds r1,r5,#0x0    @ 0801cbe8 291c
    adds r1,#0x8d    @ 0801cbea 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cbec 0878
    adds r0,#0x1    @ 0801cbee 0130
    b LAB_0801cf42                           @ 0801cbf0 a7e1
    .zero  0x2
run_vija_scene_state_machine_vija_bg_path_pair:
    .word  vija_bg_fs_path_pair           @ 0801cbf4 08dae309  ptr to {JP path, US path} pair for vija BG1 LZ5 file load
run_vija_scene_state_machine_rom_region_code_addr:
    .word  ROM_REGION_CODE_ADDR           @ 0801cbf8 ae000008  ROM header game-code high u16 (ldrh+>>8 gives region char)
run_vija_scene_state_machine_ewram_base:
    .word  EWRAM_BASE                     @ 0801cbfc 00000002  EWRAM base: used with GSETTINGS_OFFSET to reach gSettings
run_vija_scene_state_machine_gsettings_offset:
    .word  GSETTINGS_OFFSET               @ 0801cc00 2c6c0000  gSettings byte offset from EWRAM_BASE (0x6c2c)
run_vija_scene_state_machine_dispcnt_obj_en_mask_a:
    .word  DEMO_CLEAR_BITS_12_8           @ 0801cc04 ffe0ffff  DISPCNT clear bits[12:8] (BG/OBJ enable field)
switchD_0801cb1a__caseD_1:
    bl check_blend_transition_done           @ 0801cc08 f7f774fe
    adds r4,r0,#0x0    @ 0801cc0c 041c
    cmp r4,#0x0                              @ 0801cc0e 002c
    beq LAB_0801cc14                         @ 0801cc10 00d0
    b switchD_0801cb1a__default              @ 0801cc12 97e1
LAB_0801cc14:
    movs r0,#0x1    @ 0801cc14 0120
    movs r1,#0x2    @ 0801cc16 0221
    movs r2,#0x0    @ 0801cc18 0022
    movs r3,#0x10    @ 0801cc1a 1023
    bl init_blend_transition_params          @ 0801cc1c f7f79afd
    movs r0,#0x1e    @ 0801cc20 1e20
    str r0,[sp,#0x0]                         @ 0801cc22 0090
    movs r0,#0x1    @ 0801cc24 0120
    movs r1,#0x2    @ 0801cc26 0221
    movs r2,#0x10    @ 0801cc28 1022
    movs r3,#0x0    @ 0801cc2a 0023
    bl init_blend_transition_params_ex       @ 0801cc2c f7f704fe
    movs r2,#0x80    @ 0801cc30 8022
    lsls r2,r2,#0x13    @ 0801cc32 d204
    movs r0,#0x80    @ 0801cc34 8020
    lsls r0,r0,#0x1    @ 0801cc36 4000
    ldrh r1,[r2,#0x0]                        @ 0801cc38 1188
    orrs r0,r1    @ 0801cc3a 0843
    strh r0,[r2,#0x0]                        @ 0801cc3c 1080
    adds r0,r5,#0x0    @ 0801cc3e 281c
    adds r0,#0x93    @ 0801cc40 9330
    strb r4,[r0,#0x0]                        @ 0801cc42 0470
    adds r0,#0x1    @ 0801cc44 0130
    strb r4,[r0,#0x0]                        @ 0801cc46 0470
    subs r0,#0x3    @ 0801cc48 0338
    strb r4,[r0,#0x0]                        @ 0801cc4a 0470
    subs r0,#0x3    @ 0801cc4c 0338
    strb r4,[r0,#0x0]                        @ 0801cc4e 0470
    adds r1,r5,#0x0    @ 0801cc50 291c
    adds r1,#0x8d    @ 0801cc52 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cc54 0878
    adds r0,#0x1    @ 0801cc56 0130
    b LAB_0801cf42                           @ 0801cc58 73e1
switchD_0801cb1a__caseD_2:
    bl check_blend_transition_done           @ 0801cc5a f7f74bfe
    cmp r0,#0x0                              @ 0801cc5e 0028
    bne switchD_0801cb1a__caseD_3            @ 0801cc60 0bd1
    movs r2,#0x80    @ 0801cc62 8022
    lsls r2,r2,#0x13    @ 0801cc64 d204
    movs r0,#0x80    @ 0801cc66 8020
    lsls r0,r0,#0x5    @ 0801cc68 4001
    ldrh r1,[r2,#0x0]                        @ 0801cc6a 1188
    orrs r0,r1    @ 0801cc6c 0843
    strh r0,[r2,#0x0]                        @ 0801cc6e 1080
    adds r1,r5,#0x0    @ 0801cc70 291c
    adds r1,#0x8d    @ 0801cc72 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cc74 0878
    adds r0,#0x1    @ 0801cc76 0130
    strb r0,[r1,#0x0]                        @ 0801cc78 0870
switchD_0801cb1a__caseD_3:
    adds r3,r5,#0x0    @ 0801cc7a 2b1c
    adds r3,#0x93    @ 0801cc7c 9333
    adds r2,r5,#0x0    @ 0801cc7e 2a1c
    adds r2,#0x94    @ 0801cc80 9432
    ldrb r1,[r2,#0x0]                        @ 0801cc82 1178
    lsls r0,r1,#0x8    @ 0801cc84 0802
    ldrb r7,[r3,#0x0]                        @ 0801cc86 1f78
    orrs r0,r7    @ 0801cc88 3843
    adds r1,r0,#0x1    @ 0801cc8a 411c
    strb r1,[r3,#0x0]                        @ 0801cc8c 1970
    lsrs r1,r1,#0x8    @ 0801cc8e 090a
    strb r1,[r2,#0x0]                        @ 0801cc90 1170
    bl tick_bg_scroll_anim_frame             @ 0801cc92 fff70dfd
    adds r0,r5,#0x0    @ 0801cc96 281c
    adds r0,#0x8e    @ 0801cc98 8e30
    adds r4,r0,#0x0    @ 0801cc9a 041c
    ldrb r0,[r4,#0x0]                        @ 0801cc9c 2078
    cmp r0,#0x3c                             @ 0801cc9e 3c28
    bne LAB_0801ccd4                         @ 0801cca0 18d1
    adds r1,r5,#0x0    @ 0801cca2 291c
    adds r1,#0x8d    @ 0801cca4 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cca6 0878
    adds r0,#0x1    @ 0801cca8 0130
    strb r0,[r1,#0x0]                        @ 0801ccaa 0870
    movs r0,#0x0    @ 0801ccac 0020
    strb r0,[r4,#0x0]                        @ 0801ccae 2070
    movs r3,#0x0    @ 0801ccb0 0023
    movs r6,#0x7    @ 0801ccb2 0726
    movs r1,#0x8    @ 0801ccb4 0821
    rsbs r1,r1,#0    @ 0801ccb6 4942
    .hword 0x468c    @ 0801ccb8 8c46
    adds r2,r5,#0x0    @ 0801ccba 2a1c
    adds r2,#0x9c    @ 0801ccbc 9c32
LAB_0801ccbe:
    adds r1,r3,#0x0    @ 0801ccbe 191c
    ands r1,r6    @ 0801ccc0 3140
    .hword 0x4660    @ 0801ccc2 6046
    ldrb r7,[r2,#0x0]                        @ 0801ccc4 1778
    ands r0,r7    @ 0801ccc6 3840
    orrs r0,r1    @ 0801ccc8 0843
    strb r0,[r2,#0x0]                        @ 0801ccca 1070
    adds r2,#0x8    @ 0801cccc 0832
    adds r3,#0x1    @ 0801ccce 0133
    cmp r3,#0x4                              @ 0801ccd0 042b
    bls LAB_0801ccbe                         @ 0801ccd2 f4d9
LAB_0801ccd4:
    ldrb r0,[r4,#0x0]                        @ 0801ccd4 2078
    adds r0,#0x1    @ 0801ccd6 0130
    strb r0,[r4,#0x0]                        @ 0801ccd8 2070
    b switchD_0801cb1a__default              @ 0801ccda 33e1
switchD_0801cb1a__caseD_4:
    adds r0,r5,#0x0    @ 0801ccdc 281c
    adds r0,#0x8e    @ 0801ccde 8e30
    movs r1,#0x97    @ 0801cce0 9721
    adds r4,r0,#0x0    @ 0801cce2 041c
    ldrb r0,[r4,#0x0]                        @ 0801cce4 2078
    cmp r0,#0x96                             @ 0801cce6 9628
    bhi LAB_0801ccec                         @ 0801cce8 00d8
    ldrb r1,[r4,#0x0]                        @ 0801ccea 2178
LAB_0801ccec:
    adds r0,r1,#0x0    @ 0801ccec 081c
    movs r1,#0x1e    @ 0801ccee 1e21
    bl __modsi3                              @ 0801ccf0 f1f0d4fc
    cmp r0,#0x0                              @ 0801ccf4 0028
    bne LAB_0801cd0e                         @ 0801ccf6 0ad1
    adds r2,r5,#0x0    @ 0801ccf8 2a1c
    adds r2,#0x8f    @ 0801ccfa 8f32
    ldrb r1,[r2,#0x0]                        @ 0801ccfc 1178
    lsls r0,r1,#0x3    @ 0801ccfe c800
    adds r0,r5,r0    @ 0801cd00 2818
    adds r0,#0x98    @ 0801cd02 9830
    movs r1,#0x1    @ 0801cd04 0121
    strb r1,[r0,#0x0]                        @ 0801cd06 0170
    ldrb r0,[r2,#0x0]                        @ 0801cd08 1078
    adds r0,#0x1    @ 0801cd0a 0130
    strb r0,[r2,#0x0]                        @ 0801cd0c 1070
LAB_0801cd0e:
    bl tick_all_vija_obj_anim_slots          @ 0801cd0e fff7e5fe
    adds r3,r5,#0x0    @ 0801cd12 2b1c
    adds r3,#0x93    @ 0801cd14 9333
    adds r2,r5,#0x0    @ 0801cd16 2a1c
    adds r2,#0x94    @ 0801cd18 9432
    ldrb r7,[r2,#0x0]                        @ 0801cd1a 1778
    lsls r0,r7,#0x8    @ 0801cd1c 3802
    ldrb r1,[r3,#0x0]                        @ 0801cd1e 1978
    orrs r0,r1    @ 0801cd20 0843
    adds r1,r0,#0x1    @ 0801cd22 411c
    strb r1,[r3,#0x0]                        @ 0801cd24 1970
    lsrs r1,r1,#0x8    @ 0801cd26 090a
    strb r1,[r2,#0x0]                        @ 0801cd28 1170
    bl tick_bg_scroll_anim_frame             @ 0801cd2a fff7c1fc
    ldrb r0,[r4,#0x0]                        @ 0801cd2e 2078
    adds r0,#0x1    @ 0801cd30 0130
    strb r0,[r4,#0x0]                        @ 0801cd32 2070
    lsls r0,r0,#0x18    @ 0801cd34 0006
    lsrs r0,r0,#0x18    @ 0801cd36 000e
    cmp r0,#0x5a                             @ 0801cd38 5a28
    bne LAB_0801cd5a                         @ 0801cd3a 0ed1
    movs r0,#0x1    @ 0801cd3c 0120
    movs r1,#0x2    @ 0801cd3e 0221
    movs r2,#0x10    @ 0801cd40 1022
    movs r3,#0x0    @ 0801cd42 0023
    bl init_blend_transition_params          @ 0801cd44 f7f706fd
    movs r0,#0x3c    @ 0801cd48 3c20
    str r0,[sp,#0x0]                         @ 0801cd4a 0090
    movs r0,#0x1    @ 0801cd4c 0120
    movs r1,#0x2    @ 0801cd4e 0221
    movs r2,#0x0    @ 0801cd50 0022
    movs r3,#0x10    @ 0801cd52 1023
    bl init_blend_transition_params_ex       @ 0801cd54 f7f770fd
    b switchD_0801cb1a__default              @ 0801cd58 f4e0
LAB_0801cd5a:
    cmp r0,#0x97                             @ 0801cd5a 9728
    beq LAB_0801cd60                         @ 0801cd5c 00d0
    b switchD_0801cb1a__default              @ 0801cd5e f1e0
LAB_0801cd60:
    movs r0,#0x2    @ 0801cd60 0220
    movs r1,#0x4    @ 0801cd62 0421
    movs r2,#0x10    @ 0801cd64 1022
    movs r3,#0x0    @ 0801cd66 0023
    bl init_blend_transition_params          @ 0801cd68 f7f7f4fc
    movs r0,#0x3c    @ 0801cd6c 3c20
    str r0,[sp,#0x0]                         @ 0801cd6e 0090
    movs r0,#0x2    @ 0801cd70 0220
    movs r1,#0x4    @ 0801cd72 0421
    movs r2,#0x0    @ 0801cd74 0022
    movs r3,#0x10    @ 0801cd76 1023
    bl init_blend_transition_params_ex       @ 0801cd78 f7f75efd
    movs r2,#0x80    @ 0801cd7c 8022
    lsls r2,r2,#0x13    @ 0801cd7e d204
    movs r3,#0xb0    @ 0801cd80 b023
    lsls r3,r3,#0x5    @ 0801cd82 5b01
    ldr r0, run_vija_scene_state_machine_dispcnt_obj_en_mask_b @ 0801cd84 0548
    ldrh r1,[r2,#0x0]                        @ 0801cd86 1188
    ands r0,r1    @ 0801cd88 0840
    orrs r0,r3    @ 0801cd8a 1843
    strh r0,[r2,#0x0]                        @ 0801cd8c 1080
    movs r0,#0x0    @ 0801cd8e 0020
    strb r0,[r4,#0x0]                        @ 0801cd90 2070
    adds r1,r5,#0x0    @ 0801cd92 291c
    adds r1,#0x8d    @ 0801cd94 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cd96 0878
    adds r0,#0x1    @ 0801cd98 0130
    b LAB_0801cf42                           @ 0801cd9a d2e0
run_vija_scene_state_machine_dispcnt_obj_en_mask_b:
    .word  DEMO_CLEAR_BITS_12_8           @ 0801cd9c ffe0ffff
switchD_0801cb1a__caseD_5:
    bl tick_bg2_affine_anim_frame            @ 0801cda0 fff778fc
    bl check_blend_transition_done           @ 0801cda4 f7f7a6fd
    cmp r0,#0x0                              @ 0801cda8 0028
    beq LAB_0801cdae                         @ 0801cdaa 00d0
    b LAB_0801ceb6                           @ 0801cdac 83e0
LAB_0801cdae:
    ldr r1, run_vija_scene_state_machine_vija_obj_slot_seq @ 0801cdae 1449
    add r0,sp,#0x8                           @ 0801cdb0 02a8
    movs r2,#0x5    @ 0801cdb2 0522
    bl memcpy                                @ 0801cdb4 f1f0d2fd
    adds r6,r5,#0x0    @ 0801cdb8 2e1c
    adds r6,#0x8e    @ 0801cdba 8e36
    ldrb r4,[r6,#0x0]                        @ 0801cdbc 3478
    adds r0,r4,#0x0    @ 0801cdbe 201c
    movs r1,#0xa    @ 0801cdc0 0a21
    bl __umodsi3                             @ 0801cdc2 f1f047fd
    lsls r0,r0,#0x18    @ 0801cdc6 0006
    cmp r0,#0x0                              @ 0801cdc8 0028
    bne LAB_0801cde8                         @ 0801cdca 0dd1
    adds r0,r4,#0x0    @ 0801cdcc 201c
    movs r1,#0xa    @ 0801cdce 0a21
    bl __udivsi3                             @ 0801cdd0 f1f004fd
    lsls r0,r0,#0x18    @ 0801cdd4 0006
    lsrs r0,r0,#0x18    @ 0801cdd6 000e
    add r0,sp                                @ 0801cdd8 6844
    adds r0,#0x8    @ 0801cdda 0830
    ldrb r0,[r0,#0x0]                        @ 0801cddc 0078
    lsls r0,r0,#0x3    @ 0801cdde c000
    adds r0,r5,r0    @ 0801cde0 2818
    adds r0,#0x98    @ 0801cde2 9830
    movs r1,#0x3    @ 0801cde4 0321
    strb r1,[r0,#0x0]                        @ 0801cde6 0170
LAB_0801cde8:
    ldrb r2,[r6,#0x0]                        @ 0801cde8 3278
    cmp r2,#0x28                             @ 0801cdea 282a
    bne LAB_0801cdf8                         @ 0801cdec 04d1
    adds r1,r5,#0x0    @ 0801cdee 291c
    adds r1,#0x8d    @ 0801cdf0 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cdf2 0878
    adds r0,#0x1    @ 0801cdf4 0130
    strb r0,[r1,#0x0]                        @ 0801cdf6 0870
LAB_0801cdf8:
    ldrb r0,[r6,#0x0]                        @ 0801cdf8 3078
    adds r0,#0x1    @ 0801cdfa 0130
    strb r0,[r6,#0x0]                        @ 0801cdfc 3070
    b LAB_0801ceb6                           @ 0801cdfe 5ae0
run_vija_scene_state_machine_vija_obj_slot_seq:
    .word  vija_obj_slot_seq              @ 0801ce00 10dae309  ptr to 5-byte OBJ slot index sequence {01 03 00 02 04}
switchD_0801cb1a__caseD_6:
    bl tick_bg2_affine_anim_frame            @ 0801ce04 fff746fc
    adds r0,r5,#0x0    @ 0801ce08 281c
    adds r0,#0xb8    @ 0801ce0a b830
    ldrb r0,[r0,#0x0]                        @ 0801ce0c 0078
    cmp r0,#0x4                              @ 0801ce0e 0428
    bne LAB_0801ce40                         @ 0801ce10 16d1
    adds r1,r5,#0x0    @ 0801ce12 291c
    adds r1,#0x8e    @ 0801ce14 8e31
    movs r0,#0x0    @ 0801ce16 0020
    strb r0,[r1,#0x0]                        @ 0801ce18 0870
    adds r1,#0x1    @ 0801ce1a 0131
    strb r0,[r1,#0x0]                        @ 0801ce1c 0870
    movs r2,#0x80    @ 0801ce1e 8022
    lsls r2,r2,#0x13    @ 0801ce20 d204
    movs r3,#0xa0    @ 0801ce22 a023
    lsls r3,r3,#0x5    @ 0801ce24 5b01
    ldr r0, run_vija_scene_state_machine_dispcnt_obj_en_mask_c @ 0801ce26 0548
    ldrh r1,[r2,#0x0]                        @ 0801ce28 1188
    ands r0,r1    @ 0801ce2a 0840
    orrs r0,r3    @ 0801ce2c 1843
    strh r0,[r2,#0x0]                        @ 0801ce2e 1080
    adds r1,r5,#0x0    @ 0801ce30 291c
    adds r1,#0x8d    @ 0801ce32 8d31
    ldrb r0,[r1,#0x0]                        @ 0801ce34 0878
    adds r0,#0x1    @ 0801ce36 0130
    b LAB_0801cf2c                           @ 0801ce38 78e0
    .zero  0x2
run_vija_scene_state_machine_dispcnt_obj_en_mask_c:
    .word  DEMO_CLEAR_BITS_12_8           @ 0801ce3c ffe0ffff
LAB_0801ce40:
    adds r1,r5,#0x0    @ 0801ce40 291c
    adds r1,#0x8e    @ 0801ce42 8e31
    ldrb r0,[r1,#0x0]                        @ 0801ce44 0878
    b LAB_0801cf2a                           @ 0801ce46 70e0
switchD_0801cb1a__caseD_7:
    bl tick_bg2_affine_anim_frame            @ 0801ce48 fff724fc
    adds r0,r5,#0x0    @ 0801ce4c 281c
    adds r0,#0x8e    @ 0801ce4e 8e30
    ldrb r1,[r0,#0x0]                        @ 0801ce50 0178
    adds r4,r0,#0x0    @ 0801ce52 041c
    cmp r1,#0x3c                             @ 0801ce54 3c29
    beq LAB_0801ce5c                         @ 0801ce56 01d0
    cmp r1,#0x4b                             @ 0801ce58 4b29
    bne LAB_0801ce6a                         @ 0801ce5a 06d1
LAB_0801ce5c:
    movs r0,#0x3f    @ 0801ce5c 3f20
    movs r1,#0x0    @ 0801ce5e 0021
    bl gl_set_brightness                     @ 0801ce60 f7f74cfc
    movs r0,#0x3f    @ 0801ce64 3f20
    movs r1,#0x10    @ 0801ce66 1021
    b LAB_0801ce7e                           @ 0801ce68 09e0
LAB_0801ce6a:
    cmp r1,#0x41                             @ 0801ce6a 4129
    beq LAB_0801ce72                         @ 0801ce6c 01d0
    cmp r1,#0x50                             @ 0801ce6e 5029
    bne LAB_0801ce86                         @ 0801ce70 09d1
LAB_0801ce72:
    movs r0,#0x3f    @ 0801ce72 3f20
    movs r1,#0x10    @ 0801ce74 1021
    bl gl_set_brightness                     @ 0801ce76 f7f741fc
    movs r0,#0x3f    @ 0801ce7a 3f20
    movs r1,#0x0    @ 0801ce7c 0021
LAB_0801ce7e:
    movs r2,#0x4    @ 0801ce7e 0422
    bl gl_set_blend2_level                   @ 0801ce80 f7f7aafc
    b LAB_0801ceb0                           @ 0801ce84 14e0
LAB_0801ce86:
    cmp r1,#0x8c                             @ 0801ce86 8c29
    bne LAB_0801ceb0                         @ 0801ce88 12d1
    movs r0,#0x3f    @ 0801ce8a 3f20
    movs r1,#0x0    @ 0801ce8c 0021
    bl gl_set_brightness                     @ 0801ce8e f7f735fc
    movs r0,#0x3f    @ 0801ce92 3f20
    movs r1,#0x10    @ 0801ce94 1021
    movs r2,#0xf    @ 0801ce96 0f22
    bl gl_set_blend2_level                   @ 0801ce98 f7f79efc
    adds r1,r5,#0x0    @ 0801ce9c 291c
    adds r1,#0x8f    @ 0801ce9e 8f31
    movs r0,#0x0    @ 0801cea0 0020
    strb r0,[r1,#0x0]                        @ 0801cea2 0870
    movs r0,#0x3c    @ 0801cea4 3c20
    strb r0,[r4,#0x0]                        @ 0801cea6 2070
    subs r1,#0x2    @ 0801cea8 0239
    ldrb r0,[r1,#0x0]                        @ 0801ceaa 0878
    adds r0,#0x1    @ 0801ceac 0130
    strb r0,[r1,#0x0]                        @ 0801ceae 0870
LAB_0801ceb0:
    ldrb r0,[r4,#0x0]                        @ 0801ceb0 2078
    adds r0,#0x1    @ 0801ceb2 0130
    strb r0,[r4,#0x0]                        @ 0801ceb4 2070
LAB_0801ceb6:
    bl tick_all_vija_obj_anim_slots          @ 0801ceb6 fff711fe
    b switchD_0801cb1a__default              @ 0801ceba 43e0
switchD_0801cb1a__caseD_8:
    bl tick_bg2_affine_anim_frame            @ 0801cebc fff7eafb
    adds r1,r5,#0x0    @ 0801cec0 291c
    adds r1,#0x8e    @ 0801cec2 8e31
    ldrb r0,[r1,#0x0]                        @ 0801cec4 0878
    cmp r0,#0x0                              @ 0801cec6 0028
    bne LAB_0801cf2a                         @ 0801cec8 2fd1
    bl check_blend_transition_done           @ 0801ceca f7f713fd
    cmp r0,#0x0                              @ 0801cece 0028
    bne LAB_0801ceb6                         @ 0801ced0 f1d1
    adds r6,r5,#0x0    @ 0801ced2 2e1c
    adds r6,#0x8f    @ 0801ced4 8f36
    ldrb r4,[r6,#0x0]                        @ 0801ced6 3478
    cmp r4,#0x0                              @ 0801ced8 002c
    beq LAB_0801cee2                         @ 0801ceda 02d0
    cmp r4,#0x1                              @ 0801cedc 012c
    beq LAB_0801cf0c                         @ 0801cede 15d0
    b LAB_0801ceb6                           @ 0801cee0 e9e7
LAB_0801cee2:
    movs r0,#0x3f    @ 0801cee2 3f20
    movs r1,#0x10    @ 0801cee4 1021
    bl gl_set_brightness                     @ 0801cee6 f7f709fc
    movs r0,#0x3f    @ 0801ceea 3f20
    movs r1,#0x0    @ 0801ceec 0021
    movs r2,#0x1e    @ 0801ceee 1e22
    bl gl_set_blend2_level                   @ 0801cef0 f7f772fc
    movs r2,#0x80    @ 0801cef4 8022
    lsls r2,r2,#0x13    @ 0801cef6 d204
    ldr r0, run_vija_scene_state_machine_dispcnt_obj_en_mask_d @ 0801cef8 0348
    ldrh r1,[r2,#0x0]                        @ 0801cefa 1188
    ands r0,r1    @ 0801cefc 0840
    strh r0,[r2,#0x0]                        @ 0801cefe 1080
    movs r0,#0xa0    @ 0801cf00 a020
    lsls r0,r0,#0x13    @ 0801cf02 c004
    strh r4,[r0,#0x0]                        @ 0801cf04 0480
    b LAB_0801cdf8                           @ 0801cf06 77e7
run_vija_scene_state_machine_dispcnt_obj_en_mask_d:
    .word  DEMO_CLEAR_BITS_12_8           @ 0801cf08 ffe0ffff
LAB_0801cf0c:
    movs r0,#0x3f    @ 0801cf0c 3f20
    movs r1,#0x0    @ 0801cf0e 0021
    bl gl_set_brightness                     @ 0801cf10 f7f7f4fb
    movs r1,#0x10    @ 0801cf14 1021
    rsbs r1,r1,#0    @ 0801cf16 4942
    movs r0,#0x3f    @ 0801cf18 3f20
    movs r2,#0x1e    @ 0801cf1a 1e22
    bl gl_set_blend2_level                   @ 0801cf1c f7f75cfc
    adds r1,r5,#0x0    @ 0801cf20 291c
    adds r1,#0x8d    @ 0801cf22 8d31
    ldrb r0,[r1,#0x0]                        @ 0801cf24 0878
    adds r0,#0x1    @ 0801cf26 0130
    b LAB_0801cf2c                           @ 0801cf28 00e0
LAB_0801cf2a:
    subs r0,#0x1    @ 0801cf2a 0138
LAB_0801cf2c:
    strb r0,[r1,#0x0]                        @ 0801cf2c 0870
    b LAB_0801ceb6                           @ 0801cf2e c2e7
switchD_0801cb1a__caseD_9:
    bl check_blend_transition_done           @ 0801cf30 f7f7e0fc
    cmp r0,#0x0                              @ 0801cf34 0028
    bne switchD_0801cb1a__default            @ 0801cf36 05d1
    adds r1,r5,#0x0    @ 0801cf38 291c
    adds r1,#0x92    @ 0801cf3a 9231
    movs r0,#0x1    @ 0801cf3c 0120
    ldrb r7,[r1,#0x0]                        @ 0801cf3e 0f78
    orrs r0,r7    @ 0801cf40 3843
LAB_0801cf42:
    strb r0,[r1,#0x0]                        @ 0801cf42 0870
switchD_0801cb1a__default:
    bl copy_sprite_attr_table_to_oam         @ 0801cf44 f8f772f9
    bl init_gl_palette_slot_flags            @ 0801cf48 f8f70af9
    bl check_blend_transition_done           @ 0801cf4c f7f7d2fc
    cmp r0,#0x0                              @ 0801cf50 0028
    bne LAB_0801cf64                         @ 0801cf52 07d1
    adds r0,r5,#0x0    @ 0801cf54 281c
    adds r0,#0x92    @ 0801cf56 9230
    ldrb r0,[r0,#0x0]                        @ 0801cf58 0078
    lsls r0,r0,#0x1f    @ 0801cf5a c007
    cmp r0,#0x0                              @ 0801cf5c 0028
    beq LAB_0801cf64                         @ 0801cf5e 01d0
    movs r0,#0x1    @ 0801cf60 0120
    b LAB_0801cf6a                           @ 0801cf62 02e0
LAB_0801cf64:
    bl tick_blend_transition_step            @ 0801cf64 f7f7d6fc
    movs r0,#0x0    @ 0801cf68 0020
LAB_0801cf6a:
    add sp,#0x18                             @ 0801cf6a 06b0
    pop {r4,r5,r6,r7}                        @ 0801cf6c f0bc
    pop {r1}                                 @ 0801cf6e 02bc
    bx r1                                    @ 0801cf70 0847
    .zero  0x2

@ indeg=0, no direct caller; entered via function pointer table in scene frame dispatch. Structure fully symmetric with tick_scene_step_by_step_table_a (0x0801c254): reads gPrng+0x204 step index (bits[17:10]), multiplies by 4 to index step function table B (base 0x09e589b4 = ROM step table B), calls step function via invoke_r0; if step done increments step index +1 (mod 256) writes back to gPrng+0x204, returns r0=0; if table empty returns r0=1. Exit: pop {r4}; pop {r1}; bx r1.
@ 
@ Constants:
@ STEP_TABLE_BASE_B = 0x09e589b4 (ROM step table B base, 0x10 bytes after table A)
@ gPrng = 0x03000040
@ STEP_IDX_FIELD_OFFSET = 0x204 (gPrng + 0x81*4)
@ STEP_ADVANCE_MASK = 0xffc03fff
tick_scene_step_by_step_table_b:
    push {r4,lr}                             @ 0801cf74 10b5
    ldr r1, tick_scene_step_by_step_table_b_step_table @ 0801cf76 1049
    ldr r0, DWORD_0801cfbc                   @ 0801cf78 1048
    movs r2,#0x81    @ 0801cf7a 8122
    lsls r2,r2,#0x2    @ 0801cf7c 9200
    adds r4,r0,r2    @ 0801cf7e 8418
    ldr r0,[r4,#0x0]                         @ 0801cf80 2068
    lsls r0,r0,#0xa    @ 0801cf82 8002
    lsrs r0,r0,#0x18    @ 0801cf84 000e
    lsls r0,r0,#0x2    @ 0801cf86 8000
    adds r0,r0,r1    @ 0801cf88 4018
    ldr r0,[r0,#0x0]                         @ 0801cf8a 0068
    cmp r0,#0x0                              @ 0801cf8c 0028
    beq LAB_0801cfc4                         @ 0801cf8e 19d0
    bl invoke_r0                             @ 0801cf90 f1f01afb
    cmp r0,#0x0                              @ 0801cf94 0028
    beq LAB_0801cfae                         @ 0801cf96 0ad0
    ldr r2,[r4,#0x0]                         @ 0801cf98 2268
    lsls r1,r2,#0xa    @ 0801cf9a 9102
    lsrs r1,r1,#0x18    @ 0801cf9c 090e
    adds r1,#0x1    @ 0801cf9e 0131
    movs r0,#0xff    @ 0801cfa0 ff20
    ands r1,r0    @ 0801cfa2 0140
    lsls r1,r1,#0xe    @ 0801cfa4 8903
    ldr r0, tick_scene_step_by_step_table_b_step_advance_mask @ 0801cfa6 0648
    ands r0,r2    @ 0801cfa8 1040
    orrs r0,r1    @ 0801cfaa 0843
    str r0,[r4,#0x0]                         @ 0801cfac 2060
LAB_0801cfae:
    bl return_void_handler                   @ 0801cfae ddf091fa
    movs r0,#0x0    @ 0801cfb2 0020
    b LAB_0801cfc6                           @ 0801cfb4 07e0
    .zero  0x2
tick_scene_step_by_step_table_b_step_table:
    .word  0x09e589b4                     @ 0801cfb8 b489e509  ROM step table B base 0x09e589b4: 3 THUMB fn-ptrs +1 NULL
DWORD_0801cfbc:
    .word  gPrng                          @ 0801cfbc 40000003
tick_scene_step_by_step_table_b_step_advance_mask:
    .word  NAME_INPUT_PAGE_STATE_CLEAR    @ 0801cfc0 ff3fc0ff  bits[21:14] clear mask for step index field in gPrng+0x204
LAB_0801cfc4:
    movs r0,#0x1    @ 0801cfc4 0120
LAB_0801cfc6:
    pop {r4}                                 @ 0801cfc6 10bc
    pop {r1}                                 @ 0801cfc8 02bc
    bx r1                                    @ 0801cfca 0847

@ indeg=0, no direct caller; entered via function pointer table in scene frame dispatch. Structure fully symmetric with 0x0801cf74, using the same step table address (0x09e589b4): reads gPrng+0x204 step index (bits[17:10]), multiplies by 4 to index step function table B (base 0x09e589b4, shared with tick_scene_step_by_step_table_b), calls step function via invoke_r0; if step done increments step index +1 (mod 256) writes back to gPrng+0x204, returns r0=0; if table empty returns r0=1. Exit: pop {r4}; pop {r1}; bx r1 (Sub-case E).
@ 
@ Constants:
@ STEP_TABLE_BASE_B = 0x09e589b4 (same address as tick_scene_step_by_step_table_b; two separate entry points share same table)
@ gPrng = 0x03000040
@ STEP_IDX_FIELD_OFFSET = 0x204
@ STEP_ADVANCE_MASK = 0xffc03fff
tick_scene_step_by_step_table_c:
    push {r4,lr}                             @ 0801cfcc 10b5
    ldr r1, tick_scene_step_by_step_table_c_step_table @ 0801cfce 1049
    ldr r0, DWORD_0801d014                   @ 0801cfd0 1048
    movs r2,#0x81    @ 0801cfd2 8122
    lsls r2,r2,#0x2    @ 0801cfd4 9200
    adds r4,r0,r2    @ 0801cfd6 8418
    ldr r0,[r4,#0x0]                         @ 0801cfd8 2068
    lsls r0,r0,#0xa    @ 0801cfda 8002
    lsrs r0,r0,#0x18    @ 0801cfdc 000e
    lsls r0,r0,#0x2    @ 0801cfde 8000
    adds r0,r0,r1    @ 0801cfe0 4018
    ldr r0,[r0,#0x0]                         @ 0801cfe2 0068
    cmp r0,#0x0                              @ 0801cfe4 0028
    beq LAB_0801d01c                         @ 0801cfe6 19d0
    bl invoke_r0                             @ 0801cfe8 f1f0eefa
    cmp r0,#0x0                              @ 0801cfec 0028
    beq LAB_0801d006                         @ 0801cfee 0ad0
    ldr r2,[r4,#0x0]                         @ 0801cff0 2268
    lsls r1,r2,#0xa    @ 0801cff2 9102
    lsrs r1,r1,#0x18    @ 0801cff4 090e
    adds r1,#0x1    @ 0801cff6 0131
    movs r0,#0xff    @ 0801cff8 ff20
    ands r1,r0    @ 0801cffa 0140
    lsls r1,r1,#0xe    @ 0801cffc 8903
    ldr r0, tick_scene_step_by_step_table_c_step_advance_mask @ 0801cffe 0648
    ands r0,r2    @ 0801d000 1040
    orrs r0,r1    @ 0801d002 0843
    str r0,[r4,#0x0]                         @ 0801d004 2060
LAB_0801d006:
    bl return_void_handler                   @ 0801d006 ddf065fa
    movs r0,#0x0    @ 0801d00a 0020
    b LAB_0801d01e                           @ 0801d00c 07e0
    .zero  0x2
tick_scene_step_by_step_table_c_step_table:
    .word  0x09e589b4                     @ 0801d010 b489e509  ROM step table B base 0x09e589b4 (shared with table_b)
DWORD_0801d014:
    .word  gPrng                          @ 0801d014 40000003
tick_scene_step_by_step_table_c_step_advance_mask:
    .word  NAME_INPUT_PAGE_STATE_CLEAR    @ 0801d018 ff3fc0ff
LAB_0801d01c:
    movs r0,#0x1    @ 0801d01c 0120
LAB_0801d01e:
    pop {r4}                                 @ 0801d01e 10bc
    pop {r1}                                 @ 0801d020 02bc
    bx r1                                    @ 0801d022 0847
    ROM_INCBIN 0x1d024, 0x1c
    .word  0x0801d044                     @ 0801d040 44d00108
PTR_DAT_0801d044:
    .word  0x0801d0bc                     @ 0801d044 bcd00108
    .word  0x0801d0bc                     @ 0801d048 bcd00108
    .word  0x0801d0c0                     @ 0801d04c c0d00108
    .word  0x0801d0c4                     @ 0801d050 c4d00108
    .word  0x0801d0c4                     @ 0801d054 c4d00108
    .word  0x0801d0c4                     @ 0801d058 c4d00108
    .word  0x0801d0c4                     @ 0801d05c c4d00108
    .word  0x0801d0c4                     @ 0801d060 c4d00108
    .word  0x0801d0c4                     @ 0801d064 c4d00108
    .word  0x0801d0bc                     @ 0801d068 bcd00108
    .word  0x0801d0c4                     @ 0801d06c c4d00108
    .word  0x0801d0c4                     @ 0801d070 c4d00108
    .word  0x0801d0c4                     @ 0801d074 c4d00108
    .word  0x0801d0c4                     @ 0801d078 c4d00108
    .word  0x0801d0c4                     @ 0801d07c c4d00108
    .word  0x0801d0c4                     @ 0801d080 c4d00108
    .word  0x0801d0c4                     @ 0801d084 c4d00108
    .word  0x0801d0c4                     @ 0801d088 c4d00108
    .word  0x0801d0c4                     @ 0801d08c c4d00108
    .word  0x0801d0c4                     @ 0801d090 c4d00108
    .word  0x0801d0c4                     @ 0801d094 c4d00108
    .word  0x0801d0c4                     @ 0801d098 c4d00108
    .word  0x0801d0c4                     @ 0801d09c c4d00108
    .word  0x0801d0c4                     @ 0801d0a0 c4d00108
    .word  0x0801d0c4                     @ 0801d0a4 c4d00108
    .word  0x0801d0c4                     @ 0801d0a8 c4d00108
    .word  0x0801d0c4                     @ 0801d0ac c4d00108
    .word  0x0801d0c4                     @ 0801d0b0 c4d00108
    .word  0x0801d0c4                     @ 0801d0b4 c4d00108
    .word  0x0801d0c0                     @ 0801d0b8 c0d00108
DAT_0801d0bc:
    .byte  0x30, 0x20, 0x00, 0xe0, 0x50, 0x20, 0x20, 0x60, 0x10, 0xbc, 0x01, 0xbc, 0x00, 0x47, 0x00, 0x00

@ Called by write_tile_attr_strip_4wide in inner loop for each of 4 sub-elements (r4 in [0..3]) of a map entry. Accepts r0/r1 packed coordinate fields and r2 attribute byte, r3 packed params; computes BG char data VRAM address (base 0x06004000) via multi-step bit shifts, loads 4-byte tile entry, writes r2 attribute byte into the specified position then writes back to VRAM. Heavy use of hi-reg to sp move instructions (.hword 0x466x = mov rN,sp) to stage intermediate bytes on stack. Low-level tile attribute write utility. Exit: pop {r0}; bx r0 (lr saved on stack, Sub-case E - r0 is not a return value).
@ 
@ Constants:
@ VRAM_CHAR_BASE = 0x06004000 (BG char data VRAM base)
@ SUB_ELEM_COUNT = 4 (4 sub-elements per map entry, caller loop range [0..3])
write_tile_attr_byte_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 0801d0cc f0b5
    .hword 0x4647    @ 0801d0ce 4746
    push {r7}                                @ 0801d0d0 80b4
    sub sp,#0x4                              @ 0801d0d2 81b0
    lsls r5,r3,#0x10    @ 0801d0d4 1d04
    lsrs r5,r5,#0x10    @ 0801d0d6 2d0c
    lsrs r3,r3,#0x10    @ 0801d0d8 1b0c
    lsls r3,r3,#0x18    @ 0801d0da 1b06
    lsrs r3,r3,#0x18    @ 0801d0dc 1b0e
    lsls r4,r0,#0xd    @ 0801d0de 4403
    lsrs r4,r4,#0x10    @ 0801d0e0 240c
    lsls r6,r1,#0xd    @ 0801d0e2 4e03
    lsrs r6,r6,#0x10    @ 0801d0e4 360c
    movs r7,#0x7    @ 0801d0e6 0727
    .hword 0x46b8    @ 0801d0e8 b846
    .hword 0x4647    @ 0801d0ea 4746
    ands r0,r7    @ 0801d0ec 3840
    lsls r0,r0,#0x10    @ 0801d0ee 0004
    ands r1,r7    @ 0801d0f0 3940
    lsls r4,r4,#0x1    @ 0801d0f2 6400
    adds r5,r5,r4    @ 0801d0f4 2d19
    muls r3,r6    @ 0801d0f6 7343
    lsls r3,r3,#0x1    @ 0801d0f8 5b00
    adds r5,r5,r3    @ 0801d0fa ed18
    lsls r5,r5,#0x5    @ 0801d0fc 6d01
    ldr r3, write_tile_attr_byte_to_vram_vram_char_base @ 0801d0fe 164b
    adds r5,r5,r3    @ 0801d100 ed18
    lsrs r3,r0,#0x12    @ 0801d102 830c
    lsls r3,r3,#0x2    @ 0801d104 9b00
    adds r5,r5,r3    @ 0801d106 ed18
    lsls r1,r1,#0x3    @ 0801d108 c900
    adds r5,r5,r1    @ 0801d10a 6d18
    ldr r3,[r5,#0x0]                         @ 0801d10c 2b68
    .hword 0x4669    @ 0801d10e 6946
    strb r3,[r1,#0x0]                        @ 0801d110 0b70
    .hword 0x466c    @ 0801d112 6c46
    lsls r1,r3,#0x10    @ 0801d114 1904
    lsrs r1,r1,#0x18    @ 0801d116 090e
    strb r1,[r4,#0x1]                        @ 0801d118 6170
    .hword 0x4669    @ 0801d11a 6946
    lsrs r3,r3,#0x10    @ 0801d11c 1b0c
    strb r3,[r1,#0x2]                        @ 0801d11e 8b70
    lsrs r3,r3,#0x8    @ 0801d120 1b0a
    strb r3,[r1,#0x3]                        @ 0801d122 cb70
    movs r1,#0xc0    @ 0801d124 c021
    lsls r1,r1,#0xa    @ 0801d126 8902
    ands r1,r0    @ 0801d128 0140
    lsrs r1,r1,#0x10    @ 0801d12a 090c
    .hword 0x466f    @ 0801d12c 6f46
    adds r0,r7,r1    @ 0801d12e 7818
    strb r2,[r0,#0x0]                        @ 0801d130 0270
    .hword 0x466a    @ 0801d132 6a46
    .hword 0x4668    @ 0801d134 6846
    ldrb r1,[r0,#0x1]                        @ 0801d136 4178
    lsls r1,r1,#0x8    @ 0801d138 0902
    ldrb r2,[r2,#0x0]                        @ 0801d13a 1278
    orrs r1,r2    @ 0801d13c 1143
    ldrb r2,[r0,#0x2]                        @ 0801d13e 8278
    ldrb r0,[r0,#0x3]                        @ 0801d140 c078
    lsls r0,r0,#0x8    @ 0801d142 0002
    orrs r2,r0    @ 0801d144 0243
    lsls r2,r2,#0x10    @ 0801d146 1204
    orrs r1,r2    @ 0801d148 1143
    str r1,[r5,#0x0]                         @ 0801d14a 2960
    add sp,#0x4                              @ 0801d14c 01b0
    pop {r3}                                 @ 0801d14e 08bc
    .hword 0x4698    @ 0801d150 9846
    pop {r4,r5,r6,r7}                        @ 0801d152 f0bc
    pop {r0}                                 @ 0801d154 01bc
    bx r0                                    @ 0801d156 0047
write_tile_attr_byte_to_vram_vram_char_base:
    .word  BG_CHAR_VRAM_CB2               @ 0801d158 00400006  BG charblock 2 base: 0x06004000 = GBA_VRAM_BASE + 0x4000

@ Called by apply_palette_and_tile_attr_strips (tile map update function). Accepts r0 = packed param, extracts bits[11:4] (8-bit palette slot index bank_idx [0..255]), computes target address = 0x05000000 + bank_idx*32 (PALRAM, 32 bytes per slot = 16 RGB15 colors), uses r1 as source address and calls copy_memory_dma3_with_cpu_fallback to copy 0x20 bytes (1 sixteen-color palette bank). Exit: pop {r0}; bx r0 (Sub-case E, r0=lr).
@ 
@ Constants:
@ PALRAM_BASE = 0x05000000 (0xa0 << 0x13 = 0xa0 * 524288; python: hex(0xa0<<0x13) -> 0x5000000)
@ PALETTE_BANK_SIZE = 0x20 (32 bytes = 16 u16 colors = 1 sixteen-color palette bank)
@ BANK_IDX_BITS = bits[11:4] of r0 (8 bits, [0..255])
copy_palette_bank_by_slot:
    push {lr}                                @ 0801d15c 00b5
    lsls r0,r0,#0x10    @ 0801d15e 0004
    lsrs r0,r0,#0x14    @ 0801d160 000d
    lsls r0,r0,#0x5    @ 0801d162 4001
    movs r2,#0xa0    @ 0801d164 a022
    lsls r2,r2,#0x13    @ 0801d166 d204
    adds r0,r0,r2    @ 0801d168 8018
    movs r2,#0x20    @ 0801d16a 2022
    bl copy_memory_dma3_with_cpu_fallback    @ 0801d16c d7f0ccfe
    pop {r0}                                 @ 0801d170 01bc
    bx r0                                    @ 0801d172 0047

@ Writes a 4-column-wide tile attribute strip into VRAM. r0 high 16 bits = col_base_offset (saved to r10), low 16 bits = start_col (saved to sp+8); r1 = palette/attr base value (u16, written to sp+0); r2 = source tile attribute halfword array pointer; r3 = VRAM target row base pointer (saved to sp+4). Outer loop 8 rows (r9 from 0, cmp #7 bls), inner loop 4 columns (r4=0..3): reads halfword from r2, shifts right by col*4 to extract 4-bit nibble; if nibble != 0 calls write_tile_attr_byte_to_vram(col_base+r4, row_base+r5, nibble+palette_base, r3). Outer loop increments r2 by 2 each row. Called 4 consecutive times by 0x0801d208 with different column segments and attr bases. Returns void (Pattern B).
@ 
@ Params: r0=u32 packed_col_info (hi16=col_base_offset [0..N], lo16=start_col [0..N]); r1=u16 palette_attr_base [0..0xff]; r2=ptr u16[] tile attribute nibble stream; r3=ptr u8[] VRAM row target base
@ Returns: void (Pattern B: pop {r0}; bx r0)
@ Side effects: via write_tile_attr_byte_to_vram: up to 4*8=32 tile attribute bytes written to VRAM
@ Constants: COLS_PER_STRIP=4; ROWS_PER_STRIP=8
write_tile_attr_strip_4wide:
    push {r4,r5,r6,r7,lr}                    @ 0801d174 f0b5
    .hword 0x4657    @ 0801d176 5746
    .hword 0x464e    @ 0801d178 4e46
    .hword 0x4645    @ 0801d17a 4546
    push {r5,r6,r7}                          @ 0801d17c e0b4
    sub sp,#0x10                             @ 0801d17e 84b0
    str r3,[sp,#0x4]                         @ 0801d180 0193
    lsls r1,r1,#0x10    @ 0801d182 0904
    lsrs r1,r1,#0x10    @ 0801d184 090c
    str r1,[sp,#0x0]                         @ 0801d186 0091
    lsls r1,r0,#0x10    @ 0801d188 0104
    lsrs r1,r1,#0x10    @ 0801d18a 090c
    str r1,[sp,#0x8]                         @ 0801d18c 0291
    lsrs r0,r0,#0x10    @ 0801d18e 000c
    .hword 0x4682    @ 0801d190 8246
    cmp r2,#0x0                              @ 0801d192 002a
    beq LAB_0801d1f6                         @ 0801d194 2fd0
    movs r0,#0x0    @ 0801d196 0020
    .hword 0x4681    @ 0801d198 8146
LAB_0801d19a:
    movs r5,#0x0    @ 0801d19a 0025
    .hword 0x4649    @ 0801d19c 4946
    adds r1,#0x1    @ 0801d19e 0131
    str r1,[sp,#0xc]                         @ 0801d1a0 0391
LAB_0801d1a2:
    ldrh r6,[r2,#0x0]                        @ 0801d1a2 1688
    movs r4,#0x0    @ 0801d1a4 0024
    adds r7,r2,#0x2    @ 0801d1a6 971c
    adds r0,r5,#0x1    @ 0801d1a8 681c
    .hword 0x4680    @ 0801d1aa 8046
LAB_0801d1ac:
    lsls r0,r4,#0x2    @ 0801d1ac a000
    adds r2,r6,#0x0    @ 0801d1ae 321c
    asrs r2,r0    @ 0801d1b0 0241
    movs r0,#0xf    @ 0801d1b2 0f20
    ands r2,r0    @ 0801d1b4 0240
    cmp r2,#0x0                              @ 0801d1b6 002a
    beq LAB_0801d1d4                         @ 0801d1b8 0cd0
    ldr r1,[sp,#0x8]                         @ 0801d1ba 0299
    adds r0,r1,r4    @ 0801d1bc 0819
    lsls r1,r5,#0x2    @ 0801d1be a900
    adds r0,r0,r1    @ 0801d1c0 4018
    ldr r1,[sp,#0x0]                         @ 0801d1c2 0099
    adds r2,r2,r1    @ 0801d1c4 5218
    lsls r2,r2,#0x18    @ 0801d1c6 1206
    lsrs r2,r2,#0x18    @ 0801d1c8 120e
    .hword 0x4651    @ 0801d1ca 5146
    add r1,r9                                @ 0801d1cc 4944
    ldr r3,[sp,#0x4]                         @ 0801d1ce 019b
    bl write_tile_attr_byte_to_vram          @ 0801d1d0 fff77cff
LAB_0801d1d4:
    adds r0,r4,#0x1    @ 0801d1d4 601c
    lsls r0,r0,#0x10    @ 0801d1d6 0004
    lsrs r4,r0,#0x10    @ 0801d1d8 040c
    cmp r4,#0x3                              @ 0801d1da 032c
    bls LAB_0801d1ac                         @ 0801d1dc e6d9
    adds r2,r7,#0x0    @ 0801d1de 3a1c
    .hword 0x4641    @ 0801d1e0 4146
    lsls r0,r1,#0x10    @ 0801d1e2 0804
    lsrs r5,r0,#0x10    @ 0801d1e4 050c
    cmp r5,#0x1                              @ 0801d1e6 012d
    bls LAB_0801d1a2                         @ 0801d1e8 dbd9
    ldr r1,[sp,#0xc]                         @ 0801d1ea 0399
    lsls r0,r1,#0x10    @ 0801d1ec 0804
    lsrs r0,r0,#0x10    @ 0801d1ee 000c
    .hword 0x4681    @ 0801d1f0 8146
    cmp r0,#0x7                              @ 0801d1f2 0728
    bls LAB_0801d19a                         @ 0801d1f4 d1d9
LAB_0801d1f6:
    add sp,#0x10                             @ 0801d1f6 04b0
    pop {r3,r4,r5}                           @ 0801d1f8 38bc
    .hword 0x4698    @ 0801d1fa 9846
    .hword 0x46a1    @ 0801d1fc a146
    .hword 0x46aa    @ 0801d1fe aa46
    pop {r4,r5,r6,r7}                        @ 0801d200 f0bc
    pop {r0}                                 @ 0801d202 01bc
    bx r0                                    @ 0801d204 0047
    .zero  0x2

@ Applies one palette bank + four 4-wide tile attribute strips. r2=palette_slot_packed saved to r9 @ 0801d216; r3=palette_src saved to r8 @ 0801d218. Calls copy_palette_bank_by_slot to copy palette bank to PALRAM, then calls write_tile_attr_strip_4wide four times with r8 incrementing by 0x20 each call (4 segments of 8 rows x 4 cols). Typical use: card image VRAM refresh combining palette + tile attributes. Returns void (Pattern B: pop {r0}; bx r0 @ 0801d28a).
@ 
@ Constants:
@ - COL_STRIDE = 0x20
@ - COLS_PER_STRIP = 4
@ - ROWS_PER_STRIP = 8
apply_palette_and_tile_attr_strips:
    push {r4,r5,r6,r7,lr}                    @ 0801d208 f0b5
    .hword 0x4657    @ 0801d20a 5746
    .hword 0x464e    @ 0801d20c 4e46
    .hword 0x4645    @ 0801d20e 4546
    push {r5,r6,r7}                          @ 0801d210 e0b4
    adds r6,r0,#0x0    @ 0801d212 061c
    adds r7,r1,#0x0    @ 0801d214 0f1c
    .hword 0x4691    @ 0801d216 9146
    .hword 0x4698    @ 0801d218 9846
    ldr r1,[sp,#0x20]                        @ 0801d21a 0899
    .hword 0x4648    @ 0801d21c 4846
    lsls r0,r0,#0x10    @ 0801d21e 0004
    lsrs r0,r0,#0x10    @ 0801d220 000c
    .hword 0x4681    @ 0801d222 8146
    lsls r4,r6,#0x10    @ 0801d224 3404
    lsrs r4,r4,#0x10    @ 0801d226 240c
    lsrs r6,r6,#0x10    @ 0801d228 360c
    bl copy_palette_bank_by_slot             @ 0801d22a fff797ff
    lsls r5,r6,#0x10    @ 0801d22e 3504
    adds r0,r4,#0x0    @ 0801d230 201c
    orrs r0,r5    @ 0801d232 2843
    .hword 0x4649    @ 0801d234 4946
    .hword 0x4642    @ 0801d236 4246
    adds r3,r7,#0x0    @ 0801d238 3b1c
    bl write_tile_attr_strip_4wide           @ 0801d23a fff79bff
    movs r0,#0x20    @ 0801d23e 2020
    add r8,r0                                @ 0801d240 8044
    movs r0,#0x8    @ 0801d242 0820
    adds r0,r0,r4    @ 0801d244 0019
    .hword 0x4682    @ 0801d246 8246
    orrs r5,r0    @ 0801d248 0543
    adds r0,r5,#0x0    @ 0801d24a 281c
    .hword 0x4649    @ 0801d24c 4946
    .hword 0x4642    @ 0801d24e 4246
    adds r3,r7,#0x0    @ 0801d250 3b1c
    bl write_tile_attr_strip_4wide           @ 0801d252 fff78fff
    movs r0,#0x20    @ 0801d256 2020
    add r8,r0                                @ 0801d258 8044
    adds r6,#0x8    @ 0801d25a 0836
    lsls r6,r6,#0x10    @ 0801d25c 3604
    orrs r4,r6    @ 0801d25e 3443
    adds r0,r4,#0x0    @ 0801d260 201c
    .hword 0x4649    @ 0801d262 4946
    .hword 0x4642    @ 0801d264 4246
    adds r3,r7,#0x0    @ 0801d266 3b1c
    bl write_tile_attr_strip_4wide           @ 0801d268 fff784ff
    movs r0,#0x20    @ 0801d26c 2020
    add r8,r0                                @ 0801d26e 8044
    .hword 0x4650    @ 0801d270 5046
    orrs r0,r6    @ 0801d272 3043
    .hword 0x4682    @ 0801d274 8246
    .hword 0x4649    @ 0801d276 4946
    .hword 0x4642    @ 0801d278 4246
    adds r3,r7,#0x0    @ 0801d27a 3b1c
    bl write_tile_attr_strip_4wide           @ 0801d27c fff77aff
    pop {r3,r4,r5}                           @ 0801d280 38bc
    .hword 0x4698    @ 0801d282 9846
    .hword 0x46a1    @ 0801d284 a146
    .hword 0x46aa    @ 0801d286 aa46
    pop {r4,r5,r6,r7}                        @ 0801d288 f0bc
    pop {r0}                                 @ 0801d28a 01bc
    bx r0                                    @ 0801d28c 0047
    .zero  0x2

@ @ 6bpp source -> BG char VRAM tile layout. 6 input bytes -> 8 output pixels
@ @ (3 src halfwords -> 4 dst halfwords). Writes to BG charblock 2 (0x06004000).
@ @ r0/r1: tile coord params; r2: packed tile attribute; operates on card image data.
@ @ Parameters: r5=src_ptr (6bpp card image), r6=VRAM dst tile base.
@ @ Returns void (pop {r0}; bx r0, Sub-case E).
decode_card_image_6bpp:
    push {r4,r5,r6,r7,lr}                    @ 0801d290 f0b5
    .hword 0x4657    @ 0801d292 5746
    .hword 0x464e    @ 0801d294 4e46
    .hword 0x4645    @ 0801d296 4546
    push {r5,r6,r7}                          @ 0801d298 e0b4
    sub sp,#0x8                              @ 0801d29a 82b0
    adds r4,r0,#0x0    @ 0801d29c 041c
    ldr r0,[sp,#0x28]                        @ 0801d29e 0a98
    lsls r1,r1,#0x10    @ 0801d2a0 0904
    lsls r2,r2,#0x10    @ 0801d2a2 1204
    lsls r3,r3,#0x10    @ 0801d2a4 1b04
    lsls r0,r0,#0x10    @ 0801d2a6 0004
    lsrs r1,r1,#0xf    @ 0801d2a8 c90b
    adds r4,r4,r1    @ 0801d2aa 6418
    movs r7,#0x0    @ 0801d2ac 0027
    lsrs r5,r3,#0x11    @ 0801d2ae 5d0c
    ldr r1, PTR_card_image_index_0801d420    @ 0801d2b0 5b49
    .hword 0x4689    @ 0801d2b2 8946
    lsrs r1,r0,#0x14    @ 0801d2b4 010d
    .hword 0x468c    @ 0801d2b6 8c46
    lsrs r2,r2,#0xf    @ 0801d2b8 d20b
    .hword 0x4690    @ 0801d2ba 9046
    lsrs r3,r3,#0xb    @ 0801d2bc db0a
    .hword 0x469a    @ 0801d2be 9a46
    lsls r0,r0,#0x8    @ 0801d2c0 0002
    str r0,[sp,#0x0]                         @ 0801d2c2 0090
LAB_0801d2c4:
    movs r3,#0x0    @ 0801d2c4 0023
    adds r6,r4,#0x0    @ 0801d2c6 261c
    adds r6,#0x40    @ 0801d2c8 4036
LAB_0801d2ca:
    lsls r2,r3,#0x1    @ 0801d2ca 5a00
    adds r2,r2,r4    @ 0801d2cc 1219
    adds r1,r5,#0x0    @ 0801d2ce 291c
    adds r0,r1,#0x1    @ 0801d2d0 481c
    lsls r0,r0,#0x10    @ 0801d2d2 0004
    lsrs r5,r0,#0x10    @ 0801d2d4 050c
    strh r1,[r2,#0x0]                        @ 0801d2d6 1180
    adds r0,r3,#0x1    @ 0801d2d8 581c
    lsls r0,r0,#0x10    @ 0801d2da 0004
    lsrs r3,r0,#0x10    @ 0801d2dc 030c
    cmp r3,#0x9                              @ 0801d2de 092b
    bls LAB_0801d2ca                         @ 0801d2e0 f3d9
    adds r4,r6,#0x0    @ 0801d2e2 341c
    adds r0,r7,#0x1    @ 0801d2e4 781c
    lsls r0,r0,#0x10    @ 0801d2e6 0004
    lsrs r7,r0,#0x10    @ 0801d2e8 070c
    cmp r7,#0x9                              @ 0801d2ea 092f
    bls LAB_0801d2c4                         @ 0801d2ec ead9
    .hword 0x4662    @ 0801d2ee 6246
    lsls r1,r2,#0x5    @ 0801d2f0 5101
    movs r0,#0xa0    @ 0801d2f2 a020
    lsls r0,r0,#0x13    @ 0801d2f4 c004
    adds r4,r1,r0    @ 0801d2f6 0c18
    .hword 0x464d    @ 0801d2f8 4d46
    .hword 0x4642    @ 0801d2fa 4246
    movs r3,#0x0    @ 0801d2fc 0023
    ldr r0, decode_card_image_6bpp_rom_region_code_addr @ 0801d2fe 4948
    ldrh r0,[r0,#0x0]                        @ 0801d300 0088
    lsrs r0,r0,#0x8    @ 0801d302 000a
    cmp r0,#0x4a                             @ 0801d304 4a28
    bne LAB_0801d318                         @ 0801d306 07d1
    ldr r1, decode_card_image_6bpp_ewram_base @ 0801d308 4749
    ldr r0, decode_card_image_6bpp_gsettings_offset @ 0801d30a 4848
    adds r1,r1,r0    @ 0801d30c 0918
    movs r0,#0x7    @ 0801d30e 0720
    ldrb r1,[r1,#0x0]                        @ 0801d310 0978
    ands r0,r1    @ 0801d312 0840
    cmp r0,#0x0                              @ 0801d314 0028
    beq LAB_0801d31a                         @ 0801d316 00d0
LAB_0801d318:
    movs r3,#0x1    @ 0801d318 0123
LAB_0801d31a:
    orrs r2,r3    @ 0801d31a 1a43
    lsls r0,r2,#0x1    @ 0801d31c 5000
    adds r0,r5,r0    @ 0801d31e 2818
    ldrh r0,[r0,#0x0]                        @ 0801d320 0088
    lsls r1,r0,#0x7    @ 0801d322 c101
    ldr r2, PTR_card_image_palettes_0801d430 @ 0801d324 424a
    adds r1,r1,r2    @ 0801d326 8918
    adds r0,r4,#0x0    @ 0801d328 201c
    movs r2,#0x80    @ 0801d32a 8022
    bl copy_memory_dma3_with_cpu_fallback    @ 0801d32c d7f0ecfd
    ldr r4, PTR_card_image_index_0801d420    @ 0801d330 3b4c
    .hword 0x4642    @ 0801d332 4246
    movs r3,#0x0    @ 0801d334 0023
    ldr r0, decode_card_image_6bpp_rom_region_code_addr @ 0801d336 3b48
    ldrh r0,[r0,#0x0]                        @ 0801d338 0088
    lsrs r0,r0,#0x8    @ 0801d33a 000a
    cmp r0,#0x4a                             @ 0801d33c 4a28
    bne LAB_0801d350                         @ 0801d33e 07d1
    ldr r1, decode_card_image_6bpp_ewram_base @ 0801d340 3949
    ldr r5, decode_card_image_6bpp_gsettings_offset @ 0801d342 3a4d
    adds r1,r1,r5    @ 0801d344 4919
    movs r0,#0x7    @ 0801d346 0720
    ldrb r1,[r1,#0x0]                        @ 0801d348 0978
    ands r0,r1    @ 0801d34a 0840
    cmp r0,#0x0                              @ 0801d34c 0028
    beq LAB_0801d352                         @ 0801d34e 00d0
LAB_0801d350:
    movs r3,#0x1    @ 0801d350 0123
LAB_0801d352:
    orrs r3,r2    @ 0801d352 1343
    lsls r0,r3,#0x1    @ 0801d354 5800
    adds r0,r4,r0    @ 0801d356 2018
    ldrh r2,[r0,#0x0]                        @ 0801d358 0288
    lsls r1,r2,#0x2    @ 0801d35a 9100
    adds r1,r1,r2    @ 0801d35c 8918
    lsls r0,r1,#0x4    @ 0801d35e 0801
    subs r0,r0,r1    @ 0801d360 401a
    lsls r0,r0,#0x6    @ 0801d362 8001
    ldr r1, PTR_card_image_tiles_0801d434    @ 0801d364 3349
    adds r6,r0,r1    @ 0801d366 4618
    ldr r5, decode_card_image_6bpp_vram_char_base @ 0801d368 334d
    add r5,r10                               @ 0801d36a 5544
    movs r7,#0x0    @ 0801d36c 0027
    movs r4,#0x3f    @ 0801d36e 3f24
    .hword 0x46a4    @ 0801d370 a446
    movs r0,#0xfc    @ 0801d372 fc20
    lsls r0,r0,#0x4    @ 0801d374 0001
    .hword 0x4680    @ 0801d376 8046
    ldr r1, decode_card_image_6bpp_tile_x_low_mask @ 0801d378 3049
    .hword 0x4689    @ 0801d37a 8946
LAB_0801d37c:
    ldrh r2,[r6,#0x0]                        @ 0801d37c 3288
    ldrh r3,[r6,#0x2]                        @ 0801d37e 7388
    ldrh r4,[r6,#0x4]                        @ 0801d380 b488
    str r4,[sp,#0x4]                         @ 0801d382 0194
    adds r1,r2,#0x0    @ 0801d384 111c
    .hword 0x4660    @ 0801d386 6046
    ands r1,r0    @ 0801d388 0140
    adds r0,r2,#0x0    @ 0801d38a 101c
    .hword 0x4644    @ 0801d38c 4446
    ands r0,r4    @ 0801d38e 2040
    lsls r0,r0,#0x2    @ 0801d390 8000
    orrs r1,r0    @ 0801d392 0143
    strh r1,[r5,#0x0]                        @ 0801d394 2980
    lsrs r2,r2,#0xc    @ 0801d396 120b
    movs r1,#0x3    @ 0801d398 0321
    adds r0,r3,#0x0    @ 0801d39a 181c
    ands r0,r1    @ 0801d39c 0840
    lsls r0,r0,#0x4    @ 0801d39e 0001
    orrs r2,r0    @ 0801d3a0 0243
    movs r0,#0xfc    @ 0801d3a2 fc20
    ands r0,r3    @ 0801d3a4 1840
    lsls r0,r0,#0x6    @ 0801d3a6 8001
    orrs r2,r0    @ 0801d3a8 0243
    strh r2,[r5,#0x2]                        @ 0801d3aa 6a80
    lsrs r3,r3,#0x8    @ 0801d3ac 1b0a
    adds r2,r3,#0x0    @ 0801d3ae 1a1c
    .hword 0x4660    @ 0801d3b0 6046
    ands r2,r0    @ 0801d3b2 0240
    lsrs r3,r3,#0x6    @ 0801d3b4 9b09
    movs r1,#0xf    @ 0801d3b6 0f21
    ldr r0,[sp,#0x4]                         @ 0801d3b8 0198
    ands r0,r1    @ 0801d3ba 0840
    lsls r0,r0,#0x2    @ 0801d3bc 8000
    orrs r3,r0    @ 0801d3be 0343
    lsls r3,r3,#0x8    @ 0801d3c0 1b02
    orrs r2,r3    @ 0801d3c2 1a43
    strh r2,[r5,#0x4]                        @ 0801d3c4 aa80
    ldr r1,[sp,#0x4]                         @ 0801d3c6 0199
    lsrs r4,r1,#0x4    @ 0801d3c8 0c09
    adds r0,r4,#0x0    @ 0801d3ca 201c
    .hword 0x4662    @ 0801d3cc 6246
    ands r0,r2    @ 0801d3ce 1040
    .hword 0x4641    @ 0801d3d0 4146
    ands r4,r1    @ 0801d3d2 0c40
    lsls r4,r4,#0x2    @ 0801d3d4 a400
    orrs r0,r4    @ 0801d3d6 2043
    strh r0,[r5,#0x6]                        @ 0801d3d8 e880
    adds r6,#0x6    @ 0801d3da 0636
    adds r5,#0x8    @ 0801d3dc 0835
    adds r0,r7,#0x1    @ 0801d3de 781c
    lsls r0,r0,#0x10    @ 0801d3e0 0004
    lsrs r7,r0,#0x10    @ 0801d3e2 070c
    cmp r7,r9                                @ 0801d3e4 4f45
    bls LAB_0801d37c                         @ 0801d3e6 c9d9
    ldr r4, decode_card_image_6bpp_vram_char_base @ 0801d3e8 134c
    add r4,r10                               @ 0801d3ea 5444
    movs r7,#0x0    @ 0801d3ec 0027
    ldr r3, decode_card_image_6bpp_tile_xy_6bit_mask @ 0801d3ee 144b
    ldr r2,[sp,#0x0]                         @ 0801d3f0 009a
    lsrs r0,r2,#0x18    @ 0801d3f2 100e
    lsls r1,r0,#0x8    @ 0801d3f4 0102
    orrs r1,r0    @ 0801d3f6 0143
    ldr r2, decode_card_image_6bpp_attr_packed_mask @ 0801d3f8 124a
LAB_0801d3fa:
    adds r0,r3,#0x0    @ 0801d3fa 181c
    ldrh r5,[r4,#0x0]                        @ 0801d3fc 2588
    ands r0,r5    @ 0801d3fe 2840
    adds r0,r0,r1    @ 0801d400 4018
    strh r0,[r4,#0x0]                        @ 0801d402 2080
    adds r4,#0x2    @ 0801d404 0234
    adds r0,r7,#0x1    @ 0801d406 781c
    lsls r0,r0,#0x10    @ 0801d408 0004
    lsrs r7,r0,#0x10    @ 0801d40a 070c
    cmp r7,r2                                @ 0801d40c 9742
    bls LAB_0801d3fa                         @ 0801d40e f4d9
    add sp,#0x8                              @ 0801d410 02b0
    pop {r3,r4,r5}                           @ 0801d412 38bc
    .hword 0x4698    @ 0801d414 9846
    .hword 0x46a1    @ 0801d416 a146
    .hword 0x46aa    @ 0801d418 aa46
    pop {r4,r5,r6,r7}                        @ 0801d41a f0bc
    pop {r0}                                 @ 0801d41c 01bc
    bx r0                                    @ 0801d41e 0047
PTR_card_image_index_0801d420:
    .word  card_image_index               @ 0801d420 005c5b09
decode_card_image_6bpp_rom_region_code_addr:
    .word  ROM_REGION_CODE_ADDR           @ 0801d424 ae000008
decode_card_image_6bpp_ewram_base:
    .word  EWRAM_BASE                     @ 0801d428 00000002
decode_card_image_6bpp_gsettings_offset:
    .word  GSETTINGS_OFFSET               @ 0801d42c 2c6c0000
PTR_card_image_palettes_0801d430:
    .word  card_image_palettes            @ 0801d430 c0764c08
PTR_card_image_tiles_0801d434:
    .word  card_image_tiles               @ 0801d434 40065108
decode_card_image_6bpp_vram_char_base:
    .word  BG_CHAR_VRAM_CB2               @ 0801d438 00400006
decode_card_image_6bpp_tile_x_low_mask:
    .word  0x0000031f                     @ 0801d43c 1f030000  0x31f: low-9-bit tile index mask for BG char addr compute
decode_card_image_6bpp_tile_xy_6bit_mask:
    .word  0x00003f3f                     @ 0801d440 3f3f0000  0x3f3f: dual-6-bit mask for tile grid x/y coordinate fields
decode_card_image_6bpp_attr_packed_mask:
    .word  0x00000c7f                     @ 0801d444 7f0c0000  0xc7f: packed tile attribute field mask

@ p1: FUN_0801e640 的首个 bl
card_info_page_enter_with_card_id:
    push {lr}                                @ 0801d448 00b5
    ldr r0, DAT_0801d458                     @ 0801d44a 0348
    movs r1,#0x30    @ 0801d44c 3021
    bl zero_fill_by_halfword                 @ 0801d44e d7f011fd
    pop {r0}                                 @ 0801d452 01bc
    bx r0                                    @ 0801d454 0047
    .zero  0x2
DAT_0801d458:
    .word  0x0201afb0                     @ 0801d458 b0af0102

@ p1: 写 BG0CNT=0x0086, 清 BG0 VRAM
card_info_page_init_bg0:
    push {r4,lr}                             @ 0801d45c 10b5
    ldr r0, PTR_gPrng_0801d4e4               @ 0801d45e 2148
    movs r1,#0xba    @ 0801d460 ba21
    lsls r1,r1,#0x1    @ 0801d462 4900
    adds r0,r0,r1    @ 0801d464 4018
    movs r1,#0x21    @ 0801d466 2121
    strh r1,[r0,#0x0]                        @ 0801d468 0180
    movs r1,#0x80    @ 0801d46a 8021
    lsls r1,r1,#0x13    @ 0801d46c c904
    movs r0,#0x40    @ 0801d46e 4020
    strh r0,[r1,#0x0]                        @ 0801d470 0880
    ldr r0, DAT_0801d4e8                     @ 0801d472 1d48
    movs r1,#0x80    @ 0801d474 8021
    lsls r1,r1,#0x8    @ 0801d476 0902
    bl zero_fill_by_halfword                 @ 0801d478 d7f0fcfc
    movs r0,#0xc0    @ 0801d47c c020
    lsls r0,r0,#0x13    @ 0801d47e c004
    movs r1,#0xa0    @ 0801d480 a021
    lsls r1,r1,#0x6    @ 0801d482 8901
    bl zero_fill_by_halfword                 @ 0801d484 d7f0f6fc
    ldr r4, DAT_0801d4ec                     @ 0801d488 184c
    ldr r0,[r4,#0x28]                        @ 0801d48a a06a
    bl reset_display_and_obj_vram            @ 0801d48c daf0f2f8
    ldr r0,[r4,#0x2c]                        @ 0801d490 e06a
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 0801d492 d6f005ff
    ldr r1, PTR_BG0CNT_0801d4f0              @ 0801d496 1649
    movs r0,#0x86    @ 0801d498 8620
    strh r0,[r1,#0x0]                        @ 0801d49a 0880
    adds r1,#0x2    @ 0801d49c 0231
    ldr r2, DAT_0801d4f4                     @ 0801d49e 154a
    adds r0,r2,#0x0    @ 0801d4a0 101c
    strh r0,[r1,#0x0]                        @ 0801d4a2 0880
    adds r1,#0x2    @ 0801d4a4 0231
    ldr r2, DAT_0801d4f8                     @ 0801d4a6 144a
    adds r0,r2,#0x0    @ 0801d4a8 101c
    strh r0,[r1,#0x0]                        @ 0801d4aa 0880
    adds r1,#0x2    @ 0801d4ac 0231
    ldr r2, DAT_0801d4fc                     @ 0801d4ae 134a
    adds r0,r2,#0x0    @ 0801d4b0 101c
    strh r0,[r1,#0x0]                        @ 0801d4b2 0880
    bl reset_all_bg_scroll_regs_and_shadows  @ 0801d4b4 d8f0e8fa
    movs r0,#0xa0    @ 0801d4b8 a020
    lsls r0,r0,#0x13    @ 0801d4ba c004
    ldr r4, DAT_0801d500                     @ 0801d4bc 104c
    adds r1,r4,#0x0    @ 0801d4be 211c
    movs r2,#0x20    @ 0801d4c0 2022
    bl copy_bytes_by_halfword                @ 0801d4c2 d7f0effc
    ldr r0, DAT_0801d504                     @ 0801d4c6 0f48
    adds r1,r4,#0x0    @ 0801d4c8 211c
    movs r2,#0x20    @ 0801d4ca 2022
    bl copy_bytes_by_halfword                @ 0801d4cc d7f0eafc
    ldr r0, DAT_0801d508                     @ 0801d4d0 0d48
    ldr r1, PTR_card_mini_frame_pal_main_0801d50c @ 0801d4d2 0e49
    movs r2,#0x80    @ 0801d4d4 8022
    lsls r2,r2,#0x1    @ 0801d4d6 5200
    bl copy_bytes_by_halfword                @ 0801d4d8 d7f0e4fc
    pop {r4}                                 @ 0801d4dc 10bc
    pop {r0}                                 @ 0801d4de 01bc
    bx r0                                    @ 0801d4e0 0047
    .zero  0x2
PTR_gPrng_0801d4e4:
    .word  gPrng                          @ 0801d4e4 40000003
DAT_0801d4e8:
    .word  0x06004000                     @ 0801d4e8 00400006
DAT_0801d4ec:
    .word  0x0201afb0                     @ 0801d4ec b0af0102
PTR_BG0CNT_0801d4f0:
    .word  BG0CNT                         @ 0801d4f0 08000004
DAT_0801d4f4:
    .word  0x00004104                     @ 0801d4f4 04410000
DAT_0801d4f8:
    .word  0x00000407                     @ 0801d4f8 07040000
DAT_0801d4fc:
    .word  0x00000305                     @ 0801d4fc 05030000
DAT_0801d500:
    .word  0x09ccd290                     @ 0801d500 90d2cc09
DAT_0801d504:
    .word  0x050003e0                     @ 0801d504 e0030005
DAT_0801d508:
    .word  0x05000200                     @ 0801d508 00020005
PTR_card_mini_frame_pal_main_0801d50c:
    .word  card_mini_frame_pal_main       @ 0801d50c 1416e309

@ 接收卡片索引 (r0), 从 card_stats_table 读取卡种字段判断是否为特殊宽度 (0x16/0x17), 再从 IWRAM 状态字 [0x02006c2c] 读取语言/charset 标志调用 select_charset_then_load_name 加载卡名字符串, 然后按双字节 JP 编码逐字素调用 render_glyph_jp_dual_layer 将卡名渲染进行缓冲区. 限宽逻辑 (cmp #0x5c) 防止卡名溢出单行. 被 FUN_0801d6b4 (card_image_decode_wrapper 下一级) 调用, 构成绘制卡片详情页卡名行的核心路径.
render_card_name_to_line_buf:
    push {r4,r5,r6,r7,lr}                    @ 0801d510 f0b5
    .hword 0x4657    @ 0801d512 5746
    .hword 0x464e    @ 0801d514 4e46
    .hword 0x4645    @ 0801d516 4546
    push {r5,r6,r7}                          @ 0801d518 e0b4
    sub sp,#0x8                              @ 0801d51a 82b0
    lsls r0,r0,#0x10    @ 0801d51c 0004
    lsrs r4,r0,#0x10    @ 0801d51e 040c
    movs r0,#0xd    @ 0801d520 0d20
    .hword 0x4682    @ 0801d522 8246
    movs r1,#0x1    @ 0801d524 0121
    .hword 0x4689    @ 0801d526 8946
    movs r6,#0x8    @ 0801d528 0826
    str r6,[sp,#0x0]                         @ 0801d52a 0096
    ldr r1, PTR_card_stats_table_0801d5a4    @ 0801d52c 1d49
    movs r0,#0xb    @ 0801d52e 0b20
    muls r0,r4    @ 0801d530 6043
    adds r0,#0x6    @ 0801d532 0630
    lsls r0,r0,#0x1    @ 0801d534 4000
    adds r0,r0,r1    @ 0801d536 4018
    ldrh r0,[r0,#0x0]                        @ 0801d538 0088
    cmp r0,#0x17                             @ 0801d53a 1728
    bgt LAB_0801d546                         @ 0801d53c 03dc
    cmp r0,#0x16                             @ 0801d53e 1628
    blt LAB_0801d546                         @ 0801d540 01db
    movs r0,#0x7    @ 0801d542 0720
    str r0,[sp,#0x0]                         @ 0801d544 0090
LAB_0801d546:
    ldr r5, DAT_0801d5a8                     @ 0801d546 184d
    ldr r0, DAT_0801d5ac                     @ 0801d548 1848
    ldr r1, DAT_0801d5b0                     @ 0801d54a 1949
    adds r0,r0,r1    @ 0801d54c 4018
    ldrb r3,[r0,#0x0]                        @ 0801d54e 0378
    movs r2,#0x7    @ 0801d550 0722
    ands r2,r3    @ 0801d552 1a40
    rsbs r1,r2,#0    @ 0801d554 5142
    lsrs r1,r1,#0x1f    @ 0801d556 c90f
    movs r0,#0x2    @ 0801d558 0220
    rsbs r0,r0,#0    @ 0801d55a 4042
    ldrb r6,[r5,#0x8]                        @ 0801d55c 2e7a
    ands r0,r6    @ 0801d55e 3040
    orrs r0,r1    @ 0801d560 0843
    movs r1,#0x2    @ 0801d562 0221
    orrs r0,r1    @ 0801d564 0843
    strb r0,[r5,#0x8]                        @ 0801d566 2872
    ldr r1, PTR_font_jp_base_table_0801d5b4  @ 0801d568 1249
    .hword 0x4688    @ 0801d56a 8846
    lsls r1,r0,#0x1e    @ 0801d56c 8107
    lsrs r1,r1,#0x1f    @ 0801d56e c90f
    lsls r1,r1,#0x2    @ 0801d570 8900
    lsls r0,r0,#0x1f    @ 0801d572 c007
    lsrs r0,r0,#0x1f    @ 0801d574 c00f
    lsls r0,r0,#0x3    @ 0801d576 c000
    adds r1,r1,r0    @ 0801d578 0918
    add r1,r8                                @ 0801d57a 4144
    ldr r0,[r1,#0x0]                         @ 0801d57c 0868
    str r0,[r5,#0x4]                         @ 0801d57e 6860
    adds r1,r3,#0x0    @ 0801d580 191c
    cmp r2,#0x0                              @ 0801d582 002a
    bne LAB_0801d60c                         @ 0801d584 42d1
    ldr r0, DAT_0801d5b8                     @ 0801d586 0c48
    ldrb r2,[r0,#0x0]                        @ 0801d588 0278
    movs r0,#0x4    @ 0801d58a 0420
    ands r0,r2    @ 0801d58c 1040
    cmp r0,#0x0                              @ 0801d58e 0028
    bne LAB_0801d5bc                         @ 0801d590 14d1
    movs r0,#0x1    @ 0801d592 0120
    ands r0,r2    @ 0801d594 1040
    cmp r0,#0x0                              @ 0801d596 0028
    beq LAB_0801d5bc                         @ 0801d598 10d0
    adds r0,r4,#0x0    @ 0801d59a 201c
    bl resolve_card_gfx_pointer_by_type      @ 0801d59c d1f0f4f9
    b LAB_0801d5c6                           @ 0801d5a0 11e0
    .zero  0x2
PTR_card_stats_table_0801d5a4:
    .word  card_stats_table               @ 0801d5a4 b8698109
DAT_0801d5a8:
    .word  0x02006ed0                     @ 0801d5a8 d06e0002
DAT_0801d5ac:
    .word  0x02000000                     @ 0801d5ac 00000002
DAT_0801d5b0:
    .word  0x00006c2c                     @ 0801d5b0 2c6c0000
PTR_font_jp_base_table_0801d5b4:
    .word  font_jp_base_table             @ 0801d5b4 54f8e509
DAT_0801d5b8:
    .word  0x0201afb0                     @ 0801d5b8 b0af0102
LAB_0801d5bc:
    lsls r1,r1,#0x1d    @ 0801d5bc 4907
    lsrs r1,r1,#0x1d    @ 0801d5be 490f
    adds r0,r4,#0x0    @ 0801d5c0 201c
    bl select_charset_then_load_name         @ 0801d5c2 d1f0f3f8
LAB_0801d5c6:
    adds r6,r0,#0x0    @ 0801d5c6 061c
    movs r7,#0x1    @ 0801d5c8 0127
    ldrb r0,[r6,#0x0]                        @ 0801d5ca 3078
    cmp r0,#0x0                              @ 0801d5cc 0028
    beq LAB_0801d6a4                         @ 0801d5ce 69d0
    ldr r4,[sp,#0x0]                         @ 0801d5d0 009c
    lsls r4,r4,#0x10    @ 0801d5d2 2404
    .hword 0x46a0    @ 0801d5d4 a046
LAB_0801d5d6:
    ldrb r0,[r6,#0x0]                        @ 0801d5d6 3078
    lsls r4,r0,#0x8    @ 0801d5d8 0402
    ldrb r1,[r6,#0x1]                        @ 0801d5da 7178
    orrs r4,r1    @ 0801d5dc 0c43
    adds r0,r4,#0x0    @ 0801d5de 201c
    bl char_width_wide_10_or_12              @ 0801d5e0 d2f016fe
    .hword 0x4651    @ 0801d5e4 5146
    adds r5,r1,r0    @ 0801d5e6 0d18
    cmp r5,#0x5c                             @ 0801d5e8 5c2d
    bgt LAB_0801d5fc                         @ 0801d5ea 07dc
    adds r0,r4,#0x0    @ 0801d5ec 201c
    .hword 0x464a    @ 0801d5ee 4a46
    .hword 0x4644    @ 0801d5f0 4446
    lsrs r3,r4,#0x10    @ 0801d5f2 230c
    bl render_glyph_jp_dual_layer            @ 0801d5f4 d4f046f9
    .hword 0x46aa    @ 0801d5f8 aa46
    b LAB_0801d5fe                           @ 0801d5fa 00e0
LAB_0801d5fc:
    movs r7,#0x0    @ 0801d5fc 0027
LAB_0801d5fe:
    adds r6,#0x2    @ 0801d5fe 0236
    ldrb r0,[r6,#0x0]                        @ 0801d600 3078
    cmp r0,#0x0                              @ 0801d602 0028
    beq LAB_0801d6a4                         @ 0801d604 4ed0
    cmp r7,#0x0                              @ 0801d606 002f
    bne LAB_0801d5d6                         @ 0801d608 e5d1
    b LAB_0801d6a4                           @ 0801d60a 4be0
LAB_0801d60c:
    lsls r1,r3,#0x1d    @ 0801d60c 5907
    lsrs r1,r1,#0x1d    @ 0801d60e 490f
    adds r0,r4,#0x0    @ 0801d610 201c
    bl select_charset_then_load_name         @ 0801d612 d1f0cbf8
    adds r6,r0,#0x0    @ 0801d616 061c
    movs r0,#0x1    @ 0801d618 0120
    str r0,[sp,#0x4]                         @ 0801d61a 0190
    ldrb r0,[r6,#0x0]                        @ 0801d61c 3078
    cmp r0,#0x0                              @ 0801d61e 0028
    beq LAB_0801d6a4                         @ 0801d620 40d0
    adds r7,r5,#0x0    @ 0801d622 2f1c
LAB_0801d624:
    ldrb r5,[r6,#0x0]                        @ 0801d624 3578
    ldr r0, DAT_0801d650                     @ 0801d626 0a48
    adds r0,r5,r0    @ 0801d628 2818
    ldrb r1,[r0,#0x0]                        @ 0801d62a 0178
    cmp r1,r5                                @ 0801d62c a942
    beq LAB_0801d654                         @ 0801d62e 11d0
    ldrb r5,[r0,#0x0]                        @ 0801d630 0578
    movs r4,#0x3    @ 0801d632 0324
    rsbs r4,r4,#0    @ 0801d634 6442
    adds r0,r4,#0x0    @ 0801d636 201c
    ldrb r1,[r7,#0x8]                        @ 0801d638 397a
    ands r0,r1    @ 0801d63a 0840
    strb r0,[r7,#0x8]                        @ 0801d63c 3872
    lsls r0,r0,#0x1f    @ 0801d63e c007
    lsrs r0,r0,#0x1f    @ 0801d640 c00f
    lsls r0,r0,#0x3    @ 0801d642 c000
    add r0,r8                                @ 0801d644 4044
    ldr r0,[r0,#0x0]                         @ 0801d646 0068
    str r0,[r7,#0x4]                         @ 0801d648 7860
    movs r4,#0x2    @ 0801d64a 0224
    b LAB_0801d672                           @ 0801d64c 11e0
    .zero  0x2
DAT_0801d650:
    .word  0x09e589c4                     @ 0801d650 c489e509
LAB_0801d654:
    movs r0,#0x2    @ 0801d654 0220
    ldrb r1,[r7,#0x8]                        @ 0801d656 397a
    orrs r0,r1    @ 0801d658 0843
    strb r0,[r7,#0x8]                        @ 0801d65a 3872
    lsls r1,r0,#0x1e    @ 0801d65c 8107
    lsrs r1,r1,#0x1f    @ 0801d65e c90f
    lsls r1,r1,#0x2    @ 0801d660 8900
    lsls r0,r0,#0x1f    @ 0801d662 c007
    lsrs r0,r0,#0x1f    @ 0801d664 c00f
    lsls r0,r0,#0x3    @ 0801d666 c000
    adds r1,r1,r0    @ 0801d668 0918
    add r1,r8                                @ 0801d66a 4144
    ldr r0,[r1,#0x0]                         @ 0801d66c 0868
    str r0,[r7,#0x4]                         @ 0801d66e 7860
    movs r4,#0x1    @ 0801d670 0124
LAB_0801d672:
    .hword 0x46a1    @ 0801d672 a146
    bl char_width_narrow_5                   @ 0801d674 d2f0c4fd
    .hword 0x4651    @ 0801d678 5146
    adds r4,r1,r0    @ 0801d67a 0c18
    cmp r4,#0x5c                             @ 0801d67c 5c2c
    bgt LAB_0801d692                         @ 0801d67e 08dc
    ldr r0,[sp,#0x0]                         @ 0801d680 0098
    lsls r3,r0,#0x10    @ 0801d682 0304
    adds r0,r5,#0x0    @ 0801d684 281c
    .hword 0x464a    @ 0801d686 4a46
    lsrs r3,r3,#0x10    @ 0801d688 1b0c
    bl render_glyph_jp_single_layer          @ 0801d68a d4f08bf9
    .hword 0x46a2    @ 0801d68e a246
    b LAB_0801d696                           @ 0801d690 01e0
LAB_0801d692:
    movs r1,#0x0    @ 0801d692 0021
    str r1,[sp,#0x4]                         @ 0801d694 0191
LAB_0801d696:
    adds r6,#0x1    @ 0801d696 0136
    ldrb r0,[r6,#0x0]                        @ 0801d698 3078
    cmp r0,#0x0                              @ 0801d69a 0028
    beq LAB_0801d6a4                         @ 0801d69c 02d0
    ldr r4,[sp,#0x4]                         @ 0801d69e 019c
    cmp r4,#0x0                              @ 0801d6a0 002c
    bne LAB_0801d624                         @ 0801d6a2 bfd1
LAB_0801d6a4:
    add sp,#0x8                              @ 0801d6a4 02b0
    pop {r3,r4,r5}                           @ 0801d6a6 38bc
    .hword 0x4698    @ 0801d6a8 9846
    .hword 0x46a1    @ 0801d6aa a146
    .hword 0x46aa    @ 0801d6ac aa46
    pop {r4,r5,r6,r7}                        @ 0801d6ae f0bc
    pop {r0}                                 @ 0801d6b0 01bc
    bx r0                                    @ 0801d6b2 0047

@ 作为 card_image_decode_wrapper 的直接子调用, 负责将卡名文本行渲染并提交到 OBJ VRAM. 步骤固定三段: (1) 调用 setup_line_buf_pos_and_font (FUN_080f0bb4) 以 x=0xe/y=2 初始化 行缓冲区位置和字体指针, 目标 tile 基址 0x06001c00<<2=0x06007000; (2) 调用 render_card_name_to_line_buf (FUN_0801d510) 以卡片索引渲染卡名到行缓冲区; (3) 调用 commit_line_buffer_to_sprite_vram 将行缓冲区内容刷新到 VRAM 地址 0x06008500. indeg=1 (唯一来自 card_image_decode_wrapper), 确认是卡名行的专属绘制函数.
draw_card_name_label_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 0801d6b4 f0b5
    adds r4,r0,#0x0    @ 0801d6b6 041c
    lsls r4,r4,#0x10    @ 0801d6b8 2404
    lsrs r4,r4,#0x10    @ 0801d6ba 240c
    ldr r6, DAT_0801d704                     @ 0801d6bc 114e
    movs r7,#0x84    @ 0801d6be 8427
    lsls r7,r7,#0x2    @ 0801d6c0 bf00
    movs r0,#0xe    @ 0801d6c2 0e20
    movs r1,#0x2    @ 0801d6c4 0221
    bl setup_line_buf_pos_and_font           @ 0801d6c6 d3f075fa
    adds r0,r4,#0x0    @ 0801d6ca 201c
    bl render_card_name_to_line_buf          @ 0801d6cc fff720ff
    ldr r0, DAT_0801d708                     @ 0801d6d0 0d48
    movs r1,#0x0    @ 0801d6d2 0021
    bl commit_line_buffer_to_sprite_vram     @ 0801d6d4 d5f0bafb
    movs r0,#0x0    @ 0801d6d8 0020
LAB_0801d6da:
    adds r5,r6,#0x0    @ 0801d6da 351c
    adds r5,#0x40    @ 0801d6dc 4035
    adds r4,r0,#0x1    @ 0801d6de 441c
    adds r2,r6,#0x0    @ 0801d6e0 321c
    movs r3,#0xd    @ 0801d6e2 0d23
LAB_0801d6e4:
    adds r1,r7,#0x0    @ 0801d6e4 391c
    adds r0,r1,#0x1    @ 0801d6e6 481c
    lsls r0,r0,#0x10    @ 0801d6e8 0004
    lsrs r7,r0,#0x10    @ 0801d6ea 070c
    strh r1,[r2,#0x0]                        @ 0801d6ec 1180
    adds r2,#0x2    @ 0801d6ee 0232
    subs r3,#0x1    @ 0801d6f0 013b
    cmp r3,#0x0                              @ 0801d6f2 002b
    bge LAB_0801d6e4                         @ 0801d6f4 f6da
    adds r6,r5,#0x0    @ 0801d6f6 2e1c
    adds r0,r4,#0x0    @ 0801d6f8 201c
    cmp r0,#0x1                              @ 0801d6fa 0128
    ble LAB_0801d6da                         @ 0801d6fc eddd
    pop {r4,r5,r6,r7}                        @ 0801d6fe f0bc
    pop {r0}                                 @ 0801d700 01bc
    bx r0                                    @ 0801d702 0047
DAT_0801d704:
    .word  0x06001840                     @ 0801d704 40180006
DAT_0801d708:
    .word  0x06008200                     @ 0801d708 00820006

@ 接收卡片 ATK (r0) 和 DEF (r1) 值, 通过 __umodsi3/__udivsi3 逐位分解十进制数字, 对 ATK 的个/十/百/千位分别以固定列偏移 (0x36, 0x32, ...) 调用 FUN_080f1b0c 将数字字素渲染到行缓冲区中对应列; DEF 同理以另一组列偏移渲染. 行缓冲区基址从 DAT_0801d7c8 (0x0984f59c) 读取, 数字字素基址从 DAT_0801d7cc (0x0984f54c). 被 FUN_0801d7d0 (draw_atk_def_label_to_vram) 调用, 是 ATK/DEF 数值渲染的计算核心.
render_atk_def_digits_to_buf:
    push {r4,r5,r6,lr}                       @ 0801d70c 70b5
    lsls r0,r0,#0x10    @ 0801d70e 0004
    lsrs r5,r0,#0x10    @ 0801d710 050c
    lsls r1,r1,#0x10    @ 0801d712 0904
    lsrs r6,r1,#0x10    @ 0801d714 0e0c
    ldr r4, DAT_0801d7c8                     @ 0801d716 2c4c
    adds r0,r4,#0x0    @ 0801d718 201c
    movs r1,#0x1a    @ 0801d71a 1a21
    movs r2,#0x1    @ 0801d71c 0122
    movs r3,#0x8    @ 0801d71e 0823
    bl blit_glyph_columns_to_buf             @ 0801d720 d4f0f4f9
    adds r0,r4,#0x0    @ 0801d724 201c
    adds r0,#0x8    @ 0801d726 0830
    movs r1,#0x22    @ 0801d728 2221
    movs r2,#0x1    @ 0801d72a 0122
    movs r3,#0x8    @ 0801d72c 0823
    bl blit_glyph_columns_to_buf             @ 0801d72e d4f0edf9
    adds r0,r4,#0x0    @ 0801d732 201c
    adds r0,#0x10    @ 0801d734 1030
    movs r1,#0x40    @ 0801d736 4021
    movs r2,#0x1    @ 0801d738 0122
    movs r3,#0x8    @ 0801d73a 0823
    bl blit_glyph_columns_to_buf             @ 0801d73c d4f0e6f9
    adds r4,#0x18    @ 0801d740 1834
    adds r0,r4,#0x0    @ 0801d742 201c
    movs r1,#0x48    @ 0801d744 4821
    movs r2,#0x1    @ 0801d746 0122
    movs r3,#0x8    @ 0801d748 0823
    bl blit_glyph_columns_to_buf             @ 0801d74a d4f0dff9
    movs r4,#0x0    @ 0801d74e 0024
LAB_0801d750:
    cmp r4,#0x0                              @ 0801d750 002c
    beq LAB_0801d758                         @ 0801d752 01d0
    cmp r5,#0x0                              @ 0801d754 002d
    beq LAB_0801d776                         @ 0801d756 0ed0
LAB_0801d758:
    adds r0,r5,#0x0    @ 0801d758 281c
    movs r1,#0xa    @ 0801d75a 0a21
    bl __umodsi3                             @ 0801d75c f1f07af8
    lsls r0,r0,#0x10    @ 0801d760 0004
    lsrs r0,r0,#0xd    @ 0801d762 400b
    ldr r1, DAT_0801d7cc                     @ 0801d764 1949
    adds r0,r0,r1    @ 0801d766 4018
    lsls r2,r4,#0x2    @ 0801d768 a200
    movs r1,#0x36    @ 0801d76a 3621
    subs r1,r1,r2    @ 0801d76c 891a
    movs r2,#0x1    @ 0801d76e 0122
    movs r3,#0x8    @ 0801d770 0823
    bl blit_glyph_columns_to_buf             @ 0801d772 d4f0cbf9
LAB_0801d776:
    adds r0,r5,#0x0    @ 0801d776 281c
    movs r1,#0xa    @ 0801d778 0a21
    bl __udivsi3                             @ 0801d77a f1f02ff8
    lsls r0,r0,#0x10    @ 0801d77e 0004
    lsrs r5,r0,#0x10    @ 0801d780 050c
    adds r4,#0x1    @ 0801d782 0134
    cmp r4,#0x3                              @ 0801d784 032c
    ble LAB_0801d750                         @ 0801d786 e3dd
    movs r4,#0x0    @ 0801d788 0024
LAB_0801d78a:
    cmp r4,#0x0                              @ 0801d78a 002c
    beq LAB_0801d792                         @ 0801d78c 01d0
    cmp r6,#0x0                              @ 0801d78e 002e
    beq LAB_0801d7b0                         @ 0801d790 0ed0
LAB_0801d792:
    adds r0,r6,#0x0    @ 0801d792 301c
    movs r1,#0xa    @ 0801d794 0a21
    bl __umodsi3                             @ 0801d796 f1f05df8
    lsls r0,r0,#0x10    @ 0801d79a 0004
    lsrs r0,r0,#0xd    @ 0801d79c 400b
    ldr r1, DAT_0801d7cc                     @ 0801d79e 0b49
    adds r0,r0,r1    @ 0801d7a0 4018
    lsls r2,r4,#0x2    @ 0801d7a2 a200
    movs r1,#0x5c    @ 0801d7a4 5c21
    subs r1,r1,r2    @ 0801d7a6 891a
    movs r2,#0x1    @ 0801d7a8 0122
    movs r3,#0x8    @ 0801d7aa 0823
    bl blit_glyph_columns_to_buf             @ 0801d7ac d4f0aef9
LAB_0801d7b0:
    adds r0,r6,#0x0    @ 0801d7b0 301c
    movs r1,#0xa    @ 0801d7b2 0a21
    bl __udivsi3                             @ 0801d7b4 f1f012f8
    lsls r0,r0,#0x10    @ 0801d7b8 0004
    lsrs r6,r0,#0x10    @ 0801d7ba 060c
    adds r4,#0x1    @ 0801d7bc 0134
    cmp r4,#0x3                              @ 0801d7be 032c
    ble LAB_0801d78a                         @ 0801d7c0 e3dd
    pop {r4,r5,r6}                           @ 0801d7c2 70bc
    pop {r0}                                 @ 0801d7c4 01bc
    bx r0                                    @ 0801d7c6 0047
DAT_0801d7c8:
    .word  0x0984f59c                     @ 0801d7c8 9cf58409
DAT_0801d7cc:
    .word  0x0984f54c                     @ 0801d7cc 4cf58409

@ card_image_decode_wrapper 的第二个直接子调用, 负责将卡片 ATK/DEF 数值渲染并提交到 OBJ VRAM. 步骤三段: (1) 调用 setup_line_buf_pos_and_font 以 x=0xe/y=2 + tile 基址 0x06001c00 初始化行缓冲区; (2) 调用 render_atk_def_digits_to_buf (FUN_0801d70c) 将 ATK (r0) 和 DEF (r1) 数字字素渲染到缓冲区; (3) 调用 commit_line_buffer_to_sprite_vram 以目标地址 0x06008580 刷新到 VRAM. 与 draw_card_name_label_to_vram (FUN_0801d6b4) 结构完全对称, 两者均被 card_image_decode_wrapper 以 indeg=1 调用.
draw_atk_def_label_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 0801d7d0 f0b5
    adds r4,r0,#0x0    @ 0801d7d2 041c
    adds r5,r1,#0x0    @ 0801d7d4 0d1c
    lsls r4,r4,#0x10    @ 0801d7d6 2404
    lsrs r4,r4,#0x10    @ 0801d7d8 240c
    lsls r5,r5,#0x10    @ 0801d7da 2d04
    lsrs r5,r5,#0x10    @ 0801d7dc 2d0c
    ldr r6, DAT_0801d828                     @ 0801d7de 124e
    movs r7,#0x8b    @ 0801d7e0 8b27
    lsls r7,r7,#0x2    @ 0801d7e2 bf00
    movs r0,#0xe    @ 0801d7e4 0e20
    movs r1,#0x2    @ 0801d7e6 0221
    bl setup_line_buf_pos_and_font           @ 0801d7e8 d3f0e4f9
    adds r0,r4,#0x0    @ 0801d7ec 201c
    adds r1,r5,#0x0    @ 0801d7ee 291c
    bl render_atk_def_digits_to_buf          @ 0801d7f0 fff78cff
    ldr r0, DAT_0801d82c                     @ 0801d7f4 0d48
    movs r1,#0x0    @ 0801d7f6 0021
    bl commit_line_buffer_to_sprite_vram     @ 0801d7f8 d5f028fb
    movs r0,#0x0    @ 0801d7fc 0020
LAB_0801d7fe:
    adds r5,r6,#0x0    @ 0801d7fe 351c
    adds r5,#0x40    @ 0801d800 4035
    adds r4,r0,#0x1    @ 0801d802 441c
    adds r2,r6,#0x0    @ 0801d804 321c
    movs r3,#0xd    @ 0801d806 0d23
LAB_0801d808:
    adds r1,r7,#0x0    @ 0801d808 391c
    adds r0,r1,#0x1    @ 0801d80a 481c
    lsls r0,r0,#0x10    @ 0801d80c 0004
    lsrs r7,r0,#0x10    @ 0801d80e 070c
    strh r1,[r2,#0x0]                        @ 0801d810 1180
    adds r2,#0x2    @ 0801d812 0232
    subs r3,#0x1    @ 0801d814 013b
    cmp r3,#0x0                              @ 0801d816 002b
    bge LAB_0801d808                         @ 0801d818 f6da
    adds r6,r5,#0x0    @ 0801d81a 2e1c
    adds r0,r4,#0x0    @ 0801d81c 201c
    cmp r0,#0x1                              @ 0801d81e 0128
    ble LAB_0801d7fe                         @ 0801d820 eddd
    pop {r4,r5,r6,r7}                        @ 0801d822 f0bc
    pop {r0}                                 @ 0801d824 01bc
    bx r0                                    @ 0801d826 0047
DAT_0801d828:
    .word  0x06001c00                     @ 0801d828 001c0006
DAT_0801d82c:
    .word  0x06008580                     @ 0801d82c 80850006

@ 接收 level 字符串表索引 (r0, 来自 lookup_level_glyph_index 返回值), 从 ROM 字符串表 (0x09e5f726 = level/type 文字表) 定位对应文本, 先以固定 4 次调用 blit_glyph_columns_to_buf (FUN_080f1b0c, r1=0x1a/0x22/0x40/0x48) 将 "LEVEL"/"RANK" 等标签字素写入缓冲区, 再调用 count_bytes_until_null 取文本长度, 然后逐字节解码数字 (0x30-0x39 -> %10 取余, 特殊码 0x3f/'?'->0xe, 0x58/'X'->0xf) 并以 FUN_080f1b0c 渲染各数字字素到对应列. 被 FUN_0801d92c (draw_card_level_label_to_vram) 调用, 是 Level/Rank 数值行的渲染核心.
render_card_level_text_to_buf:
    push {r4,r5,r6,r7,lr}                    @ 0801d830 f0b5
    adds r7,r0,#0x0    @ 0801d832 071c
    ldr r4, DAT_0801d89c                     @ 0801d834 194c
    adds r0,r4,#0x0    @ 0801d836 201c
    movs r1,#0x1a    @ 0801d838 1a21
    movs r2,#0x1    @ 0801d83a 0122
    movs r3,#0x8    @ 0801d83c 0823
    bl blit_glyph_columns_to_buf             @ 0801d83e d4f065f9
    adds r0,r4,#0x0    @ 0801d842 201c
    adds r0,#0x8    @ 0801d844 0830
    movs r1,#0x22    @ 0801d846 2221
    movs r2,#0x1    @ 0801d848 0122
    movs r3,#0x8    @ 0801d84a 0823
    bl blit_glyph_columns_to_buf             @ 0801d84c d4f05ef9
    adds r0,r4,#0x0    @ 0801d850 201c
    adds r0,#0x10    @ 0801d852 1030
    movs r1,#0x40    @ 0801d854 4021
    movs r2,#0x1    @ 0801d856 0122
    movs r3,#0x8    @ 0801d858 0823
    bl blit_glyph_columns_to_buf             @ 0801d85a d4f057f9
    adds r4,#0x18    @ 0801d85e 1834
    adds r0,r4,#0x0    @ 0801d860 201c
    movs r1,#0x48    @ 0801d862 4821
    movs r2,#0x1    @ 0801d864 0122
    movs r3,#0x8    @ 0801d866 0823
    bl blit_glyph_columns_to_buf             @ 0801d868 d4f050f9
    lsls r4,r7,#0x2    @ 0801d86c bc00
    adds r4,r4,r7    @ 0801d86e e419
    lsls r4,r4,#0x2    @ 0801d870 a400
    ldr r0, DAT_0801d8a0                     @ 0801d872 0b48
    adds r4,r4,r0    @ 0801d874 2418
    adds r0,r4,#0x0    @ 0801d876 201c
    bl count_bytes_until_null                @ 0801d878 d7f032fe
    adds r6,r0,#0x0    @ 0801d87c 061c
    subs r0,r6,#0x1    @ 0801d87e 701e
    adds r4,r4,r0    @ 0801d880 2418
    movs r5,#0x0    @ 0801d882 0025
    cmp r5,r6                                @ 0801d884 b542
    bge LAB_0801d8c6                         @ 0801d886 1eda
LAB_0801d888:
    ldrb r0,[r4,#0x0]                        @ 0801d888 2078
    cmp r0,#0x3f                             @ 0801d88a 3f28
    beq LAB_0801d8a4                         @ 0801d88c 0ad0
    cmp r0,#0x58                             @ 0801d88e 5828
    beq LAB_0801d8a8                         @ 0801d890 0ad0
    subs r0,#0x30    @ 0801d892 3038
    movs r1,#0xa    @ 0801d894 0a21
    bl __modsi3                              @ 0801d896 f0f001ff
    b LAB_0801d8aa                           @ 0801d89a 06e0
DAT_0801d89c:
    .word  0x0984f59c                     @ 0801d89c 9cf58409
DAT_0801d8a0:
    .word  0x09e5f71e                     @ 0801d8a0 1ef7e509
LAB_0801d8a4:
    movs r0,#0xe    @ 0801d8a4 0e20
    b LAB_0801d8aa                           @ 0801d8a6 00e0
LAB_0801d8a8:
    movs r0,#0xf    @ 0801d8a8 0f20
LAB_0801d8aa:
    lsls r0,r0,#0x3    @ 0801d8aa c000
    ldr r1, DAT_0801d8f8                     @ 0801d8ac 1249
    adds r0,r0,r1    @ 0801d8ae 4018
    lsls r2,r5,#0x2    @ 0801d8b0 aa00
    movs r1,#0x36    @ 0801d8b2 3621
    subs r1,r1,r2    @ 0801d8b4 891a
    movs r2,#0x1    @ 0801d8b6 0122
    movs r3,#0x8    @ 0801d8b8 0823
    bl blit_glyph_columns_to_buf             @ 0801d8ba d4f027f9
    subs r4,#0x1    @ 0801d8be 013c
    adds r5,#0x1    @ 0801d8c0 0135
    cmp r5,r6                                @ 0801d8c2 b542
    blt LAB_0801d888                         @ 0801d8c4 e0db
LAB_0801d8c6:
    lsls r4,r7,#0x2    @ 0801d8c6 bc00
    adds r4,r4,r7    @ 0801d8c8 e419
    lsls r4,r4,#0x2    @ 0801d8ca a400
    ldr r0, DAT_0801d8fc                     @ 0801d8cc 0b48
    adds r4,r4,r0    @ 0801d8ce 2418
    adds r0,r4,#0x0    @ 0801d8d0 201c
    bl count_bytes_until_null                @ 0801d8d2 d7f005fe
    adds r6,r0,#0x0    @ 0801d8d6 061c
    subs r0,r6,#0x1    @ 0801d8d8 701e
    adds r4,r4,r0    @ 0801d8da 2418
    adds r4,r4,r0    @ 0801d8dc 2418
    movs r5,#0x0    @ 0801d8de 0025
    cmp r5,r6                                @ 0801d8e0 b542
    bge LAB_0801d922                         @ 0801d8e2 1eda
LAB_0801d8e4:
    ldrb r0,[r4,#0x0]                        @ 0801d8e4 2078
    cmp r0,#0x3f                             @ 0801d8e6 3f28
    beq LAB_0801d900                         @ 0801d8e8 0ad0
    cmp r0,#0x58                             @ 0801d8ea 5828
    beq LAB_0801d904                         @ 0801d8ec 0ad0
    subs r0,#0x30    @ 0801d8ee 3038
    movs r1,#0xa    @ 0801d8f0 0a21
    bl __modsi3                              @ 0801d8f2 f0f0d3fe
    b LAB_0801d906                           @ 0801d8f6 06e0
DAT_0801d8f8:
    .word  0x0984f54c                     @ 0801d8f8 4cf58409
DAT_0801d8fc:
    .word  0x09e5f726                     @ 0801d8fc 26f7e509
LAB_0801d900:
    movs r0,#0xe    @ 0801d900 0e20
    b LAB_0801d906                           @ 0801d902 00e0
LAB_0801d904:
    movs r0,#0xf    @ 0801d904 0f20
LAB_0801d906:
    lsls r0,r0,#0x3    @ 0801d906 c000
    ldr r1, DAT_0801d928                     @ 0801d908 0749
    adds r0,r0,r1    @ 0801d90a 4018
    lsls r2,r5,#0x2    @ 0801d90c aa00
    movs r1,#0x5c    @ 0801d90e 5c21
    subs r1,r1,r2    @ 0801d910 891a
    movs r2,#0x1    @ 0801d912 0122
    movs r3,#0x8    @ 0801d914 0823
    bl blit_glyph_columns_to_buf             @ 0801d916 d4f0f9f8
    subs r4,#0x1    @ 0801d91a 013c
    adds r5,#0x1    @ 0801d91c 0135
    cmp r5,r6                                @ 0801d91e b542
    blt LAB_0801d8e4                         @ 0801d920 e0db
LAB_0801d922:
    pop {r4,r5,r6,r7}                        @ 0801d922 f0bc
    pop {r0}                                 @ 0801d924 01bc
    bx r0                                    @ 0801d926 0047
DAT_0801d928:
    .word  0x0984f54c                     @ 0801d928 4cf58409

@ card_image_decode_wrapper 的第三个直接子调用, 负责将卡片等级 (Level/Rank) 星图渲染并提交到 OBJ VRAM. 先调用 lookup_level_glyph_index (FUN_080ef454) 以卡片索引查 level_signature_table 取等级索引; 若返回 -1 (无等级数据, 如魔法/陷阱) 则直接返回 0. 否则调用 setup_line_buf_pos_and_font (FUN_080f0bb4) 以 x=0xe/y=2 初始化行缓冲区, 再调用 render_card_level_text_to_buf (FUN_0801d830) 渲染等级文字/星图到缓冲区, 最后 commit_line_buffer_to_sprite_vram 写入 VRAM (目标地址 DAT_0801d994). indeg=1, 唯一 caller card_image_decode_wrapper.
draw_card_level_label_to_vram:
    push {r4,r5,r6,r7,lr}                    @ 0801d92c f0b5
    lsls r0,r0,#0x10    @ 0801d92e 0004
    lsrs r0,r0,#0x10    @ 0801d930 000c
    ldr r6, DAT_0801d94c                     @ 0801d932 064e
    movs r7,#0x8b    @ 0801d934 8b27
    lsls r7,r7,#0x2    @ 0801d936 bf00
    bl lookup_level_glyph_index              @ 0801d938 d1f08cfd
    adds r4,r0,#0x0    @ 0801d93c 041c
    movs r0,#0x1    @ 0801d93e 0120
    rsbs r0,r0,#0    @ 0801d940 4042
    cmp r4,r0                                @ 0801d942 8442
    bne LAB_0801d950                         @ 0801d944 04d1
    movs r0,#0x0    @ 0801d946 0020
    b LAB_0801d98e                           @ 0801d948 21e0
    .zero  0x2
DAT_0801d94c:
    .word  0x06001c00                     @ 0801d94c 001c0006
LAB_0801d950:
    movs r0,#0xe    @ 0801d950 0e20
    movs r1,#0x2    @ 0801d952 0221
    bl setup_line_buf_pos_and_font           @ 0801d954 d3f02ef9
    adds r0,r4,#0x0    @ 0801d958 201c
    bl render_card_level_text_to_buf         @ 0801d95a fff769ff
    ldr r0, DAT_0801d994                     @ 0801d95e 0d48
    movs r1,#0x0    @ 0801d960 0021
    bl commit_line_buffer_to_sprite_vram     @ 0801d962 d5f073fa
    movs r0,#0x0    @ 0801d966 0020
LAB_0801d968:
    adds r5,r6,#0x0    @ 0801d968 351c
    adds r5,#0x40    @ 0801d96a 4035
    adds r4,r0,#0x1    @ 0801d96c 441c
    adds r2,r6,#0x0    @ 0801d96e 321c
    movs r3,#0xd    @ 0801d970 0d23
LAB_0801d972:
    adds r1,r7,#0x0    @ 0801d972 391c
    adds r0,r1,#0x1    @ 0801d974 481c
    lsls r0,r0,#0x10    @ 0801d976 0004
    lsrs r7,r0,#0x10    @ 0801d978 070c
    strh r1,[r2,#0x0]                        @ 0801d97a 1180
    adds r2,#0x2    @ 0801d97c 0232
    subs r3,#0x1    @ 0801d97e 013b
    cmp r3,#0x0                              @ 0801d980 002b
    bge LAB_0801d972                         @ 0801d982 f6da
    adds r6,r5,#0x0    @ 0801d984 2e1c
    adds r0,r4,#0x0    @ 0801d986 201c
    cmp r0,#0x1                              @ 0801d988 0128
    ble LAB_0801d968                         @ 0801d98a eddd
    movs r0,#0x1    @ 0801d98c 0120
LAB_0801d98e:
    pop {r4,r5,r6,r7}                        @ 0801d98e f0bc
    pop {r1}                                 @ 0801d990 02bc
    bx r1                                    @ 0801d992 0847
DAT_0801d994:
    .word  0x06008580                     @ 0801d994 80850006

@ p1: 读卡片属性, 调 decode_card_image_6bpp (r1=0x10 palette offset)
card_image_decode_wrapper:
    push {r4,r5,r6,r7,lr}                    @ 0801d998 f0b5
    .hword 0x4657    @ 0801d99a 5746
    .hword 0x464e    @ 0801d99c 4e46
    .hword 0x4645    @ 0801d99e 4546
    push {r5,r6,r7}                          @ 0801d9a0 e0b4
    sub sp,#0xc                              @ 0801d9a2 83b0
    lsls r0,r0,#0x10    @ 0801d9a4 0004
    lsrs r5,r0,#0x10    @ 0801d9a6 050c
    lsls r1,r1,#0x10    @ 0801d9a8 0904
    lsrs r1,r1,#0x10    @ 0801d9aa 090c
    str r1,[sp,#0x4]                         @ 0801d9ac 0191
    lsls r2,r2,#0x10    @ 0801d9ae 1204
    lsrs r2,r2,#0x10    @ 0801d9b0 120c
    str r2,[sp,#0x8]                         @ 0801d9b2 0292
    ldr r2, PTR_card_stats_table_0801da8c    @ 0801d9b4 354a
    movs r0,#0xb    @ 0801d9b6 0b20
    adds r1,r5,#0x0    @ 0801d9b8 291c
    muls r1,r0    @ 0801d9ba 4143
    adds r0,r1,#0x7    @ 0801d9bc c81d
    lsls r0,r0,#0x1    @ 0801d9be 4000
    adds r0,r0,r2    @ 0801d9c0 8018
    ldrh r0,[r0,#0x0]                        @ 0801d9c2 0088
    .hword 0x4682    @ 0801d9c4 8246
    adds r0,r1,#0x6    @ 0801d9c6 881d
    lsls r0,r0,#0x1    @ 0801d9c8 4000
    adds r0,r0,r2    @ 0801d9ca 8018
    ldrh r4,[r0,#0x0]                        @ 0801d9cc 0488
    .hword 0x46a0    @ 0801d9ce a046
    adds r1,#0x9    @ 0801d9d0 0931
    lsls r1,r1,#0x1    @ 0801d9d2 4900
    adds r1,r1,r2    @ 0801d9d4 8918
    ldrh r7,[r1,#0x0]                        @ 0801d9d6 0f88
    .hword 0x46b9    @ 0801d9d8 b946
    movs r6,#0x80    @ 0801d9da 8026
    lsls r6,r6,#0x5    @ 0801d9dc 7601
    movs r2,#0x82    @ 0801d9de 8222
    lsls r2,r2,#0x2    @ 0801d9e0 9200
    ldr r3, DAT_0801da90                     @ 0801d9e2 2b4b
    adds r0,r6,#0x0    @ 0801d9e4 301c
    movs r1,#0x80    @ 0801d9e6 8021
    bl load_pack_tile_and_map_to_vram        @ 0801d9e8 d0f012fb
    movs r0,#0xc0    @ 0801d9ec c020
    lsls r0,r0,#0x4    @ 0801d9ee 0001
    ldr r2, DAT_0801da94                     @ 0801d9f0 284a
    ldr r3, DAT_0801da98                     @ 0801d9f2 294b
    movs r1,#0x80    @ 0801d9f4 8021
    bl load_pack_tile_and_map_to_vram        @ 0801d9f6 d0f00bfb
    movs r0,#0xc0    @ 0801d9fa c020
    lsls r0,r0,#0x13    @ 0801d9fc c004
    movs r1,#0x10    @ 0801d9fe 1021
    str r1,[sp,#0x0]                         @ 0801da00 0091
    movs r1,#0x82    @ 0801da02 8221
    adds r2,r5,#0x0    @ 0801da04 2a1c
    movs r3,#0x2    @ 0801da06 0223
    bl decode_card_image_6bpp                @ 0801da08 fff742fc
    cmp r4,#0x16                             @ 0801da0c 162c
    bne LAB_0801da12                         @ 0801da0e 00d1
    b LAB_0801db34                           @ 0801da10 90e0
LAB_0801da12:
    cmp r4,#0x16                             @ 0801da12 162c
    bgt LAB_0801dabc                         @ 0801da14 52dc
    cmp r4,#0x14                             @ 0801da16 142c
    ble LAB_0801da1c                         @ 0801da18 00dd
    b LAB_0801dbca                           @ 0801da1a d6e0
LAB_0801da1c:
    cmp r4,#0x1                              @ 0801da1c 012c
    bge LAB_0801da22                         @ 0801da1e 00da
    b LAB_0801dbca                           @ 0801da20 d3e0
LAB_0801da22:
    ldr r3, DAT_0801da9c                     @ 0801da22 1e4b
    adds r0,r6,#0x0    @ 0801da24 301c
    movs r1,#0x50    @ 0801da26 5021
    movs r2,#0xca    @ 0801da28 ca22
    bl load_pack_tile_and_map_to_vram        @ 0801da2a d0f0f1fa
    ldr r4, DAT_0801daa0                     @ 0801da2e 1c4c
    adds r0,r5,#0x0    @ 0801da30 281c
    bl resolve_card_type_icon_ptr            @ 0801da32 d1f04bfc
    adds r1,r0,#0x0    @ 0801da36 011c
    adds r0,r4,#0x0    @ 0801da38 201c
    movs r2,#0x20    @ 0801da3a 2022
    bl copy_bytes_by_halfword                @ 0801da3c d7f032fa
    adds r0,r5,#0x0    @ 0801da40 281c
    bl draw_card_name_label_to_vram          @ 0801da42 fff737fe
    ldr r0, DAT_0801daa4                     @ 0801da46 1748
    .hword 0x4654    @ 0801da48 5446
    subs r4,#0x1    @ 0801da4a 013c
    lsls r1,r4,#0x5    @ 0801da4c 6101
    ldr r2, DAT_0801daa8                     @ 0801da4e 164a
    adds r1,r1,r2    @ 0801da50 8918
    movs r2,#0x20    @ 0801da52 2022
    bl copy_bytes_by_halfword                @ 0801da54 d7f026fa
    ldr r0, DAT_0801daac                     @ 0801da58 1448
    lsls r4,r4,#0x7    @ 0801da5a e401
    ldr r1, DAT_0801dab0                     @ 0801da5c 1449
    adds r4,r4,r1    @ 0801da5e 6418
    adds r1,r4,#0x0    @ 0801da60 211c
    movs r2,#0x80    @ 0801da62 8022
    bl copy_bytes_by_halfword                @ 0801da64 d7f01efa
    ldr r0, DAT_0801dab4                     @ 0801da68 1248
    ldr r1, DAT_0801dab8                     @ 0801da6a 1349
    movs r2,#0x20    @ 0801da6c 2022
    bl copy_bytes_by_halfword                @ 0801da6e d7f019fa
    adds r0,r5,#0x0    @ 0801da72 281c
    bl check_card_atk_in_valid_range         @ 0801da74 d1f0a2fc
    cmp r0,#0x0                              @ 0801da78 0028
    bne LAB_0801da7e                         @ 0801da7a 00d1
    b LAB_0801dbc2                           @ 0801da7c a1e0
LAB_0801da7e:
    adds r0,r5,#0x0    @ 0801da7e 281c
    bl draw_card_level_label_to_vram         @ 0801da80 fff754ff
    cmp r0,#0x0                              @ 0801da84 0028
    beq LAB_0801da8a                         @ 0801da86 00d0
    b LAB_0801dbca                           @ 0801da88 9fe0
LAB_0801da8a:
    b LAB_0801dbb8                           @ 0801da8a 95e0
PTR_card_stats_table_0801da8c:
    .word  card_stats_table               @ 0801da8c b8698109
DAT_0801da90:
    .word  0x0985004c                     @ 0801da90 4c008509
DAT_0801da94:
    .word  0x0000020e                     @ 0801da94 0e020000
DAT_0801da98:
    .word  0x09850934                     @ 0801da98 34098509
DAT_0801da9c:
    .word  0x0984a3fc                     @ 0801da9c fca38409
DAT_0801daa0:
    .word  0x050000a0                     @ 0801daa0 a0000005
DAT_0801daa4:
    .word  0x050003a0                     @ 0801daa4 a0030005
DAT_0801daa8:
    .word  0x0984dd6c                     @ 0801daa8 6cdd8409
DAT_0801daac:
    .word  0x06017440                     @ 0801daac 40740106
DAT_0801dab0:
    .word  0x0984d8ec                     @ 0801dab0 ecd88409
DAT_0801dab4:
    .word  0x06010020                     @ 0801dab4 20000106
DAT_0801dab8:
    .word  0x09ccd2d0                     @ 0801dab8 d0d2cc09
LAB_0801dabc:
    .hword 0x4640    @ 0801dabc 4046
    cmp r0,#0x17                             @ 0801dabe 1728
    beq LAB_0801dac4                         @ 0801dac0 00d0
    b LAB_0801dbca                           @ 0801dac2 82e0
LAB_0801dac4:
    ldr r3, DAT_0801db10                     @ 0801dac4 124b
    adds r0,r6,#0x0    @ 0801dac6 301c
    movs r1,#0x50    @ 0801dac8 5021
    movs r2,#0xca    @ 0801daca ca22
    bl load_pack_tile_and_map_to_vram        @ 0801dacc d0f0a0fa
    ldr r4, DAT_0801db14                     @ 0801dad0 104c
    adds r0,r5,#0x0    @ 0801dad2 281c
    bl resolve_card_type_icon_ptr            @ 0801dad4 d1f0fafb
    adds r1,r0,#0x0    @ 0801dad8 011c
    adds r0,r4,#0x0    @ 0801dada 201c
    movs r2,#0x20    @ 0801dadc 2022
    bl copy_bytes_by_halfword                @ 0801dade d7f0e1f9
    adds r0,r5,#0x0    @ 0801dae2 281c
    bl draw_card_name_label_to_vram          @ 0801dae4 fff7e6fd
    ldr r0, DAT_0801db18                     @ 0801dae8 0b48
    ldr r1, DAT_0801db1c                     @ 0801daea 0c49
    movs r2,#0x20    @ 0801daec 2022
    bl copy_bytes_by_halfword                @ 0801daee d7f0d9f9
    ldr r0, DAT_0801db20                     @ 0801daf2 0b48
    ldr r1, DAT_0801db24                     @ 0801daf4 0b49
    movs r2,#0x80    @ 0801daf6 8022
    bl copy_bytes_by_halfword                @ 0801daf8 d7f0d4f9
    cmp r7,#0x0                              @ 0801dafc 002f
    beq LAB_0801dbca                         @ 0801dafe 64d0
    ldr r0, DAT_0801db28                     @ 0801db00 0948
    ldr r1, DAT_0801db2c                     @ 0801db02 0a49
    movs r2,#0x20    @ 0801db04 2022
    bl copy_bytes_by_halfword                @ 0801db06 d7f0cdf9
    ldr r0, DAT_0801db30                     @ 0801db0a 0948
    subs r1,r7,#0x1    @ 0801db0c 791e
    b LAB_0801db82                           @ 0801db0e 38e0
DAT_0801db10:
    .word  0x0984b994                     @ 0801db10 94b98409
DAT_0801db14:
    .word  0x050000a0                     @ 0801db14 a0000005
DAT_0801db18:
    .word  0x050003a0                     @ 0801db18 a0030005
DAT_0801db1c:
    .word  0x0984de6c                     @ 0801db1c 6cde8409
DAT_0801db20:
    .word  0x06017440                     @ 0801db20 40740106
DAT_0801db24:
    .word  0x0984dcec                     @ 0801db24 ecdc8409
DAT_0801db28:
    .word  0x050003c0                     @ 0801db28 c0030005
DAT_0801db2c:
    .word  0x0984f52c                     @ 0801db2c 2cf58409
DAT_0801db30:
    .word  0x060174c0                     @ 0801db30 c0740106
LAB_0801db34:
    ldr r3, DAT_0801db90                     @ 0801db34 164b
    adds r0,r6,#0x0    @ 0801db36 301c
    movs r1,#0x50    @ 0801db38 5021
    movs r2,#0xca    @ 0801db3a ca22
    bl load_pack_tile_and_map_to_vram        @ 0801db3c d0f068fa
    ldr r4, DAT_0801db94                     @ 0801db40 144c
    adds r0,r5,#0x0    @ 0801db42 281c
    bl resolve_card_type_icon_ptr            @ 0801db44 d1f0c2fb
    adds r1,r0,#0x0    @ 0801db48 011c
    adds r0,r4,#0x0    @ 0801db4a 201c
    movs r2,#0x20    @ 0801db4c 2022
    bl copy_bytes_by_halfword                @ 0801db4e d7f0a9f9
    adds r0,r5,#0x0    @ 0801db52 281c
    bl draw_card_name_label_to_vram          @ 0801db54 fff7aefd
    ldr r0, DAT_0801db98                     @ 0801db58 0f48
    ldr r1, DAT_0801db9c                     @ 0801db5a 1049
    movs r2,#0x20    @ 0801db5c 2022
    bl copy_bytes_by_halfword                @ 0801db5e d7f0a1f9
    ldr r0, DAT_0801dba0                     @ 0801db62 0f48
    ldr r1, DAT_0801dba4                     @ 0801db64 0f49
    movs r2,#0x80    @ 0801db66 8022
    bl copy_bytes_by_halfword                @ 0801db68 d7f09cf9
    .hword 0x4648    @ 0801db6c 4846
    cmp r0,#0x0                              @ 0801db6e 0028
    beq LAB_0801dbca                         @ 0801db70 2bd0
    ldr r0, DAT_0801dba8                     @ 0801db72 0d48
    ldr r1, DAT_0801dbac                     @ 0801db74 0d49
    movs r2,#0x20    @ 0801db76 2022
    bl copy_bytes_by_halfword                @ 0801db78 d7f094f9
    ldr r0, DAT_0801dbb0                     @ 0801db7c 0c48
    .hword 0x4649    @ 0801db7e 4946
    subs r1,#0x1    @ 0801db80 0139
LAB_0801db82:
    lsls r1,r1,#0x5    @ 0801db82 4901
    ldr r2, DAT_0801dbb4                     @ 0801db84 0b4a
    adds r1,r1,r2    @ 0801db86 8918
    movs r2,#0x20    @ 0801db88 2022
    bl copy_bytes_by_halfword                @ 0801db8a d7f08bf9
    b LAB_0801dbca                           @ 0801db8e 1ce0
DAT_0801db90:
    .word  0x0984b994                     @ 0801db90 94b98409
DAT_0801db94:
    .word  0x050000a0                     @ 0801db94 a0000005
DAT_0801db98:
    .word  0x050003a0                     @ 0801db98 a0030005
DAT_0801db9c:
    .word  0x0984de4c                     @ 0801db9c 4cde8409
DAT_0801dba0:
    .word  0x06017440                     @ 0801dba0 40740106
DAT_0801dba4:
    .word  0x0984dc6c                     @ 0801dba4 6cdc8409
DAT_0801dba8:
    .word  0x050003c0                     @ 0801dba8 c0030005
DAT_0801dbac:
    .word  0x0984f52c                     @ 0801dbac 2cf58409
DAT_0801dbb0:
    .word  0x060174c0                     @ 0801dbb0 c0740106
DAT_0801dbb4:
    .word  0x0984f46c                     @ 0801dbb4 6cf48409
LAB_0801dbb8:
    ldr r0,[sp,#0x4]                         @ 0801dbb8 0198
    ldr r1,[sp,#0x8]                         @ 0801dbba 0299
    bl draw_atk_def_label_to_vram            @ 0801dbbc fff708fe
    b LAB_0801dbca                           @ 0801dbc0 03e0
LAB_0801dbc2:
    ldr r0,[sp,#0x4]                         @ 0801dbc2 0198
    ldr r1,[sp,#0x8]                         @ 0801dbc4 0299
    bl draw_atk_def_label_to_vram            @ 0801dbc6 fff703fe
LAB_0801dbca:
    add sp,#0xc                              @ 0801dbca 03b0
    pop {r3,r4,r5}                           @ 0801dbcc 38bc
    .hword 0x4698    @ 0801dbce 9846
    .hword 0x46a1    @ 0801dbd0 a146
    .hword 0x46aa    @ 0801dbd2 aa46
    pop {r4,r5,r6,r7}                        @ 0801dbd4 f0bc
    pop {r0}                                 @ 0801dbd6 01bc
    bx r0                                    @ 0801dbd8 0047
    .zero  0x2

@ p1/p2: 页面动画/过渡 (非 tile 写入), 待细化
card_info_page_step_03_unknown:
    push {r4,r5,r6,r7,lr}                    @ 0801dbdc f0b5
    .hword 0x4657    @ 0801dbde 5746
    .hword 0x464e    @ 0801dbe0 4e46
    .hword 0x4645    @ 0801dbe2 4546
    push {r5,r6,r7}                          @ 0801dbe4 e0b4
    sub sp,#0x4                              @ 0801dbe6 81b0
    movs r0,#0x0    @ 0801dbe8 0020
    .hword 0x4681    @ 0801dbea 8146
    movs r1,#0x2    @ 0801dbec 0221
    .hword 0x468a    @ 0801dbee 8a46
    movs r2,#0x0    @ 0801dbf0 0022
    str r2,[sp,#0x0]                         @ 0801dbf2 0092
    ldr r2, DAT_0801dc28                     @ 0801dbf4 0c4a
    ldr r0, DAT_0801dc2c                     @ 0801dbf6 0d48
    ldr r3, DAT_0801dc30                     @ 0801dbf8 0d4b
    adds r0,r0,r3    @ 0801dbfa c018
    ldrb r3,[r0,#0x0]                        @ 0801dbfc 0378
    movs r0,#0x7    @ 0801dbfe 0720
    ands r0,r3    @ 0801dc00 1840
    rsbs r0,r0,#0    @ 0801dc02 4042
    lsrs r0,r0,#0x1f    @ 0801dc04 c00f
    subs r1,#0x4    @ 0801dc06 0439
    ldrb r4,[r2,#0x8]                        @ 0801dc08 147a
    ands r1,r4    @ 0801dc0a 2140
    orrs r1,r0    @ 0801dc0c 0143
    strb r1,[r2,#0x8]                        @ 0801dc0e 1172
    ldr r1, DAT_0801dc34                     @ 0801dc10 0849
    movs r0,#0x1    @ 0801dc12 0120
    ldrb r2,[r1,#0x0]                        @ 0801dc14 0a78
    ands r0,r2    @ 0801dc16 1040
    cmp r0,#0x0                              @ 0801dc18 0028
    beq LAB_0801dc38                         @ 0801dc1a 0dd0
    ldr r0,[r1,#0x0]                         @ 0801dc1c 0868
    lsls r0,r0,#0xf    @ 0801dc1e c003
    lsrs r0,r0,#0x12    @ 0801dc20 800c
    bl resolve_card_gfx_pointer_by_type      @ 0801dc22 d0f0b1fe
    b LAB_0801dc46                           @ 0801dc26 0ee0
DAT_0801dc28:
    .word  0x02006ed0                     @ 0801dc28 d06e0002
DAT_0801dc2c:
    .word  0x02000000                     @ 0801dc2c 00000002
DAT_0801dc30:
    .word  0x00006c2c                     @ 0801dc30 2c6c0000
DAT_0801dc34:
    .word  0x0201afb0                     @ 0801dc34 b0af0102
LAB_0801dc38:
    ldr r0,[r1,#0x0]                         @ 0801dc38 0868
    lsls r0,r0,#0xf    @ 0801dc3a c003
    lsrs r0,r0,#0x12    @ 0801dc3c 800c
    lsls r1,r3,#0x1d    @ 0801dc3e 5907
    lsrs r1,r1,#0x1d    @ 0801dc40 490f
    bl select_charset_then_load_name         @ 0801dc42 d0f0b3fd
LAB_0801dc46:
    adds r6,r0,#0x0    @ 0801dc46 061c
    ldr r0, DAT_0801dc9c                     @ 0801dc48 1448
    ldr r3, DAT_0801dca0                     @ 0801dc4a 154b
    adds r0,r0,r3    @ 0801dc4c c018
    movs r1,#0x7    @ 0801dc4e 0721
    ldrb r0,[r0,#0x0]                        @ 0801dc50 0078
    ands r1,r0    @ 0801dc52 0140
    cmp r1,#0x0                              @ 0801dc54 0029
    bne LAB_0801dcac                         @ 0801dc56 29d1
    adds r4,r6,#0x0    @ 0801dc58 341c
    ldr r2, DAT_0801dca4                     @ 0801dc5a 124a
    movs r0,#0x2    @ 0801dc5c 0220
    rsbs r0,r0,#0    @ 0801dc5e 4042
    ldrb r1,[r2,#0x8]                        @ 0801dc60 117a
    ands r0,r1    @ 0801dc62 0840
    movs r1,#0x2    @ 0801dc64 0221
    orrs r0,r1    @ 0801dc66 0843
    strb r0,[r2,#0x8]                        @ 0801dc68 1072
    ldr r1, PTR_font_jp_base_table_0801dca8  @ 0801dc6a 0f49
    lsls r0,r0,#0x1e    @ 0801dc6c 8007
    lsrs r0,r0,#0x1f    @ 0801dc6e c00f
    lsls r0,r0,#0x2    @ 0801dc70 8000
    adds r0,r0,r1    @ 0801dc72 4018
    ldr r0,[r0,#0x0]                         @ 0801dc74 0068
    str r0,[r2,#0x4]                         @ 0801dc76 5060
    movs r2,#0x0    @ 0801dc78 0022
    .hword 0x4691    @ 0801dc7a 9146
    ldrb r0,[r6,#0x0]                        @ 0801dc7c 3078
    cmp r0,#0x0                              @ 0801dc7e 0028
    beq LAB_0801dd40                         @ 0801dc80 5ed0
LAB_0801dc82:
    ldrb r3,[r4,#0x0]                        @ 0801dc82 2378
    lsls r0,r3,#0x8    @ 0801dc84 1802
    ldrb r1,[r4,#0x1]                        @ 0801dc86 6178
    orrs r0,r1    @ 0801dc88 0843
    bl char_width_wide_10_or_12              @ 0801dc8a d2f0c1fa
    add r9,r0                                @ 0801dc8e 8144
    adds r4,#0x2    @ 0801dc90 0234
    ldrb r0,[r4,#0x0]                        @ 0801dc92 2078
    cmp r0,#0x0                              @ 0801dc94 0028
    bne LAB_0801dc82                         @ 0801dc96 f4d1
    b LAB_0801dd40                           @ 0801dc98 52e0
    .zero  0x2
DAT_0801dc9c:
    .word  0x02000000                     @ 0801dc9c 00000002
DAT_0801dca0:
    .word  0x00006c2c                     @ 0801dca0 2c6c0000
DAT_0801dca4:
    .word  0x02006ed0                     @ 0801dca4 d06e0002
PTR_font_jp_base_table_0801dca8:
    .word  font_jp_base_table             @ 0801dca8 54f8e509
LAB_0801dcac:
    adds r5,r6,#0x0    @ 0801dcac 351c
    ldr r2, DAT_0801dd04                     @ 0801dcae 154a
    rsbs r1,r1,#0    @ 0801dcb0 4942
    lsrs r1,r1,#0x1f    @ 0801dcb2 c90f
    movs r0,#0x2    @ 0801dcb4 0220
    rsbs r0,r0,#0    @ 0801dcb6 4042
    ldrb r3,[r2,#0x8]                        @ 0801dcb8 137a
    ands r0,r3    @ 0801dcba 1840
    orrs r0,r1    @ 0801dcbc 0843
    strb r0,[r2,#0x8]                        @ 0801dcbe 1072
    ldr r3, PTR_font_jp_base_table_0801dd08  @ 0801dcc0 114b
    lsls r1,r0,#0x1e    @ 0801dcc2 8107
    lsrs r1,r1,#0x1f    @ 0801dcc4 c90f
    lsls r1,r1,#0x2    @ 0801dcc6 8900
    lsls r0,r0,#0x1f    @ 0801dcc8 c007
    lsrs r0,r0,#0x1f    @ 0801dcca c00f
    lsls r0,r0,#0x3    @ 0801dccc c000
    adds r1,r1,r0    @ 0801dcce 0918
    adds r1,r1,r3    @ 0801dcd0 c918
    ldr r0,[r1,#0x0]                         @ 0801dcd2 0868
    str r0,[r2,#0x4]                         @ 0801dcd4 5060
    ldrb r0,[r6,#0x0]                        @ 0801dcd6 3078
    cmp r0,#0x0                              @ 0801dcd8 0028
    beq LAB_0801dd40                         @ 0801dcda 31d0
    adds r4,r2,#0x0    @ 0801dcdc 141c
    adds r7,r3,#0x0    @ 0801dcde 1f1c
LAB_0801dce0:
    ldrb r1,[r5,#0x0]                        @ 0801dce0 2978
    ldr r0, DAT_0801dd0c                     @ 0801dce2 0a48
    adds r0,r1,r0    @ 0801dce4 0818
    ldrb r0,[r0,#0x0]                        @ 0801dce6 0078
    cmp r0,r1                                @ 0801dce8 8842
    beq LAB_0801dd10                         @ 0801dcea 11d0
    movs r1,#0x3    @ 0801dcec 0321
    rsbs r1,r1,#0    @ 0801dcee 4942
    adds r0,r1,#0x0    @ 0801dcf0 081c
    ldrb r2,[r4,#0x8]                        @ 0801dcf2 227a
    ands r0,r2    @ 0801dcf4 1040
    strb r0,[r4,#0x8]                        @ 0801dcf6 2072
    lsls r0,r0,#0x1f    @ 0801dcf8 c007
    lsrs r0,r0,#0x1f    @ 0801dcfa c00f
    lsls r0,r0,#0x3    @ 0801dcfc c000
    adds r0,r0,r7    @ 0801dcfe c019
    ldr r0,[r0,#0x0]                         @ 0801dd00 0068
    b LAB_0801dd2a                           @ 0801dd02 12e0
DAT_0801dd04:
    .word  0x02006ed0                     @ 0801dd04 d06e0002
PTR_font_jp_base_table_0801dd08:
    .word  font_jp_base_table             @ 0801dd08 54f8e509
DAT_0801dd0c:
    .word  0x09e589c4                     @ 0801dd0c c489e509
LAB_0801dd10:
    movs r0,#0x2    @ 0801dd10 0220
    ldrb r3,[r4,#0x8]                        @ 0801dd12 237a
    orrs r0,r3    @ 0801dd14 1843
    strb r0,[r4,#0x8]                        @ 0801dd16 2072
    lsls r1,r0,#0x1e    @ 0801dd18 8107
    lsrs r1,r1,#0x1f    @ 0801dd1a c90f
    lsls r1,r1,#0x2    @ 0801dd1c 8900
    lsls r0,r0,#0x1f    @ 0801dd1e c007
    lsrs r0,r0,#0x1f    @ 0801dd20 c00f
    lsls r0,r0,#0x3    @ 0801dd22 c000
    adds r1,r1,r0    @ 0801dd24 0918
    adds r1,r1,r7    @ 0801dd26 c919
    ldr r0,[r1,#0x0]                         @ 0801dd28 0868
LAB_0801dd2a:
    str r0,[r4,#0x4]                         @ 0801dd2a 6060
    bl char_width_narrow_5                   @ 0801dd2c d2f068fa
    .hword 0x4649    @ 0801dd30 4946
    adds r1,#0x1    @ 0801dd32 0131
    adds r1,r1,r0    @ 0801dd34 0918
    .hword 0x4689    @ 0801dd36 8946
    adds r5,#0x1    @ 0801dd38 0135
    ldrb r0,[r5,#0x0]                        @ 0801dd3a 2878
    cmp r0,#0x0                              @ 0801dd3c 0028
    bne LAB_0801dce0                         @ 0801dd3e cfd1
LAB_0801dd40:
    ldr r0, DAT_0801dd90                     @ 0801dd40 1348
    .hword 0x464c    @ 0801dd42 4c46
    str r4,[r0,#0x14]                        @ 0801dd44 4461
    ldr r1, DAT_0801dd94                     @ 0801dd46 1349
    ldr r0, DAT_0801dd98                     @ 0801dd48 1348
    adds r1,r1,r0    @ 0801dd4a 0918
    movs r0,#0x7    @ 0801dd4c 0720
    ldrb r1,[r1,#0x0]                        @ 0801dd4e 0978
    ands r0,r1    @ 0801dd50 0840
    cmp r0,#0x0                              @ 0801dd52 0028
    bne LAB_0801ddf4                         @ 0801dd54 4ed1
    adds r7,r6,#0x0    @ 0801dd56 371c
    ldr r2, DAT_0801dd9c                     @ 0801dd58 104a
    movs r0,#0x2    @ 0801dd5a 0220
    rsbs r0,r0,#0    @ 0801dd5c 4042
    ldrb r1,[r2,#0x8]                        @ 0801dd5e 117a
    ands r0,r1    @ 0801dd60 0840
    movs r1,#0x2    @ 0801dd62 0221
    orrs r0,r1    @ 0801dd64 0843
    strb r0,[r2,#0x8]                        @ 0801dd66 1072
    ldr r1, PTR_font_jp_base_table_0801dda0  @ 0801dd68 0d49
    lsls r0,r0,#0x1e    @ 0801dd6a 8007
    lsrs r0,r0,#0x1f    @ 0801dd6c c00f
    lsls r0,r0,#0x2    @ 0801dd6e 8000
    adds r0,r0,r1    @ 0801dd70 4018
    ldr r0,[r0,#0x0]                         @ 0801dd72 0068
    str r0,[r2,#0x4]                         @ 0801dd74 5060
    cmp r4,#0xe8                             @ 0801dd76 e82c
    bgt LAB_0801dda4                         @ 0801dd78 14dc
    lsrs r0,r4,#0x1f    @ 0801dd7a e00f
    add r0,r9                                @ 0801dd7c 4844
    asrs r0,r0,#0x1    @ 0801dd7e 4010
    movs r1,#0x78    @ 0801dd80 7821
    subs r6,r1,r0    @ 0801dd82 0e1a
    movs r0,#0x20    @ 0801dd84 2020
    movs r1,#0x2    @ 0801dd86 0221
    bl setup_line_buf_pos_and_font           @ 0801dd88 d2f014ff
    b LAB_0801ddb2                           @ 0801dd8c 11e0
    .zero  0x2
DAT_0801dd90:
    .word  0x0201afb0                     @ 0801dd90 b0af0102
DAT_0801dd94:
    .word  0x02000000                     @ 0801dd94 00000002
DAT_0801dd98:
    .word  0x00006c2c                     @ 0801dd98 2c6c0000
DAT_0801dd9c:
    .word  0x02006ed0                     @ 0801dd9c d06e0002
PTR_font_jp_base_table_0801dda0:
    .word  font_jp_base_table             @ 0801dda0 54f8e509
LAB_0801dda4:
    movs r6,#0x4    @ 0801dda4 0426
    movs r0,#0x40    @ 0801dda6 4020
    movs r1,#0x2    @ 0801dda8 0221
    bl setup_line_buf_pos_and_font           @ 0801ddaa d2f003ff
    movs r2,#0x1    @ 0801ddae 0122
    str r2,[sp,#0x0]                         @ 0801ddb0 0092
LAB_0801ddb2:
    ldrb r0,[r7,#0x0]                        @ 0801ddb2 3878
    cmp r0,#0x0                              @ 0801ddb4 0028
    bne LAB_0801ddba                         @ 0801ddb6 00d1
    b LAB_0801dede                           @ 0801ddb8 91e0
LAB_0801ddba:
    ldrb r3,[r7,#0x0]                        @ 0801ddba 3b78
    lsls r4,r3,#0x8    @ 0801ddbc 1c02
    ldrb r0,[r7,#0x1]                        @ 0801ddbe 7878
    orrs r4,r0    @ 0801ddc0 0443
    adds r0,r4,#0x0    @ 0801ddc2 201c
    bl char_width_wide_10_or_12              @ 0801ddc4 d2f024fa
    adds r5,r0,#0x0    @ 0801ddc8 051c
    adds r0,r4,#0x0    @ 0801ddca 201c
    adds r1,r6,#0x0    @ 0801ddcc 311c
    .hword 0x4652    @ 0801ddce 5246
    ldr r3, DAT_0801ddf0                     @ 0801ddd0 074b
    bl render_glyph_jp_dual_layer            @ 0801ddd2 d3f057fd
    adds r0,r4,#0x0    @ 0801ddd6 201c
    adds r1,r6,#0x0    @ 0801ddd8 311c
    .hword 0x4652    @ 0801ddda 5246
    movs r3,#0x7    @ 0801dddc 0723
    bl render_glyph_jp_dual_layer            @ 0801ddde d3f051fd
    adds r6,r6,r5    @ 0801dde2 7619
    adds r7,#0x2    @ 0801dde4 0237
    ldrb r0,[r7,#0x0]                        @ 0801dde6 3878
    cmp r0,#0x0                              @ 0801dde8 0028
    bne LAB_0801ddba                         @ 0801ddea e6d1
    b LAB_0801dede                           @ 0801ddec 77e0
    .zero  0x2
DAT_0801ddf0:
    .word  0x00008008                     @ 0801ddf0 08800000
LAB_0801ddf4:
    .hword 0x46b0    @ 0801ddf4 b046
    ldr r2, DAT_0801de30                     @ 0801ddf6 0e4a
    movs r1,#0x2    @ 0801ddf8 0221
    ldrb r3,[r2,#0x8]                        @ 0801ddfa 137a
    orrs r1,r3    @ 0801ddfc 1943
    strb r1,[r2,#0x8]                        @ 0801ddfe 1172
    ldr r3, PTR_font_jp_base_table_0801de34  @ 0801de00 0c4b
    lsls r0,r1,#0x1e    @ 0801de02 8807
    lsrs r0,r0,#0x1f    @ 0801de04 c00f
    lsls r0,r0,#0x2    @ 0801de06 8000
    lsls r1,r1,#0x1f    @ 0801de08 c907
    lsrs r1,r1,#0x1f    @ 0801de0a c90f
    lsls r1,r1,#0x3    @ 0801de0c c900
    adds r0,r0,r1    @ 0801de0e 4018
    adds r0,r0,r3    @ 0801de10 c018
    ldr r0,[r0,#0x0]                         @ 0801de12 0068
    str r0,[r2,#0x4]                         @ 0801de14 5060
    .hword 0x464c    @ 0801de16 4c46
    cmp r4,#0xe8                             @ 0801de18 e82c
    bgt LAB_0801de38                         @ 0801de1a 0ddc
    lsrs r0,r4,#0x1f    @ 0801de1c e00f
    add r0,r9                                @ 0801de1e 4844
    asrs r0,r0,#0x1    @ 0801de20 4010
    movs r1,#0x78    @ 0801de22 7821
    subs r6,r1,r0    @ 0801de24 0e1a
    movs r0,#0x20    @ 0801de26 2020
    movs r1,#0x2    @ 0801de28 0221
    bl setup_line_buf_pos_and_font           @ 0801de2a d2f0c3fe
    b LAB_0801de46                           @ 0801de2e 0ae0
DAT_0801de30:
    .word  0x02006ed0                     @ 0801de30 d06e0002
PTR_font_jp_base_table_0801de34:
    .word  font_jp_base_table             @ 0801de34 54f8e509
LAB_0801de38:
    movs r6,#0x4    @ 0801de38 0426
    movs r0,#0x40    @ 0801de3a 4020
    movs r1,#0x2    @ 0801de3c 0221
    bl setup_line_buf_pos_and_font           @ 0801de3e d2f0b9fe
    movs r0,#0x1    @ 0801de42 0120
    str r0,[sp,#0x0]                         @ 0801de44 0090
LAB_0801de46:
    .hword 0x4641    @ 0801de46 4146
    ldrb r0,[r1,#0x0]                        @ 0801de48 0878
    cmp r0,#0x0                              @ 0801de4a 0028
    beq LAB_0801dede                         @ 0801de4c 47d0
    ldr r7, DAT_0801de84                     @ 0801de4e 0d4f
    ldr r2, PTR_font_jp_base_table_0801de88  @ 0801de50 0d4a
    .hword 0x4691    @ 0801de52 9146
LAB_0801de54:
    .hword 0x4643    @ 0801de54 4346
    ldrb r5,[r3,#0x0]                        @ 0801de56 1d78
    ldr r0, DAT_0801de8c                     @ 0801de58 0c48
    adds r0,r5,r0    @ 0801de5a 2818
    ldrb r4,[r0,#0x0]                        @ 0801de5c 0478
    cmp r4,r5                                @ 0801de5e ac42
    beq LAB_0801de90                         @ 0801de60 16d0
    ldrb r5,[r0,#0x0]                        @ 0801de62 0578
    movs r1,#0x3    @ 0801de64 0321
    rsbs r1,r1,#0    @ 0801de66 4942
    adds r0,r1,#0x0    @ 0801de68 081c
    ldrb r2,[r7,#0x8]                        @ 0801de6a 3a7a
    ands r0,r2    @ 0801de6c 1040
    strb r0,[r7,#0x8]                        @ 0801de6e 3872
    lsls r0,r0,#0x1f    @ 0801de70 c007
    lsrs r0,r0,#0x1f    @ 0801de72 c00f
    lsls r0,r0,#0x3    @ 0801de74 c000
    add r0,r9                                @ 0801de76 4844
    ldr r0,[r0,#0x0]                         @ 0801de78 0068
    str r0,[r7,#0x4]                         @ 0801de7a 7860
    movs r3,#0x3    @ 0801de7c 0323
    .hword 0x469a    @ 0801de7e 9a46
    b LAB_0801deb0                           @ 0801de80 16e0
    .zero  0x2
DAT_0801de84:
    .word  0x02006ed0                     @ 0801de84 d06e0002
PTR_font_jp_base_table_0801de88:
    .word  font_jp_base_table             @ 0801de88 54f8e509
DAT_0801de8c:
    .word  0x09e589c4                     @ 0801de8c c489e509
LAB_0801de90:
    movs r0,#0x2    @ 0801de90 0220
    ldrb r4,[r7,#0x8]                        @ 0801de92 3c7a
    orrs r0,r4    @ 0801de94 2043
    strb r0,[r7,#0x8]                        @ 0801de96 3872
    lsls r1,r0,#0x1e    @ 0801de98 8107
    lsrs r1,r1,#0x1f    @ 0801de9a c90f
    lsls r1,r1,#0x2    @ 0801de9c 8900
    lsls r0,r0,#0x1f    @ 0801de9e c007
    lsrs r0,r0,#0x1f    @ 0801dea0 c00f
    lsls r0,r0,#0x3    @ 0801dea2 c000
    adds r1,r1,r0    @ 0801dea4 0918
    add r1,r9                                @ 0801dea6 4944
    ldr r0,[r1,#0x0]                         @ 0801dea8 0868
    str r0,[r7,#0x4]                         @ 0801deaa 7860
    movs r0,#0x2    @ 0801deac 0220
    .hword 0x4682    @ 0801deae 8246
LAB_0801deb0:
    bl char_width_narrow_5                   @ 0801deb0 d2f0a6f9
    adds r4,r0,#0x0    @ 0801deb4 041c
    adds r4,#0x1    @ 0801deb6 0134
    adds r0,r5,#0x0    @ 0801deb8 281c
    adds r1,r6,#0x0    @ 0801deba 311c
    .hword 0x4652    @ 0801debc 5246
    ldr r3, DAT_0801df48                     @ 0801debe 224b
    bl render_glyph_jp_single_layer          @ 0801dec0 d3f070fd
    adds r0,r5,#0x0    @ 0801dec4 281c
    adds r1,r6,#0x0    @ 0801dec6 311c
    .hword 0x4652    @ 0801dec8 5246
    movs r3,#0x7    @ 0801deca 0723
    bl render_glyph_jp_single_layer          @ 0801decc d3f06afd
    adds r6,r6,r4    @ 0801ded0 3619
    movs r1,#0x1    @ 0801ded2 0121
    add r8,r1                                @ 0801ded4 8844
    .hword 0x4642    @ 0801ded6 4246
    ldrb r0,[r2,#0x0]                        @ 0801ded8 1078
    cmp r0,#0x0                              @ 0801deda 0028
    bne LAB_0801de54                         @ 0801dedc bad1
LAB_0801dede:
    ldr r4, DAT_0801df4c                     @ 0801dede 1b4c
    movs r1,#0x80    @ 0801dee0 8021
    lsls r1,r1,#0x5    @ 0801dee2 4901
    adds r0,r4,#0x0    @ 0801dee4 201c
    bl zero_fill_by_halfword                 @ 0801dee6 d6f0c5ff
    adds r0,r4,#0x0    @ 0801deea 201c
    movs r1,#0x0    @ 0801deec 0021
    bl commit_line_buffer_to_sprite_vram     @ 0801deee d4f0adff
    ldr r3,[sp,#0x0]                         @ 0801def2 009b
    cmp r3,#0x0                              @ 0801def4 002b
    beq LAB_0801df5c                         @ 0801def6 31d0
    movs r4,#0xc4    @ 0801def8 c424
    lsls r4,r4,#0x1    @ 0801defa 6400
    movs r1,#0x0    @ 0801defc 0021
    ldr r6, DAT_0801df50                     @ 0801defe 144e
    ldr r7, PTR_gPrng_0801df54               @ 0801df00 144f
LAB_0801df02:
    adds r0,r1,#0x0    @ 0801df02 081c
    adds r0,#0x12    @ 0801df04 1230
    lsls r0,r0,#0x10    @ 0801df06 0004
    lsrs r0,r0,#0xa    @ 0801df08 800a
    ldr r3, DAT_0801df58                     @ 0801df0a 134b
    adds r2,r0,r3    @ 0801df0c c218
    adds r5,r1,#0x1    @ 0801df0e 4d1c
    movs r3,#0x1f    @ 0801df10 1f23
LAB_0801df12:
    adds r1,r4,#0x0    @ 0801df12 211c
    adds r0,r1,#0x1    @ 0801df14 481c
    lsls r0,r0,#0x10    @ 0801df16 0004
    lsrs r4,r0,#0x10    @ 0801df18 040c
    strh r1,[r2,#0x0]                        @ 0801df1a 1180
    adds r2,#0x2    @ 0801df1c 0232
    subs r3,#0x1    @ 0801df1e 013b
    cmp r3,#0x0                              @ 0801df20 002b
    bge LAB_0801df12                         @ 0801df22 f6da
    movs r0,#0xf8    @ 0801df24 f820
    lsls r0,r0,#0x3    @ 0801df26 c000
    adds r2,r2,r0    @ 0801df28 1218
    movs r3,#0x1f    @ 0801df2a 1f23
LAB_0801df2c:
    adds r1,r4,#0x0    @ 0801df2c 211c
    adds r0,r1,#0x1    @ 0801df2e 481c
    lsls r0,r0,#0x10    @ 0801df30 0004
    lsrs r4,r0,#0x10    @ 0801df32 040c
    strh r1,[r2,#0x0]                        @ 0801df34 1180
    adds r2,#0x2    @ 0801df36 0232
    subs r3,#0x1    @ 0801df38 013b
    cmp r3,#0x0                              @ 0801df3a 002b
    bge LAB_0801df2c                         @ 0801df3c f6da
    adds r1,r5,#0x0    @ 0801df3e 291c
    cmp r1,#0x1                              @ 0801df40 0129
    ble LAB_0801df02                         @ 0801df42 dedd
    b LAB_0801df76                           @ 0801df44 17e0
    .zero  0x2
DAT_0801df48:
    .word  0x00008008                     @ 0801df48 08800000
DAT_0801df4c:
    .word  0x06007100                     @ 0801df4c 00710006
DAT_0801df50:
    .word  0x0201afb0                     @ 0801df50 b0af0102
PTR_gPrng_0801df54:
    .word  gPrng                          @ 0801df54 40000003
DAT_0801df58:
    .word  0x06000800                     @ 0801df58 00080006
LAB_0801df5c:
    ldr r1, DAT_0801df94                     @ 0801df5c 0d49
    movs r3,#0x0    @ 0801df5e 0023
    ldr r6, DAT_0801df98                     @ 0801df60 0d4e
    ldr r7, PTR_gPrng_0801df9c               @ 0801df62 0e4f
    movs r4,#0xc4    @ 0801df64 c424
    lsls r4,r4,#0x1    @ 0801df66 6400
    adds r2,r4,#0x0    @ 0801df68 221c
LAB_0801df6a:
    adds r0,r3,r2    @ 0801df6a 9818
    strh r0,[r1,#0x0]                        @ 0801df6c 0880
    adds r1,#0x2    @ 0801df6e 0231
    adds r3,#0x1    @ 0801df70 0133
    cmp r3,#0x7f                             @ 0801df72 7f2b
    ble LAB_0801df6a                         @ 0801df74 f9dd
LAB_0801df76:
    movs r0,#0x0    @ 0801df76 0020
    str r0,[r6,#0x18]                        @ 0801df78 b061
    str r0,[r6,#0x1c]                        @ 0801df7a f061
    movs r2,#0xf1    @ 0801df7c f122
    lsls r2,r2,#0x1    @ 0801df7e 5200
    adds r1,r7,r2    @ 0801df80 b918
    strh r0,[r1,#0x0]                        @ 0801df82 0880
    add sp,#0x4                              @ 0801df84 01b0
    pop {r3,r4,r5}                           @ 0801df86 38bc
    .hword 0x4698    @ 0801df88 9846
    .hword 0x46a1    @ 0801df8a a146
    .hword 0x46aa    @ 0801df8c aa46
    pop {r4,r5,r6,r7}                        @ 0801df8e f0bc
    pop {r0}                                 @ 0801df90 01bc
    bx r0                                    @ 0801df92 0047
DAT_0801df94:
    .word  0x06000c80                     @ 0801df94 800c0006
DAT_0801df98:
    .word  0x0201afb0                     @ 0801df98 b0af0102
PTR_gPrng_0801df9c:
    .word  gPrng                          @ 0801df9c 40000003

@ 被 FUN_0801e714 (card_info 场景主循环) 唯一调用, 是卡片信息场景的逐帧滚动位置更新函数. 从 EWRAM 结构体 0x0201afb0 读取字段 [+0x14] (帧计数器), 若超过 0xe8=232 则将帧计数器继续递增并以帧数计算滚动偏移量, 写入 [+0x18] (像素 Y 偏移) 和 [+0x1c] (子计数器); 若帧计数器未超阈值则清零并停止滚动. 最终写 VRAM 0x03000240 (gFrameCounter 偏移处) 的对应字段以同步 HW 位置.
tick_scroll_frame_and_update_pos:
    push {r4,lr}                             @ 0801dfa0 10b5
    ldr r0, DAT_0801dfd0                     @ 0801dfa2 0b48
    ldr r1,[r0,#0x14]                        @ 0801dfa4 4169
    adds r3,r0,#0x0    @ 0801dfa6 031c
    cmp r1,#0xe8                             @ 0801dfa8 e829
    ble LAB_0801dff4                         @ 0801dfaa 23dd
    adds r0,r1,#0x0    @ 0801dfac 081c
    subs r0,#0xe8    @ 0801dfae e838
    lsls r4,r0,#0x1    @ 0801dfb0 4400
    adds r1,r4,#0x0    @ 0801dfb2 211c
    adds r1,#0xd2    @ 0801dfb4 d231
    ldr r0,[r3,#0x1c]                        @ 0801dfb6 d869
    adds r0,#0x1    @ 0801dfb8 0130
    str r0,[r3,#0x1c]                        @ 0801dfba d861
    cmp r0,r1                                @ 0801dfbc 8842
    blt LAB_0801dfc4                         @ 0801dfbe 01db
    movs r0,#0x0    @ 0801dfc0 0020
    str r0,[r3,#0x1c]                        @ 0801dfc2 d861
LAB_0801dfc4:
    ldr r2,[r3,#0x1c]                        @ 0801dfc4 da69
    cmp r2,#0x5a                             @ 0801dfc6 5a2a
    bgt LAB_0801dfd4                         @ 0801dfc8 04dc
    movs r0,#0x0    @ 0801dfca 0020
    b LAB_0801dfe6                           @ 0801dfcc 0be0
    .zero  0x2
DAT_0801dfd0:
    .word  0x0201afb0                     @ 0801dfd0 b0af0102
LAB_0801dfd4:
    adds r0,r4,#0x0    @ 0801dfd4 201c
    adds r0,#0x5a    @ 0801dfd6 5a30
    cmp r2,r0                                @ 0801dfd8 8242
    bgt LAB_0801dfe8                         @ 0801dfda 05dc
    adds r0,r2,#0x0    @ 0801dfdc 101c
    subs r0,#0x5a    @ 0801dfde 5a38
    lsrs r1,r0,#0x1f    @ 0801dfe0 c10f
    adds r0,r0,r1    @ 0801dfe2 4018
    asrs r0,r0,#0x1    @ 0801dfe4 4010
LAB_0801dfe6:
    str r0,[r3,#0x18]                        @ 0801dfe6 9861
LAB_0801dfe8:
    ldr r0, PTR_gPrng_0801dffc               @ 0801dfe8 0448
    ldr r1,[r3,#0x18]                        @ 0801dfea 9969
    movs r2,#0xf1    @ 0801dfec f122
    lsls r2,r2,#0x1    @ 0801dfee 5200
    adds r0,r0,r2    @ 0801dff0 8018
    strh r1,[r0,#0x0]                        @ 0801dff2 0180
LAB_0801dff4:
    pop {r4}                                 @ 0801dff4 10bc
    pop {r0}                                 @ 0801dff6 01bc
    bx r0                                    @ 0801dff8 0047
    .zero  0x2
PTR_gPrng_0801dffc:
    .word  gPrng                          @ 0801dffc 40000003

@ p2: 字段/描述绘制入口, 字面量池含 .word 0x06010040
render_card_description_text:
    push {r4,r5,r6,r7,lr}                    @ 0801e000 f0b5
    .hword 0x464f    @ 0801e002 4f46
    .hword 0x4646    @ 0801e004 4646
    push {r6,r7}                             @ 0801e006 c0b4
    .hword 0x4680    @ 0801e008 8046
    ldr r4, DAT_0801e0e8                     @ 0801e00a 374c
    ldr r0, DAT_0801e0ec                     @ 0801e00c 3748
    ldr r1, DAT_0801e0f0                     @ 0801e00e 3849
    adds r5,r0,r1    @ 0801e010 4518
    movs r6,#0x7    @ 0801e012 0726
    adds r1,r6,#0x0    @ 0801e014 311c
    ldrb r2,[r5,#0x0]                        @ 0801e016 2a78
    ands r1,r2    @ 0801e018 1140
    rsbs r1,r1,#0    @ 0801e01a 4942
    lsrs r1,r1,#0x1f    @ 0801e01c c90f
    movs r0,#0x2    @ 0801e01e 0220
    rsbs r0,r0,#0    @ 0801e020 4042
    ldrb r2,[r4,#0x8]                        @ 0801e022 227a
    ands r0,r2    @ 0801e024 1040
    orrs r0,r1    @ 0801e026 0843
    movs r1,#0x2    @ 0801e028 0221
    orrs r0,r1    @ 0801e02a 0843
    strb r0,[r4,#0x8]                        @ 0801e02c 2072
    ldr r1, PTR_font_jp_base_table_0801e0f4  @ 0801e02e 3149
    .hword 0x4689    @ 0801e030 8946
    lsls r1,r0,#0x1e    @ 0801e032 8107
    lsrs r1,r1,#0x1f    @ 0801e034 c90f
    lsls r1,r1,#0x2    @ 0801e036 8900
    lsls r0,r0,#0x1f    @ 0801e038 c007
    lsrs r0,r0,#0x1f    @ 0801e03a c00f
    lsls r0,r0,#0x3    @ 0801e03c c000
    adds r1,r1,r0    @ 0801e03e 0918
    add r1,r9                                @ 0801e040 4944
    ldr r0,[r1,#0x0]                         @ 0801e042 0868
    str r0,[r4,#0x4]                         @ 0801e044 6060
    movs r0,#0x10    @ 0801e046 1020
    movs r1,#0x3a    @ 0801e048 3a21
    movs r2,#0x1    @ 0801e04a 0122
    movs r3,#0x1    @ 0801e04c 0123
    bl setup_line_buf_with_font_and_align    @ 0801e04e d2f037fe
    movs r7,#0x40    @ 0801e052 4027
    ldrb r0,[r4,#0x15]                       @ 0801e054 607d
    orrs r0,r7    @ 0801e056 3843
    strb r0,[r4,#0x15]                       @ 0801e058 6075
    adds r0,r6,#0x0    @ 0801e05a 301c
    ldrb r2,[r5,#0x0]                        @ 0801e05c 2a78
    ands r0,r2    @ 0801e05e 1040
    movs r1,#0x0    @ 0801e060 0021
    cmp r0,#0x0                              @ 0801e062 0028
    bne LAB_0801e068                         @ 0801e064 00d1
    movs r1,#0x2    @ 0801e066 0221
LAB_0801e068:
    adds r0,r1,#0x0    @ 0801e068 081c
    movs r1,#0x2    @ 0801e06a 0221
    movs r2,#0x7    @ 0801e06c 0722
    .hword 0x4643    @ 0801e06e 4346
    bl text_render_wrapper                   @ 0801e070 d4f004fd
    ldrh r0,[r4,#0xe]                        @ 0801e074 e089
    lsls r1,r0,#0x16    @ 0801e076 8105
    movs r0,#0xe0    @ 0801e078 e020
    lsls r0,r0,#0x17    @ 0801e07a c005
    cmp r1,r0                                @ 0801e07c 8142
    bls LAB_0801e0c2                         @ 0801e07e 20d9
    movs r0,#0x3    @ 0801e080 0320
    rsbs r0,r0,#0    @ 0801e082 4042
    ldrb r1,[r4,#0x8]                        @ 0801e084 217a
    ands r0,r1    @ 0801e086 0840
    strb r0,[r4,#0x8]                        @ 0801e088 2072
    lsls r0,r0,#0x1f    @ 0801e08a c007
    lsrs r0,r0,#0x1f    @ 0801e08c c00f
    lsls r0,r0,#0x3    @ 0801e08e c000
    add r0,r9                                @ 0801e090 4844
    ldr r0,[r0,#0x0]                         @ 0801e092 0068
    str r0,[r4,#0x4]                         @ 0801e094 6060
    movs r0,#0x10    @ 0801e096 1020
    movs r1,#0x3a    @ 0801e098 3a21
    movs r2,#0x1    @ 0801e09a 0122
    movs r3,#0x1    @ 0801e09c 0123
    bl setup_line_buf_with_font_and_align    @ 0801e09e d2f00ffe
    ldrb r0,[r4,#0x15]                       @ 0801e0a2 607d
    orrs r0,r7    @ 0801e0a4 3843
    strb r0,[r4,#0x15]                       @ 0801e0a6 6075
    adds r0,r6,#0x0    @ 0801e0a8 301c
    ldrb r5,[r5,#0x0]                        @ 0801e0aa 2d78
    ands r0,r5    @ 0801e0ac 2840
    movs r1,#0x0    @ 0801e0ae 0021
    cmp r0,#0x0                              @ 0801e0b0 0028
    bne LAB_0801e0b6                         @ 0801e0b2 00d1
    movs r1,#0x2    @ 0801e0b4 0221
LAB_0801e0b6:
    adds r0,r1,#0x0    @ 0801e0b6 081c
    movs r1,#0x2    @ 0801e0b8 0221
    movs r2,#0x7    @ 0801e0ba 0722
    .hword 0x4643    @ 0801e0bc 4346
    bl text_render_wrapper                   @ 0801e0be d4f0ddfc
LAB_0801e0c2:
    ldr r1, DAT_0801e0f8                     @ 0801e0c2 0d49
    ldr r0, DAT_0801e0e8                     @ 0801e0c4 0848
    ldrh r0,[r0,#0xe]                        @ 0801e0c6 c089
    lsls r0,r0,#0x16    @ 0801e0c8 8005
    lsrs r0,r0,#0x16    @ 0801e0ca 800d
    adds r0,#0x2    @ 0801e0cc 0230
    str r0,[r1,#0x24]                        @ 0801e0ce 4862
    movs r0,#0x0    @ 0801e0d0 0020
    str r0,[r1,#0x20]                        @ 0801e0d2 0862
    ldr r0, DAT_0801e0fc                     @ 0801e0d4 0948
    movs r1,#0x0    @ 0801e0d6 0021
    bl commit_line_buffer_to_sprite_vram     @ 0801e0d8 d4f0b8fe
    pop {r3,r4}                              @ 0801e0dc 18bc
    .hword 0x4698    @ 0801e0de 9846
    .hword 0x46a1    @ 0801e0e0 a146
    pop {r4,r5,r6,r7}                        @ 0801e0e2 f0bc
    pop {r0}                                 @ 0801e0e4 01bc
    bx r0                                    @ 0801e0e6 0047
DAT_0801e0e8:
    .word  0x02006ed0                     @ 0801e0e8 d06e0002
DAT_0801e0ec:
    .word  0x02000000                     @ 0801e0ec 00000002
DAT_0801e0f0:
    .word  0x00006c2c                     @ 0801e0f0 2c6c0000
PTR_font_jp_base_table_0801e0f4:
    .word  font_jp_base_table             @ 0801e0f4 54f8e509
DAT_0801e0f8:
    .word  0x0201afb0                     @ 0801e0f8 b0af0102
DAT_0801e0fc:
    .word  0x06010040                     @ 0801e0fc 40000106

@ p2: 顶层最后一个 bl, UI 收尾
card_info_page_finalize:
    push {r4,r5,r6,r7,lr}                    @ 0801e100 f0b5
    .hword 0x4657    @ 0801e102 5746
    .hword 0x464e    @ 0801e104 4e46
    .hword 0x4645    @ 0801e106 4546
    push {r5,r6,r7}                          @ 0801e108 e0b4
    lsls r0,r0,#0x10    @ 0801e10a 0004
    lsrs r0,r0,#0x10    @ 0801e10c 000c
    ldr r3, PTR_card_stats_table_0801e18c    @ 0801e10e 1f4b
    movs r1,#0xb    @ 0801e110 0b21
    adds r2,r0,#0x0    @ 0801e112 021c
    muls r2,r1    @ 0801e114 4a43
    adds r1,r2,#0x7    @ 0801e116 d11d
    lsls r1,r1,#0x1    @ 0801e118 4900
    adds r1,r1,r3    @ 0801e11a c918
    ldrh r4,[r1,#0x0]                        @ 0801e11c 0c88
    adds r1,r2,#0x6    @ 0801e11e 911d
    lsls r1,r1,#0x1    @ 0801e120 4900
    adds r7,r1,r3    @ 0801e122 cf18
    ldrh r5,[r7,#0x0]                        @ 0801e124 3d88
    adds r2,#0x9    @ 0801e126 0932
    lsls r2,r2,#0x1    @ 0801e128 5200
    adds r2,r2,r3    @ 0801e12a d218
    ldrh r6,[r2,#0x0]                        @ 0801e12c 1688
    movs r1,#0x16    @ 0801e12e 1621
    muls r0,r1    @ 0801e130 4843
    adds r0,r0,r3    @ 0801e132 c018
    ldrh r0,[r0,#0x0]                        @ 0801e134 0088
    .hword 0x4681    @ 0801e136 8146
    ldr r0, DAT_0801e190                     @ 0801e138 1548
    .hword 0x4680    @ 0801e13a 8046
    movs r0,#0x3d    @ 0801e13c 3d20
    rsbs r0,r0,#0    @ 0801e13e 4042
    .hword 0x4641    @ 0801e140 4146
    ldrb r1,[r1,#0x2]                        @ 0801e142 8978
    ands r0,r1    @ 0801e144 0840
    movs r1,#0x3    @ 0801e146 0321
    rsbs r1,r1,#0    @ 0801e148 4942
    ands r0,r1    @ 0801e14a 0840
    .hword 0x4642    @ 0801e14c 4246
    strb r0,[r2,#0x2]                        @ 0801e14e 9070
    cmp r4,#0x0                              @ 0801e150 002c
    bgt LAB_0801e156                         @ 0801e152 00dc
    b LAB_0801e262                           @ 0801e154 85e0
LAB_0801e156:
    ldrh r1,[r7,#0x0]                        @ 0801e156 3988
    cmp r1,#0x17                             @ 0801e158 1729
    bgt LAB_0801e1a4                         @ 0801e15a 23dc
    cmp r1,#0x16                             @ 0801e15c 1629
    blt LAB_0801e1a4                         @ 0801e15e 21db
    cmp r6,#0x0                              @ 0801e160 002e
    ble LAB_0801e1d0                         @ 0801e162 35dd
    subs r6,#0x1    @ 0801e164 013e
    ldr r0, DAT_0801e194                     @ 0801e166 0b48
    ldr r1, DAT_0801e198                     @ 0801e168 0b49
    movs r2,#0x20    @ 0801e16a 2022
    bl copy_bytes_by_halfword                @ 0801e16c d6f09afe
    ldr r0, DAT_0801e19c                     @ 0801e170 0a48
    lsls r1,r6,#0x7    @ 0801e172 f101
    ldr r2, DAT_0801e1a0                     @ 0801e174 0a4a
    adds r1,r1,r2    @ 0801e176 8918
    movs r2,#0x80    @ 0801e178 8022
    bl copy_bytes_by_halfword                @ 0801e17a d6f093fe
    movs r0,#0x2    @ 0801e17e 0220
    .hword 0x4643    @ 0801e180 4346
    ldrb r3,[r3,#0x2]                        @ 0801e182 9b78
    orrs r0,r3    @ 0801e184 1843
    .hword 0x4646    @ 0801e186 4646
    strb r0,[r6,#0x2]                        @ 0801e188 b070
    b LAB_0801e1d0                           @ 0801e18a 21e0
PTR_card_stats_table_0801e18c:
    .word  card_stats_table               @ 0801e18c b8698109
DAT_0801e190:
    .word  0x0201afb0                     @ 0801e190 b0af0102
DAT_0801e194:
    .word  0x05000380                     @ 0801e194 80030005
DAT_0801e198:
    .word  0x0984f3ac                     @ 0801e198 acf38409
DAT_0801e19c:
    .word  0x06017500                     @ 0801e19c 00750106
DAT_0801e1a0:
    .word  0x0984f0ac                     @ 0801e1a0 acf08409
LAB_0801e1a4:
    cmp r5,#0x0                              @ 0801e1a4 002d
    ble LAB_0801e1d0                         @ 0801e1a6 13dd
    subs r5,#0x1    @ 0801e1a8 013d
    ldr r0, DAT_0801e270                     @ 0801e1aa 3148
    lsls r1,r5,#0x5    @ 0801e1ac 6901
    ldr r2, DAT_0801e274                     @ 0801e1ae 314a
    adds r1,r1,r2    @ 0801e1b0 8918
    movs r2,#0x20    @ 0801e1b2 2022
    bl copy_bytes_by_halfword                @ 0801e1b4 d6f076fe
    ldr r0, DAT_0801e278                     @ 0801e1b8 2f48
    lsls r1,r5,#0x7    @ 0801e1ba e901
    ldr r2, DAT_0801e27c                     @ 0801e1bc 2f4a
    adds r1,r1,r2    @ 0801e1be 8918
    movs r2,#0x80    @ 0801e1c0 8022
    bl copy_bytes_by_halfword                @ 0801e1c2 d6f06ffe
    ldr r1, DAT_0801e280                     @ 0801e1c6 2e49
    movs r0,#0x2    @ 0801e1c8 0220
    ldrb r2,[r1,#0x2]                        @ 0801e1ca 8a78
    orrs r0,r2    @ 0801e1cc 1043
    strb r0,[r1,#0x2]                        @ 0801e1ce 8870
LAB_0801e1d0:
    movs r5,#0x0    @ 0801e1d0 0025
    .hword 0x464b    @ 0801e1d2 4b46
    lsls r3,r3,#0x10    @ 0801e1d4 1b04
    .hword 0x469a    @ 0801e1d6 9a46
    ldr r6, DAT_0801e284                     @ 0801e1d8 2a4e
    .hword 0x46b1    @ 0801e1da b146
    ldr r0, DAT_0801e280                     @ 0801e1dc 2848
    .hword 0x4680    @ 0801e1de 8046
LAB_0801e1e0:
    lsls r4,r5,#0x2    @ 0801e1e0 ac00
    .hword 0x4649    @ 0801e1e2 4946
    adds r0,r4,r1    @ 0801e1e4 6018
    ldr r6,[r0,#0x0]                         @ 0801e1e6 0668
    .hword 0x4652    @ 0801e1e8 5246
    lsrs r0,r2,#0x10    @ 0801e1ea 100c
    adds r1,r6,#0x0    @ 0801e1ec 311c
    bl test_card_flag_bit                    @ 0801e1ee d1f065f9
    adds r7,r5,#0x1    @ 0801e1f2 6f1c
    cmp r0,#0x0                              @ 0801e1f4 0028
    beq LAB_0801e25c                         @ 0801e1f6 31d0
    movs r3,#0x1    @ 0801e1f8 0123
    rsbs r3,r3,#0    @ 0801e1fa 5b42
    movs r2,#0x0    @ 0801e1fc 0022
    ldr r0, DAT_0801e288                     @ 0801e1fe 2248
    ldrh r1,[r0,#0x0]                        @ 0801e200 0188
    adds r5,r0,#0x0    @ 0801e202 051c
    cmp r1,r6                                @ 0801e204 b142
    beq LAB_0801e25c                         @ 0801e206 29d0
LAB_0801e208:
    adds r2,#0x1    @ 0801e208 0132
    cmp r2,#0x20                             @ 0801e20a 202a
    bhi LAB_0801e220                         @ 0801e20c 08d8
    lsls r0,r2,#0x1    @ 0801e20e 5000
    adds r0,r0,r5    @ 0801e210 4019
    .hword 0x464e    @ 0801e212 4e46
    adds r1,r4,r6    @ 0801e214 a119
    ldrh r0,[r0,#0x0]                        @ 0801e216 0088
    ldrh r1,[r1,#0x0]                        @ 0801e218 0988
    cmp r0,r1                                @ 0801e21a 8842
    bne LAB_0801e208                         @ 0801e21c f4d1
    adds r3,r2,#0x0    @ 0801e21e 131c
LAB_0801e220:
    cmp r3,#0x0                              @ 0801e220 002b
    ble LAB_0801e25c                         @ 0801e222 1bdd
    .hword 0x4641    @ 0801e224 4146
    ldrb r1,[r1,#0x2]                        @ 0801e226 8978
    lsls r0,r1,#0x1a    @ 0801e228 8806
    lsrs r0,r0,#0x1c    @ 0801e22a 000f
    lsls r0,r0,#0x8    @ 0801e22c 0002
    ldr r2, DAT_0801e28c                     @ 0801e22e 174a
    adds r0,r0,r2    @ 0801e230 8018
    lsls r1,r3,#0x8    @ 0801e232 1902
    ldr r2, DAT_0801e290                     @ 0801e234 164a
    adds r1,r1,r2    @ 0801e236 8918
    movs r2,#0x80    @ 0801e238 8022
    lsls r2,r2,#0x1    @ 0801e23a 5200
    bl copy_bytes_by_halfword                @ 0801e23c d6f032fe
    .hword 0x4643    @ 0801e240 4346
    ldrb r2,[r3,#0x2]                        @ 0801e242 9a78
    lsls r0,r2,#0x1a    @ 0801e244 9006
    lsrs r0,r0,#0x1c    @ 0801e246 000f
    adds r0,#0x1    @ 0801e248 0130
    movs r1,#0xf    @ 0801e24a 0f21
    ands r0,r1    @ 0801e24c 0840
    lsls r0,r0,#0x2    @ 0801e24e 8000
    movs r6,#0x3d    @ 0801e250 3d26
    rsbs r6,r6,#0    @ 0801e252 7642
    adds r1,r6,#0x0    @ 0801e254 311c
    ands r2,r1    @ 0801e256 0a40
    orrs r2,r0    @ 0801e258 0243
    strb r2,[r3,#0x2]                        @ 0801e25a 9a70
LAB_0801e25c:
    adds r5,r7,#0x0    @ 0801e25c 3d1c
    cmp r5,#0x1f                             @ 0801e25e 1f2d
    ble LAB_0801e1e0                         @ 0801e260 bedd
LAB_0801e262:
    pop {r3,r4,r5}                           @ 0801e262 38bc
    .hword 0x4698    @ 0801e264 9846
    .hword 0x46a1    @ 0801e266 a146
    .hword 0x46aa    @ 0801e268 aa46
    pop {r4,r5,r6,r7}                        @ 0801e26a f0bc
    pop {r0}                                 @ 0801e26c 01bc
    bx r0                                    @ 0801e26e 0047
DAT_0801e270:
    .word  0x05000380                     @ 0801e270 80030005
DAT_0801e274:
    .word  0x0984ee2c                     @ 0801e274 2cee8409
DAT_0801e278:
    .word  0x06017500                     @ 0801e278 00750106
DAT_0801e27c:
    .word  0x0984e42c                     @ 0801e27c 2ce48409
DAT_0801e280:
    .word  0x0201afb0                     @ 0801e280 b0af0102
DAT_0801e284:
    .word  0x09e4f204                     @ 0801e284 04f2e409
DAT_0801e288:
    .word  0x09e58ac4                     @ 0801e288 c48ae509
DAT_0801e28c:
    .word  0x06017580                     @ 0801e28c 80750106
DAT_0801e290:
    .word  0x09e2ddb4                     @ 0801e290 b4dde209

@ Write a 2x2 tile glyph block into BG VRAM with palette and tile data copy.
@ Steps: (1) copy 32 bytes from PALRAM[palette_slot*32] to palette_dst;
@ (2) copy 128 bytes from OBJ VRAM char area 0x06004000[source_tile*32] to tile_data_dst;
@ (3) write 4 screen map entries at BG_SCREEN_BASE+screen_tile_offset*2 to form 2x2 glyph block
@     (entry = (palette_slot&0xF)<<12 | (source_tile+n); screen width=32 tiles, second row offset=+0x40).
@ Low-level BG font blitter integrating palette copy, tile copy, and tilemap write.
@ Constants: OBJ_CHAR_BASE=0x06004000; BG_SCREEN_BASE=0x06000000; BG_SCREEN_WIDTH=32; PALRAM_BASE=0x05000000; TILE_BYTES=32; PALETTE_ROW_BYTES=32.
blit_glyph_2x2_to_bg_vram:
    push {r4,r5,r6,lr}                       @ 0801e294 70b5
    .hword 0x464e    @ 0801e296 4e46
    .hword 0x4645    @ 0801e298 4546
    push {r5,r6}                             @ 0801e29a 60b4
    adds r5,r0,#0x0    @ 0801e29c 051c
    adds r4,r1,#0x0    @ 0801e29e 0c1c
    adds r0,r2,#0x0    @ 0801e2a0 101c
    .hword 0x4699    @ 0801e2a2 9946
    ldr r1,[sp,#0x18]                        @ 0801e2a4 0699
    lsls r5,r5,#0x10    @ 0801e2a6 2d04
    lsrs r5,r5,#0x10    @ 0801e2a8 2d0c
    lsls r4,r4,#0x10    @ 0801e2aa 2404
    lsrs r4,r4,#0x10    @ 0801e2ac 240c
    lsls r0,r0,#0x10    @ 0801e2ae 0004
    lsrs r0,r0,#0x10    @ 0801e2b0 000c
    movs r2,#0xc0    @ 0801e2b2 c022
    lsls r2,r2,#0x13    @ 0801e2b4 d204
    .hword 0x4690    @ 0801e2b6 9046
    lsls r6,r0,#0x1c    @ 0801e2b8 0607
    lsrs r6,r6,#0x10    @ 0801e2ba 360c
    lsls r0,r0,#0x5    @ 0801e2bc 4001
    movs r2,#0xa0    @ 0801e2be a022
    lsls r2,r2,#0x13    @ 0801e2c0 d204
    adds r0,r0,r2    @ 0801e2c2 8018
    movs r2,#0x20    @ 0801e2c4 2022
    bl copy_bytes_by_halfword                @ 0801e2c6 d6f0edfd
    lsls r0,r4,#0x5    @ 0801e2ca 6001
    ldr r3, DAT_0801e318                     @ 0801e2cc 124b
    adds r0,r0,r3    @ 0801e2ce c018
    .hword 0x4649    @ 0801e2d0 4946
    movs r2,#0x80    @ 0801e2d2 8022
    bl copy_bytes_by_halfword                @ 0801e2d4 d6f0e6fd
    lsls r5,r5,#0x1    @ 0801e2d8 6d00
    add r8,r5                                @ 0801e2da a844
    adds r1,r4,#0x1    @ 0801e2dc 611c
    lsls r1,r1,#0x10    @ 0801e2de 0904
    adds r4,r6,r4    @ 0801e2e0 3419
    .hword 0x4640    @ 0801e2e2 4046
    strh r4,[r0,#0x0]                        @ 0801e2e4 0480
    ldr r3, DAT_0801e31c                     @ 0801e2e6 0d4b
    adds r2,r5,r3    @ 0801e2e8 ea18
    lsrs r0,r1,#0x10    @ 0801e2ea 080c
    movs r3,#0x80    @ 0801e2ec 8023
    lsls r3,r3,#0x9    @ 0801e2ee 5b02
    adds r1,r1,r3    @ 0801e2f0 c918
    adds r0,r6,r0    @ 0801e2f2 3018
    strh r0,[r2,#0x0]                        @ 0801e2f4 1080
    ldr r0, DAT_0801e320                     @ 0801e2f6 0a48
    adds r2,r5,r0    @ 0801e2f8 2a18
    lsrs r0,r1,#0x10    @ 0801e2fa 080c
    adds r1,r1,r3    @ 0801e2fc c918
    lsrs r1,r1,#0x10    @ 0801e2fe 090c
    adds r0,r6,r0    @ 0801e300 3018
    strh r0,[r2,#0x0]                        @ 0801e302 1080
    ldr r2, DAT_0801e324                     @ 0801e304 074a
    adds r5,r5,r2    @ 0801e306 ad18
    adds r6,r6,r1    @ 0801e308 7618
    strh r6,[r5,#0x0]                        @ 0801e30a 2e80
    pop {r3,r4}                              @ 0801e30c 18bc
    .hword 0x4698    @ 0801e30e 9846
    .hword 0x46a1    @ 0801e310 a146
    pop {r4,r5,r6}                           @ 0801e312 70bc
    pop {r0}                                 @ 0801e314 01bc
    bx r0                                    @ 0801e316 0047
DAT_0801e318:
    .word  0x06004000                     @ 0801e318 00400006
DAT_0801e31c:
    .word  0x06000002                     @ 0801e31c 02000006
DAT_0801e320:
    .word  0x06000040                     @ 0801e320 40000006
DAT_0801e324:
    .word  0x06000042                     @ 0801e324 42000006

@ 被 FUN_0801e714 (card_info 场景主循环) 唯一调用. 先向 DISPCNT (0x04000000) 写入 0x1f00|当前值 (置位 bits[12:8] = BG0-BG3+OBJ 显示使能位), 然后以 delta=4 调用 tick_blend_step_by_delta 递减 blend_step. 实质是卡片信息场景每帧的混合淡出+显示模式锁定组合. 返回 tick_blend_step_by_delta 的返回值 (1=淡出完成, 0=进行中).
tick_blend_fadeout_and_set_dispcnt:
    push {lr}                                @ 0801e328 00b5
    movs r2,#0x80    @ 0801e32a 8022
    lsls r2,r2,#0x13    @ 0801e32c d204
    ldrh r0,[r2,#0x0]                        @ 0801e32e 1088
    movs r3,#0xf8    @ 0801e330 f823
    lsls r3,r3,#0x5    @ 0801e332 5b01
    adds r1,r3,#0x0    @ 0801e334 191c
    orrs r0,r1    @ 0801e336 0843
    strh r0,[r2,#0x0]                        @ 0801e338 1080
    movs r0,#0x4    @ 0801e33a 0420
    bl tick_blend_step_by_delta              @ 0801e33c d7f0bcfa
    pop {r1}                                 @ 0801e340 02bc
    bx r1                                    @ 0801e342 0847

@ 被 FUN_0801e714 (card_info 场景) 和 FUN_080fa3a8 调用. 以 target_step=4 调用 start_blend_fadein_with_target 递增 blend_step; 若返回 0 (仍在过渡) 则将返回值继续传递为 0; 若返回 1 (混合完成) 则读 DISPCNT (0x04000000), 与 DISPCNT_PRESERVE_MASK=0xe0ff 做 AND (保留 bits[7:0]+bits[15:13], 清除 bits[12:8] = BG0-BG3+OBJ 使能位), 写回 DISPCNT 关闭高位显示标志, 并返回 1. 实质是 blend fade-in 的每帧驱动函数, 完成时自动清理 DISPCNT.
tick_blend_fadein_and_poll_done:
    push {lr}                                @ 0801e344 00b5
    movs r0,#0x4    @ 0801e346 0420
    bl start_blend_fadein_with_target        @ 0801e348 d7f07afa
    cmp r0,#0x0                              @ 0801e34c 0028
    bne LAB_0801e354                         @ 0801e34e 01d1
    movs r0,#0x0    @ 0801e350 0020
    b LAB_0801e362                           @ 0801e352 06e0
LAB_0801e354:
    movs r2,#0x80    @ 0801e354 8022
    lsls r2,r2,#0x13    @ 0801e356 d204
    ldrh r1,[r2,#0x0]                        @ 0801e358 1188
    ldr r0, DAT_0801e368                     @ 0801e35a 0348
    ands r0,r1    @ 0801e35c 0840
    strh r0,[r2,#0x0]                        @ 0801e35e 1080
    movs r0,#0x1    @ 0801e360 0120
LAB_0801e362:
    pop {r1}                                 @ 0801e362 02bc
    bx r1                                    @ 0801e364 0847
    .zero  0x2
DAT_0801e368:
    .word  0x0000e0ff                     @ 0801e368 ffe00000

@ card_info 场景的每帧状态更新函数, 被 FUN_0801e714 (card_info 场景主循环) 唯一调用. 共执行四步逻辑: (1) 读 IWRAM gPrng+0x148 (0x03000188) bits[1:0], 若非零则调用 sync_state_and_init_sprite(1) 触发 sprite 初始化; (2) 读 [0x0201afb0+0x6] 倒计时字段, 若非零则递减并在归零时返回 1; (3) 根据 gPrng+0x146 的显示标志 bit7/bit6 调整 [struct+0x20] 的滚动偏移值; (4) 若 gPrng+0x148 bit2 设置且 [0x02006c2c] bits[2:0]==0, 则翻转 [struct+0x0] bit0 并调用 card_info_page_step_03_unknown. 最终返回 0 (继续更新) 或 1 (触发场景切换).
update_card_info_page_state:
    push {lr}                                @ 0801e36c 00b5
    ldr r2, PTR_gPrng_0801e38c               @ 0801e36e 074a
    movs r0,#0xa4    @ 0801e370 a420
    lsls r0,r0,#0x1    @ 0801e372 4000
    adds r1,r2,r0    @ 0801e374 1118
    movs r0,#0x3    @ 0801e376 0320
    ldrh r1,[r1,#0x0]                        @ 0801e378 0988
    ands r0,r1    @ 0801e37a 0840
    .hword 0x4694    @ 0801e37c 9446
    cmp r0,#0x0                              @ 0801e37e 0028
    beq LAB_0801e390                         @ 0801e380 06d0
    movs r0,#0x1    @ 0801e382 0120
    bl sync_state_and_init_sprite            @ 0801e384 dbf096fb
    movs r0,#0x1    @ 0801e388 0120
    b LAB_0801e434                           @ 0801e38a 53e0
PTR_gPrng_0801e38c:
    .word  gPrng                          @ 0801e38c 40000003
LAB_0801e390:
    ldr r0, DAT_0801e3a8                     @ 0801e390 0548
    ldrh r1,[r0,#0x6]                        @ 0801e392 c188
    adds r3,r0,#0x0    @ 0801e394 031c
    cmp r1,#0x0                              @ 0801e396 0029
    beq LAB_0801e3ac                         @ 0801e398 08d0
    subs r0,r1,#0x1    @ 0801e39a 481e
    strh r0,[r3,#0x6]                        @ 0801e39c d880
    lsls r0,r0,#0x10    @ 0801e39e 0004
    cmp r0,#0x0                              @ 0801e3a0 0028
    bne LAB_0801e3ac                         @ 0801e3a2 03d1
    movs r0,#0x1    @ 0801e3a4 0120
    b LAB_0801e434                           @ 0801e3a6 45e0
DAT_0801e3a8:
    .word  0x0201afb0                     @ 0801e3a8 b0af0102
LAB_0801e3ac:
    movs r1,#0xa3    @ 0801e3ac a321
    lsls r1,r1,#0x1    @ 0801e3ae 4900
    add r1,r12                               @ 0801e3b0 6144
    movs r0,#0x80    @ 0801e3b2 8020
    ldrh r1,[r1,#0x0]                        @ 0801e3b4 0988
    ands r0,r1    @ 0801e3b6 0840
    cmp r0,#0x0                              @ 0801e3b8 0028
    beq LAB_0801e3d8                         @ 0801e3ba 0dd0
    ldr r1,[r3,#0x20]                        @ 0801e3bc 196a
    adds r0,r1,#0x0    @ 0801e3be 081c
    adds r0,#0x84    @ 0801e3c0 8430
    ldr r2,[r3,#0x24]                        @ 0801e3c2 5a6a
    cmp r0,r2                                @ 0801e3c4 9042
    bge LAB_0801e3cc                         @ 0801e3c6 01da
    adds r0,r1,#0x4    @ 0801e3c8 081d
    b LAB_0801e3d6                           @ 0801e3ca 04e0
LAB_0801e3cc:
    adds r0,r1,#0x0    @ 0801e3cc 081c
    adds r0,#0x80    @ 0801e3ce 8030
    cmp r0,r2                                @ 0801e3d0 9042
    bge LAB_0801e3d8                         @ 0801e3d2 01da
    adds r0,r1,#0x1    @ 0801e3d4 481c
LAB_0801e3d6:
    str r0,[r3,#0x20]                        @ 0801e3d6 1862
LAB_0801e3d8:
    movs r1,#0xa3    @ 0801e3d8 a321
    lsls r1,r1,#0x1    @ 0801e3da 4900
    add r1,r12                               @ 0801e3dc 6144
    movs r0,#0x40    @ 0801e3de 4020
    ldrh r1,[r1,#0x0]                        @ 0801e3e0 0988
    ands r0,r1    @ 0801e3e2 0840
    cmp r0,#0x0                              @ 0801e3e4 0028
    beq LAB_0801e3fa                         @ 0801e3e6 08d0
    ldr r0,[r3,#0x20]                        @ 0801e3e8 186a
    cmp r0,#0x4                              @ 0801e3ea 0428
    ble LAB_0801e3f2                         @ 0801e3ec 01dd
    subs r0,#0x4    @ 0801e3ee 0438
    b LAB_0801e3f8                           @ 0801e3f0 02e0
LAB_0801e3f2:
    cmp r0,#0x0                              @ 0801e3f2 0028
    ble LAB_0801e3fa                         @ 0801e3f4 01dd
    subs r0,#0x1    @ 0801e3f6 0138
LAB_0801e3f8:
    str r0,[r3,#0x20]                        @ 0801e3f8 1862
LAB_0801e3fa:
    movs r1,#0xa4    @ 0801e3fa a421
    lsls r1,r1,#0x1    @ 0801e3fc 4900
    add r1,r12                               @ 0801e3fe 6144
    movs r0,#0x4    @ 0801e400 0420
    ldrh r1,[r1,#0x0]                        @ 0801e402 0988
    ands r0,r1    @ 0801e404 0840
    cmp r0,#0x0                              @ 0801e406 0028
    beq LAB_0801e432                         @ 0801e408 13d0
    ldr r1, DAT_0801e438                     @ 0801e40a 0b49
    ldr r0, DAT_0801e43c                     @ 0801e40c 0b48
    adds r1,r1,r0    @ 0801e40e 0918
    movs r0,#0x7    @ 0801e410 0720
    ldrb r1,[r1,#0x0]                        @ 0801e412 0978
    ands r0,r1    @ 0801e414 0840
    cmp r0,#0x0                              @ 0801e416 0028
    bne LAB_0801e432                         @ 0801e418 0bd1
    ldrb r2,[r3,#0x0]                        @ 0801e41a 1a78
    lsls r0,r2,#0x1f    @ 0801e41c d007
    lsrs r0,r0,#0x1f    @ 0801e41e c00f
    movs r1,#0x1    @ 0801e420 0121
    bics r1,r0    @ 0801e422 8143
    movs r0,#0x2    @ 0801e424 0220
    rsbs r0,r0,#0    @ 0801e426 4042
    ands r0,r2    @ 0801e428 1040
    orrs r0,r1    @ 0801e42a 0843
    strb r0,[r3,#0x0]                        @ 0801e42c 1870
    bl card_info_page_step_03_unknown        @ 0801e42e fff7d5fb
LAB_0801e432:
    movs r0,#0x0    @ 0801e432 0020
LAB_0801e434:
    pop {r1}                                 @ 0801e434 02bc
    bx r1                                    @ 0801e436 0847
DAT_0801e438:
    .word  0x02000000                     @ 0801e438 00000002
DAT_0801e43c:
    .word  0x00006c2c                     @ 0801e43c 2c6c0000

@ p1/p2: 卡牌信息页顶层, card_id=(word0<<15)>>18
card_info_page_entry:
    push {r4,lr}                             @ 0801e440 10b5
    bl card_info_page_init_bg0               @ 0801e442 fff70bf8
    ldr r4, DAT_0801e484                     @ 0801e446 0f4c
    ldr r0,[r4,#0x0]                         @ 0801e448 2068
    lsls r0,r0,#0xf    @ 0801e44a c003
    lsrs r0,r0,#0x12    @ 0801e44c 800c
    ldrh r1,[r4,#0xc]                        @ 0801e44e a189
    ldrh r2,[r4,#0x10]                       @ 0801e450 228a
    bl card_image_decode_wrapper             @ 0801e452 fff7a1fa
    bl card_info_page_step_03_unknown        @ 0801e456 fff7c1fb
    ldr r0,[r4,#0x0]                         @ 0801e45a 2068
    lsls r0,r0,#0xf    @ 0801e45c c003
    lsrs r0,r0,#0x12    @ 0801e45e 800c
    ldr r1, DAT_0801e488                     @ 0801e460 0949
    ldr r2, DAT_0801e48c                     @ 0801e462 0a4a
    adds r1,r1,r2    @ 0801e464 8918
    ldrb r1,[r1,#0x0]                        @ 0801e466 0978
    lsls r1,r1,#0x1d    @ 0801e468 4907
    lsrs r1,r1,#0x1d    @ 0801e46a 490f
    bl card_data_query                       @ 0801e46c d0f072fb
    bl render_card_description_text          @ 0801e470 fff7c6fd
    ldr r0,[r4,#0x0]                         @ 0801e474 2068
    lsls r0,r0,#0xf    @ 0801e476 c003
    lsrs r0,r0,#0x12    @ 0801e478 800c
    bl card_info_page_finalize               @ 0801e47a fff741fe
    pop {r4}                                 @ 0801e47e 10bc
    pop {r0}                                 @ 0801e480 01bc
    bx r0                                    @ 0801e482 0047
DAT_0801e484:
    .word  0x0201afb0                     @ 0801e484 b0af0102
DAT_0801e488:
    .word  0x02000000                     @ 0801e488 00000002
DAT_0801e48c:
    .word  0x00006c2c                     @ 0801e48c 2c6c0000

@ Called by render_card_stats_oam_for_current_card (FUN_0801e620). Reads card_id (r0 low16), looks up card_stats_table row (stride=11 halfwords), reads ATK (offset+6)/DEF (offset+5)/type (offset+9), then calls write_oam_entry_from_packed_args to write digit sprites to OAM buffer. Skips render if ATK not in 1..20 range (Spell/Trap have no ATK). For type 22 (Quick-Play Trap) with field[9]!=0, renders a second digit group.
draw_card_stat_digits_to_oam:
    push {r4,r5,r6,r7,lr}                    @ 0801e490 f0b5
    lsls r0,r0,#0x10    @ 0801e492 0004
    lsrs r0,r0,#0x10    @ 0801e494 000c
    ldr r2, PTR_card_stats_table_0801e4e0    @ 0801e496 124a
    movs r1,#0xb    @ 0801e498 0b21
    muls r1,r0    @ 0801e49a 4143
    adds r0,r1,#0x6    @ 0801e49c 881d
    lsls r0,r0,#0x1    @ 0801e49e 4000
    adds r0,r0,r2    @ 0801e4a0 8018
    ldrh r4,[r0,#0x0]                        @ 0801e4a2 0488
    adds r0,r1,#0x5    @ 0801e4a4 481d
    lsls r0,r0,#0x1    @ 0801e4a6 4000
    adds r0,r0,r2    @ 0801e4a8 8018
    ldrh r5,[r0,#0x0]                        @ 0801e4aa 0588
    adds r1,#0x9    @ 0801e4ac 0931
    lsls r1,r1,#0x1    @ 0801e4ae 4900
    adds r1,r1,r2    @ 0801e4b0 8918
    ldrh r6,[r1,#0x0]                        @ 0801e4b2 0e88
    ldr r0, DAT_0801e4e4                     @ 0801e4b4 0b48
    ldr r2, DAT_0801e4e8                     @ 0801e4b6 0c4a
    movs r1,#0x40    @ 0801e4b8 4021
    bl write_oam_entry_from_packed_args      @ 0801e4ba d7f057fe
    cmp r4,#0x1                              @ 0801e4be 012c
    blt LAB_0801e538                         @ 0801e4c0 3adb
    cmp r4,#0x14                             @ 0801e4c2 142c
    ble LAB_0801e4f4                         @ 0801e4c4 16dd
    cmp r4,#0x17                             @ 0801e4c6 172c
    bgt LAB_0801e538                         @ 0801e4c8 36dc
    cmp r4,#0x16                             @ 0801e4ca 162c
    blt LAB_0801e538                         @ 0801e4cc 34db
    cmp r6,#0x0                              @ 0801e4ce 002e
    beq LAB_0801e538                         @ 0801e4d0 32d0
    ldr r0, DAT_0801e4ec                     @ 0801e4d2 0648
    ldr r2, DAT_0801e4f0                     @ 0801e4d4 064a
    movs r1,#0x0    @ 0801e4d6 0021
    bl write_oam_entry_from_packed_args      @ 0801e4d8 d7f048fe
    b LAB_0801e538                           @ 0801e4dc 2ce0
    .zero  0x2
PTR_card_stats_table_0801e4e0:
    .word  card_stats_table               @ 0801e4e0 b8698109
DAT_0801e4e4:
    .word  0x00060056                     @ 0801e4e4 56000600
DAT_0801e4e8:
    .word  0x0000d3a2                     @ 0801e4e8 a2d30000
DAT_0801e4ec:
    .word  0x00150058                     @ 0801e4ec 58001500
DAT_0801e4f0:
    .word  0x0000e3a6                     @ 0801e4f0 a6e30000
LAB_0801e4f4:
    movs r4,#0x0    @ 0801e4f4 0024
    cmp r4,r5                                @ 0801e4f6 ac42
    bge LAB_0801e538                         @ 0801e4f8 1eda
    movs r7,#0xb0    @ 0801e4fa b027
    lsls r7,r7,#0xd    @ 0801e4fc 7f03
    movs r6,#0x0    @ 0801e4fe 0026
LAB_0801e500:
    cmp r5,#0x9                              @ 0801e500 092d
    bhi LAB_0801e51c                         @ 0801e502 0bd8
    lsls r1,r4,#0x3    @ 0801e504 e100
    movs r0,#0x5c    @ 0801e506 5c20
    subs r0,r0,r1    @ 0801e508 401a
    orrs r0,r7    @ 0801e50a 3843
    movs r1,#0x0    @ 0801e50c 0021
    ldr r2, DAT_0801e518                     @ 0801e50e 024a
    bl write_oam_entry_from_packed_args      @ 0801e510 d7f02cfe
    b LAB_0801e530                           @ 0801e514 0ce0
    .zero  0x2
DAT_0801e518:
    .word  0x0000f001                     @ 0801e518 01f00000
LAB_0801e51c:
    adds r0,r6,#0x0    @ 0801e51c 301c
    adds r1,r5,#0x0    @ 0801e51e 291c
    bl __divsi3                              @ 0801e520 f0f070f8
    adds r0,#0x14    @ 0801e524 1430
    orrs r0,r7    @ 0801e526 3843
    movs r1,#0x0    @ 0801e528 0021
    ldr r2, DAT_0801e55c                     @ 0801e52a 0c4a
    bl write_oam_entry_from_packed_args      @ 0801e52c d7f01efe
LAB_0801e530:
    adds r6,#0x50    @ 0801e530 5036
    adds r4,#0x1    @ 0801e532 0134
    cmp r4,r5                                @ 0801e534 ac42
    blt LAB_0801e500                         @ 0801e536 e3db
LAB_0801e538:
    movs r5,#0x70    @ 0801e538 7025
    ldr r6, DAT_0801e560                     @ 0801e53a 094e
    movs r0,#0x2    @ 0801e53c 0220
    ldrb r1,[r6,#0x2]                        @ 0801e53e b178
    ands r0,r1    @ 0801e540 0840
    cmp r0,#0x0                              @ 0801e542 0028
    beq LAB_0801e552                         @ 0801e544 05d0
    ldr r2, DAT_0801e564                     @ 0801e546 074a
    movs r0,#0x70    @ 0801e548 7020
    movs r1,#0x40    @ 0801e54a 4021
    bl write_oam_entry_from_packed_args      @ 0801e54c d7f00efe
    movs r5,#0x80    @ 0801e550 8025
LAB_0801e552:
    movs r4,#0x0    @ 0801e552 0024
    ldrb r6,[r6,#0x2]                        @ 0801e554 b678
    lsls r0,r6,#0x1a    @ 0801e556 b006
    b LAB_0801e584                           @ 0801e558 14e0
    .zero  0x2
DAT_0801e55c:
    .word  0x0000f001                     @ 0801e55c 01f00000
DAT_0801e560:
    .word  0x0201afb0                     @ 0801e560 b0af0102
DAT_0801e564:
    .word  0x0000c3a8                     @ 0801e564 a8c30000
LAB_0801e568:
    lsls r2,r4,#0x12    @ 0801e568 a204
    movs r0,#0xeb    @ 0801e56a eb20
    lsls r0,r0,#0x11    @ 0801e56c 4004
    adds r2,r2,r0    @ 0801e56e 1218
    lsrs r2,r2,#0x10    @ 0801e570 120c
    adds r0,r5,#0x0    @ 0801e572 281c
    movs r1,#0x40    @ 0801e574 4021
    bl write_oam_entry_with_tile_inc         @ 0801e576 d7f06bff
    adds r5,#0x10    @ 0801e57a 1035
    adds r4,#0x1    @ 0801e57c 0134
    ldr r0, DAT_0801e590                     @ 0801e57e 0448
    ldrb r0,[r0,#0x2]                        @ 0801e580 8078
    lsls r0,r0,#0x1a    @ 0801e582 8006
LAB_0801e584:
    lsrs r0,r0,#0x1c    @ 0801e584 000f
    cmp r4,r0                                @ 0801e586 8442
    blt LAB_0801e568                         @ 0801e588 eedb
    pop {r4,r5,r6,r7}                        @ 0801e58a f0bc
    pop {r0}                                 @ 0801e58c 01bc
    bx r0                                    @ 0801e58e 0047
DAT_0801e590:
    .word  0x0201afb0                     @ 0801e590 b0af0102

@ Called by render_card_stats_oam_for_current_card (FUN_0801e620). r0=row_count (signed; negative values rounded up by +7 before >>3). Folds row_count by 8 to get column/row indices, then loops writing 4 sprite entries per row at Y positions 0x70/0x90/0xb0/0xd0 (32px steps) via write_oam_entry_from_packed_args. Loop terminates when r6 > 0x8f (GBA screen height-1=143).
draw_stat_row_sprites_to_oam:
    push {r4,r5,r6,r7,lr}                    @ 0801e594 f0b5
    adds r3,r0,#0x0    @ 0801e596 031c
    cmp r3,#0x0                              @ 0801e598 002b
    bge LAB_0801e59e                         @ 0801e59a 00da
    adds r0,r3,#0x7    @ 0801e59c d81d
LAB_0801e59e:
    asrs r2,r0,#0x3    @ 0801e59e c210
    lsls r0,r2,#0x3    @ 0801e5a0 d000
    subs r0,r3,r0    @ 0801e5a2 181a
    movs r1,#0x10    @ 0801e5a4 1021
    subs r6,r1,r0    @ 0801e5a6 0e1a
    lsls r5,r2,#0x4    @ 0801e5a8 1501
    adds r5,#0x2    @ 0801e5aa 0235
    cmp r6,#0x8f                             @ 0801e5ac 8f2e
    bgt LAB_0801e606                         @ 0801e5ae 2adc
    ldr r7, DAT_0801e60c                     @ 0801e5b0 164f
LAB_0801e5b2:
    lsls r4,r6,#0x10    @ 0801e5b2 3404
    movs r0,#0x70    @ 0801e5b4 7020
    orrs r0,r4    @ 0801e5b6 2043
    ldr r1, DAT_0801e610                     @ 0801e5b8 1549
    adds r2,r5,r1    @ 0801e5ba 6a18
    lsls r2,r2,#0x10    @ 0801e5bc 1204
    lsrs r2,r2,#0x10    @ 0801e5be 120c
    adds r1,r7,#0x0    @ 0801e5c0 391c
    bl write_oam_entry_from_packed_args      @ 0801e5c2 d7f0d3fd
    movs r0,#0x90    @ 0801e5c6 9020
    orrs r0,r4    @ 0801e5c8 2043
    ldr r1, DAT_0801e614                     @ 0801e5ca 1249
    adds r2,r5,r1    @ 0801e5cc 6a18
    lsls r2,r2,#0x10    @ 0801e5ce 1204
    lsrs r2,r2,#0x10    @ 0801e5d0 120c
    adds r1,r7,#0x0    @ 0801e5d2 391c
    bl write_oam_entry_from_packed_args      @ 0801e5d4 d7f0cafd
    movs r0,#0xb0    @ 0801e5d8 b020
    orrs r0,r4    @ 0801e5da 2043
    ldr r1, DAT_0801e618                     @ 0801e5dc 0e49
    adds r2,r5,r1    @ 0801e5de 6a18
    lsls r2,r2,#0x10    @ 0801e5e0 1204
    lsrs r2,r2,#0x10    @ 0801e5e2 120c
    adds r1,r7,#0x0    @ 0801e5e4 391c
    bl write_oam_entry_from_packed_args      @ 0801e5e6 d7f0c1fd
    movs r0,#0xd0    @ 0801e5ea d020
    orrs r4,r0    @ 0801e5ec 0443
    ldr r0, DAT_0801e61c                     @ 0801e5ee 0b48
    adds r2,r5,r0    @ 0801e5f0 2a18
    lsls r2,r2,#0x10    @ 0801e5f2 1204
    lsrs r2,r2,#0x10    @ 0801e5f4 120c
    adds r0,r4,#0x0    @ 0801e5f6 201c
    adds r1,r7,#0x0    @ 0801e5f8 391c
    bl write_oam_entry_from_packed_args      @ 0801e5fa d7f0b7fd
    adds r6,#0x8    @ 0801e5fe 0836
    adds r5,#0x10    @ 0801e600 1035
    cmp r6,#0x8f                             @ 0801e602 8f2e
    ble LAB_0801e5b2                         @ 0801e604 d5dd
LAB_0801e606:
    pop {r4,r5,r6,r7}                        @ 0801e606 f0bc
    pop {r0}                                 @ 0801e608 01bc
    bx r0                                    @ 0801e60a 0047
DAT_0801e60c:
    .word  0x00004040                     @ 0801e60c 40400000
DAT_0801e610:
    .word  0xfffff800                     @ 0801e610 00f8ffff
DAT_0801e614:
    .word  0xfffff804                     @ 0801e614 04f8ffff
DAT_0801e618:
    .word  0xfffff808                     @ 0801e618 08f8ffff
DAT_0801e61c:
    .word  0xfffff80c                     @ 0801e61c 0cf8ffff

@ Called every frame by tick_card_info_page_by_state (FUN_0801e714). Reads current card_id from global state struct 0x0201afb0 (+0x0 bits[17:2]) and row_count (+0x20), then calls draw_card_stat_digits_to_oam and draw_stat_row_sprites_to_oam to write all card stat sprites to OAM buffer.
render_card_stats_oam_for_current_card:
    push {r4,lr}                             @ 0801e620 10b5
    ldr r4, DAT_0801e63c                     @ 0801e622 064c
    ldr r0,[r4,#0x0]                         @ 0801e624 2068
    lsls r0,r0,#0xf    @ 0801e626 c003
    lsrs r0,r0,#0x12    @ 0801e628 800c
    bl draw_card_stat_digits_to_oam          @ 0801e62a fff731ff
    ldr r0,[r4,#0x20]                        @ 0801e62e 206a
    bl draw_stat_row_sprites_to_oam          @ 0801e630 fff7b0ff
    pop {r4}                                 @ 0801e634 10bc
    pop {r0}                                 @ 0801e636 01bc
    bx r0                                    @ 0801e638 0047
    .zero  0x2
DAT_0801e63c:
    .word  0x0201afb0                     @ 0801e63c b0af0102

@ TG.4-next: 卡列表按 A 进详情页的派发, 首 bl 即 card_info_page_enter_with_card_id
card_list_on_select_to_info_page:
    push {r4,r5,r6,r7,lr}                    @ 0801e640 f0b5
    .hword 0x464f    @ 0801e642 4f46
    .hword 0x4646    @ 0801e644 4646
    push {r6,r7}                             @ 0801e646 c0b4
    adds r4,r0,#0x0    @ 0801e648 041c
    .hword 0x4691    @ 0801e64a 9146
    .hword 0x4698    @ 0801e64c 9846
    lsls r4,r4,#0x10    @ 0801e64e 2404
    lsrs r4,r4,#0x10    @ 0801e650 240c
    lsls r1,r1,#0x10    @ 0801e652 0904
    lsrs r6,r1,#0x10    @ 0801e654 0e0c
    bl card_info_page_enter_with_card_id     @ 0801e656 fef7f7fe
    ldr r3, DAT_0801e6b8                     @ 0801e65a 174b
    ldr r1, DAT_0801e6bc                     @ 0801e65c 1749
    ands r1,r4    @ 0801e65e 2140
    lsls r1,r1,#0x3    @ 0801e660 c900
    ldr r0,[r3,#0x0]                         @ 0801e662 1868
    ldr r2, DAT_0801e6c0                     @ 0801e664 164a
    ands r0,r2    @ 0801e666 1040
    orrs r0,r1    @ 0801e668 0843
    str r0,[r3,#0x0]                         @ 0801e66a 1860
    ldr r5, PTR_card_stats_table_0801e6c4    @ 0801e66c 154d
    movs r0,#0xb    @ 0801e66e 0b20
    muls r4,r0    @ 0801e670 4443
    adds r0,r4,#0x3    @ 0801e672 e01c
    lsls r0,r0,#0x1    @ 0801e674 4000
    adds r0,r0,r5    @ 0801e676 4019
    ldr r2, DAT_0801e6c8                     @ 0801e678 134a
    movs r1,#0x0    @ 0801e67a 0021
    ldrh r7,[r0,#0x0]                        @ 0801e67c 0788
    cmp r7,r2                                @ 0801e67e 9742
    beq LAB_0801e684                         @ 0801e680 00d0
    ldrh r1,[r0,#0x0]                        @ 0801e682 0188
LAB_0801e684:
    str r1,[r3,#0xc]                         @ 0801e684 d960
    adds r0,r4,#0x4    @ 0801e686 201d
    lsls r0,r0,#0x1    @ 0801e688 4000
    adds r0,r0,r5    @ 0801e68a 4019
    movs r1,#0x0    @ 0801e68c 0021
    ldrh r4,[r0,#0x0]                        @ 0801e68e 0488
    cmp r4,r2                                @ 0801e690 9442
    beq LAB_0801e696                         @ 0801e692 00d0
    ldrh r1,[r0,#0x0]                        @ 0801e694 0188
LAB_0801e696:
    str r1,[r3,#0x10]                        @ 0801e696 1961
    strh r6,[r3,#0x6]                        @ 0801e698 de80
    .hword 0x464f    @ 0801e69a 4f46
    str r7,[r3,#0x28]                        @ 0801e69c 9f62
    .hword 0x4640    @ 0801e69e 4046
    str r0,[r3,#0x2c]                        @ 0801e6a0 d862
    movs r0,#0x3    @ 0801e6a2 0320
    rsbs r0,r0,#0    @ 0801e6a4 4042
    ldrb r1,[r3,#0x0]                        @ 0801e6a6 1978
    ands r0,r1    @ 0801e6a8 0840
    strb r0,[r3,#0x0]                        @ 0801e6aa 1870
    pop {r3,r4}                              @ 0801e6ac 18bc
    .hword 0x4698    @ 0801e6ae 9846
    .hword 0x46a1    @ 0801e6b0 a146
    pop {r4,r5,r6,r7}                        @ 0801e6b2 f0bc
    pop {r0}                                 @ 0801e6b4 01bc
    bx r0                                    @ 0801e6b6 0047
DAT_0801e6b8:
    .word  0x0201afb0                     @ 0801e6b8 b0af0102
DAT_0801e6bc:
    .word  0x00003fff                     @ 0801e6bc ff3f0000
DAT_0801e6c0:
    .word  0xfffe0007                     @ 0801e6c0 0700feff
PTR_card_stats_table_0801e6c4:
    .word  card_stats_table               @ 0801e6c4 b8698109
DAT_0801e6c8:
    .word  0x0000ffff                     @ 0801e6c8 ffff0000

@ Adapter: convert internal card ID (icid) to card ID (cid) then open card info page.
@ Called from function pointer table at ROM 0x082E9EE8 when player selects a card.
@ Zero-extends r0 (icid) and r1 (origin_page) to u16, calls internal_card_id_to_card_id to map icid->cid,
@ then passes cid + original r1/r2/r3 to card_list_on_select_to_info_page.
@ Sibling of open_card_info_page_from_list (0x0801e6f4) which accepts cid directly; this variant adds the icid->cid step.
@ Constants: FUNC_PTR_TABLE_REF=0x082E9EE8.
open_card_info_by_icid:
    push {r4,r5,r6,lr}                       @ 0801e6cc 70b5
    adds r4,r1,#0x0    @ 0801e6ce 0c1c
    adds r5,r2,#0x0    @ 0801e6d0 151c
    adds r6,r3,#0x0    @ 0801e6d2 1e1c
    lsls r0,r0,#0x10    @ 0801e6d4 0004
    lsrs r0,r0,#0x10    @ 0801e6d6 000c
    lsls r4,r4,#0x10    @ 0801e6d8 2404
    lsrs r4,r4,#0x10    @ 0801e6da 240c
    bl internal_card_id_to_card_id           @ 0801e6dc d0f046f8
    lsls r0,r0,#0x10    @ 0801e6e0 0004
    lsrs r0,r0,#0x10    @ 0801e6e2 000c
    adds r1,r4,#0x0    @ 0801e6e4 211c
    adds r2,r5,#0x0    @ 0801e6e6 2a1c
    adds r3,r6,#0x0    @ 0801e6e8 331c
    bl card_list_on_select_to_info_page      @ 0801e6ea fff7a9ff
    pop {r4,r5,r6}                           @ 0801e6ee 70bc
    pop {r0}                                 @ 0801e6f0 01bc
    bx r0                                    @ 0801e6f2 0047

@ Transition entry called by card_list scene dispatchers (FUN_080c64b8 state=0, FUN_080d2c60 state=0) when player selects a card in the list to view its info page. Zero-extends card_id (r0) and origin_page (r1=0) to u16, calls card_list_on_select_to_info_page; then sets [0x0201afb0+0x0] bit2 (0x4) to mark card_info_page_active_flag. r0=u16 card_id, r1=u16 origin_page, r2=ptr, r3=ptr. Returns void. Constants: 0x4=[0x0201afb0+0x0] bit2 = card_info_page_active_flag.
open_card_info_page_from_list:
    push {lr}                                @ 0801e6f4 00b5
    lsls r0,r0,#0x10    @ 0801e6f6 0004
    lsrs r0,r0,#0x10    @ 0801e6f8 000c
    lsls r1,r1,#0x10    @ 0801e6fa 0904
    lsrs r1,r1,#0x10    @ 0801e6fc 090c
    bl card_list_on_select_to_info_page      @ 0801e6fe fff79fff
    ldr r1, DAT_0801e710                     @ 0801e702 0349
    movs r0,#0x4    @ 0801e704 0420
    ldrb r2,[r1,#0x0]                        @ 0801e706 0a78
    orrs r0,r2    @ 0801e708 1043
    strb r0,[r1,#0x0]                        @ 0801e70a 0870
    pop {r0}                                 @ 0801e70c 01bc
    bx r0                                    @ 0801e70e 0047
DAT_0801e710:
    .word  0x0201afb0                     @ 0801e710 b0af0102

@ card_info page per-frame main loop. Reads state halfword from 0x0201afb0+0x4, dispatches 4 paths: 0=init (read VCOUNT, call card_info_page_entry), 1/2/3=each calls render_card_stats_oam_for_current_card + tick_scroll_frame_and_update_pos, then tick_blend_fadeout_and_set_dispcnt / update_card_info_page_state / tick_blend_fadein_and_poll_done respectively. Increments state each frame; returns 1 (page exit) when state overflows, restoring VCOUNT.
tick_card_info_page_by_state:
    push {r4,r5,lr}                          @ 0801e714 30b5
    movs r5,#0x0    @ 0801e716 0025
    ldr r1, DAT_0801e744                     @ 0801e718 0a49
    movs r0,#0x4    @ 0801e71a 0420
    ldrb r2,[r1,#0x0]                        @ 0801e71c 0a78
    ands r0,r2    @ 0801e71e 1040
    adds r4,r1,#0x0    @ 0801e720 0c1c
    cmp r0,#0x0                              @ 0801e722 0028
    beq LAB_0801e732                         @ 0801e724 05d0
    ldr r0, DAT_0801e748                     @ 0801e726 0848
    ldr r1, DAT_0801e74c                     @ 0801e728 0849
    adds r0,r0,r1    @ 0801e72a 4018
    ldrb r0,[r0,#0x0]                        @ 0801e72c 0078
    lsls r0,r0,#0x1c    @ 0801e72e 0007
    lsrs r5,r0,#0x1e    @ 0801e730 850f
LAB_0801e732:
    ldrh r0,[r4,#0x4]                        @ 0801e732 a088
    cmp r0,#0x1                              @ 0801e734 0128
    beq LAB_0801e768                         @ 0801e736 17d0
    cmp r0,#0x1                              @ 0801e738 0128
    bgt LAB_0801e750                         @ 0801e73a 09dc
    cmp r0,#0x0                              @ 0801e73c 0028
    beq LAB_0801e75a                         @ 0801e73e 0cd0
    b LAB_0801e7a6                           @ 0801e740 31e0
    .zero  0x2
DAT_0801e744:
    .word  0x0201afb0                     @ 0801e744 b0af0102
DAT_0801e748:
    .word  0x02023130                     @ 0801e748 30310202
DAT_0801e74c:
    .word  0x00000222                     @ 0801e74c 22020000
LAB_0801e750:
    cmp r0,#0x2                              @ 0801e750 0228
    beq LAB_0801e776                         @ 0801e752 10d0
    cmp r0,#0x3                              @ 0801e754 0328
    beq LAB_0801e78c                         @ 0801e756 19d0
    b LAB_0801e7a6                           @ 0801e758 25e0
LAB_0801e75a:
    movs r0,#0x80    @ 0801e75a 8020
    lsls r0,r0,#0x13    @ 0801e75c c004
    ldrh r0,[r0,#0x0]                        @ 0801e75e 0088
    strh r0,[r4,#0x8]                        @ 0801e760 2081
    bl card_info_page_entry                  @ 0801e762 fff76dfe
    b LAB_0801e79c                           @ 0801e766 19e0
LAB_0801e768:
    bl render_card_stats_oam_for_current_card @ 0801e768 fff75aff
    bl tick_scroll_frame_and_update_pos      @ 0801e76c fff718fc
    bl tick_blend_fadeout_and_set_dispcnt    @ 0801e770 fff7dafd
    b LAB_0801e798                           @ 0801e774 10e0
LAB_0801e776:
    bl render_card_stats_oam_for_current_card @ 0801e776 fff753ff
    bl tick_scroll_frame_and_update_pos      @ 0801e77a fff711fc
    bl update_card_info_page_state           @ 0801e77e fff7f5fd
    cmp r0,#0x0                              @ 0801e782 0028
    bne LAB_0801e79c                         @ 0801e784 0ad1
    cmp r5,#0x0                              @ 0801e786 002d
    beq LAB_0801e7a2                         @ 0801e788 0bd0
    b LAB_0801e79c                           @ 0801e78a 07e0
LAB_0801e78c:
    bl render_card_stats_oam_for_current_card @ 0801e78c fff748ff
    bl tick_scroll_frame_and_update_pos      @ 0801e790 fff706fc
    bl tick_blend_fadein_and_poll_done       @ 0801e794 fff7d6fd
LAB_0801e798:
    cmp r0,#0x0                              @ 0801e798 0028
    beq LAB_0801e7a2                         @ 0801e79a 02d0
LAB_0801e79c:
    ldrh r0,[r4,#0x4]                        @ 0801e79c a088
    adds r0,#0x1    @ 0801e79e 0130
    strh r0,[r4,#0x4]                        @ 0801e7a0 a080
LAB_0801e7a2:
    movs r0,#0x0    @ 0801e7a2 0020
    b LAB_0801e7b0                           @ 0801e7a4 04e0
LAB_0801e7a6:
    movs r1,#0x80    @ 0801e7a6 8021
    lsls r1,r1,#0x13    @ 0801e7a8 c904
    ldrh r0,[r4,#0x8]                        @ 0801e7aa 2089
    strh r0,[r1,#0x0]                        @ 0801e7ac 0880
    movs r0,#0x1    @ 0801e7ae 0120
LAB_0801e7b0:
    pop {r4,r5}                              @ 0801e7b0 30bc
    pop {r1}                                 @ 0801e7b2 02bc
    bx r1                                    @ 0801e7b4 0847
    .zero  0x2

@ No-arg leaf; returns constant 0x81 (card data format ID / FS entry type tag). Called by deck/banlist scene callers (card_ids/card_stats/fs tags) as a format version discriminator. Body: movs r0,#0x81; bx lr.
get_card_data_format_id:
    movs r0,#0x81    @ 0801e7b8 8120
    bx lr                                    @ 0801e7ba 7047

@ Word-indexed table lookup: computes r0*4 + DAT_0801e7c8 (0x09e58b08) and returns the 32-bit value at that address. Standard ROM table fetch primitive used by card_ids/fs callers.
lookup_card_entry_by_index:
    ldr r1, DAT_0801e7c8                     @ 0801e7bc 0249
    lsls r0,r0,#0x2    @ 0801e7be 8000
    adds r0,r0,r1    @ 0801e7c0 4018
    ldr r0,[r0,#0x0]                         @ 0801e7c2 0068
    bx lr                                    @ 0801e7c4 7047
    .zero  0x2
DAT_0801e7c8:
    .word  0x09e58b08                     @ 0801e7c8 088be509

@ Called by FUN_08103524 (card_ids/fs). r0=slot_index, r1=fs_file_id. Computes IWRAM struct offset: 0x0201e2b4 + slot*0x108 (slot*33*8). Calls fs_load(r1,0), then parses FS data header: reads +0x8 halfword as count1 -> [r4+0x0], copies count1 halfwords from +0xA -> [r4+0xC], reads next halfword as count2 -> [r4+0x8], copies count2 halfwords -> [r4+0xCA]. Fills deck card FS data block into IWRAM struct.
load_card_fs_entry_to_struct:
    push {r4,lr}                             @ 0801e7cc 10b5
    lsls r2,r0,#0x5    @ 0801e7ce 4201
    adds r2,r2,r0    @ 0801e7d0 1218
    lsls r2,r2,#0x3    @ 0801e7d2 d200
    ldr r0, DAT_0801e84c                     @ 0801e7d4 1d48
    adds r4,r2,r0    @ 0801e7d6 1418
    adds r0,r1,#0x0    @ 0801e7d8 081c
    movs r1,#0x0    @ 0801e7da 0021
    bl fs_load                               @ 0801e7dc f6f7e4fb
    adds r1,r0,#0x0    @ 0801e7e0 011c
    adds r1,#0x8    @ 0801e7e2 0831
    ldrh r0,[r1,#0x0]                        @ 0801e7e4 0888
    str r0,[r4,#0x0]                         @ 0801e7e6 2060
    adds r1,#0x2    @ 0801e7e8 0231
    movs r3,#0x0    @ 0801e7ea 0023
    cmp r3,r0                                @ 0801e7ec 8342
    bcs LAB_0801e804                         @ 0801e7ee 09d2
    adds r2,r4,#0x0    @ 0801e7f0 221c
    adds r2,#0xc    @ 0801e7f2 0c32
LAB_0801e7f4:
    ldrh r0,[r1,#0x0]                        @ 0801e7f4 0888
    strh r0,[r2,#0x0]                        @ 0801e7f6 1080
    adds r1,#0x2    @ 0801e7f8 0231
    adds r2,#0x2    @ 0801e7fa 0232
    adds r3,#0x1    @ 0801e7fc 0133
    ldr r0,[r4,#0x0]                         @ 0801e7fe 2068
    cmp r3,r0                                @ 0801e800 8342
    bcc LAB_0801e7f4                         @ 0801e802 f7d3
LAB_0801e804:
    ldrh r0,[r1,#0x0]                        @ 0801e804 0888
    str r0,[r4,#0x8]                         @ 0801e806 a060
    adds r1,#0x2    @ 0801e808 0231
    movs r3,#0x0    @ 0801e80a 0023
    cmp r3,r0                                @ 0801e80c 8342
    bcs LAB_0801e824                         @ 0801e80e 09d2
    adds r2,r4,#0x0    @ 0801e810 221c
    adds r2,#0xca    @ 0801e812 ca32
LAB_0801e814:
    ldrh r0,[r1,#0x0]                        @ 0801e814 0888
    strh r0,[r2,#0x0]                        @ 0801e816 1080
    adds r1,#0x2    @ 0801e818 0231
    adds r2,#0x2    @ 0801e81a 0232
    adds r3,#0x1    @ 0801e81c 0133
    ldr r0,[r4,#0x8]                         @ 0801e81e a068
    cmp r3,r0                                @ 0801e820 8342
    bcc LAB_0801e814                         @ 0801e822 f7d3
LAB_0801e824:
    ldrh r0,[r1,#0x0]                        @ 0801e824 0888
    str r0,[r4,#0x4]                         @ 0801e826 6060
    adds r1,#0x2    @ 0801e828 0231
    movs r3,#0x0    @ 0801e82a 0023
    cmp r3,r0                                @ 0801e82c 8342
    bcs LAB_0801e844                         @ 0801e82e 09d2
    adds r2,r4,#0x0    @ 0801e830 221c
    adds r2,#0xac    @ 0801e832 ac32
LAB_0801e834:
    ldrh r0,[r1,#0x0]                        @ 0801e834 0888
    strh r0,[r2,#0x0]                        @ 0801e836 1080
    adds r1,#0x2    @ 0801e838 0231
    adds r2,#0x2    @ 0801e83a 0232
    adds r3,#0x1    @ 0801e83c 0133
    ldr r0,[r4,#0x4]                         @ 0801e83e 6068
    cmp r3,r0                                @ 0801e840 8342
    bcc LAB_0801e834                         @ 0801e842 f7d3
LAB_0801e844:
    pop {r4}                                 @ 0801e844 10bc
    pop {r0}                                 @ 0801e846 01bc
    bx r0                                    @ 0801e848 0047
    .zero  0x2
DAT_0801e84c:
    .word  0x0201e2b4                     @ 0801e84c b4e20102

@ Reads card FS data block (base 0x0201e2b4, stride=0x108, indexed by r0=slot_index) and fills up to three sub-arrays of display entries (halfword) into the target buffer at r1. Sub-array counts stored at [r1+0x18], [r1+0x19], [r1+0x1a]; entries sourced from card_stats_table and mapping table at 0x0201ff60. Callers: fill_card_fs_display_entries_for_card_list (fixed r1=0x02001138), FUN_0802752c, FUN_0802803c. Clears three word fields at r1 before filling (init write cursors). No return value (void). r0=u8 slot_index [0..1], r1=ptr display_buffer. Constants: 0x108=card FS data block stride (slot*0x108=slot*33*8).
fill_card_fs_display_entries:
    push {r4,r5,r6,r7,lr}                    @ 0801e850 f0b5
    .hword 0x4657    @ 0801e852 5746
    .hword 0x464e    @ 0801e854 4e46
    .hword 0x4645    @ 0801e856 4546
    push {r5,r6,r7}                          @ 0801e858 e0b4
    sub sp,#0x8                              @ 0801e85a 82b0
    str r0,[sp,#0x0]                         @ 0801e85c 0090
    adds r6,r1,#0x0    @ 0801e85e 0e1c
    movs r0,#0x1    @ 0801e860 0120
    .hword 0x4681    @ 0801e862 8146
    ldr r1,[sp,#0x0]                         @ 0801e864 0099
    lsls r0,r1,#0x5    @ 0801e866 4801
    adds r0,r0,r1    @ 0801e868 4018
    lsls r0,r0,#0x3    @ 0801e86a c000
    ldr r1, DAT_0801e968                     @ 0801e86c 3e49
    adds r0,r0,r1    @ 0801e86e 4018
    .hword 0x4684    @ 0801e870 8446
    movs r0,#0x0    @ 0801e872 0020
    .hword 0x4662    @ 0801e874 6246
    str r0,[r2,#0x0]                         @ 0801e876 1060
    str r0,[r2,#0x8]                         @ 0801e878 9060
    str r0,[r2,#0x4]                         @ 0801e87a 5060
    movs r4,#0x0    @ 0801e87c 0024
    ldrb r3,[r6,#0x18]                       @ 0801e87e 337e
    cmp r4,r3                                @ 0801e880 9c42
    bge LAB_0801e8ca                         @ 0801e882 22da
    ldr r5, PTR_card_stats_table_0801e96c    @ 0801e884 394d
    .hword 0x46a8    @ 0801e886 a846
    ldr r1, DAT_0801e970                     @ 0801e888 3949
    ldr r7,[sp,#0x0]                         @ 0801e88a 009f
    lsls r0,r7,#0x1    @ 0801e88c 7800
    adds r0,r0,r1    @ 0801e88e 4018
    adds r5,r0,#0x4    @ 0801e890 051d
LAB_0801e892:
    .hword 0x4660    @ 0801e892 6046
    ldr r3,[r0,#0x0]                         @ 0801e894 0368
    lsls r0,r3,#0x1    @ 0801e896 5800
    .hword 0x4662    @ 0801e898 6246
    adds r2,#0xc    @ 0801e89a 0c32
    adds r2,r2,r0    @ 0801e89c 1218
    lsls r0,r4,#0x1    @ 0801e89e 6000
    adds r1,r6,#0x0    @ 0801e8a0 311c
    adds r1,#0x1c    @ 0801e8a2 1c31
    adds r1,r1,r0    @ 0801e8a4 0918
    movs r0,#0x16    @ 0801e8a6 1620
    ldrh r7,[r1,#0x0]                        @ 0801e8a8 0f88
    muls r0,r7    @ 0801e8aa 7843
    add r0,r8                                @ 0801e8ac 4044
    ldrh r0,[r0,#0x0]                        @ 0801e8ae 0088
    strh r0,[r2,#0x0]                        @ 0801e8b0 1080
    adds r3,#0x1    @ 0801e8b2 0133
    .hword 0x4660    @ 0801e8b4 6046
    str r3,[r0,#0x0]                         @ 0801e8b6 0360
    ldrh r0,[r1,#0x0]                        @ 0801e8b8 0888
    strh r0,[r5,#0x0]                        @ 0801e8ba 2880
    adds r5,#0x4    @ 0801e8bc 0435
    movs r1,#0x1    @ 0801e8be 0121
    add r9,r1                                @ 0801e8c0 8944
    adds r4,#0x1    @ 0801e8c2 0134
    ldrb r2,[r6,#0x18]                       @ 0801e8c4 327e
    cmp r4,r2                                @ 0801e8c6 9442
    blt LAB_0801e892                         @ 0801e8c8 e3db
LAB_0801e8ca:
    movs r4,#0x0    @ 0801e8ca 0024
    ldrb r3,[r6,#0x19]                       @ 0801e8cc 737e
    cmp r4,r3                                @ 0801e8ce 9c42
    bge LAB_0801e90a                         @ 0801e8d0 1bda
    .hword 0x4665    @ 0801e8d2 6546
    adds r5,#0xac    @ 0801e8d4 ac35
    str r5,[sp,#0x4]                         @ 0801e8d6 0195
    ldr r7, PTR_card_stats_table_0801e96c    @ 0801e8d8 244f
    .hword 0x46ba    @ 0801e8da ba46
    movs r0,#0x16    @ 0801e8dc 1620
    .hword 0x4680    @ 0801e8de 8046
    adds r3,r6,#0x0    @ 0801e8e0 331c
    adds r3,#0xbc    @ 0801e8e2 bc33
LAB_0801e8e4:
    .hword 0x4661    @ 0801e8e4 6146
    ldr r2,[r1,#0x4]                         @ 0801e8e6 4a68
    lsls r1,r2,#0x1    @ 0801e8e8 5100
    ldr r5,[sp,#0x4]                         @ 0801e8ea 019d
    adds r1,r5,r1    @ 0801e8ec 6918
    ldrh r7,[r3,#0x0]                        @ 0801e8ee 1f88
    .hword 0x4640    @ 0801e8f0 4046
    muls r0,r7    @ 0801e8f2 7843
    add r0,r10                               @ 0801e8f4 5044
    ldrh r0,[r0,#0x0]                        @ 0801e8f6 0088
    strh r0,[r1,#0x0]                        @ 0801e8f8 0880
    adds r2,#0x1    @ 0801e8fa 0132
    .hword 0x4660    @ 0801e8fc 6046
    str r2,[r0,#0x4]                         @ 0801e8fe 4260
    adds r3,#0x2    @ 0801e900 0233
    adds r4,#0x1    @ 0801e902 0134
    ldrb r1,[r6,#0x19]                       @ 0801e904 717e
    cmp r4,r1                                @ 0801e906 8c42
    blt LAB_0801e8e4                         @ 0801e908 ecdb
LAB_0801e90a:
    movs r4,#0x0    @ 0801e90a 0024
    ldrb r2,[r6,#0x1a]                       @ 0801e90c b27e
    cmp r4,r2                                @ 0801e90e 9442
    bge LAB_0801e958                         @ 0801e910 22da
    ldr r3, PTR_card_stats_table_0801e96c    @ 0801e912 164b
    .hword 0x4698    @ 0801e914 9846
    ldr r0, DAT_0801e970                     @ 0801e916 1648
    .hword 0x464d    @ 0801e918 4d46
    lsls r2,r5,#0x2    @ 0801e91a aa00
    ldr r7,[sp,#0x0]                         @ 0801e91c 009f
    lsls r1,r7,#0x1    @ 0801e91e 7900
    adds r1,r1,r0    @ 0801e920 0918
    adds r5,r2,r1    @ 0801e922 5518
LAB_0801e924:
    .hword 0x4660    @ 0801e924 6046
    ldr r3,[r0,#0x8]                         @ 0801e926 8368
    lsls r0,r3,#0x1    @ 0801e928 5800
    .hword 0x4662    @ 0801e92a 6246
    adds r2,#0xca    @ 0801e92c ca32
    adds r2,r2,r0    @ 0801e92e 1218
    lsls r0,r4,#0x1    @ 0801e930 6000
    adds r1,r6,#0x0    @ 0801e932 311c
    adds r1,#0xda    @ 0801e934 da31
    adds r1,r1,r0    @ 0801e936 0918
    movs r0,#0x16    @ 0801e938 1620
    ldrh r7,[r1,#0x0]                        @ 0801e93a 0f88
    muls r0,r7    @ 0801e93c 7843
    add r0,r8                                @ 0801e93e 4044
    ldrh r0,[r0,#0x0]                        @ 0801e940 0088
    strh r0,[r2,#0x0]                        @ 0801e942 1080
    adds r3,#0x1    @ 0801e944 0133
    .hword 0x4660    @ 0801e946 6046
    str r3,[r0,#0x8]                         @ 0801e948 8360
    ldrh r0,[r1,#0x0]                        @ 0801e94a 0888
    strh r0,[r5,#0x0]                        @ 0801e94c 2880
    adds r5,#0x4    @ 0801e94e 0435
    adds r4,#0x1    @ 0801e950 0134
    ldrb r1,[r6,#0x1a]                       @ 0801e952 b17e
    cmp r4,r1                                @ 0801e954 8c42
    blt LAB_0801e924                         @ 0801e956 e5db
LAB_0801e958:
    add sp,#0x8                              @ 0801e958 02b0
    pop {r3,r4,r5}                           @ 0801e95a 38bc
    .hword 0x4698    @ 0801e95c 9846
    .hword 0x46a1    @ 0801e95e a146
    .hword 0x46aa    @ 0801e960 aa46
    pop {r4,r5,r6,r7}                        @ 0801e962 f0bc
    pop {r0}                                 @ 0801e964 01bc
    bx r0                                    @ 0801e966 0047
DAT_0801e968:
    .word  0x0201e2b4                     @ 0801e968 b4e20102
PTR_card_stats_table_0801e96c:
    .word  card_stats_table               @ 0801e96c b8698109
DAT_0801e970:
    .word  0x0201ff60                     @ 0801e970 60ff0102

@ Specialized wrapper for fill_card_fs_display_entries (FUN_0801e850) that fixes the second argument to 0x02001138 (card_list slot display buffer EWRAM address) and forwards r0 (slot_index) unchanged. Called by FUN_0802752c to write card FS data into the card_list slot display buffer. No computation logic; single ldr overwrites r1 then jumps to core function. r0=u8 slot_index [0..1]. Returns void.
fill_card_fs_display_entries_for_card_list:
    push {lr}                                @ 0801e974 00b5
    ldr r1, DAT_0801e980                     @ 0801e976 0249
    bl fill_card_fs_display_entries          @ 0801e978 fff76aff
    pop {r0}                                 @ 0801e97c 01bc
    bx r0                                    @ 0801e97e 0047
DAT_0801e980:
    .word  0x02001138                     @ 0801e980 38110002

@ Called by FUN_0801fec0 (large duel scene switch dispatcher) and FUN_08027714 (duel field prng). Main frame driver for the duel field, dispatches on global state flags via multiple paths: (1) checks [0x02023130+0x88*4] bit-mask 0xff<<10 - if 0 enters prng anim path: checks [BASE+0x21e] bit0 and [BASE+0x226] bit0, if met calls request_sound_engine_code10 + tick_duel_field_fadein_step; (2) checks multiple flags then calls advance_duel_turn_by_prng_anim; (3) conditionally calls enqueue_duel_phase_sprite_by_side; (4) conditionally calls init_duel_phase_display_flag_with_sprite; (5) unconditionally calls render_duel_field_oam_all; (6) multi-branch calls tick_card_list_scene_frame / tick_zone_display_frame / advance_duel_turn_by_prng_anim; (7) clears prng+0x213/0x217 bit7. Exit: LAB_0801ec84=movs r0,#1; LAB_0801eb70=movs r0,#0; via pop {r3}; restore r8-r10; pop {r4-r7}; pop {r1}; bx r1.
@ 
@ Constants:
@ - gP1LifePoints=0x0201c4e0
@ - BASE=0x02023130
@ - PRNG_ANIM_MASK=0xff<<0xa (high 10-bit duel anim state check)
@ - gPrng=0x03000040
@ - TIMER_FIELD=gPrng+0x84*4 (duel timer, divide by 0x3c = minutes)
@ - LP_RATIO_THRESHOLD=0xb4=180 (LP ratio card condition trigger)
@ - FLAG_BASE=gBannerState=0x0201fec0 (banner state word)
tick_duel_field_main_frame:
    push {r4,r5,r6,r7,lr}                    @ 0801e984 f0b5
    .hword 0x4647    @ 0801e986 4746
    push {r7}                                @ 0801e988 80b4
    ldr r2, DAT_0801e9ec                     @ 0801e98a 184a
    movs r1,#0x88    @ 0801e98c 8821
    lsls r1,r1,#0x2    @ 0801e98e 8900
    adds r0,r2,r1    @ 0801e990 5018
    ldr r0,[r0,#0x0]                         @ 0801e992 0068
    movs r1,#0xff    @ 0801e994 ff21
    lsls r1,r1,#0xa    @ 0801e996 8902
    ands r0,r1    @ 0801e998 0840
    adds r4,r2,#0x0    @ 0801e99a 141c
    cmp r0,#0x0                              @ 0801e99c 0028
    bne LAB_0801ea4c                         @ 0801e99e 55d1
    ldr r2, DAT_0801e9f0                     @ 0801e9a0 134a
    adds r1,r4,r2    @ 0801e9a2 a118
    movs r2,#0x1    @ 0801e9a4 0122
    adds r0,r2,#0x0    @ 0801e9a6 101c
    ldrb r1,[r1,#0x0]                        @ 0801e9a8 0978
    ands r0,r1    @ 0801e9aa 0840
    cmp r0,#0x0                              @ 0801e9ac 0028
    bne LAB_0801ea4c                         @ 0801e9ae 4dd1
    ldr r0, DAT_0801e9f4                     @ 0801e9b0 1048
    adds r5,r4,r0    @ 0801e9b2 2518
    ldrb r3,[r5,#0x0]                        @ 0801e9b4 2b78
    adds r0,r2,#0x0    @ 0801e9b6 101c
    ands r0,r3    @ 0801e9b8 1840
    cmp r0,#0x0                              @ 0801e9ba 0028
    bne LAB_0801e9fc                         @ 0801e9bc 1ed1
    ldr r2, PTR_gPrng_0801e9f8               @ 0801e9be 0e4a
    movs r0,#0xa4    @ 0801e9c0 a420
    lsls r0,r0,#0x1    @ 0801e9c2 4000
    adds r1,r2,r0    @ 0801e9c4 1118
    movs r0,#0x8    @ 0801e9c6 0820
    ldrh r1,[r1,#0x0]                        @ 0801e9c8 0988
    ands r0,r1    @ 0801e9ca 0840
    cmp r0,#0x0                              @ 0801e9cc 0028
    beq LAB_0801ea4c                         @ 0801e9ce 3dd0
    movs r1,#0xa3    @ 0801e9d0 a321
    lsls r1,r1,#0x1    @ 0801e9d2 4900
    adds r2,r2,r1    @ 0801e9d4 5218
    movs r1,#0xc1    @ 0801e9d6 c121
    lsls r1,r1,#0x2    @ 0801e9d8 8900
    adds r0,r1,#0x0    @ 0801e9da 081c
    ldrh r2,[r2,#0x0]                        @ 0801e9dc 1288
    ands r0,r2    @ 0801e9de 1040
    cmp r0,r1                                @ 0801e9e0 8842
    bne LAB_0801ea4c                         @ 0801e9e2 33d1
    movs r0,#0x1    @ 0801e9e4 0120
    orrs r0,r3    @ 0801e9e6 1843
    strb r0,[r5,#0x0]                        @ 0801e9e8 2870
    b LAB_0801eb6c                           @ 0801e9ea bfe0
DAT_0801e9ec:
    .word  0x02023130                     @ 0801e9ec 30310202
DAT_0801e9f0:
    .word  0x0000021e                     @ 0801e9f0 1e020000
DAT_0801e9f4:
    .word  0x00000226                     @ 0801e9f4 26020000
PTR_gPrng_0801e9f8:
    .word  gPrng                          @ 0801e9f8 40000003
LAB_0801e9fc:
    movs r1,#0x87    @ 0801e9fc 8721
    lsls r1,r1,#0x2    @ 0801e9fe 8900
    adds r0,r4,r1    @ 0801ea00 6018
    ldrh r0,[r0,#0x0]                        @ 0801ea02 0088
    cmp r0,#0x0                              @ 0801ea04 0028
    bne LAB_0801ea18                         @ 0801ea06 07d1
    bl request_sound_engine_code10           @ 0801ea08 dbf09af8
    bl tick_duel_field_fadein_step           @ 0801ea0c aef026f8
    cmp r0,#0x0                              @ 0801ea10 0028
    bne LAB_0801ea16                         @ 0801ea12 00d1
    b LAB_0801eb70                           @ 0801ea14 ace0
LAB_0801ea16:
    b LAB_0801ec84                           @ 0801ea16 35e1
LAB_0801ea18:
    ldr r1, DAT_0801ea40                     @ 0801ea18 0949
    adds r0,r2,#0x0    @ 0801ea1a 101c
    ldrb r1,[r1,#0x0]                        @ 0801ea1c 0978
    ands r0,r1    @ 0801ea1e 0840
    cmp r0,#0x0                              @ 0801ea20 0028
    beq LAB_0801ea26                         @ 0801ea22 00d0
    b LAB_0801ec2c                           @ 0801ea24 02e1
LAB_0801ea26:
    ldr r1, DAT_0801ea44                     @ 0801ea26 0749
    ldr r4, DAT_0801ea48                     @ 0801ea28 074c
    adds r1,r1,r4    @ 0801ea2a 0919
    adds r0,r2,#0x0    @ 0801ea2c 101c
    ldrb r1,[r1,#0x0]                        @ 0801ea2e 0978
    ands r0,r1    @ 0801ea30 0840
    cmp r0,#0x0                              @ 0801ea32 0028
    beq LAB_0801ea38                         @ 0801ea34 00d0
    b LAB_0801ec50                           @ 0801ea36 0be1
LAB_0801ea38:
    bl advance_duel_turn_by_prng_anim        @ 0801ea38 76f0b8f9
    b LAB_0801eb70                           @ 0801ea3c 98e0
    .zero  0x2
DAT_0801ea40:
    .word  0x0201f440                     @ 0801ea40 40f40102
DAT_0801ea44:
    .word  0x02020160                     @ 0801ea44 60010202
DAT_0801ea48:
    .word  0x00002f51                     @ 0801ea48 512f0000
LAB_0801ea4c:
    movs r0,#0x89    @ 0801ea4c 8920
    lsls r0,r0,#0x2    @ 0801ea4e 8000
    adds r6,r4,r0    @ 0801ea50 2618
    ldrh r0,[r6,#0x0]                        @ 0801ea52 3088
    cmp r0,#0x0                              @ 0801ea54 0028
    beq LAB_0801ea5c                         @ 0801ea56 01d0
    bl enqueue_duel_phase_sprite_by_side     @ 0801ea58 75f04efe
LAB_0801ea5c:
    ldr r7, PTR_gP1LifePoints_0801eb1c       @ 0801ea5c 2f4f
    ldr r1, DAT_0801eb20                     @ 0801ea5e 3049
    adds r0,r7,r1    @ 0801ea60 7818
    ldr r0,[r0,#0x0]                         @ 0801ea62 0068
    cmp r0,#0x0                              @ 0801ea64 0028
    bne LAB_0801ea6a                         @ 0801ea66 00d1
    b LAB_0801ec1a                           @ 0801ea68 d7e0
LAB_0801ea6a:
    ldr r2, DAT_0801eb24                     @ 0801ea6a 2e4a
    adds r0,r2,#0x0    @ 0801ea6c 101c
    adds r0,#0x37    @ 0801ea6e 3730
    ldrb r0,[r0,#0x0]                        @ 0801ea70 0078
    lsls r5,r0,#0x19    @ 0801ea72 4506
    lsrs r1,r5,#0x1b    @ 0801ea74 e90e
    lsls r0,r1,#0x2    @ 0801ea76 8800
    adds r0,r0,r1    @ 0801ea78 4018
    lsls r1,r0,#0x4    @ 0801ea7a 0101
    subs r1,r1,r0    @ 0801ea7c 091a
    lsls r1,r1,#0x2    @ 0801ea7e 8900
    .hword 0x4690    @ 0801ea80 9046
    cmp r1,#0x0                              @ 0801ea82 0029
    bne LAB_0801ea88                         @ 0801ea84 00d1
    b LAB_0801ec1a                           @ 0801ea86 c8e0
LAB_0801ea88:
    ldr r2, DAT_0801eb28                     @ 0801ea88 274a
    adds r0,r4,r2    @ 0801ea8a a018
    ldrb r4,[r0,#0x0]                        @ 0801ea8c 0478
    movs r0,#0x10    @ 0801ea8e 1020
    ands r0,r4    @ 0801ea90 2040
    cmp r0,#0x0                              @ 0801ea92 0028
    bne LAB_0801eb80                         @ 0801ea94 74d1
    ldr r1, DAT_0801eb2c                     @ 0801ea96 2549
    ldr r0, DAT_0801eb30                     @ 0801ea98 2548
    adds r1,r1,r0    @ 0801ea9a 0918
    movs r2,#0x1    @ 0801ea9c 0122
    adds r0,r2,#0x0    @ 0801ea9e 101c
    ldrb r1,[r1,#0x0]                        @ 0801eaa0 0978
    ands r0,r1    @ 0801eaa2 0840
    cmp r0,#0x0                              @ 0801eaa4 0028
    bne LAB_0801eb80                         @ 0801eaa6 6bd1
    ldr r1, DAT_0801eb34                     @ 0801eaa8 2249
    adds r0,r2,#0x0    @ 0801eaaa 101c
    ldrb r1,[r1,#0x0]                        @ 0801eaac 0978
    ands r0,r1    @ 0801eaae 0840
    cmp r0,#0x0                              @ 0801eab0 0028
    bne LAB_0801eb80                         @ 0801eab2 65d1
    ldr r1, DAT_0801eb38                     @ 0801eab4 2049
    adds r0,r2,#0x0    @ 0801eab6 101c
    ldrb r1,[r1,#0x0]                        @ 0801eab8 0978
    ands r0,r1    @ 0801eaba 0840
    cmp r0,#0x0                              @ 0801eabc 0028
    bne LAB_0801eb80                         @ 0801eabe 5fd1
    ldr r1, DAT_0801eb3c                     @ 0801eac0 1e49
    adds r0,r2,#0x0    @ 0801eac2 101c
    ldrb r1,[r1,#0x0]                        @ 0801eac4 0978
    ands r0,r1    @ 0801eac6 0840
    cmp r0,#0x0                              @ 0801eac8 0028
    bne LAB_0801eb80                         @ 0801eaca 59d1
    .hword 0x4641    @ 0801eacc 4146
    adds r1,#0x36    @ 0801eace 3631
    movs r0,#0x40    @ 0801ead0 4020
    ldrb r1,[r1,#0x0]                        @ 0801ead2 0978
    ands r0,r1    @ 0801ead4 0840
    cmp r0,#0x0                              @ 0801ead6 0028
    bne LAB_0801eb48                         @ 0801ead8 36d1
    ldr r0, PTR_gPrng_0801eb40               @ 0801eada 1948
    movs r1,#0x84    @ 0801eadc 8421
    lsls r1,r1,#0x2    @ 0801eade 8900
    adds r0,r0,r1    @ 0801eae0 4018
    ldr r0,[r0,#0x0]                         @ 0801eae2 0068
    lsls r0,r0,#0x1    @ 0801eae4 4000
    lsrs r0,r0,#0x1    @ 0801eae6 4008
    movs r1,#0x3c    @ 0801eae8 3c21
    bl __divsi3                              @ 0801eaea eff08bfd
    lsrs r1,r5,#0x1b    @ 0801eaee e90e
    lsls r2,r1,#0x2    @ 0801eaf0 8a00
    adds r2,r2,r1    @ 0801eaf2 5218
    lsls r1,r2,#0x4    @ 0801eaf4 1101
    subs r1,r1,r2    @ 0801eaf6 891a
    lsls r1,r1,#0x2    @ 0801eaf8 8900
    cmp r0,r1                                @ 0801eafa 8842
    blt LAB_0801eb48                         @ 0801eafc 24db
    ldrh r0,[r6,#0x0]                        @ 0801eafe 3088
    cmp r0,#0x0                              @ 0801eb00 0028
    bne LAB_0801eb48                         @ 0801eb02 21d1
    movs r0,#0xc    @ 0801eb04 0c20
    ands r0,r4    @ 0801eb06 2040
    cmp r0,#0x8                              @ 0801eb08 0828
    beq LAB_0801eb48                         @ 0801eb0a 1dd0
    ldr r2, DAT_0801eb44                     @ 0801eb0c 0d4a
    adds r0,r7,r2    @ 0801eb0e b818
    ldrh r0,[r0,#0x0]                        @ 0801eb10 0088
    adds r0,#0x1    @ 0801eb12 0130
    strh r0,[r6,#0x0]                        @ 0801eb14 3080
    bl enqueue_duel_phase_sprite_by_side     @ 0801eb16 75f0effd
    b LAB_0801eb6c                           @ 0801eb1a 27e0
PTR_gP1LifePoints_0801eb1c:
    .word  gP1LifePoints                  @ 0801eb1c e0c40102
DAT_0801eb20:
    .word  0x00001d08                     @ 0801eb20 081d0000
DAT_0801eb24:
    .word  0x02023360                     @ 0801eb24 60330202
DAT_0801eb28:
    .word  0x00000222                     @ 0801eb28 22020000
DAT_0801eb2c:
    .word  0x02020160                     @ 0801eb2c 60010202
DAT_0801eb30:
    .word  0x00002f51                     @ 0801eb30 512f0000
DAT_0801eb34:
    .word  0x0201ff30                     @ 0801eb34 30ff0102
DAT_0801eb38:
    .word  0x0201f440                     @ 0801eb38 40f40102
DAT_0801eb3c:
    .word  gBannerState                   @ 0801eb3c c0fe0102
PTR_gPrng_0801eb40:
    .word  gPrng                          @ 0801eb40 40000003
DAT_0801eb44:
    .word  0x00001cec                     @ 0801eb44 ec1c0000
LAB_0801eb48:
    ldr r0, DAT_0801eb74                     @ 0801eb48 0a48
    ldr r4, DAT_0801eb78                     @ 0801eb4a 0b4c
    adds r2,r0,r4    @ 0801eb4c 0219
    ldrb r1,[r2,#0x0]                        @ 0801eb4e 1178
    movs r0,#0xc    @ 0801eb50 0c20
    ands r0,r1    @ 0801eb52 0840
    cmp r0,#0x4                              @ 0801eb54 0428
    bne LAB_0801eb80                         @ 0801eb56 13d1
    movs r0,#0xd    @ 0801eb58 0d20
    rsbs r0,r0,#0    @ 0801eb5a 4042
    ands r0,r1    @ 0801eb5c 0840
    movs r1,#0x8    @ 0801eb5e 0821
    orrs r0,r1    @ 0801eb60 0843
    strb r0,[r2,#0x0]                        @ 0801eb62 1070
    ldr r0, DAT_0801eb7c                     @ 0801eb64 0548
    ldr r0,[r0,#0x4]                         @ 0801eb66 4068
    bl init_duel_phase_display_flag_with_sprite @ 0801eb68 75f0f2fd
LAB_0801eb6c:
    bl render_duel_field_oam_all             @ 0801eb6c aef042f9
LAB_0801eb70:
    movs r0,#0x0    @ 0801eb70 0020
    b LAB_0801ec86                           @ 0801eb72 88e0
DAT_0801eb74:
    .word  0x02023130                     @ 0801eb74 30310202
DAT_0801eb78:
    .word  0x00000222                     @ 0801eb78 22020000
DAT_0801eb7c:
    .word  0x0201e2a0                     @ 0801eb7c a0e20102
LAB_0801eb80:
    ldr r4, PTR_gPrng_0801ebb8               @ 0801eb80 0d4c
    movs r1,#0x84    @ 0801eb82 8421
    lsls r1,r1,#0x2    @ 0801eb84 8900
    adds r0,r4,r1    @ 0801eb86 6018
    ldr r0,[r0,#0x0]                         @ 0801eb88 0068
    lsls r0,r0,#0x1    @ 0801eb8a 4000
    lsrs r0,r0,#0x1    @ 0801eb8c 4008
    movs r1,#0x3c    @ 0801eb8e 3c21
    bl __divsi3                              @ 0801eb90 eff038fd
    .hword 0x4641    @ 0801eb94 4146
    adds r1,#0x37    @ 0801eb96 3731
    ldrb r1,[r1,#0x0]                        @ 0801eb98 0978
    lsls r1,r1,#0x19    @ 0801eb9a 4906
    lsrs r1,r1,#0x1b    @ 0801eb9c c90e
    lsls r2,r1,#0x2    @ 0801eb9e 8a00
    adds r2,r2,r1    @ 0801eba0 5218
    lsls r1,r2,#0x4    @ 0801eba2 1101
    subs r1,r1,r2    @ 0801eba4 891a
    lsls r1,r1,#0x2    @ 0801eba6 8900
    cmp r0,r1                                @ 0801eba8 8842
    bgt LAB_0801ebc0                         @ 0801ebaa 09dc
    ldr r2, DAT_0801ebbc                     @ 0801ebac 034a
    adds r1,r4,r2    @ 0801ebae a118
    movs r0,#0x80    @ 0801ebb0 8020
    ldrb r4,[r1,#0x0]                        @ 0801ebb2 0c78
    orrs r0,r4    @ 0801ebb4 2043
    b LAB_0801ebca                           @ 0801ebb6 08e0
PTR_gPrng_0801ebb8:
    .word  gPrng                          @ 0801ebb8 40000003
DAT_0801ebbc:
    .word  0x00000213                     @ 0801ebbc 13020000
LAB_0801ebc0:
    ldr r0, DAT_0801ebfc                     @ 0801ebc0 0e48
    adds r1,r4,r0    @ 0801ebc2 2118
    movs r0,#0x7f    @ 0801ebc4 7f20
    ldrb r2,[r1,#0x0]                        @ 0801ebc6 0a78
    ands r0,r2    @ 0801ebc8 1040
LAB_0801ebca:
    strb r0,[r1,#0x0]                        @ 0801ebca 0870
    ldr r0, DAT_0801ec00                     @ 0801ebcc 0c48
    ldr r0,[r0,#0x4]                         @ 0801ebce 4068
    bl check_card_play_condition_eligible    @ 0801ebd0 1df042f8
    cmp r0,#0x0                              @ 0801ebd4 0028
    beq LAB_0801ec0c                         @ 0801ebd6 19d0
    ldr r4, PTR_gPrng_0801ec04               @ 0801ebd8 0a4c
    movs r1,#0x85    @ 0801ebda 8521
    lsls r1,r1,#0x2    @ 0801ebdc 8900
    adds r0,r4,r1    @ 0801ebde 6018
    ldr r0,[r0,#0x0]                         @ 0801ebe0 0068
    lsls r0,r0,#0x1    @ 0801ebe2 4000
    lsrs r0,r0,#0x1    @ 0801ebe4 4008
    movs r1,#0x3c    @ 0801ebe6 3c21
    bl __divsi3                              @ 0801ebe8 eff00cfd
    cmp r0,#0xb4                             @ 0801ebec b428
    bgt LAB_0801ec0c                         @ 0801ebee 0ddc
    ldr r2, DAT_0801ec08                     @ 0801ebf0 054a
    adds r1,r4,r2    @ 0801ebf2 a118
    movs r0,#0x80    @ 0801ebf4 8020
    ldrb r4,[r1,#0x0]                        @ 0801ebf6 0c78
    orrs r0,r4    @ 0801ebf8 2043
    b LAB_0801ec18                           @ 0801ebfa 0de0
DAT_0801ebfc:
    .word  0x00000213                     @ 0801ebfc 13020000
DAT_0801ec00:
    .word  0x0201e2a0                     @ 0801ec00 a0e20102
PTR_gPrng_0801ec04:
    .word  gPrng                          @ 0801ec04 40000003
DAT_0801ec08:
    .word  0x00000217                     @ 0801ec08 17020000
LAB_0801ec0c:
    ldr r1, PTR_gPrng_0801ec34               @ 0801ec0c 0949
    ldr r0, DAT_0801ec38                     @ 0801ec0e 0a48
    adds r1,r1,r0    @ 0801ec10 0918
    movs r0,#0x7f    @ 0801ec12 7f20
    ldrb r2,[r1,#0x0]                        @ 0801ec14 0a78
    ands r0,r2    @ 0801ec16 1040
LAB_0801ec18:
    strb r0,[r1,#0x0]                        @ 0801ec18 0870
LAB_0801ec1a:
    bl render_duel_field_oam_all             @ 0801ec1a aef0ebf8
    ldr r1, DAT_0801ec3c                     @ 0801ec1e 0749
    movs r2,#0x1    @ 0801ec20 0122
    adds r0,r2,#0x0    @ 0801ec22 101c
    ldrb r1,[r1,#0x0]                        @ 0801ec24 0978
    ands r0,r1    @ 0801ec26 0840
    cmp r0,#0x0                              @ 0801ec28 0028
    beq LAB_0801ec40                         @ 0801ec2a 09d0
LAB_0801ec2c:
    bl tick_card_list_scene_frame            @ 0801ec2c a9f02cfd
    b LAB_0801eb70                           @ 0801ec30 9ee7
    .zero  0x2
PTR_gPrng_0801ec34:
    .word  gPrng                          @ 0801ec34 40000003
DAT_0801ec38:
    .word  0x00000217                     @ 0801ec38 17020000
DAT_0801ec3c:
    .word  0x0201f440                     @ 0801ec3c 40f40102
LAB_0801ec40:
    ldr r1, DAT_0801ec58                     @ 0801ec40 0549
    ldr r4, DAT_0801ec5c                     @ 0801ec42 064c
    adds r1,r1,r4    @ 0801ec44 0919
    adds r0,r2,#0x0    @ 0801ec46 101c
    ldrb r1,[r1,#0x0]                        @ 0801ec48 0978
    ands r0,r1    @ 0801ec4a 0840
    cmp r0,#0x0                              @ 0801ec4c 0028
    beq LAB_0801ec60                         @ 0801ec4e 07d0
LAB_0801ec50:
    bl tick_zone_display_frame               @ 0801ec50 adf06afc
    b LAB_0801eb70                           @ 0801ec54 8ce7
    .zero  0x2
DAT_0801ec58:
    .word  0x02020160                     @ 0801ec58 60010202
DAT_0801ec5c:
    .word  0x00002f51                     @ 0801ec5c 512f0000
LAB_0801ec60:
    bl advance_duel_turn_by_prng_anim        @ 0801ec60 76f0a4f8
    cmp r0,#0x0                              @ 0801ec64 0028
    bne LAB_0801ec6a                         @ 0801ec66 00d1
    b LAB_0801eb70                           @ 0801ec68 82e7
LAB_0801ec6a:
    ldr r2, PTR_gPrng_0801ec90               @ 0801ec6a 094a
    ldr r0, DAT_0801ec94                     @ 0801ec6c 0948
    adds r3,r2,r0    @ 0801ec6e 1318
    movs r1,#0x7f    @ 0801ec70 7f21
    adds r0,r1,#0x0    @ 0801ec72 081c
    ldrb r4,[r3,#0x0]                        @ 0801ec74 1c78
    ands r0,r4    @ 0801ec76 2040
    strb r0,[r3,#0x0]                        @ 0801ec78 1870
    ldr r0, DAT_0801ec98                     @ 0801ec7a 0748
    adds r2,r2,r0    @ 0801ec7c 1218
    ldrb r4,[r2,#0x0]                        @ 0801ec7e 1478
    ands r1,r4    @ 0801ec80 2140
    strb r1,[r2,#0x0]                        @ 0801ec82 1170
LAB_0801ec84:
    movs r0,#0x1    @ 0801ec84 0120
LAB_0801ec86:
    pop {r3}                                 @ 0801ec86 08bc
    .hword 0x4698    @ 0801ec88 9846
    pop {r4,r5,r6,r7}                        @ 0801ec8a f0bc
    pop {r1}                                 @ 0801ec8c 02bc
    bx r1                                    @ 0801ec8e 0847
PTR_gPrng_0801ec90:
    .word  gPrng                          @ 0801ec90 40000003
DAT_0801ec94:
    .word  0x00000213                     @ 0801ec94 13020000
DAT_0801ec98:
    .word  0x00000217                     @ 0801ec98 17020000

@ Core card display operation dispatcher (indeg=114). r0=op_code [1..0x3d] (subs#1; cmp#0x3c); dispatches via 61-entry jump table 0x0801ecc4. Case handlers (sample): 0x01/0x21=init_field_slot_aob_ctx_a, 0x03=write_zone_slot_oam_descriptor+update_zone_activation_display_state, 0x06=init_card_effect_aob_ctx, 0x09=build_slot_activation_mask_for_player+write_field_slot_activation_mask, 0x0b=init_field_slot_aob_ctx_b, 0x0c=write_zone_oam_entry_with_flip, 0x0d=write_lp_digit_tiles_to_vram, 0x14=get_player_lp_by_field_type+render_field_zone_card_tile_by_type, 0x18=init_field_slot_aob_ctx_d, 0x19=init_field_slot_aob_ctx_c, 0x1a=init_field_slot_ctx_zoom, 0x1b=render_field_slot_card_tile_by_id, 0x1c=init_field_slot_aob_ctx_a (case alias), 0x24=refresh_duel_field+refresh_zone_effect_buff_cache+refresh_all_zone_slot_tile_display, 0x31=copy_game_text_to_card_name_vram, 0x32=build_field_zone_display_state. r1/r2/r3=op args (transparent to callee). Returns 1=done or 0=default/invalid. Constants: jump_table=0x0801ecc4, op_range=[1..0x3d].
dispatch_card_display_op:
    push {r4,r5,r6,r7,lr}                    @ 0801ec9c f0b5
    .hword 0x4657    @ 0801ec9e 5746
    .hword 0x464e    @ 0801eca0 4e46
    .hword 0x4645    @ 0801eca2 4546
    push {r5,r6,r7}                          @ 0801eca4 e0b4
    adds r6,r1,#0x0    @ 0801eca6 0e1c
    adds r7,r2,#0x0    @ 0801eca8 171c
    adds r4,r3,#0x0    @ 0801ecaa 1c1c
    subs r0,#0x1    @ 0801ecac 0138
    cmp r0,#0x3c                             @ 0801ecae 3c28
    bls LAB_0801ecb4                         @ 0801ecb0 00d9
    b switchD_0801ecbc__caseD_8              @ 0801ecb2 67e1
LAB_0801ecb4:
    lsls r0,r0,#0x2    @ 0801ecb4 8000
    ldr r1, DAT_0801ecc0                     @ 0801ecb6 0249
    adds r0,r0,r1    @ 0801ecb8 4018
    ldr r0,[r0,#0x0]                         @ 0801ecba 0068
switchD_0801ecbc__switchD:
    .hword 0x4687    @ 0801ecbc 8746
    .zero  0x2
DAT_0801ecc0:
    .word  0x0801ecc4                     @ 0801ecc0 c4ec0108
switchD_0801ecbc__switchdataD_0801ecc4:
    .word  0x0801ef60                     @ 0801ecc4 60ef0108
    .word  0x0801ef60                     @ 0801ecc8 60ef0108
    .word  0x0801ee48                     @ 0801eccc 48ee0108
    .word  0x0801ef60                     @ 0801ecd0 60ef0108
    .word  0x0801ef60                     @ 0801ecd4 60ef0108
    .word  0x0801eee4                     @ 0801ecd8 e4ee0108
    .word  0x0801ef42                     @ 0801ecdc 42ef0108
    .word  0x0801ef84                     @ 0801ece0 84ef0108
    .word  0x0801ee06                     @ 0801ece4 06ee0108
    .word  0x0801edc2                     @ 0801ece8 c2ed0108
    .word  0x0801ee1e                     @ 0801ecec 1eee0108
    .word  0x0801ee12                     @ 0801ecf0 12ee0108
    .word  0x0801ee36                     @ 0801ecf4 36ee0108
    .word  0x0801ef60                     @ 0801ecf8 60ef0108
    .word  0x0801ef84                     @ 0801ecfc 84ef0108
    .word  0x0801ef60                     @ 0801ed00 60ef0108
    .word  0x0801eeec                     @ 0801ed04 ecee0108
    .word  0x0801ef20                     @ 0801ed08 20ef0108
    .word  0x0801ef60                     @ 0801ed0c 60ef0108
    .word  0x0801ede6                     @ 0801ed10 e6ed0108
    .word  0x0801ef60                     @ 0801ed14 60ef0108
    .word  0x0801ede6                     @ 0801ed18 e6ed0108
    .word  0x0801ef60                     @ 0801ed1c 60ef0108
    .word  0x0801edb8                     @ 0801ed20 b8ed0108
    .word  0x0801edc6                     @ 0801ed24 c6ed0108
    .word  0x0801eddc                     @ 0801ed28 dced0108
    .word  0x0801edd0                     @ 0801ed2c d0ed0108
    .word  0x0801edc2                     @ 0801ed30 c2ed0108
    .word  0x0801edc2                     @ 0801ed34 c2ed0108
    .word  0x0801edc2                     @ 0801ed38 c2ed0108
    .word  0x0801edc2                     @ 0801ed3c c2ed0108
    .word  0x0801ef60                     @ 0801ed40 60ef0108
    .word  0x0801ef38                     @ 0801ed44 38ef0108
    .word  0x0801edc2                     @ 0801ed48 c2ed0108
    .word  0x0801ef60                     @ 0801ed4c 60ef0108
    .word  0x0801ef4e                     @ 0801ed50 4eef0108
    .word  0x0801ef60                     @ 0801ed54 60ef0108
    .word  0x0801ef84                     @ 0801ed58 84ef0108
    .word  0x0801edc2                     @ 0801ed5c c2ed0108
    .word  0x0801edc2                     @ 0801ed60 c2ed0108
    .word  0x0801edc2                     @ 0801ed64 c2ed0108
    .word  0x0801edc2                     @ 0801ed68 c2ed0108
    .word  0x0801edc2                     @ 0801ed6c c2ed0108
    .word  0x0801edc2                     @ 0801ed70 c2ed0108
    .word  0x0801edc2                     @ 0801ed74 c2ed0108
    .word  0x0801ef60                     @ 0801ed78 60ef0108
    .word  0x0801ef60                     @ 0801ed7c 60ef0108
    .word  0x0801ef60                     @ 0801ed80 60ef0108
    .word  0x0801ee2a                     @ 0801ed84 2aee0108
    .word  0x0801ee40                     @ 0801ed88 40ee0108
    .word  0x0801ef60                     @ 0801ed8c 60ef0108
    .word  0x0801ef60                     @ 0801ed90 60ef0108
    .word  0x0801edc2                     @ 0801ed94 c2ed0108
    .word  0x0801ef84                     @ 0801ed98 84ef0108
    .word  0x0801ef60                     @ 0801ed9c 60ef0108
    .word  0x0801ef60                     @ 0801eda0 60ef0108
    .word  0x0801edc2                     @ 0801eda4 c2ed0108
    .word  0x0801ef60                     @ 0801eda8 60ef0108
    .word  0x0801ef60                     @ 0801edac 60ef0108
    .word  0x0801ef60                     @ 0801edb0 60ef0108
    .word  0x0801ef60                     @ 0801edb4 60ef0108
switchD_0801ecbc__caseD_18:
    adds r0,r6,#0x0    @ 0801edb8 301c
    adds r1,r7,#0x0    @ 0801edba 391c
    adds r2,r4,#0x0    @ 0801edbc 221c
    bl init_field_slot_aob_ctx_d             @ 0801edbe a5f08ff9
switchD_0801ecbc__caseD_a:
    movs r0,#0x1    @ 0801edc2 0120
    b LAB_0801ef86                           @ 0801edc4 dfe0
switchD_0801ecbc__caseD_19:
    adds r0,r7,#0x0    @ 0801edc6 381c
    adds r1,r4,#0x0    @ 0801edc8 211c
    bl init_field_slot_aob_ctx_c             @ 0801edca a6f069f8
    b switchD_0801ecbc__caseD_a              @ 0801edce f8e7
switchD_0801ecbc__caseD_1b:
    adds r0,r6,#0x0    @ 0801edd0 301c
    adds r1,r7,#0x0    @ 0801edd2 391c
    adds r2,r4,#0x0    @ 0801edd4 221c
    bl render_field_slot_card_tile_by_id     @ 0801edd6 a5f0a9f9
    b switchD_0801ecbc__caseD_a              @ 0801edda f2e7
switchD_0801ecbc__caseD_1a:
    adds r0,r6,#0x0    @ 0801eddc 301c
    adds r1,r7,#0x0    @ 0801edde 391c
    bl init_field_slot_ctx_zoom              @ 0801ede0 a4f08eff
    b switchD_0801ecbc__caseD_a              @ 0801ede4 ede7
switchD_0801ecbc__caseD_14:
    lsls r5,r6,#0x10    @ 0801ede6 3504
    lsrs r5,r5,#0x10    @ 0801ede8 2d0c
    lsls r4,r7,#0x10    @ 0801edea 3c04
    lsrs r4,r4,#0x10    @ 0801edec 240c
    adds r0,r6,#0x0    @ 0801edee 301c
    adds r1,r7,#0x0    @ 0801edf0 391c
    bl get_player_lp_by_field_type           @ 0801edf2 75f041fc
    adds r2,r0,#0x0    @ 0801edf6 021c
    lsls r2,r2,#0x10    @ 0801edf8 1204
    lsrs r2,r2,#0x10    @ 0801edfa 120c
    adds r0,r5,#0x0    @ 0801edfc 281c
    adds r1,r4,#0x0    @ 0801edfe 211c
    bl render_field_zone_card_tile_by_type   @ 0801ee00 a4f0fcfd
    b switchD_0801ecbc__caseD_a              @ 0801ee04 dde7
switchD_0801ecbc__caseD_9:
    bl build_slot_activation_mask_for_player @ 0801ee06 a9f0f3fe
    adds r0,r6,#0x0    @ 0801ee0a 301c
    bl write_field_slot_activation_mask      @ 0801ee0c a3f018fd
    b switchD_0801ecbc__caseD_a              @ 0801ee10 d7e7
switchD_0801ecbc__caseD_c:
    adds r0,r6,#0x0    @ 0801ee12 301c
    adds r1,r7,#0x0    @ 0801ee14 391c
    adds r2,r4,#0x0    @ 0801ee16 221c
    bl write_zone_oam_entry_with_flip        @ 0801ee18 a3f080fd
    b switchD_0801ecbc__caseD_a              @ 0801ee1c d1e7
switchD_0801ecbc__caseD_b:
    adds r0,r6,#0x0    @ 0801ee1e 301c
    adds r1,r7,#0x0    @ 0801ee20 391c
    adds r2,r4,#0x0    @ 0801ee22 221c
    bl init_field_slot_aob_ctx_b             @ 0801ee24 a3f02cfd
    b switchD_0801ecbc__caseD_a              @ 0801ee28 cbe7
switchD_0801ecbc__caseD_31:
    adds r0,r6,#0x0    @ 0801ee2a 301c
    adds r1,r7,#0x0    @ 0801ee2c 391c
    adds r2,r4,#0x0    @ 0801ee2e 221c
    bl copy_game_text_to_card_name_vram      @ 0801ee30 a8f08efd
    b switchD_0801ecbc__caseD_a              @ 0801ee34 c5e7
switchD_0801ecbc__caseD_d:
    adds r0,r6,#0x0    @ 0801ee36 301c
    adds r1,r7,#0x0    @ 0801ee38 391c
    bl write_lp_digit_tiles_to_vram          @ 0801ee3a abf0ddfb
    b switchD_0801ecbc__caseD_a              @ 0801ee3e c0e7
switchD_0801ecbc__caseD_32:
    adds r0,r7,#0x0    @ 0801ee40 381c
    bl build_field_zone_display_state        @ 0801ee42 adf089f8
    b switchD_0801ecbc__caseD_8              @ 0801ee46 9de0
switchD_0801ecbc__caseD_3:
    bl get_lp_display_anim_counter           @ 0801ee48 77f094fd
    cmp r0,#0x1                              @ 0801ee4c 0128
    bne LAB_0801ee60                         @ 0801ee4e 07d1
    ldr r0, DAT_0801ee5c                     @ 0801ee50 0248
    ldr r0,[r0,#0x4]                         @ 0801ee52 4068
    movs r1,#0xd    @ 0801ee54 0d21
    movs r2,#0x0    @ 0801ee56 0022
    b LAB_0801ef48                           @ 0801ee58 76e0
    .zero  0x2
DAT_0801ee5c:
    .word  0x0201e2a0                     @ 0801ee5c a0e20102
LAB_0801ee60:
    movs r7,#0x0    @ 0801ee60 0027
    movs r0,#0x80    @ 0801ee62 8020
    lsls r0,r0,#0x4    @ 0801ee64 0001
    .hword 0x4680    @ 0801ee66 8046
    movs r1,#0x1    @ 0801ee68 0121
    .hword 0x468a    @ 0801ee6a 8a46
    ldr r2, DAT_0801eed4                     @ 0801ee6c 194a
    .hword 0x4691    @ 0801ee6e 9146
LAB_0801ee70:
    ldr r0, DAT_0801eed8                     @ 0801ee70 1948
    ldr r5,[r0,#0x4]                         @ 0801ee72 4568
    eors r5,r7    @ 0801ee74 7d40
    movs r4,#0x0    @ 0801ee76 0024
LAB_0801ee78:
    adds r0,r5,#0x0    @ 0801ee78 281c
    adds r1,r4,#0x0    @ 0801ee7a 211c
    movs r2,#0x0    @ 0801ee7c 0022
    bl dispatch_zone_activation_by_state     @ 0801ee7e 77f05dfe
    .hword 0x4641    @ 0801ee82 4146
    ands r0,r1    @ 0801ee84 0840
    cmp r0,#0x0                              @ 0801ee86 0028
    bne LAB_0801ef6c                         @ 0801ee88 70d1
    adds r4,#0x1    @ 0801ee8a 0134
    cmp r4,#0xa                              @ 0801ee8c 0a2c
    ble LAB_0801ee78                         @ 0801ee8e f3dd
    movs r4,#0x0    @ 0801ee90 0024
    adds r0,r5,#0x0    @ 0801ee92 281c
    .hword 0x4652    @ 0801ee94 5246
    ands r0,r2    @ 0801ee96 1040
    ldr r1, DAT_0801eedc                     @ 0801ee98 1049
    muls r1,r0    @ 0801ee9a 4143
    ldr r2, DAT_0801eee0                     @ 0801ee9c 104a
    adds r0,r1,r2    @ 0801ee9e 8818
    ldr r0,[r0,#0x0]                         @ 0801eea0 0068
    cmp r4,r0                                @ 0801eea2 8442
    bcs LAB_0801eec4                         @ 0801eea4 0ed2
    adds r0,r2,#0x0    @ 0801eea6 101c
    adds r6,r1,r0    @ 0801eea8 0e18
LAB_0801eeaa:
    adds r0,r5,#0x0    @ 0801eeaa 281c
    movs r1,#0xb    @ 0801eeac 0b21
    adds r2,r4,#0x0    @ 0801eeae 221c
    bl dispatch_zone_activation_by_state     @ 0801eeb0 77f044fe
    .hword 0x4641    @ 0801eeb4 4146
    ands r0,r1    @ 0801eeb6 0840
    cmp r0,#0x0                              @ 0801eeb8 0028
    bne LAB_0801ef74                         @ 0801eeba 5bd1
    adds r4,#0x1    @ 0801eebc 0134
    ldr r0,[r6,#0x0]                         @ 0801eebe 3068
    cmp r4,r0                                @ 0801eec0 8442
    bcc LAB_0801eeaa                         @ 0801eec2 f2d3
LAB_0801eec4:
    lsls r0,r5,#0x2    @ 0801eec4 a800
    add r0,r9                                @ 0801eec6 4844
    movs r1,#0x0    @ 0801eec8 0021
    str r1,[r0,#0x0]                         @ 0801eeca 0160
    adds r7,#0x1    @ 0801eecc 0137
    cmp r7,#0x1                              @ 0801eece 012f
    ble LAB_0801ee70                         @ 0801eed0 cedd
    b switchD_0801ecbc__caseD_a              @ 0801eed2 76e7
DAT_0801eed4:
    .word  0x020230f0                     @ 0801eed4 f0300202
DAT_0801eed8:
    .word  0x0201e2a0                     @ 0801eed8 a0e20102
DAT_0801eedc:
    .word  0x00000868                     @ 0801eedc 68080000
DAT_0801eee0:
    .word  0x0201c4ec                     @ 0801eee0 ecc40102
switchD_0801ecbc__caseD_6:
    adds r0,r6,#0x0    @ 0801eee4 301c
    bl init_card_effect_aob_ctx              @ 0801eee6 aaf02ff8
    b switchD_0801ecbc__caseD_a              @ 0801eeea 6ae7
switchD_0801ecbc__caseD_11:
    ldr r2, DAT_0801ef1c                     @ 0801eeec 0b4a
    lsls r1,r7,#0x1    @ 0801eeee 7900
    lsls r0,r6,#0x2    @ 0801eef0 b000
    adds r0,r0,r6    @ 0801eef2 8019
    lsls r0,r0,#0x5    @ 0801eef4 4001
    adds r1,r1,r0    @ 0801eef6 0918
    adds r0,r2,#0x0    @ 0801eef8 101c
    adds r0,#0x50    @ 0801eefa 5030
    adds r1,r1,r0    @ 0801eefc 0918
    movs r0,#0x1    @ 0801eefe 0120
    strh r0,[r1,#0x0]                        @ 0801ef00 0880
    lsls r0,r6,#0x1    @ 0801ef02 7000
    adds r2,#0x4c    @ 0801ef04 4c32
    adds r0,r0,r2    @ 0801ef06 8018
    ldrh r1,[r0,#0x0]                        @ 0801ef08 0188
    adds r0,r6,#0x0    @ 0801ef0a 301c
    bl refresh_player_field_slot_tiles       @ 0801ef0c a5f088f9
    bl update_zone_oam_card_count_tag        @ 0801ef10 a7f03cfc
    bl refresh_duel_field_zone_info          @ 0801ef14 acf0faff
    b switchD_0801ecbc__caseD_1              @ 0801ef18 22e0
    .zero  0x2
DAT_0801ef1c:
    .word  0x02023130                     @ 0801ef1c 30310202
switchD_0801ecbc__caseD_12:
    ldr r0, DAT_0801ef34                     @ 0801ef20 0448
    lsls r1,r6,#0x1    @ 0801ef22 7100
    adds r0,#0x4c    @ 0801ef24 4c30
    adds r1,r1,r0    @ 0801ef26 0918
    ldrh r1,[r1,#0x0]                        @ 0801ef28 0988
    adds r0,r6,#0x0    @ 0801ef2a 301c
    bl refresh_player_field_slot_tiles       @ 0801ef2c a5f078f9
    b switchD_0801ecbc__caseD_a              @ 0801ef30 47e7
    .zero  0x2
DAT_0801ef34:
    .word  0x02023130                     @ 0801ef34 30310202
switchD_0801ecbc__caseD_21:
    adds r0,r6,#0x0    @ 0801ef38 301c
    adds r1,r7,#0x0    @ 0801ef3a 391c
    adds r2,r4,#0x0    @ 0801ef3c 221c
    bl init_field_slot_aob_ctx_a             @ 0801ef3e 9df029fc
switchD_0801ecbc__caseD_7:
    adds r0,r6,#0x0    @ 0801ef42 301c
    adds r1,r7,#0x0    @ 0801ef44 391c
    adds r2,r4,#0x0    @ 0801ef46 221c
LAB_0801ef48:
    bl write_zone_slot_oam_descriptor        @ 0801ef48 a7f06afd
    b switchD_0801ecbc__caseD_a              @ 0801ef4c 39e7
switchD_0801ecbc__caseD_24:
    bl refresh_duel_field_zone_info          @ 0801ef4e acf0ddff
    bl refresh_zone_effect_buff_cache        @ 0801ef52 a9f0edfe
    bl build_slot_activation_mask_for_player @ 0801ef56 a9f04bfe
    bl refresh_all_zone_slot_tile_display    @ 0801ef5a a9f0d3fc
    b switchD_0801ecbc__caseD_a              @ 0801ef5e 30e7
switchD_0801ecbc__caseD_1:
    adds r0,r6,#0x0    @ 0801ef60 301c
    adds r1,r7,#0x0    @ 0801ef62 391c
    adds r2,r4,#0x0    @ 0801ef64 221c
    bl init_field_slot_aob_ctx_a             @ 0801ef66 9df015fc
    b switchD_0801ecbc__caseD_a              @ 0801ef6a 2ae7
LAB_0801ef6c:
    adds r0,r5,#0x0    @ 0801ef6c 281c
    adds r1,r4,#0x0    @ 0801ef6e 211c
    movs r2,#0x0    @ 0801ef70 0022
    b LAB_0801ef7a                           @ 0801ef72 02e0
LAB_0801ef74:
    adds r0,r5,#0x0    @ 0801ef74 281c
    movs r1,#0xb    @ 0801ef76 0b21
    adds r2,r4,#0x0    @ 0801ef78 221c
LAB_0801ef7a:
    bl write_zone_slot_oam_descriptor        @ 0801ef7a a7f051fd
    bl update_zone_activation_display_state  @ 0801ef7e a9f033fd
    b switchD_0801ecbc__caseD_a              @ 0801ef82 1ee7
switchD_0801ecbc__caseD_8:
    movs r0,#0x0    @ 0801ef84 0020
LAB_0801ef86:
    pop {r3,r4,r5}                           @ 0801ef86 38bc
    .hword 0x4698    @ 0801ef88 9846
    .hword 0x46a1    @ 0801ef8a a146
    .hword 0x46aa    @ 0801ef8c aa46
    pop {r4,r5,r6,r7}                        @ 0801ef8e f0bc
    pop {r1}                                 @ 0801ef90 02bc
    bx r1                                    @ 0801ef92 0847

@ UI 特效派发器 (per-frame tick). r0 = effect_id (0..0x3d), 按 ID 分派到 ~28 个独立的 effect handler 子状态机, busy/done 返回. dispatch table 中 重复 fallthrough 到 default 的 case = 未实现/无效 ID. 已识别 effect: 0x01 = banner_anim_state_machine (pack 横幅出/入场), 0x1a = play_card_zoom_in (小图→大图缩放过渡), 0x3c = play_demo_shuen (终焉过场). 其他 case 子函数批量占位为 play_ui_effect_<id_hex>, 待详细分析. cmp 上限 0x3d, 大于则 default. case 0/0x18/0x19 共享 caseD_0 (state-bit 检查后选 FUN_080c4edc 或 FUN_080c4350); case 1 状态化 (banner_anim 或 FUN_080be600); case 2 三向状态分派. case 0x31/0x32 内联无 bl (特殊 readback).
play_ui_effect:
    push {lr}                                @ 0801ef94 00b5
    cmp r0,#0x3d                             @ 0801ef96 3d28
    bls LAB_0801ef9c                         @ 0801ef98 00d9
    b switchD_0801efa4__caseD_7              @ 0801ef9a 4ae1
LAB_0801ef9c:
    lsls r0,r0,#0x2    @ 0801ef9c 8000
    ldr r1, DAT_0801efa8                     @ 0801ef9e 0249
    adds r0,r0,r1    @ 0801efa0 4018
    ldr r0,[r0,#0x0]                         @ 0801efa2 0068
switchD_0801efa4__switchD:
    .hword 0x4687    @ 0801efa4 8746
    .zero  0x2
DAT_0801efa8:
    .word  0x0801efac                     @ 0801efa8 acef0108
switchD_0801efa4__switchdataD_0801efac:
    .word  0x0801f0a4                     @ 0801efac a4f00108
    .word  0x0801f13e                     @ 0801efb0 3ef10108
    .word  0x0801f162                     @ 0801efb4 62f10108
    .word  0x0801f0cc                     @ 0801efb8 ccf00108
    .word  0x0801f138                     @ 0801efbc 38f10108
    .word  0x0801f132                     @ 0801efc0 32f10108
    .word  0x0801f12c                     @ 0801efc4 2cf10108
    .word  0x0801f232                     @ 0801efc8 32f20108
    .word  0x0801f232                     @ 0801efcc 32f20108
    .word  0x0801f232                     @ 0801efd0 32f20108
    .word  0x0801f232                     @ 0801efd4 32f20108
    .word  0x0801f1ea                     @ 0801efd8 eaf10108
    .word  0x0801f1e4                     @ 0801efdc e4f10108
    .word  0x0801f232                     @ 0801efe0 32f20108
    .word  0x0801f10e                     @ 0801efe4 0ef10108
    .word  0x0801f232                     @ 0801efe8 32f20108
    .word  0x0801f0d8                     @ 0801efec d8f00108
    .word  0x0801f0de                     @ 0801eff0 def00108
    .word  0x0801f232                     @ 0801eff4 32f20108
    .word  0x0801f1de                     @ 0801eff8 def10108
    .word  0x0801f232                     @ 0801effc 32f20108
    .word  0x0801f0d2                     @ 0801f000 d2f00108
    .word  0x0801f232                     @ 0801f004 32f20108
    .word  0x0801f21a                     @ 0801f008 1af20108
    .word  0x0801f0a4                     @ 0801f00c a4f00108
    .word  0x0801f0a4                     @ 0801f010 a4f00108
    .word  0x0801f108                     @ 0801f014 08f10108
    .word  0x0801f232                     @ 0801f018 32f20108
    .word  0x0801f232                     @ 0801f01c 32f20108
    .word  0x0801f232                     @ 0801f020 32f20108
    .word  0x0801f232                     @ 0801f024 32f20108
    .word  0x0801f232                     @ 0801f028 32f20108
    .word  0x0801f1c6                     @ 0801f02c c6f10108
    .word  0x0801f1cc                     @ 0801f030 ccf10108
    .word  0x0801f232                     @ 0801f034 32f20108
    .word  0x0801f1d2                     @ 0801f038 d2f10108
    .word  0x0801f232                     @ 0801f03c 32f20108
    .word  0x0801f1d8                     @ 0801f040 d8f10108
    .word  0x0801f232                     @ 0801f044 32f20108
    .word  0x0801f232                     @ 0801f048 32f20108
    .word  0x0801f232                     @ 0801f04c 32f20108
    .word  0x0801f232                     @ 0801f050 32f20108
    .word  0x0801f232                     @ 0801f054 32f20108
    .word  0x0801f232                     @ 0801f058 32f20108
    .word  0x0801f232                     @ 0801f05c 32f20108
    .word  0x0801f232                     @ 0801f060 32f20108
    .word  0x0801f226                     @ 0801f064 26f20108
    .word  0x0801f220                     @ 0801f068 20f20108
    .word  0x0801f1c0                     @ 0801f06c c0f10108
    .word  0x0801f0e4                     @ 0801f070 e4f00108
    .word  0x0801f114                     @ 0801f074 14f10108
    .word  0x0801f1f0                     @ 0801f078 f0f10108
    .word  0x0801f1f6                     @ 0801f07c f6f10108
    .word  0x0801f232                     @ 0801f080 32f20108
    .word  0x0801f232                     @ 0801f084 32f20108
    .word  0x0801f1fc                     @ 0801f088 fcf10108
    .word  0x0801f202                     @ 0801f08c 02f20108
    .word  0x0801f232                     @ 0801f090 32f20108
    .word  0x0801f208                     @ 0801f094 08f20108
    .word  0x0801f20e                     @ 0801f098 0ef20108
    .word  0x0801f214                     @ 0801f09c 14f20108
    .word  0x0801f22c                     @ 0801f0a0 2cf20108
switchD_0801efa4__caseD_0:
    ldr r0, DAT_0801f0b8                     @ 0801f0a4 0448
    ldrb r1,[r0,#0x19]                       @ 0801f0a6 417e
    movs r0,#0x2    @ 0801f0a8 0220
    ands r0,r1    @ 0801f0aa 0840
    cmp r0,#0x0                              @ 0801f0ac 0028
    beq LAB_0801f0bc                         @ 0801f0ae 05d0
    bl run_ui_effect_card_pair_state_machine @ 0801f0b0 a5f014ff
    b LAB_0801f234                           @ 0801f0b4 bee0
    .zero  0x2
DAT_0801f0b8:
    .word  gUIEffectState                 @ 0801f0b8 10310202
LAB_0801f0bc:
    movs r0,#0x1    @ 0801f0bc 0120
    ands r0,r1    @ 0801f0be 0840
    cmp r0,#0x0                              @ 0801f0c0 0028
    bne LAB_0801f0c6                         @ 0801f0c2 00d1
    b switchD_0801efa4__caseD_7              @ 0801f0c4 b5e0
LAB_0801f0c6:
    bl dispatch_ui_effect_by_card_type       @ 0801f0c6 a5f043f9
    b LAB_0801f234                           @ 0801f0ca b3e0
switchD_0801efa4__caseD_3:
    bl play_ui_effect_03                     @ 0801f0cc adf0d8fc
    b LAB_0801f234                           @ 0801f0d0 b0e0
switchD_0801efa4__caseD_15:
    bl play_ui_effect_15                     @ 0801f0d2 9ff0dffc
    b LAB_0801f234                           @ 0801f0d6 ade0
switchD_0801efa4__caseD_10:
    bl play_ui_effect_10                     @ 0801f0d8 a3f068fa
    b LAB_0801f234                           @ 0801f0dc aae0
switchD_0801efa4__caseD_11:
    bl play_ui_effect_11                     @ 0801f0de a0f0a3f8
    b LAB_0801f234                           @ 0801f0e2 a7e0
switchD_0801efa4__caseD_31:
    ldr r0, DAT_0801f0fc                     @ 0801f0e4 0548
    ldrb r0,[r0,#0x0]                        @ 0801f0e6 0078
    lsls r1,r0,#0x1f    @ 0801f0e8 c107
    ldr r0, DAT_0801f100                     @ 0801f0ea 0548
    ldr r2, DAT_0801f104                     @ 0801f0ec 054a
    adds r0,r0,r2    @ 0801f0ee 8018
    ldrb r0,[r0,#0x0]                        @ 0801f0f0 0078
    lsls r0,r0,#0x1f    @ 0801f0f2 c007
    orrs r0,r1    @ 0801f0f4 0843
    lsrs r0,r0,#0x1f    @ 0801f0f6 c00f
    b LAB_0801f234                           @ 0801f0f8 9ce0
    .zero  0x2
DAT_0801f0fc:
    .word  0x0201f440                     @ 0801f0fc 40f40102
DAT_0801f100:
    .word  0x02020160                     @ 0801f100 60010202
DAT_0801f104:
    .word  0x00002f51                     @ 0801f104 512f0000
switchD_0801efa4__caseD_1a:
    bl play_card_zoom_in                     @ 0801f108 a4f00afe
    b LAB_0801f234                           @ 0801f10c 92e0
switchD_0801efa4__caseD_e:
    bl play_ui_effect_0e                     @ 0801f10e a0f041f9
    b LAB_0801f234                           @ 0801f112 8fe0
switchD_0801efa4__caseD_32:
    ldr r0, DAT_0801f124                     @ 0801f114 0348
    ldr r1, DAT_0801f128                     @ 0801f116 0449
    adds r0,r0,r1    @ 0801f118 4018
    ldrb r0,[r0,#0x0]                        @ 0801f11a 0078
    lsls r0,r0,#0x1f    @ 0801f11c c007
    lsrs r0,r0,#0x1f    @ 0801f11e c00f
    b LAB_0801f234                           @ 0801f120 88e0
    .zero  0x2
DAT_0801f124:
    .word  0x02020160                     @ 0801f124 60010202
DAT_0801f128:
    .word  0x00002f51                     @ 0801f128 512f0000
switchD_0801efa4__caseD_6:
    bl play_ui_effect_06                     @ 0801f12c aaf058f8
    b LAB_0801f234                           @ 0801f130 80e0
switchD_0801efa4__caseD_5:
    bl play_ui_effect_05                     @ 0801f132 a0f06bfe
    b LAB_0801f234                           @ 0801f136 7de0
switchD_0801efa4__caseD_4:
    bl play_ui_effect_04                     @ 0801f138 9ef0e0fd
    b LAB_0801f234                           @ 0801f13c 7ae0
switchD_0801efa4__caseD_1:
    ldr r1, PTR_gPrng_0801f154               @ 0801f13e 0549
    ldr r2, DAT_0801f158                     @ 0801f140 054a
    adds r1,r1,r2    @ 0801f142 8918
    movs r0,#0x1    @ 0801f144 0120
    ldrb r1,[r1,#0x0]                        @ 0801f146 0978
    ands r0,r1    @ 0801f148 0840
    cmp r0,#0x0                              @ 0801f14a 0028
    beq LAB_0801f15c                         @ 0801f14c 06d0
    bl banner_anim_state_machine             @ 0801f14e 9ef02dff
    b LAB_0801f234                           @ 0801f152 6fe0
PTR_gPrng_0801f154:
    .word  gPrng                          @ 0801f154 40000003
DAT_0801f158:
    .word  0x0000023f                     @ 0801f158 3f020000
LAB_0801f15c:
    bl tick_banner_pack_state_machine        @ 0801f15c 9ff050fa
    b LAB_0801f234                           @ 0801f160 68e0
switchD_0801efa4__caseD_2:
    ldr r1, DAT_0801f184                     @ 0801f162 0849
    movs r2,#0x1    @ 0801f164 0122
    adds r0,r2,#0x0    @ 0801f166 101c
    ldrb r1,[r1,#0x0]                        @ 0801f168 0978
    ands r0,r1    @ 0801f16a 0840
    cmp r0,#0x0                              @ 0801f16c 0028
    bne LAB_0801f180                         @ 0801f16e 07d1
    ldr r1, DAT_0801f188                     @ 0801f170 0549
    ldr r0, DAT_0801f18c                     @ 0801f172 0648
    adds r1,r1,r0    @ 0801f174 0918
    adds r0,r2,#0x0    @ 0801f176 101c
    ldrb r1,[r1,#0x0]                        @ 0801f178 0978
    ands r0,r1    @ 0801f17a 0840
    cmp r0,#0x0                              @ 0801f17c 0028
    beq LAB_0801f190                         @ 0801f17e 07d0
LAB_0801f180:
    movs r0,#0x1    @ 0801f180 0120
    b LAB_0801f234                           @ 0801f182 57e0
DAT_0801f184:
    .word  0x0201f440                     @ 0801f184 40f40102
DAT_0801f188:
    .word  0x02020160                     @ 0801f188 60010202
DAT_0801f18c:
    .word  0x00002f51                     @ 0801f18c 512f0000
LAB_0801f190:
    ldr r0, DAT_0801f1a4                     @ 0801f190 0448
    ldr r0,[r0,#0x4]                         @ 0801f192 4068
    cmp r0,#0x2                              @ 0801f194 0228
    beq LAB_0801f1b4                         @ 0801f196 0dd0
    cmp r0,#0x2                              @ 0801f198 0228
    bgt LAB_0801f1a8                         @ 0801f19a 05dc
    cmp r0,#0x1                              @ 0801f19c 0128
    beq LAB_0801f1ae                         @ 0801f19e 06d0
    b switchD_0801efa4__caseD_7              @ 0801f1a0 47e0
    .zero  0x2
DAT_0801f1a4:
    .word  gBannerState                   @ 0801f1a4 c0fe0102
LAB_0801f1a8:
    cmp r0,#0x3                              @ 0801f1a8 0328
    beq LAB_0801f1ba                         @ 0801f1aa 06d0
    b switchD_0801efa4__caseD_7              @ 0801f1ac 41e0
LAB_0801f1ae:
    bl dispatch_banner_scene_tick_by_state   @ 0801f1ae 9df07bff
    b LAB_0801f234                           @ 0801f1b2 3fe0
LAB_0801f1b4:
    bl tick_banner_display_state_machine     @ 0801f1b4 9ef01ef9
    b LAB_0801f234                           @ 0801f1b8 3ce0
LAB_0801f1ba:
    bl tick_duel_puzzle_banner_state_machine @ 0801f1ba 9ef051fa
    b LAB_0801f234                           @ 0801f1be 39e0
switchD_0801efa4__caseD_30:
    bl play_ui_effect_30                     @ 0801f1c0 9ef056fb
    b LAB_0801f234                           @ 0801f1c4 36e0
switchD_0801efa4__caseD_20:
    bl play_ui_effect_20                     @ 0801f1c6 a1f053fd
    b LAB_0801f234                           @ 0801f1ca 33e0
switchD_0801efa4__caseD_21:
    bl play_ui_effect_21                     @ 0801f1cc a1f0b4fe
    b LAB_0801f234                           @ 0801f1d0 30e0
switchD_0801efa4__caseD_23:
    bl play_ui_effect_23                     @ 0801f1d2 a2f0fffa
    b LAB_0801f234                           @ 0801f1d6 2de0
switchD_0801efa4__caseD_25:
    bl play_ui_effect_25                     @ 0801f1d8 a2f036f9
    b LAB_0801f234                           @ 0801f1dc 2ae0
switchD_0801efa4__caseD_13:
    bl play_ui_effect_13                     @ 0801f1de a2f077fc
    b LAB_0801f234                           @ 0801f1e2 27e0
switchD_0801efa4__caseD_c:
    bl play_ui_effect_0c                     @ 0801f1e4 a3f04cff
    b LAB_0801f234                           @ 0801f1e8 24e0
switchD_0801efa4__caseD_b:
    bl play_ui_effect_0b                     @ 0801f1ea a3f06ffc
    b LAB_0801f234                           @ 0801f1ee 21e0
switchD_0801efa4__caseD_33:
    bl play_ui_effect_33                     @ 0801f1f0 a1f0f8fa
    b LAB_0801f234                           @ 0801f1f4 1ee0
switchD_0801efa4__caseD_34:
    bl play_ui_effect_34                     @ 0801f1f6 a1f043fc
    b LAB_0801f234                           @ 0801f1fa 1be0
switchD_0801efa4__caseD_37:
    bl play_ui_effect_37                     @ 0801f1fc a0f0fcfa
    b LAB_0801f234                           @ 0801f200 18e0
switchD_0801efa4__caseD_38:
    bl play_ui_effect_38                     @ 0801f202 a0f0cdf9
    b LAB_0801f234                           @ 0801f206 15e0
switchD_0801efa4__caseD_3a:
    bl play_ui_effect_3a                     @ 0801f208 9df0e4fc
    b LAB_0801f234                           @ 0801f20c 12e0
switchD_0801efa4__caseD_3b:
    bl play_ui_effect_3b                     @ 0801f20e 9df083fb
    b LAB_0801f234                           @ 0801f212 0fe0
switchD_0801efa4__caseD_3c:
    bl play_demo_shuen                       @ 0801f214 9df034fb
    b LAB_0801f234                           @ 0801f218 0ce0
switchD_0801efa4__caseD_17:
    bl play_ui_effect_17                     @ 0801f21a 9ff0d1fe
    b LAB_0801f234                           @ 0801f21e 09e0
switchD_0801efa4__caseD_2f:
    bl play_ui_effect_2f                     @ 0801f220 a2f03cfe
    b LAB_0801f234                           @ 0801f224 06e0
switchD_0801efa4__caseD_2e:
    bl play_ui_effect_2e                     @ 0801f226 a2f01bfd
    b LAB_0801f234                           @ 0801f22a 03e0
switchD_0801efa4__caseD_3d:
    bl play_ui_effect_3d                     @ 0801f22c a3f08af9
    b LAB_0801f234                           @ 0801f230 00e0
switchD_0801efa4__caseD_7:
    movs r0,#0x0    @ 0801f232 0020
LAB_0801f234:
    pop {r1}                                 @ 0801f234 02bc
    bx r1                                    @ 0801f236 0847

@ Copies a game string to dest buf r0: if r1 is a raw string ID (high 15 bits == 0, mask 0xFFFE0000 & r1 == 0) calls resolve_game_str_ptr(r1) then strcpy; otherwise uses r1 directly as pointer for strcpy. r0=u8* dest; r1=u32 str_handle (raw ID or resolved ptr). Returns void. Side effects: writes NUL-terminated string to [r0..]. Constants: RAW_ID_MASK=0xFFFE0000.
copy_game_text_if_raw:
    push {r4,lr}                             @ 0801f238 10b5
    adds r4,r0,#0x0    @ 0801f23a 041c
    ldr r0, DAT_0801f258                     @ 0801f23c 0648
    ands r0,r1    @ 0801f23e 0840
    cmp r0,#0x0                              @ 0801f240 0028
    bne LAB_0801f24c                         @ 0801f242 03d1
    adds r0,r1,#0x0    @ 0801f244 081c
    bl resolve_game_str_ptr                  @ 0801f246 cff005fd
    adds r1,r0,#0x0    @ 0801f24a 011c
LAB_0801f24c:
    adds r0,r4,#0x0    @ 0801f24c 201c
    bl strcpy                                @ 0801f24e eff01fff
    pop {r4}                                 @ 0801f252 10bc
    pop {r0}                                 @ 0801f254 01bc
    bx r0                                    @ 0801f256 0047
DAT_0801f258:
    .word  0xfffe0000                     @ 0801f258 0000feff

@ Appends a game string to end of dest buf r0 (strcat variant of copy_game_text_if_raw). If r1 high 15 bits == 0 calls resolve_game_str_ptr(r1) then strcat; otherwise uses r1 directly as pointer for strcat. r0=u8* dest (existing content); r1=u32 str_handle. Returns void. Side effects: appends NUL-terminated string to [r0 end..]. Constants: RAW_ID_MASK=0xFFFE0000.
append_game_text_if_raw:
    push {r4,lr}                             @ 0801f25c 10b5
    adds r4,r0,#0x0    @ 0801f25e 041c
    ldr r0, DAT_0801f27c                     @ 0801f260 0648
    ands r0,r1    @ 0801f262 0840
    cmp r0,#0x0                              @ 0801f264 0028
    bne LAB_0801f270                         @ 0801f266 03d1
    adds r0,r1,#0x0    @ 0801f268 081c
    bl resolve_game_str_ptr                  @ 0801f26a cff0f3fc
    adds r1,r0,#0x0    @ 0801f26e 011c
LAB_0801f270:
    adds r0,r4,#0x0    @ 0801f270 201c
    bl strcat                                @ 0801f272 eff0bbfe
    pop {r4}                                 @ 0801f276 10bc
    pop {r0}                                 @ 0801f278 01bc
    bx r0                                    @ 0801f27a 0047
DAT_0801f27c:
    .word  0xfffe0000                     @ 0801f27c 0000feff

@ Called by format_game_text_with_int_arg (0x0801f338, game_str, indeg=1) when a "%d" format specifier (0x25/0x64) is detected. Inputs: r0=dest_buf (pointer to output buffer with existing prefix), r1=number (signed integer to format). Allocates a 16-byte temporary buffer on stack (sp+0..15); iterates number%10 to extract digits as ASCII (+'0'=0x30), number/10 to advance; writes digits backwards into sp+r6 (decrementing from index 15). After loop, calls append_game_text_if_raw(dest_buf, sp+digit_start) to append the result. Equivalent to itoa + strcat. Returns: void (exit via pop{r0};bx r0, return register not preserved). Side effects: appends decimal ASCII representation of number to end of dest_buf via append_game_text_if_raw. Constants: ascii_digit_base=0x30 ('0', digit-to-ASCII offset), buf_max_idx=0xf (15, max index of temp buffer = up to 15 digits), radix=10 (divisor and modulus).
format_int_to_decimal_text:
    push {r4,r5,r6,r7,lr}                    @ 0801f280 f0b5
    sub sp,#0x10                             @ 0801f282 84b0
    adds r7,r0,#0x0    @ 0801f284 071c
    adds r4,r1,#0x0    @ 0801f286 0c1c
    movs r6,#0xf    @ 0801f288 0f26
    .hword 0x4669    @ 0801f28a 6946
    adds r1,#0xf    @ 0801f28c 0f31
    movs r0,#0x0    @ 0801f28e 0020
    strb r0,[r1,#0x0]                        @ 0801f290 0870
LAB_0801f292:
    subs r6,#0x1    @ 0801f292 013e
    .hword 0x4668    @ 0801f294 6846
    adds r5,r0,r6    @ 0801f296 8519
    adds r0,r4,#0x0    @ 0801f298 201c
    movs r1,#0xa    @ 0801f29a 0a21
    bl __modsi3                              @ 0801f29c eff0fef9
    adds r0,#0x30    @ 0801f2a0 3030
    strb r0,[r5,#0x0]                        @ 0801f2a2 2870
    adds r0,r4,#0x0    @ 0801f2a4 201c
    movs r1,#0xa    @ 0801f2a6 0a21
    bl __divsi3                              @ 0801f2a8 eff0acf9
    adds r4,r0,#0x0    @ 0801f2ac 041c
    cmp r4,#0x0                              @ 0801f2ae 002c
    bne LAB_0801f292                         @ 0801f2b0 efd1
    adds r0,r7,#0x0    @ 0801f2b2 381c
    adds r1,r5,#0x0    @ 0801f2b4 291c
    bl append_game_text_if_raw               @ 0801f2b6 fff7d1ff
    add sp,#0x10                             @ 0801f2ba 04b0
    pop {r4,r5,r6,r7}                        @ 0801f2bc f0bc
    pop {r0}                                 @ 0801f2be 01bc
    bx r0                                    @ 0801f2c0 0047
    .zero  0x2

@ Replaces %s placeholder in format string r1 with string arg r2, writes result to dest buffer r0. If high 15 bits of r1 or r2 are 0 (no RAW_ID_MASK=0xfffe0000 tag), calls resolve_game_str_ptr to resolve game string ID to real pointer. Copies chars one by one; on %s truncates current position, calls append_game_text_if_raw to insert r2 content, then continues appending remaining format string. Used by 34 callers (C_util_high) as core UI text formatting utility for card/player name dynamic strings. Constants: RAW_ID_MASK=0xfffe0000 (high-15-bit mask distinguishing raw ID from real pointer).
format_game_text_with_text_arg:
    push {r4,r5,r6,r7,lr}                    @ 0801f2c4 f0b5
    adds r6,r2,#0x0    @ 0801f2c6 161c
    adds r4,r1,#0x0    @ 0801f2c8 0c1c
    adds r5,r0,#0x0    @ 0801f2ca 051c
    movs r0,#0x0    @ 0801f2cc 0020
    strb r0,[r5,#0x0]                        @ 0801f2ce 2870
    ldr r7, DAT_0801f2f8                     @ 0801f2d0 094f
    adds r0,r4,#0x0    @ 0801f2d2 201c
    ands r0,r7    @ 0801f2d4 3840
    cmp r0,#0x0                              @ 0801f2d6 0028
    bne LAB_0801f2e2                         @ 0801f2d8 03d1
    adds r0,r4,#0x0    @ 0801f2da 201c
    bl resolve_game_str_ptr                  @ 0801f2dc cff0bafc
    adds r4,r0,#0x0    @ 0801f2e0 041c
LAB_0801f2e2:
    adds r0,r6,#0x0    @ 0801f2e2 301c
    ands r0,r7    @ 0801f2e4 3840
    cmp r0,#0x0                              @ 0801f2e6 0028
    bne LAB_0801f2f2                         @ 0801f2e8 03d1
    adds r0,r6,#0x0    @ 0801f2ea 301c
    bl resolve_game_str_ptr                  @ 0801f2ec cff0b2fc
    adds r6,r0,#0x0    @ 0801f2f0 061c
LAB_0801f2f2:
    cmp r4,#0x0                              @ 0801f2f2 002c
    beq LAB_0801f330                         @ 0801f2f4 1cd0
    b LAB_0801f326                           @ 0801f2f6 16e0
DAT_0801f2f8:
    .word  0xfffe0000                     @ 0801f2f8 0000feff
LAB_0801f2fc:
    cmp r0,#0x25                             @ 0801f2fc 2528
    bne LAB_0801f31e                         @ 0801f2fe 0ed1
    ldrb r0,[r4,#0x1]                        @ 0801f300 6078
    cmp r0,#0x73                             @ 0801f302 7328
    bne LAB_0801f31e                         @ 0801f304 0bd1
    movs r0,#0x0    @ 0801f306 0020
    strb r0,[r5,#0x0]                        @ 0801f308 2870
    adds r4,#0x2    @ 0801f30a 0234
    adds r0,r5,#0x0    @ 0801f30c 281c
    adds r1,r6,#0x0    @ 0801f30e 311c
    bl append_game_text_if_raw               @ 0801f310 fff7a4ff
    adds r0,r5,#0x0    @ 0801f314 281c
    adds r1,r4,#0x0    @ 0801f316 211c
    bl append_game_text_if_raw               @ 0801f318 fff7a0ff
    b LAB_0801f330                           @ 0801f31c 08e0
LAB_0801f31e:
    ldrb r0,[r4,#0x0]                        @ 0801f31e 2078
    strb r0,[r5,#0x0]                        @ 0801f320 2870
    adds r4,#0x1    @ 0801f322 0134
    adds r5,#0x1    @ 0801f324 0135
LAB_0801f326:
    ldrb r0,[r4,#0x0]                        @ 0801f326 2078
    cmp r0,#0x0                              @ 0801f328 0028
    bne LAB_0801f2fc                         @ 0801f32a e7d1
    movs r0,#0x0    @ 0801f32c 0020
    strb r0,[r5,#0x0]                        @ 0801f32e 2870
LAB_0801f330:
    pop {r4,r5,r6,r7}                        @ 0801f330 f0bc
    pop {r0}                                 @ 0801f332 01bc
    bx r0                                    @ 0801f334 0047
    .zero  0x2

@ Called by 10 callers (D_shared_mid, indeg=10, game_str context) with r0=dest_buf, r1=format_id_or_ptr, r2=int_arg. If high 15 bits of r1 are 0 (r1 & 0xfffe0000==0), calls resolve_game_str_ptr to resolve game_str ID to real pointer; otherwise uses r1 directly as format string pointer. Initializes dest to empty string; scans format string char by char: on '%d' (0x25/0x64 two bytes) -> null-terminates current position, calls format_int_to_decimal_text(dest_end, r2), then calls append_game_text_if_raw to append remaining text; otherwise copies each byte to dest. Null-terminates dest at end. Equivalent to snprintf(dest, fmt, int_arg) single-integer variant. Returns: void (exit via pop{r0};bx r0). Side effects: dest_buf written with formatted result string (including null terminator). Constants: FMT_PERCENT=0x25 ('%'), FMT_D=0x64 ('d'), RAW_ID_MASK=0xfffe0000 (high 15 bits nonzero means real pointer, zero means game_str ID).
format_game_text_with_int_arg:
    push {r4,r5,r6,lr}                       @ 0801f338 70b5
    adds r6,r2,#0x0    @ 0801f33a 161c
    adds r4,r1,#0x0    @ 0801f33c 0c1c
    adds r5,r0,#0x0    @ 0801f33e 051c
    movs r0,#0x0    @ 0801f340 0020
    strb r0,[r5,#0x0]                        @ 0801f342 2870
    ldr r0, DAT_0801f358                     @ 0801f344 0448
    ands r0,r4    @ 0801f346 2040
    cmp r0,#0x0                              @ 0801f348 0028
    bne LAB_0801f386                         @ 0801f34a 1cd1
    adds r0,r4,#0x0    @ 0801f34c 201c
    bl resolve_game_str_ptr                  @ 0801f34e cff081fc
    adds r4,r0,#0x0    @ 0801f352 041c
    b LAB_0801f386                           @ 0801f354 17e0
    .zero  0x2
DAT_0801f358:
    .word  0xfffe0000                     @ 0801f358 0000feff
LAB_0801f35c:
    cmp r0,#0x25                             @ 0801f35c 2528
    bne LAB_0801f37e                         @ 0801f35e 0ed1
    ldrb r0,[r4,#0x1]                        @ 0801f360 6078
    cmp r0,#0x64                             @ 0801f362 6428
    bne LAB_0801f37e                         @ 0801f364 0bd1
    movs r0,#0x0    @ 0801f366 0020
    strb r0,[r5,#0x0]                        @ 0801f368 2870
    adds r4,#0x2    @ 0801f36a 0234
    adds r0,r5,#0x0    @ 0801f36c 281c
    adds r1,r6,#0x0    @ 0801f36e 311c
    bl format_int_to_decimal_text            @ 0801f370 fff786ff
    adds r0,r5,#0x0    @ 0801f374 281c
    adds r1,r4,#0x0    @ 0801f376 211c
    bl append_game_text_if_raw               @ 0801f378 fff770ff
    b LAB_0801f390                           @ 0801f37c 08e0
LAB_0801f37e:
    ldrb r0,[r4,#0x0]                        @ 0801f37e 2078
    strb r0,[r5,#0x0]                        @ 0801f380 2870
    adds r4,#0x1    @ 0801f382 0134
    adds r5,#0x1    @ 0801f384 0135
LAB_0801f386:
    ldrb r0,[r4,#0x0]                        @ 0801f386 2078
    cmp r0,#0x0                              @ 0801f388 0028
    bne LAB_0801f35c                         @ 0801f38a e7d1
    movs r0,#0x0    @ 0801f38c 0020
    strb r0,[r5,#0x0]                        @ 0801f38e 2870
LAB_0801f390:
    pop {r4,r5,r6}                           @ 0801f390 70bc
    pop {r0}                                 @ 0801f392 01bc
    bx r0                                    @ 0801f394 0047
    .zero  0x2

@ Called by FUN_08027f00 (campaign sprite row builder) and FUN_08028194 (same type) before building campaign row sprites to check SIO communication status. Reads SIOCNT (0x04000128) bits[5:4] (mask 0x30); if either bit set (SIO busy/transfer in progress) returns r0=0 (not ready); if both bits clear (SIO idle) returns r0=1 (ready). Used in campaign screen to verify link is idle before updating display data, preventing display updates during SIO transfer.
@ 
@ Constants:
@ SIOCNT = 0x04000128 (GBA SIO control register)
@ LINK_BUSY_MASK = 0x30 (bits[5:4]: bit4=start/busy, bit5=SIO mode select)
@ READY = 1 (both bits clear => link idle)
@ BUSY = 0 (either bit set => link busy)
check_siocnt_link_ready:
    movs r2,#0x0    @ 0801f398 0022
    ldr r0, DWORD_0801f3ac                   @ 0801f39a 0448
    ldrh r1,[r0,#0x0]                        @ 0801f39c 0188
    movs r0,#0x30    @ 0801f39e 3020
    ands r0,r1    @ 0801f3a0 0840
    cmp r0,#0x0                              @ 0801f3a2 0028
    bne LAB_0801f3a8                         @ 0801f3a4 00d1
    movs r2,#0x1    @ 0801f3a6 0122
LAB_0801f3a8:
    adds r0,r2,#0x0    @ 0801f3a8 101c
    bx lr                                    @ 0801f3aa 7047
DWORD_0801f3ac:
    .word  SIOCNT                         @ 0801f3ac 28010004

@ Reads a flag byte at gPrng+0x1c0[+0x584] and returns the inverted bit0 as a bool. No APCS input (first two instructions overwrite r0 and r1). Computes gPrng + (0xe0<<1)=0x1c0, dereferences the word there as a pointer, then adds offset 0x584 (DAT_0801f3cc), reads a byte, and returns bics r0(=1),r1 -> 1 if bit0 is clear, 0 if bit0 is set. Result is 'flag_is_clear' boolean. Leaf; called by FUN_080954e8 (prng tagged). No side effects (read-only). Constants: gPrng_offset=0x1c0 (0xe0<<1), entry_offset=0x584, flag_bit=0x1.
read_prng_entry_flag_clear:
    ldr r0, PTR_gPrng_0801f3c8               @ 0801f3b0 0548
    movs r1,#0xe0    @ 0801f3b2 e021
    lsls r1,r1,#0x1    @ 0801f3b4 4900
    adds r0,r0,r1    @ 0801f3b6 4018
    ldr r1,[r0,#0x0]                         @ 0801f3b8 0168
    ldr r0, DAT_0801f3cc                     @ 0801f3ba 0448
    adds r1,r1,r0    @ 0801f3bc 0918
    movs r0,#0x1    @ 0801f3be 0120
    ldrb r1,[r1,#0x0]                        @ 0801f3c0 0978
    bics r0,r1    @ 0801f3c2 8843
    bx lr                                    @ 0801f3c4 7047
    .zero  0x2
PTR_gPrng_0801f3c8:
    .word  gPrng                          @ 0801f3c8 40000003
DAT_0801f3cc:
    .word  0x00000584                     @ 0801f3cc 84050000
    .byte  0x70, 0x47, 0x00, 0x00

@ No-op stub; executes bx lr immediately and returns. Called by enqueue_sprite_attr_record (0x0803bd2c) as 'entry committed' notification placeholder after writing four halfword sprite attributes. Identical single-instruction bx lr structure to return_void_noop (0x080fa4d8, batch #28). In release build this callback is optimized to empty. Address-adjacent siblings: FUN_0801f3d8 (movs r0,#0; bx lr), FUN_0801f3dc (bx lr), FUN_0801f3e4 (movs r0,#1; bx lr). Side effects: none.
return_void_noop_stub:
    bx lr                                    @ 0801f3d4 7047
    .zero  0x2

@ Called by FUN_08094c10 in loop body LAB_08094c16. Returns r0=0 as next operation base address or completion flag. Body: movs r0,#0; bx lr. Fixed return value 0. Part of fixed-return stub family with return_one_leaf (0x0801f3e4) and return_noop_leaf (0x0801f3dc).
@ Constants: (none).
return_zero_leaf:
    movs r0,#0x0    @ 0801f3d8 0020
    bx lr                                    @ 0801f3da 7047

@ Called by FUN_08094c10 in loop body LAB_08094c16 tail. No-op stub: body is single bx lr instruction, does not modify any register or memory; r0 retains value from previous bl (write_sprite_attrs_to_seq_buf return). Part of fixed-return stub family with return_zero_leaf (0x0801f3d8) and return_one_leaf (0x0801f3e4).
@ Constants: (none).
return_noop_leaf:
    bx lr                                    @ 0801f3dc 7047
    .byte  0x00, 0x00, 0x70, 0x47, 0x00, 0x00

@ Minimal leaf stub, function body is two instructions: movs r0,#1; bx lr.
@ Called by tick_equip_activation_main_sequence (0x08094cd4) unconditionally
@ when [0x0201e2a0+8] == 3, reporting "done" signal (r0=1 = nonzero = complete this
@ frame). Paired with FUN_0801f3dc (bx lr only, r0=0) as fixed-return-value stub family.
@ No external side effects.
return_one_leaf:
    movs r0,#0x1    @ 0801f3e4 0120
    bx lr                                    @ 0801f3e6 7047

@ Linear search deck_record_table for a record whose first u16 matches search_key; return its index.
@ Iterates deck_record_table (ROM 0x09E58D0C), 32 bytes per record, up to 120 records (0x78),
@ comparing first halfword with r0. Returns index [0..119] on match, -1 on miss (rsbs on 1).
@ Callers: FUN_0802d2fc and FUN_0802d3c4 (card tilemap upload), enter_limited_duel_page (0x080e1390),
@ enter_duel_puzzle_page (0x080e1a50), enter_theme_duel_page (0x080e3904).
@ Constants: deck_record_table=0x09E58D0C; RECORD_STRIDE=0x20=32; MAX_RECORDS=0x78=120; NOT_FOUND=-1.
find_deck_record_index_by_key:
    adds r3,r0,#0x0    @ 0801f3e8 031c
    movs r1,#0x0    @ 0801f3ea 0021
    ldr r2, PTR_deck_record_table_0801f3f8   @ 0801f3ec 024a
LAB_0801f3ee:
    ldrh r0,[r2,#0x0]                        @ 0801f3ee 1088
    cmp r0,r3                                @ 0801f3f0 9842
    bne LAB_0801f3fc                         @ 0801f3f2 03d1
    adds r0,r1,#0x0    @ 0801f3f4 081c
    b LAB_0801f408                           @ 0801f3f6 07e0
PTR_deck_record_table_0801f3f8:
    .word  deck_record_table              @ 0801f3f8 0c8de509
LAB_0801f3fc:
    adds r2,#0x20    @ 0801f3fc 2032
    adds r1,#0x1    @ 0801f3fe 0131
    cmp r1,#0x78                             @ 0801f400 7829
    bls LAB_0801f3ee                         @ 0801f402 f4d9
    movs r0,#0x1    @ 0801f404 0120
    rsbs r0,r0,#0    @ 0801f406 4042
LAB_0801f408:
    bx lr                                    @ 0801f408 7047
    .zero  0x2

@ Called by FUN_0801fec0, FUN_0802752c, and FUN_0802d638 (indeg=3). Takes r0=card_id as search key, reads ROM[0x098973f6] (halfword = table entry count), reads ROM[0x098972f0] (halfword array, 2 bytes per entry). Linear search: if table[i]==card_id returns i (found); if not found after full scan returns -1. Exit: pop {r4}; pop {r1}; bx r1.
@ 
@ Constants:
@ - ROM_TABLE_COUNT_PTR=0x098973f6 (halfword: entry count)
@ - ROM_TABLE_DATA_PTR=0x098972f0 (halfword array: card id list)
@ - NOT_FOUND=-1 (0xFFFFFFFF)
find_card_index_in_rom_table:
    push {r4,lr}                             @ 0801f40c 10b5
    adds r4,r0,#0x0    @ 0801f40e 041c
    movs r1,#0x0    @ 0801f410 0021
    ldr r0, DAT_0801f428                     @ 0801f412 0548
    ldrh r0,[r0,#0x0]                        @ 0801f414 0088
    cmp r1,r0                                @ 0801f416 8142
    bge LAB_0801f438                         @ 0801f418 0eda
    adds r3,r0,#0x0    @ 0801f41a 031c
    ldr r2, DAT_0801f42c                     @ 0801f41c 034a
LAB_0801f41e:
    ldrh r0,[r2,#0x0]                        @ 0801f41e 1088
    cmp r0,r4                                @ 0801f420 a042
    bne LAB_0801f430                         @ 0801f422 05d1
    adds r0,r1,#0x0    @ 0801f424 081c
    b LAB_0801f43c                           @ 0801f426 09e0
DAT_0801f428:
    .word  0x098973f6                     @ 0801f428 f6738909
DAT_0801f42c:
    .word  0x098972f0                     @ 0801f42c f0728909
LAB_0801f430:
    adds r2,#0x2    @ 0801f430 0232
    adds r1,#0x1    @ 0801f432 0131
    cmp r1,r3                                @ 0801f434 9942
    blt LAB_0801f41e                         @ 0801f436 f2db
LAB_0801f438:
    movs r0,#0x1    @ 0801f438 0120
    rsbs r0,r0,#0    @ 0801f43a 4042
LAB_0801f43c:
    pop {r4}                                 @ 0801f43c 10bc
    pop {r1}                                 @ 0801f43e 02bc
    bx r1                                    @ 0801f440 0847
    .zero  0x2

@ Mounted as gMenuState+0x234 step function by assignment at 0x080e1514, activated in scene_pack case 5 (after tick_pack_fadein completes). Reads gPrng+0x202 halfword, extracts bits[13:8] (6-bit scene step index, [0..20] normal range); if index > 0x14 (20) calls poll_fadein_exit_to_duel_state (fadein overflow handler); otherwise indexes ROM function pointer table (base 0x0801f47c) via step index and jumps via .hword 0x4687 (mov r15,r0 = bx r0). This function is the duel_puzzle scene step dispatch entry; does not return directly (tail call bx r0).
@ 
@ Constants:
@ STEP_IDX_OFFSET = 0x202 (gPrng+0x202, halfword, bits[13:6] = 8-bit step index field)
@ MAX_STEP_IDX = 0x14 = 20 ([0..20] valid range)
@ STEP_TABLE_BASE = 0x0801f47c (ROM step function pointer table)
@ gPrng = 0x03000040
tick_duel_puzzle_scene_step:
    push {r4,r5,r6,r7,lr}                    @ 0801f444 f0b5
    .hword 0x4657    @ 0801f446 5746
    .hword 0x464e    @ 0801f448 4e46
    .hword 0x4645    @ 0801f44a 4546
    push {r5,r6,r7}                          @ 0801f44c e0b4
    sub sp,#0x8                              @ 0801f44e 82b0
    ldr r0, PTR_gPrng_0801f470               @ 0801f450 0748
    ldr r2, DAT_0801f474                     @ 0801f452 084a
    adds r1,r0,r2    @ 0801f454 8118
    ldrh r1,[r1,#0x0]                        @ 0801f456 0988
    lsls r1,r1,#0x12    @ 0801f458 8904
    lsrs r1,r1,#0x18    @ 0801f45a 090e
    adds r2,r0,#0x0    @ 0801f45c 021c
    cmp r1,#0x14                             @ 0801f45e 1429
    bls LAB_0801f466                         @ 0801f460 01d9
    bl poll_fadein_exit_to_duel_state        @ 0801f462 00f016fd
LAB_0801f466:
    lsls r0,r1,#0x2    @ 0801f466 8800
    ldr r1, DAT_0801f478                     @ 0801f468 0349
    adds r0,r0,r1    @ 0801f46a 4018
    ldr r0,[r0,#0x0]                         @ 0801f46c 0068
    .hword 0x4687    @ 0801f46e 8746
PTR_gPrng_0801f470:
    .word  gPrng                          @ 0801f470 40000003
DAT_0801f474:
    .word  0x00000202                     @ 0801f474 02020000
DAT_0801f478:
    .word  0x0801f47c                     @ 0801f478 7cf40108
PTR_DAT_0801f47c:
    .word  0x0801f4d0                     @ 0801f47c d0f40108
    .word  0x0801f5ec                     @ 0801f480 ecf50108
    .word  0x0801f60c                     @ 0801f484 0cf60108
    .word  0x0801f738                     @ 0801f488 38f70108
    .word  0x0801f9c4                     @ 0801f48c c4f90108
    .word  0x0801f9e0                     @ 0801f490 e0f90108
    .word  0x0801fb20                     @ 0801f494 20fb0108
    .word  0x0801fb2c                     @ 0801f498 2cfb0108
    .word  0x0801fbe4                     @ 0801f49c e4fb0108
    .word  0x0801fc18                     @ 0801f4a0 18fc0108
    .word  0x0801fd48                     @ 0801f4a4 48fd0108
    .word  0x0801fd80                     @ 0801f4a8 80fd0108
    .word  0x0801fe14                     @ 0801f4ac 14fe0108
    .word  0x0801fe54                     @ 0801f4b0 54fe0108
    .word  0x0801fe92                     @ 0801f4b4 92fe0108
    .word  0x0801fe92                     @ 0801f4b8 92fe0108
    .word  0x0801fe92                     @ 0801f4bc 92fe0108
    .word  0x0801fe92                     @ 0801f4c0 92fe0108
    .word  0x0801fe92                     @ 0801f4c4 92fe0108
    .word  0x0801fe92                     @ 0801f4c8 92fe0108
    .word  0x0801fe7c                     @ 0801f4cc 7cfe0108
DAT_0801f4d0:
    ROM_INCBIN 0x1f4d0, 0x690
    .word  0x0801fb64                     @ 0801fb60 64fb0108
PTR_DAT_0801fb64:
    .word  0x0801fb90                     @ 0801fb64 90fb0108
    .word  0x0801fb94                     @ 0801fb68 94fb0108
    .word  0x0801fbbe                     @ 0801fb6c befb0108
    .word  0x0801fbbe                     @ 0801fb70 befb0108
    .word  0x0801fb98                     @ 0801fb74 98fb0108
    .word  0x0801fbbe                     @ 0801fb78 befb0108
    .word  0x0801fbbe                     @ 0801fb7c befb0108
    .word  0x0801fbbe                     @ 0801fb80 befb0108
    .word  0x0801fbbe                     @ 0801fb84 befb0108
    .word  0x0801fb9c                     @ 0801fb88 9cfb0108
    .word  0x0801fbb2                     @ 0801fb8c b2fb0108
DAT_0801fb90:
    ROM_INCBIN 0x1fb90, 0x302

@ Inline exit fragment on overflow path of parent state machine FUN_0801f444 (tags: blend).
@ Triggered when field_state > 0x14.
@ Calls tick_duel_field_fadein_step to advance blend fade-in one frame;
@ if not done (nonzero), reads [0x0201e2a0+0x224] (gDuelState+0x89*4) scene state word and returns it;
@ if done (zero), returns 0x100 (=0x80<<1) signaling state machine advance.
@ Also executes parent function epilogue: add sp,#0x8; pop {r3-r7}; bx r1.
@ Pointer table DAT_0801f47c indices 0xe..0x13 all point to this address (overflow/done path confluence).
@ Constants: DUEL_STATE_SLOT=[0x0201e2a0+0x224] (gDuelState+0x89*4); FADEIN_DONE_STATUS=0x100 (0x80<<1).
poll_fadein_exit_to_duel_state:
    bl tick_duel_field_fadein_step           @ 0801fe92 acf0e3fd
    cmp r0,#0x0                              @ 0801fe96 0028
    beq LAB_0801feac                         @ 0801fe98 08d0
    ldr r0, DAT_0801fea8                     @ 0801fe9a 0348
    movs r2,#0x89    @ 0801fe9c 8922
    lsls r2,r2,#0x2    @ 0801fe9e 9200
    adds r0,r0,r2    @ 0801fea0 8018
    ldr r0,[r0,#0x0]                         @ 0801fea2 0068
    b LAB_0801feb0                           @ 0801fea4 04e0
    .zero  0x2
DAT_0801fea8:
    .word  0x0201e2a0                     @ 0801fea8 a0e20102
LAB_0801feac:
    movs r0,#0x80    @ 0801feac 8020
    lsls r0,r0,#0x1    @ 0801feae 4000
LAB_0801feb0:
    add sp,#0x8                              @ 0801feb0 02b0
    pop {r3,r4,r5}                           @ 0801feb2 38bc
    .hword 0x4698    @ 0801feb4 9846
    .hword 0x46a1    @ 0801feb6 a146
    .hword 0x46aa    @ 0801feb8 aa46
    pop {r4,r5,r6,r7}                        @ 0801feba f0bc
    pop {r1}                                 @ 0801febc 02bc
    bx r1                                    @ 0801febe 0847

@ duel-puzzle 场景主状态机入口. fn-ptr 表 0x080e1c88 (.word 0x0801fec1) 引用, 由场景调度器在每帧调用. 通过读 gPrng+0x202 halfword bits[13:6] (9-state 索引 [0..8]) 派发到 9 个分支: case 0 = 初始化 (zero_duel_scene_display_buffers + fs_load + init_duel_puzzle_scene_state + init_duel_field_vram_layout + LP 标志位设置); case 1 = tick_duel_field_fadeout_step; case 2 = tick_duel_field_main_frame (主对局帧); case 3 = tick_duel_field_fadein_step + 写 gPrng+0x23f flags; case 4..8 = 奖励/LP 显示/数据保存/结束淡出等步骤 (含 render_puzzle_lp_digit_sprites, count_cleared_puzzle_stages, accrue_money_with_cap, find_expert_challenge_slot_by_id, render_card_name_centered_to_sprite_vram, dispatch_puzzle_display_mode 等). 所有 case 共享出口 LAB_080202ec (movs r0,#0x80; lsls r0,#0x1 = 0x100) 或 LAB_080202d4 (movs r0,#0).
run_duel_puzzle_scene_state_machine:
    push {r4,r5,r6,r7,lr}                    @ 0801fec0 f0b5
    .hword 0x4657    @ 0801fec2 5746
    .hword 0x464e    @ 0801fec4 4e46
    .hword 0x4645    @ 0801fec6 4546
    push {r5,r6,r7}                          @ 0801fec8 e0b4
    .hword 0x4682    @ 0801feca 8246
    ldr r0, PTR_gPrng_0801feec               @ 0801fecc 0748
    ldr r2, DAT_0801fef0                     @ 0801fece 084a
    adds r1,r0,r2    @ 0801fed0 8118
    ldrh r1,[r1,#0x0]                        @ 0801fed2 0988
    lsls r1,r1,#0x12    @ 0801fed4 8904
    lsrs r1,r1,#0x18    @ 0801fed6 090e
    adds r2,r0,#0x0    @ 0801fed8 021c
    cmp r1,#0x8                              @ 0801feda 0829
    bls LAB_0801fee0                         @ 0801fedc 00d9
switchD_0801fee8__default:
    b LAB_080202d4                           @ 0801fede f9e1
LAB_0801fee0:
    lsls r0,r1,#0x2    @ 0801fee0 8800
    ldr r1, DAT_0801fef4                     @ 0801fee2 0449
    adds r0,r0,r1    @ 0801fee4 4018
    ldr r0,[r0,#0x0]                         @ 0801fee6 0068
switchD_0801fee8__switchD:
    .hword 0x4687    @ 0801fee8 8746
    .zero  0x2
PTR_gPrng_0801feec:
    .word  gPrng                          @ 0801feec 40000003
DAT_0801fef0:
    .word  0x00000202                     @ 0801fef0 02020000
DAT_0801fef4:
    .word  0x0801fef8                     @ 0801fef4 f8fe0108
switchD_0801fee8__switchdataD_0801fef8:
    .word  0x0801ff1c                     @ 0801fef8 1cff0108
    .word  0x0802001c                     @ 0801fefc 1c000208
    .word  0x08020028                     @ 0801ff00 28000208
    .word  0x08020044                     @ 0801ff04 44000208
    .word  0x0802007c                     @ 0801ff08 7c000208
    .word  0x080201a0                     @ 0801ff0c a0010208
    .word  0x080201d8                     @ 0801ff10 d8010208
    .word  0x0802026c                     @ 0801ff14 6c020208
    .word  0x080202ac                     @ 0801ff18 ac020208
switchD_0801fee8__caseD_0:
    ldr r0, DAT_0801ffec                     @ 0801ff1c 3348
    movs r1,#0x10    @ 0801ff1e 1021
    bl zero_fill_by_halfword                 @ 0801ff20 d4f0a8ff
    ldr r3, PTR_gPrng_0801fff0               @ 0801ff24 324b
    .hword 0x4699    @ 0801ff26 9946
    ldr r1, DAT_0801fff4                     @ 0801ff28 3249
    add r1,r9                                @ 0801ff2a 4944
    movs r4,#0x2    @ 0801ff2c 0224
    rsbs r4,r4,#0    @ 0801ff2e 6442
    adds r0,r4,#0x0    @ 0801ff30 201c
    ldrb r7,[r1,#0x0]                        @ 0801ff32 0f78
    ands r0,r7    @ 0801ff34 3840
    strb r0,[r1,#0x0]                        @ 0801ff36 0870
    bl zero_duel_scene_display_buffers       @ 0801ff38 acf080fc
    ldr r5, DAT_0801fff8                     @ 0801ff3c 2e4d
    movs r0,#0x88    @ 0801ff3e 8820
    lsls r0,r0,#0x2    @ 0801ff40 8000
    adds r0,r0,r5    @ 0801ff42 4019
    .hword 0x4680    @ 0801ff44 8046
    ldr r0,[r0,#0x0]                         @ 0801ff46 0068
    ldr r1, DAT_0801fffc                     @ 0801ff48 2c49
    ands r0,r1    @ 0801ff4a 0840
    movs r1,#0x80    @ 0801ff4c 8021
    lsls r1,r1,#0x4    @ 0801ff4e 0901
    orrs r0,r1    @ 0801ff50 0843
    .hword 0x4641    @ 0801ff52 4146
    str r0,[r1,#0x0]                         @ 0801ff54 0860
    ldr r0, DAT_08020000                     @ 0801ff56 2a48
    bl find_card_index_in_rom_table          @ 0801ff58 fff758fa
    lsls r0,r0,#0x10    @ 0801ff5c 0004
    lsrs r2,r0,#0x10    @ 0801ff5e 020c
    movs r1,#0x7f    @ 0801ff60 7f21
    ands r2,r1    @ 0801ff62 0a40
    ldr r7, DAT_08020004                     @ 0801ff64 274f
    adds r3,r5,r7    @ 0801ff66 eb19
    lsls r2,r2,#0x1    @ 0801ff68 5200
    movs r6,#0x1    @ 0801ff6a 0126
    adds r1,r6,#0x0    @ 0801ff6c 311c
    ldrb r7,[r3,#0x0]                        @ 0801ff6e 1f78
    ands r1,r7    @ 0801ff70 3940
    orrs r1,r2    @ 0801ff72 1143
    strb r1,[r3,#0x0]                        @ 0801ff74 1970
    lsrs r0,r0,#0x17    @ 0801ff76 c00d
    movs r1,#0x85    @ 0801ff78 8521
    lsls r1,r1,#0x2    @ 0801ff7a 8900
    adds r5,r5,r1    @ 0801ff7c 6d18
    ands r0,r6    @ 0801ff7e 3040
    ldrb r2,[r5,#0x0]                        @ 0801ff80 2a78
    ands r4,r2    @ 0801ff82 1440
    orrs r4,r0    @ 0801ff84 0443
    strb r4,[r5,#0x0]                        @ 0801ff86 2c70
    bl tick_prng_lcg_rand15                  @ 0801ff88 d8f0b4ff
    ldr r1, DAT_08020008                     @ 0801ff8c 1e49
    lsls r0,r0,#0x10    @ 0801ff8e 0004
    lsrs r0,r0,#0x10    @ 0801ff90 000c
    str r0,[r1,#0x0]                         @ 0801ff92 0860
    movs r0,#0x0    @ 0801ff94 0020
    str r0,[r1,#0x4]                         @ 0801ff96 4860
    str r0,[r1,#0x8]                         @ 0801ff98 8860
    str r6,[r1,#0xc]                         @ 0801ff9a ce60
    str r0,[r1,#0x10]                        @ 0801ff9c 0861
    ldr r4, DAT_0802000c                     @ 0801ff9e 1b4c
    .hword 0x4650    @ 0801ffa0 5046
    movs r1,#0x23    @ 0801ffa2 2321
    bl __umodsi3                             @ 0801ffa4 eef056fc
    lsls r0,r0,#0x2    @ 0801ffa8 8000
    adds r0,r0,r4    @ 0801ffaa 0019
    ldr r0,[r0,#0x0]                         @ 0801ffac 0068
    movs r1,#0x0    @ 0801ffae 0021
    bl fs_load                               @ 0801ffb0 f4f7faff
    bl init_duel_puzzle_scene_state          @ 0801ffb4 73f00efc
    bl init_duel_field_vram_layout           @ 0801ffb8 acf0a4fc
    ldr r0, DAT_08020010                     @ 0801ffbc 1448
    .hword 0x4643    @ 0801ffbe 4346
    ldrh r3,[r3,#0x0]                        @ 0801ffc0 1b88
    ands r0,r3    @ 0801ffc2 1840
    movs r1,#0x3c    @ 0801ffc4 3c21
    orrs r0,r1    @ 0801ffc6 0843
    .hword 0x4647    @ 0801ffc8 4746
    strh r0,[r7,#0x0]                        @ 0801ffca 3880
    ldr r0, DAT_08020014                     @ 0801ffcc 1148
    add r9,r0                                @ 0801ffce 8144
    .hword 0x4649    @ 0801ffd0 4946
    ldrh r2,[r1,#0x0]                        @ 0801ffd2 0a88
    lsls r1,r2,#0x12    @ 0801ffd4 9104
    lsrs r1,r1,#0x18    @ 0801ffd6 090e
    adds r1,#0x1    @ 0801ffd8 0131
    movs r0,#0xff    @ 0801ffda ff20
    ands r1,r0    @ 0801ffdc 0140
    lsls r1,r1,#0x6    @ 0801ffde 8901
    ldr r0, DAT_08020018                     @ 0801ffe0 0d48
    ands r0,r2    @ 0801ffe2 1040
    orrs r0,r1    @ 0801ffe4 0843
    .hword 0x464a    @ 0801ffe6 4a46
    strh r0,[r2,#0x0]                        @ 0801ffe8 1080
    b LAB_080202ec                           @ 0801ffea 7fe1
DAT_0801ffec:
    .word  0x02029e90                     @ 0801ffec 909e0202
PTR_gPrng_0801fff0:
    .word  gPrng                          @ 0801fff0 40000003
DAT_0801fff4:
    .word  0x0000023f                     @ 0801fff4 3f020000
DAT_0801fff8:
    .word  0x02023130                     @ 0801fff8 30310202
DAT_0801fffc:
    .word  0xfffc03ff                     @ 0801fffc ff03fcff
DAT_08020000:
    .word  0x00007530                     @ 08020000 30750000
DAT_08020004:
    .word  0x00000213                     @ 08020004 13020000
DAT_08020008:
    .word  0x0201e2a0                     @ 08020008 a0e20102
DAT_0802000c:
    .word  0x09e59c2c                     @ 0802000c 2c9ce509
DAT_08020010:
    .word  0xfffffc03                     @ 08020010 03fcffff
DAT_08020014:
    .word  0x00000202                     @ 08020014 02020000
DAT_08020018:
    .word  0xffffc03f                     @ 08020018 3fc0ffff
switchD_0801fee8__caseD_1:
    bl tick_duel_field_fadeout_step          @ 0802001c acf00cfd
    cmp r0,#0x0                              @ 08020020 0028
    bne LAB_08020026                         @ 08020022 00d1
    b LAB_080202ec                           @ 08020024 62e1
LAB_08020026:
    b LAB_0802023e                           @ 08020026 0ae1
switchD_0801fee8__caseD_2:
    bl tick_duel_field_main_frame            @ 08020028 fef7acfc
    cmp r0,#0x0                              @ 0802002c 0028
    bne LAB_08020032                         @ 0802002e 00d1
    b LAB_080202ec                           @ 08020030 5ce1
LAB_08020032:
    ldr r2, PTR_gPrng_0802003c               @ 08020032 024a
    ldr r7, DAT_08020040                     @ 08020034 024f
    adds r2,r2,r7    @ 08020036 d219
    b LAB_08020244                           @ 08020038 04e1
    .zero  0x2
PTR_gPrng_0802003c:
    .word  gPrng                          @ 0802003c 40000003
DAT_08020040:
    .word  0x00000202                     @ 08020040 02020000
switchD_0801fee8__caseD_3:
    bl tick_duel_field_fadein_step           @ 08020044 acf00afd
    cmp r0,#0x0                              @ 08020048 0028
    bne LAB_0802004e                         @ 0802004a 00d1
    b LAB_080202ec                           @ 0802004c 4ee1
LAB_0802004e:
    ldr r2, PTR_gPrng_08020074               @ 0802004e 094a
    ldr r0, DAT_08020078                     @ 08020050 0948
    adds r1,r2,r0    @ 08020052 1118
    movs r0,#0x3f    @ 08020054 3f20
    ldrb r3,[r1,#0x0]                        @ 08020056 0b78
    ands r0,r3    @ 08020058 1840
    strb r0,[r1,#0x0]                        @ 0802005a 0870
    movs r7,#0x81    @ 0802005c 8127
    lsls r7,r7,#0x2    @ 0802005e bf00
    adds r1,r2,r7    @ 08020060 d119
    movs r0,#0x40    @ 08020062 4020
    rsbs r0,r0,#0    @ 08020064 4042
    ldrb r3,[r1,#0x0]                        @ 08020066 0b78
    ands r0,r3    @ 08020068 1840
    strb r0,[r1,#0x0]                        @ 0802006a 0870
    subs r7,#0x2    @ 0802006c 023f
    adds r2,r2,r7    @ 0802006e d219
    b LAB_08020244                           @ 08020070 e8e0
    .zero  0x2
PTR_gPrng_08020074:
    .word  gPrng                          @ 08020074 40000003
DAT_08020078:
    .word  0x00000203                     @ 08020078 03020000
switchD_0801fee8__caseD_4:
    ldr r0, DAT_08020134                     @ 0802007c 2d48
    movs r1,#0x89    @ 0802007e 8921
    lsls r1,r1,#0x2    @ 08020080 8900
    adds r0,r0,r1    @ 08020082 4018
    ldr r0,[r0,#0x0]                         @ 08020084 0068
    cmp r0,#0x1                              @ 08020086 0128
    beq LAB_0802008c                         @ 08020088 00d0
    b LAB_08020190                           @ 0802008a 81e0
LAB_0802008c:
    movs r3,#0x8f    @ 0802008c 8f23
    lsls r3,r3,#0x2    @ 0802008e 9b00
    adds r7,r2,r3    @ 08020090 d718
    ldrh r0,[r7,#0x0]                        @ 08020092 3888
    bl find_expert_challenge_slot_by_id      @ 08020094 c1f07afb
    adds r5,r0,#0x0    @ 08020098 051c
    ldr r0, DAT_08020138                     @ 0802009a 2748
    .hword 0x4680    @ 0802009c 8046
    lsls r4,r5,#0x2    @ 0802009e ac00
    adds r0,r4,r0    @ 080200a0 2018
    ldr r1, DAT_0802013c                     @ 080200a2 2649
    adds r0,r0,r1    @ 080200a4 4018
    ldrb r0,[r0,#0x0]                        @ 080200a6 0078
    lsls r0,r0,#0x1e    @ 080200a8 8007
    lsrs r0,r0,#0x1e    @ 080200aa 800f
    cmp r0,#0x1                              @ 080200ac 0128
    beq LAB_08020190                         @ 080200ae 6fd0
    bl get_expert_challenge_count            @ 080200b0 c1f06afb
    adds r1,r0,#0x0    @ 080200b4 011c
    adds r0,r4,r5    @ 080200b6 6019
    bl __divsi3                              @ 080200b8 eef0a4fa
    adds r0,#0x1    @ 080200bc 0130
    movs r1,#0xc8    @ 080200be c821
    adds r6,r0,#0x0    @ 080200c0 061c
    muls r6,r1    @ 080200c2 4e43
    bl get_expert_challenge_count            @ 080200c4 c1f060fb
    adds r1,r0,#0x0    @ 080200c8 011c
    movs r0,#0x0    @ 080200ca 0020
    bl count_cleared_puzzle_stages           @ 080200cc c3f0b0fe
    adds r4,r0,#0x0    @ 080200d0 041c
    bl get_expert_challenge_count            @ 080200d2 c1f059fb
    subs r0,#0x1    @ 080200d6 0138
    cmp r4,r0                                @ 080200d8 8442
    bne LAB_080200e0                         @ 080200da 01d1
    ldr r2, DAT_08020140                     @ 080200dc 184a
    adds r6,r6,r2    @ 080200de b618
LAB_080200e0:
    ldrh r0,[r7,#0x0]                        @ 080200e0 3888
    bl game_str_id_to_row                    @ 080200e2 d4f099fe
    ldr r2, PTR_game_str_pointer_table_08020144 @ 080200e6 174a
    lsls r0,r0,#0x10    @ 080200e8 0004
    lsrs r0,r0,#0x10    @ 080200ea 000c
    lsls r1,r0,#0x1    @ 080200ec 4100
    adds r1,r1,r0    @ 080200ee 0918
    lsls r1,r1,#0x1    @ 080200f0 4900
    ldr r4, DAT_08020148                     @ 080200f2 154c
    add r4,r8                                @ 080200f4 4444
    ldrb r3,[r4,#0x0]                        @ 080200f6 2378
    lsls r0,r3,#0x1d    @ 080200f8 5807
    lsrs r0,r0,#0x1d    @ 080200fa 400f
    adds r1,r1,r0    @ 080200fc 0918
    lsls r1,r1,#0x2    @ 080200fe 8900
    adds r1,r1,r2    @ 08020100 8918
    ldr r0,[r1,#0x0]                         @ 08020102 0868
    ldr r5, PTR_game_str_ja_0802014c         @ 08020104 114d
    adds r0,r0,r5    @ 08020106 4019
    movs r1,#0x0    @ 08020108 0021
    bl init_pack_card_info_screen_vram       @ 0802010a 0bf041fa
    bl init_puzzle_card_name_line_buf        @ 0802010e 0bf0d5fb
    movs r1,#0x7    @ 08020112 0721
    ldrb r4,[r4,#0x0]                        @ 08020114 2478
    ands r1,r4    @ 08020116 2140
    cmp r1,#0x1                              @ 08020118 0129
    beq LAB_0802017c                         @ 0802011a 2fd0
    cmp r1,#0x2                              @ 0802011c 0229
    beq LAB_08020170                         @ 0802011e 27d0
    cmp r1,#0x3                              @ 08020120 0329
    beq LAB_08020164                         @ 08020122 1fd0
    cmp r1,#0x4                              @ 08020124 0429
    beq LAB_08020158                         @ 08020126 17d0
    ldr r7, DAT_08020150                     @ 08020128 094f
    adds r0,r5,r7    @ 0802012a e819
    cmp r1,#0x5                              @ 0802012c 0529
    bne LAB_08020180                         @ 0802012e 27d1
    ldr r1, DAT_08020154                     @ 08020130 0849
    b LAB_0802017e                           @ 08020132 24e0
DAT_08020134:
    .word  0x0201e2a0                     @ 08020134 a0e20102
DAT_08020138:
    .word  0x02000000                     @ 08020138 00000002
DAT_0802013c:
    .word  0x00006c3c                     @ 0802013c 3c6c0000
DAT_08020140:
    .word  0x00001662                     @ 08020140 62160000
PTR_game_str_pointer_table_08020144:
    .word  game_str_pointer_table         @ 08020144 400f0008
DAT_08020148:
    .word  0x00006c2c                     @ 08020148 2c6c0000
PTR_game_str_ja_0802014c:
    .word  game_str_ja                    @ 0802014c 109cdb09
DAT_08020150:
    .word  0x00004b4e                     @ 08020150 4e4b0000
DAT_08020154:
    .word  0x0003f66a                     @ 08020154 6af60300
LAB_08020158:
    ldr r2, DAT_08020160                     @ 08020158 014a
    adds r0,r5,r2    @ 0802015a a818
    b LAB_08020180                           @ 0802015c 10e0
    .zero  0x2
DAT_08020160:
    .word  0x000339ce                     @ 08020160 ce390300
LAB_08020164:
    ldr r3, DAT_0802016c                     @ 08020164 014b
    adds r0,r5,r3    @ 08020166 e818
    b LAB_08020180                           @ 08020168 0ae0
    .zero  0x2
DAT_0802016c:
    .word  0x00027532                     @ 0802016c 32750200
LAB_08020170:
    ldr r7, DAT_08020178                     @ 08020170 014f
    adds r0,r5,r7    @ 08020172 e819
    b LAB_08020180                           @ 08020174 04e0
    .zero  0x2
DAT_08020178:
    .word  0x0001b2a0                     @ 08020178 a0b20100
LAB_0802017c:
    ldr r1, DAT_0802018c                     @ 0802017c 0349
LAB_0802017e:
    adds r0,r5,r1    @ 0802017e 6818
LAB_08020180:
    adds r1,r6,#0x0    @ 08020180 311c
    bl render_card_stat_with_number_alt      @ 08020182 0bf081fd
    bl zero_sprite_vram_with_tile_seq        @ 08020186 0bf0edfd
    b LAB_0802023e                           @ 0802018a 58e0
DAT_0802018c:
    .word  0x0000fc06                     @ 0802018c 06fc0000
LAB_08020190:
    ldr r0, DAT_0802019c                     @ 08020190 0248
    movs r7,#0x89    @ 08020192 8927
    lsls r7,r7,#0x2    @ 08020194 bf00
    adds r0,r0,r7    @ 08020196 c019
    ldr r0,[r0,#0x0]                         @ 08020198 0068
    b LAB_080202f0                           @ 0802019a a9e0
DAT_0802019c:
    .word  0x0201e2a0                     @ 0802019c a0e20102
switchD_0801fee8__caseD_5:
    bl tick_lp_display_and_blend_step        @ 080201a0 0bf010fe
    cmp r0,#0x0                              @ 080201a4 0028
    bne LAB_080201aa                         @ 080201a6 00d1
    b LAB_080202ec                           @ 080201a8 a0e0
LAB_080201aa:
    ldr r2, PTR_gPrng_080201d0               @ 080201aa 094a
    ldr r0, DAT_080201d4                     @ 080201ac 0948
    adds r1,r2,r0    @ 080201ae 1118
    movs r0,#0x3f    @ 080201b0 3f20
    ldrb r3,[r1,#0x0]                        @ 080201b2 0b78
    ands r0,r3    @ 080201b4 1840
    strb r0,[r1,#0x0]                        @ 080201b6 0870
    movs r7,#0x81    @ 080201b8 8127
    lsls r7,r7,#0x2    @ 080201ba bf00
    adds r1,r2,r7    @ 080201bc d119
    movs r0,#0x40    @ 080201be 4020
    rsbs r0,r0,#0    @ 080201c0 4042
    ldrb r3,[r1,#0x0]                        @ 080201c2 0b78
    ands r0,r3    @ 080201c4 1840
    strb r0,[r1,#0x0]                        @ 080201c6 0870
    subs r7,#0x2    @ 080201c8 023f
    adds r2,r2,r7    @ 080201ca d219
    b LAB_08020244                           @ 080201cc 3ae0
    .zero  0x2
PTR_gPrng_080201d0:
    .word  gPrng                          @ 080201d0 40000003
DAT_080201d4:
    .word  0x00000203                     @ 080201d4 03020000
switchD_0801fee8__caseD_6:
    bl dispatch_puzzle_display_mode          @ 080201d8 0bf016fe
    cmp r0,#0x0                              @ 080201dc 0028
    bne LAB_080201e2                         @ 080201de 00d1
    b LAB_080202ec                           @ 080201e0 84e0
LAB_080201e2:
    ldr r0, DAT_0802020c                     @ 080201e2 0a48
    ldr r1, DAT_08020210                     @ 080201e4 0a49
    adds r0,r0,r1    @ 080201e6 4018
    movs r1,#0x7    @ 080201e8 0721
    ldrb r0,[r0,#0x0]                        @ 080201ea 0078
    ands r1,r0    @ 080201ec 0140
    cmp r1,#0x1                              @ 080201ee 0129
    beq LAB_08020234                         @ 080201f0 20d0
    cmp r1,#0x2                              @ 080201f2 0229
    beq LAB_0802022c                         @ 080201f4 1ad0
    cmp r1,#0x3                              @ 080201f6 0329
    beq LAB_08020224                         @ 080201f8 14d0
    cmp r1,#0x4                              @ 080201fa 0429
    beq LAB_0802021c                         @ 080201fc 0ed0
    ldr r0, DAT_08020214                     @ 080201fe 0548
    cmp r1,#0x5                              @ 08020200 0529
    bne LAB_08020236                         @ 08020202 18d1
    ldr r2, DAT_08020218                     @ 08020204 044a
    adds r0,r0,r2    @ 08020206 8018
    b LAB_08020236                           @ 08020208 15e0
    .zero  0x2
DAT_0802020c:
    .word  0x02000000                     @ 0802020c 00000002
DAT_08020210:
    .word  0x00006c2c                     @ 08020210 2c6c0000
DAT_08020214:
    .word  0x09dc01d8                     @ 08020214 d801dc09
DAT_08020218:
    .word  0x0003ab80                     @ 08020218 80ab0300
LAB_0802021c:
    ldr r0, DAT_08020220                     @ 0802021c 0048
    b LAB_08020236                           @ 0802021e 0ae0
DAT_08020220:
    .word  0x09def19a                     @ 08020220 9af1de09
LAB_08020224:
    ldr r0, DAT_08020228                     @ 08020224 0048
    b LAB_08020236                           @ 08020226 06e0
DAT_08020228:
    .word  0x09de2d00                     @ 08020228 002dde09
LAB_0802022c:
    ldr r0, DAT_08020230                     @ 0802022c 0048
    b LAB_08020236                           @ 0802022e 02e0
DAT_08020230:
    .word  0x09dd6982                     @ 08020230 8269dd09
LAB_08020234:
    ldr r0, DAT_0802025c                     @ 08020234 0948
LAB_08020236:
    movs r1,#0x1    @ 08020236 0121
    movs r2,#0x6    @ 08020238 0622
    bl render_card_name_centered_to_sprite_vram @ 0802023a 0bf023f9
LAB_0802023e:
    ldr r2, PTR_gPrng_08020260               @ 0802023e 084a
    ldr r3, DAT_08020264                     @ 08020240 084b
    adds r2,r2,r3    @ 08020242 d218
LAB_08020244:
    ldrh r3,[r2,#0x0]                        @ 08020244 1388
    lsls r1,r3,#0x12    @ 08020246 9904
    lsrs r1,r1,#0x18    @ 08020248 090e
    adds r1,#0x1    @ 0802024a 0131
    movs r0,#0xff    @ 0802024c ff20
    ands r1,r0    @ 0802024e 0140
    lsls r1,r1,#0x6    @ 08020250 8901
    ldr r0, DAT_08020268                     @ 08020252 0548
    ands r0,r3    @ 08020254 1840
    orrs r0,r1    @ 08020256 0843
    strh r0,[r2,#0x0]                        @ 08020258 1080
    b LAB_080202ec                           @ 0802025a 47e0
DAT_0802025c:
    .word  0x09dcafac                     @ 0802025c acafdc09
PTR_gPrng_08020260:
    .word  gPrng                          @ 08020260 40000003
DAT_08020264:
    .word  0x00000202                     @ 08020264 02020000
DAT_08020268:
    .word  0xffffc03f                     @ 08020268 3fc0ffff
switchD_0801fee8__caseD_7:
    bl render_puzzle_lp_digit_sprites        @ 0802026c 0bf0f2fa
    ldr r3, PTR_gPrng_080202a0               @ 08020270 0b4b
    movs r7,#0xa4    @ 08020272 a427
    lsls r7,r7,#0x1    @ 08020274 7f00
    adds r1,r3,r7    @ 08020276 d919
    movs r0,#0x3    @ 08020278 0320
    ldrh r1,[r1,#0x0]                        @ 0802027a 0988
    ands r0,r1    @ 0802027c 0840
    cmp r0,#0x0                              @ 0802027e 0028
    beq LAB_080202ec                         @ 08020280 34d0
    ldr r0, DAT_080202a4                     @ 08020282 0848
    adds r3,r3,r0    @ 08020284 1b18
    ldrh r2,[r3,#0x0]                        @ 08020286 1a88
    lsls r1,r2,#0x12    @ 08020288 9104
    lsrs r1,r1,#0x18    @ 0802028a 090e
    adds r1,#0x1    @ 0802028c 0131
    movs r0,#0xff    @ 0802028e ff20
    ands r1,r0    @ 08020290 0140
    lsls r1,r1,#0x6    @ 08020292 8901
    ldr r0, DAT_080202a8                     @ 08020294 0448
    ands r0,r2    @ 08020296 1040
    orrs r0,r1    @ 08020298 0843
    strh r0,[r3,#0x0]                        @ 0802029a 1880
    b LAB_080202ec                           @ 0802029c 26e0
    .zero  0x2
PTR_gPrng_080202a0:
    .word  gPrng                          @ 080202a0 40000003
DAT_080202a4:
    .word  0x00000202                     @ 080202a4 02020000
DAT_080202a8:
    .word  0xffffc03f                     @ 080202a8 3fc0ffff
switchD_0801fee8__caseD_8:
    bl tick_lp_display_and_fadein_check      @ 080202ac 0bf09afd
    cmp r0,#0x0                              @ 080202b0 0028
    beq LAB_080202ec                         @ 080202b2 1bd0
    ldr r0, DAT_080202cc                     @ 080202b4 0548
    ldr r0,[r0,#0x68]                        @ 080202b6 806e
    bl accrue_money_with_cap                 @ 080202b8 d8f030fe
    bl init_puzzle_wram_then_copy            @ 080202bc d9f0e4fc
    ldr r0, DAT_080202d0                     @ 080202c0 0348
    movs r1,#0x89    @ 080202c2 8921
    lsls r1,r1,#0x2    @ 080202c4 8900
    adds r0,r0,r1    @ 080202c6 4018
    ldr r0,[r0,#0x0]                         @ 080202c8 0068
    b LAB_080202f0                           @ 080202ca 11e0
DAT_080202cc:
    .word  0x02023360                     @ 080202cc 60330202
DAT_080202d0:
    .word  0x0201e2a0                     @ 080202d0 a0e20102
LAB_080202d4:
    bl tick_duel_field_fadein_step           @ 080202d4 acf0c2fb
    cmp r0,#0x0                              @ 080202d8 0028
    beq LAB_080202ec                         @ 080202da 07d0
    ldr r0, DAT_080202e8                     @ 080202dc 0248
    movs r2,#0x89    @ 080202de 8922
    lsls r2,r2,#0x2    @ 080202e0 9200
    adds r0,r0,r2    @ 080202e2 8018
    ldr r0,[r0,#0x0]                         @ 080202e4 0068
    b LAB_080202f0                           @ 080202e6 03e0
DAT_080202e8:
    .word  0x0201e2a0                     @ 080202e8 a0e20102
LAB_080202ec:
    movs r0,#0x80    @ 080202ec 8020
    lsls r0,r0,#0x1    @ 080202ee 4000
LAB_080202f0:
    pop {r3,r4,r5}                           @ 080202f0 38bc
    .hword 0x4698    @ 080202f2 9846
    .hword 0x46a1    @ 080202f4 a146
    .hword 0x46aa    @ 080202f6 aa46
    pop {r4,r5,r6,r7}                        @ 080202f8 f0bc
    pop {r1}                                 @ 080202fa 02bc
    bx r1                                    @ 080202fc 0847
    ROM_INCBIN 0x202fe, 0x36
    .word  0x08020338                     @ 08020334 38030208
PTR_DAT_08020338:
    .word  0x08020370                     @ 08020338 70030208
    .word  0x08020524                     @ 0802033c 24050208
    .word  0x08020544                     @ 08020340 44050208
    .word  0x08020670                     @ 08020344 70060208
    .word  0x080209f4                     @ 08020348 f4090208
    .word  0x08020a10                     @ 0802034c 100a0208
    .word  0x08020b50                     @ 08020350 500b0208
    .word  0x08020b6c                     @ 08020354 6c0b0208
    .word  0x08020b88                     @ 08020358 880b0208
    .word  0x08020ba4                     @ 0802035c a40b0208
    .word  0x08020d00                     @ 08020360 000d0208
    .word  0x08020d34                     @ 08020364 340d0208
    .word  0x08020d94                     @ 08020368 940d0208
    .word  0x08020d4c                     @ 0802036c 4c0d0208
DAT_08020370:
    ROM_INCBIN 0x20370, 0xa44

@ indeg=0, entered via function pointer table. Accepts r0 = card internal_id; maps it to a format string via multi-level binary comparison tree (ROM addresses 0x09dc... series); calls find_lp_entry_by_flag_and_type (r0=0, r1=card_id) to find matching LP record entry; if found reads [0x02006c2c] low 3 bits to select text encoding mode (0->JP, 1->EN etc) and picks format string; calls card_name_lookup_by_internal_id; calls expand_format_text_to_buf to fill card name into stack 0x100-byte buffer; calls render_game_string_with_number to render to screen. Returns r0=1 (found and rendered), r0=0 (not found). Card ID set A handled by this function: {0x1788, 0x146e, 0x112e, 0x0fe9, 0x111c, 0x1388, 0x138a, 0x15fa, 0x15b1, 0x1643, ...}.
@ 
@ Constants:
@ STACK_BUF_SIZE = 0x100 (256-byte stack buffer for format text)
@ STATE_ADDR = 0x02006c2c (encoding mode select)
@ LP_ENTRY_FLAG = 0 (find_lp_entry_by_flag_and_type r0 param)
@ CARD_ID_RANGE_A_MIN = 0x0fe9 (Perfectly Ultimate Great Moth)
@ CARD_ID_RANGE_A_MAX = 0x19ef (Elemental Hero Erikshieler)
render_lp_record_text_set_a:
    push {r4,r5,r6,lr}                       @ 08020db4 70b5
    sub sp,#0x100                            @ 08020db6 c0b0
    adds r4,r0,#0x0    @ 08020db8 041c
    ldr r0, DWORD_08020df0                   @ 08020dba 0d48
    cmp r4,r0                                @ 08020dbc 8442
    bne LAB_08020dc2                         @ 08020dbe 00d1
    b LAB_08020f16                           @ 08020dc0 a9e0
LAB_08020dc2:
    cmp r4,r0                                @ 08020dc2 8442
    bgt LAB_08020e78                         @ 08020dc4 58dc
    ldr r0, DWORD_08020df4                   @ 08020dc6 0b48
    cmp r4,r0                                @ 08020dc8 8442
    bne LAB_08020dce                         @ 08020dca 00d1
    b LAB_08020f16                           @ 08020dcc a3e0
LAB_08020dce:
    cmp r4,r0                                @ 08020dce 8442
    bgt LAB_08020e30                         @ 08020dd0 2edc
    ldr r0, DWORD_08020df8                   @ 08020dd2 0948
    cmp r4,r0                                @ 08020dd4 8442
    bne LAB_08020dda                         @ 08020dd6 00d1
    b LAB_08020f16                           @ 08020dd8 9de0
LAB_08020dda:
    cmp r4,r0                                @ 08020dda 8442
    bgt LAB_08020e10                         @ 08020ddc 18dc
    subs r0,#0x17    @ 08020dde 1738
    cmp r4,r0                                @ 08020de0 8442
    bne LAB_08020de6                         @ 08020de2 00d1
    b LAB_08020f16                           @ 08020de4 97e0
LAB_08020de6:
    cmp r4,r0                                @ 08020de6 8442
    bgt LAB_08020e00                         @ 08020de8 0adc
    ldr r0, DWORD_08020dfc                   @ 08020dea 0448
    b LAB_08020f12                           @ 08020dec 91e0
    .zero  0x2
DWORD_08020df0:
    .word  0x00001788                     @ 08020df0 88170000
DWORD_08020df4:
    .word  0x0000146e                     @ 08020df4 6e140000
DWORD_08020df8:
    .word  0x0000112e                     @ 08020df8 2e110000
DWORD_08020dfc:
    .word  0x00000fe9                     @ 08020dfc e90f0000
LAB_08020e00:
    ldr r0, DWORD_08020e0c                   @ 08020e00 0248
    cmp r4,r0                                @ 08020e02 8442
    bne LAB_08020e08                         @ 08020e04 00d1
    b LAB_08020f16                           @ 08020e06 86e0
LAB_08020e08:
    adds r0,#0x6    @ 08020e08 0630
    b LAB_08020f12                           @ 08020e0a 82e0
DWORD_08020e0c:
    .word  0x0000111c                     @ 08020e0c 1c110000
LAB_08020e10:
    ldr r0, DWORD_08020e24                   @ 08020e10 0448
    cmp r4,r0                                @ 08020e12 8442
    bgt LAB_08020e28                         @ 08020e14 08dc
    subs r0,#0x2    @ 08020e16 0238
    cmp r4,r0                                @ 08020e18 8442
    blt LAB_08020e1e                         @ 08020e1a 00db
    b LAB_08020f16                           @ 08020e1c 7be0
LAB_08020e1e:
    subs r0,#0xfa    @ 08020e1e fa38
    b LAB_08020f12                           @ 08020e20 77e0
    .zero  0x2
DWORD_08020e24:
    .word  0x00001388                     @ 08020e24 88130000
LAB_08020e28:
    ldr r0, DWORD_08020e2c                   @ 08020e28 0048
    b LAB_08020f12                           @ 08020e2a 72e0
DWORD_08020e2c:
    .word  0x0000138a                     @ 08020e2c 8a130000
LAB_08020e30:
    ldr r0, DWORD_08020e4c                   @ 08020e30 0648
    cmp r4,r0                                @ 08020e32 8442
    bgt LAB_08020e60                         @ 08020e34 14dc
    subs r0,#0x1    @ 08020e36 0138
    cmp r4,r0                                @ 08020e38 8442
    bge LAB_08020f16                         @ 08020e3a 6cda
    subs r0,#0x7b    @ 08020e3c 7b38
    cmp r4,r0                                @ 08020e3e 8442
    beq LAB_08020f16                         @ 08020e40 69d0
    cmp r4,r0                                @ 08020e42 8442
    bgt LAB_08020e50                         @ 08020e44 04dc
    subs r0,#0x4a    @ 08020e46 4a38
    b LAB_08020f12                           @ 08020e48 63e0
    .zero  0x2
DWORD_08020e4c:
    .word  0x000015fa                     @ 08020e4c fa150000
LAB_08020e50:
    ldr r0, DWORD_08020e5c                   @ 08020e50 0248
    cmp r4,r0                                @ 08020e52 8442
    beq LAB_08020f16                         @ 08020e54 5fd0
    adds r0,#0x3    @ 08020e56 0330
    b LAB_08020f12                           @ 08020e58 5be0
    .zero  0x2
DWORD_08020e5c:
    .word  0x000015b1                     @ 08020e5c b1150000
LAB_08020e60:
    ldr r0, DWORD_08020e74                   @ 08020e60 0448
    cmp r4,r0                                @ 08020e62 8442
    bge LAB_08020e68                         @ 08020e64 00da
    b LAB_08020f9c                           @ 08020e66 99e0
LAB_08020e68:
    adds r0,#0x2    @ 08020e68 0230
    cmp r4,r0                                @ 08020e6a 8442
    ble LAB_08020f16                         @ 08020e6c 53dd
    adds r0,#0xa7    @ 08020e6e a730
    b LAB_08020f12                           @ 08020e70 4fe0
    .zero  0x2
DWORD_08020e74:
    .word  0x00001643                     @ 08020e74 43160000
LAB_08020e78:
    ldr r0, DWORD_08020e9c                   @ 08020e78 0848
    cmp r4,r0                                @ 08020e7a 8442
    bgt LAB_08020ed8                         @ 08020e7c 2cdc
    subs r0,#0x1    @ 08020e7e 0138
    cmp r4,r0                                @ 08020e80 8442
    bge LAB_08020f16                         @ 08020e82 48da
    ldr r0, DWORD_08020ea0                   @ 08020e84 0648
    cmp r4,r0                                @ 08020e86 8442
    beq LAB_08020f16                         @ 08020e88 45d0
    cmp r4,r0                                @ 08020e8a 8442
    bgt LAB_08020eb4                         @ 08020e8c 12dc
    subs r0,#0x77    @ 08020e8e 7738
    cmp r4,r0                                @ 08020e90 8442
    beq LAB_08020f16                         @ 08020e92 40d0
    cmp r4,r0                                @ 08020e94 8442
    bgt LAB_08020ea4                         @ 08020e96 05dc
    subs r0,#0x4    @ 08020e98 0438
    b LAB_08020f12                           @ 08020e9a 3ae0
DWORD_08020e9c:
    .word  0x00001954                     @ 08020e9c 54190000
DWORD_08020ea0:
    .word  0x0000183d                     @ 08020ea0 3d180000
LAB_08020ea4:
    ldr r0, DWORD_08020eb0                   @ 08020ea4 0248
    cmp r4,r0                                @ 08020ea6 8442
    beq LAB_08020f16                         @ 08020ea8 35d0
    adds r0,#0x25    @ 08020eaa 2530
    b LAB_08020f12                           @ 08020eac 31e0
    .zero  0x2
DWORD_08020eb0:
    .word  0x000017c9                     @ 08020eb0 c9170000
LAB_08020eb4:
    ldr r0, DWORD_08020ec4                   @ 08020eb4 0348
    cmp r4,r0                                @ 08020eb6 8442
    beq LAB_08020f16                         @ 08020eb8 2dd0
    cmp r4,r0                                @ 08020eba 8442
    bgt LAB_08020ec8                         @ 08020ebc 04dc
    subs r0,#0x8    @ 08020ebe 0838
    b LAB_08020f12                           @ 08020ec0 27e0
    .zero  0x2
DWORD_08020ec4:
    .word  0x00001905                     @ 08020ec4 05190000
LAB_08020ec8:
    ldr r0, DWORD_08020ed4                   @ 08020ec8 0248
    cmp r4,r0                                @ 08020eca 8442
    beq LAB_08020f16                         @ 08020ecc 23d0
    adds r0,#0x1b    @ 08020ece 1b30
    b LAB_08020f12                           @ 08020ed0 1fe0
    .zero  0x2
DWORD_08020ed4:
    .word  0x00001936                     @ 08020ed4 36190000
LAB_08020ed8:
    ldr r0, DWORD_08020ef0                   @ 08020ed8 0548
    cmp r4,r0                                @ 08020eda 8442
    bgt LAB_08020ef4                         @ 08020edc 0adc
    subs r0,#0x2    @ 08020ede 0238
    cmp r4,r0                                @ 08020ee0 8442
    bge LAB_08020f16                         @ 08020ee2 18da
    subs r0,#0x4c    @ 08020ee4 4c38
    cmp r4,r0                                @ 08020ee6 8442
    beq LAB_08020f16                         @ 08020ee8 15d0
    adds r0,#0x35    @ 08020eea 3530
    b LAB_08020f12                           @ 08020eec 11e0
    .zero  0x2
DWORD_08020ef0:
    .word  0x000019a5                     @ 08020ef0 a5190000
LAB_08020ef4:
    ldr r0, DWORD_08020f0c                   @ 08020ef4 0548
    cmp r4,r0                                @ 08020ef6 8442
    beq LAB_08020f16                         @ 08020ef8 0dd0
    cmp r4,r0                                @ 08020efa 8442
    bgt LAB_08020f10                         @ 08020efc 08dc
    subs r0,#0x8    @ 08020efe 0838
    cmp r4,r0                                @ 08020f00 8442
    bgt LAB_08020f9c                         @ 08020f02 4bdc
    subs r0,#0x1    @ 08020f04 0138
    cmp r4,r0                                @ 08020f06 8442
    blt LAB_08020f9c                         @ 08020f08 48db
    b LAB_08020f16                           @ 08020f0a 04e0
DWORD_08020f0c:
    .word  0x000019d6                     @ 08020f0c d6190000
LAB_08020f10:
    ldr r0, DWORD_08020f4c                   @ 08020f10 0e48
LAB_08020f12:
    cmp r4,r0                                @ 08020f12 8442
    bne LAB_08020f9c                         @ 08020f14 42d1
LAB_08020f16:
    movs r0,#0x0    @ 08020f16 0020
    adds r1,r4,#0x0    @ 08020f18 211c
    bl find_lp_entry_by_flag_and_type        @ 08020f1a 10f015fa
    cmp r0,#0x0                              @ 08020f1e 0028
    beq LAB_08020f9c                         @ 08020f20 3cd0
    .hword 0x466e    @ 08020f22 6e46
    ldr r0, DWORD_08020f50                   @ 08020f24 0a48
    ldr r1, DWORD_08020f54                   @ 08020f26 0b49
    adds r0,r0,r1    @ 08020f28 4018
    movs r1,#0x7    @ 08020f2a 0721
    ldrb r0,[r0,#0x0]                        @ 08020f2c 0078
    ands r1,r0    @ 08020f2e 0140
    cmp r1,#0x1                              @ 08020f30 0129
    beq LAB_08020f78                         @ 08020f32 21d0
    cmp r1,#0x2                              @ 08020f34 0229
    beq LAB_08020f70                         @ 08020f36 1bd0
    cmp r1,#0x3                              @ 08020f38 0329
    beq LAB_08020f68                         @ 08020f3a 15d0
    cmp r1,#0x4                              @ 08020f3c 0429
    beq LAB_08020f60                         @ 08020f3e 0fd0
    ldr r5, DWORD_08020f58                   @ 08020f40 054d
    cmp r1,#0x5                              @ 08020f42 0529
    bne LAB_08020f7a                         @ 08020f44 19d1
    ldr r0, DWORD_08020f5c                   @ 08020f46 0548
    adds r5,r5,r0    @ 08020f48 2d18
    b LAB_08020f7a                           @ 08020f4a 16e0
DWORD_08020f4c:
    .word  0x000019ef                     @ 08020f4c ef190000
DWORD_08020f50:
    .word  0x02000000                     @ 08020f50 00000002
DWORD_08020f54:
    .word  0x00006c2c                     @ 08020f54 2c6c0000
DWORD_08020f58:
    .word  0x09dc2e62                     @ 08020f58 622edc09
DWORD_08020f5c:
    .word  0x0003ae88                     @ 08020f5c 88ae0300
LAB_08020f60:
    ldr r5, DWORD_08020f64                   @ 08020f60 004d
    b LAB_08020f7a                           @ 08020f62 0ae0
DWORD_08020f64:
    .word  0x09df2086                     @ 08020f64 8620df09
LAB_08020f68:
    ldr r5, DWORD_08020f6c                   @ 08020f68 004d
    b LAB_08020f7a                           @ 08020f6a 06e0
DWORD_08020f6c:
    .word  0x09de5d9c                     @ 08020f6c 9c5dde09
LAB_08020f70:
    ldr r5, DWORD_08020f74                   @ 08020f70 004d
    b LAB_08020f7a                           @ 08020f72 02e0
DWORD_08020f74:
    .word  0x09dd9a36                     @ 08020f74 369add09
LAB_08020f78:
    ldr r5, DWORD_08020f98                   @ 08020f78 074d
LAB_08020f7a:
    adds r0,r4,#0x0    @ 08020f7a 201c
    bl card_name_lookup_by_internal_id       @ 08020f7c cdf03efe
    adds r2,r0,#0x0    @ 08020f80 021c
    adds r0,r6,#0x0    @ 08020f82 301c
    adds r1,r5,#0x0    @ 08020f84 291c
    bl expand_format_text_to_buf             @ 08020f86 d4f0dff8
    .hword 0x4668    @ 08020f8a 6846
    movs r1,#0x7    @ 08020f8c 0721
    movs r2,#0x1    @ 08020f8e 0122
    bl render_game_string_with_number        @ 08020f90 0af0d6fc
    movs r0,#0x1    @ 08020f94 0120
    b LAB_08020f9e                           @ 08020f96 02e0
DWORD_08020f98:
    .word  0x09dcda66                     @ 08020f98 66dadc09
LAB_08020f9c:
    movs r0,#0x0    @ 08020f9c 0020
LAB_08020f9e:
    add sp,#0x100                            @ 08020f9e 40b0
    pop {r4,r5,r6}                           @ 08020fa0 70bc
    pop {r1}                                 @ 08020fa2 02bc
    bx r1                                    @ 08020fa4 0847
    .zero  0x2

@ indeg=0, structure fully symmetric with render_lp_record_text_set_a (0x08020db4). Accepts r0 = card internal_id; maps it to a different set of format strings (0x09dc-0x09df series ROM addresses) via a separate binary comparison tree; calls find_lp_entry_by_flag_and_type to find LP record; if found reads [0x02006c2c] to select encoding mode; calls card_name_lookup_by_internal_id; calls expand_format_text_to_buf; calls render_game_string_with_number to render. Returns r0=1/0. Card ID set B handled: {0x16dc, 0x16a3, 0x17ca, 0x184e, ...}.
@ 
@ Constants:
@ STACK_BUF_SIZE = 0x100 (256-byte stack buffer)
@ STATE_ADDR = 0x02006c2c
@ LP_ENTRY_FLAG = 0
@ CARD_ID_RANGE_B_MIN = 0x16a3 (Dark Scorpion Combination)
@ CARD_ID_RANGE_B_MAX = 0x184e (Fuh-Rin-Ka-Zan)
render_lp_record_text_set_b:
    push {r4,r5,r6,lr}                       @ 08020fa8 70b5
    sub sp,#0x100                            @ 08020faa c0b0
    adds r5,r0,#0x0    @ 08020fac 051c
    ldr r0, DWORD_08020fc8                   @ 08020fae 0648
    cmp r5,r0                                @ 08020fb0 8542
    beq LAB_08020ffc                         @ 08020fb2 23d0
    cmp r5,r0                                @ 08020fb4 8542
    bgt LAB_08020fdc                         @ 08020fb6 11dc
    subs r0,#0x62    @ 08020fb8 6238
    cmp r5,r0                                @ 08020fba 8542
    beq LAB_08020ffc                         @ 08020fbc 1ed0
    cmp r5,r0                                @ 08020fbe 8542
    bgt LAB_08020fcc                         @ 08020fc0 04dc
    subs r0,#0x4d    @ 08020fc2 4d38
    b LAB_08020ff8                           @ 08020fc4 18e0
    .zero  0x2
DWORD_08020fc8:
    .word  0x000016dc                     @ 08020fc8 dc160000
LAB_08020fcc:
    ldr r0, DWORD_08020fd8                   @ 08020fcc 0248
    cmp r5,r0                                @ 08020fce 8542
    beq LAB_08020ffc                         @ 08020fd0 14d0
    adds r0,#0x2c    @ 08020fd2 2c30
    b LAB_08020ff8                           @ 08020fd4 10e0
    .zero  0x2
DWORD_08020fd8:
    .word  0x000016a3                     @ 08020fd8 a3160000
LAB_08020fdc:
    ldr r0, DWORD_08020fec                   @ 08020fdc 0348
    cmp r5,r0                                @ 08020fde 8542
    beq LAB_08020ffc                         @ 08020fe0 0cd0
    cmp r5,r0                                @ 08020fe2 8542
    bgt LAB_08020ff0                         @ 08020fe4 04dc
    subs r0,#0x22    @ 08020fe6 2238
    b LAB_08020ff8                           @ 08020fe8 06e0
    .zero  0x2
DWORD_08020fec:
    .word  0x000017ca                     @ 08020fec ca170000
LAB_08020ff0:
    ldr r0, DWORD_08021034                   @ 08020ff0 1048
    cmp r5,r0                                @ 08020ff2 8542
    beq LAB_08020ffc                         @ 08020ff4 02d0
    adds r0,#0x3f    @ 08020ff6 3f30
LAB_08020ff8:
    cmp r5,r0                                @ 08020ff8 8542
    bne LAB_08021084                         @ 08020ffa 43d1
LAB_08020ffc:
    movs r0,#0x0    @ 08020ffc 0020
    adds r1,r5,#0x0    @ 08020ffe 291c
    bl find_lp_entry_by_flag_and_type        @ 08021000 10f0a2f9
    cmp r0,#0x0                              @ 08021004 0028
    beq LAB_08021084                         @ 08021006 3dd0
    .hword 0x466e    @ 08021008 6e46
    ldr r0, DWORD_08021038                   @ 0802100a 0b48
    ldr r1, DWORD_0802103c                   @ 0802100c 0b49
    adds r0,r0,r1    @ 0802100e 4018
    movs r1,#0x7    @ 08021010 0721
    ldrb r0,[r0,#0x0]                        @ 08021012 0078
    ands r1,r0    @ 08021014 0140
    cmp r1,#0x1                              @ 08021016 0129
    beq LAB_08021060                         @ 08021018 22d0
    cmp r1,#0x2                              @ 0802101a 0229
    beq LAB_08021058                         @ 0802101c 1cd0
    cmp r1,#0x3                              @ 0802101e 0329
    beq LAB_08021050                         @ 08021020 16d0
    cmp r1,#0x4                              @ 08021022 0429
    beq LAB_08021048                         @ 08021024 10d0
    ldr r4, DWORD_08021040                   @ 08021026 064c
    cmp r1,#0x5                              @ 08021028 0529
    bne LAB_08021062                         @ 0802102a 1ad1
    ldr r0, DWORD_08021044                   @ 0802102c 0548
    adds r4,r4,r0    @ 0802102e 2418
    b LAB_08021062                           @ 08021030 17e0
    .zero  0x2
DWORD_08021034:
    .word  0x0000184e                     @ 08021034 4e180000
DWORD_08021038:
    .word  0x02000000                     @ 08021038 00000002
DWORD_0802103c:
    .word  0x00006c2c                     @ 0802103c 2c6c0000
DWORD_08021040:
    .word  0x09dc2ea8                     @ 08021040 a82edc09
DWORD_08021044:
    .word  0x0003ae88                     @ 08021044 88ae0300
LAB_08021048:
    ldr r4, DWORD_0802104c                   @ 08021048 004c
    b LAB_08021062                           @ 0802104a 0ae0
DWORD_0802104c:
    .word  0x09df20cc                     @ 0802104c cc20df09
LAB_08021050:
    ldr r4, DWORD_08021054                   @ 08021050 004c
    b LAB_08021062                           @ 08021052 06e0
DWORD_08021054:
    .word  0x09de5e00                     @ 08021054 005ede09
LAB_08021058:
    ldr r4, DWORD_0802105c                   @ 08021058 004c
    b LAB_08021062                           @ 0802105a 02e0
DWORD_0802105c:
    .word  0x09dd9a86                     @ 0802105c 869add09
LAB_08021060:
    ldr r4, DWORD_08021080                   @ 08021060 074c
LAB_08021062:
    adds r0,r5,#0x0    @ 08021062 281c
    bl card_name_lookup_by_internal_id       @ 08021064 cdf0cafd
    adds r2,r0,#0x0    @ 08021068 021c
    adds r0,r6,#0x0    @ 0802106a 301c
    adds r1,r4,#0x0    @ 0802106c 211c
    bl expand_format_text_to_buf             @ 0802106e d4f06bf8
    .hword 0x4668    @ 08021072 6846
    movs r1,#0x7    @ 08021074 0721
    movs r2,#0x1    @ 08021076 0122
    bl render_game_string_with_number        @ 08021078 0af062fc
    movs r0,#0x1    @ 0802107c 0120
    b LAB_08021086                           @ 0802107e 02e0
DWORD_08021080:
    .word  0x09dcdaac                     @ 08021080 acdadc09
LAB_08021084:
    movs r0,#0x0    @ 08021084 0020
LAB_08021086:
    add sp,#0x100                            @ 08021086 40b0
    pop {r4,r5,r6}                           @ 08021088 70bc
    pop {r1}                                 @ 0802108a 02bc
    bx r1                                    @ 0802108c 0847
    ROM_INCBIN 0x2108e, 0xbe
    .word  0x08021150                     @ 0802114c 50110208
PTR_DAT_08021150:
    .word  0x080211fc                     @ 08021150 fc110208
    .word  0x080211b4                     @ 08021154 b4110208
    .word  0x080211b4                     @ 08021158 b4110208
    .word  0x080211b4                     @ 0802115c b4110208
    .word  0x080211b4                     @ 08021160 b4110208
    .word  0x080211b4                     @ 08021164 b4110208
    .word  0x080211b4                     @ 08021168 b4110208
    .word  0x080211b4                     @ 0802116c b4110208
    .word  0x080211b4                     @ 08021170 b4110208
    .word  0x080211fc                     @ 08021174 fc110208
    .word  0x080211b4                     @ 08021178 b4110208
    .word  0x080211b4                     @ 0802117c b4110208
    .word  0x080211fc                     @ 08021180 fc110208
    .word  0x080211fc                     @ 08021184 fc110208
    .word  0x080211fc                     @ 08021188 fc110208
    .word  0x080211b4                     @ 0802118c b4110208
    .word  0x080211fc                     @ 08021190 fc110208
    .word  0x080211b4                     @ 08021194 b4110208
    .word  0x080211b4                     @ 08021198 b4110208
    .word  0x080211b4                     @ 0802119c b4110208
    .word  0x080211b4                     @ 080211a0 b4110208
    .word  0x080211b4                     @ 080211a4 b4110208
    .word  0x080211b4                     @ 080211a8 b4110208
    .word  0x080211fc                     @ 080211ac fc110208
    .word  0x080211fc                     @ 080211b0 fc110208
DAT_080211b4:
    ROM_INCBIN 0x211b4, 0xc4
    .word  0x0802127c                     @ 08021278 7c120208
PTR_DAT_0802127c:
    .word  0x0802134c                     @ 0802127c 4c130208
    .word  0x080213e0                     @ 08021280 e0130208
    .word  0x08021474                     @ 08021284 74140208
    .word  0x08021508                     @ 08021288 08150208
    .word  0x08021674                     @ 0802128c 74160208
    .word  0x080216f4                     @ 08021290 f4160208
    .word  0x08021780                     @ 08021294 80170208
    .word  0x0802180c                     @ 08021298 0c180208
    .word  0x08021898                     @ 0802129c 98180208
    .word  0x08021924                     @ 080212a0 24190208
    .word  0x080219b0                     @ 080212a4 b0190208
    .word  0x08021a3c                     @ 080212a8 3c1a0208
    .word  0x08021ac8                     @ 080212ac c81a0208
    .word  0x08021b54                     @ 080212b0 541b0208
    .word  0x08021be0                     @ 080212b4 e01b0208
    .word  0x08021c6c                     @ 080212b8 6c1c0208
    .word  0x08021cf8                     @ 080212bc f81c0208
    .word  0x08021d84                     @ 080212c0 841d0208
    .word  0x08021e10                     @ 080212c4 101e0208
    .word  0x08021e9c                     @ 080212c8 9c1e0208
    .word  0x08021f30                     @ 080212cc 301f0208
    .word  0x08021fbc                     @ 080212d0 bc1f0208
    .word  0x08022048                     @ 080212d4 48200208
    .word  0x080220d4                     @ 080212d8 d4200208
    .word  0x08022160                     @ 080212dc 60210208
    .word  0x080221ec                     @ 080212e0 ec210208
    .word  0x080222b4                     @ 080212e4 b4220208
    .word  0x0802237c                     @ 080212e8 7c230208
    .word  0x08022440                     @ 080212ec 40240208
    .word  0x080224ec                     @ 080212f0 ec240208
    .word  0x0802256c                     @ 080212f4 6c250208
    .word  0x08022d22                     @ 080212f8 222d0208
    .word  0x08022d22                     @ 080212fc 222d0208
    .word  0x08022688                     @ 08021300 88260208
    .word  0x08022730                     @ 08021304 30270208
    .word  0x080227a8                     @ 08021308 a8270208
    .word  0x08022874                     @ 0802130c 74280208
    .word  0x08022894                     @ 08021310 94280208
    .word  0x08022920                     @ 08021314 20290208
    .word  0x08022940                     @ 08021318 40290208
    .word  0x08022960                     @ 0802131c 60290208
    .word  0x08022980                     @ 08021320 80290208
    .word  0x0802299c                     @ 08021324 9c290208
    .word  0x080229b8                     @ 08021328 b8290208
    .word  0x08022a50                     @ 0802132c 502a0208
    .word  0x08022b0c                     @ 08021330 0c2b0208
    .word  0x08022bb4                     @ 08021334 b42b0208
    .word  0x08022bd4                     @ 08021338 d42b0208
    .word  0x08022bf4                     @ 0802133c f42b0208
    .word  0x08022c14                     @ 08021340 142c0208
    .word  0x08022c34                     @ 08021344 342c0208
    .word  0x08022c84                     @ 08021348 842c0208
DAT_0802134c:
    ROM_INCBIN 0x2134c, 0x1ae0

@ Function pointer assigned to gMenuState+0x234 by 0x080e3a88, activated in switchD_080e3924 case 5 (after tick_pack_fadein completes) as scene step function. Reads gPrng+0x202 halfword, extracts bits[13:8] (step index [0..20]); if > 0x14 calls fetch_duel_next_state_overflow_exit (non-fadein overflow exit); otherwise indexes ROM step function table (base 0x08022e64) and tail-calls step function via .hword 0x4687 (mov pc,r0). Fully symmetric with tick_duel_puzzle_scene_step (0x0801f444) but uses a different step table, serving a different scene.
@ 
@ Constants:
@ STEP_IDX_OFFSET = 0x202 (gPrng+0x202, halfword)
@ MAX_STEP_IDX = 0x14 = 20
@ STEP_TABLE_BASE_D = 0x08022e64 (this function's step table)
@ gPrng = 0x03000040
tick_scene_step_by_step_table_d:
    push {r4,r5,r6,r7,lr}                    @ 08022e2c f0b5
    .hword 0x464f    @ 08022e2e 4f46
    .hword 0x4646    @ 08022e30 4646
    push {r6,r7}                             @ 08022e32 c0b4
    sub sp,#0x8                              @ 08022e34 82b0
    adds r2,r0,#0x0    @ 08022e36 021c
    ldr r0, PTR_gPrng_08022e58               @ 08022e38 0748
    ldr r1, DAT_08022e5c                     @ 08022e3a 0849
    adds r0,r0,r1    @ 08022e3c 4018
    ldrh r0,[r0,#0x0]                        @ 08022e3e 0088
    lsls r0,r0,#0x12    @ 08022e40 8004
    lsrs r0,r0,#0x18    @ 08022e42 000e
    cmp r0,#0x14                             @ 08022e44 1428
    bls LAB_08022e4c                         @ 08022e46 01d9
    bl fetch_duel_next_state_overflow_exit   @ 08022e48 00f009fd
LAB_08022e4c:
    lsls r0,r0,#0x2    @ 08022e4c 8000
    ldr r1, DAT_08022e60                     @ 08022e4e 0449
    adds r0,r0,r1    @ 08022e50 4018
    ldr r0,[r0,#0x0]                         @ 08022e52 0068
    .hword 0x4687    @ 08022e54 8746
    .zero  0x2
PTR_gPrng_08022e58:
    .word  gPrng                          @ 08022e58 40000003
DAT_08022e5c:
    .word  0x00000202                     @ 08022e5c 02020000
DAT_08022e60:
    .word  0x08022e64                     @ 08022e60 642e0208
PTR_DAT_08022e64:
    .word  0x08022eb8                     @ 08022e64 b82e0208
    .word  0x08022fdc                     @ 08022e68 dc2f0208
    .word  0x08023010                     @ 08022e6c 10300208
    .word  0x08023154                     @ 08022e70 54310208
    .word  0x080233dc                     @ 08022e74 dc330208
    .word  0x08023410                     @ 08022e78 10340208
    .word  0x08023558                     @ 08022e7c 58350208
    .word  0x0802358c                     @ 08022e80 8c350208
    .word  0x080235c0                     @ 08022e84 c0350208
    .word  0x08023614                     @ 08022e88 14360208
    .word  0x0802361c                     @ 08022e8c 1c360208
    .word  0x0802366c                     @ 08022e90 6c360208
    .word  0x08023774                     @ 08022e94 74370208
    .word  0x08023810                     @ 08022e98 10380208
    .word  0x0802385e                     @ 08022e9c 5e380208
    .word  0x0802385e                     @ 08022ea0 5e380208
    .word  0x0802385e                     @ 08022ea4 5e380208
    .word  0x0802385e                     @ 08022ea8 5e380208
    .word  0x0802385e                     @ 08022eac 5e380208
    .word  0x0802385e                     @ 08022eb0 5e380208
    .word  0x08023844                     @ 08022eb4 44380208
DAT_08022eb8:
    ROM_INCBIN 0x22eb8, 0x9a6

@ Inline exit fragment on overflow path of parent state machine FUN_08022e2c.
@ Triggered when field_state > 0x14.
@ Unlike poll_fadein_exit_to_duel_state (0x0801fe92), skips tick_duel_field_fadein_step;
@ directly reads [0x0201e2a0+0x224] (gDuelState+0x89*4) and returns the scene state word,
@ then executes full parent epilogue: add sp,#0x8; pop {r3,r4}; high-reg restore; pop {r4-r7}; bx r1.
@ Pointer table DAT_0x08022e64 indices 0xf..0x14 (6 entries) all point here.
@ Constants: DUEL_STATE_SLOT=[0x0201e2a0+0x224] (gDuelState+0x89*4).
fetch_duel_next_state_overflow_exit:
    ldr r0, DAT_08023878                     @ 0802385e 0648
    movs r4,#0x89    @ 08023860 8924
    lsls r4,r4,#0x2    @ 08023862 a400
    adds r0,r0,r4    @ 08023864 0019
    ldr r0,[r0,#0x0]                         @ 08023866 0068
    add sp,#0x8                              @ 08023868 02b0
    pop {r3,r4}                              @ 0802386a 18bc
    .hword 0x4698    @ 0802386c 9846
    .hword 0x46a1    @ 0802386e a146
    pop {r4,r5,r6,r7}                        @ 08023870 f0bc
    pop {r1}                                 @ 08023872 02bc
    bx r1                                    @ 08023874 0847
    .zero  0x2
DAT_08023878:
    .word  0x0201e2a0                     @ 08023878 a0e20102

@ datacrystal: 通用十进制绘制（被多处调用，含 0x080242c8 入口）
draw_decimal_with_offset:
    push {r4,r5,r6,r7,lr}                    @ 0802387c f0b5
    .hword 0x4657    @ 0802387e 5746
    .hword 0x464e    @ 08023880 4e46
    .hword 0x4645    @ 08023882 4546
    push {r5,r6,r7}                          @ 08023884 e0b4
    adds r7,r3,#0x0    @ 08023886 1f1c
    ldr r4,[sp,#0x20]                        @ 08023888 089c
    lsls r0,r0,#0x10    @ 0802388a 0004
    lsrs r0,r0,#0x10    @ 0802388c 000c
    .hword 0x4681    @ 0802388e 8146
    lsls r1,r1,#0x10    @ 08023890 0904
    lsls r2,r2,#0x10    @ 08023892 1204
    lsrs r2,r2,#0x10    @ 08023894 120c
    .hword 0x4692    @ 08023896 9246
    lsls r0,r1,#0x8    @ 08023898 0802
    lsrs r6,r0,#0x18    @ 0802389a 060e
    lsrs r1,r1,#0x18    @ 0802389c 090e
    .hword 0x4688    @ 0802389e 8846
    adds r0,r7,#0x0    @ 080238a0 381c
    bl count_bytes_until_null                @ 080238a2 d1f01dfe
    lsls r2,r6,#0x2    @ 080238a6 b200
    lsls r1,r0,#0x1    @ 080238a8 4100
    adds r1,r1,r0    @ 080238aa 0918
    subs r5,r2,r1    @ 080238ac 551a
    adds r0,r6,#0x0    @ 080238ae 301c
    .hword 0x4641    @ 080238b0 4146
    bl setup_line_buf_pos_and_font           @ 080238b2 cdf07ff9
    cmp r4,#0x0                              @ 080238b6 002c
    bne LAB_080238cc                         @ 080238b8 08d1
    ldr r1, DAT_080238c8                     @ 080238ba 0349
    movs r0,#0x2    @ 080238bc 0220
    rsbs r0,r0,#0    @ 080238be 4042
    ldrb r2,[r1,#0x8]                        @ 080238c0 0a7a
    ands r0,r2    @ 080238c2 1040
    b LAB_080238d4                           @ 080238c4 06e0
    .zero  0x2
DAT_080238c8:
    .word  0x02006ed0                     @ 080238c8 d06e0002
LAB_080238cc:
    ldr r1, DAT_08023988                     @ 080238cc 2e49
    movs r0,#0x1    @ 080238ce 0120
    ldrb r2,[r1,#0x8]                        @ 080238d0 0a7a
    orrs r0,r2    @ 080238d2 1043
LAB_080238d4:
    strb r0,[r1,#0x8]                        @ 080238d4 0872
    adds r3,r1,#0x0    @ 080238d6 0b1c
    movs r0,#0x2    @ 080238d8 0220
    ldrb r2,[r3,#0x8]                        @ 080238da 1a7a
    orrs r2,r0    @ 080238dc 0243
    strb r2,[r3,#0x8]                        @ 080238de 1a72
    ldr r4, PTR_font_jp_base_table_0802398c  @ 080238e0 2a4c
    lsls r1,r2,#0x1e    @ 080238e2 9107
    lsrs r1,r1,#0x1f    @ 080238e4 c90f
    lsls r1,r1,#0x2    @ 080238e6 8900
    lsls r0,r2,#0x1f    @ 080238e8 d007
    lsrs r0,r0,#0x1f    @ 080238ea c00f
    lsls r0,r0,#0x3    @ 080238ec c000
    adds r1,r1,r0    @ 080238ee 0918
    adds r1,r1,r4    @ 080238f0 0919
    ldr r0,[r1,#0x0]                         @ 080238f2 0868
    str r0,[r3,#0x4]                         @ 080238f4 5860
    cmp r5,#0x0                              @ 080238f6 002d
    bge LAB_08023922                         @ 080238f8 13da
    movs r0,#0x3    @ 080238fa 0320
    rsbs r0,r0,#0    @ 080238fc 4042
    ands r0,r2    @ 080238fe 1040
    strb r0,[r3,#0x8]                        @ 08023900 1872
    lsls r0,r0,#0x1f    @ 08023902 c007
    lsrs r0,r0,#0x1f    @ 08023904 c00f
    lsls r0,r0,#0x3    @ 08023906 c000
    adds r0,r0,r4    @ 08023908 0019
    ldr r0,[r0,#0x0]                         @ 0802390a 0068
    str r0,[r3,#0x4]                         @ 0802390c 5860
    adds r0,r7,#0x0    @ 0802390e 381c
    bl count_bytes_until_null                @ 08023910 d1f0e6fd
    lsls r2,r6,#0x3    @ 08023914 f200
    lsls r1,r0,#0x2    @ 08023916 8100
    adds r1,r1,r0    @ 08023918 0918
    subs r2,r2,r1    @ 0802391a 521a
    lsrs r0,r2,#0x1f    @ 0802391c d00f
    adds r2,r2,r0    @ 0802391e 1218
    asrs r5,r2,#0x1    @ 08023920 5510
LAB_08023922:
    .hword 0x4650    @ 08023922 5046
    lsrs r2,r0,#0x8    @ 08023924 020a
    cmp r2,#0x0                              @ 08023926 002a
    beq LAB_0802393c                         @ 08023928 08d0
    movs r1,#0x80    @ 0802392a 8021
    lsls r1,r1,#0x8    @ 0802392c 0902
    adds r0,r1,#0x0    @ 0802392e 081c
    orrs r2,r0    @ 08023930 0243
    adds r0,r5,#0x0    @ 08023932 281c
    movs r1,#0x3    @ 08023934 0321
    adds r3,r7,#0x0    @ 08023936 3b1c
    bl text_render_wrapper                   @ 08023938 cff0a0f8
LAB_0802393c:
    .hword 0x4650    @ 0802393c 5046
    lsls r2,r0,#0x18    @ 0802393e 0206
    lsrs r2,r2,#0x18    @ 08023940 120e
    adds r0,r5,#0x0    @ 08023942 281c
    movs r1,#0x3    @ 08023944 0321
    adds r3,r7,#0x0    @ 08023946 3b1c
    bl text_render_wrapper                   @ 08023948 cff098f8
    movs r4,#0x0    @ 0802394c 0024
    .hword 0x4649    @ 0802394e 4946
    lsls r5,r1,#0x5    @ 08023950 4d01
    cmp r4,r8                                @ 08023952 4445
    bge LAB_0802396e                         @ 08023954 0bda
LAB_08023956:
    lsls r0,r4,#0x10    @ 08023956 2004
    lsrs r0,r0,#0xb    @ 08023958 c00a
    add r0,r9                                @ 0802395a 4844
    lsls r0,r0,#0x5    @ 0802395c 4001
    ldr r2, DAT_08023990                     @ 0802395e 0c4a
    adds r0,r0,r2    @ 08023960 8018
    lsls r1,r6,#0x5    @ 08023962 7101
    bl zero_fill_by_halfword                 @ 08023964 d1f086fa
    adds r4,#0x1    @ 08023968 0134
    cmp r4,r8                                @ 0802396a 4445
    blt LAB_08023956                         @ 0802396c f3db
LAB_0802396e:
    ldr r1, DAT_08023990                     @ 0802396e 0849
    adds r0,r5,r1    @ 08023970 6818
    movs r1,#0x0    @ 08023972 0021
    bl write_line_buf_to_bg_tile_vram        @ 08023974 cff02eff
    pop {r3,r4,r5}                           @ 08023978 38bc
    .hword 0x4698    @ 0802397a 9846
    .hword 0x46a1    @ 0802397c a146
    .hword 0x46aa    @ 0802397e aa46
    pop {r4,r5,r6,r7}                        @ 08023980 f0bc
    pop {r0}                                 @ 08023982 01bc
    bx r0                                    @ 08023984 0047
    .zero  0x2
DAT_08023988:
    .word  0x02006ed0                     @ 08023988 d06e0002
PTR_font_jp_base_table_0802398c:
    .word  font_jp_base_table             @ 0802398c 54f8e509
DAT_08023990:
    .word  0x06010000                     @ 08023990 00000106

@ Called by FUN_08023b6c and 4 other callers (indeg=6). Renders one line of centered text to BG tile map VRAM. Entry: r0=x_base (tile column base, u16), r1=tile_row (row index, u16), r2=packed(palette<<24 | flags<<16), r3=y_offset (u16), [sp+0x2c]=string_ptr (u8*). Saves r5=x_base, r7=palette/flags, r6=tile_row, r8=y_offset, r9=another packed field. Calls count_bytes_until_null([sp+0x2c]) for byte count, computes center offset = x_base*4 - strlen*3, stores at [sp+8]. Reads [0x02000000+0x6c2c] = game language/settings byte, extracts bits[1:0] and bit0 for font mode flags, reads font_jp_base_table to select font set. Calls setup_line_buf_pos_and_font(x_base, flags) to init line buffer. Calls text_render_wrapper(offset, 3, string_ptr) to render to line buffer. Loops r4=0..2 (3 times): calls zero_fill_by_halfword on target BG tile row, wraps row number (r6 mod 0x1f+1). Calls commit_line_buffer_to_sprite_vram(target, 0). Then loops r4=0..5 writing BG tile map halfwords (tile index = r7+r4+base). Exit: void.
@ 
@ Constants:
@ - VRAM_BG_CHAR=0x06004000 (BG char data, write tile data)
@ - VRAM_BG_MAP=0x06000800 (BG tile map, one halfword per map entry)
@ - GAME_FLAGS=0x02000000+0x6c2c (language/font settings)
@ - BG_MAP_STRIDE=0x80 halfwords=0x100 bytes (0x80 tile map entries per row)
@ - TILE_ROW_MOD=0x1f+1=0x20 (tile row wraparound)
@ - RENDER_PASSES=3 (3 text_render_wrapper + 3 zero_fill passes)
render_centered_text_to_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 08023994 f0b5
    .hword 0x4657    @ 08023996 5746
    .hword 0x464e    @ 08023998 4e46
    .hword 0x4645    @ 0802399a 4546
    push {r5,r6,r7}                          @ 0802399c e0b4
    sub sp,#0xc                              @ 0802399e 83b0
    adds r4,r0,#0x0    @ 080239a0 041c
    lsls r4,r4,#0x10    @ 080239a2 2404
    lsrs r0,r4,#0x10    @ 080239a4 200c
    .hword 0x4682    @ 080239a6 8246
    lsls r1,r1,#0x10    @ 080239a8 0904
    lsrs r7,r1,#0x10    @ 080239aa 0f0c
    lsls r2,r2,#0x10    @ 080239ac 1204
    adds r1,r3,#0x0    @ 080239ae 191c
    lsls r1,r1,#0x10    @ 080239b0 0904
    .hword 0x4688    @ 080239b2 8846
    lsrs r1,r1,#0x10    @ 080239b4 090c
    str r1,[sp,#0x0]                         @ 080239b6 0091
    lsls r0,r2,#0x8    @ 080239b8 1002
    lsrs r5,r0,#0x18    @ 080239ba 050e
    lsrs r2,r2,#0x18    @ 080239bc 120e
    .hword 0x4691    @ 080239be 9146
    ldr r0,[sp,#0x2c]                        @ 080239c0 0b98
    bl count_bytes_until_null                @ 080239c2 d1f08dfd
    lsls r2,r5,#0x2    @ 080239c6 aa00
    lsls r1,r0,#0x1    @ 080239c8 4100
    adds r1,r1,r0    @ 080239ca 0918
    subs r2,r2,r1    @ 080239cc 521a
    str r2,[sp,#0x8]                         @ 080239ce 0292
    lsrs r6,r4,#0x15    @ 080239d0 660d
    movs r0,#0x1f    @ 080239d2 1f20
    ands r6,r0    @ 080239d4 0640
    adds r0,r5,#0x0    @ 080239d6 281c
    .hword 0x4649    @ 080239d8 4946
    bl setup_line_buf_pos_and_font           @ 080239da cdf0ebf8
    ldr r2, DAT_08023b0c                     @ 080239de 4b4a
    ldr r0, DAT_08023b10                     @ 080239e0 4b48
    ldr r3, DAT_08023b14                     @ 080239e2 4c4b
    adds r0,r0,r3    @ 080239e4 c018
    movs r1,#0x7    @ 080239e6 0721
    ldrb r0,[r0,#0x0]                        @ 080239e8 0078
    ands r1,r0    @ 080239ea 0140
    rsbs r1,r1,#0    @ 080239ec 4942
    lsrs r1,r1,#0x1f    @ 080239ee c90f
    movs r0,#0x2    @ 080239f0 0220
    rsbs r0,r0,#0    @ 080239f2 4042
    ldrb r3,[r2,#0x8]                        @ 080239f4 137a
    ands r0,r3    @ 080239f6 1840
    orrs r0,r1    @ 080239f8 0843
    movs r1,#0x2    @ 080239fa 0221
    orrs r0,r1    @ 080239fc 0843
    strb r0,[r2,#0x8]                        @ 080239fe 1072
    ldr r3, PTR_font_jp_base_table_08023b18  @ 08023a00 454b
    lsls r1,r0,#0x1e    @ 08023a02 8107
    lsrs r1,r1,#0x1f    @ 08023a04 c90f
    lsls r1,r1,#0x2    @ 08023a06 8900
    lsls r0,r0,#0x1f    @ 08023a08 c007
    lsrs r0,r0,#0x1f    @ 08023a0a c00f
    lsls r0,r0,#0x3    @ 08023a0c c000
    adds r1,r1,r0    @ 08023a0e 0918
    adds r1,r1,r3    @ 08023a10 c918
    ldr r0,[r1,#0x0]                         @ 08023a12 0868
    str r0,[r2,#0x4]                         @ 08023a14 5060
    .hword 0x4640    @ 08023a16 4046
    lsrs r2,r0,#0x18    @ 08023a18 020e
    cmp r2,#0x0                              @ 08023a1a 002a
    beq LAB_08023a30                         @ 08023a1c 08d0
    movs r1,#0x80    @ 08023a1e 8021
    lsls r1,r1,#0x8    @ 08023a20 0902
    adds r0,r1,#0x0    @ 08023a22 081c
    orrs r2,r0    @ 08023a24 0243
    ldr r0,[sp,#0x8]                         @ 08023a26 0298
    movs r1,#0x3    @ 08023a28 0321
    ldr r3,[sp,#0x2c]                        @ 08023a2a 0b9b
    bl text_render_wrapper                   @ 08023a2c cff026f8
LAB_08023a30:
    ldr r3,[sp,#0x0]                         @ 08023a30 009b
    lsls r2,r3,#0x18    @ 08023a32 1a06
    lsrs r2,r2,#0x18    @ 08023a34 120e
    ldr r0,[sp,#0x8]                         @ 08023a36 0298
    movs r1,#0x3    @ 08023a38 0321
    ldr r3,[sp,#0x2c]                        @ 08023a3a 0b9b
    bl text_render_wrapper                   @ 08023a3c cff01ef8
    lsls r4,r7,#0x5    @ 08023a40 7c01
    ldr r0, DAT_08023b1c                     @ 08023a42 3648
    adds r4,r4,r0    @ 08023a44 2418
    .hword 0x4649    @ 08023a46 4946
    lsls r0,r1,#0x5    @ 08023a48 4801
    adds r1,r5,#0x0    @ 08023a4a 291c
    muls r1,r0    @ 08023a4c 4143
    adds r0,r4,#0x0    @ 08023a4e 201c
    bl zero_fill_by_halfword                 @ 08023a50 d1f010fa
    adds r0,r4,#0x0    @ 08023a54 201c
    movs r1,#0x0    @ 08023a56 0021
    bl commit_line_buffer_to_sprite_vram     @ 08023a58 cff0f8f9
    movs r3,#0x1f    @ 08023a5c 1f23
    .hword 0x4698    @ 08023a5e 9846
    movs r4,#0x2    @ 08023a60 0224
LAB_08023a62:
    lsls r0,r6,#0x6    @ 08023a62 b001
    ldr r1, DAT_08023b20                     @ 08023a64 2e49
    adds r0,r0,r1    @ 08023a66 4018
    movs r1,#0x80    @ 08023a68 8021
    bl zero_fill_by_halfword                 @ 08023a6a d1f003fa
    adds r6,#0x2    @ 08023a6e 0236
    .hword 0x4643    @ 08023a70 4346
    ands r6,r3    @ 08023a72 1e40
    subs r4,#0x1    @ 08023a74 013c
    cmp r4,#0x0                              @ 08023a76 002c
    bge LAB_08023a62                         @ 08023a78 f3da
    movs r4,#0x0    @ 08023a7a 0024
    cmp r4,r9                                @ 08023a7c 4c45
    bge LAB_08023ab4                         @ 08023a7e 19da
LAB_08023a80:
    lsls r0,r4,#0x10    @ 08023a80 2004
    lsrs r0,r0,#0xb    @ 08023a82 c00a
    add r0,r10                               @ 08023a84 5044
    lsls r0,r0,#0x1    @ 08023a86 4000
    movs r1,#0xc0    @ 08023a88 c021
    lsls r1,r1,#0x13    @ 08023a8a c904
    adds r2,r0,r1    @ 08023a8c 4218
    adds r3,r4,#0x1    @ 08023a8e 631c
    cmp r5,#0x0                              @ 08023a90 002d
    beq LAB_08023aae                         @ 08023a92 0cd0
    movs r0,#0x80    @ 08023a94 8020
    lsls r0,r0,#0x6    @ 08023a96 8001
    adds r4,r0,#0x0    @ 08023a98 041c
    adds r1,r5,#0x0    @ 08023a9a 291c
LAB_08023a9c:
    adds r0,r7,r4    @ 08023a9c 3819
    strh r0,[r2,#0x0]                        @ 08023a9e 1080
    adds r2,#0x2    @ 08023aa0 0232
    adds r0,r7,#0x1    @ 08023aa2 781c
    lsls r0,r0,#0x10    @ 08023aa4 0004
    lsrs r7,r0,#0x10    @ 08023aa6 070c
    subs r1,#0x1    @ 08023aa8 0139
    cmp r1,#0x0                              @ 08023aaa 0029
    bne LAB_08023a9c                         @ 08023aac f6d1
LAB_08023aae:
    adds r4,r3,#0x0    @ 08023aae 1c1c
    cmp r4,r9                                @ 08023ab0 4c45
    blt LAB_08023a80                         @ 08023ab2 e5db
LAB_08023ab4:
    .hword 0x464c    @ 08023ab4 4c46
    cmp r4,#0x5                              @ 08023ab6 052c
    bgt LAB_08023afc                         @ 08023ab8 20dc
    .hword 0x4651    @ 08023aba 5146
    lsrs r7,r1,#0x5    @ 08023abc 4f09
    movs r6,#0x1f    @ 08023abe 1f26
    ands r6,r1    @ 08023ac0 0e40
LAB_08023ac2:
    adds r1,r7,r4    @ 08023ac2 3919
    adds r0,r1,#0x0    @ 08023ac4 081c
    cmp r1,#0x0                              @ 08023ac6 0029
    bge LAB_08023acc                         @ 08023ac8 00da
    adds r0,#0x1f    @ 08023aca 1f30
LAB_08023acc:
    asrs r0,r0,#0x5    @ 08023acc 4011
    lsls r0,r0,#0x5    @ 08023ace 4001
    subs r0,r1,r0    @ 08023ad0 081a
    adds r0,#0x20    @ 08023ad2 2030
    lsls r0,r0,#0x10    @ 08023ad4 0004
    lsrs r0,r0,#0xb    @ 08023ad6 c00a
    adds r0,r6,r0    @ 08023ad8 3018
    lsls r0,r0,#0x1    @ 08023ada 4000
    movs r1,#0xc0    @ 08023adc c021
    lsls r1,r1,#0x13    @ 08023ade c904
    adds r0,r0,r1    @ 08023ae0 4018
    adds r3,r4,#0x1    @ 08023ae2 631c
    cmp r5,#0x0                              @ 08023ae4 002d
    beq LAB_08023af6                         @ 08023ae6 06d0
    movs r2,#0x0    @ 08023ae8 0022
    adds r1,r5,#0x0    @ 08023aea 291c
LAB_08023aec:
    strh r2,[r0,#0x0]                        @ 08023aec 0280
    adds r0,#0x2    @ 08023aee 0230
    subs r1,#0x1    @ 08023af0 0139
    cmp r1,#0x0                              @ 08023af2 0029
    bne LAB_08023aec                         @ 08023af4 fad1
LAB_08023af6:
    adds r4,r3,#0x0    @ 08023af6 1c1c
    cmp r4,#0x5                              @ 08023af8 052c
    ble LAB_08023ac2                         @ 08023afa e2dd
LAB_08023afc:
    add sp,#0xc                              @ 08023afc 03b0
    pop {r3,r4,r5}                           @ 08023afe 38bc
    .hword 0x4698    @ 08023b00 9846
    .hword 0x46a1    @ 08023b02 a146
    .hword 0x46aa    @ 08023b04 aa46
    pop {r4,r5,r6,r7}                        @ 08023b06 f0bc
    pop {r0}                                 @ 08023b08 01bc
    bx r0                                    @ 08023b0a 0047
DAT_08023b0c:
    .word  0x02006ed0                     @ 08023b0c d06e0002
DAT_08023b10:
    .word  0x02000000                     @ 08023b10 00000002
DAT_08023b14:
    .word  0x00006c2c                     @ 08023b14 2c6c0000
PTR_font_jp_base_table_08023b18:
    .word  font_jp_base_table             @ 08023b18 54f8e509
DAT_08023b1c:
    .word  0x06004000                     @ 08023b1c 00400006
DAT_08023b20:
    .word  0x06000800                     @ 08023b20 00080006

@ Copies one row (0x20 halfwords) of icon palette data from ROM to BG palette VRAM
@ (0x05000220 + col*4 + row*0x80), and writes icon tile data via tile_2d_row_copy to
@ OBJ VRAM (0x06010000 + row*0x20*0x20 + col_tile*0x20). Called by init_duel_field_icon_and_bg_vram
@ during duel field initialization, one 3x3 tile block (width=3, height=3) per call.
@ 
@ Constants:
@ - 0x05000220 = BG palette VRAM base offset (palette slot base)
@ - 0x06010000 = OBJ tile VRAM base
copy_icon_tile_to_vram_row:
    push {r4,r5,lr}                          @ 08023b24 30b5
    adds r5,r2,#0x0    @ 08023b26 151c
    movs r4,#0x7    @ 08023b28 0724
    ands r4,r0    @ 08023b2a 0440
    asrs r2,r0,#0x3    @ 08023b2c c210
    lsls r4,r4,#0x2    @ 08023b2e a400
    lsls r2,r2,#0x7    @ 08023b30 d201
    adds r4,r4,r2    @ 08023b32 a418
    movs r2,#0x80    @ 08023b34 8022
    lsls r2,r2,#0x1    @ 08023b36 5200
    adds r4,r4,r2    @ 08023b38 a418
    lsls r4,r4,#0x10    @ 08023b3a 2404
    lsrs r4,r4,#0x10    @ 08023b3c 240c
    lsls r0,r0,#0x5    @ 08023b3e 4001
    ldr r2, DAT_08023b64                     @ 08023b40 084a
    adds r0,r0,r2    @ 08023b42 8018
    movs r2,#0x20    @ 08023b44 2022
    bl copy_bytes_by_halfword                @ 08023b46 d1f0adf9
    lsls r4,r4,#0x5    @ 08023b4a 6401
    ldr r0, DAT_08023b68                     @ 08023b4c 0648
    adds r4,r4,r0    @ 08023b4e 2418
    adds r0,r4,#0x0    @ 08023b50 201c
    adds r1,r5,#0x0    @ 08023b52 291c
    movs r2,#0x3    @ 08023b54 0322
    movs r3,#0x3    @ 08023b56 0323
    bl tile_2d_row_copy                      @ 08023b58 d3f0bcfc
    pop {r4,r5}                              @ 08023b5c 30bc
    pop {r0}                                 @ 08023b5e 01bc
    bx r0                                    @ 08023b60 0047
    .zero  0x2
DAT_08023b64:
    .word  0x05000220                     @ 08023b64 20020005
DAT_08023b68:
    .word  0x06010000                     @ 08023b68 00000106

@ Duel field initialization entry: writes control word to gPrng+0x174, clears DISPCNT,
@ calls reset_display_and_obj_vram + store_ewram_ctx_ptr_and_clear_mode_flags, then
@ configures BG0-BG3 BGCNT registers, calls reset_all_bg_scroll_regs_and_shadows,
@ uploads pack VRAM+palette, zero-fills BG tilemap/OBJ VRAM/EWRAM regions, copies palette,
@ loads pack tiles+map, uploads two tile+palette structs, loads another pack tile/map segment,
@ then iterates over player icon rows (gPlayerIcon array, up to 0x19 entries) calling
@ copy_icon_tile_to_vram_row to write icon data to OBJ VRAM and BG palette.
@ Called by three scene-switch functions (FUN_08025d58 / FUN_0802727c / FUN_08027a0c)
@ on entering the duel main field.
@ 
@ Constants:
@ - gPrng+0x174 = duel field control word (0x464f/0x4646 decode: write at 0xba*2=0x174 offset)
@ - BG0CNT = 0x04000008, set to 0x0004 (char base=1)
@ - 0xc000000 = OBJ VRAM base (OBJ tile clear target)
init_duel_field_icon_and_bg_vram:
    push {r4,r5,r6,r7,lr}                    @ 08023b6c f0b5
    .hword 0x464f    @ 08023b6e 4f46
    .hword 0x4646    @ 08023b70 4646
    push {r6,r7}                             @ 08023b72 c0b4
    sub sp,#0x4                              @ 08023b74 81b0
    ldr r0, PTR_gPrng_08023c74               @ 08023b76 3f48
    movs r1,#0xba    @ 08023b78 ba21
    lsls r1,r1,#0x1    @ 08023b7a 4900
    adds r0,r0,r1    @ 08023b7c 4018
    movs r2,#0x0    @ 08023b7e 0022
    ldr r1, DAT_08023c78                     @ 08023b80 3d49
    strh r1,[r0,#0x0]                        @ 08023b82 0180
    movs r0,#0x80    @ 08023b84 8020
    lsls r0,r0,#0x13    @ 08023b86 c004
    strh r2,[r0,#0x0]                        @ 08023b88 0280
    ldr r0, DAT_08023c7c                     @ 08023b8a 3c48
    bl reset_display_and_obj_vram            @ 08023b8c d3f072fd
    ldr r0, DAT_08023c80                     @ 08023b90 3b48
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 08023b92 d0f085fb
    ldr r1, PTR_BG0CNT_08023c84              @ 08023b96 3b49
    movs r0,#0x4    @ 08023b98 0420
    strh r0,[r1,#0x0]                        @ 08023b9a 0880
    adds r1,#0x2    @ 08023b9c 0231
    ldr r2, DAT_08023c88                     @ 08023b9e 3a4a
    adds r0,r2,#0x0    @ 08023ba0 101c
    strh r0,[r1,#0x0]                        @ 08023ba2 0880
    adds r1,#0x2    @ 08023ba4 0231
    ldr r3, DAT_08023c8c                     @ 08023ba6 394b
    adds r0,r3,#0x0    @ 08023ba8 181c
    strh r0,[r1,#0x0]                        @ 08023baa 0880
    adds r1,#0x2    @ 08023bac 0231
    ldr r4, DAT_08023c90                     @ 08023bae 384c
    adds r0,r4,#0x0    @ 08023bb0 201c
    strh r0,[r1,#0x0]                        @ 08023bb2 0880
    bl reset_all_bg_scroll_regs_and_shadows  @ 08023bb4 d1f068ff
    bl upload_pack_vram_and_palette          @ 08023bb8 d1f06eff
    ldr r0, DAT_08023c94                     @ 08023bbc 3548
    movs r4,#0x80    @ 08023bbe 8024
    lsls r4,r4,#0x8    @ 08023bc0 2402
    adds r1,r4,#0x0    @ 08023bc2 211c
    bl zero_fill_by_halfword                 @ 08023bc4 d1f056f9
    movs r0,#0xc0    @ 08023bc8 c020
    lsls r0,r0,#0x13    @ 08023bca c004
    movs r1,#0x80    @ 08023bcc 8021
    lsls r1,r1,#0x6    @ 08023bce 8901
    bl zero_fill_by_halfword                 @ 08023bd0 d1f050f9
    ldr r0, DAT_08023c98                     @ 08023bd4 3048
    adds r1,r4,#0x0    @ 08023bd6 211c
    bl zero_fill_by_halfword                 @ 08023bd8 d1f04cf9
    ldr r0, DAT_08023c9c                     @ 08023bdc 2f48
    ldr r1, DAT_08023ca0                     @ 08023bde 3049
    movs r2,#0x20    @ 08023be0 2022
    bl copy_bytes_by_halfword                @ 08023be2 d1f05ff9
    ldr r0, DAT_08023ca4                     @ 08023be6 2f48
    ldr r1, DAT_08023ca8                     @ 08023be8 2f49
    movs r2,#0x10    @ 08023bea 1022
    movs r3,#0x4    @ 08023bec 0423
    bl tile_2d_row_copy                      @ 08023bee d3f071fc
    ldr r3, DAT_08023cac                     @ 08023bf2 2e4b
    movs r0,#0x0    @ 08023bf4 0020
    movs r1,#0x10    @ 08023bf6 1021
    movs r2,#0x2    @ 08023bf8 0222
    bl load_pack_tile_and_map_to_vram        @ 08023bfa caf009fa
    ldr r2, DAT_08023cb0                     @ 08023bfe 2c4a
    movs r0,#0x20    @ 08023c00 2020
    movs r1,#0xf6    @ 08023c02 f621
    bl upload_tile_and_palette_from_struct   @ 08023c04 caf07cf9
    movs r1,#0x93    @ 08023c08 9321
    lsls r1,r1,#0x1    @ 08023c0a 4900
    ldr r2, DAT_08023cb4                     @ 08023c0c 294a
    movs r0,#0x40    @ 08023c0e 4020
    bl upload_tile_and_palette_from_struct   @ 08023c10 caf076f9
    movs r0,#0xc0    @ 08023c14 c020
    lsls r0,r0,#0x4    @ 08023c16 0001
    movs r2,#0x8c    @ 08023c18 8c22
    lsls r2,r2,#0x1    @ 08023c1a 5200
    ldr r3, DAT_08023cb8                     @ 08023c1c 264b
    movs r1,#0x30    @ 08023c1e 3021
    bl load_pack_tile_and_map_to_vram        @ 08023c20 caf0f6f9
    ldr r2, DAT_08023cbc                     @ 08023c24 254a
    ldrb r6,[r2,#0x4]                        @ 08023c26 1679
    lsrs r1,r6,#0x5    @ 08023c28 7109
    lsls r0,r1,#0x2    @ 08023c2a 8800
    adds r0,r0,r1    @ 08023c2c 4018
    movs r6,#0x0    @ 08023c2e 0026
    ldrh r2,[r2,#0x0]                        @ 08023c30 1288
    cmp r0,r2                                @ 08023c32 9042
    bge LAB_08023cf6                         @ 08023c34 5fda
    ldr r1, PTR_gPlayerIcon_08023cc0         @ 08023c36 2249
    .hword 0x4689    @ 08023c38 8946
    adds r4,r0,#0x0    @ 08023c3a 041c
    adds r1,r4,#0x0    @ 08023c3c 211c
    adds r1,#0xa    @ 08023c3e 0a31
    ldr r2, PTR_icon_palettes_base_08023cc4  @ 08023c40 204a
    .hword 0x4690    @ 08023c42 9046
    lsls r0,r1,#0x3    @ 08023c44 c800
    adds r0,r0,r1    @ 08023c46 4018
    lsls r7,r0,#0x5    @ 08023c48 4701
    lsls r1,r1,#0x5    @ 08023c4a 4901
    adds r5,r1,r2    @ 08023c4c 8d18
LAB_08023c4e:
    cmp r4,#0x19                             @ 08023c4e 192c
    bne LAB_08023ccc                         @ 08023c50 3cd1
    .hword 0x464b    @ 08023c52 4b46
    ldrb r3,[r3,#0x0]                        @ 08023c54 1b78
    lsls r0,r3,#0x19    @ 08023c56 5806
    lsrs r1,r0,#0x1c    @ 08023c58 010f
    lsls r1,r1,#0x5    @ 08023c5a 4901
    add r1,r8                                @ 08023c5c 4144
    lsrs r0,r0,#0x1c    @ 08023c5e 000f
    lsls r2,r0,#0x3    @ 08023c60 c200
    adds r2,r2,r0    @ 08023c62 1218
    lsls r2,r2,#0x5    @ 08023c64 5201
    ldr r0, PTR_icon_tiles_base_08023cc8     @ 08023c66 1848
    adds r2,r2,r0    @ 08023c68 1218
    movs r0,#0xa    @ 08023c6a 0a20
    bl copy_icon_tile_to_vram_row            @ 08023c6c fff75aff
    b LAB_08023cde                           @ 08023c70 35e0
    .zero  0x2
PTR_gPrng_08023c74:
    .word  gPrng                          @ 08023c74 40000003
DAT_08023c78:
    .word  0x00000601                     @ 08023c78 01060000
DAT_08023c7c:
    .word  0x0203eeb0                     @ 08023c7c b0ee0302
DAT_08023c80:
    .word  0x02029eb0                     @ 08023c80 b09e0202
PTR_BG0CNT_08023c84:
    .word  BG0CNT                         @ 08023c84 08000004
DAT_08023c88:
    .word  0x00000105                     @ 08023c88 05010000
DAT_08023c8c:
    .word  0x00000206                     @ 08023c8c 06020000
DAT_08023c90:
    .word  0x00000307                     @ 08023c90 07030000
DAT_08023c94:
    .word  0x06004000                     @ 08023c94 00400006
DAT_08023c98:
    .word  0x06010000                     @ 08023c98 00000106
DAT_08023c9c:
    .word  0x05000200                     @ 08023c9c 00020005
DAT_08023ca0:
    .word  0x09b97308                     @ 08023ca0 0873b909
DAT_08023ca4:
    .word  0x06010200                     @ 08023ca4 00020106
DAT_08023ca8:
    .word  0x09b97328                     @ 08023ca8 2873b909
DAT_08023cac:
    .word  0x09b95acc                     @ 08023cac cc5ab909
DAT_08023cb0:
    .word  0x09b953b4                     @ 08023cb0 b453b909
DAT_08023cb4:
    .word  0x09b96514                     @ 08023cb4 1465b909
DAT_08023cb8:
    .word  0x09b9487c                     @ 08023cb8 7c48b909
DAT_08023cbc:
    .word  0x02023360                     @ 08023cbc 60330202
PTR_gPlayerIcon_08023cc0:
    .word  gPlayerIcon                    @ 08023cc0 576e0002
PTR_icon_palettes_base_08023cc4:
    .word  icon_palettes_base             @ 08023cc4 90628909
PTR_icon_tiles_base_08023cc8:
    .word  icon_tiles_base                @ 08023cc8 30cf8809
LAB_08023ccc:
    adds r0,r4,#0x0    @ 08023ccc 201c
    movs r1,#0xf    @ 08023cce 0f21
    bl __modsi3                              @ 08023cd0 eaf0e4fc
    ldr r2, PTR_icon_tiles_base_08023d14     @ 08023cd4 0f4a
    adds r2,r7,r2    @ 08023cd6 ba18
    adds r1,r5,#0x0    @ 08023cd8 291c
    bl copy_icon_tile_to_vram_row            @ 08023cda fff723ff
LAB_08023cde:
    adds r4,#0x1    @ 08023cde 0134
    movs r0,#0x90    @ 08023ce0 9020
    lsls r0,r0,#0x1    @ 08023ce2 4000
    adds r7,r7,r0    @ 08023ce4 3f18
    adds r5,#0x20    @ 08023ce6 2035
    adds r6,#0x1    @ 08023ce8 0136
    cmp r6,#0xe                              @ 08023cea 0e2e
    bgt LAB_08023cf6                         @ 08023cec 03dc
    ldr r0, DAT_08023d18                     @ 08023cee 0a48
    ldrh r0,[r0,#0x0]                        @ 08023cf0 0088
    cmp r4,r0                                @ 08023cf2 8442
    blt LAB_08023c4e                         @ 08023cf4 abdb
LAB_08023cf6:
    ldr r0, DAT_08023d18                     @ 08023cf6 0848
    ldrb r0,[r0,#0x3]                        @ 08023cf8 c078
    lsls r0,r0,#0x1b    @ 08023cfa c006
    lsrs r1,r0,#0x1d    @ 08023cfc 410f
    cmp r1,#0x1                              @ 08023cfe 0129
    beq LAB_08023d1c                         @ 08023d00 0cd0
    cmp r1,#0x2                              @ 08023d02 0229
    beq LAB_08023db8                         @ 08023d04 58d0
    movs r6,#0x0    @ 08023d06 0026
    adds r0,r1,#0x0    @ 08023d08 081c
    cmp r6,r0                                @ 08023d0a 8642
    blt LAB_08023d10                         @ 08023d0c 00db
    b LAB_08023f56                           @ 08023d0e 22e1
LAB_08023d10:
    b LAB_08023ed8                           @ 08023d10 e2e0
    .zero  0x2
PTR_icon_tiles_base_08023d14:
    .word  icon_tiles_base                @ 08023d14 30cf8809
DAT_08023d18:
    .word  0x02023360                     @ 08023d18 60330202
LAB_08023d1c:
    ldr r0, DAT_08023d44                     @ 08023d1c 0948
    ldr r1, DAT_08023d48                     @ 08023d1e 0a49
    adds r0,r0,r1    @ 08023d20 4018
    movs r1,#0x7    @ 08023d22 0721
    ldrb r0,[r0,#0x0]                        @ 08023d24 0078
    ands r1,r0    @ 08023d26 0140
    cmp r1,#0x1                              @ 08023d28 0129
    beq LAB_08023d6c                         @ 08023d2a 1fd0
    cmp r1,#0x2                              @ 08023d2c 0229
    beq LAB_08023d64                         @ 08023d2e 19d0
    cmp r1,#0x3                              @ 08023d30 0329
    beq LAB_08023d5c                         @ 08023d32 13d0
    cmp r1,#0x4                              @ 08023d34 0429
    beq LAB_08023d54                         @ 08023d36 0dd0
    ldr r0, DAT_08023d4c                     @ 08023d38 0448
    cmp r1,#0x5                              @ 08023d3a 0529
    bne LAB_08023d6e                         @ 08023d3c 17d1
    ldr r2, DAT_08023d50                     @ 08023d3e 044a
    adds r0,r0,r2    @ 08023d40 8018
    b LAB_08023d6e                           @ 08023d42 14e0
DAT_08023d44:
    .word  0x02000000                     @ 08023d44 00000002
DAT_08023d48:
    .word  0x00006c2c                     @ 08023d48 2c6c0000
DAT_08023d4c:
    .word  0x09dc00e2                     @ 08023d4c e200dc09
DAT_08023d50:
    .word  0x0003ab5e                     @ 08023d50 5eab0300
LAB_08023d54:
    ldr r0, DAT_08023d58                     @ 08023d54 0048
    b LAB_08023d6e                           @ 08023d56 0ae0
DAT_08023d58:
    .word  0x09def06c                     @ 08023d58 6cf0de09
LAB_08023d5c:
    ldr r0, DAT_08023d60                     @ 08023d5c 0048
    b LAB_08023d6e                           @ 08023d5e 06e0
DAT_08023d60:
    .word  0x09de2bd2                     @ 08023d60 d22bde09
LAB_08023d64:
    ldr r0, DAT_08023d68                     @ 08023d64 0048
    b LAB_08023d6e                           @ 08023d66 02e0
DAT_08023d68:
    .word  0x09dd6860                     @ 08023d68 6068dd09
LAB_08023d6c:
    ldr r0, DAT_08023da0                     @ 08023d6c 0c48
LAB_08023d6e:
    str r0,[sp,#0x0]                         @ 08023d6e 0090
    ldr r0, DAT_08023da4                     @ 08023d70 0c48
    movs r1,#0x36    @ 08023d72 3621
    movs r2,#0x84    @ 08023d74 8422
    lsls r2,r2,#0x2    @ 08023d76 9200
    ldr r3, DAT_08023da8                     @ 08023d78 0b4b
    bl render_centered_text_to_bg_vram       @ 08023d7a fff70bfe
    ldr r0, DAT_08023dac                     @ 08023d7e 0b48
    ldr r3, DAT_08023db0                     @ 08023d80 0b4b
    movs r1,#0x20    @ 08023d82 2021
    movs r2,#0xf6    @ 08023d84 f622
    bl write_tile_row_to_vram                @ 08023d86 caf0e1f8
    ldr r0, PTR_gPrng_08023db4               @ 08023d8a 0a48
    movs r3,#0xf5    @ 08023d8c f523
    lsls r3,r3,#0x1    @ 08023d8e 5b00
    adds r2,r0,r3    @ 08023d90 c218
    movs r1,#0x0    @ 08023d92 0021
    strh r1,[r2,#0x0]                        @ 08023d94 1180
    movs r4,#0xf6    @ 08023d96 f624
    lsls r4,r4,#0x1    @ 08023d98 6400
    adds r0,r0,r4    @ 08023d9a 0019
    strh r1,[r0,#0x0]                        @ 08023d9c 0180
    b LAB_08023fa0                           @ 08023d9e ffe0
DAT_08023da0:
    .word  0x09dcaebe                     @ 08023da0 beaedc09
DAT_08023da4:
    .word  0x00000507                     @ 08023da4 07050000
DAT_08023da8:
    .word  0x00000f09                     @ 08023da8 090f0000
DAT_08023dac:
    .word  0x00000901                     @ 08023dac 01090000
DAT_08023db0:
    .word  0x09b953b4                     @ 08023db0 b453b909
PTR_gPrng_08023db4:
    .word  gPrng                          @ 08023db4 40000003
LAB_08023db8:
    ldr r0, DAT_08023de0                     @ 08023db8 0948
    ldr r6, DAT_08023de4                     @ 08023dba 0a4e
    adds r0,r0,r6    @ 08023dbc 8019
    movs r1,#0x7    @ 08023dbe 0721
    ldrb r0,[r0,#0x0]                        @ 08023dc0 0078
    ands r1,r0    @ 08023dc2 0140
    cmp r1,#0x1                              @ 08023dc4 0129
    beq LAB_08023e08                         @ 08023dc6 1fd0
    cmp r1,#0x2                              @ 08023dc8 0229
    beq LAB_08023e00                         @ 08023dca 19d0
    cmp r1,#0x3                              @ 08023dcc 0329
    beq LAB_08023df8                         @ 08023dce 13d0
    cmp r1,#0x4                              @ 08023dd0 0429
    beq LAB_08023df0                         @ 08023dd2 0dd0
    ldr r0, DAT_08023de8                     @ 08023dd4 0448
    cmp r1,#0x5                              @ 08023dd6 0529
    bne LAB_08023e0a                         @ 08023dd8 17d1
    ldr r1, DAT_08023dec                     @ 08023dda 0449
    adds r0,r0,r1    @ 08023ddc 4018
    b LAB_08023e0a                           @ 08023dde 14e0
DAT_08023de0:
    .word  0x02000000                     @ 08023de0 00000002
DAT_08023de4:
    .word  0x00006c2c                     @ 08023de4 2c6c0000
DAT_08023de8:
    .word  0x09dc00e2                     @ 08023de8 e200dc09
DAT_08023dec:
    .word  0x0003ab5e                     @ 08023dec 5eab0300
LAB_08023df0:
    ldr r0, DAT_08023df4                     @ 08023df0 0048
    b LAB_08023e0a                           @ 08023df2 0ae0
DAT_08023df4:
    .word  0x09def06c                     @ 08023df4 6cf0de09
LAB_08023df8:
    ldr r0, DAT_08023dfc                     @ 08023df8 0048
    b LAB_08023e0a                           @ 08023dfa 06e0
DAT_08023dfc:
    .word  0x09de2bd2                     @ 08023dfc d22bde09
LAB_08023e00:
    ldr r0, DAT_08023e04                     @ 08023e00 0048
    b LAB_08023e0a                           @ 08023e02 02e0
DAT_08023e04:
    .word  0x09dd6860                     @ 08023e04 6068dd09
LAB_08023e08:
    ldr r0, DAT_08023e44                     @ 08023e08 0e48
LAB_08023e0a:
    str r0,[sp,#0x0]                         @ 08023e0a 0090
    ldr r0, DAT_08023e48                     @ 08023e0c 0e48
    movs r1,#0x36    @ 08023e0e 3621
    movs r2,#0x84    @ 08023e10 8422
    lsls r2,r2,#0x2    @ 08023e12 9200
    ldr r3, DAT_08023e4c                     @ 08023e14 0d4b
    bl render_centered_text_to_bg_vram       @ 08023e16 fff7bdfd
    ldr r0, DAT_08023e50                     @ 08023e1a 0d48
    ldr r2, DAT_08023e54                     @ 08023e1c 0d4a
    adds r0,r0,r2    @ 08023e1e 8018
    movs r1,#0x7    @ 08023e20 0721
    ldrb r0,[r0,#0x0]                        @ 08023e22 0078
    ands r1,r0    @ 08023e24 0140
    cmp r1,#0x1                              @ 08023e26 0129
    beq LAB_08023e78                         @ 08023e28 26d0
    cmp r1,#0x2                              @ 08023e2a 0229
    beq LAB_08023e70                         @ 08023e2c 20d0
    cmp r1,#0x3                              @ 08023e2e 0329
    beq LAB_08023e68                         @ 08023e30 1ad0
    cmp r1,#0x4                              @ 08023e32 0429
    beq LAB_08023e60                         @ 08023e34 14d0
    ldr r0, DAT_08023e58                     @ 08023e36 0848
    cmp r1,#0x5                              @ 08023e38 0529
    bne LAB_08023e7a                         @ 08023e3a 1ed1
    ldr r3, DAT_08023e5c                     @ 08023e3c 074b
    adds r0,r0,r3    @ 08023e3e c018
    b LAB_08023e7a                           @ 08023e40 1be0
    .zero  0x2
DAT_08023e44:
    .word  0x09dcaebe                     @ 08023e44 beaedc09
DAT_08023e48:
    .word  0x000004a7                     @ 08023e48 a7040000
DAT_08023e4c:
    .word  0x00000f09                     @ 08023e4c 090f0000
DAT_08023e50:
    .word  0x02000000                     @ 08023e50 00000002
DAT_08023e54:
    .word  0x00006c2c                     @ 08023e54 2c6c0000
DAT_08023e58:
    .word  0x09dc00ec                     @ 08023e58 ec00dc09
DAT_08023e5c:
    .word  0x0003ab5c                     @ 08023e5c 5cab0300
LAB_08023e60:
    ldr r0, DAT_08023e64                     @ 08023e60 0048
    b LAB_08023e7a                           @ 08023e62 0ae0
DAT_08023e64:
    .word  0x09def076                     @ 08023e64 76f0de09
LAB_08023e68:
    ldr r0, DAT_08023e6c                     @ 08023e68 0048
    b LAB_08023e7a                           @ 08023e6a 06e0
DAT_08023e6c:
    .word  0x09de2bdc                     @ 08023e6c dc2bde09
LAB_08023e70:
    ldr r0, DAT_08023e74                     @ 08023e70 0048
    b LAB_08023e7a                           @ 08023e72 02e0
DAT_08023e74:
    .word  0x09dd6868                     @ 08023e74 6868dd09
LAB_08023e78:
    ldr r0, DAT_08023ebc                     @ 08023e78 1048
LAB_08023e7a:
    str r0,[sp,#0x0]                         @ 08023e7a 0090
    ldr r0, DAT_08023ec0                     @ 08023e7c 1048
    movs r1,#0x56    @ 08023e7e 5621
    movs r2,#0x84    @ 08023e80 8422
    lsls r2,r2,#0x2    @ 08023e82 9200
    ldr r3, DAT_08023ec4                     @ 08023e84 0f4b
    bl render_centered_text_to_bg_vram       @ 08023e86 fff785fd
    ldr r0, DAT_08023ec8                     @ 08023e8a 0f48
    ldr r4, DAT_08023ecc                     @ 08023e8c 0f4c
    movs r1,#0x20    @ 08023e8e 2021
    movs r2,#0xf6    @ 08023e90 f622
    adds r3,r4,#0x0    @ 08023e92 231c
    bl write_tile_row_to_vram                @ 08023e94 caf05af8
    ldr r0, DAT_08023ed0                     @ 08023e98 0d48
    movs r1,#0x20    @ 08023e9a 2021
    movs r2,#0xf6    @ 08023e9c f622
    adds r3,r4,#0x0    @ 08023e9e 231c
    bl write_tile_row_to_vram                @ 08023ea0 caf054f8
    ldr r0, PTR_gPrng_08023ed4               @ 08023ea4 0b48
    movs r4,#0xf5    @ 08023ea6 f524
    lsls r4,r4,#0x1    @ 08023ea8 6400
    adds r2,r0,r4    @ 08023eaa 0219
    movs r1,#0x0    @ 08023eac 0021
    strh r1,[r2,#0x0]                        @ 08023eae 1180
    movs r6,#0xf6    @ 08023eb0 f626
    lsls r6,r6,#0x1    @ 08023eb2 7600
    adds r0,r0,r6    @ 08023eb4 8019
    strh r1,[r0,#0x0]                        @ 08023eb6 0180
    b LAB_08023fa0                           @ 08023eb8 72e0
    .zero  0x2
DAT_08023ebc:
    .word  0x09dcaec6                     @ 08023ebc c6aedc09
DAT_08023ec0:
    .word  0x00000567                     @ 08023ec0 67050000
DAT_08023ec4:
    .word  0x00000f09                     @ 08023ec4 090f0000
DAT_08023ec8:
    .word  0x000008a1                     @ 08023ec8 a1080000
DAT_08023ecc:
    .word  0x09b953b4                     @ 08023ecc b453b909
DAT_08023ed0:
    .word  0x00000961                     @ 08023ed0 61090000
PTR_gPrng_08023ed4:
    .word  gPrng                          @ 08023ed4 40000003
LAB_08023ed8:
    movs r1,#0xbe    @ 08023ed8 be21
    lsls r1,r1,#0x4    @ 08023eda 0901
    adds r0,r6,r1    @ 08023edc 7018
    bl game_str_id_to_row                    @ 08023ede d0f09bff
    ldr r2, PTR_game_str_pointer_table_08023fb0 @ 08023ee2 334a
    lsls r0,r0,#0x10    @ 08023ee4 0004
    lsrs r0,r0,#0x10    @ 08023ee6 000c
    lsls r1,r0,#0x1    @ 08023ee8 4100
    adds r1,r1,r0    @ 08023eea 0918
    lsls r1,r1,#0x1    @ 08023eec 4900
    ldr r0, DAT_08023fb4                     @ 08023eee 3148
    ldr r3, DAT_08023fb8                     @ 08023ef0 314b
    adds r0,r0,r3    @ 08023ef2 c018
    ldrb r0,[r0,#0x0]                        @ 08023ef4 0078
    lsls r0,r0,#0x1d    @ 08023ef6 4007
    lsrs r0,r0,#0x1d    @ 08023ef8 400f
    adds r1,r1,r0    @ 08023efa 0918
    lsls r1,r1,#0x2    @ 08023efc 8900
    adds r1,r1,r2    @ 08023efe 8918
    ldr r5,[r1,#0x0]                         @ 08023f00 0d68
    ldr r0, PTR_game_str_ja_08023fbc         @ 08023f02 2e48
    adds r5,r5,r0    @ 08023f04 2d18
    lsls r4,r6,#0x1    @ 08023f06 7400
    adds r4,r4,r6    @ 08023f08 a419
    lsls r4,r4,#0x1    @ 08023f0a 6400
    adds r0,r4,#0x0    @ 08023f0c 201c
    adds r0,#0x20    @ 08023f0e 2030
    lsls r0,r0,#0x5    @ 08023f10 4001
    adds r0,#0x7    @ 08023f12 0730
    lsls r0,r0,#0x10    @ 08023f14 0004
    lsrs r0,r0,#0x10    @ 08023f16 000c
    lsls r1,r6,#0x15    @ 08023f18 7105
    movs r2,#0xd8    @ 08023f1a d822
    lsls r2,r2,#0xe    @ 08023f1c 9203
    adds r1,r1,r2    @ 08023f1e 8918
    lsrs r1,r1,#0x10    @ 08023f20 090c
    movs r2,#0x84    @ 08023f22 8422
    lsls r2,r2,#0x2    @ 08023f24 9200
    ldr r3, DAT_08023fc0                     @ 08023f26 264b
    str r5,[sp,#0x0]                         @ 08023f28 0095
    bl render_centered_text_to_bg_vram       @ 08023f2a fff733fd
    adds r4,#0x40    @ 08023f2e 4034
    lsls r4,r4,#0x5    @ 08023f30 6401
    adds r4,#0x1    @ 08023f32 0134
    lsls r4,r4,#0x10    @ 08023f34 2404
    lsrs r4,r4,#0x10    @ 08023f36 240c
    ldr r3, DAT_08023fc4                     @ 08023f38 224b
    adds r0,r4,#0x0    @ 08023f3a 201c
    movs r1,#0x20    @ 08023f3c 2021
    movs r2,#0xf6    @ 08023f3e f622
    bl write_tile_row_to_vram                @ 08023f40 caf004f8
    adds r6,#0x1    @ 08023f44 0136
    ldr r0, DAT_08023fc8                     @ 08023f46 2048
    ldrb r0,[r0,#0x3]                        @ 08023f48 c078
    lsls r0,r0,#0x1b    @ 08023f4a c006
    lsrs r0,r0,#0x1d    @ 08023f4c 400f
    cmp r6,r0                                @ 08023f4e 8642
    bge LAB_08023f56                         @ 08023f50 01da
    cmp r6,#0x4                              @ 08023f52 042e
    ble LAB_08023ed8                         @ 08023f54 c0dd
LAB_08023f56:
    ldr r5, PTR_gPrng_08023fcc               @ 08023f56 1d4d
    ldr r2, DAT_08023fc8                     @ 08023f58 1b4a
    ldrb r4,[r2,#0x3]                        @ 08023f5a d478
    lsrs r3,r4,#0x5    @ 08023f5c 6309
    movs r1,#0x1f    @ 08023f5e 1f21
    adds r0,r1,#0x0    @ 08023f60 081c
    ldrb r6,[r2,#0x4]                        @ 08023f62 1679
    ands r0,r6    @ 08023f64 3040
    lsls r0,r0,#0x3    @ 08023f66 c000
    orrs r0,r3    @ 08023f68 1843
    rsbs r0,r0,#0    @ 08023f6a 4042
    movs r6,#0xf5    @ 08023f6c f526
    lsls r6,r6,#0x1    @ 08023f6e 7600
    adds r4,r5,r6    @ 08023f70 ac19
    strh r0,[r4,#0x0]                        @ 08023f72 2080
    ldrb r0,[r2,#0x4]                        @ 08023f74 1079
    ands r1,r0    @ 08023f76 0140
    lsls r1,r1,#0x3    @ 08023f78 c900
    orrs r1,r3    @ 08023f7a 1943
    rsbs r1,r1,#0    @ 08023f7c 4942
    movs r3,#0xf6    @ 08023f7e f623
    lsls r3,r3,#0x1    @ 08023f80 5b00
    adds r0,r5,r3    @ 08023f82 e818
    strh r1,[r0,#0x0]                        @ 08023f84 0180
    ldr r0, DAT_08023fd0                     @ 08023f86 1248
    ldrh r4,[r2,#0x8]                        @ 08023f88 1489
    ands r0,r4    @ 08023f8a 2040
    strh r0,[r2,#0x8]                        @ 08023f8c 1081
    movs r0,#0x7f    @ 08023f8e 7f20
    ldrb r6,[r2,#0xb]                        @ 08023f90 d67a
    ands r0,r6    @ 08023f92 3040
    strb r0,[r2,#0xb]                        @ 08023f94 d072
    movs r0,#0x80    @ 08023f96 8020
    rsbs r0,r0,#0    @ 08023f98 4042
    ldrb r1,[r2,#0xc]                        @ 08023f9a 117b
    ands r0,r1    @ 08023f9c 0840
    strb r0,[r2,#0xc]                        @ 08023f9e 1073
LAB_08023fa0:
    add sp,#0x4                              @ 08023fa0 01b0
    pop {r3,r4}                              @ 08023fa2 18bc
    .hword 0x4698    @ 08023fa4 9846
    .hword 0x46a1    @ 08023fa6 a146
    pop {r4,r5,r6,r7}                        @ 08023fa8 f0bc
    pop {r0}                                 @ 08023faa 01bc
    bx r0                                    @ 08023fac 0047
    .zero  0x2
PTR_game_str_pointer_table_08023fb0:
    .word  game_str_pointer_table         @ 08023fb0 400f0008
DAT_08023fb4:
    .word  0x02000000                     @ 08023fb4 00000002
DAT_08023fb8:
    .word  0x00006c2c                     @ 08023fb8 2c6c0000
PTR_game_str_ja_08023fbc:
    .word  game_str_ja                    @ 08023fbc 109cdb09
DAT_08023fc0:
    .word  0x00000f09                     @ 08023fc0 090f0000
DAT_08023fc4:
    .word  0x09b953b4                     @ 08023fc4 b453b909
DAT_08023fc8:
    .word  0x02023360                     @ 08023fc8 60330202
PTR_gPrng_08023fcc:
    .word  gPrng                          @ 08023fcc 40000003
DAT_08023fd0:
    .word  0xffff807f                     @ 08023fd0 7f80ffff

@ Renders a win count (or corresponding value) as three groups of OAM digit sprites,
@ 3 sprites per group (loop 3 times via movs r5,#0x2; bge). The three groups correspond
@ to hundreds/tens/ones place, using __modsi3 + __divsi3 divide-by-10 to extract each digit,
@ adding tile base 0x474 to get the digit tile index, then calling
@ write_oam_entry_from_packed_args to write to OAM. Finally writes two fixed entries
@ (0x4040 / 0x454). Called by render_opp_wins_display_oam (tag: opp_wins) in the
@ opponent wins display scene.
@ 
@ Constants:
@ - 0x02000000+0x6e60 = gPrng+0x6e60 (frame scene control word offset 1)
@ - 0x02000000+0x6e62 = gPrng+0x6e62 (frame scene control word offset 2)
@ - 0x474 = digit tile base index
@ - 0x4040 = OAM attr0[y=0x40] | attr1[x=0x40] (separator sprite coords, off-screen)
@ - 0x454 = OAM attr2 tile index (DAT_08024110, first fixed sprite tile index)
@ - 0x458 = 0x8b << 3 (second fixed sprite tile index, computed inline)
render_win_count_digits_to_oam:
    push {r4,r5,r6,r7,lr}                    @ 08023fd4 f0b5
    .hword 0x4657    @ 08023fd6 5746
    .hword 0x464e    @ 08023fd8 4e46
    .hword 0x4645    @ 08023fda 4546
    push {r5,r6,r7}                          @ 08023fdc e0b4
    sub sp,#0x14                             @ 08023fde 85b0
    .hword 0x4682    @ 08023fe0 8246
    str r1,[sp,#0x0]                         @ 08023fe2 0091
    ldr r0, DAT_080240fc                     @ 08023fe4 4548
    lsls r2,r2,#0x2    @ 08023fe6 9200
    adds r2,r2,r0    @ 08023fe8 1218
    ldr r0, DAT_08024100                     @ 08023fea 4548
    adds r1,r2,r0    @ 08023fec 1118
    ldrh r3,[r1,#0x0]                        @ 08023fee 0b88
    lsls r0,r3,#0x14    @ 08023ff0 1805
    lsrs r7,r0,#0x14    @ 08023ff2 070d
    ldr r0,[r1,#0x0]                         @ 08023ff4 0868
    lsls r0,r0,#0xa    @ 08023ff6 8002
    lsrs r0,r0,#0x16    @ 08023ff8 800d
    .hword 0x4681    @ 08023ffa 8146
    ldr r0, DAT_08024104                     @ 08023ffc 4148
    adds r2,r2,r0    @ 08023ffe 1218
    ldrh r2,[r2,#0x0]                        @ 08024000 1288
    lsrs r2,r2,#0x6    @ 08024002 9209
    .hword 0x4690    @ 08024004 9046
    ldr r0,[sp,#0x0]                         @ 08024006 0098
    adds r0,#0x1a    @ 08024008 1a30
    lsls r1,r0,#0x10    @ 0802400a 0104
    str r1,[sp,#0x4]                         @ 0802400c 0191
    str r0,[sp,#0x10]                        @ 0802400e 0490
    .hword 0x4656    @ 08024010 5646
    adds r6,#0x2    @ 08024012 0236
    movs r5,#0x2    @ 08024014 0225
LAB_08024016:
    adds r4,r6,#0x0    @ 08024016 341c
    ldr r3,[sp,#0x4]                         @ 08024018 019b
    orrs r4,r3    @ 0802401a 1c43
    adds r0,r7,#0x0    @ 0802401c 381c
    movs r1,#0xa    @ 0802401e 0a21
    bl __modsi3                              @ 08024020 eaf03cfb
    adds r2,r0,#0x0    @ 08024024 021c
    ldr r0, DAT_08024108                     @ 08024026 3848
    adds r2,r2,r0    @ 08024028 1218
    lsls r2,r2,#0x10    @ 0802402a 1204
    lsrs r2,r2,#0x10    @ 0802402c 120c
    adds r0,r4,#0x0    @ 0802402e 201c
    movs r1,#0x0    @ 08024030 0021
    bl write_oam_entry_from_packed_args      @ 08024032 d2f09bf8
    adds r0,r7,#0x0    @ 08024036 381c
    movs r1,#0xa    @ 08024038 0a21
    bl __divsi3                              @ 0802403a eaf0e3fa
    adds r7,r0,#0x0    @ 0802403e 071c
    subs r6,#0x4    @ 08024040 043e
    subs r5,#0x1    @ 08024042 013d
    cmp r5,#0x0                              @ 08024044 002d
    bge LAB_08024016                         @ 08024046 e6da
    .hword 0x4657    @ 08024048 5746
    subs r7,#0xe    @ 0802404a 0e3f
    ldr r1,[sp,#0x0]                         @ 0802404c 0099
    adds r1,#0x19    @ 0802404e 1931
    str r1,[sp,#0xc]                         @ 08024050 0391
    .hword 0x4653    @ 08024052 5346
    adds r3,#0x12    @ 08024054 1233
    str r3,[sp,#0x8]                         @ 08024056 0293
    .hword 0x4656    @ 08024058 5646
    adds r6,#0x15    @ 0802405a 1536
    movs r5,#0x2    @ 0802405c 0225
LAB_0802405e:
    ldr r0,[sp,#0x10]                        @ 0802405e 0498
    lsls r4,r0,#0x10    @ 08024060 0404
    orrs r4,r6    @ 08024062 3443
    .hword 0x4640    @ 08024064 4046
    movs r1,#0xa    @ 08024066 0a21
    bl __modsi3                              @ 08024068 eaf018fb
    adds r2,r0,#0x0    @ 0802406c 021c
    ldr r1, DAT_08024108                     @ 0802406e 2649
    adds r2,r2,r1    @ 08024070 5218
    lsls r2,r2,#0x10    @ 08024072 1204
    lsrs r2,r2,#0x10    @ 08024074 120c
    adds r0,r4,#0x0    @ 08024076 201c
    movs r1,#0x0    @ 08024078 0021
    bl write_oam_entry_from_packed_args      @ 0802407a d2f077f8
    .hword 0x4640    @ 0802407e 4046
    movs r1,#0xa    @ 08024080 0a21
    bl __divsi3                              @ 08024082 eaf0bffa
    .hword 0x4680    @ 08024086 8046
    subs r6,#0x4    @ 08024088 043e
    subs r5,#0x1    @ 0802408a 013d
    cmp r5,#0x0                              @ 0802408c 002d
    bge LAB_0802405e                         @ 0802408e e6da
    .hword 0x4656    @ 08024090 5646
    adds r6,#0x28    @ 08024092 2836
    movs r5,#0x2    @ 08024094 0225
LAB_08024096:
    ldr r3,[sp,#0x10]                        @ 08024096 049b
    lsls r4,r3,#0x10    @ 08024098 1c04
    orrs r4,r6    @ 0802409a 3443
    .hword 0x4648    @ 0802409c 4846
    movs r1,#0xa    @ 0802409e 0a21
    bl __modsi3                              @ 080240a0 eaf0fcfa
    adds r2,r0,#0x0    @ 080240a4 021c
    ldr r0, DAT_08024108                     @ 080240a6 1848
    adds r2,r2,r0    @ 080240a8 1218
    lsls r2,r2,#0x10    @ 080240aa 1204
    lsrs r2,r2,#0x10    @ 080240ac 120c
    adds r0,r4,#0x0    @ 080240ae 201c
    movs r1,#0x0    @ 080240b0 0021
    bl write_oam_entry_from_packed_args      @ 080240b2 d2f05bf8
    .hword 0x4648    @ 080240b6 4846
    movs r1,#0xa    @ 080240b8 0a21
    bl __divsi3                              @ 080240ba eaf0a3fa
    .hword 0x4681    @ 080240be 8146
    subs r6,#0x4    @ 080240c0 043e
    subs r5,#0x1    @ 080240c2 013d
    cmp r5,#0x0                              @ 080240c4 002d
    bge LAB_08024096                         @ 080240c6 e6da
    ldr r1,[sp,#0xc]                         @ 080240c8 0399
    lsls r4,r1,#0x10    @ 080240ca 0c04
    orrs r7,r4    @ 080240cc 2743
    ldr r5, DAT_0802410c                     @ 080240ce 0f4d
    ldr r2, DAT_08024110                     @ 080240d0 0f4a
    adds r0,r7,#0x0    @ 080240d2 381c
    adds r1,r5,#0x0    @ 080240d4 291c
    bl write_oam_entry_from_packed_args      @ 080240d6 d2f049f8
    ldr r3,[sp,#0x8]                         @ 080240da 029b
    orrs r3,r4    @ 080240dc 2343
    str r3,[sp,#0x8]                         @ 080240de 0293
    movs r2,#0x8b    @ 080240e0 8b22
    lsls r2,r2,#0x3    @ 080240e2 d200
    adds r0,r3,#0x0    @ 080240e4 181c
    adds r1,r5,#0x0    @ 080240e6 291c
    bl write_oam_entry_from_packed_args      @ 080240e8 d2f040f8
    add sp,#0x14                             @ 080240ec 05b0
    pop {r3,r4,r5}                           @ 080240ee 38bc
    .hword 0x4698    @ 080240f0 9846
    .hword 0x46a1    @ 080240f2 a146
    .hword 0x46aa    @ 080240f4 aa46
    pop {r4,r5,r6,r7}                        @ 080240f6 f0bc
    pop {r0}                                 @ 080240f8 01bc
    bx r0                                    @ 080240fa 0047
DAT_080240fc:
    .word  0x02000000                     @ 080240fc 00000002
DAT_08024100:
    .word  0x00006e60                     @ 08024100 606e0000
DAT_08024104:
    .word  0x00006e62                     @ 08024104 626e0000
DAT_08024108:
    .word  0x00000474                     @ 08024108 74040000
DAT_0802410c:
    .word  0x00004040                     @ 0802410c 40400000
DAT_08024110:
    .word  0x00000454                     @ 08024110 54040000

@ Opponent wins display OAM update hub. First checks if the frame control word at
@ gPrng+0x202 equals 0x140 (i.e. 0xa0<<1, compared as (halfword[gPrng+0x202]&0x3fc0)):
@ if satisfied, extracts the card/mode flag at gPrng+0x203, tests bit2 to decide
@ whether to activate the win digit render path. Then sets a fixed OAM entry sequence
@ (4 rows x 4 columns of sprites), then based on bits[7:5] of byte at 0x02023360+0x4
@ and gPrng+0x6c2c state selects the font address, calls card_name_lookup_by_internal_id
@ to query card name, then calls draw_decimal_with_offset to render digits, and writes
@ the mode flag byte at 0x02023360+8. Triggered by 8 callers at various duel field events.
@ 
@ Constants:
@ - gPrng+0x202 = 0x02000000+0x202 (frame control word 1)
@ - gPrng+0x203 = 0x02000000+0x203 (frame control word 2)
@ - 0x3fc0 = 0xff << 6 (halfword mask bits[13:6], extracts opponent wins control field)
@ - 0x140 = 0xa0 << 1 (activation threshold for opponent wins render)
@ - 0x204 = 0x81*4 (gPrng card data field offset)
@ - gPrng+0x6e5c = scene frame counter offset (deck record table index)
render_opp_wins_display_oam:
    push {r4,r5,r6,r7,lr}                    @ 08024114 f0b5
    .hword 0x4657    @ 08024116 5746
    .hword 0x464e    @ 08024118 4e46
    .hword 0x4645    @ 0802411a 4546
    push {r5,r6,r7}                          @ 0802411c e0b4
    sub sp,#0x4                              @ 0802411e 81b0
    movs r0,#0x0    @ 08024120 0020
    .hword 0x4680    @ 08024122 8046
    ldr r3, PTR_gPrng_08024208               @ 08024124 384b
    ldr r1, DAT_0802420c                     @ 08024126 3949
    adds r0,r3,r1    @ 08024128 5818
    movs r1,#0xff    @ 0802412a ff21
    lsls r1,r1,#0x6    @ 0802412c 8901
    ldrh r0,[r0,#0x0]                        @ 0802412e 0088
    ands r1,r0    @ 08024130 0140
    movs r0,#0xa0    @ 08024132 a020
    lsls r0,r0,#0x1    @ 08024134 4000
    cmp r1,r0                                @ 08024136 8142
    bne LAB_08024160                         @ 08024138 12d1
    ldr r2, DAT_08024210                     @ 0802413a 354a
    adds r0,r3,r2    @ 0802413c 9818
    ldrb r0,[r0,#0x0]                        @ 0802413e 0078
    lsrs r2,r0,#0x6    @ 08024140 8209
    movs r4,#0x81    @ 08024142 8124
    lsls r4,r4,#0x2    @ 08024144 a400
    adds r1,r3,r4    @ 08024146 1919
    movs r0,#0x3f    @ 08024148 3f20
    ldrb r1,[r1,#0x0]                        @ 0802414a 0978
    ands r0,r1    @ 0802414c 0840
    lsls r0,r0,#0x2    @ 0802414e 8000
    orrs r0,r2    @ 08024150 1043
    movs r1,#0x4    @ 08024152 0421
    ands r0,r1    @ 08024154 0840
    lsls r0,r0,#0x10    @ 08024156 0004
    lsrs r0,r0,#0x10    @ 08024158 000c
    rsbs r0,r0,#0    @ 0802415a 4042
    lsrs r0,r0,#0x1f    @ 0802415c c00f
    .hword 0x4680    @ 0802415e 8046
LAB_08024160:
    movs r6,#0x80    @ 08024160 8026
    lsls r6,r6,#0xf    @ 08024162 f603
    movs r4,#0x38    @ 08024164 3824
    movs r5,#0x3    @ 08024166 0325
LAB_08024168:
    lsrs r2,r6,#0x10    @ 08024168 320c
    adds r0,r4,#0x0    @ 0802416a 201c
    movs r1,#0x81    @ 0802416c 8121
    lsls r1,r1,#0x7    @ 0802416e c901
    bl write_oam_entry_from_packed_args      @ 08024170 d1f0fcff
    movs r7,#0x80    @ 08024174 8027
    lsls r7,r7,#0xb    @ 08024176 ff02
    adds r6,r6,r7    @ 08024178 f619
    adds r4,#0x20    @ 0802417a 2034
    subs r5,#0x1    @ 0802417c 013d
    cmp r5,#0x0                              @ 0802417e 002d
    bge LAB_08024168                         @ 08024180 f2da
    movs r6,#0x80    @ 08024182 8026
    lsls r6,r6,#0x10    @ 08024184 3604
    movs r4,#0x8    @ 08024186 0824
    movs r5,#0x6    @ 08024188 0625
LAB_0802418a:
    movs r0,#0x80    @ 0802418a 8020
    lsls r0,r0,#0xd    @ 0802418c 4003
    orrs r0,r4    @ 0802418e 2043
    lsrs r2,r6,#0x10    @ 08024190 320c
    movs r1,#0x81    @ 08024192 8121
    lsls r1,r1,#0x7    @ 08024194 c901
    bl write_oam_entry_from_packed_args      @ 08024196 d1f0e9ff
    movs r0,#0x80    @ 0802419a 8020
    lsls r0,r0,#0xb    @ 0802419c c002
    adds r6,r6,r0    @ 0802419e 3618
    adds r4,#0x20    @ 080241a0 2034
    subs r5,#0x1    @ 080241a2 013d
    cmp r5,#0x0                              @ 080241a4 002d
    bge LAB_0802418a                         @ 080241a6 f0da
    movs r5,#0x7    @ 080241a8 0725
    ldr r2, DAT_08024214                     @ 080241aa 1a4a
    ldrb r1,[r2,#0x8]                        @ 080241ac 117a
    movs r0,#0x6    @ 080241ae 0620
    ands r0,r1    @ 080241b0 0840
    cmp r0,#0x6                              @ 080241b2 0628
    bne LAB_08024218                         @ 080241b4 30d1
    movs r6,#0xc0    @ 080241b6 c026
    lsls r6,r6,#0x10    @ 080241b8 3604
    movs r4,#0x8    @ 080241ba 0824
    movs r5,#0x6    @ 080241bc 0625
LAB_080241be:
    ldr r7, DAT_08024214                     @ 080241be 154f
    ldrb r1,[r7,#0x8]                        @ 080241c0 397a
    lsls r0,r1,#0x19    @ 080241c2 4806
    lsrs r0,r0,#0x1c    @ 080241c4 000f
    adds r0,#0x8f    @ 080241c6 8f30
    lsls r0,r0,#0x10    @ 080241c8 0004
    orrs r0,r4    @ 080241ca 2043
    lsrs r2,r6,#0x10    @ 080241cc 320c
    movs r1,#0x81    @ 080241ce 8121
    lsls r1,r1,#0x7    @ 080241d0 c901
    bl write_oam_entry_from_packed_args      @ 080241d2 d1f0cbff
    movs r2,#0x80    @ 080241d6 8022
    lsls r2,r2,#0xb    @ 080241d8 d202
    adds r6,r6,r2    @ 080241da b618
    adds r4,#0x20    @ 080241dc 2034
    subs r5,#0x1    @ 080241de 013d
    cmp r5,#0x0                              @ 080241e0 002d
    bge LAB_080241be                         @ 080241e2 ecda
    ldrb r2,[r7,#0x8]                        @ 080241e4 3a7a
    movs r0,#0x78    @ 080241e6 7820
    ands r0,r2    @ 080241e8 1040
    cmp r0,#0x0                              @ 080241ea 0028
    bne LAB_080241f0                         @ 080241ec 00d1
    b LAB_080242f2                           @ 080241ee 80e0
LAB_080241f0:
    lsls r0,r2,#0x19    @ 080241f0 5006
    lsrs r0,r0,#0x1c    @ 080241f2 000f
    subs r0,#0x1    @ 080241f4 0138
    movs r1,#0xf    @ 080241f6 0f21
    ands r0,r1    @ 080241f8 0840
    lsls r0,r0,#0x3    @ 080241fa c000
    movs r1,#0x79    @ 080241fc 7921
    rsbs r1,r1,#0    @ 080241fe 4942
    ands r1,r2    @ 08024200 1140
    orrs r1,r0    @ 08024202 0143
    strb r1,[r7,#0x8]                        @ 08024204 3972
    b LAB_080242f2                           @ 08024206 74e0
PTR_gPrng_08024208:
    .word  gPrng                          @ 08024208 40000003
DAT_0802420c:
    .word  0x00000202                     @ 0802420c 02020000
DAT_08024210:
    .word  0x00000203                     @ 08024210 03020000
DAT_08024214:
    .word  0x02023360                     @ 08024214 60330202
LAB_08024218:
    movs r0,#0x4    @ 08024218 0420
    ands r0,r1    @ 0802421a 0840
    cmp r0,#0x0                              @ 0802421c 0028
    bne LAB_08024224                         @ 0802421e 01d1
    movs r0,#0x4    @ 08024220 0420
    b LAB_080242ee                           @ 08024222 64e0
LAB_08024224:
    ldr r1, DAT_0802424c                     @ 08024224 0949
    ldr r3, DAT_08024250                     @ 08024226 0a4b
    adds r0,r1,r3    @ 08024228 c818
    ldrb r0,[r0,#0x0]                        @ 0802422a 0078
    ands r0,r5    @ 0802422c 2840
    adds r5,r1,#0x0    @ 0802422e 0d1c
    cmp r0,#0x1                              @ 08024230 0128
    beq LAB_08024274                         @ 08024232 1fd0
    cmp r0,#0x2                              @ 08024234 0228
    beq LAB_0802426c                         @ 08024236 19d0
    cmp r0,#0x3                              @ 08024238 0328
    beq LAB_08024264                         @ 0802423a 13d0
    cmp r0,#0x4                              @ 0802423c 0428
    beq LAB_0802425c                         @ 0802423e 0dd0
    ldr r3, DAT_08024254                     @ 08024240 044b
    cmp r0,#0x5                              @ 08024242 0528
    bne LAB_08024276                         @ 08024244 17d1
    ldr r4, DAT_08024258                     @ 08024246 044c
    adds r3,r3,r4    @ 08024248 1b19
    b LAB_08024276                           @ 0802424a 14e0
DAT_0802424c:
    .word  0x02000000                     @ 0802424c 00000002
DAT_08024250:
    .word  0x00006c2c                     @ 08024250 2c6c0000
DAT_08024254:
    .word  0x09dbe384                     @ 08024254 84e3db09
DAT_08024258:
    .word  0x0003aad0                     @ 08024258 d0aa0300
LAB_0802425c:
    ldr r3, DAT_08024260                     @ 0802425c 004b
    b LAB_08024276                           @ 0802425e 0ae0
DAT_08024260:
    .word  0x09ded174                     @ 08024260 74d1de09
LAB_08024264:
    ldr r3, DAT_08024268                     @ 08024264 004b
    b LAB_08024276                           @ 08024266 06e0
DAT_08024268:
    .word  0x09de0d2e                     @ 08024268 2e0dde09
LAB_0802426c:
    ldr r3, DAT_08024270                     @ 0802426c 004b
    b LAB_08024276                           @ 0802426e 02e0
DAT_08024270:
    .word  0x09dd4a9a                     @ 08024270 9a4add09
LAB_08024274:
    ldr r3, DAT_080242b0                     @ 08024274 0e4b
LAB_08024276:
    ldr r7, DAT_080242b4                     @ 08024276 0f4f
    adds r0,r5,r7    @ 08024278 e819
    ldrb r0,[r0,#0x0]                        @ 0802427a 0078
    lsls r0,r0,#0x1d    @ 0802427c 4007
    lsrs r6,r0,#0x1d    @ 0802427e 460f
    ldr r0, DAT_080242b8                     @ 08024280 0d48
    adds r2,r5,r0    @ 08024282 2a18
    ldr r0, DAT_080242bc                     @ 08024284 0d48
    ldrb r0,[r0,#0x2]                        @ 08024286 8078
    lsls r4,r0,#0x1b    @ 08024288 c406
    lsrs r0,r4,#0x1b    @ 0802428a e00e
    movs r1,#0x1    @ 0802428c 0121
    lsls r1,r0    @ 0802428e 8140
    ldr r0,[r2,#0x0]                         @ 08024290 1068
    ands r0,r1    @ 08024292 0840
    cmp r0,#0x0                              @ 08024294 0028
    beq LAB_080242d6                         @ 08024296 1ed0
    lsrs r0,r4,#0x1b    @ 08024298 e00e
    cmp r0,#0x19                             @ 0802429a 1928
    bne LAB_080242c8                         @ 0802429c 14d1
    ldr r1, DAT_080242c0                     @ 0802429e 0849
    adds r3,r5,r1    @ 080242a0 6b18
    ldr r2, DAT_080242c4                     @ 080242a2 084a
    adds r0,r5,r2    @ 080242a4 a818
    ldrb r0,[r0,#0x0]                        @ 080242a6 0078
    lsls r0,r0,#0x1d    @ 080242a8 4007
    lsrs r6,r0,#0x1d    @ 080242aa 460f
    b LAB_080242d6                           @ 080242ac 13e0
    .zero  0x2
DAT_080242b0:
    .word  0x09dc943c                     @ 080242b0 3c94dc09
DAT_080242b4:
    .word  0x00006c2c                     @ 080242b4 2c6c0000
DAT_080242b8:
    .word  0x00006e5c                     @ 080242b8 5c6e0000
DAT_080242bc:
    .word  0x02023360                     @ 080242bc 60330202
DAT_080242c0:
    .word  0x00006e48                     @ 080242c0 486e0000
DAT_080242c4:
    .word  0x00006e57                     @ 080242c4 576e0000
LAB_080242c8:
    ldr r0, PTR_deck_record_table_08024438   @ 080242c8 5b48
    lsrs r1,r4,#0x16    @ 080242ca a10d
    adds r1,r1,r0    @ 080242cc 0918
    ldrh r0,[r1,#0x2]                        @ 080242ce 4888
    bl card_name_lookup_by_internal_id       @ 080242d0 caf094fc
    adds r3,r0,#0x0    @ 080242d4 031c
LAB_080242d6:
    movs r1,#0x87    @ 080242d6 8721
    lsls r1,r1,#0x2    @ 080242d8 8900
    str r6,[sp,#0x0]                         @ 080242da 0096
    movs r0,#0xc0    @ 080242dc c020
    movs r2,#0x1    @ 080242de 0122
    bl draw_decimal_with_offset              @ 080242e0 fff7ccfa
    ldr r2, DAT_0802443c                     @ 080242e4 554a
    movs r0,#0x2    @ 080242e6 0220
    ldrb r3,[r2,#0x8]                        @ 080242e8 137a
    orrs r0,r3    @ 080242ea 1843
    movs r1,#0x78    @ 080242ec 7821
LAB_080242ee:
    orrs r0,r1    @ 080242ee 0843
    strb r0,[r2,#0x8]                        @ 080242f0 1072
LAB_080242f2:
    ldr r5, DAT_0802443c                     @ 080242f2 524d
    ldrb r4,[r5,#0x4]                        @ 080242f4 2c79
    lsrs r1,r4,#0x5    @ 080242f6 6109
    ldrb r7,[r5,#0x3]                        @ 080242f8 ef78
    lsls r0,r7,#0x1b    @ 080242fa f806
    lsrs r0,r0,#0x1d    @ 080242fc 400f
    subs r0,#0x2    @ 080242fe 0238
    cmp r1,r0                                @ 08024300 8142
    bge LAB_08024330                         @ 08024302 15da
    ldr r0, DAT_08024440                     @ 08024304 4e48
    movs r1,#0x80    @ 08024306 8021
    lsls r1,r1,#0x7    @ 08024308 c901
    ldr r4, DAT_08024444                     @ 0802430a 4e4c
    ldr r2, PTR_gPrng_08024448               @ 0802430c 4e4a
    movs r3,#0x83    @ 0802430e 8323
    lsls r3,r3,#0x2    @ 08024310 9b00
    adds r2,r2,r3    @ 08024312 d218
    ldrh r2,[r2,#0x0]                        @ 08024314 1288
    lsrs r2,r2,#0x2    @ 08024316 9208
    movs r3,#0x7    @ 08024318 0723
    ands r2,r3    @ 0802431a 1a40
    lsls r2,r2,#0x1    @ 0802431c 5200
    adds r2,r2,r4    @ 0802431e 1219
    ldrh r2,[r2,#0x0]                        @ 08024320 1288
    movs r4,#0x87    @ 08024322 8724
    lsls r4,r4,#0x3    @ 08024324 e400
    adds r2,r2,r4    @ 08024326 1219
    lsls r2,r2,#0x10    @ 08024328 1204
    lsrs r2,r2,#0x10    @ 0802432a 120c
    bl write_oam_entry_from_packed_args      @ 0802432c d1f01eff
LAB_08024330:
    movs r0,#0xe0    @ 08024330 e020
    ldrb r7,[r5,#0x4]                        @ 08024332 2f79
    ands r0,r7    @ 08024334 3840
    cmp r0,#0x0                              @ 08024336 0028
    beq LAB_08024372                         @ 08024338 1bd0
    ldr r0,[r5,#0x8]                         @ 0802433a a868
    movs r1,#0xff    @ 0802433c ff21
    lsls r1,r1,#0xf    @ 0802433e c903
    ands r0,r1    @ 08024340 0840
    cmp r0,#0x0                              @ 08024342 0028
    bne LAB_0802437e                         @ 08024344 1bd1
    ldr r0, DAT_0802444c                     @ 08024346 4148
    movs r1,#0x80    @ 08024348 8021
    lsls r1,r1,#0x7    @ 0802434a c901
    ldr r4, DAT_08024444                     @ 0802434c 3d4c
    ldr r2, PTR_gPrng_08024448               @ 0802434e 3e4a
    movs r3,#0x83    @ 08024350 8323
    lsls r3,r3,#0x2    @ 08024352 9b00
    adds r2,r2,r3    @ 08024354 d218
    ldrh r2,[r2,#0x0]                        @ 08024356 1288
    lsrs r2,r2,#0x2    @ 08024358 9208
    movs r3,#0x7    @ 0802435a 0723
    ands r2,r3    @ 0802435c 1a40
    lsls r2,r2,#0x1    @ 0802435e 5200
    adds r2,r2,r4    @ 08024360 1219
    ldrh r2,[r2,#0x0]                        @ 08024362 1288
    movs r4,#0x83    @ 08024364 8324
    lsls r4,r4,#0x3    @ 08024366 e400
    adds r2,r2,r4    @ 08024368 1219
    lsls r2,r2,#0x10    @ 0802436a 1204
    lsrs r2,r2,#0x10    @ 0802436c 120c
    bl write_oam_entry_from_packed_args      @ 0802436e d1f0fdfe
LAB_08024372:
    ldr r0,[r5,#0x8]                         @ 08024372 a868
    movs r1,#0xff    @ 08024374 ff21
    lsls r1,r1,#0xf    @ 08024376 c903
    ands r0,r1    @ 08024378 0840
    cmp r0,#0x0                              @ 0802437a 0028
    beq LAB_080243d8                         @ 0802437c 2cd0
LAB_0802437e:
    ldr r1, DAT_0802443c                     @ 0802437e 2f49
    ldrh r5,[r1,#0xc]                        @ 08024380 8d89
    lsls r4,r5,#0x11    @ 08024382 6c04
    lsrs r4,r4,#0x18    @ 08024384 240e
    ldrb r7,[r1,#0xb]                        @ 08024386 cf7a
    lsrs r2,r7,#0x7    @ 08024388 fa09
    movs r0,#0x7f    @ 0802438a 7f20
    ldrb r1,[r1,#0xc]                        @ 0802438c 097b
    ands r0,r1    @ 0802438e 0840
    lsls r0,r0,#0x1    @ 08024390 4000
    orrs r0,r2    @ 08024392 1043
    subs r4,r4,r0    @ 08024394 241a
    lsls r4,r4,#0x4    @ 08024396 2401
    adds r5,r4,#0x0    @ 08024398 251c
    adds r5,#0x20    @ 0802439a 2035
    lsls r5,r5,#0x10    @ 0802439c 2d04
    movs r0,#0x20    @ 0802439e 2020
    orrs r0,r5    @ 080243a0 2843
    ldr r2, DAT_08024450                     @ 080243a2 2b4a
    movs r1,#0x40    @ 080243a4 4021
    bl write_oam_entry_from_packed_args      @ 080243a6 d1f0e1fe
    adds r6,r5,#0x0    @ 080243aa 2e1c
    adds r7,r4,#0x0    @ 080243ac 271c
    movs r4,#0x30    @ 080243ae 3024
    movs r5,#0x8    @ 080243b0 0825
LAB_080243b2:
    adds r0,r4,#0x0    @ 080243b2 201c
    orrs r0,r6    @ 080243b4 3043
    movs r1,#0x40    @ 080243b6 4021
    ldr r2, DAT_08024454                     @ 080243b8 264a
    bl write_oam_entry_from_packed_args      @ 080243ba d1f0d7fe
    adds r4,#0x10    @ 080243be 1034
    subs r5,#0x1    @ 080243c0 013d
    cmp r5,#0x0                              @ 080243c2 002d
    bge LAB_080243b2                         @ 080243c4 f5da
    adds r0,r7,#0x0    @ 080243c6 381c
    adds r0,#0x20    @ 080243c8 2030
    lsls r0,r0,#0x10    @ 080243ca 0004
    movs r1,#0xc0    @ 080243cc c021
    orrs r0,r1    @ 080243ce 0843
    ldr r2, DAT_08024458                     @ 080243d0 214a
    movs r1,#0x40    @ 080243d2 4021
    bl write_oam_entry_from_packed_args      @ 080243d4 d1f0cafe
LAB_080243d8:
    ldr r6, DAT_0802443c                     @ 080243d8 184e
    ldr r0,[r6,#0x4]                         @ 080243da 7068
    ldr r1, DAT_0802445c                     @ 080243dc 1f49
    ands r0,r1    @ 080243de 0840
    cmp r0,#0x0                              @ 080243e0 0028
    beq LAB_080243e6                         @ 080243e2 00d0
    b LAB_080245aa                           @ 080243e4 e1e0
LAB_080243e6:
    ldr r0, DAT_08024460                     @ 080243e6 1e48
    ldr r1, DAT_08024464                     @ 080243e8 1e49
    adds r0,r0,r1    @ 080243ea 4018
    ldrb r2,[r6,#0x2]                        @ 080243ec b278
    lsls r5,r2,#0x1b    @ 080243ee d506
    lsrs r2,r5,#0x1b    @ 080243f0 ea0e
    movs r1,#0x1    @ 080243f2 0121
    lsls r1,r2    @ 080243f4 9140
    ldr r0,[r0,#0x0]                         @ 080243f6 0068
    ands r0,r1    @ 080243f8 0840
    cmp r0,#0x0                              @ 080243fa 0028
    beq LAB_080244da                         @ 080243fc 6dd0
    ldrb r3,[r6,#0x3]                        @ 080243fe f378
    lsls r0,r3,#0x1b    @ 08024400 d806
    lsrs r0,r0,#0x1d    @ 08024402 400f
    cmp r0,#0x1                              @ 08024404 0128
    beq LAB_08024468                         @ 08024406 2fd0
    cmp r0,#0x2                              @ 08024408 0228
    beq LAB_0802447c                         @ 0802440a 37d0
    adds r0,r2,#0x0    @ 0802440c 101c
    movs r1,#0x5    @ 0802440e 0521
    bl __umodsi3                             @ 08024410 eaf020fa
    lsls r0,r0,#0x10    @ 08024414 0004
    lsrs r4,r0,#0x10    @ 08024416 040c
    lsrs r0,r5,#0x1b    @ 08024418 e80e
    movs r1,#0x5    @ 0802441a 0521
    bl __udivsi3                             @ 0802441c eaf0def9
    lsls r0,r0,#0x10    @ 08024420 0004
    lsrs r2,r0,#0x10    @ 08024422 020c
    ldrb r6,[r6,#0x4]                        @ 08024424 3679
    lsrs r0,r6,#0x5    @ 08024426 7009
    subs r2,r2,r0    @ 08024428 121a
    lsrs r0,r5,#0x1b    @ 0802442a e80e
    cmp r0,#0x19                             @ 0802442c 1928
    beq LAB_080244b0                         @ 0802442e 3fd0
    cmp r0,#0x1a                             @ 08024430 1a28
    beq LAB_080244b4                         @ 08024432 3fd0
    b LAB_080244b6                           @ 08024434 3fe0
    .zero  0x2
PTR_deck_record_table_08024438:
    .word  deck_record_table              @ 08024438 0c8de509
DAT_0802443c:
    .word  0x02023360                     @ 0802443c 60330202
DAT_08024440:
    .word  0x00830070                     @ 08024440 70008300
DAT_08024444:
    .word  0x09e59ce8                     @ 08024444 e89ce509
PTR_gPrng_08024448:
    .word  gPrng                          @ 08024448 40000003
DAT_0802444c:
    .word  0x00210070                     @ 0802444c 70002100
DAT_08024450:
    .word  0x00000814                     @ 08024450 14080000
DAT_08024454:
    .word  0x00000815                     @ 08024454 15080000
DAT_08024458:
    .word  0x00000816                     @ 08024458 16080000
DAT_0802445c:
    .word  0xffff0f00                     @ 0802445c 000fffff
DAT_08024460:
    .word  0x02000000                     @ 08024460 00000002
DAT_08024464:
    .word  0x00006e5c                     @ 08024464 5c6e0000
LAB_08024468:
    lsrs r1,r5,#0x1b    @ 08024468 e90e
    lsls r0,r1,#0x2    @ 0802446a 8800
    adds r0,r0,r1    @ 0802446c 4018
    lsls r0,r0,#0x3    @ 0802446e c000
    adds r0,#0x18    @ 08024470 1830
    adds r2,r1,#0x0    @ 08024472 0a1c
    movs r1,#0x4c    @ 08024474 4c21
    bl render_win_count_digits_to_oam        @ 08024476 fff7adfd
    b LAB_080244da                           @ 0802447a 2ee0
LAB_0802447c:
    lsrs r0,r5,#0x1b    @ 0802447c e80e
    movs r1,#0x5    @ 0802447e 0521
    bl __umodsi3                             @ 08024480 eaf0e8f9
    adds r4,r0,#0x0    @ 08024484 041c
    lsls r4,r4,#0x10    @ 08024486 2404
    lsrs r4,r4,#0x10    @ 08024488 240c
    lsrs r0,r5,#0x1b    @ 0802448a e80e
    movs r1,#0x5    @ 0802448c 0521
    bl __udivsi3                             @ 0802448e eaf0a5f9
    adds r2,r0,#0x0    @ 08024492 021c
    lsls r2,r2,#0x10    @ 08024494 1204
    lsrs r2,r2,#0x10    @ 08024496 120c
    lsls r0,r4,#0x2    @ 08024498 a000
    adds r0,r0,r4    @ 0802449a 0019
    lsls r0,r0,#0x3    @ 0802449c c000
    adds r0,#0x18    @ 0802449e 1830
    lsls r1,r2,#0x1    @ 080244a0 5100
    adds r1,r1,r2    @ 080244a2 8918
    lsls r1,r1,#0x4    @ 080244a4 0901
    adds r1,#0x34    @ 080244a6 3431
    lsrs r2,r5,#0x1b    @ 080244a8 ea0e
    bl render_win_count_digits_to_oam        @ 080244aa fff793fd
    b LAB_080244da                           @ 080244ae 14e0
LAB_080244b0:
    adds r4,#0x1    @ 080244b0 0134
    b LAB_080244b6                           @ 080244b2 00e0
LAB_080244b4:
    adds r4,#0x2    @ 080244b4 0234
LAB_080244b6:
    lsls r0,r4,#0x2    @ 080244b6 a000
    adds r0,r0,r4    @ 080244b8 0019
    lsls r0,r0,#0x3    @ 080244ba c000
    adds r0,#0x18    @ 080244bc 1830
    lsls r1,r2,#0x1    @ 080244be 5100
    adds r1,r1,r2    @ 080244c0 8918
    lsls r1,r1,#0x4    @ 080244c2 0901
    ldr r3, DAT_08024520                     @ 080244c4 164b
    ldrh r4,[r3,#0x8]                        @ 080244c6 1c89
    lsls r2,r4,#0x11    @ 080244c8 6204
    lsrs r2,r2,#0x18    @ 080244ca 120e
    subs r2,#0x34    @ 080244cc 343a
    subs r1,r1,r2    @ 080244ce 891a
    ldrb r3,[r3,#0x2]                        @ 080244d0 9b78
    lsls r2,r3,#0x1b    @ 080244d2 da06
    lsrs r2,r2,#0x1b    @ 080244d4 d20e
    bl render_win_count_digits_to_oam        @ 080244d6 fff77dfd
LAB_080244da:
    .hword 0x4645    @ 080244da 4546
    cmp r5,#0x0                              @ 080244dc 002d
    bne LAB_080245aa                         @ 080244de 64d1
    ldr r6, DAT_08024520                     @ 080244e0 0f4e
    ldrb r7,[r6,#0x3]                        @ 080244e2 f778
    lsls r0,r7,#0x1b    @ 080244e4 f806
    lsrs r0,r0,#0x1d    @ 080244e6 400f
    cmp r0,#0x1                              @ 080244e8 0128
    beq LAB_08024524                         @ 080244ea 1bd0
    cmp r0,#0x2                              @ 080244ec 0228
    beq LAB_08024538                         @ 080244ee 23d0
    ldrb r0,[r6,#0x2]                        @ 080244f0 b078
    lsls r4,r0,#0x1b    @ 080244f2 c406
    lsrs r0,r4,#0x1b    @ 080244f4 e00e
    movs r1,#0x5    @ 080244f6 0521
    bl __umodsi3                             @ 080244f8 eaf0acf9
    lsls r0,r0,#0x10    @ 080244fc 0004
    lsrs r5,r0,#0x10    @ 080244fe 050c
    lsrs r0,r4,#0x1b    @ 08024500 e00e
    movs r1,#0x5    @ 08024502 0521
    bl __udivsi3                             @ 08024504 eaf06af9
    lsls r0,r0,#0x10    @ 08024508 0004
    lsrs r1,r0,#0x10    @ 0802450a 010c
    ldrb r6,[r6,#0x4]                        @ 0802450c 3679
    lsrs r0,r6,#0x5    @ 0802450e 7009
    subs r1,r1,r0    @ 08024510 091a
    lsrs r4,r4,#0x1b    @ 08024512 e40e
    cmp r4,#0x19                             @ 08024514 192c
    beq LAB_0802457c                         @ 08024516 31d0
    cmp r4,#0x1a                             @ 08024518 1a2c
    beq LAB_08024580                         @ 0802451a 31d0
    b LAB_08024582                           @ 0802451c 31e0
    .zero  0x2
DAT_08024520:
    .word  0x02023360                     @ 08024520 60330202
LAB_08024524:
    ldrb r6,[r6,#0x2]                        @ 08024524 b678
    lsls r1,r6,#0x1b    @ 08024526 f106
    lsrs r1,r1,#0x1b    @ 08024528 c90e
    lsls r0,r1,#0x2    @ 0802452a 8800
    adds r0,r0,r1    @ 0802452c 4018
    lsls r0,r0,#0x3    @ 0802452e c000
    adds r0,#0x18    @ 08024530 1830
    movs r1,#0x98    @ 08024532 9821
    lsls r1,r1,#0xf    @ 08024534 c903
    b LAB_0802456e                           @ 08024536 1ae0
LAB_08024538:
    ldrb r6,[r6,#0x2]                        @ 08024538 b678
    lsls r5,r6,#0x1b    @ 0802453a f506
    lsrs r0,r5,#0x1b    @ 0802453c e80e
    movs r1,#0x5    @ 0802453e 0521
    bl __umodsi3                             @ 08024540 eaf088f9
    adds r4,r0,#0x0    @ 08024544 041c
    lsls r4,r4,#0x10    @ 08024546 2404
    lsrs r4,r4,#0x10    @ 08024548 240c
    lsrs r5,r5,#0x1b    @ 0802454a ed0e
    adds r0,r5,#0x0    @ 0802454c 281c
    movs r1,#0x5    @ 0802454e 0521
    bl __udivsi3                             @ 08024550 eaf044f9
    adds r2,r0,#0x0    @ 08024554 021c
    lsls r2,r2,#0x10    @ 08024556 1204
    lsrs r2,r2,#0x10    @ 08024558 120c
    lsls r0,r4,#0x2    @ 0802455a a000
    adds r0,r0,r4    @ 0802455c 0019
    lsls r0,r0,#0x3    @ 0802455e c000
    adds r0,#0x18    @ 08024560 1830
    lsls r1,r2,#0x1    @ 08024562 5100
    adds r1,r1,r2    @ 08024564 8918
    lsls r1,r1,#0x14    @ 08024566 0905
    movs r2,#0xd0    @ 08024568 d022
    lsls r2,r2,#0xe    @ 0802456a 9203
    adds r1,r1,r2    @ 0802456c 8918
LAB_0802456e:
    orrs r0,r1    @ 0802456e 0843
    movs r2,#0x82    @ 08024570 8222
    lsls r2,r2,#0x3    @ 08024572 d200
    movs r1,#0x80    @ 08024574 8021
    bl write_oam_entry_from_packed_args      @ 08024576 d1f0f9fd
    b LAB_080245aa                           @ 0802457a 16e0
LAB_0802457c:
    adds r5,#0x1    @ 0802457c 0135
    b LAB_08024582                           @ 0802457e 00e0
LAB_08024580:
    adds r5,#0x2    @ 08024580 0235
LAB_08024582:
    lsls r0,r5,#0x2    @ 08024582 a800
    adds r0,r0,r5    @ 08024584 4019
    lsls r0,r0,#0x3    @ 08024586 c000
    adds r0,#0x18    @ 08024588 1830
    lsls r2,r1,#0x1    @ 0802458a 4a00
    adds r2,r2,r1    @ 0802458c 5218
    lsls r2,r2,#0x4    @ 0802458e 1201
    ldr r1, DAT_080245e8                     @ 08024590 1549
    ldrh r1,[r1,#0x8]                        @ 08024592 0989
    lsls r1,r1,#0x11    @ 08024594 4904
    lsrs r1,r1,#0x18    @ 08024596 090e
    subs r1,#0x34    @ 08024598 3439
    subs r2,r2,r1    @ 0802459a 521a
    lsls r2,r2,#0x10    @ 0802459c 1204
    orrs r0,r2    @ 0802459e 1043
    movs r2,#0x82    @ 080245a0 8222
    lsls r2,r2,#0x3    @ 080245a2 d200
    movs r1,#0x80    @ 080245a4 8021
    bl write_oam_entry_from_packed_args      @ 080245a6 d1f0e1fd
LAB_080245aa:
    ldr r1, DAT_080245e8                     @ 080245aa 0f49
    ldrb r3,[r1,#0x3]                        @ 080245ac cb78
    lsls r0,r3,#0x1b    @ 080245ae d806
    lsrs r0,r0,#0x1d    @ 080245b0 400f
    adds r7,r1,#0x0    @ 080245b2 0f1c
    cmp r0,#0x1                              @ 080245b4 0128
    beq LAB_080245ec                         @ 080245b6 19d0
    cmp r0,#0x2                              @ 080245b8 0228
    beq LAB_08024668                         @ 080245ba 55d0
    ldrb r4,[r7,#0x4]                        @ 080245bc 3c79
    lsls r0,r4,#0x18    @ 080245be 2006
    lsrs r2,r0,#0x1d    @ 080245c0 420f
    lsls r1,r2,#0x2    @ 080245c2 9100
    adds r2,r1,r2    @ 080245c4 8a18
    lsrs r0,r0,#0x1d    @ 080245c6 400f
    lsls r1,r0,#0x2    @ 080245c8 8100
    adds r1,r1,r0    @ 080245ca 0918
    movs r5,#0xa    @ 080245cc 0a25
    adds r5,r5,r1    @ 080245ce 6d18
    .hword 0x46a8    @ 080245d0 a846
    movs r0,#0x6    @ 080245d2 0620
    ldrsh r3,[r7,r0]                         @ 080245d4 3b5e
    movs r0,#0x1    @ 080245d6 0120
    rsbs r0,r0,#0    @ 080245d8 4042
    cmp r3,r0                                @ 080245da 8342
    bne LAB_080245e0                         @ 080245dc 00d1
    b LAB_08024718                           @ 080245de 9be0
LAB_080245e0:
    cmp r3,#0x1                              @ 080245e0 012b
    bne LAB_080245e6                         @ 080245e2 00d1
    b LAB_0802471c                           @ 080245e4 9ae0
LAB_080245e6:
    b LAB_08024720                           @ 080245e6 9be0
DAT_080245e8:
    .word  0x02023360                     @ 080245e8 60330202
LAB_080245ec:
    movs r5,#0x0    @ 080245ec 0025
    ldrh r7,[r7,#0x0]                        @ 080245ee 3f88
    cmp r5,r7                                @ 080245f0 bd42
    blt LAB_080245f6                         @ 080245f2 00db
    b LAB_08024848                           @ 080245f4 28e1
LAB_080245f6:
    ldr r1, DAT_0802465c                     @ 080245f6 1949
    .hword 0x4688    @ 080245f8 8846
    ldr r7, PTR_gUnlockedDuelists_08024660   @ 080245fa 194f
    movs r6,#0xa0    @ 080245fc a026
    lsls r6,r6,#0x1    @ 080245fe 7600
LAB_08024600:
    movs r2,#0xff    @ 08024600 ff22
    lsls r2,r2,#0x6    @ 08024602 9201
    adds r0,r2,#0x0    @ 08024604 101c
    .hword 0x4643    @ 08024606 4346
    ldrh r3,[r3,#0x0]                        @ 08024608 1b88
    ands r0,r3    @ 0802460a 1840
    cmp r0,r6                                @ 0802460c b042
    bne LAB_0802461e                         @ 0802460e 06d1
    ldr r0, DAT_08024664                     @ 08024610 1448
    ldrb r0,[r0,#0x2]                        @ 08024612 8078
    lsls r0,r0,#0x1b    @ 08024614 c006
    lsrs r0,r0,#0x1b    @ 08024616 c00e
    adds r4,r5,#0x1    @ 08024618 6c1c
    cmp r5,r0                                @ 0802461a 8542
    bne LAB_0802464e                         @ 0802461c 17d1
LAB_0802461e:
    movs r0,#0x1    @ 0802461e 0120
    lsls r0,r5    @ 08024620 a840
    ldr r1,[r7,#0x0]                         @ 08024622 3968
    ands r1,r0    @ 08024624 0140
    adds r4,r5,#0x1    @ 08024626 6c1c
    cmp r1,#0x0                              @ 08024628 0029
    beq LAB_0802464e                         @ 0802462a 10d0
    lsls r2,r5,#0x2    @ 0802462c aa00
    adds r0,r2,r5    @ 0802462e 5019
    lsls r0,r0,#0x3    @ 08024630 c000
    adds r0,#0x1c    @ 08024632 1c30
    movs r1,#0xa0    @ 08024634 a021
    lsls r1,r1,#0xf    @ 08024636 c903
    orrs r0,r1    @ 08024638 0843
    lsls r1,r4,#0xc    @ 0802463a 2103
    adds r2,r2,r1    @ 0802463c 5218
    movs r5,#0xa0    @ 0802463e a025
    lsls r5,r5,#0x3    @ 08024640 ed00
    adds r2,r2,r5    @ 08024642 5219
    lsls r2,r2,#0x10    @ 08024644 1204
    lsrs r2,r2,#0x10    @ 08024646 120c
    movs r1,#0x80    @ 08024648 8021
    bl write_oam_entry_from_packed_args      @ 0802464a d1f08ffd
LAB_0802464e:
    adds r5,r4,#0x0    @ 0802464e 251c
    ldr r0, DAT_08024664                     @ 08024650 0448
    ldrh r0,[r0,#0x0]                        @ 08024652 0088
    cmp r5,r0                                @ 08024654 8542
    blt LAB_08024600                         @ 08024656 d3db
    b LAB_08024848                           @ 08024658 f6e0
    .zero  0x2
DAT_0802465c:
    .word  0x03000242                     @ 0802465c 42020003
PTR_gUnlockedDuelists_08024660:
    .word  gUnlockedDuelists              @ 08024660 5c6e0002
DAT_08024664:
    .word  0x02023360                     @ 08024664 60330202
LAB_08024668:
    movs r5,#0x0    @ 08024668 0025
    ldrh r7,[r7,#0x0]                        @ 0802466a 3f88
    cmp r5,r7                                @ 0802466c bd42
    blt LAB_08024672                         @ 0802466e 00db
    b LAB_08024848                           @ 08024670 eae0
LAB_08024672:
    movs r7,#0xa0    @ 08024672 a027
    lsls r7,r7,#0x1    @ 08024674 7f00
    .hword 0x46b9    @ 08024676 b946
    ldr r0, DAT_08024708                     @ 08024678 2348
    .hword 0x4680    @ 0802467a 8046
LAB_0802467c:
    movs r0,#0x7    @ 0802467c 0720
    ands r0,r5    @ 0802467e 2840
    asrs r1,r5,#0x3    @ 08024680 e910
    lsls r0,r0,#0x2    @ 08024682 8000
    lsls r1,r1,#0x7    @ 08024684 c901
    adds r0,r0,r1    @ 08024686 4018
    lsls r0,r0,#0x10    @ 08024688 0004
    lsrs r7,r0,#0x10    @ 0802468a 070c
    adds r0,r5,#0x0    @ 0802468c 281c
    movs r1,#0x5    @ 0802468e 0521
    bl __modsi3                              @ 08024690 eaf004f8
    adds r6,r0,#0x0    @ 08024694 061c
    adds r0,r5,#0x0    @ 08024696 281c
    movs r1,#0x5    @ 08024698 0521
    bl __divsi3                              @ 0802469a e9f0b3ff
    adds r2,r0,#0x0    @ 0802469e 021c
    movs r1,#0xff    @ 080246a0 ff21
    lsls r1,r1,#0x6    @ 080246a2 8901
    adds r0,r1,#0x0    @ 080246a4 081c
    .hword 0x4643    @ 080246a6 4346
    ldrh r3,[r3,#0x0]                        @ 080246a8 1b88
    ands r0,r3    @ 080246aa 1840
    cmp r0,r9                                @ 080246ac 4845
    bne LAB_080246be                         @ 080246ae 06d1
    ldr r0, DAT_0802470c                     @ 080246b0 1648
    ldrb r0,[r0,#0x2]                        @ 080246b2 8078
    lsls r0,r0,#0x1b    @ 080246b4 c006
    lsrs r0,r0,#0x1b    @ 080246b6 c00e
    adds r4,r5,#0x1    @ 080246b8 6c1c
    cmp r5,r0                                @ 080246ba 8542
    bne LAB_080246fc                         @ 080246bc 1ed1
LAB_080246be:
    ldr r0, DAT_08024710                     @ 080246be 1448
    ldr r4, DAT_08024714                     @ 080246c0 144c
    adds r0,r0,r4    @ 080246c2 0019
    movs r1,#0x1    @ 080246c4 0121
    lsls r1,r5    @ 080246c6 a940
    ldr r0,[r0,#0x0]                         @ 080246c8 0068
    ands r0,r1    @ 080246ca 0840
    adds r4,r5,#0x1    @ 080246cc 6c1c
    cmp r0,#0x0                              @ 080246ce 0028
    beq LAB_080246fc                         @ 080246d0 14d0
    lsls r0,r6,#0x2    @ 080246d2 b000
    adds r0,r0,r6    @ 080246d4 8019
    lsls r0,r0,#0x3    @ 080246d6 c000
    adds r0,#0x1c    @ 080246d8 1c30
    lsls r1,r2,#0x1    @ 080246da 5100
    adds r1,r1,r2    @ 080246dc 8918
    lsls r1,r1,#0x14    @ 080246de 0905
    movs r5,#0xe0    @ 080246e0 e025
    lsls r5,r5,#0xe    @ 080246e2 ad03
    adds r1,r1,r5    @ 080246e4 4919
    orrs r0,r1    @ 080246e6 0843
    lsls r2,r4,#0xc    @ 080246e8 2203
    adds r2,r7,r2    @ 080246ea ba18
    movs r7,#0xa0    @ 080246ec a027
    lsls r7,r7,#0x3    @ 080246ee ff00
    adds r2,r2,r7    @ 080246f0 d219
    lsls r2,r2,#0x10    @ 080246f2 1204
    lsrs r2,r2,#0x10    @ 080246f4 120c
    movs r1,#0x80    @ 080246f6 8021
    bl write_oam_entry_from_packed_args      @ 080246f8 d1f038fd
LAB_080246fc:
    adds r5,r4,#0x0    @ 080246fc 251c
    ldr r0, DAT_0802470c                     @ 080246fe 0348
    ldrh r0,[r0,#0x0]                        @ 08024700 0088
    cmp r5,r0                                @ 08024702 8542
    blt LAB_0802467c                         @ 08024704 badb
    b LAB_08024848                           @ 08024706 9fe0
DAT_08024708:
    .word  0x03000242                     @ 08024708 42020003
DAT_0802470c:
    .word  0x02023360                     @ 0802470c 60330202
DAT_08024710:
    .word  0x02000000                     @ 08024710 00000002
DAT_08024714:
    .word  0x00006e5c                     @ 08024714 5c6e0000
LAB_08024718:
    subs r2,#0x5    @ 08024718 053a
    b LAB_08024720                           @ 0802471a 01e0
LAB_0802471c:
    adds r1,#0xf    @ 0802471c 0f31
    .hword 0x4688    @ 0802471e 8846
LAB_08024720:
    cmp r2,#0x0                              @ 08024720 002a
    bge LAB_08024726                         @ 08024722 00da
    movs r2,#0x0    @ 08024724 0022
LAB_08024726:
    ldrh r1,[r7,#0x0]                        @ 08024726 3988
    subs r0,r1,#0x1    @ 08024728 481e
    cmp r8,r0                                @ 0802472a 8045
    ble LAB_08024730                         @ 0802472c 00dd
    .hword 0x4688    @ 0802472e 8846
LAB_08024730:
    adds r5,r2,#0x0    @ 08024730 151c
    cmp r5,r8                                @ 08024732 4545
    bge LAB_080247f4                         @ 08024734 5eda
    movs r0,#0xa0    @ 08024736 a020
    lsls r0,r0,#0x1    @ 08024738 4000
    .hword 0x4682    @ 0802473a 8246
LAB_0802473c:
    adds r0,r5,#0x0    @ 0802473c 281c
    movs r1,#0xf    @ 0802473e 0f21
    bl __modsi3                              @ 08024740 e9f0acff
    adds r6,r0,#0x0    @ 08024744 061c
    movs r0,#0x7    @ 08024746 0720
    ands r0,r6    @ 08024748 3040
    asrs r1,r6,#0x3    @ 0802474a f110
    lsls r0,r0,#0x2    @ 0802474c 8000
    lsls r1,r1,#0x7    @ 0802474e c901
    adds r0,r0,r1    @ 08024750 4018
    lsls r0,r0,#0x10    @ 08024752 0004
    lsrs r0,r0,#0x10    @ 08024754 000c
    .hword 0x4681    @ 08024756 8146
    adds r0,r5,#0x0    @ 08024758 281c
    movs r1,#0x5    @ 0802475a 0521
    bl __modsi3                              @ 0802475c e9f09eff
    adds r4,r0,#0x0    @ 08024760 041c
    adds r0,r5,#0x0    @ 08024762 281c
    movs r1,#0x5    @ 08024764 0521
    bl __divsi3                              @ 08024766 e9f04dff
    adds r3,r0,#0x0    @ 0802476a 031c
    cmp r5,#0x19                             @ 0802476c 192d
    beq LAB_08024776                         @ 0802476e 02d0
    cmp r5,#0x1a                             @ 08024770 1a2d
    beq LAB_0802477a                         @ 08024772 02d0
    b LAB_0802477c                           @ 08024774 02e0
LAB_08024776:
    adds r4,#0x1    @ 08024776 0134
    b LAB_0802477c                           @ 08024778 00e0
LAB_0802477a:
    adds r4,#0x2    @ 0802477a 0234
LAB_0802477c:
    ldr r0, PTR_gPrng_08024858               @ 0802477c 3648
    ldr r1, DAT_0802485c                     @ 0802477e 3749
    adds r0,r0,r1    @ 08024780 4018
    movs r2,#0xff    @ 08024782 ff22
    lsls r2,r2,#0x6    @ 08024784 9201
    adds r1,r2,#0x0    @ 08024786 111c
    ldrh r0,[r0,#0x0]                        @ 08024788 0088
    ands r0,r1    @ 0802478a 0840
    cmp r0,r10                               @ 0802478c 5045
    bne LAB_0802479a                         @ 0802478e 04d1
    ldrb r7,[r7,#0x2]                        @ 08024790 bf78
    lsls r0,r7,#0x1b    @ 08024792 f806
    lsrs r0,r0,#0x1b    @ 08024794 c00e
    cmp r5,r0                                @ 08024796 8542
    bne LAB_080247ec                         @ 08024798 28d1
LAB_0802479a:
    movs r1,#0x1    @ 0802479a 0121
    lsls r1,r5    @ 0802479c a940
    ldr r7, PTR_gUnlockedDuelists_08024860   @ 0802479e 304f
    ldr r0,[r7,#0x0]                         @ 080247a0 3868
    ands r0,r1    @ 080247a2 0840
    cmp r0,#0x0                              @ 080247a4 0028
    beq LAB_080247ec                         @ 080247a6 21d0
    lsls r0,r4,#0x2    @ 080247a8 a000
    adds r0,r0,r4    @ 080247aa 0019
    lsls r0,r0,#0x3    @ 080247ac c000
    adds r0,#0x1c    @ 080247ae 1c30
    lsls r2,r3,#0x1    @ 080247b0 5a00
    adds r2,r2,r3    @ 080247b2 d218
    lsls r2,r2,#0x4    @ 080247b4 1201
    ldr r3, DAT_08024864                     @ 080247b6 2b4b
    ldrb r1,[r3,#0x3]                        @ 080247b8 d978
    lsrs r4,r1,#0x5    @ 080247ba 4c09
    movs r1,#0x1f    @ 080247bc 1f21
    ldrb r7,[r3,#0x4]                        @ 080247be 1f79
    ands r1,r7    @ 080247c0 3940
    lsls r1,r1,#0x3    @ 080247c2 c900
    orrs r1,r4    @ 080247c4 2143
    adds r1,#0x10    @ 080247c6 1031
    adds r2,r2,r1    @ 080247c8 5218
    ldrh r3,[r3,#0x8]                        @ 080247ca 1b89
    lsls r1,r3,#0x11    @ 080247cc 5904
    lsrs r1,r1,#0x18    @ 080247ce 090e
    subs r2,r2,r1    @ 080247d0 521a
    lsls r2,r2,#0x10    @ 080247d2 1204
    orrs r0,r2    @ 080247d4 1043
    adds r2,r6,#0x1    @ 080247d6 721c
    lsls r2,r2,#0xc    @ 080247d8 1203
    add r2,r9                                @ 080247da 4a44
    movs r1,#0xa0    @ 080247dc a021
    lsls r1,r1,#0x3    @ 080247de c900
    adds r2,r2,r1    @ 080247e0 5218
    lsls r2,r2,#0x10    @ 080247e2 1204
    lsrs r2,r2,#0x10    @ 080247e4 120c
    movs r1,#0x80    @ 080247e6 8021
    bl write_oam_entry_from_packed_args      @ 080247e8 d1f0c0fc
LAB_080247ec:
    adds r5,#0x1    @ 080247ec 0135
    ldr r7, DAT_08024864                     @ 080247ee 1d4f
    cmp r5,r8                                @ 080247f0 4545
    blt LAB_0802473c                         @ 080247f2 a3db
LAB_080247f4:
    ldr r4, PTR_gPrng_08024858               @ 080247f4 184c
    ldrh r2,[r7,#0x8]                        @ 080247f6 3a89
    lsrs r1,r2,#0x7    @ 080247f8 d109
    lsls r1,r1,#0x18    @ 080247fa 0906
    lsrs r1,r1,#0x18    @ 080247fc 090e
    ldrb r5,[r7,#0x3]                        @ 080247fe fd78
    lsrs r3,r5,#0x5    @ 08024800 6b09
    movs r2,#0x1f    @ 08024802 1f22
    adds r0,r2,#0x0    @ 08024804 101c
    ldrb r5,[r7,#0x4]                        @ 08024806 3d79
    ands r0,r5    @ 08024808 2840
    lsls r0,r0,#0x3    @ 0802480a c000
    orrs r0,r3    @ 0802480c 1843
    subs r1,r1,r0    @ 0802480e 091a
    ldrb r0,[r7,#0xb]                        @ 08024810 f87a
    lsrs r3,r0,#0x7    @ 08024812 c309
    movs r0,#0x7f    @ 08024814 7f20
    ldrb r5,[r7,#0xc]                        @ 08024816 3d7b
    ands r0,r5    @ 08024818 2840
    lsls r0,r0,#0x1    @ 0802481a 4000
    orrs r0,r3    @ 0802481c 1843
    lsls r0,r0,#0x4    @ 0802481e 0001
    adds r1,r1,r0    @ 08024820 0918
    movs r3,#0xf5    @ 08024822 f523
    lsls r3,r3,#0x1    @ 08024824 5b00
    adds r0,r4,r3    @ 08024826 e018
    strh r1,[r0,#0x0]                        @ 08024828 0180
    ldrh r5,[r7,#0x8]                        @ 0802482a 3d89
    lsrs r0,r5,#0x7    @ 0802482c e809
    lsls r0,r0,#0x18    @ 0802482e 0006
    lsrs r0,r0,#0x18    @ 08024830 000e
    ldrb r3,[r7,#0x3]                        @ 08024832 fb78
    lsrs r1,r3,#0x5    @ 08024834 5909
    ldrb r7,[r7,#0x4]                        @ 08024836 3f79
    ands r2,r7    @ 08024838 3a40
    lsls r2,r2,#0x3    @ 0802483a d200
    orrs r2,r1    @ 0802483c 0a43
    subs r0,r0,r2    @ 0802483e 801a
    movs r5,#0xf6    @ 08024840 f625
    lsls r5,r5,#0x1    @ 08024842 6d00
    adds r1,r4,r5    @ 08024844 6119
    strh r0,[r1,#0x0]                        @ 08024846 0880
LAB_08024848:
    add sp,#0x4                              @ 08024848 01b0
    pop {r3,r4,r5}                           @ 0802484a 38bc
    .hword 0x4698    @ 0802484c 9846
    .hword 0x46a1    @ 0802484e a146
    .hword 0x46aa    @ 08024850 aa46
    pop {r4,r5,r6,r7}                        @ 08024852 f0bc
    pop {r0}                                 @ 08024854 01bc
    bx r0                                    @ 08024856 0047
PTR_gPrng_08024858:
    .word  gPrng                          @ 08024858 40000003
DAT_0802485c:
    .word  0x00000202                     @ 0802485c 02020000
PTR_gUnlockedDuelists_08024860:
    .word  gUnlockedDuelists              @ 08024860 5c6e0002
DAT_08024864:
    .word  0x02023360                     @ 08024864 60330202

@ Check whether all 4 consecutive scene slot entries have their low 12 bits >= threshold.
@ Base address = 0x02006e60 + (slot_idx-1)*20 (r0 is 1-based; stride = 5*4=20 bytes).
@ Reads 4 halfwords at 4-byte intervals; extracts bits[11:0] of each via lsls/lsrs #0x14.
@ Returns 1 if all 4 values >= r1 (threshold), 0 if any value < threshold.
@ Pure read, no external writes.
@ Constants: SCENE_SLOT_BASE=0x02006e60; SLOT_ENTRY_SIZE=20; ENTRY_VALUE_MASK=0xFFF; INNER_COUNT=4.
check_scene_slot_all_entries_meet_threshold:
    push {r4,lr}                             @ 08024868 10b5
    adds r3,r1,#0x0    @ 0802486a 0b1c
    subs r0,#0x1    @ 0802486c 0138
    lsls r1,r0,#0x2    @ 0802486e 8100
    adds r1,r1,r0    @ 08024870 0918
    movs r2,#0x0    @ 08024872 0022
    ldr r0, DAT_0802488c                     @ 08024874 0548
    lsls r1,r1,#0x2    @ 08024876 8900
    ldr r4, DAT_08024890                     @ 08024878 054c
    adds r0,r0,r4    @ 0802487a 0019
    adds r1,r1,r0    @ 0802487c 0918
LAB_0802487e:
    ldrh r4,[r1,#0x0]                        @ 0802487e 0c88
    lsls r0,r4,#0x14    @ 08024880 2005
    lsrs r0,r0,#0x14    @ 08024882 000d
    cmp r0,r3                                @ 08024884 9842
    bge LAB_08024894                         @ 08024886 05da
    movs r0,#0x0    @ 08024888 0020
    b LAB_0802489e                           @ 0802488a 08e0
DAT_0802488c:
    .word  0x02000000                     @ 0802488c 00000002
DAT_08024890:
    .word  0x00006e60                     @ 08024890 606e0000
LAB_08024894:
    adds r1,#0x4    @ 08024894 0431
    adds r2,#0x1    @ 08024896 0132
    cmp r2,#0x4                              @ 08024898 042a
    ble LAB_0802487e                         @ 0802489a f0dd
    movs r0,#0x1    @ 0802489c 0120
LAB_0802489e:
    pop {r4}                                 @ 0802489e 10bc
    pop {r1}                                 @ 080248a0 02bc
    bx r1                                    @ 080248a2 0847

@ Called by FUN_080dafc4 (scene_pack/duel_puzzle/opp_wins), FUN_080e1020 (scene_duel_puzzle/opp_wins), FUN_080e328c (card_ids/duel_puzzle/opp_wins) to compute total challenge clear rate for percentage display. Sequentially calls get_expert_challenge_count (-> r4), get_duel_puzzle_count (-> r5), get_standard_challenge_count (-> r0); sums to total. If total is zero jumps to LAB_080248dc (r6=0, computes percentage directly). Otherwise iterates [0x02006c3c] entry array (4 bytes each, total_count entries): extracts bits[1:0] of each entry, counts entries equal to 1 (cleared) into r6. Finally computes r6*100/__divsi3(total_count) and returns r0 = clear percentage [0..100].
@ 
@ Constants:
@ ENTRY_ARRAY_BASE = 0x02006c3c (EWRAM challenge entry array base)
@ ENTRY_STRIDE = 4 (bytes per entry)
@ CLEARED_BIT_MASK = 0x3 (bits[1:0], value 1 => cleared)
@ PERCENT_SCALE = 100 (multiplier before integer division)
get_total_challenge_cleared_count:
    push {r4,r5,r6,lr}                       @ 080248a4 70b5
    movs r6,#0x0    @ 080248a6 0026
    bl get_expert_challenge_count            @ 080248a8 bcf06eff
    adds r4,r0,#0x0    @ 080248ac 041c
    bl get_duel_puzzle_count                 @ 080248ae bef0d3fc
    adds r5,r0,#0x0    @ 080248b2 051c
    bl get_standard_challenge_count          @ 080248b4 bcf09afb
    adds r4,r4,r5    @ 080248b8 6419
    adds r1,r4,r0    @ 080248ba 2118
    cmp r6,r1                                @ 080248bc 8e42
    bge LAB_080248dc                         @ 080248be 0dda
    ldr r0, DAT_080248ec                     @ 080248c0 0a48
    ldr r2, DAT_080248f0                     @ 080248c2 0b4a
    adds r3,r0,r2    @ 080248c4 8318
    adds r2,r1,#0x0    @ 080248c6 0a1c
LAB_080248c8:
    ldrb r4,[r3,#0x0]                        @ 080248c8 1c78
    lsls r0,r4,#0x1e    @ 080248ca a007
    lsrs r0,r0,#0x1e    @ 080248cc 800f
    cmp r0,#0x1                              @ 080248ce 0128
    bne LAB_080248d4                         @ 080248d0 00d1
    adds r6,#0x1    @ 080248d2 0136
LAB_080248d4:
    adds r3,#0x4    @ 080248d4 0433
    subs r2,#0x1    @ 080248d6 013a
    cmp r2,#0x0                              @ 080248d8 002a
    bne LAB_080248c8                         @ 080248da f5d1
LAB_080248dc:
    movs r0,#0x64    @ 080248dc 6420
    muls r0,r6    @ 080248de 7043
    bl __divsi3                              @ 080248e0 e9f090fe
    pop {r4,r5,r6}                           @ 080248e4 70bc
    pop {r1}                                 @ 080248e6 02bc
    bx r1                                    @ 080248e8 0847
    .zero  0x2
DAT_080248ec:
    .word  0x02000000                     @ 080248ec 00000002
DAT_080248f0:
    .word  0x00006c3c                     @ 080248f0 3c6c0000

@ Iterates all 27 field slots (r4 from 0 to 0x1a=26), checks each slot state via jump
@ table (PTR_PTR_0802490c, 27 entries): if the handler returns nonzero (r1 != 0), sets
@ the corresponding bit in r5 (movs r0,#0x1; lsls r0,r4; orrs r5,r0). After the loop,
@ writes r5 to gPrng+0x6e5c (field slot activation bitmap), writes halfword 1 to
@ 0x02023360, then iterates active bits 0..0x1a writing each slot index into the deck
@ slot count table (0x02023360+2*n). Finally calls init_puzzle_wram_then_copy to sync
@ field state. Called by three scene-switch functions (FUN_08025d58 / FUN_0802727c /
@ FUN_08027a0c) at duel start.
@ 
@ Constants:
@ - 0x1a = 26 (max slot index, 27 slots total)
@ - PTR_PTR_0802490c jump table: 27 entries, indices 0..4 -> default path LAB_080249f8
@ - gPrng+0x6e5c = 0x02000000+0x6e5c (field slot activation bitmap storage)
@ - 0x02023360 = deck slot state table base
build_field_slot_bitmask:
    push {r4,r5,r6,lr}                       @ 080248f4 70b5
    movs r5,#0x0    @ 080248f6 0025
    movs r4,#0x0    @ 080248f8 0024
LAB_080248fa:
    movs r1,#0x0    @ 080248fa 0021
    cmp r4,#0x1a                             @ 080248fc 1a2c
    bhi LAB_080249f4                         @ 080248fe 79d8
    lsls r0,r4,#0x2    @ 08024900 a000
    ldr r1, PTR_PTR_0802490c                 @ 08024902 0249
    adds r0,r0,r1    @ 08024904 4018
    ldr r0,[r0,#0x0]                         @ 08024906 0068
    .hword 0x4687    @ 08024908 8746
    .zero  0x2
PTR_PTR_0802490c:
    .word  0x08024910                     @ 0802490c 10490208
PTR_LAB_08024910:
    .word  0x080249f8                     @ 08024910 f8490208
    .word  0x080249f8                     @ 08024914 f8490208
    .word  0x080249f8                     @ 08024918 f8490208
    .word  0x080249f8                     @ 0802491c f8490208
    .word  0x080249f8                     @ 08024920 f8490208
    .word  0x0802497c                     @ 08024924 7c490208
    .word  0x08024982                     @ 08024928 82490208
    .word  0x08024982                     @ 0802492c 82490208
    .word  0x08024988                     @ 08024930 88490208
    .word  0x08024988                     @ 08024934 88490208
    .word  0x0802498c                     @ 08024938 8c490208
    .word  0x08024992                     @ 0802493c 92490208
    .word  0x08024992                     @ 08024940 92490208
    .word  0x08024998                     @ 08024944 98490208
    .word  0x08024998                     @ 08024948 98490208
    .word  0x0802499c                     @ 0802494c 9c490208
    .word  0x080249a2                     @ 08024950 a2490208
    .word  0x080249a2                     @ 08024954 a2490208
    .word  0x080249a8                     @ 08024958 a8490208
    .word  0x080249a8                     @ 0802495c a8490208
    .word  0x080249ac                     @ 08024960 ac490208
    .word  0x080249ac                     @ 08024964 ac490208
    .word  0x080249b8                     @ 08024968 b8490208
    .word  0x080249c4                     @ 0802496c c4490208
    .word  0x080249d0                     @ 08024970 d0490208
    .word  0x080249dc                     @ 08024974 dc490208
    .word  0x080249e8                     @ 08024978 e8490208
DAT_0802497c:
    ROM_INCBIN 0x2497c, 0x78
LAB_080249f4:
    cmp r1,#0x0                              @ 080249f4 0029
    beq LAB_080249fe                         @ 080249f6 02d0
LAB_080249f8:
    movs r0,#0x1    @ 080249f8 0120
    lsls r0,r4    @ 080249fa a040
    orrs r5,r0    @ 080249fc 0543
LAB_080249fe:
    adds r4,#0x1    @ 080249fe 0134
    cmp r4,#0x1a                             @ 08024a00 1a2c
    bgt LAB_08024a06                         @ 08024a02 00dc
    b LAB_080248fa                           @ 08024a04 79e7
LAB_08024a06:
    ldr r0, DWORD_08024a5c                   @ 08024a06 1548
    ldr r1, DWORD_08024a60                   @ 08024a08 1549
    adds r0,r0,r1    @ 08024a0a 4018
    ldr r1,[r0,#0x0]                         @ 08024a0c 0168
    orrs r1,r5    @ 08024a0e 2943
    str r1,[r0,#0x0]                         @ 08024a10 0160
    ldr r2, DWORD_08024a64                   @ 08024a12 144a
    movs r0,#0x1    @ 08024a14 0120
    strh r0,[r2,#0x0]                        @ 08024a16 1080
    movs r4,#0x0    @ 08024a18 0024
    adds r5,r2,#0x0    @ 08024a1a 151c
    movs r6,#0x1    @ 08024a1c 0126
    adds r3,r5,#0x0    @ 08024a1e 2b1c
LAB_08024a20:
    adds r0,r6,#0x0    @ 08024a20 301c
    lsls r0,r4    @ 08024a22 a040
    ands r0,r1    @ 08024a24 0840
    adds r2,r4,#0x1    @ 08024a26 621c
    cmp r0,#0x0                              @ 08024a28 0028
    beq LAB_08024a2e                         @ 08024a2a 00d0
    strh r2,[r3,#0x0]                        @ 08024a2c 1a80
LAB_08024a2e:
    adds r4,r2,#0x0    @ 08024a2e 141c
    cmp r4,#0x1a                             @ 08024a30 1a2c
    ble LAB_08024a20                         @ 08024a32 f5dd
    ldrh r0,[r5,#0x0]                        @ 08024a34 2888
    adds r0,#0x4    @ 08024a36 0430
    movs r1,#0x5    @ 08024a38 0521
    bl __divsi3                              @ 08024a3a e9f0e3fd
    movs r1,#0x7    @ 08024a3e 0721
    ands r0,r1    @ 08024a40 0840
    lsls r0,r0,#0x2    @ 08024a42 8000
    movs r1,#0x1d    @ 08024a44 1d21
    rsbs r1,r1,#0    @ 08024a46 4942
    ldrb r2,[r5,#0x3]                        @ 08024a48 ea78
    ands r1,r2    @ 08024a4a 1140
    orrs r1,r0    @ 08024a4c 0143
    strb r1,[r5,#0x3]                        @ 08024a4e e970
    bl init_puzzle_wram_then_copy            @ 08024a50 d5f01af9
    pop {r4,r5,r6}                           @ 08024a54 70bc
    pop {r0}                                 @ 08024a56 01bc
    bx r0                                    @ 08024a58 0047
    .zero  0x2
DWORD_08024a5c:
    .word  0x02000000                     @ 08024a5c 00000002
DWORD_08024a60:
    .word  0x00006e5c                     @ 08024a60 5c6e0000
DWORD_08024a64:
    .word  0x02023360                     @ 08024a64 60330202

@ Selects a ROM font data pointer based on gPrng+0x6c2c bits[2:0] (font_type, [1..5]),
@ stores it in high registers r8/r9/r10/r11, then calls setup_line_buf_pos_and_font
@ (x=0x16, font_id=2) to configure the line buffer position, and finally calls
@ render_text_with_u16_width for actual text rendering. Input r0 determines the line
@ buffer Y offset ((r0&7)*0x2c + 0x152) and X offset ((r0&0xf)*2+6, truncated to 5 bits).
@ Called by FUN_08026748 and FUN_08026858 in text rendering scenes.
@ 
@ Constants:
@ - gPrng+0x6c2c = 0x02006c2c (font_type field, bits[2:0])
@ - 0xa9*2 = 0x152 (Y base offset)
@ - 0x2c = 44 (line spacing step)
@ - font_type 1 ptr = 0x09dca398 (DAT_08024c60)
@ - font_type 2 ptr = 0x09dd5b3a (DAT_08024af0)
@ - font_type 3 ptr = 0x09de1e76 (DAT_08024ae4)
@ - font_type 4 ptr = 0x09dee362 (DAT_08024ad8)
@ - font_type 5 ptr = 0x09df9f2a (DAT_08024ac8 0x09dbf4d6 + DAT_08024acc 0x0003aa54)
render_text_with_font_type_select:
    push {r4,r5,r6,r7,lr}                    @ 08024a68 f0b5
    .hword 0x4657    @ 08024a6a 5746
    .hword 0x464e    @ 08024a6c 4e46
    .hword 0x4645    @ 08024a6e 4546
    push {r5,r6,r7}                          @ 08024a70 e0b4
    sub sp,#0xc                              @ 08024a72 83b0
    adds r7,r0,#0x0    @ 08024a74 071c
    movs r2,#0x7    @ 08024a76 0722
    ands r0,r2    @ 08024a78 1040
    movs r1,#0x2c    @ 08024a7a 2c21
    muls r0,r1    @ 08024a7c 4843
    movs r1,#0xa9    @ 08024a7e a921
    lsls r1,r1,#0x1    @ 08024a80 4900
    adds r1,r1,r0    @ 08024a82 0918
    .hword 0x4688    @ 08024a84 8846
    movs r0,#0xf    @ 08024a86 0f20
    ands r0,r7    @ 08024a88 3840
    lsls r0,r0,#0x1    @ 08024a8a 4000
    adds r0,#0x6    @ 08024a8c 0630
    str r0,[sp,#0x4]                         @ 08024a8e 0190
    movs r0,#0x1f    @ 08024a90 1f20
    ldr r3,[sp,#0x4]                         @ 08024a92 019b
    ands r3,r0    @ 08024a94 0340
    str r3,[sp,#0x4]                         @ 08024a96 0193
    ldr r0, DWORD_08024ac0                   @ 08024a98 0948
    ldr r4, DWORD_08024ac4                   @ 08024a9a 0a4c
    adds r0,r0,r4    @ 08024a9c 0019
    ldrb r0,[r0,#0x0]                        @ 08024a9e 0078
    ands r2,r0    @ 08024aa0 0240
    cmp r2,#0x1                              @ 08024aa2 012a
    beq LAB_08024af4                         @ 08024aa4 26d0
    cmp r2,#0x2                              @ 08024aa6 022a
    beq LAB_08024ae8                         @ 08024aa8 1ed0
    cmp r2,#0x3                              @ 08024aaa 032a
    beq LAB_08024adc                         @ 08024aac 16d0
    cmp r2,#0x4                              @ 08024aae 042a
    beq LAB_08024ad0                         @ 08024ab0 0ed0
    ldr r0, DWORD_08024ac8                   @ 08024ab2 0548
    .hword 0x4681    @ 08024ab4 8146
    cmp r2,#0x5                              @ 08024ab6 052a
    bne LAB_08024af8                         @ 08024ab8 1ed1
    ldr r1, DWORD_08024acc                   @ 08024aba 0449
    add r9,r1                                @ 08024abc 8944
    b LAB_08024af8                           @ 08024abe 1be0
DWORD_08024ac0:
    .word  0x02000000                     @ 08024ac0 00000002
DWORD_08024ac4:
    .word  0x00006c2c                     @ 08024ac4 2c6c0000
DWORD_08024ac8:
    .word  0x09dbf4d6                     @ 08024ac8 d6f4db09
DWORD_08024acc:
    .word  0x0003aa54                     @ 08024acc 54aa0300
LAB_08024ad0:
    ldr r2, DWORD_08024ad8                   @ 08024ad0 014a
    .hword 0x4691    @ 08024ad2 9146
    b LAB_08024af8                           @ 08024ad4 10e0
    .zero  0x2
DWORD_08024ad8:
    .word  0x09dee362                     @ 08024ad8 62e3de09
LAB_08024adc:
    ldr r3, DWORD_08024ae4                   @ 08024adc 014b
    .hword 0x4699    @ 08024ade 9946
    b LAB_08024af8                           @ 08024ae0 0ae0
    .zero  0x2
DWORD_08024ae4:
    .word  0x09de1e76                     @ 08024ae4 761ede09
LAB_08024ae8:
    ldr r4, DWORD_08024af0                   @ 08024ae8 014c
    .hword 0x46a1    @ 08024aea a146
    b LAB_08024af8                           @ 08024aec 04e0
    .zero  0x2
DWORD_08024af0:
    .word  0x09dd5b3a                     @ 08024af0 3a5bdd09
LAB_08024af4:
    ldr r0, DWORD_08024c60                   @ 08024af4 5a48
    .hword 0x4681    @ 08024af6 8146
LAB_08024af8:
    movs r0,#0x16    @ 08024af8 1620
    movs r1,#0x2    @ 08024afa 0221
    bl setup_line_buf_pos_and_font           @ 08024afc ccf05af8
    ldr r1, DWORD_08024c64                   @ 08024b00 5849
    .hword 0x468a    @ 08024b02 8a46
    ldr r2, DWORD_08024c68                   @ 08024b04 584a
    ldr r3, DWORD_08024c6c                   @ 08024b06 594b
    adds r0,r2,r3    @ 08024b08 d018
    movs r1,#0x7    @ 08024b0a 0721
    ldrb r0,[r0,#0x0]                        @ 08024b0c 0078
    ands r1,r0    @ 08024b0e 0140
    rsbs r1,r1,#0    @ 08024b10 4942
    movs r0,#0x1    @ 08024b12 0120
    .hword 0x466c    @ 08024b14 6c46
    strb r0,[r4,#0x8]                        @ 08024b16 2072
    lsrs r1,r1,#0x1f    @ 08024b18 c90f
    movs r0,#0x2    @ 08024b1a 0220
    rsbs r0,r0,#0    @ 08024b1c 4042
    .hword 0x4652    @ 08024b1e 5246
    ldrb r2,[r2,#0x8]                        @ 08024b20 127a
    ands r0,r2    @ 08024b22 1040
    orrs r0,r1    @ 08024b24 0843
    movs r1,#0x2    @ 08024b26 0221
    orrs r0,r1    @ 08024b28 0843
    .hword 0x4653    @ 08024b2a 5346
    strb r0,[r3,#0x8]                        @ 08024b2c 1872
    lsls r1,r0,#0x1e    @ 08024b2e 8107
    lsrs r1,r1,#0x1f    @ 08024b30 c90f
    lsls r1,r1,#0x2    @ 08024b32 8900
    lsls r0,r0,#0x1f    @ 08024b34 c007
    lsrs r0,r0,#0x1f    @ 08024b36 c00f
    lsls r0,r0,#0x3    @ 08024b38 c000
    adds r1,r1,r0    @ 08024b3a 0918
    ldr r4, DWORD_08024c70                   @ 08024b3c 4c4c
    adds r1,r1,r4    @ 08024b3e 0919
    ldr r0,[r1,#0x0]                         @ 08024b40 0868
    str r0,[r3,#0x4]                         @ 08024b42 5860
    .hword 0x466c    @ 08024b44 6c46
    adds r5,r7,#0x1    @ 08024b46 7d1c
    adds r0,r5,#0x0    @ 08024b48 281c
    movs r1,#0xa    @ 08024b4a 0a21
    bl __divsi3                              @ 08024b4c e9f05afd
    movs r1,#0xa    @ 08024b50 0a21
    bl __modsi3                              @ 08024b52 e9f0a3fd
    adds r0,#0x30    @ 08024b56 3030
    movs r6,#0x0    @ 08024b58 0026
    strb r0,[r4,#0x0]                        @ 08024b5a 2070
    .hword 0x466c    @ 08024b5c 6c46
    adds r0,r5,#0x0    @ 08024b5e 281c
    movs r1,#0xa    @ 08024b60 0a21
    bl __modsi3                              @ 08024b62 e9f09bfd
    adds r0,#0x30    @ 08024b66 3030
    strb r0,[r4,#0x1]                        @ 08024b68 6070
    .hword 0x4669    @ 08024b6a 6946
    movs r0,#0x3a    @ 08024b6c 3a20
    strb r0,[r1,#0x2]                        @ 08024b6e 8870
    .hword 0x4668    @ 08024b70 6846
    strb r6,[r0,#0x3]                        @ 08024b72 c670
    movs r0,#0x0    @ 08024b74 0020
    movs r1,#0x2    @ 08024b76 0221
    movs r2,#0x7    @ 08024b78 0722
    .hword 0x466b    @ 08024b7a 6b46
    bl render_text_with_u16_width            @ 08024b7c cef056f8
    adds r0,r7,#0x0    @ 08024b80 381c
    cmp r7,#0x0                              @ 08024b82 002f
    bge LAB_08024b88                         @ 08024b84 00da
    adds r0,#0x1f    @ 08024b86 1f30
LAB_08024b88:
    asrs r0,r0,#0x5    @ 08024b88 4011
    lsls r2,r0,#0x2    @ 08024b8a 8200
    ldr r3, DWORD_08024c68                   @ 08024b8c 364b
    ldr r4, DWORD_08024c74                   @ 08024b8e 394c
    adds r1,r3,r4    @ 08024b90 1919
    adds r2,r2,r1    @ 08024b92 5218
    lsls r0,r0,#0x5    @ 08024b94 4001
    subs r0,r7,r0    @ 08024b96 381a
    movs r1,#0x1    @ 08024b98 0121
    lsls r1,r0    @ 08024b9a 8140
    ldr r0,[r2,#0x0]                         @ 08024b9c 1068
    ands r0,r1    @ 08024b9e 0840
    cmp r0,#0x0                              @ 08024ba0 0028
    beq LAB_08024bee                         @ 08024ba2 24d0
    lsls r0,r7,#0x3    @ 08024ba4 f800
    adds r0,r0,r7    @ 08024ba6 c019
    lsls r0,r0,#0x2    @ 08024ba8 8000
    subs r0,r0,r7    @ 08024baa c01b
    lsls r0,r0,#0x3    @ 08024bac c000
    ldr r2, DWORD_08024c78                   @ 08024bae 324a
    adds r1,r3,r2    @ 08024bb0 9918
    adds r1,r1,r0    @ 08024bb2 0918
    .hword 0x4689    @ 08024bb4 8946
    adds r0,r0,r3    @ 08024bb6 c018
    ldr r3, DWORD_08024c7c                   @ 08024bb8 304b
    adds r0,r0,r3    @ 08024bba c018
    ldrb r0,[r0,#0x0]                        @ 08024bbc 0078
    rsbs r1,r0,#0    @ 08024bbe 4142
    lsrs r1,r1,#0x1f    @ 08024bc0 c90f
    .hword 0x466c    @ 08024bc2 6c46
    ldrb r4,[r4,#0x8]                        @ 08024bc4 247a
    ands r1,r4    @ 08024bc6 2140
    movs r0,#0x2    @ 08024bc8 0220
    rsbs r0,r0,#0    @ 08024bca 4042
    .hword 0x4652    @ 08024bcc 5246
    ldrb r2,[r2,#0x8]                        @ 08024bce 127a
    ands r0,r2    @ 08024bd0 1040
    orrs r0,r1    @ 08024bd2 0843
    .hword 0x4653    @ 08024bd4 5346
    strb r0,[r3,#0x8]                        @ 08024bd6 1872
    lsls r1,r0,#0x1e    @ 08024bd8 8107
    lsrs r1,r1,#0x1f    @ 08024bda c90f
    lsls r1,r1,#0x2    @ 08024bdc 8900
    lsls r0,r0,#0x1f    @ 08024bde c007
    lsrs r0,r0,#0x1f    @ 08024be0 c00f
    lsls r0,r0,#0x3    @ 08024be2 c000
    adds r1,r1,r0    @ 08024be4 0918
    ldr r4, DWORD_08024c70                   @ 08024be6 224c
    adds r1,r1,r4    @ 08024be8 0919
    ldr r0,[r1,#0x0]                         @ 08024bea 0868
    str r0,[r3,#0x4]                         @ 08024bec 5860
LAB_08024bee:
    .hword 0x4648    @ 08024bee 4846
    bl count_bytes_until_null                @ 08024bf0 d0f076fc
    lsls r1,r0,#0x1    @ 08024bf4 4100
    adds r1,r1,r0    @ 08024bf6 0918
    movs r0,#0x60    @ 08024bf8 6020
    subs r0,r0,r1    @ 08024bfa 401a
    movs r1,#0x2    @ 08024bfc 0221
    movs r2,#0x7    @ 08024bfe 0722
    .hword 0x464b    @ 08024c00 4b46
    bl text_render_wrapper                   @ 08024c02 cdf03bff
    .hword 0x4640    @ 08024c06 4046
    lsls r4,r0,#0x5    @ 08024c08 4401
    ldr r1, DWORD_08024c80                   @ 08024c0a 1d49
    adds r4,r4,r1    @ 08024c0c 6418
    movs r1,#0xb0    @ 08024c0e b021
    lsls r1,r1,#0x3    @ 08024c10 c900
    adds r0,r4,#0x0    @ 08024c12 201c
    bl zero_fill_by_halfword                 @ 08024c14 d0f02ef9
    adds r0,r4,#0x0    @ 08024c18 201c
    movs r1,#0x0    @ 08024c1a 0021
    bl commit_line_buffer_to_sprite_vram     @ 08024c1c cef016f9
    movs r1,#0x0    @ 08024c20 0021
    ldr r5, DWORD_08024c84                   @ 08024c22 184d
LAB_08024c24:
    ldr r2,[sp,#0x4]                         @ 08024c24 019a
    adds r0,r2,r1    @ 08024c26 5018
    lsls r0,r0,#0x10    @ 08024c28 0004
    lsrs r0,r0,#0xb    @ 08024c2a c00a
    adds r0,#0x4    @ 08024c2c 0430
    lsls r0,r0,#0x1    @ 08024c2e 4000
    adds r2,r0,r5    @ 08024c30 4219
    adds r4,r1,#0x1    @ 08024c32 4c1c
    movs r3,#0x15    @ 08024c34 1523
LAB_08024c36:
    .hword 0x4641    @ 08024c36 4146
    adds r0,r1,#0x1    @ 08024c38 481c
    lsls r0,r0,#0x10    @ 08024c3a 0004
    lsrs r0,r0,#0x10    @ 08024c3c 000c
    .hword 0x4680    @ 08024c3e 8046
    strh r1,[r2,#0x0]                        @ 08024c40 1180
    adds r2,#0x2    @ 08024c42 0232
    subs r3,#0x1    @ 08024c44 013b
    cmp r3,#0x0                              @ 08024c46 002b
    bge LAB_08024c36                         @ 08024c48 f5da
    adds r1,r4,#0x0    @ 08024c4a 211c
    cmp r1,#0x1                              @ 08024c4c 0129
    ble LAB_08024c24                         @ 08024c4e e9dd
    add sp,#0xc                              @ 08024c50 03b0
    pop {r3,r4,r5}                           @ 08024c52 38bc
    .hword 0x4698    @ 08024c54 9846
    .hword 0x46a1    @ 08024c56 a146
    .hword 0x46aa    @ 08024c58 aa46
    pop {r4,r5,r6,r7}                        @ 08024c5a f0bc
    pop {r0}                                 @ 08024c5c 01bc
    bx r0                                    @ 08024c5e 0047
DWORD_08024c60:
    .word  0x09dca398                     @ 08024c60 98a3dc09
DWORD_08024c64:
    .word  0x02006ed0                     @ 08024c64 d06e0002
DWORD_08024c68:
    .word  0x02000000                     @ 08024c68 00000002
DWORD_08024c6c:
    .word  0x00006c2c                     @ 08024c6c 2c6c0000
DWORD_08024c70:
    .word  font_jp_base_table             @ 08024c70 54f8e509
DWORD_08024c74:
    .word  0x000053f0                     @ 08024c74 f0530000
DWORD_08024c78:
    .word  0x00001250                     @ 08024c78 50120000
DWORD_08024c7c:
    .word  0x00001267                     @ 08024c7c 67120000
DWORD_08024c80:
    .word  0x06004000                     @ 08024c80 00400006
DWORD_08024c84:
    .word  0x06000800                     @ 08024c84 00080006

@ Card attribute render hub: first calls get_card_data_bit_by_index(4) to read card bit 4
@ (e.g. ATK type flag); skips if zero. Otherwise selects font pointer from font_type
@ (gPrng+0x6c2c bits[2:0]) and calls render_card_stat_with_number_alt (FUN_0802bc88)
@ to render the first attribute group; then calls render_game_string_with_number
@ (FUN_0802b940) with r2=100 for separator content; next calls get_card_data_bit_by_index(2)
@ and if nonzero, selects font and calls render_game_string_with_number (r1=2, r2=2).
@ Called by FUN_080277a4 in the card info display scene.
@ 
@ Constants:
@ - bit_index=4 = card data bit 4 (e.g. ATK/DEF type)
@ - bit_index=2 = card data bit 2 (e.g. card category)
@ - r2=0x64=100 = separator/value parameter for render_game_string_with_number
render_card_stats_to_line_buf:
    push {r4,r5,lr}                          @ 08024c88 30b5
    movs r0,#0x4    @ 08024c8a 0420
    bl get_card_data_bit_by_index            @ 08024c8c 70f0f2f8
    cmp r0,#0x0                              @ 08024c90 0028
    bgt LAB_08024c96                         @ 08024c92 00dc
    b LAB_08024d74                           @ 08024c94 6ee0
LAB_08024c96:
    ldr r0, DWORD_08024cc0                   @ 08024c96 0a48
    ldr r1, DWORD_08024cc4                   @ 08024c98 0a49
    adds r0,r0,r1    @ 08024c9a 4018
    movs r1,#0x7    @ 08024c9c 0721
    ldrb r0,[r0,#0x0]                        @ 08024c9e 0078
    ands r1,r0    @ 08024ca0 0140
    cmp r1,#0x1                              @ 08024ca2 0129
    beq LAB_08024ce8                         @ 08024ca4 20d0
    cmp r1,#0x2                              @ 08024ca6 0229
    beq LAB_08024ce0                         @ 08024ca8 1ad0
    cmp r1,#0x3                              @ 08024caa 0329
    beq LAB_08024cd8                         @ 08024cac 14d0
    cmp r1,#0x4                              @ 08024cae 0429
    beq LAB_08024cd0                         @ 08024cb0 0ed0
    ldr r4, DWORD_08024cc8                   @ 08024cb2 054c
    cmp r1,#0x5                              @ 08024cb4 0529
    bne LAB_08024cea                         @ 08024cb6 18d1
    ldr r2, DWORD_08024ccc                   @ 08024cb8 044a
    adds r4,r4,r2    @ 08024cba a418
    b LAB_08024cea                           @ 08024cbc 15e0
    .zero  0x2
DWORD_08024cc0:
    .word  0x02000000                     @ 08024cc0 00000002
DWORD_08024cc4:
    .word  0x00006c2c                     @ 08024cc4 2c6c0000
DWORD_08024cc8:
    .word  0x09dbe4c2                     @ 08024cc8 c2e4db09
DWORD_08024ccc:
    .word  0x0003aaee                     @ 08024ccc eeaa0300
LAB_08024cd0:
    ldr r4, DWORD_08024cd4                   @ 08024cd0 004c
    b LAB_08024cea                           @ 08024cd2 0ae0
DWORD_08024cd4:
    .word  0x09ded2d8                     @ 08024cd4 d8d2de09
LAB_08024cd8:
    ldr r4, DWORD_08024cdc                   @ 08024cd8 004c
    b LAB_08024cea                           @ 08024cda 06e0
DWORD_08024cdc:
    .word  0x09de0e7e                     @ 08024cdc 7e0ede09
LAB_08024ce0:
    ldr r4, DWORD_08024ce4                   @ 08024ce0 004c
    b LAB_08024cea                           @ 08024ce2 02e0
DWORD_08024ce4:
    .word  0x09dd4bde                     @ 08024ce4 de4bdd09
LAB_08024ce8:
    ldr r4, DWORD_08024d34                   @ 08024ce8 124c
LAB_08024cea:
    movs r0,#0x4    @ 08024cea 0420
    bl get_card_data_bit_by_index            @ 08024cec 70f0c2f8
    adds r1,r0,#0x0    @ 08024cf0 011c
    adds r0,r4,#0x0    @ 08024cf2 201c
    bl render_card_stat_with_number_alt      @ 08024cf4 06f0c8ff
    ldr r0, DWORD_08024d38                   @ 08024cf8 0f48
    movs r1,#0x3    @ 08024cfa 0321
    movs r2,#0x64    @ 08024cfc 6422
    bl render_game_string_with_number        @ 08024cfe 06f01ffe
    movs r0,#0x2    @ 08024d02 0220
    bl get_card_data_bit_by_index            @ 08024d04 70f0b6f8
    cmp r0,#0x0                              @ 08024d08 0028
    bne LAB_08024dce                         @ 08024d0a 60d1
    ldr r0, DWORD_08024d3c                   @ 08024d0c 0b48
    ldr r3, DWORD_08024d40                   @ 08024d0e 0c4b
    adds r0,r0,r3    @ 08024d10 c018
    movs r1,#0x7    @ 08024d12 0721
    ldrb r0,[r0,#0x0]                        @ 08024d14 0078
    ands r1,r0    @ 08024d16 0140
    cmp r1,#0x1                              @ 08024d18 0129
    beq LAB_08024d64                         @ 08024d1a 23d0
    cmp r1,#0x2                              @ 08024d1c 0229
    beq LAB_08024d5c                         @ 08024d1e 1dd0
    cmp r1,#0x3                              @ 08024d20 0329
    beq LAB_08024d54                         @ 08024d22 17d0
    cmp r1,#0x4                              @ 08024d24 0429
    beq LAB_08024d4c                         @ 08024d26 11d0
    ldr r0, DWORD_08024d44                   @ 08024d28 0648
    cmp r1,#0x5                              @ 08024d2a 0529
    bne LAB_08024d66                         @ 08024d2c 1bd1
    ldr r1, DWORD_08024d48                   @ 08024d2e 0649
    adds r0,r0,r1    @ 08024d30 4018
    b LAB_08024d66                           @ 08024d32 18e0
DWORD_08024d34:
    .word  0x09dc957a                     @ 08024d34 7a95dc09
DWORD_08024d38:
    .word  0x09e3e740                     @ 08024d38 40e7e309
DWORD_08024d3c:
    .word  0x02000000                     @ 08024d3c 00000002
DWORD_08024d40:
    .word  0x00006c2c                     @ 08024d40 2c6c0000
DWORD_08024d44:
    .word  0x09dbea7e                     @ 08024d44 7eeadb09
DWORD_08024d48:
    .word  0x0003ab4c                     @ 08024d48 4cab0300
LAB_08024d4c:
    ldr r0, DWORD_08024d50                   @ 08024d4c 0048
    b LAB_08024d66                           @ 08024d4e 0ae0
DWORD_08024d50:
    .word  0x09ded9d6                     @ 08024d50 d6d9de09
LAB_08024d54:
    ldr r0, DWORD_08024d58                   @ 08024d54 0048
    b LAB_08024d66                           @ 08024d56 06e0
DWORD_08024d58:
    .word  0x09de14ec                     @ 08024d58 ec14de09
LAB_08024d5c:
    ldr r0, DWORD_08024d60                   @ 08024d5c 0048
    b LAB_08024d66                           @ 08024d5e 02e0
DWORD_08024d60:
    .word  0x09dd5204                     @ 08024d60 0452dd09
LAB_08024d64:
    ldr r0, DWORD_08024d70                   @ 08024d64 0248
LAB_08024d66:
    movs r1,#0x2    @ 08024d66 0221
    movs r2,#0x2    @ 08024d68 0222
    bl render_game_string_with_number        @ 08024d6a 06f0e9fd
    b LAB_08024dce                           @ 08024d6e 2ee0
DWORD_08024d70:
    .word  0x09dc9b3c                     @ 08024d70 3c9bdc09
LAB_08024d74:
    ldr r0, DWORD_08024d9c                   @ 08024d74 0948
    ldr r2, DWORD_08024da0                   @ 08024d76 0a4a
    adds r0,r0,r2    @ 08024d78 8018
    movs r1,#0x7    @ 08024d7a 0721
    ldrb r0,[r0,#0x0]                        @ 08024d7c 0078
    ands r1,r0    @ 08024d7e 0140
    cmp r1,#0x1                              @ 08024d80 0129
    beq LAB_08024dc4                         @ 08024d82 1fd0
    cmp r1,#0x2                              @ 08024d84 0229
    beq LAB_08024dbc                         @ 08024d86 19d0
    cmp r1,#0x3                              @ 08024d88 0329
    beq LAB_08024db4                         @ 08024d8a 13d0
    cmp r1,#0x4                              @ 08024d8c 0429
    beq LAB_08024dac                         @ 08024d8e 0dd0
    ldr r0, DWORD_08024da4                   @ 08024d90 0448
    cmp r1,#0x5                              @ 08024d92 0529
    bne LAB_08024dc6                         @ 08024d94 17d1
    ldr r3, DWORD_08024da8                   @ 08024d96 044b
    adds r0,r0,r3    @ 08024d98 c018
    b LAB_08024dc6                           @ 08024d9a 14e0
DWORD_08024d9c:
    .word  0x02000000                     @ 08024d9c 00000002
DWORD_08024da0:
    .word  0x00006c2c                     @ 08024da0 2c6c0000
DWORD_08024da4:
    .word  0x09dbea98                     @ 08024da4 98eadb09
DWORD_08024da8:
    .word  0x0003ab4e                     @ 08024da8 4eab0300
LAB_08024dac:
    ldr r0, DWORD_08024db0                   @ 08024dac 0048
    b LAB_08024dc6                           @ 08024dae 0ae0
DWORD_08024db0:
    .word  0x09ded9f4                     @ 08024db0 f4d9de09
LAB_08024db4:
    ldr r0, DWORD_08024db8                   @ 08024db4 0048
    b LAB_08024dc6                           @ 08024db6 06e0
DWORD_08024db8:
    .word  0x09de1504                     @ 08024db8 0415de09
LAB_08024dbc:
    ldr r0, DWORD_08024dc0                   @ 08024dbc 0048
    b LAB_08024dc6                           @ 08024dbe 02e0
DWORD_08024dc0:
    .word  0x09dd5220                     @ 08024dc0 2052dd09
LAB_08024dc4:
    ldr r0, DWORD_08024e04                   @ 08024dc4 0f48
LAB_08024dc6:
    movs r1,#0x96    @ 08024dc6 9621
    lsls r1,r1,#0x1    @ 08024dc8 4900
    bl render_card_stat_with_number_alt      @ 08024dca 06f05dff
LAB_08024dce:
    movs r0,#0x0    @ 08024dce 0020
    bl get_card_data_bit_by_index            @ 08024dd0 70f050f8
    ldr r1, DWORD_08024e08                   @ 08024dd4 0c49
    cmp r0,r1                                @ 08024dd6 8842
    ble LAB_08024e4a                         @ 08024dd8 37dd
    ldr r0, DWORD_08024e0c                   @ 08024dda 0c48
    ldr r1, DWORD_08024e10                   @ 08024ddc 0c49
    adds r0,r0,r1    @ 08024dde 4018
    movs r1,#0x7    @ 08024de0 0721
    ldrb r0,[r0,#0x0]                        @ 08024de2 0078
    ands r1,r0    @ 08024de4 0140
    cmp r1,#0x1                              @ 08024de6 0129
    beq LAB_08024e34                         @ 08024de8 24d0
    cmp r1,#0x2                              @ 08024dea 0229
    beq LAB_08024e2c                         @ 08024dec 1ed0
    cmp r1,#0x3                              @ 08024dee 0329
    beq LAB_08024e24                         @ 08024df0 18d0
    cmp r1,#0x4                              @ 08024df2 0429
    beq LAB_08024e1c                         @ 08024df4 12d0
    ldr r4, DWORD_08024e14                   @ 08024df6 074c
    cmp r1,#0x5                              @ 08024df8 0529
    bne LAB_08024e36                         @ 08024dfa 1cd1
    ldr r2, DWORD_08024e18                   @ 08024dfc 064a
    adds r4,r4,r2    @ 08024dfe a418
    b LAB_08024e36                           @ 08024e00 19e0
    .zero  0x2
DWORD_08024e04:
    .word  0x09dc9b56                     @ 08024e04 569bdc09
DWORD_08024e08:
    .word  0x00000bb8                     @ 08024e08 b80b0000
DWORD_08024e0c:
    .word  0x02000000                     @ 08024e0c 00000002
DWORD_08024e10:
    .word  0x00006c2c                     @ 08024e10 2c6c0000
DWORD_08024e14:
    .word  0x09dbea14                     @ 08024e14 14eadb09
DWORD_08024e18:
    .word  0x0003ab50                     @ 08024e18 50ab0300
LAB_08024e1c:
    ldr r4, DWORD_08024e20                   @ 08024e1c 004c
    b LAB_08024e36                           @ 08024e1e 0ae0
DWORD_08024e20:
    .word  0x09ded95e                     @ 08024e20 5ed9de09
LAB_08024e24:
    ldr r4, DWORD_08024e28                   @ 08024e24 004c
    b LAB_08024e36                           @ 08024e26 06e0
DWORD_08024e28:
    .word  0x09de1474                     @ 08024e28 7414de09
LAB_08024e2c:
    ldr r4, DWORD_08024e30                   @ 08024e2c 004c
    b LAB_08024e36                           @ 08024e2e 02e0
DWORD_08024e30:
    .word  0x09dd518e                     @ 08024e30 8e51dd09
LAB_08024e34:
    ldr r4, DWORD_08024ea4                   @ 08024e34 1b4c
LAB_08024e36:
    movs r0,#0x0    @ 08024e36 0020
    bl get_card_data_bit_by_index            @ 08024e38 70f01cf8
    movs r1,#0x64    @ 08024e3c 6421
    bl __divsi3                              @ 08024e3e e9f0e1fb
    adds r1,r0,#0x0    @ 08024e42 011c
    adds r0,r4,#0x0    @ 08024e44 201c
    bl render_card_stat_with_number_alt      @ 08024e46 06f01fff
LAB_08024e4a:
    movs r0,#0x1    @ 08024e4a 0120
    bl get_card_data_bit_by_index            @ 08024e4c 70f012f8
    movs r4,#0xfa    @ 08024e50 fa24
    lsls r4,r4,#0x4    @ 08024e52 2401
    cmp r0,r4                                @ 08024e54 a042
    bgt LAB_08024e62                         @ 08024e56 04dc
    movs r0,#0x3    @ 08024e58 0320
    bl get_card_data_bit_by_index            @ 08024e5a 70f00bf8
    cmp r0,r4                                @ 08024e5e a042
    ble LAB_08024ee2                         @ 08024e60 3fdd
LAB_08024e62:
    movs r0,#0x3    @ 08024e62 0320
    bl get_card_data_bit_by_index            @ 08024e64 70f006f8
    adds r5,r0,#0x0    @ 08024e68 051c
    movs r0,#0x1    @ 08024e6a 0120
    bl get_card_data_bit_by_index            @ 08024e6c 70f002f8
    cmp r5,r0                                @ 08024e70 8542
    bge LAB_08024e7c                         @ 08024e72 03da
    movs r0,#0x1    @ 08024e74 0120
    bl get_card_data_bit_by_index            @ 08024e76 6ff0fdff
    adds r5,r0,#0x0    @ 08024e7a 051c
LAB_08024e7c:
    ldr r0, DWORD_08024ea8                   @ 08024e7c 0a48
    ldr r3, DWORD_08024eac                   @ 08024e7e 0b4b
    adds r0,r0,r3    @ 08024e80 c018
    movs r1,#0x7    @ 08024e82 0721
    ldrb r0,[r0,#0x0]                        @ 08024e84 0078
    ands r1,r0    @ 08024e86 0140
    cmp r1,#0x1                              @ 08024e88 0129
    beq LAB_08024ed0                         @ 08024e8a 21d0
    cmp r1,#0x2                              @ 08024e8c 0229
    beq LAB_08024ec8                         @ 08024e8e 1bd0
    cmp r1,#0x3                              @ 08024e90 0329
    beq LAB_08024ec0                         @ 08024e92 15d0
    cmp r1,#0x4                              @ 08024e94 0429
    beq LAB_08024eb8                         @ 08024e96 0fd0
    ldr r4, DWORD_08024eb0                   @ 08024e98 054c
    cmp r1,#0x5                              @ 08024e9a 0529
    bne LAB_08024ed2                         @ 08024e9c 19d1
    ldr r0, DWORD_08024eb4                   @ 08024e9e 0548
    adds r4,r4,r0    @ 08024ea0 2418
    b LAB_08024ed2                           @ 08024ea2 16e0
DWORD_08024ea4:
    .word  0x09dc9ad6                     @ 08024ea4 d69adc09
DWORD_08024ea8:
    .word  0x02000000                     @ 08024ea8 00000002
DWORD_08024eac:
    .word  0x00006c2c                     @ 08024eac 2c6c0000
DWORD_08024eb0:
    .word  0x09dbea28                     @ 08024eb0 28eadb09
DWORD_08024eb4:
    .word  0x0003ab4a                     @ 08024eb4 4aab0300
LAB_08024eb8:
    ldr r4, DWORD_08024ebc                   @ 08024eb8 004c
    b LAB_08024ed2                           @ 08024eba 0ae0
DWORD_08024ebc:
    .word  0x09ded974                     @ 08024ebc 74d9de09
LAB_08024ec0:
    ldr r4, DWORD_08024ec4                   @ 08024ec0 004c
    b LAB_08024ed2                           @ 08024ec2 06e0
DWORD_08024ec4:
    .word  0x09de1488                     @ 08024ec4 8814de09
LAB_08024ec8:
    ldr r4, DWORD_08024ecc                   @ 08024ec8 004c
    b LAB_08024ed2                           @ 08024eca 02e0
DWORD_08024ecc:
    .word  0x09dd51a2                     @ 08024ecc a251dd09
LAB_08024ed0:
    ldr r4, DWORD_08024f14                   @ 08024ed0 104c
LAB_08024ed2:
    adds r0,r5,#0x0    @ 08024ed2 281c
    movs r1,#0x64    @ 08024ed4 6421
    bl __divsi3                              @ 08024ed6 e9f095fb
    adds r1,r0,#0x0    @ 08024eda 011c
    adds r0,r4,#0x0    @ 08024edc 201c
    bl render_card_stat_with_number_alt      @ 08024ede 06f0d3fe
LAB_08024ee2:
    movs r0,#0xf    @ 08024ee2 0f20
    bl get_card_data_bit_by_index            @ 08024ee4 6ff0c6ff
    cmp r0,#0x0                              @ 08024ee8 0028
    ble LAB_08024f54                         @ 08024eea 33dd
    ldr r0, DWORD_08024f18                   @ 08024eec 0a48
    ldr r1, DWORD_08024f1c                   @ 08024eee 0b49
    adds r0,r0,r1    @ 08024ef0 4018
    movs r1,#0x7    @ 08024ef2 0721
    ldrb r0,[r0,#0x0]                        @ 08024ef4 0078
    ands r1,r0    @ 08024ef6 0140
    cmp r1,#0x1                              @ 08024ef8 0129
    beq LAB_08024f40                         @ 08024efa 21d0
    cmp r1,#0x2                              @ 08024efc 0229
    beq LAB_08024f38                         @ 08024efe 1bd0
    cmp r1,#0x3                              @ 08024f00 0329
    beq LAB_08024f30                         @ 08024f02 15d0
    cmp r1,#0x4                              @ 08024f04 0429
    beq LAB_08024f28                         @ 08024f06 0fd0
    ldr r4, DWORD_08024f20                   @ 08024f08 054c
    cmp r1,#0x5                              @ 08024f0a 0529
    bne LAB_08024f42                         @ 08024f0c 19d1
    ldr r2, DWORD_08024f24                   @ 08024f0e 054a
    adds r4,r4,r2    @ 08024f10 a418
    b LAB_08024f42                           @ 08024f12 16e0
DWORD_08024f14:
    .word  0x09dc9ae4                     @ 08024f14 e49adc09
DWORD_08024f18:
    .word  0x02000000                     @ 08024f18 00000002
DWORD_08024f1c:
    .word  0x00006c2c                     @ 08024f1c 2c6c0000
DWORD_08024f20:
    .word  0x09dbeab2                     @ 08024f20 b2eadb09
DWORD_08024f24:
    .word  0x0003ab4e                     @ 08024f24 4eab0300
LAB_08024f28:
    ldr r4, DWORD_08024f2c                   @ 08024f28 004c
    b LAB_08024f42                           @ 08024f2a 0ae0
DWORD_08024f2c:
    .word  0x09deda10                     @ 08024f2c 10dade09
LAB_08024f30:
    ldr r4, DWORD_08024f34                   @ 08024f30 004c
    b LAB_08024f42                           @ 08024f32 06e0
DWORD_08024f34:
    .word  0x09de151e                     @ 08024f34 1e15de09
LAB_08024f38:
    ldr r4, DWORD_08024f3c                   @ 08024f38 004c
    b LAB_08024f42                           @ 08024f3a 02e0
DWORD_08024f3c:
    .word  0x09dd523c                     @ 08024f3c 3c52dd09
LAB_08024f40:
    ldr r4, DWORD_08024f88                   @ 08024f40 114c
LAB_08024f42:
    movs r0,#0xf    @ 08024f42 0f20
    bl get_card_data_bit_by_index            @ 08024f44 6ff096ff
    lsls r1,r0,#0x2    @ 08024f48 8100
    adds r1,r1,r0    @ 08024f4a 0918
    lsls r1,r1,#0x4    @ 08024f4c 0901
    adds r0,r4,#0x0    @ 08024f4e 201c
    bl render_card_stat_with_number_alt      @ 08024f50 06f09afe
LAB_08024f54:
    movs r0,#0x18    @ 08024f54 1820
    bl get_card_data_bit_by_index            @ 08024f56 6ff08dff
    cmp r0,#0x0                              @ 08024f5a 0028
    ble LAB_08024fc8                         @ 08024f5c 34dd
    ldr r0, DWORD_08024f8c                   @ 08024f5e 0b48
    ldr r3, DWORD_08024f90                   @ 08024f60 0b4b
    adds r0,r0,r3    @ 08024f62 c018
    movs r1,#0x7    @ 08024f64 0721
    ldrb r0,[r0,#0x0]                        @ 08024f66 0078
    ands r1,r0    @ 08024f68 0140
    cmp r1,#0x1                              @ 08024f6a 0129
    beq LAB_08024fb4                         @ 08024f6c 22d0
    cmp r1,#0x2                              @ 08024f6e 0229
    beq LAB_08024fac                         @ 08024f70 1cd0
    cmp r1,#0x3                              @ 08024f72 0329
    beq LAB_08024fa4                         @ 08024f74 16d0
    cmp r1,#0x4                              @ 08024f76 0429
    beq LAB_08024f9c                         @ 08024f78 10d0
    ldr r4, DWORD_08024f94                   @ 08024f7a 064c
    cmp r1,#0x5                              @ 08024f7c 0529
    bne LAB_08024fb6                         @ 08024f7e 1ad1
    ldr r0, DWORD_08024f98                   @ 08024f80 0548
    adds r4,r4,r0    @ 08024f82 2418
    b LAB_08024fb6                           @ 08024f84 17e0
    .zero  0x2
DWORD_08024f88:
    .word  0x09dc9b70                     @ 08024f88 709bdc09
DWORD_08024f8c:
    .word  0x02000000                     @ 08024f8c 00000002
DWORD_08024f90:
    .word  0x00006c2c                     @ 08024f90 2c6c0000
DWORD_08024f94:
    .word  0x09dbe9d8                     @ 08024f94 d8e9db09
DWORD_08024f98:
    .word  0x0003ab48                     @ 08024f98 48ab0300
LAB_08024f9c:
    ldr r4, DWORD_08024fa0                   @ 08024f9c 004c
    b LAB_08024fb6                           @ 08024f9e 0ae0
DWORD_08024fa0:
    .word  0x09ded914                     @ 08024fa0 14d9de09
LAB_08024fa4:
    ldr r4, DWORD_08024fa8                   @ 08024fa4 004c
    b LAB_08024fb6                           @ 08024fa6 06e0
DWORD_08024fa8:
    .word  0x09de142a                     @ 08024fa8 2a14de09
LAB_08024fac:
    ldr r4, DWORD_08024fb0                   @ 08024fac 004c
    b LAB_08024fb6                           @ 08024fae 02e0
DWORD_08024fb0:
    .word  0x09dd514e                     @ 08024fb0 4e51dd09
LAB_08024fb4:
    ldr r4, DWORD_08024ffc                   @ 08024fb4 114c
LAB_08024fb6:
    movs r0,#0x18    @ 08024fb6 1820
    bl get_card_data_bit_by_index            @ 08024fb8 6ff05cff
    lsls r1,r0,#0x2    @ 08024fbc 8100
    adds r1,r1,r0    @ 08024fbe 0918
    lsls r1,r1,#0x4    @ 08024fc0 0901
    adds r0,r4,#0x0    @ 08024fc2 201c
    bl render_card_stat_with_number_alt      @ 08024fc4 06f060fe
LAB_08024fc8:
    movs r0,#0x23    @ 08024fc8 2320
    bl get_card_data_bit_by_index            @ 08024fca 6ff053ff
    cmp r0,#0x0                              @ 08024fce 0028
    ble LAB_0802503a                         @ 08024fd0 33dd
    ldr r0, DWORD_08025000                   @ 08024fd2 0b48
    ldr r1, DWORD_08025004                   @ 08024fd4 0b49
    adds r0,r0,r1    @ 08024fd6 4018
    movs r1,#0x7    @ 08024fd8 0721
    ldrb r0,[r0,#0x0]                        @ 08024fda 0078
    ands r1,r0    @ 08024fdc 0140
    cmp r1,#0x1                              @ 08024fde 0129
    beq LAB_08025028                         @ 08024fe0 22d0
    cmp r1,#0x2                              @ 08024fe2 0229
    beq LAB_08025020                         @ 08024fe4 1cd0
    cmp r1,#0x3                              @ 08024fe6 0329
    beq LAB_08025018                         @ 08024fe8 16d0
    cmp r1,#0x4                              @ 08024fea 0429
    beq LAB_08025010                         @ 08024fec 10d0
    ldr r4, DWORD_08025008                   @ 08024fee 064c
    cmp r1,#0x5                              @ 08024ff0 0529
    bne LAB_0802502a                         @ 08024ff2 1ad1
    ldr r2, DWORD_0802500c                   @ 08024ff4 054a
    adds r4,r4,r2    @ 08024ff6 a418
    b LAB_0802502a                           @ 08024ff8 17e0
    .zero  0x2
DWORD_08024ffc:
    .word  0x09dc9a9c                     @ 08024ffc 9c9adc09
DWORD_08025000:
    .word  0x02000000                     @ 08025000 00000002
DWORD_08025004:
    .word  0x00006c2c                     @ 08025004 2c6c0000
DWORD_08025008:
    .word  0x09dbe9b4                     @ 08025008 b4e9db09
DWORD_0802500c:
    .word  0x0003ab34                     @ 0802500c 34ab0300
LAB_08025010:
    ldr r4, DWORD_08025014                   @ 08025010 004c
    b LAB_0802502a                           @ 08025012 0ae0
DWORD_08025014:
    .word  0x09ded8e0                     @ 08025014 e0d8de09
LAB_08025018:
    ldr r4, DWORD_0802501c                   @ 08025018 004c
    b LAB_0802502a                           @ 0802501a 06e0
DWORD_0802501c:
    .word  0x09de13f4                     @ 0802501c f413de09
LAB_08025020:
    ldr r4, DWORD_08025024                   @ 08025020 004c
    b LAB_0802502a                           @ 08025022 02e0
DWORD_08025024:
    .word  0x09dd511c                     @ 08025024 1c51dd09
LAB_08025028:
    ldr r4, DWORD_0802506c                   @ 08025028 104c
LAB_0802502a:
    movs r0,#0x23    @ 0802502a 2320
    bl get_card_data_bit_by_index            @ 0802502c 6ff022ff
    movs r1,#0x96    @ 08025030 9621
    muls r1,r0    @ 08025032 4143
    adds r0,r4,#0x0    @ 08025034 201c
    bl render_card_stat_with_number_alt      @ 08025036 06f027fe
LAB_0802503a:
    movs r0,#0x24    @ 0802503a 2420
    bl get_card_data_bit_by_index            @ 0802503c 6ff01aff
    cmp r0,#0x0                              @ 08025040 0028
    ble LAB_080250b0                         @ 08025042 35dd
    ldr r0, DWORD_08025070                   @ 08025044 0a48
    ldr r3, DWORD_08025074                   @ 08025046 0b4b
    adds r0,r0,r3    @ 08025048 c018
    movs r1,#0x7    @ 0802504a 0721
    ldrb r0,[r0,#0x0]                        @ 0802504c 0078
    ands r1,r0    @ 0802504e 0140
    cmp r1,#0x1                              @ 08025050 0129
    beq LAB_08025098                         @ 08025052 21d0
    cmp r1,#0x2                              @ 08025054 0229
    beq LAB_08025090                         @ 08025056 1bd0
    cmp r1,#0x3                              @ 08025058 0329
    beq LAB_08025088                         @ 0802505a 15d0
    cmp r1,#0x4                              @ 0802505c 0429
    beq LAB_08025080                         @ 0802505e 0fd0
    ldr r4, DWORD_08025078                   @ 08025060 054c
    cmp r1,#0x5                              @ 08025062 0529
    bne LAB_0802509a                         @ 08025064 19d1
    ldr r0, DWORD_0802507c                   @ 08025066 0548
    adds r4,r4,r0    @ 08025068 2418
    b LAB_0802509a                           @ 0802506a 16e0
DWORD_0802506c:
    .word  0x09dc9a74                     @ 0802506c 749adc09
DWORD_08025070:
    .word  0x02000000                     @ 08025070 00000002
DWORD_08025074:
    .word  0x00006c2c                     @ 08025074 2c6c0000
DWORD_08025078:
    .word  0x09dbe9c6                     @ 08025078 c6e9db09
DWORD_0802507c:
    .word  0x0003ab3e                     @ 0802507c 3eab0300
LAB_08025080:
    ldr r4, DWORD_08025084                   @ 08025080 004c
    b LAB_0802509a                           @ 08025082 0ae0
DWORD_08025084:
    .word  0x09ded8fa                     @ 08025084 fad8de09
LAB_08025088:
    ldr r4, DWORD_0802508c                   @ 08025088 004c
    b LAB_0802509a                           @ 0802508a 06e0
DWORD_0802508c:
    .word  0x09de140e                     @ 0802508c 0e14de09
LAB_08025090:
    ldr r4, DWORD_08025094                   @ 08025090 004c
    b LAB_0802509a                           @ 08025092 02e0
DWORD_08025094:
    .word  0x09dd5136                     @ 08025094 3651dd09
LAB_08025098:
    ldr r4, DWORD_080250e4                   @ 08025098 124c
LAB_0802509a:
    movs r0,#0x24    @ 0802509a 2420
    bl get_card_data_bit_by_index            @ 0802509c 6ff0eafe
    lsls r2,r0,#0x2    @ 080250a0 8200
    adds r2,r2,r0    @ 080250a2 1218
    lsls r1,r2,#0x4    @ 080250a4 1101
    subs r1,r1,r2    @ 080250a6 891a
    lsls r1,r1,#0x2    @ 080250a8 8900
    adds r0,r4,#0x0    @ 080250aa 201c
    bl render_card_stat_with_number_alt      @ 080250ac 06f0ecfd
LAB_080250b0:
    movs r0,#0x19    @ 080250b0 1920
    bl get_card_data_bit_by_index            @ 080250b2 6ff0dffe
    cmp r0,#0x0                              @ 080250b6 0028
    bne LAB_08025118                         @ 080250b8 2ed1
    ldr r0, DWORD_080250e8                   @ 080250ba 0b48
    ldr r1, DWORD_080250ec                   @ 080250bc 0b49
    adds r0,r0,r1    @ 080250be 4018
    movs r1,#0x7    @ 080250c0 0721
    ldrb r0,[r0,#0x0]                        @ 080250c2 0078
    ands r1,r0    @ 080250c4 0140
    cmp r1,#0x1                              @ 080250c6 0129
    beq LAB_08025110                         @ 080250c8 22d0
    cmp r1,#0x2                              @ 080250ca 0229
    beq LAB_08025108                         @ 080250cc 1cd0
    cmp r1,#0x3                              @ 080250ce 0329
    beq LAB_08025100                         @ 080250d0 16d0
    cmp r1,#0x4                              @ 080250d2 0429
    beq LAB_080250f8                         @ 080250d4 10d0
    ldr r0, DWORD_080250f0                   @ 080250d6 0648
    cmp r1,#0x5                              @ 080250d8 0529
    bne LAB_08025112                         @ 080250da 1ad1
    ldr r2, DWORD_080250f4                   @ 080250dc 054a
    adds r0,r0,r2    @ 080250de 8018
    b LAB_08025112                           @ 080250e0 17e0
    .zero  0x2
DWORD_080250e4:
    .word  0x09dc9a88                     @ 080250e4 889adc09
DWORD_080250e8:
    .word  0x02000000                     @ 080250e8 00000002
DWORD_080250ec:
    .word  0x00006c2c                     @ 080250ec 2c6c0000
DWORD_080250f0:
    .word  0x09dbe9ea                     @ 080250f0 eae9db09
DWORD_080250f4:
    .word  0x0003ab52                     @ 080250f4 52ab0300
LAB_080250f8:
    ldr r0, DWORD_080250fc                   @ 080250f8 0048
    b LAB_08025112                           @ 080250fa 0ae0
DWORD_080250fc:
    .word  0x09ded92e                     @ 080250fc 2ed9de09
LAB_08025100:
    ldr r0, DWORD_08025104                   @ 08025100 0048
    b LAB_08025112                           @ 08025102 06e0
DWORD_08025104:
    .word  0x09de1448                     @ 08025104 4814de09
LAB_08025108:
    ldr r0, DWORD_0802510c                   @ 08025108 0048
    b LAB_08025112                           @ 0802510a 02e0
DWORD_0802510c:
    .word  0x09dd5166                     @ 0802510c 6651dd09
LAB_08025110:
    ldr r0, DWORD_0802514c                   @ 08025110 0e48
LAB_08025112:
    movs r1,#0xc8    @ 08025112 c821
    bl render_card_stat_with_number_alt      @ 08025114 06f0b8fd
LAB_08025118:
    movs r0,#0x1f    @ 08025118 1f20
    bl get_card_data_bit_by_index            @ 0802511a 6ff0abfe
    cmp r0,#0x0                              @ 0802511e 0028
    ble LAB_08025194                         @ 08025120 38dd
    ldr r0, DWORD_08025150                   @ 08025122 0b48
    ldr r3, DWORD_08025154                   @ 08025124 0b4b
    adds r0,r0,r3    @ 08025126 c018
    movs r1,#0x7    @ 08025128 0721
    ldrb r0,[r0,#0x0]                        @ 0802512a 0078
    ands r1,r0    @ 0802512c 0140
    cmp r1,#0x1                              @ 0802512e 0129
    beq LAB_08025178                         @ 08025130 22d0
    cmp r1,#0x2                              @ 08025132 0229
    beq LAB_08025170                         @ 08025134 1cd0
    cmp r1,#0x3                              @ 08025136 0329
    beq LAB_08025168                         @ 08025138 16d0
    cmp r1,#0x4                              @ 0802513a 0429
    beq LAB_08025160                         @ 0802513c 10d0
    ldr r4, DWORD_08025158                   @ 0802513e 064c
    cmp r1,#0x5                              @ 08025140 0529
    bne LAB_0802517a                         @ 08025142 1ad1
    ldr r0, DWORD_0802515c                   @ 08025144 0548
    adds r4,r4,r0    @ 08025146 2418
    b LAB_0802517a                           @ 08025148 17e0
    .zero  0x2
DWORD_0802514c:
    .word  0x09dc9ab2                     @ 0802514c b29adc09
DWORD_08025150:
    .word  0x02000000                     @ 08025150 00000002
DWORD_08025154:
    .word  0x00006c2c                     @ 08025154 2c6c0000
DWORD_08025158:
    .word  0x09dbe954                     @ 08025158 54e9db09
DWORD_0802515c:
    .word  0x0003ab34                     @ 0802515c 34ab0300
LAB_08025160:
    ldr r4, DWORD_08025164                   @ 08025160 004c
    b LAB_0802517a                           @ 08025162 0ae0
DWORD_08025164:
    .word  0x09ded87a                     @ 08025164 7ad8de09
LAB_08025168:
    ldr r4, DWORD_0802516c                   @ 08025168 004c
    b LAB_0802517a                           @ 0802516a 06e0
DWORD_0802516c:
    .word  0x09de1394                     @ 0802516c 9413de09
LAB_08025170:
    ldr r4, DWORD_08025174                   @ 08025170 004c
    b LAB_0802517a                           @ 08025172 02e0
DWORD_08025174:
    .word  0x09dd50c4                     @ 08025174 c450dd09
LAB_08025178:
    ldr r4, DWORD_08025190                   @ 08025178 054c
LAB_0802517a:
    movs r0,#0x1f    @ 0802517a 1f20
    bl get_card_data_bit_by_index            @ 0802517c 6ff07afe
    lsls r1,r0,#0x2    @ 08025180 8100
    adds r1,r1,r0    @ 08025182 0918
    lsls r1,r1,#0x2    @ 08025184 8900
    adds r0,r4,#0x0    @ 08025186 201c
    bl render_card_stat_with_number_alt      @ 08025188 06f07efd
    b LAB_080251ec                           @ 0802518c 2ee0
    .zero  0x2
DWORD_08025190:
    .word  0x09dc9a28                     @ 08025190 289adc09
LAB_08025194:
    ldr r0, DWORD_080251bc                   @ 08025194 0948
    ldr r1, DWORD_080251c0                   @ 08025196 0a49
    adds r0,r0,r1    @ 08025198 4018
    movs r1,#0x7    @ 0802519a 0721
    ldrb r0,[r0,#0x0]                        @ 0802519c 0078
    ands r1,r0    @ 0802519e 0140
    cmp r1,#0x1                              @ 080251a0 0129
    beq LAB_080251e4                         @ 080251a2 1fd0
    cmp r1,#0x2                              @ 080251a4 0229
    beq LAB_080251dc                         @ 080251a6 19d0
    cmp r1,#0x3                              @ 080251a8 0329
    beq LAB_080251d4                         @ 080251aa 13d0
    cmp r1,#0x4                              @ 080251ac 0429
    beq LAB_080251cc                         @ 080251ae 0dd0
    ldr r0, DWORD_080251c4                   @ 080251b0 0448
    cmp r1,#0x5                              @ 080251b2 0529
    bne LAB_080251e6                         @ 080251b4 17d1
    ldr r2, DWORD_080251c8                   @ 080251b6 044a
    adds r0,r0,r2    @ 080251b8 8018
    b LAB_080251e6                           @ 080251ba 14e0
DWORD_080251bc:
    .word  0x02000000                     @ 080251bc 00000002
DWORD_080251c0:
    .word  0x00006c2c                     @ 080251c0 2c6c0000
DWORD_080251c4:
    .word  0x09dbe982                     @ 080251c4 82e9db09
DWORD_080251c8:
    .word  0x0003ab30                     @ 080251c8 30ab0300
LAB_080251cc:
    ldr r0, DWORD_080251d0                   @ 080251cc 0048
    b LAB_080251e6                           @ 080251ce 0ae0
DWORD_080251d0:
    .word  0x09ded8aa                     @ 080251d0 aad8de09
LAB_080251d4:
    ldr r0, DWORD_080251d8                   @ 080251d4 0048
    b LAB_080251e6                           @ 080251d6 06e0
DWORD_080251d8:
    .word  0x09de13bc                     @ 080251d8 bc13de09
LAB_080251dc:
    ldr r0, DWORD_080251e0                   @ 080251dc 0048
    b LAB_080251e6                           @ 080251de 02e0
DWORD_080251e0:
    .word  0x09dd50e8                     @ 080251e0 e850dd09
LAB_080251e4:
    ldr r0, DWORD_08025220                   @ 080251e4 0e48
LAB_080251e6:
    movs r1,#0xc8    @ 080251e6 c821
    bl render_card_stat_with_number_alt      @ 080251e8 06f04efd
LAB_080251ec:
    movs r0,#0x21    @ 080251ec 2120
    bl get_card_data_bit_by_index            @ 080251ee 6ff041fe
    cmp r0,#0x0                              @ 080251f2 0028
    ble LAB_08025268                         @ 080251f4 38dd
    ldr r0, DWORD_08025224                   @ 080251f6 0b48
    ldr r3, DWORD_08025228                   @ 080251f8 0b4b
    adds r0,r0,r3    @ 080251fa c018
    movs r1,#0x7    @ 080251fc 0721
    ldrb r0,[r0,#0x0]                        @ 080251fe 0078
    ands r1,r0    @ 08025200 0140
    cmp r1,#0x1                              @ 08025202 0129
    beq LAB_0802524c                         @ 08025204 22d0
    cmp r1,#0x2                              @ 08025206 0229
    beq LAB_08025244                         @ 08025208 1cd0
    cmp r1,#0x3                              @ 0802520a 0329
    beq LAB_0802523c                         @ 0802520c 16d0
    cmp r1,#0x4                              @ 0802520e 0429
    beq LAB_08025234                         @ 08025210 10d0
    ldr r4, DWORD_0802522c                   @ 08025212 064c
    cmp r1,#0x5                              @ 08025214 0529
    bne LAB_0802524e                         @ 08025216 1ad1
    ldr r0, DWORD_08025230                   @ 08025218 0548
    adds r4,r4,r0    @ 0802521a 2418
    b LAB_0802524e                           @ 0802521c 17e0
    .zero  0x2
DWORD_08025220:
    .word  0x09dc9a4a                     @ 08025220 4a9adc09
DWORD_08025224:
    .word  0x02000000                     @ 08025224 00000002
DWORD_08025228:
    .word  0x00006c2c                     @ 08025228 2c6c0000
DWORD_0802522c:
    .word  0x09dbe96c                     @ 0802522c 6ce9db09
DWORD_08025230:
    .word  0x0003ab30                     @ 08025230 30ab0300
LAB_08025234:
    ldr r4, DWORD_08025238                   @ 08025234 004c
    b LAB_0802524e                           @ 08025236 0ae0
DWORD_08025238:
    .word  0x09ded890                     @ 08025238 90d8de09
LAB_0802523c:
    ldr r4, DWORD_08025240                   @ 0802523c 004c
    b LAB_0802524e                           @ 0802523e 06e0
DWORD_08025240:
    .word  0x09de13a8                     @ 08025240 a813de09
LAB_08025244:
    ldr r4, DWORD_08025248                   @ 08025244 004c
    b LAB_0802524e                           @ 08025246 02e0
DWORD_08025248:
    .word  0x09dd50d6                     @ 08025248 d650dd09
LAB_0802524c:
    ldr r4, DWORD_08025264                   @ 0802524c 054c
LAB_0802524e:
    movs r0,#0x21    @ 0802524e 2120
    bl get_card_data_bit_by_index            @ 08025250 6ff010fe
    lsls r1,r0,#0x4    @ 08025254 0101
    subs r1,r1,r0    @ 08025256 091a
    lsls r1,r1,#0x1    @ 08025258 4900
    adds r0,r4,#0x0    @ 0802525a 201c
    bl render_card_stat_with_number_alt      @ 0802525c 06f014fd
    b LAB_080252c0                           @ 08025260 2ee0
    .zero  0x2
DWORD_08025264:
    .word  0x09dc9a3a                     @ 08025264 3a9adc09
LAB_08025268:
    ldr r0, DWORD_08025290                   @ 08025268 0948
    ldr r1, DWORD_08025294                   @ 0802526a 0a49
    adds r0,r0,r1    @ 0802526c 4018
    movs r1,#0x7    @ 0802526e 0721
    ldrb r0,[r0,#0x0]                        @ 08025270 0078
    ands r1,r0    @ 08025272 0140
    cmp r1,#0x1                              @ 08025274 0129
    beq LAB_080252b8                         @ 08025276 1fd0
    cmp r1,#0x2                              @ 08025278 0229
    beq LAB_080252b0                         @ 0802527a 19d0
    cmp r1,#0x3                              @ 0802527c 0329
    beq LAB_080252a8                         @ 0802527e 13d0
    cmp r1,#0x4                              @ 08025280 0429
    beq LAB_080252a0                         @ 08025282 0dd0
    ldr r0, DWORD_08025298                   @ 08025284 0448
    cmp r1,#0x5                              @ 08025286 0529
    bne LAB_080252ba                         @ 08025288 17d1
    ldr r2, DWORD_0802529c                   @ 0802528a 044a
    adds r0,r0,r2    @ 0802528c 8018
    b LAB_080252ba                           @ 0802528e 14e0
DWORD_08025290:
    .word  0x02000000                     @ 08025290 00000002
DWORD_08025294:
    .word  0x00006c2c                     @ 08025294 2c6c0000
DWORD_08025298:
    .word  0x09dbe99c                     @ 08025298 9ce9db09
DWORD_0802529c:
    .word  0x0003ab30                     @ 0802529c 30ab0300
LAB_080252a0:
    ldr r0, DWORD_080252a4                   @ 080252a0 0048
    b LAB_080252ba                           @ 080252a2 0ae0
DWORD_080252a4:
    .word  0x09ded8c4                     @ 080252a4 c4d8de09
LAB_080252a8:
    ldr r0, DWORD_080252ac                   @ 080252a8 0048
    b LAB_080252ba                           @ 080252aa 06e0
DWORD_080252ac:
    .word  0x09de13d8                     @ 080252ac d813de09
LAB_080252b0:
    ldr r0, DWORD_080252b4                   @ 080252b0 0048
    b LAB_080252ba                           @ 080252b2 02e0
DWORD_080252b4:
    .word  0x09dd5102                     @ 080252b4 0251dd09
LAB_080252b8:
    ldr r0, DWORD_08025308                   @ 080252b8 1348
LAB_080252ba:
    movs r1,#0x64    @ 080252ba 6421
    bl render_card_stat_with_number_alt      @ 080252bc 06f0e4fc
LAB_080252c0:
    ldr r1, DWORD_0802530c                   @ 080252c0 1249
    movs r3,#0x89    @ 080252c2 8923
    lsls r3,r3,#0x2    @ 080252c4 9b00
    adds r0,r1,r3    @ 080252c6 c818
    ldr r2,[r0,#0x0]                         @ 080252c8 0268
    cmp r2,#0x1                              @ 080252ca 012a
    bne LAB_08025348                         @ 080252cc 3cd1
    ldr r0, DWORD_08025310                   @ 080252ce 1048
    ldr r3, DWORD_08025314                   @ 080252d0 104b
    adds r0,r0,r3    @ 080252d2 c018
    ldr r1,[r1,#0x4]                         @ 080252d4 4968
    eors r1,r2    @ 080252d6 5140
    ldr r0,[r0,#0x0]                         @ 080252d8 0068
    cmp r0,r1                                @ 080252da 8842
    bne LAB_08025348                         @ 080252dc 34d1
    ldr r0, DWORD_08025318                   @ 080252de 0e48
    ldr r1, DWORD_0802531c                   @ 080252e0 0e49
    adds r0,r0,r1    @ 080252e2 4018
    movs r1,#0x7    @ 080252e4 0721
    ldrb r0,[r0,#0x0]                        @ 080252e6 0078
    ands r1,r0    @ 080252e8 0140
    cmp r1,#0x1                              @ 080252ea 0129
    beq LAB_08025340                         @ 080252ec 28d0
    cmp r1,#0x2                              @ 080252ee 0229
    beq LAB_08025338                         @ 080252f0 22d0
    cmp r1,#0x3                              @ 080252f2 0329
    beq LAB_08025330                         @ 080252f4 1cd0
    cmp r1,#0x4                              @ 080252f6 0429
    beq LAB_08025328                         @ 080252f8 16d0
    ldr r0, DWORD_08025320                   @ 080252fa 0948
    cmp r1,#0x5                              @ 080252fc 0529
    bne LAB_08025342                         @ 080252fe 20d1
    ldr r2, DWORD_08025324                   @ 08025300 084a
    adds r0,r0,r2    @ 08025302 8018
    b LAB_08025342                           @ 08025304 1de0
    .zero  0x2
DWORD_08025308:
    .word  0x09dc9a60                     @ 08025308 609adc09
DWORD_0802530c:
    .word  0x0201e2a0                     @ 0802530c a0e20102
DWORD_08025310:
    .word  gP1LifePoints                  @ 08025310 e0c40102
DWORD_08025314:
    .word  0x00001ce8                     @ 08025314 e81c0000
DWORD_08025318:
    .word  0x02000000                     @ 08025318 00000002
DWORD_0802531c:
    .word  0x00006c2c                     @ 0802531c 2c6c0000
DWORD_08025320:
    .word  0x09dbe89c                     @ 08025320 9ce8db09
DWORD_08025324:
    .word  0x0003ab4e                     @ 08025324 4eab0300
LAB_08025328:
    ldr r0, DWORD_0802532c                   @ 08025328 0048
    b LAB_08025342                           @ 0802532a 0ae0
DWORD_0802532c:
    .word  0x09ded7b2                     @ 0802532c b2d7de09
LAB_08025330:
    ldr r0, DWORD_08025334                   @ 08025330 0048
    b LAB_08025342                           @ 08025332 06e0
DWORD_08025334:
    .word  0x09de12da                     @ 08025334 da12de09
LAB_08025338:
    ldr r0, DWORD_0802533c                   @ 08025338 0048
    b LAB_08025342                           @ 0802533a 02e0
DWORD_0802533c:
    .word  0x09dd500c                     @ 0802533c 0c50dd09
LAB_08025340:
    ldr r0, DWORD_08025368                   @ 08025340 0948
LAB_08025342:
    movs r1,#0xc8    @ 08025342 c821
    bl render_card_stat_with_number_alt      @ 08025344 06f0a0fc
LAB_08025348:
    ldr r0, DWORD_0802536c                   @ 08025348 0848
    movs r3,#0x89    @ 0802534a 8923
    lsls r3,r3,#0x2    @ 0802534c 9b00
    adds r0,r0,r3    @ 0802534e c018
    ldr r0,[r0,#0x0]                         @ 08025350 0068
    cmp r0,#0x2                              @ 08025352 0228
    bne LAB_0802535a                         @ 08025354 01d1
    bl render_game_text_with_font_type_a     @ 08025356 00f03bfc
LAB_0802535a:
    cmp r0,#0x2                              @ 0802535a 0228
    bgt LAB_08025370                         @ 0802535c 08dc
    cmp r0,#0x1                              @ 0802535e 0128
    beq LAB_0802537c                         @ 08025360 0cd0
    bl SUB_08025c8a                          @ 08025362 00f092fc
    movs r0,r0    @ 08025366 0000
DWORD_08025368:
    .word  0x09dc9988                     @ 08025368 8899dc09
DWORD_0802536c:
    .word  0x0201e2a0                     @ 0802536c a0e20102
LAB_08025370:
    cmp r0,#0x3                              @ 08025370 0328
    bne LAB_08025378                         @ 08025372 01d1
    bl render_game_text_with_font_type_b     @ 08025374 00f05cfc
LAB_08025378:
    bl SUB_08025c8a                          @ 08025378 00f087fc
LAB_0802537c:
    ldr r0, DWORD_080253c0                   @ 0802537c 1048
    ldrb r0,[r0,#0x2]                        @ 0802537e 8078
    lsls r0,r0,#0x1b    @ 08025380 c006
    lsrs r0,r0,#0x1b    @ 08025382 c00e
    movs r1,#0x5    @ 08025384 0521
    bl __udivsi3                             @ 08025386 e9f029fa
    lsls r0,r0,#0x10    @ 0802538a 0004
    lsrs r0,r0,#0x10    @ 0802538c 000c
    adds r1,r0,#0x1    @ 0802538e 411c
    cmp r1,#0x5                              @ 08025390 0529
    ble LAB_08025396                         @ 08025392 00dd
    movs r1,#0x2    @ 08025394 0221
LAB_08025396:
    ldr r0, DWORD_080253c4                   @ 08025396 0b48
    ldr r2, DWORD_080253c8                   @ 08025398 0b4a
    adds r0,r0,r2    @ 0802539a 8018
    movs r2,#0x7    @ 0802539c 0722
    ldrb r0,[r0,#0x0]                        @ 0802539e 0078
    ands r2,r0    @ 080253a0 0240
    cmp r2,#0x1                              @ 080253a2 012a
    beq LAB_080253ec                         @ 080253a4 22d0
    cmp r2,#0x2                              @ 080253a6 022a
    beq LAB_080253e4                         @ 080253a8 1cd0
    cmp r2,#0x3                              @ 080253aa 032a
    beq LAB_080253dc                         @ 080253ac 16d0
    cmp r2,#0x4                              @ 080253ae 042a
    beq LAB_080253d4                         @ 080253b0 10d0
    ldr r3, DWORD_080253cc                   @ 080253b2 064b
    cmp r2,#0x5                              @ 080253b4 052a
    bne LAB_080253ee                         @ 080253b6 1ad1
    ldr r0, DWORD_080253d0                   @ 080253b8 0548
    adds r3,r3,r0    @ 080253ba 1b18
    b LAB_080253ee                           @ 080253bc 17e0
    .zero  0x2
DWORD_080253c0:
    .word  0x02023360                     @ 080253c0 60330202
DWORD_080253c4:
    .word  0x02000000                     @ 080253c4 00000002
DWORD_080253c8:
    .word  0x00006c2c                     @ 080253c8 2c6c0000
DWORD_080253cc:
    .word  0x09dbe7e6                     @ 080253cc e6e7db09
DWORD_080253d0:
    .word  0x0003ab0e                     @ 080253d0 0eab0300
LAB_080253d4:
    ldr r3, DWORD_080253d8                   @ 080253d4 004b
    b LAB_080253ee                           @ 080253d6 0ae0
DWORD_080253d8:
    .word  0x09ded68a                     @ 080253d8 8ad6de09
LAB_080253dc:
    ldr r3, DWORD_080253e0                   @ 080253dc 004b
    b LAB_080253ee                           @ 080253de 06e0
DWORD_080253e0:
    .word  0x09de11dc                     @ 080253e0 dc11de09
LAB_080253e4:
    ldr r3, DWORD_080253e8                   @ 080253e4 004b
    b LAB_080253ee                           @ 080253e6 02e0
DWORD_080253e8:
    .word  0x09dd4f2c                     @ 080253e8 2c4fdd09
LAB_080253ec:
    ldr r3, DWORD_0802542c                   @ 080253ec 0f4b
LAB_080253ee:
    movs r0,#0x32    @ 080253ee 3220
    muls r1,r0    @ 080253f0 4143
    adds r0,r3,#0x0    @ 080253f2 181c
    bl render_card_stat_with_number_alt      @ 080253f4 06f048fc
    movs r0,#0x36    @ 080253f8 3620
    bl get_card_data_bit_by_index            @ 080253fa 6ff03bfd
    cmp r0,#0x0                              @ 080253fe 0028
    bne LAB_08025460                         @ 08025400 2ed1
    ldr r0, DWORD_08025430                   @ 08025402 0b48
    ldr r1, DWORD_08025434                   @ 08025404 0b49
    adds r0,r0,r1    @ 08025406 4018
    movs r1,#0x7    @ 08025408 0721
    ldrb r0,[r0,#0x0]                        @ 0802540a 0078
    ands r1,r0    @ 0802540c 0140
    cmp r1,#0x1                              @ 0802540e 0129
    beq LAB_08025458                         @ 08025410 22d0
    cmp r1,#0x2                              @ 08025412 0229
    beq LAB_08025450                         @ 08025414 1cd0
    cmp r1,#0x3                              @ 08025416 0329
    beq LAB_08025448                         @ 08025418 16d0
    cmp r1,#0x4                              @ 0802541a 0429
    beq LAB_08025440                         @ 0802541c 10d0
    ldr r0, DWORD_08025438                   @ 0802541e 0648
    cmp r1,#0x5                              @ 08025420 0529
    bne LAB_0802545a                         @ 08025422 1ad1
    ldr r2, DWORD_0802543c                   @ 08025424 054a
    adds r0,r0,r2    @ 08025426 8018
    b LAB_0802545a                           @ 08025428 17e0
    .zero  0x2
DWORD_0802542c:
    .word  0x09dc9886                     @ 0802542c 8698dc09
DWORD_08025430:
    .word  0x02000000                     @ 08025430 00000002
DWORD_08025434:
    .word  0x00006c2c                     @ 08025434 2c6c0000
DWORD_08025438:
    .word  0x09dbe8e2                     @ 08025438 e2e8db09
DWORD_0802543c:
    .word  0x0003ab4a                     @ 0802543c 4aab0300
LAB_08025440:
    ldr r0, DWORD_08025444                   @ 08025440 0048
    b LAB_0802545a                           @ 08025442 0ae0
DWORD_08025444:
    .word  0x09ded7fc                     @ 08025444 fcd7de09
LAB_08025448:
    ldr r0, DWORD_0802544c                   @ 08025448 0048
    b LAB_0802545a                           @ 0802544a 06e0
DWORD_0802544c:
    .word  0x09de1322                     @ 0802544c 2213de09
LAB_08025450:
    ldr r0, DWORD_08025454                   @ 08025450 0048
    b LAB_0802545a                           @ 08025452 02e0
DWORD_08025454:
    .word  0x09dd5058                     @ 08025454 5850dd09
LAB_08025458:
    ldr r0, DWORD_08025494                   @ 08025458 0e48
LAB_0802545a:
    movs r1,#0x64    @ 0802545a 6421
    bl render_card_stat_with_number_alt      @ 0802545c 06f014fc
LAB_08025460:
    movs r0,#0x37    @ 08025460 3720
    bl get_card_data_bit_by_index            @ 08025462 6ff007fd
    cmp r0,#0x0                              @ 08025466 0028
    beq LAB_080254c8                         @ 08025468 2ed0
    ldr r0, DWORD_08025498                   @ 0802546a 0b48
    ldr r3, DWORD_0802549c                   @ 0802546c 0b4b
    adds r0,r0,r3    @ 0802546e c018
    movs r1,#0x7    @ 08025470 0721
    ldrb r0,[r0,#0x0]                        @ 08025472 0078
    ands r1,r0    @ 08025474 0140
    cmp r1,#0x1                              @ 08025476 0129
    beq LAB_080254c0                         @ 08025478 22d0
    cmp r1,#0x2                              @ 0802547a 0229
    beq LAB_080254b8                         @ 0802547c 1cd0
    cmp r1,#0x3                              @ 0802547e 0329
    beq LAB_080254b0                         @ 08025480 16d0
    cmp r1,#0x4                              @ 08025482 0429
    beq LAB_080254a8                         @ 08025484 10d0
    ldr r0, DWORD_080254a0                   @ 08025486 0648
    cmp r1,#0x5                              @ 08025488 0529
    bne LAB_080254c2                         @ 0802548a 1ad1
    ldr r1, DWORD_080254a4                   @ 0802548c 0549
    adds r0,r0,r1    @ 0802548e 4018
    b LAB_080254c2                           @ 08025490 17e0
    .zero  0x2
DWORD_08025494:
    .word  0x09dc99cc                     @ 08025494 cc99dc09
DWORD_08025498:
    .word  0x02000000                     @ 08025498 00000002
DWORD_0802549c:
    .word  0x00006c2c                     @ 0802549c 2c6c0000
DWORD_080254a0:
    .word  0x09dbea68                     @ 080254a0 68eadb09
DWORD_080254a4:
    .word  0x0003ab4a                     @ 080254a4 4aab0300
LAB_080254a8:
    ldr r0, DWORD_080254ac                   @ 080254a8 0048
    b LAB_080254c2                           @ 080254aa 0ae0
DWORD_080254ac:
    .word  0x09ded9c0                     @ 080254ac c0d9de09
LAB_080254b0:
    ldr r0, DWORD_080254b4                   @ 080254b0 0048
    b LAB_080254c2                           @ 080254b2 06e0
DWORD_080254b4:
    .word  0x09de14d4                     @ 080254b4 d414de09
LAB_080254b8:
    ldr r0, DWORD_080254bc                   @ 080254b8 0048
    b LAB_080254c2                           @ 080254ba 02e0
DWORD_080254bc:
    .word  0x09dd51ee                     @ 080254bc ee51dd09
LAB_080254c0:
    ldr r0, DWORD_080254fc                   @ 080254c0 0e48
LAB_080254c2:
    movs r1,#0x64    @ 080254c2 6421
    bl render_card_stat_with_number_alt      @ 080254c4 06f0e0fb
LAB_080254c8:
    movs r0,#0x3f    @ 080254c8 3f20
    bl get_card_data_bit_by_index            @ 080254ca 6ff0d3fc
    cmp r0,#0x0                              @ 080254ce 0028
    beq LAB_08025530                         @ 080254d0 2ed0
    ldr r0, DWORD_08025500                   @ 080254d2 0b48
    ldr r2, DWORD_08025504                   @ 080254d4 0b4a
    adds r0,r0,r2    @ 080254d6 8018
    movs r1,#0x7    @ 080254d8 0721
    ldrb r0,[r0,#0x0]                        @ 080254da 0078
    ands r1,r0    @ 080254dc 0140
    cmp r1,#0x1                              @ 080254de 0129
    beq LAB_08025528                         @ 080254e0 22d0
    cmp r1,#0x2                              @ 080254e2 0229
    beq LAB_08025520                         @ 080254e4 1cd0
    cmp r1,#0x3                              @ 080254e6 0329
    beq LAB_08025518                         @ 080254e8 16d0
    cmp r1,#0x4                              @ 080254ea 0429
    beq LAB_08025510                         @ 080254ec 10d0
    ldr r0, DWORD_08025508                   @ 080254ee 0648
    cmp r1,#0x5                              @ 080254f0 0529
    bne LAB_0802552a                         @ 080254f2 1ad1
    ldr r3, DWORD_0802550c                   @ 080254f4 054b
    adds r0,r0,r3    @ 080254f6 c018
    b LAB_0802552a                           @ 080254f8 17e0
    .zero  0x2
DWORD_080254fc:
    .word  0x09dc9b28                     @ 080254fc 289bdc09
DWORD_08025500:
    .word  0x02000000                     @ 08025500 00000002
DWORD_08025504:
    .word  0x00006c2c                     @ 08025504 2c6c0000
DWORD_08025508:
    .word  0x09dbe86c                     @ 08025508 6ce8db09
DWORD_0802550c:
    .word  0x0003ab32                     @ 0802550c 32ab0300
LAB_08025510:
    ldr r0, DWORD_08025514                   @ 08025510 0048
    b LAB_0802552a                           @ 08025512 0ae0
DWORD_08025514:
    .word  0x09ded760                     @ 08025514 60d7de09
LAB_08025518:
    ldr r0, DWORD_0802551c                   @ 08025518 0048
    b LAB_0802552a                           @ 0802551a 06e0
DWORD_0802551c:
    .word  0x09de128c                     @ 0802551c 8c12de09
LAB_08025520:
    ldr r0, DWORD_08025524                   @ 08025520 0048
    b LAB_0802552a                           @ 08025522 02e0
DWORD_08025524:
    .word  0x09dd4fca                     @ 08025524 ca4fdd09
LAB_08025528:
    ldr r0, DWORD_08025564                   @ 08025528 0e48
LAB_0802552a:
    movs r1,#0xa    @ 0802552a 0a21
    bl render_card_stat_with_number_alt      @ 0802552c 06f0acfb
LAB_08025530:
    movs r0,#0x38    @ 08025530 3820
    bl get_card_data_bit_by_index            @ 08025532 6ff09ffc
    cmp r0,#0x0                              @ 08025536 0028
    beq LAB_08025598                         @ 08025538 2ed0
    ldr r0, DWORD_08025568                   @ 0802553a 0b48
    ldr r1, DWORD_0802556c                   @ 0802553c 0b49
    adds r0,r0,r1    @ 0802553e 4018
    movs r1,#0x7    @ 08025540 0721
    ldrb r0,[r0,#0x0]                        @ 08025542 0078
    ands r1,r0    @ 08025544 0140
    cmp r1,#0x1                              @ 08025546 0129
    beq LAB_08025590                         @ 08025548 22d0
    cmp r1,#0x2                              @ 0802554a 0229
    beq LAB_08025588                         @ 0802554c 1cd0
    cmp r1,#0x3                              @ 0802554e 0329
    beq LAB_08025580                         @ 08025550 16d0
    cmp r1,#0x4                              @ 08025552 0429
    beq LAB_08025578                         @ 08025554 10d0
    ldr r0, DWORD_08025570                   @ 08025556 0648
    cmp r1,#0x5                              @ 08025558 0529
    bne LAB_08025592                         @ 0802555a 1ad1
    ldr r2, DWORD_08025574                   @ 0802555c 054a
    adds r0,r0,r2    @ 0802555e 8018
    b LAB_08025592                           @ 08025560 17e0
    .zero  0x2
DWORD_08025564:
    .word  0x09dc9942                     @ 08025564 4299dc09
DWORD_08025568:
    .word  0x02000000                     @ 08025568 00000002
DWORD_0802556c:
    .word  0x00006c2c                     @ 0802556c 2c6c0000
DWORD_08025570:
    .word  0x09dbe88a                     @ 08025570 8ae8db09
DWORD_08025574:
    .word  0x0003ab46                     @ 08025574 46ab0300
LAB_08025578:
    ldr r0, DWORD_0802557c                   @ 08025578 0048
    b LAB_08025592                           @ 0802557a 0ae0
DWORD_0802557c:
    .word  0x09ded796                     @ 0802557c 96d7de09
LAB_08025580:
    ldr r0, DWORD_08025584                   @ 08025580 0048
    b LAB_08025592                           @ 08025582 06e0
DWORD_08025584:
    .word  0x09de12bc                     @ 08025584 bc12de09
LAB_08025588:
    ldr r0, DWORD_0802558c                   @ 08025588 0048
    b LAB_08025592                           @ 0802558a 02e0
DWORD_0802558c:
    .word  0x09dd4ff6                     @ 0802558c f64fdd09
LAB_08025590:
    ldr r0, DWORD_080255b4                   @ 08025590 0848
LAB_08025592:
    movs r1,#0x1e    @ 08025592 1e21
    bl render_card_stat_with_number_alt      @ 08025594 06f078fb
LAB_08025598:
    ldr r0, DWORD_080255b8                   @ 08025598 0748
    ldr r1,[r0,#0x0]                         @ 0802559a 0168
    ldr r0, DWORD_080255bc                   @ 0802559c 0748
    cmp r1,r0                                @ 0802559e 8142
    bne LAB_080255a4                         @ 080255a0 00d1
    b LAB_080256b8                           @ 080255a2 89e0
LAB_080255a4:
    cmp r1,r0                                @ 080255a4 8142
    bgt LAB_080255c0                         @ 080255a6 0bdc
    cmp r1,#0x1                              @ 080255a8 0129
    bge LAB_080255ae                         @ 080255aa 00da
    b LAB_0802576c                           @ 080255ac dee0
LAB_080255ae:
    cmp r1,#0x63                             @ 080255ae 6329
    ble LAB_08025658                         @ 080255b0 52dd
    b LAB_080255f4                           @ 080255b2 1fe0
DWORD_080255b4:
    .word  0x09dc9972                     @ 080255b4 7299dc09
DWORD_080255b8:
    .word  gP1LifePoints                  @ 080255b8 e0c40102
DWORD_080255bc:
    .word  0x0000023d                     @ 080255bc 3d020000
LAB_080255c0:
    ldr r0, DWORD_080255e0                   @ 080255c0 0748
    cmp r1,r0                                @ 080255c2 8142
    bne LAB_080255c8                         @ 080255c4 00d1
    b LAB_08025710                           @ 080255c6 a3e0
LAB_080255c8:
    cmp r1,r0                                @ 080255c8 8142
    ble LAB_080255ec                         @ 080255ca 0fdd
    ldr r0, DWORD_080255e4                   @ 080255cc 0548
    cmp r1,r0                                @ 080255ce 8142
    bne LAB_080255d4                         @ 080255d0 00d1
    b LAB_08025710                           @ 080255d2 9de0
LAB_080255d4:
    ldr r0, DWORD_080255e8                   @ 080255d4 0448
    cmp r1,r0                                @ 080255d6 8142
    bne LAB_080255dc                         @ 080255d8 00d1
    b LAB_08025710                           @ 080255da 99e0
LAB_080255dc:
    b LAB_0802576c                           @ 080255dc c6e0
    .zero  0x2
DWORD_080255e0:
    .word  0x00001662                     @ 080255e0 62160000
DWORD_080255e4:
    .word  0x0000dfd4                     @ 080255e4 d4df0000
DWORD_080255e8:
    .word  0x0008be48                     @ 080255e8 48be0800
LAB_080255ec:
    ldr r0, DWORD_0802561c                   @ 080255ec 0b48
    cmp r1,r0                                @ 080255ee 8142
    ble LAB_080255f4                         @ 080255f0 00dd
    b LAB_0802576c                           @ 080255f2 bbe0
LAB_080255f4:
    ldr r0, DWORD_08025620                   @ 080255f4 0a48
    ldr r3, DWORD_08025624                   @ 080255f6 0b4b
    adds r0,r0,r3    @ 080255f8 c018
    movs r1,#0x7    @ 080255fa 0721
    ldrb r0,[r0,#0x0]                        @ 080255fc 0078
    ands r1,r0    @ 080255fe 0140
    cmp r1,#0x1                              @ 08025600 0129
    beq LAB_08025648                         @ 08025602 21d0
    cmp r1,#0x2                              @ 08025604 0229
    beq LAB_08025640                         @ 08025606 1bd0
    cmp r1,#0x3                              @ 08025608 0329
    beq LAB_08025638                         @ 0802560a 15d0
    cmp r1,#0x4                              @ 0802560c 0429
    beq LAB_08025630                         @ 0802560e 0fd0
    ldr r0, DWORD_08025628                   @ 08025610 0548
    cmp r1,#0x5                              @ 08025612 0529
    bne LAB_0802564a                         @ 08025614 19d1
    ldr r1, DWORD_0802562c                   @ 08025616 0549
    adds r0,r0,r1    @ 08025618 4018
    b LAB_0802564a                           @ 0802561a 16e0
DWORD_0802561c:
    .word  0x000003e7                     @ 0802561c e7030000
DWORD_08025620:
    .word  0x02000000                     @ 08025620 00000002
DWORD_08025624:
    .word  0x00006c2c                     @ 08025624 2c6c0000
DWORD_08025628:
    .word  0x09dbe8b4                     @ 08025628 b4e8db09
DWORD_0802562c:
    .word  0x0003ab52                     @ 0802562c 52ab0300
LAB_08025630:
    ldr r0, DWORD_08025634                   @ 08025630 0048
    b LAB_0802564a                           @ 08025632 0ae0
DWORD_08025634:
    .word  0x09ded7d0                     @ 08025634 d0d7de09
LAB_08025638:
    ldr r0, DWORD_0802563c                   @ 08025638 0048
    b LAB_0802564a                           @ 0802563a 06e0
DWORD_0802563c:
    .word  0x09de12f6                     @ 0802563c f612de09
LAB_08025640:
    ldr r0, DWORD_08025644                   @ 08025640 0048
    b LAB_0802564a                           @ 08025642 02e0
DWORD_08025644:
    .word  0x09dd5026                     @ 08025644 2650dd09
LAB_08025648:
    ldr r0, DWORD_08025654                   @ 08025648 0248
LAB_0802564a:
    movs r1,#0xc8    @ 0802564a c821
    bl render_card_stat_with_number_alt      @ 0802564c 06f01cfb
    b LAB_0802576c                           @ 08025650 8ce0
    .zero  0x2
DWORD_08025654:
    .word  0x09dc99a6                     @ 08025654 a699dc09
LAB_08025658:
    ldr r0, DWORD_08025680                   @ 08025658 0948
    ldr r2, DWORD_08025684                   @ 0802565a 0a4a
    adds r0,r0,r2    @ 0802565c 8018
    movs r1,#0x7    @ 0802565e 0721
    ldrb r0,[r0,#0x0]                        @ 08025660 0078
    ands r1,r0    @ 08025662 0140
    cmp r1,#0x1                              @ 08025664 0129
    beq LAB_080256a8                         @ 08025666 1fd0
    cmp r1,#0x2                              @ 08025668 0229
    beq LAB_080256a0                         @ 0802566a 19d0
    cmp r1,#0x3                              @ 0802566c 0329
    beq LAB_08025698                         @ 0802566e 13d0
    cmp r1,#0x4                              @ 08025670 0429
    beq LAB_08025690                         @ 08025672 0dd0
    ldr r0, DWORD_08025688                   @ 08025674 0448
    cmp r1,#0x5                              @ 08025676 0529
    bne LAB_080256aa                         @ 08025678 17d1
    ldr r3, DWORD_0802568c                   @ 0802567a 044b
    adds r0,r0,r3    @ 0802567c c018
    b LAB_080256aa                           @ 0802567e 14e0
DWORD_08025680:
    .word  0x02000000                     @ 08025680 00000002
DWORD_08025684:
    .word  0x00006c2c                     @ 08025684 2c6c0000
DWORD_08025688:
    .word  0x09dbe8ca                     @ 08025688 cae8db09
DWORD_0802568c:
    .word  0x0003ab4a                     @ 0802568c 4aab0300
LAB_08025690:
    ldr r0, DWORD_08025694                   @ 08025690 0048
    b LAB_080256aa                           @ 08025692 0ae0
DWORD_08025694:
    .word  0x09ded7e4                     @ 08025694 e4d7de09
LAB_08025698:
    ldr r0, DWORD_0802569c                   @ 08025698 0048
    b LAB_080256aa                           @ 0802569a 06e0
DWORD_0802569c:
    .word  0x09de130a                     @ 0802569c 0a13de09
LAB_080256a0:
    ldr r0, DWORD_080256a4                   @ 080256a0 0048
    b LAB_080256aa                           @ 080256a2 02e0
DWORD_080256a4:
    .word  0x09dd503c                     @ 080256a4 3c50dd09
LAB_080256a8:
    ldr r0, DWORD_080256b4                   @ 080256a8 0248
LAB_080256aa:
    movs r1,#0xfa    @ 080256aa fa21
    lsls r1,r1,#0x3    @ 080256ac c900
    bl render_card_stat_with_number_alt      @ 080256ae 06f0ebfa
    b LAB_0802576c                           @ 080256b2 5be0
DWORD_080256b4:
    .word  0x09dc99b4                     @ 080256b4 b499dc09
LAB_080256b8:
    ldr r0, DWORD_080256e0                   @ 080256b8 0948
    ldr r1, DWORD_080256e4                   @ 080256ba 0a49
    adds r0,r0,r1    @ 080256bc 4018
    movs r1,#0x7    @ 080256be 0721
    ldrb r0,[r0,#0x0]                        @ 080256c0 0078
    ands r1,r0    @ 080256c2 0140
    cmp r1,#0x1                              @ 080256c4 0129
    beq LAB_08025708                         @ 080256c6 1fd0
    cmp r1,#0x2                              @ 080256c8 0229
    beq LAB_08025700                         @ 080256ca 19d0
    cmp r1,#0x3                              @ 080256cc 0329
    beq LAB_080256f8                         @ 080256ce 13d0
    cmp r1,#0x4                              @ 080256d0 0429
    beq LAB_080256f0                         @ 080256d2 0dd0
    ldr r0, DWORD_080256e8                   @ 080256d4 0448
    cmp r1,#0x5                              @ 080256d6 0529
    bne LAB_0802570a                         @ 080256d8 17d1
    ldr r2, DWORD_080256ec                   @ 080256da 044a
    adds r0,r0,r2    @ 080256dc 8018
    b LAB_0802570a                           @ 080256de 14e0
DWORD_080256e0:
    .word  0x02000000                     @ 080256e0 00000002
DWORD_080256e4:
    .word  0x00006c2c                     @ 080256e4 2c6c0000
DWORD_080256e8:
    .word  0x09dbe8b4                     @ 080256e8 b4e8db09
DWORD_080256ec:
    .word  0x0003ab52                     @ 080256ec 52ab0300
LAB_080256f0:
    ldr r0, DWORD_080256f4                   @ 080256f0 0048
    b LAB_0802570a                           @ 080256f2 0ae0
DWORD_080256f4:
    .word  0x09ded7d0                     @ 080256f4 d0d7de09
LAB_080256f8:
    ldr r0, DWORD_080256fc                   @ 080256f8 0048
    b LAB_0802570a                           @ 080256fa 06e0
DWORD_080256fc:
    .word  0x09de12f6                     @ 080256fc f612de09
LAB_08025700:
    ldr r0, DWORD_08025704                   @ 08025700 0048
    b LAB_0802570a                           @ 08025702 02e0
DWORD_08025704:
    .word  0x09dd5026                     @ 08025704 2650dd09
LAB_08025708:
    ldr r0, DWORD_08025738                   @ 08025708 0b48
LAB_0802570a:
    movs r1,#0xc8    @ 0802570a c821
    bl render_card_stat_with_number_alt      @ 0802570c 06f0bcfa
LAB_08025710:
    ldr r0, DWORD_0802573c                   @ 08025710 0a48
    ldr r3, DWORD_08025740                   @ 08025712 0b4b
    adds r0,r0,r3    @ 08025714 c018
    movs r1,#0x7    @ 08025716 0721
    ldrb r0,[r0,#0x0]                        @ 08025718 0078
    ands r1,r0    @ 0802571a 0140
    cmp r1,#0x1                              @ 0802571c 0129
    beq LAB_08025764                         @ 0802571e 21d0
    cmp r1,#0x2                              @ 08025720 0229
    beq LAB_0802575c                         @ 08025722 1bd0
    cmp r1,#0x3                              @ 08025724 0329
    beq LAB_08025754                         @ 08025726 15d0
    cmp r1,#0x4                              @ 08025728 0429
    beq LAB_0802574c                         @ 0802572a 0fd0
    ldr r0, DWORD_08025744                   @ 0802572c 0548
    cmp r1,#0x5                              @ 0802572e 0529
    bne LAB_08025766                         @ 08025730 19d1
    ldr r1, DWORD_08025748                   @ 08025732 0549
    adds r0,r0,r1    @ 08025734 4018
    b LAB_08025766                           @ 08025736 16e0
DWORD_08025738:
    .word  0x09dc99a6                     @ 08025738 a699dc09
DWORD_0802573c:
    .word  0x02000000                     @ 0802573c 00000002
DWORD_08025740:
    .word  0x00006c2c                     @ 08025740 2c6c0000
DWORD_08025744:
    .word  0x09dbe910                     @ 08025744 10e9db09
DWORD_08025748:
    .word  0x0003ab40                     @ 08025748 40ab0300
LAB_0802574c:
    ldr r0, DWORD_08025750                   @ 0802574c 0048
    b LAB_08025766                           @ 0802574e 0ae0
DWORD_08025750:
    .word  0x09ded836                     @ 08025750 36d8de09
LAB_08025754:
    ldr r0, DWORD_08025758                   @ 08025754 0048
    b LAB_08025766                           @ 08025756 06e0
DWORD_08025758:
    .word  0x09de1356                     @ 08025758 5613de09
LAB_0802575c:
    ldr r0, DWORD_08025760                   @ 0802575c 0048
    b LAB_08025766                           @ 0802575e 02e0
DWORD_08025760:
    .word  0x09dd5080                     @ 08025760 8050dd09
LAB_08025764:
    ldr r0, DWORD_080257a0                   @ 08025764 0e48
LAB_08025766:
    ldr r1, DWORD_080257a4                   @ 08025766 0f49
    bl render_card_stat_with_number_alt      @ 08025768 06f08efa
LAB_0802576c:
    ldr r0, DWORD_080257a8                   @ 0802576c 0e48
    ldr r1,[r0,#0x0]                         @ 0802576e 0168
    ldr r0, DWORD_080257ac                   @ 08025770 0e48
    cmp r1,r0                                @ 08025772 8142
    ble LAB_080257e0                         @ 08025774 34dd
    ldr r0, DWORD_080257b0                   @ 08025776 0e48
    ldr r2, DWORD_080257b4                   @ 08025778 0e4a
    adds r0,r0,r2    @ 0802577a 8018
    movs r1,#0x7    @ 0802577c 0721
    ldrb r0,[r0,#0x0]                        @ 0802577e 0078
    ands r1,r0    @ 08025780 0140
    cmp r1,#0x1                              @ 08025782 0129
    beq LAB_080257d8                         @ 08025784 28d0
    cmp r1,#0x2                              @ 08025786 0229
    beq LAB_080257d0                         @ 08025788 22d0
    cmp r1,#0x3                              @ 0802578a 0329
    beq LAB_080257c8                         @ 0802578c 1cd0
    cmp r1,#0x4                              @ 0802578e 0429
    beq LAB_080257c0                         @ 08025790 16d0
    ldr r0, DWORD_080257b8                   @ 08025792 0948
    cmp r1,#0x5                              @ 08025794 0529
    bne LAB_080257da                         @ 08025796 20d1
    ldr r3, DWORD_080257bc                   @ 08025798 084b
    adds r0,r0,r3    @ 0802579a c018
    b LAB_080257da                           @ 0802579c 1de0
    .zero  0x2
DWORD_080257a0:
    .word  0x09dc99f0                     @ 080257a0 f099dc09
DWORD_080257a4:
    .word  0x0000023d                     @ 080257a4 3d020000
DWORD_080257a8:
    .word  gP1LifePoints                  @ 080257a8 e0c40102
DWORD_080257ac:
    .word  0x00004e20                     @ 080257ac 204e0000
DWORD_080257b0:
    .word  0x02000000                     @ 080257b0 00000002
DWORD_080257b4:
    .word  0x00006c2c                     @ 080257b4 2c6c0000
DWORD_080257b8:
    .word  0x09dbe8f8                     @ 080257b8 f8e8db09
DWORD_080257bc:
    .word  0x0003ab42                     @ 080257bc 42ab0300
LAB_080257c0:
    ldr r0, DWORD_080257c4                   @ 080257c0 0048
    b LAB_080257da                           @ 080257c2 0ae0
DWORD_080257c4:
    .word  0x09ded81c                     @ 080257c4 1cd8de09
LAB_080257c8:
    ldr r0, DWORD_080257cc                   @ 080257c8 0048
    b LAB_080257da                           @ 080257ca 06e0
DWORD_080257cc:
    .word  0x09de133c                     @ 080257cc 3c13de09
LAB_080257d0:
    ldr r0, DWORD_080257d4                   @ 080257d0 0048
    b LAB_080257da                           @ 080257d2 02e0
DWORD_080257d4:
    .word  0x09dd506c                     @ 080257d4 6c50dd09
LAB_080257d8:
    ldr r0, DWORD_08025814                   @ 080257d8 0e48
LAB_080257da:
    movs r1,#0xc8    @ 080257da c821
    bl render_card_stat_with_number_alt      @ 080257dc 06f054fa
LAB_080257e0:
    ldr r0, DWORD_08025818                   @ 080257e0 0d48
    ldr r0,[r0,#0x10]                        @ 080257e2 0069
    cmp r0,#0x0                              @ 080257e4 0028
    beq LAB_08025854                         @ 080257e6 35d0
    cmp r0,#0x5                              @ 080257e8 0528
    bhi LAB_080258ac                         @ 080257ea 5fd8
    ldr r0, DWORD_0802581c                   @ 080257ec 0b48
    ldr r1, DWORD_08025820                   @ 080257ee 0c49
    adds r0,r0,r1    @ 080257f0 4018
    movs r1,#0x7    @ 080257f2 0721
    ldrb r0,[r0,#0x0]                        @ 080257f4 0078
    ands r1,r0    @ 080257f6 0140
    cmp r1,#0x1                              @ 080257f8 0129
    beq LAB_08025844                         @ 080257fa 23d0
    cmp r1,#0x2                              @ 080257fc 0229
    beq LAB_0802583c                         @ 080257fe 1dd0
    cmp r1,#0x3                              @ 08025800 0329
    beq LAB_08025834                         @ 08025802 17d0
    cmp r1,#0x4                              @ 08025804 0429
    beq LAB_0802582c                         @ 08025806 11d0
    ldr r0, DWORD_08025824                   @ 08025808 0648
    cmp r1,#0x5                              @ 0802580a 0529
    bne LAB_08025846                         @ 0802580c 1bd1
    ldr r2, DWORD_08025828                   @ 0802580e 064a
    adds r0,r0,r2    @ 08025810 8018
    b LAB_08025846                           @ 08025812 18e0
DWORD_08025814:
    .word  0x09dc99dc                     @ 08025814 dc99dc09
DWORD_08025818:
    .word  gP1LifePoints                  @ 08025818 e0c40102
DWORD_0802581c:
    .word  0x02000000                     @ 0802581c 00000002
DWORD_08025820:
    .word  0x00006c2c                     @ 08025820 2c6c0000
DWORD_08025824:
    .word  0x09dbe922                     @ 08025824 22e9db09
DWORD_08025828:
    .word  0x0003ab3c                     @ 08025828 3cab0300
LAB_0802582c:
    ldr r0, DWORD_08025830                   @ 0802582c 0048
    b LAB_08025846                           @ 0802582e 0ae0
DWORD_08025830:
    .word  0x09ded844                     @ 08025830 44d8de09
LAB_08025834:
    ldr r0, DWORD_08025838                   @ 08025834 0048
    b LAB_08025846                           @ 08025836 06e0
DWORD_08025838:
    .word  0x09de1366                     @ 08025838 6613de09
LAB_0802583c:
    ldr r0, DWORD_08025840                   @ 0802583c 0048
    b LAB_08025846                           @ 0802583e 02e0
DWORD_08025840:
    .word  0x09dd508e                     @ 08025840 8e50dd09
LAB_08025844:
    ldr r0, DWORD_08025850                   @ 08025844 0248
LAB_08025846:
    movs r1,#0x96    @ 08025846 9621
    bl render_card_stat_with_number_alt      @ 08025848 06f01efa
    b LAB_080258ac                           @ 0802584c 2ee0
    .zero  0x2
DWORD_08025850:
    .word  0x09dc99fe                     @ 08025850 fe99dc09
LAB_08025854:
    ldr r0, DWORD_0802587c                   @ 08025854 0948
    ldr r3, DWORD_08025880                   @ 08025856 0a4b
    adds r0,r0,r3    @ 08025858 c018
    movs r1,#0x7    @ 0802585a 0721
    ldrb r0,[r0,#0x0]                        @ 0802585c 0078
    ands r1,r0    @ 0802585e 0140
    cmp r1,#0x1                              @ 08025860 0129
    beq LAB_080258a4                         @ 08025862 1fd0
    cmp r1,#0x2                              @ 08025864 0229
    beq LAB_0802589c                         @ 08025866 19d0
    cmp r1,#0x3                              @ 08025868 0329
    beq LAB_08025894                         @ 0802586a 13d0
    cmp r1,#0x4                              @ 0802586c 0429
    beq LAB_0802588c                         @ 0802586e 0dd0
    ldr r0, DWORD_08025884                   @ 08025870 0448
    cmp r1,#0x5                              @ 08025872 0529
    bne LAB_080258a6                         @ 08025874 17d1
    ldr r1, DWORD_08025888                   @ 08025876 0449
    adds r0,r0,r1    @ 08025878 4018
    b LAB_080258a6                           @ 0802587a 14e0
DWORD_0802587c:
    .word  0x02000000                     @ 0802587c 00000002
DWORD_08025880:
    .word  0x00006c2c                     @ 08025880 2c6c0000
DWORD_08025884:
    .word  0x09dbe93a                     @ 08025884 3ae9db09
DWORD_08025888:
    .word  0x0003ab34                     @ 08025888 34ab0300
LAB_0802588c:
    ldr r0, DWORD_08025890                   @ 0802588c 0048
    b LAB_080258a6                           @ 0802588e 0ae0
DWORD_08025890:
    .word  0x09ded85e                     @ 08025890 5ed8de09
LAB_08025894:
    ldr r0, DWORD_08025898                   @ 08025894 0048
    b LAB_080258a6                           @ 08025896 06e0
DWORD_08025898:
    .word  0x09de137a                     @ 08025898 7a13de09
LAB_0802589c:
    ldr r0, DWORD_080258a0                   @ 0802589c 0048
    b LAB_080258a6                           @ 0802589e 02e0
DWORD_080258a0:
    .word  0x09dd50a8                     @ 080258a0 a850dd09
LAB_080258a4:
    ldr r0, DWORD_080258c8                   @ 080258a4 0848
LAB_080258a6:
    ldr r1, DWORD_080258cc                   @ 080258a6 0949
    bl render_card_stat_with_number_alt      @ 080258a8 06f0eef9
LAB_080258ac:
    ldr r0, DWORD_080258d0                   @ 080258ac 0848
    movs r2,#0x8a    @ 080258ae 8a22
    lsls r2,r2,#0x2    @ 080258b0 9200
    adds r0,r0,r2    @ 080258b2 8018
    ldr r0,[r0,#0x0]                         @ 080258b4 0068
    subs r0,#0x2    @ 080258b6 0238
    cmp r0,#0x5                              @ 080258b8 0528
    bls LAB_080258be                         @ 080258ba 00d9
    b LAB_08025b20                           @ 080258bc 30e1
LAB_080258be:
    lsls r0,r0,#0x2    @ 080258be 8000
    ldr r1, DWORD_080258d4                   @ 080258c0 0449
    adds r0,r0,r1    @ 080258c2 4018
    ldr r0,[r0,#0x0]                         @ 080258c4 0068
    .hword 0x4687    @ 080258c6 8746
DWORD_080258c8:
    .word  0x09dc9a0e                     @ 080258c8 0e9adc09
DWORD_080258cc:
    .word  0x000005dc                     @ 080258cc dc050000
DWORD_080258d0:
    .word  0x0201e2a0                     @ 080258d0 a0e20102
DWORD_080258d4:
    .word  0x080258d8                     @ 080258d4 d8580208
    .word  0x080259a8                     @ 080258d8 a8590208
    .word  0x080258f0                     @ 080258dc f0580208
    .word  0x0802594c                     @ 080258e0 4c590208
    .word  0x08025ac8                     @ 080258e4 c85a0208
    .word  0x08025a68                     @ 080258e8 685a0208
    .word  0x08025a08                     @ 080258ec 085a0208
DAT_080258f0:
    ROM_INCBIN 0x258f0, 0x230
LAB_08025b20:
    movs r1,#0x0    @ 08025b20 0021
    ldr r0, DWORD_08025b3c                   @ 08025b22 0648
    ldr r3, DWORD_08025b40                   @ 08025b24 064b
    adds r0,r0,r3    @ 08025b26 c018
    ldr r0,[r0,#0x0]                         @ 08025b28 0068
    cmp r0,#0x5                              @ 08025b2a 0528
    bhi LAB_08025b6e                         @ 08025b2c 1fd8
    lsls r0,r0,#0x2    @ 08025b2e 8000
    ldr r1, PTR_PTR_08025b44                 @ 08025b30 0449
    adds r0,r0,r1    @ 08025b32 4018
    ldr r0,[r0,#0x0]                         @ 08025b34 0068
    .hword 0x4687    @ 08025b36 8746
    .byte  0x28, 0x99, 0xdc, 0x09
DWORD_08025b3c:
    .word  gP1LifePoints                  @ 08025b3c e0c40102
DWORD_08025b40:
    .word  0x00001cec                     @ 08025b40 ec1c0000
PTR_PTR_08025b44:
    .word  0x08025b48                     @ 08025b44 485b0208
PTR_DAT_08025b48:
    .word  0x08025b60                     @ 08025b48 605b0208
    .word  0x08025b60                     @ 08025b4c 605b0208
    .word  0x08025b66                     @ 08025b50 665b0208
    .word  0x08025b66                     @ 08025b54 665b0208
    .word  0x08025b6c                     @ 08025b58 6c5b0208
    .word  0x08025b6c                     @ 08025b5c 6c5b0208
DAT_08025b60:
    .byte  0xfa, 0x21, 0x49, 0x00, 0x06, 0xe0, 0x96, 0x21, 0x49, 0x00, 0x03, 0xe0, 0x64, 0x21
LAB_08025b6e:
    cmp r1,#0x0                              @ 08025b6e 0029
    bne LAB_08025b74                         @ 08025b70 00d1
    b SUB_08025c8a                           @ 08025b72 8ae0
LAB_08025b74:
    ldr r0, DWORD_08025b9c                   @ 08025b74 0948
    ldr r2, DWORD_08025ba0                   @ 08025b76 0a4a
    adds r0,r0,r2    @ 08025b78 8018
    movs r2,#0x7    @ 08025b7a 0722
    ldrb r0,[r0,#0x0]                        @ 08025b7c 0078
    ands r2,r0    @ 08025b7e 0240
    cmp r2,#0x1                              @ 08025b80 012a
    beq LAB_08025bc4                         @ 08025b82 1fd0
    cmp r2,#0x2                              @ 08025b84 022a
    beq LAB_08025bbc                         @ 08025b86 19d0
    cmp r2,#0x3                              @ 08025b88 032a
    beq LAB_08025bb4                         @ 08025b8a 13d0
    cmp r2,#0x4                              @ 08025b8c 042a
    beq LAB_08025bac                         @ 08025b8e 0dd0
    ldr r0, DWORD_08025ba4                   @ 08025b90 0448
    cmp r2,#0x5                              @ 08025b92 052a
    bne LAB_08025bc6                         @ 08025b94 17d1
    ldr r3, DWORD_08025ba8                   @ 08025b96 044b
    adds r0,r0,r3    @ 08025b98 c018
    b LAB_08025bc6                           @ 08025b9a 14e0
DWORD_08025b9c:
    .word  0x02000000                     @ 08025b9c 00000002
DWORD_08025ba0:
    .word  0x00006c2c                     @ 08025ba0 2c6c0000
DWORD_08025ba4:
    .word  0x09dbe878                     @ 08025ba4 78e8db09
DWORD_08025ba8:
    .word  0x0003ab3e                     @ 08025ba8 3eab0300
LAB_08025bac:
    ldr r0, DWORD_08025bb0                   @ 08025bac 0048
    b LAB_08025bc6                           @ 08025bae 0ae0
DWORD_08025bb0:
    .word  0x09ded77c                     @ 08025bb0 7cd7de09
LAB_08025bb4:
    ldr r0, DWORD_08025bb8                   @ 08025bb4 0048
    b LAB_08025bc6                           @ 08025bb6 06e0
DWORD_08025bb8:
    .word  0x09de12a4                     @ 08025bb8 a412de09
LAB_08025bbc:
    ldr r0, DWORD_08025bc0                   @ 08025bbc 0048
    b LAB_08025bc6                           @ 08025bbe 02e0
DWORD_08025bc0:
    .word  0x09dd4fe0                     @ 08025bc0 e04fdd09
LAB_08025bc4:
    ldr r0, DWORD_08025bcc                   @ 08025bc4 0148
LAB_08025bc6:
    bl render_card_stat_with_number_alt      @ 08025bc6 06f05ff8
    b SUB_08025c8a                           @ 08025bca 5ee0
DWORD_08025bcc:
    .word  0x09dc995e                     @ 08025bcc 5e99dc09

@ Selects a ROM font data pointer r0 based on gPrng+0x6c2c bits[2:0] (font_type, [1..5]),
@ then calls render_game_string_with_number (FUN_0802b940) with fixed args (r1=3, r2=10)
@ to render a game string. font_type==5 adds offset 0x3ab84 to ROM base 0x09dc01ac;
@ font_type 4/3/2/1 each have independent ROM font pointers. Called only by
@ render_card_stats_to_line_buf as the A-string (r2=10) render sub-path.
@ 
@ Constants:
@ - gPrng+0x6c2c = font_type field (0x02006c2c)
@ - 0x09dc01ac = font_type 5 base (ROM offset)
@ - 0x3ab84 = font_type 5 additional offset
@ - r2=10 (0xa) = digit_value parameter for render_game_string_with_number
render_game_text_with_font_type_a:
    ldr r0, DWORD_08025bf8                   @ 08025bd0 0948
    ldr r1, DWORD_08025bfc                   @ 08025bd2 0a49
    adds r0,r0,r1    @ 08025bd4 4018
    movs r1,#0x7    @ 08025bd6 0721
    ldrb r0,[r0,#0x0]                        @ 08025bd8 0078
    ands r1,r0    @ 08025bda 0140
    cmp r1,#0x1                              @ 08025bdc 0129
    beq LAB_08025c20                         @ 08025bde 1fd0
    cmp r1,#0x2                              @ 08025be0 0229
    beq LAB_08025c18                         @ 08025be2 19d0
    cmp r1,#0x3                              @ 08025be4 0329
    beq LAB_08025c10                         @ 08025be6 13d0
    cmp r1,#0x4                              @ 08025be8 0429
    beq LAB_08025c08                         @ 08025bea 0dd0
    ldr r0, DWORD_08025c00                   @ 08025bec 0448
    cmp r1,#0x5                              @ 08025bee 0529
    bne LAB_08025c22                         @ 08025bf0 17d1
    ldr r2, DWORD_08025c04                   @ 08025bf2 044a
    adds r0,r0,r2    @ 08025bf4 8018
    b LAB_08025c22                           @ 08025bf6 14e0
DWORD_08025bf8:
    .word  0x02000000                     @ 08025bf8 00000002
DWORD_08025bfc:
    .word  0x00006c2c                     @ 08025bfc 2c6c0000
DWORD_08025c00:
    .word  0x09dc01ac                     @ 08025c00 ac01dc09
DWORD_08025c04:
    .word  0x0003ab84                     @ 08025c04 84ab0300
LAB_08025c08:
    ldr r0, DWORD_08025c0c                   @ 08025c08 0048
    b LAB_08025c22                           @ 08025c0a 0ae0
DWORD_08025c0c:
    .word  0x09def168                     @ 08025c0c 68f1de09
LAB_08025c10:
    ldr r0, DWORD_08025c14                   @ 08025c10 0048
    b LAB_08025c22                           @ 08025c12 06e0
DWORD_08025c14:
    .word  0x09de2cd8                     @ 08025c14 d82cde09
LAB_08025c18:
    ldr r0, DWORD_08025c1c                   @ 08025c18 0048
    b LAB_08025c22                           @ 08025c1a 02e0
DWORD_08025c1c:
    .word  0x09dd694c                     @ 08025c1c 4c69dd09
LAB_08025c20:
    ldr r0, DWORD_08025c2c                   @ 08025c20 0248
LAB_08025c22:
    movs r1,#0x3    @ 08025c22 0321
    movs r2,#0xa    @ 08025c24 0a22
    bl render_game_string_with_number        @ 08025c26 05f08bfe
    b SUB_08025c8a                           @ 08025c2a 2ee0
DWORD_08025c2c:
    .word  0x09dcaf86                     @ 08025c2c 86afdc09

@ Symmetric sibling of render_game_text_with_font_type_a (FUN_08025bd0): only differences are
@ (1) different font pointer constants (0x09dc01b2 vs 0x09dc01ac); (2) r2=2 (vs r2=10)
@ passed to render_game_string_with_number (FUN_0802b940). Also selects font by
@ gPrng+0x6c2c bits[2:0], renders with fixed r1=3. Called only by render_card_stats_to_line_buf
@ as the B-string (r2=2) render sub-path.
@ 
@ Constants:
@ - gPrng+0x6c2c = font_type field (0x02006c2c)
@ - 0x09dc01b2 = font_type 5/default ROM base for sibling B (+6 offset from A)
@ - 0x3ab86 = font_type 5 additional offset (+2 from A's 0x3ab84)
@ - r2=2 = mode parameter for render_game_string_with_number
render_game_text_with_font_type_b:
    ldr r0, DWORD_08025c58                   @ 08025c30 0948
    ldr r3, DWORD_08025c5c                   @ 08025c32 0a4b
    adds r0,r0,r3    @ 08025c34 c018
    movs r1,#0x7    @ 08025c36 0721
    ldrb r0,[r0,#0x0]                        @ 08025c38 0078
    ands r1,r0    @ 08025c3a 0140
    cmp r1,#0x1                              @ 08025c3c 0129
    beq LAB_08025c80                         @ 08025c3e 1fd0
    cmp r1,#0x2                              @ 08025c40 0229
    beq LAB_08025c78                         @ 08025c42 19d0
    cmp r1,#0x3                              @ 08025c44 0329
    beq LAB_08025c70                         @ 08025c46 13d0
    cmp r1,#0x4                              @ 08025c48 0429
    beq LAB_08025c68                         @ 08025c4a 0dd0
    ldr r0, DWORD_08025c60                   @ 08025c4c 0448
    cmp r1,#0x5                              @ 08025c4e 0529
    bne LAB_08025c82                         @ 08025c50 17d1
    ldr r1, DWORD_08025c64                   @ 08025c52 0449
    adds r0,r0,r1    @ 08025c54 4018
    b LAB_08025c82                           @ 08025c56 14e0
DWORD_08025c58:
    .word  0x02000000                     @ 08025c58 00000002
DWORD_08025c5c:
    .word  0x00006c2c                     @ 08025c5c 2c6c0000
DWORD_08025c60:
    .word  0x09dc01b2                     @ 08025c60 b201dc09
DWORD_08025c64:
    .word  0x0003ab86                     @ 08025c64 86ab0300
LAB_08025c68:
    ldr r0, DWORD_08025c6c                   @ 08025c68 0048
    b LAB_08025c82                           @ 08025c6a 0ae0
DWORD_08025c6c:
    .word  0x09def172                     @ 08025c6c 72f1de09
LAB_08025c70:
    ldr r0, DWORD_08025c74                   @ 08025c70 0048
    b LAB_08025c82                           @ 08025c72 06e0
DWORD_08025c74:
    .word  0x09de2ce0                     @ 08025c74 e02cde09
LAB_08025c78:
    ldr r0, DWORD_08025c7c                   @ 08025c78 0048
    b LAB_08025c82                           @ 08025c7a 02e0
DWORD_08025c7c:
    .word  0x09dd6956                     @ 08025c7c 5669dd09
LAB_08025c80:
    ldr r0, DWORD_08025c90                   @ 08025c80 0348
LAB_08025c82:
    movs r1,#0x3    @ 08025c82 0321
    movs r2,#0x2    @ 08025c84 0222
    bl render_game_string_with_number        @ 08025c86 05f05bfe
SUB_08025c8a:
    pop {r4,r5}                              @ 08025c8a 30bc
    pop {r0}                                 @ 08025c8c 01bc
    bx r0                                    @ 08025c8e 0047
DWORD_08025c90:
    .word  0x09dcaf8c                     @ 08025c90 8cafdc09

@ Root dispatch function for the campaign scene. Called indirectly via gMenuState+0x234 function pointer (written by enter_campaign_page). Each frame: reads gPrng+0x202 bits[13:6] as step_index [0..34]. If step_index > 0x22 -> bl exit_campaign_scene_with_next_handler. Otherwise multiplies by 4 and jumps into 35-entry function pointer table at 0x08025ccc. Table entries 8/9/13..19 all point to exit_campaign_scene_with_next_handler (placeholder steps).
@ 
@ Constants:
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6] [0..0xff]
@ - step_max = 0x22 (34, 35 entries total)
@ - dispatch_table = 0x08025ccc (35 * 4 = 0x8c bytes)
@ - step_8/9/13..19 = 0x08027c78 (exit_campaign_scene_with_next_handler placeholder)
campaign_scene_handler:
    push {r4,r5,r6,r7,lr}                    @ 08025c94 f0b5
    .hword 0x4657    @ 08025c96 5746
    .hword 0x464e    @ 08025c98 4e46
    .hword 0x4645    @ 08025c9a 4546
    push {r5,r6,r7}                          @ 08025c9c e0b4
    sub sp,#0x14                             @ 08025c9e 85b0
    ldr r0, PTR_gPrng_08025cc0               @ 08025ca0 0748
    ldr r2, DAT_08025cc4                     @ 08025ca2 084a
    adds r1,r0,r2    @ 08025ca4 8118
    ldrh r1,[r1,#0x0]                        @ 08025ca6 0988
    lsls r1,r1,#0x12    @ 08025ca8 8904
    lsrs r1,r1,#0x18    @ 08025caa 090e
    .hword 0x4681    @ 08025cac 8146
    cmp r1,#0x22                             @ 08025cae 2229
    bls LAB_08025cb6                         @ 08025cb0 01d9
    bl exit_campaign_scene_with_next_handler @ 08025cb2 01f0e1ff
LAB_08025cb6:
    lsls r0,r1,#0x2    @ 08025cb6 8800
    ldr r1, DAT_08025cc8                     @ 08025cb8 0349
    adds r0,r0,r1    @ 08025cba 4018
    ldr r0,[r0,#0x0]                         @ 08025cbc 0068
    .hword 0x4687    @ 08025cbe 8746
PTR_gPrng_08025cc0:
    .word  gPrng                          @ 08025cc0 40000003
DAT_08025cc4:
    .word  0x00000202                     @ 08025cc4 02020000
DAT_08025cc8:
    .word  0x08025ccc                     @ 08025cc8 cc5c0208
PTR_run_campaign_step0_field_vram_init_08025ccc:
    .word  0x08025d58                     @ 08025ccc 585d0208
    .word  0x08025ec0                     @ 08025cd0 c05e0208
    .word  0x08025f14                     @ 08025cd4 145f0208
    .word  0x080266bc                     @ 08025cd8 bc660208
    .word  0x080266d0                     @ 08025cdc d0660208
    .word  0x08026748                     @ 08025ce0 48670208
    .word  0x080267ca                     @ 08025ce4 ca670208
    .word  0x08026858                     @ 08025ce8 58680208
    .word  0x08027c78                     @ 08025cec 787c0208
    .word  0x08027c78                     @ 08025cf0 787c0208
    .word  0x08026a2c                     @ 08025cf4 2c6a0208
    .word  0x08026af2                     @ 08025cf8 f26a0208
    .word  0x08026bc8                     @ 08025cfc c86b0208
    .word  0x08027c78                     @ 08025d00 787c0208
    .word  0x08027c78                     @ 08025d04 787c0208
    .word  0x08027c78                     @ 08025d08 787c0208
    .word  0x08027c78                     @ 08025d0c 787c0208
    .word  0x08027c78                     @ 08025d10 787c0208
    .word  0x08027c78                     @ 08025d14 787c0208
    .word  0x08027c78                     @ 08025d18 787c0208
    .word  0x08026c88                     @ 08025d1c 886c0208
    .word  0x08026e68                     @ 08025d20 686e0208
    .word  0x08026e9c                     @ 08025d24 9c6e0208
    .word  0x08026fe4                     @ 08025d28 e46f0208
    .word  0x0802727c                     @ 08025d2c 7c720208
    .word  0x080274f4                     @ 08025d30 f4740208
    .word  0x0802752c                     @ 08025d34 2c750208
    .word  0x080276dc                     @ 08025d38 dc760208
    .word  0x08027714                     @ 08025d3c 14770208
    .word  0x0802774c                     @ 08025d40 4c770208
    .word  0x080277a4                     @ 08025d44 a4770208
    .word  0x08027834                     @ 08025d48 34780208
    .word  0x08027888                     @ 08025d4c 88780208
    .word  0x080278c0                     @ 08025d50 c0780208
    .word  0x08027a0c                     @ 08025d54 0c7a0208

@ campaign_scene_handler dispatch table index 0. Trigger: gPrng+0x202 bits[13:6] == 0x00. Sequence: (1) bl build_field_slot_bitmask; (2) clears/sets multiple byte fields in scene_ctx (0x02023360): +0x2 bit5, +0x3 bits[4:0], +0x4 bits[4:0] := 0x5, +0x5 bit4, +0x8 halfword high byte; (3) bl init_duel_field_icon_and_bg_vram; (4) branches on [0x02006c2c] bits[2:0] = deck_type [0..5] to select tile data pointer r3; (5) same deck_type switch selects BG palette data; (6) bl draw_decimal_with_offset twice (x=0x40/0x80, y=0x210/0x21c); (7) advances gPrng+0x202 bits[13:6] by 1 then tail-calls SUB_08027c22. Does not return normally.
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - deck_type_reg = [0x02006c2c] bits[2:0] [0..5]
@ - slot_mode_bits = 0x5 (OR into scene_ctx+0x4)
@ - x_win_label = 0x40, y_win_label = 0x84*4 = 0x210
@ - x_lp_label = 0x80, y_lp_label = 0x87*4 = 0x21c
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6], mask = 0xffffc03f
run_campaign_step0_field_vram_init:
    bl build_field_slot_bitmask              @ 08025d58 fef7ccfd
    ldr r2, DWORD_08025dd0                   @ 08025d5c 1c4a
    movs r1,#0x20    @ 08025d5e 2021
    rsbs r1,r1,#0    @ 08025d60 4942
    adds r0,r1,#0x0    @ 08025d62 081c
    ldrb r3,[r2,#0x2]                        @ 08025d64 9378
    ands r0,r3    @ 08025d66 1840
    strb r0,[r2,#0x2]                        @ 08025d68 9070
    movs r3,#0x1f    @ 08025d6a 1f23
    adds r0,r3,#0x0    @ 08025d6c 181c
    ldrb r4,[r2,#0x3]                        @ 08025d6e d478
    ands r0,r4    @ 08025d70 2040
    strb r0,[r2,#0x3]                        @ 08025d72 d070
    ldrb r5,[r2,#0x4]                        @ 08025d74 1579
    ands r1,r5    @ 08025d76 2940
    movs r0,#0x5    @ 08025d78 0520
    orrs r1,r0    @ 08025d7a 0143
    ldr r0, DWORD_08025dd4                   @ 08025d7c 1548
    ldrh r6,[r2,#0x8]                        @ 08025d7e 1689
    ands r0,r6    @ 08025d80 3040
    strh r0,[r2,#0x8]                        @ 08025d82 1081
    ands r1,r3    @ 08025d84 1940
    strb r1,[r2,#0x4]                        @ 08025d86 1171
    movs r0,#0x10    @ 08025d88 1020
    rsbs r0,r0,#0    @ 08025d8a 4042
    ldrb r1,[r2,#0x5]                        @ 08025d8c 5179
    ands r0,r1    @ 08025d8e 0840
    strb r0,[r2,#0x5]                        @ 08025d90 5071
    movs r0,#0x3    @ 08025d92 0320
    rsbs r0,r0,#0    @ 08025d94 4042
    ldrb r3,[r2,#0x8]                        @ 08025d96 137a
    ands r0,r3    @ 08025d98 1840
    movs r1,#0x5    @ 08025d9a 0521
    rsbs r1,r1,#0    @ 08025d9c 4942
    ands r0,r1    @ 08025d9e 0840
    strb r0,[r2,#0x8]                        @ 08025da0 1072
    bl init_duel_field_icon_and_bg_vram      @ 08025da2 fdf7e3fe
    ldr r0, DWORD_08025dd8                   @ 08025da6 0c48
    ldr r4, DWORD_08025ddc                   @ 08025da8 0c4c
    adds r0,r0,r4    @ 08025daa 0019
    movs r1,#0x7    @ 08025dac 0721
    ldrb r0,[r0,#0x0]                        @ 08025dae 0078
    ands r1,r0    @ 08025db0 0140
    cmp r1,#0x1                              @ 08025db2 0129
    beq LAB_08025e00                         @ 08025db4 24d0
    cmp r1,#0x2                              @ 08025db6 0229
    beq LAB_08025df8                         @ 08025db8 1ed0
    cmp r1,#0x3                              @ 08025dba 0329
    beq LAB_08025df0                         @ 08025dbc 18d0
    cmp r1,#0x4                              @ 08025dbe 0429
    beq LAB_08025de8                         @ 08025dc0 12d0
    ldr r3, DWORD_08025de0                   @ 08025dc2 074b
    cmp r1,#0x5                              @ 08025dc4 0529
    bne LAB_08025e02                         @ 08025dc6 1cd1
    ldr r5, DWORD_08025de4                   @ 08025dc8 064d
    adds r3,r3,r5    @ 08025dca 5b19
    b LAB_08025e02                           @ 08025dcc 19e0
    .zero  0x2
DWORD_08025dd0:
    .word  0x02023360                     @ 08025dd0 60330202
DWORD_08025dd4:
    .word  0xffff807f                     @ 08025dd4 7f80ffff
DWORD_08025dd8:
    .word  0x02000000                     @ 08025dd8 00000002
DWORD_08025ddc:
    .word  0x00006c2c                     @ 08025ddc 2c6c0000
DWORD_08025de0:
    .word  0x09dbff0e                     @ 08025de0 0effdb09
DWORD_08025de4:
    .word  0x0003ab1e                     @ 08025de4 1eab0300
LAB_08025de8:
    ldr r3, DWORD_08025dec                   @ 08025de8 004b
    b LAB_08025e02                           @ 08025dea 0ae0
DWORD_08025dec:
    .word  0x09deee62                     @ 08025dec 62eede09
LAB_08025df0:
    ldr r3, DWORD_08025df4                   @ 08025df0 004b
    b LAB_08025e02                           @ 08025df2 06e0
DWORD_08025df4:
    .word  0x09de29ae                     @ 08025df4 ae29de09
LAB_08025df8:
    ldr r3, DWORD_08025dfc                   @ 08025df8 004b
    b LAB_08025e02                           @ 08025dfa 02e0
DWORD_08025dfc:
    .word  0x09dd6636                     @ 08025dfc 3666dd09
LAB_08025e00:
    ldr r3, DWORD_08025e40                   @ 08025e00 0f4b
LAB_08025e02:
    ldr r4, DWORD_08025e44                   @ 08025e02 104c
    ldr r6, DWORD_08025e48                   @ 08025e04 104e
    adds r4,r4,r6    @ 08025e06 a419
    ldrb r1,[r4,#0x0]                        @ 08025e08 2178
    lsls r0,r1,#0x1d    @ 08025e0a 4807
    lsrs r0,r0,#0x1d    @ 08025e0c 400f
    str r0,[sp,#0x0]                         @ 08025e0e 0090
    movs r0,#0x40    @ 08025e10 4020
    movs r1,#0x84    @ 08025e12 8421
    lsls r1,r1,#0x2    @ 08025e14 8900
    ldr r2, DWORD_08025e4c                   @ 08025e16 0d4a
    bl draw_decimal_with_offset              @ 08025e18 fdf730fd
    movs r0,#0x7    @ 08025e1c 0720
    ldrb r4,[r4,#0x0]                        @ 08025e1e 2478
    ands r0,r4    @ 08025e20 2040
    cmp r0,#0x1                              @ 08025e22 0128
    beq LAB_08025e70                         @ 08025e24 24d0
    cmp r0,#0x2                              @ 08025e26 0228
    beq LAB_08025e68                         @ 08025e28 1ed0
    cmp r0,#0x3                              @ 08025e2a 0328
    beq LAB_08025e60                         @ 08025e2c 18d0
    cmp r0,#0x4                              @ 08025e2e 0428
    beq LAB_08025e58                         @ 08025e30 12d0
    ldr r3, DWORD_08025e50                   @ 08025e32 074b
    cmp r0,#0x5                              @ 08025e34 0528
    bne LAB_08025e72                         @ 08025e36 1cd1
    ldr r2, DWORD_08025e54                   @ 08025e38 064a
    adds r3,r3,r2    @ 08025e3a 9b18
    b LAB_08025e72                           @ 08025e3c 19e0
    .zero  0x2
DWORD_08025e40:
    .word  0x09dcad08                     @ 08025e40 08addc09
DWORD_08025e44:
    .word  0x02000000                     @ 08025e44 00000002
DWORD_08025e48:
    .word  0x00006c2c                     @ 08025e48 2c6c0000
DWORD_08025e4c:
    .word  0x0000010f                     @ 08025e4c 0f010000
DWORD_08025e50:
    .word  0x09dc00b8                     @ 08025e50 b800dc09
DWORD_08025e54:
    .word  0x0003ab50                     @ 08025e54 50ab0300
LAB_08025e58:
    ldr r3, DWORD_08025e5c                   @ 08025e58 004b
    b LAB_08025e72                           @ 08025e5a 0ae0
DWORD_08025e5c:
    .word  0x09def042                     @ 08025e5c 42f0de09
LAB_08025e60:
    ldr r3, DWORD_08025e64                   @ 08025e60 004b
    b LAB_08025e72                           @ 08025e62 06e0
DWORD_08025e64:
    .word  0x09de2b9e                     @ 08025e64 9e2bde09
LAB_08025e68:
    ldr r3, DWORD_08025e6c                   @ 08025e68 004b
    b LAB_08025e72                           @ 08025e6a 02e0
DWORD_08025e6c:
    .word  0x09dd6832                     @ 08025e6c 3268dd09
LAB_08025e70:
    ldr r3, DWORD_08025ea8                   @ 08025e70 0d4b
LAB_08025e72:
    ldr r0, DWORD_08025eac                   @ 08025e72 0e48
    ldr r4, DWORD_08025eb0                   @ 08025e74 0e4c
    adds r0,r0,r4    @ 08025e76 0019
    ldrb r0,[r0,#0x0]                        @ 08025e78 0078
    lsls r0,r0,#0x1d    @ 08025e7a 4007
    lsrs r0,r0,#0x1d    @ 08025e7c 400f
    str r0,[sp,#0x0]                         @ 08025e7e 0090
    movs r0,#0x80    @ 08025e80 8020
    movs r1,#0x87    @ 08025e82 8721
    lsls r1,r1,#0x2    @ 08025e84 8900
    movs r2,#0x1    @ 08025e86 0122
    bl draw_decimal_with_offset              @ 08025e88 fdf7f8fc
    ldr r2, DWORD_08025eb4                   @ 08025e8c 094a
    ldr r5, DWORD_08025eb8                   @ 08025e8e 0a4d
    adds r2,r2,r5    @ 08025e90 5219
    ldrh r3,[r2,#0x0]                        @ 08025e92 1388
    lsls r1,r3,#0x12    @ 08025e94 9904
    lsrs r1,r1,#0x18    @ 08025e96 090e
    adds r1,#0x1    @ 08025e98 0131
    movs r0,#0xff    @ 08025e9a ff20
    ands r1,r0    @ 08025e9c 0140
    lsls r1,r1,#0x6    @ 08025e9e 8901
    ldr r0, DWORD_08025ebc                   @ 08025ea0 0648
    ands r0,r3    @ 08025ea2 1840
    bl SUB_08027c22                          @ 08025ea4 01f0bdfe
DWORD_08025ea8:
    .word  0x09dcaea0                     @ 08025ea8 a0aedc09
DWORD_08025eac:
    .word  0x02000000                     @ 08025eac 00000002
DWORD_08025eb0:
    .word  0x00006c2c                     @ 08025eb0 2c6c0000
DWORD_08025eb4:
    .word  gPrng                          @ 08025eb4 40000003
DWORD_08025eb8:
    .word  0x00000202                     @ 08025eb8 02020000
DWORD_08025ebc:
    .word  0xffffc03f                     @ 08025ebc 3fc0ffff

@ Per-frame tick handler for campaign_scene_handler dispatch table index 1. Trigger: gPrng+0x202 bits[13:6] == 0x01. Sequence: (1) call set_channel_if_changed(4) to switch BGM channel; (2) call render_opp_wins_display_oam to refresh opponent wins sprites; (3) OR DISPCNT shadow with 0xf8*32=0x1f00 to enable sprite display mode; (4) call tick_blend_step_by_delta(4) to advance blend fade; (5) if returns 0 (fade not done) call SUB_08026714 to wait; (6) if done write incremented frame counter to gPrng+0x202 bits[13:6] and update scaler field; (7) tail-call SUB_08026714 to advance.
@ 
@ Constants:
@ - step_index=1
@ - channel_id=4
@ - sprite_mode_or=0xf8*32=0x1f00 (DISPCNT sprite enable mask)
@ - blend_delta=4
@ - frame_ctr_mask=0xffffc03f
run_campaign_step1_channel_and_blend_tick:
    movs r0,#0x4    @ 08025ec0 0420
    bl set_channel_if_changed                @ 08025ec2 d3f00bfe
    bl render_opp_wins_display_oam           @ 08025ec6 fef725f9
    movs r2,#0x80    @ 08025eca 8022
    lsls r2,r2,#0x13    @ 08025ecc d204
    ldrh r0,[r2,#0x0]                        @ 08025ece 1088
    movs r6,#0xf8    @ 08025ed0 f826
    lsls r6,r6,#0x5    @ 08025ed2 7601
    adds r1,r6,#0x0    @ 08025ed4 311c
    orrs r0,r1    @ 08025ed6 0843
    strh r0,[r2,#0x0]                        @ 08025ed8 1080
    movs r0,#0x4    @ 08025eda 0420
    bl tick_blend_step_by_delta              @ 08025edc cff0ecfc
    cmp r0,#0x0                              @ 08025ee0 0028
    bne LAB_08025ee8                         @ 08025ee2 01d1
    bl SUB_08026714                          @ 08025ee4 00f016fc
LAB_08025ee8:
    ldr r2, DWORD_08025f08                   @ 08025ee8 074a
    ldr r0, DWORD_08025f0c                   @ 08025eea 0848
    adds r2,r2,r0    @ 08025eec 1218
    ldrh r3,[r2,#0x0]                        @ 08025eee 1388
    lsls r1,r3,#0x12    @ 08025ef0 9904
    lsrs r1,r1,#0x18    @ 08025ef2 090e
    adds r1,#0x1    @ 08025ef4 0131
    movs r0,#0xff    @ 08025ef6 ff20
    ands r1,r0    @ 08025ef8 0140
    lsls r1,r1,#0x6    @ 08025efa 8901
    ldr r0, DWORD_08025f10                   @ 08025efc 0448
    ands r0,r3    @ 08025efe 1840
    orrs r0,r1    @ 08025f00 0843
    strh r0,[r2,#0x0]                        @ 08025f02 1080
    bl SUB_08026714                          @ 08025f04 00f006fc
DWORD_08025f08:
    .word  gPrng                          @ 08025f08 40000003
DWORD_08025f0c:
    .word  0x00000202                     @ 08025f0c 02020000
DWORD_08025f10:
    .word  0xffffc03f                     @ 08025f10 3fc0ffff

@ campaign_scene_handler dispatch table entry index 2, handles scroll state update for pack selection screen. Clears [scene_ctx+0x8] bit1 (0x02 mask). Reads [scene_ctx+0x3] bits[4:3] as scroll_dir [0..3]: if ==1 jump to LAB_08025fca (scroll right path), if ==2 enter scroll left logic. Left path: check gPrng+0x148 bit6, if set and slot_type > 4 call sync_state_and_init_sprite(0) to init new sprite, update slot_type = (slot_type-5) & 0x1f, set [scene_ctx+0x8] bit0. Right path: check gPrng+0x148 bit7, if set call sync_state_and_init_sprite(0), update slot_type = (slot_type+5) & 0x1f (cyclic clamp to slot_count-1), set bit0.
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - gPrng scroll register = gPrng+0xa4*2 = gPrng+0x148
@ - bit6 = 0x40 (pack scroll left trigger)
@ - bit7 = 0x80 (pack scroll right trigger)
@ - scroll_dir = [scene_ctx+0x3] bits[4:3]
@ - slot stride = 5 (scroll 5 slots per step)
@ - slot_type mask = 0x1f [0..31]
run_campaign_step2_pack_scroll_state:
    ldr r6, DWORD_08026004                   @ 08025f14 3b4e
    movs r4,#0x2    @ 08025f16 0224
    rsbs r4,r4,#0    @ 08025f18 6442
    ldrb r1,[r6,#0x8]                        @ 08025f1a 317a
    ands r4,r1    @ 08025f1c 0c40
    strb r4,[r6,#0x8]                        @ 08025f1e 3472
    ldrb r7,[r6,#0x3]                        @ 08025f20 f778
    lsls r0,r7,#0x1b    @ 08025f22 f806
    lsrs r0,r0,#0x1d    @ 08025f24 400f
    cmp r0,#0x1                              @ 08025f26 0128
    beq LAB_08025fca                         @ 08025f28 4fd0
    cmp r0,#0x2                              @ 08025f2a 0228
    beq LAB_08025f30                         @ 08025f2c 00d0
    b LAB_08026088                           @ 08025f2e abe0
LAB_08025f30:
    ldr r1, DWORD_08026008                   @ 08025f30 3549
    movs r2,#0xa4    @ 08025f32 a422
    lsls r2,r2,#0x1    @ 08025f34 5200
    adds r1,r1,r2    @ 08025f36 8918
    movs r0,#0x40    @ 08025f38 4020
    ldrh r1,[r1,#0x0]                        @ 08025f3a 0988
    ands r0,r1    @ 08025f3c 0840
    cmp r0,#0x0                              @ 08025f3e 0028
    beq LAB_08025f70                         @ 08025f40 16d0
    ldrb r3,[r6,#0x2]                        @ 08025f42 b378
    lsls r0,r3,#0x1b    @ 08025f44 d806
    lsrs r0,r0,#0x1b    @ 08025f46 c00e
    cmp r0,#0x4                              @ 08025f48 0428
    bls LAB_08025f70                         @ 08025f4a 11d9
    movs r0,#0x0    @ 08025f4c 0020
    bl sync_state_and_init_sprite            @ 08025f4e d3f0b1fd
    ldrb r2,[r6,#0x2]                        @ 08025f52 b278
    lsls r1,r2,#0x1b    @ 08025f54 d106
    lsrs r1,r1,#0x1b    @ 08025f56 c90e
    subs r1,#0x5    @ 08025f58 0539
    movs r0,#0x1f    @ 08025f5a 1f20
    ands r1,r0    @ 08025f5c 0140
    movs r0,#0x20    @ 08025f5e 2020
    rsbs r0,r0,#0    @ 08025f60 4042
    ands r0,r2    @ 08025f62 1040
    orrs r0,r1    @ 08025f64 0843
    strb r0,[r6,#0x2]                        @ 08025f66 b070
    movs r0,#0x1    @ 08025f68 0120
    ldrb r4,[r6,#0x8]                        @ 08025f6a 347a
    orrs r0,r4    @ 08025f6c 2043
    strb r0,[r6,#0x8]                        @ 08025f6e 3072
LAB_08025f70:
    ldr r2, DWORD_08026008                   @ 08025f70 254a
    movs r5,#0xa4    @ 08025f72 a425
    lsls r5,r5,#0x1    @ 08025f74 6d00
    adds r1,r2,r5    @ 08025f76 5119
    movs r0,#0x80    @ 08025f78 8020
    ldrh r1,[r1,#0x0]                        @ 08025f7a 0988
    ands r0,r1    @ 08025f7c 0840
    .hword 0x4691    @ 08025f7e 9146
    cmp r0,#0x0                              @ 08025f80 0028
    beq LAB_08025fca                         @ 08025f82 22d0
    ldr r4, DWORD_08026004                   @ 08025f84 1f4c
    ldrb r6,[r4,#0x2]                        @ 08025f86 a678
    lsls r0,r6,#0x1b    @ 08025f88 f006
    lsrs r0,r0,#0x1b    @ 08025f8a c00e
    cmp r0,#0x4                              @ 08025f8c 0428
    bhi LAB_08025fca                         @ 08025f8e 1cd8
    movs r0,#0x0    @ 08025f90 0020
    bl sync_state_and_init_sprite            @ 08025f92 d3f08ffd
    ldrb r0,[r4,#0x2]                        @ 08025f96 a078
    lsls r1,r0,#0x1b    @ 08025f98 c106
    lsrs r1,r1,#0x1b    @ 08025f9a c90e
    adds r1,#0x5    @ 08025f9c 0531
    movs r5,#0x1f    @ 08025f9e 1f25
    ands r1,r5    @ 08025fa0 2940
    movs r3,#0x20    @ 08025fa2 2023
    rsbs r3,r3,#0    @ 08025fa4 5b42
    adds r2,r3,#0x0    @ 08025fa6 1a1c
    ands r2,r0    @ 08025fa8 0240
    orrs r2,r1    @ 08025faa 0a43
    strb r2,[r4,#0x2]                        @ 08025fac a270
    lsls r0,r2,#0x1b    @ 08025fae d006
    lsrs r0,r0,#0x1b    @ 08025fb0 c00e
    ldrh r1,[r4,#0x0]                        @ 08025fb2 2188
    subs r1,#0x1    @ 08025fb4 0139
    cmp r0,r1                                @ 08025fb6 8842
    ble LAB_08025fc2                         @ 08025fb8 03dd
    ands r1,r5    @ 08025fba 2940
    ands r2,r3    @ 08025fbc 1a40
    orrs r2,r1    @ 08025fbe 0a43
    strb r2,[r4,#0x2]                        @ 08025fc0 a270
LAB_08025fc2:
    movs r0,#0x1    @ 08025fc2 0120
    ldrb r1,[r4,#0x8]                        @ 08025fc4 217a
    orrs r0,r1    @ 08025fc6 0843
    strb r0,[r4,#0x8]                        @ 08025fc8 2072
LAB_08025fca:
    movs r1,#0xa4    @ 08025fca a421
    lsls r1,r1,#0x1    @ 08025fcc 4900
    add r1,r9                                @ 08025fce 4944
    movs r0,#0x20    @ 08025fd0 2020
    ldrh r1,[r1,#0x0]                        @ 08025fd2 0988
    ands r0,r1    @ 08025fd4 0840
    cmp r0,#0x0                              @ 08025fd6 0028
    beq LAB_0802602a                         @ 08025fd8 27d0
    movs r0,#0x0    @ 08025fda 0020
    bl sync_state_and_init_sprite            @ 08025fdc d3f06afd
    ldr r3, DWORD_08026004                   @ 08025fe0 084b
    ldrb r2,[r3,#0x2]                        @ 08025fe2 9a78
    movs r4,#0x1f    @ 08025fe4 1f24
    movs r0,#0x1f    @ 08025fe6 1f20
    ands r0,r2    @ 08025fe8 1040
    cmp r0,#0x0                              @ 08025fea 0028
    beq LAB_0802600c                         @ 08025fec 0ed0
    lsls r0,r2,#0x1b    @ 08025fee d006
    lsrs r0,r0,#0x1b    @ 08025ff0 c00e
    subs r0,#0x1    @ 08025ff2 0138
    ands r0,r4    @ 08025ff4 2040
    movs r1,#0x20    @ 08025ff6 2021
    rsbs r1,r1,#0    @ 08025ff8 4942
    ands r1,r2    @ 08025ffa 1140
    orrs r1,r0    @ 08025ffc 0143
    strb r1,[r3,#0x2]                        @ 08025ffe 9970
    b LAB_0802601c                           @ 08026000 0ce0
    .zero  0x2
DWORD_08026004:
    .word  0x02023360                     @ 08026004 60330202
DWORD_08026008:
    .word  gPrng                          @ 08026008 40000003
LAB_0802600c:
    ldrh r1,[r3,#0x0]                        @ 0802600c 1988
    subs r1,#0x1    @ 0802600e 0139
    ands r1,r4    @ 08026010 2140
    movs r0,#0x20    @ 08026012 2020
    rsbs r0,r0,#0    @ 08026014 4042
    ands r0,r2    @ 08026016 1040
    orrs r0,r1    @ 08026018 0843
    strb r0,[r3,#0x2]                        @ 0802601a 9870
LAB_0802601c:
    ldr r1, DWORD_08026068                   @ 0802601c 1249
    movs r0,#0x1    @ 0802601e 0120
    ldrb r2,[r1,#0x8]                        @ 08026020 0a7a
    orrs r0,r2    @ 08026022 1043
    strb r0,[r1,#0x8]                        @ 08026024 0872
    ldr r3, DWORD_0802606c                   @ 08026026 114b
    .hword 0x4699    @ 08026028 9946
LAB_0802602a:
    movs r1,#0xa4    @ 0802602a a421
    lsls r1,r1,#0x1    @ 0802602c 4900
    add r1,r9                                @ 0802602e 4944
    movs r0,#0x10    @ 08026030 1020
    ldrh r1,[r1,#0x0]                        @ 08026032 0988
    ands r0,r1    @ 08026034 0840
    cmp r0,#0x0                              @ 08026036 0028
    bne LAB_0802603c                         @ 08026038 00d1
    b LAB_080265c2                           @ 0802603a c2e2
LAB_0802603c:
    movs r0,#0x0    @ 0802603c 0020
    bl sync_state_and_init_sprite            @ 0802603e d3f039fd
    ldr r4, DWORD_08026068                   @ 08026042 094c
    ldrb r2,[r4,#0x2]                        @ 08026044 a278
    lsls r3,r2,#0x1b    @ 08026046 d306
    lsrs r1,r3,#0x1b    @ 08026048 d90e
    ldrh r0,[r4,#0x0]                        @ 0802604a 2088
    subs r0,#0x1    @ 0802604c 0138
    cmp r1,r0                                @ 0802604e 8142
    bge LAB_08026070                         @ 08026050 0eda
    adds r0,r1,#0x0    @ 08026052 081c
    adds r0,#0x1    @ 08026054 0130
    movs r1,#0x1f    @ 08026056 1f21
    ands r0,r1    @ 08026058 0840
    movs r1,#0x20    @ 0802605a 2021
    rsbs r1,r1,#0    @ 0802605c 4942
    ands r1,r2    @ 0802605e 1140
    orrs r1,r0    @ 08026060 0143
    strb r1,[r4,#0x2]                        @ 08026062 a170
    b LAB_08026078                           @ 08026064 08e0
    .zero  0x2
DWORD_08026068:
    .word  0x02023360                     @ 08026068 60330202
DWORD_0802606c:
    .word  gPrng                          @ 0802606c 40000003
LAB_08026070:
    movs r0,#0x20    @ 08026070 2020
    rsbs r0,r0,#0    @ 08026072 4042
    ands r0,r2    @ 08026074 1040
    strb r0,[r4,#0x2]                        @ 08026076 a070
LAB_08026078:
    ldr r1, DWORD_08026084                   @ 08026078 0249
    movs r0,#0x1    @ 0802607a 0120
    ldrb r4,[r1,#0x8]                        @ 0802607c 0c7a
    orrs r0,r4    @ 0802607e 2043
    strb r0,[r1,#0x8]                        @ 08026080 0872
    b LAB_080265c2                           @ 08026082 9ee2
DWORD_08026084:
    .word  0x02023360                     @ 08026084 60330202
LAB_08026088:
    ldrb r2,[r6,#0x5]                        @ 08026088 7279
    movs r5,#0xf    @ 0802608a 0f25
    .hword 0x46a8    @ 0802608c a846
    .hword 0x4640    @ 0802608e 4046
    ands r0,r2    @ 08026090 1040
    cmp r0,#0x0                              @ 08026092 0028
    beq LAB_08026114                         @ 08026094 3ed0
    lsls r0,r2,#0x1c    @ 08026096 1007
    lsrs r0,r0,#0x1c    @ 08026098 000f
    subs r0,#0x1    @ 0802609a 0138
    movs r1,#0xf    @ 0802609c 0f21
    ands r0,r1    @ 0802609e 0840
    movs r3,#0x10    @ 080260a0 1023
    rsbs r3,r3,#0    @ 080260a2 5b42
    ands r3,r2    @ 080260a4 1340
    orrs r3,r0    @ 080260a6 0343
    strb r3,[r6,#0x5]                        @ 080260a8 7371
    lsls r0,r7,#0x18    @ 080260aa 3806
    lsrs r0,r0,#0x1d    @ 080260ac 400f
    movs r4,#0x1f    @ 080260ae 1f24
    adds r1,r4,#0x0    @ 080260b0 211c
    ldrb r2,[r6,#0x4]                        @ 080260b2 3279
    ands r1,r2    @ 080260b4 1140
    lsls r1,r1,#0x3    @ 080260b6 c900
    orrs r1,r0    @ 080260b8 0143
    movs r0,#0x6    @ 080260ba 0620
    ldrsh r5,[r6,r0]                         @ 080260bc 355e
    ldr r2, DWORD_08026110                   @ 080260be 144a
    lsls r0,r3,#0x1c    @ 080260c0 1807
    lsrs r0,r0,#0x1a    @ 080260c2 800e
    adds r0,r0,r2    @ 080260c4 8018
    ldr r0,[r0,#0x0]                         @ 080260c6 0068
    muls r0,r5    @ 080260c8 6843
    subs r1,r1,r0    @ 080260ca 091a
    lsls r1,r1,#0x10    @ 080260cc 0904
    lsrs r2,r1,#0x10    @ 080260ce 0a0c
    movs r0,#0x7    @ 080260d0 0720
    ands r2,r0    @ 080260d2 0240
    lsls r2,r2,#0x5    @ 080260d4 5201
    adds r0,r4,#0x0    @ 080260d6 201c
    ands r0,r7    @ 080260d8 3840
    orrs r0,r2    @ 080260da 1043
    strb r0,[r6,#0x3]                        @ 080260dc f070
    lsrs r1,r1,#0x13    @ 080260de c90c
    movs r5,#0x1f    @ 080260e0 1f25
    ands r1,r4    @ 080260e2 2140
    movs r2,#0x20    @ 080260e4 2022
    rsbs r2,r2,#0    @ 080260e6 5242
    adds r0,r2,#0x0    @ 080260e8 101c
    ldrb r4,[r6,#0x4]                        @ 080260ea 3479
    ands r0,r4    @ 080260ec 2040
    orrs r0,r1    @ 080260ee 0843
    strb r0,[r6,#0x4]                        @ 080260f0 3071
    .hword 0x4640    @ 080260f2 4046
    ands r3,r0    @ 080260f4 0340
    cmp r3,#0x0                              @ 080260f6 002b
    beq LAB_080260fc                         @ 080260f8 00d0
    b LAB_080265c2                           @ 080260fa 62e2
LAB_080260fc:
    ldrh r3,[r6,#0x2]                        @ 080260fc 7388
    lsls r1,r3,#0x16    @ 080260fe 9905
    lsrs r1,r1,#0x1b    @ 08026100 c90e
    ands r1,r5    @ 08026102 2940
    adds r0,r2,#0x0    @ 08026104 101c
    ldrb r4,[r6,#0x2]                        @ 08026106 b478
    ands r0,r4    @ 08026108 2040
    orrs r0,r1    @ 0802610a 0843
    strb r0,[r6,#0x2]                        @ 0802610c b070
    b LAB_080265c2                           @ 0802610e 58e2
DWORD_08026110:
    .word  0x09e59cf8                     @ 08026110 f89ce509
LAB_08026114:
    movs r5,#0x0    @ 08026114 0025
    str r5,[sp,#0x8]                         @ 08026116 0295
    movs r0,#0x0    @ 08026118 0020
    str r0,[sp,#0xc]                         @ 0802611a 0390
    ldrh r3,[r6,#0x6]                        @ 0802611c f388
    movs r1,#0x6    @ 0802611e 0621
    ldrsh r0,[r6,r1]                         @ 08026120 705e
    cmp r0,#0x0                              @ 08026122 0028
    beq LAB_08026154                         @ 08026124 16d0
    ldrb r2,[r6,#0x4]                        @ 08026126 3279
    lsrs r1,r2,#0x5    @ 08026128 5109
    adds r1,r1,r3    @ 0802612a c918
    lsls r1,r1,#0x5    @ 0802612c 4901
    movs r0,#0x1f    @ 0802612e 1f20
    ands r0,r2    @ 08026130 1040
    orrs r0,r1    @ 08026132 0843
    strb r0,[r6,#0x4]                        @ 08026134 3071
    .hword 0x466a    @ 08026136 6a46
    ldrh r2,[r2,#0xc]                        @ 08026138 9289
    strh r2,[r6,#0x6]                        @ 0802613a f280
    ldrh r3,[r6,#0x2]                        @ 0802613c 7388
    lsls r1,r3,#0x16    @ 0802613e 9905
    lsrs r1,r1,#0x1b    @ 08026140 c90e
    movs r0,#0x20    @ 08026142 2020
    rsbs r0,r0,#0    @ 08026144 4042
    ldrb r5,[r6,#0x2]                        @ 08026146 b578
    ands r0,r5    @ 08026148 2840
    orrs r0,r1    @ 0802614a 0843
    strb r0,[r6,#0x2]                        @ 0802614c b070
    movs r0,#0x1    @ 0802614e 0120
    orrs r4,r0    @ 08026150 0443
    strb r4,[r6,#0x8]                        @ 08026152 3472
LAB_08026154:
    ldrb r1,[r6,#0x2]                        @ 08026154 b178
    lsls r0,r1,#0x1b    @ 08026156 c806
    movs r2,#0x1f    @ 08026158 1f22
    .hword 0x4690    @ 0802615a 9046
    lsrs r0,r0,#0x16    @ 0802615c 800d
    ldr r7, DWORD_080261b8                   @ 0802615e 164f
    adds r5,r7,#0x0    @ 08026160 3d1c
    ldrh r3,[r6,#0x2]                        @ 08026162 7388
    ands r5,r3    @ 08026164 1d40
    orrs r5,r0    @ 08026166 0543
    strh r5,[r6,#0x2]                        @ 08026168 7580
    movs r0,#0xa4    @ 0802616a a420
    lsls r0,r0,#0x1    @ 0802616c 4000
    add r0,r9                                @ 0802616e 4844
    ldrh r1,[r0,#0x0]                        @ 08026170 0188
    movs r0,#0x40    @ 08026172 4020
    ands r0,r1    @ 08026174 0840
    cmp r0,#0x0                              @ 08026176 0028
    beq LAB_080261bc                         @ 08026178 20d0
    lsls r0,r5,#0x16    @ 0802617a a805
    lsrs r0,r0,#0x1b    @ 0802617c c00e
    cmp r0,#0x4                              @ 0802617e 0428
    bhi LAB_08026184                         @ 08026180 00d8
    b LAB_080262e4                           @ 08026182 afe0
LAB_08026184:
    movs r0,#0x0    @ 08026184 0020
    bl sync_state_and_init_sprite            @ 08026186 d3f095fc
    ldrh r2,[r6,#0x2]                        @ 0802618a 7288
    lsls r0,r2,#0x16    @ 0802618c 9005
    lsrs r0,r0,#0x1b    @ 0802618e c00e
    subs r0,#0x5    @ 08026190 0538
    .hword 0x4644    @ 08026192 4446
    ands r0,r4    @ 08026194 2040
    lsls r0,r0,#0x5    @ 08026196 4001
    adds r1,r7,#0x0    @ 08026198 391c
    ands r1,r2    @ 0802619a 1140
    orrs r1,r0    @ 0802619c 0143
    strh r1,[r6,#0x2]                        @ 0802619e 7180
    lsls r1,r1,#0x16    @ 080261a0 8905
    lsrs r1,r1,#0x1b    @ 080261a2 c90e
    ldrb r6,[r6,#0x4]                        @ 080261a4 3679
    lsrs r2,r6,#0x5    @ 080261a6 7209
    lsls r0,r2,#0x2    @ 080261a8 9000
    adds r0,r0,r2    @ 080261aa 8018
    cmp r1,r0                                @ 080261ac 8142
    blt LAB_080261b2                         @ 080261ae 00db
    b LAB_080262e4                           @ 080261b0 98e0
LAB_080261b2:
    movs r5,#0x1    @ 080261b2 0125
    str r5,[sp,#0x8]                         @ 080261b4 0295
    b LAB_080262e4                           @ 080261b6 95e0
DWORD_080261b8:
    .word  0xfffffc1f                     @ 080261b8 1ffcffff
LAB_080261bc:
    movs r0,#0x80    @ 080261bc 8020
    ands r0,r1    @ 080261be 0840
    cmp r0,#0x0                              @ 080261c0 0028
    beq LAB_08026228                         @ 080261c2 31d0
    lsls r2,r5,#0x16    @ 080261c4 aa05
    lsrs r2,r2,#0x1b    @ 080261c6 d20e
    adds r2,#0x5    @ 080261c8 0532
    ldrb r0,[r6,#0x3]                        @ 080261ca f078
    lsls r1,r0,#0x1b    @ 080261cc c106
    lsrs r1,r1,#0x1d    @ 080261ce 490f
    lsls r0,r1,#0x2    @ 080261d0 8800
    adds r0,r0,r1    @ 080261d2 4018
    cmp r2,r0                                @ 080261d4 8242
    blt LAB_080261da                         @ 080261d6 00db
    b LAB_080262e4                           @ 080261d8 84e0
LAB_080261da:
    movs r0,#0x0    @ 080261da 0020
    bl sync_state_and_init_sprite            @ 080261dc d3f06afc
    ldrh r0,[r6,#0x2]                        @ 080261e0 7088
    lsls r1,r0,#0x16    @ 080261e2 8105
    lsrs r1,r1,#0x1b    @ 080261e4 c90e
    adds r1,#0x5    @ 080261e6 0531
    .hword 0x4642    @ 080261e8 4246
    ands r1,r2    @ 080261ea 1140
    lsls r1,r1,#0x5    @ 080261ec 4901
    adds r2,r7,#0x0    @ 080261ee 3a1c
    ands r2,r0    @ 080261f0 0240
    orrs r2,r1    @ 080261f2 0a43
    strh r2,[r6,#0x2]                        @ 080261f4 7280
    lsls r0,r2,#0x16    @ 080261f6 9005
    lsrs r0,r0,#0x1b    @ 080261f8 c00e
    ldrh r1,[r6,#0x0]                        @ 080261fa 3188
    subs r1,#0x1    @ 080261fc 0139
    cmp r0,r1                                @ 080261fe 8842
    ble LAB_0802620e                         @ 08026200 05dd
    .hword 0x4643    @ 08026202 4346
    ands r1,r3    @ 08026204 1940
    lsls r0,r1,#0x5    @ 08026206 4801
    ands r2,r7    @ 08026208 3a40
    orrs r2,r0    @ 0802620a 0243
    strh r2,[r6,#0x2]                        @ 0802620c 7280
LAB_0802620e:
    ldrh r4,[r6,#0x2]                        @ 0802620e 7488
    lsls r2,r4,#0x16    @ 08026210 a205
    lsrs r2,r2,#0x1b    @ 08026212 d20e
    ldrb r6,[r6,#0x4]                        @ 08026214 3679
    lsrs r1,r6,#0x5    @ 08026216 7109
    lsls r0,r1,#0x2    @ 08026218 8800
    adds r0,r0,r1    @ 0802621a 4018
    adds r0,#0x9    @ 0802621c 0930
    cmp r2,r0                                @ 0802621e 8242
    ble LAB_080262e4                         @ 08026220 60dd
    movs r5,#0x1    @ 08026222 0125
    str r5,[sp,#0xc]                         @ 08026224 0395
    b LAB_080262ec                           @ 08026226 61e0
LAB_08026228:
    movs r0,#0x20    @ 08026228 2020
    ands r0,r1    @ 0802622a 0840
    cmp r0,#0x0                              @ 0802622c 0028
    beq LAB_08026278                         @ 0802622e 23d0
    movs r0,#0x0    @ 08026230 0020
    bl sync_state_and_init_sprite            @ 08026232 d3f03ffc
    ldrh r2,[r6,#0x2]                        @ 08026236 7288
    movs r0,#0xf8    @ 08026238 f820
    lsls r0,r0,#0x2    @ 0802623a 8000
    ands r0,r2    @ 0802623c 1040
    cmp r0,#0x0                              @ 0802623e 0028
    beq LAB_0802626c                         @ 08026240 14d0
    lsls r0,r2,#0x16    @ 08026242 9005
    lsrs r0,r0,#0x1b    @ 08026244 c00e
    subs r0,#0x1    @ 08026246 0138
    .hword 0x4641    @ 08026248 4146
    ands r0,r1    @ 0802624a 0840
    lsls r0,r0,#0x5    @ 0802624c 4001
    adds r1,r7,#0x0    @ 0802624e 391c
    ands r1,r2    @ 08026250 1140
    orrs r1,r0    @ 08026252 0143
    strh r1,[r6,#0x2]                        @ 08026254 7180
    lsls r1,r1,#0x16    @ 08026256 8905
    lsrs r1,r1,#0x1b    @ 08026258 c90e
    ldrb r6,[r6,#0x4]                        @ 0802625a 3679
    lsrs r2,r6,#0x5    @ 0802625c 7209
    lsls r0,r2,#0x2    @ 0802625e 9000
    adds r0,r0,r2    @ 08026260 8018
    cmp r1,r0                                @ 08026262 8142
    bge LAB_080262e4                         @ 08026264 3eda
    movs r2,#0x1    @ 08026266 0122
    str r2,[sp,#0x8]                         @ 08026268 0292
    b LAB_080262e4                           @ 0802626a 3be0
LAB_0802626c:
    adds r0,r7,#0x0    @ 0802626c 381c
    ands r0,r2    @ 0802626e 1040
    movs r1,#0x80    @ 08026270 8021
    orrs r0,r1    @ 08026272 0843
    strh r0,[r6,#0x2]                        @ 08026274 7080
    b LAB_080262e4                           @ 08026276 35e0
LAB_08026278:
    movs r0,#0x10    @ 08026278 1020
    ands r0,r1    @ 0802627a 0840
    cmp r0,#0x0                              @ 0802627c 0028
    beq LAB_080262e4                         @ 0802627e 31d0
    lsls r2,r5,#0x16    @ 08026280 aa05
    lsrs r3,r2,#0x1b    @ 08026282 d30e
    .hword 0x4699    @ 08026284 9946
    adds r1,r3,#0x0    @ 08026286 191c
    ldrh r0,[r6,#0x0]                        @ 08026288 3088
    subs r0,#0x1    @ 0802628a 0138
    cmp r1,r0                                @ 0802628c 8142
    bge LAB_080262ba                         @ 0802628e 14da
    adds r0,r1,#0x0    @ 08026290 081c
    adds r0,#0x1    @ 08026292 0130
    .hword 0x4644    @ 08026294 4446
    ands r0,r4    @ 08026296 2040
    lsls r0,r0,#0x5    @ 08026298 4001
    adds r1,r7,#0x0    @ 0802629a 391c
    ands r1,r5    @ 0802629c 2940
    orrs r1,r0    @ 0802629e 0143
    strh r1,[r6,#0x2]                        @ 080262a0 7180
    lsls r1,r1,#0x16    @ 080262a2 8905
    lsrs r1,r1,#0x1b    @ 080262a4 c90e
    ldrb r6,[r6,#0x4]                        @ 080262a6 3679
    lsrs r2,r6,#0x5    @ 080262a8 7209
    lsls r0,r2,#0x2    @ 080262aa 9000
    adds r0,r0,r2    @ 080262ac 8018
    adds r0,#0x9    @ 080262ae 0930
    cmp r1,r0                                @ 080262b0 8142
    ble LAB_080262d2                         @ 080262b2 0edd
    movs r5,#0x1    @ 080262b4 0125
    str r5,[sp,#0xc]                         @ 080262b6 0395
    b LAB_080262d2                           @ 080262b8 0be0
LAB_080262ba:
    lsrs r4,r2,#0x1b    @ 080262ba d40e
    adds r0,r4,#0x0    @ 080262bc 201c
    movs r1,#0x5    @ 080262be 0521
    bl __umodsi3                             @ 080262c0 e8f0c8fa
    subs r4,r4,r0    @ 080262c4 241a
    .hword 0x4640    @ 080262c6 4046
    ands r4,r0    @ 080262c8 0440
    lsls r4,r4,#0x5    @ 080262ca 6401
    ands r5,r7    @ 080262cc 3d40
    orrs r5,r4    @ 080262ce 2543
    strh r5,[r6,#0x2]                        @ 080262d0 7580
LAB_080262d2:
    ldr r0, DWORD_0802644c                   @ 080262d2 5e48
    ldrh r0,[r0,#0x2]                        @ 080262d4 4088
    lsls r0,r0,#0x16    @ 080262d6 8005
    lsrs r0,r0,#0x1b    @ 080262d8 c00e
    cmp r9,r0                                @ 080262da 8145
    beq LAB_080262e4                         @ 080262dc 02d0
    movs r0,#0x0    @ 080262de 0020
    bl sync_state_and_init_sprite            @ 080262e0 d3f0e8fb
LAB_080262e4:
    ldr r1,[sp,#0xc]                         @ 080262e4 0399
    cmp r1,#0x0                              @ 080262e6 0029
    bne LAB_080262ec                         @ 080262e8 00d1
    b LAB_08026416                           @ 080262ea 94e0
LAB_080262ec:
    ldr r2, DWORD_0802644c                   @ 080262ec 574a
    movs r0,#0x1    @ 080262ee 0120
    strh r0,[r2,#0x6]                        @ 080262f0 d080
    subs r0,#0x11    @ 080262f2 1138
    ldrb r3,[r2,#0x5]                        @ 080262f4 5379
    ands r0,r3    @ 080262f6 1840
    movs r1,#0x8    @ 080262f8 0821
    orrs r0,r1    @ 080262fa 0843
    strb r0,[r2,#0x5]                        @ 080262fc 5071
    movs r0,#0xe0    @ 080262fe e020
    ldrb r4,[r2,#0x4]                        @ 08026300 1479
    ands r0,r4    @ 08026302 2040
    cmp r0,#0x40                             @ 08026304 4028
    beq LAB_0802630a                         @ 08026306 00d0
    b LAB_08026416                           @ 08026308 85e0
LAB_0802630a:
    ldrb r2,[r2,#0x3]                        @ 0802630a d278
    lsls r0,r2,#0x1b    @ 0802630c d006
    lsrs r0,r0,#0x1d    @ 0802630e 400f
    cmp r0,#0x5                              @ 08026310 0528
    bhi LAB_08026316                         @ 08026312 00d8
    b LAB_08026416                           @ 08026314 7fe0
LAB_08026316:
    ldr r0, DWORD_08026450                   @ 08026316 4e48
    bl game_str_id_to_row                    @ 08026318 cef07efd
    ldr r2, DWORD_08026454                   @ 0802631c 4d4a
    lsls r0,r0,#0x10    @ 0802631e 0004
    lsrs r0,r0,#0x10    @ 08026320 000c
    lsls r1,r0,#0x1    @ 08026322 4100
    adds r1,r1,r0    @ 08026324 0918
    lsls r1,r1,#0x1    @ 08026326 4900
    ldr r0, DWORD_08026458                   @ 08026328 4b48
    ldr r5, DWORD_0802645c                   @ 0802632a 4c4d
    adds r0,r0,r5    @ 0802632c 4019
    ldrb r0,[r0,#0x0]                        @ 0802632e 0078
    lsls r0,r0,#0x1d    @ 08026330 4007
    lsrs r0,r0,#0x1d    @ 08026332 400f
    adds r1,r1,r0    @ 08026334 0918
    lsls r1,r1,#0x2    @ 08026336 8900
    adds r1,r1,r2    @ 08026338 8918
    ldr r1,[r1,#0x0]                         @ 0802633a 0968
    ldr r0, DWORD_08026460                   @ 0802633c 4848
    adds r1,r1,r0    @ 0802633e 0918
    ldr r0, DWORD_08026464                   @ 08026340 4848
    movs r2,#0x84    @ 08026342 8422
    lsls r2,r2,#0x2    @ 08026344 9200
    ldr r3, DWORD_08026468                   @ 08026346 484b
    str r1,[sp,#0x0]                         @ 08026348 0091
    movs r1,#0xd6    @ 0802634a d621
    bl render_centered_text_to_bg_vram       @ 0802634c fdf722fb
    ldr r5, DWORD_0802646c                   @ 08026350 464d
    movs r6,#0x93    @ 08026352 9326
    lsls r6,r6,#0x1    @ 08026354 7600
    ldr r4, DWORD_08026470                   @ 08026356 464c
    adds r0,r5,#0x0    @ 08026358 281c
    movs r1,#0x40    @ 0802635a 4021
    adds r2,r6,#0x0    @ 0802635c 321c
    adds r3,r4,#0x0    @ 0802635e 231c
    bl write_tile_row_to_vram                @ 08026360 c7f0f4fd
    ldrh r6,[r4,#0x0]                        @ 08026364 2688
    lsls r0,r6,#0x1    @ 08026366 7000
    adds r1,r0,#0x0    @ 08026368 011c
    adds r1,#0x8    @ 0802636a 0831
    adds r1,r1,r4    @ 0802636c 0919
    adds r0,#0x10    @ 0802636e 1030
    adds r0,r0,r4    @ 08026370 0019
    ldrh r1,[r1,#0x0]                        @ 08026372 0988
    lsls r1,r1,#0x5    @ 08026374 4901
    adds r0,r0,r1    @ 08026376 4018
    .hword 0x4680    @ 08026378 8046
    .hword 0x4645    @ 0802637a 4546
    adds r5,#0x8    @ 0802637c 0835
    movs r7,#0x0    @ 0802637e 0027
    ldrh r0,[r0,#0x0]                        @ 08026380 0088
    cmp r7,r0                                @ 08026382 8742
    bcs LAB_08026406                         @ 08026384 3fd2
    movs r1,#0xc0    @ 08026386 c021
    lsls r1,r1,#0x4    @ 08026388 0901
    .hword 0x468c    @ 0802638a 8c46
    ldr r2, DWORD_08026474                   @ 0802638c 394a
    .hword 0x4692    @ 0802638e 9246
    ldr r3, DWORD_08026478                   @ 08026390 394b
    .hword 0x4699    @ 08026392 9946
LAB_08026394:
    ldrh r0,[r5,#0x0]                        @ 08026394 2888
    adds r5,#0x2    @ 08026396 0235
    ldrh r4,[r5,#0x0]                        @ 08026398 2c88
    adds r5,#0x2    @ 0802639a 0235
    movs r3,#0x3f    @ 0802639c 3f23
    ands r3,r0    @ 0802639e 0340
    movs r6,#0xff    @ 080263a0 ff26
    lsls r6,r6,#0x8    @ 080263a2 3602
    ands r0,r6    @ 080263a4 3040
    movs r1,#0xc0    @ 080263a6 c021
    lsls r1,r1,#0x13    @ 080263a8 c904
    str r1,[sp,#0x10]                        @ 080263aa 0491
    lsrs r1,r0,#0x3    @ 080263ac c108
    adds r0,r3,#0x0    @ 080263ae 181c
    orrs r0,r1    @ 080263b0 0843
    adds r2,r4,#0x0    @ 080263b2 221c
    .hword 0x4666    @ 080263b4 6646
    ands r2,r6    @ 080263b6 3240
    cmp r3,#0x1f                             @ 080263b8 1f2b
    bls LAB_080263ca                         @ 080263ba 06d9
    ldr r0, DWORD_0802647c                   @ 080263bc 2f48
    str r0,[sp,#0x10]                        @ 080263be 0490
    adds r0,r3,#0x0    @ 080263c0 181c
    subs r0,#0x20    @ 080263c2 2038
    orrs r1,r0    @ 080263c4 0143
    lsls r0,r1,#0x10    @ 080263c6 0804
    lsrs r0,r0,#0x10    @ 080263c8 000c
LAB_080263ca:
    ldr r1, DWORD_0802646c                   @ 080263ca 2849
    adds r0,r0,r1    @ 080263cc 4018
    lsls r0,r0,#0x10    @ 080263ce 0004
    lsrs r0,r0,#0x10    @ 080263d0 000c
    cmp r0,r10                               @ 080263d2 5045
    bls LAB_080263de                         @ 080263d4 03d9
    ldr r3, DWORD_08026480                   @ 080263d6 2a4b
    adds r0,r0,r3    @ 080263d8 c018
    lsls r0,r0,#0x10    @ 080263da 0004
    lsrs r0,r0,#0x10    @ 080263dc 000c
LAB_080263de:
    .hword 0x464e    @ 080263de 4e46
    ands r4,r6    @ 080263e0 3440
    lsls r1,r0,#0x1    @ 080263e2 4100
    ldr r0,[sp,#0x10]                        @ 080263e4 0498
    adds r1,r1,r0    @ 080263e6 0918
    movs r3,#0x93    @ 080263e8 9323
    lsls r3,r3,#0x1    @ 080263ea 5b00
    adds r0,r4,r3    @ 080263ec e018
    orrs r2,r0    @ 080263ee 0243
    movs r4,#0x40    @ 080263f0 4024
    lsls r0,r4,#0x8    @ 080263f2 2002
    orrs r2,r0    @ 080263f4 0243
    strh r2,[r1,#0x0]                        @ 080263f6 0a80
    adds r0,r7,#0x1    @ 080263f8 781c
    lsls r0,r0,#0x10    @ 080263fa 0004
    lsrs r7,r0,#0x10    @ 080263fc 070c
    .hword 0x4646    @ 080263fe 4646
    ldrh r6,[r6,#0x0]                        @ 08026400 3688
    cmp r7,r6                                @ 08026402 b742
    bcc LAB_08026394                         @ 08026404 c6d3
LAB_08026406:
    ldr r0, DWORD_08026484                   @ 08026406 1f48
    movs r1,#0x80    @ 08026408 8021
    bl zero_fill_by_halfword                 @ 0802640a cef033fd
    ldr r0, DWORD_0802647c                   @ 0802640e 1b48
    movs r1,#0x80    @ 08026410 8021
    bl zero_fill_by_halfword                 @ 08026412 cef02ffd
LAB_08026416:
    ldr r0,[sp,#0x8]                         @ 08026416 0298
    cmp r0,#0x0                              @ 08026418 0028
    bne LAB_08026488                         @ 0802641a 35d1
    ldr r1,[sp,#0xc]                         @ 0802641c 0399
    cmp r1,#0x0                              @ 0802641e 0029
    bne LAB_080264fe                         @ 08026420 6dd1
    ldr r3, DWORD_0802644c                   @ 08026422 0a4b
    ldrb r4,[r3,#0x2]                        @ 08026424 9c78
    lsls r0,r4,#0x1b    @ 08026426 e006
    ldrh r5,[r3,#0x2]                        @ 08026428 5d88
    lsls r2,r5,#0x16    @ 0802642a aa05
    lsrs r0,r0,#0x1b    @ 0802642c c00e
    lsrs r1,r2,#0x1b    @ 0802642e d10e
    cmp r0,r1                                @ 08026430 8842
    beq LAB_080264fe                         @ 08026432 64d0
    adds r0,r1,#0x0    @ 08026434 081c
    movs r1,#0x20    @ 08026436 2021
    rsbs r1,r1,#0    @ 08026438 4942
    ands r1,r4    @ 0802643a 2140
    orrs r1,r0    @ 0802643c 0143
    strb r1,[r3,#0x2]                        @ 0802643e 9970
    movs r0,#0x1    @ 08026440 0120
    ldrb r6,[r3,#0x8]                        @ 08026442 1e7a
    orrs r0,r6    @ 08026444 3043
    strb r0,[r3,#0x8]                        @ 08026446 1872
    b LAB_080265c2                           @ 08026448 bbe0
    .zero  0x2
DWORD_0802644c:
    .word  0x02023360                     @ 0802644c 60330202
DWORD_08026450:
    .word  0x00000be5                     @ 08026450 e50b0000
DWORD_08026454:
    .word  game_str_pointer_table         @ 08026454 400f0008
DWORD_08026458:
    .word  0x02000000                     @ 08026458 00000002
DWORD_0802645c:
    .word  0x00006c2c                     @ 0802645c 2c6c0000
DWORD_08026460:
    .word  game_str_ja                    @ 08026460 109cdb09
DWORD_08026464:
    .word  0x000007c7                     @ 08026464 c7070000
DWORD_08026468:
    .word  0x00000f09                     @ 08026468 090f0000
DWORD_0802646c:
    .word  0x00000bc1                     @ 0802646c c10b0000
DWORD_08026470:
    .word  0x09b96514                     @ 08026470 1465b909
DWORD_08026474:
    .word  0x00000bff                     @ 08026474 ff0b0000
DWORD_08026478:
    .word  0x000003ff                     @ 08026478 ff030000
DWORD_0802647c:
    .word  0x06000800                     @ 0802647c 00080006
DWORD_08026480:
    .word  0xfffffc00                     @ 08026480 00fcffff
DWORD_08026484:
    .word  0x06001100                     @ 08026484 00110006
LAB_08026488:
    ldr r2, DWORD_0802655c                   @ 08026488 344a
    ldr r0, DWORD_08026560                   @ 0802648a 3548
    strh r0,[r2,#0x6]                        @ 0802648c d080
    movs r0,#0x10    @ 0802648e 1020
    rsbs r0,r0,#0    @ 08026490 4042
    ldrb r1,[r2,#0x5]                        @ 08026492 5179
    ands r0,r1    @ 08026494 0840
    movs r1,#0x8    @ 08026496 0821
    orrs r0,r1    @ 08026498 0843
    strb r0,[r2,#0x5]                        @ 0802649a 5071
    movs r0,#0xe0    @ 0802649c e020
    ldrb r2,[r2,#0x4]                        @ 0802649e 1279
    ands r0,r2    @ 080264a0 1040
    cmp r0,#0x40                             @ 080264a2 4028
    bne LAB_080264fe                         @ 080264a4 2bd1
    movs r0,#0xbe    @ 080264a6 be20
    lsls r0,r0,#0x4    @ 080264a8 0001
    bl game_str_id_to_row                    @ 080264aa cef0b5fc
    ldr r2, DWORD_08026564                   @ 080264ae 2d4a
    lsls r0,r0,#0x10    @ 080264b0 0004
    lsrs r0,r0,#0x10    @ 080264b2 000c
    lsls r1,r0,#0x1    @ 080264b4 4100
    adds r1,r1,r0    @ 080264b6 0918
    lsls r1,r1,#0x1    @ 080264b8 4900
    ldr r0, DWORD_08026568                   @ 080264ba 2b48
    ldr r3, DWORD_0802656c                   @ 080264bc 2b4b
    adds r0,r0,r3    @ 080264be c018
    ldrb r0,[r0,#0x0]                        @ 080264c0 0078
    lsls r0,r0,#0x1d    @ 080264c2 4007
    lsrs r0,r0,#0x1d    @ 080264c4 400f
    adds r1,r1,r0    @ 080264c6 0918
    lsls r1,r1,#0x2    @ 080264c8 8900
    adds r1,r1,r2    @ 080264ca 8918
    ldr r1,[r1,#0x0]                         @ 080264cc 0968
    ldr r0, DWORD_08026570                   @ 080264ce 2848
    adds r1,r1,r0    @ 080264d0 0918
    ldr r0, DWORD_08026574                   @ 080264d2 2848
    movs r2,#0x84    @ 080264d4 8422
    lsls r2,r2,#0x2    @ 080264d6 9200
    ldr r3, DWORD_08026578                   @ 080264d8 274b
    str r1,[sp,#0x0]                         @ 080264da 0091
    movs r1,#0x36    @ 080264dc 3621
    bl render_centered_text_to_bg_vram       @ 080264de fdf759fa
    ldr r0, DWORD_0802657c                   @ 080264e2 2648
    ldr r3, DWORD_08026580                   @ 080264e4 264b
    movs r1,#0x20    @ 080264e6 2021
    movs r2,#0xf6    @ 080264e8 f622
    bl write_tile_row_to_vram                @ 080264ea c7f02ffd
    ldr r0, DWORD_08026584                   @ 080264ee 2548
    movs r1,#0x80    @ 080264f0 8021
    bl zero_fill_by_halfword                 @ 080264f2 cef0bffc
    ldr r0, DWORD_08026588                   @ 080264f6 2448
    movs r1,#0x80    @ 080264f8 8021
    bl zero_fill_by_halfword                 @ 080264fa cef0bbfc
LAB_080264fe:
    ldr r4, DWORD_0802655c                   @ 080264fe 174c
    ldrh r5,[r4,#0x2]                        @ 08026500 6588
    lsls r0,r5,#0x16    @ 08026502 a805
    lsrs r5,r0,#0x1b    @ 08026504 c50e
    adds r0,r5,#0x0    @ 08026506 281c
    movs r1,#0x5    @ 08026508 0521
    bl __umodsi3                             @ 0802650a e8f0a3f9
    lsls r0,r0,#0x10    @ 0802650e 0004
    lsrs r0,r0,#0x10    @ 08026510 000c
    subs r0,r5,r0    @ 08026512 281a
    movs r7,#0x0    @ 08026514 0027
    ldrh r4,[r4,#0x0]                        @ 08026516 2488
    cmp r0,r4                                @ 08026518 a042
    bge LAB_080265c2                         @ 0802651a 52da
    ldr r6, DWORD_0802658c                   @ 0802651c 1b4e
    .hword 0x46b1    @ 0802651e b146
    adds r5,r0,#0x0    @ 08026520 051c
    adds r1,r5,#0x0    @ 08026522 291c
    adds r1,#0xa    @ 08026524 0a31
    ldr r0, DWORD_08026590                   @ 08026526 1a48
    .hword 0x4680    @ 08026528 8046
    lsls r0,r1,#0x3    @ 0802652a c800
    adds r0,r0,r1    @ 0802652c 4018
    lsls r6,r0,#0x5    @ 0802652e 4601
    lsls r1,r1,#0x5    @ 08026530 4901
    .hword 0x4642    @ 08026532 4246
    adds r4,r1,r2    @ 08026534 8c18
LAB_08026536:
    cmp r5,#0x19                             @ 08026536 192d
    bne LAB_08026598                         @ 08026538 2ed1
    .hword 0x464b    @ 0802653a 4b46
    ldrb r3,[r3,#0x0]                        @ 0802653c 1b78
    lsls r0,r3,#0x19    @ 0802653e 5806
    lsrs r1,r0,#0x1c    @ 08026540 010f
    lsls r1,r1,#0x5    @ 08026542 4901
    add r1,r8                                @ 08026544 4144
    lsrs r0,r0,#0x1c    @ 08026546 000f
    lsls r2,r0,#0x3    @ 08026548 c200
    adds r2,r2,r0    @ 0802654a 1218
    lsls r2,r2,#0x5    @ 0802654c 5201
    ldr r0, DWORD_08026594                   @ 0802654e 1148
    adds r2,r2,r0    @ 08026550 1218
    movs r0,#0xa    @ 08026552 0a20
    bl copy_icon_tile_to_vram_row            @ 08026554 fdf7e6fa
    b LAB_080265aa                           @ 08026558 27e0
    .zero  0x2
DWORD_0802655c:
    .word  0x02023360                     @ 0802655c 60330202
DWORD_08026560:
    .word  0x0000ffff                     @ 08026560 ffff0000
DWORD_08026564:
    .word  game_str_pointer_table         @ 08026564 400f0008
DWORD_08026568:
    .word  0x02000000                     @ 08026568 00000002
DWORD_0802656c:
    .word  0x00006c2c                     @ 0802656c 2c6c0000
DWORD_08026570:
    .word  game_str_ja                    @ 08026570 109cdb09
DWORD_08026574:
    .word  0x00000407                     @ 08026574 07040000
DWORD_08026578:
    .word  0x00000f09                     @ 08026578 090f0000
DWORD_0802657c:
    .word  0x00000801                     @ 0802657c 01080000
DWORD_08026580:
    .word  0x09b953b4                     @ 08026580 b453b909
DWORD_08026584:
    .word  0x06001780                     @ 08026584 80170006
DWORD_08026588:
    .word  0x06000f80                     @ 08026588 800f0006
DWORD_0802658c:
    .word  gPlayerIcon                    @ 0802658c 576e0002
DWORD_08026590:
    .word  icon_palettes_base             @ 08026590 90628909
DWORD_08026594:
    .word  icon_tiles_base                @ 08026594 30cf8809
LAB_08026598:
    adds r0,r5,#0x0    @ 08026598 281c
    movs r1,#0xf    @ 0802659a 0f21
    bl __modsi3                              @ 0802659c e8f07ef8
    ldr r2, DWORD_08026624                   @ 080265a0 204a
    adds r2,r6,r2    @ 080265a2 b218
    adds r1,r4,#0x0    @ 080265a4 211c
    bl copy_icon_tile_to_vram_row            @ 080265a6 fdf7bdfa
LAB_080265aa:
    adds r5,#0x1    @ 080265aa 0135
    movs r0,#0x90    @ 080265ac 9020
    lsls r0,r0,#0x1    @ 080265ae 4000
    adds r6,r6,r0    @ 080265b0 3618
    adds r4,#0x20    @ 080265b2 2034
    adds r7,#0x1    @ 080265b4 0137
    cmp r7,#0x4                              @ 080265b6 042f
    bgt LAB_080265c2                         @ 080265b8 03dc
    ldr r0, DWORD_08026628                   @ 080265ba 1b48
    ldrh r0,[r0,#0x0]                        @ 080265bc 0088
    cmp r5,r0                                @ 080265be 8542
    blt LAB_08026536                         @ 080265c0 b9db
LAB_080265c2:
    ldr r4, DWORD_08026628                   @ 080265c2 194c
    ldrh r1,[r4,#0x0]                        @ 080265c4 2188
    cmp r1,#0x1                              @ 080265c6 0129
    bne LAB_080265d4                         @ 080265c8 04d1
    movs r0,#0x2    @ 080265ca 0220
    rsbs r0,r0,#0    @ 080265cc 4042
    ldrb r2,[r4,#0x8]                        @ 080265ce 227a
    ands r0,r2    @ 080265d0 1040
    strb r0,[r4,#0x8]                        @ 080265d2 2072
LAB_080265d4:
    ldrb r1,[r4,#0x8]                        @ 080265d4 217a
    movs r6,#0x1    @ 080265d6 0126
    adds r0,r6,#0x0    @ 080265d8 301c
    ands r0,r1    @ 080265da 0840
    cmp r0,#0x0                              @ 080265dc 0028
    beq LAB_080265ee                         @ 080265de 06d0
    movs r0,#0x3    @ 080265e0 0320
    rsbs r0,r0,#0    @ 080265e2 4042
    ands r0,r1    @ 080265e4 0840
    movs r1,#0x5    @ 080265e6 0521
    rsbs r1,r1,#0    @ 080265e8 4942
    ands r0,r1    @ 080265ea 0840
    strb r0,[r4,#0x8]                        @ 080265ec 2072
LAB_080265ee:
    bl render_opp_wins_display_oam           @ 080265ee fdf791fd
    movs r0,#0xf    @ 080265f2 0f20
    ldrb r3,[r4,#0x5]                        @ 080265f4 6379
    ands r0,r3    @ 080265f6 1840
    cmp r0,#0x0                              @ 080265f8 0028
    beq LAB_080265fe                         @ 080265fa 00d0
    b SUB_08026714                           @ 080265fc 8ae0
LAB_080265fe:
    ldr r5, DWORD_0802662c                   @ 080265fe 0b4d
    movs r1,#0xa4    @ 08026600 a421
    lsls r1,r1,#0x1    @ 08026602 4900
    adds r0,r5,r1    @ 08026604 6818
    ldrh r1,[r0,#0x0]                        @ 08026606 0188
    movs r0,#0x2    @ 08026608 0220
    ands r0,r1    @ 0802660a 0840
    cmp r0,#0x0                              @ 0802660c 0028
    beq LAB_08026638                         @ 0802660e 13d0
    movs r0,#0x1    @ 08026610 0120
    bl sync_state_and_init_sprite            @ 08026612 d3f04ffa
    ldr r2, DWORD_08026630                   @ 08026616 064a
    adds r0,r5,r2    @ 08026618 a818
    ldr r1, DWORD_08026634                   @ 0802661a 0649
    ldrh r3,[r0,#0x0]                        @ 0802661c 0388
    ands r1,r3    @ 0802661e 1940
    movs r2,#0xc0    @ 08026620 c022
    b LAB_08026c56                           @ 08026622 18e3
DWORD_08026624:
    .word  icon_tiles_base                @ 08026624 30cf8809
DWORD_08026628:
    .word  0x02023360                     @ 08026628 60330202
DWORD_0802662c:
    .word  gPrng                          @ 0802662c 40000003
DWORD_08026630:
    .word  0x00000202                     @ 08026630 02020000
DWORD_08026634:
    .word  0xffffc03f                     @ 08026634 3fc0ffff
LAB_08026638:
    adds r0,r6,#0x0    @ 08026638 301c
    ands r0,r1    @ 0802663a 0840
    cmp r0,#0x0                              @ 0802663c 0028
    beq SUB_08026714                         @ 0802663e 69d0
    ldr r2, DWORD_080266a8                   @ 08026640 194a
    ldr r0, DWORD_080266ac                   @ 08026642 1a48
    adds r2,r2,r0    @ 08026644 1218
    ldrb r1,[r4,#0x2]                        @ 08026646 a178
    lsls r0,r1,#0x1b    @ 08026648 c806
    lsrs r0,r0,#0x1b    @ 0802664a c00e
    adds r1,r6,#0x0    @ 0802664c 311c
    lsls r1,r0    @ 0802664e 8140
    ldr r0,[r2,#0x0]                         @ 08026650 1068
    ands r0,r1    @ 08026652 0840
    cmp r0,#0x0                              @ 08026654 0028
    beq SUB_08026714                         @ 08026656 5dd0
    movs r0,#0x24    @ 08026658 2420
    bl sync_state_and_init_sprite            @ 0802665a d3f02bfa
    ldr r2, DWORD_080266b0                   @ 0802665e 144a
    adds r1,r5,r2    @ 08026660 a918
    movs r0,#0x3f    @ 08026662 3f20
    ldrb r3,[r1,#0x0]                        @ 08026664 0b78
    ands r0,r3    @ 08026666 1840
    strb r0,[r1,#0x0]                        @ 08026668 0870
    movs r6,#0x81    @ 0802666a 8126
    lsls r6,r6,#0x2    @ 0802666c b600
    adds r1,r5,r6    @ 0802666e a919
    movs r0,#0x40    @ 08026670 4020
    rsbs r0,r0,#0    @ 08026672 4042
    ldrb r2,[r1,#0x0]                        @ 08026674 0a78
    ands r0,r2    @ 08026676 1040
    strb r0,[r1,#0x0]                        @ 08026678 0870
    ldr r3, DWORD_080266b4                   @ 0802667a 0e4b
    adds r1,r5,r3    @ 0802667c e918
    ldr r3, DWORD_080266b8                   @ 0802667e 0e4b
    adds r2,r3,#0x0    @ 08026680 1a1c
    ldrh r5,[r1,#0x0]                        @ 08026682 0d88
    ands r2,r5    @ 08026684 2a40
    movs r6,#0x80    @ 08026686 8026
    lsls r6,r6,#0x1    @ 08026688 7600
    adds r0,r6,#0x0    @ 0802668a 301c
    orrs r2,r0    @ 0802668c 0243
    strh r2,[r1,#0x0]                        @ 0802668e 0a80
    movs r0,#0x1f    @ 08026690 1f20
    ldrb r4,[r4,#0x2]                        @ 08026692 a478
    ands r0,r4    @ 08026694 2040
    cmp r0,#0x1a                             @ 08026696 1a28
    bne SUB_08026714                         @ 08026698 3cd1
    ands r2,r3    @ 0802669a 1a40
    movs r3,#0xa0    @ 0802669c a023
    lsls r3,r3,#0x1    @ 0802669e 5b00
    adds r0,r3,#0x0    @ 080266a0 181c
    orrs r2,r0    @ 080266a2 0243
    strh r2,[r1,#0x0]                        @ 080266a4 0a80
    b SUB_08026714                           @ 080266a6 35e0
DWORD_080266a8:
    .word  0x02000000                     @ 080266a8 00000002
DWORD_080266ac:
    .word  0x00006e5c                     @ 080266ac 5c6e0000
DWORD_080266b0:
    .word  0x00000203                     @ 080266b0 03020000
DWORD_080266b4:
    .word  0x00000202                     @ 080266b4 02020000
DWORD_080266b8:
    .word  0xffffc03f                     @ 080266b8 3fc0ffff

@ Per-frame tick handler for campaign_scene_handler dispatch table index 3. Trigger: gPrng+0x202 bits[13:6] == 0x03. Calls render_opp_wins_display_oam to refresh opponent wins sprites, then calls start_blend_fadein_with_target(4) to advance fadein. If fadein returns 0 (not done) tail-calls b SUB_08026714 to wait; if done (nonzero) calls SUB_08027768 (trigger scene-enter complete event) then tail-calls SUB_08026714 to advance.
@ 
@ Constants:
@ - step_index=3
@ - fadein_target=4
run_campaign_step3_opp_wins_fadein_tick:
    bl render_opp_wins_display_oam           @ 080266bc fdf72afd
    movs r0,#0x4    @ 080266c0 0420
    bl start_blend_fadein_with_target        @ 080266c2 cff0bdf8
    cmp r0,#0x0                              @ 080266c6 0028
    beq LAB_080266ce                         @ 080266c8 01d0
    bl SUB_08027768                          @ 080266ca 01f04df8
LAB_080266ce:
    b SUB_08026714                           @ 080266ce 21e0

@ campaign_scene_handler dispatch table index 4. Trigger: gPrng+0x202 bits[13:6] == 0x04. Sequence: (1) bl render_opp_wins_display_oam; (2) reads gPrng+0x203 bits[7:6] and gPrng+0x204 bits[5:0] to form frame_counter r0; (3) if r0 <= 0x1d (29): increments frame_counter, writes back split across +0x203/+0x204, then bl start_blend_fadein_with_target(4); if blend returns nonzero (complete) advances scene step via LAB_08026c56; (4) if r0 > 0x1d: directly bl start_blend_fadein_with_target(4) and waits.
@ 
@ Constants:
@ - frame_counter_max = 0x1d (29)
@ - blend_target = 4
@ - gPrng_frame_ctr = gPrng+0x203 bits[7:6] | gPrng+0x204 bits[5:0]
@ - gPrng_frame_mask = 0xffffc03f
run_campaign_step4_wins_and_blend_tick:
    bl render_opp_wins_display_oam           @ 080266d0 fdf720fd
    ldr r4, DWORD_0802671c                   @ 080266d4 114c
    ldr r5, DWORD_08026720                   @ 080266d6 124d
    adds r7,r4,r5    @ 080266d8 6719
    ldrb r6,[r7,#0x0]                        @ 080266da 3e78
    lsrs r1,r6,#0x6    @ 080266dc b109
    movs r0,#0x81    @ 080266de 8120
    lsls r0,r0,#0x2    @ 080266e0 8000
    adds r5,r4,r0    @ 080266e2 2518
    movs r3,#0x3f    @ 080266e4 3f23
    adds r0,r3,#0x0    @ 080266e6 181c
    ldrb r2,[r5,#0x0]                        @ 080266e8 2a78
    ands r0,r2    @ 080266ea 1040
    lsls r0,r0,#0x2    @ 080266ec 8000
    orrs r0,r1    @ 080266ee 0843
    cmp r0,#0x1d                             @ 080266f0 1d28
    bhi LAB_08026724                         @ 080266f2 17d8
    adds r2,r0,#0x1    @ 080266f4 421c
    movs r1,#0x3    @ 080266f6 0321
    ands r1,r2    @ 080266f8 1140
    lsls r1,r1,#0x6    @ 080266fa 8901
    adds r0,r3,#0x0    @ 080266fc 181c
    ands r0,r6    @ 080266fe 3040
    orrs r0,r1    @ 08026700 0843
    strb r0,[r7,#0x0]                        @ 08026702 3870
    lsrs r2,r2,#0x2    @ 08026704 9208
    ands r2,r3    @ 08026706 1a40
    movs r0,#0x40    @ 08026708 4020
    rsbs r0,r0,#0    @ 0802670a 4042
    ldrb r3,[r5,#0x0]                        @ 0802670c 2b78
    ands r0,r3    @ 0802670e 1840
    orrs r0,r2    @ 08026710 1043
    strb r0,[r5,#0x0]                        @ 08026712 2870
SUB_08026714:
    movs r0,#0x80    @ 08026714 8020
    lsls r0,r0,#0x1    @ 08026716 4000
    bl SUB_08027c82                          @ 08026718 01f0b3fa
DWORD_0802671c:
    .word  gPrng                          @ 0802671c 40000003
DWORD_08026720:
    .word  0x00000203                     @ 08026720 03020000
LAB_08026724:
    movs r0,#0x4    @ 08026724 0420
    bl start_blend_fadein_with_target        @ 08026726 cff08bf8
    cmp r0,#0x0                              @ 0802672a 0028
    beq SUB_08026714                         @ 0802672c f2d0
    ldr r5, DWORD_08026740                   @ 0802672e 044d
    adds r0,r4,r5    @ 08026730 6019
    ldr r1, DWORD_08026744                   @ 08026732 0449
    ldrh r6,[r0,#0x0]                        @ 08026734 0688
    ands r1,r6    @ 08026736 3140
    movs r3,#0xa0    @ 08026738 a023
    lsls r3,r3,#0x3    @ 0802673a db00
    adds r2,r3,#0x0    @ 0802673c 1a1c
    b LAB_08026c56                           @ 0802673e 8ae2
DWORD_08026740:
    .word  0x00000202                     @ 08026740 02020000
DWORD_08026744:
    .word  0xffffc03f                     @ 08026744 3fc0ffff

@ Init handler for campaign_scene_handler dispatch table index 5. Trigger: gPrng+0x202 bits[13:6] == 0x05. Initializes pack-select VRAM and text: (1) zero_fill_by_halfword(0x06001180, 0x80*8=0x400 halfwords) clears BG tile region 1; (2) load_pack_tile_and_map_to_vram(0x840, 0x50, 0x148, 0x09b96c2c) loads pack tile and tilemap; (3) zero_fill_by_halfword(0x06000800, 0xc0*8=0x600 halfwords) clears BG tile region 2; (4) loop r4=0..6 calls render_text_with_font_type_select(r4) 7 times; (5) clears scene_ctx(0x02023360)+8 halfword and word high bits; (6) increments gPrng+0x202 frame counter bits[13:6] and tail-calls SUB_08026714.
@ 
@ Constants:
@ - step_index=5
@ - VRAM_clear_1=0x06001180 (0x80*8=0x400 halfwords)
@ - pack_tile_data_ptr=0x09b96c2c
@ - VRAM_clear_2=0x06000800 (0xc0*8=0x600 halfwords)
@ - pack_tile_dest=0x840=0x84*0x10
@ - pack_map_offset=0x148=0xa4*2
@ - text_line_count=7 (loop 0..6)
@ - scene_ctx=0x02023360
@ - frame_ctr_mask=0xffffc03f
run_campaign_step5_pack_vram_and_text_init:
    ldr r0, DWORD_08026808                   @ 08026748 2f48
    movs r1,#0x80    @ 0802674a 8021
    lsls r1,r1,#0x3    @ 0802674c c900
    bl zero_fill_by_halfword                 @ 0802674e cef091fb
    movs r0,#0x84    @ 08026752 8420
    lsls r0,r0,#0x4    @ 08026754 0001
    movs r2,#0xa4    @ 08026756 a422
    lsls r2,r2,#0x1    @ 08026758 5200
    ldr r3, DWORD_0802680c                   @ 0802675a 2c4b
    movs r1,#0x50    @ 0802675c 5021
    bl load_pack_tile_and_map_to_vram        @ 0802675e c7f057fc
    ldr r0, DWORD_08026810                   @ 08026762 2b48
    movs r1,#0xc0    @ 08026764 c021
    lsls r1,r1,#0x3    @ 08026766 c900
    bl zero_fill_by_halfword                 @ 08026768 cef084fb
    movs r4,#0x0    @ 0802676c 0024
LAB_0802676e:
    adds r0,r4,#0x0    @ 0802676e 201c
    bl render_text_with_font_type_select     @ 08026770 fef77af9
    adds r4,#0x1    @ 08026774 0134
    cmp r4,#0x6                              @ 08026776 062c
    ble LAB_0802676e                         @ 08026778 f9dd
    ldr r2, DWORD_08026814                   @ 0802677a 264a
    ldr r3, DWORD_08026818                   @ 0802677c 264b
    adds r0,r3,#0x0    @ 0802677e 181c
    ldrh r4,[r2,#0x8]                        @ 08026780 1489
    ands r0,r4    @ 08026782 2040
    strh r0,[r2,#0x8]                        @ 08026784 1081
    ldr r0,[r2,#0x8]                         @ 08026786 9068
    ldr r1, DWORD_0802681c                   @ 08026788 2449
    ands r0,r1    @ 0802678a 0840
    str r0,[r2,#0x8]                         @ 0802678c 9060
    adds r0,r3,#0x0    @ 0802678e 181c
    ldrh r5,[r2,#0xc]                        @ 08026790 9589
    ands r0,r5    @ 08026792 2840
    strh r0,[r2,#0xc]                        @ 08026794 9081
    ldrh r6,[r2,#0xa]                        @ 08026796 5689
    ands r3,r6    @ 08026798 3340
    strh r3,[r2,#0xa]                        @ 0802679a 5381
    movs r0,#0x7f    @ 0802679c 7f20
    ldrb r1,[r2,#0xb]                        @ 0802679e d17a
    ands r0,r1    @ 080267a0 0840
    strb r0,[r2,#0xb]                        @ 080267a2 d072
    movs r0,#0x80    @ 080267a4 8020
    rsbs r0,r0,#0    @ 080267a6 4042
    ldrb r3,[r2,#0xc]                        @ 080267a8 137b
    ands r0,r3    @ 080267aa 1840
    strb r0,[r2,#0xc]                        @ 080267ac 1073
    ldr r2, DWORD_08026820                   @ 080267ae 1c4a
    ldr r4, DWORD_08026824                   @ 080267b0 1c4c
    adds r2,r2,r4    @ 080267b2 1219
    ldrh r3,[r2,#0x0]                        @ 080267b4 1388
    lsls r1,r3,#0x12    @ 080267b6 9904
    lsrs r1,r1,#0x18    @ 080267b8 090e
    adds r1,#0x1    @ 080267ba 0131
    movs r0,#0xff    @ 080267bc ff20
    ands r1,r0    @ 080267be 0140
    lsls r1,r1,#0x6    @ 080267c0 8901
    ldr r0, DWORD_08026828                   @ 080267c2 1948
    ands r0,r3    @ 080267c4 1840
    orrs r0,r1    @ 080267c6 0843
    strh r0,[r2,#0x0]                        @ 080267c8 1080

@ Per-frame tick handler for campaign_scene_handler dispatch table index 6. Trigger: gPrng+0x202 bits[13:6] == 0x06. Calls render_opp_wins_display_oam to refresh opponent wins sprites. Reads scene_ctx(0x02023360)+8 word, extracts bits[22:15] as sprite_state [0..255]. If sprite_state > 7 jumps to LAB_08026830 (alternate update path writing gPrng+0x202 scaler then jumping to SUB_08027c22). Otherwise reads ROM table 0x09e59d18[sprite_state*4] as anim_code, writes (sprite_state+1)<<15 to scene_ctx+8 bits[22:15] and (anim_code&0xff)<<7 to bits[14:7], then tail-calls SUB_08026714.
@ 
@ Constants:
@ - step_index=6
@ - scene_ctx=0x02023360
@ - sprite_state=scene_ctx+8 bits[22:15] [0..7]
@ - anim_table=0x09e59d18 (ROM sprite animation code table)
@ - state_mask_clear=0xff807fff (clears bits[22:15])
@ - anim_mask_clear=0xffff807f (clears bits[14:7])
run_campaign_step6_opp_scroll_sprite_tick:
    bl render_opp_wins_display_oam           @ 080267ca fdf7a3fc
    ldr r6, DWORD_08026814                   @ 080267ce 114e
    ldr r5,[r6,#0x8]                         @ 080267d0 b568
    lsls r4,r5,#0x9    @ 080267d2 6c02
    lsrs r0,r4,#0x18    @ 080267d4 200e
    cmp r0,#0x7                              @ 080267d6 0728
    bhi LAB_08026830                         @ 080267d8 2ad8
    ldr r3, DWORD_0802682c                   @ 080267da 144b
    adds r1,r0,#0x0    @ 080267dc 011c
    adds r1,#0x1    @ 080267de 0131
    movs r2,#0xff    @ 080267e0 ff22
    ands r1,r2    @ 080267e2 1140
    lsls r1,r1,#0xf    @ 080267e4 c903
    ldr r0, DWORD_0802681c                   @ 080267e6 0d48
    ands r0,r5    @ 080267e8 2840
    orrs r0,r1    @ 080267ea 0843
    str r0,[r6,#0x8]                         @ 080267ec b060
    lsrs r0,r4,#0x18    @ 080267ee 200e
    lsls r0,r0,#0x2    @ 080267f0 8000
    adds r0,r0,r3    @ 080267f2 c018
    ldr r1,[r0,#0x0]                         @ 080267f4 0168
    ands r1,r2    @ 080267f6 1140
    lsls r1,r1,#0x7    @ 080267f8 c901
    ldr r0, DWORD_08026818                   @ 080267fa 0748
    ldrh r5,[r6,#0x8]                        @ 080267fc 3589
    ands r0,r5    @ 080267fe 2840
    orrs r0,r1    @ 08026800 0843
    strh r0,[r6,#0x8]                        @ 08026802 3081
    b SUB_08026714                           @ 08026804 86e7
    .zero  0x2
DWORD_08026808:
    .word  0x06001180                     @ 08026808 80110006
DWORD_0802680c:
    .word  0x09b96c2c                     @ 0802680c 2c6cb909
DWORD_08026810:
    .word  0x06000800                     @ 08026810 00080006
DWORD_08026814:
    .word  0x02023360                     @ 08026814 60330202
DWORD_08026818:
    .word  0xffff807f                     @ 08026818 7f80ffff
DWORD_0802681c:
    .word  0xff807fff                     @ 0802681c ff7f80ff
DWORD_08026820:
    .word  gPrng                          @ 08026820 40000003
DWORD_08026824:
    .word  0x00000202                     @ 08026824 02020000
DWORD_08026828:
    .word  0xffffc03f                     @ 08026828 3fc0ffff
DWORD_0802682c:
    .word  0x09e59d18                     @ 0802682c 189de509
LAB_08026830:
    ldr r2, DWORD_0802684c                   @ 08026830 064a
    ldr r6, DWORD_08026850                   @ 08026832 074e
    adds r2,r2,r6    @ 08026834 9219
    ldrh r3,[r2,#0x0]                        @ 08026836 1388
    lsls r1,r3,#0x12    @ 08026838 9904
    lsrs r1,r1,#0x18    @ 0802683a 090e
    adds r1,#0x1    @ 0802683c 0131
    movs r0,#0xff    @ 0802683e ff20
    ands r1,r0    @ 08026840 0140
    lsls r1,r1,#0x6    @ 08026842 8901
    ldr r0, DWORD_08026854                   @ 08026844 0348
    ands r0,r3    @ 08026846 1840
    bl SUB_08027c22                          @ 08026848 01f0ebf9
DWORD_0802684c:
    .word  gPrng                          @ 0802684c 40000003
DWORD_08026850:
    .word  0x00000202                     @ 08026850 02020000
DWORD_08026854:
    .word  0xffffc03f                     @ 08026854 3fc0ffff

@ campaign_scene_handler dispatch table index 7. Trigger: gPrng+0x202 bits[13:6] == 0x07. Sequence: (1) bl render_opp_wins_display_oam; (2) checks gPrng+0x148 bit6 (0x40): if set, reads scene_ctx+0xc halfword, extracts row offset index, if at limit decrements by 1 and bl render_text_with_font_type_select; (3) bl sync_state_and_init_sprite(0); (4) checks bit7 (0x80) path for opposite scroll direction, if row index <= 0x3a then adds 6 and renders; (5) checks bit1 (0x2): if set clears scene_ctx+0xb/+0xc scroll fields; (6) if gPrng+0x148 bit0 == 0 waits via SUB_08026714, else bl sync_state_and_init_sprite(0x24) and advances step.
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - gPrng_scroll_reg = gPrng+0xa4*2 = gPrng+0x148
@ - bit6 = 0x40 (scroll up trigger), bit7 = 0x80 (scroll down trigger)
@ - bit1 = 0x2 (reset path), bit0 = 0x1 (advance scene)
@ - row_max_threshold = 0x3a (58), row_advance_step = 6
run_campaign_step7_scroll_text_tick:
    bl render_opp_wins_display_oam           @ 08026858 fdf75cfc
    ldr r1, DWORD_08026a10                   @ 0802685c 6c49
    movs r0,#0xa4    @ 0802685e a420
    lsls r0,r0,#0x1    @ 08026860 4000
    adds r1,r1,r0    @ 08026862 0918
    movs r0,#0x40    @ 08026864 4020
    ldrh r1,[r1,#0x0]                        @ 08026866 0988
    ands r0,r1    @ 08026868 0840
    cmp r0,#0x0                              @ 0802686a 0028
    beq LAB_080268e4                         @ 0802686c 3ad0
    ldr r4, DWORD_08026a14                   @ 0802686e 694c
    ldrh r1,[r4,#0xc]                        @ 08026870 a189
    movs r0,#0xff    @ 08026872 ff20
    lsls r0,r0,#0x7    @ 08026874 c001
    ands r0,r1    @ 08026876 0840
    cmp r0,#0x0                              @ 08026878 0028
    beq LAB_080268e4                         @ 0802687a 33d0
    lsls r0,r1,#0x11    @ 0802687c 4804
    ldrb r5,[r4,#0xb]                        @ 0802687e e57a
    lsrs r2,r5,#0x7    @ 08026880 ea09
    movs r3,#0x7f    @ 08026882 7f23
    adds r1,r3,#0x0    @ 08026884 191c
    ldrb r6,[r4,#0xc]                        @ 08026886 267b
    ands r1,r6    @ 08026888 3140
    lsls r1,r1,#0x1    @ 0802688a 4900
    orrs r1,r2    @ 0802688c 1143
    lsrs r0,r0,#0x18    @ 0802688e 000e
    cmp r0,r1                                @ 08026890 8842
    bne LAB_080268c8                         @ 08026892 19d1
    subs r2,r1,#0x1    @ 08026894 4a1e
    lsls r2,r2,#0x10    @ 08026896 1204
    lsrs r0,r2,#0x10    @ 08026898 100c
    movs r1,#0x1    @ 0802689a 0121
    ands r0,r1    @ 0802689c 0840
    lsls r0,r0,#0x7    @ 0802689e c001
    adds r1,r3,#0x0    @ 080268a0 191c
    ands r1,r5    @ 080268a2 2940
    orrs r1,r0    @ 080268a4 0143
    strb r1,[r4,#0xb]                        @ 080268a6 e172
    lsrs r2,r2,#0x11    @ 080268a8 520c
    ands r2,r3    @ 080268aa 1a40
    movs r0,#0x80    @ 080268ac 8020
    rsbs r0,r0,#0    @ 080268ae 4042
    adds r5,r6,#0x0    @ 080268b0 351c
    ands r0,r5    @ 080268b2 2840
    orrs r0,r2    @ 080268b4 1043
    strb r0,[r4,#0xc]                        @ 080268b6 2073
    lsrs r1,r1,#0x7    @ 080268b8 c909
    adds r0,r3,#0x0    @ 080268ba 181c
    ldrb r6,[r4,#0xc]                        @ 080268bc 267b
    ands r0,r6    @ 080268be 3040
    lsls r0,r0,#0x1    @ 080268c0 4000
    orrs r0,r1    @ 080268c2 0843
    bl render_text_with_font_type_select     @ 080268c4 fef7d0f8
LAB_080268c8:
    movs r0,#0x0    @ 080268c8 0020
    bl sync_state_and_init_sprite            @ 080268ca d3f0f3f8
    ldrh r2,[r4,#0xc]                        @ 080268ce a289
    lsls r1,r2,#0x11    @ 080268d0 5104
    lsrs r1,r1,#0x18    @ 080268d2 090e
    subs r1,#0x1    @ 080268d4 0139
    movs r0,#0xff    @ 080268d6 ff20
    ands r1,r0    @ 080268d8 0140
    lsls r1,r1,#0x7    @ 080268da c901
    ldr r0, DWORD_08026a18                   @ 080268dc 4e48
    ands r0,r2    @ 080268de 1040
    orrs r0,r1    @ 080268e0 0843
    strh r0,[r4,#0xc]                        @ 080268e2 a081
LAB_080268e4:
    ldr r1, DWORD_08026a10                   @ 080268e4 4a49
    movs r0,#0xa4    @ 080268e6 a420
    lsls r0,r0,#0x1    @ 080268e8 4000
    adds r1,r1,r0    @ 080268ea 0918
    movs r0,#0x80    @ 080268ec 8020
    ldrh r1,[r1,#0x0]                        @ 080268ee 0988
    ands r0,r1    @ 080268f0 0840
    cmp r0,#0x0                              @ 080268f2 0028
    beq LAB_0802696c                         @ 080268f4 3ad0
    ldr r4, DWORD_08026a14                   @ 080268f6 474c
    ldrh r1,[r4,#0xc]                        @ 080268f8 a189
    lsls r2,r1,#0x11    @ 080268fa 4a04
    lsrs r0,r2,#0x18    @ 080268fc 100e
    cmp r0,#0x3a                             @ 080268fe 3a28
    bhi LAB_0802696c                         @ 08026900 34d8
    adds r2,r0,#0x0    @ 08026902 021c
    ldrb r6,[r4,#0xb]                        @ 08026904 e67a
    lsrs r1,r6,#0x7    @ 08026906 f109
    movs r5,#0x7f    @ 08026908 7f25
    adds r0,r5,#0x0    @ 0802690a 281c
    ldrb r3,[r4,#0xc]                        @ 0802690c 237b
    ands r0,r3    @ 0802690e 1840
    lsls r3,r0,#0x1    @ 08026910 4300
    orrs r3,r1    @ 08026912 0b43
    adds r0,r3,#0x6    @ 08026914 981d
    cmp r2,r0                                @ 08026916 8242
    bne LAB_08026950                         @ 08026918 1ad1
    adds r2,r3,#0x1    @ 0802691a 5a1c
    lsls r2,r2,#0x10    @ 0802691c 1204
    lsrs r0,r2,#0x10    @ 0802691e 100c
    movs r1,#0x1    @ 08026920 0121
    ands r0,r1    @ 08026922 0840
    lsls r0,r0,#0x7    @ 08026924 c001
    adds r1,r5,#0x0    @ 08026926 291c
    ands r1,r6    @ 08026928 3140
    orrs r1,r0    @ 0802692a 0143
    strb r1,[r4,#0xb]                        @ 0802692c e172
    lsrs r2,r2,#0x11    @ 0802692e 520c
    ands r2,r5    @ 08026930 2a40
    movs r0,#0x80    @ 08026932 8020
    rsbs r0,r0,#0    @ 08026934 4042
    ldrb r6,[r4,#0xc]                        @ 08026936 267b
    ands r0,r6    @ 08026938 3040
    orrs r0,r2    @ 0802693a 1043
    strb r0,[r4,#0xc]                        @ 0802693c 2073
    lsrs r1,r1,#0x7    @ 0802693e c909
    adds r0,r5,#0x0    @ 08026940 281c
    ldrb r2,[r4,#0xc]                        @ 08026942 227b
    ands r0,r2    @ 08026944 1040
    lsls r0,r0,#0x1    @ 08026946 4000
    orrs r0,r1    @ 08026948 0843
    adds r0,#0x6    @ 0802694a 0630
    bl render_text_with_font_type_select     @ 0802694c fef78cf8
LAB_08026950:
    movs r0,#0x0    @ 08026950 0020
    bl sync_state_and_init_sprite            @ 08026952 d3f0aff8
    ldrh r2,[r4,#0xc]                        @ 08026956 a289
    lsls r1,r2,#0x11    @ 08026958 5104
    lsrs r1,r1,#0x18    @ 0802695a 090e
    adds r1,#0x1    @ 0802695c 0131
    movs r0,#0xff    @ 0802695e ff20
    ands r1,r0    @ 08026960 0140
    lsls r1,r1,#0x7    @ 08026962 c901
    ldr r0, DWORD_08026a18                   @ 08026964 2c48
    ands r0,r2    @ 08026966 1040
    orrs r0,r1    @ 08026968 0843
    strh r0,[r4,#0xc]                        @ 0802696a a081
LAB_0802696c:
    ldr r4, DWORD_08026a10                   @ 0802696c 284c
    movs r3,#0xa4    @ 0802696e a423
    lsls r3,r3,#0x1    @ 08026970 5b00
    adds r6,r4,r3    @ 08026972 e618
    movs r0,#0x2    @ 08026974 0220
    ldrh r5,[r6,#0x0]                        @ 08026976 3588
    ands r0,r5    @ 08026978 2840
    cmp r0,#0x0                              @ 0802697a 0028
    beq LAB_080269c4                         @ 0802697c 22d0
    ldr r2, DWORD_08026a14                   @ 0802697e 254a
    movs r0,#0x7f    @ 08026980 7f20
    ldrb r1,[r2,#0xb]                        @ 08026982 d17a
    ands r0,r1    @ 08026984 0840
    strb r0,[r2,#0xb]                        @ 08026986 d072
    movs r0,#0x80    @ 08026988 8020
    rsbs r0,r0,#0    @ 0802698a 4042
    ldrb r3,[r2,#0xc]                        @ 0802698c 137b
    ands r0,r3    @ 0802698e 1840
    strb r0,[r2,#0xc]                        @ 08026990 1073
    ldrh r5,[r2,#0x8]                        @ 08026992 1589
    lsrs r1,r5,#0x7    @ 08026994 e909
    lsls r1,r1,#0x18    @ 08026996 0906
    lsrs r1,r1,#0x18    @ 08026998 090e
    ldrb r0,[r2,#0x3]                        @ 0802699a d078
    lsrs r3,r0,#0x5    @ 0802699c 4309
    movs r0,#0x1f    @ 0802699e 1f20
    ldrb r2,[r2,#0x4]                        @ 080269a0 1279
    ands r0,r2    @ 080269a2 1040
    lsls r0,r0,#0x3    @ 080269a4 c000
    orrs r0,r3    @ 080269a6 1843
    subs r1,r1,r0    @ 080269a8 091a
    movs r2,#0xf5    @ 080269aa f522
    lsls r2,r2,#0x1    @ 080269ac 5200
    adds r0,r4,r2    @ 080269ae a018
    strh r1,[r0,#0x0]                        @ 080269b0 0180
    ldr r3, DWORD_08026a1c                   @ 080269b2 1a4b
    adds r2,r4,r3    @ 080269b4 e218
    ldr r0, DWORD_08026a20                   @ 080269b6 1a48
    ldrh r5,[r2,#0x0]                        @ 080269b8 1588
    ands r0,r5    @ 080269ba 2840
    adds r3,#0x7e    @ 080269bc 7e33
    adds r1,r3,#0x0    @ 080269be 191c
    orrs r0,r1    @ 080269c0 0843
    strh r0,[r2,#0x0]                        @ 080269c2 1080
LAB_080269c4:
    movs r5,#0x1    @ 080269c4 0125
    adds r0,r5,#0x0    @ 080269c6 281c
    ldrh r6,[r6,#0x0]                        @ 080269c8 3688
    ands r0,r6    @ 080269ca 3040
    cmp r0,#0x0                              @ 080269cc 0028
    bne LAB_080269d2                         @ 080269ce 00d1
    b SUB_08026714                           @ 080269d0 a0e6
LAB_080269d2:
    ldr r1, DWORD_08026a24                   @ 080269d2 1449
    ldr r0, DWORD_08026a14                   @ 080269d4 0f48
    ldrh r0,[r0,#0xc]                        @ 080269d6 8089
    lsls r2,r0,#0x11    @ 080269d8 4204
    lsrs r3,r2,#0x1d    @ 080269da 530f
    lsls r3,r3,#0x2    @ 080269dc 9b00
    ldr r6, DWORD_08026a28                   @ 080269de 124e
    adds r1,r1,r6    @ 080269e0 8919
    adds r3,r3,r1    @ 080269e2 5b18
    lsrs r2,r2,#0x18    @ 080269e4 120e
    movs r0,#0x1f    @ 080269e6 1f20
    ands r2,r0    @ 080269e8 0240
    adds r1,r5,#0x0    @ 080269ea 291c
    lsls r1,r2    @ 080269ec 9140
    ldr r0,[r3,#0x0]                         @ 080269ee 1868
    ands r0,r1    @ 080269f0 0840
    cmp r0,#0x0                              @ 080269f2 0028
    bne LAB_080269f8                         @ 080269f4 00d1
    b SUB_08026714                           @ 080269f6 8de6
LAB_080269f8:
    movs r0,#0x24    @ 080269f8 2420
    bl sync_state_and_init_sprite            @ 080269fa d3f05bf8
    ldr r1, DWORD_08026a1c                   @ 080269fe 0749
    adds r0,r4,r1    @ 08026a00 6018
    ldr r1, DWORD_08026a20                   @ 08026a02 0749
    ldrh r2,[r0,#0x0]                        @ 08026a04 0288
    ands r1,r2    @ 08026a06 1140
    movs r3,#0x80    @ 08026a08 8023
    lsls r3,r3,#0x1    @ 08026a0a 5b00
    adds r2,r3,#0x0    @ 08026a0c 1a1c
    b LAB_08026c56                           @ 08026a0e 22e1
DWORD_08026a10:
    .word  gPrng                          @ 08026a10 40000003
DWORD_08026a14:
    .word  0x02023360                     @ 08026a14 60330202
DWORD_08026a18:
    .word  0xffff807f                     @ 08026a18 7f80ffff
DWORD_08026a1c:
    .word  0x00000202                     @ 08026a1c 02020000
DWORD_08026a20:
    .word  0xffffc03f                     @ 08026a20 3fc0ffff
DWORD_08026a24:
    .word  0x02000000                     @ 08026a24 00000002
DWORD_08026a28:
    .word  0x000053f0                     @ 08026a28 f0530000

@ Per-frame handler for campaign_scene_handler dispatch table index 10. Trigger: gPrng+0x202 bits[13:6] == 0x0a. Sequence: (1) call sync_state_and_init_sprite(1) to reset sprite state; (2) call game_str_id_to_row(0x0be4) and render_centered_text_to_bg_vram to render opponent card name row 1; (3) call write_tile_row_to_vram for separator tile row; (4) call game_str_id_to_row(0x0be5) and render_centered_text_to_bg_vram for row 2; (5) call write_tile_row_to_vram for second separator; (6) zero_fill_by_halfword(0x06000d80, 0x80) and zero_fill_by_halfword(0x06000900, 0x80); (7) clear scene_ctx+8 high bits with 0xff807fff mask; (8) increment gPrng+0x202 frame counter bits[13:6].
@ 
@ Constants:
@ - scene_ctx=0x02023360
@ - game_str_id_opponent_name_1=0x0be4
@ - game_str_id_opponent_name_2=0x0be5
@ - VRAM_clear_1=0x06000d80 (0x80 halfwords)
@ - VRAM_clear_2=0x06000900 (0x80 halfwords)
@ - gPrng_frame_ctr=gPrng+0x202 bits[13:6]
@ - mask_clear=0xff807fff (clears bits[14:15])
@ - frame_ctr_mask=0xffffc03f
run_campaign_step10_render_opponent_card_names:
    movs r0,#0x1    @ 08026a2c 0120
    bl sync_state_and_init_sprite            @ 08026a2e d3f041f8
    ldr r0, DWORD_08026b34                   @ 08026a32 4048
    bl game_str_id_to_row                    @ 08026a34 cef0f0f9
    ldr r4, DWORD_08026b38                   @ 08026a38 3f4c
    .hword 0x46a1    @ 08026a3a a146
    lsls r0,r0,#0x10    @ 08026a3c 0004
    lsrs r0,r0,#0x10    @ 08026a3e 000c
    lsls r1,r0,#0x1    @ 08026a40 4100
    adds r1,r1,r0    @ 08026a42 0918
    lsls r1,r1,#0x1    @ 08026a44 4900
    ldr r4, DWORD_08026b3c                   @ 08026a46 3d4c
    ldr r5, DWORD_08026b40                   @ 08026a48 3d4d
    adds r4,r4,r5    @ 08026a4a 6419
    ldrb r6,[r4,#0x0]                        @ 08026a4c 2678
    lsls r0,r6,#0x1d    @ 08026a4e 7007
    lsrs r0,r0,#0x1d    @ 08026a50 400f
    adds r1,r1,r0    @ 08026a52 0918
    lsls r1,r1,#0x2    @ 08026a54 8900
    add r1,r9                                @ 08026a56 4944
    ldr r1,[r1,#0x0]                         @ 08026a58 0968
    ldr r5, DWORD_08026b44                   @ 08026a5a 3a4d
    adds r1,r1,r5    @ 08026a5c 4919
    ldr r0, DWORD_08026b48                   @ 08026a5e 3a48
    movs r6,#0x84    @ 08026a60 8426
    lsls r6,r6,#0x2    @ 08026a62 b600
    ldr r2, DWORD_08026b4c                   @ 08026a64 394a
    .hword 0x4690    @ 08026a66 9046
    str r1,[sp,#0x0]                         @ 08026a68 0091
    movs r1,#0xb6    @ 08026a6a b621
    adds r2,r6,#0x0    @ 08026a6c 321c
    .hword 0x4643    @ 08026a6e 4346
    bl render_centered_text_to_bg_vram       @ 08026a70 fcf790ff
    ldr r0, DWORD_08026b50                   @ 08026a74 3648
    ldr r3, DWORD_08026b54                   @ 08026a76 374b
    movs r1,#0x20    @ 08026a78 2021
    movs r2,#0xf6    @ 08026a7a f622
    bl write_tile_row_to_vram                @ 08026a7c c7f066fa
    ldr r0, DWORD_08026b58                   @ 08026a80 3548
    bl game_str_id_to_row                    @ 08026a82 cef0c9f9
    lsls r0,r0,#0x10    @ 08026a86 0004
    lsrs r0,r0,#0x10    @ 08026a88 000c
    lsls r1,r0,#0x1    @ 08026a8a 4100
    adds r1,r1,r0    @ 08026a8c 0918
    lsls r1,r1,#0x1    @ 08026a8e 4900
    ldrb r4,[r4,#0x0]                        @ 08026a90 2478
    lsls r0,r4,#0x1d    @ 08026a92 6007
    lsrs r0,r0,#0x1d    @ 08026a94 400f
    adds r1,r1,r0    @ 08026a96 0918
    lsls r1,r1,#0x2    @ 08026a98 8900
    add r1,r9                                @ 08026a9a 4944
    ldr r1,[r1,#0x0]                         @ 08026a9c 0968
    adds r1,r1,r5    @ 08026a9e 4919
    ldr r0, DWORD_08026b5c                   @ 08026aa0 2e48
    str r1,[sp,#0x0]                         @ 08026aa2 0091
    movs r1,#0xd6    @ 08026aa4 d621
    adds r2,r6,#0x0    @ 08026aa6 321c
    .hword 0x4643    @ 08026aa8 4346
    bl render_centered_text_to_bg_vram       @ 08026aaa fcf773ff
    ldr r0, DWORD_08026b60                   @ 08026aae 2c48
    movs r2,#0x93    @ 08026ab0 9322
    lsls r2,r2,#0x1    @ 08026ab2 5200
    ldr r3, DWORD_08026b64                   @ 08026ab4 2b4b
    movs r1,#0x40    @ 08026ab6 4021
    bl write_tile_row_to_vram                @ 08026ab8 c7f048fa
    ldr r0, DWORD_08026b68                   @ 08026abc 2a48
    movs r1,#0x80    @ 08026abe 8021
    bl zero_fill_by_halfword                 @ 08026ac0 cef0d8f9
    ldr r0, DWORD_08026b6c                   @ 08026ac4 2948
    movs r1,#0x80    @ 08026ac6 8021
    bl zero_fill_by_halfword                 @ 08026ac8 cef0d4f9
    ldr r2, DWORD_08026b70                   @ 08026acc 284a
    ldr r0,[r2,#0x8]                         @ 08026ace 9068
    ldr r1, DWORD_08026b74                   @ 08026ad0 2849
    ands r0,r1    @ 08026ad2 0840
    str r0,[r2,#0x8]                         @ 08026ad4 9060
    ldr r2, DWORD_08026b78                   @ 08026ad6 284a
    ldr r3, DWORD_08026b7c                   @ 08026ad8 284b
    adds r2,r2,r3    @ 08026ada d218
    ldrh r3,[r2,#0x0]                        @ 08026adc 1388
    lsls r1,r3,#0x12    @ 08026ade 9904
    lsrs r1,r1,#0x18    @ 08026ae0 090e
    adds r1,#0x1    @ 08026ae2 0131
    movs r0,#0xff    @ 08026ae4 ff20
    ands r1,r0    @ 08026ae6 0140
    lsls r1,r1,#0x6    @ 08026ae8 8901
    ldr r0, DWORD_08026b80                   @ 08026aea 2548
    ands r0,r3    @ 08026aec 1840
    orrs r0,r1    @ 08026aee 0843
    strh r0,[r2,#0x0]                        @ 08026af0 1080

@ campaign_scene_handler dispatch table index 11. Trigger: gPrng+0x202 bits[13:6] == 0x0b. Sequence: (1) reads scene_ctx+0x8 word, checks bits[22:15] (8-bit timer); (2) if nonzero: decrements timer by 1, writes back; looks up ROM table 0x09e59d18 at index (new_timer)*4, takes result & 0xff, shifts left 7 to write anim_frame into scene_ctx+0x8 halfword bits[14:7]; (3) if zero: clears scene_ctx+0x8 bits[14:7] (mask 0xffff807f), reads gPrng+0x202, increments bits[13:6] by 1, writes back (advance to step 12); (4) both paths: bl render_opp_wins_display_oam then b SUB_08026714.
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - timer_field = scene_ctx+0x8 word bits[22:15] [0..255]
@ - anim_frame_table = 0x09e59d18 (ROM lookup, 4 bytes/entry)
@ - anim_frame_field = scene_ctx+0x8 halfword bits[14:7]
@ - mask_clear_anim = 0xffff807f
@ - mask_clear_timer = 0xff807fff
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6], mask = 0xffffc03f
run_campaign_step11_anim_timer_tick:
    ldr r4, DWORD_08026b70                   @ 08026af2 1f4c
    ldr r3,[r4,#0x8]                         @ 08026af4 a368
    movs r0,#0xff    @ 08026af6 ff20
    lsls r0,r0,#0xf    @ 08026af8 c003
    ands r0,r3    @ 08026afa 1840
    cmp r0,#0x0                              @ 08026afc 0028
    beq LAB_08026b8c                         @ 08026afe 45d0
    lsls r1,r3,#0x9    @ 08026b00 5902
    lsrs r1,r1,#0x18    @ 08026b02 090e
    subs r1,#0x1    @ 08026b04 0139
    lsls r1,r1,#0x10    @ 08026b06 0904
    lsrs r1,r1,#0x10    @ 08026b08 090c
    movs r2,#0xff    @ 08026b0a ff22
    ands r1,r2    @ 08026b0c 1140
    lsls r1,r1,#0xf    @ 08026b0e c903
    ldr r0, DWORD_08026b74                   @ 08026b10 1848
    ands r0,r3    @ 08026b12 1840
    orrs r0,r1    @ 08026b14 0843
    str r0,[r4,#0x8]                         @ 08026b16 a060
    ldr r1, DWORD_08026b84                   @ 08026b18 1a49
    lsls r0,r0,#0x9    @ 08026b1a 4002
    lsrs r0,r0,#0x18    @ 08026b1c 000e
    lsls r0,r0,#0x2    @ 08026b1e 8000
    adds r0,r0,r1    @ 08026b20 4018
    ldr r1,[r0,#0x0]                         @ 08026b22 0168
    ands r1,r2    @ 08026b24 1140
    lsls r1,r1,#0x7    @ 08026b26 c901
    ldr r0, DWORD_08026b88                   @ 08026b28 1748
    ldrh r5,[r4,#0x8]                        @ 08026b2a 2589
    ands r0,r5    @ 08026b2c 2840
    orrs r0,r1    @ 08026b2e 0843
    strh r0,[r4,#0x8]                        @ 08026b30 2081
    b LAB_08026bb0                           @ 08026b32 3de0
DWORD_08026b34:
    .word  0x00000be4                     @ 08026b34 e40b0000
DWORD_08026b38:
    .word  game_str_pointer_table         @ 08026b38 400f0008
DWORD_08026b3c:
    .word  0x02000000                     @ 08026b3c 00000002
DWORD_08026b40:
    .word  0x00006c2c                     @ 08026b40 2c6c0000
DWORD_08026b44:
    .word  game_str_ja                    @ 08026b44 109cdb09
DWORD_08026b48:
    .word  0x00000707                     @ 08026b48 07070000
DWORD_08026b4c:
    .word  0x00000f09                     @ 08026b4c 090f0000
DWORD_08026b50:
    .word  0x00000b01                     @ 08026b50 010b0000
DWORD_08026b54:
    .word  0x09b953b4                     @ 08026b54 b453b909
DWORD_08026b58:
    .word  0x00000be5                     @ 08026b58 e50b0000
DWORD_08026b5c:
    .word  0x000007c7                     @ 08026b5c c7070000
DWORD_08026b60:
    .word  0x00000bc1                     @ 08026b60 c10b0000
DWORD_08026b64:
    .word  0x09b96514                     @ 08026b64 1465b909
DWORD_08026b68:
    .word  0x06000d80                     @ 08026b68 800d0006
DWORD_08026b6c:
    .word  0x06000900                     @ 08026b6c 00090006
DWORD_08026b70:
    .word  0x02023360                     @ 08026b70 60330202
DWORD_08026b74:
    .word  0xff807fff                     @ 08026b74 ff7f80ff
DWORD_08026b78:
    .word  gPrng                          @ 08026b78 40000003
DWORD_08026b7c:
    .word  0x00000202                     @ 08026b7c 02020000
DWORD_08026b80:
    .word  0xffffc03f                     @ 08026b80 3fc0ffff
DWORD_08026b84:
    .word  0x09e59d18                     @ 08026b84 189de509
DWORD_08026b88:
    .word  0xffff807f                     @ 08026b88 7f80ffff
LAB_08026b8c:
    ldr r0, DWORD_08026bb8                   @ 08026b8c 0a48
    ldrh r6,[r4,#0x8]                        @ 08026b8e 2689
    ands r0,r6    @ 08026b90 3040
    strh r0,[r4,#0x8]                        @ 08026b92 2081
    ldr r2, DWORD_08026bbc                   @ 08026b94 094a
    ldr r0, DWORD_08026bc0                   @ 08026b96 0a48
    adds r2,r2,r0    @ 08026b98 1218
    ldrh r3,[r2,#0x0]                        @ 08026b9a 1388
    lsls r1,r3,#0x12    @ 08026b9c 9904
    lsrs r1,r1,#0x18    @ 08026b9e 090e
    adds r1,#0x1    @ 08026ba0 0131
    movs r0,#0xff    @ 08026ba2 ff20
    ands r1,r0    @ 08026ba4 0140
    lsls r1,r1,#0x6    @ 08026ba6 8901
    ldr r0, DWORD_08026bc4                   @ 08026ba8 0648
    ands r0,r3    @ 08026baa 1840
    orrs r0,r1    @ 08026bac 0843
    strh r0,[r2,#0x0]                        @ 08026bae 1080
LAB_08026bb0:
    bl render_opp_wins_display_oam           @ 08026bb0 fdf7b0fa
    b SUB_08026714                           @ 08026bb4 aee5
    .zero  0x2
DWORD_08026bb8:
    .word  0xffff807f                     @ 08026bb8 7f80ffff
DWORD_08026bbc:
    .word  gPrng                          @ 08026bbc 40000003
DWORD_08026bc0:
    .word  0x00000202                     @ 08026bc0 02020000
DWORD_08026bc4:
    .word  0xffffc03f                     @ 08026bc4 3fc0ffff

@ Pack name text renderer for campaign_scene_handler dispatch table index 12. Trigger: gPrng+0x202 bits[13:6] == 0x0c. Reads scene_ctx(0x02023360)+3 bits[4:3] as pack_count [0..3]. If pack_count==0 jumps to completion path. Otherwise loops r4=1..min(pack_count,3): calls game_str_id_to_row(r4+0xbe0) to get pack name string row, calls render_centered_text_to_bg_vram to draw centered text, calls write_tile_row_to_vram for separator tile. After loop calls render_opp_wins_display_oam, then tail-calls LAB_08026c56 (writes gPrng+0x202 scaler and jumps to SUB_08026714).
@ 
@ Constants:
@ - step_index=12 (0x0c)
@ - scene_ctx=0x02023360
@ - pack_count=scene_ctx+3 bits[4:3] [0..3]
@ - game_str_id_base=0xbe0 (0xbe*0x10); loop: id=r4+0xbe0
@ - max_loop=3 (loop guard cmp r4,#0x3; ble)
@ - tile_row_data=0x09b953b4
run_campaign_step12_render_pack_name_rows:
    movs r4,#0x1    @ 08026bc8 0124
    ldr r0, DWORD_08026c5c                   @ 08026bca 2448
    ldrb r0,[r0,#0x3]                        @ 08026bcc c078
    lsls r0,r0,#0x1b    @ 08026bce c006
    lsrs r0,r0,#0x1d    @ 08026bd0 400f
    cmp r4,r0                                @ 08026bd2 8442
    bge LAB_08026c44                         @ 08026bd4 36da
    ldr r1, DWORD_08026c60                   @ 08026bd6 2249
    .hword 0x4688    @ 08026bd8 8846
    ldr r6, DWORD_08026c64                   @ 08026bda 224e
    ldr r5, DWORD_08026c68                   @ 08026bdc 224d
    ldr r7, DWORD_08026c6c                   @ 08026bde 234f
LAB_08026be0:
    movs r2,#0xbe    @ 08026be0 be22
    lsls r2,r2,#0x4    @ 08026be2 1201
    adds r0,r4,r2    @ 08026be4 a018
    bl game_str_id_to_row                    @ 08026be6 cef017f9
    lsls r0,r0,#0x10    @ 08026bea 0004
    lsrs r0,r0,#0x10    @ 08026bec 000c
    lsls r1,r0,#0x1    @ 08026bee 4100
    adds r1,r1,r0    @ 08026bf0 0918
    lsls r1,r1,#0x1    @ 08026bf2 4900
    ldrb r3,[r7,#0x0]                        @ 08026bf4 3b78
    lsls r0,r3,#0x1d    @ 08026bf6 5807
    lsrs r0,r0,#0x1d    @ 08026bf8 400f
    adds r1,r1,r0    @ 08026bfa 0918
    lsls r1,r1,#0x2    @ 08026bfc 8900
    add r1,r8                                @ 08026bfe 4144
    ldr r2,[r1,#0x0]                         @ 08026c00 0a68
    ldr r0, DWORD_08026c70                   @ 08026c02 1b48
    adds r2,r2,r0    @ 08026c04 1218
    lsrs r0,r5,#0x10    @ 08026c06 280c
    lsls r1,r4,#0x15    @ 08026c08 6105
    movs r3,#0xd8    @ 08026c0a d823
    lsls r3,r3,#0xe    @ 08026c0c 9b03
    adds r1,r1,r3    @ 08026c0e c918
    lsrs r1,r1,#0x10    @ 08026c10 090c
    str r2,[sp,#0x0]                         @ 08026c12 0092
    movs r2,#0x84    @ 08026c14 8422
    lsls r2,r2,#0x2    @ 08026c16 9200
    ldr r3, DWORD_08026c74                   @ 08026c18 164b
    bl render_centered_text_to_bg_vram       @ 08026c1a fcf7bbfe
    lsrs r0,r6,#0x10    @ 08026c1e 300c
    movs r1,#0x20    @ 08026c20 2021
    movs r2,#0xf6    @ 08026c22 f622
    ldr r3, DWORD_08026c78                   @ 08026c24 144b
    bl write_tile_row_to_vram                @ 08026c26 c7f091f9
    movs r0,#0xc0    @ 08026c2a c020
    lsls r0,r0,#0x10    @ 08026c2c 0004
    adds r6,r6,r0    @ 08026c2e 3618
    adds r5,r5,r0    @ 08026c30 2d18
    adds r4,#0x1    @ 08026c32 0134
    ldr r0, DWORD_08026c5c                   @ 08026c34 0948
    ldrb r0,[r0,#0x3]                        @ 08026c36 c078
    lsls r0,r0,#0x1b    @ 08026c38 c006
    lsrs r0,r0,#0x1d    @ 08026c3a 400f
    cmp r4,r0                                @ 08026c3c 8442
    bge LAB_08026c44                         @ 08026c3e 01da
    cmp r4,#0x3                              @ 08026c40 032c
    ble LAB_08026be0                         @ 08026c42 cddd
LAB_08026c44:
    bl render_opp_wins_display_oam           @ 08026c44 fdf766fa
    ldr r0, DWORD_08026c7c                   @ 08026c48 0c48
    ldr r1, DWORD_08026c80                   @ 08026c4a 0d49
    adds r0,r0,r1    @ 08026c4c 4018
    ldr r1, DWORD_08026c84                   @ 08026c4e 0d49
    ldrh r2,[r0,#0x0]                        @ 08026c50 0288
    ands r1,r2    @ 08026c52 1140
    movs r2,#0x80    @ 08026c54 8022
LAB_08026c56:
    orrs r1,r2    @ 08026c56 1143
    strh r1,[r0,#0x0]                        @ 08026c58 0180
    b SUB_08026714                           @ 08026c5a 5be5
DWORD_08026c5c:
    .word  0x02023360                     @ 08026c5c 60330202
DWORD_08026c60:
    .word  game_str_pointer_table         @ 08026c60 400f0008
DWORD_08026c64:
    .word  0x08c10000                     @ 08026c64 0000c108
DWORD_08026c68:
    .word  0x04c70000                     @ 08026c68 0000c704
DWORD_08026c6c:
    .word  gSettings                      @ 08026c6c 2c6c0002
DWORD_08026c70:
    .word  game_str_ja                    @ 08026c70 109cdb09
DWORD_08026c74:
    .word  0x00000f09                     @ 08026c74 090f0000
DWORD_08026c78:
    .word  0x09b953b4                     @ 08026c78 b453b909
DWORD_08026c7c:
    .word  gPrng                          @ 08026c7c 40000003
DWORD_08026c80:
    .word  0x00000202                     @ 08026c80 02020000
DWORD_08026c84:
    .word  0xffffc03f                     @ 08026c84 3fc0ffff

@ campaign_scene_handler (FUN_08025c94) dispatch table entry index 20, responsible for full initialization sequence before entering opponent card display screen. Trigger: scene state word gPrng+0x202 bits[13:6] == 0x14. Flow: (1) clear scene state word flag bits; (2) call init_campaign_bg_and_obj_vram for BG/OBJ VRAM global init; (3) extract slot type code bits[4:0] and call init_opponent_card_bg_vram(slot_type); (4) call init_duel_scroll_params; (5) compute and write IWRAM scroll params (0x02023360+0x23c = 0xfa*32 | slot_type); (6) write secondary IWRAM byte; (7) read font mode byte and look up font_jp_base_table to update font pointer; (8) branch on slot_type (0x19/0x1a or other): if neither, call card_name_lookup_by_internal_id + game_str_id_to_row + render_opponent_card_icon_and_name to render card name; (9) jump to LAB_08026df2 to write scene counter.
@ 
@ Constants:
@ - IWRAM scene_ctx base = 0x02023360
@ - scroll_param_target offset = 0x23c
@ - scroll base value = 0xfa*32 = 0x1f40
@ - slot_type special values: 0x19 (empty slot branch A), 0x1a (empty slot branch B)
run_campaign_step20_card_display_init:
    ldr r4, DWORD_08026d4c                   @ 08026c88 304c
    ldr r0,[r4,#0x8]                         @ 08026c8a a068
    ldr r1, DWORD_08026d50                   @ 08026c8c 3049
    ands r0,r1    @ 08026c8e 0840
    str r0,[r4,#0x8]                         @ 08026c90 a060
    bl init_campaign_bg_and_obj_vram         @ 08026c92 06f0eff9
    ldrb r3,[r4,#0x2]                        @ 08026c96 a378
    lsls r0,r3,#0x1b    @ 08026c98 d806
    lsrs r0,r0,#0x1b    @ 08026c9a c00e
    bl init_opponent_card_bg_vram            @ 08026c9c 06f080fa
    bl init_duel_scroll_params               @ 08026ca0 06f0f4fb
    ldr r2, DWORD_08026d54                   @ 08026ca4 2b4a
    ldrb r5,[r4,#0x2]                        @ 08026ca6 a578
    lsls r1,r5,#0x1b    @ 08026ca8 e906
    lsrs r1,r1,#0x1b    @ 08026caa c90e
    movs r6,#0xfa    @ 08026cac fa26
    lsls r6,r6,#0x5    @ 08026cae 7601
    adds r0,r6,#0x0    @ 08026cb0 301c
    orrs r0,r1    @ 08026cb2 0843
    movs r3,#0x8f    @ 08026cb4 8f23
    lsls r3,r3,#0x2    @ 08026cb6 9b00
    adds r3,r3,r2    @ 08026cb8 9b18
    .hword 0x469a    @ 08026cba 9a46
    strh r0,[r3,#0x0]                        @ 08026cbc 1880
    ldr r5, DWORD_08026d58                   @ 08026cbe 264d
    adds r7,r2,r5    @ 08026cc0 5719
    strb r1,[r7,#0x0]                        @ 08026cc2 3970
    ldr r6, DWORD_08026d5c                   @ 08026cc4 254e
    ldr r0, DWORD_08026d60                   @ 08026cc6 2648
    adds r0,r0,r6    @ 08026cc8 8019
    .hword 0x4681    @ 08026cca 8146
    ldrb r2,[r0,#0x0]                        @ 08026ccc 0278
    lsls r1,r2,#0x19    @ 08026cce 5106
    lsrs r1,r1,#0x1c    @ 08026cd0 090f
    lsls r2,r2,#0x1d    @ 08026cd2 5207
    lsrs r2,r2,#0x1d    @ 08026cd4 520f
    ldr r3, DWORD_08026d64                   @ 08026cd6 234b
    adds r3,r3,r6    @ 08026cd8 9b19
    .hword 0x4698    @ 08026cda 9846
    ldrb r0,[r3,#0x0]                        @ 08026cdc 1878
    str r0,[sp,#0x0]                         @ 08026cde 0090
    ldr r0, DWORD_08026d68                   @ 08026ce0 2148
    adds r5,r6,r0    @ 08026ce2 3518
    str r5,[sp,#0x4]                         @ 08026ce4 0195
    movs r0,#0x0    @ 08026ce6 0020
    ldr r3, DWORD_08026d6c                   @ 08026ce8 204b
    bl render_opponent_card_icon_and_name    @ 08026cea 06f0a5fc
    ldrb r1,[r4,#0x2]                        @ 08026cee a178
    lsls r0,r1,#0x1b    @ 08026cf0 c806
    lsrs r0,r0,#0x1b    @ 08026cf2 c00e
    cmp r0,#0x19                             @ 08026cf4 1928
    beq LAB_08026d80                         @ 08026cf6 43d0
    cmp r0,#0x1a                             @ 08026cf8 1a28
    beq LAB_08026da4                         @ 08026cfa 53d0
    ldr r4, DWORD_08026d70                   @ 08026cfc 1c4c
    ldrb r2,[r7,#0x0]                        @ 08026cfe 3a78
    lsls r0,r2,#0x5    @ 08026d00 5001
    adds r0,r0,r4    @ 08026d02 0019
    ldrh r0,[r0,#0x2]                        @ 08026d04 4088
    bl card_name_lookup_by_internal_id       @ 08026d06 c7f079ff
    adds r5,r0,#0x0    @ 08026d0a 051c
    ldrb r7,[r7,#0x0]                        @ 08026d0c 3f78
    lsls r0,r7,#0x5    @ 08026d0e 7801
    adds r0,r0,r4    @ 08026d10 0019
    ldrh r0,[r0,#0x4]                        @ 08026d12 8088
    bl game_str_id_to_row                    @ 08026d14 cef080f8
    ldr r2, DWORD_08026d74                   @ 08026d18 164a
    lsls r0,r0,#0x10    @ 08026d1a 0004
    lsrs r0,r0,#0x10    @ 08026d1c 000c
    lsls r1,r0,#0x1    @ 08026d1e 4100
    adds r1,r1,r0    @ 08026d20 0918
    lsls r1,r1,#0x1    @ 08026d22 4900
    ldr r3, DWORD_08026d78                   @ 08026d24 144b
    adds r0,r6,r3    @ 08026d26 f018
    ldrb r0,[r0,#0x0]                        @ 08026d28 0078
    lsls r4,r0,#0x1d    @ 08026d2a 4407
    lsrs r0,r4,#0x1d    @ 08026d2c 600f
    adds r1,r1,r0    @ 08026d2e 0918
    lsls r1,r1,#0x2    @ 08026d30 8900
    adds r1,r1,r2    @ 08026d32 8918
    ldr r3,[r1,#0x0]                         @ 08026d34 0b68
    ldr r0, DWORD_08026d7c                   @ 08026d36 1148
    adds r3,r3,r0    @ 08026d38 1b18
    .hword 0x4656    @ 08026d3a 5646
    ldrh r1,[r6,#0x0]                        @ 08026d3c 3188
    lsrs r2,r4,#0x1d    @ 08026d3e 620f
    adds r4,r2,#0x0    @ 08026d40 141c
    str r4,[sp,#0x0]                         @ 08026d42 0094
    str r3,[sp,#0x4]                         @ 08026d44 0193
    movs r0,#0x1    @ 08026d46 0120
    adds r3,r5,#0x0    @ 08026d48 2b1c
    b LAB_08026df2                           @ 08026d4a 52e0
DWORD_08026d4c:
    .word  0x02023360                     @ 08026d4c 60330202
DWORD_08026d50:
    .word  0xff807fff                     @ 08026d50 ff7f80ff
DWORD_08026d54:
    .word  gPrng                          @ 08026d54 40000003
DWORD_08026d58:
    .word  0x0000023e                     @ 08026d58 3e020000
DWORD_08026d5c:
    .word  0x02000000                     @ 08026d5c 00000002
DWORD_08026d60:
    .word  0x00006e57                     @ 08026d60 576e0000
DWORD_08026d64:
    .word  0x0000114f                     @ 08026d64 4f110000
DWORD_08026d68:
    .word  0x00001138                     @ 08026d68 38110000
DWORD_08026d6c:
    .word  gPlayerName                    @ 08026d6c 486e0002
DWORD_08026d70:
    .word  deck_record_table              @ 08026d70 0c8de509
DWORD_08026d74:
    .word  game_str_pointer_table         @ 08026d74 400f0008
DWORD_08026d78:
    .word  0x00006c2c                     @ 08026d78 2c6c0000
DWORD_08026d7c:
    .word  game_str_ja                    @ 08026d7c 109cdb09
LAB_08026d80:
    .hword 0x4648    @ 08026d80 4846
    ldrb r2,[r0,#0x0]                        @ 08026d82 0278
    lsls r1,r2,#0x19    @ 08026d84 5106
    lsrs r1,r1,#0x1c    @ 08026d86 090f
    lsls r2,r2,#0x1d    @ 08026d88 5207
    lsrs r2,r2,#0x1d    @ 08026d8a 520f
    .hword 0x4643    @ 08026d8c 4346
    ldrb r0,[r3,#0x0]                        @ 08026d8e 1878
    str r0,[sp,#0x0]                         @ 08026d90 0090
    str r5,[sp,#0x4]                         @ 08026d92 0195
    movs r0,#0x1    @ 08026d94 0120
    ldr r3, DWORD_08026da0                   @ 08026d96 024b
    bl render_opponent_card_icon_and_name    @ 08026d98 06f04efc
    b LAB_08026df6                           @ 08026d9c 2be0
    .zero  0x2
DWORD_08026da0:
    .word  gPlayerName                    @ 08026da0 486e0002
LAB_08026da4:
    ldr r1, DWORD_08026e44                   @ 08026da4 2749
    ldrb r7,[r7,#0x0]                        @ 08026da6 3f78
    lsls r0,r7,#0x5    @ 08026da8 7801
    adds r0,r0,r1    @ 08026daa 4018
    ldrh r0,[r0,#0x2]                        @ 08026dac 4088
    bl card_name_lookup_by_internal_id       @ 08026dae c7f025ff
    adds r3,r0,#0x0    @ 08026db2 031c
    .hword 0x4655    @ 08026db4 5546
    ldrh r1,[r5,#0x0]                        @ 08026db6 2988
    ldr r2, DWORD_08026e48                   @ 08026db8 234a
    adds r0,r6,r2    @ 08026dba b018
    ldrb r0,[r0,#0x0]                        @ 08026dbc 0078
    lsls r2,r0,#0x1d    @ 08026dbe 4207
    lsrs r2,r2,#0x1d    @ 08026dc0 520f
    ldrh r4,[r4,#0xc]                        @ 08026dc2 a489
    lsls r5,r4,#0x11    @ 08026dc4 6504
    lsrs r4,r5,#0x18    @ 08026dc6 2c0e
    lsls r0,r4,#0x3    @ 08026dc8 e000
    adds r0,r0,r4    @ 08026dca 0019
    lsls r0,r0,#0x2    @ 08026dcc 8000
    subs r0,r0,r4    @ 08026dce 001b
    lsls r0,r0,#0x3    @ 08026dd0 c000
    adds r0,r0,r6    @ 08026dd2 8019
    ldr r4, DWORD_08026e4c                   @ 08026dd4 1d4c
    adds r0,r0,r4    @ 08026dd6 0019
    ldrb r0,[r0,#0x0]                        @ 08026dd8 0078
    str r0,[sp,#0x0]                         @ 08026dda 0090
    lsrs r5,r5,#0x18    @ 08026ddc 2d0e
    lsls r0,r5,#0x3    @ 08026dde e800
    adds r0,r0,r5    @ 08026de0 4019
    lsls r0,r0,#0x2    @ 08026de2 8000
    subs r0,r0,r5    @ 08026de4 401b
    lsls r0,r0,#0x3    @ 08026de6 c000
    ldr r5, DWORD_08026e50                   @ 08026de8 194d
    adds r4,r6,r5    @ 08026dea 7419
    adds r0,r0,r4    @ 08026dec 0019
    str r0,[sp,#0x4]                         @ 08026dee 0190
    movs r0,#0x1    @ 08026df0 0120
LAB_08026df2:
    bl render_opponent_card_icon_and_name    @ 08026df2 06f021fc
LAB_08026df6:
    ldr r1, DWORD_08026e54                   @ 08026df6 1749
    adds r1,#0x39    @ 08026df8 3931
    movs r0,#0x21    @ 08026dfa 2120
    rsbs r0,r0,#0    @ 08026dfc 4042
    ldrb r6,[r1,#0x0]                        @ 08026dfe 0e78
    ands r0,r6    @ 08026e00 3040
    strb r0,[r1,#0x0]                        @ 08026e02 0870
    movs r0,#0x0    @ 08026e04 0020
    bl draw_card_name_label_to_sprite_vram   @ 08026e06 06f0c1fb
    ldr r2, DWORD_08026e58                   @ 08026e0a 134a
    ldr r0, DWORD_08026e5c                   @ 08026e0c 1348
    adds r1,r2,r0    @ 08026e0e 1118
    movs r0,#0x3f    @ 08026e10 3f20
    ldrb r3,[r1,#0x0]                        @ 08026e12 0b78
    ands r0,r3    @ 08026e14 1840
    strb r0,[r1,#0x0]                        @ 08026e16 0870
    movs r4,#0x81    @ 08026e18 8124
    lsls r4,r4,#0x2    @ 08026e1a a400
    adds r1,r2,r4    @ 08026e1c 1119
    movs r0,#0x40    @ 08026e1e 4020
    rsbs r0,r0,#0    @ 08026e20 4042
    ldrb r5,[r1,#0x0]                        @ 08026e22 0d78
    ands r0,r5    @ 08026e24 2840
    strb r0,[r1,#0x0]                        @ 08026e26 0870
    ldr r6, DWORD_08026e60                   @ 08026e28 0d4e
    adds r2,r2,r6    @ 08026e2a 9219
    ldrh r3,[r2,#0x0]                        @ 08026e2c 1388
    lsls r1,r3,#0x12    @ 08026e2e 9904
    lsrs r1,r1,#0x18    @ 08026e30 090e
    adds r1,#0x1    @ 08026e32 0131
    movs r0,#0xff    @ 08026e34 ff20
    ands r1,r0    @ 08026e36 0140
    lsls r1,r1,#0x6    @ 08026e38 8901
    ldr r0, DWORD_08026e64                   @ 08026e3a 0a48
    ands r0,r3    @ 08026e3c 1840
    bl SUB_08027c22                          @ 08026e3e 00f0f0fe
    movs r0,r0    @ 08026e42 0000
DWORD_08026e44:
    .word  deck_record_table              @ 08026e44 0c8de509
DWORD_08026e48:
    .word  0x00006c2c                     @ 08026e48 2c6c0000
DWORD_08026e4c:
    .word  0x00001267                     @ 08026e4c 67120000
DWORD_08026e50:
    .word  0x00001250                     @ 08026e50 50120000
DWORD_08026e54:
    .word  0x02023360                     @ 08026e54 60330202
DWORD_08026e58:
    .word  gPrng                          @ 08026e58 40000003
DWORD_08026e5c:
    .word  0x00000203                     @ 08026e5c 03020000
DWORD_08026e60:
    .word  0x00000202                     @ 08026e60 02020000
DWORD_08026e64:
    .word  0xffffc03f                     @ 08026e64 3fc0ffff

@ campaign_scene_handler dispatch table index 21. Trigger: gPrng+0x202 bits[13:6] == 0x15. Sequence: (1) bl tick_aob_display_with_sprite_enable_blend; (2) if r0 == 0 (blend not complete): b SUB_08026714 to wait; (3) if r0 != 0 (blend complete): reads gPrng+0x202, increments bits[13:6] by 1, writes back, then b SUB_08026714 to advance to step 22. Note: tick_aob_display_with_sprite_enable_blend exits via pop{r1};bx r1, r0 comes from tick_blend_step_by_delta return (0=not done, 1=done).
@ 
@ Constants:
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6], mask = 0xffffc03f
run_campaign_step21_aob_sprite_blend_tick:
    bl tick_aob_display_with_sprite_enable_blend @ 08026e68 07f056fd
    cmp r0,#0x0                              @ 08026e6c 0028
    bne LAB_08026e72                         @ 08026e6e 00d1
    b SUB_08026714                           @ 08026e70 50e4
LAB_08026e72:
    ldr r2, DWORD_08026e90                   @ 08026e72 074a
    ldr r0, DWORD_08026e94                   @ 08026e74 0748
    adds r2,r2,r0    @ 08026e76 1218
    ldrh r3,[r2,#0x0]                        @ 08026e78 1388
    lsls r1,r3,#0x12    @ 08026e7a 9904
    lsrs r1,r1,#0x18    @ 08026e7c 090e
    adds r1,#0x1    @ 08026e7e 0131
    movs r0,#0xff    @ 08026e80 ff20
    ands r1,r0    @ 08026e82 0140
    lsls r1,r1,#0x6    @ 08026e84 8901
    ldr r0, DWORD_08026e98                   @ 08026e86 0448
    ands r0,r3    @ 08026e88 1840
    orrs r0,r1    @ 08026e8a 0843
    strh r0,[r2,#0x0]                        @ 08026e8c 1080
    b SUB_08026714                           @ 08026e8e 41e4
DWORD_08026e90:
    .word  gPrng                          @ 08026e90 40000003
DWORD_08026e94:
    .word  0x00000202                     @ 08026e94 02020000
DWORD_08026e98:
    .word  0xffffc03f                     @ 08026e98 3fc0ffff

@ campaign_scene_handler dispatch table entry index 22, opponent card AOB animation display phase per-frame tick. Calls tick_opponent_aob_by_phase (FUN_0802d4bc) for frame update; if return is 0 (animation not finished) tail-jumps via b SUB_08026714 to advance scene state machine; if nonzero continues with subsequent dispatch logic (display type selection / label render / state advance).
@ 
@ Constants:
@ - no additional constants (only bl + cmp + bne + b four instructions)
run_campaign_step22_aob_tick:
    bl tick_opponent_aob_by_phase            @ 08026e9c 06f00efb
    cmp r0,#0x0                              @ 08026ea0 0028
    bne LAB_08026ea6                         @ 08026ea2 00d1
    b SUB_08026714                           @ 08026ea4 36e4
LAB_08026ea6:
    ldr r0, DWORD_08026ed0                   @ 08026ea6 0a48
    ldr r1, DWORD_08026ed4                   @ 08026ea8 0a49
    adds r0,r0,r1    @ 08026eaa 4018
    movs r1,#0x7    @ 08026eac 0721
    ldrb r0,[r0,#0x0]                        @ 08026eae 0078
    ands r1,r0    @ 08026eb0 0140
    cmp r1,#0x1                              @ 08026eb2 0129
    beq LAB_08026ef8                         @ 08026eb4 20d0
    cmp r1,#0x2                              @ 08026eb6 0229
    beq LAB_08026ef0                         @ 08026eb8 1ad0
    cmp r1,#0x3                              @ 08026eba 0329
    beq LAB_08026ee8                         @ 08026ebc 14d0
    cmp r1,#0x4                              @ 08026ebe 0429
    beq LAB_08026ee0                         @ 08026ec0 0ed0
    ldr r0, DWORD_08026ed8                   @ 08026ec2 0548
    cmp r1,#0x5                              @ 08026ec4 0529
    bne LAB_08026efa                         @ 08026ec6 18d1
    ldr r2, DWORD_08026edc                   @ 08026ec8 044a
    adds r0,r0,r2    @ 08026eca 8018
    b LAB_08026efa                           @ 08026ecc 15e0
    .zero  0x2
DWORD_08026ed0:
    .word  0x02000000                     @ 08026ed0 00000002
DWORD_08026ed4:
    .word  0x00006c2c                     @ 08026ed4 2c6c0000
DWORD_08026ed8:
    .word  0x09dba750                     @ 08026ed8 50a7db09
DWORD_08026edc:
    .word  0x0003a30c                     @ 08026edc 0ca30300
LAB_08026ee0:
    ldr r0, DWORD_08026ee4                   @ 08026ee0 0048
    b LAB_08026efa                           @ 08026ee2 0ae0
DWORD_08026ee4:
    .word  0x09de8ab2                     @ 08026ee4 b28ade09
LAB_08026ee8:
    ldr r0, DWORD_08026eec                   @ 08026ee8 0048
    b LAB_08026efa                           @ 08026eea 06e0
DWORD_08026eec:
    .word  0x09ddc6cc                     @ 08026eec ccc6dd09
LAB_08026ef0:
    ldr r0, DWORD_08026ef4                   @ 08026ef0 0048
    b LAB_08026efa                           @ 08026ef2 02e0
DWORD_08026ef4:
    .word  0x09dd037a                     @ 08026ef4 7a03dd09
LAB_08026ef8:
    ldr r0, DWORD_08026f28                   @ 08026ef8 0b48
LAB_08026efa:
    bl draw_card_name_label_to_sprite_vram   @ 08026efa 06f047fb
    ldr r0, DWORD_08026f2c                   @ 08026efe 0b48
    ldr r3, DWORD_08026f30                   @ 08026f00 0b4b
    adds r0,r0,r3    @ 08026f02 c018
    movs r2,#0x7    @ 08026f04 0722
    ldrb r0,[r0,#0x0]                        @ 08026f06 0078
    ands r2,r0    @ 08026f08 0240
    cmp r2,#0x1                              @ 08026f0a 012a
    beq LAB_08026f54                         @ 08026f0c 22d0
    cmp r2,#0x2                              @ 08026f0e 022a
    beq LAB_08026f4c                         @ 08026f10 1cd0
    cmp r2,#0x3                              @ 08026f12 032a
    beq LAB_08026f44                         @ 08026f14 16d0
    cmp r2,#0x4                              @ 08026f16 042a
    beq LAB_08026f3c                         @ 08026f18 10d0
    ldr r1, DWORD_08026f34                   @ 08026f1a 0649
    cmp r2,#0x5                              @ 08026f1c 052a
    bne LAB_08026f56                         @ 08026f1e 1ad1
    ldr r4, DWORD_08026f38                   @ 08026f20 054c
    adds r1,r1,r4    @ 08026f22 0919
    b LAB_08026f56                           @ 08026f24 17e0
    .zero  0x2
DWORD_08026f28:
    .word  0x09dc53d6                     @ 08026f28 d653dc09
DWORD_08026f2c:
    .word  0x02000000                     @ 08026f2c 00000002
DWORD_08026f30:
    .word  0x00006c2c                     @ 08026f30 2c6c0000
DWORD_08026f34:
    .word  0x09dbd7cc                     @ 08026f34 ccd7db09
DWORD_08026f38:
    .word  0x0003a910                     @ 08026f38 10a90300
LAB_08026f3c:
    ldr r1, DWORD_08026f40                   @ 08026f3c 0049
    b LAB_08026f56                           @ 08026f3e 0ae0
DWORD_08026f40:
    .word  0x09dec2c6                     @ 08026f40 c6c2de09
LAB_08026f44:
    ldr r1, DWORD_08026f48                   @ 08026f44 0049
    b LAB_08026f56                           @ 08026f46 06e0
DWORD_08026f48:
    .word  0x09ddffc8                     @ 08026f48 c8ffdd09
LAB_08026f4c:
    ldr r1, DWORD_08026f50                   @ 08026f4c 0049
    b LAB_08026f56                           @ 08026f4e 02e0
DWORD_08026f50:
    .word  0x09dd3cec                     @ 08026f50 ec3cdd09
LAB_08026f54:
    ldr r1, DWORD_08026f80                   @ 08026f54 0a49
LAB_08026f56:
    ldr r0, DWORD_08026f84                   @ 08026f56 0b48
    ldr r5, DWORD_08026f88                   @ 08026f58 0b4d
    adds r0,r0,r5    @ 08026f5a 4019
    movs r3,#0x7    @ 08026f5c 0723
    ldrb r0,[r0,#0x0]                        @ 08026f5e 0078
    ands r3,r0    @ 08026f60 0340
    cmp r3,#0x1                              @ 08026f62 012b
    beq LAB_08026fac                         @ 08026f64 22d0
    cmp r3,#0x2                              @ 08026f66 022b
    beq LAB_08026fa4                         @ 08026f68 1cd0
    cmp r3,#0x3                              @ 08026f6a 032b
    beq LAB_08026f9c                         @ 08026f6c 16d0
    cmp r3,#0x4                              @ 08026f6e 042b
    beq LAB_08026f94                         @ 08026f70 10d0
    ldr r2, DWORD_08026f8c                   @ 08026f72 064a
    cmp r3,#0x5                              @ 08026f74 052b
    bne LAB_08026fae                         @ 08026f76 1ad1
    ldr r6, DWORD_08026f90                   @ 08026f78 054e
    adds r2,r2,r6    @ 08026f7a 9219
    b LAB_08026fae                           @ 08026f7c 17e0
    .zero  0x2
DWORD_08026f80:
    .word  0x09dc882a                     @ 08026f80 2a88dc09
DWORD_08026f84:
    .word  0x02000000                     @ 08026f84 00000002
DWORD_08026f88:
    .word  0x00006c2c                     @ 08026f88 2c6c0000
DWORD_08026f8c:
    .word  0x09dbd7d4                     @ 08026f8c d4d7db09
DWORD_08026f90:
    .word  0x0003a90e                     @ 08026f90 0ea90300
LAB_08026f94:
    ldr r2, DWORD_08026f98                   @ 08026f94 004a
    b LAB_08026fae                           @ 08026f96 0ae0
DWORD_08026f98:
    .word  0x09dec2cc                     @ 08026f98 ccc2de09
LAB_08026f9c:
    ldr r2, DWORD_08026fa0                   @ 08026f9c 004a
    b LAB_08026fae                           @ 08026f9e 06e0
DWORD_08026fa0:
    .word  0x09ddffce                     @ 08026fa0 ceffdd09
LAB_08026fa4:
    ldr r2, DWORD_08026fa8                   @ 08026fa4 004a
    b LAB_08026fae                           @ 08026fa6 02e0
DWORD_08026fa8:
    .word  0x09dd3cf2                     @ 08026fa8 f23cdd09
LAB_08026fac:
    ldr r2, DWORD_08026fd4                   @ 08026fac 094a
LAB_08026fae:
    movs r0,#0x3    @ 08026fae 0320
    bl setup_label_render_ctx                @ 08026fb0 06f08cfd
    ldr r2, DWORD_08026fd8                   @ 08026fb4 084a
    ldr r0, DWORD_08026fdc                   @ 08026fb6 0948
    adds r2,r2,r0    @ 08026fb8 1218
    ldrh r3,[r2,#0x0]                        @ 08026fba 1388
    lsls r1,r3,#0x12    @ 08026fbc 9904
    lsrs r1,r1,#0x18    @ 08026fbe 090e
    adds r1,#0x1    @ 08026fc0 0131
    movs r0,#0xff    @ 08026fc2 ff20
    ands r1,r0    @ 08026fc4 0140
    lsls r1,r1,#0x6    @ 08026fc6 8901
    ldr r0, DWORD_08026fe0                   @ 08026fc8 0548
    ands r0,r3    @ 08026fca 1840
    orrs r0,r1    @ 08026fcc 0843
    strh r0,[r2,#0x0]                        @ 08026fce 1080
    bl SUB_08026714                          @ 08026fd0 fff7a0fb
DWORD_08026fd4:
    .word  0x09dc8830                     @ 08026fd4 3088dc09
DWORD_08026fd8:
    .word  gPrng                          @ 08026fd8 40000003
DWORD_08026fdc:
    .word  0x00000202                     @ 08026fdc 02020000
DWORD_08026fe0:
    .word  0xffffc03f                     @ 08026fe0 3fc0ffff

@ campaign_scene_handler dispatch table index 23. Trigger: gPrng+0x202 bits[13:6] == 0x17. Sequence: (1) bl tick_campaign_card_select_display_state; (2) if returns 0 (not done): b SUB_08026714 to wait; (3) if returns nonzero (done): checks scene_ctx+0x39 bit4 (0x10) and bit3 (0x08) -- if both set, enters extended detail display path (LP panel/deck info rendering); exits via b LAB_08025d28 or b SUB_08026714.
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - bit4 = 0x10 (display complete flag)
@ - bit3 = 0x08 (detail mode flag)
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6]
run_campaign_step23_card_select_tick:
    bl tick_campaign_card_select_display_state @ 08026fe4 07f090f8
    cmp r0,#0x0                              @ 08026fe8 0028
    bne LAB_08026ff0                         @ 08026fea 01d1
    bl SUB_08026714                          @ 08026fec fff792fb
LAB_08026ff0:
    ldr r0, DWORD_08027034                   @ 08026ff0 1048
    adds r0,#0x39    @ 08026ff2 3930
    ldrb r1,[r0,#0x0]                        @ 08026ff4 0178
    movs r0,#0x10    @ 08026ff6 1020
    ands r0,r1    @ 08026ff8 0840
    cmp r0,#0x0                              @ 08026ffa 0028
    bne LAB_08027000                         @ 08026ffc 00d1
    b LAB_0802724c                           @ 08026ffe 25e1
LAB_08027000:
    movs r0,#0x8    @ 08027000 0820
    ands r0,r1    @ 08027002 0840
    cmp r0,#0x0                              @ 08027004 0028
    bne LAB_0802700a                         @ 08027006 00d1
    b LAB_08027124                           @ 08027008 8ce0
LAB_0802700a:
    ldr r0, DWORD_08027038                   @ 0802700a 0b48
    ldr r1, DWORD_0802703c                   @ 0802700c 0b49
    adds r0,r0,r1    @ 0802700e 4018
    movs r1,#0x7    @ 08027010 0721
    ldrb r0,[r0,#0x0]                        @ 08027012 0078
    ands r1,r0    @ 08027014 0140
    cmp r1,#0x1                              @ 08027016 0129
    beq LAB_08027060                         @ 08027018 22d0
    cmp r1,#0x2                              @ 0802701a 0229
    beq LAB_08027058                         @ 0802701c 1cd0
    cmp r1,#0x3                              @ 0802701e 0329
    beq LAB_08027050                         @ 08027020 16d0
    cmp r1,#0x4                              @ 08027022 0429
    beq LAB_08027048                         @ 08027024 10d0
    ldr r0, DWORD_08027040                   @ 08027026 0648
    cmp r1,#0x5                              @ 08027028 0529
    bne LAB_08027062                         @ 0802702a 1ad1
    ldr r2, DWORD_08027044                   @ 0802702c 054a
    adds r0,r0,r2    @ 0802702e 8018
    b LAB_08027062                           @ 08027030 17e0
    .zero  0x2
DWORD_08027034:
    .word  0x02023360                     @ 08027034 60330202
DWORD_08027038:
    .word  0x02000000                     @ 08027038 00000002
DWORD_0802703c:
    .word  0x00006c2c                     @ 0802703c 2c6c0000
DWORD_08027040:
    .word  0x09dbfd66                     @ 08027040 66fddb09
DWORD_08027044:
    .word  0x0003ab16                     @ 08027044 16ab0300
LAB_08027048:
    ldr r0, DWORD_0802704c                   @ 08027048 0048
    b LAB_08027062                           @ 0802704a 0ae0
DWORD_0802704c:
    .word  0x09deeca0                     @ 0802704c a0ecde09
LAB_08027050:
    ldr r0, DWORD_08027054                   @ 08027050 0048
    b LAB_08027062                           @ 08027052 06e0
DWORD_08027054:
    .word  0x09de27ec                     @ 08027054 ec27de09
LAB_08027058:
    ldr r0, DWORD_0802705c                   @ 08027058 0048
    b LAB_08027062                           @ 0802705a 02e0
DWORD_0802705c:
    .word  0x09dd6478                     @ 0802705c 7864dd09
LAB_08027060:
    ldr r0, DWORD_08027090                   @ 08027060 0b48
LAB_08027062:
    bl draw_card_name_label_to_sprite_vram   @ 08027062 06f093fa
    ldr r0, DWORD_08027094                   @ 08027066 0b48
    ldr r3, DWORD_08027098                   @ 08027068 0b4b
    adds r0,r0,r3    @ 0802706a c018
    movs r2,#0x7    @ 0802706c 0722
    ldrb r0,[r0,#0x0]                        @ 0802706e 0078
    ands r2,r0    @ 08027070 0240
    cmp r2,#0x1                              @ 08027072 012a
    beq LAB_080270bc                         @ 08027074 22d0
    cmp r2,#0x2                              @ 08027076 022a
    beq LAB_080270b4                         @ 08027078 1cd0
    cmp r2,#0x3                              @ 0802707a 032a
    beq LAB_080270ac                         @ 0802707c 16d0
    cmp r2,#0x4                              @ 0802707e 042a
    beq LAB_080270a4                         @ 08027080 10d0
    ldr r1, DWORD_0802709c                   @ 08027082 0649
    cmp r2,#0x5                              @ 08027084 052a
    bne LAB_080270be                         @ 08027086 1ad1
    ldr r4, DWORD_080270a0                   @ 08027088 054c
    adds r1,r1,r4    @ 0802708a 0919
    b LAB_080270be                           @ 0802708c 17e0
    .zero  0x2
DWORD_08027090:
    .word  0x09dcab86                     @ 08027090 86abdc09
DWORD_08027094:
    .word  0x02000000                     @ 08027094 00000002
DWORD_08027098:
    .word  0x00006c2c                     @ 08027098 2c6c0000
DWORD_0802709c:
    .word  0x09dbfd82                     @ 0802709c 82fddb09
DWORD_080270a0:
    .word  0x0003ab0e                     @ 080270a0 0eab0300
LAB_080270a4:
    ldr r1, DWORD_080270a8                   @ 080270a4 0049
    b LAB_080270be                           @ 080270a6 0ae0
DWORD_080270a8:
    .word  0x09deecb2                     @ 080270a8 b2ecde09
LAB_080270ac:
    ldr r1, DWORD_080270b0                   @ 080270ac 0049
    b LAB_080270be                           @ 080270ae 06e0
DWORD_080270b0:
    .word  0x09de2802                     @ 080270b0 0228de09
LAB_080270b4:
    ldr r1, DWORD_080270b8                   @ 080270b4 0049
    b LAB_080270be                           @ 080270b6 02e0
DWORD_080270b8:
    .word  0x09dd648e                     @ 080270b8 8e64dd09
LAB_080270bc:
    ldr r1, DWORD_080270e8                   @ 080270bc 0a49
LAB_080270be:
    ldr r0, DWORD_080270ec                   @ 080270be 0b48
    ldr r5, DWORD_080270f0                   @ 080270c0 0b4d
    adds r0,r0,r5    @ 080270c2 4019
    movs r3,#0x7    @ 080270c4 0723
    ldrb r0,[r0,#0x0]                        @ 080270c6 0078
    ands r3,r0    @ 080270c8 0340
    cmp r3,#0x1                              @ 080270ca 012b
    beq LAB_08027114                         @ 080270cc 22d0
    cmp r3,#0x2                              @ 080270ce 022b
    beq LAB_0802710c                         @ 080270d0 1cd0
    cmp r3,#0x3                              @ 080270d2 032b
    beq LAB_08027104                         @ 080270d4 16d0
    cmp r3,#0x4                              @ 080270d6 042b
    beq LAB_080270fc                         @ 080270d8 10d0
    ldr r2, DWORD_080270f4                   @ 080270da 064a
    cmp r3,#0x5                              @ 080270dc 052b
    bne LAB_08027116                         @ 080270de 1ad1
    ldr r6, DWORD_080270f8                   @ 080270e0 054e
    adds r2,r2,r6    @ 080270e2 9219
    b LAB_08027116                           @ 080270e4 17e0
    .zero  0x2
DWORD_080270e8:
    .word  0x09dcab98                     @ 080270e8 98abdc09
DWORD_080270ec:
    .word  0x02000000                     @ 080270ec 00000002
DWORD_080270f0:
    .word  0x00006c2c                     @ 080270f0 2c6c0000
DWORD_080270f4:
    .word  0x09dbfd88                     @ 080270f4 88fddb09
DWORD_080270f8:
    .word  0x0003ab10                     @ 080270f8 10ab0300
LAB_080270fc:
    ldr r2, DWORD_08027100                   @ 080270fc 004a
    b LAB_08027116                           @ 080270fe 0ae0
DWORD_08027100:
    .word  0x09deecb8                     @ 08027100 b8ecde09
LAB_08027104:
    ldr r2, DWORD_08027108                   @ 08027104 004a
    b LAB_08027116                           @ 08027106 06e0
DWORD_08027108:
    .word  0x09de280a                     @ 08027108 0a28de09
LAB_0802710c:
    ldr r2, DWORD_08027110                   @ 0802710c 004a
    b LAB_08027116                           @ 0802710e 02e0
DWORD_08027110:
    .word  0x09dd6496                     @ 08027110 9664dd09
LAB_08027114:
    ldr r2, DWORD_08027120                   @ 08027114 024a
LAB_08027116:
    movs r0,#0x2    @ 08027116 0220
    bl setup_label_render_ctx                @ 08027118 06f0d8fc
    b LAB_08027230                           @ 0802711c 88e0
    .zero  0x2
DWORD_08027120:
    .word  0x09dcab9e                     @ 08027120 9eabdc09
LAB_08027124:
    ldr r0, DWORD_0802714c                   @ 08027124 0948
    ldr r1, DWORD_08027150                   @ 08027126 0a49
    adds r0,r0,r1    @ 08027128 4018
    movs r1,#0x7    @ 0802712a 0721
    ldrb r0,[r0,#0x0]                        @ 0802712c 0078
    ands r1,r0    @ 0802712e 0140
    cmp r1,#0x1                              @ 08027130 0129
    beq LAB_08027174                         @ 08027132 1fd0
    cmp r1,#0x2                              @ 08027134 0229
    beq LAB_0802716c                         @ 08027136 19d0
    cmp r1,#0x3                              @ 08027138 0329
    beq LAB_08027164                         @ 0802713a 13d0
    cmp r1,#0x4                              @ 0802713c 0429
    beq LAB_0802715c                         @ 0802713e 0dd0
    ldr r0, DWORD_08027154                   @ 08027140 0448
    cmp r1,#0x5                              @ 08027142 0529
    bne LAB_08027176                         @ 08027144 17d1
    ldr r2, DWORD_08027158                   @ 08027146 044a
    adds r0,r0,r2    @ 08027148 8018
    b LAB_08027176                           @ 0802714a 14e0
DWORD_0802714c:
    .word  0x02000000                     @ 0802714c 00000002
DWORD_08027150:
    .word  0x00006c2c                     @ 08027150 2c6c0000
DWORD_08027154:
    .word  0x09dbfda6                     @ 08027154 a6fddb09
DWORD_08027158:
    .word  0x0003ab14                     @ 08027158 14ab0300
LAB_0802715c:
    ldr r0, DWORD_08027160                   @ 0802715c 0048
    b LAB_08027176                           @ 0802715e 0ae0
DWORD_08027160:
    .word  0x09deecd8                     @ 08027160 d8ecde09
LAB_08027164:
    ldr r0, DWORD_08027168                   @ 08027164 0048
    b LAB_08027176                           @ 08027166 06e0
DWORD_08027168:
    .word  0x09de282c                     @ 08027168 2c28de09
LAB_0802716c:
    ldr r0, DWORD_08027170                   @ 0802716c 0048
    b LAB_08027176                           @ 0802716e 02e0
DWORD_08027170:
    .word  0x09dd64b2                     @ 08027170 b264dd09
LAB_08027174:
    ldr r0, DWORD_080271a4                   @ 08027174 0b48
LAB_08027176:
    bl draw_card_name_label_to_sprite_vram   @ 08027176 06f009fa
    ldr r0, DWORD_080271a8                   @ 0802717a 0b48
    ldr r3, DWORD_080271ac                   @ 0802717c 0b4b
    adds r0,r0,r3    @ 0802717e c018
    movs r2,#0x7    @ 08027180 0722
    ldrb r0,[r0,#0x0]                        @ 08027182 0078
    ands r2,r0    @ 08027184 0240
    cmp r2,#0x1                              @ 08027186 012a
    beq LAB_080271d0                         @ 08027188 22d0
    cmp r2,#0x2                              @ 0802718a 022a
    beq LAB_080271c8                         @ 0802718c 1cd0
    cmp r2,#0x3                              @ 0802718e 032a
    beq LAB_080271c0                         @ 08027190 16d0
    cmp r2,#0x4                              @ 08027192 042a
    beq LAB_080271b8                         @ 08027194 10d0
    ldr r1, DWORD_080271b0                   @ 08027196 0649
    cmp r2,#0x5                              @ 08027198 052a
    bne LAB_080271d2                         @ 0802719a 1ad1
    ldr r4, DWORD_080271b4                   @ 0802719c 054c
    adds r1,r1,r4    @ 0802719e 0919
    b LAB_080271d2                           @ 080271a0 17e0
    .zero  0x2
DWORD_080271a4:
    .word  0x09dcabba                     @ 080271a4 baabdc09
DWORD_080271a8:
    .word  0x02000000                     @ 080271a8 00000002
DWORD_080271ac:
    .word  0x00006c2c                     @ 080271ac 2c6c0000
DWORD_080271b0:
    .word  0x09dbfd82                     @ 080271b0 82fddb09
DWORD_080271b4:
    .word  0x0003ab0e                     @ 080271b4 0eab0300
LAB_080271b8:
    ldr r1, DWORD_080271bc                   @ 080271b8 0049
    b LAB_080271d2                           @ 080271ba 0ae0
DWORD_080271bc:
    .word  0x09deecb2                     @ 080271bc b2ecde09
LAB_080271c0:
    ldr r1, DWORD_080271c4                   @ 080271c0 0049
    b LAB_080271d2                           @ 080271c2 06e0
DWORD_080271c4:
    .word  0x09de2802                     @ 080271c4 0228de09
LAB_080271c8:
    ldr r1, DWORD_080271cc                   @ 080271c8 0049
    b LAB_080271d2                           @ 080271ca 02e0
DWORD_080271cc:
    .word  0x09dd648e                     @ 080271cc 8e64dd09
LAB_080271d0:
    ldr r1, DWORD_080271fc                   @ 080271d0 0a49
LAB_080271d2:
    ldr r0, DWORD_08027200                   @ 080271d2 0b48
    ldr r5, DWORD_08027204                   @ 080271d4 0b4d
    adds r0,r0,r5    @ 080271d6 4019
    movs r3,#0x7    @ 080271d8 0723
    ldrb r0,[r0,#0x0]                        @ 080271da 0078
    ands r3,r0    @ 080271dc 0340
    cmp r3,#0x1                              @ 080271de 012b
    beq LAB_08027228                         @ 080271e0 22d0
    cmp r3,#0x2                              @ 080271e2 022b
    beq LAB_08027220                         @ 080271e4 1cd0
    cmp r3,#0x3                              @ 080271e6 032b
    beq LAB_08027218                         @ 080271e8 16d0
    cmp r3,#0x4                              @ 080271ea 042b
    beq LAB_08027210                         @ 080271ec 10d0
    ldr r2, DWORD_08027208                   @ 080271ee 064a
    cmp r3,#0x5                              @ 080271f0 052b
    bne LAB_0802722a                         @ 080271f2 1ad1
    ldr r6, DWORD_0802720c                   @ 080271f4 054e
    adds r2,r2,r6    @ 080271f6 9219
    b LAB_0802722a                           @ 080271f8 17e0
    .zero  0x2
DWORD_080271fc:
    .word  0x09dcab98                     @ 080271fc 98abdc09
DWORD_08027200:
    .word  0x02000000                     @ 08027200 00000002
DWORD_08027204:
    .word  0x00006c2c                     @ 08027204 2c6c0000
DWORD_08027208:
    .word  0x09dbfd88                     @ 08027208 88fddb09
DWORD_0802720c:
    .word  0x0003ab10                     @ 0802720c 10ab0300
LAB_08027210:
    ldr r2, DWORD_08027214                   @ 08027210 004a
    b LAB_0802722a                           @ 08027212 0ae0
DWORD_08027214:
    .word  0x09deecb8                     @ 08027214 b8ecde09
LAB_08027218:
    ldr r2, DWORD_0802721c                   @ 08027218 004a
    b LAB_0802722a                           @ 0802721a 06e0
DWORD_0802721c:
    .word  0x09de280a                     @ 0802721c 0a28de09
LAB_08027220:
    ldr r2, DWORD_08027224                   @ 08027220 004a
    b LAB_0802722a                           @ 08027222 02e0
DWORD_08027224:
    .word  0x09dd6496                     @ 08027224 9664dd09
LAB_08027228:
    ldr r2, DWORD_0802726c                   @ 08027228 104a
LAB_0802722a:
    movs r0,#0x6    @ 0802722a 0620
    bl setup_label_render_ctx                @ 0802722c 06f04efc
LAB_08027230:
    ldr r2, DWORD_08027270                   @ 08027230 0f4a
    ldr r0, DWORD_08027274                   @ 08027232 1048
    adds r2,r2,r0    @ 08027234 1218
    ldrh r3,[r2,#0x0]                        @ 08027236 1388
    lsls r1,r3,#0x12    @ 08027238 9904
    lsrs r1,r1,#0x18    @ 0802723a 090e
    adds r1,#0x1    @ 0802723c 0131
    movs r0,#0xff    @ 0802723e ff20
    ands r1,r0    @ 08027240 0140
    lsls r1,r1,#0x6    @ 08027242 8901
    ldr r0, DWORD_08027278                   @ 08027244 0c48
    ands r0,r3    @ 08027246 1840
    orrs r0,r1    @ 08027248 0843
    strh r0,[r2,#0x0]                        @ 0802724a 1080
LAB_0802724c:
    ldr r2, DWORD_08027270                   @ 0802724c 084a
    ldr r1, DWORD_08027274                   @ 0802724e 0949
    adds r2,r2,r1    @ 08027250 5218
    ldrh r3,[r2,#0x0]                        @ 08027252 1388
    lsls r1,r3,#0x12    @ 08027254 9904
    lsrs r1,r1,#0x18    @ 08027256 090e
    adds r1,#0x1    @ 08027258 0131
    movs r0,#0xff    @ 0802725a ff20
    ands r1,r0    @ 0802725c 0140
    lsls r1,r1,#0x6    @ 0802725e 8901
    ldr r0, DWORD_08027278                   @ 08027260 0548
    ands r0,r3    @ 08027262 1840
    orrs r0,r1    @ 08027264 0843
    strh r0,[r2,#0x0]                        @ 08027266 1080
    bl SUB_08026714                          @ 08027268 fff754fa
DWORD_0802726c:
    .word  0x09dcab9e                     @ 0802726c 9eabdc09
DWORD_08027270:
    .word  gPrng                          @ 08027270 40000003
DWORD_08027274:
    .word  0x00000202                     @ 08027274 02020000
DWORD_08027278:
    .word  0xffffc03f                     @ 08027278 3fc0ffff

@ campaign_scene_handler dispatch table index 24. Trigger: gPrng+0x202 bits[13:6] == 0x18. Sequence: (1) bl tick_aob_display_with_fadein; if returns 0 (fade-in not complete): b SUB_08026714 to wait. If returns nonzero (complete): (2) bl build_field_slot_bitmask; (3) bl init_duel_field_icon_and_bg_vram; (4) branches on [0x02006c2c] bits[2:0] = deck_type [0..5] twice to select tile data and BG color data; (5) bl draw_decimal_with_offset(0x40, 0x210, src, 0x10f) and (0x80, 0x21c, 0x1, ..); (6) if scene_ctx+0x4 bits[7:5] > 2 and bits[4:3] > 5: bl game_str_id_to_row + bl render_centered_text_to_bg_vram + bl write_tile_row_to_vram; (7) OAM sprite batch-write loop for card condition sprites; exits via b SUB_08026714.
@ 
@ Constants:
@ - deck_type_reg = [0x02006c2c] bits[2:0] [0..5]
@ - x_win_label = 0x40, y_win_label = 0x84*4 = 0x210
@ - x_lp_label = 0x80, y_lp_label = 0x87*4 = 0x21c
@ - oam_sprite_loop_stride = 0xc0<<4 = 0xc00
run_campaign_step24_fadein_and_field_init:
    bl tick_aob_display_with_fadein          @ 0802727c 07f05cfb
    cmp r0,#0x0                              @ 08027280 0028
    bne LAB_08027288                         @ 08027282 01d1
    bl SUB_08026714                          @ 08027284 fff746fa
LAB_08027288:
    bl build_field_slot_bitmask              @ 08027288 fdf734fb
    bl init_duel_field_icon_and_bg_vram      @ 0802728c fcf76efc
    ldr r0, DWORD_080272b8                   @ 08027290 0948
    ldr r2, DWORD_080272bc                   @ 08027292 0a4a
    adds r0,r0,r2    @ 08027294 8018
    movs r1,#0x7    @ 08027296 0721
    ldrb r0,[r0,#0x0]                        @ 08027298 0078
    ands r1,r0    @ 0802729a 0140
    cmp r1,#0x1                              @ 0802729c 0129
    beq LAB_080272e0                         @ 0802729e 1fd0
    cmp r1,#0x2                              @ 080272a0 0229
    beq LAB_080272d8                         @ 080272a2 19d0
    cmp r1,#0x3                              @ 080272a4 0329
    beq LAB_080272d0                         @ 080272a6 13d0
    cmp r1,#0x4                              @ 080272a8 0429
    beq LAB_080272c8                         @ 080272aa 0dd0
    ldr r3, DWORD_080272c0                   @ 080272ac 044b
    cmp r1,#0x5                              @ 080272ae 0529
    bne LAB_080272e2                         @ 080272b0 17d1
    ldr r4, DWORD_080272c4                   @ 080272b2 044c
    adds r3,r3,r4    @ 080272b4 1b19
    b LAB_080272e2                           @ 080272b6 14e0
DWORD_080272b8:
    .word  0x02000000                     @ 080272b8 00000002
DWORD_080272bc:
    .word  0x00006c2c                     @ 080272bc 2c6c0000
DWORD_080272c0:
    .word  0x09dbff0e                     @ 080272c0 0effdb09
DWORD_080272c4:
    .word  0x0003ab1e                     @ 080272c4 1eab0300
LAB_080272c8:
    ldr r3, DWORD_080272cc                   @ 080272c8 004b
    b LAB_080272e2                           @ 080272ca 0ae0
DWORD_080272cc:
    .word  0x09deee62                     @ 080272cc 62eede09
LAB_080272d0:
    ldr r3, DWORD_080272d4                   @ 080272d0 004b
    b LAB_080272e2                           @ 080272d2 06e0
DWORD_080272d4:
    .word  0x09de29ae                     @ 080272d4 ae29de09
LAB_080272d8:
    ldr r3, DWORD_080272dc                   @ 080272d8 004b
    b LAB_080272e2                           @ 080272da 02e0
DWORD_080272dc:
    .word  0x09dd6636                     @ 080272dc 3666dd09
LAB_080272e0:
    ldr r3, DWORD_08027320                   @ 080272e0 0f4b
LAB_080272e2:
    ldr r4, DWORD_08027324                   @ 080272e2 104c
    ldr r5, DWORD_08027328                   @ 080272e4 104d
    adds r4,r4,r5    @ 080272e6 6419
    ldrb r6,[r4,#0x0]                        @ 080272e8 2678
    lsls r0,r6,#0x1d    @ 080272ea 7007
    lsrs r0,r0,#0x1d    @ 080272ec 400f
    str r0,[sp,#0x0]                         @ 080272ee 0090
    movs r0,#0x40    @ 080272f0 4020
    movs r1,#0x84    @ 080272f2 8421
    lsls r1,r1,#0x2    @ 080272f4 8900
    ldr r2, DWORD_0802732c                   @ 080272f6 0d4a
    bl draw_decimal_with_offset              @ 080272f8 fcf7c0fa
    movs r0,#0x7    @ 080272fc 0720
    ldrb r4,[r4,#0x0]                        @ 080272fe 2478
    ands r0,r4    @ 08027300 2040
    cmp r0,#0x1                              @ 08027302 0128
    beq LAB_08027350                         @ 08027304 24d0
    cmp r0,#0x2                              @ 08027306 0228
    beq LAB_08027348                         @ 08027308 1ed0
    cmp r0,#0x3                              @ 0802730a 0328
    beq LAB_08027340                         @ 0802730c 18d0
    cmp r0,#0x4                              @ 0802730e 0428
    beq LAB_08027338                         @ 08027310 12d0
    ldr r3, DWORD_08027330                   @ 08027312 074b
    cmp r0,#0x5                              @ 08027314 0528
    bne LAB_08027352                         @ 08027316 1cd1
    ldr r0, DWORD_08027334                   @ 08027318 0648
    adds r3,r3,r0    @ 0802731a 1b18
    b LAB_08027352                           @ 0802731c 19e0
    .zero  0x2
DWORD_08027320:
    .word  0x09dcad08                     @ 08027320 08addc09
DWORD_08027324:
    .word  0x02000000                     @ 08027324 00000002
DWORD_08027328:
    .word  0x00006c2c                     @ 08027328 2c6c0000
DWORD_0802732c:
    .word  0x0000010f                     @ 0802732c 0f010000
DWORD_08027330:
    .word  0x09dc00b8                     @ 08027330 b800dc09
DWORD_08027334:
    .word  0x0003ab50                     @ 08027334 50ab0300
LAB_08027338:
    ldr r3, DWORD_0802733c                   @ 08027338 004b
    b LAB_08027352                           @ 0802733a 0ae0
DWORD_0802733c:
    .word  0x09def042                     @ 0802733c 42f0de09
LAB_08027340:
    ldr r3, DWORD_08027344                   @ 08027340 004b
    b LAB_08027352                           @ 08027342 06e0
DWORD_08027344:
    .word  0x09de2b9e                     @ 08027344 9e2bde09
LAB_08027348:
    ldr r3, DWORD_0802734c                   @ 08027348 004b
    b LAB_08027352                           @ 0802734a 02e0
DWORD_0802734c:
    .word  0x09dd6832                     @ 0802734c 3268dd09
LAB_08027350:
    ldr r3, DWORD_080274a8                   @ 08027350 554b
LAB_08027352:
    ldr r0, DWORD_080274ac                   @ 08027352 5648
    ldr r1, DWORD_080274b0                   @ 08027354 5649
    adds r4,r0,r1    @ 08027356 4418
    ldrb r2,[r4,#0x0]                        @ 08027358 2278
    lsls r0,r2,#0x1d    @ 0802735a 5007
    lsrs r0,r0,#0x1d    @ 0802735c 400f
    str r0,[sp,#0x0]                         @ 0802735e 0090
    movs r0,#0x80    @ 08027360 8020
    movs r1,#0x87    @ 08027362 8721
    lsls r1,r1,#0x2    @ 08027364 8900
    movs r2,#0x1    @ 08027366 0122
    bl draw_decimal_with_offset              @ 08027368 fcf788fa
    ldr r1, DWORD_080274b4                   @ 0802736c 5149
    ldrb r3,[r1,#0x4]                        @ 0802736e 0b79
    lsrs r0,r3,#0x5    @ 08027370 5809
    cmp r0,#0x2                              @ 08027372 0228
    bhi LAB_08027378                         @ 08027374 00d8
    b LAB_0802747e                           @ 08027376 82e0
LAB_08027378:
    ldrb r1,[r1,#0x3]                        @ 08027378 c978
    lsls r0,r1,#0x1b    @ 0802737a c806
    lsrs r0,r0,#0x1d    @ 0802737c 400f
    cmp r0,#0x5                              @ 0802737e 0528
    bls LAB_0802747e                         @ 08027380 7dd9
    ldr r0, DWORD_080274b8                   @ 08027382 4d48
    bl game_str_id_to_row                    @ 08027384 cdf048fd
    ldr r2, DWORD_080274bc                   @ 08027388 4c4a
    lsls r0,r0,#0x10    @ 0802738a 0004
    lsrs r0,r0,#0x10    @ 0802738c 000c
    lsls r1,r0,#0x1    @ 0802738e 4100
    adds r1,r1,r0    @ 08027390 0918
    lsls r1,r1,#0x1    @ 08027392 4900
    ldrb r4,[r4,#0x0]                        @ 08027394 2478
    lsls r0,r4,#0x1d    @ 08027396 6007
    lsrs r0,r0,#0x1d    @ 08027398 400f
    adds r1,r1,r0    @ 0802739a 0918
    lsls r1,r1,#0x2    @ 0802739c 8900
    adds r1,r1,r2    @ 0802739e 8918
    ldr r1,[r1,#0x0]                         @ 080273a0 0968
    ldr r0, DWORD_080274c0                   @ 080273a2 4748
    adds r1,r1,r0    @ 080273a4 0918
    ldr r0, DWORD_080274c4                   @ 080273a6 4748
    movs r2,#0x84    @ 080273a8 8422
    lsls r2,r2,#0x2    @ 080273aa 9200
    ldr r3, DWORD_080274c8                   @ 080273ac 464b
    str r1,[sp,#0x0]                         @ 080273ae 0091
    movs r1,#0xd6    @ 080273b0 d621
    bl render_centered_text_to_bg_vram       @ 080273b2 fcf7effa
    ldr r5, DWORD_080274cc                   @ 080273b6 454d
    movs r6,#0x93    @ 080273b8 9326
    lsls r6,r6,#0x1    @ 080273ba 7600
    ldr r4, DWORD_080274d0                   @ 080273bc 444c
    adds r0,r5,#0x0    @ 080273be 281c
    movs r1,#0x40    @ 080273c0 4021
    adds r2,r6,#0x0    @ 080273c2 321c
    adds r3,r4,#0x0    @ 080273c4 231c
    bl write_tile_row_to_vram                @ 080273c6 c6f0c1fd
    ldrh r5,[r4,#0x0]                        @ 080273ca 2588
    lsls r0,r5,#0x1    @ 080273cc 6800
    adds r1,r0,#0x0    @ 080273ce 011c
    adds r1,#0x8    @ 080273d0 0831
    adds r1,r1,r4    @ 080273d2 0919
    adds r0,#0x10    @ 080273d4 1030
    adds r0,r0,r4    @ 080273d6 0019
    ldrh r1,[r1,#0x0]                        @ 080273d8 0988
    lsls r1,r1,#0x5    @ 080273da 4901
    adds r0,r0,r1    @ 080273dc 4018
    .hword 0x4680    @ 080273de 8046
    .hword 0x4645    @ 080273e0 4546
    adds r5,#0x8    @ 080273e2 0835
    movs r7,#0x0    @ 080273e4 0027
    .hword 0x4646    @ 080273e6 4646
    ldrh r6,[r6,#0x0]                        @ 080273e8 3688
    cmp r7,r6                                @ 080273ea b742
    bcs LAB_0802746e                         @ 080273ec 3fd2
    movs r0,#0xc0    @ 080273ee c020
    lsls r0,r0,#0x4    @ 080273f0 0001
    .hword 0x4684    @ 080273f2 8446
    ldr r1, DWORD_080274d4                   @ 080273f4 3749
    .hword 0x468a    @ 080273f6 8a46
    ldr r2, DWORD_080274d8                   @ 080273f8 374a
    .hword 0x4691    @ 080273fa 9146
LAB_080273fc:
    ldrh r0,[r5,#0x0]                        @ 080273fc 2888
    adds r5,#0x2    @ 080273fe 0235
    ldrh r4,[r5,#0x0]                        @ 08027400 2c88
    adds r5,#0x2    @ 08027402 0235
    movs r3,#0x3f    @ 08027404 3f23
    ands r3,r0    @ 08027406 0340
    movs r6,#0xff    @ 08027408 ff26
    lsls r6,r6,#0x8    @ 0802740a 3602
    ands r0,r6    @ 0802740c 3040
    movs r1,#0xc0    @ 0802740e c021
    lsls r1,r1,#0x13    @ 08027410 c904
    str r1,[sp,#0x10]                        @ 08027412 0491
    lsrs r1,r0,#0x3    @ 08027414 c108
    adds r0,r3,#0x0    @ 08027416 181c
    orrs r0,r1    @ 08027418 0843
    adds r2,r4,#0x0    @ 0802741a 221c
    .hword 0x4666    @ 0802741c 6646
    ands r2,r6    @ 0802741e 3240
    cmp r3,#0x1f                             @ 08027420 1f2b
    bls LAB_08027432                         @ 08027422 06d9
    ldr r0, DWORD_080274dc                   @ 08027424 2d48
    str r0,[sp,#0x10]                        @ 08027426 0490
    adds r0,r3,#0x0    @ 08027428 181c
    subs r0,#0x20    @ 0802742a 2038
    orrs r1,r0    @ 0802742c 0143
    lsls r0,r1,#0x10    @ 0802742e 0804
    lsrs r0,r0,#0x10    @ 08027430 000c
LAB_08027432:
    ldr r1, DWORD_080274cc                   @ 08027432 2649
    adds r0,r0,r1    @ 08027434 4018
    lsls r0,r0,#0x10    @ 08027436 0004
    lsrs r0,r0,#0x10    @ 08027438 000c
    cmp r0,r10                               @ 0802743a 5045
    bls LAB_08027446                         @ 0802743c 03d9
    ldr r3, DWORD_080274e0                   @ 0802743e 284b
    adds r0,r0,r3    @ 08027440 c018
    lsls r0,r0,#0x10    @ 08027442 0004
    lsrs r0,r0,#0x10    @ 08027444 000c
LAB_08027446:
    .hword 0x464e    @ 08027446 4e46
    ands r4,r6    @ 08027448 3440
    lsls r1,r0,#0x1    @ 0802744a 4100
    ldr r0,[sp,#0x10]                        @ 0802744c 0498
    adds r1,r1,r0    @ 0802744e 0918
    movs r3,#0x93    @ 08027450 9323
    lsls r3,r3,#0x1    @ 08027452 5b00
    adds r0,r4,r3    @ 08027454 e018
    orrs r2,r0    @ 08027456 0243
    movs r4,#0x40    @ 08027458 4024
    lsls r0,r4,#0x8    @ 0802745a 2002
    orrs r2,r0    @ 0802745c 0243
    strh r2,[r1,#0x0]                        @ 0802745e 0a80
    adds r0,r7,#0x1    @ 08027460 781c
    lsls r0,r0,#0x10    @ 08027462 0004
    lsrs r7,r0,#0x10    @ 08027464 070c
    .hword 0x4646    @ 08027466 4646
    ldrh r6,[r6,#0x0]                        @ 08027468 3688
    cmp r7,r6                                @ 0802746a b742
    bcc LAB_080273fc                         @ 0802746c c6d3
LAB_0802746e:
    ldr r0, DWORD_080274e4                   @ 0802746e 1d48
    movs r1,#0x80    @ 08027470 8021
    bl zero_fill_by_halfword                 @ 08027472 cdf0fffc
    ldr r0, DWORD_080274dc                   @ 08027476 1948
    movs r1,#0x80    @ 08027478 8021
    bl zero_fill_by_halfword                 @ 0802747a cdf0fbfc
LAB_0802747e:
    ldr r2, DWORD_080274b4                   @ 0802747e 0d4a
    movs r0,#0x3    @ 08027480 0320
    rsbs r0,r0,#0    @ 08027482 4042
    ldrb r1,[r2,#0x8]                        @ 08027484 117a
    ands r0,r1    @ 08027486 0840
    movs r1,#0x5    @ 08027488 0521
    rsbs r1,r1,#0    @ 0802748a 4942
    ands r0,r1    @ 0802748c 0840
    strb r0,[r2,#0x8]                        @ 0802748e 1072
    ldr r2, DWORD_080274e8                   @ 08027490 154a
    ldr r3, DWORD_080274ec                   @ 08027492 164b
    adds r2,r2,r3    @ 08027494 d218
    ldr r0, DWORD_080274f0                   @ 08027496 1648
    ldrh r4,[r2,#0x0]                        @ 08027498 1488
    ands r0,r4    @ 0802749a 2040
    movs r1,#0x40    @ 0802749c 4021
    orrs r0,r1    @ 0802749e 0843
    strh r0,[r2,#0x0]                        @ 080274a0 1080
    bl SUB_08026714                          @ 080274a2 fff737f9
    movs r0,r0    @ 080274a6 0000
DWORD_080274a8:
    .word  0x09dcaea0                     @ 080274a8 a0aedc09
DWORD_080274ac:
    .word  0x02000000                     @ 080274ac 00000002
DWORD_080274b0:
    .word  0x00006c2c                     @ 080274b0 2c6c0000
DWORD_080274b4:
    .word  0x02023360                     @ 080274b4 60330202
DWORD_080274b8:
    .word  0x00000be5                     @ 080274b8 e50b0000
DWORD_080274bc:
    .word  game_str_pointer_table         @ 080274bc 400f0008
DWORD_080274c0:
    .word  game_str_ja                    @ 080274c0 109cdb09
DWORD_080274c4:
    .word  0x000007c7                     @ 080274c4 c7070000
DWORD_080274c8:
    .word  0x00000f09                     @ 080274c8 090f0000
DWORD_080274cc:
    .word  0x00000bc1                     @ 080274cc c10b0000
DWORD_080274d0:
    .word  0x09b96514                     @ 080274d0 1465b909
DWORD_080274d4:
    .word  0x00000bff                     @ 080274d4 ff0b0000
DWORD_080274d8:
    .word  0x000003ff                     @ 080274d8 ff030000
DWORD_080274dc:
    .word  0x06000800                     @ 080274dc 00080006
DWORD_080274e0:
    .word  0xfffffc00                     @ 080274e0 00fcffff
DWORD_080274e4:
    .word  0x06001100                     @ 080274e4 00110006
DWORD_080274e8:
    .word  gPrng                          @ 080274e8 40000003
DWORD_080274ec:
    .word  0x00000202                     @ 080274ec 02020000
DWORD_080274f0:
    .word  0xffffc03f                     @ 080274f0 3fc0ffff

@ campaign_scene_handler dispatch table index 25. Trigger: gPrng+0x202 bits[13:6] == 0x19. Symmetric to run_campaign_step23_card_select_tick (0x08026fe4): (1) bl tick_campaign_card_select_display_state; (2) if returns 0: b SUB_08026714 to wait; (3) if returns nonzero: reads gPrng+0x202, increments bits[13:6] by 1, writes back, then b SUB_08026714 to advance to step 26. Steps 23 and 25 both use the same display state machine tick; they correspond to first and second entry into the card-select display phase.
@ 
@ Constants:
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6], mask = 0xffffc03f
run_campaign_step25_card_select_tick:
    bl tick_campaign_card_select_display_state @ 080274f4 06f008fe
    cmp r0,#0x0                              @ 080274f8 0028
    bne LAB_08027500                         @ 080274fa 01d1
    bl SUB_08026714                          @ 080274fc fff70af9
LAB_08027500:
    ldr r2, DWORD_08027520                   @ 08027500 074a
    ldr r5, DWORD_08027524                   @ 08027502 084d
    adds r2,r2,r5    @ 08027504 5219
    ldrh r3,[r2,#0x0]                        @ 08027506 1388
    lsls r1,r3,#0x12    @ 08027508 9904
    lsrs r1,r1,#0x18    @ 0802750a 090e
    adds r1,#0x1    @ 0802750c 0131
    movs r0,#0xff    @ 0802750e ff20
    ands r1,r0    @ 08027510 0140
    lsls r1,r1,#0x6    @ 08027512 8901
    ldr r0, DWORD_08027528                   @ 08027514 0448
    ands r0,r3    @ 08027516 1840
    orrs r0,r1    @ 08027518 0843
    strh r0,[r2,#0x0]                        @ 0802751a 1080
    bl SUB_08026714                          @ 0802751c fff7faf8
DWORD_08027520:
    .word  gPrng                          @ 08027520 40000003
DWORD_08027524:
    .word  0x00000202                     @ 08027524 02020000
DWORD_08027528:
    .word  0xffffc03f                     @ 08027528 3fc0ffff

@ Per-frame handler for campaign_scene_handler dispatch table index 26. Trigger: gPrng+0x202 bits[13:6] == 0x1a. Full duel_puzzle initialization sequence: (1) tick_aob_display_with_fadein; if returns 0 calls SUB_08026714 to wait; (2) clear DISPCNT shadow word to 0; (3) clear_oam_active_flags_in_hand_range; (4) zero_fill_by_halfword(0x02029e90, 0x10 halfwords); (5) clear [gPrng+0x23f] bit1 (0x02 mask); (6) zero_duel_scene_display_buffers; (7) clear [0x02023130+0x88*4] OAM cache field with 0xfffc03ff mask; (8) call find_card_index_in_rom_table with current hand card; (9) step_prng_and_get_rand15 then write rand15 to scene_ctx2 as initial seed; (10) fill_card_fs_display_entries_for_card_list; (11) init_duel_puzzle_field_and_hand_display; (12) init_duel_field_vram_layout; (13) compute pack_index (slot_type/5+9) and write OAM attrs; (14) increment gPrng+0x202 frame counter.
@ 
@ Constants:
@ - step_index=26 (0x1a)
@ - DISPCNT_SHADOW=word at 0x04000400 (cleared to 0)
@ - gPrng_scene_byte=gPrng+0x23f (bit1 cleared)
@ - OAM_cache_mask=0xfffc03ff
run_campaign_step26_init_duel_puzzle_scene:
    bl tick_aob_display_with_fadein          @ 0802752c 07f004fa
    cmp r0,#0x0                              @ 08027530 0028
    bne LAB_08027538                         @ 08027532 01d1
    bl SUB_08026714                          @ 08027534 fff7eef8
LAB_08027538:
    movs r1,#0x80    @ 08027538 8021
    lsls r1,r1,#0x13    @ 0802753a c904
    movs r0,#0x0    @ 0802753c 0020
    strh r0,[r1,#0x0]                        @ 0802753e 0880
    bl clear_oam_active_flags_in_hand_range  @ 08027540 d1f0e8fd
    ldr r0, DWORD_080275fc                   @ 08027544 2d48
    movs r1,#0x10    @ 08027546 1021
    bl zero_fill_by_halfword                 @ 08027548 cdf094fc
    ldr r6, DWORD_08027600                   @ 0802754c 2c4e
    .hword 0x46b0    @ 0802754e b046
    ldr r1, DWORD_08027604                   @ 08027550 2c49
    add r1,r8                                @ 08027552 4144
    movs r0,#0x2    @ 08027554 0220
    rsbs r0,r0,#0    @ 08027556 4042
    .hword 0x4681    @ 08027558 8146
    ldrb r2,[r1,#0x0]                        @ 0802755a 0a78
    ands r0,r2    @ 0802755c 1040
    strb r0,[r1,#0x0]                        @ 0802755e 0870
    bl zero_duel_scene_display_buffers       @ 08027560 a5f06cf9
    ldr r4, DWORD_08027608                   @ 08027564 284c
    movs r3,#0x88    @ 08027566 8823
    lsls r3,r3,#0x2    @ 08027568 9b00
    adds r2,r4,r3    @ 0802756a e218
    ldr r0,[r2,#0x0]                         @ 0802756c 1068
    ldr r1, DWORD_0802760c                   @ 0802756e 2749
    ands r0,r1    @ 08027570 0840
    str r0,[r2,#0x0]                         @ 08027572 1060
    movs r0,#0x8f    @ 08027574 8f20
    lsls r0,r0,#0x2    @ 08027576 8000
    add r0,r8                                @ 08027578 4044
    ldrh r0,[r0,#0x0]                        @ 0802757a 0088
    bl find_card_index_in_rom_table          @ 0802757c f7f746ff
    lsls r0,r0,#0x10    @ 08027580 0004
    lsrs r2,r0,#0x10    @ 08027582 020c
    movs r5,#0x7f    @ 08027584 7f25
    ands r2,r5    @ 08027586 2a40
    ldr r1, DWORD_08027610                   @ 08027588 2149
    adds r6,r4,r1    @ 0802758a 6618
    lsls r2,r2,#0x1    @ 0802758c 5200
    movs r7,#0x1    @ 0802758e 0127
    adds r1,r7,#0x0    @ 08027590 391c
    ldrb r3,[r6,#0x0]                        @ 08027592 3378
    ands r1,r3    @ 08027594 1940
    orrs r1,r2    @ 08027596 1143
    strb r1,[r6,#0x0]                        @ 08027598 3170
    lsrs r0,r0,#0x17    @ 0802759a c00d
    movs r5,#0x1    @ 0802759c 0125
    .hword 0x46aa    @ 0802759e aa46
    movs r1,#0x85    @ 080275a0 8521
    lsls r1,r1,#0x2    @ 080275a2 8900
    adds r4,r4,r1    @ 080275a4 6418
    ands r0,r7    @ 080275a6 3840
    .hword 0x4649    @ 080275a8 4946
    ldrb r2,[r4,#0x0]                        @ 080275aa 2278
    ands r1,r2    @ 080275ac 1140
    orrs r1,r0    @ 080275ae 0143
    strb r1,[r4,#0x0]                        @ 080275b0 2170
    bl tick_prng_lcg_rand15                  @ 080275b2 d1f09ffc
    ldr r1, DWORD_08027614                   @ 080275b6 1749
    lsls r0,r0,#0x10    @ 080275b8 0004
    lsrs r0,r0,#0x10    @ 080275ba 000c
    str r0,[r1,#0x0]                         @ 080275bc 0860
    movs r0,#0x0    @ 080275be 0020
    str r0,[r1,#0x4]                         @ 080275c0 4860
    str r0,[r1,#0x8]                         @ 080275c2 8860
    str r7,[r1,#0xc]                         @ 080275c4 cf60
    ldr r5, DWORD_08027618                   @ 080275c6 144d
    adds r0,r5,#0x0    @ 080275c8 281c
    adds r0,#0x39    @ 080275ca 3930
    ldrb r0,[r0,#0x0]                        @ 080275cc 0078
    lsls r0,r0,#0x1c    @ 080275ce 0007
    lsrs r0,r0,#0x1f    @ 080275d0 c00f
    str r0,[r1,#0x10]                        @ 080275d2 0861
    movs r0,#0x0    @ 080275d4 0020
    bl fill_card_fs_display_entries_for_card_list @ 080275d6 f7f7cdf9
    ldrb r3,[r5,#0x2]                        @ 080275da ab78
    lsls r0,r3,#0x1b    @ 080275dc d806
    lsrs r0,r0,#0x1b    @ 080275de c00e
    cmp r0,#0x19                             @ 080275e0 1928
    beq LAB_08027624                         @ 080275e2 1fd0
    cmp r0,#0x1a                             @ 080275e4 1a28
    beq LAB_08027658                         @ 080275e6 37d0
    ldr r0, DWORD_0802761c                   @ 080275e8 0c48
    add r0,r8                                @ 080275ea 4044
    ldrb r0,[r0,#0x0]                        @ 080275ec 0078
    lsls r1,r0,#0x5    @ 080275ee 4101
    ldr r0, DWORD_08027620                   @ 080275f0 0b48
    adds r1,r1,r0    @ 080275f2 0918
    movs r0,#0x1    @ 080275f4 0120
    bl load_card_fs_entry_to_struct          @ 080275f6 f7f7e9f8
    b LAB_08027672                           @ 080275fa 3ae0
DWORD_080275fc:
    .word  0x02029e90                     @ 080275fc 909e0202
DWORD_08027600:
    .word  gPrng                          @ 08027600 40000003
DWORD_08027604:
    .word  0x0000023f                     @ 08027604 3f020000
DWORD_08027608:
    .word  0x02023130                     @ 08027608 30310202
DWORD_0802760c:
    .word  0xfffc03ff                     @ 0802760c ff03fcff
DWORD_08027610:
    .word  0x00000213                     @ 08027610 13020000
DWORD_08027614:
    .word  0x0201e2a0                     @ 08027614 a0e20102
DWORD_08027618:
    .word  0x02023360                     @ 08027618 60330202
DWORD_0802761c:
    .word  0x0000023e                     @ 0802761c 3e020000
DWORD_08027620:
    .word  0x09e58d12                     @ 08027620 128de509
LAB_08027624:
    movs r0,#0x1    @ 08027624 0120
    bl fill_card_fs_display_entries_for_card_list @ 08027626 f7f7a5f9
    ldr r0, DWORD_08027650                   @ 0802762a 0948
    ldr r5, DWORD_08027654                   @ 0802762c 094d
    adds r0,r0,r5    @ 0802762e 4019
    ldrb r0,[r0,#0x0]                        @ 08027630 0078
    lsls r0,r0,#0x19    @ 08027632 4006
    lsrs r0,r0,#0x1c    @ 08027634 000f
    movs r1,#0x7f    @ 08027636 7f21
    ands r1,r0    @ 08027638 0140
    lsls r1,r1,#0x1    @ 0802763a 4900
    adds r0,r7,#0x0    @ 0802763c 381c
    ldrb r2,[r6,#0x0]                        @ 0802763e 3278
    ands r0,r2    @ 08027640 1040
    orrs r0,r1    @ 08027642 0843
    strb r0,[r6,#0x0]                        @ 08027644 3070
    .hword 0x4648    @ 08027646 4846
    ldrb r3,[r4,#0x0]                        @ 08027648 2378
    ands r0,r3    @ 0802764a 1840
    strb r0,[r4,#0x0]                        @ 0802764c 2070
    b LAB_08027672                           @ 0802764e 10e0
DWORD_08027650:
    .word  0x02000000                     @ 08027650 00000002
DWORD_08027654:
    .word  0x00006e57                     @ 08027654 576e0000
LAB_08027658:
    ldrh r5,[r5,#0xc]                        @ 08027658 ad89
    lsls r0,r5,#0x11    @ 0802765a 6804
    lsrs r0,r0,#0x18    @ 0802765c 000e
    lsls r1,r0,#0x3    @ 0802765e c100
    adds r1,r1,r0    @ 08027660 0918
    lsls r1,r1,#0x2    @ 08027662 8900
    subs r1,r1,r0    @ 08027664 091a
    lsls r1,r1,#0x3    @ 08027666 c900
    ldr r0, DWORD_080276c0                   @ 08027668 1548
    adds r1,r1,r0    @ 0802766a 0918
    movs r0,#0x1    @ 0802766c 0120
    bl fill_card_fs_display_entries          @ 0802766e f7f7eff8
LAB_08027672:
    bl init_duel_puzzle_field_and_hand_display @ 08027672 6bf0f5ff
    bl init_duel_field_vram_layout           @ 08027676 a5f045f9
    ldr r4, DWORD_080276c4                   @ 0802767a 124c
    ldr r0, DWORD_080276c8                   @ 0802767c 1248
    ldrb r0,[r0,#0x2]                        @ 0802767e 8078
    lsls r0,r0,#0x1b    @ 08027680 c006
    lsrs r0,r0,#0x1b    @ 08027682 c00e
    movs r1,#0x5    @ 08027684 0521
    bl __udivsi3                             @ 08027686 e7f0a9f8
    adds r0,#0x9    @ 0802768a 0930
    movs r5,#0x88    @ 0802768c 8825
    lsls r5,r5,#0x2    @ 0802768e ad00
    adds r4,r4,r5    @ 08027690 6419
    movs r5,#0xff    @ 08027692 ff25
    ands r0,r5    @ 08027694 2840
    lsls r0,r0,#0x2    @ 08027696 8000
    ldr r1, DWORD_080276cc                   @ 08027698 0c49
    ldrh r6,[r4,#0x0]                        @ 0802769a 2688
    ands r1,r6    @ 0802769c 3140
    orrs r1,r0    @ 0802769e 0143
    strh r1,[r4,#0x0]                        @ 080276a0 2180
    ldr r2, DWORD_080276d0                   @ 080276a2 0b4a
    ldr r0, DWORD_080276d4                   @ 080276a4 0b48
    adds r2,r2,r0    @ 080276a6 1218
    ldrh r3,[r2,#0x0]                        @ 080276a8 1388
    lsls r0,r3,#0x12    @ 080276aa 9804
    lsrs r0,r0,#0x18    @ 080276ac 000e
    adds r0,#0x1    @ 080276ae 0130
    ands r0,r5    @ 080276b0 2840
    lsls r0,r0,#0x6    @ 080276b2 8001
    ldr r1, DWORD_080276d8                   @ 080276b4 0849
    ands r1,r3    @ 080276b6 1940
    orrs r1,r0    @ 080276b8 0143
    strh r1,[r2,#0x0]                        @ 080276ba 1180
    bl SUB_08026714                          @ 080276bc fff72af8
DWORD_080276c0:
    .word  0x02001250                     @ 080276c0 50120002
DWORD_080276c4:
    .word  0x02023130                     @ 080276c4 30310202
DWORD_080276c8:
    .word  0x02023360                     @ 080276c8 60330202
DWORD_080276cc:
    .word  0xfffffc03                     @ 080276cc 03fcffff
DWORD_080276d0:
    .word  gPrng                          @ 080276d0 40000003
DWORD_080276d4:
    .word  0x00000202                     @ 080276d4 02020000
DWORD_080276d8:
    .word  0xffffc03f                     @ 080276d8 3fc0ffff

@ campaign_scene_handler dispatch table index 27. Trigger: gPrng+0x202 bits[13:6] == 0x1b. Sequence: (1) bl tick_duel_field_fadeout_step; (2) if returns 0 (fadeout not complete): b SUB_08026714 to wait; (3) if returns nonzero (fadeout complete): reads gPrng+0x202 halfword, increments bits[13:6] by 1, writes back, then b SUB_08026714 to advance to step 28. No direct r0 return value; both exit paths via b tail-call.
@ 
@ Constants:
@ - gPrng_step_ctr = gPrng+0x202 bits[13:6], mask = 0xffffc03f
run_campaign_step27_duel_field_fadeout_tick:
    bl tick_duel_field_fadeout_step          @ 080276dc a5f0acf9
    cmp r0,#0x0                              @ 080276e0 0028
    bne LAB_080276e8                         @ 080276e2 01d1
    bl SUB_08026714                          @ 080276e4 fff716f8
LAB_080276e8:
    ldr r2, DWORD_08027708                   @ 080276e8 074a
    ldr r1, DWORD_0802770c                   @ 080276ea 0849
    adds r2,r2,r1    @ 080276ec 5218
    ldrh r3,[r2,#0x0]                        @ 080276ee 1388
    lsls r1,r3,#0x12    @ 080276f0 9904
    lsrs r1,r1,#0x18    @ 080276f2 090e
    adds r1,#0x1    @ 080276f4 0131
    movs r0,#0xff    @ 080276f6 ff20
    ands r1,r0    @ 080276f8 0140
    lsls r1,r1,#0x6    @ 080276fa 8901
    ldr r0, DWORD_08027710                   @ 080276fc 0448
    ands r0,r3    @ 080276fe 1840
    orrs r0,r1    @ 08027700 0843
    strh r0,[r2,#0x0]                        @ 08027702 1080
    bl SUB_08026714                          @ 08027704 fff706f8
DWORD_08027708:
    .word  gPrng                          @ 08027708 40000003
DWORD_0802770c:
    .word  0x00000202                     @ 0802770c 02020000
DWORD_08027710:
    .word  0xffffc03f                     @ 08027710 3fc0ffff

@ campaign_scene_handler dispatch table entry index 28, duel field main frame animation tick phase. Calls tick_duel_field_main_frame to execute field main frame logic; if return is 0 (frame not complete) calls SUB_08026714 to advance scene state. In all cases reads gPrng+0x202 frame counter bits[13:6], increments by 1 taking low 8 bits, writes back to bits[13:6], then calls SUB_08026714 again to advance scene state machine.
@ 
@ Constants:
@ - state counter = gPrng+0x202 bits[13:6]
@ - counter mask = 0xffffc03f (clears bits[13:6])
run_campaign_step28_duel_field_tick:
    bl tick_duel_field_main_frame            @ 08027714 f7f736f9
    cmp r0,#0x0                              @ 08027718 0028
    bne LAB_08027720                         @ 0802771a 01d1
    bl SUB_08026714                          @ 0802771c fef7faff
LAB_08027720:
    ldr r2, DWORD_08027740                   @ 08027720 074a
    ldr r3, DWORD_08027744                   @ 08027722 084b
    adds r2,r2,r3    @ 08027724 d218
    ldrh r3,[r2,#0x0]                        @ 08027726 1388
    lsls r1,r3,#0x12    @ 08027728 9904
    lsrs r1,r1,#0x18    @ 0802772a 090e
    adds r1,#0x1    @ 0802772c 0131
    movs r0,#0xff    @ 0802772e ff20
    ands r1,r0    @ 08027730 0140
    lsls r1,r1,#0x6    @ 08027732 8901
    ldr r0, DWORD_08027748                   @ 08027734 0448
    ands r0,r3    @ 08027736 1840
    orrs r0,r1    @ 08027738 0843
    strh r0,[r2,#0x0]                        @ 0802773a 1080
    bl SUB_08026714                          @ 0802773c fef7eaff
DWORD_08027740:
    .word  gPrng                          @ 08027740 40000003
DWORD_08027744:
    .word  0x00000202                     @ 08027744 02020000
DWORD_08027748:
    .word  0xffffc03f                     @ 08027748 3fc0ffff

@ Duel field fadein tick handler for campaign_scene_handler dispatch table index 29. Trigger: gPrng+0x202 bits[13:6] == 0x1d. Calls tick_duel_field_fadein_step to advance duel field fadein; if returns 0 (not done) tail-calls SUB_08026714 to wait. If done reads [0x02023130+0x226] byte0 bit0: if bit0==1 calls SUB_08027768 (trigger scene-enter complete event); otherwise increments gPrng+0x202 frame counter bits[13:6] and tail-calls SUB_08026714 to advance to step 30.
@ 
@ Constants:
@ - step_index=29 (0x1d)
@ - state_flag_addr=0x02023130+0x226=0x02023356 bit0
@ - frame_ctr_mask=0xffffc03f
run_campaign_step29_duel_field_fadein_tick:
    bl tick_duel_field_fadein_step           @ 0802774c a5f086f9
    cmp r0,#0x0                              @ 08027750 0028
    bne LAB_08027758                         @ 08027752 01d1
    bl SUB_08026714                          @ 08027754 fef7deff
LAB_08027758:
    ldr r1, DWORD_08027770                   @ 08027758 0549
    ldr r4, DWORD_08027774                   @ 0802775a 064c
    adds r1,r1,r4    @ 0802775c 0919
    movs r0,#0x1    @ 0802775e 0120
    ldrb r1,[r1,#0x0]                        @ 08027760 0978
    ands r0,r1    @ 08027762 0840
    cmp r0,#0x0                              @ 08027764 0028
    beq LAB_08027778                         @ 08027766 07d0
SUB_08027768:
    movs r0,#0x80    @ 08027768 8020
    lsls r0,r0,#0x7    @ 0802776a c001
    b SUB_08027c82                           @ 0802776c 89e2
    .zero  0x2
DWORD_08027770:
    .word  0x02023130                     @ 08027770 30310202
DWORD_08027774:
    .word  0x00000226                     @ 08027774 26020000
LAB_08027778:
    ldr r2, DWORD_08027798                   @ 08027778 074a
    ldr r5, DWORD_0802779c                   @ 0802777a 084d
    adds r2,r2,r5    @ 0802777c 5219
    ldrh r3,[r2,#0x0]                        @ 0802777e 1388
    lsls r1,r3,#0x12    @ 08027780 9904
    lsrs r1,r1,#0x18    @ 08027782 090e
    adds r1,#0x1    @ 08027784 0131
    movs r0,#0xff    @ 08027786 ff20
    ands r1,r0    @ 08027788 0140
    lsls r1,r1,#0x6    @ 0802778a 8901
    ldr r0, DWORD_080277a0                   @ 0802778c 0448
    ands r0,r3    @ 0802778e 1840
    orrs r0,r1    @ 08027790 0843
    strh r0,[r2,#0x0]                        @ 08027792 1080
    bl SUB_08026714                          @ 08027794 fef7beff
DWORD_08027798:
    .word  gPrng                          @ 08027798 40000003
DWORD_0802779c:
    .word  0x00000202                     @ 0802779c 02020000
DWORD_080277a0:
    .word  0xffffc03f                     @ 080277a0 3fc0ffff

@ campaign_scene_handler dispatch table entry index 30, initializes pack card info display screen. Symmetric structure with run_campaign_step34_field_rule_display (0x08027a0c): first reads [0x02000000+0x6c2c] low 3 bits rule_type [1..5], selects different ROM tile data pointers per rule_type (5 sets). Then: (1) calls init_pack_card_info_screen_vram (FUN_0802b590, r1=1) for pack VRAM full init and card name render; (2) calls init_puzzle_card_name_line_buf (FUN_0802b8bc) to init line buffer; (3) calls render_card_stats_to_line_buf to render card stat numbers; (4) calls zero_sprite_vram_with_tile_seq (FUN_0802bd64) to clear sprite VRAM and write tilemap; (5) reads gPrng+0x202 frame counter and increments by 1; (6) tail-jumps b SUB_08027c22 to advance scene state machine.
@ 
@ Constants:
@ - rule_type = [0x02000000+0x6c2c] bits[2:0] [1..5]
@ - init_pack_card_info_screen_vram r1=1 (pack_index=1, fixed)
@ - gPrng+0x202 = frame count field bits[13:6]
run_campaign_step30_pack_card_info_display:
    ldr r0, DWORD_080277cc                   @ 080277a4 0948
    ldr r6, DWORD_080277d0                   @ 080277a6 0a4e
    adds r0,r0,r6    @ 080277a8 8019
    movs r1,#0x7    @ 080277aa 0721
    ldrb r0,[r0,#0x0]                        @ 080277ac 0078
    ands r1,r0    @ 080277ae 0140
    cmp r1,#0x1                              @ 080277b0 0129
    beq LAB_080277f4                         @ 080277b2 1fd0
    cmp r1,#0x2                              @ 080277b4 0229
    beq LAB_080277ec                         @ 080277b6 19d0
    cmp r1,#0x3                              @ 080277b8 0329
    beq LAB_080277e4                         @ 080277ba 13d0
    cmp r1,#0x4                              @ 080277bc 0429
    beq LAB_080277dc                         @ 080277be 0dd0
    ldr r0, DWORD_080277d4                   @ 080277c0 0448
    cmp r1,#0x5                              @ 080277c2 0529
    bne LAB_080277f6                         @ 080277c4 17d1
    ldr r1, DWORD_080277d8                   @ 080277c6 0449
    adds r0,r0,r1    @ 080277c8 4018
    b LAB_080277f6                           @ 080277ca 14e0
DWORD_080277cc:
    .word  0x02000000                     @ 080277cc 00000002
DWORD_080277d0:
    .word  0x00006c2c                     @ 080277d0 2c6c0000
DWORD_080277d4:
    .word  0x09dbe49a                     @ 080277d4 9ae4db09
DWORD_080277d8:
    .word  0x0003aade                     @ 080277d8 deaa0300
LAB_080277dc:
    ldr r0, DWORD_080277e0                   @ 080277dc 0048
    b LAB_080277f6                           @ 080277de 0ae0
DWORD_080277e0:
    .word  0x09ded29a                     @ 080277e0 9ad2de09
LAB_080277e4:
    ldr r0, DWORD_080277e8                   @ 080277e4 0048
    b LAB_080277f6                           @ 080277e6 06e0
DWORD_080277e8:
    .word  0x09de0e46                     @ 080277e8 460ede09
LAB_080277ec:
    ldr r0, DWORD_080277f0                   @ 080277ec 0048
    b LAB_080277f6                           @ 080277ee 02e0
DWORD_080277f0:
    .word  0x09dd4bb4                     @ 080277f0 b44bdd09
LAB_080277f4:
    ldr r0, DWORD_08027824                   @ 080277f4 0b48
LAB_080277f6:
    movs r1,#0x1    @ 080277f6 0121
    bl init_pack_card_info_screen_vram       @ 080277f8 03f0cafe
    bl init_puzzle_card_name_line_buf        @ 080277fc 04f05ef8
    bl render_card_stats_to_line_buf         @ 08027800 fdf742fa
    bl zero_sprite_vram_with_tile_seq        @ 08027804 04f0aefa
    ldr r2, DWORD_08027828                   @ 08027808 074a
    ldr r3, DWORD_0802782c                   @ 0802780a 084b
    adds r2,r2,r3    @ 0802780c d218
    ldrh r3,[r2,#0x0]                        @ 0802780e 1388
    lsls r1,r3,#0x12    @ 08027810 9904
    lsrs r1,r1,#0x18    @ 08027812 090e
    adds r1,#0x1    @ 08027814 0131
    movs r0,#0xff    @ 08027816 ff20
    ands r1,r0    @ 08027818 0140
    lsls r1,r1,#0x6    @ 0802781a 8901
    ldr r0, DWORD_08027830                   @ 0802781c 0448
    ands r0,r3    @ 0802781e 1840
    b SUB_08027c22                           @ 08027820 ffe1
    .zero  0x2
DWORD_08027824:
    .word  0x09dc9548                     @ 08027824 4895dc09
DWORD_08027828:
    .word  gPrng                          @ 08027828 40000003
DWORD_0802782c:
    .word  0x00000202                     @ 0802782c 02020000
DWORD_08027830:
    .word  0xffffc03f                     @ 08027830 3fc0ffff

@ Per-frame tick handler for campaign_scene_handler dispatch table index 31. Trigger: gPrng+0x202 bits[13:6] == 0x1f. Calls tick_lp_display_and_blend_step to advance LP digit sprite rendering and blend fade; if returns 0 (not done) calls SUB_08026714 to wait next frame. Otherwise clears gPrng+0x203 low 6 bits (AND 0x3f, slot_type mask) and clears bit6 (AND ~0x40) at gPrng+0x224+0x204, increments gPrng+0x202 frame counter bits[13:6], then tail-calls SUB_08026714 to advance to next step.
@ 
@ Constants:
@ - step_index=31 (0x1f)
@ - gPrng_slot_offset=0x203 (low 6 bits=slot_type index)
@ - slot_type_mask=0x3f
@ - gPrng_bit6_addr=gPrng+0x203 (AND ~0x40 clears bit6)
@ - frame_ctr_mask=0xffffc03f
run_campaign_step31_duel_lp_fadein_tick:
    bl tick_lp_display_and_blend_step        @ 08027834 04f0c6fa
    cmp r0,#0x0                              @ 08027838 0028
    bne LAB_08027840                         @ 0802783a 01d1
    bl SUB_08026714                          @ 0802783c fef76aff
LAB_08027840:
    ldr r2, DWORD_0802787c                   @ 08027840 0e4a
    ldr r4, DWORD_08027880                   @ 08027842 0f4c
    adds r1,r2,r4    @ 08027844 1119
    movs r0,#0x3f    @ 08027846 3f20
    ldrb r5,[r1,#0x0]                        @ 08027848 0d78
    ands r0,r5    @ 0802784a 2840
    strb r0,[r1,#0x0]                        @ 0802784c 0870
    movs r6,#0x81    @ 0802784e 8126
    lsls r6,r6,#0x2    @ 08027850 b600
    adds r1,r2,r6    @ 08027852 9119
    movs r0,#0x40    @ 08027854 4020
    rsbs r0,r0,#0    @ 08027856 4042
    ldrb r3,[r1,#0x0]                        @ 08027858 0b78
    ands r0,r3    @ 0802785a 1840
    strb r0,[r1,#0x0]                        @ 0802785c 0870
    subs r4,#0x1    @ 0802785e 013c
    adds r2,r2,r4    @ 08027860 1219
    ldrh r3,[r2,#0x0]                        @ 08027862 1388
    lsls r1,r3,#0x12    @ 08027864 9904
    lsrs r1,r1,#0x18    @ 08027866 090e
    adds r1,#0x1    @ 08027868 0131
    movs r0,#0xff    @ 0802786a ff20
    ands r1,r0    @ 0802786c 0140
    lsls r1,r1,#0x6    @ 0802786e 8901
    ldr r0, DWORD_08027884                   @ 08027870 0448
    ands r0,r3    @ 08027872 1840
    orrs r0,r1    @ 08027874 0843
    strh r0,[r2,#0x0]                        @ 08027876 1080
    bl SUB_08026714                          @ 08027878 fef74cff
DWORD_0802787c:
    .word  gPrng                          @ 0802787c 40000003
DWORD_08027880:
    .word  0x00000203                     @ 08027880 03020000
DWORD_08027884:
    .word  0xffffc03f                     @ 08027884 3fc0ffff

@ campaign_scene_handler (FUN_08025c94) dispatch table entry index 32, duel_puzzle display phase per-frame tick. Calls dispatch_puzzle_display_mode (FUN_0802be08) for LP digit render and mode dispatch; if return is 0 (scene not ready) calls SUB_08026714 to advance state. In all cases reads gPrng+0x202 bits[13:6] (frame count field), increments by 1 taking low 8 bits, shifts left 6, writes back to same field position, then calls SUB_08026714 to advance scene state machine again.
@ 
@ Constants:
@ - state counter = gPrng+0x202 bits[13:6]
@ - counter mask = 0xffffc03f (clears bits[13:6])
run_campaign_step32_puzzle_display_tick:
    bl dispatch_puzzle_display_mode          @ 08027888 04f0befa
    cmp r0,#0x0                              @ 0802788c 0028
    bne LAB_08027894                         @ 0802788e 01d1
    bl SUB_08026714                          @ 08027890 fef740ff
LAB_08027894:
    ldr r2, DWORD_080278b4                   @ 08027894 074a
    ldr r5, DWORD_080278b8                   @ 08027896 084d
    adds r2,r2,r5    @ 08027898 5219
    ldrh r3,[r2,#0x0]                        @ 0802789a 1388
    lsls r1,r3,#0x12    @ 0802789c 9904
    lsrs r1,r1,#0x18    @ 0802789e 090e
    adds r1,#0x1    @ 080278a0 0131
    movs r0,#0xff    @ 080278a2 ff20
    ands r1,r0    @ 080278a4 0140
    lsls r1,r1,#0x6    @ 080278a6 8901
    ldr r0, DWORD_080278bc                   @ 080278a8 0448
    ands r0,r3    @ 080278aa 1840
    orrs r0,r1    @ 080278ac 0843
    strh r0,[r2,#0x0]                        @ 080278ae 1080
    bl SUB_08026714                          @ 080278b0 fef730ff
DWORD_080278b4:
    .word  gPrng                          @ 080278b4 40000003
DWORD_080278b8:
    .word  0x00000202                     @ 080278b8 02020000
DWORD_080278bc:
    .word  0xffffc03f                     @ 080278bc 3fc0ffff

@ Per-frame tick handler for campaign_scene_handler dispatch table index 33. Trigger: gPrng+0x202 bits[13:6] == 0x21. Sequence: (1) call tick_lp_display_and_fadein_check; if returns 0 tail-calls SUB_08026714 to wait; (2) read [scene_ctx+0x68] LP prize amount, call accrue_money_with_cap to award coins; (3) read [scene_ctx2+0x89*4] battle_result field (0=no_result, 1=player_win, 2=draw, 3=opp_win); dispatch on four paths each reading next scene ID from a different EWRAM slot and triggering scene transition.
@ 
@ Constants:
@ - step_index=33 (0x21)
@ - scene_ctx=0x02023360
@ - LP_reward_offset=0x68 (scene_ctx+0x68=LP prize amount)
@ - scene_ctx2=0x0201e2a0
@ - battle_result_offset=0x89*4=0x224 (dword at 0x0201e4c4)
@ - battle_result: 1=player_win, 2=draw, 3=opp_win, 0/other=no_result
@ - player_slot_base=0x02006e60 (player slot list for next scene select)
run_campaign_step33_duel_reward_and_fadein_tick:
    bl tick_lp_display_and_fadein_check      @ 080278c0 04f090fa
    cmp r0,#0x0                              @ 080278c4 0028
    bne LAB_080278cc                         @ 080278c6 01d1
    bl SUB_08026714                          @ 080278c8 fef724ff
LAB_080278cc:
    ldr r4, DWORD_080278ec                   @ 080278cc 074c
    ldr r0,[r4,#0x68]                        @ 080278ce a06e
    bl accrue_money_with_cap                 @ 080278d0 d1f024fb
    ldr r0, DWORD_080278f0                   @ 080278d4 0648
    movs r6,#0x89    @ 080278d6 8926
    lsls r6,r6,#0x2    @ 080278d8 b600
    adds r0,r0,r6    @ 080278da 8019
    ldr r0,[r0,#0x0]                         @ 080278dc 0068
    cmp r0,#0x2                              @ 080278de 0228
    beq LAB_0802794c                         @ 080278e0 34d0
    cmp r0,#0x2                              @ 080278e2 0228
    bgt LAB_080278f4                         @ 080278e4 06dc
    cmp r0,#0x1                              @ 080278e6 0128
    beq LAB_080278fa                         @ 080278e8 07d0
    b LAB_080279d4                           @ 080278ea 73e0
DWORD_080278ec:
    .word  0x02023360                     @ 080278ec 60330202
DWORD_080278f0:
    .word  0x0201e2a0                     @ 080278f0 a0e20102
LAB_080278f4:
    cmp r0,#0x3                              @ 080278f4 0328
    beq LAB_0802799c                         @ 080278f6 51d0
    b LAB_080279d4                           @ 080278f8 6ce0
LAB_080278fa:
    ldr r5, DWORD_08027938                   @ 080278fa 0f4d
    ldrb r4,[r4,#0x2]                        @ 080278fc a478
    lsls r3,r4,#0x1b    @ 080278fe e306
    lsrs r0,r3,#0x19    @ 08027900 580e
    adds r0,r0,r5    @ 08027902 4019
    ldr r1, DWORD_0802793c                   @ 08027904 0d49
    adds r0,r0,r1    @ 08027906 4018
    ldrh r0,[r0,#0x0]                        @ 08027908 0088
    lsls r1,r0,#0x14    @ 0802790a 0105
    ldr r0, DWORD_08027940                   @ 0802790c 0c48
    cmp r1,r0                                @ 0802790e 8142
    bhi LAB_080279d4                         @ 08027910 60d8
    lsrs r2,r3,#0x19    @ 08027912 5a0e
    adds r2,r2,r5    @ 08027914 5219
    lsrs r0,r3,#0x19    @ 08027916 580e
    adds r0,r0,r5    @ 08027918 4019
    ldr r3, DWORD_0802793c                   @ 0802791a 084b
    adds r0,r0,r3    @ 0802791c c018
    ldrh r0,[r0,#0x0]                        @ 0802791e 0088
    lsls r1,r0,#0x14    @ 08027920 0105
    lsrs r1,r1,#0x14    @ 08027922 090d
    adds r1,#0x1    @ 08027924 0131
    adds r2,r2,r3    @ 08027926 d218
    ldr r4, DWORD_08027944                   @ 08027928 064c
    adds r0,r4,#0x0    @ 0802792a 201c
    ands r1,r0    @ 0802792c 0140
    ldr r0, DWORD_08027948                   @ 0802792e 0648
    ldrh r5,[r2,#0x0]                        @ 08027930 1588
    ands r0,r5    @ 08027932 2840
    b LAB_080279d0                           @ 08027934 4ce0
    .zero  0x2
DWORD_08027938:
    .word  0x02000000                     @ 08027938 00000002
DWORD_0802793c:
    .word  0x00006e60                     @ 0802793c 606e0000
DWORD_08027940:
    .word  0xffe00000                     @ 08027940 0000e0ff
DWORD_08027944:
    .word  0x00000fff                     @ 08027944 ff0f0000
DWORD_08027948:
    .word  0xfffff000                     @ 08027948 00f0ffff
LAB_0802794c:
    ldr r5, DWORD_0802798c                   @ 0802794c 0f4d
    ldrb r4,[r4,#0x2]                        @ 0802794e a478
    lsls r2,r4,#0x1b    @ 08027950 e206
    lsrs r0,r2,#0x19    @ 08027952 500e
    adds r0,r0,r5    @ 08027954 4019
    ldr r6, DWORD_08027990                   @ 08027956 0e4e
    adds r0,r0,r6    @ 08027958 8019
    ldr r0,[r0,#0x0]                         @ 0802795a 0068
    lsls r0,r0,#0xa    @ 0802795c 8002
    lsrs r0,r0,#0x16    @ 0802795e 800d
    ldr r1, DWORD_08027994                   @ 08027960 0c49
    cmp r0,r1                                @ 08027962 8842
    bhi LAB_080279d4                         @ 08027964 36d8
    lsrs r3,r2,#0x19    @ 08027966 530e
    adds r3,r3,r5    @ 08027968 5b19
    lsrs r0,r2,#0x19    @ 0802796a 500e
    adds r0,r0,r5    @ 0802796c 4019
    adds r0,r0,r6    @ 0802796e 8019
    ldr r0,[r0,#0x0]                         @ 08027970 0068
    lsls r0,r0,#0xa    @ 08027972 8002
    lsrs r0,r0,#0x16    @ 08027974 800d
    adds r3,r3,r6    @ 08027976 9b19
    adds r0,#0x1    @ 08027978 0130
    adds r1,#0x1    @ 0802797a 0131
    ands r0,r1    @ 0802797c 0840
    lsls r0,r0,#0xc    @ 0802797e 0003
    ldr r1,[r3,#0x0]                         @ 08027980 1968
    ldr r2, DWORD_08027998                   @ 08027982 054a
    ands r1,r2    @ 08027984 1140
    orrs r1,r0    @ 08027986 0143
    str r1,[r3,#0x0]                         @ 08027988 1960
    b LAB_080279d4                           @ 0802798a 23e0
DWORD_0802798c:
    .word  0x02000000                     @ 0802798c 00000002
DWORD_08027990:
    .word  0x00006e60                     @ 08027990 606e0000
DWORD_08027994:
    .word  0x000003fe                     @ 08027994 fe030000
DWORD_08027998:
    .word  0xffc00fff                     @ 08027998 ff0fc0ff
LAB_0802799c:
    ldr r5, DWORD_080279f4                   @ 0802799c 154d
    ldrb r4,[r4,#0x2]                        @ 0802799e a478
    lsls r3,r4,#0x1b    @ 080279a0 e306
    lsrs r0,r3,#0x19    @ 080279a2 580e
    adds r0,r0,r5    @ 080279a4 4019
    ldr r1, DWORD_080279f8                   @ 080279a6 1449
    adds r0,r0,r1    @ 080279a8 4018
    ldrh r0,[r0,#0x0]                        @ 080279aa 0088
    lsrs r1,r0,#0x6    @ 080279ac 8109
    ldr r0, DWORD_080279fc                   @ 080279ae 1348
    cmp r1,r0                                @ 080279b0 8142
    bhi LAB_080279d4                         @ 080279b2 0fd8
    lsrs r2,r3,#0x19    @ 080279b4 5a0e
    adds r2,r2,r5    @ 080279b6 5219
    lsrs r0,r3,#0x19    @ 080279b8 580e
    adds r0,r0,r5    @ 080279ba 4019
    ldr r3, DWORD_080279f8                   @ 080279bc 0e4b
    adds r0,r0,r3    @ 080279be c018
    ldrh r0,[r0,#0x0]                        @ 080279c0 0088
    lsrs r1,r0,#0x6    @ 080279c2 8109
    adds r1,#0x1    @ 080279c4 0131
    adds r2,r2,r3    @ 080279c6 d218
    lsls r1,r1,#0x6    @ 080279c8 8901
    movs r0,#0x3f    @ 080279ca 3f20
    ldrh r4,[r2,#0x0]                        @ 080279cc 1488
    ands r0,r4    @ 080279ce 2040
LAB_080279d0:
    orrs r0,r1    @ 080279d0 0843
    strh r0,[r2,#0x0]                        @ 080279d2 1080
LAB_080279d4:
    ldr r2, DWORD_08027a00                   @ 080279d4 0a4a
    ldr r5, DWORD_08027a04                   @ 080279d6 0b4d
    adds r2,r2,r5    @ 080279d8 5219
    ldrh r3,[r2,#0x0]                        @ 080279da 1388
    lsls r1,r3,#0x12    @ 080279dc 9904
    lsrs r1,r1,#0x18    @ 080279de 090e
    adds r1,#0x1    @ 080279e0 0131
    movs r0,#0xff    @ 080279e2 ff20
    ands r1,r0    @ 080279e4 0140
    lsls r1,r1,#0x6    @ 080279e6 8901
    ldr r0, DWORD_08027a08                   @ 080279e8 0748
    ands r0,r3    @ 080279ea 1840
    orrs r0,r1    @ 080279ec 0843
    strh r0,[r2,#0x0]                        @ 080279ee 1080
    bl SUB_08026714                          @ 080279f0 fef790fe
DWORD_080279f4:
    .word  0x02000000                     @ 080279f4 00000002
DWORD_080279f8:
    .word  0x00006e62                     @ 080279f8 626e0000
DWORD_080279fc:
    .word  0x000003fe                     @ 080279fc fe030000
DWORD_08027a00:
    .word  gPrng                          @ 08027a00 40000003
DWORD_08027a04:
    .word  0x00000202                     @ 08027a04 02020000
DWORD_08027a08:
    .word  0xffffc03f                     @ 08027a08 3fc0ffff

@ campaign_scene_handler dispatch table entry index 34, displays rule information after duel field initialization. Calls build_field_slot_bitmask to build field slot mask, then init_duel_field_icon_and_bg_vram to init field icon and BG VRAM. Reads [0x02000000+0x6c2c] low 3 bits as rule_type [1..5], selects ROM data pointer for each rule type (5 different graphic resources). Then calls draw_decimal_with_offset to render decimal number at screen position (turn_count or LP limit display), reads rule_type again and selects second set of data pointers, calls draw_decimal_with_offset again. Overall completes duel field rule number display.
@ 
@ Constants:
@ - rule_type = [0x02000000+0x6c2c] bits[2:0] [1..5]
@ - rule ROM data ptrs: case1=0x09dcad08, case2=0x09dd6636, case3=0x09de29ae, case4=0x09deee62, case5=0x09dba750+0x3ab1e
@ - draw position: col=0x40, row=0x84*4=0x210 (draw_decimal_with_offset args)
run_campaign_step34_field_rule_display:
    bl build_field_slot_bitmask              @ 08027a0c fcf772ff
    bl init_duel_field_icon_and_bg_vram      @ 08027a10 fcf7acf8
    ldr r0, DWORD_08027a3c                   @ 08027a14 0948
    ldr r6, DWORD_08027a40                   @ 08027a16 0a4e
    adds r0,r0,r6    @ 08027a18 8019
    movs r1,#0x7    @ 08027a1a 0721
    ldrb r0,[r0,#0x0]                        @ 08027a1c 0078
    ands r1,r0    @ 08027a1e 0140
    cmp r1,#0x1                              @ 08027a20 0129
    beq LAB_08027a64                         @ 08027a22 1fd0
    cmp r1,#0x2                              @ 08027a24 0229
    beq LAB_08027a5c                         @ 08027a26 19d0
    cmp r1,#0x3                              @ 08027a28 0329
    beq LAB_08027a54                         @ 08027a2a 13d0
    cmp r1,#0x4                              @ 08027a2c 0429
    beq LAB_08027a4c                         @ 08027a2e 0dd0
    ldr r3, DWORD_08027a44                   @ 08027a30 044b
    cmp r1,#0x5                              @ 08027a32 0529
    bne LAB_08027a66                         @ 08027a34 17d1
    ldr r0, DWORD_08027a48                   @ 08027a36 0448
    adds r3,r3,r0    @ 08027a38 1b18
    b LAB_08027a66                           @ 08027a3a 14e0
DWORD_08027a3c:
    .word  0x02000000                     @ 08027a3c 00000002
DWORD_08027a40:
    .word  0x00006c2c                     @ 08027a40 2c6c0000
DWORD_08027a44:
    .word  0x09dbff0e                     @ 08027a44 0effdb09
DWORD_08027a48:
    .word  0x0003ab1e                     @ 08027a48 1eab0300
LAB_08027a4c:
    ldr r3, DWORD_08027a50                   @ 08027a4c 004b
    b LAB_08027a66                           @ 08027a4e 0ae0
DWORD_08027a50:
    .word  0x09deee62                     @ 08027a50 62eede09
LAB_08027a54:
    ldr r3, DWORD_08027a58                   @ 08027a54 004b
    b LAB_08027a66                           @ 08027a56 06e0
DWORD_08027a58:
    .word  0x09de29ae                     @ 08027a58 ae29de09
LAB_08027a5c:
    ldr r3, DWORD_08027a60                   @ 08027a5c 004b
    b LAB_08027a66                           @ 08027a5e 02e0
DWORD_08027a60:
    .word  0x09dd6636                     @ 08027a60 3666dd09
LAB_08027a64:
    ldr r3, DWORD_08027aa4                   @ 08027a64 0f4b
LAB_08027a66:
    ldr r4, DWORD_08027aa8                   @ 08027a66 104c
    ldr r1, DWORD_08027aac                   @ 08027a68 1049
    adds r4,r4,r1    @ 08027a6a 6418
    ldrb r2,[r4,#0x0]                        @ 08027a6c 2278
    lsls r0,r2,#0x1d    @ 08027a6e 5007
    lsrs r0,r0,#0x1d    @ 08027a70 400f
    str r0,[sp,#0x0]                         @ 08027a72 0090
    movs r0,#0x40    @ 08027a74 4020
    movs r1,#0x84    @ 08027a76 8421
    lsls r1,r1,#0x2    @ 08027a78 8900
    ldr r2, DWORD_08027ab0                   @ 08027a7a 0d4a
    bl draw_decimal_with_offset              @ 08027a7c fbf7fefe
    movs r0,#0x7    @ 08027a80 0720
    ldrb r4,[r4,#0x0]                        @ 08027a82 2478
    ands r0,r4    @ 08027a84 2040
    cmp r0,#0x1                              @ 08027a86 0128
    beq LAB_08027ad4                         @ 08027a88 24d0
    cmp r0,#0x2                              @ 08027a8a 0228
    beq LAB_08027acc                         @ 08027a8c 1ed0
    cmp r0,#0x3                              @ 08027a8e 0328
    beq LAB_08027ac4                         @ 08027a90 18d0
    cmp r0,#0x4                              @ 08027a92 0428
    beq LAB_08027abc                         @ 08027a94 12d0
    ldr r3, DWORD_08027ab4                   @ 08027a96 074b
    cmp r0,#0x5                              @ 08027a98 0528
    bne LAB_08027ad6                         @ 08027a9a 1cd1
    ldr r4, DWORD_08027ab8                   @ 08027a9c 064c
    adds r3,r3,r4    @ 08027a9e 1b19
    b LAB_08027ad6                           @ 08027aa0 19e0
    .zero  0x2
DWORD_08027aa4:
    .word  0x09dcad08                     @ 08027aa4 08addc09
DWORD_08027aa8:
    .word  0x02000000                     @ 08027aa8 00000002
DWORD_08027aac:
    .word  0x00006c2c                     @ 08027aac 2c6c0000
DWORD_08027ab0:
    .word  0x0000010f                     @ 08027ab0 0f010000
DWORD_08027ab4:
    .word  0x09dc00b8                     @ 08027ab4 b800dc09
DWORD_08027ab8:
    .word  0x0003ab50                     @ 08027ab8 50ab0300
LAB_08027abc:
    ldr r3, DWORD_08027ac0                   @ 08027abc 004b
    b LAB_08027ad6                           @ 08027abe 0ae0
DWORD_08027ac0:
    .word  0x09def042                     @ 08027ac0 42f0de09
LAB_08027ac4:
    ldr r3, DWORD_08027ac8                   @ 08027ac4 004b
    b LAB_08027ad6                           @ 08027ac6 06e0
DWORD_08027ac8:
    .word  0x09de2b9e                     @ 08027ac8 9e2bde09
LAB_08027acc:
    ldr r3, DWORD_08027ad0                   @ 08027acc 004b
    b LAB_08027ad6                           @ 08027ace 02e0
DWORD_08027ad0:
    .word  0x09dd6832                     @ 08027ad0 3268dd09
LAB_08027ad4:
    ldr r3, DWORD_08027c2c                   @ 08027ad4 554b
LAB_08027ad6:
    ldr r0, DWORD_08027c30                   @ 08027ad6 5648
    ldr r5, DWORD_08027c34                   @ 08027ad8 564d
    adds r4,r0,r5    @ 08027ada 4419
    ldrb r6,[r4,#0x0]                        @ 08027adc 2678
    lsls r0,r6,#0x1d    @ 08027ade 7007
    lsrs r0,r0,#0x1d    @ 08027ae0 400f
    str r0,[sp,#0x0]                         @ 08027ae2 0090
    movs r0,#0x80    @ 08027ae4 8020
    movs r1,#0x87    @ 08027ae6 8721
    lsls r1,r1,#0x2    @ 08027ae8 8900
    movs r2,#0x1    @ 08027aea 0122
    bl draw_decimal_with_offset              @ 08027aec fbf7c6fe
    ldr r1, DWORD_08027c38                   @ 08027af0 5149
    ldrb r2,[r1,#0x4]                        @ 08027af2 0a79
    lsrs r0,r2,#0x5    @ 08027af4 5009
    cmp r0,#0x2                              @ 08027af6 0228
    bhi LAB_08027afc                         @ 08027af8 00d8
    b LAB_08027c02                           @ 08027afa 82e0
LAB_08027afc:
    ldrb r1,[r1,#0x3]                        @ 08027afc c978
    lsls r0,r1,#0x1b    @ 08027afe c806
    lsrs r0,r0,#0x1d    @ 08027b00 400f
    cmp r0,#0x5                              @ 08027b02 0528
    bls LAB_08027c02                         @ 08027b04 7dd9
    ldr r0, DWORD_08027c3c                   @ 08027b06 4d48
    bl game_str_id_to_row                    @ 08027b08 cdf086f9
    ldr r2, DWORD_08027c40                   @ 08027b0c 4c4a
    lsls r0,r0,#0x10    @ 08027b0e 0004
    lsrs r0,r0,#0x10    @ 08027b10 000c
    lsls r1,r0,#0x1    @ 08027b12 4100
    adds r1,r1,r0    @ 08027b14 0918
    lsls r1,r1,#0x1    @ 08027b16 4900
    ldrb r4,[r4,#0x0]                        @ 08027b18 2478
    lsls r0,r4,#0x1d    @ 08027b1a 6007
    lsrs r0,r0,#0x1d    @ 08027b1c 400f
    adds r1,r1,r0    @ 08027b1e 0918
    lsls r1,r1,#0x2    @ 08027b20 8900
    adds r1,r1,r2    @ 08027b22 8918
    ldr r1,[r1,#0x0]                         @ 08027b24 0968
    ldr r0, DWORD_08027c44                   @ 08027b26 4748
    adds r1,r1,r0    @ 08027b28 0918
    ldr r0, DWORD_08027c48                   @ 08027b2a 4748
    movs r2,#0x84    @ 08027b2c 8422
    lsls r2,r2,#0x2    @ 08027b2e 9200
    ldr r3, DWORD_08027c4c                   @ 08027b30 464b
    str r1,[sp,#0x0]                         @ 08027b32 0091
    movs r1,#0xd6    @ 08027b34 d621
    bl render_centered_text_to_bg_vram       @ 08027b36 fbf72dff
    ldr r5, DWORD_08027c50                   @ 08027b3a 454d
    movs r6,#0x93    @ 08027b3c 9326
    lsls r6,r6,#0x1    @ 08027b3e 7600
    ldr r4, DWORD_08027c54                   @ 08027b40 444c
    adds r0,r5,#0x0    @ 08027b42 281c
    movs r1,#0x40    @ 08027b44 4021
    adds r2,r6,#0x0    @ 08027b46 321c
    adds r3,r4,#0x0    @ 08027b48 231c
    bl write_tile_row_to_vram                @ 08027b4a c6f0fff9
    ldrh r3,[r4,#0x0]                        @ 08027b4e 2388
    lsls r0,r3,#0x1    @ 08027b50 5800
    adds r1,r0,#0x0    @ 08027b52 011c
    adds r1,#0x8    @ 08027b54 0831
    adds r1,r1,r4    @ 08027b56 0919
    adds r0,#0x10    @ 08027b58 1030
    adds r0,r0,r4    @ 08027b5a 0019
    ldrh r1,[r1,#0x0]                        @ 08027b5c 0988
    lsls r1,r1,#0x5    @ 08027b5e 4901
    adds r0,r0,r1    @ 08027b60 4018
    .hword 0x4680    @ 08027b62 8046
    .hword 0x4645    @ 08027b64 4546
    adds r5,#0x8    @ 08027b66 0835
    movs r7,#0x0    @ 08027b68 0027
    .hword 0x4644    @ 08027b6a 4446
    ldrh r4,[r4,#0x0]                        @ 08027b6c 2488
    cmp r7,r4                                @ 08027b6e a742
    bcs LAB_08027bf2                         @ 08027b70 3fd2
    movs r6,#0xc0    @ 08027b72 c026
    lsls r6,r6,#0x4    @ 08027b74 3601
    .hword 0x46b4    @ 08027b76 b446
    ldr r0, DWORD_08027c58                   @ 08027b78 3748
    .hword 0x4682    @ 08027b7a 8246
    ldr r1, DWORD_08027c5c                   @ 08027b7c 3749
    .hword 0x4689    @ 08027b7e 8946
LAB_08027b80:
    ldrh r0,[r5,#0x0]                        @ 08027b80 2888
    adds r5,#0x2    @ 08027b82 0235
    ldrh r4,[r5,#0x0]                        @ 08027b84 2c88
    adds r5,#0x2    @ 08027b86 0235
    movs r3,#0x3f    @ 08027b88 3f23
    ands r3,r0    @ 08027b8a 0340
    movs r2,#0xff    @ 08027b8c ff22
    lsls r2,r2,#0x8    @ 08027b8e 1202
    ands r0,r2    @ 08027b90 1040
    movs r6,#0xc0    @ 08027b92 c026
    lsls r6,r6,#0x13    @ 08027b94 f604
    str r6,[sp,#0x10]                        @ 08027b96 0496
    lsrs r1,r0,#0x3    @ 08027b98 c108
    adds r0,r3,#0x0    @ 08027b9a 181c
    orrs r0,r1    @ 08027b9c 0843
    adds r2,r4,#0x0    @ 08027b9e 221c
    .hword 0x4666    @ 08027ba0 6646
    ands r2,r6    @ 08027ba2 3240
    cmp r3,#0x1f                             @ 08027ba4 1f2b
    bls LAB_08027bb6                         @ 08027ba6 06d9
    ldr r0, DWORD_08027c60                   @ 08027ba8 2d48
    str r0,[sp,#0x10]                        @ 08027baa 0490
    adds r0,r3,#0x0    @ 08027bac 181c
    subs r0,#0x20    @ 08027bae 2038
    orrs r1,r0    @ 08027bb0 0143
    lsls r0,r1,#0x10    @ 08027bb2 0804
    lsrs r0,r0,#0x10    @ 08027bb4 000c
LAB_08027bb6:
    ldr r1, DWORD_08027c50                   @ 08027bb6 2649
    adds r0,r0,r1    @ 08027bb8 4018
    lsls r0,r0,#0x10    @ 08027bba 0004
    lsrs r0,r0,#0x10    @ 08027bbc 000c
    cmp r0,r10                               @ 08027bbe 5045
    bls LAB_08027bca                         @ 08027bc0 03d9
    ldr r3, DWORD_08027c64                   @ 08027bc2 284b
    adds r0,r0,r3    @ 08027bc4 c018
    lsls r0,r0,#0x10    @ 08027bc6 0004
    lsrs r0,r0,#0x10    @ 08027bc8 000c
LAB_08027bca:
    .hword 0x464e    @ 08027bca 4e46
    ands r4,r6    @ 08027bcc 3440
    lsls r1,r0,#0x1    @ 08027bce 4100
    ldr r0,[sp,#0x10]                        @ 08027bd0 0498
    adds r1,r1,r0    @ 08027bd2 0918
    movs r3,#0x93    @ 08027bd4 9323
    lsls r3,r3,#0x1    @ 08027bd6 5b00
    adds r0,r4,r3    @ 08027bd8 e018
    orrs r2,r0    @ 08027bda 0243
    movs r4,#0x40    @ 08027bdc 4024
    lsls r0,r4,#0x8    @ 08027bde 2002
    orrs r2,r0    @ 08027be0 0243
    strh r2,[r1,#0x0]                        @ 08027be2 0a80
    adds r0,r7,#0x1    @ 08027be4 781c
    lsls r0,r0,#0x10    @ 08027be6 0004
    lsrs r7,r0,#0x10    @ 08027be8 070c
    .hword 0x4646    @ 08027bea 4646
    ldrh r6,[r6,#0x0]                        @ 08027bec 3688
    cmp r7,r6                                @ 08027bee b742
    bcc LAB_08027b80                         @ 08027bf0 c6d3
LAB_08027bf2:
    ldr r0, DWORD_08027c68                   @ 08027bf2 1d48
    movs r1,#0x80    @ 08027bf4 8021
    bl zero_fill_by_halfword                 @ 08027bf6 cdf03df9
    ldr r0, DWORD_08027c60                   @ 08027bfa 1948
    movs r1,#0x80    @ 08027bfc 8021
    bl zero_fill_by_halfword                 @ 08027bfe cdf039f9
LAB_08027c02:
    ldr r2, DWORD_08027c38                   @ 08027c02 0d4a
    movs r0,#0x3    @ 08027c04 0320
    rsbs r0,r0,#0    @ 08027c06 4042
    ldrb r1,[r2,#0x8]                        @ 08027c08 117a
    ands r0,r1    @ 08027c0a 0840
    movs r1,#0x5    @ 08027c0c 0521
    rsbs r1,r1,#0    @ 08027c0e 4942
    ands r0,r1    @ 08027c10 0840
    strb r0,[r2,#0x8]                        @ 08027c12 1072
    ldr r2, DWORD_08027c6c                   @ 08027c14 154a
    ldr r3, DWORD_08027c70                   @ 08027c16 164b
    adds r2,r2,r3    @ 08027c18 d218
    ldr r0, DWORD_08027c74                   @ 08027c1a 1648
    ldrh r4,[r2,#0x0]                        @ 08027c1c 1488
    ands r0,r4    @ 08027c1e 2040
    movs r1,#0x40    @ 08027c20 4021
SUB_08027c22:
    orrs r0,r1    @ 08027c22 0843
    strh r0,[r2,#0x0]                        @ 08027c24 1080
    bl SUB_08026714                          @ 08027c26 fef775fd
    movs r0,r0    @ 08027c2a 0000
DWORD_08027c2c:
    .word  0x09dcaea0                     @ 08027c2c a0aedc09
DWORD_08027c30:
    .word  0x02000000                     @ 08027c30 00000002
DWORD_08027c34:
    .word  0x00006c2c                     @ 08027c34 2c6c0000
DWORD_08027c38:
    .word  0x02023360                     @ 08027c38 60330202
DWORD_08027c3c:
    .word  0x00000be5                     @ 08027c3c e50b0000
DWORD_08027c40:
    .word  game_str_pointer_table         @ 08027c40 400f0008
DWORD_08027c44:
    .word  game_str_ja                    @ 08027c44 109cdb09
DWORD_08027c48:
    .word  0x000007c7                     @ 08027c48 c7070000
DWORD_08027c4c:
    .word  0x00000f09                     @ 08027c4c 090f0000
DWORD_08027c50:
    .word  0x00000bc1                     @ 08027c50 c10b0000
DWORD_08027c54:
    .word  0x09b96514                     @ 08027c54 1465b909
DWORD_08027c58:
    .word  0x00000bff                     @ 08027c58 ff0b0000
DWORD_08027c5c:
    .word  0x000003ff                     @ 08027c5c ff030000
DWORD_08027c60:
    .word  0x06000800                     @ 08027c60 00080006
DWORD_08027c64:
    .word  0xfffffc00                     @ 08027c64 00fcffff
DWORD_08027c68:
    .word  0x06001100                     @ 08027c68 00110006
DWORD_08027c6c:
    .word  gPrng                          @ 08027c6c 40000003
DWORD_08027c70:
    .word  0x00000202                     @ 08027c70 02020000
DWORD_08027c74:
    .word  0xffffc03f                     @ 08027c74 3fc0ffff

@ Fast exit function for campaign_scene_handler; also serves as placeholder for steps 8/9/13..19 and the out-of-range (step > 0x22) path. Loads next scene handler pointer from player_state+0x224 = [0x0201e4c4] into r0, then falls into SUB_08027c82 (campaign_scene_handler full epilogue): restores sp (add sp,#0x14), pops r8/r9/r10 via r3/r4/r5 aliases, pops callee-save r4/r5/r6/r7, pops lr into r1, bx r1. r0 = [0x0201e4c4] returned to campaign_scene_handler caller as next dispatch target.
@ 
@ Constants:
@ - player_state_base = 0x0201e2a0
@ - next_handler_offset = 0x89*4 = 0x224
@ - next_handler_addr = 0x0201e4c4
exit_campaign_scene_with_next_handler:
    ldr r0, DAT_08027c94                     @ 08027c78 0648
    movs r5,#0x89    @ 08027c7a 8925
    lsls r5,r5,#0x2    @ 08027c7c ad00
    adds r0,r0,r5    @ 08027c7e 4019
    ldr r0,[r0,#0x0]                         @ 08027c80 0068
SUB_08027c82:
    add sp,#0x14                             @ 08027c82 05b0
    pop {r3,r4,r5}                           @ 08027c84 38bc
    .hword 0x4698    @ 08027c86 9846
    .hword 0x46a1    @ 08027c88 a146
    .hword 0x46aa    @ 08027c8a aa46
    pop {r4,r5,r6,r7}                        @ 08027c8c f0bc
    pop {r1}                                 @ 08027c8e 02bc
    bx r1                                    @ 08027c90 0847
    .zero  0x2
DAT_08027c94:
    .word  0x0201e2a0                     @ 08027c94 a0e20102

@ Builds campaign sprite row data for a given row_type r0 [0..8] and writes to VRAM buffer. Called by wrapper functions that pass a fixed row_type constant. Switch with 9 cases: case 0 copies 4 bytes from ROM DAT 0x09e3ef46 + bl memcpy; case 1 builds 14-byte name data from [0x02000000+0x6e48] (player name/level fields) + bl write_sprite_row_to_vram_buffer(count=0x16); case 2 reads scene_ctx+0x36/0x37 halfword, extracts bits[10:8]/bit[7], writes 4-byte struct to sp+0x1c; case 3 writes type=3 to sp+0x13c + bl write_sprite_row_to_vram_buffer(count=2); case 4 bl copy_bytes_by_halfword(src=0x03000288, len=0x118) + bl write_sprite_row_to_vram_buffer(count=0x8d*2); case 5 reads scene_ctx+0x39 bit4/bit3 into sp+0x140; case 6 reads scene_ctx+0x39 bit4 into sp+0x148; case 7 reads player_profile(0x0201e2a0)+0x10/+0x0 into sp+0x14c; case 8 writes type=8 to sp+0x154. r0 > 8 -> default (no write). Returns via pop{r0};bx r0 (no r0 semantic).
@ 
@ Constants:
@ - scene_ctx = 0x02023360
@ - player_profile = 0x0201e2a0
@ - player_name_src = 0x02000000+0x6e48 (14-byte name region)
@ - ROM_name_template = 0x09e3ef46 (case 0)
@ - scratch_buf_src = 0x03000288 (case 4, OBJ scratch)
@ - row_count_case1 = 0x16, row_count_case4 = 0x8d*2
build_campaign_sprite_row_by_type:
    push {r4,r5,r6,lr}                       @ 08027c98 70b5
    sub sp,#0x158                            @ 08027c9a d6b0
    cmp r0,#0x8                              @ 08027c9c 0828
    bls LAB_08027ca2                         @ 08027c9e 00d9
    b switchD_08027caa__default              @ 08027ca0 c6e0
LAB_08027ca2:
    lsls r0,r0,#0x2    @ 08027ca2 8000
    ldr r1, DAT_08027cac                     @ 08027ca4 0149
    adds r0,r0,r1    @ 08027ca6 4018
    ldr r0,[r0,#0x0]                         @ 08027ca8 0068
switchD_08027caa__switchD:
    .hword 0x4687    @ 08027caa 8746
DAT_08027cac:
    .word  0x08027cb0                     @ 08027cac b07c0208
switchD_08027caa__switchdataD_08027cb0:
    .word  0x08027cd4                     @ 08027cb0 d47c0208
    .word  0x08027ce8                     @ 08027cb4 e87c0208
    .word  0x08027d68                     @ 08027cb8 687d0208
    .word  0x08027db8                     @ 08027cbc b87d0208
    .word  0x08027d94                     @ 08027cc0 947d0208
    .word  0x08027dc6                     @ 08027cc4 c67d0208
    .word  0x08027de8                     @ 08027cc8 e87d0208
    .word  0x08027e08                     @ 08027ccc 087e0208
    .word  0x08027e24                     @ 08027cd0 247e0208
switchD_08027caa__caseD_0:
    ldr r1, DAT_08027ce4                     @ 08027cd4 0349
    .hword 0x4668    @ 08027cd6 6846
    movs r2,#0x4    @ 08027cd8 0422
    bl memcpy                                @ 08027cda e6f03ffe
    .hword 0x4668    @ 08027cde 6846
    b LAB_08027dfa                           @ 08027ce0 8be0
    .zero  0x2
DAT_08027ce4:
    .word  0x09e3ef46                     @ 08027ce4 46efe309
switchD_08027caa__caseD_1:
    add r1,sp,#0x4                           @ 08027ce8 01a9
    .hword 0x466c    @ 08027cea 6c46
    adds r4,#0x6    @ 08027cec 0634
    movs r0,#0x1    @ 08027cee 0120
    strh r0,[r1,#0x0]                        @ 08027cf0 0880
    movs r2,#0x0    @ 08027cf2 0022
    adds r6,r1,#0x0    @ 08027cf4 0e1c
    ldr r5, DAT_08027d58                     @ 08027cf6 184d
    ldr r0, DAT_08027d5c                     @ 08027cf8 1848
    adds r3,r5,r0    @ 08027cfa 2b18
LAB_08027cfc:
    adds r0,r4,r2    @ 08027cfc a018
    adds r1,r2,r3    @ 08027cfe d118
    ldrb r1,[r1,#0x0]                        @ 08027d00 0978
    strb r1,[r0,#0x0]                        @ 08027d02 0170
    adds r2,#0x1    @ 08027d04 0132
    cmp r2,#0xe                              @ 08027d06 0e2a
    ble LAB_08027cfc                         @ 08027d08 f8dd
    ldr r1, DAT_08027d60                     @ 08027d0a 1549
    adds r0,r5,r1    @ 08027d0c 6818
    ldrb r3,[r0,#0x0]                        @ 08027d0e 0378
    lsls r0,r3,#0x1d    @ 08027d10 5807
    lsrs r0,r0,#0x1d    @ 08027d12 400f
    movs r1,#0x8    @ 08027d14 0821
    rsbs r1,r1,#0    @ 08027d16 4942
    ldrb r2,[r4,#0xf]                        @ 08027d18 e27b
    ands r1,r2    @ 08027d1a 1140
    orrs r1,r0    @ 08027d1c 0143
    movs r0,#0x78    @ 08027d1e 7820
    ands r0,r3    @ 08027d20 1840
    movs r2,#0x79    @ 08027d22 7922
    rsbs r2,r2,#0    @ 08027d24 5242
    ands r1,r2    @ 08027d26 1140
    orrs r1,r0    @ 08027d28 0143
    lsrs r3,r3,#0x7    @ 08027d2a db09
    ldr r2, DAT_08027d64                     @ 08027d2c 0d4a
    adds r0,r5,r2    @ 08027d2e a818
    ldrb r0,[r0,#0x0]                        @ 08027d30 0078
    lsls r0,r0,#0x1    @ 08027d32 4000
    orrs r0,r3    @ 08027d34 1843
    lsls r0,r0,#0x10    @ 08027d36 0004
    lsrs r2,r0,#0x10    @ 08027d38 020c
    movs r3,#0x1    @ 08027d3a 0123
    ands r2,r3    @ 08027d3c 1a40
    lsls r2,r2,#0x7    @ 08027d3e d201
    movs r3,#0x7f    @ 08027d40 7f23
    ands r1,r3    @ 08027d42 1940
    orrs r1,r2    @ 08027d44 1143
    strb r1,[r4,#0xf]                        @ 08027d46 e173
    lsrs r0,r0,#0x11    @ 08027d48 400c
    strb r0,[r4,#0x10]                       @ 08027d4a 2074
    adds r0,r6,#0x0    @ 08027d4c 301c
    movs r1,#0x16    @ 08027d4e 1621
    bl write_sprite_row_to_vram_buffer       @ 08027d50 c5f082fd
    b switchD_08027caa__default              @ 08027d54 6ce0
    .zero  0x2
DAT_08027d58:
    .word  0x02000000                     @ 08027d58 00000002
DAT_08027d5c:
    .word  0x00006e48                     @ 08027d5c 486e0000
DAT_08027d60:
    .word  0x00006e57                     @ 08027d60 576e0000
DAT_08027d64:
    .word  0x00006e58                     @ 08027d64 586e0000
switchD_08027caa__caseD_2:
    add r0,sp,#0x1c                          @ 08027d68 07a8
    movs r1,#0x2    @ 08027d6a 0221
    strh r1,[r0,#0x0]                        @ 08027d6c 0180
    ldr r1, DAT_08027d90                     @ 08027d6e 0849
    ldrh r2,[r1,#0x36]                       @ 08027d70 ca8e
    lsls r3,r2,#0x17    @ 08027d72 d305
    lsrs r3,r3,#0x1e    @ 08027d74 9b0f
    adds r1,#0x37    @ 08027d76 3731
    ldrb r2,[r1,#0x0]                        @ 08027d78 0a78
    lsls r1,r2,#0x1e    @ 08027d7a 9107
    lsrs r1,r1,#0x1f    @ 08027d7c c90f
    lsls r1,r1,#0x2    @ 08027d7e 8900
    orrs r3,r1    @ 08027d80 0b43
    lsls r2,r2,#0x19    @ 08027d82 5206
    lsrs r2,r2,#0x1b    @ 08027d84 d20e
    lsls r2,r2,#0x3    @ 08027d86 d200
    orrs r3,r2    @ 08027d88 1343
    strh r3,[r0,#0x2]                        @ 08027d8a 4380
    b LAB_08027dfa                           @ 08027d8c 35e0
    .zero  0x2
DAT_08027d90:
    .word  0x02023360                     @ 08027d90 60330202
switchD_08027caa__caseD_4:
    add r4,sp,#0x20                          @ 08027d94 08ac
    movs r0,#0x4    @ 08027d96 0420
    strh r0,[r4,#0x0]                        @ 08027d98 2080
    .hword 0x4668    @ 08027d9a 6846
    adds r0,#0x22    @ 08027d9c 2230
    ldr r1, DAT_08027db4                     @ 08027d9e 0549
    movs r2,#0x8c    @ 08027da0 8c22
    lsls r2,r2,#0x1    @ 08027da2 5200
    bl copy_bytes_by_halfword                @ 08027da4 cdf07ef8
    movs r1,#0x8d    @ 08027da8 8d21
    lsls r1,r1,#0x1    @ 08027daa 4900
    adds r0,r4,#0x0    @ 08027dac 201c
    bl write_sprite_row_to_vram_buffer       @ 08027dae c5f053fd
    b switchD_08027caa__default              @ 08027db2 3de0
DAT_08027db4:
    .word  0x03000288                     @ 08027db4 88020003
switchD_08027caa__caseD_3:
    add r0,sp,#0x13c                         @ 08027db8 4fa8
    movs r1,#0x3    @ 08027dba 0321
    strh r1,[r0,#0x0]                        @ 08027dbc 0180
    movs r1,#0x2    @ 08027dbe 0221
    bl write_sprite_row_to_vram_buffer       @ 08027dc0 c5f04afd
    b switchD_08027caa__default              @ 08027dc4 34e0
switchD_08027caa__caseD_5:
    add r0,sp,#0x140                         @ 08027dc6 50a8
    movs r1,#0x5    @ 08027dc8 0521
    strh r1,[r0,#0x0]                        @ 08027dca 0180
    ldr r1, DAT_08027de4                     @ 08027dcc 0549
    adds r1,#0x39    @ 08027dce 3931
    ldrb r3,[r1,#0x0]                        @ 08027dd0 0b78
    lsls r1,r3,#0x1c    @ 08027dd2 1907
    lsrs r1,r1,#0x1f    @ 08027dd4 c90f
    movs r2,#0x1    @ 08027dd6 0122
    eors r1,r2    @ 08027dd8 5140
    strh r1,[r0,#0x2]                        @ 08027dda 4180
    lsls r3,r3,#0x1d    @ 08027ddc 5b07
    lsrs r3,r3,#0x1f    @ 08027dde db0f
    strh r3,[r0,#0x4]                        @ 08027de0 8380
    b LAB_08027e18                           @ 08027de2 19e0
DAT_08027de4:
    .word  0x02023360                     @ 08027de4 60330202
switchD_08027caa__caseD_6:
    add r0,sp,#0x148                         @ 08027de8 52a8
    movs r1,#0x6    @ 08027dea 0621
    strh r1,[r0,#0x0]                        @ 08027dec 0180
    ldr r1, DAT_08027e04                     @ 08027dee 0549
    adds r1,#0x39    @ 08027df0 3931
    ldrb r1,[r1,#0x0]                        @ 08027df2 0978
    lsls r1,r1,#0x1c    @ 08027df4 0907
    lsrs r1,r1,#0x1f    @ 08027df6 c90f
    strh r1,[r0,#0x2]                        @ 08027df8 4180
LAB_08027dfa:
    movs r1,#0x4    @ 08027dfa 0421
    bl write_sprite_row_to_vram_buffer       @ 08027dfc c5f02cfd
    b switchD_08027caa__default              @ 08027e00 16e0
    .zero  0x2
DAT_08027e04:
    .word  0x02023360                     @ 08027e04 60330202
switchD_08027caa__caseD_7:
    add r0,sp,#0x14c                         @ 08027e08 53a8
    movs r1,#0x7    @ 08027e0a 0721
    strh r1,[r0,#0x0]                        @ 08027e0c 0180
    ldr r2, DAT_08027e20                     @ 08027e0e 044a
    ldr r1,[r2,#0x10]                        @ 08027e10 1169
    strh r1,[r0,#0x2]                        @ 08027e12 4180
    ldr r1,[r2,#0x0]                         @ 08027e14 1168
    strh r1,[r0,#0x4]                        @ 08027e16 8180
LAB_08027e18:
    movs r1,#0x6    @ 08027e18 0621
    bl write_sprite_row_to_vram_buffer       @ 08027e1a c5f01dfd
    b switchD_08027caa__default              @ 08027e1e 07e0
DAT_08027e20:
    .word  0x0201e2a0                     @ 08027e20 a0e20102
switchD_08027caa__caseD_8:
    add r0,sp,#0x154                         @ 08027e24 55a8
    movs r1,#0x8    @ 08027e26 0821
    strh r1,[r0,#0x0]                        @ 08027e28 0180
    movs r1,#0x4    @ 08027e2a 0421
    bl write_sprite_row_to_vram_buffer       @ 08027e2c c5f014fd
switchD_08027caa__default:
    add sp,#0x158                            @ 08027e30 56b0
    pop {r4,r5,r6}                           @ 08027e32 70bc
    pop {r0}                                 @ 08027e34 01bc
    bx r0                                    @ 08027e36 0047

@ Minimal wrapper that calls build_campaign_sprite_row_by_type with fixed row_type=5. Called by tick_campaign_card_select_display_state (0x0802e108) in a specific display sub-state. Forms a type5/type6 sibling pair with invoke_build_campaign_sprite_row_type6 (0x08027e44). Body: push{lr}; movs r0,#5; bl build_campaign_sprite_row_by_type; pop{r0}; bx r0. No independent r0 return value.
@ 
@ Constants:
@ - row_type = 5 (sprite row type 5, scene_ctx+0x39 bit4/bit3 dual-flag path)
invoke_build_campaign_sprite_row_type5:
    push {lr}                                @ 08027e38 00b5
    movs r0,#0x5    @ 08027e3a 0520
    bl build_campaign_sprite_row_by_type     @ 08027e3c fff72cff
    pop {r0}                                 @ 08027e40 01bc
    bx r0                                    @ 08027e42 0047

@ Minimal wrapper that calls build_campaign_sprite_row_by_type with fixed row_type=6. Called by tick_campaign_card_select_display_state (0x0802e108) in a specific display sub-state. Body: push{lr}; movs r0,#6; bl build_campaign_sprite_row_by_type; pop{r0}; bx r0. Forms a type5/type6 sibling pair with invoke_build_campaign_sprite_row_type5 (0x08027e38). No independent r0 return value.
@ 
@ Constants:
@ - row_type = 6 (sprite row type 6, scene_ctx+0x39 bit4 flag path)
invoke_build_campaign_sprite_row_type6:
    push {lr}                                @ 08027e44 00b5
    movs r0,#0x6    @ 08027e46 0620
    bl build_campaign_sprite_row_by_type     @ 08027e48 fff726ff
    pop {r0}                                 @ 08027e4c 01bc
    bx r0                                    @ 08027e4e 0047
    ROM_INCBIN 0x27e50, 0x6c
    .word  0x08027ec0                     @ 08027ebc c07e0208
PTR_run_campaign_card_select_handler_0_08027ec0:
    .word  0x08027f00                     @ 08027ec0 007f0208
    .word  0x08027f48                     @ 08027ec4 487f0208
    .word  0x08027fcc                     @ 08027ec8 cc7f0208
    .word  0x080280bc                     @ 08027ecc bc800208
    .word  0x0802803c                     @ 08027ed0 3c800208
    .word  0x080280d0                     @ 08027ed4 d0800208
    .word  0x08028118                     @ 08027ed8 18810208
    .word  0x08028194                     @ 08027edc 94810208
    .word  0x08028402                     @ 08027ee0 02840208
    .word  0x080281d8                     @ 08027ee4 d8810208
    .word  0x0802826e                     @ 08027ee8 6e820208
    .word  0x080282a0                     @ 08027eec a0820208
    .word  0x080282ac                     @ 08027ef0 ac820208
    .word  0x080282c2                     @ 08027ef4 c2820208
    .word  0x080282f0                     @ 08027ef8 f0820208
    .word  0x080283e8                     @ 08027efc e8830208

@ Campaign card-select scene dispatch table (PTR_FUN_08027ec0) case 0 handler. No independent push prologue (inline exit fragment, inherits parent frame registers). Entry .hword 0x4668=mov r0,sp reads parent frame stack pointer; ldrh r1,[r0+2] reads SIO message sub_cmd; compares to 0x2c06 -- if not equal jumps LAB_08028404 (notifies parent frame no action taken). If equal: calls check_siocnt_link_ready to verify SIO ready; if not ready skips build_campaign_sprite_row_by_type(0); continues to read gPrng+OAM field to update OAM tile frame, then branches to LAB_080280b2 shared frame-end path. Called via PTR_FUN_08027ec0 entry index 0.
@ 
@ Params: r0=(none -- inline fragment, parent frame stack via mov r0,sp; no independent APCS input)
@ Returns: void (b LAB_08028404 shared epilogue)
@ Side effects: via build_campaign_sprite_row_by_type(0): VRAM sprite row written
@ Constants: SIO_CMD_MATCH=0x2c06; SPRITE_ROW_TYPE=0
run_campaign_card_select_handler_0:
    .hword 0x4668    @ 08027f00 6846
    ldrh r1,[r0,#0x2]                        @ 08027f02 4188
    ldr r0, DWORD_08027f10                   @ 08027f04 0248
    cmp r1,r0                                @ 08027f06 8142
    beq LAB_08027f14                         @ 08027f08 04d0
    movs r0,#0x0    @ 08027f0a 0020
    b LAB_08028404                           @ 08027f0c 7ae2
    .zero  0x2
DWORD_08027f10:
    .word  0x00002c06                     @ 08027f10 062c0000
LAB_08027f14:
    bl check_siocnt_link_ready               @ 08027f14 f7f740fa
    cmp r0,#0x0                              @ 08027f18 0028
    bne LAB_08027f22                         @ 08027f1a 02d1
    movs r0,#0x0    @ 08027f1c 0020
    bl build_campaign_sprite_row_by_type     @ 08027f1e fff7bbfe
LAB_08027f22:
    ldr r2, DWORD_08027f3c                   @ 08027f22 064a
    ldr r5, DWORD_08027f40                   @ 08027f24 064d
    adds r2,r2,r5    @ 08027f26 5219
    ldrh r3,[r2,#0x0]                        @ 08027f28 1388
    lsls r1,r3,#0x12    @ 08027f2a 9904
    lsrs r1,r1,#0x18    @ 08027f2c 090e
    adds r1,#0x1    @ 08027f2e 0131
    movs r0,#0xff    @ 08027f30 ff20
    ands r1,r0    @ 08027f32 0140
    lsls r1,r1,#0x6    @ 08027f34 8901
    ldr r0, DWORD_08027f44                   @ 08027f36 0348
    ands r0,r3    @ 08027f38 1840
    b LAB_080280b2                           @ 08027f3a bae0
DWORD_08027f3c:
    .word  gPrng                          @ 08027f3c 40000003
DWORD_08027f40:
    .word  0x00000202                     @ 08027f40 02020000
DWORD_08027f44:
    .word  0xffffc03f                     @ 08027f44 3fc0ffff

@ At index 1 of PTR_FUN_08027ec0 jump table (addr 0x08027ec4). Inline exit fragment, no push prologue; accesses parent frame data via r4 (= .hword 0x466c -> mov r4,sp; adds r4,#2 => sp+2 card data ptr). Copies r4+0..0xe (14 bytes) to destination struct (0x02023360+0xe), modifies 0x02023360+0x1d bit fields, handles r4[0xf] bit 0 (set/clear 0x02023360+0x1d bit 0x8), copies r4[0x10] bits to 0x02023360+0x1d, then increments gPrng+0x202 step counter field (+1 step) and branches to FUN_08028402 (parent frame epilogue). Syncs selected card data fields to display state struct 0x02023360 and advances card select step.
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360 (campaign card select display state base)
@ FIELD_COPY_LEN = 0xe (field copy length in bytes)
@ STEP_CTR_OFFSET = 0x202 (gPrng+0x202 step counter halfword)
@ gPrng = 0x03000040
run_campaign_card_select_handler_1:
    .hword 0x466c    @ 08027f48 6c46
    adds r4,#0x2    @ 08027f4a 0234
    movs r2,#0x0    @ 08027f4c 0022
    ldr r6, DWORD_08027fb8                   @ 08027f4e 1a4e
    ldr r5, DWORD_08027fbc                   @ 08027f50 1a4d
    adds r3,r5,#0x0    @ 08027f52 2b1c
    adds r3,#0xe    @ 08027f54 0e33
LAB_08027f56:
    adds r0,r2,r3    @ 08027f56 d018
    adds r1,r4,r2    @ 08027f58 a118
    ldrb r1,[r1,#0x0]                        @ 08027f5a 0978
    strb r1,[r0,#0x0]                        @ 08027f5c 0170
    adds r2,#0x1    @ 08027f5e 0132
    cmp r2,#0xe                              @ 08027f60 0e2a
    ble LAB_08027f56                         @ 08027f62 f8dd
    ldrb r3,[r4,#0xf]                        @ 08027f64 e37b
    lsls r1,r3,#0x1d    @ 08027f66 5907
    lsrs r1,r1,#0x1d    @ 08027f68 490f
    movs r0,#0x8    @ 08027f6a 0820
    rsbs r0,r0,#0    @ 08027f6c 4042
    ldrb r2,[r5,#0x1d]                       @ 08027f6e 6a7f
    ands r0,r2    @ 08027f70 1040
    orrs r0,r1    @ 08027f72 0843
    movs r1,#0x78    @ 08027f74 7821
    ands r1,r3    @ 08027f76 1940
    movs r2,#0x79    @ 08027f78 7922
    rsbs r2,r2,#0    @ 08027f7a 5242
    ands r0,r2    @ 08027f7c 1040
    orrs r0,r1    @ 08027f7e 0843
    strb r0,[r5,#0x1d]                       @ 08027f80 6877
    lsls r3,r3,#0x18    @ 08027f82 1b06
    lsrs r3,r3,#0x1f    @ 08027f84 db0f
    ldrb r4,[r4,#0x10]                       @ 08027f86 247c
    lsls r0,r4,#0x1    @ 08027f88 6000
    orrs r0,r3    @ 08027f8a 1843
    movs r1,#0x3f    @ 08027f8c 3f21
    ands r0,r1    @ 08027f8e 0840
    lsls r0,r0,#0xf    @ 08027f90 c003
    ldr r1,[r5,#0x1c]                        @ 08027f92 e969
    ldr r2, DWORD_08027fc0                   @ 08027f94 0a4a
    ands r1,r2    @ 08027f96 1140
    orrs r1,r0    @ 08027f98 0143
    str r1,[r5,#0x1c]                        @ 08027f9a e961
    ldr r4, DWORD_08027fc4                   @ 08027f9c 094c
    adds r3,r6,r4    @ 08027f9e 3319
    ldrh r2,[r3,#0x0]                        @ 08027fa0 1a88
    lsls r1,r2,#0x12    @ 08027fa2 9104
    lsrs r1,r1,#0x18    @ 08027fa4 090e
    adds r1,#0x1    @ 08027fa6 0131
    movs r0,#0xff    @ 08027fa8 ff20
    ands r1,r0    @ 08027faa 0140
    lsls r1,r1,#0x6    @ 08027fac 8901
    ldr r0, DWORD_08027fc8                   @ 08027fae 0648
    ands r0,r2    @ 08027fb0 1040
    orrs r0,r1    @ 08027fb2 0843
    strh r0,[r3,#0x0]                        @ 08027fb4 1880
    b finalize_campaign_card_select_frame    @ 08027fb6 24e2
DWORD_08027fb8:
    .word  gPrng                          @ 08027fb8 40000003
DWORD_08027fbc:
    .word  0x02023360                     @ 08027fbc 60330202
DWORD_08027fc0:
    .word  0xffe07fff                     @ 08027fc0 ff7fe0ff
DWORD_08027fc4:
    .word  0x00000202                     @ 08027fc4 02020000
DWORD_08027fc8:
    .word  0xffffc03f                     @ 08027fc8 3fc0ffff

@ At index 2 of PTR_FUN_08027ec0 jump table (0x08027ec8). Inline exit fragment, no push prologue. Reads parent frame r0 (sp, .hword 0x4668=mov r0,sp) [r0+2] halfword: extracts bits[1:0] writes to 0x02023360+0x36 bits[8:7] (lsls #7), clears and ORs in; extracts bit[2] writes to 0x02023360+0x37 bits[1:0]; extracts bits[7:3] writes to same byte bits[6:2]. Then checks 0x02023360+0x36 bits[10:9] (lsls #5; lsrs #0x1e): if <= 2 branches to FUN_08028402; otherwise reads gPrng+0x202 step field, loads 0x02023360+step*2 halfword, ANDs with mask then merges high bits (0xf0<<3=0x780), writes back to gPrng+0x202 step word.
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360
@ SP_DATA_OFFSET = 0x2 (parent frame [sp+2] halfword = current card mode word)
@ MASK_CLEAR_HOFS = 0xfffffe7f (0x02023360+0x36 clear bits[8:7])
@ STEP_HIGH_BITS = 0x780 (0xf0 << 3, step high bits mask)
run_campaign_card_select_handler_2:
    ldr r3, DWORD_08028028                   @ 08027fcc 164b
    .hword 0x4668    @ 08027fce 6846
    ldrh r2,[r0,#0x2]                        @ 08027fd0 4288
    movs r1,#0x3    @ 08027fd2 0321
    ands r1,r2    @ 08027fd4 1140
    lsls r1,r1,#0x7    @ 08027fd6 c901
    ldr r0, DWORD_0802802c                   @ 08027fd8 1448
    ldrh r5,[r3,#0x36]                       @ 08027fda dd8e
    ands r0,r5    @ 08027fdc 2840
    orrs r0,r1    @ 08027fde 0843
    strh r0,[r3,#0x36]                       @ 08027fe0 d886
    movs r0,#0x4    @ 08027fe2 0420
    ands r0,r2    @ 08027fe4 1040
    lsls r0,r0,#0x10    @ 08027fe6 0004
    adds r4,r3,#0x0    @ 08027fe8 1c1c
    adds r4,#0x37    @ 08027fea 3734
    lsrs r0,r0,#0x12    @ 08027fec 800c
    lsls r0,r0,#0x1    @ 08027fee 4000
    movs r1,#0x3    @ 08027ff0 0321
    rsbs r1,r1,#0    @ 08027ff2 4942
    ldrb r5,[r4,#0x0]                        @ 08027ff4 2578
    ands r1,r5    @ 08027ff6 2940
    orrs r1,r0    @ 08027ff8 0143
    movs r0,#0xf8    @ 08027ffa f820
    ands r0,r2    @ 08027ffc 1040
    lsrs r0,r0,#0x1    @ 08027ffe 4008
    movs r2,#0x7d    @ 08028000 7d22
    rsbs r2,r2,#0    @ 08028002 5242
    ands r1,r2    @ 08028004 1140
    orrs r1,r0    @ 08028006 0143
    strb r1,[r4,#0x0]                        @ 08028008 2170
    ldrh r3,[r3,#0x36]                       @ 0802800a db8e
    lsls r0,r3,#0x17    @ 0802800c d805
    lsrs r0,r0,#0x1e    @ 0802800e 800f
    cmp r0,#0x2                              @ 08028010 0228
    bhi LAB_08028016                         @ 08028012 00d8
    b finalize_campaign_card_select_frame    @ 08028014 f5e1
LAB_08028016:
    ldr r0, DWORD_08028030                   @ 08028016 0648
    ldr r1, DWORD_08028034                   @ 08028018 0649
    adds r0,r0,r1    @ 0802801a 4018
    ldr r1, DWORD_08028038                   @ 0802801c 0649
    ldrh r2,[r0,#0x0]                        @ 0802801e 0288
    ands r1,r2    @ 08028020 1140
    movs r3,#0xa0    @ 08028022 a023
    lsls r3,r3,#0x3    @ 08028024 db00
    b LAB_080281c0                           @ 08028026 cbe0
DWORD_08028028:
    .word  0x02023360                     @ 08028028 60330202
DWORD_0802802c:
    .word  0xfffffe7f                     @ 0802802c 7ffeffff
DWORD_08028030:
    .word  gPrng                          @ 08028030 40000003
DWORD_08028034:
    .word  0x00000202                     @ 08028034 02020000
DWORD_08028038:
    .word  0xffffc03f                     @ 08028038 3fc0ffff

@ At index 4 of PTR_FUN_08027ec0 jump table (0x08027ed0). Inline exit fragment, no push prologue. Reads parent frame r3 (.hword 0x466b=mov r3,sp; adds r3,#2 => sp+2 = current card entry ptr). Loads card field from 0x02023360+0x17, extracts 5-bit value and writes to 0x0201e2a0+0x1e bits[7:3] (lsls #5); writes r5-sourced data to 0x0201e2a0+0x1f..0x34 (22-byte loop copy); reads [r5+4] flag, eors 1 (flips low bit), calls fill_card_fs_display_entries; reads gPrng+0x202 step word, checks bits[7:2] == 0x8 or 0x3c to decide branch path (write gPrng step +1 or direct epilogue). Fills card FS display data into EWRAM display buffer and updates step state.
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360
@ CARD_DATA_BASE = 0x0201e2a0 (card data EWRAM base, entry write target)
@ FS_DATA_LEN = 0x16 (22 bytes data copy)
@ STEP_MODE_8 = 0x8 (step mode A)
@ STEP_MODE_3C = 0x3c (step mode B)
run_campaign_card_select_handler_4:
    .hword 0x466b    @ 0802803c 6b46
    adds r3,#0x2    @ 0802803e 0233
    ldr r0, DWORD_08028088                   @ 08028040 1148
    ldrb r4,[r3,#0x17]                       @ 08028042 dc7d
    lsls r2,r4,#0x5    @ 08028044 6201
    movs r1,#0x1f    @ 08028046 1f21
    ldrb r5,[r0,#0x1e]                       @ 08028048 857f
    ands r1,r5    @ 0802804a 2940
    orrs r1,r2    @ 0802804c 1143
    strb r1,[r0,#0x1e]                       @ 0802804e 8177
    movs r2,#0x0    @ 08028050 0022
    ldr r5, DWORD_0802808c                   @ 08028052 0e4d
    adds r4,r0,#0x0    @ 08028054 041c
    adds r4,#0x1f    @ 08028056 1f34
LAB_08028058:
    adds r0,r2,r4    @ 08028058 1019
    adds r1,r3,r2    @ 0802805a 9918
    ldrb r1,[r1,#0x0]                        @ 0802805c 0978
    strb r1,[r0,#0x0]                        @ 0802805e 0170
    adds r2,#0x1    @ 08028060 0132
    cmp r2,#0x16                             @ 08028062 162a
    ble LAB_08028058                         @ 08028064 f8dd
    ldr r0,[r5,#0x4]                         @ 08028066 6868
    movs r1,#0x1    @ 08028068 0121
    eors r0,r1    @ 0802806a 4840
    adds r1,r3,#0x0    @ 0802806c 191c
    bl fill_card_fs_display_entries          @ 0802806e f6f7effb
    ldr r0, DWORD_08028090                   @ 08028072 0748
    ldr r1, DWORD_08028094                   @ 08028074 0749
    adds r2,r0,r1    @ 08028076 4218
    ldrh r1,[r2,#0x0]                        @ 08028078 1188
    lsls r0,r1,#0x12    @ 0802807a 8804
    lsrs r0,r0,#0x18    @ 0802807c 000e
    cmp r0,#0x8                              @ 0802807e 0828
    beq LAB_08028098                         @ 08028080 0ad0
    cmp r0,#0x3c                             @ 08028082 3c28
    beq LAB_080280a8                         @ 08028084 10d0
    b finalize_campaign_card_select_frame    @ 08028086 bce1
DWORD_08028088:
    .word  0x02023360                     @ 08028088 60330202
DWORD_0802808c:
    .word  0x0201e2a0                     @ 0802808c a0e20102
DWORD_08028090:
    .word  gPrng                          @ 08028090 40000003
DWORD_08028094:
    .word  0x00000202                     @ 08028094 02020000
LAB_08028098:
    ldr r0, DWORD_080280a4                   @ 08028098 0248
    ands r0,r1    @ 0802809a 0840
    movs r3,#0xa0    @ 0802809c a023
    lsls r3,r3,#0x2    @ 0802809e 9b00
    adds r1,r3,#0x0    @ 080280a0 191c
    b LAB_080280b2                           @ 080280a2 06e0
DWORD_080280a4:
    .word  0xffffc03f                     @ 080280a4 3fc0ffff
LAB_080280a8:
    ldr r0, DWORD_080280b8                   @ 080280a8 0348
    ands r0,r1    @ 080280aa 0840
    movs r4,#0x8c    @ 080280ac 8c24
    lsls r4,r4,#0x5    @ 080280ae 6401
    adds r1,r4,#0x0    @ 080280b0 211c
LAB_080280b2:
    orrs r0,r1    @ 080280b2 0843
    strh r0,[r2,#0x0]                        @ 080280b4 1080
    b finalize_campaign_card_select_frame    @ 080280b6 a4e1
DWORD_080280b8:
    .word  0xffffc03f                     @ 080280b8 3fc0ffff

@ At index 3 of PTR_FUN_08027ec0 jump table (0x08027ecc). Shortest inline exit fragment (8 instructions), no push prologue. Reads byte at 0x02023360+0x36, sets bit 5 (OR 0x20), writes back; then branches to FUN_08028402 (parent frame epilogue). Sets bit5 of display state word at offset 0x36 in campaign card select display context, then immediately returns to parent frame. No parent frame data read.
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360
@ STATUS_OFFSET = 0x36 (status byte offset)
@ READY_BIT = 0x20 (bit5, set to indicate a ready/loaded state)
run_campaign_card_select_handler_3:
    ldr r1, DWORD_080280cc                   @ 080280bc 0349
    adds r1,#0x36    @ 080280be 3631
    movs r0,#0x20    @ 080280c0 2020
    ldrb r5,[r1,#0x0]                        @ 080280c2 0d78
    orrs r0,r5    @ 080280c4 2843
    strb r0,[r1,#0x0]                        @ 080280c6 0870
    b finalize_campaign_card_select_frame    @ 080280c8 9be1
    .zero  0x2
DWORD_080280cc:
    .word  0x02023360                     @ 080280cc 60330202

@ At index 5 of PTR_FUN_08027ec0 jump table (0x08027ed4). Inline exit fragment, no push prologue. Reads parent frame r0 (.hword 0x4668=mov r0,sp), loads current sprite state byte from 0x02023360+0x39, updates bit3 from [r0+2] halfword bit0 (lsls r1,#3) and bit2 from [sp+4] bit0, then ORs 0x10 (bit4 fixed set), writes back to 0x02023360+0x39; calls sync_state_and_init_sprite(r0=0x24) to init sprite; reads 0x02023360+0x3b then falls through to LAB_0802814a (shared convergence path with run_campaign_card_select_handler_6 for animation step processing).
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360
@ SPRITE_STATE_OFFSET = 0x39 (sprite state byte)
@ SPRITE_OAM_FLAG = 0x10 (bit4, fixed set)
@ SPRITE_ID = 0x24 (sprite slot passed to sync_state_and_init_sprite)
run_campaign_card_select_handler_5:
    ldr r7, DWORD_08028114                   @ 080280d0 104f
    .hword 0x4668    @ 080280d2 6846
    ldrh r0,[r0,#0x2]                        @ 080280d4 4088
    adds r3,r7,#0x0    @ 080280d6 3b1c
    adds r3,#0x39    @ 080280d8 3933
    movs r6,#0x1    @ 080280da 0126
    adds r1,r6,#0x0    @ 080280dc 311c
    ands r1,r0    @ 080280de 0140
    lsls r1,r1,#0x3    @ 080280e0 c900
    movs r0,#0x9    @ 080280e2 0920
    rsbs r0,r0,#0    @ 080280e4 4042
    ldrb r2,[r3,#0x0]                        @ 080280e6 1a78
    ands r0,r2    @ 080280e8 1040
    orrs r0,r1    @ 080280ea 0843
    .hword 0x4669    @ 080280ec 6946
    ldrb r1,[r1,#0x4]                        @ 080280ee 0979
    ands r1,r6    @ 080280f0 3140
    lsls r1,r1,#0x2    @ 080280f2 8900
    movs r2,#0x5    @ 080280f4 0522
    rsbs r2,r2,#0    @ 080280f6 5242
    ands r0,r2    @ 080280f8 1040
    orrs r0,r1    @ 080280fa 0843
    movs r1,#0x10    @ 080280fc 1021
    orrs r0,r1    @ 080280fe 0843
    strb r0,[r3,#0x0]                        @ 08028100 1870
    movs r0,#0x24    @ 08028102 2420
    bl sync_state_and_init_sprite            @ 08028104 d1f0d6fc
    movs r3,#0x3b    @ 08028108 3b23
    adds r3,r3,r7    @ 0802810a db19
    .hword 0x4698    @ 0802810c 9846
    ldrb r5,[r3,#0x0]                        @ 0802810e 1d78
    b LAB_0802814a                           @ 08028110 1be0
    .zero  0x2
DWORD_08028114:
    .word  0x02023360                     @ 08028114 60330202

@ At index 6 of PTR_FUN_08027ec0 jump table (0x08027ed8). Inline exit fragment, no push prologue. Symmetric with handler index 5 (0x080280d0): reads parent frame r0 (.hword 0x4668=mov r0,sp), takes bit0 from [r0+2] halfword and eors 1 (flips it, unlike op5 which uses ands directly), updates 0x02023360+0x39 bit3 with flipped value (no bit2 update step); ORs 0x10 (bit4 fixed set), writes back; calls sync_state_and_init_sprite(r0=0x24); converges at LAB_0802814a (shared with op5 for animation step counter processing at 0x02023360+0x3a and 0x3c).
@ 
@ Constants:
@ DISPLAY_CTX_BASE = 0x02023360
@ SPRITE_STATE_OFFSET = 0x39
@ SPRITE_OAM_FLAG = 0x10 (bit4 fixed set)
@ SPRITE_ID = 0x24 (sync_state_and_init_sprite param)
@ BIT_FLIP_MASK = 0x1 (eors 1 => flips [r0+2] bit0, differs from op5 ands)
run_campaign_card_select_handler_6:
    ldr r7, DWORD_0802818c                   @ 08028118 1c4f
    .hword 0x4668    @ 0802811a 6846
    ldrh r1,[r0,#0x2]                        @ 0802811c 4188
    movs r0,#0x1    @ 0802811e 0120
    eors r1,r0    @ 08028120 4140
    adds r2,r7,#0x0    @ 08028122 3a1c
    adds r2,#0x39    @ 08028124 3932
    movs r6,#0x1    @ 08028126 0126
    ands r1,r6    @ 08028128 3140
    lsls r1,r1,#0x3    @ 0802812a c900
    movs r0,#0x9    @ 0802812c 0920
    rsbs r0,r0,#0    @ 0802812e 4042
    ldrb r4,[r2,#0x0]                        @ 08028130 1478
    ands r0,r4    @ 08028132 2040
    orrs r0,r1    @ 08028134 0843
    movs r1,#0x10    @ 08028136 1021
    orrs r0,r1    @ 08028138 0843
    strb r0,[r2,#0x0]                        @ 0802813a 1070
    movs r0,#0x24    @ 0802813c 2420
    bl sync_state_and_init_sprite            @ 0802813e d1f0b9fc
    movs r5,#0x3b    @ 08028142 3b25
    adds r5,r5,r7    @ 08028144 ed19
    .hword 0x46a8    @ 08028146 a846
    ldrb r5,[r5,#0x0]                        @ 08028148 2d78
LAB_0802814a:
    lsrs r1,r5,#0x1    @ 0802814a 6908
    adds r4,r7,#0x0    @ 0802814c 3c1c
    adds r4,#0x3c    @ 0802814e 3c34
    movs r3,#0x1    @ 08028150 0123
    adds r0,r3,#0x0    @ 08028152 181c
    ldrb r2,[r4,#0x0]                        @ 08028154 2278
    ands r0,r2    @ 08028156 1040
    lsls r0,r0,#0x7    @ 08028158 c001
    orrs r0,r1    @ 0802815a 0843
    adds r0,#0x1    @ 0802815c 0130
    movs r2,#0x7f    @ 0802815e 7f22
    ands r2,r0    @ 08028160 0240
    lsls r2,r2,#0x1    @ 08028162 5200
    adds r1,r3,#0x0    @ 08028164 191c
    ands r1,r5    @ 08028166 2940
    orrs r1,r2    @ 08028168 1143
    .hword 0x4645    @ 0802816a 4546
    strb r1,[r5,#0x0]                        @ 0802816c 2970
    lsrs r0,r0,#0x7    @ 0802816e c009
    ands r0,r3    @ 08028170 1840
    ands r0,r6    @ 08028172 3040
    movs r1,#0x2    @ 08028174 0221
    rsbs r1,r1,#0    @ 08028176 4942
    ldrb r2,[r4,#0x0]                        @ 08028178 2278
    ands r1,r2    @ 0802817a 1140
    orrs r1,r0    @ 0802817c 0143
    strb r1,[r4,#0x0]                        @ 0802817e 2170
    ldr r0, DWORD_08028190                   @ 08028180 0348
    ldrh r3,[r7,#0x3a]                       @ 08028182 7b8f
    ands r0,r3    @ 08028184 1840
    strh r0,[r7,#0x3a]                       @ 08028186 7887
    b finalize_campaign_card_select_frame    @ 08028188 3be1
    .zero  0x2
DWORD_0802818c:
    .word  0x02023360                     @ 0802818c 60330202
DWORD_08028190:
    .word  0xfffffe03                     @ 08028190 03feffff

@ Campaign card-select scene dispatch table (PTR_FUN_08027ec0) case 7 handler. No independent push prologue (inline exit fragment). Calls check_siocnt_link_ready; if SIO ready: reads parent frame sp+2 halfword (SIO received data), writes to 0x0201e2a0+0x10 (card_cmd field) and +0x0 (card_id field); calls build_campaign_sprite_row_by_type(7). Regardless of SIO state: reads gPrng+OAM field to update OAM attr (clears/sets bit1 by 3-bit truncation), sets r3=0xf0<<3=0x780, branches LAB_080281c0 to execute strh + b finalize_campaign_card_select_frame. Called via PTR_FUN_08027ec0 entry index 7 at table addr 0x08027edc.
@ 
@ Params: r0=(none -- inline fragment, no APCS input)
@ Returns: void (b finalize_campaign_card_select_frame)
@ Side effects: [0x0201e2a0+0x10] := SIO sp+2 halfword (card_cmd); [0x0201e2a0+0x0] := SIO sp+4 halfword (card_id); via build_campaign_sprite_row_by_type(7): VRAM sprite row written
@ Constants: CARD_CMD_BASE=0x0201e2a0; CARD_CMD_OFF=0x10; CARD_ID_OFF=0x0; SPRITE_ROW_TYPE=7; OAM_ATTR_MASK=0xf0<<3=0x780
run_campaign_card_select_handler_7:
    bl check_siocnt_link_ready               @ 08028194 f7f700f9
    cmp r0,#0x0                              @ 08028198 0028
    bne LAB_080281b0                         @ 0802819a 09d1
    ldr r1, DWORD_080281c8                   @ 0802819c 0a49
    .hword 0x4668    @ 0802819e 6846
    ldrh r0,[r0,#0x2]                        @ 080281a0 4088
    str r0,[r1,#0x10]                        @ 080281a2 0861
    .hword 0x4668    @ 080281a4 6846
    ldrh r0,[r0,#0x4]                        @ 080281a6 8088
    str r0,[r1,#0x0]                         @ 080281a8 0860
    movs r0,#0x7    @ 080281aa 0720
    bl build_campaign_sprite_row_by_type     @ 080281ac fff774fd
LAB_080281b0:
    ldr r0, DWORD_080281cc                   @ 080281b0 0648
    ldr r4, DWORD_080281d0                   @ 080281b2 074c
    adds r0,r0,r4    @ 080281b4 0019
    ldr r1, DWORD_080281d4                   @ 080281b6 0749
    ldrh r5,[r0,#0x0]                        @ 080281b8 0588
    ands r1,r5    @ 080281ba 2940
    movs r3,#0xf0    @ 080281bc f023
    lsls r3,r3,#0x3    @ 080281be db00
LAB_080281c0:
    adds r2,r3,#0x0    @ 080281c0 1a1c
    orrs r1,r2    @ 080281c2 1143
    strh r1,[r0,#0x0]                        @ 080281c4 0180
    b finalize_campaign_card_select_frame    @ 080281c6 1ce1
DWORD_080281c8:
    .word  0x0201e2a0                     @ 080281c8 a0e20102
DWORD_080281cc:
    .word  gPrng                          @ 080281cc 40000003
DWORD_080281d0:
    .word  0x00000202                     @ 080281d0 02020000
DWORD_080281d4:
    .word  0xffffc03f                     @ 080281d4 3fc0ffff

@ At index 9 of PTR_FUN_08027ec0 jump table (0x08027ee4). Inline exit fragment, no push prologue. Reads parent frame r0 (.hword 0x4668=mov r0,sp), loads [r0+2] halfword as current step value: if > 0x3b (59) branches to FUN_08028402 (out of range, exit); if < 0 branches to FUN_08028402 (below minimum, exit); if in [0..59] falls to LAB_080281e8 (reads sp+0x11c frame slot, writes 4 into [sp+0x11c], continues processing). Validates parent frame step value in valid range [0..0x3b]; exits early if out of range.
@ 
@ Constants:
@ STEP_MAX = 0x3b = 59 (valid step upper bound)
@ STEP_MIN = 0 (lower bound)
@ SP_STEP_OFFSET = 0x2 ([sp+2] = parent frame step value)
@ SP_SLOT_OFFSET = 0x11c (sp+0x11c = subsequent processing slot)
run_campaign_card_select_handler_9:
    .hword 0x4668    @ 080281d8 6846
    ldrh r0,[r0,#0x2]                        @ 080281da 4088
    cmp r0,#0x3b                             @ 080281dc 3b28
    ble LAB_080281e2                         @ 080281de 00dd
    b finalize_campaign_card_select_frame    @ 080281e0 0fe1
LAB_080281e2:
    cmp r0,#0x0                              @ 080281e2 0028
    bge LAB_080281e8                         @ 080281e4 00da
    b finalize_campaign_card_select_frame    @ 080281e6 0ce1
LAB_080281e8:
    add r6,sp,#0x11c                         @ 080281e8 47ae
    movs r0,#0x4    @ 080281ea 0420
    strh r0,[r6,#0x0]                        @ 080281ec 3080
    .hword 0x4668    @ 080281ee 6846
    ldrh r0,[r0,#0x2]                        @ 080281f0 4088
    strh r0,[r6,#0x2]                        @ 080281f2 7080
    ldr r7, DWORD_08028258                   @ 080281f4 184f
    .hword 0x4668    @ 080281f6 6846
    ldrh r2,[r0,#0x2]                        @ 080281f8 4288
    lsrs r1,r2,#0x5    @ 080281fa 5109
    lsls r1,r1,#0x2    @ 080281fc 8900
    ldr r5, DWORD_0802825c                   @ 080281fe 174d
    adds r4,r7,r5    @ 08028200 7c19
    adds r1,r1,r4    @ 08028202 0919
    movs r5,#0x1f    @ 08028204 1f25
    ands r2,r5    @ 08028206 2a40
    movs r3,#0x1    @ 08028208 0123
    adds r0,r3,#0x0    @ 0802820a 181c
    lsls r0,r2    @ 0802820c 9040
    ldrh r1,[r1,#0x0]                        @ 0802820e 0988
    ands r0,r1    @ 08028210 0840
    strh r0,[r6,#0x4]                        @ 08028212 b080
    .hword 0x4668    @ 08028214 6846
    ldrh r2,[r0,#0x2]                        @ 08028216 4288
    lsrs r1,r2,#0x5    @ 08028218 5109
    lsls r1,r1,#0x2    @ 0802821a 8900
    adds r1,r1,r4    @ 0802821c 0919
    adds r0,r2,#0x0    @ 0802821e 101c
    ands r0,r5    @ 08028220 2840
    lsls r3,r0    @ 08028222 8340
    ldr r0,[r1,#0x0]                         @ 08028224 0868
    ands r0,r3    @ 08028226 1840
    cmp r0,#0x0                              @ 08028228 0028
    beq LAB_08028264                         @ 0802822a 1bd0
    movs r0,#0x91    @ 0802822c 9120
    lsls r0,r0,#0x1    @ 0802822e 4000
    add r0,sp                                @ 08028230 6844
    lsls r1,r2,#0x3    @ 08028232 d100
    adds r1,r1,r2    @ 08028234 8918
    lsls r1,r1,#0x2    @ 08028236 8900
    subs r1,r1,r2    @ 08028238 891a
    lsls r1,r1,#0x3    @ 0802823a c900
    ldr r3, DWORD_08028260                   @ 0802823c 084b
    adds r2,r7,r3    @ 0802823e fa18
    adds r1,r1,r2    @ 08028240 8918
    movs r2,#0x8c    @ 08028242 8c22
    lsls r2,r2,#0x1    @ 08028244 5200
    bl copy_bytes_by_halfword                @ 08028246 ccf02dfe
    movs r1,#0x8f    @ 0802824a 8f21
    lsls r1,r1,#0x1    @ 0802824c 4900
    adds r0,r6,#0x0    @ 0802824e 301c
    bl write_sprite_row_to_vram_buffer       @ 08028250 c5f002fb
    b finalize_campaign_card_select_frame    @ 08028254 d5e0
    .zero  0x2
DWORD_08028258:
    .word  0x02000000                     @ 08028258 00000002
DWORD_0802825c:
    .word  0x000053f0                     @ 0802825c f0530000
DWORD_08028260:
    .word  0x00001250                     @ 08028260 50120000
LAB_08028264:
    adds r0,r6,#0x0    @ 08028264 301c
    movs r1,#0x6    @ 08028266 0621
    bl write_sprite_row_to_vram_buffer       @ 08028268 c5f0f6fa
    b finalize_campaign_card_select_frame    @ 0802826c c9e0

@ Function: PTR_FUN_08027ec0 jump table index 10 handler for campaign card select. Reads parent frame sp+0x11c for sprite_row descriptor address, writes attr0=4 (8x8 obj), attr1 (y=0x1ff), attr2=1 (tile_idx=1), then calls copy_bytes_by_halfword to copy 0x8c*2=0x118 bytes of prototype row data from 0x02001138 into sp+0x11c, then calls write_sprite_row_to_vram_buffer with tile_base_y=0x11e (0x8f<<1) to commit OBJ VRAM row write. No own push prologue; this is a parent-frame inline exit fragment that jumps to parent frame shared epilogue via b FUN_08028402.
@ 
@ Side effects: OBJ VRAM written via write_sprite_row_to_vram_buffer.
@ 
@ Constants:
@ - SPRITE_ROW_ATTR0 = 0x4 // 8x8 mode
@ - SPRITE_ROW_ATTR1 = 0xffff // y=ATTR1_HIDDEN sentinel
@ - SPRITE_ROW_ATTR2 = 0x1 // tile index 1
@ - PROTO_DATA_SRC = 0x02001138 // EWRAM sprite row template source
@ - COPY_LEN_HW = 0x8c*2 = 0x118 bytes (0x8c halfwords)
@ - TILE_BASE_Y = 0x11e (0x8f<<1)
run_campaign_card_select_handler_10:
    add r4,sp,#0x11c                         @ 0802826e 47ac
    movs r0,#0x4    @ 08028270 0420
    strh r0,[r4,#0x0]                        @ 08028272 2080
    ldr r0, DWORD_08028298                   @ 08028274 0848
    strh r0,[r4,#0x2]                        @ 08028276 6080
    movs r0,#0x1    @ 08028278 0120
    strh r0,[r4,#0x4]                        @ 0802827a a080
    movs r0,#0x91    @ 0802827c 9120
    lsls r0,r0,#0x1    @ 0802827e 4000
    add r0,sp                                @ 08028280 6844
    ldr r1, DWORD_0802829c                   @ 08028282 0649
    movs r2,#0x8c    @ 08028284 8c22
    lsls r2,r2,#0x1    @ 08028286 5200
    bl copy_bytes_by_halfword                @ 08028288 ccf00cfe
    movs r1,#0x8f    @ 0802828c 8f21
    lsls r1,r1,#0x1    @ 0802828e 4900
    adds r0,r4,#0x0    @ 08028290 201c
    bl write_sprite_row_to_vram_buffer       @ 08028292 c5f0e1fa
    b finalize_campaign_card_select_frame    @ 08028296 b4e0
DWORD_08028298:
    .word  0x0000ffff                     @ 08028298 ffff0000
DWORD_0802829c:
    .word  0x02001138                     @ 0802829c 38110002

@ Function: PTR_FUN_08027ec0 jump table index 11 handler for campaign card select. No own push prologue (inline exit fragment). .hword 0x4668 = mov r0,sp to get parent frame stack pointer; ldrh r0,[r0,#2] reads sp+2 halfword as hand_oam_slot_id; movs r1,#1; bl apply_delta_to_hand_oam_entry applies delta=+1 to hand OAM entry (scroll forward). Then b LAB_080282b6 to init_puzzle_wram_then_copy + build_campaign_sprite_row_by_type(0x8) shared tail before entering parent frame epilogue.
@ 
@ Side effects: OAM hand entry y-offset modified via apply_delta_to_hand_oam_entry.
@ 
@ Constants:
@ - HAND_OAM_DELTA = 1 // apply_delta_to_hand_oam_entry r1 parameter
run_campaign_card_select_handler_11:
    .hword 0x4668    @ 080282a0 6846
    ldrh r0,[r0,#0x2]                        @ 080282a2 4088
    movs r1,#0x1    @ 080282a4 0121
    bl apply_delta_to_hand_oam_entry         @ 080282a6 d0f0d5fe
    b LAB_080282b6                           @ 080282aa 04e0

@ Campaign card-select scene dispatch table (PTR_FUN_08027ec0) case 12 handler. No independent push prologue (inline exit fragment). .hword 0x4668=mov r0,sp reads parent frame stack; ldrh r0,[r0+2] reads SIO received halfword; movs r1,#1; bl apply_delta_to_hand_oam_entry__080f90a8 applies delta=+1 to hand OAM entry (scroll up). Then jumps to LAB_080282b6 shared tail: init_puzzle_wram_then_copy + build_campaign_sprite_row_by_type(8) + b finalize_campaign_card_select_frame. Only difference from run_campaign_card_select_handler_11 (0x080282a0): calls apply_delta_to_hand_oam_entry__080f90a8 instead of apply_delta_to_hand_oam_entry. Called via PTR_FUN_08027ec0 entry index 12 at table addr 0x08027ef0.
@ 
@ Params: r0=(none -- inline fragment, no APCS input)
@ Returns: void (b finalize_campaign_card_select_frame)
@ Side effects: via apply_delta_to_hand_oam_entry__080f90a8: hand OAM entry y offset +1; via init_puzzle_wram_then_copy: puzzle WRAM initialized; via build_campaign_sprite_row_by_type(8): VRAM sprite row written
@ Constants: HAND_OAM_DELTA=1; SPRITE_ROW_TYPE=8
run_campaign_card_select_handler_12:
    .hword 0x4668    @ 080282ac 6846
    ldrh r0,[r0,#0x2]                        @ 080282ae 4088
    movs r1,#0x1    @ 080282b0 0121
    bl apply_delta_to_hand_oam_entry__080f90a8 @ 080282b2 d0f0f9fe
LAB_080282b6:
    bl init_puzzle_wram_then_copy            @ 080282b6 d1f0e7fc
    movs r0,#0x8    @ 080282ba 0820
    bl build_campaign_sprite_row_by_type     @ 080282bc fff7ecfc
    b finalize_campaign_card_select_frame    @ 080282c0 9fe0

@ Function: PTR_FUN_08027ec0 jump table index 13 handler for campaign card select. Calls build_campaign_sprite_row_by_type(0x8) to refresh player profile sprite row; then iterates hand OAM entry array (reads hand_count halfword from 0x095b7cca, calls apply_delta_to_hand_oam_entry(idx, delta=1) for each index in [0..hand_count), scrolling all hand OAM entry y-offsets); skips loop if hand_count==0. Finally b FUN_08028402 to parent frame shared epilogue.
@ 
@ Side effects: all hand OAM entry y-offsets +1; build_campaign_sprite_row_by_type writes VRAM.
@ 
@ Constants:
@ - SPRITE_TYPE = 0x8 // build_campaign_sprite_row_by_type parameter
@ - HAND_ARRAY_BASE = 0x095b7cca // ROM hand array head (count halfword at +0)
@ - HAND_OAM_DELTA = 1
run_campaign_card_select_handler_13:
    movs r0,#0x8    @ 080282c2 0820
    bl build_campaign_sprite_row_by_type     @ 080282c4 fff7e8fc
    movs r4,#0x0    @ 080282c8 0024
    ldr r0, DWORD_080282ec                   @ 080282ca 0848
    ldrh r5,[r0,#0x0]                        @ 080282cc 0588
    cmp r4,r5                                @ 080282ce ac42
    blt LAB_080282d4                         @ 080282d0 00db
    b finalize_campaign_card_select_frame    @ 080282d2 96e0
LAB_080282d4:
    adds r5,r0,#0x0    @ 080282d4 051c
LAB_080282d6:
    lsls r0,r4,#0x10    @ 080282d6 2004
    lsrs r0,r0,#0x10    @ 080282d8 000c
    movs r1,#0x1    @ 080282da 0121
    bl apply_delta_to_hand_oam_entry         @ 080282dc d0f0bafe
    adds r4,#0x1    @ 080282e0 0134
    ldrh r0,[r5,#0x0]                        @ 080282e2 2888
    cmp r4,r0                                @ 080282e4 8442
    blt LAB_080282d6                         @ 080282e6 f6db
    b finalize_campaign_card_select_frame    @ 080282e8 8be0
    .zero  0x2
DWORD_080282ec:
    .word  0x095b7cca                     @ 080282ec ca7c5b09

@ Function: PTR_FUN_08027ec0 jump table index 14 handler for campaign card select. Calls build_campaign_sprite_row_by_type(0x8) to refresh sprite row; then iterates 0x7d (125) challenge records (r5 in [0..0x7c]) in three segments: expert [0..0x22], standard [0x23..0x4b], duel_puzzle [0x4c..0x7c]. For each challenge record reads completion status halfword[+8]; if 0x7 (completed), modifies ROM flag byte [r4+0] bits[1:0] via bit operations (also computes y-sprite scale offset written back to [r4+0]); if 0x4 (special state, only duel_puzzle segment), clears that field. Each iteration advances r10/r9/r8/r4 by 0xc bytes. After loop calls init_puzzle_wram_then_copy, then b FUN_08028402.
@ 
@ Side effects: ROM flag table [r4+0] challenge completion status bits modified; init_puzzle_wram_then_copy side effects.
@ 
@ Constants:
@ - SPRITE_TYPE = 0x8
@ - CHALLENGE_COUNT = 0x7d // 125 entries total
@ - EXPERT_RANGE = [0..0x22] (35 entries)
@ - STANDARD_RANGE = [0x23..0x4b] (41 entries)
@ - PUZZLE_RANGE = [0x4c..0x7c] (49 entries)
@ - COMPLETED_STATUS = 0x7 // halfword[+8] value meaning completed
@ - SPECIAL_STATUS = 0x4 // puzzle special clear state
@ - ENTRY_STRIDE = 0xc // r10/r9/r8/r4 step per iteration
@ - EXPERT_BASE = 0x09e5e80c // challenge record array base (expert)
@ - STANDARD_BASE = 0x09e5e620
@ - PUZZLE_BASE = 0x09e5e9cc
run_campaign_card_select_handler_14:
    movs r0,#0x8    @ 080282f0 0820
    bl build_campaign_sprite_row_by_type     @ 080282f2 fff7d1fc
    movs r5,#0x0    @ 080282f6 0025
    ldr r0, DWORD_080283ac                   @ 080282f8 2c48
    movs r6,#0x3    @ 080282fa 0326
    ldr r1, DWORD_080283b0                   @ 080282fc 2c49
    .hword 0x468a    @ 080282fe 8a46
    ldr r2, DWORD_080283b4                   @ 08028300 2c4a
    .hword 0x4691    @ 08028302 9146
    ldr r3, DWORD_080283b8                   @ 08028304 2c4b
    adds r4,r0,r3    @ 08028306 c418
    ldr r7, DWORD_080283bc                   @ 08028308 2c4f
    .hword 0x46a8    @ 0802830a a846
LAB_0802830c:
    ldrb r1,[r4,#0x0]                        @ 0802830c 2178
    lsls r0,r1,#0x1e    @ 0802830e 8807
    lsrs r0,r0,#0x1e    @ 08028310 800f
    cmp r0,#0x3                              @ 08028312 0328
    bgt LAB_0802831a                         @ 08028314 01dc
    cmp r0,#0x1                              @ 08028316 0128
    bge LAB_08028320                         @ 08028318 02da
LAB_0802831a:
    movs r0,#0x3    @ 0802831a 0320
    orrs r0,r1    @ 0802831c 0843
    strb r0,[r4,#0x0]                        @ 0802831e 2070
LAB_08028320:
    cmp r5,#0x0                              @ 08028320 002d
    blt LAB_0802834c                         @ 08028322 13db
    bl get_expert_challenge_count            @ 08028324 b9f030fa
    cmp r5,r0                                @ 08028328 8542
    bge LAB_0802834c                         @ 0802832a 0fda
    ldr r0, DWORD_080283c0                   @ 0802832c 2448
    add r0,r8                                @ 0802832e 4044
    ldrh r0,[r0,#0x8]                        @ 08028330 0089
    cmp r0,#0x7                              @ 08028332 0728
    bne LAB_0802834c                         @ 08028334 0ad1
    ldr r2,[r4,#0x0]                         @ 08028336 2268
    ands r2,r6    @ 08028338 3240
    orrs r2,r7    @ 0802833a 3a43
    lsrs r0,r2,#0x2    @ 0802833c 9008
    lsls r1,r0,#0x4    @ 0802833e 0101
    subs r1,r1,r0    @ 08028340 091a
    lsls r1,r1,#0x4    @ 08028342 0901
    adds r0,r6,#0x0    @ 08028344 301c
    ands r0,r2    @ 08028346 1040
    orrs r0,r1    @ 08028348 0843
    str r0,[r4,#0x0]                         @ 0802834a 2060
LAB_0802834c:
    cmp r5,#0x22                             @ 0802834c 222d
    ble LAB_0802837a                         @ 0802834e 14dd
    bl get_standard_challenge_count          @ 08028350 b8f04cfe
    adds r0,#0x23    @ 08028354 2330
    cmp r5,r0                                @ 08028356 8542
    bge LAB_0802837a                         @ 08028358 0fda
    ldr r0, DWORD_080283c4                   @ 0802835a 1a48
    add r0,r9                                @ 0802835c 4844
    ldrh r0,[r0,#0x8]                        @ 0802835e 0089
    cmp r0,#0x7                              @ 08028360 0728
    bne LAB_0802837a                         @ 08028362 0ad1
    ldr r2,[r4,#0x0]                         @ 08028364 2268
    ands r2,r6    @ 08028366 3240
    orrs r2,r7    @ 08028368 3a43
    lsrs r0,r2,#0x2    @ 0802836a 9008
    lsls r1,r0,#0x4    @ 0802836c 0101
    subs r1,r1,r0    @ 0802836e 091a
    lsls r1,r1,#0x4    @ 08028370 0901
    adds r0,r6,#0x0    @ 08028372 301c
    ands r0,r2    @ 08028374 1040
    orrs r0,r1    @ 08028376 0843
    str r0,[r4,#0x0]                         @ 08028378 2060
LAB_0802837a:
    cmp r5,#0x4b                             @ 0802837a 4b2d
    ble LAB_080283d2                         @ 0802837c 29dd
    bl get_duel_puzzle_count                 @ 0802837e baf06bff
    adds r0,#0x4c    @ 08028382 4c30
    cmp r5,r0                                @ 08028384 8542
    bge LAB_080283d2                         @ 08028386 24da
    ldr r0, DWORD_080283c8                   @ 08028388 0f48
    add r0,r10                               @ 0802838a 5044
    ldrh r0,[r0,#0x8]                        @ 0802838c 0089
    cmp r0,#0x4                              @ 0802838e 0428
    beq LAB_080283cc                         @ 08028390 1cd0
    cmp r0,#0x7                              @ 08028392 0728
    bne LAB_080283d2                         @ 08028394 1dd1
    ldr r2,[r4,#0x0]                         @ 08028396 2268
    ands r2,r6    @ 08028398 3240
    orrs r2,r7    @ 0802839a 3a43
    lsrs r0,r2,#0x2    @ 0802839c 9008
    lsls r1,r0,#0x4    @ 0802839e 0101
    subs r1,r1,r0    @ 080283a0 091a
    lsls r1,r1,#0x4    @ 080283a2 0901
    adds r0,r6,#0x0    @ 080283a4 301c
    ands r0,r2    @ 080283a6 1040
    orrs r0,r1    @ 080283a8 0843
    b LAB_080283d0                           @ 080283aa 11e0
DWORD_080283ac:
    .word  0x02000000                     @ 080283ac 00000002
DWORD_080283b0:
    .word  0xfffffc70                     @ 080283b0 70fcffff
DWORD_080283b4:
    .word  0xfffffe5c                     @ 080283b4 5cfeffff
DWORD_080283b8:
    .word  0x00006c3c                     @ 080283b8 3c6c0000
DWORD_080283bc:
    .word  0x0000e0fc                     @ 080283bc fce00000
DWORD_080283c0:
    .word  0x09e5e80c                     @ 080283c0 0ce8e509
DWORD_080283c4:
    .word  0x09e5e620                     @ 080283c4 20e6e509
DWORD_080283c8:
    .word  0x09e5e9cc                     @ 080283c8 cce9e509
LAB_080283cc:
    ldr r0,[r4,#0x0]                         @ 080283cc 2068
    ands r0,r6    @ 080283ce 3040
LAB_080283d0:
    str r0,[r4,#0x0]                         @ 080283d0 2060
LAB_080283d2:
    movs r0,#0xc    @ 080283d2 0c20
    add r10,r0                               @ 080283d4 8244
    add r9,r0                                @ 080283d6 8144
    adds r4,#0x4    @ 080283d8 0434
    add r8,r0                                @ 080283da 8044
    adds r5,#0x1    @ 080283dc 0135
    cmp r5,#0x7d                             @ 080283de 7d2d
    ble LAB_0802830c                         @ 080283e0 94dd
    bl init_puzzle_wram_then_copy            @ 080283e2 d1f051fc
    b finalize_campaign_card_select_frame    @ 080283e6 0ce0

@ Function: PTR_FUN_08027ec0 jump table index 15 handler for campaign card select. No own push prologue (inline exit fragment). .hword 0x4668 = mov r0,sp gets parent frame sp; ldrh r0,[r0,#2] reads sp+2 halfword as money_delta low 16 bits; .hword 0x4669=mov r1,sp; ldrh r1,[r1,#4] reads sp+4 halfword as money_delta high 16 bits; orrs r0,r1<<16 combines to 32-bit money value; bl accrue_money_with_cap accumulates money (with cap). Then bl init_puzzle_wram_then_copy, movs r0,#8, bl build_campaign_sprite_row_by_type(8) refreshes sprite row, then enters parent frame epilogue.
@ 
@ Side effects: player money state updated via accrue_money_with_cap; init_puzzle_wram_then_copy side effects; VRAM OBJ via build_campaign_sprite_row_by_type.
@ 
@ Constants:
@ - SPRITE_TYPE = 0x8
run_campaign_card_select_handler_15:
    .hword 0x4668    @ 080283e8 6846
    ldrh r0,[r0,#0x2]                        @ 080283ea 4088
    .hword 0x4669    @ 080283ec 6946
    ldrh r1,[r1,#0x4]                        @ 080283ee 8988
    lsls r1,r1,#0x10    @ 080283f0 0904
    orrs r0,r1    @ 080283f2 0843
    bl accrue_money_with_cap                 @ 080283f4 d0f092fd
    bl init_puzzle_wram_then_copy            @ 080283f8 d1f046fc
    movs r0,#0x8    @ 080283fc 0820
    bl build_campaign_sprite_row_by_type     @ 080283fe fff74bfc

@ Function: shared epilogue fragment for campaign card select parent frame. PTR_FUN_08027ec0[8] points directly here; all handler_10..15 also jump here via "b FUN_08028402". Entry sets r0=1 (frame processing done / tick done), then restores r8/r9/r10/r4/r5/r6/r7 callee-save values via pop/mov sequence, then pop {r1}; bx r1 returns (Sub-case E: return value in r0 unaffected by pop). Essentially the unified exit path for the parent frame (large switch-driven frame function).
@ 
@ Side effects: none; restores calling-convention registers.
@ 
@ Constants:
@ - DONE_FLAG = 1 // r0 exit value, frame tick complete
finalize_campaign_card_select_frame:
    movs r0,#0x1    @ 08028402 0120
LAB_08028404:
    movs r3,#0x8f    @ 08028404 8f23
    lsls r3,r3,#0x2    @ 08028406 9b00
    add sp,r3                                @ 08028408 9d44
    pop {r3,r4,r5}                           @ 0802840a 38bc
    .hword 0x4698    @ 0802840c 9846
    .hword 0x46a1    @ 0802840e a146
    .hword 0x46aa    @ 08028410 aa46
    pop {r4,r5,r6,r7}                        @ 08028412 f0bc
    pop {r1}                                 @ 08028414 02bc
    bx r1                                    @ 08028416 0847

@ Function: campaign card select screen text line renderer (centered variant). Accepts col/row coordinates (r0/r1), packed col_width/row_count (r2), style flags (r3), text pointer (sp[0x20]). First calls count_bytes_until_null to get string byte count, subtracts 3*strlen/2 from col_width to get horizontal center offset, calls setup_line_buf_pos_and_font(col_centered, row) to set font line buffer position and font; reads 0x02006c2c game flags bit0-2 to set style bits at line buffer byte [0x02006ed0+8] (bit0=bold/italic, bit1=underline); calls text_render_wrapper twice to render two text lines; calls zero_fill_by_halfword to clear target tile in BG VRAM 0x06004000 region, then commit_line_buffer_to_sprite_vram to commit; finally writes tile index into VRAM row (strh loop). Exit pop {r1}; bx r1 (Sub-case E).
@ 
@ Side effects:
@ - [0x02006ed0+8] := style bits (bold/italic/underline flags)
@ - VRAM 0x06004000 + tile_offset: zero_fill_by_halfword clear
@ - VRAM 0x06004000 area: commit_line_buffer_to_sprite_vram writes text pixels
@ - VRAM BG tile row: strh loop writes tile index
@ 
@ Constants:
@ - GAME_STATE_FLAG_BASE = 0x02000000
@ - GAME_STATE_OFFSET = 0x6c2c // 0x02000000+0x6c2c=0x02006c2c
@ - LINE_BUF_STYLE_PTR = 0x02006ed0 // style flags at [+8]
@ - FONT_BASE_TABLE = font_jp_base_table (0x09e5f854)
@ - BG_VRAM_BASE = 0x06004000
@ - BOLD_BIT = 0x2 // style bit1
@ - CENTER_DIVISOR = 3 // strlen * 3 / 2 = center pixel estimate
render_campaign_text_line_centered:
    push {r4,r5,r6,r7,lr}                    @ 08028418 f0b5
    .hword 0x4657    @ 0802841a 5746
    .hword 0x464e    @ 0802841c 4e46
    .hword 0x4645    @ 0802841e 4546
    push {r5,r6,r7}                          @ 08028420 e0b4
    adds r4,r3,#0x0    @ 08028422 1c1c
    lsls r0,r0,#0x10    @ 08028424 0004
    lsrs r0,r0,#0x10    @ 08028426 000c
    .hword 0x4680    @ 08028428 8046
    lsls r1,r1,#0x10    @ 0802842a 0904
    lsrs r5,r1,#0x10    @ 0802842c 0d0c
    lsls r2,r2,#0x10    @ 0802842e 1204
    lsls r4,r4,#0x10    @ 08028430 2404
    lsrs r0,r4,#0x10    @ 08028432 200c
    .hword 0x4682    @ 08028434 8246
    lsls r0,r2,#0x8    @ 08028436 1002
    lsrs r6,r0,#0x18    @ 08028438 060e
    lsrs r7,r2,#0x18    @ 0802843a 170e
    ldr r0,[sp,#0x20]                        @ 0802843c 0898
    bl count_bytes_until_null                @ 0802843e cdf04ff8
    lsls r2,r6,#0x2    @ 08028442 b200
    lsls r1,r0,#0x1    @ 08028444 4100
    adds r1,r1,r0    @ 08028446 0918
    subs r2,r2,r1    @ 08028448 521a
    .hword 0x4691    @ 0802844a 9146
    adds r0,r6,#0x0    @ 0802844c 301c
    adds r1,r7,#0x0    @ 0802844e 391c
    bl setup_line_buf_pos_and_font           @ 08028450 c8f0b0fb
    ldr r2, DWORD_08028554                   @ 08028454 3f4a
    ldr r0, DWORD_08028558                   @ 08028456 4048
    ldr r1, DWORD_0802855c                   @ 08028458 4049
    adds r0,r0,r1    @ 0802845a 4018
    movs r1,#0x7    @ 0802845c 0721
    ldrb r0,[r0,#0x0]                        @ 0802845e 0078
    ands r1,r0    @ 08028460 0140
    rsbs r1,r1,#0    @ 08028462 4942
    lsrs r1,r1,#0x1f    @ 08028464 c90f
    movs r0,#0x2    @ 08028466 0220
    rsbs r0,r0,#0    @ 08028468 4042
    ldrb r3,[r2,#0x8]                        @ 0802846a 137a
    ands r0,r3    @ 0802846c 1840
    orrs r0,r1    @ 0802846e 0843
    movs r1,#0x2    @ 08028470 0221
    orrs r0,r1    @ 08028472 0843
    strb r0,[r2,#0x8]                        @ 08028474 1072
    ldr r3, DWORD_08028560                   @ 08028476 3a4b
    lsls r1,r0,#0x1e    @ 08028478 8107
    lsrs r1,r1,#0x1f    @ 0802847a c90f
    lsls r1,r1,#0x2    @ 0802847c 8900
    lsls r0,r0,#0x1f    @ 0802847e c007
    lsrs r0,r0,#0x1f    @ 08028480 c00f
    lsls r0,r0,#0x3    @ 08028482 c000
    adds r1,r1,r0    @ 08028484 0918
    adds r1,r1,r3    @ 08028486 c918
    ldr r0,[r1,#0x0]                         @ 08028488 0868
    str r0,[r2,#0x4]                         @ 0802848a 5060
    lsrs r2,r4,#0x18    @ 0802848c 220e
    cmp r2,#0x0                              @ 0802848e 002a
    beq LAB_080284a4                         @ 08028490 08d0
    movs r1,#0x80    @ 08028492 8021
    lsls r1,r1,#0x8    @ 08028494 0902
    adds r0,r1,#0x0    @ 08028496 081c
    orrs r2,r0    @ 08028498 0243
    .hword 0x4648    @ 0802849a 4846
    movs r1,#0x2    @ 0802849c 0221
    ldr r3,[sp,#0x20]                        @ 0802849e 089b
    bl text_render_wrapper                   @ 080284a0 caf0ecfa
LAB_080284a4:
    .hword 0x4653    @ 080284a4 5346
    lsls r2,r3,#0x18    @ 080284a6 1a06
    lsrs r2,r2,#0x18    @ 080284a8 120e
    .hword 0x4648    @ 080284aa 4846
    movs r1,#0x2    @ 080284ac 0221
    ldr r3,[sp,#0x20]                        @ 080284ae 089b
    bl text_render_wrapper                   @ 080284b0 caf0e4fa
    lsls r4,r5,#0x5    @ 080284b4 6c01
    ldr r0, DWORD_08028564                   @ 080284b6 2b48
    adds r4,r4,r0    @ 080284b8 2418
    lsls r0,r7,#0x5    @ 080284ba 7801
    adds r1,r6,#0x0    @ 080284bc 311c
    muls r1,r0    @ 080284be 4143
    adds r0,r4,#0x0    @ 080284c0 201c
    bl zero_fill_by_halfword                 @ 080284c2 ccf0d7fc
    adds r0,r4,#0x0    @ 080284c6 201c
    movs r1,#0x0    @ 080284c8 0021
    bl commit_line_buffer_to_sprite_vram     @ 080284ca caf0bffc
    movs r3,#0x0    @ 080284ce 0023
    cmp r3,r7                                @ 080284d0 bb42
    bge LAB_080284fe                         @ 080284d2 14da
    movs r4,#0xc0    @ 080284d4 c024
    lsls r4,r4,#0x13    @ 080284d6 e404
LAB_080284d8:
    lsls r0,r3,#0x10    @ 080284d8 1804
    lsrs r0,r0,#0xb    @ 080284da c00a
    add r0,r8                                @ 080284dc 4044
    lsls r0,r0,#0x1    @ 080284de 4000
    adds r2,r0,r4    @ 080284e0 0219
    adds r3,#0x1    @ 080284e2 0133
    cmp r6,#0x0                              @ 080284e4 002e
    beq LAB_080284fa                         @ 080284e6 08d0
    adds r1,r6,#0x0    @ 080284e8 311c
LAB_080284ea:
    strh r5,[r2,#0x0]                        @ 080284ea 1580
    adds r2,#0x2    @ 080284ec 0232
    adds r0,r5,#0x1    @ 080284ee 681c
    lsls r0,r0,#0x10    @ 080284f0 0004
    lsrs r5,r0,#0x10    @ 080284f2 050c
    subs r1,#0x1    @ 080284f4 0139
    cmp r1,#0x0                              @ 080284f6 0029
    bne LAB_080284ea                         @ 080284f8 f7d1
LAB_080284fa:
    cmp r3,r7                                @ 080284fa bb42
    blt LAB_080284d8                         @ 080284fc ecdb
LAB_080284fe:
    adds r3,r7,#0x0    @ 080284fe 3b1c
    cmp r3,#0x5                              @ 08028500 052b
    bgt LAB_08028544                         @ 08028502 1fdc
    .hword 0x4641    @ 08028504 4146
    lsrs r5,r1,#0x5    @ 08028506 4d09
    movs r4,#0x1f    @ 08028508 1f24
    ands r4,r1    @ 0802850a 0c40
LAB_0802850c:
    adds r1,r5,r3    @ 0802850c e918
    adds r0,r1,#0x0    @ 0802850e 081c
    cmp r1,#0x0                              @ 08028510 0029
    bge LAB_08028516                         @ 08028512 00da
    adds r0,#0x1f    @ 08028514 1f30
LAB_08028516:
    asrs r0,r0,#0x5    @ 08028516 4011
    lsls r0,r0,#0x5    @ 08028518 4001
    subs r0,r1,r0    @ 0802851a 081a
    adds r0,#0x20    @ 0802851c 2030
    lsls r0,r0,#0x10    @ 0802851e 0004
    lsrs r0,r0,#0xb    @ 08028520 c00a
    adds r0,r4,r0    @ 08028522 2018
    lsls r0,r0,#0x1    @ 08028524 4000
    movs r1,#0xc0    @ 08028526 c021
    lsls r1,r1,#0x13    @ 08028528 c904
    adds r0,r0,r1    @ 0802852a 4018
    adds r3,#0x1    @ 0802852c 0133
    cmp r6,#0x0                              @ 0802852e 002e
    beq LAB_08028540                         @ 08028530 06d0
    movs r2,#0x0    @ 08028532 0022
    adds r1,r6,#0x0    @ 08028534 311c
LAB_08028536:
    strh r2,[r0,#0x0]                        @ 08028536 0280
    adds r0,#0x2    @ 08028538 0230
    subs r1,#0x1    @ 0802853a 0139
    cmp r1,#0x0                              @ 0802853c 0029
    bne LAB_08028536                         @ 0802853e fad1
LAB_08028540:
    cmp r3,#0x5                              @ 08028540 052b
    ble LAB_0802850c                         @ 08028542 e3dd
LAB_08028544:
    pop {r3,r4,r5}                           @ 08028544 38bc
    .hword 0x4698    @ 08028546 9846
    .hword 0x46a1    @ 08028548 a146
    .hword 0x46aa    @ 0802854a aa46
    pop {r4,r5,r6,r7}                        @ 0802854c f0bc
    pop {r0}                                 @ 0802854e 01bc
    bx r0                                    @ 08028550 0047
    .zero  0x2
DWORD_08028554:
    .word  0x02006ed0                     @ 08028554 d06e0002
DWORD_08028558:
    .word  0x02000000                     @ 08028558 00000002
DWORD_0802855c:
    .word  0x00006c2c                     @ 0802855c 2c6c0000
DWORD_08028560:
    .word  font_jp_base_table             @ 08028560 54f8e509
DWORD_08028564:
    .word  0x06004000                     @ 08028564 00400006

@ Function: campaign card select screen text line renderer (aligned variant). Structure highly symmetric with render_campaign_text_line_centered (0x08028418); differences: uses setup_line_buf_with_font_and_align instead of setup_line_buf_pos_and_font (extra align=2, color=1 params); reads sp[0x2c] as bool_center (6th param, frame=0x28, sp[0x2c]=2nd stack arg), performs center offset calculation (calls count_bytes_until_null) only when bool_center!=0; when bool_center==0 skips centering and calls setup directly with r0=r8 (col_x). Reads sp[0x28] as text_str passed to text_render_wrapper. Remaining flow (style bits write / text_render_wrapper / zero_fill / commit_line_buffer_to_sprite_vram / tile write loop) identical to centered variant. Exit pop {r1}; bx r1 (Sub-case E).
@ 
@ Side effects:
@ - [0x02006ed0+8] := style bits
@ - VRAM 0x06004000 + tile_offset: zero fill + text pixels + tile index
@ 
@ Constants:
@ - GAME_STATE_FLAG_BASE = 0x02000000
@ - GAME_STATE_OFFSET = 0x6c2c
@ - LINE_BUF_STYLE_PTR = 0x02006ed0
@ - FONT_BASE_TABLE = font_jp_base_table
@ - BG_VRAM_BASE = 0x06004000
@ - ALIGN_PARAM = 2 // setup_line_buf_with_font_and_align r3 arg
@ - COLOR_PARAM = 1 // setup_line_buf_with_font_and_align r2 arg
render_campaign_text_line_with_align:
    push {r4,r5,r6,r7,lr}                    @ 08028568 f0b5
    .hword 0x4657    @ 0802856a 5746
    .hword 0x464e    @ 0802856c 4e46
    .hword 0x4645    @ 0802856e 4546
    push {r5,r6,r7}                          @ 08028570 e0b4
    sub sp,#0x8                              @ 08028572 82b0
    ldr r4,[sp,#0x2c]                        @ 08028574 0b9c
    lsls r0,r0,#0x10    @ 08028576 0004
    lsrs r0,r0,#0x10    @ 08028578 000c
    str r0,[sp,#0x0]                         @ 0802857a 0090
    lsls r1,r1,#0x10    @ 0802857c 0904
    lsrs r5,r1,#0x10    @ 0802857e 0d0c
    lsls r2,r2,#0x10    @ 08028580 1204
    lsls r3,r3,#0x10    @ 08028582 1b04
    .hword 0x469a    @ 08028584 9a46
    .hword 0x4650    @ 08028586 5046
    lsrs r0,r0,#0x10    @ 08028588 000c
    str r0,[sp,#0x4]                         @ 0802858a 0190
    lsls r0,r2,#0x8    @ 0802858c 1002
    lsrs r6,r0,#0x18    @ 0802858e 060e
    lsrs r7,r2,#0x18    @ 08028590 170e
    movs r1,#0x2    @ 08028592 0221
    .hword 0x4689    @ 08028594 8946
    .hword 0x4688    @ 08028596 8846
    cmp r4,#0x0                              @ 08028598 002c
    beq LAB_080285b2                         @ 0802859a 0ad0
    ldr r0,[sp,#0x28]                        @ 0802859c 0a98
    bl count_bytes_until_null                @ 0802859e ccf09fff
    lsls r2,r6,#0x2    @ 080285a2 b200
    lsls r1,r0,#0x1    @ 080285a4 4100
    adds r1,r1,r0    @ 080285a6 0918
    subs r2,r2,r1    @ 080285a8 521a
    .hword 0x4691    @ 080285aa 9146
    lsls r0,r7,#0x2    @ 080285ac b800
    subs r0,#0x5    @ 080285ae 0538
    .hword 0x4680    @ 080285b0 8046
LAB_080285b2:
    adds r0,r6,#0x0    @ 080285b2 301c
    adds r1,r7,#0x0    @ 080285b4 391c
    movs r2,#0x1    @ 080285b6 0122
    movs r3,#0x2    @ 080285b8 0223
    bl setup_line_buf_with_font_and_align    @ 080285ba c8f081fb
    ldr r2, DWORD_08028680                   @ 080285be 304a
    ldr r0, DWORD_08028684                   @ 080285c0 3048
    ldr r3, DWORD_08028688                   @ 080285c2 314b
    adds r0,r0,r3    @ 080285c4 c018
    movs r1,#0x7    @ 080285c6 0721
    ldrb r0,[r0,#0x0]                        @ 080285c8 0078
    ands r1,r0    @ 080285ca 0140
    rsbs r1,r1,#0    @ 080285cc 4942
    lsrs r1,r1,#0x1f    @ 080285ce c90f
    movs r0,#0x2    @ 080285d0 0220
    rsbs r0,r0,#0    @ 080285d2 4042
    ldrb r4,[r2,#0x8]                        @ 080285d4 147a
    ands r0,r4    @ 080285d6 2040
    orrs r0,r1    @ 080285d8 0843
    movs r1,#0x2    @ 080285da 0221
    orrs r0,r1    @ 080285dc 0843
    strb r0,[r2,#0x8]                        @ 080285de 1072
    ldr r3, DWORD_0802868c                   @ 080285e0 2a4b
    lsls r1,r0,#0x1e    @ 080285e2 8107
    lsrs r1,r1,#0x1f    @ 080285e4 c90f
    lsls r1,r1,#0x2    @ 080285e6 8900
    lsls r0,r0,#0x1f    @ 080285e8 c007
    lsrs r0,r0,#0x1f    @ 080285ea c00f
    lsls r0,r0,#0x3    @ 080285ec c000
    adds r1,r1,r0    @ 080285ee 0918
    adds r1,r1,r3    @ 080285f0 c918
    ldr r0,[r1,#0x0]                         @ 080285f2 0868
    str r0,[r2,#0x4]                         @ 080285f4 5060
    .hword 0x4650    @ 080285f6 5046
    lsrs r2,r0,#0x18    @ 080285f8 020e
    cmp r2,#0x0                              @ 080285fa 002a
    beq LAB_08028610                         @ 080285fc 08d0
    movs r1,#0x80    @ 080285fe 8021
    lsls r1,r1,#0x8    @ 08028600 0902
    adds r0,r1,#0x0    @ 08028602 081c
    orrs r2,r0    @ 08028604 0243
    .hword 0x4648    @ 08028606 4846
    .hword 0x4641    @ 08028608 4146
    ldr r3,[sp,#0x28]                        @ 0802860a 0a9b
    bl text_render_wrapper                   @ 0802860c caf036fa
LAB_08028610:
    ldr r3,[sp,#0x4]                         @ 08028610 019b
    lsls r2,r3,#0x18    @ 08028612 1a06
    lsrs r2,r2,#0x18    @ 08028614 120e
    .hword 0x4648    @ 08028616 4846
    .hword 0x4641    @ 08028618 4146
    ldr r3,[sp,#0x28]                        @ 0802861a 0a9b
    bl text_render_wrapper                   @ 0802861c caf02efa
    lsls r4,r5,#0x5    @ 08028620 6c01
    ldr r0, DWORD_08028690                   @ 08028622 1b48
    adds r4,r4,r0    @ 08028624 2418
    lsls r0,r7,#0x5    @ 08028626 7801
    adds r1,r6,#0x0    @ 08028628 311c
    muls r1,r0    @ 0802862a 4143
    adds r0,r4,#0x0    @ 0802862c 201c
    bl zero_fill_by_halfword                 @ 0802862e ccf021fc
    adds r0,r4,#0x0    @ 08028632 201c
    movs r1,#0x0    @ 08028634 0021
    bl commit_line_buffer_to_sprite_vram     @ 08028636 caf009fc
    movs r1,#0x0    @ 0802863a 0021
    cmp r1,r7                                @ 0802863c b942
    bge LAB_0802866e                         @ 0802863e 16da
    movs r4,#0xc0    @ 08028640 c024
    lsls r4,r4,#0x13    @ 08028642 e404
LAB_08028644:
    lsls r0,r1,#0x10    @ 08028644 0804
    lsrs r0,r0,#0xb    @ 08028646 c00a
    ldr r2,[sp,#0x0]                         @ 08028648 009a
    adds r0,r2,r0    @ 0802864a 1018
    lsls r0,r0,#0x1    @ 0802864c 4000
    adds r2,r0,r4    @ 0802864e 0219
    adds r3,r1,#0x1    @ 08028650 4b1c
    cmp r6,#0x0                              @ 08028652 002e
    beq LAB_08028668                         @ 08028654 08d0
    adds r1,r6,#0x0    @ 08028656 311c
LAB_08028658:
    strh r5,[r2,#0x0]                        @ 08028658 1580
    adds r2,#0x2    @ 0802865a 0232
    adds r0,r5,#0x1    @ 0802865c 681c
    lsls r0,r0,#0x10    @ 0802865e 0004
    lsrs r5,r0,#0x10    @ 08028660 050c
    subs r1,#0x1    @ 08028662 0139
    cmp r1,#0x0                              @ 08028664 0029
    bne LAB_08028658                         @ 08028666 f7d1
LAB_08028668:
    adds r1,r3,#0x0    @ 08028668 191c
    cmp r1,r7                                @ 0802866a b942
    blt LAB_08028644                         @ 0802866c eadb
LAB_0802866e:
    add sp,#0x8                              @ 0802866e 02b0
    pop {r3,r4,r5}                           @ 08028670 38bc
    .hword 0x4698    @ 08028672 9846
    .hword 0x46a1    @ 08028674 a146
    .hword 0x46aa    @ 08028676 aa46
    pop {r4,r5,r6,r7}                        @ 08028678 f0bc
    pop {r0}                                 @ 0802867a 01bc
    bx r0                                    @ 0802867c 0047
    .zero  0x2
DWORD_08028680:
    .word  0x02006ed0                     @ 08028680 d06e0002
DWORD_08028684:
    .word  0x02000000                     @ 08028684 00000002
DWORD_08028688:
    .word  0x00006c2c                     @ 08028688 2c6c0000
DWORD_0802868c:
    .word  font_jp_base_table             @ 0802868c 54f8e509
DWORD_08028690:
    .word  0x06004000                     @ 08028690 00400006

@ Function: initialize pack scene VRAM and display state. No APCS input params (r0 overwritten by ldr gPrng at entry). Execution order: (1) write 0x601 to gPrng+0xba*2=gPrng+0x174 (display control value); (2) write 0 to DISPCNT=0x04000000 (disable display); (3) call reset_display_and_obj_vram (clear OBJ VRAM and display registers); (4) call store_ewram_ctx_ptr_and_clear_mode_flags (write EWRAM context pointer, clear mode flags); (5) write 4 halfwords consecutively to BG0CNT-BG3CNT (bg_ctrl[0..3]={0x4,0x105,0x206,0x307}); (6) call reset_all_bg_scroll_regs_and_shadows + upload_pack_vram_and_palette; (7) three zero_fill_by_halfword calls to clear 0x06004000/0x06010000 and another region (r4=0x8000 halfwords = 0x10000 bytes each call). Exit pop {r0}; bx r0 (Sub-case E, r0 overwritten by pop -> void).
@ 
@ Side effects:
@ - [gPrng+0x174] := 0x601
@ - [DISPCNT=0x04000000] := 0
@ - [BG0CNT=0x04000004] := 0x0004
@ - [BG1CNT=0x04000006] := 0x0105
@ - [BG2CNT=0x04000008] := 0x0206
@ - [BG3CNT=0x0400000a] := 0x0307
@ - VRAM 0x06004000 (0x10000 bytes): zero fill
@ - VRAM 0x06010000 (0x10000 bytes): zero fill
@ - EWRAM ctx ptr: via store_ewram_ctx_ptr_and_clear_mode_flags
@ 
@ Constants:
@ - DISPCNT = 0x04000000
@ - BG0CNT = 0x04000004
@ - PRNG_CTRL_FIELD_OFFSET = 0xba*2 = 0x174
@ - PRNG_CTRL_VALUE = 0x601
@ - BG0_CTRL = 0x0004 // BG0 priority 0, tile base 0
@ - BG1_CTRL = 0x0105 // BG1 priority 1, tile base 1
@ - BG2_CTRL = 0x0206 // BG2 priority 2, tile base 2
@ - BG3_CTRL = 0x0307 // BG3 priority 3, tile base 3
@ - VRAM_OBJ_BASE = 0x06004000
@ - VRAM_BG_BASE = 0x06010000
@ - ZERO_FILL_SIZE = 0x80<<8 = 0x8000 halfwords (= 0x10000 bytes per call)
init_pack_scene_vram_regs:
    push {r4,lr}                             @ 08028694 10b5
    ldr r0, DWORD_08028704                   @ 08028696 1b48
    movs r1,#0xba    @ 08028698 ba21
    lsls r1,r1,#0x1    @ 0802869a 4900
    adds r0,r0,r1    @ 0802869c 4018
    movs r2,#0x0    @ 0802869e 0022
    ldr r1, DWORD_08028708                   @ 080286a0 1949
    strh r1,[r0,#0x0]                        @ 080286a2 0180
    movs r0,#0x80    @ 080286a4 8020
    lsls r0,r0,#0x13    @ 080286a6 c004
    strh r2,[r0,#0x0]                        @ 080286a8 0280
    ldr r0, DWORD_0802870c                   @ 080286aa 1848
    bl reset_display_and_obj_vram            @ 080286ac cef0e2ff
    ldr r0, DWORD_08028710                   @ 080286b0 1748
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 080286b2 cbf0f5fd
    ldr r1, DWORD_08028714                   @ 080286b6 1749
    movs r0,#0x4    @ 080286b8 0420
    strh r0,[r1,#0x0]                        @ 080286ba 0880
    adds r1,#0x2    @ 080286bc 0231
    ldr r2, DWORD_08028718                   @ 080286be 164a
    adds r0,r2,#0x0    @ 080286c0 101c
    strh r0,[r1,#0x0]                        @ 080286c2 0880
    adds r1,#0x2    @ 080286c4 0231
    ldr r2, DWORD_0802871c                   @ 080286c6 154a
    adds r0,r2,#0x0    @ 080286c8 101c
    strh r0,[r1,#0x0]                        @ 080286ca 0880
    adds r1,#0x2    @ 080286cc 0231
    ldr r2, DWORD_08028720                   @ 080286ce 144a
    adds r0,r2,#0x0    @ 080286d0 101c
    strh r0,[r1,#0x0]                        @ 080286d2 0880
    bl reset_all_bg_scroll_regs_and_shadows  @ 080286d4 cdf0d8f9
    bl upload_pack_vram_and_palette          @ 080286d8 cdf0def9
    ldr r0, DWORD_08028724                   @ 080286dc 1148
    movs r4,#0x80    @ 080286de 8024
    lsls r4,r4,#0x8    @ 080286e0 2402
    adds r1,r4,#0x0    @ 080286e2 211c
    bl zero_fill_by_halfword                 @ 080286e4 ccf0c6fb
    movs r0,#0xc0    @ 080286e8 c020
    lsls r0,r0,#0x13    @ 080286ea c004
    movs r1,#0x80    @ 080286ec 8021
    lsls r1,r1,#0x6    @ 080286ee 8901
    bl zero_fill_by_halfword                 @ 080286f0 ccf0c0fb
    ldr r0, DWORD_08028728                   @ 080286f4 0c48
    adds r1,r4,#0x0    @ 080286f6 211c
    bl zero_fill_by_halfword                 @ 080286f8 ccf0bcfb
    pop {r4}                                 @ 080286fc 10bc
    pop {r0}                                 @ 080286fe 01bc
    bx r0                                    @ 08028700 0047
    .zero  0x2
DWORD_08028704:
    .word  gPrng                          @ 08028704 40000003
DWORD_08028708:
    .word  0x00000601                     @ 08028708 01060000
DWORD_0802870c:
    .word  0x0203eeb0                     @ 0802870c b0ee0302
DWORD_08028710:
    .word  0x02029eb0                     @ 08028710 b09e0202
DWORD_08028714:
    .word  BG0CNT                         @ 08028714 08000004
DWORD_08028718:
    .word  0x00000105                     @ 08028718 05010000
DWORD_0802871c:
    .word  0x00000206                     @ 0802871c 06020000
DWORD_08028720:
    .word  0x00000307                     @ 08028720 07030000
DWORD_08028724:
    .word  0x06004000                     @ 08028724 00400006
DWORD_08028728:
    .word  0x06010000                     @ 08028728 00000106

@ Function: select one of two pack tile loading paths based on r0 flag, then initialize palette flags. When r0==0: loads pack tile set B (0x09ba050c, 0x30 tiles, 2bpp mode 0x4e) to VRAM 0xc00 and pack tile set C (0x09b9fa20, 0x20 tiles, mode 0x2) to VRAM 0x800. When r0!=0: loads only pack tile set A (0x09b9e6e8, 0x10 tiles, mode 0x2) to VRAM 0xc00. Both paths converge: copy_bytes_by_halfword copies 0x20 halfwords from ROM 0x09b9e6c8 to PAL_RAM 0x05000220; tile_2d_row_copy copies 0x20x8 rows from ROM 0x09b9c6c8 to VRAM 0x06010000; sets bit0 of byte [0x02023360+0x36] (palette init flag). Exit pop {r0}; bx r0 (Sub-case E, void).
@ 
@ Side effects:
@ - VRAM tile offset 0xc00 (or 0x800): pack tile data written via load_pack_tile_and_map_to_vram
@ - PAL_RAM 0x05000220: 0x20 halfwords (64 bytes) palette copy
@ - VRAM 0x06010000: 0x20x8 = 0x100 rows tile 2D copy
@ - [0x02023360+0x36] bit0 := 1 (palette init flag)
@ 
@ Constants:
@ - VRAM_TILE_BASE_C = 0xc00 (0xc0<<4, OBJ tile index)
@ - VRAM_TILE_BASE_B = 0x800 (0x80<<4)
@ - PACK_TILES_A = 0x09b9e6e8 (r0!=0 path: 16 tiles, mode 2)
@ - PACK_TILES_B = 0x09ba050c (r0==0 path: 48 tiles, mode 0x4e)
@ - PACK_TILES_C = 0x09b9fa20 (r0==0 path: 32 tiles, mode 2)
@ - PACK_PAL_SRC = 0x09b9e6c8 // palette data source (32 halfwords)
@ - PAL_RAM_DEST = 0x05000220
@ - VRAM_BG_BASE = 0x06010000
@ - PAL_INIT_FLAG_OFFSET = 0x36 // [0x02023360+0x36] bit0
load_pack_tiles_with_palette_init:
    push {lr}                                @ 0802872c 00b5
    cmp r0,#0x0                              @ 0802872e 0028
    beq LAB_08028748                         @ 08028730 0ad0
    movs r0,#0xc0    @ 08028732 c020
    lsls r0,r0,#0x4    @ 08028734 0001
    ldr r3, DWORD_08028744                   @ 08028736 034b
    movs r1,#0x10    @ 08028738 1021
    movs r2,#0x2    @ 0802873a 0222
    bl load_pack_tile_and_map_to_vram        @ 0802873c c5f068fc
    b LAB_08028764                           @ 08028740 10e0
    .zero  0x2
DWORD_08028744:
    .word  0x09b9e6e8                     @ 08028744 e8e6b909
LAB_08028748:
    movs r0,#0xc0    @ 08028748 c020
    lsls r0,r0,#0x4    @ 0802874a 0001
    ldr r3, DWORD_0802878c                   @ 0802874c 0f4b
    movs r1,#0x30    @ 0802874e 3021
    movs r2,#0x4e    @ 08028750 4e22
    bl load_pack_tile_and_map_to_vram        @ 08028752 c5f05dfc
    movs r0,#0x80    @ 08028756 8020
    lsls r0,r0,#0x4    @ 08028758 0001
    ldr r3, DWORD_08028790                   @ 0802875a 0d4b
    movs r1,#0x20    @ 0802875c 2021
    movs r2,#0x2    @ 0802875e 0222
    bl load_pack_tile_and_map_to_vram        @ 08028760 c5f056fc
LAB_08028764:
    ldr r0, DWORD_08028794                   @ 08028764 0b48
    ldr r1, DWORD_08028798                   @ 08028766 0c49
    movs r2,#0x20    @ 08028768 2022
    bl copy_bytes_by_halfword                @ 0802876a ccf09bfb
    ldr r0, DWORD_0802879c                   @ 0802876e 0b48
    ldr r1, DWORD_080287a0                   @ 08028770 0b49
    movs r2,#0x20    @ 08028772 2022
    movs r3,#0x8    @ 08028774 0823
    bl tile_2d_row_copy                      @ 08028776 cef0adfe
    ldr r1, DWORD_080287a4                   @ 0802877a 0a49
    adds r1,#0x36    @ 0802877c 3631
    movs r0,#0x1    @ 0802877e 0120
    ldrb r2,[r1,#0x0]                        @ 08028780 0a78
    orrs r0,r2    @ 08028782 1043
    strb r0,[r1,#0x0]                        @ 08028784 0870
    pop {r0}                                 @ 08028786 01bc
    bx r0                                    @ 08028788 0047
    .zero  0x2
DWORD_0802878c:
    .word  0x09ba050c                     @ 0802878c 0c05ba09
DWORD_08028790:
    .word  0x09b9fa20                     @ 08028790 20fab909
DWORD_08028794:
    .word  0x05000220                     @ 08028794 20020005
DWORD_08028798:
    .word  0x09b9e6c8                     @ 08028798 c8e6b909
DWORD_0802879c:
    .word  0x06010000                     @ 0802879c 00000106
DWORD_080287a0:
    .word  0x09b9c6c8                     @ 080287a0 c8c6b909
DWORD_080287a4:
    .word  0x02023360                     @ 080287a4 60330202

@ Function: write 3 OAM entries for pack scene sprite strip. Reads gPrng+0x20c halfword bits[4:2] as 3-bit index (0..7), fetches corresponding tile_id halfword from ROM table 0x09e59d78 (r4); using r0=x_pos [0x1b..0x4c], r1=y_row [0x40..0x8a] as position params, loops 3 times (r6=2..0): calls write_oam_entry_from_packed_args(packed_xy, attr1=0x4080 (0x81<<7), tile_id+delta), each iteration tile_id advances +4, x advances +0x20. Exit pop {r0}; bx r0 (Sub-case E, void).
@ 
@ Side effects:
@ - OAM: write_oam_entry_from_packed_args x3 writes 3 sprite entries
@ 
@ Constants:
@ - ROM_TILE_TABLE = 0x09e59d78 // 8-entry halfword table, indexed by gPrng field
@ - PRNG_FIELD_OFFSET = 0x20c // gPrng+0x20c, bits[4:2]
@ - OAM_ATTR1 = 0x4080 (0x81<<7)
@ - TILE_Y_DELTA = 0x1000 (0x80<<5)
@ - X_STEP = 0x20
@ - TILE_STEP = 4
write_pack_strip_oam_entries:
    push {r4,r5,r6,r7,lr}                    @ 080287a8 f0b5
    adds r5,r0,#0x0    @ 080287aa 051c
    adds r7,r1,#0x0    @ 080287ac 0f1c
    ldr r2, DWORD_080287f4                   @ 080287ae 114a
    ldr r0, DWORD_080287f8                   @ 080287b0 1148
    movs r1,#0x83    @ 080287b2 8321
    lsls r1,r1,#0x2    @ 080287b4 8900
    adds r0,r0,r1    @ 080287b6 4018
    ldrh r0,[r0,#0x0]                        @ 080287b8 0088
    lsrs r0,r0,#0x2    @ 080287ba 8008
    movs r1,#0x7    @ 080287bc 0721
    ands r0,r1    @ 080287be 0840
    lsls r0,r0,#0x1    @ 080287c0 4000
    adds r0,r0,r2    @ 080287c2 8018
    ldrh r4,[r0,#0x0]                        @ 080287c4 0488
    movs r6,#0x2    @ 080287c6 0226
LAB_080287c8:
    lsls r0,r7,#0x10    @ 080287c8 3804
    orrs r0,r5    @ 080287ca 2843
    movs r1,#0x80    @ 080287cc 8021
    lsls r1,r1,#0x5    @ 080287ce 4901
    adds r2,r4,r1    @ 080287d0 6218
    lsls r2,r2,#0x10    @ 080287d2 1204
    lsrs r2,r2,#0x10    @ 080287d4 120c
    movs r1,#0x81    @ 080287d6 8121
    lsls r1,r1,#0x7    @ 080287d8 c901
    bl write_oam_entry_from_packed_args      @ 080287da cdf0c7fc
    adds r0,r4,#0x4    @ 080287de 201d
    lsls r0,r0,#0x10    @ 080287e0 0004
    lsrs r4,r0,#0x10    @ 080287e2 040c
    adds r5,#0x20    @ 080287e4 2035
    subs r6,#0x1    @ 080287e6 013e
    cmp r6,#0x0                              @ 080287e8 002e
    bge LAB_080287c8                         @ 080287ea edda
    pop {r4,r5,r6,r7}                        @ 080287ec f0bc
    pop {r0}                                 @ 080287ee 01bc
    bx r0                                    @ 080287f0 0047
    .zero  0x2
DWORD_080287f4:
    .word  0x09e59d78                     @ 080287f4 789de509
DWORD_080287f8:
    .word  gPrng                          @ 080287f8 40000003

@ Function: write up to 2 OAM entries for pack card grid (10-column layout). r0 is row base pointer (+6), r1 is column index (pack position packed), r2 is tile_base (u32, saved to r8), r3 is y offset (saved to r5, scaled <<6). Computes tile_base % 10 (column position) + y_scaled -> r2 (column coordinate); generates initial r2 from r9=0x188; calls write_oam_entry_from_packed_args to write 1st OAM sprite (r0=packed_pos, r1=r10=0x8000, r2=column_pos). Then computes tile_base / 10: if tile_base/10 == 0 jumps to end; otherwise ORs 0x3f with row_base+6 bit field (orrs r6,r7) then computes %10 for 2nd sprite column position, calls write_oam_entry_from_packed_args to write 2nd OAM sprite. Exit pop {r0}; bx r0 (Sub-case E, void).
@ 
@ Side effects:
@ - OAM: write_oam_entry_from_packed_args x1 or x2 writes pack grid sprites
@ 
@ Constants:
@ - COL_COUNT = 10 // __modsi3 / __divsi3 divisor = 10 columns
@ - TILE_Y_SCALE = 0x40 (r5 <<= 6)
@ - ATTR1_BASE = 0x8000 (0x80<<8) // saved to r10
@ - COL_BASE_OFFSET = 0x188 (0xc4<<1) // column base offset saved to r9
@ - ROW_ADJUST = 6 // r7 = r0+6 (row base offset)
write_pack_grid_oam_by_card_slot:
    push {r4,r5,r6,r7,lr}                    @ 080287fc f0b5
    .hword 0x4657    @ 080287fe 5746
    .hword 0x464e    @ 08028800 4e46
    .hword 0x4645    @ 08028802 4546
    push {r5,r6,r7}                          @ 08028804 e0b4
    adds r7,r0,#0x0    @ 08028806 071c
    .hword 0x4690    @ 08028808 9046
    adds r5,r3,#0x0    @ 0802880a 1d1c
    adds r7,#0x6    @ 0802880c 0637
    lsls r6,r1,#0x10    @ 0802880e 0e04
    adds r4,r7,#0x0    @ 08028810 3c1c
    orrs r4,r6    @ 08028812 3443
    movs r0,#0x80    @ 08028814 8020
    lsls r0,r0,#0x8    @ 08028816 0002
    .hword 0x4682    @ 08028818 8246
    .hword 0x4640    @ 0802881a 4046
    movs r1,#0xa    @ 0802881c 0a21
    bl __modsi3                              @ 0802881e e5f03dff
    adds r2,r0,#0x0    @ 08028822 021c
    lsls r5,r5,#0x6    @ 08028824 ad01
    adds r2,r2,r5    @ 08028826 5219
    movs r0,#0xc4    @ 08028828 c420
    lsls r0,r0,#0x1    @ 0802882a 4000
    .hword 0x4681    @ 0802882c 8146
    add r2,r9                                @ 0802882e 4a44
    lsls r2,r2,#0x10    @ 08028830 1204
    lsrs r2,r2,#0x10    @ 08028832 120c
    adds r0,r4,#0x0    @ 08028834 201c
    .hword 0x4651    @ 08028836 5146
    bl write_oam_entry_from_packed_args      @ 08028838 cdf098fc
    .hword 0x4640    @ 0802883c 4046
    movs r1,#0xa    @ 0802883e 0a21
    bl __divsi3                              @ 08028840 e5f0e0fe
    subs r7,#0x6    @ 08028844 063f
    cmp r0,#0x0                              @ 08028846 0028
    ble LAB_08028864                         @ 08028848 0cdd
    orrs r6,r7    @ 0802884a 3e43
    movs r1,#0xa    @ 0802884c 0a21
    bl __modsi3                              @ 0802884e e5f025ff
    adds r2,r0,#0x0    @ 08028852 021c
    adds r2,r2,r5    @ 08028854 5219
    add r2,r9                                @ 08028856 4a44
    lsls r2,r2,#0x10    @ 08028858 1204
    lsrs r2,r2,#0x10    @ 0802885a 120c
    adds r0,r6,#0x0    @ 0802885c 301c
    .hword 0x4651    @ 0802885e 5146
    bl write_oam_entry_from_packed_args      @ 08028860 cdf084fc
LAB_08028864:
    pop {r3,r4,r5}                           @ 08028864 38bc
    .hword 0x4698    @ 08028866 9846
    .hword 0x46a1    @ 08028868 a146
    .hword 0x46aa    @ 0802886a aa46
    pop {r4,r5,r6,r7}                        @ 0802886c f0bc
    pop {r0}                                 @ 0802886e 01bc
    bx r0                                    @ 08028870 0047
    .zero  0x2

@ Campaign card-select UI OAM frame tick. Reads 0x02023360+0x36 byte bits[6:3] as display_mode [0..3] and dispatches four ways: mode 0/2: using ROM table base 0x09e59d38 and OAM attr table 0x0300024c, loops 0x1d times (29 OAM entries), calls write_oam_entry_from_packed_args and write_oam_entry_with_slot_check to write OAM attrs; mode 1: checks gPrng+0x20c halfword bit4 (mask 0x10), if condition met enters alternate branch render; mode 3: reads effect_slot data, validates slot match, then calls write_oam_entry_from_packed_args + write_oam_entry_with_slot_check. indeg=0, Sub-type A (no fn-ptr table reference found). Returns void (Pattern B).
@ 
@ Params: r0=(none -- no APCS input; push {r4..r7}; internal load r7=0x02023360 at entry)
@ Returns: void (Pattern B: pop {r0}; bx r0)
@ Side effects: via write_oam_entry_from_packed_args: OAM entry attr0/attr1/attr2 written (mode 0/2/3 paths); via write_oam_entry_with_slot_check: OAM entry written after validity check (mode 0/2/3 paths)
@ Constants: SCENE_BASE=0x02023360; DISPLAY_MODE_OFF=0x36 (bits[6:3]=[0..3]); OAM_TABLE_BASE=0x09e59d38; OAM_ATTR_BASE=0x0300024c; LOOP_COUNT=0x1d=29; OAM_ATTR0_BASE=0x90<<14=0x240000; OAM_ATTR1_BASE=0x8c<<15=0x460000
tick_campaign_card_selector_oam:
    push {r4,r5,r6,r7,lr}                    @ 08028874 f0b5
    .hword 0x464f    @ 08028876 4f46
    .hword 0x4646    @ 08028878 4646
    push {r6,r7}                             @ 0802887a c0b4
    ldr r7, DWORD_08028898                   @ 0802887c 064f
    adds r0,r7,#0x0    @ 0802887e 381c
    adds r0,#0x36    @ 08028880 3630
    ldrb r0,[r0,#0x0]                        @ 08028882 0078
    lsls r0,r0,#0x1b    @ 08028884 c006
    lsrs r0,r0,#0x1c    @ 08028886 000f
    cmp r0,#0x1                              @ 08028888 0128
    beq LAB_08028920                         @ 0802888a 49d0
    cmp r0,#0x1                              @ 0802888c 0128
    bgt LAB_0802889c                         @ 0802888e 05dc
    cmp r0,#0x0                              @ 08028890 0028
    beq LAB_080288a6                         @ 08028892 08d0
    b LAB_08028bba                           @ 08028894 91e1
    .zero  0x2
DWORD_08028898:
    .word  0x02023360                     @ 08028898 60330202
LAB_0802889c:
    cmp r0,#0x2                              @ 0802889c 0228
    beq LAB_080288a6                         @ 0802889e 02d0
    cmp r0,#0x3                              @ 080288a0 0328
    beq LAB_0802894c                         @ 080288a2 53d0
    b LAB_08028bba                           @ 080288a4 89e1
LAB_080288a6:
    movs r5,#0x0    @ 080288a6 0025
    ldr r0, DWORD_08028918                   @ 080288a8 1b48
    .hword 0x4680    @ 080288aa 8046
    ldr r1, DWORD_0802891c                   @ 080288ac 1b49
    .hword 0x4689    @ 080288ae 8946
    movs r6,#0x0    @ 080288b0 0026
    movs r7,#0x1f    @ 080288b2 1f27
LAB_080288b4:
    adds r1,r7,#0x0    @ 080288b4 391c
    .hword 0x464a    @ 080288b6 4a46
    ldrh r2,[r2,#0x0]                        @ 080288b8 1288
    ands r1,r2    @ 080288ba 1140
    adds r0,r1,#0x0    @ 080288bc 081c
    subs r0,#0x20    @ 080288be 2038
    subs r0,r5,r0    @ 080288c0 281a
    ands r0,r7    @ 080288c2 3840
    lsls r0,r0,#0x1    @ 080288c4 4000
    add r0,r8                                @ 080288c6 4044
    ldrh r2,[r0,#0x0]                        @ 080288c8 0288
    adds r1,#0x20    @ 080288ca 2031
    adds r1,r5,r1    @ 080288cc 6918
    ands r1,r7    @ 080288ce 3940
    lsls r1,r1,#0x1    @ 080288d0 4900
    add r1,r8                                @ 080288d2 4144
    ldrh r4,[r1,#0x0]                        @ 080288d4 0c88
    cmp r2,#0x0                              @ 080288d6 002a
    ble LAB_080288f0                         @ 080288d8 0add
    movs r0,#0x90    @ 080288da 9020
    lsls r0,r0,#0xe    @ 080288dc 8003
    orrs r0,r6    @ 080288de 3043
    movs r3,#0x80    @ 080288e0 8023
    lsls r3,r3,#0x5    @ 080288e2 5b01
    adds r2,r2,r3    @ 080288e4 d218
    lsls r2,r2,#0x10    @ 080288e6 1204
    lsrs r2,r2,#0x10    @ 080288e8 120c
    movs r1,#0x0    @ 080288ea 0021
    bl write_oam_entry_from_packed_args      @ 080288ec cdf03efc
LAB_080288f0:
    cmp r4,#0x0                              @ 080288f0 002c
    ble LAB_0802890e                         @ 080288f2 0cdd
    movs r0,#0x8c    @ 080288f4 8c20
    lsls r0,r0,#0xf    @ 080288f6 c003
    orrs r0,r6    @ 080288f8 3043
    movs r1,#0x80    @ 080288fa 8021
    lsls r1,r1,#0x5    @ 080288fc 4901
    adds r2,r4,r1    @ 080288fe 6218
    lsls r2,r2,#0x10    @ 08028900 1204
    lsrs r2,r2,#0x10    @ 08028902 120c
    movs r1,#0x0    @ 08028904 0021
    movs r3,#0x80    @ 08028906 8023
    lsls r3,r3,#0x5    @ 08028908 5b01
    bl write_oam_entry_with_slot_check       @ 0802890a cdf073ff
LAB_0802890e:
    adds r6,#0x8    @ 0802890e 0836
    adds r5,#0x1    @ 08028910 0135
    cmp r5,#0x1d                             @ 08028912 1d2d
    ble LAB_080288b4                         @ 08028914 cedd
    b LAB_08028bba                           @ 08028916 50e1
DWORD_08028918:
    .word  0x09e59d38                     @ 08028918 389de509
DWORD_0802891c:
    .word  0x0300024c                     @ 0802891c 4c020003
LAB_08028920:
    ldr r1, DWORD_08028944                   @ 08028920 0849
    movs r2,#0x83    @ 08028922 8322
    lsls r2,r2,#0x2    @ 08028924 9200
    adds r1,r1,r2    @ 08028926 8918
    movs r0,#0x10    @ 08028928 1020
    ldrh r1,[r1,#0x0]                        @ 0802892a 0988
    ands r0,r1    @ 0802892c 0840
    cmp r0,#0x0                              @ 0802892e 0028
    bne LAB_08028934                         @ 08028930 00d1
    b LAB_08028bba                           @ 08028932 42e1
LAB_08028934:
    ldr r0, DWORD_08028948                   @ 08028934 0448
    movs r2,#0x82    @ 08028936 8222
    lsls r2,r2,#0x5    @ 08028938 5201
    movs r1,#0x80    @ 0802893a 8021
    bl write_oam_entry_from_packed_args      @ 0802893c cdf016fc
    b LAB_08028bba                           @ 08028940 3be1
    .zero  0x2
DWORD_08028944:
    .word  gPrng                          @ 08028944 40000003
DWORD_08028948:
    .word  0x0060006e                     @ 08028948 6e006000
LAB_0802894c:
    movs r3,#0xc0    @ 0802894c c023
    lsls r3,r3,#0x1    @ 0802894e 5b00
    .hword 0x4698    @ 08028950 9846
    .hword 0x4640    @ 08028952 4046
    ldrh r1,[r7,#0x36]                       @ 08028954 f98e
    ands r0,r1    @ 08028956 0840
    movs r2,#0x37    @ 08028958 3722
    adds r2,r2,r7    @ 0802895a d219
    .hword 0x4691    @ 0802895c 9146
    cmp r0,#0x0                              @ 0802895e 0028
    bne LAB_08028976                         @ 08028960 09d1
    ldrb r3,[r2,#0x0]                        @ 08028962 1378
    lsls r1,r3,#0x1e    @ 08028964 9907
    lsrs r1,r1,#0x1f    @ 08028966 c90f
    lsls r0,r1,#0x3    @ 08028968 c800
    subs r0,r0,r1    @ 0802896a 401a
    lsls r0,r0,#0x4    @ 0802896c 0001
    adds r0,#0x1b    @ 0802896e 1b30
    movs r1,#0x40    @ 08028970 4021
    bl write_pack_strip_oam_entries          @ 08028972 fff719ff
LAB_08028976:
    ldr r0, DWORD_08028a34                   @ 08028976 2f48
    movs r5,#0x81    @ 08028978 8125
    lsls r5,r5,#0x7    @ 0802897a ed01
    .hword 0x464e    @ 0802897c 4e46
    ldrb r1,[r6,#0x0]                        @ 0802897e 3178
    lsls r2,r1,#0x1e    @ 08028980 8a07
    lsrs r2,r2,#0x1f    @ 08028982 d20f
    lsls r2,r2,#0x6    @ 08028984 9201
    movs r3,#0x80    @ 08028986 8023
    lsls r3,r3,#0x1    @ 08028988 5b00
    adds r1,r3,#0x0    @ 0802898a 191c
    orrs r2,r1    @ 0802898c 0a43
    adds r1,r5,#0x0    @ 0802898e 291c
    bl write_oam_entry_from_packed_args      @ 08028990 cdf0ecfb
    ldr r0, DWORD_08028a38                   @ 08028994 2848
    ldrb r1,[r6,#0x0]                        @ 08028996 3178
    lsls r2,r1,#0x1e    @ 08028998 8a07
    lsrs r2,r2,#0x1f    @ 0802899a d20f
    lsls r2,r2,#0x6    @ 0802899c 9201
    movs r3,#0x82    @ 0802899e 8223
    lsls r3,r3,#0x1    @ 080289a0 5b00
    adds r1,r3,#0x0    @ 080289a2 191c
    orrs r2,r1    @ 080289a4 0a43
    adds r1,r5,#0x0    @ 080289a6 291c
    bl write_oam_entry_from_packed_args      @ 080289a8 cdf0e0fb
    ldr r0, DWORD_08028a3c                   @ 080289ac 2348
    ldrb r1,[r6,#0x0]                        @ 080289ae 3178
    lsls r2,r1,#0x1e    @ 080289b0 8a07
    lsrs r2,r2,#0x1f    @ 080289b2 d20f
    lsls r2,r2,#0x6    @ 080289b4 9201
    movs r3,#0x84    @ 080289b6 8423
    lsls r3,r3,#0x1    @ 080289b8 5b00
    adds r1,r3,#0x0    @ 080289ba 191c
    orrs r2,r1    @ 080289bc 0a43
    adds r1,r5,#0x0    @ 080289be 291c
    bl write_oam_entry_from_packed_args      @ 080289c0 cdf0d4fb
    ldr r0, DWORD_08028a40                   @ 080289c4 1e48
    movs r2,#0x2    @ 080289c6 0222
    ldrb r1,[r6,#0x0]                        @ 080289c8 3178
    ands r2,r1    @ 080289ca 0a40
    movs r4,#0x2    @ 080289cc 0224
    subs r2,r4,r2    @ 080289ce a21a
    lsls r2,r2,#0x15    @ 080289d0 5205
    movs r3,#0x86    @ 080289d2 8623
    lsls r3,r3,#0x11    @ 080289d4 5b04
    adds r2,r2,r3    @ 080289d6 d218
    lsrs r2,r2,#0x10    @ 080289d8 120c
    adds r1,r5,#0x0    @ 080289da 291c
    bl write_oam_entry_from_packed_args      @ 080289dc cdf0c6fb
    ldr r0, DWORD_08028a44                   @ 080289e0 1848
    movs r2,#0x2    @ 080289e2 0222
    ldrb r1,[r6,#0x0]                        @ 080289e4 3178
    ands r2,r1    @ 080289e6 0a40
    subs r2,r4,r2    @ 080289e8 a21a
    lsls r2,r2,#0x15    @ 080289ea 5205
    movs r3,#0x88    @ 080289ec 8823
    lsls r3,r3,#0x11    @ 080289ee 5b04
    adds r2,r2,r3    @ 080289f0 d218
    lsrs r2,r2,#0x10    @ 080289f2 120c
    adds r1,r5,#0x0    @ 080289f4 291c
    bl write_oam_entry_from_packed_args      @ 080289f6 cdf0b9fb
    ldr r0, DWORD_08028a48                   @ 080289fa 1348
    movs r1,#0x2    @ 080289fc 0221
    ldrb r2,[r6,#0x0]                        @ 080289fe 3278
    ands r1,r2    @ 08028a00 1140
    subs r4,r4,r1    @ 08028a02 641a
    lsls r4,r4,#0x15    @ 08028a04 6405
    movs r3,#0x8a    @ 08028a06 8a23
    lsls r3,r3,#0x11    @ 08028a08 5b04
    adds r4,r4,r3    @ 08028a0a e418
    lsrs r4,r4,#0x10    @ 08028a0c 240c
    adds r1,r5,#0x0    @ 08028a0e 291c
    adds r2,r4,#0x0    @ 08028a10 221c
    bl write_oam_entry_from_packed_args      @ 08028a12 cdf0abfb
    .hword 0x4640    @ 08028a16 4046
    ldrh r1,[r7,#0x36]                       @ 08028a18 f98e
    ands r0,r1    @ 08028a1a 0840
    cmp r0,#0x80                             @ 08028a1c 8028
    bne LAB_08028ac0                         @ 08028a1e 4fd1
    ldrb r3,[r6,#0x0]                        @ 08028a20 3378
    movs r0,#0x7c    @ 08028a22 7c20
    ands r0,r3    @ 08028a24 1840
    cmp r0,#0x0                              @ 08028a26 0028
    bne LAB_08028a4c                         @ 08028a28 10d1
    movs r0,#0x1b    @ 08028a2a 1b20
    movs r1,#0x70    @ 08028a2c 7021
    bl write_pack_strip_oam_entries          @ 08028a2e fff7bbfe
    b LAB_08028ac0                           @ 08028a32 45e0
DWORD_08028a34:
    .word  0x003e0014                     @ 08028a34 14003e00
DWORD_08028a38:
    .word  0x003e0034                     @ 08028a38 34003e00
DWORD_08028a3c:
    .word  0x003e0054                     @ 08028a3c 54003e00
DWORD_08028a40:
    .word  0x003e0084                     @ 08028a40 84003e00
DWORD_08028a44:
    .word  0x003e00a4                     @ 08028a44 a4003e00
DWORD_08028a48:
    .word  0x003e00c4                     @ 08028a48 c4003e00
LAB_08028a4c:
    ldr r2, DWORD_08028b24                   @ 08028a4c 354a
    ldr r0, DWORD_08028b28                   @ 08028a4e 3648
    movs r1,#0x83    @ 08028a50 8321
    lsls r1,r1,#0x2    @ 08028a52 8900
    adds r0,r0,r1    @ 08028a54 4018
    ldrh r0,[r0,#0x0]                        @ 08028a56 0088
    lsrs r0,r0,#0x2    @ 08028a58 8008
    movs r1,#0xf    @ 08028a5a 0f21
    ands r0,r1    @ 08028a5c 0840
    lsls r0,r0,#0x1    @ 08028a5e 4000
    adds r0,r0,r2    @ 08028a60 8018
    ldrh r4,[r0,#0x0]                        @ 08028a62 0488
    lsls r1,r3,#0x18    @ 08028a64 1906
    lsrs r1,r1,#0x1f    @ 08028a66 c90f
    adds r6,r7,#0x0    @ 08028a68 3e1c
    adds r6,#0x38    @ 08028a6a 3836
    movs r7,#0x7f    @ 08028a6c 7f27
    adds r0,r7,#0x0    @ 08028a6e 381c
    ldrb r2,[r6,#0x0]                        @ 08028a70 3278
    ands r0,r2    @ 08028a72 1040
    lsls r0,r0,#0x1    @ 08028a74 4000
    orrs r0,r1    @ 08028a76 0843
    adds r0,#0x80    @ 08028a78 8030
    movs r5,#0xe0    @ 08028a7a e025
    lsls r5,r5,#0xf    @ 08028a7c ed03
    orrs r0,r5    @ 08028a7e 2843
    movs r3,#0x80    @ 08028a80 8023
    lsls r3,r3,#0x8    @ 08028a82 1b02
    .hword 0x4698    @ 08028a84 9846
    ldr r1, DWORD_08028b2c                   @ 08028a86 2949
    adds r2,r4,r1    @ 08028a88 6218
    lsls r2,r2,#0x10    @ 08028a8a 1204
    lsrs r2,r2,#0x10    @ 08028a8c 120c
    .hword 0x4641    @ 08028a8e 4146
    bl write_oam_entry_from_packed_args      @ 08028a90 cdf06cfb
    .hword 0x464a    @ 08028a94 4a46
    ldrb r1,[r2,#0x0]                        @ 08028a96 1178
    lsls r0,r1,#0x19    @ 08028a98 4806
    lsrs r0,r0,#0x1b    @ 08028a9a c00e
    cmp r0,#0xb                              @ 08028a9c 0b28
    bhi LAB_08028ac0                         @ 08028a9e 0fd8
    lsrs r0,r1,#0x7    @ 08028aa0 c809
    adds r1,r7,#0x0    @ 08028aa2 391c
    ldrb r6,[r6,#0x0]                        @ 08028aa4 3678
    ands r1,r6    @ 08028aa6 3140
    lsls r1,r1,#0x1    @ 08028aa8 4900
    orrs r1,r0    @ 08028aaa 0143
    movs r0,#0xd8    @ 08028aac d820
    subs r0,r0,r1    @ 08028aae 401a
    orrs r0,r5    @ 08028ab0 2843
    ldr r3, DWORD_08028b30                   @ 08028ab2 1f4b
    adds r2,r4,r3    @ 08028ab4 e218
    lsls r2,r2,#0x10    @ 08028ab6 1204
    lsrs r2,r2,#0x10    @ 08028ab8 120c
    .hword 0x4641    @ 08028aba 4146
    bl write_oam_entry_from_packed_args      @ 08028abc cdf056fb
LAB_08028ac0:
    ldr r6, DWORD_08028b34                   @ 08028ac0 1c4e
    adds r5,r6,#0x0    @ 08028ac2 351c
    adds r5,#0x37    @ 08028ac4 3735
    movs r0,#0x7c    @ 08028ac6 7c20
    ldrb r1,[r5,#0x0]                        @ 08028ac8 2978
    ands r0,r1    @ 08028aca 0840
    cmp r0,#0x0                              @ 08028acc 0028
    bne LAB_08028b48                         @ 08028ace 3bd1
    ldr r0, DWORD_08028b38                   @ 08028ad0 1948
    movs r4,#0x81    @ 08028ad2 8124
    lsls r4,r4,#0x7    @ 08028ad4 e401
    movs r2,#0x8c    @ 08028ad6 8c22
    lsls r2,r2,#0x1    @ 08028ad8 5200
    adds r1,r4,#0x0    @ 08028ada 211c
    bl write_oam_entry_from_packed_args      @ 08028adc cdf046fb
    ldr r0, DWORD_08028b3c                   @ 08028ae0 1648
    movs r2,#0x8e    @ 08028ae2 8e22
    lsls r2,r2,#0x1    @ 08028ae4 5200
    adds r1,r4,#0x0    @ 08028ae6 211c
    bl write_oam_entry_from_packed_args      @ 08028ae8 cdf040fb
    ldr r0, DWORD_08028b40                   @ 08028aec 1448
    movs r2,#0xe0    @ 08028aee e022
    lsls r2,r2,#0x1    @ 08028af0 5200
    adds r1,r4,#0x0    @ 08028af2 211c
    bl write_oam_entry_from_packed_args      @ 08028af4 cdf03afb
    ldr r0, DWORD_08028b44                   @ 08028af8 1248
    movs r2,#0xe2    @ 08028afa e222
    lsls r2,r2,#0x1    @ 08028afc 5200
    adds r1,r4,#0x0    @ 08028afe 211c
    bl write_oam_entry_from_packed_args      @ 08028b00 cdf034fb
    ldrb r5,[r5,#0x0]                        @ 08028b04 2d78
    lsrs r2,r5,#0x7    @ 08028b06 ea09
    adds r1,r6,#0x0    @ 08028b08 311c
    adds r1,#0x38    @ 08028b0a 3831
    movs r0,#0x7f    @ 08028b0c 7f20
    ldrb r1,[r1,#0x0]                        @ 08028b0e 0978
    ands r0,r1    @ 08028b10 0840
    lsls r0,r0,#0x1    @ 08028b12 4000
    orrs r0,r2    @ 08028b14 1043
    adds r0,#0x88    @ 08028b16 8830
    movs r1,#0x6e    @ 08028b18 6e21
    movs r2,#0x0    @ 08028b1a 0022
    movs r3,#0x1    @ 08028b1c 0123
    bl write_pack_grid_oam_by_card_slot      @ 08028b1e fff76dfe
    b LAB_08028ba0                           @ 08028b22 3de0
DWORD_08028b24:
    .word  0x09e59d88                     @ 08028b24 889de509
DWORD_08028b28:
    .word  gPrng                          @ 08028b28 40000003
DWORD_08028b2c:
    .word  0x00001006                     @ 08028b2c 06100000
DWORD_08028b30:
    .word  0x00001007                     @ 08028b30 07100000
DWORD_08028b34:
    .word  0x02023360                     @ 08028b34 60330202
DWORD_08028b38:
    .word  0x006e0024                     @ 08028b38 24006e00
DWORD_08028b3c:
    .word  0x006e0044                     @ 08028b3c 44006e00
DWORD_08028b40:
    .word  0x006e0094                     @ 08028b40 94006e00
DWORD_08028b44:
    .word  0x006e00b4                     @ 08028b44 b4006e00
LAB_08028b48:
    ldr r0, DWORD_08028bc8                   @ 08028b48 1f48
    movs r4,#0x81    @ 08028b4a 8124
    lsls r4,r4,#0x7    @ 08028b4c e401
    movs r2,#0xac    @ 08028b4e ac22
    lsls r2,r2,#0x1    @ 08028b50 5200
    adds r1,r4,#0x0    @ 08028b52 211c
    bl write_oam_entry_from_packed_args      @ 08028b54 cdf00afb
    ldr r0, DWORD_08028bcc                   @ 08028b58 1c48
    movs r2,#0xae    @ 08028b5a ae22
    lsls r2,r2,#0x1    @ 08028b5c 5200
    adds r1,r4,#0x0    @ 08028b5e 211c
    bl write_oam_entry_from_packed_args      @ 08028b60 cdf004fb
    ldr r0, DWORD_08028bd0                   @ 08028b64 1a48
    movs r2,#0xc0    @ 08028b66 c022
    lsls r2,r2,#0x1    @ 08028b68 5200
    adds r1,r4,#0x0    @ 08028b6a 211c
    bl write_oam_entry_from_packed_args      @ 08028b6c cdf0fefa
    ldr r0, DWORD_08028bd4                   @ 08028b70 1848
    movs r2,#0xc2    @ 08028b72 c222
    lsls r2,r2,#0x1    @ 08028b74 5200
    adds r1,r4,#0x0    @ 08028b76 211c
    bl write_oam_entry_from_packed_args      @ 08028b78 cdf0f8fa
    ldrb r1,[r5,#0x0]                        @ 08028b7c 2978
    lsrs r3,r1,#0x7    @ 08028b7e cb09
    adds r2,r6,#0x0    @ 08028b80 321c
    adds r2,#0x38    @ 08028b82 3832
    movs r0,#0x7f    @ 08028b84 7f20
    ldrb r2,[r2,#0x0]                        @ 08028b86 1278
    ands r0,r2    @ 08028b88 1040
    lsls r0,r0,#0x1    @ 08028b8a 4000
    orrs r0,r3    @ 08028b8c 1843
    adds r0,#0x88    @ 08028b8e 8830
    lsls r1,r1,#0x19    @ 08028b90 4906
    lsrs r1,r1,#0x1b    @ 08028b92 c90e
    lsls r2,r1,#0x2    @ 08028b94 8a00
    adds r2,r2,r1    @ 08028b96 5218
    movs r1,#0x6e    @ 08028b98 6e21
    movs r3,#0x0    @ 08028b9a 0023
    bl write_pack_grid_oam_by_card_slot      @ 08028b9c fff72efe
LAB_08028ba0:
    ldr r0, DWORD_08028bd8                   @ 08028ba0 0d48
    movs r1,#0xc0    @ 08028ba2 c021
    lsls r1,r1,#0x1    @ 08028ba4 4900
    ldrh r0,[r0,#0x36]                       @ 08028ba6 c08e
    ands r1,r0    @ 08028ba8 0140
    movs r0,#0x80    @ 08028baa 8020
    lsls r0,r0,#0x1    @ 08028bac 4000
    cmp r1,r0                                @ 08028bae 8142
    bne LAB_08028bba                         @ 08028bb0 03d1
    movs r0,#0x4c    @ 08028bb2 4c20
    movs r1,#0x8a    @ 08028bb4 8a21
    bl write_pack_strip_oam_entries          @ 08028bb6 fff7f7fd
LAB_08028bba:
    pop {r3,r4}                              @ 08028bba 18bc
    .hword 0x4698    @ 08028bbc 9846
    .hword 0x46a1    @ 08028bbe a146
    pop {r4,r5,r6,r7}                        @ 08028bc0 f0bc
    pop {r0}                                 @ 08028bc2 01bc
    bx r0                                    @ 08028bc4 0047
    .zero  0x2
DWORD_08028bc8:
    .word  0x006e0024                     @ 08028bc8 24006e00
DWORD_08028bcc:
    .word  0x006e0044                     @ 08028bcc 44006e00
DWORD_08028bd0:
    .word  0x006e0094                     @ 08028bd0 94006e00
DWORD_08028bd4:
    .word  0x006e00b4                     @ 08028bd4 b4006e00
DWORD_08028bd8:
    .word  0x02023360                     @ 08028bd8 60330202

@ Function: evaluate campaign current duel victory state, returning enum value 0-3. No APCS input (r0 overwritten by internal load at entry). First reads state_word at 0x0201e2a0+0x8a*4=0x0201e4a8; if equal to 8 checks sub_state at 0x0201e2a0+0x89*4=0x0201e4a4: 1->return 1 (player wins), 2->return 2 (opponent wins). Otherwise reads bit6 of byte at 0x02023360+0x36 (0x40 mask); if bit6 set loads 0x0201e2a0+0x89*4 and returns its value. If bit6 clear: reads gPrng+0x23f byte bits[7:1] as win_count, reads gPrng+0x240 byte bit0 as lock_bit; computes score = win_count * (lock_bit<<7 | win_count>>1) and checks sign to decide winner; further reads multiple challenge sub-states for combined judgment. Returns {0=draw/continue, 1=player_wins, 2=opp_wins, 3=undecided}.
@ 
@ Side effects: no external writes (pure state read).
@ 
@ Constants:
@ - CAMPAIGN_CTX_BASE = 0x0201e2a0 // campaign EWRAM context
@ - STATE_FIELD_OFFSET = 0x8a*4 = 0x228 // main state word
@ - SUB_STATE_OFFSET = 0x89*4 = 0x224
@ - PLAYER_STRUCT = 0x02023360
@ - FLAG_BIT6_OFFSET = 0x36 // player struct flags
@ - IWRAM_WIN_COUNT_OFFSET = 0x23f // gPrng+0x23f: win count byte
@ - IWRAM_LOCK_OFFSET = 0x240 // gPrng+0x240: lock bit byte
@ - CHALLENGE_OFFSET_A = 0x241 // gPrng+0x241
@ - STATE_VAL_MATCH = 8 // trigger for sub_state check
@ - RETURN_PLAYER_WIN = 1
@ - RETURN_OPP_WIN = 2
@ - RETURN_DRAW = 0
@ - RETURN_UNKNOWN = 3
evaluate_campaign_victory_state:
    push {r4,r5,r6,r7,lr}                    @ 08028bdc f0b5
    .hword 0x4647    @ 08028bde 4746
    push {r7}                                @ 08028be0 80b4
    movs r5,#0x0    @ 08028be2 0025
    ldr r1, DWORD_08028c24                   @ 08028be4 0f49
    movs r2,#0x8a    @ 08028be6 8a22
    lsls r2,r2,#0x2    @ 08028be8 9200
    adds r0,r1,r2    @ 08028bea 8818
    ldr r0,[r0,#0x0]                         @ 08028bec 0068
    .hword 0x468c    @ 08028bee 8c46
    cmp r0,#0x8                              @ 08028bf0 0828
    bne LAB_08028c08                         @ 08028bf2 09d1
    movs r0,#0x89    @ 08028bf4 8920
    lsls r0,r0,#0x2    @ 08028bf6 8000
    add r0,r12                               @ 08028bf8 6044
    ldr r0,[r0,#0x0]                         @ 08028bfa 0068
    cmp r0,#0x1                              @ 08028bfc 0128
    bne LAB_08028c02                         @ 08028bfe 00d1
    b LAB_08028d24                           @ 08028c00 90e0
LAB_08028c02:
    cmp r0,#0x2                              @ 08028c02 0228
    bne LAB_08028c08                         @ 08028c04 00d1
    b LAB_08028d2c                           @ 08028c06 91e0
LAB_08028c08:
    ldr r1, DWORD_08028c28                   @ 08028c08 0749
    adds r2,r1,#0x0    @ 08028c0a 0a1c
    adds r2,#0x36    @ 08028c0c 3632
    movs r0,#0x40    @ 08028c0e 4020
    ldrb r2,[r2,#0x0]                        @ 08028c10 1278
    ands r0,r2    @ 08028c12 1040
    .hword 0x4688    @ 08028c14 8846
    cmp r0,#0x0                              @ 08028c16 0028
    beq LAB_08028c2c                         @ 08028c18 08d0
    movs r0,#0x89    @ 08028c1a 8920
    lsls r0,r0,#0x2    @ 08028c1c 8000
    add r0,r12                               @ 08028c1e 6044
    ldr r0,[r0,#0x0]                         @ 08028c20 0068
    b LAB_08028d36                           @ 08028c22 88e0
DWORD_08028c24:
    .word  0x0201e2a0                     @ 08028c24 a0e20102
DWORD_08028c28:
    .word  0x02023360                     @ 08028c28 60330202
LAB_08028c2c:
    movs r4,#0x0    @ 08028c2c 0024
    ldr r2, DWORD_08028c64                   @ 08028c2e 0d4a
    ldr r1, DWORD_08028c68                   @ 08028c30 0d49
    adds r0,r2,r1    @ 08028c32 5018
    ldrb r0,[r0,#0x0]                        @ 08028c34 0078
    lsrs r3,r0,#0x1    @ 08028c36 4308
    movs r0,#0x90    @ 08028c38 9020
    lsls r0,r0,#0x2    @ 08028c3a 8000
    adds r1,r2,r0    @ 08028c3c 1118
    movs r0,#0x1    @ 08028c3e 0120
    ldrb r1,[r1,#0x0]                        @ 08028c40 0978
    ands r0,r1    @ 08028c42 0840
    lsls r0,r0,#0x7    @ 08028c44 c001
    orrs r0,r3    @ 08028c46 1843
    adds r0,#0x1    @ 08028c48 0130
    adds r7,r2,#0x0    @ 08028c4a 171c
    cmp r4,r0                                @ 08028c4c 8442
    bge LAB_08028c7c                         @ 08028c4e 15da
    ldr r1, DWORD_08028c6c                   @ 08028c50 0649
    adds r2,r7,r1    @ 08028c52 7a18
    adds r1,r0,#0x0    @ 08028c54 011c
LAB_08028c56:
    adds r0,r4,r2    @ 08028c56 a018
    ldrb r0,[r0,#0x0]                        @ 08028c58 0078
    cmp r0,#0x1                              @ 08028c5a 0128
    beq LAB_08028c70                         @ 08028c5c 08d0
    cmp r0,#0x2                              @ 08028c5e 0228
    beq LAB_08028c74                         @ 08028c60 08d0
    b LAB_08028c76                           @ 08028c62 08e0
DWORD_08028c64:
    .word  gPrng                          @ 08028c64 40000003
DWORD_08028c68:
    .word  0x0000023f                     @ 08028c68 3f020000
DWORD_08028c6c:
    .word  0x00000241                     @ 08028c6c 41020000
LAB_08028c70:
    adds r5,#0x1    @ 08028c70 0135
    b LAB_08028c76                           @ 08028c72 00e0
LAB_08028c74:
    subs r5,#0x1    @ 08028c74 013d
LAB_08028c76:
    adds r4,#0x1    @ 08028c76 0134
    cmp r4,r1                                @ 08028c78 8c42
    blt LAB_08028c56                         @ 08028c7a ecdb
LAB_08028c7c:
    adds r1,r7,#0x0    @ 08028c7c 391c
    ldr r2, DWORD_08028d0c                   @ 08028c7e 234a
    adds r0,r1,r2    @ 08028c80 8818
    ldrb r0,[r0,#0x0]                        @ 08028c82 0078
    lsrs r2,r0,#0x1    @ 08028c84 4208
    movs r0,#0x90    @ 08028c86 9020
    lsls r0,r0,#0x2    @ 08028c88 8000
    adds r1,r1,r0    @ 08028c8a 0918
    movs r0,#0x1    @ 08028c8c 0120
    ldrb r1,[r1,#0x0]                        @ 08028c8e 0978
    ands r0,r1    @ 08028c90 0840
    lsls r6,r0,#0x7    @ 08028c92 c601
    orrs r6,r2    @ 08028c94 1643
    muls r5,r6    @ 08028c96 7543
    cmp r5,#0x1                              @ 08028c98 012d
    bgt LAB_08028d24                         @ 08028c9a 43dc
    movs r0,#0x1    @ 08028c9c 0120
    rsbs r0,r0,#0    @ 08028c9e 4042
    cmp r5,r0                                @ 08028ca0 8542
    blt LAB_08028d2c                         @ 08028ca2 43db
    cmp r6,#0x1                              @ 08028ca4 012e
    bhi LAB_08028d34                         @ 08028ca6 45d8
    movs r0,#0x8a    @ 08028ca8 8a20
    lsls r0,r0,#0x2    @ 08028caa 8000
    add r0,r12                               @ 08028cac 6044
    ldr r0,[r0,#0x0]                         @ 08028cae 0068
    cmp r0,#0x9                              @ 08028cb0 0928
    beq LAB_08028cee                         @ 08028cb2 1cd0
    .hword 0x4640    @ 08028cb4 4046
    adds r0,#0x37    @ 08028cb6 3730
    ldrb r0,[r0,#0x0]                        @ 08028cb8 0078
    lsls r4,r0,#0x19    @ 08028cba 4406
    lsrs r0,r4,#0x1b    @ 08028cbc e00e
    lsls r1,r0,#0x2    @ 08028cbe 8100
    adds r1,r1,r0    @ 08028cc0 0918
    lsls r0,r1,#0x4    @ 08028cc2 0801
    subs r0,r0,r1    @ 08028cc4 401a
    lsls r0,r0,#0x2    @ 08028cc6 8000
    cmp r0,#0x0                              @ 08028cc8 0028
    beq LAB_08028d30                         @ 08028cca 31d0
    movs r1,#0x84    @ 08028ccc 8421
    lsls r1,r1,#0x2    @ 08028cce 8900
    adds r0,r7,r1    @ 08028cd0 7818
    ldr r0,[r0,#0x0]                         @ 08028cd2 0068
    lsls r0,r0,#0x1    @ 08028cd4 4000
    lsrs r0,r0,#0x1    @ 08028cd6 4008
    movs r1,#0x3c    @ 08028cd8 3c21
    bl __divsi3                              @ 08028cda e5f093fc
    lsrs r1,r4,#0x1b    @ 08028cde e10e
    lsls r2,r1,#0x2    @ 08028ce0 8a00
    adds r2,r2,r1    @ 08028ce2 5218
    lsls r1,r2,#0x4    @ 08028ce4 1101
    subs r1,r1,r2    @ 08028ce6 891a
    lsls r1,r1,#0x2    @ 08028ce8 8900
    cmp r0,r1                                @ 08028cea 8842
    blt LAB_08028d30                         @ 08028cec 20db
LAB_08028cee:
    movs r5,#0x0    @ 08028cee 0025
    movs r4,#0x0    @ 08028cf0 0024
    adds r0,r6,#0x1    @ 08028cf2 701c
    cmp r5,r0                                @ 08028cf4 8542
    bge LAB_08028d20                         @ 08028cf6 13da
    ldr r2, DWORD_08028d10                   @ 08028cf8 054a
    adds r1,r7,r2    @ 08028cfa b918
    adds r3,r0,#0x0    @ 08028cfc 031c
LAB_08028cfe:
    adds r0,r4,r1    @ 08028cfe 6018
    ldrb r0,[r0,#0x0]                        @ 08028d00 0078
    cmp r0,#0x1                              @ 08028d02 0128
    beq LAB_08028d14                         @ 08028d04 06d0
    cmp r0,#0x2                              @ 08028d06 0228
    beq LAB_08028d18                         @ 08028d08 06d0
    b LAB_08028d1a                           @ 08028d0a 06e0
DWORD_08028d0c:
    .word  0x0000023f                     @ 08028d0c 3f020000
DWORD_08028d10:
    .word  0x00000241                     @ 08028d10 41020000
LAB_08028d14:
    adds r5,#0x1    @ 08028d14 0135
    b LAB_08028d1a                           @ 08028d16 00e0
LAB_08028d18:
    subs r5,#0x1    @ 08028d18 013d
LAB_08028d1a:
    adds r4,#0x1    @ 08028d1a 0134
    cmp r4,r3                                @ 08028d1c 9c42
    blt LAB_08028cfe                         @ 08028d1e eedb
LAB_08028d20:
    cmp r5,#0x0                              @ 08028d20 002d
    ble LAB_08028d28                         @ 08028d22 01dd
LAB_08028d24:
    movs r0,#0x1    @ 08028d24 0120
    b LAB_08028d36                           @ 08028d26 06e0
LAB_08028d28:
    cmp r5,#0x0                              @ 08028d28 002d
    bge LAB_08028d34                         @ 08028d2a 03da
LAB_08028d2c:
    movs r0,#0x2    @ 08028d2c 0220
    b LAB_08028d36                           @ 08028d2e 02e0
LAB_08028d30:
    movs r0,#0x0    @ 08028d30 0020
    b LAB_08028d36                           @ 08028d32 00e0
LAB_08028d34:
    movs r0,#0x3    @ 08028d34 0320
LAB_08028d36:
    pop {r3}                                 @ 08028d36 08bc
    .hword 0x4698    @ 08028d38 9846
    pop {r4,r5,r6,r7}                        @ 08028d3a f0bc
    pop {r1}                                 @ 08028d3c 02bc
    bx r1                                    @ 08028d3e 0847

@ Campaign scene main dispatcher by PRNG state. Reads gPrng+0x202 halfword, extracts bits[13:6] (lsls#0x12; lsrs#0x18 => 8-bit index [0..0xfd]); if index>0xfd calls load_campaign_state_post_sio to correct. Uses index to look up 256-entry function pointer table @ DAT_08028d78, loads target address, tail-calls via bx r7. Return value is the dispatched case handler's return value (tail-call passthrough). Function pointer 0x08028d41 referenced at 0x080e7a88 (Sub-type B).
@ 
@ Constants:
@ - INDEX_OFFSET = 0x202
@ - INDEX_BITS = bits[13:6]
@ - INDEX_RANGE = [0..0xfd]
@ - DISPATCH_TABLE = 0x08028d78
dispatch_campaign_scene_by_prng_state:
    push {r4,r5,r6,r7,lr}                    @ 08028d40 f0b5
    .hword 0x4657    @ 08028d42 5746
    .hword 0x464e    @ 08028d44 4e46
    .hword 0x4645    @ 08028d46 4546
    push {r5,r6,r7}                          @ 08028d48 e0b4
    sub sp,#0x50                             @ 08028d4a 94b0
    ldr r0, PTR_gPrng_08028d6c               @ 08028d4c 0748
    ldr r2, DAT_08028d70                     @ 08028d4e 084a
    adds r1,r0,r2    @ 08028d50 8118
    ldrh r1,[r1,#0x0]                        @ 08028d52 0988
    lsls r1,r1,#0x12    @ 08028d54 8904
    lsrs r1,r1,#0x18    @ 08028d56 090e
    .hword 0x4680    @ 08028d58 8046
    cmp r1,#0xfd                             @ 08028d5a fd29
    bls LAB_08028d62                         @ 08028d5c 01d9
    bl load_campaign_state_post_sio          @ 08028d5e 02f07ffb
LAB_08028d62:
    lsls r0,r1,#0x2    @ 08028d62 8800
    ldr r1, DAT_08028d74                     @ 08028d64 0349
    adds r0,r0,r1    @ 08028d66 4018
    ldr r0,[r0,#0x0]                         @ 08028d68 0068
    .hword 0x4687    @ 08028d6a 8746
PTR_gPrng_08028d6c:
    .word  gPrng                          @ 08028d6c 40000003
DAT_08028d70:
    .word  0x00000202                     @ 08028d70 02020000
DAT_08028d74:
    .word  0x08028d78                     @ 08028d74 788d0208
PTR_DAT_08028d78:
    .word  0x08029170                     @ 08028d78 70910208
    .word  0x080292b4                     @ 08028d7c b4920208
    .word  0x08029304                     @ 08028d80 04930208
    .word  0x08029398                     @ 08028d84 98930208
    .word  0x080294bc                     @ 08028d88 bc940208
    .word  0x0802952c                     @ 08028d8c 2c950208
    .word  0x080294bc                     @ 08028d90 bc940208
    .word  0x0802957c                     @ 08028d94 7c950208
    .word  0x080294bc                     @ 08028d98 bc940208
    .word  0x0802b460                     @ 08028d9c 60b40208
    .word  0x080295cc                     @ 08028da0 cc950208
    .word  0x080292b4                     @ 08028da4 b4920208
    .word  0x08029bf0                     @ 08028da8 f09b0208
    .word  0x0802b460                     @ 08028dac 60b40208
    .word  0x0802b460                     @ 08028db0 60b40208
    .word  0x0802b460                     @ 08028db4 60b40208
    .word  0x0802b460                     @ 08028db8 60b40208
    .word  0x0802b460                     @ 08028dbc 60b40208
    .word  0x0802b460                     @ 08028dc0 60b40208
    .word  0x0802b460                     @ 08028dc4 60b40208
    .word  0x08029e38                     @ 08028dc8 389e0208
    .word  0x08029fac                     @ 08028dcc ac9f0208
    .word  0x0802a00c                     @ 08028dd0 0ca00208
    .word  0x0802a1cc                     @ 08028dd4 cca10208
    .word  0x0802a3e4                     @ 08028dd8 e4a30208
    .word  0x0802a3e4                     @ 08028ddc e4a30208
    .word  0x0802a43c                     @ 08028de0 3ca40208
    .word  0x0802a4c8                     @ 08028de4 c8a40208
    .word  0x0802b460                     @ 08028de8 60b40208
    .word  0x0802b460                     @ 08028dec 60b40208
    .word  0x0802a4f4                     @ 08028df0 f4a40208
    .word  0x0802a57c                     @ 08028df4 7ca50208
    .word  0x0802a5b4                     @ 08028df8 b4a50208
    .word  0x0802a640                     @ 08028dfc 40a60208
    .word  0x0802b460                     @ 08028e00 60b40208
    .word  0x0802b460                     @ 08028e04 60b40208
    .word  0x0802b460                     @ 08028e08 60b40208
    .word  0x0802b460                     @ 08028e0c 60b40208
    .word  0x0802b460                     @ 08028e10 60b40208
    .word  0x0802b460                     @ 08028e14 60b40208
    .word  0x0802b460                     @ 08028e18 60b40208
    .word  0x0802b460                     @ 08028e1c 60b40208
    .word  0x0802b460                     @ 08028e20 60b40208
    .word  0x0802b460                     @ 08028e24 60b40208
    .word  0x0802b460                     @ 08028e28 60b40208
    .word  0x0802b460                     @ 08028e2c 60b40208
    .word  0x0802b460                     @ 08028e30 60b40208
    .word  0x0802b460                     @ 08028e34 60b40208
    .word  0x0802b460                     @ 08028e38 60b40208
    .word  0x0802b460                     @ 08028e3c 60b40208
    .word  0x0802a784                     @ 08028e40 84a70208
    .word  0x0802a83c                     @ 08028e44 3ca80208
    .word  0x0802a89c                     @ 08028e48 9ca80208
    .word  0x0802a9f8                     @ 08028e4c f8a90208
    .word  0x0802aa64                     @ 08028e50 64aa0208
    .word  0x08029398                     @ 08028e54 98930208
    .word  0x080294bc                     @ 08028e58 bc940208
    .word  0x0802952c                     @ 08028e5c 2c950208
    .word  0x080294bc                     @ 08028e60 bc940208
    .word  0x0802957c                     @ 08028e64 7c950208
    .word  0x080294bc                     @ 08028e68 bc940208
    .word  0x0802b460                     @ 08028e6c 60b40208
    .word  0x0802b460                     @ 08028e70 60b40208
    .word  0x0802b460                     @ 08028e74 60b40208
    .word  0x0802b460                     @ 08028e78 60b40208
    .word  0x0802b460                     @ 08028e7c 60b40208
    .word  0x0802b460                     @ 08028e80 60b40208
    .word  0x0802b460                     @ 08028e84 60b40208
    .word  0x0802b460                     @ 08028e88 60b40208
    .word  0x0802b460                     @ 08028e8c 60b40208
    .word  0x0802aac4                     @ 08028e90 c4aa0208
    .word  0x08029fac                     @ 08028e94 ac9f0208
    .word  0x0802ac54                     @ 08028e98 54ac0208
    .word  0x0802b460                     @ 08028e9c 60b40208
    .word  0x0802b460                     @ 08028ea0 60b40208
    .word  0x0802b460                     @ 08028ea4 60b40208
    .word  0x0802b460                     @ 08028ea8 60b40208
    .word  0x0802b460                     @ 08028eac 60b40208
    .word  0x0802b460                     @ 08028eb0 60b40208
    .word  0x0802b460                     @ 08028eb4 60b40208
    .word  0x0802b460                     @ 08028eb8 60b40208
    .word  0x0802b460                     @ 08028ebc 60b40208
    .word  0x0802b460                     @ 08028ec0 60b40208
    .word  0x0802b460                     @ 08028ec4 60b40208
    .word  0x0802b460                     @ 08028ec8 60b40208
    .word  0x0802b460                     @ 08028ecc 60b40208
    .word  0x0802b460                     @ 08028ed0 60b40208
    .word  0x0802b460                     @ 08028ed4 60b40208
    .word  0x0802b460                     @ 08028ed8 60b40208
    .word  0x0802b460                     @ 08028edc 60b40208
    .word  0x0802b460                     @ 08028ee0 60b40208
    .word  0x0802b460                     @ 08028ee4 60b40208
    .word  0x0802b460                     @ 08028ee8 60b40208
    .word  0x0802b460                     @ 08028eec 60b40208
    .word  0x0802b460                     @ 08028ef0 60b40208
    .word  0x0802b460                     @ 08028ef4 60b40208
    .word  0x0802b460                     @ 08028ef8 60b40208
    .word  0x0802b460                     @ 08028efc 60b40208
    .word  0x0802b460                     @ 08028f00 60b40208
    .word  0x0802b460                     @ 08028f04 60b40208
    .word  0x0802ae40                     @ 08028f08 40ae0208
    .word  0x0802aeac                     @ 08028f0c acae0208
    .word  0x0802b148                     @ 08028f10 48b10208
    .word  0x0802b1a0                     @ 08028f14 a0b10208
    .word  0x0802b1d8                     @ 08028f18 d8b10208
    .word  0x0802b460                     @ 08028f1c 60b40208
    .word  0x0802b460                     @ 08028f20 60b40208
    .word  0x0802b460                     @ 08028f24 60b40208
    .word  0x0802b460                     @ 08028f28 60b40208
    .word  0x0802b460                     @ 08028f2c 60b40208
    .word  0x0802b460                     @ 08028f30 60b40208
    .word  0x0802b460                     @ 08028f34 60b40208
    .word  0x0802b460                     @ 08028f38 60b40208
    .word  0x0802b460                     @ 08028f3c 60b40208
    .word  0x0802b460                     @ 08028f40 60b40208
    .word  0x0802b460                     @ 08028f44 60b40208
    .word  0x0802b460                     @ 08028f48 60b40208
    .word  0x0802b460                     @ 08028f4c 60b40208
    .word  0x0802b460                     @ 08028f50 60b40208
    .word  0x0802b460                     @ 08028f54 60b40208
    .word  0x0802b460                     @ 08028f58 60b40208
    .word  0x0802b460                     @ 08028f5c 60b40208
    .word  0x0802b460                     @ 08028f60 60b40208
    .word  0x0802b460                     @ 08028f64 60b40208
    .word  0x0802b460                     @ 08028f68 60b40208
    .word  0x0802b460                     @ 08028f6c 60b40208
    .word  0x0802b460                     @ 08028f70 60b40208
    .word  0x0802b460                     @ 08028f74 60b40208
    .word  0x0802b460                     @ 08028f78 60b40208
    .word  0x0802b460                     @ 08028f7c 60b40208
    .word  0x0802b460                     @ 08028f80 60b40208
    .word  0x0802b460                     @ 08028f84 60b40208
    .word  0x0802b460                     @ 08028f88 60b40208
    .word  0x0802b460                     @ 08028f8c 60b40208
    .word  0x0802b460                     @ 08028f90 60b40208
    .word  0x0802b460                     @ 08028f94 60b40208
    .word  0x0802b460                     @ 08028f98 60b40208
    .word  0x0802b460                     @ 08028f9c 60b40208
    .word  0x0802b460                     @ 08028fa0 60b40208
    .word  0x0802b460                     @ 08028fa4 60b40208
    .word  0x0802b460                     @ 08028fa8 60b40208
    .word  0x0802b460                     @ 08028fac 60b40208
    .word  0x0802b460                     @ 08028fb0 60b40208
    .word  0x0802b460                     @ 08028fb4 60b40208
    .word  0x0802b460                     @ 08028fb8 60b40208
    .word  0x0802b460                     @ 08028fbc 60b40208
    .word  0x0802b460                     @ 08028fc0 60b40208
    .word  0x0802b460                     @ 08028fc4 60b40208
    .word  0x0802b460                     @ 08028fc8 60b40208
    .word  0x0802b460                     @ 08028fcc 60b40208
    .word  0x0802b460                     @ 08028fd0 60b40208
    .word  0x0802b460                     @ 08028fd4 60b40208
    .word  0x0802b460                     @ 08028fd8 60b40208
    .word  0x0802b460                     @ 08028fdc 60b40208
    .word  0x0802b460                     @ 08028fe0 60b40208
    .word  0x0802b460                     @ 08028fe4 60b40208
    .word  0x0802b460                     @ 08028fe8 60b40208
    .word  0x0802b460                     @ 08028fec 60b40208
    .word  0x0802b460                     @ 08028ff0 60b40208
    .word  0x0802b460                     @ 08028ff4 60b40208
    .word  0x0802b460                     @ 08028ff8 60b40208
    .word  0x0802b460                     @ 08028ffc 60b40208
    .word  0x0802b460                     @ 08029000 60b40208
    .word  0x0802b460                     @ 08029004 60b40208
    .word  0x0802b460                     @ 08029008 60b40208
    .word  0x0802b460                     @ 0802900c 60b40208
    .word  0x0802b460                     @ 08029010 60b40208
    .word  0x0802b460                     @ 08029014 60b40208
    .word  0x0802b460                     @ 08029018 60b40208
    .word  0x0802b460                     @ 0802901c 60b40208
    .word  0x0802b460                     @ 08029020 60b40208
    .word  0x0802b460                     @ 08029024 60b40208
    .word  0x0802b460                     @ 08029028 60b40208
    .word  0x0802b460                     @ 0802902c 60b40208
    .word  0x0802b460                     @ 08029030 60b40208
    .word  0x0802b460                     @ 08029034 60b40208
    .word  0x0802b460                     @ 08029038 60b40208
    .word  0x0802b460                     @ 0802903c 60b40208
    .word  0x0802b460                     @ 08029040 60b40208
    .word  0x0802b460                     @ 08029044 60b40208
    .word  0x0802b460                     @ 08029048 60b40208
    .word  0x0802b460                     @ 0802904c 60b40208
    .word  0x0802b460                     @ 08029050 60b40208
    .word  0x0802b460                     @ 08029054 60b40208
    .word  0x0802b460                     @ 08029058 60b40208
    .word  0x0802b460                     @ 0802905c 60b40208
    .word  0x0802b460                     @ 08029060 60b40208
    .word  0x0802b460                     @ 08029064 60b40208
    .word  0x0802b460                     @ 08029068 60b40208
    .word  0x0802b460                     @ 0802906c 60b40208
    .word  0x0802b460                     @ 08029070 60b40208
    .word  0x0802b460                     @ 08029074 60b40208
    .word  0x0802b460                     @ 08029078 60b40208
    .word  0x0802b460                     @ 0802907c 60b40208
    .word  0x0802b460                     @ 08029080 60b40208
    .word  0x0802b460                     @ 08029084 60b40208
    .word  0x0802b460                     @ 08029088 60b40208
    .word  0x0802b460                     @ 0802908c 60b40208
    .word  0x0802b460                     @ 08029090 60b40208
    .word  0x0802b460                     @ 08029094 60b40208
    .word  0x0802b460                     @ 08029098 60b40208
    .word  0x0802b460                     @ 0802909c 60b40208
    .word  0x0802b460                     @ 080290a0 60b40208
    .word  0x0802b460                     @ 080290a4 60b40208
    .word  0x0802b460                     @ 080290a8 60b40208
    .word  0x0802b460                     @ 080290ac 60b40208
    .word  0x0802b460                     @ 080290b0 60b40208
    .word  0x0802b460                     @ 080290b4 60b40208
    .word  0x0802b460                     @ 080290b8 60b40208
    .word  0x0802b460                     @ 080290bc 60b40208
    .word  0x0802b460                     @ 080290c0 60b40208
    .word  0x0802b460                     @ 080290c4 60b40208
    .word  0x0802b460                     @ 080290c8 60b40208
    .word  0x0802b460                     @ 080290cc 60b40208
    .word  0x0802b460                     @ 080290d0 60b40208
    .word  0x0802b460                     @ 080290d4 60b40208
    .word  0x0802b460                     @ 080290d8 60b40208
    .word  0x0802b460                     @ 080290dc 60b40208
    .word  0x0802b460                     @ 080290e0 60b40208
    .word  0x0802b460                     @ 080290e4 60b40208
    .word  0x0802b460                     @ 080290e8 60b40208
    .word  0x0802b460                     @ 080290ec 60b40208
    .word  0x0802b460                     @ 080290f0 60b40208
    .word  0x0802b460                     @ 080290f4 60b40208
    .word  0x0802b460                     @ 080290f8 60b40208
    .word  0x0802b460                     @ 080290fc 60b40208
    .word  0x0802b460                     @ 08029100 60b40208
    .word  0x0802b460                     @ 08029104 60b40208
    .word  0x0802b460                     @ 08029108 60b40208
    .word  0x0802b460                     @ 0802910c 60b40208
    .word  0x0802b460                     @ 08029110 60b40208
    .word  0x0802b460                     @ 08029114 60b40208
    .word  0x0802b460                     @ 08029118 60b40208
    .word  0x0802b460                     @ 0802911c 60b40208
    .word  0x0802b460                     @ 08029120 60b40208
    .word  0x0802b460                     @ 08029124 60b40208
    .word  0x0802b460                     @ 08029128 60b40208
    .word  0x0802b460                     @ 0802912c 60b40208
    .word  0x0802b460                     @ 08029130 60b40208
    .word  0x0802b460                     @ 08029134 60b40208
    .word  0x0802b460                     @ 08029138 60b40208
    .word  0x0802b460                     @ 0802913c 60b40208
    .word  0x0802b460                     @ 08029140 60b40208
    .word  0x0802b460                     @ 08029144 60b40208
    .word  0x0802b460                     @ 08029148 60b40208
    .word  0x0802b460                     @ 0802914c 60b40208
    .word  0x0802b460                     @ 08029150 60b40208
    .word  0x0802b460                     @ 08029154 60b40208
    .word  0x0802b460                     @ 08029158 60b40208
    .word  0x0802b460                     @ 0802915c 60b40208
    .word  0x0802b220                     @ 08029160 20b20208
    .word  0x080292b4                     @ 08029164 b4920208
    .word  0x0802b3a4                     @ 08029168 a4b30208
    .word  0x0802b434                     @ 0802916c 34b40208
DAT_08029170:
    ROM_INCBIN 0x29170, 0x22f0

@ SIO link session teardown epilogue fragment that reads campaign state word. Calls teardown_sio_link_session to disconnect SIO; then loads 0x0201e2a0+0x89*4=0x0201e4c4 (campaign state word address) into r0; exits via pop {r1}; bx r1 (Sub-case E) -- r0 holds the loaded state value returned to parent function. Large dispatch table at 0x08029098 (26+ entries all pointing here) indicates all "SIO terminate" state paths share this implementation.
@ 
@ Params: r0=(none -- inline exit fragment; no APCS input; r0 set by ldr at 0x0802b464)
@ Returns: r0=u32 campaign_state_word (value at 0x0201e4c4; Sub-case E: pop {r1}; bx r1)
@ Side effects: via teardown_sio_link_session: SIO hardware and EWRAM SIO state cleared
@ Constants: CAMPAIGN_STATE_BASE=0x0201e2a0; CAMPAIGN_STATE_OFF=0x89<<2=0x224; CAMPAIGN_STATE_ADDR=0x0201e4c4
load_campaign_state_post_sio:
    bl teardown_sio_link_session             @ 0802b460 c2f0e2fc
    ldr r0, DAT_0802b480                     @ 0802b464 0648
    movs r7,#0x89    @ 0802b466 8927
    lsls r7,r7,#0x2    @ 0802b468 bf00
    adds r0,r0,r7    @ 0802b46a c019
    ldr r0,[r0,#0x0]                         @ 0802b46c 0068
    add sp,#0x50                             @ 0802b46e 14b0
    pop {r3,r4,r5}                           @ 0802b470 38bc
    .hword 0x4698    @ 0802b472 9846
    .hword 0x46a1    @ 0802b474 a146
    .hword 0x46aa    @ 0802b476 aa46
    pop {r4,r5,r6,r7}                        @ 0802b478 f0bc
    pop {r1}                                 @ 0802b47a 02bc
    bx r1                                    @ 0802b47c 0847
    .zero  0x2
DAT_0802b480:
    .word  0x0201e2a0                     @ 0802b480 a0e20102

@ Core function to render card name centered to sprite VRAM, called by FUN_0801fec0 (duel_puzzle main loop) and init_pack_card_info_screen_vram (0x0802b590). Accepts r0=card_name_ptr (card name C string). Inits line buffer (col=0xc, font=2), reads [0x02000000+0x6c2c] font_style bits[2:0], updates [0x02006ed0+0x8] render mode byte (bit1 by font_style, bit1 forced=1), looks up font_jp_base_table for font pointer. Computes name byte length len; if len*3 > 0x30 selects narrow font (font_style bit0=0, clears bit0, relooks up table). Center offset = (0x30 - len*3) / 2, calls text_render_wrapper twice (normal + shadow, row=2 both). Computes length again, center offset = (0x30 - len*3) >> 1. Finally calls commit_line_buffer_to_sprite_vram(0x060053c0, 0) to write line buffer to OBJ VRAM. Then loops to write tilemap indices (2 rows x 12 cols = 24 tiles) to 0x06000812 region.
@ 
@ Constants:
@ - line_buf_ctx = 0x02006ed0
@ - font table = font_jp_base_table
@ - setup params: col=0xc, font=2
@ - name width budget = 0x30 (48 pixels)
@ - len*3 formula: lsls r1,r0,#1; adds r1,r1,r0 (len*2+len=len*3)
@ - narrow font threshold = 0x30 (if len*3 > 48 use narrow)
@ - centered x = (0x30 - len*3) >> 1
@ - OBJ VRAM commit target = 0x060053c0
@ - tilemap area = 0x06000812; 2 rows x 12 cols
@ - tile id start = 0x009e
render_card_name_centered_to_sprite_vram:
    push {r4,r5,r6,r7,lr}                    @ 0802b484 f0b5
    .hword 0x464f    @ 0802b486 4f46
    .hword 0x4646    @ 0802b488 4646
    push {r6,r7}                             @ 0802b48a c0b4
    adds r4,r0,#0x0    @ 0802b48c 041c
    .hword 0x4689    @ 0802b48e 8946
    .hword 0x4690    @ 0802b490 9046
    movs r0,#0xc    @ 0802b492 0c20
    movs r1,#0x2    @ 0802b494 0221
    bl setup_line_buf_pos_and_font           @ 0802b496 c5f08dfb
    ldr r5, DAT_0802b578                     @ 0802b49a 374d
    ldr r0, DAT_0802b57c                     @ 0802b49c 3748
    ldr r1, DAT_0802b580                     @ 0802b49e 3849
    adds r0,r0,r1    @ 0802b4a0 4018
    movs r1,#0x7    @ 0802b4a2 0721
    ldrb r0,[r0,#0x0]                        @ 0802b4a4 0078
    ands r1,r0    @ 0802b4a6 0140
    rsbs r1,r1,#0    @ 0802b4a8 4942
    lsrs r1,r1,#0x1f    @ 0802b4aa c90f
    movs r0,#0x2    @ 0802b4ac 0220
    rsbs r0,r0,#0    @ 0802b4ae 4042
    ldrb r2,[r5,#0x8]                        @ 0802b4b0 2a7a
    ands r0,r2    @ 0802b4b2 1040
    orrs r0,r1    @ 0802b4b4 0843
    movs r1,#0x2    @ 0802b4b6 0221
    orrs r0,r1    @ 0802b4b8 0843
    strb r0,[r5,#0x8]                        @ 0802b4ba 2872
    ldr r7, PTR_font_jp_base_table_0802b584  @ 0802b4bc 314f
    lsls r1,r0,#0x1e    @ 0802b4be 8107
    lsrs r1,r1,#0x1f    @ 0802b4c0 c90f
    lsls r1,r1,#0x2    @ 0802b4c2 8900
    lsls r0,r0,#0x1f    @ 0802b4c4 c007
    lsrs r0,r0,#0x1f    @ 0802b4c6 c00f
    lsls r0,r0,#0x3    @ 0802b4c8 c000
    adds r1,r1,r0    @ 0802b4ca 0918
    adds r1,r1,r7    @ 0802b4cc c919
    ldr r0,[r1,#0x0]                         @ 0802b4ce 0868
    str r0,[r5,#0x4]                         @ 0802b4d0 6860
    adds r0,r4,#0x0    @ 0802b4d2 201c
    bl count_bytes_until_null                @ 0802b4d4 caf004f8
    lsls r1,r0,#0x1    @ 0802b4d8 4100
    adds r1,r1,r0    @ 0802b4da 0918
    movs r6,#0x30    @ 0802b4dc 3026
    subs r1,r6,r1    @ 0802b4de 711a
    cmp r1,#0x0                              @ 0802b4e0 0029
    bge LAB_0802b4fa                         @ 0802b4e2 0ada
    movs r0,#0x3    @ 0802b4e4 0320
    rsbs r0,r0,#0    @ 0802b4e6 4042
    ldrb r3,[r5,#0x8]                        @ 0802b4e8 2b7a
    ands r0,r3    @ 0802b4ea 1840
    strb r0,[r5,#0x8]                        @ 0802b4ec 2872
    lsls r0,r0,#0x1f    @ 0802b4ee c007
    lsrs r0,r0,#0x1f    @ 0802b4f0 c00f
    lsls r0,r0,#0x3    @ 0802b4f2 c000
    adds r0,r0,r7    @ 0802b4f4 c019
    ldr r0,[r0,#0x0]                         @ 0802b4f6 0068
    str r0,[r5,#0x4]                         @ 0802b4f8 6860
LAB_0802b4fa:
    adds r0,r4,#0x0    @ 0802b4fa 201c
    bl count_bytes_until_null                @ 0802b4fc c9f0f0ff
    adds r1,r0,#0x0    @ 0802b500 011c
    lsls r0,r1,#0x1    @ 0802b502 4800
    adds r0,r0,r1    @ 0802b504 4018
    subs r0,r6,r0    @ 0802b506 301a
    .hword 0x4641    @ 0802b508 4146
    lsls r2,r1,#0x18    @ 0802b50a 0a06
    lsrs r2,r2,#0x18    @ 0802b50c 120e
    movs r3,#0x80    @ 0802b50e 8023
    lsls r3,r3,#0x8    @ 0802b510 1b02
    adds r1,r3,#0x0    @ 0802b512 191c
    orrs r2,r1    @ 0802b514 0a43
    movs r1,#0x2    @ 0802b516 0221
    adds r3,r4,#0x0    @ 0802b518 231c
    bl text_render_wrapper                   @ 0802b51a c7f0affa
    adds r0,r4,#0x0    @ 0802b51e 201c
    bl count_bytes_until_null                @ 0802b520 c9f0deff
    adds r1,r0,#0x0    @ 0802b524 011c
    lsls r0,r1,#0x1    @ 0802b526 4800
    adds r0,r0,r1    @ 0802b528 4018
    subs r0,r6,r0    @ 0802b52a 301a
    .hword 0x4649    @ 0802b52c 4946
    lsls r2,r1,#0x10    @ 0802b52e 0a04
    lsrs r2,r2,#0x10    @ 0802b530 120c
    movs r1,#0x2    @ 0802b532 0221
    adds r3,r4,#0x0    @ 0802b534 231c
    bl text_render_wrapper                   @ 0802b536 c7f0a1fa
    ldr r0, DAT_0802b588                     @ 0802b53a 1348
    movs r1,#0x0    @ 0802b53c 0021
    bl commit_line_buffer_to_sprite_vram     @ 0802b53e c7f085fc
    movs r3,#0x9e    @ 0802b542 9e23
    movs r2,#0x0    @ 0802b544 0022
LAB_0802b546:
    adds r0,r2,#0x0    @ 0802b546 101c
    adds r0,#0x12    @ 0802b548 1230
    lsls r0,r0,#0x10    @ 0802b54a 0004
    lsrs r0,r0,#0xa    @ 0802b54c 800a
    ldr r4, DAT_0802b58c                     @ 0802b54e 0f4c
    adds r1,r0,r4    @ 0802b550 0119
    adds r4,r2,#0x1    @ 0802b552 541c
    movs r2,#0xb    @ 0802b554 0b22
LAB_0802b556:
    strh r3,[r1,#0x0]                        @ 0802b556 0b80
    adds r1,#0x2    @ 0802b558 0231
    adds r0,r3,#0x1    @ 0802b55a 581c
    lsls r0,r0,#0x10    @ 0802b55c 0004
    lsrs r3,r0,#0x10    @ 0802b55e 030c
    subs r2,#0x1    @ 0802b560 013a
    cmp r2,#0x0                              @ 0802b562 002a
    bge LAB_0802b556                         @ 0802b564 f7da
    adds r2,r4,#0x0    @ 0802b566 221c
    cmp r2,#0x1                              @ 0802b568 012a
    ble LAB_0802b546                         @ 0802b56a ecdd
    pop {r3,r4}                              @ 0802b56c 18bc
    .hword 0x4698    @ 0802b56e 9846
    .hword 0x46a1    @ 0802b570 a146
    pop {r4,r5,r6,r7}                        @ 0802b572 f0bc
    pop {r0}                                 @ 0802b574 01bc
    bx r0                                    @ 0802b576 0047
DAT_0802b578:
    .word  0x02006ed0                     @ 0802b578 d06e0002
DAT_0802b57c:
    .word  0x02000000                     @ 0802b57c 00000002
DAT_0802b580:
    .word  0x00006c2c                     @ 0802b580 2c6c0000
PTR_font_jp_base_table_0802b584:
    .word  font_jp_base_table             @ 0802b584 54f8e509
DAT_0802b588:
    .word  0x060053c0                     @ 0802b588 c0530006
DAT_0802b58c:
    .word  0x06000812                     @ 0802b58c 12080006

@ Pack buy/card info screen complete VRAM init + card name text render function, called by FUN_0801fec0 (duel_puzzle main loop) and run_campaign_step30_pack_card_info_display (0x080277a4). Accepts r0=card_name_ptr, r1=pack_index [0..N]. Flow: writes DISPCNT shadow (gPrng+0x174 = 0x0401), writes DISPCNT register (0x04000000 = 0), calls reset_display_and_obj_vram, store_ewram_ctx_ptr_and_clear_mode_flags, writes BG0-BG3 control regs, reset_all_bg_scroll_regs_and_shadows, upload_pack_vram_and_palette; zero_fills three BG/OBJ tile regions; copies palette and pack tile data; calls load_pack_tile_and_map_to_vram three times (pack cover/title/background tile+map layers); inits line buffer (col=0x1e, font=2); computes name length to select font (long > 0xef bytes use narrow); two text_render_wrapper calls to render name; commit_line_buffer_to_sprite_vram; writes tilemap index row.
@ 
@ Constants:
@ - DISPCNT shadow = gPrng+0x174; value = 0x0401 (BG0+OBJ on)
@ - BG0CNT=0x0005, BG1CNT=0x0104, BG2CNT=0x820a, BG3CNT=0x0407
@ - OBJ VRAM = 0x06004000, size = 0xc000 bytes (zero_fill)
@ - BG tile = 0x06010000, size = 0x8000 bytes (zero_fill)
@ - pack palette src = 0x05000220 (0x20 halfwords)
@ - pack tile data src = 0x09b8fb8c (0x2000 bytes)
@ - load_pack_tile_and_map_to_vram: 3 calls for 3 pack graphic layers
@ - line_buf setup: col=0x1e, font=2
@ - long name threshold = 0xef (239 bytes; len*4 comparison)
@ - commit target = 0x060053c0, tilemap area = 0x06000812
init_pack_card_info_screen_vram:
    push {r4,r5,r6,r7,lr}                    @ 0802b590 f0b5
    adds r5,r0,#0x0    @ 0802b592 051c
    adds r7,r1,#0x0    @ 0802b594 0f1c
    ldr r0, PTR_gPrng_0802b6c8               @ 0802b596 4c48
    movs r1,#0xba    @ 0802b598 ba21
    lsls r1,r1,#0x1    @ 0802b59a 4900
    adds r0,r0,r1    @ 0802b59c 4018
    movs r2,#0x0    @ 0802b59e 0022
    ldr r1, DAT_0802b6cc                     @ 0802b5a0 4a49
    strh r1,[r0,#0x0]                        @ 0802b5a2 0180
    movs r0,#0x80    @ 0802b5a4 8020
    lsls r0,r0,#0x13    @ 0802b5a6 c004
    strh r2,[r0,#0x0]                        @ 0802b5a8 0280
    ldr r0, DAT_0802b6d0                     @ 0802b5aa 4948
    bl reset_display_and_obj_vram            @ 0802b5ac ccf062f8
    ldr r0, DAT_0802b6d4                     @ 0802b5b0 4848
    bl store_ewram_ctx_ptr_and_clear_mode_flags @ 0802b5b2 c8f075fe
    ldr r1, PTR_BG0CNT_0802b6d8              @ 0802b5b6 4849
    movs r0,#0x5    @ 0802b5b8 0520
    strh r0,[r1,#0x0]                        @ 0802b5ba 0880
    adds r1,#0x2    @ 0802b5bc 0231
    movs r2,#0x82    @ 0802b5be 8222
    lsls r2,r2,#0x1    @ 0802b5c0 5200
    adds r0,r2,#0x0    @ 0802b5c2 101c
    strh r0,[r1,#0x0]                        @ 0802b5c4 0880
    adds r1,#0x2    @ 0802b5c6 0231
    ldr r3, DAT_0802b6dc                     @ 0802b5c8 444b
    adds r0,r3,#0x0    @ 0802b5ca 181c
    strh r0,[r1,#0x0]                        @ 0802b5cc 0880
    adds r1,#0x2    @ 0802b5ce 0231
    ldr r2, DAT_0802b6e0                     @ 0802b5d0 434a
    adds r0,r2,#0x0    @ 0802b5d2 101c
    strh r0,[r1,#0x0]                        @ 0802b5d4 0880
    bl reset_all_bg_scroll_regs_and_shadows  @ 0802b5d6 caf057fa
    bl upload_pack_vram_and_palette          @ 0802b5da caf05dfa
    ldr r0, DAT_0802b6e4                     @ 0802b5de 4148
    movs r1,#0xc0    @ 0802b5e0 c021
    lsls r1,r1,#0x8    @ 0802b5e2 0902
    bl zero_fill_by_halfword                 @ 0802b5e4 c9f046fc
    movs r0,#0xc0    @ 0802b5e8 c020
    lsls r0,r0,#0x13    @ 0802b5ea c004
    movs r1,#0xa0    @ 0802b5ec a021
    lsls r1,r1,#0x6    @ 0802b5ee 8901
    bl zero_fill_by_halfword                 @ 0802b5f0 c9f040fc
    ldr r4, DAT_0802b6e8                     @ 0802b5f4 3c4c
    movs r1,#0x80    @ 0802b5f6 8021
    lsls r1,r1,#0x8    @ 0802b5f8 0902
    adds r0,r4,#0x0    @ 0802b5fa 201c
    bl zero_fill_by_halfword                 @ 0802b5fc c9f03afc
    ldr r0, DAT_0802b6ec                     @ 0802b600 3a48
    ldr r1, DAT_0802b6f0                     @ 0802b602 3b49
    movs r2,#0x20    @ 0802b604 2022
    bl copy_bytes_by_halfword                @ 0802b606 c9f04dfc
    ldr r1, DAT_0802b6f4                     @ 0802b60a 3a49
    movs r2,#0x80    @ 0802b60c 8022
    lsls r2,r2,#0x4    @ 0802b60e 1201
    adds r0,r4,#0x0    @ 0802b610 201c
    bl copy_bytes_by_halfword                @ 0802b612 c9f047fc
    ldr r3, DAT_0802b6f8                     @ 0802b616 384b
    movs r0,#0x0    @ 0802b618 0020
    movs r1,#0x10    @ 0802b61a 1021
    movs r2,#0x2    @ 0802b61c 0222
    bl load_pack_tile_and_map_to_vram        @ 0802b61e c2f0f7fc
    movs r0,#0x80    @ 0802b622 8020
    lsls r0,r0,#0x3    @ 0802b624 c000
    ldr r3, DAT_0802b6fc                     @ 0802b626 354b
    movs r1,#0x20    @ 0802b628 2021
    movs r2,#0x40    @ 0802b62a 4022
    bl load_pack_tile_and_map_to_vram        @ 0802b62c c2f0f0fc
    movs r0,#0x80    @ 0802b630 8020
    lsls r0,r0,#0x5    @ 0802b632 4001
    ldr r3, DAT_0802b700                     @ 0802b634 324b
    movs r1,#0x10    @ 0802b636 1021
    movs r2,#0x5a    @ 0802b638 5a22
    bl load_pack_tile_and_map_to_vram        @ 0802b63a c2f0e9fc
    movs r0,#0x1e    @ 0802b63e 1e20
    movs r1,#0x2    @ 0802b640 0221
    bl setup_line_buf_pos_and_font           @ 0802b642 c5f0b7fa
    adds r0,r5,#0x0    @ 0802b646 281c
    bl count_bytes_until_null                @ 0802b648 c9f04aff
    lsls r1,r0,#0x1    @ 0802b64c 4100
    adds r1,r1,r0    @ 0802b64e 0918
    lsls r1,r1,#0x1    @ 0802b650 4900
    cmp r1,#0xef                             @ 0802b652 ef29
    ble LAB_0802b718                         @ 0802b654 60dd
    ldr r2, DAT_0802b704                     @ 0802b656 2b4a
    ldr r0, DAT_0802b708                     @ 0802b658 2b48
    ldr r3, DAT_0802b70c                     @ 0802b65a 2c4b
    adds r0,r0,r3    @ 0802b65c c018
    movs r1,#0x7    @ 0802b65e 0721
    ldrb r0,[r0,#0x0]                        @ 0802b660 0078
    ands r1,r0    @ 0802b662 0140
    rsbs r1,r1,#0    @ 0802b664 4942
    lsrs r1,r1,#0x1f    @ 0802b666 c90f
    movs r0,#0x2    @ 0802b668 0220
    rsbs r0,r0,#0    @ 0802b66a 4042
    ldrb r3,[r2,#0x8]                        @ 0802b66c 137a
    ands r0,r3    @ 0802b66e 1840
    orrs r0,r1    @ 0802b670 0843
    movs r1,#0x3    @ 0802b672 0321
    rsbs r1,r1,#0    @ 0802b674 4942
    ands r0,r1    @ 0802b676 0840
    strb r0,[r2,#0x8]                        @ 0802b678 1072
    ldr r1, PTR_font_jp_base_table_0802b710  @ 0802b67a 2549
    lsls r0,r0,#0x1f    @ 0802b67c c007
    lsrs r0,r0,#0x1f    @ 0802b67e c00f
    lsls r0,r0,#0x3    @ 0802b680 c000
    adds r0,r0,r1    @ 0802b682 4018
    ldr r0,[r0,#0x0]                         @ 0802b684 0068
    str r0,[r2,#0x4]                         @ 0802b686 5060
    adds r0,r5,#0x0    @ 0802b688 281c
    bl count_bytes_until_null                @ 0802b68a c9f029ff
    adds r1,r0,#0x0    @ 0802b68e 011c
    lsls r0,r1,#0x2    @ 0802b690 8800
    adds r0,r0,r1    @ 0802b692 4018
    movs r4,#0xf0    @ 0802b694 f024
    subs r0,r4,r0    @ 0802b696 201a
    lsrs r1,r0,#0x1f    @ 0802b698 c10f
    adds r0,r0,r1    @ 0802b69a 4018
    asrs r0,r0,#0x1    @ 0802b69c 4010
    ldr r2, DAT_0802b714                     @ 0802b69e 1d4a
    movs r1,#0x3    @ 0802b6a0 0321
    adds r3,r5,#0x0    @ 0802b6a2 2b1c
    bl text_render_wrapper                   @ 0802b6a4 c7f0eaf9
    adds r0,r5,#0x0    @ 0802b6a8 281c
    bl count_bytes_until_null                @ 0802b6aa c9f019ff
    lsls r1,r0,#0x2    @ 0802b6ae 8100
    adds r1,r1,r0    @ 0802b6b0 0918
    subs r4,r4,r1    @ 0802b6b2 641a
    lsrs r0,r4,#0x1f    @ 0802b6b4 e00f
    adds r4,r4,r0    @ 0802b6b6 2418
    asrs r4,r4,#0x1    @ 0802b6b8 6410
    adds r0,r4,#0x0    @ 0802b6ba 201c
    movs r1,#0x3    @ 0802b6bc 0321
    movs r2,#0xe    @ 0802b6be 0e22
    adds r3,r5,#0x0    @ 0802b6c0 2b1c
    bl text_render_wrapper                   @ 0802b6c2 c7f0dbf9
    b LAB_0802b782                           @ 0802b6c6 5ce0
PTR_gPrng_0802b6c8:
    .word  gPrng                          @ 0802b6c8 40000003
DAT_0802b6cc:
    .word  0x00000401                     @ 0802b6cc 01040000
DAT_0802b6d0:
    .word  0x0203eeb0                     @ 0802b6d0 b0ee0302
DAT_0802b6d4:
    .word  0x02029eb0                     @ 0802b6d4 b09e0202
PTR_BG0CNT_0802b6d8:
    .word  BG0CNT                         @ 0802b6d8 08000004
DAT_0802b6dc:
    .word  0x0000820a                     @ 0802b6dc 0a820000
DAT_0802b6e0:
    .word  0x00000407                     @ 0802b6e0 07040000
DAT_0802b6e4:
    .word  0x06004000                     @ 0802b6e4 00400006
DAT_0802b6e8:
    .word  0x06010000                     @ 0802b6e8 00000106
DAT_0802b6ec:
    .word  0x05000220                     @ 0802b6ec 20020005
DAT_0802b6f0:
    .word  0x09b8fb8c                     @ 0802b6f0 8cfbb809
DAT_0802b6f4:
    .word  0x09b8fbac                     @ 0802b6f4 acfbb809
DAT_0802b6f8:
    .word  0x09b903ac                     @ 0802b6f8 ac03b909
DAT_0802b6fc:
    .word  0x09b90ddc                     @ 0802b6fc dc0db909
DAT_0802b700:
    .word  0x09b9119c                     @ 0802b700 9c11b909
DAT_0802b704:
    .word  0x02006ed0                     @ 0802b704 d06e0002
DAT_0802b708:
    .word  0x02000000                     @ 0802b708 00000002
DAT_0802b70c:
    .word  0x00006c2c                     @ 0802b70c 2c6c0000
PTR_font_jp_base_table_0802b710:
    .word  font_jp_base_table             @ 0802b710 54f8e509
DAT_0802b714:
    .word  0x00008001                     @ 0802b714 01800000
LAB_0802b718:
    ldr r2, DAT_0802b800                     @ 0802b718 394a
    ldr r0, DAT_0802b804                     @ 0802b71a 3a48
    ldr r1, DAT_0802b808                     @ 0802b71c 3a49
    adds r0,r0,r1    @ 0802b71e 4018
    movs r1,#0x7    @ 0802b720 0721
    ldrb r0,[r0,#0x0]                        @ 0802b722 0078
    ands r1,r0    @ 0802b724 0140
    rsbs r1,r1,#0    @ 0802b726 4942
    lsrs r1,r1,#0x1f    @ 0802b728 c90f
    movs r0,#0x2    @ 0802b72a 0220
    rsbs r0,r0,#0    @ 0802b72c 4042
    ldrb r3,[r2,#0x8]                        @ 0802b72e 137a
    ands r0,r3    @ 0802b730 1840
    orrs r0,r1    @ 0802b732 0843
    movs r1,#0x2    @ 0802b734 0221
    orrs r0,r1    @ 0802b736 0843
    strb r0,[r2,#0x8]                        @ 0802b738 1072
    ldr r3, PTR_font_jp_base_table_0802b80c  @ 0802b73a 344b
    lsls r1,r0,#0x1e    @ 0802b73c 8107
    lsrs r1,r1,#0x1f    @ 0802b73e c90f
    lsls r1,r1,#0x2    @ 0802b740 8900
    lsls r0,r0,#0x1f    @ 0802b742 c007
    lsrs r0,r0,#0x1f    @ 0802b744 c00f
    lsls r0,r0,#0x3    @ 0802b746 c000
    adds r1,r1,r0    @ 0802b748 0918
    adds r1,r1,r3    @ 0802b74a c918
    ldr r0,[r1,#0x0]                         @ 0802b74c 0868
    str r0,[r2,#0x4]                         @ 0802b74e 5060
    adds r0,r5,#0x0    @ 0802b750 281c
    bl count_bytes_until_null                @ 0802b752 c9f0c5fe
    adds r1,r0,#0x0    @ 0802b756 011c
    lsls r0,r1,#0x1    @ 0802b758 4800
    adds r0,r0,r1    @ 0802b75a 4018
    movs r4,#0x78    @ 0802b75c 7824
    subs r0,r4,r0    @ 0802b75e 201a
    ldr r2, DAT_0802b810                     @ 0802b760 2b4a
    movs r1,#0x3    @ 0802b762 0321
    adds r3,r5,#0x0    @ 0802b764 2b1c
    bl text_render_wrapper                   @ 0802b766 c7f089f9
    adds r0,r5,#0x0    @ 0802b76a 281c
    bl count_bytes_until_null                @ 0802b76c c9f0b8fe
    lsls r1,r0,#0x1    @ 0802b770 4100
    adds r1,r1,r0    @ 0802b772 0918
    subs r4,r4,r1    @ 0802b774 641a
    adds r0,r4,#0x0    @ 0802b776 201c
    movs r1,#0x3    @ 0802b778 0321
    movs r2,#0xe    @ 0802b77a 0e22
    adds r3,r5,#0x0    @ 0802b77c 2b1c
    bl text_render_wrapper                   @ 0802b77e c7f07df9
LAB_0802b782:
    ldr r0, DAT_0802b814                     @ 0802b782 2448
    movs r1,#0x0    @ 0802b784 0021
    bl commit_line_buffer_to_sprite_vram     @ 0802b786 c7f061fb
    movs r4,#0x62    @ 0802b78a 6224
    movs r3,#0x0    @ 0802b78c 0023
    ldr r6, DAT_0802b818                     @ 0802b78e 224e
    movs r0,#0x80    @ 0802b790 8020
    lsls r0,r0,#0x6    @ 0802b792 8001
    adds r5,r0,#0x0    @ 0802b794 051c
LAB_0802b796:
    lsls r0,r3,#0x10    @ 0802b796 1804
    lsrs r0,r0,#0xa    @ 0802b798 800a
    ldr r2, DAT_0802b81c                     @ 0802b79a 204a
    adds r1,r0,r2    @ 0802b79c 8118
    adds r2,r3,#0x1    @ 0802b79e 5a1c
    movs r3,#0x1d    @ 0802b7a0 1d23
LAB_0802b7a2:
    adds r0,r4,r5    @ 0802b7a2 6019
    strh r0,[r1,#0x0]                        @ 0802b7a4 0880
    adds r1,#0x2    @ 0802b7a6 0231
    adds r0,r4,#0x1    @ 0802b7a8 601c
    lsls r0,r0,#0x10    @ 0802b7aa 0004
    lsrs r4,r0,#0x10    @ 0802b7ac 040c
    subs r3,#0x1    @ 0802b7ae 013b
    cmp r3,#0x0                              @ 0802b7b0 002b
    bge LAB_0802b7a2                         @ 0802b7b2 f6da
    adds r3,r2,#0x0    @ 0802b7b4 131c
    cmp r3,#0x1                              @ 0802b7b6 012b
    ble LAB_0802b796                         @ 0802b7b8 eddd
    adds r2,r6,#0x0    @ 0802b7ba 321c
    adds r2,#0x6d    @ 0802b7bc 6d32
    movs r0,#0x1    @ 0802b7be 0120
    adds r1,r7,#0x0    @ 0802b7c0 391c
    ands r1,r0    @ 0802b7c2 0140
    lsls r1,r1,#0x6    @ 0802b7c4 8901
    movs r0,#0x41    @ 0802b7c6 4120
    rsbs r0,r0,#0    @ 0802b7c8 4042
    ldrb r3,[r2,#0x0]                        @ 0802b7ca 1378
    ands r0,r3    @ 0802b7cc 1840
    orrs r0,r1    @ 0802b7ce 0843
    strb r0,[r2,#0x0]                        @ 0802b7d0 1070
    cmp r7,#0x0                              @ 0802b7d2 002f
    beq LAB_0802b84a                         @ 0802b7d4 39d0
    ldr r0, DAT_0802b804                     @ 0802b7d6 0b48
    ldr r1, DAT_0802b808                     @ 0802b7d8 0b49
    adds r0,r0,r1    @ 0802b7da 4018
    movs r1,#0x7    @ 0802b7dc 0721
    ldrb r0,[r0,#0x0]                        @ 0802b7de 0078
    ands r1,r0    @ 0802b7e0 0140
    cmp r1,#0x1                              @ 0802b7e2 0129
    beq LAB_0802b840                         @ 0802b7e4 2cd0
    cmp r1,#0x2                              @ 0802b7e6 0229
    beq LAB_0802b838                         @ 0802b7e8 26d0
    cmp r1,#0x3                              @ 0802b7ea 0329
    beq LAB_0802b830                         @ 0802b7ec 20d0
    cmp r1,#0x4                              @ 0802b7ee 0429
    beq LAB_0802b828                         @ 0802b7f0 1ad0
    ldr r0, DAT_0802b820                     @ 0802b7f2 0b48
    cmp r1,#0x5                              @ 0802b7f4 0529
    bne LAB_0802b842                         @ 0802b7f6 24d1
    ldr r2, DAT_0802b824                     @ 0802b7f8 0a4a
    adds r0,r0,r2    @ 0802b7fa 8018
    b LAB_0802b842                           @ 0802b7fc 21e0
    .zero  0x2
DAT_0802b800:
    .word  0x02006ed0                     @ 0802b800 d06e0002
DAT_0802b804:
    .word  0x02000000                     @ 0802b804 00000002
DAT_0802b808:
    .word  0x00006c2c                     @ 0802b808 2c6c0000
PTR_font_jp_base_table_0802b80c:
    .word  font_jp_base_table             @ 0802b80c 54f8e509
DAT_0802b810:
    .word  0x00008001                     @ 0802b810 01800000
DAT_0802b814:
    .word  0x06004c40                     @ 0802b814 404c0006
DAT_0802b818:
    .word  0x02023360                     @ 0802b818 60330202
DAT_0802b81c:
    .word  0x06000800                     @ 0802b81c 00080006
DAT_0802b820:
    .word  0x09dbe758                     @ 0802b820 58e7db09
DAT_0802b824:
    .word  0x0003ab1c                     @ 0802b824 1cab0300
LAB_0802b828:
    ldr r0, DAT_0802b82c                     @ 0802b828 0048
    b LAB_0802b842                           @ 0802b82a 0ae0
DAT_0802b82c:
    .word  0x09ded5d6                     @ 0802b82c d6d5de09
LAB_0802b830:
    ldr r0, DAT_0802b834                     @ 0802b830 0048
    b LAB_0802b842                           @ 0802b832 06e0
DAT_0802b834:
    .word  0x09de113c                     @ 0802b834 3c11de09
LAB_0802b838:
    ldr r0, DAT_0802b83c                     @ 0802b838 0048
    b LAB_0802b842                           @ 0802b83a 02e0
DAT_0802b83c:
    .word  0x09dd4ea8                     @ 0802b83c a84edd09
LAB_0802b840:
    ldr r0, DAT_0802b850                     @ 0802b840 0348
LAB_0802b842:
    movs r1,#0x2    @ 0802b842 0221
    movs r2,#0x1    @ 0802b844 0122
    bl render_card_name_centered_to_sprite_vram @ 0802b846 fff71dfe
LAB_0802b84a:
    pop {r4,r5,r6,r7}                        @ 0802b84a f0bc
    pop {r0}                                 @ 0802b84c 01bc
    bx r0                                    @ 0802b84e 0047
DAT_0802b850:
    .word  0x09dc9810                     @ 0802b850 1098dc09

@ duel_puzzle scene LP digit OAM sprite render function, called by FUN_0801fec0 (duel_puzzle main loop) and FUN_0802bdc4 / FUN_0802bde4 / dispatch_puzzle_display_mode (0x0802be08) each frame. Reads [0x02023360+0x68] as current LP value, copies it to gPrng+0x1ec as display shadow value, checks [0x02023360+0x6d] bit6 as LP display enable flag. If enabled, iterates: LP %10 -> digit; OAM Y coord = 0x9000_0000 | (r5 -= 6 per digit) | digit_x_offset; OAM tile = 0x8000; call write_oam_entry_from_packed_args; LP /= 10; until LP==0. Each digit y-coord decreases by 6 pixels (higher-order digits appear higher), tile index = 0x1008 + digit_value.
@ 
@ Constants:
@ - scene_ctx base = 0x02023360
@ - LP value offset = 0x68 (word)
@ - LP display shadow = gPrng+0x1ec (gPrng+0xf6*2)
@ - LP display enable flag = [0x02023360+0x6d] bit6 (0x40)
@ - digit tile base offset = 0x1008
@ - OAM attr1 base = 0x8000 (8x8 sprite size)
@ - digit y-step = 6 pixels per digit
@ - modulo divisor = 10 (via __modsi3 / __divsi3)
render_puzzle_lp_digit_sprites:
    push {r4,r5,lr}                          @ 0802b854 30b5
    movs r5,#0xc6    @ 0802b856 c625
    ldr r1, DAT_0802b8b0                     @ 0802b858 1549
    ldr r4,[r1,#0x68]                        @ 0802b85a 8c6e
    ldr r0, PTR_gPrng_0802b8b4               @ 0802b85c 1548
    adds r2,r1,#0x0    @ 0802b85e 0a1c
    adds r2,#0x62    @ 0802b860 6232
    ldrh r2,[r2,#0x0]                        @ 0802b862 1288
    movs r3,#0xf6    @ 0802b864 f623
    lsls r3,r3,#0x1    @ 0802b866 5b00
    adds r0,r0,r3    @ 0802b868 c018
    strh r2,[r0,#0x0]                        @ 0802b86a 0280
    adds r1,#0x6d    @ 0802b86c 6d31
    movs r0,#0x40    @ 0802b86e 4020
    ldrb r1,[r1,#0x0]                        @ 0802b870 0978
    ands r0,r1    @ 0802b872 0840
    cmp r0,#0x0                              @ 0802b874 0028
    beq LAB_0802b8a8                         @ 0802b876 17d0
LAB_0802b878:
    adds r0,r4,#0x0    @ 0802b878 201c
    movs r1,#0xa    @ 0802b87a 0a21
    bl __modsi3                              @ 0802b87c e2f00eff
    adds r2,r0,#0x0    @ 0802b880 021c
    movs r0,#0x90    @ 0802b882 9020
    lsls r0,r0,#0x10    @ 0802b884 0004
    orrs r0,r5    @ 0802b886 2843
    ldr r1, DAT_0802b8b8                     @ 0802b888 0b49
    adds r2,r2,r1    @ 0802b88a 5218
    lsls r2,r2,#0x10    @ 0802b88c 1204
    lsrs r2,r2,#0x10    @ 0802b88e 120c
    movs r1,#0x80    @ 0802b890 8021
    lsls r1,r1,#0x8    @ 0802b892 0902
    bl write_oam_entry_from_packed_args      @ 0802b894 caf06afc
    subs r5,#0x6    @ 0802b898 063d
    adds r0,r4,#0x0    @ 0802b89a 201c
    movs r1,#0xa    @ 0802b89c 0a21
    bl __divsi3                              @ 0802b89e e2f0b1fe
    adds r4,r0,#0x0    @ 0802b8a2 041c
    cmp r4,#0x0                              @ 0802b8a4 002c
    bgt LAB_0802b878                         @ 0802b8a6 e7dc
LAB_0802b8a8:
    pop {r4,r5}                              @ 0802b8a8 30bc
    pop {r0}                                 @ 0802b8aa 01bc
    bx r0                                    @ 0802b8ac 0047
    .zero  0x2
DAT_0802b8b0:
    .word  0x02023360                     @ 0802b8b0 60330202
PTR_gPrng_0802b8b4:
    .word  gPrng                          @ 0802b8b4 40000003
DAT_0802b8b8:
    .word  0x00001008                     @ 0802b8b8 08100000

@ duel_puzzle scene card name display line buffer init function, called by run_campaign_step30_pack_card_info_display (0x080277a4). No parameters. Fixed call to setup_line_buf_with_font_and_align(col=0x18, width=0x2a, align=1, flags=0) to init line buffer. Reads [0x02000000+0x6c2c] (scene state byte) bits[2:0] as font_style, clears [0x02006ed0+0x8] bit1 via ~0x02 mask, computes (font_style&7 nonzero) -> bit0 set; looks up font_jp_base_table[bit_combo] to update [0x02006ed0+0x4] font pointer. Then zero_fill [0x02006ed0+?] region 0x20 halfwords (clear line-buf content). Writes 0 to [scene_ctx+0x62], [+0x64], [+0x68], clears [scene_ctx+0x6c] bit5.
@ 
@ Constants:
@ - line_buf_ctx = 0x02006ed0
@ - font table = font_jp_base_table
@ - setup params: col=0x18, width=0x2a, align=1, flags=0
@ - zero_fill target = line-buf content area, 0x20 halfwords
@ - scene_ctx = 0x02023360
@ - fields cleared: [scene_ctx+0x62]=0, [+0x64]=0, [+0x68]=0, [+0x6c] &= ~0x20 (bit5)
init_puzzle_card_name_line_buf:
    push {lr}                                @ 0802b8bc 00b5
    movs r0,#0x18    @ 0802b8be 1820
    movs r1,#0x2a    @ 0802b8c0 2a21
    movs r2,#0x1    @ 0802b8c2 0122
    movs r3,#0x0    @ 0802b8c4 0023
    bl setup_line_buf_with_font_and_align    @ 0802b8c6 c5f0fbf9
    ldr r2, DAT_0802b928                     @ 0802b8ca 174a
    ldr r0, DAT_0802b92c                     @ 0802b8cc 1748
    ldr r1, DAT_0802b930                     @ 0802b8ce 1849
    adds r0,r0,r1    @ 0802b8d0 4018
    movs r1,#0x7    @ 0802b8d2 0721
    ldrb r0,[r0,#0x0]                        @ 0802b8d4 0078
    ands r1,r0    @ 0802b8d6 0140
    rsbs r1,r1,#0    @ 0802b8d8 4942
    lsrs r1,r1,#0x1f    @ 0802b8da c90f
    movs r0,#0x2    @ 0802b8dc 0220
    rsbs r0,r0,#0    @ 0802b8de 4042
    ldrb r3,[r2,#0x8]                        @ 0802b8e0 137a
    ands r0,r3    @ 0802b8e2 1840
    orrs r0,r1    @ 0802b8e4 0843
    movs r1,#0x2    @ 0802b8e6 0221
    orrs r0,r1    @ 0802b8e8 0843
    strb r0,[r2,#0x8]                        @ 0802b8ea 1072
    ldr r3, PTR_font_jp_base_table_0802b934  @ 0802b8ec 114b
    lsls r1,r0,#0x1e    @ 0802b8ee 8107
    lsrs r1,r1,#0x1f    @ 0802b8f0 c90f
    lsls r1,r1,#0x2    @ 0802b8f2 8900
    lsls r0,r0,#0x1f    @ 0802b8f4 c007
    lsrs r0,r0,#0x1f    @ 0802b8f6 c00f
    lsls r0,r0,#0x3    @ 0802b8f8 c000
    adds r1,r1,r0    @ 0802b8fa 0918
    adds r1,r1,r3    @ 0802b8fc c918
    ldr r0,[r1,#0x0]                         @ 0802b8fe 0868
    str r0,[r2,#0x4]                         @ 0802b900 5060
    ldr r0, DAT_0802b938                     @ 0802b902 0d48
    movs r1,#0x20    @ 0802b904 2021
    bl zero_fill_by_halfword                 @ 0802b906 c9f0b5fa
    ldr r2, DAT_0802b93c                     @ 0802b90a 0c4a
    adds r1,r2,#0x0    @ 0802b90c 111c
    adds r1,#0x62    @ 0802b90e 6231
    movs r0,#0x0    @ 0802b910 0020
    strh r0,[r1,#0x0]                        @ 0802b912 0880
    adds r1,#0x2    @ 0802b914 0231
    strh r0,[r1,#0x0]                        @ 0802b916 0880
    str r0,[r2,#0x68]                        @ 0802b918 9066
    adds r1,#0x8    @ 0802b91a 0831
    subs r0,#0x20    @ 0802b91c 2038
    ldrb r2,[r1,#0x0]                        @ 0802b91e 0a78
    ands r0,r2    @ 0802b920 1040
    strb r0,[r1,#0x0]                        @ 0802b922 0870
    pop {r0}                                 @ 0802b924 01bc
    bx r0                                    @ 0802b926 0047
DAT_0802b928:
    .word  0x02006ed0                     @ 0802b928 d06e0002
DAT_0802b92c:
    .word  0x02000000                     @ 0802b92c 00000002
DAT_0802b930:
    .word  0x00006c2c                     @ 0802b930 2c6c0000
PTR_font_jp_base_table_0802b934:
    .word  font_jp_base_table             @ 0802b934 54f8e509
DAT_0802b938:
    .word  0x050001e0                     @ 0802b938 e0010005
DAT_0802b93c:
    .word  0x02023360                     @ 0802b93c 60330202

@ General game string + number combined render function. Writes r2 (text_ptr) to the
@ gPrng scene struct line buffer slot (position determined by r0 bits[4:0] and bits[4:0]>>2),
@ writes r1 (line_buf_y) to another slot, then truncates the low 6 bits of halfword at
@ 0x02006ed0+0xc, calls text_render_wrapper(2, line_buf_x, 7, text_ptr) to render the main
@ string. Then based on r1: r1==7 -> updates line_buf_x += 0xc and branches; r1==8 ->
@ branches to alternate render path; otherwise -> selects digit render branch based on
@ whether r0 <= 9 (uses FUN_0802bb74 for <=9, FUN_0802bb68 for >9).
@ Called by render_card_stats_to_line_buf / render_game_text_with_font_type_a /
@ render_game_text_with_font_type_b and others.
@ 
@ Constants:
@ - gPrng+0xb6*2 = 0x16c (line buffer slot Y base address)
@ - 0x02023360 = scene line buffer base
@ - 0x02006ed0 = known EWRAM scene state region
@ - 0x3f mask = low 6 bits truncation (line_buf x count)
render_game_string_with_number:
    push {r4,r5,r6,r7,lr}                    @ 0802b940 f0b5
    .hword 0x464f    @ 0802b942 4f46
    .hword 0x4646    @ 0802b944 4646
    push {r6,r7}                             @ 0802b946 c0b4
    adds r3,r0,#0x0    @ 0802b948 031c
    adds r7,r1,#0x0    @ 0802b94a 0f1c
    adds r6,r2,#0x0    @ 0802b94c 161c
    movs r0,#0xb6    @ 0802b94e b620
    .hword 0x4681    @ 0802b950 8146
    ldr r5, DAT_0802b9b0                     @ 0802b952 174d
    adds r2,r5,#0x0    @ 0802b954 2a1c
    adds r2,#0x6c    @ 0802b956 6c32
    ldrb r1,[r2,#0x0]                        @ 0802b958 1178
    lsls r0,r1,#0x1b    @ 0802b95a c806
    lsrs r0,r0,#0x19    @ 0802b95c 400e
    adds r1,r5,#0x0    @ 0802b95e 291c
    adds r1,#0x78    @ 0802b960 7831
    adds r0,r0,r1    @ 0802b962 4018
    str r6,[r0,#0x0]                         @ 0802b964 0660
    ldrb r2,[r2,#0x0]                        @ 0802b966 1278
    lsls r0,r2,#0x1b    @ 0802b968 d006
    lsrs r0,r0,#0x1b    @ 0802b96a c00e
    adds r1,#0x80    @ 0802b96c 8031
    adds r0,r0,r1    @ 0802b96e 4018
    strb r7,[r0,#0x0]                        @ 0802b970 0770
    ldr r4, DAT_0802b9b4                     @ 0802b972 104c
    movs r0,#0x3f    @ 0802b974 3f20
    ldrh r2,[r4,#0xc]                        @ 0802b976 a289
    ands r0,r2    @ 0802b978 1040
    strh r0,[r4,#0xc]                        @ 0802b97a a081
    adds r5,#0x64    @ 0802b97c 6435
    ldrh r1,[r5,#0x0]                        @ 0802b97e 2988
    movs r0,#0x2    @ 0802b980 0220
    movs r2,#0x7    @ 0802b982 0722
    bl text_render_wrapper                   @ 0802b984 c7f07af8
    ldrh r1,[r4,#0xe]                        @ 0802b988 e189
    lsls r0,r1,#0x16    @ 0802b98a 8805
    lsrs r0,r0,#0x16    @ 0802b98c 800d
    ldrh r1,[r5,#0x0]                        @ 0802b98e 2988
    adds r1,#0xc    @ 0802b990 0c31
    cmp r0,r1                                @ 0802b992 8842
    ble LAB_0802b998                         @ 0802b994 00dd
    strh r1,[r5,#0x0]                        @ 0802b996 2980
LAB_0802b998:
    cmp r7,#0x7                              @ 0802b998 072f
    beq LAB_0802b9b8                         @ 0802b99a 0dd0
    cmp r7,#0x8                              @ 0802b99c 082f
    bne LAB_0802b9a2                         @ 0802b99e 00d1
    b LAB_0802bc54                           @ 0802b9a0 58e1
LAB_0802b9a2:
    movs r5,#0xb6    @ 0802b9a2 b625
    adds r0,r6,#0x0    @ 0802b9a4 301c
    cmp r6,#0x9                              @ 0802b9a6 092e
    bgt LAB_0802b9ac                         @ 0802b9a8 00dc
    b LAB_0802bb74                           @ 0802b9aa e3e0
LAB_0802b9ac:
    b LAB_0802bb68                           @ 0802b9ac dce0
    .zero  0x2
DAT_0802b9b0:
    .word  0x02023360                     @ 0802b9b0 60330202
DAT_0802b9b4:
    .word  0x02006ed0                     @ 0802b9b4 d06e0002
LAB_0802b9b8:
    ldrh r0,[r5,#0x0]                        @ 0802b9b8 2888
    adds r0,#0xc    @ 0802b9ba 0c30
    strh r0,[r5,#0x0]                        @ 0802b9bc 2880
    cmp r6,#0x0                              @ 0802b9be 002e
    beq LAB_0802ba94                         @ 0802b9c0 68d0
    ldr r0, DAT_0802b9e8                     @ 0802b9c2 0948
    ldr r2, DAT_0802b9ec                     @ 0802b9c4 094a
    adds r0,r0,r2    @ 0802b9c6 8018
    ldrb r0,[r0,#0x0]                        @ 0802b9c8 0078
    ands r0,r7    @ 0802b9ca 3840
    cmp r0,#0x1                              @ 0802b9cc 0128
    beq LAB_0802ba10                         @ 0802b9ce 1fd0
    cmp r0,#0x2                              @ 0802b9d0 0228
    beq LAB_0802ba08                         @ 0802b9d2 19d0
    cmp r0,#0x3                              @ 0802b9d4 0328
    beq LAB_0802ba00                         @ 0802b9d6 13d0
    cmp r0,#0x4                              @ 0802b9d8 0428
    beq LAB_0802b9f8                         @ 0802b9da 0dd0
    ldr r1, DAT_0802b9f0                     @ 0802b9dc 0449
    cmp r0,#0x5                              @ 0802b9de 0528
    bne LAB_0802ba12                         @ 0802b9e0 17d1
    ldr r0, DAT_0802b9f4                     @ 0802b9e2 0448
    adds r1,r1,r0    @ 0802b9e4 0918
    b LAB_0802ba12                           @ 0802b9e6 14e0
DAT_0802b9e8:
    .word  0x02000000                     @ 0802b9e8 00000002
DAT_0802b9ec:
    .word  0x00006c2c                     @ 0802b9ec 2c6c0000
DAT_0802b9f0:
    .word  0x09dc01d8                     @ 0802b9f0 d801dc09
DAT_0802b9f4:
    .word  0x0003ab80                     @ 0802b9f4 80ab0300
LAB_0802b9f8:
    ldr r1, DAT_0802b9fc                     @ 0802b9f8 0049
    b LAB_0802ba12                           @ 0802b9fa 0ae0
DAT_0802b9fc:
    .word  0x09def19a                     @ 0802b9fc 9af1de09
LAB_0802ba00:
    ldr r1, DAT_0802ba04                     @ 0802ba00 0049
    b LAB_0802ba12                           @ 0802ba02 06e0
DAT_0802ba04:
    .word  0x09de2d00                     @ 0802ba04 002dde09
LAB_0802ba08:
    ldr r1, DAT_0802ba0c                     @ 0802ba08 0049
    b LAB_0802ba12                           @ 0802ba0a 02e0
DAT_0802ba0c:
    .word  0x09dd6982                     @ 0802ba0c 8269dd09
LAB_0802ba10:
    ldr r1, DAT_0802ba54                     @ 0802ba10 1049
LAB_0802ba12:
    adds r0,r1,#0x0    @ 0802ba12 081c
    bl count_bytes_until_null                @ 0802ba14 c9f064fd
    lsls r1,r0,#0x1    @ 0802ba18 4100
    adds r1,r1,r0    @ 0802ba1a 0918
    lsls r1,r1,#0x1    @ 0802ba1c 4900
    .hword 0x464a    @ 0802ba1e 4a46
    subs r2,r2,r1    @ 0802ba20 521a
    .hword 0x4691    @ 0802ba22 9146
    ldr r0, DAT_0802ba58                     @ 0802ba24 0c48
    adds r0,#0x64    @ 0802ba26 6430
    ldrh r1,[r0,#0x0]                        @ 0802ba28 0188
    ldr r0, DAT_0802ba5c                     @ 0802ba2a 0c48
    ldr r2, DAT_0802ba60                     @ 0802ba2c 0c4a
    adds r0,r0,r2    @ 0802ba2e 8018
    movs r2,#0x7    @ 0802ba30 0722
    ldrb r0,[r0,#0x0]                        @ 0802ba32 0078
    ands r2,r0    @ 0802ba34 0240
    cmp r2,#0x1                              @ 0802ba36 012a
    beq LAB_0802ba84                         @ 0802ba38 24d0
    cmp r2,#0x2                              @ 0802ba3a 022a
    beq LAB_0802ba7c                         @ 0802ba3c 1ed0
    cmp r2,#0x3                              @ 0802ba3e 032a
    beq LAB_0802ba74                         @ 0802ba40 18d0
    cmp r2,#0x4                              @ 0802ba42 042a
    beq LAB_0802ba6c                         @ 0802ba44 12d0
    ldr r3, DAT_0802ba64                     @ 0802ba46 074b
    cmp r2,#0x5                              @ 0802ba48 052a
    bne LAB_0802ba86                         @ 0802ba4a 1cd1
    ldr r0, DAT_0802ba68                     @ 0802ba4c 0648
    adds r3,r3,r0    @ 0802ba4e 1b18
    b LAB_0802ba86                           @ 0802ba50 19e0
    .zero  0x2
DAT_0802ba54:
    .word  0x09dcafac                     @ 0802ba54 acafdc09
DAT_0802ba58:
    .word  0x02023360                     @ 0802ba58 60330202
DAT_0802ba5c:
    .word  0x02000000                     @ 0802ba5c 00000002
DAT_0802ba60:
    .word  0x00006c2c                     @ 0802ba60 2c6c0000
DAT_0802ba64:
    .word  0x09dc01d8                     @ 0802ba64 d801dc09
DAT_0802ba68:
    .word  0x0003ab80                     @ 0802ba68 80ab0300
LAB_0802ba6c:
    ldr r3, DAT_0802ba70                     @ 0802ba6c 004b
    b LAB_0802ba86                           @ 0802ba6e 0ae0
DAT_0802ba70:
    .word  0x09def19a                     @ 0802ba70 9af1de09
LAB_0802ba74:
    ldr r3, DAT_0802ba78                     @ 0802ba74 004b
    b LAB_0802ba86                           @ 0802ba76 06e0
DAT_0802ba78:
    .word  0x09de2d00                     @ 0802ba78 002dde09
LAB_0802ba7c:
    ldr r3, DAT_0802ba80                     @ 0802ba7c 004b
    b LAB_0802ba86                           @ 0802ba7e 02e0
DAT_0802ba80:
    .word  0x09dd6982                     @ 0802ba80 8269dd09
LAB_0802ba84:
    ldr r3, DAT_0802ba90                     @ 0802ba84 024b
LAB_0802ba86:
    .hword 0x4648    @ 0802ba86 4846
    movs r2,#0x6    @ 0802ba88 0622
    bl text_render_wrapper                   @ 0802ba8a c6f0f7ff
    b LAB_0802bc30                           @ 0802ba8e cfe0
DAT_0802ba90:
    .word  0x09dcafac                     @ 0802ba90 acafdc09
LAB_0802ba94:
    ldr r0, DAT_0802babc                     @ 0802ba94 0948
    ldr r1, DAT_0802bac0                     @ 0802ba96 0a49
    adds r0,r0,r1    @ 0802ba98 4018
    ldrb r0,[r0,#0x0]                        @ 0802ba9a 0078
    ands r0,r7    @ 0802ba9c 3840
    cmp r0,#0x1                              @ 0802ba9e 0128
    beq LAB_0802bae4                         @ 0802baa0 20d0
    cmp r0,#0x2                              @ 0802baa2 0228
    beq LAB_0802badc                         @ 0802baa4 1ad0
    cmp r0,#0x3                              @ 0802baa6 0328
    beq LAB_0802bad4                         @ 0802baa8 14d0
    cmp r0,#0x4                              @ 0802baaa 0428
    beq LAB_0802bacc                         @ 0802baac 0ed0
    ldr r1, DAT_0802bac4                     @ 0802baae 0549
    cmp r0,#0x5                              @ 0802bab0 0528
    bne LAB_0802bae6                         @ 0802bab2 18d1
    ldr r2, DAT_0802bac8                     @ 0802bab4 044a
    adds r1,r1,r2    @ 0802bab6 8918
    b LAB_0802bae6                           @ 0802bab8 15e0
    .zero  0x2
DAT_0802babc:
    .word  0x02000000                     @ 0802babc 00000002
DAT_0802bac0:
    .word  0x00006c2c                     @ 0802bac0 2c6c0000
DAT_0802bac4:
    .word  0x09dc01de                     @ 0802bac4 de01dc09
DAT_0802bac8:
    .word  0x0003ab86                     @ 0802bac8 86ab0300
LAB_0802bacc:
    ldr r1, DAT_0802bad0                     @ 0802bacc 0049
    b LAB_0802bae6                           @ 0802bace 0ae0
DAT_0802bad0:
    .word  0x09def1a6                     @ 0802bad0 a6f1de09
LAB_0802bad4:
    ldr r1, DAT_0802bad8                     @ 0802bad4 0049
    b LAB_0802bae6                           @ 0802bad6 06e0
DAT_0802bad8:
    .word  0x09de2d08                     @ 0802bad8 082dde09
LAB_0802badc:
    ldr r1, DAT_0802bae0                     @ 0802badc 0049
    b LAB_0802bae6                           @ 0802bade 02e0
DAT_0802bae0:
    .word  0x09dd698c                     @ 0802bae0 8c69dd09
LAB_0802bae4:
    ldr r1, DAT_0802bb28                     @ 0802bae4 1049
LAB_0802bae6:
    adds r0,r1,#0x0    @ 0802bae6 081c
    bl count_bytes_until_null                @ 0802bae8 c9f0fafc
    lsls r1,r0,#0x1    @ 0802baec 4100
    adds r1,r1,r0    @ 0802baee 0918
    lsls r1,r1,#0x1    @ 0802baf0 4900
    .hword 0x4648    @ 0802baf2 4846
    subs r0,r0,r1    @ 0802baf4 401a
    .hword 0x4681    @ 0802baf6 8146
    ldr r0, DAT_0802bb2c                     @ 0802baf8 0c48
    adds r0,#0x64    @ 0802bafa 6430
    ldrh r1,[r0,#0x0]                        @ 0802bafc 0188
    ldr r0, DAT_0802bb30                     @ 0802bafe 0c48
    ldr r2, DAT_0802bb34                     @ 0802bb00 0c4a
    adds r0,r0,r2    @ 0802bb02 8018
    movs r2,#0x7    @ 0802bb04 0722
    ldrb r0,[r0,#0x0]                        @ 0802bb06 0078
    ands r2,r0    @ 0802bb08 0240
    cmp r2,#0x1                              @ 0802bb0a 012a
    beq LAB_0802bb58                         @ 0802bb0c 24d0
    cmp r2,#0x2                              @ 0802bb0e 022a
    beq LAB_0802bb50                         @ 0802bb10 1ed0
    cmp r2,#0x3                              @ 0802bb12 032a
    beq LAB_0802bb48                         @ 0802bb14 18d0
    cmp r2,#0x4                              @ 0802bb16 042a
    beq LAB_0802bb40                         @ 0802bb18 12d0
    ldr r3, DAT_0802bb38                     @ 0802bb1a 074b
    cmp r2,#0x5                              @ 0802bb1c 052a
    bne LAB_0802bb5a                         @ 0802bb1e 1cd1
    ldr r0, DAT_0802bb3c                     @ 0802bb20 0648
    adds r3,r3,r0    @ 0802bb22 1b18
    b LAB_0802bb5a                           @ 0802bb24 19e0
    .zero  0x2
DAT_0802bb28:
    .word  0x09dcafb8                     @ 0802bb28 b8afdc09
DAT_0802bb2c:
    .word  0x02023360                     @ 0802bb2c 60330202
DAT_0802bb30:
    .word  0x02000000                     @ 0802bb30 00000002
DAT_0802bb34:
    .word  0x00006c2c                     @ 0802bb34 2c6c0000
DAT_0802bb38:
    .word  0x09dc01de                     @ 0802bb38 de01dc09
DAT_0802bb3c:
    .word  0x0003ab86                     @ 0802bb3c 86ab0300
LAB_0802bb40:
    ldr r3, DAT_0802bb44                     @ 0802bb40 004b
    b LAB_0802bb5a                           @ 0802bb42 0ae0
DAT_0802bb44:
    .word  0x09def1a6                     @ 0802bb44 a6f1de09
LAB_0802bb48:
    ldr r3, DAT_0802bb4c                     @ 0802bb48 004b
    b LAB_0802bb5a                           @ 0802bb4a 06e0
DAT_0802bb4c:
    .word  0x09de2d08                     @ 0802bb4c 082dde09
LAB_0802bb50:
    ldr r3, DAT_0802bb54                     @ 0802bb50 004b
    b LAB_0802bb5a                           @ 0802bb52 02e0
DAT_0802bb54:
    .word  0x09dd698c                     @ 0802bb54 8c69dd09
LAB_0802bb58:
    ldr r3, DAT_0802bb64                     @ 0802bb58 024b
LAB_0802bb5a:
    .hword 0x4648    @ 0802bb5a 4846
    movs r2,#0x3    @ 0802bb5c 0322
    bl text_render_wrapper                   @ 0802bb5e c6f08dff
    b LAB_0802bc30                           @ 0802bb62 65e0
DAT_0802bb64:
    .word  0x09dcafb8                     @ 0802bb64 b8afdc09
LAB_0802bb68:
    movs r1,#0xa    @ 0802bb68 0a21
    bl __divsi3                              @ 0802bb6a e2f04bfd
    subs r5,#0x6    @ 0802bb6e 063d
    cmp r0,#0x9                              @ 0802bb70 0928
    bgt LAB_0802bb68                         @ 0802bb72 f9dc
LAB_0802bb74:
    cmp r7,#0x3                              @ 0802bb74 032f
    bgt LAB_0802bb7a                         @ 0802bb76 00dc
    subs r5,#0xc    @ 0802bb78 0c3d
LAB_0802bb7a:
    ldrh r4,[r4,#0xc]                        @ 0802bb7a a489
    lsrs r0,r4,#0x6    @ 0802bb7c a009
    cmp r5,r0                                @ 0802bb7e 8542
    bge LAB_0802bb8c                         @ 0802bb80 04da
    ldr r0, DAT_0802bc60                     @ 0802bb82 3748
    adds r0,#0x64    @ 0802bb84 6430
    ldrh r1,[r0,#0x0]                        @ 0802bb86 0188
    adds r1,#0xc    @ 0802bb88 0c31
    strh r1,[r0,#0x0]                        @ 0802bb8a 0180
LAB_0802bb8c:
    ldr r5, DAT_0802bc64                     @ 0802bb8c 354d
    ldr r0, DAT_0802bc68                     @ 0802bb8e 3648
    adds r4,r7,r0    @ 0802bb90 3c18
LAB_0802bb92:
    adds r0,r6,#0x0    @ 0802bb92 301c
    movs r1,#0xa    @ 0802bb94 0a21
    bl __modsi3                              @ 0802bb96 e2f081fd
    adds r0,#0x30    @ 0802bb9a 3030
    lsls r0,r0,#0x18    @ 0802bb9c 0006
    lsrs r0,r0,#0x18    @ 0802bb9e 000e
    ldrh r2,[r5,#0x0]                        @ 0802bba0 2a88
    ldrb r3,[r4,#0x0]                        @ 0802bba2 2378
    .hword 0x4649    @ 0802bba4 4946
    bl render_glyph_jp_single_layer          @ 0802bba6 c5f0fdfe
    adds r0,r6,#0x0    @ 0802bbaa 301c
    movs r1,#0xa    @ 0802bbac 0a21
    bl __divsi3                              @ 0802bbae e2f029fd
    adds r6,r0,#0x0    @ 0802bbb2 061c
    movs r1,#0x6    @ 0802bbb4 0621
    rsbs r1,r1,#0    @ 0802bbb6 4942
    add r9,r1                                @ 0802bbb8 8944
    cmp r6,#0x0                              @ 0802bbba 002e
    bgt LAB_0802bb92                         @ 0802bbbc e9dc
    movs r2,#0xc    @ 0802bbbe 0c22
    rsbs r2,r2,#0    @ 0802bbc0 5242
    add r9,r2                                @ 0802bbc2 9144
    cmp r7,#0x3                              @ 0802bbc4 032f
    bgt LAB_0802bc30                         @ 0802bbc6 33dc
    ldr r5, DAT_0802bc6c                     @ 0802bbc8 284d
    movs r4,#0x2    @ 0802bbca 0224
    rsbs r4,r4,#0    @ 0802bbcc 6442
    adds r0,r4,#0x0    @ 0802bbce 201c
    ldrb r1,[r5,#0x8]                        @ 0802bbd0 297a
    ands r0,r1    @ 0802bbd2 0840
    strb r0,[r5,#0x8]                        @ 0802bbd4 2872
    ldr r1, PTR_font_jp_base_table_0802bc70  @ 0802bbd6 2649
    lsls r0,r0,#0x1e    @ 0802bbd8 8007
    lsrs r0,r0,#0x1f    @ 0802bbda c00f
    lsls r0,r0,#0x2    @ 0802bbdc 8000
    adds r0,r0,r1    @ 0802bbde 4018
    ldr r0,[r0,#0x0]                         @ 0802bbe0 0068
    str r0,[r5,#0x4]                         @ 0802bbe2 6860
    ldr r0, DAT_0802bc60                     @ 0802bbe4 1e48
    adds r0,#0x64    @ 0802bbe6 6430
    ldrh r0,[r0,#0x0]                        @ 0802bbe8 0088
    .hword 0x4680    @ 0802bbea 8046
    ldr r0, DAT_0802bc68                     @ 0802bbec 1e48
    adds r0,r7,r0    @ 0802bbee 3818
    ldrb r6,[r0,#0x0]                        @ 0802bbf0 0678
    ldr r2, DAT_0802bc74                     @ 0802bbf2 204a
    adds r0,r7,r2    @ 0802bbf4 b818
    bl game_str_id_to_row                    @ 0802bbf6 c9f00ff9
    ldr r2, PTR_game_str_pointer_table_0802bc78 @ 0802bbfa 1f4a
    lsls r0,r0,#0x10    @ 0802bbfc 0004
    lsrs r0,r0,#0x10    @ 0802bbfe 000c
    lsls r1,r0,#0x1    @ 0802bc00 4100
    adds r1,r1,r0    @ 0802bc02 0918
    lsls r1,r1,#0x3    @ 0802bc04 c900
    adds r1,r1,r2    @ 0802bc06 8918
    ldr r3,[r1,#0x0]                         @ 0802bc08 0b68
    ldr r0, PTR_game_str_ja_0802bc7c         @ 0802bc0a 1c48
    adds r3,r3,r0    @ 0802bc0c 1b18
    .hword 0x4648    @ 0802bc0e 4846
    .hword 0x4641    @ 0802bc10 4146
    adds r2,r6,#0x0    @ 0802bc12 321c
    bl text_render_wrapper                   @ 0802bc14 c6f032ff
    ldr r1, DAT_0802bc80                     @ 0802bc18 1949
    ldr r0, DAT_0802bc84                     @ 0802bc1a 1a48
    adds r1,r1,r0    @ 0802bc1c 0918
    movs r0,#0x7    @ 0802bc1e 0720
    ldrb r1,[r1,#0x0]                        @ 0802bc20 0978
    ands r0,r1    @ 0802bc22 0840
    rsbs r0,r0,#0    @ 0802bc24 4042
    lsrs r0,r0,#0x1f    @ 0802bc26 c00f
    ldrb r1,[r5,#0x8]                        @ 0802bc28 297a
    ands r4,r1    @ 0802bc2a 0c40
    orrs r4,r0    @ 0802bc2c 0443
    strb r4,[r5,#0x8]                        @ 0802bc2e 2c72
LAB_0802bc30:
    ldr r2, DAT_0802bc60                     @ 0802bc30 0b4a
    adds r1,r2,#0x0    @ 0802bc32 111c
    adds r1,#0x64    @ 0802bc34 6431
    ldrh r0,[r1,#0x0]                        @ 0802bc36 0888
    adds r0,#0xc    @ 0802bc38 0c30
    strh r0,[r1,#0x0]                        @ 0802bc3a 0880
    adds r2,#0x6c    @ 0802bc3c 6c32
    ldrb r3,[r2,#0x0]                        @ 0802bc3e 1378
    lsls r1,r3,#0x1b    @ 0802bc40 d906
    lsrs r1,r1,#0x1b    @ 0802bc42 c90e
    adds r1,#0x1    @ 0802bc44 0131
    movs r0,#0x1f    @ 0802bc46 1f20
    ands r1,r0    @ 0802bc48 0140
    movs r0,#0x20    @ 0802bc4a 2020
    rsbs r0,r0,#0    @ 0802bc4c 4042
    ands r0,r3    @ 0802bc4e 1840
    orrs r0,r1    @ 0802bc50 0843
    strb r0,[r2,#0x0]                        @ 0802bc52 1070
LAB_0802bc54:
    pop {r3,r4}                              @ 0802bc54 18bc
    .hword 0x4698    @ 0802bc56 9846
    .hword 0x46a1    @ 0802bc58 a146
    pop {r4,r5,r6,r7}                        @ 0802bc5a f0bc
    pop {r0}                                 @ 0802bc5c 01bc
    bx r0                                    @ 0802bc5e 0047
DAT_0802bc60:
    .word  0x02023360                     @ 0802bc60 60330202
DAT_0802bc64:
    .word  0x020233c4                     @ 0802bc64 c4330202
DAT_0802bc68:
    .word  0x09e59da8                     @ 0802bc68 a89de509
DAT_0802bc6c:
    .word  0x02006ed0                     @ 0802bc6c d06e0002
PTR_font_jp_base_table_0802bc70:
    .word  font_jp_base_table             @ 0802bc70 54f8e509
DAT_0802bc74:
    .word  0x00000bfa                     @ 0802bc74 fa0b0000
PTR_game_str_pointer_table_0802bc78:
    .word  game_str_pointer_table         @ 0802bc78 400f0008
PTR_game_str_ja_0802bc7c:
    .word  game_str_ja                    @ 0802bc7c 109cdb09
DAT_0802bc80:
    .word  0x02000000                     @ 0802bc80 00000002
DAT_0802bc84:
    .word  0x00006c2c                     @ 0802bc84 2c6c0000

@ Variant of render_game_string_with_number (FUN_0802b940): main difference is that
@ text_render_wrapper is called with r2=6 (vs 7), representing a different render
@ mode/width parameter. r0=text_ptr (card data string), r1=digit_value (card attribute
@ value, from get_card_data_bit_by_index return). Writes to line buffer slot then renders
@ text; if digit_value > 9, performs decimal decomposition loop (render_glyph_jp_single_layer);
@ if <= 9, writes single character directly. Finally increments slot count bits[4:0]+1 and
@ writes back. Called by FUN_0801fec0 (full scene hub) and render_card_stats_to_line_buf.
@ 
@ Constants:
@ - gPrng+0xb6*2 = 0x16c (line buffer slot base)
@ - 0x02006ed0 = scene state region (halfword at +0xc, low 6 bits truncated)
@ - 0x3f mask = low 6 bits slot count
@ - r2=6 = render mode parameter (differs from render_game_string_with_number r2=7)
render_card_stat_with_number_alt:
    push {r4,r5,r6,r7,lr}                    @ 0802bc88 f0b5
    adds r3,r0,#0x0    @ 0802bc8a 031c
    adds r4,r1,#0x0    @ 0802bc8c 0c1c
    movs r7,#0xb6    @ 0802bc8e b627
    ldr r0, DAT_0802bd58                     @ 0802bc90 3148
    .hword 0x4684    @ 0802bc92 8446
    .hword 0x4662    @ 0802bc94 6246
    adds r2,#0x6c    @ 0802bc96 6c32
    ldrb r1,[r2,#0x0]                        @ 0802bc98 1178
    lsls r0,r1,#0x1b    @ 0802bc9a c806
    lsrs r0,r0,#0x19    @ 0802bc9c 400e
    .hword 0x4661    @ 0802bc9e 6146
    adds r1,#0x78    @ 0802bca0 7831
    adds r0,r0,r1    @ 0802bca2 4018
    str r4,[r0,#0x0]                         @ 0802bca4 0460
    ldrb r2,[r2,#0x0]                        @ 0802bca6 1278
    lsls r0,r2,#0x1b    @ 0802bca8 d006
    lsrs r0,r0,#0x1b    @ 0802bcaa c00e
    adds r1,#0x80    @ 0802bcac 8031
    adds r0,r0,r1    @ 0802bcae 4018
    movs r1,#0x0    @ 0802bcb0 0021
    strb r1,[r0,#0x0]                        @ 0802bcb2 0170
    ldr r6, DAT_0802bd5c                     @ 0802bcb4 294e
    movs r0,#0x3f    @ 0802bcb6 3f20
    ldrh r1,[r6,#0xc]                        @ 0802bcb8 b189
    ands r0,r1    @ 0802bcba 0840
    strh r0,[r6,#0xc]                        @ 0802bcbc b081
    .hword 0x4665    @ 0802bcbe 6546
    adds r5,#0x64    @ 0802bcc0 6435
    ldrh r1,[r5,#0x0]                        @ 0802bcc2 2988
    movs r0,#0x2    @ 0802bcc4 0220
    movs r2,#0x6    @ 0802bcc6 0622
    bl text_render_wrapper                   @ 0802bcc8 c6f0d8fe
    ldrh r1,[r6,#0xe]                        @ 0802bccc f189
    lsls r0,r1,#0x16    @ 0802bcce 8805
    lsrs r0,r0,#0x16    @ 0802bcd0 800d
    ldrh r1,[r5,#0x0]                        @ 0802bcd2 2988
    adds r1,#0xc    @ 0802bcd4 0c31
    cmp r0,r1                                @ 0802bcd6 8842
    ble LAB_0802bcdc                         @ 0802bcd8 00dd
    strh r1,[r5,#0x0]                        @ 0802bcda 2980
LAB_0802bcdc:
    movs r5,#0xb6    @ 0802bcdc b625
    adds r0,r4,#0x0    @ 0802bcde 201c
    cmp r4,#0x9                              @ 0802bce0 092c
    ble LAB_0802bcf0                         @ 0802bce2 05dd
LAB_0802bce4:
    movs r1,#0xa    @ 0802bce4 0a21
    bl __divsi3                              @ 0802bce6 e2f08dfc
    subs r5,#0x6    @ 0802bcea 063d
    cmp r0,#0x9                              @ 0802bcec 0928
    bgt LAB_0802bce4                         @ 0802bcee f9dc
LAB_0802bcf0:
    ldrh r6,[r6,#0xc]                        @ 0802bcf0 b689
    lsrs r0,r6,#0x6    @ 0802bcf2 b009
    cmp r5,r0                                @ 0802bcf4 8542
    bge LAB_0802bd02                         @ 0802bcf6 04da
    ldr r0, DAT_0802bd58                     @ 0802bcf8 1748
    adds r0,#0x64    @ 0802bcfa 6430
    ldrh r1,[r0,#0x0]                        @ 0802bcfc 0188
    adds r1,#0xc    @ 0802bcfe 0c31
    strh r1,[r0,#0x0]                        @ 0802bd00 0180
LAB_0802bd02:
    ldr r5, DAT_0802bd60                     @ 0802bd02 174d
LAB_0802bd04:
    adds r0,r4,#0x0    @ 0802bd04 201c
    movs r1,#0xa    @ 0802bd06 0a21
    bl __modsi3                              @ 0802bd08 e2f0c8fc
    adds r0,#0x30    @ 0802bd0c 3030
    lsls r0,r0,#0x18    @ 0802bd0e 0006
    lsrs r0,r0,#0x18    @ 0802bd10 000e
    ldrh r2,[r5,#0x0]                        @ 0802bd12 2a88
    adds r1,r7,#0x0    @ 0802bd14 391c
    movs r3,#0x7    @ 0802bd16 0723
    bl render_glyph_jp_single_layer          @ 0802bd18 c5f044fe
    adds r0,r4,#0x0    @ 0802bd1c 201c
    movs r1,#0xa    @ 0802bd1e 0a21
    bl __divsi3                              @ 0802bd20 e2f070fc
    adds r4,r0,#0x0    @ 0802bd24 041c
    subs r7,#0x6    @ 0802bd26 063f
    cmp r4,#0x0                              @ 0802bd28 002c
    bgt LAB_0802bd04                         @ 0802bd2a ebdc
    ldr r2, DAT_0802bd58                     @ 0802bd2c 0a4a
    adds r1,r2,#0x0    @ 0802bd2e 111c
    adds r1,#0x64    @ 0802bd30 6431
    ldrh r0,[r1,#0x0]                        @ 0802bd32 0888
    adds r0,#0xc    @ 0802bd34 0c30
    strh r0,[r1,#0x0]                        @ 0802bd36 0880
    adds r2,#0x6c    @ 0802bd38 6c32
    ldrb r3,[r2,#0x0]                        @ 0802bd3a 1378
    lsls r1,r3,#0x1b    @ 0802bd3c d906
    lsrs r1,r1,#0x1b    @ 0802bd3e c90e
    adds r1,#0x1    @ 0802bd40 0131
    movs r0,#0x1f    @ 0802bd42 1f20
    ands r1,r0    @ 0802bd44 0140
    movs r0,#0x20    @ 0802bd46 2020
    rsbs r0,r0,#0    @ 0802bd48 4042
    ands r0,r3    @ 0802bd4a 1840
    orrs r0,r1    @ 0802bd4c 0843
    strb r0,[r2,#0x0]                        @ 0802bd4e 1070
    pop {r4,r5,r6,r7}                        @ 0802bd50 f0bc
    pop {r0}                                 @ 0802bd52 01bc
    bx r0                                    @ 0802bd54 0047
    .zero  0x2
DAT_0802bd58:
    .word  0x02023360                     @ 0802bd58 60330202
DAT_0802bd5c:
    .word  0x02006ed0                     @ 0802bd5c d06e0002
DAT_0802bd60:
    .word  0x020233c4                     @ 0802bd60 c4330202

@ Utility function to clear a sprite VRAM region and write sequential tile index sequence, called by FUN_0801fec0 (duel_puzzle main loop) and run_campaign_step30_pack_card_info_display (0x080277a4) during card name display init. First zero_fill_by_halfword at 0x06008020 (0xfc<<7=0x7e00 halfwords = 0xff00 bytes), then commit_line_buffer_to_sprite_vram(0x06008020, 0) to commit empty line buffer. Then loops from row=0 to row=41 (0x29): for each row writes 2 halfwords = 0x0000 prefix, then 24 consecutive tile indices (starting at r6=1 incrementing), then 5 halfwords = 0x0000 suffix. Total 0x2a rows (42 rows).
@ 
@ Constants:
@ - sprite VRAM target = 0x06008020
@ - tilemap scratch = 0x06001440
@ - zero_fill size = 0xfc<<7 = 0x7e00 halfwords
@ - tile seq start = 1
@ - tile seq len per row = 24 tiles (0x17+1)
@ - zero prefix per row = 2 halfwords
@ - zero suffix per row = 5 halfwords
@ - row count = 0x2a = 42 rows
zero_sprite_vram_with_tile_seq:
    push {r4,r5,r6,lr}                       @ 0802bd64 70b5
    movs r6,#0x1    @ 0802bd66 0126
    ldr r5, DAT_0802bdbc                     @ 0802bd68 144d
    ldr r4, DAT_0802bdc0                     @ 0802bd6a 154c
    movs r1,#0xfc    @ 0802bd6c fc21
    lsls r1,r1,#0x7    @ 0802bd6e c901
    adds r0,r4,#0x0    @ 0802bd70 201c
    bl zero_fill_by_halfword                 @ 0802bd72 c9f07ff8
    adds r0,r4,#0x0    @ 0802bd76 201c
    movs r1,#0x0    @ 0802bd78 0021
    bl commit_line_buffer_to_sprite_vram     @ 0802bd7a c7f067f8
    movs r0,#0x0    @ 0802bd7e 0020
    movs r3,#0x0    @ 0802bd80 0023
LAB_0802bd82:
    adds r2,r0,#0x1    @ 0802bd82 421c
    movs r1,#0x2    @ 0802bd84 0221
LAB_0802bd86:
    strh r3,[r5,#0x0]                        @ 0802bd86 2b80
    adds r5,#0x2    @ 0802bd88 0235
    subs r1,#0x1    @ 0802bd8a 0139
    cmp r1,#0x0                              @ 0802bd8c 0029
    bge LAB_0802bd86                         @ 0802bd8e fada
    movs r1,#0x17    @ 0802bd90 1721
LAB_0802bd92:
    strh r6,[r5,#0x0]                        @ 0802bd92 2e80
    adds r5,#0x2    @ 0802bd94 0235
    adds r0,r6,#0x1    @ 0802bd96 701c
    lsls r0,r0,#0x10    @ 0802bd98 0004
    lsrs r6,r0,#0x10    @ 0802bd9a 060c
    subs r1,#0x1    @ 0802bd9c 0139
    cmp r1,#0x0                              @ 0802bd9e 0029
    bge LAB_0802bd92                         @ 0802bda0 f7da
    movs r0,#0x0    @ 0802bda2 0020
    movs r1,#0x4    @ 0802bda4 0421
LAB_0802bda6:
    strh r0,[r5,#0x0]                        @ 0802bda6 2880
    adds r5,#0x2    @ 0802bda8 0235
    subs r1,#0x1    @ 0802bdaa 0139
    cmp r1,#0x0                              @ 0802bdac 0029
    bge LAB_0802bda6                         @ 0802bdae fada
    adds r0,r2,#0x0    @ 0802bdb0 101c
    cmp r0,#0x29                             @ 0802bdb2 2928
    ble LAB_0802bd82                         @ 0802bdb4 e5dd
    pop {r4,r5,r6}                           @ 0802bdb6 70bc
    pop {r0}                                 @ 0802bdb8 01bc
    bx r0                                    @ 0802bdba 0047
DAT_0802bdbc:
    .word  0x06001440                     @ 0802bdbc 40140006
DAT_0802bdc0:
    .word  0x06008020                     @ 0802bdc0 20800006

@ Per-frame tick: advances LP digit sprite display and blend step. Called by run_campaign_step31_duel_lp_fadein_tick (0x08027834) and FUN_0801fec0 (duel_puzzle main loop). Calls render_puzzle_lp_digit_sprites to refresh OAM; ORs DISPCNT shadow with 0xf8*32=0x1f00 to set sprite display mode bits; calls tick_blend_step_by_delta(4) to advance blend fade. Returns tick_blend_step_by_delta result (0=fade in progress, nonzero=done) via pop {r1}; bx r1 (pattern B). Caller checks cmp r0,#0; bne to decide whether to keep waiting.
@ 
@ Constants:
@ - DISPCNT_shadow=0x80*32*0x13 (base area)
@ - sprite_mode_mask=0xf8*32=0x1f00 (DISPCNT bits for sprite enable)
@ - blend_delta=4
tick_lp_display_and_blend_step:
    push {lr}                                @ 0802bdc4 00b5
    bl render_puzzle_lp_digit_sprites        @ 0802bdc6 fff745fd
    movs r2,#0x80    @ 0802bdca 8022
    lsls r2,r2,#0x13    @ 0802bdcc d204
    ldrh r0,[r2,#0x0]                        @ 0802bdce 1088
    movs r3,#0xf8    @ 0802bdd0 f823
    lsls r3,r3,#0x5    @ 0802bdd2 5b01
    adds r1,r3,#0x0    @ 0802bdd4 191c
    orrs r0,r1    @ 0802bdd6 0843
    strh r0,[r2,#0x0]                        @ 0802bdd8 1080
    movs r0,#0x4    @ 0802bdda 0420
    bl tick_blend_step_by_delta              @ 0802bddc c9f06cfd
    pop {r1}                                 @ 0802bde0 02bc
    bx r1                                    @ 0802bde2 0847

@ Per-frame tick: advances LP digit sprite display and checks fadein completion. Called by run_campaign_step33_duel_reward_and_fadein_tick (0x080278c0) and FUN_0801fec0 (duel_puzzle main loop). Calls render_puzzle_lp_digit_sprites to refresh OAM; calls start_blend_fadein_with_target(4) to advance fadein. If fadein returns 0 (not done) returns 0; if done clears DISPCNT shadow (strh 0 at 0x04000400) and returns 1. Differs from tick_lp_display_and_blend_step: uses start_blend_fadein_with_target (with target detection) instead of tick_blend_step_by_delta (no target check), so it actively clears DISPCNT shadow on completion.
@ 
@ Constants:
@ - fadein_target=4
@ - DISPCNT_shadow_clear=0x80*32*0x13=0x04000000 (strh 0)
tick_lp_display_and_fadein_check:
    push {lr}                                @ 0802bde4 00b5
    bl render_puzzle_lp_digit_sprites        @ 0802bde6 fff735fd
    movs r0,#0x4    @ 0802bdea 0420
    bl start_blend_fadein_with_target        @ 0802bdec c9f028fd
    cmp r0,#0x0                              @ 0802bdf0 0028
    bne LAB_0802bdf8                         @ 0802bdf2 01d1
    movs r0,#0x0    @ 0802bdf4 0020
    b LAB_0802be02                           @ 0802bdf6 04e0
LAB_0802bdf8:
    movs r1,#0x80    @ 0802bdf8 8021
    lsls r1,r1,#0x13    @ 0802bdfa c904
    movs r0,#0x0    @ 0802bdfc 0020
    strh r0,[r1,#0x0]                        @ 0802bdfe 0880
    movs r0,#0x1    @ 0802be00 0120
LAB_0802be02:
    pop {r1}                                 @ 0802be02 02bc
    bx r1                                    @ 0802be04 0847
    .zero  0x2

@ duel_puzzle scene display mode dispatch function, called by FUN_0801fec0 (duel_puzzle main loop) and run_campaign_step32_puzzle_display_tick (0x08027888). First calls render_puzzle_lp_digit_sprites to update LP digit OAM. Then reads one byte from gPrng+0x204, extracts bits[7:6] (2-bit high-priority mode r2) and bits[5:0]&0x3f (low 6-bit base mode field, shifted left 2), combines into mode_key = (byte&0x3f)<<2 | byte>>6, dispatches r0 to four paths: case 0 -> LAB_0802be58, case 1 -> LAB_0802be8e, case >1 -> LAB_0802be48, default -> LAB_0802c1a4.
@ 
@ Constants:
@ - mode byte = gPrng+0x204 (gPrng+0x81*4)
@ - mode_key = ((byte & 0x3f) << 2) | (byte >> 6); enum [0..3]
@ - case 0 = LAB_0802be58
@ - case 1 = LAB_0802be8e
@ - case >1 (bgt) = LAB_0802be48
@ - default = LAB_0802c1a4
@ - returns 0 = scene not ready/waiting, 1 = scene advanced (caller FUN_08027888 checks cmp r0,#0 -> bne)
dispatch_puzzle_display_mode:
    push {r4,r5,r6,r7,lr}                    @ 0802be08 f0b5
    .hword 0x464f    @ 0802be0a 4f46
    .hword 0x4646    @ 0802be0c 4646
    push {r6,r7}                             @ 0802be0e c0b4
    bl render_puzzle_lp_digit_sprites        @ 0802be10 fff720fd
    ldr r0, PTR_gPrng_0802be40               @ 0802be14 0a48
    ldr r1, DAT_0802be44                     @ 0802be16 0b49
    adds r6,r0,r1    @ 0802be18 4618
    ldrb r5,[r6,#0x0]                        @ 0802be1a 3578
    lsrs r2,r5,#0x6    @ 0802be1c aa09
    movs r3,#0x81    @ 0802be1e 8123
    lsls r3,r3,#0x2    @ 0802be20 9b00
    adds r4,r0,r3    @ 0802be22 c418
    movs r3,#0x3f    @ 0802be24 3f23
    adds r0,r3,#0x0    @ 0802be26 181c
    ldrb r7,[r4,#0x0]                        @ 0802be28 2778
    ands r0,r7    @ 0802be2a 3840
    lsls r0,r0,#0x2    @ 0802be2c 8000
    orrs r0,r2    @ 0802be2e 1043
    cmp r0,#0x1                              @ 0802be30 0128
    beq LAB_0802be8e                         @ 0802be32 2cd0
    cmp r0,#0x1                              @ 0802be34 0128
    bgt LAB_0802be48                         @ 0802be36 07dc
    cmp r0,#0x0                              @ 0802be38 0028
    beq LAB_0802be58                         @ 0802be3a 0dd0
    b LAB_0802c1a4                           @ 0802be3c b2e1
    .zero  0x2
PTR_gPrng_0802be40:
    .word  gPrng                          @ 0802be40 40000003
DAT_0802be44:
    .word  0x00000203                     @ 0802be44 03020000
LAB_0802be48:
    ldr r1, DAT_0802be54                     @ 0802be48 0249
    .hword 0x4688    @ 0802be4a 8846
    cmp r0,#0x2                              @ 0802be4c 0228
    bne LAB_0802be52                         @ 0802be4e 00d1
    b LAB_0802bfa4                           @ 0802be50 a8e0
LAB_0802be52:
    b LAB_0802c1a4                           @ 0802be52 a7e1
DAT_0802be54:
    .word  0x02023360                     @ 0802be54 60330202
LAB_0802be58:
    ldr r1, DAT_0802bf14                     @ 0802be58 2e49
    adds r1,#0x6c    @ 0802be5a 6c31
    ldr r0, DAT_0802bf18                     @ 0802be5c 2e48
    ldrh r7,[r1,#0x0]                        @ 0802be5e 0f88
    ands r0,r7    @ 0802be60 3840
    strh r0,[r1,#0x0]                        @ 0802be62 0880
    adds r1,r3,#0x0    @ 0802be64 191c
    ldrb r0,[r4,#0x0]                        @ 0802be66 2078
    ands r1,r0    @ 0802be68 0140
    lsls r1,r1,#0x2    @ 0802be6a 8900
    orrs r1,r2    @ 0802be6c 1143
    adds r1,#0x1    @ 0802be6e 0131
    movs r2,#0x3    @ 0802be70 0322
    ands r2,r1    @ 0802be72 0a40
    lsls r2,r2,#0x6    @ 0802be74 9201
    adds r0,r3,#0x0    @ 0802be76 181c
    ands r0,r5    @ 0802be78 2840
    orrs r0,r2    @ 0802be7a 1043
    strb r0,[r6,#0x0]                        @ 0802be7c 3070
    lsrs r1,r1,#0x2    @ 0802be7e 8908
    ands r1,r3    @ 0802be80 1940
    movs r0,#0x40    @ 0802be82 4020
    rsbs r0,r0,#0    @ 0802be84 4042
    ldrb r2,[r4,#0x0]                        @ 0802be86 2278
    ands r0,r2    @ 0802be88 1040
    orrs r0,r1    @ 0802be8a 0843
    strb r0,[r4,#0x0]                        @ 0802be8c 2070
LAB_0802be8e:
    ldr r2, DAT_0802bf14                     @ 0802be8e 214a
    adds r3,r2,#0x0    @ 0802be90 131c
    adds r3,#0x6c    @ 0802be92 6c33
    ldrh r4,[r3,#0x0]                        @ 0802be94 1c88
    lsls r0,r4,#0x16    @ 0802be96 a005
    lsrs r1,r0,#0x1b    @ 0802be98 c10e
    ldrb r7,[r3,#0x0]                        @ 0802be9a 1f78
    lsls r0,r7,#0x1b    @ 0802be9c f806
    lsrs r0,r0,#0x1b    @ 0802be9e c00e
    .hword 0x4690    @ 0802bea0 9046
    cmp r1,r0                                @ 0802bea2 8142
    blt LAB_0802bf24                         @ 0802bea4 3edb
    ldr r4, PTR_gPrng_0802bf1c               @ 0802bea6 1d4c
    ldr r0, DAT_0802bf20                     @ 0802bea8 1d48
    adds r0,r0,r4    @ 0802beaa 0019
    .hword 0x4681    @ 0802beac 8146
    ldrb r2,[r0,#0x0]                        @ 0802beae 0278
    lsrs r1,r2,#0x6    @ 0802beb0 9109
    movs r3,#0x81    @ 0802beb2 8123
    lsls r3,r3,#0x2    @ 0802beb4 9b00
    adds r4,r4,r3    @ 0802beb6 e418
    movs r5,#0x3f    @ 0802beb8 3f25
    adds r0,r5,#0x0    @ 0802beba 281c
    ldrb r7,[r4,#0x0]                        @ 0802bebc 2778
    ands r0,r7    @ 0802bebe 3840
    lsls r0,r0,#0x2    @ 0802bec0 8000
    orrs r0,r1    @ 0802bec2 0843
    adds r0,#0x1    @ 0802bec4 0130
    movs r1,#0x3    @ 0802bec6 0321
    .hword 0x4688    @ 0802bec8 8846
    adds r1,r0,#0x0    @ 0802beca 011c
    .hword 0x4643    @ 0802becc 4346
    ands r1,r3    @ 0802bece 1940
    lsls r1,r1,#0x6    @ 0802bed0 8901
    adds r3,r5,#0x0    @ 0802bed2 2b1c
    ands r3,r2    @ 0802bed4 1340
    orrs r3,r1    @ 0802bed6 0b43
    lsrs r0,r0,#0x2    @ 0802bed8 8008
    ands r0,r5    @ 0802beda 2840
    movs r6,#0x40    @ 0802bedc 4026
    rsbs r6,r6,#0    @ 0802bede 7642
    adds r2,r6,#0x0    @ 0802bee0 321c
    ands r2,r7    @ 0802bee2 3a40
    orrs r2,r0    @ 0802bee4 0243
    strb r2,[r4,#0x0]                        @ 0802bee6 2270
    lsls r1,r3,#0x18    @ 0802bee8 1906
    lsrs r1,r1,#0x1e    @ 0802beea 890f
    adds r0,r5,#0x0    @ 0802beec 281c
    ands r0,r2    @ 0802beee 1040
    lsls r0,r0,#0x2    @ 0802bef0 8000
    orrs r0,r1    @ 0802bef2 0843
    adds r0,#0x1    @ 0802bef4 0130
    adds r1,r0,#0x0    @ 0802bef6 011c
    .hword 0x4647    @ 0802bef8 4746
    ands r1,r7    @ 0802befa 3940
    lsls r1,r1,#0x6    @ 0802befc 8901
    ands r3,r5    @ 0802befe 2b40
    orrs r3,r1    @ 0802bf00 0b43
    .hword 0x4649    @ 0802bf02 4946
    strb r3,[r1,#0x0]                        @ 0802bf04 0b70
    lsrs r0,r0,#0x2    @ 0802bf06 8008
    ands r0,r5    @ 0802bf08 2840
    ands r2,r6    @ 0802bf0a 3240
    orrs r2,r0    @ 0802bf0c 0243
    strb r2,[r4,#0x0]                        @ 0802bf0e 2270
    b LAB_0802c228                           @ 0802bf10 8ae1
    .zero  0x2
DAT_0802bf14:
    .word  0x02023360                     @ 0802bf14 60330202
DAT_0802bf18:
    .word  0xfffffc1f                     @ 0802bf18 1ffcffff
PTR_gPrng_0802bf1c:
    .word  gPrng                          @ 0802bf1c 40000003
DAT_0802bf20:
    .word  0x00000203                     @ 0802bf20 03020000
LAB_0802bf24:
    lsls r0,r1,#0x2    @ 0802bf24 8800
    .hword 0x4641    @ 0802bf26 4146
    adds r1,#0x78    @ 0802bf28 7831
    adds r0,r0,r1    @ 0802bf2a 4018
    ldr r0,[r0,#0x0]                         @ 0802bf2c 0068
    .hword 0x4642    @ 0802bf2e 4246
    str r0,[r2,#0x74]                        @ 0802bf30 5067
    ldrh r4,[r3,#0x0]                        @ 0802bf32 1c88
    lsls r0,r4,#0x16    @ 0802bf34 a005
    lsrs r0,r0,#0x1b    @ 0802bf36 c00e
    adds r1,#0x80    @ 0802bf38 8031
    adds r0,r0,r1    @ 0802bf3a 4018
    adds r2,#0x6d    @ 0802bf3c 6d32
    movs r1,#0x7    @ 0802bf3e 0721
    ldrb r0,[r0,#0x0]                        @ 0802bf40 0078
    ands r1,r0    @ 0802bf42 0140
    lsls r1,r1,#0x2    @ 0802bf44 8900
    movs r0,#0x1d    @ 0802bf46 1d20
    rsbs r0,r0,#0    @ 0802bf48 4042
    ldrb r7,[r2,#0x0]                        @ 0802bf4a 1778
    ands r0,r7    @ 0802bf4c 3840
    orrs r0,r1    @ 0802bf4e 0843
    strb r0,[r2,#0x0]                        @ 0802bf50 1070
    ldrh r2,[r3,#0x0]                        @ 0802bf52 1a88
    lsls r1,r2,#0x16    @ 0802bf54 9105
    lsrs r1,r1,#0x1b    @ 0802bf56 c90e
    adds r1,#0x1    @ 0802bf58 0131
    movs r0,#0x1f    @ 0802bf5a 1f20
    ands r1,r0    @ 0802bf5c 0140
    lsls r1,r1,#0x5    @ 0802bf5e 4901
    ldr r0, DAT_0802bfe4                     @ 0802bf60 2048
    ands r0,r2    @ 0802bf62 1040
    orrs r0,r1    @ 0802bf64 0843
    strh r0,[r3,#0x0]                        @ 0802bf66 1880
    ldr r3, PTR_gPrng_0802bfe8               @ 0802bf68 1f4b
    ldr r0, DAT_0802bfec                     @ 0802bf6a 2048
    adds r6,r3,r0    @ 0802bf6c 1e18
    ldrb r5,[r6,#0x0]                        @ 0802bf6e 3578
    lsrs r0,r5,#0x6    @ 0802bf70 a809
    movs r1,#0x81    @ 0802bf72 8121
    lsls r1,r1,#0x2    @ 0802bf74 8900
    adds r3,r3,r1    @ 0802bf76 5b18
    movs r4,#0x3f    @ 0802bf78 3f24
    adds r1,r4,#0x0    @ 0802bf7a 211c
    ldrb r2,[r3,#0x0]                        @ 0802bf7c 1a78
    ands r1,r2    @ 0802bf7e 1140
    lsls r1,r1,#0x2    @ 0802bf80 8900
    orrs r1,r0    @ 0802bf82 0143
    adds r1,#0x1    @ 0802bf84 0131
    movs r2,#0x3    @ 0802bf86 0322
    ands r2,r1    @ 0802bf88 0a40
    lsls r2,r2,#0x6    @ 0802bf8a 9201
    adds r0,r4,#0x0    @ 0802bf8c 201c
    ands r0,r5    @ 0802bf8e 2840
    orrs r0,r2    @ 0802bf90 1043
    strb r0,[r6,#0x0]                        @ 0802bf92 3070
    lsrs r1,r1,#0x2    @ 0802bf94 8908
    ands r1,r4    @ 0802bf96 2140
    movs r0,#0x40    @ 0802bf98 4020
    rsbs r0,r0,#0    @ 0802bf9a 4042
    ldrb r4,[r3,#0x0]                        @ 0802bf9c 1c78
    ands r0,r4    @ 0802bf9e 2040
    orrs r0,r1    @ 0802bfa0 0843
    strb r0,[r3,#0x0]                        @ 0802bfa2 1870
LAB_0802bfa4:
    ldr r1, PTR_gPrng_0802bfe8               @ 0802bfa4 1049
    movs r7,#0xa3    @ 0802bfa6 a327
    lsls r7,r7,#0x1    @ 0802bfa8 7f00
    adds r3,r1,r7    @ 0802bfaa cb19
    movs r0,#0x2    @ 0802bfac 0220
    ldrh r3,[r3,#0x0]                        @ 0802bfae 1b88
    ands r0,r3    @ 0802bfb0 1840
    adds r4,r1,#0x0    @ 0802bfb2 0c1c
    cmp r0,#0x0                              @ 0802bfb4 0028
    beq LAB_0802c070                         @ 0802bfb6 5bd0
    .hword 0x4640    @ 0802bfb8 4046
    adds r0,#0x6c    @ 0802bfba 6c30
    ldrh r0,[r0,#0x0]                        @ 0802bfbc 0088
    lsls r0,r0,#0x16    @ 0802bfbe 8005
    lsrs r0,r0,#0x1b    @ 0802bfc0 c00e
    lsls r1,r0,#0x1    @ 0802bfc2 4100
    adds r1,r1,r0    @ 0802bfc4 0918
    lsls r1,r1,#0x2    @ 0802bfc6 8900
    .hword 0x4640    @ 0802bfc8 4046
    adds r0,#0x62    @ 0802bfca 6230
    strh r1,[r0,#0x0]                        @ 0802bfcc 0180
    adds r0,#0xb    @ 0802bfce 0b30
    ldrb r0,[r0,#0x0]                        @ 0802bfd0 0078
    lsls r0,r0,#0x1b    @ 0802bfd2 c006
    lsrs r0,r0,#0x1d    @ 0802bfd4 400f
    cmp r0,#0x1                              @ 0802bfd6 0128
    beq LAB_0802c004                         @ 0802bfd8 14d0
    cmp r0,#0x1                              @ 0802bfda 0128
    bgt LAB_0802bff0                         @ 0802bfdc 08dc
    cmp r0,#0x0                              @ 0802bfde 0028
    beq LAB_0802bffa                         @ 0802bfe0 0bd0
    b LAB_0802c02a                           @ 0802bfe2 22e0
DAT_0802bfe4:
    .word  0xfffffc1f                     @ 0802bfe4 1ffcffff
PTR_gPrng_0802bfe8:
    .word  gPrng                          @ 0802bfe8 40000003
DAT_0802bfec:
    .word  0x00000203                     @ 0802bfec 03020000
LAB_0802bff0:
    cmp r0,#0x2                              @ 0802bff0 0228
    beq LAB_0802c010                         @ 0802bff2 0dd0
    cmp r0,#0x3                              @ 0802bff4 0328
    beq LAB_0802c01c                         @ 0802bff6 11d0
    b LAB_0802c02a                           @ 0802bff8 17e0
LAB_0802bffa:
    .hword 0x4641    @ 0802bffa 4146
    ldr r0,[r1,#0x68]                        @ 0802bffc 886e
    ldr r1,[r1,#0x74]                        @ 0802bffe 496f
    adds r0,r0,r1    @ 0802c000 4018
    b LAB_0802c026                           @ 0802c002 10e0
LAB_0802c004:
    .hword 0x4643    @ 0802c004 4346
    ldr r0,[r3,#0x68]                        @ 0802c006 986e
    ldr r1,[r3,#0x74]                        @ 0802c008 596f
    subs r0,r0,r1    @ 0802c00a 401a
    str r0,[r3,#0x68]                        @ 0802c00c 9866
    b LAB_0802c02a                           @ 0802c00e 0ce0
LAB_0802c010:
    .hword 0x4647    @ 0802c010 4746
    ldr r0,[r7,#0x68]                        @ 0802c012 b86e
    ldr r1,[r7,#0x74]                        @ 0802c014 796f
    muls r0,r1    @ 0802c016 4843
    str r0,[r7,#0x68]                        @ 0802c018 b866
    b LAB_0802c02a                           @ 0802c01a 06e0
LAB_0802c01c:
    .hword 0x4641    @ 0802c01c 4146
    ldr r0,[r1,#0x68]                        @ 0802c01e 886e
    ldr r1,[r1,#0x74]                        @ 0802c020 496f
    bl __udivsi3                             @ 0802c022 e2f0dbfb
LAB_0802c026:
    .hword 0x4642    @ 0802c026 4246
    str r0,[r2,#0x68]                        @ 0802c028 9066
LAB_0802c02a:
    ldr r3, DAT_0802c06c                     @ 0802c02a 104b
    adds r6,r4,r3    @ 0802c02c e618
    ldrb r5,[r6,#0x0]                        @ 0802c02e 3578
    lsrs r0,r5,#0x6    @ 0802c030 a809
    movs r7,#0x81    @ 0802c032 8127
    lsls r7,r7,#0x2    @ 0802c034 bf00
    adds r4,r4,r7    @ 0802c036 e419
    movs r3,#0x3f    @ 0802c038 3f23
    adds r1,r3,#0x0    @ 0802c03a 191c
    ldrb r2,[r4,#0x0]                        @ 0802c03c 2278
    ands r1,r2    @ 0802c03e 1140
    lsls r1,r1,#0x2    @ 0802c040 8900
    orrs r1,r0    @ 0802c042 0143
    subs r1,#0x1    @ 0802c044 0139
    lsls r1,r1,#0x10    @ 0802c046 0904
    lsrs r2,r1,#0x10    @ 0802c048 0a0c
    movs r0,#0x3    @ 0802c04a 0320
    ands r2,r0    @ 0802c04c 0240
    lsls r2,r2,#0x6    @ 0802c04e 9201
    adds r0,r3,#0x0    @ 0802c050 181c
    ands r0,r5    @ 0802c052 2840
    orrs r0,r2    @ 0802c054 1043
    strb r0,[r6,#0x0]                        @ 0802c056 3070
    lsrs r1,r1,#0x12    @ 0802c058 890c
    ands r1,r3    @ 0802c05a 1940
    movs r0,#0x40    @ 0802c05c 4020
    rsbs r0,r0,#0    @ 0802c05e 4042
    ldrb r3,[r4,#0x0]                        @ 0802c060 2378
    ands r0,r3    @ 0802c062 1840
    orrs r0,r1    @ 0802c064 0843
    strb r0,[r4,#0x0]                        @ 0802c066 2070
    b LAB_0802c228                           @ 0802c068 dee0
    .zero  0x2
DAT_0802c06c:
    .word  0x00000203                     @ 0802c06c 03020000
LAB_0802c070:
    .hword 0x4643    @ 0802c070 4346
    adds r3,#0x62    @ 0802c072 6233
    ldrh r2,[r3,#0x0]                        @ 0802c074 1a88
    .hword 0x4640    @ 0802c076 4046
    adds r0,#0x6c    @ 0802c078 6c30
    ldrh r0,[r0,#0x0]                        @ 0802c07a 0088
    lsls r1,r0,#0x16    @ 0802c07c 8105
    lsrs r1,r1,#0x1b    @ 0802c07e c90e
    lsls r0,r1,#0x1    @ 0802c080 4800
    adds r0,r0,r1    @ 0802c082 4018
    lsls r0,r0,#0x2    @ 0802c084 8000
    cmp r2,r0                                @ 0802c086 8242
    bge LAB_0802c090                         @ 0802c088 02da
    adds r0,r2,#0x4    @ 0802c08a 101d
    strh r0,[r3,#0x0]                        @ 0802c08c 1880
    b LAB_0802c228                           @ 0802c08e cbe0
LAB_0802c090:
    .hword 0x4640    @ 0802c090 4046
    adds r0,#0x6d    @ 0802c092 6d30
    ldrb r0,[r0,#0x0]                        @ 0802c094 0078
    lsls r0,r0,#0x1b    @ 0802c096 c006
    lsrs r0,r0,#0x1d    @ 0802c098 400f
    cmp r0,#0x1                              @ 0802c09a 0128
    beq LAB_0802c136                         @ 0802c09c 4bd0
    cmp r0,#0x1                              @ 0802c09e 0128
    bgt LAB_0802c0a8                         @ 0802c0a0 02dc
    cmp r0,#0x0                              @ 0802c0a2 0028
    beq LAB_0802c0b2                         @ 0802c0a4 05d0
    b LAB_0802c15a                           @ 0802c0a6 58e0
LAB_0802c0a8:
    cmp r0,#0x2                              @ 0802c0a8 0228
    beq LAB_0802c142                         @ 0802c0aa 4ad0
    cmp r0,#0x3                              @ 0802c0ac 0328
    beq LAB_0802c14e                         @ 0802c0ae 4ed0
    b LAB_0802c15a                           @ 0802c0b0 53e0
LAB_0802c0b2:
    movs r0,#0x0    @ 0802c0b2 0020
    bl sync_state_and_init_sprite            @ 0802c0b4 cdf0fefc
    .hword 0x4644    @ 0802c0b8 4446
    ldr r1,[r4,#0x74]                        @ 0802c0ba 616f
    ldr r0, DAT_0802c0d4                     @ 0802c0bc 0548
    cmp r1,r0                                @ 0802c0be 8142
    ble LAB_0802c0dc                         @ 0802c0c0 0cdd
    ldr r7, DAT_0802c0d8                     @ 0802c0c2 054f
    adds r0,r1,r7    @ 0802c0c4 c819
    str r0,[r4,#0x74]                        @ 0802c0c6 6067
    ldr r0,[r4,#0x68]                        @ 0802c0c8 a06e
    ldr r1, DAT_0802c0d4                     @ 0802c0ca 0249
    adds r0,r0,r1    @ 0802c0cc 4018
    str r0,[r4,#0x68]                        @ 0802c0ce a066
    b LAB_0802c228                           @ 0802c0d0 aae0
    .zero  0x2
DAT_0802c0d4:
    .word  0x00002710                     @ 0802c0d4 10270000
DAT_0802c0d8:
    .word  0xffffd8f0                     @ 0802c0d8 f0d8ffff
LAB_0802c0dc:
    movs r0,#0xfa    @ 0802c0dc fa20
    lsls r0,r0,#0x2    @ 0802c0de 8000
    cmp r1,r0                                @ 0802c0e0 8142
    ble LAB_0802c0fc                         @ 0802c0e2 0bdd
    ldr r2, DAT_0802c0f8                     @ 0802c0e4 044a
    adds r0,r1,r2    @ 0802c0e6 8818
    .hword 0x4643    @ 0802c0e8 4346
    str r0,[r3,#0x74]                        @ 0802c0ea 5867
    ldr r0,[r3,#0x68]                        @ 0802c0ec 986e
    movs r4,#0xfa    @ 0802c0ee fa24
    lsls r4,r4,#0x2    @ 0802c0f0 a400
    adds r0,r0,r4    @ 0802c0f2 0019
    str r0,[r3,#0x68]                        @ 0802c0f4 9866
    b LAB_0802c228                           @ 0802c0f6 97e0
DAT_0802c0f8:
    .word  0xfffffc18                     @ 0802c0f8 18fcffff
LAB_0802c0fc:
    cmp r1,#0x64                             @ 0802c0fc 6429
    ble LAB_0802c110                         @ 0802c0fe 07dd
    adds r0,r1,#0x0    @ 0802c100 081c
    subs r0,#0x64    @ 0802c102 6438
    .hword 0x4647    @ 0802c104 4746
    str r0,[r7,#0x74]                        @ 0802c106 7867
    ldr r0,[r7,#0x68]                        @ 0802c108 b86e
    adds r0,#0x64    @ 0802c10a 6430
    str r0,[r7,#0x68]                        @ 0802c10c b866
    b LAB_0802c228                           @ 0802c10e 8be0
LAB_0802c110:
    cmp r1,#0xa                              @ 0802c110 0a29
    ble LAB_0802c124                         @ 0802c112 07dd
    adds r0,r1,#0x0    @ 0802c114 081c
    subs r0,#0xa    @ 0802c116 0a38
    .hword 0x4641    @ 0802c118 4146
    str r0,[r1,#0x74]                        @ 0802c11a 4867
    ldr r0,[r1,#0x68]                        @ 0802c11c 886e
    adds r0,#0xa    @ 0802c11e 0a30
    str r0,[r1,#0x68]                        @ 0802c120 8866
    b LAB_0802c228                           @ 0802c122 81e0
LAB_0802c124:
    cmp r1,#0x0                              @ 0802c124 0029
    ble LAB_0802c15a                         @ 0802c126 18dd
    subs r0,r1,#0x1    @ 0802c128 481e
    .hword 0x4642    @ 0802c12a 4246
    str r0,[r2,#0x74]                        @ 0802c12c 5067
    ldr r0,[r2,#0x68]                        @ 0802c12e 906e
    adds r0,#0x1    @ 0802c130 0130
    str r0,[r2,#0x68]                        @ 0802c132 9066
    b LAB_0802c228                           @ 0802c134 78e0
LAB_0802c136:
    .hword 0x4643    @ 0802c136 4346
    ldr r0,[r3,#0x68]                        @ 0802c138 986e
    ldr r1,[r3,#0x74]                        @ 0802c13a 596f
    subs r0,r0,r1    @ 0802c13c 401a
    str r0,[r3,#0x68]                        @ 0802c13e 9866
    b LAB_0802c15a                           @ 0802c140 0be0
LAB_0802c142:
    .hword 0x4644    @ 0802c142 4446
    ldr r0,[r4,#0x68]                        @ 0802c144 a06e
    ldr r1,[r4,#0x74]                        @ 0802c146 616f
    muls r0,r1    @ 0802c148 4843
    str r0,[r4,#0x68]                        @ 0802c14a a066
    b LAB_0802c15a                           @ 0802c14c 05e0
LAB_0802c14e:
    .hword 0x4647    @ 0802c14e 4746
    ldr r0,[r7,#0x68]                        @ 0802c150 b86e
    ldr r1,[r7,#0x74]                        @ 0802c152 796f
    bl __udivsi3                             @ 0802c154 e2f042fb
    str r0,[r7,#0x68]                        @ 0802c158 b866
LAB_0802c15a:
    ldr r3, PTR_gPrng_0802c19c               @ 0802c15a 104b
    ldr r0, DAT_0802c1a0                     @ 0802c15c 1048
    adds r6,r3,r0    @ 0802c15e 1e18
    ldrb r5,[r6,#0x0]                        @ 0802c160 3578
    lsrs r0,r5,#0x6    @ 0802c162 a809
    movs r1,#0x81    @ 0802c164 8121
    lsls r1,r1,#0x2    @ 0802c166 8900
    adds r3,r3,r1    @ 0802c168 5b18
    movs r4,#0x3f    @ 0802c16a 3f24
    adds r1,r4,#0x0    @ 0802c16c 211c
    ldrb r2,[r3,#0x0]                        @ 0802c16e 1a78
    ands r1,r2    @ 0802c170 1140
    lsls r1,r1,#0x2    @ 0802c172 8900
    orrs r1,r0    @ 0802c174 0143
    subs r1,#0x1    @ 0802c176 0139
    lsls r1,r1,#0x10    @ 0802c178 0904
    lsrs r2,r1,#0x10    @ 0802c17a 0a0c
    movs r0,#0x3    @ 0802c17c 0320
    ands r2,r0    @ 0802c17e 0240
    lsls r2,r2,#0x6    @ 0802c180 9201
    adds r0,r4,#0x0    @ 0802c182 201c
    ands r0,r5    @ 0802c184 2840
    orrs r0,r2    @ 0802c186 1043
    strb r0,[r6,#0x0]                        @ 0802c188 3070
    lsrs r1,r1,#0x12    @ 0802c18a 890c
    ands r1,r4    @ 0802c18c 2140
    movs r0,#0x40    @ 0802c18e 4020
    rsbs r0,r0,#0    @ 0802c190 4042
    ldrb r4,[r3,#0x0]                        @ 0802c192 1c78
    ands r0,r4    @ 0802c194 2040
    orrs r0,r1    @ 0802c196 0843
    strb r0,[r3,#0x0]                        @ 0802c198 1870
    b LAB_0802c228                           @ 0802c19a 45e0
PTR_gPrng_0802c19c:
    .word  gPrng                          @ 0802c19c 40000003
DAT_0802c1a0:
    .word  0x00000203                     @ 0802c1a0 03020000
LAB_0802c1a4:
    ldr r0, DAT_0802c1bc                     @ 0802c1a4 0548
    adds r5,r0,#0x0    @ 0802c1a6 051c
    adds r5,#0x62    @ 0802c1a8 6235
    ldrh r3,[r5,#0x0]                        @ 0802c1aa 2b88
    adds r6,r3,#0x0    @ 0802c1ac 1e1c
    .hword 0x4680    @ 0802c1ae 8046
    cmp r6,#0x73                             @ 0802c1b0 732e
    bhi LAB_0802c1c0                         @ 0802c1b2 05d8
    adds r0,r3,#0x4    @ 0802c1b4 181d
    strh r0,[r5,#0x0]                        @ 0802c1b6 2880
    b LAB_0802c228                           @ 0802c1b8 36e0
    .zero  0x2
DAT_0802c1bc:
    .word  0x02023360                     @ 0802c1bc 60330202
LAB_0802c1c0:
    .hword 0x4641    @ 0802c1c0 4146
    adds r1,#0x6d    @ 0802c1c2 6d31
    movs r0,#0x40    @ 0802c1c4 4020
    ldrb r1,[r1,#0x0]                        @ 0802c1c6 0978
    ands r0,r1    @ 0802c1c8 0840
    cmp r0,#0x0                              @ 0802c1ca 0028
    beq LAB_0802c1e2                         @ 0802c1cc 09d0
    ldr r2, PTR_gPrng_0802c1e8               @ 0802c1ce 064a
    movs r7,#0xa4    @ 0802c1d0 a427
    lsls r7,r7,#0x1    @ 0802c1d2 7f00
    adds r1,r2,r7    @ 0802c1d4 d119
    movs r0,#0x3    @ 0802c1d6 0320
    ldrh r1,[r1,#0x0]                        @ 0802c1d8 0988
    ands r0,r1    @ 0802c1da 0840
    adds r4,r2,#0x0    @ 0802c1dc 141c
    cmp r0,#0x0                              @ 0802c1de 0028
    beq LAB_0802c1ec                         @ 0802c1e0 04d0
LAB_0802c1e2:
    movs r0,#0x1    @ 0802c1e2 0120
    b LAB_0802c22a                           @ 0802c1e4 21e0
    .zero  0x2
PTR_gPrng_0802c1e8:
    .word  gPrng                          @ 0802c1e8 40000003
LAB_0802c1ec:
    movs r0,#0xa3    @ 0802c1ec a320
    lsls r0,r0,#0x1    @ 0802c1ee 4000
    adds r1,r4,r0    @ 0802c1f0 2118
    movs r0,#0x80    @ 0802c1f2 8020
    ldrh r1,[r1,#0x0]                        @ 0802c1f4 0988
    ands r0,r1    @ 0802c1f6 0840
    cmp r0,#0x0                              @ 0802c1f8 0028
    beq LAB_0802c20a                         @ 0802c1fa 06d0
    .hword 0x4640    @ 0802c1fc 4046
    adds r0,#0x64    @ 0802c1fe 6430
    ldrh r0,[r0,#0x0]                        @ 0802c200 0088
    cmp r6,r0                                @ 0802c202 8642
    bcs LAB_0802c20a                         @ 0802c204 01d2
    adds r0,r3,#0x4    @ 0802c206 181d
    strh r0,[r5,#0x0]                        @ 0802c208 2880
LAB_0802c20a:
    movs r2,#0xa3    @ 0802c20a a322
    lsls r2,r2,#0x1    @ 0802c20c 5200
    adds r1,r4,r2    @ 0802c20e a118
    movs r0,#0x40    @ 0802c210 4020
    ldrh r1,[r1,#0x0]                        @ 0802c212 0988
    ands r0,r1    @ 0802c214 0840
    cmp r0,#0x0                              @ 0802c216 0028
    beq LAB_0802c228                         @ 0802c218 06d0
    .hword 0x4641    @ 0802c21a 4146
    adds r1,#0x62    @ 0802c21c 6231
    ldrh r0,[r1,#0x0]                        @ 0802c21e 0888
    cmp r0,#0x74                             @ 0802c220 7428
    bls LAB_0802c228                         @ 0802c222 01d9
    subs r0,#0x4    @ 0802c224 0438
    strh r0,[r1,#0x0]                        @ 0802c226 0880
LAB_0802c228:
    movs r0,#0x0    @ 0802c228 0020
LAB_0802c22a:
    pop {r3,r4}                              @ 0802c22a 18bc
    .hword 0x4698    @ 0802c22c 9846
    .hword 0x46a1    @ 0802c22e a146
    pop {r4,r5,r6,r7}                        @ 0802c230 f0bc
    pop {r1}                                 @ 0802c232 02bc
    bx r1                                    @ 0802c234 0847
    .zero  0x2

