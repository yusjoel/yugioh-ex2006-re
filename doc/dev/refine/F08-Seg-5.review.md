# Refine Review: F08-Seg-5

Segment: `0x08067fa4..0x080690dc`, file `asm/08_equip_oam_neodaed.s` (lines 8958-11401)
20 named fn, 65 DWORD_/DAT_ auto-name slots, 1 PTR_ auto-name slot, 0 ROM_INCBIN, 1 .byte stub.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致, 未跳号/回头 | PASS | Seg-4 已 commit 5b5eeae; Seg-5 正确接续 0x08067fa4..0x080690dc |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块有归宿 | PASS | ROM_INCBIN=0; 唯一 .byte (L10090/4B @0x08068828) → disasm 计划覆盖 |
| C3 Rule3 | §5.1 块确 0 引用 (独立 ref-scan) | PASS | 段内无 §5.1 候选; .byte 块已独立复核 raw=0, THUMB+1=3 (见下) |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 17 key slot python 独立核对全通过 (见下) |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | PASS | 3 new CID + 5 new OAM/domain 常量 grep 0 命中; reuse 逐一确存在 (见下) |
| C6 R2 名 | 槽名合规, 无碰撞 | PASS | check_equip_eligible_always_false 形式合规; 无重复标签 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 4 REF slots 均 .word 符号已在 asm 中, 仅需 slot label 改名; 无新 carve |
| C8 R5 现名 | 段内无残留 FUN_ | PASS | grep Seg-5 行区间 FUN_[0-9a-f]{8} = 0 命中 |
| C9 ASCII | plate/EOL 文本纯 ASCII | NEEDS_FIX | L10092 CJK mojibake 待 ASCII 重写 (提案有 ASCII 替换文本); L11400 为 Seg-6 第一函数 plate, Seg-6 处理 |
| C10 carve | 无 carve 块 (Seg-5 无数据表) | N/A | switchD_080686a2 已 inline (L9917-10024 确认); 无新 carve 需求 |
| C11 误名 | 函数体全局与函数名无矛盾 | PASS | 20 个函数名经本次复核无矛盾; FUNC_RENAME=None 正确 |
| C12 R6 | 关键槽语义有 file:line 证据 + 置信度 | PASS | 6 个关键槽提供消费者证据; 2 处 med-conf 名见专项评估 (见下) |
| C13 残留 | 段内所有残留自动名槽全覆盖 | PASS | asm scan: 65 DWORD_/DAT_ + 1 PTR_ = 66; proposal 处理 65 EQ/RENAME + 1 REF = 66, 全覆盖 |

---

## 专项独立验证结果

### stub @ 0x08068828 (4B): 机器码 + ref-scan + CID 偏移

**机器码核**: ROM @ 0x08068828 = `00 20 70 47` = `movs r0,#0; bx lr` — CORRECT.

**ref-scan 独立复核**:
- raw refs (0x08068828): 0
- THUMB+1 refs (0x08068829): 3, 地址:
  - 0x09e3fed8
  - 0x09e40478
  - 0x09e40bc8

**CID 偏移核** (关键, 独立 python 实读):

| fn_eligible_slot_addr | value | [addr-4] | [addr-8] | [addr-0xc] |
|---|---|---|---|---|
| 0x09e3fed8 | 0x08068829 | **0x00001302** | 0x00000000 | 0x00000000 |
| 0x09e40478 | 0x08068829 | **0x00001360** | 0x00000000 | 0x00000000 |
| 0x09e40bc8 | 0x08068829 | **0x00001495** | 0x00000000 | 0x00000000 |

Proposal 称 "CID at fn_ptr-4" — **与 ROM 实读吻合**: 偏移 -4 给出正确 CID, 偏移 -0xc 均为 0。

