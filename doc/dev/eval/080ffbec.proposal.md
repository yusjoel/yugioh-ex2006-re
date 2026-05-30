# Naming Proposal: 0x080ffbec

## 提案
- **proposed_name**: update_card_list_scroll_position
- **confidence**: high

## plate comment (中文, ASCII 标点)
卡片列表滚动位置更新函数. 首先调用 compute_card_list_scroll_position; 若返回负值则立即返回 0 (无法滚动). 读取 display_mode 字段 [+0x44] (0..3 -> r7). 检查 [0x0202f3c0+2] (link_battle 标志): link 模式下比较滚动增量与阈值 0x100; 非 link 模式按 mode(0/1/2/3) 使用不同阈值 (0x50/0xf/0x1e). 满足阈值条件后调用 count_valid_cards_by_slot_type (slot types 1/2/3), update_deck_slot_card_entry, __modsi3 (取模运算). 正常完成返回 1. indeg=0, fn-ptr 表入口.

Constants:
CARD_LIST_CTX=0x0202a4d0 (card_list EWRAM 上下文基址)
CANDIDATE_BUF=0x0202f3c0 (card_list 候选缓冲区基址)
LINK_FLAG_OFF=0x2 (link_battle 标志字节偏移)
DISPLAY_MODE_OFF=0x44 (display_mode 字段偏移, [0..3])
LINK_SCROLL_THRESHOLD=0x100 (link 模式滚动阈值)
MODE1_THRESHOLD=0x50 (非 link mode 0 滚动阈值)
MODE2_THRESHOLD=0xf (非 link mode 1 滚动阈值)
MODE3_THRESHOLD=0x1e (非 link mode 2 滚动阈值)

## 参数签名
- r0: (unused)
- 返回: r0 = s32 (0=无法滚动/早退, 1=正常完成; Sub-case E pop{r4,r5,r6,r7}; pop{r1}; bx r1; movs r0,#0 早退路径, movs r0,#1 正常路径)

## 副作用
- 通过 update_deck_slot_card_entry 写入 EWRAM 卡片列表状态

## 行级注释 (<=30 行精华)
- @ 080ffbee: compute_card_list_scroll_position - 计算滚动位置
- @ 080ffbf4: blt 返回 0 - 负值 = 无法滚动
- @ 080ffbfc: [+0x44] bits[1:0] -> display_mode (0..3)
- @ 080ffc02: [0x0202f3c0+2] - link_battle 标志检查
- @ 080ffc10: link 模式: 阈值 0x100
- @ 080ffc20: 非 link 模式: 按 mode 选阈值 0x50/0xf/0x1e
- @ 080ffc50: count_valid_cards_by_slot_type + update_deck_slot_card_entry + __modsi3
- @ 080ffc60: movs r0,#1 正常返回

## 调用图
CALLEE-COLUMN GREP: grepping callee=0x080ffbec
- caller: indeg=0; grep ".word 0x080ffbed" asm/all.s -> 0 hits (Sub-type A)
- callee: compute_card_list_scroll_position, count_valid_cards_by_slot_type, update_deck_slot_card_entry, __modsi3

## 置信度证据
- L1 (asm body 445354-445470): 完整双路分支 + 4 callee, 返回值语义清晰
- L2 (CANDIDATE_BUF=0x0202f3c0 + LINK_FLAG_OFF=0x2): card_list 专用 EWRAM 地址 + link flag 偏移
- L6 (命名 callee): compute_card_list_scroll_position, count_valid_cards_by_slot_type, update_deck_slot_card_entry 均为已命名函数
