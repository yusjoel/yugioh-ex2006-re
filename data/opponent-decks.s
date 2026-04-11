@ =============================================================================
@ 对手卡组数据（Opponent Decks）
@ ROM偏移: 0x1E6468E - 0x1E65A45
@
@ 格式: [so_code LE16] 连续排列，以 0x0000 终止，后跟融合卡组数据和填充
@ 对手卡组均为 40 张牌（重复条目表示多张副本）
@
@ 来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md
@ =============================================================================

@ -----------------------------------------------------------------------------
@ Kuriboh
@ GBA地址: 0x09E6468E  ROM偏移: 0x1E6468E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_kuriboh:
    deck_card  4007    @ Blue-Eyes White Dragon                        (密码: 89631139)
    deck_card  4041    @ Dark Magician                                 (密码: 46986414)
    deck_card  4088    @ Red-Eyes B. Dragon                            (密码: 74677422)
    deck_card  4385    @ La Jinn the Mystical Genie of the Lamp        (密码: 97590747)
    deck_card  4385    @ La Jinn the Mystical Genie of the Lamp        (密码: 97590747)
    deck_card  4008    @ Mystical Elf                                  (密码: 15025844)
    deck_card  5067    @ Rocket Warrior                                (密码: 30860696)
    deck_card  4499    @ Maha Vailo                                    (密码: 93013676)
    deck_card  4499    @ Maha Vailo                                    (密码: 93013676)
    deck_card  6040    @ Double Coston                                 (密码: 44436472)
    deck_card  6040    @ Double Coston                                 (密码: 44436472)
    deck_card  5059    @ Gearfried the Iron Knight                     (密码: 00423705)
    deck_card  5059    @ Gearfried the Iron Knight                     (密码: 00423705)
    deck_card  4764    @ Big Shield Gardna                             (密码: 65240384)
    deck_card  4762    @ Reflect Bounder                               (密码: 02851070)
    deck_card  4080    @ Giant Soldier of Stone                        (密码: 13039848)
    deck_card  4080    @ Giant Soldier of Stone                        (密码: 13039848)
    deck_card  4064    @ Kuriboh                                       (密码: 40640057)
    deck_card  4064    @ Kuriboh                                       (密码: 40640057)
    deck_card  4064    @ Kuriboh                                       (密码: 40640057)
    deck_card  6636    @ The Flute of Summoning Kuriboh                (密码: 20065322)
    deck_card  6636    @ The Flute of Summoning Kuriboh                (密码: 20065322)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  4856    @ Tribute to The Doomed                         (密码: 79759861)
    deck_card  4805    @ Multiply                                      (密码: 40703222)
    deck_card  4805    @ Multiply                                      (密码: 40703222)
    deck_card  4310    @ Axe of Despair                                (密码: 40619825)
    deck_card  4310    @ Axe of Despair                                (密码: 40619825)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4354    @ Swords of Revealing Light                     (密码: 72302403)
    deck_card  4317    @ Black Pendant                                 (密码: 65169794)
    deck_card  4838    @ Remove Trap                                   (密码: 51482758)
    deck_card  4849    @ Reinforcements                                (密码: 17814387)
    deck_card  4836    @ Trap Hole                                     (密码: 04206964)
    deck_card  4804    @ Negate Attack                                 (密码: 14315573)
    deck_card  5124    @ Magic Cylinder                                (密码: 62279055)
    deck_card  4664    @ Metalmorph                                    (密码: 68540058)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0xA7, 0x0F
    .byte 0xC9, 0x0F, 0xF8, 0x0F, 0x21, 0x11, 0x21, 0x11, 0xA8, 0x0F, 0xCB, 0x13, 0x93, 0x11, 0x93, 0x11
    .byte 0x98, 0x17, 0x98, 0x17, 0xC3, 0x13, 0xC3, 0x13, 0x9C, 0x12, 0x9A, 0x12, 0xF0, 0x0F, 0xF0, 0x0F
    .byte 0xE0, 0x0F, 0xE0, 0x0F, 0xE0, 0x0F, 0xEC, 0x19, 0xEC, 0x19, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0xF8, 0x12, 0xC5, 0x12, 0xC5, 0x12, 0xD6, 0x10, 0xD6, 0x10, 0x66, 0x13, 0x02, 0x11, 0xDD, 0x10
    .byte 0xE6, 0x12, 0xF1, 0x12, 0xE4, 0x12, 0xC4, 0x12, 0x04, 0x14, 0x38, 0x12, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Pikeru
@ GBA地址: 0x09E6474E  ROM偏移: 0x1E6474E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_pikeru:
    deck_card  6170    @ Silent Magician LV8                           (密码: 72443568)
    deck_card  6606    @ Princess Curran                               (密码: 02316186)
    deck_card  6605    @ Princess Pikeru                               (密码: 75917088)
    deck_card  5476    @ Toon Gemini Elf                               (密码: 42386471)
    deck_card  5476    @ Toon Gemini Elf                               (密码: 42386471)
    deck_card  4538    @ Gemini Elf                                    (密码: 69140098)
    deck_card  4538    @ Gemini Elf                                    (密码: 69140098)
    deck_card  5869    @ Magician's Valkyrie                           (密码: 80304126)
    deck_card  5869    @ Magician's Valkyrie                           (密码: 80304126)
    deck_card  5975    @ White Magician Pikeru                         (密码: 81383947)
    deck_card  5975    @ White Magician Pikeru                         (密码: 81383947)
    deck_card  6429    @ Ebon Magician Curran                          (密码: 46128076)
    deck_card  6429    @ Ebon Magician Curran                          (密码: 46128076)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6167    @ Silent Magician LV4                           (密码: 73665146)
    deck_card  5031    @ Injection Fairy Lily                          (密码: 79575620)
    deck_card  5955    @ The Unhappy Girl                              (密码: 27618634)
    deck_card  5955    @ The Unhappy Girl                              (密码: 27618634)
    deck_card  5650    @ Apprentice Magician                           (密码: 09156135)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6616    @ Trial of the Princesses                       (密码: 72709014)
    deck_card  6616    @ Trial of the Princesses                       (密码: 72709014)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  4310    @ Axe of Despair                                (密码: 40619825)
    deck_card  5213    @ Mage Power                                    (密码: 83746708)
    deck_card  4341    @ Yami                                          (密码: 59197169)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  6168    @ Magician's Circle                             (密码: 00050755)
    deck_card  6443    @ A Rival Appears!                              (密码: 05728014)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x1A, 0x18
    .byte 0xCE, 0x19, 0xCD, 0x19, 0x64, 0x15, 0x64, 0x15, 0xBA, 0x11, 0xBA, 0x11, 0xED, 0x16, 0xED, 0x16
    .byte 0x57, 0x17, 0x57, 0x17, 0x1D, 0x19, 0x1D, 0x19, 0xD6, 0x0F, 0x17, 0x18, 0xA7, 0x13, 0x43, 0x17
    .byte 0x43, 0x17, 0x12, 0x16, 0x52, 0x11, 0x52, 0x11, 0xD8, 0x19, 0xD8, 0x19, 0x1B, 0x13, 0x22, 0x13
    .byte 0xEC, 0x12, 0x2D, 0x13, 0x11, 0x17, 0xD2, 0x12, 0xD6, 0x10, 0x5D, 0x14, 0xF5, 0x10, 0x61, 0x14
    .byte 0x7C, 0x13, 0x7C, 0x13, 0x18, 0x15, 0x18, 0x18, 0x2B, 0x19, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Scapegoat
@ GBA地址: 0x09E6480E  ROM偏移: 0x1E6480E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_scapegoat:
    deck_card  6200    @ Fusilier Dragon, the Dual-Mode Beast          (密码: 51632798)
    deck_card  6200    @ Fusilier Dragon, the Dual-Mode Beast          (密码: 51632798)
    deck_card  6200    @ Fusilier Dragon, the Dual-Mode Beast          (密码: 51632798)
    deck_card  6244    @ Behemoth the King of All Animals              (密码: 22996376)
    deck_card  6244    @ Behemoth the King of All Animals              (密码: 22996376)
    deck_card  6599    @ Chainsaw Insect                               (密码: 77252217)
    deck_card  6599    @ Chainsaw Insect                               (密码: 77252217)
    deck_card  5145    @ Goblin Attack Force                           (密码: 78658564)
    deck_card  5145    @ Goblin Attack Force                           (密码: 78658564)
    deck_card  6421    @ Indomitable Fighter Lei Lei                   (密码: 84173492)
    deck_card  6421    @ Indomitable Fighter Lei Lei                   (密码: 84173492)
    deck_card  4373    @ Jirai Gumo                                    (密码: 94773007)
    deck_card  5586    @ Giant Orc                                     (密码: 73698349)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  4108    @ Mask of Darkness                              (密码: 28933734)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  5231    @ Cathedral of Nobles                           (密码: 29762407)
    deck_card  5275    @ Bait Doll                                     (密码: 07165085)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  4910    @ Giant Trunade                                 (密码: 42703248)
    deck_card  6266    @ A Feather of the Phoenix                      (密码: 49140998)
    deck_card  6266    @ A Feather of the Phoenix                      (密码: 49140998)
    deck_card  5232    @ Judgment of Anubis                            (密码: 55256016)
    deck_card  6366    @ Royal Surrender                               (密码: 56058888)
    deck_card  4861    @ Solemn Judgment                               (密码: 41420027)
    deck_card  4861    @ Solemn Judgment                               (密码: 41420027)
    deck_card  5740    @ Skill Drain                                   (密码: 82732705)
    deck_card  5740    @ Skill Drain                                   (密码: 82732705)
    deck_card  5740    @ Skill Drain                                   (密码: 82732705)
    deck_card  4851    @ Ultimate Offering                             (密码: 80604091)
    deck_card  4863    @ Seven Tools of the Bandit                     (密码: 03819470)
    deck_card  4862    @ Magic Jammer                                  (密码: 77414722)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x38, 0x18
    .byte 0x38, 0x18, 0x38, 0x18, 0x64, 0x18, 0x64, 0x18, 0xC7, 0x19, 0xC7, 0x19, 0x19, 0x14, 0x19, 0x14
    .byte 0x15, 0x19, 0x15, 0x19, 0x15, 0x11, 0xD2, 0x15, 0x12, 0x19, 0x12, 0x19, 0xD6, 0x0F, 0x0C, 0x10
    .byte 0x90, 0x15, 0x90, 0x15, 0x90, 0x15, 0x8D, 0x19, 0x8D, 0x19, 0x6F, 0x14, 0x9B, 0x14, 0xEC, 0x12
    .byte 0x2D, 0x13, 0xD2, 0x12, 0x2E, 0x13, 0x7A, 0x18, 0x7A, 0x18, 0x70, 0x14, 0xDE, 0x18, 0xFD, 0x12
    .byte 0xFD, 0x12, 0x6C, 0x16, 0x6C, 0x16, 0x6C, 0x16, 0xF3, 0x12, 0xFF, 0x12, 0xFE, 0x12, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Skull Servant
