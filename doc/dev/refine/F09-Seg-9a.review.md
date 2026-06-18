# Refine Review: F09-Seg-9a

## 段范围
`[0x0807738c, 0x08077c50)` — blocks B1..B5, Seg-9 前半段

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | Seg-9 roadmap: 0x7738c..0x7850c, B1-B5 = 前5块 (0x7757c/2c, 0x775d0/a8, 0x779e4/30, 0x77a3c/120, 0x77b88/c8) 完全吻合 |
| C2 | 每个 ROM_INCBIN 块都有归宿 | ✅ | 全5块归 R4 disasm; 无静默保留 |
| C3 | §5.1 块确 0 引用 | ✅ | §5.1=0; 所有5块均有确认 refs (THUMB+1 或 raw dispatch ptr); 独立 ref-scan 复核: B1 thumb=1, B2 raw=1, B3 thumb=1, B4 raw=1+B4_embedded thumb=1, B5 raw=1 |
| C4 | EQ value == ROM 4 字节小端 | ✅ | 独立 python 读 ROM 验证全部 26 个 EQ 槽; 全部 OK |
| C5 | 新建 constants 前无现有可复用 | ✅ | 3 新 CID (0x1749/0x1866/0x1717) 逐一按 VALUE grep constants/*.inc: 0 命中; REUSE 槽均确认存在 |
| C6 | 槽名格式合规, 无碰撞 | ❌ | **10 个 global var 池标签 (g-prefix) 使用了全小写, 违背既成惯例**; 另 1 个 CID 池标签缩写丢失 `_master` (见 #3/#4) |
| C7 | carve/全局槽有 USER-label + DATA-ref | ✅ | PTR_DAT_080775ac: .word self-ptr @ 0x080775a8 (ROM confirmed); PTR_DAT_08077a18: .word self-ptr @ 0x08077a14 (ROM confirmed); sub-stubs blocks: entry[8] of respective tables confirmed |
| C8 | plate 引用无残留 `FUN_` | ✅ | 独立 grep lines 19213..20094: 0 FUN_ 命中 |
| C9 | plate/EOL 纯 ASCII | ✅ | python 扫描 lines 19213..20094: 0 非 ASCII 字节; PLATE=0 正确 |
| C10 | carve 指针表条目 +1 (THUMB) | ✅ | FS entry 结构独立验证: B1 CID@+8=0x16df (SPATIAL_COLLAPSE), fn_elig@+c=0x0807757d (THUMB+1); B3 CID@+8=0x1712 (DIMENSION_FUSION), fn_elig@+c=0x080779e5; B4-emb CID@+8=0x1717 (JADE_INSECT_WHISTLE), fn_elig@+c=0x08077b35 |
| C11 | 函数名与体无矛盾 (FUNC_RENAME) | ✅ | FUNC_RENAME=0; 9 函数均未见名体矛盾迹象 |
| C12 | 关键槽语义有 file:line + 置信度证据 | ✅ | 消费者证据表 9 条均有 asm/09 行号 + 具体指令引用; 新 CID 有 card-stats.s 行号 + passcode; 置信度标注为 high; 无零容忍词 |
| C13 | 段内所有残留自动名槽 100% 覆盖 | ✅ | 独立 python 扫描 lines 19213..20094 (实际范围含 PTR_DAT_08077a18/DAT_08077a3c/DAT_08077b88): 31 槽 = 26 EQ + 5 REF; 与 proposal 完全吻合; 无漏计 |

---

## 独立复核细节

### EQ 槽 ROM 字节核验
python 独立读取全部 26 个 EQ 槽 ROM 4 字节小端值, 与 proposal 完全一致 (ALL OK).

### Ref-scan 独立结果
```
B1 (0x0807757c): raw=0 thumb=1  -> FS table [0x09e41ca8]=0x0807757d ✓
B2 (0x080775d0): raw=1 thumb=0  -> dispatch table entry[8]@0x080775cc=0x080775d0 ✓
B3 (0x080779e4): raw=0 thumb=1  -> FS table [0x09e41d68]=0x080779e5 ✓
B4 (0x08077a3c): raw=1 thumb=0  -> dispatch table entry[8]@0x08077a38=0x08077a3c ✓
B4_embedded (0x08077b34): raw=0 thumb=1 -> FS table [0x09e41de0]=0x08077b35 ✓
B5 (0x08077b88): raw=1 thumb=0  -> dispatch table @0x08077b84=0x08077b88 ✓
```
B5 的 `0x09f836e3` 验证为压缩数据区 (`0x09f8xxxx`)，非 FS 表; 排除为有效 THUMB+1 引用 (原始 4 字节 = 0x077ba14b 非 GBA ROM 指针), 判断正确.

### C5 新 CID 验证
- 0x1749: card-stats.s L48081 `card_4052: @ Legendary Jujitsu Master slot=0x1749 pw=25773409` ✓
- 0x1866: card-stats.s L51376 `card_4337: @ Kangaroo Champ slot=0x1866 pw=95789089` ✓
- 0x1717: card-stats.s L47551 `card_4002: @ Jade Insect Whistle slot=0x1717 pw=95214051` ✓
- 全部 grep constants/*.inc 0 命中 ✓

### C13 行范围说明
Proposal 注明范围 `19213..20068`, 但 PTR_DAT_08077a18 (L20070), DAT_08077a3c (L20080), DAT_08077b88 (L20093) 三个 REF 槽位于 line 20068 之后. 实际有效范围为 19213..20094 (到 B5 ROM_INCBIN 所在行). 完整扫描确认 31 槽, 结果正确.

---

## 状态: NEEDS_FIX (4 items)

---

## 修改清单

### #1 — C4 (R4 disasm 计划) — B4 缺少入口 0x08077ac2

**问题**: B4 dispatch table (PTR_DAT_08077a18, 9-entry) 独立读出 6 个唯一入口点, 但 proposal 只列了 5 个.

ROM 实测唯一入口:
```
entry[0]=0x08077b00, entry[1..4]=0x08077b2c, entry[5]=0x08077ac2, entry[6]=0x08077ab4,
entry[7]=0x08077a70, entry[8]=0x08077a3c
唯一集: {0x08077a3c, 0x08077a70, 0x08077ab4, 0x08077ac2, 0x08077b00, 0x08077b2c} = 6个
```

Proposal 漏掉 `0x08077ac2` (entry[5], 1 raw ref). `0x08077ac2` 在 B4 范围 [0x08077a3c, 0x08077b5c) 内, 是独立入口 (与 0x08077ab4 相差 0xe 字节).

**修复**: 在 B4 disasm 计划中增加第 6 个 DisassembleCommand: `DisassembleCommand(0x08077ac2)`. 在 Labels 列表中增加 `sub_7ac2`. 将 "5 unique sub-stub entries" 改为 "6 unique sub-stub entries".

---

### #2 — C4 (R4 disasm 计划) — B5 入口点错误: 0x77c00 应替换为 0x77c3a

**问题**: B5 dispatch table (11-entry, at 0x08077b5c..0x08077b84) 独立读出 6 个唯一入口点, 但 proposal 列的集合有误:

ROM 实测 B5 dispatch table 唯一入口:
```
entry[0]=0x08077c3a, entry[1]=0x08077c2c, entry[2]=0x08077c18, entry[3..8]=0x08077c48,
entry[9]=0x08077bb6, entry[10]=0x08077b88
唯一集: {0x08077b88, 0x08077bb6, 0x08077c18, 0x08077c2c, 0x08077c3a, 0x08077c48} = 6个
```

Proposal 列的 `0x08077c00`:
- ROM 中 `0x08077c00` 无 raw refs, 也无 THUMB+1 refs (独立 ref-scan = 0)
- 读取该地址字节 `0x0fc0` = `lsrs r0,r0,#0x3`, 是中间代码而非入口

Proposal 缺少 `0x08077c3a`:
- B5 dispatch table entry[0] = 0x08077c3a (1 raw ref in ROM)
- 字节 `0x78a4` = `ldrb r4,[r0,#0x2]`, 是有效 THUMB 入口

**修复**: 将 proposal B5 唯一入口列表中:
- 删除 `0x08077c00` (无 dispatch 引用, 非入口)
- 添加 `0x08077c3a` (dispatch table entry[0], 1 raw ref)
- DisassembleCommand 列表对应修改: 删除 `DisassembleCommand(0x08077c00)`, 添加 `DisassembleCommand(0x08077c3a)`
- Labels 列表: 删除 `sub_7c00`, 添加 `sub_7c3a` (或 `default_7c3a` 视 sub-stub 语义)
- B5 `sub-entries: 0x77c00 raw=2` 数据有误, 改为 `sub-entries: 0x77c3a raw=1`

---

### #3 — C6 (R2) — 10 个 g-prefix 全局变量池标签违背 camelCase 惯例

**问题**: 既成惯例 (文件内 60+ 处证据: `gDuelPhaseFlags_pool_4428`, `gP1LifePoints_pool_4a48`, `gDuelFieldSlots_pool_4430`, `gP1AltHandSlotArray_pool_6bac` 等) 要求 g-prefix 全局变量名在池标签中保持 camelCase. Proposal 将其全部小写化且截短.

需修正的 10 个池标签:

| slot | 当前 (错误) | 应改为 |
|------|------------|--------|
| DAT_08077410 | `gP1_alt_hand_slot_pool_7410` | `gP1AltHandSlotArray_pool_7410` |
| DAT_08077450 | `gduel_phase_pool_7450` | `gDuelPhaseFlags_pool_7450` |
| DWORD_08077524 | `gduel_phase_pool_7524` | `gDuelPhaseFlags_pool_7524` |
| DWORD_080777a0 | `gequip_zone_cnt_pool_77a0` | `gEquipZoneCountTable_pool_77a0` |
| DWORD_080777a8 | `gp1_zone_hand_cnt_pool_77a8` | `gP1ZoneHandCount_pool_77a8` |
| DWORD_080777ac | `gp1_field_array_c_pool_77ac` | `gP1FieldArrayCBase_pool_77ac` |
| DWORD_080777f8 | `gduel_phase_pool_77f8` | `gDuelPhaseFlags_pool_77f8` |
| DWORD_0807788c | `gp1lp_pool_788c` | `gP1LifePoints_pool_788c` |
| DWORD_080778e0 | `gp1lp_pool_78e0` | `gP1LifePoints_pool_78e0` |
| DWORD_080779b8 | `gduel_field_slots_pool_79b8` | `gDuelFieldSlots_pool_79b8` |

注: 全大写常量 (PLAYER_BLOCK_STRIDE, EQUIP_PHASE_FRAME_OFF, PRICKLE_FAIRY_CID 等) 使用全小写池标签是正确的既成惯例, 无需修改.

---

### #4 — C6 (R2) — LEGENDARY_JUJITSU_MASTER_CID 池标签缩写丢失 `_master`

**问题**: 常量名为 `LEGENDARY_JUJITSU_MASTER_CID`, 但 proposal 池标签写成 `legendary_jujitsu_cid_pool_7960`, 丢掉了 `_master` 部分.

**修复**: 将 `DWORD_08077960` 的池标签从 `legendary_jujitsu_cid_pool_7960` 改为 `legendary_jujitsu_master_cid_pool_7960`.

---

## 附: 不影响判定的信息性备注

- B2 描述文本 "9 unique entry points" 应为 "9 entries, 6 unique entry points"; 实际列出的 6 个地址是正确的, 不影响 disasm 执行.
- Proposal 段内行范围写为 `19213..20068`, 实际 REF 槽跨越到 L20093/20094. C13 核算时用全范围 19213..20094 已得到正确计数 31.

---

## Reviewer Verdict: F09-Seg-9a = NEEDS_FIX(4 items)
