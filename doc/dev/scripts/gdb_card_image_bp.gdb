set pagination off
set print pretty off

target remote localhost:2345

echo === Connected. Setting hardware breakpoints ===\n

# decode_card_image_6bpp entry
hbreak *0x0801d290
# card_image_decode_wrapper entry
hbreak *0x0801d998
# card_info_page_entry
hbreak *0x0801e440
# card_info_page_init_bg0
hbreak *0x0801d45c

echo === 4 hbreaks set. Continuing... ===\n
continue

echo \n=== Breakpoint hit! ===\n
echo --- PC and registers ---\n
info registers
echo \n--- Backtrace attempt ---\n
bt 5
echo \n--- Memory around PC ---\n
x/8i $pc
echo \n=== Done. Disconnecting. ===\n
detach
quit