@ GBA地址: 0x09E648CE  ROM偏移: 0x1E648CE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_skull_servant:
    deck_card  4930    @ Mystic Tomato                                 (密码: 83011277)
    deck_card  5561    @ Goblin Zombie                                 (密码: 63665875)
    deck_card  5561    @ Goblin Zombie                                 (密码: 63665875)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  5323    @ Exiled Force                                  (密码: 74131780)
    deck_card  5882    @ Stealth Bird                                  (密码: 03510565)
    deck_card  5882    @ Stealth Bird                                  (密码: 03510565)
    deck_card  5427    @ Des Lacooda                                   (密码: 02326738)
    deck_card  5427    @ Des Lacooda                                   (密码: 02326738)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4030    @ Skull Servant                                 (密码: 32274490)
    deck_card  4030    @ Skull Servant                                 (密码: 32274490)
    deck_card  4030    @ Skull Servant                                 (密码: 32274490)
    deck_card  4754    @ Stone Statue of the Aztecs                    (密码: 31812496)
    deck_card  4754    @ Stone Statue of the Aztecs                    (密码: 31812496)
    deck_card  6341    @ King of the Skull Servants                    (密码: 36021814)
    deck_card  6341    @ King of the Skull Servants                    (密码: 36021814)
    deck_card  6341    @ King of the Skull Servants                    (密码: 36021814)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  5236    @ Foolish Burial                                (密码: 81439173)
    deck_card  5977    @ Opti-Camouflage Armor                         (密码: 44762290)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  5849    @ Reload                                        (密码: 22589918)
    deck_card  5849    @ Reload                                        (密码: 22589918)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  6520    @ The League of Uniform Nomenclature            (密码: 55008284)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  6620    @ Next to be Lost                               (密码: 07076131)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x42, 0x13
    .byte 0xB9, 0x15, 0xB9, 0x15, 0xD6, 0x0F, 0xCB, 0x14, 0xFA, 0x16, 0xFA, 0x16, 0x33, 0x15, 0x33, 0x15
    .byte 0x96, 0x15, 0x96, 0x15, 0x52, 0x11, 0xBE, 0x0F, 0xBE, 0x0F, 0xBE, 0x0F, 0x92, 0x12, 0x92, 0x12
    .byte 0xC5, 0x18, 0xC5, 0x18, 0xC5, 0x18, 0x1B, 0x13, 0x74, 0x14, 0x59, 0x17, 0xEC, 0x12, 0x2D, 0x13
    .byte 0x11, 0x17, 0x11, 0x17, 0x66, 0x13, 0x61, 0x14, 0xD9, 0x16, 0xD9, 0x16, 0xA6, 0x17, 0xA6, 0x17
    .byte 0x0E, 0x14, 0x0E, 0x14, 0x7C, 0x13, 0x7C, 0x13, 0x78, 0x19, 0x7D, 0x13, 0xDC, 0x19, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Watapon
@ GBA地址: 0x09E6498E  ROM偏移: 0x1E6498E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_watapon:
    deck_card  5965    @ Zaborg the Thunder Monarch                    (密码: 51945556)
    deck_card  6164    @ Silent Swordsman LV5                          (密码: 74388798)
    deck_card  5251    @ Soul of Purity and Light                      (密码: 77527210)
    deck_card  5023    @ Airknight Parshath                            (密码: 18036057)
    deck_card  4786    @ Dunames Dark Witch                            (密码: 12493482)
    deck_card  6111    @ Ninja Grandmaster Sasuke                      (密码: 04041838)
    deck_card  6111    @ Ninja Grandmaster Sasuke                      (密码: 04041838)
    deck_card  5381    @ Asura Priest                                  (密码: 02134346)
    deck_card  4762    @ Reflect Bounder                               (密码: 02851070)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  4924    @ Shining Angel                                 (密码: 95956346)
    deck_card  4924    @ Shining Angel                                 (密码: 95956346)
    deck_card  6162    @ Silent Swordsman LV3                          (密码: 01995985)
    deck_card  6162    @ Silent Swordsman LV3                          (密码: 01995985)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6000    @ Marshmallon                                   (密码: 31305911)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6092    @ Watapon                                       (密码: 87774234)
    deck_card  5658    @ Royal Magical Library                         (密码: 70791313)
    deck_card  4795    @ Copycat                                       (密码: 26376390)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  6213    @ Monster Reincarnation                         (密码: 74848038)
    deck_card  5982    @ The Sanctuary in the Sky                      (密码: 56433456)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  4354    @ Swords of Revealing Light                     (密码: 72302403)
    deck_card  4964    @ Nobleman of Extermination                     (密码: 17449108)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  6546    @ Mistobody                                     (密码: 47529357)
    deck_card  5544    @ Raigeki Break                                 (密码: 04178474)
    deck_card  4863    @ Seven Tools of the Bandit                     (密码: 03819470)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  4692    @ Widespread Ruin                               (密码: 77754944)
    deck_card  5990    @ Wall of Revealing Light                       (密码: 17078030)
    deck_card  5993    @ Beckoning Light                               (密码: 16255442)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x4D, 0x17
    .byte 0x14, 0x18, 0x83, 0x14, 0x9F, 0x13, 0xB2, 0x12, 0xDF, 0x17, 0xDF, 0x17, 0x05, 0x15, 0x9A, 0x12
    .byte 0x57, 0x16, 0x3C, 0x13, 0x3C, 0x13, 0x12, 0x18, 0x12, 0x18, 0xD6, 0x0F, 0x70, 0x17, 0x52, 0x11
    .byte 0xCC, 0x17, 0x1A, 0x16, 0xBB, 0x12, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0x11, 0x17
    .byte 0x45, 0x18, 0x5E, 0x17, 0xF2, 0x17, 0x02, 0x11, 0x64, 0x13, 0x63, 0x13, 0x92, 0x19, 0xA8, 0x15
    .byte 0xFF, 0x12, 0x18, 0x15, 0x54, 0x12, 0x66, 0x17, 0x69, 0x17, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Batteryman C
@ GBA地址: 0x09E64A4E  ROM偏移: 0x1E64A4E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_batteryman_c:
    deck_card  6315    @ Ancient Gear Golem                            (密码: 83104731)
    deck_card  5804    @ Perfect Machine King                          (密码: 18891691)
    deck_card  4413    @ Machine King                                  (密码: 46700124)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    deck_card  4421    @ Mechanicalchaser                              (密码: 07359741)
    deck_card  6590    @ Machine King Prototype                        (密码: 89222931)
    deck_card  6387    @ Drillroid                                     (密码: 71218746)
    deck_card  6121    @ The Trojan Horse                              (密码: 38479725)
    deck_card  6121    @ The Trojan Horse                              (密码: 38479725)
    deck_card  6385    @ Gyroid                                        (密码: 18325492)
    deck_card  6181    @ Heavy Mech Support Platform                   (密码: 23265594)
    deck_card  6181    @ Heavy Mech Support Platform                   (密码: 23265594)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6428    @ Batteryman C                                  (密码: 19733961)
    deck_card  6428    @ Batteryman C                                  (密码: 19733961)
    deck_card  6428    @ Batteryman C                                  (密码: 19733961)
    deck_card  6339    @ Batteryman AA                                 (密码: 63142001)
    deck_card  6339    @ Batteryman AA                                 (密码: 63142001)
    deck_card  6339    @ Batteryman AA                                 (密码: 63142001)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  6542    @ Inferno Reckless Summon                       (密码: 12247206)
    deck_card  6542    @ Inferno Reckless Summon                       (密码: 12247206)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  6348    @ Battery Charger                               (密码: 61181383)
    deck_card  6348    @ Battery Charger                               (密码: 61181383)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  5129    @ Limiter Removal                               (密码: 23171610)
    deck_card  6521    @ Roll Out!                                     (密码: 91597389)
    deck_card  6521    @ Roll Out!                                     (密码: 91597389)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4951    @ DNA Surgery                                   (密码: 74701381)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  6219    @ Rare Metalmorph                               (密码: 12503902)
    deck_card  6219    @ Rare Metalmorph                               (密码: 12503902)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0xAB, 0x18
    .byte 0xAC, 0x16, 0x3D, 0x11, 0xF6, 0x18, 0xF6, 0x18, 0x45, 0x11, 0xBE, 0x19, 0xF3, 0x18, 0xE9, 0x17
    .byte 0xE9, 0x17, 0xF1, 0x18, 0x25, 0x18, 0x25, 0x18, 0x52, 0x11, 0x1C, 0x19, 0x1C, 0x19, 0x1C, 0x19
    .byte 0xC3, 0x18, 0xC3, 0x18, 0xC3, 0x18, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0x8E, 0x19
    .byte 0x8E, 0x19, 0xEB, 0x14, 0xCC, 0x18, 0xCC, 0x18, 0x66, 0x13, 0xF2, 0x17, 0x09, 0x14, 0x79, 0x19
    .byte 0x79, 0x19, 0x7C, 0x13, 0x57, 0x13, 0xA7, 0x16, 0x7D, 0x13, 0x4B, 0x18, 0x4B, 0x18, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Des Frog
