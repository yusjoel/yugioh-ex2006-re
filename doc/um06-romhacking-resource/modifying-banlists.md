# Modifying Banlists

> 所属文档: [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)  
> Sheet 编号: 8  
> 原始作者: Scrub Busted（YouTube: [@scrubbusted](https://www.youtube.com/@scrubbusted)）

---

|  |  | first instance of ban list card implementation is at 08EF16A (good breakpoint, returns from 80EEFC0) 9E5F6C8 = Pointer table for the banlists? 30 EF E5 09 03000000 3C EF E5 09 0E000000 74 EF E5 09 1B000000 E0 EF E5 09 27000000 7C F0 E5 09 35000000 50 F1 E5 09 39000000 34 F2 E5 09 3E000000 2C F3 E5 09 45000000 40 F4 E5 09 50000000 80 F5 E5 09 53000000 |  | that address has the cards listed out |  | 87 13 58 30 | 01E5EF30 - 01E5EFDE 01E5EFE0 - 01E5F07A 01E5F07C - 01E5F14E 01E5F150 - 01E5F232 01E5F234 - 01E5F329 01E5F32C - 01E5F43C 01E5F440 - 01E5F57E 01E5F580 - 01E5F6CA | no banned cards no banned cards no banned cards no banned cards sept 03? Sept 04! March 05! Sept 05! |
|---|---|---|---|---|---|---|---|---|
|  |  | 09E5EF30 | 30 | default? | the restricted cards listed out, find pointers next |  |  |  |
|  |  |  |  |  |  | right leg of forbidden one 01E5EF40 |  |  |
|  |  | 09E5EF3C | 0E |  |  |  |  |  |
|  |  | 09E5EF74 |  |  |  |  |  |  |
|  |  | leads: |  |  |  |  |  |  |
|  |  | 9E5F714 |  |  |  |  |  |  |
|  |  | Potential banlist zones |  |  |  |  |  |  |
|  |  |  | 01E5EF30 - 01E5F6CA |  |  |  |  |  |
|  |  |  | Potential sub-lists |  |  |  |  |  |
|  |  |  |  | mirage of nightmare at 1 at 09E5F2B3 (sept 03?) |  |  |  |  |
|  |  |  |  | Chick the yellow at 09E5F554 | (march 05) |  |  |  |
|  |  |  |  | united we stand banned at 09E5F354 (sept 04) |  |  |  |  |
|  |  |  | Only |  |  |  |  |  |
