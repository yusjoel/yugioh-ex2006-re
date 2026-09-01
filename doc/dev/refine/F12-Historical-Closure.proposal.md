# Refine Proposal: F12-Historical-Closure

本批为用户明确授权的 module12 历史补漏, 在 Seg10 正式闭环后按涉及地址递增处理. 仅修原登记 7 个自动槽、080952fc 的 8 B 误标代码、20 行旧注释, 加上同一 08095550 注释地址所需的既有表 base LABEL 主标签选择. 不预析 module13, 不扩大到其他模块的历史注释. executor 只写本提案和 closure-* 证据, 未写 Ghidra/正式代码/constants/进度, 未 build/stage/commit.

基线: asm/12_equip_activation_scan.s SHA256=ac38c3b9b8068ba46ad0b070a4f099c1aa66691bdcfca33af06455f43467ad8f; 完整模块范围 [080941c4,0809d718), 38228 B. 原 ROM SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. 前态依据主线程 root-closure-slots-before.json, root-closure-functions-before.json, root-closure-eol-before.json 的真实只读对象数据, 而非由旧 Seg2 文档或 asm 推断 Ghidra 类型. 95554双LABEL及表/case完整前态以 root-closure-switch-before.json 为准; primary切换依据 closure-review-symbol-api.json 中本机Ghidra源码证据. 所有运行证据均在 output/refine-run-20260831-194634/.

## 段测绘

- 7 个历史自动槽: 6 个 DWORD 已有正确 equate, 1 个 DAT 是未建 ref 的 gSpriteAttrBuf 地址. 另 08095550 是已有语义名槽, 仅提升其现有 switch 目标的 global USER_DEFINED LABEL id31014 为primary, 不新增目标LABEL, 不将其计入自动槽.
- 操作计数: EQ=0, REF=2, RENAME=6, full PLATE=19, EOL=8, FUNC_RENAME=0, DISASM=1 range/8 B/3 instructions. NEW=0, REUSE=6 unique symbols. 19 个 full PLATE 覆盖18个原旧注释函数及954e8本批残留槽/EOL所属函数; 20行旧注释中的1577/1591属于同一个94cd4 plate, 2756是95550的EOL.
- 32 B literal数据(7自动槽28 B+1既有具名槽4 B)逐一验证ROM值, 与8 B新反汇编互不重叠. 新反汇编无LDR, 新literal pool=0; 不建立新函数、不改19个现有函数名或body.
- 全模块16709项覆盖38228 B无洞/重叠, 含唯一8 B .byte和4个既有ROM_INCBIN共134 B. 新反汇编后 .byte=0, 四个134 B保留块不变. 完整字节图见closure-module-map.json.

### 前态自动槽与已有依赖槽

| slot | 前态 label | ROM u32 | 当前 Ghidra Data | 计划 | 消费者 |
|---|---|---|---|---|---|
| 0x08095280 | `DWORD_08095280` | 0x00001d5c | /dword, 4 B | RENAME | asm12:2387 |
| 0x080952cc | `DWORD_080952cc` | 0x00001d6c | /dword, 4 B | RENAME | asm12:2417 |
| 0x080952d0 | `DWORD_080952d0` | 0x00001d68 | /dword, 4 B | RENAME | asm12:2426 |
| 0x08095328 | `DWORD_08095328` | 0x00001d68 | /dword, 4 B | RENAME | asm12:2463 |
| 0x0809532c | `DWORD_0809532c` | 0x00001d6c | /dword, 4 B | RENAME | asm12:2466 |
| 0x08095330 | `DWORD_08095330` | 0x00001d54 | /dword, 4 B | RENAME | asm12:2474 |
| 0x08095550 | `sprite_row_tbl2_95550` | 0x08095554 | /undefined4, 4 B | REF | asm12:2749 |
| 0x0809565c | `DAT_0809565c` | 0x0201b870 | /undefined4, 4 B | REF | asm12:2852 |

### 受影响函数入口

本表只列19个完整PLATE对象. Ghidra body_size是地址集合大小, 不包括所有池/已定义case代码, 不等同于连续汇编跨度. 08095220的44 B body保持; 新8 B代码及其两个来源分支原先均没有FunctionContaining.

| addr | current name | Symbol ID | body B | old plate chars | source |
|---|---|---:|---:|---:|---|
| 0x08094290 | `get_clamped_tile_row_count` | 16932 | 48 | 457 | asm/12_equip_activation_scan.s:110 |
| 0x080942dc | `get_monster_slot_entry_ptr` | 3667 | 12 | 368 | asm/12_equip_activation_scan.s:163 |
| 0x080942ec | `get_effect_slot_entry_ptr` | 5615 | 8 | 304 | asm/12_equip_activation_scan.s:178 |
| 0x08094314 | `get_duel_activation_zone_id` | 2042 | 6 | 376 | asm/12_equip_activation_scan.s:209 |
| 0x08094564 | `read_slot_palette_index` | 520 | 18 | 334 | asm/12_equip_activation_scan.s:525 |
| 0x0809463c | `advance_prng_state` | 522 | 26 | 487 | asm/12_equip_activation_scan.s:668 |
| 0x08094664 | `sample_prng_scaled` | 523 | 18 | 444 | asm/12_equip_activation_scan.s:691 |
| 0x080946f8 | `enqueue_duel_phase_sprite_by_side` | 4393 | 62 | 873 | asm/12_equip_activation_scan.s:786 |
| 0x08094750 | `init_duel_phase_display_flag_with_sprite` | 4910 | 60 | 849 | asm/12_equip_activation_scan.s:834 |
| 0x08094c10 | `poll_sprite_seq_until_done` | 4911 | 46 | 671 | asm/12_equip_activation_scan.s:1489 |
| 0x08094c60 | `tick_equip_activation_dispatch_hub` | 16708 | 86 | 1065 | asm/12_equip_activation_scan.s:1516 |
| 0x08094cd4 | `tick_equip_activation_main_sequence` | 16709 | 180 | 1220 | asm/12_equip_activation_scan.s:1595 |
| 0x08094dac | `advance_duel_turn_by_prng_anim` | 4912 | 164 | 1072 | asm/12_equip_activation_scan.s:1712 |
| 0x08094f70 | `update_card_display_index_by_type_rules` | 4285 | 248 | 982 | asm/12_equip_activation_scan.s:1973 |
| 0x08095220 | `dispatch_equip_confirm_phase_by_step` | 16933 | 44 | 583 | asm/12_equip_activation_scan.s:2352 |
| 0x08095380 | `pack_sprite_row_attr_words` | 3671 | 58 | 816 | asm/12_equip_activation_scan.s:2539 |
| 0x080954e8 | `step_prng_anim_frame` | 4394 | 1088 | 590 | asm/12_equip_activation_scan.s:2702 |
| 0x08097150 | `dispatch_to_effect_handler_by_card_type` | 4913 | 56 | 412 | asm/12_equip_activation_scan.s:6520 |
| 0x0809757c | `refresh_slot_activation_display_if_changed` | 7176 | 278 | 1179 | asm/12_equip_activation_scan.s:7080 |

