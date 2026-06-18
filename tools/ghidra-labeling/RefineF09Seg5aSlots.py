# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aSlots.py -- F09 Seg-5a (0x08072d20..0x08073a5c)
#   12 fn: enqueue_zone_sprite_attr_type11_from_slot / tick_equip_lp_display_state_by_slot /
#          setup_equip_oam_by_placeable_card_id_and_zone / tick_equip_lp_display_bitmap_state_by_slot /
#          tick_equip_lp_display_type18_state_by_slot / enqueue_equip_zone_sprite_by_slot_lp_state /
#          enqueue_slot_sprite_if_chain_flags_and_node_active / tick_equip_deck_pair_hand_sprite_state /
#          apply_lp_delta_for_slot_by_series_code / tick_neo_daedalus_equip_display_seq /
#          enqueue_slot_sprite_mode3_with_effect_node / dispatch_equip_slot_activation_or_sprite_by_type
#          + enqueue_hand_spell_sprite_by_set_code_match (0x0807381c..0x08073863)
#
#   EQ=48 (38 REUSE + 10 NEW)
#   REF=10 (all gP1LifePoints=0x0201c4e0)
#   RENAME=3 (DAT_080731e4 / DAT_08073628 / DAT_08073900)
#   FUNC_RENAME=0; PLATE=0; carve=0; sec5.1=0
#   DISASM=6 blocks (B1-B6)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260619_010102-pre-F09Seg5a

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType, FlowType
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


