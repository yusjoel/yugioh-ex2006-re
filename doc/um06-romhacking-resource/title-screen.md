# Title Screen

> 所属文档: [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)  
> Sheet 编号: 7  
> 原始作者: 不详（公开文档）

---

| 01EC33DC | Compressed Memory |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
|  | Uses lz77 uncompression |  |  |  |  |  |  |  |  |  |
|  |  | uncompressedRamSection.bin breakdown |  |  |  |  |  |  |  |  |
|  |  | 00000000 - 00000020 | Palette Header Data (doesnt change? maybe total size) |  |  |  |  |  |  |  |
|  |  | 00000020 - 00000220 | Palletes |  |  |  |  |  |  |  |
|  |  | 00000220 - 00000239 | Tile header data |  |  |  |  |  |  |  |
|  |  | 0000023C - 000006EB | Tile identifiers |  |  |  |  |  |  |  |
|  |  | 000006EC - 000031AB | Tiles |  |  |  |  |  |  | paste starting there |
|  |  | unused? |  |  |  |  |  |  |  |  |
|  |  | 000031AC - 0000340F | ? DFPL |  |  |  | in actual mem its at 0200E110 |  |  |  |
|  | solved: |  |  |  |  |  |  |  |  |  |
|  | make backgrounds and export palette |  |  |  |  |  |  |  |  |  |
|  | import backgrounds in tilemap studio, save the png tilemap and then save the tile identifier data as a .bin |  |  |  |  |  |  |  |  |  |
|  | open palette in APE, open any rom (don't need to replace) |  |  |  |  |  |  |  |  |  |
|  | open ram template in HxD ("uncompressed ram section" in gitlz > close sample) |  |  |  |  |  |  |  |  |  |
|  | manually type in the color codes into the hex editor (already in reverse format) |  |  |  |  |  |  |  |  |  |
|  | copy and paste the tile identifier data |  |  |  |  |  |  |  |  |  |
|  | save the ram template in HxD |  |  |  |  |  |  |  |  |  |
|  | Open ram template in tile mole |  |  |  |  |  |  |  |  |  |
|  | resize and copy from file the tilemap png, place and save |  |  |  |  |  |  |  |  |  |
|  | open GBA crusher and select the ram template, LZ77 VRAM safe |  |  |  |  |  |  |  |  |  |
