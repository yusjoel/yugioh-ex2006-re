# 函数和数据细化计划 · `asm/16_duelfield_zone.s`

> 范围 `[0x080c1448,0x080cbf0c)`，共 43716 字节。主序已完成 16/25 个模块，历史正引用补漏 1 项。当前模块完成 6/10 段，下一任务为 F16-Seg-7 `[0x080c7af8,0x080c8bf0)`；按最新指令逐段验收、单独提交并持续推进。

## 一、规则

按 `doc/dev/methodology/refine-loop.md` 严格地址序执行。函数间数据有有效引用时须 carve 或反汇编；全 ROM raw 与 THUMB+1 引用均为 0 后才登记 §5.1。新 Ghidra PLATE/EOL 一律 ASCII，PLATE 最多 500 字符。每段先读消费者和既有常量，再冻结方案并独立复核。

## 二、验收流程

源码和数据库备份后，依次执行分析、独立复核、真实只读全后态和同 Program 强制回滚核验。持久保存须单次门禁，保存后由新进程及独立采集器核验。随后重导汇编、同步常量与命名清单、完成资产导出和构建，并逐字节比较整个 ROM，最终验收通过后更新路线表。按 2026-11-12 用户指令，每段最终验收通过后单独提交。按 2026-11-13 最新续接指令，从 Seg-6 恢复，提交后依地址序持续推进。

## 三、当前进度

Seg-1 至 Seg-6 均已完成独立复核、实际落地、保存后核验和整ROM逐字节验证。当前完成6/10段，112个Function、1747个池字；剩余549个自动数据名（DAT422、DWORD57、PTR70）。初始测绘材料保留于§4.00。下一段为Seg-7。

Seg-4、Seg-5 的 7 个正引用原始块共 3352 字节已结构化；仅剩 Seg-7 的 1 个原始块共 58 字节未分类。当前 §5.1 登记为 0；剩余块由其所属段扫描并读取消费者后决定处理方式。

## 四、工作记录

### 4.00 建档与独立测绘（2026-11-06）

模块 15 的 10 段已全部验收，最终门禁 `6d20d4d9833cc7d6bf8f3eb9eaef9f371a62ecca9655fc3d43e10c9557421877`，文档关闭门禁 `fb507f70eff28120066f7b37fe612535d9eeef79a8a868f76d3da3eaf0868564`。ROM 33554432 字节逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

地址地图 `output/refine-run-20261028-105948/f16-module-initial-map-v2.json` SHA256 `ee5f3ba8930c4011580070162d9cc9e12f67a4f27c353a01c6e1e16562f6dc95`。独立 8G 只读快照 `root-f16-independent-map-prestate.json` SHA256 `26126121307bb2c813cd8c00e6e1c3b3a1e564fb87b6c954510c614a6a4124ba`，覆盖全部 43716 字节、112 个段内 Function 加前后两个保护 Function、1580 个 word、1614 个明确地址状态和 505 个 raw-word 目标；全局 Equate 2476 个、绑定 12643 条。物理数据库 15 个文件前后哈希相等。

Root 逐字节核对 ROM 与采集的 code unit，并逐项核对全部 112 个 Function 的 body ranges：10 段连续无缝、无重叠，全部现有 Function 均完整落在其所属段内；原始块未被段界切开。边界沿用实际 Function 入口，前一 Function 的尾指令、字面量池和填充均留在前段。

### 4.01 Seg-1（2026-11-12）

范围 `[0x080c1448,0x080c2544)`，共 4348 字节、7 个既有 Function 和 210 个池字。完成 43 EQ_ADD、58 REF_ADD、54 REF_PRESERVE、55 PRESERVE，155 个源标签及 EOL、19 个新目标、5 个函数改名和 7 个 PLATE。两个 pack-banner Function 的既有 PLATE 保留。段内 raw、carve、disasm 和新增 §5.1 均为 0。