@ GBA地址: 0x09E64B0E  ROM偏移: 0x1E64B0E
@ 42 张牌，融合卡组 1 张
@ -----------------------------------------------------------------------------
deck_des_frog:
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  4926    @ Mother Grizzly                                (密码: 57839750)
    deck_card  4926    @ Mother Grizzly                                (密码: 57839750)
    deck_card  4926    @ Mother Grizzly                                (密码: 57839750)
    deck_card  6425    @ T.A.D.P.O.L.E.                                (密码: 10456559)
    deck_card  6425    @ T.A.D.P.O.L.E.                                (密码: 10456559)
    deck_card  6425    @ T.A.D.P.O.L.E.                                (密码: 10456559)
    deck_card  6604    @ Beelze Frog                                   (密码: 49522489)
    deck_card  6604    @ Beelze Frog                                   (密码: 49522489)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  5411    @ Gora Turtle                                   (密码: 80233946)
    deck_card  6603    @ Treeborn Frog                                 (密码: 12538374)
    deck_card  6424    @ Des Frog                                      (密码: 84451804)
    deck_card  6424    @ Des Frog                                      (密码: 84451804)
    deck_card  6424    @ Des Frog                                      (密码: 84451804)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  4608    @ Penguin Soldier                               (密码: 93920745)
    deck_card  5803    @ Nightmare Penguin                             (密码: 81306586)
    deck_card  5803    @ Nightmare Penguin                             (密码: 81306586)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4933    @ Umiiruka                                      (密码: 82999629)
    deck_card  4933    @ Umiiruka                                      (密码: 82999629)
    deck_card  6137    @ Big Wave Small Wave                           (密码: 51562916)
    deck_card  5162    @ Creature Swap                                 (密码: 31036355)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  4803    @ Brain Control                                 (密码: 87910978)
    deck_card  6435    @ Des Croaking                                  (密码: 44883830)
    deck_card  6435    @ Des Croaking                                  (密码: 44883830)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  4354    @ Swords of Revealing Light                     (密码: 72302403)
    deck_card  4837    @ Polymerization                                (密码: 24094653)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  5114    @ Torrential Tribute                            (密码: 53582587)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  5908    @ Salvage                                       (密码: 96947648)
    deck_card  5908    @ Salvage                                       (密码: 96947648)
    deck_card     1    @ SO=0x0001                                     (密码: ?)
    deck_card  6614    @ D.3.S. Frog                                   (密码: 09910360)
    .hword 0    @ 卡组终止符
    @ 融合卡组（1 张）
    deck_card 52225    @ SO=0xCC01                                     (密码: ?)
    @ padding/其他数据（104 字节）
    .byte 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0xD6, 0x0F, 0x3E, 0x13, 0x3E, 0x13, 0x3E, 0x13
    .byte 0x19, 0x19, 0x19, 0x19, 0x19, 0x19, 0xCC, 0x19, 0xCC, 0x19, 0x27, 0x17, 0x27, 0x17, 0x23, 0x15
    .byte 0xCB, 0x19, 0x18, 0x19, 0x18, 0x19, 0x18, 0x19, 0x1C, 0x16, 0x00, 0x12, 0xAB, 0x16, 0xAB, 0x16
    .byte 0x52, 0x11, 0x45, 0x13, 0x45, 0x13, 0xF9, 0x17, 0x2A, 0x14, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0xC3, 0x12, 0x23, 0x19, 0x23, 0x19, 0x66, 0x13, 0xF2, 0x17, 0x02, 0x11, 0xE5, 0x12, 0x02, 0x13
    .byte 0xFA, 0x13, 0x7D, 0x13, 0x14, 0x17, 0x14, 0x17, 0x01, 0x00, 0xD6, 0x19, 0x00, 0x00, 0x01, 0xFC
    .byte 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Goblin King
@ GBA地址: 0x09E64BCE  ROM偏移: 0x1E64BCE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_goblin_king:
    deck_card  5301    @ Dark Ruler Ha Des                             (密码: 53982768)
    deck_card  5301    @ Dark Ruler Ha Des                             (密码: 53982768)
    deck_card  5222    @ Dark Necrofear                                (密码: 31829185)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  5037    @ Slate Warrior                                 (密码: 78636495)
    deck_card  5037    @ Slate Warrior                                 (密码: 78636495)
    deck_card  5762    @ Archfiend Soldier                             (密码: 49881766)
    deck_card  5762    @ Archfiend Soldier                             (密码: 49881766)
    deck_card  5762    @ Archfiend Soldier                             (密码: 49881766)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  4930    @ Mystic Tomato                                 (密码: 83011277)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  5323    @ Exiled Force                                  (密码: 74131780)
    deck_card  5973    @ Goblin King                                   (密码: 18590133)
    deck_card  5768    @ Great Maju Garzett                            (密码: 47942531)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  4341    @ Yami                                          (密码: 59197169)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5133    @ Magic Drain                                   (密码: 59344077)
    deck_card  5310    @ Bark of Dark Ruler                            (密码: 41925941)
    deck_card  5310    @ Bark of Dark Ruler                            (密码: 41925941)
    deck_card  5310    @ Bark of Dark Ruler                            (密码: 41925941)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（302 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0xB5, 0x14
    .byte 0xB5, 0x14, 0x66, 0x14, 0x12, 0x19, 0x12, 0x19, 0x12, 0x19, 0xAD, 0x13, 0xAD, 0x13, 0x82, 0x16
    .byte 0x82, 0x16, 0x82, 0x16, 0x57, 0x16, 0x42, 0x13, 0x39, 0x13, 0x39, 0x13, 0x39, 0x13, 0xD6, 0x0F
    .byte 0xCB, 0x14, 0x55, 0x17, 0x88, 0x16, 0x8D, 0x19, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0x11, 0x17, 0xEB, 0x14, 0xD2, 0x12, 0x29, 0x13, 0x66, 0x13, 0xF2, 0x17, 0xF5, 0x10, 0x7C, 0x13
    .byte 0x7C, 0x13, 0x0D, 0x14, 0xBE, 0x14, 0xBE, 0x14, 0xBE, 0x14, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0x92, 0x16
    .byte 0x92, 0x16, 0xB5, 0x14, 0x91, 0x16, 0x91, 0x16, 0x91, 0x16, 0x8D, 0x16, 0x8D, 0x16, 0x8D, 0x16
    .byte 0x82, 0x16, 0x82, 0x16, 0x8C, 0x16, 0x8C, 0x16, 0x8F, 0x16, 0x8F, 0x16, 0x90, 0x16, 0x90, 0x16
    .byte 0x8E, 0x16, 0x55, 0x17, 0x55, 0x17, 0xEC, 0x12, 0x2D, 0x13, 0x9B, 0x16, 0xD6, 0x10, 0xD6, 0x10
    .byte 0x66, 0x13, 0x9F, 0x16, 0x9F, 0x16, 0x9F, 0x16, 0x9A, 0x16, 0x9A, 0x16, 0xA2, 0x16, 0xA2, 0x16
    .byte 0xA4, 0x16, 0xBE, 0x14, 0xBE, 0x14, 0xBE, 0x14, 0x7D, 0x13, 0xC0, 0x14, 0x35, 0x16, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0x92, 0x16
    .byte 0x92, 0x16, 0xB5, 0x14, 0x91, 0x16, 0x91, 0x16, 0x91, 0x16, 0x8D, 0x16, 0x8D, 0x16, 0x8D, 0x16
    .byte 0x82, 0x16, 0x82, 0x16, 0x8C, 0x16, 0x8C, 0x16, 0x8F, 0x16, 0x8F, 0x16, 0x90, 0x16, 0x90, 0x16
    .byte 0x8E, 0x16, 0x55, 0x17, 0x55, 0x17, 0xEC, 0x12, 0x2D, 0x13, 0x9B, 0x16, 0xD6, 0x10, 0xD6, 0x10
    .byte 0x66, 0x13, 0x9F, 0x16, 0x9F, 0x16, 0x9F, 0x16, 0x9A, 0x16, 0x9A, 0x16, 0xA2, 0x16, 0xA2, 0x16
    .byte 0xA4, 0x16, 0xBE, 0x14, 0xBE, 0x14, 0xBE, 0x14, 0x7D, 0x13, 0xC0, 0x14, 0x35, 0x16, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Ojama Yellow
@ GBA地址: 0x09E64D4E  ROM偏移: 0x1E64D4E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_ojama_yellow:
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  4930    @ Mystic Tomato                                 (密码: 83011277)
    deck_card  4930    @ Mystic Tomato                                 (密码: 83011277)
    deck_card  5687    @ Bowganian                                     (密码: 52090844)
    deck_card  5687    @ Bowganian                                     (密码: 52090844)
    deck_card  6429    @ Ebon Magician Curran                          (密码: 46128076)
    deck_card  6429    @ Ebon Magician Curran                          (密码: 46128076)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  5260    @ Maryokutai                                    (密码: 71466592)
    deck_card  4108    @ Mask of Darkness                              (密码: 28933734)
    deck_card  5882    @ Stealth Bird                                  (密码: 03510565)
    deck_card  5882    @ Stealth Bird                                  (密码: 03510565)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  5520    @ A Cat of Ill Omen                             (密码: 24140059)
    deck_card  6202    @ A-Team: Trap Disposal Unit                    (密码: 13026402)
    deck_card  5811    @ Ojama Yellow                                  (密码: 42941100)
    deck_card  5531    @ Dark Room of Nightmare                        (密码: 85562745)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5170    @ Ground Collapse                               (密码: 90502999)
    deck_card  5170    @ Ground Collapse                               (密码: 90502999)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  5855    @ Spatial Collapse                              (密码: 20644748)
    deck_card  5855    @ Spatial Collapse                              (密码: 20644748)
    deck_card  5738    @ Ojama Trio                                    (密码: 29843091)
    deck_card  5738    @ Ojama Trio                                    (密码: 29843091)
    deck_card  5738    @ Ojama Trio                                    (密码: 29843091)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  6218    @ Xing Zhen Hu                                  (密码: 76515293)
    deck_card  6218    @ Xing Zhen Hu                                  (密码: 76515293)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0x56, 0x17
    .byte 0x56, 0x17, 0x42, 0x13, 0x42, 0x13, 0x37, 0x16, 0x37, 0x16, 0x1D, 0x19, 0x1D, 0x19, 0xD6, 0x0F
    .byte 0x8C, 0x14, 0x0C, 0x10, 0xFA, 0x16, 0xFA, 0x16, 0x90, 0x15, 0x90, 0x15, 0x90, 0x15, 0x3A, 0x18
    .byte 0xB3, 0x16, 0x9B, 0x15, 0x8D, 0x19, 0xEC, 0x12, 0x2D, 0x13, 0x32, 0x14, 0x32, 0x14, 0xD2, 0x12
    .byte 0xF2, 0x17, 0x61, 0x14, 0xA6, 0x17, 0xA6, 0x17, 0xDF, 0x16, 0xDF, 0x16, 0x6A, 0x16, 0x6A, 0x16
    .byte 0x6A, 0x16, 0x0E, 0x14, 0x0E, 0x14, 0x7C, 0x13, 0x7C, 0x13, 0x4A, 0x18, 0x4A, 0x18, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Water Dragon
