# 卡包封面图静态分析报告

**日期**: 2026-04-16
**目标**: 定位 pack 列表页 5 张卡包封面条幅图 (32×64, 8bpp OBJ sprite) 的 ROM 数据来源
**方法**: 参照 `doc/dev/locate-rom-asset-from-vram-diff.md` 六步流程，执行方向 B + C

---

## 一、OAM 分析 (state2_pack_list)

DISPCNT=0x1D00 → OBJ 使用 **2D tile mapping** (bit 6=0)。

### 卡包封面 OBJ sprite (OAM #19-#23)

| OAM# | X | Y | 尺寸 | 色深 | Tile# | VRAM 地址 | 优先级 |
|-------|-----|-----|--------|------|-------|-----------|--------|
| #19 | 27 | 48 | 32×64 | 8bpp | 512 | 0x06014000 | 3 |
| #20 | 65 | 48 | 32×64 | 8bpp | 520 | 0x06014100 | 3 |
| #21 | 104 | 48 | 32×64 | 8bpp | 528 | 0x06014200 | 3 |
| #22 | 142 | 48 | 32×64 | 8bpp | 536 | 0x06014300 | 3 |
| #23 | 181 | 48 | 32×64 | 8bpp | 768 | 0x06016000 | 3 |

2D mapping 下 tile 寻址: `VRAM_addr = 0x06010000 + tile_number * 32`。
每 sprite 32×64=4×8 tiles (8bpp), 每行 4 tiles × 64B = 256B, 行间距 = 32 slots × 32B = 1024B (0x400)。

### 其他相关 sprite

| OAM# | 尺寸 | 色深 | 说明 |
|-------|--------|------|------|
| #4 | 32×64 | 4bpp, pal 13 | 选中卡包高亮边框 |
| #5-9 | 32×16 | 4bpp, pal 14, 半透明 | "NEW" 标签 (共享 tile 780) |
| #11-18 | 32×16 / 8×16 | 4bpp, pal 11 | 底部 UI 文字 ("Return / Exchange") |

---

## 二、方向 B：VRAM 字面量搜索

### 指纹强度评估

| 字面量 | asm/all.s 命中数 | 评级 |
|--------|------------------|------|
| `0x06014000` | 52 | 弱 (信噪比低) |
| `0x06016000` | **2** | **极强** |
| `0x06015000` | 2 | 极强 |
| `0x06014200` | 5 | 强 |

### 命中函数

两个 `0x06016000` 命中均在 0x080B 代码区:

1. **0x080BCD84** → 属于 switch 函数 (入口约 0x080BCC7E), case 0/1/2 处理卡包分类 overlay
2. **0x080BE120** → 属于 **FUN_080bdfac** (0x080BDFAC), case 0 处理卡包封面区域

### FUN_080bdfac — 卡包 UI 运行时状态机

- **入口**: 0x080BDFAC
- **调用者**: `0x0801F14E` (`switchD_0801efa4__caseD_1`, 顶层菜单)
- **状态结构体**: `0x0201FEC0`, offset 0x10 = case 编号 (0-6)
- **7 路 switch**: case 0 加载图形, 其余处理动画/交互

#### Case 0 图形加载逻辑

分两个 code path (由 `byte_at(0x02023396) & 0x40` 选择):

**Path A (bit 6 clear)**:
```
1. FUN_080f4ea4(0x05000260, 0x0992069c, 0x20)     ← 调色板 A → OBJ PALRAM
2. index = byte_at(0x02006c2c) & 0x7
   src = 0x099206bc + index * 9 * 0x800             ← tile base A
   FUN_080f74d4(0x06014000, src, 0x18, 0x4)         ← 24 tiles wide × 4 rows
3. (查表加载 → 0x06015000)
```

**Path B (bit 6 set)**:
```
1. FUN_080f74d4(0x06014000, src_B, 0x18, 0x4)       ← 不同 ROM base
2. FUN_080f74d4(0x06016000, src_C, 0x18, 0x8)       ← 8 rows
```

#### FUN_080f74d4 — 2D tile row-copy

```
FUN_080f74d4(vram_dest, rom_src, width_tiles, height_rows):
  row_bytes = width_tiles << 5    // = width_tiles * 32
  for i in range(height_rows):
    memcpy(vram_dest, rom_src, row_bytes)
    vram_dest += 0x400            // 2D mapping 行间距
    rom_src   += row_bytes
```

被调用 130 次, 是通用的 2D OBJ tile 行拷贝器。

#### ROM 源地址 (分类 overlay)

| 标签 | 调色板地址 | Tile base | 间距 | 高度 |
|------|-----------|-----------|------|------|
| A | 0x0992069c | 0x099206bc | index × 0x4800 | 4 rows |
| B | 0x0993b6bc | 0x0993b6dc | index × 0x1800 | 8 rows |
| C | 0x099446dc | 0x099446fc | index × 0x1800 | 8 rows |

