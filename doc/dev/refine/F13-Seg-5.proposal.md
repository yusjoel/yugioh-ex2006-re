# Refine Proposal: F13-Seg-5 + controlled historical closure

Landing scope: historical R4 reopen `[0x080a0b20..0x080a1338)`, original Seg-5 `[0x080a1658..0x080a27a0)`, and the existing caller at `0x08094d30`. The one generated target Symbol at `0x080a38f8` is a frozen cross-edge projection described in section 7.2; its four bytes and listing type are outside the mutable scope.

## 0. 结论

- 原 Seg-5 范围: [0x080a1658,0x080a27a0), 0x1148 = 4424 bytes; 扩大闭包只增加历史块 [0x080a0b20,0x080a1338), 0x818 = 2072 bytes, 以及已有 caller 0x08094d30.
- 原 Seg-5 既有 Function=38，其中 0x080a1658 改名为 tick_equip_display_row_by_type；新建 Function=3 (0x080a0b20, 0x080a1f68, 0x080a24cc)。全局 Function 计数从 5209 精确变为 5212。
- 原自动槽=108 个 4-byte 槽: DAT=52, DWORD=36, PTR=20. DAT_080a1720 与 DAT_080a2018 是裸块头, 不计入 108.
- 原 Seg-5 的 31 个 R4 code ranges、70 个 R4/dataization 新增槽和 178 槽合同全部保留。历史闭包新增 49 个 R4 code ranges、71 个 pool slots。合计 R4=4 top-level regions / 80 code ranges / 1231 instructions / 2640 code bytes，R4/dataization 新增槽=141，最终槽覆盖=249。
- 动作: EQ=190, REF=33, RENAME=26, FUNC_RENAME=1, PLATE=10, EOL=250 (249 slot + one instruction). TSV reuse_status=224 REUSE + 25 NEW.
- 块: R4 disasm=4 top-level regions; local dataization=1 range; Rule 3 / §5.1=2 ranges; rom.s carve=0. 历史 [0x080a0b20,0x080a1338) 不再属于 §5.1，且没有残余子区间。
- BLOCKED: none.
- 权威逐槽表: doc/dev/refine/F13-Seg-5.slots.tsv, 249 data rows.
- TSV SHA256: ff0425315b47c77c8576776d66abfe01d8415acdb1cda3c3f3bc7ab4d64d4664.
- 直接边证据: output/refine-run-20260831-194634/F13-Seg-5-expanded-direct-edges.tsv, 375 data rows, SHA256 88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a.

## 1. 段测绘

### 1.1 Function entries

temp/ghidra-functions.csv 给出下列 38 个既有 Function; 入口均与 ROM Thumb push 相符:

| address | name |
|---|---|
| 080a1658 | tick_equip_display_row_by_type (from check_equip_target_slot_state) |
| 080a1968 | commit_lp_display_row_to_sprite |
| 080a1a00 | set_lp_display_row_fields |
| 080a1a38 | setup_lp_display_row_with_data |
| 080a1a78 | enqueue_lp_display_row_if_enabled |
| 080a1aa4 | set_lp_row_type1_with_attr_flags |
| 080a1ae8 | set_lp_display_row_if_nonzero |
| 080a1b00 | set_lp_row_type2_with_nonzero_flag |
| 080a1b1c | set_lp_row_type2_with_attr_flags |
| 080a1b58 | set_lp_row_type2_with_sign_flags |
| 080a1b90 | set_lp_row_type2_with_sign_flag_only |
| 080a1bc0 | apply_lp_delta_if_slot_active |
| 080a1c18 | set_lp_row_type4_with_value |
| 080a1c2c | set_lp_display_row_type5 |
| 080a1c48 | set_lp_row_type6_with_value |
| 080a1c5c | set_lp_display_row_type6 |
| 080a1c78 | set_lp_display_row_type8 |
| 080a1c94 | set_lp_row_type8_with_byte_flags |
| 080a1cb4 | set_lp_display_row_type9 |
| 080a1cd0 | set_lp_row_type7_if_opponent_linked |
| 080a1d04 | set_lp_display_row_all_slots |
| 080a1d18 | set_lp_display_row_type15 |
| 080a1d34 | set_lp_row_type11_with_byte_flags |
| 080a1d50 | set_lp_row_type10_with_value |
| 080a1d64 | set_lp_display_row_type14 |
| 080a1d80 | set_lp_display_row_type12 |
| 080a1d9c | setup_lp_row_type12_from_array |
| 080a1de8 | set_lp_row_type16_with_player_id |
| 080a1e0c | enqueue_lp_display_row_type17 |
| 080a1e30 | set_lp_row_type18_with_value |
| 080a1e44 | set_lp_row_type18_with_decremented_value |
| 080a1e64 | set_lp_display_row_type19 |
| 080a1e80 | check_equip_slot_eligibility_extended |
| 080a2234 | tick_equip_lp_bar_display_phase_a |
| 080a2358 | tick_equip_lp_bar_display_phase_b |
| 080a24f0 | check_equip_slot_card_stat8_is_7 |
| 080a2540 | check_equip_slot_card_field5_is_nonzero |
| 080a2590 | tick_equip_activation_display_by_card_type |

新建:

| address | name | evidence |
|---|---|---|
| 080a0b20 | tick_equip_card_message_by_id | `080a18ba: f7ff f931 bl 080a0b20`; entry push/high-register save; fresh recursive closure covers all 2072 bytes |
| 080a1f68 | tick_equip_target_slot_selection_phase | BL 080a1732 -> 080a1f68; entry push {r4-r7,lr} |
| 080a24cc | check_equip_opponent_zone11_target | slot 080a25a8 = 080a24cd; body ends bx lr at 080a24ee |

### 1.2 Blocks

| block | size | source |
|---|---:|---|
| 080a0b20..080a1338 | 2072 | historical Seg-4 ROM_INCBIN, controlled §5.1 reopen |
| 080a1720..080a190a | 490 | ROM_INCBIN |
| 080a1950..080a1954 | 4 | .byte |
| 080a1dd8..080a1de8 | 16 | .byte |
| 080a1f54..080a2000 | 172 | ROM_INCBIN |
| 080a2018..080a2234 | 540 | ROM_INCBIN |

## 2. 数据块分类与 full-ROM ref-scan

扫描对块内每个 halfword 地址搜索 raw 与 address|1, 并逐项归因到机器行或结构化/raw 数据; 另查 BL、PC-relative literal、switch 与 fall-through.

| block | raw / thumb | decision | evidence |
|---|---|---|---|
| 0b20..1338 | entry 0 / 0; fresh candidate-start scan below | controlled reopen to R4 | `080a18ba: f7ff f931 bl 080a0b20` is a real machine CALL edge. The old §5.1 registration explicitly required reopening when a later real external reference appeared. Fresh recursive Thumb closure accounts for 1754B code, 284B pools and 34B zero padding, with no residual interval. |
| 1720..190a | 29 / 2 | R4 disasm | 16d4..171c 有 19 个有效 raw switch words，其中 row types 1/2 均到 1720；其余 10 raw + 2 thumb 为逐项列明的数据偶合；19 路均到 190a。 |
| 1950..1954 | 0 / 0 | referenced dataization | 18fa 的 PC-relative ldr 精确到 1950; ROM word=00001d98. |
| 1dd8..1de8 | 0 / 0 | Rule 3 / §5.1 | 有效 Thumb wrapper, 但 entry/internal 全 0 packed refs; 前函数在 1dd6 返回, 后函数从 1de8 开始; 无 branch/literal/switch/fall-through. |
| 1f54..2000 | 1 / 0 | split §5.1 + R4 | 1f54..1f68 无有效引用; 唯一 raw hit 是候选 1fee 的 raw-host 偶合. BL 1732 进入 1f68. |
| 2018..2234 | 6 / 6 | R4 disasm | 2004..2014 的五个有效 raw words 到 2018/203a/20a0/2140/217c; 另 1 raw + 6 thumb 均为数据偶合; 共享 2214..2232 尾部. |