def apply_ref(slot_addr, target_addr, gas_label, slot_label):
    """USER-label on target + DATA memory-reference from slot + USER-label on slot."""
    if not _check(slot_addr, target_addr):
        return
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    src_addr = _addr(slot_addr)
    dst_addr = _addr(target_addr)

    # Create label on target
    existing_dst = [s.getName() for s in sym_tbl.getSymbols(dst_addr)]
    if gas_label not in existing_dst:
        try:
            sym_tbl.createLabel(dst_addr, gas_label, SourceType.USER_DEFINED)
            print("[REF-TGT] %s @ 0x%08x" % (gas_label, target_addr))
        except Exception as e:
            print("[WARN] createLabel target %s: %s" % (gas_label, e))

    # Add DATA memory reference from slot to target
    try:
        ref = ref_mgr.addMemoryReference(src_addr, dst_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        ref_mgr.setPrimary(ref, True)
        print("[REF-LINK] 0x%08x -> 0x%08x (%s)" % (slot_addr, target_addr, gas_label))
    except Exception as e:
        print("[WARN] addMemoryReference @ 0x%08x: %s" % (slot_addr, e))

    # Create slot label
    existing_src = [s.getName() for s in sym_tbl.getSymbols(src_addr)]
    if slot_label not in existing_src:
        try:
            sym_tbl.createLabel(src_addr, slot_label, SourceType.USER_DEFINED)
            print("[REF-SLOT] %s @ 0x%08x" % (slot_label, slot_addr))
        except Exception as e:
            print("[WARN] createLabel slot %s: %s" % (slot_label, e))


def force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    """Force a DWord data item at pool_addr, create label and optional EOL."""
    pa = _addr(pool_addr)
    try:
        clearListing(pa, _addr(pool_addr + 7))
    except Exception as e:
        print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData DWord returned None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
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
    print("=== RefineF09Seg5aSlots (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    # =========================================================================
    # A. EQ_SLOTS: 48 equate slots (38 REUSE + 10 NEW)
    # NEW: EQUIP_CHAIN_BASE_OFF, STATUE_OF_THE_WICKED_CID, SPRITE_ATTR_CLR_BIT13,
    #      TOKEN_13FB_CID, TOKEN_14FA_CID, TOKEN_154E_CID, TOKEN_15BD_CID,
    #      TOKEN_15BE_CID, TOKEN_1603_CID, TOKEN_1639_CID, TOKEN_195A_CID, TRAP_DUSTSHOOT_CID
    # (12 new constants, EQUIP_CHAIN_BASE_OFF counted once then REUSE at second slot)
    # =========================================================================
    EQ_SLOTS = [

        # ---- enqueue_zone_sprite_attr_type11_from_slot (0x08072d20..0x08072d33) ----
        (0x08072d58, 0x0201b290, 'gDuelPhaseFlags',          'gduel_phase_2d58', None),

        # ---- tick_equip_lp_display_state_by_slot (0x08072d34..0x08072eb3) ----
        (0x08072d90, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_2d90', None),
        (0x08072db8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',    'equip_phase_frame_2db8', None),
        (0x08072dc0, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_2dc0', None),
        (0x08072df4, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_2df4', None),

        # ---- setup_equip_oam_by_placeable_card_id_and_zone (0x08072eb4..0x08072fd3) ----
        (0x08072e5c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',    'equip_phase_frame_2e5c', None),
        (0x08072e60, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_2e60', None),
        (0x08072e64, 0x0201c600, 'gP1FieldArrayCBase',       'gp1field_arrc_2e64', None),
        # NEW: EQUIP_CHAIN_BASE_OFF = 0x1c88 (first occurrence)
        (0x08072e68, 0x00001c88, 'EQUIP_CHAIN_BASE_OFF',     'equip_chain_base_off_2e68',
         'EQUIP_CHAIN_BASE_OFF=0x1c88; gP1FieldArrayCBase(0x0201c600)+0x1c88=gEquipChainEntryBase(0x0201e288)'),
        (0x08072eb0, 0x0201bb90, 'gEquipChainSlotRefs',      'gequip_chain_refs_2eb0', None),
        (0x08072ee4, 0x000013ff, 'JAM_BREEDING_MACHINE_CID', 'jam_breed_cid_2ee4', None),
        (0x08072f1c, 0x00001595, 'COBRA_JAR_CID',            'cobra_jar_cid_2f1c', None),
        (0x08072f20, 0x000013ff, 'JAM_BREEDING_MACHINE_CID', 'jam_breed_cid_2f20', None),
        # NEW: STATUE_OF_THE_WICKED_CID = 0x1543
        (0x08072f2c, 0x00001543, 'STATUE_OF_THE_WICKED_CID', 'statue_wicked_cid_2f2c',
         'STATUE_OF_THE_WICKED_CID=0x1543; setup_equip_oam BST input CID check'),
        (0x08072f44, 0x000015d5, 'DES_DENDLE_CID',           'des_dendle_cid_2f44', None),
        (0x08072f58, 0x000019a5, 'RAVIEL_LORD_CID',          'raviel_lord_cid_2f58', None),
        # NEW token CIDs
        (0x08072f60, 0x000013fb, 'TOKEN_13FB_CID',           'token_13fb_cid_2f60',
         'TOKEN_13FB_CID=0x13fb; unnamed token result (card-stats.s L27068)'),
        (0x08072f68, 0x000014fa, 'TOKEN_14FA_CID',           'token_14fa_cid_2f68',
         'TOKEN_14FA_CID=0x14fa; unnamed token result (card-stats.s L27120)'),
        (0x08072f70, 0x0000154e, 'TOKEN_154E_CID',           'token_154e_cid_2f70',
         'TOKEN_154E_CID=0x154e; unnamed token result (card-stats.s L27133)'),
        (0x08072f78, 0x000015bd, 'TOKEN_15BD_CID',           'token_15bd_cid_2f78',
         'TOKEN_15BD_CID=0x15bd; unnamed token result (card-stats.s L27146)'),
        (0x08072f84, 0x000015be, 'TOKEN_15BE_CID',           'token_15be_cid_2f84',
         'TOKEN_15BE_CID=0x15be; unnamed token result (card-stats.s L27159)'),
        (0x08072f8c, 0x00001603, 'TOKEN_1603_CID',           'token_1603_cid_2f8c',
         'TOKEN_1603_CID=0x1603; unnamed token result (card-stats.s L27172)'),
        (0x08072f94, 0x00001639, 'TOKEN_1639_CID',           'token_1639_cid_2f94',
         'TOKEN_1639_CID=0x1639; unnamed token result (card-stats.s L27185)'),
        (0x08072fcc, 0x0000195a, 'TOKEN_195A_CID',           'token_195a_cid_2fcc',
         'TOKEN_195A_CID=0x195a; unnamed token result (card-stats.s L27250)'),
        # NEW: SPRITE_ATTR_CLR_BIT13 = 0xffffdfff
        (0x08072fd0, 0xffffdfff, 'SPRITE_ATTR_CLR_BIT13',    'sprite_attr_clr_bit13_2fd0',
         'SPRITE_ATTR_CLR_BIT13=0xffffdfff; AND mask clears bit13 (player_id bit); ands r1,mask then orrs r1,player<<0xd'),

        # ---- tick_equip_lp_display_bitmap_state_by_slot (0x08072fd4..0x080730df) ----
        (0x08072ff4, 0x0201b290, 'gDuelPhaseFlags',          'gduel_phase_2ff4', None),
        (0x08073040, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_3040', None),
        (0x08073074, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_3074', None),
        (0x08073090, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_3090', None),
        (0x080730dc, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_30dc', None),

        # ---- tick_equip_lp_display_type18_state_by_slot (0x080730e0..0x080732a7) ----
        (0x08073108, 0x0201b290, 'gDuelPhaseFlags',          'gduel_phase_3108', None),
        (0x08073120, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'lp_card_track_off_3120', None),

        # ---- enqueue_slot_sprite_if_chain_flags_and_node_active (0x080732fc..0x0807338b) ----
        (0x080732f8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',     'p1lp_block2_off_32f8', None),

        # ---- tick_equip_deck_pair_hand_sprite_state (0x0807338c..0x08073427) ----
        (0x08073380, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_act_link_flag_3380', None),
        (0x08073384, 0x0201bb90, 'gEquipChainSlotRefs',      'gequip_chain_refs_3384', None),
        (0x08073388, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_3388', None),
        (0x080733ac, 0x0201b290, 'gDuelPhaseFlags',          'gduel_phase_33ac', None),

        # ---- apply_lp_delta_for_slot_by_series_code (0x08073428..0x08073453) ----
        (0x080733fc, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_33fc', None),
        (0x08073400, 0x0201c740, 'gP1SlotSetCodeArray',      'gp1slot_setcode_3400', None),

        # ---- tick_neo_daedalus_equip_display_seq (0x08073454..0x0807375f) ----
        (0x08073474, 0x0201b290, 'gDuelPhaseFlags',          'gduel_phase_3474', None),
        (0x080734d8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',    'equip_phase_frame_34d8', None),
        (0x080734dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_34dc', None),
        (0x080734e0, 0x0201c510, 'gDuelFieldSlots',          'gduel_slots_34e0', None),
        (0x08073528, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',    'equip_phase_frame_3528', None),
        (0x0807355c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',    'equip_phase_frame_355c', None),
        (0x08073560, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'player_stride_3560', None),
        (0x08073564, 0x0201c600, 'gP1FieldArrayCBase',       'gp1field_arrc_3564', None),
        # REUSE: EQUIP_CHAIN_BASE_OFF (second occurrence)
        (0x08073568, 0x00001c88, 'EQUIP_CHAIN_BASE_OFF',     'equip_chain_base_off_3568',
         'EQUIP_CHAIN_BASE_OFF=0x1c88 (reuse); gP1FieldArrayCBase+0x1c88=gEquipChainEntryBase'),
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
    # B. REF_SLOTS: 10 slots all pointing to gP1LifePoints (0x0201c4e0)
    # =========================================================================
    # gP1LifePoints target address
    GP1LP = 0x0201c4e0

    REF_SLOTS = [
        # DWORD_ slots (no existing label)
        (0x08072d8c,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_2d8c'),
        (0x08072dbc,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_2dbc'),
        (0x08072df0,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_2df0'),
        (0x080732f4,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_32f4'),
        (0x0807337c,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_337c'),
        # PTR_gP1LifePoints_ slots (already labeled, add USER label + DATA ref)
        (0x0807303c,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_303c'),
        (0x08073070,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_3070'),
        (0x0807308c,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_308c'),
        (0x080730d8,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_30d8'),
        (0x0807311c,  GP1LP, 'gP1LifePoints', 'gp1lp_ref_311c'),
    ]

    if DRY:
        print("[dry] Would apply %d REF_SLOTS -> gP1LifePoints @ 0x%08x" % (len(REF_SLOTS), GP1LP))
        for s in REF_SLOTS:
            print("  0x%08x -> 0x%08x" % (s[0], s[1]))
    else:
        for slot_addr, tgt, gas_lbl, slot_lbl in REF_SLOTS:
            apply_ref(slot_addr, tgt, gas_lbl, slot_lbl)
        print("[REF] done: %d slots all -> gP1LifePoints" % len(REF_SLOTS))

    # =========================================================================
    # C. RENAME_SLOTS: 3 block-start auto-names -> semantic labels
    # =========================================================================
    RENAME_SLOTS = [
        (0x080731e4, 'trap_dustshoot_dispatch_sub_stubs_31e4',
         'Trap Dustshoot CID=0x1546 dispatch sub-stubs; raw-ref from dispatch table @0x08073168'),
        (0x08073628, 'machine_dup_dispatch_sub_stubs_3628',
         'Machine Dup/League CID=0x157a/0x1978 dispatch sub-stubs; raw-ref from dispatch table @0x080735b4'),
        (0x08073900, 'cat_ill_omen_dispatch_sub_stubs_3900',
         'A Cat of Ill Omen/An Owl of Luck CID=0x1590/0x1593 dispatch sub-stubs; raw-ref from dispatch table @0x0807388c'),
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
    # D. DISASM: 6 blocks (B1-B6)
    # =========================================================================

    # ----- B1: fn_eligible_trap_dustshoot @ 0x08073140 -----
    # Block: 0x0807313e/0x2a (padding .zero 2 at 0x0807313e, fn at 0x08073140..0x08073167)
    # Literal pool: [0x08073160]=gDuelPhaseFlags(0x0201b290), [0x08073164]=0x08073168(ptr to B2 table)
    # Dispatch table: 0x08073168..0x080731e3 (31 words)
    print("\n--- BLOCK B1: fn_eligible_trap_dustshoot @ 0x08073140 ---")
    B1_CLEAR_START = 0x08073140
    B1_CLEAR_END   = 0x08073167  # inclusive (end of fn stub)
    B1_ENTRY       = 0x08073140
    B1_LABEL       = 'fn_eligible_trap_dustshoot_3140'
    B1_EOL         = 'fn_eligible: Trap Dustshoot (CID=0x1546=TRAP_DUSTSHOOT_CID); FS THUMB+1 @GBA:0x09e411b0'
    B1_POOL = [
        (0x08073160, 0x0201b290, 'pool_b1_3160',
         'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_trap_dustshoot'),
        (0x08073164, 0x08073168, 'pool_b1_3164',
         '0x08073168=trap_dustshoot_dispatch_table_3168; literal pool fn_eligible_trap_dustshoot'),
    ]
    # Dispatch table label
    B1_TABLE_LABEL = 'trap_dustshoot_dispatch_table_3168'
    B1_TABLE_EOL   = 'dispatch table: 31 entries (card_zone_type -> B2 sub-stub); index [0..30]'

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B1_CLEAR_START, B1_CLEAR_END))
        print("[dry] setTMode THUMB=1 @ B1 range")
        print("[dry] DisassembleCommand @ 0x%08x" % B1_ENTRY)
        print("[dry] createLabel %s" % B1_LABEL)
        print("[dry] label dispatch table %s" % B1_TABLE_LABEL)
    else:
        a_lo = _addr(B1_CLEAR_START)
        a_hi = _addr(B1_CLEAR_END)
        a_en = _addr(B1_ENTRY)
        print("[B1.1] clearListing 0x%08x..0x%08x" % (B1_CLEAR_START, B1_CLEAR_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B1: %s" % e)
        print("[B1.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B1.3] DisassembleCommand @ 0x%08x" % B1_ENTRY)
        cmd = DisassembleCommand(a_en, None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B1: %s" % cmd.getStatusMsg())
        # Label fn entry
        existing = [s.getName() for s in sym_tbl.getSymbols(a_en)]
        if B1_LABEL not in existing:
            sym_tbl.createLabel(a_en, B1_LABEL, SourceType.USER_DEFINED)
            print("[B1.4] label %s created" % B1_LABEL)
        cu_b1 = listing.getCodeUnitAt(a_en)
        if cu_b1 is not None:
            cu_b1.setComment(CodeUnit.EOL_COMMENT, B1_EOL)
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B1_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # Label dispatch table
        dt_addr = _addr(0x08073168)
        existing_dt = [s.getName() for s in sym_tbl.getSymbols(dt_addr)]
        if B1_TABLE_LABEL not in existing_dt:
            sym_tbl.createLabel(dt_addr, B1_TABLE_LABEL, SourceType.USER_DEFINED)
            print("[B1.5] dispatch table label created: %s" % B1_TABLE_LABEL)
        cu_dt = listing.getCodeUnitAt(dt_addr)
        if cu_dt is not None:
            cu_dt.setComment(CodeUnit.EOL_COMMENT, B1_TABLE_EOL)

    # ----- B2: trap_dustshoot dispatch sub-stubs @ 0x080731e4..0x080732a7 -----
    # Pre-block dispatch table at 0x08073168..0x080731e3 (31 entries)
    # Sub-stub entry points from dispatch table:
    #   0x080731e4, 0x0807322a, 0x0807326c, 0x08073280, 0x08073290, 0x080732a0
    # Default stub: 0x080732a0 (movs r0,#0; return 0)
    # Pool words in block: [0x08073210]=gP1LifePoints(0x0201c4e0), [0x08073214]=PLAYER_BLOCK_STRIDE(0x868)
    #                      [0x08073264]=gP1LifePoints(0x0201c4e0), [0x08073268]=LP_CARD_TRACK_BASE_OFF(0x1da8)
    print("\n--- BLOCK B2: trap_dustshoot_dispatch_sub_stubs_31e4 @ 0x080731e4..0x080732a7 ---")
    B2_RANGE_START = 0x080731e4
    B2_RANGE_END   = 0x080732a7  # inclusive

    B2_STUBS = [
        (0x080731e4, 'trap_dustshoot_sub_31e4',
         'raw-dispatch sub-stub (table[0x080731e0]=0x080731e4); see trap_dustshoot_dispatch_table_3168'),
        (0x0807322a, 'trap_dustshoot_sub_322a', None),
        (0x0807326c, 'trap_dustshoot_sub_326c', None),
        (0x08073280, 'trap_dustshoot_sub_3280', None),
        (0x08073290, 'trap_dustshoot_sub_3290', None),
        (0x080732a0, 'trap_dustshoot_default_32a0',
         'default sub-stub: movs r0,#0; return 0 (22 dispatch table entries point here)'),
    ]
    B2_POOL = [
        (0x08073210, 0x0201c4e0, 'pool_b2_3210', 'gP1LifePoints=0x0201c4e0; literal pool B2'),
        (0x08073214, 0x00000868, 'pool_b2_3214', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B2'),
        (0x08073264, 0x0201c4e0, 'pool_b2_3264', 'gP1LifePoints=0x0201c4e0; literal pool B2'),
        (0x08073268, 0x00001da8, 'pool_b2_3268', 'LP_CARD_TRACK_BASE_OFF=0x1da8; literal pool B2'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_lo = _addr(B2_RANGE_START)
        a_hi = _addr(B2_RANGE_END)
        print("[B2.1] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B2: %s" % e)
        print("[B2.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[B2.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd = DisassembleCommand(stub_a, None, False)
            if cmd.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd.getStatusMsg()))
        # Force DWord on pool words
        for pool_addr, pool_val, pool_label, pool_eol in B2_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("[B2.5] label %s @ 0x%08x created" % (stub_label, stub_addr))
            else:
                print("[B2.5] label %s already present" % stub_label)
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    # ----- B3: fn_eligible_machine_dup_and_league @ 0x0807356c..0x080735b3 -----
    # FS handler refs: 0x09e41288 (CID=0x157a Machine Duplication), 0x09e42dd0 (CID=0x1978 League)
    # Block: 0x0807356c/0x48, end 0x080735b4
    # Note: .zero 2 at 0x0807356a (padding before fn); fn starts at 0x0807356c
    # Pool words: [0x080735a8]=gP1LifePoints(0x0201c4e0), [0x080735ac]=gDuelPhaseFlags(0x0201b290)
    #             [0x080735b0]=0x080735b4 (ptr to B4 dispatch table)
    # Dispatch table: 0x080735b4..0x08073627 (29 words)
    print("\n--- BLOCK B3: fn_eligible_machine_dup_and_league @ 0x0807356c ---")
    B3_CLEAR_START = 0x0807356c
    B3_CLEAR_END   = 0x080735b3  # inclusive (end of fn stub)
    B3_ENTRY       = 0x0807356c
    B3_LABEL       = 'fn_eligible_machine_dup_and_league_356c'
    B3_EOL         = 'fn_eligible: Machine Duplication (CID=0x157a) + League (CID=0x1978) shared; FS THUMB+1 x2'
    B3_POOL = [
        (0x080735a8, 0x0201c4e0, 'pool_b3_35a8',
         'gP1LifePoints=0x0201c4e0; literal pool fn_eligible_machine_dup_and_league'),
        (0x080735ac, 0x0201b290, 'pool_b3_35ac',
         'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_machine_dup_and_league'),
        (0x080735b0, 0x080735b4, 'pool_b3_35b0',
         '0x080735b4=machine_dup_dispatch_table_35b4; literal pool fn_eligible_machine_dup_and_league'),
    ]
    B3_TABLE_LABEL = 'machine_dup_dispatch_table_35b4'
    B3_TABLE_EOL   = 'dispatch table: 29 entries (zone_type -> B4 sub-stub); Machine Dup/League handler'

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B3_CLEAR_START, B3_CLEAR_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B3_ENTRY)
        print("[dry] label dispatch table %s" % B3_TABLE_LABEL)
    else:
        a_lo = _addr(B3_CLEAR_START)
        a_hi = _addr(B3_CLEAR_END)
        a_en = _addr(B3_ENTRY)
        print("[B3.1] clearListing 0x%08x..0x%08x" % (B3_CLEAR_START, B3_CLEAR_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B3: %s" % e)
        print("[B3.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B3.3] DisassembleCommand @ 0x%08x" % B3_ENTRY)
        cmd = DisassembleCommand(a_en, None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B3: %s" % cmd.getStatusMsg())
        # Label fn entry
        existing = [s.getName() for s in sym_tbl.getSymbols(a_en)]
        if B3_LABEL not in existing:
            sym_tbl.createLabel(a_en, B3_LABEL, SourceType.USER_DEFINED)
            print("[B3.4] label %s created" % B3_LABEL)
        cu_b3 = listing.getCodeUnitAt(a_en)
        if cu_b3 is not None:
            cu_b3.setComment(CodeUnit.EOL_COMMENT, B3_EOL)
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B3_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # Label dispatch table
        dt_addr = _addr(0x080735b4)
        existing_dt = [s.getName() for s in sym_tbl.getSymbols(dt_addr)]
        if B3_TABLE_LABEL not in existing_dt:
            sym_tbl.createLabel(dt_addr, B3_TABLE_LABEL, SourceType.USER_DEFINED)
            print("[B3.5] dispatch table label created: %s" % B3_TABLE_LABEL)
        cu_dt = listing.getCodeUnitAt(dt_addr)
        if cu_dt is not None:
            cu_dt.setComment(CodeUnit.EOL_COMMENT, B3_TABLE_EOL)

    # ----- B4: machine_dup dispatch sub-stubs @ 0x08073628..0x0807375f -----
    # Pre-block dispatch table at 0x080735b4..0x08073627 (29 entries)
    # Sub-stub entry points: 0x08073628, 0x08073690, 0x080736ee, 0x08073704, 0x0807373a, 0x0807374c, 0x08073756
    # Default: 0x08073756 (movs r0,#0; return 0; 23 dispatch table entries)
    # Pool words in block: [0x0807368c]=0x11d, [0x080736a0]=0x157a(Machine Dup CID), [0x080736a4]=0x1978(League CID)
    print("\n--- BLOCK B4: machine_dup_dispatch_sub_stubs_3628 @ 0x08073628..0x0807375f ---")
    B4_RANGE_START = 0x08073628
    B4_RANGE_END   = 0x0807375f  # inclusive

    B4_STUBS = [
        (0x08073628, 'machine_dup_sub_3628',
         'raw-dispatch sub-stub (table[0x08073624]=0x08073628); see machine_dup_dispatch_table_35b4'),
        (0x08073690, 'machine_dup_sub_3690', None),
        (0x080736ee, 'machine_dup_sub_36ee', None),
        (0x08073704, 'machine_dup_sub_3704', None),
        (0x0807373a, 'machine_dup_sub_373a', None),
        (0x0807374c, 'machine_dup_sub_374c', None),
        (0x08073756, 'machine_dup_default_3756',
         'default sub-stub: movs r0,#0; return 0 (23 dispatch table entries point here)'),
    ]
    # Pool words: [0x0807368c]=0x11d (zone count boundary), [0x080736a0]=0x157a, [0x080736a4]=0x1978
    B4_POOL = [
        (0x0807368c, 0x0000011d, 'pool_b4_368c', '0x11d=285 zone count upper bound; literal pool B4'),
        (0x080736a0, 0x0000157a, 'pool_b4_36a0', '0x157a=MACHINE_DUPLICATION_CID; literal pool B4'),
        (0x080736a4, 0x00001978, 'pool_b4_36a4', '0x1978=LEAGUE_OF_UNIFORMITY_CID; literal pool B4'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B4_RANGE_START, B4_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_lo = _addr(B4_RANGE_START)
        a_hi = _addr(B4_RANGE_END)
        print("[B4.1] clearListing 0x%08x..0x%08x" % (B4_RANGE_START, B4_RANGE_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B4: %s" % e)
        print("[B4.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            print("[B4.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd = DisassembleCommand(stub_a, None, False)
            if cmd.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd.getStatusMsg()))
        # Force DWord on pool words
        for pool_addr, pool_val, pool_label, pool_eol in B4_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B4_STUBS:
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("[B4.5] label %s @ 0x%08x created" % (stub_label, stub_addr))
            else:
                print("[B4.5] label %s already present" % stub_label)
            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

    # ----- B5: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864..0x0807388b -----
    # FS handler refs: 0x09e44108 (CID=0x1590 A Cat of Ill Omen), 0x09e44138 (CID=0x1593 An Owl of Luck)
    # Shared stub for both cards. Neither CID appears as literal pool word in fn body.
    # Pool words: [0x08073884]=gDuelPhaseFlags(0x0201b290), [0x08073888]=0x0807388c (ptr to B6 table)
    # Dispatch table: 0x0807388c..0x080738ff (29 words)
    print("\n--- BLOCK B5: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864 ---")
    B5_CLEAR_START = 0x08073864
    B5_CLEAR_END   = 0x0807388b  # inclusive
    B5_ENTRY       = 0x08073864
    B5_LABEL       = 'fn_eligible_cat_ill_omen_and_owl_of_luck'
    B5_EOL         = 'fn_eligible: A Cat of Ill Omen (CID=0x1590) + An Owl of Luck (CID=0x1593) shared stub'
    B5_POOL = [
        (0x08073884, 0x0201b290, 'pool_b5_3884',
         'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_cat_ill_omen_and_owl_of_luck'),
        (0x08073888, 0x0807388c, 'pool_b5_3888',
         '0x0807388c=cat_ill_omen_dispatch_table_388c; literal pool fn_eligible_cat_ill_omen_and_owl_of_luck'),
    ]
    B5_TABLE_LABEL = 'cat_ill_omen_dispatch_table_388c'
    B5_TABLE_EOL   = 'dispatch table: 29 entries (zone_type -> B6 sub-stub); Cat of Ill Omen/Owl of Luck handler'

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B5_CLEAR_START, B5_CLEAR_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B5_ENTRY)
        print("[dry] label dispatch table %s" % B5_TABLE_LABEL)
    else:
        a_lo = _addr(B5_CLEAR_START)
        a_hi = _addr(B5_CLEAR_END)
        a_en = _addr(B5_ENTRY)
        print("[B5.1] clearListing 0x%08x..0x%08x" % (B5_CLEAR_START, B5_CLEAR_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B5: %s" % e)
        print("[B5.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")
        print("[B5.3] DisassembleCommand @ 0x%08x" % B5_ENTRY)
        cmd = DisassembleCommand(a_en, None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B5: %s" % cmd.getStatusMsg())
        # Label fn entry
        existing = [s.getName() for s in sym_tbl.getSymbols(a_en)]
        if B5_LABEL not in existing:
            sym_tbl.createLabel(a_en, B5_LABEL, SourceType.USER_DEFINED)
            print("[B5.4] label %s created" % B5_LABEL)
        cu_b5 = listing.getCodeUnitAt(a_en)
        if cu_b5 is not None:
            cu_b5.setComment(CodeUnit.EOL_COMMENT, B5_EOL)
        # Literal pool DWords
        for pool_addr, pool_val, pool_label, pool_eol in B5_POOL:
            force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)
        # Label dispatch table
        dt_addr = _addr(0x0807388c)
        existing_dt = [s.getName() for s in sym_tbl.getSymbols(dt_addr)]
        if B5_TABLE_LABEL not in existing_dt:
            sym_tbl.createLabel(dt_addr, B5_TABLE_LABEL, SourceType.USER_DEFINED)
            print("[B5.5] dispatch table label created: %s" % B5_TABLE_LABEL)
        cu_dt = listing.getCodeUnitAt(dt_addr)
        if cu_dt is not None:
            cu_dt.setComment(CodeUnit.EOL_COMMENT, B5_TABLE_EOL)

    # ----- B6: cat_ill_omen dispatch sub-stubs @ 0x08073900..0x08073a5b -----
    # Pre-block dispatch table at 0x0807388c..0x080738ff (29 entries, in B5 region)
    # Sub-stub entry points: 0x08073900, 0x08073932, 0x08073946, 0x08073968, 0x080739b0,
    #                        0x08073a34, 0x08073a46, 0x08073a54
    # Default stub: 0x08073a54 (movs r0,#0 / pop {r4,r5,r6} / pop {r1} / bx r1; 22 entries)
    # Pool words in block: [0x08073990]=0x159d (NECROVALLEY_CID, already in card_info.inc)
    #                      [0x08073994]=0x0201e2a0 (gDuelCardCtxBase, already in ewram.inc)
    #                      [0x08073998]=0x131 (zone sub-index boundary)
    #                      [0x080739ac]=gP1LifePoints(0x0201c4e0)
    #                      [0x080739d4]=gP1LifePoints(0x0201c4e0)
    #                      [0x08073a30]=0x8056 (OAM_EFFECT_SLOT_TILE_P1, already in oam_attr.inc)
    print("\n--- BLOCK B6: cat_ill_omen_dispatch_sub_stubs_3900 @ 0x08073900..0x08073a5b ---")
    B6_RANGE_START = 0x08073900
    B6_RANGE_END   = 0x08073a5b  # inclusive

    B6_STUBS = [
        (0x08073900, 'cat_ill_omen_sub_3900',
         'raw-dispatch sub-stub (table[0x080738fc]=0x08073900); see cat_ill_omen_dispatch_table_388c'),
        (0x08073932, 'cat_ill_omen_sub_3932', None),
        (0x08073946, 'cat_ill_omen_sub_3946', None),
        (0x08073968, 'cat_ill_omen_sub_3968', None),
        (0x080739b0, 'cat_ill_omen_sub_39b0', None),
        (0x08073a34, 'cat_ill_omen_sub_3a34', None),
        (0x08073a46, 'cat_ill_omen_sub_3a46', None),
        (0x08073a54, 'cat_ill_omen_default_3a54',
         'default sub-stub: movs r0,#0; pop {r4,r5,r6}; pop {r1}; bx r1 (22 dispatch table entries)'),
    ]
    # Pool words (all pre-existing constants, just need DWord + label)
    B6_POOL = [
        (0x08073990, 0x0000159d, 'pool_b6_3990', 'NECROVALLEY_CID=0x159d; literal pool B6 sub_3968'),
        (0x08073994, 0x0201e2a0, 'pool_b6_3994', 'gDuelCardCtxBase=0x0201e2a0; literal pool B6 sub_3968'),
        (0x08073998, 0x00000131, 'pool_b6_3998', '0x131=305; zone sub-index boundary; literal pool B6 sub_3968'),
        (0x080739ac, 0x0201c4e0, 'pool_b6_39ac', 'gP1LifePoints=0x0201c4e0; literal pool B6 sub_399c'),
        (0x080739d4, 0x0201c4e0, 'pool_b6_39d4', 'gP1LifePoints=0x0201c4e0; literal pool B6 sub_39b0'),
        (0x08073a30, 0x00008056, 'pool_b6_3a30', 'OAM_EFFECT_SLOT_TILE_P1=0x8056; literal pool B6 sub_39b0'),
    ]

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B6_RANGE_START, B6_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B6_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        a_lo = _addr(B6_RANGE_START)
        a_hi = _addr(B6_RANGE_END)
        print("[B6.1] clearListing 0x%08x..0x%08x" % (B6_RANGE_START, B6_RANGE_END))
        try:
            clearListing(a_lo, a_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B6: %s" % e)
        print("[B6.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode not found")
        # Per-stub DisassembleCommand
        for stub_addr, stub_label, stub_eol in B6_STUBS:
            print("[B6.3] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd = DisassembleCommand(stub_a, None, False)
            if cmd.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd.getStatusMsg()))
        # Force DWord on pool words
        for pool_addr, pool_val, pool_label, pool_eol in B6_POOL:
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

    print("\n=== RefineF09Seg5aSlots DONE ===")
    print("  EQ: %d slots (38 REUSE + 10 NEW)" % len(EQ_SLOTS))
    print("  REF: %d slots -> gP1LifePoints(0x0201c4e0)" % len(REF_SLOTS))
    print("  RENAME: trap_dustshoot_dispatch_sub_stubs_31e4 / machine_dup_dispatch_sub_stubs_3628 / cat_ill_omen_dispatch_sub_stubs_3900")
    print("  DISASM B1: fn_eligible_trap_dustshoot_3140 @ 0x08073140")
    print("  DISASM B2: 6 sub-stubs trap_dustshoot @ 0x080731e4..0x080732a7")
    print("  DISASM B3: fn_eligible_machine_dup_and_league_356c @ 0x0807356c")
    print("  DISASM B4: 7 sub-stubs machine_dup @ 0x08073628..0x0807375f")
    print("  DISASM B5: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864")
    print("  DISASM B6: 8 sub-stubs cat_ill_omen @ 0x08073900..0x08073a5b")


main()
