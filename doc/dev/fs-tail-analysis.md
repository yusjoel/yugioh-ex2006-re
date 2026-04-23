# FS 尾段 (0x1ED4AA4 .. 0x2000000) 分段分析 — 任务 D2

**日期**：2026-04-23（bug #12 修复后更新）
**范围**：ROM `0x01ED4AA4..0x02000000`（= **1,225,564 B** = 1.17 MB）
**任务目标**：prompt 声称此段含 "125 KB NitroSDK assertion 池"，要求进一步分段结构化

> **注**：早期 FS 尾段起点是 `0x1ED49D4`（含 FID 339 orphan palette 208 B）。
> bug #12 修复后 orphan 正式并入 `data/fs-payload.s`，尾段起点后移到 `0x1ED4AA4`，
> 缩短 208 B。本文分段编号保留以利对照；段 A 现属 FS 内部，不再是尾段范围。

---

## 一、宏观布局（修订版）

| 段 | 范围 | 大小 | 内容 | 熵（每字节比特） |
|---|---|---|---|---|
| ~~**A**~~ | `0x1ED49D4..0x1ED4AA4` | 208 B | **已移入 fs-payload（FID 339 orphan NCLR 调色板）**，不再属尾段 | — |
| **B** | `0x1ED4AA4..0x1ED52A4` | ~2 KB | 稀疏结构化（u32 指针 + 大量 0） | ≈ 0.7 |
| **C** | `0x1ED52A4..0x2000000` | **1,222,188 B** | **均匀随机数据**，等同 ROM padding | 7.996 |

（段 A 现在就是 FID 339 orphan palette `title_obj_s.LZnclr`，见 `fs/titleEx/title_obj_s.LZnclr`
与 `fs-decompressed/titleEx/title_obj_s.nclr`。）

---

## 二、段 B（结构化 2 KB）详探

范围：`0x1ED4AA4..0x1ED52A4`（~2 KB，非零字节 ≈ 3,245/4,096 前段）

### 头部字节

```
+0x00  2c 39 07 00       u32 = 0x00073928 = 473,384  （疑似 table size / offset）
+0x04  00 00 00 00       reserved
+0x08  8c 4c ed 09       ROM 指针 → 0x09ED4C8C (= ROM 偏移 0x1ED4C8C，在段 B 自身内部)
+0x0C  e4 4c ed 09       → 0x09ED4CE4
+0x10  3c 4d ed 09       → 0x09ED4D3C
+0x14 .. +0x3F           全 0
+0x40  7c 86 e5 09       → 0x09E5867C (= ROM 偏移 0x1E5867C，pre-FS 区域)
+0x44 .. +0x5B           全 0
+0x5C  01 00 00 00       u32 = 1
...
+0x100..+0x3FF           全 0
```

### 指针表（`+0x400..+0x800`）

从 `+0x400 (0x1ED4EA4)` 开始出现 u32 指针密集数组，每条 4 B，指向 `0x09ED4E98` 附近：

```
+0x400  98 4e ed 09 a0 4e ed 09 a0 4e ed 09 a8 4e ed 09
+0x410  a8 4e ed 09 b0 4e ed 09 b0 4e ed 09 b8 4e ed 09
```

解读：u32 指针 `0x09ED4E98`, `0x09ED4EA0`, `0x09ED4EA0`, `0x09ED4EA8`, ... 步长 8 B，
成对出现（每 2 个相同）。典型 "next/prev" 链表或 pair 结构。

### 推断

- 此 2 KB 疑是**运行时初始化的全局变量的段映像**（BSS/.data 末尾），链接器 section 排序
  让它落在 FS 数据后（没人显式 `.incbin` 到这片）
- 所有指针 `0x09ED4xxx` 都回指自身区域，确认这是一个自引用数据结构
- `0x09E5867C` 指向 pre-FS 区域 (`0x1E5867C`)，可能是 code 或早期 data 表

由于指针值依赖 CPU 地址（`0x09xxxxxx` = ROM mirror address），这**不是输入/输出数据**，
而是 **静态初始化表**。从 `asm/all.s` 中追对 `0x09ED4AA4` 附近指针的引用，可定位到其 consumer。

（完整 C/C++ struct 布局逆向非本任务范围，留待后续做链接重构时需要再碰。）

---

## 三、段 C（1.17 MB 高熵填充）

### 熵剖面

用 4 KB 滑动窗分析熵：

| chunk | 地址 | 熵 | 备注 |
|---|---|---|---|
| [0] | `0x1ED49D4` | 6.456 | 段 A + 段 B 前半 |
| [1] | `0x1ED59D4` | **7.959** | **段 C 起点** |
| [2]–[299] | `0x1ED69D4..0x1FFF9D4` | 7.95–7.997 | 全段 C |

### 字节分布（取样 64 KB）

```
 @0x1EE0000: top 3 = 0xED(311), 0x84(299), 0xFD(291)
 @0x1F00000: top 3 = 0xC3(300), 0x85(300), 0xE2(296)
 @0x1FF0000: top 3 = 0x3E(305), 0x82(299), 0xB7(298)
```

每字节计数 ≈ 65536/256 ≈ 256，无偏，**符合均匀随机分布**。

### ASCII 字符串扫描

- **0 条** 含 "nitro" / "nnsys" / "nns_"
- **0 条** 含 `.c` / `.h` / `include/`
- 所有 "run of 8+ ASCII chars" 都是巧合命中的随机字节（语义上是噪声）

### 推断

段 C 的 1.17 MB **不含 NitroSDK assertion 串池**（prompt 声称有误）。
最可能的解释是 **ROM 卡带容量补齐填充**（padding to 32 MB = 0x02000000）：

- 真实游戏数据终止于 `~0x1ED59D4`（约 31 MB）
- 余下 1.17 MB 填充至 32 MB cartridge 边界
- 填充内容 **不是全零**（如 `0xFF` 或 `0x00`），也不是已知的惰性 pattern，
  而是均匀随机字节 → 可能是：
  - Konami 的私有 PRNG 生成的反工程扰动
  - 加密/混淆数据（但无已知对应解密路径）
  - 另一个 ROM 镜像的 junk data（如早期开发版的 leftover）

不管是哪种，**不含可恢复的 game logic 或 asset**。D2 任务结束：
- ~~**段 A**~~：已解（A1 任务），bug #12 修复后并入 fs-payload.s，不再属尾段
- **段 B**：稀疏 pointer table；非关键；留待后续按需追 consumer
- **段 C**：纯 padding / 噪声，无 asset 语义

---

## 四、对 PLAN.md 进度的影响

原 PLAN.md 若认为 "FS 尾段全部可结构化"，应修正为：
- 可结构化部分 ≈ 2 KB (段 B) — 段 A 208 B 已并入 FS
- 剩余 1.22 MB (= 尾段的 99.84%) 为**不可结构化随机填充**

覆盖率增益有限：新增 ≈ 2 KB 可标注 → 约 0.006% 百分比推进。

---

## 五、后续

若未来想完全消除 "unknown" 标记：
1. **段 B 的 2 KB**：反编译找对 `0x09ED4C8C` 等指针的 consumer，推 C struct 布局，替换为带注释的 `.word` 数据
2. **段 C 的 1.22 MB**：确认是否由 Konami build tool 生成的确定性填充（若是 PRNG，找 seed 后可程序化重建），或接受其为 `.incbin` 不入库的 blob

当前方案：`asm/rom.s` 已用单个 `.incbin "roms/2343.gba", 0x1ED4AA4, 0x12B55C` 覆盖整片
尾段——byte-identical 构建不受影响。
