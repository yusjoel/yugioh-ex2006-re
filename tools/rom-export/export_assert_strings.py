# -*- coding: utf-8 -*-
"""
export_assert_strings.py  (一次性扫描器, 非 export_all 步骤)

扫 asm 找所有 suppress_assert_report 调用点的 file/expr 字符串指针 (NNS/GL SDK 断言串,
位于 0x09e3xxxx..0x09e5xxxx, 在 rom.s line733 raw blob 内), 生成 Ghidra 标注驱动 CSV:
  tools/ghidra-labeling/assert_labels.csv  (slot_addr,string_addr,label)

随后 AddAssertStringLabels.py 据此在 Ghidra 给串地址建 USER_DEFINED label + 给代码槽加
DATA ref; 再跑 ExportRomLabelsToInc.py 把 label 写入 constants/rom_data.inc (项目既定模式);
代码侧 .word 经 resolve_word_symbol 导出为 label 名 -> byte-identical。

命名 (小写, 匹配 rom_data.inc 风格):
  file 串 (.c/.h)  -> <basename 小写, . -> _>_filename  (如 gl_file_c_filename)
  expr 串          -> assert_<内容 sanitized 小写截断>  (碰撞加 _<addr 低3位>)
已在 rom_data.inc 的地址跳过 (用既有 label); 名字与既有 label 去重。

用法: python tools/rom-export/export_assert_strings.py
"""
import re, glob, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
ROM = os.path.join(ROOT, "roms", "2343.gba")
ROMDATA = os.path.join(ROOT, "constants", "rom_data.inc")
OUT = os.path.join(ROOT, "tools", "ghidra-labeling", "assert_labels.csv")
B = 0x08000000
rom = open(ROM, "rb").read()


def readstr(addr):
    o = addr - B
    j = o
    while j < len(rom) and 32 <= rom[j] < 127:
        j += 1
    return rom[o:j].decode("ascii", "replace")


def is_asciz(addr):
    o = addr - B
    if o < 0 or o >= len(rom):
        return False
    s = readstr(addr)
    if len(s) < 2:
        return False
    return (o + len(s) < len(rom)) and rom[o + len(s)] == 0


def load_rom_data():
    addrs = {}
    names = set()
    for l in open(ROMDATA, encoding="utf-8"):
        m = re.match(r'\.equ\s+(\w+),\s+0x([0-9A-Fa-f]+)', l.strip())
        if m:
            addrs[int(m.group(2), 16)] = m.group(1)
            names.add(m.group(1))
    return addrs, names


def scan():
    pairs = []
    for fn in glob.glob(os.path.join(ROOT, "asm", "[0-9][0-9]_*.s")):
        L = open(fn, encoding="utf-8", errors="replace").read().splitlines()
        lab = {}
        for i, l in enumerate(L):
            m = re.match(r'^([A-Za-z_]\w*):', l)
            if m and i + 1 < len(L):
                mw = re.search(r'^\s*\.word\s+\S.*@\s*([0-9a-f]{8})\s+([0-9a-f]{8})(?:\s|$)', L[i + 1])
                if mw:
                    sa = int(mw.group(1), 16)
                    by = mw.group(2)
                    v = int(by[6:8] + by[4:6] + by[2:4] + by[0:2], 16)
                    lab[m.group(1)] = (sa, v)
        for i, l in enumerate(L):
            if 'bl suppress_assert_report' in l:
                closest = {}
                for j in range(i - 1, max(0, i - 25) - 1, -1):
                    mm = re.match(r'\s*ldr (r[02]),\s*([A-Za-z_]\w*)', L[j])
                    if mm and mm.group(1) not in closest and mm.group(2) in lab:
                        closest[mm.group(1)] = lab[mm.group(2)]
                    if len(closest) == 2:
                        break
                for reg, (sa, v) in closest.items():
                    if 0x09e396b8 <= v < 0x09e398dc:   # demo 块 (已 carve)
                        continue
                    if is_asciz(v):
                        pairs.append((sa, v))
    return sorted(set(pairs))


def san(s, maxlen=30):
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_').lower()
    return s[:maxlen].rstrip('_')


