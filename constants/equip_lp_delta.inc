@ =============================================================================
@ Equip card LP delta penalty constants (s32, stored in gDuelFieldOutput player slot)
@ Used by dispatch_equip_lp_delta_by_card_id sub-functions (asm/08 Seg-1).
@ Semantically distinct from SCORE_DELTA_* (equip LP penalty vs ATK/DEF score adjustment).
@ Values are two's complement signed 32-bit integers.
@ Source: asm/08_equip_oam_neodaed.s, Seg-1 (0x080643e0..0x0806544c)
@ =============================================================================

.equ LP_EQUIP_DELTA_NEG_300,  0xfffffed4  @ -300 (s32); Legendary Black Belt range path; 6 ROM refs
.equ LP_EQUIP_DELTA_NEG_500,  0xfffffe0c  @ -500 (s32); Woodland Sprite / Goblin Thief opp side; 27 ROM refs
.equ LP_EQUIP_DELTA_NEG_600,  0xfffffda8  @ -600 (s32); Solar Ray per eligible zone; 4 ROM refs
.equ LP_EQUIP_DELTA_NEG_800,  0xfffffce0  @ -800 (s32); Dragon Gunfire shared path; 5 ROM refs
.equ LP_EQUIP_DELTA_NEG_1000, 0xfffffc18  @ -1000 (s32); Atomic Firefly / Mecha-Dog Marron / Marshmallon LP penalty; 3 Seg-2 slots
.equ LP_EQUIP_DELTA_NEG_1200, 0xfffffb50  @ -1200 (s32); Toon Cannon Soldier / Secret Barrel range; 3 ROM refs
.equ LP_EQUIP_DELTA_NEG_1500, 0xfffffa24  @ -1500 (s32); Inferno equip penalty; 1 ROM ref
.equ LP_EQUIP_DELTA_NEG_2000, 0xfffff830  @ -2000 (s32); Granadora attack-position penalty; 8 ROM refs
.equ LP_EQUIP_DELTA_NEG_3000, 0xfffff448  @ -3000 (s32); Blasting the Ruins penalty; 1 ROM ref
