# Refine Review: F07-Seg-1  [iter-2 re-review]

**Segment**: `0x0805c2f0 .. 0x0805cfec` (34 fn, 66 slots, 5 ROM_INCBIN)
**Module**: `asm/07_equip_effect_chain.s` lines 1..2019
**Reviewer**: independent re-run iter-2 (no trust in proposal conclusions)

---

## iter-1 recap

iter-1 found NEEDS_FIX(2 items, both C5):
- #1: EQUIP_PAIR_INVALID=0xffff -> must reuse SLOT_CARD_EMPTY (card_info.inc:386)
- #2: CHAIN_NODE_NOT_FOUND=0xffff0000 -> must reuse EQUIP_CHAIN_SENTINEL (duel_field.inc:270)

fixer mode A applied both fixes. Additionally fixer changed PAIRED_SLOTS_SEARCH_ARG=0xfe4 to reuse HARPIE_LADY_CID (card_info.inc:311). iter-2 verifies all three changes plus the open 0x1119 collision question.

---

## iter-2 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | 路线图 Seg-1: 0x5c2f0..0x5cfec / 34 fn / 5 ROM_INCBIN 完全吻合 |
| C2 Rule2 | 5 个 ROM_INCBIN 块全有归宿 | PASS | 4 disasm + 1 §5.1; 无静默保留 |
| C3 Rule3 | §5.1 块 (0x5c4aa/0x2a) 确 0 引用 | PASS | 独立重跑: raw=0, THUMB+1=0 (全 2B-step 穷举) |
| C4 R1 值 | 所有 EQ/REF 槽 ROM 字节核对 | PASS | 独立 python 核验: 0x0805c514=0x00000fe4 OK; 0x0805c588=0x00001119 OK; 0x08056638=0x00001119 OK |
| C5 R1 复用 | 新建 constants 前无现有可复用 | PASS | 见下方 iter-2 复查结论 |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 全 66 个 slot_label 均符合 `^[a-z][a-z0-9_]+$`; 同名常量槽均加地址后缀 |
| C7 R3 接通 | REF 槽有 USER-label + DATA-ref 计划 | PASS | 3 个 REF 槽均指向 gP1LifePoints (ewram.inc 已定义) |
| C8 R5 现名 | 无残留 FUN_[0-9a-f]{8} | PASS | 扫描 lines 1..2019: 0 命中 |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | line 2 CJK 为文件头 GAS @ 注释非 Ghidra plate; 函数 plate 区域 0 CJK |
| C10 carve | THUMB+1 == ROM raw 值; 无 carve 条目 | PASS | 独立核: 5 disasm 块首 hit 处 THUMB+1 值全部与 ROM 匹配 |
| C11 误名 | 函数体语义与函数名无矛盾 | PASS | 抽查 dispatch_effect_for_neo_daedalus_paired_slot / dispatch_lord_of_d_effect_by_slot_pair / check_neo_daedalus_lp_count_eligible: 名称与体一致 |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | R6 表内 9 个关键槽均有 asm/07 行号 + 置信度; 无零容忍词 |
| C13 残留 | 段内全部自动名槽 100% 覆盖 | PASS | DAT_=47, DWORD_=10, PTR_=9, 合计 66; EQ(54)+REF(3)+RENAME(9)=66; missing=0 |

---

## iter-2 专项复查

### 1. C5 修复确认: SLOT_CARD_EMPTY + EQUIP_CHAIN_SENTINEL

iter-2 提案已将两处修正落实:
- slot 0x0805c794: const_name=SLOT_CARD_EMPTY (card_info.inc:386 `.equ SLOT_CARD_EMPTY, 0x0000ffff` 确认存在), slot_label=slot_card_empty_0805c794, EOL 注释 "SLOT_CARD_EMPTY reuse: 0xffff = no pair found (same sentinel as card slot empty check)" -- OK
- slot 0x0805ca88: const_name=EQUIP_CHAIN_SENTINEL (duel_field.inc:270 `.equ EQUIP_CHAIN_SENTINEL, 0xffff0000` 确认存在), slot_label=equip_chain_sentinel_0805ca88, EOL 注释 "EQUIP_CHAIN_SENTINEL reuse: post-lsls#16 sentinel check for no-node-found (low-16 of return = 0xffff)" -- OK
- proposal New Constants 块已删除两条旧新建 `.equ` 条目 -- OK

