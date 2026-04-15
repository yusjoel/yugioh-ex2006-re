"""扫 asm/all.s，找"把 0x86 写入 BG0CNT(0x04000008) 的函数"。

指纹定义（保守版）：
  函数体内同时含：
    1) 字面量 `.word 0x04000008`（BG0CNT 地址）
    2) `movs Rx, #0x86`（立即数 0x86）
    3) 紧随 movs 的 `strh Rx, [Ry]`（半字写入）
  且 2) 的 movs 与 3) 的 strh 行号相邻（间隔 ≤ 2 行，允许中间插一条 ldr）

输出所有命中函数与行号，验证 FUN_0801d45c 是否（接近）唯一。
"""
from __future__ import annotations
import re
from pathlib import Path

ASM = Path("asm/all.s")

FUN_RE = re.compile(r"^(FUN_[0-9a-f]{8}):")
LIT_BG0CNT = re.compile(r"\.word\s+0x04000008\b")
MOVS_86 = re.compile(r"\bmovs\s+r(\d+)\s*,\s*#0x86\b")
STRH = re.compile(r"\bstrh\s+r(\d+)\s*,\s*\[r(\d+)")

def main() -> None:
    lines = ASM.read_text(encoding="utf-8", errors="replace").splitlines()

    # 1) 划分函数范围
    fun_starts: list[tuple[int, str]] = []
    for i, ln in enumerate(lines):
        m = FUN_RE.match(ln)
        if m:
            fun_starts.append((i, m.group(1)))
    fun_starts.append((len(lines), "<EOF>"))
    ranges = [
        (fun_starts[k][1], fun_starts[k][0], fun_starts[k + 1][0])
        for k in range(len(fun_starts) - 1)
    ]

    print(f"asm/all.s 行数: {len(lines):,}  函数数: {len(ranges):,}\n")

    # 2) 全局统计单独指纹
    n_bg0cnt = sum(1 for ln in lines if LIT_BG0CNT.search(ln))
    n_movs86 = sum(1 for ln in lines if MOVS_86.search(ln))
    print(f"全 ROM `.word 0x04000008` 出现: {n_bg0cnt} 处")
    print(f"全 ROM `movs Rx,#0x86` 出现:    {n_movs86} 处\n")

    # 3) 三条件联合筛选
    # 对每个函数体做一次扫描
    hits = []
    for name, s, e in ranges:
        body = lines[s:e]
        has_bg0cnt = any(LIT_BG0CNT.search(ln) for ln in body)
        if not has_bg0cnt:
            continue

        # 找所有 movs Rx,#0x86 及紧邻 strh Rx,[Ry]
        sequence_matches = []
        for i, ln in enumerate(body):
            m = MOVS_86.search(ln)
            if not m:
                continue
            rx = m.group(1)
            # 向下看至多 2 行，找 strh rX, [...]
            for j in range(i + 1, min(i + 3, len(body))):
                sm = STRH.search(body[j])
                if sm and sm.group(1) == rx:
                    sequence_matches.append((s + i + 1, s + j + 1))  # 1-indexed
                    break
        if sequence_matches:
            hits.append((name, s + 1, e, sequence_matches))

    # 4) 输出
    print(f"同时满足三条件（含 0x04000008 字面量 + movs 0x86 + 紧邻 strh）的函数: {len(hits)}\n")
    for name, fs, fe, seqs in hits:
        print(f"  {name}  (行 {fs}..{fe - 1}, size={fe - fs})")
        for mv, sh in seqs:
            print(f"      movs #0x86 @ 行 {mv}   strh @ 行 {sh}")

    # 5) 仅按"movs 0x86 + 紧邻 strh"筛一遍（忽略 0x04000008 字面量要求），
    #    看放宽后有多少假阳性
    loose = []
    for name, s, e in ranges:
        body = lines[s:e]
        for i, ln in enumerate(body):
            m = MOVS_86.search(ln)
            if not m:
                continue
            rx = m.group(1)
            for j in range(i + 1, min(i + 3, len(body))):
                sm = STRH.search(body[j])
                if sm and sm.group(1) == rx:
                    loose.append(name)
                    break
            else:
                continue
            break
    loose = sorted(set(loose))
    print(f"\n仅用 movs+strh 指纹（不要求 0x04000008 字面量）命中函数: {len(loose)}")
    if len(loose) <= 20:
        for n in loose:
            print(f"  {n}")


if __name__ == "__main__":
    main()