@ GBA地址: 0x09E64E0E  ROM偏移: 0x1E64E0E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_water_dragon:
    deck_card  6481    @ Water Dragon                                  (密码: 85066822)
    deck_card  5895    @ Levia-Dragon - Daedalus                       (密码: 37721209)
    deck_card  5871    @ Giga Gagagigo                                 (密码: 43793530)
    deck_card  5871    @ Giga Gagagigo                                 (密码: 43793530)
    deck_card  5759    @ Gagagigo                                      (密码: 49003308)
    deck_card  5874    @ Sea Serpent Warrior of Darkness               (密码: 42071342)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  6480    @ Oxygeddon                                     (密码: 58071123)
    deck_card  6480    @ Oxygeddon                                     (密码: 58071123)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  6479    @ Hydrogeddon                                   (密码: 22587018)
    deck_card  6479    @ Hydrogeddon                                   (密码: 22587018)
    deck_card  6479    @ Hydrogeddon                                   (密码: 22587018)
    deck_card  6120    @ Unshaven Angler                               (密码: 92084010)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5803    @ Nightmare Penguin                             (密码: 81306586)
    deck_card  4608    @ Penguin Soldier                               (密码: 93920745)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  6492    @ Bonding - H2O                                 (密码: 45898858)
    deck_card  6492    @ Bonding - H2O                                 (密码: 45898858)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  4861    @ Solemn Judgment                               (密码: 41420027)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4863    @ Seven Tools of the Bandit                     (密码: 03819470)
    deck_card  5111    @ Tornado Wall                                  (密码: 18605135)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x51, 0x19
    .byte 0x07, 0x17, 0xEF, 0x16, 0xEF, 0x16, 0x7F, 0x16, 0xF2, 0x16, 0x27, 0x17, 0x27, 0x17, 0x50, 0x19
    .byte 0x50, 0x19, 0x2C, 0x17, 0x1C, 0x16, 0x4F, 0x19, 0x4F, 0x19, 0x4F, 0x19, 0xE8, 0x17, 0x57, 0x16
    .byte 0xAB, 0x16, 0x00, 0x12, 0x52, 0x11, 0x8D, 0x19, 0x8D, 0x19, 0x1B, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0x0B, 0x15, 0x0B, 0x15, 0x0B, 0x15, 0x66, 0x13, 0xF2, 0x17, 0x5C, 0x19, 0x5C, 0x19, 0x61, 0x14
    .byte 0xFD, 0x12, 0x7C, 0x13, 0xFF, 0x12, 0xF7, 0x13, 0x18, 0x15, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Red Eyes Darkness Dragon
@ GBA地址: 0x09E64ECE  ROM偏移: 0x1E64ECE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_red_eyes_darkness_dragon:
    deck_card  6540    @ Armed Dragon LV10                             (密码: 59464593)
    deck_card  6107    @ Armed Dragon LV7                              (密码: 73879377)
    deck_card  6106    @ Armed Dragon LV5                              (密码: 46384672)
    deck_card  6106    @ Armed Dragon LV5                              (密码: 46384672)
    deck_card  6292    @ Red-Eyes Darkness Dragon                      (密码: 96561011)
    deck_card  6547    @ Axe Dragonute                                 (密码: 84914462)
    deck_card  6547    @ Axe Dragonute                                 (密码: 84914462)
    deck_card  5644    @ Luster Dragon                                 (密码: 11091375)
    deck_card  5644    @ Luster Dragon                                 (密码: 11091375)
    deck_card  5644    @ Luster Dragon                                 (密码: 11091375)
    deck_card  5030    @ Twin-Headed Behemoth                          (密码: 43586926)
    deck_card  6115    @ Element Dragon                                (密码: 30314994)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  6118    @ Masked Dragon                                 (密码: 39191307)
    deck_card  6118    @ Masked Dragon                                 (密码: 39191307)
    deck_card  6105    @ Armed Dragon LV3                              (密码: 00980973)
    deck_card  6105    @ Armed Dragon LV3                              (密码: 00980973)
    deck_card  5323    @ Exiled Force                                  (密码: 74131780)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6109    @ Red-Eyes B. Chick                             (密码: 36262024)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  5345    @ Stamping Destruction                          (密码: 81385346)
    deck_card  5345    @ Stamping Destruction                          (密码: 81385346)
    deck_card  5345    @ Stamping Destruction                          (密码: 81385346)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  6135    @ The Graveyard in the Fourth Dimension         (密码: 88089103)
    deck_card  4956    @ Ceasefire                                     (密码: 36468556)
    deck_card  5342    @ The Dragon's Bead                             (密码: 92408984)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  5347    @ Dragon's Rage                                 (密码: 54178050)
    deck_card  5347    @ Dragon's Rage                                 (密码: 54178050)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x8C, 0x19
    .byte 0xDB, 0x17, 0xDA, 0x17, 0xDA, 0x17, 0x94, 0x18, 0x93, 0x19, 0x93, 0x19, 0x0C, 0x16, 0x0C, 0x16
    .byte 0x0C, 0x16, 0xA6, 0x13, 0xE3, 0x17, 0x57, 0x16, 0xE6, 0x17, 0xE6, 0x17, 0xD9, 0x17, 0xD9, 0x17
    .byte 0xCB, 0x14, 0xD6, 0x0F, 0xDD, 0x17, 0x8D, 0x19, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0xD2, 0x12, 0xE1, 0x14, 0xE1, 0x14, 0xE1, 0x14, 0x29, 0x13, 0x66, 0x13, 0x63, 0x13, 0xF7, 0x17
    .byte 0x5C, 0x13, 0xDE, 0x14, 0x18, 0x15, 0xA7, 0x16, 0x7D, 0x13, 0xE3, 0x14, 0xE3, 0x14, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Ocean Dragon Lord Neo D
@ GBA地址: 0x09E64F8E  ROM偏移: 0x1E64F8E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_ocean_dragon_lord_neo_d:
    deck_card  6376    @ Ocean Dragon Lord - Neo-Daedalus              (密码: 10485110)
    deck_card  5895    @ Levia-Dragon - Daedalus                       (密码: 37721209)
    deck_card  5871    @ Giga Gagagigo                                 (密码: 43793530)
    deck_card  5871    @ Giga Gagagigo                                 (密码: 43793530)
    deck_card  6114    @ Mobius the Frost Monarch                      (密码: 04929256)
    deck_card  5759    @ Gagagigo                                      (密码: 49003308)
    deck_card  5759    @ Gagagigo                                      (密码: 49003308)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  5927    @ Abyss Soldier                                 (密码: 18318842)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  6120    @ Unshaven Angler                               (密码: 92084010)
    deck_card  6120    @ Unshaven Angler                               (密码: 92084010)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5967    @ Mermaid Knight                                (密码: 24435369)
    deck_card  5967    @ Mermaid Knight                                (密码: 24435369)
    deck_card  5830    @ Fenrir                                        (密码: 00218704)
    deck_card  4926    @ Mother Grizzly                                (密码: 57839750)
    deck_card  4926    @ Mother Grizzly                                (密码: 57839750)
    deck_card  5803    @ Nightmare Penguin                             (密码: 81306586)
    deck_card  4608    @ Penguin Soldier                               (密码: 93920745)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  6137    @ Big Wave Small Wave                           (密码: 51562916)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5908    @ Salvage                                       (密码: 96947648)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  5387    @ A Legendary Ocean                             (密码: 00295517)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5114    @ Torrential Tribute                            (密码: 53582587)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5111    @ Tornado Wall                                  (密码: 18605135)
    deck_card  5111    @ Tornado Wall                                  (密码: 18605135)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0xE8, 0x18
    .byte 0x07, 0x17, 0xEF, 0x16, 0xEF, 0x16, 0xE2, 0x17, 0x7F, 0x16, 0x7F, 0x16, 0x27, 0x17, 0x27, 0x17
    .byte 0x1C, 0x16, 0xE8, 0x17, 0xE8, 0x17, 0x57, 0x16, 0x4F, 0x17, 0x4F, 0x17, 0xC6, 0x16, 0x3E, 0x13
    .byte 0x3E, 0x13, 0xAB, 0x16, 0x00, 0x12, 0x52, 0x11, 0x1B, 0x13, 0xF9, 0x17, 0x22, 0x13, 0xEC, 0x12
    .byte 0x2D, 0x13, 0x14, 0x17, 0x11, 0x17, 0x0B, 0x15, 0x0B, 0x15, 0x0B, 0x15, 0x66, 0x13, 0x0E, 0x14
    .byte 0x0E, 0x14, 0xFA, 0x13, 0x7C, 0x13, 0xF7, 0x13, 0xF7, 0x13, 0x18, 0x15, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Infernal Flame Emperor
@ GBA地址: 0x09E6504E  ROM偏移: 0x1E6504E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_infernal_flame_emperor:
    deck_card  5496    @ Lava Golem                                    (密码: 00102380)
    deck_card  5496    @ Lava Golem                                    (密码: 00102380)
    deck_card  6368    @ Infernal Flame Emperor                        (密码: 19847532)
    deck_card  6197    @ Gaia Soul the Combustible Collective          (密码: 51355346)
    deck_card  5876    @ Blazing Inpachi                               (密码: 05464695)
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  4917    @ UFO Turtle                                    (密码: 60806437)
    deck_card  4917    @ UFO Turtle                                    (密码: 60806437)
    deck_card  6193    @ Invasion of Flames                            (密码: 26082229)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6113    @ Ultimate Baseball Kid                         (密码: 67934141)
    deck_card  6113    @ Ultimate Baseball Kid                         (密码: 67934141)
    deck_card  6198    @ Fox Fire                                      (密码: 88753985)
    deck_card  6198    @ Fox Fire                                      (密码: 88753985)
    deck_card  6093    @ Charcoal Inpachi                              (密码: 13179332)
    deck_card  6189    @ Raging Flame Sprite                           (密码: 90810762)
    deck_card  6189    @ Raging Flame Sprite                           (密码: 90810762)
    deck_card  6189    @ Raging Flame Sprite                           (密码: 90810762)
    deck_card  5531    @ Dark Room of Nightmare                        (密码: 85562745)
    deck_card  5531    @ Dark Room of Nightmare                        (密码: 85562745)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  6054    @ Level Limit - Area B                          (密码: 03136426)
    deck_card  4861    @ Solemn Judgment                               (密码: 41420027)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5134    @ Gravity Bind                                  (密码: 85742772)
    deck_card  5298    @ Nightmare Wheel                               (密码: 54704216)
    deck_card  5298    @ Nightmare Wheel                               (密码: 54704216)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x78, 0x15
    .byte 0x78, 0x15, 0xE0, 0x18, 0x35, 0x18, 0xF4, 0x16, 0x56, 0x17, 0x56, 0x17, 0x56, 0x17, 0x35, 0x13
    .byte 0x35, 0x13, 0x31, 0x18, 0xD6, 0x0F, 0xE1, 0x17, 0xE1, 0x17, 0x36, 0x18, 0x36, 0x18, 0xCD, 0x17
    .byte 0x2D, 0x18, 0x2D, 0x18, 0x2D, 0x18, 0x9B, 0x15, 0x9B, 0x15, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12
    .byte 0x2D, 0x13, 0x11, 0x17, 0x66, 0x13, 0x63, 0x13, 0xA6, 0x17, 0xA6, 0x17, 0xFD, 0x12, 0x0E, 0x14
    .byte 0x0E, 0x14, 0xB2, 0x14, 0xB2, 0x14, 0x7C, 0x13, 0x7C, 0x13, 0x18, 0x15, 0x18, 0x15, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Helios Duo Megiste
