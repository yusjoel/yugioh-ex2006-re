# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg10Slots.py -- file 04 Seg-10 (0x08047ec0..0x08049014)
#   test_equip_target_zone14_with_ctx_clear /
#   update_equip_target_bitmap_zone_e_no_flag /
#   update_equip_bitmap_zone_e_with_slot_save /
#   update_equip_bitmap_with_cross_side_flag /
#   render_slot_card_sprite_from_descriptor /
#   render_slot_card_sprite_and_effects /
#   render_zone_sprite_with_effect_dispatch_by_slot /
#   render_slot_card_sprite_with_chaos_equip_check /
#   render_zone_sprite_with_effect_dispatch_alt /
#   enqueue_sprite_attr_for_zone_card_id_lookup /
#   enqueue_sprite_attr_by_sign /
#   enqueue_equip_zone_sprite_by_side /
#   enqueue_sprite_attr_for_slot_indicator /
#   enqueue_sprite_attr_position_by_player /
#   enqueue_sprite_attr_clamped /
#   enqueue_sprite_attr_record_with_cap /
#   submit_lp_indicator_with_slot_xor_flag /
#   submit_lp_change_indicator_with_chain_check /
#   setup_equip_slot_sprite_attr_by_card
#
# Sections:
#   A. EQ_SLOTS  (87) -- 10 new oam_attr.inc + 26 new card_info.inc + 2 new duel_field.inc
#                        + 49 reuse existing constants
#   B. REF_SLOTS (25) -- USER label on target + DATA ref + slot rename (all reuse existing globals)
#   C. PLATE_REWRITES (8 fn) -- FUN_ replacement + wrong-global-name corrections
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
    """Create equate + slot label + optional EOL."""
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