Fresh full-ROM packed scan for the reopened closure used the 49 recursive code-range starts plus the shared epilogue candidate 080a131c. Entry 080a0b20 is raw/thumb=0/0. Among the 49 starts, only 080a0c0c (26/65), 080a0d18 (0/1), and 080a0f0c (2/3) have packed hits; every host is inside graphics/card-image/libc raw asset bytes and none is an asm machine line or structured pointer word. The internal epilogue 080a131c is raw/thumb=4/1, again only at raw asset hosts 083a0e9f, 083a9967, 083d35da, 084428ea, and 08471f87. Thus packed references contribute no entry, while the decoded CALL at 080a18ba supplies the real entry. Because the recursive partition has zero uncovered bytes, there is no child interval eligible for Rule 3.

False hits:

| candidate/mode | ROM hit | host |
|---|---|---|
| 1720/raw | 083916ab | asm/24_libc_runtime.s:10611 host 083818d8+fdd3 |
| 1724/raw | 08397a67 | same host +1618f |
| 1800/raw | 0801024f | graphics/bin/boot-ui/tilemaps/seg_08010130.bin+11f |
| 1800/raw | 09e13b4b | asm/rom.s:783 host 09dff9e4+14167 |
| 1806/raw | 08505548 | graphics/bin/card-images/palettes/tb1981.bin+8 |
| 180e/thumb | 09d7db82 | asm/rom.s:765 host 09ce822c+95956 |
| 1814/raw | 084579c9 | asm/24_libc_runtime.s:10611 host +d60f1 |
| 1818/thumb | 083efd0c | same host +6e434 |
| 1900/raw | 08010253 | graphics/bin/boot-ui/tilemaps/seg_08010130.bin+123 |
| 1900/raw | 09cf06f7 | asm/rom.s:765 host 09ce822c+84cb |
| 1900/raw | 09e13b4f | asm/rom.s:783 raw host [09dff9e4,09e246d4), offset +1416b; bytes `00 19 0a 08` |
| 1906/raw | 083bf476 | asm/24_libc_runtime.s:10611 host +3db9e |
| 1fee/raw | 0814729f | asm/24_libc_runtime.s:7838 host 0812b12c+1c173 |
| 2022/thumb | 0828e017 | asm/24_libc_runtime.s:10083 host 0825c390+31c87 |
| 2022/thumb | 084edac8 | graphics/bin/card-images/palettes/tb1224.bin+8 |
| 2024/thumb | 08431f30 | asm/24_libc_runtime.s:10611 host +b0658 |
| 2042/thumb | 087d7a14 | graphics/bin/card-images/tiles/tb0606.bin+1154 |
| 2128/thumb | 083f668e | asm/24_libc_runtime.s:10611 host +74db6 |
| 2136/raw | 08439531 | asm/24_libc_runtime.s:10611 host +b7c59 |
| 220c/thumb | 0829c478 | asm/24_libc_runtime.s:10083 host +400e8 |

## 3. R4 disasm plan

### 3.0 0b20..1338 controlled historical closure

This is a Rule-3 controlled reopen, not a retroactive declaration that the earlier scan was fabricated. The former registration said to reopen on a later real external reference; disassembling the Seg-5 row-type-15 case exposed exactly that event at `080a18ba -> 080a0b20`.

Fresh recursive Thumb closure starts only at 080a0b20 and follows fall-through, every direct B/BL, and every PC-relative LDR. It yields 49 exact half-open code ranges, 822 instructions, and 1754 code bytes:

    [0b20,0b5c) [0b6c,0b9c) [0ba8,0bba) [0bc0,0bd8) [0bdc,0bee)
    [0bf8,0c02) [0c0c,0c18) [0c1c,0c3a) [0c44,0c98) [0ca0,0d0a)
    [0d18,0d40) [0d48,0d78) [0d80,0da8) [0db8,0dc8) [0dcc,0dd8)
    [0de0,0e2c) [0e3c,0e4c) [0e50,0e5a) [0e60,0e7c) [0e80,0e8a)
    [0e90,0ea0) [0ea4,0eae) [0eb4,0edc) [0ee0,0ee4) [0ee8,0ef8)
    [0efc,0f06) [0f0c,0f28) [0f2c,0f30) [0f34,0f44) [0f48,0f4c)
    [0f50,0f80) [0f84,0f9a) [0fa0,0fa4) [0fa8,0fc8) [0fcc,0fdc)
    [0fe0,0fea) [0ff0,101e) [1024,1028) [102c,103c) [1040,104a)
    [1050,106a) [1070,107a) [1080,1096) [109c,10a4) [10a8,11b0)
    [11b8,1250) [1254,126e) [1274,12f4) [12f8,1330)

The 71 exact 4-byte pool words, 284 bytes total, are:

    0b5c=fffffcf0 0b60=0201c4e0 0b64=00001d94 0b68=00001da8
    0b9c=0201e2a0 0ba0=00001488 0ba4=000012fd 0bbc=0000140d
    0bd8=000015dd 0bf0=0000167a 0bf4=00001932 0c04=0201c4e0
    0c08=00001da8 0c18=00001da8 0c3c=00000868 0c40=00001da8
    0c98=00000868 0c9c=0201c600 0d0c=00000868 0d10=0201c4e0
    0d14=00001da8 0d40=00000868 0d44=00001da8 0d78=00001ce8
    0d7c=00001da8 0da8=00001ce8 0dac=00000868 0db0=00000bb7
    0db4=00001da8 0dc8=00001ce8 0dd8=0201c4e0 0ddc=00001da8
    0e2c=000015dd 0e30=00001488 0e34=000012fd 0e38=000010f8
    0e4c=000012c6 0e5c=000012f3 0e7c=00001368 0e8c=0000135b
    0ea0=0000139c 0eb0=0000140d 0edc=00001544 0ee4=00001519
    0ef8=0000153d 0f08=0000153f 0f28=00001593 0f30=00001590
    0f44=000015a5 0f4c=000015d3 0f80=00001717 0f9c=000015f7
    0fa4=0000161e 0fc8=00001686 0fdc=000016d3 0fec=000016df
    1020=00001841 1028=00001746 103c=000017c3 104c=00001803
    106c=00001968 107c=00001932 1098=000019c2 10a4=000019d3
    11b0=00000868 11b4=00000103 1250=00000129 1270=00000141
    12f4=09e47894 1330=0201c4e0 1334=00001d94

The 17 exact padding ranges, 34 bytes total, are `[0bba,0bbc) [0bee,0bf0) [0c02,0c04) [0c3a,0c3c) [0d0a,0d0c) [0e5a,0e5c) [0e8a,0e8c) [0eae,0eb0) [0f06,0f08) [0f9a,0f9c) [0fea,0fec) [101e,1020) [104a,104c) [106a,106c) [107a,107c) [1096,1098) [126e,1270)`; every range is exactly `00 00`.

The byte partition is exact: 1754 code + 284 pool + 34 padding = 2072 bytes. There is no overlap, gap, or residual subrange. Pool addresses are Data, padding remains undefined/alignment bytes, and no instruction may cross either class.

