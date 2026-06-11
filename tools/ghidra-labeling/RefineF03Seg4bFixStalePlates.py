# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4bFixStalePlates.py -- Fix 4 stale FUN_ plate comments in Seg-4b
#   These plate comments are at inner code-block addresses (not function entry points),
#   so they were not updated by the main RefineF03Seg4bSlots.py PLATE_SLOTS dict.
#   All text is pure ASCII (no CJK).
#
#   Addresses and correct plates:
#   0x08038c02 -> compute_lp_cost_by_hand_field6 (FUN_08037ec0 -> eval_slot_score_entry_full)
#   0x08038d08 -> compute_lp_cost_by_extra_deck_card_id (FUN_08037ec0 -> eval_slot_score_entry_full)
#   0x08038dd4 -> compute_lp_cost_by_zone_field5_x100 (FUN_08038dea -> compute_lp_cost_by_zone_field5_x200)
#   0x08038e00 -> compute_lp_cost_by_zone_field5_both_players (FUN_08037ec0 -> eval_slot_score_entry_full)

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(val):
    return toAddr(val)

# (addr, new_plate_text) -- pure ASCII, no FUN_/CJK
STALE_PLATE_FIXES = [
    (0x08038c02,
     "compute_lp_cost_by_hand_field6 [0x08038c60]\n"
     "Wrap count_hand_cards_by_field6: scale count by 5 for LP cost, jump to shared scale path.\n"
     "Flow: ldr r0=[sp+0x3c] (player_side); movs r1,1 (target_field6=1);\n"
     "bl count_hand_cards_by_field6; lsls r1,r0,2; adds r1,r1,r0 (r1=count*5);\n"
     "b LAB_08038d98 (multiply r1 by 0x4e=78 and store into r10).\n"
     "Case branch of eval_slot_score_entry_full large LP cost dispatch.\n"
     "Constants: field6_target=1, lp_scale=5, shared_scale_addr=0x08038d98."),

    (0x08038d08,
     "compute_lp_cost_by_extra_deck_card_id [0x08038d34]\n"
     "Wrap count_extra_deck_cards_by_id: scale count by 5 for LP cost, jump to shared scale path.\n"
     "Flow: ldr r1,DAT=0x1919 (card_id=0x1919); ldr r0=[sp+0x3c] (player_side);\n"
     "bl count_extra_deck_cards_by_id(player, 0x1919); lsls r1,r0,2; adds r1,r1,r0 (r1=count*5);\n"
     "b LAB_08038d98 (multiply by (0x10-1)*4 and accumulate into r10).\n"
     "Case branch of eval_slot_score_entry_full large LP cost dispatch.\n"
     "Constants: card_id_target=0x1919, lp_scale=5, shared_scale_addr=0x08038d98."),

    (0x08038dd4,
     "compute_lp_cost_by_zone_field5_x100 [0x08038e84]\n"
     "Call count_zone_slots_with_card_field5(0) and (1), sum both-side counts,\n"
     "multiply by 0x64 (100), write to r7[+0x18] and r7[+0x14] via fall-through.\n"
     "No APCS params; r7 (non-APCS): slot_score_entry ptr.\n"
     "Side effects: [r7+0x18] := count*100; [r7+0x14] := count*100 (fall-through).\n"
     "Sibling variants: compute_lp_cost_by_zone_field5_x200 (x200),\n"
     "compute_lp_cost_by_zone_field5_both_players (x390). Constants: scale_factor=0x64=100."),

    (0x08038e00,
     "compute_lp_cost_by_zone_field5_both_players [0x08038e9c]\n"
     "Call count_zone_slots_with_card_field5 for both players, sum results,\n"
     "apply LP cost formula (count*5)*0x4e, write to r7[+0x18] and r7[+0x14].\n"
     "Flow: bl count_zone_slots_with_card_field5(0)->r4; bl (1)->r0; r4+=r0;\n"
     "r1=r4*5; r0=(r1*0x10-r1)*4; write to r7[+0x18]; shared path LAB_08038e18 writes r7[+0x14].\n"
     "Case branch of eval_slot_score_entry_full large LP cost dispatch.\n"
     "Constants: lp_scale_a=5, lp_scale_b=0x4e=78 (total factor=count*390)."),
]

print("=== RefineF03Seg4bFixStalePlates.py DRY=%s ===" % DRY)

applied = 0
skipped = 0
for addr_val, plate_text in STALE_PLATE_FIXES:
    addr = _addr(addr_val)
    if DRY:
        print("DRY PLATE at 0x%08x: %s..." % (addr_val, plate_text[:40]))
        applied += 1
        continue
    cu = currentProgram.getListing().getCodeUnitAt(addr)
    if cu is None:
        print("WARN: no code unit at 0x%08x -- SKIP" % addr_val)
        skipped += 1
        continue
    cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
    print("Applied PLATE at 0x%08x" % addr_val)
    applied += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
