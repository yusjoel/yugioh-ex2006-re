# Refine Review: F13-Seg-6

## 审查对象与独立取证

- 固定范围：`[0x080a27a0,0x080a38fc)`，4444 B。
- proposal SHA256：`18d731242d6d485021c6632634a6ba1dafed194c19e6e720f84b61796d5b4db3`。
- slots TSV SHA256：`2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe`。
- 本轮直接读取 `roms/2343.gba`、`asm/13_equip_placement.s`、`constants/*.inc`、`asm/rom.s`、`temp/ghidra-functions.csv`、消费者与活动文档；没有采用 executor 的 refscan、direct-edge 或 self-check 作为结论。executor 产物仅在独立结果形成后用于集合交叉。
- 独立解析当前 asm 机器行并读取 ROM：184 个自动四字节槽全部逐值一致；现有代码为 1712 instruction units / 3590 B，另有 189 words / 756 B 和 47 个 2 B padding；尾块反汇编后为 1714 instruction units / 3594 B，总计 4444 B，无重叠或未归因字节。

## C1-C13 核验

| # | 检查 | 结果 | 独立证据与结论 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | `refine-progress.md:11-12`、活动文档 `p5-refine-13-equip-placement.md:43-50,151,161-168` 均指定 Seg-6 为 `[080a27a0,080a38fc)`；proposal 未进入下一函数 `080a38fc`。 |
| C2 | Rule 2 每个裸块有归宿 | ✅ | 当前范围内没有 `ROM_INCBIN`，唯一裸块为 `asm/13_equip_placement.s:13574-13575` 的 `[080a38f8,080a38fc)`；ROM 字节 `01 20 70 47` 解码为 `movs r0,#1; bx lr`，R4 + Function create 正确。carve=0。 |
| C3 | Rule 3 零引用 | ✅ | proposal 不新增 §5.1。独立全 ROM packed scan 对 `080a38f8` 与 `080a38f9` 均为 0 hit，但直接 Thumb BL 解码得到唯一入边 `080a187a -> 080a38f8`（`asm/13_equip_placement.s:8863`），故该块必须 R4。既有两块 `[080a1dd8,080a1de8)`、`[080a1f54,080a1f68)`没有被本段 378 条直接边命中。 |
| C4 | R1 ROM 值 | ✅ | 独立读取 184 个 slot 的 ROM little-endian word，184/184 与 TSV `original_value` 相等；其中 EQ=138。五个 switch words `080a2b00..080a2b10` 依次为 `080a2b14/2b44/2b5c/2b9c/2c28`。 |
| C5 | R1 复用/NEW | ✅ | 169 REUSE 均可在现有 constants 或 Function inventory 解析且数值匹配。15 NEW 对应 3 个新数值常量和 8 个 Thumb alias（11 个唯一新定义）；新名当前均无碰撞。`0x1d10` 仅有既存 `DISPLAY_SEQ_ACTIVE_PLAYER_OFF` 同值，但该名以 `gP1LifePoints` 为基址；`080a3450..3458` 明确以 `gDuelFieldSlots` 为基址并到达 `gEquipLpActivBitmap`，不复用成立。 |
| C6 | R2 命名形式/碰撞 | ✅ | 184 个 `slot_label` 全部唯一、ASCII，均匹配 `^[a-z][a-z0-9_]+$`，且对现有 asm/constants 定义扫描为 0 碰撞；11 个新定义同样无碰撞。 |
| C7 | R3 LABEL + DATA-ref 接通 | ❌ | TSV/提案只给出 14 个 `(slot,target)` 和“operand-0 DATA reference”（proposal:61-65,176），没有分别冻结五个唯一 target LABEL 的 pre/post `name/source/type/namespace/primary/alias/Data`，也没有冻结 14 个 pool reference 的 `operand/type/source/primary`。尤其 `080a2b00` 当前导出为 scoped `switchD_080a2af0__switchdataD_080a2b00`，提案未说明如何在同一 Symbol 对象上规范为 global USER_DEFINED `equip_target_selection_phase_jump_table` 并禁止 alias。该合同不足以执行 fail-closed dry/persisted check。 |
| C8 | R5 现名/自动名残留 | ✅ | 八个现有 PLATE 中独立找到 2 个 stale `FUN_` 与 6 个 stale `DAT_`；九个拟写 PLATE 均不含 `FUN_/SUB_/DAT_/DWORD_/PTR_/UNK_`，引用均为当前语义名。注释事实错误另在 C12/R5 裁定。 |
| C9 | ASCII/长度 | ✅ | 9 个 PLATE 全 ASCII，字节长度为 `201/266/241/204/171/197/207/167/180`，最大 266；184 个 TSV EOL 全部非空且 ASCII，最大 83；均不含自动名。 |
| C10 | Thumb odd/even | ✅ | 11 个 odd callback word 逐项等于对应 Function entry + 1；其余 4 个 NEW 是数值常量槽。五个 switch target 为精确 even code addresses。 |
| C11 | Function/误名 | ✅ | `temp/ghidra-functions.csv` 在段内精确有 16 个 USER_DEFINED Function，独立按相邻入口和 code/pool/padding 分区得到的 16 组 body ranges、instruction counts、byte lengths均与当前 inventory 一致；`080a38f8` 当前无 Function，`080a38fc` 是下一 Function。尾体精确 2 指令/4 B、无读入参、返回 1，唯一 caller 是 `tick_equip_display_row_by_type` case 13，`return_equip_row_type_13_complete` 满足 R1 `verb_object[_qualifier]`。既有 Function rename=0 成立。 |
| C12 | R6 消费者/语义证据 | ❌ | 184 个槽的 decoded PC-relative LDR consumers 与 TSV 精确一致且每槽至少 1 个；但提案有两处可执行语义错误：一是 proposal:112 称 `0x1d9e` 在 `080a2b22..2b26` 被 cleared，实际 `asm/13_equip_placement.s:11554-11556` 为 `strh r4`，而 r4 是入参 r2 的 low8；caller `080a17e8..17ea` 传入 `EQUIP_REROLL_COUNT_TARGET_OFF` 字段，随后 case 4 在 `080a2c28..2c34` 递减。二是 proposal:137 的 `080a2c64` PLATE 称需 `query_slot_effect_eligibility_nonzero` “to succeed”，实际 `080a2cae..2cb4` 在返回非零时跳到失败出口；合格条件是该调用返回 0。 |
| C13 | 残留/完整覆盖 | ✅ | 当前自动槽独立清点精确为 184=`DAT66+DWORD101+PTR17`，与 TSV 一一对应，0 缺失、0 多余、0 地址/值错配。动作精确 `EQ138/REF14/RENAME32`。全 ROM slot-address scan 为 182 个 raw/odd=`0/0`，`080a2800=4/0`，`080a2968=1/0`；五个 raw 命中均位于资产字节且不是机器行、结构化指针或控制流引用。独立直接边为 378=`Bcc186+B109+BL83`，296 段内、82 段外/34 unique；所有段内目标是 instruction boundary，所有段外目标是现有 Function entry。加唯一入边 `187a->38f8` 为 379；`18ba->0b20` 是独立 Seg-5 边，未混淆。 |