**ROM 数据验证**: 绝大部分 index 的 tile 数据为**全零**; 仅 index=6 的 base A 区域有非零 palette 数据 (暖色渐变)。说明这些 ROM 地址存储**分类级 overlay** (选中高亮/发光特效), 不是逐 pack 封面图。

### 相关 switch 函数 (0x080BCC area)

入口约 0x080BCC7E, 9 路 switch (state struct offset 0x12)。
Case 0 分 3 个子路径 (r2=0/1/2):
- 子路径 1: `0x0993b6bc/dc` → 0x06016000, height=8
- 子路径 2: `0x099446dc/fc` → 0x06016000, height=8
- 公共: 调色板 → 0x05000280, BLDCNT/WINOUT 设置

---

## 三、方向 C：IO 寄存器指纹搜索

### 指纹选择

| IO 值 | 寄存器 | asm/all.s 命中数 | 评级 |
|--------|--------|------------------|------|
| `.word 0x00001E0D` | BG2CNT | **1** | **极强 (一击命中)** |
| `.word 0x00001F0F` | BG3CNT | 2 | 极强 |
| `.word 0x00001C00` | BG0CNT (literal) | 0 | 不出现 (inline 构造) |
| `.word 0x00001D00` | DISPCNT | 0 | 不出现 |

BG0CNT=0x1C00 通过 `movs r0, #0xE0; lsls r0, r0, #5` 内联构造，无字面量。

### 命中路径

`.word 0x00001E0D` 唯一命中 → **FUN_080d8d84** (0x080D8D84):

```asm
FUN_080d8d84:
  ldr r1, =0x04000008         @ BG0CNT 寄存器
  movs r0, #0xE0
  lsls r0, r0, #5             @ r0 = 0x1C00
  strh r0, [r1]               @ BG0CNT = 0x1C00
  adds r1, #4                 @ r1 = 0x0400000C (BG2CNT)
  ldr r0, =0x1E0D
  strh r0, [r1]               @ BG2CNT = 0x1E0D
  @ 后续清空 VRAM: 0x06000000(CBB0), 0x0600E000(SBB28), 0x0600D000, 0x0600F000(SBB30)
```

### 调用图爬升

```
FUN_080d8d84
  ↑ 唯一调用者
FUN_080d971c  ← pack 列表页初始化器 (函数指针表 0x09E4948C[11])
  ├─ bl FUN_080d8d84     BG 配置 + VRAM 清空
  ├─ bl FUN_080d8f08     BG tilemap 加载
  │    ├─ FUN_0810e418(0x09CCE2B0+4, 0x0600D000)  解压 tilemap
  │    ├─ FUN_0810e418(0x09CCE2D0+4, 0x0600F000)  解压 tilemap
  │    └─ FUN_080f4f08(0x050001A0, 0x09CCE2C0+4, 0x20)  调色板
  ├─ loop × N: bl FUN_080d8e98   逐 pack 初始化
  │    ├─ bl FUN_080d8f48(pack_id, slot)
  │    │    └─ bl FUN_080db860(pack_id, vram, 0, 1)  OBJ tile 加载
  │    │         └─ ROM 指针表 0x09CCE960[pack_id] → 0x800B data (全零!)
  │    ├─ bl FUN_080dbbc0(buf+8, pack_id)  文字渲染 (pack 名称)
  │    │    ├─ ROM pack 信息表: 0x09E5E2E8 (每条 16B)
  │    │    ├─ text_render_wrapper × 2
  │    │    └─ commit_line_buffer_to_sprite_vram
  │    ├─ bl FUN_080dbf40  pack 详情
  │    └─ bl FUN_080dc098  pack 卡牌信息
  ├─ bl FUN_080f4f08     EWRAM → BG VRAM 批量复制
  ├─ bl FUN_080d912c     UI 滚动条布局
  ├─ bl FUN_080dc378     文字渲染 (价格)
  ├─ bl FUN_080dc3b8     文字渲染 (DP 信息)
  └─ bl FUN_080d91e0     收尾
```

### 函数指针表 (0x09E4948C)

Pack 模块完整回调表, 32 条目 (含 2 个 null 分隔):
- [0-8]: 第一组 9 个函数 (0x080D87D1 - 0x080D8D2D)
- [9]: null 分隔
- [10-19]: 第二组, [11] = **FUN_080d971c** (page init)
- [20-31]: 第三组 + null 终止

所有函数均在 0x080D8000-0x080DAE00 范围, 紧密聚集。

---

## 四、关键数据结构

### ROM 数据表

