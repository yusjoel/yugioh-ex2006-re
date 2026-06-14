# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg10Slots.py -- F06 Seg-10 (0x0805b480..0x0805c2f0) [file 06 FINAL segment]
#   equip eligibility zone/summon check cluster + Neo Daedalus dispatch (15 fn, 2 switchD tables)
#   EQ=56  REF=12  RENAME=9 (5 DAT_ + 4 PTR_)  PLATE_SUB=5 (10 FUN_ stale refs across 5 fns)
#
# New constants added to constants/ before running this script:
#   card_info.inc: GORGONS_EYE_CID/RITE_OF_SPIRIT_CID/SILENT_INSECT_CID/cid_134e-1351 (+7)
#   duel_field.inc: ZONE_STATUS_SUMMON_ELIGIBLE (+1)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (56 slots; mix of reuse + new)
#   B. REF_SLOTS  -- USER label + DATA ref + slot rename (12 slots)
#   C. RENAME_SLOTS -- plain rename + EOL (5 DAT_ + 4 PTR_gP1LifePoints_)
#   D. PLATE_SUB  -- substring replace of stale FUN_XXXXXXXX with current names (5 fns)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython double UTF-8 mojibake prevention).
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_150000-pre-F06Seg10

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

FAILS = []

def _addr(va):
    return toAddr(va)

def _check(slot, expected):
    """Read 4 bytes little-endian from slot; warn if mismatch."""
    mem = currentProgram.getMemory()
    try:
        v = mem.getInt(_addr(slot)) & 0xffffffff
    except Exception as e:
        print("WARN _check read error @ 0x%08x: %s" % (slot, e))
        FAILS.append(slot)
        return False
    if v != (expected & 0xffffffff):
        print("WARN value mismatch @ 0x%08x: ROM=0x%08x expected=0x%08x -- SKIP" % (slot, v, expected))
        FAILS.append(slot)
        return False
    return True

def make_equate(name, val):
    et = currentProgram.getEquateTable()
    eq = et.getEquate(name)
    if eq is None:
        if not DRY:
            eq = et.createEquate(name, val & 0xffffffff)
        print("  NEW equate %s = 0x%x" % (name, val))
    return eq

def apply_eq(slot, value, eq_name, slot_label, eol=None):
    if not _check(slot, value):
        return
    if DRY:
        print("DRY EQ 0x%08x %s=%s label=%s" % (slot, eq_name, hex(value), slot_label))
        return
    eq = make_equate(eq_name, value)
    if eq:
        try:
            eq.addReference(_addr(slot), 0)
        except Exception as e:
            print("WARN addRef eq @ 0x%08x: %s" % (slot, e))
    sym_tbl = currentProgram.getSymbolTable()
    try:
        sym_tbl.createLabel(_addr(slot), slot_label, SourceType.USER_DEFINED)
    except Exception as e:
        print("WARN createLabel slot @ 0x%08x: %s" % (slot, e))
    if eol:
        try:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(_addr(slot))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        except Exception as e:
            print("WARN setEOL @ 0x%08x: %s" % (slot, e))
    print("  EQ 0x%08x %s=%s -> %s" % (slot, eq_name, hex(value), slot_label))

def apply_ref(slot, target, gas_label, slot_label, eol=None):
    if DRY:
        print("DRY REF 0x%08x -> 0x%08x label=%s slot=%s" % (slot, target, gas_label, slot_label))
        return
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    try:
        sym_tbl.createLabel(_addr(target), gas_label, SourceType.USER_DEFINED)
    except Exception as e:
        print("WARN createLabel target 0x%08x: %s" % (target, e))
    try:
        ref = ref_mgr.addMemoryReference(_addr(slot), _addr(target), RefType.DATA, SourceType.USER_DEFINED, 0)
        ref_mgr.setPrimary(ref, True)
    except Exception as e:
        print("WARN addMemRef @ 0x%08x: %s" % (slot, e))
    try:
        sym_tbl.createLabel(_addr(slot), slot_label, SourceType.USER_DEFINED)
    except Exception as e:
        print("WARN createLabel slot 0x%08x: %s" % (slot, e))
    if eol:
        try:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(_addr(slot))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        except Exception as e:
            print("WARN setEOL @ 0x%08x: %s" % (slot, e))
    print("  REF 0x%08x -> %s (%s)" % (slot, gas_label, slot_label))