实际 prestate、dry 和 owned fullrollback 依次通过，覆盖 117 个 Function、2181 个地址状态、1580 个模块池字、43716 个模块单位及 48 个外部保护单位。owned transaction 1242 的完整后态为 0 FAIL，end(False) 后同 Program 的完整前态恢复也为 0 FAIL。独立最终 Phase1 审查通过后执行唯一保存，新进程 check 与两份独立保存后门禁均通过。16172 个指令位置的保护属性精确保持，只投影 1042 个批准的 owner 名字段；全局 Equate 为 2479 个，绑定为 12686 条。

独立 fresh 桥接最初发现 49 个全局 Equate 的引用顺序差异。逐项核对确认成员、值、类型和重复数量一致，组件 r3 仅将这些引用按严格多重集比较，29 个正反例及真实完整 fresh 回归通过。旧 raw、auth、manifest、日志和物理门禁保留在不可变归档中，原实际 prestate 经精确来源链复用。Script、动作和后态计划保持原字节。

全范围原生汇编重导、mode 注入和模块拆分通过。189 个 native 表达式与 115 个有效 pins 的 210 项表达式断言通过，GNU 新定义 22 项。7 个既有 registry tuple 与 5 个 CSV name cell 精确同步。源码仅改变 15 项许可范围内的 13 个路径，其他模块及 `asm/rom.s` 的内容精确保持。49/49 资产导出和正常构建通过，33554432 字节 ROM 与原件逐字节相等，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

证据目录 `output/refine-run-20261028-105948/`。

| 核验 | 文件 | SHA256 |
|---|---|---|
| 实际 Phase1 独审 | `f16-seg1-phase1-static-review-v3.json` | `32ebbabc77d5138a487b42d4c1154a2b1d6e64e301a76b52aaec48f9d3819878` |
| 实际保存 | `f16-seg1-apply-v3.json` | `01b72edd3e705a2b45ce2a3489ee6226fc3de61c7360ff13a560a99217e6a7ae` |
| 独立数据库后态 | `root-f16-seg1-independent-saved-db-gate-v3.json` | `aa87ef17dc571bb14171c1873f587f1f6c89810aeb7327c3df43cb1ec697cd00` |
| 指令保护属性 | `root-f16-seg1-saved-instruction-properties-gate-v3.json` | `54297908e09519d144e05982cf9e31b986552438acd413cbb4b4bff956727576` |
| 源码与 ROM | `f16-seg1-source-landing-final-v1.json` | `cce5422c21da99ec5073cfd6ba4a95e3075faac1533fd623c4460d8539fdfa61` |

Root 最终收束留痕为 `root-f16-seg1-final-gates-v3.json`。下一任务为 F16-Seg-2 `[0x080c2544,0x080c36a8)`。

### 4.02 Seg-2（2026-11-13）

范围 `[0x080c2544,0x080c36a8)`，共 4452 字节、15 个既有 Function 和 145 个池字。完成 39 EQ_ADD、57 REF_ADD、22 REF_PRESERVE、27 PRESERVE，118 个源标签及 EOL、12 个新目标、8 个函数改名和 16 个 PLATE（段内 14、必要上下文 2）；另保留 1 个段内 PLATE。段内 raw、carve、disasm 和新增 §5.1 均为 0。

初版真实 owned 演练的 POST 在两个 Function 报 2 项差异，定位为 4 条既有 ANALYSIS 引用的 DEFAULT offcut 显示名：基址 `0x093264c0` 标记为 `card_mini_frame_second_half_tile_data` 后，`0x093264c2` 显示名从 `DWORD_093264c0+2` 派生为 `card_mini_frame_second_half_tile_data+2`。该轮强制回滚且物理 DB15/source202 不变，但未形成完整回滚恢复 PASS，旧证据独立归档。全项目 378 地址读取确认只有这 4 条 offcut 引用；相邻 `0x093264c4` 为独立 dword，保留其 2 条引用。R5 只修 3 个模型产物的 8 处 after 名称副本，所有 before 保持，另 27 条 DEFAULT `+` 引用保持；不增加写入动作。

