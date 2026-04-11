# Tool Development

> 所属文档: [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)  
> Sheet 编号: 10  
> 原始作者: 不详（公开文档）

---

| Give it a file interpret this as hex translate to ascii card lists with codes import ydk | starter decks Opponent decks challenge decks ban lists pack lists | starting deck names | Radio buttons break password machine patch arts patch huge revolution language deleter |  | Duel puzzles unlock conditions | to add: Restore Defaults OCG artwork options check for fusiosn check for symbols in names |  | dec | to hex |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | opponent names |  |  |  |  | Check when the .ydk is located for card parameters |  | 28 | 1C |  |  |  |  |
|  | deck names |  |  |  |  | Dont overwrite until submit is clicked |  |  |  |  |  |  |  |
|  | duelist titles |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Campaign +level 1, level 2, level 3 etc |  |  |  |  |  |  |  |  |  |  |  |  |
|  | duel rewards |  |  |  |  |  |  |  |  |  |  |  |  |
|  | pack costs |  |  |  |  |  |  |  |  |  |  |  |  |
|  | starting dp |  |  |  |  |  |  |  |  |  |  |  |  |
|  | change "licensed by nintendo" |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | Variables in Prompt |  |  |  |  |  |  |  |
|  | Immediate to do |  |  |  |  | "Card Passwords" |  |  |  |  |  |  |  |
|  | Address Padding |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Empty Space | Yak patch empty space start | 162248B |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | After relocating |  |  |  |  |  |  |  |
|  | Pointers to structure decks | Change Address to: | Change Slots to |  |  | Start (hex) | End (hex) | Size |  |  |  |  |  |
|  | 01E5FD54 | 1622490h | 37h |  | 1 | 1622490h | 162256Bh | DCh |  |  |  |  |  |
|  | 01E5FD5C | 162256Ch | 37h |  | 2 | 162256Ch | 1622647h | DCh |  |  |  |  |  |
|  | 01E5FD64 | 1622648h | 37h |  | 3 | 1622648h | 1622723h | DCh |  |  |  |  |  |
|  | 01E5FD6C | 1622724h | 37h |  | 4 | 1622724h | 16227FFh | DCh |  |  |  |  |  |
|  | 01E5FD74 | 1622800h | 37h |  | 5 | 1622800h | 16228DBh | DCh |  |  |  |  |  |
|  | 01E5FD7C | 16228DCh | 37h |  | 6 | 16228DCh | 16229B7h | DCh |  |  |  |  |  |
|  | Leaves 55 slots for each | ends at 16229B7 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | first foreign word at 1DCF486 |  |  |  |  |  |  |  |  |  |
| Address | Default Pointer Value (Hex) | Change to | Name Locations | New Location (foreign names sacrifice) |  |  |  |  |  |  |  |  |  |
| 4CC4 | 10346 | 1BA66 | 1DC9F56 | 1DD5676 |  |  |  |  |  |  |  |  |  |
| 4CDC | 10354 | 1BA86 | 1DC9F64 | 1DD5696 |  |  |  |  |  |  |  |  |  |
| 4CF4 | 10364 | 1BAA6 | 1DC9F74 | 1DD56B6 |  |  |  |  |  |  |  |  |  |
| 4D0C | 10378 | 1BAC6 | 1DC9F88 | 1DD56C6 |  |  |  |  |  |  |  |  |  |
| 4D24 | 1038C | 1BAE6 | 1DC9D9C | 1DD56E6 |  |  |  |  |  |  |  |  |  |
| 4D3C | 1039E | 1BB06 | 1DC9FAE | 1DD5706 |  |  |  |  |  |  |  |  |  |
|  | Leave 27 (1Ch) characters for each name, leave 00 as padd for 28 |  |  |  |  |  |  |  |  |  |  |  |  |
| Address | Write values starting at address |  |  |  |  |  |  |  |  |  |  |  |  |
| 4CC4 | 1BA66 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4CDC | 1BA86 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4CF4 | 1BAA6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4D0C | 1BAC6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4D24 | 1BAE6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4D3C | 1BB06 |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD54 | 1622490h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD5C | 162256Ch |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD64 | 1622648h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD6C | 1622724h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD74 | 1622800h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD7C | 16228DCh |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD58 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD60 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD68 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD70 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD78 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
| 01E5FD80 | 37h |  |  |  |  |  |  |  |  |  |  |  |  |
