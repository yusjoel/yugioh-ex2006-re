# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg1Slots.py -- F08 Seg-1 (0x080643e0..0x0806544c)
#   equip slot eligibility + Neo Daedalus cluster + LP delta dispatch
#   EQ=87 (52 reuse + 35 new CIDs/LP-delta)
#   RENAME=13 (PTR_gP1LifePoints_* -> write_equip_lp_*_lp_base labels)
#   PLATE=17 occurrences (3 stale FUN_ names -> current names; file header mojibake rewrite)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- any CJK here is a red-line error.
# Two disasm blocks handled in DisassembleF08Seg1Blocks.py.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (12 slots) ----
    (0x0806446c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_eligible_zone_type_stride_a', None),
    (0x080644a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_eligible_zone_type_stride_b', None),
    (0x08064558, 0x0000ffff, 'SLOT_CARD_EMPTY',
     'check_chain_pair_pair_not_found',
     'SLOT_CARD_EMPTY sentinel 0xffff: pair_id == 0xffff means not-found'),
    (0x08064560, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_chain_pair_stride', None),
    (0x080646f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'invoke_equip_sprite_stride_a', None),
    (0x08064874, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_sprite_stride', None),
    (0x08065148, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_des_koala_stride', None),
    (0x08065174, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_alt_player_stride', None),
    (0x080651b8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_ka2_stride', None),
    (0x08065258, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_minar_stride', None),
    (0x08065420, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_vandalgyon_stride_a', None),
    (0x08065448, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'write_equip_lp_vandalgyon_stride_b', None),

    # ---- ewram.inc: gDuelFieldSlots = 0x0201c510 (5 slots) ----
    (0x08064470, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_eligible_zone_type_slots_a', None),
    (0x080644a8, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_eligible_zone_type_slots_b', None),
    (0x080646f8, 0x0201c510, 'gDuelFieldSlots',
     'invoke_equip_sprite_slots_a', None),
    (0x0806487c, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_sprite_slots', None),
    (0x080651bc, 0x0201c510, 'gDuelFieldSlots',
     'write_equip_lp_ka2_slots', None),

    # ---- ewram.inc: gP1LifePoints = 0x0201c4e0 (1 slot - already-named DWORD) ----
    (0x0806455c, 0x0201c4e0, 'gP1LifePoints',
     'check_chain_pair_lp_base', None),

    # ---- ewram.inc: gDuelFieldSlots_p2_base = 0x0201c5d8 (1 slot) ----
    (0x08064878, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'dispatch_equip_sprite_slots_p2', None),

    # ---- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 (1 slot) ----
    (0x0806526c, 0x0201bb90, 'gEquipChainSlotRefs',
     'write_equip_lp_equip_chain_ref', None),

    # ---- card_info.inc: CID reuse (29 existing slots) ----
    (0x08064758, 0x000012c6, 'cid_12c6',
     'invoke_equip_sprite_cid_a', None),
    (0x0806475c, 0x0000145b, 'SCROLL_OF_BEWITCHMENT_CID',
     'invoke_equip_sprite_cid_b', None),
    (0x08064914, 0x0000118a, 'AMEBA_CID',
     'dispatch_equip_lp_ameba_cid', None),
    (0x0806492c, 0x000010f8, 'MOOYAN_CURRY_CID',
     'dispatch_equip_lp_mooyan_curry_cid', None),
    (0x080649a4, 0x000011bc, 'MINAR_CID',
     'dispatch_equip_lp_minar_cid', None),
    (0x080649cc, 0x000012a2, 'SKULL_MARK_LADYBUG_CID',
     'dispatch_equip_lp_skull_ladybug_cid', None),
    (0x080649f4, 0x00001322, 'SNATCH_STEAL_CID',
     'dispatch_equip_lp_snatch_steal_cid', None),
    (0x08064a04, 0x00001307, 'RESTRUCTER_REVOLUTION_CID',
     'dispatch_equip_lp_restructer_cid', None),
    (0x08064a20, 0x0000137b, 'EYE_OF_TRUTH_CID',
     'dispatch_equip_lp_eye_of_truth_cid', None),
    (0x08064b64, 0x0000159b, 'DARK_ROOM_OF_NIGHTMARE_CID',
     'dispatch_equip_lp_dark_room_cid', None),
    (0x08064b74, 0x0000158c, 'GRAVEKEEPERS_CANNONHOLDER_CID',
     'dispatch_equip_lp_gk_cannonholder_cid', None),
    (0x08064b90, 0x000015ee, 'WAVE_MOTION_CANNON_CID',
     'dispatch_equip_lp_wave_cannon_cid', None),
    (0x08064bf4, 0x000017c8, 'SPHINX_TELEIA_CID',
     'dispatch_equip_lp_sphinx_teleia_cid', None),
    (0x08064c08, 0x0000163f, 'GRANADORA_CID',
     'dispatch_equip_lp_granadora_cid', None),
    (0x08064c70, 0x000016f5, 'BURNING_ALGAE_CID',
     'dispatch_equip_lp_burning_algae_cid', None),
    (0x08064c84, 0x0000170b, 'GUARDIAN_ANGEL_JOAN_CID',
     'dispatch_equip_lp_guardian_joan_cid', None),
    (0x08064c98, 0x0000173f, 'AGENT_OF_JUDGMENT_SATURN_CID',
     'dispatch_equip_lp_saturn_cid', None),
    (0x08064cec, 0x00001762, 'BACKFIRE_CID',
     'dispatch_equip_lp_backfire_cid', None),
    (0x08064d34, 0x000017a5, 'CARD_7_CID',
     'dispatch_equip_lp_card7_cid', None),
    (0x08064d80, 0x0000190a, 'DARK_RULER_VANDALGYON_CID',
     'dispatch_equip_lp_vandalgyon_cid', None),
    (0x08064d90, 0x00001804, 'CEMETARY_BOMB_CID',
     'dispatch_equip_lp_cemetary_bomb_cid', None),
    (0x08064db0, 0x00001877, 'BRAIN_JACKER_CID',
     'dispatch_equip_lp_brain_jacker_cid', None),
    (0x08064dc0, 0x0000187b, 'POISON_FANGS_CID',
     'dispatch_equip_lp_poison_fangs_cid', None),
    (0x08064de8, 0x000018d0, 'LEGENDARY_BLACK_BELT_CID',
     'dispatch_equip_lp_legendary_belt_cid', None),
    (0x08064e04, 0x000018d7, 'KOZAKYS_SELF_DESTRUCT_CID',
     'dispatch_equip_lp_kozaky_cid', None),
    (0x08064e48, 0x00001987, 'ELEMENTAL_HERO_STEAM_HEALER_CID',
     'dispatch_equip_lp_steam_healer_cid', None),
    (0x08064e50, 0x00001929, 'SPIRITUAL_FIRE_ART_CID',
     'dispatch_equip_lp_spiritual_fire_cid', None),
    (0x08064e6c, 0x00001950, 'OXYGEDDON_CID',
     'dispatch_equip_lp_oxygeddon_cid', None),

    # ---- duel_field.inc: LP/score constants reuse (4 slots) ----
    (0x08065014, 0xfffffc18, 'PUZZLE_LP_STEP_1000',
     'write_equip_lp_snatch_steal_neg1000',
     'PUZZLE_LP_STEP_1000 = -1000 (s32); Snatch Steal LP penalty'),
    (0x080650d4, 0x00000bb8, 'LP_COST_3000',
     'write_equip_lp_des_koala_max_3000',
     'LP_COST_3000 = 3000 LP threshold for Des Koala scaled LP path'),
    (0x080650ec, 0xfffffe70, 'ZONE_EFFECT_ATK_PENALTY_500',
     'write_equip_lp_neg400',
     'ZONE_EFFECT_ATK_PENALTY_500 = 0xfffffe70 = -400 (name misleading, actual value -400)'),
    (0x080653d0, 0xfffffd44, 'SCORE_DELTA_NEG_700',
     'write_equip_lp_fuhma_neg700',
     'SCORE_DELTA_NEG_700 = -700; Fuhma Shuriken LP penalty (same value as score domain -700)'),

    # ---- card_info.inc: NEW CIDs (29 new) ----
    (0x0806490c, 0x0000161d, 'DES_KOALA_CID',
     'dispatch_equip_lp_des_koala_cid', None),
    (0x08064910, 0x000013a8, 'WOODLAND_SPRITE_CID',
     'dispatch_equip_lp_woodland_sprite_cid', None),
    (0x08064950, 0x000010fe, 'cid_10fe',
     'dispatch_equip_lp_cid_10fe', None),
    (0x08064998, 0x000012e8, 'cid_12e8',
     'dispatch_equip_lp_cid_12e8', None),
    (0x0806499c, 0x000011c9, 'GRIGGLE_CID',
     'dispatch_equip_lp_griggle_cid', None),
    (0x080649c4, 0x0000129a, 'REFLECT_BOUNDER_CID',
     'dispatch_equip_lp_reflect_bounder_cid', None),
    (0x08064a18, 0x0000137a, 'GIFT_OF_MYSTICAL_ELF_CID',
     'dispatch_equip_lp_mystical_elf_cid', None),
    (0x08064a74, 0x0000141f, 'RAIN_OF_MERCY_CID',
     'dispatch_equip_lp_rain_of_mercy_cid', None),
    (0x08064a94, 0x0000144b, 'AMAZON_ARCHER_CID',
     'dispatch_equip_lp_amazon_archer_cid', None),
    (0x08064ab8, 0x00001459, 'MARIE_THE_FALLEN_ONE_CID',
     'dispatch_equip_lp_marie_cid', None),
    (0x08064acc, 0x00001467, 'DARK_MAGICIAN_TOME_CID',
     'dispatch_equip_lp_dm_tome_cid', None),
    (0x08064ad4, 0x000014b2, 'NIGHTMARE_WHEEL_CID',
     'dispatch_equip_lp_nightmare_wheel_cid', None),
    (0x08064b08, 0x00001565, 'TOON_CANNON_SOLDIER_CID',
     'dispatch_equip_lp_toon_cannon_cid', None),
    (0x08064b18, 0x000014f3, 'ZOLGA_CID',
     'dispatch_equip_lp_zolga_cid', None),
    (0x08064b3c, 0x00001525, 'POISON_MUMMY_CID',
     'dispatch_equip_lp_poison_mummy_cid', None),
    (0x08064ba0, 0x000015f4, 'SECRET_BARREL_CID',
     'dispatch_equip_lp_secret_barrel_cid', None),
    (0x08064c34, 0x000016c5, 'INFERNO_CID',
     'dispatch_equip_lp_inferno_cid', None),
    (0x08064c60, 0x000016fa, 'STEALTH_BIRD_CID',
     'dispatch_equip_lp_stealth_bird_cid', None),
    (0x08064cc4, 0x00001767, 'SOLAR_RAY_CID',
     'dispatch_equip_lp_solar_ray_cid', None),
    (0x08064ce4, 0x00001761, 'GOBLIN_THIEF_CID',
     'dispatch_equip_lp_goblin_thief_cid', None),
    (0x08064d18, 0x00001794, 'ELEPHANT_STATUE_CID',
     'dispatch_equip_lp_elephant_statue_cid', None),
    (0x08064d44, 0x000017c7, 'ANDRO_SPHINX_CID',
     'dispatch_equip_lp_andro_sphinx_cid', None),
    (0x08064df0, 0x000018c8, 'ELEMENTAL_HERO_FLAME_WINGMAN_CID',
     'dispatch_equip_lp_eh_flame_wingman_cid', None),
    (0x08064e14, 0x000018da, 'ROCK_BOMBARDMENT_CID',
     'dispatch_equip_lp_rock_bombardment_cid', None),
    (0x08064e70, 0x00001984, 'MAGICAL_BLAST_CID',
     'dispatch_equip_lp_magical_blast_cid', None),
    (0x08064e90, 0x000019cf, 'MEMORY_CRUSHER_CID',
     'dispatch_equip_lp_memory_crusher_cid', None),
    (0x08064eb8, 0x000019f0, 'GUARDIAN_EXODE_CID',
     'dispatch_equip_lp_guardian_exode_cid', None),

    # ---- equip_lp_delta.inc: NEW LP penalty constants (8 new) ----
    (0x08065098, 0xfffffda8, 'LP_EQUIP_DELTA_NEG_600',
     'write_equip_lp_solar_ray_neg600',
     'LP_EQUIP_DELTA_NEG_600 = -600 (s32); Solar Ray per eligible zone penalty'),
    (0x08065104, 0xfffffed4, 'LP_EQUIP_DELTA_NEG_300',
     'write_equip_lp_legendary_belt_neg300',
     'LP_EQUIP_DELTA_NEG_300 = -300 (s32); Legendary Black Belt range path (distinct domain from SCORE_DELTA_NEG_300)'),
    (0x080651c0, 0xfffffe0c, 'LP_EQUIP_DELTA_NEG_500',
     'write_equip_lp_woodland_neg500',
     'LP_EQUIP_DELTA_NEG_500 = -500 (s32); Woodland Sprite / Goblin Thief opp side (distinct domain from SCORE_DELTA_NEG_500)'),
    (0x080651d4, 0xfffffb50, 'LP_EQUIP_DELTA_NEG_1200',
     'write_equip_lp_gk_cannon_neg1200',
     'LP_EQUIP_DELTA_NEG_1200 = -1200 (s32); Toon Cannon Soldier / Secret Barrel range'),
    (0x080651e8, 0xfffffce0, 'LP_EQUIP_DELTA_NEG_800',
     'write_equip_lp_dragon_gunfire_neg800',
     'LP_EQUIP_DELTA_NEG_800 = -800 (s32); Dragon Gunfire shared path'),
    (0x080653bc, 0xfffffa24, 'LP_EQUIP_DELTA_NEG_1500',
     'write_equip_lp_inferno_neg1500',
     'LP_EQUIP_DELTA_NEG_1500 = -1500 (s32); Inferno equip penalty'),
    (0x080653e4, 0xfffff448, 'LP_EQUIP_DELTA_NEG_3000',
     'write_equip_lp_blasting_ruins_neg3000',
     'LP_EQUIP_DELTA_NEG_3000 = -3000 (s32); Blasting the Ruins penalty'),
    (0x080653f8, 0xfffff830, 'LP_EQUIP_DELTA_NEG_2000',
     'write_equip_lp_granadora_atk_neg2000',
     'LP_EQUIP_DELTA_NEG_2000 = -2000 (s32); Granadora attack-position penalty'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    PTR_gP1LifePoints_* -> descriptive lp_base labels
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080645e4, 'check_equip_target_lp_base',
     'gP1LifePoints ptr for check_slot_equip_target_has_field5 LP base'),
    (0x08065144, 'write_equip_lp_des_koala_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_scaled_by_lp_count Des Koala path LP base'),
    (0x08065170, 'write_equip_lp_alt_player_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_by_alt_player LP base'),
    (0x08065254, 'write_equip_lp_minar_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_minar LP base'),
    (0x08065290, 'write_equip_lp_wave_cannon_lp_base_a',
     'gP1LifePoints ptr for write_equip_lp_delta_wave_cannon P1 LP base'),
    (0x080652b8, 'write_equip_lp_wave_cannon_lp_base_b',
     'gP1LifePoints ptr for write_equip_lp_delta_wave_cannon P2 LP base'),
    (0x080652ec, 'write_equip_lp_greed_lp_base_a',
     'gP1LifePoints ptr for write_equip_lp_delta_scaled_by_lp_count Greed P1 LP base'),
    (0x08065320, 'write_equip_lp_greed_lp_base_b',
     'gP1LifePoints ptr for write_equip_lp_delta_scaled_by_lp_count Greed P2 LP base'),
    (0x08065344, 'write_equip_lp_secret_barrel_lp_base',
     'gP1LifePoints ptr for write_equip_lp_secret_barrel LP base'),
    (0x08065378, 'write_equip_lp_snatch_steal_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_snatch_steal LP base'),
    (0x080653a8, 'write_equip_lp_guardian_joan_lp_base',
     'gP1LifePoints ptr for write_equip_lp_delta_guardian_joan LP base'),
    (0x0806541c, 'write_equip_lp_vandalgyon_lp_base_a',
     'gP1LifePoints ptr for write_equip_lp_delta_vandalgyon P1 LP base'),
    (0x08065444, 'write_equip_lp_vandalgyon_lp_base_b',
     'gP1LifePoints ptr for write_equip_lp_delta_vandalgyon P2 LP base'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replace stale FUN_ references in existing plate comments.
#    All text must be pure ASCII.
#
#    Stale FUN_ names to replace in Seg-1 (0x643e0..0x6544c) scope:
#      FUN_08064880  -> dispatch_equip_lp_delta_by_card_id  (13 occurrences)
#      FUN_080714ec  -> dispatch_equip_zone11_target_by_activation_state (1 occurrence)
#      FUN_080655da  -> restore_equip_effect_frame  (4 occurrences)
#
#    Entries: (func_addr_of_plate, old_stale_text, new_current_name)
#    Multiple stale names in same plate -> multiple entries for same func_addr.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # submit_equip_zone_bitmap_pair_update @ 0x08064660: FUN_080714ec
    (0x08064660, 'FUN_080714ec', 'dispatch_equip_zone11_target_by_activation_state'),

    # dispatch_equip_sprite_update_by_card_type @ 0x08064760: FUN_08064880
    (0x08064760, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_by_opponent_side @ 0x0806505c: FUN_08064880 + FUN_080655da
    (0x0806505c, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    (0x0806505c, 'FUN_080655da', 'restore_equip_effect_frame'),

    # write_equip_lp_delta_by_own_side @ 0x080650bc: FUN_08064880 + FUN_080655da
    (0x080650bc, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    (0x080650bc, 'FUN_080655da', 'restore_equip_effect_frame'),

    # write_equip_lp_delta_scaled_by_lp_count @ 0x0806514c: FUN_08064880
    (0x0806514c, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_by_alt_player @ 0x080651d8: FUN_08064880 + FUN_080655da
    (0x080651d8, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    (0x080651d8, 'FUN_080655da', 'restore_equip_effect_frame'),

    # write_equip_lp_delta_negated_atk @ 0x080651ec: FUN_08064880 + FUN_080655da
    (0x080651ec, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
    (0x080651ec, 'FUN_080655da', 'restore_equip_effect_frame'),

    # write_equip_lp_delta_minar @ 0x0806525c: FUN_08064880
    (0x0806525c, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_ka2_des_scissors @ 0x08065348: FUN_08064880
    (0x08065348, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_inferno @ 0x080653ac: FUN_08064880
    (0x080653ac, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_fuhma_shuriken @ 0x080653c0: FUN_08064880
    (0x080653c0, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_blasting_the_ruins @ 0x080653d4: FUN_08064880
    (0x080653d4, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),

    # write_equip_lp_delta_goblin_thief @ 0x0806544c: FUN_08064880
    (0x0806544c, 'FUN_08064880', 'dispatch_equip_lp_delta_by_card_id'),
]

# ---------------------------------------------------------------------------
# D. FILE HEADER MOJIBAKE REWRITE
#    asm/08 file header (0x080643e0) plate has CJK mojibake comment.
#    Rewrite to pure ASCII.
# ---------------------------------------------------------------------------
FILE_HEADER_ADDR = 0x080643e0
FILE_HEADER_ASCII = (
    '@ neo daedalus eligibility + equip OAM write + zone tile count'
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- WARN treated as FAIL" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment (ASCII only)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))


def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if not bad:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
            else:
                print("[WARN] non-ASCII in RENAME EOL @ 0x%08x -- skipping EOL" % slot_addr)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))


def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    # ASCII guard
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix text @ 0x%08x -- skipping" % func_addr)
            return

    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment -- FAIL" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate -- FAIL" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))


def _rewrite_file_header(addr, ascii_text):
    """Rewrite file header EOL/plate at addr to pure ASCII (remove mojibake)."""
    bad = any(ord(ch) > 127 for ch in ascii_text)
    if bad:
        print("[FAIL] _rewrite_file_header: non-ASCII in replacement text!")
        return
    a = _addr(addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] _rewrite_file_header 0x%08x: no code unit" % addr)
        return

    if DRY:
        print("[dry] FILE_HEADER_REWRITE 0x%08x -> '%s'" % (addr, ascii_text))
        return

    # Check and fix existing EOL (may contain CJK mojibake)
    existing_eol = cu.getComment(CodeUnit.EOL_COMMENT)
    if existing_eol is not None:
        bad_existing = any(ord(ch) > 127 for ch in existing_eol)
        if bad_existing:
            cu.setComment(CodeUnit.EOL_COMMENT, ascii_text)
            print("[HDR] 0x%08x: rewrote mojibake EOL to ASCII" % addr)
        else:
            print("[HDR] 0x%08x: EOL already ASCII, no change needed" % addr)
    else:
        cu.setComment(CodeUnit.EOL_COMMENT, ascii_text)
        print("[HDR] 0x%08x: set ASCII EOL header" % addr)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg1Slots (DRY=%s) ===" % DRY)
    print("  Seg-1: 0x080643e0..0x0806544c")
    print("  EQ=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        mem = currentProgram.getMemory()
        a = _addr(slot_addr)
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
            if actual != (value & 0xFFFFFFFF):
                eq_fail += 1
                print("[FAIL] 0x%08x (%s): rom=0x%08x expect=0x%08x" % (
                    slot_addr, eq_name, actual, value & 0xFFFFFFFF))
                continue
        except Exception as e:
            eq_fail += 1
            print("[FAIL] 0x%08x (%s): read error %s" % (slot_addr, eq_name, e))
            continue
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- check values before real run !!!" % eq_fail)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    plate_fail = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        # Pre-check: plate exists and contains old_text
        a = _addr(func_addr)
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is None:
            print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
            plate_fail += 1
            continue
        existing = cu.getComment(CodeUnit.PLATE_COMMENT)
        if existing is None:
            print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
            plate_fail += 1
            continue
        if old_text not in existing:
            print("[WARN] plate_fix 0x%08x: '%s' not found -- FAIL" % (func_addr, old_text))
            plate_fail += 1
            continue
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d ok, %d fail" % (plate_ok, plate_fail))
    if plate_fail > 0:
        print("  !!! %d PLATE FAILURES -- check addresses !!!" % plate_fail)

    # D. FILE HEADER REWRITE
    print("\n--- D. FILE HEADER ASCII REWRITE ---")
    _rewrite_file_header(FILE_HEADER_ADDR, FILE_HEADER_ASCII)

    print("\n=== RefineF08Seg1Slots DONE ===")
    print("  EQ=%d/%d ok  RENAME=%d  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS), ren_ok, plate_ok, len(PLATE_REWRITES)))


main()
