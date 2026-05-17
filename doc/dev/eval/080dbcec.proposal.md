# Naming Proposal: 0x080dbcec

## 提案
- **proposed_name**: zero_fill_pack_obj_vram_region_alt
- **confidence**: high

## plate comment (中文, ASCII 标点)
与 zero_fill_pack_obj_vram_region (0x080dbbb0) 功能完全相同: 调用 zero_fill_halfword_wrapper(r0, 0xc00) 清零 OBJ VRAM 中 6 KB 区域. 区别在于调用方不同 -- 来自 FUN_080d4de4 (卡包横幅初始化函数), 传入的目标地址是卡包横幅 OBJ VRAM 区域 (由 FUN_080d4de4 计算得到的 0x06000000+偏移).

Constants:
- ZERO_COUNT=0xc00 // 0xc0<<4: 清零 halfword 数量 (= 6 KB)

## 参数签名
- r0: u16* vram_dst -- OBJ VRAM 目标起始地址 (由 caller FUN_080d4de4 计算设置)
- 返回: r0 = void; `pop{r0}; bx r0` 退出

## 副作用
- OBJ VRAM [r0..r0+0x17ff] := 0 (zero_fill 0xc00 halfwords)

## 行级注释 (<=30 行精华)
- @ 080dbcee: movs r1,0xc0; lsls r1,r1,4 -> r1=0xc00
- @ 080dbcf2: bl zero_fill_halfword_wrapper(r0, 0xc00) -- 清零 6 KB
- @ 080dbcf6: pop{r0}; bx r0 -> void 返回

## 调用图
- callee: zero_fill_halfword_wrapper
- caller:
  - addr 0x080d4e08 (tags: [card_image]; role: FUN_080d4de4 卡包横幅初始化时清空 OBJ VRAM 横幅区域)

## 置信度证据
- L1 全静态 3 条指令叶子函数 (行 358931-358937), 与 0x080dbbb0 逐字节相同
- L2 常量: 0xc0<<4=0xc00; zero_fill_halfword_wrapper 已命名
- L6 sibling: zero_fill_pack_obj_vram_region (0x080dbbb0) 完全对称; 使用 _alt qualifier 区分调用者