**入口类型分析**: dispatch table 24B entry 布局经两套已知 entry 交叉验证:
- `[+0]` CID, `[+4]` fn_eligible THUMB+1, `[+8]` null/pad, `[+0xc]` fn_activate THUMB+1 (or 0), `[+0x10]` 0, `[+0x14]` 0
- Seg-2 commit 确认 `check_equip_eligible_state_dispatch_for_time_wizard` (0x08065d79) 在 TW 表项 `[+4]` = fn_eligible 位置
- 内存文档 "fn_eligible CID 在 fn_ptr-0xc" 适用于 fn_eligible 在 `[+0xc]` 的表项类型; 本段表项 fn_eligible 在 `[+4]`, CID = slot_addr-4 ✓
- Proposal 函数名 `check_equip_eligible_always_false` 及 plate "fn_eligible slots" — **CORRECT**

**card-stats.s passcode 核对**:
- 0x09e3fed8 → CID=0x1302: card-stats.s L8959 `@ Royal Decree slot=0x1302 pw=51452091` ✓
- 0x09e40478 → CID=0x1360: card-stats.s L9986 `@ Imperial Order slot=0x1360 pw=61740673` ✓
- 0x09e40bc8 → CID=0x1495: card-stats.s L12742 `@ The Emperor's Holiday slot=0x1495 pw=68400115` ✓

ROYAL_DECREE_CID=0x1302 已在 card_info.inc L790; THE_EMPERORS_HOLIDAY_CID=0x1495 已在 card_info.inc L509.
IMPERIAL_ORDER_CID=0x1360 未在 constants — proposal 新建, 正确.

### C4: EQ 值独立核对 (17 key slots)

全部通过, 列举代表性:

| slot | expected | ROM actual | |
|---|---|---|---|
| 0x0806805c | 0x00000868 | 0x00000868 | OK |
| 0x08068600 | 0x00001286 | 0x00001286 | OK |
| 0x08068760 | 0x0000139d | 0x0000139d | OK |
| 0x08068f08 | 0x0000ffff | 0x0000ffff | OK |
| 0x08068f70 | 0x0000801b | 0x0000801b | OK |
| 0x08068f74 | 0x0000801c | 0x0000801c | OK |
| 0x08068ff0 | 0x000014f8 | 0x000014f8 | OK |
| 0x08068c74 | 0x0201e500 | 0x0201e500 | OK |
| 0x080686a8 | 0x080686ac | 0x080686ac | OK |
| 0x0806905c | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x080690d0 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x080690d4 | 0x00001da8 | 0x00001da8 | OK |
| 0x080690d8 | 0x00001ce8 | 0x00001ce8 | OK |

"DWORD_082a8" 系 proposal 表格笔误 (truncated), 实际 label 为 `DWORD_080682a8` (asm L9351), 地址 0x080682a8 在段范围内, 值 0x0201c510 与 ROM 吻合 — 仅 proposal 元数据笔误, 不影响落地.

### C5: 双向核

