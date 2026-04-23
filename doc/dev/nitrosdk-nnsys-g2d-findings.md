# ROM 内嵌 NitroSDK / NNS g2d 库识别报告

调查日期：2026-04-17
ROM：`roms/2343.gba`（33,554,432 B / 0x2000000）

---

## 结论

本 GBA ROM 在其构建时**静态链接了 NitroSDK 的 OAM/FX 子系统，以及建立在 NitroSDK 之上的 NNS g2d（Nintendo Nitro System Graphics 2D）库**。证据来自 `__FILE__` 宏被 assertion 展开后嵌入 ROM 的源文件路径和符号字面量。

这意味着：

1. 本项目涉及的卡牌动画/sprite/调色板资源使用 **NDS 标准容器格式**（NCGR/NCER/NANR/NCLR/NMAR），而非任意自定义二进制
2. 我们一直没定位的 P2-palette（卡列表小图 OBJ 256 色调色板）极可能是某个 `.LZnclr` 文件
3. `file-paths.s` 里 64 个 `.LZn*` 扩展名文件对应明确的数据格式契约
4. ROM 代码里存在一批**可命名的公开符号**，过去识别为 `FUN_xxx` 的函数有相当比例属于 NitroSDK/NNS 公共 API

---

## 证据 1：assertion 字符串区域

`0x1E38EB4 – 0x1E584EE`（约 125 KB）集中分布以下 assert 引用的源文件路径：

**NitroSDK 头文件引用（`__FILE__`）**
- `inc/nitro/fx_mtx22.h`
- `inc/nitro/g2_oam.h`

**NNS（Nitro System）头文件引用**
- `inc/nnsys/g2d/fmt/g2d_Anim_data.h`
- `inc/nnsys/g2d/fmt/g2d_Cell_data.h`
- `inc/nnsys/g2d/g2d_Animation_inline.h`
- `inc/nnsys/g2d/g2d_CellAnimation.h`
- `inc/nnsys/g2d/g2d_Image.h`
- `inc/nnsys/g2d/g2d_SRTControl.h`
- `inc/nnsys/g2d/load/g2d_NAN_load.h`

**NNS 源文件引用（说明这些 `.c` 被 Konami 就地编译进了 GBA 目标）**
- `nnsys/g2d/fx_mtx22.c`
- `nnsys/g2d/g2d_Animation.c`
- `nnsys/g2d/g2d_CellAnimation.c`
- `nnsys/g2d/g2d_Image.c`
- `nnsys/g2d/g2d_Load.c`
- `nnsys/g2d/g2d_NAN_load.c`
- `nnsys/g2d/g2d_NCG_load.c`
- `nnsys/g2d/g2d_NCL_load.c`
- `nnsys/g2d/g2d_NOB_load.c`
- `nnsys/g2d/g2d_SRTControl.c`

**游戏自身源目录**（非 SDK，Konami 自写）
- `GL/GL_Common.c`、`GL/GL_File.c`、`GL/GL_Oam.c`、`GL/GL_Scrollbar.c`、`GL/IG2D_Main.c`、`GL/ISD_Draw.c`、`GL/PRH_Main.c`
- `Exodia/EXO_main.c`、`NameInput/Name_main.c`、`PassInput/Pass_main.c`、`Shuen/SHU_main.c`、`Vija/VIJ_main.c`、`titleEx/TitleEx_main.c`
- `system/s_opdobj.c`

> `GL/` 推测是 "Graphics Layer"（游戏自封装的 OAM/BG 辅助层，调用 NNS g2d）；`Shuen` = 日文"終焉"（终焉）、`Vija` = 相关的融合召唤 demo。

---

## 证据 2：NNS 符号字面量

assertion 表达式里直接出现的 NNS API 符号（15 个 distinct）：

