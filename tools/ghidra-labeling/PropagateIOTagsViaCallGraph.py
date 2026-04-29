# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PropagateIOTagsViaCallGraph.py
#
# 方法论 doc/dev/methodology/function-naming.md §四 (硬件寄存器簇) 的扩展:
# 在 TagFunctionsByIORegs.py 直接 tag 之上, 通过调用图反向传播 family.
#
# 算法:
#   Round 0   "种子"      = 直接命中 IO/PAL/VRAM/OAM 的函数 (depth=0)
#   Round N+1 "传播"      对每个未 tag 函数 F:
#                          - 收集所有"callee 已 tag 且 callee.depth < N+1"的 family
#                          - 若总票数 >= 1, 取多数派 (winner_count * 2 > total_votes)
#                          - 通过则 F.family = winner_fam, F.depth = N+1
#   最多 MAX_DEPTH 轮, 收敛即停 (某轮无新增)
#
# 输出: temp/ghidra-funcs-io-tags-propagated.csv (一行一函数)
#         columns: address, name, family, depth, callee_votes
#         depth 0 = 直接命中, 1+ = 经 N 跳传播
#
# 此脚本 *只读*: 不 createFunction / 不 setName / 不写注释.
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat PropagateIOTagsViaCallGraph.py

import os

from ghidra.util.task import ConsoleTaskMonitor


IO_LO = 0x04000000
IO_HI = 0x04000400
PAL_LO  = 0x05000000
PAL_HI  = 0x05000400
VRAM_LO = 0x06000000
VRAM_HI = 0x06018000
OAM_LO  = 0x07000000
OAM_HI  = 0x07000400

IO_FAMILIES = [
    (0x04000000, 0x04000008, "display"),
    (0x04000008, 0x04000040, "bg"),
    (0x04000040, 0x04000050, "win"),
    (0x04000050, 0x04000058, "blend"),
    (0x04000058, 0x040000B0, "snd"),
    (0x040000B0, 0x04000100, "dma"),
    (0x04000100, 0x04000120, "timer"),
    (0x04000120, 0x04000130, "sio"),
    (0x04000130, 0x04000134, "input"),
    (0x04000134, 0x04000200, "sio"),
    (0x04000200, 0x04000400, "sys"),
]

MAX_DEPTH = 10


def family_for(addr_int):
    if PAL_LO <= addr_int < PAL_HI:
        return "pal"
    if VRAM_LO <= addr_int < VRAM_HI:
        return "vram"
    if OAM_LO <= addr_int < OAM_HI:
        return "obj"
    if not (IO_LO <= addr_int < IO_HI):
        return None
    for lo, hi, fname in IO_FAMILIES:
        if lo <= addr_int < hi:
            return fname
    return "io"


