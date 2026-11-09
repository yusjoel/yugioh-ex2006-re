# Refine Review: F14-Seg-5

## 审查边界

- 段: `asm/14_equip_ai_scoring.s [0x080acc30,0x080ade8c)`，4700 bytes。
- 第二轮冻结 manifest: `output/refine-run-20261028-105948/f14-seg5-freeze-manifest.json`，SHA256 `86fb68f23debb1f4e2b1082c62f04ef749ca1b3c0ba68b3fb8e4fe85b8dc4e7a`。
- proposal / slots / plates SHA256 分别为 `e580007963a9f48a70143bd147037115cde75acd55084e22d6ebd359bd9aee76`、`0fe6bd46a8d93421f0ef6f5bc2b6e609ba48c4fae5ccbbf424e7b5acd8e5e5bb`、`756195365a799c3b5c2981777dbc2fbe2f44a01800a52fda228810e24ac23145`。
- manifest 的 21 个 `review_basis` 文件逐项重算 SHA256 和长度，差异 0。首轮 review/audit 在不可变归档中的 SHA256 仍为 `8e14098ec0d96ca3df2220ab8a788978fc5135cff30d90a987a015f7e57a8f03` / `b6572e86a7cadfb227b690c7dfe2b4737f4d30b4c5484d1124297e3b8d0ed88f`。
- 第二轮独立机器审计: `output/refine-run-20261028-105948/f14-seg5-review-round2-audit.json`，SHA256 `8b6ab40d78c28268b9740cb2ef6969f3ab43976bac7c5259b95807e7577c3c37`。
- 当前 108 个保护 source 文件及 current/backup 两份 15-file Ghidra 物理数据库均逐文件重算，差异 0；本轮仅评审冻结 proposal 合同，尚未执行 Mode B。

## 第二轮窄差异

- `F14-Seg-5.slots.tsv` 仅 `0x080adc68` 的 7 个批准 after 字段变化；其余 149 行逐字段不变。动作仍为 `EQ_ADD`，原值、bytes、Data type、PC READ、无 DATA ref 的前态均未改变。
- `F14-Seg-5.plates.tsv` 仅 `0x080ad4c8/0x080ad510/0x080ad608/0x080ad720` 的 `new_plate` 及两处字符数字段变化；其余 16 行逐字段不变。
- 150 槽、20 PLATE、19 段内 Function、1 个必要段外 caller、两个改名及所有 before-state 合同与首轮冻结证据连续。

## 核验 (C1-C13)

| # | 检查 | 结果 | 独立证据 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | 活动文档 §五的 Seg-5 边界为 `[0x080acc30,0x080ade8c)`，与前段结束地址和 manifest 完全一致。 |
| C2 | Rule 2 raw 块归宿 | ✅ | 段内 raw 块为 0。覆盖仍为 1906 InstructionDB / 3976 code bytes + 150 words / 600 bytes + 62 padding / 124 bytes = 4700 bytes，无空洞或重叠。 |
| C3 | Rule 3 §5.1 零引用 | ✅ | carve/disasm/§5.1 均为 0。重新对两个改名入口做全 ROM 非对齐 raw 与 THUMB\|1 扫描，`0x080ad270/271`、`0x080ad844/845` 命中均为 0。 |
| C4 | R1 值 | ✅ | 150 槽逐一从 `roms/2343.gba` 读取 4-byte LE，`original_value` 与 `old_bytes` 差异均为 0；`0x080adc68` 仍为 `70feffff` / `0xfffffe70`。 |
| C5 | R1 复用 | ✅ | 121 行复用现有常量，11 行新增常量。10 个 CID 常量的结构化身份证据未变；常量目录不存在准确的 `ZONE_EFFECT_ATK_PENALTY_400` 同域名称。旧 `ZONE_EFFECT_ATK_PENALTY_500=0xfffffe70` 名称与算术不符，合同保留其定义及五个旧绑定，并只为 `0x080adc68` 新增准确的 `-400` Equate。 |
| C6 | R2 槽名 | ✅ | 150 个最终 source label 全部唯一且匹配 `^[a-z][a-z0-9_]+$`；`zone_effect_atk_penalty_400_lit_080adc68` 无碰撞。 |
| C7 | R3 接通 | ✅ | 132 EQ 均为 operand-0 Equate；8 个既有 DATA ref 按 CORE6 保留，10 个 REF_ADD 均为唯一 `DATA/USER_DEFINED/operand0/primary`。动态 `0x0201e500` 的唯一 USER 物化合同及其余静态 target ID/type/source 合同未变。旧 500 Equate 五个引用保持，新 400 Equate 仅批准 `0x080adc68`。 |
| C8 | R5 注释 | ✅ | 20 条新 PLATE 无自动名残留。四条首轮问题已按真实指令订正：AD510/AD720 的 r2 均为 eligibility-mode flag，排除表经第五栈参数传递；AD4C8/AD608 成功编码均为高字节 slot、低字节 player。 |
| C9 | ASCII | ✅ | 150 条新 EOL 与 20 条新 PLATE 全为 ASCII；最大 PLATE 424 chars。 |
| C10 | carve 指针 | ✅ | carve=0，无 THUMB 指针表或 `+1` 表达式动作。 |
| C11 | 误名 | ✅ | 两个改名入口的 body/caller 语义及全 ROM pointer-hold 仍闭合：AD270 是 field-spell placement bypass set；AD844 使用 `+0x18` count 和 `+0x3a0`、stride 4 的 chain-zone array。其余 17 个段内现名与 body 无矛盾。 |
| C12 | R6 消费者证据 | ✅ | 四项首轮问题已由真实消费者闭合：AD510 见 `asm/14_equip_ai_scoring.s:12498-12549`；AD720 见 `12787-12814` 及 caller `asm/15_equip_target_summon_zoom.s:6920-6929`；编码见 `12461-12482,12637-12658` 与解码 `12553-12558`；`0x080adc68` 的有符号加法见 `13547-13559`。proposal 的证据表、自检和直接派生计数均已同步。 |
| C13 | 残留覆盖 | ✅ | 段内 150 个 `.word` 地址集合与 TSV 精确相等；前态 150 个自动 source label（138 `DAT_`、6 `DWORD_`、6 `PTR_`）全部由 132 EQ + 10 REF_ADD + 8 REF_PRESERVE 覆盖。1906 个 InstructionDB 地址不进入数据动作。 |

