# Refine Review: f01-Seg-4

Segment: `asm/01_vija_scene_text.s` ROM [0x0801e36c, 0x0801e714), 8 fn, card_info page state machine.
Proposal: `doc/dev/refine/f01-Seg-4.proposal.md`
Reviewer: independent (no proposal conclusions accepted without re-verification)

---

## 自主复核

### ROM 字节核对 (C4)

独立 python 读 ROM `roms/2343.gba` 逐槽核 4 字节小端值。

**全 26 槽 (24 EQ + 2 RENAME) 值与 proposal 完全一致，无任何 MISMATCH。**

关键新建常量核对：

| 地址     | 常量名                        | 期望值       | 实际 ROM 值  | 结果 |
|----------|-------------------------------|-------------|-------------|------|
| 0x1e4e4  | CARD_STAT_ATK_DEF_OAM_XY     | 0x00060056  | 0x00060056  | OK   |
| 0x1e4e8  | CARD_STAT_ATK_DEF_OAM_ATTR2  | 0x0000d3a2  | 0x0000d3a2  | OK   |
| 0x1e4ec  | CARD_STAT_QPLAY_OAM_XY       | 0x00150058  | 0x00150058  | OK   |
| 0x1e4f0  | CARD_STAT_QPLAY_OAM_ATTR2    | 0x0000e3a6  | 0x0000e3a6  | OK   |
| 0x1e518  | CARD_STAT_DIGIT_OAM_ATTR2    | 0x0000f001  | 0x0000f001  | OK   |
| 0x1e55c  | CARD_STAT_DIGIT_OAM_ATTR2    | 0x0000f001  | 0x0000f001  | OK   |
| 0x1e564  | CARD_STAT_FUSION_OAM_ATTR2   | 0x0000c3a8  | 0x0000c3a8  | OK   |
| 0x1e610  | CARD_STAT_ROW_ATTR2_BASE_A   | 0xfffff800  | 0xfffff800  | OK   |
| 0x1e614  | CARD_STAT_ROW_ATTR2_BASE_B   | 0xfffff804  | 0xfffff804  | OK   |
| 0x1e618  | CARD_STAT_ROW_ATTR2_BASE_C   | 0xfffff808  | 0xfffff808  | OK   |
| 0x1e61c  | CARD_STAT_ROW_ATTR2_BASE_D   | 0xfffff80c  | 0xfffff80c  | OK   |
| 0x1e6bc  | CARD_INFO_STATE_CARD_ID_MASK | 0x00003fff  | 0x00003fff  | OK   |
| 0x1e6c0  | CARD_INFO_STATE_CARD_ID_CLEAR| 0xfffe0007  | 0xfffe0007  | OK   |
| 0x1e60c  | tile_r1 (RENAME)             | 0x00004040  | 0x00004040  | OK   |
| 0x1e6c8  | sentinel (RENAME)            | 0x0000ffff  | 0x0000ffff  | OK   |

复用槽核对（gCardInfoPageState x7, EWRAM_BASE x2, GSETTINGS_OFFSET x2）：全部 OK。

### ref-scan 重跑 (C3)

段内无 ROM_INCBIN / .byte 数据块（asm 扫描 lines 3243-3737 证实），§5.1 块为空。C3 vacuously 满足；无块需要 ref-scan。

### C2 ROM_INCBIN 覆盖

asm lines 3243-3737 扫描：0 个 ROM_INCBIN / 实质 .byte 行（.zero 是对齐填充，不计）。C2 成立。

### C13 残留 DAT_ 扫描

asm 扫描 lines 3243-3737 实测得 **26 个** DAT_ label 定义（无 DWORD_/UNK_）。Proposal 表中列了 26 行（24 EQ + 2 RENAME），全集完整覆盖，无遗漏。

注：Proposal header 写"x20"为笔误（实际表格 26 行），不影响覆盖正确性。

### C5 重值去重

