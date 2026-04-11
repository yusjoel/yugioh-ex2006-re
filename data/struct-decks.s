@ =============================================================================
@ 预组数据
@ ROM偏移: 0x1E5FA58 - 0x1E5FD84 (共 0x32C = 812 字节)
@
@ 卡牌编码格式 (每条 4 字节):
@   字节 0-1: so_code * 4 | 副本数量  [小端 16 位]，通过 deck_entry 宏生成
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
        deck_entry  4088, 1    @ Red-Eyes B. Dragon (密码: 74677422)
        deck_entry  4354, 1    @ Swords of Revealing Light (密码: 72302403)
        deck_entry  4844, 1    @ Pot of Greed (密码: 55144522)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4898, 1    @ Snatch Steal (密码: 45986603)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4956, 1    @ Ceasefire (密码: 36468556)
        deck_entry  4963, 2    @ Nobleman of Crossout ×2 (密码: 71044499)
        deck_entry  4966, 1    @ Premature Burial (密码: 70828912)
        deck_entry  4989, 1    @ Call of the Haunted (密码: 97077563)
        deck_entry  5030, 1    @ Twin-Headed Behemoth (密码: 43586926)
        deck_entry  5162, 2    @ Creature Swap ×2 (密码: 31036355)
        deck_entry  5342, 1    @ The Dragon's Bead (密码: 92408984)
        deck_entry  5345, 3    @ Stamping Destruction ×3 (密码: 81385346)
        deck_entry  5347, 2    @ Dragon's Rage ×2 (密码: 54178050)
        deck_entry  5448, 1    @ Reckless Greed (密码: 37576645)
        deck_entry  5560, 2    @ Interdimensional Matter Transporter ×2 (密码: 36261276)
        deck_entry  5644, 2    @ Luster Dragon ×2 (密码: 11091375)
        deck_entry  5849, 2    @ Reload ×2 (密码: 22589918)
        deck_entry  5921, 1    @ Trap Jammer (密码: 19252988)
        deck_entry  6067, 1    @ Curse of Anubis (密码: 66742250)
        deck_entry  6105, 2    @ Armed Dragon LV3 ×2 (密码: 00980973)
        deck_entry  6106, 2    @ Armed Dragon LV5 ×2 (密码: 46384672)
        deck_entry  6109, 1    @ Red-Eyes B. Chick (密码: 36262024)
        deck_entry  6115, 1    @ Element Dragon (密码: 30314994)
        deck_entry  6118, 3    @ Masked Dragon ×3 (密码: 39191307)
        deck_entry  6135, 1    @ The Graveyard in the Fourth Dimension (密码: 88089103)
        deck_entry  6292, 1    @ Red-Eyes Darkness Dragon (密码: 96561011)

@ -----------------------------------------------------------------------------
@ Zombie Madness
@ GBA地址: 0x09E5FAC8  ROM偏移: 0x1E5FAC8
@ 28 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
zombie_madness:
        deck_entry  4844, 1    @ Pot of Greed (密码: 55144522)
        deck_entry  4862, 1    @ Magic Jammer (密码: 77414722)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4898, 1    @ Snatch Steal (密码: 45986603)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4910, 1    @ Giant Trunade (密码: 42703248)
        deck_entry  4963, 1    @ Nobleman of Crossout (密码: 71044499)
        deck_entry  4988, 1    @ Dust Tornado (密码: 60082869)
        deck_entry  5114, 1    @ Torrential Tribute (密码: 53582587)
        deck_entry  5123, 1    @ Card of Safe Return (密码: 57953380)
        deck_entry  5162, 2    @ Creature Swap ×2 (密码: 31036355)
        deck_entry  5410, 1    @ Vampire Lord (密码: 53839837)
        deck_entry  5414, 1    @ Dark Dust Spirit (密码: 89111398)
        deck_entry  5423, 3    @ Pyramid Turtle ×3 (密码: 77044671)
        deck_entry  5430, 2    @ Book of Life ×2 (密码: 02204140)
        deck_entry  5435, 3    @ Call of the Mummy ×3 (密码: 04861205)
        deck_entry  5448, 1    @ Reckless Greed (密码: 37576645)
        deck_entry  5506, 1    @ Master Kyonshee (密码: 24530661)
        deck_entry  5526, 1    @ Spirit Reaper (密码: 23205979)
        deck_entry  5715, 2    @ Despair from the Dark ×2 (密码: 71200730)
        deck_entry  5849, 2    @ Reload ×2 (密码: 22589918)
        deck_entry  5902, 2    @ Ryu Kokki ×2 (密码: 57281778)
        deck_entry  5914, 3    @ Compulsory Evacuation Device ×3 (密码: 94192409)
        deck_entry  5956, 1    @ Soul-Absorbing Bone Tower (密码: 63012333)
        deck_entry  5958, 1    @ Vampire Lady (密码: 26495087)
        deck_entry  6040, 1    @ Double Coston (密码: 44436472)
        deck_entry  6041, 2    @ Regenerating Mummy ×2 (密码: 70821187)
        deck_entry  6293, 1    @ Vampire Genesis (密码: 22056710)