C5 修复完整, 无遗漏。

### 2. 0xfe4 -> HARPIE_LADY_CID 复用确认 (C5)

**证据链**:
- ROM 字节核验: 0x0805c514 = 0x00000fe4 (confirmed)
- card-stats.s: `card_0068: @ Harpie Lady  slot=0x0FE4  pw=76812113` -- 0xfe4 = Harpie Lady slot
- card_info.inc:311: `.equ HARPIE_LADY_CID, 0x00000fe4` -- 确认存在
- count_paired_slots_both_sides 全部 call site 均传 card_id 参数:
  - asm/07 line 1632: `dispatch_lord_of_d_effect_by_slot_pair` 传 0x128b (Lord of D.)
  - asm/07 line 9336: `check_necrovalley_paired_slots_exist` 传 0x159d (Necrovalley)
  - asm/07 line 12447: 传 0x16cb (BLS-Envoy) + 0x16e4 (CED-Envoy)
  - asm/03 line 5401-5402: `ldr r0, eval_harpie_lady_cid` -> `bl count_paired_slots_both_sides` (slot label name 直接坐实)
  - asm/07 Seg-1 consumer: `dispatch_effect_for_neo_daedalus_paired_slot` 传 0xfe4 -- 与上述模式完全一致, 0xfe4 = Harpie Lady CID

**裁定**: 0xfe4 确作 card_id 参数 (= Harpie Lady), 非搜索 arg。HARPIE_LADY_CID 复用正确, C5 合规。

### 3. 0x1119 碰撞决定性裁定: SANGA_OF_THUNDER_CID vs EQUIP_SPRITE_CARD_DATA

**被比较的两处**:

**File 07 (asm/07_equip_effect_chain.s line 305, slot 0x0805c588)**:
- 函数: `check_equip_slot_eligible_with_sanga_and_prereqs`
- 用法: `ldr r2, DAT_0805c588` (r2=0x1119) -> `bl check_node_in_slot_chain(player_id, slot_idx, icid=0x1119, mode=3)` -- 0x1119 作为 internal card_id (icid) 参数传入 chain node 检查函数
- 语义域: card_id 比较 (检查 Sanga of the Thunder 是否已在链中)
- card-stats.s 坐实: `card_0329: @ Sanga of the Thunder  slot=0x1119  pw=25955164`
- ROM 核验: 0x0805c588 = 0x00001119 (confirmed)

**File 06 (asm/06_equip_eligibility_b.s line 7298-7299, slot 0x08056638)**:
- 函数: `enqueue_equip_card_sprite_mode3`
- 用法: `ldr r2, enqueue_equip_card_sprite_mode3_card_data` (r2=0x1119) -> `bl enqueue_sprite_attr_with_mode(player_id, slot_group, card_data=0x1119, 0, 3)` -- 0x1119 作为固定 card_data 字段值传入 sprite 属性入队函数
- 语义域: sprite attribute `card_data` 参数 (固定常量, 非 card_id 比较)
- EOL 注释: "enqueue_sprite_attr_with_mode arg r2=card_data fixed 0x1119; mode=3"
- 常量名: EQUIP_SPRITE_CARD_DATA (duel_field.inc:345)
- ROM 核验: 0x08056638 = 0x00001119 (confirmed)

**关键区别**:
- File 06 中 0x1119 是 sprite enqueue 函数的 `card_data` 形参 (固定魔法参数, 非 card_id 相等比较)
- File 07 中 0x1119 是 `icid` 参数 (内部卡ID, 用于 chain node 存在性检测)
- 两者属于不同语义域: sprite 属性格式参数 vs. card_id 检索 key
- EQUIP_SPRITE_CARD_DATA 名本身也反映"sprite 数据字段"语义, 非 CID 名

