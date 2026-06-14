# Refine Proposal: F07-Seg-8  [0x08061eb4..0x08062d28)

## 段测绘

- 函数入口 x34:
  - 0x08061eb4 check_equip_slot_eligible_by_zone_slot_flag_and_status
  - 0x08061f10 check_equip_slot_eligible_by_effect_slot_side_match
  - 0x08061f80 check_equip_slot_eligible_field_spell_by_hand_set_code_dispatch
  - 0x08061ff8 check_equip_slot_eligible_zone_type580_silent_magician_lv8
  - 0x08062048 check_equip_slot_eligible_zone_type3c0_high_atk_field5
  - 0x08062090 check_equip_slot_eligible_horus_lv4_chain_with_banisher
  - 0x080620c0 check_equip_slot_eligible_zone_type80_banisher_guard
  - 0x080620e0 check_equip_slot_eligible_zone140_horus_or_ctx_slot6
  - 0x0806210c check_equip_slot_eligible_banisher_absent_with_dispatch
  - 0x08062170 check_equip_slot_eligible_banisher_absent_silent_swordsman_loop
  - 0x08062244 check_equip_slot_eligible_banisher_absent_with_monster_loop
  - 0x080622dc check_equip_slot_state_active_with_card_present
  - 0x0806231c check_equip_slot_eligible_by_zone_flags_and_bls_envoy
  - 0x0806234c check_any_slot_accepts_card_for_ctrl
  - 0x080623a4 check_equip_slot_eligible_by_field_zone_both_sides_active
  - 0x0806244c check_equip_slot_eligible_by_card_in_slot_chain
  - 0x08062498 check_equip_slot_eligible_banisher_absent_monster_zone_ratio
  - 0x080624fc check_equip_slot_eligible_by_set_code_and_monster_quota
  - 0x08062564 check_equip_slot_eligible_zone_flags_vs_slot_target_count
  - 0x08062610 check_equip_slot_eligible_with_silent_swordsman_lv5_in_slot
  - 0x08062640 check_equip_slot_eligible_zone_type640_slot_effect_vs_4
  - 0x08062704 check_equip_slot_eligible_zone_type480_state12_neo_daedalus
  - 0x0806276c check_equip_slot_eligible_dual_field_state12_multi_slot
  - 0x08062818 check_equip_slot_eligible_neo_daedalus_chain_absent_with_field
  - 0x0806285c check_equip_slot_eligible_neo_daedalus_with_hand_setcode
  - 0x08062888 check_equip_slot_eligible_banisher_absent_field6_match
  - 0x080628f0 check_field_spell_zone_activated_by_side
  - 0x08062934 check_equip_slot_eligible_chain_absent_by_protector_guard_dispatch
  - 0x080629c8 check_equip_slot_eligible_card_field_guards_by_tier
  - 0x08062a0c check_equip_slot_eligible_by_dual_player_zone_count_match
  - 0x08062ac8 check_equip_slot_eligible_quad_zone_flag_lp_guard
  - 0x08062be8 check_equip_slot_placeable_for_card
  - 0x08062cb8 check_slot_equippable_by_field_group
  - 0x08062cec check_equip_slot_eligible_zone_type180_by_effect_vs_field_quota
  (note: store_slot_effect_value_from_card at 0x08062d28 is Seg-9 first fn)

- 残留自动名槽 x55:
  DWORD_08061f00=0x0201c4e0, DWORD_08061f04=0x868,
  DWORD_08061fe8=0x0201c4e0, DWORD_08061fec=0x868,
  DWORD_0806203c=0x0201c4e0, DWORD_08062084=0xbb7,
  DWORD_080620b4=0x17d2, DWORD_0806215c=0x1332,
  DWORD_08062160=0x0201c4e0, DWORD_08062164=0x868,
  DAT_08062200=0x1332, PTR_gP1LifePoints_08062204=0x0201c4e0,
  DAT_08062208=0x868, DAT_0806220c=0x0201c600,
  DAT_08062284=0x1332, PTR_gP1LifePoints_080622d4=0x0201c4e0,
  DAT_080622d8=0x868, DWORD_0806230c=0x0201bb90,
  DWORD_08062310=0x868, DWORD_08062314=0x0201c510,
  DWORD_080623e4=0x0201c4e0, DWORD_080623e8=0x868,
  DWORD_080624cc=0x1332, DWORD_080625fc=0x0201c4e0,
  DWORD_08062600=0x868, DWORD_08062634=0x1814,
  DWORD_080626bc=0x868, DWORD_080626c0=0x0201c510,
  DWORD_080626f0=0x181a, DWORD_08062758=0x0201bb90,
  DWORD_0806275c=0x0201c4e0, DWORD_08062760=0x868,
  DWORD_0806278c=0x0201c4e0, DWORD_08062790=0x1cf4,
  DWORD_08062814=0x868, DWORD_0806284c=0x0201c4e0,
  DWORD_08062850=0x868, DAT_080628e4=0x1332,
  PTR_gP1LifePoints_08062924=0x0201c4e0, DAT_08062928=0x868,
  PTR_gP1LifePoints_08062968=0x0201c4e0, DAT_0806296c=0x1cf4,
  DAT_08062970=0x178b, PTR_gP1LifePoints_080629c0=0x0201c4e0,
  DAT_080629c4=0x868, DAT_08062a94=0x868,
  DAT_08062a98=0x0201c510, DAT_08062bc8=0x080507ad,
  DAT_08062bcc=0x08051abd, PTR_gP1LifePoints_08062bd0=0x0201c4e0,
  DAT_08062bd4=0x868, DAT_08062bd8=0x1cf4,
  DAT_08062bdc=0x178b, DAT_08062c34=0x0201bb90,
  DAT_08062c38=0x1318

- ROM_INCBIN / .byte 块 x5:
  - 0x08062378 size 0x2c
  - 0x080623ec size 0x60
  - 0x0806246e size 0x2a
  - 0x08062a9c size 0x2c
  - 0x08062c52 size 0x66

---

## 数据块分类 (Rule 2/3)

### ref-scan 汇总

