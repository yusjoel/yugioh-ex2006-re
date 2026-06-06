@ =============================================================================
@ Name-input / banlist page constants (NameInput/Name_main.c, PassInput/Pass_main.c)
@ =============================================================================

@ bios_cpu_set fill-zero control words
.equ CHAR_FRAME_DECODE_CPUSET_CTRL, 0x01000168  @ fill 0x168 halfwords (360 x 2B = 720B)
                                                 @ used by decode_char_frame_to_vram to zero stack buf
.equ NAME_INPUT_STATE_CPUSET_CTRL,  0x050000c9  @ fill+32bit 0xc9 words (201 x 4B = 804B)
                                                 @ used by name_input_page_init to zero gState

@ BG layer control register init values for name-input page
.equ NAME_INPUT_BG0CNT_INIT, 0x00001c02  @ BG0: pri=2 scrbase=28 charbase=0 16col 32x32
.equ NAME_INPUT_BG1CNT_INIT, 0x00001d8c  @ BG1: pri=0 scrbase=29 charbase=3 256col 32x32
.equ NAME_INPUT_BG2CNT_INIT, 0x00001e8d  @ BG2: pri=1 scrbase=30 charbase=3 256col 32x32
.equ NAME_INPUT_BG3CNT_INIT, 0x00001f8f  @ BG3: pri=3 scrbase=31 charbase=3 256col 32x32

@ gSettings base+offset split (used in load_game_str_*_to_state funcs)
.equ GSETTINGS_OFFSET, 0x00006c2c        @ offset of gSettings from EWRAM_BASE

@ bios_cpu_fast_set / bios_cpu_set control words for BG/char VRAM clear
.equ NAME_INPUT_BG0_SCREEN_CLEAR_CTRL, 0x01000200  @ bios_cpu_fast_set: fill 0x200 halfwords -> BG0 screen VRAM (32x32 tiles, 2048B)
.equ NAME_INPUT_CHAR_VRAM_CLEAR_CTRL,  0x01001800  @ bios_cpu_fast_set: fill 0x1800 halfwords -> char VRAM (6144 tiles x 4B = 24576B)
.equ NAME_INPUT_BG_ROW_CLEAR_CTRL,     0x05000160  @ bios_cpu_set: copy 0x160=352 words=1408B -> clear one BG row (44 tiles x 32B)