R5 原生辅助读取完整保护 c2 的 4 字节、虚拟 ID、DEFAULT/Label、namespace/dynamic 和全部引用身份，并保留 c4 的完整数据边界及来源 Function。真实 prestate、dry 和 owned fullrollback 依次通过：119 个 Function、3097 个核心状态、1580 个模块池字、43716 个模块单位、48 个外部保护单位及 16452 个指令位置。transaction 1242 的完整 post 和 end(False) 后同 Program 核心与辅助前态恢复均为 0 FAIL，三模式物理 DB15/source202 前后逐字节一致。

独立最终审查通过后唯一保存一次，新进程 check 和独立原生采集全部通过。130 个新 USER 标签、8 个函数改名及 138 个 primary 节点精确核对；全局 Equate 2487 个、绑定 12725 条。16452 个指令位置仅投影 1086 个批准 owner 名字段，控制流类型及 override 精确保持。c2 的 4 条派生引用与 c4 独立边界后验通过。

全范围原生重导、mode 注入和模块拆分通过；137 个 native 表达式、8 个新增 fallback、123 个有效 pins（115 继承加 8 新增）及 145 个表达式断言通过。20 个 GNU 定义、16 个既有 registry tuple 和 8 个 CSV name cell 精确同步。源码仅在 15 项许可范围内改变 13 个路径。49/49 资产导出、构建和 33554432 字节整 ROM 逐字节比较通过，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，ELF SHA256 `b1a8cbb9cf2dd7ef2e791998771858bf0289238aca064c4b51332e2628023964`。剩余自动名 863；8 个原始块 3410 字节继续由其所属段处理。

证据目录 `output/refine-run-20261028-105948/`。

| 核验 | 文件 | SHA256 |
|---|---|---|
| 实际 Phase1 独审 | `f16-seg2-phase1-static-review-v1.json` | `0d18ac3059f1f25b367e2517d498729c231dc3fc2a781beb2bd676474a09115b` |
| 唯一保存 | `f16-seg2-apply-v1.json` | `60cdea828622405d0fdbfbdd82e0b96b0e85fe822079ab62ae23b51610d26c6f` |
| 新进程 check | `f16-seg2-persisted-check-v1.json` | `7ece3c3c4807a2cf7fe88d76354330afb01e8cc4bf9169e3f27f1a93d8bd725b` |
| 独立数据库与辅助后态 | `root-f16-seg2-saved-db-gate-v3.json` | `de1563b3b4a554b44a1d6a6339193503d31507b697fdfad5277bae8cadac2967` |
| 指令保护属性 | `root-f16-seg2-saved-properties-gate-v3.json` | `37555c0a596e75ca262940b9a3cde1b1301007bd6c9fba0d44d237e143ff6b99` |
| 源码与整 ROM | `f16-seg2-source-landing-final-v1.json` | `7c8a2c9612f3712778e34825bc50f83b561285ff27aad6ceb3268b9dd63df8ad` |

下一任务为 F16-Seg-3 `[0x080c36a8,0x080c4350)`，12 个 Function、98 个池字、76 个自动名、无 raw 块。

### 4.03 Seg-3（2026-11-13）

范围 `[0x080c36a8,0x080c4350)`，共 3240 字节、12 个既有 Function 和 98 个池字。完成 14 EQ_ADD、45 REF_ADD、17 REF_PRESERVE、22 PRESERVE，76 个源标签及槽 EOL、12 个新目标、4 个函数改名、15 个 PLATE（段内 12、必要上下文 3），以及缩放动画 84 条既有指令 EOL 的精确订正。注释 setter 共 175 次；raw、carve、disasm 和新增 §5.1 均为 0。两个共享清零/拷贝 helper 的长度参数按实际字节单位订正，dispatcher case 编号保持原值。

