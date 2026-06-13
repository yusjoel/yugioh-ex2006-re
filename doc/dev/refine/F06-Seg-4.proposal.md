# Refine Proposal: F06-Seg-4  [0x08055440..0x080565e8)

## 分段拆分计划

Seg-4 共 153 槽, 超过 120 槽重段阈值, 按函数边界拆为 **Seg-4a / Seg-4b**:

| 子段 | 地址范围 | 函数数 | 槽数 | 主题 |
|------|----------|--------|------|------|
| Seg-4a | 0x08055440..0x08055ebc | 12 | 81 | same_player_type_mismatch + equip eligibility 谓词簇 + get_card_lp_cost_by_id + classify_equip_card_id_tier_abce/abc_short |
| Seg-4b | 0x08055ebc..0x080565e8 | 10 | 72 | classify_equip_card_id_tier_abcx + lookup_equip_card_score_by_card_id_and_player + render/trigger/enqueue + tick_equip_activation_state_machine 簇 |

fixer 分两次落地: Seg-4a → Seg-4b (地址序不回头)。

---

## 段测绘

### 函数入口 (22 fn)

| 地址 | 函数名 |
|------|--------|
| 0x08055440 | check_equip_slot_same_player_type_mismatch |
| 0x080554a0 | check_equip_slot_eligible_by_side_and_bst_or_field6 |
| 0x080554c4 | check_equip_slot_eligible_by_cross_player_and_field6_zero |
| 0x08055524 | check_equip_slot_cross_player_state7_type_eligible |
| 0x08055590 | check_equip_slot_eligible_by_same_side_whitelist_and_space |
| 0x08055624 | check_equip_slot_eligible_by_rival_appears_effect |
| 0x080556f0 | check_equip_slot_eligible_by_setcode_activation_and_zone_pair |
| 0x0805577c | check_equip_slot_zone_present_with_score_match |
| 0x080557e0 | check_equip_slot_eligible_by_card_id_bst_special_cases |
| 0x08055930 | get_card_lp_cost_by_id |
| 0x08055cd0 | classify_equip_card_id_tier_abce |
| 0x08055e60 | classify_equip_card_id_tier_abc_short |
| 0x08055ebc | classify_equip_card_id_tier_abcx |
| 0x08055f34 | lookup_equip_card_score_by_card_id_and_player |
| 0x0805635c | render_equip_lp_cost_sprite |
| 0x08056380 | trigger_lp_row_type2_if_equip_tier_nonzero |
| 0x080563a4 | enqueue_equip_zone_sprite_at_slot |
| 0x080563cc | tick_equip_activation_state_machine |
| 0x0805652c | dispatch_equip_zone_sprite_by_card_in_zone |
| 0x08056558 | set_equip_activation_player_state_bit |
| 0x08056578 | enqueue_lp_display_row_from_card_byte2 |
| 0x08056598 | tick_equip_activation_with_lp_row_type8_entry |

### 残留自动名槽: 153 个

(详见 EQ_SLOTS / REF_SLOTS / RENAME_SLOTS 各章节)

### ROM_INCBIN / .byte 块

**无** -- 段内无 ROM_INCBIN 或 .byte 块 (ref-scan 不需要)。

---

## 数据块分类 (Rule 2/3)

Seg-4 无 ROM_INCBIN 块, Rule 2/3 分类不适用。

---

## 符号化计划 (R1/R2/R3)

### 槽分类总览 (153 槽; 149 DAT_/DWORD_ + 4 PTR_ = 153 槽全覆盖)

| 类型 | 数量 | 说明 |
|------|------|------|
| EQ -- PLAYER_BLOCK_STRIDE 复用 | 10 | 0x868 × 5 对 |
| EQ -- gDuelFieldSlots 复用 | 10 | 0x0201c510 × 5 对 |
| EQ -- gDuelPhaseFlags 复用 | 5 | 0x0201b290 × 5 |
| EQ -- PHASE_LOCK_FLAG_OFF 复用 | 2 | 0x4bc × 2 (tick fns) |
| REF -- PTR_gP1LifePoints 复用 | 4 | gP1LifePoints 0x0201c4e0 |
| EQ -- EQUIP_ACTIVATION_STEP_OFF 新建 | 4 | 0x4ac × 4 |
| EQ -- CID 复用 (card_info.inc) | 17 | 已存在 CID equate |
| EQ -- CID 新建 (card_info.inc) | 55 | 50 具名 CID + 5 gap CID; 未在 card_info.inc 中存在 |
| EQ -- LP cost 已存 (gDuelCardCtxBase) | 1 | 0x0201e2a0 |
| EQ -- LP cost 复用 (duel_field.inc) | 2 | LP_COST_1500=0x5dc (line 201) / LP_COST_3000=0xbb8 (line 200) |
| EQ -- LP cost 新建 (duel_field.inc) | 1 | LP_COST_5000=0x1388 |
| EQ -- LP score scalar (RENAME) | 22 | lookup_equip_score_b_0x1a5..0x1cf (22 BST 分支返回值) |
| EQ -- 其他偏移/标量 新建 | 3 | EQUIP_ACTIVATION_STEP_OFF / TRIGGER_OP_PARAM_107 / EQUIP_ZONE_SPRITE_ATTR |
| RENAME -- DWORD_ slots | 3 | tick_equip_activation_with_lp_row_type8_entry |
| PLATE -- mojibake CJK 全段重写 | 2 | tick_equip_activation_state_machine (P1) / tick_equip_activation_with_lp_row_type8_entry (P2) |
| PLATE -- stale FUN_ substring 替换 | 1 | P4: 两处 FUN_ (FUN_0805715c + FUN_08059be0) 同时替换 |

---

### EQ_SLOTS (data-equate)

#### Seg-4a (slots in 0x08055440..0x08055ebc)

