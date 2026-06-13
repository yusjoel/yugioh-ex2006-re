# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF06Seg6Blocks.py -- F06 Seg-6 R4 disasm (3 ranges)
#
# Range 1: unlabeled fn check_equip_slot_active_for_player_and_group @ 0x08057678
#   Currently inside dead-zone of apply_lp_delta_for_slot_player_mode0.
#   THUMB fn @ 0x57678..0x576ab: player/slot predicate, returns 0/1.
#   THUMB+1 refs at 0x08057778 and 0x08057b88 (DAT_ slots).
#   clearListing(0x57678..0x576af) -> setTMode -> disasm -> createFunction + name + plate.
#
# Range 2: block1 dispatch fn @ 0x08057d0c (inside ROM_INCBIN 0x57d0a, 0x2a)
#   2 zero-pad bytes @ 0x57d0a (alignment).
#   THUMB fn @ 0x57d0c..0x57d29: 5-state dispatcher (reads [gDuelPhaseFlags+0x4ac]),
#   state<=4 -> indirect jump via ptr_table[state]; state>4 -> return stub @ 0x57ea0.
#   Literal pool @ 0x57d2a..0x57d33: 2 zero + gDuelPhaseFlags(0x0201b290) + STEP_OFF(0x4ac).
#   Ptr-to-table .word @ 0x57d34 = 0x08057d38 (covered by REF in RefineF06Seg6Slots.py).
#   fn-ptr THUMB+1 ref at 0x09e40e8c (CID 0x14e6 Emergency Provisions handler table slot 4).
#   clearListing(0x57d0a..0x57d33) -> setTMode(0x57d0c..0x57d33) -> disasm -> createFn + name + plate.
#
# Range 3: block2 sub-fns @ 0x08057d4c..0x08057ea7 (ROM_INCBIN 0x57d4c, 0x15c)
#   4 sub-functions reached via ptr_table indirect jump (raw addresses, not THUMB+1):
#   - sub-fn A @ 0x57d4c (0xac B): state=0 handler
#   - sub-fn B @ 0x57df8 (0x48 B): state=2 handler
#   - sub-fn C @ 0x57e40 (0x60 B): state=1/4 handler
#   - return stub @ 0x57ea0 (0x8 B): trivial return-1 stub
#   clearListing(0x57d4c..0x57ea7) -> setTMode -> per-stub DisassembleCommand -> label + plate each.
#
# Note: sub-fns in block2 are reached via indirect jump (mov pc,r0) NOT bl.
#   They share the caller's stack frame. Labels are jump-target labels.
#   createFunction attempted but may not succeed for non-entry-point stubs.
#
# All plate comments: ASCII only (no CJK -- Jython double UTF-8 mojibake prevention).
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_052051-pre-f06seg6

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_at(ep_int, block_lo, block_hi):
    """Disassemble at ep_int, restricted to [block_lo..block_hi]."""
    ep_addr = _addr(ep_int)
    lo = _addr(block_lo)
    hi = _addr(block_hi)
    cmd = DisassembleCommand(ep_addr, AddressSet(lo, hi), True)
    if cmd.applyTo(currentProgram):
        print("[ok ] disasm @ 0x%08x" % ep_int)
        return True
    else:
        print("[warn] disasm @ 0x%08x: %s" % (ep_int, cmd.getStatusMsg()))
        return False


def _create_dword(addr_int):
    """Force a DWORD data item at addr_int (literal pool slot)."""
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            print("[DW ] already DWORD @ 0x%08x" % addr_int)
            return True
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr_int)
        return True
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
        return False


def _create_fn_or_label(addr_int, name):
    """Create function (or fallback label) at addr_int with name."""
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    sm = currentProgram.getSymbolTable()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        fn.setName(name, SourceType.USER_DEFINED)
        print("[FN ] renamed existing: %s @ 0x%08x" % (name, addr_int))
        return fn
    fn = createFunction(a, name)
    if fn is not None:
        fn.setName(name, SourceType.USER_DEFINED)
        print("[FN ] created: %s @ 0x%08x" % (name, addr_int))
        return fn
    # fallback: label only
    sm.createLabel(a, name, SourceType.USER_DEFINED)
    print("[FN ] label fallback: %s @ 0x%08x" % (name, addr_int))
    return None