## R1-R9 核验

| 规则 | 结果 | 结论 |
|---|---|---|
| R1 常量 equate | ✅ | 138 个 EQ ROM 值正确；REUSE/NEW 数值与定义规划一致。 |
| R2 自动名语义化 | ✅ | 184 槽全覆盖，命名形式、唯一性及碰撞检查通过。 |
| R3 USER label + DATA ref | ❌ | 五个目标 LABEL source 与 14 个引用 source/primary 合同未分离冻结，`080a2b00` 的同对象规范化路径未定义。 |
| R4 误标代码反汇编 | ✅ | `080a38f8..38fc` 有真实 BL 入边，字节和 Thumb 边界明确；前一函数在 `38e8` 返回，`38ec..38f4` 是 pool，不存在 fall-through。 |
| R5 注释使用现名且事实正确 | ❌ | 自动名清理方案正确，但 `080a2c64` replacement PLATE 把 callee 返回条件写反。 |
| R6 先读消费者 | ❌ | PC-relative 全覆盖；`0x1d9e` 的写入语义被误述为 clear，须按 caller/寄存器数据流订正。 |
| R7 carve | ✅ | 本段没有可 carve 数据块；唯一裸块是可达代码。 |
| R8 图形核对 | ✅ | 段内不存在图形资产候选；唯一裸块由机器码与控制流完成分类。 |
| R9 备份/回滚/byte-identical | ❌ | proposal:155-184 有 source scope、inventory、dry counts、persisted/source/build门禁，但没有要求写入前 `.rep` 物理备份及 15/15 hash 核验，没有定义 apply/post/persist/export/build 任一步失败后的事务 rollback + 物理恢复，也没有要求 fresh `-noanalysis -readOnly` 查询前后 DB hashes 不变。 |

## 独立计数摘要

- 槽：184=`66 DAT + 101 DWORD + 17 PTR`；动作 `138 EQ + 14 REF + 32 RENAME`；`169 REUSE + 15 NEW`。
- 布局：现有 `1712 instructions / 3590 B + 189 words / 756 B + 47 padding / 94 B + tail 4 B`；R4 后 `1714 instructions / 3594 B`，总长 4444 B。
- Function：16 个现有 body 保持；创建 `080a38f8..080a38fc` 一个 Function；inventory 计划 `5212/5122/90 -> 5213/5123/90` 合理；refine-created Function 不新增历史 CSV 评分行合理。
- 边：段源 378，段内 296，段外 82/34 unique，另 1 条控制入边，总 379；历史 §5.1 命中 0。
- 注释：9 PLATE、184 EOL 全 ASCII；PLATE 最大 266 B。

## 状态: NEEDS_FIX

## 修改清单

### #1 — C7 / R3 — 补齐 target LABEL 与 pool reference 的双层 source 合同

在 proposal 中新增五个唯一 REF target 的独立 pre/post 表：`0201e2a0 gDuelCardCtxBase`、`0201c510 gDuelFieldSlots`、`0201bb90 gEquipChainSlotRefs`、`0201e220 gEquipLpActivBitmap`、`080a2b00 equip_target_selection_phase_jump_table`。每项必须冻结 target 的 address、primary name、Symbol type、source、namespace、Symbol ID、alias count、Data type/length，并说明合法动态 ID 变化条件。对 `080a2b00` 明确：复用并规范同址唯一 primary Symbol 为 global USER_DEFINED 名，保留五个 switch word 的 Data/值，不创建 alias/重复 label。

另列 14 个 REF slot 的精确 post tuple：`from, operand=0, to, type=DATA, source=USER_DEFINED, primary=true`，同时冻结 pre tuple/无引用状态；dry 与 fresh persisted check 必须分别检查 target LABEL 和 pool reference，禁止由导出文本或彼此状态推断。

### #2 — C12 / R6 — 订正 `0x1d9e` 的消费者证据

把 proposal:112 的 “is cleared at 0x080a2b22..0x080a2b26” 改为可由机器行复核的事实：`tick_equip_target_selection_display_seq` 将入参 r2 截为 low8 存入 r4，case 0 在 `080a2b22..2b26` 把 r4 初始化到 `[gP1LifePoints+0x1d9e]`；case 4 在 `080a2c28..2c34` 读取并在值大于 1 时递减。补入 caller `080a17e8..17ea` 从 `EQUIP_REROLL_COUNT_TARGET_OFF` 取 r2 的证据。常量名 `EQUIP_TARGET_SELECTION_DELAY_OFF` 可保留。

### #3 — C12 / R5 — 修正 `080a2c64` replacement PLATE 的返回条件

将 proposal:137 中 “query_slot_effect_eligibility_nonzero to succeed” 改为无歧义事实，例如：`Rejects the candidate when query_slot_effect_eligibility_nonzero returns nonzero.` 必须保留纯 ASCII，并重新计数 PLATE 长度不超过 500 B。

### #4 — R9 — 增补物理备份、失败恢复与 fresh read-only 门禁

在 landing plan 中明确：任何 Ghidra dry/apply 前建立新的 `.rep` 物理备份，核对 current/backup 15/15 文件及 hash；冻结 proposal/TSV/review/plan/script hashes；dry 为只读且 `0 FAIL`，退出前后 DB hash 不变。real apply 的 transaction/postcheck/save、persisted check、全量导出、mode 处理、inject、split、`export_all.py`、`NOPAUSE=1 build.bat`、ROM size/fc/SHA1、source-scope/inventory 任一步失败时，立即 rollback，并从该物理备份恢复后再做 fresh prestate 验证；禁止写 progress/receipt 成功态。保存成功后另启 fresh `-noanalysis -readOnly` 复核完整计数和合同，查询前后 15 个 DB 文件 hash 必须完全相同。最终 ROM 必须为 33554432 B 且 SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

## Reviewer Verdict: F13-Seg-6 = NEEDS_FIX(4 items)

---

## 第二轮独立复审

### 复审输入

- 修订 proposal SHA256：`4080946cbf31f7cb9db68901b56466a3a1a473fdd7fae2e4034bea8d03ebcac6`，与 driver 给定值一致。
- slots TSV SHA256：`2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe`，与首轮完全相同。
- C7 raw prestate SHA256：`e85ecaf4fd4ce0c82376c17e9af8a3aedc17330fb17e7cd9242ade0da589e12c`。
- 本轮逐项读取修订 proposal、原 TSV、raw prestate JSON 与取证脚本，并重新对照当前 asm/ROM/constants 和首轮独立结果；没有采用 Fixer Mode A Report 作为结论。

