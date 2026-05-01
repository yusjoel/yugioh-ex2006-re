#!/usr/bin/env python3
"""
一键从 ROM 导出全部构建所需的 data/*.s 和 graphics/* 资产, 并刷新 text/ UTF-8 源.

用法:
    python tools/rom-export/export_all.py

流程:
- Step 1-3: ROM → data/*.s, graphics/*, fs/*, fs-decompressed/*
- Step 4:   data/<text-dataset>.s → text/<text-dataset>/*.txt (UTF-8 源, 刷新)
            ⚠ 覆盖 text/ 当前内容; 若已手编辑 text/ 文件, 跑前先备份.
- Step 5:   text/<text-dataset>/*.txt → data/<text-dataset>.s (重编码 = build 流程)
            验证 text/ ↔ data/ 闭环 (此步等价 build.bat 的 encoder 部分).

注意事项:
- export_card_data.py 必须最先跑（生成 card-names.s，其他 7 个脚本依赖它）。
- 其余脚本相互独立，按稳定顺序执行。
- Step 4/5 依赖 codetable.json (tools/jp-decode/) 已建好.
- Step 5 跑完后 data/<text-dataset>.s 应与 Step 1-3 的输出 byte-identical.
"""

import importlib.util
import os
import sys
import time

# 按依赖顺序执行 — (路径前缀, 脚本名) 形式; 路径前缀以 tools/ 为根
# None = tools/rom-export/, 其他值 = tools/<dir>/
EXPORT_PIPELINE = [
    # Step 1: 前置依赖（card-names.s 是后续 7 个脚本的输入）
    (None, 'export_card_data.py'),              # data/card-names.s (名字池 + 指针表) + card-stats.s

    # Step 2: 独立脚本（只读 ROM）
    (None, 'export_gfx.py'),                    # graphics/{opponents,icons,duel-field}/*
    (None, 'export_card_passcodes.py'),         # data/card-passcodes.s（加密密码表, 2098×u32, LCG-XOR）
    (None, 'export_card_descriptions.py'),      # data/card-descriptions.s (merged: ET + special + offset table + anchors)
    (None, 'export_game_strings.py'),           # data/game-strings-{en,de,fr,it,es}.s
    (None, 'export_file_paths.py'),             # data/file-paths.s
    (None, 'export_fs_tables.py'),              # data/fs-tables.s
    (None, 'export_fs_files.py'),               # fs/<orig path> + data/fs-payload.s（338 个 FS 文件）
    (None, 'export_nns_unpacked.py'),           # fs-decompressed/**/*.{nanr,ncer,ncgr,nclr}（63 个解压 NNS）
    (None, 'export_lz5bg_unpacked.py'),         # fs-decompressed/**/*.gbtn（26 个解压 NTBG BG 容器）
    (None, 'render_gbtn.py'),                   # graphics/images/gbtn-previews/**/*.png（26 个 .gbtn BG 层预览）
    (None, 'export_nns_parsed.py'),             # graphics/fs-nns/*.{json,png} (NNS parser + palette/tile PNG)
    (None, 'export_fs_ui_name_pass.py'),        # graphics/images/fs-ui/name_*, pass_* (cell 合成)
    (None, 'export_fs_ui_demos.py'),            # graphics/images/fs-ui/demo_* (cutscene cells + NANR 关键帧)
    (None, 'export_fs_ui_titles.py'),           # graphics/images/fs-ui/title_<lang>_* (6 语言 OBJ 层)
    (None, 'export_duel_puzzles_v2.py'),        # data/duel-puzzles-v2.s（35 个决斗谜题，结构化 INI 文本）
    (None, 'export_ydc_structured.py'),         # data/ydc-all.s + ydc-index.json（215 个 .ydc 头部+体+尾结构化）
    (None, 'export_font.py'),                   # data/font.s + graphics/font/*
    (None, 'export_font_jp.py'),                # graphics/{bin,images}/font-jp/* (4 charset 变体)
    (None, 'export_pack_banners.py'),           # data/pack-banners.s + graphics/pack-banners/*
    (None, 'export_card_mini_frame.py'),        # data/card-mini-frame{,-palette}.s + graphics/{bin,images}/card-mini-frame/*
    (None, 'export_card_medium_frame.py'),      # data/card-medium-frame.s + graphics/{bin,images}/card-medium-frame/*
    (None, 'export_ui_sheets.py'),              # graphics/{bin,images}/ui-misc/* (HUD/state/switch sheets + aux palettes)
    (None, 'export_deck_strings.py'),           # data/game-strings-ja.s

    # Step 3: 依赖 card-names.s 的脚本
    (None, 'export_card_images.py'),            # data/card-image-* + cards-ids-array.s + graphics/card-images-rom/
    (None, 'export_pack_card_lists.py'),        # data/pack-card-lists.s
    (None, 'export_banlists.py'),               # data/banlists.s
    (None, 'export_main_menu.py'),              # data/main-menu.s (主菜单 page table + sub-rows)
    (None, 'export_post_banlists_tables.py'),   # data/post-banlists-tables.s (level_signature + font_jp_dim/base/stride)
    (None, 'export_starter_deck.py'),           # data/starter-deck.s
    (None, 'export_struct_decks.py'),           # data/struct-decks.s
    (None, 'export_opponent_card_values.py'),   # data/opponent-card-values.s

    # Step 4: data/<text-dataset>.s → text/<text-dataset>/*.txt (UTF-8 源, 刷新)
    # ⚠ 覆盖 text/ 现内容; 编辑过 text/ 的话先备份再跑
    ('card-desc',    'decode_s_to_txt.py'),     # text/card-desc/{ja,en,de,fr,it,es}.txt
    ('card-desc',    'extract_pointer_table.py'),# text/card-desc/pointer-table.txt
    ('card-names',   'decode_s_to_txt.py'),     # text/card-names/{ja,en,de,fr,it,es}.txt + pointer-table.txt
    ('game-strings', 'decode_s_to_txt.py'),     # text/game-strings/ja.txt

    # Step 5: text/<text-dataset>/*.txt → data/<text-dataset>.s (重编码闭环, 等价 build.bat encoder)
    # 跑完后 data/*.s 与 Step 1-3 的输出应 byte-identical
    ('jp-decode',    'iterate_codetable.py'),         # tools/jp-decode/codetable.json (前置: 多源合并)
    ('jp-decode',    'fix_halfwidth_to_fullwidth.py'),# 半角→全角 + Math Bold 唯一占位
    ('card-desc',    'build_char_to_idx.py'),         # tools/card-desc/char_to_idx.json
    ('card-names',   'build_char_to_idx.py'),         # tools/card-names/char_to_idx.json
    ('game-strings', 'build_char_to_idx.py'),         # tools/game-strings/char_to_idx.json
    ('card-desc',    'encode_txt_to_s.py'),           # data/card-descriptions.s
    ('card-names',   'encode_txt_to_s.py'),           # data/card-names.s
    ('game-strings', 'encode_txt_to_s.py'),           # data/game-strings-ja.s
    ('game-strings', 'build_pointer_table.py'),       # data/game-strings-pointer-table.s (master 表 1651 行)
]