@ GBA地址: 0x09E6510E  ROM偏移: 0x1E6510E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_helios_duo_megiste:
    deck_card  6332    @ D.D. Survivor                                 (密码: 48092532)
    deck_card  6332    @ D.D. Survivor                                 (密码: 48092532)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  6645    @ Homunculus Gold                               (密码: 27408609)
    deck_card  6645    @ Homunculus Gold                               (密码: 27408609)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  4262    @ Dimensional Warrior                           (密码: 37043180)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  5597    @ Dimension Jar                                 (密码: 73414375)
    deck_card  4914    @ Banisher of the Light                         (密码: 61528025)
    deck_card  4914    @ Banisher of the Light                         (密码: 61528025)
    deck_card  4914    @ Banisher of the Light                         (密码: 61528025)
    deck_card  5834    @ Gren Maju Da Eiza                             (密码: 36584821)
    deck_card  5834    @ Gren Maju Da Eiza                             (密码: 36584821)
    deck_card  6647    @ Helios Duo Megiste                            (密码: 80887952)
    deck_card  6647    @ Helios Duo Megiste                            (密码: 80887952)
    deck_card  6648    @ Helios Tris Megiste                           (密码: 17286057)
    deck_card  6646    @ The Ancient Sun Helios                        (密码: 54493213)
    deck_card  6646    @ The Ancient Sun Helios                        (密码: 54493213)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  4857    @ Soul Release                                  (密码: 05758500)
    deck_card  4857    @ Soul Release                                  (密码: 05758500)
    deck_card  4821    @ Card Destruction                              (密码: 72892473)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  6619    @ Karma Cut                                     (密码: 71587526)
    deck_card  6619    @ Karma Cut                                     (密码: 71587526)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5851    @ Big Burn                                      (密码: 95472621)
    deck_card  5405    @ Fiend Comedian                                (密码: 81172176)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0xBC, 0x18
    .byte 0xBC, 0x18, 0x2C, 0x17, 0x2C, 0x17, 0xF5, 0x19, 0xF5, 0x19, 0x57, 0x16, 0xA6, 0x10, 0x52, 0x11
    .byte 0xDD, 0x15, 0x32, 0x13, 0x32, 0x13, 0x32, 0x13, 0xCA, 0x16, 0xCA, 0x16, 0xF7, 0x19, 0xF7, 0x19
    .byte 0xF8, 0x19, 0xF6, 0x19, 0xF6, 0x19, 0x1B, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0xEB, 0x14, 0xF9, 0x12
    .byte 0xF9, 0x12, 0xD5, 0x12, 0x63, 0x13, 0x63, 0x13, 0x61, 0x14, 0xDB, 0x19, 0xDB, 0x19, 0x7C, 0x13
    .byte 0x7C, 0x13, 0xDB, 0x16, 0x1D, 0x15, 0x18, 0x15, 0x18, 0x15, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Vampire Genesis
@ GBA地址: 0x09E651CE  ROM偏移: 0x1E651CE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_vampire_genesis:
    deck_card  6293    @ Vampire Genesis                               (密码: 22056710)
    deck_card  5902    @ Ryu Kokki                                     (密码: 57281778)
    deck_card  5902    @ Ryu Kokki                                     (密码: 57281778)
    deck_card  5410    @ Vampire Lord                                  (密码: 53839837)
    deck_card  5410    @ Vampire Lord                                  (密码: 53839837)
    deck_card  6287    @ Curse of Vampire                              (密码: 34294855)
    deck_card  6041    @ Regenerating Mummy                            (密码: 70821187)
    deck_card  6041    @ Regenerating Mummy                            (密码: 70821187)
    deck_card  6041    @ Regenerating Mummy                            (密码: 70821187)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  5561    @ Goblin Zombie                                 (密码: 63665875)
    deck_card  5561    @ Goblin Zombie                                 (密码: 63665875)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  5956    @ Soul-Absorbing Bone Tower                     (密码: 63012333)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  6291    @ Overpowering Eye                              (密码: 60577362)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5123    @ Card of Safe Return                           (密码: 57953380)
    deck_card  5430    @ Book of Life                                  (密码: 02204140)
    deck_card  5430    @ Book of Life                                  (密码: 02204140)
    deck_card  5430    @ Book of Life                                  (密码: 02204140)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  5435    @ Call of the Mummy                             (密码: 04861205)
    deck_card  5435    @ Call of the Mummy                             (密码: 04861205)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  5114    @ Torrential Tribute                            (密码: 53582587)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x95, 0x18
    .byte 0x0E, 0x17, 0x0E, 0x17, 0x22, 0x15, 0x22, 0x15, 0x8F, 0x18, 0x99, 0x17, 0x99, 0x17, 0x99, 0x17
    .byte 0x1C, 0x16, 0x57, 0x16, 0x2F, 0x15, 0x2F, 0x15, 0x2F, 0x15, 0xB9, 0x15, 0xB9, 0x15, 0xD6, 0x0F
    .byte 0x44, 0x17, 0x52, 0x11, 0x96, 0x15, 0x96, 0x15, 0x96, 0x15, 0x93, 0x18, 0x1B, 0x13, 0x22, 0x13
    .byte 0xEC, 0x12, 0x2D, 0x13, 0x03, 0x14, 0x36, 0x15, 0x36, 0x15, 0x36, 0x15, 0x29, 0x13, 0x63, 0x13
    .byte 0x3B, 0x15, 0x3B, 0x15, 0x61, 0x14, 0xFA, 0x13, 0x7C, 0x13, 0x18, 0x15, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Elemental Hero Electrum
@ GBA地址: 0x09E6528E  ROM偏移: 0x1E6528E
@ 50 张牌，融合卡组 9 张
@ -----------------------------------------------------------------------------
deck_elemental_hero_electrum:
    deck_card  6477    @ Elemental Hero Bladedge                       (密码: 59793705)
    deck_card  6477    @ Elemental Hero Bladedge                       (密码: 59793705)
    deck_card  6313    @ Elemental Hero Sparkman                       (密码: 20721928)
    deck_card  6313    @ Elemental Hero Sparkman                       (密码: 20721928)
    deck_card  6478    @ Elemental Hero Wildheart                      (密码: 86188410)
    deck_card  6478    @ Elemental Hero Wildheart                      (密码: 86188410)
    deck_card  6311    @ Elemental Hero Burstinatrix                   (密码: 58932615)
    deck_card  6311    @ Elemental Hero Burstinatrix                   (密码: 58932615)
    deck_card  6310    @ Elemental Hero Avian                          (密码: 21844576)
    deck_card  6310    @ Elemental Hero Avian                          (密码: 21844576)
    deck_card  6393    @ Elemental Hero Bubbleman                      (密码: 79979666)
    deck_card  6393    @ Elemental Hero Bubbleman                      (密码: 79979666)
    deck_card  6312    @ Elemental Hero Clayman                        (密码: 84327329)
    deck_card  6312    @ Elemental Hero Clayman                        (密码: 84327329)
    deck_card  6391    @ Wroughtweiler                                 (密码: 06480253)
    deck_card  6391    @ Wroughtweiler                                 (密码: 06480253)
    deck_card  6044    @ King of the Swamp                             (密码: 79109599)
    deck_card  6044    @ King of the Swamp                             (密码: 79109599)
    deck_card  6044    @ King of the Swamp                             (密码: 79109599)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5330    @ The Warrior Returning Alive                   (密码: 95281259)
    deck_card  5328    @ Reinforcement of the Army                     (密码: 32807846)
    deck_card  5328    @ Reinforcement of the Army                     (密码: 32807846)
    deck_card  6431    @ Fusion Recovery                               (密码: 18511384)
    deck_card  6431    @ Fusion Recovery                               (密码: 18511384)
    deck_card  6399    @ Skyscraper                                    (密码: 63035430)
    deck_card  6399    @ Skyscraper                                    (密码: 63035430)
    deck_card  6432    @ Miracle Fusion                                (密码: 45906428)
    deck_card  6432    @ Miracle Fusion                                (密码: 45906428)
    deck_card  4837    @ Polymerization                                (密码: 24094653)
    deck_card  4837    @ Polymerization                                (密码: 24094653)
    deck_card  4837    @ Polymerization                                (密码: 24094653)
    deck_card  5118    @ De-Fusion                                     (密码: 95286165)
    deck_card  5915    @ A Hero Emerges                                (密码: 21597117)
    deck_card  6356    @ Hero Signal                                   (密码: 22020907)
    deck_card  6495    @ Hero Barrier                                  (密码: 44676200)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  6528    @ Hero Heyro                                    (密码: 26647858)
    deck_card     9    @ SO=0x0009                                     (密码: ?)
    deck_card  6639    @ Elemental Hero Erikshieler                    (密码: 29343734)
    deck_card  6487    @ Elemental Hero Tempest                        (密码: 83121692)
    deck_card  6488    @ Elemental Hero Wildedge                       (密码: 10526791)
    deck_card  6467    @ Elemental Hero Shining Flare Wingman          (密码: 25366484)
    deck_card  6345    @ Elemental Hero Thunder Giant                  (密码: 61204971)
    deck_card  6344    @ Elemental Hero Flame Wingman                  (密码: 35809262)
    deck_card  6486    @ Elemental Hero Rampart Blaster                (密码: 47737087)
    deck_card  6529    @ Elemental Hero Madballman                     (密码: 52031567)
    deck_card  6535    @ Elemental Hero Steam Healer                   (密码: 81197327)
    .hword 0    @ 卡组终止符
    @ 融合卡组（9 张）
    deck_card 52225    @ SO=0xCC01                                     (密码: ?)
    deck_card 52428    @ SO=0xCCCC                                     (密码: ?)
    deck_card  8575    @ SO=0x217F                                     (密码: ?)
    deck_card 16759    @ SO=0x4177                                     (密码: ?)
    deck_card    40    @ SO=0x0028                                     (密码: ?)
    deck_card  6477    @ Elemental Hero Bladedge                       (密码: 59793705)
    deck_card  6477    @ Elemental Hero Bladedge                       (密码: 59793705)
    deck_card  6313    @ Elemental Hero Sparkman                       (密码: 20721928)
    deck_card  6313    @ Elemental Hero Sparkman                       (密码: 20721928)
    @ padding/其他数据（104 字节）
    .byte 0x4E, 0x19, 0x4E, 0x19, 0xA7, 0x18, 0xA7, 0x18, 0xA6, 0x18, 0xA6, 0x18, 0xF9, 0x18, 0xF9, 0x18
    .byte 0xA8, 0x18, 0xA8, 0x18, 0xF7, 0x18, 0xF7, 0x18, 0x9C, 0x17, 0x9C, 0x17, 0x9C, 0x17, 0xEC, 0x12
    .byte 0x2D, 0x13, 0xD2, 0x14, 0xD0, 0x14, 0xD0, 0x14, 0x1F, 0x19, 0x1F, 0x19, 0xFF, 0x18, 0xFF, 0x18
    .byte 0x20, 0x19, 0x20, 0x19, 0xE5, 0x12, 0xE5, 0x12, 0xE5, 0x12, 0xFE, 0x13, 0x1B, 0x17, 0xD4, 0x18
    .byte 0x5F, 0x19, 0x7D, 0x13, 0x02, 0x13, 0x80, 0x19, 0x09, 0x00, 0xEF, 0x19, 0x57, 0x19, 0x58, 0x19
    .byte 0x43, 0x19, 0xC9, 0x18, 0xC8, 0x18, 0x56, 0x19, 0x81, 0x19, 0x87, 0x19, 0x00, 0x00, 0x01, 0xFC
    .byte 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Goldd Wu-Lord of Dark