| 地址 | 用途 | 条目数 | 条目大小 |
|------|------|--------|---------|
| `0x08510440` | **pack banner OBJ 调色板** | 256 色 | 512B (BGR555) |
| `0x09CCE960` | pack 图片指针表 | 51 | 4B (ptr) |
| `0x09CCEA2C-0x09CE7A2C` | pack 图片 tile 数据 | 51 | 0x800B |
| `0x09CCE2B0/C0/D0` | BG tilemap 间接指针 | 3 | 指针+数据 |
| `0x09E5E2E8` | pack 信息记录表 | ~51 | 16B |
| `0x09E4948C` | pack 模块函数指针表 | 32 | 4B |

### EWRAM 布局

| 地址 | 用途 |
|------|------|
| `0x0201FEC0` | pack UI 状态结构体 (FUN_080bdfac 用) |
| `0x02006C2C` | pack 分类 index (bits 0-2) |
| `0x02023360` | pack 显示标志 (bit 6 @ offset 0x36) |
| `0x02029EB0` | pack 记录缓存 (每条 0x1288B, 含渲染后文字 tile) |

### PALRAM 目标

| PALRAM 地址 | 用途 | ROM 源 |
|-------------|------|--------|
| `0x05000200-0x050003FF` | OBJ 256 色调色板 (全) | `0x08510440` (512B) |
| `0x05000200-0x05000320` | Slot 0-8: banner tile 使用 | 同上 (前 288B) |
| `0x05000340-0x050003FF` | Slot 10-15: UI 元素 (运行时填充) | 各 UI 函数 |
| `0x05000260` | Slot 3: overlay 调色板 A | `0x0992069c` (32B) |
| `0x05000280` | Slot 4: overlay 调色板 B | `0x098a5024` (32B) |
| `0x050001A0` | BG 调色板 | `0x09CCE2C0+4` (32B) |

### VRAM 目标

| VRAM 地址 | 用途 | 写入者 |
|-----------|------|--------|
| `0x06014000-0x06015FFF` | 前 4 张 pack 封面 (OBJ tile 512-639) | FUN_080db860 |
| `0x06016000-0x06017FFF` | 第 5 张 pack 封面 (OBJ tile 768+) | FUN_080db860 |
| `0x0600E000` | BG0 SBB28 tilemap | FUN_080d8d84 清空 |
| `0x0600D000/F000` | BG2 SBB26/30 tilemap | FUN_080d8f08 加载 |
| `0x06000240` | BG0 CBB0 pack 名称 tile | FUN_080d8f84 |

---

## 五、方向 A：GDB hbreak 动态验证

### 实验结果

hbreak 在 `FUN_080d971c` 和 `FUN_080db860` 上，游戏导航至 pack 列表后全部命中：

- **HIT 1**: `FUN_080d971c` (page init), LR=0x080DAE5F (函数指针表调度)
- **HIT 2-6**: `FUN_080db860` 调用 5 次, 参数：

| Hit | r0 (pack_id) | r1 (VRAM dest) | r3 (mode) |
|-----|-------------|----------------|-----------|
| 2 | 0 | 0x06014000 | 1 |
| 3 | 1 | 0x06014100 | 1 |
| 4 | 2 | 0x06014200 | 1 |
| 5 | 3 | 0x06014300 | 1 |
| 6 | 4 | 0x06016000 | 1 |

LR=0x080D8F7B → 均从 `FUN_080d8f48` 调用。

### VRAM watchpoint 不触发的原因

`watch *(unsigned int*)0x06014000` 未触发——推测 `FUN_080f4f08` 在当前运行时使用 DMA 模式（flag bit 13 at 0x030001B4 为 set），绕过了 CPU 硬件 watchpoint。这是方向 A 的已知限制。

## 六、ROM 数据验证——初始错误修正

### 关键修正

方向 B/C 分析时报告"ROM 指针表 0x09CCE960 的 51 条数据全零"是**误判**。原因：仅检查了每条 0x800 字节的前 16-32 字节（恰好是零 padding），未检查完整数据块。

**实际情况**：每个 pack 的 0x800 字节块中有 **1800 字节非零 tile 数据**，首个非零字节在 offset **0x11**（前 0x11 字节是零 padding/透明像素）。

### ROM 字节搜索验证

从 state2 VRAM 快照 `0x06014020` 提取 16 字节，在 ROM 中搜索 → **唯一命中** `0x1CCEA4C`（= pack 0 数据起始 `0x1CCEA2C` + 0x20）。

### 完整匹配验证

| Slot | Pack | VRAM 地址 | ROM 偏移 | 行匹配 |
|------|------|-----------|---------|--------|
| 0 | 0 | 0x06014000 | 0x1CCEA2C | **8/8** |
| 1 | 1 | 0x06014100 | 0x1CCF22C | **8/8** |
| 2 | 2 | 0x06014200 | 0x1CCFA2C | **8/8** |
| 3 | 3 | 0x06014300 | 0x1CD022C | **8/8** |
| 4 | 4 | 0x06016000 | 0x1CD0A2C | **8/8** |