def _ref(slot, target_val, gas_label, slot_label):
    """Create USER label on target + DATA memory ref + slot label."""
    slot_addr = _addr(slot)
    target_addr = _addr(target_val)
    sym_table = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if not DRY:
        try:
            sym_table.createLabel(target_addr, gas_label, SourceType.USER_DEFINED)
            for s in sym_table.getSymbols(target_addr):
                if s.getName() == gas_label:
                    s.setPrimary()
                    break
        except Exception as e:
            print("  WARN REF target-label @ 0x%08x %s: %s" % (target_val, gas_label, e))
        try:
            ref_mgr.addMemoryReference(slot_addr, target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        except Exception as e:
            print("  WARN REF mem-ref @ 0x%08x: %s" % (slot, e))
        try:
            sym_table.createLabel(slot_addr, slot_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("  WARN REF slot-label @ 0x%08x %s: %s" % (slot, slot_label, e))
        print("  REF OK 0x%08x -> 0x%08x (%s) label=%s" % (slot, target_val, gas_label, slot_label))
    else:
        print("  DRY REF 0x%08x -> 0x%08x (%s) label=%s" % (slot, target_val, gas_label, slot_label))

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
# A. EQ_SLOTS
# ---------------------------------------------------------------------------
# Format: (slot_addr, expected_val, eq_name, slot_label, eol_or_None)
# Slot label MUST differ from eq_name (avoids GAS PC-relative "value too big").
# All new constants: oam_attr.inc (10), card_info.inc (26), duel_field.inc (2).
# All reuse constants: verify existing name used unchanged.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==========================================================================
    # render_slot_card_sprite_from_descriptor (0x08047f50)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_SLOT_SPRITE_P2 = 0x00008032
    (0x08048018, 0x00008032, 'OAM_SLOT_SPRITE_P2',
     'render_slot_card_descr_oam_p2',
     'OAM_SLOT_SPRITE_P2: P2 duel slot sprite attr0 (bit15+0x32; P1=0x32 inline)'),
    # REUSE: BANISHER_OF_THE_LIGHT_CID = 0x00001332
    (0x0804801c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'render_slot_card_descr_banisher_cid',
     'Banisher of the Light card id (0x1332)'),

    # ==========================================================================
    # render_slot_card_sprite_and_effects (0x08048020)
    # ==========================================================================
    # NEW duel_field.inc: FIELD_COPY_COUNT_FLAG = 0x00010002
    (0x08048228, 0x00010002, 'FIELD_COPY_COUNT_FLAG',
     'render_and_eff_field_copy_flag',
     'FIELD_COPY_COUNT_FLAG: bit0=mode2,bit16=copy_exists; anded with count_field_copies_of_card result'),
    # REUSE: BANISHER_OF_THE_LIGHT_CID = 0x00001332
    (0x08048224, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'render_and_eff_banisher_cid',
     None),
    # REUSE: DARK_MAGICIAN_OF_CHAOS_CID = 0x000016f8
    (0x0804822c, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID',
     'render_and_eff_dmoc_cid',
     None),
    # REUSE: OAM_ATTR1_X_CLEAR = 0xfffffe00
    (0x08048234, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',
     'render_and_eff_x_clear',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BITS13_10 = 0xffffc3ff
    (0x08048238, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10',
     'render_and_eff_clr_bits13_10',
     None),
    # REUSE: SLOT_ACTIVE_BIT14_CLR = 0xffffbfff
    (0x0804823c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',
     'render_and_eff_clr_bit14',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT17 = 0xfffdffff
    (0x08048240, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17',
     'render_and_eff_clr_bit17',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT18 = 0xfffbffff
    (0x08048244, 0xfffbffff, 'OAM_SPRITE_ATTR_CLR_BIT18',
     'render_and_eff_clr_bit18',
     None),
    # REUSE: SLOT_ACTIVE_BIT23_CLR = 0xff7fffff
    (0x08048248, 0xff7fffff, 'SLOT_ACTIVE_BIT23_CLR',
     'render_and_eff_clr_bit23',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BITS22_19 = 0xff87ffff
    (0x0804824c, 0xff87ffff, 'OAM_SPRITE_ATTR_CLR_BITS22_19',
     'render_and_eff_clr_bits22_19',
     None),
    # REUSE: OAM_EFFECT_ZONE_SPRITE_P1 = 0x00008031
    (0x08048250, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',
     'render_and_eff_effect_zone_p1',
     None),

    # ==========================================================================
    # render_zone_sprite_with_effect_dispatch_by_slot (0x08048268)
    # ==========================================================================
    # REUSE: OAM_EFFECT_ZONE_SPRITE_P1 = 0x00008031
    (0x080482f8, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',
     'dispatch_slot_effect_zone_p1',
     None),

    # ==========================================================================
    # render_slot_card_sprite_with_chaos_equip_check (0x08048364)
    # ==========================================================================
    # REUSE: OAM_EQUIP_ZONE_SPRITE_P1 = 0x00008033
    (0x0804834c, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',
     'chaos_chk_equip_zone_p1',
     None),
    # REUSE: BANISHER_OF_THE_LIGHT_CID = 0x00001332
    (0x08048350, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'chaos_chk_banisher_cid',
     None),

    # ==========================================================================
    # render_zone_sprite_with_effect_dispatch_alt (0x08048560)
    # ==========================================================================
    # REUSE: OAM_ATTR1_X_CLEAR = 0xfffffe00
    (0x0804852c, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',
     'dispatch_alt_x_clear',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BITS13_10 = 0xffffc3ff
    (0x08048530, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10',
     'dispatch_alt_clr_bits13_10',
     None),
    # REUSE: SLOT_ACTIVE_BIT14_CLR = 0xffffbfff
    (0x08048534, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',
     'dispatch_alt_clr_bit14',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT17 = 0xfffdffff
    (0x08048538, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17',
     'dispatch_alt_clr_bit17',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT18 = 0xfffbffff
    (0x0804853c, 0xfffbffff, 'OAM_SPRITE_ATTR_CLR_BIT18',
     'dispatch_alt_clr_bit18',
     None),
    # REUSE: SLOT_ACTIVE_BIT23_CLR = 0xff7fffff
    (0x08048540, 0xff7fffff, 'SLOT_ACTIVE_BIT23_CLR',
     'dispatch_alt_clr_bit23',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BITS22_19 = 0xff87ffff
    (0x08048544, 0xff87ffff, 'OAM_SPRITE_ATTR_CLR_BITS22_19',
     'dispatch_alt_clr_bits22_19',
     None),
    # REUSE: OAM_ZONE_EQUIP_SPRITE_P1 = 0x00008045
    (0x08048548, 0x00008045, 'OAM_ZONE_EQUIP_SPRITE_P1',
     'dispatch_alt_zone_equip_p1',
     None),
    # REUSE: BANISHER_OF_THE_LIGHT_CID = 0x00001332
    (0x08048520, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'dispatch_alt_banisher_cid',
     None),
    # REUSE: DARK_MAGICIAN_OF_CHAOS_CID = 0x000016f8
    (0x08048524, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID',
     'dispatch_alt_dmoc_cid',
     None),
    # REUSE: OAM_EFFECT_ZONE_SPRITE_P1 = 0x00008031
    (0x080485f0, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',
     'dispatch_alt_effect_zone_p1',
     None),
    # REUSE: BANISHER_OF_THE_LIGHT_CID = 0x00001332 (at 0x08048660)
    (0x08048660, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'dispatch_alt_banisher_cid_b',
     None),

    # ==========================================================================
    # enqueue_sprite_attr_for_zone_card_id_lookup (0x08048674)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_ZONE_CARD_ID_SPRITE_P2 = 0x0000802e
    (0x080486ac, 0x0000802e, 'OAM_ZONE_CARD_ID_SPRITE_P2',
     'zone_id_lkup_oam_p2',
     'OAM_ZONE_CARD_ID_SPRITE_P2: P2 zone card-id sprite attr0 (bit15+0x2e)'),

    # ==========================================================================
    # enqueue_sprite_attr_by_sign (0x080486b0)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_SIGN_SPRITE_P2 = 0x00008030
    (0x080486e0, 0x00008030, 'OAM_SIGN_SPRITE_P2',
     'sign_sprite_p2',
     'OAM_SIGN_SPRITE_P2: P2 sign/palette sprite attr0 (bit15+0x30)'),

    # ==========================================================================
    # enqueue_equip_zone_sprite_by_side (0x080486e4)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_EQUIP_ZONE_SIDE_P2 = 0x0000802f
    (0x08048700, 0x0000802f, 'OAM_EQUIP_ZONE_SIDE_P2',
     'equip_zone_side_p2',
     'OAM_EQUIP_ZONE_SIDE_P2: P2 equip zone side sprite attr0 (bit15+0x2f)'),

    # ==========================================================================
    # enqueue_sprite_attr_for_slot_indicator (0x08048704)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_SLOT_INDICATOR_P2 = 0x0000802b
    (0x08048720, 0x0000802b, 'OAM_SLOT_INDICATOR_P2',
     'slot_indicator_p2',
     'OAM_SLOT_INDICATOR_P2: P2 slot occupied-indicator sprite attr0 (bit15+0x2b)'),

    # ==========================================================================
    # enqueue_sprite_attr_position_by_player (0x08048724)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_POSITION_ATTR_P2 = 0x00008026
    (0x0804874c, 0x00008026, 'OAM_POSITION_ATTR_P2',
     'pos_attr_p2',
     'OAM_POSITION_ATTR_P2: P2 LP position sprite attr0 (bit15+0x26)'),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x08048748, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'pos_attr_hidden',
     None),

    # ==========================================================================
    # enqueue_sprite_attr_clamped (0x08048750)
    # ==========================================================================
    # NEW oam_attr.inc: OAM_SPRITE_COUNT_P2 = 0x00008025
    (0x0804877c, 0x00008025, 'OAM_SPRITE_COUNT_P2',
     'sprite_count_p2',
     'OAM_SPRITE_COUNT_P2: P2 sprite count extended mode attr0 (bit15+0x25)'),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x08048778, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'sprite_clamped_hidden',
     None),

    # ==========================================================================
    # enqueue_sprite_attr_record_with_cap (0x08048780)
    # ==========================================================================
    # REUSE: OAM_SPRITE_COUNT_P2 = 0x00008025 (already created above)
    (0x080487ac, 0x00008025, 'OAM_SPRITE_COUNT_P2',
     'sprite_cap_count_p2',
     None),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x080487a8, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'sprite_cap_hidden',
     None),

    # ==========================================================================
    # submit_lp_change_indicator_with_chain_check (0x080487dc)
    # ==========================================================================
    # NEW card_info.inc: HALLOWED_LIFE_BARRIER_CID = 0x00001805
    (0x0804881c, 0x00001805, 'HALLOWED_LIFE_BARRIER_CID',
     'lp_change_hallowed_barrier_cid',
     'Hallowed Life Barrier (pw=88789641; card_1681); LP display gate A'),
    # NEW card_info.inc: PIKERUS_CIRCLE_OF_ENCHANTMENT_CID = 0x00001850
    (0x08048820, 0x00001850, 'PIKERUS_CIRCLE_OF_ENCHANTMENT_CID',
     'lp_change_pikerus_cid',
     "Pikeru's Circle of Enchantment (pw=74270067; card_1747); LP display gate B"),
    # NEW card_info.inc: DES_WOMBAT_CID = 0x000018c4
    (0x08048824, 0x000018c4, 'DES_WOMBAT_CID',
     'lp_change_des_wombat_cid',
     'Des Wombat (pw=09637706; card_1844); count_available_effect_zones key'),
    # NEW card_info.inc: DARK_ROOM_OF_NIGHTMARE_CID = 0x0000159b
    (0x08048880, 0x0000159b, 'DARK_ROOM_OF_NIGHTMARE_CID',
     'lp_change_dark_room_cid',
     'Dark Room of Nightmare (pw=85562745; card_1183); LP display gate'),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT16 = 0xfffeffff
    (0x08048884, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16',
     'lp_change_clr_bit16',
     None),
    # REUSE: EQUIP_CHAIN_SENTINEL / CLR_LOWER16 = 0xffff0000
    (0x08048888, 0xffff0000, 'EQUIP_CHAIN_SENTINEL',
     'lp_change_sentinel',
     None),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x08048878, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'lp_change_hidden',
     None),
    # REUSE: OAM_SPRITE_COUNT_P2 = 0x00008025 (third usage)
    (0x0804887c, 0x00008025, 'OAM_SPRITE_COUNT_P2',
     'lp_change_count_p2',
     None),

    # ==========================================================================
    # setup_equip_slot_sprite_attr_by_card (0x0804888c)
    # ==========================================================================
    # REUSE: PLAYER_BLOCK_STRIDE = 0x00000868
    (0x08048984, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'equip_slot_stride',
     None),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x0804898c, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'equip_slot_hidden_a',
     None),
    # REUSE: EQUIP_CHAIN_SENTINEL = 0xffff0000
    (0x08048990, 0xffff0000, 'EQUIP_CHAIN_SENTINEL',
     'equip_slot_sentinel',
     None),
    # REUSE: OAM_SPRITE_ATTR_CLR_BIT16 = 0xfffeffff
    (0x08048994, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16',
     'equip_slot_clr_bit16',
     None),
    # NEW oam_attr.inc: OAM_SPRITE_ATTR_CLR_BITS20_17 = 0xffe1ffff
    (0x08048998, 0xffe1ffff, 'OAM_SPRITE_ATTR_CLR_BITS20_17',
     'equip_slot_clr_bits20_17',
     'OAM_SPRITE_ATTR_CLR_BITS20_17: AND mask clears OAM attr bits[20:17] (equip_state 4-bit field)'),
    # REUSE: SLOT_BIT21_CLR = 0xffdfffff
    (0x0804899c, 0xffdfffff, 'SLOT_BIT21_CLR',
     'equip_slot_clr_bit21',
     None),
    # NEW oam_attr.inc: OAM_SPRITE_ATTR_CLR_BITS25_22 = 0xfc3fffff
    (0x080489a0, 0xfc3fffff, 'OAM_SPRITE_ATTR_CLR_BITS25_22',
     'equip_slot_clr_bits25_22',
     'OAM_SPRITE_ATTR_CLR_BITS25_22: AND mask clears OAM attr bits[25:22] (mode 4-bit field)'),
    # NEW oam_attr.inc: OAM_SPRITE_ATTR_CLR_BIT26 = 0xfbffffff
    (0x080489a8, 0xfbffffff, 'OAM_SPRITE_ATTR_CLR_BIT26',
     'equip_slot_clr_bit26',
     'OAM_SPRITE_ATTR_CLR_BIT26: AND mask clears OAM attr bit26; setup_equip_slot_sprite_attr_by_card'),
    # REUSE: SPRITE_COUNT_P2 -- for 0x080489ac
    (0x080489ac, 0x00008025, 'OAM_SPRITE_COUNT_P2',
     'equip_slot_count_p2',
     None),
    # REUSE: REAPER_ON_NIGHTMARE_CID = 0x00001598
    (0x080489b0, 0x00001598, 'REAPER_ON_NIGHTMARE_CID',
     'equip_slot_reaper_cid',
     'Reaper on the Nightmare card id (0x1598)'),
    # NEW card_info.inc: DRILL_BUG_CID = 0x000012a7
    (0x080489b4, 0x000012a7, 'DRILL_BUG_CID',
     'equip_slot_drill_bug_cid',
     'Drill Bug (pw=88733579; card_0631)'),
    # NEW card_info.inc: WHITE_MAGICAL_HAT_CID = 0x00001018
    (0x080489b8, 0x00001018, 'WHITE_MAGICAL_HAT_CID',
     'equip_slot_white_hat_cid',
     'White Magical Hat (pw=15150365; card_0117)'),
    # NEW card_info.inc: MASKED_SORCERER_CID = 0x00001082
    (0x080489c8, 0x00001082, 'MASKED_SORCERER_CID',
     'equip_slot_masked_sorc_cid',
     'Masked Sorcerer (pw=10189126; card_0208)'),
    # NEW card_info.inc: BISTRO_BUTCHER_CID = 0x000011b1
    (0x080489cc, 0x000011b1, 'BISTRO_BUTCHER_CID',
     'equip_slot_bistro_cid',
     'The Bistro Butcher (pw=71107816; card_0436)'),
    # REUSE: MUCUS_YOLK_CID = 0x000013b2
    (0x080489e0, 0x000013b2, 'MUCUS_YOLK_CID',
     'equip_slot_mucus_yolk_cid',
     'Mucus Yolk card id (0x13b2)'),
    # NEW card_info.inc: DON_ZALOOG_CID = 0x00001532
    (0x08048a10, 0x00001532, 'DON_ZALOOG_CID',
     'equip_slot_don_zaloog_cid',
     'Don Zaloog (pw=76922029; card_1111)'),
    # REUSE: VAMPIRE_LORD_CID = 0x00001522
    (0x08048a18, 0x00001522, 'VAMPIRE_LORD_CID',
     'equip_slot_vampire_lord_cid',
     'Vampire Lord card id (0x1522)'),
    # NEW card_info.inc: TOON_MASKED_SORCERER_CID = 0x00001563
    (0x08048a30, 0x00001563, 'TOON_MASKED_SORCERER_CID',
     'equip_slot_toon_masked_cid',
     'Toon Masked Sorcerer (pw=16392422; card_1139)'),
    # NEW card_info.inc: VAMPIRE_LADY_CID = 0x00001746
    (0x08048a58, 0x00001746, 'VAMPIRE_LADY_CID',
     'equip_slot_vampire_lady_cid',
     'Vampire Lady (pw=26495087; card_1521)'),
    # Low-conf gap stub: equip_cid_15de_08048a68 = 0x000015de
    (0x08048a68, 0x000015de, 'equip_cid_15de_08048a68',
     'equip_slot_cid_15de',
     'slot_id 0x15de: no match in card-stats.s; gap stub; conf low'),
    # NEW card_info.inc: MEFIST_THE_INFERNAL_GENERAL_CID = 0x0000168b
    (0x08048a88, 0x0000168b, 'MEFIST_THE_INFERNAL_GENERAL_CID',
     'equip_slot_mefist_cid',
     'Mefist the Infernal General (pw=46820049; card_1367)'),
    # NEW card_info.inc: SASUKE_SAMURAI_3_CID = 0x000016bd
    (0x08048a90, 0x000016bd, 'SASUKE_SAMURAI_3_CID',
     'equip_slot_sasuke3_cid',
     'Sasuke Samurai #3 (pw=77379481; card_1408)'),
    # NEW card_info.inc: DARK_BLADE_THE_DRAGON_KNIGHT_CID = 0x0000183c
    (0x08048aac, 0x0000183c, 'DARK_BLADE_THE_DRAGON_KNIGHT_CID',
     'equip_slot_dark_blade_dknight_cid',
     'Dark Blade the Dragon Knight (pw=86805855; card_1728)'),
    # REUSE: SILENT_SWORDSMAN_LV5_CID = 0x00001814
    (0x08048abc, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',
     'equip_slot_silent_sw_lv5_cid',
     'Silent Swordsman LV5 card id (0x1814)'),
    # NEW card_info.inc: BRRON_MAD_KING_OF_DARK_WORLD_CID = 0x00001967
    (0x08048ad4, 0x00001967, 'BRRON_MAD_KING_OF_DARK_WORLD_CID',
     'equip_slot_brron_cid',
     'Brron, Mad King of Dark World (pw=06214884; card_1973)'),
    # NEW card_info.inc: DOOM_DOZER_CID = 0x000019ca
    (0x08048ae8, 0x000019ca, 'DOOM_DOZER_CID',
     'equip_slot_doom_dozer_cid',
     'Doom Dozer (pw=76039636; card_2045)'),
    # REUSE: PLAYER_BLOCK_STRIDE = 0x00000868 (second pool in setup fn)
    (0x08048b58, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'equip_slot_stride_b',
     None),

    # setup_equip_slot_sprite_attr_by_card continued (longer fn, more pools)
    # NEW card_info.inc: SPIRAL_SPEAR_STRIKE_CID = 0x0000187d
    (0x08048f28, 0x0000187d, 'SPIRAL_SPEAR_STRIKE_CID',
     'equip_slot_spiral_spear_cid',
     'Spiral Spear Strike (pw=49328340; card_1790)'),
    # REUSE: PLAYER_BLOCK_STRIDE = 0x00000868
    (0x08048f30, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'equip_slot_stride_c',
     None),
    # NEW card_info.inc: ROBBINS_GOBLIN_CID = 0x0000130c
    (0x08048f34, 0x0000130c, 'ROBBINS_GOBLIN_CID',
     'equip_slot_robbin_goblin_cid',
     "Robbin' Goblin (pw=88279736; card_0696)"),
    # NEW card_info.inc: SECRET_OF_THE_BANDIT_CID = 0x00001511
    (0x08048f38, 0x00001511, 'SECRET_OF_THE_BANDIT_CID',
     'equip_slot_secret_bandit_cid',
     'The Secret of the Bandit (pw=99351431; card_1084)'),
    # NEW duel_field.inc: EQUIP_ZONE_EFFECT_ATTR_OR = 0x1e501511 (low-conf packed OR mask)
    (0x08048f3c, 0x1e501511, 'EQUIP_ZONE_EFFECT_ATTR_OR',
     'equip_slot_zone_eff_attr',
     'packed equip zone effect attr OR mask; low16=0x1511 type; high16=0x1e50 mode; conf LOW'),
    # NEW card_info.inc: CESTUS_OF_DAGLA_CID = 0x000014ed
    (0x08048f40, 0x000014ed, 'CESTUS_OF_DAGLA_CID',
     'equip_slot_cestus_cid',
     'Cestus of Dagla (pw=28106077; card_1053)'),
    # NEW card_info.inc: POISON_FANGS_CID = 0x0000187b
    (0x08048f44, 0x0000187b, 'POISON_FANGS_CID',
     'equip_slot_poison_fangs_cid',
     'Poison Fangs (pw=76539047; card_1788)'),
    # REUSE: OAM_ATTR0_HIDDEN = 0x0000ffff
    (0x08048f48, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'equip_slot_hidden_b',
     None),
    # NEW card_info.inc: FREEZING_BEAST_CID = 0x000015d7
    (0x08048f4c, 0x000015d7, 'FREEZING_BEAST_CID',
     'equip_slot_freezing_beast_cid',
     'Freezing Beast (pw=85359414; card_1227)'),
    # REUSE: EQUIP_CHAIN_SENTINEL = 0xffff0000
    (0x08048f58, 0xffff0000, 'EQUIP_CHAIN_SENTINEL',
     'equip_slot_sentinel_b',
     None),
    # NEW card_info.inc: RELINQUISHED_CID = 0x00001281
    (0x08048f54, 0x00001281, 'RELINQUISHED_CID',
     'equip_slot_relinquished_cid',
     'Relinquished (pw=64631466; card_0592)'),
    # NEW card_info.inc: DES_COUNTERBLOW_CID = 0x000017b5
    (0x08048f60, 0x000017b5, 'DES_COUNTERBLOW_CID',
     'equip_slot_des_counterblow_cid',
     'Des Counterblow (pw=39131963; card_1609)'),
    # REUSE: PLAYER_BLOCK_STRIDE = 0x00000868
    (0x0804900c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'equip_slot_stride_d',
     None),
    # NEW card_info.inc: BEGONE_KNAVE_CID = 0x0000171e
    (0x08049004, 0x0000171e, 'BEGONE_KNAVE_CID',
     'equip_slot_begone_knave_cid',
     'Begone, Knave! (pw=20374520; card_1494)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS (25)
# All target globals exist in ewram.inc. No new globals needed.
# Format: (slot_addr, target_val, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # render_slot_card_sprite_from_descriptor (0x08047f50)
    (0x0804803c, 0x0201bb90, 'gEquipChainSlotRefs', 'render_and_eff_p1_base'),
    (0x08048050, 0x0201bb90, 'gEquipChainSlotRefs', 'render_and_eff_p2_base'),

    # render_slot_card_sprite_and_effects (0x08048020)
    (0x08048220, 0x0201bc54, 'gDuelEffectChainSlots', 'render_and_eff_zone_tbl'),
    (0x08048230, 0x0201bb90, 'gEquipChainSlotRefs',   'render_and_eff_turn_base'),

    # render_zone_sprite_with_effect_dispatch_by_slot (0x08048268)
    (0x08048280, 0x0201bb90, 'gEquipChainSlotRefs',   'dispatch_slot_p1_base'),
    (0x08048290, 0x0201bb90, 'gEquipChainSlotRefs',   'dispatch_slot_p2_base'),
    (0x080482f4, 0x0201bc54, 'gDuelEffectChainSlots', 'dispatch_slot_zone_tbl'),

    # render_slot_card_sprite_with_chaos_equip_check (0x08048364)
    (0x08048380, 0x0201bb90, 'gEquipChainSlotRefs',   'chaos_chk_p1_base'),
    (0x08048394, 0x0201bb90, 'gEquipChainSlotRefs',   'chaos_chk_p2_base'),
    (0x0804851c, 0x0201bc54, 'gDuelEffectChainSlots', 'chaos_chk_zone_tbl'),
    (0x08048528, 0x0201bb90, 'gEquipChainSlotRefs',   'chaos_chk_turn_base'),

    # render_zone_sprite_with_effect_dispatch_alt (0x08048560)
    (0x0804857c, 0x0201bb90, 'gEquipChainSlotRefs',   'dispatch_alt_p1_base'),
    (0x0804858c, 0x0201bb90, 'gEquipChainSlotRefs',   'dispatch_alt_p2_base'),
    (0x080485ec, 0x0201bc54, 'gDuelEffectChainSlots', 'dispatch_alt_zone_tbl'),

    # enqueue_sprite_attr_for_zone_card_id_lookup (0x08048674)
    (0x080486a8, 0x0201c4e0, 'gP1LifePoints',         'zone_id_lkup_lp_ptr'),

    # setup_equip_slot_sprite_attr_by_card (0x0804888c)
    (0x08048988, 0x0201c510, 'gDuelFieldSlots',       'equip_slot_field_slots'),
    (0x080489a4, 0x0201bb90, 'gEquipChainSlotRefs',   'equip_slot_turn_base'),
    (0x08048b54, 0x0201bb90, 'gEquipChainSlotRefs',   'equip_slot_turn_base_b'),
    (0x08048b5c, 0x0201c510, 'gDuelFieldSlots',       'equip_slot_field_slots_b'),

    # setup_equip_slot_sprite_attr_by_card continued (more pools)
    (0x08048f2c, 0x0201c510, 'gDuelFieldSlots',       'equip_slot_field_slots_c'),
    (0x08048f50, 0x0201c4e0, 'gP1LifePoints',         'equip_slot_lp_ptr'),
    (0x08048f5c, 0x0201bb90, 'gEquipChainSlotRefs',   'equip_slot_turn_base_c'),
    (0x08048f64, 0x0201e1c8, 'gEquipZoneCountTable',  'equip_slot_zone_cnt_tbl'),
    (0x08049008, 0x0201e1c8, 'gEquipZoneCountTable',  'equip_slot_zone_cnt_tbl_b'),
    (0x08049010, 0x0201c510, 'gDuelFieldSlots',       'equip_slot_field_slots_d'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES (8 functions)
# All token replacements are pure ASCII. WARN = FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # (1) update_equip_target_bitmap_zone_e_no_flag (0x08047ef0)
    #     3 unnamed callers -> addr literals
    (0x08047ef0, 'update_equip_target_bitmap_zone_e_no_flag', [
        ('FUN_080584cc', '0x080584cc'),
        ('FUN_080777d8', '0x080777d8'),
        ('FUN_0807c474', '0x0807c474'),
    ]),

    # (2) update_equip_bitmap_zone_e_with_slot_save (0x08047f00)
    #     1 unnamed caller -> addr literal
    (0x08047f00, 'update_equip_bitmap_zone_e_with_slot_save', [
        ('FUN_08059068', '0x08059068'),
    ]),

    # (3) render_zone_sprite_with_effect_dispatch_alt (0x08048560)
    #     FUN_08048268 -> rendered name
    (0x08048560, 'render_zone_sprite_with_effect_dispatch_alt', [
        ('FUN_08048268', 'render_zone_sprite_with_effect_dispatch_by_slot'),
    ]),

    # (4) enqueue_sprite_attr_by_sign (0x080486b0)
    #     FUN_08049014 -> addr, FUN_080490b4 -> partial name
    (0x080486b0, 'enqueue_sprite_attr_by_sign', [
        ('FUN_08049014', '0x08049014'),
        ('FUN_080490b4', 'duel_field_080490b4'),
    ]),

    # (5) enqueue_equip_zone_sprite_by_side (0x080486e4)
    #     5 unnamed callers -> addr literals
    (0x080486e4, 'enqueue_equip_zone_sprite_by_side', [
        ('FUN_080440b8', '0x080440b8'),
        ('FUN_08044618', '0x08044618'),
        ('FUN_080576b0', '0x080576b0'),
        ('FUN_08084738', '0x08084738'),
        ('FUN_0808f608', '0x0808f608'),
    ]),

    # (6) enqueue_sprite_attr_clamped (0x08048750)
    #     2 unnamed callers
    (0x08048750, 'enqueue_sprite_attr_clamped', [
        ('FUN_0805635c', '0x0805635c'),
        ('FUN_080572b8', 'duel_field_080572b8'),
    ]),

    # (7) enqueue_sprite_attr_record_with_cap (0x08048780)
    #     1 unnamed caller
    (0x08048780, 'enqueue_sprite_attr_record_with_cap', [
        ('FUN_08098264', '0x08098264'),
    ]),

    # (8) submit_lp_change_indicator_with_chain_check (0x080487dc)
    #     FUN_0808f938 -> real name
    (0x080487dc, 'submit_lp_change_indicator_with_chain_check', [
        ('FUN_0808f938', 'refresh_opponent_field_slots_for_card_attached'),
    ]),
]

# Additional C9 plate corrections (wrong global names) -- applied via PLATE_REWRITES extension below.
# render_slot_card_sprite_from_descriptor, render_slot_card_sprite_and_effects,
# render_zone_sprite_with_effect_dispatch_by_slot, render_slot_card_sprite_with_chaos_equip_check,
# render_zone_sprite_with_effect_dispatch_alt:
#   "gDuelFieldSlots=0x0201bc54" or "gDuelFieldSlots_ext=0x0201bc54" -> "gDuelEffectChainSlots=0x0201bc54"
#   "gDuelTurnStruct=0x0201bb90" -> "gEquipChainSlotRefs=0x0201bb90"
C9_CORRECTIONS = [
    (0x08047f50, 'render_slot_card_sprite_from_descriptor', [
        ('gDuelFieldSlots=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelFieldSlots_ext=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
    ]),
    (0x08048020, 'render_slot_card_sprite_and_effects', [
        ('gDuelFieldSlots=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelFieldSlots_ext=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelTurnStruct=0x0201bb90', 'gEquipChainSlotRefs=0x0201bb90'),
    ]),
    (0x08048268, 'render_zone_sprite_with_effect_dispatch_by_slot', [
        ('gDuelFieldSlots=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelFieldSlots_ext=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelTurnStruct=0x0201bb90', 'gEquipChainSlotRefs=0x0201bb90'),
    ]),
    (0x08048364, 'render_slot_card_sprite_with_chaos_equip_check', [
        ('gDuelFieldSlots=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelFieldSlots_ext=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelTurnStruct=0x0201bb90', 'gEquipChainSlotRefs=0x0201bb90'),
    ]),
    (0x08048560, 'render_zone_sprite_with_effect_dispatch_alt', [
        ('gDuelFieldSlots=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelFieldSlots_ext=0x0201bc54', 'gDuelEffectChainSlots=0x0201bc54'),
        ('gDuelTurnStruct=0x0201bb90', 'gEquipChainSlotRefs=0x0201bb90'),
    ]),
]

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg10Slots (DRY=%s) ===" % DRY)
    print("  Seg-10: 0x08047ec0..0x08049014, 19 fn")
    print("  EQ=%d  REF=%d  PLATE_FN=%d  C9_FN=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(PLATE_REWRITES), len(C9_CORRECTIONS)))

    # C4 ROM value check before applying
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
    # Also check REF slots
    for slot, target_val, gas_label, slot_label in REF_SLOTS:
        ok, msg = _check(slot, target_val)
        if not ok:
            print("  FAIL C4 REF 0x%08x %s: %s" % (slot, gas_label, msg))
            fails += 1
        else:
            if DRY:
                print("  OK   C4 REF 0x%08x %s=0x%08x" % (slot, gas_label, target_val))
    if fails > 0:
        print("  !! %d C4 failures -- ABORT" % fails)
        return

    print("  C4 all OK (%d EQ + %d REF slots)" % (len(EQ_SLOTS), len(REF_SLOTS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for entry in EQ_SLOTS:
        slot, expected, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _eq(slot, eq_name, slot_label, eol)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot, target_val, gas_label, slot_label in REF_SLOTS:
        _ref(slot, target_val, gas_label, slot_label)

    # D. PLATE_REWRITES (FUN_ substitutions)
    print("\n--- D. PLATE_REWRITES (%d fn) ---" % len(PLATE_REWRITES))
    total_plate_warns = 0
    listing = currentProgram.getListing()
    for fn_addr, fn_name, replacements in PLATE_REWRITES:
        addr = _addr(fn_addr)
        cu = listing.getCodeUnitAt(addr)
        if cu is not None:
            old = cu.getComment(CodeUnit.PLATE_COMMENT)
            if old:
                for old_tok, new_tok in replacements:
                    if old_tok not in old:
                        total_plate_warns += 1
        _plate(fn_addr, fn_name, replacements)

    # D2. C9 corrections (wrong global names)
    print("\n--- D2. C9 wrong-global-name corrections (%d fn) ---" % len(C9_CORRECTIONS))
    for fn_addr, fn_name, replacements in C9_CORRECTIONS:
        addr = _addr(fn_addr)
        cu = listing.getCodeUnitAt(addr)
        if cu is not None:
            old = cu.getComment(CodeUnit.PLATE_COMMENT)
            if old:
                found_any = False
                for old_tok, new_tok in replacements:
                    if old_tok in old:
                        found_any = True
                if found_any:
                    _plate(fn_addr, fn_name, replacements)
                else:
                    print("  INFO C9 0x%08x (%s) no matching tokens -- already corrected or absent" % (
                        fn_addr, fn_name))
            else:
                print("  INFO C9 0x%08x (%s) no plate comment" % (fn_addr, fn_name))
        else:
            print("  WARN C9 no code unit @ 0x%08x (%s)" % (fn_addr, fn_name))

    print("\n=== RefineF04Seg10Slots DONE ===")
    print("  EQ=%d  REF=%d  PLATE_FN=%d  plate_warns=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(PLATE_REWRITES), total_plate_warns))
    if total_plate_warns > 0:
        print("  !! plate WARNs detected -- review before commit")

main()