@ GBA地址: 0x09E6536E  ROM偏移: 0x1E6536E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_goldd_wu_lord_of_dark:
    deck_card  6505    @ Goldd, Wu-Lord of Dark World                  (密码: 78004197)
    deck_card  6505    @ Goldd, Wu-Lord of Dark World                  (密码: 78004197)
    deck_card  6505    @ Goldd, Wu-Lord of Dark World                  (密码: 78004197)
    deck_card  6504    @ Sillva, Warlord of Dark World                 (密码: 32619583)
    deck_card  6504    @ Sillva, Warlord of Dark World                 (密码: 32619583)
    deck_card  6504    @ Sillva, Warlord of Dark World                 (密码: 32619583)
    deck_card  6503    @ Brron, Mad King of Dark World                 (密码: 06214884)
    deck_card  6503    @ Brron, Mad King of Dark World                 (密码: 06214884)
    deck_card  6503    @ Brron, Mad King of Dark World                 (密码: 06214884)
    deck_card  6497    @ Zure, Knight of Dark World                    (密码: 07459013)
    deck_card  6497    @ Zure, Knight of Dark World                    (密码: 07459013)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  6501    @ Beiige, Vanguard of Dark World                (密码: 33731070)
    deck_card  6501    @ Beiige, Vanguard of Dark World                (密码: 33731070)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  6502    @ Broww, Huntsman of Dark World                 (密码: 79126789)
    deck_card  4597    @ Morphing Jar                                  (密码: 33508719)
    deck_card  6506    @ Scarr, Scout of Dark World                    (密码: 05498296)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6515    @ Gateway to Dark World                         (密码: 93431518)
    deck_card  6515    @ Gateway to Dark World                         (密码: 93431518)
    deck_card  6512    @ Dark World Lightning                          (密码: 93554166)
    deck_card  6512    @ Dark World Lightning                          (密码: 93554166)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  5123    @ Card of Safe Return                           (密码: 57953380)
    deck_card  4821    @ Card Destruction                              (密码: 72892473)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  6516    @ The Forces of Darkness                        (密码: 29826127)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5544    @ Raigeki Break                                 (密码: 04178474)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  6517    @ Dark Deal                                     (密码: 65824822)
    deck_card  6517    @ Dark Deal                                     (密码: 65824822)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x69, 0x19
    .byte 0x69, 0x19, 0x69, 0x19, 0x68, 0x19, 0x68, 0x19, 0x68, 0x19, 0x67, 0x19, 0x67, 0x19, 0x67, 0x19
    .byte 0x61, 0x19, 0x61, 0x19, 0x1C, 0x16, 0x65, 0x19, 0x65, 0x19, 0x57, 0x16, 0x66, 0x19, 0xF5, 0x11
    .byte 0x6A, 0x19, 0x52, 0x11, 0x73, 0x19, 0x73, 0x19, 0x70, 0x19, 0x70, 0x19, 0x8D, 0x19, 0x1B, 0x13
    .byte 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0xEB, 0x14, 0x03, 0x14, 0xD5, 0x12, 0x61, 0x14, 0x74, 0x19
    .byte 0x7C, 0x13, 0xA8, 0x15, 0x18, 0x15, 0x75, 0x19, 0x75, 0x19, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Guardian Exode
@ GBA地址: 0x09E6542E  ROM偏移: 0x1E6542E
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_guardian_exode:
    deck_card  6239    @ Granmarg the Rock Monarch                     (密码: 60229110)
    deck_card  6321    @ Hieracosphinx                                 (密码: 82260502)
    deck_card  5422    @ Guardian Sphinx                               (密码: 40659562)
    deck_card  6326    @ Grave Ohja                                    (密码: 40937767)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  6322    @ Criosphinx                                    (密码: 18654201)
    deck_card  6323    @ Moai Interceptor Cannons                      (密码: 45159319)
    deck_card  6323    @ Moai Interceptor Cannons                      (密码: 45159319)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6610    @ Sand Moth                                     (密码: 73648243)
    deck_card  4913    @ Cyber Jar                                     (密码: 34124316)
    deck_card  6254    @ Golem Sentry                                  (密码: 52323207)
    deck_card  6254    @ Golem Sentry                                  (密码: 52323207)
    deck_card  4754    @ Stone Statue of the Aztecs                    (密码: 31812496)
    deck_card  4754    @ Stone Statue of the Aztecs                    (密码: 31812496)
    deck_card  4754    @ Stone Statue of the Aztecs                    (密码: 31812496)
    deck_card  6320    @ Lost Guardian                                 (密码: 45871897)
    deck_card  6640    @ Guardian Exode                                (密码: 55737443)
    deck_card  6324    @ Megarock Dragon                               (密码: 71544954)
    deck_card  4965    @ The Shallow Grave                             (密码: 43434803)
    deck_card  4965    @ The Shallow Grave                             (密码: 43434803)
    deck_card  6354    @ Shifting Shadows                              (密码: 59237154)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  5755    @ Unity                                         (密码: 14731897)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  6642    @ Fault Zone                                    (密码: 28120197)
    deck_card  6642    @ Fault Zone                                    (密码: 28120197)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4811    @ Shield & Sword                                (密码: 52097679)
    deck_card  6362    @ Rock Bombardment                              (密码: 20781762)
    deck_card  6362    @ Rock Bombardment                              (密码: 20781762)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5737    @ Staunch Defender                              (密码: 92854392)
    deck_card  5737    @ Staunch Defender                              (密码: 92854392)
    deck_card  5113    @ Fairy Box                                     (密码: 21598948)
    deck_card  5113    @ Fairy Box                                     (密码: 21598948)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x5F, 0x18
    .byte 0xB1, 0x18, 0x2E, 0x15, 0xB6, 0x18, 0x57, 0x16, 0xB2, 0x18, 0xB3, 0x18, 0xB3, 0x18, 0xD6, 0x0F
    .byte 0xD2, 0x19, 0x31, 0x13, 0x6E, 0x18, 0x6E, 0x18, 0x92, 0x12, 0x92, 0x12, 0x92, 0x12, 0xB0, 0x18
    .byte 0xF0, 0x19, 0xB4, 0x18, 0x65, 0x13, 0x65, 0x13, 0xD2, 0x18, 0x1B, 0x13, 0x7B, 0x16, 0xEC, 0x12
    .byte 0x2D, 0x13, 0xEB, 0x14, 0xEB, 0x14, 0xF2, 0x19, 0xF2, 0x19, 0x66, 0x13, 0xCB, 0x12, 0xDA, 0x18
    .byte 0xDA, 0x18, 0x7C, 0x13, 0x69, 0x16, 0x69, 0x16, 0xF9, 0x13, 0xF9, 0x13, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Gilford the Legend
@ GBA地址: 0x09E654EE  ROM偏移: 0x1E654EE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_gilford_the_legend:
    deck_card  6456    @ Gilford the Legend                            (密码: 69933858)
    deck_card  5145    @ Goblin Attack Force                           (密码: 78658564)
    deck_card  5145    @ Goblin Attack Force                           (密码: 78658564)
    deck_card  6164    @ Silent Swordsman LV5                          (密码: 74388798)
    deck_card  5245    @ Zombyra the Dark                              (密码: 88472456)
    deck_card  6111    @ Ninja Grandmaster Sasuke                      (密码: 04041838)
    deck_card  6111    @ Ninja Grandmaster Sasuke                      (密码: 04041838)
    deck_card  6111    @ Ninja Grandmaster Sasuke                      (密码: 04041838)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5898    @ Mataza the Zapper                             (密码: 22609617)
    deck_card  5017    @ Command Knight                                (密码: 10375182)
    deck_card  5318    @ Marauding Captain                             (密码: 02460565)
    deck_card  5318    @ Marauding Captain                             (密码: 02460565)
    deck_card  5318    @ Marauding Captain                             (密码: 02460565)
    deck_card  5323    @ Exiled Force                                  (密码: 74131780)
    deck_card  6162    @ Silent Swordsman LV3                          (密码: 01995985)
    deck_card  6162    @ Silent Swordsman LV3                          (密码: 01995985)
    deck_card  6252    @ Armed Samurai - Ben Kei                       (密码: 84430950)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  6458    @ Divine Sword - Phoenix Blade                  (密码: 31423101)
    deck_card  5330    @ The Warrior Returning Alive                   (密码: 95281259)
    deck_card  5328    @ Reinforcement of the Army                     (密码: 32807846)
    deck_card  5328    @ Reinforcement of the Army                     (密码: 32807846)
    deck_card  5212    @ United We Stand                               (密码: 56747793)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  5727    @ Wicked-Breaking Flamberge - Baou              (密码: 68427465)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4910    @ Giant Trunade                                 (密码: 42703248)
    deck_card  5213    @ Mage Power                                    (密码: 83746708)
    deck_card  5388    @ Fusion Sword Murasame Blade                   (密码: 37684215)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  5327    @ The A. Forces                                 (密码: 00403847)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x38, 0x19
    .byte 0x19, 0x14, 0x19, 0x14, 0x14, 0x18, 0x7D, 0x14, 0xDF, 0x17, 0xDF, 0x17, 0xDF, 0x17, 0x2C, 0x17
    .byte 0x2C, 0x17, 0x57, 0x16, 0x0A, 0x17, 0x99, 0x13, 0xC6, 0x14, 0xC6, 0x14, 0xC6, 0x14, 0xCB, 0x14
    .byte 0x12, 0x18, 0x12, 0x18, 0x6C, 0x18, 0x1B, 0x13, 0x22, 0x13, 0x2D, 0x13, 0x11, 0x17, 0x3A, 0x19
    .byte 0xD2, 0x14, 0xD0, 0x14, 0xD0, 0x14, 0x5C, 0x14, 0x29, 0x13, 0x5F, 0x16, 0x66, 0x13, 0x2E, 0x13
    .byte 0x5D, 0x14, 0x0C, 0x15, 0x61, 0x14, 0xCF, 0x14, 0x02, 0x13, 0x02, 0x13, 0x7C, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Dark Eradicator Warlock
