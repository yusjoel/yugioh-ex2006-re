# 游戏 UI 文本表 (game-strings)

游戏 UI 文本（提示、菜单、SD/OPP 名等）存储为 **6 lang × 1642 logical entries** 的统一表，由
**master pointer table** 索引。

---

## 一、整体结构

| 项目 | 值 |
|---|---|
| Master pointer table 起点 | `0x08000F40` |
| Master 表大小 | 1642 行 × 24 B = 39408 B |
| Lang 顺序 (slot 内) | `[JA, EN, DE, FR, IT, ES]`，每 lang 4 B offset |
| STRING_TABLE_BASE (offset 基址) | `0x09DB9C10` (= JA 区起点) |
| 字符串区段范围 | `0x09DB9C10 ~ 0x09DFF9D2` (286,146 B) |

每行 `master[i]` 描述同一逻辑 entry 在 6 lang 下的字节地址：
```
entry_addr_in_lang(i, lang) = STRING_TABLE_BASE + master[i].offset[lang]
```

代码引用：`0x08000F40` 在 ROM 字面量池 **101 hits**，`0x09DB9C10` **99 hits**。

---

## 二、6 lang 区段

| Lang | 起点 | 大小 (B) | 非空 entry 数 | Leading pad |
|---|---|---|---|---|
| JA | `0x09DB9C10` | 43,536 | 1597 (= 1588 master + 9 JA-only) | 0 |
| EN | `0x09DC4620` | 44,625 | 1564 | 0 |
| DE | `0x09DCF471` | 50,029 | 1560 | 19 |
| FR | `0x09DDB7DE` | 50,393 | 1560 | 20 |
| IT | `0x09DE7CB7` | 49,071 | 1560 | 19 |
| ES | `0x09DF3C66` | 48,492 | 1560 | 20 |

各 lang 的 ROM 字节顺序与 master idx 顺序严格一致（每 lang ptr 在 row 0..1641 单调递增）。

**编码**：
- JA: 自定义 2B JA + 1B ASCII control。`b >= 0xF0` → 2B pair (idx = `(b & 0xF) << 7 | (lo & 0x7F)`)，`b < 0xF0` → 1B raw (含 `@N` 色码)
- 5 lang: CP1252 (Latin-1 + extended)

---

## 三、SD / OPP 槽

7 SD + 25 OPP = 32 命名 entry，是 master 表的特定 row：

| Slot | Master rows | 历史 "table" 视图 (无效) |
|---|---|---|
| SD[0..6] | 655..661 | `0x08004CAC`, stride 24, 顺序 `[EN,DE,FR,IT,ES,JA]` |
| OPP[0..24] | 1217..1241 | `0x0800815C`, stride 24, 同上 |

**⚠ 历史"SD table"视图错位 1 槽 (JA col 错位)**：
该视图把 `master[k] EN..ES` 与 `master[k+1] JA` 拼成"一个 SD 槽"，故 `SD[0].JA` 误指向
master row 656 JA = "ドラゴンの力" (实为 SD[1])。已在 master-table 驱动 pipeline 中修正。
代码未引用 `0x4CAC / 0x815C` (0 ROM 字面量 hits)，故无运行时影响。

---

## 四、JA 末尾 9 条 master 表外 extras

JA 区末尾有 9 条 entry **不在 master 表内**（master 表仅覆盖 0..1641，这 9 条在 row 1641 之后）：

| idx (extra) | 内容 |
|---|---|
| 00 | "Death Message" 卡牌效果描述（长） |
| 01..04 | 「Ｉ」「Ｎ」「Ａ」「Ｌ」 4 张 kanji 卡名 |
| 05..08 | 「アイ」「エヌ」「エー」「エル」 4 张 hiragana 读音变体 |

通过非 master-table 的代码路径（硬编码地址或独立索引）访问。

---

## 五、Empty slot

某 lang 此 row 无翻译时，`master[i].offset[lang]` 指向一个 `\0` 字节（0-byte data + pad）。
各 lang empty 数：
- JA: 54
- EN: 78
- DE: 82
- FR/IT/ES 略有差异

总 entry 数对齐：每 lang `1642 = nonempty + empty`。

---

## 六、Anomaly: hi byte 0x9E

JA 区 staff credits (master row 956) 含 1 处异常 2B pair `9E 8A` (= idx 1802 '立')，
hi byte 0x9E 偏离常规 0xF0-0xFE 范围。

**处理**：decoder 用 `b >= 0xF0` 阈值，把 `9E 8A` 切成 2 个 raw 字节透传到 txt；encoder
反向 encode 时保留 raw 字节 (cp ≤ 0xFF → `out.append(cp)`)。byte-identical 保持。

---

## 七、文件布局

| 文件 | 内容 |
|---|---|
| `data/game-strings.s` | 6 lang wrapper (JA → EN → DE → FR → IT → ES) |
| `data/game-strings-ja.s` | JA 区 `.byte` form |
| `data/game-strings-{en,de,fr,it,es}.s` | 5 lang `.ascii` form (CP1252 编码写盘) |
| `text/game-strings/{ja,en,de,fr,it,es}.txt` | UTF-8 中间产物 (master row idx 编号) |
| `tools/game-strings/decode_s_to_txt.py` | ROM → txt (master 表驱动) |
| `tools/game-strings/encode_txt_to_s.py` | txt → .s |
| `tools/game-strings/build_char_to_idx.py` | 扫 ja.txt 建 char_to_idx (JA encoder 用) |
| `tools/game-strings/char_to_idx.json` | JA char → idx 表 (来自 codetable + ja.txt 字符集) |
| `tools/jp-decode/codetable.json` | JA glyph → Unicode 字符 (1925 idx) |

---

## 八、Ghidra labels

由 `tools/ghidra-labeling/LabelDataCrystalRomMap.py` 维护：

| 地址 | Label | 说明 |
|---|---|---|
| `0x08000F40` | `game_str_pointer_table` | master 表 |
| `0x09DB9C10` | `game_str_ja` | JA 区 (= STRING_TABLE_BASE) |
| `0x09DC4620` | `game_str_en` | EN 区 |
| `0x09DCF471` | `game_str_de` | DE 区 |
| `0x09DDB7DE` | `game_str_fr` | FR 区 |
| `0x09DE7CB7` | `game_str_it` | IT 区 |
| `0x09DF3C66` | `game_str_es` | ES 区 |

asm/all.s `.word 0x08000F40` 自动符号化为 `.word game_str_pointer_table` (101 处)；
`.word 0x09DB9C10` → `.word game_str_ja` (99 处)。

---

## 九、txt 格式范例 (decode 输出)

```
=PRE= pad=19 @ region 起始未指向 leading \0 区        # 仅 5 lang 有

=0000= pad=2 (empty) @ row 0 = empty placeholder

=0001= pad=2
Summoning this monster requires @31 Tribute@0. Do you wish to @2Summon@0?

=0655= pad=2 @ SD[0] Starter Deck
STARTER DECK

=1217= pad=2 @ OPP[0] Kuriboh
Kuriboh & Friends

=1641= pad=2 @ last shared entry
Fight On!

@ === JA-only extras (master 表外) ===
=JA_EXTRA_00= pad=2 @ Death Message description (long)
相手ターン終了時每に...
```

---

## 十、相关方法论

- `doc/dev/methodology/symbolization.md` — 字面量池符号化通用流程
- `doc/dev/methodology/font-glyph-ocr.md` — JA 字库码表逆向（codetable 数据来源）
