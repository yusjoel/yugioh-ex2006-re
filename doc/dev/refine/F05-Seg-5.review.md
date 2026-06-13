# Refine Review: F05-Seg-5

Segment: `0x0804c6e8..0x0804d124` (dispatch_card_eligibility_state_machine body extends to 0x4d1d2),
file `asm/05_equip_eligibility_a.s`
Reviewer: independent re-scan (2026-06-13)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | OK | Seg-5 范围 0x4c6e8..0x4d124 与 §五路线图完全一致；Seg-4b 已完成 (commit 8a924b3)，Seg-5 是下一段，无跳号/回头 |
| C2 Rule2 | OK | 段内 ROM_INCBIN 3 块：0x4c734/0x38、0x4cca2/0xea、0x4cdac/0x2c；proposal 对全部 3 块做 §5.1 登记处理；无静默保留 |
| C3 Rule3 | WARN | **独立重跑 ref-scan (穷举 2B-step)**：Block1 (0x4c734/0x38) raw=0 thumb=0 ✓；Block2 (0x4cca2/0xea) 仅 0x4cd34 有 raw=1 来自 0x086bb944 (compressed resource区, 非代码) ✓；Block3 (0x4cdac/0x2c) **raw=7** (0x4cd90/94/98/9c/cda0/cda4/cda8, 均属 PTR_DAT_0804cd90 跳转表内部引用，跳转表本身亦为孤立), thumb=0 ✓。§5.1 判定均正确。**但 proposal 的证据描述有误**："raw=3 (internal refs from PTR_DAT_0804cd90 at 0x4cd90/94/9c only)" — 实际 PTR_DAT 表有 7 个条目 (0x4cd90..0x4cda8 = 7×4B)，raw 引用为 7 件而非 3 件。所有 7 个引用均为孤立岛内部引用，外部引用仍为 0，§5.1 分类正确。属证据计数有误，不影响结论 |
| C4 R1 值 | OK | 独立 python struct.unpack_from('<I', rom, addr-0x08000000) 核对全部 75 个 EQ/RENAME 槽 (3 批次)，ROM 字节与 proposal 值 100% 吻合。gP1LifePoints=0x0201c4e0、gDuelPhaseFlags=0x0201b290、gDuelCardCtxBase=0x0201e2a0、所有 ELIGIB_*_OFF 等全部正确 |
| C5 R1 复用 | FAIL | **C5 碰撞**: `ELIGIB_RESULT_OFF = 0x00000584` 与 `constants/duel_field.inc` 中已有的 `GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF = 0x00000584` 值相同。Proposal 未扫描到此碰撞，直接新建 `ELIGIB_RESULT_OFF`。按 C5 规则"不分语义域"，fixer 物化前须处理此碰撞 (见 #1 修改清单)。其余 17 个新建常量均无碰撞 ✓ |
| C6 R2 名 | WARN | 67 个 EQ slot label 全部唯一、无重复。**但含大写 'D' 的 `caseD_` 系列 label** (如 `dispatch_eligib_caseD_0_state_off`, `dispatch_eligib_caseD_1_card_ctx` 等共 35+ 个) 严格而言不符合 `^[a-z][a-z0-9_]+$`。Ghidra label 本身允许大写。项目内 switchD_/caseD_ 系列 label 已作为 Ghidra 生成约定存在于 ASM 中，slot label 引用 caseD 后缀以区分同函数内多个同类槽是必要的实践。建议 fixer 与用户确认此约定是否豁免 C6 大写限制，或改用全小写后缀 (如 `_case_d0_`、`_case_d1_` 等)。本条判 WARN 而非 FAIL，因改名不影响语义正确性 |
| C7 R3 接通 | OK | 本段无 REF_SLOTS (proposal 明确声明 0 个)。8 个 RENAME_SLOTS 中：PTR_gP1LifePoints_* 系列指向已存在全局 gP1LifePoints ✓；orphan_slot_card_eligible_fn_table 重命名现有 PTR_DAT_0804cd90 ✓；dispatch_eligib_switchdata_ptr 指向 ASM 现存的 switchD_0804ce98__switchdataD_0804cea8 ✓；dispatch_eligib_caseD_1_ineligible_cid_tbl 指向 ROM 数据表 0x09e3f118 (10-entry CID array 已验证) ✓ |
| C8 R5 现名 | OK (deferred) | 段内 7 个函数 plate 中，`apply_equip_activation_with_id_lookup` / `init_card_sprite_row_entry` / `init_card_sprite_row_entry_alt` 的 plate 含 stale FUN_ 引用 (`FUN_080432bc/FUN_08043714/FUN_080439e0/FUN_08043d90/FUN_080440b8`, `FUN_08095ba8/FUN_08095ca0/FUN_08095d84`)。Proposal 明确说明这些是 Seg-6+ 的 caller，将在对应段细化时修订。查 naming-proposals.csv 确认：上述 FUN_ 均已命名 (如 `enqueue_zone_slot_sprite_attr_by_card_type`, `init_equip_card_sprite_row_entry` 等)，延迟修订有据可查。项目先例 (Seg-2 review) 允许跨段 caller FUN_ 延迟修订。本段自身函数的 plate 无 stale FUN_ |
| C9 ASCII | OK | Proposal 实际写入 Ghidra 的 EOL/plate 文本全为 ASCII。RENAME_SLOTS 的 EOL 字符串 (`.word gP1LifePoints ; 0x0201c4e0`, `orphan jump table (0 external refs)...`, `.word 0x09e3f118 ; ROM ptr: 10-entry CID array...`) 均为纯 ASCII。Proposal 文档本身的日中文标题/说明不进 Ghidra，无影响 |
| C10 carve | N/A | 本段无需 carve。switchdataD_0804c6e8 (6-entry) 和 switchD_0804ce98__switchdataD_0804cea8 (32-entry) 均为 PC-relative 跳转表，条目是裸 ROM 地址 (非 fn-ptr, 无 THUMB+1 需求)。PTR_DAT_0804cd90 表同样为裸地址。无 fn-ptr 表条目 +1 问题 |
| C11 误名 | OK | 抽查 7 个函数语义：`submit_slot_card_sprite_row_entry` 确实调用 `submit_sprite_row_data(type=0x14,count=0xc)` ✓；`check_card_slot_activation_eligible` 确实为 BST 多叉比较器 ✓；`dispatch_card_eligibility_state_machine` 确实按 [gDuelPhaseFlags+0x574] 分派 32 个 case ✓。无误名信号 |
| C12 R6 | OK | 关键槽均有 asm 文件行号证据及置信度标注 (high)。ELIGIB_*_OFF 系列来自 dispatch 函数体的直接 ldr/str 证据，置信度合理。SPRITE_ATTR_TYPE_HIDDEN_Y97=0x8061 的 OBJ disabled + Y=0x61 语义通过对比 0x0061 (enabled) 的使用路径验证。CID 值均经 card-stats.s passcode→slot_id 坐实 |
| C13 残留 | OK | 独立 python 清点：段内 `.word` 数据槽 (不含 incbin block 起点 DAT_0804cdac) 75 个 = 64 在严格段范围内 + 11 在 dispatch 函数体 [0x4d124..0x4d1e0]。EQ 67 + RENAME 8 = 75，全覆盖，无遗漏 |

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单 (NEEDS_FIX 逐条可执行)

### #1 — C5 — ELIGIB_RESULT_OFF = 0x584 与 duel_field.inc 现有常量碰撞

**问题**: Proposal 新建 `ELIGIB_RESULT_OFF = 0x00000584` (ewram.inc)，但 `constants/duel_field.inc` 已有：

```
.equ GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF, 0x00000584  @ gPrng+0x1c0 dereference + 0x584: display_ready flag byte; 20 ROM refs
```

两者值相同 (0x584)，基址不同 (gDuelPhaseFlags vs gPrng+0x1c0)。

**C5 规则**: "新建常量前必扫全 constants/*.inc 确认无同值常量，不分语义域"。

**涉及槽** (共 8 个, 均使用 0x584 值):
- EQ 槽: 0x0804d0e4 (`dispatch_eligib_caseD_14_result_off`)
- EQ 槽: 0x0804d11c (`dispatch_eligib_caseD_15_result_off`)
- EQ 槽: 0x0804d1e0 (`dispatch_eligib_caseD_1f_result_off`)
- 以上 3 个 EQ 槽在 proposal 中用 `ELIGIB_RESULT_OFF` 常量

**需要处理**: Fixer 须选择以下方案之一，并在 proposal 中明确说明:

**方案 A**: 复用现有 `GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF` (名称会产生语义混淆)，仅修改这 3 个 slot label。按 C5 字面规则此为标准做法，但名称 GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF 用于 gDuelPhaseFlags offset 语境语义极度混乱。

**方案 B**: 请求用户豁免此碰撞 (两值的语义基址完全不同，GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF 是 gPrng+0x1c0 的额外偏移，而 ELIGIB_RESULT_OFF 是 gDuelPhaseFlags 的直接偏移)，新建 `ELIGIB_RESULT_OFF` 作为独立语义常量。需用户裁决，reviewer 不代做此决定。

**建议**: 本 reviewer 倾向方案 B (分语义新建)，但须经用户确认方可物化。Fixer 应上报此碰撞，暂停等待裁决。

---

## 附注

### C3 ref-scan 证据计数有误 (非阻断)

Proposal 对 Block3 (0x4cdac/0x2c) 描述 "raw=3 (internal refs from PTR_DAT_0804cd90 at 0x4cd90/94/9c only)" 有误。

独立穷举扫描确认：PTR_DAT_0804cd90 表共 7 个条目 (地址 0x4cd90, 0x4cd94, 0x4cd98, 0x4cd9c, 0x4cda0, 0x4cda4, 0x4cda8)，指向 block3 内 3 个入口点：
- 0x4cdac (×4 次): entries[0,1,3,5]... 实际 ASM 显示 entries 0,1,3 = 0x4cdac, entries 4,5 = 0x4cdb6, entries 2,6 = 0x4cdc2
- raw 引用 7 件，均为孤立岛内部。外部引用仍为 0，§5.1 分类正确。

Fixer 在落地时应更新证据描述为 "raw=7 (all 7 entries of PTR_DAT_0804cd90 at 0x4cd90..0x4cda8, all internal to orphan island)"。

### C6 caseD_ 大写约定 (建议与用户确认)

35+ 个 slot label 含 `caseD_` 后缀 (大写 D)。`switchD_`/`caseD_` 是 Ghidra 生成 switch 分支标签的约定，已在 ASM 文件中大量存在。以 caseD_ 后缀区分同函数多个同类槽是合理实践。建议 fixer 在本段落地前与用户确认：这类 `caseD_` 后缀是否豁免 `^[a-z][a-z0-9_]+$` 限制。若不豁免，需改为全小写形式 (如 `_case0_`, `_case1_` 等)，影响 35+ 个 label。

### C8 跨段 FUN_ 延迟修订 (已记录)

`apply_equip_activation_with_id_lookup` plate 含 FUN_080432bc/08043714/080439e0/08043d90/080440b8；
`init_card_sprite_row_entry` / `init_card_sprite_row_entry_alt` plate 含 FUN_08095ba8/08095ca0/08095d84。
全部已在 naming-proposals.csv 命名。Fixer 落地 Seg-6 及 file 09 对应段时须一并清理。

### 总槽计数 (供参考)

Proposal 正文"75 total"正确: 64 个在严格段内 (0x4c6e8..0x4d124) + 11 个在 dispatch 函数体 (0x4d124..0x4d1e0)。DAT_0804cdac 为 ROM_INCBIN 块头标签，不计入 .word 数据槽，正确排除。
