# ROM 明文字符串扫描报告

扫描日期：2026-04-16
ROM：`roms/2343.gba`（33,554,432 B / 0x2000000）

## 扫描方法

- 用 ASCII 可打印范围（0x20–0x7E）扫描连续字节 ≥ 12 字符的片段
- 按内容特征分类：真实文本（含空格 + 英文单词）、文件路径、断言条件、调试格式串等
- 排除已提取区域（card-names / card-descriptions / card-stats / deck-strings / game-strings）
- 聚类：相邻 4 KB 内的字符串归为一组

## 已提取区域（基线）

| 数据区 | ROM 范围 | 大小 | data/*.s |
|--------|---------|------|----------|
| 卡牌名称（6 语言） | 0x015BB5AC–0x015F3A5B | 377,711 B | card-names.s |
| 卡牌描述文本（39 张） | 0x01800000–0x018169B5 | 92,598 B | card-descriptions.s |
| 卡牌属性数据 | 0x018169B6–0x01832601 | 113,740 B | card-stats.s |
| 卡组名称字符串 | 0x01DBF01A–0x01DFC852 | ~223 KB | deck-strings.s |
| 游戏界面文本（5 语言） | 0x01DC4620–0x01DFF9D1 | 242,610 B | game-strings.s |

---

## 未提取的大段明文区域

### 1. 卡牌效果描述全文（最大区域）

| 项目 | 值 |
|------|-----|
| **ROM 范围** | 0x01600000–0x017FFFFF |
| **跨度** | 2,097,152 B（2 MB） |
| **ASCII 占比** | ~84%（大量多语言文本） |
| **null 终止字符串数** | ~12,084 条（≥10 字符） |
| **总文本字节** | ~2,078,000 B |
| **类别** | **CARD_TEXT** — 所有卡牌的风味文本/效果描述（EN/DE/FR/IT/ES/JP） |

这是 ROM 中**最大的未结构化明文区域**。已提取的 `card-descriptions.s`（0x01800000+）仅覆盖 39 张卡的描述，而此区域包含全部 ~2000+ 张卡的 6 语言效果文本。

**示例**：
```
0x015FFF6C [150B] This legendary dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.
0x01600004 [200B] Dieser legendäre Drache ist eine mächtige Zerstörungsmaschine... (DE)
0x016000CE [157B] Ce dragon légendaire est un puissant moteur de destruction... (FR)
0x0160016C [179B] Questo drago leggendario è una potente macchina distruttrice... (IT)
0x01600220 [173B] Este legendario dragón es una poderosa máquina de destrucción... (ES)
0x016002CE  [56B] (JP — 自定义编码，非 ASCII)
```

**前导间隙** 0x015F3A5C–0x015FFFFF（~50 KB）：含偏移量表（小端序递增整数），可能是每张卡描述的偏移量索引。

### 2. SDK 断言/调试字符串（区域 A）

| 项目 | 值 |
|------|-----|
| **ROM 范围** | 0x01E491FC–0x01E59C24 |
| **跨度** | ~68 KB |
| **有意义字符串** | 883 条 |
| **类别** | **SDK_ASSERT / DEBUG** |

内含 Nitro SDK（NNS — Nintendo Nitro System）的断言条件、源文件路径和调试格式字符串。

**子分类统计**：
- 断言条件：546 条 — `(oam) != NULL`、`(priority) >= (0) && (priority) <= (3)` 等
- SDK 源文件路径：306 条 — `inc/nitro/g2_oam.h`、`nnsys/g2d/g2d_Animation.c` 等
- 调试格式串：3 条 — `Chain Run:: iPlayer:%d, iLocate:%d, iNum:%d` 等

**包含的游戏源文件路径**（极有价值的逆向线索）：
```
Exodia/EXO_main.c
GL/GL_Common.c
GL/GL_File.c
GL/GL_Oam.c
GL/GL_Scrollbar.c
GL/IG2D_Main.c
GL/ISD_Draw.c
GL/PRH_Main.c
NameInput/Name_main.c
PassInput/Pass_main.c
Shuen/SHU_main.c
Vija/VIJ_main.c
BASICSIO (通信模块)
OBJANIME (OBJ动画模块)
```

### 3. SDK 断言/调试字符串（区域 B）

| 项目 | 值 |
|------|-----|
| **ROM 范围** | 0x01E36595–0x01E3EF44 |
| **跨度** | ~35 KB |
| **SDK 相关字符串** | 161 条 |
| **类别** | **SDK_ASSERT / DEBUG** |

与区域 A 结构相同，也是多个编译单元各自内联的 NNS SDK 断言。同样包含游戏模块源文件路径：
```
Exodia/EXO_main.c（重复出现）
GL/GL_Common.c / GL_File.c / GL_Oam.c / GL_Scrollbar.c
GL/IG2D_Main.c / ISD_Draw.c / PRH_Main.c
NameInput/Name_main.c
PassInput/Pass_main.c
Shuen/SHU_main.c
Vija/VIJ_main.c
```

### 4. 内部文件路径表

| 项目 | 值 |
|------|-----|
| **ROM 范围** | 0x01E6118C–0x01E63BE6 |
| **跨度** | ~11 KB |
| **总字符串** | 339 条（238 个唯一路径） |
| **类别** | **FILE_PATHS** |

游戏使用的内部文件系统路径（`.ydc` = 卡组文件，`.LZncgr/.LZnclr/.LZnscr` = 压缩图形资源）。

**卡组文件路径**（按等级分组）：
```
deck/LV1_kuriboh.ydc, LV1_pikeru.ydc, LV1_sukego.ydc, LV1_waito.ydc, LV1_watapon.ydc
deck/LV2_denti.ydc, LV2_kaeru.ydc, LV2_kingG.ydc, LV2_kingG2.ydc, LV2_ojama.ydc, LV2_waterD.ydc
deck/LV3_RedEyes.ydc, LV3_daidaros.ydc, LV3_flame.ydc, LV3_heriosu.ydc, LV3_vamp.ydc
deck/LV4_Ehero.ydc, LV4_ankokukai.ydc, LV4_exodo.ydc, LV4_gilfo.ydc, LV4_kuromadou.ydc
deck/LV5_cyber.ydc, LV5_gadget.ydc, LV5_horus.ydc, LV5_nephthys.ydc, LV5_ravieru.ydc
deck/SD0_STARTER.ydc ~ SD5_*.ydc（预组）
deck/limit_000.ydc ~ limit_041.ydc（禁卡表）
```

**图形资源路径**：
```
titleEx/title_obj_s.LZncgr
titleEx/title_obj_s.LZnclr
（等，完整列表待深入提取）
```

### 5. 存档格式定义字符串

| 项目 | 值 |
|------|-----|
| **ROM 范围** | 0x01EB90D8–0x01EC33C3 |
| **跨度** | ~42 KB |
| **字符串数** | 1,565 条 |
| **类别** | **SAVE_FORMAT** |

决斗题目（DUEL QUESTION）的存档模板，包含完整的游戏状态序列化格式定义。

**示例**：
```
[DUEL QUESTION]
Phase=MAIN1
[Player0]
PlayerLP0=1000
CardInGame0_001=6603
CardInGame0_001_Face=1
CardInGame0_001_Turn=0
...
CardInDeck1_004=5811
CardInGrave1=0
CardInExclude1=0
```

对理解游戏存档格式和决斗状态机非常有价值。

---

## 总结

| # | 区域 | ROM 范围 | 大小 | 类别 | 结构化价值 |
|---|------|---------|------|------|-----------|
| **1** | 卡牌效果全文 | 0x01600000–0x017FFFFF | **2 MB** | CARD_TEXT | ★★★ 最大未结构化文本区域 |
| **2** | SDK 断言 A | 0x01E491FC–0x01E59C24 | 68 KB | SDK_ASSERT | ★★ 含游戏源码路径 |
| **3** | SDK 断言 B | 0x01E36595–0x01E3EF44 | 35 KB | SDK_ASSERT | ★★ 含游戏源码路径 |
| **4** | 内部文件路径 | 0x01E6118C–0x01E63BE6 | 11 KB | FILE_PATHS | ★★ 含卡组/资源路径 |
| **5** | 存档格式模板 | 0x01EB90D8–0x01EC33C3 | 42 KB | SAVE_FORMAT | ★★ 存档格式参考 |

**其余小集群**（如 0x004BFC94、0x00269C9F 等）多为图形 tile 数据碰巧落入 ASCII 范围，不是真正的文本。

### 优先结构化建议

1. **卡牌效果全文**（0x01600000–0x017FFFFF）：2 MB 的多语言卡牌描述文本，是下一阶段最大的结构化目标。前方 0x015F3A5C 起的偏移量表可能是索引。
2. **SDK 断言字符串**：对函数命名和代码理解有极高参考价值（可提取所有 `*.c` 路径用于 Ghidra 标注），但结构化优先级低于游戏数据。
3. **文件路径表**和**存档格式**：体量小但信息密度高，可快速结构化。