| 符号 | 类别 |
|------|------|
| `NNS_G2dGetAnimSequenceAnimType` | 函数 |
| `NNS_G2dMakeVersionData` | 函数 |
| `NNSi_G2dGetCharacterFmtType` | 内部函数（`NNSi_` 前缀） |
| `NNSi_G2dIsBinFileSignatureValid` | 内部函数 |
| `NNSi_G2dIsBinFileVersionValid` | 内部函数 |
| `NNSi_G2dIsCharacterVramTransfered` | 内部函数 |
| `NNS_G2D_1D_MAPPING_CHAR_SIZE` | 常量 |
| `NNS_G2D_ANIMATIONTYPE_CELL` | enum 值 |
| `NNS_G2D_ANMCALLBACKTYPE_SPEC_FRM` | enum 值 |
| `NNS_G2D_CHARACTER_FMT_CHAR` | enum 值 |
| `NNS_G2D_INVALID_CELL_TRANSFER_STATE_HANDLE` | sentinel |
| `NNS_G2D_SRTCONTROLTYPE_SRT` | enum 值 |
| `NNS_G2D_VRAM_TYPE_2DMAIN` | enum 值 |
| `NNS_G2D_VRAM_TYPE_2DSUB` | enum 值（注：GBA 无 2DSUB，但常量定义仍被编入） |
| `NNS_G2D_VRAM_TYPE_3DMAIN` | enum 值（同上） |

NitroSDK 侧的 `GX_OAM_*` 宏也大量出现在 assert 条件表达式中（OAM SHAPE/MODE/COLORMODE/EFFECT 枚举）。

---

## 证据 3：NitroSDK 资源格式文件清单（64 个）

`data/file-paths.s` 里按扩展名归类：

| 扩展名 | 数量 | 含义（NDS 标准格式） |
|---|---|---|
| `.LZncgr` | 18 | NDS Character Graphic Resource（tile 图块），LZ77 压缩 |
| `.LZnclr` | 18 | NDS Color Resource（调色板），LZ77 压缩 |
| `.LZnanr` | 14 | NDS Animation Resource（帧动画），LZ77 压缩 |
| `.LZncer` | 14 | NDS Cell Resource（sprite 组合定义），LZ77 压缩 |

按模块分组：

| 模块 | 文件前缀 | 推测用途 |
|------|----------|----------|
| `demo/exodia/` | `exodia01_obj`, `exodia02_obj` | Exodia 召唤胜利演出 |
| `demo/shuen/` | `shuen_obj` | "終焉"相关（Final Countdown？或 Destiny Board 终局？） |
| `demo/vija/` | `wija_obj_all`, `wija_obj_allUS` | 某融合/召唤演出，日版 + US 版双套 |
| `name_input/` | `name_o_01` | 玩家名输入界面 |
| `pass_input/` | `pass_o_01` | 密码输入界面 |
| `titleEx/` | `title_obj_{e,f,g,i,j,s}` | 标题画面 6 语言（EN/FR/DE/IT/JP/ES） |

**LZ77 压缩头约定**：GBA BIOS `SWI 0x11/0x12`（`LZ77UnCompReadNormalWrite{8,16}bit`）；文件开头 `0x10 [size:24]`，解压后首 4 字节为 ASCII magic（NCGR/NCER/NANR/NCLR）。

ROM 里未压缩的容器 magic 也出现在 `0x1E4C7AA – 0x1E4E1E6` 附近（NANR/NMAR/NCGR/NCLR/NCER 各一处），可能是默认 asset 或解压后驻留区。

---

## 证据 4：未压缩 magic byte 定位（BE ASCII 搜索）

| Magic | 首次出现 ROM 偏移 |
|-------|-------------------|
| `NANR` | `0x1E4C7AA` |
| `NMAR` | `0x1E4C832` |
| `NCGR` | `0x1E4D00A` |
| `NCLR` | `0x1E4D99D` |
| `NCER` | `0x1E4E1E6` |

全部集中在 `0x1E4C7AA – 0x1E4E1E6`（约 6.3 KB 窗口内），疑为某个默认/fallback 资源束。

---

## CPU 架构对齐说明

