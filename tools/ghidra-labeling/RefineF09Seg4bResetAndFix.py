# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bResetAndFix.py -- Full reset and redo of B6, B7, B8 disasm
#
# Problem: force_dword with 8-byte clearListing over-cleared into adjacent stubs.
# Fix: clearListing entire block range, setTMode, then per-address DisassembleCommand
# for ALL entry points (stubs + branch targets + fn_eligible), THEN force DWords
# on pool words with 4-byte clearListing only.
#
# B6 [0x72444..0x7257b]: entry points (all 6 stubs + fn_eligible):
#   Stubs from dispatch table: 0x72444, 0x7248a, 0x724ac, 0x724b4, 0x72534, 0x72540
#   Plus intermediate code regions reached by branches:
#     0x72480 (LAB_08072480, 10 bytes, reachable from 0x72444 branch b LAB_08072486)
#     0x7250c (LAB_0807250c, 0x24 bytes, reachable from 0x724b4 branch beq LAB_0807252a)
#     0x72556 (LAB_08072556, 0x1e bytes, reachable from fn_eligible branch b LAB_080726e6)
#
# B7 [0x72594..0x72733]: entry points:
#   Stubs: 0x72594, 0x725e8, 0x72624, 0x7264c, 0x72678, 0x726bc, 0x726f4
#   Plus intermediate code regions:
#     0x725a6 (LAB_080725a6, 0x32 bytes from 0x72594 branch b LAB_080726e6)
#     0x72620 (LAB_08072620, 4 bytes from vampire_sub_25e8)
#     0x726d2 (LAB_080726d2, 0x22 bytes, contains LAB_080726e6/e8)
#
# B8 [0x7274c..0x7286f]: entry points:
#   Stubs: 0x7274c, 0x727b8, 0x727e4, 0x72804, 0x72848, 0x72856
#   (No intermediate regions needed - simpler structure)
#
# Pool DWords to force AFTER disasm (4-byte clearListing only):
# B6: 0x72478, 0x7247c, 0x724a8, 0x72500, 0x72504, 0x72508, 0x72530, 0x72574, 0x72578
# B7: 0x725d8, 0x725dc, 0x725e0, 0x725e4, 0x7260c, 0x72610, 0x72614, 0x72618, 0x7261c
#     0x72648, 0x72674, 0x726b0, 0x726b4, 0x726b8, 0x7272c, 0x72730
# B8: 0x72788, 0x7278c, 0x72790, 0x727b4, 0x727dc, 0x727e0, 0x72800, 0x7282c, 0x72834

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def force_dword_4(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    """Force a DWord using EXACT 4-byte clearListing only."""
    pa = _addr(pool_addr)
    # Clear exactly 4 bytes
    try:
        clearListing(pa, _addr(pool_addr + 3))
    except Exception as e:
        print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
        print("[WARN] CodeUnitInsertionException @ 0x%08x: %s" % (pool_addr, e))
    except Exception as e:
        print("[WARN] unexpected createData @ 0x%08x: %s" % (pool_addr, e))
    existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing_p:
        try:
            sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (pool_label, e))
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)

def ensure_user_label(sym_tbl, addr_val, label_name):
    addr = _addr(addr_val)
    ud_exists = any(s.getName() == label_name and str(s.getSource()) == 'USER_DEFINED'
                   for s in sym_tbl.getSymbols(addr))
    if not ud_exists:
        try:
            sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x" % (label_name, addr_val))
        except Exception as e:
            print("[WARN] ensure_user_label %s: %s" % (label_name, e))

listing = currentProgram.getListing()
sym_tbl = currentProgram.getSymbolTable()
ctx = currentProgram.getProgramContext()
tmode = ctx.getRegister("TMode")

print("=== RefineF09Seg4bResetAndFix ===")

# =========================================================================
# STEP 1: Clear all 3 blocks completely
# =========================================================================
for (block_start, block_end, name) in [
    (0x08072444, 0x0807257b, 'B6'),
    (0x08072594, 0x08072733, 'B7'),
    (0x0807274c, 0x0807286f, 'B8'),
]:
    print("[CLEAR] %s 0x%08x..0x%08x" % (name, block_start, block_end))
    try:
        clearListing(_addr(block_start), _addr(block_end))
        print("        done")
    except Exception as e:
        print("[WARN] clearListing %s: %s" % (name, e))

# =========================================================================
# STEP 2: Set TMode for all 3 blocks
# =========================================================================
if tmode is not None:
    for (block_start, block_end) in [
        (0x08072444, 0x0807257b),
        (0x08072594, 0x08072733),
        (0x0807274c, 0x0807286f),
    ]:
        ctx.setValue(tmode, _addr(block_start), _addr(block_end), BigInteger.ONE)
    print("[TMODE] Set for B6/B7/B8")

