# HUD UI 资源在 `asm/all.s` 里的引用图谱

**触发问题**：确认 ROM `0x01E246D4` + 3,712 B 是否被代码引用、以及附近是否有更多 sheet。

**结论（先行）**：
1. `0x01E246D4` **确实被引用**（`asm/all.s:334143`，函数 `FUN_08101068`）。
2. 该引用是一组 **BG + OBJ tile block + 3 条 palette** 的连续批量拷贝序列的一部分，整体连续 sheet = **`0x01E246D4..0x01E25554`（3,712 B = 116 tiles × 32B）**，与 stride-4 VRAM 扫描结果完全一致。
3. **附近还有大量未归档 sheet**：FUN_08101068 后续 + `FUN_081016c0`（状态切换拷贝）+ `FUN_081066fc`（OBJ 小块）+ 一个 **13 分支 switch dispatcher `FUN_08109788`** 共索引 13 张额外 sprite sheet，全部位于 UNKNOWN 段 `0x01DFF9D2 / 0x31B82`。
4. **两个调色板落在 UNKNOWN 段 `0x01E31714`**：`0x01E31754`（FUN_081058c8 调色板动画源）与 `0x01E31794`（FUN_081066fc OBJ pal 8）。

---

## 一、`FUN_08101068` —— HUD / 列表视图资源装载（单次）

位于 `asm/all.s:334019`，入口 `0x08101068`。一次性将以下 ROM 源段 DMA 拷到 VRAM + PALRAM。

### BG 部分（dest → OBJ cb3 的 0x0600C000 区）

| ROM 源 | ROM 终 | tiles | VRAM dest | 备注 |
|---|---|---:|---|---|
| `0x01E246D4` | `0x01E247B4` | 7 | `0x0600C3A0` | **HUD 数字/图标 sheet 起点** |
| `0x01E247B4` | `0x01E24834` | 4 | `0x0600C480` | 紧邻 |
| `0x01E24834` | `0x01E24934` | 8 | `0x0600C500` | 紧邻 |
| `0x01E24934` | `0x01E24AF4` | 14 | `0x0600C040` | 紧邻（同源亦拷 OBJ） |
| `0x01E24AF4` | `0x01E24C94`¹ | 13 | `0x0600C200` | 紧邻（同源亦拷 OBJ） |

¹ BG 只拷前 13 tiles；实际该块的 OBJ 复用扩到 `0x01E24CF4`（16 tiles）。

### OBJ 部分（dest → OBJ tile mem `0x06016000`+）

| ROM 源 | ROM 终 | tiles | VRAM dest | 调用 | 尺寸 |
|---|---|---:|---|---|---|
| `0x01E24934` | `0x01E24B14` | 14 (0xE) | `0x06016400` | tile_2d_row_copy | (0xE,1) |
| `0x01E24AF4` | `0x01E24CF4` | 16 (0x10) | `0x06016800` | tile_2d_row_copy | (0x10,1) |
| `0x01E24CF4` | `0x01E24EF4` | 16 | `0x06016C00` | tile_2d_row_copy | (0x10,1) |
| `0x01E24EF4` | `0x01E250F4` | 16 | `0x06017000` | tile_2d_row_copy | (0x10,1) |
| `0x01E250F4` | `0x01E252F4` | 16 | `0x06017400` | tile_2d_row_copy | (0x10,1) |
| `0x01E252F4` | `0x01E25414` | 9 | `0x06017800` | tile_2d_row_copy | (0x9,1) |
| `0x01E25414` | `0x01E25554` | 10 | `0x06017C00` | tile_2d_row_copy | (0xA,1) |

### Palette 部分

| ROM 源 | size | PAL dest | 含义 |
|---|---:|---|---|
| `0x01E31554` | 0x20 | `0x05000140` | BG palbank 10（第 1 子调色板） |
| `0x01E31554` | 0x20 | `0x05000300` | OBJ palbank 8（复用同源） |
| `0x01E31574` | 0x20 | `0x05000320` | OBJ palbank 9 |
| `0x01E31614` | 0x100 | `0x05000200` | **OBJ palbanks 0-7** 整批 |

> **注**：`0x01E31554` 是已分析的 `card-mini-frame-palette` 起点 (`data/card-mini-frame-palette.s`)，大小 0x1C0。上表所有 ROM→PAL 源都在其范围内。

### 整体覆盖

