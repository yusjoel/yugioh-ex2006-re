# GAS 汇编文件中的 CP1252 字符串

## 背景

本游戏包含 5 种欧洲语言（EN/DE/FR/IT/ES）的文本字符串，采用 **CP1252（Windows-1252）** 单字节编码。

CP1252 是 Latin-1（ISO 8859-1）的超集：
- `0x20–0x7E`：与 ASCII 完全相同
- `0xA0–0xFF`：与 Latin-1 完全相同（西欧字符）
- **`0x80–0x9F`：CP1252 扩展区，Latin-1 中为未定义的 C1 控制码**

正是这段扩展区包含德语、法语等语言中实际使用的印刷符号：

| 字符 | 字节 | 说明 |
|------|------|------|
| „    | 0x84 | 德语开引号（下双引号） |
| "    | 0x93 | 德语闭引号（右双引号） |
| …    | 0x85 | 省略号 |
| –    | 0x96 | 半破折号 |
| —    | 0x97 | 全破折号 |
| ü    | 0xFC | 德语（Unglück…） |
| ö    | 0xF6 | 德语（Hölle…） |
| é    | 0xE9 | 法语（nécessite…） |
| ¡    | 0xA1 | 西班牙语（¡Atacar!…） |

---

## 为什么不能用 Latin-1

Latin-1 将 `0x80–0x9F` 定义为 C1 控制码（不可打印），无法直接表示 `„`（0x84）、`"`（0x93）等字符。  
若使用 Latin-1 打开以 CP1252 保存的文件，这些字节会显示为乱码或控制字符。

**结论：游戏字符串文件必须使用 CP1252 编码，而非 Latin-1。**

---

## GAS 指令选择

### `.ascii` 的使用规则

本项目使用 `.ascii`（不自动追加 null 终止符），终止符需手动写入 `\0`：

```asm
.ascii "Kuriboh & Friends\0"          @ 单 null 终止（常见情形）
.ascii "Do you surrender?\0\0"        @ 双 null（最多在 .ascii 内包含 2 个 \0）
.zero 3                               @ 超过 2 个 \0 时，剩余部分用 .zero
```

> **规则：`.ascii` 字面量内最多含 2 个 `\0`，超出的连续 null 字节改用 `.zero N`。**

### 特殊字符写法

**方案 A — `\xNN` 十六进制转义（UTF-8 源文件）**

```asm
.ascii "Monster des Ungl\xfccks\0"    @ ü = 0xFC
.ascii "Begriff \x84Dunkler\x93\0"    @ „…" = 0x84 / 0x93
```

**方案 B — 直接写入 CP1252 字符（CP1252 源文件）** ✅ 推荐

将 `.s` 文件以 **CP1252 编码** 保存，GAS 逐字节读取字符串字面量，源文件中的字节直接输出，无需转义：

```asm
.ascii "Monster des Unglücks\0"       @ ü 直接写入，汇编输出 0xFC
.ascii "Begriff „Dunkler Skorpion"\0" @ „ = 0x84，" = 0x93，直接写入
```

> **不能使用 UTF-8：** UTF-8 中 `ü` 占两字节（`0xC3 0xBC`），GAS 会输出两个字节，导致 ROM 错误。

---

## Python 生成脚本规范

```python
def asm_escape(raw: bytes) -> str:
    """将字节序列转换为 GAS .ascii 字面量内容（CP1252 源文件）。"""
    parts = []
    for b in raw:
        if   b == 0x22: parts.append('\\"')        # 双引号
        elif b == 0x5C: parts.append('\\\\')       # 反斜杠
        elif b == 0x0A: parts.append('\\n')
        elif b == 0x0D: parts.append('\\r')
        elif b == 0x09: parts.append('\\t')
        elif b == 0x00: parts.append('\\0')        # null 终止符
        elif 0x20 <= b < 0x7F:                     # 可打印 ASCII
            parts.append(chr(b))
        elif 0x80 <= b <= 0x9F:                    # CP1252 扩展字符（如 „ "）
            try:    parts.append(bytes([b]).decode('cp1252'))
            except (UnicodeDecodeError, ValueError):
                    parts.append(f'\\x{b:02x}')    # 极少数未定义字节（0x81等）
        elif 0xA0 <= b <= 0xFF:                    # 可打印 Latin-1 / CP1252 高位字符
            parts.append(chr(b))
        else:
            parts.append(f'\\x{b:02x}')            # C0 控制字符
    return ''.join(parts)

# 写入时使用 CP1252 编码
with open('data/game-strings-de.s', 'w', encoding='cp1252') as f:
    f.write(content)
```

### 字节处理范围一览

| 范围 | 分类 | 处理方式 |
|------|------|---------|
| 0x00 | null 终止符 | `\0` |
| 0x01–0x1F | C0 控制码 | `\xNN`（`\n` `\r` `\t` 除外） |
| 0x20–0x7E | 可打印 ASCII | 直接写入 |
| 0x7F | DEL | `\x7f` |
| 0x80–0x9F | **CP1252 扩展区** | **直接写入对应字符**（未定义字节用 `\xNN`） |
| 0xA0–0xFF | 可打印 Latin-1 / CP1252 | 直接写入 |

---

## 编辑器配置

编辑 `data/game-strings-*.s` 时，需以 **CP1252** 打开，避免意外重编码：

- **VS Code**：点击右下角编码标签 → "以指定编码重新打开" → "西欧(Windows 1252)"  
  或在 `.vscode/settings.json` 中添加：
  ```json
  { "files.encoding": "windows1252" }
  ```

- **Notepad++**：编码 → 字符集 → 西欧语言 → Windows-1252

- **Vim**：`:set fileencoding=cp1252`

---

## 相关文件

| 文件 | 编码 | 说明 |
|------|------|------|
| `data/game-strings-en.s` | **CP1252** | 英语游戏文本 |
| `data/game-strings-de.s` | **CP1252** | 德语（含 `„` `"` 等 0x80–0x9F 字符） |
| `data/game-strings-fr.s` | **CP1252** | 法语 |
| `data/game-strings-it.s` | **CP1252** | 意大利语 |
| `data/game-strings-es.s` | **CP1252** | 西班牙语 |
| `data/deck-strings.s` | ASCII | 卡组名（自定义 2 字节编码） |
| 其余 `.s` 文件 | ASCII | 纯 ASCII 内容 |
| `tools/export_game_strings.py` | — | 生成脚本，输出编码 `cp1252` |
