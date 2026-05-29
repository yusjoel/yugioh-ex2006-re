# Naming Proposal: 0x080eecfc

## 提案
- **proposed_name**: get_game_text_ptr_by_str_type_c
- **confidence**: high

## plate comment (中文, ASCII 标点)
游戏字符串指针获取函数, string family C 变体. r0=string_id. 若 r0==0 返回空字符串地址 0x09e4f348. 否则: r0 += 0x226 (DWORD_080eed30), 调用 game_str_id_to_row 转换为行索引; 以行索引和 [0x02006c2c] bits[2:0] (语言码) 计算 game_str_pointer_table 中的指针偏移; 返回 game_str_ja + offset. 与 get_game_text_ptr_by_str_type_b (0x080eed50, 偏移 0x212) 和 get_game_text_ptr_by_lang_offset (0x080eeca8, 偏移 0x1f4) 构成字符串查询三兄弟簇, 区别仅在 ID_OFFSET 常量不同 (本函数 0x226).

Constants:
- ID_OFFSET_C = 0x226 (DWORD_080eed30)
- game_str_pointer_table, game_str_ja: 已命名 ROM 标签
- gSettings_LANG = [0x02006c2c] bits[2:0]
- NULL_STR = 0x09e4f348 (DWORD_080eed4c)

## 参数签名
- r0: u16 string_id - 字符串 ID [0..1650] (0 返回空串; game_str_id_remap_count=0x0673=1651 entries, row [0..1650])
- 返回: r0 = char* 指向对应语言游戏字符串的 ROM 指针

## 副作用
- 无外部写

## 行级注释 (<=30 行精华)
- @ 0x080eecfc: cmp r0,0; beq -> 返回 NULL_STR
- @ 0x080eed02: ldr r1=0x226; adds r0,r0,r1 => ID+0x226
- @ 0x080eed06: bl game_str_id_to_row => 行索引
- @ 0x080eed0a: ldr r2=game_str_pointer_table; 计算 row*6*2+lang*4 偏移
- @ 0x080eed16: ldrb lang=[0x02006c2c]; lsls/lsrs 取低 3 位; 累加到偏移
- @ 0x080eed28: ldr r0=[table+offset]; adds r0,r0,game_str_ja => 返回字符串指针

## 调用图
- caller: indeg=0
  - grep ".word 0x080eecfd" asm/all.s: 0 hits (Sub-type A)
- callee: game_str_id_to_row (0x080f4e18)

## 置信度证据
- L3 共享 label 锚: 与已命名 get_game_text_ptr_by_str_type_b (0x080eed50) 和 get_game_text_ptr_by_lang_offset (0x080eeca8) 完全结构同源; asm line 405938 plate comment 直接描述 "string-family B/C sibling with FUN_080eeda4 (offset 0x23a)"
- L2 数据 label: game_str_pointer_table / game_str_ja 已命名; ID_OFFSET_C=0x226 静态可读
- L1 短函数体全静态: asm lines 405893-405936 (~44 行)
