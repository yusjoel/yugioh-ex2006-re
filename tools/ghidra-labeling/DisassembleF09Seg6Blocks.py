# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg6Blocks.py -- p5 file09 Seg-6 R4 disasm (blocks B1 + B2)
#
# Block1: fn_eligible_dimension_jar @ 0x08074854 (ROM_INCBIN 0x74852/0x4a)
#   - 2B align pad at 0x08074852 (00 00)
#   - fn body: 0x08074854..0x0807489b
#   - THUMB+1 ref: 0x08074855 from FS table at GBA:0x09e442a0 (CID=0x15dd Dimension Jar)
#   - Literal pool: 5 DWords at 0x0807488c/90/94/98/9c
#       0x0807488c: 0x0201c4e0 (gP1LifePoints)
#       0x08074890: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#       0x08074894: 0x0201b290 (gDuelPhaseFlags)
#       0x08074898: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#       0x0807489c: 0x080748a0 (equip_zone_dispatch_table_48a0 ptr)
#   - Pool word at 0x7489c is already in asm as .word 0x080748a0 (NOT inside Block1 incbin).
#     Block1 incbin ends at 0x7489b. The .word at 0x7489c is outside the incbin range.
#     clearListing range: 0x08074852..0x0807489b (inclusive, 0x4a bytes)
#   - createFunction @ 0x08074854 named fn_eligible_dimension_jar
#
# Block2: equip_zone_sub_stubs @ 0x08074914 (ROM_INCBIN 0x74914/0xcc)
#   - Range: 0x08074914..0x080749df (0xcc bytes)
#   - 6 sub-stubs entered via raw ptr from dispatch table at 0x080748a0:
#       equip_zone_sub_914 @ 0x08074914 -- clears EQUIP_PHASE_FRAME_OFF, calls increment_lp_bar
#       equip_zone_sub_920 @ 0x08074920 -- check_field_spell_neo_daedalus_group_placeable path
#       equip_zone_sub_948 @ 0x08074948 -- reads LP_CARD_TRACK_BASE_OFF; cmp zone count path
#       equip_zone_sub_964 @ 0x08074964 -- loop over zone hits with PLAYER_BLOCK_STRIDE math
#       equip_zone_sub_9b8 @ 0x080749b8 -- increment zone field at EQUIP_PHASE_FRAME_OFF+4
#       equip_zone_epilogue_9d4 @ 0x080749d4 -- movs r0,#0; pop...bx r1 (default/noop handler)
#   - Literal pool words in Block2 (force-DWord required):
#       0x08074944: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)     -- in sub_920 pool
#       0x08074960: 0x00001da8 (LP_CARD_TRACK_BASE_OFF)    -- in sub_948 pool
#       0x080749b0: 0x00001da8 (LP_CARD_TRACK_BASE_OFF dup)-- in sub_964 pool
#       0x080749b4: 0x00000868 (PLAYER_BLOCK_STRIDE)       -- in sub_964 pool
#       0x080749cc: 0x000004a4 (EQUIP_PHASE_FRAME_OFF dup) -- in sub_9b8 pool
#   - NOTE: 0x080749ac and 0x080749c8 contain branch displacements (0x0000e013/0x0000e005)
#     embedded in code -- do NOT force-DWord these; let disasm handle them.
#   - No createFunction for sub-stubs (raw ptr dispatch, not bl-called)
#
# Pattern: clearListing -> setTMode -> per-stub DisassembleCommand -> force-DWord pool words
# Per-stub labeling adds USER_DEFINED labels at each sub-stub entry point.
#
# NOTE: All labels are pure ASCII. No CJK in EOL/plate.

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

# ---------------------------------------------------------------------------
# Block1 ranges
# ---------------------------------------------------------------------------
B1_PAD  = 0x08074852   # 2B align pad (0x0000), NOT disasmed
B1_LO   = 0x08074854   # fn body start
B1_HI   = 0x0807489b   # end of incbin range (0x4a bytes from 0x74852)
                        # pool at 0x0807488c..0x0807489f (5 DWords = 0x14 bytes)
                        # fn body code ends before pool; pool at 0x488c..0x489f but
                        # incbin is 0x4a bytes = 0x74852..0x7489b -> pool at 0x489c is OUTSIDE
B1_POOL_DWORDS = [0x0807488c, 0x08074890, 0x08074894, 0x08074898]
# Note: 0x0807489c is OUTSIDE incbin (it's the .word 0x080748a0 in asm line 13174)
#       clearListing covers 0x08074852..0x0807489b only

# ---------------------------------------------------------------------------
# Block2 ranges
# ---------------------------------------------------------------------------
B2_LO = 0x08074914
B2_HI = 0x080749df   # inclusive (0xcc bytes from 0x74914)

# Sub-stub definitions (start_addr, size_bytes, label)
B2_STUBS = [
    (0x08074914, 0x0c, 'equip_zone_sub_914'),     # 12B: clears phase frame off, calls incr_lp_bar
    (0x08074920, 0x28, 'equip_zone_sub_920'),     # 40B: check_field_spell_neo_daedalus path
    (0x08074948, 0x1c, 'equip_zone_sub_948'),     # 28B: reads LP_CARD_TRACK_BASE_OFF; zone cmp
    (0x08074964, 0x54, 'equip_zone_sub_964'),     # 84B: loop over zone hits with stride math
    (0x080749b8, 0x1c, 'equip_zone_sub_9b8'),     # 28B: increment zone field at phase_frame+4
    (0x080749d4, 0x0c, 'equip_zone_epilogue_9d4'), # 12B: movs r0,#0; pop...bx epilogue
]

