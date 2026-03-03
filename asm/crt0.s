RomBase: @ 8000000
	b Init

	.include "asm/rom_header.s"

    .arm
	.align 2
	.globl Init
Init: @ 80000C0
