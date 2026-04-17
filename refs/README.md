# refs/ — 本地参考资料目录

本目录收录反汇编/分析过程中使用的外部参考资源。  
**所有子目录均不纳入版本控制**（已在 `.gitignore` 中以 `refs/*/` 整体忽略）。

---

## 子目录说明

### ygocdb/

**来源**：[ygocdb.com](https://ygocdb.com) 开放 API  
**作用**：游戏王卡牌中文数据库，用于将 ROM 中的卡牌 ID 还原为中文卡名及属性。

| 文件 | 说明 |
|------|------|
| `cards.json` | 完整卡牌数据（约 13 MB），按需下载 |
| `cards.zip.md5` | 远端压缩包的 MD5，用于增量更新判断 |

#### 字段说明

| 字段 | 含义 |
|------|------|
| `cid` | 官方数据库唯一标识符 |
| `cn_name` | YGOPro 译名（中文） |
| `sc_name` | 官方简体中文名称 |
| `md_name` | Master Duel 中文名称 |
| `nwbbs_n` | NWBBS 论坛译名 |
| `cnocg_n` | CNOCG 论坛译名 |
| `wiki_en` | Yugipedia 英文名（仅未正式发售的卡有此字段） |

#### 下载方法

```powershell
$md5Url  = "https://ygocdb.com/api/v0/cards.zip.md5"
$zipUrl  = "https://ygocdb.com/api/v0/cards.zip"
$md5File = "refs\ygocdb\cards.zip.md5"
$jsonFile = "refs\ygocdb\cards.json"

$remote = (Invoke-WebRequest $md5Url).Content.Trim().Trim('"')
$local  = if (Test-Path $md5File) { Get-Content $md5File } else { "" }

if ($remote -ne $local) {
    Invoke-WebRequest $zipUrl -OutFile "refs\ygocdb\cards.zip"
    Expand-Archive -Path "refs\ygocdb\cards.zip" -DestinationPath "refs\ygocdb\" -Force
    Remove-Item "refs\ygocdb\cards.zip"
    Set-Content $md5File $remote -Encoding UTF8 -NoNewline
    Write-Host "cards.json 已更新"
} else {
    Write-Host "cards.json 已是最新"
}
```

> MD5 端点：`https://ygocdb.com/api/v0/cards.zip.md5`  
> 建议先比对 MD5，仅有变化时才重新下载完整压缩包。

---

### agbcc/

**来源**：<https://github.com/pret/agbcc>  
**作用**：GBA 专用 C 编译器（基于 GCC 2.95），用于将 C 代码重新编译为与原版 ROM 二进制完全一致的目标代码。在逆向工程中作为"回归编译"的参考工具链，可验证反汇编得到的 C 代码能否产生相同的机器码。

---

### pokeruby/

**来源**：<https://github.com/pret/pokeruby>  
**作用**：《口袋妖怪 红宝石》GBA 完整反汇编项目，与本项目使用相同的开发工具链（devkitARM / agbcc）和项目结构约定。作为同平台同时代 GBA 游戏反汇编的参考范本，涵盖：
- 汇编代码组织方式
- GBA 硬件寄存器用法惯例
- Makefile / 链接脚本写法
- 图形/音频数据格式

---

### WCT2006BATTLECITY/

**来源**：本地收集的《游戏王 世界锦标赛 2006》Battle City 模式相关素材  
**作用**：包含角色立绘、卡组配置、场地贴图、补丁文件等游戏资产，用于对比分析 EX2006 与 WCT2006 两作之间的共用数据结构和差异，辅助逆向过程中的数据表识别。

---

### awesome-gbadev/

**来源**：<https://github.com/gbadev-org/awesome-gbadev>  
**作用**：GBA 开发资源精选列表，收录了工具链、文档、教程、示例项目等，作为反汇编和 ROM hack 工作的参考索引。

---

### mgba/

**来源**：<https://github.com/mgba-emu/mgba>  
**作用**：mGBA 模拟器源码，主要参考 GDB stub 实现（`src/debugger/gdb-stub.c`），用于理解模拟器与调试器之间的 RSP 协议交互细节，以及逆向调试工作流的搭建。

---

### datacrystal-um2006/

**来源**：[TCRF Data Crystal](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006)  
**作用**：Data Crystal 社区针对本游戏整理的 ROM/RAM 地图、文本编码表与杂项笔记，含若干段精简反汇编（`internal_card_id` → `card_id` 映射、卡名指针加载、字符集分支等）。

| 文件 | 内容摘要 |
|------|---------|
| `rom-map.md` | 7 段 ARM Thumb 反汇编 + Cards IDs / Card name pointers / Cards names 三个数据表起始地址 |
| `ram-map.md` | EWRAM (语言/DP/谜题进度/玩家名/胜场/LP/Banlist 缓冲) + IWRAM (PRNG/帧计数器) |
| `text-table.md` | 文本编码 (ASCII + 拉丁扩展，含 `0x5C=¥`、`0x91/0x92` 闪电符号) |
| `notes.md` | Player Icons ID 表（仅前 16 项；上游页面本身不完整） |

**用途**：
- `rom-map.md` 揭示 `0x15F3A5C` 是 *卡名指针表*（已据此拆出 `data/card-name-pointer-table.s`），`0x15B7CCC` 是 *internal_card_id → card_id 反向映射表*（已据此拆出 `data/cards-ids-array.s`）。
- `ram-map.md` 提供的 RAM 地址已收录到 `constants/ewram.inc` / `constants/iwram.inc`，未来反汇编中可用符号常量替代裸 `.word`。
- `text-table.md` 与 `data/font.s` / `game-strings-*.s` 互证编码假设。

抓取时间：2026-04-17。Data Crystal 是 wiki 内容，可能持续更新；如发现新增条目，可重新跑 WebFetch 同步。

---

## 注意事项

- 首次克隆仓库后，以上子目录均为空（不存在）。根据实际需要手动下载或迁移。
- `refs/README.md` 本身是版本控制的唯一文件，其余内容全部在本地保留。