对全部 17 个 constants/*.inc 文件做机器搜索：

- 12 个新建常量均不在任何现有 .inc 文件中。
- 特殊：0x1e6c8 = 0x0000ffff，`oam_attr.inc` 中有 `OAM_ATTR0_HIDDEN = 0x0000ffff`。
  但本处用法为 ATK/DEF 字段哨兵（card_stats_table row hword = 0xffff 表示 Spell/Trap 无 ATK），
  语义与 OAM hidden 不同。proposal 选 RENAME-only（不 equate，因 7616 ROM refs 太泛滥）
  且不复用 OAM_ATTR0_HIDDEN，判断正确。C5 无问题。

### C9 ASCII plate 核实

asm 扫描 lines 3243-3737 全部 @ 注释行：仅 **2 行**含 CJK：
- Line 3358: `@ p1/p2: 卡牌信息页顶层, card_id=(word0<<15)>>18`
- Line 3618: `@ TG.4-next: 卡列表按 A 进详情页的派发, 首 bl 即 card_info_page_enter_with_card_id`

Proposal PLATE 1/2 正好处理这两行，替换为纯 ASCII。
Proposal 的 5 条新 plate 文本均为纯 ASCII（人工核查 PLATE 1-5 内容无 CJK）。C9 OK。

### C8 stale FUN_ 核实

- FUN_0801e620: asm 中对应 `render_card_stats_oam_for_current_card`（label 在 line 3602），已命名。删除 parenthetical 正确。
- FUN_0801e714: asm line 3737 = `tick_card_info_page_by_state`，已命名。删除正确。

### C11 FUNC_RENAME=0 抽查

3 函数体语义 vs 名：
- `update_card_info_page_state` (0x1e36c): 体内读 gPrng 键标志、处理 gCardInfoPageState countdown/scroll 字段。名称描述状态更新，准确。
- `open_card_info_by_icid` (0x1e6cc): 体内 icid->cid 转换再调 card_list_on_select_to_info_page。名称描述 icid 适配器，准确。
- `open_card_info_page_from_list` (0x1e6f4): 体内 u16-extend r0/r1，调 card_list_on_select_to_info_page，设 gCardInfoPageState bit2。名称描述 list 直接入口，准确。

FUNC_RENAME=0 成立。

### C1 边界核实

- 地址序：Seg-3 end = 0x1e36c = Seg-4 start（连续，无跳号/回头）。
- Seg-4 end = 0x1e714：asm line 3737 确认 tick_card_info_page_by_state 从 0x1e714 开始（push {r4,r5,lr} = 0xb530）；最后 DAT_ = 0x1e710（< 0x1e714）。
- 所有 26 槽 addr 最大 = 0x1e710，全部 < 0x1e714。C1 OK。

### C6 label 格式与碰撞

全 26 个 slot label 均符合 `^[a-z][a-z0-9_]+$`，无重复，无碰撞。

同名多槽（如 `draw_card_stat_digits_to_oam_gcardinfopagestate_a/b`、`_digit_attr2_a/b`）已加后缀区分。

### C12 R6 消费者证据

所有 24 EQ 槽均有 file:line 引用 + 置信度标注（high/med）。
CARD_STAT_ROW_ATTR2_BASE_A..D 为 med 置信度，已在 proposal 中明确标注且说明理由（循环结构推断，未经 mGBA 验证）。符合 C12 要求。

### C7 REF_SLOTS

无新 carve/全局槽，REF_SLOTS 节声明 PTR_ 已符号化。C7 N/A。

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | Seg-3 end=0x1e36c = Seg-4 start；最大槽 0x1e710 < 0x1e714 |
| C2 Rule2 | PASS | 0 ROM_INCBIN/.byte 块；.zero 为对齐填充不计 |
| C3 Rule3 | N/A | 无 §5.1 块，vacuously OK |
| C4 R1 值 | PASS | 全 26 槽 ROM 4 字节小端核对 100% 匹配 |
| C5 R1 复用 | PASS | 12 新常量全局唯一；0x0000ffff 语义不同于 OAM_ATTR0_HIDDEN，不需复用 |
| C6 R2 名 | PASS | 全 26 label 符合规范；多同类加 _a/b 后缀，无碰撞 |
| C7 R3 接通 | N/A | 无全局槽/carve |
| C8 R5 现名 | PASS | FUN_0801e620/0x1e714 均已命名；proposal 删除 stale 括注正确 |
| C9 ASCII | PASS | asm 中 2 处 CJK plate 已被 proposal 覆盖为 ASCII；新 plate 全 ASCII |
| C10 carve | N/A | 无 carve 块 |
| C11 误名 | PASS | 3 函数抽查：名与体一致，FUNC_RENAME=0 合理 |
| C12 R6 | PASS | 所有槽有 file:line 证据 + high/med 置信度；med 槽已标注升级路径 |
| C13 残留 | PASS | asm 实测 26 DAT_，proposal 覆盖 26（24 EQ + 2 RENAME），无遗漏 |

---

## 状态: PASS

修改清单: 无。Proposal 可直接落地。

---

## 落地前置提醒 (fixer 参考)

1. Proposal header 中 "残留自动名槽 x20" 为笔误（实际 26），落地无影响，可选择修正或忽略。
2. `card_info.inc` 追加 12 个新常量（含注释格式见 proposal §新增 constants）。
3. 5 条 PLATE 改动：plates 1-2 替换 CJK；plates 3-4-5 删除 FUN_ 括注。
4. 26 个 DAT_ slot label 全部 EQ/RENAME，无 §5.1 登记，无 carve，无 disasm。
5. byte-identical SHA1 `9689337d` 必须在 build 后验证。