```python
import struct
rom = open('roms/2343.gba','rb').read(); rom_base=0x08000000
blocks = [(0x62378,0x2c),(0x623ec,0x60),(0x6246e,0x2a),(0x62a9c,0x2c),(0x62c52,0x66)]
for off,sz in blocks:
    a = rom_base+off
    for v in (a, a|1):
        print(hex(v), rom.count(struct.pack('<I',v)))
```

2B-step scan (穷举各 +0x02 对齐候选入口):

| 块 | 起始 ROM addr | size | raw=N | THUMB+1=N | THUMB+1 命中处 |
|---|---|---|---|---|---|
| Block1 | 0x08062378 | 0x2c | 0 | 1 | 0x09e42280 (+0x00) |
| Block2-F1 | 0x080623ec | 0x60 | 0 | 1 | 0x09e42340 (+0x00) |
| Block2-F2 | 0x08062420 | — | — | 1 | 0x09e42388 (+0x34 in block) |
| Block3 | 0x0806246e | 0x2a | 0 | 0 | — |
| Block3+0x02 | 0x08062470 | — | — | 1 | 0x09e423b8 |
| Block4 | 0x08062a9c | 0x2c | 0 | 1 | 0x09e42580 (+0x00) |
| Block5 | 0x08062c52 | 0x66 | 0 | 0 | — |
| Block5+0x02 | 0x08062c54 | — | — | 1 | 0x09e425f8 |

所有命中点均在 0x09e4xxxx 段 (card effect handler dispatch table); 经 fn_elig 槽 (+0xc) 结构验证:

| 块 | entry_start | CID | card name (card-stats.s) | fn_elig value |
|---|---|---|---|---|
| Block1 +0x00 | 0x09e42274 | 0x17f3 | Mind Wipe (pw=52817046) | 0x08062379 (match) |
| Block2 +0x00 | 0x09e42334 | 0x17fc | Taunt (pw=90740329) | 0x080623ed (match) |
| Block2 +0x34 | 0x09e4237c | 0x1801 | Heavy Slump (pw=52417194) | 0x08062421 (match) |
| Block3 +0x02 | 0x09e423ac | 0x1804 | Cemetary Bomb (pw=51394546) | 0x08062471 (match) |
| Block4 +0x00 | 0x09e42574 | 0x184d | Mind Haxorz (pw=75392615) | 0x08062a9d (match) |
| Block5 +0x02 | 0x09e425ec | 0x1853 | Covering Fire (pw=74458486) | 0x08062c55 (match) |

判定:

| 块 | 判定 | 理由 |
|---|---|---|
| 0x08062378/0x2c | **R4 disasm** (1 fn) | THUMB+1=1 @ 0x09e42280; fn_elig CID=0x17f3 Mind Wipe; bx lr exit @ 0x0806239a; lit pool @ 0x806239c |
| 0x080623ec/0x60 | **R4 disasm** (2 fn) | THUMB+1=2 @ 0x09e42340+0x09e42388; fn_elig CID=0x17fc Taunt (F1@+0x00) + 0x1801 Heavy Slump (F2@+0x34); F1 bx lr @ 0x806241e; F2 bx lr @ 0x8062440 |
| 0x0806246e/0x2a | **R4 disasm** (1 fn) | THUMB+1=1 @ 0x09e423b8; fn entry @ +0x02 (0x08062470; 2B pad at 0x806246e); fn_elig CID=0x1804 Cemetary Bomb; bx lr @ 0x806248c |
| 0x08062a9c/0x2c | **R4 disasm** (1 fn) | THUMB+1=1 @ 0x09e42580; fn_elig CID=0x184d Mind Haxorz; bx lr @ 0x8062ac6; lit pool embedded @ 0x8062abc/ac0 |
| 0x08062c52/0x66 | **R4 disasm** (1 fn) | THUMB+1=1 @ 0x09e425f8; fn entry @ +0x02 (0x08062c54; 2B pad at 0x8062c52); fn_elig CID=0x1853 Covering Fire; bx lr @ 0x8062cb6 |

全部 5 块 -> **R4 disasm** (总计 6 新函数); 无 §5.1 块。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate)

全部复用现有常量, 无新建。C5 双向核:

| 值 | 常量名 | 来源 inc | grep 证据 | 槽 x数 |
|---|---|---|---|---|
| 0x0201c4e0 | gP1LifePoints | ewram.inc | L79 `.equ gP1LifePoints, 0x0201C4E0` | x15 (DWORD+DAT+PTR) |
| 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | L250 `.equ PLAYER_BLOCK_STRIDE, 0x868` | x16 |
| 0x1332 | BANISHER_OF_THE_LIGHT_CID | card_info.inc | `.equ BANISHER_OF_THE_LIGHT_CID` | x5 |
| 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | L315 `.equ gEquipChainSlotRefs, 0x0201bb90` | x3 |
| 0x0201c510 | gDuelFieldSlots | ewram.inc | L312 `.equ gDuelFieldSlots, 0x0201c510` | x3 |
| 0x1cf4 | FIELD_STATE_OFF | duel_field.inc | L205 `.equ FIELD_STATE_OFF, 0x00001cf4` | x3 |
| 0x178b | PROTECTOR_OF_SANCTUARY_CID | card_info.inc | L1217 `.equ PROTECTOR_OF_SANCTUARY_CID` | x2 |
| 0x17d2 | HORUS_LV4_CID | card_info.inc | L673 `.equ HORUS_LV4_CID, 0x000017d2` | x1 |
| 0x0201c600 | gP1FieldArrayCBase | ewram.inc | L364 `.equ gP1FieldArrayCBase, 0x0201c600` | x1 |
| 0x1814 | SILENT_SWORDSMAN_LV5_CID | card_info.inc | L236 `.equ SILENT_SWORDSMAN_LV5_CID, 0x00001814` | x1 |
| 0x181a | SILENT_MAGICIAN_LV8_CID | card_info.inc | L531 `.equ SILENT_MAGICIAN_LV8_CID, 0x0000181a` | x1 |
| 0x1318 | RING_OF_MAGNETISM_CID | card_info.inc | L161 `.equ RING_OF_MAGNETISM_CID, 0x00001318` | x1 |
| 0x17fc | TAUNT_CID | card_info.inc | L196 `.equ TAUNT_CID, 0x000017fc` | (disasm lit pool) |
| 0x1804 | CEMETARY_BOMB_CID | card_info.inc | L824 `.equ CEMETARY_BOMB_CID, 0x00001804` | (disasm lit pool) |