## 数据块分类 (Rule 2/3)

全ROM扫描对每块所有半字边界分别搜索 raw address 和 address|1, 搜索原ROM每个字节偏移. 因而不是只查块首或4B对齐位置. 另由25模块实际Thumb指令编码解码条件跳转、B、BL, 查所有落入块内的目标, 并检查前一有效指令的退出行为. 结果见closure-block-refscan.json和closure-branches.json.

| range | raw / THUMB|1 | 局部控制流 | 分类 |
|---|---|---|---|
| [0x0809437c,0x08094398) 28 B | raw=0, thumb=0 | 无分支目标 | 既有Section5.1保留, effective refs=0 |
| [0x08094c3e,0x08094c60) 34 B | raw=0, thumb=0 | 无分支目标 | 既有Section5.1保留, effective refs=0 |
| [0x080952fc,0x08095304) 8 B | raw=0, thumb=0 | 0x080952b6->0x080952fc,0x080952ba->0x080952fc | DISASM: 两条件分支到块首, 不得登记Section5.1 |
| [0x08095b28,0x08095b3c) 20 B | raw=0, thumb=0 | 无分支目标 | 既有Section5.1保留, effective refs=0 |
| [0x08096eec,0x08096f20) 52 B | raw=1, thumb=0 | 无分支目标 | 既有Section5.1保留, effective refs=0 |

四块无fall-through证据: 9437c前是9437a BX r1; 94c3e前是94c3c BX r0; 95b28前最近指令95b1c BX r1, 之后为对齐/池; 96eec前最近指令96edc BX lr, 之后为对齐/池. 不把池/对齐视为可执行fall-through. 四块分类不变, 不新增carve/disasm到这些范围.
96eec真实raw计数是1, 命中08b16c2f. 独立定位为asm/rom.s:100引入的未压缩6bpp卡图tiles: data/card-image-tiles.s:1322包含graphics/bin/card-images/tiles/tb1316.bin, 记录VA08b16940, 长4800 B. 记录内offset0x2ef的ec 6e 09 08与ROM匹配, 所在对象是像素位数据, 不是地址字段或指针表. 排除依据是资产归属和实际字节用途, 不仅是未4B对齐. 原活动doc:346已记录同一巧合, 本批独立确认effective raw=0, thumb=0. 不把此资产称为压缩数据. 证据closure-raw-collision.json.

### 已结构化跳转表审计

0809524c有10个u32偶地址, 08095554有32个u32偶地址. 两处实际操作码均0x4687=MOV pc,r0, 不是BX r0, 不切换Thumb状态. 仅95554两个既有LABEL的primary对调; 不改两者名称/namespace/source, 不改表值、case标签、表边界、Data类型. 两表base及全部不同case目标做全ROM raw/THUMB|1扫描, 逐目标位置见closure-switches.json.
```text
0x0809524c: count=10, size=0x28, MOV_pc=0x0809523c; values=0x0809530a,0x0809529e,0x080952aa,0x08095292,0x08095284,0x0809528a,0x0809528e,0x08095274,0x08095274,0x08095304
0x08095554: count=32, size=0x80, MOV_pc=0x0809554c; values=0x0809562e,0x08095af0,0x080955d4,0x08095610,0x08095b00,0x08095b00,0x0809562e,0x08095ac4,0x08095ad8,0x08095660,0x08095678,0x080956ce,0x080956a8,0x08095728,0x0809573c,0x080957e0,0x08095820,0x08095830,0x0809578c,0x080957a8,0x080957c0,0x08095620,0x0809563c,0x0809564c,0x080959cc,0x08095a68,0x08095948,0x0809598c,0x080958d0,0x08095914,0x08095880,0x080958ac
```

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (0)

none. 六个DWORD已经有正确唯一equate, 不能重新按EQ创建或改equate引用. 保持名字/值/operand关联; 只有池LABEL改名和EOL替换.

### REF_SLOTS (2)

标准四元组为(slot,value,gas_label,slot_label). 两个REF的前态不同, 按下列分别执行, 不套统一重建策略.
```text
(0x08095550, 0x08095554, switchD_0809554c__switchdataD_08095554, sprite_row_tbl2_95550)
(0x0809565c, 0x0201b870, gSpriteAttrBuf, gsprattrb_9565c)
```
- 08095550: 该池已经是USER_DEFINED主LABEL sprite_row_tbl2_95550(id31015), /undefined4长4, operand0 DATA/USER_DEFINED/primary ref指向08095554. 原槽Symbol、u32、数据类型/长度、equate及完整引用集合保持, 不新增/删除/重建引用. 目标现有两个LABEL: scoped ANALYSIS主LABEL id4244和global USER_DEFINED非主LABEL id31014. 精确复用id31014, 目标唯一写动作是调用其setPrimary(); id4244仅primary由true变false, id31014仅primary由false变true. 两者ID/地址/name/qualified_name/namespace/source/type均保留, 不setName、不setNamespace、不setSource、不createLabel、不delete或合并任何同址标签. 不改case的namespace/name/source. 除此primary切换外, 此槽只设置原审定EOL.
- 0809565c: 原/undefined4长4, equate=[]、refs_from=[]. 改池主LABEL为gsprattrb_9565c, USER_DEFINED, 并建立operand0 DATA/USER_DEFINED/primary ref到0201b870. 目标复用现有USER_DEFINED主LABEL gSpriteAttrBuf(id21747), 不创建别名、不改目标SymbolID/名称/source/primary. RAM当前definedData是/undefined2长2, 必须保持, 不把该RAM目标重定义为4B, 不读取RAM字节作为ROM核验. 其余operand/非目标引用若前态出现差异须先报告, 不大范围清引用.
导出路径: tools/asm-regen/ghidra/ExportRangeToGas.py:506的resolve_word_symbol读取primary USER_DEFINED.getName(); ROM目标要求LABEL, FUNCTION被排除. 95554当前primary为ANALYSIS id4244, 已有USER_DEFINED id31014尚非primary, 导致95550仍导出裸数值. 将现有id31014提升为唯一primary后, 必须导出.word switchD_0809554c__switchdataD_08095554, 不接受裸值或短名回退; 无需修改两个LABEL的名称表示. 9565c的RAM LABEL已有constants/ewram.inc绝对值定义, 接通DATA ref即可按名导出. 两项均无fn+1表达式, 不改exporter, 不新建callback equate. 新代码BL是正常指令调用, 不经过.word的ROM FUNCTION筛选.

