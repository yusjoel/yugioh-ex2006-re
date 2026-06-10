@ =============================================================================
@ Bit-manipulation algorithm constants
@ Used by count_set_bits_in_word (0x08030208) parallel popcount implementation
@ =============================================================================

@ Popcount parallel-reduction masks (standard Hamming weight algorithm)
@ Step 1: 2-bit groups -- count bits pairwise
.equ POPCOUNT_MASK_ODD,   0xaaaaaaaa  @ even-bit pairs mask (bits set every other, hi); 1 Seg-4 use
.equ POPCOUNT_MASK_EVEN,  0x55555555  @ odd-bit pairs mask (bits set every other, lo); 1 use
@ Step 2: 4-bit groups -- sum 2-bit counts
.equ POPCOUNT_MASK_HI2,   0xcccccccc  @ hi nibble-pair mask (bits[3:2] of each group); 1 use
.equ POPCOUNT_MASK_LO2,   0x33333333  @ lo nibble-pair mask (bits[1:0] of each group); 1 use
@ Step 3: 8-bit groups -- sum 4-bit counts
.equ POPCOUNT_MASK_HI4,   0xf0f0f0f0  @ hi-4 mask (upper nibble of each byte); 1 use
.equ POPCOUNT_MASK_LO4,   0x0f0f0f0f  @ lo-4 mask (lower nibble of each byte); 1 use
@ Step 4: 16-bit groups -- sum 8-bit counts
.equ POPCOUNT_MASK_HI8,   0xff00ff00  @ hi-8 mask (upper byte of each halfword); 1 use
.equ POPCOUNT_MASK_LO8,   0x00ff00ff  @ lo-8 mask (lower byte of each halfword); 1 use
@ Step 5: final merge -- OAM_ATTR0_HIDDEN (0x0000ffff, oam_attr.inc) reused for MASK_LO16
