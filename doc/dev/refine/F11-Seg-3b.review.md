# Refine Review: F11-Seg-3b

Segment: `[0x080872e4, 0x08087d58)` — 15 functions, 0 ROM_INCBIN, 105 auto-name slots.
Proposal: `doc/dev/refine/F11-Seg-3b.proposal.md`

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-3a(✅ 3689026) -> Seg-3b(⬜) 严格地址序，无跳号/回头 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | OK | 段内 0 个 ROM_INCBIN/.byte 块，无需处理 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 段内无孤儿块；15 个函数入口均有 ≥1 THUMB+1 引用（最少 1 个，最多 30 个），无 0-ref 函数 |
| C4 R1 值 | EQ/REF slot 值 == ROM 4 字节小端 | OK | 独立 python 核查: 10 NEW CID slots + 10 REF slots + 15 STRIDE slots + 13 RENAME slots 全部匹配 ROM |
| C5 R1 复用 | 10 NEW CID 均 value-grep=0 (新建) | OK | grep constants/*.inc 全部 0 命中 |
| C5 REUSE | 所有标 REUSE 的常量确实存在 | OK | 抽查 MYSTIC_SWORDSMAN_LV2_CID/GREEN_GADGET_CID/PLAYER_BLOCK_STRIDE 等均存在 |
| C6 R2 名 | slot 标签 `^[a-z][a-z0-9_]+$`，无碰撞 | OK | 105 个 slot 标签全部通过正则；无重复 |
| C7 R3 接通 | REF/RENAME 槽有现有 USER-label（gP1LifePoints 等） | OK | gP1FieldArrayCBase/gP1SlotSetCodeArray/gP1HandSlotArray/gP1ChainZoneArray/gP1LifePoints 全在 ewram.inc 中定义 |
| C8 R5 现名 | 新 plate 无残留 FUN_ | OK | 14 个新 plate 文本独立检查: 0 个 FUN_ 引用；现有 plate L5203 含 `FUN_0809078c` 被新 plate 替换（新 plate 用 `count_zone_pair_hits_with_fn_ptr` 现名） |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | OK | 段内现有注释行 0 个非 ASCII；14 个新 plate 独立检查均纯 ASCII |
| C10 carve | 段内无 carve（无 ROM_INCBIN） | N/A | |
| C11 误名 | 函数体全局 vs 函数名无矛盾 | OK | 独立核查 7 个函数的 substate 字节（movs r1,#N 指令）: c/c/d/e/d/e/e 均与函数名后缀一致；FUNC_RENAME=0 结论成立 |
| C12 R6 | 关键槽语义有 file:line 证据 + 置信度 | OK | gP1HandSlotArray/gP1FieldArrayCBase/gP1SlotSetCodeArray/gP1ChainZoneArray 均有 asm/11 行号 + conf:high；zone_query_hand_tag_12a1 区别于 PARASITE_PARACIDE_CID 有明确说明 |
| C13 残留 | 段内 DAT_/PTR_ 全覆盖 | OK | python 独立清点: 92 DAT_ + 13 PTR_gP1LifePoints_ = 105 slots；EQ(82)+REF(10)+RENAME(13)=105，完全匹配 |

---

## 独立核查要点

### C4 ROM 字节核查（python struct.unpack_from 逐一核验）

所有 10 NEW CID slot、10 REF slot、15 STRIDE slot、13 RENAME slot 的 ROM 4 字节均与 proposal 列出的值完全一致。额外抽查 30 个 REUSE CID slot 也全部匹配。

### C5 NEW CID 卡名核查（card-stats.s 坐实）

| const_name | value | card-stats.s 记录 |
|---|---|---|
| ELEGANT_EGOTIST_CID | 0x10e4 | card_0288: Elegant Egotist slot=0x10E4 pw=90219263 |
| DARK_SAGE_CID | 0x146e | card_0944: Dark Sage slot=0x146E pw=92377303 |
| MIRAGE_KNIGHT_CID | 0x1643 | card_1308: Mirage Knight slot=0x1643 pw=49217579 |
| MYSTICAL_SHINE_BALL_CID | 0x173d | card_1512: Mystical Shine Ball slot=0x173D pw=39552864 |
| SPIRIT_OF_PHARAOH_CID | 0x1788 | card_1570: Spirit of the Pharaoh slot=0x1788 pw=25343280 |
| RELEASE_RESTRAINT_CID | 0x187e | card_1791: Release Restraint slot=0x187E pw=75417459 |
| CYBER_BARRIER_DRAGON_CID | 0x19a8 | card_2017: Cyber Barrier Dragon slot=0x19A8 pw=68774379 |
| GAZELLE_CID | 0x1291 | card_0607: Gazelle the King of Mythical Beasts slot=0x1291 pw=05818798 |
| BERFOMET_CID | 0x1293 | card_0609: Berfomet slot=0x1293 pw=77207191 |
| BUSTER_BLADER_CID | 0x1377 | card_0787: Buster Blader slot=0x1377 pw=78193831 |

注：proposal 将 DARK_SAGE_CID 记为 "card_0882 (approx)"，实际是 card_0944。卡名和 slot 值本身正确，label 序号标注不精确，非 blocking。

### C8 残留 FUN_ 核查

全段（L4611–L6188）grep FUN_: 仅 L5203 现有 plate 含 `FUN_0809078c`（指向 `count_zone_pair_hits_with_fn_ptr`，该函数已命名，地址 0x0809078c 在 Seg-3b 范围外）。该 plate 被 proposal 的新 plate 替换，新文本已用现名，无残留。所有 asm/*.s grep FUN_ 在范围 [0x080872e4,0x08087d58)：0 hits。

### 三条硬规则核查

- Rule 1 (地址序): 已验，Seg-3a 完成后推进 Seg-3b，边界 0x080872e4 / 0x08087d58 与路线图一致。
- Rule 2 (函数间 ROM_INCBIN 必处理): 段内 0 个 ROM_INCBIN/.byte 块，Rule 2 trivially 满足。
- Rule 3 (0 引用 -> §5.1): 所有 15 函数均有 THUMB+1 引用（最少 1 个）；段内无任何孤立数据块。

### 三个 CORRECTED plate 基址验证

1. **populate_equip_zone_entries_substate_e_by_pair**: 函数体 L5168-5170 `movs r4,#0x83; lsls r4,r4,#0x3; adds r0,r3,r4` — 0x83<<3=0x418，加 gP1LifePoints(0x0201c4e0) = 0x0201c8f8 = gP1HandSlotArray。ROM 验证: slot 0x08087a1c = 0x0201c8f8 ✅。旧 plate "gDuelCardPool_alt_base" 错误，新 plate 正确。
2. **scan_zone_equip_category_match_substate_e**: 同样的 0x83<<3=0x418 offset，base = 0x0201c8f8 = gP1HandSlotArray。旧 plate "MONSTER_ZONE_BASE=0x0201c5d8" 错误，新 plate 正确。
3. **write_equip_zone_entries_by_lv_card_id**: slot 0x08087674=0x0201c600=gP1FieldArrayCBase ✅; slot 0x08087678=0x0201c740=gP1SlotSetCodeArray ✅。旧 plate "gDuelEffectZones/gDuelCardPool_alt" 错误，新 plate 正确。

### REF slot 文件来源小偏差（非 blocking）

proposal 的 REF_SLOTS 表将来源写为 "duel_field.inc REUSE"，但实际上：
- gP1FieldArrayCBase、gP1SlotSetCodeArray、gP1HandSlotArray、gP1ChainZoneArray 均定义在 **ewram.inc**（duel_field.inc 仅有注释引用）。
- PLAYER_BLOCK_STRIDE 也在 ewram.inc。

这不影响落地正确性（常量均存在可复用），但 fixer 脚本应 include ewram.inc 而非 duel_field.inc。非 blocking。

### Plate 字符数与 ASCII

14 个新 plate 全部 ≤500 chars（最大 488 chars），全部纯 ASCII，全部无 FUN_ 残留。

### Substate 字母匹配验证

独立解码 movs r1,#N 指令：populate_substate_e(0xe ✅)、scan_equip_target_substate_c(0xc ✅)、write_all_substate_c(0xc ✅)、scan_gadget_substate_d(0xd ✅)、scan_equip_category_substate_e(0xe ✅)、scan_field5_atk_bound_substate_d(0xd ✅)、scan_chimera_substate_e(0xe ✅)。

### C13 残留 100% 覆盖

python 精确清点 [L4611, L6188): DAT_=92, PTR_gP1LifePoints_=13, DWORD_=0。EQ(82)+REF(10)+RENAME(13)=105 = 92+13。完全匹配。

---

## 状态: PASS

无阻塞问题。唯一的非 blocking 观察（DARK_SAGE card_0944 vs "card_0882 approx"；REF 来源文件 ewram.inc vs 写的 duel_field.inc）均不影响落地正确性。

## 修改清单

无需修改。Fixer 可直接进入模式 B 落地。

注意 fixer：
- EQ slot 使用的常量 PLAYER_BLOCK_STRIDE / gP1FieldArrayCBase / gP1SlotSetCodeArray / gP1HandSlotArray / gP1ChainZoneArray 均在 `constants/ewram.inc`（非 duel_field.inc）。
- 10 个 NEW CID 常量目标文件：append to `constants/card_info.inc`。
- Dark Sage card 标签为 card_0944（非 card_0882）。