RAM 基址 `gUIEffectArgs` 的两个 DEFAULT 虚拟符号及 7 条既有引用只派生显示名，字节、类型、ID、namespace 和独立边界完整保持。v1 真实 owned 演练另发现外部 typed pointer `080d70d4` 自动从 `PTR_DAT_080d70d4` 派生为 `PTR_BG_SCREENBLOCK_29_BASE_080d70d4`，5 个失败检查仅有 7 个名称叶字段差异；该轮事务强制撤销，DB15/source207 不变且没有保存。原生 Tiny1 和完整三态诊断确认其 DEFAULT/dynamic 身份、旧 ID、`/undefined *`、`00e80006`、单条 `080d709e` READ 及 owner ID 全部不变。v2 只追加此单点派生投影，保护原 RAM2/7；源码范围增加 asm18 的标签与 LDR 两处显示投影，池字仍为原始 `0x0600e800`。

v2 的 21 个产物实际双回放逐字节相同，两次独立 validator 通过；原 20 个产物中 15 个逐字节不变、5 个必要变化，新增 1 份 pointer 辅助合同。独立完整原生 post/restore 预测均为 0 未预期差异，10 个新增 pointer 反例全部拒绝。生产 v2 的真实 prestate、dry 和 owned fullrollback 全部通过，覆盖 162 个 Function、3837 个核心地址、1580 个模块池字、43716 个模块单位、48 个外部保护单位、25823 个指令位置、65 个外部指令位置、366 行标签闭包和独立 pointer Tiny1。完整后态、同 Program end(False) 恢复以及三个模式的 DB15/source207 前后哈希均通过；旧 v1 失败材料保留。

独立最终审查后唯一保存一次，新进程 check 和五份独立原生采集通过。88 个新 USER、4 个 Function 改名、92 个 primary 节点、45 条新 DATA 均精确核对；全局 Equate 2488 个、绑定 12739 条。标签闭包 incoming 为 400→417；25823 个指令位置只投影 360 个批准 owner 名字段，65 个外部指令位置及控制流类型、override 精确保持。3 个 DEFAULT 派生符号与 8 条引用按 RAM2/7、pointer1/1 分别完整保护。

全范围原生汇编重导、mode 注入和模块拆分通过。92 个 native 表达式、6 个新增 fallback、129 个有效 pins（123 继承加 6 新增）及 98 个表达式断言通过；11 个 GNU 定义、14 个既有 registry tuple 和 4 个 CSV name cell 精确同步。源码在 16 项许可范围内精确改变 14 个路径。49/49 资产导出、构建和 33554432 字节整 ROM 逐字节比较通过，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，ELF SHA256 `5e94f4e96abb2414a25114e1f6c3f44c5f4318892423816515654a8ab72587b4`。剩余自动名 787；8 个原始块 3410 字节继续由其所属段处理。

证据目录 `output/refine-run-20261028-105948/`。

| 核验 | 文件 | SHA256 |
|---|---|---|
| 实际 Phase1 独审 | `f16-seg3-phase1-static-review-v2.json` | `5a9d22ff28dac21ca762dfea172421c3fc50e08bdbe81f0824b310c6c4fdcf49` |
| 唯一保存 | `f16-seg3-apply-v2.json` | `581aba3b9d8f2580cdab2ea14df3a30ea6a81ce83e0bdec218d540c96ba4a78c` |
| 新进程 check | `f16-seg3-persisted-check-v2.json` | `2f84eb64434e1b0fab7890104209e08ce372f1bc499af29ae630cf811274b72d` |
| 独立数据库与派生后态 | `root-f16-seg3-saved-db-gate-v2.json` | `d8ed59aabda3d1cd3d64b98504894b4bbb3a9df71908f80151b9d3dae0ebbb26` |
| 指令保护属性 | `root-f16-seg3-saved-properties-gate-v2.json` | `6be465b058934cc48eba4cce41f472992f0d2fe52a43b32dd4772cf2a3456767` |
| 源码与整 ROM | `f16-seg3-source-landing-final-v2.json` | `f9e78299fedc7add8a54dd66b04f13da77fa2a9942960d6795dd3ff7439cb640` |

下一任务为 F16-Seg-4 `[0x080c4350,0x080c57c4)`，8 个 Function、139 个池字、61 个自动名、4 个 raw 块共 2128 字节。

