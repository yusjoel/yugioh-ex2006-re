# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF06Seg8Blocks.py -- F06 Seg-8 R4 disasm (4 ranges)
#
# Block1 @ 0x0805953c..0x08059567 (ROM_INCBIN 0x5953a 0x2a; 2 zero pad bytes at 0x5953a..0x5953b)
#   Function: dispatch_equip_activation_seq_by_type80 inner code (code entry at 0x0805953c)
#   AKA: equip_type80_activation_case_dispatch
#   THUMB fn: push{r4,r5,lr}; reads [gDuelPhaseFlags+STEP_OFF]; cmp r0,#7; bhi default;
#   dispatch via PTR_DAT_08059568 using 'mov pc, r0' (0x4687) -- NOT bx, stays THUMB.
#   Literal pool at 0x0805955c..0x08059567 (gDuelPhaseFlags/STEP_OFF/PTR_DAT_08059568).
#   THUMB+1 ref from fn-ptr table at 0x09e46fac (CID 0x183a row).
#   Note: dispatch_equip_activation_seq_by_type80 function already named; this creates its body.
#
# Block2 @ 0x08059588..0x080596eb (ROM_INCBIN 0x59588 0x164)
#   6 unique THUMB sub-fns reached via raw-addr dispatch from Block1 ('mov pc, r0'):
#   - equip_type80_case0_and_1_init_sprite @ 0x08059588
#   - equip_type80_case1_also @ 0x080595a8
#   - equip_type80_case2_and_5_no_op @ 0x080595d4
#   - equip_type80_case3_and_6_select_target @ 0x08059618
#   - equip_type80_case4_enqueue @ 0x08059670
#   - equip_type80_case7_and_return0 @ 0x080596d4
#   All sub-fns THUMB; raw-addr entries (lsb=0) in dispatch table because 'mov pc,r0' not BX.
#
# Block3 @ 0x08059cc8..0x08059cef (ROM_INCBIN 0x59cc8 0x28)
#   Function: equip_lp_spell_zone_case_dispatch
#   THUMB fn: push{r4-r7,lr}; reads [gDuelPhaseFlags+STEP_OFF]; cmp r0,#7; bhi far stub;
#   dispatch via PTR_DAT_08059cf4 using 'mov pc, r0' (0x4687) -- stays THUMB.
#   Literal pool at 0x08059ce0..0x08059cef (gDuelPhaseFlags/STEP_OFF/ptr-to-table).
#   THUMB+1 ref from fn-ptr table at 0x09e451dc (CID 0x18e0 row).
#
# Block4 @ 0x08059d14..0x08059ddf (ROM_INCBIN 0x59d14 0xcc)
#   5 unique THUMB sub-fns reached via raw-addr dispatch from Block3:
#   - equip_lp_spell_zone_case_shared_abc @ 0x08059d14 (cases 0,1,2 -> same entry)
#   - equip_lp_spell_zone_case5_op31 @ 0x08059d38 (case 5)
#   - equip_lp_spell_zone_case6_something @ 0x08059d54 (case 6)
#   - equip_lp_spell_zone_case7_something @ 0x08059d90 (case 7)
#   - equip_lp_spell_zone_case34_return1 @ 0x08059dd4 (cases 3,4 -> same entry)
#
# Dispatch tables PTR_DAT_08059568 and PTR_DAT_08059cf4 already present in asm as labeled .word
# entries. Block1/Block3 will be labeled as functions; Block2/Block4 sub-fns via jump-target labels.
#
# All plate comments: ASCII only (no CJK -- Jython double UTF-8 mojibake prevention).
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_071238-pre-F06Seg8

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
    """Force a DWORD data item at addr_int (literal pool slot).
    Clears any existing instruction/data at the 4-byte range first."""
    a = _addr(addr_int)
    hi = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            print("[DW ] already DWORD @ 0x%08x" % addr_int)
            return True
        # Clear any conflicting instructions/data first
        try:
            clearListing(a, hi)
        except Exception:
            pass
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
# Block1: dispatch_equip_activation_seq_by_type80 body @ 0x0805953c
#   ROM_INCBIN 0x5953a 0x2a: 2 zero-pad bytes at 0x5953a..0x5953b; code at 0x5953c..0x59563
#   Literal pool: [0x5955c]=gDuelPhaseFlags, [0x59560]=STEP_OFF, [0x59564]=ptr_to_table
# =========================================================================
BLOCK1_CLEAR_LO = 0x0805953a  # inclusive: 2 zero pad bytes
BLOCK1_CLEAR_HI = 0x0805956b  # inclusive: end of literal pool (0x59564..0x5956b is PTR slot area)
BLOCK1_ENTRY    = 0x0805953c
BLOCK1_POOL     = [
    0x0805955c,  # gDuelPhaseFlags = 0x0201b290
    0x08059560,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x08059564,  # ptr-to-table = 0x08059568 (address of PTR_DAT_08059568)
]
BLOCK1_NAME  = 'dispatch_equip_activation_seq_by_type80'
BLOCK1_PLATE = (
    'dispatch_equip_activation_seq_by_type80 @ 0x0805953c\n'
    'Type-80 equip activation 8-case state dispatcher (inner body).\n'
    'Entry fn-ptr THUMB+1 ref at 0x09e46fac (dispatch table slot for CID 0x183a).\n'
    'Reads [gDuelPhaseFlags + EQUIP_ACTIVATION_STEP_OFF] (0x0201b290+0x4ac); state=0..7.\n'
    'If state > 7: branches to default stub (equip_type80_case7_and_return0 return-0 path).\n'
    'Otherwise: loads ptr_table_ref @ pc+offset (0x08059568 = PTR_DAT_08059568), adds state*4,\n'
    'loads raw sub-fn addr, branches via mov pc,r0 (indirect, NOT BX -- stays THUMB).\n'
    'Dispatch table @ 0x08059568: 8 entries, raw THUMB addrs (lsb=0):\n'
    '  [0]=0x8059588, [1]=0x80595a8, [2]=0x80595d4, [3]=0x8059618,\n'
    '  [4]=0x8059670, [5]=0x80595d4, [6]=0x8059618, [7]=0x80596d4.\n'
    'Sub-fns (block2) share caller stack frame (push in block1 dispatcher).\n'
    'indeg=1 via fn-ptr table 0x09e46fac.'
)

