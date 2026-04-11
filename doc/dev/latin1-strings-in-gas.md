# Latin-1 Strings in GAS Assembly Files

## Background

The game contains text strings for 5 European languages (EN/DE/FR/IT/ES).
These strings use **Latin-1 (ISO 8859-1)** encoding — the standard single-byte
encoding covering Western European characters such as:

| Char | Byte | Language |
|------|------|----------|
| ü    | 0xFC | German (Unglück, Beschwörung…) |
| ö    | 0xF6 | German (Hölle, beschwören…) |
| ä    | 0xE4 | German (wählen, Kämpfer…) |
| é    | 0xE9 | French (nécessite, évocation…) |
| ô    | 0xF4 | French (Fantômes…) |
| à    | 0xE0 | French (à Effet…) |
| ¡    | 0xA1 | Spanish (¡Atacar!…) |
| ¿    | 0xBF | Spanish (¿Continuar?…) |

---

## GAS Directive Choices

### `.ascii` vs `.string`

| Directive | Null terminator | Notes |
|-----------|----------------|-------|
| `.ascii "text"` | **Not added** — must write `\0` explicitly | Flexible but verbose |
| `.string "text"` | **Auto-appended** | Cleaner for C-style strings |
| `.asciz "text"` | Same as `.string` | Alias |

For this project we use **`.string`**:

```asm
.string "Kuriboh & Friends"        @ single-null terminated (common case)
.string "Do you surrender?\0"      @ double-null: literal \0 + auto null = 2 bytes
```

### Writing Special Characters

**Option A — `\xNN` hex escapes (UTF-8 source file)**

Works in any encoding but reduces readability:
```asm
.string "Monster des Ungl\xfccks"   @ u-umlaut = 0xFC
.string "beschw\xf6ren"             @ o-umlaut = 0xF6
```

**Option B — Direct Latin-1 characters (Latin-1 source file)** ✅ Preferred

Save the `.s` file with **Latin-1 encoding**.
GAS reads source bytes verbatim inside string literals, so byte 0xFC in the
source file produces byte 0xFC in the output — exactly what we need.

```asm
.string "Monster des Unglücks"     @ u-umlaut written directly, assembles to 0xFC
.string "beschwören"               @ o-umlaut written directly, assembles to 0xF6
```

> **Why not UTF-8?**
> In a UTF-8 file, `ü` is two bytes: `0xC3 0xBC`.
> GAS would output both bytes, producing wrong binary output.
> Latin-1 keeps every character as exactly one byte.

---

## File Generation (Python)

When generating `.s` files with Python, declare `latin-1` in the coding cookie
and open the output file with the same encoding:

```python
# -*- coding: latin-1 -*-

def asm_escape(raw: bytes) -> str:
    """Convert raw bytes to a GAS .string literal body (Latin-1 source file)."""
    parts = []
    for b in raw:
        if   b == 0x22: parts.append('\\"')       # double-quote
        elif b == 0x5C: parts.append('\\\\')      # backslash
        elif b == 0x0A: parts.append('\\n')
        elif b == 0x0D: parts.append('\\r')
        elif b == 0x09: parts.append('\\t')
        elif 0x20 <= b < 0x7F:   parts.append(chr(b))   # printable ASCII
        elif 0xA0 <= b <= 0xFF:  parts.append(chr(b))   # printable Latin-1 (written directly)
        else:                    parts.append(f'\\x{b:02x}')  # C0/C1 control codes
    return ''.join(parts)

with open('data/game-strings.s', 'w', encoding='latin-1') as f:
    f.write(content)
```

> **Why this works in Python 3:**
> `chr(0xFC)` in Python is Unicode codepoint U+00FC (`ü`).
> When written with `encoding='latin-1'`, Python maps U+0000–U+00FF directly
> to bytes 0x00–0xFF, so `ü` becomes the single byte `0xFC` on disk.

### Mojibake Trap

A common mistake when generating `.s` files from byte values:

```python
# WRONG: build string from raw bytes, save as UTF-8
s = ''.join(chr(b) for b in raw_bytes)   # chr(0xFC) = 'ü' (U+00FC)
with open('out.s', 'w', encoding='utf-8') as f:
    f.write(s)
# Result: 'ü' encodes to 0xC3 0xBC in UTF-8 → two bytes in output, wrong!
```

```python
# CORRECT: use latin-1 encoding so U+00FC -> single byte 0xFC
with open('out.s', 'w', encoding='latin-1') as f:
    f.write(s)
```

Alternatively, escape all non-ASCII bytes with `\xNN` and use UTF-8:

```python
# ALSO CORRECT: escape everything, save as UTF-8
parts.append(f'\\x{b:02x}')  # e.g. \xfc — readable only for maintainers
with open('out.s', 'w', encoding='utf-8') as f:
    f.write(s)
```

---

## Bytes to Avoid Writing Directly

| Range | Classification | Treatment |
|-------|---------------|-----------|
| 0x00–0x1F | C0 control codes | `\xNN` (except `\n`, `\r`, `\t`) |
| 0x20–0x7E | Printable ASCII | Write directly |
| 0x7F | DEL | `\x7f` |
| 0x80–0x9F | C1 control codes | `\xNN` — non-printable in Latin-1 |
| 0xA0–0xFF | Printable Latin-1 | Write directly ✅ |

---

## Editor Setup

To avoid accidental re-encoding when editing `data/game-strings.s`:

- **VS Code**: Click the encoding label in the bottom-right status bar →
  "Reopen with Encoding" → "Western (ISO 8859-1)".
  Or add to `.vscode/settings.json`:
  ```json
  { "files.encoding": "latin1" }
  ```

- **Notepad++**: Encoding → Character sets → Western European → ISO-8859-1

- **Vim**: `:set fileencoding=latin1`

---

## Related Files

| File | Encoding | Notes |
|------|----------|-------|
| `data/game-strings.s` | **Latin-1** | EN/DE/FR/IT/ES game text, ~343 KB |
| `data/deck-strings.s` | ASCII | XX-language deck names (custom 2-byte encoding, unknown) |
| All other `.s` files   | ASCII | Pure ASCII content |
| Generator script | `files/gen_game_strings.py` | Session state; `# -*- coding: latin-1 -*-` |
