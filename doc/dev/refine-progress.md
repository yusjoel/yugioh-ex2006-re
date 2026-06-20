# refine-progress — asm/ 25 模块细化总进度

> **总目标**: `asm/` 下 25 个反汇编模块 (`NN_*.s`, 覆盖 ROM 0x080000c0..0x084c7637) **全部内部细化完成**——
> 消灭 `DAT_/DWORD_/UNK_/PTR_DAT_` 自动名 + `ROM_INCBIN`/`.byte` 未分化块, 立即数符号化, 注释订正,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> **驱动**: skill `refine-loop` + 3 sub-agent (`refine-{executor,reviewer,fixer}`)。方法论
> `doc/dev/methodology/refine-loop.md`。这是 refine-loop 的**跨文件状态镜像** (类比 analysis-loop 的
> `eval/PROGRESS.md`)。
>
> **当前文件**: `09_equip_lp_display.s` (0x0806e76c..0x08079e60)。
> **下一任务 (正向进度)**: file 09 Seg-10 `[0x0807850c..0x08079e60)` (19 fn, 88 slots, 10 inc: 0x78a90/44 + 0x78b24/d4 + 0x78fde/f6 + 0x79148/1ec + 0x793ac/154 + 0x7965c/50 + 0x796c4/10c + 0x79a1c/48 + 0x79adc/13c + 0x79c9c/1c4; 最重段, likely Seg-10a/10b split)。
> **修补进度 (REMEDIATION)**: Seg-1 DONE; Seg-4 DONE; Seg-5 DONE; **Seg-8 DONE (2026-06-21)**. ALL done-segment remediation COMPLETE. Done range [0x6e76c..0x7738c) has zero ROM_INCBIN + zero .byte-code residue.

上次更新: 2026-06-21 **file 09 Seg-9b 完成 (Seg-9 COMPLETE)**. EQ=33 all REUSE (gDuelPhaseFlags x3/gP1LifePoints x8/PLAYER_BLOCK_STRIDE x9/LP_CARD_TRACK_BASE_OFF x3/gEquipChainSlotRefs x2/gDuelFieldSlots x3/ACTIVATION_STATE_B_OFF x1/gDuelCardCtxBase x1/EQUIP_PHASE_FRAME_OFF x4/gDuelFieldSlots_p2_base x2/SANCTUARY_CID_SHIFTED x2/BLUE_EYES_WHITE_DRAGON_CID x1/gEquipZoneCountTable x1); REF=3 (PTR_DAT_08077f2c->dangerous_machine_dispatch_table_7f44/DAT_08077f44->dangerous_machine_dispatch_sub_stubs_7f44 self-ref/DAT_08078368->monster_gate_dispatch_sub_stubs_8368 self-ref); RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; DISASM=4 blocks (B6 fn_eligible_dangerous_machine_type6@0x08077ecc CID=0x1738/B7 6 dangerous_machine sub-stubs@0x08077f44 6-entry dispatch/B8 fn_eligible_monster_gate@0x080782c0 CID=0x175c/B9 8 monster_gate sub-stubs@0x08078368 31-entry dispatch); §5.1=0; card_info.inc +2 (DANGEROUS_MACHINE_TYPE6_CID=0x1738/MONSTER_GATE_CID=0x175c); CSV +2 rows (fn_eligible_dangerous_machine_type6@0x08077ecc+fn_eligible_monster_gate@0x080782c0); ROM_INCBIN 14->10 (4 blocks eliminated); Seg-9b range [0x77c50,0x7850c): 0 ROM_INCBIN 0 non-ASCII; 踩坑: 5 fix-scripts needed (PoolFix: 0x77f98+0x78394+0x78398+0x78454; Residues: LAB_08077eec+08077fae+08077fd0; Pools2: wrong DWords at 0x77f18/1c->correct at 0x77f20/24); byte-identical 9689337d. **下一任务: Seg-10 [0x0807850c..0x08079e60)**.

