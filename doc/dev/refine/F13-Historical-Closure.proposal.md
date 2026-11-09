# Refine Proposal: F13-Historical-Closure  [0x0809d718..0x080a78dc)

## 范围与证据

- 模块范围: `asm/13_equip_placement.s`, `[0x0809d718,0x080a78dc)`, 41412 bytes. 本提案只做 C13 模块收尾, 不进入 file 14.
- 完整 Function 清单: `output/refine-run-20261028-105948/root-f13-closure-functions-input.json`, 214 rows, SHA256 `4d2cf7f0c35d71a4e7656805dbc7ff96007f26a849003f1bd0866aeb5b5c19fa`.
- 完整只读 DB 前态: `root-f13-closure-independent-prestate.json`, 214 Functions, 1530 words, 3410 module symbols, 1627 comments, 41412 byte states, SHA256 `cbc04bac7658908aff98af6cc0481be01daadd0486ad009707e5204175320d50`.
- 只读 DB 门禁: `root-f13-closure-independent-prestate.json.db-gate.json`, 15/15 physical files unchanged, SHA256 `b11c27b46014c3dd120611bd63cce211bd0d3a32b02dc09bf86e9396205ecd8e`.
- 独立整模块覆盖门禁: `root-f13-closure-module-layout-baseline.json`, SHA256 `cd84a7529073d28307664ecc920ea0fbb1bcde9da5fb8354029fdf4f661dfbbc`.
- 源码基线: `root-source-baseline-f13closure.json`, SHA256 `5b11abcb2dd23a95a1768c8c120ecb6b9053a13e1a741f93ea661cb3ae473334`; 15 个 DB 物理备份 manifest SHA256 `00bf9674f188c66bda31e37ef8a8c44e40273deb01150d9f0913580f20e5350a`.
- executor 源码审计: `f13-closure-source-audit.json`, SHA256 `d51c1e60ec81c26dfe75084eded5b26ede2a52e1022b35d3f8c62af6cbb0ceda`; 布局汇总: `f13-closure-layout.json`.
- 全 ROM raw/THUMB 扫描: `f13-closure-refscan.tsv`, 18 个偶地址候选, SHA256 `e92622211dec988f9c0eb8e224901798f9b2134f5fdaf6f3da3655e1d4e8ec0e`.
- 唯一写入合同: `doc/dev/refine/F13-Historical-Closure.plates.tsv`, 1 row. 本闭包没有 slot action, 因此不创建空 `slots.tsv`.

## 模块测绘

### Function 与字节布局

- 214 个 Function 入口全部与当前 inventory 和源码地址标注一致, 无重复入口.
- Ghidra 当前 18635 个 code units 完整覆盖 41412 bytes: 16365 个 InstructionDB / 34552 bytes, 2270 个 DataDB / 6860 bytes, 无空洞和重叠.
- InstructionDB = 15718 条普通助记符 + 647 条 `.hword`; 长度分布为 15454 x 2-byte 与 911 x 4-byte.
- DataDB = 1530 x 4-byte words + 740 x 1-byte units. 740 bytes 由 352 个 2-byte `.zero` 的 704 bytes 和两块登记 raw 的 36 bytes 精确组成.
- 1530 个 source words 地址唯一且逐项等于 ROM little-endian word. Ghidra类型分布: `/dword` 479, `/pointer` 179, `/undefined *` 95, `/undefined4` 777.

### 残留自动名与注释审计

- module symbols 共 3410. `DAT_`, `DWORD_`, `PTR_DAT_`, `UNK_`, `FUN_`, `SUB_` 自动名前缀命中 0.
- module comments 共 1627 = 214 PLATE + 1413 EOL; 其他 comment type 为 0, 非 ASCII 为 0.
- 精确旧自动名 token 只命中 `0x080a38fc` PLATE 内的 `DAT_0x12d`. 当前 PLATE 为 ASCII 1458 chars, SHA256 `42ea00f354a03aa7c3b6de64a37393d23c5c4b0a27eb3729e7d2df85a2a161ad`.
- 源码第 2 行中文是 `split_manifest.tsv` 生成的模块 header, 不是 Ghidra comment, 不纳入 PLATE/EOL 写入范围.

### 剩余 raw 块

| block | source | size | bytes SHA256 |
|---|---|---:|---|
| `[0x080a1dd8,0x080a1de8)` | `asm/13_equip_placement.s:9682`, `.byte` | 16 | `ecb74f8ca78e7d15e028d75264bef15594c44fb24f75a2aff7ba6db7d4015637` |
| `[0x080a1f54,0x080a1f68)` | `asm/13_equip_placement.s:9895`, `ROM_INCBIN` | 20 | `ec105d014111e6faceee9eaeba7ad2b1f3c98bc223872df8382c59d55312bf2d` |

