@ =============================================================================
@ 结构卡组数据
@ ROM偏移: 0x1E5FA58 - 0x1E5FD84 (共 0x32C = 812 字节)
@
@ 卡牌编码格式 (每条 4 字节):
@   字节 0-1: (SO_code << 2) | 副本数量  [小端 16 位]
@   字节 2-3: 0x0000 (填充)
@
@ SO_code: 卡牌在游戏内部数据库中的 16 位标识符
@ 副本数量: 1 = 1张, 2 = 2张, 3 = 3张
@
@ 来源文档: doc/um06-deck-modification-tool/data.md
@ =============================================================================

@ -----------------------------------------------------------------------------
@ Dragon's Roar
@ GBA地址: 0x09E5FA58  ROM偏移: 0x1E5FA58
@ 28 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
dragons_roar:
    .hword 0x3FE1, 0x0000    @ Red-Eyes B. Dragon     [密码: 74677422]
    .hword 0x4409, 0x0000    @ Swords of Revealing Light     [密码: 72302403]
    .hword 0x4BB1, 0x0000    @ Pot of Greed     [密码: 55144522]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4C89, 0x0000    @ Snatch Steal     [密码: 45986603]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4D71, 0x0000    @ Ceasefire     [密码: 36468556]
    .hword 0x4D8E, 0x0000    @ Nobleman of Crossout x2  [密码: 71044499]
    .hword 0x4D99, 0x0000    @ Premature Burial     [密码: 70828912]
    .hword 0x4DF5, 0x0000    @ Call of the Haunted     [密码: 97077563]
    .hword 0x4E99, 0x0000    @ Twin-Headed Behemoth     [密码: 43586926]
    .hword 0x50AA, 0x0000    @ Creature Swap x2  [密码: 31036355]
    .hword 0x5379, 0x0000    @ The Dragon's Bead     [密码: 92408984]
    .hword 0x5387, 0x0000    @ Stamping Destruction x3  [密码: 81385346]
    .hword 0x538E, 0x0000    @ Dragon's Rage x2  [密码: 54178050]
    .hword 0x5521, 0x0000    @ Reckless Greed     [密码: 37576645]
    .hword 0x56E2, 0x0000    @ Interdimensional Matter Transporter x2  [密码: 36261276]
    .hword 0x5832, 0x0000    @ Luster Dragon x2  [密码: 11091375]
    .hword 0x5B66, 0x0000    @ Reload x2  [密码: 22589918]
    .hword 0x5C85, 0x0000    @ Trap Jammer     [密码: 19252988]
    .hword 0x5ECD, 0x0000    @ Curse of Anubis     [密码: 66742250]
    .hword 0x5F66, 0x0000    @ Armed Dragon LV3 x2  [密码: 00980973]
    .hword 0x5F6A, 0x0000    @ Armed Dragon LV5 x2  [密码: 46384672]
    .hword 0x5F75, 0x0000    @ Red-Eyes B. Chick     [密码: 36262024]
    .hword 0x5F8D, 0x0000    @ Element Dragon     [密码: 30314994]
    .hword 0x5F9B, 0x0000    @ Masked Dragon x3  [密码: 39191307]
    .hword 0x5FDD, 0x0000    @ The Graveyard in the Fourth Dimensi     [密码: 88089103]
    .hword 0x6251, 0x0000    @ Red-Eyes Darkness Dragon     [密码: 96561011]

