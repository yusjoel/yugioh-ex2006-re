# Refine Review: F09-Seg-1

Segment: `[0x0806e76c, 0x0806ff50)` — asm/09_equip_lp_display.s Seg-1
Reviewer: independent (not executor)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | 路线图 Seg-1 = 0x6e76c..0x6ff50, 20 fn; proposal 一致 |
| C2 Rule2 | 每个 ROM_INCBIN/ROM_INCBIN 块都有归宿 | OK | 6 块全部判 DISASM; switchD_0806e8b6 已 decode 无需 R4 行动 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | §5.1=0, 所有块均有引用; 无需核 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 全部 40 个 EQ slot 独立 python 读取确认; 含 NEW × 8 + REUSE × 32 |
| C5 R1 复用 | 新建 constants 前无现有可复用 | OK | 7 个 NEW 值 (0x1882/0x1ce4/0x874/0x144c/0x1452/0x801a/0x142a) grep 全部 0 命中 |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$ 无碰撞 | OK | 全部 77 个 slot_label 格式合规; 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | carve=0; 34 REF 槽全有 gas_label + DATA-ref 计划 |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_/DAT_/DWORD_ | **FAIL** | (1) 已知: FUN_0806e898 at asm/09 L148 — proposal 已识别并列入 PLATE 修正, OK. (2) **未识别**: asm/09 L207 现有 plate 写 `LP_STATE_BASE = 0x0201b290 (gP1LifePoints)` 但 0x0201b290 = gDuelPhaseFlags (非 gP1LifePoints); proposal 未修正此错误命名 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | asm/09 L2 有 CJK 是文件级 header 注释 (非 Ghidra 导出 plate/EOL), 不违规; proposal 新增 EOL 全部 ASCII |
| C10 carve | 指针表条目 +1 (THUMB) | N/A | carve=0; Block1/3/5 THUMB+1 在 FS table, 已 ROM 字节核对 (CID at fn_elig_ptr - 4 = 0x142a/0x1468/0x146f 全 OK) |
| C11 误名 | 函数体全局 vs 函数名矛盾 | OK | FUNC_RENAME=0; 20 fn 名无明显名-体矛盾; L207 plate 错全局名问题归 C8 处理 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据, 无零容忍词 | OK | 7 个消费者证据表完整, 含 asm/09 行号 + conf 标注, 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | OK | python 精确清点: 77 auto-name slots = 40 EQ + 34 REF + 3 RENAME (并集 = 全集, 无遗漏) |

### 关键独立核验数据

**ref-scan 独立重跑结果 (与 proposal 比对):**

| Block | raw (file off) | THUMB+1 (file off) | 与 proposal 一致 |
|-------|---------------|-------------------|-----------------|
| B1 0x0806f008/0x34 | 1@0x806d7 (非对齐, false) | 1@0x1e40958 | OK |
| B2 0x0806f054/0x174 | 1@0x6f050 (aligned, dispatch tbl) | 0 | OK |
| B3 0x0806f85c/0x138 | 0 | 2@0x1e40a90+0x1e43a30 | OK |
| B4 0x0806fa08/0x180 | 1@0x6fa04 (aligned, dispatch tbl) | 0 | OK |
| B5 0x0806fdec/0x28 | 0 | 2@0x3d3eb6(false)+0x1e46610(real) | OK |
| B6 0x0806fe88/0xc8 | 1@0x6fe84 (aligned, dispatch tbl) | 0 | OK |

**CID 独立核 (fn_eligible_ptr - 4):**
- B1: file[0x1e40954] = 0x142a (Creature Swap) OK
- B3 ref1: file[0x1e40a8c] = 0x1468 (Destiny Board) OK
- B3 ref2: file[0x1e43a2c] = 0x1468 OK
- B5: file[0x1e4660c] = 0x146f (Cathedral of Nobles) OK

**dispatch table 目标核 (独立读 ROM):**
- B2: 6 unique targets = {0x806f054, 0x806f066, 0x806f078, 0x806f0ac, 0x806f0cc, 0x806f188} — 与 proposal 完全一致
- B4: 10 unique targets — 与 proposal 完全一致
- B6: 8 unique targets — 与 proposal 完全一致
- 全部 dispatch table 条目均为偶数地址 (raw ptr, 非 THUMB+1), DISASM 判断正确

**REF slot 地址独立核 (python ROM 读取):**
- 全部 34 个 REF slot 值确认:
  - gP1LifePoints (0x0201c4e0): 12 个 slot 全 OK
  - gDuelPhaseFlags (0x0201b290): 9 个 slot 全 OK
  - gDuelFieldSlots (0x0201c510): 10 个 slot 全 OK
  - gP1HandSlotArray (0x0201c8f8): DWORD_0806ee50 OK
  - gEquipChainSlotRefs (0x0201bb90): 2 个 slot 全 OK
  - switchD 表指针 DAT_0806e8bc (0x0806e8c0): OK

**PLAYER_BLOCK_STRIDE 18 个 slot 全部 = 0x868 OK**

---

## 状态: NEEDS_FIX

---

## 修改清单

### #1 — C8 — asm/09 L207 plate 错误全局名 (gP1LifePoints 应为 gDuelPhaseFlags)

**位置**: `asm/09_equip_lp_display.s` 第 148 行 plate 注释 (dispatch_equip_chain_state_sprite_by_slot 函数 plate) 之 Constants 段, 第 207 行:

```
@   LP_STATE_BASE = 0x0201b290 (gP1LifePoints)
```

**问题**: 0x0201b290 在整个项目中定义为 `gDuelPhaseFlags`; `gP1LifePoints = 0x0201c4e0`. 代码 `ldr r0, DAT_0806e8b8` 加载的是 gDuelPhaseFlags, 与注释中 gP1LifePoints 相矛盾.

**修正**: Ghidra 中将 dispatch_equip_chain_state_sprite_by_slot 的 plate comment 里该行改为:
```
   LP_STATE_BASE = 0x0201b290 (gDuelPhaseFlags)
```
或删去括号内名称, 改为符合现名的描述.

**验证**: 改后 asm/09 该行不再包含 `gP1LifePoints` (对应 0x0201b290 位置).

---

## 附: 已确认正确的核心项目

以下全部独立核验通过, fixer 可放心落地:

- 40 EQ 值全部 ROM 字节匹配
- C5: 7 个 NEW 常量 grep=0 确认; 所有 REUSE 常量 grep 存在确认
- C13: 77 = 40+34+3 完整覆盖, 无遗漏
- 6 个 DISASM 块 ref-scan 分类正确 (THUMB+1 vs raw 各归其类)
- FS table CID (0x142a / 0x1468 / 0x146f) 独立 ROM 字节核验正确
- ICID_RESERVED_D(0x144c) / ICID_RESERVED_E(0x1452) 确为 card-stats.s 缺口 (reserved)
- BIG_MARCH_OF_ANIMALS_CID(0x1882) = card_1795 pw=01689516 核实
- CREATURE_SWAP_CID(0x142a) = card_0910 pw=31036355 核实
- gEquipChainSlotRefs = 0x0201bb90 两个 slot 确认 (无误引)
- 所有 slot_label 合规 ^[a-z][a-z0-9_]+$, 无碰撞
- EOL/plate 新增文本全 ASCII
- Block 边界: B1 end=0x806f03c, B2 end=0x806f1c8, B3 end=0x806f994, B4 end=0x806fb88 (approx), B5 end=0x806fe14, B6 end=0x806ff50 (=Seg-1 end) 全部一致
