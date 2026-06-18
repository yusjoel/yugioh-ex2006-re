# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg1Blocks.py -- F09 Seg-1 R4 disasm
#   6 ROM_INCBIN blocks -> THUMB code:
#   Block1 (0x0806f008..0x0806f03b, 0x34B): fn_eligible stub for Creature Swap (CID=0x142a)
#   Block2 (0x0806f054..0x0806f1c7, 0x174B): raw dispatch sub-stubs (6 entry points)
#   Block3 (0x0806f85c..0x0806f993, 0x138B): fn_eligible stub for Destiny Board (CID=0x1468)
#   Block4 (0x0806fa08..0x0806fb87, 0x180B): raw dispatch sub-stubs (10 entry points)
#   Block5 (0x0806fdec..0x0806fe13, 0x28B): fn_eligible stub for Cathedral of Nobles (CID=0x146f)
#   Block6 (0x0806fe88..0x0806ff4f, 0xc8B): raw dispatch sub-stubs (8 entry points)
#   + 3 dispatch table labels + dispatch table structuring
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_194628-pre-F09Seg1

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
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


def _disasm_block(lo, hi, stubs, label_map, eol_map):
    """
    Clear listing for [lo..hi], set TMode=THUMB, then disassemble each stub address individually.
    stubs: list of int addresses to disassemble
    label_map: dict{addr: label_str}
    eol_map: dict{addr: eol_str}
    """
    a_lo = _addr(lo)
    a_hi = _addr(hi)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] would clearListing(0x%08x..0x%08x) + setTMode + disasm %d stubs" % (
            lo, hi, len(stubs)))
        for s in stubs:
            lbl = label_map.get(s, '')
            print("[dry]   stub 0x%08x  label=%s" % (s, lbl))
        return

    # 1) Clear entire range
    try:
        clearListing(a_lo, a_hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo, hi, e))

    # 2) Set TMode=1 (THUMB) for entire range
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)

    # 3) Disassemble each stub individually
    for stub_addr in stubs:
        sa = _addr(stub_addr)
        cmd = DisassembleCommand(sa, AddressSet(sa, sa), True)
        if not cmd.applyTo(currentProgram):
            print("[warn] disasm 0x%08x: %s" % (stub_addr, cmd.getStatusMsg()))
        else:
            print("[DIS] disasm 0x%08x ok" % stub_addr)

    # 4) Apply labels and EOL comments
    for stub_addr in stubs:
        sa = _addr(stub_addr)
        lbl = label_map.get(stub_addr)
        if lbl:
            existing = [s.getName() for s in sym_tbl.getSymbols(sa)]
            if lbl not in existing:
                sym_tbl.createLabel(sa, lbl, SourceType.USER_DEFINED)
            print("[LBL] 0x%08x -> %s" % (stub_addr, lbl))
        eol = eol_map.get(stub_addr)
        if eol:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII EOL @ 0x%08x -- skip" % stub_addr)
            else:
                cu = listing.getCodeUnitAt(sa)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[DIS] block 0x%08x..0x%08x done (%d stubs)" % (lo, hi, len(stubs)))


def _label_dispatch_table(tbl_addr, tbl_label, n_entries):
    """Label a dispatch table as tbl_label at tbl_addr."""
    if DRY:
        print("[dry] dispatch table 0x%08x -> %s (%d entries)" % (tbl_addr, tbl_label, n_entries))
        return
    a = _addr(tbl_addr)
    sym_tbl = currentProgram.getSymbolTable()
    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if tbl_label not in existing:
        sym_tbl.createLabel(a, tbl_label, SourceType.USER_DEFINED)
    print("[TBL] 0x%08x -> %s (%d entries)" % (tbl_addr, tbl_label, n_entries))