Create one Function at 080a0b20 named `tick_equip_card_message_by_id`. APCS signature: `u32 tick_equip_card_message_by_id(u32 player_id, u16 card_id, u16 unused_row_value)`. The body is exactly the 49 ranges above. The `bl 080a131c` at 080a0b58 reaches a shared local epilogue inside `[12f8,1330)`; 080a131c has no prologue, restores the same 0x310-byte frame and saved high registers, and is not a second Function. Normalize its target Symbol to the USER_DEFINED local label `equip_card_message_shared_epilogue`. If disassembly creates a provisional Function at 080a131c, verify its entry first, remove only that provisional Function, keep its Instructions, and include the range in the 080a0b20 Function body.

Semantic evidence is high confidence:

- Caller row-type-15 code 080a18a8..080a18be loads r0 from `[gP1LifePoints+0x1d8c]`, r1 from `[gP1LifePoints+0x1d98]`, r2 from `[gP1LifePoints+0x1d9a]`, then calls 080a0b20. Callee preserves r0 as player_id and zero-extends r1 as card_id; entry r2 is overwritten before any read.
- The callee reads `gP1LifePoints+EQUIP_PHASE_DISPLAY_STATE_OFF`. In state 0, a duel-context gate other than 1 stores phase 1 and returns 0. When that gate is 1, the card_id dispatch writes a selector/count to `LP_CARD_TRACK_BASE_OFF` using field/hand checks, occupied-zone counts, card stats, score lookup, and PRNG, then returns 1 through the shared epilogue.
- State 1 dispatches by card_id, looks up card names/game text, formats text in the 0x310-byte stack frame, invokes display op 0x31 variants, increments `EQUIP_PHASE_DISPLAY_STATE_OFF` at 080a130e..080a1318, and returns 0.
- State values above 1 copy the shared display word at offset 0x1d40 into `LP_CARD_TRACK_BASE_OFF` and return 1.

Direct BL callees and occurrence counts from the 49 ranges are: copy_game_text_if_raw=3, append_game_text_if_raw=2, format_game_text_with_text_arg=8, format_game_text_with_int_arg=2, count_occupied_monster_zones=3, check_card_field5_is_nonzero=1, lookup_equip_card_score_by_card_id_and_player=6, trigger_card_display_op31_if_not_active=8, invoke_card_display_op_0x31_sub1=7, invoke_card_display_op_0x31_with_params=1, invoke_card_display_op_0x31_sub3_with_packed_params=2, sample_prng_scaled=2, check_hand_equip_target_available_via_field_check=1, card_name_lookup_by_internal_id=5, get_game_text_ptr_by_lang_offset=1, get_game_text_ptr_by_str_type_b=1, get_card_extended_stat_field6=1, plus the internal epilogue call=1.

### 3.1 1720..190a: 19-way switch

16d4..171c stores even case addresses because mov pc,r0 preserves Thumb state. Entries: 1720,1720,1740,1764,1788,17ac,17c8,17d8,17fc,1820,183c,1858,1874,1884,18a8,18cc,18e8,18ee,18f4.

The 19 table words have 18 unique row-type entries. Create or normalize exactly these USER_DEFINED primary target labels; 1720 is shared by the first two row types and is not a case-1-only label:

| target | row-type label |
|---|---|
| 080a1720 | equip_row_type_case_1_or_2 |
| 080a1740 | equip_row_type_case_3 |
| 080a1764 | equip_row_type_case_4 |
| 080a1788 | equip_row_type_case_5 |
| 080a17ac | equip_row_type_case_6 |
| 080a17c8 | equip_row_type_case_7 |
| 080a17d8 | equip_row_type_case_8 |
| 080a17fc | equip_row_type_case_9 |
| 080a1820 | equip_row_type_case_10 |
| 080a183c | equip_row_type_case_11 |
| 080a1858 | equip_row_type_case_12 |
| 080a1874 | equip_row_type_case_13 |
| 080a1884 | equip_row_type_case_14 |
| 080a18a8 | equip_row_type_case_15 |
| 080a18cc | equip_row_type_case_16 |
| 080a18e8 | equip_row_type_case_17 |
| 080a18ee | equip_row_type_case_18 |
| 080a18f4 | equip_row_type_case_19 |

| code | padding | pools |
|---|---|---|
| 1720..1738 | - | 1738,173c |
| 1740..1758 | - | 1758,175c,1760 |
| 1764..177c | - | 177c,1780,1784 |
| 1788..17a0 | - | 17a0,17a4,17a8 |
| 17ac..17be | 17be..17c0 | 17c0,17c4 |
| 17c8..17d4 | - | 17d4 |
| 17d8..17f0 | - | 17f0,17f4,17f8 |
| 17fc..1814 | - | 1814,1818,181c |
| 1820..1832 | 1832..1834 | 1834,1838 |
| 183c..184e | 184e..1850 | 1850,1854 |
| 1858..186a | 186a..186c | 186c,1870 |
| 1874..1880 | - | 1880 |
| 1884..189c | - | 189c,18a0,18a4 |
| 18a8..18c0 | - | 18c0,18c4,18c8 |
| 18cc..18de | 18de..18e0 | 18e0,18e4 |
| 18e8..18ee | - | - |
| 18ee..18f4 | - | - |
| 18f4..190a | - | existing 194c + new 1950 |

### 3.2 1f54..2000 split

- Keep 1f54..1f68 under Rule 3: code 1f54..1f60, words 1f60/1f64, zero pad 1f66..1f68.
- Disassemble 1f68..2000 and create tick_equip_target_slot_selection_phase. Its pre-switch code body is exactly [1f68,1fba) and [1fc4,1ff8); 1fba..1fc4 and 1ff8..2004 stay outside the Function as padding/pools.
- Pools: 1fbc,1fc0,1ff8,1ffc; 2000 is pointer to table 2004.

### 3.3 2018..2234: five switch cases

Table words: 2004->2018, 2008->203a, 200c->20a0, 2010->2140, 2014->217c. These are even switch entries, not callback pointers.

| code | padding | pools |
|---|---|---|
| 2018..2056 | 2056..2058 | 2058,205c,2060,2064 |
| 2068..2096 | 2096..2098 | 2098,209c |
| 20a0..20b8 | - | 20b8,20bc |
| 20c0..20e8 | - | 20e8,20ec |
| 20f0..212a | 212a..212c | 212c,2130,2134,2138,213c |
| 2140..215c | - | 215c,2160,2164,2168 |
| 216c..2174 | - | 2174,2178 |
| 217c..219a | 219a..219c | 219c,21a0 |
| 21a4..21c6 | 21c6..21c8 | 21c8 |
| 21cc..21e0 | - | 21e0,21e4 |
| 21e8..2226 | 2226..2228 | 2228,222c,2230 |

All 11 code ranges remain blocks in the 1f68 Function. The shared return tail [2214,2226) is included inside the last [21e8,2226) range. Do not create five case Functions.

### 3.4 Exact Function-body and identity contract

