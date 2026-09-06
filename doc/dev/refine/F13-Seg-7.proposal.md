# Refine Proposal: F13-Seg-7 [0x080a38fc..0x080a46a0)

## 0. 结论

- 严格主范围为 `[0x080a38fc,0x080a46a0)`, 长度 `0x0da4 = 3492` bytes。本轮从低地址向高地址处理 Seg-7；`0x080a46a0` 是 Seg-8 首函数，仅作为边界 direct-call 目标核验，不分析其内部语义。
- 实测既有 Function=22，其中 non-push 入口=2；保留14个现名，订正8个误名，不创建或删除 Function，所有既有 body 保持不变。
- 实测残留自动槽=96，组成 `DAT=92, PTR=4`。逐槽合同为 `EQ=73, REF=19, RENAME=4`；槽引用状态为 `REUSE=70, NEW=26`，每槽设置一条 ASCII EOL。
- 布局为 `1352 instruction + 91 hword_instruction`，共1443个代码单元、3050 code bytes；另有96个4-byte pool words（384 bytes）及29个2-byte padding ranges（58 bytes），总和3492 bytes。段内没有 `ROM_INCBIN` 或 `.byte` 裸块。
- 依赖 carve=2：`[0x09e47898,0x09e478a4)` Gate Guardian 三材料 CID 表与 `[0x09e478a4,0x09e478b0)` Valkyrion 三材料 CID 表。两表均有真实 raw 引用，不能进入 Rule 3。
- R4=0，Rule 3 / §5.1=0。direct edges=305（`B=60, Bcc=163, BL=82`）；所有段外目标均为既有 Function，唯一高地址边界目标为 `0x080a46a0`。
- Function rename=9（段内8个，段外语义涟漪1个）；PLATE full rewrite=14（9个误名函数、2个段内语义/旧名PLATE、3个段外旧名涟漪PLATE）；新增定义=16（11 constants、3 Thumb aliases、2 ROM table labels）。
- BLOCKED: none。误名订正均由 caller gate、callee body、全局读写及 `data/card-stats.s` 的结构化 CID 四层证据闭合，置信度 high。

## 1. 前态与权威证据

| artifact | rows / role | SHA256 |
|---|---:|---|
| `asm/13_equip_placement.s` | executor source baseline | `bedc6c7c34abfb18f1ddbcc979e1ad49d5f33d1bfcc740ba1a76316d2090042f` |
| `temp/ghidra-functions.csv` | Function inventory baseline | `25bdb15db9649399f13241e8b34594ee5efc4df85f439a3d22583613c4f7e3b` |
| `output/refine-run-20260831-194634/f13-module-map.json` | full module machine map | `d8ea39ee7a3d2a0f1a8118949849a833ca5566cf87ad2eb5f0365e4a1ef0175c` |
| `doc/dev/refine/F13-Seg-7.slots.tsv` | 96 revised slot rows | `2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f` |
| `doc/dev/refine/F13-Seg-7.review.md` | authoritative Round2 NEEDS_FIX(1) | `61b478f23eea5439a83843a0e7ae6cb11f6698a7119e84f0823abf47fc4839f3` |
| `output/refine-run-20260831-194634/f13-seg7-refscan.tsv` | 96 slot-address scans | `e98fe19aa98963f587f62ef05107aad86e1a2aa3292d4a7b54cb8472c276d52a` |
| `output/refine-run-20260831-194634/f13-seg7-functions.tsv` | 22 Functions, 65 exact body ranges | `57e4d3cf6a5720d6ddf7d20074fdddd58a688489f6c125e3397de7c2940301c3` |
| `output/refine-run-20260831-194634/f13-seg7-direct-edges.tsv` | 305 direct edges | `afc0106593069583a9ad418b6e4c5501bc6f277a3eac92d90208c1200632767e` |
| `output/refine-run-20260831-194634/f13-seg7-literal-reads.tsv` | 100 decoded PC-relative reads | `62c42d3f553e240641073f3b9ed41e11d5a5943b8f3ebb41e21f6f0e0d23d5d1` |
| `output/refine-run-20260831-194634/f13-seg7-consumers.tsv` | 10 semantic decisions | `d81ef5de9411ffbf0eaf8a1e17da5f186b2a95e5c1c2bbc90886b142a61a4eb1` |
| `output/refine-run-20260831-194634/f13-seg7-layout.json` | layout, closure and carve summary | `c2487fa74d1ee2f348e0e8e07c0f8f816c131004c93a6b1a79ad98cec1a50798` |
| `output/refine-run-20260831-194634/F13Seg7ProposalPrestate.py` | read-only target/slot/external-Function query | `13d5032c70438ca67cd5ad8e8bdbc2089cb70cdee6606c0f2ea7f196f760d51f` |
| `output/refine-run-20260831-194634/f13-seg7-ghidra-prestate.json` | fresh read-only 8 targets + 19 REF + 4 RENAME + 2 external Functions | `54d59f1f9cdad65c034da875f92f367944adba41ab332a93b4a5e031ddf0a623` |
| `output/refine-run-20260831-194634/f13-seg7-ghidra-prestate-gate.json` | command/exit/marker + DB before/after 15/15 exact | `57efed71e2db94267a220d69f0c07478371c117c2157742a363db9a03a2ccbab` |

`slots.tsv` 是逐槽唯一落地合同，字段包括地址、旧名、原值、动作、目标符号、最终槽名、REUSE/NEW、raw/THUMB|1 命中、PC-relative consumers、证据与 ASCII EOL。`functions.tsv` 的 `body_ranges` 是65个精确非连续代码范围；不得用线性入口到下一入口替代 Ghidra Function body。

## 2. Function inventory 与误名订正

