# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg8Slots.py -- f11 Seg-8 slot symbolization [0x08090a78..0x08091888)
#
# 3 named functions:
#   build_equip_candidate_score_table   (0x08090a78, ~0xc48 B, data-dense)
#   invoke_build_equip_candidate_score_table (0x080916c0)
#   write_equip_target_score_entry      (0x080916cc, ~0x1bc B)
#
# EQ:  53 total (37 REUSE + 16 NEW)
# REF: 21 total (16 REUSE + 5 NEW) -- createLabel + addMemoryReference + setPrimary
# RENAME: 21 (the 21 REF slot labels)
# PLATE: 3 (ASCII, CJK->ASCII + stale FUN_ substitution + Viser Des -> Dimension Wall fix)
#
# NEW constants (added to constants/card_info.inc + constants/ewram.inc before this script):
#   card_info.inc: KINETIC_SOLDIER_CID=0x13aa, HUNTER_7_WEAPONS_CID=0x14cc,
#                  AMAZONESS_SWORDS_WOMAN_CID=0x14a4, STEAMROID_CID=0x18f2,
#                  SKYSCRAPER_CID=0x18ff, DIMENSION_WALL_CID=0x1930,
#                  EQUIP_ATK_SCORE_HI_2499=0x9c3, EQUIP_ATK_SCORE_HI_2500=0x9c4
#   ewram.inc:  gEquipLpScoreBase=0x0201afe0, gEquipCandidateSlotA=0x0201bc38,
#               gEquipCandidateSlotB=0x0201bc3c
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL, skip that item.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, name='?'):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(slot_addr)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL value @0x%08x %s: expected=0x%08x actual=0x%08x" % (
                slot_addr, name, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x%08x %s: %s" % (slot_addr, name, e))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol=None):
    if not _check(slot_addr, value, eq_name):
        return False
    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_val, gas_label, slot_label, eol=None):
    """Create USER label at target + USER label at slot + DATA ref slot->target + setPrimary."""
    if not _check(slot_addr, target_val, gas_label):
        return False
    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas=%s  label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True
    a = _addr(slot_addr)
    t = _addr(target_val)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    # Create label at target (global) if not present
    tgt_syms = list(sym_tbl.getSymbols(t))
    if not any(s.getName() == gas_label for s in tgt_syms):
        sym_tbl.createLabel(t, gas_label, SourceType.USER_DEFINED)
    # Create slot label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    # Add DATA reference from slot -> target
    ref_mgr.addMemoryReference(a, t, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary on new ref
    for ref in ref_mgr.getReferencesFrom(a):
        if ref.getToAddress() == t:
            ref_mgr.setPrimary(ref, True)
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REF] 0x%08x  target=0x%08x  -> %s" % (slot_addr, target_val, slot_label))
    return True


