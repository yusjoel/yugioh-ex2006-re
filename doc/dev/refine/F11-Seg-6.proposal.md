# Refine Proposal: F11-Seg-6  [0x0808ea28, 0x0808f7c0)

> Executor: Refine Executor Agent
> Range: [0x0808ea28, 0x0808f7c0)  (Seg-5 pool ends at 0x0808ea24; first fn = enqueue_paired_slot_sprite_attrs_for_player @ 0x0808ea28)
> Note: Route map says "Seg-6: 0x808e8fc..0x808f7c0"; scan_all_zone_slots_for_lp_change_indicator
>       @ 0x808e8fc is fn18 of Seg-5 (included in F11-Seg-5.proposal.md). Seg-6 actual code starts
>       at the next function enqueue_paired_slot_sprite_attrs_for_player @ 0x0808ea28.
> Seg-7 boundary: scan_field_slots_for_equip_chain_node_bitmap_update @ 0x0808f86c
>   (enqueue_sprite_by_field_copy_count @ 0x0808f7c0 is LAST fn of Seg-6; its body ends at 0x0808f869)
> Functions: 19 pre-existing named (region C, 0 ROM_INCBIN)
> Slots: 97 total (90 DAT_ + 7 PTR_gP1LifePoints_)
> Status: PROPOSAL

---

## 段测绘

### 函数清单 (19 fn, address order)