# =========================================================================
# Block2: 6 THUMB sub-fns @ 0x08059588..0x080596eb (ROM_INCBIN 0x59588 0x164)
#   Reached via raw-addr dispatch from Block1 (mov pc, r0; no mode switch).
# =========================================================================
BLOCK2_LO = 0x08059588
BLOCK2_HI = 0x080596eb  # inclusive; 0x80596ec = next named fn tick_equip_banisher_lp_display_seq
BLOCK2_ENTRIES = [
    (0x08059588, 'equip_type80_case0_and_1_init_sprite',
     'equip_type80_case0_and_1_init_sprite @ 0x08059588\n'
     'Type-80 equip activation sub-fn: handles state=0 and state=1 (shared entry).\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'State=0/1: calls init_equip_slot_sprite_attr or similar setup; advances step counter.\n'
     'Part of type-80 equip activation state machine. Uses shared caller stack frame.\n'
     'Dispatch table ref: equip_type80_dispatch_table_ptr[0]=0x08059588, [1]=0x080595a8.'),

    (0x080595a8, 'equip_type80_case1_also',
     'equip_type80_case1_also @ 0x080595a8\n'
     'Type-80 equip activation sub-fn: secondary state=1 entry.\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'Dispatch table ref: equip_type80_dispatch_table_ptr[1]=0x080595a8.\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x080595d4, 'equip_type80_case2_and_5_no_op',
     'equip_type80_case2_and_5_no_op @ 0x080595d4\n'
     'Type-80 equip activation sub-fn: handles state=2 and state=5 (no-op/pass-through).\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'External THUMB+1 ref at 0x086f4074 (to 0x08059615, within this sub-fn).\n'
     'Dispatch table refs: equip_type80_dispatch_table_ptr[2]=0x80595d4, [5]=0x80595d4.\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x08059618, 'equip_type80_case3_and_6_select_target',
     'equip_type80_case3_and_6_select_target @ 0x08059618\n'
     'Type-80 equip activation sub-fn: handles state=3 and state=6 (select target).\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'Dispatch table refs: equip_type80_dispatch_table_ptr[3]=0x8059618, [6]=0x8059618.\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x08059670, 'equip_type80_case4_enqueue',
     'equip_type80_case4_enqueue @ 0x08059670\n'
     'Type-80 equip activation sub-fn: handles state=4 (enqueue sprite/effect).\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'Dispatch table ref: equip_type80_dispatch_table_ptr[4]=0x8059670.\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x080596d4, 'equip_type80_case7_and_return0',
     'equip_type80_case7_and_return0 @ 0x080596d4\n'
     'Type-80 equip activation sub-fn: state=7 handler + default return-0 stub.\n'
     'Reached via raw-addr dispatch from dispatch_equip_activation_seq_by_type80 (mov pc,r0).\n'
     'Dispatch table ref: equip_type80_dispatch_table_ptr[7]=0x80596d4. Default branch also here.\n'
     'Returns 0 (no match / terminal state). Uses shared caller stack frame.'),
]