@ -----------------------------------------------------------------------------
@ Molten Destruction
@ GBA地址: 0x09E5FB38  ROM偏移: 0x1E5FB38
@ 31 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
molten_destruction:
        deck_entry  4604, 1    @ Little Chimera (密码: 68658728)
        deck_entry  4844, 1    @ Pot of Greed (密码: 55144522)
        deck_entry  4856, 1    @ Tribute to The Doomed (密码: 79759861)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4898, 1    @ Snatch Steal (密码: 45986603)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4917, 3    @ UFO Turtle ×3 (密码: 60806437)
        deck_entry  4934, 2    @ Molten Destruction ×2 (密码: 19384334)
        deck_entry  4963, 1    @ Nobleman of Crossout (密码: 71044499)
        deck_entry  4966, 1    @ Premature Burial (密码: 70828912)
        deck_entry  4988, 2    @ Dust Tornado ×2 (密码: 60082869)
        deck_entry  4989, 1    @ Call of the Haunted (密码: 97077563)
        deck_entry  5210, 1    @ Jar of Greed (密码: 83968380)
        deck_entry  5216, 1    @ Meteor of Destruction (密码: 33767325)
        deck_entry  5531, 1    @ Dark Room of Nightmare (密码: 85562745)
        deck_entry  5617, 1    @ Spell Shield Type-8 (密码: 38275183)
        deck_entry  5641, 1    @ Great Angus (密码: 11813953)
        deck_entry  5829, 2    @ Inferno ×2 (密码: 74823665)
        deck_entry  5849, 1    @ Reload (密码: 22589918)
        deck_entry  5876, 1    @ Blazing Inpachi (密码: 05464695)
        deck_entry  5879, 1    @ Molten Zombie (密码: 04732017)
        deck_entry  5974, 2    @ Solar Flare Dragon ×2 (密码: 45985838)
        deck_entry  5986, 2    @ Backfire ×2 (密码: 82705573)
        deck_entry  6054, 2    @ Level Limit - Area B ×2 (密码: 03136426)
        deck_entry  6113, 2    @ Ultimate Baseball Kid ×2 (密码: 67934141)
        deck_entry  6189, 1    @ Raging Flame Sprite (密码: 90810762)
        deck_entry  6190, 1    @ Thestalos the Firestorm Monarch (密码: 26205777)
        deck_entry  6197, 1    @ Gaia Soul the Combustible Collective (密码: 51355346)
        deck_entry  6198, 1    @ Fox Fire (密码: 88753985)
        deck_entry  6209, 1    @ Necklace of Command (密码: 48576971)
        deck_entry  6368, 1    @ Infernal Flame Emperor (密码: 19847532)