NitroSDK 官方目标是 NDS ARM946E（ARMv5TE）。本 ROM 是 GBA ROM（ARM7TDMI / ARMv4T）。证据显示 Konami 把 NitroSDK/NNS 的 C 源码**重新用 ARMv4T 目标编译**，嵌入 GBA ROM：

- ROM 使用 THUMB + ARM 混合，未见 ARMv5 独占指令（CLZ / BLX imm / SMULxy / PLD）的片段
- assertion 字符串中的 `__FILE__` 路径格式与 Metrowerks CodeWarrior（NitroSDK 官方编译器）惯例一致
- 因此，**无法用 NitroSDK 预编译库做字节级指纹匹配**；但源码级等价性成立，函数语义、调用契约、数据结构布局跨 CPU 不变

---

## 对项目的影响

### 立即可行的跟进

1. **P2-palette 问题改路径**：把 "卡列表小图 OBJ 256 色调色板未定位" 这个 pending，从 "在 ROM 里按 palette 字节模式搜索" 改为 "定位 `GL/GL_File.c` 的 filename→ROM offset 映射表，解析对应 `.LZnclr` 文件"。

2. **`GL/GL_File.c` 函数定位**：这是 Konami 自写的 FS 层，管 64 个资源的地址查表。定位它的 lookup 表地址 = 64 个资源在 ROM 中的实际偏移全部拿到。
   - 切入点：ROM 里有 `"GL/GL_File.c"` 字符串，追 XREF 找到该模块函数

3. **Ghidra 类型系统扩展**：为 `tools/ghidra-labeling/CreateCardStatsType.py` 增加：
   - `GXOamAttr`（3×u16 OAM 条目）
   - `GXCharFmt16` / `GXCharFmt256`
   - `GXBGPltt16` / `GXBGPltt256`
   - NCGR/NCER/NANR/NCLR 文件头结构体
   这些类型定义是公开的 NDS homebrew 社区知识，跨 CPU 通用。

4. **NNS 符号命名**：把 assert 里出现的 15 个 NNS 符号 + NitroSDK 公开 API 名（GX_/MI_/OS_/FX_/MTX_ 前缀）整理成命名候选池，供后续 `tools/ghidra-labeling/RenameKnownFunctions.py` 扩充使用。定位的关键线索是 **assert 字符串 XREF**：引用 `(oam) != NULL` 的函数就是操作 OAM 的 NitroSDK API。

### 不可行 / 已否定的路径

- **用 CrystalTile2 "NitroSDK 符号表搜索"**（stevexmh Ep2 方法）：该工具的指纹库是 NDS ARM9 预编译产物指纹，对本 ROM（ARMv4T）0 命中。
- **直接字节级 fingerprint**：ISA 不同，编译产物字节序列差异显著。

### 外部资源需求

- **NNS g2d 源码**不在目前持有的 NitroSDK 克隆里（那份是 NitroSDK 本体，不含 NNS 上层）。如果要彻底弄懂 `.LZncgr/.LZnclr/.LZnanr/.LZncer` 的解析细节，需另找 NNS 源。当前替代方案是参考 NDS 社区公开的格式逆向文档（GBATEK 附带、ConsoleTool、Tinke 等工具的说明）。

---

## 验证脚本备忘

扫描方法可在任何时候重跑（ROM 未变）：

```python
import re
with open('roms/2343.gba','rb') as f:
    d = f.read()

# assertion 区域里的源文件路径
for m in re.finditer(rb'inc/nitro/[A-Za-z0-9_./]+\.h', d):
    print(hex(m.start()), m.group().decode())
for m in re.finditer(rb'nnsys/g2d/[A-Za-z0-9_./]+\.[ch]', d):
    print(hex(m.start()), m.group().decode())

# NNS API 名字
for m in set(m.group() for m in re.finditer(rb'NNSi?_[A-Za-z0-9_]+', d)):
    print(m.decode())

# NCGR/NCER/NANR/NCLR/NMAR magic
for magic in [b'NCGR', b'NCER', b'NANR', b'NCLR', b'NMAR']:
    for m in re.finditer(re.escape(magic), d):
        print(magic.decode(), hex(m.start()))
        break
```
