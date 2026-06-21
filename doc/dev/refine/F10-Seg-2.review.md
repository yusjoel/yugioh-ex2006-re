# Refine Review: F10-Seg-2

> Segment [0x0807ae84, 0x0807be2c), file `asm/10_equip_effect_dispatch.s`
> Reviewer: independent (not executor). All ref-scans and byte reads re-run from scratch.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ PASS | Seg-2 [0x0807ae84, 0x0807be2c) 与 §五 roadmap 完全一致；Seg-1 已落地 (aa53bf0)，本段是下一段 |
| C2 Rule2 | ✅ PASS | 8 个 ROM_INCBIN 块全部有明确 R4 disasm 归宿；无静默保留 |
| C3 Rule3 | N/A | 无 §5.1 块；独立 ref-scan 确认所有 8 块均有引用（THUMB+1 或 raw）|
| C4 R1 值 | ❌ FAIL | BLK3 createDWord(0x0807b4f4) 目标地址存放的是 0x4687 (MOV PC,r0 THUMB 指令)，而非 data；这是 Seg-1 BLK5 trap 的重演 |
| C5 R1 复用 | ✅ PASS | 16 个不同值全部在 constants/*.inc 中按值 grep 命中；0 个新建 .equ 确认无误 |
| C6 R2 名 | ✅ PASS | 55 个提议标签全部满足 `^[a-z][a-z0-9_]+$`；无重名碰撞 |
| C7 R3 接通 | ✅ PASS | 6 个 REF 槽均给出 `.word <fn>+1`；目标函数地址已确认 (push 0xb570 开头) |
| C8 R5 现名 | ✅ PASS | Seg-2 范围内 0 处 FUN_ 残留；Seg-2 上下文行内 0 处 FUN_ |
| C9 ASCII | ✅ PASS | PLATE=1 (fn_eligible_hero_kid_hyena) 纯 ASCII；无 CJK 字符加入 |
| C10 carve | ✅ PASS | 6 个 REF 槽值均为奇数 (THUMB+1)；`.word <fn>+1` 语法正确 |
| C11 误名 | ✅ PASS | FUNC_RENAME 唯一项：旧名仅出现 1 次（定义处），indeg=0，去后缀安全 |
| C12 R6 | ✅ PASS | 7 个关键槽均提供 file:line 证据 + conf: high；无零容忍词 |
| C13 残留 | ✅ PASS | 独立清点：19 DAT_ + 28 DWORD_ + 4 PTR_ = 51；EQ(31)+REF(6)+RENAME(14)=51；并集 == 全集 |

---

## 状态: NEEDS_FIX (1 critical + 5 annotation)

---

## 修改清单

### #1 — C4 (pool-address-correctness) — BLK3 createDWord(0x0807b4f4) 目标是代码地址 [CRITICAL, 必修]

**问题**: 提案 BLK3 节写道 `createDWord: 0x0807b4f4 (padding .hword 0x0000)`。

独立字节核对：

```
0x0807b4f4: halfword = 0x4687  →  THUMB: MOV PC, r0 (间接跳转，与 BLK1 @ 0x0807af96 同一指令)
0x0807b4f6: halfword = 0x0000  →  对齐填充
0x0807b4f8: word    = 0x0201b290  →  gDuelPhaseFlags (正确的 literal pool 起点)
0x0807b4fc: word    = 0x0807b500  →  dispatch table ptr (正确的 literal pool)
```

提案自身已注明 "Seg-1 BLK5 trap (0x4687 = MOV PC,r0 mistaken for data) does NOT apply here"，但 BLK3 恰好犯了同样的错误：将 0x4687 代码地址列入 createDWord。

**必须修改**：

- **删除** `createDWord(0x0807b4f4)` 调用
- 保留 `createDWord(0x0807b4f8)` 和 `createDWord(0x0807b4fc)` （正确）
- 0x0807b4f4 (0x4687) 是 THUMB 指令，由 DisassembleCommand 正常消化；0x0807b4f6 (0x0000) 是对齐 pad，随后自动出现在 pool 前

---

### #2 — BLK2 ref 计数注解错误 [annotation-only]

**问题**: 提案 ROM_INCBIN 表行写 `raw=1 (base) + 6 sub-entries`，但独立 ref-scan 结果为 **6 个 raw refs 共计**（dispatch table 0x0807afa0..0x0807afb4 正好 6 个条目，每条指向 BLK2 内不同地址）。

表格 table[0..5] 的 6 个唯一目标 = 6 个 sub-stubs（含 default 共 6 个，不是 7 个）。

sub-stub **名字列表**已列 6 个，属正确。错误仅在行头的 "7 sub-stubs" 和 "raw=1 base + 6 sub-entries" 计数。

**修改**: 将 BLK2 行改为 `raw refs=6 (6-entry table); 6 unique sub-stubs`；删除 "7 sub-stubs" 说法。

---

### #3 — BLK6 0x0807b8e0 ref 计数注解错误 [annotation-only]

**问题**: 提案写 `rescue_cat_dispatch_8e0 (+0x068, 2 refs): 2 table entries`。

独立 ref-scan：在整个 ROM 中，0x0807b8e0 的 raw refs = 1（仅 table[25] at 0x0807b868）。

BLK6 dispatch table 完整转储确认：0x0807b8e0 仅出现 1 次（index 25）。

**修改**: 将 rescue_cat_dispatch_8e0 的 ref 数改为 `(1 ref, table[25])`。

---

### #4 — BLK4 table 索引注解错误 [annotation-only]

**问题**: 提案写 `hero_kid_hyena_dispatch_6a2 (+0x12e, 1 ref from table[21])`，但独立核实：0x0807b6a2 实际在 table[0]（0x0807b500 处）。

table[21] 的值是 0x0807b6ac（default stub），不是 0x0807b6a2。

所有 7 个唯一入口地址均正确，只是 table 索引注解有误。

**修改**: 将 `hero_kid_hyena_dispatch_6a2` 的 table 索引从 [21] 改为 [0]。

---

### #5 — BLK5 "raw=1" 注解错误 [annotation-only]

**问题**: 提案写 `Note: 0x0807b800 has raw=1 (table pointer stored in fn_eligible literal pool) -> createDWord at 0x0807b800`。

独立 ref-scan：0x0807b800 在整个 ROM 中的 raw refs = 0。地址 0x0807b800 存放的值是 0x0807b804（dispatch table 起点），createDWord 调用本身是正确的（防止 Ghidra 误解析为代码），但 "raw=1" 说法不正确。

**修改**: 将 BLK5 注解改为 "Note: literal pool at 0x0807b800 (.word dispatch_table_ptr=0x0807b804); createDWord mandatory to prevent code re-analysis"（删除 "raw=1" 说法）。

---

### #6 — FS table 地址空间标注错误 [annotation-only]

**问题**: 提案对各 fn_eligible 的 THUMB+1 引用位置标注为 "EWRAM 0x01e4xxxx"（如 "EWRAM 0x01e46fe8"），实际地址为 ROM FS 数据区 0x09e46fe8（0x09 前缀 = ROM 镜像/FS 区域，非 EWRAM 0x02xxxxxx）。

CID 数值全部正确（按 fn_ptr_addr-0x4 偏移读取），无需改正功能性内容。

附：提案正文提到 "CID at 0x01e46fe4=0x1847"，CID 实际位于 fn_eligible_ptr_addr-0x4（即 0x09e46fe4），确认值 0x1847 正确。4 个 CID 均已独立核实：Lighten the Load=0x1847 ✓, Hero Kid=0x19a7 ✓, Hyena=0x1867 ✓, Rescue Cat=0x1876 ✓, Gatling Dragon=0x1878 ✓。

**修改**: 将所有 "EWRAM 0x01e4xxxx" 改为 "ROM FS 0x09e4xxxx"（纯文档订正，不影响落地脚本）。

---

## 独立 ref-scan 总结

| BLK | 范围 | raw refs | THUMB+1 refs | 结论 |
|-----|------|----------|--------------|------|
| 1 | 0x0807af66..0x0807afa0 | 1 (= THUMB+1 同地址) | 1 (0x9e46fe8 -> 0x0807af69) | R4 disasm fn_eligible |
| 2 | 0x0807afb8..0x0807b0c8 | 6 (table[0..5] at 0x0807afa0..0x0807afb4) | 0 | R4 disasm 6 sub-stubs |
| 3 | 0x0807b4d4..0x0807b500 | 2 (= THUMB+1 同地址) | 2 (0x9e45428, 0x9e46028 -> 0x0807b4d5) | R4 disasm fn_eligible |
| 4 | 0x0807b574..0x0807b6b8 | 29 (table 29-entry) | 0 | R4 disasm 7 sub-stubs |
| 5 | 0x0807b7dc..0x0807b804 | 1 (= THUMB+1) | 1 (0x9e470f0 -> 0x0807b7dd) | R4 disasm fn_eligible |
| 6 | 0x0807b878..0x0807b958 | 29 (table 29-entry) | 0 | R4 disasm 7 sub-stubs |
| 7 | 0x0807b9f4..0x0807ba1c | 1 (= THUMB+1) | 1 (0x9e47108 -> 0x0807b9f5) | R4 disasm fn_eligible |
| 8 | 0x0807ba30..0x0807bb30 | 5 (table 5-entry) | 0 | R4 disasm 5 sub-stubs |

全部 8 块有引用，无 §5.1 块。

## fn_eligible 入口地址核实

| BLK | 入口地址 | THUMB+1 ref 值 | 验证 |
|-----|---------|----------------|------|
| 1 | 0x0807af68 | 0x0807af69 (奇数 OK) | first hword=0xb5f0 (push{r4-r7,lr}) |
| 3 | 0x0807b4d4 | 0x0807b4d5 (奇数 OK) | first hword=0xb570 (push{r4-r6,lr}) |
| 5 | 0x0807b7dc | 0x0807b7dd (奇数 OK) | first hword=0xb530 (push{r4,r5,lr}) |
| 7 | 0x0807b9f4 | 0x0807b9f5 (奇数 OK) | first hword=0xb530 (push{r4,r5,lr}) |

---

## Reviewer Verdict: F10-Seg-2 = NEEDS_FIX(1 items)
