# Refine Review: F11-Seg-4e

Segment: `[0x0808ad8c, 0x0808bb7c)` -- 0xDF0 = 3568 bytes  
Proposal: `doc/dev/refine/F11-Seg-4e.proposal.md`  
Source: `asm/11_effect_slot_puzzletext.s` (giant ROM_INCBIN, 5th sub-segment)  
Review date: 2026-06-26

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | refine-progress.md 明确 "下一任务: file 11 Seg-4e [0x0808ad8c..0x0808bb7c)"; active doc §五 line 269: Seg-4e `[0x0808ad8c, 0x0808bb7c)` — 完全匹配; Seg-4d 结尾 0x0808ad8c = Seg-4e 起点，严格地址序无回头 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 段内纯 THUMB 代码; 无 sub-block; 25 fn disasm 计划 + 4 excluded (2 degenerate strong + 2 weak) 覆盖全部 0xDF0 字节; size sum = 0xDF0 (Python 独立验证); post-disasm residue gate (grep ROM_INCBIN/.byte ==0) 已在提案指定 |
| C3 | §5.1 块确 0 引用 | N/A | 段内无 §5.1 登记; 提案正确宣称无孤儿数据区; 4 个 excluded 字节 (degenerate/weak) 均属父函数体/pool 内部 — THUMB+1 引用全部指向 >0x082d4000 压缩数据区 (独立 ref-scan 确认: 0x0808b40e→0x8ac54cc; 0x0808b95a→0x8f845cc; 0x0808b58a→0x880a946; 0x0808b798→0x877c27e) |
| C4 | EQ value == ROM 4 字节小端 | PASS | Python 独立核对 25 个 pool slot: 全部 OK (详见自查数据); 含关键值 gP1LifePoints=0x0201c4e0 (×21), gP1FieldArrayCBase=0x0201c600 (×7), gP1ChainZoneArray=0x0201c880, gDuelFieldSlots=0x0201c510, PARASITE_PARACIDE_CID=0x12a1 (×2), CARD_FIELD3_THRESHOLD_1500=0x5dc, fn21 sentinel 0xbc100000 |
| C5 | 新建 constants 前确无现有可复用 | PASS | 独立 value-grep 全部 11 个 NEW CID: 0x1764/0x1769/0x1795/0x17a2/0x17e5/0x17f8/0x1845/0x1847/0x1870/0x1871/0x1872 — 全部 0 hits (card_info.inc); card-stats.s slot= 核对全部匹配提案 pw 值; LIGHTEN_THE_LOAD_CID=0x1847 在全 constants/ 目录内 0 hits — 确为 NEW; 4 个 REUSE 抽查 (AVATAR_OF_THE_POT_CID=0x1748, MONSTER_GATE_CID=0x175c, ARCHLORD_ZERATO_CID=0x1758, MOKEY_MOKEY_KING_CID=0x183d) 全部 PRESENT |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 25 个函数名全部通过 regex 验证; 段内无重复; asm/*.s + naming-proposals.csv 均无先有同名 (grep 0 hits) |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | REF=46 完整: Python 独立扫描 [0x0808ad8c, 0x0808bb7c) 内所有 EWRAM 指针 pool slot — 8 个全局各自计数与提案 REF_SLOTS 表完全吻合 (gP1LifePoints×21/gP1FieldArrayCBase×7/gP1HandSlotArray×6/gP1SlotSetCodeArray×7/gP1ZoneHandCount×2/gP1SlotCountBase×1/gDuelFieldSlots×1/gP1ChainZoneArray×1=46); 所有槽均有 createDWordWithRef + RENAME 计划 |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | 提案全文 `grep FUN_` = 0 hits |
| C9 | ASCII 检查 | PASS | 提案中非 ASCII 字符仅出现在 markdown 标题 (§ / CJK 小节名), 未进入任何 plate/EOL 文本; 25 个 plate 文本独立验收: 全部纯 ASCII; 最长 fn25=466 chars ≤ 500; 无 U+3000-U+9FFF 等 CJK 字符 |
| C10 | 指针表条目 +1 (THUMB) | PASS | Python 独立全量扫描 dispatch table (305 entries @ 0x09e5a128): 30 条 entries 指向 Seg-4e 范围; 25 个唯一 fn 地址与提案完全一致; group handlers fn03/fn14/fn25 的多 CID 与 ROM 完全匹配 (fn03→entry[182,184]; fn14→entry[210,211,258]; fn25→entry[237,238,239]); 4 个 excluded entries 均不在 dispatch table 中 |
| C11 | 函数体全局 vs 函数名矛盾 | PASS | substate MOVS r1,#N 独立核对 15 个点 (fn02/fn05/fn11/fn14 ×2/fn15/fn16 ×2/fn17/fn18/fn21/fn22/fn23/fn24/fn25) 全部通过; 无函数名与 substate 字母矛盾; 无 FUNC_RENAME 信号 |
| C12 R6 | 关键槽语义有 file:line 证据; 无零容忍词 | PASS | 20 个关键消费者函数均有 naming-proposals.csv / ewram.inc 行号引用; write_equip_zone_entry_by_substate 0x0808d88c 已在 Seg-4a..4d 建立 high-conf; fn21 raw sentinel 0xbc100000 标 med-conf 加明确 EOL 解释并声明不编造语义名称 — 可接受; 无零容忍词 |
| C13 | 段内残留 DAT_ 全覆盖 | PASS | 25 fn spans 连续无间隙 (Python 验证: 每个 end = 下一个 start); size sum = 0xDF0 = 3568 B = 段大小; fn25 ends at 0x0808bb7c = 段终 = 下一 fn (CID=0x1876@0x0808bb7c) 起点; 无孤儿 incbin/.byte 残留 |

---

## 自查关键数据

```
=== C5 value-grep (全 11 NEW CID) ===
0x1764 (LIGHT_OF_JUDGMENT_CID):        0 hits in card_info.inc -- TRUE NEW; card-stats.s card_1549 slot=0x1764 Light of Judgment pw=44595286 ✓
0x1769 (BECKONING_LIGHT_CID):          0 hits -- TRUE NEW; card-stats.s card_1553 slot=0x1769 Beckoning Light pw=16255442 ✓
0x1795 (SPIRIT_CALLER_CID):            0 hits -- TRUE NEW; card-stats.s card_1581 slot=0x1795 Spirit Caller pw=48659020 ✓
0x17a2 (SOUL_REVERSAL_CID):            0 hits -- TRUE NEW; card-stats.s card_1593 slot=0x17A2 Soul Reversal pw=78864369 ✓
0x17e5 (HOWLING_INSECT_CID):           0 hits -- TRUE NEW; card-stats.s card_1650 slot=0x17E5 Howling Insect pw=93107608 ✓
0x17f8 (TWO_MAN_CELL_BATTLE_CID):      0 hits -- TRUE NEW; card-stats.s card_1669 slot=0x17F8 Two-Man Cell Battle pw=25578802 ✓
0x1845 (MONSTER_REINCARNATION_CID):    0 hits -- TRUE NEW; card-stats.s card_1737 slot=0x1845 Monster Reincarnation pw=74848038 ✓
0x1847 (LIGHTEN_THE_LOAD_CID):         0 hits in ALL constants/ -- TRUE NEW (not in file 10 Seg-2 either); card-stats.s card_1739 slot=0x1847 Lighten the Load pw=37231841 ✓
0x1870 (LIGHT_HEX_SEALED_FUSION_CID):  0 hits -- TRUE NEW; card-stats.s card_1777 slot=0x1870 The Light - Hex-Sealed Fusion pw=15717011 ✓
0x1871 (DARK_HEX_SEALED_FUSION_CID):   0 hits -- TRUE NEW; card-stats.s card_1778 slot=0x1871 The Dark - Hex-Sealed Fusion pw=52101615 ✓
0x1872 (EARTH_HEX_SEALED_FUSION_CID):  0 hits -- TRUE NEW; card-stats.s card_1779 slot=0x1872 The Earth - Hex-Sealed Fusion pw=88696724 ✓

=== C3: degenerate/weak excluded entry ref-scan ===
0x0808b40e THUMB+1=0x0808b40f: ROM ref @0x8ac54cc (>0x082d4000, compressed) -- not real dispatch ✓
0x0808b95a THUMB+1=0x0808b95b: ROM ref @0x8f845cc (>0x082d4000, compressed) -- not real dispatch ✓
0x0808b58a THUMB+1=0x0808b58b: ROM ref @0x880a946 (>0x082d4000, compressed) -- not real dispatch ✓
0x0808b798 THUMB+1=0x0808b799: ROM ref @0x877c27e (>0x082d4000, compressed) -- not real dispatch ✓

Neither 0x0808b40e nor 0x0808b95a (the 2 NOT-in-CID-map entries) appear in dispatch table:
  0x0808b40e: NOT in dispatch table ✓ (mid-body of fn12 at offset +0x66; bytes=0x210d MOVS r1,#0xd confirmed)
  0x0808b95a: NOT in dispatch table ✓ (mid-body of fn23 at offset +0x1a; bytes=0x0e09 LSRS r1,r1,#24 confirmed)

=== C4 pool DWord ROM 核对 (25 slots) ===
0x0808adc8: 0x0201c600 gP1FieldArrayCBase OK
0x0808adcc: 0x000012ec POT_OF_GREED_CID OK
0x0808adc4: 0x00000868 PLAYER_BLOCK_STRIDE OK
0x0808ae40: 0x0201c4e0 gP1LifePoints OK
0x0808ae48: 0x0201c740 gP1SlotSetCodeArray OK
0x0808afec: 0x0201c600 gP1FieldArrayCBase OK
0x0808aff0: 0x000012a1 PARASITE_PARACIDE_CID OK
0x0808aff4: 0x0201c4ec gP1ZoneHandCount OK
0x0808aff8: 0x0201c740 gP1SlotSetCodeArray OK
0x0808b070: 0x0201c4e0 gP1LifePoints OK
0x0808b078: 0x0201c8f8 gP1HandSlotArray OK
0x0808b520: 0x000005dc CARD_FIELD3_THRESHOLD_1500 OK
0x0808b524: 0x000012a1 PARASITE_PARACIDE_CID OK
0x0808b528: 0x0201c4f0 gP1SlotCountBase OK
0x0808b8e4: 0xbc100000 fn21 slot sentinel OK
0x0808bb24: 0x0201c510 gDuelFieldSlots OK
0x0808bb2c: 0x0201c880 gP1ChainZoneArray OK
0x0808bb28: 0x0201c4e0 gP1LifePoints (fn25 loop1) OK
0x0808bb74: 0x0201c4e0 gP1LifePoints (fn25 loop2) OK
0x0808bb78: 0x00000868 PLAYER_BLOCK_STRIDE (fn25 loop2) OK
0x0808b680: 0x0201c4ec gP1ZoneHandCount (fn16) OK
0x0808b984: 0x0201c600 gP1FieldArrayCBase (fn23) OK
0x0808b9d8: 0x0201c4e0 gP1LifePoints (fn24) OK
0x0808b868: 0x0201c4e0 gP1LifePoints (fn20) OK
0x0808b870: 0x0201c740 gP1SlotSetCodeArray (fn20) OK

=== C7 EWRAM pool scan (Python 独立, word-aligned) ===
gP1LifePoints    (0x0201c4e0): found=21  expected=21  OK
gP1FieldArrayCBase (0x0201c600): found=7  expected=7  OK
gP1HandSlotArray (0x0201c8f8): found=6  expected=6  OK
gP1SlotSetCodeArray (0x0201c740): found=7  expected=7  OK
gP1ZoneHandCount (0x0201c4ec): found=2  expected=2  OK
gP1SlotCountBase (0x0201c4f0): found=1  expected=1  OK
gDuelFieldSlots  (0x0201c510): found=1  expected=1  OK
gP1ChainZoneArray (0x0201c880): found=1  expected=1  OK
Total = 46 -- REF=46 confirmed ✓

=== C9 substate spot-checks ===
fn02 0x0808ae1e: 0x210d MOVS r1,#0xd ✓  (substate_d)
fn05 0x0808b04c: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn11 0x0808b388: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn14 0x0808b4da: 0x210b MOVS r1,#0xb ✓  (substate_b)
fn14 0x0808b4e8: 0x210d MOVS r1,#0xd ✓  (substate_d)
fn16 loop1 0x0808b5e4: 0x210b MOVS r1,#0xb ✓  (substate_b)
fn16 loop2 0x0808b64e: 0x210d MOVS r1,#0xd ✓  (substate_d)
fn18 0x0808b738: 0x210b MOVS r1,#0xb ✓  (substate_b)
fn23 0x0808b970: 0x210b MOVS r1,#0xb ✓  (substate_b)
fn25 0x0808bb46: 0x210c MOVS r1,#0xc ✓  (substate_c)
fn15 0x0808b564: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn20 0x0808b846: 0x210d MOVS r1,#0xd ✓  (substate_d)
fn17 0x0808b6c0: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn21 0x0808b8ba: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn22 0x0808b920: 0x210e MOVS r1,#0xe ✓  (substate_e)
fn24 0x0808b9c0: 0x210e MOVS r1,#0xe ✓  (substate_e)

=== C13 contiguity and size ===
25 fn sizes: 0x44+0x7c+0x4c+0x164+0x80+0xb0+0x80+0x94+0x88+0x88+0x58+0x94+0x18+0xd8+0x58+0x104+0x58+0x70+0x8c+0x98+0x74+0x58+0x48+0x58+0x19c = 0xDF0 ✓
Each fn end = next fn start: contiguous ✓
fn25 ends 0x0808bb7c = segment end ✓

=== pool alignment ===
All 76 pool DWORDs: 4-byte aligned ✓ (no misalignment like Seg-4d 0x0808ab92 padding-gap)

=== dispatch table full scan ===
30 entries in [0x0808ad8c, 0x0808bb7c): 25 unique fn addresses -- matches proposal ✓
group handlers confirmed:
  fn03: entry[182]=0x1758 + entry[184]=0x1764 -> 0x0808ae4c ✓
  fn14: entry[210]=0x17e5 + entry[211]=0x17e6 + entry[258]=0x18f4 -> 0x0808b454 ✓
  fn25: entry[237]=0x1870 + entry[238]=0x1871 + entry[239]=0x1872 -> 0x0808b9e0 ✓
```

---

## 不阻塞项 (信息性记录)

**I1**: card_info.inc 中 MAGICIANS_CIRCLE_CID 注释写 pw=74083143，但 card-stats.s card_1694 实际 pw=00050755。提案正确使用 pw=00050755。先前 equate 注释有误，但 CID 值 0x1818 正确且与本段无关。无需本段修正。

**I2**: BEHEMOTH_KING_CID (0x1864) 在 card_info.inc 注释写 pw=00000000，但 card-stats.s card_1765 实际 pw=22996376。提案正确使用 pw=22996376。同 I1，先前注释问题，不影响本段。

**I3**: fn21 raw sentinel 0xbc100000 采用 med-conf EOL 标注不编造语义名称，提案已在"求助"节明确说明。可接受。

**I4**: entry[181] (CID=0x1754, fn=0x0808abf4) 属 Seg-4d 范围，提案正确跳过；dispatch table 内部 gap (如 entry[188]=0x178a->0x0808724c) 均指向 Seg-4d 或更早段的函数，与本段无关，提案处理正确。

---

## 状态: PASS

全部 C1-C13 通过，0 必修项。

---

## Reviewer Verdict: F11-Seg-4e = PASS
