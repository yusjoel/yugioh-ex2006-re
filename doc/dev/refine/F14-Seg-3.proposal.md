# Refine Proposal: F14-Seg-3  [0x080aa120..0x080aba78)

## 范围与冻结输入

- 正式段范围: `asm/14_equip_ai_scoring.s [0x080aa120,0x080aba78)`, 6488 bytes.
- 当前权威全模块前态: `root-f14-seg2-independent-post-v2.json`. 本提案不采用 Seg-1 或 Seg-2 落地前的旧模块 map.
- 段初始前态: `root-f14-seg3-initial-baseline.json`, 5 Functions, 116 current words, 5 raw blocks, 6488 byte units.
- 补充只读前态: `root-f14-seg3-supplement-prestate.json`, 34 non-NULL Function rows, 116 current words, 453 rich address states, 6488 byte units. `.json.db-gate.json` 证明 15 个物理 DB 文件查询前后 hash 完全相同.
- 源码与 DB 备份: `root-source-baseline-f14seg3.json`, `root-f14-seg3-db-backup.json`.
- 完整槽合同: `F14-Seg-3.slots.tsv`, 206 rows. Function/PLATE 合同: `F14-Seg-3.plates.tsv`, 5 rows.
- R4 地址级合同: `f14-seg3-r4-cfg-map.json`, SHA256 `0ef41331aac5d2f562f123d5bf7013dbe94cfeb4a96c178a0d75183f91c5b66e`.
- Root 独立 opcode/partition gate: `root-f14-seg3-r4-static-gate.json`, PASS.
- 本段不修改段外源码. Naming registry, `doc/dev/naming-proposals.csv`, 以及 canonical inventories `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md` 只按 3 个批准 rename 和 4 个 body length 变化同步. `tools/ghidra-labeling/ghidra-functions.*` 是 5213/5123 的 legacy stale copies, 不属于同步真源且保持不动.

## 段测绘

### Function 入口

| entry | current | final | action |
|---|---|---|---|
| `0x080aa120` | `dispatch_equip_entry_state_by_phase_index` | `dispatch_equip_mode2_phase_by_combined_index` | rename + R4 body extend |
| `0x080aa77c` | `dispatch_equip_entry_slot_phase_c` | `dispatch_equip_mode3_phase_by_combined_index` | rename + R4 body extend |
| `0x080aaf54` | `exit_equip_phase_oob_epilogue` | same | body preserve + incoming/PLATE update |
| `0x080aaf64` | `dispatch_equip_entry_slot_phase_d` | `dispatch_equip_mode4_phase_by_combined_index` | rename + R4 body extend |
| `0x080ab200` | `dispatch_equip_entry_slot_by_mode` | same | remove 2-byte erroneous Data ownership + PLATE projection |

三项 rename 的证据均为 high confidence:

- `0x080ab200` 在 `asm/14_equip_ai_scoring.s:5996-5998,6013-6022` 通过 `ldrh [state+0x12]; lsl #23; lsr #29` 提取 mode bits `[8:6]`, 再分别调用 mode 1, 2, 3, 4 dispatcher.
- `0x080aa120`, `0x080aa77c`, `0x080aaf64` 分别从 state bytes `+0x13/+0x14` 计算同一 `combined_index`, 并通过各自 10, 10, 8 项 phase table 跳转.
- 三个新名字统一为 `dispatch_equip_modeN_phase_by_combined_index`, 与已完成的 `dispatch_equip_mode1_phase_by_combined_index@0x080a9734` 同构.

### word 与 raw 块