@ -----------------------------------------------------------------------------
@ Fury from the Deep
@ GBA地址: 0x09E5FBB4  ROM偏移: 0x1E5FBB4
@ 32 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
fury_from_the_deep:
        deck_entry  4446, 1    @ 7 Colored Fish (密码: 23771716)
        deck_entry  4530, 1    @ Star Boy (密码: 08201910)
        deck_entry  4844, 1    @ Pot of Greed (密码: 55144522)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4898, 1    @ Snatch Steal (密码: 45986603)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4926, 3    @ Mother Grizzly ×3 (密码: 57839750)
        deck_entry  4966, 1    @ Premature Burial (密码: 70828912)
        deck_entry  4988, 1    @ Dust Tornado (密码: 60082869)
        deck_entry  4989, 1    @ Call of the Haunted (密码: 97077563)
        deck_entry  5111, 1    @ Tornado Wall (密码: 18605135)
        deck_entry  5114, 1    @ Torrential Tribute (密码: 53582587)
        deck_entry  5134, 2    @ Gravity Bind ×2 (密码: 85742772)
        deck_entry  5162, 1    @ Creature Swap (密码: 31036355)
        deck_entry  5387, 3    @ A Legendary Ocean ×3 (密码: 00295517)
        deck_entry  5617, 1    @ Spell Shield Type-8 (密码: 38275183)
        deck_entry  5660, 1    @ Tribe-Infecting Virus (密码: 33184167)
        deck_entry  5830, 2    @ Fenrir ×2 (密码: 00218704)
        deck_entry  5849, 2    @ Reload ×2 (密码: 22589918)
        deck_entry  5874, 1    @ Sea Serpent Warrior of Darkness (密码: 42071342)
        deck_entry  5893, 1    @ Amphibious Bugroth MK-3 (密码: 64342551)
        deck_entry  5895, 1    @ Levia-Dragon - Daedalus (密码: 37721209)
        deck_entry  5908, 2    @ Salvage ×2 (密码: 96947648)
        deck_entry  5967, 1    @ Mermaid Knight (密码: 24435369)
        deck_entry  6114, 1    @ Mobius the Frost Monarch (密码: 04929256)
        deck_entry  6120, 1    @ Unshaven Angler (密码: 92084010)
        deck_entry  6130, 1    @ Hammer Shot (密码: 26412047)
        deck_entry  6137, 1    @ Big Wave Small Wave (密码: 51562916)
        deck_entry  6194, 1    @ Creeping Doom Manta (密码: 52571838)
        deck_entry  6218, 1    @ Xing Zhen Hu (密码: 76515293)
        deck_entry  6232, 1    @ Space Mambo (密码: 36119641)
        deck_entry  6376, 1    @ Ocean Dragon Lord - Neo-Daedalus (密码: 10485110)

@ -----------------------------------------------------------------------------
@ Warrior's Triumph
@ GBA地址: 0x09E5FC34  ROM偏移: 0x1E5FC34
@ 36 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
warriors_triumph:
        deck_entry  4862, 1    @ Magic Jammer (密码: 77414722)
        deck_entry  4866, 1    @ Royal Decree (密码: 51452091)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4898, 1    @ Snatch Steal (密码: 45986603)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4910, 1    @ Giant Trunade (密码: 42703248)
        deck_entry  4989, 1    @ Call of the Haunted (密码: 97077563)
        deck_entry  5017, 1    @ Command Knight (密码: 10375182)
        deck_entry  5059, 2    @ Gearfried the Iron Knight ×2 (密码: 00423705)
        deck_entry  5110, 1    @ Lightning Blade (密码: 55226821)
        deck_entry  5145, 1    @ Goblin Attack Force (密码: 78658564)
        deck_entry  5217, 1    @ Lightning Vortex (密码: 69162969)
        deck_entry  5243, 1    @ Swift Gaia the Fierce Knight (密码: 16589042)
        deck_entry  5244, 1    @ Obnoxious Celtic Guard (密码: 52077741)
        deck_entry  5318, 2    @ Marauding Captain ×2 (密码: 02460565)
        deck_entry  5323, 1    @ Exiled Force (密码: 74131780)
        deck_entry  5328, 2    @ Reinforcement of the Army ×2 (密码: 32807846)
        deck_entry  5330, 1    @ The Warrior Returning Alive (密码: 95281259)
        deck_entry  5388, 1    @ Fusion Sword Murasame Blade (密码: 37684215)
        deck_entry  5396, 1    @ Blast with Chain (密码: 98239899)
        deck_entry  5581, 1    @ Dark Blade (密码: 11321183)
        deck_entry  5719, 1    @ D.D. Warrior Lady (密码: 07572887)
        deck_entry  5727, 1    @ Wicked-Breaking Flamberge - Baou (密码: 68427465)
        deck_entry  5732, 1    @ Fairy of the Spring (密码: 20188127)
        deck_entry  5849, 2    @ Reload ×2 (密码: 22589918)
        deck_entry  5898, 1    @ Mataza the Zapper (密码: 22609617)
        deck_entry  6103, 1    @ Mystic Swordsman LV2 (密码: 47507260)
        deck_entry  6104, 1    @ Mystic Swordsman LV4 (密码: 74591968)
        deck_entry  6111, 1    @ Ninja Grandmaster Sasuke (密码: 04041838)
        deck_entry  6251, 1    @ Gearfried the Swordmaster (密码: 57046845)
        deck_entry  6252, 1    @ Armed Samurai - Ben Kei (密码: 84430950)
        deck_entry  6268, 1    @ Swords of Concealing Light (密码: 12923641)
        deck_entry  6270, 1    @ Release Restraint (密码: 75417459)
        deck_entry  6456, 1    @ Gilford the Legend (密码: 69933858)
        deck_entry  6457, 1    @ Warrior Lady of the Wasteland (密码: 05438492)
        deck_entry  6458, 1    @ Divine Sword - Phoenix Blade (密码: 31423101)

