# Naming Proposal: 0x080bacfc

## 提案
- **proposed_name**: invoke_count_occupied_monster_zones
- **confidence**: high

## plate comment (中文, ASCII 标点)
包装 count_occupied_monster_zones, 从 zone_ptr->byte[2] bit0 提取 player_id 后直接调用之. 入口读 r0->byte[2], 通过 lsls/lsrs #0x1f 提取 bit0 = player_id, 传入 count_occupied_monster_zones; 固定返回 r0=0 (不使用 count 结果). 通过 pop{r1}+bx r1 退出 (Sub-case E, r0=0). 用于需要 zone_ptr 作为入口参数但只需调用 count_occupied_monster_zones 副作用的调用场景.

Constants:
- 无非平凡字面量

## 参数签名
- r0: ptr zone_ptr (field zone 指针, byte[2] bit0 = player_id)
- 返回: r0 = u32 0 (fixed, 调用后固定 movs r0,#0)

## 副作用
- 调用 count_occupied_monster_zones(player_id) -> 结果未被使用

## 行级注释 (<=30 行精华)
- @ 080bacfe: ldrb r0,[r0,#2] -> 读取 zone byte[2]
- @ 080bad00: lsls r0,r0,#0x1f -> 提取 bit0
- @ 080bad02: lsrs r0,r0,#0x1f -> player_id = bit0
- @ 080bad04: bl count_occupied_monster_zones(player_id)
- @ 080bad08: movs r0,#0 -> 固定返回 0
- @ 080bad0a: pop{r1}+bx r1 -> Sub-case E

## 调用图
- caller: indeg=0; grep ".word 0x080bacfd" asm/all.s -> 0 hits; Sub-type A: no static reference, dead-code path
- callee: count_occupied_monster_zones (0x08033188)

## 置信度证据
- L1: 函数体 5 条有效指令 (asm lines 302536-302543), 全静态可读
- L2: 调用已命名 count_occupied_monster_zones, 返回语义直接明确
- L6: count_occupied_monster_zones (0x08033188) 已在 naming-proposals.csv 命名