def run_script(tools_dir, subdir, name):
    """动态导入并执行脚本的 main(). 若脚本无 main(), 则按顶层模块直接 exec_module
    (适用于 decode_s_to_txt 等顶层语句脚本)."""
    if subdir is None:
        path = os.path.join(tools_dir, 'rom-export', name)
    else:
        path = os.path.join(tools_dir, subdir, name)
    if not os.path.exists(path):
        print(f'[SKIP] {path} not found')
        return False

    spec = importlib.util.spec_from_file_location(name.replace('.py', ''), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, 'main'):
        mod.main()
    # 顶层语句脚本 (如 decode_s_to_txt.py) 在 exec_module 时已运行
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # tools/rom-export
    tools_dir = os.path.dirname(script_dir)                  # tools
    project_root = os.path.dirname(tools_dir)                # 项目根
    os.chdir(project_root)

    rom_path = 'roms/2343.gba'
    if not os.path.exists(rom_path):
        print(f'ERROR: {rom_path} not found. Place the original ROM there first.')
        sys.exit(1)

    os.makedirs('data', exist_ok=True)
    os.makedirs('graphics', exist_ok=True)
    os.makedirs('text', exist_ok=True)

    print('=' * 60)
    print('  ROM 资产全量导出')
    print('=' * 60)

    t0 = time.time()
    ok = 0
    for subdir, name in EXPORT_PIPELINE:
        label = f'{subdir}/{name}' if subdir else name
        print(f'\n{"─" * 60}')
        print(f'  [{ok+1}/{len(EXPORT_PIPELINE)}] {label}')
        print(f'{"─" * 60}')
        os.chdir(project_root)  # 保险：每个脚本前 chdir 回根
        if run_script(tools_dir, subdir, name):
            ok += 1

    elapsed = time.time() - t0
    print(f'\n{"=" * 60}')
    print(f'  完成: {ok}/{len(EXPORT_PIPELINE)} 个脚本, 耗时 {elapsed:.1f}s')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