### 4.04 Seg-4（2026-11-13）

范围 `[0x080c4350,0x080c57c4)`，共 5236 字节、8 个既有 Function。原 139 个池字加回收的 64 个池字，合计 203 槽：27 EQ_ADD、80 REF_ADD、13 REF_PRESERVE、83 CASE_VECTOR_PRESERVE_CORE；120 个源标签、122 条 EOL、73 个其余目标标签、3 个函数改名及 9 个 PLATE。新 USER 标签共 193 个；旧 switch 命名空间、83 个偶数 case 向量的字节与引用核心保持。

四个正引用 raw 块共 2128 字节完成 R4：884 条 Thumb 指令共 1838 字节、64 个 `/undefined4` 池字共 256 字节，以及 17 个原样双字节零对齐共 34 字节。反汇编只作用 25 个明确代码区间，关闭跟随流与代码分析，不新建、删除或合并 Function。`080c4350` 的 body 从 56 字节扩展到 1894 字节，排除池与对齐；既有 `080c4ca0` helper 的 body 和标志保持。仅 `080c437a`、`080c4424` 两个共享栈帧出口设置 CALL_RETURN。carve 和新增 §5.1 均为 0。

函数名订正为 `run_ui_effect_card_render_state_machine`、`classify_player_hand_count_threshold`、`init_ui_effect_card_pair_request`；阈值读取的结构字段为手牌数，OAM 的 `0x70fb/0x70fc/0x70fd` 为 attr2 tile/palette 值。对应消费者与上下文注释一并核对。两个 RAM offcut 的 31 条既有引用仅接受批准的派生显示名变化。

完整保护范围为 141 个 Function、4876 个去重状态（4440 槽 holder、1644 word、508 target 的并集）、43716 个模块字节单位及 48 个外部单位。22359 条指令属性、2618 行闭包与 60 条 typed pointer 边完整核验；闭包 incoming 从 270 增至 443。193 个实际新 USER ID 严格唯一，且与全部 83848 个 before 身份不相交；其余字段由 before、批准动作与原生 detached decode 推导，未用实际 POST 回填期望。

正式分析第三轮 PASS，静态接线和来源工具修正版独立复核通过。真实 prestate、dry 与同 Program 完整 owned-false 演练均通过；完整 POST 验证后撤销事务，原生状态、DB15 和 source212 均恢复一致。最终 Phase1 独立审计 `12a0093abe15a1625c34de170a4f67b73fe98c98458891e3ebd14a11b71f1d72` 通过后唯一保存。实际 apply 收据 `5d549ff7c60fe74e77eec8667438f5482b1022dd6fac734ae700c05f29b1d7aa`、新进程 check 收据 `32b2ff59a810c8765304204d7405126b79317338fb3ad935158d2555040f5edd` 与三组独立 Java 后验全部通过。保存后完整门禁为 `93735f31e1a0bbd59cc1612b3369391eb985f5217d88ee794e5ad31c71ddb1bc`。

重导全汇编、模式注入与拆分检查通过；10 个 GNU 定义、200 个原生表达式、132 个有效 GAS 投影及 203 槽表达式断言完成。9 个既存 registry tuple、文档 CSV 的 3 个 name cell、真实 inventory 的 3 个函数名与 `4350` body length `56→1894` 精确同步。许可 11 路径内精确变化 9 路径；原始块中的 49 条高寄存器 MOV 经注入器按原 opcode 导出为 `.hword`，仍对应实际 Ghidra 指令。

资产导出 49/49、构建及 33554432 字节整 ROM 逐字节比较通过；SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。ELF SHA256 为 `920e8cc788ef1260fafa627044f6b9a5189a8e98bd4afed28f4a0b02811864be`；源码流水线门禁为 `f85cf9d3203402ace96a18a505c7fc78b669848832c56223fdc10c3f0dfa9b16`。