| 槽地址 | 槽标签 | 值 | 常量名 | 来源 |
|--------|--------|-----|--------|------|
| 0x08055490 | DAT_08055490 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x08055494 | DAT_08055494 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055514 | DAT_08055514 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x08055518 | DAT_08055518 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055580 | DAT_08055580 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x08055584 | DAT_08055584 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055608 | DAT_08055608 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x0805560c | DAT_0805560c | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055610 | DAT_08055610 | 0x0201b290 | gDuelPhaseFlags | ewram.inc 复用 |
| 0x08055614 | DAT_08055614 | 0x000004bc | PHASE_LOCK_FLAG_OFF | duel_field.inc 复用 |
| 0x080556d4 | DAT_080556d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x080556d8 | DAT_080556d8 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x080556dc | DAT_080556dc | 0x0000192b | A_RIVAL_APPEARS_CID | card_info.inc 新建; pw=5728014; "A Rival Appears!" |
| 0x08055768 | DAT_08055768 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x0805576c | DAT_0805576c | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055770 | DAT_08055770 | 0x080525d1 | check_equip_slot_eligible_by_type_and_card_id_pair+1 | REF_SLOT (fn-ptr, see below) |
| 0x080557b0 | DAT_080557b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x080557b4 | DAT_080557b4 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x08055854 | DAT_08055854 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x08055858 | DAT_08055858 | 0x0201c510 | gDuelFieldSlots | ewram.inc 复用 |
| 0x0805585c | DAT_0805585c | 0x00001669 | STAUNCH_DEFENDER_CID | card_info.inc 复用 |
| 0x08055870 | DAT_08055870 | 0x00001908 | BUBBLE_SHUFFLE_CID | card_info.inc 新建; pw=61968753; "Bubble Shuffle" |
| 0x080558cc | DAT_080558cc | 0x000013cd | LEGENDARY_FISHERMAN_CID | card_info.inc 复用 |
| 0x080558d0 | DAT_080558d0 | 0x0000164e | GUARDIAN_KAYEST_CID | card_info.inc 复用 |
| 0x080558e4 | DAT_080558e4 | 0x000010f4 | UMI_CARD_ID | card_info.inc 复用 (line 145) |
| 0x080558fc | DAT_080558fc | 0x000018f9 | EHERO_BUBBLEMAN_CID | card_info.inc 复用 |
| 0x0805596c | DAT_0805596c | 0x000017a3 | SPELL_ECONOMICS_CID | card_info.inc 新建; pw=4259068; "Spell Economics"; `get_card_lp_cost_by_id` field6==0x16 gate |
| 0x080559b4 | DAT_080559b4 | 0x000015ff | DIFFUSION_WAVE_MOTION_CID | card_info.inc 复用 |
| 0x080559b8 | DAT_080559b8 | 0x00001325 | DELINQUENT_DUO_CID | card_info.inc 复用 |
| 0x080559bc | DAT_080559bc | 0x000011cf | get_card_lp_cost_by_id_cid_11cf | card_info.inc 新建; gap CID (no card assigned in card-stats.s); neutral name |
| 0x080559d8 | DAT_080559d8 | 0x00001190 | get_card_lp_cost_by_id_cid_1190 | card_info.inc 新建; gap CID; neutral name |
| 0x08055a04 | DAT_08055a04 | 0x000012de | DARK_MAGIC_CURTAIN_CID | card_info.inc 新建; pw=99789342; "Dark Magic Curtain" |
| 0x08055a0c | DAT_08055a0c | 0x000012c3 | BRAIN_CONTROL_CID | card_info.inc 新建; pw=87910978; "Brain Control" |
| 0x08055a20 | DAT_08055a20 | 0x000012fd | SOLEMN_JUDGMENT_CID | card_info.inc 新建; pw=41420027; "Solemn Judgment" |
| 0x08055a28 | DAT_08055a28 | 0x000012ff | SEVEN_TOOLS_OF_THE_BANDIT_CID | card_info.inc 新建; pw=3819470; "Seven Tools of the Bandit" |
| 0x08055a54 | DAT_08055a54 | 0x000014be | BARK_OF_DARK_RULER_CID | card_info.inc 新建; pw=41925941; "Bark of Dark Ruler" |
| 0x08055a58 | DAT_08055a58 | 0x000013a7 | INJECTION_FAIRY_LILY_CID | card_info.inc 复用 |
| 0x08055a60 | DAT_08055a60 | 0x00001393 | get_card_lp_cost_by_id_cid_1393 | card_info.inc 新建; gap CID (no slot= in card-stats.s); neutral name |
| 0x08055a7c | DAT_08055a7c | 0x000014ab | AMAZONESS_CHAIN_MASTER_CID | card_info.inc 复用 |
| 0x08055a84 | DAT_08055a84 | 0x000014b6 | DARK_BALTER_THE_TERRIBLE_CID | card_info.inc 新建; pw=80071763; "Dark Balter the Terrible" |
| 0x08055aa4 | DAT_08055aa4 | 0x00001599 | CARD_SHUFFLE_CID | card_info.inc 新建; pw=12183332; "Card Shuffle" |
| 0x08055aac | DAT_08055aac | 0x0000156a | PUPPET_MASTER_CID | card_info.inc 新建; pw=41442341; "Puppet Master" |
| 0x08055ac0 | DAT_08055ac0 | 0x000015b5 | ROPE_OF_SPIRIT_CID | card_info.inc 新建; pw=37383714; "Rope of Spirit" |
| 0x08055ad0 | DAT_08055ad0 | 0x000015e6 | AUTONOMOUS_ACTION_UNIT_CID | card_info.inc 复用 |
| 0x08055b08 | DAT_08055b08 | 0x000017bc | CRUSH_D_GANDRA_CID | card_info.inc 新建; pw=64681432; "Crush D. Gandra" |
| 0x08055b0c | DAT_08055b0c | 0x000016a4 | EQUIP_LOCK_A_CID | card_info.inc 复用 |
| 0x08055b14 | DAT_08055b14 | 0x0000166c | SKILL_DRAIN_CID | card_info.inc 新建; pw=82732705; "Skill Drain" |
| 0x08055b28 | DAT_08055b28 | 0x0000169c | FINAL_COUNTDOWN_CID | card_info.inc 复用 |
| 0x08055b38 | DAT_08055b38 | 0x0000169d | get_card_lp_cost_by_id_cid_169d | card_info.inc 新建; gap CID; neutral name |
| 0x08055b58 | DAT_08055b58 | 0x00001741 | AGENT_OF_CREATION_VENUS_CID | card_info.inc 新建; pw=64734921; "The Agent of Creation - Venus" |
| 0x08055b68 | DAT_08055b68 | 0x00001712 | DIMENSION_FUSION_CID | card_info.inc 新建; pw=23557835; "Dimension Fusion" |
| 0x08055b7c | DAT_08055b7c | 0x00001775 | RETURN_ZOMBIE_CID | card_info.inc 新建; pw=3072077; "Return Zombie" |
| 0x08055b88 | DAT_08055b88 | 0x000017a7 | ENCHANTING_FITTING_ROOM_CID | card_info.inc 新建; pw=30531525; "Enchanting Fitting Room" |
| 0x08055bb8 | DAT_08055bb8 | 0x000018cc | BATTERY_CHARGER_CID | card_info.inc 新建; pw=61181383; "Battery Charger" |
| 0x08055bc0 | DAT_08055bc0 | 0x000017f4 | ABYSSAL_DESIGNATOR_CID | card_info.inc 新建; pw=89801755; "Abyssal Designator" |
| 0x08055bf8 | DAT_08055bf8 | 0x00001975 | DARK_DEAL_CID | card_info.inc 新建; pw=65824822; "Dark Deal" |
| 0x08055c04 | DAT_08055c04 | 0x00001932 | TRIAGE_CID | card_info.inc 新建; pw=30888983; "Triage" |
| 0x08055c1c | DAT_08055c1c | 0x000019d5 | DEMISE_KING_OF_ARMAGEDDON_CID | card_info.inc 新建; pw=72426662; "Demise, King of Armageddon" |
| 0x08055c30 | DAT_08055c30 | 0x000019e2 | MALFUNCTION_CID | card_info.inc 新建; pw=6137095; "Malfunction" |
| 0x08055c40 | DAT_08055c40 | 0x000005dc | LP_COST_1500 | duel_field.inc 复用 (line 201; file 03 Seg-4b 建) |
| 0x08055c50 | DAT_08055c50 | 0x00000bb8 | LP_COST_3000 | duel_field.inc 复用 (line 200; file 03 Seg-4b 建) |
| 0x08055c58 | DAT_08055c58 | 0x00001388 | LP_COST_5000 | 新建常量 duel_field.inc; 0x1388 = 5000 LP cost |
| 0x08055c70 | DAT_08055c70 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc 复用 |
| 0x08055d08 | DAT_08055d08 | 0x0000161c | TRIBE_INFECTING_VIRUS_CID | card_info.inc 复用 |
| 0x08055d0c | DAT_08055d0c | 0x000014de | THE_DRAGONS_BEAD_CID | card_info.inc 复用 |
| 0x08055d1c | DAT_08055d1c | 0x00001321 | FINAL_DESTINY_CID | card_info.inc 新建; pw=18591904; "Final Destiny" |
| 0x08055d30 | DAT_08055d30 | 0x00001470 | JUDGMENT_OF_ANUBIS_CID | card_info.inc 新建; pw=55256016; "Judgment of Anubis" |
| 0x08055d40 | DAT_08055d40 | 0x000014a7 | ROPE_OF_LIFE_CID | card_info.inc 新建; pw=93382620; "Rope of Life" |
| 0x08055d60 | DAT_08055d60 | 0x000015b4 | XYZ_DRAGON_CANNON_CID | card_info.inc 复用 |
| 0x08055d70 | DAT_08055d70 | 0x000015ad | NON_AGGRESSION_AREA_CID | card_info.inc 复用 |
| 0x08055d8c | DAT_08055d8c | 0x000015fa | YZ_TANK_DRAGON_CID | card_info.inc 复用 |
| 0x08055d94 | DAT_08055d94 | 0x000015fc | DARK_PALADIN_CID | card_info.inc 复用 |
| 0x08055dc0 | DAT_08055dc0 | 0x00001851 | SPELL_PURIFICATION_CID | card_info.inc 新建; pw=1669772; "Spell Purification" |
| 0x08055dc4 | DAT_08055dc4 | 0x000016a6 | SPELL_VANISHING_CID | card_info.inc 新建; pw=29735721; "Spell Vanishing" |
| 0x08055dd4 | DAT_08055dd4 | 0x0000179e | SPECIAL_HURRICANE_CID | card_info.inc 新建; pw=42598242; "Special Hurricane" |
| 0x08055df4 | DAT_08055df4 | 0x00001844 | BACK_TO_SQUARE_ONE_CID | card_info.inc 新建; pw=47453433; "Back to Square One" |
| 0x08055e10 | DAT_08055e10 | 0x0000190e | CYBERNETIC_MAGICIAN_CID | card_info.inc 新建; pw=59023523; "Cybernetic Magician" |
| 0x08055e20 | DAT_08055e20 | 0x0000188e | FORCED_CEASEFIRE_CID | card_info.inc 新建; pw=97806240; "Forced Ceasefire" |
| 0x08055e3c | DAT_08055e3c | 0x000019ae | ANCIENT_GEAR_DRILL_CID | card_info.inc 复用 |
| 0x08055e50 | DAT_08055e50 | 0x000019b6 | DAMAGE_CONDENSER_CID | card_info.inc 新建; pw=28378427; "Damage Condenser" |
| 0x08055e7c | DAT_08055e7c | 0x00001661 | TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID | card_info.inc 复用 |
| 0x08055e80 | DAT_08055e80 | 0x000014ea | SPELL_REPRODUCTION_CID | card_info.inc 新建; pw=29228529; "Spell Reproduction" |
| 0x08055e8c | DAT_08055e8c | 0x0000165f | WICKED_BREAKING_FLAMBERGE_BAOU_CID | card_info.inc 复用 |
| 0x08055ea0 | DAT_08055ea0 | 0x0000198c | ARMED_DRAGON_LV10_CID | card_info.inc 复用 |
| 0x08055eac | DAT_08055eac | 0x000019af | PHANTASMAL_MARTYRS_CID | card_info.inc 新建; pw=93224848; "Phantasmal Martyrs" |