def apply_rename(slot, slot_label, eol=None):
    if DRY:
        print("DRY RENAME 0x%08x -> %s" % (slot, slot_label))
        return
    sym_tbl = currentProgram.getSymbolTable()
    try:
        sym_tbl.createLabel(_addr(slot), slot_label, SourceType.USER_DEFINED)
    except Exception as e:
        print("WARN createLabel rename @ 0x%08x: %s" % (slot, e))
    if eol:
        try:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(_addr(slot))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        except Exception as e:
            print("WARN setEOL @ 0x%08x: %s" % (slot, e))
    print("  RENAME 0x%08x -> %s" % (slot, slot_label))

def apply_plate(func_addr, new_text):
    if DRY:
        print("DRY PLATE 0x%08x len=%d" % (func_addr, len(new_text)))
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(func_addr))
    if cu is None:
        print("WARN PLATE: no code unit @ 0x%08x" % func_addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
    print("  PLATE SET @ 0x%08x" % func_addr)

def plate_sub(func_addr, replacements):
    """Substring replace stale FUN_ refs in existing plate comment."""
    if DRY:
        for old, new in replacements:
            print("DRY PLATE_SUB 0x%08x: %s -> %s" % (func_addr, old, new))
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(func_addr))
    if cu is None:
        print("WARN PLATE_SUB: no code unit @ 0x%08x" % func_addr)
        return
    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("WARN PLATE_SUB: no existing plate @ 0x%08x -- skip" % func_addr)
        return
    updated = existing
    for old, new in replacements:
        if old in updated:
            updated = updated.replace(old, new)
            print("  PLATE_SUB 0x%08x: %s -> %s" % (func_addr, old, new))
        else:
            print("WARN PLATE_SUB: pattern not found in plate @ 0x%08x: '%s'" % (func_addr, old))
            FAILS.append(func_addr)
    if updated != existing:
        cu.setComment(CodeUnit.PLATE_COMMENT, updated)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) -- 7 slots ====
    (0x0805b87c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'find_zone_slot_match_by_type_in_node_list_stride', None),
    (0x0805ba48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_equip_zone_candidates_with_snapshot_stride', None),
    (0x0805bf98, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_equip_slots_eligible_for_card_stride', None),
    (0x0805c034, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_equip_slots_eligible_for_card_stride_b', None),
    (0x0805c16c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_equip_slots_eligible_banisher_guard_stride', None),
    (0x0805c1bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'get_lp_count_minus_zone_slot_offset_stride', None),
    (0x0805c2ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_effect_for_neo_daedalus_slot_with_monster_count_stride', None),

    # ==== LP_BAR_ANIM_STATE_OFF = 0x000004cc (ewram.inc) -- 2 slots ====
    (0x0805b528, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'find_zone_slot_match_by_type_in_node_list_count_off', None),
    (0x0805b5ec, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'find_zone_slot_match_by_type_in_node_list_count_off_b', None),

    # ==== SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (ewram.inc) -- 1 slot ====
    (0x0805b550, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'find_zone_slot_match_by_type_in_node_list_zone_off', None),

    # ==== CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (ewram.inc) -- 1 slot ====
    (0x0805b5e4, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'find_zone_slot_match_by_type_in_node_list_slot_off', None),

    # ==== SCROLLBAR_KEEP_BITS_8_0 = 0x000001ff (gl_scrollbar.inc) -- 2 slots ====
    (0x0805b520, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0', 'find_zone_slot_match_by_type_in_node_list_slot_mask', None),
    (0x0805b5e8, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0', 'find_zone_slot_match_by_type_in_node_list_slot_mask_b', None),

    # ==== FIELD_ARRAY_C_TO_COUNT_NEG_OFF = 0xfffffeec (duel_field.inc) -- 2 slots ====
    (0x0805c040, 0xfffffeec, 'FIELD_ARRAY_C_TO_COUNT_NEG_OFF', 'scan_equip_slots_eligible_for_card_neg_off', None),
    (0x0805c178, 0xfffffeec, 'FIELD_ARRAY_C_TO_COUNT_NEG_OFF', 'scan_equip_slots_eligible_banisher_guard_neg_off', None),

    # ==== EQUIP_ZONE_SPRITE_ATTR = 0x00000fb6 (duel_field.inc) -- 1 slot ====
    (0x0805c1e0, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR', 'check_equip_slot_chain_absent_sentinel',
     '0xfb6 equip-slot chain sentinel: check_equip_slot_chain_absent uses as chain-occupied marker'),

    # ==== CID equates -- reuse card_info.inc ====
    # JINZO_CID = 0x00001296
    (0x0805b894, 0x00001296, 'JINZO_CID', 'populate_effect_node_snapshot_jinzo', None),

    # LEVEL_MODULATION_CID = 0x00001944 (3 slots)
    (0x0805b88c, 0x00001944, 'LEVEL_MODULATION_CID', 'populate_effect_node_snapshot_lvmod', None),
    (0x0805bb24, 0x00001944, 'LEVEL_MODULATION_CID', 'populate_effect_node_snapshot_lvmod_b', None),
    (0x0805bdc4, 0x00001944, 'LEVEL_MODULATION_CID', 'check_card_special_summon_eligible_full_lvmod', None),
    (0x0805be14, 0x00001944, 'LEVEL_MODULATION_CID', 'check_card_special_summon_eligible_full_lvmod_b', None),

    # SPELL_CANCELLER_CID = 0x000015da
    (0x0805b890, 0x000015da, 'SPELL_CANCELLER_CID', 'populate_effect_node_snapshot_spcancel', None),

    # SKILL_DRAIN_CID = 0x0000166c (2 slots)
    (0x0805b878, 0x0000166c, 'SKILL_DRAIN_CID', 'populate_effect_node_snapshot_skdrain', None),
    (0x0805bdbc, 0x0000166c, 'SKILL_DRAIN_CID', 'check_card_special_summon_eligible_full_skdrain', None),

    # JUDGEMENT_OF_PHARAOH_CID = 0x00001679 (3 slots)
    (0x0805b860, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'populate_effect_node_snapshot_jphar', None),
    (0x0805be18, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'check_card_special_summon_eligible_full_jphar', None),
    (0x0805bef4, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'check_card_special_summon_eligible_full_jphar_b', None),

    # ROYAL_DECREE_CID = 0x00001302 (3 slots)
    (0x0805b984, 0x00001302, 'ROYAL_DECREE_CID', 'populate_effect_node_snapshot_royaldec', None),
    (0x0805bb28, 0x00001302, 'ROYAL_DECREE_CID', 'scan_equip_zone_candidates_with_snapshot_royaldec', None),
    (0x0805bc9c, 0x00001302, 'ROYAL_DECREE_CID', 'check_card_normal_summon_eligible_full_royaldec', None),

    # PARASITE_PARACIDE_CID = 0x000012a1 (2 slots)
    (0x0805c03c, 0x000012a1, 'PARASITE_PARACIDE_CID', 'scan_equip_slots_eligible_for_card_sentinel', None),
    (0x0805c174, 0x000012a1, 'PARASITE_PARACIDE_CID', 'scan_equip_slots_eligible_banisher_guard_sentinel', None),

    # SILENT_SWORDSMAN_LV7_CID = 0x00001816
    (0x0805b8ac, 0x00001816, 'SILENT_SWORDSMAN_LV7_CID', 'populate_effect_node_snapshot_sw7', None),

    # SILENT_SWORDSMAN_LV3_CID = 0x00001812
    (0x0805bc3c, 0x00001812, 'SILENT_SWORDSMAN_LV3_CID', 'scan_equip_zone_candidates_with_snapshot_sw3', None),

    # BLUE_EYES_SHINING_DRAGON_CID = 0x000017c2
    (0x0805bc40, 0x000017c2, 'BLUE_EYES_SHINING_DRAGON_CID', 'scan_equip_zone_candidates_with_snapshot_besd', None),

    # AMPLIFIER_CID = 0x000012d3
    (0x0805b8d0, 0x000012d3, 'AMPLIFIER_CID', 'populate_effect_node_snapshot_amp', None),

    # ROYAL_COMMAND_CID = 0x0000148e (2 slots)
    (0x0805b98c, 0x0000148e, 'ROYAL_COMMAND_CID', 'populate_effect_node_snapshot_royalcmd', None),
    (0x0805bdb4, 0x0000148e, 'ROYAL_COMMAND_CID', 'check_card_special_summon_eligible_full_royalcmd', None),

    # THE_EMPERORS_HOLIDAY_CID = 0x00001495
    (0x0805b988, 0x00001495, 'THE_EMPERORS_HOLIDAY_CID', 'populate_effect_node_snapshot_emphl', None),

    # FIEND_SKULL_DRAGON_CID = 0x000014da (2 slots)
    (0x0805b898, 0x000014da, 'FIEND_SKULL_DRAGON_CID', 'populate_effect_node_snapshot_fsd', None),
    (0x0805bdb8, 0x000014da, 'FIEND_SKULL_DRAGON_CID', 'check_card_special_summon_eligible_full_fsd', None),

    # NECROVALLEY_CID = 0x0000159d
    (0x0805bef8, 0x0000159d, 'NECROVALLEY_CID', 'check_card_special_summon_eligible_full_necrov', None),

    # CYBER_BLADER_CID = 0x00001955
    (0x0805bef0, 0x00001955, 'CYBER_BLADER_CID', 'check_card_special_summon_eligible_full_cyberb', None),

    # EHERO_WILDHEART_CID = 0x0000194e
    (0x0805ba54, 0x0000194e, 'EHERO_WILDHEART_CID', 'scan_equip_zone_candidates_with_snapshot_ehwild', None),

    # THE_END_OF_ANUBIS_CID = 0x000017b9
    (0x0805bf08, 0x000017b9, 'THE_END_OF_ANUBIS_CID', 'check_card_special_summon_eligible_full_anubis', None),

    # BANISHER_OF_THE_LIGHT_CID = 0x00001332
    (0x0805c08c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'scan_equip_slots_eligible_banisher_guard_cid', None),

    # ZONE_STATUS_MASK = 0x0000303e (card_info.inc)
    (0x0805bf00, 0x0000303e, 'ZONE_STATUS_MASK', 'check_card_special_summon_eligible_full_zone_mask', None),

    # ==== NEW CID equates (card_info.inc Seg-10 additions) ====
    # GORGONS_EYE_CID = 0x000012bf (2 slots)
    (0x0805b874, 0x000012bf, 'GORGONS_EYE_CID', 'populate_effect_node_snapshot_gorgonseye', None),
    (0x0805bdc0, 0x000012bf, 'GORGONS_EYE_CID', 'check_card_special_summon_eligible_full_gorgonseye', None),

    # RITE_OF_SPIRIT_CID = 0x000015ac
    (0x0805befc, 0x000015ac, 'RITE_OF_SPIRIT_CID', 'check_card_special_summon_eligible_full_riteofspirit', None),

    # SILENT_INSECT_CID = 0x000019c6
    (0x0805b8b0, 0x000019c6, 'SILENT_INSECT_CID', 'populate_effect_node_snapshot_silentinsect', None),

    # cid_134e = 0x0000134e
    (0x0805b870, 0x0000134e, 'cid_134e', 'populate_effect_node_snapshot_cid_134e', None),

    # cid_134f = 0x0000134f
    (0x0805b86c, 0x0000134f, 'cid_134f', 'populate_effect_node_snapshot_cid_134f', None),

    # cid_1350 = 0x00001350
    (0x0805b868, 0x00001350, 'cid_1350', 'populate_effect_node_snapshot_cid_1350', None),

    # cid_1351 = 0x00001351
    (0x0805b864, 0x00001351, 'cid_1351', 'populate_effect_node_snapshot_cid_1351', None),

    # ==== NEW scalar: ZONE_STATUS_SUMMON_ELIGIBLE = 0x0000201c (duel_field.inc) ====
    (0x0805bf04, 0x0000201c, 'ZONE_STATUS_SUMMON_ELIGIBLE', 'check_card_normal_summon_eligible_full_zone_val', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gDuelPhaseFlags = 0x0201b290 (ewram.inc)
    (0x0805b524, 0x0201b290, 'gDuelPhaseFlags', 'find_zone_slot_match_by_type_in_node_list_base', None),

    # gDuelFieldSlots = 0x0201c510 (ewram.inc) -- 3 slots
    (0x0805b880, 0x0201c510, 'gDuelFieldSlots', 'populate_effect_node_snapshot_slots', None),
    (0x0805ba4c, 0x0201c510, 'gDuelFieldSlots', 'scan_equip_zone_candidates_with_snapshot_slots', None),
    (0x0805bb20, 0x0201c510, 'gDuelFieldSlots', 'scan_equip_zone_candidates_with_snapshot_slots_b', None),

    # gDuelFieldSlotState = 0x0201c520 (ewram.inc) -- 2 slots
    (0x0805ba50, 0x0201c520, 'gDuelFieldSlotState', 'scan_equip_zone_candidates_with_snapshot_slot_state', None),
    (0x0805bc44, 0x0201c520, 'gDuelFieldSlotState', 'check_card_normal_summon_eligible_full_slot_state', None),

    # gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 3 slots
    (0x0805bf9c, 0x0201c600, 'gP1FieldArrayCBase', 'scan_equip_slots_eligible_for_card_arr', None),
    (0x0805c038, 0x0201c600, 'gP1FieldArrayCBase', 'scan_equip_slots_eligible_for_card_arr_b', None),
    (0x0805c170, 0x0201c600, 'gP1FieldArrayCBase', 'scan_equip_slots_eligible_banisher_guard_arr', None),

    # gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF = 0x0201d5b4 (ewram.inc computed)
    (0x0805b888, 0x0201d5b4, 'gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF', 'populate_effect_node_snapshot_effect_zone', None),

    # switchdataD internal ptr slots -- labeled as RENAME, values are internal table addresses
    # 0x0805b49c -> 0x0805b4a0 (outer switch table ptr)
    (0x0805b49c, 0x0805b4a0, 'find_zone_slot_match__outer_table', 'find_zone_slot_match_zone_dispatch_table_ptr', None),
    # 0x0805b554 -> 0x0805b558 (inner switch table ptr)
    (0x0805b554, 0x0805b558, 'find_zone_slot_match__inner_table', 'find_zone_slot_match_node_zone_dispatch_table_ptr', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # DAT_ compound pattern rename
    (0x0805b884, 'populate_effect_node_snapshot_cyber_blader_slotword',
     '0xcaa80000 = CYBER_BLADER_CID(0x1955)<<19; lsls r0,slot_word,#0x13 tests bits[12:0]==0x1955'),

    # PTR_gP1LifePoints_ renames (value 0x0201c4e0 = gP1LifePoints)
    (0x0805bf94, 'scan_equip_slots_eligible_for_card_p1lp', 'gP1LifePoints ref'),
    (0x0805c168, 'scan_equip_slots_eligible_banisher_guard_p1lp', 'gP1LifePoints ref'),
    (0x0805c1b8, 'get_lp_count_minus_zone_slot_offset_p1lp', 'gP1LifePoints ref'),
    (0x0805c2e8, 'dispatch_effect_for_neo_daedalus_slot_with_monster_count_p1lp', 'gP1LifePoints ref'),

    # switchD sub-label renames (outer switch, find_zone_slot_match_by_type_in_node_list)
    (0x0805b498, 'find_zone_slot_match__outer_dispatch',
     'outer switchD: mov pc,r0 dispatch on zone_type (25-entry table at 0x0805b4a0)'),
    (0x0805b4a0, 'find_zone_slot_match__outer_table',
     '25-entry zone_type->case jump table (case 6=zone_type_valid, case 9=zone_type_invalid)'),
    (0x0805b504, 'find_zone_slot_match__zone_type_valid',
     'zone_type in [6..30]: check slot[+0x14] field'),
    (0x0805b52c, 'find_zone_slot_match__zone_type_invalid',
     'out-of-range or no-match: return 0'),

    # switchD sub-label renames (inner switch, find_zone_slot_match_by_type_in_node_list)
    (0x0805b54e, 'find_zone_slot_match__inner_dispatch',
     'inner loop switchD: zone comparison dispatch (25-entry table at 0x0805b558)'),
    (0x0805b558, 'find_zone_slot_match__inner_table',
     '25-entry inner zone_type comparison table (case 6=node_zone_match, case 9=node_next)'),
    (0x0805b5bc, 'find_zone_slot_match__node_zone_match',
     'node.zone == slot.zone: compare slot fields'),
    (0x0805b5ce, 'find_zone_slot_match__node_next',
     'continue to next node in list'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUB: (func_addr, [(old_FUN_str, new_name_str), ...])
#    Substring replace stale FUN_ refs in existing plate comments.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # populate_effect_node_snapshot (0x0805b5f0): 2 stale FUN_
    (0x0805b5f0, [
        ('FUN_0805b990', 'scan_equip_zone_candidates_with_snapshot'),
        ('FUN_0805bc48', 'check_card_normal_summon_eligible_full'),
    ]),
    # scan_equip_zone_candidates_with_snapshot (0x0805b990): 3 stale FUN_
    (0x0805b990, [
        ('FUN_08047724', 'update_equip_target_bitmap_for_field'),
        ('FUN_0806d960', 'dispatch_field_spell_placement_display_by_state'),
        ('FUN_08090218', 'dispatch_equip_field_scan_sequence'),
    ]),
    # check_card_normal_summon_eligible_full (0x0805bc48): 1 stale FUN_
    (0x0805bc48, [
        ('FUN_0803088c', 'check_effect_slot_summon_path_eligible'),
    ]),
    # check_card_special_summon_eligible_full (0x0805bcf0): 3 stale FUN_
    (0x0805bcf0, [
        ('FUN_0809f21c', 'scan_equip_zone_for_special_summon_activation_return_zombie'),
        ('FUN_080ad974', 'dispatch_card_effect_by_card_id'),
        ('FUN_080bae6c', 'check_card_summon_eligible_by_field6'),
    ]),
    # scan_equip_slots_eligible_for_card (0x0805bf20): 1 stale FUN_
    (0x0805bf20, [
        ('FUN_0805c044', 'dispatch_equip_slot_scan_with_field6_guard'),
    ]),
]

# ===========================================================================
# MAIN
# ===========================================================================
print("=" * 60)
print("RefineF06Seg10Slots %s" % ("DRY RUN" if DRY else "LIVE"))
print("=" * 60)

print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
for entry in EQ_SLOTS:
    apply_eq(*entry)

print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
for entry in REF_SLOTS:
    apply_ref(*entry)

print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
for entry in RENAME_SLOTS:
    apply_rename(*entry)

print("\n--- D. PLATE_SUB (%d fns) ---" % len(PLATE_SUBS))
for func_addr, replacements in PLATE_SUBS:
    plate_sub(func_addr, replacements)

print("\n--- SUMMARY ---")
print("EQ=%d  REF=%d  RENAME=%d  PLATE_SUB=%d" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_SUBS)))
if FAILS:
    print("FAILS (%d): %s" % (len(FAILS), [hex(f) for f in FAILS]))
else:
    print("0 FAILS")
print("Done.")