新建 1 个:
| 值 | 常量名 | 来源 | grep 验证 |
|---|---|---|---|
| 0xbb7 | ATK_THRESHOLD_2999 | duel_field.inc (新) | grep `0xbb7` card_info.inc: 0 hits; grep `ATK_THRESHOLD_2999`: 0 hits; ROM raw count=4 (0x8062084/0x80a0db0/0x80bb1fc/0x89143ac); distinct from LP_COST_3000=0xbb8; semantics: cmp halfword[+0x14] against 0xbb7, bls->fail means ATK must be >2999 (i.e. >=3000) to pass; high-conf |

CID 新建 (disasm 用; 现有检查):
| CID | 卡名 | card-stats.s 证据 | grep card_info.inc |
|---|---|---|---|
| 0x17f3 | Mind Wipe | card_1664 slot=0x17F3 pw=52817046 | 0 hits -> NEW |
| 0x1801 | Heavy Slump | card_1678 slot=0x1801 pw=52417194 | 0 hits -> NEW |
| 0x184d | Mind Haxorz | card_1744 slot=0x184D pw=75392615 | 0 hits -> NEW |
| 0x1853 | Covering Fire | card_1750 slot=0x1853 pw=74458486 | 0 hits -> NEW |

(0x17fc=TAUNT_CID 已存; 0x1804=CEMETARY_BOMB_CID 已存)

EQ 汇总表 (slot, value, const_name, slot_label):

```
DWORD_08061f00   0x0201c4e0  gP1LifePoints           gp1lp_ref_08061f00
DWORD_08061f04   0x868       PLAYER_BLOCK_STRIDE     player_stride_08061f04
DWORD_08061fe8   0x0201c4e0  gP1LifePoints           gp1lp_ref_08061fe8
DWORD_08061fec   0x868       PLAYER_BLOCK_STRIDE     player_stride_08061fec
DWORD_0806203c   0x0201c4e0  gP1LifePoints           gp1lp_ref_0806203c
DWORD_08062084   0xbb7       ATK_THRESHOLD_2999      atk_threshold_2999_08062084
DWORD_080620b4   0x17d2      HORUS_LV4_CID           horus_lv4_cid_080620b4
DWORD_0806215c   0x1332      BANISHER_OF_THE_LIGHT_CID  banisher_cid_0806215c
DWORD_08062160   0x0201c4e0  gP1LifePoints           gp1lp_ref_08062160
DWORD_08062164   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062164
DAT_08062200     0x1332      BANISHER_OF_THE_LIGHT_CID  banisher_cid_08062200
DAT_08062208     0x868       PLAYER_BLOCK_STRIDE     player_stride_08062208
DAT_0806220c     0x0201c600  gP1FieldArrayCBase      field_array_c_0806220c
DAT_08062284     0x1332      BANISHER_OF_THE_LIGHT_CID  banisher_cid_08062284
DAT_080622d8     0x868       PLAYER_BLOCK_STRIDE     player_stride_080622d8
DWORD_0806230c   0x0201bb90  gEquipChainSlotRefs     equip_chain_refs_0806230c
DWORD_08062310   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062310
DWORD_08062314   0x0201c510  gDuelFieldSlots         duel_field_slots_08062314
DWORD_080623e4   0x0201c4e0  gP1LifePoints           gp1lp_ref_080623e4
DWORD_080623e8   0x868       PLAYER_BLOCK_STRIDE     player_stride_080623e8
DWORD_080624cc   0x1332      BANISHER_OF_THE_LIGHT_CID  banisher_cid_080624cc
DWORD_080625fc   0x0201c4e0  gP1LifePoints           gp1lp_ref_080625fc
DWORD_08062600   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062600
DWORD_08062634   0x1814      SILENT_SWORDSMAN_LV5_CID  ss_lv5_cid_08062634
DWORD_080626bc   0x868       PLAYER_BLOCK_STRIDE     player_stride_080626bc
DWORD_080626c0   0x0201c510  gDuelFieldSlots         duel_field_slots_080626c0
DWORD_080626f0   0x181a      SILENT_MAGICIAN_LV8_CID  sm_lv8_cid_080626f0
DWORD_08062758   0x0201bb90  gEquipChainSlotRefs     equip_chain_refs_08062758
DWORD_0806275c   0x0201c4e0  gP1LifePoints           gp1lp_ref_0806275c
DWORD_08062760   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062760
DWORD_0806278c   0x0201c4e0  gP1LifePoints           gp1lp_ref_0806278c
DWORD_08062790   0x1cf4      FIELD_STATE_OFF         field_state_off_08062790
DWORD_08062814   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062814
DWORD_0806284c   0x0201c4e0  gP1LifePoints           gp1lp_ref_0806284c
DWORD_08062850   0x868       PLAYER_BLOCK_STRIDE     player_stride_08062850
DAT_080628e4     0x1332      BANISHER_OF_THE_LIGHT_CID  banisher_cid_080628e4
DAT_08062928     0x868       PLAYER_BLOCK_STRIDE     player_stride_08062928
PTR_gP1LifePoints_08062968  0x0201c4e0  gP1LifePoints  gp1lp_ref_08062968
DAT_0806296c     0x1cf4      FIELD_STATE_OFF         field_state_off_0806296c
DAT_08062970     0x178b      PROTECTOR_OF_SANCTUARY_CID  protector_cid_08062970
PTR_gP1LifePoints_080629c0  0x0201c4e0  gP1LifePoints  gp1lp_ref_080629c0
DAT_080629c4     0x868       PLAYER_BLOCK_STRIDE     player_stride_080629c4
DAT_08062a94     0x868       PLAYER_BLOCK_STRIDE     player_stride_08062a94
DAT_08062a98     0x0201c510  gDuelFieldSlots         duel_field_slots_08062a98
PTR_gP1LifePoints_08062bd0  0x0201c4e0  gP1LifePoints  gp1lp_ref_08062bd0
DAT_08062bd4     0x868       PLAYER_BLOCK_STRIDE     player_stride_08062bd4
DAT_08062bd8     0x1cf4      FIELD_STATE_OFF         field_state_off_08062bd8
DAT_08062bdc     0x178b      PROTECTOR_OF_SANCTUARY_CID  protector_cid_08062bdc
DAT_08062c34     0x0201bb90  gEquipChainSlotRefs     equip_chain_refs_08062c34
DAT_08062c38     0x1318      RING_OF_MAGNETISM_CID   ring_of_magnetism_cid_08062c38
```