VRAM 2D 映射布局（行间距 0x400）与 ROM 连续布局（行间距 0x100）的转换由 `FUN_080db860` mode 1 完成，逐行复制 8×256B。

### 全 51 pack 数据分布

- 每条: 0x800 字节 (2048B), 含 1800 字节有效像素
- Pack 0-17: 第一种色调 (first_byte pattern `8383...`)
- Pack 18-44: 第二种色调 (pattern `7979...`)
- Pack 45-50: 各有独特色调
- 总数据量: 51 × 0x800 = 0x28800 = 165,888 字节

### ROM 布局

```
0x09CCE960 (ROM 0x1CCE960): 指针表 [51 entries × 4B = 204B]
0x09CCEA2C (ROM 0x1CCEA2C): Pack 0 tile data (0x800B)
0x09CCF22C (ROM 0x1CCF22C): Pack 1 tile data (0x800B)
...
0x09CE7A2C (ROM 0x1CE7A2C): Pack 50 tile data (0x800B)
                             Total = 0x09CE822C
```

## 七、完整调用链（已验证）

```
函数指针表 0x09E4948C[11] → FUN_080d971c (pack list page init)
  ├─ bl FUN_080d8d84         BG 配置 (BG0CNT=0x1C00, BG2CNT=0x1E0D)
  ├─ bl FUN_080d8f08         BG tilemap 加载 (ROM 0x09CCE2B0/C0/D0)
  ├─ loop × 5: bl FUN_080d8e98  逐 pack 初始化
  │    ├─ bl FUN_080d8f48(pack_id, slot_index)
  │    │    └─ bl FUN_080db860(pack_id, vram_addr, 0, 1)  ★ 卡包封面 tile 加载
  │    │         ├─ ROM 指针表: 0x09CCE960[pack_id] → pack tile data (0x800B)
  │    │         ├─ 格式: 8bpp raw tiles, 8 rows × 256B, 2D stride copy
  │    │         └─ VRAM 目标: 0x06014000/0x06014100/.../0x06016000
  │    ├─ bl FUN_080dbbc0     文字渲染 (pack 名称)
  │    ├─ bl FUN_080dbf40     pack 详情
  │    └─ bl FUN_080dc098     pack 卡牌信息
  └─ 后续 UI 布局 + 文字渲染
```

## 八、调色板定位

### 方法: ROM 字节搜索

从 state2 PALRAM 快照 (`state2_pack_list_palram.bin`) 提取 OBJ palette 各 slot 的前 16 字节，在 ROM 中搜索。

### 结果

| Sub-palette slot | PALRAM 地址 | ROM 命中 | 状态 |
|-----------------|-------------|----------|------|
| 0 | 0x05000200 | 0x510440 | MATCH |
| 1 | 0x05000220 | 0x510460 | MATCH |
| 2 | 0x05000240 | 0x510480 | MATCH |
| 3 | 0x05000260 | 0x5104A0 | MATCH |
| 4 | 0x05000280 | 0x5104C0 | MATCH |
| 5 | 0x050002A0 | 0x5104E0 | MATCH |
| 6 | 0x050002C0 | 0x510500 | MATCH |
| 7 | 0x050002E0 | 0x510520 | MATCH |
| 8 | 0x05000300 | 0x510540 | MATCH |
| 9 | 0x05000320 | 0x510560 | MATCH (全零) |
| 10-15 | 0x05000340+ | 不匹配 | UI 运行时填充 |

Slot 0-9 连续存储在 **ROM 0x510440**（512 字节），紧跟在 `card-image-palettes.s` (0x4C76C0-0x510440) 之后。

### 像素 index 范围分析

Banner tile 使用 pixel index 0-143 → 覆盖 slot 0-8 (144 色)：
- Pack 00: 61 unique colors, slots {0,1,2,3,4,5,6,7,8}
- Pack 18: 62 unique colors, slots {0,1,2,3,4,5,6,7,8}
- Pack 45: 34 unique colors, slots {0,2,3,4,5,6,7,8}

Slot 10-15 为 UI 元素使用：选中框 (pal 13)、"NEW" 标签 (pal 14)、文字 (pal 11/15) 等。

### 彩色渲染验证

使用 ROM 0x510440 调色板渲染彩色 PNG，与 `state2_pack_list.png` 截图目视对比：
- Pack 00 (LEGEND OF B.E.W.D.): 蓝眼白龙图案，绿色调 ✓
- Pack 04 (DARK MAGICIAN GIRL): 黑魔导女孩图案，绿色调 ✓
- Pack 46 (ELEMENTAL HERO): 英雄图案，暖橙色调 ✓

**调色板定位完成。**
