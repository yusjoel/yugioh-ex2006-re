# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg9Blocks.py -- f10 Seg-9 R4 disasm (2 ROM_INCBIN blocks)
#
#   BLK1: fn_eligible_book_of_life @ 0x0808420e..0x08084233 (0x26 bytes)
#     - 0x0808420e..0x0808420f: 2B zero-pad alignment (.zero 2, not fn code)
#     - fn_eligible THUMB code starts at 0x08084210 (opcode 0xb570 = push {r4,r5,r6,lr})
#     - THUMB+1 = 0x08084211; dispatch table at 0x09e410b8 stores 0x08084211 (confirmed)
#     - dispatch table entry 0x09e410a4: [+0x00]=0x1536 (BOOK_OF_LIFE_CID), [+0x14]=0x08084211
#     Literal pools in BLK1 (ROM-verified by reviewer):
#       0x0808422c = 0x0201b290 (gDuelPhaseFlags) -- createDWord + EQ
#       0x08084230 = 0x08084234 (BLK2 JT base raw ptr) -- createDWord + EOL only
#     NOTE: 0x08084232 = .hword 0x4687 (MOV PC,r0) -- THUMB opcode, NOT a pool word
#           DO NOT createDWord at 0x08084232/0x08084233
#
#   BLK2: 6 sub-stubs @ 0x0808424c..0x08084317 (0xcc bytes)
#     JT at 0x08084234..0x0808424b (6x.word) already decoded in asm as .word entries
#     Sub-stub entries (JT values):
#       state 0: 0x0808424c (DAT_0808424c = BLK2 start, renamed to book_of_life_eligible_dispatch_state0)
#       state 1: 0x0808429a
#       state 2: 0x080842cc (shared with state 5)
#       state 3: 0x080842ac
#       state 4: 0x080842ba
#       state 5: 0x080842cc (same as state 2)
#     Unique entry points: 0x0808424c, 0x0808429a, 0x080842ac, 0x080842ba, 0x080842cc
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: Per methodology: clearListing entire range before setTMode; per-stub DisassembleCommand.
# NOTE: Do NOT createDWord at 0x08084232 (= 0x4687 MOV PC,r0 THUMB opcode in fn body).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
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


def _clear_and_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    print("[tmode] set THUMB 0x%08x..0x%08x" % (lo_int, hi_int))


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def _create_dword(addr_int, label=None, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _create_label(addr_int, label, eol=None):
    a = _addr(addr_int)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[label ok] 0x%08x %s" % (addr_int, label))


def _create_function(addr_int, fn_name, plate_text=None):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        fn.setName(fn_name, SourceType.USER_DEFINED)
        print("[fn rename] 0x%08x -> %s" % (addr_int, fn_name))
    else:
        fn = createFunction(a, fn_name)
        if fn is not None:
            print("[fn create] 0x%08x %s" % (addr_int, fn_name))
        else:
            print("[warn] createFunction 0x%08x %s failed" % (addr_int, fn_name))
    if plate_text and fn is not None:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            print("[plate ok] 0x%08x" % addr_int)


def _apply_eq_pool(addr_int, value, eq_name, slot_label, eol=None):
    """Apply equate + label + EOL to a pool dword after createDWord."""
    a = _addr(addr_int)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ pool] 0x%08x  %s -> %s" % (addr_int, eq_name, slot_label))