| entry | current name | final name | action |
|---|---|---|---|
| 0x080a38fc | tick_equip_score_display_phase | same | preserve |
| 0x080a3a80 | scan_activatable_equip_slots_init | same | preserve |
| 0x080a3ae8 | scan_equip_activation_for_player | same | preserve |
| 0x080a3b50 | get_equip_activation_mode_by_card_id | same | preserve, non-push |
| 0x080a3b74 | scan_equip_activation_with_mode | same | preserve |
| 0x080a3c2c | check_banisher_of_light_activatable | check_banisher_sensitive_summon_allowed | rename |
| 0x080a3d0c | scan_activatable_equip_slots_alt | same | preserve |
| 0x080a3d74 | check_banisher_pair_activation_allowed | check_neo_bubbleman_summon_allowed | rename |
| 0x080a3dac | check_equip_set_activatable_for_player | check_gate_guardian_summon_allowed | rename |
| 0x080a3eb4 | eval_equip_card_placeable_for_player | check_valkyrion_summon_allowed | rename |
| 0x080a3fc8 | eval_equip_card_multi_target_placeable | same | preserve |
| 0x080a4058 | init_spell_activation_context | same | preserve |
| 0x080a40bc | check_equip_target_monster_placeable | same | preserve |
| 0x080a4134 | check_ritual_fusion_pairable_slots_exist | check_fusion_material_pair_slots_exist | rename |
| 0x080a422c | classify_spell_card_activation_type | get_special_summon_material_rule_by_card_id | rename, non-push |
| 0x080a42b0 | eval_spell_card_activation_placeable | check_special_summon_material_rule_satisfied | rename |
| 0x080a43c8 | eval_spell_equip_target_availability | same | preserve |
| 0x080a4490 | eval_equip_targets_for_card | same | preserve |
| 0x080a4574 | check_equip_slot_has_field_spell_target | check_necroshade_normal_summon_available | rename |
| 0x080a45f4 | check_equip_card_activation_valid | same | preserve |
| 0x080a4648 | check_player_can_place_card | same | preserve |
| 0x080a4694 | eval_card_placement_flags_default | same | preserve |

### 2.1 Rename evidence 与 APCS

- `0x080a3c2c`: `r0=u32 player_side`, `r1=u16 card_id`, returns `u32 bool`; writes `gEquipZoneRankState`. Caller `0x080a50a0` dispatches Uria `0x19a3`, Hamon `0x19a4` and Anteatereatingant `0x19c8`; entry guard rejects when Banisher `0x1332` is present. The old name reverses subject and guard.
- `0x080a3d74`: `r0=u32 player_side`, `r1=u16 card_id`, returns `u32 bool`; delegated scan writes `gEquipZoneRankState`. Exclusive caller `0x080a50aa` is reached for Neo Bubbleman `0x19a6`; the body requires Banisher absent and a valid Metamorphosis `0x15a3` pair. The old PLATE's Ectoplasmer identity is contradicted by `data/card-stats.s:15498`.
- `0x080a3dac`: `r0=u32 player_side`, returns `u32 bool`, read-only. The body `asm/13_equip_placement.s:14229-14334` copies and scans only the `0x09e47898` Sanga/Kazejin/Suijin table; callers `asm/13_equip_placement.s:16259-16262,16809-16812` reach it only through the `0x111c` Gate Guardian branch.
- `0x080a3eb4`: `r0=u32 player_side`, returns `u32 bool`, read-only. The body `asm/13_equip_placement.s:14367-14465` copies and scans only the `0x09e478a4` Alpha/Beta/Gamma table; callers `asm/13_equip_placement.s:16303-16311,16813-16816` reach it through `0x13e9-0x5f=0x138a`, Valkyrion. `r10` is the current table material CID inside the loop, not a caller argument.
- `0x080a4134`: `r0=u32 player_side`, `r1=u16 fusion_card_id`, returns `u32 bool`, read-only. Every key and subordinate material is in the XZ/YZ/XYZ/VW/VWXYZ fusion cluster; no ritual card participates.
- `0x080a422c`: `r0=u16 card_id`, returns `u32 material_rule` in `0..3`, read-only. All keys are special-summon monsters; rule values partition mixed-material, same-type and three-Fiend requirements. This is not a spell activation type.
- `0x080a42b0`: `r0=u32 player_side`, `r1=u16 card_id`, returns `u32 bool`; it consumes the rule from `0x080a422c`, scans candidate slots and may dispatch the card effect handler. The result is whether the special-summon material rule is satisfied.
- `0x080a4574`: `r0=u32 player_side`, `r1=u32 slot_idx`, returns `u32 bool`, read-only. Caller `0x080a49e4` first gates on normal-summon type; the body scans `gP1HandSlotArray` for `0x197f`, which `data/card-stats.s:25937` identifies as Elemental Hero Necroshade. The old Field Spell subject is false.
- `0x08094f58`: `r0=u16 card_id`, returns void. Its sole caller `asm/04_card_zone_sprite.s:3053-3057` extracts the current field-slot card ID into `r0`; the callee passes that value unchanged to `get_special_summon_material_rule_by_card_id` and writes display index `0x1a`, bit value1, only for a nonzero rule. The old spell-activation subject and the prior no-argument claim are false.

All nine final names match `^[a-z][a-z0-9_]+$` and use a verb-object-qualified form. `doc/dev/naming-proposals.csv` must update exactly these nine existing address rows after persisted verification.

### 2.2 Nine-Function landing contract

The following old/new pairs and exact half-open Ghidra bodies are frozen. Preflight requires one USER_DEFINED Global Function at each entry with the old name and the listed body; postcheck requires the same Function ID, entry, body, calling convention and parameter/return storage, with only its name and approved ASCII PLATE changed. CSV sync changes only the `name` cell of these nine existing address rows. Registry sync changes the eight existing Seg-7 tuples and adds exactly one previously absent `FUN_08094f58 -> write_special_summon_material_rule_display_bit` tuple with the approved PLATE; it must not add a duplicate old or final name. The four inventories must be regenerated from the persisted DB. No Function is created, deleted, resized or split.