- New Function 080a0b20 is tick_equip_card_message_by_id with the exact 49-range body in section 3.0. It owns 080a131c as a local shared epilogue. No pool or padding byte enters the Function body, and no second Function is created inside the closure.
- Existing Function 080a1658 keeps Function ID 16936 and entry 080a1658, changes its name to tick_equip_display_row_by_type, and receives all 18 case entries from the mapping above. Its exact normalized half-open body is `[1658,166c) [1674,169e) [16b4,16cc) [1720,1738) [1740,1758) [1764,177c) [1788,17a0) [17ac,17be) [17c8,17d4) [17d8,17f0) [17fc,1814) [1820,1832) [183c,184e) [1858,186a) [1874,1880) [1884,189c) [18a8,18c0) [18cc,18de) [18e8,194a)`. The final normalized range joins adjacent cases 17/18/19 to the existing 190a shared tail; guard all 18 entry addresses individually. Every pool and padding range in section 3.1 stays outside this Function body.
- New Function 080a1f68 is tick_equip_target_slot_selection_phase with exact body `[1f68,1fba) [1fc4,1ff8) [2018,2056) [2068,2096) [20a0,20b8) [20c0,20e8) [20f0,212a) [2140,215c) [216c,2174) [217c,219a) [21a4,21c6) [21cc,21e0) [21e8,2226)`. This includes the five computed-switch entries and shared tail [2214,2226), and excludes every pool/padding range in sections 3.2/3.3.
- New Function 080a24cc is check_equip_opponent_zone11_target with exact body `[24cc,24e4) [24ec,24f0)`. The pool words 24e4/24e8 are excluded; 24ee is the final `bx lr`.
- Call `createFunction` only for 080a0b20, 080a1f68, and 080a24cc. Add address ranges to the three dispatcher Functions through their Function bodies; no case entry or 080a131c becomes an independent Function. After apply, global Function count must be exactly 5212 from the 5209 pre-state.
- Incoming-reference guard: 080a0b20 receives exactly `080a18ba -> 080a0b20` as operand-0 UNCONDITIONAL_CALL/DEFAULT/primary with ROM bytes `ff f7 31 f9`; 080a1658 preserves exactly `08094d30 -> 080a1658`; disassembly establishes `080a1732 -> 080a1f68`; 080a24cc has no incoming reference to the even Function entry because 080a25a8 stores odd callback value 080a24cd as an equate. Guard 080a25a8 separately as `check_equip_opponent_zone11_target+1`.
- Postcheck every listed range against its Function entry/ID/body. Record the three newly allocated Function IDs in the transaction receipt and require the fresh read-only process to observe the same IDs; verify all listed pools and padding retain the proposed non-Function types.

## 4. Symbolization plan

### 4.1 TSV contract

- EQ: create target_symbol equate on the 4-byte data scalar, rename to slot_label.
- REF: remove only wrong operand-0 refs, add exactly one operand-0 DATA/USER_DEFINED/primary ref to target_symbol, then rename the slot.
- RENAME: preflight the complete operand-0 reference tuple. Preserve its target/type/source/primary fields exactly, including the no-reference pre-state at 080a25ec, then rename the slot.
- Apply eol_ascii verbatim. It is ASCII. Equates belong on pool data, never instruction operands.

| population | EQ | REF | RENAME | total |
|---|---:|---:|---:|---:|
| original | 71 | 12 | 25 | 108 |
| original Seg-5 R4/dataization | 56 | 14 | 0 | 70 |
| historical closure R4 | 63 | 7 | 1 | 71 |
| final | 190 | 33 | 26 | 249 |

The two switch-table slot-label revisions change no action category. The old 178-row contract remains byte-for-byte represented in the expanded TSV; the 71 new rows are exactly the historical closure pool words.

### 4.2 REF target LABEL-source contract

The following seven unique REF targets are independent target observations. Preserve each existing Data object exactly; create or normalize only the USER_DEFINED primary LABEL. In particular, do not create or retype Data in uninitialized RAM.

| address | required primary name | pre-state primary/source | pre-state Data | post-state contract |
|---|---|---|---|---|
| 0201c4e0 | gP1LifePoints | gP1LifePoints / USER_DEFINED | /undefined4, 4 bytes | reuse the same USER_DEFINED primary LABEL and Data |
| 0201e2a0 | gDuelCardCtxBase | gDuelCardCtxBase / USER_DEFINED | /undefined4, 4 bytes | reuse the same USER_DEFINED primary LABEL and Data |
| 0201c600 | gP1FieldArrayCBase | gP1FieldArrayCBase / USER_DEFINED | /undefined4, 4 bytes | reuse the same USER_DEFINED primary LABEL and Data |
| 0201b870 | gSpriteAttrBuf | gSpriteAttrBuf / USER_DEFINED | /undefined2, 2 bytes | reuse the same USER_DEFINED primary LABEL and Data |
| 0201e274 | gEquipPhaseDisplayState | DAT_0201e274 / DEFAULT | /undefined4, 4 bytes | create/normalize one USER_DEFINED primary LABEL; preserve the existing Data |
| 0201e28a | gLpCardTrackNext | DAT_0201e28a / DEFAULT | /undefined2, 2 bytes | create/normalize one USER_DEFINED primary LABEL; preserve the existing Data |
| 080a2004 | equip_target_select_phase_switch_table | PTR_DAT_080a2004 / DEFAULT | /undefined pointer, 4 bytes | rename the same primary Symbol object to one USER_DEFINED global table LABEL; preserve the Data |

The 33 REF rows have this exact post-state; every row is operand 0, type DATA, source USER_DEFINED, primary=true:

| slot | target |
|---|---|
| 080a0b60 | gP1LifePoints@0201c4e0 |
| 080a0b9c | gDuelCardCtxBase@0201e2a0 |
| 080a0c04 | gP1LifePoints@0201c4e0 |
| 080a0c9c | gP1FieldArrayCBase@0201c600 |
| 080a0d10 | gP1LifePoints@0201c4e0 |
| 080a0dd8 | gP1LifePoints@0201c4e0 |
| 080a1330 | gP1LifePoints@0201c4e0 |
| 080a16a8 | gDuelCardCtxBase@0201e2a0 |
| 080a16ac | gSpriteAttrBuf@0201b870 |
| 080a195c | gDuelCardCtxBase@0201e2a0 |
| 080a19f0 | gDuelCardCtxBase@0201e2a0 |
| 080a19f8 | gSpriteAttrBuf@0201b870 |
| 080a1f44 | gP1FieldArrayCBase@0201c600 |
| 080a1fc0 | gP1LifePoints@0201c4e0 |
| 080a1ff8 | gP1LifePoints@0201c4e0 |
| 080a2000 | equip_target_select_phase_switch_table@080a2004 |
| 080a2058 | gP1LifePoints@0201c4e0 |
| 080a2064 | gDuelCardCtxBase@0201e2a0 |
| 080a2098 | gP1LifePoints@0201c4e0 |
| 080a20b8 | gP1LifePoints@0201c4e0 |
| 080a20e8 | gDuelCardCtxBase@0201e2a0 |
| 080a2138 | gP1LifePoints@0201c4e0 |
| 080a215c | gP1LifePoints@0201c4e0 |
| 080a2174 | gP1LifePoints@0201c4e0 |
| 080a219c | gP1LifePoints@0201c4e0 |
| 080a21e0 | gP1LifePoints@0201c4e0 |
| 080a2228 | gP1LifePoints@0201c4e0 |
| 080a2390 | gEquipPhaseDisplayState@0201e274 |
| 080a23cc | gEquipPhaseDisplayState@0201e274 |
| 080a2448 | gLpCardTrackNext@0201e28a |
| 080a2458 | gEquipPhaseDisplayState@0201e274 |
| 080a2498 | gLpCardTrackNext@0201e28a |
| 080a2688 | gDuelCardCtxBase@0201e2a0 |

### 4.3 RENAME reference-preservation contract

The following table is the complete 26-row operand-0 pre-state. `DATA/DEFAULT/primary` and `DATA/USER_DEFINED/primary` are exact reference tuples and must survive unchanged. `none` means no reference may be created by the RENAME action.