#### 08095554 双LABEL完整前后态与引用守卫

dry必须枚举08095554的完整symbols集合, 恰为下列两个LABEL, 不得只看primary或以同址任意USER标签替代指定id31014. 名称、qualified_name和namespace均逐项匹配; 地址均为08095554. 任一字段不符即停写报告.

| id | name | qualified_name | namespace | type/source | primary before -> after |
|---:|---|---|---|---|---|
| 4244 | switchdataD_08095554 | switchD_0809554c::switchdataD_08095554 | switchD_0809554c | LABEL / ANALYSIS | true -> false |
| 31014 | switchD_0809554c__switchdataD_08095554 | switchD_0809554c__switchdataD_08095554 | global | LABEL / USER_DEFINED | false -> true |

目标/pointer长4、u32=0809562e及完整refs前后不变: incoming为95550 operand0 DATA/USER_DEFINED/primary、95546 operand0 PARAM/ANALYSIS/primary、9554a operand1 DATA/ANALYSIS/primary; outgoing为95554 operand0 DATA/DEFAULT/primary到0809562e. 95550原slot id31015的全部符号属性、u32=08095554、/undefined4长4、空equate、incoming READ及outgoing DATA引用的from/to/operand/type/source/primary前后相同. 引用快照的target_primary是目标导航元数据, 仅因该目标primary切换从id4244反映为id31014, 不表示引用被增删重建.

32个table word及30个不同case目标的完整symbols/data/refs在dry保存并逐项比对. 后态仅允许表base上述两个primary布尔值对调, 不新增/删除Symbol对象; 其余表/case对象、数据定义、全部值/偶地址/重复项及引用的from/to/operand/type/source/primary均保持前态. 所有case引用的target_primary也逐字保持, 唯一派生例外是9564c到9565c的原READ引用: 按本提案原定9565c新池主LABEL gsprattrb_9565c/USER_DEFINED核对其导航元数据, 不改变该READ引用本身. closure-plan.json保存目标完整前后态、两对象namespace守卫、原95550槽前后态和32表项/30case前态, 明确上述对象/派生元数据差异; 保存后只读check重复同一合同.

原id4244规范化步骤已被既有id31014 primary提升替代. review源码证据: SymbolDB.java:292-306、367-368、427-430和SymbolManager.java:489-495表明原改名/namespace动作会撞现有id31014并抛DuplicateNameException; CodeSymbol.java:136-160表明setPrimary仅解除旧primary并设新primary, 保留两者名字/source/ID. 这是只读前态及源码支持的修订合同, 未在真实DB试改, 不是实际落地验证.

### RENAME_SLOTS (6)

标准三元组为(slot,slot_label,eol_ascii). 六个旧DWORD均为DEFAULT主LABEL, /dword长4; 每槽保留恰一个原ELIGIB_* equate及空refs_from. 只改池标签为USER_DEFINED并设EOL. 这些RENAME没有LP指针ref, 不沿用Seg10的DEFAULT LP引用模板.
```text
(0x08095280, eligib_act_type_95280, "Byte offset from gP1LifePoints; steps8/9 load the activation type as u16.")
(0x080952cc, eligib_anim_state_952cc, "Byte offset from gP1LifePoints; step3 reads the animation state for the 11..15 split.")
(0x080952d0, eligib_sprite_ctrl_952d0, "Byte offset from gP1LifePoints; step3 states12..15 load the sprite-control argument.")
(0x08095328, eligib_sprite_ctrl_95328, "Byte offset from gP1LifePoints; step1 reads sprite control for display-context initialization.")
(0x0809532c, eligib_anim_state_9532c, "Byte offset from gP1LifePoints; step1 passes animation state minus11 to context initialization.")
(0x08095330, eligib_state_ctrl_95330, "Byte offset from gP1LifePoints; step1 clears state control through the shared store path.")
```

### REF槽 EOL (2; 与六个RENAME合计8)
```text
(0x08095550, "32-entry even-address type table at 0x08095554, indexed by type0..31; dispatch uses MOV pc,r0 and stays in Thumb state.")
(0x0809565c, "Sprite attribute buffer base; type0x17 sets bit1 of byte[base+0x300].")
```
95550旧EOL全文与SHA256采用root-closure-eol-before.json, closure-plan.json.expected已保存. 七个原自动槽EOL在dry阶段逐项读取备份, 设置上述评审全文, 不依据asm省略推断其CodeUnit定义或ref来源.

### FUNC_RENAME (0)

none. 19个Function名称/对象ID/body及全部原incoming保持, 不重命名内部LAB为函数. CSV、registry、4个inventory文件、所有constants保持原字节, 不调用name-sync实写或历史命名脚本. 未修改其他模块的历史plate.

## DISASM计划 (R4)

唯一范围[080952fc,08095304), 原字节00 20 00 f0 53 fc 1b e0. 三条指令完整覆盖8 B, 不包含literal load, 不引入新pool. 原状态为8个独立undefined DataDB/length1, getDefinedDataAt均None, InstructionAt均None, FunctionContaining均None, TMode=1; 不是一个definedData8, 也不是独立函数.
```text
0x080952fc: 0020  movs r0,#0
0x080952fe: 00f053fc  bl init_equip_card_sprite_row_entry
0x08095302: 1be0  b LAB_0809533c
```

