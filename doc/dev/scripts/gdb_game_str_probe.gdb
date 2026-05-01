set pagination off
set print pretty off
set confirm off

target remote localhost:2345

echo === Setting hbreak on game_str_id_to_row ===\n
hbreak *0x080f4e18

echo === continuing... ===\n

define hit_info
  printf "id=0x%04x  lr=0x%08x\n", $r0 & 0xffff, $lr
end

continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info
continue
hit_info

kill
quit