### 首轮 Fix #1-#4 闭合情况

| 首轮项 | 结果 | 第二轮独立结论 |
|---|---|---|
| Fix #1：C7 双层 source 合同 | ❌ 部分闭合 | 五个 target 的 pre/post Symbol/Data 合同已补齐。raw JSON 独立核得四个 RAM target 均为唯一 global USER_DEFINED Label、`/undefined4`/4 B；`080a2b00` 确为唯一 ID=5854、ANALYSIS、namespace=`switchD_080a2af0`、`/pointer`/4 B、alias=0，提案要求同一 ID 移到 Global 并改为 USER_DEFINED，禁止 `createLabel`/alias，正确。14 个 REF 的 pre Symbol 和空引用、post Symbol 及 `(operand=0,type=DATA,source=USER_DEFINED,primary=true)` 已逐槽列全；但 14 个 slot 自身的 pre/post Data 类型和“不 retype”合同仍缺失，且 dry/post/fresh 没有要求逐槽验证该 Data。 |
| Fix #2：`0x1d9e` 数据流 | ✅ 闭合 | proposal:150 已准确记录 `r2 -> low8 -> r4`，case 0 的 `strh r4` 初始化，以及 case 4 在值大于 1 时递减；与 `asm/13_equip_placement.s:8790-8791,11554-11556,11690-11696` 一致。 |
| Fix #3：`080a2c64` PLATE | ✅ 闭合 | proposal:175 已改为非零返回时 reject，与 `080a2cae..080a2cb4` 的 `cmp r0,#0; bne failure` 一致。新 PLATE 为 ASCII，270 B，小于 500 B。 |
| Fix #4：R9 | ❌ 部分闭合 | proposal:204-213 已加入新 `.rep` 物理备份、15/15 path/size/SHA256、冻结输入、fresh `-noanalysis -readOnly`、事务失败恢复、全流水线及 ROM SHA1 门禁。但 formal source snapshot 只包含授权改动文件、四个 inventory 与进度文档；全量 exporter/split 会接触的其他 24 个 asm 模块、`asm/includes.inc`、CSV/registry 等没有进入同一 scope/rollback baseline。发生越界改动时无法按该 snapshot 逐文件检测并恢复。 |

### C7 raw prestate 的独立核对

- 五个 target 与 proposal:74-78 全字段一致；`080a2b00` 的 `ID=5854`、qualified name、ANALYSIS source、scoped namespace、primary、0 alias 和 `/pointer`/4 B 均由 raw JSON 直接复现。
- 14 个 REF slot 地址与 TSV 完全一致，均只有一个 global primary DEFAULT Label、alias=0、`references_from=[]`；其 ID、旧名与 proposal:88-101 逐项相等。
- raw JSON 还给出了 14 个 slot 的 Data，但 proposal 没有把它们纳入合同：`080a29c8`、`080a2afc`、`080a2b78` 为 `/undefined4`/4 B；其余 11 个为 `/dword`/4 B。section 3.2 的 post 要求只覆盖 Symbol/reference，section 3.2 尾部的 persisted 要求也只写 target Data，没有要求 14 个 slot Data 保持。
- proposal:25 声称本次 fresh 查询前后 15 个 DB 文件 path/size/SHA256 一致；唯一新增的 `f13-seg6-ref-prestate.json` 只有 `mode/targets/slots` 三组字段，取证脚本中的 `mode="read_only_prestate"` 是脚本写入的常量。当前证据集中没有命令行、退出码或 DB before/after hash manifest，因此不能独立证明该次查询实际使用 `-noanalysis -readOnly` 或 DB 物理文件未变。

### 第二轮 C1-C13

| criterion | 结果 | 第二轮结论 |
|---|---|---|
| C1-C6 | ✅ | 范围、裸块分类、ROM 值、复用/NEW、命名与首轮一致；TSV hash 未变。 |
| C7 | ❌ | target 与引用 Symbol/source 合同已补齐，但 14 个 REF slot 的 Data pre/post 合同和可审计 fresh-readonly 取证门禁未闭合。 |
| C8-C11 | ✅ | 9 个 PLATE 全 ASCII，长度 `201/266/270/204/171/197/207/167/180`；184 EOL 不变；odd/even、16 preserve + 1 create 与首轮一致。 |
| C12 | ✅ | `0x1d9e` 与 `080a2c64` 两处语义错误均已精确订正；184 个 PC-relative consumer 合同未变。 |
| C13 | ✅ | TSV 仍为 184=`66/101/17`、动作 `138/14/32`；提案仍为 17 Function、1714 instructions/3594 B、189 words、47 padding、379 edges、R4=1、carve=0、§5.1=0。没有范围或动作漂移。 |

### 第二轮 R1-R9

| 规则 | 结果 | 第二轮结论 |
|---|---|---|
| R1-R2 | ✅ | 数值、复用、新定义和槽命名合同未变。 |
| R3 | ❌ | 14 个 REF slot 的 listing Data type/length/unchanged 未进入 pre/post/dry/persisted 合同。 |
| R4 | ✅ | 尾块 R4 与 Function create 未变。 |
| R5-R6 | ✅ | 两处首轮注释/消费者问题已修正。 |
| R7-R8 | ✅ | carve=0；唯一裸块仍由控制流判为代码。 |
| R9 | ❌ | 未来 landing 的 DB 门禁已补齐，但本次 C7 fresh 取证缺少可审计的命令与 DB hash manifest；formal source snapshot 也没有覆盖完整 source-scope/rollback baseline。 |

### 第二轮机械守卫

- proposal 与 TSV 中没有零容忍词。
- 9 个 PLATE 与 184 个 EOL 全 ASCII；最大 PLATE 270 B，最大 EOL 83 B。
- proposal 保持 `EQ=138/REF=14/RENAME=32`、`Function create=1`、`existing rename=0`、`PLATE=9`、`EOL=184`、`R4=1`、`carve=0`、`§5.1=0`、379 edges；没有进入 `080a38fc`。

## 第二轮状态: NEEDS_FIX

## 第二轮修改清单

### #1 — C7 / R3 — 冻结 14 个 REF slot 的 Data pre/post 状态

在 section 3.2 对 14 个槽增加 Data 合同：`080a29c8`、`080a2afc`、`080a2b78` 的 pre/post 必须均为 `/undefined4`, length=4；其余 11 个槽的 pre/post 必须均为 `/dword`, length=4。REF 安装和 slot Symbol 物化不得 retype、clear 或重建这些 Data。preflight、postcheck、apply receipt 和 fresh persisted check 均须逐槽比较 address/type/length；任何 Data 变化直接失败。

### #2 — C7 / R9 — 为 C7 fresh prestate 补可审计的 read-only/DB-hash manifest

