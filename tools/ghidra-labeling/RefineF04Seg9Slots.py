# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg9Slots.py -- file 04 Seg-9 (0x08047990..0x08047ec0)
#   check_equip_slot_eligible_in_target_bitmap /
#   update_equip_target_bitmap_by_card_type /
#   update_equip_target_bitmap_zone14 /
#   query_equip_target_bitmap_with_zone_struct /
#   update_equip_target_bitmap_zone15 /
#   render_equip_zone_bitmap_sprite_by_chain /
#   forward_equip_bitmap_update_with_full_mask /
#   test_equip_target_slot_zone11 /
#   query_equip_zone_slot_target_bit /
#   forward_equip_bitmap_update_zone11 /
#   test_equip_target_slot_zone13 /
#   test_equip_target_slot_zone13_crossside /
#   update_equip_target_bitmap_zone_d_no_flag /
#   reset_equip_slot_ctx_with_bitmap_update_zone_d /
#   test_equip_target_zone13_with_slot_parity_flag /
#   submit_equip_sprite_if_slot_eligible /
#   submit_equip_sprite_samsara_zone_select /
#   prepare_equip_slot_ctx_for_bitmap_update /
#   test_equip_target_slot_zone14 /
#   test_equip_target_slot_zone14_with_flags
#
# Sections:
#   A. EQ_SLOTS  (14) -- all reuse existing constants, 0 new
#   B. REF_SLOTS  (0) -- none
#   C. RENAME_SLOTS (0) -- none
#   D. PLATE_REWRITES (6 fn) -- FUN_/DAT_/wrong-global-name substr replace
#
# NOTE: All plate text is pure ASCII. No CJK.

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
# helpers
# ---------------------------------------------------------------------------
def _addr(x):
    return toAddr(x)

def _check(slot, expected):
    mem = currentProgram.getMemory()
    try:
        val = mem.getInt(_addr(slot)) & 0xffffffff
    except Exception as e:
        return False, "read-error: %s" % e
    if val == expected:
        return True, None
    return False, "ROM=0x%08x expected=0x%08x" % (val, expected)

def _eq(slot, eq_name, slot_label, eol=None):
    """Create equate + slot label + optional EOL. Values read from ROM."""
    addr = _addr(slot)
    listing = currentProgram.getListing()
    sym_table = currentProgram.getSymbolTable()
    eq_table = currentProgram.getEquateTable()

    mem = currentProgram.getMemory()
    try:
        val = mem.getInt(addr) & 0xffffffff
    except Exception as e:
        print("  WARN EQ read-error @ 0x%08x: %s" % (slot, e))
        return

    if not DRY:
        try:
            eq = eq_table.getEquate(eq_name)
            if eq is None:
                eq = eq_table.createEquate(eq_name, val)
        except Exception as e:
            print("  WARN EQ create @ 0x%08x %s: %s" % (slot, eq_name, e))
            return
        try:
            eq.addReference(addr, 0)
        except Exception:
            pass
        try:
            sym_table.createLabel(addr, slot_label, SourceType.USER_DEFINED)
        except Exception:
            pass
        if eol:
            try:
                listing.setComment(addr, CodeUnit.EOL_COMMENT, eol)
            except Exception:
                pass
        print("  EQ OK 0x%08x %s label=%s" % (slot, eq_name, slot_label))
    else:
        print("  DRY EQ 0x%08x %s=%s label=%s" % (slot, eq_name, hex(val), slot_label))