模块保留 112 个 Function，池字增至 1644 个；剩余自动数据名 726 个（DAT 549、DWORD 90、PTR 87），未分类块剩余 4 个共 1282 字节。下一任务为 F16-Seg-5 `[0x080c57c4,0x080c699c)`，11 个 Function、139 个池字、79 个自动名、3 个 raw 块共 1224 字节。

### 4.05 Seg-5（2026-11-13）

范围 `[0x080c57c4,0x080c699c)`，共 4568 字节、11 个既有 Function 和 139 个原有池字。段内 242 槽加外部回调表 8 槽，共 250 槽；完成 37 EQ_ADD、139 REF_ADD、4 REF_PRESERVE、62 CASE_VECTOR_PRESERVE_CORE、7 R7_DATA_DEFINE 和 1 R7_TYPE_PRESERVE。新建 333 个 USER 标签、写入 188 个数据 EOL，订正 9 个函数名及 11 个 ASCII PLATE；函数签名、参数存储及标志保留。

三处正引用原始块共 1224 字节完成结构化：395 条 Thumb 指令共 794 字节，103 个 `/undefined4` 池字共 412 字节，9 处原样双字节零对齐共 18 字节。代码只覆盖 69 个明确区间，逐 head 解码且不跟随流、不启用自动分析；不新建、删除或合并 Function，不修改 flow override。`080c5b78` 的 body 从 330 字节扩为 1028 字节、67 个规范化区间；`080c6268` 从 334 字节扩为 430 字节、8 个区间，均排除池和对齐。`080c60f4` 原为无标签四字节 `.byte`，由 `080c6088` 的真实 LDR 读取，已接通 `game_str_en_0484`，不登记 §5.1。

状态表 `[0x09e5ab84,0x09e5aba4)` 完成 32 字节 carve：8 项中 6 项为函数地址加 1，索引 4、7 为 0，close handler 重复使用。首个既有 `/dword` 保留，其余 7 个单元定义为 `/dword`；8 项原有空 outgoing refs 精确保持，`080c661c` 的既定 operand-0 DATA 引用接通表基址。后续 88 字节保持原始 incbin，相邻 `09e5aba4` 独立表保持。新增 §5.1 为 0。

正式方案、生产脚本及 Root 核验工具分别完成独立复核；原 ROM 13 个入口乘 6 种语言的 78 条局部化路径独立匹配真实 GNU 字符串地址。真实 prestate、dry 和 owned fullrollback 全部通过：137 个 Function、7295 个完整地址状态、1755 个 word holder、578 个 target holder（含 5 个非 NULL even_function 完整 ABI）、20264 个指令位置、2441 行标签闭包及 46 条 typed pointer 边。transaction 1242 的完整 POST 通过后 end(False)，完整 BEFORE 和 83960 个原有符号身份恢复；DB15/source217 与源码副本在三模式前后精确相等。

最终实际 Phase1 独审通过后唯一保存一次，新进程 check 与三份独立 Java 后验全部通过。333 个实际 USER ID 严格互异，且与 35925 个静态身份和 48035 个动态身份的全集不相交；其他原生字段与独立预测一致，未预期差异为 0。闭包 incoming 为 211→532，全局 Equate 为 2503 个、绑定 12803 条。保存后的两个 body、7 个新 dword、103 个新池字和全部 395 条指令均完整验收。

全范围原生重导、mode 注入和模块拆分通过。242 个表达式断言由 235 个 native 表达式和 7 个新增精确 fallback 闭合；132 个继承 pins 保持，有效 pins 共 139。15 个 GNU 定义、11 个既有 registry tuple、9 个 CSV name cell 及 inventory 的 9 个名称与 2 个 body 长度精确同步。源码只在 15 项许可范围内改变 13 个路径；段外仅模块 01、15、17 的 4 条批准 BL 显示投影。49/49 资产导出和构建通过，33554432 字节整 ROM 与原件逐字节相等，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，ELF SHA256 `6f3d9a40dbd6623c07f8607e81c554844b299f694314c240b26d9afe1517afa2`。

证据目录 `output/refine-run-20261028-105948/`。

