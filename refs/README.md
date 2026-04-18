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

### yugioh-card-search/

**来源**：<https://github.com/ryosbsk/yugioh-card-search>
**作用**：日文社区开发的 EX2006 网页版卡牌检索工具，含约 2,000 张卡的**日文名 + 所属卡包**。

| 文件 | 内容 |
|------|------|
| `data/card_master.csv` | 卡片主表：`#,种,カード名,パック,...` (按五十音排序) |
| `data/pack_master.csv` | 卡包主表：`#,パック名,出现内容,获取难易度` |
| `data/query_results.csv` | 按 pack 拆分的查询结果（含每包卡的指针） |
| `script.js` / `index.html` | 检索逻辑 + UI |

**用途**：
- **XX 语言编码研究**：`data/card-names.s` 的 `lang=0` 槽（XX）是变长自定义编码（6-32 字节），实测特征：
  - 总是**偶数长度** → 每字符 2 字节定长
  - 高字节集中在 `0xF0`–`0xFF`（最常见 `0xF1`/`0xF2`/`0xF0`）
  - 低字节散布在 `0x80`–`0xFF`
  - 字节对数 ≈ JP 卡名字符数（按汉字/假名/中点 1 字符 = 2 字节统计；不是按"读音假名"展开）
  - 例：Blue-Eyes 青眼の白龍 (5 字) → `f8 f7 f4 8c f1 a9 fb d9 fe 91` (10B = 5 pairs) ✓
  - 例：Mystical Elf ホーリー・エルフ (8 字含中点) → `f2 89 f0 8b f2 98 f0 8b f0 84 f1 d6 f2 99 f2 83` (16B = 8 pairs) ✓
- **对照数据**：本仓库 CSV 按**五十音排序**（青眼の白龍 在 #0064 而非 #0001），可与 ROM XX 排序对照验证假说。
- **日文名 → card_id 映射**：CSV `#` 是 CSV 内部序号（按五十音）非 ROM `card_id`；需要建立两表的对应关系才能用作日文卡名补全。

抓取时间：2026-04-17。本目录已加入 `.gitignore`（与其他 repo 镜像一致），不入库。

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

### poptracker-ygo06/

**来源**：<https://github.com/Rensen3/poptracker-ygo06>
**作用**：Archipelago randomizer 的 PopTracker 进度追踪包（Lua + JSON）。**不含 ROM 偏移、不含 RAM 地址**——autotracking 完全走 AP 网络协议，不读 GBA 内存。

对本项目（数据结构化/byte-identical 反汇编）直接帮助有限；**数据层面的内容我们都已从 ROM 拆出**：
- 2080 条英文卡名 → 已有 `card-name-pointer-table.s` + `card-effect-text.s`
- 45 个卡包内容 → 已有 `pack-card-lists.s`
- 25 套对手卡组 → 已有 `opponent-decks.s` / `opponent-card-values.s`

**未来逆向游戏机制时的参考价值**：
- `scripts/autotracking/card_amount.lua`：45 种 Duelist Bonus 的触发条件 + 奖励配额 + 所需卡 archetype（Exodia Finish / Destiny Board Finish / Yata-Lock / Konami Bonus=5730 LP 等），属于**玩法规则文档**，不在 ROM 任何显式表中
- `items/campaign_opponents.jsonc` + `images/campaign_opponents/*.png`：Tier×Column 战役网格 → 25 个对手角色名的映射（Tier1Col1=Kuriboh ... Tier5Col5=Cyber End Dragon），可反查我们 `opponent-decks.s` 里对手出现在战役菜单的哪个位置
- `locations/challenges.jsonc` + `location_mapping.lua`：LD01–41 + TD01–50 共 91 个挑战的**官方英文标题**（"LD23 Refer to Mar 05 Banlist"、"TD37 Uria, Lord of Searing Flames"），可用于反向定位 ROM 中挑战描述字符串
- `scripts/create_cards.lua`：关键卡 → `card_id` 对照（Exodia=21、Dark Magician=37、Raviel=2014、Uria=2012、Hamon=2013 等），可作为 ground truth 验证我们 `card_id` 索引基准
- `items/boosterpacks.jsonc`：45 个卡包的官方大写命名，可回填 `pack-card-lists.s` 注释

**Archipelago 侧**：独立的 ygo06 AP world + BizHawk Lua 连接器（不在此仓库）才真正读写 GBA RAM——如果将来需要 RAM 地址/写回协议，应去 Archipelago ygo06 world 仓库捡连接器脚本。

抓取时间：2026-04-17。

---

## 注意事项

- 首次克隆仓库后，以上子目录均为空（不存在）。根据实际需要手动下载或迁移。
- `refs/README.md` 本身是版本控制的唯一文件，其余内容全部在本地保留。
