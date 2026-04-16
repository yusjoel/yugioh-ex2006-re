# 工作流：从未知 ROM 资产到结构化汇编的完整流程

**写作日期**：2026-04-16
**实战案例**：卡包封面条幅图（pack banner），51 张 32×64 8bpp OBJ sprite
**耗时**：单次会话完成全流程
**前置依赖**：`doc/dev/locate-rom-asset-from-vram-diff.md`（六步定位方法论）

---

## 一、流程概览

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: 定位                                              │
│  ① 游戏截图 + VRAM/PALRAM/OAM 快照                         │
│  ② OAM 分析 → sprite 尺寸/色深/tile 地址                    │
│  ③ 三方向静态分析 (B=VRAM字面量 / C=IO指纹 / A=GDB动态)     │
│  ④ ROM 字节搜索验证 VRAM↔ROM 匹配                          │
│  ⑤ 调色板定位 (PALRAM dump → ROM 搜索)                      │
│  ⑥ 导出 PNG + 截图目视对比                                  │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 结构化                                            │
│  ⑦ 编写导出脚本 (ROM → bin + PNG + .s)                      │
│  ⑧ 修改 rom.s (拆分 incbin → .include data/*.s)             │
│  ⑨ 构建 + byte-identical 验证                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 反向标注                                          │
│  ⑩ Ghidra 函数重命名 (RenameKnownFunctions.py)              │
│  ⑪ Ghidra 数据 label (LabelPackBanners.py)                  │
│  ⑫ 重导出 asm/all.s + 构建验证                              │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 文档                                              │
│  ⑬ 分析报告 (doc/dev/*.md)                                  │
│  ⑭ 方法论更新 (locate-rom-asset-from-vram-diff.md)          │
│  ⑮ README 更新                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、各步骤详述

### Phase 1: 定位

#### ① 游戏截图 + 快照采集

**输入**：游戏存档（落在目标 UI 页面前）
**工具**：`mgba_live_start` + `mgba_live_export_screenshot` + `mgba_live_read_range`
**产出**：截图 PNG + VRAM/PALRAM/OAM/IO binary dump

本次使用了之前 `pack_capture.py` 的 7 状态快照。关键是 state2（pack 列表页）的截图和 VRAM/PALRAM dump。

#### ② OAM 分析

**输入**：OAM dump (1024 B, 128 entries × 8 B)
**方法**：解析 GBA OAM attr0/attr1/attr2，确定目标 sprite 的：
- 位置 (X, Y)
- 尺寸 (shape × size 查表)
- 色深 (4bpp / 8bpp)
- tile 编号 → VRAM 地址
- 2D / 1D 映射模式 (DISPCNT bit 6)

**本次结果**：5 个 32×64 8bpp OBJ sprite @ tile 512/520/528/536/768，2D mapping

#### ③ 三方向静态/动态分析

参照 `locate-rom-asset-from-vram-diff.md`：

| 方向 | 指纹 | 命中数 | 定位到 |
|------|------|--------|--------|
| B: VRAM 字面量 | `0x06016000` | 2 | FUN_080bdfac (状态机) |
| C: IO 指纹 | BG2CNT=`0x1E0D` | 1 | FUN_080d8d84 → FUN_080d971c (页面初始化) |
| A: GDB hbreak | FUN_080d971c + FUN_080db860 | 6 hits | 验证参数和调用链 |

**关键教训**：
- 方向 B 和 C 找到的是**互补的**函数群（运行时状态机 vs 一次性初始化）
- GDB VRAM watchpoint 因 DMA 未触发，改用 hbreak 在已知函数上成功
- `0x06014000` 有 52 处命中太多，改用 `0x06016000`（仅 2 处）作为强指纹

#### ④ ROM 字节搜索验证

**方法**：从 state2 VRAM dump 提取 OBJ tile 区特征字节，在 ROM 中搜索
**本次关键修正**：初次检查 ROM 数据时只看了前 16-32 字节（恰好是零 padding），误判为"数据全零"。后来通过 ROM 字节搜索发现数据从 offset 0x11 开始，1800/2048 字节非零。

**验证**：逐行比对 VRAM（2D stride 0x400）与 ROM（连续 0x100/行），5 个 pack 全部 8/8 行匹配。

#### ⑤ 调色板定位

**方法**：从 state2 PALRAM dump 提取 OBJ palette 各 sub-palette slot，在 ROM 中搜索
**结果**：Slot 0-9 连续命中 ROM 0x510440（512B），紧接 card-image-palettes 之后
**验证**：banner tile pixel index 范围 0-143 → 覆盖 slot 0-8（144 色），与 ROM 调色板完全匹配

#### ⑥ 导出 PNG + 目视对比

**必须步骤**：用定位到的 tile 数据 + 调色板渲染彩色 PNG，与游戏截图目视对比。
**本次拦截的 bug**：首次渲染时把 8bpp 8×8 tile 数据误当线性像素处理，导出 PNG 是乱码。对比截图后立即发现，改为按 `tile_col*64 + py*8 + px` 寻址后图案正确。

### Phase 2: 结构化

#### ⑦ 编写导出脚本

**脚本**：`tools/rom-export/export_pack_banners.py`
**产出**：
- `graphics/pack-banners/pack_XX_banner.bin` — tile 二进制（不入库）
- `graphics/pack-banners/pack_XX_banner.png` — 彩色 RGBA 预览（不入库）
- `data/pack-banners.s` — 结构化汇编（入库）

**设计要点**：
- 指针表用 `.word pack_banner_XX` label 形式，不导出为 bin——因为指针值会由汇编器根据 label 位置自动计算
- tile 数据用 `.incbin` 引用导出的 bin 文件
- PNG 渲染必须按 GBA 8×8 tile 结构解码，不能当线性像素

#### ⑧ 修改 rom.s

**操作**：将覆盖目标区域的大 `.incbin` 拆分为三段：
```
原: .incbin "roms/2343.gba", 0x1CCD290, 0xF1D8A    @ 一整段

改: .incbin "roms/2343.gba", 0x1CCD290, 0x16D0      @ 前部
    .include "data/pack-banners.s"                    @ 结构化数据
    .incbin "roms/2343.gba", 0x1CE822C, 0xD6DEE      @ 后部
```

**校验**：三段大小之和 = 原始大小（`0x16D0 + 0x198CC + 0xD6DEE = 0xF1D8A`）

#### ⑨ 构建 + byte-identical 验证

```bat
as.exe -mcpu=arm7tdmi -o output/rom.o asm/rom.s
ld.exe -T ld_script.txt -o output/2343.elf output/rom.o
objcopy.exe -O binary output/2343.elf output/2343.gba
diff <(xxd roms/2343.gba) <(xxd output/2343.gba)   @ 必须零差异
```

### Phase 3: 反向标注

#### ⑩ Ghidra 函数重命名

**脚本**：`RenameKnownFunctions.py`（追加条目）
**本次新增 11 个**：`pack_list_page_init`、`pack_banner_tile_copy`、`tile_2d_row_copy` 等
**运行**：`tools\asm-regen\ghidra-run-script.bat RenameKnownFunctions.py`

#### ⑪ Ghidra 数据 label

**脚本**：`LabelPackBanners.py`（新建）
**本次新增 53 个**：1 调色板 + 1 指针表 + 51 pack tile
**特点**：从 ROM 指针表动态读取各 pack 地址，不硬编码

#### ⑫ 重导出 asm/all.s

```bat
tools\asm-regen\ghidra-export-range.bat 080000c0 084c7637 asm\all.s.raw 0
python tools/asm-regen/inject_modes.py asm/all.s.raw asm/all.s
```

导出后 `bl FUN_080db860` 变为 `bl pack_banner_tile_copy`，提升代码可读性。
再次构建验证 byte-identical。

### Phase 4: 文档

#### ⑬ 分析报告

`doc/dev/pack-banner-static-analysis.md`：完整记录 OAM 分析、三方向结果、ROM 数据验证、调色板定位、调用链。

#### ⑭ 方法论更新

`doc/dev/locate-rom-asset-from-vram-diff.md`：新增步骤 ⑦"导出 + 目视对比验证"，记录 tile 格式误判教训。

#### ⑮ README 更新

根目录 `README.md`：构建前置步骤、数据提取表、工具脚本表、目录结构、图形资产管线。

---

## 三、产出清单

| 类型 | 文件 | 入库 |
|------|------|------|
| 导出脚本 | `tools/rom-export/export_pack_banners.py` | ✓ |
| 结构化汇编 | `data/pack-banners.s` | ✓ |
| ROM 引用 | `asm/rom.s`（拆分 incbin + .include） | ✓ |
| 反汇编代码 | `asm/all.s`（函数名更新） | ✓ |
| Ghidra 脚本 | `tools/ghidra-labeling/RenameKnownFunctions.py`（+11 条） | ✓ |
| Ghidra 脚本 | `tools/ghidra-labeling/LabelPackBanners.py`（53 label） | ✓ |
| GDB 脚本 | `doc/dev/scripts/gdb_pack_banner_*.gdb`（3 个） | ✓ |
| 分析报告 | `doc/dev/pack-banner-static-analysis.md` | ✓ |
| 方法论 | `doc/dev/locate-rom-asset-from-vram-diff.md`（+步骤⑦） | ✓ |
| 函数名登记 | `doc/dev/ghidra-function-names.md`（+11 条） | ✓ |
| 项目文档 | `README.md` | ✓ |
| tile 二进制 | `graphics/pack-banners/pack_XX_banner.bin` × 51 | ✗（导出生成） |
| 彩色预览 | `graphics/pack-banners/pack_XX_banner.png` × 51 | ✗（导出生成） |

**Git commits**: 5 个（feat×2 + refactor×2 + docs×1）

---

## 四、可复用检查清单

后续定位新资产时，按以下清单逐项打勾：

- [ ] 游戏截图 + VRAM/PALRAM/OAM dump
- [ ] OAM 解析（sprite 尺寸/色深/tile/mapping 模式）
- [ ] 方向 B/C 静态分析（选最强指纹，grep 密度 < 5）
- [ ] 方向 A 动态验证（hbreak 优先于 watchpoint，DMA 绕过问题）
- [ ] ROM 字节搜索（VRAM tile → ROM 匹配，**检查完整 block 不只看前几字节**）
- [ ] 调色板搜索（PALRAM sub-palette → ROM 匹配）
- [ ] 渲染 PNG + 截图目视对比（**拦截 tile 格式/bpp/行列序错误**）
- [ ] 导出脚本（bin + PNG + .s，指针表用 label 不用 bin）
- [ ] rom.s 拆分（前部 incbin + .include + 后部 incbin，大小校验）
- [ ] 构建 byte-identical
- [ ] Ghidra 函数重命名 + 数据 label
- [ ] 重导出 asm/all.s + 再次构建验证
- [ ] 分析报告 + 方法论更新 + README 更新
- [ ] 函数名登记表 (ghidra-function-names.md) 更新