#### Seg-4b (slots in 0x08055ebc..0x080565e8)

| 槽地址 | 槽标签 | 值 | 常量名 | 来源 |
|--------|--------|-----|--------|------|
| 0x08055edc | DAT_08055edc | 0x00001617 | BREAKER_MAGICAL_WARRIOR_CID | card_info.inc 新建; pw=71413901; "Breaker the Magical Warrior" |
| 0x08055ee0 | DAT_08055ee0 | 0x0000128e | HANNIBAL_NECROMANCER_CID | card_info.inc 复用 |
| 0x08055eec | DAT_08055eec | 0x00001615 | MAGICAL_MARIONETTE_CID | card_info.inc 复用 |
| 0x08055f08 | DAT_08055f08 | 0x00001631 | MIRACLE_RESTORING_CID | card_info.inc 复用 |
| 0x08055f1c | DAT_08055f1c | 0x00001634 | ANTI_SPELL_CID | card_info.inc 新建; pw=53112492; "Anti-Spell" |
| 0x08055f70 | DAT_08055f70 | 0x000015cf | KIRYU_CID | card_info.inc 复用 |
| 0x08055f74 | DAT_08055f74 | 0x00001388 | lookup_equip_card_score_cid_1388 | card_info.inc 新建; gap CID; neutral name |
| 0x08055f78 | DAT_08055f78 | 0x000010f8 | MOOYAN_CURRY_CID | card_info.inc 新建; pw=58074572; "Mooyan Curry" |
| 0x08055f80 | DAT_08055f80 | 0x000012c6 | cid_12c6 | card_info.inc 复用 (line 886) |
| 0x08055f9c | DAT_08055f9c | 0x000014fd | MAHARAGHI_CID | card_info.inc 新建; pw=40695128; "Maharaghi" |
| 0x08055fa4 | DAT_08055fa4 | 0x00001519 | OMINOUS_FORTUNETELLING_CID | card_info.inc 新建; pw=56995655; "Ominous Fortunetelling" |
| 0x08055fcc | DAT_08055fcc | 0x00001544 | DARK_COFFIN_CID | card_info.inc 复用 |
| 0x08055fd4 | DAT_08055fd4 | 0x0000153f | ORDEAL_OF_A_TRAVELER_CID | card_info.inc 新建; pw=39537362; "Ordeal of a Traveler" |
| 0x08055ff0 | DAT_08055ff0 | 0x00001599 | CARD_SHUFFLE_CID | card_info.inc -- 同 0x08055aa4; 复用同一 CID |
| 0x08056000 | DAT_08056000 | 0x000015a5 | REVERSAL_QUIZ_CID | card_info.inc 新建; pw=5990062; "Reversal Quiz" |
| 0x08056034 | DAT_08056034 | 0x00001685 | DARK_SCORPION_GORG_THE_STRONG_CID | card_info.inc 新建; pw=48768179; "Dark Scorpion - Gorg the Strong" |
| 0x08056044 | DAT_08056044 | 0x000015f1 | SPELL_SHIELD_TYPE8_CID | card_info.inc 新建; pw=38275183; "Spell Shield Type-8" |
| 0x08056060 | DAT_08056060 | 0x00001656 | DARK_SCORPION_CHICK_CID | card_info.inc 复用 |
| 0x08056070 | DAT_08056070 | 0x00001679 | JUDGEMENT_OF_PHARAOH_CID | card_info.inc 复用 |
| 0x08056094 | DAT_08056094 | 0x00001776 | CORPSE_OF_YATA_GARASU_CID | card_info.inc 复用 |
| 0x080560a0 | DAT_080560a0 | 0x0000175a | MYSTIK_WOK_CID | card_info.inc 新建; pw=80161395; "Mystik Wok" |
| 0x080560bc | DAT_080560bc | 0x0000184e | FUH_RIN_KA_ZAN_CID | card_info.inc 新建; pw=1781310; "Fuh-Rin-Ka-Zan" |
| 0x080560d4 | DAT_080560d4 | 0x00001916 | PROTECTIVE_SOUL_AILIN_CID | card_info.inc 新建; pw=11678191; "Protective Soul Ailin" |
| 0x080560e8 | DAT_080560e8 | 0x00000197 | lookup_equip_score_mooyan_p0 | RENAME (score literal); med-conf label; Mooyan Curry player 0 score |
| 0x08056100 | DAT_08056100 | 0x000001c7 | lookup_equip_score_a_rival_appears_p1 | RENAME; "A Rival Appears!" player 1 score 0x1c7 |
| 0x08056118 | DAT_08056118 | 0x00000199 | lookup_equip_score_mooyan_p1 | RENAME; Mooyan Curry player 1 score 0x199 |
| 0x0805613c | DAT_0805613c | 0x000001ad | lookup_equip_score_b_0x1ad | RENAME (shared score) |
| 0x0805616c | DAT_0805616c | 0x000001b9 | lookup_equip_score_b_0x1b9 | RENAME |
| 0x08056198 | DAT_08056198 | 0x000001ab | lookup_equip_score_b_0x1ab | RENAME |
| 0x080561b0 | DAT_080561b0 | 0x000001bf | lookup_equip_score_b_0x1bf | RENAME |
| 0x080561c8 | DAT_080561c8 | 0x000001a9 | lookup_equip_score_b_0x1a9 | RENAME |
| 0x080561dc | DAT_080561dc | 0x000001cd | lookup_equip_score_b_0x1cd | RENAME |
| 0x0805621c | DAT_0805621c | 0x000001c3 | lookup_equip_score_b_0x1c3 | RENAME |
| 0x08056234 | DAT_08056234 | 0x000001c5 | lookup_equip_score_b_0x1c5 | RENAME |
| 0x08056248 | DAT_08056248 | 0x000001af | lookup_equip_score_b_0x1af | RENAME |
| 0x08056250 | DAT_08056250 | 0x000001a7 | lookup_equip_score_b_0x1a7 | RENAME |
| 0x08056278 | DAT_08056278 | 0x000001b1 | lookup_equip_score_b_0x1b1 | RENAME |
| 0x08056288 | DAT_08056288 | 0x000001b7 | lookup_equip_score_b_0x1b7 | RENAME |
| 0x080562a0 | DAT_080562a0 | 0x000001c9 | lookup_equip_score_b_0x1c9 | RENAME |
| 0x080562b8 | DAT_080562b8 | 0x000001b3 | lookup_equip_score_b_0x1b3 | RENAME |
| 0x080562d0 | DAT_080562d0 | 0x000001b5 | lookup_equip_score_b_0x1b5 | RENAME |
| 0x08056318 | DAT_08056318 | 0x000001cb | lookup_equip_score_b_0x1cb | RENAME |
| 0x08056320 | DAT_08056320 | 0x000001a5 | lookup_equip_score_b_0x1a5 | RENAME |
| 0x08056328 | DAT_08056328 | 0x000001c1 | lookup_equip_score_b_0x1c1 | RENAME |
| 0x0805634c | DAT_0805634c | 0x000001cf | lookup_equip_score_b_0x1cf | RENAME |
| 0x080563c8 | DAT_080563c8 | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | 新建常量 duel_field.inc; 0xfb6=4022 sprite attr code for equip zone display |
| 0x080563f8 | DAT_080563f8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc 复用 |
| 0x080563fc | DAT_080563fc | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | 新建常量 duel_field.inc; gDuelPhaseFlags+0x4ac 装备激活步骤计数器 |
| 0x08056420 | DAT_08056420 | 0x00000107 | TRIGGER_OP_PARAM_107 | 新建常量 duel_field.inc; trigger_card_display_op31_if_not_active 参数 0x107 |
| 0x08056450 | DAT_08056450 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc 复用 |
| 0x08056474 | DAT_08056474 | 0x000010e7 | MALEVOLENT_NUZZLER_CID | card_info.inc 新建; pw=99597615; "Malevolent Nuzzler"; tick_equip_activation BST dispatch |
| 0x08056488 | DAT_08056488 | 0x00001294 | CHIMERA_FLYING_MYTHICAL_BEAST_CID | card_info.inc 新建; pw=4796100; "Chimera the Flying Mythical Beast" |
| 0x080564bc | DAT_080564bc | 0x000012a1 | PARASITE_PARACIDE_CID | card_info.inc 复用 |
| 0x080564c0 | DAT_080564c0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc 复用 |
| 0x080564c4 | DAT_080564c4 | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc 复用 |
| 0x080564ec | DAT_080564ec | 0x000017cc | WATAPON_CID | card_info.inc 复用 |
| 0x08056510 | DAT_08056510 | 0x0000190a | DARK_RULER_VANDALGYON_CID | card_info.inc 复用 |
| 0x08056514 | DAT_08056514 | 0x000010d6 | AXE_OF_DESPAIR_CID | card_info.inc 复用 |
| 0x08056518 | DAT_08056518 | 0x0201b290 | gDuelPhaseFlags | ewram.inc 复用 |
| 0x0805651c | DAT_0805651c | 0x000004ac | EQUIP_ACTIVATION_STEP_OFF | duel_field.inc 复用 |
| 0x08056574 | DAT_08056574 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc 复用 (gP1LifePoints+0x1d68 current player offset) |

