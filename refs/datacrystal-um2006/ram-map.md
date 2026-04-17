# Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006 — RAM map

> 来源: https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/RAM_map
> 抓取日期: 2026-04-17

## EWRAM

| Address | Size | Description |
|---------|------|-------------|
| 2000008 | 4160 | Cards / "New" icon |
| 2006C2C | 1 | Various settings, including Language |
| 2006C38 | 4 | Money (DP) |
| 2006C3C | 140 | Duel Puzzle times + completion status<br/>35 × 4 bytes, 0x34BB13 means the puzzle is not completed<br/>Byte 1 has the completion flags in the least significant bits<br/>bit 1: Completed<br/>bit 2: Failed<br/>bit 1+2: Not completed<br/>If neither of these flags are set, a fail-safe will reinitialize the value as 0x34BB13 |
| 2006CC8 | 164 | Limited duels times + completion status<br/>41 × 4 bytes, 0x34BB13 means the puzzle is not completed<br/>Byte 1 has the completion flags in the least significant bits<br/>bit 1: Completed<br/>bit 2: Failed<br/>bit 1+2: Not completed<br/>A value of 0 means the limited duel is not yet unlocked |
| 2006D6C | 200 | Theme Duel scores + completion status<br/>50 × 4 bytes<br/>Byte 1 has the completion flags in the least significant bits<br/>bit 1: Completed<br/>bit 2: Failed<br/>bit 1+2: Not completed<br/>If neither of these flags are set, a fail-safe will set bits 1 and 2<br/>The other bits on byte 1 with the 3 other bytes are the high score |
| 2006E48 | 14 | Player's Name |
| 2006E5C | 8 | Unlocked Duelists |
| 2006E60 | 108 | Player Wins |
| 2006E60 | 4 | Wins vs Kuriboh |
| 2006E64 | 4 | Wins vs Scapegoat |
| 2006E68 | 4 | Wins vs Skull Servant |
| 2006E6C | 4 | Wins vs Watapon |
| 2006E70 | 4 | Wins vs White Magician Pikeru |
| 2006E74 | 4 | Wins vs Batteryman C |
| 2006E78 | 4 | Wins vs Ojama Yellow |
| 2006E7C | 4 | Wins vs Goblin King |
| 2006E80 | 4 | Wins vs Des Frog |
| 2006E84 | 4 | Wins vs Water Dragon |
| 2006E88 | 4 | Wins vs Red-Eyes Darkness Dragon |
| 2006E8C | 4 | Wins vs Vampire Genesis |
| 2006E90 | 4 | Wins vs Infernal Flame Emperor |
| 2006E94 | 4 | Wins vs Ocean Dragon Lord - Neo-Daedalus |
| 2006E98 | 4 | Wins vs Helios Duo Megiste |
| 2006E9C | 4 | Wins vs Gilford the Legend |
| 2006EA0 | 4 | Wins vs Dark Eradicator Warlock |
| 2006EA4 | 4 | Wins vs Guardian Exode |
| 2006EA8 | 4 | Wins vs Goldd, Wu-Lord of Dark World |
| 2006EAC | 4 | Wins vs Elemental Hero Erikshieler |
| 2006EB0 | 4 | Wins vs Raviel, Lord of Phantasms |
| 2006EB4 | 4 | Wins vs Horus the Black Flame Dragon LV8 |
| 2006EB8 | 4 | Wins vs Stronghold |
| 2006EBC | 4 | Wins vs Sacred Phoenix of Nephtys |
| 2006EC0 | 4 | Wins vs Cyber End Dragon |
| 2006EC4 | 4 | Wins vs _Player_ |
| 2006EC8 | 4 | Wins vs Copycat |
| 2006E57 | 1 | Player's Icon |
| 201C4E0 | 2 | P1 Life Points |
| 201CD48 | 2 | P2 Life Points |
| 2029512 | 14 | Player's Name (Name Entry) |
| 2029810 | 1440 | Banlist Password<br/>xx yy<br/>xx = charset<br/>yy = character id |

## IWRAM

| Address | Size | Description |
|---------|------|-------------|
| 3000040 | 4 | PRNG |
| 3000240 | 4 | Frame counter |