def _set_plate(addr_int, text):
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr_int))
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, text)
        print("[ok ] plate set @ 0x%08x (%d chars)" % (addr_int, len(text)))
    else:
        print("[warn] no CodeUnit @ 0x%08x for plate" % addr_int)


def _count_instrs(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    listing = currentProgram.getListing()
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# =========================================================================
# Range 1: check_equip_slot_active_for_player_and_group @ 0x08057678
# =========================================================================
RANGE1_LO    = 0x08057678
RANGE1_HI    = 0x080576af  # inclusive; 0x576b0 = next fn tick_equip_chain_sprite_and_spell_zone_seq
RANGE1_ENTRY = 0x08057678
# Literal pool @ 0x576a2..0x576ab (0x00000868, 0x0201c510)
RANGE1_POOL_STRIDE = 0x080576a2  # PLAYER_BLOCK_STRIDE
RANGE1_POOL_SLOTS  = 0x080576a6  # gDuelFieldSlots
RANGE1_NAME = 'check_equip_slot_active_for_player_and_group'
RANGE1_PLATE = (
    'check_equip_slot_active_for_player_and_group @ 0x08057678\n'
    'Equip slot active predicate: checks if player slot (r2) in group (r3) is active.\n'
    'Inputs: r0=card_entry, r1=ignored(?), r2=slot_idx, r3=group_id.\n'
    'Decodes player_id from card_entry[+2] bit0 (ldrb/lsls/lsrs).\n'
    'Loads gDuelFieldSlots[player_id * PLAYER_BLOCK_STRIDE + slot_idx * 0x14].\n'
    'Checks zone word bit: lsls #0x13 -> cmp with group -> movs r0,#1 if match / #0 if not.\n'
    'Returns 1 if slot active in group, 0 otherwise. Leaf fn (bx lr).\n'
    'THUMB+1 refs at 0x08057778 (DAT_) and 0x08057b88 (DAT_) as fn-ptr slots.\n'
    'Reached via card effect handler dispatch: not a direct bl callee.\n'
    'Constants: PLAYER_BLOCK_STRIDE=0x868, gDuelFieldSlots=0x0201c510.'
)

# =========================================================================
# Range 2: block1 dispatch fn @ 0x08057d0c (inside ROM_INCBIN 0x57d0a, 0x2a)
# =========================================================================
# clearListing covers 0x57d0a..0x57d33 (2 zero + fn + literal pool, NOT 0x57d34 .word)
RANGE2_CLEAR_LO = 0x08057d0a
RANGE2_CLEAR_HI = 0x08057d33  # inclusive end of literal pool; 0x57d34 = ptr-to-table .word
RANGE2_ENTRY    = 0x08057d0c
RANGE2_NAME     = 'dispatch_emergency_provisions_equip_activation_state'
RANGE2_PLATE    = (
    'dispatch_emergency_provisions_equip_activation_state @ 0x08057d0c\n'
    'Emergency Provisions (CID 0x14e6) equip activation 5-state dispatcher.\n'
    'Entry fn-ptr THUMB+1 ref at 0x09e40e8c (dispatch table slot 4 for CID 0x14e6).\n'
    'Reads [gDuelPhaseFlags + EQUIP_ACTIVATION_STEP_OFF] (0x0201b290+0x4ac); state=0..4.\n'
    'If state > 4: branches to return stub @ 0x08057ea0 (state finished).\n'
    'Otherwise: loads ptr_table_ref @ pc+0x10 (0x57d34 = 0x08057d38), adds state*4,\n'
    'loads raw sub-fn addr, branches via mov pc,r0 (indirect jump, NOT bl).\n'
    'ptr_table @ 0x08057d38: [A=0x57d4c, C=0x57e40, B=0x57df8, stub=0x57ea0, C=0x57e40].\n'
    'Literal pool @ 0x57d2c: gDuelPhaseFlags=0x0201b290, STEP_OFF=0x000004ac.\n'
    'Sub-fns (block2) share stack frame via push/pop in this fn.\n'
    'reached via card effect handler dispatch table 0x09e40e8c, CID 0x14e6 Emergency Provisions.'
)

# =========================================================================
# Range 3: block2 sub-fns @ 0x08057d4c..0x08057ea7 (ROM_INCBIN 0x57d4c, 0x15c)
# =========================================================================
RANGE3_LO = 0x08057d4c
RANGE3_HI = 0x08057ea7  # inclusive; 0x57ea8 = next fn set_lp_row_type2_for_equip_tier_abc
# 4 entry points (raw addresses, used by indirect jump not bl)
RANGE3_ENTRIES = [
    (0x08057d4c, 'dispatch_ep_state0_lp_display',
     'dispatch_ep_state0_lp_display @ 0x08057d4c\n'
     'Emergency Provisions state=0 handler (sub-fn A). Reached via indirect jump\n'
     'from dispatch_emergency_provisions_equip_activation_state (ptr_table entry 0).\n'
     'Clears slot[+8] (strh r0,[r4,#8]); triggers card display op 0x3a\n'
     '(trigger_card_display_op31_if_not_active); checks check_equip_slot_eligible;\n'
     'calls set_lp_row_type2_with_nonzero_flag. Returns via shared caller stack frame.\n'
     'ptr_table raw ref at 0x08057d38 (state=0 entry). Part of Emergency Provisions dispatch.\n'
     'reached via card effect handler dispatch table 0x09e40e8c, CID 0x14e6 Emergency Provisions.'),

    (0x08057df8, 'dispatch_ep_state2_slot_display',
     'dispatch_ep_state2_slot_display @ 0x08057df8\n'
     'Emergency Provisions state=2 handler (sub-fn B). Reached via indirect jump.\n'
     'Calls check_spell_zone_slot_placeable; reads LP; strh slot[+8]; set_lp_display_row_type8.\n'
     'ptr_table raw ref at 0x08057d40 (state=2 entry).\n'
     'reached via card effect handler dispatch table 0x09e40e8c, CID 0x14e6 Emergency Provisions.'),

    (0x08057e40, 'dispatch_ep_state1_confirm_lp',
     'dispatch_ep_state1_confirm_lp @ 0x08057e40\n'
     'Emergency Provisions state=1/4 handler (sub-fn C). Reached via indirect jump.\n'
     'Calls check_activation_display_state_is_confirmed; invokes LP row update.\n'
     'ptr_table raw refs at 0x08057d3c (state=1) and 0x08057d48 (state=4) -- shared.\n'
     'reached via card effect handler dispatch table 0x09e40e8c, CID 0x14e6 Emergency Provisions.'),

    (0x08057ea0, 'dispatch_ep_state3_return',
     'dispatch_ep_state3_return @ 0x08057ea0\n'
     'Emergency Provisions state=3 return stub. Trivial: movs r0,#1; pop{r4,r5}; pop{r1}; bx r1.\n'
     'Returns 1 (success/complete) to the original caller of the main dispatch fn.\n'
     'ptr_table raw ref at 0x08057d44 (state=3 entry).\n'
     'reached via card effect handler dispatch table 0x09e40e8c, CID 0x14e6 Emergency Provisions.'),
]


def main():
    print("=== DisassembleF06Seg6Blocks (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()

    # =====================================================================
    # Range 1: check_equip_slot_active_for_player_and_group
    # =====================================================================
    print("\n--- Range 1: %s @ 0x%08x ---" % (RANGE1_NAME, RANGE1_ENTRY))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (RANGE1_LO, RANGE1_HI))
        print("[dry] disasm @ 0x%08x" % RANGE1_ENTRY)
        print("[dry] createDWord @ 0x%08x (PLAYER_BLOCK_STRIDE)" % RANGE1_POOL_STRIDE)
        print("[dry] createDWord @ 0x%08x (gDuelFieldSlots)" % RANGE1_POOL_SLOTS)
        print("[dry] createFunction + setName '%s'" % RANGE1_NAME)
        print("[dry] setPlateComment (%d chars)" % len(RANGE1_PLATE))
    else:
        _clear_and_set_thumb(RANGE1_LO, RANGE1_HI)
        _disasm_at(RANGE1_ENTRY, RANGE1_LO, RANGE1_HI)
        _create_dword(RANGE1_POOL_STRIDE)
        _create_dword(RANGE1_POOL_SLOTS)
        _create_fn_or_label(RANGE1_ENTRY, RANGE1_NAME)
        _set_plate(RANGE1_ENTRY, RANGE1_PLATE)
        n = _count_instrs(RANGE1_LO, RANGE1_HI)
        print("[ok ] Range 1: %d instructions" % n)

    # =====================================================================
    # Range 2: block1 dispatch fn (inside ROM_INCBIN 0x57d0a, 0x2a)
    # =====================================================================
    print("\n--- Range 2: %s @ 0x%08x ---" % (RANGE2_NAME, RANGE2_ENTRY))
    # Literal pool slots @ 0x57d2c (gDuelPhaseFlags) and 0x57d30 (STEP_OFF)
    # Zero-pad bytes @ 0x57d0a..0x57d0b and @ 0x57d2a..0x57d2b (literal pool alignment)
    RANGE2_POOL_PHASE = 0x08057d2c  # gDuelPhaseFlags = 0x0201b290
    RANGE2_POOL_STEP  = 0x08057d30  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (RANGE2_CLEAR_LO, RANGE2_CLEAR_HI))
        print("[dry] disasm @ 0x%08x (block1 fn entry)" % RANGE2_ENTRY)
        print("[dry] createDWord @ 0x%08x (gDuelPhaseFlags)" % RANGE2_POOL_PHASE)
        print("[dry] createDWord @ 0x%08x (EQUIP_ACTIVATION_STEP_OFF)" % RANGE2_POOL_STEP)
        print("[dry] createFunction + setName '%s'" % RANGE2_NAME)
        print("[dry] setPlateComment (%d chars)" % len(RANGE2_PLATE))
    else:
        _clear_and_set_thumb(RANGE2_CLEAR_LO, RANGE2_CLEAR_HI)
        _disasm_at(RANGE2_ENTRY, RANGE2_CLEAR_LO, RANGE2_CLEAR_HI)
        _create_dword(RANGE2_POOL_PHASE)
        _create_dword(RANGE2_POOL_STEP)
        _create_fn_or_label(RANGE2_ENTRY, RANGE2_NAME)
        _set_plate(RANGE2_ENTRY, RANGE2_PLATE)
        n = _count_instrs(RANGE2_CLEAR_LO, RANGE2_CLEAR_HI)
        print("[ok ] Range 2: %d instructions" % n)

    # =====================================================================
    # Range 3: block2 sub-fns (ROM_INCBIN 0x57d4c, 0x15c)
    # =====================================================================
    print("\n--- Range 3: block2 sub-fns 0x%08x..0x%08x ---" % (RANGE3_LO, RANGE3_HI))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (RANGE3_LO, RANGE3_HI))
        for ep, lbl, plate in RANGE3_ENTRIES:
            print("[dry] disasm @ 0x%08x label=%s" % (ep, lbl))
            print("[dry] setPlateComment @ 0x%08x (%d chars)" % (ep, len(plate)))
    else:
        _clear_and_set_thumb(RANGE3_LO, RANGE3_HI)
        sm = currentProgram.getSymbolTable()
        fm = currentProgram.getFunctionManager()
        ok_count = 0
        for ep_int, ep_label, ep_plate in RANGE3_ENTRIES:
            if _disasm_at(ep_int, RANGE3_LO, RANGE3_HI):
                ok_count += 1
            # Apply label (these are jump-target labels, createFunction may or may not succeed)
            ep_addr = _addr(ep_int)
            try:
                sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
                print("[ok ] label '%s' @ 0x%08x" % (ep_label, ep_int))
            except Exception as le:
                print("[warn] label @ 0x%08x: %s" % (ep_int, le))
            # Try createFunction (best-effort -- sub-fns may not be recognized as fns)
            fn = fm.getFunctionAt(ep_addr)
            if fn is None:
                fn = createFunction(ep_addr, ep_label)
                if fn is not None:
                    print("[FN ] created: %s @ 0x%08x" % (ep_label, ep_int))
                else:
                    print("[FN ] no function created @ 0x%08x (jump target label only)" % ep_int)
            else:
                fn.setName(ep_label, SourceType.USER_DEFINED)
                print("[FN ] renamed: %s @ 0x%08x" % (ep_label, ep_int))
            # Set plate comment
            _set_plate(ep_int, ep_plate)

        n_total = _count_instrs(RANGE3_LO, RANGE3_HI)
        print("[ok ] Range 3: %d/%d stubs disasmed, %d instructions total" % (
            ok_count, len(RANGE3_ENTRIES), n_total))

    print("\n=== DisassembleF06Seg6Blocks DONE (DRY=%s) ===" % DRY)


main()
