# Refine Review: F11-Seg-6

> Reviewer: independent
> Proposal: doc/dev/refine/F11-Seg-6.proposal.md
> Module: asm/11_effect_slot_puzzletext.s [0x0808ea28, 0x0808f869]
> Actual range includes fn19 (enqueue_sprite_by_field_copy_count @ 0x0808f7c0, body ends 0x0808f869)
> Seg-7 starts at scan_field_slots_for_equip_chain_node_bitmap_update @ 0x0808f86c

---

## 独立复核关键步骤

### C13 slot count 独立核查

Python 扫描 asm lines 20625-22525 (1-indexed, `enqueue_paired_slot_sprite_attrs_for_player`..last line before `scan_field_slots_for_equip_chain_node_bitmap_update`):

```
Auto-named slots (DAT_/DWORD_/PTR_): 97
ROM_INCBIN/.byte-as-code count: 0
```

Result: 97 = 90 DAT_ + 7 PTR_gP1LifePoints_ — matches proposal claim exactly. 0 ROM_INCBIN confirmed.

### C4 ROM 字节核对 (16 槽抽查)

Python `struct.unpack("<I")` at ROM offset = addr - 0x08000000:

```
SPELL_ZONE_TARGET_CID_PACKED   0x0808eb54: 0x13680000  OK
SOLEMN_WISHES_SLOT_STATE_MASK  0x0808ed94: 0xa0280000  OK
FIRE_PRINCESS_SLOT_STATE_MASK  0x0808ef9c: 0xa2680000  OK
AMAZONESS_TIGER_SLOT_STATE_MASK 0x0808f2ac: 0xb0780000  OK
FATAL_ABACUS_SLOT_STATE_MASK   0x0808f44c: 0xa5f80000  OK
EQUIP_NODE_TAG_MASK            0x0808f6dc: 0x000fffff  OK
CRUSH_CARD_ZONE11_TAG          0x0808f6e0: 0x0002123b  OK
DECK_DEV_VIRUS_ZONE11_TAG      0x0808f7bc: 0x0002188c  OK
slot_set_code_array_neg_off_eb64 0x0808eb64: 0xfffffdb0  OK
THUNDER_NYAN_NYAN_CID          0x0808ebf0: 0x000013a4  OK
FIRE_PRINCESS_CID              0x0808eeac: 0x0000144d  OK
MYSTICAL_BEAST_SERKET_CID      0x0808f1b0: 0x0000147a  OK
KOZAKY_CID                     0x0808f218: 0x00001784  OK
CONVULSION_OF_NATURE_CID       0x0808f7e8: 0x00001510  OK
switchd_base_f818              0x0808f818: 0x0808f81c  OK
lp_block2_to_zone_chain_neg_off_f7b0 0x0808f7b0: 0xffffe438  OK
```

All 16 match ROM. C4 PASS.

### C5 NEW constants value-grep (13 values)

