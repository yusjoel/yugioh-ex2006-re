#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_game_str_func_details.py

从 asm/all.s 解析 44 个 game_str 函数的细节，输出 temp/game-str-funcs-detail.csv。

输入:
  - temp/game-str-funcs.csv  : 44 个目标函数 (来自 awk 提取)
  - asm/all.s                : 全 ROM main code 反汇编 (已符号化)

每个函数提取:
  - body_lines               : 函数体行数 (FUN_xxx: 到下一个 FUN_xxx:)
  - n_callees / callees      : bl 调用列表
  - has_master_table         : 是否 ldr game_str_pointer_table
  - lang_bases               : 引用的 lang base 列表 (ja/en/de/fr/it/es)
  - has_lang_global          : 是否含 0x02006C2C / 0x02000000 + 0x6C2C 模式 (lang setting 全局)
  - direct_string_addrs      : 字面量池 .word 落在 STRING_TABLE 区段 [0x09DB9C10, 0x09DFF9D2] 的硬编码地址列表
  - candidate_ids            : 可能是 string id 的小立即数 (来自 mov #imm / cmp #imm / 字面量池小整数)
  - small_word_lits          : 字面量池里 < 0x800 的 .word 整数值 (剔除地址)
  - cmp_consts               : cmp #imm 立即数列表
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO = Path(__file__).resolve().parents[2]
ALL_S = REPO / "asm" / "all.s"
TARGETS_CSV = REPO / "temp" / "game-str-funcs.csv"
OUT_CSV = REPO / "temp" / "game-str-funcs-detail.csv"

# 字符串表寻址常量 (来自 doc/dev/data-structure/game-strings.md)
STRING_TABLE_LO = 0x09DB9C10
STRING_TABLE_HI = 0x09DFF9D2
LANG_BASES = {
    0x09DB9C10: "ja",
    0x09DC4620: "en",
    0x09DCF471: "de",
    0x09DDB7DE: "fr",
    0x09DE7CB7: "it",
    0x09DF3C66: "es",
}
MASTER_TABLE = 0x08000F40
LANG_GLOBAL = 0x02006C2C  # 多数函数用 ldr 0x02000000 + ldr 0x6C2C 拼出

# 目录边界: ROM 主代码区
ROM_CODE_LO = 0x08000000
ROM_CODE_HI = 0x084C7637

# 候选 id 范围: master 表行号 [0, 1641]，留点缓冲到 0x800 = 2048
ID_MAX_HEUR = 0x800

# ----- regex -----
RE_FUNC_LABEL = re.compile(r"^(FUN|SUB|thunk_FUN)_([0-9a-f]{8}):\s*$")
RE_ANY_LABEL = re.compile(r"^(\w[\w\d]*):\s*(?:@.*)?$")  # 任意 column-0 label
RE_INSTR = re.compile(r"^    (\S.*?)(?:\s+@\s+([0-9a-f]{8})\s+([0-9a-f]+))?$")

# 常见指令解析
RE_LDR_LABEL = re.compile(
    r"^\s*ldr\s+r\d+,\s*((?:PTR|DAT|LAB|SWITCH|UNK|OFF|EXT|FUN|SUB)_[\w]+)\s*(?:@.*)?$"
)
RE_BL = re.compile(r"^\s*bl\s+(\S+)\s*(?:@.*)?$")
RE_MOV_IMM = re.compile(r"^\s*movs?\s+r\d+,\s*#(0x[0-9a-fA-F]+|\d+)\s*(?:@.*)?$")
RE_CMP_IMM = re.compile(r"^\s*cmp\s+r\d+,\s*#(0x[0-9a-fA-F]+|\d+)\s*(?:@.*)?$")

# label 后跟一行 .word/.hword/.byte 解析
RE_WORD_VAL = re.compile(r"^\s*\.word\s+(\S+)")
RE_HWORD_VAL = re.compile(r"^\s*\.hword\s+(\S+)")


def parse_int_maybe(s: str) -> int | None:
    """0x... / 十进制 / 否则 None."""
    s = s.strip().rstrip(",")
    try:
        if s.startswith("0x") or s.startswith("0X"):
            return int(s, 16)
        return int(s)
    except ValueError:
        return None


def load_targets() -> List[Tuple[int, str, str, str, str]]:
    """读 temp/game-str-funcs.csv，返回 [(addr, fun_label, proposed, score, tags), ...]."""
    out = []
    with TARGETS_CSV.open() as f:
        for row in csv.reader(f):
            if not row:
                continue
            addr = parse_int_maybe(row[0])
            if addr is None:
                continue
            out.append((addr, row[1], row[2], row[3], row[4]))
    return out


def build_label_value_map(lines: List[str]) -> Dict[str, Tuple[str, str]]:
    """
    遍历整个 all.s, 为每个 column-0 label 记录紧随其后的 .word/.hword/.byte 值。
    返回: { label_name: (kind, raw_value) }
       kind: 'word' | 'hword' | 'byte' | 'other'
       raw_value: e.g. "game_str_pointer_table" / "0x09DB9C10" / "0x4012"
    只取 label 紧邻的 *第一行* (跳过空行); 多 .word 的连续表只记第一个 (用于 PTR_/DAT_ 解析).
    """
    out: Dict[str, Tuple[str, str]] = {}
    n = len(lines)
    for i, line in enumerate(lines):
        m = RE_ANY_LABEL.match(line)
        if not m:
            continue
        name = m.group(1)
        # 跳过函数标签 (它们后面是指令,非 .word)
        if RE_FUNC_LABEL.match(line):
            continue
        # 找紧邻下一行 (跳过空行)
        j = i + 1
        while j < n and lines[j].strip() == "":
            j += 1
        if j >= n:
            continue
        nxt = lines[j].rstrip("\n")
        m2 = RE_WORD_VAL.match(nxt)
        if m2:
            out[name] = ("word", m2.group(1))
            continue
        m3 = RE_HWORD_VAL.match(nxt)
        if m3:
            out[name] = ("hword", m3.group(1))
            continue
        if nxt.lstrip().startswith(".byte"):
            out[name] = ("byte", nxt.strip())
            continue
        out[name] = ("other", nxt.strip())
    return out


def find_func_starts(lines: List[str]) -> List[Tuple[int, int, str]]:
    """返回 [(line_idx, addr, label), ...] 按地址升序."""
    out = []
    for i, line in enumerate(lines):
        m = RE_FUNC_LABEL.match(line)
        if m:
            addr = int(m.group(2), 16)
            out.append((i, addr, line.split(":")[0]))
    out.sort(key=lambda t: t[1])
    return out


def resolve_word_value(
    label: str, lv_map: Dict[str, Tuple[str, str]]
) -> Tuple[str, int | None, str | None]:
    """
    给 ldr 引用的 label, 解析成 (kind, int_val, sym_val)
       kind: 'int' | 'sym' | 'unknown'
       int_val: 数值 (kind==int 时)
       sym_val: 符号名 (kind==sym 时, 如 'game_str_pointer_table')
    """
    if label not in lv_map:
        return ("unknown", None, None)
    kind, raw = lv_map[label]
    if kind != "word":
        # PTR/DAT 都该是 .word; 不是的话异常
        return ("unknown", None, None)
    iv = parse_int_maybe(raw)
    if iv is not None:
        return ("int", iv, None)
    # 否则当作符号名
    return ("sym", None, raw.rstrip(","))


def classify_word_value(int_val: int) -> str:
    """给 ldr 出来的数值分类."""
    if int_val == MASTER_TABLE:
        return "master_table"
    if int_val in LANG_BASES:
        return "lang_%s" % LANG_BASES[int_val]
    if STRING_TABLE_LO <= int_val <= STRING_TABLE_HI:
        return "string_addr"
    if int_val == LANG_GLOBAL:
        return "lang_global"
    if int_val == 0x02000000:
        return "ewram_base"
    if int_val == 0x6C2C:
        return "lang_offset"  # 配合 ewram_base 拼成 lang_global
    if 0x02000000 <= int_val < 0x02040000:
        return "ewram_addr"
    if 0x03000000 <= int_val < 0x03008000:
        return "iwram_addr"
    if 0x04000000 <= int_val < 0x04000400:
        return "io_reg"
    if ROM_CODE_LO <= int_val <= ROM_CODE_HI:
        return "rom_code_ptr"
    if 0x084C7638 <= int_val <= 0x09FFFFFF:
        return "rom_data_ptr"
    if 0 <= int_val < ID_MAX_HEUR:
        return "small_int"
    return "other_int"


def analyze_function(
    addr: int,
    body_lines: List[str],
    lv_map: Dict[str, Tuple[str, str]],
) -> dict:
    """
    扫一个函数体 lines (含尾随的 DAT/PTR pool, 但只把指令行当作分析对象).
    """
    info = {
        "address": "0x%08x" % addr,
        "body_lines": 0,
        "n_instr": 0,
        "callees": [],
        "n_callees": 0,
        "has_master_table": False,
        "lang_bases": [],
        "has_lang_global": False,
        "has_ewram_lang_pair": False,  # ewram_base + 0x6C2C 同时出现
        "direct_string_addrs": [],
        "small_word_lits": [],  # 字面量池里 < 0x800 的整数 (DAT_xxx: .word 0x0NNN)
        "candidate_ids_imm": [],  # mov #imm 立即数 (在 [0, 0x800) 范围)
        "cmp_consts": [],
        "all_word_u16": [],  # 字面量池所有 < 0x10000 的整数 .word (用于 logical_id remap 反查)
        "all_imm_u16": [],   # 函数体内所有 mov/movs #imm 立即数 (8-bit, 已含 candidate_ids_imm)
        "literal_summary": [],  # [(label, classify, value)]
    }

    info["body_lines"] = len(body_lines)

    seen_ewram_base = False
    seen_lang_offset = False

    for ln in body_lines:
        # 指令行 (4 空格缩进 + 指令)
        if not ln.startswith("    ") or ln.lstrip().startswith("."):
            # 数据行 / label 行 / .word 行 - 在 literal pool 里
            # 这里我们已经按 ldr label 引用解析, 所以 pool 行不直接处理
            continue

        info["n_instr"] += 1

        # ldr rN, <LABEL>
        m = RE_LDR_LABEL.match(ln)
        if m:
            lbl = m.group(1)
            kind, iv, sv = resolve_word_value(lbl, lv_map)
            if kind == "sym":
                info["literal_summary"].append((lbl, "sym:%s" % sv, sv))
                if sv == "game_str_pointer_table":
                    info["has_master_table"] = True
                elif sv.startswith("game_str_") and sv[len("game_str_"):] in (
                    "ja",
                    "en",
                    "de",
                    "fr",
                    "it",
                    "es",
                ):
                    lang = sv[len("game_str_"):]
                    if lang not in info["lang_bases"]:
                        info["lang_bases"].append(lang)
            elif kind == "int":
                cls = classify_word_value(iv)
                info["literal_summary"].append((lbl, cls, "0x%x" % iv))
                if 0 <= iv < 0x10000 and iv not in info["all_word_u16"]:
                    info["all_word_u16"].append(iv)
                if cls == "master_table":
                    info["has_master_table"] = True
                elif cls.startswith("lang_") and cls[5:] in (
                    "ja",
                    "en",
                    "de",
                    "fr",
                    "it",
                    "es",
                ):
                    lng = cls[5:]
                    if lng not in info["lang_bases"]:
                        info["lang_bases"].append(lng)
                elif cls == "lang_global":
                    info["has_lang_global"] = True
                elif cls == "ewram_base":
                    seen_ewram_base = True
                elif cls == "lang_offset":
                    seen_lang_offset = True
                elif cls == "string_addr":
                    if iv not in info["direct_string_addrs"]:
                        info["direct_string_addrs"].append(iv)
                elif cls == "small_int":
                    if iv not in info["small_word_lits"]:
                        info["small_word_lits"].append(iv)
            else:
                info["literal_summary"].append((lbl, "unknown", ""))
            continue

        # bl <target>
        m = RE_BL.match(ln)
        if m:
            tgt = m.group(1).rstrip(",")
            if tgt not in info["callees"]:
                info["callees"].append(tgt)
            continue

        # mov/movs rN, #imm
        m = RE_MOV_IMM.match(ln)
        if m:
            iv = parse_int_maybe(m.group(1))
            if iv is not None and 0 <= iv < 0x10000:
                if iv not in info["all_imm_u16"]:
                    info["all_imm_u16"].append(iv)
                if iv < ID_MAX_HEUR and iv not in info["candidate_ids_imm"]:
                    info["candidate_ids_imm"].append(iv)
            continue

        # cmp rN, #imm
        m = RE_CMP_IMM.match(ln)
        if m:
            iv = parse_int_maybe(m.group(1))
            if iv is not None:
                if iv not in info["cmp_consts"]:
                    info["cmp_consts"].append(iv)
            continue

    info["has_ewram_lang_pair"] = seen_ewram_base and seen_lang_offset
    if info["has_ewram_lang_pair"]:
        info["has_lang_global"] = True
    info["n_callees"] = len(info["callees"])
    return info


def serialize_list(xs, fmt=str, sep="|", limit=None):
    if limit is not None and len(xs) > limit:
        xs = xs[:limit] + ["..."]
    return sep.join(fmt(x) if x != "..." else "..." for x in xs)


def main():
    if not ALL_S.exists():
        print("ERROR: %s not found" % ALL_S, file=sys.stderr)
        sys.exit(1)
    if not TARGETS_CSV.exists():
        print("ERROR: %s not found" % TARGETS_CSV, file=sys.stderr)
        sys.exit(1)

    print("[load] reading %s ..." % ALL_S)
    text = ALL_S.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    print("[load] %d lines" % len(lines))

    print("[pass1] building label -> value map ...")
    lv_map = build_label_value_map(lines)
    print("[pass1] %d labels with .word/.hword/.byte payload" % len(lv_map))

    print("[pass1] scanning function starts ...")
    func_starts = find_func_starts(lines)
    func_idx_by_addr = {addr: i for i, (_, addr, _) in enumerate(func_starts)}
    print("[pass1] %d functions in all.s" % len(func_starts))

    targets = load_targets()
    print("[targets] %d game_str functions to analyze" % len(targets))

    rows = []
    for addr, fun_lbl, proposed, score, tags in targets:
        if addr not in func_idx_by_addr:
            print("  WARN: 0x%08x not found as FUN_ label in all.s" % addr)
            continue
        fi = func_idx_by_addr[addr]
        line_start = func_starts[fi][0] + 1
        if fi + 1 < len(func_starts):
            line_end = func_starts[fi + 1][0]
        else:
            line_end = len(lines)
        body = lines[line_start:line_end]
        info = analyze_function(addr, body, lv_map)
        info["name"] = fun_lbl
        info["proposed"] = proposed
        info["score"] = score
        info["tags"] = tags
        rows.append(info)

    # 输出 CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "address",
                "name",
                "proposed",
                "score",
                "tags",
                "body_lines",
                "n_instr",
                "n_callees",
                "callees",
                "has_master_table",
                "lang_bases",
                "has_lang_global",
                "n_direct_string_addrs",
                "direct_string_addrs",
                "candidate_ids_imm",
                "small_word_lits",
                "cmp_consts",
                "all_imm_u16",
                "all_word_u16",
                "literal_summary",
            ]
        )
        for info in rows:
            w.writerow(
                [
                    info["address"],
                    info["name"],
                    info["proposed"],
                    info["score"],
                    info["tags"],
                    info["body_lines"],
                    info["n_instr"],
                    info["n_callees"],
                    serialize_list(info["callees"], limit=20),
                    "1" if info["has_master_table"] else "0",
                    serialize_list(info["lang_bases"]),
                    "1" if info["has_lang_global"] else "0",
                    len(info["direct_string_addrs"]),
                    serialize_list(
                        info["direct_string_addrs"], fmt=lambda v: "0x%08x" % v, limit=20
                    ),
                    serialize_list(
                        info["candidate_ids_imm"], fmt=lambda v: str(v), limit=30
                    ),
                    serialize_list(
                        info["small_word_lits"], fmt=lambda v: str(v), limit=30
                    ),
                    serialize_list(info["cmp_consts"], fmt=lambda v: str(v), limit=20),
                    serialize_list(
                        info["all_imm_u16"], fmt=lambda v: "0x%x" % v, limit=60
                    ),
                    serialize_list(
                        info["all_word_u16"], fmt=lambda v: "0x%x" % v, limit=60
                    ),
                    serialize_list(
                        [
                            "%s:%s=%s" % (lbl, cls, val)
                            for lbl, cls, val in info["literal_summary"]
                        ],
                        limit=30,
                    ),
                ]
            )

    print("[done] wrote %s (%d rows)" % (OUT_CSV, len(rows)))

    # 摘要 stdout
    print("\n[summary]")
    n_master = sum(1 for r in rows if r["has_master_table"])
    n_lang = sum(1 for r in rows if r["lang_bases"])
    n_lang_global = sum(1 for r in rows if r["has_lang_global"])
    n_direct = sum(1 for r in rows if r["direct_string_addrs"])
    n_cand_imm = sum(1 for r in rows if r["candidate_ids_imm"])
    print("  master_table ref      : %d / %d" % (n_master, len(rows)))
    print("  lang_base   ref       : %d / %d" % (n_lang, len(rows)))
    print("  lang_global  ref      : %d / %d" % (n_lang_global, len(rows)))
    print("  direct_string_addr    : %d / %d" % (n_direct, len(rows)))
    print("  candidate_ids_imm     : %d / %d" % (n_cand_imm, len(rows)))


if __name__ == "__main__":
    main()
