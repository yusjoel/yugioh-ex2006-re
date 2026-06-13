# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg3Slots.py -- p5 file-05 Seg-3 (0x0804ad48..0x0804b4f4)
#   Sections:
#     A. EQ_SLOTS      -- data-equate (const_name + slot rename)
#     B. REF_SLOTS     -- USER label on target + DATA ref + slot rename
#     C. RENAME_SLOTS  -- plain rename + optional EOL (pure ASCII)
#     D. FUNC_RENAME   -- rename function (check_card_id_in_special_set -> check_card_is_ninja_type)
#     E. PLATE_SUBS    -- stale FUN_xxxx -> current name (substring replace)
#     E2. PLATE_REWRITE -- full plate rewrite for check_card_is_ninja_type (wrong card names)
#
#   73 DAT_/PTR_DAT_ slots total: EQ=71, REF=2, RENAME=1 (add 1 for dark_world_range_case1_ret)
#   FUNC_RENAME=1 (0x0804b09c)
#   PLATE_SUBS=6 (stale FUN_ substring) + PLATE_REWRITE=1 (full rewrite ninja_type)
#
#   NOTE: EQ slots for disasm blocks (Block A/B/C) are handled separately in
#         DisassembleF05Seg3Blocks.py AFTER the blocks are disassembled.
#
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM.
#    NOTE: slots inside disasm blocks (BlockA 0x4ae40-0x4ae9f,
#          BlockB 0x4af88-0x4b047, BlockC 0x4b250-0x4b2db)
#          are NOT listed here -- handled in DisassembleF05Seg3Blocks.py
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # check_card_is_archfiend_type (0x0804aea0) -- main segment literal pool
    (0x0804aec4, 0x000014b7, 'LESSER_FIEND_CID',               'archfiend_lesser_fiend_cid'),
    (0x0804aec8, 0x000010ab, 'WICKED_MIRROR_CID',              'archfiend_wicked_mirror_cid'),
    (0x0804aed0, 0x0000107f, 'B_SKULL_DRAGON_CID',             'archfiend_b_skull_dragon_cid'),
    (0x0804aee4, 0x0000127f, 'TOON_SUMMONED_SKULL_CID',        'archfiend_toon_summoned_skull_cid'),
    (0x0804aee8, 0x000010d6, 'AXE_OF_DESPAIR_CID',             'archfiend_axe_of_despair_cid'),
    (0x0804aef8, 0x000012b5, 'BEAST_OF_TALWAR_CID',            'archfiend_beast_of_talwar_cid'),
    (0x0804aefc, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID',        'archfiend_gilfer_cid'),
    (0x0804af1c, 0x00001692, 'SKULL_ARCHFIEND_OF_LIGHTNING_CID','archfiend_skull_archfiend_cid'),
    (0x0804af20, 0x000014da, 'FIEND_SKULL_DRAGON_CID',         'archfiend_fiend_skull_cid'),
    (0x0804af30, 0x0000165a, 'A_DEAL_WITH_DARK_RULER_CID',     'archfiend_deal_dark_cid'),
    (0x0804af48, 0x000016a4, 'EQUIP_LOCK_A_CID',               'archfiend_equip_lock_a_cid'),
    (0x0804af58, 0x00001911, 'CYBER_ARCHFIEND_CID',            'archfiend_cyber_cid'),
    # check_card_is_gravekeeper (0x0804af60)
    (0x0804af7c, 0x0000131d, 'GRAVEKEEPERS_SERVANT_CID',       'gravekeeper_servant_cid'),
    (0x0804af80, 0x0000158d, 'GRAVEKEEPERS_ASSAILANT_CID',     'gravekeeper_assailant_cid'),
    # check_card_is_amazoness_type (0x0804b048)
    (0x0804b064, 0x000014ab, 'AMAZONESS_CHAIN_MASTER_CID',     'amazoness_chain_master_cid'),
    (0x0804b070, 0x000014a6, 'AMAZONESS_ARCHERS_CID',          'amazoness_archers_cid'),
    (0x0804b090, 0x000014af, 'AMAZONESS_FIGHTER_CID',          'amazoness_fighter_cid'),
    (0x0804b094, 0x0000160f, 'AMAZONESS_TIGER_CID',            'amazoness_tiger_cid'),
    # check_card_is_ninja_type (0x0804b09c, misnamed check_card_id_in_special_set)
    (0x0804b0b0, 0x000016b9, 'STRIKE_NINJA_CID',               'ninja_type_strike_ninja_cid'),
    (0x0804b0b4, 0x0000117b, 'ARMED_NINJA_CID',                'ninja_type_armed_ninja_cid'),
    (0x0804b0cc, 0x000017df, 'NINJA_GRANDMASTER_SASUKE_CID',   'ninja_type_sasuke_cid'),
    (0x0804b0dc, 0x000018be, 'WHITE_NINJA_CID',                'ninja_type_white_ninja_cid'),
    # check_card_id_is_effect_monster_type_b (0x0804b0e4)
    (0x0804b104, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID',        'effect_b_smlv8_cid'),
    (0x0804b118, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',       'effect_b_sslv5_a_cid'),
    (0x0804b134, 0x0000185e, 'ULTIMATE_INSECT_LV5_CID',        'effect_b_uilv5_cid'),
    (0x0804b14c, 0x00001906, 'WINGED_KURIBOH_LV10_CID',        'effect_b_wkl10_cid'),
    (0x0804b15c, 0x0000198c, 'ARMED_DRAGON_LV10_CID',          'effect_b_adlv10_cid'),
    # check_card_id_is_normal_summon_type (0x0804b164)
    (0x0804b18c, 0x0000194e, 'EHERO_WILDHEART_CID',            'normal_summon_max_cid'),
    (0x0804b19c, 0x000018f9, 'EHERO_BUBBLEMAN_CID',            'normal_summon_bubbleman_cid'),
    (0x0804b1bc, 0x00001981, 'EHERO_MADBALLMAN_CID',           'normal_summon_madballman_cid'),
    (0x0804b1d4, 0x000019a6, 'EHERO_NEO_BUBBLEMAN_CID',        'normal_summon_neo_bubbleman_cid'),
    (0x0804b1e8, 0x000019ef, 'EHERO_ERIKSHIELER_CID',          'normal_summon_extra_d_cid'),
    # check_card_id_is_effect_monster_type_c (0x0804b1f0)
    (0x0804b210, 0x000016b4, 'OJAMA_BLACK_CID',                'effect_c_ojama_black_cid'),
    (0x0804b218, 0x00001681, 'OJAMA_GREEN_CID',                'effect_c_ojama_green_cid'),
    (0x0804b230, 0x000017ee, 'OJAMA_KING_CARD_ID',             'effect_c_ojama_king_cid'),
    (0x0804b234, 0x000016cf, 'OJAMA_DELTA_HURRICANE_CID',      'effect_c_ojama_delta_cid'),
    (0x0804b248, 0x00001946, 'OJAMAGIC_CID',                   'effect_c_ojamagic_cid'),
    # check_card_id_is_bes_type (0x0804b2dc)
    (0x0804b2f0, 0x00001913, 'BES_CRYSTAL_CORE_CID',           'bes_type_crystal_core_cid'),
    (0x0804b304, 0x00001962, 'BES_TETRAN_CID',                 'bes_type_tetran_cid'),
    # check_card_id_is_special_summon_type (0x0804b30c)
    (0x0804b330, 0x000019ae, 'ANCIENT_GEAR_DRILL_CID',         'spsummon_agdrill_cid'),
    (0x0804b334, 0x000018ab, 'ANCIENT_GEAR_GOLEM_CID',         'spsummon_aggolem_cid'),
    (0x0804b348, 0x000019b2, 'ANCIENT_GEAR_CASTLE_CID',        'spsummon_agcastle_cid'),
    # check_card_id_in_fusion_target_range (0x0804b350)
    (0x0804b368, 0x000017c9, 'THEINEN_THE_GREAT_SPHINX_CID',   'fusion_theinen_cid'),
    (0x0804b36c, 0x0000152e, 'GUARDIAN_SPHINX_CID',            'fusion_guardian_sphinx_cid'),
    (0x0804b380, 0x000018b2, 'CRIOSPHINX_CID',                 'fusion_criosphinx_cid'),
    # get_card_evolution_target_ids (0x0804b388)
    (0x0804b3bc, 0x000017da, 'ARMED_DRAGON_LV5_CID',           'evo_adlv5_cid'),
    (0x0804b3c0, 0x000017d5, 'DARK_MIMIC_LV1_CID',             'evo_dkmimic_lv1_cid'),
    (0x0804b3c4, 0x000017d2, 'HORUS_LV4_CID',                  'evo_horus_lv4_cid'),
    (0x0804b3d8, 0x000017d3, 'HORUS_LV6_CID',                  'evo_horus_lv6_a_cid'),
    (0x0804b3dc, 0x000017d4, 'HORUS_LV8_CID',                  'evo_horus_lv8_a_cid'),
    (0x0804b3fc, 0x000017d7, 'MYSTIC_SWORDSMAN_LV2_CID',       'evo_mslv2_cid'),
    (0x0804b418, 0x00001817, 'SILENT_MAGICIAN_LV4_CID',        'evo_smlv4_cid'),
    (0x0804b41c, 0x00001812, 'SILENT_SWORDSMAN_LV3_CID',       'evo_sslv3_cid'),
    (0x0804b42c, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',       'evo_sslv5_b_cid'),
    (0x0804b430, 0x00001816, 'SILENT_SWORDSMAN_LV7_CID',       'evo_sslv7_a_cid'),
    (0x0804b44c, 0x0000185e, 'ULTIMATE_INSECT_LV5_CID',        'evo_uilv5_cid'),
    (0x0804b450, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID',        'evo_smlv8_a_cid'),
    (0x0804b464, 0x000018af, 'ULTIMATE_INSECT_LV7_CID',        'evo_uilv7_cid'),
    (0x0804b46c, 0x00001822, 'ULTIMATE_INSECT_LV3_CID',        'evo_uilv3_a_cid'),
    (0x0804b474, 0x000017d3, 'HORUS_LV6_CID',                  'evo_horus_lv6_b_cid'),
    (0x0804b47c, 0x000017d4, 'HORUS_LV8_CID',                  'evo_horus_lv8_b_cid'),
    (0x0804b484, 0x000017d6, 'DARK_MIMIC_LV3_CID',             'evo_dkmimic_lv3_cid'),
    (0x0804b48c, 0x000017d8, 'MYSTIC_SWORDSMAN_LV4_CID',       'evo_mslv4_cid'),
    (0x0804b494, 0x00001823, 'MYSTIC_SWORDSMAN_LV6_CID',       'evo_mslv6_cid'),
    (0x0804b49c, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',       'evo_sslv5_c_cid'),
    (0x0804b4a4, 0x00001816, 'SILENT_SWORDSMAN_LV7_CID',       'evo_sslv7_b_cid'),
    (0x0804b4ac, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID',        'evo_smlv8_b_cid'),
    (0x0804b4c0, 0x000017d1, 'ULTIMATE_INSECT_LV1_CID',        'evo_uilv1_cid'),
    (0x0804b4d0, 0x00001822, 'ULTIMATE_INSECT_LV3_CID',        'evo_uilv3_b_cid'),
    (0x0804b4e4, 0x000017db, 'ARMED_DRAGON_LV7_CID',           'evo_adlv7_cid'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # check_card_field8_is_normal switch table ptr
    (0x0804ad88, 0x0804ad8c, 'switchdataD_0804ad8c', 'check_card_field8_is_normal_switch_table'),
    # check_card_is_dark_world_range_type switch table base ptr (inside BlockC -- but it's a data ptr)
    # NOTE: 0x0804b288 is inside BlockC (disasm range). We still set the ref from the slot,
    # but the slot may be in code after disasm. We handle it in the disasm script.
    # Keeping here for the pre-disasm case if Ghidra still shows it as data.
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Pure ASCII EOL only.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # dark_world_range_case1_ret inline stub (inside BlockC -- post-disasm handled in disasm script)
    # Pre-disasm: DAT_0804b2d4 rename here if Ghidra still sees it as data
    (0x0804b2d4, 'dark_world_range_case1_ret',
     'inline THUMB stub: movs r0,#1; b; movs r0,#0; bx lr (switch case targets)'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (func_addr, old_name, new_name)
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x0804b09c, 'check_card_id_in_special_set', 'check_card_is_ninja_type'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Substring replace in existing plate comment.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # check_card_field8_is_normal: FUN_08030aa4 -> check_slot_card_is_equip_type
    (0x0804ad70, 'FUN_08030aa4', 'check_slot_card_is_equip_type'),
    # check_card_stat_field8_is_6: FUN_0804ae18 -> check_card_stat_field8_is_7
    (0x0804ae04, 'FUN_0804ae18', 'check_card_stat_field8_is_7'),
    # check_card_stat_field8_is_8: FUN_0804ae18 -> check_card_stat_field8_is_7
    (0x0804ae2c, 'FUN_0804ae18', 'check_card_stat_field8_is_7'),
    # check_card_id_is_normal_summon_type: FUN_080a46a0 -> eval_card_placement_flags_for_ai
    (0x0804b164, 'FUN_080a46a0', 'eval_card_placement_flags_for_ai'),
    # check_card_id_is_bes_type: FUN_0803e594 -> tick_zone_card_place_with_slot_resolve_seq
    (0x0804b2dc, 'FUN_0803e594', 'tick_zone_card_place_with_slot_resolve_seq'),
    # check_card_id_is_bes_type: FUN_0803eb0c -> tick_equip_node_chain_link_display_seq
    (0x0804b2dc, 'FUN_0803eb0c', 'tick_equip_node_chain_link_display_seq'),
    # check_card_id_is_special_summon_type: FUN_0804b2dc -> check_card_id_is_bes_type
    (0x0804b30c, 'FUN_0804b2dc', 'check_card_id_is_bes_type'),
    # check_card_id_is_special_summon_type: FUN_0804b1f0 -> check_card_id_is_effect_monster_type_c
    (0x0804b30c, 'FUN_0804b1f0', 'check_card_id_is_effect_monster_type_c'),
]

# ---------------------------------------------------------------------------
# E2. PLATE_REWRITE: full plate rewrite for check_card_is_ninja_type
#     The old plate has WRONG card names (Nekogal_1/Gemini_Elf/Elemental_Burst)
#     and stale FUN_* references. Full ASCII rewrite.
# ---------------------------------------------------------------------------
NINJA_PLATE_NEW = (
    "Bool whitelist checker; leaf. Checks r0=card_id against 5 Ninja-type card IDs:\n"
    "[0x16b8..0x16b9]=(Crimson Ninja, Strike Ninja), 0x117b=Armed Ninja,\n"
    "0x17df=Ninja Grandmaster Sasuke, 0x18be=White Ninja.\n"
    "Returns 1 if any match, 0 otherwise. indeg=3.\n"
    "Callers: check_slot_card_eligible_by_card_id (0x0804f6c4),\n"
    "check_equip_slot_eligible_by_card_id_bst_and_pairs (0x08051cc4),\n"
    "check_equip_slot_eligible_by_card_id_dispatch_b (0x08052aa8)."
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF05Seg3Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    fm      = currentProgram.getFunctionManager()
    nA = nB = nC = nD = nE = 0
    made    = set()

    # --- A. EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->0x%08x %s)" % (slot_int, slot_label, tgt_int, gas_label)); nB += 1

    # --- C. RENAME_SLOTS ---
    for slot_int, label, eol in RENAME_SLOTS:
        cu = listing.getCodeUnitAt(_addr(slot_int))
        if cu is None:
            # Try as data
            d = getDataAt(_addr(slot_int))
            if d is None:
                print("[C FAIL] no CodeUnit or data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu2 = listing.getCodeUnitAt(_addr(slot_int))
            if cu2 is not None:
                cu2.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D. FUNC_RENAME ---
    for func_int, old_name, new_name in FUNC_RENAME:
        func = fm.getFunctionAt(_addr(func_int))
        if func is None:
            print("[D FAIL] no function @ 0x%08x" % func_int); continue
        cur_name = func.getName()
        if DRY:
            print("[D dry] 0x%08x %s -> %s" % (func_int, cur_name, new_name)); nD += 1; continue
        func.setName(new_name, SourceType.USER_DEFINED)
        print("[D ok] 0x%08x %s -> %s" % (func_int, cur_name, new_name)); nD += 1

    # --- E. PLATE_SUBS ---
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[E FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[E SKIP] no plate @ 0x%08x" % func_int); continue
        if old_s not in plate:
            print("[E SKIP] '%s' not in plate @ 0x%08x" % (old_s, func_int)); continue
        if DRY:
            print("[E dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nE += 1; continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[E ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s)); nE += 1

    # --- E2. PLATE_REWRITE for check_card_is_ninja_type (0x0804b09c) ---
    # After FUNC_RENAME above, the function is now check_card_is_ninja_type
    ninja_addr = 0x0804b09c
    cu = listing.getCodeUnitAt(_addr(ninja_addr))
    if cu is None:
        print("[E2 FAIL] no CodeUnit @ 0x%08x" % ninja_addr)
    else:
        if DRY:
            print("[E2 dry] 0x%08x full plate rewrite (check_card_is_ninja_type, wrong card names -> ASCII)" % ninja_addr)
        else:
            cu.setComment(CodeUnit.PLATE_COMMENT, NINJA_PLATE_NEW)
            print("[E2 ok] 0x%08x plate rewritten for check_card_is_ninja_type" % ninja_addr)

    print("[done] A=%d B=%d C=%d D=%d E=%d (DRY=%s)" % (nA, nB, nC, nD, nE, DRY))


main()
