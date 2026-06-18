# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4aSlots.py -- F09 Seg-4a (0x080719fc..0x08072404)
#   setup_equip_oam_entry_for_neo_daedalus_zone14 + dispatch_field_spell_display_by_activation_state
#   + dispatch_spirit_monster_zone_sprite_by_card_id + tick_equip_activation_zone13_oam_state
#   + enqueue_slot_card_sprite_if_effect_node_active + dispatch_equip_zone_sprite_by_zone_bit4_state
#   + refresh_equip_zone_bitmap_with_full_mask + tick_equip_lp_row_sprite_extended_state
#   + dispatch_banisher_equip_zone_sprite_by_target_slot (9 fn)
#
#   EQ=38 (36 REUSE + 2 NEW: YAMATA_DRAGON_CID + DARK_DUST_SPIRIT_CID)
#   RENAME=2 (DAT_08071ad4 -> neo_daedalus_z14_sub_stubs_1ad4;
#             DAT_08072004 -> field_spell_dispatch_sub_stubs_2004)
#   PLATE=1 (dispatch_spirit_monster_zone_sprite_by_card_id: callee-swap fix at L7081)
#   DISASM=4 blocks (B1/B3: fn_eligible stubs; B2/B4: raw-dispatch sub-stubs)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_230753-pre-F09Seg4a

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val):
    """Read 4-byte LE from slot_addr and compare to expected_val. Return True on match."""
    mem = currentProgram.getMemory()
    addr = _addr(slot_addr)
    try:
        b0 = mem.getByte(addr) & 0xff
        b1 = mem.getByte(_addr(slot_addr + 1)) & 0xff
        b2 = mem.getByte(_addr(slot_addr + 2)) & 0xff
        b3 = mem.getByte(_addr(slot_addr + 3)) & 0xff
        actual = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
        if actual != expected_val:
            print("[FAIL] _check @ 0x%08x: expected=0x%08x actual=0x%08x -- SKIPPING" % (
                slot_addr, expected_val, actual))
            return False
        return True
    except Exception as e:
        print("[FAIL] _check @ 0x%08x: %s -- SKIPPING" % (slot_addr, e))
        return False


def apply_equate(slot_addr, value, eq_name, slot_label, eol_text=None):
    if not _check(slot_addr, value):
        return
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl  = currentProgram.getEquateTable()
    addr = _addr(slot_addr)

    # Create equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        try:
            eq = eq_tbl.createEquate(eq_name, value)
            print("[EQ] created %s = 0x%x" % (eq_name, value))
        except Exception as e:
            print("[WARN] createEquate %s: %s" % (eq_name, e))
    else:
        print("[EQ] reuse %s = 0x%x" % (eq_name, value))
    if eq is not None:
        try:
            eq.addReference(addr, 0)
        except Exception as e:
            print("[WARN] addReference %s @ 0x%08x: %s" % (eq_name, slot_addr, e))

    # Create slot label
    existing = [s.getName() for s in sym_tbl.getSymbols(addr)]
    if slot_label not in existing:
        try:
            sym_tbl.createLabel(addr, slot_label, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x" % (slot_label, slot_addr))
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (slot_label, e))

    # EOL comment
    if eol_text:
        cu = listing.getCodeUnitAt(addr)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol_text)