@ -----------------------------------------------------------------------------
@ Zombie Madness
@ GBA地址: 0x09E5FAC8  ROM偏移: 0x1E5FAC8
@ 28 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
zombie_madness:
    .hword 0x4BB1, 0x0000    @ Pot of Greed     [密码: 55144522]
    .hword 0x4BF9, 0x0000    @ Magic Jammer     [密码: 77414722]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4C89, 0x0000    @ Snatch Steal     [密码: 45986603]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4CB9, 0x0000    @ Giant Trunade     [密码: 42703248]
    .hword 0x4D8D, 0x0000    @ Nobleman of Crossout     [密码: 71044499]
    .hword 0x4DF1, 0x0000    @ Dust Tornado     [密码: 60082869]
    .hword 0x4FE9, 0x0000    @ Torrential Tribute     [密码: 53582587]
    .hword 0x500D, 0x0000    @ Card of Safe Return     [密码: 57953380]
    .hword 0x50AA, 0x0000    @ Creature Swap x2  [密码: 31036355]
    .hword 0x5489, 0x0000    @ Vampire Lord     [密码: 53839837]
    .hword 0x5499, 0x0000    @ Dark Dust Spirit     [密码: 89111398]
    .hword 0x54BF, 0x0000    @ Pyramid Turtle x3  [密码: 77044671]
    .hword 0x54DA, 0x0000    @ Book of Life x2  [密码: 02204140]
    .hword 0x54EF, 0x0000    @ Call of the Mummy x3  [密码: 04861205]
    .hword 0x5521, 0x0000    @ Reckless Greed     [密码: 37576645]
    .hword 0x5609, 0x0000    @ Master Kyonshee     [密码: 24530661]
    .hword 0x5659, 0x0000    @ Spirit Reaper     [密码: 23205979]
    .hword 0x594E, 0x0000    @ Despair from the Dark x2  [密码: 71200730]
    .hword 0x5B66, 0x0000    @ Reload x2  [密码: 22589918]
    .hword 0x5C3A, 0x0000    @ Ryu Kokki x2  [密码: 57281778]
    .hword 0x5C6B, 0x0000    @ Compulsory Evacuation Device x3  [密码: 94192409]
    .hword 0x5D11, 0x0000    @ Soul-Absorbing Bone Tower     [密码: 63012333]
    .hword 0x5D19, 0x0000    @ Vampire Lady     [密码: 26495087]
    .hword 0x5E61, 0x0000    @ Double Coston     [密码: 44436472]
    .hword 0x5E66, 0x0000    @ Regenerating Mummy x2  [密码: 70821187]
    .hword 0x6255, 0x0000    @ Vampire Genesis     [密码: 22056710]

@ -----------------------------------------------------------------------------
@ Molten Destruction
@ GBA地址: 0x09E5FB38  ROM偏移: 0x1E5FB38
@ 31 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
molten_destruction:
    .hword 0x47F1, 0x0000    @ Little Chimera     [密码: 68658728]
    .hword 0x4BB1, 0x0000    @ Pot of Greed     [密码: 55144522]
    .hword 0x4BE1, 0x0000    @ Tribute to The Doomed     [密码: 79759861]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4C89, 0x0000    @ Snatch Steal     [密码: 45986603]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4CD7, 0x0000    @ UFO Turtle x3  [密码: 60806437]
    .hword 0x4D1A, 0x0000    @ Molten Destruction x2  [密码: 19384334]
    .hword 0x4D8D, 0x0000    @ Nobleman of Crossout     [密码: 71044499]
    .hword 0x4D99, 0x0000    @ Premature Burial     [密码: 70828912]
    .hword 0x4DF2, 0x0000    @ Dust Tornado x2  [密码: 60082869]
    .hword 0x4DF5, 0x0000    @ Call of the Haunted     [密码: 97077563]
    .hword 0x5169, 0x0000    @ Jar of Greed     [密码: 83968380]
    .hword 0x5181, 0x0000    @ Meteor of Destruction     [密码: 33767325]
    .hword 0x566D, 0x0000    @ Dark Room of Nightmare     [密码: 85562745]
    .hword 0x57C5, 0x0000    @ Spell Shield Type-8     [密码: 38275183]
    .hword 0x5825, 0x0000    @ Great Angus     [密码: 11813953]
    .hword 0x5B16, 0x0000    @ Inferno x2  [密码: 74823665]
    .hword 0x5B65, 0x0000    @ Reload     [密码: 22589918]
    .hword 0x5BD1, 0x0000    @ Blazing Inpachi     [密码: 05464695]
    .hword 0x5BDD, 0x0000    @ Molten Zombie     [密码: 04732017]
    .hword 0x5D5A, 0x0000    @ Solar Flare Dragon x2  [密码: 45985838]
    .hword 0x5D8A, 0x0000    @ Backfire x2  [密码: 82705573]
    .hword 0x5E9A, 0x0000    @ Level Limit - Area B x2  [密码: 03136426]
    .hword 0x5F86, 0x0000    @ Ultimate Baseball Kid x2  [密码: 67934141]
    .hword 0x60B5, 0x0000    @ Raging Flame Sprite     [密码: 90810762]
    .hword 0x60B9, 0x0000    @ Thestalos the Firestorm Monarch     [密码: 26205777]
    .hword 0x60D5, 0x0000    @ Gaia Soul the Combustible Collectiv     [密码: 51355346]
    .hword 0x60D9, 0x0000    @ Fox Fire     [密码: 88753985]
    .hword 0x6105, 0x0000    @ Necklace of Command     [密码: 48576971]
    .hword 0x6381, 0x0000    @ Infernal Flame Emperor     [密码: 19847532]