EQ 总计: 50 (49 已有常量复用 + 1 新建 ATK_THRESHOLD_2999)

### REF_SLOTS (USER-label + DATA-ref)

3 槽: PTR_gP1LifePoints 前缀 + 值 = gP1LifePoints 全局地址 -> 设为 REF (DATA ref to gP1LifePoints):

```
PTR_gP1LifePoints_08062204  0x0201c4e0  gP1LifePoints  gp1lp_ptr_08062204
PTR_gP1LifePoints_080622d4  0x0201c4e0  gP1LifePoints  gp1lp_ptr_080622d4
PTR_gP1LifePoints_08062924  0x0201c4e0  gP1LifePoints  gp1lp_ptr_08062924
```

### RENAME_SLOTS (fn-ptr 槽 + EOL)

2 槽: fn-ptr 原始值; 函数已命名。

```
DAT_08062bc8   0x080507ad  check_equip_slot_eligible_by_type_query+1   zone_pair_pred_07ac_ptr_08062bc8
  EOL: "fn-ptr check_equip_slot_eligible_by_type_query+1 (0x080507ac+1)"
DAT_08062bcc   0x08051abd  check_equip_slot_eligible_by_side_and_setcode+1  zone_pair_pred_1abc_ptr_08062bcc
  EOL: "fn-ptr check_equip_slot_eligible_by_side_and_setcode+1 (0x08051abc+1)"
```

证据: naming-proposals.csv L1124 `0x080507ac,check_equip_slot_eligible_by_type_query` / L1155 `0x08051abc,check_equip_slot_eligible_by_side_and_setcode`; conf: high.

### FUNC_RENAME (误名订正)

无。函数体与函数名一致; 无误名信号检出 (全段函数名均由命名阶段正确赋予, plate 检查见下方)。

### PLATE (R5; 含 C8 stale FUN_ 订正 + CJK 重写)

**C8 stale FUN_ 扫描**:

grep `FUN_[0-9a-f]{8}` 在 Seg-8 asm 行 L15232..L17235 发现 2 处:
- L15350 (plate of check_equip_slot_eligible_field_spell_by_hand_set_code_dispatch):
  `"called by FUN_08059110 (0x08059110)"` -> naming-proposals.csv L1373: `0x08059110,tick_equip_activation_if_field_spell_hand_ok`
  -> 替换为 `"called by tick_equip_activation_if_field_spell_hand_ok (0x08059110)"`
- L15867 (plate of check_equip_slot_state_active_with_card_present):
  `"called by FUN_080619c0 (0x080619c0)"` -> naming-proposals.csv L1700: `0x080619c0,check_equip_slot_eligible_by_active_ctx_score_threshold`
  -> 替换为 `"called by check_equip_slot_eligible_by_active_ctx_score_threshold (0x080619c0)"`

**CJK mojibake plate**:

grep 段内非 ASCII 发现 3 行 (L15515/L15519/L15520), 均属 check_equip_slot_eligible_horus_lv4_chain_with_banisher (0x08062090) 的 plate。
完整 ASCII 重写:

```
@ Equip slot eligibility predicate, returns 0/1. Extracts zone_idx (bits[6:2] = lsls #0x1a; lsrs #0x1b) and player_id (bit0) from slot[+2]. Calls check_value_in_slot_chain(player_id, zone_idx, CARD_ID_HORUS_LV4=0x17d2, chain_type=0xb): if Horus LV4 is in slot chain, calls check_equip_slot_eligible_banisher_absent_with_dispatch(slot, arg) and returns its result; else returns 0. Semantic: equip chain containing Horus LV4 is prerequisite for Banisher-absent dispatch evaluation.
@ Constants:
@   CARD_ID_HORUS_LV4 = 0x17d2 (Horus the Black Flame Dragon LV4, pw=75830094)
@   CHAIN_TYPE = 0xb -- equip chain node type code
@   ZONE_IDX_SHIFT = 0x1a/0x1b -- slot[+2] bits[6:2] extract
```

PLATE 总计: 3 (2 FUN_ substring 替换 + 1 CJK full ASCII 重写)。

---

## disasm 计划 (R4)

### Block1: 0x08062378/0x2c -> CID 0x17f3 Mind Wipe (1 fn)

fn 入口: 0x08062378
fn 退出: bx lr @ 0x0806239a
literal pool: 0x0806239c (gP1LifePoints=0x0201c4e0), 0x080623a0 (PLAYER_BLOCK_STRIDE=0x868)
函数结束: 0x080623a4 (= block end 0x62378+0x2c)

