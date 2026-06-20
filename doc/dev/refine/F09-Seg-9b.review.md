# Refine Review: F09-Seg-9b [0x08077c50..0x0807850c)

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-9a commit done; Seg-9b status=⬜ 正确为下一段 |
| C2 Rule2 | 4 个 ROM_INCBIN 全有归宿 | OK | B6/B8=disasm(fn_eligible), B7/B9=disasm(sub-stubs), §5.1=0 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | §5.1=0; B6/B8 THUMB+1 验证见下节 |
| **C3 disasm完整** | **B9 覆盖 0 residue** | **FAIL** | **sub_8476 (0x08078476) 漏判: dispatch table entry[26] raw=1 @0x08078354; 6 字节 BL+b 无 DisassembleCommand** |
| C4 R1 值 | EQ slot 值 vs ROM 4 字节 | OK | 全部 33 个 EQ slot 采样验证; 28 个精确核对均 OK |
| C5 R1 复用 | 新建前 grep 0 命中 | OK | 0x1738: constants/ 无 CID 匹配 (rom_data.inc 0x09821738 = ROM 地址，不同域); 0x175c: constants/ 无任何匹配 |
| C6 R2 名 | 槽名格式合规, 无碰撞 | OK | 所有 pool_label 格式 ^[a-z][a-z0-9_]+$ |
| C7 R3 接通 | REF_SLOTS 有 USER-label+DATA-ref | OK | 3 个 REF_SLOT: PTR_DAT_08077f2c / DAT_08077f44 / DAT_08078368; gas_label 各异 |
| C8 R5 现名 | 无残留 stale FUN_ | OK | grep 段内 (lines 21225..22098) FUN_[0-9a-f]{8} = 0 命中 |
| C9 ASCII | plate/EOL 纯 ASCII | OK | grep -P '[^\x00-\x7F]' 段内 = 0; PLATE=0 (正确) |
| C10 carve | 指针表条目 +1 核对 | OK | B7/B9 为 raw dispatch table (.word fn_addr 非 THUMB+1); B6/B8 为 FS THUMB+1 fn_eligible; carve=0 正确 |
| C11 误名 | 无 FUNC_RENAME 信号 | OK | 10 fn 语义一致; 无函数体全局矛盾 |
| C12 R6 | 关键槽有 file:line + 置信度 | OK | 5 个关键槽 (ACTIVATION_STATE_B_OFF / SANCTUARY_CID_SHIFTED / BLUE_EYES_WHITE_DRAGON_CID / gDuelCardCtxBase / gEquipChainSlotRefs) 均 file:line + high |
| C13 残留 | 段内 auto-name 100% 覆盖 | OK | grep 实测 36 个 (DAT_/DWORD_/PTR_DAT_); 33 EQ + 3 REF = 36; 100% |

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C3/disasm-completeness — B9 漏 sub_8476; 错列 sub_841c

**问题描述**

reviewer 独立重跑 B9 dispatch table 枚举，31-entry 表 (0x080782ec..0x08078367) 有 **8 个唯一目标**：

| 目标 | 来源 | 状态 |
|------|------|------|
| 0x08078368 (entry[30]) | raw=1 @0x08078364 | 提案已列 |
| 0x080783a0 (entry[28]) | raw=1 @0x0807835c | 提案已列 |
| 0x080783a8 (entry[27]) | raw=1 @0x08078358 | 提案已列 |
| **0x08078476 (entry[26])** | **raw=1 @0x08078354** | **提案漏列** |
| 0x0807847c (entry[2]) | raw=1 @0x080782f4 | 提案已列 |
| 0x0807848c (entry[1]) | raw=1 @0x080782f0 | 提案已列 |
| 0x0807849e (entry[0]) | raw=1 @0x080782ec | 提案已列 |
| 0x080784a8 (entries[3..25,29]) | raw=24 | 提案已列 default |

**0x08078476** (B9+0x10e)：独立 ref-scan 确认 raw=1 @0x08078354 (dispatch table entry[26])；解码为 `BL 0x0804a870; b 0x080784a8` (6 字节，0x78476..0x7847b)。

**0x0807841c** (B9+0xb4)：提案列为 `sub_841c`，但独立验证：
- 0x0807841a: `0xf7bb`（THUMB2 BL 第一 HW）
- 0x0807841c: `0xf8cd`（THUMB2 BL 第二 HW）  
- 0x0807841c 是 BL 指令中间位——**不是有效 THUMB 入口**
- THUMB+1 ref @0x09f73fd6 (0x09f7xxxx 压缩区) = 提案自己已 REJECT
- raw refs = 0 (不在 dispatch table 中)
- 在 0x0807841c 执行 DisassembleCommand 会破坏已 disasm 的 sub_83a8 主体

**影响**：不修复则落地后 0x78476..0x7847b (6 字节) 残留 ROM_INCBIN，违反 Rule2 zero-residue。

**修复动作 (fixer 执行)**

在 B9 disasm 计划中：
1. **删除** `sub_841c` (0x0807841c) 的 DisassembleCommand 调用及对应 label
2. **新增** `sub_8476` (0x08078476) 的 DisassembleCommand：
   ```
   DisassembleCommand(0x08078476)   # BL 0x0804a870; b 0x080784a8 (6 bytes)
   ```
3. **在 B9 clearListing 范围内**新增 `sub_8476` label 在 Ghidra 脚本中

