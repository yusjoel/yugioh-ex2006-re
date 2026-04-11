@ =============================================================================
@ 初始卡组数据（Starter Deck）
@ ROM偏移: 0x1E5F884 - 0x1E5F8E9（共 102 字节）
@
@ 格式: [so_code LE16] 连续排列，以 0x0000 终止
@ 重复相同 so_code 表示多张副本
@
@ 来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md
@ =============================================================================

starter_deck:
    deck_card  4064    @ Kuriboh                                       (密码: 40640057)
    deck_card  4272    @ Princess of Tsurugi                           (密码: 51371017)
    deck_card  4317    @ Black Pendant                                 (密码: 65169794)
    deck_card  4345    @ Red Medicine                                  (密码: 38199696)
    deck_card  4352    @ Ookazi                                        (密码: 19523799)
    deck_card  4434    @ Magician of Faith                             (密码: 31560081)
    deck_card  4546    @ Skelengel                                     (密码: 60694662)
    deck_card  4753    @ Gazelle the King of Mythical Beasts           (密码: 05818798)
    deck_card  4803    @ Brain Control                                 (密码: 87910978)
    deck_card  4835    @ Fissure                                       (密码: 66788016)
    deck_card  4849    @ Reinforcements                                (密码: 17814387)
    deck_card  4850    @ Castle Walls                                  (密码: 44209392)
    deck_card  4856    @ Tribute to The Doomed                         (密码: 79759861)
    deck_card  4891    @ Heavy Storm                                   (密码: 19613556)
    deck_card  4932    @ Gaia Power                                    (密码: 56594520)
    deck_card  4966    @ Premature Burial                              (密码: 70828912)
    deck_card  4988    @ Dust Tornado                                  (密码: 60082869)
    deck_card  5124    @ Magic Cylinder                                (密码: 62279055)
    deck_card  5210    @ Jar of Greed                                  (密码: 83968380)
    deck_card  5320    @ Warrior Dai Grepher                           (密码: 75953262)
    deck_card  5330    @ The Warrior Returning Alive                   (密码: 95281259)
    deck_card  5331    @ Ready for Intercepting                        (密码: 31785398)
    deck_card  5334    @ Spear Dragon                                  (密码: 31553716)
    deck_card  5349    @ Luster Dragon #2                              (密码: 17658803)
    deck_card  5581    @ Dark Blade                                    (密码: 11321183)
    deck_card  5644    @ Luster Dragon                                 (密码: 11091375)
    deck_card  5799    @ Sakuretsu Armor                               (密码: 56120475)
    deck_card  5914    @ Compulsory Evacuation Device                  (密码: 94192409)
    deck_card  5947    @ Warrior of Zera                               (密码: 66073051)
    deck_card  6037    @ Spirit Caller                                 (密码: 48659020)
    deck_card  6121    @ The Trojan Horse                              (密码: 38479725)
    deck_card  6129    @ Dark Factory of Mass Production               (密码: 90928333)
    deck_card  6148    @ Cemetary Bomb                                 (密码: 51394546)
    deck_card  6196    @ Mirage Dragon                                 (密码: 15960641)
    deck_card  6213    @ Monster Reincarnation                         (密码: 74848038)
    deck_card  6310    @ Elemental Hero Avian                          (密码: 21844576)
    deck_card  6311    @ Elemental Hero Burstinatrix                   (密码: 58932615)
    deck_card  6312    @ Elemental Hero Clayman                        (密码: 84327329)
    deck_card  6313    @ Elemental Hero Sparkman                       (密码: 20721928)
    deck_card  6477    @ Elemental Hero Bladedge                       (密码: 59793705)
    deck_card    64    @ SO=0x0040                                     (密码: ?)
    deck_card    64    @ SO=0x0040                                     (密码: ?)
    deck_card   128    @ SO=0x0080                                     (密码: ?)
    deck_card   128    @ SO=0x0080                                     (密码: ?)
    deck_card    32    @ SO=0x0020                                     (密码: ?)
    deck_card    16    @ SO=0x0010                                     (密码: ?)
    deck_card    32    @ SO=0x0020                                     (密码: ?)
    deck_card    16    @ SO=0x0010                                     (密码: ?)
    deck_card     2    @ SO=0x0002                                     (密码: ?)
    deck_card     1    @ SO=0x0001                                     (密码: ?)
    .hword 0    @ 卡组终止符