| 指令 | 目标实算 | 条件/作用 |
|---|---|---|
| 080952b6, halfword d321 | 080952b6+4+(0x21<<1)=080952fc | unsigned animation state<11 |
| 080952ba, halfword d81f | 080952ba+4+(0x1f<<1)=080952fc | unsigned animation state>15 |
| 080952fe, halfwords f000/fc53 | PC08095302 + ((0x000<<12)|(0x453<<1)) =08095ba8 | BL init_equip_card_sprite_row_entry, r0=0 |
| 08095302, halfword e01b | 08095302+4+(0x1b<<1)=0809533c | B existing shared epilogue |
080952aa..952ba先将state==11送独立路径, 再比较<11或>15. 12..15载入sprite control并调用另一路display dispatch. 新解码路径只处理范围外state, 以r0=0调用现有init_equip_card_sprite_row_entry; 该callee在08095bae把r0保存到r8, 08095bea..95bee检验r8选择零参数路径, 不使用不存在的新参数.
逻辑调用帧来自dispatch_equip_confirm_phase_by_step@08095220的push{r4,lr}, 新块没有prologue; 0809533c pop{r4}, 0809533e pop{r0}, 08095340 BX r0归还原caller. Ghidra当前cases不在该FunctionContaining内, 本批只反汇编8 B, 不扩张44 B函数body, 不CreateFunction或命名一个新callback.
落地限制: 在已验证的8B undefined范围内转为Thumb三条Instruction, 限制反汇编范围/flow, 不顺流重定义callee或epilogue. 保留既有952fc目标LABEL、两条DEFAULT CONDITIONAL_JUMP来源ref. 新CALL从952fe到95ba8, 新JUMP从95302到9533c; 除这两条必要outgoing/incoming外, callee/epilogue对象、旧refs、bytes均保持. 无auto-analysis式扩函数体或扫到相邻pool. 若反汇编输出额外DAT/POOL/函数或越界, 停止并报告, 不自动扩补漏范围.


Final read-only dependency guards (root-closure-callee-before.json and root-closure-branch-target-before.json):
- 0x08095ba8 is the existing USER_DEFINED Function init_equip_card_sprite_row_entry, Symbol id4286, body194 B, body SHA256 fa7a31b9116d521ab430397d0490db7a69a6f640cd26e1690fcb2f09e6955fd7. Preserve its identity, body, old776-character plate, empty EOLs and both existing DEFAULT/UNCONDITIONAL_CALL/operand0/primary incoming references from 0x0804d1a6 and 0x08086092. Only add the decoded CALL from 0x080952fe; this callee is not a PLATE target in this closure.
- 0x0809533c is the existing 2-byte `pop {r4}` instruction, inside the original 0x08095220 body, with the existing dynamic DEFAULT LAB label. Preserve its instruction, symbol and eight DEFAULT/UNCONDITIONAL_JUMP/operand0/primary incoming references from 0x0809527e, 0x08095288, 0x0809529c, 0x080952a8, 0x080952c8, 0x08095308, 0x080952e8 and 0x080952fa. Only add the decoded JUMP from 0x08095302.
- The new instruction references are DEFAULT, matching normal disassembly flow references; they are not the USER_DEFINED DATA references used for REF_SLOTS. No prior reference may disappear or change source, type, operand or primary state. The 15 database-file hashes remained unchanged during these read-only observations.

## PLATE (19, full rewrite, ASCII <=500)

每项使用主线程真实Ghidra旧全文与hash作为前态守卫, closure-plan.json保存expected_old_text/expected_function; 不做字符串盲替、动态截断或临时生成新正文. 当前19旧全文已与asm原plate逐字匹配. 19篇新plate全部ASCII, 最长485字符. 新正文未引用FUN/DAT/DWORD/PTR等旧自动名.

#### 0x08094290 get_clamped_tile_row_count
source: asm/12_equip_activation_scan.s:110; confidence=high; chars=283; expected_old_sha256=b679e2d425f3f9d13e1b9ab19eeec2277ac062d6c26e9446c98b2c3387350ab9
```text
No inputs. Read signed phase at gEquipEffectZoneBase+4. Return 0 if phase<=5. Otherwise start with n=1; phase 7..38 sets n=phase-6, and phase 40..71 sets n=phase-39. Return unsigned min(n,word[base+0xc]). Thus phase 6,39 and values above71 use n=1. Pure read; no bounds-state writes.
```

#### 0x080942dc get_monster_slot_entry_ptr
source: asm/12_equip_activation_scan.s:163; confidence=high; chars=200; expected_old_sha256=509e0cd35a74c0f264a0a72e39f0f3e4e85d14423defc81e0668f5da4a63bb34
```text
No inputs. Read index=word[gEquipEffectZoneBase+8] and return gEquipEffectZoneBase+0x10+4*index. Does not dereference the selected entry, increment the index or check bounds. Pure address calculation.
```

#### 0x080942ec get_effect_slot_entry_ptr
source: asm/12_equip_activation_scan.s:178; confidence=high; chars=177; expected_old_sha256=1fe4449fcc6d3cfd88c87acc5291a40e9522fe8c46c38f9edfad91bd565d4bf9
```text
r0=slot index. Return gEquipLpZoneEntryBase+4*index using 32-bit address arithmetic. The selected entry is not dereferenced and the index is not range-checked. No memory writes.
```

#### 0x08094314 get_duel_activation_zone_id
source: asm/12_equip_activation_scan.s:209; confidence=high; chars=197; expected_old_sha256=007655ad3e73341f9d6a3c8b7e63bb1f4f794b62b122b068980cc13bc2f0f3df
```text
No inputs. Return the u32 at gEquipEffectZoneBase+0xc. Three-instruction leaf with no writes; the base comes from the existing gEquipEffectZoneBase literal. Used by activation-zone display callers.
```

#### 0x08094564 read_slot_palette_index
source: asm/12_equip_activation_scan.s:525; confidence=high; chars=224; expected_old_sha256=cae31922a6c2592764f3c2e14933dcf9aebeefe3453736ffcd49537f4dc15135
```text
r0=slot index. Return the high byte of the halfword at gEquipEffectZoneBase+0x410+2*index, as an unsigned value 0..255. No bounds check or memory write. Used by reset_slots_above_palette_index and check_slot_palette_nonzero.
```

#### 0x0809463c advance_prng_state
source: asm/12_equip_activation_scan.s:668; confidence=high; chars=291; expected_old_sha256=cf5956fb193728e3ebf7b39fb7d6ad18727ca59ffbb84e1a50640f1ad660c484
```text
No inputs. Advance the u32 seed at gP1LifePoints+0x1ce0: seed=seed*LCG_MUL_343FD+LCG_INC_269EC3 modulo 2^32. Store the new seed and return (seed>>16)&0x7fff, in range0..32767. Modifies only the seed word. Direct callers are the scaling wrapper and two random-draw/display sequence functions.
```

#### 0x08094664 sample_prng_scaled
source: asm/12_equip_activation_scan.s:691; confidence=high; chars=276; expected_old_sha256=b9b313b8ee7ec7b7fd4855f93752807e758ee8e5c2d666c25257a9762a3750c1
```text
r0=scale. Call advance_prng_state, multiply its 15-bit result by scale using a 32-bit product, then return product>>15. No input range check; multiplication can wrap for large scale. Advances the shared seed. For positive scale with no product overflow, result is below scale.
```