## 数据块分类 (Rule 2/3)

| block | full-ROM ref-scan | current ASM / Ghidra incoming | internal shape | 判定 |
|---|---|---|---|---|
| `[0x080a1dd8,0x080a1de8)` | 8 个偶地址候选各 raw=0, THUMB=0; asset coincidence=0 | 所有候选 `references_to=[]`, 无 owner/symbol/comment; 前驱 `0x080a1dd6 bx r0`, 无 fallthrough; 全模块 direct/PC-literal/switch 文本引用=0 | 7 instructions / 8 encoded halfwords: `push; movs r1,13; movs r2,0; movs r3,0; bl set_lp_display_row_fields; pop; bx`. `0x080a1de0 -> 0x080a1a00`; `r0` passthrough, `r1=13`, `r2=0`, `r3=0`. 静态解码有 outgoing call, 但入口和任一内部候选均无 incoming | Section 5.1 保留 |
| `[0x080a1f54,0x080a1f68)` | 10 个偶地址候选各 raw=0, THUMB=0; asset coincidence=0 | 所有候选 `references_to=[]`, 无 owner/symbol/comment; 前驱 `0x080a1f52 bx r1`, 无 fallthrough; 全模块外部 direct/PC-literal/switch 引用=0 | 代码头读取内部 literals: `0x080a1f54 -> 0x080a1f60` (`gP1LifePoints`) 与 `0x080a1f56 -> 0x080a1f64` (`LP_CARD_TRACK_NEXT_OFF`), 然后 `ldrh; bx lr`; 这两条是 dead component 自包含边, 不是外部 live 入口 | Section 5.1 保留 |

两块每个半字候选的 raw/THUMB 原始命中数和 offset 均在 `f13-closure-refscan.tsv`. Seg-10 R4 新布局没有指向这 36 bytes 的 direct branch, call, PC literal, switch 或 fallthrough. 本闭包不重开 R4 或 carve.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

none. 1530 个既有 word 全部保留值, Data type, Symbol, reference, equate 与 EOL 前态.

### REF_SLOTS

none.

### RENAME_SLOTS

none.

### FUNC_RENAME

none. `tick_equip_score_display_phase` 与真实三步显示回调行为一致, Function 名称保持.

### PLATE (R5)

完整合同见 `F13-Historical-Closure.plates.tsv`.

| entry | action | old | new |
|---|---|---|---|
| `0x080a38fc` | full rewrite | ASCII 1458 chars, 含错误参数、状态和 `DAT_0x12d` | ASCII 490 chars, SHA256 `a30952b1a94a5e28be7fc202eae44bf8709bbc31acf3dd538ab7f0ecb5357985` |

拟写 PLATE 全文:

> Three-step card-specific display callback, called by tick_equip_display_row_by_type row type 19. Inputs: r0=player_id, r1=card_id, r2=display_value. Step 0 sets gEquipPhaseDisplayState to 1. Step 1 handles Bark of Dark Ruler (LP-cost texts 301/303), Reasoning (level texts 280/304 or random level 4..7), and Wall of Revealing Light (LP-cost texts 301/302 and a bounded thousands score), then advances. Later steps copy the score to LP card tracking. Returns 0 while active, 1 when complete.

Function 前态保持合同:

- Function ID 3436, USER_DEFINED Function, Global namespace ID 0, symbol_count 1.
- body size 316, SHA256 `022a58f575b307702c527609011c7aa42d0c101b3eecbfbe31315fe983b2f639`.
- half-open body ranges: `[080a38fc,080a392a)`, `[080a3938,080a3950)`, `[080a3954,080a395c)`, `[080a3960,080a3978)`, `[080a397c,080a3988)`, `[080a3990,080a39b0)`, `[080a39b4,080a3a20)`, `[080a3a30,080a3a6e)`.
- calling convention `unknown`, signature source DEFAULT, prototype `undefined tick_equip_score_display_phase()`, no custom storage/varargs/inline/no-return/external/thunk, stack purge `2147483647`, return `/undefined <UNASSIGNED>`, params `[]`, EOL `[]`.
- 唯一 incoming ref 保持: `0x080a1906 -> 0x080a38fc`, operand 0, `UNCONDITIONAL_CALL`, DEFAULT, primary, target Function ID 3436.

