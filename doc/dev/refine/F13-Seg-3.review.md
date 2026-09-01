# Refine Review: F13-Seg-3

## 第一轮独立复核

- 范围：`[0x0809f744,0x080a0840)`，4348 B。
- proposal SHA256：`59836f75543608441c7188cfe5f0a1e5f80ca1cfe35bcb01a53d88ee69063fc1`。
- plan SHA256：`9062fe541dcb8529ed607868cc5bb959113483aeb6c5dc198da3babfd9c69acb`。
- plates SHA256：`5eab55dbf65fe3792d0efd1e189ddf5646ff456bc82eefbb7e52dcad0c5c53f5`。
- selfcheck SHA256：`1d2b454582c20cc3dd330867437dd292d6c7982039a0c3db423d9c8ac9e8c6d5`。
- 当前 `asm/13_equip_placement.s` SHA256：`634dafdad722f681b8f308cd112229f5363c7825c13f3536f0de27c9fdfbda49`。
- ROM SHA256：`f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。
- P0：通过。proposal 存在、非空，没有中止标记。

本轮没有采用 executor 的 PASS 项作为证明。我从当前 asm 重新枚举自动槽，按 ROM 指令重新解码 Thumb literal LDR，逐槽读取 ROM little-endian word；另对两张外部表的每个候选地址重跑全 ROM raw/THUMB|1 扫描，并从当前 constants、卡表、函数体、改名依赖和 exporter 源码独立核对语义与可落地性。证据写在：

- `output/refine-run-20260831-194634/f13-seg3-review-mechanical.json`
- `output/refine-run-20260831-194634/f13-seg3-review-constants.json`
- `output/refine-run-20260831-194634/f13-seg3-review-cids.json`
- `output/refine-run-20260831-194634/f13-seg3-review-functions.json`
- `output/refine-run-20260831-194634/f13-seg3-review-ghidra-prestate.json`
- `output/refine-run-20260831-194634/f13-seg3-review-names-comments.json`
- `output/refine-run-20260831-194634/f13-seg3-review-rename-deps.json`
- `output/refine-run-20260831-194634/f13-seg3-review-registry-plate.json`

## 三条硬规则

| 规则 | 结果 | 独立证据 |
| --- | --- | --- |
| 地址序 | ✅ | 活动文档 §五把 Seg-3 定为 `0809f744..080a0840`；Seg-1/2 已闭合，Seg-4 从 `080a0840` 开始。本提案没有分析或修改 Seg-4。 |
| 函数间块必须处理 | ✅ | 当前段内 `ROM_INCBIN=0`、`.byte=0`。本段三个真实 literal 引用所需的段外表按消费者界定为 54+4 word，并全部进入 carve。 |
| §5.1 只收全 ROM 零引用块 | ✅ | 本段 §5.1 为 0。对 `09e477ac..09e47894` 每个 4 B 候选地址重扫 raw/THUMB|1；仅 `09e477ac` raw 命中 `0809fb8c`，`09e47884` raw 命中 `0809fb84/0809fbcc`，内部候选地址与所有 THUMB 地址均无命中。两块都有真实消费者，未误入 §5.1。 |

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
| --- | --- | --- | --- |
| C1 | Rule1 范围/路线图 | ✅ | `p5-refine-13-equip-placement.md:120` 与本提案边界、函数簇和自动槽类别一致；没有跳号或回头。 |
| C2 | Rule2 裸块全归宿 | ✅ | 段内没有裸块。外部依赖表由 `0809fb24..3a` 的四次循环和 `0809fb44..72` 的 cursor `0..0x35` 循环固定为 4、54 项；没有静默保留。 |
| C3 | Rule3 独立 ref-scan | ✅ | 已对两表共 58 个候选地址逐项扫 raw 与 `addr|1`，结果见 `f13-seg3-review-mechanical.json`；结论与真实消费者一致。 |
| C4 | R1 槽值 | ✅ | 从 asm 独立枚举 138 槽=`106 DAT+15 DWORD+17 PTR`；proposal 的 `98 EQ+21 REF+19 RENAME` 地址并集唯一且等于该集合。138/138 ROM word 匹配；153 条真实 Thumb literal LDR 的 opcode 解码 target 与 proposal uses 完全相同。 |
| C5 | R1 常量复用 | ✅ | 当前 `constants/*.inc` 实际 6022 个 `.equ`、无重复名。17 个 NEW 名和值均不存在；30 个唯一 REUSE 名和值均精确命中现定义。`gEquipActivationScanCursor=0201e204` 同时等于 `gP1LifePoints+1d24` 与 `gDuelFieldSlots+FIELD_STATE_OFF`，本段消费者实际把它用作 `0..9` 扫描 cursor。 |
| C6 | R2 命名/碰撞 | ✅ | 138 个槽名唯一且全匹配 `^[a-z][a-z0-9_]+$`；两个表头、6 个函数新名及 17 个 NEW 常量没有现存同名碰撞。`gEquipActivationScanCursor` 同时作为同地址 `.equ` 与 USER label 是有意的单一全局，不是两个符号冲突。 |
| C7 | R3 接通/导出 | ✅ | 21 REF 槽前态均无 outgoing ref，提案为其建立精确 operand0 DATA/USER_DEFINED primary ref。19 RENAME 槽原引用为 17 DEFAULT+2 USER_DEFINED，提案保持引用本体不变。`09e477ac/09e47884` 新 USER 主 LABEL 可使三个代码池导出表名。`080a01c8/080a02b8` 的 odd callback 用 equate fallback，辅助 DATA ref 指向偶 Function；`ExportRangeToGas.py:506-562` 对 ROM Function 返回空，随后 `:565-583` 取 equate，计划可执行。 |
| C8 | R5 现名/残留 | ✅ | 20 条新 Ghidra PLATE 中 `FUN_/DAT_/DWORD_/PTR_DAT_/UNK_/SUB_` 命中均为 0，并使用6个拟议新函数名。真实指令扫描确认6个改名入口的 direct incoming 数为 `0/5/0/8/5/1`，raw odd 命中仅 f744@`09e47814`、f9cc@`09e5aac8`。 |
| C9 | ASCII/长度 | ❌ | 20 条实际 Ghidra PLATE 全 ASCII，长度 170..405；138 条 EOL 全 ASCII。但 proposal:254 还要求在 registry 的 `FUN_0809ed50` PLATE 上只替换旧 f744 名。该可执行 plate payload 当前 630 字符，替换后 633，超过 500；见修改项 #2。 |
| C10 | carve THUMB +1 | ✅ | ROM 两表共 58 word 全为 odd；逐项 `raw == 当前函数入口+1`，包括拟改名 f744 的 `09e47814=0809f745`。host `.incbin` 从 offset `1e477ac` carve `0xe8` B 后续为 offset `1e47894`、长度 `0x2478=0x2560-0xe8`，边界 `09e47894` 不变。 |
| C11 | 函数误名 | ✅ | f744 实算 `slot=cursor%5+5`，旧 monster-zone 名错误；f89c 的13项 BST 同时覆盖非 field-spell maintenance 卡；f9cc 由 equip phase table 间接调用并驱动 display phase，不读 AI choice/result。fb16/a06a4/a06a6 分别是同一 `0x298` frame 的 return0、return1、release 入口，Function ID/body/控制流合同保持。其余14个现名与函数体未发现必须改名的矛盾。 |
| C12 | R6 消费者/事实证据 | ❌ | 所有138槽的真实 LDR source、表边界、函数输入/返回和状态转换均可由指令闭合；32个 CID 候选也按 `cards-ids-array.s` 正确列复核。但 proposal:508 与 plan 的 NEW reason 把 Armor Exe 密码写错，见修改项 #1。 |
| C13 | 残留自动槽全覆盖 | ✅ | 独立 asm 枚举得到 138 个 4 B 自动槽，proposal 地址集合无遗漏、无额外地址、无重复动作；段末下一个自动槽在 Seg-4。 |

## R1-R9 复核

| 项 | 结果 | 说明 |
| --- | --- | --- |
| R1 常量 | ✅ | 98 EQ 的 ROM 值、17 NEW 和 30 REUSE 均闭合；修改项 #1 只纠正文档证据，不改变常量名和值。 |
| R2 标签 | ✅ | 自动槽、表头和 RAM 全局命名可读且无碰撞。 |
| R3 接通 | ✅ | RAM/ROM 表头、odd callback equate fallback 与引用 source 保留合同完整。 |
| R4 disasm | ✅ | 段内无裸代码，`disasm=0`有证据支持。 |
| R5 注释 | ❌ | 本段20条真实 PLATE 合格；registry 的段外 sibling plate 更新方式不满足 500 字符上限。 |
| R6 消费者 | ❌ | 指令消费者已闭合，但 Armor Exe 的密码旁证与本地三份权威数据冲突。 |
| R7 carve | ✅ | 两表尺寸、顺序、58个 `fn + 1` 和 host 切割精确。4项表只改 `rom.s` 表示，不给后两项臆造 Ghidra Data/ref。 |
| R8 图形 | ✅ | 本段没有图形资产。 |
| R9 byte-identical/备份 | ✅（计划） | 提案要求落地前态守卫、完整重导与 ROM SHA1；本轮只评 proposal，未 build、未写 Ghidra。 |

## 关键独立证据

1. `09e477ac..09e47884` 的 54 项 Ghidra 前态全部为 4 B `/undefined *`，每项恰一条 operand0 DATA/DEFAULT primary ref 到 ROM 中存放的 odd 地址；只有表头有动态符号。`09e47884..94` 前两项为 `/undefined4`/4 B、后两项 Data=None/1 B，四项均无 outgoing ref；`09e47894` 也为 Data=None/1 B。proposal 对二者采取不同落地策略是正确的。
2. 20 个既有 Function 的 ID、body ranges、body size、旧 plate hash均与只读前态一致；按 ranges 从 ROM 重新拼接的20个 body SHA256全部一致。f9cc 的 odd入口在 `EQUIP_PHASE_FN_TABLE_ROM[2]=0809f9cd`；调用 hub 在 `asm/12_equip_activation_scan.s:1521-1541`按 main phase 索引并在非零返回时推进 phase。
3. Armor Exe 的真实链路一致：`data/cards-ids-array.s:1669`为 `icid=161b -> cid=1279`，`doc/um06-deck-modification-tool/data.md:1259`、`data/card-stats.s:16642/44695`与`data/card-passcodes.s:1301`均给出密码 `07180418`。proposal 的 `71950093`没有本地证据支持。
4. `RenameKnownFunctions.py` 的 `FUN_0809ed50` tuple 第三字段当前 SHA256 为 `93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc`、630字符；简单换名后633字符。Seg-2 已审定并已在当前 asm 导出的真实 plate 是 `asm/13_equip_placement.s:2982` 的347字符 ASCII 全文，SHA256 `a4e4cb281edffe3e3534690a3883fdd4b69ae802c1c14e6732199205273b27e1`。

## 状态: NEEDS_FIX

## 修改清单

### #1 — C12/R6 — 纠正 ARMOR_EXE_CID 的密码旁证并同步派生输入

1. 把 proposal:508 与 `f13-seg3-plan.json` 中 `ARMOR_EXE_CID=0x0000161b` 的 reason 从 `password 71950093` 改为 `password 07180418`。
2. 同步生成该 reason 的 `f13-seg3-plan-command.txt`（或实际生成源），重新生成 proposal/plan，并刷新 selfcheck 的输入 hash/修订说明。现有 `f13-seg3-cid-proof.json` 已记录正确的 `07180418`，不得反向改坏。
3. 保持 `ARMOR_EXE_CID` 名、值、目标文件、slot `0809fcd8`、138动作、17 NEW、20 PLATE、6 FUNC_RENAME 和两张 carve 表完全不变；增加检查以断言 proposal/plan 的四个新具名 CID 密码与正确 CID 列、card-stats、passcode 三方一致。

### #2 — C9/R5 — registry sibling plate 必须完整同步为已审定的 <=500 ASCII 全文

1. 不得执行 proposal:254 所述的630字符旧 registry plate substring 替换。对 `RenameKnownFunctions.py` 中 key=`FUN_0809ed50`、target=`scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend` 的 tuple，先守卫当前第三字段全文或 SHA256 `93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc`，再把第三字段完整替换为 Seg-2 已审定的347字符全文：

   ```text
   r0=player. Resume ten monster slots with LP+0x1d24 cursor: side=(cursor/5)^player, slot=cursor%5. For active Infernalqueen Archfiend, pack the actual entry CID, side and slot, then call activation with decoded flags. Ignore its result; advance cursor and return 0 after the first match. Other entries advance and continue. Return 1 after cursor 9.
   ```

   新全文 SHA256 必须为 `a4e4cb281edffe3e3534690a3883fdd4b69ae802c1c14e6732199205273b27e1`，ASCII、347字符。
2. 在 proposal、plan rename dependency/guard 和 selfcheck 中把“sibling PLATE substring”改为上述完整 registry tuple plate 同步，并验证本轮会触及的7个 registry plate payload（6个改名tuple及此 sibling tuple）全 ASCII、均不超过500字符。
3. 这是 registry-only 依赖同步：当前真实 `0809ed50` Ghidra/asm plate 已是该347字符全文，不新增第21条 Ghidra PLATE，不改其 Function、body、refs、EOL或机器字节；本段20条 Ghidra PLATE及其他动作计数保持不变。

## Reviewer Verdict: F13-Seg-3 = NEEDS_FIX(2 items)

## 第二轮独立复核

- 轮次：2/3。
- proposal SHA256：`f00685aad1690e7c4264311ecbe941e429c0e7a400136a882497725643fea89c`。
- plan SHA256：`c0438860bcdbfc05f8a4db4be8fe2e347362b8cb007247e3ccf15fe64ac90b12`。
- plates SHA256：`5eab55dbf65fe3792d0efd1e189ddf5646ff456bc82eefbb7e52dcad0c5c53f5`，与第一轮逐字节相同。
- selfcheck SHA256：`ab377e76cbd2ff22c586fef9da364039a5a675bb82940b790f3a43b3ae76f114`。
- 当前 `asm/13_equip_placement.s` SHA256：`634dafdad722f681b8f308cd112229f5363c7825c13f3536f0de27c9fdfbda49`，与第一轮相同。
- 第一轮冻结 review SHA256：`e1f58fd1368ad020cfbbc74300494c807916f5964bba4513393b591de276fb24`。
- 独立差分证据：`output/refine-run-20260831-194634/f13-seg3-review-round2-diff.json`，SHA256 `33a10c487eb05b5d692e7a38f33b82292fe77bfba8466a518a10f47d5d688c7e`。
- P0：通过。新版 proposal 存在、非空，没有中止标记。

本轮先独立比较第一、二轮冻结输入，再复核首轮两项修订的真实来源。plan 的递归差分恰为6个路径：新增 `registry_sync`、`mode_a_revision` 和3个 registry guard，并只修改 `new_definitions[7].reason`；138个动作、动作计数、6个函数改名、20个段内 PLATE、两张58项 carve 表及其余16个 NEW 定义均未变化。proposal 只有4个差分块，plates 文件没有任何字节变化。新版 selfcheck 保留第一轮888个具名结果且内容逐项相同，新增10个针对本轮修订的检查，最终为898项、`failed=[]`；我另行读取其命令和真实输入验证了新增断言，并未把布尔结果本身当作证据。

## 第二轮三条硬规则

| 规则 | 结果 | 独立证据 |
| --- | --- | --- |
| 地址序 | ✅ | 范围仍为 `[0809f744,080a0840)`，没有新增段外代码分析；唯一段外动作是首轮已要求的 registry 字段同步。 |
| 函数间块必须处理 | ✅ | 第一轮独立枚举与当前 asm hash均未变化：段内裸块仍为0，两张外部依赖表仍精确 carve 54+4 word。 |
| §5.1 只收全 ROM 零引用块 | ✅ | §5.1仍为0；第一轮逐地址 raw/THUMB|1 扫描证据绑定同一 ROM、asm 和未变表范围，可以复用。 |

## 第二轮核验（C1-C13）

| # | 检查 | 结果 | 备注 |
| --- | --- | --- | --- |
| C1 | Rule1 范围/路线图 | ✅ | 范围、20个函数和后继边界均未变，没有扩入 Seg-4。 |
| C2 | Rule2 裸块全归宿 | ✅ | 段内 `ROM_INCBIN/.byte=0`；两张外部表及58项 carve 与第一轮完全相同。 |
| C3 | Rule3 独立 ref-scan | ✅ | 第一轮对58个候选地址执行的 raw 与 `addr|1` 全 ROM 扫描证据未受本轮文档修订影响。 |
| C4 | R1 槽值 | ✅ | `98 EQ+21 REF+19 RENAME=138` 的地址、值、用途和153条 LDR 解码记录逐项未变。 |
| C5 | R1 常量复用 | ✅ | 17 NEW 的名和值未变；仅 Armor Exe reason 的密码文本纠正。30个 REUSE 仍与第一轮6022常量定义扫描一致。 |
| C6 | R2 命名/碰撞 | ✅ | 槽名、表名、函数名和常量名均未变，第一轮碰撞扫描继续成立。 |
| C7 | R3 接通/导出 | ✅ | 21 REF、19 RENAME、odd callback equate fallback 和58项表的引用合同未变；本轮 registry-only 字段替换不触碰 Ghidra 引用。 |
| C8 | R5 现名/残留 | ✅ | 20个段内 PLATE 全文逐字节不变，仍无自动名残留；6个改名依赖未变化。 |
| C9 | ASCII/长度 | ✅ | 首轮问题 #2 已闭合。`FUN_0809ed50` registry tuple 当前第三字段唯一命中，旧全文630字符、SHA256 `93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc`；提案现要求受守卫的完整字段替换，目标为347字符 ASCII、SHA256 `a4e4cb281edffe3e3534690a3883fdd4b69ae802c1c14e6732199205273b27e1`。6个改名 payload 加此 sibling 共7项，长度 `327/320/405/353/187/264/347`，全部 ASCII 且不超过500。 |
| C10 | carve THUMB +1 | ✅ | 两表58个 odd word、`fn+1` 值和 host 切割均未变化；plates 文件逐字节相同。 |
| C11 | 函数误名 | ✅ | 6个 FUNC_RENAME 的地址、body、incoming 和 odd raw 依赖未变化；没有新增或撤销改名。 |
| C12 | R6 消费者/事实证据 | ✅ | 首轮问题 #1 已闭合。新版 proposal/plan 均只写 `07180418`，不再含 `71950093`。独立读取 `data.md:1259`、`card-stats.s:16642/44695`、`cards-ids-array.s:1669` 和 `card-passcodes.s:1301`，确认 Armor Exe 为 ICID `161b`、逻辑 CID1279、密码 `07180418`。selfcheck 也按正确 CID 列、stat记录和passcode三方核对4个新具名 CID。 |
| C13 | 残留自动槽全覆盖 | ✅ | plan actions 与第一轮逐项相同，138/138自动槽仍唯一覆盖，无新增或遗漏。 |

## 第二轮 R1-R9 结论

| 项 | 结果 | 说明 |
| --- | --- | --- |
| R1-R4 | ✅ | 常量、标签、接通和无 disasm 结论复用第一轮未变输入的独立证据。 |
| R5 | ✅ | 段内20个 PLATE 不变；段外 sibling 改为受旧全文/hash守卫的347字符完整 registry 字段替换，不新增 Ghidra PLATE。 |
| R6 | ✅ | Armor Exe 密码证据已与五处真实来源闭合，其余消费者证据未变。 |
| R7-R8 | ✅ | 58项 carve 合同未变；本段无图形资产。 |
| R9 | ✅（计划） | 本结论只批准 proposal；Mode B仍须依提案执行前态守卫、重导和 byte-identical 验证。本轮未写 Ghidra、未 build。 |

## 第二轮状态: PASS

首轮两项修改清单已全部精确解决，没有新增修改项。此 PASS 仅针对 SHA256 `f00685aad1690e7c4264311ecbe941e429c0e7a400136a882497725643fea89c` 的 proposal。

## Reviewer Verdict: F13-Seg-3 = PASS