新增并在 proposal artifact 表中冻结一个 gate manifest，至少记录：实际 headless 命令/参数或等价结构化字段、`-noanalysis`、`-readOnly`、退出码 0、取证脚本 SHA256、raw prestate JSON SHA256、查询前后 15 个 DB 文件的相对路径/大小/SHA256 完整 map 及 exact-equality 结论。proposal:25 的 15/15 不变陈述必须由该 manifest 直接支持；脚本自行写入的 `mode` 字符串不能代替进程与 DB 证据。

### #3 — R9 — 扩大 formal source snapshot 为完整 scope/rollback baseline

在任何正式导出或源码编辑前，按当前活动文件既有落地做法建立完整 baseline，至少覆盖全部 `asm/*.s`、`asm/includes.inc`、授权 constants、`tools/ghidra-labeling/RenameKnownFunctions.py`、`doc/dev/naming-proposals.csv`、四个 Function inventory 输出、活动/总进度文档以及计划中的 Seg-6 script/plan 路径；记录存在性、大小和 SHA256。source-scope 必须对该全集逐文件比较，只允许 proposal:196-202 明列的变化；失败恢复必须恢复所有已有文件并删除本次新增文件。不得用 Git 基线覆盖用户或前序段的既有工作树状态。

## Reviewer Verdict (Round 2): F13-Seg-6 = NEEDS_FIX(3 items)

---

## 第三轮最终 proposal 独立复审

### 复审输入与证据冻结

- 最新 proposal SHA256：`e8b6d3846956140b66a09876873622bb7bb6b1f2de332cd36ef1de3779ceaeab`，与 driver 给定值一致。
- slots TSV SHA256：`2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe`，与前两轮完全相同。
- fresh raw prestate SHA256：`e85ecaf4fd4ce0c82376c17e9af8a3aedc17330fb17e7cd9242ade0da589e12c`。
- fresh inspection script SHA256：`4f2aa5dbd8161f6be01de341da243242f478da614cfe4d05dcbdf0b03d185298`。
- fresh gate SHA256：`e149bb3a46ef62a2b4f77e4a68c22f5681beebe9703044408f62428bfcb4c4b7`。
- 本轮重新解析 raw、gate 与脚本，并独立重算当前 `.rep` 的完整文件 manifest；没有把 Mode A 报告或 proposal 自述当作结论。

### 第二轮 Fix #1-#3 闭合情况

| 第二轮项 | 结果 | 第三轮独立结论 |
|---|---|---|
| Fix #1：14 个 REF slot Data pre/post 合同 | ✅ 闭合 | raw 中 `080a29c8/080a2afc/080a2b78` 精确为 `/undefined4`，其余 11 个精确为 `/dword`，14/14 均为 length=4。proposal:83-104 已逐槽冻结地址、类型、长度、object span 和 bytes 不变，并明确要求 preflight、postcheck、receipt 与 fresh persisted check 逐槽比较；REF 不得 clear/retype/recreate Data。独立读取 ROM 后，14 个槽的 4-byte word 与 TSV 全部一致。 |
| Fix #2：可审计 fresh read-only/DB gate | ✅ 闭合 | gate 文件实际记录完整 executable、command line 与 arguments；参数明确含 `-noanalysis`、`-readOnly`，exit code=0，success marker 为 `F13_SEG6_REF_PRESTATE_OK targets=5 slots=14`。gate 引用的 inspection script/raw SHA256 与文件实算值一致。DB before/after 均含 15 个 relative-path/size/SHA256 完整条目，两个 map 精确相等；本轮又对当前 `.rep` 逐文件重算，文件数、路径、大小和 SHA256 仍与 gate 的 15 项完全相等。 |
| Fix #3：完整 source/scope baseline 与恢复 | ✅ 闭合 | proposal:205-213 已要求在正式导出/源码编辑前以当前工作树建立物理 baseline：覆盖 every present `asm/*.s`，显式核 25 个 `asm/NN_*.s`、`asm/rom.s`、`asm/includes.inc`、全部 `constants/*.inc`、Function registry、CSV、四份 inventory、活动/总进度文档、计划 script/plan 及 runner 可能写入的其他正式路径。每个路径冻结 existence/size/SHA256；rollback 对 prestate-present 文件逐字节恢复、对 prestate-absent 后新建文件删除，并明确不以 Git 作为恢复基线。 |

### 第三轮 C1-C13

| # | 检查 | 结果 | 第三轮结论 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | 范围仍为 `[080a27a0,080a38fc)`，没有进入下一 Function。 |
| C2 | Rule 2 裸块归宿 | ✅ | 唯一尾块仍按 R4 反汇编并创建 Function；carve=0，残余裸块=0。 |
| C3 | Rule 3 | ✅ | §5.1=0；`187a->38f8` 的真实 BL 入边与尾块代码裁定不变。 |
| C4 | R1 ROM 值 | ✅ | 再读 ROM 得 184/184 TSV word 精确相等；动作仍为 EQ=138、REF=14、RENAME=32。 |
| C5 | R1 复用/NEW | ✅ | REUSE=169、NEW=15，3 个新 constants 与 8 个 Thumb aliases 的 11 个唯一新定义未漂移。 |
| C6 | R2 名称 | ✅ | 184 个槽名的形式、唯一性和碰撞合同未变。 |
| C7 | R3 LABEL/DATA-ref | ✅ | 五个 target 与 14 个 slot 的 Symbol/Data/reference 双层合同完整；14 个 slot Data 精确为 `3 x /undefined4 + 11 x /dword`、全长 4，object span/bytes 保持。fresh gate 的真实进程参数与 DB 不变证据闭合。 |
| C8 | R5 现名 | ✅ | 九个最终 PLATE 不含旧自动名或过期 caller 名。 |
| C9 | ASCII | ✅ | 9 个 PLATE 与 184 个 EOL 仍为纯 ASCII；PLATE 均低于 500 B。 |
| C10 | Thumb odd/even | ✅ | 8 个新增 Thumb alias 及 switch even target 合同未变。 |
| C11 | Function/误名 | ✅ | 16 个既有 Function body 保持，尾部只创建 `080a38f8..080a38fc` 一个 Function；既有 Function rename=0。 |
| C12 | 消费者/语义 | ✅ | `0x1d9e` 的 r2-low8 初始化/case-4 递减证据和 `080a2c64` nonzero-reject PLATE 均保持正确。 |
| C13 | 完整覆盖 | ✅ | 184=`DAT66+DWORD101+PTR17`，17 Function、1714 instructions/3594 B、189 words、47 padding、379 edges、R4=1、carve=0、§5.1=0，均无范围或动作漂移。 |

### 第三轮 R1-R9