def _check_mem_word(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        match = (actual == (expected & 0xFFFFFFFF))
        status = 'OK' if match else 'MISMATCH'
        print("[check] 0x%08x: got=0x%08x exp=0x%08x %s" % (
            addr_int, actual, expected & 0xFFFFFFFF, status))
        return match
    except Exception as e:
        print("[check err] 0x%08x: %s" % (addr_int, e))
        return False


def main():
    print("=== DisassembleF10Seg9Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] BLK1: fn_eligible_book_of_life stub (0x08084210..0x08084233)")
        print("[DRY]   2B zero-pad at 0x0808420e (not fn code); fn starts 0x08084210")
        print("[DRY]   clearListing + setTMode 0x08084210..0x08084233")
        print("[DRY]   disasm_stub 0x08084210 (PUSH 0xb570 confirmed THUMB fn entry)")
        print("[DRY]   createDWord 0x0808422c=gDuelPhaseFlags(0x0201b290) pool word")
        print("[DRY]   createDWord 0x08084230=0x08084234 raw JT base ptr (EOL only)")
        print("[DRY]   DO NOT createDWord 0x08084232 (=0x4687 MOV PC,r0 THUMB opcode)")
        print("[DRY]   createFunction fn_eligible_book_of_life @ 0x08084210 + plate")
        print("[DRY] BLK2: 6 sub-stubs (0x0808424c..0x08084317)")
        print("[DRY]   clearListing + setTMode 0x0808424c..0x08084317")
        print("[DRY]   disasm_stub x5: 0x424c/0x429a/0x42ac/0x42ba/0x42cc")
        print("[DRY]   createFunction x5 sub-stubs + plates")
        return

    # -----------------------------------------------------------------------
    # BLK1: fn_eligible_book_of_life
    # Range: [0x0808420e, 0x08084234)
    #   0x0808420e..0x0808420f = 2B zero-pad (alignment between prior fn and THUMB fn)
    #   fn_eligible code: 0x08084210..0x08084231 (approx)
    #   literal pool:
    #     0x0808422c = 0x0201b290 (gDuelPhaseFlags)
    #     0x08084230 = 0x08084234 (JT base)
    #   0x08084232..0x08084233 = .hword 0x4687 (THUMB MOV PC,r0 in fn body) -- NOT pool word
    # JT at 0x08084234..0x0808424b already decoded as .word entries -- NO action needed
    # -----------------------------------------------------------------------
    print("--- BLK1: fn_eligible_book_of_life ---")

    # Verify key bytes (little-endian 32-bit reads)
    # 0x0808420e: [0x0000] zero-pad halfword + [0xb570] PUSH{r4,r5,r6,lr} halfword = 0xb5700000
    _check_mem_word(0x0808420e, 0xb5700000)  # 2B zero-pad + PUSH opcode as 32-bit word
    _check_mem_word(0x0808422c, 0x0201b290)  # gDuelPhaseFlags pool word
    _check_mem_word(0x08084230, 0x08084234)  # JT base ptr

    # clearListing + setTMode from fn start (skip zero-pad at 0x420e)
    _clear_and_tmode(0x08084210, 0x08084233)
    _disasm_stub(0x08084210)  # fn entry: push {r4,r5,r6,lr} = 0xb570

    # Literal pool createDWords (after disasm so they don't get disassembled as code)
    _create_dword(0x0808422c, 'fn_eligible_bol_phase_flags_2c',
                  'gDuelPhaseFlags=0x0201b290: duel phase state base (pool word)')
    # Apply equate to pool word
    _apply_eq_pool(0x0808422c, 0x0201b290, 'gDuelPhaseFlags',
                   'duel_phase_flags_0808422c',
                   'gDuelPhaseFlags (pool word in fn_eligible_book_of_life)')

    _create_dword(0x08084230, 'fn_eligible_bol_jt_ptr_30',
                  'JT base: book_of_life_eligible state dispatch table start (0x08084234)')
    # NOTE: 0x08084232 = .hword 0x4687 MOV PC,r0 -- is THUMB code opcode, NOT a pool word
    # Ghidra disasm should have handled this as code. No createDWord here.

    _create_function(
        0x08084210,
        'fn_eligible_book_of_life',
        "@ fn_eligible stub for BOOK_OF_LIFE_CID(0x1536).\n"
        "@ Received via FS handler dispatch table at 0x09e410a4:\n"
        "@   [+0x00]=0x1536 (BOOK_OF_LIFE_CID=Book of Life), [+0x14]=0x08084211 (fn_eligible+1).\n"
        "@ Reads state from [gDuelPhaseFlags+0x4b0], loads JT base from literal pool at 0x08084230,\n"
        "@ dispatches to 5 unique sub-stubs via JT at 0x08084234 (6 entries, states 2 and 5 share 0x080842cc).\n"
        "@ JT entries:\n"
        "@   state 0: 0x0808424c, state 1: 0x0808429a, state 2: 0x080842cc,\n"
        "@   state 3: 0x080842ac, state 4: 0x080842ba, state 5: 0x080842cc (shared).\n"
        "@ 2B zero-pad at 0x0808420e (alignment between prior fn and this fn entry)."
    )

    # -----------------------------------------------------------------------
    # BLK2: 6 Book of Life fn_eligible dispatch sub-stubs
    # Range: [0x0808424c, 0x08084318)
    # JT at 0x08084234..0x0808424b already decoded as 6x.word in asm -- NO action
    # 5 unique entry points to disasm (states 2+5 share 0x080842cc)
    # -----------------------------------------------------------------------
    print("--- BLK2: 6 Book of Life fn_eligible sub-stubs ---")

    # Verify BLK2 is within expected range (spot check JT already decoded)
    print("[info] BLK2 sub-stubs: 0x424c/0x429a/0x42ac/0x42ba/0x42cc; JT at 0x08084234 already decoded")

    _clear_and_tmode(0x0808424c, 0x08084317)

    # Per-stub DisassembleCommand (one per unique JT entry)
    _disasm_stub(0x0808424c)  # state 0 (book_of_life_eligible_dispatch_state0)
    _disasm_stub(0x0808429a)  # state 1
    _disasm_stub(0x080842ac)  # state 3
    _disasm_stub(0x080842ba)  # state 4
    _disasm_stub(0x080842cc)  # state 2 + state 5 (shared)

    # Create functions for each unique sub-stub
    _create_function(
        0x0808424c,
        'book_of_life_eligible_state0',
        "@ Book of Life fn_eligible dispatch sub-stub: state 0 (JT[0]=0x0808424c).\n"
        "@ Entry from fn_eligible_book_of_life JT dispatch table (0x08084234).\n"
        "@ Handles state 0 of Book of Life equip eligibility check."
    )
    _create_function(
        0x0808429a,
        'book_of_life_eligible_state1',
        "@ Book of Life fn_eligible dispatch sub-stub: state 1 (JT[1]=0x0808429a).\n"
        "@ Entry from fn_eligible_book_of_life JT dispatch table (0x08084234).\n"
        "@ Handles state 1 of Book of Life equip eligibility check."
    )
    _create_function(
        0x080842ac,
        'book_of_life_eligible_state3',
        "@ Book of Life fn_eligible dispatch sub-stub: state 3 (JT[3]=0x080842ac).\n"
        "@ Entry from fn_eligible_book_of_life JT dispatch table (0x08084234).\n"
        "@ Handles state 3 of Book of Life equip eligibility check."
    )
    _create_function(
        0x080842ba,
        'book_of_life_eligible_state4',
        "@ Book of Life fn_eligible dispatch sub-stub: state 4 (JT[4]=0x080842ba).\n"
        "@ Entry from fn_eligible_book_of_life JT dispatch table (0x08084234).\n"
        "@ Handles state 4 of Book of Life equip eligibility check."
    )
    _create_function(
        0x080842cc,
        'book_of_life_eligible_state2_5',
        "@ Book of Life fn_eligible dispatch sub-stub: states 2 and 5 shared (JT[2]=JT[5]=0x080842cc).\n"
        "@ Entry from fn_eligible_book_of_life JT dispatch table (0x08084234).\n"
        "@ Shared exit/handling stub for states 2 and 5 of Book of Life equip eligibility."
    )

    print("")
    print("=== DisassembleF10Seg9Blocks DONE ===")
    print("=== BLK1: fn_eligible_book_of_life @ 0x08084210 (2 pool DWords) ===")
    print("=== BLK2: 5 unique sub-stubs @ 0x424c/0x429a/0x42ac/0x42ba/0x42cc ===")


main()