---

### REF_SLOTS (USER-label + DATA-ref)

| 槽地址 | 槽标签 | 值 | GAS label | slot_label |
|--------|--------|-----|-----------|------------|
| 0x08055770 | DAT_08055770 | 0x080525d1 | `check_equip_slot_eligible_by_type_and_card_id_pair+1` | check_equip_slot_eligible_by_setcode_activation_and_zone_pair_fn_ptr |
| 0x08055c6c | PTR_gP1LifePoints_08055c6c | 0x0201c4e0 | `gP1LifePoints` | get_card_lp_cost_by_id_gp1lp |
| 0x08056454 | PTR_gP1LifePoints_08056454 | 0x0201c4e0 | `gP1LifePoints` | tick_equip_activation_gp1lp_a |
| 0x080564e8 | PTR_gP1LifePoints_080564e8 | 0x0201c4e0 | `gP1LifePoints` | tick_equip_activation_gp1lp_b |
| 0x08056570 | PTR_gP1LifePoints_08056570 | 0x0201c4e0 | `gP1LifePoints` | set_equip_activation_player_state_bit_gp1lp |

Note: DAT_08055770 fn-ptr slot already analyzed -- `check_equip_slot_eligible_by_type_and_card_id_pair` is in asm/05 @ 0x080525d0; fn-ptr = +1 (THUMB). Confidence: high (asm/06 line 4946 annotation + asm/05 line 21180 entry verified).