#### 0x080946f8 enqueue_duel_phase_sprite_by_side
source: asm/12_equip_activation_scan.s:786; confidence=high; chars=359; expected_old_sha256=6db2c17a57aa5c5fb13f3904c1e3f2dd3adf4c1a07193a6b608316cf2421aa59
```text
No inputs. If gP1LifePoints+P1LP_BACKUP_DST_OFF is not 0xffff, return. Also return when check_player_side_condition is nonzero. Otherwise copy the timer at P1LP_TIMER_OFF to the backup word and enqueue sprite type 0xb or SPRITE_ATTR_DUEL_PHASE_P2 according to gDuelCardCtxBase+4 being zero or nonzero. The other three enqueue arguments are zero. Returns void.
```

#### 0x08094750 init_duel_phase_display_flag_with_sprite
source: asm/12_equip_activation_scan.s:834; confidence=high; chars=323; expected_old_sha256=d6c07de3f1c67f238a54c7fe1ed8319a05af5fd1a10e8942b2bfa4884699db5d
```text
r0=player. Return if word[gP1LifePoints+LP_DISCARD_ZONE_OFF] is nonzero; otherwise set it to1. Store display variant2 if player equals word[gDuelCardCtxBase+4], else1. Enqueue type0x23 for player0 or SPRITE_ATTR_DUEL_PHASE_P2_B otherwise, with remaining arguments (0xb,0,0). Writes the guard and variant once; returns void.
```

#### 0x08094c10 poll_sprite_seq_until_done
source: asm/12_equip_activation_scan.s:1489; confidence=high; chars=388; expected_old_sha256=61e18541e97dccd63bfc63b4a27988d97f6a9c7407e4342020dee4b890b0ad1c
```text
r0 is saved as a loop-continuation flag. The first call is return_one_leaf, which returns1 in this ROM, so this entry immediately returns without reading a frame or writing the sprite sequence. The dormant loop would read four halfwords from return_zero_leaf, submit them, and test the saved flag only after that work. The supplied flag is not an initial null-pointer guard. Returns void.
```

#### 0x08094c60 tick_equip_activation_dispatch_hub
source: asm/12_equip_activation_scan.s:1516; confidence=high; chars=405; expected_old_sha256=41ad5744c5a392d85d9b8d37f5b3689bbe335de9c867b9192122c19ee09b7392
```text
No inputs. Check Last Turn in current-player zone0xb; if present and the subphase dispatcher returns0, return0. Otherwise index EQUIP_PHASE_FN_TABLE_ROM by the shared main phase. A null function pointer returns1. Invoke a nonnull pointer; on nonzero result clear CARD_PLAY_PHASE_CTR_OFF and increment main phase. All nonnull-pointer paths return0. No player-stride multiplication precedes the chain query.
```

#### 0x08094cd4 tick_equip_activation_main_sequence
source: asm/12_equip_activation_scan.s:1595; confidence=high; chars=413; expected_old_sha256=1b56b16c1bb8c5461b628c08f8284b43aed880163992e3f6f3243c7896149d56
```text
No inputs. Return1 for context mode3, active sprite-busy gate or discard guard. Run six UI/target/confirm update checks until one returns nonzero; store (result==0) at gP1LifePoints+0x1d10. Nonzero returns0. On zero, a nonzero normal-summon check returns1; otherwise call tick_equip_slot_activation_step for player context2, or tick_equip_activation_dispatch_hub, and return0. Both final call results are ignored.
```

#### 0x08094dac advance_duel_turn_by_prng_anim
source: asm/12_equip_activation_scan.s:1712; confidence=high; chars=404; expected_old_sha256=814295519f625919318a3013499b9a77dd8f661a5e08e0d6bcf0503a0fcc3896
```text
No inputs. Index DUEL_TURN_FN_TABLE_ROM by shared turn state. A null entry copies display variant and the selected player word into duel context, then returns1. For a nonnull entry, a required PRNG-animation step returning0 returns1; a nonzero animation-event result returns0. Otherwise invoke the entry; a nonzero result advances turn state and clears the card-play counter. This dispatch path returns0.
```

#### 0x08094f70 update_card_display_index_by_type_rules
source: asm/12_equip_activation_scan.s:1973; confidence=high; chars=451; expected_old_sha256=a62ba11b3055fe079ddafb8ce49da555e8dbeb1abc9ce17ee28d632507f43ca8
```text
r0=24-byte card entry; r1=entry index (>0 enables the previous-entry test). Require entry side XOR its flip bit to equal current player. Field6=23 writes index0x3a, then0x21 if flags0x30 are clear; field9==1 plus prior-entry/CID/entity tests enable0x22. Field6=22 writes0x39, then0x1f when those flags are clear; opposite cached player and field9==5 enable0x20. All writes use value1. Returns void; caller supplies the index from gSpriteAttrBuf+0x310.
```

#### 0x08095220 dispatch_equip_confirm_phase_by_step
source: asm/12_equip_activation_scan.s:2352; confidence=high; chars=429; expected_old_sha256=92d43bb83936044591e5926476099eeb3b9a23aaa54f61623b048796baf53288
```text
No inputs. Read ELIGIB_ACT_TYPE_OFF from gP1LifePoints; steps1..10 select ten even-address cases via MOV pc,r0. Other steps clear ELIGIB_STATE_CTRL_OFF. Cases initialize/tick equip display using the shared entry frame. In step3, animation state outside11..15 calls init_equip_card_sprite_row_entry(0); state11 and12..15 use distinct paths. All cases return through the saved r4/lr epilogue at 0x0809533c; no extra callback frame.
```

#### 0x08095380 pack_sprite_row_attr_words
source: asm/12_equip_activation_scan.s:2539; confidence=high; chars=342; expected_old_sha256=e882514bf54c6445ac889c8cdbd9dec391f0fd8c53b2c16ddeaab89f6335e3e5
```text
r0-r3 supply four low16 fields. Build two local words: low16(r0)|(r1<<16) and low16(r2)|(r3<<16). Submit them with submit_sprite_row_data(low16(r0),-1,sp+2,6), then restore the local stack and forward its r0 result. The sp+4 intermediate is masked twice so no old stack bits survive. The pointer sp+2 is not an input stride or fifth argument.
```