| 核验 | 文件 | SHA256 |
|---|---|---|
| 最终实际 Phase1 独审 | `f16-seg5-phase1-static-review-v1.json` | `e76930ffec069694a5959fec8f7c581d0c13c92d104cc36a0324ad45d2ed18e7` |
| 唯一保存 | `f16-seg5-apply-v1.json` | `0fe4d954648dc8338e7c03ae64a790767254d66b21a21912eee5ce2ff333a1fa` |
| 新进程 check | `f16-seg5-persisted-check-v1.json` | `b256b74839a047f67801d3025010129e36ef85967ac829904833f2066d13b3b3` |
| 独立完整保存后态 | `root-f16-seg5-saved-complete-v1.json` | `c521f08aba0d4cfdb5047ce4454769b2e0bc8fc0642e4edd6bdccd05e4aa5b82` |
| 源码与整 ROM | `f16-seg5-source-landing-final-v1.json` | `6a18d729a2e29ac7661e813794f487f86fd842dbfb57e4adf75a04886cbe05ed` |

模块仍为 112 个 Function，池字增至 1747 个；剩余自动数据名 647 个（DAT 505、DWORD 57、PTR 85），只剩 Seg-7 的 58 字节原始块。按用户最新指令，本轮在 Seg-5 完成并提交后停止，Seg-6 未开始；下次任务为 `[0x080c699c,0x080c7af8)`，13 个 Function、176 个池字、98 个自动名、无 raw 块。

### 4.06 Seg-6（2026-11-13）

范围 `[0x080c699c,0x080c7af8)`，4444 字节、13 个既有 Function、176 个池字、98 个自动数据名，无原始块。完成35条常量绑定、48条新增DATA引用和15条既有引用保持，78项CASE核心状态保持；98个源标签加5个目标标签共103个USER、156条EOL、10个函数改名和34份ASCII PLATE。函数body、ABI、数据类型及flow override保持，无carve、反汇编和新增§5.1。

真实prestate、dry和fullrollback通过。完整后态与独立预测一致；事务1242执行end(False)后，同Program完整前态及84196个既有符号ID恢复，DB15/source222和副本逐字节相等。最终实际独审通过后唯一保存一次，新进程check及独立Java后验通过，覆盖183个Function、1933个word、3262个完整地址状态、26385条指令属性、14980行标签闭包和1600条typed pointer边。新增103个USER ID互异且不与全部既有ID相交，incoming为9258→9306，全局Equate为2512个、绑定12838条。

首次独立Core采集因配置误选测绘扩展版、多出source_owners字段，被严格比较拒绝。原始结果保留；独立调查证明183条附加owner记录正确，其余仅49处合法集合顺序差。改用前态已验证的标准Java采集器、相同输入重采Core后，原有严格比较器通过；Properties/Tiny复用原始合格结果。未删除观察字段，未放宽后验，也未重复保存。

原生重导和模块拆分通过。11个GNU定义、152个有效pins（139继承、13新增）、163个native表达式及176项表达式断言通过；精确同步34个现存registry tuple和10个CSV名称单元格。源码仅12个许可路径变化（含3个忽略中间文件），asm/rom.s保持。49/49资产导出、构建和33554432字节整ROM逐字节比较通过，SHA1为9689337d6aac1ce9699ab60aac73fc2cfdccad9b。

证据目录：`output/refine-run-20261028-105948/`。

| 验收记录 | SHA256 |
|---|---|
| `f16-seg6-phase1-static-review-v1.json` | `c3ca5db4b707c9aad25d75f4c633ceff99a7045e7d7232925b8858a0800df997` |
| `f16-seg6-apply-v1.json` | `183bfb586ba60f9117db8895c7a3dc0d304a4c074b38d6cd7d928c29438a4558` |
| `f16-seg6-persisted-check-v1.json` | `c6a3e8b098f57b576dcce3d622ef24365018ca3f1c2e015eec67c1d267efca91` |
| `root-f16-seg6-saved-native-gate-v1.json` | `df2a2f88157e21376034647ea62d70e64b3638d5d1d147e1ca8e689c421c7859` |
| `f16-seg6-source-landing-final-v1.json` | `b77fbd2e90571c6bf42b5e3a5842bb8751750428918a0afd0e199dac63382fb7` |
| `f16-seg6-saved-java3-schema-investigation-v1.json` | `65c766797075f2736b38408fbc2e7e23a699ac44ff618af26908490ef214b3d4` |

