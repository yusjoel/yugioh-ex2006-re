#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_pack_ui_state_writes.py  --  静态扫所有对 pack_ui_state 的写入

输入: asm/all.s + temp/ghidra-functions.csv
输出: temp/pack_ui_state_writes.csv

实现:
1. 解析 asm/all.s 收集 (line_no, addr, op_text, raw)
2. 找 DAT_<addr>: .word pack_ui_state 字面量定义点 (~210 处)
3. 找 ldr Rn, DAT_<addr> 加载点 (每个字面量被 1 个或多个 ldr 引用)
4. 从 ldr 位置往后扫指令, 追踪 Rn 的污染传播:
     - mov / adds 派生新寄存器, 同时维护 base_offset
     - STR/STRH/STRB Rv,[Rt,#imm]  Rt 命中 -> 记录写入 (offset_total = Rt.offset + imm)
5. 写入值 Rv 回溯前 8 条指令:
     - movs Rv,#imm                    -> imm
     - movs Rv,#imm + lsls Rv,Rv,#k    -> imm<<k  (常见 thumb 大常量构造)
     - ldr Rv, DAT_<addr>              -> 解析 .word 值
     - mvns / etc                      -> 标 'reg' 不解析
6. 按 (offset, value) 聚合并输出
"""

import csv
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASM = os.path.join(REPO, "asm", "all.s")
FUNCS_CSV = os.path.join(REPO, "temp", "ghidra-functions.csv")
OUT_CSV = os.path.join(REPO, "temp", "pack_ui_state_writes.csv")

PACK_UI_STATE_TOKEN = "pack_ui_state"

# 正则
RE_LINE_ADDR = re.compile(r"@\s*([0-9a-f]{8})\s*[0-9a-f]+\s*$")
RE_DAT_DEF = re.compile(r"^(DAT_[0-9a-f]{8}):\s*$")
RE_DAT_DEF_INLINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*$")
RE_WORD_PACK = re.compile(
    r"^\s*\.word\s+(pack_ui_state|0x03005850)\b"
)
RE_LDR_DAT = re.compile(
    r"^\s*ldr\s+(r\d+),\s*(DAT_[0-9a-f]{8}|[A-Za-z_][A-Za-z0-9_]*)"
)
# str/strh/strb forms
RE_STR_REG_OFF = re.compile(
    r"^\s*(str|strh|strb)\s+(r\d+),\s*\[(r\d+)(?:,\s*#(0x[0-9a-fA-F]+|\d+))?\]"
)
RE_MOVS_IMM = re.compile(r"^\s*(movs|mov)\s+(r\d+),\s*#(0x[0-9a-fA-F]+|\d+)")
RE_LSLS_IMM = re.compile(r"^\s*lsls\s+(r\d+),\s*(r\d+),\s*#(0x[0-9a-fA-F]+|\d+)")
RE_ADDS_IMM = re.compile(
    r"^\s*adds?\s+(r\d+),\s*(r\d+),\s*#(0x[0-9a-fA-F]+|\d+)"
)
RE_ADDS_REG = re.compile(r"^\s*adds?\s+(r\d+),\s*(r\d+),\s*(r\d+)")
RE_MOV_REG = re.compile(r"^\s*(mov|movs)\s+(r\d+),\s*(r\d+)\s*(?:@|$)")
RE_LDR_REG = re.compile(r"^\s*ldr\s+(r\d+),\s*\[(r\d+)(?:,\s*#(0x[0-9a-fA-F]+|\d+))?\]")
RE_BL = re.compile(r"^\s*bl\s+")
RE_BX = re.compile(r"^\s*bx\s+lr")
RE_POP_PC = re.compile(r"^\s*pop\s+\{[^}]*pc\}")


def parse_imm(s):
    return int(s, 0)


def load_func_entries(path):
    """Return sorted list of (entry_addr, name) and {addr: name}."""
    entries = []
    name_by_addr = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            a = int(r["address"], 0)
            n = r["name"]
            entries.append((a, n))
            name_by_addr[a] = n
    entries.sort()
    return entries, name_by_addr


def load_asm(path):
    """Return list of dicts:
       {line_no, addr (int or None), text (the asm op without comment),
        full (raw line), label (None or str if line starts a label)}.
    """
    out = []
    with open(path, encoding="utf-8") as f:
        for ln, raw in enumerate(f, 1):
            text = raw.rstrip("\n")
            label = None
            # label-only line "xxx:"
            mlab = RE_DAT_DEF_INLINE.match(text)
            if mlab:
                label = mlab.group(1)
            # extract @ <addr> comment if present
            addr = None
            m = RE_LINE_ADDR.search(text)
            if m:
                try:
                    addr = int(m.group(1), 16)
                except Exception:
                    addr = None
            # strip comment and label-stuff for op text
            op_text = text
            cmt_idx = op_text.find("@")
            if cmt_idx >= 0:
                op_text = op_text[:cmt_idx]
            op_text = op_text.strip()
            out.append({
                "line": ln,
                "addr": addr,
                "text": op_text,
                "raw": text,
                "label": label,
            })
    return out


def find_pack_ui_state_dats(lines):
    """Find every (DAT_label_name, line_no_of_label, addr_of_label) where
       the next non-empty line is `.word pack_ui_state` or `.word 0x03005850`."""
    out = []  # (dat_name, dat_addr_int, def_line)
    for i, ln in enumerate(lines):
        if ln["label"] is None:
            continue
        # next non-empty line
        j = i + 1
        while j < len(lines) and not lines[j]["text"]:
            j += 1
        if j >= len(lines):
            continue
        if RE_WORD_PACK.match(lines[j]["text"]):
            out.append((ln["label"], lines[j]["addr"], i))
    return out


def find_ldr_uses(lines, dat_names):
    """Return list of (line_index, dest_reg, dat_name)."""
    dat_set = set(dat_names)
    out = []
    for i, ln in enumerate(lines):
        if not ln["text"].startswith(("ldr",)):
            continue
        m = RE_LDR_DAT.match(ln["text"])
        if not m:
            continue
        if m.group(2) in dat_set:
            out.append((i, m.group(1), m.group(2)))
    return out


def func_for_line_addr(addr, entries):
    """Find function entry that covers this addr (largest entry <= addr).
       Returns (entry_addr, name) or (None, None)."""
    if addr is None:
        return (None, None)
    lo, hi = 0, len(entries) - 1
    best = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if entries[mid][0] <= addr:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    if best < 0:
        return (None, None)
    return entries[best]


def trace_writes(lines, ldr_idx, dest_reg, entries, max_steps=80):
    """Forward-scan from the LDR; collect writes.
       Returns list of dicts:
         {func_addr, func_name, instr_addr, op, val_reg, base_reg,
          base_offset, imm_offset, total_offset, value_kind, value}
    """
    writes = []
    # tainted: register -> offset_from_pack_ui_state_base
    taint = {dest_reg: 0}
    # Find function the LDR belongs to
    ldr_line = lines[ldr_idx]
    f_entry, f_name = func_for_line_addr(ldr_line["addr"], entries)

    # Helper: scan back to find immediate value of register
    def lookup_imm(start_idx, reg):
        # scan back up to 10 instr lines
        steps = 0
        i = start_idx - 1
        last_imm = None
        last_lsls = None
        while i >= 0 and steps < 10:
            t = lines[i]["text"]
            if not t:
                i -= 1
                continue
            steps += 1
            # if reg is overwritten by something we don't model, give up
            m = RE_MOVS_IMM.match(t)
            if m and m.group(2) == reg:
                last_imm = parse_imm(m.group(3))
                # check if there's an lsls *after* this movs that shifts reg
                # we did the scan back-to-forward, so look forward for lsls of same reg
                for j in range(i + 1, start_idx):
                    t2 = lines[j]["text"]
                    if not t2:
                        continue
                    m2 = RE_LSLS_IMM.match(t2)
                    if m2 and m2.group(1) == reg and m2.group(2) == reg:
                        last_imm = (last_imm << parse_imm(m2.group(3))) & 0xFFFFFFFF
                return ("imm", last_imm)
            # ldr Rv, DAT_xxx --> resolve via .word value
            m = RE_LDR_DAT.match(t)
            if m and m.group(1) == reg:
                # find the DAT_ definition
                tgt = m.group(2)
                for k in range(len(lines)):
                    if lines[k]["label"] == tgt:
                        # next non-empty line
                        kk = k + 1
                        while kk < len(lines) and not lines[kk]["text"]:
                            kk += 1
                        wt = lines[kk]["text"] if kk < len(lines) else ""
                        mw = re.match(
                            r"^\.word\s+(\S+)", wt
                        )
                        if mw:
                            v = mw.group(1)
                            try:
                                return ("imm", parse_imm(v))
                            except Exception:
                                return ("symbol", v)
                        break
                return ("ldr_dat", tgt)
            # ldr Rv,[...] dynamic
            m = RE_LDR_REG.match(t)
            if m and m.group(1) == reg:
                return ("dyn_ldr", "[%s+%s]" % (m.group(2), m.group(3) or "0"))
            # mov reg,reg copy: trace through
            m = RE_MOV_REG.match(t)
            if m and m.group(2) == reg:
                reg = m.group(3)  # follow source
                continue
            # adds Rv, ..., #imm: stop (we don't fully model)
            m = RE_ADDS_IMM.match(t)
            if m and m.group(1) == reg:
                return ("dyn", "adds")
            i -= 1
        return ("unk", None)

    for step in range(max_steps):
        idx = ldr_idx + 1 + step
        if idx >= len(lines):
            break
        ln = lines[idx]
        # don't cross function boundary
        if ln["addr"] is not None:
            cur_entry, _ = func_for_line_addr(ln["addr"], entries)
            if cur_entry != f_entry and cur_entry is not None:
                break
        t = ln["text"]
        if not t:
            continue
        # store?
        m = RE_STR_REG_OFF.match(t)
        if m:
            op, vreg, breg, immstr = m.group(1), m.group(2), m.group(3), m.group(4)
            if breg in taint:
                imm = parse_imm(immstr) if immstr else 0
                base_off = taint[breg]
                total = base_off + imm
                vk, vv = lookup_imm(idx, vreg)
                writes.append({
                    "func_addr": "0x%08x" % f_entry if f_entry else "",
                    "func_name": f_name or "",
                    "instr_addr": "0x%08x" % ln["addr"] if ln["addr"] else "",
                    "op": op,
                    "val_reg": vreg,
                    "base_reg": breg,
                    "base_offset": base_off,
                    "imm_offset": imm,
                    "total_offset": total,
                    "value_kind": vk,
                    "value": vv,
                })
            # don't continue tracking writer reg, but tainted base may be reused
        # adds Rk, Rt, #imm: derive
        m = RE_ADDS_IMM.match(t)
        if m:
            dst, src, immstr = m.group(1), m.group(2), m.group(3)
            if src in taint:
                taint[dst] = taint[src] + parse_imm(immstr)
            elif dst in taint and src != dst:
                # dst overwritten by non-tainted source
                taint.pop(dst, None)
            continue
        # adds Rk, Rt, Rs: derive with dynamic offset
        m = RE_ADDS_REG.match(t)
        if m:
            dst, src1, src2 = m.group(1), m.group(2), m.group(3)
            if src1 in taint or src2 in taint:
                # treat as derived but offset unknown
                base_t = taint.get(src1, taint.get(src2))
                taint[dst] = base_t  # approximation: copy known base offset, ignore dyn
            elif dst in taint:
                taint.pop(dst, None)
            continue
        # mov Rk, Rt
        m = RE_MOV_REG.match(t)
        if m:
            dst, src = m.group(2), m.group(3)
            if src in taint:
                taint[dst] = taint[src]
            elif dst in taint:
                taint.pop(dst, None)
            continue
        # ldr Rk, ... or movs Rk, #imm: clobber if Rk in taint
        m = RE_MOVS_IMM.match(t)
        if m:
            r = m.group(2)
            if r in taint:
                taint.pop(r, None)
            continue
        m = RE_LDR_DAT.match(t) or RE_LDR_REG.match(t)
        if m:
            r = m.group(1)
            if r in taint:
                taint.pop(r, None)
            continue
        # bl: caller-saved regs r0-r3,r12 are clobbered
        if RE_BL.match(t):
            for cs in ("r0", "r1", "r2", "r3", "r12"):
                taint.pop(cs, None)
            continue
        # function exit: stop
        if RE_BX.match(t) or RE_POP_PC.match(t):
            break
        # else: ignore
    return writes


def main():
    print("[load] %s" % ASM)
    lines = load_asm(ASM)
    print("  %d lines" % len(lines))
    print("[load] %s" % FUNCS_CSV)
    entries, name_by_addr = load_func_entries(FUNCS_CSV)
    print("  %d functions" % len(entries))

    print("[scan] pack_ui_state literal pool entries...")
    dats = find_pack_ui_state_dats(lines)
    print("  %d DAT_ defs pointing at pack_ui_state" % len(dats))
    dat_names = [d[0] for d in dats]
    ldrs = find_ldr_uses(lines, dat_names)
    print("  %d LDRs loading them" % len(ldrs))

    all_writes = []
    for ldr_idx, dest_reg, dat_name in ldrs:
        ws = trace_writes(lines, ldr_idx, dest_reg, entries)
        all_writes.extend(ws)
    print("[trace] %d total write instructions captured" % len(all_writes))

    # Aggregate by (offset, value)
    by_off_val = {}
    by_func = {}
    for w in all_writes:
        key = (w["total_offset"], w["value_kind"], w["value"])
        by_off_val.setdefault(key, []).append(w)
        by_func.setdefault(w["func_name"], set()).add(
            (w["total_offset"], w["value_kind"], w["value"])
        )

    # Dump CSV
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        cols = ["func_addr", "func_name", "instr_addr", "op",
                "total_offset", "value_kind", "value", "base_offset",
                "imm_offset", "val_reg", "base_reg"]
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for w in sorted(all_writes,
                        key=lambda x: (x["total_offset"],
                                       x["func_addr"], x["instr_addr"])):
            row = dict(w)
            row["total_offset"] = "0x%x" % row["total_offset"]
            row["base_offset"] = "0x%x" % row["base_offset"]
            row["imm_offset"] = "0x%x" % row["imm_offset"]
            if isinstance(row["value"], int):
                row["value"] = "0x%x" % row["value"]
            elif row["value"] is None:
                row["value"] = ""
            wr.writerow(row)
    print("[wrote] %s" % OUT_CSV)

    # Summary printout
    print()
    print("=" * 78)
    print("WRITE SUMMARY: aggregated by (offset, value)")
    print("-" * 78)
    print("%-10s %-8s %-14s %5s  funcs (sample)" %
          ("offset", "kind", "value", "hits"))
    print("-" * 78)
    rows_sorted = sorted(by_off_val.items(),
                         key=lambda kv: (kv[0][0], -len(kv[1])))
    for (off, vk, vv), ws in rows_sorted:
        if isinstance(vv, int):
            vstr = "0x%x" % vv
        elif vv is None:
            vstr = ""
        else:
            vstr = str(vv)
        funcs = sorted(set(w["func_name"] for w in ws))
        sample = ", ".join(funcs[:3])
        if len(funcs) > 3:
            sample += " (+%d)" % (len(funcs) - 3)
        print("0x%-8x %-8s %-14s %5d  %s" %
              (off, vk, vstr[:14], len(ws), sample))


if __name__ == "__main__":
    main()
