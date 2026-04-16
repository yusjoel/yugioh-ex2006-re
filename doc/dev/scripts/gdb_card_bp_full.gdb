set pagination off
set print pretty off

target remote localhost:2345

echo === Setting hardware breakpoints ===\n

# BP1: card_info_page_init_bg0 (writes BG0CNT=0x86)
hbreak *0x0801d45c
# BP2: card_image_decode_wrapper (reads card attrs + calls 6bpp decoder)
hbreak *0x0801d998
# BP3: decode_card_image_6bpp (the actual 6bpp tile decoder)
hbreak *0x0801d290

echo === 3 hbreaks set. Continuing to let game run... ===\n
continue

echo \n========================================\n
echo === HIT 1 ===\n
info registers
echo \n--- Disassembly at PC ---\n
x/12i $pc
echo \n--- Continuing to next breakpoint ---\n
continue

echo \n========================================\n
echo === HIT 2 ===\n
info registers
echo \n--- Disassembly at PC ---\n
x/12i $pc
echo \n--- Continuing to next breakpoint ---\n
continue

echo \n========================================\n
echo === HIT 3 ===\n
info registers
echo \n--- Disassembly at PC ---\n
x/12i $pc
echo \n--- Key memory reads ---\n
echo card_select struct at 0x0201AFB0:\n
x/8x 0x0201AFB0
echo \nBG0CNT at 0x04000008:\n
x/1h 0x04000008
echo \nVRAM first tile at 0x06004000:\n
x/4x 0x06004000

echo \n=== All 3 breakpoints captured. ===\n
kill
quit