| 规则 | 结果 | 第三轮结论 |
|---|---|---|
| R1 | ✅ | 184 个 ROM word、138 个 EQ、复用与 NEW 合同不变。 |
| R2 | ✅ | 184 个自动槽全覆盖且名称合同不变。 |
| R3 | ✅ | target、slot Data 与 exact REF tuple 均有可执行 pre/post/fresh 合同。 |
| R4 | ✅ | 尾块 4 B 代码、控制流和 Function create 合同不变。 |
| R5 | ✅ | 九个 ASCII PLATE 使用现名且事实正确。 |
| R6 | ✅ | 关键消费者数据流与全部 PC-relative consumer 证据未漂移。 |
| R7 | ✅ | carve=0 合理。 |
| R8 | ✅ | 本段没有图形候选；尾块由机器码和控制流归类。 |
| R9 | ✅ | 新 `.rep`、15/15 hash、真实 fresh `-noanalysis -readOnly`、完整 source baseline、present/absent 恢复、全流水线失败闭环和 byte-identical 门禁均已写成 fail-closed 合同。 |

### 第三轮机械守卫

- TSV 仍为 184 行，动作精确 `EQ=138/REF=14/RENAME=32`；proposal 仍为 Function create=1、existing Function rename=0、PLATE=9、EOL=184、R4=1、carve=0、§5.1=0。
- 184 个槽的 ROM little-endian word 再核为 184/184 相等；14 个 REF 地址集合与 raw/TSV 完全一致。
- proposal 的 PLATE/EOL payload 未出现非 ASCII 字符，也未出现零容忍词。
- 本轮没有发现新的范围、动作、Function、Data、引用或注释语义漂移。

## 第三轮状态: PASS

proposal 可以进入物化及 Mode B 前实现复核。此结论只批准按已冻结合同生成并审查 materialized script/plan；real apply 仍须在脚本逐字段实现复核、最终 dry 与 root 门禁全部通过后才能放行。

## Reviewer Verdict (Round 3): F13-Seg-6 = PASS

---

## Pre-real-apply implementation review

本小节只审查最终 `PASS` proposal 的 plan、物化脚本与写前证据；不改变前文 C1-C13 的
`PASS`。审查中没有运行 `apply`、事务 probe、export 或 build，没有修改 Ghidra、proposal、TSV、
plan、脚本或正式源码，也没有 stage/commit。

### 冻结输入与物化一致性

独立重算的关键 SHA256 为：

- proposal：`e8b6d3846956140b66a09876873622bb7bb6b1f2de332cd36ef1de3779ceaeab`；
- 本实现审查前 review：`a4fbb19e5d4f441f388417b0735b2809f607c2031ce4b190a15bc75212dc9bd5`；
- TSV：`2070db7653e739f32396fa55c7ca49c70575edb857f3523fb0e55416f983d1fe`；
- plan：`267768c6347e6ce13e806c77b2ff36919edfcc2352e28793bd6e640cc89747a8`；
- `RefineF13Seg6.py`：`2a6eb438dfcb5f3ae9c36d472ff0f0e1780cf447bcc4a182346bb5c99d39bff1`；
- final dry-only gate：`15c6f05a6dc68c3b389758afd99944a5978f8e0bb89d71631731e903fbe22d0f`。

plan 的 184 个 action 与 TSV 按地址、旧名、kind、ROM value、action、target、slot label、reuse、
consumer、evidence 和 EOL 逐字段一致；独立重读 ROM 得 184/184 word 相等。计数精确为
`EQ=138/REF=14/RENAME=32`、`REUSE=169/NEW=15`。3 个新 constants 与 8 个 Thumb aliases 均与
proposal 原文一致，alias 值全为批准 Function entry+1。

对 plan 的 97 个 post-code ranges、189 个四字节 words 和 47 个二字节 padding ranges 重新做地址
分区，得到 `3594+756+94=4444` B，精确覆盖 `[080a27a0,080a38fc)`，无洞、无重叠。独立从 ROM
半字重新解码得到 379 条边，精确为 `Bcc=186/B=109/BL=84`，并与 plan 的
`source/op/target/rom_bytes` 379/379 相等。

### Symbol、Data、Function 与注释实现

- `normalize_targets()` 在所有 slot/listing 动作前调用。四个既有 RAM target 保持原 Symbol ID；
  `080a2b00` 要求同址唯一 primary ID=5854，并以 `setNameAndNamespace` 把同一对象规范为 Global
  USER_DEFINED `equip_target_selection_phase_jump_table`。postcheck 再核 ID、Global、source、primary
  和同址 Symbol count=1。
- 14 个 REF 的 plan Data 精确为 3 个 `/undefined4` 加 11 个 `/dword`，全为 length=4；与 full
  prestate 的 address/min/max/type/length 和 ROM bytes 逐项一致。`apply_slot()` 的 REF 分支没有
  `clearCodeUnits`、`createData`、`removeData` 或 retype；加引用前后均比较同一 Data 合同。postcheck
  要求唯一 operand-0 `DATA/USER_DEFINED/primary=true` tuple、唯一 Global USER slot label、Data 与字节
  不变。32 个 RENAME 保留完整 pre-reference 集合，138 个 EQ 要求 name/value/operand-0 reference。
- 尾块仅清 `[080a38f8,080a38fc)`，设置 Thumb mode，连续反汇编两条/4 B 后创建精确 body；返回类型
  `uint`、参数数为 0。postcheck 核 `movs r0,#1; bx lr`、唯一 `187a->38f8` incoming、Function name/
  source/body/signature。16 个既有 Function 的 ID、name、body、calling convention、return、parameters、
  incoming 与相应 PLATE 均有 preserve check。
- 8 个旧 PLATE 加 1 个尾 PLATE、184 个 EOL 全由冻结 plan 驱动；脚本和 payload 均为 ASCII，PLATE
  均小于 500 B。postcheck 同时拒绝段内任何残余 `DAT_/DWORD_/PTR_/UNK_/FUN_/SUB_` 自动名。

### dry、backup、scope 与模式隔离

- 物理 backup evidence 指向
  `Yu-Gi-Oh WCT 2006.rep.bak-20260906-093710-pre-F13Seg6`。本轮独立重枚举当前 `.rep`、backup 与
  evidence，三者均为 15 个文件，relative path/size/SHA256 15/15 完全相等。
- source baseline 含 63 个路径和 63 份已核物理副本：25 个 `asm/NN_*.s`，当前全部 30 个
  `asm/*.s`、`asm/includes.inc`、全部 constants、registry、CSV、四份 inventory、活动/总进度及
  Seg-6 script/plan。当前文件与 snapshot 的 existence/size/SHA256 63/63 仍相等；rollback contract
  明确 present 恢复、absent 删除，不使用 Git baseline。
- final dry 实际命令含 `-noanalysis -readOnly ... RefineF13Seg6.py dry`，exit=0、success marker 命中、
  `semantic_actions_applied=false`，DB before/after 15/15 精确相等。当前不存在 apply receipt 或
  persisted-check。三次保存的 dry-failure restore evidence 也分别为 15 files、0 mismatch。