| slot | pre-state target | pre-state ref tuple | post-state |
|---|---|---|---|
| 080a12f4 | none; numeric ROM value 09e47894 | none | preserve no-reference state; rename to equip_card_message_separator_ptr_080a12f4 only; external text bytes stay out of scope |
| 080a166c | gP1LifePoints@0201c4e0 | DATA/USER_DEFINED/primary | preserve exactly |
| 080a16d0 | PTR_DAT_080a16d4@080a16d4 | DATA/DEFAULT/primary | preserve tuple; target primary becomes equip_row_type_switch_table on the same Symbol object |
| 080a16d4 | DAT_080a1720@080a1720 | DATA/DEFAULT/primary | preserve tuple; target primary becomes equip_row_type_case_1_or_2 on the same Symbol object |
| 080a1954 | gP1LifePoints@0201c4e0 | DATA/USER_DEFINED/primary | preserve exactly |
| 080a19e0 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1a28 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1a6c | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1bf4 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1cfc | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1e04 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a1f30 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a2004 | DAT_080a2018@080a2018 | DATA/DEFAULT/primary | preserve tuple; target primary becomes equip_target_select_phase_case_0 on the same Symbol object |
| 080a225c | gP1LifePoints@0201c4e0 | DATA/USER_DEFINED/primary | preserve exactly |
| 080a238c | gP1LifePoints@0201c4e0 | DATA/USER_DEFINED/primary | preserve exactly |
| 080a24e4 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a252c | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a257c | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a25e4 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a25ec | none | none | preserve no-reference state; rename only the slot |
| 080a2690 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a26c0 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a26e0 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a2708 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a2724 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |
| 080a2790 | gP1LifePoints@0201c4e0 | DATA/DEFAULT/primary | preserve exactly |

Dry-run must inspect target primary Symbol name/address/source/Data separately from slot reference target/type/source/primary. The saved-program fresh read-only check repeats both sets independently; neither set may be inferred from exported text or from the other set.

### 4.4 Reuse

- duel_field.inc: EQUIP_PHASE_DISPLAY_STATE_OFF, EQUIP_CONTEXT_PLAYER_OFF, EQUIP_REROLL_SPRITE_PARAM_OFF, EQUIP_REROLL_COUNT_TARGET_OFF, EQUIP_ACT_SCORE_MODE_103, ATK_THRESHOLD_2999, zone_query_hand_tag_12a1.
- ewram.inc: gP1LifePoints, gDuelCardCtxBase, gP1FieldArrayCBase, gSpriteAttrBuf, P1LP_BLOCK2_OFF, LP_CARD_TRACK_BASE_OFF, LP_CARD_TRACK_NEXT_OFF, LP_CARD_TRACK_ALT_OFF, PLAYER_BLOCK_STRIDE, P1LP_BLOCK2_OFF_1CE8, LP_BANISHER_CTX_OFF, LP_EQUIP_DISPLAY_FLAG_OFF, SPRITE_ROW_BUSY_BYTE_OFF.
- card_info.inc: the original FENGSHENG_MIRROR_CID, TRAP_DUSTSHOOT_CID and SLOT_CARD_EMPTY, plus closure values GILASAURUS_CID, SOLEMN_JUDGMENT_CID, MAGIC_DRAIN_CID, DIMENSION_JAR_CID, FRIENDSHIP_CID, TRIAGE_CID, MOOYAN_CURRY_CID, cid_12c6, ULTIMATE_OFFERING_CID, SPELL_ZONE_TARGET_CARD_ID, cid_135b, PATRICIAN_OF_DARKNESS_CID, DARK_COFFIN_CID, OMINOUS_FORTUNETELLING_CID, PYRAMID_ENERGY_CID, ORDEAL_OF_A_TRAVELER_CID, AN_OWL_OF_LUCK_CID, A_CAT_OF_ILL_OMEN_CID, REVERSAL_QUIZ_CID, SECOND_GOBLIN_CID, JADE_INSECT_WHISTLE_CID, FORMATION_UNION_CID, CLIFF_THE_TRAP_REMOVER_CID, DARK_SCORPION_MEANAE_CID, cid_16d3, SPATIAL_COLLAPSE_CARD_ID, NECKLACE_OF_COMMAND_CID, VAMPIRE_LADY_CID, FAMILIAR_KNIGHT_CID, cid_1803, SILLVA_WARLORD_OF_DARK_WORLD_CID, DISCIPLE_FORBIDDEN_SPELL_CID, and DIVINE_DRAGON_EXCELION_CID.
- oam_attr.inc: OAM_EQUIP_ZONE_CHAIN_SPRITE_P2.

0x12a1 at 1f40 is the third argument to find_effect_node_in_zone, so it uses zone_query_hand_tag_12a1, not the equal-valued card CID. Evidence: constants/duel_field.inc:424 and asm/13:8519.

CID structure checks: 1509 Fengsheng Mirror at data/card-stats.s:14003-14005 and constants/card_info.inc:1438; 1546 Trap Dustshoot at data/card-stats.s:14705-14707 and constants/card_info.inc:1456.

Fresh structured-data verification for the reopened closure found all 28 named card IDs at their `slot=0x....` records in data/card-stats.s: Mooyan Curry 3915, Solemn Judgment 8894, Patrician 10584, Magic Drain 11559, Gilasaurus 12573, Ominous Fortunetelling 14172, Pyramid Energy 14588, Ordeal 14614, Dark Coffin 14679, Cat 15251, Owl 15290, Reversal Quiz 15524, Second Goblin 15914, Dimension Jar 16018, Formation Union 16278, Cliff 16681, Friendship 17578, Meanae 17734, Spatial Collapse 18735, Jade Insect Whistle 19346, Vampire Lady 19788, Familiar Knight 21049, Necklace of Command 22544, Triage 25170, Sillva 25677, Disciple 26496, Divine Dragon Excelion 26717, and Ultimate Offering 36241. Values 12c6, 135b, 16d3, and 1803 have zero `slot=` records and reuse the existing unassigned `cid_*` constants. Value 1368 is consumed as `SPELL_ZONE_TARGET_CARD_ID`, not as a card-stats record. Confidence is high for every mapping because the TSV value, constant value, structured slot or declared unassigned status, and instruction consumer agree.

### 4.5 New definitions

| file | definition | evidence |
|---|---|---|
| constants/duel_field.inc | EQUIP_CARD_MESSAGE_FRAME_NEG=0xfffffcf0 | 080a0b2a loads it and 080a0b2c adds it to sp; epilogue 080a131c restores 0x310 bytes |
| constants/duel_field.inc | EQUIP_CARD_MESSAGE_FORMAT_ID_129=0x129 | 080a1230 loads it as r1 for format_game_text_with_int_arg at 080a1238 |
| constants/duel_field.inc | EQUIP_CARD_DISPLAY_SUB_ID_141=0x141 | 080a126a loads it as r1 for trigger_card_display_op31_if_not_active at 080a127a; alternate path supplies 0x122 |
| constants/duel_field.inc | LP_EQUIP_ROW_ACTIVE_OFF=0x1d88 | asm/13:7470,7611,7677,8016 |
| constants/duel_field.inc | LP_EQUIP_ROW_TYPE_OFF=0x1d90 | asm/13:7538 switch read; 7717 writer |
| constants/ewram.inc | gEquipPhaseDisplayState=0x0201e274 | phase-B slots 2390/23cc/2458; gP1LifePoints+1d94 |
| constants/ewram.inc | gLpCardTrackNext=0x0201e28a | halfword slots 2448/2498; gP1LifePoints+1daa |

Add these GAS aliases beside the existing file-08 aliases in asm/rom.s:

    .equ check_equip_opponent_zone11_target_1, check_equip_opponent_zone11_target+1
    .equ check_equip_slot_card_stat8_is_7_1, check_equip_slot_card_stat8_is_7+1
    .equ check_equip_slot_card_field5_is_nonzero_1, check_equip_slot_card_field5_is_nonzero+1
    .equ check_equip_slot_eligibility_extended_1, check_equip_slot_eligibility_extended+1

