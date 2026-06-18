# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg3Disasm.py -- F09 Seg-3 R4 disasm (2 blocks)
#
# Block 1: ROM_INCBIN 0x080716fa size 0x42 (GBA 0x080716fa..0x0807173b)
#   - 0x080716fa/2: 2-byte alignment pad (.zero 0x2)
#   - 0x080716fc: fn_eligible stub for Dragged Down into the Grave (CID=0x14e8)
#     THUMB push {r4,r5,lr} = 0x30b5 at ROM offset 0x716fc
#     FS table THUMB+1 ref @ GBA:0x09e40e98 -> fn=0x080716fc
#   - Literal pool @ 0x0807172c..0x0807173b
#     0x0807172c: 0x0201c4e0 (gP1LifePoints)
#     0x08071730: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#     0x08071734: 0x0201b290 (gDuelPhaseFlags)
#     0x08071738: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#
# Block 2: ROM_INCBIN 0x08071754 size 0x9c (GBA 0x08071754..0x080717ef)
#   5 dispatch sub-stubs, reached via MOV PC,r0 from dispatch_hand_card_sprite_by_effect_slot_zone
#   No push prologue (shared stack frame from block1 fn)
#   Sub-stub entry points (from PTR_DAT_08071740 dispatch table):
#     equip_lp_sub_754 @ 0x08071754  (table[4])
#     equip_lp_sub_77c @ 0x0807177c  (table[3])
#     equip_lp_sub_78a @ 0x0807178a  (table[2])
#     equip_lp_sub_7a4 @ 0x080717a4  (table[1])
#     equip_lp_sub_7c4 @ 0x080717c4  (table[0])
#   Shared epilogue @ ~0x080717e8 (pop {r0}; bx r0 pattern)
#
# Procedure:
#   Block1:
#     1. clearListing 0x080716fc..0x0807173b (fn body + literal pool)
#     2. setTMode THUMB=1 for range
#     3. DisassembleCommand at 0x080716fc (unrestricted flow)
#     4. createLabel eligible_dragged_down_into_grave_16fc + EOL
#     5. createDWord for 4 literal pool words + labels
#   Block2:
#     6. clearListing 0x08071754..0x080717ef (whole block)
#     7. setTMode THUMB=1
#     8. DisassembleCommand at each of 5 entry points (per-stub, not single-pass)
#     9. createLabel for each sub-stub entry + EOL on sub_754 and sub_7c4
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_220254-pre-F09Seg3

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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


