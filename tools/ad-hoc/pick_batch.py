#!/usr/bin/env python3
"""
pick_batch.py — Select N≤max unanalyzed functions in topo order for batched naming loop.

Strategy: simple sequential pick by topo_idx ascending, skipping A_named/B_runtime classes
and already-analyzed functions (per naming-proposals.csv `name` column).

For each picked function, also extracts:
- function body line range in asm/all.s (start = `^FUN_<addr>:` or `^<name>:`, end = next func label)
- direct callees (from asm body bl <name> instructions; no csv lookup needed)
- ≤5 callers with (addr, tags, name) from complete_callgraph.csv + naming-proposals.csv

Output: JSON to stdout (or --out file). Format:
{
    "batch": [
        {
            "addr": "0x0801950c",
            "topo_idx": 37,
            "depth": 4,
            "indeg": 1,
            "class": "E_specific_low",
            "current_name": "FUN_0801950c",  # or actual name if renamed
            "tags": ["banlist", "settings"],
            "asm_start": 11955,  # line in asm/all.s where ^FUN_0801950c: appears
            "asm_end": 12010,
            "callees": ["refresh_selected_char_obj_tile"],  # from asm body
            "callers": [
                {"addr": "0x08019820", "name": "FUN_08019820", "tags": ["name_input"]},
                ...
            ]
        },
        ...
    ],
    "skipped": ["<reason: addr or addr range>", ...]
}

Usage:
    python tools/ad-hoc/pick_batch.py --max 15 [--out batch.json]
    python tools/ad-hoc/pick_batch.py --root 0x0801950c --max 15  # explicit root
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOPO_CSV = REPO / "temp/closure_topo_order.csv"
CALLGRAPH_CSV = REPO / "temp/complete_callgraph.csv"
NAMING_CSV = REPO / "doc/dev/naming-proposals.csv"
ASM_S = REPO / "asm/all.s"


def load_naming_proposals():
    """addr -> {name, tags}"""
    out = {}
    with open(NAMING_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["address"]] = {
                "name": row["name"],
                "tags": [t for t in row.get("tags", "").split(";") if t],
            }
    return out


def load_topo():
    """list of dicts in topo order"""
    out = []
    with open(TOPO_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(
                {
                    "topo_idx": int(row["topo_idx"]),
                    "addr": row["addr"],
                    "depth": int(row["depth"]),
                    "indeg": int(row["indeg"]),
                    "class": row["class"],
                    "name": row["name"],
                }
            )
    return out


def load_callgraph_callers():
    """callee_addr -> [caller_addr, ...]"""
    out = {}
    with open(CALLGRAPH_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.setdefault(row["callee_addr"], []).append(row["caller_addr"])
    return out


def is_analyzed(name_proposals, addr):
    """Already-analyzed = name col != FUN_<addr> and != SUB_<addr>"""
    if addr not in name_proposals:
        return False
    name = name_proposals[addr]["name"]
    return not (name.startswith("FUN_") or name.startswith("SUB_"))


def find_asm_line_range(asm_lines, addr, current_name):
    """Find line range for function body in asm/all.s.

    Start: ^<current_name>: or ^FUN_<addr_no_0x>:
    End: next function label (next ^[a-zA-Z_][a-zA-Z0-9_]*: in column 1 OR end of file)
    Returns (start_line, end_line) 1-indexed, or (None, None) if not found.
    """
    addr_short = addr[2:]  # strip 0x
    candidates = [
        f"{current_name}:",
        f"FUN_{addr_short}:",
    ]
    label_re = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*:$")

    start = None
    for i, line in enumerate(asm_lines):
        stripped = line.rstrip("\n").rstrip()
        if stripped in candidates:
            start = i + 1  # 1-indexed
            break

    if start is None:
        return None, None

    # find end: next label
    end = len(asm_lines)
    for i in range(start, len(asm_lines)):
        stripped = asm_lines[i].rstrip("\n").rstrip()
        if label_re.match(stripped):
            end = i  # exclusive of label line, but inclusive 1-indexed = i (0-indexed i is line i+1)
            break

    return start, end


def extract_callees_from_asm(asm_lines, start, end):
    """Extract bl/blx target names from asm body."""
    bl_re = re.compile(r"^\s+bl\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(@.*)?$")
    out = set()
    for i in range(start - 1, min(end, len(asm_lines))):
        m = bl_re.match(asm_lines[i])
        if m:
            target = m.group(1)
            # skip pseudo-targets like FUN_xxx
            out.add(target)
    return sorted(out)


def get_callers(addr, callers_map, name_proposals, max_callers=5):
    """Return ≤max caller dicts."""
    callers = callers_map.get(addr, [])
    out = []
    for c_addr in callers[:max_callers]:
        info = name_proposals.get(c_addr, {})
        out.append(
            {
                "addr": c_addr,
                "name": info.get("name", f"FUN_{c_addr[2:]}"),
                "tags": info.get("tags", []),
            }
        )
    return out


def pick_batch(max_n, root_addr=None):
    name_props = load_naming_proposals()
    topo = load_topo()
    callers_map = load_callgraph_callers()

    asm_lines = ASM_S.read_text(encoding="utf-8").splitlines(keepends=True)

    # Filter out A_named (already named) and B_runtime/invoker (not naming targets)
    candidates = [
        t for t in topo
        if t["class"] not in ("A_named",)
        and not t["class"].startswith("B_")
        and not is_analyzed(name_props, t["addr"])
    ]

    # If root specified, find its position in candidates and start there
    if root_addr:
        start_idx = next(
            (i for i, t in enumerate(candidates) if t["addr"] == root_addr), None
        )
        if start_idx is None:
            print(f"ERROR: root {root_addr} not in candidates", file=sys.stderr)
            sys.exit(1)
        candidates = candidates[start_idx:]

    batch_topo = candidates[:max_n]

    batch = []
    skipped = []
    for t in batch_topo:
        addr = t["addr"]
        current_name = name_props.get(addr, {}).get("name", f"FUN_{addr[2:]}")
        tags = name_props.get(addr, {}).get("tags", [])

        start, end = find_asm_line_range(asm_lines, addr, current_name)
        if start is None:
            skipped.append(f"{addr}: asm label not found")
            continue

        callees = extract_callees_from_asm(asm_lines, start, end)
        callers = get_callers(addr, callers_map, name_props)

        batch.append(
            {
                "addr": addr,
                "topo_idx": t["topo_idx"],
                "depth": t["depth"],
                "indeg": t["indeg"],
                "class": t["class"],
                "current_name": current_name,
                "tags": tags,
                "asm_start": start,
                "asm_end": end,
                "callees": callees,
                "callers": callers,
            }
        )

    return {"batch": batch, "skipped": skipped}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=15, help="batch size cap")
    ap.add_argument(
        "--root", default=None, help="explicit root addr (e.g. 0x0801950c)"
    )
    ap.add_argument("--out", default=None, help="output JSON path; default stdout")
    args = ap.parse_args()

    result = pick_batch(args.max, args.root)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(
            f"wrote batch of {len(result['batch'])} (skipped {len(result['skipped'])}) to {args.out}",
            file=sys.stderr,
        )
    else:
        print(output)


if __name__ == "__main__":
    main()