# =========================================================================
# Block3: equip_lp_spell_zone_case_dispatch @ 0x08059cc8
#   ROM_INCBIN 0x59cc8 0x28
#   Literal pool: [0x59ce0]=gDuelPhaseFlags, [0x59ce4]=STEP_OFF,
#                 ptr-to-table via [pc+#0x10] at instr 0x59cde -> loads 0x08059cf0
#                 [0x59cf0] = 0x08059cf4 (address of PTR_DAT_08059cf4 table)
# =========================================================================
BLOCK3_CLEAR_LO = 0x08059cc8
BLOCK3_CLEAR_HI = 0x08059cef  # inclusive end (0x08059cc8 + 0x28 - 1 = 0x08059cef)
BLOCK3_ENTRY    = 0x08059cc8
BLOCK3_POOL     = [
    0x08059ce0,  # gDuelPhaseFlags = 0x0201b290
    0x08059ce4,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x08059cf0,  # ptr-to-table = 0x08059cf4 (address of PTR_DAT_08059cf4)
]
BLOCK3_NAME  = 'equip_lp_spell_zone_case_dispatch'
BLOCK3_PLATE = (
    'equip_lp_spell_zone_case_dispatch @ 0x08059cc8\n'
    'LP spell zone equip 8-case state dispatcher.\n'
    'Entry fn-ptr THUMB+1 ref at 0x09e451dc (dispatch table slot for CID 0x18e0).\n'
    'Reads [gDuelPhaseFlags + EQUIP_ACTIVATION_STEP_OFF] (0x0201b290+0x4ac); state=0..7.\n'
    'If state > 7: branches to far return stub (beyond block4).\n'
    'Otherwise: lsls r0,r0,#2; ldr r1,[pc,#0x10] (loads 0x08059cf4 = PTR_DAT_08059cf4);\n'
    'adds r0,r0,r1; ldr r0,[r0]; mov pc,r0 (indirect, NOT BX -- stays THUMB).\n'
    'Dispatch table @ 0x08059cf4: 8 entries, raw THUMB addrs (lsb=0):\n'
    '  [0..2]=0x8059d14, [3..4]=0x8059dd4, [5]=0x8059d38, [6]=0x8059d54, [7]=0x8059d90.\n'
    'Sub-fns (block4) share caller stack frame.\n'
    'indeg=1 via fn-ptr table 0x09e451dc.'
)