- 脚本仅 `apply` 分支进入 transaction；preflight 在 transaction 前，action 与 postcheck 在单一
  transaction 内，异常时 `commit=False` 并由 `finally` rollback。`dry` 只验证并写外部 dry JSON；
  `check` 只读取 receipt 和持久态，不调用 Ghidra 写动作。

### 实质失败：fresh check 的瞬时计数必然与 receipt 不同

`RefineF13Seg6.py:52` 在每个新进程把 `COUNTS` 七项全部初始化为 0。apply 进程执行动作后，
`:637-645` 把 `EQ=138/REF=14/RENAME=32/EOL=184/PLATE=9/R4=1/FUNC_CREATE=1` 同时写入 receipt
顶层和 `receipt.after`。但是 fresh `check` 分支 `:617-624` 不执行动作、也不重建 `COUNTS`，直接把
`:590-598` 的 `capture()`（其中含全零 `counts`）与 `receipt['after']` 做 `PERSISTED_EXACT`。

因此即使所有 Ghidra 持久状态完全正确，fresh check 仍会在唯一这个进程内计数字段上确定失败；当前
脚本不能完成 proposal:212、234 要求的 persisted fresh-readonly 门禁。这是实现错误，不是证据缺失。

### transaction commit 前 receipt 的失败语义

`:642-647` 在 `endTransaction(..., True)` 前写 `f13-seg6-apply-receipt.json`，成功 marker 则在
`:652`、transaction end 之后才打印；Ghidra project save 由 headless 进程退出阶段完成。因此该 receipt
只能是 transaction-postcheck 的 provisional evidence，不能单独代表 commit、save 或 landing 成功。

这一顺序可由外层闭环安全兜底，但放行时必须同时满足：启动前删除或拒绝旧 receipt；apply 进程
exit=0 且 transaction-success marker 命中；随后 fresh `-noanalysis -readOnly check` 成功且查询前后
DB 15/15 不变。transaction end、save、marker、fresh check 或后续任一门禁失败时，外层必须忽略并
删除 provisional receipt，从新 backup 物理恢复 DB、恢复 source baseline、删除 absent 后新建路径，
再跑 fresh prestate。当前 proposal 已规定这条恢复路径；修复下述 fresh-check 缺陷并按此执行后，
receipt 的提前写入不构成额外 Ghidra 动作漂移。

## Implementation 状态: NEEDS_FIX

### #1 — persisted check — 把动作计数与持久 DB capture 分离

精确修改 `tools/ghidra-labeling/RefineF13Seg6.py`：

1. 定义一个唯一 `EXPECTED_APPLY_COUNTS`，内容精确为
   `EQ=138, REF=14, RENAME=32, EOL=184, PLATE=9, R4=1, FUNC_CREATE=1`；apply postcheck 与 fresh
   check 共用，不得复制成可漂移的两份常量。
2. 从 `capture()` 中移除进程内瞬时字段 `counts`；receipt 顶层继续保留动作计数。apply 的
   `receipt['after']` 与 fresh `capture()` 只比较真正可持久化的 segment hash、Function count、slots、
   targets 与 Functions。
3. 在 `check` 分支读取 receipt 后，先精确核
   `status=F13_SEG6_APPLIED_POSTCHECK_OK`、`FAIL=0`、当前 script SHA、当前 plan SHA，以及
   `receipt['counts']==EXPECTED_APPLY_COUNTS`，再执行 `verify_post()` 与无瞬时计数的
   `PERSISTED_EXACT`。不得用把 fresh `COUNTS` 人工填成 receipt 值来掩盖合同错误。
4. 保持 `dry`/`apply`/`check` 的 Ghidra 行为、184 个 action、5 target、14 Data、tail、Function、PLATE、
   EOL 和 edge 实现完全不变；不得借此扩大范围或加入 probe/apply。

### 修后唯一最终放行顺序

追加本实现 review 后，旧 review hash 已改变，所以现有 plan、脚本、source baseline、dry gate 与
`15c6f05a...` final gate 都只能作为本轮输入证据，不能直接用于 real apply。fixer 应按以下顺序闭环：

1. 冻结本 review 的新 SHA256；仅应用上述 persisted-check 窄修，并把新 review hash 写入 plan/input
   contract。
2. 依次重算 plan SHA 与 script SHA；重新生成覆盖最终 plan/script 的完整 source baseline，并重算其
   hash。proposal、TSV、refscan、edges、functions、layout 和语义动作必须保持原 hash/计数。
3. 重新运行 final fresh `-noanalysis -readOnly dry`，要求 `FAIL=0`、15/15 DB before/after exact、当前
   DB=backup、source baseline 0 mismatch；生成新的 final preapply gate。
4. 此后只允许 root 做不写文档的独立 hash、静态 scope 和门禁核验；禁止再次 append review 或修改
   已冻结输入，避免 review-hash 循环。root 明确放行后才可运行 real apply。
5. real apply 外层严格执行上一节的 provisional-receipt/marker/restore 规则，并在 apply exit=0 后先跑
   修正后的 fresh persisted check，再进入 export、constants/aliases、split、inventory、build、
   byte-identical、scope 与 progress 顺序。任何失败不得 stage/commit，也不得记录成功态。

## Implementation Reviewer Verdict: F13-Seg-6 = NEEDS_FIX(1 item)

---

## Real-apply failure narrow-fix implementation review

本小节是最后一次写入 review，只审查首次 real-apply 失败、恢复链和其后的两项窄修；不改变前文
C1-C13 `PASS`。本轮没有运行 apply、probe、build 或 export，没有修改 Ghidra、proposal、TSV、plan、
脚本或正式源码，也没有 stage/commit。

### 首次 apply 失败的独立归因

- 失败时冻结的 plan/script SHA256 分别为
  `a6cc2608f4ecb7cbe351e089010fe2c56b1dec5e6106d9877e25e24ce3e451a5` 和
  `69ab729cedda0d8ef063a8667decc9c54c91c6717e96c0bbfcee9fb788726092`。
- `f13-seg6-apply-headless.log` 明确记录完整 preflight 为
  `slots=184 EQ=138 REF=14 RENAME=32 ... FAIL=0`。transaction 内 postcheck 的失败精确为六项：五个
  `TARGET_DATA_POST` 和一个 `TAIL_INSTRUCTIONS_POST`；其余动作、Function、范围、边和注释检查没有
  产生失败。
- 五个 target 的实际 Data 均含 `address/min/max/type/length`，旧 plan expected 只含
  `address/type/length`，所以是同一 Data 对象的字典形状不等，不是 retype、clear、长度或地址改变。
  tail 的实际第一条 Ghidra listing 是 `mov r0,#0x1`，旧脚本脆弱地要求文本
  `movs r0,#0x1`；ROM halfword `0x2001` 的 Thumb 编码语义仍是 MOVS-immediate。