| entry | pre name | post name | exact body ranges |
|---|---|---|---|
| `0x080a3c2c` | `check_banisher_of_light_activatable` | `check_banisher_sensitive_summon_allowed` | `[0x080a3c2c,0x080a3c86);[0x080a3c9c,0x080a3ca4);[0x080a3ca8,0x080a3cae);[0x080a3cb4,0x080a3cba);[0x080a3cc0,0x080a3cfc);[0x080a3d00,0x080a3d0c)` |
| `0x080a3d74` | `check_banisher_pair_activation_allowed` | `check_neo_bubbleman_summon_allowed` | `[0x080a3d74,0x080a3d9a);[0x080a3da4,0x080a3dac)` |
| `0x080a3dac` | `check_equip_set_activatable_for_player` | `check_gate_guardian_summon_allowed` | `[0x080a3dac,0x080a3e8e);[0x080a3ea0,0x080a3eb2)` |
| `0x080a3eb4` | `eval_equip_card_placeable_for_player` | `check_valkyrion_summon_allowed` | `[0x080a3eb4,0x080a3f8c);[0x080a3f9c,0x080a3fc8)` |
| `0x080a4134` | `check_ritual_fusion_pairable_slots_exist` | `check_fusion_material_pair_slots_exist` | `[0x080a4134,0x080a4150);[0x080a4154,0x080a4166);[0x080a4170,0x080a4178);[0x080a417c,0x080a418e);[0x080a4194,0x080a41b2);[0x080a41bc,0x080a41ce);[0x080a41d4,0x080a41e4);[0x080a41ec,0x080a41fc);[0x080a4204,0x080a4220);[0x080a4224,0x080a422c)` |
| `0x080a422c` | `classify_spell_card_activation_type` | `get_special_summon_material_rule_by_card_id` | `[0x080a422c,0x080a424e);[0x080a4258,0x080a425c);[0x080a4260,0x080a4272);[0x080a4278,0x080a428a);[0x080a4294,0x080a429c);[0x080a42a0,0x080a42b0)` |
| `0x080a42b0` | `eval_spell_card_activation_placeable` | `check_special_summon_material_rule_satisfied` | `[0x080a42b0,0x080a433a);[0x080a434c,0x080a436e);[0x080a4374,0x080a43c8)` |
| `0x080a4574` | `check_equip_slot_has_field_spell_target` | `check_necroshade_normal_summon_available` | `[0x080a4574,0x080a45d4);[0x080a45e4,0x080a45f4)` |
| `0x08094f58` | `write_spell_activation_type_display_bit` | `write_special_summon_material_rule_display_bit` | `[0x08094f58,0x08094f6e)` |

APCS is frozen as stated in section 2.1: entries `3c2c/3d74/4134/42b0` take `r0=u32 player_side,r1=u16 card_id` and return `r0=u32`; `3dac/3eb4` take only `r0=u32 player_side` and return `r0=u32`; `422c` takes `r0=u16 card_id` and returns `r0=u32`; `4574` takes `r0=u32 player_side,r1=u32 slot_idx` and returns `r0=u32`; external `08094f58` takes `r0=u16 card_id` and returns void. The caller/callee/global contracts are the direct-edge ledger plus section 2.1; the two added segment functions are specifically read-only and consume only their approved material table, field-slot helpers and Mask of Restrict guard. Mode B must capture the nine Function/Symbol IDs before mutation and require identical IDs after save and in the fresh persisted check.

### 2.3 External Function and caller-PLATE prestate contract

The refreshed headless query ran with literal `-noanalysis -readOnly`, exited0, emitted marker `F13_SEG7_PROPOSAL_PRESTATE_READONLY_OK targets=8 REF=19 RENAME=4 EXT_FN=2`, and left the 15-file DB manifest byte-identical. It freezes these two external objects in addition to the slot/target contracts:

| entry | exact prestate Function/Symbol | exact body | pre PLATE / post action |
|---|---|---|---|
| `0x08094f58` | Function ID=`5446`, name=`write_spell_activation_type_display_bit`, Symbol type=`Function`, source=`USER_DEFINED`, namespace=`Global`, primary=`true`, alias count=`0`, calling convention=`unknown`, return type=`/undefined`, parameters=`[]` | `[0x08094f58,0x08094f6e)`, 22 bytes | current PLATE falsely states no caller parameters and spell activation type; post renames the same ID and replaces only the full PLATE |
| `0x0804154c` | Function ID=`5416`, name=`tick_spell_equip_zone_display_seq`, Symbol type=`Function`, source=`USER_DEFINED`, namespace=`Global`, primary=`true`, alias count=`0`, calling convention=`unknown`, return type=`/undefined`, parameters=`[]` | `[0x0804154c,0x0804162c);[0x08041648,0x0804169c);[0x080416a8,0x080416d6);[0x080416e4,0x08041754)`, 466 bytes | current PLATE contains `FUN_08094f58 (write_spell_activation_type_display_bit)`; post preserves Function/Symbol/body and replaces only the full PLATE |

Postcheck and fresh persisted check require IDs `5446/5416`, entries, bodies, source/type/namespace/primary, calling convention, return type and parameter storage to remain exact; each entry must have exactly one Symbol and no alias. Exporter projection is exact: module12 defines `write_special_summon_material_rule_display_bit:` and its `0x08094f5a` call is `bl get_special_summon_material_rule_by_card_id`; module04 `0x080415be` is `bl write_special_summon_material_rule_display_bit`. Formal asm must contain neither `FUN_08094f58` nor `write_spell_activation_type_display_bit` after landing.

## 3. 自动槽与符号化计划

| kind | count |
|---|---:|
| DAT | 92 |
| PTR | 4 |
| total | 96 |

| action | count | exact operation |
|---|---:|---|
| EQ | 73 | attach the named equate at operand 0, rename the slot, set the TSV EOL; includes three odd Thumb callback words |
| REF | 19 | rename the slot, install the exact operand-0 DATA reference, set the TSV EOL |
| RENAME | 4 | preserve the existing `gP1LifePoints` DATA reference, rename the slot, set the TSV EOL |

All 96 final slot labels are unique and match `^[a-z][a-z0-9_]+$`. All 96 ROM values have been checked against little-endian words at the slot addresses. Full-ROM packed scans of every slot address and `slot|1` both return zero; this is expected because the 100 consumers are decoded PC-relative LDRs, not packed pointers to literal-pool addresses. The 100 reads cover all 96 slots.

### 3.1 EQ target summary

The authoritative per-address list is `F13-Seg-7.slots.tsv`. Reused constants include `REASONING_CID`, `SORCERER_OF_DARK_MAGIC_CID`, `RAVIEL_LORD_CID`, `BANISHER_OF_THE_LIGHT_CID`, `HAMON_LORD_CID`, `METAMORPHOSIS_CID`, `MASK_OF_RESTRICT_CID`, `ULTIMATE_OFFERING_CID`, the existing fusion/special-summon CIDs, `PLAYER_BLOCK_STRIDE`, `EQUIP_PHASE_DISPLAY_STATE_OFF`, `LP_CARD_TRACK_BASE_OFF` and `CARD_STAT_LP_THRESHOLD_999`.

New EQ definitions cover ten constant values in 21 slot rows plus three Thumb `even_function+1` alias values in three slot rows, for 13 named targets across 24 NEW EQ rows. The constant subset remains six card CIDs, two display parameters and two equip-activation bit masks. Same numeric values in another field domain are not reused as semantic aliases.

