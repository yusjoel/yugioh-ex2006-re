@ =============================================================================
@ Field spell ATK bonus constants
@ Source: asm/03_equip_chain_hand.s Seg-4a (0x08037904..0x08037ec0)
@ =============================================================================

@ Row index bias for field_spell_atk_bonus_table
@ table[card_id + FIELD_SPELL_TABLE_IDX_BIAS][field_level] = s16 ATK bonus
@ 6 rows (card_id 0x10f0..0x10f5 = Forest/Wasteland/Mountain/Sogen/Umi/Yami)
.equ FIELD_SPELL_TABLE_IDX_BIAS,  0xffffef10  @ -0x10f0 (s32): card_id + bias = 0-based row index;
                                               @ Forest(0x10f0)->0, Yami(0x10f5)->5;
                                               @ 1 ROM ref (compute_zone_effect_atk_delta)

@ Necrovalley / Harpies Hunting Ground ATK/DEF penalty (s32)
.equ ZONE_EFFECT_ATK_PENALTY_500, 0xfffffe70  @ -500 (s32): ATK/DEF score penalty for opponent
                                               @ Necrovalley / Harpies' Hunting Ground zone effects;
                                               @ 4 ROM refs (compute_zone_effect_atk_delta)
