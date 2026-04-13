# GDB script: watch DMA3 source address register to catch any DMA3 transfer
#
# GBA DMA3 registers (all at 0x04000000 base):
#   0x040000D0: DMA3SAD  - Source Address (written by CPU before transfer)
#   0x040000D4: DMA3DAD  - Destination Address
#   0x040000D8: DMA3CNT_L - Word Count
#   0x040000DA: DMA3CNT_H - Control (write triggers DMA)
#
# Strategy: watch DMA3SAD write -> captures moment CPU sets up DMA source
# At trigger: r0/r1 = value being written (ROM source addr), PC = setup code
#
# Goal: catch any DMA3 source address write (one trigger = success)
set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

echo \n[GDB] Connected\n
info registers pc

watch *(unsigned int*)0x040000D0

echo \n[GDB] Watching DMA3SAD (0x040000D0)\n
echo [GDB] Waiting for first DMA3 trigger...\n

define hook-stop
  echo \n=== DMA3SAD WRITE CAPTURED ===\n
  info registers pc lr r0 r1 r2 r3
  echo --- DMA3 registers (D0=SAD D4=DAD D8=CNT) ---\n
  x/4xw 0x040000D0
end

continue

echo \n[GDB] Done - one DMA3 trigger captured.\n
quit