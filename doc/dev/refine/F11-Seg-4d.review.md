# Refine Review: F11-Seg-4d

Segment: `[0x0808a2ac, 0x0808ad8c)` -- 0xAE0 = 2784 bytes
Proposal: `doc/dev/refine/F11-Seg-4d.proposal.md`
Source: `asm/11_effect_slot_puzzletext.s` (giant ROM_INCBIN, 4th sub-segment)
Review date: 2026-06-26

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | active doc §五 line 249: Seg-4d `[0x0808a2ac, 0x0808ad8c)` -- 完全匹配 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 纯 THUMB 代码段; 无 sub-block; 24 fn disasm 计划覆盖所有字节; post-disasm gate (grep ROM_INCBIN/.byte ==0) 已在提案中指定 |
| C3 | §5.1 块确 0 引用 | N/A | 段内无 §5.1 条目; 3 个 degenerate strong + 3 个 weak 均已确认 THUMB+1 引用全部来自压缩数据区 (>0x082d4000): 0x0808a44c->0x08ea6bc8; 0x0808a450->0x08bf3948; 0x0808a996->0x0893b848; 三者均属巧合字节值 |
| C4 | EQ value == ROM 4 字节小端 | FAIL | **fn20 Literal Pool DWord List 地址错误**: 提案写 `0x0808ab92=PLAYER_BLOCK_STRIDE` 但 0x0808ab92 是 2B 对齐偏移，非 word-aligned; 实际 PLAYER_BLOCK_STRIDE pool DWord 在 0x0808ab94; ROM 核对: rom_read32(0x0808ab94)=0x00000868 ✓; rom_read32(0x0808ab92)=0x08680000 (错位读) ✗; 其余 14 个 spot-checked pool 值全部正确 |
| C5 | 新建 constants 前确无现有可复用 | PASS | 独立 value-grep 全部 11 个 NEW CID: 0x1628/0x166b/0x16c4/0x16d8/0x17be/0x191e/0x170c/0x1714/0x1754/0x1647/0x16bc 全部 0 hits -- 真 NEW; card-stats.s slot= 核对: 11 个 slot= 行与卡名完全匹配; 23 个 REUSE CID 按值 grep 全部 PRESENT |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 24 个函数名全合规 (regex 验证); 段内无重复; CSV 无先有同名 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | REF=34 完整: Python 独立扫描段内所有 EWRAM 指针 pool slot = 34 个 (gP1LifePoints x22/gP1FieldArrayCBase x3/gP1HandSlotArray x5/gP1SlotSetCodeArray x2/gP1AltHandSlotArray x1/gP1HandCountBase x1), 与提案 REF 表逐项吻合; 所有槽均有 createDWordWithRef+ptr_* 标签计划 |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | 提案全文 grep `FUN_[0-9a-fA-F]{8}` = 0 hits |
| C9 | ASCII 检查 | PASS | 独立计数全部 24 个 plate 文本: 全部 ASCII; 无 CJK/非 ASCII 字符; 最长实际长度 fn14=477 chars (提案自报 484); 提案自报长度多处与实际不符 (误差 6-67 chars) 但所有实际长度均 <=500 |
| C10 | 指针表条目 +1 (THUMB) | PASS | dispatch table 抽查 10 条: entry[130]/[143]/[165]/[171]/[197]/[267]/[137]/[138]/[153]/[178] 的 CID 和 fnptr+1 值全部与提案一致 (Python 核对); fn02 双 CID entry [132]+[232] 均指向 0x0808a379 ✓ |
| C11 | 函数体全局 vs 函数名矛盾 | PASS | ROM 核对 fn03 substate_d (MOVS r1,#0xd at 0x0808a3d4=0x210d ✓); fn16 substate_f (MOVS r1,#0xf at 0x0808a996=0x210f ✓); fn24 substate_e (MOVS r1,#0xe at 0x0808ad4e=0x210e ✓); 无函数名与 substate 矛盾信号 |
| C12 R6 | 关键槽语义有 file:line 置信度证据; 无零容忍词 | PASS | 14 个关键消费者函数均有 naming-proposals.csv 引用; write_equip_zone_entry_by_substate 0x0808d88c 确认; fn24 mask 0xffff803f 标 med-conf 并注明无 named constant -- 可接受; 无零容忍词 |
| C13 | 段内残留 DAT_ 全覆盖 | PASS | 24 fn spans 连续无间隙: size sum = 0xcc+0x40+0x30+0x58+0x58+0x58+0xa8+0x58+0x8c+0x8c+0x80+0xb4+0x58+0x8c+0x58+0x3c+0x84+0x7c+0x90+0x58+0x58+0x54+0x58+0xec = 0xAE0 = segment size (Python 验证); fn24 ends at 0x0808ad8c = segment end ✓; no orphan blocks |

---

## 自查关键数据

```
=== C5 value-grep (全 11 NEW CID) ===
0x1628 (SENRI_EYE_CID):                    0 hits -- TRUE NEW ✓  card-stats.s card_1291 slot=0x1628 Senri Eye ✓
0x166b (ARSENAL_ROBBER_CID):               0 hits -- TRUE NEW ✓  card-stats.s card_1345 slot=0x166B Arsenal Robber ✓
0x16c4 (CHAOSRIDER_GUSTAPH_CID):           0 hits -- TRUE NEW ✓  card-stats.s card_1414 slot=0x16C4 Chaosrider Gustaph ✓
0x16d8 (DIMENSION_DISTORTION_CID):         0 hits -- TRUE NEW ✓  card-stats.s card_1433 slot=0x16D8 Dimension Distortion ✓
0x17be (RETURN_FROM_DD_CID):               0 hits -- TRUE NEW ✓  card-stats.s card_1615 slot=0x17BE Return from the DD ✓
0x191e (DDM_DIFF_DIM_MASTER_CID):          0 hits -- TRUE NEW ✓  card-stats.s card_1915 slot=0x191E D.D.M. ✓
0x170c (MANJU_TEN_THOUSAND_HANDS_CID):     0 hits -- TRUE NEW ✓  card-stats.s card_1476 slot=0x170C Manju ✓
0x1714 (SALVAGE_CID):                      0 hits -- TRUE NEW ✓  card-stats.s card_1484 slot=0x1714 Salvage ✓
0x1754 (LADY_NINJA_YAE_CID):               0 hits -- TRUE NEW ✓  card-stats.s card_1535 slot=0x1754 Lady Ninja Yae ✓
0x1647 (ARSENAL_SUMMONER_CID):             0 hits -- TRUE NEW ✓  card-stats.s card_1312 slot=0x1647 Arsenal Summoner ✓
0x16bc (CHOPMAN_THE_DESPERATE_OUTLAW_CID): 0 hits -- TRUE NEW ✓  card-stats.s card_1407 slot=0x16BC Chopman ✓

=== C3 degenerate ref-scan ===
0x0808a44c: THUMB+1 ref @0x08ea6bc8 (>0x082d4000, 压缩数据) ✓
0x0808a450: THUMB+1 ref @0x08bf3948 (>0x082d4000, 压缩数据) ✓
0x0808a996: THUMB+1 ref @0x0893b848 (>0x082d4000, 压缩数据) ✓
Weak 0x0808a974: dword=0x00000868 (PLAYER_BLOCK_STRIDE pool) ✓
Weak 0x0808a9c2: hw=0x1c11 (MOV r1,r2 inside loop) ✓
Weak 0x0808ab2c: hw=0xbcf0 (POP {r4-r7} epilogue bytes) ✓

=== C4 pool DWord ROM 核对 (15 slots spot-check) ===
0x0808a36c: 0x0201c4e0 gP1LifePoints OK
0x0808a370: 0x00000868 PLAYER_BLOCK_STRIDE OK
0x0808a374: 0x0000159d NECROVALLEY_CID OK
0x0808a368: 0x00001377 BUSTER_BLADER_CID OK
0x0808a364: 0x00001629 EMBLEM_CID OK
0x0808a490: 0x0201c4e0 gP1LifePoints OK
0x0808a494: 0x00000868 PLAYER_BLOCK_STRIDE OK
0x0808aa34: 0x0201cab0 gP1AltHandSlotArray OK
0x0808aa2c: 0x0201c4e0 gP1LifePoints OK
0x0808ad84: 0xffff803f mask OK
0x0808ad88: 0x0201c4f4 gP1HandCountBase OK
0x0808ad78: 0x0201c4e0 gP1LifePoints OK
0x0808ad80: 0x0201c8f8 gP1HandSlotArray OK
0x0808a678: 0x0201c740 gP1SlotSetCodeArray OK
0x0808ab40: 0x000005dc CARD_FIELD3_THRESHOLD_1500 OK
**0x0808ab92: 0x08680000 -- WRONG (misaligned read of fn20 pool)**
**0x0808ab94: 0x00000868 -- CORRECT address for fn20 PLAYER_BLOCK_STRIDE pool**
**0x0808ab98: 0x0201c600 -- gP1FieldArrayCBase OK (correct)**

=== C7 EWRAM pool scan (Python 独立) ===
gP1LifePoints    x22 OK (proposal: 22)
gP1FieldArrayCBase x3 OK (proposal: 3)
gP1HandSlotArray x5 OK (proposal: 5)
gP1SlotSetCodeArray x2 OK (proposal: 2)
gP1AltHandSlotArray x1 OK (proposal: 1)
gP1HandCountBase x1 OK (proposal: 1)
Total = 34 -- C7 PASS

=== dispatch table spot-check ===
entry[130] CID=0x00001628 fnptr=0x0808a3b9 OK (fn03)
entry[143] CID=0x0000166b fnptr=0x0808a441 OK (fn05)
entry[165] CID=0x000016d8 fnptr=0x0808a9b5 OK (fn17)
entry[197] CID=0x000017be fnptr=0x0808a9b5 OK (fn17)
entry[267] CID=0x0000191e fnptr=0x0808a9b5 OK (fn17)
entry[137] CID=0x00001647 fnptr=0x0808ac49 OK (fn23)
entry[138] CID=0x0000164a fnptr=0x0808aca1 OK (fn24)
entry[153] CID=0x000016bc fnptr=0x0808aca1 OK (fn24)
entry[178] CID=0x00001745 fnptr=0x0808aca1 OK (fn24)
entry[132] CID=0x0000162c fnptr=0x0808a379 OK (fn02)
entry[232] CID=0x0000184c fnptr=0x0808a379 OK (fn02)

=== C9 plate 长度 (实测 vs 提案自报) ===
fn01: actual=382 reported=449 (mismatch, but 382<=500 OK)
fn14: actual=477 reported=484 (mismatch, but 477<=500 OK -- max)
fn17: actual=458 reported=490 (mismatch, but 458<=500 OK)
fn22: actual=400 reported=362 (mismatch, but 400<=500 OK)
fn24: actual=469 reported=482 (mismatch, but 469<=500 OK)
All 24 plates: actual <=500, all ASCII -- C9 PASS

=== fn20 pool detail ===
0x0808ab88: 0xf002 (BL hi-word)
0x0808ab8a: 0xfe80 (BL lo-word)
0x0808ab8c: 0xbc70 (pop {r4..r6})
0x0808ab8e: 0xbc01 (pop {pc})
0x0808ab90: 0x4700 (bx r0)
0x0808ab92: 0x0000 (2B alignment gap -- NOT a pool DWord start)
0x0808ab94: 0x0868 (hi-hw of 0x00000868 = PLAYER_BLOCK_STRIDE)
0x0808ab96: 0x0000 (lo-hw of 0x00000868)
0x0808ab98: 0xc600 (gP1FieldArrayCBase start)
0x0808ab9a: 0x0201
Correct pool: [0x0808ab94, 0x0808ab98]; proposal incorrectly listed [0x0808ab92, 0x0808ab98]
```

---

## 状态: NEEDS_FIX(1 item)

---

## 修改清单 (fixer 逐条执行)

### #1 -- C4 -- fn20 Literal Pool DWord List 地址 0x0808ab92 应为 0x0808ab94

**问题**: `## Literal Pool DWord List` 段中 fn20 的条目写为:
```
**fn20** (0x0808ab44): 0x0808ab92, 0x0808ab98
```

0x0808ab92 不是 word-aligned 地址 (0x92 & 3 = 2); 该处实际为 2B alignment padding (0x0000). 正确的 PLAYER_BLOCK_STRIDE pool DWord 地址是 0x0808ab94 (word-aligned, ROM 核对: rom_read32(0x0808ab94)=0x00000868 ✓).

**修正**:
- `## Literal Pool DWord List` 中 fn20 行:
  ```
  **fn20** (0x0808ab44): 0x0808ab94, 0x0808ab98
  ```
  (0x0808ab92 → 0x0808ab94)

- fn20 section body 注释行 (if present): 确认 PLAYER_BLOCK_STRIDE pool 在 0x0808ab94, 非 0x0808ab92.

**对落地的影响**: fixer 执行 createDWord 时会对 0x0808ab92 操作，读到错误值 0x08680000，而非 0x00000868。必须用正确地址 0x0808ab94。gP1FieldArrayCBase 那行 (0x0808ab98) 不受影响。

---

## 不阻塞项 (信息性)

**I1**: 提案自报 plate 长度与实测不符 (差异 6-67 chars，多为高估)。实测所有 24 个 plate 文本长度 <=500，全 ASCII，无超限。不需要修正 (自报数字仅为 proposal 内部参考，不影响落地)。

**I2**: fn20 section 正文说 "pool: 0x0808ab92=PLAYER_BLOCK_STRIDE" -- 该描述与错误的 Literal Pool DWord List 一致，但 fn20 的 REF_SLOTS 表未包含 gP1LifePoints (fn20 用 gP1FieldArrayCBase，不用 gP1LifePoints)，这是正确的。修正 #1 仅需改 pool 地址列表；若 fn20 section body 也有该地址引用则一并改。

**I3**: 24 个函数名均无零容忍词；高置信度断言均有 body-read 证据 (gate BL 列表 + dispatch table 核对)；fn24 mask 0xffff803f 标 med-conf 结构证据可接受。

**I4**: PLAYER_BLOCK_STRIDE 独立 word-aligned 扫描结果 = 25 slots，与提案 "25 slots" 一致 ✓；但其中 fn20 的 slot 实际在 0x0808ab94 (不在 0x0808ab92)，#1 修正后扫描一致。

**I5**: fn02 group 卡名问题: 提案将 fn02 命名为 `scan_zone_reserved_icid_group_substate_d`，两个 CID 为 ICID_RESERVED_A(0x162c) + ICID_RESERVED_B(0x184c)。card_info.inc 已有这两个名字。命名语义合理。
