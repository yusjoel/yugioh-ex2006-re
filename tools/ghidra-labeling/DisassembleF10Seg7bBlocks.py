# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg7bBlocks.py -- f10 Seg-7b R4 disasm (2 ROM_INCBIN blocks)
#
#   BLK1: route_penguin_soldier_equip_display (0x08082048..0x08082133, ~0xec fn body)
#     THUMB+1 ref: ROM[0x09e43428]=0x08082049 (FS card effect handler table, CID=0x1200)
#     FS entry at 0x09e43414: [+0x00]=0x1200 (PENGUIN_SOLDIER_CID), [+0x04]=0x080676e1,
#       [+0x08]=0x080509fd, [+0x14]=0x08082049 (fn_routing slot = BLK1+1)
#     0x82046..0x82047 = 0x0000 padding (skip; not a fn entry)
#     0x82134..0x8213f = literal pool (6 words handled as createDWord)
#     Literal pool words: 0x82134=0x0201e2a0 (gDuelCardCtxBase), 0x82138=0xfffc7fff,
#       0x8213c=0x00000868 (PLAYER_BLOCK_STRIDE), 0x82140? NO -- 0x82140 = JT base (NOT pool)
#     Wait: proposal says pool 0x82134..0x82140 = 6 words:
#       0x82134=0x0201e2a0, 0x82138=0xfffc7fff, 0x8213c=0x00000868,
#       0x82140? But 0x82140 is the jump table base (6 entries at 82140..82157).
#     Re-read proposal: "literal pool 0x82134..0x8213f (6 words: 0x0201e2a0, 0xfffc7fff,
#       0x00000868, 0x0201c510, 0x0201b290, 0x08082140)"
#     6 words at: 0x82134, 0x82138, 0x8213c, 0x82140?... wait that's only 5*4=20B
#     Pool 0x82134..0x8213f = 0xc bytes = 3 words: 0x82134, 0x82138, 0x8213c
#     Then 0x82140..0x82157 = 6*4=0x18 bytes = jump table (6 words)
#     BUT proposal says: "0x82134..0x82140: literal pool (6 words)" -- 6*4=0x18B
#     meaning pool extends from 0x82134 to 0x82147 (inclusive)?
#     Offset 0x82134: gDuelCardCtxBase
#     Offset 0x82138: DISPLAY_CODE_CLEAR_MASK/DUAL_LABEL_RENDER_STATE_CLEAR
#     Offset 0x8213c: PLAYER_BLOCK_STRIDE
#     Offset 0x82140: wait, proposal says 6 words in pool...
#     Actually re-reading: "0x82134..0x82140: literal pool (6 words: 0x0201e2a0, 0xfffc7fff,
#     0x00000868, 0x0201c510, 0x0201b290, 0x08082140)" -- the JT ptr IS the 6th pool word
#     so pool = 0x82134..0x82147 (6 * 4B = 0x18B), then JT at 0x82148?
#     But current asm already shows JT .word entries at lines 17812-17817 starting at
#     "@ 08082140 58210808" etc. So JT starts at 0x82140.
#     6 pool words ending at 0x8214f would overlap JT. This cannot be right.
#     RESOLUTION: pool = 4 words at 0x82134..0x82143 (the 5th=0x0201b290, 6th=0x08082140 JT ptr)?
#     No, asm already has ".word 0x08082158 @ 08082140..." etc -- these are the JT entries.
#     The "6 words" in proposal appears to count pool + JT base ptr together.
#     ACTUAL pool (before JT): words at 0x82134, 0x82138, 0x8213c ONLY = 3 words.
#     Then JT at 0x82140 is already decoded in asm as .word entries (lines 17812-17817).
#     So: createDWord for pool words 0x82134, 0x82138, 0x8213c ONLY (3 words in BLK1).
#     The 0x8213c may actually be JT ptr or JT start -- check asm to be sure:
#
#   BLK2: 6 sub-stubs at 0x08082158..0x0808228f
#     Reached via raw-ptr jump table at 0x8082140 (JT[0..5] already as .word in asm).
#     Sub-stubs: sub0=0x08082158, sub1=0x08082190, sub2=0x080821bc,
#                sub3=0x08082214, sub4=0x08082218, sub5=0x08082240
#     DAT_08082158 label already present in asm.
#     Per-stub DisassembleCommand (NOT single range -- JT is raw-ptr dispatch).
#     setTMode for full range [0x08082158, 0x08082290) before disasm.
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler
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


