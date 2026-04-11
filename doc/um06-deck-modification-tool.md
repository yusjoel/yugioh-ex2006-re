# UM06 Deck Modification Tool 1.0

> **原始标题**: UM06 Deck Modification Tool 1.0  
> **原始网址**: https://docs.google.com/spreadsheets/d/1dXa8EyyL2ozM04TpZb_yAsYO7A98CfKIZacchXT2US8/edit?gid=667998836#gid=667998836  
> **原始作者**: 不详（Google Sheets 公开文档，未标注作者）  

---

## Sheet 1: Home（默认卡组位置）

### Default Decks（预置卡组）

| 卡组名 | 卡组地址 | 指针地址 | 槽位数 |
|--------|----------|----------|--------|
| Dragons Roar | 01E5FA58 | 01E5FD54 | 28 |
| Zombie Madness | 01E5FAC8 | 01E5FD5C | 28 |
| Molten Destruction | 01E5FB38 | 01E5FD64 | 31 |
| Fury from the Deep | 01E5FBB4 | 01E5FD6C | 32 |
| Warrior's Triumph | 01E5FC34 | 01E5FD74 | 36 |
| Spellcaster's Judgement | 01E5FCC4 | 01E5FD7C | 36 |

### True Starter Deck（初始卡组）

> 备注：导出 .ydk 文件，用记事本打开后将内容粘贴到 Google Sheet 中。

| 卡组名 | 卡组地址 | 指针地址 |
|--------|----------|----------|
| Starter Deck | 01E5F884 | 000F4558 |

### Opponents（对手卡组）

| 对手名 | 卡组地址 | 备注 |
|--------|----------|------|
| Kuriboh | 1E6468E |  |
| Scapegoat | 1E6480E |  |
| Skull Servant | 1E648CE |  |
| Watapon | 1E6498E |  |
| Pikeru | 1E6474E |  |
| Batteryman C | 1E64A4E |  |
| Ojama Yellow | 1E64D4E |  |
| Goblin King | 1E64BCE |  |
| Des Frog | 1E64B0E | Fusion Deck: 1 |
| Water Dragon | 1E64E0E |  |
| Red Eyes Darkness D | 1E64ECE |  |
| Vampire Genesis | 1E651CE |  |
| Infernal Flame Emperor | 1E6504E |  |
| Ocean Dragon Lord Neo D | 1E64F8E |  |
| Helios Duos Megiste | 1E6510E |  |
| Gilford | 1E654EE |  |
| Dark Eradicator Warlock | 1E655AE |  |
| Guardian Exode | 1E6542E |  |
| Goldd, Wu-Lord of the D | 1E6536E |  |
| Elemental Hero Electrum | 1E6528E | Fusion Deck: 9 |
| Raviel, Lord of Phantasms | 1E65986 |  |
| Horus the Black Flame D | 1E65806 |  |
| Stronghold | 1E65746 |  |
| Sacred Phoenix of N | 1E658C6 |  |
| Cyber End Dragon | 1E6566E | Fusion Deck: 7 |

---

## Sheet 2: Starter & Opponent Paste Tool（卡组编辑工具）

此 Sheet 是交互工具：在 A 列粘贴卡牌密码（Password），B、C 列自动查找卡名和所属对手/初始卡组的 Hex 编码。
右侧（F-H 列）提供卡名搜索和卡组位置参考表（与 Home sheet 相同）。

**列说明：**

| 列 | 说明 |
|----|------|
| A (Paste Below) | 粘贴卡牌密码 (Password) |
| B (Name) | 自动查找的卡名 |
| C (Opponent & Starter Deck) | 该卡在对手/初始卡组中的 Hex 编码 |
| F (Card Name Lookup) | 输入卡名可反查 |
| G (Password) | 反查结果的密码 |

---

## Sheet 3: Structure Deck Paste Tool（结构卡组编辑工具）

此 Sheet 是交互工具：在 B 列粘贴卡牌密码，C 列输入数量，D、E 列自动查找卡名和结构卡组的 Hex 编码，F 列生成补零格式。

**列说明：**

| 列 | 说明 |
|----|------|
| A (行号) | 序号（最多 191 张，对应最大槽位总数）|
| B (Paste Below) | 粘贴卡牌密码 |
| C (Quantity) | 数量 |
| D (Name) | 自动查找的卡名 |
| E (Structure Decks) | 该卡在结构卡组中的 Hex 编码 |
| F (0 Padder) | 补零后的 4 位 Hex（用于写入 ROM）|

### 结构卡组指针表（Pointers）

| 卡组名 | 槽位数 | 反转格式 (Reverse Format) | 槽位大小 (Hex) | 补零 |
|--------|--------|---------------------------|----------------|------|
| Dragon's Roar | 28 | 58FAE509 | 1C | 000000 |
| Zombie Madness | 28 | C8FAE509 | 1C | 000000 |
| Molten Destruction | 31 | 38FBE509 | 1F | 000000 |
| Fury from the Deep | 32 | B4FBE509 | 20 | 000000 |
| Warrior's Triumph | 36 | 34FCE509 | 24 | 000000 |
| Spellcaster's Judgement | 36 | C4FCE509 | 24 | 000000 |

---

## Sheet 4: Data（卡牌数据库）

完整卡牌列表，包含每张卡的密码、卡名及其在结构卡组/对手卡组中的 Hex 编码。

**列说明：**

| 列 | 说明 |
|----|------|
| Password | 卡牌密码（8位数字）|
| Card Name | 卡名 |
| Structure Decks | 该卡在结构卡组槽中的 Hex 编码（写入 ROM 用）|
| Starter/Opponent | 该卡在初始/对手卡组槽中的 Hex 编码 |
| Reverse Format | Starter/Opponent 的字节反转格式 |