def _apply_plate(fn_addr, plate_text):
    if DRY:
        print("[dry] PLATE 0x%08x  len=%d" % (fn_addr, len(plate_text)))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT] 0x%08x OK  len=%d" % (fn_addr, len(plate_text)))
        return True
    except Exception as e:
        print("FAIL PLATE 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


# =============================================================================
# EQ_SLOTS: 53 total (37 REUSE + 16 NEW)
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================
EQ_SLOTS = [
    # --- build_equip_candidate_score_table [0x08090a78] literal pool ---
    # REUSE slots
    (0x08090cb0, 0x00000868, 'PLAYER_BLOCK_STRIDE',              'seg8_pool_stride_0cb0',    None),
    (0x08090cbc, 0x00001381, 'MIRROR_WALL_CID',                  'seg8_pool_cid_mw_0cbc',    None),
    (0x08090cc0, 0x00001905, 'DARK_DREADROUTE_CID',              'seg8_pool_cid_ddr_0cc0',   None),
    (0x08090cc4, 0x00001951, 'WATER_DRAGON_CID',                 'seg8_pool_cid_wd_0cc4',    None),
    (0x08090cc8, 0x00001955, 'CYBER_BLADER_CID',                 'seg8_pool_cid_cb_0cc8',    None),
    (0x08090ccc, 0x000014d7, 'SPIRIT_RYU_CID',                   'seg8_pool_cid_sr_0ccc',    None),
    (0x08090cf8, 0x00001643, 'MIRAGE_KNIGHT_CID',                'seg8_pool_cid_mk_0cf8',    None),
    (0x08090d04, 0x00001956, 'EHERO_RAMPART_BLASTER_CARD_ID',    'seg8_pool_cid_erb_0d04',   None),
    (0x08090d24, 0x00000bb8, 'LP_COST_3000',                     'seg8_pool_lp3k_0d24',      None),
    (0x08090e50, 0x00001846, 'BALLISTA_OF_RAMPART_SMASHING_CID', 'seg8_pool_cid_brs_0e50',   None),
    (0x08090e58, 0x000005dc, 'LP_COST_1500',                     'seg8_pool_lp15_0e58',      None),
    (0x08090e5c, 0x00000868, 'PLAYER_BLOCK_STRIDE',              'seg8_pool_stride_0e5c',    None),
    (0x08090e64, 0x000013a7, 'INJECTION_FAIRY_LILY_CID',         'seg8_pool_cid_ifl_0e64',   None),
    (0x08090e68, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',           'seg8_pool_enbo_0e68',      None),
    (0x08090e6c, 0x00001119, 'SANGA_OF_THUNDER_CID',             'seg8_pool_cid_st_0e6c',    None),
    (0x08090ea8, 0x00000bb8, 'LP_COST_3000',                     'seg8_pool_lp3k_0ea8',      None),
    (0x08091040, 0x00001257, 'REVERSE_TRAP_CID',                 'seg8_pool_cid_rt_1040',    None),
    (0x08091048, 0x00001381, 'MIRROR_WALL_CID',                  'seg8_pool_cid_mw_1048',    None),
    (0x0809104c, 0x00001905, 'DARK_DREADROUTE_CID',              'seg8_pool_cid_ddr_104c',   None),
    (0x08091050, 0x00001951, 'WATER_DRAGON_CID',                 'seg8_pool_cid_wd_1050',    None),
    (0x08091054, 0x00001955, 'CYBER_BLADER_CID',                 'seg8_pool_cid_cb_1054',    None),
    (0x08091058, 0x00000868, 'PLAYER_BLOCK_STRIDE',              'seg8_pool_stride_1058',    None),
    (0x08091064, 0x000013a7, 'INJECTION_FAIRY_LILY_CID',         'seg8_pool_cid_ifl_1064',   None),
    (0x08091078, 0x00001643, 'MIRAGE_KNIGHT_CID',                'seg8_pool_cid_mk_1078',    None),
    (0x080910a8, 0x00000bb8, 'LP_COST_3000',                     'seg8_pool_lp3k_10a8',      None),
    (0x08091348, 0xfffffe0c, 'LP_EQUIP_DELTA_NEG_500',           'seg8_pool_delta_1348',     None),
    (0x08091350, 0x00001853, 'COVERING_FIRE_CID',                'seg8_pool_cid_cf_1350',    None),
    (0x08091354, 0x00001238, 'METALMORPH_CID',                   'seg8_pool_cid_mm_1354',    None),
    (0x0809135c, 0x00000868, 'PLAYER_BLOCK_STRIDE',              'seg8_pool_stride_135c',    None),
    (0x08091368, 0x0000159e, 'BUSTER_RANCHER_CID',               'seg8_pool_cid_br_1368',    None),
    (0x080914f4, 0x0000159e, 'BUSTER_RANCHER_CID',               'seg8_pool_cid_br_14f4',    None),
    (0x080916ac, 0x0000159e, 'BUSTER_RANCHER_CID',               'seg8_pool_cid_br_16ac',    None),
    (0x080916b4, 0x00000513, 'FIELD5_SCORE_THRESHOLD_1299',      'seg8_pool_f5th_16b4',      None),
    (0x080916b8, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID',         'seg8_pool_cid_hcw_16b8',   None),
    (0x080917d4, 0x00001639, 'TOKEN_1639_CID',                   'seg8_pool_cid_tok_17d4',   None),
    (0x080917d8, 0x00000868, 'PLAYER_BLOCK_STRIDE',              'seg8_pool_stride_17d8',    None),
    # EQ_NEW slots
    (0x08090cd0, 0x000013aa, 'KINETIC_SOLDIER_CID',              'seg8_pool_cid_ks_0cd0',    None),
    (0x08090cdc, 0x000014cc, 'HUNTER_7_WEAPONS_CID',             'seg8_pool_cid_h7w_0cdc',   None),
    (0x08090e80, 0x000013aa, 'KINETIC_SOLDIER_CID',              'seg8_pool_cid_ks_0e80',    None),
    (0x08090e84, 0x000014cc, 'HUNTER_7_WEAPONS_CID',             'seg8_pool_cid_h7w_0e84',   None),
    (0x08091060, 0x000014cc, 'HUNTER_7_WEAPONS_CID',             'seg8_pool_cid_h7w_1060',   None),
    (0x08090cf4, 0x000018f2, 'STEAMROID_CID',                    'seg8_pool_cid_str_0cf4',   None),
    (0x0809107c, 0x000018f2, 'STEAMROID_CID',                    'seg8_pool_cid_str_107c',   None),
    (0x08091358, 0x000018ff, 'SKYSCRAPER_CID',                   'seg8_pool_cid_sky_1358',   None),
    (0x08091388, 0x000009c3, 'EQUIP_ATK_SCORE_HI_2499',          'seg8_pool_atk2499_1388',   None),
    (0x080914ec, 0x000009c3, 'EQUIP_ATK_SCORE_HI_2499',          'seg8_pool_atk2499_14ec',   None),
    (0x08091520, 0x000009c3, 'EQUIP_ATK_SCORE_HI_2499',          'seg8_pool_atk2499_1520',   None),
    (0x080916a4, 0x000009c3, 'EQUIP_ATK_SCORE_HI_2499',          'seg8_pool_atk2499_16a4',   None),
    (0x080914f8, 0x000009c4, 'EQUIP_ATK_SCORE_HI_2500',          'seg8_pool_atk2500_14f8',   None),
    (0x080916b0, 0x000009c4, 'EQUIP_ATK_SCORE_HI_2500',          'seg8_pool_atk2500_16b0',   None),
    (0x080917d0, 0x000014a4, 'AMAZONESS_SWORDS_WOMAN_CID',       'seg8_pool_cid_asw_17d0',   None),
    (0x08091850, 0x00001930, 'DIMENSION_WALL_CID',               'seg8_pool_cid_dw_1850',    None),
]

# =============================================================================
# REF_SLOTS: 21 total (16 REUSE + 5 NEW)
# Format: (slot_addr, target_val, gas_label, slot_label, eol_or_None)
# =============================================================================
REF_SLOTS = [
    # REUSE (16 slots -- existing globals, only label rename needed)
    (0x08090cb4, 0x0201c510, 'gDuelFieldSlots',       'ptr_gDuelFieldSlots_0cb4',      'gDuelFieldSlots'),
    (0x08090cb8, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_0cb8',  'gEquipChainSlotRefs'),
    (0x08090e54, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_0e54',  'gEquipChainSlotRefs'),
    (0x08090e60, 0x0201c510, 'gDuelFieldSlots',       'ptr_gDuelFieldSlots_0e60',      'gDuelFieldSlots'),
    (0x08091044, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_1044',  'gEquipChainSlotRefs'),
    (0x0809105c, 0x0201c510, 'gDuelFieldSlots',       'ptr_gDuelFieldSlots_105c',      'gDuelFieldSlots'),
    (0x08091100, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_1100',  'gEquipChainSlotRefs'),
    (0x0809134c, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_134c',  'gEquipChainSlotRefs'),
    (0x08091360, 0x0201c510, 'gDuelFieldSlots',       'ptr_gDuelFieldSlots_1360',      'gDuelFieldSlots'),
    (0x08091364, 0x0201d9c0, 'gEquipNodePool',        'ptr_gEquipNodePool_1364',       'gEquipNodePool'),
    (0x080914f0, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_14f0',  'gEquipChainSlotRefs'),
    (0x080916a8, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_16a8',  'gEquipChainSlotRefs'),
    (0x080916bc, 0x0201e2a0, 'gDuelCardCtxBase',      'ptr_gDuelCardCtxBase_16bc',     'gDuelCardCtxBase'),
    (0x08091730, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_1730',  'gEquipChainSlotRefs'),
    (0x080917dc, 0x0201c520, 'gDuelFieldSlotState',   'ptr_gDuelFieldSlotState_17dc',  'gDuelFieldSlotState'),
    (0x08091884, 0x0201bb90, 'gEquipChainSlotRefs',   'ptr_gEquipChainSlotRefs_1884',  'gEquipChainSlotRefs'),
    # NEW (5 slots -- 3 new globals: gEquipLpScoreBase / gEquipCandidateSlotA / gEquipCandidateSlotB)
    (0x08090b34, 0x0201afe0, 'gEquipLpScoreBase',     'ptr_gEquipLpScoreBase_0b34',    'gEquipLpScoreBase'),
    (0x080917cc, 0x0201bc38, 'gEquipCandidateSlotA',  'ptr_gEquipCandidateSlotA_17cc', 'gEquipCandidateSlotA'),
    (0x0809184c, 0x0201bc38, 'gEquipCandidateSlotA',  'ptr_gEquipCandidateSlotA_184c', 'gEquipCandidateSlotA'),
    (0x080917e0, 0x0201bc3c, 'gEquipCandidateSlotB',  'ptr_gEquipCandidateSlotB_17e0', 'gEquipCandidateSlotB'),
    (0x08091848, 0x0201bc3c, 'gEquipCandidateSlotB',  'ptr_gEquipCandidateSlotB_1848', 'gEquipCandidateSlotB'),
]

# =============================================================================
# PLATE_SLOTS: 3 functions -- ASCII only, no CJK
# =============================================================================
PLATE_SLOTS = [
    # build_equip_candidate_score_table (0x08090a78): CJK->ASCII rewrite, FUN_ substitution
    (0x08090a78,
     "Called by eval_equip_spell_placement_with_score + eval_fieldspell_equip_placement_full (indeg>=2, r1=1). "
     "Entry: r7=player_side, r9=mode_flag. Reads gEquipChainSlotRefs (0x0201bb90) context; "
     "outer loop r6=[0..1]: r6==r9 copies 9-word candidate entry via ldmia/stmia x3; "
     "r6!=r9 calls eval_slot_score_entry_full. Zeroes slot_b[+0x10/+1c/+20]. "
     "Writes gEquipChainSlotRefs score table. entry_size=0x38, player_stride=0x868."),
    # invoke_build_equip_candidate_score_table (0x080916c0): over-500 rewrite
    (0x080916c0,
     "Thunk: sets r0=0, calls build_equip_candidate_score_table, returns via pop {r0}; bx r0. "
     "Called from tick_equip_zone_activation_display_state and FUN_08099314 (case_0 path) "
     "+ 5 other callsites (7 total) at equip activation init. "
     "Returns pass-through from build_equip_candidate_score_table (0=success)."),
    # write_equip_target_score_entry (0x080916cc): CJK->ASCII, FUN_ sub, Viser Des->Dimension Wall
    (0x080916cc,
     "Called by eval_field_equip_activation_candidates (indeg=6). "
     "r0=player_id, r1=duel_zone_ptr, r2=score_entry_ptr, r8=target_slot_idx (non-APCS). "
     "Reads gEquipChainSlotRefs[+0x9c] (is_activated); "
     "writes [+0x2c+idx*4], [+0xa0+idx*4], [+0xa4+idx*4]. "
     "If r1==0: writes [+0xa8]=(1-r2[0]), [+0xac]=5; else r1[0]/r1[4]. "
     "Checks DIMENSION_WALL_CID=0x1930 via check_value_in_slot_chain; "
     "if found writes [+0xac]=5. Toggles zone[+0x38+idx*4] (activation toggle)."),
]


# =============================================================================
# MAIN
# =============================================================================
print("=" * 60)
print("RefineF11Seg8Slots.py  DRY=%s" % DRY)
print("=" * 60)

eq_ok = eq_fail = 0
for (slot_addr, value, eq_name, slot_label, eol) in EQ_SLOTS:
    if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
        eq_ok += 1
    else:
        eq_fail += 1

print("--- EQ done: %d ok / %d fail ---" % (eq_ok, eq_fail))

ref_ok = ref_fail = 0
for (slot_addr, target_val, gas_label, slot_label, eol) in REF_SLOTS:
    if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
        ref_ok += 1
    else:
        ref_fail += 1

print("--- REF done: %d ok / %d fail ---" % (ref_ok, ref_fail))

plate_ok = plate_fail = 0
for (fn_addr, plate_text) in PLATE_SLOTS:
    if _apply_plate(fn_addr, plate_text):
        plate_ok += 1
    else:
        plate_fail += 1

print("--- PLATE done: %d ok / %d fail ---" % (plate_ok, plate_fail))

total_fail = eq_fail + ref_fail + plate_fail
print("=" * 60)
print("TOTAL: EQ=%d/%d  REF=%d/%d  PLATE=%d/%d  FAIL=%d" % (
    eq_ok, len(EQ_SLOTS), ref_ok, len(REF_SLOTS), plate_ok, len(PLATE_SLOTS), total_fail))
if total_fail == 0:
    print("ALL OK")
else:
    print("*** FAILURES DETECTED -- review output above ***")
print("=" * 60)