---

### RENAME_SLOTS (纯改名 + EOL)

#### DWORD_ slots in tick_equip_activation_with_lp_row_type8_entry

| 槽地址 | 旧标签 | 新标签 | EOL (ASCII) |
|--------|--------|--------|-------------|
| 0x080565bc | DWORD_080565bc | tick_lp_row_type8_entry_duel_state | gDuelPhaseFlags base; loaded with EQUIP_ACTIVATION_STEP_OFF |
| 0x080565c0 | DWORD_080565c0 | tick_lp_row_type8_entry_step_off | EQUIP_ACTIVATION_STEP_OFF = 0x4ac |
| 0x080565dc | DWORD_080565dc | tick_lp_row_type8_entry_all_slots_mask | 0xffff = LP_ROW_ALL_SLOTS_MASK |

Note: After EQ symbolization these three DWORD_ slots will be replaced by equate references; RENAME is fallback label only if Ghidra equate fails on them separately. Standard approach: equate them.

---

### FUNC_RENAME

None. All 22 functions already carry correct semantic names.

---

### PLATE (R5 -- full ASCII 重写或 substring 替换)

#### P1: tick_equip_activation_state_machine (0x080563cc)

Current plate: **CJK mojibake** (asm/06 line 6886 -- 装备激活... double-encoded).
Action: full ASCII rewrite.