Python grep against constants/*.inc (case-insensitive, word-boundary):

```
0x13a4 (THUNDER_NYAN_NYAN_CID):       0 hits  OK
0x144d (FIRE_PRINCESS_CID):           0 hits  OK
0x147a (MYSTICAL_BEAST_SERKET_CID):   0 hits  OK
0x1510 (CONVULSION_OF_NATURE_CID):    0 hits  OK
0x1784 (KOZAKY_CID):                  0 hits  OK
0xa0280000 (SOLEMN_WISHES mask):      0 hits  OK
0xa2680000 (FIRE_PRINCESS mask):      0 hits  OK
0xa5f80000 (FATAL_ABACUS mask):       0 hits  OK
0xb0780000 (AMAZONESS_TIGER mask):    0 hits  OK
0x13680000 (SPELL_ZONE_TARGET_CID_PACKED): 0 hits  OK
0x0002123b (CRUSH_CARD_ZONE11_TAG):   0 hits  OK
0x0002188c (DECK_DEV_VIRUS_ZONE11_TAG): 0 hits  OK
0x000fffff (EQUIP_NODE_TAG_MASK):     0 hits  OK
```

All 13 confirmed new. C5 value-presence PASS — but see C6 naming issue below.

### KOZAKY CID distinction verified

```
constants/card_info.inc: KOZAKYS_SELF_DESTRUCT_CID = 0x18d7 (distinct)
constants/card_info.inc: GIANT_KOZAKY_CID          = 0x1914 (distinct)
card-stats.s L~20373: card_1566 @ Kozaky slot=0x1784 pw=99171160  (confirmed)
```

KOZAKY_CID=0x1784 is the base "Kozaky" monster card, not a duplicate of either existing constant.

### CID card-stats.s verification (5 new CIDs)

```
0x13a4: card_0821 @ Thunder Nyan Nyan  slot=0x13A4  pw=70797118  CONFIRMED
0x144d: card_0916 @ Fire Princess      slot=0x144D  pw=64752646  CONFIRMED
0x147a: card_0952 @ Mystical Beast Serket slot=0x147A pw=89194033 CONFIRMED
0x1510: card_1083 @ Convulsion of Nature slot=0x1510 pw=62966332  CONFIRMED
0x1784: card_1566 @ Kozaky             slot=0x1784  pw=99171160  CONFIRMED
```

### Mask encoding verification (4 CID_SHIFTED values)

All four are `CID << 19` (= `lsls reg, #0x13` then cmp sentinel pattern):

```
SOLEMN_WISHES  0x1405 << 19 = 0xa0280000  OK  (Solemn Wishes pw=35346968 slot=0x1405)
FIRE_PRINCESS  0x144d << 19 = 0xa2680000  OK
FATAL_ABACUS   0x14bf << 19 = 0xa5f80000  OK  (Fatal Abacus pw=77910045 slot=0x14BF)
AMAZONESS_TIGER 0x160f << 19 = 0xb0780000 OK
```

Encoding pattern confirmed in ASM at e.g. 0x0808ed4a `ldr r0,[r4,#0x0]` -> `lsls r0,r0,#0x13` -> `cmp r0, DAT_0808ed94`. Values correct. **Naming suffix is wrong** — see C6 issue.

### C8 plate FUN_ current-name verification (5 of 13 sampled)

```
FUN_08044e30 -> update_duel_field_slot_sprite_state       asm/04_card_zone_sprite.s:L10823  OK
FUN_08090218 -> dispatch_equip_field_scan_sequence        asm/11_effect_slot_puzzletext.s:L23832  OK
FUN_0804a2c8 -> submit_equip_slot_sprite_zone11           asm/05_equip_eligibility_a.s:L2521  OK
FUN_080486e4 -> enqueue_equip_zone_sprite_by_side         asm/04_card_zone_sprite.s:L18695  OK
FUN_0806c368 -> enqueue_paired_zone_sprite_if_slot_matches asm/08_equip_oam_neodaed.s:L18537 OK
```

All 5 sampled addresses match label definitions. C8 PASS.

### C9 non-ASCII grep

Python scan of asm lines 20625-22525: 0 characters > 0x7f. C9 PASS.

### RENAME label format (C6)

All proposed RENAME labels match `^[a-z][a-z0-9_]+$`. No collision with existing labels in asm/11_effect_slot_puzzletext.s. Format C6 PASS for format check.

### switchD in fn19

DAT_0808f818 = 0x0808f81c (switchdataD label address). Ghidra switch labels present: `switchD_0808f816__switchD`, `switchD_0808f816__switchdataD_0808f81c`, `switchD_0808f816__caseD_{2,3,6,a}`. RENAME to `switchd_base_f818` is correct. C2 PASS.

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | 路线图 "Seg-6: 0x808e8fc..0x808f7c0" — proposal 说明 0x808e8fc 是 Seg-5 fn18 已处理; 实际代码从 0x808ea28 开始; fn19 起始 0x808f7c0 体到 0x808f869; Seg-7 从 0x808f86c 开始; 无跳号/回头 |
| C2 Rule2 | ✅ | 0 ROM_INCBIN / 0 .byte-as-code; switchD 已 Ghidra 解码 (case labels 存在); 无遗漏 |
| C3 Rule3 | ✅ | 无 §5.1 块; 段内无孤儿数据块需 ref-scan |
| C4 R1 值 | ✅ | 16 槽抽查全部与 ROM LE-word 一致 (含全部 4 掩码 + zone11 tag + 5 CID + switchD base + neg offset) |
| C5 R1 复用 | ✅ | 13 NEW 常量按值 grep constants/*.inc 全部 0 命中; KOZAKY_CID=0x1784 与 KOZAKYS_SELF_DESTRUCT_CID=0x18d7/GIANT_KOZAKY_CID=0x1914 无碰撞; CID 按 card-stats.s slot 确认 |
| C6 R2 名 | ❌ | 4 个 `_SLOT_STATE_MASK` 命名违反 codebase 既有约定; card_info.inc 已有 9 个同类常量均使用 `_CID_SHIFTED` 后缀 (DNA_TRANSPLANT_CID_SHIFTED/UNHAPPY_GIRL_CID_SHIFTED/HELPOEMER_CID_SHIFTED/GEARFRIED_IRON_KNIGHT_CID_SHIFTED 等); 这 4 个应改为 `_CID_SHIFTED` |
| C7 R3 接通 | ✅ | 无 REF 槽; PTR_gP1LifePoints_ 作 equate-based RENAME (与 Seg-3a/3b/5 一致) |
| C8 R5 现名 | ✅ | 5/13 FUN_ 抽查: 地址全部匹配当前定义; 13 个 FUN_ 全部在 proposal PLATE 表中列出 |
| C9 ASCII | ✅ | asm lines 20625-22525: 0 非 ASCII 字符 |
| C10 carve | ✅ | 无 carve; 无 fn-ptr+1 条目 |
| C11 误名 | ✅ | 抽查 fn07/fn11/fn19: enqueue_active_card_shape_sprites_in_zone (5 slots, test_slot_has_active_card Fire Princess, enqueue_sprite_attr_with_shape), scan_field_for_unpaired_equip_slot_update (Giant Kozaky active + Kozaky pair count both 0), enqueue_sprite_by_field_copy_count (count copies + switchD on slot_byte bits) — 与名称无矛盾 |
| C12 R6 | ✅ | 关键槽均有 card-stats.s slot= 行号证据 + 置信度 high/med; 无零容忍词 |
| C13 残留 | ✅ | python 独立统计 97 槽 (90 DAT_ + 7 PTR_); proposal C13 计数 73 EQ-REUSE + 17 raw-table = 90 DAT_ + 7 PTR_ = 97/97; 无遗漏 (但见修改清单 #2 关于 eb54 双重处理的歧义) |

---

## 状态: NEEDS_FIX

---

## 修改清单 (逐条可执行)

### #1 — C6 — 4 个 `_SLOT_STATE_MASK` 改为 `_CID_SHIFTED`

**问题**: card_info.inc 已有 9 个常量使用 `_CID_SHIFTED` 后缀 (HAMON_LORD_CID_SHIFTED=0xcd200000, DNA_TRANSPLANT_CID_SHIFTED=0xb8f80000, UNHAPPY_GIRL_CID_SHIFTED=0xba180000, HELPOEMER_CID_SHIFTED=0xab880000, EKIBYO_DRAKMORD_CID_SHIFTED=0xa4e80000, GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000 等) 表示 `CID << 19` lsls sentinel 值。proposal 为相同编码模式引入 4 个 `_SLOT_STATE_MASK` 名称，违反已建立约定。

**操作**: 在 proposal §二 new EQ section 和 §七 NEW constants block 中，将以下 4 个名称全部替换：

```
SOLEMN_WISHES_SLOT_STATE_MASK  -> SOLEMN_WISHES_CID_SHIFTED
FIRE_PRINCESS_SLOT_STATE_MASK  -> FIRE_PRINCESS_CID_SHIFTED
FATAL_ABACUS_SLOT_STATE_MASK   -> FATAL_ABACUS_CID_SHIFTED
AMAZONESS_TIGER_SLOT_STATE_MASK -> AMAZONESS_TIGER_CID_SHIFTED
```

所有注释保持不变 (值/CID<<19/文件:行 证据) — 仅改后缀。

涉及槽: DAT_0808ed94, DAT_0808ee7c (SOLEMN_WISHES); DAT_0808ef9c (FIRE_PRINCESS); DAT_0808f44c, DAT_0808f570 (FATAL_ABACUS); DAT_0808f2ac (AMAZONESS_TIGER) — 共 6 次出现。

---

### #2 — C13 — 删除 RENAME 表中 DAT_0808eb54 的冗余 raw-label 行

**问题**: DAT_0808eb54 在 §二 NEW EQ 区已正确定义为 `SPELL_ZONE_TARGET_CID_PACKED, 0x13680000`。但 §三 RENAME_SLOTS 表同时列出了 `DAT_0808eb54 -> seg6_spell_zone_cid_packed_eb54`，并注 "`or raw label`"，对 fixer 产生歧义指令——两种处置不能同时执行。

**操作**: 删除 §三 RENAME_SLOTS raw 区中以下行：
```
| DAT_0808eb54 | seg6_spell_zone_cid_packed_eb54 | `.equ SPELL_ZONE_TARGET_CID_PACKED` used; or raw label |
```

保留 §二 NEW EQ 中 `SPELL_ZONE_TARGET_CID_PACKED, 0x13680000` 定义不变。

同步更新 §二 title "RENAME(13)" → "RENAME(12)" (去掉 eb54 后实际 RENAME 为 7 PTR_ + 5 raw = 12)。

---

## Reviewer Verdict: F11-Seg-6 = NEEDS_FIX(2 items)
