# 静态分析：卡图 ROM 数据定位（早期失败路径）

**日期**: 2026-04-13  
**分析对象**: `asm/all.s`（Ghidra 导出的反汇编，16MB，覆盖 0x08000000–0x08ffffff）  
**目标**: 找到游戏加载卡牌大图时调用解压函数的位置，从而在断点触发时读取 ROM 源地址

> ⚠️ **主体结论已证伪**：`FUN_08014fa8` 走 BIOS SWI 0x11/0x12 路径，**不是**卡图加载路径。
> 真实卡图加载走 `FUN_0801d290`，用自写 6bpp 解码（非 BIOS SWI）。最终结论见
> [`p1-phase-b2-findings.md`](p1-phase-b2-findings.md)。
>
> 本文保留作为**负面结果归档**（记录"为什么不是这条路"）+ 附录的 **THUMB 高寄存器 MOV 解码速查表**（通用参考价值）。

---

## 一、分析思路

已知卡牌详情页的卡图通过 BIOS SWI 解压写入 VRAM BG2（0x06000000），但：
- GDB watchpoint 在 VRAM/EWRAM 地址不可用（mGBA stub 限制）
- 无法从 BIOS 向量拦截

因此改为**从 ROM 侧静态分析**：在 all.s 中找到调用 SWI 的位置，对该调用指令设 hbreak，触发时读 r0（压缩数据 ROM 地址）。

---

## 二、定位 SWI 包装函数

### 搜索 `svc` 指令

BIOS SWI 在 Ghidra 反汇编中以 `svc` 表示（ARMv7 起 SWI 改名为 SVC，编码完全相同；Ghidra 统一使用新助记符）。

> **注意**：搜索 `swi` 会得到 0 条结果。正确关键词是 `svc`。

```
grep "svc" asm/all.s
```

结果中与解压相关的：

```
svc 0x12    @ 0810e418   FUN_0810e418  (LZ77UnCompWram)
svc 0x11    @ 0810e41c   FUN_0810e41c  (LZ77UnCompVram)
```

两个函数均为极简包装：

```asm
FUN_0810e418:
    svc 0x12        @ 0810e418
    bx lr           @ 0810e41a

FUN_0810e41c:
    svc 0x11        @ 0810e41c
    bx lr           @ 0810e41e
```

### 统计调用次数

```
grep "bl FUN_0810e41c"  →  1 处 (@ 0x080150be)
grep "bl FUN_0810e418"  →  11 处
```

`FUN_0810e41c`（SWI 0x11）**只有 1 个调用点**，极大缩小了分析范围。

---

## 三、分析唯一调用方 FUN_08014fa8

调用 `FUN_0810e41c` 的上层函数入口：`FUN_08014fa8 @ 0x08014fa8`

### 3.1 函数入口 —— 保存高位寄存器

Ghidra 将某些高寄存器 MOV 编码为 `.hword`，需手动解码：

| 地址 | 编码 | 解码（THUMB 高寄存器 MOV） | 含义 |
|------|------|--------------------------|------|
| 0x08014faa | `0x4657` | MOV r7, r10 | 保存 r10 |
| 0x08014fac | `0x464e` | MOV r6, r9  | 保存 r9  |
| 0x08014fae | `0x4645` | MOV r5, r8  | 保存 r8  |
| 0x08014fb4 | `0x4688` | MOV r8, r1  | **r8 = 第2参数（目标地址）** |
| 0x08014fb8 | `0x466b` | MOV r3, sp  | r3 = 栈指针 |

> **THUMB 高寄存器 MOV 解码方法**：
> 格式 `0100 0110 D Rm Rdn`（16位），D=bit7，Rm=bits[6:3]，Rdn=bits[2:0]；目标寄存器 = D*8 + Rdn

**结论**：函数第2参数 r1（目标地址）在入口处保存到 r8。

### 3.2 加载数据结构根指针

```asm
ldr r7, DAT_08015084    @ r7 = 0x09e61178  (卡图数据结构根指针)
```

`DAT_08015084` 是字面量池，值为 `0x09e61178`（ROM 扩展区，超过 16MB 边界）。

从 r7（0x09e61178）读取偏移表并存入栈：

| 栈偏移 | 来源 | 内容 |
|--------|------|------|
| sp+0x58 | r7[0x4] + r7 | 相对指针→绝对 ROM 地址 |
| sp+0x5c | r7[0x8] + r7 | **卡图指针表基址** |
| sp+0x60 | r7[0xc] + r7 | 另一偏移表基址 |
| sp+0x64 | r7[0x10] + r7 | 卡图数据区基址 |

### 3.3 用卡牌 ID 索引卡图指针表

```asm
lsls r1, r4, #0x2      @ r1 = r4 * 4（卡牌 ID × 4 字节 = 表项字节偏移）
ldr  r3, [sp, #0x5c]   @ r3 = 卡图指针表基址
adds r2, r1, r3        @ r2 = 表基址 + 偏移
ldr  r2, [r2, #0x0]    @ r2 = 指针表[卡牌 ID]（相对偏移值）
ldr  r5, [sp, #0x64]   @ r5 = 卡图数据区基址
adds r4, r5, r2        @ r4 = 基址 + 相对偏移 = 卡图压缩数据 ROM 地址
```