# =========================================================================
# STEP 3: Disassemble all entry points in order (address order)
# =========================================================================
ALL_ENTRIES = [
    # B6
    (0x08072444, 'last_turn_sub_2444'),
    (0x08072480, 'LAB_08072480'),           # branch target of last_turn_sub_2444
    (0x0807248a, 'last_turn_sub_248a'),
    (0x080724ac, 'last_turn_sub_24ac'),
    (0x080724b4, 'last_turn_sub_24b4'),
    (0x0807250c, 'LAB_0807250c'),           # branch target of last_turn_sub_24b4
    (0x08072534, 'last_turn_sub_2534'),
    (0x08072540, 'fn_eligible_last_turn_2540'),
    (0x08072556, 'LAB_08072556'),           # branch target of fn_eligible_last_turn
    # B7
    (0x08072594, 'vampire_sub_2594'),
    (0x080725a6, 'LAB_080725a6'),           # branch target of vampire_sub_2594
    (0x080725e8, 'vampire_sub_25e8'),
    (0x08072624, 'vampire_sub_2624'),
    (0x08072620, 'LAB_08072620'),           # branch target of vampire_sub_25e8
    (0x0807264c, 'vampire_sub_264c'),
    (0x08072678, 'vampire_sub_2678'),
    (0x080726bc, 'vampire_sub_26bc'),
    (0x080726d2, 'LAB_080726d2'),           # branch target of vampire_sub_26bc (contains LAB_e6/e8)
    (0x080726f4, 'fn_eligible_vampire_lord_lady_26f4'),
    # B8
    (0x0807274c, 'equip_zone_sub_274c'),
    (0x080727b8, 'equip_zone_sub_27b8'),
    (0x080727e4, 'equip_zone_sub_27e4'),
    (0x08072804, 'equip_zone_sub_2804'),
    (0x08072848, 'equip_zone_sub_2848'),
    (0x08072856, 'equip_zone_sub_2856'),
]

for stub_addr, stub_label in ALL_ENTRIES:
    stub_a = _addr(stub_addr)
    cmd = DisassembleCommand(stub_a, None, False)
    if cmd.applyTo(currentProgram):
        print("[DISASM] ok @ 0x%08x (%s)" % (stub_addr, stub_label))
    else:
        print("[WARN] disasm 0x%08x (%s): %s" % (stub_addr, stub_label, cmd.getStatusMsg()))