**连续合并后**：ROM `0x01E246D4..0x01E25554` = **0xE80 = 3,712 B = 116 tiles**
完美对应我前次 VRAM stride-4 扫到的 116-tile run 报告。

---

## 二、`FUN_081016c0` —— 状态切换 sprite 加载

`asm/all.s:334840`，根据状态变量 `*(short*)0x0202A4D0` 分派：

### state == 1（`LAB_081016D8`）
| ROM 源 | size | dest | 用途 |
|---|---:|---|---|
| `0x01E25934` | (0xC, 2) tiles | `0x06016A80` (OBJ) | sprite sheet A |
| `0x01E25674` + N·0x40 | (1, 2) × 11 iter | `0x060162A0`+ | 11 个小 sprite 循环拷（按 VRAM dest 步 0x40） |
| `0x01E31594` | 0x20 | `0x05000360` (OBJ pal B) | palette |

### state == 3（`LAB_08101724`）
| ROM 源 | size | dest |
|---|---:|---|
| `0x01E25C34` + N·0x80 | (2, 2) × 6 iter | `0x06016A80`+ |
| `0x01E315B4` | 0x20 | `0x05000360` (OBJ pal B) |

---

## 三、`FUN_081066fc` —— 小 UI 块（unknown seg palette）

`asm/all.s:345253`。

| ROM 源 | size | dest | 所属段 |
|---|---:|---|---|
| `0x01E310B4` | (0x8, 2) = 16 tiles | `0x06016300` (OBJ) | **UNKNOWN `0x01DFF9D2`** |
| `0x01E31794` | 0x20 | `0x05000300` (OBJ pal 8) | **UNKNOWN `0x01E31714`** |

---

## 四、`FUN_08109788` —— 13 路 switch dispatcher

`asm/all.s:351625`，输入 case 0..12 返回对应 sprite sheet 指针。**所有 13 个指针落在 UNKNOWN `0x01DFF9D2`**：

| case | ROM 指针 | stride vs 前 |
|---:|---|---:|
| 0 | `0x01E265B4` | — |
| 1 | `0x01E26AB4` | +0x500 |
| 2 | `0x01E270B4` | +0x600 |
| 3 | `0x01E27BB4` | +0xB00 |
| 4 | `0x01E280B4` | +0x500 |
| 5 | `0x01E289B4` | +0x900 |
| 6 | `0x01E28DB4` | +0x400 |
| 7 | `0x01E2A1B4` | +0x1400 |
| 8 | `0x01E2CDB4` | +0x2C00 |
| 9 | `0x01E2DDB4` | +0x1000 |
| a | `0x01E297B4` | （0x01E28DB4+0xA00） |
| b | `0x01E2B7B4` | |
| c | `0x01E2D5B4` | |

非均匀 stride → 每个 case 对应不同尺寸的独立 sheet（估计按 case 角色不同：卡种徽章 / 等级星 / 属性 / 种族，正好 ≈13 种）。

---

## 五、其他散点引用（单发）

| 引用处 | ROM | 推测用途 |
|---|---|---|
| `asm/all.s:15749` (`0x0801D50C`) | `0x01E31614` | 某处直接读 mini-frame-palette 子区（OBJ pal 0-7 起点） |
| `asm/all.s:17486` (`0x0801E290`) | `0x01E2DDB4` | 与 switch case 9 同一 sheet 的独立引用 |
| `asm/all.s:332592/332647/351687` | `0x01E28DB4` | switch case 6 + 两处 hardcoded 调用 |
| `asm/all.s:332596/351707` | `0x01E2CDB4` | switch case 8 |
| `asm/all.s:332651/351697` | `0x01E2A1B4` | switch case 7 |
| `asm/all.s:335387` (`0x08101ADC`) | `0x01E31594` | 单独 pal B 副本 |
| `asm/all.s:340955` (`0x081044A8`) | `0x01E25F34` | 独立 sprite sheet（未被 switch 覆盖） |
| `asm/all.s:341096` (`0x081045BC`) | `0x01E315D4` | 单独 palette 0x20 |
| `asm/all.s:343436` (`0x08105908`) | `0x01E31754` | **UNKNOWN `0x01E31714`** — **动画 palette 表**（16×N halfwords，循环索引读取） |
| `asm/all.s:345271` | `0x01E310B4` | 见第三节 |
| `asm/all.s:345275` | `0x01E31794` | **UNKNOWN `0x01E31714`** |
| `asm/all.s:346932/351994/354000` | `0x01E25554` | 多处引用 HUD sheet 尾边界 |
| `asm/all.s:346960` (`0x081073AC`) | `0x01E3157A` | **未对齐**，疑似读取单色 halfword |
| `asm/all.s:346991/347698` | `0x01E31574` | pal 9 复用 |
| `asm/all.s:347694` (`0x08107960`) | `0x01E252F4` | HUD sheet 内 OBJ 起点复用 |
| `asm/all.s:351255` (`0x081094C8`) | `0x01E26334` | 0x01E26 范围内的孤立 sheet（switch 外） |
| `asm/all.s:351400` (`0x081095E4`) | `0x01E315FA` | **未对齐** palette 读 |
| `asm/all.s:376006` (`0x084C4B10`) | `0x01E209DD` | **未对齐**，代码段末尾，疑似字符串/指针表内嵌 |