正确的 8 个 DisassembleCommand 目标（不含 default）：
```
0x08078368  # sub_8368
0x080783a0  # sub_83a0
0x080783a8  # sub_83a8
0x08078476  # sub_8476  <-- 新增; BL decrement_lp_bar_display_counter; b default
0x0807847c  # sub_847c
0x0807848c  # sub_848c
0x0807849e  # sub_849e
0x080784a8  # default_84a8
```

---

### #2 — C3/disasm-completeness — B7 pool 地址描述有笔误（非阻塞注释修正）

**问题描述**

提案 B7 disasm 计划写：
> "Also contains literal pool words at +0x50=0x08077f94 (0x080507ad, fn_ptr within range)"

但 0x08077f94 (B7+0x50) 的实际值为 LE32 = `0xe033` (halfword = 0xe033，是 `b` 分支指令，CODE)。
0x080507ad 实际在 **B7+0x88 = 0x08077fcc**（reviewer 实测确认）。

`force_dword(0x08077fcc)` 这一行 pool 操作是正确的（+0x88 地址有效），问题仅在描述文字把 +0x50 和 +0x88 混淆了。
proposal 脚本如果按描述在 0x77f94 执行 force_dword 会破坏代码——**但如果实际脚本按 0x77fcc 执行则无影响**。

**修复动作 (fixer 确认)**

确认 Ghidra 脚本中 `force_dword(0x08077f94)` **不存在**（不要对此地址调用 force_dword）；`force_dword(0x08077fcc)` 存在且正确。若脚本已按 0x77fcc 写则 pass；若按 0x77f94 写则必须改为 0x77fcc。

---

## 附：ref-scan 核验记录（reviewer 自主重跑）

### B6: 0x08077ecc/0x5c (fn_eligible_dangerous_machine_type6)

```
raw_refs(0x08077ecc) = 0
thumb_refs(0x08077ecc) = 1
  @0x09e448d0 -> ROM offset 0x01e448d0 -> value = 0x08077ecd (= 0x08077ecc | 1) CONFIRMED
```

FS 表结构 (0x09e448cc 起)：
```
0x09e448cc: 0x00001738  <-- CID (fn_eligible_addr - 4)
0x09e448d0: 0x08077ecd  <-- fn_eligible THUMB+1
```

CID 0x1738 vs card-stats.s L19606: `card_1507 @ Dangerous Machine TYPE-6 slot=0x1738 pw=76895648` -- MATCH

注：提案称 "entry @0x09e448c4; CID=0x1738"，实际 CID 在 fn_eligible_addr-4 = 0x09e448cc，entry_base+0 = 0x09e448c4 处值为 0x00000000。CID 值本身正确。

### B8: 0x080782c0/0x2c (fn_eligible_monster_gate)

```
raw_refs(0x080782c0) = 0
thumb_refs(0x080782c0) = 1
  @0x09e41f18 -> ROM offset 0x01e41f18 -> value = 0x080782c1 (= 0x080782c0 | 1) CONFIRMED
```

FS 表结构：
```
0x09e41f14: 0x0000175c  <-- CID (fn_eligible_addr - 4)
0x09e41f18: 0x080782c1  <-- fn_eligible THUMB+1
```

CID 0x175c vs card-stats.s L20074: `card_1543 @ Monster Gate slot=0x175C pw=43040603` -- MATCH

### B7: 0x08077f44/0xc0 (dangerous_machine sub-stubs)

6-entry raw dispatch table at 0x08077f2c..0x08077f43：

| entry | addr | value | in_B7 | raw |
|-------|------|-------|-------|-----|
| [0] | 0x08077f2c | 0x08077f44 | YES | 1 |
| [1] | 0x08077f30 | 0x08077f56 | YES | 1 |
| [2] | 0x08077f34 | 0x08077f6c | YES | 1 |
| [3] | 0x08077f38 | 0x08077f7a | YES | 1 |
| [4] | 0x08077f3c | 0x08077f86 | YES | 1 |
| [5] | 0x08077f40 | 0x08077f9c | YES | 1 |

All 6 entries match proposal. All in B7 range (0x77f44..0x78003). CONFIRMED.

### B9: 0x08078368/0x14c (monster_gate sub-stubs)

31-entry raw dispatch table at 0x080782ec..0x08078367：

| unique entry | source entries | raw | proposal status |
|-------------|----------------|-----|-----------------|
| 0x08078368 | entry[30] | 1 | listed |
| 0x080783a0 | entry[28] | 1 | listed |
| 0x080783a8 | entry[27] | 1 | listed |
| **0x08078476** | **entry[26]** | **1** | **MISSING** |
| 0x0807847c | entry[2] | 1 | listed |
| 0x0807848c | entry[1] | 1 | listed |
| 0x0807849e | entry[0] | 1 | listed |
| 0x080784a8 | entries[3-25,29] | 24 | listed (default) |

0x08078476 decoded: `BL 0x0804a870 (decrement_lp_bar_display_counter?); b 0x080784a8` (6 bytes).
Branch at 0x7847a (e015): target = 0x0807847a + 4 + 21*2 = **0x080784a8** (default) CONFIRMED.

0x0807841c: mid-BL at (0x0807841a: f7bb | 0x0807841c: f8cd). raw=0, thumb=1 @0x09f73fd6 (compressed region, REJECT). NOT a valid dispatch entry.

## Reviewer Verdict: F09-Seg-9b = NEEDS_FIX(2 items)
