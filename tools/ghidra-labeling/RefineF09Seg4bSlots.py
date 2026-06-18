# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bSlots.py -- F09 Seg-4b (0x08072404..0x08072d20)
#   11 fn: check_equip_target_slot_in_chain_context_bitmap +
#          dispatch_equip_slot_sprite_by_activation_state + dispatch_equip_slot_sprite_unconditional +
#          forward_equip_bitmap_zone11_with_player_shift + dispatch_lp_delta_display_by_card_pair_diff +
#          tick_equip_spell_zone_lp_display_state + dispatch_equip_slot_lp_sprite_by_field_type +
#          tick_equip_zone_type14_oam_placement_state + apply_equip_activation_by_zone_slot_head_check +
#          dispatch_equip_sprite_by_zone_side_match + tick_dragon_summon_display_if_monster_zones_occupied
#
#   EQ=23 (22 REUSE + 1 NEW: LP_DELTA_6000=0x1770)
#   RENAME=3 (DAT_08072444/DAT_08072594/DAT_0807274c -> semantic labels)
#   PLATE=1 (tick_dragon_summon_display_if_monster_zones_occupied @0x08072ce4 -- CJK->ASCII)
#   DISASM=4 blocks (B5: fn_eligible_fiend_comedian; B6: 5sub+fn_eligible_last_turn;
#                    B7: 6sub+fn_eligible_vampire_lord_lady; B8: 6sub-stubs)
#   FUNC_RENAME=0; carve=0; sec5.1=0
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_233248-pre-F09Seg4b

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
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


def force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    """Force a DWord data item at pool_addr, create label and optional EOL."""
    pa = _addr(pool_addr)
    # Clear a wider range (8 bytes) to handle any overlapping code units
    try:
        clearListing(pa, _addr(pool_addr + 7))
    except Exception as e:
        print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
    # Try createData -- catch both Python and Java exceptions
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData DWord returned None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
        # Java checked exception: usually means overlapping code unit still present
        # Try clearing again with a larger range and retry once
        try:
            clearListing(pa, _addr(pool_addr + 11))
            d2 = listing.createData(pa, DWordDataType.dataType)
            if d2 is not None:
                print("[POOL] DWord @ 0x%08x (%s) [retry ok]" % (pool_addr, pool_label))
            else:
                print("[WARN] createData DWord retry returned None @ 0x%08x" % pool_addr)
        except Exception as e2:
            print("[WARN] createData DWord failed even after retry @ 0x%08x: %s" % (pool_addr, e2))
    except Exception as e:
        print("[WARN] createData DWord unexpected error @ 0x%08x: %s" % (pool_addr, e))
    existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing_p:
        try:
            sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("[WARN] createLabel pool %s: %s" % (pool_label, e))
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)


