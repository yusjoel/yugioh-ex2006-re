# Refine Review: 04-Seg-8b

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | Seg-8b 范围 0x4640c..0x47990 与 §五 路线图一致; 上一段 Seg-8a (0x44e30..0x4640c) 已完成; 下一段 Seg-9 (0x47990..0x47ec0) 未开始; 无跳号/回头 |
| C2 Rule2 | PASS | 段内 0 ROM_INCBIN / .byte 块 (grep 确认); 全为 THUMB 代码 + 函数内 literal pool; 无独立数据块需 carve |
| C3 Rule3 | PASS | §5.1 登记 = 0; 段内无任何 .byte/.incbin 块, ref-scan 不适用 |
| C4 R1 值 | PASS | 独立 python struct.unpack_from 核对全部 123 槽: 127 次地址读取全部与 proposal 值一致 (含 4 个 0x0000ffff sentinel: 0x46894/695c/6e70/6fcc; gEquipZoneCountTable 0x47878=0x0201e1c8; 复合 REF 0x478f0=0x0201d5b4; 所有 19 新 CID 槽逐一核对) |
| C5 R1 复用 | PASS | 23 新建常量 (19 card_info + 1 duel_field + 3 oam_attr) 逐一扫全 constants/*.inc: 无同值碰撞; 复用槽 (PANDEMONIUM_CID/SPHINX_TELEIA_CID/DARK_MAGICIAN_OF_CHAOS_CID/BANISHER_OF_THE_LIGHT_CID 等) 均已存在于 card_info.inc |
| C6 R2 名 | PASS | 全部 EQ/RENAME slot_label 符合 ^[a-z][a-z0-9_]+$; 多同值槽用 _b/_c/_d 后缀; PTR_gP1LifePoints_* 沿用已建立惯例 (同文件已有 22 个同前缀标签) |
| C7 R3 接通 | PASS | 6 REF 槽均有 USER-label (5x PTR_gP1LifePoints_XXXXXXXX + DAT_080478f0) + DATA-ref 计划 (.word gP1LifePoints / .word gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF); 复合 REF 算式核对: 0x0201c510+0x10a4=0x0201d5b4 正确 |
| C8 R5 现名 | PASS | 独立统计 Seg-8b 范围 FUN_ token: 15 个 (2+8+4+1=15 与 proposal 一致); 4 函数 plate 全部映射到已存在函数名 (update_equip_target_bitmap_for_field/build_equip_placement_valid_bitmap/handle_card_effect_zone_eligibility_by_field6/render_slot_card_sprite_with_chaos_equip_check 等均确认存在于 asm/04); FUN_08047114/FUN_080470a4 正确识别为内部 LAB_ (LAB_08047114:line15727, LAB_080470a4:line15670) |
| C9 ASCII | PASS | proposal 中 Ghidra 侧文本 (RENAME EOL 23 条 + plate 替换目标名) 逐一验证纯 ASCII; 无 CJK/全角字符 |
| C10 carve | N/A | 段内无 fn-ptr 表/carve; 无 .word fn+1 条目需核对 |
| C11 误名 | PASS | proposal 声明无 FUNC_RENAME 候选; 10 函数名称经审查与函数体操作语义一致 |
| C12 R6 | PASS | 所有关键槽均有 file:line 证据 + 置信度标注; 无零容忍词; 独立核对引用行: line 16629 (EQUIP_BITMAP_CTRL_OFF), line 14231 (HEAVY_MECH_SUPPORT_PLATFORM_CID), line 15053 (BIG_BANG_SHOT_CID), line 16241/16313 (OAM_EFFECT_ZONE_SPRITE_P1) 全部对应正确内容 |
| C13 残留 | PASS | 独立 grep: DAT_ 标签 118 个 + PTR_ 标签 5 个 = 123 总计; EQ=117 (118 DAT_ 减 1 复合 REF) + REF=6 = 123; diff=0; 无遗漏残留 |

## 独立核查摘要

**C4 ROM 字节核对 (自主重跑)**

executor 自纠的 5 个槽独立核对:
- 0x08046894: ROM=0x0000ffff (OAM_ATTR0_HIDDEN) - 正确
- 0x0804695c: ROM=0x0000ffff (OAM_ATTR0_HIDDEN) - 正确
- 0x08046e70: ROM=0x0000ffff (OAM_ATTR0_HIDDEN) - 正确
- 0x08046fcc: ROM=0x0000ffff (OAM_ATTR0_HIDDEN) - 正确
- 0x08047878: ROM=0x0201e1c8 (gEquipZoneCountTable) - 正确

注: 任务描述中出现的 "0x4685c" 地址并非 proposal 中的槽地址; 独立核对 0x0804685c=0x280004c0 (THUMB 指令字节, 不在 EQ_SLOTS 表内)。proposal EQ_SLOTS 表内容正确, 无该地址。

**C13 残留清点 (自主重跑)**

段内 .word 条目总数: 123 (与 proposal 一致)
- 0x0000ffff 出现: 4 次 (0x46894/695c/6e70/6fcc), 全部在 proposal 中

**C5 新建常量碰撞扫描 (自主重跑)**

23 个新建常量 (19 CID + 1 duel_field + 3 oam_attr) 全部无碰撞确认。

**C5b CID 坐实**

19 个新建 CID 全部在 data/card-stats.s 中确认 (card_NNNN 条目存在 + slot_id 值匹配)。
card_id 0x1258: slot=0x1258 在 card-stats.s 中确认为 gap (0x1256 存在, 0x1257 存在, 0x1258 不存在, 0x125a 不存在), 低置信 RENAME stub 处理合规。

**C8 FUN_ token 核对 (自主重跑)**

段内 FUN_ token 15 个 (grep 确认), 全部映射到已存在函数名:
- FUN_08047114/FUN_080470a4: 内部 LAB_ (LAB_08047114 at line 15727, LAB_080470a4 at line 15670), 替换为外层函数名合规
- 其余 11 个 FUN_ 全部对应已命名函数

**med-conf 槽注记**

- OAM_EFFECT_ZONE_SPRITE_P1=0x8031: med-conf 标注合规 (file:line 证据充分, 无零容忍词); P2 sibling 0x8032 在 ROM 确认有 42 个引用, 不影响本段
- 0x1258 gap: low-conf 标注合规 (card-stats.s 确认无该 slot_id)

## 状态: PASS

## 修改清单

无需修改。

---

> 核验时间: 2026-06-13
> 核验方法: python struct.unpack_from 独立读取全部关键槽 ROM 字节; grep asm/04_card_zone_sprite.s 计数 DAT_/PTR_/FUN_ 标签; grep data/card-stats.s 核对 19 CID; grep constants/*.inc 核对 23 新建常量无碰撞