def main():
    print("=== RefineF09Seg3Disasm (DRY=%s) ===" % DRY)

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    # =========================================================================
    # BLOCK 1: fn_eligible stub for Dragged Down into the Grave
    # =========================================================================
    print("\n--- BLOCK 1: fn_eligible_dragged_down_into_grave_16fc ---")

    B1_RANGE_START = 0x080716fc  # start of fn body (skip 2-byte pad at 0x080716fa)
    B1_RANGE_END   = 0x0807173b  # end of literal pool (inclusive)
    B1_STUB_ENTRY  = 0x080716fc
    B1_STUB_LABEL  = 'eligible_dragged_down_into_grave_16fc'
    B1_STUB_EOL    = 'fn_eligible stub: Dragged Down into the Grave (CID=0x14e8); FS table THUMB+1 ref @GBA:0x09e40e98'

    # Literal pool at 0x0807172c..0x0807173b
    B1_POOL = [
        (0x0807172c, 0x0201c4e0, 'gp1lp_pool_172c',
         'gP1LifePoints=0x0201c4e0; literal pool eligible_dragged_down_into_grave_16fc'),
        (0x08071730, 0x00001ce8, 'p1lp_block2_pool_1730',
         'P1LP_BLOCK2_OFF_1CE8=0x1ce8; literal pool eligible_dragged_down_into_grave_16fc'),
        (0x08071734, 0x0201b290, 'gduel_phase_pool_1734',
         'gDuelPhaseFlags=0x0201b290; literal pool eligible_dragged_down_into_grave_16fc'),
        (0x08071738, 0x000004a4, 'equip_phase_frame_pool_1738',
         'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool eligible_dragged_down_into_grave_16fc'),
    ]

    a_b1_lo = _addr(B1_RANGE_START)
    a_b1_hi = _addr(B1_RANGE_END)
    a_b1_stub = _addr(B1_STUB_ENTRY)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B1_RANGE_START, B1_RANGE_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x" % B1_STUB_ENTRY)
        print("[dry] createLabel %s @ 0x%08x + EOL" % (B1_STUB_LABEL, B1_STUB_ENTRY))
        for pool_addr, pool_val, pool_label, pool_eol in B1_POOL:
            print("[dry] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
    else:
        # Step 1: clearListing
        print("[B1.1] clearListing 0x%08x..0x%08x" % (B1_RANGE_START, B1_RANGE_END))
        try:
            clearListing(a_b1_lo, a_b1_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B1: %s" % e)

        # Step 2: setTMode THUMB=1
        print("[B1.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_b1_lo, a_b1_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")

        # Step 3: DisassembleCommand (unrestricted)
        print("[B1.3] DisassembleCommand @ 0x%08x" % B1_STUB_ENTRY)
        cmd = DisassembleCommand(a_b1_stub, None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm B1: %s" % cmd.getStatusMsg())

        # Step 4: label + EOL
        print("[B1.4] createLabel %s @ 0x%08x" % (B1_STUB_LABEL, B1_STUB_ENTRY))
        existing = [s.getName() for s in sym_tbl.getSymbols(a_b1_stub)]
        if B1_STUB_LABEL not in existing:
            sym_tbl.createLabel(a_b1_stub, B1_STUB_LABEL, SourceType.USER_DEFINED)
            print("       label created")
        else:
            print("       label already present")

        cu = listing.getCodeUnitAt(a_b1_stub)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, B1_STUB_EOL)
            print("       EOL set")
        else:
            print("[WARN] no CodeUnit at 0x%08x" % B1_STUB_ENTRY)

        # Step 5: literal pool createDWord + labels
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

    # =========================================================================
    # BLOCK 2: 5 dispatch sub-stubs (equip_lp_sub_754..7c4)
    # =========================================================================
    print("\n--- BLOCK 2: equip_lp_sub_754..7c4 (5 sub-stubs) ---")

    B2_RANGE_START = 0x08071754
    B2_RANGE_END   = 0x080717ef  # inclusive

    # Sub-stub entries: (addr, label, eol_or_None)
    B2_STUBS = [
        (0x08071754, 'equip_lp_sub_754',
         'dispatch sub-stub 1 of 5 (table[4]); equip_lp_disp_sub_table[4]'),
        (0x0807177c, 'equip_lp_sub_77c', None),
        (0x0807178a, 'equip_lp_sub_78a', None),
        (0x080717a4, 'equip_lp_sub_7a4', None),
        (0x080717c4, 'equip_lp_sub_7c4',
         'dispatch sub-stub 5 of 5 (table[0]); equip_lp_disp_sub_table[0]; calls enqueue_monster_zone_equip_sprites_and_lp_counters'),
    ]

    a_b2_lo = _addr(B2_RANGE_START)
    a_b2_hi = _addr(B2_RANGE_END)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (stub_addr, stub_label))
    else:
        # Step 6: clearListing entire block 2 range
        print("[B2.6] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        try:
            clearListing(a_b2_lo, a_b2_hi)
            print("       done")
        except Exception as e:
            print("[WARN] clearListing B2: %s" % e)

        # Step 7: setTMode THUMB=1 for entire block 2
        print("[B2.7] setTMode THUMB=1 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        if tmode is not None:
            ctx.setValue(tmode, a_b2_lo, a_b2_hi, BigInteger.ONE)
            print("       TMode set")
        else:
            print("[WARN] TMode register not found")

        # Step 8: DisassembleCommand per stub (not single-pass)
        # Must do per-stub because MOV PC,r0 indirect dispatch targets need individual treatment
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[B2.8] DisassembleCommand @ 0x%08x (%s)" % (stub_addr, stub_label))
            stub_a = _addr(stub_addr)
            cmd2 = DisassembleCommand(stub_a, None, False)
            if cmd2.applyTo(currentProgram):
                print("       disasm ok")
            else:
                print("[WARN] disasm 0x%08x: %s" % (stub_addr, cmd2.getStatusMsg()))

        # Step 9: createLabel + EOL for each sub-stub
        for stub_addr, stub_label, stub_eol in B2_STUBS:
            print("[B2.9] createLabel %s @ 0x%08x" % (stub_label, stub_addr))
            stub_a = _addr(stub_addr)
            existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
            if stub_label not in existing:
                sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
                print("       label created")
            else:
                print("       label already present")

            if stub_eol:
                cu = listing.getCodeUnitAt(stub_a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)
                    print("       EOL set")
                else:
                    print("[WARN] no CodeUnit at 0x%08x after disasm" % stub_addr)

    print("\n=== RefineF09Seg3Disasm DONE ===")
    print("  Block1: eligible_dragged_down_into_grave_16fc @ 0x080716fc")
    print("  Block2: equip_lp_sub_{754,77c,78a,7a4,7c4} @ 0x08071754..0x080717ef")


main()