def main():
    print("=== DisassembleF09Seg1Blocks (DRY=%s) ===" % DRY)

    # -------------------------------------------------------------------------
    # Block1: 0x0806f008..0x0806f03b (0x34B)
    #   fn_eligible stub: Creature Swap (CID=0x142a)
    #   FS table THUMB+1 ref @0x1e40958
    # -------------------------------------------------------------------------
    print("\n--- Block1: 0x0806f008..0x0806f03b (fn_eligible Creature Swap) ---")
    _disasm_block(
        lo=0x0806f008, hi=0x0806f03b,
        stubs=[0x0806f008],
        label_map={0x0806f008: 'eligible_creature_swap_f008'},
        eol_map={0x0806f008:
            'fn_eligible stub: Creature Swap (CID=0x142a); FS table THUMB+1 ref @0x1e40958'}
    )

    # Dispatch table at 0x0806f03c (6 entries, raw code ptrs to Block2 stubs)
    _label_dispatch_table(0x0806f03c, 'equip_disp_table_f03c', 6)

    # -------------------------------------------------------------------------
    # Block2: 0x0806f054..0x0806f1c7 (0x174B)
    #   Raw dispatch sub-stubs (6 entry points)
    #   Reached via dispatch table at 0x0806f03c via MOV PC,r0
    # -------------------------------------------------------------------------
    print("\n--- Block2: 0x0806f054..0x0806f1c7 (dispatch sub-stubs x6) ---")
    _disasm_block(
        lo=0x0806f054, hi=0x0806f1c7,
        stubs=[0x0806f054, 0x0806f066, 0x0806f078, 0x0806f0ac, 0x0806f0cc, 0x0806f188],
        label_map={
            0x0806f054: 'equip_disp_sub_f054',
            0x0806f066: 'equip_disp_sub_f066',
            0x0806f078: 'equip_disp_sub_f078',
            0x0806f0ac: 'equip_disp_sub_f0ac',
            0x0806f0cc: 'equip_disp_sub_f0cc',
            0x0806f188: 'equip_disp_sub_f188',
        },
        eol_map={}
    )

    # -------------------------------------------------------------------------
    # Block3: 0x0806f85c..0x0806f993 (0x138B)
    #   fn_eligible stub: Destiny Board (CID=0x1468)
    #   2x FS table THUMB+1 ref @0x1e40a90+0x1e43a30
    # -------------------------------------------------------------------------
    print("\n--- Block3: 0x0806f85c..0x0806f993 (fn_eligible Destiny Board) ---")
    _disasm_block(
        lo=0x0806f85c, hi=0x0806f993,
        stubs=[0x0806f85c],
        label_map={0x0806f85c: 'eligible_destiny_board_f85c'},
        eol_map={0x0806f85c:
            'fn_eligible stub: Destiny Board (CID=0x1468); 2x FS table THUMB+1 ref @0x1e40a90+0x1e43a30'}
    )

    # Dispatch table at 0x0806f994 (29 entries)
    _label_dispatch_table(0x0806f994, 'equip_lp_disp_table_f994', 29)

    # -------------------------------------------------------------------------
    # Block4: 0x0806fa08..0x0806fb87 (0x180B)
    #   Raw dispatch sub-stubs (10 entry points)
    # -------------------------------------------------------------------------
    print("\n--- Block4: 0x0806fa08..0x0806fb87 (dispatch sub-stubs x10) ---")
    _disasm_block(
        lo=0x0806fa08, hi=0x0806fb87,
        stubs=[0x0806fa08, 0x0806fa4c, 0x0806fa5e, 0x0806fa74,
               0x0806fb14, 0x0806fb4c, 0x0806fb58, 0x0806fb64,
               0x0806fb70, 0x0806fb76],
        label_map={
            0x0806fa08: 'equip_lp_sub_fa08',
            0x0806fa4c: 'equip_lp_sub_fa4c',
            0x0806fa5e: 'equip_lp_sub_fa5e',
            0x0806fa74: 'equip_lp_sub_fa74',
            0x0806fb14: 'equip_lp_sub_fb14',
            0x0806fb4c: 'equip_lp_sub_fb4c',
            0x0806fb58: 'equip_lp_sub_fb58',
            0x0806fb64: 'equip_lp_sub_fb64',
            0x0806fb70: 'equip_lp_sub_fb70',
            0x0806fb76: 'equip_lp_sub_fb76',
        },
        eol_map={}
    )

    # -------------------------------------------------------------------------
    # Block5: 0x0806fdec..0x0806fe13 (0x28B)
    #   fn_eligible stub: Cathedral of Nobles (CID=0x146f)
    #   FS table THUMB+1 ref @0x1e46610; false-positive @0x3d3eb6 (compressed data)
    # -------------------------------------------------------------------------
    print("\n--- Block5: 0x0806fdec..0x0806fe13 (fn_eligible Cathedral of Nobles) ---")
    _disasm_block(
        lo=0x0806fdec, hi=0x0806fe13,
        stubs=[0x0806fdec],
        label_map={0x0806fdec: 'eligible_cathedral_of_nobles_fdec'},
        eol_map={0x0806fdec:
            'fn_eligible stub: Cathedral of Nobles (CID=0x146f); 2x FS table THUMB+1 ref @0x1e46610; false-positive at 0x3d3eb6 (compressed data)'}
    )

    # Dispatch table at 0x0806fe14 (29 entries)
    _label_dispatch_table(0x0806fe14, 'equip_chain_act_disp_table_fe14', 29)

    # -------------------------------------------------------------------------
    # Block6: 0x0806fe88..0x0806ff4f (0xc8B)
    #   Raw dispatch sub-stubs (8 entry points)
    # -------------------------------------------------------------------------
    print("\n--- Block6: 0x0806fe88..0x0806ff4f (dispatch sub-stubs x8) ---")
    _disasm_block(
        lo=0x0806fe88, hi=0x0806ff4f,
        stubs=[0x0806fe88, 0x0806fedc, 0x0806fef0, 0x0806ff0a,
               0x0806ff1a, 0x0806ff2c, 0x0806ff3c, 0x0806ff46],
        label_map={
            0x0806fe88: 'equip_chain_act_sub_fe88',
            0x0806fedc: 'equip_chain_act_sub_fedc',
            0x0806fef0: 'equip_chain_act_sub_fef0',
            0x0806ff0a: 'equip_chain_act_sub_ff0a',
            0x0806ff1a: 'equip_chain_act_sub_ff1a',
            0x0806ff2c: 'equip_chain_act_sub_ff2c',
            0x0806ff3c: 'equip_chain_act_sub_ff3c',
            0x0806ff46: 'equip_chain_act_sub_ff46',
        },
        eol_map={}
    )

    print("\n=== DisassembleF09Seg1Blocks DONE ===")
    print("  6 blocks disassembled + 3 dispatch tables labeled")


main()