上次更新 (prev): 2026-06-21 **file 09 Seg-8 REMEDIATION 完成 (LAST done-segment remnant)**. DISASM=2 (Block A: ROM_INCBIN 0x768dc/0x1e->15 THUMB instrs in spell_vanishing_sub_6818 beq-taken path; Block B: .byte 0x10,0x20 at LAB_08076750->movs r0,#0x10 in fn_eligible_mustering_dark_scorpions beq-taken path); DATA createDWord=2 (Block C: DAT_08076720 Ghidra split artifact->DWORD_08076720 .word DARK_SCORPION_BURGLARS_CID=0x1531 REUSE card_info.inc:1476; Block D: DAT_0807677c 4B .byte->DWORD_0807677c .word PLAYER_BLOCK_STRIDE=0x868 REUSE ewram.inc:250); EQ=2 all REUSE; carve=0; REF=0; RENAME=0; NO new constants; ROM_INCBIN 15->14; Seg-8 range [0x7629c,0x7738c): 0 residue; GLOBAL done-range [0x6e76c,0x7738c): 0 ROM_INCBIN 0 .byte-code; byte-identical 9689337d. Script: RefineF09Seg8RBlocks.py. REMEDIATION ALL DONE.

上次更新 (prev): 2026-06-20 **file 09 Seg-5 REMEDIATION 完成**. DISASM=9 (2 ROM_INCBIN: 0x73218/12+0x73636/56 + 7 .byte CODE: 0x73156/a+0x7326c/4+0x7359e/a+0x73732/8+0x7387a/a+0x73922/10+0x73d30/e); DATA createDWord=3 (0x73168->trap_dustshoot_sub_3290 / 0x735b4->machine_dup_sub_374c / 0x7388c->cat_ill_omen_sub_3a46); EQ=1 REUSE (CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d card_info.inc:1496 at pool_b4_368c); ROM_INCBIN 17->15; 0 residue in Seg-5 range [0x72d20,0x74338); byte-identical 9689337d. Script: DisassembleF09Seg5RBlocks.py.

上次更新 (prev): 2026-06-20 **file 09 Seg-4 REMEDIATION 完成**. DISASM=8 (4 ROM_INCBIN: 0x720e2/12+0x7270e/1e+0x7276a/1e+0x72794/20 + 4 .byte CODE: 0x71f74/c+0x7241c/c+0x7256a/a+0x72838/10); DATA createDWord=4 (0x72430/0x7257c/0x72734/0x72830); EQ=2 REUSE (LP_CARD_TRACK_BASE_OFF/lookup_equip_score_b_0x1b9); fix script: FixF09Seg4RLPPoolLabel.py (pool label self-ref rename); ROM_INCBIN 21->17; 0 residue in Seg-4 range; byte-identical 9689337d. Scripts: DisassembleF09Seg4RBlocks.py + FixF09Seg4RLPPoolLabel.py.

上次更新 (prev): 2026-06-20 **file 09 Seg-1 REMEDIATION Cluster-2+3 完成** (Cluster-3 B7c-B7g co-disassembled in same session). DISASM=20 items (9 ROM_INCBIN: 0x6f85e/136+0x6fa0a/36+0x6fa62/12+0x6fa78/8c+0x6fb16/32+0x6fdee/26+0x6fe8a/4a+0x6fede/12+0x6fef2/18; 11 .byte: 0x6fa4e/10+B2c-g/B7c-g); EQ=15 (11R+4N: OAM_EQUIP_LP_SPRITE_P1_5E=0x805e/SPIRIT_MESSAGE_N_CID=0x1498/SPIRIT_MESSAGE_A_CID=0x1499/CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d); REF=2 (equip_lp_tbl_f990/equip_chain_tbl_fe10); ROM_INCBIN count 30->21; byte-identical 9689337d. Scripts: DisassembleF09Seg1R2Cluster2.py + DisassembleF09Seg1R2B1Fix.py. Note: B1 multi-pass + unrestricted-disasm fix needed (A10 range-limited DisassembleCommand stopped early; fixed with unrestricted flow pass).

上次更新 (prev): 2026-06-20 **file 09 Seg-1 REMEDIATION Cluster-1 完成**. DISASM=7 blocks (5 ROM_INCBIN 0x6f00a/32+0x6f07a/22+0x6f0ae/12+0x6f0ce/b2+0x6f18a/3a + 2 .byte 0x6f056/10+0x6f068/10); REF=2 (gduel_phase_f034/equip_disp_tbl_f038); ROM_INCBIN count 35->30; byte-identical 9689337d. Script: DisassembleF09Seg1RCluster1.py.

上次更新 (prev): 2026-06-19 **file 09 Seg-9a 完成**. EQ=26(all REUSE except LEGENDARY_JUJITSU_MASTER_CID/KANGAROO_CHAMP_CID NEW)/REF=5(spatial_collapse/jade_insect dispatch tables+sub-stub blocks+dimension_fusion sub-stubs)/RENAME=0/FUNC_RENAME=0/PLATE=0; disasm=5 blocks(B1 fn_eligible_spatial_collapse@0x0807757c CID=0x16df pool x2/B2 6 spatial_collapse sub-stubs@0x080775d0/B3 fn_eligible_dimension_fusion@0x080779e4 CID=0x1712 pool x2/B4 6 jade_insect sub-stubs+fn_eligible_jade_insect_whistle@0x08077b34 CID=0x1717/B5 6 dimension_fusion sub-stubs@0x08077b88); PoolFix 12 const-pool DWords(0x4a4/0x1ce8/0x1da8/0x8056/0x1daa); REF label-collision fix(RefineF09Seg9aRefFix.py); card_info.inc +3(JADE_INSECT_WHISTLE_CID/LEGENDARY_JUJITSU_MASTER_CID/KANGAROO_CHAMP_CID); CSV +3 rows(fn_eligible_spatial_collapse/fn_eligible_dimension_fusion/fn_eligible_jade_insect_whistle); byte-identical 9689337d. **下一任务: file 09 Seg-9b [0x08077c50..0x0807850c)**.

上次更新 (prev): 2026-06-19 **file 09 Seg-8 完成**. EQ=68(63R+5N: DARK_SCORPION_BURGLARS_CID/DD_SCOUT_PLANE_CID/ENERGY_DRAIN_CID/GIFT_OF_THE_MARTYR_CID/HAND_SPELL_SLOT_CC8_OFF)/REF=0/RENAME=8(bitmap_dispatch_switch_table_ptr_6398+3 type_query_ptrs+side_match_ptr+mustering_dispatch_sub_stubs_65f0+spell_vanishing_dispatch_sub_stubs_67f8+equip_effect_opcode_switch_table_ptr_714c)/FUNC_RENAME=0/PLATE=0; disasm=4 blocks(B1 fn_eligible_mustering_dark_scorpions@0x080765b0/0x2c CID Dark Scorpion Burglars pool x2; B2 5 mustering sub-stubs@0x080765f0/0x19c 5-entry dispatch; B3 fn_eligible_spell_vanishing@0x080767ac/0x32 2B pad@0x767aa pool x2; B4 7 spell_vanishing sub-stubs@0x080767f8/0x110 7-entry dispatch); 8-pass pool fix campaign(PoolFixF09Seg8.py->b->c->d->e->f->g->h: DisassembleCommand stops at unconditional branch+clearListing wipes pool DWords+Ghidra re-merges adjacent DWords->split each disasm range at pool boundary+per-stub DisassembleCommand+force_dword after disasm; sub_66d8 case labels 0x76748/50 required 3 extra passes g+h as b-branches stopped flow); card_info.inc +5(DARK_SCORPION_BURGLARS_CID/DD_SCOUT_PLANE_CID/ENERGY_DRAIN_CID/GIFT_OF_THE_MARTYR_CID/DEAL_OF_PHANTOM_CID doc-only)/ewram.inc +1(HAND_SPELL_SLOT_CC8_OFF=0xcc8); CSV +2 rows(fn_eligible_mustering_dark_scorpions@0x080765b0+fn_eligible_spell_vanishing@0x080767ac); byte-identical 9689337d. **下一任务: file 09 Seg-9 [0x0807738c..0x0807850c)**.

上次更新 (prev Seg-7): 2026-06-19 **file 09 Seg-7 完成**. EQ=42(all REUSE)/REF=0/RENAME=4(emblem_dispatch_sub_stubs_5414+dispatch_eff_act_card_id_ptr_5c24+magical_dim_dispatch_sub_stubs_5d5c+friendship_dispatch_sub_stubs_5fe0)/FUNC_RENAME=0/PLATE=2(gEffectSlots→gEquipZoneCountTable+gSlotData→gDuelFieldSlots on enqueue_effect_slot_sprites_all_players); disasm=6 blocks(B1 fn_eligible_emblem_of_dragon_destroyer@0x08075378+pool×1; B2 6 emblem sub-stubs@0x08075414/0xa4; B3 fn_eligible_magical_dimension@0x08075d0c+pool×2; B4 9 magical_dim sub-stubs@0x08075d5c/0x214+inline pools; B5 fn_eligible_friendship@0x08075f90 2B pad@0x08075f8e+pool×2; B6 6 friendship sub-stubs@0x08075fe0/0x17c+inline pools); 3 PoolFix passes(PoolFixF09Seg7/b/c: 29+7 DWords); card_info.inc +2(EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629/MAGICAL_DIMENSION_CID=0x1678); FRIENDSHIP_CID=0x167a REUSE; CSV +3 rows(fn_eligible_emblem_of_dragon_destroyer/fn_eligible_magical_dimension/fn_eligible_friendship); byte-identical 9689337d. **下一任务: file 09 Seg-8 [0x0807629c..0x0807738c)**.

上上次更新: 2026-06-19 **file 09 Seg-6 完成**. EQ=55(all REUSE)/REF=5(gP1LifePoints x4+gEquipLpActivBitmap=0x0201e220 NEW)/RENAME=5(equip_zone_dispatch_table_48a0+equip_zone_sub_stubs_4914+check_equip_slot_eligible_bst_filter_ptr_4aac+check_equip_slot_eligible_by_type_query_ptr_4d4c+equip_display_switch_table_ptr_5150)/PLATE=1(FUN_0807a680->dispatch_equip_sprite_by_zone_or_capacity_guard)+CJK_fix(dispatch_dragon_summon_or_lp_delta_by_slot_type @0x08074770); carve=1(equip_zone_dispatch_table_48a0 29-entry raw-ptr table symbolic); disasm=2 blocks(B1 fn_eligible_dimension_jar 0x08074854/0x4a CID=0x15dd Dimension Jar+pool x4; B2 6 equip_zone_sub_stubs 0x08074914/0xcc+pool x5+labels x6); NEW constants: card_info.inc +1(DIMENSION_JAR_CID=0x15dd)/ewram.inc +1(gEquipLpActivBitmap=0x0201e220); CSV +1 row(fn_eligible_dimension_jar@0x08074854); byte-identical 9689337d. **下一任务: file 09 Seg-7 [0x080752cc..0x0807629c)**. EQ=21(19R+2N: RELOAD_CID/DISTURBANCE_STRATEGY_CID)/REF=4(gP1LifePoints×4)/RENAME=2(reasoning_dispatch_sub_stubs_3bc8/reversal_quiz_dispatch_sub_stubs_4080)/FUNC_RENAME=0/PLATE=1(stale FUN_08071d64→dispatch_spirit_monster_zone_sprite_by_card_id @0x08074318, benign [FAIL]已预先落地); disasm=4 blocks(B7 fn_eligible_reasoning 0x08073b1c/0x30+pool×2; B8 reasoning_dispatch_table 0x7c/31-entry/9-unique-targets 0x08073bc8+9stubs+3inline-pool×8DW; B9 fn_eligible_reversal_quiz 0x08073fde+pool×2; B10 reversal_quiz_dispatch_table 0x7c/31-entry 0x08074080+6stubs+5inline-pool×9DW); card_info.inc +2; 踩坑: force_dword 地址偏 2B(pad vs aligned pool)→PoolFixF09Seg5b.py 补正; byte-identical 9689337d. **Seg-5 (5a+5b) 全完成**. 上上次: file 09 Seg-5a 完成. EQ=48/REF=10(gP1LifePoints=0x0201c4e0)/RENAME=3(trap_dustshoot_dispatch_sub_stubs_2d62/cat_ill_omen_dispatch_sub_stubs_388c/an_owl_of_luck_dispatch_sub_stubs_38b8)/DISASM=6blocks(B1 fn_eligible_trap_dustshoot+dispatch+B2 machine_dup_sub_3690+6 sub_stubs+B3 fn_eligible_machine_duplication+dispatch+B4 machine_dup_sub_3690+6 sub_stubs+B5 cat/owl_eligible+dispatch+B6 cat/owl sub-stubs 0x73900/0x15c); card_info.inc +11(STATUE_OF_THE_WICKED_CID/TRAP_DUSTSHOOT_CID+9 TOKEN_*_CID)/ewram.inc +1(EQUIP_CHAIN_BASE_OFF)/oam_attr.inc +1(SPRITE_ATTR_CLR_BIT13); 踩坑: 8B force_dword 破坏 inline pool 相邻代码→改 4B + 5轮 PoolFix 脚本(Fix1..5); byte-identical 9689337d. **下一任务: file 09 Seg-5b [0x08073a5c..0x08074338)**.

上次更新 (prev): 2026-06-19 **file 09 Seg-5b 完成**. EQ=35(33R+2N: EQUIP_ZONE_WORD_MASK/FREED_THE_MATCHLESS_GENERAL_CID)/RENAME=4(fnptr+1 invoke_effect_node*_1538+check_equip_zone_pattern_ptr+equip_lp_disp_sub_table+equip_lp_sub_stubs_754)/PLATE=2(L6141 CJK->ASCII+L6209 stale FUN_)/DISASM=2blocks(eligible_dragged_down_into_grave_16fc+5 equip_lp_sub_{754/77c/78a/7a4/7c4}); Block2PoolFix 4 literal pool DWords; duel_field.inc +1/card_info.inc +2; byte-identical 9689337d. **file 08 Seg-10 完成 (file 08 全 10 段完成 ✅)**. EQ=42/RENAME=2/PLATE=0; disasm=4 blocks/19 new fn (check_equip_eligible_state_dispatch_cid_13ed + 11 cid_13ed_state_stubs + check_equip_eligible_state_dispatch_de_fusion + 6 de_fusion_state_stubs); De-Fusion state stub inversion corrected (Mode A #1); EQUIP_BITMAP_QUERY_KEY renamed from DISPCNT_SHADOW (Mode A #2); card_info.inc +5 (GAP_CID_13ED/MULTIPLICATION_OF_ANTS_CID/NEO_SPACE_SPAWN_CAT_1422/1813/19BA); duel_field.inc +2 (LP_DISPLAY_SEQ_PROGRESS_OFF/EQUIP_BITMAP_QUERY_KEY); CSV +19 rows; fn-ptr+1 periodic fix; byte-identical 9689337d. **file 08 Seg-9 完成** (EQ=51/RENAME=12/PLATE=3(1 CJK→ASCII rewrite + 2 stale FUN_ sub); 4 NEW constants (RING_OF_DESTRUCTION_CID=0x138d/MAGIC_CYLINDER_CID=0x1404/DRAINING_SHIELD_CID=0x176a/SPRITE_RECORD_P2_SIDE=0x8020); fn-ptr+1 periodic fix: check_equip_activation_at_slot11_1+check_equip_slot_eligible_by_equip_type_1 .equ aliases added to rom.s; CSV sync: 不需要; byte-identical 9689337d). **file 08 Seg-8c 完成** (EQ=39/RENAME=2/FUNC_RENAME=1/PLATE=2; disasm=2 blocks/9 new fn (check_equip_eligible_morphing_jar_2 + 8 morphing_jar2_state_stubs); Morphing Jar #2 CID=0x1369; tick_spear_cretin_placement_state_machine 误名订正 (dispatch_neo_daedalus_placement_check_by_state); P2LP_BLOCK2_OFF_1CF4 域例外 (base=gP1LifePoints vs FIELD_STATE_OFF base=gDuelFieldSlots); card_info.inc +2/oam_attr.inc +1/ewram.inc +1; FixF08Seg8cLiteralPools 17 DWORDs; FixF08Seg8cRipplePlate 3 hits; fn-ptr +1 fix 3 slots; CSV +9 rows +1 update; byte-identical 9689337d). **file 08 Seg-8b 完成** (EQ=17/REF=2/PLATE=3; disasm=5 blocks/30 new fn (check_equip_eligible_cid_135b + 10 cid_135b_state_stubs + check_equip_eligible_magical_hats + 11 magical_hats_state_stubs + 7 magical_hats_zone_state_stubs); 嵌套跳表 0x6bc2c->0x6bfa0->0x6bfbc; card_info.inc +3 (MAGICAL_HATS_CID/CEASEFIRE_CID/SPELL_ABSORBING_LIFE_CID); FixF08Seg8bLiteralPools 32 DWORDs; fn-ptr +1 fix 3 slots; CSV +30 rows; byte-identical 9689337d). **file 08 Seg-8a 完成** (EQ=22/REF=1/RENAME=5/FUNC_RENAME=2/PLATE=6; disasm=3 blocks/21 new fn; card_info.inc +1 GIANT_GERM_CID; CSV +21 rows; byte-identical 9689337d). **file 08 Seg-7 完成** (EQ=40/3 new const (EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8/OAM_ZONE_SPRITE_PAIR_P2_FIRST=0x8028/LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff); §5.1 +1 (0x0806a544 4B orphan); fn-ptr+1 periodic fix 4 slots (check_equip_activation_at_slot11 x2 + check_activation_ctx_zone11_match_cb + check_zone_activation_ctx_match_cb); CSV sync: 无; byte-identical 9689337d). **file 08 Seg-6 完成** (EQ=82+7/REF=3/CREATE_FUNC=1/PLATE=1 CJK+wrong-card rewrite; disasm=1 fn (check_equip_eligible_set_slot8_flag_for_cid_12da); duel_field.inc +0 / ewram.inc +1 / oam_attr.inc +2 / card_info.inc +4; CSV +2; byte-identical 9689337d). **file 08 Seg-5 完成** (EQ=62/REF=4/DISASM=1 stub/PLATE=1 CJK→ASCII; 3 new card_info CID (BLAST_SPHERE/BIRDFACE/IMPERIAL_ORDER) + ewram +2 (gEquipLpZoneEntryBase/EQUIP_OAM_ENTRY_ATTR_14F8) + oam_attr +3 (OAM_EQUIP_SPRITE_TILE_P2_1B/1C/EQUIP_SLOT_SCORE_CAP); check_equip_eligible_always_false @ 0x08068828 新建 fn; CSV +1 row; byte-identical 9689337d). **file 08 Seg-4 完成** (EQ=73/REF=1/CREATE_FUNC=1/PLATE=1; 4 new card_info.inc CID+thresholds (SOUL_ABSORBING_BONE_TOWER/MALICE_ASCENDANT/CARD_FIELD3_THRESHOLD_1499/1500); fn-ptr +1 periodic fix asm/03 x4 + asm/04 x1 + asm/08 x3 (incl. Seg-2 regression fix); CSV +1 row (check_activation_ctx_zone11_match_cb); byte-identical 9689337d; 下一任务 Seg-5 0x67fa4..0x690dc + switchD_080686a2). **file 08 Seg-3 完成** (EQ=51/REF=4/RENAME=2/PLATE=2; disasm=1 block/8 new stub fn (dispatch_equip_effect_type_stub_{80/7f/7e/7d/78/77/76/75}); card_info.inc +5 CID (DE_SPELL/CYBER_STEIN/ICID_RESERVED_A/B/C); oam_attr.inc +1 (OAM_ATTR_P2_SPRITE); CSV +8 rows; byte-identical 9689337d; 下一任务 Seg-4 0x67160..0x67fa4). **file 07 Seg-10 完成 (file 07 全 10 段完成 ✅)** (EQ=40/RENAME=3/FUNC_RENAME=0/PLATE=0; disasm=3 blocks/3 new fn (Block A check_opp_active_player_duel_phase_leq3 shared CID 0x17fd/0x1886/0x195f + Block B check_opp_alt_hand_count_nonzero_for_cid_188b D.D.Dynamite 0x188b + Block C check_zone_non_field_type_or_has_monsters_for_cid_1911 Cyber Archfiend 0x1911); card_info.inc +4 CID (THREATENING_ROAR/D_D_DYNAMITE/HERO_BARRIER/DES_FROG); CSV +3 rows; byte-identical 9689337d; 下一任务 Seg-10). **file 07 Seg-8 完成** (EQ=64/REF=3/RENAME=2/FUNC_RENAME=0/PLATE=3(2 stale FUN_+1 CJK rewrite); disasm=5 blocks/6 new fn (Block1 check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3 Mind Wipe 0x17f3 + Block2 check_equip_slot_eligible_opp_is_active_field_eq2_for_cid_17fc Taunt 0x17fc+check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801 Heavy Slump 0x1801 + Block3 check_equip_slot_eligible_opp_lp_field14_nonzero_for_cid_1804 Cemetary Bomb 0x1804 + Block4 check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d Mind Haxorz 0x184d + Block5 check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853 Covering Fire 0x1853); duel_field.inc +1 ATK_THRESHOLD_2999=0xbb7; card_info.inc +4 CID; CSV +6 rows; byte-identical 9689337d; 下一任务 Seg-9). **file 07 Seg-7 完成** (EQ=44/REF=17+2disasm/RENAME=2/FUNC_RENAME=1(check_zera_ritual->check_banisher_of_light_absent_from_field)/PLATE=10(7 CJK+2 gDuelEffectCtx fix+1 Zera->Banisher); disasm=1 block(0x61c66/0x2a check_player_lp_status_nonzero_for_cid_1776@0x08061c68 CID 0x1776 Corpse of Yata-Garasu); card_info.inc +7 CID/ewram.inc +1 LP_GAP_THRESHOLD_7000; CSV +1 new fn+1 rename; byte-identical 9689337d; 下一任务 Seg-8). **file 07 Seg-6 完成** (EQ=47/PLATE=6(6 CJK rewrites incl. DUEL_STATE_PTR->gEquipChainSlotRefs 语义订正); disasm=3 blocks/3 new fn (Block1 check_exodia_set_in_extra_for_cid_165b@0x08060a88/CID 0x165b + Block2 check_zone_type580_direction_mismatch_for_cid_16c6@0x08061070/CID 0x16c6 + Block3 check_lp_zone_hand_above6_for_cid_16d1@0x0806121c/CID 0x16d1); card_info.inc +12 CID (QUEENS_KNIGHT/CONTRACT_WITH_EXODIA/SAGES_STONE/OJAMA_YELLOW/FENRIR/CHAOS_END/CHAOS_EMPEROR_DRAGON/RIGHT_LEG/LEFT_LEG/RIGHT_ARM/LEFT_ARM/EXODIA_THE_FORBIDDEN_ONE); CSV +3 rows; byte-identical 9689337d; 下一任务 Seg-7). **file 07 Seg-5 完成** (EQ=52/PLATE=10(4 stale FUN_ sub+6 CJK rewrite); disasm=3 blocks/6 new fn (Block1 check_equip_slot_eligible_by_lp_slot_for_cid_159a + Block2 check_equip_slot_eligible_by_type_and_player_for_cid_15dc + Block3 F1/F2/F3 cid_15f0/15f2/15f3 + Block4 check_equip_slot_eligible_active_player_with_chain_and_node_count); literal-pool fix 9 slots; card_info.inc +8 CID (PEOPLE_RUNNING_ABOUT/OPPRESSED_PEOPLE/UNITED_RESISTANCE + REASONING/HELPING_ROBO/THUNDER_OF_RULER/METEORAIN/PINEAPPLE_BLAST); ewram.inc +3 / duel_field.inc +1; CSV +6 rows; byte-identical 9689337d). **file 07 Seg-4 完成** (EQ=44/REF=2/RENAME=1/PLATE_SUB=3; disasm=5 blocks/5 new fn (Block1 check_field_state_leq3_for_cid_14d4/Block2 check_zone640_opponent_turn_bit10_for_cid_151c/Block3 check_opp_turn_lp_leq1000_return2_for_cid_151e/Block4 check_player_lp_state_off10_nonzero/Block5 check_player_zone_count_above3_for_cid_1546); literal-pool fix 11 slots; periodic fn-ptr/symbol-primary fixes (FixF07Seg4PeriodicFnPtrs.py + FixF07Seg4PeriodicFnPtrs2.py + FixF07Seg4SymbolPrimary.py); ewram.inc +2 (gDuelEquipCtx/gDuelFieldSlotsEffectZoneBase); card_info.inc +4 CID; rom.s +1 label (zone_monster_field_bonus_dest_entry7); CSV +5 rows; byte-identical 9689337d). **file 07 Seg-3 完成** (EQ=24/REF=16/RENAME=5/PLATE_SUB=2; disasm=4 blocks/11 new fn (Block1 cid_13f9/13fa + Block2 cid_144e + Block3 cid_1450/1451/1460 + Block4 cid_1468/146f/1472/1475/147f); literal-pool fix 18 slots; fn-ptr periodic fix asm/03 x4+asm/04 x3+asm/06 x1+asm/07 x1; card_info.inc +2 CID (REVIVAL_JAM/RED_MOON_BABY); CSV +11 rows; byte-identical 9689337d). **file 07 Seg-2 完成** (EQ=65/REF=27/PLATE=3; disasm=2 blocks/5 new fn; card_info.inc +19 CID; ewram.inc +P2_ZONE1_LP_OFF; literal-pool fix 13 slots; fn-ptr periodic fix asm/03 x4+asm/04 x3+asm/06 x1+asm/07 x1; CSV +5 rows; byte-identical 9689337d). **file 07 Seg-1 完成** (EQ=54/REF=3/RENAME=9/PLATE=0; disasm=4 blocks/5 new fn; card_info.inc +11 CID (SANGA_OF_THUNDER/SCAPEGOAT/GRACEFUL_CHARITY/GREENKAPPA/REAPER_OF_CARDS/HARPIES_FEATHER_DUSTER/DRIVING_SNOW/NOBLEMAN_EXTERMINATION/BAIT_DOLL/cid_131c/cid_12fb); CSV +5 rows; §5.1 +1 (0x5c4aa/0x2a); byte-identical 9689337d; 下一任务 Seg-2 0x5cfec..0x5e358). **file 06 Seg-9 完成** (EQ=140/REF=1/RENAME=5/PLATE=7; disasm=2 blocks/6 new fn (tick_bonding_or_photon_activation_seq + 5 state handlers); card_info.inc +23 (SPECIAL_EQUIP_SENTINEL_ID/ZONE_STATUS_MASK/SPECIAL_EQUIP_TARGET_CID_A + 20 CID); CSV +6 rows; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d; 下一任务 file 06 Seg-10 0x5b480..0x5c2f0). **file 06 Seg-8 完成** (EQ=93/REF=21/RENAME=17/PLATE=3; disasm=4 blocks/13 new fn; card_info.inc +1 ABYSS_SOLDIER_CID / duel_field.inc +1 OP31_EFFECT_NODE_COUNT_CODE; CSV +13 rows + 2 updates; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; byte-identical 9689337d). **file 06 Seg-7 完成** (EQ=53/REF=5/PLATE=4; card_info.inc +1 CRIMSON_NINJA_CID / ewram.inc +1 LP_BANISHER_CTX_OFF / duel_field.inc +1 EQUIP_ACTIVE_CTX_OFF; 4 CJK plate 全段 ASCII 重写 + 1 stale FUN_ 订正; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-6 完成** (disasm=3 ranges/6 new fn; EQ=86/REF=5/RENAME=28/FUNC_RENAME=1/PLATE_SET=2; duel_field.inc +2 / card_info.inc +2; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; CSV +6 rows + 1 update; byte-identical 9689337d). **file 06 Seg-5 完成** (EQ=94/REF=23/PLATE_SET=5/PLATE_SUB=1; card_info.inc +7 CID / duel_field.inc +3 scalar; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-4 完成** (EQ=145/REF=5/RENAME=3/PLATE_SUBS=2/PLATE_SET=2; card_info.inc +55 CID; duel_field.inc +4 structural+22 score labels; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-3 完成** (disasm=1 ROM_INCBIN 0x55188/0x34 -> check_zone_slot_occupied_with_clear_equip_flag; EQ=44/REF=1; 0 new constants (全复用 ewram.inc); fn-ptr fix asm/03 x4 + asm/04 x3 + asm/05 x6 + asm/06 x1; CSV +1; byte-identical 9689337d). **file 06 Seg-2 完成** (disasm=1 ROM_INCBIN 0x54614/0x48 -> check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight; EQ=52/PLATE=1; card_info.inc +5 CID+pattern / duel_field.inc +1 offset; CSV +1; fn-ptr fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-1 完成** (EQ=45/REF=1/RENAME=1/PLATE=3; card_info.inc +1 GRAVEKEEPERS_CANNONHOLDER_CID; ewram.inc +2 EQUIP_CTX_PLAYER_OFF/SLOT_REF_OFF; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d, commit f3bb6a9). **file 05 Seg-10 完成 (file 05 全 10 段完成 ✅)** (EQ=51/EOL=10/PLATE=2rewrites; card_info.inc +2 (BOTTOMLESS_TRAP_HOLE_CID/FIELD5_SCORE_THRESHOLD_1499); fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 05 Seg-9 完成** (EQ=112/RENAME=5/PLATE=2subs; card_info.inc +27 CID (SUMMONED_SKULL/RED_EYES_B_DRAGON/MULTIPLY/GRACEFUL_DICE/SHADOW_TAMER/DRAGON_MANIPULATOR/WINGBEAT_GIANT_DRAGON/INSECT_IMITATION/LIMITER_REMOVAL/CATHEDRAL_OF_NOBLES/PYRAMID_ENERGY/METAMORPHOSIS/FORMATION_UNION/KNIGHTS_TITLE/TERRORKING_ARCHFIEND/ULTRA_EVOLUTION_PILL/ORDER_TO_CHARGE/ORDER_TO_SMASH/BIG_WAVE_SMALL_WAVE/DOUBLE_ATTACK/KAMINOTE_BLOW/MINEFIELD_ERUPTION/TRANSCENDENT_WINGS/SPIRITUAL_EARTH_ART/ELEMENTAL_HERO_TEMPEST/HERO_HEART/PHOTON_GENERATOR_UNIT); fn-ptr periodic fix asm/03 x4 + asm/04 x4; byte-identical 9689337d). **file 05 Seg-8 完成** (EQ=75/REF=1/FNPTR=6/RENAME=1/PLATE=4subs; card_info.inc +11 CID+1 threshold / ewram.inc +1 / duel_field.inc +3; §5.1 +1; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; byte-identical 9689337d). **file 05 Seg-7 完成** (EQ=69/REF=0/RENAME=3/PLATE=4subs; card_info.inc +22 CID (18 named + 4 unallocated); fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 05 Seg-6 完成** (EQ=129/REF=2/RENAME=2/PLATE=13; ewram.inc +8 / card_info.inc +36 CID+1 / 5 disasm regions (Block1 13 stubs + Block2 12 stubs + RegA 3 + RegC 4 + RegD 2) / 138 literal pool DWORD fixes; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-5 完成** (EQ=67/REF=0/RENAME=8/PLATE=0; card_info.inc +7 CID / oam_attr.inc +2 / ewram.inc +9; §5.1 +3 orphan blocks (0x4c734/0x38, 0x4cca2/0xea, 0x4cdac/0x2c); byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-4b 完成** (EQ=89/RENAME=10/FUNC_RENAME=0/PLATE=1; card_info.inc +57 new CID; §5.1 +1 orphan 0x4becc/0x54; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3; Seg-4 全完成 4a+4b). **file 05 Seg-4a 完成** (EQ=95/RENAME=6/SCALAR_EQ=5; card_info.inc +68 (63 B-class CID + 3 inline CID + 2 field6 type); byte-identical 9689337d; no carve/disasm; commit 3155175). **file 05 Seg-3 完成** (EQ=87/REF=2/RENAME=3/FUNC_RENAME=1/PLATE=7; card_info.inc +50 CID; 3 disasm blocks → 5 new THUMB fn; FixF05Seg3SplitLiteralPools (20 DWORD forced) + FixF05Seg3BlockCStubTable (switch table + inline stub); byte-identical 9689337d; fn-ptr +1 periodic fix asm/04 x3; commit bd9ce13). **file 05 Seg-2 完成** (EQ=33/REF=1/card_id_EQ=34/PLATE=4subs; ewram.inc +2 + duel_field.inc +2 + oam_attr.inc +2 + card_info.inc +5; §5.1 +1 orphan 0x4aa5e/0xee; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-1 完成** (EQ=99/REF=14/RENAME=39/PLATE=33; card_info.inc +16 CID + oam_attr.inc +21; byte-identical 9689337d; fn-ptr +1 periodic fix 7 slots). file 04 全 10 段完成 ✅ (Seg-10: EQ=87/REF=25/PLATE=8fn; 新建 oam_attr x10 + card_info x26 + duel_field x2; byte-identical 9689337d, commit cb54638)。

---

## 一、25 文件总表

| # | 文件 | 地址区间 | 段(~10/文件) | 状态 | 活动 doc |
|---|------|----------|------|------|---------|
| 00 | system_str_vija | 0x080000c0..0x0801cb00 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-00-system-str-vija.md` |
| 01 | vija_scene_text | 0x0801cb00..0x0802c238 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-01-vija-scene-text.md` |
| 02 | text_lp_fieldspell | 0x0802c238..0x08035f54 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-02-text-lp-fieldspell.md` |
| 03 | equip_chain_hand | 0x08035f54..0x0804020c | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-03-equip-chain-hand.md` |
| 04 | card_zone_sprite | 0x0804020c..0x08049014 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-04-card-zone-sprite.md` |
| 05 | equip_eligibility_a | 0x08049014..0x080537c0 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-05-equip-eligibility-a.md` |
| 06 | equip_eligibility_b | 0x080537c0..0x0805c2f0 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-06-equip-eligibility-b.md` |
| 07 | equip_effect_chain | 0x0805c2f0..0x080643e0 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-07-equip-effect-chain.md` |
| 08 | equip_oam_neodaed | 0x080643e0..0x0806e76c | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-08-equip-oam-neodaed.md` |
| 09 | equip_lp_display | 0x0806e76c..0x08079e60 | Seg-1..10 已拆 | 🟡 进行中 (9/10) | `doc/dev/p5-refine-09-equip-lp-display.md` |
| 10 | equip_effect_dispatch | 0x08079e60..0x080850d8 | 未拆 | ⬜ | |
| 11 | effect_slot_puzzletext | 0x080850d8..0x080941c4 | 未拆 | ⬜ | |
| 12 | equip_activation_scan | 0x080941c4..0x0809d718 | 未拆 | ⬜ | |
| 13 | equip_placement | 0x0809d718..0x080a78dc | 未拆 | ⬜ | |
| 14 | equip_ai_scoring | 0x080a78dc..0x080b5348 | 未拆 | ⬜ | |
| 15 | equip_target_summon_zoom | 0x080b5348..0x080c1448 | 未拆 | ⬜ | |
| 16 | duelfield_zone | 0x080c1448..0x080cbf0c | 未拆 | ⬜ | |
| 17 | duelfield_pack_frame | 0x080cbf0c..0x080d5e84 | 未拆 | ⬜ | |
| 18 | pack_card_info | 0x080d5e84..0x080df368 | 未拆 | ⬜ | |
| 19 | pack_eligibility_anim | 0x080df368..0x080e90a0 | 未拆 | ⬜ | |
| 20 | anim_jp_tileblit | 0x080e90a0..0x080f413c | 未拆 | ⬜ | |
| 21 | font_title_scene | 0x080f413c..0x080fdd3c | 未拆 | ⬜ | |
| 22 | cardlist_scene | 0x080fdd3c..0x081078d4 | 未拆 | ⬜ | |
| 23 | sound_cardlist_libc | 0x081078d4..0x08110dc8 | 未拆 | ⬜ | |
| 24 | libc_runtime | 0x08110dc8..0x084c7637 | 未拆 | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 二、当前文件 (00) 段进度

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1a | b1 残留 3 defer | ✅ | da7eb99 |
| 1b | 0x14398..0x14600 (7 fn) | ✅ | f37d2ed |
| 2 | 0x14838..0x14fa8 (§5.1 only) | ✅ | 39b3dfd |
| 3a | fs_load (carve fs 关键字表) | ✅ | ea54718 |
| 3b | 0x1510a..0x1571c | ✅ | 0421491 |
| 4 | 0x1571c..0x16218 | ✅ | 9626e06 |
| 5a | write_tile_region | ✅ | b177f9a |
| 5b | apply_bgdt/objd | ✅ | (committed) |
| 5c | apply_gfx_resource_list + R4 disasm 63 SJIS stubs | ✅ | (committed) |
| 5d | 0x171ec..0x1794c (15 fn + 2 carve + §5.1 0x17424/0x40) | ✅ | 8c4ec5a |
| 6a | 0x1794c..0x17e48 (5 fn, kana carve A+B+pool+I) | ✅ | baabb9a |
| 6b | 0x17e48..0x18774 (23 fn, carve F/G/H, §5.1 0x186ce/0x22) | ✅ | 67862bf |
| 7 | 0x18774..0x19a58 (28 fn, carve J/K + §5.1 0x19640/0x20) | ✅ | (this session) |
| **8** | **0x19a58..0x1a794 (28 fn, banlist password 渲染簇)** | **✅** | (this session) |
| **9** | **0x1a794..0x1b850 (banlist/shuen 28fn + carve 1/2/3 + disasm block B + §5.1 block A)** | **✅** | (this session) |
| **10** | **0x1b850..0x1cb00 (vija/shuen 场景 tick, 32fn)** | **✅** | (see active doc §四.4.0ab) |

00 文件完整路线图 (段范围 / ROM_INCBIN / 旧覆盖) 见其活动 doc §五。
00 文件 §5.1 未引用登记: 0x14e54 / 0x14f9c / 0x1547e / 0x1550a / 0x156ec / 0x15d18 / 0x15fe8 /
0x16074 / 0x169d6+0x16a20 / 0x17424 / 0x186ce / 0x19640 / **0x1a89c** (孤儿 dead-code, 引用到时再 R4 disasm)。

### file 06 段进度 (equip_eligibility_b, 进行中)

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1 | 0x537c0..0x541cc (22 fn, 47 槽) | ✅ | f3bb6a9 |
| 2 | 0x541cc..0x54ba0 (22 fn, 50 槽, ROM_INCBIN 0x54614/0x48) | ✅ | 6c90482 |
| 3 | 0x54ba0..0x55440 (22 fn, 43 槽, ROM_INCBIN 0x55188/0x34) | ✅ | aee415f |
| 4 | 0x55440..0x565e8 (22 fn, 149 槽) | ✅ | fd8e6b6 |
| 5 | 0x565e8..0x57458 (22 fn, 101 槽) | ✅ | 3177750 |
| 6 | 0x57458..0x58550 (22 fn, 99 槽, ROM_INCBIN x2) | ✅ | 51ebd37 |
| 7 | 0x58550..0x58cec (22 fn, 58 槽) | ✅ | 8fd1210 |
| 8 | 0x58cec..0x59de0 (22 fn+13 new, 107 槽, ROM_INCBIN x2 + switchD) | ✅ | 11c409d |
| 9 | 0x59de0..0x5b480 (22 fn+6 new, 140 槽, ROM_INCBIN x2) | ✅ | 8c4bd9a |
| 10 | 0x5b480..0x5c2f0 (15 fn, 69 槽, switchD x2) | ✅ | c71149a |

**Seg-10 完成**: vija/shuen 32fn 全符号化, gVijaState 新全局, BG3HOFS plate 订正, CJK plate/EOL ASCII 转换; DWORD_SLOTS 永久修复 literal pool label 丢失问题; byte-identical 9689337d; file 00 全 10 段完成 ✅。

### file 07 段进度 (equip_effect_chain, 全完成)

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1 | 0x5c2f0..0x5cfec (34+5 fn) | ✅ | 7e1caa2 |
| 2 | 0x5cfec..0x5e358 (34+5 fn) | ✅ | da58892 |
| 3 | 0x5e358..0x5f1cc (34+11 fn) | ✅ | 2b80239 |
| 4 | 0x5f1cc..0x5fc94 (34+5 fn) | ✅ | 667391b |
| 5 | 0x5fc94..0x60898 (34+6 fn) | ✅ | 3fcbbce |
| 6 | 0x60898..0x613b4 (34+3 fn) | ✅ | d959091 |
| 7 | 0x613b4..0x61eb4 (34+1 fn) | ✅ | 45be161 |
| 8 | 0x61eb4..0x62d28 (34+6 fn) | ✅ | 926cdab |
| 9 | 0x62d28..0x63830 (34+3 fn) | ✅ | db741f1 |
| 10 | 0x63830..0x643e0 (33+4 fn) | ✅ | 55d0efe |

**Seg-9 完成**: Seg-8 executor proposal 越界预析已复用, Seg-9 全部落地:
- Block A (0x1a89c/0x20): §5.1 候选 (thumb=0; raw=1 偶合 0x08af5768 压缩 FS 资产)
- Block B (0x1ad18/0xec): R4 disasm 5 stubs (dispatch_banlist_cursor_action MOV PC,R0 跳转表目标)
- banlist_pass_ext_char_group carve (@0x09e3be3c, 代码引用 DWORD_0801abb0 in Seg-9)
- 越界 EQ 4槽: advance/retreat_banlist_password_cursor_slot_ewram_base/gsettings_offset
- 越界 RENAME 18槽: advance/retreat_banlist_password_cursor_slot_dir_field_off + load_banlist_char_by_cursor_slot_*/get_banlist_scroll_pixel_offset_*/get_banlist_password_entry_ptr_*/render_banlist_*/advance/retreat_banlist_pw_char_and_render_* 族
- 越界 REF 10槽: 7x gBanlistPasswordBuffer (Seg-9 fn) + 3x carve (char_candidate_str/alt_char/ext_char_group)

### file 09 段进度 (equip_lp_display, 进行中)

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1 | 0x6e76c..0x6ff50 (20 fn, 6 inc + 1 sw) | ✅ | 08b3db1 |
| 2 | 0x6ff50..0x7104c (20 fn, 1 inc) | ✅ | 79000e6 |
| 3 | 0x7104c..0x719fc (20 fn, 2 inc) | ✅ | c1c490d |
| 4 | 0x719fc..0x72d20 (20 fn, 8 inc; split 4a+4b) | ✅ | a9aa009 + (this session) |
| 5 | 0x72d20..0x74338 (20 fn, 10 inc; split 5a+5b) | ✅ | fa30373 + (this session) |
| 6 | 0x74338..0x752cc (20 fn, 2 inc + 1 sw) | ✅ | (this session) |
| 7 | 0x752cc..0x7629c (19 fn, 6 inc) | ✅ | (see p5-refine-09 §四) |
| 8 | 0x7629c..0x7738c (19 fn, 4 inc + 2 sw) | ✅ | 1e38556 + F09Seg8R |
| 9 | 0x7738c..0x7850c (19 fn, 9 inc) | ⬜ | |
| 10 | 0x7850c..0x79e60 (19 fn, 10 inc) | ⬜ | |

---

## 三、自动推进协议 (refine-loop 跨文件)

```
当前段完成 → 同文件下一段 (地址序, 不跳号)
当前文件全段 ✅ → 在本表标 ✅ → 自动跳下一文件 (NN+1):
   1) 为新文件建活动 doc doc/dev/refine/<NN_name>.md (含 §一 R1-R9 引用 / §二 pipeline /
      §三 进度 / §四 逐段记录 / §五 路线图 / §5.1 登记) —— 模板抄 00 文件 doc
   2) **先按地址拆分**: push-prologue 抽函数入口, 地址序均分 ~10 段 (边界=函数结束处),
      写入新 doc §五 路线图 (每段地址范围 + 内含 ROM_INCBIN + 旧覆盖列留空)
   3) **再逐批处理**: 从 Seg-1 起, executor → reviewer → fixer 逐段推进
   4) 更新本表该文件 doc 列 + 状态, 更新顶部"当前文件/下一任务"
