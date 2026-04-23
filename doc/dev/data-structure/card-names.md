# 卡牌名字符串表

卡名存储于两个独立区域：**欧洲 5 语言池**（CP1252）+ **日语池**（XX 双字节编码）。

---

## 欧洲语言（EN/DE/FR/IT/ES）

| 项目 | 值 |
|------|-----|
| ROM 偏移起始 | `0x015BB5AC` |
| 字符串编码 | CP1252（兼容 Latin-1，含德/法/西班牙 extended 字符） |
| 排列顺序 | 与 `card-attributes.md` 主记录槽位顺序一致 |

### 排列

每张卡依次排列 **5 个语言**的 null 终止字符串：

| 顺序 | 语言 |
|------|------|
| 1 | EN（英语） |
| 2 | DE（德语） |
| 3 | FR（法语） |
| 4 | IT（意大利语） |
| 5 | ES（西班牙语） |

**对齐规则**：每个字符串（含终止 `\0`）若字节数为奇数，补一个额外 `\0`，保持 2 字节对齐。

### 已验证示例（Blue-Eyes White Dragon @ slot 0x0FA7）

```
ROM 0x015BB5AC  → "Blue-Eyes White Dragon\0"     (EN, 24 字节，已对齐)
                → "Blauäugiger Weißer Drache\0\0" (DE, 奇长补一个 0)
                → "Dragon Blanc aux Yeux Bleus\0\0" (FR)
                → "Drago Bianco Occhi Blu\0\0"    (IT)
                → "Dragón Blanco de Ojos Azules\0" (ES)

下一张卡（slot 0x0FA8 = Mystical Elf）紧接其后
```

---

## 日语卡名（XX 双字节编码）

游戏内部保留日语卡名数据，存储于两个连续区域：索引表 + 字符串池。

### 索引表

| 项目 | 值 |
|------|-----|
| 索引表起始 | `0x0183885C` |
| 索引表结束 | `0x0183A924` |
| 条目数 | 2098 条 × 4 字节 = 8392 字节 |
| 条目类型 | `uint32 LE` |
| 含义 | 相对于字符串池基址的字节偏移 |

### 字符串池

| 项目 | 值 |
|------|-----|
| 字符串池起始 | `0x0183A924` |
| 字符串池大小 | ~43 KB（最大偏移量 = 43010） |
| 字符串编码 | 自定义 XX 2 字节（范围 `0xF081 – 0xF2A1`）|
| 终止符 | `0x00`（单字节） |

**访问算法**（函数 `0x000EEB3C`）：

```
card_name_ptr = 0x0183A924 + u32_le[0x0183885C + name_index × 4]
```

### 唯一字符串数

2054 个（44 对条目共享同一偏移，对应同名异画卡）。

---

## 编码细节

- CP1252 字符表与 GAS 汇编语法对齐规范 → 见 `string-encodings.md`（未来写入）
- XX 编码的 2 字节值 → 字符 映射表 → 见 `string-encodings.md`

---

## 相关文件

| 文件 | 内容 |
|------|------|
| `data/card-names.s` | 卡名池 + 2098×6 u32 指针表 合并汇编 |
| `tools/rom-export/export_card_data.py` | 从 ROM 重建 `card-names.s` |
| `tools/xx_codec.py` | XX 编码解码器（已映射 ~130 字符，覆盖率 37.8%） |