Normalize switch Symbols without same-address aliases:

- At 080a16d4, rename the current primary `PTR_DAT_080a16d4` Symbol object itself to the single slot/table name equip_row_type_switch_table. Rename the current 080a1720 block-head Symbol itself to equip_row_type_case_1_or_2, and apply the exact case-3..19 mapping in section 3.1 to the remaining 17 unique targets.
- At 080a2004, rename the current primary `PTR_DAT_080a2004` Symbol object itself to the single slot/table name equip_target_select_phase_switch_table. Rename current target Symbols at 2018/203a/20a0/2140/217c to equip_target_select_phase_case_0..4 on the same objects.
- At 080a25f0, move/rename the current scoped ANALYSIS primary Symbol object to the global USER_DEFINED name equip_activation_card_type_switch_table. Preserve the six existing even case targets and their values.
- The 19+5+6 computed-switch words remain even. Do not create a second label at 16d4, 2004, or 25f0.

## 5. PLATE, EOL, and local dataization

Keep 37 existing Seg-5 names, rename 080a1658 as specified in section 3.4, and create the three names in section 1.1. Full-rewrite exactly these ten ASCII PLATE comments:

    080a0b20: r0=player_id; r1=card_id; r2 ignored. Row-type-15 phase at EQUIP_PHASE_DISPLAY_STATE_OFF. State 0: if the context gate is not 1, set phase 1 and return 0; otherwise compute LP_CARD_TRACK_BASE_OFF from field and hand checks, zone counts, stats, score, and PRNG, then return 1. State 1: format card text, invoke display op 0x31, advance phase, and return 0. Later: copy the shared display word to LP_CARD_TRACK_BASE_OFF and return 1. Stack frame=0x310 bytes.

    080a1658: No APCS arguments. Reads the equip display active flag, player context, and row type. If active, dispatches row types 1..19 through the even-address table at 0x080a16d4, then performs shared display-state cleanup. Returns 0 for inactive state and 1 after the active path.

    080a1968: No APCS arguments. Sets the gP1LifePoints row-active flag to 1 and clears the phase and display flags. When the stored player matches the opposing duel player and LP data is valid, copies 0x10 bytes to a stack row, calls submit_sprite_row_data with type 0x1e and count 0x12, clears gSpriteAttrBuf+0x301 bits 0/1, then sets the display flag to 1. Called by setup_lp_display_row_with_data and set_lp_display_row_fields. Returns void.

    080a1b1c: r0=LP row value, r1=row parameter, r2=attribute code. Builds flags bit0 for code 1, bit2 for code 8, bit3 for code 7, and forces bit4. Calls set_lp_display_row_fields with row type 2, low 16 bits of r1, and the flags. Tail-called by set_lp_row_type2_with_nonzero_flag. Returns void.

    080a1bc0: r0=player_id, r1=fallback row value, r2=LP delta; entry r3 is not read. If the active flag is set, the stored player matches r0, and row type is 3, adds entry r2 to the stored halfword. Otherwise calls set_lp_display_row_fields with row type 3, entry r1 as callee r2, and entry r2 as callee r3. Returns void.

    080a1e0c: r0=LP row base, r1=LP value, r2=display mode, r3=display state. Zero-extends r1 to 16 bits, combines the high-byte inputs into flags, and calls set_lp_display_row_fields with fixed row type 17. Called by tick_equip_activation_display_state and other LP render paths. Returns void.

    080a1f68: r0=player_id, r1=row value, r2=packed flag bits. Masks r2 as 0x01 for the phase-1 0x29/0xeb choice, 0x02 for the phase-4 boolean, 0x08 for phase-1 0x14, 0x10 for phase-2 mode and phase-4 branch, 0x20 for phase-1 0x3d and phase-4 path, and 0x80 for extended eligibility and phase-4 gating. Dispatches phases 0..4 through the even table at 0x080a2004. Returns 0 while active or 1 when complete.

    080a24cc: r0=player_id, r1=zone type. Returns 0x800 when r0 is the opponent of the stored equip player and r1 is 0xb; otherwise returns 0. Used as a Thumb callback by tick_equip_activation_display_by_card_type.

    080a24f0: r0=player_id, r1=target type, r2=slot index. Requires the stored equip player to differ from r0 and r1 to equal 0xb, loads the slot card ID, and calls check_card_stat_field8_is_7. Returns 0x800 on success and 0 otherwise. Called by tick_equip_activation_display_by_card_type through callback alias check_equip_slot_card_stat8_is_7_1 at 0x080a25c0. No external writes.

    080a2540: r0=player_id, r1=target type, r2=slot index. Requires the stored equip player to differ from r0 and r1 to equal 0xb, loads the slot card ID, and calls check_card_field5_is_nonzero. Returns 0x800 on success and 0 otherwise. Called by tick_equip_activation_display_by_card_type through callback alias check_equip_slot_card_field5_is_nonzero_1 at 0x080a25e0. No external writes.

All ten PLATE payloads are ASCII. Byte lengths are 0b20=456, 1658=271, 1968=431, 1b1c=282, 1bc0=308, 1e0c=280, 1f68=392, 24cc=200, 24f0=367, and 2540=375; maximum=456, below 500. TSV eol_ascii is the complete 249-item slot-EOL plan. Add exactly one non-slot EOL at 080a131c: `Shared epilogue; restores the 0x310-byte frame and saved high registers.` This payload is ASCII. No other PLATE or instruction-EOL change is approved.

Dataize 1950..1954 as one 4-byte scalar named equip_reroll_sprite_param_off_080a1950, equated to EQUIP_REROLL_SPRITE_PARAM_OFF. Consumer evidence: asm/13_equip_placement.s:7563 raw block; ROM @080a18fa (0x4a15) -> literal 080a1950. No rom.s carve.

### 5.A Function rename and generated-source synchronization