@ GBA地址: 0x09E655AE  ROM偏移: 0x1E655AE
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_dark_eradicator_warlock:
    deck_card  6530    @ Dark Eradicator Warlock                       (密码: 29436665)
    deck_card  4041    @ Dark Magician                                 (密码: 46986414)
    deck_card  5833    @ Chaos Sorcerer                                (密码: 09596126)
    deck_card  5833    @ Chaos Sorcerer                                (密码: 09596126)
    deck_card  5649    @ Skilled Dark Magician                         (密码: 73752131)
    deck_card  5649    @ Skilled Dark Magician                         (密码: 73752131)
    deck_card  5649    @ Skilled Dark Magician                         (密码: 73752131)
    deck_card  5476    @ Toon Gemini Elf                               (密码: 42386471)
    deck_card  5248    @ Kycoo the Ghost Destroyer                     (密码: 88240808)
    deck_card  5248    @ Kycoo the Ghost Destroyer                     (密码: 88240808)
    deck_card  5869    @ Magician's Valkyrie                           (密码: 80304126)
    deck_card  5655    @ Breaker the Magical Warrior                   (密码: 71413901)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5323    @ Exiled Force                                  (密码: 74131780)
    deck_card  5650    @ Apprentice Magician                           (密码: 09156135)
    deck_card  5650    @ Apprentice Magician                           (密码: 09156135)
    deck_card  5031    @ Injection Fairy Lily                          (密码: 79575620)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  5658    @ Royal Magical Library                         (密码: 70791313)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  6213    @ Monster Reincarnation                         (密码: 74848038)
    deck_card  5212    @ United We Stand                               (密码: 56747793)
    deck_card  5752    @ Magical Dimension                             (密码: 28553439)
    deck_card  5752    @ Magical Dimension                             (密码: 28553439)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4354    @ Swords of Revealing Light                     (密码: 72302403)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  5213    @ Mage Power                                    (密码: 83746708)
    deck_card  5630    @ Spell Absorption                              (密码: 51481927)
    deck_card  4341    @ Yami                                          (密码: 59197169)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  6168    @ Magician's Circle                             (密码: 00050755)
    deck_card  5124    @ Magic Cylinder                                (密码: 62279055)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x82, 0x19
    .byte 0xC9, 0x0F, 0xC9, 0x16, 0xC9, 0x16, 0x11, 0x16, 0x11, 0x16, 0x11, 0x16, 0x64, 0x15, 0x80, 0x14
    .byte 0x80, 0x14, 0xED, 0x16, 0x17, 0x16, 0x57, 0x16, 0xCB, 0x14, 0x12, 0x16, 0x12, 0x16, 0xA7, 0x13
    .byte 0x52, 0x11, 0x52, 0x11, 0x1A, 0x16, 0x1B, 0x13, 0x2D, 0x13, 0x11, 0x17, 0x45, 0x18, 0x5C, 0x14
    .byte 0x78, 0x16, 0x78, 0x16, 0x66, 0x13, 0x02, 0x11, 0x63, 0x13, 0x5D, 0x14, 0xFE, 0x15, 0xF5, 0x10
    .byte 0x61, 0x14, 0x7C, 0x13, 0x18, 0x15, 0x18, 0x18, 0x04, 0x14, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Cyber End Dragon
@ GBA地址: 0x09E6566E  ROM偏移: 0x1E6566E
@ 48 张牌，融合卡组 7 张
@ -----------------------------------------------------------------------------
deck_cyber_end_dragon:
    deck_card  6568    @ Cyber Barrier Dragon                          (密码: 68774379)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    deck_card  4421    @ Mechanicalchaser                              (密码: 07359741)
    deck_card  4421    @ Mechanicalchaser                              (密码: 07359741)
    deck_card  4421    @ Mechanicalchaser                              (密码: 07359741)
    deck_card  4924    @ Shining Angel                                 (密码: 95956346)
    deck_card  4924    @ Shining Angel                                 (密码: 95956346)
    deck_card  4924    @ Shining Angel                                 (密码: 95956346)
    deck_card  5504    @ X-Head Cannon                                 (密码: 62651957)
    deck_card  5504    @ X-Head Cannon                                 (密码: 62651957)
    deck_card  5504    @ X-Head Cannon                                 (密码: 62651957)
    deck_card  6588    @ Proto-Cyber Dragon                            (密码: 26439287)
    deck_card  6588    @ Proto-Cyber Dragon                            (密码: 26439287)
    deck_card  6588    @ Proto-Cyber Dragon                            (密码: 26439287)
    deck_card  6256    @ The Light - Hex-Sealed Fusion                 (密码: 15717011)
    deck_card  6256    @ The Light - Hex-Sealed Fusion                 (密码: 15717011)
    deck_card  6256    @ The Light - Hex-Sealed Fusion                 (密码: 15717011)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  6213    @ Monster Reincarnation                         (密码: 74848038)
    deck_card  4936    @ Luminous Spark                                (密码: 81777047)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  6511    @ Pot of Avarice                                (密码: 67169062)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  6398    @ Power Bond                                    (密码: 37630732)
    deck_card  6398    @ Power Bond                                    (密码: 37630732)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  5539    @ Metamorphosis                                 (密码: 46411259)
    deck_card  5129    @ Limiter Removal                               (密码: 23171610)
    deck_card  5560    @ Interdimensional Matter Transporter           (密码: 36261276)
    deck_card  6581    @ Attack Reflector Unit                         (密码: 91989718)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5686    @ Metal Reflect Slime                           (密码: 26905245)
    deck_card  5686    @ Metal Reflect Slime                           (密码: 26905245)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card     7    @ SO=0x0007                                     (密码: ?)
    deck_card  6397    @ Cyber End Dragon                              (密码: 01546123)
    deck_card  6397    @ Cyber End Dragon                              (密码: 01546123)
    deck_card  6397    @ Cyber End Dragon                              (密码: 01546123)
    deck_card  6396    @ Cyber Twin Dragon                             (密码: 74157028)
    deck_card  6396    @ Cyber Twin Dragon                             (密码: 74157028)
    deck_card  6396    @ Cyber Twin Dragon                             (密码: 74157028)
    deck_card  4740    @ Thousand-Eyes Restrict                        (密码: 63519819)
    .hword 0    @ 卡组终止符
    @ 融合卡组（7 张）
    deck_card 52225    @ SO=0xCC01                                     (密码: ?)
    deck_card 52428    @ SO=0xCCCC                                     (密码: ?)
    deck_card  8575    @ SO=0x217F                                     (密码: ?)
    deck_card 16759    @ SO=0x4177                                     (密码: ?)
    deck_card    40    @ SO=0x0028                                     (密码: ?)
    deck_card  6568    @ Cyber Barrier Dragon                          (密码: 68774379)
    deck_card  6390    @ Cyber Dragon                                  (密码: 70095154)
    @ padding/其他数据（104 字节）
    .byte 0xF6, 0x18, 0xF6, 0x18, 0x45, 0x11, 0x45, 0x11, 0x45, 0x11, 0x3C, 0x13, 0x3C, 0x13, 0x3C, 0x13
    .byte 0x80, 0x15, 0x80, 0x15, 0x80, 0x15, 0xBC, 0x19, 0xBC, 0x19, 0xBC, 0x19, 0x70, 0x18, 0x70, 0x18
    .byte 0x70, 0x18, 0x52, 0x11, 0x52, 0x11, 0xEC, 0x12, 0x2D, 0x13, 0x45, 0x18, 0x48, 0x13, 0xEB, 0x14
    .byte 0x6F, 0x19, 0x66, 0x13, 0xFE, 0x18, 0xFE, 0x18, 0x63, 0x13, 0xA3, 0x15, 0x09, 0x14, 0xB8, 0x15
    .byte 0xB5, 0x19, 0x7C, 0x13, 0x36, 0x16, 0x36, 0x16, 0x7D, 0x13, 0xA7, 0x16, 0x07, 0x00, 0xFD, 0x18
    .byte 0xFD, 0x18, 0xFD, 0x18, 0xFC, 0x18, 0xFC, 0x18, 0xFC, 0x18, 0x84, 0x12, 0x00, 0x00, 0x01, 0xCC
    .byte 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Stronghold
@ GBA地址: 0x09E65746  ROM偏移: 0x1E65746
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_stronghold:
    deck_card  5810    @ Chiron the Mage                               (密码: 16956455)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  5655    @ Breaker the Magical Warrior                   (密码: 71413901)
    deck_card  6151    @ Green Gadget                                  (密码: 41172955)
    deck_card  6151    @ Green Gadget                                  (密码: 41172955)
    deck_card  6151    @ Green Gadget                                  (密码: 41172955)
    deck_card  6155    @ Red Gadget                                    (密码: 86445415)
    deck_card  6155    @ Red Gadget                                    (密码: 86445415)
    deck_card  6155    @ Red Gadget                                    (密码: 86445415)
    deck_card  6156    @ Yellow Gadget                                 (密码: 13839120)
    deck_card  6156    @ Yellow Gadget                                 (密码: 13839120)
    deck_card  6156    @ Yellow Gadget                                 (密码: 13839120)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  6003    @ Shield Crash                                  (密码: 30683373)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  4835    @ Fissure                                       (密码: 66788016)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  6511    @ Pot of Avarice                                (密码: 67169062)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4342    @ Dark Hole                                     (密码: 53129443)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  5129    @ Limiter Removal                               (密码: 23171610)
    deck_card  5849    @ Reload                                        (密码: 22589918)
    deck_card  4861    @ Solemn Judgment                               (密码: 41420027)
    deck_card  6153    @ Stronghold                                    (密码: 13955608)
    deck_card  6153    @ Stronghold                                    (密码: 13955608)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  4692    @ Widespread Ruin                               (密码: 77754944)
    deck_card  6445    @ Rising Energy                                 (密码: 78211862)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0xB2, 0x16
    .byte 0x1C, 0x16, 0x17, 0x16, 0x07, 0x18, 0x07, 0x18, 0x07, 0x18, 0x0B, 0x18, 0x0B, 0x18, 0x0B, 0x18
    .byte 0x0C, 0x18, 0x0C, 0x18, 0x0C, 0x18, 0x1B, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0x73, 0x17, 0x11, 0x17
    .byte 0x11, 0x17, 0xEB, 0x14, 0xEB, 0x14, 0xE3, 0x12, 0x29, 0x13, 0x29, 0x13, 0x6F, 0x19, 0x66, 0x13
    .byte 0xF6, 0x10, 0x63, 0x13, 0x63, 0x13, 0x09, 0x14, 0xD9, 0x16, 0xFD, 0x12, 0x09, 0x18, 0x09, 0x18
    .byte 0x18, 0x15, 0x18, 0x15, 0x54, 0x12, 0x2D, 0x19, 0xA7, 0x16, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Horus the Black Flame D