The three callback slots are equates, never references:

| slot | stored value | equate target | forbidden mutation |
|---|---:|---|---|
| `0x080a3cb0` | `0x080a839d` | `check_equip_target_slot_eligible_by_field6_eq17_1` | no Label/Data/Function at odd address; no DATA ref |
| `0x080a3cbc` | `0x080a840d` | `check_equip_target_slot_eligible_by_field9_eq4_field6_eq16_1` | no Label/Data/Function at odd address; no DATA ref |
| `0x080a3cfc` | `0x080a8479` | `check_equip_target_slot_eligible_by_whitelist_or_special_1` | no Label/Data/Function at odd address; no DATA ref |

For each row Mode B must verify the even address is the existing USER_DEFINED Function, the GAS alias resolves to `even_function+1`, the slot stays `/undefined4` length4 with identical bytes, operand0 has exactly the named equate and zero references, and exporter output is exactly `.word <alias>`.

### 3.2 REF target summary

| target | slot count | target action |
|---|---:|---|
| gDuelCardCtxBase | 3 | reuse existing global |
| gEquipLpScoreBase | 1 | reuse existing global |
| gEquipZoneRankState | 6 | reuse existing global |
| gDuelFieldSlots | 6 | reuse existing global |
| gP1HandSlotArray | 1 | reuse existing global |
| gate_guardian_material_cids | 1 | create global table label + carve |
| valkyrion_material_cids | 1 | create global table label + carve |

The three callback values are `0x080a839d`, `0x080a840d`, and `0x080a8479`; their even entries `0x080a839c`, `0x080a840c`, and `0x080a8478` are existing USER_DEFINED Functions. Keep the stored low bit through `name_1 = name+1`; do not create Labels, Data or Functions at odd addresses.

### 3.2.1 Read-only prestate evidence and target contract

Fresh headless command `analyzeHeadless.bat <repo>/ghidra "Yu-Gi-Oh WCT 2006" -process 2343.gba -noanalysis -readOnly -scriptPath <run> -postScript F13Seg7ProposalPrestate.py <result>` exited 0 with marker `F13_SEG7_PROPOSAL_PRESTATE_READONLY_OK targets=8 REF=19 RENAME=4`. Evidence is `output/refine-run-20260831-194634/f13-seg7-ghidra-prestate.json`; its gate records the exact 15-file DB manifests before/after and `dbExact=true`. This is read-only proposal evidence, not a completed Mode B dry/apply claim.

All eight target addresses currently have exactly one Global primary Label, alias count0, `/undefined4` Data length4 at the exact four-byte span, no Instruction and no Function at the target address. RAM bytes are unavailable because the block is uninitialized; ROM table first-word bytes are frozen below. Post keeps every Data object/type/span and all bytes unchanged. Four existing USER_DEFINED labels and `gP1LifePoints` keep their exact IDs. Three dynamic DEFAULT labels are normalized at the same address to the approved USER_DEFINED name; their dynamic ID is expected to materialize as a new persistent ID, which must be recorded in the provisional receipt and remain identical in fresh persisted check. No alias or second Symbol is allowed.

| address | exact pre primary `id/name/source/type/ns/primary` | post primary | Data pre/post |
|---|---|---|---|
| `0x0201e2a0` | `18879/gDuelCardCtxBase/USER_DEFINED/Label/Global/true` | same object and ID | `/undefined4`,4,`[0201e2a0,0201e2a4)` |
| `0x0201afe0` | `30393/gEquipLpScoreBase/USER_DEFINED/Label/Global/true` | same object and ID | `/undefined4`,4,`[0201afe0,0201afe4)` |
| `0x0201e4d0` | `4611686018461066448/DAT_0201e4d0/DEFAULT/Label/Global/true` | unique `gEquipZoneRankState/USER_DEFINED/Label/Global/true`; receipt/persisted ID exact | `/undefined4`,4,`[0201e4d0,0201e4d4)` |
| `0x0201c4e0` | `15545/gP1LifePoints/USER_DEFINED/Label/Global/true` | same object and ID | `/undefined4`,4,`[0201c4e0,0201c4e4)` |
| `0x0201c510` | `20369/gDuelFieldSlots/USER_DEFINED/Label/Global/true` | same object and ID | `/undefined4`,4,`[0201c510,0201c514)` |
| `0x0201c8f8` | `21609/gP1HandSlotArray/USER_DEFINED/Label/Global/true` | same object and ID | `/undefined4`,4,`[0201c8f8,0201c8fc)` |
| `0x09e47898` | `4611686018593355928/DAT_09e47898/DEFAULT/Label/Global/true`, bytes `19110000` | unique `gate_guardian_material_cids/USER_DEFINED/Label/Global/true`; receipt/persisted ID exact | `/undefined4`,4,`[09e47898,09e4789c)` |
| `0x09e478a4` | `4611686018593355940/DAT_09e478a4/DEFAULT/Label/Global/true`, bytes `88120000` | unique `valkyrion_material_cids/USER_DEFINED/Label/Global/true`; receipt/persisted ID exact | `/undefined4`,4,`[09e478a4,09e478a8)` |

### 3.2.2 Nineteen REF source-slot contracts

Each source slot currently has the exact dynamic DEFAULT primary Label ID below, `/undefined4` Data length4 on `[slot,slot+4)`, the listed bytes, zero outgoing references, zero equates and no EOL. Post permits the dynamic slot Symbol to materialize once as the listed Global USER_DEFINED primary Label; its new persistent ID is captured in the receipt and must match the fresh persisted query. Data identity/type/span/bytes remain unchanged. Post references-from is exactly one tuple `(from=slot,to=target,operand=0,type=DATA,source=USER_DEFINED,primary=true)` whose target primary is the section 3.2.1 approved Symbol; non-target reference set stays empty. Exporter output must be exactly `.word target_symbol` at each row.