#### 0x080954e8 step_prng_anim_frame
source: asm/12_equip_activation_scan.s:2702; confidence=high; chars=430; expected_old_sha256=2b4b12d8b60eb95a6b34d3715736b578c9b00cd05a60046df69b4ff352c77aa5
```text
No inputs. If gSpriteAttrBuf+0x300 bit0 is set, return1. Otherwise dequeue a record; a nonzero result dispatches its type through32 even-address MOV pc cases. Cases update sprite/effect/LP state; most return1, while type1,4,5 or out-of-range type set LP_DISPLAY_STATE_OFF=1 and return0. With no record, return1 only when read_prng_entry_flag_clear is nonzero and LP display state is zero; otherwise set that state to1 and return0.
```

#### 0x08097150 dispatch_to_effect_handler_by_card_type
source: asm/12_equip_activation_scan.s:6520; confidence=high; chars=372; expected_old_sha256=1047da44473c9c2516a9d85651ae1f59513ae1a0aafb9e1b5adb3e22bc6367b2
```text
r0=context; r1=type key; r2=sub-parameter. Scan18 records in EQUIP_ACTIVATION_HANDLER_TABLE, indices0..17 with stride0x10. Compare the full r1 word to record+0. On the first match invoke the function pointer at record+0xc with the original (context,type,sub-parameter), then return. No match returns without dispatch. No key truncation or handler-null check. Returns void.
```

#### 0x0809757c refresh_slot_activation_display_if_changed
source: asm/12_equip_activation_scan.s:7080; confidence=high; chars=485; expected_old_sha256=ac3a101ce7f13d0acf6c864ecaaf1fe52ada0cc02c4617a61b347330d827a3b4
```text
No inputs. Build a 0x44-byte slot-state image and compare with gEquipChainSlotRefs+0xec. A mismatch in either leading word clears cached mode/chain-active, sets chain step1 and returns1. Further state, eligibility and EARTHBOUND_INVITATION_CID checks detect changes. No change returns0. On change, clear mode/chain-active; guard returning0 enqueues the slot sprite and sets step1, otherwise set step2 and request card display/slot-bit updates. Return1; this is not a cache-pointer API.
```

## 消费者证据与旧自动名闭合 (R6/C8)

本批不从旧plate反推事实. closure-consumers.txt保存实际本体, closure-call-relations.json保存按机器码BL确认的关系. 对module13只查既有正式名称和调用边, 未展开其本体分析. 旧名字的当前归属表如下; data项显示当前池名, 95a18是已有内部LABEL, 不是函数.

| 旧地址 | 当前正式函数/数据符号 | 当前来源 |
|---|---|---|
| 0x0801e984 | `tick_duel_field_main_frame` | asm/01_vija_scene_text.s:4112 |
| 0x08031668 | `shuffle_player_hand_list` | asm/02_text_lp_fieldspell.s:11904 |
| 0x08031d44 | `build_hand_zone_display_slots_shuffled` | asm/02_text_lp_fieldspell.s:12902 |
| 0x08037c20 | `shuffle_hand_by_player_deck_flag` | asm/03_equip_chain_hand.s:3969 |
| 0x0803c3b4 | `tick_duel_anim_event_hub` | asm/03_equip_chain_hand.s:13801 |
| 0x08057874 | `tick_equip_slot_score_fill_display_seq` | asm/06_equip_eligibility_b.s:10137 |
| 0x08057c28 | `tick_equip_banisher_zone_display_step` | asm/06_equip_eligibility_b.s:10654 |
| 0x080598d8 | `tick_equip_atk_zone_sprite_display_seq` | asm/06_equip_eligibility_b.s:15142 |
| 0x08059b4c | `tick_equip_neo_daedalus_slot_display_seq` | asm/06_equip_eligibility_b.s:15489 |
| 0x08093660 | `init_duel_puzzle_field_and_hand_display` | asm/11_effect_slot_puzzletext.s:30989 |
| 0x0809431c | `gequipeffzone_931c` | asm/12_equip_activation_scan.s:214 |
| 0x0809457c | `reset_slots_above_palette_index` | asm/12_equip_activation_scan.s:544 |
| 0x0809474c | `sprite_attr_p2_974c` | asm/12_equip_activation_scan.s:829 |
| 0x0809479c | `sprite_attr_p2b_979c` | asm/12_equip_activation_scan.s:875 |
| 0x08094c10 | `poll_sprite_seq_until_done` | asm/12_equip_activation_scan.s:1489 |
| 0x08094c8c | `last_turn_9c8c` | asm/12_equip_activation_scan.s:1538 |
| 0x08094cc8 | `card_play_phase_9cc8` | asm/12_equip_activation_scan.s:1568 |
| 0x08094cd4 | `tick_equip_activation_main_sequence` | asm/12_equip_activation_scan.s:1595 |
| 0x08095248 | `eq_confirm_jumptbl_95248` | asm/12_equip_activation_scan.s:2374 |
| 0x080953bc | `sprite_hi_mask_953bc` | asm/12_equip_activation_scan.s:2569 |
| 0x080953c0 | `sprite_lo_mask_953c0` | asm/12_equip_activation_scan.s:2571 |
| 0x08095550 | `sprite_row_tbl2_95550` | asm/12_equip_activation_scan.s:2756 |
| 0x08095a18 | `LAB_08095a18` | asm/12_equip_activation_scan.s:3354 |
| 0x0809717c | `equip_act_tbl_717c` | asm/12_equip_activation_scan.s:6543 |
| 0x080975b0 | `gequipchainrefs_75b0` | asm/12_equip_activation_scan.s:7107 |
| 0x0809e6f4 | `dispatch_equip_activation_state_by_subphase` | asm/13_equip_placement.s:2103 |
| 0x080a06bc | `tick_equip_display_phase_by_state_code` | asm/13_equip_placement.s:6231 |
| 0x080a0b14 | `tick_equip_slot_activation_step` | asm/13_equip_placement.s:6857 |
| 0x080bb414 | `dispatch_equip_activation_full_sequence` | asm/15_equip_target_summon_zoom.s:7204 |
| 0x080d2ef4 | `tick_zone_card_list_view` | asm/17_duelfield_pack_frame.s:13248 |
| 0x0810e5c8 | `invoke_r0` | asm/23_sound_cardlist_libc.s:15334 |

### 原20行逐项覆盖