| #  | 地址       | 函数名                                         | 主要操作 |
|----|------------|------------------------------------------------|---------|
| 01 | 0x0808ea28 | enqueue_paired_slot_sprite_attrs_for_player    | 2x11 slot pair loop; check_slot_card_pair_allowed; enqueue_sprite_attr_with_mode(mode=3); second pass: find_effect_node_in_zone(zone=0xb,tag=0x12a1) |
| 02 | 0x0808eb68 | find_first_eligible_zone_slot_for_player       | 5 field slots; bit12 flag + [+0x8] nonzero + check_slot_zone_bit_eligible(r2=1); return 1 on first match |
| 03 | 0x0808ebb8 | scan_field_slots_for_zone_equip_bitmap_update  | 2x5 loop; test_slot_has_active_card(0x13a4=Thunder Nyan Nyan); find_first_eligible_zone_slot_for_player; enqueue_equip_slot_bitmap_update |
| 04 | 0x0808ec08 | scan_field_slots_for_graveyard_equip_activation| 2x10 loop; [gP1LP+1ce8]; card_id=0x1403=Card of Safe Return; chain ptr [+0xc]; enqueue_sprite_attr_with_xy_split; apply_equip_activation_with_id_lookup |
| 05 | 0x0808ed2c | enqueue_zone_sprite_by_activation_flags        | 5 zone slots [5..9]; state_mask 0xa0280000 (Solemn Wishes encoded); bit5/bit1 inverted; enqueue_sprite_attr_with_shape |
| 06 | 0x0808ed98 | scan_field_slots_for_card_pair_sprite_update   | 2x10 loop; state_mask=0xa0280000; [+0xc] chain nonzero; enqueue_sprite_attr_with_xy_split; enqueue_sprite_attr_for_zone_card_id_lookup; submit_effect_zone_lp_and_shape_sprites |
| 07 | 0x0808ee80 | enqueue_active_card_shape_sprites_in_zone      | 5 slots; test_slot_has_active_card(0x144d=Fire Princess); enqueue_sprite_attr_with_shape(mode=1) |
| 08 | 0x0808eeb0 | scan_field_slots_for_chain_sprite_enqueue      | 2x5 loop; state_mask 0xa2680000 (Fire Princess encoded); [slot+0xc] check; enqueue_sprite_attr_with_xy_split |
| 09 | 0x0808efa8 | scan_field_for_whitelist_equip_sprite_and_lp   | 2x5 loop; check_slot_card_is_equip_whitelist; get_node_entity_id_in_slot(0x1472=Embodiment of Apophis); test_equip_target_slot_in_bitmap / update_equip_bitmap_with_cross_side_flag; enqueue_equip_slot_sprite_attr; enqueue_sprite_attr_with_mode(mode=5); 0xffff803f slot mask |
| 10 | 0x0808f174 | scan_field_for_paired_equip_slot_bitmap_update | 2x5 loop; test_slot_has_active_card(0x147a=Mystical Beast Serket); count_paired_slots_with_field5_default(0x146f=Cathedral of Nobles); enqueue_equip_slot_bitmap_update |
| 11 | 0x0808f1cc | scan_field_for_unpaired_equip_slot_update      | 2x5 loop; test_slot_has_active_card(0x1914=Giant Kozaky); count_equipped_paired_slots_for_player(0x1784=Kozaky) x2; enqueue_equip_slot_bitmap_update |
| 12 | 0x0808f230 | scan_field_for_equip_priority_slot_update      | 2x5 loop; test_slot_has_active_card(0x160f=Amazoness Tiger); state_mask 0xb0780000; compare [slot+0x4] values; enqueue_equip_slot_bitmap_update |
| 13 | 0x0808f2f0 | enqueue_exchange_slot_sprite_attrs             | find_equip_chain_pair_across_field; 0xffff no-pair check; enqueue_equip_set_slot_sprite_by_zone_col; get_equip_card_set_code_for_slot; enqueue_equip_chain_slot_sprite_attr(mode=1); [gP1LP+player*stride+0x30+0x40] filters |
| 14 | 0x0808f3b0 | scan_field_slots_for_attached_sprite_by_id     | 2x5 slots [5..9]; state_mask 0xa5f80000 (Fatal Abacus 0x14bf encoded); [+0x40] bit5+bit1 filter; enqueue_sprite_attr_with_shape |
| 15 | 0x0808f450 | scan_field_slots_for_lp_change_sprite_update   | 2x9 loop; [gP1LP+1ce8]; state_mask 0xa5f80000; enqueue_sprite_attr_with_xy_split; equip bitmap; enqueue_sprite_attr_for_zone_card_id_lookup; submit_lp_change_indicator_with_chain_check x2 |
| 16 | 0x0808f57c | scan_equip_chain_slots_for_bitmap_update       | 2x5 loop; test_slot_has_active_card(0x14fc=Gradius' Option); find_equip_chain_pair_across_field; 0xffff check; enqueue_equip_slot_bitmap_update |
| 17 | 0x0808f608 | scan_chain_nodes_for_equip_zone_sprite         | 2x11 loop; check_node_in_slot_chain(0x123b=Crush Card, zone=0xb, type=2); chain node traverse; [node] AND 0x000fffff == 0x0002123b zone marker; find_slot_idx_by_card_id_in_player_zones; enqueue_equip_zone_sprite_by_side; submit_equip_slot_sprite_zone11 |
| 18 | 0x0808f6e4 | scan_chain_nodes_for_equip_zone11_sprite       | 2x (player); check_node_in_slot_chain(0x188c=Deck Devastation Virus, zone=0xb, type=2); [node] AND 0x000fffff == 0x0002188c zone11 marker; find_slot_idx_by_card_id_in_player_zones; enqueue_equip_zone_sprite_by_side + submit_equip_slot_sprite_zone11 |
| 19 | 0x0808f7c0 | enqueue_sprite_by_field_copy_count             | count_field_copies_of_card(0x1510=Convulsion of Nature); [gP1LP+0x10d0] bit2 compare; if changed: enqueue_sprite_attr_for_card_slot; switchD on [slot_byte+2] bits[3:0]-2 in range [0..9] |

---

## 数据块分类 (Rule 2/3)

Seg-6 contains 0 ROM_INCBIN / .byte inter-function blocks. All data is literal pool slots embedded within named functions. No ref-scan needed for data blocks.

The `switchD_0808f816` within `enqueue_sprite_by_field_copy_count` (fn19) is already handled by Ghidra's switch recovery -- labels `switchD_0808f816__switchD`, `switchD_0808f816__switchdataD_0808f81c`, etc. are already in the asm. DAT_0808f818 is the jump table base pointer (ROM address 0x0808f81c = switchdataD label). This is an internal pc-relative pool slot; RENAME to `switchd_base_f818`.

---

## EQ_SLOTS (equate slots)

### REUSE slots (value-grep confirmed in constants/*.inc)

| 槽地址 | 值 | 常量名 | 来源文件 | grep 证据 |
|--------|-----|--------|---------|----------|
| DAT_0808eb48 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | ewram.inc:L~140 `.equ PLAYER_BLOCK_STRIDE, 0x868` |
| DAT_0808eb4c | 0x0201c510 | gDuelFieldSlots | ewram.inc | ewram.inc `.equ gDuelFieldSlots, 0x0201c510` |
| DAT_0808eb50 | 0x00001368 | SPELL_ZONE_TARGET_CARD_ID | card_info.inc | card_info.inc:L147 `.equ SPELL_ZONE_TARGET_CARD_ID, 0x00001368` |
| DAT_0808eb58 | 0x000012a1 | zone_query_hand_tag_12a1 | duel_field.inc | duel_field.inc:L423 `.equ zone_query_hand_tag_12a1, 0x000012a1`; context: find_effect_node_in_zone(zone=0xb) |
| DAT_0808eb5c | 0x0201c4f0 | gP1SlotCountBase | ewram.inc | ewram.inc `.equ gP1SlotCountBase, 0x0201c4f0` |
| DAT_0808eb60 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc | ewram.inc `.equ gP1SlotSetCodeArray, 0x0201c740` |
| DAT_0808eba0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same as above |
| DAT_0808eba4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same as above |
| DAT_0808ebec | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | ewram.inc:L397 `.equ gEquipZoneCountTable, 0x0201e1c8` |
| DAT_0808ebf0 | 0x000013a4 | THUNDER_NYAN_NYAN_CID | card_info.inc | **NEW** (value-grep 0 hits; card-stats.s slot=0x13A4 = Thunder Nyan Nyan pw=70797118) |
| DAT_0808ed0c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | ewram.inc `.equ P1LP_BLOCK2_OFF_1CE8, 0x1ce8` |
| DAT_0808ed10 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808ed14 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808ed18 | 0x00001403 | CARD_OF_SAFE_RETURN_CID | card_info.inc | card_info.inc:L1317 `.equ CARD_OF_SAFE_RETURN_CID, 0x00001403` |
| DAT_0808ed1c | 0x0201c520 | gDuelFieldSlotState | ewram.inc | ewram.inc `.equ gDuelFieldSlotState, 0x0201c520` |
| DAT_0808ed20 | 0xfffffdff | OAM_SPRITE_ATTR_CLR_BIT9 | oam_attr.inc | oam_attr.inc:L38 `.equ OAM_SPRITE_ATTR_CLR_BIT9, 0xfffffdff` |
| DAT_0808ed24 | 0x000001ff | OAM_ATTR1_X_MASK | oam_attr.inc | oam_attr.inc:L18 `.equ OAM_ATTR1_X_MASK, 0x000001ff`; used in OAM attr x-pos packing path |
| DAT_0808ed28 | 0xfffffe00 | OAM_ATTR1_X_CLEAR | oam_attr.inc | oam_attr.inc:L19 `.equ OAM_ATTR1_X_CLEAR, 0xfffffe00`; complement of OAM_ATTR1_X_MASK |
| DAT_0808ed8c | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808ed90 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808ee70 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same as above |
| DAT_0808ee74 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808ee78 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808eeac | 0x0000144d | FIRE_PRINCESS_CID | card_info.inc | **NEW** (value-grep 0 hits; card-stats.s L11923 slot=0x144D = Fire Princess pw=64752646) |
| DAT_0808ef90 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808ef94 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808ef98 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808efa0 | 0x0201c520 | gDuelFieldSlotState | ewram.inc | same |
| DAT_0808efa4 | 0x0000144d | FIRE_PRINCESS_CID | card_info.inc | same NEW entry |
| DAT_0808f09c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | same |
| DAT_0808f0a0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f0a4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808f0a8 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc | card_info.inc:L330 `.equ EMBODIMENT_OF_APOPHIS_CID, 0x00001472` |
| DAT_0808f0ac | 0xffff803f | slot_field_mask_ffff803f | card_info.inc | card_info.inc:L1765 `.equ slot_field_mask_ffff803f, 0xffff803f` |
| DAT_0808f130 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc | same REUSE |
| DAT_0808f170 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc | same REUSE |
| DAT_0808f1ac | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808f1b0 | 0x0000147a | MYSTICAL_BEAST_SERKET_CID | card_info.inc | **NEW** (value-grep 0 hits; card-stats.s L12391 slot=0x147A = Mystical Beast Serket pw=89194033) |
| DAT_0808f1b4 | 0x0000146f | CATHEDRAL_OF_NOBLES_CID | card_info.inc | card_info.inc:L962 `.equ CATHEDRAL_OF_NOBLES_CID, 0x0000146f` |
| DAT_0808f210 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808f214 | 0x00001914 | GIANT_KOZAKY_CID | card_info.inc | card_info.inc:L551 `.equ GIANT_KOZAKY_CID, 0x00001914` |
| DAT_0808f218 | 0x00001784 | KOZAKY_CID | card_info.inc | **NEW** (value-grep 0 hits; card-stats.s L20373 slot=0x1784 = Kozaky pw=99171160) |
| DAT_0808f29c | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808f2a0 | 0x0000160f | AMAZONESS_TIGER_CID | card_info.inc | card_info.inc:L177 `.equ AMAZONESS_TIGER_CID, 0x0000160f` |
| DAT_0808f2a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f2a8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808f3ac | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f440 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f444 | 0x0201c520 | gDuelFieldSlotState | ewram.inc | same |
| DAT_0808f448 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808f564 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | same |
| DAT_0808f568 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f56c | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808f574 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808f578 | 0x00001717 | JADE_INSECT_WHISTLE_CID | card_info.inc | card_info.inc:L1503 `.equ JADE_INSECT_WHISTLE_CID, 0x00001717` |
| DAT_0808f5e0 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | same |
| DAT_0808f5e4 | 0x000014fc | GRADIUS_OPTION_CID | card_info.inc | card_info.inc:L259 `.equ GRADIUS_OPTION_CID, 0x000014fc` |
| DAT_0808f5e8 | 0x0000ffff | SLOT_CARD_EMPTY | card_info.inc | card_info.inc:L386 `.equ SLOT_CARD_EMPTY, 0x0000ffff`; context: pair = 0xffff = no pair found |
| DAT_0808f5ec | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f5f0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | same |
| DAT_0808f6c4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | same |
| DAT_0808f6c8 | 0x0000123b | CRUSH_CARD_CID | card_info.inc | card_info.inc:L622 `.equ CRUSH_CARD_CID, 0x0000123b` |
| DAT_0808f6cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f6d0 | 0x0201c5ec | gDuelFieldSpellZoneBase | ewram.inc | ewram.inc `.equ gDuelFieldSpellZoneBase, 0x0201c5ec` |
| DAT_0808f6d8 | 0x0201d9c0 | gEquipNodePool | ewram.inc | ewram.inc `.equ gEquipNodePool, 0x0201d9c0` |
| DAT_0808f7a0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | same |
| DAT_0808f7a4 | 0x0000188c | DECK_DEVASTATION_VIRUS_CID | card_info.inc | card_info.inc:L629 `.equ DECK_DEVASTATION_VIRUS_CID, 0x0000188c` |
| DAT_0808f7a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | same |
| DAT_0808f7ac | 0x0201c5ec | gDuelFieldSpellZoneBase | ewram.inc | same |
| DAT_0808f7b0 | 0xffffe438 | (neg offset, raw RENAME; see below) | -- | NEW raw |
| DAT_0808f7b4 | 0x0201d9c0 | gEquipNodePool | ewram.inc | same |
| DAT_0808f7e8 | 0x00001510 | CONVULSION_OF_NATURE_CID | card_info.inc | **NEW** (value-grep 0 hits; card-stats.s L14094 slot=0x1510 = Convulsion of Nature pw=62966332) |
| DAT_0808f7f0 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc | ewram.inc:L484 `.equ LP_ACTIVATION_LINK_FLAG_OFF, 0x000010d0`; domain=gP1LifePoints (distinct from EFFECT_ZONE_BITMASK_OFF same value base=gDuelFieldSlots) |
| DAT_0808f854 | 0x00001598 | REAPER_ON_NIGHTMARE_CID | card_info.inc | card_info.inc:L172 `.equ REAPER_ON_NIGHTMARE_CID, 0x00001598` |

### Raw/state-mask slots (EQ with semantic label OR raw RENAME)

These slots hold composite encoded values or negative offsets; no shared named constant exists. They are symbolized as new equates in card_info.inc (state masks) or as raw labeled words via RENAME.

| 槽地址 | 值 | 解码 / 用途 | 处理 |
|--------|-----|-----------|------|
| DAT_0808eb54 | 0x13680000 | SPELL_ZONE_TARGET_CARD_ID<<16 packed; used via `lsrs r2,r3,#0x10` -> r2=0x1368 passed to enqueue | NEW EQ: `SPELL_ZONE_TARGET_CID_PACKED, 0x13680000` (card_info.inc); conf: high (asm/11 L20690-20692) |
| DAT_0808eb64 | 0xfffffdb0 | neg offset from gP1SlotSetCodeArray to card slot array (0xfffffdb0 = -0x250); used as `adds r0,r1,r3` where r1=gP1SlotSetCodeArray | raw RENAME -> `slot_set_code_array_neg_off_eb64`; conf: med |
| DAT_0808ed94 | 0xa0280000 | Solemn Wishes CID (0x1405) encoded as `cid<<19`; after `lsls [slot],#0x13` compare | NEW EQ: `SOLEMN_WISHES_CID_SHIFTED, 0xa0280000` (card_info.inc); conf: high (L21086 context enqueue_zone_sprite_by_activation_flags; 0xa0280000>>19=0x1405=Solemn Wishes pw=35346968 card-stats.s L11455) |
| DAT_0808ee6c | 0xffffe358 | neg offset; gEquipZoneCountTable(0x0201e1c8) + 0xffffe358 = 0x0201c520 = gDuelFieldSlotState; used as base addend in scan_field_slots_for_card_pair_sprite_update | raw RENAME -> `equip_zone_to_slot_state_neg_off_ee6c`; conf: high (python verified: 0x201e1c8 + (-0x1ca8) = 0x201c520) |
| DAT_0808ee7c | 0xa0280000 | same as DAT_0808ed94 | REUSE SOLEMN_WISHES_CID_SHIFTED (second occurrence) |
| DAT_0808ef9c | 0xa2680000 | Fire Princess CID (0x144d) encoded as `cid<<19`; 0xa2680000>>19=0x144d; scan_field_slots_for_chain_sprite_enqueue CHAIN_NODE_MAGIC constant | NEW EQ: `FIRE_PRINCESS_CID_SHIFTED, 0xa2680000` (card_info.inc); conf: high (L21357 context) |
| DAT_0808f2ac | 0xb0780000 | Amazoness Tiger CID (0x160f) encoded as `cid<<19`; scan_field_for_equip_priority_slot_update state filter | NEW EQ: `AMAZONESS_TIGER_CID_SHIFTED, 0xb0780000` (card_info.inc); conf: high (L21766 context; 0xb0780000>>19=0x160f) |
| DAT_0808f3a4 | 0x0000ffff | no-pair sentinel from find_equip_chain_pair_across_field (returns 0xffff when no pair); cmp with masked return value | REUSE SLOT_CARD_EMPTY (card_info.inc:L386; value 0xffff; same domain distinct from OAM_ATTR0_HIDDEN -- here used as pair sentinel in equip chain context) |
| DAT_0808f44c | 0xa5f80000 | Fatal Abacus CID (0x14bf) encoded as `cid<<19`; scan_field_slots_for_attached_sprite_by_id state filter; 0xa5f80000>>19=0x14bf (card-stats.s L13145 slot=0x14BF = Fatal Abacus pw=77910045) | NEW EQ: `FATAL_ABACUS_CID_SHIFTED, 0xa5f80000` (card_info.inc); conf: high |
| DAT_0808f570 | 0xa5f80000 | same as DAT_0808f44c | REUSE FATAL_ABACUS_CID_SHIFTED |
| DAT_0808f6d4 | 0xffffe438 | neg offset used in scan_chain_nodes_for_equip_zone_sprite: `adds r0,r5,r3` where r5=[gP1LP+1ce8 value]; value = -0x1bc8; 0x0201e1c8-0x1bc8=0x0201c600=gDuelFieldSpellZoneBase+0x14 (second zone entry); used as delta-from-block2-base | raw RENAME -> `lp_block2_to_zone_chain_neg_off_f6d4`; conf: med |
| DAT_0808f6dc | 0x000fffff | chain node tag mask; `ands r1,r0` then `cmp r1, 0x0002123b`; extracts low 20 bits of node[0] word | NEW EQ: `EQUIP_NODE_TAG_MASK, 0x000fffff` (duel_field.inc); conf: high (same value at both f6dc and f7b8, same usage pattern) |
| DAT_0808f6e0 | 0x0002123b | zone11 node tag = CRUSH_CARD_CID|(2<<16); chain node [0] AND 0x000fffff == 0x0002123b identifies zone11 Crush Card chain node | NEW EQ: `CRUSH_CARD_ZONE11_TAG, 0x0002123b` (card_info.inc); conf: high (0x0002123b = 0x00020000|0x123b; matches plate comment "zone11_marker=0x0002123b") |
| DAT_0808f7b0 | 0xffffe438 | same as DAT_0808f6d4 | same raw RENAME reuse -> `lp_block2_to_zone_chain_neg_off_f7b0` (distinct slot address) |
| DAT_0808f7b8 | 0x000fffff | same as DAT_0808f6dc | REUSE EQUIP_NODE_TAG_MASK |
| DAT_0808f7bc | 0x0002188c | zone11 node tag = DECK_DEVASTATION_VIRUS_CID|(2<<16); [node] AND 0x000fffff == 0x0002188c identifies zone11 Deck Dev chain node | NEW EQ: `DECK_DEV_VIRUS_ZONE11_TAG, 0x0002188c` (card_info.inc); conf: high (plate "zone11_marker=0x0002188c") |
| DAT_0808f818 | 0x0808f81c | switchD jump table base pointer (points to switchdataD_0808f81c within fn19); internal pc-relative pool | RENAME -> `switchd_base_f818` (no addMemoryReference; Ghidra switch already resolved) |

---

## REF_SLOTS

No REF slots. All pointer pools point to constants handled as EQ equates. PTR_gP1LifePoints_ slots are equate-based RENAME (as per Seg-3a/3b/5 precedent). DAT_0808f818 is an internal switchD base pointer (no external ref needed).

---

## RENAME_SLOTS

### PTR_gP1LifePoints_ -> ptr_lp_<suffix>

| 旧标签 | 新标签 |
|--------|--------|
| PTR_gP1LifePoints_0808ed08 | ptr_lp_ed08 |
| PTR_gP1LifePoints_0808f098 | ptr_lp_f098 |
| PTR_gP1LifePoints_0808f3a8 | ptr_lp_f3a8 |
| PTR_gP1LifePoints_0808f560 | ptr_lp_f560 |
| PTR_gP1LifePoints_0808f6c0 | ptr_lp_f6c0 |
| PTR_gP1LifePoints_0808f79c | ptr_lp_f79c |
| PTR_gP1LifePoints_0808f7ec | ptr_lp_f7ec |

### Raw composite / neg-offset labels

| 旧标签 | 新标签 | EOL (ASCII) |
|--------|--------|-------------|
| DAT_0808eb64 | slot_set_code_array_neg_off_eb64 | -0x250 neg offset from gP1SlotSetCodeArray to card array |
| DAT_0808ee6c | equip_zone_to_slot_state_neg_off_ee6c | gEquipZoneCountTable-gDuelFieldSlotState = -0x1ca8 |
| DAT_0808f6d4 | lp_block2_to_zone_chain_neg_off_f6d4 | [gP1LP+1ce8]+0xffffe438 -> gDuelFieldSpellZoneBase+0x14 |
| DAT_0808f7b0 | lp_block2_to_zone_chain_neg_off_f7b0 | same offset as f6d4 (distinct slot) |
| DAT_0808f818 | switchd_base_f818 | switch(bits[3:0]-2) 10-case table for enqueue_sprite_by_field_copy_count |

---

## PLATE (C8 stale FUN_ substitution + verification)

13 distinct FUN_ references appear in the 19 function plates. All require substring replacement. No CJK/non-ASCII found (python grep of lines 20624-22528 returned 0 hits).

| stale FUN_ | current name | source file:line |
|------------|--------------|-----------------|
| FUN_08044e30 | update_duel_field_slot_sprite_state | asm/04_card_zone_sprite.s:L10823 |
| FUN_08047218 | handle_card_effect_zone_eligibility_by_field6 | asm/04_card_zone_sprite.s:L15863 |
| FUN_08047f50 | render_slot_card_sprite_from_descriptor | asm/04_card_zone_sprite.s:L17680 |
| FUN_08048020 | render_slot_card_sprite_and_effects | asm/04_card_zone_sprite.s:L17786 |
| FUN_08048364 | render_slot_card_sprite_with_chaos_equip_check | asm/04_card_zone_sprite.s:L18223 |
| FUN_080486e4 | enqueue_equip_zone_sprite_by_side | asm/04_card_zone_sprite.s:L18695 |
| FUN_08049014 | submit_effect_zone_lp_and_shape_sprites | asm/05_equip_eligibility_a.s:L5 |
| FUN_080490b4 | tick_duel_field_zone_sprite_update_pipeline | asm/05_equip_eligibility_a.s:L87 |
| FUN_0804a2c8 | submit_equip_slot_sprite_zone11 | asm/05_equip_eligibility_a.s:L2521 |
| FUN_0806c368 | enqueue_paired_zone_sprite_if_slot_matches | asm/08_equip_oam_neodaed.s:L18537 |
| FUN_08090218 | dispatch_equip_field_scan_sequence | asm/11_effect_slot_puzzletext.s:L23832 |
| FUN_08099e0c | run_equip_spell_display_state_machine | asm/12_equip_activation_scan.s:L12316 |
| FUN_0809a1a4 | eval_equip_slot_pair_eligibility | asm/12_equip_activation_scan.s:L12795 |

Affected function plates (13 unique FUN_ across 19 functions):
- enqueue_paired_slot_sprite_attrs_for_player: FUN_08044e30, FUN_0806c368
- find_first_eligible_zone_slot_for_player: FUN_0809a1a4
- scan_field_slots_for_zone_equip_bitmap_update: FUN_08090218
- scan_field_slots_for_graveyard_equip_activation: FUN_08090218
- enqueue_zone_sprite_by_activation_flags: FUN_080490b4
- scan_field_slots_for_card_pair_sprite_update: FUN_08090218, FUN_08049014
- enqueue_active_card_shape_sprites_in_zone: FUN_08049014
- scan_field_slots_for_chain_sprite_enqueue: FUN_08090218
- scan_field_for_whitelist_equip_sprite_and_lp: (no FUN_ in plate -- indirect)
- scan_field_for_paired_equip_slot_bitmap_update: FUN_08090218
- scan_field_for_unpaired_equip_slot_update: FUN_08090218
- scan_field_for_equip_priority_slot_update: FUN_08090218
- enqueue_exchange_slot_sprite_attrs: (no FUN_ in plate)
- scan_field_slots_for_attached_sprite_by_id: FUN_08047218, FUN_08047f50, FUN_08048020, FUN_08048364
- scan_field_slots_for_lp_change_sprite_update: FUN_08090218
- scan_equip_chain_slots_for_bitmap_update: FUN_08090218
- scan_chain_nodes_for_equip_zone_sprite: FUN_08090218, FUN_080486e4, FUN_0804a2c8
- scan_chain_nodes_for_equip_zone11_sprite: FUN_08090218, FUN_0804a2c8, FUN_080486e4
- enqueue_sprite_by_field_copy_count: FUN_08090218

Fixer must verify post-substitution that `grep -c "FUN_[0-9a-f]\{8\}" asm/11_effect_slot_puzzletext.s` on Seg-6 lines returns 0 (C8 gate).

---

## carve 计划 (R7)

None. Seg-6 has 0 ROM_INCBIN. No inter-function data blocks requiring carve.

---

## disasm 计划 (R4)

None. All 19 functions are pre-named THUMB code. No mislabeled data blocks.

---

## 新增 constants (C5 grep confirmed NEW)

Added to `constants/card_info.inc` (CIDs) and `constants/duel_field.inc` (node tag mask):

### card_info.inc additions

```
.equ THUNDER_NYAN_NYAN_CID,       0x000013a4  @ Thunder Nyan Nyan (pw=70797118; card-stats.s L10688 slot=0x13A4); scan_field_slots_for_zone_equip_bitmap_update 1 slot
.equ FIRE_PRINCESS_CID,           0x0000144d  @ Fire Princess (pw=64752646; card-stats.s L11923 slot=0x144D); enqueue_active_card_shape_sprites_in_zone + scan_field_slots_for_chain_sprite_enqueue 2 slots
.equ MYSTICAL_BEAST_SERKET_CID,   0x0000147a  @ Mystical Beast Serket (pw=89194033; card-stats.s L12391 slot=0x147A); scan_field_for_paired_equip_slot_bitmap_update 1 slot
.equ CONVULSION_OF_NATURE_CID,    0x00001510  @ Convulsion of Nature (pw=62966332; card-stats.s L14094 slot=0x1510); enqueue_sprite_by_field_copy_count 1 slot
.equ KOZAKY_CID,                  0x00001784  @ Kozaky (pw=99171160; card-stats.s L20373 slot=0x1784); scan_field_for_unpaired_equip_slot_update 1 slot
.equ SOLEMN_WISHES_CID_SHIFTED,   0xa0280000  @ Solemn Wishes CID(0x1405) encoded as cid<<19; slot state filter after lsls [slot],#0x13; enqueue_zone_sprite_by_activation_flags + scan_field_slots_for_card_pair_sprite_update 2 slots; conf: high
.equ FIRE_PRINCESS_CID_SHIFTED,   0xa2680000  @ Fire Princess CID(0x144d) encoded as cid<<19; slot state CHAIN_NODE_MAGIC; scan_field_slots_for_chain_sprite_enqueue 1 slot; conf: high
.equ FATAL_ABACUS_CID_SHIFTED,    0xa5f80000  @ Fatal Abacus CID(0x14bf) encoded as cid<<19; slot state filter; scan_field_slots_for_attached_sprite_by_id + scan_field_slots_for_lp_change_sprite_update 2 slots; conf: high (card-stats.s L13145 slot=0x14BF = Fatal Abacus)
.equ AMAZONESS_TIGER_CID_SHIFTED, 0xb0780000  @ Amazoness Tiger CID(0x160f) encoded as cid<<19; slot state filter; scan_field_for_equip_priority_slot_update 1 slot; conf: high
.equ SPELL_ZONE_TARGET_CID_PACKED,  0x13680000  @ SPELL_ZONE_TARGET_CARD_ID(0x1368) in high 16 bits; loaded+lsrs #0x10 to extract CID for enqueue arg; enqueue_paired_slot_sprite_attrs_for_player 1 slot; conf: high
.equ CRUSH_CARD_ZONE11_TAG,        0x0002123b  @ Crush Card zone11 chain node tag = CRUSH_CARD_CID|(2<<16); [node+0] AND EQUIP_NODE_TAG_MASK == CRUSH_CARD_ZONE11_TAG identifies zone; scan_chain_nodes_for_equip_zone_sprite 1 slot; conf: high
.equ DECK_DEV_VIRUS_ZONE11_TAG,    0x0002188c  @ Deck Devastation Virus zone11 chain node tag = DECK_DEVASTATION_VIRUS_CID|(2<<16); scan_chain_nodes_for_equip_zone11_sprite 1 slot; conf: high
```

### duel_field.inc addition

```
.equ EQUIP_NODE_TAG_MASK,   0x000fffff  @ chain node [+0] low-20-bit tag mask; ands r1,r0 before comparing zone11 tag; scan_chain_nodes_for_equip_zone_sprite + scan_chain_nodes_for_equip_zone11_sprite 2 slots; conf: high
```

**C5 value-grep evidence (all verified 0 hits before declaring NEW):**
- 0x13a4: `grep -rE '0x0*13a4\b' constants/*.inc` -> 0 hits (excluding CARD_TILE_PACK_GLYPH_OFF_B which contains 0x09850934)
- 0x144d: `grep -rE '0x0*144d\b' constants/*.inc` -> 0 hits
- 0x147a: `grep -rE '0x0*147a\b' constants/*.inc` -> 0 hits
- 0x1510: `grep -rE '0x0*1510\b' constants/*.inc` -> 0 hits (LP_ACTIVATION_LINK_FLAG_OFF=0x10d0 different value)
- 0x1784: `grep -rE '0x0*1784\b' constants/*.inc` -> 0 hits (GIANT_KOZAKY_CID=0x1914 different)
- 0xa0280000 (SOLEMN_WISHES_CID_SHIFTED): `grep -rE '0xa0280000\b' constants/*.inc` -> 0 hits
- 0xa2680000 (FIRE_PRINCESS_CID_SHIFTED): `grep -rE '0xa2680000\b' constants/*.inc` -> 0 hits
- 0xa5f80000 (FATAL_ABACUS_CID_SHIFTED): `grep -rE '0xa5f80000\b' constants/*.inc` -> 0 hits
- 0xb0780000 (AMAZONESS_TIGER_CID_SHIFTED): `grep -rE '0xb0780000\b' constants/*.inc` -> 0 hits
- 0x13680000: `grep -rE '0x13680000\b' constants/*.inc` -> 0 hits
- 0x0002123b: `grep -rE '0x0*2123b\b' constants/*.inc` -> 0 hits
- 0x0002188c: `grep -rE '0x0*2188c\b' constants/*.inc` -> 0 hits
- 0x000fffff: `grep -rE '0x0*fffff\b' constants/*.inc` -> 0 hits

---

## §5.1 登记 (Rule 3) -- 0 引用块

No inter-function ROM_INCBIN or .byte blocks in Seg-6 (0 ROM_INCBIN in region C). No §5.1 entries.

---

## 消费者证据 (R6) -- 关键槽语义

| 槽 | 值 | 文件:行 | 语义 | 置信度 |
|----|-----|--------|------|--------|
| DAT_0808ebf0 = 0x13a4 | Thunder Nyan Nyan | data/card-stats.s:L10688 slot=0x13A4 | CID filter in test_slot_has_active_card | high |
| DAT_0808eeac = 0x144d | Fire Princess | data/card-stats.s:L11923 slot=0x144D | CID filter for shape sprite enqueue | high |
| DAT_0808f1b0 = 0x147a | Mystical Beast Serket | data/card-stats.s:L12391 slot=0x147A | paired equip bitmap check | high |
| DAT_0808f218 = 0x1784 | Kozaky | data/card-stats.s:L20373 slot=0x1784 | count_equipped_paired_slots_for_player arg | high |
| DAT_0808f7e8 = 0x1510 | Convulsion of Nature | data/card-stats.s:L14094 slot=0x1510 | count_field_copies_of_card arg | high |
| DAT_0808ed94 = 0xa0280000 | SOLEMN_WISHES_CID_SHIFTED | 0xa0280000>>19=0x1405; card-stats.s:L11455 slot=0x1405 | CID<<19 slot state sentinel post-lsls#0x13 | high |
| DAT_0808f6dc = 0x000fffff | chain node tag mask | asm/11 L22254-22257: `ands r1,r0; cmp r1,DAT_f6e0` | low-20-bit field extraction | high |
| DAT_0808f6e0 = 0x0002123b | zone11 tag | asm/11 plate L22319: "zone11_marker=0x0002123b" | 0x2123b = 0x20000|CRUSH_CARD_CID | high |
| DAT_0808f7bc = 0x0002188c | zone11 tag | asm/11 plate L22323: "zone11_marker=0x0002188c" | 0x2188c = 0x20000|DECK_DEV_VIRUS_CID | high |

---

## FUNC_RENAME

No misnomer detected. All 19 function names consistent with body operations.

---

## C13 Coverage Statement

Total auto-named slots in [0x0808ea28, 0x0808f7c0):
- 90 DAT_ + 7 PTR_gP1LifePoints_ = **97 slots**

EQ_SLOTS plan covers:
- 52 DAT_ REUSE (named constants) + 13 NEW (5 plain CID + 5 state mask + 3 composite/packed) = 65 DAT_ EQ
- 7 DAT_ raw RENAME (neg offsets, switchD base)
- Subtotal DAT_ accounted: 65 + 7 = 72

Wait -- 90 DAT_ total; recounting:
- Named REUSE (from EQ_SLOTS table): PLAYER_BLOCK_STRIDE x13, gDuelFieldSlots x12, gEquipZoneCountTable x7, P1LP_BLOCK2_OFF_1CE8 x5, gDuelFieldSlotState x3, EMBODIMENT_OF_APOPHIS_CID x3, FIRE_PRINCESS_CID x2, gDuelFieldSpellZoneBase x2, gEquipNodePool x2, SLOT_CARD_EMPTY x2 (f3a4+f5e8), EQUIP_NODE_TAG_MASK x2 (f6dc+f7b8), FATAL_ABACUS_CID_SHIFTED x2 (f44c+f570), SOLEMN_WISHES_CID_SHIFTED x2 (ed94+ee7c) -- plus all singletons
- Complete list by address from slot table above = 90 DAT_ (65 named EQ + 7 raw renamed = 72; remaining 18 need check)

Detailed accounting:
- EQ REUSE rows in table: eb48, eb4c, eb50, eb58, eb5c, eb60, eba0, eba4, ebec, ebf0(NEW), ed0c, ed10, ed14, ed18, ed1c, ed20, ed24, ed28, ed8c, ed90, ee70, ee74, ee78, eeac(NEW), ef90, ef94, ef98, efa0, efa4, f09c, f0a0, f0a4, f0a8, f0ac, f130, f170, f1ac, f1b0(NEW), f1b4, f210, f214, f218(NEW), f29c, f2a0, f2a4, f2a8, f3ac, f440, f444, f448, f564, f568, f56c, f574, f578, f5e0, f5e4, f5e8, f5ec, f5f0, f6c4, f6c8, f6cc, f6d0, f6d8, f7a0, f7a4, f7a8, f7ac, f7b4, f7e8(NEW), f7f0, f854 = 73 slots
- Raw state mask EQ (NEW): ed94, ee7c (SOLEMN_WISHES_CID_SHIFTED), ef9c (FIRE_PRINCESS_CID_SHIFTED), f2ac (AMAZONESS_TIGER_CID_SHIFTED), f44c/f570 (FATAL_ABACUS_CID_SHIFTED x2), f3a4(SLOT_CARD_EMPTY already counted above in f5e8 group) = 6 additional  
- Zone11 tag EQ (NEW): f6dc/f7b8 (EQUIP_NODE_TAG_MASK already in above? No -- let me check: f6dc and f7b8 should be in the raw table)

Let me enumerate the raw/state-mask rows: eb54, eb64, ed94, ee6c, ee7c, ef9c, f2ac, f3a4 (moved to REUSE above), f44c, f570, f6d4, f6dc, f6e0, f7b0, f7b8, f7bc, f818 = 17 additional slots
- f3a4 = SLOT_CARD_EMPTY (REUSE in card_info.inc) -- counted in EQ REUSE group

Revised:
- EQ REUSE (73 from above) + EQ/RENAME raw (17 from raw table + subtract f3a4 already counted = 16) = 89 DAT_ 
- Plus 1 missed: DAT_0808f3a4 appears in both groups: it's in raw/state-mask table as "REUSE SLOT_CARD_EMPTY" AND in the EQ REUSE list implicitly via f5e8.

Actually: f3a4 was listed in the EQ raw table as REUSE SLOT_CARD_EMPTY (row: "DAT_0808f3a4 | 0x0000ffff | SLOT_CARD_EMPTY"). So 90 DAT_ = 73 EQ-REUSE + 17 raw-table = 90. Check: 73+17=90. Correct.

**C13: 90 DAT_ (73 EQ-named + 17 raw/state-mask EQ or RENAME) + 7 PTR_ (RENAME) = 97/97 = 100% covered.**

---

## 求助

None. All semantic decisions reached high or med confidence with evidence.