- Rename only existing Function 080a1658 from check_equip_target_slot_state to tick_equip_display_row_by_type; FUNC_RENAME=1. Preserve Function ID 16936, the incoming call tuple, and the exact expanded body contract in section 3.4.
- Full export changes the historical 0b20..1338 block and the original Seg-5 definitions in asm/13_equip_placement.s, plus the real caller operand at asm/12_equip_activation_scan.s:1604 (`08094d30: bl tick_equip_display_row_by_type`). The exact generated `SUB_080a38f8:` target label described in section 7.2 is the sole frozen projection beyond those ranges. No other caller, callee, or out-of-range assembly text change is approved.
- After the saved Ghidra change, run `ExportFunctionInventory.py` and regenerate the four real outputs: `temp/ghidra-functions.csv`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-auto.txt`, and `temp/ghidra-functions-summary.md`. The expected counts are total 5212, named 5122, auto 90: the rename keeps one named Function, while the three created named Functions enter inventory.
- Run `tools/ad-hoc/sync_ghidra_names_to_proposals.py` through its normal dry-run/apply flow. In doc/dev/naming-proposals.csv, change only the `name` cell on the existing 0x080a1658 row from check_equip_target_slot_state to tick_equip_display_row_by_type; preserve every other column and every other row.
- doc/dev/naming-proposals.csv currently has no rows for 0x080a0b20, 0x080a1f68, or 0x080a24cc. Do not create historical scoring rows for these newly created Functions.
- `tools/ghidra-labeling/RenameKnownFunctions.py` currently has no tuple for 0x080a0b20, 0x080a1658, 0x080a1f68, or 0x080a24cc. Do not fabricate missing history. If a fresh source snapshot contains a matching formal registry tuple at landing time, synchronize only its approved name and full PLATE fields and preserve all other tuple fields; otherwise leave the registry unchanged. Any conflicting tuple aborts the transaction for a new review.
- Historical eval/proposal/review evidence remains unchanged. Production-source searches must leave no exported caller/definition use of the old 080a1658 name outside those frozen historical records.

## 6. §5.1 registration

Withdraw the historical `[080a0b20,080a1338)` row only after the R4 closure passes every transaction and persisted-state gate. Until landing succeeds, the activity and total-progress documents must describe it only as `controlled reopen; R4 closure pending`, never as completed. This is the documented Rule-3 path "referenced later, then process". The closure contributes zero residual Rule-3 child ranges.

| range | size | description | proof |
|---|---:|---|---|
| 1dd8..1de8 | 16 | orphan Thumb wrapper calling set_lp_display_row_fields with row type 13 | every raw/thumb candidate 0; no control-flow or fall-through |
| 1f54..1f68 | 20 | orphan Thumb getter, two words, zero pad | entry/range raw/thumb 0; no control-flow or fall-through |

## 7. Consumer evidence

### 7.1 State, globals, and arguments

| subject | evidence | semantic | confidence |
|---|---|---|---|
| 080a0b20 caller | ROM 080a18a8..080a18be; `080a18ba ff f7 31 f9` | row-type-15 dispatcher passes player_id/card_id and creates the real CALL entry | high |
| 080a0b20 state | ROM 080a0b34..080a0b46 and 080a130e..080a1318 | reads and advances EQUIP_PHASE_DISPLAY_STATE_OFF | high |
| 080a0b20 output | ROM 080a0b48..080a0b58 plus state-0 stores through LP_CARD_TRACK_BASE_OFF | shared display word or card-specific selector/count output | high |
| 080a0b20 text | BL targets at 080a10aa..080a130a | card-name/game-text formatting followed by display-op-31 calls | high |
| 080a131c | ROM 080a131c..080a132e | shared local epilogue restoring the 0x310-byte frame and saved registers | high |
| 1d88 | asm/13:7470,7611,7677,8016 | equip row active flag | high |
| 1d90 | asm/13:7538,7717 | 19-way row type | high |
| 1d8c/1d98/1d9a | asm/13:7692-7719 | player/row parameter/count fields | high |
| 1950 dataization | asm/13_equip_placement.s:7563 raw block; ROM 18fa instruction 0x4a15 resolves to literal 1950 | EQUIP_REROLL_SPRITE_PARAM_OFF scalar | high |
| 1bc0 arguments | ROM 1bc2..1bc6 and 1c00..1c0c | entry r1 becomes fallback callee r2; entry r2 is active-path delta and fallback callee r3; entry r3 is unread | high |
| 1f68 packed flags | ROM 1f78..1fa6 plus phase branches 2048..2088, 20ce..20e2, 217c..21fc | r2 independent masks 01/02/08/10/20/80 | high |
| 0201e274 | asm/13:8751,8783,8852 | direct phase-state global | high |
| 0201e28a | asm/13:8844,8884 | direct next-track halfword global | high |
| 12a1 | asm/13:8519 and following call | zone query tag | high |
| 1509/1546 | asm/13:9041-9060 plus card-stats lines above | two card CIDs | high |
| 080a24cd | asm/13:9040; body 24cc..24ee | Thumb predicate callback | high |
| 080a1e81 | R4 pools 20ec/2134 | extended eligibility Thumb callback | high |
| 1720 block | table 16d4..171c and join 190a | row-type switch code | high |
| 2018 block | table 2004..2014 and shared epilogue | phase switch code | high |

### 7.2 Direct B/BL target closure and the 080a38f8 boundary projection

The complete edge ledger is `output/refine-run-20260831-194634/F13-Seg-5-expanded-direct-edges.tsv` (SHA256 `88ac58dc4bc0815933535bbd8252a84d959acb9e4955bc05936ed4563dbf182a`). It decodes every direct B/BL in all 49 reopened ranges and all 31 retained Seg-5 ranges: 375 edges = 89 BL + 286 B, 226 unique targets. Source groups are 289 historical-closure edges and 86 original-Seg-5 edges.

The per-edge classification is exhaustive: REOPENED_R4_CODE=234, REOPENED_LOCAL_EPILOGUE=1, REOPENED_FUNCTION_ENTRY=1, SEG5_R4_CODE=35, SEG5_NEW_FUNCTION_ENTRY=1, EXISTING_FUNCTION=85, EXISTING_FUNCTION_BODY=17, and EXTERNAL_EXISTING_STUB=1. There are zero UNAPPROVED rows and zero targets in any pool or padding range. The ledger marks 236 edges to 152 targets inside the former `[080a0b20,080a1338)` Rule-3 row as `controlled_reopen`; after this proposal that entire row is R4 code/pool/padding, not active §5.1. The original two Seg-5 Rule-3 ranges receive no direct edge.

The scope-failure edge is an explicit ledger row: source 080a18ba, opcode BL, target 080a0b20, ROM bytes `ff f7 31 f9`, classification REOPENED_FUNCTION_ENTRY. It must survive as one operand-0 UNCONDITIONAL_CALL/DEFAULT/primary reference after apply and persisted reload.

The sole boundary case is `080a187a: bl 080a38f8`, ROM bytes `02 f0 3d f8`. The target is the already exported four-byte stub `01 20 70 47` (`movs r0,#1; bx lr`) immediately before the existing Function at 080a38fc. It lies in the next address-ordered Seg-6 tail and is neither a pool nor an active §5.1 range. This proposal does not disassemble, create a Function, assign semantics, rename, or comment at 080a38f8. Ghidra's automatic cross-reference projection emits exactly `SUB_080a38f8:` before the unchanged `.byte 0x01,0x20,0x70,0x47`; the production scope checker may whitelist only that one generated Symbol line and must require identical four bytes and listing type. Strict address order requires Seg-6 to close `[080a38f8,080a38fc)` before any later Seg-6 refinement; the activity/progress entry remains plan-only as `Seg-6 boundary stub R4 closure pending`. Any additional Seg-6 delta stops landing.

## 8. C1-C13 and executable landing guards

| check | result / guard |
|---|---|
| C1 | Original fixed range remains mapped as 38 Functions, 108 original slots and five blocks; the controlled historical expansion is exactly one 2072-byte former Rule-3 block plus caller 08094d30. |
| C2 | TSV covers all 108 originals, all 70 retained Seg-5 R4/dataization slots, and all 71 reopened pools. The four exact Function bodies include every approved code island and exclude all pools/padding. |
| C3 | The real 18ba CALL reopens 0b20..1338 under R4; referenced 1950 goes dataization; only the two zero-valid-ref Seg-5 ranges remain in §5.1. |
| C4 | TSV generated from ROM little-endian reads; all new slot values asserted. |
| C5 | Existing definitions are reused first; new definitions are 5 numeric offsets/codes, 2 globals, and 4 GAS aliases. |
| C6 | 249 slot labels are unique; 16d4 and 2004 each use one slot/table name, and 1720 is case_1_or_2. |
| C7 | Seven target LABEL contracts, 33 REF post-states, and 26 RENAME pre-states are explicit and independently guarded. |
| C8 | All ten complete PLATE rewrites use current names; no approved PLATE retains the five reviewed stale-name sets. |
| C9 | Exact PLATE/EOL payloads are ASCII; each PLATE is below 500 bytes; EOL count is 249 slot comments plus one 131c local-epilogue comment. |
| C10 | Callback pointers are odd; mov-pc switch tables intentionally store even addresses. |
| C11 | Existing 080a1658 Function is renamed to tick_equip_display_row_by_type; exactly three new Functions are created and the count is 5209 -> 5212. No SUB_080a0b20 or provisional 080a131c Function remains. |
| C12 | 0b20, 1bc0 and 1f68 arguments and the 1950 raw-block evidence are derived from ROM instructions; 131c is guarded as a local epilogue. |
| C13 | Exactly two zero-valid-ref Rule-3 ranges remain. The 375-edge ledger has no pool/padding/unapproved target; 38f8 is the one frozen next-segment Symbol projection. Full export/export_all/build and physical rollback gates are mandatory. |

