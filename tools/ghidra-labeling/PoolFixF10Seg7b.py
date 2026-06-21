# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF10Seg7b.py -- f10 Seg-7b BLK2 literal pool DWord fix
#   Pool words inside 6 sub-stubs (0x82158..0x8228f) that remained as .byte blocks
#   after DisassembleF10Seg7bBlocks.py ran.
#   Fixes build errors: "invalid offset, value too big (0xFFFFFFFC)" at asm/10 L17948/17991/...
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, label, eol_ascii)
# All values ROM-verified via python struct.unpack
POOL_DWORDS = [
    # sub0 pool (0x82188..0x8218f): 2 words
    (0x08082188, 'penguin_sub0_attr_clear_188',
     'DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff: AND mask clears bits[17:15]'),
    (0x0808218c, 'penguin_sub0_phase_flags_18c',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),

    # sub1 pool (0x821a4): 1 word
    (0x080821a4, 'penguin_sub1_lp_base_1a4',
     'gP1LifePoints=0x0201c4e0: LP state struct base'),

    # sub2 pool (0x821f4..0x82200): 4 words
    (0x080821f4, 'penguin_sub2_lp_base_1f4',
     'gP1LifePoints=0x0201c4e0: LP state struct base'),
    (0x080821f8, 'penguin_sub2_sprite_off_1f8',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68: [gP1LifePoints+0x1d68] sprite display control'),
    (0x080821fc, 'penguin_sub2_anim_off_1fc',
     'ELIGIB_ANIM_STATE_OFF=0x1d6c: [gP1LifePoints+0x1d6c] animation state index'),
    (0x08082200, 'penguin_sub2_phase_flags_200',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),

    # sub3/sub4 boundary pool (0x82210): 1 word
    (0x08082210, 'penguin_sub3_phase_flags_210',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),

    # sub4 pool (0x82238..0x8223c): 2 words
    (0x08082238, 'penguin_sub4_lp_base_238',
     'gP1LifePoints=0x0201c4e0: LP state struct base'),
    (0x0808223c, 'penguin_sub4_handler_ptr_23c',
     'check_effect_node_handler_for_slot+1 (THUMB fn-ptr)=0x08081de5'),

    # sub5 pool (0x82268..0x82270): 3 words
    (0x08082268, 'penguin_sub5_lp_base_268',
     'gP1LifePoints=0x0201c4e0: LP state struct base'),
    (0x0808226c, 'penguin_sub5_sprite_off_26c',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68: [gP1LifePoints+0x1d68] sprite display control'),
    (0x08082270, 'penguin_sub5_anim_off_270',
     'ELIGIB_ANIM_STATE_OFF=0x1d6c: [gP1LifePoints+0x1d6c] animation state index'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword(addr_int, label, eol):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType

    if DRY:
        print("[dry] POOL_FIX 0x%08x  %s  '%s'" % (addr_int, label, eol))
        return

    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))

    sm = currentProgram.getSymbolTable()
    sm.createLabel(a, label, SourceType.USER_DEFINED)

    cu = listing.getCodeUnitAt(a)
    if cu is not None:
        cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[pool fix] 0x%08x %s" % (addr_int, label))


def main():
    print("=== PoolFixF10Seg7b (DRY=%s) ===" % DRY)
    print("  Fixing %d BLK2 sub-stub literal pool words" % len(POOL_DWORDS))
    for addr_int, label, eol in POOL_DWORDS:
        _create_dword(addr_int, label, eol)
    print("=== PoolFixF10Seg7b DONE ===")


main()
