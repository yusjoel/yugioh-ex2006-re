# Duel Field

> 所属文档: [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)  
> Sheet 编号: 4  
> 原始作者: Scrub Busted（YouTube: [@scrubbusted](https://www.youtube.com/@scrubbusted)）

---

|  |  | Image in Tile Mole | Tilemap Location in HxD | Palette Location in APE | Palette Decimal |  |  | Location in HxD |  |
|---|---|---|---|---|---|---|---|---|---|
|  | Campgin Inner Field | 0185D720 |  | 018674A0 | 25588896 |  | Inner Field Images Pointer Table |  |  |
|  | Campaign Outer Field | 0185504C | 0185B650 | 018593A8 | 25531304 |  | Inner Field Tile Map Pointer Table |  |  |
|  | Link Duel Inner Field | 0185EDA0 |  | 018674C0 | 25588928 |  | Inner Field Palette Pointer Table |  |  |
|  | Link Duel Outer Field | 01855A2C | 0185BB00 | 018593E8 | 25531368 |  | Outer Field Images Pointer Table | 01855030 | Outer fields use the same tileset and palette but have 2 tilemaps: |
|  | Duel Puzzle Inner Field | 01860420 |  | 018674E0 | 25588960 |  | Outer Field Tile Map Pointer Table | 0185B634 | One for the outer field itself |
|  | Duel Puzzle Outer Field | 0185600C | 185BFB0 | 01859428 | 25531432 |  | Outer Phases/LP Tilemap Pointer Table | 01859548 | One for the phases/life poitns |
|  | Limited Duel Inner Field | 01861AA0 |  | 01867500 | 25588992 |  | Outer Field Palette Pointer Table | 0185936C |  |
|  | Limited Duel Outer Field | 018567EC | 0185C460 | 01859468 | 25531496 |  |  |  |  |
|  | Theme Duel Inner Field | 01863120 |  | 01867520 | 25589024 |  |  |  |  |
|  | Theme Duel Outer Field | 018575CC | 0185C910 | 018594A8 | 25531560 |  |  |  |  |
|  | Survival Mode Inner Field | 018647A0 |  | 01867540 | 25589056 |  |  |  |  |
|  | Survival Mode Outer Field | 01857FAC | 0185CDC0 | 018594E8 | 25531624 |  |  |  |  |
|  | Campaign Duel Data Field | 0185504C |  |  |  |  |  |  |  |
|  | Link Duel Data Field |  |  |  |  |  |  |  |  |
|  | Duel Puzzle Data Field |  |  |  |  |  |  |  |  |
|  | Limited Duel Data Field |  |  |  |  |  |  |  |  |
|  | Theme Duel Data Field |  |  |  |  |  |  |  |  |
|  | Survival Duel Data Field |  |  |  |  |  |  |  |  |
|  | Player Icon BG Color |  |  |  |  |  |  |  |  |
|  | Phases Highlight Color | 018519FC |  |  |  |  |  |  |  |
|  | Life Points Font | 01850B1C | Uses Palette 0 | Life Points Color Possible Locations : 185938C |  |  |  |  |  |
|  | Number Font Color for Deck count, turn count : 185159D |  |  |  |  | 18593CC |  |  |  |
|  |  |  |  |  |  | (search for string : 1F 00 1F 7C E0 03 E0 7F FF 03 FF 7F |  |  |  |
|  | Phases Tilemaps | 01859548 |  |  |  |  |  |  |  |
|  | Phases Map? | 0185B184 |  |  |  |  |  |  |  |
|  | Phase Highlights Object Palette | 18515DC - 18515FB |  |  |  |  |  |  |  |
|  | Opponent Phase Object Palette |  |  |  |  |  |  |  |  |