Landing order:

1. Before any write, make a physical recursive copy of `ghidra/Yu-Gi-Oh WCT 2006.rep` named with timestamp and `pre-F13Seg5`. Enumerate all 15 database files in source and backup, record size and SHA256, and require a complete 15/15 match. A logical Ghidra state snapshot does not replace this physical backup.
2. Before modifying formal sources, record a source snapshot with file-existence, size and SHA256 for all `asm/*.s`, asm/rom.s, constants/duel_field.inc, constants/ewram.inc, tools/ghidra-labeling/RenameKnownFunctions.py, doc/dev/naming-proposals.csv, the four temp inventory outputs, the activity/progress documents, and the planned RefineF13Seg5 script path. Preserve unrelated user and earlier-segment changes; the snapshot is the rollback source and scope baseline.
3. Re-run ref-scan and require exactly: reopened entry 0b20 raw/thumb=0/0 plus real machine CALL 18ba->0b20; its nonzero candidate-start packed hits are only 0c0c=26/65, 0d18=0/1, 0f0c=2/3 and local epilogue 131c=4/1, all attributed to raw assets; 1720..190a raw/thumb=29/2 (19 true switch words, 10 raw coincidences including `1900 -> 09e13b4f` with bytes `00 19 0a 08`, and 2 thumb coincidences); 1950..1954=0/0 plus the ROM 18fa literal read; 1dd8..1de8=0/0; 1f54..2000=1/0 with only the 1fee raw-host coincidence and the real BL to 1f68; 2018..2234=6/6 with five true even switch words. Rebuild the 80-range direct-edge ledger and require 375 rows, 226 targets, explicit 18ba->0b20, zero UNAPPROVED and only the frozen 38f8 boundary projection. Any count or attribution difference stops landing before write.
4. Run the apply script in dry mode against a fresh state and require exact planned counts: 249 slots = 190 EQ + 33 REF + 26 RENAME; four R4 top-level regions / 80 code ranges; one dataization; three Function creates; one Function rename; ten PLATE comments; 250 EOL comments (249 slot + one 131c instruction); zero carve; zero FAIL. Dry mode also verifies the four exact Function-body plans, Function pre-count 5209, every ROM word, all 30 even switch entries, four odd callbacks, seven target Symbol/Data contracts, 33 REF tuples, 26 RENAME tuples, and ASCII/PLATE-length limits.
5. Only after dry success, begin one Ghidra transaction. Add seven constants/globals and four GAS aliases after duplicate/value checks; R4-disassemble only the section 3 code islands; type the listed pools as 4-byte scalars; dataize 1950..1954; normalize the switch Symbols; apply the 249 TSV rows in address order; normalize the 131c local epilogue Symbol/EOL; set exact Function bodies; create only Functions 0b20/1f68/24cc; rename only Function 1658; and write exactly ten PLATE plus 250 EOL comments. Do not mutate 38f8 or any other Seg-6 byte/listing/Symbol/comment.
6. Run all postchecks inside that transaction before commit. Any failed value, Symbol/ref source, Function identity/body/count, incoming-ref, Data type, comment, automatic-name, pool/padding, or scope guard ends the transaction with rollback. Commit the transaction only with zero FAIL, then save the program.
7. After save, start a fresh Ghidra headless process with `-noanalysis -readOnly`. Recheck Function count 5212 and all four exact bodies/entries/IDs, incoming refs, seven target primary LABEL names/addresses/sources and Data objects, all 33 REF and 26 RENAME tuples, pool/padding/Data types, ten exact PLATE and 250 exact EOL comments, ASCII/length limits, switch/callback values, the 131c local Symbol/non-Function state, and residual automatic labels/blocks. Require no `SUB_080a0b20`. Record the 15 database file hashes before and after this read-only process and require no change.
8. Run the full export range `080000c0..084c7637` to asm/all.s, remove only the known standalone mode directives, run inject_modes.py, and run split_all_s.py. Verify all 25 module boundaries and require that no instruction crosses an approved pool or padding range. Check production scope: only `[080a0b20,080a1338)`, the original Seg-5 projection, the single asm12 caller at 08094d30, and the exact generated `SUB_080a38f8:` Symbol line may differ. The 38f8 bytes must remain `.byte 0x01,0x20,0x70,0x47`; all other Seg-6 `[080a27a0,080a38fc)` text and every unapproved formal file remain byte-for-byte at the source snapshot.
9. Run `python tools/rom-export/export_all.py`, then `NOPAUSE=1 build.bat`. Require output/2343.gba size 33554432 bytes, byte-for-byte equality with roms/2343.gba, and SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`. Only after every preceding gate succeeds, withdraw the historical 0b20 Rule-3 row, retain/update the two Seg-5 §5.1 rows, update real inventory and the guarded 080a1658 naming row. Activity/total progress must say the historical closure and original Seg-5 remain `R4 closure pending` until the full persisted/export/build verification succeeds; record the 38f8 Seg-6 boundary stub as the immediate next address-ordered closure, not as completed.
10. On any failure after transaction commit or source editing, stop immediately, restore the physical `.rep` backup and every allowed source from the source snapshot, then recheck the 15 database hashes and formal-file scope. Do not continue to documentation completion after a failed gate.
11. No Seg-6 write or semantic analysis is authorized. The automatic `SUB_080a38f8:` export line is the sole read-only boundary projection and does not authorize disassembly, Function creation, naming, or comments there. Do not commit or stage any file in this landing; root performs the later repository-level decision after independent review.

## Executor Report: F13-Seg-5

- 槽: EQ=190 REF=33 RENAME=26 FUNC_RENAME=1 PLATE=10 EOL=250 (249 slot + one instruction); total=249 (original contract 178 retained + historical closure 71)
- Function create=3; carve=0; disasm=4 top-level regions / 80 code ranges; §5.1=2 ranges
- Historical closure: 49 code ranges / 822 instructions / 1754B code; 71 pools / 284B; 17 padding ranges / 34B; residual=0
- Combined R4: 80 code ranges / 1231 instructions / 2640B code; 141 R4/dataization slots including 71 historical-closure pools
- Direct edges: 375 rows / 226 targets / UNAPPROVED=0; explicit 18ba->0b20; frozen next-Seg-6 projection=38f8 only
- 新增 constants/全局: EQUIP_CARD_MESSAGE_FRAME_NEG, EQUIP_CARD_MESSAGE_FORMAT_ID_129, EQUIP_CARD_DISPLAY_SUB_ID_141, LP_EQUIP_ROW_ACTIVE_OFF, LP_EQUIP_ROW_TYPE_OFF, gEquipPhaseDisplayState, gLpCardTrackNext; GAS aliases=4
- 求助: none
- BLOCKED: none
- proposal: doc/dev/refine/F13-Seg-5.proposal.md
- slots: doc/dev/refine/F13-Seg-5.slots.tsv
- edges: output/refine-run-20260831-194634/F13-Seg-5-expanded-direct-edges.tsv
