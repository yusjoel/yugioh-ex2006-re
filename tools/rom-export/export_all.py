#!/usr/bin/env python3
"""
构建前置：从 ROM 导出所有构建所需的图形/数据文件。

运行后产出 graphics/ 和 data/pack-banners.s 等构建依赖文件（均不入库）。
等价于依次运行下列脚本，但统一了工作目录和错误处理。

用法:
    python tools/rom-export/export_all.py
"""

import importlib.util
import os
import sys
import time

# 构建必须的导出脚本（按依赖顺序）
BUILD_REQUIRED = [
    'export_gfx.py',             # opponents + icons + duel-field
    'export_card_images.py',     # card-images-rom (palettes + tiles, 2331 条)
    'export_pack_banners.py',    # pack-banners (51 条 + data/pack-banners.s)
]


def run_script(script_dir, name):
    """动态导入并执行脚本的 main()。"""
    path = os.path.join(script_dir, name)
    if not os.path.exists(path):
        print(f'[SKIP] {name} not found')
        return False

    spec = importlib.util.spec_from_file_location(name.replace('.py', ''), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, 'main'):
        mod.main()
        return True
    else:
        print(f'[SKIP] {name} has no main()')
        return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    rom_path = 'roms/2343.gba'
    if not os.path.exists(rom_path):
        print(f'ERROR: {rom_path} not found. Place the original ROM there first.')
        sys.exit(1)

    print('=' * 60)
    print('  ROM 资产全量导出')
    print('=' * 60)

    t0 = time.time()
    ok = 0
    for name in BUILD_REQUIRED:
        print(f'\n{"─" * 60}')
        print(f'  [{ok+1}/{len(BUILD_REQUIRED)}] {name}')
        print(f'{"─" * 60}')
        if run_script(script_dir, name):
            ok += 1

    elapsed = time.time() - t0
    print(f'\n{"=" * 60}')
    print(f'  完成: {ok}/{len(BUILD_REQUIRED)} 个脚本, 耗时 {elapsed:.1f}s')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