全 25 文件 ✅ → refine 总目标达成
```

> 跨文件注意: 符号化时**优先复用**已建的 `constants/*.inc` (gSettings / OBJ_PALRAM_BASE / FourCC tag /
> ROM_REGION_CODE_ADDR / gFsDecompBuf / gTextEncodingOverride / GFX_ATTR_CLEAR_BITS_* 等)。
> 同一 ROM 数据被多文件引用时, 谁先 carve 谁建 label, 后者直接 `.word <label>` 引用。

---

## 四、关键路径

| 文件 | 用途 |
|------|------|
| `.claude/skills/refine-loop/SKILL.md` | 驱动器 (3-agent 编排 + 三条硬规则) |
| `.claude/agents/refine-{executor,reviewer,fixer}.md` | 3 sub-agent |
| `doc/dev/methodology/refine-loop.md` | 完整方法论 |
| `doc/dev/refine/<Seg>.{proposal,review}.md` | 每段留痕 |
| `tools/asm-regen/split_manifest.tsv` | 25 文件地址边界 (本表来源) |
| `output/2343.gba` SHA1 == 9689337d… | byte-identical 红线 |

**上次更新**: 2026-06-18 **file 09 Seg-2 完成** (EQ=71(61 REUSE+10 NEW: GUARDIAN_BAOU_CID/LEGENDARY_FIEND_CID/INSECT_PRINCESS_CID/AQUA_SPIRIT_CID/THUNDER_CRASH_CID/ENCHANTED_ARROW_CID/TOKEN_THANKSGIVING_CID/TOKEN_FEASTEVIL_CID/GRYPHONS_FEATHER_DUSTER_CID/CYCLONE_BOOMERANG_CID)/REF=3/RENAME=3(fnptr)/FUNC_RENAME=1(check_zone_tile_count_and_set_summon_restriction_flag@0x08070900)/PLATE=0; DISASM=1 block fn_eligible_bazoo_the_soul_eater@0x08070476+literal pool@0x08070514/18; BAZOO_THE_SOUL_EATER_CID=0x1482 EOL; 新常量: card_info.inc +11; CSV +1 row (0x08070900); byte-identical 9689337d; 下一任务 Seg-3 0x7104c..0x719fc). file 09 Seg-1 完成: EQ=40/REF=34/RENAME=3/PLATE=2/DISASM=6 blocks(25 stubs + 3 dispatch tables); 新常量: card_info.inc +4/ewram.inc +2/oam_attr.inc +1; Literal pool fix: FixF08Seg10AndF09Seg1LiteralPools(43 DWORDs)+FixF08Seg10CidStateLiteralPools2(8 DWORDs)+FixF08ThumbPlusOneLabels(2 THUMB+1 labels); byte-identical 9689337d; 下一任务 Seg-2 0x6ff50..0x7104c). file 08 Seg-8a 完成: EQ=22(1 NEW GIANT_GERM_CID)/REF=1/RENAME=5/FUNC_RENAME=2(dispatch_neo_daedalus_*→dispatch_germ_momonga_*/dispatch_spear_cretin_*)/PLATE=6/DISASM=21(3 blocks: Block1 8 stubs + Block2 7 stubs + Block3 6 stubs); §5.1 +1 (0x6adb6/0x3e); CSV +21 rows (new stubs) + 2 FUNC_RENAME 行手改; 附带修正: FixF08Seg8aLiteralPools(21 DWORD)/FixF08Seg8aPlateIds/fn-ptr+1 check_equip_activation_at_slot11 x2 + GAS .equ fixes x2; 跨模块 plate asm/05 line 4; byte-identical 9689337d; 下一任务 Seg-8b 0x6b56c..0x6cbe8)。 **Seg-7 完成** (EQ=40/3 new const (EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8/OAM_ZONE_SPRITE_PAIR_P2_FIRST=0x8028/LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff); §5.1 +1 (0x0806a544 4B orphan); fn-ptr+1 periodic fix 4 slots (check_equip_activation_at_slot11 x2 + check_activation_ctx_zone11_match_cb + check_zone_activation_ctx_match_cb); CSV sync: 无; byte-identical 9689337d). **file 08 Seg-6 完成** (EQ=82+7/REF=3/RENAME_ONLY=8/PLATE=1/DISASM=1/CREATE_FUNC=1; 新建 card_info +4 CID + ewram +1 LP_ACTIVATION_LINK_FLAG_OFF + oam_attr +2 OAM_SPRITE_CODE_P1_ACTIVATION/ZONE_ENTRY_FLAGS_CLR_MASK; CSV +2 rows; byte-identical 9689337d; 附带修正: RepairF08Seg3DataLabels/FixF08Seg6ThumbPlusPtrLabels/fn-ptr+1 check_equip_activation_at_slot11; 下一任务 Seg-7 0x6a118..0x6ab0c)。