**NEW 常量** (grep constants/*.inc by value = 0 命中, 各独立验证):
- `BLAST_SPHERE_CID` = 0x1286: 0 命中 ✓; card-stats.s L7763 pw=26302522 ✓
- `BIRDFACE_CID` = 0x139d: 0 命中 ✓; card-stats.s L10597 pw=45547649 ✓
- `IMPERIAL_ORDER_CID` = 0x1360: 0 命中 ✓; card-stats.s L9986 pw=61740673 ✓
- `OAM_EQUIP_SPRITE_TILE_P2_1B` = 0x801b: 0 命中 ✓ (全字 0x0000801b 精确搜索)
- `OAM_EQUIP_SPRITE_TILE_P2_1C` = 0x801c: 0 命中 ✓ (同上)
- `gEquipLpZoneEntryBase` = 0x0201e500: 0 命中 ✓
- `EQUIP_OAM_ENTRY_ATTR_14F8` = 0x14f8: 0 命中 ✓

**REUSE 常量** (grep 确存在+值匹配):
- PLAYER_BLOCK_STRIDE=0x868 ✓ (ewram.inc L250)
- gDuelFieldSlots=0x0201c510 ✓ (ewram.inc L312)
- gDuelPhaseFlags=0x0201b290 ✓ (ewram.inc L351)
- gP1FieldArrayCBase=0x0201c600 ✓ (ewram.inc L364)
- EQUIP_PHASE_FRAME_OFF=0x4a4 ✓ (ewram.inc L434)
- gP1HandSlotArray=0x0201c8f8 ✓ (ewram.inc L332)
- OAM_EFFECT_SLOT_TILE_P1=0x8056 ✓ (oam_attr.inc L107)
- LP_CARD_TRACK_NEXT_OFF=0x1daa ✓ (ewram.inc L248)
- LP_CARD_TRACK_BASE_OFF=0x1da8 ✓ (ewram.inc L247)
- P1LP_BLOCK2_OFF_1CE8=0x1ce8 ✓ (ewram.inc L275)
- ROYAL_DECREE_CID=0x1302 ✓ (card_info.inc L790)
- THE_EMPERORS_HOLIDAY_CID=0x1495 ✓ (card_info.inc L509)
- 8 个 CID reuse (GREENKAPPA/REAPER_OF_CARDS/HARPIES_FEATHER_DUSTER/DRIVING_SNOW/BAIT_DOLL/NOBLEMAN_EXTERMINATION/CRIMSON_NINJA/cid_131c) 全部 grep 确存在 ✓

**域裁定 (EQUIP_SLOT_SCORE_CAP=0xffff)**:
- 同值已有: SLOT_CARD_EMPTY=0xffff (card_info.inc) 和 OAM_ATTR0_HIDDEN=0xffff (oam_attr.inc)
- 消费者独立核查: asm L11073-11083, `ldr r3, DWORD_08068f08; cmp r0,r3; ble LAB_08068ed8; adds r0,r3,#0` — 两组独立 cmp+ble+saturate 模式, 语义明确为 score 饱和上限
- 与 card-empty sentinel 和 OAM hidden 语义截然不同, Seg-4 域裁定先例适用 — 域裁定 PASS

### C13: 残留槽 100% 覆盖

asm 独立 scan (L8958-L11401) 结果: 65 个 DWORD_/DAT_/UNK_ + 1 个 PTR_gP1LifePoints_0806867c = 66 total.
Proposal: 65 个 EQ/RENAME 表 + 1 个 PTR 在 REF_SLOTS = 66 total. 全覆盖, 无遗漏.
所有 66 个 slot 地址均在 [0x08067fa4, 0x080690dc) 范围内 ✓.

### C9: CJK plate 状态

- **L10092** (`dispatch_equip_slot_sprite_by_zone_type` @ 0x0806882c): CJK mojibake 待 ASCII 重写.
  Proposal 提供 ASCII 替换文本 (dispatch_equip_slot_sprite_by_zone_type 节), 内容合理, 无零容忍词.
- **L11400** (`tick_dragon_summon_display_if_slots_paired` plate): 属 Seg-6 第一函数 (0x080690dc) 的 pre-entry comment, 在 Seg-5 行扫描范围内但语义属 Seg-6. Proposal 正确标注 "Seg-6 修正", 此处不要求 Seg-5 落地修复.

CID 0x128b = Lord of D. (card-stats.s L7802 pw=17985575) — 确认 Seg-6 boundary plate 卡名错误, 但 Seg-5 不动.

### C8: stale FUN_ 扫描

`grep FUN_[0-9a-f] asm/08_equip_oam_neodaed.s` 限 L8958-11401: 0 命中 — PASS.

---

## 专项评估: 2 个 med-conf 新名

### (a) EQUIP_OAM_ENTRY_ATTR_14F8 = 0x14f8

独立 ref-scan (4-byte aligned exact 0x000014f8): 5 次 (0x08001960 在早期数据表, 0x08068ff0 在 Seg-5, 余 3 在 FS/data 区域). **Proposal 称 "8 raw ROM refs" 为过计**, 实际 ROM code 内仅 2 处.

消费者证据 (asm L11255): `ldr r2, DWORD_08068ff0; lsls r1,r1,#0xd; orrs r1,r2; str r1,[sp,#0x4]` — OR 组合构建 attr word, 随后 `bl setup_equip_oam_entry_with_sprite_attr`. 证据充分, 语义为 OAM entry attr 参数.

**评估**: ref count 元数据不准确, 但名称语义有消费者证据支持, 保守命名 `EQUIP_OAM_ENTRY_ATTR_14F8` 可接受 (conf: med). Fixer 落地后可追加所有 5 处引用的 EOL 同步.

### (b) gEquipLpZoneEntryBase = 0x0201e500

独立 ref-scan (4-byte aligned exact 0x0201e500): **28 次** — 与 proposal 一致.
跨模块分布: 0x0806xxxx (本文件 Seg-5/Seg-6), 0x0807xxxx, 0x0809xxxx, 0x080axxxx, 0x080bxxxx, 0x080cxxxx — 广泛全局变量特征.

Seg-5 消费者 (L10713, `dispatch_equip_lp_field_state_by_card_id`): `ldr r0, DAT_08068c74; ldr r2,[r0,#0x0]` — 读取基址然后提取 card_type bits, 用于 sprite_code 选择. Seg-6 同模式.

Proposal 注: Seg-6 plate 称该地址为 "OAM_DATA_PTR", 与 Seg-5 名有出入.

**评估**: 名称 `gEquipLpZoneEntryBase` 基于 Seg-5 用途命名, 保守且无歧义. **建议 Seg-6 落地时按消费者语义最终确认名称** (若 OAM_DATA_PTR 更准确则在 Seg-6 阶段做 CONST_RENAME). 当前接受.

---

## 元数据不准确 (非阻断)

以下 proposal 元数据与独立核对不符, 不影响 C2/C3/C5 判定, 由 fixer 知悉:

| 项 | Proposal 声称 | 独立核对 |
|---|---|---|
| EQUIP_OAM_ENTRY_ATTR_14F8 raw refs | "8 raw ROM refs" | 4-byte 精确: 5 次 (2 在 ROM code, 3 在 FS) |
| OAM_EQUIP_SPRITE_TILE_P2_1C raw refs | "24 raw ROM refs" | 4-byte 精确: 3 次 |
| proposal 表格行 DWORD_082a8 | 笔误截断 | 实际 label `DWORD_080682a8` @ asm L9351, 无影响 |

---

## 状态: PASS

C9 的 L10092 CJK plate 属 Seg-5 内 CJK, proposal 已计划 ASCII 重写, 落地时 fixer 执行即可 (不阻断 proposal 批准). 其余 C1-C13 全部独立验证通过.

---

## 落地注意 (给 fixer)

1. **C9 必达**: 落地脚本中对 `dispatch_equip_slot_sprite_by_zone_type` @ 0x0806882c 执行 setPlateComment, 使用 proposal 提供的 ASCII 文本. 落地后 grep asm/08 中该函数附近无 `\x{4e00}-\x{9fff}` 字符.
2. **IMPERIAL_ORDER_CID**: 新建 card_info.inc `.equ IMPERIAL_ORDER_CID, 0x00001360  @ Imperial Order (pw=61740673; card-stats.s slot=0x1360)`.
3. **ref count 元数据修正** (非阻断, 建议): ewram.inc 中 `EQUIP_OAM_ENTRY_ATTR_14F8` 的注释应标 "2 ROM code refs" 而非 "8"; `OAM_EQUIP_SPRITE_TILE_P2_1C` 注释标 "3 raw refs". 可选择落地时修正.
4. **gEquipLpZoneEntryBase 命名**: 当前 ewram.inc 注释可标 "(Seg-5 name; Seg-6 may refine)" 便于后续追踪.
5. **L11400 CJK plate**: 不在 Seg-5 scope, Seg-6 负责修正 (包括 "Stamping Destruction" → "Lord of D." 卡名).