| 原行 | 实际归属 | 正文/关系订正 |
|---|---|---|
| 108 | 0x08094290 `get_clamped_tile_row_count` | 4290真实区间7..38/40..71, 其他>5用1, 最后unsigned min; 旧区间/回退错误. tick_zone_card_list_view真实2处BL. |
| 161 | 0x080942dc `get_monster_slot_entry_ptr` | 42dc仅index地址计算, 不写count. 三个旧caller均已确认真实BL, 不保留旧indeg=26断言. |
| 174 | 0x080942ec `get_effect_slot_entry_ptr` | 42ec indexed base+4, 旧caller目标现名dispatch_equip_activation_full_sequence, 有2处BL. |
| 207 | 0x08094314 `get_duel_activation_zone_id` | 4314读取gEquipEffectZoneBase+0xc; 旧pool已名gequipeffzone_931c, 两个caller关系真实. |
| 523 | 0x08094564 `read_slot_palette_index` | 4564返回palette halfword高8位; 457c现名reset_slots_above_palette_index, BL94586. |
| 666 | 0x0809463c `advance_prng_state` | 463c旧reset caller关系错误: 457c只读/改palette, 无PRNG调用. 实际direct callers为sample_prng_scaled、tick_random_draw_display_seq、tick_prng_advance_display_op38_seq. |
| 689 | 0x08094664 `sample_prng_scaled` | 4664 32-bit product右移15, 不声称对任意输入均匀或无溢出. 三个shuffle caller关系真实. |
| 776 | 0x080946f8 `enqueue_duel_phase_sprite_by_side` | 46f8没有r0=0实参承诺; check_player_side_condition无输入. enqueue其他三个参数均0, 不是旧写法的(0xb,0,0). |
| 831 | 0x08094750 `init_duel_phase_display_flag_with_sprite` | 4750输入player, 一次guard和variant2/1, sprite0x23/0x8023. 两旧caller正式名和BL已核对. |
| 1482 | 0x08094c10 `poll_sprite_seq_until_done` | 4c10先调用当前return_one_leaf=1立即返回; 旧空指针早退/运行时持续loop解释不成立. 93660现名有真实BL. |
| 1513 | 0x08094c60 `tick_equip_activation_dispatch_hub` | 4c60不乘player stride; LastTurn链存在且subphase=0先返回0. NULLcallback才返回1; callback非0推进phase并清counter. |
| 1577 | 0x08094cd4 `tick_equip_activation_main_sequence` | 94cd4旧caller94c10错误: poll_sprite_seq_until_done不调用本函数, 当前Ghidra incoming也为0. 删除错误caller/indeg断言. |
| 1591 | 0x08094cd4 `tick_equip_activation_main_sequence` | 与1577同一94cd4 plate. 9d96实际BL tick_equip_slot_activation_step, 9da0 BL本模块hub, 两结果均忽略并返回0. |
| 1703 | 0x08094dac `advance_duel_turn_by_prng_anim` | 94dac区分frame step=0返回1/event非0返回0; 末端NULLentry写variant+selected player word, 不颠倒读写方向. |
| 1971 | 0x08094f70 `update_card_display_index_by_type_rules` | 4f70的旧FUN95a18是step_prng_anim_frame内部LABEL. r1来自gSpriteAttrBuf+310, 不是LP+310. field9=1是允许继续的条件, 不是提前退出条件. |
| 2346 | 0x08095220 `dispatch_equip_confirm_phase_by_step` | 5220的0x4687为MOV pc而非BX; 十个case已结构化, 不再声称位于ROM_INCBIN. 8B遗留路径按本提案补反汇编. |
| 2537 | 0x08095380 `pack_sprite_row_attr_words` | 5380两半字完整覆写两个local words; submit第3参数是SP+2指针, 不是原r2+2 stride; 不存在第5参数base_attr. |
| 2756 | 0x080954e8 `step_prng_anim_frame` | 95550是EOL, 表count=32(type0..31), 不是30. 原槽ref已USER; 目标primary为ANALYSIS id4244, 仅提升已有global USER id31014为primary并按名导出, 保留两个LABEL名字/source. |
| 6518 | 0x08097150 `dispatch_to_effect_handler_by_card_type` | 7150 cmp index,#0x11配BLS形成0..17共18条, 非17条; type key未truncate; returns void. |
| 7078 | 0x0809757c `refresh_slot_activation_display_if_changed` | 757c入口r0被覆盖, 无cache指针参数. 两个leading word mismatch直接清mode/chain-active并step1返回1; 后续change还分guard0/非0两路. |

新plate对重要消费者的直接证据:
- asm12:110-139证明phase signed<=5早退、两个unsigned区间、r2默认1及与+0xc的unsigned min. 不是旧注释的值本身clamp. 对负phase同样先返回0.
- asm01:5399-5400的return_one_leaf实际为movs r0,#1; BX lr; asm12:1491/1504先走该调用. dormant frame读取路径因此不执行. 不改变其他模块stub或plate.
- asm12:1973-2101完整field6/field9/state tests; 3354-3356通过内部95a18读r1=[gSpriteAttrBuf+310]后BL4f70. 只按现有index用途说明, 不建立新函数.
- asm12:2539-2566保存r0-r3低半字, 两个mask依次删除旧stack半字; 0x466a是MOV r2,sp, 随后ADD r2,#2, 故传入SP+2. call后r0不被改, return透传.
- asm12:2702-2753与3475-3491证明dequeue结果、32项table和return0/1分流; case17在2852-2859将gSpriteAttrBuf+300 bit1置位, 3461完成store. 本体其他cases见closure-consumers.txt, 不是从旧30-entry EOL推导.
- asm12:6520-6552证明18x16B查表、entry+0xc pointer和3实参透传. 表范围[09e47560,09e47680), 下一地址正是已验证的Seg10两CID表, 不切割段外ROM. invoke_r3@0810e5d4实际BX r3, 无额外参数生成.
- asm12:7080-7246证明无输入、0x44B状态图、首两word早退及后续guard分路; 080975b0当前池值0201bb90=既有gEquipChainSlotRefs, 不再叫cache参数区域.

### CID 核对

正文涉及Last Turn、EARTHBOUND_INVITATION_CID, 以及type-rules消费者的NEGATE_ATTACK_CID均重查本地ROM/card-stats/名字密码. data.md严格按password/name/SO/CID/little-endian-CID列解析, 只匹配逻辑CID列. 多图记录保存在closure-cids.json, 不用全行首次字符串命中.

| CID | 逻辑卡名 | password | card-stats行 / ROM CID addr | data.md行 |
|---|---|---|---|---|
| 0x12c4 | Negate Attack | 14315573 | 8439 / 0x0981a168 | 635 |
| 0x151e | Last Turn | 28566710 | 14224 / 0x0981c7a6 | 1078 |
| 0x177a | Earthbound Spirit's Invitation | 65743242 | 20334 / 0x0981f00a | 1543 |