| slot | pre primary ID | post slot label | target | bytes | pre refs |
|---|---:|---|---|---|---:|
| `0x080a3978` | `4611686018562275704` | `ptr_gduelcardctxbase_080a3978` | `gDuelCardCtxBase` | `a0e20102` | `0` |
| `0x080a39b0` | `4611686018562275760` | `ptr_gduelcardctxbase_080a39b0` | `gDuelCardCtxBase` | `a0e20102` | `0` |
| `0x080a3a20` | `4611686018562275872` | `ptr_gduelcardctxbase_080a3a20` | `gDuelCardCtxBase` | `a0e20102` | `0` |
| `0x080a3a28` | `4611686018562275880` | `ptr_gequiplpscorebase_080a3a28` | `gEquipLpScoreBase` | `e0af0102` | `0` |
| `0x080a3ac8` | `4611686018562276040` | `ptr_gequipzonerankstate_080a3ac8` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a3b30` | `4611686018562276144` | `ptr_gequipzonerankstate_080a3b30` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a3c10` | `4611686018562276368` | `ptr_gequipzonerankstate_080a3c10` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a3c8c` | `4611686018562276492` | `ptr_gequipzonerankstate_080a3c8c` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a3d54` | `4611686018562276692` | `ptr_gequipzonerankstate_080a3d54` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a3e90` | `4611686018562277008` | `ptr_gate_guardian_material_cids_080a3e90` | `gate_guardian_material_cids` | `9878e409` | `0` |
| `0x080a3e9c` | `4611686018562277020` | `ptr_gduelfieldslots_080a3e9c` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a3f8c` | `4611686018562277260` | `valkyrion_material_cids_ptr_080a3f8c` | `valkyrion_material_cids` | `a478e409` | `0` |
| `0x080a3f98` | `4611686018562277272` | `ptr_gduelfieldslots_080a3f98` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a4030` | `4611686018562277424` | `ptr_gduelfieldslots_080a4030` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a40a0` | `4611686018562277536` | `ptr_gequipzonerankstate_080a40a0` | `gEquipZoneRankState` | `d0e40102` | `0` |
| `0x080a4340` | `4611686018562278208` | `ptr_gduelfieldslots_080a4340` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a4430` | `4611686018562278448` | `ptr_gduelfieldslots_080a4430` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a4550` | `4611686018562278736` | `ptr_gduelfieldslots_080a4550` | `gDuelFieldSlots` | `10c50102` | `0` |
| `0x080a45dc` | `4611686018562278876` | `ptr_gp1handslotarray_080a45dc` | `gP1HandSlotArray` | `f8c80102` | `0` |

### 3.2.3 Four RENAME source-slot contracts

Each row has one dynamic Global primary DEFAULT pointer label with the exact ID below, `/pointer` Data length4 on `[slot,slot+4)`, bytes `e0c40102`, and exactly one existing reference `(to=0201c4e0,operand=0,type=DATA,source=DEFAULT,primary=true,targetID=15545)`. Post changes only the slot name to the listed Global USER_DEFINED primary Label; it must retain `/pointer` Data, bytes and the complete reference tuple/object set unchanged. No equate, alias or additional reference is allowed; exporter output is exactly `.word gP1LifePoints`.

| slot | pre primary ID | post slot label |
|---|---:|---|
| `0x080a392c` | `4611686018562275628` | `ptr_g_p1_life_points_080a392c` |
| `0x080a3a78` | `4611686018562275960` | `ptr_g_p1_life_points_080a3a78` |
| `0x080a40fc` | `4611686018562277628` | `ptr_g_p1_life_points_080a40fc` |
| `0x080a45d4` | `4611686018562278868` | `ptr_g_p1_life_points_080a45d4` |

## 4. 数据块分类与 carve

The Seg-7 interval itself contains no ROM_INCBIN or `.byte` block, so there is no local block eligible for R4 or Rule 3.

| dependency block | full-ROM ref-scan | contents | decision |
|---|---|---|---|
| `[0x09e47898,0x09e478a4)` 12B | raw `0x09e47898`: one hit at `0x080a3e90`; THUMB|1: zero | `0x1119,0x111a,0x111b` = Sanga, Kazejin, Suijin | carve `gate_guardian_material_cids` |
| `[0x09e478a4,0x09e478b0)` 12B | raw `0x09e478a4`: one hit at `0x080a3f8c`; THUMB|1: zero | `0x1288,0x129b,0x12b8` = Alpha, Beta, Gamma | carve `valkyrion_material_cids` |

Both ranges sit inside `asm/rom.s:1514`, whose current `ROM_INCBIN` is offset `0x1e47894`, size `0x2478`. Landing must split it exactly as follows; the suffix size is `0x245c`:

```asm
ROM_INCBIN 0x1e47894, 0x4
gate_guardian_material_cids:
    .word SANGA_OF_THUNDER_CID
    .word KAZEJIN_CID
    .word SUIJIN_CID
valkyrion_material_cids:
    .word ALPHA_MAGNET_WARRIOR_CID
    .word BETA_MAGNET_WARRIOR_CID
    .word GAMMA_MAGNET_WARRIOR_CID
ROM_INCBIN 0x1e478b0, 0x245c
```

The tables are data, not code: their six values are valid CIDs, consumers use `ldmia/stmia`, and neither table address has a THUMB reference. No R4 disassembly is authorized.

## 5. 新增 constants 与 aliases

Add exactly seven CID constants to `constants/card_info.inc` after verifying no symbol with the same card identity exists:

```asm
.equ WALL_OF_REVEALING_LIGHT_CID,       0x00001766
.equ ANTEATEREATINGANT_CID,             0x000019c8
.equ GRAND_TIKI_ELDER_CID,              0x000013e5
.equ XZ_TANK_CANNON_CID,                0x000015f9
.equ W_WING_CATAPULT_CID,               0x0000194b
.equ ELEMENTAL_HERO_NECROSHADE_CID,     0x0000197f
.equ KAZEJIN_CID,                       0x0000111a
```

Add exactly four field-domain constants to `constants/duel_field.inc`:

```asm
.equ EQUIP_SCORE_DISPLAY_SLOT_12D,          0x0000012d
.equ EQUIP_SCORE_DISPLAY_FIELD_12F,         0x0000012f
.equ EQUIP_ACTIVATION_CARD_ID_MASK,         0x00007fff
.equ EQUIP_ACTIVATION_CARD_ID_CLEAR_MASK,   0xff8000ff
```

Add exactly three GAS aliases to `asm/rom.s`:

```asm
.equ check_equip_target_slot_eligible_by_field6_eq17_1, check_equip_target_slot_eligible_by_field6_eq17+1
.equ check_equip_target_slot_eligible_by_field9_eq4_field6_eq16_1, check_equip_target_slot_eligible_by_field9_eq4_field6_eq16+1
.equ check_equip_target_slot_eligible_by_whitelist_or_special_1, check_equip_target_slot_eligible_by_whitelist_or_special+1
```