def main():
    print("=== RefineF09Seg4aSlots (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    # =========================================================================
    # A. EQ_SLOTS: 38 equate slots (36 REUSE + 2 NEW)
    # Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
    # =========================================================================
    EQ_SLOTS = [

        # ---- setup_equip_oam_entry_for_neo_daedalus_zone14 (0x080719fc..0x08071bdb) ----
        (0x08071a80, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1a80', None),
        (0x08071a84, 0x0201c8f8, 'gP1HandSlotArray',      'gp1hand_1a84', None),
        (0x08071bfc, 0x0201b290, 'gDuelPhaseFlags',       'gduel_phase_1bfc', None),
        (0x08071c44, 0x0201c4e0, 'gP1LifePoints',         'gp1lp_1c44', None),
        (0x08071c48, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1c48', None),
        (0x08071c4c, 0x0201e2a0, 'gDuelCardCtxBase',      'gduel_ctx_1c4c', None),
        (0x08071ca4, 0x0201c4e0, 'gP1LifePoints',         'gp1lp_1ca4', None),
        (0x08071ca8, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1ca8', None),
        (0x08071cac, 0x0201e2a0, 'gDuelCardCtxBase',      'gduel_ctx_1cac', None),
        (0x08071ccc, 0x000001b7, 'lookup_equip_score_b_0x1b7', 'lookup_score_1ccc', None),
        (0x08071cf4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1cf4', None),
        (0x08071cf8, 0x0201c4e0, 'gP1LifePoints',         'gp1lp_1cf8', None),
        (0x08071d54, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1d54', None),
        (0x08071d58, 0x00008056, 'OAM_EFFECT_SLOT_TILE_P1','oam_effect_tile_p1_1d58',
         'OAM_EFFECT_SLOT_TILE_P1=0x8056: OAM tile offset for P1 effect slot sprite'),
        (0x08071d5c, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1d5c', None),
        (0x08071d60, 0x0201c740, 'gP1SlotSetCodeArray',   'gp1slot_set_code_1d60', None),

        # ---- dispatch_spirit_monster_zone_sprite_by_card_id (0x08071d64..0x08071e97) ----
        (0x08071dd0, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1dd0', None),
        (0x08071dd4, 0x0201c510, 'gDuelFieldSlots',       'gduel_slots_1dd4', None),
        (0x08071df8, 0x00001503, 'OTOHIME_CID',           'otohime_cid_1df8',
         'OTOHIME_CID=0x1503: Otohime; BST pivot in dispatch_spirit_monster_zone_sprite_by_card_id'),
        (0x08071e0c, 0x00001501, 'YAMATA_DRAGON_CID',     'yamata_cid_1e0c',
         'YAMATA_DRAGON_CID=0x1501: Yamata Dragon (pw=76862289); BST -> dispatch_equip_draw_counter_sprite_tick'),
        (0x08071e24, 0x00001506, 'FUSHI_NO_TORI_CID',     'fushi_no_tori_cid_1e24',
         'FUSHI_NO_TORI_CID=0x1506: Fushi No Tori; BST -> submit_equip_lp_indicators_with_bar'),
        (0x08071e38, 0x00001526, 'DARK_DUST_SPIRIT_CID',  'dark_dust_spirit_cid_1e38',
         'DARK_DUST_SPIRIT_CID=0x1526: Dark Dust Spirit (pw=89111398); BST -> submit_equip_zone_bitmap_pair_update'),
        (0x08071e3c, 0x00001694, 'TSUKUYOMI_CID',         'tsukuyomi_cid_1e3c',
         'TSUKUYOMI_CID=0x1694: Tsukuyomi; BST -> dispatch_equip_slot_sprite_if_zone_entry_active'),
        (0x08071f18, 0x0201b290, 'gDuelPhaseFlags',       'gduel_phase_1f18', None),
        (0x08071f1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_1f1c', None),
        (0x08071f20, 0x0201c510, 'gDuelFieldSlots',       'gduel_slots_1f20', None),

        # ---- enqueue_slot_card_sprite_if_effect_node_active (0x08072104..0x08072153) ----
        (0x080721b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_21b0', None),
        (0x080721b4, 0x0201c510, 'gDuelFieldSlots',       'gduel_slots_21b4', None),

        # ---- refresh_equip_zone_bitmap_with_full_mask (0x0807220c..0x08072227) ----
        (0x0807224c, 0x0201b290, 'gDuelPhaseFlags',       'gduel_phase_224c', None),

        # ---- tick_equip_lp_row_sprite_extended_state (0x08072228..0x080723cf) ----
        (0x080722a8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_22a8', None),
        (0x080722ac, 0x0201c4e0, 'gP1LifePoints',         'gp1lp_22ac', None),
        (0x080722b0, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF','lp_card_track_off_22b0', None),
        (0x080722b4, 0x0201e2a0, 'gDuelCardCtxBase',      'gduel_ctx_22b4', None),
        (0x080722d8, 0x000001b9, 'lookup_equip_score_b_0x1b9', 'lookup_score_22d8', None),
        (0x080722fc, 0x0201c4e0, 'gP1LifePoints',         'gp1lp_22fc', None),

        # ---- dispatch_banisher_equip_zone_sprite_by_target_slot (0x080723d0..0x08072403) ----
        (0x08072374, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_2374', None),
        (0x08072378, 0x00000868, 'PLAYER_BLOCK_STRIDE',   'player_stride_2378', None),
        (0x0807237c, 0x0201c600, 'gP1FieldArrayCBase',    'gp1field_arr_237c', None),
    ]

    if DRY:
        print("[dry] Would apply %d EQ_SLOTS" % len(EQ_SLOTS))
        for s in EQ_SLOTS:
            print("  0x%08x  %s  = 0x%08x" % (s[0], s[2], s[1]))
    else:
        fail_count = 0
        for slot_addr, value, eq_name, slot_label, eol in EQ_SLOTS:
            if not _check(slot_addr, value):
                fail_count += 1
                continue
            apply_equate(slot_addr, value, eq_name, slot_label, eol)
        print("[EQ] done: %d slots, %d skipped" % (len(EQ_SLOTS), fail_count))

    # =========================================================================
    # B. RENAME_SLOTS: 2 block-start labels (DAT_ -> semantic name + EOL)
    # =========================================================================
    RENAME_SLOTS = [
        (0x08071ad4, 'neo_daedalus_z14_sub_stubs_1ad4',
         'raw-dispatch sub-stubs: 7 entry-pts; B2 DISASM'),
        (0x08072004, 'field_spell_dispatch_sub_stubs_2004',
         'raw-dispatch sub-stubs: 11 entry-pts; B4 DISASM'),
    ]

    if DRY:
        print("[dry] Would apply %d RENAME_SLOTS" % len(RENAME_SLOTS))
        for s in RENAME_SLOTS:
            print("  0x%08x  -> %s" % (s[0], s[1]))
    else:
        for slot_addr, new_label, eol in RENAME_SLOTS:
            addr = _addr(slot_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(addr)]
            if new_label not in existing:
                try:
                    sym_tbl.createLabel(addr, new_label, SourceType.USER_DEFINED)
                    print("[RENAME] %s @ 0x%08x" % (new_label, slot_addr))
                except Exception as e:
                    print("[WARN] RENAME createLabel %s: %s" % (new_label, e))
            else:
                print("[RENAME] already present: %s @ 0x%08x" % (new_label, slot_addr))
            # Set primary
            for sym in sym_tbl.getSymbols(addr):
                if sym.getName() == new_label:
                    try:
                        sym.setPrimary()
                    except Exception as e:
                        print("[WARN] setPrimary %s: %s" % (new_label, e))
                    break
            # EOL
            cu = listing.getCodeUnitAt(addr)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    # =========================================================================
    # C. PLATE-1: Fix callee-swap in dispatch_spirit_monster_zone_sprite_by_card_id
    #    Function at 0x08071d64
    #    OLD substring: "0x14ff Yata-Garasu -> dispatch_equip_draw_counter_sprite_tick,
    #                    0x1501 Yamata Dragon / 0x1502 Great Long Nose
    #                    -> enqueue_spirit_zone_sprite_with_lp_check"
    #    NEW (corrected): "0x14ff Yata-Garasu -> enqueue_spirit_zone_sprite_with_lp_check,
    #                      0x1501 Yamata Dragon -> dispatch_equip_draw_counter_sprite_tick,
    #                      0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check"
    # =========================================================================
    PLATE_FUNC_ADDR = 0x08071d64
    PLATE_OLD_SUB = "0x14ff Yata-Garasu -> dispatch_equip_draw_counter_sprite_tick, 0x1501 Yamata Dragon / 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check"
    PLATE_NEW_SUB = "0x14ff Yata-Garasu -> enqueue_spirit_zone_sprite_with_lp_check, 0x1501 Yamata Dragon -> dispatch_equip_draw_counter_sprite_tick, 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check"

    if DRY:
        print("[dry] PLATE-1: would fix callee-swap at 0x%08x" % PLATE_FUNC_ADDR)
        print("  OLD sub: %s" % PLATE_OLD_SUB)
        print("  NEW sub: %s" % PLATE_NEW_SUB)
    else:
        fn_addr = _addr(PLATE_FUNC_ADDR)
        fn_obj = currentProgram.getListing().getFunctionAt(fn_addr)
        if fn_obj is None:
            print("[FAIL] PLATE-1: no function found at 0x%08x" % PLATE_FUNC_ADDR)
        else:
            cu = listing.getCodeUnitAt(fn_addr)
            if cu is None:
                print("[FAIL] PLATE-1: no CodeUnit at 0x%08x" % PLATE_FUNC_ADDR)
            else:
                current_plate = cu.getComment(CodeUnit.PLATE_COMMENT)
                if current_plate is None:
                    print("[FAIL] PLATE-1: no PLATE comment at 0x%08x" % PLATE_FUNC_ADDR)
                elif PLATE_OLD_SUB not in current_plate:
                    print("[FAIL] PLATE-1: old substring NOT found in plate at 0x%08x -- substring may have drifted" % PLATE_FUNC_ADDR)
                    print("  Current plate (first 300 chars): %s" % current_plate[:300])
                else:
                    new_plate = current_plate.replace(PLATE_OLD_SUB, PLATE_NEW_SUB)
                    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
                    print("[PLATE-1] callee-swap fixed at 0x%08x" % PLATE_FUNC_ADDR)

    # =========================================================================
    # D. DISASM: 4 blocks
    #   B1: fn_eligible_fiber_jar_1a94 @ 0x08071a94  (0x08071a92/0x2a)
    #   B2: 7 sub-stubs neo_daedalus_z14_sub_stubs @ 0x08071ad4  (0x08071ad4/0x108)
    #   B3: fn_eligible_fengsheng_mirror_1f58 @ 0x08071f58  (0x08071f56/0x32)
    #   B4: 11 sub-stubs field_spell_dispatch_sub_stubs @ 0x08072004  (0x08072004/0x100)
    # =========================================================================

    # ----- B1: fn_eligible_fiber_jar_1a94 -----
    print("\n--- BLOCK B1: fn_eligible_fiber_jar_1a94 @ 0x08071a94 ---")
    B1_CLEAR_START = 0x08071a94  # skip 2-byte pad at 0x08071a92
    B1_CLEAR_END   = 0x08071abb  # end of literal pool (inclusive)
    B1_ENTRY       = 0x08071a94
    B1_LABEL       = 'fn_eligible_fiber_jar_1a94'
    B1_EOL         = 'fn_eligible stub: Fiber Jar (CID=0x14fb); FS table THUMB+1 ref @GBA:0x09e43c88'
    # Literal pool: 0x08071ab4=gP1HandSlotArray(0x0201c8f8), 0x08071ab8=? (need to force DWord)
    B1_POOL = [
        (0x08071ab4, 0x0201c8f8, 'gp1hand_pool_1ab4',
         'gP1HandSlotArray=0x0201c8f8; literal pool fn_eligible_fiber_jar_1a94'),
        (0x08071ab8, None, 'pool_1ab8', 'literal pool fn_eligible_fiber_jar_1a94'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B1_CLEAR_START, B1_CLEAR_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B1_ENTRY)
        print("[dry] createLabel %s" % B1_LABEL)
        for pa, pv, pl, pe in B1_POOL:
            print("[dry] createDWord @ 0x%08x  label=%s" % (pa, pl))
    else:
        a_b1_lo = _addr(B1_CLEAR_START)
        a_b1_hi = _addr(B1_CLEAR_END)
        a_b1_en = _addr(B1_ENTRY)
        print("[B1.1] clearListing 0x%08x..0x%08x" % (B1_CLEAR_START, B1_CLEAR_END))
        try:
            clearListing(a_b1_lo, a_b1_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B1: %s" % e)
        print("[B1.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b1_lo, a_b1_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B1.3] DisassembleCommand @ 0x%08x" % B1_ENTRY)
        cmd = DisassembleCommand(a_b1_en, None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B1: %s" % cmd.getStatusMsg())
        print("[B1.4] createLabel %s" % B1_LABEL)
        existing = [s.getName() for s in sym_tbl.getSymbols(a_b1_en)]
        if B1_LABEL not in existing:
            sym_tbl.createLabel(a_b1_en, B1_LABEL, SourceType.USER_DEFINED)
            print("       label created")
        else:
            print("       label already present")
        cu = listing.getCodeUnitAt(a_b1_en)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, B1_EOL)
            print("       EOL set")
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B1_POOL:
            print("[B1.5] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
            pa = _addr(pool_addr)
            try:
                clearListing(pa, _addr(pool_addr + 3))
            except Exception as e:
                print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
            d = listing.createData(pa, DWordDataType.dataType)
            if d is not None:
                print("       DWord created")
            else:
                print("[WARN] createData failed @ 0x%08x" % pool_addr)
            existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
            if pool_label not in existing_p:
                sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
            cu_p = listing.getCodeUnitAt(pa)
            if cu_p is not None:
                cu_p.setComment(CodeUnit.EOL_COMMENT, pool_eol)

    # ----- B2: 7 sub-stubs inside block 0x08071ad4..0x08071bdb -----
    print("\n--- BLOCK B2: neo_daedalus_z14_sub_stubs @ 0x08071ad4..0x08071bdb ---")
    B2_RANGE_START = 0x08071ad4
    B2_RANGE_END   = 0x08071bdb  # inclusive (fn starts at 0x08071bdc)

    B2_STUBS = [
        (0x08071ad4, 'field_spell_sub_1ad4',
         'raw-dispatch sub-stub 1 (dispatch table entry 0x71ad0); 6-entry table @ 0x71abc..0x71ad0'),
        (0x08071b02, 'field_spell_sub_1b02', None),
        (0x08071b24, 'field_spell_sub_1b24', None),
        (0x08071b30, 'field_spell_sub_1b30', None),
        (0x08071b64, 'field_spell_sub_1b64', None),
        (0x08071ba0, 'field_spell_sub_1ba0', None),
        (0x08071bbc, 'field_spell_sub_1bbc',
         'raw-dispatch sub-stub 7 (dispatch table entry 0x71abc)'),
    ]
    # Known literal pool words in B2 block (need force DWord)
    B2_POOL = [
        (0x08071b28, None, 'pool_1b28', 'literal pool inside field_spell_sub_1b24'),
        (0x08071b2c, None, 'pool_1b2c', 'literal pool inside field_spell_sub_1b24'),
        (0x08071b58, None, 'pool_1b58', 'literal pool inside field_spell_sub_1b30'),
        (0x08071b5c, None, 'pool_1b5c', 'literal pool inside field_spell_sub_1b30'),
        (0x08071b60, None, 'pool_1b60', 'literal pool inside field_spell_sub_1b30'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_b2_lo = _addr(B2_RANGE_START)
        a_b2_hi = _addr(B2_RANGE_END)
        print("[B2.1] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        try:
            clearListing(a_b2_lo, a_b2_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B2: %s" % e)
        print("[B2.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b2_lo, a_b2_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[B2.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd2 = DisassembleCommand(stub_a, None, False)
            if cmd2.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd2.getStatusMsg()))
        # Force DWord on literal pool words
        for pool_addr, pool_val, pool_label, pool_eol in B2_POOL:
            print("[B2.4] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
            pa = _addr(pool_addr)
            try:
                clearListing(pa, _addr(pool_addr + 3))
            except Exception as e:
                print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
            d = listing.createData(pa, DWordDataType.dataType)
            if d is not None:
                print("       DWord created")
            else:
                print("[WARN] createData failed @ 0x%08x" % pool_addr)
            existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
            if pool_label not in existing_p:
                sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
            cu_p = listing.getCodeUnitAt(pa)
            if cu_p is not None:
                cu_p.setComment(CodeUnit.EOL_COMMENT, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[B2.5] createLabel %s @ 0x%08x" % (stub_label, stub_addr))
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("       label created")
            else:
                print("       already present")
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    # ----- B3: fn_eligible_fengsheng_mirror_1f58 -----
    print("\n--- BLOCK B3: fn_eligible_fengsheng_mirror_1f58 @ 0x08071f58 ---")
    B3_CLEAR_START = 0x08071f58  # skip 2-byte pad at 0x08071f56
    B3_CLEAR_END   = 0x08071f87  # end of literal pool (inclusive)
    B3_ENTRY       = 0x08071f58
    B3_LABEL       = 'fn_eligible_fengsheng_mirror_1f58'
    B3_EOL         = 'fn_eligible stub: Fengsheng Mirror (CID=0x1509); FS table THUMB+1 ref @GBA:0x09e40f58'
    B3_POOL = [
        (0x08071f80, None, 'pool_1f80', 'literal pool fn_eligible_fengsheng_mirror_1f58'),
        (0x08071f84, None, 'pool_1f84', 'literal pool fn_eligible_fengsheng_mirror_1f58'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B3_CLEAR_START, B3_CLEAR_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B3_ENTRY)
        print("[dry] createLabel %s" % B3_LABEL)
        for pa, pv, pl, pe in B3_POOL:
            print("[dry] createDWord @ 0x%08x  label=%s" % (pa, pl))
    else:
        a_b3_lo = _addr(B3_CLEAR_START)
        a_b3_hi = _addr(B3_CLEAR_END)
        a_b3_en = _addr(B3_ENTRY)
        print("[B3.1] clearListing 0x%08x..0x%08x" % (B3_CLEAR_START, B3_CLEAR_END))
        try:
            clearListing(a_b3_lo, a_b3_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B3: %s" % e)
        print("[B3.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b3_lo, a_b3_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B3.3] DisassembleCommand @ 0x%08x" % B3_ENTRY)
        cmd3 = DisassembleCommand(a_b3_en, None, False)
        if cmd3.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B3: %s" % cmd3.getStatusMsg())
        print("[B3.4] createLabel %s" % B3_LABEL)
        existing = [s.getName() for s in sym_tbl.getSymbols(a_b3_en)]
        if B3_LABEL not in existing:
            sym_tbl.createLabel(a_b3_en, B3_LABEL, SourceType.USER_DEFINED)
            print("       label created")
        else:
            print("       label already present")
        cu = listing.getCodeUnitAt(a_b3_en)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, B3_EOL)
            print("       EOL set")
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B3_POOL:
            print("[B3.5] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
            pa = _addr(pool_addr)
            try:
                clearListing(pa, _addr(pool_addr + 3))
            except Exception as e:
                print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
            d = listing.createData(pa, DWordDataType.dataType)
            if d is not None:
                print("       DWord created")
            else:
                print("[WARN] createData failed @ 0x%08x" % pool_addr)
            existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
            if pool_label not in existing_p:
                sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
            cu_p = listing.getCodeUnitAt(pa)
            if cu_p is not None:
                cu_p.setComment(CodeUnit.EOL_COMMENT, pool_eol)

    # ----- B4: 11 sub-stubs inside 0x08072004..0x08072103 -----
    print("\n--- BLOCK B4: field_spell_dispatch_sub_stubs @ 0x08072004..0x08072103 ---")
    B4_RANGE_START = 0x08072004
    B4_RANGE_END   = 0x08072103  # inclusive (fn at 0x08072104)

    B4_STUBS = [
        (0x08072004, 'field_spell_sub_2004',
         'raw-dispatch sub-stub 1 (32-entry dispatch table @ 0x71f88..0x72000, entry[0x1f]=0x72000)'),
        (0x08072036, 'field_spell_sub_2036', None),
        (0x0807204a, 'field_spell_sub_204a', None),
        (0x0807204e, 'field_spell_sub_204e', None),
        (0x0807207e, 'field_spell_sub_207e', None),
        (0x08072082, 'field_spell_sub_2082', None),
        (0x08072088, 'field_spell_sub_2088', None),
        (0x080720ac, 'field_spell_sub_20ac', None),
        (0x080720c0, 'field_spell_sub_20c0', None),
        (0x080720d0, 'field_spell_sub_20d0', None),
        (0x080720f4, 'field_spell_sub_20f4',
         'raw-dispatch sub-stub 11 (default stub: 26 of 32 table entries point here)'),
    ]
    # Likely literal pool words in B4 (check/force DWord)
    B4_POOL_CANDIDATES = [
        (0x08072020, 'pool_2020', 'literal pool field_spell_sub_2004'),
        (0x08072024, 'pool_2024', 'literal pool field_spell_sub_2004'),
        (0x08072028, 'pool_2028', 'literal pool field_spell_sub_2004'),
        (0x08072090, 'pool_2090', 'literal pool field_spell_sub_2088'),
        (0x08072094, 'pool_2094', 'literal pool field_spell_sub_2088'),
        (0x080720b4, 'pool_20b4', 'literal pool field_spell_sub_20ac'),
        (0x080720b8, 'pool_20b8', 'literal pool field_spell_sub_20ac'),
        (0x080720e4, 'pool_20e4', 'literal pool field_spell_sub_20d0'),
        (0x080720e8, 'pool_20e8', 'literal pool field_spell_sub_20d0'),
        (0x080720ec, 'pool_20ec', 'literal pool field_spell_sub_20d0'),
        (0x080720f0, 'pool_20f0', 'literal pool field_spell_sub_20d0'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B4_RANGE_START, B4_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_b4_lo = _addr(B4_RANGE_START)
        a_b4_hi = _addr(B4_RANGE_END)
        print("[B4.1] clearListing 0x%08x..0x%08x" % (B4_RANGE_START, B4_RANGE_END))
        try:
            clearListing(a_b4_lo, a_b4_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B4: %s" % e)
        print("[B4.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b4_lo, a_b4_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            print("[B4.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd4 = DisassembleCommand(stub_a, None, False)
            if cmd4.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd4.getStatusMsg()))
        # Force DWord on pool candidates that GAS may not handle as instructions
        for pool_addr, pool_label, pool_eol in B4_POOL_CANDIDATES:
            pa = _addr(pool_addr)
            cu_test = listing.getCodeUnitAt(pa)
            if cu_test is None:
                # Not yet defined as code -- may need to force DWord
                print("[B4.4] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
                try:
                    clearListing(pa, _addr(pool_addr + 3))
                except Exception as e:
                    print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
                d = listing.createData(pa, DWordDataType.dataType)
                if d is not None:
                    print("       DWord created")
                existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
                if pool_label not in existing_p:
                    sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
                cu_p = listing.getCodeUnitAt(pa)
                if cu_p is not None:
                    cu_p.setComment(CodeUnit.EOL_COMMENT, pool_eol)
            else:
                print("[B4.4] pool @ 0x%08x already defined as code, skipping DWord force" % pool_addr)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            print("[B4.5] createLabel %s @ 0x%08x" % (stub_label, stub_addr))
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("       label created")
            else:
                print("       already present")
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    print("\n=== RefineF09Seg4aSlots DONE ===")
    print("  EQ: %d slots" % len(EQ_SLOTS))
    print("  RENAME: neo_daedalus_z14_sub_stubs_1ad4 / field_spell_dispatch_sub_stubs_2004")
    print("  PLATE-1: callee-swap fix @ dispatch_spirit_monster_zone_sprite_by_card_id")
    print("  DISASM B1: fn_eligible_fiber_jar_1a94 @ 0x08071a94")
    print("  DISASM B2: 7 sub-stubs field_spell_sub_1ad4..1bbc")
    print("  DISASM B3: fn_eligible_fengsheng_mirror_1f58 @ 0x08071f58")
    print("  DISASM B4: 11 sub-stubs field_spell_sub_2004..20f4")


main()