# =========================================================================
# Block4: 5 THUMB sub-fns @ 0x08059d14..0x08059ddf (ROM_INCBIN 0x59d14 0xcc)
#   Reached via raw-addr dispatch from Block3 (mov pc, r0).
# =========================================================================
BLOCK4_LO = 0x08059d14
BLOCK4_HI = 0x08059ddf  # inclusive; 0x08059d14 + 0xcc - 1 = 0x08059ddf
BLOCK4_ENTRIES = [
    (0x08059d14, 'equip_lp_spell_zone_case_shared_abc',
     'equip_lp_spell_zone_case_shared_abc @ 0x08059d14\n'
     'LP spell zone equip sub-fn: handles states 0, 1, and 2 (shared entry).\n'
     'Reached via raw-addr dispatch from equip_lp_spell_zone_case_dispatch (mov pc,r0).\n'
     'Dispatch table refs: equip_lp_spell_zone_dispatch_table_ptr[0..2]=0x8059d14.\n'
     'Uses shared caller stack frame from Block3 dispatcher.'),

    (0x08059d38, 'equip_lp_spell_zone_case5_op31',
     'equip_lp_spell_zone_case5_op31 @ 0x08059d38\n'
     'LP spell zone equip sub-fn: handles state 5 (op31 trigger).\n'
     'Reached via raw-addr dispatch from equip_lp_spell_zone_case_dispatch (mov pc,r0).\n'
     'Dispatch table ref: equip_lp_spell_zone_dispatch_table_ptr[5]=0x8059d38.\n'
     'Uses shared caller stack frame from Block3 dispatcher.'),

    (0x08059d54, 'equip_lp_spell_zone_case6_something',
     'equip_lp_spell_zone_case6_something @ 0x08059d54\n'
     'LP spell zone equip sub-fn: handles state 6.\n'
     'Reached via raw-addr dispatch from equip_lp_spell_zone_case_dispatch (mov pc,r0).\n'
     'Dispatch table ref: equip_lp_spell_zone_dispatch_table_ptr[6]=0x8059d54.\n'
     'Uses shared caller stack frame from Block3 dispatcher.'),

    (0x08059d90, 'equip_lp_spell_zone_case7_something',
     'equip_lp_spell_zone_case7_something @ 0x08059d90\n'
     'LP spell zone equip sub-fn: handles state 7.\n'
     'Reached via raw-addr dispatch from equip_lp_spell_zone_case_dispatch (mov pc,r0).\n'
     'Dispatch table ref: equip_lp_spell_zone_dispatch_table_ptr[7]=0x8059d90.\n'
     'Uses shared caller stack frame from Block3 dispatcher.'),

    (0x08059dd4, 'equip_lp_spell_zone_case34_return1',
     'equip_lp_spell_zone_case34_return1 @ 0x08059dd4\n'
     'LP spell zone equip sub-fn: handles states 3 and 4 (return-1 / complete).\n'
     'Reached via raw-addr dispatch from equip_lp_spell_zone_case_dispatch (mov pc,r0).\n'
     'Dispatch table refs: equip_lp_spell_zone_dispatch_table_ptr[3..4]=0x8059dd4.\n'
     'Returns 1 (activation complete). Uses shared caller stack frame from Block3 dispatcher.'),
]


