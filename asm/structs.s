/* Struct definitions exported from Ghidra */
/* Program: 2343.gba */
/* Language ID: ARM:LE:32:v4t */

/* struct GBA_CARTR_HEADER size=0xc0 */
.struct 0
GBA_CARTR_HEADER_h_rom_entry_point = .
.space 4    @ dword
GBA_CARTR_HEADER_h_nintendo_logo = .
.space 156    @ byte[156]
GBA_CARTR_HEADER_h_game_title = .
.space 12    @ string
GBA_CARTR_HEADER_h_game_code = .
.space 4    @ string
GBA_CARTR_HEADER_h_maker_code = .
.space 2    @ char[2]
GBA_CARTR_HEADER_h_fixed_value = .
.space 1    @ byte
GBA_CARTR_HEADER_h_main_unit_code = .
.space 1    @ byte
GBA_CARTR_HEADER_h_device_type = .
.space 1    @ byte
GBA_CARTR_HEADER_h_reserved = .
.space 7    @ byte[7]
GBA_CARTR_HEADER_h_software_vers = .
.space 1    @ byte
GBA_CARTR_HEADER_h_complement_check = .
.space 1    @ byte
GBA_CARTR_HEADER_h_reserved2 = .
.space 2    @ byte[2]
GBA_CARTR_HEADER_SIZE = .
.endstruct

/* End */