模块完成6/10段，112个Function、1747个池字；剩余549个自动数据名（DAT422、DWORD57、PTR70）。仅剩Seg-7的58字节原始块待所属段分类，§5.1为0。完成单段提交后继续F16-Seg-7 `[0x080c7af8,0x080c8bf0)`。

## 五、地址序路线图

| 段 | 范围 | 字节 | 既有 Function | word | 自动数据名 | raw 块/字节 | 状态 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | `0x080c1448..0x080c2544` | 4348 | 7 | 210 | 155 | 0/0 | ✅ root 验收通过，单段提交 |
| 2 | `0x080c2544..0x080c36a8` | 4452 | 15 | 145 | 118 | 0/0 | ✅ root 验收通过，单段提交 |
| 3 | `0x080c36a8..0x080c4350` | 3240 | 12 | 98 | 76 | 0/0 | ✅ root 验收通过，单段提交 |
| 4 | `0x080c4350..0x080c57c4` | 5236 | 8 | 139 | 61 | 4/2128 | ✅ root 验收通过，单段提交 |
| 5 | `0x080c57c4..0x080c699c` | 4568 | 11 | 139 | 79 | 3/1224 | ✅ root 验收通过，单段提交后停止 |
| 6 | `0x080c699c..0x080c7af8` | 4444 | 13 | 176 | 98 | 0/0 | ✅ root验收通过，单段提交 |
| 7 | `0x080c7af8..0x080c8bf0` | 4344 | 12 | 223 | 152 | 1/58 | 未开始 |
| 8 | `0x080c8bf0..0x080c9c94` | 4260 | 16 | 110 | 95 | 0/0 | 未开始 |
| 9 | `0x080c9c94..0x080cad78` | 4324 | 13 | 167 | 158 | 0/0 | 未开始 |
| 10 | `0x080cad78..0x080cbf0c` | 4500 | 5 | 173 | 144 | 0/0 | 未开始 |

### 原始块初始化清单

| 所属段 | 起点 | 字节 | 处理状态 |
|---|---|---:|---|
| 4 | `0x080c43a4` | 272 | ✅ 正引用 R4；代码、池及原样对齐已结构化，见 §4.04 |
| 4 | `0x080c44dc` | 528 | ✅ 正引用 R4；代码、池及原样对齐已结构化，见 §4.04 |
| 4 | `0x080c472c` | 940 | ✅ 正引用 R4；代码、池及原样对齐已结构化，见 §4.04 |
| 4 | `0x080c4b1c` | 388 | ✅ 正引用 R4；代码、池及原样对齐已结构化，见 §4.04 |
| 5 | `0x080c5c3c` | 1102 | ✅ R4：349 指令/698B、98 池字/392B、6 处零对齐/12B，见 §4.05 |
| 5 | `0x080c60f4` | 4 | ✅ 6088 LDR 正引用池；复用 game_str_en_0484，见 §4.05 |
| 5 | `0x080c63e0` | 118 | ✅ R4：46 指令/96B、4 池字/16B、3 处零对齐/6B，见 §4.05 |
| 7 | `0x080c7b68` | 58 | 未分类；在所属段执行全 ROM raw/THUMB+1 引用扫描 |

## 六、§5.1 登记与跨文件补漏

当前登记 0 项。原始块分类在各段执行；初始化统计不构成零引用结论。

历史正引用补漏 `[0x0804becc,0x0804bf20)` 共 84 字节，caller 为 04D374 与 B9E0A，仍按主序 25 个模块全部完成后闭合，不能据此提前宣告总目标完成。