def main():
    print("=== DisassembleF06Seg8Blocks (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()

    # =====================================================================
    # Block1: dispatch_equip_activation_seq_by_type80 body
    # =====================================================================
    print("\n--- Block1: %s @ 0x%08x ---" % (BLOCK1_NAME, BLOCK1_ENTRY))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI))
        print("[dry] disasm @ 0x%08x" % BLOCK1_ENTRY)
        for p in BLOCK1_POOL:
            print("[dry] createDWord @ 0x%08x" % p)
        print("[dry] createFunction + setName '%s'" % BLOCK1_NAME)
        print("[dry] setPlateComment (%d chars)" % len(BLOCK1_PLATE))
    else:
        _clear_and_set_thumb(BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        _disasm_at(BLOCK1_ENTRY, BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        for p in BLOCK1_POOL:
            _create_dword(p)
        _create_fn_or_label(BLOCK1_ENTRY, BLOCK1_NAME)
        _set_plate(BLOCK1_ENTRY, BLOCK1_PLATE)
        n = _count_instrs(BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        print("[ok ] Block1: %d instructions" % n)

    # =====================================================================
    # Block2: 6 sub-fns (ROM_INCBIN 0x59588 0x164)
    # =====================================================================
    print("\n--- Block2: sub-fns 0x%08x..0x%08x ---" % (BLOCK2_LO, BLOCK2_HI))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK2_LO, BLOCK2_HI))
        for ep, lbl, plate in BLOCK2_ENTRIES:
            print("[dry] disasm @ 0x%08x label=%s" % (ep, lbl))
            print("[dry] setPlateComment @ 0x%08x (%d chars)" % (ep, len(plate)))
    else:
        _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
        ok_count = 0
        for ep_int, ep_label, ep_plate in BLOCK2_ENTRIES:
            if _disasm_at(ep_int, BLOCK2_LO, BLOCK2_HI):
                ok_count += 1
            ep_addr = _addr(ep_int)
            try:
                sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
                print("[ok ] label '%s' @ 0x%08x" % (ep_label, ep_int))
            except Exception as le:
                print("[warn] label @ 0x%08x: %s" % (ep_int, le))
            fn = fm.getFunctionAt(ep_addr)
            if fn is None:
                fn = createFunction(ep_addr, ep_label)
                if fn is not None:
                    print("[FN ] created: %s @ 0x%08x" % (ep_label, ep_int))
                else:
                    print("[FN ] label-only: %s @ 0x%08x" % (ep_label, ep_int))
            else:
                fn.setName(ep_label, SourceType.USER_DEFINED)
                print("[FN ] renamed: %s @ 0x%08x" % (ep_label, ep_int))
            _set_plate(ep_int, ep_plate)
        n_total = _count_instrs(BLOCK2_LO, BLOCK2_HI)
        print("[ok ] Block2: %d/%d stubs disasmd, %d instructions total" % (
            ok_count, len(BLOCK2_ENTRIES), n_total))

    # =====================================================================
    # Block3: equip_lp_spell_zone_case_dispatch
    # =====================================================================
    print("\n--- Block3: %s @ 0x%08x ---" % (BLOCK3_NAME, BLOCK3_ENTRY))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK3_CLEAR_LO, BLOCK3_CLEAR_HI))
        print("[dry] disasm @ 0x%08x" % BLOCK3_ENTRY)
        for p in BLOCK3_POOL:
            print("[dry] createDWord @ 0x%08x" % p)
        print("[dry] createFunction + setName '%s'" % BLOCK3_NAME)
        print("[dry] setPlateComment (%d chars)" % len(BLOCK3_PLATE))
    else:
        _clear_and_set_thumb(BLOCK3_CLEAR_LO, BLOCK3_CLEAR_HI)
        _disasm_at(BLOCK3_ENTRY, BLOCK3_CLEAR_LO, BLOCK3_CLEAR_HI)
        for p in BLOCK3_POOL:
            _create_dword(p)
        _create_fn_or_label(BLOCK3_ENTRY, BLOCK3_NAME)
        _set_plate(BLOCK3_ENTRY, BLOCK3_PLATE)
        n = _count_instrs(BLOCK3_CLEAR_LO, BLOCK3_CLEAR_HI)
        print("[ok ] Block3: %d instructions" % n)

    # =====================================================================
    # Block4: 5 sub-fns (ROM_INCBIN 0x59d14 0xcc)
    # =====================================================================
    print("\n--- Block4: sub-fns 0x%08x..0x%08x ---" % (BLOCK4_LO, BLOCK4_HI))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK4_LO, BLOCK4_HI))
        for ep, lbl, plate in BLOCK4_ENTRIES:
            print("[dry] disasm @ 0x%08x label=%s" % (ep, lbl))
            print("[dry] setPlateComment @ 0x%08x (%d chars)" % (ep, len(plate)))
    else:
        _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)
        ok_count = 0
        for ep_int, ep_label, ep_plate in BLOCK4_ENTRIES:
            if _disasm_at(ep_int, BLOCK4_LO, BLOCK4_HI):
                ok_count += 1
            ep_addr = _addr(ep_int)
            try:
                sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
                print("[ok ] label '%s' @ 0x%08x" % (ep_label, ep_int))
            except Exception as le:
                print("[warn] label @ 0x%08x: %s" % (ep_int, le))
            fn = fm.getFunctionAt(ep_addr)
            if fn is None:
                fn = createFunction(ep_addr, ep_label)
                if fn is not None:
                    print("[FN ] created: %s @ 0x%08x" % (ep_label, ep_int))
                else:
                    print("[FN ] label-only: %s @ 0x%08x" % (ep_label, ep_int))
            else:
                fn.setName(ep_label, SourceType.USER_DEFINED)
                print("[FN ] renamed: %s @ 0x%08x" % (ep_label, ep_int))
            _set_plate(ep_int, ep_plate)
        n_total = _count_instrs(BLOCK4_LO, BLOCK4_HI)
        print("[ok ] Block4: %d/%d stubs disasmd, %d instructions total" % (
            ok_count, len(BLOCK4_ENTRIES), n_total))

    print("\n=== DisassembleF06Seg8Blocks DONE (DRY=%s) ===" % DRY)


main()