def main():
    print("=== RefineF09Seg4bSlots (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    # =========================================================================
    # A. EQ_SLOTS: 23 equate slots (22 REUSE + 1 NEW: LP_DELTA_6000)
    # Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
    # =========================================================================
    EQ_SLOTS = [

        # ---- check_equip_target_slot_in_chain_context_bitmap (0x08072870..0x0807288f) ----
        (0x0807288c, 0x0201bb90, 'gEquipChainSlotRefs',    'gequip_chain_slot_refs_288c',
         'gEquipChainSlotRefs=0x0201bb90: equip chain slot reference array; [+0x14] chain status'),

        # ---- dispatch_equip_slot_sprite_by_activation_state (0x08072890..0x080728d3) ----
        (0x080728bc, 0x0201b290, 'gDuelPhaseFlags',        'gduel_phase_28bc', None),

        # ---- dispatch_lp_delta_display_by_card_pair_diff (0x0807290c..0x080729db) ----
        (0x08072938, 0x0201c4e0, 'gP1LifePoints',          'gp1lp_2938', None),
        (0x0807293c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',   'p1lp_block2_off_293c', None),
        (0x08072940, 0x0201b290, 'gDuelPhaseFlags',        'gduel_phase_2940', None),
        (0x08072944, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',  'equip_phase_frame_2944', None),
        (0x08072990, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_2990', None),
        (0x080729d8, 0x00001770, 'LP_DELTA_6000',          'lp_delta_6000_29d8',
         'LP_DELTA_6000=0x1770=6000: fixed LP delta when card-pair count v==6; submit_lp_indicator_with_slot_xor_flag arg'),

        # ---- tick_equip_spell_zone_lp_display_state (0x080729dc..0x08072a73) ----
        (0x080729f8, 0x0201b290, 'gDuelPhaseFlags',        'gduel_phase_29f8', None),
        (0x08072a40, 0x0201c4e0, 'gP1LifePoints',          'gp1lp_2a40', None),
        (0x08072a44, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_2a44', None),
        (0x08072a48, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_2a48', None),

        # ---- apply_equip_activation_by_zone_slot_head_check (0x08072b7c..0x08072bfb) ----
        (0x08072b10, 0x0201b290, 'gDuelPhaseFlags',        'gduel_phase_2b10', None),
        (0x08072b14, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_2b14', None),
        (0x08072b18, 0x0201c8f8, 'gP1HandSlotArray',       'gp1hand_2b18', None),

        # ---- dispatch_equip_sprite_by_zone_side_match (0x08072bfc..0x08072ce3) ----
        (0x08072b6c, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_2b6c', None),
        (0x08072b70, 0x0201c8f8, 'gP1HandSlotArray',       'gp1hand_2b70', None),
        (0x08072bdc, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_2bdc', None),
        (0x08072be0, 0x0201c510, 'gDuelFieldSlots',        'gduel_slots_2be0', None),

        # ---- (also within dispatch_equip_sprite_by_zone_side_match or sub fn group) ----
        (0x08072cac, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_2cac', None),
        (0x08072cb0, 0x0201c510, 'gDuelFieldSlots',        'gduel_slots_2cb0', None),
        (0x08072cb4, 0x00001cb8, 'DUEL_ACTIVE_PLAYER_OFF', 'duel_active_player_2cb4', None),

        # ---- tick_dragon_summon_display_if_monster_zones_occupied (0x08072ce4..0x08072d1f) ----
        (0x08072d0c, 0x0201b290, 'gDuelPhaseFlags',        'gduel_phase_2d0c', None),
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
    # B. RENAME_SLOTS: 3 block-start labels (DAT_ -> semantic name + EOL)
    # =========================================================================
    RENAME_SLOTS = [
        (0x08072444, 'last_turn_dispatch_sub_stubs_2444',
         'raw-dispatch sub-stubs: 5 entry-pts + fn_eligible B6'),
        (0x08072594, 'vampire_dispatch_sub_stubs_2594',
         'raw-dispatch sub-stubs: 6 entry-pts + fn_eligible B7'),
        (0x0807274c, 'equip_zone_sub_stubs_274c',
         'raw-dispatch sub-stubs: 6 entry-pts B8'),
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
    # C. PLATE-1: Replace CJK mojibake plate at tick_dragon_summon_display_if_monster_zones_occupied
    #    Function at 0x08072ce4
    #    Replace the full plate with pure ASCII text.
    #    treat setPlateComment WARN/not-found as FAIL (red line).
    # =========================================================================
    PLATE1_ADDR = 0x08072ce4
    PLATE1_ASCII = (
        "Equip chain dragon-summon display gate driver.\n"
        "Takes card_entry_ptr(r0), scene_ptr(r1).\n"
        "Reads [gDuelPhaseFlags+0x4a0] step code.\n"
        "If step==0x80: extracts player_id from [r0+2] bit0;\n"
        "  calls count_occupied_monster_zones(player_id).\n"
        "  If result==0 (no occupied monster zones) returns 0 immediately.\n"
        "If step!=0x80 or monster zones are occupied:\n"
        "  calls tick_dragon_summon_effect_display_state_machine(r4,r5).\n"
        "Returns result of tick_dragon_summon_effect_display_state_machine.\n"
        "indeg=0; driven by fn-ptr dispatch table."
    )

    if DRY:
        print("[dry] PLATE-1: would replace plate at 0x%08x with ASCII text" % PLATE1_ADDR)
        print("  ASCII text (first 80 chars): %s" % PLATE1_ASCII[:80])
    else:
        fn_addr_p1 = _addr(PLATE1_ADDR)
        fn_obj_p1 = currentProgram.getListing().getFunctionAt(fn_addr_p1)
        if fn_obj_p1 is None:
            print("[FAIL] PLATE-1: no function found at 0x%08x -- ABORT plate set" % PLATE1_ADDR)
        else:
            cu_p1 = listing.getCodeUnitAt(fn_addr_p1)
            if cu_p1 is None:
                print("[FAIL] PLATE-1: no CodeUnit at 0x%08x -- ABORT plate set" % PLATE1_ADDR)
            else:
                cu_p1.setComment(CodeUnit.PLATE_COMMENT, PLATE1_ASCII)
                # Verify it actually landed
                verify_plate = cu_p1.getComment(CodeUnit.PLATE_COMMENT)
                if verify_plate is None or verify_plate != PLATE1_ASCII:
                    print("[FAIL] PLATE-1: plate verification failed at 0x%08x -- ABORT" % PLATE1_ADDR)
                    print("  Expected length: %d  Actual: %s" % (
                        len(PLATE1_ASCII),
                        len(verify_plate) if verify_plate else "None"))
                else:
                    # Check for non-ASCII bytes in the set plate
                    non_ascii = [c for c in verify_plate if ord(c) > 0x7f]
                    if non_ascii:
                        print("[FAIL] PLATE-1: non-ASCII chars detected after set: %s -- ABORT" % repr(non_ascii[:5]))
                    else:
                        print("[PLATE-1] ASCII plate set successfully at 0x%08x" % PLATE1_ADDR)

    # =========================================================================
    # D. DISASM: 4 blocks
    #   B5: fn_eligible_fiend_comedian @ 0x08072404 (block 0x72404/0x2c)
    #   B6: 5 sub-stubs + fn_eligible_last_turn @ 0x08072444 (block 0x72444/0x138)
    #   B7: 6 sub-stubs + fn_eligible_vampire_lord_lady @ 0x08072594 (block 0x72594/0x1a0)
    #   B8: 6 sub-stubs @ 0x0807274c (block 0x7274c/0x124)
    # =========================================================================

    # ----- B5: fn_eligible_fiend_comedian @ 0x08072404 -----
    print("\n--- BLOCK B5: fn_eligible_fiend_comedian @ 0x08072404 ---")
    # block: 0x72404..0x72430 (0x2c bytes)
    # literal pool: [0x72428]=gDuelPhaseFlags(0x0201b290), [0x7242c]=0x08072430
    B5_CLEAR_START = 0x08072404
    B5_CLEAR_END   = 0x0807242f  # inclusive end
    B5_ENTRY       = 0x08072404
    B5_LABEL       = 'fn_eligible_fiend_comedian_2404'
    B5_EOL         = 'fn_eligible: Fiend Comedian (CID=0x151d=FIEND_COMEDIAN_CID); FS THUMB+1 @GBA:0x09e41078'
    B5_POOL = [
        (0x08072428, 0x0201b290, 'gduel_phase_pool_2428',
         'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_fiend_comedian_2404'),
        (0x0807242c, 0x08072430, 'pool_next_addr_242c',
         '0x08072430=next address; literal pool fn_eligible_fiend_comedian_2404'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B5_CLEAR_START, B5_CLEAR_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B5_ENTRY)
        print("[dry] createLabel %s" % B5_LABEL)
        for pa, pv, pl, pe in B5_POOL:
            print("[dry] createDWord @ 0x%08x  label=%s" % (pa, pl))
    else:
        a_b5_lo = _addr(B5_CLEAR_START)
        a_b5_hi = _addr(B5_CLEAR_END)
        a_b5_en = _addr(B5_ENTRY)
        print("[B5.1] clearListing 0x%08x..0x%08x" % (B5_CLEAR_START, B5_CLEAR_END))
        try:
            clearListing(a_b5_lo, a_b5_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B5: %s" % e)
        print("[B5.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b5_lo, a_b5_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B5.3] DisassembleCommand @ 0x%08x" % B5_ENTRY)
        cmd_b5 = DisassembleCommand(a_b5_en, None, False)
        if cmd_b5.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B5: %s" % cmd_b5.getStatusMsg())
        print("[B5.4] createLabel %s" % B5_LABEL)
        existing = [s.getName() for s in sym_tbl.getSymbols(a_b5_en)]
        if B5_LABEL not in existing:
            sym_tbl.createLabel(a_b5_en, B5_LABEL, SourceType.USER_DEFINED)
            print("       label created")
        else:
            print("       label already present")
        cu_b5 = listing.getCodeUnitAt(a_b5_en)
        if cu_b5 is not None:
            cu_b5.setComment(CodeUnit.EOL_COMMENT, B5_EOL)
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B5_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)

    # ----- B6: 5 sub-stubs + fn_eligible_last_turn @ 0x08072444..0x0807257b -----
    print("\n--- BLOCK B6: last_turn_dispatch_sub_stubs_2444 @ 0x08072444..0x0807257b ---")
    # pre-block dispatch table at 0x72430..0x72443 (5 entries):
    #   0x72430: 0x08072534, 0x72434: 0x080724b4, 0x72438: 0x080724ac
    #   0x7243c: 0x0807248a, 0x72440: 0x08072444
    # fn_eligible at 0x08072540 (+0xfc)
    # literal pool of fn_eligible: [0x72574]=gDuelPhaseFlags, [0x72578]=0x0807257c
    B6_RANGE_START = 0x08072444
    B6_RANGE_END   = 0x0807257b  # inclusive

    B6_STUBS = [
        (0x08072444, 'last_turn_sub_2444',
         'raw-dispatch sub-stub (table[0x72440]=0x08072444); 5-entry table @0x72430..0x72443'),
        (0x0807248a, 'last_turn_sub_248a', None),
        (0x080724ac, 'last_turn_sub_24ac', None),
        (0x080724b4, 'last_turn_sub_24b4', None),
        (0x08072534, 'last_turn_sub_2534', None),
        (0x08072540, 'fn_eligible_last_turn_2540',
         'fn_eligible: Last Turn (CID=0x151e=LAST_TURN_CID); FS THUMB+1 @GBA:0x09e41090'),
    ]
    # Literal pool words in B6 (identified from raw scan):
    # 0x72478=gDuelCardCtxBase, 0x7247c=gP1LifePoints, 0x724a8=gP1LifePoints
    # 0x72500=gP1LifePoints, 0x72508=PLAYER_BLOCK_STRIDE, 0x72530=PLAYER_BLOCK_STRIDE
    # 0x72574=gDuelPhaseFlags, 0x72578=0x0807257c
    B6_POOL = [
        (0x08072478, 'pool_b6_2478', 'gDuelCardCtxBase=0x0201e2a0; literal pool B6'),
        (0x0807247c, 'pool_b6_247c', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
        (0x080724a8, 'pool_b6_24a8', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
        (0x08072500, 'pool_b6_2500', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
        (0x08072508, 'pool_b6_2508', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B6'),
        (0x08072530, 'pool_b6_2530', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B6'),
        (0x08072574, 'pool_b6_2574', 'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_last_turn'),
        (0x08072578, 'pool_b6_2578', '0x0807257c; literal pool fn_eligible_last_turn'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B6_RANGE_START, B6_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B6_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_b6_lo = _addr(B6_RANGE_START)
        a_b6_hi = _addr(B6_RANGE_END)
        print("[B6.1] clearListing 0x%08x..0x%08x" % (B6_RANGE_START, B6_RANGE_END))
        try:
            clearListing(a_b6_lo, a_b6_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B6: %s" % e)
        print("[B6.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b6_lo, a_b6_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B6_STUBS:
            print("[B6.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd_b6 = DisassembleCommand(stub_a, None, False)
            if cmd_b6.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd_b6.getStatusMsg()))
        # Force DWord on pool words (always force, even if already defined as code)
        for pool_addr, pool_label, pool_eol in B6_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B6_STUBS:
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("[B6.5] label %s @ 0x%08x created" % (stub_label, stub_addr))
            else:
                print("[B6.5] label %s already present" % stub_label)
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    # ----- B7: 6 sub-stubs + fn_eligible_vampire_lord_lady @ 0x08072594..0x08072733 -----
    print("\n--- BLOCK B7: vampire_dispatch_sub_stubs_2594 @ 0x08072594..0x08072733 ---")
    # pre-block dispatch table at 0x7257c..0x72593 (6 entries):
    #   0x7257c: 0x080726bc, 0x72580: 0x08072678, 0x72584: 0x0807264c
    #   0x72588: 0x08072624, 0x7258c: 0x080725e8, 0x72590: 0x08072594
    # fn_eligible at 0x080726f4 (+0x160) -- handles VAMPIRE_LORD_CID(0x1522) and VAMPIRE_LADY_CID(0x1746)
    # literal pool of fn_eligible: [0x7272c]=gDuelPhaseFlags, [0x72730]=0x08072734
    B7_RANGE_START = 0x08072594
    B7_RANGE_END   = 0x08072733  # inclusive

    B7_STUBS = [
        (0x08072594, 'vampire_sub_2594',
         'raw-dispatch sub-stub (table[0x72590]=0x08072594); 6-entry table @0x7257c..0x72593'),
        (0x080725e8, 'vampire_sub_25e8', None),
        (0x08072624, 'vampire_sub_2624', None),
        (0x0807264c, 'vampire_sub_264c', None),
        (0x08072678, 'vampire_sub_2678', None),
        (0x080726bc, 'vampire_sub_26bc', None),
        (0x080726f4, 'fn_eligible_vampire_lord_lady_26f4',
         'fn_eligible: VAMPIRE_LORD_CID(0x1522,x2)+VAMPIRE_LADY_CID(0x1746); FS THUMB+1 x3 @GBA:0x09e43e08/0x09e44930/0x09e45b60'),
    ]
    # Literal pool words in B7 (identified from raw scan):
    # 0x725d8=gP1LifePoints, 0x725e0=EQUIP_PHASE_FRAME_OFF, 0x725e4=0x08090625 (ROM addr)
    # 0x7260c=gDuelPhaseFlags, 0x72610=EQUIP_PHASE_FRAME_OFF, 0x72614=gP1LifePoints
    # 0x72648=EQUIP_PHASE_FRAME_OFF, 0x72674=EQUIP_PHASE_FRAME_OFF
    # 0x726b0=gP1LifePoints, 0x726b8=PLAYER_BLOCK_STRIDE
    # 0x7272c=gDuelPhaseFlags, 0x72730=0x08072734
    B7_POOL = [
        (0x080725d8, 'pool_b7_25d8', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
        (0x080725e0, 'pool_b7_25e0', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
        (0x080725e4, 'pool_b7_25e4', '0x08090625 ROM addr; literal pool B7'),
        (0x0807260c, 'pool_b7_260c', 'gDuelPhaseFlags=0x0201b290; literal pool B7'),
        (0x08072610, 'pool_b7_2610', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
        (0x08072614, 'pool_b7_2614', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
        (0x08072648, 'pool_b7_2648', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
        (0x08072674, 'pool_b7_2674', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
        (0x080726b0, 'pool_b7_26b0', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
        (0x080726b8, 'pool_b7_26b8', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B7'),
        (0x0807272c, 'pool_b7_272c', 'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_vampire_lord_lady'),
        (0x08072730, 'pool_b7_2730', '0x08072734; literal pool fn_eligible_vampire_lord_lady'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B7_RANGE_START, B7_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B7_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_b7_lo = _addr(B7_RANGE_START)
        a_b7_hi = _addr(B7_RANGE_END)
        print("[B7.1] clearListing 0x%08x..0x%08x" % (B7_RANGE_START, B7_RANGE_END))
        try:
            clearListing(a_b7_lo, a_b7_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B7: %s" % e)
        print("[B7.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b7_lo, a_b7_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B7_STUBS:
            print("[B7.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd_b7 = DisassembleCommand(stub_a, None, False)
            if cmd_b7.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd_b7.getStatusMsg()))
        # Force DWord on pool words (always force, even if already defined as code)
        for pool_addr, pool_label, pool_eol in B7_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B7_STUBS:
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("[B7.5] label %s @ 0x%08x created" % (stub_label, stub_addr))
            else:
                print("[B7.5] label %s already present" % stub_label)
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    # ----- B8: 6 sub-stubs @ 0x0807274c..0x0807286f -----
    print("\n--- BLOCK B8: equip_zone_sub_stubs_274c @ 0x0807274c..0x0807286f ---")
    # pre-block dispatch table at 0x72734..0x7274b (6 entries):
    #   0x72734: 0x08072856, 0x72738: 0x08072848, 0x7273c: 0x08072804
    #   0x72740: 0x080727e4, 0x72744: 0x080727b8, 0x72748: 0x0807274c
    # No fn_eligible THUMB+1 refs.
    B8_RANGE_START = 0x0807274c
    B8_RANGE_END   = 0x0807286f  # inclusive

    B8_STUBS = [
        (0x0807274c, 'equip_zone_sub_274c',
         'raw-dispatch sub-stub (table[0x72748]=0x0807274c); 6-entry table @0x72734..0x7274b'),
        (0x080727b8, 'equip_zone_sub_27b8', None),
        (0x080727e4, 'equip_zone_sub_27e4', None),
        (0x08072804, 'equip_zone_sub_2804', None),
        (0x08072848, 'equip_zone_sub_2848', None),
        (0x08072856, 'equip_zone_sub_2856', None),
    ]
    # Literal pool words in B8 (from raw scan):
    # 0x72788=gP1LifePoints, 0x7278c=PLAYER_BLOCK_STRIDE, 0x72790=gDuelCardCtxBase
    # 0x727b4=lookup_equip_score_b_0x1b9(?), 0x727dc=EQUIP_PHASE_FRAME_OFF, 0x727e0=gP1LifePoints
    # 0x72800=EQUIP_PHASE_FRAME_OFF, 0x7282c=gP1LifePoints
    B8_POOL = [
        (0x08072788, 'pool_b8_2788', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
        (0x0807278c, 'pool_b8_278c', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B8'),
        (0x08072790, 'pool_b8_2790', 'gDuelCardCtxBase=0x0201e2a0; literal pool B8'),
        (0x080727b4, 'pool_b8_27b4', '0x1b9; literal pool B8'),
        (0x080727dc, 'pool_b8_27dc', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B8'),
        (0x080727e0, 'pool_b8_27e0', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
        (0x08072800, 'pool_b8_2800', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B8'),
        (0x0807282c, 'pool_b8_282c', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B8_RANGE_START, B8_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B8_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_b8_lo = _addr(B8_RANGE_START)
        a_b8_hi = _addr(B8_RANGE_END)
        print("[B8.1] clearListing 0x%08x..0x%08x" % (B8_RANGE_START, B8_RANGE_END))
        try:
            clearListing(a_b8_lo, a_b8_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B8: %s" % e)
        print("[B8.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b8_lo, a_b8_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B8_STUBS:
            print("[B8.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd_b8 = DisassembleCommand(stub_a, None, False)
            if cmd_b8.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd_b8.getStatusMsg()))
        # Force DWord on pool words (always force, even if already defined as code)
        for pool_addr, pool_label, pool_eol in B8_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B8_STUBS:
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("[B8.5] label %s @ 0x%08x created" % (stub_label, stub_addr))
            else:
                print("[B8.5] label %s already present" % stub_label)
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    print("\n=== RefineF09Seg4bSlots DONE ===")
    print("  EQ: %d slots (22 REUSE + 1 NEW: LP_DELTA_6000)" % len(EQ_SLOTS))
    print("  RENAME: last_turn_dispatch_sub_stubs_2444 / vampire_dispatch_sub_stubs_2594 / equip_zone_sub_stubs_274c")
    print("  PLATE-1: CJK->ASCII at tick_dragon_summon_display_if_monster_zones_occupied @0x08072ce4")
    print("  DISASM B5: fn_eligible_fiend_comedian_2404 @ 0x08072404")
    print("  DISASM B6: 5 sub-stubs + fn_eligible_last_turn_2540 @ 0x08072444..0x0807257b")
    print("  DISASM B7: 6 sub-stubs + fn_eligible_vampire_lord_lady_26f4 @ 0x08072594..0x08072733")
    print("  DISASM B8: 6 sub-stubs equip_zone_sub @ 0x0807274c..0x0807286f")


main()
