# Banlist Code Breaking

> 所属文档: [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)  
> Sheet 编号: 9  
> 原始作者: Scrub Busted（YouTube: [@scrubbusted](https://www.youtube.com/@scrubbusted)）

---

|  |  | 0202A4D8 080FE866 080FE87A Result If you change the byte at 000FE87A from 03 to 01 (or anything) then it will break that function Icon for banlist code entry | index/cursor within forb/lmtd menu Instruction reading index selection when A is pressed (line breakpoint here) Compares index to 3 (represents the password entry as the 4th option) 000FE87A |  |  |  |
|---|---|---|---|---|---|---|
|  |  | Palette | 1E314B4 - 1E314CF |  | 31659188 | in Decimal |
|  |  | Tile Molester | 01E22874 | (Tilemap start) |  |  |
