#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_ready_phase12.py

重算 Phase 12 ready 集合并锁定批次清单 (Phase 5 完成后重算).

ready 定义: unnamed AND (no callees OR all callees named)
  - unnamed: temp/ghidra-functions.csv source == DEFAULT (即仍是 FUN_/SUB_/auto)
  - named:   source != DEFAULT
  - callees: temp/ghidra-funcs-callgraph.csv (caller_addr,callee_addr), 排除 self-edge

输出:
  temp/ready_addrs_phase12.txt          (升序地址清单, 每行一个)
  doc/dev/eval/ready_batches_phase12.json (20/批锁定清单)
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FUNCS = os.path.join(ROOT, "temp", "ghidra-functions.csv")
CALLGRAPH = os.path.join(ROOT, "temp", "ghidra-funcs-callgraph.csv")
OUT_TXT = os.path.join(ROOT, "temp", "ready_addrs_phase12.txt")
OUT_JSON = os.path.join(ROOT, "doc", "dev", "eval", "ready_batches_phase12.json")

BATCH_SIZE = 20
FIRST_BATCH_IDX = 217  # Phase 11 ended at #216

# --- load naming status ---
named = {}   # addr(int) -> bool (True=named)
with open(FUNCS, newline="") as f:
    for row in csv.DictReader(f):
        a = int(row["address"], 16)
        named[a] = (row["source"] != "DEFAULT")

# --- load callgraph (callees per caller) ---
callees = {}  # caller(int) -> set(callee int)
with open(CALLGRAPH, newline="") as f:
    for row in csv.DictReader(f):
        c = int(row["caller_addr"], 16)
        e = int(row["callee_addr"], 16)
        if c == e:
            continue
        callees.setdefault(c, set()).add(e)

# --- compute indegree for reporting ---
indeg = {}
for c, es in callees.items():
    for e in es:
        indeg[e] = indeg.get(e, 0) + 1

# --- ready set ---
ready = []
for a in sorted(named):
    if named[a]:
        continue  # already named
    cs = callees.get(a, set())
    if all(named.get(e, True) for e in cs):
        ready.append(a)

print("[compute] total functions   = %d" % len(named))
print("[compute] named             = %d" % sum(1 for v in named.values() if v))
print("[compute] unnamed FUN_*      = %d" % sum(1 for v in named.values() if not v))
print("[compute] ready (Phase 12)    = %d" % len(ready))

# indeg distribution of ready
buckets = {"0":0, "1-2":0, "3-5":0, "6-10":0, "11+":0}
for a in ready:
    d = indeg.get(a, 0)
    if d == 0: buckets["0"] += 1
    elif d <= 2: buckets["1-2"] += 1
    elif d <= 5: buckets["3-5"] += 1
    elif d <= 10: buckets["6-10"] += 1
    else: buckets["11+"] += 1
print("[compute] ready indeg dist   = %s" % buckets)

# top indeg hubs in ready
hubs = sorted(((indeg.get(a,0), a) for a in ready), reverse=True)[:10]
print("[compute] top indeg hubs:")
for d, a in hubs:
    print("    indeg=%-3d 0x%08x" % (d, a))

# blocked unnamed (not ready) count
blocked = sum(1 for a in named if not named[a] and a not in set(ready))
print("[compute] blocked unnamed    = %d" % blocked)

# --- write addr list ---
with open(OUT_TXT, "w") as f:
    for a in ready:
        f.write("0x%08x\n" % a)

# --- batch into groups of 20 ---
batches = []
for i in range(0, len(ready), BATCH_SIZE):
    chunk = ready[i:i+BATCH_SIZE]
    batches.append({
        "batch_idx": FIRST_BATCH_IDX + len(batches),
        "addrs": ["0x%08x" % a for a in chunk],
    })

meta = {
    "generated": "2026-06-03",
    "phase": 12,
    "mode": "20/batch, single sub-agent per phase (serial executor/reviewer/fixer/lesson-keeper)",
    "criterion": "unnamed AND (no callees OR all callees named); set locked at Phase 12 start (recomputed after Phase 5 named 164)",
    "source_addr_list": "temp/ready_addrs_phase12.txt",
    "callgraph_source": "temp/ghidra-funcs-callgraph.csv (2026-05-31, 4641 fns / 13158 edges)",
    "total_ready": len(ready),
    "total_batches": len(batches),
    "batch_size": BATCH_SIZE,
    "addr_range": ["0x%08x" % ready[0], "0x%08x" % ready[-1]] if ready else [],
    "first_batch_idx": FIRST_BATCH_IDX,
    "indeg_dist": buckets,
    "blocked_unnamed": blocked,
}

with open(OUT_JSON, "w") as f:
    json.dump({"meta": meta, "batches": batches}, f, indent=2)

print("[done] wrote %s (%d addrs)" % (OUT_TXT, len(ready)))
print("[done] wrote %s (%d batches, #%d..#%d)" % (
    OUT_JSON, len(batches), FIRST_BATCH_IDX, FIRST_BATCH_IDX + len(batches) - 1))
