# 计划：通过 ROM 侧函数断点定位卡图压缩数据

## 目标

在游戏加载卡牌大图时，捕获传入解压函数的 ROM 源地址（即卡图压缩块在 ROM 中的位置）。

## 已完成的静态分析

### 关键函数：FUN_08014fa8（all.s line 3526）

```
参数：
  r0 = 卡牌信息指针（某结构体）
  r1 = 解压目标地址（保存到 r8）

内部逻辑：
  1. 从 ROM 数据结构 DAT_08015084 (0x09e61178) 加载各偏移表
  2. 用卡牌 ID 索引卡图指针表，计算 r4 = 压缩数据 ROM 地址
  3. 判断目标地址 r8：
     - r8 > 0x05ffffff（VRAM）→ 走 0x08015076，SWI 0x12 直写 VRAM
     - r8 ≤ 0x05ffffff（RAM）→ 走 0x080150be，SWI 0x11 写入 EWRAM 0x0200af20
```

### 断点位置：`0x08015076`

```asm
08015072  adds r0,r4,#0x0   ; r0 = r4 = 压缩数据 ROM 地址
08015074  mov  r1,r8         ; r1 = r8 = VRAM 目标地址（0x06000000）
08015076  bl FUN_0810e418    ; <== 断点在此，调用 SWI 0x12 LZ77UnCompWram
```

触发时：`r0` = 卡图压缩块 ROM 地址（GBA 地址格式 0x09xxxxxxx）

### 相关数据结构

| 符号 | ROM GBA 地址 | 内容 |
|------|-------------|------|
| DAT_08015084 | 0x08015084 | 指向 0x09e61178（卡图数据结构根指针） |
| DAT_0801509c | 0x0801509c | EWRAM 缓冲区地址 0x0200af20 |
| DAT_080150a0 | 0x080150a0 | 阈值 0x05ffffff（区分 VRAM/RAM 路径） |

## 执行步骤

1. 重启 mGBA（黑屏等待 GDB）
2. 运行：`tools/arm-none-eabi-gdb.exe --batch -x output/gdb_break_cardimage.gdb`
3. GDB 输出 `RUNNING` 后，在 mGBA 中按 A 打开卡牌详情页
4. 记录触发时的 r0 值（卡图压缩块 ROM 地址）
5. 验证：读取该地址前 4 字节，应为 LZ77 压缩头（byte[0]=0x10, bytes[1-3]=解压大小）

## GDB 脚本

`output/gdb_break_cardimage.gdb`

## 预期结果

r0 = 卡图压缩块 GBA 地址，例如 `0x09xxxxxx`  
r1 = `0x06000000`（BG2 VRAM，确认是卡图）

后续：根据 r0 计算 ROM 文件偏移（= r0 - 0x08000000），读取压缩头验证，
再枚举所有卡牌 ID → 对应 ROM 偏移的映射关系。