| Password | Card Name | Structure Decks | Starter/Opponent | Reverse Format |
|----------|-----------|-----------------|------------------|----------------|
| 89631139 | Blue-Eyes White Dragon | 3E9C | 0FA7 | A70F |
| 15025844 | Mystical Elf | 3EA0 | 0FA8 | A80F |
| 76184692 | Hitotsu-Me Giant | 3EA4 | 0FA9 | A90F |
| 88819587 | Baby Dragon | 3EA8 | 0FAA | AA0F |
| 15303296 | Ryu-Kishin | 3EAC | 0FAB | AB0F |
| 41392891 | Feral Imp | 3EB0 | 0FAC | AC0F |
| 87796900 | Winged Dragon, Guardian of the Fortress #1 | 3EB4 | 0FAD | AD0F |
| 14181608 | Mushroom Man | 3EB8 | 0FAE | AE0F |
| 87564352 | Blackland Fire Dragon | 3EC0 | 0FB0 | B00F |
| 72842870 | Tyhone | 3ECC | 0FB3 | B30F |
| 45231177 | Flame Swordsman | 3ED4 | 0FB5 | B50F |
| 71625222 | Time Wizard | 3ED8 | 0FB6 | B60F |
| 08124921 | Right Leg of the Forbidden One | 3EDC | 0FB7 | B70F |
| 44519536 | Left Leg of the Forbidden One | 3EE0 | 0FB8 | B80F |
| 70903634 | Right Arm of the Forbidden One | 3EE4 | 0FB9 | B90F |
| 07902349 | Left Arm of the Forbidden One | 3EE8 | 0FBA | BA0F |
| 33396948 | Exodia the Forbidden One | 3EEC | 0FBB | BB0F |
| 70781052 | Summoned Skull | 3EF0 | 0FBC | BC0F |
| 06285791 | The Wicked Worm Beast | 3EF4 | 0FBD | BD0F |
| 32274490 | Skull Servant | 3EF8 | 0FBE | BE0F |
| 69669405 | Horn Imp | 3EFC | 0FBF | BF0F |
| 05053103 | Battle Ox | 3F00 | 0FC0 | C00F |
| 32452818 | Beaver Warrior | 3F04 | 0FC1 | C10F |
| 68846917 | Rock Ogre Grotto #1 | 3F08 | 0FC2 | C20F |
| 04931562 | Mountain Warrior | 3F0C | 0FC3 | C30F |
| 31339260 | Zombie Warrior | 3F10 | 0FC4 | C40F |
| 67724379 | Koumori Dragon | 3F14 | 0FC5 | C50F |
| 94119974 | Two-Headed King Rex | 3F18 | 0FC6 | C60F |
| 30113682 | Judge Man | 3F1C | 0FC7 | C70F |
| 66602787 | Saggi the Dark Clown | 3F20 | 0FC8 | C80F |
| 46986414 | Dark Magician | 3F24 | 0FC9 | C90F |
| 29491031 | The Snake Hair | 3F28 | 0FCA | CA0F |
| 66889139 | Gaia the Dragon Champion | 3F2C | 0FCB | CB0F |
| 06368038 | Gaia The Fierce Knight | 3F30 | 0FCC | CC0F |
| 28279543 | Curse of Dragon | 3F34 | 0FCD | CD0F |
| 91152256 | Celtic Guardian | 3F3C | 0FCF | CF0F |
| 28546905 | Illusionist Faceless Mage | 3F40 | 0FD0 | D00F |
| 54541900 | Karbonala Warrior | 3F44 | 0FD1 | D10F |
| 91939608 | Rogue Doll | 3F48 | 0FD2 | D20F |
| 27324313 | Oscillo Hero #2 | 3F4C | 0FD3 | D30F |
| 53829412 | Griffore | 3F50 | 0FD4 | D40F |
| 80813021 | Torike | 3F54 | 0FD5 | D50F |
| 26202165 | Sangan | 3F58 | 0FD6 | D60F |
| 53606874 | Big Insect | 3F5C | 0FD7 | D70F |
| 89091579 | Basic Insect | 3F60 | 0FD8 | D80F |
| 15480588 | Armored Lizard | 3F64 | 0FD9 | D90F |
| 88979991 | Killer Needle | 3F6C | 0FDB | DB0F |
| 15367030 | Gokibore | 3F70 | 0FDC | DC0F |
| 41762634 | Giant Flea | 3F74 | 0FDD | DD0F |
| 87756343 | Larvae Moth | 3F78 | 0FDE | DE0F |
| 14141448 | Great Moth | 3F7C | 0FDF | DF0F |
| 40640057 | Kuriboh | 3F80 | 0FE0 | E00F |
| 40374923 | Mammoth Graveyard | 3F84 | 0FE1 | E10F |
| 13429800 | Great White | 3F88 | 0FE2 | E20F |
| 49417509 | Wolf | 3F8C | 0FE3 | E30F |
| 76812113 | Harpie Lady | 3F90 | 0FE4 | E40F |
| 12206212 | Harpie Lady Sisters | 3F94 | 0FE5 | E50F |
| 49791927 | Tiger Axe | 3F98 | 0FE6 | E60F |
| 90357090 | Silver Fang | 3F9C | 0FE7 | E70F |
| 01184620 | Kojikocy | 3FA0 | 0FE8 | E80F |
| 48579379 | Perfectly Ultimate Great Moth | 3FA4 | 0FE9 | E90F |
| 41462083 | Thousand Dragon | 3FAC | 0FEB | EB0F |
| 77456781 | Fiend Kraken | 3FB0 | 0FEC | EC0F |
| 14851496 | Jellyfish | 3FB4 | 0FED | ED0F |
| 40240595 | Cocoon of Evolution | 3FB8 | 0FEE | EE0F |
| 13039848 | Giant Soldier of Stone | 3FC0 | 0FF0 | F00F |
| 49127943 | Man-Eating Plant | 3FC4 | 0FF1 | F10F |
| 76512652 | Krokodilus | 3FC8 | 0FF2 | F20F |
| 02906250 | Grappler | 3FCC | 0FF3 | F30F |
| 48305365 | Axe Raider | 3FD0 | 0FF4 | F40F |
| 75390004 | Megazowler | 3FD4 | 0FF5 | F50F |
| 01784619 | Uraby | 3FD8 | 0FF6 | F60F |
| 38289717 | Crawling Dragon #2 | 3FDC | 0FF7 | F70F |
| 74677422 | Red-Eyes B. Dragon | 3FE0 | 0FF8 | F80F |
| 00062121 | Castle of Dark Illusions | 3FE4 | 0FF9 | F90F |
| 33066139 | Reaper of the Cards | 3FE8 | 0FFA | FA0F |
| 69455834 | King of Yamimakai | 3FEC | 0FFB | FB0F |
| 06840573 | Barox | 3FF0 | 0FFC | FC0F |
| 68339286 | Metal Guardian | 3FF8 | 0FFE | FE0F |
| 95727991 | Catapult Turtle | 3FFC | 0FFF | FF0F |
| 31122090 | Gyakutenno Megami | 4000 | 1000 | 0010 |
| 68516705 | Mystic Horseman | 4004 | 1001 | 0110 |
| 94905343 | Rabid Horseman | 4008 | 1002 | 0210 |
| 93889755 | Crass Clown | 4014 | 1005 | 0510 |
| 20277860 | Armored Zombie | 4018 | 1006 | 0610 |
| 66672569 | Dragon Zombie | 401C | 1007 | 0710 |
| 92667214 | Clown Zombie | 4020 | 1008 | 0810 |
| 29155212 | Pumpking the King of Ghosts | 4024 | 1009 | 0910 |
| 55550921 | Battle Warrior | 4028 | 100A | 0A10 |
| 92944626 | Wings of Wicked Flame | 402C | 100B | 0B10 |
| 28933734 | Mask of Darkness | 4030 | 100C | 0C10 |
| 55337339 | Job-Change Mirror | 4034 | 100D | 0D10 |
| 22026707 | Curtain of the Dark Ones | 4038 | 100E | 0E10 |
| 80600490 | Kageningen | 4044 | 1011 | 1110 |
| 27094595 | Graveyard and the Hand of Invitation | 4048 | 1012 | 1210 |
| 53493204 | Goddess with the Third Eye | 404C | 1013 | 1310 |
| 89987208 | Hero of the East | 4050 | 1014 | 1410 |
| 52367652 | That Which Feeds on Life | 4058 | 1016 | 1610 |
| 09159938 | Dark Gray | 405C | 1017 | 1710 |
| 15150365 | White Magical Hat | 4060 | 1018 | 1810 |
| 41544074 | Kamionwizard | 4064 | 1019 | 1910 |
| 88643173 | Nightmare Scorpion | 4068 | 101A | 1A10 |
| 14037717 | Spirit of the Books | 406C | 101B | 1B10 |
| 41422426 | Supporter in the Shadows | 4070 | 101C | 1C10 |
| 77827521 | Trial of Nightmare | 4074 | 101D | 1D10 |
| 13215230 | Dream Clown | 4078 | 101E | 1E10 |
| 40200834 | Sleeping Lion | 407C | 101F | 1F10 |
| 76704943 | Yamatano Dragon Scroll | 4080 | 1020 | 2010 |
| 75582395 | Faith Bird | 408C | 1023 | 2310 |
| 90963488 | Nemuriko | 409C | 1027 | 2710 |
| 37243151 | Weather Control | 40A0 | 1028 | 2810 |
| 00032864 | The 13th Grave | 40A8 | 102A | 2A10 |
| 37421579 | Charubin the Fire Knight | 40AC | 102B | 2B10 |
| 63515678 | Mystical Capture Chain | 40B0 | 102C | 2C10 |
| 52800428 | Fiend's Hand | 40B4 | 102D | 2D10 |
| 36304921 | Witty Phantom | 40B8 | 102E | 2E10 |
| 09197735 | Dragon Statue | 40C0 | 1030 | 3010 |
| 35282433 | Blue-Eyed Silver Zombie | 40C4 | 1031 | 3110 |
| 62671448 | Toad Master | 40C8 | 1032 | 3210 |
| 98075147 | Spiked Snail | 40CC | 1033 | 3310 |
| 34460851 | Flame Manipulator | 40D0 | 1034 | 3410 |
| 61454890 | Necrolancer the Timelord | 40D4 | 1035 | 3510 |
| 97843505 | Djinn the Watcher of the Wind | 40D8 | 1036 | 3610 |
| 24348204 | The Bewitching Phantom Thief | 40DC | 1037 | 3710 |
| 00732302 | Temple of Skulls | 40E0 | 1038 | 3810 |
| 36121917 | Monster Egg | 40E4 | 1039 | 3910 |
| 63125616 | The Shadow Who Controls the Dark | 40E8 | 103A | 3A10 |
| 99510761 | Lord of the Lamp | 40EC | 103B | 3B10 |
| 62403074 | Rhaimundos of the Red Sword | 40F4 | 103D | 3D10 |
| 98898173 | The Melting Red Shadow | 40F8 | 103E | 3E10 |
| 25882881 | Dokuroizo the Grim Reaper | 40FC | 103F | 3F10 |
| 53581214 | Fire Reaper | 4100 | 1040 | 4010 |
| 94675535 | Larvas | 4104 | 1041 | 4110 |
| 20060230 | Hard Armor | 4108 | 1042 | 4210 |
| 53293545 | Firegrass | 410C | 1043 | 4310 |
| 93553943 | Man Eater | 4110 | 1044 | 4410 |
| 29948642 | Dig Beak | 4114 | 1045 | 4510 |
| 56342351 | M-Warrior #1 | 4118 | 1046 | 4610 |
| 92731455 | M-Warrior #2 | 411C | 1047 | 4710 |
| 55210709 | Lisark | 4124 | 1049 | 4910 |
| 81618817 | Lord of Zemia | 4128 | 104A | 4A10 |
| 28003512 | The Judgement Hand | 412C | 104B | 4B10 |
| 54098121 | Mysterious Puppeteer | 4130 | 104C | 4C10 |
| 17881964 | Darkfire Dragon | 4138 | 104E | 4E10 |
| 53375573 | Dark King of the Abyss | 413C | 104F | 4F10 |
| 80770678 | Spirit of the Harp | 4140 | 1050 | 5010 |
| 53153481 | Armaill | 4148 | 1052 | 5210 |
| 89558090 | Dark Prisoner | 414C | 1053 | 5310 |
| 15042735 | Hurricail | 4150 | 1054 | 5410 |
| 88435542 | Fire Eye | 4158 | 1056 | 5610 |
| 15820147 | Monsturtle | 415C | 1057 | 5710 |
| 41218256 | Claw Reacher | 4160 | 1058 | 5810 |
| 77603950 | Phantom Dewan | 4164 | 1059 | 5910 |
| 14708569 | Arlownay | 4168 | 105A | 5A10 |
| 40196604 | Dark Shade | 416C | 105B | 5B10 |
| 77581312 | Masked Clown | 4170 | 105C | 5C10 |
| 03985011 | Lucky Trinket | 4174 | 105D | 5D10 |
| 49370026 | Genin | 4178 | 105E | 5E10 |
| 64511793 | Eyearmor | 417C | 105F | 5F10 |
| 02863439 | Fiend Reflection #2 | 4180 | 1060 | 6010 |
| 49258578 | Gate Deeg | 4184 | 1061 | 6110 |
| 75646173 | Synchar | 4188 | 1062 | 6210 |
| 01641882 | Fusionist | 418C | 1063 | 6310 |
| 38035986 | Akakieisu | 4190 | 1064 | 6410 |
| 09430387 | LaLa Li-oon | 4194 | 1065 | 6510 |
| 37313348 | Turtle Tiger | 419C | 1067 | 6710 |
| 63308047 | Terra the Terrible | 41A0 | 1068 | 6810 |
| 00756652 | Doron | 41A4 | 1069 | 6910 |
| 36151751 | Arma Knight | 41A8 | 106A | 6A10 |
| 99030164 | Happy Lover | 41B0 | 106C | 6C10 |
| 36039163 | Penguin Knight | 41B4 | 106D | 6D10 |
| 75356564 | Petit Dragon | 41B8 | 106E | 6E10 |
| 98818516 | Frenzied Panda | 41BC | 106F | 6F10 |
| 75889523 | Archfiend Marmot of Nefariousness | 41C0 | 1070 | 7010 |
| 61201220 | Phantom Ghost | 41C4 | 1071 | 7110 |
| 24194033 | Dorover | 41CC | 1073 | 7310 |
| 60589682 | Twin Long Rods #1 | 41D0 | 1074 | 7410 |
| 97973387 | Droll Bird | 41D4 | 1075 | 7510 |
| 38142739 | Petit Angel | 41D8 | 1076 | 7610 |
| 39175982 | Winged Cleaver | 41DC | 1077 | 7710 |
| 96851799 | Hinotama Soul | 41E0 | 1078 | 7810 |
| 15510988 | Kaminarikozou | 41E4 | 1079 | 7910 |
| 53832650 | Meotoko | 41E8 | 107A | 7A10 |
| 85639257 | Aqua Madoor | 41EC | 107B | 7B10 |
| 15401633 | Kagemusha of the Blue Flame | 41F0 | 107C | 7C10 |
| 58528964 | Flame Ghost | 41F4 | 107D | 7D10 |
| 84916669 | Dryad | 41F8 | 107E | 7E10 |
| 11901678 | B. Skull Dragon | 41FC | 107F | 7F10 |
| 57305373 | Two-Mouth Darkruler | 4200 | 1080 | 8010 |
| 84794011 | Solitude | 4204 | 1081 | 8110 |
| 10189126 | Masked Sorcerer | 4208 | 1082 | 8210 |
| 56283725 | Kumootoko | 420C | 1083 | 8310 |
| 83678433 | Midnight Fiend | 4210 | 1084 | 8410 |
| 46461247 | Trap Master | 4218 | 1086 | 8610 |
| 22855882 | Fiend Sword | 421C | 1087 | 8710 |
| 54844990 | Skull Stalker | 4220 | 1088 | 8810 |
| 46718686 | Hitodenchak | 4224 | 1089 | 8910 |
| 17733394 | Wood Remains | 4228 | 108A | 8A10 |
| 08783685 | Hourglass of Life | 422C | 108B | 8B10 |
| 80516007 | Rare Fish | 4230 | 108C | 8C10 |
| 17511156 | Wood Clown | 4234 | 108D | 8D10 |
| 43905751 | Madjinn Gunn | 4238 | 108E | 8E10 |
| 89494469 | Dark Titan of Terror | 423C | 108F | 8F10 |
| 16899564 | Beautiful Headhuntress | 4240 | 1090 | 9010 |
| 89272878 | Guardian of the Labyrinth | 4248 | 1092 | 9210 |
| 41061625 | Yashinoki | 4250 | 1094 | 9410 |
| 78556320 | Vishwar Randi | 4254 | 1095 | 9510 |
| 08944575 | The Drdek | 4258 | 1096 | 9610 |
| 41949033 | Dark Assailant | 425C | 1097 | 9710 |
| 47695416 | Candle of Fate | 4260 | 1098 | 9810 |
| 03732747 | Water Element | 4264 | 1099 | 9910 |
| 40826495 | Dissolverock | 4268 | 109A | 9A10 |
| 76211194 | Meda Bat | 426C | 109B | 9B10 |
| 03606209 | One Who Hunts Souls | 4270 | 109C | 9C10 |
| 39004808 | Root Water | 4274 | 109D | 9D10 |
| 75499502 | Master & Expert | 4278 | 109E | 9E10 |
| 02483611 | Water Omotics | 427C | 109F | 9F10 |
| 38982356 | Hyo | 4280 | 10A0 | A010 |
| 75376965 | Enchanting Mermaid | 4284 | 10A1 | A110 |
| 01761063 | Nekogal #1 | 4288 | 10A2 | A210 |
| 37160778 | Fairywitch | 428C | 10A3 | A310 |
| 64154377 | Embryonic Beast | 4290 | 10A4 | A410 |
| 00549481 | Prevent Rat | 4294 | 10A5 | A510 |
| 37043180 | Dimensional Warrior | 4298 | 10A6 | A610 |
| 63432835 | Stone Armadiller | 429C | 10A7 | A710 |
| 99426834 | Beastking of the Swamps | 42A0 | 10A8 | A810 |
| 36821538 | Ancient Sorcerer | 42A4 | 10A9 | A910 |
| 62210247 | Lunar Queen Elzaim | 42A8 | 10AA | AA10 |
| 15150371 | Wicked Mirror | 42AC | 10AB | AB10 |
| 25109950 | The Little Swordsman of Aile | 42B0 | 10AC | AC10 |
| 62193699 | Rock Ogre Grotto #2 | 42B4 | 10AD | AD10 |
| 98582704 | Wing Egg Elf | 42B8 | 10AE | AE10 |
| 18710707 | The Furious Sea King | 42BC | 10AF | AF10 |
| 51371017 | Princess of Tsurugi | 42C0 | 10B0 | B010 |
| 97360116 | Unknown Warrior of Fiend | 42C4 | 10B1 | B110 |
| 15507080 | Sectarian of Secrets | 42C8 | 10B2 | B210 |
| 50259460 | Versago the Destroyer | 42CC | 10B3 | B310 |
| 96643568 | Wetha | 42D0 | 10B4 | B410 |
| 23032273 | Megirus Light | 42D4 | 10B5 | B510 |
| 59036972 | Mavelus | 42D8 | 10B6 | B610 |
| 86421986 | Ancient Tree of Enlightenment | 42DC | 10B7 | B710 |
| 22910685 | Green Phantom King | 42E0 | 10B8 | B810 |
| 58314394 | Ground Attacker Bugroth | 42E4 | 10B9 | B910 |
| 85309439 | Ray & Temperature | 42E8 | 10BA | BA10 |
| 11793047 | Gorgon Egg | 42EC | 10BB | BB10 |
| 58192742 | Petit Moth | 42F0 | 10BC | BC10 |
| 84686841 | King Fog | 42F4 | 10BD | BD10 |
| 10071456 | Protector of the Throne | 42F8 | 10BE | BE10 |
| 47060154 | Mystic Clown | 42FC | 10BF | BF10 |
| 83464209 | Mystical Sheep #2 | 4300 | 10C0 | C010 |
| 10859908 | Holograh | 4304 | 10C1 | C110 |
| 46247516 | Tao the Chanter | 4308 | 10C2 | C210 |
| 82742611 | Serpent Marauder | 430C | 10C3 | C310 |
| 45121025 | Ogre of the Black Shadow | 4314 | 10C5 | C510 |
| 45909477 | Moon Envoy | 4320 | 10C8 | C810 |
| 71407486 | Fireyarou | 4324 | 10C9 | C910 |
| 07892180 | Psychic Kappa | 4328 | 10CA | CA10 |
| 44287299 | Masaki the Legendary Swordsman | 432C | 10CB | CB10 |
| 70681994 | Dragoness the Wicked Knight | 4330 | 10CC | CC10 |
| 07670542 | Bio Plant | 4334 | 10CD | CD10 |
| 33064647 | One-Eyed Shield Dragon | 4338 | 10CE | CE10 |
| 75559356 | Cyber Soldier of Darkworld | 433C | 10CF | CF10 |
| 02957055 | Wicked Dragon with the Ersatz Head | 4340 | 10D0 | D010 |
| 38942059 | Sonic Maid | 4344 | 10D1 | D110 |
| 85705804 | Kurama | 4348 | 10D2 | D210 |
| 40619825 | Axe of Despair | 4358 | 10D6 | D610 |
| 03492538 | Insect Armor with Laser Cannon | 4360 | 10D8 | D810 |
| 65169794 | Black Pendant | 4374 | 10DD | DD10 |
| 38552107 | Horn of Light | 437C | 10DF | DF10 |
| 64047146 | Horn of the Unicorn | 4380 | 10E0 | E010 |
| 90219263 | Elegant Egotist | 4390 | 10E4 | E410 |
| 63102017 | Stop Defense | 4398 | 10E6 | E610 |
| 99597615 | Malevolent Nuzzler | 439C | 10E7 | E710 |
| 50045299 | Dragon Capture Jar | 43BC | 10EF | EF10 |
| 87430998 | Forest | 43C0 | 10F0 | F010 |
| 23424603 | Wasteland | 43C4 | 10F1 | F110 |
| 50913601 | Mountain | 43C8 | 10F2 | F210 |
| 86318356 | Sogen | 43CC | 10F3 | F310 |
| 22702055 | Umi | 43D0 | 10F4 | F410 |
| 59197169 | Yami | 43D4 | 10F5 | F510 |
| 53129443 | Dark Hole | 43D8 | 10F6 | F610 |
| 12580477 | Raigeki | 43DC | 10F7 | F710 |
| 58074572 | Mooyan Curry | 43E0 | 10F8 | F810 |
| 38199696 | Red Medicine | 43E4 | 10F9 | F910 |
| 11868825 | Goblin's Secret Remedy | 43E8 | 10FA | FA10 |
| 47852924 | Soul of the Pure | 43EC | 10FB | FB10 |
| 84257639 | Dian Keto the Cure Master | 43F0 | 10FC | FC10 |
| 76103675 | Sparks | 43F4 | 10FD | FD10 |
| 19523799 | Ookazi | 4400 | 1100 | 0011 |
| 46918794 | Tremendous Fire | 4404 | 1101 | 0111 |
| 72302403 | Swords of Revealing Light | 4408 | 1102 | 0211 |
| 18807108 | Spellbinding Circle | 440C | 1103 | 0311 |
| 45895206 | Dark-Piercing Light | 4410 | 1104 | 0411 |
| 71280811 | Yaranzo | 4414 | 1105 | 0511 |
| 12829151 | Kanan the Swordmistress | 4418 | 1106 | 0611 |
| 44073668 | Takriminos | 441C | 1107 | 0711 |
| 71068263 | Stuffed Animal | 4420 | 1108 | 0811 |
| 33951077 | Super War-Lion | 4428 | 110A | 0A11 |
| 33734439 | Three-Legged Zombies | 4434 | 110D | 0D11 |
| 69123138 | Zera The Mant | 4438 | 110E | 0E11 |
| 05628232 | Flying Penguin | 443C | 110F | 0F11 |
| 32012841 | Millennium Shield | 4440 | 1110 | 1011 |
| 68401546 | Fairy's Gift | 4444 | 1111 | 1111 |
| 05405694 | Black Luster Soldier | 4448 | 1112 | 1211 |
| 31890399 | Fiend's Mirror | 444C | 1113 | 1311 |
| 67284908 | Labyrinth Wall | 4450 | 1114 | 1411 |
| 94773007 | Jirai Gumo | 4454 | 1115 | 1511 |
| 30778711 | Shadow Ghoul | 4458 | 1116 | 1611 |
| 63162310 | Wall Shadow | 445C | 1117 | 1711 |
| 99551425 | Labyrinth Tank | 4460 | 1118 | 1811 |
| 25955164 | Sanga of the Thunder | 4464 | 1119 | 1911 |
| 62340868 | Kazejin | 4468 | 111A | 1A11 |
| 98434877 | Suijin | 446C | 111B | 1B11 |
| 25833572 | Gate Guardian | 4470 | 111C | 1C11 |
| 24611934 | Ryu-Kishin Powered | 447C | 111F | 1F11 |
| 50005633 | Swordstalker | 4480 | 1120 | 2011 |
| 97590747 | La Jinn the Mystical Genie of the Lamp | 4484 | 1121 | 2111 |
| 23995346 | Blue-Eyes Ultimate Dragon | 4488 | 1122 | 2211 |
| 59383041 | Toon Alligator | 448C | 1123 | 2311 |
| 62762898 | Parrot Dragon | 4494 | 1125 | 2511 |
| 99261403 | Dark Rabbit | 4498 | 1126 | 2611 |
| 25655502 | Bickuribox | 449C | 1127 | 2711 |
| 52040216 | Harpie's Pet Dragon | 44A0 | 1128 | 2811 |
| 24433920 | Pendulum Machine | 44A8 | 112A | 2A11 |
| 51828629 | Giltia the D. Knight | 44AC | 112B | 2B11 |
| 87322377 | Launcher Spider | 44B0 | 112C | 2C11 |
| 24311372 | Zoa | 44B4 | 112D | 2D11 |
| 50705071 | Metalzoa | 44B8 | 112E | 2E11 |
| 86088138 | Ocubeam | 44C8 | 1132 | 3211 |
| 84133008 | Monster Eye | 44E0 | 1138 | 3811 |
| 10315429 | Yaiba Robo | 44F0 | 113C | 3C11 |
| 46700124 | Machine King | 44F4 | 113D | 3D11 |
| 09293977 | Metal Dragon | 44FC | 113F | 3F11 |
| 08471389 | Giga-Tech Wolf | 4508 | 1142 | 4211 |
| 71950093 | Shovel Crusher | 4510 | 1144 | 4411 |
| 07359741 | Mechanicalchaser | 4514 | 1145 | 4511 |
| 34743446 | Blocker | 4518 | 1146 | 4611 |
| 07526150 | Golgoil | 4520 | 1148 | 4811 |
| 69015963 | Cyber-Stein | 4528 | 114A | 4A11 |
| 06400512 | Cyber Commander | 452C | 114B | 4B11 |
| 32809211 | Jinzo #7 | 4530 | 114C | 4C11 |
| 31786629 | Thunder Dragon | 453C | 114F | 4F11 |
| 94566432 | Kaiser Dragon | 4544 | 1151 | 5111 |
| 31560081 | Magician of Faith | 4548 | 1152 | 5211 |
| 67959180 | Goddess of Whim | 454C | 1153 | 5311 |
| 93343894 | Water Magician | 4550 | 1154 | 5411 |
| 20848593 | Ice Water | 4554 | 1155 | 5511 |
| 66836598 | Waterdragon Fairy | 4558 | 1156 | 5611 |
| 93221206 | Ancient Elf | 455C | 1157 | 5711 |
| 55014050 | Water Girl | 4564 | 1159 | 5911 |
| 28593363 | Deepsea Shark | 456C | 115B | 5B11 |
| 81386177 | Bottom Dweller | 4574 | 115D | 5D11 |
| 23771716 | 7 Colored Fish | 4578 | 115E | 5E11 |
| 85448931 | Guardian of the Sea | 458C | 1163 | 6311 |
| 12436646 | Aqua Snake | 4590 | 1164 | 6411 |
| 58831685 | Giant Red Seasnake | 4594 | 1165 | 6511 |
| 48109103 | Kappa Avenger | 45A0 | 1168 | 6811 |
| 84103702 | Kanikabuto | 45A4 | 1169 | 6911 |
| 10598400 | Zarigun | 45A8 | 116A | 6A11 |
| 47986555 | Millennium Golem | 45AC | 116B | 6B11 |
| 73481154 | Destroyer Golem | 45B0 | 116C | 6C11 |
| 10476868 | Barrel Rock | 45B4 | 116D | 6D11 |
| 46864967 | Minomushi Warrior | 45B8 | 116E | 6E11 |
| 72269672 | Stone Ghost | 45BC | 116F | 6F11 |
| 09653271 | Kaminari Attack | 45C0 | 1170 | 7011 |
| 45042329 | Tripwire Beast | 45C4 | 1171 | 7111 |
| 48531733 | Bolt Penguin | 45CC | 1173 | 7311 |
| 84926738 | The Immortal of Thunder | 45D0 | 1174 | 7411 |
| 11324436 | Electric Snake | 45D4 | 1175 | 7511 |
| 74703140 | Punished Eagle | 45DC | 1177 | 7711 |
| 10202894 | Skull Red Bird | 45E0 | 1178 | 7811 |
| 46696593 | Crimson Sunbird | 45E4 | 1179 | 7911 |
| 09076207 | Armed Ninja | 45EC | 117B | 7B11 |
| 46474915 | Magical Ghost | 45F0 | 117C | 7C11 |
| 72869010 | Soul Hunter | 45F4 | 117D | 7D11 |
| 35752363 | Vermillion Sparrow | 45FC | 117F | 7F11 |
| 71746462 | Sea Kamen | 4600 | 1180 | 8011 |
| 08131171 | Sinister Serpent | 4604 | 1181 | 8111 |
| 34536276 | Ganigumo | 4608 | 1182 | 8211 |
| 70924884 | Alinsection | 460C | 1183 | 8311 |
| 07019529 | Insect Soldiers of the Sky | 4610 | 1184 | 8411 |
| 33413638 | Cockroach Knight | 4614 | 1185 | 8511 |
| 06297941 | Burglar | 461C | 1187 | 8711 |
| 33691040 | Pragtical | 4620 | 1188 | 8811 |
| 95174353 | Ameba | 4628 | 118A | 8A11 |
| 32569498 | Korogashi | 462C | 118B | 8B11 |
| 68963107 | Boo Koo | 4630 | 118C | 8C11 |
| 95952802 | Flower Wolf | 4634 | 118D | 8D11 |
| 21347810 | Rainbow Flower | 4638 | 118E | 8E11 |
| 67841515 | Barrel Lily | 463C | 118F | 8F11 |
| 67629977 | Hoshiningen | 4648 | 1192 | 9211 |
| 93013676 | Maha Vailo | 464C | 1193 | 9311 |
| 56907389 | Musician King | 4654 | 1195 | 9511 |
| 92391084 | Wilmee | 4658 | 1196 | 9611 |
| 28563545 | Dragon Seeker | 4668 | 119A | 9A11 |
| 54652250 | Man-Eater Bug | 466C | 119B | 9B11 |
| 81057959 | D. Human | 4670 | 119C | 9C11 |
| 17441953 | Turtle Raccoon | 4674 | 119D | 9D11 |
| 80234301 | Prisman | 467C | 119F | 9F11 |
| 53713014 | Crazy Fish | 4684 | 11A1 | A111 |
| 16507828 | Bracchio-raidus | 468C | 11A3 | A311 |
| 42591472 | Laughing Flower | 4690 | 11A4 | A411 |
| 84990171 | Bean Soldier | 4694 | 11A5 | A511 |
| 11384280 | Cannon Soldier | 4698 | 11A6 | A611 |
| 47879985 | Guardian of the Throne Room | 469C | 11A7 | A711 |
| 74277583 | Brave Scizzar | 46A0 | 11A8 | A811 |
| 10262698 | The Statue of Easter Island | 46A4 | 11A9 | A911 |
| 46657337 | Muka Muka | 46A8 | 11AA | AA11 |
| 09540040 | Boulder Tortoise | 46B0 | 11AC | AC11 |
| 46534755 | Fire Kraken | 46B4 | 11AD | AD11 |
| 72929454 | Turtle Bird | 46B8 | 11AE | AE11 |
| 08327462 | Skullbird | 46BC | 11AF | AF11 |
| 35712107 | Monstrous Bird | 46C0 | 11B0 | B011 |
| 71107816 | The Bistro Butcher | 46C4 | 11B1 | B111 |
| 08201910 | Star Boy | 46C8 | 11B2 | B211 |
| 07489323 | Milus Radiant | 46D4 | 11B5 | B511 |
| 60862676 | Flame Cerebrus | 46DC | 11B7 | B711 |
| 06367785 | Eldeen | 46E0 | 11B8 | B811 |
| 32751480 | Mystical Sand | 46E4 | 11B9 | B911 |
| 69140098 | Gemini Elf | 46E8 | 11BA | BA11 |
| 32539892 | Minar | 46F0 | 11BC | BC11 |
| 68928540 | Kamakiriman | 46F4 | 11BD | BD11 |
| 94412545 | Mechaleon | 46F8 | 11BE | BE11 |
| 21817254 | Mega Thunderball | 46FC | 11BF | BF11 |
| 07805359 | Niwatori | 4700 | 11C0 | C011 |
| 34290067 | Corroding Shark | 4704 | 11C1 | C111 |
| 60694662 | Skelengel | 4708 | 11C2 | C211 |
| 07089711 | Hane-Hane | 470C | 11C3 | C311 |
| 69572024 | Tongyo | 4714 | 11C5 | C511 |
| 96967123 | Dharma Cannon | 4718 | 11C6 | C611 |
| 32355828 | Skelgon | 471C | 11C7 | C711 |
| 69750536 | Wow Warrior | 4720 | 11C8 | C811 |
| 95744531 | Griggle | 4724 | 11C9 | C911 |
| 68638985 | Frog the Jam | 472C | 11CB | CB11 |
| 94022093 | Behegon | 4730 | 11CC | CC11 |
| 21417692 | Dark Elf | 4734 | 11CD | CD11 |
| 57405307 | Winged Dragon, Guardian of the Fortress #2 | 4738 | 11CE | CE11 |
| 93788854 | The Wandering Doomed | 4748 | 11D2 | D211 |
| 29172562 | Steel Ogre Grotto #1 | 474C | 11D3 | D311 |
| 82065276 | Oscillo Hero | 4754 | 11D5 | D511 |
| 28450915 | Invader from Another Dimension | 4758 | 11D6 | D611 |
| 55444629 | Lesser Dragon | 475C | 11D7 | D711 |
| 81843628 | Needle Worm | 4760 | 11D8 | D811 |
| 17238333 | Wretched Ghost of the Attic | 4764 | 11D9 | D911 |
| 54622031 | Great Mammoth of Goldfine | 4768 | 11DA | DA11 |
| 80727036 | Man-eating Black Shark | 476C | 11DB | DB11 |
| 17115745 | Yormungarde | 4770 | 11DC | DC11 |
| 43500484 | Darkworld Thorns | 4774 | 11DD | DD11 |
| 89904598 | Anthrosaurus | 4778 | 11DE | DE11 |
| 16353197 | Drooling Lizard | 477C | 11DF | DF11 |
| 42348802 | Trakadon | 4780 | 11E0 | E011 |
| 89832901 | B. Dragon Jungle King | 4784 | 11E1 | E111 |
| 42625254 | Little D | 478C | 11E3 | E311 |
| 78010363 | Witch of the Black Forest | 4790 | 11E4 | E411 |
| 41403766 | Giant Scorpion of the Tundra | 4798 | 11E6 | E611 |
| 40387124 | Abyss Flower | 47A4 | 11E9 | E911 |
| 03170832 | Takuhee | 47AC | 11EB | EB11 |
| 08058240 | Binding Chain | 47B8 | 11EE | EE11 |
| 34442949 | Mechanical Snail | 47BC | 11EF | EF11 |
| 61831093 | Greenkappa | 47C0 | 11F0 | F011 |
| 07225792 | Mon Larvas | 47C4 | 11F1 | F111 |
| 34320307 | Living Vase | 47C8 | 11F2 | F211 |
| 60715406 | Tentacle Plant | 47CC | 11F3 | F311 |
| 06103114 | Beaked Snake | 47D0 | 11F4 | F411 |
| 33508719 | Morphing Jar | 47D4 | 11F5 | F511 |
| 69992868 | Muse-A | 47D8 | 11F6 | F611 |
| 32485271 | Rose Spectre of Dunn | 47E0 | 11F8 | F811 |
| 68870276 | Fiend Reflection #1 | 47E4 | 11F9 | F911 |
| 95265975 | Ghoul with an Appetite | 47E8 | 11FA | FA11 |
| 21263083 | Pale Beast | 47EC | 11FB | FB11 |
| 68658728 | Little Chimera | 47F0 | 11FC | FC11 |
| 94042337 | Violent Rain | 47F4 | 11FD | FD11 |
| 20541432 | Key Mace #2 | 47F8 | 11FE | FE11 |
| 57935140 | Tenderness | 47FC | 11FF | FF11 |
| 93920745 | Penguin Soldier | 4800 | 1200 | 0012 |
| 20315854 | Fairy Dragon | 4804 | 1201 | 0112 |
| 56713552 | Obese Marmot of Nefariousness | 4808 | 1202 | 0212 |
| 93108297 | Liquid Beast | 480C | 1203 | 0312 |
| 29692206 | Twin Long Rods #2 | 4810 | 1204 | 0412 |
| 55691901 | Great Bill | 4814 | 1205 | 0512 |
| 82085619 | Shining Friendship | 4818 | 1206 | 0612 |
| 28470714 | Bladefly | 481C | 1207 | 0712 |
| 81863068 | Hiro's Shadow Scout | 4824 | 1209 | 0912 |
| 17358176 | Lady of Faith | 4828 | 120A | 0A12 |
| 54752875 | Twin-Headed Thunder Dragon | 482C | 120B | 0B12 |
| 17535588 | Armored Starfish | 4834 | 120D | 0D12 |
| 29929832 | Marine Beast | 483C | 120F | 0F12 |
| 56413937 | Warrior of Tradition | 4840 | 1210 | 1012 |
| 29802344 | Snakeyashi | 4848 | 1212 | 1212 |
| 18180762 | The Thing That Hides in the Mud | 4854 | 1215 | 1512 |
| 54579801 | High Tide Gyojin | 4858 | 1216 | 1612 |
| 81563416 | Fairy of the Fountain | 485C | 1217 | 1712 |
| 17968114 | Amazon of the Seas | 4860 | 1218 | 1812 |
| 43352213 | Nekogal #2 | 4864 | 1219 | 1912 |
| 80741828 | Witch's Apprentice | 4868 | 121A | 1A12 |
| 16246527 | Armored Rat | 486C | 121B | 1B12 |
| 43230671 | Ancient Lizard Warrior | 4870 | 121C | 1C12 |
| 79629370 | Maiden of the Moonlight | 4874 | 121D | 1D12 |
| 78402798 | Night Lizard | 4880 | 1220 | 2012 |
| 41396436 | Blue-Winged Crown | 4888 | 1222 | 2212 |
| 40173854 | Amphibious Bugroth | 4894 | 1225 | 2512 |
| 77568553 | Acid Crawler | 4898 | 1226 | 2612 |
| 03056267 | Invader of the Throne | 489C | 1227 | 2712 |
| 30451366 | Mystical Sheep #1 | 48A0 | 1228 | 2812 |
| 76446915 | Disk Magician | 48A4 | 1229 | 2912 |
| 02830619 | Flame Viper | 48A8 | 122A | 2A12 |
| 39239728 | Royal Guard | 48AC | 122B | 2B12 |
| 65623423 | Gruesome Goo | 48B0 | 122C | 2C12 |
| 91996584 | Whiptail Crow | 48C0 | 1230 | 3012 |
| 37390589 | Kunai with Chain | 48C4 | 1231 | 3112 |
| 64389297 | Magical Labyrinth | 48C8 | 1232 | 3212 |
| 32268901 | Salamandra | 48D0 | 1234 | 3412 |
| 95051344 | Eternal Rest | 48D8 | 1236 | 3612 |
| 22046459 | Megamorph | 48DC | 1237 | 3712 |
| 68540058 | Metalmorph | 48E0 | 1238 | 3812 |
| 57728570 | Crush Card | 48EC | 123B | 3B12 |
| 82878489 | Bright Castle | 4908 | 1242 | 4212 |
| 29267084 | Shadow Spell | 490C | 1243 | 4312 |
| 55761792 | Black Luster Ritual | 4910 | 1244 | 4412 |
| 81756897 | Zera Ritual | 4914 | 1245 | 4512 |
| 18144506 | Harpie's Feather Duster | 4918 | 1246 | 4612 |
| 54539105 | War-Lion Ritual | 491C | 1247 | 4712 |
| 81933259 | Beastly Mirror Ritual | 4920 | 1248 | 4812 |
| 43417563 | Commencement Dance | 4928 | 124A | 4A12 |
| 80811661 | Hamburger Recipe | 492C | 124B | 4B12 |
| 43694075 | Novox's Prayer | 4934 | 124D | 4D12 |
| 15083728 | House of Adhesive Tape | 493C | 124F | 4F12 |
| 41356845 | Acid Trap Hole | 494C | 1253 | 5312 |
| 77754944 | Widespread Ruin | 4950 | 1254 | 5412 |
| 40633297 | Bad Reaction to Simochi | 4958 | 1256 | 5612 |
| 77622396 | Reverse Trap | 495C | 1257 | 5712 |
| 76806714 | Turtle Oath | 4968 | 125A | 5A12 |
| 39399168 | Resurrection of Chakra | 4970 | 125C | 5C12 |
| 41182875 | Javelin Beetle Pact | 4978 | 125E | 5E12 |
| 78577570 | Garma Sword Oath | 497C | 125F | 5F12 |
| 31066283 | Revival of Dokurorider | 4984 | 1261 | 6112 |
| 77454922 | Fortress Whale's Oath | 4988 | 1262 | 6212 |
| 04849037 | Performance of Sword | 498C | 1263 | 6312 |
| 30243636 | Hungry Burger | 4990 | 1264 | 6412 |
| 76232340 | Sengenjin | 4994 | 1265 | 6512 |
| 03627449 | Skull Guardian | 4998 | 1266 | 6612 |
| 39111158 | Tri-Horned Dragon | 499C | 1267 | 6712 |
| 66516792 | Serpent Night Dragon | 49A0 | 1268 | 6812 |
| 38999506 | Cosmo Queen | 49A8 | 126A | 6A12 |
| 65393205 | Chakra | 49AC | 126B | 6B12 |
| 91782219 | Crab Turtle | 49B0 | 126C | 6C12 |
| 38277918 | Mikazukinoyaiba | 49B4 | 126D | 6D12 |
| 64271667 | Meteor Dragon | 49B8 | 126E | 6E12 |
| 90660762 | Meteor B. Dragon | 49BC | 126F | 6F12 |
| 27054370 | Firewing Pegasus | 49C0 | 1270 | 7012 |
| 90844184 | Garma Sword | 49C8 | 1272 | 7212 |
| 26932788 | Javelin Beetle | 49CC | 1273 | 7312 |
| 62337487 | Fortress Whale | 49D0 | 1274 | 7412 |
| 99721536 | Dokurorider | 49D4 | 1275 | 7512 |
| 76792184 | Dark Magic Ritual | 49DC | 1277 | 7712 |
| 30208479 | Magician of Black Chaos | 49E0 | 1278 | 7812 |
| 03797883 | Slot Machine | 49E4 | 1279 | 7912 |
| 65570596 | Red Archery Girl | 49EC | 127B | 7B12 |
| 02964201 | Ryu-Ran | 49F0 | 127C | 7C12 |
| 38369349 | Manga Ryu-Ran | 49F4 | 127D | 7D12 |
| 65458948 | Toon Mermaid | 49F8 | 127E | 7E12 |
| 91842653 | Toon Summoned Skull | 49FC | 127F | 7F12 |
| 64631466 | Relinquished | 4A04 | 1281 | 8112 |
| 27125110 | Thousand-Eyes Idol | 4A0C | 1283 | 8312 |
| 63519819 | Thousand-Eyes Restrict | 4A10 | 1284 | 8412 |
| 90908427 | Steel Ogre Grotto #2 | 4A14 | 1285 | 8512 |
| 26302522 | Blast Sphere | 4A18 | 1286 | 8612 |
| 62397231 | Hyozanryu | 4A1C | 1287 | 8712 |
| 99785935 | Alpha The Magnet Warrior | 4A20 | 1288 | 8812 |
| 17985575 | Lord of D. | 4A2C | 128B | 8B12 |
| 64335804 | Red-Eyes Black Metal Dragon | 4A30 | 128C | 8C12 |
| 81480460 | Barrel Dragon | 4A34 | 128D | 8D12 |
| 05640330 | Hannibal Necromancer | 4A38 | 128E | 8E12 |
| 42035044 | Panther Warrior | 4A3C | 128F | 8F12 |
| 78423643 | Three-Headed Geedo | 4A40 | 1290 | 9012 |
| 05818798 | Gazelle the King of Mythical Beasts | 4A44 | 1291 | 9112 |
| 31812496 | Stone Statue of the Aztecs | 4A48 | 1292 | 9212 |
| 77207191 | Berfomet | 4A4C | 1293 | 9312 |
| 04796100 | Chimera the Flying Mythical Beast | 4A50 | 1294 | 9412 |
| 30190809 | Gear Golem the Moving Fortress | 4A54 | 1295 | 9512 |
| 77585513 | Jinzo | 4A58 | 1296 | 9612 |
| 03573512 | Swordsman of Landstar | 4A5C | 1297 | 9712 |
| 39978267 | Cyber Raider | 4A60 | 1298 | 9812 |
| 66362965 | The Fiend Megacyber | 4A64 | 1299 | 9912 |
| 02851070 | Reflect Bounder | 4A68 | 129A | 9A12 |
| 39256679 | Beta The Magnet Warrior | 4A6C | 129B | 9B12 |
| 65240384 | Big Shield Gardna | 4A70 | 129C | 9C12 |
| 38033121 | Dark Magician Girl | 4A78 | 129E | 9E12 |
| 64428736 | Alligator's Sword | 4A7C | 129F | 9F12 |
| 91512835 | Insect Queen | 4A80 | 12A0 | A012 |
| 27911549 | Parasite Paracide | 4A84 | 12A1 | A112 |
| 64306248 | Skull-Mark Ladybug | 4A88 | 12A2 | A212 |
| 90790253 | Little-Winguard | 4A8C | 12A3 | A312 |
| 26185991 | Pinch Hopper | 4A90 | 12A4 | A412 |
| 53183600 | Blue-Eyes Toon Dragon | 4A94 | 12A5 | A512 |
| 51345461 | Sword Hunter | 4A98 | 12A6 | A612 |
| 88733579 | Drill Bug | 4A9C | 12A7 | A712 |
| 24128274 | Deepsea Warrior | 4AA0 | 12A8 | A812 |
| 50400231 | Satellite Cannon | 4AB0 | 12AC | AC12 |
| 86099788 | The Last Warrior from Another Planet | 4AC4 | 12B1 | B112 |
| 12493482 | Dunames Dark Witch | 4AC8 | 12B2 | B212 |
| 49888191 | Garnecia Elefantis | 4ACC | 12B3 | B312 |
| 75372290 | Total Defense Shogun | 4AD0 | 12B4 | B412 |
| 11761845 | Beast of Talwar | 4AD4 | 12B5 | B512 |
| 48766543 | Cyber-Tech Alligator | 4AD8 | 12B6 | B612 |
| 11549357 | Gamma The Magnet Warrior | 4AE0 | 12B8 | B812 |
| 80987696 | Time Machine | 4AE8 | 12BA | BA12 |
| 26376390 | Copycat | 4AEC | 12BB | BB12 |
| 15259703 | Toon World | 4AF8 | 12BE | BE12 |
| 52648457 | Gorgon's Eye | 4AFC | 12BF | BF12 |
| 41426869 | Black Illusion Ritual | 4B08 | 12C2 | C212 |
| 87910978 | Brain Control | 4B0C | 12C3 | C312 |
| 14315573 | Negate Attack | 4B10 | 12C4 | C412 |
| 40703222 | Multiply | 4B14 | 12C5 | C512 |
| 49587034 | Lightforce Sword | 4B20 | 12C8 | C812 |
| 43973174 | The Flute of Summoning Dragon | 4B28 | 12CA | CA12 |
| 52097679 | Shield & Sword | 4B2C | 12CB | CB12 |
| 79571449 | Graceful Charity | 4B30 | 12CC | CC12 |
| 01248895 | Chain Destruction | 4B34 | 12CD | CD12 |
| 48642904 | Mesmeric Control | 4B38 | 12CE | CE12 |
| 74137509 | Graceful Dice | 4B3C | 12CF | CF12 |
| 00126218 | Skull Dice | 4B40 | 12D0 | D012 |
| 37520316 | Mind Control | 4B44 | 12D1 | D112 |
| 73915051 | Scapegoat | 4B48 | 12D2 | D212 |
| 00303660 | Amplifier | 4B4C | 12D3 | D312 |
| 72892473 | Card Destruction | 4B54 | 12D5 | D512 |
| 35686187 | Tragedy | 4B5C | 12D7 | D712 |
| 97342942 | Ectoplasmer | 4B70 | 12DC | DC12 |
| 99789342 | Dark Magic Curtain | 4B78 | 12DE | DE12 |
| 23615409 | Insect Barrier | 4B80 | 12E0 | E012 |
| 96008713 | Magic-Arm Shield | 4B88 | 12E2 | E212 |
| 66788016 | Fissure | 4B8C | 12E3 | E312 |
| 04206964 | Trap Hole | 4B90 | 12E4 | E412 |
| 24094653 | Polymerization | 4B94 | 12E5 | E512 |
| 51482758 | Remove Trap | 4B98 | 12E6 | E612 |
| 83887306 | Two-Pronged Attack | 4B9C | 12E7 | E712 |
| 83764718 | Monster Reborn | 4BA8 | 12EA | EA12 |
| 19159413 | De-Spell | 4BAC | 12EB | EB12 |
| 55144522 | Pot of Greed | 4BB0 | 12EC | EC12 |
| 82542267 | Gravedigger Ghoul | 4BB4 | 12ED | ED12 |
| 17814387 | Reinforcements | 4BC4 | 12F1 | F112 |
| 44209392 | Castle Walls | 4BC8 | 12F2 | F212 |
| 80604091 | Ultimate Offering | 4BCC | 12F3 | F312 |
| 79759861 | Tribute to The Doomed | 4BE0 | 12F8 | F812 |
| 05758500 | Soul Release | 4BE4 | 12F9 | F912 |
| 41142615 | The Cheerful Coffin | 4BE8 | 12FA | FA12 |
| 04031928 | Change of Heart | 4BF0 | 12FC | FC12 |
| 41420027 | Solemn Judgment | 4BF4 | 12FD | FD12 |
| 77414722 | Magic Jammer | 4BF8 | 12FE | FE12 |
| 03819470 | Seven Tools of the Bandit | 4BFC | 12FF | FF12 |
| 98069388 | Horn of Heaven | 4C00 | 1300 | 0013 |
| 24068492 | Just Desserts | 4C04 | 1301 | 0113 |
| 51452091 | Royal Decree | 4C08 | 1302 | 0213 |
| 24094653 | Polymerization | 4C0C | 1303 | 0313 |
| 53119267 | Magical Thorn | 4C18 | 1306 | 0613 |
| 99518961 | Restructer Revolution | 4C1C | 1307 | 0713 |
| 26902560 | Fusion Sage | 4C20 | 1308 | 0813 |
| 98495314 | Sword of Deep-Seated | 4C24 | 1309 | 0913 |
| 25880422 | Block Attack | 4C28 | 130A | 0A13 |
| 51275027 | The Unhappy Maiden | 4C2C | 130B | 0B13 |
| 88279736 | Robbin' Goblin | 4C30 | 130C | 0C13 |
| 24668830 | Germ Infection | 4C34 | 130D | 0D13 |
| 13945283 | Wall of Illusion | 4C40 | 1310 | 1013 |
| 50930991 | Neo the Magic Swordsman | 4C44 | 1311 | 1113 |
| 86325596 | Baron of the Fiend Sword | 4C48 | 1312 | 1213 |
| 13723605 | Man-Eating Treasure Chest | 4C4C | 1313 | 1313 |
| 49218300 | Sorcerer of the Doomed | 4C50 | 1314 | 1413 |
| 85602018 | Last Will | 4C54 | 1315 | 1513 |
| 12607053 | Waboku | 4C58 | 1316 | 1613 |
| 44095762 | Mirror Force | 4C5C | 1317 | 1713 |
| 20436034 | Ring of Magnetism | 4C60 | 1318 | 1813 |
| 56830749 | Share the Pain | 4C64 | 1319 | 1913 |
| 83225447 | Stim-Pack | 4C68 | 131A | 1A13 |
| 19613556 | Heavy Storm | 4C6C | 131B | 1B13 |
| 16762927 | Gravekeeper's Servant | 4C74 | 131D | 1D13 |
| 70368879 | Upstart Goblin | 4C7C | 131F | 1F13 |
| 82003859 | Toll | 4C80 | 1320 | 2013 |
| 18591904 | Final Destiny | 4C84 | 1321 | 2113 |
| 45986603 | Snatch Steal | 4C88 | 1322 | 2213 |
| 81380218 | Chorus of Sanctuary | 4C8C | 1323 | 2313 |
| 17375316 | Confiscation | 4C90 | 1324 | 2413 |
| 44763025 | Delinquent Duo | 4C94 | 1325 | 2513 |
| 17653779 | Fairy's Hand Mirror | 4C9C | 1327 | 2713 |
| 43641473 | Tailor of the Fickle | 4CA0 | 1328 | 2813 |
| 70046172 | Rush Recklessly | 4CA4 | 1329 | 2913 |
| 16430187 | The Reliable Guardian | 4CA8 | 132A | 2A13 |
| 42829885 | The Forceful Sentry | 4CAC | 132B | 2B13 |
| 79323590 | Chain Energy | 4CB0 | 132C | 2C13 |
| 05318639 | Mystical Space Typhoon | 4CB4 | 132D | 2D13 |
| 42703248 | Giant Trunade | 4CB8 | 132E | 2E13 |
| 74191942 | Painful Choice | 4CBC | 132F | 2F13 |
| 00596051 | Snake Fang | 4CC0 | 1330 | 3013 |
| 34124316 | Cyber Jar | 4CC4 | 1331 | 3113 |
| 61528025 | Banisher of the Light | 4CC8 | 1332 | 3213 |
| 97017120 | Giant Rat | 4CCC | 1333 | 3313 |
| 23401839 | Senju of the Thousand Hands | 4CD0 | 1334 | 3413 |
| 60806437 | UFO Turtle | 4CD4 | 1335 | 3513 |
| 96890582 | Flash Assailant | 4CD8 | 1336 | 3613 |
| 23289281 | Karate Man | 4CDC | 1337 | 3713 |
| 95178994 | Giant Germ | 4CE4 | 1339 | 3913 |
| 22567609 | Nimble Momonga | 4CE8 | 133A | 3A13 |
| 58551308 | Spear Cretin | 4CEC | 133B | 3B13 |
| 95956346 | Shining Angel | 4CF0 | 133C | 3C13 |
| 57839750 | Mother Grizzly | 4CF8 | 133E | 3E13 |
| 84834865 | Flying Kamakiri #1 | 4CFC | 133F | 3F13 |
| 20228463 | Ceremonial Bell | 4D00 | 1340 | 4013 |
| 57617178 | Sonic Bird | 4D04 | 1341 | 4113 |
| 83011277 | Mystic Tomato | 4D08 | 1342 | 4213 |
| 19406822 | Kotodama | 4D0C | 1343 | 4313 |
| 56594520 | Gaia Power | 4D10 | 1344 | 4413 |
| 82999629 | Umiiruka | 4D14 | 1345 | 4513 |
| 19384334 | Molten Destruction | 4D18 | 1346 | 4613 |
| 45778932 | Rising Air Current | 4D1C | 1347 | 4713 |
| 81777047 | Luminous Spark | 4D20 | 1348 | 4813 |
| 18161786 | Mystic Plasma Zone | 4D24 | 1349 | 4913 |
| 44656491 | Messenger of Peace | 4D28 | 134A | 4A13 |
| 37580756 | Michizure | 4D2C | 134B | 4B13 |
| 73079365 | Gust | 4D30 | 134C | 4C13 |
| 00473469 | Driving Snow | 4D34 | 134D | 4D13 |
| 02130625 | Numinous Healer | 4D48 | 1352 | 5213 |
| 48539234 | Appropriate | 4D4C | 1353 | 5313 |
| 74923978 | Forced Requisition | 4D50 | 1354 | 5413 |
| 01918087 | Minor Goblin Official | 4D54 | 1355 | 5513 |
| 37313786 | Gamble | 4D58 | 1356 | 5613 |
| 74701381 | DNA Surgery | 4D5C | 1357 | 5713 |
| 00296499 | The Regulation of Tribe | 4D60 | 1358 | 5813 |
| 36280194 | Backup Soldier | 4D64 | 1359 | 5913 |
| 63689843 | Attack and Receive | 4D68 | 135A | 5A13 |
| 36468556 | Ceasefire | 4D70 | 135C | 5C13 |
| 62867251 | Light of Intervention | 4D74 | 135D | 5D13 |
| 08951260 | Respect Play | 4D78 | 135E | 5E13 |
| 61740673 | Imperial Order | 4D80 | 1360 | 6013 |
| 98139712 | Skull Invitation | 4D84 | 1361 | 6113 |
| 81210420 | Magical Hats | 4D88 | 1362 | 6213 |
| 71044499 | Nobleman of Crossout | 4D8C | 1363 | 6313 |
| 17449108 | Nobleman of Extermination | 4D90 | 1364 | 6413 |
| 43434803 | The Shallow Grave | 4D94 | 1365 | 6513 |
| 70828912 | Premature Burial | 4D98 | 1366 | 6613 |
| 79106360 | Morphing Jar #2 | 4DA4 | 1369 | 6913 |
| 06104968 | Bubonic Vermin | 4DA8 | 136A | 6A13 |
| 78984772 | Twin-Headed Fire Dragon | 4DB0 | 136C | 6C13 |
| 05388481 | Darkfire Soldier #1 | 4DB4 | 136D | 6D13 |
| 31477025 | Mr. Volcano | 4DB8 | 136E | 6E13 |
| 78861134 | Darkfire Soldier #2 | 4DBC | 136F | 6F13 |
| 04266839 | Kiseitai | 4DC0 | 1370 | 7013 |
| 30655537 | Cyber Falcon | 4DC4 | 1371 | 7113 |
| 67049542 | Dark Bat | 4DC8 | 1372 | 7213 |
| 03134241 | Flying Kamakiri #2 | 4DCC | 1373 | 7313 |
| 30532390 | Harpie's Brother | 4DD0 | 1374 | 7413 |
| 66927994 | Oni Tank T-34 | 4DD4 | 1375 | 7513 |
| 02311603 | Overdrive | 4DD8 | 1376 | 7613 |
| 78193831 | Buster Blader | 4DDC | 1377 | 7713 |
| 35316708 | Time Seal | 4DE0 | 1378 | 7813 |
| 61705417 | Graverobber | 4DE4 | 1379 | 7913 |
| 98299011 | Gift of The Mystical Elf | 4DE8 | 137A | 7A13 |
| 34694160 | The Eye of Truth | 4DEC | 137B | 7B13 |
| 60082869 | Dust Tornado | 4DF0 | 137C | 7C13 |
| 97077563 | Call of the Haunted | 4DF4 | 137D | 7D13 |
| 23471572 | Solomon's Lawbook | 4DF8 | 137E | 7E13 |
| 96355986 | Enchanted Javelin | 4E00 | 1380 | 8013 |
| 22359980 | Mirror Wall | 4E04 | 1381 | 8113 |
| 59744639 | Windstorm of Etaqua | 4E24 | 1389 | 8913 |
| 75347539 | Valkyrion the Magna Warrior | 4E28 | 138A | 8A13 |
| 03366982 | Alligator's Sword Dragon | 4E2C | 138B | 8B13 |
| 14898066 | Vorse Raider | 4E30 | 138C | 8C13 |
| 83555666 | Ring of Destruction | 4E34 | 138D | 8D13 |
| 95132338 | Aqua Chorus | 4E38 | 138E | 8E13 |
| 22537443 | Sebek's Blessing | 4E3C | 138F | 8F13 |
| 58921041 | Anti-Spell Fragrance | 4E40 | 1390 | 9013 |
| 34016756 | Riryoku | 4E44 | 1391 | 9113 |
| 61405855 | Sword of Dragon's Soul | 4E48 | 1392 | 9213 |
| 57482479 | Luminous Soldier | 4E5C | 1397 | 9713 |
| 83986578 | King Tiger Wanghu | 4E60 | 1398 | 9813 |
| 10375182 | Command Knight | 4E64 | 1399 | 9913 |
| 56369281 | Wolf Axwielder | 4E68 | 139A | 9A13 |
| 83764996 | The Illusory Gentleman | 4E6C | 139B | 9B13 |
| 19153634 | Patrician of Darkness | 4E70 | 139C | 9C13 |
| 45547649 | Birdface | 4E74 | 139D | 9D13 |
| 82642348 | Kryuel | 4E78 | 139E | 9E13 |
| 18036057 | Airknight Parshath | 4E7C | 139F | 9F13 |
| 45425051 | Fairy King Truesdale | 4E80 | 13A0 | A013 |
| 71829750 | Serpentine Princess | 4E84 | 13A1 | A113 |
| 17214465 | Maiden of the Aqua | 4E88 | 13A2 | A213 |
| 44203504 | Robotic Knight | 4E8C | 13A3 | A313 |
| 70797118 | Thunder Nyan Nyan | 4E90 | 13A4 | A413 |
| 17192817 | Molten Behemoth | 4E94 | 13A5 | A513 |
| 43586926 | Twin-Headed Behemoth | 4E98 | 13A6 | A613 |
| 79575620 | Injection Fairy Lily | 4E9C | 13A7 | A713 |
| 06979239 | Woodland Sprite | 4EA0 | 13A8 | A813 |
| 42364374 | Arsenal Bug | 4EA4 | 13A9 | A913 |
| 79853073 | Kinetic Soldier | 4EA8 | 13AA | AA13 |
| 05257687 | Jowls of Dark Demise | 4EAC | 13AB | AB13 |
| 31242786 | Souleater | 4EB0 | 13AC | AC13 |
| 78636495 | Slate Warrior | 4EB4 | 13AD | AD13 |
| 44913552 | Timeater | 4EC4 | 13B1 | B113 |
| 70307656 | Mucus Yolk | 4EC8 | 13B2 | B213 |
| 02792265 | Servant of Catabolism | 4ECC | 13B3 | B313 |
| 39180960 | Rigras Leever | 4ED0 | 13B4 | B413 |
| 75285069 | Moisture Creature | 4ED4 | 13B5 | B513 |
| 98456117 | Boneheimer | 4ED8 | 13B6 | B613 |
| 12883044 | Flame Dancer | 4EE0 | 13B8 | B813 |
| 84550200 | Sonic Jammer | 4EF4 | 13BD | BD13 |
| 00423705 | Gearfried the Iron Knight | 4F0C | 13C3 | C313 |
| 46821314 | Humanoid Slime | 4F10 | 13C4 | C413 |
| 73216412 | Worm Drake | 4F14 | 13C5 | C513 |
| 05600127 | Humanoid Worm Drake | 4F18 | 13C6 | C613 |
| 31709826 | Revival Jam | 4F1C | 13C7 | C713 |
| 31987274 | Flying Fish | 4F24 | 13C9 | C913 |
| 67371383 | Amphibian Beast | 4F28 | 13CA | CA13 |
| 30860696 | Rocket Warrior | 4F2C | 13CB | CB13 |
| 03643300 | The Legendary Fisherman | 4F34 | 13CD | CD13 |
| 92421852 | Robolady | 4F40 | 13D0 | D013 |
| 38916461 | Roboyarou | 4F44 | 13D1 | D113 |
| 27671321 | Lightning Conger | 4F5C | 13D7 | D713 |
| 52121290 | Spherous Lady | 4F78 | 13DE | DE13 |
| 87303357 | Shining Abyss | 4F88 | 13E2 | E213 |
| 50287060 | Archfiend of Gilfer | 4F8C | 13E3 | E313 |
| 86281779 | Gadget Soldier | 4F90 | 13E4 | E413 |
| 13676474 | Grand Tiki Elder | 4F94 | 13E5 | E513 |
| 49064413 | The Masked Beast | 4F98 | 13E6 | E613 |
| 86569121 | Melchid the Four-Face Beast | 4F9C | 13E7 | E713 |
| 12953226 | Nuvia the Wicked | 4FA0 | 13E8 | E813 |
| 68005187 | Soul Exchange | 4FAC | 13EB | EB13 |
| 57882509 | Mask of Weakness | 4FB8 | 13EE | EE13 |
| 94377247 | Curse of the Masked Beast | 4FBC | 13EF | EF13 |
| 20765952 | Mask of Dispel | 4FC0 | 13F0 | F013 |
| 29549364 | Mask of Restrict | 4FC8 | 13F2 | F213 |
| 56948373 | Mask of the Accursed | 4FCC | 13F3 | F313 |
| 82432018 | Mask of Brutality | 4FD0 | 13F4 | F413 |
| 19827717 | Return of the Doomed | 4FD4 | 13F5 | F513 |
| 55226821 | Lightning Blade | 4FD8 | 13F6 | F613 |
| 18605135 | Tornado Wall | 4FDC | 13F7 | F713 |
| 54109233 | Infinite Dismissal | 4FE0 | 13F8 | F813 |
| 21598948 | Fairy Box | 4FE4 | 13F9 | F913 |
| 53582587 | Torrential Tribute | 4FE8 | 13FA | FA13 |
| 22493811 | Multiplication of Ants | 4FF0 | 13FC | FC13 |
| 95286165 | De-Fusion | 4FF8 | 13FE | FE13 |
| 21770260 | Jam Breeding Machine | 4FFC | 13FF | FF13 |
| 58775978 | Nightmare's Steelcage | 5000 | 1400 | 0014 |
| 94163677 | Infinite Cards | 5004 | 1401 | 0114 |
| 21558682 | Jam Defender | 5008 | 1402 | 0214 |
| 57953380 | Card of Safe Return | 500C | 1403 | 0314 |
| 62279055 | Magic Cylinder | 5010 | 1404 | 0414 |
| 35346968 | Solemn Wishes | 5014 | 1405 | 0514 |
| 24294108 | Burning Land | 5018 | 1406 | 0614 |
| 60682203 | Cold Wave | 501C | 1407 | 0714 |
| 97687912 | Fairy Meteor Crush | 5020 | 1408 | 0814 |
| 23171610 | Limiter Removal | 5024 | 1409 | 0914 |
| 59560625 | Shift | 5028 | 140A | 0A14 |
| 96965364 | Insect Imitation | 502C | 140B | 0B14 |
| 22959079 | Dimensionhole | 5030 | 140C | 0C14 |
| 59344077 | Magic Drain | 5034 | 140D | 0D14 |
| 85742772 | Gravity Bind | 5038 | 140E | 0E14 |
| 58621589 | Shadow of Eyes | 503C | 140F | 0F14 |
| 84620194 | Girochin Kuwagata | 5040 | 1410 | 1014 |
| 21015833 | Hayabusa Knight | 5044 | 1411 | 1114 |
| 57409948 | Bombardment Beetle | 5048 | 1412 | 1214 |
| 83994646 | 4-Starred Ladybug of Doom | 504C | 1413 | 1314 |
| 10992251 | Gradius | 5050 | 1414 | 1414 |
| 56387350 | Red-Moon Baby | 5054 | 1415 | 1514 |
| 79870141 | Mad Sword Beast | 5058 | 1416 | 1614 |
| 05265750 | Skull Mariner | 505C | 1417 | 1714 |
| 32269855 | The All-Seeing White Tiger | 5060 | 1418 | 1814 |
| 78658564 | Goblin Attack Force | 5064 | 1419 | 1914 |
| 04042268 | Island Turtle | 5068 | 141A | 1A14 |
| 31447217 | Wingweaver | 506C | 141B | 1B14 |
| 67532912 | Science Soldier | 5070 | 141C | 1C14 |
| 04920010 | Souls of the Forgotten | 5074 | 141D | 1D14 |
| 30325729 | Dokuroyaiba | 5078 | 141E | 1E14 |
| 66719324 | Rain of Mercy | 507C | 141F | 1F14 |
| 93108433 | Monster Recovery | 5080 | 1420 | 2014 |
| 21237481 | Type Zero Magic Crusher | 5084 | 1421 | 2114 |
| 04542651 | Yellow Luster Shield | 50A4 | 1429 | 2914 |
| 31036355 | Creature Swap | 50A8 | 142A | 2A14 |
| 46986414 | Dark Magician | 50B4 | 142D | 2D14 |
| 63391643 | Thousand Knives | 50B8 | 142E | 2E14 |
| 25774450 | Mystic Box | 50C0 | 1430 | 3014 |
| 90502999 | Ground Collapse | 50C8 | 1432 | 3214 |
| 91869203 | Amazon Archer | 512C | 144B | 4B14 |
| 64752646 | Fire Princess | 5134 | 144D | 4D14 |
| 53530069 | Spirit of the Breeze | 5140 | 1450 | 5014 |
| 90925163 | Dancing Fairy | 5144 | 1451 | 5114 |
| 58818411 | Empress Mantis | 514C | 1453 | 5314 |
| 85802526 | Cure Mermaid | 5150 | 1454 | 5414 |
| 21297224 | Hysteric Fairy | 5154 | 1455 | 5514 |
| 58696829 | Bio-Mage | 5158 | 1456 | 5614 |
| 84080938 | The Forgiving Maiden | 515C | 1457 | 5714 |
| 21175632 | St. Joan | 5160 | 1458 | 5814 |
| 57579381 | Marie the Fallen One | 5164 | 1459 | 5914 |
| 83968380 | Jar of Greed | 5168 | 145A | 5A14 |
| 10352095 | Scroll of Bewitchment | 516C | 145B | 5B14 |
| 56747793 | United We Stand | 5170 | 145C | 5C14 |
| 83746708 | Mage Power | 5174 | 145D | 5D14 |
| 19230407 | Offerings to the Doomed | 5178 | 145E | 5E14 |
| 33767325 | Meteor of Destruction | 5180 | 1460 | 6014 |
| 69162969 | Lightning Vortex | 5184 | 1461 | 6114 |
| 05556668 | Exchange | 5188 | 1462 | 6214 |
| 32541773 | The Portrait's Secret | 518C | 1463 | 6314 |
| 68049471 | The Gross Ghost of Fled Dreams | 5190 | 1464 | 6414 |
| 05434080 | Headless Knight | 5194 | 1465 | 6514 |
| 31829185 | Dark Necrofear | 5198 | 1466 | 6614 |
| 67227834 | Dark Magician's Tome of Black Magic | 519C | 1467 | 6714 |
| 94212438 | Destiny Board | 51A0 | 1468 | 6814 |
| 30606547 | The Dark Door | 51A4 | 1469 | 6914 |
| 67105242 | Earthbound Spirit | 51A8 | 146A | 6A14 |
| 93599951 | Dark Spirit of the Silent | 51AC | 146B | 6B14 |
| 66989694 | The Earl of Demise | 51B4 | 146D | 6D14 |
| 92377303 | Dark Sage | 51B8 | 146E | 6E14 |
| 29762407 | Cathedral of Nobles | 51BC | 146F | 6F14 |
| 55256016 | Judgment of Anubis | 51C0 | 1470 | 7014 |
| 28649820 | Embodiment of Apophis | 51C8 | 1472 | 7214 |
| 81439173 | Foolish Burial | 51D0 | 1474 | 7414 |
| 27827272 | Makiu | 51D4 | 1475 | 7514 |
| 54912977 | Ancient Lamp | 51D8 | 1476 | 7614 |
| 80316585 | Cyber Harpie Lady | 51DC | 1477 | 7714 |
| 89194033 | Mystical Beast Serket | 51E8 | 147A | 7A14 |
| 16589042 | Swift Gaia the Fierce Knight | 51EC | 147B | 7B14 |
| 52077741 | Obnoxious Celtic Guard | 51F0 | 147C | 7C14 |
| 88472456 | Zombyra the Dark | 51F4 | 147D | 7D14 |
| 15866454 | Spiritualism | 51F8 | 147E | 7E14 |
| 41855169 | Jowgen the Spiritualist | 51FC | 147F | 7F14 |
| 88240808 | Kycoo the Ghost Destroyer | 5200 | 1480 | 8014 |
| 14644902 | Summoner of Illusions | 5204 | 1481 | 8114 |
| 40133511 | Bazoo the Soul-Eater | 5208 | 1482 | 8214 |
| 77527210 | Soul of Purity and Light | 520C | 1483 | 8314 |
| 13522325 | Spirit of Flames | 5210 | 1484 | 8414 |
| 40916023 | Aqua Spirit | 5214 | 1485 | 8514 |
| 76305638 | The Rock Spirit | 5218 | 1486 | 8614 |
| 12800777 | Garuda the Wind Spirit | 521C | 1487 | 8714 |
| 45894482 | Gilasaurus | 5220 | 1488 | 8814 |
| 71283180 | Tornado Bird | 5224 | 1489 | 8914 |
| 08687195 | Dreamsprite | 5228 | 148A | 8A14 |
| 44072894 | Supply | 522C | 148B | 8B14 |
| 71466592 | Maryokutai | 5230 | 148C | 8C14 |
| 07565547 | Collected Power | 5234 | 148D | 8D14 |
| 33950246 | Royal Command | 5238 | 148E | 8E14 |
| 70344351 | Riryoku Field | 523C | 148F | 8F14 |
| 06733059 | Skull Lair | 5240 | 1490 | 9014 |
| 33737664 | Graverobber's Retribution | 5244 | 1491 | 9114 |
| 69122763 | Deal of Phantom | 5248 | 1492 | 9214 |
| 05616412 | Destruction Punch | 524C | 1493 | 9314 |
| 32015116 | Blind Destruction | 5250 | 1494 | 9414 |
| 68400115 | The Emperor's Holiday | 5254 | 1495 | 9514 |
| 05494820 | Cyclon Laser | 5258 | 1496 | 9614 |
| 31893528 | Spirit Message "I" | 525C | 1497 | 9714 |
| 67287533 | Spirit Message "N" | 5260 | 1498 | 9814 |
| 94772232 | Spirit Message "A" | 5264 | 1499 | 9914 |
| 30170981 | Spirit Message "L" | 5268 | 149A | 9A14 |
| 07165085 | Bait Doll | 526C | 149B | 9B14 |
| 33550694 | Fusion Gate | 5270 | 149C | 9C14 |
| 69954399 | Ekibyo Drakmord | 5274 | 149D | 9D14 |
| 06343408 | Miracle Dig | 5278 | 149E | 9E14 |
| 95220856 | Vengeful Bog Spirit | 5284 | 14A1 | A114 |
| 94004268 | Amazoness Swords Woman | 5290 | 14A4 | A414 |
| 21593977 | Makyura the Destructor | 5294 | 14A5 | A514 |
| 67987611 | Amazoness Archers | 5298 | 14A6 | A614 |
| 93382620 | Rope of Life | 529C | 14A7 | A714 |
| 93260132 | Enchanted Arrow | 52A8 | 14AA | AA14 |
| 29654737 | Amazoness Chain Master | 52AC | 14AB | AB14 |
| 56043446 | Viser Des | 52B0 | 14AC | AC14 |
| 55821894 | Amazoness Fighter | 52BC | 14AF | AF14 |
| 54704216 | Nightmare Wheel | 52C8 | 14B2 | B214 |
| 17597059 | Byser Shock | 52D0 | 14B4 | B414 |
| 53982768 | Dark Ruler Ha Des | 52D4 | 14B5 | B514 |
| 80071763 | Dark Balter the Terrible | 52D8 | 14B6 | B614 |
| 16475472 | Lesser Fiend | 52DC | 14B7 | B714 |
| 52860176 | Possessed Dark Soul | 52E0 | 14B8 | B814 |
| 89258225 | Winged Minion | 52E4 | 14B9 | B914 |
| 42647539 | Ryu-Kishin Clown | 52EC | 14BB | BB14 |
| 88132637 | Twin-Headed Wolf | 52F0 | 14BC | BC14 |
| 14531242 | Opticlops | 52F4 | 14BD | BD14 |
| 41925941 | Bark of Dark Ruler | 52F8 | 14BE | BE14 |
| 77910045 | Fatal Abacus | 52FC | 14BF | BF14 |
| 14318794 | Life Absorbing Machine | 5300 | 14C0 | C014 |
| 03682106 | Double Snare | 530C | 14C3 | C314 |
| 49681811 | Freed the Matchless General | 5310 | 14C4 | C414 |
| 76075810 | Throwstone Unit | 5314 | 14C5 | C514 |
| 02460565 | Marauding Captain | 5318 | 14C6 | C614 |
| 49868263 | Ryu Senshi | 531C | 14C7 | C714 |
| 75953262 | Warrior Dai Grepher | 5320 | 14C8 | C814 |
| 38742075 | Frontier Wiseman | 5328 | 14CA | CA14 |
| 74131780 | Exiled Force | 532C | 14CB | CB14 |
| 01525329 | The Hunter with 7 Weapons | 5330 | 14CC | CC14 |
| 37620434 | Shadow Tamer | 5334 | 14CD | CD14 |
| 63018132 | Dragon Manipulator | 5338 | 14CE | CE14 |
| 00403847 | The A. Forces | 533C | 14CF | CF14 |
| 32807846 | Reinforcement of the Army | 5340 | 14D0 | D014 |
| 69296555 | Array of Revealing Light | 5344 | 14D1 | D114 |
| 95281259 | The Warrior Returning Alive | 5348 | 14D2 | D214 |
| 31785398 | Ready for Intercepting | 534C | 14D3 | D314 |
| 68170903 | A Feint Plan | 5350 | 14D4 | D414 |
| 94568601 | Tyrant Dragon | 5354 | 14D5 | D514 |
| 31553716 | Spear Dragon | 5358 | 14D6 | D614 |
| 67957315 | Spirit Ryu | 535C | 14D7 | D714 |
| 93346024 | The Dragon dwelling in the Cave | 5360 | 14D8 | D814 |
| 20831168 | Lizard Soldier | 5364 | 14D9 | D914 |
| 66235877 | Fiend Skull Dragon | 5368 | 14DA | DA14 |
| 93220472 | Cave Dragon | 536C | 14DB | DB14 |
| 29618570 | Gray Wing | 5370 | 14DC | DC14 |
| 55013285 | Troop Dragon | 5374 | 14DD | DD14 |
| 92408984 | The Dragon's Bead | 5378 | 14DE | DE14 |
| 28596933 | A Wingbeat of Giant Dragon | 537C | 14DF | DF14 |
| 55991637 | Dragon's Gunfire | 5380 | 14E0 | E014 |
| 81385346 | Stamping Destruction | 5384 | 14E1 | E114 |
| 27770341 | Super Rejuvenation | 5388 | 14E2 | E214 |
| 54178050 | Dragon's Rage | 538C | 14E3 | E314 |
| 80163754 | Burst Breath | 5390 | 14E4 | E414 |
| 17658803 | Luster Dragon #2 | 5394 | 14E5 | E514 |
| 53046408 | Emergency Provisions | 5398 | 14E6 | E614 |
| 80441106 | Keldo | 539C | 14E7 | E714 |
| 16435215 | Dragged Down into the Grave | 53A0 | 14E8 | E814 |
| 52824910 | Kaiser Glider | 53A4 | 14E9 | E914 |
| 29228529 | Spell Reproduction | 53A8 | 14EA | EA14 |
| 55713623 | Collapse | 53AC | 14EB | EB14 |
| 82108372 | Mudora | 53B0 | 14EC | EC14 |
| 28106077 | Cestus of Dagla | 53B4 | 14ED | ED14 |
| 54591086 | De-Spell Germ Weapon | 53B8 | 14EE | EE14 |
| 81985784 | Des Feral Imp | 53BC | 14EF | EF14 |
| 17484499 | Reversal of Graves | 53C0 | 14F0 | F014 |
| 54878498 | Kelbek | 53C4 | 14F1 | F114 |
| 16268841 | Zolga | 53CC | 14F3 | F314 |
| 89041555 | Blast Held by a Tribute | 53D4 | 14F5 | F514 |
| 16135253 | Agido | 53D8 | 14F6 | F614 |
| 42534368 | Silent Fiend | 53DC | 14F7 | F714 |
| 78706415 | Fiber Jar | 53EC | 14FB | FB14 |
| 14291024 | Gradius' Option | 53F0 | 14FC | FC14 |
| 40695128 | Maharaghi | 53F4 | 14FD | FD14 |
| 77084837 | Inaba White Rabbit | 53F8 | 14FE | FE14 |
| 03078576 | Yata-Garasu | 53FC | 14FF | FF14 |
| 40473581 | Susa Soldier | 5400 | 1500 | 0015 |
| 76862289 | Yamata Dragon | 5404 | 1501 | 0115 |
| 02356994 | Great Long Nose | 5408 | 1502 | 0215 |
| 39751093 | Otohime | 540C | 1503 | 0315 |
| 75745607 | Hino-Kagu-Tsuchi | 5410 | 1504 | 0415 |
| 02134346 | Asura Priest | 5414 | 1505 | 0515 |
| 38538445 | Fushi No Tori | 5418 | 1506 | 0615 |
| 75923050 | Super Robolady | 541C | 1507 | 0715 |
| 01412158 | Super Roboyarou | 5420 | 1508 | 0815 |
| 37406863 | Fengsheng Mirror | 5424 | 1509 | 0915 |
| 64801562 | Heart of Clear Water | 5428 | 150A | 0A15 |
| 00295517 | A Legendary Ocean | 542C | 150B | 0B15 |
| 37684215 | Fusion Sword Murasame Blade | 5430 | 150C | 0C15 |
| 63789924 | Smoke Grenade of the Thief | 5434 | 150D | 0D15 |
| 99173029 | Spiritual Energy Settle Machine | 5438 | 150E | 0E15 |
| 36562627 | Second Coin Toss | 543C | 150F | 0F15 |
| 62966332 | Convulsion of Nature | 5440 | 1510 | 1015 |
| 99351431 | The Secret of the Bandit | 5444 | 1511 | 1115 |
| 25345186 | After the Struggle | 5448 | 1512 | 1215 |
| 98239899 | Blast with Chain | 5450 | 1514 | 1415 |
| 24623598 | Disappear | 5454 | 1515 | 1515 |
| 29401950 | Bottomless Trap Hole | 5460 | 1518 | 1815 |
| 56995655 | Ominous Fortunetelling | 5464 | 1519 | 1915 |
| 29389368 | Nutrient Z | 546C | 151B | 1B15 |
| 55773067 | Drop Off | 5470 | 151C | 1C15 |
| 81172176 | Fiend Comedian | 5474 | 151D | 1D15 |
| 28566710 | Last Turn | 5478 | 151E | 1E15 |
| 81059524 | Des Volstgalph | 5480 | 1520 | 2015 |
| 17444133 | Kaiser Sea Horse | 5484 | 1521 | 2115 |
| 53839837 | Vampire Lord | 5488 | 1522 | 2215 |
| 80233946 | Gora Turtle | 548C | 1523 | 2315 |
| 16222645 | Sasuke Samurai | 5490 | 1524 | 2415 |
| 43716289 | Poison Mummy | 5494 | 1525 | 2515 |
| 89111398 | Dark Dust Spirit | 5498 | 1526 | 2615 |
| 16509093 | Royal Keeper | 549C | 1527 | 2715 |
| 42994702 | Wandering Mummy | 54A0 | 1528 | 2815 |
| 88989706 | Great Dezard | 54A4 | 1529 | 2915 |
| 15383415 | Swarm of Scarabs | 54A8 | 152A | 2A15 |
| 41872150 | Swarm of Locusts | 54AC | 152B | 2B15 |
| 78266168 | Giant Axe Mummy | 54B0 | 152C | 2C15 |
| 40659562 | Guardian Sphinx | 54B8 | 152E | 2E15 |
| 77044671 | Pyramid Turtle | 54BC | 152F | 2F15 |
| 03549275 | Dice Jar | 54C0 | 1530 | 3015 |
| 40933924 | Dark Scorpion Burglars | 54C4 | 1531 | 3115 |
| 76922029 | Don Zaloog | 54C8 | 1532 | 3215 |
| 02326738 | Des Lacooda | 54CC | 1533 | 3315 |
| 39711336 | Fushioh Richie | 54D0 | 1534 | 3415 |
| 75109441 | Cobraman Sakuzy | 54D4 | 1535 | 3515 |
| 02204140 | Book of Life | 54D8 | 1536 | 3615 |
| 38699854 | Book of Taiyou | 54DC | 1537 | 3715 |
| 14087893 | Book of Moon | 54E0 | 1538 | 3815 |
| 41482598 | Mirage of Nightmare | 54E4 | 1539 | 3915 |
| 04861205 | Call of the Mummy | 54EC | 153B | 3B15 |
| 40350910 | Timidity | 54F0 | 153C | 3C15 |
| 76754619 | Pyramid Energy | 54F4 | 153D | 3D15 |
| 03149764 | Tutan Mask | 54F8 | 153E | 3E15 |
| 39537362 | Ordeal of a Traveler | 54FC | 153F | 3F15 |
| 76532077 | Bottomless Shifting Sand | 5500 | 1540 | 4015 |
| 02926176 | Curse of Royal | 5504 | 1541 | 4115 |
| 38411870 | Needle Ceiling | 5508 | 1542 | 4215 |
| 65810489 | Statue of the Wicked | 550C | 1543 | 4315 |
| 01804528 | Dark Coffin | 5510 | 1544 | 4415 |
| 38299233 | Needle Wall | 5514 | 1545 | 4515 |
| 64697231 | Trap Dustshoot | 5518 | 1546 | 4615 |
| 37576645 | Reckless Greed | 5520 | 1548 | 4815 |
| 90960358 | Toon Dark Magician Girl | 5528 | 154A | 4A15 |
| 36354007 | Gilford the Lightning | 552C | 154B | 4B15 |
| 63749102 | Exarion Universe | 5530 | 154C | 4C15 |
| 99747800 | Legendary Fiend | 5534 | 154D | 4D15 |
| 43509019 | Toon Defense | 5584 | 1561 | 6115 |
| 89997728 | Toon Table of Contents | 5588 | 1562 | 6215 |
| 16392422 | Toon Masked Sorcerer | 558C | 1563 | 6315 |
| 42386471 | Toon Gemini Elf | 5590 | 1564 | 6415 |
| 79875176 | Toon Cannon Soldier | 5594 | 1565 | 6515 |
| 15270885 | Toon Goblin Attack Force | 5598 | 1566 | 6615 |
| 42664989 | Card of Sanctity | 559C | 1567 | 6715 |
| 41442341 | Puppet Master | 55A8 | 156A | 6A15 |
| 04335645 | Newdoria | 55B0 | 156C | 6C15 |
| 40320754 | Lord Poison | 55B4 | 156D | 6D15 |
| 39507162 | Blade Knight | 55C0 | 1570 | 7015 |
| 76052811 | Helpoemer | 55C4 | 1571 | 7115 |
| 02047519 | Hidden Soldier | 55C8 | 1572 | 7215 |
| 38445524 | Gil Garth | 55CC | 1573 | 7315 |
| 01224927 | Calamity of the Wicked | 55D4 | 1575 | 7515 |
| 00102380 | Lava Golem | 55E0 | 1578 | 7815 |
| 37507488 | Monster Relief | 55E4 | 1579 | 7915 |
| 63995093 | Machine Duplication | 55E8 | 157A | 7A15 |
| 90980792 | Dark Jeroid | 55EC | 157B | 7B15 |
| 62873545 | Master of Dragon Soldier | 55F4 | 157D | 7D15 |
| 99267150 | F.G.D. | 55F8 | 157E | 7E15 |
| 25652259 | Queen's Knight | 55FC | 157F | 7F15 |
| 62651957 | X-Head Cannon | 5600 | 1580 | 8015 |
| 98045062 | Enemy Controller | 5604 | 1581 | 8115 |
| 24530661 | Master Kyonshee | 5608 | 1582 | 8215 |
| 51934376 | Kabazauls | 560C | 1583 | 8315 |
| 97923414 | Inpachi | 5610 | 1584 | 8415 |
| 24317029 | Gravekeeper's Spy | 5614 | 1585 | 8515 |
| 50712728 | Gravekeeper's Curse | 5618 | 1586 | 8615 |
| 37101832 | Gravekeeper's Guard | 561C | 1587 | 8715 |
| 63695531 | Gravekeeper's Spear Soldier | 5620 | 1588 | 8815 |
| 99877698 | Gravekeeper's Cannonholder | 5630 | 158C | 8C15 |
| 25262697 | Gravekeeper's Assailant | 5634 | 158D | 8D15 |
| 51351302 | A Man with Wdjat | 5638 | 158E | 8E15 |
| 98745000 | Mystical Knight of Jackal | 563C | 158F | 8F15 |
| 24140059 | A Cat of Ill Omen | 5640 | 1590 | 9015 |
| 51534754 | Yomi Ship | 5644 | 1591 | 9115 |
| 87523462 | Winged Sage Falcos | 5648 | 1592 | 9215 |
| 23927567 | An Owl of Luck | 564C | 1593 | 9315 |
| 50412166 | Charm of Shabti | 5650 | 1594 | 9415 |
| 86801871 | Cobra Jar | 5654 | 1595 | 9515 |
| 23205979 | Spirit Reaper | 5658 | 1596 | 9615 |
| 59290628 | Nightmare Horse | 565C | 1597 | 9715 |
| 85684223 | Reaper on the Nightmare | 5660 | 1598 | 9815 |
| 12183332 | Card Shuffle | 5664 | 1599 | 9915 |
| 58577036 | Reasoning | 5668 | 159A | 9A15 |
| 85562745 | Dark Room of Nightmare | 566C | 159B | 9B15 |
| 11961740 | Different Dimension Capsule | 5670 | 159C | 9C15 |
| 47355498 | Necrovalley | 5674 | 159D | 9D15 |
| 84740193 | Buster Rancher | 5678 | 159E | 9E15 |
| 10248192 | Hieroglyph Lithograph | 567C | 159F | 9F15 |
| 47233801 | Dark Snake Syndrome | 5680 | 15A0 | A015 |
| 73628505 | Terraforming | 5684 | 15A1 | A115 |
| 10012614 | Banner of Courage | 5688 | 15A2 | A215 |
| 46411259 | Metamorphosis | 568C | 15A3 | A315 |
| 72405967 | Royal Tribute | 5690 | 15A4 | A415 |
| 05990062 | Reversal Quiz | 5694 | 15A5 | A515 |
| 41398771 | Curse of Aging | 5698 | 15A6 | A615 |
| 04178474 | Raigeki Break | 56A0 | 15A8 | A815 |
| 77561728 | Disturbance Strategy | 56A8 | 15AA | AA15 |
| 30450531 | Rite of Spirit | 56B0 | 15AC | AC15 |
| 76848240 | Non Aggression Area | 56B4 | 15AD | AD15 |
| 02833249 | D. Tribe | 56B8 | 15AE | AE15 |
| 65622692 | Y-Dragon Head | 56C0 | 15B0 | B015 |
| 02111707 | XY-Dragon Cannon | 56C4 | 15B1 | B115 |
| 64500000 | Z-Metal Tank | 56CC | 15B3 | B315 |
| 91998119 | XYZ-Dragon Cannon | 56D0 | 15B4 | B415 |
| 37383714 | Rope of Spirit | 56D4 | 15B5 | B515 |
| 64788463 | King's Knight | 56D8 | 15B6 | B615 |
| 90876561 | Jack's Knight | 56DC | 15B7 | B715 |
| 36261276 | Interdimensional Matter Transporter | 56E0 | 15B8 | B815 |
| 63665875 | Goblin Zombie | 56E4 | 15B9 | B915 |
| 99050989 | Drillago | 56E8 | 15BA | BA15 |
| 62543393 | Lekunga | 56F0 | 15BC | BC15 |
| 23265313 | Cost Down | 571C | 15C7 | C715 |
| 12143771 | People Running About | 5728 | 15CA | CA15 |
| 58538870 | Oppressed People | 572C | 15CB | CB15 |
| 85936485 | United Resistance | 5730 | 15CC | CC15 |
| 11321183 | Dark Blade | 5734 | 15CD | CD15 |
| 47415292 | Pitch-Dark Dragon | 5738 | 15CE | CE15 |
| 84814897 | Kiryu | 573C | 15CF | CF15 |
| 10209545 | Decayed Commander | 5740 | 15D0 | D015 |
| 47693640 | Zombie Tiger | 5744 | 15D1 | D115 |
| 73698349 | Giant Orc | 5748 | 15D2 | D215 |
| 19086954 | Second Goblin | 574C | 15D3 | D315 |
| 46571052 | Vampire Orchis | 5750 | 15D4 | D415 |
| 12965761 | Des Dendle | 5754 | 15D5 | D515 |
| 59364406 | Burning Beast | 5758 | 15D6 | D615 |
| 85359414 | Freezing Beast | 575C | 15D7 | D715 |
| 48148828 | D.D. Crazy Beast | 5764 | 15D9 | D915 |
| 84636823 | Spell Canceller | 5768 | 15DA | DA15 |
| 47025270 | Helping Robo For Combat | 5770 | 15DC | DC15 |
| 73414375 | Dimension Jar | 5774 | 15DD | DD15 |
| 46303688 | Roulette Barrel | 577C | 15DF | DF15 |
| 73398797 | Paladin of White Dragon | 5780 | 15E0 | E015 |
| 09786492 | White Dragon Ritual | 5784 | 15E1 | E115 |
| 46181000 | Frontline Base | 5788 | 15E2 | E215 |
| 72575145 | Demotion | 578C | 15E3 | E315 |
| 08964854 | Combination Attack | 5790 | 15E4 | E415 |
| 71453557 | Autonomous Action Unit | 5798 | 15E6 | E615 |
| 08842266 | Poison of the Old Man | 579C | 15E7 | E715 |
| 70231910 | Dark Core | 57A4 | 15E9 | E915 |
| 07625614 | Raregold Armor | 57A8 | 15EA | EA15 |
| 60519422 | Kishido Spirit | 57B0 | 15EC | EC15 |
| 02903036 | Tribute Doll | 57B4 | 15ED | ED15 |
| 38992735 | Wave-Motion Cannon | 57B8 | 15EE | EE15 |
| 65396880 | Huge Revolution | 57BC | 15EF | EF15 |
| 91781589 | Thunder of Ruler | 57C0 | 15F0 | F015 |
| 38275183 | Spell Shield Type-8 | 57C4 | 15F1 | F115 |
| 64274292 | Meteorain | 57C8 | 15F2 | F215 |
| 90669991 | Pineapple Blast | 57CC | 15F3 | F315 |
| 27053506 | Secret Barrel | 57D0 | 15F4 | F415 |
| 26931058 | Formation Union | 57DC | 15F7 | F715 |
| 62325062 | Adhesion Trap Hole | 57E0 | 15F8 | F815 |
| 99724761 | XZ-Tank Cannon | 57E4 | 15F9 | F915 |
| 25119460 | YZ-Tank Dragon | 57E8 | 15FA | FA15 |
| 52503575 | Final Attack Orders | 57EC | 15FB | FB15 |
| 98502113 | Dark Paladin | 57F0 | 15FC | FC15 |
| 51481927 | Spell Absorption | 57F8 | 15FE | FE15 |
| 87880531 | Diffusion Wave-Motion | 57FC | 15FF | FF15 |
| 24874630 | Fiend's Sanctuary | 5800 | 1600 | 0016 |
| 11813953 | Great Angus | 5824 | 1609 | 0916 |
| 48202661 | Aitsu | 5828 | 160A | 0A16 |
| 84696266 | Sonic Duck | 582C | 160B | 0B16 |
| 11091375 | Luster Dragon | 5830 | 160C | 0C16 |
| 47480070 | Amazoness Paladin | 5834 | 160D | 0D16 |
| 73574678 | Amazoness Blowpiper | 5838 | 160E | 0E16 |
| 10979723 | Amazoness Tiger | 583C | 160F | 0F16 |
| 46363422 | Skilled White Magician | 5840 | 1610 | 1016 |
| 73752131 | Skilled Dark Magician | 5844 | 1611 | 1116 |
| 09156135 | Apprentice Magician | 5848 | 1612 | 1216 |
| 45141844 | Old Vindictive Magician | 584C | 1613 | 1316 |
| 72630549 | Chaos Command Magician | 5850 | 1614 | 1416 |
| 08034697 | Magical Marionette | 5854 | 1615 | 1516 |
| 71413901 | Breaker the Magical Warrior | 585C | 1617 | 1716 |
| 07802006 | Magical Plant Mandragola | 5860 | 1618 | 1816 |
| 34206604 | Magical Scientist | 5864 | 1619 | 1916 |
| 70791313 | Royal Magical Library | 5868 | 161A | 1A16 |
| 07180418 | Armor Exe | 586C | 161B | 1B16 |
| 33184167 | Tribe-Infecting Virus | 5870 | 161C | 1C16 |
| 69579761 | Des Koala | 5874 | 161D | 1D16 |
| 06967870 | Cliff the Trap Remover | 5878 | 161E | 1E16 |
| 32362575 | Magical Merchant | 587C | 161F | 1F16 |
| 69456283 | Koitsu | 5880 | 1620 | 2016 |
| 95841282 | Cat's Ear Tribe | 5884 | 1621 | 2116 |
| 32240937 | Ultimate Obedient Fiend | 5888 | 1622 | 2216 |
| 34029630 | Pitch-Black Power Stone | 5890 | 1624 | 2416 |
| 61127349 | Big Bang Shot | 5894 | 1625 | 2516 |
| 07512044 | Gather Your Mind | 5898 | 1626 | 2616 |
| 34906152 | Mass Driver | 589C | 1627 | 2716 |
| 60391791 | Senri Eye | 58A0 | 1628 | 2816 |
| 06390406 | Emblem of Dragon Destroyer | 58A4 | 1629 | 2916 |
| 33784505 | Jar Robber | 58A8 | 162A | 2A16 |
| 32062913 | Mega Ton Magical Cannon | 58B4 | 162D | 2D16 |
| 68057622 | Continuous Destruction Punch | 58B8 | 162E | 2E16 |
| 95451366 | Exhausting Spell | 58BC | 162F | 2F16 |
| 21840375 | Hidden Book of Spell | 58C0 | 1630 | 3016 |
| 68334074 | Miracle Restoring | 58C4 | 1631 | 3116 |
| 20727787 | Disarmament | 58CC | 1633 | 3316 |
| 53112492 | Anti-Spell | 58D0 | 1634 | 3416 |
| 99517131 | The Spell Absorbing Life | 58D4 | 1635 | 3516 |
| 26905245 | Metal Reflect Slime | 58D8 | 1636 | 3616 |
| 52090844 | Bowganian | 58DC | 1637 | 3716 |
| 98494543 | Excavation of Mage Stones | 58E0 | 1638 | 3816 |
| 13944422 | Granadora | 58FC | 163F | 3F16 |
| 86327225 | Shinato, King of a Higher Plane | 5904 | 1641 | 4116 |
| 13722870 | Dark Flare Knight | 5908 | 1642 | 4216 |
| 49217579 | Mirage Knight | 590C | 1643 | 4316 |
| 85605684 | Berserk Dragon | 5910 | 1644 | 4416 |
| 12600382 | Exodia Necross | 5914 | 1645 | 4516 |
| 48094997 | Battle Footballer | 5918 | 1646 | 4616 |
| 85489096 | Arsenal Summoner | 591C | 1647 | 4716 |
| 11987744 | Nin-Ken Dog | 5920 | 1648 | 4816 |
| 47372349 | Acrobat Monkey | 5924 | 1649 | 4916 |
| 74367458 | Guardian Elma | 5928 | 164A | 4A16 |
| 10755153 | Guardian Ceal | 592C | 164B | 4B16 |
| 47150851 | Guardian Grarl | 5930 | 164C | 4C16 |
| 73544866 | Guardian Baou | 5934 | 164D | 4D16 |
| 09633505 | Guardian Kay'est | 5938 | 164E | 4E16 |
| 46037213 | Guardian Tryce | 593C | 164F | 4F16 |
| 09817927 | Gyaku-Gire Panda | 5944 | 1651 | 5116 |
| 35215622 | Blindly Loyal Goblin | 5948 | 1652 | 5216 |
| 71200730 | Despair from the Dark | 594C | 1653 | 5316 |
| 08794435 | Maju Garzett | 5950 | 1654 | 5416 |
| 34193084 | Fear from the Dark | 5954 | 1655 | 5516 |
| 61587183 | Dark Scorpion - Chick the Yellow | 5958 | 1656 | 5616 |
| 07572887 | D.D. Warrior Lady | 595C | 1657 | 5716 |
| 33977496 | Thousand Needles | 5960 | 1658 | 5816 |
| 60365591 | Shinato's Ark | 5964 | 1659 | 5916 |
| 06850209 | A Deal with Dark Ruler | 5968 | 165A | 5A16 |
| 33244944 | Contract with Exodia | 596C | 165B | 5B16 |
| 69243953 | Butterfly Dagger - Elma | 5970 | 165C | 5C16 |
| 95638658 | Shooting Star Bow - Ceal | 5974 | 165D | 5D16 |
| 32022366 | Gravity Axe - Grarl | 5978 | 165E | 5E16 |
| 68427465 | Wicked-Breaking Flamberge - Baou | 597C | 165F | 5F16 |
| 95515060 | Rod of Silence - Kay'est | 5980 | 1660 | 6016 |
| 21900719 | Twin Swords of Flashing Light - Tryce | 5984 | 1661 | 6116 |
| 68304813 | Precious Cards from Beyond | 5988 | 1662 | 6216 |
| 94793422 | Rod of the Mind's Eye | 598C | 1663 | 6316 |
| 20188127 | Fairy of the Spring | 5990 | 1664 | 6416 |
| 57182235 | Token Thanksgiving | 5994 | 1665 | 6516 |
| 20065549 | Non-Spellcasting Area | 599C | 1667 | 6716 |
| 92854392 | Staunch Defender | 59A4 | 1669 | 6916 |
| 29843091 | Ojama Trio | 59A8 | 166A | 6A16 |
| 55348096 | Arsenal Robber | 59AC | 166B | 6B16 |
| 82732705 | Skill Drain | 59B0 | 166C | 6C16 |
| 28121403 | Really Eternal Rest | 59B4 | 166D | 6D16 |
| 81510157 | Soul Taker | 59BC | 166F | 6F16 |
| 28553439 | Magical Dimension | 59E0 | 1678 | 7816 |
| 55948544 | Judgement of Pharaoh | 59E4 | 1679 | 7916 |
| 81332143 | Friendship | 59E8 | 167A | 7A16 |
| 14731897 | Unity | 59EC | 167B | 7B16 |
| 50725996 | Dark Magician Knight | 59F0 | 167C | 7C16 |
| 87210505 | Knight's Title | 59F4 | 167D | 7D16 |
| 13604200 | Sage's Stone | 59F8 | 167E | 7E16 |
| 49003308 | Gagagigo | 59FC | 167F | 7F16 |
| 86498013 | D. D. Trainer | 5A00 | 1680 | 8016 |
| 12482652 | Ojama Green | 5A04 | 1681 | 8116 |
| 49881766 | Archfiend Soldier | 5A08 | 1682 | 8216 |
| 75375465 | Pandemonium Watchbear | 5A0C | 1683 | 8316 |
| 11760174 | Sasuke Samurai #2 | 5A10 | 1684 | 8416 |
| 48768179 | Dark Scorpion - Gorg the Strong | 5A14 | 1685 | 8516 |
| 74153887 | Dark Scorpion - Meanae the Thorn | 5A18 | 1686 | 8616 |
| 11548522 | Outstanding Dog Marron | 5A1C | 1687 | 8716 |
| 47942531 | Great Maju Garzett | 5A20 | 1688 | 8816 |
| 73431236 | Iron Blacksmith Kotetsu | 5A24 | 1689 | 8916 |
| 46820049 | Mefist the Infernal General | 5A2C | 168B | 8B16 |
| 73219648 | Vilepawn Archfiend | 5A30 | 168C | 8C16 |
| 09603356 | Shadowknight Archfiend | 5A34 | 168D | 8D16 |
| 35798491 | Darkbishop Archfiend | 5A38 | 168E | 8E16 |
| 72192100 | Desrook Archfiend | 5A3C | 168F | 8F16 |
| 08581705 | Infernalqueen Archfiend | 5A40 | 1690 | 9016 |
| 35975813 | Terrorking Archfiend | 5A44 | 1691 | 9116 |
| 61370518 | Skull Archfiend of Lightning | 5A48 | 1692 | 9216 |
| 07369217 | Metallizing Parasite - Lunatite | 5A4C | 1693 | 9316 |
| 34853266 | Tsukuyomi | 5A50 | 1694 | 9416 |
| 60258960 | Legendary Flame Lord | 5A54 | 1695 | 9516 |
| 97642679 | Dark Master - Zorc | 5A58 | 1696 | 9616 |
| 33031674 | Incandescent Ordeal | 5A5C | 1697 | 9716 |
| 69035382 | Contract with the Abyss | 5A60 | 1698 | 9816 |
| 96420087 | Contract with the Dark Master | 5A64 | 1699 | 9916 |
| 32919136 | Falling Down | 5A68 | 169A | 9A16 |
| 69313735 | Checkmate | 5A6C | 169B | 9B16 |
| 95308449 | Final Countdown | 5A70 | 169C | 9C16 |
| 68191243 | Mustering of the Dark Scorpions | 5A78 | 169E | 9E16 |
| 94585852 | Pandemonium | 5A7C | 169F | 9F16 |
| 21070956 | Altar for Tribute | 5A80 | 16A0 | A016 |
| 57069605 | Frozen Soul | 5A84 | 16A1 | A116 |
| 94463200 | Battle-Scarred | 5A88 | 16A2 | A216 |
| 20858318 | Dark Scorpion Combination | 5A8C | 16A3 | A316 |
| 56246017 | Archfiend's Roar | 5A90 | 16A4 | A416 |
| 83241722 | Dice Re-Roll | 5A94 | 16A5 | A516 |
| 29735721 | Spell Vanishing | 5A98 | 16A6 | A616 |
| 56120475 | Sakuretsu Armor | 5A9C | 16A7 | A716 |
| 82529174 | Ray of Hope | 5AA0 | 16A8 | A816 |
| 81306586 | Nightmare Penguin | 5AAC | 16AB | AB16 |
| 18891691 | Perfect Machine King | 5AB0 | 16AC | AC16 |
| 16956455 | Chiron the Mage | 5AC8 | 16B2 | B216 |
| 42941100 | Ojama Yellow | 5ACC | 16B3 | B316 |
| 79335209 | Ojama Black | 5AD0 | 16B4 | B416 |
| 15734813 | Soul Tiger | 5AD4 | 16B5 | B516 |
| 42129512 | Big Koala | 5AD8 | 16B6 | B616 |
| 78613627 | Des Kangaroo | 5ADC | 16B7 | B716 |
| 14618326 | Crimson Ninja | 5AE0 | 16B8 | B816 |
| 41006930 | Strike Ninja | 5AE4 | 16B9 | B916 |
| 77491079 | Gale Lizard | 5AE8 | 16BA | BA16 |
| 40884383 | Chopman the Desperate Outlaw | 5AF0 | 16BC | BC16 |
| 77379481 | Sasuke Samurai #3 | 5AF4 | 16BD | BD16 |
| 03773196 | D. D. Scout Plane | 5AF8 | 16BE | BE16 |
| 39168895 | Berserk Gorilla | 5AFC | 16BF | BF16 |
| 16556849 | Freed the Brave Wanderer | 5B00 | 16C0 | C016 |
| 75946257 | Witch Doctor of Chaos | 5B08 | 16C2 | C216 |
| 01434352 | Chaos Necromancer | 5B0C | 16C3 | C316 |
| 47829960 | Chaosrider Gustaph | 5B10 | 16C4 | C416 |
| 74823665 | Inferno | 5B14 | 16C5 | C516 |
| 00218704 | Fenrir | 5B18 | 16C6 | C616 |
| 47606319 | Gigantes | 5B1C | 16C7 | C716 |
| 73001017 | Silpheed | 5B20 | 16C8 | C816 |
| 09596126 | Chaos Sorcerer | 5B24 | 16C9 | C916 |
| 36584821 | Gren Maju Da Eiza | 5B28 | 16CA | CA16 |
| 72989439 | Black Luster Soldier - Envoy of the Beginning | 5B2C | 16CB | CB16 |
| 09373534 | Fuhma Shuriken | 5B30 | 16CC | CC16 |
| 35762283 | Heart of the Underdog | 5B34 | 16CD | CD16 |
| 61166988 | Wild Nature's Release | 5B38 | 16CE | CE16 |
| 08251996 | Ojama Delta Hurricane!! | 5B3C | 16CF | CF16 |
| 34646691 | Stumbling | 5B40 | 16D0 | D016 |
| 61044390 | Chaos End | 5B44 | 16D1 | D116 |
| 97439308 | Chaos Greed | 5B48 | 16D2 | D216 |
| 60912752 | D. D. Borderline | 5B50 | 16D4 | D416 |
| 96316857 | Recycle | 5B54 | 16D5 | D516 |
| 23701465 | Primal Seed | 5B58 | 16D6 | D616 |
| 69196160 | Thunder Crash | 5B5C | 16D7 | D716 |
| 95194279 | Dimension Distortion | 5B60 | 16D8 | D816 |
| 22589918 | Reload | 5B64 | 16D9 | D916 |
| 68073522 | Soul Absorption | 5B68 | 16DA | DA16 |
| 95472621 | Big Burn | 5B6C | 16DB | DB16 |
| 21466326 | Blasting the Ruins | 5B70 | 16DC | DC16 |
| 58851034 | Cursed Seal of the Forbidden Spell | 5B74 | 16DD | DD16 |
| 94256039 | Tower of Babel | 5B78 | 16DE | DE16 |
| 20644748 | Spatial Collapse | 5B7C | 16DF | DF16 |
| 57139487 | Chain Disappearance | 5B80 | 16E0 | E016 |
| 83133491 | Zero Gravity | 5B84 | 16E1 | E116 |
| 20522190 | Dark Mirror Force | 5B88 | 16E2 | E216 |
| 56916805 | Energy Drain | 5B8C | 16E3 | E316 |
| 82301904 | Chaos Emperor Dragon - Envoy of the End | 5B90 | 16E4 | E416 |
| 44910027 | Victory D. | 5BB0 | 16EC | EC16 |
| 80304126 | Magician's Valkyrie | 5BB4 | 16ED | ED16 |
| 43793530 | Giga Gagagigo | 5BBC | 16EF | EF16 |
| 79182538 | Mad Dog of Darkness | 5BC0 | 16F0 | F016 |
| 16587243 | Neo Bug | 5BC4 | 16F1 | F116 |
| 42071342 | Sea Serpent Warrior of Darkness | 5BC8 | 16F2 | F216 |
| 78060096 | Terrorking Salmon | 5BCC | 16F3 | F316 |
| 05464695 | Blazing Inpachi | 5BD0 | 16F4 | F416 |
| 41859700 | Burning Algae | 5BD4 | 16F5 | F516 |
| 78243409 | The Thing in the Crater | 5BD8 | 16F6 | F616 |
| 04732017 | Molten Zombie | 5BDC | 16F7 | F716 |
| 40737112 | Dark Magician of Chaos | 5BE0 | 16F8 | F816 |
| 77121851 | Manticore of Darkness | 5BE4 | 16F9 | F916 |
| 03510565 | Stealth Bird | 5BE8 | 16FA | FA16 |
| 30914564 | Sacred Crane | 5BEC | 16FB | FB16 |
| 76909279 | Enraged Battle Ox | 5BF0 | 16FC | FC16 |
| 03493978 | Don Turtle | 5BF4 | 16FD | FD16 |
| 65287621 | Dark Driceratops | 5BFC | 16FF | FF16 |
| 02671330 | Hyper Hammerhead | 5C00 | 1700 | 0017 |
| 38670435 | Black Tyranno | 5C04 | 1701 | 0117 |
| 65064143 | Anti-Aircraft Flower | 5C08 | 1702 | 0217 |
| 91559748 | Prickle Fairy | 5C0C | 1703 | 0317 |
| 37957847 | Insect Princess | 5C10 | 1704 | 0417 |
| 64342551 | Amphibious Bugroth MK-3 | 5C14 | 1705 | 0517 |
| 90337190 | Torpedo Fish | 5C18 | 1706 | 0617 |
| 37721209 | Levia-Dragon - Daedalus | 5C1C | 1707 | 0717 |
| 63120904 | Orca Mega-Fortress of Darkness | 5C20 | 1708 | 0817 |
| 95614612 | Cannonball Spear Shellfish | 5C24 | 1709 | 0917 |
| 22609617 | Mataza the Zapper | 5C28 | 170A | 0A17 |
| 68007326 | Guardian Angel Joan | 5C2C | 170B | 0B17 |
| 95492061 | Manju of the Ten Thousand Hands | 5C30 | 170C | 0C17 |
| 21887179 | Getsu Fuhma | 5C34 | 170D | 0D17 |
| 57281778 | Ryu Kokki | 5C38 | 170E | 0E17 |
| 34370473 | Gryphon's Feather Duster | 5C3C | 170F | 0F17 |
| 60764581 | Stray Lambs | 5C40 | 1710 | 1017 |
| 97169186 | Smashing Ground | 5C44 | 1711 | 1117 |
| 23557835 | Dimension Fusion | 5C48 | 1712 | 1217 |
| 69542930 | Dedication through Light and Darkness | 5C4C | 1713 | 1317 |
| 96947648 | Salvage | 5C50 | 1714 | 1417 |
| 22431243 | Ultra Evolution Pill | 5C54 | 1715 | 1517 |
| 59820352 | Earth Chant | 5C58 | 1716 | 1617 |
| 95214051 | Jade Insect Whistle | 5C5C | 1717 | 1717 |
| 21219755 | Destruction Ring | 5C60 | 1718 | 1817 |
| 58607704 | Fiend's Hand Mirror | 5C64 | 1719 | 1917 |
| 94192409 | Compulsory Evacuation Device | 5C68 | 171A | 1A17 |
| 21597117 | A Hero Emerges | 5C6C | 171B | 1B17 |
| 57585212 | Self-Destruct Button | 5C70 | 171C | 1C17 |
| 84970821 | Curse of Darkness | 5C74 | 171D | 1D17 |
| 20374520 | Begone, Knave! | 5C78 | 171E | 1E17 |
| 56769674 | DNA Transplant | 5C7C | 171F | 1F17 |
| 83258273 | Robbin' Zombie | 5C80 | 1720 | 2017 |
| 19252988 | Trap Jammer | 5C84 | 1721 | 2117 |
| 56647086 | Invader of Darkness | 5C88 | 1722 | 2217 |
| 82035781 | Twinheaded Beast | 5C8C | 1723 | 2317 |
| 18318842 | Abyss Soldier | 5C9C | 1727 | 2717 |
| 17185260 | Inferno Hammer | 5CA8 | 172A | 2A17 |
| 43580269 | Emes the Infinity | 5CAC | 172B | 2B17 |
| 70074904 | D. D. Assailant | 5CB0 | 172C | 2C17 |
| 16469012 | Teva | 5CB4 | 172D | 2D17 |
| 79852326 | Skull Zoma | 5CBC | 172F | 2F17 |
| 30707994 | Maximum Six | 5CDC | 1737 | 3717 |
| 76895648 | Dangerous Machine TYPE-6 | 5CE0 | 1738 | 3817 |
| 03280747 | Sixth Sense | 5CE4 | 1739 | 3917 |
| 39674352 | Gogiga Gagagigo | 5CE8 | 173A | 3A17 |
| 66073051 | Warrior of Zera | 5CEC | 173B | 3B17 |
| 02468169 | Sealmaster Meisei | 5CF0 | 173C | 3C17 |
| 39552864 | Mystical Shine Ball | 5CF4 | 173D | 3D17 |
| 65957473 | Metal Armored Bug | 5CF8 | 173E | 3E17 |
| 91345518 | The Agent of Judgment - Saturn | 5CFC | 173F | 3F17 |
| 38730226 | The Agent of Wisdom - Mercury | 5D00 | 1740 | 4017 |
| 64734921 | The Agent of Creation - Venus | 5D04 | 1741 | 4117 |
| 91123920 | The Agent of Force - Mars | 5D08 | 1742 | 4217 |
| 27618634 | The Unhappy Girl | 5D0C | 1743 | 4317 |
| 63012333 | Soul-Absorbing Bone Tower | 5D10 | 1744 | 4417 |
| 90407382 | The Kick Man | 5D14 | 1745 | 4517 |
| 26495087 | Vampire Lady | 5D18 | 1746 | 4617 |
| 53890795 | Rocket Jumper | 5D1C | 1747 | 4717 |
| 99284890 | Avatar of The Pot | 5D20 | 1748 | 4817 |
| 25773409 | Legendary Jujitsu Master | 5D24 | 1749 | 4917 |
| 52768103 | KA-2 Des Scissors | 5D28 | 174A | 4A17 |
| 98162242 | Needle Burrower | 5D2C | 174B | 4B17 |
| 25551951 | Blowback Dragon | 5D30 | 174C | 4C17 |
| 51945556 | Zaborg the Thunder Monarch | 5D34 | 174D | 4D17 |
| 87340664 | Atomic Firefly | 5D38 | 174E | 4E17 |
| 24435369 | Mermaid Knight | 5D3C | 174F | 4F17 |
| 50823978 | Piranha Army | 5D40 | 1750 | 5017 |
| 83228073 | Two Thousand Needles | 5D44 | 1751 | 5117 |
| 19612721 | Disc Fighter | 5D48 | 1752 | 5217 |
| 55001420 | Arcane Archer of the Forest | 5D4C | 1753 | 5317 |
| 82005435 | Lady Ninja Yae | 5D50 | 1754 | 5417 |
| 18590133 | Goblin King | 5D54 | 1755 | 5517 |
| 45985838 | Solar Flare Dragon | 5D58 | 1756 | 5617 |
| 81383947 | White Magician Pikeru | 5D5C | 1757 | 5717 |
| 18378582 | Archlord Zerato | 5D60 | 1758 | 5817 |
| 44762290 | Opti-Camouflage Armor | 5D64 | 1759 | 5917 |
| 80161395 | Mystik Wok | 5D68 | 175A | 5A17 |
| 17655904 | Burst Stream of Destruction | 5D6C | 175B | 5B17 |
| 43040603 | Monster Gate | 5D70 | 175C | 5C17 |
| 56433456 | The Sanctuary in the Sky | 5D78 | 175E | 5E17 |
| 82828051 | Earthquake | 5D7C | 175F | 5F17 |
| 45311864 | Goblin Thief | 5D84 | 1761 | 6117 |
| 82705573 | Backfire | 5D88 | 1762 | 6217 |
| 18190572 | Micro Ray | 5D8C | 1763 | 6317 |
| 44595286 | Light of Judgment | 5D90 | 1764 | 6417 |
| 17078030 | Wall of Revealing Light | 5D98 | 1766 | 6617 |
| 44472639 | Solar Ray | 5D9C | 1767 | 6717 |
| 70861343 | Ninjitsu Art of Transformation | 5DA0 | 1768 | 6817 |
| 16255442 | Beckoning Light | 5DA4 | 1769 | 6917 |
| 43250041 | Draining Shield | 5DA8 | 176A | 6A17 |
| 79649195 | Armor Break | 5DAC | 176B | 6B17 |
| 06133894 | Mazera DeVille | 5DB0 | 176C | 6C17 |
| 31305911 | Marshmallon | 5DC0 | 1770 | 7017 |
| 78700060 | Skull Descovery Knight | 5DC4 | 1771 | 7117 |
| 30683373 | Shield Crash | 5DCC | 1773 | 7317 |
| 03072077 | Return Zombie | 5DD4 | 1775 | 7517 |
| 30461781 | Corpse of Yata-Garasu | 5DD8 | 1776 | 7617 |
| 66865880 | Marshmallon glasses | 5DDC | 1777 | 7717 |
| 65743242 | Earthbound Spirit's Invitation | 5DE8 | 177A | 7A17 |
| 27288416 | Mokey Mokey | 5E08 | 1782 | 8217 |
| 53776525 | Gigobyte | 5E0C | 1783 | 8317 |
| 99171160 | Kozaky | 5E10 | 1784 | 8417 |
| 26566878 | Fiend Scorpion | 5E14 | 1785 | 8517 |
| 52550973 | Pharaoh's Servant | 5E18 | 1786 | 8617 |
| 89959682 | Pharaonic Protector | 5E1C | 1787 | 8717 |
| 25343280 | Spirit of the Pharaoh | 5E20 | 1788 | 8817 |
| 51838385 | Theban Nightmare | 5E24 | 1789 | 8917 |
| 88236094 | Aswan Apparition | 5E28 | 178A | 8A17 |
| 24221739 | Protector of the Sanctuary | 5E2C | 178B | 8B17 |
| 51616747 | Nubian Guard | 5E30 | 178C | 8C17 |
| 13409151 | Desertapir | 5E38 | 178E | 8E17 |
| 50593156 | Sand Gambler | 5E3C | 178F | 8F17 |
| 13386503 | Ghost Knight of Jackal | 5E44 | 1791 | 9117 |
| 49771608 | Absorbing Kid from the Sky | 5E48 | 1792 | 9217 |
| 85166216 | Elephant Statue of Blessing | 5E4C | 1793 | 9317 |
| 12160911 | Elephant Statue of Disaster | 5E50 | 1794 | 9417 |
| 48659020 | Spirit Caller | 5E54 | 1795 | 9517 |
| 75043725 | Emissary of the Afterlife | 5E58 | 1796 | 9617 |
| 44436472 | Double Coston | 5E60 | 1798 | 9817 |
| 70821187 | Regenerating Mummy | 5E64 | 1799 | 9917 |
| 16226786 | Night Assailant | 5E68 | 179A | 9A17 |
| 43714890 | Man-Thro' Tro' | 5E6C | 179B | 9B17 |
| 79109599 | King of the Swamp | 5E70 | 179C | 9C17 |
| 06103294 | Emissary of the Oasis | 5E74 | 179D | 9D17 |
| 42598242 | Special Hurricane | 5E78 | 179E | 9E17 |
| 78986941 | Order to Charge | 5E7C | 179F | 9F17 |
| 05371656 | Sword of the Soul-Eater | 5E80 | 17A0 | A017 |
| 31476755 | Dust Barrier | 5E84 | 17A1 | A117 |
| 78864369 | Soul Reversal | 5E88 | 17A2 | A217 |
| 04259068 | Spell Economics | 5E8C | 17A3 | A317 |
| 67048711 | 7 | 5E94 | 17A5 | A517 |
| 03136426 | Level Limit - Area B | 5E98 | 17A6 | A617 |
| 30531525 | Enchanting Fitting Room | 5E9C | 17A7 | A717 |
| 66926224 | The Law of the Normal | 5EA0 | 17A8 | A817 |
| 02314238 | Dark Magic Attack | 5EA4 | 17A9 | A917 |
| 39719977 | Delta Attacker | 5EA8 | 17AA | AA17 |
| 05703682 | Thousand Energy | 5EAC | 17AB | AB17 |
| 32298781 | Triangle Power | 5EB0 | 17AC | AC17 |
| 78697395 | The Third Sarcophagus | 5EB4 | 17AD | AD17 |
| 04081094 | The Second Sarcophagus | 5EB8 | 17AE | AE17 |
| 31076103 | The First Sarcophagus | 5EBC | 17AF | AF17 |
| 30353551 | Human-Wave Tactics | 5EC8 | 17B2 | B217 |
| 66742250 | Curse of Anubis | 5ECC | 17B3 | B317 |
| 93747864 | Desert Sunlight | 5ED0 | 17B4 | B417 |
| 39131963 | Des Counterblow | 5ED4 | 17B5 | B517 |
| 66526672 | Labyrinth of Nightmare | 5ED8 | 17B6 | B617 |
| 92924317 | Soul Resurrection | 5EDC | 17B7 | B717 |
| 39019325 | Order to Smash | 5EE0 | 17B8 | B817 |
| 65403020 | The End of Anubis | 5EE4 | 17B9 | B917 |
| 64681432 | Crush D. Gandra | 5EF0 | 17BC | BC17 |
| 27174286 | Return from the Different Dimension | 5EF8 | 17BE | BE17 |
| 53569894 | Pyramid of Light | 5EFC | 17BF | BF17 |
| 53347303 | Blue-Eyes Shining Dragon | 5F08 | 17C2 | C217 |
| 89731911 | Familiar Knight | 5F0C | 17C3 | C317 |
| 25236056 | Rare Metal Dragon | 5F10 | 17C4 | C417 |
| 52624755 | Peten the Dark Clown | 5F14 | 17C5 | C517 |
| 88619463 | Sorcerer of Dark Magic | 5F18 | 17C6 | C617 |
| 15013468 | Andro Sphinx | 5F1C | 17C7 | C717 |
| 51402177 | Sphinx Teleia | 5F20 | 17C8 | C817 |
| 87997872 | Theinen the Great Sphinx | 5F24 | 17C9 | C917 |
| 14391920 | Inferno Tempest | 5F28 | 17CA | CA17 |
| 87774234 | Watapon | 5F30 | 17CC | CC17 |
| 13179332 | Charcoal Inpachi | 5F34 | 17CD | CD17 |
| 49563947 | Neo Aqua Madoor | 5F38 | 17CE | CE17 |
| 86652646 | Skull Dog Marron | 5F3C | 17CF | CF17 |
| 12057781 | Goblin Calligrapher | 5F40 | 17D0 | D017 |
| 49441499 | Ultimate Insect LV1 | 5F44 | 17D1 | D117 |
| 75830094 | Horus the Black Flame Dragon LV4 | 5F48 | 17D2 | D217 |
| 11224103 | Horus the Black Flame Dragon LV6 | 5F4C | 17D3 | D317 |
| 48229808 | Horus the Black Flame Dragon LV8 | 5F50 | 17D4 | D417 |
| 74713516 | Dark Mimic LV1 | 5F54 | 17D5 | D517 |
| 01102515 | Dark Mimic LV3 | 5F58 | 17D6 | D617 |
| 47507260 | Mystic Swordsman LV2 | 5F5C | 17D7 | D717 |
| 74591968 | Mystic Swordsman LV4 | 5F60 | 17D8 | D817 |
| 00980973 | Armed Dragon LV3 | 5F64 | 17D9 | D917 |
| 46384672 | Armed Dragon LV5 | 5F68 | 17DA | DA17 |
| 73879377 | Armed Dragon LV7 | 5F6C | 17DB | DB17 |
| 09264485 | Horus' Servant | 5F70 | 17DC | DC17 |
| 36262024 | Red-Eyes B. Chick | 5F74 | 17DD | DD17 |
| 04041838 | Ninja Grandmaster Sasuke | 5F7C | 17DF | DF17 |
| 31440542 | Rafflesia Seduction | 5F80 | 17E0 | E017 |
| 67934141 | Ultimate Baseball Kid | 5F84 | 17E1 | E117 |
| 04929256 | Mobius the Frost Monarch | 5F88 | 17E2 | E217 |
| 30314994 | Element Dragon | 5F8C | 17E3 | E317 |
| 66712593 | Element Soldier | 5F90 | 17E4 | E417 |
| 93107608 | Howling Insect | 5F94 | 17E5 | E517 |
| 39191307 | Masked Dragon | 5F98 | 17E6 | E617 |
| 66690411 | Mind on Air | 5F9C | 17E7 | E717 |
| 92084010 | Unshaven Angler | 5FA0 | 17E8 | E817 |
| 38479725 | The Trojan Horse | 5FA4 | 17E9 | E917 |
| 65878864 | Nobleman-Eater Bug | 5FA8 | 17EA | EA17 |
| 91862578 | Enraged Muka Muka | 5FAC | 17EB | EB17 |
| 28357177 | Hade-Hane | 5FB0 | 17EC | EC17 |
| 64751286 | Penumbral Soldier Lady | 5FB4 | 17ED | ED17 |
| 90140980 | Ojama King | 5FB8 | 17EE | EE17 |
| 27134689 | Master of Oz | 5FBC | 17EF | EF17 |
| 53539634 | Sanwitch | 5FC0 | 17F0 | F017 |
| 90928333 | Dark Factory of Mass Production | 5FC4 | 17F1 | F117 |
| 26412047 | Hammer Shot | 5FC8 | 17F2 | F217 |
| 52817046 | Mind Wipe | 5FCC | 17F3 | F317 |
| 89801755 | Abyssal Designator | 5FD0 | 17F4 | F417 |
| 25290459 | Level Up! | 5FD4 | 17F5 | F517 |
| 52684508 | Inferno Fire Blast | 5FD8 | 17F6 | F617 |
| 88089103 | The Graveyard in the Fourth Dimension | 5FDC | 17F7 | F717 |
| 25578802 | Two-Man Cell Battle | 5FE0 | 17F8 | F817 |
| 51562916 | Big Wave Small Wave | 5FE4 | 17F9 | F917 |
| 27967615 | Fusion Weapon | 5FE8 | 17FA | FA17 |
| 54351224 | Ritual Weapon | 5FEC | 17FB | FB17 |
| 90740329 | Taunt | 5FF0 | 17FC | FC17 |
| 27744077 | Absolute End | 5FF4 | 17FD | FD17 |
| 53239672 | Spirit Barrier | 5FF8 | 17FE | FE17 |
| 89628781 | Ninjitsu Art of Decoy | 5FFC | 17FF | FF17 |
| 26022485 | Enervating Mist | 6000 | 1800 | 0018 |
| 52417194 | Heavy Slump | 6004 | 1801 | 0118 |
| 89405199 | Greed | 6008 | 1802 | 0218 |
| 51394546 | Cemetary Bomb | 6010 | 1804 | 0418 |
| 88789641 | Hallowed Life Barrier | 6014 | 1805 | 0518 |
| 14778250 | The Tricky | 6018 | 1806 | 0618 |
| 41172955 | Green Gadget | 601C | 1807 | 0718 |
| 13955608 | Stronghold | 6024 | 1809 | 0918 |
| 86445415 | Red Gadget | 602C | 180B | 0B18 |
| 13839120 | Yellow Gadget | 6030 | 180C | 0C18 |
| 75622824 | Tricky's Magic 4 | 6038 | 180E | 0E18 |
| 48115277 | The Blockman | 6040 | 1810 | 1018 |
| 01995985 | Silent Swordsman LV3 | 6048 | 1812 | 1218 |
| 74388798 | Silent Swordsman LV5 | 6050 | 1814 | 1418 |
| 37267041 | Silent Swordsman LV7 | 6058 | 1816 | 1618 |
| 73665146 | Silent Magician LV4 | 605C | 1817 | 1718 |
| 00050755 | Magician's Circle | 6060 | 1818 | 1818 |
| 36045450 | Magician's Unite | 6064 | 1819 | 1918 |
| 72443568 | Silent Magician LV8 | 6068 | 181A | 1A18 |
| 35322812 | Woodborg Inpachi | 6070 | 181C | 1C18 |
| 62327910 | Mighty Guard | 6074 | 181D | 1D18 |
| 08715625 | Bokoichi the Freightening Car | 6078 | 181E | 1E18 |
| 34100324 | Harpie Girl | 607C | 181F | 1F18 |
| 61505339 | The Creator | 6080 | 1820 | 2018 |
| 97093037 | The Creator Incarnate | 6084 | 1821 | 2118 |
| 34088136 | Ultimate Insect LV3 | 6088 | 1822 | 2218 |
| 60482781 | Mystic Swordsman LV6 | 608C | 1823 | 2318 |
| 23265594 | Heavy Mech Support Platform | 6094 | 1825 | 2518 |
| 65260293 | Element Magician | 6098 | 1826 | 2618 |
| 92755808 | Element Saurus | 609C | 1827 | 2718 |
| 28143906 | Roc from the Valley of Haze | 60A0 | 1828 | 2818 |
| 64538655 | Sasuke Samurai #4 | 60A4 | 1829 | 2918 |
| 91932350 | Harpie Lady 1 | 60A8 | 182A | 2A18 |
| 27927359 | Harpie Lady 2 | 60AC | 182B | 2B18 |
| 54415063 | Harpie Lady 3 | 60B0 | 182C | 2C18 |
| 90810762 | Raging Flame Sprite | 60B4 | 182D | 2D18 |
| 26205777 | Thestalos the Firestorm Monarch | 60B8 | 182E | 2E18 |
| 53693416 | Eagle Eye | 60BC | 182F | 2F18 |
| 89698120 | Tactical Espionage Expert | 60C0 | 1830 | 3018 |
| 26082229 | Invasion of Flames | 60C4 | 1831 | 3118 |
| 52571838 | Creeping Doom Manta | 60C8 | 1832 | 3218 |
| 88975532 | Pitch-Black Warwolf | 60CC | 1833 | 3318 |
| 15960641 | Mirage Dragon | 60D0 | 1834 | 3418 |
| 51355346 | Gaia Soul the Combustible Collective | 60D4 | 1835 | 3518 |
| 88753985 | Fox Fire | 60D8 | 1836 | 3618 |
| 14148099 | Big Core | 60DC | 1837 | 3718 |
| 51632798 | Fusilier Dragon, the Dual-Mode Beast | 60E0 | 1838 | 3818 |
| 87621407 | Dekoichi the Battlechanted Locomotive | 60E4 | 1839 | 3918 |
| 13026402 | A-Team: Trap Disposal Unit | 60E8 | 183A | 3A18 |
| 40410110 | Homunculus the Alchemic Being | 60EC | 183B | 3B18 |
| 86805855 | Dark Blade the Dragon Knight | 60F0 | 183C | 3C18 |
| 13803864 | Mokey Mokey King | 60F4 | 183D | 3D18 |
| 49398568 | Serial Spell | 60F8 | 183E | 3E18 |
| 75782277 | Harpies' Hunting Ground | 60FC | 183F | 3F18 |
| 12181376 | Triangle Ecstasy Spark | 6100 | 1840 | 4018 |
| 48576971 | Necklace of Command | 6104 | 1841 | 4118 |
| 75560629 | Flint | 6108 | 1842 | 4218 |
| 01965724 | Mokey Mokey Smackdown | 610C | 1843 | 4318 |
| 47453433 | Back to Square One | 6110 | 1844 | 4418 |
| 74848038 | Monster Reincarnation | 6114 | 1845 | 4518 |
| 00242146 | Ballista of Rampart Smashing | 6118 | 1846 | 4618 |
| 37231841 | Lighten the Load | 611C | 1847 | 4718 |
| 13626450 | Malice Dispersion | 6120 | 1848 | 4818 |
| 49010598 | Divine Wrath | 6124 | 1849 | 4918 |
| 76515293 | Xing Zhen Hu | 6128 | 184A | 4A18 |
| 12503902 | Rare Metalmorph | 612C | 184B | 4B18 |
| 75392615 | Mind Haxorz | 6134 | 184D | 4D18 |
| 01781310 | Fuh-Rin-Ka-Zan | 6138 | 184E | 4E18 |
| 48276469 | Chain Burst | 613C | 184F | 4F18 |
| 74270067 | Pikeru's Circle of Enchantment | 6140 | 1850 | 5018 |
| 01669772 | Spell Purification | 6144 | 1851 | 5118 |
| 37053871 | Astral Barrier | 6148 | 1852 | 5218 |
| 74458486 | Covering Fire | 614C | 1853 | 5318 |
| 36931229 | Castle Gate | 6154 | 1855 | 5518 |
| 09720537 | Owner's Seal | 615C | 1857 | 5718 |
| 36119641 | Space Mambo | 6160 | 1858 | 5818 |
| 62113340 | Divine Dragon Ragnarok | 6164 | 1859 | 5918 |
| 08508055 | Chu-Ske the Mouse Fighter | 6168 | 185A | 5A18 |
| 35052053 | Insect Knight | 616C | 185B | 5B18 |
| 61441708 | Sacred Phoenix of Nephthys | 6170 | 185C | 5C18 |
| 98446407 | Hand of Nephthys | 6174 | 185D | 5D18 |
| 34830502 | Ultimate Insect LV5 | 6178 | 185E | 5E18 |
| 60229110 | Granmarg the Rock Monarch | 617C | 185F | 5F18 |
| 97623219 | Element Valkyrie | 6180 | 1860 | 6018 |
| 23118924 | Element Doom | 6184 | 1861 | 6118 |
| 60102563 | Maji-Gire Panda | 6188 | 1862 | 6218 |
| 96501677 | Catnipped Kitty | 618C | 1863 | 6318 |
| 22996376 | Behemoth the King of All Animals | 6190 | 1864 | 6418 |
| 59380081 | Big-Tusked Mammoth | 6194 | 1865 | 6518 |
| 95789089 | Kangaroo Champ | 6198 | 1866 | 6618 |
| 22873798 | Hyena | 619C | 1867 | 6718 |
| 58268433 | Blade Rabbit | 61A0 | 1868 | 6818 |
| 94667532 | Mecha-Dog Marron | 61A4 | 1869 | 6918 |
| 21051146 | Blast Magician | 61A8 | 186A | 6A18 |
| 57046845 | Gearfried the Swordmaster | 61AC | 186B | 6B18 |
| 84430950 | Armed Samurai - Ben Kei | 61B0 | 186C | 6C18 |
| 20939559 | Shadowslayer | 61B4 | 186D | 6D18 |
| 52323207 | Golem Sentry | 61B8 | 186E | 6E18 |
| 89718302 | Abare Ushioni | 61BC | 186F | 6F18 |
| 15717011 | The Light - Hex-Sealed Fusion | 61C0 | 1870 | 7018 |
| 52101615 | The Dark - Hex-Sealed Fusion | 61C4 | 1871 | 7118 |
| 88696724 | The Earth - Hex-Sealed Fusion | 61C8 | 1872 | 7218 |
| 15090429 | Whirlwind Prodigy | 61CC | 1873 | 7318 |
| 41089128 | Flame Ruler | 61D0 | 1874 | 7418 |
| 87473172 | Firebird | 61D4 | 1875 | 7518 |
| 14878871 | Rescue Cat | 61D8 | 1876 | 7618 |
| 40267580 | Brain Jacker | 61DC | 1877 | 7718 |
| 87751584 | Gatling Dragon | 61E0 | 1878 | 7818 |
| 13756293 | King Dragun | 61E4 | 1879 | 7918 |
| 49140998 | A Feather of the Phoenix | 61E8 | 187A | 7A18 |
| 76539047 | Poison Fangs | 61EC | 187B | 7B18 |
| 12923641 | Swords of Concealing Light | 61F0 | 187C | 7C18 |
| 49328340 | Spiral Spear Strike | 61F4 | 187D | 7D18 |
| 75417459 | Release Restraint | 61F8 | 187E | 7E18 |
| 01801154 | Centrifugal Field | 61FC | 187F | 7F18 |
| 48206762 | Fulfillment of the Contract | 6200 | 1880 | 8018 |
| 74694807 | Re-Fusion | 6204 | 1881 | 8118 |
| 01689516 | The Big March of Animals | 6208 | 1882 | 8218 |
| 37083210 | Cross Counter | 620C | 1883 | 8318 |
| 36361633 | Threatening Roar | 6218 | 1886 | 8618 |
| 63356631 | Phoenix Wing Wind Blast | 621C | 1887 | 8718 |
| 09744376 | Good Goblin Housekeeping | 6220 | 1888 | 8818 |
| 35149085 | Beast Soul Swap | 6224 | 1889 | 8918 |
| 62633180 | Assault on GHQ | 6228 | 188A | 8A18 |
| 08628798 | D.D. Dynamite | 622C | 188B | 8B18 |
| 35027493 | Deck Devastation Virus | 6230 | 188C | 8C18 |
| 61411502 | Elemental Burst | 6234 | 188D | 8D18 |
| 97806240 | Forced Ceasefire | 6238 | 188E | 8E18 |
| 34294855 | Curse of Vampire | 623C | 188F | 8F18 |
| 60399954 | Union Attack | 6240 | 1890 | 9018 |
| 97783659 | Blood Sucker | 6244 | 1891 | 9118 |
| 60577362 | Overpowering Eye | 624C | 1893 | 9318 |
| 96561011 | Red-Eyes Darkness Dragon | 6250 | 1894 | 9418 |
| 22056710 | Vampire Genesis | 6254 | 1895 | 9518 |
| 34627841 | Kaibaman | 6268 | 189A | 9A18 |
| 21844576 | Elemental Hero Avian | 6298 | 18A6 | A618 |
| 58932615 | Elemental Hero Burstinatrix | 629C | 18A7 | A718 |
| 84327329 | Elemental Hero Clayman | 62A0 | 18A8 | A818 |
| 20721928 | Elemental Hero Sparkman | 62A4 | 18A9 | A918 |
| 57116033 | Winged Kuriboh | 62A8 | 18AA | AA18 |
| 83104731 | Ancient Gear Golem | 62AC | 18AB | AB18 |
| 10509340 | Ancient Gear Beast | 62B0 | 18AC | AC18 |
| 56094445 | Ancient Gear Soldier | 62B4 | 18AD | AD18 |
| 82482194 | Millennium Scorpion | 62B8 | 18AE | AE18 |
| 19877898 | Ultimate Insect LV7 | 62BC | 18AF | AF18 |
| 45871897 | Lost Guardian | 62C0 | 18B0 | B018 |
| 82260502 | Hieracosphinx | 62C4 | 18B1 | B118 |
| 18654201 | Criosphinx | 62C8 | 18B2 | B218 |
| 45159319 | Moai Interceptor Cannons | 62CC | 18B3 | B318 |
| 71544954 | Megarock Dragon | 62D0 | 18B4 | B418 |
| 13532663 | Dummy Golem | 62D4 | 18B5 | B518 |
| 40937767 | Grave Ohja | 62D8 | 18B6 | B618 |
| 76321376 | Mine Golem | 62DC | 18B7 | B718 |
| 03810071 | Monk Fighter | 62E0 | 18B8 | B818 |
| 49814180 | Master Monk | 62E4 | 18B9 | B918 |
| 75209824 | Guardian Statue | 62E8 | 18BA | BA18 |
| 02694423 | Medusa Worm | 62EC | 18BB | BB18 |
| 48092532 | D.D. Survivor | 62F0 | 18BC | BC18 |
| 75487237 | Mid Shield Gardna | 62F4 | 18BD | BD18 |
| 01571945 | White Ninja | 62F8 | 18BE | BE18 |
| 37970940 | Aussa the Earth Charmer | 62FC | 18BF | BF18 |
| 74364659 | Eria the Water Charmer | 6300 | 18C0 | C018 |
| 00759393 | Hiita the Fire Charmer | 6304 | 18C1 | C118 |
| 37744402 | Wynn the Wind Charmer | 6308 | 18C2 | C218 |
| 63142001 | Batteryman AA | 630C | 18C3 | C318 |
| 09637706 | Des Wombat | 6310 | 18C4 | C418 |
| 36021814 | King of the Skull Servants | 6314 | 18C5 | C518 |
| 62420419 | Reshef the Dark Being | 6318 | 18C6 | C618 |
| 99414168 | Elemental Mistress Doriado | 631C | 18C7 | C718 |
| 35809262 | Elemental Hero Flame Wingman | 6320 | 18C8 | C818 |
| 61204971 | Elemental Hero Thunder Giant | 6324 | 18C9 | C918 |
| 98792570 | Gift of the Martyr | 6328 | 18CA | CA18 |
| 34187685 | Double Attack | 632C | 18CB | CB18 |
| 61181383 | Battery Charger | 6330 | 18CC | CC18 |
| 97570038 | Kaminote Blow | 6334 | 18CD | CD18 |
| 23965037 | Doriado's Blessing | 6338 | 18CE | CE18 |
| 60369732 | Final Ritual of the Ancients | 633C | 18CF | CF18 |
| 96458440 | Legendary Black Belt | 6340 | 18D0 | D018 |
| 23842445 | Nitro Unit | 6344 | 18D1 | D118 |
| 59237154 | Shifting Shadows | 6348 | 18D2 | D218 |
| 96631852 | Impenetrable Formation | 634C | 18D3 | D318 |
| 22020907 | Hero Signal | 6350 | 18D4 | D418 |
| 58015506 | Pikeru's Second Sight | 6354 | 18D5 | D518 |
| 85519211 | Minefield Eruption | 6358 | 18D6 | D618 |
| 21908319 | Kozaky's Self-Destruct Button | 635C | 18D7 | D718 |
| 58392024 | Mispolymerization | 6360 | 18D8 | D818 |
| 84397023 | Level Conversion Lab | 6364 | 18D9 | D918 |
| 20781762 | Rock Bombardment | 6368 | 18DA | DA18 |
| 83675475 | Token Feastevil | 6370 | 18DC | DC18 |
| 10069180 | Spell-Stopping Statute | 6374 | 18DD | DD18 |
| 56058888 | Royal Surrender | 6378 | 18DE | DE18 |
| 19847532 | Infernal Flame Emperor | 6380 | 18E0 | E018 |
| 57902462 | Holy Knight Ishzark | 6398 | 18E6 | E618 |
| 10485110 | Ocean Dragon Lord - Neo-Daedalus | 63A0 | 18E8 | E818 |
| 45945685 | Cycroid | 63BC | 18EF | EF18 |
| 71930383 | Patroid | 63C0 | 18F0 | F018 |
| 18325492 | Gyroid | 63C4 | 18F1 | F118 |
| 44729197 | Steamroid | 63C8 | 18F2 | F218 |
| 71218746 | Drillroid | 63CC | 18F3 | F318 |
| 07602840 | UFOroid | 63D0 | 18F4 | F418 |
| 43697559 | Jetroid | 63D4 | 18F5 | F518 |
| 70095154 | Cyber Dragon | 63D8 | 18F6 | F618 |
| 06480253 | Wroughtweiler | 63DC | 18F7 | F718 |
| 79979666 | Elemental Hero Bubbleman | 63E4 | 18F9 | F918 |
| 05368615 | Steam Gyroid | 63E8 | 18FA | FA18 |
| 32752319 | UFOroid Fighter | 63EC | 18FB | FB18 |
| 74157028 | Cyber Twin Dragon | 63F0 | 18FC | FC18 |
| 01546123 | Cyber End Dragon | 63F4 | 18FD | FD18 |
| 37630732 | Power Bond | 63F8 | 18FE | FE18 |
| 63035430 | Skyscraper | 63FC | 18FF | FF18 |
| 00423585 | Summon Priest | 6400 | 1900 | 0019 |
| 62180201 | Dark Dreadroute | 6414 | 1905 | 0519 |
| 98585345 | Winged Kuriboh LV10 | 6418 | 1906 | 0619 |
| 25573054 | Transcendent Wings | 641C | 1907 | 0719 |
| 61968753 | Bubble Shuffle | 6420 | 1908 | 0819 |
| 97362768 | Spark Blaster | 6424 | 1909 | 0919 |
| 24857466 | Dark Ruler Vandalgyon | 6428 | 190A | 0A19 |
| 60246171 | Soitsu | 642C | 190B | 0B19 |
| 97240270 | Mad Lobster | 6430 | 190C | 0C19 |
| 23635815 | Jerry Beans Man | 6434 | 190D | 0D19 |
| 59023523 | Cybernetic Magician | 6438 | 190E | 0E19 |
| 96428622 | Cybernetic Cyclopean | 643C | 190F | 0F19 |
| 22512237 | Mechanical Hound | 6440 | 1910 | 1019 |
| 59907935 | Cyber Archfiend | 6444 | 1911 | 1119 |
| 85306040 | Goblin Elite Attack Force | 6448 | 1912 | 1219 |
| 22790789 | B.E.S. Crystal Core | 644C | 1913 | 1319 |
| 58185394 | Giant Kozaky | 6450 | 1914 | 1419 |
| 84173492 | Indomitable Fighter Lei Lei | 6454 | 1915 | 1519 |
| 11678191 | Protective Soul Ailin | 6458 | 1916 | 1619 |
| 57062206 | Doitsu | 645C | 1917 | 1719 |
| 84451804 | Des Frog | 6460 | 1918 | 1819 |
| 10456559 | T.A.D.P.O.L.E. | 6464 | 1919 | 1919 |
| 56840658 | Poison Draw Frog | 6468 | 191A | 1A19 |
| 83235263 | Tyranno Infinity | 646C | 191B | 1B19 |
| 19733961 | Batteryman C | 6470 | 191C | 1C19 |
| 46128076 | Ebon Magician Curran | 6474 | 191D | 1D19 |
| 82112775 | D.D.M. - Different Dimension Master | 6478 | 191E | 1E19 |
| 18511384 | Fusion Recovery | 647C | 191F | 1F19 |
| 45906428 | Miracle Fusion | 6480 | 1920 | 2019 |
| 71490127 | Dragon's Mirror | 6484 | 1921 | 2119 |
| 18895832 | System Down | 6488 | 1922 | 2219 |
| 44883830 | Des Croaking | 648C | 1923 | 2319 |
| 70278545 | Pot of Generosity | 6490 | 1924 | 2419 |
| 07672244 | Shien's Spy | 6494 | 1925 | 2519 |
| 43061293 | Fire Darts | 6498 | 1926 | 2619 |
| 70156997 | Spiritual Earth Art - Kurogane | 649C | 1927 | 2719 |
| 06540606 | Spiritual Water Art - Aoi | 64A0 | 1928 | 2819 |
| 42945701 | Spiritual Fire Art - Kurenai | 64A4 | 1929 | 2919 |
| 79333300 | Spiritual Wind Art - Miyabi | 64A8 | 192A | 2A19 |
| 05728014 | A Rival Appears! | 64AC | 192B | 2B19 |
| 32723153 | Magical Explosion | 64B0 | 192C | 2C19 |
| 78211862 | Rising Energy | 64B4 | 192D | 2D19 |
| 05606466 | D.D. Trap Hole | 64B8 | 192E | 2E19 |
| 31000575 | Conscription | 64BC | 192F | 2F19 |
| 67095270 | Dimension Wall | 64C0 | 1930 | 3019 |
| 04483989 | Prepare to Strike Back | 64C4 | 1931 | 3119 |
| 30888983 | Triage | 64C8 | 1932 | 3219 |
| 06150044 | Alkana Knight Joker | 64D8 | 1936 | 3619 |
| 69933858 | Gilford the Legend | 64E0 | 1938 | 3819 |
| 05438492 | Warrior Lady of the Wasteland | 64E4 | 1939 | 3919 |
| 31423101 | Divine Sword - Phoenix Blade | 64E8 | 193A | 3A19 |
| 25366484 | Elemental Hero Shining Flare Wingman | 650C | 1943 | 4319 |
| 61850482 | Level Modulation | 6510 | 1944 | 4419 |
| 98259197 | Ojamuscle | 6514 | 1945 | 4519 |
| 24643836 | Ojamagic | 6518 | 1946 | 4619 |
| 51638941 | V-Tiger Jet | 651C | 1947 | 4719 |
| 97023549 | Blade Skater | 6520 | 1948 | 4819 |
| 23421244 | Reborn Zombie | 6524 | 1949 | 4919 |
| 96300057 | W-Wing Catapult | 652C | 194B | 4B19 |
| 59793705 | Elemental Hero Bladedge | 6534 | 194D | 4D19 |
| 86188410 | Elemental Hero Wildheart | 6538 | 194E | 4E19 |
| 22587018 | Hydrogeddon | 653C | 194F | 4F19 |
| 58071123 | Oxygeddon | 6540 | 1950 | 5019 |
| 85066822 | Water Dragon | 6544 | 1951 | 5119 |
| 11460577 | Etoile Cyber | 6548 | 1952 | 5219 |
| 58859575 | VW-Tiger Catapult | 654C | 1953 | 5319 |
| 84243274 | VWXYZ-Dragon Catapult Cannon | 6550 | 1954 | 5419 |
| 10248389 | Cyber Blader | 6554 | 1955 | 5519 |
| 47737087 | Elemental Hero Rampart Blaster | 6558 | 1956 | 5619 |
| 83121692 | Elemental Hero Tempest | 655C | 1957 | 5719 |
| 10526791 | Elemental Hero Wildedge | 6560 | 1958 | 5819 |
| 46910446 | Chthonian Alliance | 6564 | 1959 | 5919 |
| 19394153 | Feather Shot | 656C | 195B | 5B19 |
| 45898858 | Bonding - H2O | 6570 | 195C | 5C19 |
| 72287557 | Chthonian Polymer | 6574 | 195D | 5D19 |
| 18271561 | Chthonian Blast | 6578 | 195E | 5E19 |
| 44676200 | Hero Barrier | 657C | 195F | 5F19 |
| 71060915 | Feather Wind | 6580 | 1960 | 6019 |
| 07459013 | Zure, Knight of Dark World | 6584 | 1961 | 6119 |
| 44954628 | B.E.S. Tetran | 6588 | 1962 | 6219 |
| 70948327 | Nanobreaker | 658C | 1963 | 6319 |
| 06337436 | Rapid-Fire Magician | 6590 | 1964 | 6419 |
| 33731070 | Beiige, Vanguard of Dark World | 6594 | 1965 | 6519 |
| 79126789 | Broww, Huntsman of Dark World | 6598 | 1966 | 6619 |
| 06214884 | Brron, Mad King of Dark World | 659C | 1967 | 6719 |
| 32619583 | Sillva, Warlord of Dark World | 65A0 | 1968 | 6819 |
| 78004197 | Goldd, Wu-Lord of Dark World | 65A4 | 1969 | 6919 |
| 05498296 | Scarr, Scout of Dark World | 65A8 | 196A | 6A19 |
| 31887905 | Familiar-Possessed - Aussa | 65AC | 196B | 6B19 |
| 68881649 | Familiar-Possessed - Eria | 65B0 | 196C | 6C19 |
| 04376658 | Familiar-Possessed - Hiita | 65B4 | 196D | 6D19 |
| 31764353 | Familiar-Possessed - Wynn | 65B8 | 196E | 6E19 |
| 67169062 | Pot of Avarice | 65BC | 196F | 6F19 |
| 93554166 | Dark World Lightning | 65C0 | 1970 | 7019 |
| 66947414 | Boss Rush | 65C8 | 1972 | 7219 |
| 93431518 | Gateway to Dark World | 65CC | 1973 | 7319 |
| 29826127 | The Forces of Darkness | 65D0 | 1974 | 7419 |
| 65824822 | Dark Deal | 65D4 | 1975 | 7519 |
| 92219931 | Simultaneous Loss | 65D8 | 1976 | 7619 |
| 28604635 | Weed Out | 65DC | 1977 | 7719 |
| 55008284 | The League of Uniform Nomenclature | 65E0 | 1978 | 7819 |
| 91597389 | Roll Out! | 65E4 | 1979 | 7919 |
| 27581098 | Non-Fusion Area | 65E8 | 197A | 7A19 |
| 54976796 | Level Limit - Area A | 65EC | 197B | 7B19 |
| 90374791 | Armed Changer | 65F0 | 197C | 7C19 |
| 89252153 | Elemental Hero Necroshade | 65FC | 197F | 7F19 |
| 26647858 | Hero Heyro | 6600 | 1980 | 8019 |
| 52031567 | Elemental Hero Madballman | 6604 | 1981 | 8119 |
| 29436665 | Dark Eradicator Warlock | 6608 | 1982 | 8219 |
| 55424270 | Mythical Beast Cerberus | 660C | 1983 | 8319 |
| 91819979 | Magical Blast | 6610 | 1984 | 8419 |
| 81197327 | Elemental Hero Steam Healer | 661C | 1987 | 8719 |
| 27191436 | Burst Return | 6620 | 1988 | 8819 |
| 53586134 | Bubble Blaster | 6624 | 1989 | 8919 |
| 80075749 | Bubble Illusion | 6628 | 198A | 8A19 |
| 22479888 | Clay Charge | 662C | 198B | 8B19 |
| 59464593 | Armed Dragon LV10 | 6630 | 198C | 8C19 |
| 85852291 | Magical Mallet | 6634 | 198D | 8D19 |
| 12247206 | Inferno Reckless Summon | 6638 | 198E | 8E19 |
| 11125718 | Rancer Dragonute | 6644 | 1991 | 9119 |
| 47529357 | Mistobody | 6648 | 1992 | 9219 |
| 84914462 | Axe Dragonute | 664C | 1993 | 9319 |
| 73891874 | White Horns D. | 6658 | 1996 | 9619 |
| 06007213 | Uria, Lord of Searing Flames | 668C | 19A3 | A319 |
| 32491822 | Hamon, Lord of Striking Thunder | 6690 | 19A4 | A419 |
| 69890967 | Raviel, Lord of Phantasms | 6694 | 19A5 | A519 |
| 05285665 | Elemental Hero Neo Bubbleman | 6698 | 19A6 | A619 |
| 32679370 | Hero Kid | 669C | 19A7 | A719 |
| 68774379 | Cyber Barrier Dragon | 66A0 | 19A8 | A819 |
| 04162088 | Cyber Laser Dragon | 66A4 | 19A9 | A919 |
| 31557782 | Ancient Gear | 66A8 | 19AA | AA19 |
| 67951831 | Hero Heart | 66AC | 19AB | AB19 |
| 94940436 | Magnet Circle LV2 | 66B0 | 19AC | AC19 |
| 67829249 | Ancient Gear Drill | 66B8 | 19AE | AE19 |
| 93224848 | Phantasmal Martyrs | 66BC | 19AF | AF19 |
| 29612557 | Cyclone Boomerang | 66C0 | 19B0 | B019 |
| 66607691 | Photon Generator Unit | 66C4 | 19B1 | B119 |
| 92001300 | Ancient Gear Castle | 66C8 | 19B2 | B219 |
| 55985014 | Miracle Kids | 66D0 | 19B4 | B419 |
| 91989718 | Attack Reflector Unit | 66D4 | 19B5 | B519 |
| 28378427 | Damage Condenser | 66D8 | 19B6 | B619 |
| 80045583 | Ancient Gear Cannon | 66EC | 19BB | BB19 |
| 26439287 | Proto-Cyber Dragon | 66F0 | 19BC | BC19 |
| 53828396 | Adhesive Explosive | 66F4 | 19BD | BD19 |
| 89222931 | Machine King Prototype | 66F8 | 19BE | BE19 |
| 15317640 | B.E.S. Covered Core | 66FC | 19BF | BF19 |
| 52702748 | D.D. Guide | 6700 | 19C0 | C019 |
| 88190453 | Chain Thrasher | 6704 | 19C1 | C119 |
| 15595052 | Disciple of the Forbidden Spell | 6708 | 19C2 | C219 |
| 41589166 | Tenkabito Shien | 670C | 19C3 | C319 |
| 87978805 | Parasitic Ticky | 6710 | 19C4 | C419 |
| 14472500 | Gokipon | 6714 | 19C5 | C519 |
| 40867519 | Silent Insect | 6718 | 19C6 | C619 |
| 77252217 | Chainsaw Insect | 671C | 19C7 | C719 |
| 13250922 | Anteatereatingant | 6720 | 19C8 | C819 |
| 49645921 | Saber Beetle | 6724 | 19C9 | C919 |
| 76039636 | Doom Dozer | 6728 | 19CA | CA19 |
| 12538374 | Treeborn Frog | 672C | 19CB | CB19 |
| 49522489 | Beelze Frog | 6730 | 19CC | CC19 |
| 75917088 | Princess Pikeru | 6734 | 19CD | CD19 |
| 02316186 | Princess Curran | 6738 | 19CE | CE19 |
| 48700891 | Memory Crusher | 673C | 19CF | CF19 |
| 14255590 | Malice Ascendant | 6740 | 19D0 | D019 |
| 41249545 | Grass Phantom | 6744 | 19D1 | D119 |
| 73648243 | Sand Moth | 6748 | 19D2 | D219 |
| 10032958 | Divine Dragon - Excelion | 674C | 19D3 | D319 |
| 46427957 | Ruin, Queen of Oblivion | 6750 | 19D4 | D419 |
| 72426662 | Demise, King of Armageddon | 6754 | 19D5 | D519 |
| 09910360 | D.3.S. Frog | 6758 | 19D6 | D619 |
| 45305419 | Symbol of Heritage | 675C | 19D7 | D719 |
| 72709014 | Trial of the Princesses | 6760 | 19D8 | D819 |
| 08198712 | End of the World | 6764 | 19D9 | D919 |
| 44182827 | Samsara | 6768 | 19DA | DA19 |
| 71587526 | Karma Cut | 676C | 19DB | DB19 |
| 07076131 | Next to be Lost | 6770 | 19DC | DC19 |
| 34460239 | Generation Shift | 6774 | 19DD | DD19 |
| 70865988 | Full Salvo | 6778 | 19DE | DE19 |
| 06859683 | Success Probability 0% | 677C | 19DF | DF19 |
| 33248692 | Option Hunter | 6780 | 19E0 | E019 |
| 69632396 | Goblin Out of the Frying Pan | 6784 | 19E1 | E119 |
| 06137095 | Malfunction | 6788 | 19E2 | E219 |
| 20065322 | The Flute of Summoning Kuriboh | 67B0 | 19EC | EC19 |
| 29343734 | Elemental Hero Erikshieler | 67BC | 19EF | EF19 |
| 55737443 | Guardian Exode | 67C0 | 19F0 | F019 |
| 92736188 | Great Spirit | 67C4 | 19F1 | F119 |
| 28120197 | Fault Zone | 67C8 | 19F2 | F219 |
| 27408609 | Homunculus Gold | 67D4 | 19F5 | F519 |
| 54493213 | The Ancient Sun Helios | 67D8 | 19F6 | F619 |
| 80887952 | Helios Duo Megiste | 67DC | 19F7 | F719 |
| 17286057 | Helios Tris Megiste | 67E0 | 19F8 | F819 |
| 89943723 | Elemental Hero Neos | 67F4 | 19FD | FD19 |
| 15341821 | Dandylion | 67F8 | 19FE | FE19 |
| Blue-Eyes White Dragon | 89631139 |  |  |  |
| Mystical Elf | 15025844 |  |  |  |
| Hitotsu-Me Giant | 76184692 |  |  |  |
| Baby Dragon | 88819587 |  |  |  |
| Ryu-Kishin | 15303296 |  |  |  |
| Feral Imp | 41392891 |  |  |  |
| Winged Dragon, Guardian of the Fortress #1 | 87796900 |  |  |  |
| Mushroom Man | 14181608 |  |  |  |
| Blackland Fire Dragon | 87564352 |  |  |  |
| Tyhone | 72842870 |  |  |  |
| Flame Swordsman | 45231177 |  |  |  |
| Time Wizard | 71625222 |  |  |  |
| Right Leg of the Forbidden One | 08124921 |  |  |  |
| Left Leg of the Forbidden One | 44519536 |  |  |  |
| Right Arm of the Forbidden One | 70903634 |  |  |  |
| Left Arm of the Forbidden One | 07902349 |  |  |  |
| Exodia the Forbidden One | 33396948 |  |  |  |
| Summoned Skull | 70781052 |  |  |  |
| The Wicked Worm Beast | 06285791 |  |  |  |
| Skull Servant | 32274490 |  |  |  |
| Horn Imp | 69669405 |  |  |  |
| Battle Ox | 05053103 |  |  |  |
| Beaver Warrior | 32452818 |  |  |  |
| Rock Ogre Grotto #1 | 68846917 |  |  |  |
| Mountain Warrior | 04931562 |  |  |  |
| Zombie Warrior | 31339260 |  |  |  |
| Koumori Dragon | 67724379 |  |  |  |
| Two-Headed King Rex | 94119974 |  |  |  |
| Judge Man | 30113682 |  |  |  |
| Saggi the Dark Clown | 66602787 |  |  |  |
| Dark Magician | 46986414 |  |  |  |
| The Snake Hair | 29491031 |  |  |  |
| Gaia the Dragon Champion | 66889139 |  |  |  |
| Gaia The Fierce Knight | 06368038 |  |  |  |
| Curse of Dragon | 28279543 |  |  |  |
| Celtic Guardian | 91152256 |  |  |  |
| Illusionist Faceless Mage | 28546905 |  |  |  |
| Karbonala Warrior | 54541900 |  |  |  |
| Rogue Doll | 91939608 |  |  |  |
| Oscillo Hero #2 | 27324313 |  |  |  |
| Griffore | 53829412 |  |  |  |
| Torike | 80813021 |  |  |  |
| Sangan | 26202165 |  |  |  |
| Big Insect | 53606874 |  |  |  |
| Basic Insect | 89091579 |  |  |  |
| Armored Lizard | 15480588 |  |  |  |
| Killer Needle | 88979991 |  |  |  |
| Gokibore | 15367030 |  |  |  |
| Giant Flea | 41762634 |  |  |  |
| Larvae Moth | 87756343 |  |  |  |
| Great Moth | 14141448 |  |  |  |
| Kuriboh | 40640057 |  |  |  |
| Mammoth Graveyard | 40374923 |  |  |  |
| Great White | 13429800 |  |  |  |
| Wolf | 49417509 |  |  |  |
| Harpie Lady | 76812113 |  |  |  |
| Harpie Lady Sisters | 12206212 |  |  |  |
| Tiger Axe | 49791927 |  |  |  |
| Silver Fang | 90357090 |  |  |  |
| Kojikocy | 01184620 |  |  |  |
| Perfectly Ultimate Great Moth | 48579379 |  |  |  |
| Thousand Dragon | 41462083 |  |  |  |
| Fiend Kraken | 77456781 |  |  |  |
| Jellyfish | 14851496 |  |  |  |
| Cocoon of Evolution | 40240595 |  |  |  |
| Giant Soldier of Stone | 13039848 |  |  |  |
| Man-Eating Plant | 49127943 |  |  |  |
| Krokodilus | 76512652 |  |  |  |
| Grappler | 02906250 |  |  |  |
| Axe Raider | 48305365 |  |  |  |
| Megazowler | 75390004 |  |  |  |
| Uraby | 01784619 |  |  |  |
| Crawling Dragon #2 | 38289717 |  |  |  |
| Red-Eyes B. Dragon | 74677422 |  |  |  |
| Castle of Dark Illusions | 00062121 |  |  |  |
| Reaper of the Cards | 33066139 |  |  |  |
| King of Yamimakai | 69455834 |  |  |  |
| Barox | 06840573 |  |  |  |
| Metal Guardian | 68339286 |  |  |  |
| Catapult Turtle | 95727991 |  |  |  |
| Gyakutenno Megami | 31122090 |  |  |  |
| Mystic Horseman | 68516705 |  |  |  |
| Rabid Horseman | 94905343 |  |  |  |
| Crass Clown | 93889755 |  |  |  |
| Armored Zombie | 20277860 |  |  |  |
| Dragon Zombie | 66672569 |  |  |  |
| Clown Zombie | 92667214 |  |  |  |
| Pumpking the King of Ghosts | 29155212 |  |  |  |
| Battle Warrior | 55550921 |  |  |  |
| Wings of Wicked Flame | 92944626 |  |  |  |
| Mask of Darkness | 28933734 |  |  |  |
| Job-Change Mirror | 55337339 |  |  |  |
| Curtain of the Dark Ones | 22026707 |  |  |  |
| Kageningen | 80600490 |  |  |  |
| Graveyard and the Hand of Invitation | 27094595 |  |  |  |
| Goddess with the Third Eye | 53493204 |  |  |  |
| Hero of the East | 89987208 |  |  |  |
| That Which Feeds on Life | 52367652 |  |  |  |
| Dark Gray | 09159938 |  |  |  |
| White Magical Hat | 15150365 |  |  |  |
| Kamionwizard | 41544074 |  |  |  |
| Nightmare Scorpion | 88643173 |  |  |  |
| Spirit of the Books | 14037717 |  |  |  |
| Supporter in the Shadows | 41422426 |  |  |  |
| Trial of Nightmare | 77827521 |  |  |  |
| Dream Clown | 13215230 |  |  |  |
| Sleeping Lion | 40200834 |  |  |  |
| Yamatano Dragon Scroll | 76704943 |  |  |  |
| Faith Bird | 75582395 |  |  |  |
| Nemuriko | 90963488 |  |  |  |
| Weather Control | 37243151 |  |  |  |
| The 13th Grave | 00032864 |  |  |  |
| Charubin the Fire Knight | 37421579 |  |  |  |
| Mystical Capture Chain | 63515678 |  |  |  |
| Fiend's Hand | 52800428 |  |  |  |
| Witty Phantom | 36304921 |  |  |  |
| Dragon Statue | 09197735 |  |  |  |
| Blue-Eyed Silver Zombie | 35282433 |  |  |  |
| Toad Master | 62671448 |  |  |  |
| Spiked Snail | 98075147 |  |  |  |
| Flame Manipulator | 34460851 |  |  |  |
| Necrolancer the Timelord | 61454890 |  |  |  |
| Djinn the Watcher of the Wind | 97843505 |  |  |  |
| The Bewitching Phantom Thief | 24348204 |  |  |  |
| Temple of Skulls | 00732302 |  |  |  |
| Monster Egg | 36121917 |  |  |  |
| The Shadow Who Controls the Dark | 63125616 |  |  |  |
| Lord of the Lamp | 99510761 |  |  |  |
| Rhaimundos of the Red Sword | 62403074 |  |  |  |
| The Melting Red Shadow | 98898173 |  |  |  |
| Dokuroizo the Grim Reaper | 25882881 |  |  |  |
| Fire Reaper | 53581214 |  |  |  |
| Larvas | 94675535 |  |  |  |
| Hard Armor | 20060230 |  |  |  |
| Firegrass | 53293545 |  |  |  |
| Man Eater | 93553943 |  |  |  |
| Dig Beak | 29948642 |  |  |  |
| M-Warrior #1 | 56342351 |  |  |  |
| M-Warrior #2 | 92731455 |  |  |  |
| Lisark | 55210709 |  |  |  |
| Lord of Zemia | 81618817 |  |  |  |
| The Judgement Hand | 28003512 |  |  |  |
| Mysterious Puppeteer | 54098121 |  |  |  |
| Darkfire Dragon | 17881964 |  |  |  |
| Dark King of the Abyss | 53375573 |  |  |  |
| Spirit of the Harp | 80770678 |  |  |  |
| Armaill | 53153481 |  |  |  |
| Dark Prisoner | 89558090 |  |  |  |
| Hurricail | 15042735 |  |  |  |
| Fire Eye | 88435542 |  |  |  |
| Monsturtle | 15820147 |  |  |  |
| Claw Reacher | 41218256 |  |  |  |
| Phantom Dewan | 77603950 |  |  |  |
| Arlownay | 14708569 |  |  |  |
| Dark Shade | 40196604 |  |  |  |
| Masked Clown | 77581312 |  |  |  |
| Lucky Trinket | 03985011 |  |  |  |
| Genin | 49370026 |  |  |  |
| Eyearmor | 64511793 |  |  |  |
| Fiend Reflection #2 | 02863439 |  |  |  |
| Gate Deeg | 49258578 |  |  |  |
| Synchar | 75646173 |  |  |  |
| Fusionist | 01641882 |  |  |  |
| Akakieisu | 38035986 |  |  |  |
| LaLa Li-oon | 09430387 |  |  |  |
| Turtle Tiger | 37313348 |  |  |  |
| Terra the Terrible | 63308047 |  |  |  |
| Doron | 00756652 |  |  |  |
| Arma Knight | 36151751 |  |  |  |
| Happy Lover | 99030164 |  |  |  |
| Penguin Knight | 36039163 |  |  |  |
| Petit Dragon | 75356564 |  |  |  |
| Frenzied Panda | 98818516 |  |  |  |
| Archfiend Marmot of Nefariousness | 75889523 |  |  |  |
| Phantom Ghost | 61201220 |  |  |  |
| Dorover | 24194033 |  |  |  |
| Twin Long Rods #1 | 60589682 |  |  |  |
| Droll Bird | 97973387 |  |  |  |
| Petit Angel | 38142739 |  |  |  |
| Winged Cleaver | 39175982 |  |  |  |
| Hinotama Soul | 96851799 |  |  |  |
| Kaminarikozou | 15510988 |  |  |  |
| Meotoko | 53832650 |  |  |  |
| Aqua Madoor | 85639257 |  |  |  |
| Kagemusha of the Blue Flame | 15401633 |  |  |  |
| Flame Ghost | 58528964 |  |  |  |
| Dryad | 84916669 |  |  |  |
| B. Skull Dragon | 11901678 |  |  |  |
| Two-Mouth Darkruler | 57305373 |  |  |  |
| Solitude | 84794011 |  |  |  |
| Masked Sorcerer | 10189126 |  |  |  |
| Kumootoko | 56283725 |  |  |  |
| Midnight Fiend | 83678433 |  |  |  |
| Trap Master | 46461247 |  |  |  |
| Fiend Sword | 22855882 |  |  |  |
| Skull Stalker | 54844990 |  |  |  |
| Hitodenchak | 46718686 |  |  |  |
| Wood Remains | 17733394 |  |  |  |
| Hourglass of Life | 08783685 |  |  |  |
| Rare Fish | 80516007 |  |  |  |
| Wood Clown | 17511156 |  |  |  |
| Madjinn Gunn | 43905751 |  |  |  |
| Dark Titan of Terror | 89494469 |  |  |  |
| Beautiful Headhuntress | 16899564 |  |  |  |
| Guardian of the Labyrinth | 89272878 |  |  |  |
| Yashinoki | 41061625 |  |  |  |
| Vishwar Randi | 78556320 |  |  |  |
| The Drdek | 08944575 |  |  |  |
| Dark Assailant | 41949033 |  |  |  |
| Candle of Fate | 47695416 |  |  |  |
| Water Element | 03732747 |  |  |  |
| Dissolverock | 40826495 |  |  |  |
| Meda Bat | 76211194 |  |  |  |
| One Who Hunts Souls | 03606209 |  |  |  |
| Root Water | 39004808 |  |  |  |
| Master & Expert | 75499502 |  |  |  |
| Water Omotics | 02483611 |  |  |  |
| Hyo | 38982356 |  |  |  |
| Enchanting Mermaid | 75376965 |  |  |  |
| Nekogal #1 | 01761063 |  |  |  |
| Fairywitch | 37160778 |  |  |  |
| Embryonic Beast | 64154377 |  |  |  |
| Prevent Rat | 00549481 |  |  |  |
| Dimensional Warrior | 37043180 |  |  |  |
| Stone Armadiller | 63432835 |  |  |  |
| Beastking of the Swamps | 99426834 |  |  |  |
| Ancient Sorcerer | 36821538 |  |  |  |
| Lunar Queen Elzaim | 62210247 |  |  |  |
| Wicked Mirror | 15150371 |  |  |  |
| The Little Swordsman of Aile | 25109950 |  |  |  |
| Rock Ogre Grotto #2 | 62193699 |  |  |  |
| Wing Egg Elf | 98582704 |  |  |  |
| The Furious Sea King | 18710707 |  |  |  |
| Princess of Tsurugi | 51371017 |  |  |  |
| Unknown Warrior of Fiend | 97360116 |  |  |  |
| Sectarian of Secrets | 15507080 |  |  |  |
| Versago the Destroyer | 50259460 |  |  |  |
| Wetha | 96643568 |  |  |  |
| Megirus Light | 23032273 |  |  |  |
| Mavelus | 59036972 |  |  |  |
| Ancient Tree of Enlightenment | 86421986 |  |  |  |
| Green Phantom King | 22910685 |  |  |  |
| Ground Attacker Bugroth | 58314394 |  |  |  |
| Ray & Temperature | 85309439 |  |  |  |
| Gorgon Egg | 11793047 |  |  |  |
| Petit Moth | 58192742 |  |  |  |
| King Fog | 84686841 |  |  |  |
| Protector of the Throne | 10071456 |  |  |  |
| Mystic Clown | 47060154 |  |  |  |
| Mystical Sheep #2 | 83464209 |  |  |  |
| Holograh | 10859908 |  |  |  |
| Tao the Chanter | 46247516 |  |  |  |
| Serpent Marauder | 82742611 |  |  |  |
| Ogre of the Black Shadow | 45121025 |  |  |  |
| Moon Envoy | 45909477 |  |  |  |
| Fireyarou | 71407486 |  |  |  |
| Psychic Kappa | 07892180 |  |  |  |
| Masaki the Legendary Swordsman | 44287299 |  |  |  |
| Dragoness the Wicked Knight | 70681994 |  |  |  |
| Bio Plant | 07670542 |  |  |  |
| One-Eyed Shield Dragon | 33064647 |  |  |  |
| Cyber Soldier of Darkworld | 75559356 |  |  |  |
| Wicked Dragon with the Ersatz Head | 02957055 |  |  |  |
| Sonic Maid | 38942059 |  |  |  |
| Kurama | 85705804 |  |  |  |
| Axe of Despair | 40619825 |  |  |  |
| Insect Armor with Laser Cannon | 03492538 |  |  |  |
| Black Pendant | 65169794 |  |  |  |
| Horn of Light | 38552107 |  |  |  |
| Horn of the Unicorn | 64047146 |  |  |  |
| Elegant Egotist | 90219263 |  |  |  |
| Stop Defense | 63102017 |  |  |  |
| Malevolent Nuzzler | 99597615 |  |  |  |
| Dragon Capture Jar | 50045299 |  |  |  |
| Forest | 87430998 |  |  |  |
| Wasteland | 23424603 |  |  |  |
| Mountain | 50913601 |  |  |  |
| Sogen | 86318356 |  |  |  |
| Umi | 22702055 |  |  |  |
| Yami | 59197169 |  |  |  |
| Dark Hole | 53129443 |  |  |  |
| Raigeki | 12580477 |  |  |  |
| Mooyan Curry | 58074572 |  |  |  |
| Red Medicine | 38199696 |  |  |  |
| Goblin's Secret Remedy | 11868825 |  |  |  |
| Soul of the Pure | 47852924 |  |  |  |
| Dian Keto the Cure Master | 84257639 |  |  |  |
| Sparks | 76103675 |  |  |  |
| Ookazi | 19523799 |  |  |  |
| Tremendous Fire | 46918794 |  |  |  |
| Swords of Revealing Light | 72302403 |  |  |  |
| Spellbinding Circle | 18807108 |  |  |  |
| Dark-Piercing Light | 45895206 |  |  |  |
| Yaranzo | 71280811 |  |  |  |
| Kanan the Swordmistress | 12829151 |  |  |  |
| Takriminos | 44073668 |  |  |  |
| Stuffed Animal | 71068263 |  |  |  |
| Super War-Lion | 33951077 |  |  |  |
| Three-Legged Zombies | 33734439 |  |  |  |
| Zera The Mant | 69123138 |  |  |  |
| Flying Penguin | 05628232 |  |  |  |
| Millennium Shield | 32012841 |  |  |  |
| Fairy's Gift | 68401546 |  |  |  |
| Black Luster Soldier | 05405694 |  |  |  |
| Fiend's Mirror | 31890399 |  |  |  |
| Labyrinth Wall | 67284908 |  |  |  |
| Jirai Gumo | 94773007 |  |  |  |
| Shadow Ghoul | 30778711 |  |  |  |
| Wall Shadow | 63162310 |  |  |  |
| Labyrinth Tank | 99551425 |  |  |  |
| Sanga of the Thunder | 25955164 |  |  |  |
| Kazejin | 62340868 |  |  |  |
| Suijin | 98434877 |  |  |  |
| Gate Guardian | 25833572 |  |  |  |
| Ryu-Kishin Powered | 24611934 |  |  |  |
| Swordstalker | 50005633 |  |  |  |
| La Jinn the Mystical Genie of the Lamp | 97590747 |  |  |  |
| Blue-Eyes Ultimate Dragon | 23995346 |  |  |  |
| Toon Alligator | 59383041 |  |  |  |
| Parrot Dragon | 62762898 |  |  |  |
| Dark Rabbit | 99261403 |  |  |  |
| Bickuribox | 25655502 |  |  |  |
| Harpie's Pet Dragon | 52040216 |  |  |  |
| Pendulum Machine | 24433920 |  |  |  |
| Giltia the D. Knight | 51828629 |  |  |  |
| Launcher Spider | 87322377 |  |  |  |
| Zoa | 24311372 |  |  |  |
| Metalzoa | 50705071 |  |  |  |
| Ocubeam | 86088138 |  |  |  |
| Monster Eye | 84133008 |  |  |  |
| Yaiba Robo | 10315429 |  |  |  |
| Machine King | 46700124 |  |  |  |
| Metal Dragon | 09293977 |  |  |  |
| Giga-Tech Wolf | 08471389 |  |  |  |
| Shovel Crusher | 71950093 |  |  |  |
| Mechanicalchaser | 07359741 |  |  |  |
| Blocker | 34743446 |  |  |  |
| Golgoil | 07526150 |  |  |  |
| Cyber-Stein | 69015963 |  |  |  |
| Cyber Commander | 06400512 |  |  |  |
| Jinzo #7 | 32809211 |  |  |  |
| Thunder Dragon | 31786629 |  |  |  |
| Kaiser Dragon | 94566432 |  |  |  |
| Magician of Faith | 31560081 |  |  |  |
| Goddess of Whim | 67959180 |  |  |  |
| Water Magician | 93343894 |  |  |  |
| Ice Water | 20848593 |  |  |  |
| Waterdragon Fairy | 66836598 |  |  |  |
| Ancient Elf | 93221206 |  |  |  |
| Water Girl | 55014050 |  |  |  |
| Deepsea Shark | 28593363 |  |  |  |
| Bottom Dweller | 81386177 |  |  |  |
| 7 Colored Fish | 23771716 |  |  |  |
| Guardian of the Sea | 85448931 |  |  |  |
| Aqua Snake | 12436646 |  |  |  |
| Giant Red Seasnake | 58831685 |  |  |  |
| Kappa Avenger | 48109103 |  |  |  |
| Kanikabuto | 84103702 |  |  |  |
| Zarigun | 10598400 |  |  |  |
| Millennium Golem | 47986555 |  |  |  |
| Destroyer Golem | 73481154 |  |  |  |
| Barrel Rock | 10476868 |  |  |  |
| Minomushi Warrior | 46864967 |  |  |  |
| Stone Ghost | 72269672 |  |  |  |
| Kaminari Attack | 09653271 |  |  |  |
| Tripwire Beast | 45042329 |  |  |  |
| Bolt Penguin | 48531733 |  |  |  |
| The Immortal of Thunder | 84926738 |  |  |  |
| Electric Snake | 11324436 |  |  |  |
| Punished Eagle | 74703140 |  |  |  |
| Skull Red Bird | 10202894 |  |  |  |
| Crimson Sunbird | 46696593 |  |  |  |
| Armed Ninja | 09076207 |  |  |  |
| Magical Ghost | 46474915 |  |  |  |
| Soul Hunter | 72869010 |  |  |  |
| Vermillion Sparrow | 35752363 |  |  |  |
| Sea Kamen | 71746462 |  |  |  |
| Sinister Serpent | 08131171 |  |  |  |
| Ganigumo | 34536276 |  |  |  |
| Alinsection | 70924884 |  |  |  |
| Insect Soldiers of the Sky | 07019529 |  |  |  |
| Cockroach Knight | 33413638 |  |  |  |
| Burglar | 06297941 |  |  |  |
| Pragtical | 33691040 |  |  |  |
| Ameba | 95174353 |  |  |  |
| Korogashi | 32569498 |  |  |  |
| Boo Koo | 68963107 |  |  |  |
| Flower Wolf | 95952802 |  |  |  |
| Rainbow Flower | 21347810 |  |  |  |
| Barrel Lily | 67841515 |  |  |  |
| Hoshiningen | 67629977 |  |  |  |
| Maha Vailo | 93013676 |  |  |  |
| Musician King | 56907389 |  |  |  |
| Wilmee | 92391084 |  |  |  |
| Dragon Seeker | 28563545 |  |  |  |
| Man-Eater Bug | 54652250 |  |  |  |
| D. Human | 81057959 |  |  |  |
| Turtle Raccoon | 17441953 |  |  |  |
| Prisman | 80234301 |  |  |  |
| Crazy Fish | 53713014 |  |  |  |
| Bracchio-raidus | 16507828 |  |  |  |
| Laughing Flower | 42591472 |  |  |  |
| Bean Soldier | 84990171 |  |  |  |
| Cannon Soldier | 11384280 |  |  |  |
| Guardian of the Throne Room | 47879985 |  |  |  |
| Brave Scizzar | 74277583 |  |  |  |
| The Statue of Easter Island | 10262698 |  |  |  |
| Muka Muka | 46657337 |  |  |  |
| Boulder Tortoise | 09540040 |  |  |  |
| Fire Kraken | 46534755 |  |  |  |
| Turtle Bird | 72929454 |  |  |  |
| Skullbird | 08327462 |  |  |  |
| Monstrous Bird | 35712107 |  |  |  |
| The Bistro Butcher | 71107816 |  |  |  |
| Star Boy | 08201910 |  |  |  |
| Milus Radiant | 07489323 |  |  |  |
| Flame Cerebrus | 60862676 |  |  |  |
| Eldeen | 06367785 |  |  |  |
| Mystical Sand | 32751480 |  |  |  |
| Gemini Elf | 69140098 |  |  |  |
| Minar | 32539892 |  |  |  |
| Kamakiriman | 68928540 |  |  |  |
| Mechaleon | 94412545 |  |  |  |
| Mega Thunderball | 21817254 |  |  |  |
| Niwatori | 07805359 |  |  |  |
| Corroding Shark | 34290067 |  |  |  |
| Skelengel | 60694662 |  |  |  |
| Hane-Hane | 07089711 |  |  |  |
| Tongyo | 69572024 |  |  |  |
| Dharma Cannon | 96967123 |  |  |  |
| Skelgon | 32355828 |  |  |  |
| Wow Warrior | 69750536 |  |  |  |
| Griggle | 95744531 |  |  |  |
| Frog the Jam | 68638985 |  |  |  |
| Behegon | 94022093 |  |  |  |
| Dark Elf | 21417692 |  |  |  |
| Winged Dragon, Guardian of the Fortress #2 | 57405307 |  |  |  |
| The Wandering Doomed | 93788854 |  |  |  |
| Steel Ogre Grotto #1 | 29172562 |  |  |  |
| Oscillo Hero | 82065276 |  |  |  |
| Invader from Another Dimension | 28450915 |  |  |  |
| Lesser Dragon | 55444629 |  |  |  |
| Needle Worm | 81843628 |  |  |  |
| Wretched Ghost of the Attic | 17238333 |  |  |  |
| Great Mammoth of Goldfine | 54622031 |  |  |  |
| Man-eating Black Shark | 80727036 |  |  |  |
| Yormungarde | 17115745 |  |  |  |
| Darkworld Thorns | 43500484 |  |  |  |
| Anthrosaurus | 89904598 |  |  |  |
| Drooling Lizard | 16353197 |  |  |  |
| Trakadon | 42348802 |  |  |  |
| B. Dragon Jungle King | 89832901 |  |  |  |
| Little D | 42625254 |  |  |  |
| Witch of the Black Forest | 78010363 |  |  |  |
| Giant Scorpion of the Tundra | 41403766 |  |  |  |
| Abyss Flower | 40387124 |  |  |  |
| Takuhee | 03170832 |  |  |  |
| Binding Chain | 08058240 |  |  |  |
| Mechanical Snail | 34442949 |  |  |  |
| Greenkappa | 61831093 |  |  |  |
| Mon Larvas | 07225792 |  |  |  |
| Living Vase | 34320307 |  |  |  |
| Tentacle Plant | 60715406 |  |  |  |
| Beaked Snake | 06103114 |  |  |  |
| Morphing Jar | 33508719 |  |  |  |
| Muse-A | 69992868 |  |  |  |
| Rose Spectre of Dunn | 32485271 |  |  |  |
| Fiend Reflection #1 | 68870276 |  |  |  |
| Ghoul with an Appetite | 95265975 |  |  |  |
| Pale Beast | 21263083 |  |  |  |
| Little Chimera | 68658728 |  |  |  |
| Violent Rain | 94042337 |  |  |  |
| Key Mace #2 | 20541432 |  |  |  |
| Tenderness | 57935140 |  |  |  |
| Penguin Soldier | 93920745 |  |  |  |
| Fairy Dragon | 20315854 |  |  |  |
| Obese Marmot of Nefariousness | 56713552 |  |  |  |
| Liquid Beast | 93108297 |  |  |  |
| Twin Long Rods #2 | 29692206 |  |  |  |
| Great Bill | 55691901 |  |  |  |
| Shining Friendship | 82085619 |  |  |  |
| Bladefly | 28470714 |  |  |  |
| Hiro's Shadow Scout | 81863068 |  |  |  |
| Lady of Faith | 17358176 |  |  |  |
| Twin-Headed Thunder Dragon | 54752875 |  |  |  |
| Armored Starfish | 17535588 |  |  |  |
| Marine Beast | 29929832 |  |  |  |
| Warrior of Tradition | 56413937 |  |  |  |
| Snakeyashi | 29802344 |  |  |  |
| The Thing That Hides in the Mud | 18180762 |  |  |  |
| High Tide Gyojin | 54579801 |  |  |  |
| Fairy of the Fountain | 81563416 |  |  |  |
| Amazon of the Seas | 17968114 |  |  |  |
| Nekogal #2 | 43352213 |  |  |  |
| Witch's Apprentice | 80741828 |  |  |  |
| Armored Rat | 16246527 |  |  |  |
| Ancient Lizard Warrior | 43230671 |  |  |  |
| Maiden of the Moonlight | 79629370 |  |  |  |
| Night Lizard | 78402798 |  |  |  |
| Blue-Winged Crown | 41396436 |  |  |  |
| Amphibious Bugroth | 40173854 |  |  |  |
| Acid Crawler | 77568553 |  |  |  |
| Invader of the Throne | 03056267 |  |  |  |
| Mystical Sheep #1 | 30451366 |  |  |  |
| Disk Magician | 76446915 |  |  |  |
| Flame Viper | 02830619 |  |  |  |
| Royal Guard | 39239728 |  |  |  |
| Gruesome Goo | 65623423 |  |  |  |
| Whiptail Crow | 91996584 |  |  |  |
| Kunai with Chain | 37390589 |  |  |  |
| Magical Labyrinth | 64389297 |  |  |  |
| Salamandra | 32268901 |  |  |  |
| Eternal Rest | 95051344 |  |  |  |
| Megamorph | 22046459 |  |  |  |
| Metalmorph | 68540058 |  |  |  |
| Crush Card | 57728570 |  |  |  |
| Bright Castle | 82878489 |  |  |  |
| Shadow Spell | 29267084 |  |  |  |
| Black Luster Ritual | 55761792 |  |  |  |
| Zera Ritual | 81756897 |  |  |  |
| Harpie's Feather Duster | 18144506 |  |  |  |
| War-Lion Ritual | 54539105 |  |  |  |
| Beastly Mirror Ritual | 81933259 |  |  |  |
| Commencement Dance | 43417563 |  |  |  |
| Hamburger Recipe | 80811661 |  |  |  |
| Novox's Prayer | 43694075 |  |  |  |
| House of Adhesive Tape | 15083728 |  |  |  |
| Acid Trap Hole | 41356845 |  |  |  |
| Widespread Ruin | 77754944 |  |  |  |
| Bad Reaction to Simochi | 40633297 |  |  |  |
| Reverse Trap | 77622396 |  |  |  |
| Turtle Oath | 76806714 |  |  |  |
| Resurrection of Chakra | 39399168 |  |  |  |
| Javelin Beetle Pact | 41182875 |  |  |  |
| Garma Sword Oath | 78577570 |  |  |  |
| Revival of Dokurorider | 31066283 |  |  |  |
| Fortress Whale's Oath | 77454922 |  |  |  |
| Performance of Sword | 04849037 |  |  |  |
| Hungry Burger | 30243636 |  |  |  |
| Sengenjin | 76232340 |  |  |  |
| Skull Guardian | 03627449 |  |  |  |
| Tri-Horned Dragon | 39111158 |  |  |  |
| Serpent Night Dragon | 66516792 |  |  |  |
| Cosmo Queen | 38999506 |  |  |  |
| Chakra | 65393205 |  |  |  |
| Crab Turtle | 91782219 |  |  |  |
| Mikazukinoyaiba | 38277918 |  |  |  |
| Meteor Dragon | 64271667 |  |  |  |
| Meteor B. Dragon | 90660762 |  |  |  |
| Firewing Pegasus | 27054370 |  |  |  |
| Garma Sword | 90844184 |  |  |  |
| Javelin Beetle | 26932788 |  |  |  |
| Fortress Whale | 62337487 |  |  |  |
| Dokurorider | 99721536 |  |  |  |
| Dark Magic Ritual | 76792184 |  |  |  |
| Magician of Black Chaos | 30208479 |  |  |  |
| Slot Machine | 03797883 |  |  |  |
| Red Archery Girl | 65570596 |  |  |  |
| Ryu-Ran | 02964201 |  |  |  |
| Manga Ryu-Ran | 38369349 |  |  |  |
| Toon Mermaid | 65458948 |  |  |  |
| Toon Summoned Skull | 91842653 |  |  |  |
| Relinquished | 64631466 |  |  |  |
| Thousand-Eyes Idol | 27125110 |  |  |  |
| Thousand-Eyes Restrict | 63519819 |  |  |  |
| Steel Ogre Grotto #2 | 90908427 |  |  |  |
| Blast Sphere | 26302522 |  |  |  |
| Hyozanryu | 62397231 |  |  |  |
| Alpha The Magnet Warrior | 99785935 |  |  |  |
| Lord of D. | 17985575 |  |  |  |
| Red-Eyes Black Metal Dragon | 64335804 |  |  |  |
| Barrel Dragon | 81480460 |  |  |  |
| Hannibal Necromancer | 05640330 |  |  |  |
| Panther Warrior | 42035044 |  |  |  |
| Three-Headed Geedo | 78423643 |  |  |  |
| Gazelle the King of Mythical Beasts | 05818798 |  |  |  |
| Stone Statue of the Aztecs | 31812496 |  |  |  |
| Berfomet | 77207191 |  |  |  |
| Chimera the Flying Mythical Beast | 04796100 |  |  |  |
| Gear Golem the Moving Fortress | 30190809 |  |  |  |
| Jinzo | 77585513 |  |  |  |
| Swordsman of Landstar | 03573512 |  |  |  |
| Cyber Raider | 39978267 |  |  |  |
| The Fiend Megacyber | 66362965 |  |  |  |
| Reflect Bounder | 02851070 |  |  |  |
| Beta The Magnet Warrior | 39256679 |  |  |  |
| Big Shield Gardna | 65240384 |  |  |  |
| Dark Magician Girl | 38033121 |  |  |  |
| Alligator's Sword | 64428736 |  |  |  |
| Insect Queen | 91512835 |  |  |  |
| Parasite Paracide | 27911549 |  |  |  |
| Skull-Mark Ladybug | 64306248 |  |  |  |
| Little-Winguard | 90790253 |  |  |  |
| Pinch Hopper | 26185991 |  |  |  |
| Blue-Eyes Toon Dragon | 53183600 |  |  |  |
| Sword Hunter | 51345461 |  |  |  |
| Drill Bug | 88733579 |  |  |  |
| Deepsea Warrior | 24128274 |  |  |  |
| Satellite Cannon | 50400231 |  |  |  |
| The Last Warrior from Another Planet | 86099788 |  |  |  |
| Dunames Dark Witch | 12493482 |  |  |  |
| Garnecia Elefantis | 49888191 |  |  |  |
| Total Defense Shogun | 75372290 |  |  |  |
| Beast of Talwar | 11761845 |  |  |  |
| Cyber-Tech Alligator | 48766543 |  |  |  |
| Gamma The Magnet Warrior | 11549357 |  |  |  |
| Time Machine | 80987696 |  |  |  |
| Copycat | 26376390 |  |  |  |
| Toon World | 15259703 |  |  |  |
| Gorgon's Eye | 52648457 |  |  |  |
| Black Illusion Ritual | 41426869 |  |  |  |
| Brain Control | 87910978 |  |  |  |
| Negate Attack | 14315573 |  |  |  |
| Multiply | 40703222 |  |  |  |
| Lightforce Sword | 49587034 |  |  |  |
| The Flute of Summoning Dragon | 43973174 |  |  |  |
| Shield & Sword | 52097679 |  |  |  |
| Graceful Charity | 79571449 |  |  |  |
| Chain Destruction | 01248895 |  |  |  |
| Mesmeric Control | 48642904 |  |  |  |
| Graceful Dice | 74137509 |  |  |  |
| Skull Dice | 00126218 |  |  |  |
| Mind Control | 37520316 |  |  |  |
| Scapegoat | 73915051 |  |  |  |
| Amplifier | 00303660 |  |  |  |
| Card Destruction | 72892473 |  |  |  |
| Tragedy | 35686187 |  |  |  |
| Ectoplasmer | 97342942 |  |  |  |
| Dark Magic Curtain | 99789342 |  |  |  |
| Insect Barrier | 23615409 |  |  |  |
| Magic-Arm Shield | 96008713 |  |  |  |
| Fissure | 66788016 |  |  |  |
| Trap Hole | 04206964 |  |  |  |
| Polymerization | 24094653 |  |  |  |
| Remove Trap | 51482758 |  |  |  |
| Two-Pronged Attack | 83887306 |  |  |  |
| Monster Reborn | 83764718 |  |  |  |
| De-Spell | 19159413 |  |  |  |
| Pot of Greed | 55144522 |  |  |  |
| Gravedigger Ghoul | 82542267 |  |  |  |
| Reinforcements | 17814387 |  |  |  |
| Castle Walls | 44209392 |  |  |  |
| Ultimate Offering | 80604091 |  |  |  |
| Tribute to The Doomed | 79759861 |  |  |  |
| Soul Release | 05758500 |  |  |  |
| The Cheerful Coffin | 41142615 |  |  |  |
| Change of Heart | 04031928 |  |  |  |
| Solemn Judgment | 41420027 |  |  |  |
| Magic Jammer | 77414722 |  |  |  |
| Seven Tools of the Bandit | 03819470 |  |  |  |
| Horn of Heaven | 98069388 |  |  |  |
| Just Desserts | 24068492 |  |  |  |
| Royal Decree | 51452091 |  |  |  |
| Polymerization | 24094653 |  |  |  |
| Magical Thorn | 53119267 |  |  |  |
| Restructer Revolution | 99518961 |  |  |  |
| Fusion Sage | 26902560 |  |  |  |
| Sword of Deep-Seated | 98495314 |  |  |  |
| Block Attack | 25880422 |  |  |  |
| The Unhappy Maiden | 51275027 |  |  |  |
| Robbin' Goblin | 88279736 |  |  |  |
| Germ Infection | 24668830 |  |  |  |
| Wall of Illusion | 13945283 |  |  |  |
| Neo the Magic Swordsman | 50930991 |  |  |  |
| Baron of the Fiend Sword | 86325596 |  |  |  |
| Man-Eating Treasure Chest | 13723605 |  |  |  |
| Sorcerer of the Doomed | 49218300 |  |  |  |
| Last Will | 85602018 |  |  |  |
| Waboku | 12607053 |  |  |  |
| Mirror Force | 44095762 |  |  |  |
| Ring of Magnetism | 20436034 |  |  |  |
| Share the Pain | 56830749 |  |  |  |
| Stim-Pack | 83225447 |  |  |  |
| Heavy Storm | 19613556 |  |  |  |
| Gravekeeper's Servant | 16762927 |  |  |  |
| Upstart Goblin | 70368879 |  |  |  |
| Toll | 82003859 |  |  |  |
| Final Destiny | 18591904 |  |  |  |
| Snatch Steal | 45986603 |  |  |  |
| Chorus of Sanctuary | 81380218 |  |  |  |
| Confiscation | 17375316 |  |  |  |
| Delinquent Duo | 44763025 |  |  |  |
| Fairy's Hand Mirror | 17653779 |  |  |  |
| Tailor of the Fickle | 43641473 |  |  |  |
| Rush Recklessly | 70046172 |  |  |  |
| The Reliable Guardian | 16430187 |  |  |  |
| The Forceful Sentry | 42829885 |  |  |  |
| Chain Energy | 79323590 |  |  |  |
| Mystical Space Typhoon | 05318639 |  |  |  |
| Giant Trunade | 42703248 |  |  |  |
| Painful Choice | 74191942 |  |  |  |
| Snake Fang | 00596051 |  |  |  |
| Cyber Jar | 34124316 |  |  |  |
| Banisher of the Light | 61528025 |  |  |  |
| Giant Rat | 97017120 |  |  |  |
| Senju of the Thousand Hands | 23401839 |  |  |  |
| UFO Turtle | 60806437 |  |  |  |
| Flash Assailant | 96890582 |  |  |  |
| Karate Man | 23289281 |  |  |  |
| Giant Germ | 95178994 |  |  |  |
| Nimble Momonga | 22567609 |  |  |  |
| Spear Cretin | 58551308 |  |  |  |
| Shining Angel | 95956346 |  |  |  |
| Mother Grizzly | 57839750 |  |  |  |
| Flying Kamakiri #1 | 84834865 |  |  |  |
| Ceremonial Bell | 20228463 |  |  |  |
| Sonic Bird | 57617178 |  |  |  |
| Mystic Tomato | 83011277 |  |  |  |
| Kotodama | 19406822 |  |  |  |
| Gaia Power | 56594520 |  |  |  |
| Umiiruka | 82999629 |  |  |  |
| Molten Destruction | 19384334 |  |  |  |
| Rising Air Current | 45778932 |  |  |  |
| Luminous Spark | 81777047 |  |  |  |
| Mystic Plasma Zone | 18161786 |  |  |  |
| Messenger of Peace | 44656491 |  |  |  |
| Michizure | 37580756 |  |  |  |
| Gust | 73079365 |  |  |  |
| Driving Snow | 00473469 |  |  |  |
| Numinous Healer | 02130625 |  |  |  |
| Appropriate | 48539234 |  |  |  |
| Forced Requisition | 74923978 |  |  |  |
| Minor Goblin Official | 01918087 |  |  |  |
| Gamble | 37313786 |  |  |  |
| DNA Surgery | 74701381 |  |  |  |
| The Regulation of Tribe | 00296499 |  |  |  |
| Backup Soldier | 36280194 |  |  |  |
| Attack and Receive | 63689843 |  |  |  |
| Ceasefire | 36468556 |  |  |  |
| Light of Intervention | 62867251 |  |  |  |
| Respect Play | 08951260 |  |  |  |
| Imperial Order | 61740673 |  |  |  |
| Skull Invitation | 98139712 |  |  |  |
| Magical Hats | 81210420 |  |  |  |
| Nobleman of Crossout | 71044499 |  |  |  |
| Nobleman of Extermination | 17449108 |  |  |  |
| The Shallow Grave | 43434803 |  |  |  |
| Premature Burial | 70828912 |  |  |  |
| Morphing Jar #2 | 79106360 |  |  |  |
| Bubonic Vermin | 06104968 |  |  |  |
| Twin-Headed Fire Dragon | 78984772 |  |  |  |
| Darkfire Soldier #1 | 05388481 |  |  |  |
| Mr. Volcano | 31477025 |  |  |  |
| Darkfire Soldier #2 | 78861134 |  |  |  |
| Kiseitai | 04266839 |  |  |  |
| Cyber Falcon | 30655537 |  |  |  |
| Dark Bat | 67049542 |  |  |  |
| Flying Kamakiri #2 | 03134241 |  |  |  |
| Harpie's Brother | 30532390 |  |  |  |
| Oni Tank T-34 | 66927994 |  |  |  |
| Overdrive | 02311603 |  |  |  |
| Buster Blader | 78193831 |  |  |  |
| Time Seal | 35316708 |  |  |  |
| Graverobber | 61705417 |  |  |  |
| Gift of The Mystical Elf | 98299011 |  |  |  |
| The Eye of Truth | 34694160 |  |  |  |
| Dust Tornado | 60082869 |  |  |  |
| Call of the Haunted | 97077563 |  |  |  |
| Solomon's Lawbook | 23471572 |  |  |  |
| Enchanted Javelin | 96355986 |  |  |  |
| Mirror Wall | 22359980 |  |  |  |
| Windstorm of Etaqua | 59744639 |  |  |  |
| Valkyrion the Magna Warrior | 75347539 |  |  |  |
| Alligator's Sword Dragon | 03366982 |  |  |  |
| Vorse Raider | 14898066 |  |  |  |
| Ring of Destruction | 83555666 |  |  |  |
| Aqua Chorus | 95132338 |  |  |  |
| Sebek's Blessing | 22537443 |  |  |  |
| Anti-Spell Fragrance | 58921041 |  |  |  |
| Riryoku | 34016756 |  |  |  |
| Sword of Dragon's Soul | 61405855 |  |  |  |
| Luminous Soldier | 57482479 |  |  |  |
| King Tiger Wanghu | 83986578 |  |  |  |
| Command Knight | 10375182 |  |  |  |
| Wolf Axwielder | 56369281 |  |  |  |
| The Illusory Gentleman | 83764996 |  |  |  |
| Patrician of Darkness | 19153634 |  |  |  |
| Birdface | 45547649 |  |  |  |
| Kryuel | 82642348 |  |  |  |
| Airknight Parshath | 18036057 |  |  |  |
| Fairy King Truesdale | 45425051 |  |  |  |
| Serpentine Princess | 71829750 |  |  |  |
| Maiden of the Aqua | 17214465 |  |  |  |
| Robotic Knight | 44203504 |  |  |  |
| Thunder Nyan Nyan | 70797118 |  |  |  |
| Molten Behemoth | 17192817 |  |  |  |
| Twin-Headed Behemoth | 43586926 |  |  |  |
| Injection Fairy Lily | 79575620 |  |  |  |
| Woodland Sprite | 06979239 |  |  |  |
| Arsenal Bug | 42364374 |  |  |  |
| Kinetic Soldier | 79853073 |  |  |  |
| Jowls of Dark Demise | 05257687 |  |  |  |
| Souleater | 31242786 |  |  |  |
| Slate Warrior | 78636495 |  |  |  |
| Timeater | 44913552 |  |  |  |
| Mucus Yolk | 70307656 |  |  |  |
| Servant of Catabolism | 02792265 |  |  |  |
| Rigras Leever | 39180960 |  |  |  |
| Moisture Creature | 75285069 |  |  |  |
| Boneheimer | 98456117 |  |  |  |
| Flame Dancer | 12883044 |  |  |  |
| Sonic Jammer | 84550200 |  |  |  |
| Gearfried the Iron Knight | 00423705 |  |  |  |
| Humanoid Slime | 46821314 |  |  |  |
| Worm Drake | 73216412 |  |  |  |
| Humanoid Worm Drake | 05600127 |  |  |  |
| Revival Jam | 31709826 |  |  |  |
| Flying Fish | 31987274 |  |  |  |
| Amphibian Beast | 67371383 |  |  |  |
| Rocket Warrior | 30860696 |  |  |  |
| The Legendary Fisherman | 03643300 |  |  |  |
| Robolady | 92421852 |  |  |  |
| Roboyarou | 38916461 |  |  |  |
| Lightning Conger | 27671321 |  |  |  |
| Spherous Lady | 52121290 |  |  |  |
| Shining Abyss | 87303357 |  |  |  |
| Archfiend of Gilfer | 50287060 |  |  |  |
| Gadget Soldier | 86281779 |  |  |  |
| Grand Tiki Elder | 13676474 |  |  |  |
| The Masked Beast | 49064413 |  |  |  |
| Melchid the Four-Face Beast | 86569121 |  |  |  |
| Nuvia the Wicked | 12953226 |  |  |  |
| Soul Exchange | 68005187 |  |  |  |
| Mask of Weakness | 57882509 |  |  |  |
| Curse of the Masked Beast | 94377247 |  |  |  |
| Mask of Dispel | 20765952 |  |  |  |
| Mask of Restrict | 29549364 |  |  |  |
| Mask of the Accursed | 56948373 |  |  |  |
| Mask of Brutality | 82432018 |  |  |  |
| Return of the Doomed | 19827717 |  |  |  |
| Lightning Blade | 55226821 |  |  |  |
| Tornado Wall | 18605135 |  |  |  |
| Infinite Dismissal | 54109233 |  |  |  |
| Fairy Box | 21598948 |  |  |  |
| Torrential Tribute | 53582587 |  |  |  |
| Multiplication of Ants | 22493811 |  |  |  |
| De-Fusion | 95286165 |  |  |  |
| Jam Breeding Machine | 21770260 |  |  |  |
| Nightmare's Steelcage | 58775978 |  |  |  |
| Infinite Cards | 94163677 |  |  |  |
| Jam Defender | 21558682 |  |  |  |
| Card of Safe Return | 57953380 |  |  |  |
| Magic Cylinder | 62279055 |  |  |  |
| Solemn Wishes | 35346968 |  |  |  |
| Burning Land | 24294108 |  |  |  |
| Cold Wave | 60682203 |  |  |  |
| Fairy Meteor Crush | 97687912 |  |  |  |
| Limiter Removal | 23171610 |  |  |  |
| Shift | 59560625 |  |  |  |
| Insect Imitation | 96965364 |  |  |  |
| Dimensionhole | 22959079 |  |  |  |
| Magic Drain | 59344077 |  |  |  |
| Gravity Bind | 85742772 |  |  |  |
| Shadow of Eyes | 58621589 |  |  |  |
| Girochin Kuwagata | 84620194 |  |  |  |
| Hayabusa Knight | 21015833 |  |  |  |
| Bombardment Beetle | 57409948 |  |  |  |
| 4-Starred Ladybug of Doom | 83994646 |  |  |  |
| Gradius | 10992251 |  |  |  |
| Red-Moon Baby | 56387350 |  |  |  |
| Mad Sword Beast | 79870141 |  |  |  |
| Skull Mariner | 05265750 |  |  |  |
| The All-Seeing White Tiger | 32269855 |  |  |  |
| Goblin Attack Force | 78658564 |  |  |  |
| Island Turtle | 04042268 |  |  |  |
| Wingweaver | 31447217 |  |  |  |
| Science Soldier | 67532912 |  |  |  |
| Souls of the Forgotten | 04920010 |  |  |  |
| Dokuroyaiba | 30325729 |  |  |  |
| Rain of Mercy | 66719324 |  |  |  |
| Monster Recovery | 93108433 |  |  |  |
| Type Zero Magic Crusher | 21237481 |  |  |  |
| Yellow Luster Shield | 04542651 |  |  |  |
| Creature Swap | 31036355 |  |  |  |
| Dark Magician | 46986414 |  |  |  |
| Thousand Knives | 63391643 |  |  |  |
| Mystic Box | 25774450 |  |  |  |
| Ground Collapse | 90502999 |  |  |  |
| Amazon Archer | 91869203 |  |  |  |
| Fire Princess | 64752646 |  |  |  |
| Spirit of the Breeze | 53530069 |  |  |  |
| Dancing Fairy | 90925163 |  |  |  |
| Empress Mantis | 58818411 |  |  |  |
| Cure Mermaid | 85802526 |  |  |  |
| Hysteric Fairy | 21297224 |  |  |  |
| Bio-Mage | 58696829 |  |  |  |
| The Forgiving Maiden | 84080938 |  |  |  |
| St. Joan | 21175632 |  |  |  |
| Marie the Fallen One | 57579381 |  |  |  |
| Jar of Greed | 83968380 |  |  |  |
| Scroll of Bewitchment | 10352095 |  |  |  |
| United We Stand | 56747793 |  |  |  |
| Mage Power | 83746708 |  |  |  |
| Offerings to the Doomed | 19230407 |  |  |  |
| Meteor of Destruction | 33767325 |  |  |  |
| Lightning Vortex | 69162969 |  |  |  |
| Exchange | 05556668 |  |  |  |
| The Portrait's Secret | 32541773 |  |  |  |
| The Gross Ghost of Fled Dreams | 68049471 |  |  |  |
| Headless Knight | 05434080 |  |  |  |
| Dark Necrofear | 31829185 |  |  |  |
| Dark Magician's Tome of Black Magic | 67227834 |  |  |  |
| Destiny Board | 94212438 |  |  |  |
| The Dark Door | 30606547 |  |  |  |
| Earthbound Spirit | 67105242 |  |  |  |
| Dark Spirit of the Silent | 93599951 |  |  |  |
| The Earl of Demise | 66989694 |  |  |  |
| Dark Sage | 92377303 |  |  |  |
| Cathedral of Nobles | 29762407 |  |  |  |
| Judgment of Anubis | 55256016 |  |  |  |
| Embodiment of Apophis | 28649820 |  |  |  |
| Foolish Burial | 81439173 |  |  |  |
| Makiu | 27827272 |  |  |  |
| Ancient Lamp | 54912977 |  |  |  |
| Cyber Harpie Lady | 80316585 |  |  |  |
| Mystical Beast Serket | 89194033 |  |  |  |
| Swift Gaia the Fierce Knight | 16589042 |  |  |  |
| Obnoxious Celtic Guard | 52077741 |  |  |  |
| Zombyra the Dark | 88472456 |  |  |  |
| Spiritualism | 15866454 |  |  |  |
| Jowgen the Spiritualist | 41855169 |  |  |  |
| Kycoo the Ghost Destroyer | 88240808 |  |  |  |
| Summoner of Illusions | 14644902 |  |  |  |
| Bazoo the Soul-Eater | 40133511 |  |  |  |
| Soul of Purity and Light | 77527210 |  |  |  |
| Spirit of Flames | 13522325 |  |  |  |
| Aqua Spirit | 40916023 |  |  |  |
| The Rock Spirit | 76305638 |  |  |  |
| Garuda the Wind Spirit | 12800777 |  |  |  |
| Gilasaurus | 45894482 |  |  |  |
| Tornado Bird | 71283180 |  |  |  |
| Dreamsprite | 08687195 |  |  |  |
| Supply | 44072894 |  |  |  |
| Maryokutai | 71466592 |  |  |  |
| Collected Power | 07565547 |  |  |  |
| Royal Command | 33950246 |  |  |  |
| Riryoku Field | 70344351 |  |  |  |
| Skull Lair | 06733059 |  |  |  |
| Graverobber's Retribution | 33737664 |  |  |  |
| Deal of Phantom | 69122763 |  |  |  |
| Destruction Punch | 05616412 |  |  |  |
| Blind Destruction | 32015116 |  |  |  |
| The Emperor's Holiday | 68400115 |  |  |  |
| Cyclon Laser | 05494820 |  |  |  |
| Spirit Message "I" | 31893528 |  |  |  |
| Spirit Message "N" | 67287533 |  |  |  |
| Spirit Message "A" | 94772232 |  |  |  |
| Spirit Message "L" | 30170981 |  |  |  |
| Bait Doll | 07165085 |  |  |  |
| Fusion Gate | 33550694 |  |  |  |
| Ekibyo Drakmord | 69954399 |  |  |  |
| Miracle Dig | 06343408 |  |  |  |
| Vengeful Bog Spirit | 95220856 |  |  |  |
| Amazoness Swords Woman | 94004268 |  |  |  |
| Makyura the Destructor | 21593977 |  |  |  |
| Amazoness Archers | 67987611 |  |  |  |
| Rope of Life | 93382620 |  |  |  |
| Enchanted Arrow | 93260132 |  |  |  |
| Amazoness Chain Master | 29654737 |  |  |  |
| Viser Des | 56043446 |  |  |  |
| Amazoness Fighter | 55821894 |  |  |  |
| Nightmare Wheel | 54704216 |  |  |  |
| Byser Shock | 17597059 |  |  |  |
| Dark Ruler Ha Des | 53982768 |  |  |  |
| Dark Balter the Terrible | 80071763 |  |  |  |
| Lesser Fiend | 16475472 |  |  |  |
| Possessed Dark Soul | 52860176 |  |  |  |
| Winged Minion | 89258225 |  |  |  |
| Ryu-Kishin Clown | 42647539 |  |  |  |
| Twin-Headed Wolf | 88132637 |  |  |  |
| Opticlops | 14531242 |  |  |  |
| Bark of Dark Ruler | 41925941 |  |  |  |
| Fatal Abacus | 77910045 |  |  |  |
| Life Absorbing Machine | 14318794 |  |  |  |
| Double Snare | 03682106 |  |  |  |
| Freed the Matchless General | 49681811 |  |  |  |
| Throwstone Unit | 76075810 |  |  |  |
| Marauding Captain | 02460565 |  |  |  |
| Ryu Senshi | 49868263 |  |  |  |
| Warrior Dai Grepher | 75953262 |  |  |  |
| Frontier Wiseman | 38742075 |  |  |  |
| Exiled Force | 74131780 |  |  |  |
| The Hunter with 7 Weapons | 01525329 |  |  |  |
| Shadow Tamer | 37620434 |  |  |  |
| Dragon Manipulator | 63018132 |  |  |  |
| The A. Forces | 00403847 |  |  |  |
| Reinforcement of the Army | 32807846 |  |  |  |
| Array of Revealing Light | 69296555 |  |  |  |
| The Warrior Returning Alive | 95281259 |  |  |  |
| Ready for Intercepting | 31785398 |  |  |  |
| A Feint Plan | 68170903 |  |  |  |
| Tyrant Dragon | 94568601 |  |  |  |
| Spear Dragon | 31553716 |  |  |  |
| Spirit Ryu | 67957315 |  |  |  |
| The Dragon dwelling in the Cave | 93346024 |  |  |  |
| Lizard Soldier | 20831168 |  |  |  |
| Fiend Skull Dragon | 66235877 |  |  |  |
| Cave Dragon | 93220472 |  |  |  |
| Gray Wing | 29618570 |  |  |  |
| Troop Dragon | 55013285 |  |  |  |
| The Dragon's Bead | 92408984 |  |  |  |
| A Wingbeat of Giant Dragon | 28596933 |  |  |  |
| Dragon's Gunfire | 55991637 |  |  |  |
| Stamping Destruction | 81385346 |  |  |  |
| Super Rejuvenation | 27770341 |  |  |  |
| Dragon's Rage | 54178050 |  |  |  |
| Burst Breath | 80163754 |  |  |  |
| Luster Dragon #2 | 17658803 |  |  |  |
| Emergency Provisions | 53046408 |  |  |  |
| Keldo | 80441106 |  |  |  |
| Dragged Down into the Grave | 16435215 |  |  |  |
| Kaiser Glider | 52824910 |  |  |  |
| Spell Reproduction | 29228529 |  |  |  |
| Collapse | 55713623 |  |  |  |
| Mudora | 82108372 |  |  |  |
| Cestus of Dagla | 28106077 |  |  |  |
| De-Spell Germ Weapon | 54591086 |  |  |  |
| Des Feral Imp | 81985784 |  |  |  |
| Reversal of Graves | 17484499 |  |  |  |
| Kelbek | 54878498 |  |  |  |
| Zolga | 16268841 |  |  |  |
| Blast Held by a Tribute | 89041555 |  |  |  |
| Agido | 16135253 |  |  |  |
| Silent Fiend | 42534368 |  |  |  |
| Fiber Jar | 78706415 |  |  |  |
| Gradius' Option | 14291024 |  |  |  |
| Maharaghi | 40695128 |  |  |  |
| Inaba White Rabbit | 77084837 |  |  |  |
| Yata-Garasu | 03078576 |  |  |  |
| Susa Soldier | 40473581 |  |  |  |
| Yamata Dragon | 76862289 |  |  |  |
| Great Long Nose | 02356994 |  |  |  |
| Otohime | 39751093 |  |  |  |
| Hino-Kagu-Tsuchi | 75745607 |  |  |  |
| Asura Priest | 02134346 |  |  |  |
| Fushi No Tori | 38538445 |  |  |  |
| Super Robolady | 75923050 |  |  |  |
| Super Roboyarou | 01412158 |  |  |  |
| Fengsheng Mirror | 37406863 |  |  |  |
| Heart of Clear Water | 64801562 |  |  |  |
| A Legendary Ocean | 00295517 |  |  |  |
| Fusion Sword Murasame Blade | 37684215 |  |  |  |
| Smoke Grenade of the Thief | 63789924 |  |  |  |
| Spiritual Energy Settle Machine | 99173029 |  |  |  |
| Second Coin Toss | 36562627 |  |  |  |
| Convulsion of Nature | 62966332 |  |  |  |
| The Secret of the Bandit | 99351431 |  |  |  |
| After the Struggle | 25345186 |  |  |  |
| Blast with Chain | 98239899 |  |  |  |
| Disappear | 24623598 |  |  |  |
| Bottomless Trap Hole | 29401950 |  |  |  |
| Ominous Fortunetelling | 56995655 |  |  |  |
| Nutrient Z | 29389368 |  |  |  |
| Drop Off | 55773067 |  |  |  |
| Fiend Comedian | 81172176 |  |  |  |
| Last Turn | 28566710 |  |  |  |
| Des Volstgalph | 81059524 |  |  |  |
| Kaiser Sea Horse | 17444133 |  |  |  |
| Vampire Lord | 53839837 |  |  |  |
| Gora Turtle | 80233946 |  |  |  |
| Sasuke Samurai | 16222645 |  |  |  |
| Poison Mummy | 43716289 |  |  |  |
| Dark Dust Spirit | 89111398 |  |  |  |
| Royal Keeper | 16509093 |  |  |  |
| Wandering Mummy | 42994702 |  |  |  |
| Great Dezard | 88989706 |  |  |  |
| Swarm of Scarabs | 15383415 |  |  |  |
| Swarm of Locusts | 41872150 |  |  |  |
| Giant Axe Mummy | 78266168 |  |  |  |
| Guardian Sphinx | 40659562 |  |  |  |
| Pyramid Turtle | 77044671 |  |  |  |
| Dice Jar | 03549275 |  |  |  |
| Dark Scorpion Burglars | 40933924 |  |  |  |
| Don Zaloog | 76922029 |  |  |  |
| Des Lacooda | 02326738 |  |  |  |
| Fushioh Richie | 39711336 |  |  |  |
| Cobraman Sakuzy | 75109441 |  |  |  |
| Book of Life | 02204140 |  |  |  |
| Book of Taiyou | 38699854 |  |  |  |
| Book of Moon | 14087893 |  |  |  |
| Mirage of Nightmare | 41482598 |  |  |  |
| Call of the Mummy | 04861205 |  |  |  |
| Timidity | 40350910 |  |  |  |
| Pyramid Energy | 76754619 |  |  |  |
| Tutan Mask | 03149764 |  |  |  |
| Ordeal of a Traveler | 39537362 |  |  |  |
| Bottomless Shifting Sand | 76532077 |  |  |  |
| Curse of Royal | 02926176 |  |  |  |
| Needle Ceiling | 38411870 |  |  |  |
| Statue of the Wicked | 65810489 |  |  |  |
| Dark Coffin | 01804528 |  |  |  |
| Needle Wall | 38299233 |  |  |  |
| Trap Dustshoot | 64697231 |  |  |  |
| Reckless Greed | 37576645 |  |  |  |
| Toon Dark Magician Girl | 90960358 |  |  |  |
| Gilford the Lightning | 36354007 |  |  |  |
| Exarion Universe | 63749102 |  |  |  |
| Legendary Fiend | 99747800 |  |  |  |
| Toon Defense | 43509019 |  |  |  |
| Toon Table of Contents | 89997728 |  |  |  |
| Toon Masked Sorcerer | 16392422 |  |  |  |
| Toon Gemini Elf | 42386471 |  |  |  |
| Toon Cannon Soldier | 79875176 |  |  |  |
| Toon Goblin Attack Force | 15270885 |  |  |  |
| Card of Sanctity | 42664989 |  |  |  |
| Puppet Master | 41442341 |  |  |  |
| Newdoria | 04335645 |  |  |  |
| Lord Poison | 40320754 |  |  |  |
| Blade Knight | 39507162 |  |  |  |
| Helpoemer | 76052811 |  |  |  |
| Hidden Soldier | 02047519 |  |  |  |
| Gil Garth | 38445524 |  |  |  |
| Calamity of the Wicked | 01224927 |  |  |  |
| Lava Golem | 00102380 |  |  |  |
| Monster Relief | 37507488 |  |  |  |
| Machine Duplication | 63995093 |  |  |  |
| Dark Jeroid | 90980792 |  |  |  |
| Master of Dragon Soldier | 62873545 |  |  |  |
| F.G.D. | 99267150 |  |  |  |
| Queen's Knight | 25652259 |  |  |  |
| X-Head Cannon | 62651957 |  |  |  |
| Enemy Controller | 98045062 |  |  |  |
| Master Kyonshee | 24530661 |  |  |  |
| Kabazauls | 51934376 |  |  |  |
| Inpachi | 97923414 |  |  |  |
| Gravekeeper's Spy | 24317029 |  |  |  |
| Gravekeeper's Curse | 50712728 |  |  |  |
| Gravekeeper's Guard | 37101832 |  |  |  |
| Gravekeeper's Spear Soldier | 63695531 |  |  |  |
| Gravekeeper's Cannonholder | 99877698 |  |  |  |
| Gravekeeper's Assailant | 25262697 |  |  |  |
| A Man with Wdjat | 51351302 |  |  |  |
| Mystical Knight of Jackal | 98745000 |  |  |  |
| A Cat of Ill Omen | 24140059 |  |  |  |
| Yomi Ship | 51534754 |  |  |  |
| Winged Sage Falcos | 87523462 |  |  |  |
| An Owl of Luck | 23927567 |  |  |  |
| Charm of Shabti | 50412166 |  |  |  |
| Cobra Jar | 86801871 |  |  |  |
| Spirit Reaper | 23205979 |  |  |  |
| Nightmare Horse | 59290628 |  |  |  |
| Reaper on the Nightmare | 85684223 |  |  |  |
| Card Shuffle | 12183332 |  |  |  |
| Reasoning | 58577036 |  |  |  |
| Dark Room of Nightmare | 85562745 |  |  |  |
| Different Dimension Capsule | 11961740 |  |  |  |
| Necrovalley | 47355498 |  |  |  |
| Buster Rancher | 84740193 |  |  |  |
| Hieroglyph Lithograph | 10248192 |  |  |  |
| Dark Snake Syndrome | 47233801 |  |  |  |
| Terraforming | 73628505 |  |  |  |
| Banner of Courage | 10012614 |  |  |  |
| Metamorphosis | 46411259 |  |  |  |
| Royal Tribute | 72405967 |  |  |  |
| Reversal Quiz | 05990062 |  |  |  |
| Curse of Aging | 41398771 |  |  |  |
| Raigeki Break | 04178474 |  |  |  |
| Disturbance Strategy | 77561728 |  |  |  |
| Rite of Spirit | 30450531 |  |  |  |
| Non Aggression Area | 76848240 |  |  |  |
| D. Tribe | 02833249 |  |  |  |
| Y-Dragon Head | 65622692 |  |  |  |
| XY-Dragon Cannon | 02111707 |  |  |  |
| Z-Metal Tank | 64500000 |  |  |  |
| XYZ-Dragon Cannon | 91998119 |  |  |  |
| Rope of Spirit | 37383714 |  |  |  |
| King's Knight | 64788463 |  |  |  |
| Jack's Knight | 90876561 |  |  |  |
| Interdimensional Matter Transporter | 36261276 |  |  |  |
| Goblin Zombie | 63665875 |  |  |  |
| Drillago | 99050989 |  |  |  |
| Lekunga | 62543393 |  |  |  |
| Cost Down | 23265313 |  |  |  |
| People Running About | 12143771 |  |  |  |
| Oppressed People | 58538870 |  |  |  |
| United Resistance | 85936485 |  |  |  |
| Dark Blade | 11321183 |  |  |  |
| Pitch-Dark Dragon | 47415292 |  |  |  |
| Kiryu | 84814897 |  |  |  |
| Decayed Commander | 10209545 |  |  |  |
| Zombie Tiger | 47693640 |  |  |  |
| Giant Orc | 73698349 |  |  |  |
| Second Goblin | 19086954 |  |  |  |
| Vampire Orchis | 46571052 |  |  |  |
| Des Dendle | 12965761 |  |  |  |
| Burning Beast | 59364406 |  |  |  |
| Freezing Beast | 85359414 |  |  |  |
| D.D. Crazy Beast | 48148828 |  |  |  |
| Spell Canceller | 84636823 |  |  |  |
| Helping Robo For Combat | 47025270 |  |  |  |
| Dimension Jar | 73414375 |  |  |  |
| Roulette Barrel | 46303688 |  |  |  |
| Paladin of White Dragon | 73398797 |  |  |  |
| White Dragon Ritual | 09786492 |  |  |  |
| Frontline Base | 46181000 |  |  |  |
| Demotion | 72575145 |  |  |  |
| Combination Attack | 08964854 |  |  |  |
| Autonomous Action Unit | 71453557 |  |  |  |
| Poison of the Old Man | 08842266 |  |  |  |
| Dark Core | 70231910 |  |  |  |
| Raregold Armor | 07625614 |  |  |  |
| Kishido Spirit | 60519422 |  |  |  |
| Tribute Doll | 02903036 |  |  |  |
| Wave-Motion Cannon | 38992735 |  |  |  |
| Huge Revolution | 65396880 |  |  |  |
| Thunder of Ruler | 91781589 |  |  |  |
| Spell Shield Type-8 | 38275183 |  |  |  |
| Meteorain | 64274292 |  |  |  |
| Pineapple Blast | 90669991 |  |  |  |
| Secret Barrel | 27053506 |  |  |  |
| Formation Union | 26931058 |  |  |  |
| Adhesion Trap Hole | 62325062 |  |  |  |
| XZ-Tank Cannon | 99724761 |  |  |  |
| YZ-Tank Dragon | 25119460 |  |  |  |
| Final Attack Orders | 52503575 |  |  |  |
| Dark Paladin | 98502113 |  |  |  |
| Spell Absorption | 51481927 |  |  |  |
| Diffusion Wave-Motion | 87880531 |  |  |  |
| Fiend's Sanctuary | 24874630 |  |  |  |
| Great Angus | 11813953 |  |  |  |
| Aitsu | 48202661 |  |  |  |
| Sonic Duck | 84696266 |  |  |  |
| Luster Dragon | 11091375 |  |  |  |
| Amazoness Paladin | 47480070 |  |  |  |
| Amazoness Blowpiper | 73574678 |  |  |  |
| Amazoness Tiger | 10979723 |  |  |  |
| Skilled White Magician | 46363422 |  |  |  |
| Skilled Dark Magician | 73752131 |  |  |  |
| Apprentice Magician | 09156135 |  |  |  |
| Old Vindictive Magician | 45141844 |  |  |  |
| Chaos Command Magician | 72630549 |  |  |  |
| Magical Marionette | 08034697 |  |  |  |
| Breaker the Magical Warrior | 71413901 |  |  |  |
| Magical Plant Mandragola | 07802006 |  |  |  |
| Magical Scientist | 34206604 |  |  |  |
| Royal Magical Library | 70791313 |  |  |  |
| Armor Exe | 07180418 |  |  |  |
| Tribe-Infecting Virus | 33184167 |  |  |  |
| Des Koala | 69579761 |  |  |  |
| Cliff the Trap Remover | 06967870 |  |  |  |
| Magical Merchant | 32362575 |  |  |  |
| Koitsu | 69456283 |  |  |  |
| Cat's Ear Tribe | 95841282 |  |  |  |
| Ultimate Obedient Fiend | 32240937 |  |  |  |
| Pitch-Black Power Stone | 34029630 |  |  |  |
| Big Bang Shot | 61127349 |  |  |  |
| Gather Your Mind | 07512044 |  |  |  |
| Mass Driver | 34906152 |  |  |  |
| Senri Eye | 60391791 |  |  |  |
| Emblem of Dragon Destroyer | 06390406 |  |  |  |
| Jar Robber | 33784505 |  |  |  |
| Mega Ton Magical Cannon | 32062913 |  |  |  |
| Continuous Destruction Punch | 68057622 |  |  |  |
| Exhausting Spell | 95451366 |  |  |  |
| Hidden Book of Spell | 21840375 |  |  |  |
| Miracle Restoring | 68334074 |  |  |  |
| Disarmament | 20727787 |  |  |  |
| Anti-Spell | 53112492 |  |  |  |
| The Spell Absorbing Life | 99517131 |  |  |  |
| Metal Reflect Slime | 26905245 |  |  |  |
| Bowganian | 52090844 |  |  |  |
| Excavation of Mage Stones | 98494543 |  |  |  |
| Granadora | 13944422 |  |  |  |
| Shinato, King of a Higher Plane | 86327225 |  |  |  |
| Dark Flare Knight | 13722870 |  |  |  |
| Mirage Knight | 49217579 |  |  |  |
| Berserk Dragon | 85605684 |  |  |  |
| Exodia Necross | 12600382 |  |  |  |
| Battle Footballer | 48094997 |  |  |  |
| Arsenal Summoner | 85489096 |  |  |  |
| Nin-Ken Dog | 11987744 |  |  |  |
| Acrobat Monkey | 47372349 |  |  |  |
| Guardian Elma | 74367458 |  |  |  |
| Guardian Ceal | 10755153 |  |  |  |
| Guardian Grarl | 47150851 |  |  |  |
| Guardian Baou | 73544866 |  |  |  |
| Guardian Kay'est | 09633505 |  |  |  |
| Guardian Tryce | 46037213 |  |  |  |
| Gyaku-Gire Panda | 09817927 |  |  |  |
| Blindly Loyal Goblin | 35215622 |  |  |  |
| Despair from the Dark | 71200730 |  |  |  |
| Maju Garzett | 08794435 |  |  |  |
| Fear from the Dark | 34193084 |  |  |  |
| Dark Scorpion - Chick the Yellow | 61587183 |  |  |  |
| D.D. Warrior Lady | 07572887 |  |  |  |
| Thousand Needles | 33977496 |  |  |  |
| Shinato's Ark | 60365591 |  |  |  |
| A Deal with Dark Ruler | 06850209 |  |  |  |
| Contract with Exodia | 33244944 |  |  |  |
| Butterfly Dagger - Elma | 69243953 |  |  |  |
| Shooting Star Bow - Ceal | 95638658 |  |  |  |
| Gravity Axe - Grarl | 32022366 |  |  |  |
| Wicked-Breaking Flamberge - Baou | 68427465 |  |  |  |
| Rod of Silence - Kay'est | 95515060 |  |  |  |
| Twin Swords of Flashing Light - Tryce | 21900719 |  |  |  |
| Precious Cards from Beyond | 68304813 |  |  |  |
| Rod of the Mind's Eye | 94793422 |  |  |  |
| Fairy of the Spring | 20188127 |  |  |  |
| Token Thanksgiving | 57182235 |  |  |  |
| Non-Spellcasting Area | 20065549 |  |  |  |
| Staunch Defender | 92854392 |  |  |  |
| Ojama Trio | 29843091 |  |  |  |
| Arsenal Robber | 55348096 |  |  |  |
| Skill Drain | 82732705 |  |  |  |
| Really Eternal Rest | 28121403 |  |  |  |
| Soul Taker | 81510157 |  |  |  |
| Magical Dimension | 28553439 |  |  |  |
| Judgement of Pharaoh | 55948544 |  |  |  |
| Friendship | 81332143 |  |  |  |
| Unity | 14731897 |  |  |  |
| Dark Magician Knight | 50725996 |  |  |  |
| Knight's Title | 87210505 |  |  |  |
| Sage's Stone | 13604200 |  |  |  |
| Gagagigo | 49003308 |  |  |  |
| D. D. Trainer | 86498013 |  |  |  |
| Ojama Green | 12482652 |  |  |  |
| Archfiend Soldier | 49881766 |  |  |  |
| Pandemonium Watchbear | 75375465 |  |  |  |
| Sasuke Samurai #2 | 11760174 |  |  |  |
| Dark Scorpion - Gorg the Strong | 48768179 |  |  |  |
| Dark Scorpion - Meanae the Thorn | 74153887 |  |  |  |
| Outstanding Dog Marron | 11548522 |  |  |  |
| Great Maju Garzett | 47942531 |  |  |  |
| Iron Blacksmith Kotetsu | 73431236 |  |  |  |
| Mefist the Infernal General | 46820049 |  |  |  |
| Vilepawn Archfiend | 73219648 |  |  |  |
| Shadowknight Archfiend | 09603356 |  |  |  |
| Darkbishop Archfiend | 35798491 |  |  |  |
| Desrook Archfiend | 72192100 |  |  |  |
| Infernalqueen Archfiend | 08581705 |  |  |  |
| Terrorking Archfiend | 35975813 |  |  |  |
| Skull Archfiend of Lightning | 61370518 |  |  |  |
| Metallizing Parasite - Lunatite | 07369217 |  |  |  |
| Tsukuyomi | 34853266 |  |  |  |
| Legendary Flame Lord | 60258960 |  |  |  |
| Dark Master - Zorc | 97642679 |  |  |  |
| Incandescent Ordeal | 33031674 |  |  |  |
| Contract with the Abyss | 69035382 |  |  |  |
| Contract with the Dark Master | 96420087 |  |  |  |
| Falling Down | 32919136 |  |  |  |
| Checkmate | 69313735 |  |  |  |
| Final Countdown | 95308449 |  |  |  |
| Mustering of the Dark Scorpions | 68191243 |  |  |  |
| Pandemonium | 94585852 |  |  |  |
| Altar for Tribute | 21070956 |  |  |  |
| Frozen Soul | 57069605 |  |  |  |
| Battle-Scarred | 94463200 |  |  |  |
| Dark Scorpion Combination | 20858318 |  |  |  |
| Archfiend's Roar | 56246017 |  |  |  |
| Dice Re-Roll | 83241722 |  |  |  |
| Spell Vanishing | 29735721 |  |  |  |
| Sakuretsu Armor | 56120475 |  |  |  |
| Ray of Hope | 82529174 |  |  |  |
| Nightmare Penguin | 81306586 |  |  |  |
| Perfect Machine King | 18891691 |  |  |  |
| Chiron the Mage | 16956455 |  |  |  |
| Ojama Yellow | 42941100 |  |  |  |
| Ojama Black | 79335209 |  |  |  |
| Soul Tiger | 15734813 |  |  |  |
| Big Koala | 42129512 |  |  |  |
| Des Kangaroo | 78613627 |  |  |  |
| Crimson Ninja | 14618326 |  |  |  |
| Strike Ninja | 41006930 |  |  |  |
| Gale Lizard | 77491079 |  |  |  |
| Chopman the Desperate Outlaw | 40884383 |  |  |  |
| Sasuke Samurai #3 | 77379481 |  |  |  |
| D. D. Scout Plane | 03773196 |  |  |  |
| Berserk Gorilla | 39168895 |  |  |  |
| Freed the Brave Wanderer | 16556849 |  |  |  |
| Witch Doctor of Chaos | 75946257 |  |  |  |
| Chaos Necromancer | 01434352 |  |  |  |
| Chaosrider Gustaph | 47829960 |  |  |  |
| Inferno | 74823665 |  |  |  |
| Fenrir | 00218704 |  |  |  |
| Gigantes | 47606319 |  |  |  |
| Silpheed | 73001017 |  |  |  |
| Chaos Sorcerer | 09596126 |  |  |  |
| Gren Maju Da Eiza | 36584821 |  |  |  |
| Black Luster Soldier - Envoy of the Beginning | 72989439 |  |  |  |
| Fuhma Shuriken | 09373534 |  |  |  |
| Heart of the Underdog | 35762283 |  |  |  |
| Wild Nature's Release | 61166988 |  |  |  |
| Ojama Delta Hurricane!! | 08251996 |  |  |  |
| Stumbling | 34646691 |  |  |  |
| Chaos End | 61044390 |  |  |  |
| Chaos Greed | 97439308 |  |  |  |
| D. D. Borderline | 60912752 |  |  |  |
| Recycle | 96316857 |  |  |  |
| Primal Seed | 23701465 |  |  |  |
| Thunder Crash | 69196160 |  |  |  |
| Dimension Distortion | 95194279 |  |  |  |
| Reload | 22589918 |  |  |  |
| Soul Absorption | 68073522 |  |  |  |
| Big Burn | 95472621 |  |  |  |
| Blasting the Ruins | 21466326 |  |  |  |
| Cursed Seal of the Forbidden Spell | 58851034 |  |  |  |
| Tower of Babel | 94256039 |  |  |  |
| Spatial Collapse | 20644748 |  |  |  |
| Chain Disappearance | 57139487 |  |  |  |
| Zero Gravity | 83133491 |  |  |  |
| Dark Mirror Force | 20522190 |  |  |  |
| Energy Drain | 56916805 |  |  |  |
| Chaos Emperor Dragon - Envoy of the End | 82301904 |  |  |  |
| Victory D. | 44910027 |  |  |  |
| Magician's Valkyrie | 80304126 |  |  |  |
| Giga Gagagigo | 43793530 |  |  |  |
| Mad Dog of Darkness | 79182538 |  |  |  |
| Neo Bug | 16587243 |  |  |  |
| Sea Serpent Warrior of Darkness | 42071342 |  |  |  |
| Terrorking Salmon | 78060096 |  |  |  |
| Blazing Inpachi | 05464695 |  |  |  |
| Burning Algae | 41859700 |  |  |  |
| The Thing in the Crater | 78243409 |  |  |  |
| Molten Zombie | 04732017 |  |  |  |
| Dark Magician of Chaos | 40737112 |  |  |  |
| Manticore of Darkness | 77121851 |  |  |  |
| Stealth Bird | 03510565 |  |  |  |
| Sacred Crane | 30914564 |  |  |  |
| Enraged Battle Ox | 76909279 |  |  |  |
| Don Turtle | 03493978 |  |  |  |
| Dark Driceratops | 65287621 |  |  |  |
| Hyper Hammerhead | 02671330 |  |  |  |
| Black Tyranno | 38670435 |  |  |  |
| Anti-Aircraft Flower | 65064143 |  |  |  |
| Prickle Fairy | 91559748 |  |  |  |
| Insect Princess | 37957847 |  |  |  |
| Amphibious Bugroth MK-3 | 64342551 |  |  |  |
| Torpedo Fish | 90337190 |  |  |  |
| Levia-Dragon - Daedalus | 37721209 |  |  |  |
| Orca Mega-Fortress of Darkness | 63120904 |  |  |  |
| Cannonball Spear Shellfish | 95614612 |  |  |  |
| Mataza the Zapper | 22609617 |  |  |  |
| Guardian Angel Joan | 68007326 |  |  |  |
| Manju of the Ten Thousand Hands | 95492061 |  |  |  |
| Getsu Fuhma | 21887179 |  |  |  |
| Ryu Kokki | 57281778 |  |  |  |
| Gryphon's Feather Duster | 34370473 |  |  |  |
| Stray Lambs | 60764581 |  |  |  |
| Smashing Ground | 97169186 |  |  |  |
| Dimension Fusion | 23557835 |  |  |  |
| Dedication through Light and Darkness | 69542930 |  |  |  |
| Salvage | 96947648 |  |  |  |
| Ultra Evolution Pill | 22431243 |  |  |  |
| Earth Chant | 59820352 |  |  |  |
| Jade Insect Whistle | 95214051 |  |  |  |
| Destruction Ring | 21219755 |  |  |  |
| Fiend's Hand Mirror | 58607704 |  |  |  |
| Compulsory Evacuation Device | 94192409 |  |  |  |
| A Hero Emerges | 21597117 |  |  |  |
| Self-Destruct Button | 57585212 |  |  |  |
| Curse of Darkness | 84970821 |  |  |  |
| Begone, Knave! | 20374520 |  |  |  |
| DNA Transplant | 56769674 |  |  |  |
| Robbin' Zombie | 83258273 |  |  |  |
| Trap Jammer | 19252988 |  |  |  |
| Invader of Darkness | 56647086 |  |  |  |
| Twinheaded Beast | 82035781 |  |  |  |
| Abyss Soldier | 18318842 |  |  |  |
| Inferno Hammer | 17185260 |  |  |  |
| Emes the Infinity | 43580269 |  |  |  |
| D. D. Assailant | 70074904 |  |  |  |
| Teva | 16469012 |  |  |  |
| Skull Zoma | 79852326 |  |  |  |
| Maximum Six | 30707994 |  |  |  |
| Dangerous Machine TYPE-6 | 76895648 |  |  |  |
| Sixth Sense | 03280747 |  |  |  |
| Gogiga Gagagigo | 39674352 |  |  |  |
| Warrior of Zera | 66073051 |  |  |  |
| Sealmaster Meisei | 02468169 |  |  |  |
| Mystical Shine Ball | 39552864 |  |  |  |
| Metal Armored Bug | 65957473 |  |  |  |
| The Agent of Judgment - Saturn | 91345518 |  |  |  |
| The Agent of Wisdom - Mercury | 38730226 |  |  |  |
| The Agent of Creation - Venus | 64734921 |  |  |  |
| The Agent of Force - Mars | 91123920 |  |  |  |
| The Unhappy Girl | 27618634 |  |  |  |
| Soul-Absorbing Bone Tower | 63012333 |  |  |  |
| The Kick Man | 90407382 |  |  |  |
| Vampire Lady | 26495087 |  |  |  |
| Rocket Jumper | 53890795 |  |  |  |
| Avatar of The Pot | 99284890 |  |  |  |
| Legendary Jujitsu Master | 25773409 |  |  |  |
| KA-2 Des Scissors | 52768103 |  |  |  |
| Needle Burrower | 98162242 |  |  |  |
| Blowback Dragon | 25551951 |  |  |  |
| Zaborg the Thunder Monarch | 51945556 |  |  |  |
| Atomic Firefly | 87340664 |  |  |  |
| Mermaid Knight | 24435369 |  |  |  |
| Piranha Army | 50823978 |  |  |  |
| Two Thousand Needles | 83228073 |  |  |  |
| Disc Fighter | 19612721 |  |  |  |
| Arcane Archer of the Forest | 55001420 |  |  |  |
| Lady Ninja Yae | 82005435 |  |  |  |
| Goblin King | 18590133 |  |  |  |
| Solar Flare Dragon | 45985838 |  |  |  |
| White Magician Pikeru | 81383947 |  |  |  |
| Archlord Zerato | 18378582 |  |  |  |
| Opti-Camouflage Armor | 44762290 |  |  |  |
| Mystik Wok | 80161395 |  |  |  |
| Burst Stream of Destruction | 17655904 |  |  |  |
| Monster Gate | 43040603 |  |  |  |
| The Sanctuary in the Sky | 56433456 |  |  |  |
| Earthquake | 82828051 |  |  |  |
| Goblin Thief | 45311864 |  |  |  |
| Backfire | 82705573 |  |  |  |
| Micro Ray | 18190572 |  |  |  |
| Light of Judgment | 44595286 |  |  |  |
| Wall of Revealing Light | 17078030 |  |  |  |
| Solar Ray | 44472639 |  |  |  |
| Ninjitsu Art of Transformation | 70861343 |  |  |  |
| Beckoning Light | 16255442 |  |  |  |
| Draining Shield | 43250041 |  |  |  |
| Armor Break | 79649195 |  |  |  |
| Mazera DeVille | 06133894 |  |  |  |
| Marshmallon | 31305911 |  |  |  |
| Skull Descovery Knight | 78700060 |  |  |  |
| Shield Crash | 30683373 |  |  |  |
| Return Zombie | 03072077 |  |  |  |
| Corpse of Yata-Garasu | 30461781 |  |  |  |
| Marshmallon glasses | 66865880 |  |  |  |
| Earthbound Spirit's Invitation | 65743242 |  |  |  |
| Mokey Mokey | 27288416 |  |  |  |
| Gigobyte | 53776525 |  |  |  |
| Kozaky | 99171160 |  |  |  |
| Fiend Scorpion | 26566878 |  |  |  |
| Pharaoh's Servant | 52550973 |  |  |  |
| Pharaonic Protector | 89959682 |  |  |  |
| Spirit of the Pharaoh | 25343280 |  |  |  |
| Theban Nightmare | 51838385 |  |  |  |
| Aswan Apparition | 88236094 |  |  |  |
| Protector of the Sanctuary | 24221739 |  |  |  |
| Nubian Guard | 51616747 |  |  |  |
| Desertapir | 13409151 |  |  |  |
| Sand Gambler | 50593156 |  |  |  |
| Ghost Knight of Jackal | 13386503 |  |  |  |
| Absorbing Kid from the Sky | 49771608 |  |  |  |
| Elephant Statue of Blessing | 85166216 |  |  |  |
| Elephant Statue of Disaster | 12160911 |  |  |  |
| Spirit Caller | 48659020 |  |  |  |
| Emissary of the Afterlife | 75043725 |  |  |  |
| Double Coston | 44436472 |  |  |  |
| Regenerating Mummy | 70821187 |  |  |  |
| Night Assailant | 16226786 |  |  |  |
| Man-Thro' Tro' | 43714890 |  |  |  |
| King of the Swamp | 79109599 |  |  |  |
| Emissary of the Oasis | 06103294 |  |  |  |
| Special Hurricane | 42598242 |  |  |  |
| Order to Charge | 78986941 |  |  |  |
| Sword of the Soul-Eater | 05371656 |  |  |  |
| Dust Barrier | 31476755 |  |  |  |
| Soul Reversal | 78864369 |  |  |  |
| Spell Economics | 04259068 |  |  |  |
| 7 | 67048711 |  |  |  |
| Level Limit - Area B | 03136426 |  |  |  |
| Enchanting Fitting Room | 30531525 |  |  |  |
| The Law of the Normal | 66926224 |  |  |  |
| Dark Magic Attack | 02314238 |  |  |  |
| Delta Attacker | 39719977 |  |  |  |
| Thousand Energy | 05703682 |  |  |  |
| Triangle Power | 32298781 |  |  |  |
| The Third Sarcophagus | 78697395 |  |  |  |
| The Second Sarcophagus | 04081094 |  |  |  |
| The First Sarcophagus | 31076103 |  |  |  |
| Human-Wave Tactics | 30353551 |  |  |  |
| Curse of Anubis | 66742250 |  |  |  |
| Desert Sunlight | 93747864 |  |  |  |
| Des Counterblow | 39131963 |  |  |  |
| Labyrinth of Nightmare | 66526672 |  |  |  |
| Soul Resurrection | 92924317 |  |  |  |
| Order to Smash | 39019325 |  |  |  |
| The End of Anubis | 65403020 |  |  |  |
| Crush D. Gandra | 64681432 |  |  |  |
| Return from the Different Dimension | 27174286 |  |  |  |
| Pyramid of Light | 53569894 |  |  |  |
| Blue-Eyes Shining Dragon | 53347303 |  |  |  |
| Familiar Knight | 89731911 |  |  |  |
| Rare Metal Dragon | 25236056 |  |  |  |
| Peten the Dark Clown | 52624755 |  |  |  |
| Sorcerer of Dark Magic | 88619463 |  |  |  |
| Andro Sphinx | 15013468 |  |  |  |
| Sphinx Teleia | 51402177 |  |  |  |
| Theinen the Great Sphinx | 87997872 |  |  |  |
| Inferno Tempest | 14391920 |  |  |  |
| Watapon | 87774234 |  |  |  |
| Charcoal Inpachi | 13179332 |  |  |  |
| Neo Aqua Madoor | 49563947 |  |  |  |
| Skull Dog Marron | 86652646 |  |  |  |
| Goblin Calligrapher | 12057781 |  |  |  |
| Ultimate Insect LV1 | 49441499 |  |  |  |
| Horus the Black Flame Dragon LV4 | 75830094 |  |  |  |
| Horus the Black Flame Dragon LV6 | 11224103 |  |  |  |
| Horus the Black Flame Dragon LV8 | 48229808 |  |  |  |
| Dark Mimic LV1 | 74713516 |  |  |  |
| Dark Mimic LV3 | 01102515 |  |  |  |
| Mystic Swordsman LV2 | 47507260 |  |  |  |
| Mystic Swordsman LV4 | 74591968 |  |  |  |
| Armed Dragon LV3 | 00980973 |  |  |  |
| Armed Dragon LV5 | 46384672 |  |  |  |
| Armed Dragon LV7 | 73879377 |  |  |  |
| Horus' Servant | 09264485 |  |  |  |
| Red-Eyes B. Chick | 36262024 |  |  |  |
| Ninja Grandmaster Sasuke | 04041838 |  |  |  |
| Rafflesia Seduction | 31440542 |  |  |  |
| Ultimate Baseball Kid | 67934141 |  |  |  |
| Mobius the Frost Monarch | 04929256 |  |  |  |
| Element Dragon | 30314994 |  |  |  |
| Element Soldier | 66712593 |  |  |  |
| Howling Insect | 93107608 |  |  |  |
| Masked Dragon | 39191307 |  |  |  |
| Mind on Air | 66690411 |  |  |  |
| Unshaven Angler | 92084010 |  |  |  |
| The Trojan Horse | 38479725 |  |  |  |
| Nobleman-Eater Bug | 65878864 |  |  |  |
| Enraged Muka Muka | 91862578 |  |  |  |
| Hade-Hane | 28357177 |  |  |  |
| Penumbral Soldier Lady | 64751286 |  |  |  |
| Ojama King | 90140980 |  |  |  |
| Master of Oz | 27134689 |  |  |  |
| Sanwitch | 53539634 |  |  |  |
| Dark Factory of Mass Production | 90928333 |  |  |  |
| Hammer Shot | 26412047 |  |  |  |
| Mind Wipe | 52817046 |  |  |  |
| Abyssal Designator | 89801755 |  |  |  |
| Level Up! | 25290459 |  |  |  |
| Inferno Fire Blast | 52684508 |  |  |  |
| The Graveyard in the Fourth Dimension | 88089103 |  |  |  |
| Two-Man Cell Battle | 25578802 |  |  |  |
| Big Wave Small Wave | 51562916 |  |  |  |
| Fusion Weapon | 27967615 |  |  |  |
| Ritual Weapon | 54351224 |  |  |  |
| Taunt | 90740329 |  |  |  |
| Absolute End | 27744077 |  |  |  |
| Spirit Barrier | 53239672 |  |  |  |
| Ninjitsu Art of Decoy | 89628781 |  |  |  |
| Enervating Mist | 26022485 |  |  |  |
| Heavy Slump | 52417194 |  |  |  |
| Greed | 89405199 |  |  |  |
| Cemetary Bomb | 51394546 |  |  |  |
| Hallowed Life Barrier | 88789641 |  |  |  |
| The Tricky | 14778250 |  |  |  |
| Green Gadget | 41172955 |  |  |  |
| Stronghold | 13955608 |  |  |  |
| Red Gadget | 86445415 |  |  |  |
| Yellow Gadget | 13839120 |  |  |  |
| Tricky's Magic 4 | 75622824 |  |  |  |
| The Blockman | 48115277 |  |  |  |
| Silent Swordsman LV3 | 01995985 |  |  |  |
| Silent Swordsman LV5 | 74388798 |  |  |  |
| Silent Swordsman LV7 | 37267041 |  |  |  |
| Silent Magician LV4 | 73665146 |  |  |  |
| Magician's Circle | 00050755 |  |  |  |
| Magician's Unite | 36045450 |  |  |  |
| Silent Magician LV8 | 72443568 |  |  |  |
| Woodborg Inpachi | 35322812 |  |  |  |
| Mighty Guard | 62327910 |  |  |  |
| Bokoichi the Freightening Car | 08715625 |  |  |  |
| Harpie Girl | 34100324 |  |  |  |
| The Creator | 61505339 |  |  |  |
| The Creator Incarnate | 97093037 |  |  |  |
| Ultimate Insect LV3 | 34088136 |  |  |  |
| Mystic Swordsman LV6 | 60482781 |  |  |  |
| Heavy Mech Support Platform | 23265594 |  |  |  |
| Element Magician | 65260293 |  |  |  |
| Element Saurus | 92755808 |  |  |  |
| Roc from the Valley of Haze | 28143906 |  |  |  |
| Sasuke Samurai #4 | 64538655 |  |  |  |
| Harpie Lady 1 | 91932350 |  |  |  |
| Harpie Lady 2 | 27927359 |  |  |  |
| Harpie Lady 3 | 54415063 |  |  |  |
| Raging Flame Sprite | 90810762 |  |  |  |
| Thestalos the Firestorm Monarch | 26205777 |  |  |  |
| Eagle Eye | 53693416 |  |  |  |
| Tactical Espionage Expert | 89698120 |  |  |  |
| Invasion of Flames | 26082229 |  |  |  |
| Creeping Doom Manta | 52571838 |  |  |  |
| Pitch-Black Warwolf | 88975532 |  |  |  |
| Mirage Dragon | 15960641 |  |  |  |
| Gaia Soul the Combustible Collective | 51355346 |  |  |  |
| Fox Fire | 88753985 |  |  |  |
| Big Core | 14148099 |  |  |  |
| Fusilier Dragon, the Dual-Mode Beast | 51632798 |  |  |  |
| Dekoichi the Battlechanted Locomotive | 87621407 |  |  |  |
| A-Team: Trap Disposal Unit | 13026402 |  |  |  |
| Homunculus the Alchemic Being | 40410110 |  |  |  |
| Dark Blade the Dragon Knight | 86805855 |  |  |  |
| Mokey Mokey King | 13803864 |  |  |  |
| Serial Spell | 49398568 |  |  |  |
| Harpies' Hunting Ground | 75782277 |  |  |  |
| Triangle Ecstasy Spark | 12181376 |  |  |  |
| Necklace of Command | 48576971 |  |  |  |
| Flint | 75560629 |  |  |  |
| Mokey Mokey Smackdown | 01965724 |  |  |  |
| Back to Square One | 47453433 |  |  |  |
| Monster Reincarnation | 74848038 |  |  |  |
| Ballista of Rampart Smashing | 00242146 |  |  |  |
| Lighten the Load | 37231841 |  |  |  |
| Malice Dispersion | 13626450 |  |  |  |
| Divine Wrath | 49010598 |  |  |  |
| Xing Zhen Hu | 76515293 |  |  |  |
| Rare Metalmorph | 12503902 |  |  |  |
| Mind Haxorz | 75392615 |  |  |  |
| Fuh-Rin-Ka-Zan | 01781310 |  |  |  |
| Chain Burst | 48276469 |  |  |  |
| Pikeru's Circle of Enchantment | 74270067 |  |  |  |
| Spell Purification | 01669772 |  |  |  |
| Astral Barrier | 37053871 |  |  |  |
| Covering Fire | 74458486 |  |  |  |
| Castle Gate | 36931229 |  |  |  |
| Owner's Seal | 09720537 |  |  |  |
| Space Mambo | 36119641 |  |  |  |
| Divine Dragon Ragnarok | 62113340 |  |  |  |
| Chu-Ske the Mouse Fighter | 08508055 |  |  |  |
| Insect Knight | 35052053 |  |  |  |
| Sacred Phoenix of Nephthys | 61441708 |  |  |  |
| Hand of Nephthys | 98446407 |  |  |  |
| Ultimate Insect LV5 | 34830502 |  |  |  |
| Granmarg the Rock Monarch | 60229110 |  |  |  |
| Element Valkyrie | 97623219 |  |  |  |
| Element Doom | 23118924 |  |  |  |
| Maji-Gire Panda | 60102563 |  |  |  |
| Catnipped Kitty | 96501677 |  |  |  |
| Behemoth the King of All Animals | 22996376 |  |  |  |
| Big-Tusked Mammoth | 59380081 |  |  |  |
| Kangaroo Champ | 95789089 |  |  |  |
| Hyena | 22873798 |  |  |  |
| Blade Rabbit | 58268433 |  |  |  |
| Mecha-Dog Marron | 94667532 |  |  |  |
| Blast Magician | 21051146 |  |  |  |
| Gearfried the Swordmaster | 57046845 |  |  |  |
| Armed Samurai - Ben Kei | 84430950 |  |  |  |
| Shadowslayer | 20939559 |  |  |  |
| Golem Sentry | 52323207 |  |  |  |
| Abare Ushioni | 89718302 |  |  |  |
| The Light - Hex-Sealed Fusion | 15717011 |  |  |  |
| The Dark - Hex-Sealed Fusion | 52101615 |  |  |  |
| The Earth - Hex-Sealed Fusion | 88696724 |  |  |  |
| Whirlwind Prodigy | 15090429 |  |  |  |
| Flame Ruler | 41089128 |  |  |  |
| Firebird | 87473172 |  |  |  |
| Rescue Cat | 14878871 |  |  |  |
| Brain Jacker | 40267580 |  |  |  |
| Gatling Dragon | 87751584 |  |  |  |
| King Dragun | 13756293 |  |  |  |
| A Feather of the Phoenix | 49140998 |  |  |  |
| Poison Fangs | 76539047 |  |  |  |
| Swords of Concealing Light | 12923641 |  |  |  |
| Spiral Spear Strike | 49328340 |  |  |  |
| Release Restraint | 75417459 |  |  |  |
| Centrifugal Field | 01801154 |  |  |  |
| Fulfillment of the Contract | 48206762 |  |  |  |
| Re-Fusion | 74694807 |  |  |  |
| The Big March of Animals | 01689516 |  |  |  |
| Cross Counter | 37083210 |  |  |  |
| Threatening Roar | 36361633 |  |  |  |
| Phoenix Wing Wind Blast | 63356631 |  |  |  |
| Good Goblin Housekeeping | 09744376 |  |  |  |
| Beast Soul Swap | 35149085 |  |  |  |
| Assault on GHQ | 62633180 |  |  |  |
| D.D. Dynamite | 08628798 |  |  |  |
| Deck Devastation Virus | 35027493 |  |  |  |
| Elemental Burst | 61411502 |  |  |  |
| Forced Ceasefire | 97806240 |  |  |  |
| Curse of Vampire | 34294855 |  |  |  |
| Union Attack | 60399954 |  |  |  |
| Blood Sucker | 97783659 |  |  |  |
| Overpowering Eye | 60577362 |  |  |  |
| Red-Eyes Darkness Dragon | 96561011 |  |  |  |
| Vampire Genesis | 22056710 |  |  |  |
| Kaibaman | 34627841 |  |  |  |
| Elemental Hero Avian | 21844576 |  |  |  |
| Elemental Hero Burstinatrix | 58932615 |  |  |  |
| Elemental Hero Clayman | 84327329 |  |  |  |
| Elemental Hero Sparkman | 20721928 |  |  |  |
| Winged Kuriboh | 57116033 |  |  |  |
| Ancient Gear Golem | 83104731 |  |  |  |
| Ancient Gear Beast | 10509340 |  |  |  |
| Ancient Gear Soldier | 56094445 |  |  |  |
| Millennium Scorpion | 82482194 |  |  |  |
| Ultimate Insect LV7 | 19877898 |  |  |  |
| Lost Guardian | 45871897 |  |  |  |
| Hieracosphinx | 82260502 |  |  |  |
| Criosphinx | 18654201 |  |  |  |
| Moai Interceptor Cannons | 45159319 |  |  |  |
| Megarock Dragon | 71544954 |  |  |  |
| Dummy Golem | 13532663 |  |  |  |
| Grave Ohja | 40937767 |  |  |  |
| Mine Golem | 76321376 |  |  |  |
| Monk Fighter | 03810071 |  |  |  |
| Master Monk | 49814180 |  |  |  |
| Guardian Statue | 75209824 |  |  |  |
| Medusa Worm | 02694423 |  |  |  |
| D.D. Survivor | 48092532 |  |  |  |
| Mid Shield Gardna | 75487237 |  |  |  |
| White Ninja | 01571945 |  |  |  |
| Aussa the Earth Charmer | 37970940 |  |  |  |
| Eria the Water Charmer | 74364659 |  |  |  |
| Hiita the Fire Charmer | 00759393 |  |  |  |
| Wynn the Wind Charmer | 37744402 |  |  |  |
| Batteryman AA | 63142001 |  |  |  |
| Des Wombat | 09637706 |  |  |  |
| King of the Skull Servants | 36021814 |  |  |  |
| Reshef the Dark Being | 62420419 |  |  |  |
| Elemental Mistress Doriado | 99414168 |  |  |  |
| Elemental Hero Flame Wingman | 35809262 |  |  |  |
| Elemental Hero Thunder Giant | 61204971 |  |  |  |
| Gift of the Martyr | 98792570 |  |  |  |
| Double Attack | 34187685 |  |  |  |
| Battery Charger | 61181383 |  |  |  |
| Kaminote Blow | 97570038 |  |  |  |
| Doriado's Blessing | 23965037 |  |  |  |
| Final Ritual of the Ancients | 60369732 |  |  |  |
| Legendary Black Belt | 96458440 |  |  |  |
| Nitro Unit | 23842445 |  |  |  |
| Shifting Shadows | 59237154 |  |  |  |
| Impenetrable Formation | 96631852 |  |  |  |
| Hero Signal | 22020907 |  |  |  |
| Pikeru's Second Sight | 58015506 |  |  |  |
| Minefield Eruption | 85519211 |  |  |  |
| Kozaky's Self-Destruct Button | 21908319 |  |  |  |
| Mispolymerization | 58392024 |  |  |  |
| Level Conversion Lab | 84397023 |  |  |  |
| Rock Bombardment | 20781762 |  |  |  |
| Token Feastevil | 83675475 |  |  |  |
| Spell-Stopping Statute | 10069180 |  |  |  |
| Royal Surrender | 56058888 |  |  |  |
| Infernal Flame Emperor | 19847532 |  |  |  |
| Holy Knight Ishzark | 57902462 |  |  |  |
| Ocean Dragon Lord - Neo-Daedalus | 10485110 |  |  |  |
| Cycroid | 45945685 |  |  |  |
| Patroid | 71930383 |  |  |  |
| Gyroid | 18325492 |  |  |  |
| Steamroid | 44729197 |  |  |  |
| Drillroid | 71218746 |  |  |  |
| UFOroid | 07602840 |  |  |  |
| Jetroid | 43697559 |  |  |  |
| Cyber Dragon | 70095154 |  |  |  |
| Wroughtweiler | 06480253 |  |  |  |
| Elemental Hero Bubbleman | 79979666 |  |  |  |
| Steam Gyroid | 05368615 |  |  |  |
| UFOroid Fighter | 32752319 |  |  |  |
| Cyber Twin Dragon | 74157028 |  |  |  |
| Cyber End Dragon | 01546123 |  |  |  |
| Power Bond | 37630732 |  |  |  |
| Skyscraper | 63035430 |  |  |  |
| Summon Priest | 00423585 |  |  |  |
| Dark Dreadroute | 62180201 |  |  |  |
| Winged Kuriboh LV10 | 98585345 |  |  |  |
| Transcendent Wings | 25573054 |  |  |  |
| Bubble Shuffle | 61968753 |  |  |  |
| Spark Blaster | 97362768 |  |  |  |
| Dark Ruler Vandalgyon | 24857466 |  |  |  |
| Soitsu | 60246171 |  |  |  |
| Mad Lobster | 97240270 |  |  |  |
| Jerry Beans Man | 23635815 |  |  |  |
| Cybernetic Magician | 59023523 |  |  |  |
| Cybernetic Cyclopean | 96428622 |  |  |  |
| Mechanical Hound | 22512237 |  |  |  |
| Cyber Archfiend | 59907935 |  |  |  |
| Goblin Elite Attack Force | 85306040 |  |  |  |
| B.E.S. Crystal Core | 22790789 |  |  |  |
| Giant Kozaky | 58185394 |  |  |  |
| Indomitable Fighter Lei Lei | 84173492 |  |  |  |
| Protective Soul Ailin | 11678191 |  |  |  |
| Doitsu | 57062206 |  |  |  |
| Des Frog | 84451804 |  |  |  |
| T.A.D.P.O.L.E. | 10456559 |  |  |  |
| Poison Draw Frog | 56840658 |  |  |  |
| Tyranno Infinity | 83235263 |  |  |  |
| Batteryman C | 19733961 |  |  |  |
| Ebon Magician Curran | 46128076 |  |  |  |
| D.D.M. - Different Dimension Master | 82112775 |  |  |  |
| Fusion Recovery | 18511384 |  |  |  |
| Miracle Fusion | 45906428 |  |  |  |
| Dragon's Mirror | 71490127 |  |  |  |
| System Down | 18895832 |  |  |  |
| Des Croaking | 44883830 |  |  |  |
| Pot of Generosity | 70278545 |  |  |  |
| Shien's Spy | 07672244 |  |  |  |
| Fire Darts | 43061293 |  |  |  |
| Spiritual Earth Art - Kurogane | 70156997 |  |  |  |
| Spiritual Water Art - Aoi | 06540606 |  |  |  |
| Spiritual Fire Art - Kurenai | 42945701 |  |  |  |
| Spiritual Wind Art - Miyabi | 79333300 |  |  |  |
| A Rival Appears! | 05728014 |  |  |  |
| Magical Explosion | 32723153 |  |  |  |
| Rising Energy | 78211862 |  |  |  |
| D.D. Trap Hole | 05606466 |  |  |  |
| Conscription | 31000575 |  |  |  |
| Dimension Wall | 67095270 |  |  |  |
| Prepare to Strike Back | 04483989 |  |  |  |
| Triage | 30888983 |  |  |  |
| Alkana Knight Joker | 06150044 |  |  |  |
| Gilford the Legend | 69933858 |  |  |  |
| Warrior Lady of the Wasteland | 05438492 |  |  |  |
| Divine Sword - Phoenix Blade | 31423101 |  |  |  |
| Elemental Hero Shining Flare Wingman | 25366484 |  |  |  |
| Level Modulation | 61850482 |  |  |  |
| Ojamuscle | 98259197 |  |  |  |
| Ojamagic | 24643836 |  |  |  |
| V-Tiger Jet | 51638941 |  |  |  |
| Blade Skater | 97023549 |  |  |  |
| Reborn Zombie | 23421244 |  |  |  |
| W-Wing Catapult | 96300057 |  |  |  |
| Elemental Hero Bladedge | 59793705 |  |  |  |
| Elemental Hero Wildheart | 86188410 |  |  |  |
| Hydrogeddon | 22587018 |  |  |  |
| Oxygeddon | 58071123 |  |  |  |
| Water Dragon | 85066822 |  |  |  |
| Etoile Cyber | 11460577 |  |  |  |
| VW-Tiger Catapult | 58859575 |  |  |  |
| VWXYZ-Dragon Catapult Cannon | 84243274 |  |  |  |
| Cyber Blader | 10248389 |  |  |  |
| Elemental Hero Rampart Blaster | 47737087 |  |  |  |
| Elemental Hero Tempest | 83121692 |  |  |  |
| Elemental Hero Wildedge | 10526791 |  |  |  |
| Chthonian Alliance | 46910446 |  |  |  |
| Feather Shot | 19394153 |  |  |  |
| Bonding - H2O | 45898858 |  |  |  |
| Chthonian Polymer | 72287557 |  |  |  |
| Chthonian Blast | 18271561 |  |  |  |
| Hero Barrier | 44676200 |  |  |  |
| Feather Wind | 71060915 |  |  |  |
| Zure, Knight of Dark World | 07459013 |  |  |  |
| B.E.S. Tetran | 44954628 |  |  |  |
| Nanobreaker | 70948327 |  |  |  |
| Rapid-Fire Magician | 06337436 |  |  |  |
| Beiige, Vanguard of Dark World | 33731070 |  |  |  |
| Broww, Huntsman of Dark World | 79126789 |  |  |  |
| Brron, Mad King of Dark World | 06214884 |  |  |  |
| Sillva, Warlord of Dark World | 32619583 |  |  |  |
| Goldd, Wu-Lord of Dark World | 78004197 |  |  |  |
| Scarr, Scout of Dark World | 05498296 |  |  |  |
| Familiar-Possessed - Aussa | 31887905 |  |  |  |
| Familiar-Possessed - Eria | 68881649 |  |  |  |
| Familiar-Possessed - Hiita | 04376658 |  |  |  |
| Familiar-Possessed - Wynn | 31764353 |  |  |  |
| Pot of Avarice | 67169062 |  |  |  |
| Dark World Lightning | 93554166 |  |  |  |
| Boss Rush | 66947414 |  |  |  |
| Gateway to Dark World | 93431518 |  |  |  |
| The Forces of Darkness | 29826127 |  |  |  |
| Dark Deal | 65824822 |  |  |  |
| Simultaneous Loss | 92219931 |  |  |  |
| Weed Out | 28604635 |  |  |  |
| The League of Uniform Nomenclature | 55008284 |  |  |  |
| Roll Out! | 91597389 |  |  |  |
| Non-Fusion Area | 27581098 |  |  |  |
| Level Limit - Area A | 54976796 |  |  |  |
| Armed Changer | 90374791 |  |  |  |
| Elemental Hero Necroshade | 89252153 |  |  |  |
| Hero Heyro | 26647858 |  |  |  |
| Elemental Hero Madballman | 52031567 |  |  |  |
| Dark Eradicator Warlock | 29436665 |  |  |  |
| Mythical Beast Cerberus | 55424270 |  |  |  |
| Magical Blast | 91819979 |  |  |  |
| Elemental Hero Steam Healer | 81197327 |  |  |  |
| Burst Return | 27191436 |  |  |  |
| Bubble Blaster | 53586134 |  |  |  |
| Bubble Illusion | 80075749 |  |  |  |
| Clay Charge | 22479888 |  |  |  |
| Armed Dragon LV10 | 59464593 |  |  |  |
| Magical Mallet | 85852291 |  |  |  |
| Inferno Reckless Summon | 12247206 |  |  |  |
| Rancer Dragonute | 11125718 |  |  |  |
| Mistobody | 47529357 |  |  |  |
| Axe Dragonute | 84914462 |  |  |  |
| White Horns D. | 73891874 |  |  |  |
| Uria, Lord of Searing Flames | 06007213 |  |  |  |
| Hamon, Lord of Striking Thunder | 32491822 |  |  |  |
| Raviel, Lord of Phantasms | 69890967 |  |  |  |
| Elemental Hero Neo Bubbleman | 05285665 |  |  |  |
| Hero Kid | 32679370 |  |  |  |
| Cyber Barrier Dragon | 68774379 |  |  |  |
| Cyber Laser Dragon | 04162088 |  |  |  |
| Ancient Gear | 31557782 |  |  |  |
| Hero Heart | 67951831 |  |  |  |
| Magnet Circle LV2 | 94940436 |  |  |  |
| Ancient Gear Drill | 67829249 |  |  |  |
| Phantasmal Martyrs | 93224848 |  |  |  |
| Cyclone Boomerang | 29612557 |  |  |  |
| Photon Generator Unit | 66607691 |  |  |  |
| Ancient Gear Castle | 92001300 |  |  |  |
| Miracle Kids | 55985014 |  |  |  |
| Attack Reflector Unit | 91989718 |  |  |  |
| Damage Condenser | 28378427 |  |  |  |
| Ancient Gear Cannon | 80045583 |  |  |  |
| Proto-Cyber Dragon | 26439287 |  |  |  |
| Adhesive Explosive | 53828396 |  |  |  |
| Machine King Prototype | 89222931 |  |  |  |
| B.E.S. Covered Core | 15317640 |  |  |  |
| D.D. Guide | 52702748 |  |  |  |
| Chain Thrasher | 88190453 |  |  |  |
| Disciple of the Forbidden Spell | 15595052 |  |  |  |
| Tenkabito Shien | 41589166 |  |  |  |
| Parasitic Ticky | 87978805 |  |  |  |
| Gokipon | 14472500 |  |  |  |
| Silent Insect | 40867519 |  |  |  |
| Chainsaw Insect | 77252217 |  |  |  |
| Anteatereatingant | 13250922 |  |  |  |
| Saber Beetle | 49645921 |  |  |  |
| Doom Dozer | 76039636 |  |  |  |
| Treeborn Frog | 12538374 |  |  |  |
| Beelze Frog | 49522489 |  |  |  |
| Princess Pikeru | 75917088 |  |  |  |
| Princess Curran | 02316186 |  |  |  |
| Memory Crusher | 48700891 |  |  |  |
| Malice Ascendant | 14255590 |  |  |  |
| Grass Phantom | 41249545 |  |  |  |
| Sand Moth | 73648243 |  |  |  |
| Divine Dragon - Excelion | 10032958 |  |  |  |
| Ruin, Queen of Oblivion | 46427957 |  |  |  |
| Demise, King of Armageddon | 72426662 |  |  |  |
| D.3.S. Frog | 09910360 |  |  |  |
| Symbol of Heritage | 45305419 |  |  |  |
| Trial of the Princesses | 72709014 |  |  |  |
| End of the World | 08198712 |  |  |  |
| Samsara | 44182827 |  |  |  |
| Karma Cut | 71587526 |  |  |  |
| Next to be Lost | 07076131 |  |  |  |
| Generation Shift | 34460239 |  |  |  |
| Full Salvo | 70865988 |  |  |  |
| Success Probability 0% | 06859683 |  |  |  |
| Option Hunter | 33248692 |  |  |  |
| Goblin Out of the Frying Pan | 69632396 |  |  |  |
| Malfunction | 06137095 |  |  |  |
| The Flute of Summoning Kuriboh | 20065322 |  |  |  |
| Elemental Hero Erikshieler | 29343734 |  |  |  |
| Guardian Exode | 55737443 |  |  |  |
| Great Spirit | 92736188 |  |  |  |
| Fault Zone | 28120197 |  |  |  |
| Homunculus Gold | 27408609 |  |  |  |
| The Ancient Sun Helios | 54493213 |  |  |  |
| Helios Duo Megiste | 80887952 |  |  |  |
| Helios Tris Megiste | 17286057 |  |  |  |
| Elemental Hero Neos | 89943723 |  |  |  |
| Dandylion | 15341821 |  |  |  |

> 共 4072 条卡牌记录