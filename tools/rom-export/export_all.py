#!/usr/bin/env python3
"""
一键从 ROM 导出全部构建所需的 data/*.s 和 graphics/* 资产。

用法:
    python tools/rom-export/export_all.py

注意事项:
- export_card_data.py 必须最先跑（生成 card-names.s，其他 7 个脚本依赖它）。
- 其余脚本相互独立，按稳定顺序执行。
"""

import importlib.util
import os
import sys
import time

# 按依赖顺序执行
EXPORT_PIPELINE = [
    # Step 1: 前置依赖（card-names.s 是后续 7 个脚本的输入）
    'export_card_data.py',              # data/card-names.s (名字池 + 指针表) + card-stats.s

    # Step 2: 独立脚本（只读 ROM）
    'export_gfx.py',                    # graphics/{opponents,icons,duel-field}/*
    'export_card_passcodes.py',         # data/card-passcodes.s（加密密码表, 2098×u32, LCG-XOR）
    'export_card_descriptions.py',      # data/card-descriptions.s (merged: ET + special + offset table + anchors)
    'export_game_strings.py',           # data/game-strings-{en,de,fr,it,es}.s
    'export_file_paths.py',             # data/file-paths.s
    'export_fs_tables.py',              # data/fs-tables.s
    'export_fs_files.py',               # fs/<orig path> + data/fs-payload.s（338 个 FS 文件）
    'export_nns_unpacked.py',           # fs-decompressed/**/*.{nanr,ncer,ncgr,nclr}（63 个解压 NNS）
    'export_lz5bg_unpacked.py',         # fs-decompressed/**/*.gbtn（26 个解压 NTBG BG 容器）
    'render_gbtn.py',                   # graphics/images/gbtn-previews/**/*.png（26 个 .gbtn BG 层预览）
    'export_nns_parsed.py',             # graphics/fs-nns/*.{json,png} (NNS parser + palette/tile PNG)
    'export_fs_ui_name_pass.py',        # graphics/images/fs-ui/name_*, pass_* (cell 合成)
    'export_fs_ui_demos.py',            # graphics/images/fs-ui/demo_* (cutscene cells + NANR 关键帧)
    'export_fs_ui_titles.py',           # graphics/images/fs-ui/title_<lang>_* (6 语言 OBJ 层)
    'export_duel_puzzles_v2.py',        # data/duel-puzzles-v2.s（35 个决斗谜题，结构化 INI 文本）
    'export_ydc_structured.py',         # data/ydc-all.s + ydc-index.json（215 个 .ydc 头部+体+尾结构化）
    'export_font.py',                   # data/font.s + graphics/font/*
    'export_pack_banners.py',           # data/pack-banners.s + graphics/pack-banners/*
    'export_card_mini_frame.py',        # data/card-mini-frame{,-palette}.s + graphics/{bin,images}/card-mini-frame/*
    'export_card_medium_frame.py',      # data/card-medium-frame.s + graphics/{bin,images}/card-medium-frame/*
    'export_ui_sheets.py',              # graphics/{bin,images}/ui-misc/* (HUD/state/switch sheets + aux palettes)
    'export_deck_strings.py',           # data/deck-strings.s

    # Step 3: 依赖 card-names.s 的脚本
    'export_card_images.py',            # data/card-image-* + cards-ids-array.s + graphics/card-images-rom/
    'export_pack_card_lists.py',        # data/pack-card-lists.s
    'export_banlists.py',               # data/banlists.s
    'export_starter_deck.py',           # data/starter-deck.s
    'export_struct_decks.py',           # data/struct-decks.s
    'export_opponent_card_values.py',   # data/opponent-card-values.s
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

    os.makedirs('data', exist_ok=True)
    os.makedirs('graphics', exist_ok=True)

    print('=' * 60)
    print('  ROM 资产全量导出')
    print('=' * 60)

    t0 = time.time()
    ok = 0
    for name in EXPORT_PIPELINE:
        print(f'\n{"─" * 60}')
        print(f'  [{ok+1}/{len(EXPORT_PIPELINE)}] {name}')
        print(f'{"─" * 60}')
        os.chdir(project_root)  # 保险：每个脚本前 chdir 回根
        if run_script(script_dir, name):
            ok += 1

    elapsed = time.time() - t0
    print(f'\n{"=" * 60}')
    print(f'  完成: {ok}/{len(EXPORT_PIPELINE)} 个脚本, 耗时 {elapsed:.1f}s')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