- apply failure JSON 精确为上述六项，phase=`APPLY_POSTCHECK`。虽然 headless 返回 exit code 0 且在
  rollback 后写出一个新 DB generation，外层因 transaction-success marker 缺失而判定 FAIL；没有
  apply receipt，也没有 persisted marker。该事实再次证明不能只信 headless exit code。

### 失败恢复与 fresh prestate

- `f13-seg6-restore-gate.json` 为 `F13_SEG6_PHYSICAL_RESTORE_PASS`：DB 15 files、与物理 backup
  path/size/SHA256 精确相等，source baseline mismatch=0。
- 恢复后重新生成的 full prestate SHA256 仍为
  `4237671c74c2204f046107dcc0aea069d4d0ecd7d3c29adc2eb42b161ba5e0e5`；对应 gate 使用 fresh
  `-noanalysis -readOnly`，exit=0、success marker 命中，DB before/after 15/15 完全相等，Function
  count 恢复为 5212。
- 本轮又独立枚举当前 `.rep` 与
  `Yu-Gi-Oh WCT 2006.rep.bak-20260906-093710-pre-F13Seg6`，两者及 backup manifest 仍为 15/15
  relative-path/size/SHA256 完全相等。当前不存在 apply receipt 或 persisted-check。

### tail rollback probe 的独立复核

`ProbeF13Seg6Tail.py` 只有一个 transaction；只 clear/disassemble `[080a38f8,080a38fc)`，不调用
Function create、不调用任何 slot action，并在 `finally` 无条件执行
`endTransaction(transaction, False)`。probe raw 在 rollback 前记录的两条指令精确为：

| address | bytes | TMode | length | mnemonic | operands | flow/fallthrough | to_string |
|---|---|---:|---:|---|---|---|---|
| `080a38f8` | `0120` | 1 | 2 | `mov` | `r0`, `#0x1` | `FALL_THROUGH`, next=`080a38fa`, flows=[] | `mov r0,#0x1` |
| `080a38fa` | `7047` | 1 | 2 | `bx` | `lr` | `TERMINATOR`, next=null, flows=[] | `bx lr` |

probe 同时记录总字节 `01207047`、Function created=false、semantic slot actions=false、rollback
pending=true。process gate 的 exit=0、rollback marker 和 raw SHA 均正确；headless 退出仍产生 DB generation
变化，随后物理 restore。组合 restore gate 明确为
`F13_SEG6_TAIL_PROBE_AND_RESTORE_PASS`、restored DB=15、exact=true。本轮重算 probe raw SHA256 为
`4eef1354130a8eeeeb405c5542d5c18623bb10097a98fa6d8f65d3235a865d85`，restore gate SHA256 为
`aa13465e8a676bd1c28c55de58344b9eda7ad37c54d59ae12b3fba64e6c8786e`。

### 当前 plan/script 的窄修与无漂移证明

- 当前 plan SHA256 为
  `84885fe890303b7fcc86716c906d2e32b52155fc67f9af45c6b3f5718a8929f0`；当前 script SHA256 为
  `a88e8084f712c99a12c1f83cb4fb7b1768c51783dd5d015b62f37756cc10eec6`。
- 五个 target 的 plan pre Data 现在全部含精确 `address=min`、`max=address+3`、`length=4` 和原
  `type`；`verify_post()` 用 `actual['data']` 与该完整字典做 exact comparison。因此 RAM 四项仍为
  `/undefined4`，`080a2b00` 仍为 `/pointer`，不会把缺字段误报为 Data 变化。
- plan 的 `tail.instruction_contract` 与上表 probe raw 逐字段完全相等。新增
  `tail_instruction_row()` 采集 address/address_text、bytes、TMode、length、mnemonic、operands、
  flow type、flows、fallthrough 和 to_string，postcheck 全字段 exact comparison。另冻结
  `encoding_semantics=['movs_r0_imm8_1','bx_lr']` 与总字节 `01207047`；语义由编码合同固定，不再依赖
  错误的 `movs` renderer 文本。
- 对失败时 source snapshot 与当前文件做 AST/结构差分：脚本共同函数中仅
  `verify_frozen_plan`、`verify_post` 改变，只新增 `tail_instruction_row`；plan 只新增 probe/restore
  hashes、五个 target Data 的 min/max 和 tail instruction/encoding contract。normalize、slot、REF、
  Function create、PLATE、transaction、capture 及三模式分支均未改变。
- 上一节修复的 persisted-count 合同保持：唯一 `EXPECTED_APPLY_COUNTS`、`capture()` 不再含瞬时
  COUNTS，fresh check 明确核 receipt status/FAIL/script/plan/counts 后才比较持久 capture。
- 当前 script/plan 的 `INPUT_HASHES` 已包含 tail probe raw 与组合 restore gate；组合 gate 内嵌 process
  参数、marker、raw SHA、DB before/after 和物理恢复结果。审查写入前，所有冻结 input hash 均与实际
  文件相等。

机械复核仍为 184 actions=`138 EQ + 14 REF + 32 RENAME`、5 targets、14 REF Data、3 constants、
8 aliases、16 Function preserve+1 tail create、9 PLATE、184 EOL、379 edges；97 code ranges/3594 B、
189 words/756 B、47 padding/94 B 精确覆盖 4444 B。proposal/TSV/refscan/edges/functions/layout hash 未变，
没有范围、Function 语义、Data、注释或正式 source 动作漂移。旧 source baseline 与当前比较只有
plan/script 两个预期窄修路径不同，其余 61/61 相等。

## Narrow-fix implementation 状态: IMPLEMENTATION_FIX_PASS

两项实际失败断言均按观测合同闭合，且窄修没有改变批准动作。现有恢复状态安全；可以进入最后一次
重冻结与 dry/root 门禁，但本结论本身不授权直接复用旧 gate 或运行 real apply。

### 唯一最终放行顺序

1. 以本小节追加后的 review 新 SHA256 为最终 review hash，只更新该 hash 并重算 plan/script；不得
   改 proposal、TSV、refscan、edges、functions、layout、动作或语义。
2. 重新建立覆盖最终 review 所对应 plan/script 的 63-path source baseline，要求当前/快照全部相等；
   重新核当前 DB 与 backup 15/15 exact。
3. 重跑 final fresh `-noanalysis -readOnly dry`，要求 preflight/final FAIL=0、DB before/after 15/15 exact、
   source mismatch=0，并生成新的 final preapply gate。
4. 从此禁止再改 review。root 只做不写文档的独立 hash、静态 scope、marker、backup/baseline 和 dry
   gate 验收；验收后才可明确放行 real apply，避免 review hash 再次形成循环。
5. real apply 仍必须以 marker 而非单独 exit code/receipt 判 transaction 成功；随后先跑 fresh persisted
   check，再进入 export、constants/aliases、split、inventory、build、byte-identical、scope、progress
   顺序。任一步失败立即物理恢复 DB、恢复 source baseline、删除本轮新增路径并回到 fresh prestate；
   禁止 stage/commit 或记录成功态。