@ GBA地址: 0x09E65806  ROM偏移: 0x1E65806
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_horus_the_black_flame_d:
    deck_card  6100    @ Horus the Black Flame Dragon LV8              (密码: 48229808)
    deck_card  6100    @ Horus the Black Flame Dragon LV8              (密码: 48229808)
    deck_card  6099    @ Horus the Black Flame Dragon LV6              (密码: 11224103)
    deck_card  6099    @ Horus the Black Flame Dragon LV6              (密码: 11224103)
    deck_card  5876    @ Blazing Inpachi                               (密码: 05464695)
    deck_card  5876    @ Blazing Inpachi                               (密码: 05464695)
    deck_card  5810    @ Chiron the Mage                               (密码: 16956455)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  6098    @ Horus the Black Flame Dragon LV4              (密码: 75830094)
    deck_card  6098    @ Horus the Black Flame Dragon LV4              (密码: 75830094)
    deck_card  6098    @ Horus the Black Flame Dragon LV4              (密码: 75830094)
    deck_card  6595    @ Tenkabito Shien                               (密码: 41589166)
    deck_card  6595    @ Tenkabito Shien                               (密码: 41589166)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5974    @ Solar Flare Dragon                            (密码: 45985838)
    deck_card  4917    @ UFO Turtle                                    (密码: 60806437)
    deck_card  4917    @ UFO Turtle                                    (密码: 60806437)
    deck_card  5878    @ The Thing in the Crater                       (密码: 78243409)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6093    @ Charcoal Inpachi                              (密码: 13179332)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  4934    @ Molten Destruction                            (密码: 19384334)
    deck_card  4934    @ Molten Destruction                            (密码: 19384334)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4354    @ Swords of Revealing Light                     (密码: 72302403)
    deck_card  4963    @ Nobleman of Crossout                          (密码: 71044499)
    deck_card  6135    @ The Graveyard in the Fourth Dimension         (密码: 88089103)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  6133    @ Level Up!                                     (密码: 25290459)
    deck_card  6133    @ Level Up!                                     (密码: 25290459)
    deck_card  6468    @ Level Modulation                              (密码: 61850482)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  4866    @ Royal Decree                                  (密码: 51452091)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00, 0xD4, 0x17
    .byte 0xD4, 0x17, 0xD3, 0x17, 0xD3, 0x17, 0xF4, 0x16, 0xF4, 0x16, 0xB2, 0x16, 0x1C, 0x16, 0xD2, 0x17
    .byte 0xD2, 0x17, 0xD2, 0x17, 0xC3, 0x19, 0xC3, 0x19, 0x57, 0x16, 0x56, 0x17, 0x35, 0x13, 0x35, 0x13
    .byte 0xF6, 0x16, 0x52, 0x11, 0xCD, 0x17, 0x1B, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0xEB, 0x14, 0xEB, 0x14
    .byte 0x46, 0x13, 0x46, 0x13, 0x66, 0x13, 0x02, 0x11, 0x63, 0x13, 0xF7, 0x17, 0x61, 0x14, 0xF5, 0x17
    .byte 0xF5, 0x17, 0x44, 0x19, 0x02, 0x13, 0x02, 0x13, 0x02, 0x13, 0x7C, 0x13, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Sacred Phoenix of N
@ GBA地址: 0x09E658C6  ROM偏移: 0x1E658C6
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_sacred_phoenix_of_n:
    deck_card  6236    @ Sacred Phoenix of Nephthys                    (密码: 61441708)
    deck_card  5902    @ Ryu Kokki                                     (密码: 57281778)
    deck_card  5410    @ Vampire Lord                                  (密码: 53839837)
    deck_card  5410    @ Vampire Lord                                  (密码: 53839837)
    deck_card  6287    @ Curse of Vampire                              (密码: 34294855)
    deck_card  6041    @ Regenerating Mummy                            (密码: 70821187)
    deck_card  6041    @ Regenerating Mummy                            (密码: 70821187)
    deck_card  5810    @ Chiron the Mage                               (密码: 16956455)
    deck_card  5932    @ D. D. Assailant                               (密码: 70074904)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  5423    @ Pyramid Turtle                                (密码: 77044671)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  6237    @ Hand of Nephthys                              (密码: 98446407)
    deck_card  6237    @ Hand of Nephthys                              (密码: 98446407)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  5526    @ Spirit Reaper                                 (密码: 23205979)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5905    @ Smashing Ground                               (密码: 97169186)
    deck_card  4818    @ Scapegoat                                     (密码: 73915051)
    deck_card  5430    @ Book of Life                                  (密码: 02204140)
    deck_card  5430    @ Book of Life                                  (密码: 02204140)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  5435    @ Call of the Mummy                             (密码: 04861205)
    deck_card  6546    @ Mistobody                                     (密码: 47529357)
    deck_card  6546    @ Mistobody                                     (密码: 47529357)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5544    @ Raigeki Break                                 (密码: 04178474)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    deck_card  4886    @ Waboku                                        (密码: 12607053)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0x5C, 0x18
    .byte 0x0E, 0x17, 0x22, 0x15, 0x22, 0x15, 0x8F, 0x18, 0x99, 0x17, 0x99, 0x17, 0xB2, 0x16, 0x2C, 0x17
    .byte 0x57, 0x16, 0x2F, 0x15, 0x2F, 0x15, 0x2F, 0x15, 0xD6, 0x0F, 0x5D, 0x18, 0x5D, 0x18, 0x96, 0x15
    .byte 0x96, 0x15, 0x52, 0x11, 0x8D, 0x19, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13, 0x11, 0x17
    .byte 0xD2, 0x12, 0x36, 0x15, 0x36, 0x15, 0xF2, 0x17, 0x3B, 0x15, 0x92, 0x19, 0x92, 0x19, 0x61, 0x14
    .byte 0x7C, 0x13, 0xA8, 0x15, 0x18, 0x15, 0xA7, 0x16, 0xA7, 0x16, 0x7D, 0x13, 0x16, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00

@ -----------------------------------------------------------------------------
@ Raviel Lord of Phantasms
@ GBA地址: 0x09E65986  ROM偏移: 0x1E65986
@ 40 张牌
@ -----------------------------------------------------------------------------
deck_raviel_lord_of_phantasms:
    deck_card  6565    @ Raviel, Lord of Phantasms                     (密码: 69890967)
    deck_card  6565    @ Raviel, Lord of Phantasms                     (密码: 69890967)
    deck_card  6565    @ Raviel, Lord of Phantasms                     (密码: 69890967)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  6418    @ Goblin Elite Attack Force                     (密码: 85306040)
    deck_card  5037    @ Slate Warrior                                 (密码: 78636495)
    deck_card  5037    @ Slate Warrior                                 (密码: 78636495)
    deck_card  5037    @ Slate Warrior                                 (密码: 78636495)
    deck_card  5762    @ Archfiend Soldier                             (密码: 49881766)
    deck_card  5655    @ Breaker the Magical Warrior                   (密码: 71413901)
    deck_card  5660    @ Tribe-Infecting Virus                         (密码: 33184167)
    deck_card  5719    @ D.D. Warrior Lady                             (密码: 07572887)
    deck_card  6027    @ Protector of the Sanctuary                    (密码: 24221739)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4921    @ Giant Germ                                    (密码: 95178994)
    deck_card  4054    @ Sangan                                        (密码: 26202165)
    deck_card  5226    @ Earthbound Spirit                             (密码: 67105242)
    deck_card  4923    @ Spear Cretin                                  (密码: 58551308)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  6541    @ Magical Mallet                                (密码: 85852291)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4898    @ Snatch Steal                                  (密码: 45986603)
    deck_card  4844    @ Pot of Greed                                  (密码: 55144522)
    deck_card  4909    @ Mystical Space Typhoon                        (密码: 05318639)
    deck_card  5355    @ Collapse                                      (密码: 55713623)
    deck_card  4803    @ Brain Control                                 (密码: 87910978)
    deck_card  5212    @ United We Stand                               (密码: 56747793)
    deck_card  5432    @ Book of Moon                                  (密码: 14087893)
    deck_card  4905    @ Rush Recklessly                               (密码: 70046172)
    deck_card  6130    @ Hammer Shot                                   (密码: 26412047)
    deck_card  5217    @ Lightning Vortex                              (密码: 69162969)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5544    @ Raigeki Break                                 (密码: 04178474)
    deck_card  5400    @ Bottomless Trap Hole                          (密码: 29401950)
    deck_card  5310    @ Bark of Dark Ruler                            (密码: 41925941)
    deck_card  5310    @ Bark of Dark Ruler                            (密码: 41925941)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  4989    @ Call of the Haunted                           (密码: 97077563)
    .hword 0    @ 卡组终止符
    @ padding/其他数据（110 字节）
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x12, 0x00, 0x4F, 0x57, 0x44, 0x3F, 0x28, 0x00, 0xA5, 0x19
    .byte 0xA5, 0x19, 0xA5, 0x19, 0x12, 0x19, 0x12, 0x19, 0xAD, 0x13, 0xAD, 0x13, 0xAD, 0x13, 0x82, 0x16
    .byte 0x17, 0x16, 0x1C, 0x16, 0x57, 0x16, 0x8B, 0x17, 0x39, 0x13, 0x39, 0x13, 0x39, 0x13, 0xD6, 0x0F
    .byte 0x6A, 0x14, 0x3B, 0x13, 0x52, 0x11, 0x8D, 0x19, 0x1B, 0x13, 0x22, 0x13, 0xEC, 0x12, 0x2D, 0x13
    .byte 0xEB, 0x14, 0xC3, 0x12, 0x5C, 0x14, 0x38, 0x15, 0x29, 0x13, 0xF2, 0x17, 0x61, 0x14, 0x7C, 0x13
    .byte 0x7C, 0x13, 0xA8, 0x15, 0x18, 0x15, 0xBE, 0x14, 0xBE, 0x14, 0xA7, 0x16, 0x7D, 0x13, 0x00, 0x00
    .byte 0x00, 0x00, 0x00, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0x7F, 0x21, 0x77, 0x41, 0x28, 0x00

