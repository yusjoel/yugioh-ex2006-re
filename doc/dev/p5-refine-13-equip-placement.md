# 函数/数据细化计划 -- `asm/13_equip_placement.s`

> 范围 `[0x0809d718,0x080a78dc)`, 精确长度 **41412 B / 0xa1c4**。这是按文件序推进的第14个模块。
> F13-Seg-1至Seg-4均已完成精确落地、构建、持久化检查及root独立验收；其余6段尚未开始。
> 下一任务: **F13-Seg-5 `[0x080a1658,0x080a27a0)`**；本轮工作在Seg-4完整验收后进入提交收束，尚未启动Seg-5。
> 所有落地必须保持ROM SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`；后续仍按executor -> reviewer -> fixer顺序使用gpt-5.6-sol + xhigh。

## 一、细化要求 (R1-R9)

完整规则见 [refine-loop方法论](methodology/refine-loop.md), R1-R9逐项检查沿用该文。执行角色以当前 `.codex/agents/refine-{executor,reviewer,fixer}.toml` 为准; skill中的旧角色路径和auto-commit文字不构成授权。

- R1/R2/R3: 常量先全库按值和用途复用; 全部自动槽逐项EQ/REF/RENAME覆盖。目标LABEL的source和池槽reference的source分别读取, 不互相推断。现有equate/ref在RENAME操作中原样保留。
- R4/R7: 每个ROM_INCBIN或.byte均在所属段做全ROM raw及THUMB|1扫描, 同时检查局部分支、switch表、literal读取及fall-through。真实引用代码反汇编、数据结构化; 不能从字节形态直接登记§5.1。
- R5/R6: 先读真实消费者和机器码, 不用旧plate证明参数、返回值、卡名或基址。CID对照ROM/card-stats及data.md的逻辑CID列、密码、卡名; 禁止用整行首次字符串命中替代结构化核对。
- R8: 涉及图形时按资产定位方法验证。raw指针命中若为资产偶合, 必须提供具体文件、偏移和原字节, 保留原始命中数。
- R9: 写入前备份, dry-run逐项守卫, 全量导出和构建后验证byte-identical, 保存后再做只读持久化核验。所有新Ghidra PLATE/EOL为ASCII, PLATE全文不超过500字符。
- 地址序: Seg-1至Seg-10连续推进, 段内低地址优先。需要拆子段时保持连续边界, 不切函数、池、裸块或共享栈尾; 不提前分析后段语义。
- C7导出约束: 当前exporter只将USER_DEFINED LABEL目标导为普通符号, ROM FUNCTION不能依赖DATA REF自动导出`fn+1`; Thumb回调表达必须按实际导出路径设计。scoped switch标签复用同一Symbol对象并规范namespace/name, 不新增同址alias或改变偶地址case值。
- C13完整清点: 四字节槽与裸块头自动标签分开统计, 不能遗漏PTR/DWORD/UNK; disasm产生的新池槽必须重新扫描并完成覆盖。模块收尾必须再次检查所有自动名及stale FUN/SUB注释, 不以历史完成记录代替当前文件实测。

## 二、落地工作流 (pipeline)

```text
source/.rep备份 -> executor proposal -> reviewer独立C1-C13
-> NEEDS_FIX由fixer模式A修proposal并重审 / PASS由fixer模式B实施
-> 精确前态dry-run -> Ghidra equate/label/ref/rename/plate/disasm及必要rom.s结构化
-> 全量Ghidra导出 -> inject_modes -> split_all_s
-> export_all.py -> build -> ROM字节与SHA1核验
-> 保存 -> 独立只读后态检查 -> asm/ELF/ROM逐槽及模块残留验收
-> 活动文档/总进度更新; 仅实际函数改名时同步正式命名来源
```

本轮提交由root在最终文件审计后统一收束。executor不评分、不写review、不修改Ghidra或正式asm/constants, 不运行build。§5.1登记需要所属段的扫描证据和独立评审。

## 三、当前进度 (13_equip_placement.s)

2026-09-01完成Seg-1至Seg-4：共495槽全部落地。Seg-1的142槽、15PLATE/142EOL、两函数改名及三表carve，Seg-2的158槽、59PLATE/158槽EOL、8个case EOL、4函数改名及424B R4反汇编，Seg-3的138槽、20PLATE/138EOL、6函数改名及两张回调表carve，以及Seg-4的57槽、7PLATE/57EOL和8个新定义，均通过ROM、保存后检查和root独立验收。Seg-4把2072B零有效入口引用块保留为§5.1；Seg-5至Seg-10尚未开始。

| Seg | 半开地址范围 | 字节 | 函数对象 | 4B自动槽 | 裸块/字节 | 状态 |
|---|---|---:|---:|---:|---:|---|
| 1 | `[0x0809d718,0x0809e6f4)` | 4060 | 15 | 142 → 0 | 0/0 | ✅ 已验证 |
| 2 | `[0x0809e6f4,0x0809f744)` | 4176 | 59 | 126+32新增 → 0 | 0/0 | ✅ 已验证 |
| 3 | `[0x0809f744,0x080a0840)` | 4348 | 20 | 138 → 0 | 0/0 | ✅ 已验证 |
| 4 | `[0x080a0840,0x080a1658)` | 3608 | 7 | 57 → 0 | 1/2072 | ✅ 已验证；§5.1保留2072B |
| 5 | `[0x080a1658,0x080a27a0)` | 4424 | 38 | 108 | 5/1222 | 未开始 |
| 6 | `[0x080a27a0,0x080a38fc)` | 4444 | 16 | 184 | 1/4 | 未开始 |
| 7 | `[0x080a38fc,0x080a46a0)` | 3492 | 22 | 96 | 0/0 | 未开始 |
| 8 | `[0x080a46a0,0x080a585c)` | 4540 | 7 | 155 | 0/0 | 未开始 |
| 9 | `[0x080a585c,0x080a689c)` | 4160 | 13 | 111 | 0/0 | 未开始 |
| 10 | `[0x080a689c,0x080a78dc)` | 4160 | 13 | 78 | 2/1038 | 未开始 |

机械总数: **210个既有Ghidra Function对象**, 其中197个push入口、13个非push入口; 全文241条push中的另外44条为既有函数内部保存寄存器。函数对象数包含共享控制流入口, 不能视为210个独立栈帧。

建档基线自动标签定义共 **1199**: 四字节池槽 **1195 = DAT741 + DWORD313 + PTR141 + UNK0**, 另4个DAT标签定义在ROM_INCBIN块头, 不能当成4B Data。所有1195个槽都有地址、标签、原ROM值、源码行和使用行记录。6个ROM_INCBIN合计4732B, 4个.byte合计28B, 共10块4760B。

建档时全模块已有1329条.word, 其中134条不属于当时的自动槽定义; 仍须在所属段测绘检查用途。初始注释扫描命中90行旧自动名、18行非ASCII注释, 这是扫描行数而非PLATE数量; 正式段内分析须归并到实际comment对象。

Seg-1完成后实测剩余 **1057个自动标签定义**：四字节池槽 **1053 = DAT631 + DWORD313 + PTR109 + UNK0**，另4个DAT裸块头。Seg-2再消除原126个自动槽及`DAT_0809e74c`块头，剩余 **930个自动标签定义**：四字节池槽 **927 = DAT528 + DWORD310 + PTR89 + UNK0**，另3个DAT裸块头。Seg-3再消除138个自动槽，剩余 **792个自动标签定义**：四字节池槽 **789 = DAT422 + DWORD295 + PTR72 + UNK0**，另3个DAT裸块头。Seg-4再消除57个自动槽，当前剩余 **735个自动标签定义**：四字节池槽 **732 = DAT408 + DWORD252 + PTR72 + UNK0**，另3个DAT裸块头。上述阶段计数及初始注释扫描数均保留为历史；模块尚未整体清零。

## 四、工作记录

### 4.00 建档测绘 (2026-09-01, 未落地)

- `split_manifest.tsv`给定起止地址, 与当前asm逐字节连续覆盖一致: 41412B, 无空洞或重叠, 代码/word/zero/incbin/.byte的原始字节全部与ROM吻合。
- `temp/ghidra-functions.csv`与当前asm的210个函数入口名称、地址逐一一致, 无自动函数名, 没有脱离inventory的具名代码入口。197个push入口与13个非push入口分别记录; 不用CSV的length推算连续函数结束。
- 现有非CALL直接分支和1266次Thumb PC-relative literal读取完成机械目标计算。9个段边界均未切code/data单元、裸块或这些引用。所有跨inventory入口的非CALL分支位于Seg-3共享控制流簇内。
- root独立只读查询的28个边界/共享簇Function实际body ranges全部落在规划段内; Seg-1另外15个函数body全部在Seg-1内。没有进行Ghidra写入, root确认15个DB文件哈希不变。
- `[0x0809f9cc,0x080a06bc)`包含1个push入口和9个非push入口, 以及跨入口分支。整簇留在Seg-3, 不按CSV相邻入口切段。这里只记录控制流连接, 不对后段函数名或状态语义作判断。
- 裸块分类尚未执行, 所以§5.1保持空表。后续disasm新增函数/池槽会改变实测数量, 届时按逐段完整覆盖更新路线图, 不保留初计替代实测。

建档时asm13 SHA256: `e473bd1db9d96114f78e5ea8cde07ee83c9003d7a4f6e920ad25887196190671`；当前落地版本hash见§4.03，Seg-1/2中间态见§4.01/§4.02。

主要机械证据在 `output/refine-run-20260831-194634/`:

- `f13-module-map.json`: 全地址单元、函数、全部槽、裸块、非CALL分支、literal目标、10段映射及边界守卫。
- `f13-seg1-function-entries.json` / `f13-seg1-slots.json`: Seg-1只读查询输入, 分别15入口和142槽。
- `f13-boundary-function-entries.json`: 28个边界/共享簇入口查询输入。
- `root-f13-boundary-functions.json` / `root-f13-seg1-functions-before.json` / `root-f13-seg1-slots-before.json`: root抓取的真实Ghidra前态; `root-f13-preflight.log`记录三项查询成功。
- `root-f13-route-check.json`: root独立复核10段覆盖及42个去重Function实际body; `root-f13-seg1-targets-before.json`记录三个引用目标的真实符号对象。
- `f13-module-selfcheck.json`: 机械计数、覆盖和边界核验结果。

### 4.01 F13-Seg-1 完成记录 (2026-09-01，已验证)

- 范围`[0x0809d718,0x0809e6f4)`，4060B。第二轮正式review PASS；最终proposal SHA256 `fd84b9c4fcffb99261851465d7f1bf2033fd0133009e4b0b070b1f06e6bdb1a7`，review SHA256 `1b5146d8697bf6ccbe03f259dc941fc287e30ffb4f38fe6ae74030f34b86c022`。首轮消费者伪命中及d914条件修订历史完整保留。
- `tools/ghidra-labeling/RefineF13Seg1.py`最终SHA256 `12deef1a64fc083ddc623ce91105b4585fd81c9086fdc002f1474d56d017b6f9`。93EQ/19REF/30RENAME，共142槽；15全文PLATE、142EOL均ASCII，最大PLATE472字符，d914为403字符。9NEW（8数值常量+1RAM地址）/35REUSE，0disasm、0新增Function、0新增§5.1。
- 19REF中17条新增USER DATA，2条switch DEFAULT按目标/operand0精确替换；30个LP槽原DATA/DEFAULT/primary引用完整保留。switch基址Symbol id6770/id7145只复用原对象规范全局名；52个偶地址word及24个case对象保持。C5EC/D9C0的DefinedData仍为None；E1CC的undefined4及原22条READ/WRITE保持，未读取未初始化RAM值。独立后态同时核对16条既有case-LDR随已批准池标签变化的target_primary导航，引用本体字段均未变。
- `rom.s`仅把原10160B host拆为340B前缀、三表63个`fn+1`/252B、9568B后缀。63个原pointer Data及DEFAULT odd引用、477ac边界完整保持；只创建三张表的USER主LABEL，不重定向偶Function或改Data类型。无NULL补造、无额外carve。
- 两个Function保持原ID/body/incoming/指令EOL，仅改名：`0x0809d7ec` -> `enqueue_equip_chain_counter_sprites_by_card`；`0x0809e5e0` -> `scan_field_slots_for_vwxyz_dragon_catapult_cannon_activation`。全部15个函数身份/函数体及局部共享尾保留，全局Function总数5209；28个边界/共享簇函数独立守卫通过（其中27个完全原样，另一项与本段已批准PLATE集合相交）。
- 最初备份`.rep.bak-20260901-022608-pre-F13Seg1`的15DB和`pre-f13-seg-1`的59源码快照保留。首次apply仅在后置观察代码解析`Stack[-0x38]`时抛错，事务执行rollback；后续290地址+15函数完整state（含body_refs）与首次写入前逐字段相同，JSON SHA256同为`057c69e207dfd69771f4fa2543dad3a3d4a32820ff4f6577018ec80c9be65d00`。这是观察代码错误，不是ROM byte-identical失败；Save改变了DB物理文件，未声称DB字节回原。修正两处导航解析后重新通过root脚本门禁/dry3，并新增核验`.rep.bak-20260901-041113-pre-F13Seg1-retry`。第二次apply的计数/STATUS均FAIL=0且Save成功，首次失败证据继续保存。
- 全量Ghidra导出`080000c0..084c7637`完成，去除4条独立mode指令后inject/split；本次`export_all.py`全部49步成功，`NOPAUSE=1 build.bat`成功。输出33554432B与原ROM逐字节相同，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。5目录18200文件逐SHA1与本次导出前一致；原exporter修复保持，构建仅有既有r13警告。fresh `-noanalysis -readOnly check`与保存的完整post-state精确相同。
- 真实`ExportFunctionInventory.py`刷新4文件后执行sync `--dry-run`前后审计；CSV仅两行name单元格改变，proposed_name/score及其他字段保持。registry仅六条：两项name+PLATE、三wrapper PLATE、97828一个旧callee子串；其余1512tuple不变，未把97828旧registry PLATE写入DB。正式asm12仅97ac2/97b48两个BL目标拼写变化；其余23模块、asm13后段、rom.s host外、既有constants和exporter原样。
- 最终段内自动槽/旧FUN或DAT类注释/裸块均0；1525条指令、194word及32处2B对齐注记/机器码保持。当前asm13 SHA256 `3218ebbbd6743fab7ebf47d96c7ad61c08fd64972dbd9fc5ea8fa62371681bd7`。保留既有CRLF，实际whitespace检查通过；该段验收状态已由root记录。

证据均在`output/refine-run-20260831-194634/`：`f13-seg1-dry3.log`、`f13-seg1-apply2.log`、`f13-seg1-apply-receipt.json`、`f13-seg1-rollback-verification.json`、`f13-seg1-retry-audit.json`、`f13-seg1-byte-identical.json`、`f13-seg1-persisted-check.json`、`f13-seg1-name-sync.json`及`f13-seg1-landing-gates.json`。root的独立结果为`root-f13-seg1-{words,scope,functions,names,slots}-verification.json`及`root-f13-boundary-after-verification.json`，全部通过；7项fresh只读查询前后15DB文件hash保持。

下一段为Seg-2 `[0x0809e6f4,0x0809f744)`，本句保留§4.01完成时的时态；其后完成结果见§4.02。

### 4.02 F13-Seg-2 完成记录 (2026-09-01，已验证)

- 范围`[0x0809e6f4,0x0809f744)`，4176B。第二轮正式review PASS；最终proposal SHA256 `60370c445976ffe021413cdea6410e9bce8e9ab134613e4a91dd193bfb03b8b4`，review SHA256 `2a757d6db38da4943ec3f84894f48130fb415326dd415f0329221c570bb3523a`，plan SHA256 `b54987a1ad0cc564e5e6bfa3693b8e435d5700ace3e38f4d1facb7f5b1b4fd0a`。首轮review要求把两个12B fixed-CID wrapper一并纳入函数改名；Mode A只扩充相关函数名、同步合同与三处段外odd word守卫，158槽、R4范围、24NEW/48REUSE及59条PLATE数量均未扩大。
- `tools/ghidra-labeling/RefineF13Seg2.py`最终SHA256 `8ff995381e3d524217d5e97ad8cf111a5f73b246e50c10dd04ef1d6ae287fd89`。119EQ/20REF/19RENAME，共158槽；59条完整PLATE、158条槽EOL及8条case EOL均为ASCII，最大PLATE 469字符。新增17个`card_info.inc`常量和7个`duel_field.inc`常量，共24NEW；48REUSE。
- 原`[0x0809e74c,0x0809e8f4)` 424B块已按R4精确反汇编为145条指令/316B、25个DWORD池/100B和4处仍为undefined1的2B padding/8B。原27条指令保持；新增控制流为13 CALL、21 branch和26 literal READ。dispatcher Function id16934保持，body由54B扩至370B、精确覆盖12个range；8个case共用原函数栈帧，没有新建case Function，全局Function数仍为5209。
- 19个RENAME槽的operand0 DATA/DEFAULT主引用完整保留；20个REF按审定合同建立DATA/USER_DEFINED主引用。8个case目标、25个池、3个RAM对象及4处padding的Data/ref/type/source/长度后态均通过独立守卫。`0x09e477c0`原DEFAULT DATA引用本体不变，仅目标导航名随`0x0809ec34`函数改名派生更新；`0x09e4788c`与`0x09e47890`继续保持无Ghidra Data/ref，三处odd raw word均保值且未carve。
- 四个Function保持原ID/body bytes/incoming和原EOL，仅改名为`scan_player_card_array_for_equip_activation_marie_the_fallen_one`、`scan_player_card_array_for_equip_activation_by_cid`、`scan_player_card_array_for_equip_activation_sinister_serpent`和`scan_player_card_array_for_equip_activation_treeborn_frog`。全部59个函数的身份、body、incoming和PLATE/EOL合同，以及13个callee的既有状态均通过root只读后态核验。
- 首次真实apply的事务动作已回滚：失败来自后置观察器对80个Ghidra mnemonic显示别名、4个函数prototype中派生显示名，以及`0x0809e8f4/0x0809e8f6`批准分支新增incoming的过严比较，共86项；不是ROM byte-identical失败。`f13-seg2-apply-before.json`与回滚后dry3完整179地址、59函数、13callee、465 units/Function总数5209的state逐字段相同；通用wrapper Save改变过DB物理文件，因此仅陈述语义前态恢复。保留首次失败脚本/日志/诊断，另建`.rep.bak-20260901-064538-retry-F13Seg2`并核验15/15文件。最终脚本只加入10组显式mnemonic规范、4个prototype精确旧名到新名替换、以及批准branch incoming差集守卫；dry4和root重试门禁通过后第二次apply、事务postcheck与Save均FAIL=0。
- 全量Ghidra导出、mode清理、inject、split、`export_all.py` 49步及`NOPAUSE=1 build.bat`均成功。首次导出因调用端等待超时留下不完整日志，未作为成功依据；PTY重跑完成后才进入后续步骤。输出ROM为33554432B，与原ROM逐字节相同，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。fresh `-noanalysis -readOnly` persisted check与保存后state一致。
- 真实`ExportFunctionInventory.py`刷新4文件后，CSV仅4个`name`单元格变化，registry仅4个完整name+PLATE tuple变化；其余1514 registry tuple、CSV其他列、auto inventory和summary保持。inventory共5209行，仅4个函数名与dispatcher body length `54 -> 370`变化。其他24个asm模块、Seg-2范围外源码、`rom.s`/includes、旧常量行及`export_post_banlists_tables.py`修复保持。
- 自身`f13-seg2-landing-gates.json`和`f13-seg2-persisted-check.json`通过：段内自动标签、旧FUN/DAT注释、`ROM_INCBIN`/`.byte`残留均0，24个新常量精确，只有`asm/13_equip_placement.s`变化。root汇总`root-f13-seg2-final-gates.json`再次独立核对scope/names/state/slots、5项fresh只读查询和15个DB文件前后hash，均PASS；当前asm13 SHA256 `634dafdad722f681b8f308cd112229f5363c7825c13f3536f0de27c9fdfbda49`。该段验收时暂存区为空，完成状态已由root记录。

下一段为Seg-3 `[0x0809f744,0x080a0840)`；本记录没有预先分析其语义。

### 4.03 F13-Seg-3 完成记录 (2026-09-01，已验证)

- 范围`[0x0809f744,0x080a0840)`，4348B。第二轮正式review PASS；最终proposal SHA256 `f00685aad1690e7c4264311ecbe941e429c0e7a400136a882497725643fea89c`，plan SHA256 `c0438860bcdbfc05f8a4db4be8fe2e347362b8cb007247e3ccf15fe64ac90b12`，review SHA256 `a528e345bf7585aef15131b8b0247433d081ac1171b8633d57108009d9781919`。Mode A只订正`ARMOR_EXE_CID`的密码证据和段外sibling registry全文替换合同，138槽及其他动作范围保持。
- `tools/ghidra-labeling/RefineF13Seg3.py`最终SHA256 `251c4845960d1228cc0514b32e7a515739f33a8eb732426543f01d4383764935`。98EQ/21REF/19RENAME，共138槽；20条完整PLATE和138条槽EOL均为ASCII且不超过500字符。新增17个定义，另复用30个既有定义；0新增Function、0disasm、0新增§5.1。
- `rom.s`把两张外部回调表结构化为58个保值的Thumb odd word，共232B：`equip_activation_phase3_callbacks`为54项，`equip_activation_phase1_callbacks`为4项。phase-3表原Data/DEFAULT odd引用保持；phase-1表前两项Data4状态及后两项无Data/无ref状态均保持，未扩大carve。另有2条审定辅助引用指向偶地址Function，用于保留odd回调值的导航；回调word、原引用本体及目标Function边界均未改变。
- 6个Function按审定名称改名；20个Function的Symbol ID、body bytes/ranges和incoming保持，prototype只随批准名称精确同步。20条PLATE完整落地。`0x0809fb16`的Function body包含池槽`0x0809fb1c/0x0809fb20`，因此其EOL后态只增加这两条批准的槽注释，其余19个Function的EOL保持前态。
- 首次真实apply仅因后置守卫仍要求`0x0809fb16`函数EOL完全等于前态而事务rollback，无receipt、未导出或构建，也不是ROM byte-identical失败。回滚后205地址和20函数完整state与写入前逐字段相同，原始JSON SHA256同为`d48299ccc7979736c6731c5e00667c148a91e30f5ed26c36955e1aa1a6f5c4c2`；Save可能改变DB物理文件，故只陈述语义前态完整恢复。守卫仅按函数body半开范围加入上述两条批准EOL，新建`.rep.bak-20260901-082900-pre-F13Seg3Retry`并核15/15后，经root重放行的第二次apply、postcheck、Save和fresh readOnly persisted check均PASS。
- 全量Ghidra导出、mode清理、inject、split、`export_all.py` 49步及`NOPAUSE=1 build.bat`均成功。输出ROM为33554432B，与原ROM逐字节相同，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。17个新定义、两表58word、138个槽表达式/ELF值/ROM原值及段内ASCII、自动名和裸块残留均通过自身`f13-seg3-landing-gates.json`。
- 真实inventory刷新后，CSV仅6个name单元格改变；registry精确同步6个rename tuple及`FUN_0809ed50`一条审定sibling PLATE全文，其余命名数据不变。root汇总`root-f13-seg3-final-gates.json`独立核验3项fresh只读查询、15DB查询前后hash、20函数、138槽+2辅助引用、58回调word、17定义、命名同步、24个其他模块和段外源码，全部PASS。正式快照仅11个批准文件变化，暂存区为空。
- 当前asm13 SHA256 `121004fdbfcc154d2677d5e04263e6f2e6039c9e59f56e31a07f9242923fd42b`。Seg-3段内自动数据名、旧自动名注释及裸`.byte`/`.incbin`残留均0；该段独立验收闭合。

下一段为Seg-4 `[0x080a0840,0x080a1658)`；本记录没有预先分析其语义。

### 4.04 F13-Seg-4 完成记录 (2026-09-01，已验证)

- 范围`[0x080a0840,0x080a1658)`，3608B。首轮正式review PASS；最终proposal SHA256 `2dba3097eafc80290faa35c4a8d7e02541b3a7cd7f08676c5d7f1cdcda2d4eba`，plan SHA256 `66e0dfd362db5f82670dd3cbcaa5c878e25e5c8ed9fd91ad32bbdef819c823fa`，review SHA256 `21438e4af40d6d1b6f3678b4b92544728ef7e2f6d76d8fc60aa652c294de1985`。review概述中的PLATE最大长度461是旧统计，落地以plan全文实测466为准，未改proposal动作范围。
- `tools/ghidra-labeling/RefineF13Seg4.py`最终SHA256 `1bff5760ae34a726d95a9194d0981b0992ac90916915ef4839204d25f098275b`。34EQ/16REF/7RENAME，共57槽；7条完整PLATE、57条EOL均为ASCII，最大PLATE466字符。新增8个定义：`card_info.inc` 2项、`duel_field.inc` 4项、`oam_attr.inc` 2项；其余21个常量或全局复用。0函数改名、0carve、0disasm。
- 7个gP1LifePoints槽的operand0 DATA/USER_DEFINED主引用原样保留；16个REF按审定合同建立DATA/USER_DEFINED主引用。`gEffectEntryArray@0201b590`保留原`undefined2` Data及全部既有引用，不创建alias或RAM Data。Ghidra把动态DEFAULT对象调用`setName`后物化为唯一USER_DEFINED主LABEL并分配新ID，这是Symbol API的实测行为；最终三个新槽导航到同一持久化ID，名称/source/address及Data/ref合同均通过独立后态核验。
- 首次实写在`gEffectEntryArray`前态守卫中未识别同一事务内已规范化状态，事务rollback且无receipt。后续诊断确认动态DEFAULT标签物化时Symbol ID变化，诊断事务的缓存视图在rollback后仍显示USER标签；fresh只读进程证明持久化语义前态未污染。retry-2仍错误要求同ID，retry-3已接受合法新ID但漏对RAM目标执行导航ID归一化；retry-4只修正post归一化调用范围，并以离线synthetic test验证目标和三个槽的生成ID归一化。每次重试前均建立并核验15/15备份，动作/PLATE/EOL表未变；最终real apply的PREFLIGHT、POSTCHECK、STATUS均FAIL=0，receipt、Save及fresh persisted check成功。上述为Ghidra后验守卫修正，不是ROM mismatch。
- `[0x080a0b20,0x080a1338)`的2072B块按Rule 3保留原`ROM_INCBIN 0xa0b20, 0x818`。入口raw/THUMB|1命中均0；758个内部滑窗命中经机器行/结构化数据源过滤后有效入口引用0。递归解码只用于分类证据：822条指令/1754B、71个literal word/284B、17处2B padding/34B；Ghidra的2072个DataDB1、symbols/refs/TMode及源码投影均保持。块内55个BL出边和共享退出不构成外部入口引用，正式登记§5.1。
- 全量Ghidra导出、4条独立mode清理、inject、split及25模块边界检查完成；`export_all.py` 49/49、`NOPAUSE=1 build.bat`和fresh只读持久化检查均成功。输出ROM为33554432B，与原ROM逐字节相同，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。相对pre-Seg-4的59文件快照仅`asm/13_equip_placement.s`、三份新增常量文件和`output/2343.elf`变化；其他24模块、`rom.s`、includes、CSV、registry、四份inventory和exporter修复保持。
- 自身`f13-seg4-landing-gates.json`与root汇总`root-f13-seg4-final-gates.json`均PASS：57槽asm表达式/ELF/ROM值、8定义、62地址、7函数、2072B块、ASCII/残留和模块scope全部精确；root的fresh只读查询结束后15DB文件hash保持。当前asm13 SHA256 `aaa2b403112747ba06a0994ca7688044542adc935c807f8a95edb3d54a7b9044`。本轮在Seg-4完整验收后进入提交收束。

下一段为Seg-5 `[0x080a1658,0x080a27a0)`；尚未启动语义分析。

## 五、10段路线图 (地址序)

边界按地址约均分后吸附到完整函数入口; 所有尾池、对齐、共享尾和裸块分配给唯一所属段。函数列为Ghidra对象数; 非push列保留不能用push扫描发现的入口。旧细化覆盖尚未核验, 全部从本轮逐槽证据重新建立。

| Seg | 范围 | fn/非push | DAT/DWORD/PTR/UNK | 块头自动名 | 裸块分布 | 旧覆盖 | 下一工作 |
|---|---|---:|---:|---:|---|---|---|
| 1 | `0809d718..0809e6f4` | 15/0 | 0/0/0/0 | 0 | 0 | 本轮完成 | ✅ 已验证 |
| 2 | `0809e6f4..0809f744` | 59/1 | 0/0/0/0 | 0 | 0 | 本轮完成 | ✅ 已验证 |
| 3 | `0809f744..080a0840` | 20/10 | 0/0/0/0 | 0 | 0 | 本轮完成 | ✅ 已验证 |
| 4 | `080a0840..080a1658` | 7/0 | 0/0/0/0 | 0 | `080a0b20/818` incbin | 本轮完成 | ✅ 已验证；§5.1保留2072B |
| 5 | `080a1658..080a27a0` | 38/0 | 52/36/20/0 | 2 | `080a1720/1ea` incbin; `080a1950/4` .byte; `080a1dd8/10` .byte; `080a1f54/ac` incbin; `080a2018/21c` incbin | 未核验 | executor -> reviewer -> fixer |
| 6 | `080a27a0..080a38fc` | 16/0 | 66/101/17/0 | 0 | `080a38f8/4` .byte | 未核验 | executor -> reviewer -> fixer |
| 7 | `080a38fc..080a46a0` | 22/2 | 92/0/4/0 | 0 | 0 | 未核验 | executor -> reviewer -> fixer |
| 8 | `080a46a0..080a585c` | 7/0 | 138/0/17/0 | 0 | 0 | 未核验 | executor -> reviewer -> fixer |
| 9 | `080a585c..080a689c` | 13/0 | 60/37/14/0 | 0 | 0 | 未核验 | executor -> reviewer -> fixer |
| 10 | `080a689c..080a78dc` | 13/0 | 0/78/0/0 | 1 | `080a7234/40a` incbin; `080a764c/4` .byte | 未核验 | executor -> reviewer -> fixer |

### Seg-1 建档入口与风险（历史记录，已由§4.01闭合）

下列入口名与风险描述保留建档前态；两处现名及全部守卫的落地结果见§4.01，不再表示待执行的Seg-1计划。

`[0x0809d718,0x0809e6f4)`, 4060B, 15函数, 142槽(110DAT+32PTR), 无ROM_INCBIN/.byte。末函数的Ghidra body到`0x0809e6f1`, `0x0809e6f2..0x0809e6f3`为2B对齐, 下一完整函数从`0x0809e6f4`开始, 不属于Seg-1。

| 入口 | 当前正式名称 | 地址区间内自动槽 |
|---|---|---:|
| `0x0809d718` | `scan_equip_zone_for_last_turn_activation` | 1 |
| `0x0809d764` | `scan_equip_zone_for_last_turn_sprite` | 1 |
| `0x0809d79c` | `scan_equip_chain_for_power_bond_sprite_and_lp_indicator` | 1 |
| `0x0809d7ec` | `scan_equip_chain_list_for_sprite_by_card_and_zone` | 4 |
| `0x0809d86c` | `scan_equip_chain_list_for_sprite_crush_card` | 1 |
| `0x0809d880` | `scan_equip_chain_list_for_sprite_deck_devastation_virus` | 1 |
| `0x0809d894` | `scan_equip_chain_list_for_sprite_pikeru_second_sight` | 1 |
| `0x0809d8a8` | `scan_equip_zone_for_final_countdown_sprite` | 3 |
| `0x0809d914` | `scan_equip_zone_for_infinite_cards_lp_display_update` | 4 |
| `0x0809d984` | `run_equip_activation_phase_by_counter` | 48 |
| `0x0809e078` | `dispatch_field_spell_phase_by_display_state` | 11 |
| `0x0809e168` | `tick_duel_field_spell_activation_state` | 57 |
| `0x0809e5e0` | `scan_equip_zone_for_toon_card_activation` | 3 |
| `0x0809e654` | `find_equip_slot_idx_with_entity_id_one` | 3 |
| `0x0809e6a4` | `find_equip_slot_idx_with_entity_id_zero` | 3 |

机械风险: `0x0809d984..0x0809e078`的分配区间1780B/48槽, `0x0809e168..0x0809e5e0`为1144B/57槽; 二者共105槽。已有两个结构化switch表位于`0x0809da00`和`0x0809e1c4`, 正式proposal须读取消费者、核对偶地址MOV pc规则及目标LABEL的实际namespace/source。只读前态已确认142槽均为DefinedData4: 110槽无ref, 30个LP槽与2个switch槽均为operand0 DATA/DEFAULT主ref。gP1LifePoints目标为USER_DEFINED主LABEL id15545; 两个switch目标为scoped ANALYSIS主LABEL id6770与id7145, 均无同址额外alias。后续提案必须区分目标source与reference source, 复用原Symbol对象规范GAS名, 保留30个LP槽的既有DEFAULT引用。上述区间长度用于源文件归属, 不是把Ghidra body当连续范围。无裸块不代表无需检查全部未具名.word、旧plate和disasm后新增残留。

Seg-2有59个既有函数对象; Seg-4含2072B裸块; Seg-5含5块; Seg-6有184槽。这些仅为工作量提示, 不提前指定裸块用途或后段语义处理方案。需要拆子段时, 由该段实际调查给出完整边界后再交driver确认。

### 裸块机械清单 (未分类)

| 地址范围 | 类型 | 大小 | Seg | 当前块头自动标签 | 状态 |
|---|---|---:|---:|---|---|
| `[0x0809e74c,0x0809e8f4)` | ROM_INCBIN | 424 | 2 | `DAT_0809e74c` | ✅ R4反汇编为145指令+25池+4处2B padding，残留0；见§4.02 |
| `[0x080a0b20,0x080a1338)` | ROM_INCBIN | 2072 | 4 | `none` | ✅ Rule 3 / §5.1保留；entry raw/THUMB=0/0、有效内部入口引用0；见§4.04 |
| `[0x080a1720,0x080a190a)` | ROM_INCBIN | 490 | 5 | `DAT_080a1720` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a1950,0x080a1954)` | .byte | 4 | 5 | `none` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a1dd8,0x080a1de8)` | .byte | 16 | 5 | `none` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a1f54,0x080a2000)` | ROM_INCBIN | 172 | 5 | `none` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a2018,0x080a2234)` | ROM_INCBIN | 540 | 5 | `DAT_080a2018` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a38f8,0x080a38fc)` | .byte | 4 | 6 | `none` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a7234,0x080a763e)` | ROM_INCBIN | 1034 | 10 | `DAT_080a7234` | 所属段执行raw/THUMB扫描及消费者分类 |
| `[0x080a764c,0x080a7650)` | .byte | 4 | 10 | `none` | 所属段执行raw/THUMB扫描及消费者分类 |

### 5.1 未引用数据登记表

Seg-1段内无裸块，三个有真实引用的段外表均carve；Seg-2的424B块有真实switch/控制流/literal引用并已按R4完整反汇编；Seg-3段内无裸块，两张有真实引用的段外回调表均carve。Seg-4新增下列1项§5.1登记；Seg-5至Seg-10尚未分类，建档机械测绘不构成零引用结论。

| 地址 | 大小 | Seg | raw/THUMB原始命中 | 引用/分支排除证据 | 已评审结论 |
|---|---|---|---|---|---|
| `[0x080a0b20,0x080a1338)` | 2072B | 4 | entry `0/0`；内部滑窗raw=391、thumb=367 | 758个内部命中均不来自当前asm真实机器行或结构化数据行；Ghidra前后保持2072个DataDB1且无Function/Instruction/DefinedData/ref。55个BL均为出边，块内共享退出不构成入口引用 | Rule 3保留原`ROM_INCBIN`；仅在后续发现真实外部入口引用时重新进入R4 |