## Narrow-fix Implementation Reviewer Verdict: F13-Seg-6 = IMPLEMENTATION_FIX_PASS

---

## Apply wrapper order-fix implementation review

本节是经 root 明确授权的最后一个 wrapper 审查章节；只审查 retry-2 的顺序误判修复及外层门禁，
不改变前文 C1-C13 `PASS` 和 Ghidra 语义实现结论。本轮没有执行 apply、Ghidra、build 或 export，
没有修改 wrapper、plan、script、proposal、TSV 或正式源码。

### 输入与 retry-2 证据

- 当前 `run_f13_seg6_apply_gate.ps1` SHA256 为
  `4b0c5d02002a0acdee5714375730d85630607c3303275db5009f68a09396f04e`；PowerShell AST 独立解析为
  0 error，且只有一个 `Test-ReceiptCountsExact` 定义。
- retry-2 apply log SHA256 为
  `90e37f0867af0c32582fa45f9a95d4260ef129cc032b55ae69950e901e7c48a3`：preflight 和 postcheck
  均为 `FAIL=0`，动作计数保持 `184=138 EQ+14 REF+32 RENAME`，并打印唯一 transaction committed
  marker。旧 apply gate SHA256
  `cf4d57709198a0c5d384ebb18d9bdca52d7a49cb92e6a371885004eabfec982f` 同时记录 exit=0、marker=true、
  receipt present、receipt status 正确、receipt FAIL=0、DB changed=true，唯一失败项为旧的
  `receipt_counts_exact=false`。这与 PSCustomObject 属性顺序被错误当成合同的根因一致。
- restore gate SHA256 为
  `8bc041c73320a1ca67a48fc8476d50ba56d03642b7c3b18cf1bfd81a312487af`，状态为
  `F13_SEG6_PHYSICAL_RESTORE_PASS`，DB 15 files exact、source mismatch=0；当前不存在 apply receipt。
  因此 retry-2 未留下可继续使用的 Ghidra 落地状态。

### 键集合、顺序和外层 PASS 合同

对 wrapper 中 AST 提取出的原始函数体独立运行纯 PowerShell 合成测试，未 dot-source 或执行 apply
主体。结果如下：

| case | 期望 | 实际 | 结论 |
|---|---:|---:|---|
| 精确 7 键、标准顺序 | true | true | 通过 |
| 精确 7 键、完全乱序 | true | true | 通过 |
| 多 1 键 | false | false | 通过 |
| 少 1 键 | false | false | 通过 |
| `EQ=139` | false | false | 通过 |
| 键名大小写错误 | false | false | 通过 |
| counts=null | false | false | 通过 |

`run_f13_seg6_apply_gate.ps1:38-45` 先按属性名构建集合、要求数量相等，再以大小写敏感方式确认每个
expected key 恰有一个属性，所以键顺序不参与判断，extra/missing/错名均被拒绝。

其余语义门禁没有放宽：`:52-58` 先核 proposal/review/TSV/plan/script/baseline frozen hash；`:65-84`
要求 current/backup DB 15/15 exact 且 source baseline 无 mismatch；`:92-105` 合取 transaction marker、
receipt presence、status、FAIL、script SHA、plan SHA 和 counts；`:106-110` 另要求 DB changed，且最终 PASS
还要求 prechecks exact 和 process exit=0。`:130-131` 对任何非精确 PASS 状态执行 `throw`，因此仍会交给
上层物理 restore；上述 restore gate 已证明该恢复链在 retry-2 实际执行成功。

### 实质失败：值比较不是精确整数合同

`run_f13_seg6_apply_gate.ps1:46` 对任意属性值直接执行 `[int64]` 强制转换，再于 `:47` 比较。独立负测
得到以下错误接受结果：

| 非法 JSON 值 | expected | 当前结果 |
|---|---:|---:|
| `EQ="138"`（String） | 138 | true |
| `R4=1.1`（Double） | 1 | true |
| `R4=true`（Boolean） | 1 | true |

PowerShell 会分别解析普通 JSON 整数 `138` 为 `System.Int64`、`1.1` 为 `System.Double`、`true` 为
`System.Boolean`；直接转换会把后两者变成 1，并接受可解析的数字字符串。这违反本轮要求的 int64
精确值和 wrong-value rejection。属性集合修复本身正确，但当前函数仍允许畸形 receipt 绕过 counts
值合同，不能放行 real apply。

## Wrapper 状态: NEEDS_FIX

### #1 — receipt counts — 拒绝非整数 CLR 类型后再做精确值比较

精确修改 `run_f13_seg6_apply_gate.ps1:46-47`：

1. 对 `$property[0].Value` 先做类型白名单，只接受 CLR 整数类型
   `SByte/Byte/Int16/UInt16/Int32/UInt32/Int64/UInt64`；明确拒绝 Boolean、String、Single、Double、Decimal
   和 null。`UInt64` 超出 Int64 范围时须由 checked conversion/catch 返回 false。
2. 类型通过后再转换为 `[int64]`，与 `[int64]$Expected[$name]` 精确比较；不得使用数值舍入、字符串
   parse 或 truthy conversion。expected 属性集合仍必须精确为
   `EQ/REF/RENAME/EOL/PLATE/R4/FUNC_CREATE` 七键，键名大小写敏感且顺序无关。
3. 重跑相同纯函数测试；除既有 exact/乱序/extra/missing/wrong/错名/null 用例外，必须确认数字字符串、
   fractional number 和 Boolean 三类均返回 false。不得修改 precheck、marker、receipt status/FAIL、
   script/plan hash、DB changed、最终 PASS 合取或失败 `throw`。

### 修后冻结与唯一放行顺序

1. 本节写入后 review SHA 改变。fixer 只应用上述 validator 窄修，并把本 review 的最终 SHA 写入
   plan/script/wrapper 冻结合同，随后按依赖顺序重算 plan、script 和完整 source baseline。
2. plan 当前 `INPUT_HASHES` 不含 apply wrapper；因此最终 wrapper SHA 必须由 root/landing 外层 gate
   单独冻结并核验，不能通过修改 Ghidra 语义、扩大 proposal scope 或新增 action 来补偿。
3. 重跑 final fresh `-noanalysis -readOnly dry`，要求 frozen/source prechecks、FAIL=0、当前 DB=backup
   15/15 exact、dry 前后 DB exact；此后本 review 永久冻结，不再追加章节。
4. root 只做不写文档的 wrapper hash、AST、上述合成测试与全门禁合取核验。全部通过后才可授权 real
   apply；任一失败仍须 throw、物理恢复 DB/source、fresh prestate，禁止继续 landing 或记录成功态。

## Wrapper Reviewer Verdict: F13-Seg-6 = NEEDS_FIX(1 item)