- 当前 words 共 116: 88 个自动 `DWORD_` slots, 28 个已有无 source label 的 switch table words. 全部进入 slots TSV.
- R4 新 literal pools 共 90 words. final words 共 206.
- 当前布局: 1285 InstructionDB / 2658 code bytes; 116 words / 464 bytes; 5 raw blocks / 3334 bytes; 32 padding bytes. 总计 6488 bytes, 无空洞或重叠.
- `0x080ab278` 是 4-byte `/dword` `d0e40102`, 值 `gEquipZoneRankState`. 当前 `dispatch_equip_entry_slot_by_mode` body 的局部 range `[0x080ab238,0x080ab27a)` 错误包含其前 2 bytes. 本提案仅把该受影响局部 range 收到 `[0x080ab238,0x080ab278)`; 整个 23-range Function 仍延续到 `0x080aba50`, final size 2424 bytes / SHA256 `64c7172d01bc2be293ae7c27e9ecf51b8cfb0f79890fa948a318be05f04bf940`. `0x080ab278` Data unit, `READ 0x080ab24c -> 0x080ab278`, source symbol, EOL 和 bytes 保持.

## 数据块分类, Rule 2/3

完整 1667 个 even candidate 的 raw/THUMB|1 扫描见 `f14-seg3-full-rom-refscan.json`, ROM SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`.

| 块 | full-ROM raw / THUMB scan | CFG 证据 | 判定 |
|---|---|---|---|
| `aa184..aa768`, 1508B | raw=11, THUMB=1. 10 raw hits 来自 table `aa15c..aa180`; raw `aa2fe@09f9f968` 与 THUMB `aa195@08acb8ff` 是资产偶合 | 6 table destinations; 635 InstructionDB / 1324 code bytes + 43 pools / 172B + 6 pads / 12B | disasm |
| `aa7dc..aac1c`, 1088B | raw=6, THUMB=0. 5 raw hits 来自 table `aa7b4/b8/bc/d4/d8`; raw `aab3c@0851c07a` 是资产偶合 | table cases and direct CFG enter raw3/raw4 and existing shared tails; 452 InstructionDB / 930 code bytes + 35 pools / 140B + 9 pads / 18B | disasm |
| `aac32..aacbc`, 138B | raw=0, THUMB=0 | direct branches from `aab10/aab1c/aab28/aab34/aab52/aab5a/aab6a/aab7e/aab8e/aabae/aabb8/aabc2/aabc8/aabd0/aabea/aabf0/aac64/aac76` enter the internal starts; 61 InstructionDB / 128 code bytes + 2 pools / 8B + 1 pad / 2B, then code falls into existing `aacbc` shared tail | disasm |
| `aacc4..aad20`, 92B | raw=0, THUMB=0 | direct branches from `aab76/aabd8/aabfc` and internal CFG enter `aacc4/aacd8/aacea`; 41 InstructionDB / 92 code bytes, then code reaches existing `aad20` shared tail | disasm |
| `aafb0..ab1ac`, 508B | raw=8, THUMB=1. 8 raw hits come from table `aaf90..aafac`; THUMB `ab0ad@098a0c25` is an asset偶合 | 4 unique table destinations; 222 InstructionDB / 464 code bytes + 10 pools / 40B + 2 pads / 4B | disasm |

四项资产偶合保留原始 source, alignment 和 host:

- THUMB `0x080aa195` at `0x08acb8ff`, mod4=3, `data/card-image-tiles.s:1257`, `tb1251.bin+0x127f`.
- raw `0x080aa2fe` at `0x09f9f968`, mod4=0, `asm/rom.s:2097` FS-tail host, relative `0xcaec4`.
- raw `0x080aab3c` at `0x0851c07a`, mod4=2, `data/card-image-tiles.s:15`, `tb0009.bin+0x117a`.
- THUMB `0x080ab0ad` at `0x098a0c25`, mod4=1, `asm/rom.s:641` compressed asset host, relative `0x73ed`.

这些 source 均位于资产 bytes, 不形成 code/data consumer. 五块均有 switch 或 direct CFG live 入口, 本段没有 carve, 也没有 Section 5.1 raw block.

## 符号化计划, R1/R2/R3

### 完整 slots 合同

`F14-Seg-3.slots.tsv` 精确覆盖 116 current words 与 90 R4 new pools. 每行冻结 source Data, symbols, primary ID/name/type/source, `refs_from_json`, `refs_to_json`, 前态 `equates_json`, 精确后态 `after_equates_json`, EOL, target prestate, final label 和 GAS expression.

| action | count | contract |
|---|---:|---|
| `EQ_ADD` | 57 | 保持 current 4-byte Data, 新增或复用 equate |
| `REF_ADD` | 30 | 保持 current 4-byte Data, 新建批准的 DATA ref |
| `REF_PRESERVE` | 1 | `0x080ab6d0 -> gP1LifePoints` 既有 operand-0 `DATA/USER_DEFINED/primary` CORE6 原样保留; target Symbol ID `15545` 不变 |
| `TABLE_ENTRY_MATERIALIZE` | 23 | 保持现有 table word 与 source DATA ref; materialize table base/case target labels |
| `TABLE_ENTRY_EQUATE_EVEN_FUNCTION` | 5 | `aa7c0/c4/c8/cc/d0` 保持原 DATA/DEFAULT refs 指向 USER Function ID16957, 并为 operand0 增加同名 even-value Equate native projection |
| `EQ_MATERIALIZE` | 65 | 将 R4 undefined pool bytes 建成 4-byte Data + equate + source USER label |
| `REF_MATERIALIZE` | 25 | 将 R4 undefined pool bytes 建成 4-byte Data + DATA ref + source USER label |

Source `refs_from` 与 PC `READ refs_to` 必须分开. 已有 source DATA refs 的 CORE6 保持. 新 pool 在 disasm 后由 PC literal instruction 形成 `READ` refs_to, fixer 再按 TSV 建 source DATA ref 或 equate.

### switch table

- Mode 2 table base `equip_mode2_phase_table@0x080aa15c`; targets `phase_0=aa184`, `phase_1=aa22c`, `phase_2=aa2ac`, `phase_3_to_7=aa340`, `phase_8=aa348`, `phase_9=aa3d0`.
- Mode 3 table base `equip_mode3_phase_table@0x080aa7b4`; targets `phase_0=aa7dc`, `phase_1=aa894`, `phase_2=aa924`, phases 3..7 keep existing Function target `exit_equip_phase_oob_epilogue@aaf54`, `phase_8=aaa7c`, `phase_9=aaaf8`.
- Mode 4 table base `equip_mode4_phase_table@0x080aaf90`; targets `phase_0=aafb0`, `phase_1=ab040`, `phase_2=ab0ec`, `phase_3_to_7=ab1a4`.

28 table source words 已有 DATA refs. Dynamic DEFAULT case target labels materialize 为单一 USER label 时 primary ID 可合法变化. 16 个 unique targets 分为 15 个待物化 USER Label 与现有 USER Function `exit_equip_phase_oob_epilogue@aaf54` (ID `16957`) 1 个; 后者 ID/source/type/body/name 保持, 不在同址新增 Label alias. 五个 source `aa7c0/c4/c8/cc/d0` 的 DATA/DEFAULT/operand0/primary refs 保持, 仅创建全局 Equate `exit_equip_phase_oob_epilogue=0x080aaf54` 一次并精确绑定五个 operand0 EquateReference. 不加 `+1`, 不在 odd address 建 Label/Data/ref.

### FUNC_RENAME

| entry | old | new | direct callers |
|---|---|---|---|
| `080aa120` | `dispatch_equip_entry_state_by_phase_index` | `dispatch_equip_mode2_phase_by_combined_index` | `080ab2a8` |
| `080aa77c` | `dispatch_equip_entry_slot_phase_c` | `dispatch_equip_mode3_phase_by_combined_index` | `080ab1ac`, `080ab2ae` |
| `080aaf64` | `dispatch_equip_entry_slot_phase_d` | `dispatch_equip_mode4_phase_by_combined_index` | `080ab2b4` |

Function IDs `16955/16956/16958`, namespaces, signatures, calling conventions, flags, params 和 return metadata 保持. 所有 direct caller operands, current ASM text, 5 条 PLATE, registry, CSV 和 inventories 按 final names 同步.

`f14-seg3-name-reference-baseline.json` 冻结正式 source/registry/CSV 与 canonical `temp/` inventories 的 28 个旧名文本命中. Generated `asm/all.s*`, `output/**` 和 stale `tools/ghidra-labeling/ghidra-functions.*` 明确排除; stale copies 保持字节不变. Canonical inventory 前/后计数均为 5214 Functions / 5124 renamed / 90 auto. Root 独立 full-ROM pointer scan 对三个入口均得 raw=0, THUMB|1=0 (`root-f14-seg3-function-pointer-holds.json`), 因此没有 odd callback 或 `_1` alias 投影.

### PLATE

`F14-Seg-3.plates.tsv` 含 5 个完整 ASCII PLATE. 长度分别为 419, 489, 343, 412, 500 chars, 全部不超过 500. 不做 substring-only 写入.

- `aa120/aa77c/aaf64`: rename + 完整 R4 行为说明.
- `aaf54`: 将 516-char 旧 PLATE 收敛到 343 chars, 订正为 entry `r0=1` 与 interior `aaf56` 共用 epilogue.
- `ab200`: 投影 3 个 final callee names, 将 selector 准确写为 mode bits `[8:6]`, 并明确仅受影响的局部 body range 在 `ab278` 截止; 整个 Function 仍延续到 `aba50`.

## carve 计划, R7

None. 90 new pools 只指向 RAM globals 或 scalar constants. 本段没有 ROM data target 需要从 `asm/rom.s` carve.

## disasm 计划, R4

### 2.1 Even Function table native projection

`ExportRangeToGas.py` SHA256 `4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87` 对 ROM Function target 不走 symbol projection, 因此五槽必须使用现有 equate fallback. 全局 Equate 前态为 absent/refs=0; 后态精确为 name `exit_equip_phase_oob_epilogue`, value `0x080aaf54`, references `aa7c0/c4/c8/cc/d0` operand0. EquateTable 与 SymbolTable/ReferenceManager 独立: 不改五条 DATA refs, 不改 Function ID16957, 不创建同址 Symbol alias. 该不变量严格限定于 `operation_scope=projection_only`: projection 本身对 AAF54 memory incoming refs 的 delta=0, 不写其 PLATE; 整个 Seg3 仍按 `F14-Seg-3.plates.tsv`, `f14-seg3-function-plan.json` 与 R4 map 执行已批准的 AAF54 PLATE 和 old+new incoming 更新. `after_equates_json` 对全部 206 槽冻结精确后态: 122 literal EQ 槽各一项, 5 projection 槽各一项, 其余 79 槽为空; total equated slots=127, distinct projection global Equate=1. 合同 `f14-seg3-even-function-equate-contract.json` SHA256 `cc60560d717af799e24da92304dd345ecd259b758ada89aa96995d57f3747776`.

### 精确地址级布局

`f14-seg3-r4-cfg-map.json` 的 `instructions[]` 是 1411 个新增 InstructionDB 地址的权威集合. 每项冻结 `address`, `length`, ROM little-endian `raw_bytes`, decoded halfwords, direct flows, calls, PC reads 和 machine/API fallthrough.

- 新 InstructionDB: 1411, 2938 code bytes.
- 新 pools: 90 words, 360 bytes.
- 新 zero pads: 18 halfwords, 36 bytes.
- direct flows: 248, 其中 CALL=58.
- PC literal reads: 95.
- machine/API fallthrough edges: 1338. 不设置 FlowOverride.
- final segment: 2696 InstructionDB / 5596 code bytes; 206 words / 824 bytes; 68 padding bytes. 合计 6488 bytes.

40 个 maximal code ranges:

- Mode 2: `[aa184,aa1e6)`, `[aa200,aa21e)`, `[aa22c,aa2a2)`, `[aa2ac,aa308)`, `[aa30c,aa33c)`, `[aa340,aa3c4)`, `[aa3d0,aa5b8)`, `[aa5f8,aa602)`, `[aa608,aa61c)`, `[aa620,aa624)`, `[aa628,aa646)`, `[aa658,aa662)`, `[aa668,aa690)`, `[aa694,aa760)`.
- Mode 3: `[aa7dc,aa81e)`, `[aa828,aa886)`, `[aa894,aa90e)`, `[aa924,aa964)`, `[aa968,aa9c8)`, `[aa9d4,aa9e6)`, `[aa9ec,aa9f4)`, `[aa9f8,aaa2a)`, `[aaa30,aaa6c)`, `[aaa7c,aaaea)`, `[aaaf8,aab3a)`, `[aab4c,aab5e)`, `[aab64,aab82)`, `[aab88,aab98)`, `[aaba0,aaba4)`, `[aaba8,aabdc)`, `[aabe0,aabf4)`, `[aabf8,aac1c)`, `[aac3c,aacbc)`, `[aacc4,aad20)`.
- Mode 4: `[aafb0,aaff0)`, `[aaff8,ab03a)`, `[ab040,ab0e0)`, `[ab0ec,ab178)`, `[ab184,ab19e)`, `[ab1a4,ab1ac)`.

18 个 zero pads:

`aa1e6`, `aa21e`, `aa2a2`, `aa602`, `aa646`, `aa662`, `aa81e`, `aa886`, `aa90e`, `aa9e6`, `aaa2a`, `aaaea`, `aab3a`, `aab5e`, `aab82`, `aac32`, `ab03a`, `ab19e`.

90 个 pool 地址全部在 slots TSV 以 `R4_NEW_POOL` 覆盖. 三组精确地址也冻结在 map 的 `pool_words[]`; fixer 必须逐地址创建 4-byte Data, 不能把 code/pad 合并进 pool.

### seeds 与覆盖门禁

- Table seeds: `aa184,aa22c,aa2ac,aa340,aa348,aa3d0`; `aa7dc,aa894,aa924,aaa7c,aaaf8`; `aafb0,ab040,ab0ec,ab1a4`.
- Cross-range CFG seeds: `aac3c,aac54,aac66,aac78,aac90,aaca8,aacc4,aacd8,aacea`.
- 先对 restricted expected-code AddressSet 执行 seeds. 然后将实际 InstructionDB start set 与 map 的 1411-address set 比较, 对每个 missing start 单点补 disasm. 任一 extra start 立即中止落地并回滚 `.rep`.
- 所有 248 direct flows, 95 PC reads, 1338 machine/API fallthroughs 必须与 map 相同. CALL 保留默认 machine/API fallthrough; semantic return 行为只写 PLATE, 不设置 FlowOverride.

### Function body 与 shared-tail ownership

完整 ranges 和 SHA 同时冻结在 `f14-seg3-function-plan.json` 与 plates TSV:

- `aa120`: 68 -> 1392 bytes, 16 ranges, SHA256 `4265027bac9c9ae9aa5638f1a1d6c21355090d04739b1c93158e8a1b5bf204e1`.
  `aa120..aa152, aa184..aa1e6, aa200..aa21e, aa22c..aa2a2, aa2ac..aa308, aa30c..aa33c, aa340..aa3c4, aa3d0..aa5b8, aa5f8..aa602, aa608..aa61c, aa620..aa624, aa628..aa646, aa658..aa662, aa668..aa690, aa694..aa760, aa768..aa77a`.
- `aa77c`: 46 -> 1196 bytes, 21 ranges, SHA256 `986595291773e3c7fc99d438d66a0eebe1f3f6232a8742fba9d3f27b3949f7db`.
  `aa77c..aa7aa, aa7dc..aa81e, aa828..aa886, aa894..aa90e, aa924..aa964, aa968..aa9c8, aa9d4..aa9e6, aa9ec..aa9f4, aa9f8..aaa2a, aaa30..aaa6c, aaa7c..aaaea, aaaf8..aab3a, aab4c..aab5e, aab64..aab82, aab88..aab98, aaba0..aaba4, aaba8..aabdc, aabe0..aabf4, aabf8..aac1c, aac3c..aacbc, aacc4..aad20`.
- `aaf54`: 16 bytes unchanged, range `[aaf54,aaf64)`, SHA256 `8b63e6c361cdc73016abed1822263bd899e711bea8d668d52ea9210b28d21d78`.
- `aaf64`: 104 -> 568 bytes, 9 ranges, SHA256 `fea44969df8f38719074463ab5bad2318b6b0eb453dc5df9975d7023ec4f071b`.
  `aaf64..aaf88, aafb0..aaff0, aaff8..ab03a, ab040..ab0e0, ab0ec..ab178, ab184..ab19e, ab1a4..ab1cc, ab1d4..ab1ee, ab1f4..ab1fe`.
- `ab200`: 2426 -> 2424 bytes, 23 ranges, SHA256 `64c7172d01bc2be293ae7c27e9ecf51b8cfb0f79890fa948a318be05f04bf940`.
  `aac1c..aac32, aacbc..aacc4, aad20..aad6c, aad78..aad82, aad8c..aada0, aada4..aadb2, aadb8..aadd2, aadd8..aaddc, aade0..aadf8, aae00..aae0e, aae14..aae1e, aae24..aae48, aae4c..aaf2a, ab200..ab234, ab238..ab278, ab284..ab3ae, ab3e0..ab482, ab498..ab6c4, ab6f0..ab74e, ab768..ab778, ab77c..ab796, ab79c..ab82a, ab840..aba50`.

Mode-3 raw code 保留 `aa77c` 的 prologue/frame context. Existing backward/shared tails 保持 `ab200` owner, 不建立重叠 Function body. 新 cross-owner edges 共 27:

- To `aaf54`: `aaaa4->aaf54`; interior `aaa6a/aaae8/aab04->aaf56`.
- To `ab200` tail `aaef4`: `aa7e4,aa81c,aa884,aa8ec,aa8fa,aa90c`.
- To `ab200` tail `aad20`: 13 direct sources `aab5c,aab80,aabca,aabda,aabf2,aac02,aac0a,aac12,aac52,aac8e,aaca6,aacd6,aace8` plus API fallthrough `aad1c->aad20`.
- To `ab200` tail `aacbc`: direct `aac64->aacbc` plus API fallthrough `aacba->aacbc`.
- To `ab200` tail `aac1c`: API fallthrough `aac1a->aac1c`.

这些 edges 新增 address-level incoming refs. `aaf54` Function-entry incoming 增加 `aaaa4->aaf54`; interior `aaf56` 单独维护 3 条 JUMP refs. `ab200` Function entry incoming 不变, body interior incoming 按上述 23 条增加.

### source 格式预测

当前 1285 InstructionDB 导出为 1222 mnemonic + 63 `.hword`. 新 code 中 29 条 `0x46xx` high-register move 预计由当前 exporter 输出为 `.hword`. Final 预计为 2604 mnemonic + 92 `.hword` = 2696 InstructionDB. 完整地址集见 `f14-seg3-source-format-prediction.json`; 后态必须同时核对 Instruction API set, source mnemonic + `.hword` total, 以及 ROM bytes.

## 新增 constants / 全局

现有 constants 已全库按 value + domain 搜索. 新增 15 项, 结构化证据见 `f14-seg3-constant-plan.json`:

- `constants/card_info.inc`: `CID_GAP_1255`, `SWARM_OF_LOCUSTS_CID`, `GOLEM_SENTRY_CID`, `CID_GAP_133D`, `CID_GAP_1387`, `KING_TIGER_WANGHU_CID`, `BYSER_SHOCK_CID`, `DARK_JEROID_CID`, `DARK_MAGICIAN_KNIGHT_CID`, `STUMBLING_CID`, `SACRED_CRANE_CID`.
- `constants/oam_attr.inc`: `EQUIP_MODE3_CARD_SPRITE_CODE_SIDE1=0x8047`.
- `constants/ewram.inc`: 定义 `.equ gLpBarDisplayCounter, gDuelPhaseFlags + LP_BAR_DISPLAY_CTR_OFF`, 由全局定义复用 base+offset 且不新增同址 alias. `0x080ab494` 的单一 USER target 是 `gLpBarDisplayCounter`, 因此 native resolver 的 slot expression 必须是 `.word gLpBarDisplayCounter`; 不改 exporter, 不在 slot expression 展开 base+offset.
- `constants/duel_field.inc`: `HARPIES_HUNTING_GROUND_EQUIP_ATTR_FLAGGED=0x012a183f`, `HARPIES_HUNTING_GROUND_EQUIP_ATTR_BASE=0x002a183f`.

Card evidence:

- `0x152b` = Swarm of Locusts, logical CID 1105, password 41872150; `0x186e` = Golem Sentry, logical CID 1775, password 52323207.
- `0x1398` = King Tiger Wanghu, logical CID 809, password 83986578; `0x14b4` = Byser Shock, logical CID 1000, password 17597059.
- `0x157b` = Dark Jeroid, logical CID 1155, password 90980792; `0x167c` = Dark Magician Knight, logical CID 1353, password 50725996.
- `0x16d0` = Stumbling, logical CID 1426, password 34646691; `0x16fb` = Sacred Crane, logical CID 1460, password 30914564.
- `0x1255`, `0x133d`, `0x1387` 的 `data/cards-ids-array.s` inverse entries 均为 `0xffff`, 且 `card-stats.s` 无对应 slot.

复用现有 `upd_cid_120e`, `lookup_equip_card_score_cid_1388`, 所有 RAM globals, masks, sprite codes 和已命名 card IDs. 不新增同值 duplicate alias.

## Section 5.1 登记, Rule 3

None. 五个 raw blocks 均由真实 table/direct CFG consumer 进入.

## 消费者证据, R6

- `asm/14_equip_ai_scoring.s:5407-5460`: mode-2 prologue, table 和 local epilogue; confidence high.
- `asm/14_equip_ai_scoring.s:5464-5834`: mode-3 dispatcher, current shared tails, table phases 3..7; R4 CFG 补全见 map; confidence high.
- `asm/14_equip_ai_scoring.s:5846-5924`: mode-4 dispatcher, 8-entry table, mode-3 chaining; confidence high.
- `asm/14_equip_ai_scoring.s:5928-6022`: controller mode switch 与 3 个 direct rename callers; confidence high.
- `0x080aa93e/0x080aa95e`: selects `0x47/0x8047` by player-side bit and calls `enqueue_sprite_attr_record`; confidence high.
- `constants/ewram.inc:404` 已定义 `LP_BAR_DISPLAY_CTR_OFF=0x4c4`; `gDuelPhaseFlags(0x0201b290)+0x4c4=0x0201b754`. `asm/05_equip_eligibility_a.s:3237-3238,3304-3305,3361-3362` 的全局消费者对该域执行 LP-bar display counter 增减; `asm/14_equip_ai_scoring.s:6269` / consumer `0x080ab46a` 只读取同一 counter 来选择局部显示路径; confidence high.
- `0x080ab6c0..0x080ab712`: `0x012a183f/0x002a183f` preserve low CID `HARPIES_HUNTING_GROUND_CID`, add side/slot fields, then call `apply_equip_activation_with_id_lookup`; confidence high.
- 每一 slots TSV row 另含当前 source line 或 planned PC-read address, refs_from/refs_to 与 high confidence 标记.

## 同步与守恒合同

- `RenameKnownFunctions.py`: add missing tuples for `aa120` and `aaf54`; update existing tuples for `aa77c`, `aaf64`, `ab200` with final names/PLATE. 其他 registry rows 不变.
- Canonical inventories 仅为 `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-summary.md`: 前/后保持 5214 Functions / 5124 renamed / 90 auto; update 3 names and body lengths `aa120 68->1392`, `aa77c 46->1196`, `aaf64 104->568`, `ab200 2426->2424`. Legacy `tools/ghidra-labeling/ghidra-functions.*` 不写.
- `doc/dev/naming-proposals.csv` 当前 5079 data rows; 仅更新 `aa120/aa77c/aaf64` 三个既有 row 的 name cell, 保持原 row 顺序及全部其他字段, 不增删 row.
- Function IDs, static USER target IDs, namespaces, signatures, params, flags 保持. Dynamic DEFAULT source/case labels materialize USER 时允许合法新 ID.
- 116 current words 的 Data type/bytes/refs/equates 前态逐项冻结, 206 槽的 `after_equates_json` 逐项冻结. 90 new pools 只在批准地址 materialize. ROM bytes 必须 byte-identical.

## 冻结 hash

- `root-f14-seg3-initial-baseline.json`: `2ad36fd86016e11065dd87226d1bace66e1f298674176ce7527ed86ffdafaa01`.
- `root-f14-seg3-supplement-prestate.json`: `fcd04b3e0888a6cd414e05390d28292e7a5755eb2a4cae52049fd2feca14309d`.
- supplement DB gate: `35e4df505ff9074c300f7049760d7326d412cf124a4dc102bb28a49250f6c4d6`.
- `f14-seg3-r4-cfg-map.json`: `0ef41331aac5d2f562f123d5bf7013dbe94cfeb4a96c178a0d75183f91c5b66e`.
- root R4 static gate: `05b760e67e73dab0cd0f4a838b02e0eb040356b601136775d14a850ba0036a31`.
- `f14-seg3-full-rom-refscan.json`: `170430a6b46ca86299b0b378656fff0d9a639df3c27c4e1ad2d4bfd9124d29f9`.
- `f14-seg3-function-plan.json`: `204006f29399e9f8c4b952e190154c5d6431c2cab6069d531c63cd41a81f3502`.
- `f14-seg3-constant-plan.json`: `1930920fa0b40f0a64487dcb9a1935e509acca2206ec6b524eec5bf46e88ca06`.
- `f14-seg3-source-format-prediction.json`: `61de87a862c0fb5bf7f736795d72c8f936e43932d50998cf3720b67d35e427e4`.
- `f14-seg3-name-reference-baseline.json`: `4222b9a73a0eb8850bef43f1b72cf9358b8c202adb87503cea2b88acac355c59`.
- `f14-seg3-mode-a-machine-contract.json`: `ecd6922ab4690225fc3c09cc1cacb25dc09589bcfc94914eb72e3494a987b989`.
- `f14-seg3-even-function-equate-contract.json`: `cc60560d717af799e24da92304dd345ecd259b758ada89aa96995d57f3747776`.
- even-Function export addendum (immutable round2 archive): `4b88b4bcbd7f2315368fd09c6738f7a8407b92a687d7dc43dc049359f61dc5f4`.
- global Equate prestate: `2dd2701bddc804924638e9e3215a60784628726cf55ff81a37fa8f5bdb733a94`; readonly DB gate `35e4df505ff9074c300f7049760d7326d412cf124a4dc102bb28a49250f6c4d6`.
- root Mode-A correction proof: `4feebec9c2d699ad85f60ff37ad3b2dd7d3f57e488dc8087ee23816bf2139d58`.
- root Function pointer holds: `b00de0843e1efd9c49c8dc6edea377cc2060c5362a9c5cea803d3e623d16de80`.
- `F14-Seg-3.slots.tsv`: `370def5e0e4bb363827bb8c9f47eadf512a5ee63b70d3150586eb86556fdb20f`.
- `F14-Seg-3.plates.tsv`: `a9e41dd029dbb747f9378d17337e8026ed748387b8c6b3802acc8ea35b35bcfd`.

## 求助

None.

## Executor Report: F14-Seg-3

- 槽: literal EQ=122 (`EQ_ADD=57`, `EQ_MATERIALIZE=65`), REF=56 (`REF_ADD=30`, `REF_PRESERVE=1`, `REF_MATERIALIZE=25`), TABLE=28 (`TABLE_ENTRY_MATERIALIZE=23`, `TABLE_ENTRY_EQUATE_EVEN_FUNCTION=5`), projection Equate refs=5 / distinct global Equate=1 / total equated slots=127, FUNC_RENAME=3, PLATE=5.
- carve=0, disasm=40 ranges / 1411 InstructionDB, Section 5.1=0.
- 新增 constants/global: 15.
- 求助: none.
- proposal: `doc/dev/refine/F14-Seg-3.proposal.md`.