def repo_root():
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def main():
    fm = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()
    monitor = ConsoleTaskMonitor()

    # === Step 1: 收集函数 + 直接 tag ===
    print("== Step 1: direct IO tagging (depth=0) ==")
    funcs = []
    it = fm.getFunctions(True)
    while it.hasNext():
        funcs.append(it.next())

    func_by_ep = {}
    direct_tag = {}

    for f in funcs:
        ep_int = f.getEntryPoint().getOffset() & 0xFFFFFFFF
        func_by_ep[ep_int] = f
        body = f.getBody()
        if body is None:
            continue
        family_hit = {}
        instr_iter = listing.getInstructions(body, True)
        while instr_iter.hasNext():
            instr = instr_iter.next()
            for ref in instr.getReferencesFrom():
                ta = ref.getToAddress()
                if ta is None:
                    continue
                ta_int = ta.getOffset() & 0xFFFFFFFF
                fam = family_for(ta_int)
                if fam is None:
                    continue
                family_hit[fam] = family_hit.get(fam, 0) + 1
        if family_hit:
            primary = sorted(family_hit.items(), key=lambda x: -x[1])[0][0]
            direct_tag[ep_int] = primary

    print("  direct tagged = %d / %d" % (len(direct_tag), len(funcs)))

    # === Step 2: 建 call graph ===
    print("\n== Step 2: building call graph ==")
    call_out = {}
    for f in funcs:
        ep_int = f.getEntryPoint().getOffset() & 0xFFFFFFFF
        callees = f.getCalledFunctions(monitor)
        callee_set = set()
        for c in callees:
            c_ep = c.getEntryPoint().getOffset() & 0xFFFFFFFF
            if c_ep in func_by_ep:
                callee_set.add(c_ep)
        call_out[ep_int] = callee_set

    n_with_callees = len([s for s in call_out.values() if s])
    total_edges = sum([len(s) for s in call_out.values()])
    avg = (float(total_edges) / len(call_out)) if call_out else 0.0
    print("  funcs with >=1 callee = %d" % n_with_callees)
    print("  total edges           = %d" % total_edges)
    print("  avg out-degree        = %.2f" % avg)

    # === Step 3: 迭代传播 ===
    print("\n== Step 3: propagation ==")
    tags = {}
    for ep, fam in direct_tag.items():
        tags[ep] = (fam, 0, 0)

    for depth in range(1, MAX_DEPTH + 1):
        added = 0
        new_tags = {}
        for ep_int in func_by_ep:
            if ep_int in tags:
                continue
            callees = call_out.get(ep_int, set())
            if not callees:
                continue
            votes = {}
            for c_ep in callees:
                if c_ep not in tags:
                    continue
                c_fam, c_depth, _ = tags[c_ep]
                if c_depth >= depth:
                    continue
                votes[c_fam] = votes.get(c_fam, 0) + 1
            if not votes:
                continue
            sorted_v = sorted(votes.items(), key=lambda x: -x[1])
            winner_fam, winner_count = sorted_v[0]
            total_votes = sum(votes.values())
            if winner_count * 2 <= total_votes:
                continue  # 严格多数 (>50%, 不含平局)
            new_tags[ep_int] = (winner_fam, depth, winner_count)
            added += 1
        tags.update(new_tags)
        print("  round %d  +%-4d  cumulative %d / %d" % (
            depth, added, len(tags), len(funcs)))
        if added == 0:
            print("  收敛")
            break

    # === Step 4: 输出 ===
    out_dir = os.path.join(repo_root(), "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    csv_path = os.path.join(out_dir, "ghidra-funcs-io-tags-propagated.csv")

    fcsv = open(csv_path, "w")
    fcsv.write("address,name,family,depth,callee_votes\n")
    by_family = {}
    by_depth = {}
    named_per_fam_dep = {}  # (fam, dep) -> [(name, addr)]
    for ep_int in sorted(func_by_ep.keys()):
        f = func_by_ep[ep_int]
        name = f.getName()
        if ep_int in tags:
            fam, dep, contrib = tags[ep_int]
            by_family[fam] = by_family.get(fam, 0) + 1
            by_depth[dep] = by_depth.get(dep, 0) + 1
            fcsv.write("0x%08x,%s,%s,%d,%d\n" % (ep_int, name, fam, dep, contrib))
            if not (name.startswith("FUN_") or name.startswith("SUB_") or name.startswith("thunk_FUN_")):
                named_per_fam_dep.setdefault((fam, dep), []).append((name, ep_int))
        else:
            fcsv.write("0x%08x,%s,,,0\n" % (ep_int, name))
    fcsv.close()

    print("\n[done] PropagateIOTagsViaCallGraph")
    print("  total funcs   = %d" % len(funcs))
    print("  tagged        = %d (%.1f%%)" % (
        len(tags), 100.0 * len(tags) / len(funcs) if funcs else 0))
    print("\n  -- by family --")
    for fam in sorted(by_family.keys(), key=lambda k: -by_family[k]):
        print("    %-10s = %4d" % (fam, by_family[fam]))
    print("\n  -- by depth --")
    for dep in sorted(by_depth.keys()):
        label = "direct" if dep == 0 else "via depth %d callees" % (dep - 1)
        print("    depth %d  = %4d  (%s)" % (dep, by_depth[dep], label))

    # Sanity check: 已命名函数的 depth 0/1 分布
    print("\n  -- 已命名函数 propagation 后 family/depth --")
    for (fam, dep) in sorted(named_per_fam_dep.keys()):
        items = named_per_fam_dep[(fam, dep)]
        print("    [%s, depth=%d] %d 个:" % (fam, dep, len(items)))
        for nm, a in items[:5]:
            print("      0x%08x  %s" % (a, nm))
        if len(items) > 5:
            print("      ... +%d" % (len(items) - 5))

    print("\n  -> %s" % csv_path)


main()