## 首轮四项关闭证据

### #1 — AD510 r2 ABI：关闭

- `asm/14_equip_ai_scoring.s:12498-12506` 将 entry r2 保存到 r6，仅按 zero/nonzero 生成 mode；`12528-12549` 以同一条件驱动 normal/alternate selector。
- `12512` 从 callee `[sp,#0x40]` 读取 packed exclusion pointer，r3 保存为 excluded-entry count。新 424-char ASCII PLATE 与该接口一致。

### #2 — AD720 r2 ABI：关闭

- `0x4691@0x080ad72c` 为 `mov r9,r2`；`0x464a@0x080ad75c` 为 `mov r2,r9`，随后调用 AD510。
- `0x080ad752/756` 构造本地 `sp+4` exclusion buffer 并把其地址写入第五 outgoing stack argument；caller `0x080bb228` 在 `asm/15_equip_target_summon_zoom.s:6928` 传 r2=1。新 418-char ASCII PLATE 准确。

### #3 — 两个 selector 的编码顺序：关闭

- AD4C8 的 `0x080ad4e0..0x080ad506` 与 AD608 的 `0x080ad620..0x080ad646` 都计算 `(slot << 8) | player`。
- AD510 在 `0x080ad588..0x080ad58e` 抽取 low byte 给 player 参数、高字节给 slot 参数，独立确认新 PLATE 的 `slot in bits 15:8 and player in bits 7:0`。

### #4 — `0x080adc68` 的 `-400` 常量：关闭

- `0xfffffe70` 的 s32 值为 `-400`；`asm/14_equip_ai_scoring.s:13547-13559` 将它直接加到 zone score。
- `root-f14-seg5-penalty-equate-prestate.json` 冻结旧 `ZONE_EFFECT_ATK_PENALTY_500` 的五个 operand-0 引用 `0x08037e14/2c/44/5c`、`0x080650ec`，同时证明新 `ZONE_EFFECT_ATK_PENALTY_400` 前态不存在、`0x080adc68` 前态无 Equate。
- 新合同只在 `constants/field_spell_bonus.inc` 追加 `.equ ZONE_EFFECT_ATK_PENALTY_400, 0xfffffe70` 并绑定 `0x080adc68`；旧定义、五个旧绑定、其余槽和代码均保持。

## 状态: PASS

四项首轮清单已全部关闭，未发现新增修订项。允许进入 Mode B；本结论不替代落地后的 byte-identical、source scope、DB state、registry/CSV/inventory 和旧 500 / 新 400 Equate 引用门禁。

## Reviewer Verdict: F14-Seg-5 = PASS