## 新增 constants / 全局

none. 全6002条现有equate逐项求值成功, 无未解析项. 四个offset与gSpriteAttrBuf各有且只有一个同值定义, 值和base/单位均吻合, 不创建同义常量. switch复用既有LABEL, 不创建ROM equate. 新slot标签只是池标签, 不增加数据对象.

| REUSE | value | source | 用途/单位 |
|---|---|---|---|
| `ELIGIB_STATE_CTRL_OFF` | 0x00001d54 | constants/ewram.inc:419 | gP1LifePoints相对byte offset |
| `ELIGIB_ACT_TYPE_OFF` | 0x00001d5c | constants/ewram.inc:421 | gP1LifePoints相对byte offset |
| `ELIGIB_SPRITE_CTRL_OFF` | 0x00001d68 | constants/ewram.inc:422 | gP1LifePoints相对byte offset |
| `ELIGIB_ANIM_STATE_OFF` | 0x00001d6c | constants/ewram.inc:423 | gP1LifePoints相对byte offset |
| `gSpriteAttrBuf` | 0x0201b870 | constants/ewram.inc:378 | 既有RAM byte buffer base |
| `switchD_0809554c__switchdataD_08095554` | 0x08095554 | asm12:2757, 既有global USER LABEL id31014; root-closure-switch-before.json | 32项u32偶地址table base, 仅setPrimary提升id31014, 原scoped ANALYSIS id4244保持且转非primary |

## carve计划 (R7)

none. 本批唯一需处理的8B裸数据实为指令; 四个既有Section5.1块保留. 不编辑asm/rom.s或导出器, 不重定义未压缩卡图资产.

## Section 5.1 登记/复核

保持四条旧登记: 9437c/1c, 94c3e/22, 95b28/14, 96eec/34. 真正引用均0, 无任何段内分支落点, 无fall-through. 96eec需保持raw=1但仅像素巧合/effective=0的准确措辞. 不新增登记, 不将有两条真实分支引用的952fc放入此节.

## 落地守卫与全模块 C13 清单

执行操作按closure-plan.json.operation_order的地址递增顺序. 所有前态先整体dry核验成功, 再写入. 已获用户授权此补漏范围, 不要求新的重复许可; 若实际对象/字节与下列guard不符, 停写并报告具体差异, 不放宽guard或扩大范围.

| guard | 必须保持/最终验证 |
|---|---|
| 原值和布局 | 8个slot u32、8B解码、整个38228B映射与ROM一致; 跳转目标和值不变. 当前源hash必须与本提案基线相同. |
| 6 RENAME | 每槽/dword4、单个指定ELIGIB equate、空outgoing refs保留; 仅新池名和审定EOL. 不新增equate/ref. |
| 9565c REF | /undefined4池长度/bytes保持; 唯一新增operand0 DATA/USER_DEFINED primary->0201b870; target id21747已有LABEL保留, RAM /undefined2不变. |
| 95550 REF | dry精确核对目标完整双LABEL集合及REF节全部前态; 仅id31014.setPrimary(), id4244/31014的ID/地址/name/qualified_name/namespace/source/type不变且primary对调. slot id31015/u32/definedData/equate/原完整USER ref不变, 不重建引用; 32table words/30case及全部symbols/data/refs保持, 仅目标两primary例外. 后态唯一primary为id31014, .word必须为现有GAS全名, 不接受裸值/短名. |
| DISASM | 原8个undefined length1转为精确3Instruction(2/4/2 B), TMode仍1; 保留952fcLABEL和两个旧branch refs. 不创建函数/扩body/改池; 新CALL与JUMP目标精确. |
| PLATE | 19个旧全文/hash/Function name+id+body+incoming精确匹配; 设置19个审定完整ASCII正文<=500, 禁止substring-only留下超长旧文. after全文逐字一致. |
| EOL | 仅8个slot设置审定ASCII EOL; 95550旧EOL完整guard匹配. 其他EOL和注释保持, 不批量清空. |
| C13-before | 7个自动定义=6DWORD+1DAT; 20个旧注释行; 1个8B.byte; 四个Section5.1 ROM_INCBIN. 新发现对象必须显式报告. |
| C13-after | 自动标签定义/旧FUN,SUB,DAT,DWORD,PTR,UNK注释均0, .byte=0, ROM_INCBIN恰4块134B且地址/字节不变. LAB与已结构化switch/case标签属于控制流标签, 不计待消灭literal自动名. |
| 范围与同步 | 正式25模块只允许asm12在19plate/8slot/8B解码处改变; 95554数据库仅切换既有两LABEL的primary, 不改其名称表示, 95550按既有GAS全名导出. 其他24模块、constants、rom.s/includes、CSV/registry/4inventory全不变. 无函数改名无需name-sync. |
| 验证 | 保存后只读重开核对对象/plate/ref/三Instruction; 全量标准导出与注入/split/ROM导出/build由fixer执行, 最终byte-identical及主线程独立C13验收不可省略. executor未执行build. 禁止stage/commit. |

## 自检

closure-selfcheck.json与closure-projected-module.s仅为静态提案预演, 不是正式落地或PASS. 已确认19旧plate源码全文与真实Ghidra前态一致; 新19plate ASCII且最长485; 8个slot标签合法且无新增碰撞; 6002 constants求值完整; slot/新BL与条件分支目标按ROM验证; 新8B没有literal load或pool. 预演结果自动label/自动符号/旧自动名注释/.byte均0, 四个ROM_INCBIN的(起点,size)精确不变. 预演完整模块字节仍与原ROM一致. 不据此代替reviewer独立C1-C13或fixer byte-identical流程.

Mode A #1仅修95554目标动作、完整前后态/引用守卫及相关说明, 同步closure-plan.json与closure-selfcheck.json的hash/证据来源. 8槽地址/值/池名/分类、6RENAME的原equate与空refs、两REF的池引用合同、19PLATE全文/旧hash、8EOL、DISASM三指令/函数body合同、4块Section5.1及NEW0/REUSE6/FUNC_RENAME0/carve0均未改. 原静态预演证据保留, 本轮仅做清单落实与diff自检, 未重跑该预演、未重新评分、未运行Ghidra/build, 未落地; 复审PASS后方可进入Mode B.

## 求助

none. 全部操作有数值、消费者和只读对象证据. 96eec像素巧合已独立分类, 不存在需扩大范围的真实引用. 95a18已确认是内部LABEL, 不猜造函数名. 未触及module13语义分析或其他未授权历史范围.