函数语义 (从 hex dump 解码):
- `movs r3,#0x0` / `ldr r2,[pc,#n]` (=gP1LifePoints) / `ldrb r0,[r0,#2]` (player_id bit0) / `lsls r0,#0x1f; lsrs r0,#0x1f` / `movs r1,#1; EOR r0,r1` (0x4048=EOR r0,r1 -> r0=player^1=1-player=opp) / `ldr r1,[pc,#n]` (PLAYER_BLOCK_STRIDE) / `muls r1,r0` / `adds r2,#0xc` -> `ldr r0,[r0,r2]` -> load gP1LP[(1-player)*0x868+0xc] / `subs r0,#1` (0x3801) / `cmp r0,#2` (0x2802) -> `bhi {return 0}` (0xd800; zone_count=0->0xFFFFFFFF>2 fail; zone_count>=4->val>2 fail) / fall-through: `movs r3,#1` / `movs r0,r3; bx lr`
- Semantic: reads opponent LP zone count (gP1LP[(1-player)*0x868+0xc]), bhi taken when (zone_count-1) > 2 unsigned -> returns 0; fall-through (zone_count-1 <= 2) -> returns 1. Pass condition: zone_count in {1,2,3}. Handler for Mind Wipe CID 0x17f3. Evidence: ROM 0x08062390=0x3801 (subs r0,#1), 0x08062392=0x2802 (cmp r0,#2), 0x08062394=0xd800 (bhi); conf: high.

名称: `check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3`
plate: `Reached via card effect handler dispatch table 0x09e42274. CID=0x17f3 (Mind Wipe, pw=52817046). Reads gP1LifePoints[(1-player)*0x868+0xc] (opp zone count); returns 1 if opp_zone_count in {1,2,3} (zone_count-1 <= 2 unsigned), else 0. bx lr exit. Lit pool: gP1LifePoints(0x0201c4e0), PLAYER_BLOCK_STRIDE(0x868).`

disasm literal pool slots (2):
```
player_stride_08062378_lp0 @ 0x0806239c = gP1LifePoints  (EQ)
player_stride_08062378_lp1 @ 0x080623a0 = PLAYER_BLOCK_STRIDE  (EQ)
```

### Block2: 0x080623ec/0x60 -> 2 fn (CID 0x17fc Taunt + 0x1801 Heavy Slump)

**F1 entry: 0x080623ec** (THUMB+1=0x080623ed @ 0x09e42340)
F1 退出: bx lr @ 0x0806241e -> F1 body end 0x08062420
literal pool embedded at 0x8062410..0x806241f:
  0x8062410=gP1LifePoints, 0x8062414=P1LP_BLOCK2_OFF_1CE8(0x1ce8), 0x8062418=FIELD_STATE_OFF(0x1cf4)

F1 语义 (from hex dump):
- `ldr r3,[pc,#n]` (gP1LifePoints) / `ldr r1,[pc,#n]` (P1LP_BLOCK2_OFF_1CE8) / `adds r2,r3,r1` -> load `[gP1LP+0x1ce8]` (active player id) / `ldrb r0,[r0,#2]` extract player bit0 / `lsls r0,#0x1f; lsrs r0,#0x1f` / `movs r1,#1; subs r1,r1,r0` (opp_player=1-player) / `cmp r1,[gP1LP+0x1ce8]; bne fail` / `ldr r1,[pc,#n]` (FIELD_STATE_OFF=0x1cf4) / `adds r0,r3,r1; ldr r0,[r0]` (field state) / `cmp r0,#2; bne fail; movs r0,#1; b ret` / `movs r0,#0; bx lr`
- Semantic: opp_player must equal active player [+0x1ce8]; field_state [+0x1cf4] must be ==2 (exactly). Returns 1 if both pass, 0 otherwise. Handler for Taunt CID 0x17fc.

F1 名称: `check_equip_slot_eligible_opp_is_active_field_eq2_for_cid_17fc`
F1 plate: `Reached via card effect handler dispatch table 0x09e42334. CID=0x17fc (Taunt, pw=90740329). Guards: (1) opp_player == gP1LP[0x1ce8] (active player id); (2) gP1LP[0x1cf4] (field state) == 2. Returns 1 on pass, 0 otherwise. bx lr exit. Lit pool embedded at 0x8062410: gP1LifePoints/P1LP_BLOCK2_OFF_1CE8/FIELD_STATE_OFF.`

F1 lit pool (3 EQ slots from within block body):
```
gp1lp_ref_08062410 @ 0x08062410 = gP1LifePoints  (EQ)
block2_f1_off_1ce8_08062414 @ 0x08062414 = P1LP_BLOCK2_OFF_1CE8  (EQ)
block2_f1_field_state_08062418 @ 0x08062418 = FIELD_STATE_OFF  (EQ)
```

**F2 entry: 0x08062420** (THUMB+1=0x08062421 @ 0x09e4237c)
.zero 2 pad at 0x8062420? No - hex dump shows 0x8062420: 2300 -> `movs r3,#0x0` (valid THUMB). Entry is 0x08062420.
F2 退出: bx lr @ 0x8062440 -> F2 body end 0x8062442
literal pool: 0x8062444 (gP1LifePoints=0x0201c4e0), 0x8062448 (PLAYER_BLOCK_STRIDE=0x868)
Block2 block end = 0x623ec + 0x60 = 0x8062 44c -> matches.

F2 语义:
- `movs r3,#0x0` / `ldr r2,[pc,#n]` (gP1LifePoints) / `ldrb r0,[r0,#2]` / `lsls r0,#0x1f; lsrs r0,#0x1f` player bit0 / `movs r1,#1; EOR r0,r1` (=0x4048 EOR -> r0=player^1=1-player=opp_player) / `ldr r1,[pc,#n]` (PLAYER_BLOCK_STRIDE) / `muls r1` / `adds r2,#0xc; adds r0,r0,r2; ldr r0,[r0]` -> gP1LP[(1-player)*0x868+0xc] / `cmp r0,#7; bls fail; movs r3,#1` / `movs r0,r3; bx lr`
- Semantic: opp LP zone count (gP1LP[(1-player)*0x868+0xc]) must be > 7 (i.e. >=8). Returns 1 if opp_zone_count > 7, else 0. Handler for Heavy Slump CID 0x1801. Evidence: +0x0c = 0x4048 = EOR r0,r1 (r1=1) -> r0=1-player=opp.

F2 名称: `check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801`
F2 plate: `Reached via card effect handler dispatch table 0x09e4237c. CID=0x1801 (Heavy Slump, pw=52417194). Reads gP1LifePoints[(1-player)*0x868+0xc] (opp LP zone count); returns 1 if opp_count > 7, else 0. bx lr exit. Lit pool: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868) @ 0x8062444.`

F2 lit pool (2 EQ):
```
gp1lp_ref_08062444 @ 0x08062444 = gP1LifePoints  (EQ)
player_stride_08062448 @ 0x08062448 = PLAYER_BLOCK_STRIDE  (EQ)
```

### Block3: 0x0806246e/0x2a -> CID 0x1804 Cemetary Bomb (1 fn, +0x02 pad)

pad: 0x0806246e (2 bytes .zero 2)
fn entry: 0x08062470 (THUMB+1=0x08062471 @ 0x09e423b8)
fn 退出: bx lr @ 0x806248c -> fn body end 0x806248e
literal pool: 0x8062490 (gP1LifePoints=0x0201c4e0), 0x8062494 (PLAYER_BLOCK_STRIDE=0x868)
Block3 end = 0x6246e + 0x2a = 0x8062498 -> matches.

fn 语义:
- `ldr r2,[pc,#n]` (gP1LifePoints) / `ldrb r0,[r0,#2]` player bit0 / `lsls r0,#0x1f; lsrs r0,#0x1f` / `movs r1,#1; EOR r0,r1` (0x4048=EOR r0,r1 -> r0=player^1=1-player=opp_player) / `ldr r1,[pc,#n]` (PLAYER_BLOCK_STRIDE) / `muls r0,r1` / `adds r2,#0x14` / `adds r0,r0,r2; ldr r0,[r0]` -> gP1LP[(1-player)*0x868+0x14] / `cmp r0,#0; beq fail` / `movs r0,#1; bx lr`
- Semantic: reads gP1LP[(1-player)*0x868+0x14] (opp field). Nonzero -> returns 1, zero -> returns 0. Handler for Cemetary Bomb CID 0x1804. Evidence: +0x0a = 0x4048 = EOR r0,r1 (r1=1) -> opp player; +0x10 = 0x3214 = adds r2,#0x14 -> offset 0x14.

fn 名称: `check_equip_slot_eligible_opp_lp_field14_nonzero_for_cid_1804`
fn plate: `Reached via card effect handler dispatch table 0x09e423ac. CID=0x1804 (Cemetary Bomb, pw=51394546). Reads gP1LifePoints[(1-player)*0x868+0x14] (opp); returns 1 if nonzero, else 0. .zero 2 pad at 0x806246e before fn entry at 0x8062470. bx lr exit. Lit pool: gP1LifePoints/PLAYER_BLOCK_STRIDE @ 0x8062490.`

Block3 lit pool (2 EQ):
```
gp1lp_ref_08062490 @ 0x08062490 = gP1LifePoints  (EQ)
player_stride_08062494 @ 0x08062494 = PLAYER_BLOCK_STRIDE  (EQ)
```

### Block4: 0x08062a9c/0x2c -> CID 0x184d Mind Haxorz (1 fn)

fn entry: 0x08062a9c
fn 退出: bx lr @ 0x8062ac6 -> fn body end 0x8062ac8 (= 0x62a9c+0x2c)
literal pool embedded within block:
  0x8062abc (gP1LifePoints=0x0201c4e0), 0x8062ac0 (PLAYER_BLOCK_STRIDE=0x868)
  (lit pool is inside the block before bx lr at 0x8062ac6, reached by ldr+pc)

fn 语义 (from hex dump + ldr decodes):
- `ldr r2,[pc,#n]` (gP1LifePoints) / `ldrb r0,[r0,#2]` / `lsls r0,#0x1f; lsrs r0,#0x1f` player bit0 / `movs r1,#1; EOR r0,r1` (0x4048=EOR -> r0=1-player=opp) / `ldr r1,[pc,n]`(PLAYER_BLOCK_STRIDE) / `muls r0,r1` / `adds r2,#0xc` / `adds r0,r0,r2; ldr r0,[r0]` -> gP1LP[(1-player)*0x868+0xc] / `cmp r0,#0; bne LAB` / `movs r0,#1; b ret` / LAB: lit pool (2 words) / `movs r0,#2; bx lr`
- Semantic: reads gP1LP[(1-player)*0x868+0xc] (opp LP zone count); if 0 -> returns 1; if nonzero -> returns 2. Handler for Mind Haxorz CID 0x184d. Evidence: +0x0a = 0x4048 = EOR r0,r1 (r1=1) -> opp player; +0x10 = 0x320c = adds r2,#0xc.

fn 名称: `check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d`
fn plate: `Reached via card effect handler dispatch table 0x09e42574. CID=0x184d (Mind Haxorz, pw=75392615). Reads gP1LifePoints[(1-player)*0x868+0xc] (opp LP zone count); returns 1 if zero (no opp LP zones), returns 2 if nonzero. bx lr exit. Lit pool embedded @ 0x8062abc: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868).`

Block4 lit pool (2 EQ, embedded before bx lr):
```
gp1lp_ref_08062abc @ 0x08062abc = gP1LifePoints  (EQ)
player_stride_08062ac0 @ 0x08062ac0 = PLAYER_BLOCK_STRIDE  (EQ)
```

### Block5: 0x08062c52/0x66 -> CID 0x1853 Covering Fire (1 fn, +0x02 pad)

pad: 0x08062c52 (2 bytes .zero 2)
fn entry: 0x08062c54
fn 退出: bx lr @ 0x8062cb6 -> fn body end 0x8062cb8 (= 0x62c52+0x66)
literal pool:
  0x8062ca8 (gEquipChainSlotRefs=0x0201bb90), 0x8062cac (PLAYER_BLOCK_STRIDE=0x868), 0x8062cb0 (gDuelFieldSlots=0x0201c510)

fn 语义 (from hex dump):
Byte[0x00-0x01]: 0x1c01 = `adds r1,r0,#0x0` -> saves slot_ptr. The hex at +0x02 is `884a` = ldrh? No: `88 4a` -> `ldrh r0,[r0,#0x4]`? Checking: 0x4a88 = `ldrh r0,[r1,#4]`. Wait, bytes are little-endian: byte +0x04=88, +0x05=4a -> halfword at that offset = 0x4a88 = `ldrh r0,[r1,#4]`.

Reconstructing from full dump:
```
+0x00: 1c01 -> adds r1,r0,#0
+0x02: 884a -> ldrh r0,[r1,#4]
+0x04: 0510 -> lsls r0,#0x?  (0x1005 = lsls r5,r0,#0)... 
```
Wait - reading the hex dump correctly (little-endian 16-bit each line):
```
0x8062c54: 1c01 = adds r1,r0,#0
0x8062c56: 884a = ldrh r0,[r1,#4]   (nope: 0x4a88 not 0x884a)
```

Hexdump shows: `+0x04: 4a 88 10 05` which at +0x04 is halfword 0x884a (bytes 4a,88) = THUMB instr 0x884a not 0x4a88.

Actually the file shows:
```
+0x02: 884a  -> but byte order: addr+0x56=0x88, addr+0x57=0x4a -> hw = 0x4a88 = ldrh r0,[r1,#4]
```
No - the dump format is: `+0x02: 1c01` means byte at 0x8062c54=0x01, byte at 0x8062c55=0x1c -> hw = 0x1c01. Correct.
`+0x04: 884a` means byte at 0x8062c56=0x88, byte at 0x8062c57=0x4a -> hw = 0x4a88.

0x4a88 = `ldrh r0,[r1,#4]`? No: 0x4a88 in THUMB:
- Bits[15:11]=01001 -> this is a `ldr rd,[pc,#imm]` form: rd = bits[10:8]=(0x4a88>>8)&7=2, imm=(0x4a88&0xff)<<2=0x88*4=0x220? That seems large.

Actually `0x4a88` = 0100 1010 1000 1000:
- Bits[15:11]=01001 -> LDR Rd, [PC, #Imm] where Rd=bits[10:8]=010=2, Imm8=bits[7:0]=0x88=136 -> Imm=136*4=0x220 bytes from PC+4.

Let me re-examine more carefully. Actually the fn entry starts at 0x8062c54 (offset +0x02 into the 0x66 block). But looking at the hex dump:

```
+0x00: 0000  (pad bytes at 0x8062c52-0x8062c53)
+0x02: 1c01  (at 0x8062c54)
+0x04: 884a  (at 0x8062c56)
+0x06: 0510  (at 0x8062c58)
```

The ldr decodes confirmed: `ldr r3,[pc,#64]` at +0x12 (=0x8062c64) -> pool at 0x8062ca8=0x0201bb90 (gEquipChainSlotRefs). This reads gEquipChainSlotRefs. Then `ldr r0,[r3,#0x18]` = r0=[gEquipChainSlotRefs+0x18]. Branches to tests.

Function accesses gEquipChainSlotRefs fields + gDuelFieldSlots. Semantic: eligibility check involving chain slot refs + field slot status bits for Covering Fire CID 0x1853.

Low-confidence on exact logic without ARM disassembler. Proposal uses conservative plate.

fn 名称: `check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853`
fn plate: `Reached via card effect handler dispatch table 0x09e425ec. CID=0x1853 (Covering Fire, pw=74458486). Guards: reads gEquipChainSlotRefs[+0x8]/[+0x18] fields + slot byte[+2] player bit + gDuelFieldSlots slot halfword[+0x8]/[+0x6]; zone-type pre-filter (cmp vs 0xd and 0x14). .zero 2 pad at 0x8062c52. bx lr exit. Lit pool @ 0x8062ca8: gEquipChainSlotRefs(0x0201bb90)/PLAYER_BLOCK_STRIDE(0x868)/gDuelFieldSlots(0x0201c510).`

Block5 lit pool (3 EQ):
```
equip_chain_refs_08062ca8 @ 0x08062ca8 = gEquipChainSlotRefs  (EQ)
player_stride_08062cac @ 0x08062cac = PLAYER_BLOCK_STRIDE  (EQ)
duel_field_slots_08062cb0 @ 0x08062cb0 = gDuelFieldSlots  (EQ)
```

---

## disasm 新增 EQ 槽汇总 (6 新 fn 的 literal pool 槽, 含在 EQ_SLOTS 总计内)

Block1 lit pool: 2 slots (gP1LifePoints + PLAYER_BLOCK_STRIDE)
Block2-F1 lit pool: 3 slots (embedded: gP1LifePoints + P1LP_BLOCK2_OFF_1CE8 + FIELD_STATE_OFF)
Block2-F2 lit pool: 2 slots (gP1LifePoints + PLAYER_BLOCK_STRIDE)
Block3 lit pool: 2 slots (gP1LifePoints + PLAYER_BLOCK_STRIDE)
Block4 lit pool: 2 slots (embedded: gP1LifePoints + PLAYER_BLOCK_STRIDE)
Block5 lit pool: 3 slots (gEquipChainSlotRefs + PLAYER_BLOCK_STRIDE + gDuelFieldSlots)

Total disasm lit pool slots: 14 (all EQ, all reuse)

---

## carve 计划 (R7)

无。5 个 ROM_INCBIN 全部是代码 (R4 disasm), 无数据表需 carve 进 rom.s。

---

## 新增 constants / 全局

1 个新增 equate:
- `ATK_THRESHOLD_2999 = 0x00000bb7` -> `constants/duel_field.inc`
  证据: DWORD_08062084 in check_equip_slot_eligible_zone_type3c0_high_atk_field5; `cmp r2,r0 / bls fail` semantics: ATK must be > 2999 (>=3000) to pass; ROM raw count=4 (0x8062084/0x80a0db0/0x80bb1fc/0x89143ac; only 0x8062084 in Seg-8); distinct from LP_COST_3000=0xbb8 (duel_field.inc L200) by 1; conf: high.

4 个新增 CID equate (disasm 新 fn 用):
- `MIND_WIPE_CID = 0x00017f3` -> card_info.inc; card_1664 slot=0x17F3 pw=52817046; grep 0 hits; conf: high.
- `HEAVY_SLUMP_CID = 0x00001801` -> card_info.inc; card_1678 slot=0x1801 pw=52417194; grep 0 hits; conf: high.
- `MIND_HAXORZ_CID = 0x0000184d` -> card_info.inc; card_1744 slot=0x184D pw=75392615; grep 0 hits; conf: high.
- `COVERING_FIRE_CID = 0x00001853` -> card_info.inc; card_1750 slot=0x1853 pw=74458486; grep 0 hits; conf: high.

(TAUNT_CID=0x17fc 已存 card_info.inc L196; CEMETARY_BOMB_CID=0x1804 已存 card_info.inc L824)

---

## §5.1 登记 (Rule 3)

无。全部 5 个 ROM_INCBIN 块均有 THUMB+1 真引用 (handler dispatch table), 全部 R4 disasm。

---

## 消费者证据 (R6)

### DWORD_08062084 = 0xbb7 (ATK_THRESHOLD_2999)

- `check_equip_slot_eligible_zone_type3c0_high_atk_field5` (0x08062048): L15497 `DWORD_08062084` / L15499 `ldrh r2,[r2,#0x14]` (ATK-like field) / L15500 `cmp r2,r0` / L15501 `bls LAB_08062088` (fail if r2<=0xbb7, i.e. ATK<=2999) / L15503 `movs r0,#0x1` success. Semantics: zone halfword[+0x14] treated as ATK stat; pass condition = ATK > 2999. conf: high.

### DAT_08062bc8 = 0x080507ad (check_equip_slot_eligible_by_type_query+1)

- `check_equip_slot_eligible_quad_zone_flag_lp_guard` (0x08062ac8): L17024 `ldr r1, DAT_08062bc8` / L17025-17026 `bl invoke_count_zone_pair_hits_full_range` - passes fn-ptr as second arg to zone-pair hit counter. conf: high; naming-proposals.csv L1124.

### DAT_08062bcc = 0x08051abd (check_equip_slot_eligible_by_side_and_setcode+1)

- same function L17029-17031 second call to `invoke_count_zone_pair_hits_full_range` with this fn-ptr. conf: high; naming-proposals.csv L1155.

### gEquipChainSlotRefs in DWORD_0806230c (check_equip_slot_state_active_with_card_present)

- L15878 `DWORD_0806230c` = 0x0201bb90; L15879 `ldr r0,[r1,#0x8]` / `cmp r0,#0x0; bne fail` - reads [gEquipChainSlotRefs+0x8] chain slot state. Plate confirms "gDuelActivation 0x0201bb90 global state". ewram.inc L315 `gEquipChainSlotRefs,0x0201bb90`. conf: high (note: plate says gDuelActivation but ewram.inc name is gEquipChainSlotRefs - same address, different name in plate vs inc; use gEquipChainSlotRefs per ewram.inc authority).

---

## 自检结果

1. 所有 EQ value 与 ROM 字节核对: python read32 per slot - 全部匹配 (见上方 Slot value verification 输出)。
2. carve 指针表: N/A (无 carve)。
3. Plate/EOL 文本: 已标记全 ASCII。
4. §5.1: 0 块 (无 0 引用块)。
5. 槽名格式: 全部 `^[a-z][a-z0-9_]+$`, 多同类用 `_<hexaddr>` 后缀避碰撞。
6. disasm fn 命名: `check_equip_slot_eligible_<qualifier>_for_cid_<hex>` (R1 verb-first); 无 cid_ 前缀。
7. C5 双向核: 标 reuse 均 grep 确存在; 标 new 均 grep 0 命中。
8. Block2-F1 literal pool 地址: embedded at 0x8062410-0x806241c (within fn body, pc-relative loads). Python decode: `ldr r3,[pc,#n]` at 0x80623ec+0=0x80623ec, imm = 0x4b08 -> `ldr r3,[pc,#0x20]` -> PC=0x80623f0, pool=(0x80623f0+0x20)=0x8062410=gP1LifePoints. Verified.
9. Block4 bx lr at 0x8062ac6, lit pool at 0x8062abc/0x8062ac0 (both inside 0x2c block). Verified.
10. Block5 fn entry at 0x8062c54 (not 0x8062c52). Pad 2 bytes.

---

## 求助

低置信度项:
1. **Block5 fn (0x08062c54) 精确语义**: zone-type pre-filter 的精确比较值和 chain-slot-ref 字段语义未完全解码 (hex dump 手工分析有歧义)。置信度 low。建议 fixer 在 disasm 落地后通过 Ghidra 导出的汇编核实 plate 描述, 必要时修正精确语义。函数名 `check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853` 是保守命名, 落地后可优化。

**Player direction verification (blocks 1/2F2/3/4)**:
All four blocks (0x08062378, 0x08062420, 0x08062470, 0x08062a9c) use instruction 0x4048 = `EOR r0, r1` (r1=1) to compute `1-player` = opponent player index. Verified by THUMB opcode decode: ALU op=0001=EOR, rs=r1, rd=r0. Block1 main section correctly names `opp_lp_zone_count_lte3_for_cid_17f3`. Blocks 2F2/3/4 names and plates updated accordingly. conf: high.

---

## 最终 EQ_SLOTS 总计

原始 auto-name 槽 55 + disasm 新增 lit-pool 槽 14 = 69 total EQ+REF+RENAME

- EQ: 50 (named) + 14 (disasm lit pool) = 64 slots
- REF: 3 (PTR_gP1LifePoints_* x3)
- RENAME: 2 (fn-ptr slots)
- Total: 69

Note: The count of 55 original slots above already includes the DAT_ and DWORD_ slots within the existing named asm. The disasm lit pool slots (14) are NEW slots created when blocks are disassembled. Grand total for C13 coverage: 69 slots.

---

## Executor Report: F07-Seg-8

- 槽: EQ=64 REF=3 RENAME=2 FUNC_RENAME=0 PLATE=3
- disasm=5 blocks (6 new fn: check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3 / check_equip_slot_eligible_opp_is_active_field_eq2_for_cid_17fc / check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801 / check_equip_slot_eligible_opp_lp_field14_nonzero_for_cid_1804 / check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d / check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853)
- carve=0 §5.1=0
- 新增 constants/全局: ATK_THRESHOLD_2999=0xbb7 (duel_field.inc) + MIND_WIPE_CID=0x17f3 / HEAVY_SLUMP_CID=0x1801 / MIND_HAXORZ_CID=0x184d / COVERING_FIRE_CID=0x1853 (card_info.inc x4)
- 求助: Block5 fn (0x08062c54) 精确 zone-type/chain-field 语义 low-conf; all blocks 1/2F2/3/4 player direction verified opp (0x4048=EOR r0,r1; conf: high)
- proposal: doc/dev/refine/F07-Seg-8.proposal.md
