# Naming Proposal: 0x080dbebc

## 提案
- **proposed_name**: fill_pack_palette_hue_gradient
- **confidence**: high

## plate comment (中文, ASCII 标点)
为拆包场景封面调色板生成色相渐变条带. 以 r0 指向的调色板缓冲区 (偏移 +0x12 起) 为写目标, 循环迭代 9..12 共 4 次, 每次用 bios_div 将索引映射到色相 H (0..0xb4 范围内均匀分布), 固定传入 S=0xff/V=0xff 给 convert_hsv_to_gba_rgb555 转换为 GBA RGB555 写入目标 halfword. 循环结束后写入哨兵值 0x7fff (白色). 然后根据 r1 (基础饱和度参数, 若 <= 0xb3 向前 bios_div, 否则从 0x168-r1 反向) 计算饱和度压缩因子, 调用 scale_pixel_saturation_in_buffer 对整段缓冲区做逐像素饱和度缩放. 被 tick_pack_name_scroll_strip_row0 (0x080d4fa4) 在封面 HSV 调色板路径中调用.

Constants:
- HUE_CYCLE = 0xb4 (180, 色相循环上限)
- HUE_STEPS = 4 (循环 9..12)
- HUE_STRIDE = 0xb4 (每步色相增量基数)
- S_FULL = 0xff (饱和度满值)
- V_FULL = 0xff (明度满值)
- SENTINEL_COLOR = 0x7fff (终止哨兵白色)
- SAT_HALF = 0x80 (饱和度压缩除数)
- REFLECT_THRESHOLD = 0xb3 (超出此值使用对称反射公式)

## 参数签名
- r0: u16* pal_buf (调色板目标缓冲区基址, 写入从 +0x12 偏移起的 4+1 个 halfword)
- r1: u16 hue_base (基础色相/饱和度输入, [0..0x168], 决定渐变起点和饱和度压缩比)
- 返回: void (pop {r0}; bx r0 Pattern B, 0x080dbf2c/0x080dbf2e)

## 副作用
- [r0+0x12..r0+0x1a]: 4 个 GBA RGB555 halfword 写入 (色相渐变)
- [r0+0x1a]: 0x7fff 哨兵 halfword (结束标记)
- [scale_pixel_saturation_in_buffer 内部缓冲区]: 逐像素饱和度修改

## 行级注释 (<=30 行精华)
- @ 0x080dbecc: movs r0,#0xb4; muls r0,r1 -> 当前迭代色相值 = (step-9)*0xb4
- @ 0x080dbed2: bios_div(hue_raw, 4) -> 均匀映射到 [0..0xb4/4] 色相区间
- @ 0x080dbedc: get_bios_div_remainder(hue_raw*2, 0x168) -> 取色相余数用于 H 参数
- @ 0x080dbee4: convert_hsv_to_gba_rgb555(H=r0, S=0xff, V=0xff) -> 纯色相色
- @ 0x080dbef2: 写入哨兵颜色 0x7fff 作为调色板终止标记
- @ 0x080dbef8: cmp r6,#0xb3 -> 判断是否进入反射路径 (r6 已保存 r1 入参 hue_base)
- @ 0x080dbf0c-0x080dbf14: 超出阈值时取 0x168-hue_base 做对称反射再除 0x80
- @ 0x080dbf1a-0x080dbf1e: lsls r2,r0,#0x10; orrs r2,#1 -> 打包 pixel_count=1 到 r2 高 16 位
- @ 0x080dbf24: scale_pixel_saturation_in_buffer 对 r4 指向缓冲区做整体饱和度缩放

## 调用图
CALLEE-COLUMN GREP: grepping callee=0x080dbebc
- caller: addr 0x080d4fa4 (tags: [pack,vram,pal]; role: tick_pack_name_scroll_strip_row0 封面 HSV 调色板刷新路径)
- callee: bios_div (0x0810e3fc), get_bios_div_remainder (0x0810e400), convert_hsv_to_gba_rgb555 (0x080dd980), scale_pixel_saturation_in_buffer (0x080ddb64)

## 置信度证据
- L1 (函数体 asm 374236-374291): 完整循环 bls+adds 结构, cmp #0xb3 反射, 逐步可跟踪
- L2 (IO 魔数): SENTINEL_COLOR=0x7fff 白色哨兵, HUE_CYCLE=0xb4=180 度色相环
- L6 (命名 callee): convert_hsv_to_gba_rgb555 / scale_pixel_saturation_in_buffer 已命名, 场景语义清晰
