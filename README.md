# 游戏王 EX2006 反汇编项目

《游戏王 The Sacred Cards》（GBA，ROM 编号 2343，游戏代码 `BY7E`）的反汇编与数据提取项目。  
目标是将原始 ROM 逐步分解为结构清晰的汇编源文件，最终能重新汇编出与原始 ROM **完全一致**（byte-identical）的二进制文件。

## 环境要求

- **devkitARM**（包含 `as`、`ld`、`objcopy`）  
  安装路径需在 `PATH` 中，或修改 `build.bat` 指向实际路径  
  推荐安装目录：`D:\devkitPro\devkitARM\arm-none-eabi\bin\`
- **原始 ROM**：将未修改的原版 ROM 放置于 `roms/2343.gba`

## 快速开始

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

## 技术说明

- GBA ROM 基址：`0x08000000`，入口点：`0x080000C0`
- 指令集：ARM（32 位）与 THUMB（16 位）混合，游戏代码大部分为 THUMB
- ROM 大小：`0x1FFFF00` 字节（33,554,176 B），构建时必须精确
- `roms/2343.gba` 同时作为数据源和校验基准

## 卡牌数据库（YGOCdb）

`data/cards.json` 包含完整的游戏王卡牌中文数据，来自 [ygocdb.com](https://ygocdb.com)。  
该文件体积较大（约 13 MB），不纳入版本控制，需手动下载。

### 字段说明

| 字段 | 含义 |
|------|------|
| `cid` | 官方数据库唯一标识符 |
| `cn_name` | YGOPro 译名（中文） |
| `sc_name` | 官方简体中文名称 |
| `md_name` | Master Duel 中文名称 |
| `nwbbs_n` | NWBBS 论坛译名 |
| `cnocg_n` | CNOCG 论坛译名 |
| `wiki_en` | Yugipedia 英文名（仅未正式发售的卡有此字段） |

### 下载方法

```powershell
# 1. 获取最新 MD5 校验值
$md5Url  = "https://ygocdb.com/api/v0/cards.zip.md5"
$zipUrl  = "https://ygocdb.com/api/v0/cards.zip"
$md5File = "data\cards.zip.md5"
$jsonFile = "data\cards.json"

# 2. 仅在远端有更新时重新下载
$remote = (Invoke-WebRequest $md5Url).Content.Trim().Trim('"')
$local  = if (Test-Path $md5File) { Get-Content $md5File } else { "" }

if ($remote -ne $local) {
    Invoke-WebRequest $zipUrl -OutFile "data\cards.zip"
    Expand-Archive -Path "data\cards.zip" -DestinationPath "data\" -Force
    Remove-Item "data\cards.zip"
    Set-Content $md5File $remote -Encoding UTF8 -NoNewline
    Write-Host "cards.json 已更新"
} else {
    Write-Host "cards.json 已是最新"
}
```

> MD5 端点：`https://ygocdb.com/api/v0/cards.zip.md5`  
> 建议在自动化脚本中先比对 MD5，仅有变化时才重新下载完整压缩包。

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