@ -----------------------------------------------------------------------------
@ Fury from the Deep
@ GBA地址: 0x09E5FBB4  ROM偏移: 0x1E5FBB4
@ 32 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
fury_from_the_deep:
    .hword 0x4579, 0x0000    @ 7 Colored Fish     [密码: 23771716]
    .hword 0x46C9, 0x0000    @ Star Boy     [密码: 08201910]
    .hword 0x4BB1, 0x0000    @ Pot of Greed     [密码: 55144522]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4C89, 0x0000    @ Snatch Steal     [密码: 45986603]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4CFB, 0x0000    @ Mother Grizzly x3  [密码: 57839750]
    .hword 0x4D99, 0x0000    @ Premature Burial     [密码: 70828912]
    .hword 0x4DF1, 0x0000    @ Dust Tornado     [密码: 60082869]
    .hword 0x4DF5, 0x0000    @ Call of the Haunted     [密码: 97077563]
    .hword 0x4FDD, 0x0000    @ Tornado Wall     [密码: 18605135]
    .hword 0x4FE9, 0x0000    @ Torrential Tribute     [密码: 53582587]
    .hword 0x503A, 0x0000    @ Gravity Bind x2  [密码: 85742772]
    .hword 0x50A9, 0x0000    @ Creature Swap     [密码: 31036355]
    .hword 0x542F, 0x0000    @ A Legendary Ocean x3  [密码: 00295517]
    .hword 0x57C5, 0x0000    @ Spell Shield Type-8     [密码: 38275183]
    .hword 0x5871, 0x0000    @ Tribe-Infecting Virus     [密码: 33184167]
    .hword 0x5B1A, 0x0000    @ Fenrir x2  [密码: 00218704]
    .hword 0x5B66, 0x0000    @ Reload x2  [密码: 22589918]
    .hword 0x5BC9, 0x0000    @ Sea Serpent Warrior of Darkness     [密码: 42071342]
    .hword 0x5C15, 0x0000    @ Amphibious Bugroth MK-3     [密码: 64342551]
    .hword 0x5C1D, 0x0000    @ Levia-Dragon - Daedalus     [密码: 37721209]
    .hword 0x5C52, 0x0000    @ Salvage x2  [密码: 96947648]
    .hword 0x5D3D, 0x0000    @ Mermaid Knight     [密码: 24435369]
    .hword 0x5F89, 0x0000    @ Mobius the Frost Monarch     [密码: 04929256]
    .hword 0x5FA1, 0x0000    @ Unshaven Angler     [密码: 92084010]
    .hword 0x5FC9, 0x0000    @ Hammer Shot     [密码: 26412047]
    .hword 0x5FE5, 0x0000    @ Big Wave Small Wave     [密码: 51562916]
    .hword 0x60C9, 0x0000    @ Creeping Doom Manta     [密码: 52571838]
    .hword 0x6129, 0x0000    @ Xing Zhen Hu     [密码: 76515293]
    .hword 0x6161, 0x0000    @ Space Mambo     [密码: 36119641]
    .hword 0x63A1, 0x0000    @ Ocean Dragon Lord - Neo-Daedalus     [密码: 10485110]