# Pool words in Block2 (force-DWord required):
B2_POOL_DWORDS = [0x08074944, 0x08074960, 0x080749b0, 0x080749b4, 0x080749cc]
# NOTE: 0x080749ac (0xe013) and 0x080749c8 (0xe005) are branch displacements in code -- skip

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")

def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))

def _disasm_stub(sa, size, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(sa + size - 1)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x (%dB)" % (label, sa, size))

def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def _add_label(addr_int, label):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if label not in names:
        sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
        print("[ok ] label 0x%08x -> %s" % (addr_int, label))
    else:
        print("[ok ] label 0x%08x -> %s (already exists)" % (addr_int, label))

def _create_function(addr_int, name):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        if fn.getName() != name:
            fn.setName(name, SourceType.USER_DEFINED)
            print("[ok ] function renamed 0x%08x -> %s" % (addr_int, name))
        else:
            print("[ok ] function 0x%08x already named %s" % (addr_int, name))
    else:
        try:
            fm.createFunction(name, a, AddressSet(_addr(addr_int), _addr(B1_HI)),
                              SourceType.USER_DEFINED)
            print("[ok ] createFunction %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr_int, e))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg6Blocks (DRY=%s) ===" % DRY)
    print("  B1: fn_eligible_dimension_jar @ 0x%08x (ROM_INCBIN 0x74852/0x4a)" % B1_LO)
    print("  B2: equip_zone_sub_stubs @ 0x%08x (ROM_INCBIN 0x74914/0xcc)" % B2_LO)

    if DRY:
        print("[dry] B1: clearListing(0x08074852..0x0807489b) + setTMode + disasm(0x08074854..0x0807488b)")
        print("[dry] B1: force_dword x4 (pool 0x488c/90/94/98)")
        print("[dry] B1: createFunction fn_eligible_dimension_jar @ 0x08074854")
        print("[dry] B2: clearListing(0x08074914..0x080749df) + setTMode")
        print("[dry] B2: per-stub DisassembleCommand x6 + force_dword x5 + labels x6")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block1: fn_eligible_dimension_jar @ 0x08074854
    # -----------------------------------------------------------------------
    print("\n--- Block1: fn_eligible_dimension_jar @ 0x08074854 ---")
    print("    CID=0x15dd Dimension Jar; FS THUMB+1 @ GBA:0x09e442a0")
    print("    clearListing range: 0x%08x..0x%08x (0x4a B incl 2B pad)" % (B1_PAD, B1_HI))

    # clearListing whole incbin range (including pad bytes)
    _clear_listing(B1_PAD, B1_HI)
    # setTMode for fn body (not the pad)
    _set_tmode(B1_LO, B1_HI)

    # Disassemble fn body up to before literal pool
    # Pool starts at 0x0807488c; fn code ends at 0x0807488b
    b1_fn_code_hi = 0x0807488b
    b1_lo_a = _addr(B1_LO)
    b1_code_hi_a = _addr(b1_fn_code_hi)
    cmd = DisassembleCommand(b1_lo_a, AddressSet(b1_lo_a, b1_code_hi_a), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm B1 fn body: %s" % cmd.getStatusMsg())
    else:
        print("[ok ] disasm B1 fn_eligible_dimension_jar fn body (0x08074854..0x0807488b)")

    # Force DWords for literal pool (4 DWords: 0x488c/90/94/98)
    print("  Force-DWord pool: 0x488c/90/94/98")
    for dw_addr in B1_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction
    _create_function(B1_LO, 'fn_eligible_dimension_jar')

    # Add USER_DEFINED label at fn start (idempotent)
    _add_label(B1_LO, 'fn_eligible_dimension_jar')

    # -----------------------------------------------------------------------
    # Block2: equip_zone_sub_stubs @ 0x08074914
    # -----------------------------------------------------------------------
    print("\n--- Block2: equip_zone_sub_stubs @ 0x08074914 ---")
    print("    ROM_INCBIN 0x74914/0xcc; 6 sub-stubs via raw ptr dispatch from table_48a0")

    # clearListing entire Block2 range
    _clear_listing(B2_LO, B2_HI)
    # setTMode for whole range
    _set_tmode(B2_LO, B2_HI)

    # Force DWords for literal pool words BEFORE disasm (to avoid coverage collisions)
    # Must force before disasm so that pool words are not absorbed into code
    print("  Force-DWord pool words in Block2: 0x944/960/9b0/9b4/9cc")
    for dw_addr in B2_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    for sa, size, label in B2_STUBS:
        _disasm_stub(sa, size, label)
        _add_label(sa, label)

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B1_LO, B1_HI, "B1"),
        (B2_LO, B2_HI, "B2"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg6Blocks DONE ===")
    print("  B1: fn_eligible_dimension_jar @ 0x08074854 (0x4a B incbin)")
    print("  B2: 6 sub-stubs @ 0x08074914 (0xcc B incbin)")
    print("  Total new functions: 1 (fn_eligible_dimension_jar)")
    print("  Total sub-stub labels: 6")


main()