**File 06 EQUIP_SPRITE_CARD_DATA 是否误名?**: 不是。enqueue_equip_card_sprite_mode3 函数体明确: r2 由 `ldr r2, enqueue_equip_card_sprite_mode3_card_data` 加载固定常量 0x1119, 不读 card_entry[+0] card_id -- 这是独立的 sprite 属性字段值, 恰好数值等于 Sanga of Thunder 的 slot_id, 但语义用途截然不同 (sprite card_data 格式字段 ≠ card_id 比较)。EQUIP_SPRITE_CARD_DATA 命名正确, 无需订正。

**裁定**: 结论 (b) -- 良性值碰撞, 不同语义域。
- File 07 SANGA_OF_THUNDER_CID=0x1119 新建 card_info.inc **正确合规**
- card_info.inc grep 0x00001119 = 0 hits (confirmed) -- 无重复定义冲突
- File 06 EQUIP_SPRITE_CARD_DATA=0x1119 保持不变, 无误名, 无交叉订正需求

### 4. 剩余新建 CID 双向核验 (C5)

11 个 "new" CID 全部 grep constants/*.inc 0 hits:
- SANGA_OF_THUNDER_CID 0x00001119: card_info.inc=0 hits (duel_field.inc:345 为不同常量名 EQUIP_SPRITE_CARD_DATA, 良性碰撞已裁定)
- SCAPEGOAT_CID 0x000012d2: 0 hits
- GRACEFUL_CHARITY_CID 0x000012cc: 0 hits
- GREENKAPPA_CID 0x000011f0: 0 hits
- REAPER_OF_CARDS_CID 0x00000ffa: 0 hits
- HARPIES_FEATHER_DUSTER_CID 0x00001246: 0 hits
- DRIVING_SNOW_CID 0x0000134d: 0 hits
- NOBLEMAN_EXTERMINATION_CID 0x00001364: 0 hits
- BAIT_DOLL_CID 0x0000149b: 0 hits
- cid_131c 0x0000131c: 0 hits
- cid_12fb 0x000012fb: 0 hits

card-stats.s 坐实 (各高置信 CID):
- 0x1119=Sanga of the Thunder, 0x12d2=Scapegoat, 0x12cc=Graceful Charity, 0x11f0=Greenkappa, 0x0ffa=Reaper of the Cards, 0x1246=Harpie's Feather Duster, 0x134d=Driving Snow, 0x1364=Nobleman of Extermination, 0x149b=Bait Doll -- 均有 card-stats.s 匹配记录
- cid_131c (0x131c) + cid_12fb (0x12fb): card-stats.s 无记录, 中性命名正确 (low confidence)

### 5. disasm 4 + §5.1 1 简核

ref-scan 结果 (与 iter-1 一致, 独立核验已完成):
- 0x5c40a/0x5e: raw=1(偶合,压缩区), THUMB+1=25 (fn1 x4 + fn2 x21) -> disasm PASS
- 0x5c4aa/0x2a: raw=0, THUMB+1=0 -> §5.1 PASS
- 0x5c608/0x28: raw=0, THUMB+1=1 -> disasm PASS
- 0x5cd86/0x2a: raw=0, THUMB+1=15 -> disasm PASS
- 0x5cf1c/0x20: raw=0, THUMB+1=3 -> disasm PASS

C13 三表并集自洽: EQ(54)+REF(3)+RENAME(9)=66 = DAT_(47)+DWORD_(10)+PTR_(9) -- 完全覆盖。

---

## 状态: PASS

所有 C1-C13 项均通过。iter-1 NEEDS_FIX(2) 已由 fixer mode A 完整修复; 附加改动 (HARPIE_LADY_CID 复用) 正确合规; 0x1119 碰撞经独立核验裁定为良性值碰撞 (不同语义域), SANGA_OF_THUNDER_CID 新建合规。

---

## Reviewer Verdict: F07-Seg-1 = PASS