@ -----------------------------------------------------------------------------
@ Warrior's Triumph
@ GBA地址: 0x09E5FC34  ROM偏移: 0x1E5FC34
@ 36 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
warriors_triumph:
    .hword 0x4BF9, 0x0000    @ Magic Jammer     [密码: 77414722]
    .hword 0x4C09, 0x0000    @ Royal Decree     [密码: 51452091]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4C89, 0x0000    @ Snatch Steal     [密码: 45986603]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4CB9, 0x0000    @ Giant Trunade     [密码: 42703248]
    .hword 0x4DF5, 0x0000    @ Call of the Haunted     [密码: 97077563]
    .hword 0x4E65, 0x0000    @ Command Knight     [密码: 10375182]
    .hword 0x4F0E, 0x0000    @ Gearfried the Iron Knight x2  [密码: 00423705]
    .hword 0x4FD9, 0x0000    @ Lightning Blade     [密码: 55226821]
    .hword 0x5065, 0x0000    @ Goblin Attack Force     [密码: 78658564]
    .hword 0x5185, 0x0000    @ Lightning Vortex     [密码: 69162969]
    .hword 0x51ED, 0x0000    @ Swift Gaia the Fierce Knight     [密码: 16589042]
    .hword 0x51F1, 0x0000    @ Obnoxious Celtic Guard     [密码: 52077741]
    .hword 0x531A, 0x0000    @ Marauding Captain x2  [密码: 02460565]
    .hword 0x532D, 0x0000    @ Exiled Force     [密码: 74131780]
    .hword 0x5342, 0x0000    @ Reinforcement of the Army x2  [密码: 32807846]
    .hword 0x5349, 0x0000    @ The Warrior Returning Alive     [密码: 95281259]
    .hword 0x5431, 0x0000    @ Fusion Sword Murasame Blade     [密码: 37684215]
    .hword 0x5451, 0x0000    @ Blast with Chain     [密码: 98239899]
    .hword 0x5735, 0x0000    @ Dark Blade     [密码: 11321183]
    .hword 0x595D, 0x0000    @ D.D. Warrior Lady     [密码: 07572887]
    .hword 0x597D, 0x0000    @ Wicked-Breaking Flamberge - Baou     [密码: 68427465]
    .hword 0x5991, 0x0000    @ Fairy of the Spring     [密码: 20188127]
    .hword 0x5B66, 0x0000    @ Reload x2  [密码: 22589918]
    .hword 0x5C29, 0x0000    @ Mataza the Zapper     [密码: 22609617]
    .hword 0x5F5D, 0x0000    @ Mystic Swordsman LV2     [密码: 47507260]
    .hword 0x5F61, 0x0000    @ Mystic Swordsman LV4     [密码: 74591968]
    .hword 0x5F7D, 0x0000    @ Ninja Grandmaster Sasuke     [密码: 04041838]
    .hword 0x61AD, 0x0000    @ Gearfried the Swordmaster     [密码: 57046845]
    .hword 0x61B1, 0x0000    @ Armed Samurai - Ben Kei     [密码: 84430950]
    .hword 0x61F1, 0x0000    @ Swords of Concealing Light     [密码: 12923641]
    .hword 0x61F9, 0x0000    @ Release Restraint     [密码: 75417459]
    .hword 0x64E1, 0x0000    @ Gilford the Legend     [密码: 69933858]
    .hword 0x64E5, 0x0000    @ Warrior Lady of the Wasteland     [密码: 05438492]
    .hword 0x64E9, 0x0000    @ Divine Sword - Phoenix Blade     [密码: 31423101]

