# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RenameFromCSV.py  (2026-05-16)
#
# CSV-driven 替代 RenameKnownFunctions.py + RenameBatch<N>.py.
# 不再每批新建 Python 脚本; 数据真相源:
#   - doc/dev/naming-proposals.csv  `name` 列 (canonical, address -> 当前已 landed 的名字)
#   - doc/dev/eval/<addr>.plate.txt (ASCII plate, fixer 落地时产出, 一函数一文件)
#
# 注: CSV 第 3 列 proposed_name 是早期 tagging 阶段的 stub 提案 (category prefix:
# font_jp_/card_ids_/prng_ 等), 本脚本忽略, 仅以第 2 列 name 为准.
#
# 处理逻辑 (幂等):
#   1. 读 CSV, 收集 address+name (name 非空且非 FUN_/SUB_ 前缀才是真名)
#   2. 对每个候选, 看 .rep 中该地址符号:
#      - 已是 CSV name -> 跳过 (idempotent)
#      - 不是, 但 plate.txt 文件存在 -> rename + 写 plate
#      - 不是, 但 plate.txt 缺失 -> 报错 (不静默错过); 仅历史已 landed 函数不会到这分支
#   3. plate 写入: 仅在 .rep 当前无 plate 或 user-rename 时覆盖 (保护手编内容)
#
# 历史 (1147+21=1168 函数) 已经在 .rep 内 rename + plate; 本脚本只处理 batch #64 起.
# 旧批次 disaster recovery: 先跑 RenameKnownFunctions.py + RenameBatch63.py, 再跑本脚本.
#
# Usage:
#   ghidra-run-script.bat RenameFromCSV.py            # 应用 (默认非 dry)
#   ghidra-run-script.bat RenameFromCSV.py dry        # dry-run, 不写

import os

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


# Repo paths (脚本作为 Ghidra script 跑时, cwd = SCRIPT_DIR, 用 .. 推 repo root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")
EVAL_DIR = os.path.join(REPO_ROOT, "doc", "dev", "eval")


def load_csv_candidates():
    """Return list of (addr_str_lower, name) for rows where col 2 'name' is a real custom name
    (non-empty, not FUN_/SUB_ prefix). proposed_name col 3 是 early-tagging stub, 忽略."""
    out = []
    f = open(CSV_PATH, "rb")
    try:
        raw = f.read().decode("utf-8")
    finally:
        f.close()
    lines = raw.splitlines()
    if not lines:
        return out
    header = lines[0].split(",")
    if header[:3] != ["address", "name", "proposed_name"]:
        raise RuntimeError("Unexpected CSV header: %s" % header)
    for line in lines[1:]:
        cols = line.split(",")
        if len(cols) < 2:
            continue
        addr = cols[0].strip().lower()
        name = cols[1].strip()
        if not name:
            continue
        if name.startswith("FUN_") or name.startswith("SUB_"):
            continue
        if not addr.startswith("0x"):
            continue
        out.append((addr, name))
    return out


def load_plate(addr):
    """Read doc/dev/eval/<addr_8hex>.plate.txt as unicode. Return None if missing."""
    addr_hex = addr[2:] if addr.startswith("0x") else addr
    path = os.path.join(EVAL_DIR, addr_hex + ".plate.txt")
    if not os.path.exists(path):
        return None
    f = open(path, "rb")
    try:
        raw = f.read()
    finally:
        f.close()
    # plate.txt 是 ASCII; 用 utf-8 decode 兼容 (BOM 也行)
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    return raw.decode("utf-8").rstrip()


def apply_rename(addr, desired_name, fm, st, listing, space):
    """Idempotent rename + plate for one entry. Returns 'ok'/'skip'/'fail'."""
    addr_int = int(addr, 16)
    ghidra_addr = space.getAddress(addr_int)
    func = fm.getFunctionAt(ghidra_addr)
    if func is None:
        print("[skip ] no function at %s" % addr)
        return "skip"

    current_name = func.getName()
    needs_rename = (current_name != desired_name)

    plate_text = load_plate(addr)
    cu = listing.getCodeUnitAt(func.getEntryPoint())
    existing_plate = cu.getComment(CodeUnit.PLATE_COMMENT) if cu is not None else None
    needs_plate_write = (plate_text is not None and (needs_rename or not existing_plate))

    if not needs_rename and not needs_plate_write:
        return "skip"

    if needs_rename and plate_text is None:
        # rename 需要落地但没有 plate.txt -> 严格失败 (新批次必须先 fixer 写 plate.txt)
        print("[fail] %s: needs rename '%s' -> '%s' but plate.txt missing" %
              (addr, current_name, desired_name))
        return "fail"

    if RUN_DRY:
        print("[dry ] %s: '%s' -> '%s' (plate: %s)" %
              (addr, current_name, desired_name, "yes" if needs_plate_write else "no"))
        return "ok"

    if needs_rename:
        try:
            func.getSymbol().setName(desired_name, SourceType.USER_DEFINED)
        except Exception as e:
            print("[fail] rename %s -> %s: %s" % (current_name, desired_name, e))
            return "fail"

    if needs_plate_write and cu is not None:
        try:
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        except Exception as e:
            print("[warn] plate %s: %s" % (desired_name, e))

    print("[ok  ] %s: %s -> %s" % (addr, current_name, desired_name))
    return "ok"


def main():
    candidates = load_csv_candidates()
    print("[info] CSV candidates with proposed_name: %d" % len(candidates))

    space = currentProgram.getAddressFactory().getDefaultAddressSpace()
    st = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()

    n_ok = 0
    n_skip = 0
    n_fail = 0
    for addr, proposed in candidates:
        result = apply_rename(addr, proposed, fm, st, listing, space)
        if result == "ok":
            n_ok += 1
        elif result == "skip":
            n_skip += 1
        else:
            n_fail += 1
    print("[done] RenameFromCSV: ok=%d skip=%d fail=%d total=%d" %
          (n_ok, n_skip, n_fail, len(candidates)))


main()