Registry / CSV / inventory 合同:

- `RenameKnownFunctions.py` 当前没有 `0x080a38fc` tuple. 新增 `("FUN_080a38fc", "tick_equip_score_display_phase", <new_plate>)` 到 file 13 Historical-Closure reviewed registry; 其他 tuple 不变.
- `doc/dev/naming-proposals.csv:3257` 已是 `0x080a38fc,tick_equip_score_display_phase,...`; 名称不变, CSV 不编辑.
- 四份 Function inventory 重新导出后, 本 Function 的 entry/name/body/signature 元数据保持; 本次只允许 PLATE 正文变化.

## carve 计划 (R7)

none.

## disasm 计划 (R4)

none.

## 新增 constants / 全局

none. 本闭包复用 `BARK_OF_DARK_RULER_CID`, `REASONING_CID`, `WALL_OF_REVEALING_LIGHT_CID` 及现有 equip/display constants.

## Section 5.1 登记 (Rule 3)

| block | bytes | 登记结论 |
|---|---:|---|
| `[0x080a1dd8,0x080a1de8)` | 16 | 全候选 raw/THUMB=0, 无 incoming/ref/owner/fallthrough, 保持 `.byte` 与原始字节 |
| `[0x080a1f54,0x080a1f68)` | 20 | 全候选 raw/THUMB=0, 两条内部 literal edge 不构成外部入口, 保持 `ROM_INCBIN` 与原始字节 |

## 消费者证据 (R6)

- `asm/13_equip_placement.s:8923-8933`, high: row type 19 读取 player ID, card ID 和 display value 到 r0/r1/r2, 在 `0x080a1906` 调用本 Function.
- `asm/13_equip_placement.s:13570-13576`, high: r3 在 `0x080a3904` 由 r2 覆盖, r8 在 `0x080a3908` 设为 `gP1LifePoints`; 旧 PLATE 的 r3/r8 输入描述错误.
- `asm/13_equip_placement.s:13597-13600`, high: step 0 写 `gEquipPhaseDisplayState=1` 并返回 0, 不是清零.
- `asm/13_equip_placement.s:13602-13644`, high: `REASONING_CID-0xdc = 0x14be` 是 Bark of Dark Ruler; active path 保存 r2 display value, fallback 使用 301/303 与 `r2=1`.
- `asm/13_equip_placement.s:13645-13671`, high: Reasoning active path写随机 level 4..7, fallback 使用 280/304/1/12.
- `asm/13_equip_placement.s:13672-13742`, high: Wall of Revealing Light active path计算有界 thousands score, fallback 使用 301/302/1/LP-thousands.
- `asm/13_equip_placement.s:13581-13589`, high: later step 将 score 复制到 LP card tracking 后返回 1.
- `constants/card_info.inc:1019`, `:1193`, `:2086` 与 `doc/um06-deck-modification-tool/data.md:994`, `:1166`, `:1530`, high: 三个 CID 分别对应 Bark of Dark Ruler, Reasoning, Wall of Revealing Light.
- `text/game-strings/en.txt:853-854`, `:916-926`, high: text 280/301/302/303/304 分别为 level prompt, LP-cost prompt, `%d000LP`, `%d00LP`, `Level %d`.

## Module-close 落地与门禁

1. 仅按 plates TSV 在 `0x080a38fc` 写一个 ASCII PLATE 全文, 长度 490; 保持 Function 名称/ID/body/signature/incoming 和全部 EOL.
2. 新增缺失 registry tuple; CSV name row 与全部已存在 registry tuples 保持.
3. 重导 asm, split file 13. 允许的源码差异只有 `0x080a38fc` 前 PLATE 投影; `.word`, `.hword`, opcode, padding 和两块 raw directives/bytes 保持.
4. 复核整模块后态仍为 214 Functions, 16365 InstructionDB, 1530 words, 352 个 2-byte padding, 两块登记 raw 共 36 bytes, 全范围 41412 bytes 无空洞/重叠.
5. build 与 byte-identical、DB 备份/回滚和最终 C13 scope gate 由 fixer/reviewer 阶段执行; executor 不执行 build 或写 DB.

## 求助

none.

## Executor Report: F13-Historical-Closure

- 槽: EQ=0 REF=0 RENAME=0 FUNC_RENAME=0 PLATE=1
- carve=0 disasm=0 range Section 5.1=2 blocks / 36 bytes
- 新增 constants/全局: none
- 求助: none
- proposal: `doc/dev/refine/F13-Historical-Closure.proposal.md`