@ -----------------------------------------------------------------------------
@ Spellcaster's Judgement
@ GBA地址: 0x09E5FCC4  ROM偏移: 0x1E5FCC4
@ 36 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
spellcasters_judgement:
    .hword 0x3F25, 0x0000    @ Dark Magician     [密码: 46986414]
    .hword 0x4409, 0x0000    @ Swords of Revealing Light     [密码: 72302403]
    .hword 0x454A, 0x0000    @ Magician of Faith x2  [密码: 31560081]
    .hword 0x46E9, 0x0000    @ Gemini Elf     [密码: 69140098]
    .hword 0x4C6D, 0x0000    @ Heavy Storm     [密码: 19613556]
    .hword 0x4CB5, 0x0000    @ Mystical Space Typhoon     [密码: 05318639]
    .hword 0x4D8D, 0x0000    @ Nobleman of Crossout     [密码: 71044499]
    .hword 0x4D99, 0x0000    @ Premature Burial     [密码: 70828912]
    .hword 0x4DF5, 0x0000    @ Call of the Haunted     [密码: 97077563]
    .hword 0x5001, 0x0000    @ Nightmare's Steelcage     [密码: 58775978]
    .hword 0x5011, 0x0000    @ Magic Cylinder     [密码: 62279055]
    .hword 0x50C1, 0x0000    @ Mystic Box     [密码: 25774450]
    .hword 0x5175, 0x0000    @ Mage Power     [密码: 83746708]
    .hword 0x5185, 0x0000    @ Lightning Vortex     [密码: 69162969]
    .hword 0x57C5, 0x0000    @ Spell Shield Type-8     [密码: 38275183]
    .hword 0x57F9, 0x0000    @ Spell Absorption     [密码: 51481927]
    .hword 0x57FD, 0x0000    @ Diffusion Wave-Motion     [密码: 87880531]
    .hword 0x5846, 0x0000    @ Skilled Dark Magician x2  [密码: 73752131]
    .hword 0x584A, 0x0000    @ Apprentice Magician x2  [密码: 09156135]
    .hword 0x5851, 0x0000    @ Chaos Command Magician     [密码: 72630549]
    .hword 0x585D, 0x0000    @ Breaker the Magical Warrior     [密码: 71413901]
    .hword 0x5869, 0x0000    @ Royal Magical Library     [密码: 70791313]
    .hword 0x5891, 0x0000    @ Pitch-Black Power Stone     [密码: 34029630]
    .hword 0x59E2, 0x0000    @ Magical Dimension x2  [密码: 28553439]
    .hword 0x5A51, 0x0000    @ Tsukuyomi     [密码: 34853266]
    .hword 0x5B25, 0x0000    @ Chaos Sorcerer     [密码: 09596126]
    .hword 0x5B65, 0x0000    @ Reload     [密码: 22589918]
    .hword 0x5D5D, 0x0000    @ White Magician Pikeru     [密码: 81383947]
    .hword 0x5EA5, 0x0000    @ Dark Magic Attack     [密码: 02314238]
    .hword 0x6125, 0x0000    @ Divine Wrath     [密码: 49010598]
    .hword 0x61A9, 0x0000    @ Blast Magician     [密码: 21051146]
    .hword 0x6475, 0x0000    @ Ebon Magician Curran     [密码: 46128076]
    .hword 0x6591, 0x0000    @ Rapid-Fire Magician     [密码: 06337436]
    .hword 0x6609, 0x0000    @ Dark Eradicator Warlock     [密码: 29436665]
    .hword 0x660D, 0x0000    @ Mythical Beast Cerberus     [密码: 55424270]
    .hword 0x6611, 0x0000    @ Magical Blast     [密码: 91819979]

@ -----------------------------------------------------------------------------
@ 结构卡组指针表
@ GBA地址: 0x09E5FD54  ROM偏移: 0x1E5FD54
@ 格式: [卡组GBA地址 LE32][槽位数 LE32]
@ -----------------------------------------------------------------------------
struct_deck_table:
    .word 0x09E5FA58, 0x0000001C    @ Dragon's Roar (28 槽)
    .word 0x09E5FAC8, 0x0000001C    @ Zombie Madness (28 槽)
    .word 0x09E5FB38, 0x0000001F    @ Molten Destruction (31 槽)
    .word 0x09E5FBB4, 0x00000020    @ Fury from the Deep (32 槽)
    .word 0x09E5FC34, 0x00000024    @ Warrior's Triumph (36 槽)
    .word 0x09E5FCC4, 0x00000024    @ Spellcaster's Judgement (36 槽)