```
Equip activation per-frame state machine hub, indeg=11.
Params: r0=card_entry_ptr, r1=second_param (encodes player/slot).
Reads [gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF] for current step (0/1/2).
Step 0: checks find_zone_slot_match_by_type_in_node_list; if found,
  calls trigger_card_display_op31_if_not_active(player_id, 0x107), returns -1.
  Else calls dispatch_card_effect_activation; if nonzero, reads
  [gDuelCardCtxBase+player*4+8]: if ==1 calls dispatch_card_effect_by_card_id,
  writes result to gP1LifePoints+0x1d40; else BST-dispatches on card_id
  (Malevolent Nuzzler/Axe of Despair/Chimera/Parasite Paracide/
   Dark Ruler Vandalgyon + others) to text_format_code, calls
  card_name_lookup_by_internal_id + format_game_text_with_text_arg +
  invoke_card_display_op_0x31_sub1.
Step 1 (LP wait): checks gP1LifePoints+0x1d40==0; if so calls
  set_lp_display_row_all_slots by card_id (Watapon/Dark Ruler Vandalgyon).
Step 2: increments [gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF].
Returns -1=done, 0=wait, 1=step-advance.
```

#### P2: tick_equip_activation_with_lp_row_type8_entry (0x08056598)

Current plate: **CJK mojibake** (asm/06 line 7169).
Action: full ASCII rewrite.

```
Equip activation entry wrapper with LP display row type8 init.
Called by tick_equip_activation_lp_cost_sprite_by_type (indeg=1).
Reads gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF step counter.
state==0xa: extracts player_id from card_entry[+2] bit0,
  calls set_lp_display_row_type8(player_id, 0xffff, 1),
  advances counter to 0xb; returns 0.
state==0xb: returns 1 (sequence complete).
other: calls tick_equip_activation_state_machine(card_entry);
  if returns 1, sets counter to 0xa (next phase). Returns 0.
```

#### P3: tick_equip_activation_with_lp_cost_sprite (0x080565e8) -- boundary note

This function starts at 0x080565e8 = Seg-5 boundary; its plate is CJK-mojibake (asm/06 line 7214). Seg-4 fixer **does not touch it** -- belongs to Seg-5.

#### P4: trigger_lp_row_type2_if_equip_tier_nonzero (0x08056380)

Current plate (asm/06 line 6830) contains **two** stale FUN_ references:
- `FUN_0805715c` -> `tick_equip_activation_state_by_phase` (asm/06 line 8950; confidence: high)
- `FUN_08059be0` -> `enqueue_equip_zone_sprite_with_lp_tier` (asm/06 line 14965; confidence: high)

Substring replace in plate (both replacements required):
- `FUN_0805715c` -> `tick_equip_activation_state_by_phase`
- `FUN_08059be0` -> `enqueue_equip_zone_sprite_with_lp_tier`

Exhaustive scan: before committing, grep `FUN_[0-9a-f]{8}` across all 5 PLATE blocks (P1-P5) and the full Seg-4 asm line range (lines covering 0x08055440..0x080565e8). Count must be 0 after all plate rewrites/substitutions are applied.

#### P5: tick_equip_activation_with_lp_row_type8_entry plate (line 7169)

Stale `FUN_08057430` -> `tick_equip_activation_lp_cost_sprite_by_type` (asm/06 line 9389; confidence: high).
But full rewrite already planned (P2 above replaces CJK plate entirely).

---

## carve 计划 (R7)

**无** -- Seg-4 内无 ROM_INCBIN 块。

---

## disasm 计划 (R4)

**无** -- Seg-4 内无需 R4 反汇编。

---

## 新增 constants / 全局

### card_info.inc 新建 CID (55 个)

按值排序。C5 穷举核验: `python -c "import re; content=open('constants/card_info.inc').read(); [print(hex(v), 'HIT') for v in [<all 55 values>] if re.search(f'0x0*{v:04x}', content, re.I)]"` 对全部 55 值执行, 输出 0 条命中 (2026-06-14 已跑, 确认 55 个全部不在 card_info.inc 中)。