**此时 r4 = 当前卡牌的压缩图像在 ROM 中的绝对 GBA 地址。**

### 3.4 目标地址分支

```asm
ldr  r5, DAT_0801509c      @ r5 = 0x0200af20（EWRAM 缓冲区地址）
ldr  r0, DAT_080150a0      @ r0 = 0x05ffffff（阈值）
cmp  r8, r0                @ 比较目标地址与阈值
bls  LAB_080150a4          @ 若 r8 ≤ 0x05ffffff（RAM），跳到 EWRAM 路径
```

#### 路径 A：目标为 VRAM（r8 > 0x05ffffff，即 0x06000000+）

```asm
@ 0x08015072
adds r0, r4, #0x0   @ r0 = r4 = 压缩数据 ROM 地址
mov  r1, r8         @ r1 = r8 = VRAM 目标地址（0x06000000）
bl   FUN_0810e418   @ 0x08015076  <== 断点位置，SWI 0x12 LZ77UnCompWram
b    LAB_080150f8
```

#### 路径 B：目标为 RAM（r8 ≤ 0x05ffffff）

```asm
@ LAB_080150a4
ldr  r0, [r4, #0x0]     @ 读取压缩头
lsls r0, r0, #0x18
lsrs r0, r0, #0x1c      @ 提取压缩类型（bits 7-4）
cmp  r0, #0x1           @ type == 1 → LZ77
beq  LAB_080150ba

@ LAB_080150ba
adds r0, r4, #0x0       @ r0 = 源地址
adds r1, r5, #0x0       @ r1 = 0x0200af20（EWRAM 目标）
bl   FUN_0810e41c        @ 0x080150be  SWI 0x11 LZ77UnCompVram
```

---

## 四、结论

### 卡图加载路径（静态分析推测，已被实验否定）

```
FUN_08014fa8(r0=卡牌信息, r1=0x06000000)
    ↓
r4 = 通过卡牌 ID 查表得到的压缩数据 ROM 地址
    ↓
r8 (= r1 = 0x06000000) > 0x05ffffff → 走 VRAM 路径
    ↓
bl FUN_0810e418 @ 0x08015076
    ↓
SWI 0x12 LZ77UnCompWram(r0=ROM源, r1=0x06000000)
    → 直接解压到 VRAM BG2
```

### ⚠️ 实验验证结果：断点全部未触发

对以下地址依次设 `hbreak`，按 A 打开卡牌详情页，均**未触发**：

| 断点地址 | 说明 | 结果 |
|----------|------|------|
| `0x08015076` | VRAM 路径 BL 指令 | ❌ 未触发 |
| `0x08014fa8` | `FUN_08014fa8` 函数入口 | ❌ 未触发 |
| `0x0810e418` | SWI 0x12 包装函数本体 | ❌ 未触发 |
| `0x0810e41c` | SWI 0x11 包装函数本体 | ❌ 未触发 |

### 可能原因

1. **软件解压**：游戏使用自写 LZ77 解压，不调用 BIOS SWI（最可能）
2. **预加载机制**：卡图在进入列表页时已解压完毕，按 A 只是切换显示
3. **Ghidra 分析偏差**：`FUN_08014fa8` 可能不是卡图路径，只是形态相似的函数
4. **ROM 扩展区盲区**：all.s 覆盖 0x08000000–0x08ffffff，卡图加载代码可能在 0x09xxxxxx 区段（all.s 未反汇编）

### 下一步建议

- **方向 A**：验证"预加载"假设——在卡牌列表页（按 A **之前**）就设断点，观察 SWI 是否在此时触发
- **方向 B**：搜索软件 LZ77 实现——在 all.s 中搜索典型 LZ77 解压特征代码（滑动窗口、位读取循环）
- **方向 C**：ROM 离线搜索压缩块——扫描 ROM 中 LZ77 头部特征（`0x10 xx xx xx`，解压大小合理），不依赖运行时调试

---

## 五、相关文件

| 文件 | 说明 |
|------|------|
| `output/gdb_break_cardimage.gdb` | 历次 hbreak 脚本（已更新为交互模式） |
| `doc/dev/gdb-watchpoint-card-image.md` | 所有实验完整记录（含本次失败） |
| `asm/all.s` line 3526 | FUN_08014fa8 反汇编（Ghidra 导出） |
| `doc/analysis/card-detail-page.md` | VRAM 布局分析（BG2 = 卡图层） |

## 附录：THUMB 高寄存器 MOV 速查

Ghidra 有时将 THUMB 高寄存器操作输出为 `.hword 0xXXXX`，解码方法：

```
格式: 0100 0110 D Rm Rdn  (16位 little-endian)
      ^^^^ ^^^^           固定前缀 0x46xx

D   = bit 7 of byte 1
Rm  = bits [6:3] of byte 1
Rdn = bits [2:0] of byte 1
目标寄存器 = D*8 + Rdn

常见示例：
  0x4688  = 0100 0110 1000 1000  → MOV r8, r1   (D=1, Rm=r1, Rdn=r0+8=r8)
  0x4641  = 0100 0110 0100 0001  → MOV r1, r8   (D=0, Rm=r8, Rdn=r1)
  0x4657  = 0100 0110 0101 0111  → MOV r7, r10  (D=0, Rm=r10, Rdn=r7)
```