def _plate(fn_addr, fn_name, replacements):
    """Substring-replace tokens in plate comment. WARN if token not found."""
    listing = currentProgram.getListing()
    addr = _addr(fn_addr)
    cu = listing.getCodeUnitAt(addr)
    if cu is None:
        print("  WARN PLATE no code unit @ 0x%08x (%s)" % (fn_addr, fn_name))
        return
    old = cu.getComment(CodeUnit.PLATE_COMMENT)
    if old is None:
        old = ""
    new = old
    warns = 0
    for old_tok, new_tok in replacements:
        if old_tok not in new:
            print("  WARN PLATE 0x%08x (%s): token '%s' not found" % (fn_addr, fn_name, old_tok))
            warns += 1
        else:
            new = new.replace(old_tok, new_tok)
    if new == old and warns == 0:
        print("  WARN PLATE no-change @ 0x%08x (%s) -- check tokens" % (fn_addr, fn_name))
        return
    if not DRY:
        try:
            listing.setComment(addr, CodeUnit.PLATE_COMMENT, new)
            print("  PLATE OK 0x%08x (%s) -- %d tokens replaced, %d warns" % (
                fn_addr, fn_name, len(replacements) - warns, warns))
        except Exception as e:
            print("  WARN PLATE set @ 0x%08x: %s" % (fn_addr, e))
    else:
        print("  DRY PLATE 0x%08x (%s) -- %d tokens, %d warns" % (
            fn_addr, fn_name, len(replacements), warns))

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, expected_val, eq_name, slot_label, eol_or_None)
# All 14 slots reuse existing constants from ewram.inc / card_info.inc.
# Slot label MUST differ from eq_name to avoid GAS PC-relative conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- update_equip_target_bitmap_by_card_type (0x080479c4) ---
    (0x08047a0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'update_equip_bitmap_by_cardtype_stride',
     'PLAYER_BLOCK_STRIDE: 0x868 bytes per player block'),
    (0x08047a10, 0x0201c510, 'gDuelFieldSlots',
     'update_equip_bitmap_by_cardtype_slots',
     None),

    # --- render_equip_zone_bitmap_sprite_by_chain (0x08047aa0) ---
    (0x08047b0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'render_equip_zone_bmp_sprite_stride',
     None),
    (0x08047b10, 0x0201c510, 'gDuelFieldSlots',
     'render_equip_zone_bmp_sprite_slots_a',
     None),
    (0x08047b14, 0x0201d9c0, 'gEquipNodePool',
     'render_equip_zone_bmp_sprite_node_pool',
     None),
    (0x08047b18, 0x000017d5, 'DARK_MIMIC_LV1_CID',
     'render_equip_zone_bmp_sprite_cid_a',
     'Dark Mimic LV1 card id (0x17d5)'),
    (0x08047b64, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',
     'render_equip_zone_bmp_sprite_cid_b',
     'Silent Swordsman LV5 card id (0x1814)'),
    (0x08047b68, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'render_equip_zone_bmp_sprite_stride_b',
     None),
    (0x08047b6c, 0x0201c510, 'gDuelFieldSlots',
     'render_equip_zone_bmp_sprite_slots_b',
     None),

    # --- test_equip_target_zone13_with_slot_parity_flag (0x08047cd4) ---
    (0x08047d20, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'test_zone13_parity_stride',
     None),
    (0x08047d24, 0x0201c510, 'gDuelFieldSlots',
     'test_zone13_parity_slots',
     None),

    # --- submit_equip_sprite_if_slot_eligible (0x08047d28) ---
    (0x08047d8c, 0x000014e2, 'SUPER_REJUVENATION_CID',
     'submit_equip_sprite_if_eligible_cid',
     'Super Rejuvenation card id (0x14e2)'),

    # --- submit_equip_sprite_samsara_zone_select (0x08047d9c) ---
    (0x08047e0c, 0x000019da, 'SAMSARA_CID',
     'submit_equip_sprite_samsara_cid_a',
     'Samsara card id (0x19da)'),
    (0x08047e10, 0x000014e2, 'SUPER_REJUVENATION_CID',
     'submit_equip_sprite_samsara_cid_b',
     None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: none
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (fn_addr, fn_name, [(old_tok, new_tok), ...])
# All text pure ASCII. WARN is treated as FAIL (no commit if warns > 0).
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # (1) update_equip_target_bitmap_by_card_type: 1 FUN_ token
    (0x080479c4, 'update_equip_target_bitmap_by_card_type', [
        ('FUN_0807a9c8', 'dispatch_equip_banisher_activation_by_state'),
    ]),

    # (2) update_equip_target_bitmap_zone14: 3 FUN_ tokens
    (0x08047a14, 'update_equip_target_bitmap_zone14', [
        ('FUN_08065698', 'set_equip_partner_flags_with_bitmap_refresh'),
        ('FUN_0806a334', 'dispatch_equip_slot_sprite_by_field6_range_and_zone14'),
        ('FUN_0806ecb0', 'apply_equip_activation_if_zone_entry_vacant'),
    ]),

    # (3) update_equip_target_bitmap_zone15: 1 FUN_ token
    (0x08047a80, 'update_equip_target_bitmap_zone15', [
        ('FUN_080576b0', 'tick_equip_chain_sprite_and_spell_zone_seq'),
    ]),

    # (4) render_equip_zone_bitmap_sprite_by_chain: wrong-global-name + CID correction
    #     gDuelFieldSlots_A -> gDuelFieldSlots
    #     gDuelFieldSlots_B -> gEquipNodePool
    #     CARD_ID_B=0x1814 (The All-Seeing White Tiger) -> SILENT_SWORDSMAN_LV5_CID=0x1814
    (0x08047aa0, 'render_equip_zone_bitmap_sprite_by_chain', [
        ('gDuelFieldSlots_A', 'gDuelFieldSlots'),
        ('gDuelFieldSlots_B', 'gEquipNodePool'),
        ('CARD_ID_B=0x1814 (The All-Seeing White Tiger)', 'SILENT_SWORDSMAN_LV5_CID=0x1814'),
    ]),

    # (5) test_equip_target_zone13_with_slot_parity_flag: wrong-global-name correction
    #     gDuelFieldSlots_A -> gDuelFieldSlots
    (0x08047cd4, 'test_equip_target_zone13_with_slot_parity_flag', [
        ('gDuelFieldSlots_A', 'gDuelFieldSlots'),
    ]),

    # (6) submit_equip_sprite_if_slot_eligible: DAT_ old name -> constant name
    #     DAT_08047d8c=0x14e2 -> SUPER_REJUVENATION_CID=0x14e2
    (0x08047d28, 'submit_equip_sprite_if_slot_eligible', [
        ('DAT_08047d8c=0x14e2', 'SUPER_REJUVENATION_CID=0x14e2'),
    ]),
]

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg9Slots (DRY=%s) ===" % DRY)
    print("  Seg-9: 0x08047990..0x08047ec0, 20 fn")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FN=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # C4 value check before applying
    print("\n--- C4 ROM value check (%d slots) ---" % len(EQ_SLOTS))
    fails = 0
    for entry in EQ_SLOTS:
        slot, expected, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        ok, msg = _check(slot, expected)
        if not ok:
            print("  FAIL C4 0x%08x %s: %s" % (slot, eq_name, msg))
            fails += 1
        else:
            if DRY:
                print("  OK   C4 0x%08x %s=0x%08x" % (slot, eq_name, expected))
    if fails > 0:
        print("  !! %d C4 failures -- ABORT" % fails)
        return

    print("  C4 all OK (%d slots)" % len(EQ_SLOTS))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for entry in EQ_SLOTS:
        slot, expected, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _eq(slot, eq_name, slot_label, eol)

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS (none)
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d fn) ---" % len(PLATE_REWRITES))
    total_plate_warns = 0
    for fn_addr, fn_name, replacements in PLATE_REWRITES:
        # count pre-warns by checking tokens
        listing = currentProgram.getListing()
        addr = _addr(fn_addr)
        cu = listing.getCodeUnitAt(addr)
        if cu is not None:
            old = cu.getComment(CodeUnit.PLATE_COMMENT)
            if old:
                for old_tok, new_tok in replacements:
                    if old_tok not in old:
                        total_plate_warns += 1
        _plate(fn_addr, fn_name, replacements)

    print("\n=== RefineF04Seg9Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FN=%d  plate_warns=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), total_plate_warns))
    if total_plate_warns > 0:
        print("  !! plate WARNs detected -- review before commit")

main()