def main():
    rd_addrs, rd_names = load_rom_data()
    pairs = scan()
    straddrs = sorted(set(v for _, v in pairs))

    label = {}
    used = set(rd_names)
    skipped_existing = 0
    for a in straddrs:
        if a in rd_addrs:           # 已在 rom_data.inc, 用既有 label, 不重建
            label[a] = rd_addrs[a]
            skipped_existing += 1
            continue
        c = readstr(a)
        if re.search(r'\.[ch]$', c):
            base = san(c.rsplit('/', 1)[-1]) + "_filename"
        else:
            base = "assert_" + san(c)
        base = base or ("assert_%x" % a)
        nm = base
        if nm in used:
            nm = "%s_%03x" % (base, a & 0xfff)
        while nm in used:
            nm = nm + "_x"
        used.add(nm)
        label[a] = nm

    rows = ["slot_addr,string_addr,label,is_new"]
    for sa, v in pairs:
        is_new = "0" if v in rd_addrs else "1"
        rows.append("0x%08x,0x%08x,%s,%s" % (sa, v, label[v], is_new))
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")

    # ---- 函数映射 (slot_addr -> 所属函数名, largest start <= slot) ----
    funcs = []
    for l in open(os.path.join(ROOT, "temp", "ghidra-functions.csv"), encoding="utf-8"):
        p = l.strip().split(",")
        if len(p) >= 2 and p[0].startswith("0x"):
            try:
                funcs.append((int(p[0], 16), p[1]))
            except ValueError:
                pass
    funcs.sort()
    import bisect
    faddrs = [a for a, _ in funcs]

    def fn_of(slot):
        i = bisect.bisect_right(faddrs, slot) - 1
        return funcs[i][1] if i >= 0 else "fn_%08x" % slot

    # ---- carve 块: 把 after-demo incbin [0x1E398DC,0x1E58D0C) 拆成 .incbin + .asciz ----
    AFTER_START, AFTER_END = 0x1E398DC, 0x1E58D0C

    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"')

    cb = ["@ ----------------------------------------------------------------------------",
          "@ NNS/GL SDK 断言串 (suppress_assert_report file/expr 参数) — carve 自 0x1E317B4 blob 的",
          "@ after-demo 段; 仅被代码引用的 156 串抽成带 label 的 .asciz, 其余 (未引用串/二进制/指针表)",
          "@ 仍以 .incbin 原样保留。代码 .word 经 resolve_word_symbol 指向这些 label。byte-identical。",
          "@ ----------------------------------------------------------------------------"]
    prev = AFTER_START
    for a in straddrs:  # 已排序
        foff = a - B
        if foff < prev:
            continue  # 不在 after 段 (理论上不会)
        if foff > prev:
            cb.append('\t.incbin "roms/2343.gba", 0x%X, 0x%X' % (prev, foff - prev))
        s = readstr(a)
        cb.append('%s:' % label[a])
        cb.append('\t.asciz "%s"' % esc(s))
        prev = foff + len(s) + 1
    if prev < AFTER_END:
        cb.append('\t.incbin "roms/2343.gba", 0x%X, 0x%X' % (prev, AFTER_END - prev))
    open(os.path.join(ROOT, "tools", "ghidra-labeling", "assert_carve_block.txt"),
         "w", encoding="utf-8", newline="\n").write("\n".join(cb) + "\n")

    # ---- 槽改名 + EOL CSV: slot_addr, new_label=<func>_<string_label>, eol_text ----
    used_slot = {}
    srows = ["slot_addr,slot_label,eol_text"]
    for sa, v in sorted(pairs):
        base = "%s_%s" % (fn_of(sa), label[v])
        n = used_slot.get(base, 0)
        used_slot[base] = n + 1
        sl = base if n == 0 else "%s_%03x" % (base, sa & 0xfff)
        eol = readstr(v).replace(",", " ")[:60]
        srows.append("0x%08x,%s,%s" % (sa, sl, eol))
    open(os.path.join(ROOT, "tools", "ghidra-labeling", "assert_slots.csv"),
         "w", encoding="utf-8", newline="\n").write("\n".join(srows) + "\n")

    nnew = len([a for a in straddrs if a not in rd_addrs])
    print("[ok] %s (%d 槽引用)" % (OUT, len(pairs)))
    print("[ok] assert_carve_block.txt — 替换 rom.s 的 after-demo incbin (%d 串 carve)" % len(straddrs))
    print("[ok] assert_slots.csv (%d 槽改名 <func>_<label>+EOL)" % len(pairs))
    print("  唯一断言串: %d (rom_data.inc 既有: %d, 新: %d)" % (len(straddrs), skipped_existing, nnew))


if __name__ == "__main__":
    main()