# =========================================================================
# STEP 4: Force DWords on pool words (4-byte clearListing only)
# =========================================================================
ALL_POOLS = [
    # B6 pools
    (0x08072478, 'pool_b6_2478', 'gDuelCardCtxBase=0x0201e2a0; literal pool B6'),
    (0x0807247c, 'pool_b6_247c', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
    (0x080724a8, 'pool_b6_24a8', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
    (0x08072500, 'pool_b6_2500', 'gP1LifePoints=0x0201c4e0; literal pool B6'),
    (0x08072504, 'pool_b6_2504', 'LP_CARD_TRACK_NEXT_OFF=0x1daa; literal pool B6'),
    (0x08072508, 'pool_b6_2508', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B6'),
    (0x08072530, 'pool_b6_2530', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B6'),
    (0x08072574, 'pool_b6_2574', 'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_last_turn'),
    (0x08072578, 'pool_b6_2578', '0x0807257c; literal pool fn_eligible_last_turn'),
    # B7 pools
    (0x080725d8, 'pool_b7_25d8', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
    (0x080725dc, 'pool_b7_25dc', '0x000010d0 offset; literal pool B7'),
    (0x080725e0, 'pool_b7_25e0', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
    (0x080725e4, 'pool_b7_25e4', '0x08090625 ROM addr; literal pool B7'),
    (0x0807260c, 'pool_b7_260c', 'gDuelPhaseFlags=0x0201b290; literal pool B7'),
    (0x08072610, 'pool_b7_2610', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
    (0x08072614, 'pool_b7_2614', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
    (0x08072618, 'pool_b7_2618', '0x1d6c LP offset; literal pool B7'),
    (0x0807261c, 'pool_b7_261c', '0x1d70 LP offset; literal pool B7'),
    (0x08072648, 'pool_b7_2648', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
    (0x08072674, 'pool_b7_2674', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B7'),
    (0x080726b0, 'pool_b7_26b0', 'gP1LifePoints=0x0201c4e0; literal pool B7'),
    (0x080726b4, 'pool_b7_26b4', '0x1ce8 LP offset; literal pool B7'),
    (0x080726b8, 'pool_b7_26b8', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B7'),
    (0x0807272c, 'pool_b7_272c', 'gDuelPhaseFlags=0x0201b290; literal pool fn_eligible_vampire_lord_lady'),
    (0x08072730, 'pool_b7_2730', '0x08072734; literal pool fn_eligible_vampire_lord_lady'),
    # B8 pools
    (0x08072788, 'pool_b8_2788', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
    (0x0807278c, 'pool_b8_278c', 'PLAYER_BLOCK_STRIDE=0x868; literal pool B8'),
    (0x08072790, 'pool_b8_2790', 'gDuelCardCtxBase=0x0201e2a0; literal pool B8'),
    (0x080727b4, 'pool_b8_27b4', '0x1b9; literal pool B8'),
    (0x080727dc, 'pool_b8_27dc', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B8'),
    (0x080727e0, 'pool_b8_27e0', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
    (0x08072800, 'pool_b8_2800', 'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool B8'),
    (0x0807282c, 'pool_b8_282c', 'gP1LifePoints=0x0201c4e0; literal pool B8'),
    (0x08072834, 'pool_b8_2834', 'LP_CARD_TRACK_NEXT_OFF=0x1daa; literal pool B8'),
]

for pool_addr, pool_label, pool_eol in ALL_POOLS:
    force_dword_4(listing, sym_tbl, pool_addr, pool_label, pool_eol)

# =========================================================================
# STEP 5: Create stub labels + EOL
# =========================================================================
STUB_LABELS_EOL = [
    # B6
    (0x08072444, 'last_turn_sub_2444',
     'raw-dispatch sub-stub (table[0x72440]=0x08072444); 5-entry table @0x72430..0x72443'),
    (0x0807248a, 'last_turn_sub_248a', None),
    (0x080724ac, 'last_turn_sub_24ac', None),
    (0x080724b4, 'last_turn_sub_24b4', None),
    (0x08072534, 'last_turn_sub_2534', None),
    (0x08072540, 'fn_eligible_last_turn_2540',
     'fn_eligible: Last Turn (CID=0x151e=LAST_TURN_CID); FS THUMB+1 @GBA:0x09e41090'),
    # B7
    (0x08072594, 'vampire_sub_2594',
     'raw-dispatch sub-stub (table[0x72590]=0x08072594); 6-entry table @0x7257c..0x72593'),
    (0x080725e8, 'vampire_sub_25e8', None),
    (0x08072624, 'vampire_sub_2624', None),
    (0x0807264c, 'vampire_sub_264c', None),
    (0x08072678, 'vampire_sub_2678', None),
    (0x080726bc, 'vampire_sub_26bc', None),
    (0x080726f4, 'fn_eligible_vampire_lord_lady_26f4',
     'fn_eligible: VAMPIRE_LORD_CID(0x1522,x2)+VAMPIRE_LADY_CID(0x1746); FS THUMB+1 x3 @GBA:0x09e43e08/0x09e44930/0x09e45b60'),
    # B8
    (0x0807274c, 'equip_zone_sub_274c',
     'raw-dispatch sub-stub (table[0x72748]=0x0807274c); 6-entry table @0x72734..0x7274b'),
    (0x080727b8, 'equip_zone_sub_27b8', None),
    (0x080727e4, 'equip_zone_sub_27e4', None),
    (0x08072804, 'equip_zone_sub_2804', None),
    (0x08072848, 'equip_zone_sub_2848', None),
    (0x08072856, 'equip_zone_sub_2856', None),
]

for stub_addr, stub_label, stub_eol in STUB_LABELS_EOL:
    stub_a = _addr(stub_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
    if stub_label not in existing:
        try:
            sym_tbl.createLabel(stub_a, stub_label, SourceType.USER_DEFINED)
            print("[LABEL] %s created" % stub_label)
        except Exception as e:
            print("[WARN] label %s: %s" % (stub_label, e))
    if stub_eol:
        cu = listing.getCodeUnitAt(stub_a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, stub_eol)

# =========================================================================
# STEP 6: Ensure USER_DEFINED labels for key branch targets
# =========================================================================
for addr_val, label_name in [
    (0x08072486, 'LAB_08072486'),
    (0x0807252a, 'LAB_0807252a'),
    (0x080726e6, 'LAB_080726e6'),
    (0x080726e8, 'LAB_080726e8'),
]:
    ensure_user_label(sym_tbl, addr_val, label_name)

print("\n=== RefineF09Seg4bResetAndFix DONE ===")
