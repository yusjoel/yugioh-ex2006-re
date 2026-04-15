"""扫 asm/all.s 里所有 `.word 0x06004000`，输出每处所属的 FUN_ 及粗略特征。

用途：验证"0x06004000 这个字面量在 ROM 里出现次数有限，且含大循环+读 ROM 基址的
候选函数唯一收敛到 FUN_0801d290"这一说法。
"""
from __future__ import annotations
import re
from pathlib import Path

ASM = Path("asm/all.s")
TARGET = "0x06004000"

FUN_RE = re.compile(r"^(FUN_[0-9a-f]{8}):")
LIT_RE = re.compile(rf"\.word\s+{re.escape(TARGET)}\b")
ROM_LIT_RE = re.compile(r"\.word\s+0x0[89a-f][0-9a-f]{6}\b")  # ROM 地址字面量
LOOP_B_RE = re.compile(r"\b(bls|bcc|bne|bhi|ble|blt)\s+LAB_[0-9a-f]{8}\b")

def main() -> None:
    lines = ASM.read_text(encoding="utf-8", errors="replace").splitlines()

    # 1) 建立 "行号 → 所属函数名、函数起止行" 映射
    fun_starts: list[tuple[int, str]] = []
    for i, ln in enumerate(lines):
        m = FUN_RE.match(ln)
        if m:
            fun_starts.append((i, m.group(1)))
    fun_starts.append((len(lines), "<EOF>"))

    def owner_of(line_idx: int) -> tuple[str, int, int]:
        # 二分也行，线性够用
        for k in range(len(fun_starts) - 1):
            s, name = fun_starts[k]
            e, _ = fun_starts[k + 1]
            if s <= line_idx < e:
                return name, s, e
        return "<none>", 0, 0

    # 2) 找到所有命中
    hits: list[int] = [i for i, ln in enumerate(lines) if LIT_RE.search(ln)]

    print(f"asm/all.s 行数: {len(lines):,}")
    print(f"FUN_ 标签总数: {len(fun_starts) - 1}")
    print(f"`.word {TARGET}` 出现: {len(hits)} 处\n")

    # 3) 按所属函数聚合
    per_fun: dict[str, list[int]] = {}
    for h in hits:
        name, _, _ = owner_of(h)
        per_fun.setdefault(name, []).append(h)

    print(f"涉及独立函数数: {len(per_fun)}\n")
    print(f"{'函数名':<22} {'函数大小(行)':>12} {'命中行号':>10} {'该函数ROM字面量数':>18} {'循环跳转数':>10}")
    print("-" * 80)

    rows = []
    for name, hs in per_fun.items():
        # 找该函数的范围
        _, s, e = owner_of(hs[0])
        body = lines[s:e]
        rom_lits = sum(1 for ln in body if ROM_LIT_RE.search(ln))
        loops = sum(1 for ln in body if LOOP_B_RE.search(ln))
        rows.append((name, e - s, hs, rom_lits, loops))

    # 按"函数大小 + ROM 字面量数"降序，大函数 + 多 ROM 字面量 ≈ 资源加载器候选
    rows.sort(key=lambda r: (r[3], r[1]), reverse=True)

    for name, size, hs, rom_lits, loops in rows:
        hstr = ",".join(str(h + 1) for h in hs)  # 1-indexed，方便对照编辑器
        print(f"{name:<22} {size:>12,} {hstr:>10} {rom_lits:>18} {loops:>10}")

    # 4) 再按"大循环 + 多 ROM 字面量"筛一遍作为强候选
    print("\n=== 强候选（ROM 字面量 ≥ 8 且 循环 ≥ 4） ===")
    strong = [r for r in rows if r[3] >= 8 and r[4] >= 4]
    for name, size, hs, rom_lits, loops in strong:
        print(f"  {name}  size={size}  rom_lits={rom_lits}  loops={loops}")
    print(f"强候选数: {len(strong)}")


if __name__ == "__main__":
    main()
