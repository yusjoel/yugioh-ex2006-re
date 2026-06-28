@ =============================================================================
@ PRNG (Linear Congruential Generator) constants
@ Source: asm/12_equip_activation_scan.s, Seg-1 advance_prng_state [0x0809463c]
@   Implements classic C rand() LCG: seed = seed * LCG_MUL_343FD + LCG_INC_269EC3
@ C5 grep verified: 0x343fd/0x269ec3 -> 0 hits in constants/ before adding
@ =============================================================================

.equ LCG_MUL_343FD,    0x000343fd  @ LCG multiplier (standard C rand() parameter); advance_prng_state: seed *= 0x343fd; 13 ROM refs; C5 grep=0; conf: high
.equ LCG_INC_269EC3,   0x00269ec3  @ LCG increment (standard C rand() parameter); advance_prng_state: seed += 0x269ec3; 13 ROM refs; C5 grep=0; conf: high