`KAZEJIN_CID` is used only by the carve and is therefore absent from the 26 NEW slot rows. Total new definitions are `11 constants + 3 aliases + 2 table labels = 16`.

## 6. PLATE 与 EOL 计划

Apply the following fourteen full PLATE rewrites. Each execution string is ASCII and below 500 bytes: ten in module13, one caller ripple in module04, and three external rewrites in modules02/12/23.

### 0x080a3c2c check_banisher_sensitive_summon_allowed

```text
Checks whether the r1 summon card can satisfy its field-slot requirement for player r0 while Banisher of the Light is absent. Dispatches Uria, Hamon, and Anteatereatingant to three Thumb callbacks and scans slots 0..10. Writes gEquipZoneRankState and returns 1 when the requirement is met, else 0. Called from 0x080a50a0. Inputs: r0=player_side, r1=card_id. Confidence: high.
```

### 0x080a3d0c scan_activatable_equip_slots_alt

```text
Initializes gEquipZoneRankState from player r0 and card context r1, then scans both players and slots 0..4 with check_equip_slot_pair_can_activate_alt. Returns 1 at the first accepted pair, else 0. The callee name is current and semantic. Confidence: high.
```

### 0x080a3d74 check_neo_bubbleman_summon_allowed

```text
Checks the Neo Bubbleman summon setup for player r0. Requires Banisher of the Light to be absent and at least one valid Metamorphosis pair, then delegates to scan_activatable_equip_slots_alt with card context r1. Returns a boolean and may update gEquipZoneRankState through the delegate. Exclusive caller: 0x080a50aa for card 0x19a6. Confidence: high.
```

### 0x080a3dac check_gate_guardian_summon_allowed

```text
Checks whether player r0 can satisfy the Gate Guardian summon setup. Requires Mask of Restrict to be absent, copies the Sanga, Kazejin, and Suijin CID table, scans both players' field slots for usable matching materials, and requires the resulting available-slot/material count to exceed 3. Returns 1 when allowed, else 0. Read-only. Callers dispatch Gate Guardian card 0x111c. Confidence: high.
```

### 0x080a3eb4 check_valkyrion_summon_allowed

```text
Checks whether player r0 can satisfy the Valkyrion summon setup. Requires Mask of Restrict to be absent, copies the Alpha, Beta, and Gamma Magnet Warrior CID table, scans both players' field slots for usable matching materials, and applies the material-pair count gate. r10 is the current table CID, not an input. Returns 1 when allowed, else 0. Read-only. Callers dispatch Valkyrion card 0x138a. Confidence: high.
```

### 0x080a4134 check_fusion_material_pair_slots_exist

```text
Checks whether player r0 has the required unpaired material slots for fusion card r1. Dispatches the XZ, YZ, XYZ, VW, and VWXYZ fusion cluster and tests the corresponding V/W/X/Y/Z materials with count_unpaired_slots_for_card. Returns 1 when the required material combination exists, else 0. Read-only. Confidence: high.
```

### 0x080a422c get_special_summon_material_rule_by_card_id

```text
Maps special-summon monster card_id r0 to material rule 0..3. The keys cover elemental spirits, Chaos monsters, Fenrir, Dark Necrofear, Megarock Dragon, and Doom Dozer. Rule 0 means this classifier has no dedicated rule. Leaf function with no side effects. Callers: 0x08094f5a and 0x080a42c4. Confidence: high.
```

### 0x080a42b0 check_special_summon_material_rule_satisfied

```text
Checks whether player r0 can satisfy the dedicated special-summon material rule for card_id r1. Gets rule 0..3 from get_special_summon_material_rule_by_card_id, applies zone and chain gates, scans five field slots, and falls back to dispatch_effect_handler_by_card_id for rule 0. Returns 1 when the summon setup is accepted, else 0. Confidence: high.
```

### 0x080a4574 check_necroshade_normal_summon_available

```text
Checks whether a normal-summon placement for player r0 and slot r1 can use Elemental Hero Necroshade. Requires an available monster slot and equip bonus above 4, then scans gP1HandSlotArray for Necroshade card 0x197f and rejects an existing matching zone-0xb effect node. Returns a boolean and has no writes. Exclusive caller: 0x080a49e4. Confidence: high.
```

### 0x080a4694 eval_card_placement_flags_default

```text
Wrapper for eval_card_placement_flags_for_ai with fixed chain_check_flag r2=1. Passes player_side in r0 and the caller parameter in r1, then returns the placement flags unchanged. The delegated function name is current and semantic. Confidence: high.
```

### 0x08033610 count_monster_slots_accepting_card (module02 ripple)

```text
Counts monster-zone slots 0..4 for player r0 that accept a new card placement. Calls check_monster_slot_accepts_card for each slot and returns the number of accepted slots in r0, range 0..5. Counting sibling of count_available_monster_slots. Called by check_equip_card_activation_valid and check_banisher_sensitive_summon_allowed. Input: r0=player_side. Confidence: high.
```

### 0x0804154c tick_spell_equip_zone_display_seq (module04 ripple)

```text
Handles duel display sequence case 0x44 for a spell or equip field slot. Reads the player, slot and packed flags from the display state, writes applicable display-index bits, and calls write_special_summon_material_rule_display_bit with the current field-slot card ID. Marks the field slot active, dispatches display operation 0x24, and clears the step-lock field. Confidence: high.
```

### 0x08094f58 write_special_summon_material_rule_display_bit (module12 ripple rename)

```text
Tests whether card_id r0 has a dedicated special-summon material rule. Calls get_special_summon_material_rule_by_card_id; if the result is nonzero, calls write_card_display_index_with_bit_offset with display index 0x1a and bit value 1. Returns without writing when the rule is 0. Input: r0=u16 card_id. Returns: void. Confidence: high.
```

### 0x0810e5e4 invoke_r7 (module23 ripple)

```text
Single-instruction function-pointer trampoline: executes bx r7 to jump to the target held in r7. r7 is a non-APCS callee-save register set by callers. Called from duel-field zone-slot chain traversal at 0x08030048/0x0803009c, count_matching_monster_zone_slots at 0x08033214, and check_banisher_sensitive_summon_allowed at 0x080a3c2c. Confidence: high.
```