| CID | 常量名 | passcode | 卡名 |
|-----|--------|----------|------|
| 0x10e7 | MALEVOLENT_NUZZLER_CID | 99597615 | Malevolent Nuzzler |
| 0x10f8 | MOOYAN_CURRY_CID | 58074572 | Mooyan Curry |
| 0x1190 | get_card_lp_cost_by_id_cid_1190 | (gap) | unassigned slot |
| 0x11cf | get_card_lp_cost_by_id_cid_11cf | (gap) | unassigned slot |
| 0x1294 | CHIMERA_FLYING_MYTHICAL_BEAST_CID | 4796100 | Chimera the Flying Mythical Beast |
| 0x12c3 | BRAIN_CONTROL_CID | 87910978 | Brain Control |
| 0x12de | DARK_MAGIC_CURTAIN_CID | 99789342 | Dark Magic Curtain |
| 0x12fd | SOLEMN_JUDGMENT_CID | 41420027 | Solemn Judgment |
| 0x12ff | SEVEN_TOOLS_OF_THE_BANDIT_CID | 3819470 | Seven Tools of the Bandit |
| 0x1321 | FINAL_DESTINY_CID | 18591904 | Final Destiny |
| 0x1388 | lookup_equip_card_score_cid_1388 | (gap) | unassigned slot |
| 0x1393 | get_card_lp_cost_by_id_cid_1393 | (gap) | unassigned slot |
| 0x1470 | JUDGMENT_OF_ANUBIS_CID | 55256016 | Judgment of Anubis |
| 0x14a7 | ROPE_OF_LIFE_CID | 93382620 | Rope of Life |
| 0x14b6 | DARK_BALTER_THE_TERRIBLE_CID | 80071763 | Dark Balter the Terrible |
| 0x14be | BARK_OF_DARK_RULER_CID | 41925941 | Bark of Dark Ruler |
| 0x14ea | SPELL_REPRODUCTION_CID | 29228529 | Spell Reproduction |
| 0x14fd | MAHARAGHI_CID | 40695128 | Maharaghi |
| 0x1519 | OMINOUS_FORTUNETELLING_CID | 56995655 | Ominous Fortunetelling |
| 0x153f | ORDEAL_OF_A_TRAVELER_CID | 39537362 | Ordeal of a Traveler |
| 0x156a | PUPPET_MASTER_CID | 41442341 | Puppet Master |
| 0x1599 | CARD_SHUFFLE_CID | 12183332 | Card Shuffle |
| 0x15a5 | REVERSAL_QUIZ_CID | 5990062 | Reversal Quiz |
| 0x15b5 | ROPE_OF_SPIRIT_CID | 37383714 | Rope of Spirit |
| 0x15f1 | SPELL_SHIELD_TYPE8_CID | 38275183 | Spell Shield Type-8 |
| 0x1617 | BREAKER_MAGICAL_WARRIOR_CID | 71413901 | Breaker the Magical Warrior |
| 0x1634 | ANTI_SPELL_CID | 53112492 | Anti-Spell |
| 0x166c | SKILL_DRAIN_CID | 82732705 | Skill Drain |
| 0x1685 | DARK_SCORPION_GORG_THE_STRONG_CID | 48768179 | Dark Scorpion - Gorg the Strong |
| 0x169d | get_card_lp_cost_by_id_cid_169d | (gap) | unassigned slot |
| 0x16a6 | SPELL_VANISHING_CID | 29735721 | Spell Vanishing |
| 0x1712 | DIMENSION_FUSION_CID | 23557835 | Dimension Fusion |
| 0x1741 | AGENT_OF_CREATION_VENUS_CID | 64734921 | The Agent of Creation - Venus |
| 0x175a | MYSTIK_WOK_CID | 80161395 | Mystik Wok |
| 0x1775 | RETURN_ZOMBIE_CID | 3072077 | Return Zombie |
| 0x179e | SPECIAL_HURRICANE_CID | 42598242 | Special Hurricane |
| 0x17a3 | SPELL_ECONOMICS_CID | 4259068 | Spell Economics |
| 0x17a7 | ENCHANTING_FITTING_ROOM_CID | 30531525 | Enchanting Fitting Room |
| 0x17bc | CRUSH_D_GANDRA_CID | 64681432 | Crush D. Gandra |
| 0x17f4 | ABYSSAL_DESIGNATOR_CID | 89801755 | Abyssal Designator |
| 0x1844 | BACK_TO_SQUARE_ONE_CID | 47453433 | Back to Square One |
| 0x184e | FUH_RIN_KA_ZAN_CID | 1781310 | Fuh-Rin-Ka-Zan |
| 0x1851 | SPELL_PURIFICATION_CID | 1669772 | Spell Purification |
| 0x188e | FORCED_CEASEFIRE_CID | 97806240 | Forced Ceasefire |
| 0x18cc | BATTERY_CHARGER_CID | 61181383 | Battery Charger |
| 0x1908 | BUBBLE_SHUFFLE_CID | 61968753 | Bubble Shuffle |
| 0x190e | CYBERNETIC_MAGICIAN_CID | 59023523 | Cybernetic Magician |
| 0x1916 | PROTECTIVE_SOUL_AILIN_CID | 11678191 | Protective Soul Ailin |
| 0x192b | A_RIVAL_APPEARS_CID | 5728014 | A Rival Appears! |
| 0x1932 | TRIAGE_CID | 30888983 | Triage |
| 0x1975 | DARK_DEAL_CID | 65824822 | Dark Deal |
| 0x19af | PHANTASMAL_MARTYRS_CID | 93224848 | Phantasmal Martyrs |
| 0x19b6 | DAMAGE_CONDENSER_CID | 28378427 | Damage Condenser |
| 0x19d5 | DEMISE_KING_OF_ARMAGEDDON_CID | 72426662 | Demise, King of Armageddon |
| 0x19e2 | MALFUNCTION_CID | 6137095 | Malfunction |

Note: The 5 gap CIDs (0x1190/0x11cf/0x1388/0x1393/0x169d) appear as BST range boundary nodes in `get_card_lp_cost_by_id` and `lookup_equip_card_score_by_card_id_and_player`. No card is assigned to these slot IDs in card-stats.s (confirmed: no `slot=0xXXXX` entry found). Names follow pattern `<func_abbrev>_cid_<hex>` (low-conf; neutral). Evidence: data/card-stats.s checked against all 5 values. (0x12c6 was previously listed as a gap CID but exists in card_info.inc line 886 as `cid_12c6`; slot 0x08055f80 now uses that existing equate.)

### duel_field.inc 新建常量 (4 个)

LP_COST_1500 (0x5dc) 和 LP_COST_3000 (0xbb8) 已存在于 duel_field.inc line 201/200 (file 03 Seg-4b 建), 本段**复用**不新建。