---

## 六、`0x01E246D4` 附近 ROM 更大图景

把所有已识别引用按 ROM 升序排列：

```
0x01E246D4  ─┐
 ...          │ (HUD sheet — FUN_08101068 批量加载, 116 tiles / 3712 B)
0x01E25554  ─┘
0x01E25674    (FUN_081016c0 state=1, 11-iter 循环)
0x01E25934    (FUN_081016c0 state=1, sheet A)
0x01E25C34    (FUN_081016c0 state=3, 6-iter 循环)
0x01E25F34    (FUN @0x081044A8, 未归档)
0x01E26334    (FUN @0x081094C8)
0x01E265B4  ┐
0x01E26AB4  │
0x01E270B4  │
0x01E27BB4  │ 13 张 switch dispatcher sheet
0x01E280B4  │ (FUN_08109788, 按 case 0..c)
0x01E289B4  │
0x01E28DB4  │
0x01E297B4  │
0x01E2A1B4  │
0x01E2B7B4  │
0x01E2CDB4  │
0x01E2D5B4  │
0x01E2DDB4  ┘
...
0x01E310B4    (FUN_081066fc, 16 tiles OBJ)
0x01E31554    ── card-mini-frame-palette 起点（已知，ends 0x01E31714）
0x01E31754    (FUN_081058c8 palette 动画, UNKNOWN seg)
0x01E31794    (FUN_081066fc pal, UNKNOWN seg)
```

**UNKNOWN 段 `0x01DFF9D2 / 0x31B82`（203,650 B）内明确引用的累计字节**：
- HUD sheet：3,712 B
- 13 张 switch sheet（估计按平均 1.5 KB）：~20 KB
- 其他 state sheet + 散点：~5 KB
- 合计 **估计 ≥ 28 KB**（占该段 14%），与 stride-4 VRAM 扫到的 15 KB 下限一致；更多内容当前 ss 画面未引用、暂未显式识别。

**UNKNOWN 段 `0x01E31714 / 0x275FA`（161,274 B）**：
- 仅 `0x01E31754`（动画调色板）和 `0x01E31794`（单 subpal）**两处** 代码级引用，合计 ~几百字节。
- 整段剩余 >160 KB 尚无显式引用 —— 大概率是**静态 palette 库**（对应 `data-analysis-coverage.md` 里"调色板后，对手卡值前"的备注），需切换更多 UI 场景才能触发。

---

## 七、后续建议

1. **立即可结构化**：
   - HUD sheet (`0x01E246D4..0x01E25554`) 已导出 `graphics/bin/ui-misc/hud_digits_icons_sheet.bin`，
     可直接在 `asm/rom.s` 里把 raw incbin 替换为新路径，`build.bat` 验证 byte-identical。
2. **下一批目标 sheet**：
   - FUN_081016c0 的两组（state=1/3）结构已清楚；`0x01E25674/5934/5C34/5F34` 依次导出 4 个小 sheet。
   - 13 张 switch sheet 可一次性导出到 `graphics/bin/ui-misc/switch_sheets/case_0..c.bin`，每张按 stride 裁剪。
3. **Palettes 归档**：
   - 把 `0x01E31754`、`0x01E31794` 从 UNKNOWN `0x01E31714` 拆出独立 .bin，明确命名（palette-anim / obj-pal-aux）。
4. **未引用的剩余 ~175 KB（seg `0x01DFF9D2` 未提及部分 + seg `0x01E31714` 大部分）**：
   - 切换更多 UI 画面（商店 / 卡包 / 对手选择 / 决斗中 phase 切换）再次做 stride-4 VRAM→ROM 扫描，逐步覆盖。
