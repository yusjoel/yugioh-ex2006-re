# Refine Review: F08-Seg-4

段范围: ROM `0x08067160..0x08067fa4`, 21 函数入口, 74 DAT_/DWORD_ + 7 PTR_ = 81 槽

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与路线图一致 | ✅ | Seg-4 接 Seg-3 end 0x67160, 无跳号/回头 |
| C2 | ROM_INCBIN/.byte 块 0 个 | ✅ | grep 段内 ROM_INCBIN = 0 命中; 提案称 0 正确 |
| C3 | §5.1 块确 0 引用 | ✅ N/A | 本段无 ROM_INCBIN 块; fn-ptr cb 0x080671bc raw=0 / THUMB+1=1 (见 C7) |
| C4 | EQ value == ROM 4 字节 | ✅ | 22 个关键槽独立 python 核对全部匹配 (见下表) |
| C5 | 新建前确无可复用 | ✅* | NEW 2 CID 均 0 命中; 0x5db/0x5dc 域裁定成立 (见 C5 详析) |
| C6 | 槽名格式/无碰撞 | ✅** | 函数名 21/21 合规; 槽名 23 处含混合大小写 (gDuelPhaseFlags_* 等) — 与 Seg-2 已提交标签 stub80_gDuelCardCtxBase 等一致; 无碰撞; 1 处轻微拼写 (见备注) |
| C7 | carve/全局槽接通 | ✅ | DAT_08067270=0x080671bd; bit0=1 THUMB; check_activation_ctx_zone11_match_cb+1 正确 |
| C8 | plate 引用全用现名 | ✅ | grep 段内 FUN_[0-9a-f]{8} = 0 命中 |
| C9 | plate/EOL 纯 ASCII | ✅ | 新 plate 文本独立 ord() 验证 0 非 ASCII 字符 |
| C10 | 指针表 +1 THUMB 核对 | ✅ N/A | 段内仅 1 个 fn-ptr 槽 (DAT_08067270); 已在 C7 覆盖 |
| C11 | 函数名与函数体一致 | ✅ | FUNC_RENAME=0; 抽查 tick_equip_head_slot_sprite_state_machine / check_activation_ctx_zone11_match_cb / dispatch_effect_zone_lp_sprites_by_slot_flags 均与函数体一致 |
| C12 | 关键槽语义有证据 | ✅ | 0x5db/0x5dc / SOUL_ABSORBING_BONE_TOWER_CID / MALICE_ASCENDANT_CID 均给出 file:line + conf:high; 无零容忍词 |
| C13 | 段内残留 100% 覆盖 | ❌ | DWORD_08067c40 在 EQ 表列出但 RENAME 表遗漏 (见 #1 修改清单) |

## C4 关键 ROM 值核对 (抽样 22 槽)

| 地址 | 提案值 | ROM 实读 | 匹配 |
|------|--------|----------|------|
| 0x08067188 | 0x00000bb8 | 0x00000bb8 | ✅ |
| 0x080671b4 | 0x00000bb8 | 0x00000bb8 | ✅ |
| 0x080671b8 | 0x00001388 | 0x00001388 | ✅ |
| 0x080671dc | 0x0201b290 | 0x0201b290 | ✅ |
| 0x080671e0 | 0x00000484 | 0x00000484 | ✅ |
| 0x08067224 | 0x0201e2a0 | 0x0201e2a0 | ✅ |
| 0x08067228 | 0x0201b290 | 0x0201b290 | ✅ |
| 0x08067250 | 0x00000868 | 0x00000868 | ✅ |
| 0x08067270 | 0x080671bd | 0x080671bd | ✅ |
| 0x08067298 | 0x00001d70 | 0x00001d70 | ✅ |
| 0x080673fc | 0x00001744 | 0x00001744 | ✅ |
| 0x0806740c | 0x000019d0 | 0x000019d0 | ✅ |
| 0x080674b0 | 0x00000868 | 0x00000868 | ✅ |
| 0x080674b4 | 0x0201c510 | 0x0201c510 | ✅ |
| 0x08067cc0 | 0x000005db | 0x000005db | ✅ |
| 0x08067ce4 | 0x000005dc | 0x000005dc | ✅ |
| 0x08067ca8 | 0x0000123b | 0x0000123b | ✅ |
| 0x08067cac | 0x0000188c | 0x0000188c | ✅ |
| 0x08067de4 | 0x0201c4e0 | 0x0201c4e0 | ✅ |
| 0x08067e98 | 0x0201c4e0 | 0x0201c4e0 | ✅ |
| 0x08067bf8 | 0x0201c740 | 0x0201c740 | ✅ |
| 0x08067a90 | 0x000004a4 | 0x000004a4 | ✅ |

## C5 详析

**NEW CID 核对 (必须 0 命中)**:
- SOUL_ABSORBING_BONE_TOWER_CID=0x1744: grep constants/*.inc "0x1744" = 0 命中 ✅; card-stats.s line 19762 "slot=0x1744 pw=63012333" 坐实
- MALICE_ASCENDANT_CID=0x19d0: grep constants/*.inc "0x19d0" = 0 命中 ✅; card-stats.s line 26678 "slot=0x19D0 pw=14255590" 坐实

**域裁定 0x5db/0x5dc 独立核验**:
- 0x5db 现有命中: card_info.inc:981 FIELD5_SCORE_THRESHOLD_1499 (field5 资格 score gate)
- 0x5dc 现有命中: card_info.inc:84 CARD_STAT_LP_THRESHOLD_1500 (LP 渲染阈值); duel_field.inc:201 LP_COST_1500 (LP 费用)
- 消费者机器码独立验证 (asm/08 line 8467-8495):
  - 0x08067cba: 0xdd0a = ble (condition 0xdd) -> Crush Card path: field3>0x5db -> target (ATK>=1500 怪兽)
  - 0x08067cce: 0xdc00 = bgt (condition 0xdc) -> DDV path: field3<=0x5dc -> target (ATK<=1500 怪兽)
  - 消费函数 `get_card_extended_stat_field3` / `get_card_extended_stat_field3_raw` 明确为怪兽 ATK 域
- 语义对比: ATK AI 选标 vs LP 显示阈值 vs field5 资格分 = 三个截然不同的域
- 先例: 0x5dc 已有 2 个独立常量 (项目已接受同值多域)
- 裁定: CARD_FIELD3_THRESHOLD_1499/1500 新建 **成立** ✅

**Reuse 常量验证**: 21 个 reuse 常量全部存在且值匹配 ✅

## C7 ref-scan 详情

check_activation_ctx_zone11_match_cb @ 0x080671bc:
- raw (0x080671bc): 0 occurrences
- THUMB+1 (0x080671bd): 1 occurrence (= DAT_08067270 slot)
- 提案称 "1 raw ROM ref" 但实际是 1 THUMB+1 ref — 表述有误 (raw 应为 0, THUMB+1 应为 1)
- 功能结论正确: 仅通过 fn-ptr 被引用; .word check_activation_ctx_zone11_match_cb+1 表达式正确 ✅

## C6 备注

1. **混合大小写标签** (技术违规但项目已有先例): 提案中 23 个标签含 gDuelPhaseFlags_* / gDuelFieldSlots_* / gP1LifePoints_* / gP1SlotSetCodeArray_* 格式, 这些以 'g' 开头后接大写字母 (gD/gP), 严格来说不符合 ^[a-z][a-z0-9_]+$ 规则。但 Seg-2 已提交代码 (commit 4b6b4a4) 中已存在 stub80_gDuelCardCtxBase / stub7e_gDuelFieldSlots 等相同模式的标签 — 项目已接受此惯例。**不作为阻塞项。**
2. **轻微拼写**: `gDuelCardCtxBase_dispatch_act_80067224` — 后缀 `80067224` 应为 `08067224` (槽地址 0x08067224, 前导 0 被省略). 纯拼写错误, GAS 汇编无功能影响, 且标签唯一. **不作为阻塞项。**

## 状态: NEEDS_FIX

## 修改清单

### #1 — C13 — 添加 DWORD_08067c40 的 RENAME 条目

**问题**: DWORD_08067c40 (值=0x0201b290=gDuelPhaseFlags) 在 EQ 表的 gDuelPhaseFlags 全局地址列表中已列出 (proposal 第 56 行), 但 RENAME_SLOTS 表中缺少对应条目。提案执行后 ASM 中该槽标签仍为 `DWORD_08067c40`, 违反 C13 (残留自动名槽 100% 覆盖)。

**修改**: 在 proposal 的 RENAME_SLOTS 表中追加:

```
| DWORD_08067c40 | gDuelPhaseFlags_tick_head_07c40 | gDuelPhaseFlags |
```

**位置**: tick_equip_head_slot_sprite_state_machine @ asm/08 line 8394:
```
ldr r2, DWORD_08067c40   @ 08067c22  ; gDuelPhaseFlags base, computes +0x4a0 state field
```

**影响**: Ghidra rename script 需补 1 条 renameLabel(0x08067c40, "gDuelPhaseFlags_tick_head_07c40"); 其余 80 槽不变。

---

*Reviewer note*: C7 表述修正 (不影响执行): 提案 REF_SLOTS 证据描述 "1 raw ROM ref" 应为 "1 THUMB+1 ROM ref (0x080671bd)" — raw=0, THUMB+1=1. 功能结论和 GAS 表达式均正确, 无需回滚, 可在 fixer 执行时顺带订正证据文字。
