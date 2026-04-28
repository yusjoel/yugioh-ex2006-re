#!/usr/bin/env python3
r"""比较 temp\<dir>\ 与 .\<dir>\ 是否字节级一致 (round-trip 验证).

clean-all.bat 把 data/fs/fs-decompressed/graphics/text 五个导出目录移到 temp\,
build-all.bat 重新导出后调本脚本, 验证重建内容是否与 temp\ baseline 字节级相同.

退出码: 0 = 全部一致, 1 = 至少一个目录有差异.
"""
import os
import sys
import hashlib

DIRS = ['data', 'fs', 'fs-decompressed', 'graphics', 'text']
SHOW_LIMIT = 20  # 每类差异最多打印多少条


def hash_file(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(64 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def walk_files(root):
    """{rel_posix_path: abs_path}"""
    out = {}
    for dp, _, fns in os.walk(root):
        for f in fns:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace('\\', '/')
            out[rel] = full
    return out


def compare(name):
    temp_dir = os.path.join('temp', name)
    cur_dir = name

    if not os.path.isdir(temp_dir):
        print(f'[SKIP] {name}: temp\\{name} 不存在 (clean-all 未跑过?)')
        return True
    if not os.path.isdir(cur_dir):
        print(f'[FAIL] {name}: 当前 {name}\\ 不存在')
        return False

    a = walk_files(temp_dir)
    b = walk_files(cur_dir)
    only_temp = sorted(set(a) - set(b))
    only_cur = sorted(set(b) - set(a))
    common = set(a) & set(b)
    diffs = []
    for rel in sorted(common):
        if hash_file(a[rel]) != hash_file(b[rel]):
            diffs.append(rel)

    if not (only_temp or only_cur or diffs):
        print(f'[OK]   {name}: {len(common)} files identical')
        return True

    print(f'[FAIL] {name}: '
          f'+{len(only_cur)} -{len(only_temp)} ~{len(diffs)} '
          f'(共 {len(common) + len(only_cur)} cur / {len(common) + len(only_temp)} temp)')
    for r in only_temp[:SHOW_LIMIT]:
        print(f'  - only in temp:  {r}')
    if len(only_temp) > SHOW_LIMIT:
        print(f'  - ... +{len(only_temp) - SHOW_LIMIT} more')
    for r in only_cur[:SHOW_LIMIT]:
        print(f'  + only in cur:   {r}')
    if len(only_cur) > SHOW_LIMIT:
        print(f'  + ... +{len(only_cur) - SHOW_LIMIT} more')
    for r in diffs[:SHOW_LIMIT]:
        print(f'  ~ differs:       {r}')
    if len(diffs) > SHOW_LIMIT:
        print(f'  ~ ... +{len(diffs) - SHOW_LIMIT} more')
    return False


def main():
    print()
    print('=' * 60)
    print('  Round-trip 验证: temp\\<dir>\\ vs .\\<dir>\\')
    print('=' * 60)
    ok = True
    for d in DIRS:
        if not compare(d):
            ok = False
    print()
    if ok:
        print('全部 5 个目录 byte-identical')
        sys.exit(0)
    else:
        print('至少 1 个目录有差异')
        sys.exit(1)


if __name__ == '__main__':
    main()
