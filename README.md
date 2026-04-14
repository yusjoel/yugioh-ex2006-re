# Yu-Gi-Oh! Ultimate Masters: WCT 2006 反汇编项目

《Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006》（GBA，ROM 编号 2343，游戏代码 `BY7E`）的反汇编与数据提取项目。
目标是将原始 ROM 逐步分解为结构清晰的汇编源文件，最终能重新汇编出与原始 ROM **完全一致**（byte-identical）的二进制文件。

## 环境要求

- **devkitARM**（包含 `as`、`ld`、`objcopy`）  
  安装路径需在 `PATH` 中，或修改 `build.bat` 指向实际路径  
  推荐安装目录：`<devkitPro安装目录>\devkitARM\arm-none-eabi\bin\`
- **原始 ROM**：将未修改的原版 ROM 放置于 `roms/2343.gba`

## 快速开始

> ⚠️ **构建前置步骤**：`asm/rom.s` 引用了 `graphics/opponents/*.bin`（tilemap/palette 二进制），
> 这些文件**不纳入版本控制**，需先从 ROM 导出：
>
> ```bat
> python tools/export_gfx.py   @ 从 roms/2343.gba 导出图形二进制和 PNG 预览
> build.bat                    @ 汇编、链接并生成 output/2343.gba
> ```

```bat
build.bat    @ 汇编、链接并生成 output/2343.gba
clean.bat    @ 清理编译产物
```

构建流水线：`asm/rom.s` → (as) → `output/rom.o` → (ld) → `output/2343.elf` → (objcopy) → `output/2343.gba`

## 目录结构

```
.
├── asm/
│   ├── rom.s             # 主入口文件，串联所有数据段
│   ├── rom_header.s      # GBA ROM 头部（0x000–0x0BF）
│   ├── crt0.s            # 启动代码（0x0C0–0x0FF）
│   └── all.s             # 前 16MB 反汇编代码
├── data/                 # 已结构化的数据区（.s 格式，含注释）
│   ├── opponent-card-values.s  # 27 个对手卡值块（ROM 0x1E58D0E）
│   ├── banlists.s              # 8 个版本禁卡表，487 条目（ROM 0x1E5EF30）
│   ├── starter-deck.s          # 初始卡组，50 张（ROM 0x1E5F884）
│   ├── struct-decks.s          # 6 套预组 + 指针表（ROM 0x1E5FA58）
│   └── opponent-decks.s        # 25 套对手卡组（ROM 0x1E6468E）
├── graphics/             # 图形资产（不含于仓库，由 tools/export_gfx.py 生成）
│   ├── opponents/        # 对手大图 PNG + tilemap.bin + palette_copy1.bin
│   └── icons/            # 对手小图标 PNG
├── tools/
│   └── export_gfx.py     # ROM → PNG / tilemap.bin / palette.bin 导出脚本
├── include/
│   └── macros.inc        # 汇编宏：deck_entry、banlist_entry、deck_card
├── constants/
│   └── gba_constants.inc # GBA 硬件寄存器常量
├── doc/                  # 研究文档（来自 Google Sheets，转存为 Markdown）
│   ├── um06-deck-modification-tool/   # 卡组修改工具数据
│   └── um06-romhacking-resource/      # ROM 破解资源参考
├── roms/                 # 原始 ROM（不含于仓库）
├── output/               # 编译产物（不含于仓库）
├── build.bat             # 构建脚本
├── clean.bat             # 清理脚本
└── PLAN.md               # 数据汇编化进度计划
```

## 已完成的数据提取

以下数据区已从 `.incbin` 替换为带注释的可读汇编代码，每条目包含卡牌名称和密码：

| 数据区 | ROM 偏移 | 大小 | 说明 |
|--------|---------|------|------|
| 对手卡值块 | `0x1E58D0E` | 864 B | 27 个对手的卡牌实力值 + 内部文件路径 |
| 禁卡表（8版本）| `0x1E5EF30` | 1948 B | Sept03/Sept04/March05/Sept05 等 |
| 初始卡组 | `0x1E5F884` | 102 B | 50 张牌 |
| 预组（6套）| `0x1E5FA58` | 812 B | Dragon's Roar、Zombie Madness 等 |
| 对手卡组（25套）| `0x1E6468E` | 5048 B | Kuriboh～Raviel 全部对手 |

### 数据格式示例

```asm
@ 预组（真红眼黑龙 ×1）
deck_entry 4088, 1    @ Red-Eyes B. Dragon (密码: 74677422)

@ 禁卡表（限制 1 张）
banlist_entry 4088, 1    @ Red-Eyes B. Dragon (密码: 74677422)

@ 对手/初始卡组
deck_card 4088    @ Red-Eyes B. Dragon (密码: 74677422)
```

宏在 `include/macros.inc` 中定义，`so_code` 使用十进制整数（如 `4088` = `0x0FF8`），编译时自动计算编码。

## 图形资产管线

对手图形（27 个对手的大图壁纸和小图标）采用以下管线管理：

```
roms/2343.gba
  └─ tools/export_gfx.py ──► graphics/opponents/
  │                              palette_copy1.bin   调色板块（7776 B）
  │                              <name>_top_tilemap.bin   (1200 B × 27)
  │                              <name>_bottom_tilemap.bin
  │                              <name>_top.png      渲染合成图（240×160，仅预览）
  │                              <name>_bottom.png
  │                          graphics/icons/
  │                              <name>_icon.png     图标（24×24）
  └─ build.bat ──► output/2343.gba
      （通过 asm/rom.s 中的 .incbin 引用 graphics/opponents/*.bin）
```

`graphics/` 目录下所有文件均**不纳入版本控制**，须在构建前运行导出脚本生成。

### 图形数据 ROM 布局

| ROM 偏移 | 内容 | 大小 |
|---------|------|------|
| `0x1B101AC` | 调色板块（Copy 1 & 2，内容相同） | 7776 B |
| `0x1B1200C` | Top 图块（4bpp，27 个对手） | 221184 B |
| `0x1B4800C` | Top Tilemap（27 × 1200 B） | 32400 B |
| `0x1B51CFC` | Bottom 图块（4bpp，27 个对手） | 221184 B |
| `0x1B87CFC` | Bottom Tilemap（27 × 1200 B） | 32400 B |



- GBA ROM 基址：`0x08000000`，入口点：`0x080000C0`
- 指令集：ARM（32 位）与 THUMB（16 位）混合，游戏代码大部分为 THUMB
- ROM 大小：`0x1FFFF00` 字节（33,554,176 B），构建时必须精确
- `roms/2343.gba` 同时作为数据源和校验基准

---

## 调试工具链

项目已完成调试工具链验证（P0），可通过以下两种方式对运行中的游戏进行动态调试。

### mGBA MCP（截图 / 内存读取 / Lua 注入）

通过 [mGBA MCP](https://github.com/souldzin/mGBA-http) 提供的 MCP 工具直接控制 mGBA。

**启动**：
```ps1
# 启动 mGBA 并加载存档（工具位于 tools/）
pwsh -File tools\start-mgba-gdb-ss1.ps1
```

**已验证工具**（详见 `doc/dev/p0-3-mgba-mcp-feature-validation.md`）：

| 工具 | 功能 |
|------|------|
| `mgba_live_start` | 启动 mGBA 会话 |
| `mgba_live_export_screenshot` | 截图 |
| `mgba_live_input_tap` | 模拟按键 |
| `mgba_live_run_lua` | 注入 Lua 脚本 |
| `mgba_live_read_memory` | 读取指定地址 |
| `mgba_live_read_range` | 读取内存范围 |
| `mgba_live_dump_oam` | 转储 OAM 精灵表 |

### GDB MCP（断点 / 寄存器 / 单步执行）

通过 [GDB MCP](https://github.com/pansila/gdb-mcp) 工具，以 MI 协议驱动 GDB 连接 mGBA GDB stub。

**启动顺序**：
```ps1
# 1. 启动 mGBA（带 GDB stub，端口 2345）
pwsh -File tools\start-mgba-gdb-ss1.ps1
# 2. 等待 stub 就绪（约 9 秒）
pwsh -File tools\wait-mgba-ready.ps1
# 3. 通过 MCP 工具连接（在 AI 助手中调用）
# gdb_init(gdbPath: "tools/arm-none-eabi-gdb.exe")
# gdb_connect(target: "localhost:2345")
```

> ⚠️ 必须使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2），
> `devkitPro` 自带的 GDB 14.1 与 mGBA stub 不兼容。
> 调用 `gdb_init` 时**不要**使用 `architecture` 参数。

> ⚠️ mGBA GDB stub 为一次性连接：GDB 断开后 stub 永久关闭，每次调试需重启 mGBA。

**已验证工具**（详见 `doc/dev/p0-5-gdb-mcp-integration.md`）：

| 工具 | 功能 |
|------|------|
| `gdb_init` / `gdb_connect` / `gdb_disconnect` | 连接管理 |
| `gdb_set_breakpoint` | 设置断点（支持条件断点） |
| `gdb_list_breakpoints` / `gdb_delete_breakpoint` | 断点管理 |
| `gdb_continue` / `gdb_interrupt` | 执行控制 |
| `gdb_evaluate_expression` | 表达式求值（可读取内存/寄存器） |
| `gdb_command` | 直接执行 GDB MI 命令 |

**已知限制**：mGBA THUMB 代码不支持栈回溯（`gdb_list_frames` 失败）；`gdb_read_memory` 存在解析 bug，可用 `gdb_evaluate_expression` 代替。

### 纯 GDB 脚本方式

适合已知流程的批处理场景（如固定 watchpoint 监听），详见 `doc/dev/scripts/`：

```ps1
tools\arm-none-eabi-gdb.exe --batch -x doc\dev\scripts\gdb_dma_watch.gdb
```

---

## 参考文档

项目 `doc/` 目录下保存了以下研究文档（原始 Google Sheets，转存为 Markdown）：

- **[UM06 Deck Modification Tool 1.0](doc/um06-deck-modification-tool/toc.md)**  
  含完整卡牌数据库（4072 条）、卡组地址表、编码工具
- **[UM06 Romhacking Resource Ver 2.0](doc/um06-romhacking-resource/toc.md)**  
  含图形地址、禁卡表解析、卡组修改方法等 10 个 Sheet

---

## 致谢

感谢 **Scrub Busted**（[@scrubbusted](https://www.youtube.com/@scrubbusted)）对《游戏王 EX2006》ROM 破解研究的开创性贡献，其制作的教程视频和共享文档是本项目数据分析的重要基础。

**教程视频系列（Ultimate Masters ROMHACKING TUTORIAL）：**

| # | 标题 | 链接 |
|---|------|------|
| Part 1 | Graphics - Custom Field Playmat, Custom Palettes | [YouTube](https://www.youtube.com/watch?v=BbPcN3r_QIs) |
| Part 2 | Graphics - Deck Images, 64 Color Palettes, 8bpp | [YouTube](https://www.youtube.com/watch?v=_l0UY5goXLM) |
| Part 3 | MODIFYING DECKS - Starter, Structure & Opponents | [YouTube](https://www.youtube.com/watch?v=KsobsJKv4K8) |
| Part 4 | Tilemap Studio Tutorial - Modify Coin Flip Backgrounds | [YouTube](https://www.youtube.com/watch?v=uLpnGkV1lXs) |

**参考文档（Google Sheets）：**

- [UM06 Deck Modification Tool 1.0](https://docs.google.com/spreadsheets/d/1dXa8EyyL2ozM04TpZb_yAsYO7A98CfKIZacchXT2US8/edit)
- [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)