def _check_mem_word(addr_int, expected):
    """Verify ROM word at addr_int matches expected (for debug)."""
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        match = (actual == (expected & 0xFFFFFFFF))
        print("[check] 0x%08x: got=0x%08x exp=0x%08x %s" % (
            addr_int, actual, expected & 0xFFFFFFFF, 'OK' if match else 'MISMATCH'))
        return match
    except Exception as e:
        print("[check err] 0x%08x: %s" % (addr_int, e))
        return False


def main():
    print("=== DisassembleF10Seg7bBlocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] BLK1: route_penguin_soldier_equip_display (0x08082048..0x08082133)")
        print("[DRY]   clearListing + setTMode 0x08082046..0x0808213f (BLK1 range)")
        print("[DRY]   disasm_stub 0x08082048 (fn entry; 0x82046 = 0x0000 padding skip)")
        print("[DRY]   createDWord pool: 0x0808210c=gDuelCardCtxBase, "
              "0x08082110=DUAL_LABEL_RENDER_STATE_CLEAR, 0x08082114=PLAYER_BLOCK_STRIDE, "
              "0x08082118=gDuelFieldSlots; 0x82134=0x4687=THUMB CODE skip; "
              "0x82138=gDuelPhaseFlags, 0x8213c=JT ptr")
        print("[DRY]   createLabel 0x0808213c: route_penguin_soldier_jump_table_ptr")
        print("[DRY]   createFunction 0x08082048: route_penguin_soldier_equip_display + plate")
        print("[DRY] BLK2: 6 sub-stubs (0x08082158..0x0808228f)")
        print("[DRY]   clearListing + setTMode 0x08082158..0x0808228f")
        print("[DRY]   disasm_stub x6: 0x82158/0x82190/0x821bc/0x82214/0x82218/0x82240")
        print("[DRY]   createFunction x6: route_penguin_soldier_equip_sub0..sub5 + plates")
        return

    # -----------------------------------------------------------------------
    # BLK1: route_penguin_soldier_equip_display
    # Range: 0x08082046..0x0808213f (BLK1 incbin range)
    # Fn body: 0x08082048..0x08082133; pool: 0x08082134..0x0808213f (3 words)
    # 0x08082046..0x08082047 = 0x0000 padding, skip
    # Jump table 0x08082140..0x08082157 already decoded as .word in asm -- NO action
    # -----------------------------------------------------------------------
    print("--- BLK1: route_penguin_soldier_equip_display ---")
    # Verify key pool words (ROM-verified layout; 0x82134=0x4687=THUMB code, skip)
    _check_mem_word(0x0808210c, 0x0201e2a0)  # expect gDuelCardCtxBase
    _check_mem_word(0x08082110, 0xfffc7fff)  # expect DUAL_LABEL_RENDER_STATE_CLEAR
    _check_mem_word(0x08082114, 0x00000868)  # expect PLAYER_BLOCK_STRIDE
    _check_mem_word(0x08082118, 0x0201c510)  # expect gDuelFieldSlots
    _check_mem_word(0x08082138, 0x0201b290)  # expect gDuelPhaseFlags
    _check_mem_word(0x0808213c, 0x08082140)  # expect JT ptr

    _clear_and_tmode(0x08082046, 0x0808213f)
    _disasm_stub(0x08082048)  # fn entry (push {r4,r5,...,lr} or similar THUMB entry)

    # Pool words in BLK1 -- ROM-verified layout:
    # 0x8210c=0x0201e2a0, 0x82110=0xfffc7fff, 0x82114=0x868, 0x82118=0x0201c510 (mid-fn pool)
    # 0x82134=0x4687 = THUMB code (mov pc,r0) -- DO NOT createDWord here
    # 0x82138=0x0201b290, 0x8213c=0x08082140 (trailing literal pool, 2 words)
    _create_dword(0x0808210c, 'penguin_equip_card_ctx_10c',
                  'gDuelCardCtxBase=0x0201e2a0: duel card activation context base')
    _create_dword(0x08082110, 'penguin_equip_attr_clear_110',
                  'DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff: AND mask clears bits[17:15]')
    _create_dword(0x08082114, 'penguin_equip_stride_114',
                  'PLAYER_BLOCK_STRIDE=0x868: player data block stride')
    _create_dword(0x08082118, 'penguin_equip_dfs_118',
                  'gDuelFieldSlots=0x0201c510: duel field zone slot array')
    # 0x82134 = 0x4687 = THUMB code (mov pc,r0) -- skip createDWord
    _create_dword(0x08082138, 'penguin_equip_phase_flags_138',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0808213c, 'route_penguin_soldier_jump_table_ptr',
                  'ptr to raw-ptr jump table for 6 equip display sub-stubs at 0x08082140')

    _create_function(
        0x08082048,
        'route_penguin_soldier_equip_display',
        "@ fn_routing for PENGUIN_SOLDIER_CID(0x1200). "
        "Received via FS table entry 0x09e43414 "
        "[CID=0x1200, fn_activate=0x080676e1, fn_eligible=0x080509fd, fn_routing=0x08082049]. "
        "Drives equip display state machine with sub-stub dispatch via raw-ptr jump table "
        "at 0x08082140."
    )

    # -----------------------------------------------------------------------
    # BLK2: 6 sub-stubs (0x08082158..0x0808228f)
    # Reached via raw-ptr JT at 0x08082140 (already decoded as .word in asm)
    # DAT_08082158 label already present in asm
    # -----------------------------------------------------------------------
    print("--- BLK2: 6 sub-stubs (route_penguin_soldier_equip_sub0..sub5) ---")
    _clear_and_tmode(0x08082158, 0x0808228f)

    # Per-stub DisassembleCommand (one per JT entry to ensure correct stub boundaries)
    _disasm_stub(0x08082158)  # sub0: BL count_effect_node_zone_activations + invoke_card_display_op_0x31_sub1
    _disasm_stub(0x08082190)  # sub1: BL set_equip_activation_state_by_mode__08096a4c
    _disasm_stub(0x080821bc)  # sub2: BL check_activation_display_state_is_confirmed + enqueue
    _disasm_stub(0x08082214)  # sub3: 4B stub movs r0,#0x75; b <somewhere>
    _disasm_stub(0x08082218)  # sub4: BL set_equip_activation_state_by_mode__08096a4c
    _disasm_stub(0x08082240)  # sub5: BL check_activation_display_state_is_confirmed + enqueue; exit Sub-case E

    # Create functions for each sub-stub
    _create_function(
        0x08082158,
        'route_penguin_soldier_equip_sub0',
        "@ Sub-stub 0 of Penguin Soldier equip display: reached via JT[0]=0x08082158. "
        "Calls count_effect_node_zone_activations + invoke_card_display_op_0x31_sub1."
    )
    _create_function(
        0x08082190,
        'route_penguin_soldier_equip_sub1',
        "@ Sub-stub 1: reached via JT[1]=0x08082190. "
        "Calls set_equip_activation_state_by_mode__08096a4c."
    )
    _create_function(
        0x080821bc,
        'route_penguin_soldier_equip_sub2',
        "@ Sub-stub 2: reached via JT[2]=0x080821bc. "
        "Calls check_activation_display_state_is_confirmed; "
        "if confirmed calls enqueue_equip_slot_sprite_with_code_rotation."
    )
    _create_function(
        0x08082214,
        'route_penguin_soldier_equip_sub3',
        "@ Sub-stub 3: reached via JT[3]=0x08082214. "
        "4-byte stub: sets r0=0x75 then branches."
    )
    _create_function(
        0x08082218,
        'route_penguin_soldier_equip_sub4',
        "@ Sub-stub 4: reached via JT[4]=0x08082218. "
        "Calls set_equip_activation_state_by_mode__08096a4c."
    )
    _create_function(
        0x08082240,
        'route_penguin_soldier_equip_sub5',
        "@ Sub-stub 5: reached via JT[5]=0x08082240. "
        "Calls check_activation_display_state_is_confirmed; "
        "if confirmed calls enqueue_equip_slot_sprite_with_code_rotation. "
        "Exit Sub-case E (pop {r1};bx r1 at 0x08082288)."
    )

    # Pool word at end of BLK2 (0x8228c..0x8228f = 0x0201b290 = gDuelPhaseFlags)
    _create_dword(0x0808228c, 'penguin_sub5_phase_flags_28c',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub5 literal pool)')

    print("")
    print("=== DisassembleF10Seg7bBlocks DONE ===")
    print("=== BLK1: route_penguin_soldier_equip_display @ 0x08082048 (6 pool DWords) ===")
    print("=== BLK2: 6 sub-stubs route_penguin_soldier_equip_sub0..sub5 @ 0x08082158..0x08082240 ===")


main()
