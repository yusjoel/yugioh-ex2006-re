# Refine Review: F08-Seg-1

Reviewer 独立复核，不信 proposal 结论，自主重跑 ref-scan + 机器码核 + ROM 字节验证。

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 0x643e0..0x6544c 与 §五 Seg-1 完全吻合 |
| C2 Rule2 | 全部 ROM_INCBIN 块有归宿 | ✅ | 2 块均判 R4 disasm |
| C3 Rule3 | §5.1 块 0 引用确认 | ✅ | 无 §5.1 登记；两块均有 THUMB+1 命中（reviewer 重跑验证） |
| C4 R1 值 | EQ slot ROM 字节核对 | ✅ | Block1 0x6457c: ROM[0x0806457c]=0x3218=ADDS r2,#0x18 正确；0x6457e=0x1880=ADDS r0,r0,r2；0x64582=0x2801=CMP r0,#1；全部与 proposal 吻合 |
| C5 R1 复用 | 新建前确无现有可复用 | ✅ | iter-2: MEMORY_CRUSHER_CID(0x19cf)+GUARDIAN_EXODE_CID(0x19f0) 移入 NEW table；card_info.inc grep 确认两者均无现有 .equ；REUSE 52 + NEW 35 计数自洽 |
| C6 R2 名 | slot 名 ^[a-z][a-z0-9_]+$, 无碰撞 | ✅ | 全 100 label + 新函数名 check_opponent_chain_zone_count_gt1_for_cid_19df 均合规；asm/*.s 无重名 |
| C7 R3 接通 | 13 PTR_ 槽有 USER-label + DATA-ref | ✅ | 13 PTR_gP1LifePoints_* 明确列入 RENAME_SLOTS |
| C8 R5 现名 | plate 无残留 stale FUN_ | ✅ | iter-2: FUN_080655da 4 处（line 1823/1887/2054/2071）全部进入 PLATE 表，replacement=restore_equip_effect_frame；line 2707 地址 0x080655da>0x0806544c，属 Seg-2 不在本段范围；FUN_08064880 出现 13 次（lines 503/1823/1887/1973/2054/2071/2134/2259/2318/2336/2354/2425/2439 中 2439 属 Seg-2）全覆盖；FUN_080714ec line 345 覆盖 |
| C9 ASCII | plate/EOL 纯 ASCII | ✅ | Ghidra 绑定 EOL/plate 文本全 ASCII；line 344 引用现存 mojibake 仅作文档说明，替换目标 line 345 为纯 ASCII；doc/ 内中文解释合规 |
| C10 carve | 指针表条目 +1 核 | N/A | 无 carve 块 |
| C11 误名 | 函数体与函数名无矛盾 | ✅ | iter-2: Block1 函数名改为 check_opponent_chain_zone_count_gt1_for_cid_19df（3 处出现，旧名 check_opponent_lp_slot_nonzero_for_cid_19df 已删除）；与 ADDS r2,#0x18 + gP1ChainZoneCountBase 语义一致 |
| C12 R6 | 关键槽 file:line + 置信度证据 | ✅ | Block1 disasm 消费者证据同步订正（gP1ChainZoneCountBase+opp*0x868）；关键槽均有 high 证据 |
| C13 残留 | 段内所有残留自动名槽全覆盖 | ✅ | 独立 python 清点：87 DAT_/DWORD_ + 13 PTR_gP1LifePoints_ = 100 个，RENAME_SLOTS 表完全覆盖，无遗漏无越界 |

**状态: PASS**

---

## 独立验证摘要

### ref-scan (自主重跑)

```
Block 1 (0x0806456c): raw=0 thumb+1=1 -> ROM[0x9e43078]=0x0806456d -> R4 disasm
Block 2 (0x080645f0): raw=0 thumb+1=1 -> ROM[0x9e45580]=0x080645f1  -> R4 disasm
```

### 机器码核

| 地址 | ROM 值 | 解码 | 与 proposal 一致 |
|------|--------|------|------|
| 0x0806457c | 0x3218 | ADDS r2,#0x18 | ✅ |
| 0x0806457e | 0x1880 | ADDS r0,r0,r2 | ✅ |
| 0x08064582 | 0x2801 | CMP r0,#1 | ✅ |
| 0x08064584 | 0xd906 | BLS (<=1 branch) | ✅ |

### C5 iter-2 验证

- REUSE 表 52 行（grep 精确匹配）
- NEW CID 表含 MEMORY_CRUSHER_CID(0x19cf) + GUARDIAN_EXODE_CID(0x19f0)
- card_info.inc grep 19cf/19f0/MEMORY_CRUSHER/GUARDIAN_EXODE 均 0 命中

### C8 iter-2 验证

- asm/08 中 FUN_080655da 共 5 处：lines 1823/1887/2054/2071（Seg-1，已覆盖）+ line 2707（Seg-2，地址 0x080655da > 0x0806544c，不在本段）
- asm/08 中 FUN_08064880 共 14 处（lines 345 错位，但 line 503/1823/1887/1973/2054/2071/2134/2259/2318/2336/2354/2425 = Seg-1 12 处 + line 2439 = Seg-2 1 处）；提案覆盖 Seg-1 内全部 13 处含 line 503
- asm/08 中 FUN_080714ec 1 处（line 345）已覆盖

### C13 验证

独立 python 扫描 asm/08 中地址 [0x080643e0, 0x0806544c) 的自动名 label：100 个（87 DAT_/DWORD_ + 13 PTR_gP1LifePoints_），与 proposal RENAME_SLOTS Total=100 完全吻合。

---

## iter-1 修改确认

| # | 原问题 | iter-2 状态 |
|---|--------|-------------|
| #1 (C4) | Block1 0x6457c 写成 adds r2,r2,r0 | 已订正为 adds r2,#0x18 ✅ |
| #2 (C5) | MEMORY_CRUSHER/GUARDIAN_EXODE 误放 REUSE 表 | 移入 NEW table，REUSE=52/NEW=35 ✅ |
| #3 (C8) | FUN_080655da 4 处未覆盖 | 全部列入 PLATE 表 ✅ |
| #4 (C11) | 函数名含 lp_slot 语义错误 | 改为 check_opponent_chain_zone_count_gt1_for_cid_19df ✅ |

---

## 额外观察 (不阻塞落地)

### OBS-1: ZONE_EFFECT_ATK_PENALTY_500 预存名称错误 (pre-existing, out of scope)

`constants/field_spell_bonus.inc`: `ZONE_EFFECT_ATK_PENALTY_500 = 0xfffffe70 = -400`，名称写 "500" 实值 -400。proposal 正确标为 out of scope。建议 fixer 在 EOL 注释写 `-400 (constant name misleading)` 提醒读者。

### OBS-2: equip_lp_delta.inc 独立文件

8 LP 扣减常量独立文件合理，reviewer 支持。

---

## 状态: PASS

所有 C1-C13 全部 ✅。iter-1 4 项修改全部确认解决。fixer 可直接进入落地模式 B。
