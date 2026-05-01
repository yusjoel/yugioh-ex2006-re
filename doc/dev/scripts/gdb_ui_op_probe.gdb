set pagination off
set print pretty off
set confirm off

target remote localhost:2345

echo === Setting hbreak on render_duel_field_zone_info ===\n
hbreak *0x080cb998

echo === continuing... ===\n

define hit_info
  echo \n----- HIT -----\n
  printf "pc =0x%08x  lr=0x%08x\n", $pc, $lr
  printf "r0 =0x%08x  r1=0x%08x  r2=0x%08x  r3=0x%08x\n", $r0, $r1, $r2, $r3
  printf "r4 =0x%08x  r5=0x%08x  r6=0x%08x  r7=0x%08x\n", $r4, $r5, $r6, $r7
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

kill
quit