@ -----------------------------------------------------------------------------
@ Spellcaster's Judgement
@ GBA地址: 0x09E5FCC4  ROM偏移: 0x1E5FCC4
@ 36 种牌型, 共 40 张
@ -----------------------------------------------------------------------------
spellcasters_judgement:
        deck_entry  4041, 1    @ Dark Magician (密码: 46986414)
        deck_entry  4354, 1    @ Swords of Revealing Light (密码: 72302403)
        deck_entry  4434, 2    @ Magician of Faith ×2 (密码: 31560081)
        deck_entry  4538, 1    @ Gemini Elf (密码: 69140098)
        deck_entry  4891, 1    @ Heavy Storm (密码: 19613556)
        deck_entry  4909, 1    @ Mystical Space Typhoon (密码: 05318639)
        deck_entry  4963, 1    @ Nobleman of Crossout (密码: 71044499)
        deck_entry  4966, 1    @ Premature Burial (密码: 70828912)
        deck_entry  4989, 1    @ Call of the Haunted (密码: 97077563)
        deck_entry  5120, 1    @ Nightmare's Steelcage (密码: 58775978)
        deck_entry  5124, 1    @ Magic Cylinder (密码: 62279055)
        deck_entry  5168, 1    @ Mystic Box (密码: 25774450)
        deck_entry  5213, 1    @ Mage Power (密码: 83746708)
        deck_entry  5217, 1    @ Lightning Vortex (密码: 69162969)
        deck_entry  5617, 1    @ Spell Shield Type-8 (密码: 38275183)
        deck_entry  5630, 1    @ Spell Absorption (密码: 51481927)
        deck_entry  5631, 1    @ Diffusion Wave-Motion (密码: 87880531)
        deck_entry  5649, 2    @ Skilled Dark Magician ×2 (密码: 73752131)
        deck_entry  5650, 2    @ Apprentice Magician ×2 (密码: 09156135)
        deck_entry  5652, 1    @ Chaos Command Magician (密码: 72630549)
        deck_entry  5655, 1    @ Breaker the Magical Warrior (密码: 71413901)
        deck_entry  5658, 1    @ Royal Magical Library (密码: 70791313)
        deck_entry  5668, 1    @ Pitch-Black Power Stone (密码: 34029630)
        deck_entry  5752, 2    @ Magical Dimension ×2 (密码: 28553439)
        deck_entry  5780, 1    @ Tsukuyomi (密码: 34853266)
        deck_entry  5833, 1    @ Chaos Sorcerer (密码: 09596126)
        deck_entry  5849, 1    @ Reload (密码: 22589918)
        deck_entry  5975, 1    @ White Magician Pikeru (密码: 81383947)
        deck_entry  6057, 1    @ Dark Magic Attack (密码: 02314238)
        deck_entry  6217, 1    @ Divine Wrath (密码: 49010598)
        deck_entry  6250, 1    @ Blast Magician (密码: 21051146)
        deck_entry  6429, 1    @ Ebon Magician Curran (密码: 46128076)
        deck_entry  6500, 1    @ Rapid-Fire Magician (密码: 06337436)
        deck_entry  6530, 1    @ Dark Eradicator Warlock (密码: 29436665)
        deck_entry  6531, 1    @ Mythical Beast Cerberus (密码: 55424270)
        deck_entry  6532, 1    @ Magical Blast (密码: 91819979)

@ -----------------------------------------------------------------------------
@ 预组指针表
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