| 常量名 | 值 | 说明 |
|--------|-----|------|
| EQUIP_ACTIVATION_STEP_OFF | 0x000004ac | [gDuelPhaseFlags+0x4ac] 装备激活步骤计数器; used in 4 slots (0x080563fc/0x080564c4/0x0805651c/0x080565c0). Confidence: high -- asm/06 line 6913/7018/7066/7191 + multiple Seg-5..10 comments confirm "step counter offset". |
| TRIGGER_OP_PARAM_107 | 0x00000107 | trigger_card_display_op31_if_not_active 第 2 参数; asm/06 line 6931. Confidence: med -- only 1 slot, semantics from function call context. |
| LP_COST_5000 | 0x00001388 | get_card_lp_cost_by_id return value 5000 LP; asm/06 line 5697 DAT_08055c58 = 0x1388. 同值有 EQUIP_SLOT_CARD_ID_RANGE_MAX (card_id 域) 和 gap CID 节点, 三者跨域异义各建独立常量 (reviewer N2 确认). Confidence: high. |
| EQUIP_ZONE_SPRITE_ATTR | 0x00000fb6 | enqueue_equip_zone_sprite_at_slot: r2 arg to enqueue_sprite_attr_with_mode = 4022 (0xfb6). Confidence: high -- asm/06 line 6883 + function plate confirms "SPRITE_ATTR=0x0fb6 (4022)". |

---

## §5.1 登记 (Rule 3) -- 0 引用块

**无** -- Seg-4 内无 ROM_INCBIN 块, §5.1 不适用。

---

## 消费者证据 (R6) -- 关键槽语义

| 槽/常量 | 语义 | file:line 证据 | 置信度 |
|---------|------|---------------|--------|
| EQUIP_ACTIVATION_STEP_OFF=0x4ac | gDuelPhaseFlags+0x4ac 装备激活步骤计数器 | asm/06 line 6886 plate (tick_equip_activation_state_machine "读 [0x0201b290+0x4ac] 当前激活状态机步骤 (0/1/2)"); line 7169 plate (tick_equip_activation_with_lp_row_type8_entry); multiple Seg-5..Seg-10 comments | high |
| A_RIVAL_APPEARS_CID=0x192b | A Rival Appears! (pw=5728014) | asm/06 line 4762 "CARD_A_RIVAL_APPEARS = 0x192b (icid; 'A Rival Appears!')"; data/card-stats.s slot=0x192b | high |
| STAUNCH_DEFENDER_CID=0x1669 | Staunch Defender (pw=82102215) | asm/06 line 5035 "CARD_STAUNCH_DEFENDER = 0x1669 (icid; 'Staunch Defender')"; data/card-stats.s slot=0x1669 | high |
| BUBBLE_SHUFFLE_CID=0x1908 | Bubble Shuffle (pw=61968753) | asm/06 line 5036 "CARD_BUBBLE_SHUFFLE = 0x1908 (icid; 'Bubble Shuffle')"; data/card-stats.s slot=0x1908 | high |
| DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713 | Dedication through Light and Darkness | asm/06 line 5037 plate comment; data/card-stats.s slot=0x1713 | high |
| LP_COST_1500=0x5dc | get_card_lp_cost_by_id LAB_08055c3a: ldr r6,[DAT_08055c40]; duel_field.inc line 201 复用 | asm/06 line 5679: `.word 0x000005dc @ 08055c40` | high |
| EQUIP_ZONE_SPRITE_ATTR=0xfb6 | enqueue_equip_zone_sprite_at_slot r2 param | asm/06 line 6863 plate "SPRITE_ATTR=0x0fb6 (4022), MODE=2"; asm/06 line 6873 `ldr r2, DAT_080563c8` | high |
| ELIGIB_SPRITE_CTRL_OFF=0x1d68 | set_equip_activation_player_state_bit CURRENT_PLAYER_OFFSET | asm/06 line 7120 plate "CURRENT_PLAYER_OFFSET=0x1d68"; ewram.inc existing constant | high |
| gDuelCardCtxBase=0x0201e2a0 | tick_equip_activation_state_machine reads [+player*4+8] confirm flag | asm/06 line 6954 DAT_08056450; ewram.inc existing `.equ gDuelCardCtxBase` | high |
| TRIGGER_OP_PARAM_107=0x107 | trigger_card_display_op31_if_not_active(player_id, 0x107) | asm/06 line 6923 `ldr r1, DAT_08056420` then line 6925 `bl trigger_card_display_op31_if_not_active`; asm/06 line 6931 `.word 0x00000107` | med |

---

## 求助

1. **CARD_SHUFFLE_CID collision**: CID 0x1599 appears in both Seg-4a (DAT_08055aa4) and Seg-4b (DAT_08055ff0). Both = 0x1599. Both should use `CARD_SHUFFLE_CID`. C5 confirms this is the same card -- no conflict.

2. **gap CID 0x1388 dual use**: The same value 0x1388 appears as LP_COST_5000 (0x5dc slot DAT_08055c58 = 0x00001388) AND as a gap CID boundary node (DAT_08055f74 = 0x00001388). These are **different semantics at different slots**. Slot DAT_08055c58 at end of get_card_lp_cost_by_id = LP cost 5000. Slot DAT_08055f74 in lookup_equip_card_score_by_card_id_and_player = CID boundary 0x1388. The EQ approach puts different constants at each slot address -- no collision since Ghidra equates are per-slot.
   - Resolution: DAT_08055c58 -> EQ to LP_COST_5000; DAT_08055f74 -> EQ to lookup_equip_card_score_cid_1388. Both have distinct equate names targeting the same value -- this is permitted (C5: value collision, different semantics).

3. **Score literal slots (22 slots)**: The per-card-per-player equip scores in `lookup_equip_card_score_by_card_id_and_player` are raw literal values (0x1a5..0x1cf). They cannot be mapped to a named constant without full BST tracing (complex). Proposed as RENAME with descriptive label `lookup_equip_score_b_0x<val>`. Confidence: med for labels, high for values (all ROM-verified). If user prefers EQ with a generic constant prefix, confirm.