Set exactly the 96 slot EOL strings from `F13-Seg-7.slots.tsv`. Do not write CJK into Ghidra comments. No instruction-level EOL outside those 96 slot addresses is requested. A fixed-string scan of all nine pre-rename names plus `FUN_08094f58` across formal `asm/*.s` must be zero after landing; the minimum approved PLATE scope is module02 at `0x08033610`, module04 at `0x0804154c`, module12 at `0x08094f58`, module13 at the ten entries above, and module23 at `0x0810e5e4`.

The exact nine-name fixed-string set is `check_banisher_of_light_activatable`, `check_banisher_pair_activation_allowed`, `check_equip_set_activatable_for_player`, `eval_equip_card_placeable_for_player`, `check_ritual_fusion_pairable_slots_exist`, `classify_spell_card_activation_type`, `eval_spell_card_activation_placeable`, `check_equip_slot_has_field_spell_target`, and `write_spell_activation_type_display_bit`. `FUN_08094f58` is a separate mandatory-zero legacy auto-name scan. The receipt records `fixed_old_name_scan=9` only when all nine named strings and the additional auto-name string are absent from formal asm.

## 7. Direct-edge closure

The full ledger has 305 rows: 226 targets remain inside Seg-7 and 79 edges reach 34 unique existing Functions outside Seg-7. External targets and counts are:

`0802fc90:3, 0802fd60:1, 0803279c:7, 08032e20:1, 08032fa4:8, 080333ac:5, 080335b8:6, 08033610:2, 08033634:2, 08033688:2, 08033730:7, 080337f0:1, 080339d8:1, 080377b0:2, 08037a2c:2, 0803abf0:2, 0803b1a4:1, 0803b230:1, 0803bb7c:2, 0803bc24:2, 0808dab0:3, 08093534:3, 08094664:1, 080a46a0:1, 080a533c:1, 080a5498:1, 080a5714:1, 080a57b8:1, 080a80a8:1, 080ac028:1, 080eedf8:2, 080eee24:1, 0810e5e4:1, 0810e604:3`.

Every one of these 34 targets exists in `temp/ghidra-functions.csv`; none lands in an active §5.1 range or an unapproved address. The edge to `0x080a46a0 eval_card_placement_flags_for_ai` is the exact end-boundary call from `0x080a4698`; it does not authorize Seg-8 body edits. The three odd callback literals are indirect Thumb values, covered by operand-0 EQ plus GAS aliases in sections 3 and 5; they create no Ghidra DATA reference or odd-address Symbol.

## 8. Landing, source scope and rollback contract

Mode A stops at this revised proposal, unchanged TSV and read-only evidence. Reviewer must independently re-scan the 96 slot addresses, the two data table addresses, the 305 direct edges, CID identities, all nine rename claims, 14 PLATE texts and the executable recovery contract before PASS. No Mode B script materialization or real mutation is authorized by this document alone.

After a reviewer PASS, Mode B is fail-closed and must execute in this dependency order:

1. **Physical DB backup.** Before any Ghidra write, copy the complete current `ghidra/Yu-Gi-Oh WCT 2006.rep` directory to a new timestamped physical `.rep.bak-<timestamp>-pre-F13Seg7`. Build sorted manifests for current and backup using relative path, file size and SHA256; each side must contain exactly the same 15-file set and all 15 entries must match. Preserve this backup until all landing gates finish. No Git operation is a DB backup.
2. **Complete source baseline.** Before dry/apply/export, enumerate and physically copy every potentially touched formal path: all 25 `asm/NN_*.s`; every present `asm/*.s` including `all.s`, `rom.s`, `includes.inc`, header/crt0/structs; every `constants/*.inc`; `doc/dev/naming-proposals.csv`; the Function-symbol registry (`tools/ghidra-labeling/RenameKnownFunctions.py`); all four inventories (`temp/ghidra-functions.csv`, `-renamed.txt`, `-auto.txt`, `-summary.md`); activity and total progress docs; and the final Seg-7 script/plan/evidence paths. Record for every allowlisted path whether it was present plus size/SHA256, and store a physical copy of every present file. Also enumerate prestate-absent formal outputs so rollback can delete files created by this landing. The allowlist includes modules02/04/12/13/23, `asm/rom.s`, `constants/card_info.inc`, `constants/duel_field.inc`, CSV/registry/inventory/docs; every other formal path must remain byte-identical to baseline.
3. **Freeze inputs, then fresh dry.** After final review, freeze SHA256 for proposal, TSV, review, refscan, functions/body ledger, direct-edge ledger, layout, read-only prestate result/gate, generated plan and script. If review changes, regenerate plan/script/baseline and refreeze in that dependency order. Start a fresh headless process with literal flags `-noanalysis -readOnly`; record the full command, exit code0 and success marker. Its before/after DB manifests must be byte-identical 15/15. Dry requires `FAIL=0` and checks all 96 slots (`EQ73/REF19/RENAME4`), eight targets, four preserved RENAME refs, 22 segment Functions/65 body ranges, both external Function contracts in section2.3, two carve targets, nine renames, 14 PLATE strings, 305 edges, exact ROM values, no odd-address Symbols/refs, no R4 and no Rule3.
4. **One transaction and provisional receipt.** Reject and remove any old Seg-7 receipt/check outputs before apply. Run all Ghidra semantic actions and the full postcheck in one transaction: 73 EQ, 19 REF, 4 RENAME, 96 EOL, nine Function renames and 14 PLATE rewrites. Any exception or failed assertion calls transaction rollback. The apply process is accepted only with process exit0, exact transaction-commit marker, provisional receipt status/FAIL/hash/counts matching the exact expected set `EQ=73,REF=19,RENAME=4,EOL=96,FUNC_RENAME=9,PLATE=14,CARVE=2,FIXED_OLD_NAME_SCAN=9`, and a DB manifest change from prestate. A receipt with a missing, extra or mismatched count, or without every other gate, has no authority.
5. **Fresh persisted check before export.** Immediately launch a separate `-noanalysis -readOnly` process. It must validate the provisional receipt first, then reproduce the complete semantic poststate: all slots/Data/refs/equates/EOL, target and slot Symbol identities, nine Function IDs/names/APCS/bodies, 14 PLATEs, carve-target preconditions and edge/layout invariants. It must report `PERSISTED_EXACT`, exit0 and a success marker; DB manifests before/after this query must be identical 15/15. Export is forbidden before this gate passes.
6. **Source projection and pipeline.** Only after persisted PASS, add exactly 11 constants, three GAS aliases and the two 12-byte table carves; export full `0x080000c0..0x084c7637`, remove only known standalone modes, run `inject_modes.py` and `split_all_s.py`, and verify all 25 boundaries. Projection must be restricted to modules02/04/12/13/23 plus approved `rom.s`/constants/CSV/registry/inventory/docs. Module02 and23 change only their ripple PLATEs; module04 changes only the full PLATE at `0x0804154c` and its call projection at `0x080415be`; module12 changes the Function definition/PLATE at `0x08094f58` and its `0x08094f5a` call projection; module13 carries the eight in-segment renames and ten PLATEs. Full fixed-string scan of all nine old Function names plus `FUN_08094f58` in formal asm must be zero; Seg-8 body at/after `0x080a46a0` remains unchanged.
7. **Inventory, build and completion.** Synchronize exactly nine existing CSV address rows by changing only each `name` cell. Update the eight existing Seg-7 registry tuples and insert exactly one nonduplicate `FUN_08094f58` tuple; no historical CSV row may be created. Regenerate the four inventories from the persisted DB. Require exporter checks for `080415be -> write_special_summon_material_rule_display_bit`, `08094f58` final definition and `08094f5a -> get_special_summon_material_rule_by_card_id`, with no old-name text. Run `python tools/rom-export/export_all.py` and require all steps PASS, then `NOPAUSE=1 build.bat`. Require `output/2343.gba` size `33554432`, `fc /b` exit0, byte-for-byte equality with `roms/2343.gba`, and SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`. Only after source-scope, inventory and ROM gates all pass may activity/total progress be marked complete and a final non-provisional landing receipt be written.
8. **Recovery on any failure.** A failure in transaction, save, receipt, fresh persisted check, export, source edit, carve, inventory, CSV/registry, build, ROM or scope immediately stops the pipeline. Delete/ignore provisional receipt and restore current `.rep` physically from the 15-file backup, removing any extra DB generations before verifying exact relative-path/size/SHA256 equality. Restore every baseline-present formal path byte-for-byte from its physical snapshot and delete every baseline-absent formal path created by the landing. Then run a fresh `-noanalysis -readOnly` prestate check and require DB query before/after 15/15 equality plus complete semantic prestate `FAIL=0`. Do not write completion progress, stage or commit after a failure.

Acceptance requires: `EQ=73`, `REF=19`, `RENAME=4`, slot EOL=96, Function create/delete=0, Function rename=9, PLATE rewrite=14, carve=2 ranges/24 bytes, R4=0, §5.1=0, direct edges=305, new definitions=16, no old renamed Function symbol/text, no odd callback target mutation, all Ghidra comments ASCII, exact source inventory convergence, and byte-identical ROM output.

Do not stage or commit in executor, reviewer or fixer landing work unless the user separately authorizes it.

## 9. C1-C13 self-check matrix

| criterion | proposal evidence |
|---|---|
| C1 inventory | 22 Functions and 96 slots exactly; DAT92/PTR4 |
| C2 raw/THUMB scan | 96 slot-address pairs plus two carve addresses recorded |
| C3 block classification | no local blocks; two referenced external data tables carved |
| C4 ROM values | every TSV original value checked little-endian; table words listed |
| C5 constant reuse | 70 REUSE rows; 11 new constants are domain-distinct or absent |
| C6 consumer semantics | `f13-seg7-consumers.tsv` plus exact asm/card-stats lines |
| C7 target references | 19 operand-0 DATA refs plus four preserved RENAME refs have per-target/per-slot Symbol/Data/ref/exporter contracts; three odd callbacks are EQ only |
| C8 names/comments | nine misnames fixed; two additional in-segment PLATEs plus three external ripple PLATEs; 14 total, ASCII only |
| C9 body integrity | 22 existing bodies frozen as 65 exact ranges; no Function creation |
| C10 edge closure | all 305 direct edges classified; no §5.1 or unknown target |
| C11 source projection | modules02/04/12/13/23, rom.s, constants, CSV/registry/inventory/docs and unchanged-file allowlist enumerated |
| C12 build identity | standard export/build plus byte-for-byte and SHA1 ROM comparison |
| C13 rollback | physical `.rep` 15/15, complete present/absent source snapshot, one transaction, fresh read-only, receipt/marker and exact restore contract |

## Executor Report: F13-Seg-7

- 槽: `EQ=73 REF=19 RENAME=4 FUNC_RENAME=9 PLATE=14 EOL=96`
- `carve=2 ranges / 24 bytes; disasm=0; §5.1=0`
- 新增 constants/aliases/labels: `11 / 3 / 2`
- Functions: `22 segment preserve-body; rename=9 including external 08094f58; create=0`
- direct edges: `305 = B60 + Bcc163 + BL82`
- 求助: none
- proposal: `doc/dev/refine/F13-Seg-7.proposal.md`

## Mode A Fix Report

- #1 applied: odd callbacks `080a3cb0/3cbc/3cfc` are EQ-only; final slot counts are `73/19/4`; eight target and all 19 REF/four RENAME object contracts are frozen from fresh read-only evidence.
- #2 applied: `080a3dac` and `080a3eb4` are high-confidence Gate Guardian/Valkyrion renames with exact bodies, APCS, callers, CSV/registry and ASCII PLATE contracts; the in-segment rename count is8 and Round2 raises the landing total to9.
- #3 applied and Round2-extended: module02 `08033610`, module04 `0804154c`, module12 `08094f58` and module23 `0810e5e4` are full ASCII PLATE rewrites; approved formal projection is modules02/04/12/13/23 and PLATE count is14.
- #4 applied: Mode B now requires physical `.rep` 15/15 backup/restore, full present/absent source snapshots, frozen inputs, fresh read-only DB equality, one transaction, receipt/commit marker, persisted verification, full export/split/export_all/build/fc/SHA gates and unconditional recovery on every failure stage.
- Round2 #1 applied: external `08094f58` is renamed to `write_special_summon_material_rule_display_bit` with `r0=u16 card_id`, same ID/body/Symbol contract, exact ASCII PLATE, CSV/registry/exporter rules, and a new full ripple PLATE at module04 `0804154c`. Final scope is modules02/04/12/13/23, `FUNC_RENAME=9`, `PLATE=14`, and the fixed-string old-name scan set has nine Function names plus `FUN_08094f58`.
- Fixer Mode A Round2 done, 1 item applied; BLOCKED=none. TSV is unchanged. No Mode B materialization or formal landing was performed.
