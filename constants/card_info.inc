@ =============================================================================
@ Card Info Page constants (card_info_page_init_bg0 / draw_card_*_label_to_vram)
@ Source: asm/01_vija_scene_text.s, Seg-2 (0x0801d448..0x0801d998)
@ Seg-3 additions: card_image_decode_wrapper / render_card_name_to_desc_page_vram /
@   card_info_page_finalize / blit_glyph_2x2_to_bg_vram / tick_blend_fadein_and_poll_done
@ =============================================================================

@ BG Layer Control Register initial values (written to BG1CNT/BG2CNT/BG3CNT)
.equ CARD_INFO_BG1CNT_INIT, 0x00004104  @ BG1CNT: pri=0 charbase=1 16col scrbase=0x10 32x32
.equ CARD_INFO_BG2CNT_INIT, 0x00000407  @ BG2CNT: pri=3 charbase=1 16col scrbase=0 32x32
.equ CARD_INFO_BG3CNT_INIT, 0x00000305  @ BG3CNT: pri=1 charbase=0 16col scrbase=0 32x32

@ OBJ Palette slot for card info frame (OBJ_PALRAM_BASE + 0x1e0 = pal 15 color 0)
.equ CARD_INFO_OBJ_PAL_SLOT, 0x050003e0  @ OBJ palette slot for card name/stat frame tiles

@ BG VRAM write bases for card info text (all < 0x06010000 = BG VRAM, not OBJ tile VRAM)
.equ CARD_INFO_NAME_BG_TILE_VRAM, 0x06001840  @ BG screen-map tile-attr write base for card name line (CB0, SB3+0x040)
.equ CARD_INFO_NAME_SPRITE_VRAM,  0x06008200  @ commit_line_buffer_to_sprite_vram target for card name
.equ CARD_INFO_STAT_BG_TILE_VRAM, 0x06001c00  @ BG screen-map tile-attr write base for ATK/DEF/Level lines (CB0, SB3+0x400)
.equ CARD_INFO_STAT_SPRITE_VRAM,  0x06008580  @ commit_line_buffer_to_sprite_vram target for ATK/DEF/Level

@ --- Seg-3 additions (card_image_decode_wrapper + render_card_name_to_desc_page_vram + card_info_page_finalize) ---

@ Card image tile pack parameters (card_image_decode_wrapper)
.equ CARD_TILE_PACK_GLYPH_OFF_A,   0x0985004c  @ card_glyph_table_3+0xa80 (tile src A, normal card map)
.equ CARD_TILE_PACK_GLYPH_OFF_B,   0x09850934  @ card_glyph_table_3+0x1368 (tile src B)
.equ CARD_TILE_PACK_MAP_PARAM,     0x0000020e  @ load_pack_tile_and_map_to_vram map param (31 ROM refs)
.equ CARD_FRAME_TILE_SRC_MONSTER,  0x0984a3fc  @ seg-C blob: monster card frame tile pack source
.equ CARD_FRAME_TILE_SRC_SPELL,    0x0984b994  @ seg-C blob: spell card frame tile pack source (type23)
.equ CARD_FRAME_PAL_SRC_MONSTER_A, 0x0984dd6c  @ seg-C blob: monster frame OBJ palette A (32B)
.equ CARD_FRAME_TILE_SRC_MONSTER_A,0x0984d8ec  @ seg-C blob: monster frame OBJ tile data A (256B)
.equ CARD_FRAME_PAL_SRC_SPELL_A,   0x0984de6c  @ seg-C blob: spell frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_SPELL_A,  0x0984dcec  @ seg-C blob: spell frame OBJ tile data A
.equ CARD_FRAME_PAL_SRC_STAR_A,    0x0984f52c  @ seg-C blob: star/level frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_STAR,     0x0984dc6c  @ seg-C blob: star/level OBJ tile data
.equ CARD_FRAME_TILE_SRC_STAR_B,   0x0984f46c  @ seg-C blob: star/level OBJ tile data B
.equ CARD_FRAME_PAL_SRC_MONSTER_B, 0x0984de4c  @ seg-C blob: monster frame OBJ palette B
.equ CARD_FRAME_PAL_SRC_ICON_A,    0x0984ee2c  @ seg-C blob: icon frame OBJ palette A (type 0x17)
.equ CARD_FRAME_PAL_SRC_ICON_B,    0x0984f3ac  @ seg-C blob: icon frame OBJ palette B (type 0x16)
.equ CARD_FRAME_TILE_SRC_ICON,     0x0984f0ac  @ seg-C blob: icon frame OBJ tile data (type 0x16)
.equ CARD_FRAME_TILE_SRC_SPELL_B,  0x0984e42c  @ seg-C blob: spell frame OBJ tile data B (type 0x17)
.equ CARD_OVERLAY_TILE_SRC,        0x09ccd2d0  @ name_o region+0x40: card overlay nibble-sequence tile (5 refs)

@ Card frame PALRAM/VRAM destinations (card_image_decode_wrapper + card_info_page_finalize)
.equ CARD_FRAME_BG_PAL_BASE,    0x050000a0  @ BG PALRAM row 5 (card frame BG palette base)
.equ CARD_FRAME_OBJ_PAL_MONSTER,0x050003a0  @ OBJ PALRAM slot 13 (monster frame palette, PAL+0x1a0)
.equ CARD_FRAME_OBJ_PAL_SPELL,  0x050003c0  @ OBJ PALRAM slot 14 (spell/star frame palette, PAL+0x1c0)
.equ CARD_FRAME_OBJ_PAL_LEVEL,  0x05000380  @ OBJ PALRAM slot 12 (level/icon frame palette, PAL+0x180)
.equ CARD_FRAME_OBJ_TILE_BASE,  0x06017440  @ OBJ VRAM card frame tile base (OBJ+0x7440)
.equ CARD_LEVEL_OBJ_TILE_BASE,  0x060174c0  @ OBJ VRAM card level star tile base (OBJ+0x74c0)
.equ CARD_SPELL_OBJ_TILE_BASE,  0x06017500  @ OBJ VRAM spell card icon tile base (OBJ+0x7500)
.equ CARD_ICON_OBJ_TILE_BASE,   0x06017580  @ OBJ VRAM card icon/status tile base (OBJ+0x7580)
.equ CARD_FRAME_OBJ_TILE_SLOT1, 0x06010020  @ OBJ_TILE_VRAM_BASE+0x20 (tile slot 1 for card art overlay)
.equ CARD_DESC_OBJ_TILE_BASE,   0x06010040  @ OBJ_TILE_VRAM_BASE+0x40 (tile slot 2 for card desc text)

@ Card description page text VRAM (render_card_name_to_desc_page_vram + render_card_description_text)
.equ CARD_DESC_LINE_BUF_VRAM,   0x06007100  @ BG VRAM card description text line buffer
.equ CARD_DESC_BG_VRAM_A,       0x06000800  @ BG VRAM desc page tile region A (tile-seq write target A)
.equ CARD_DESC_BG_VRAM_B,       0x06000c80  @ BG VRAM desc page tile region B (tile-seq write target B)
.equ CARD_DESC_RENDER_PARAM,    0x00008008  @ render_glyph_jp layer param for card description

@ --- Seg-4 additions (draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam) ---

@ OAM packed constants for card stat digit sprites (write_oam_entry_from_packed_args: r0=packed_xy, r1=tile_idx, r2=attr2)
@ packed_xy format: low16=x_coord (9-bit), high16=oam_y
.equ CARD_STAT_ATK_DEF_OAM_XY,    0x00060056  @ ATK/DEF frame OBJ position (x=86, y=6); 4 ROM refs
.equ CARD_STAT_ATK_DEF_OAM_ATTR2, 0x0000d3a2  @ ATK/DEF frame attr2: pal13, tile0x3a2; 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_XY,      0x00150058  @ Quick-Play Spell secondary marker pos (x=88, y=21); 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_ATTR2,   0x0000e3a6  @ Quick-Play marker attr2: pal14, tile0x3a6; 2 ROM refs
.equ CARD_STAT_DIGIT_OAM_ATTR2,   0x0000f001  @ ATK/DEF digit sprite attr2: pal15, tile1; 2 ROM refs
.equ CARD_STAT_FUSION_OAM_ATTR2,  0x0000c3a8  @ Fusion/extra-type marker attr2: pal12, tile0x3a8; 1 ROM ref

@ OAM attr2 base offsets for stat row sprites (draw_stat_row_sprites_to_oam)
@ Added to r5 (col_idx*0x10 + 2) then u16-truncated to produce attr2 per row
.equ CARD_STAT_ROW_ATTR2_BASE_A,  0xfffff800  @ stat row sprite group A attr2 base (row 0, Y=0x70)
.equ CARD_STAT_ROW_ATTR2_BASE_B,  0xfffff804  @ stat row sprite group B attr2 base (row 1, Y=0x90)
.equ CARD_STAT_ROW_ATTR2_BASE_C,  0xfffff808  @ stat row sprite group C attr2 base (row 2, Y=0xb0)
.equ CARD_STAT_ROW_ATTR2_BASE_D,  0xfffff80c  @ stat row sprite group D attr2 base (row 3, Y=0xd0)

@ --- Seg-8 additions: LP threshold constants for render_card_stats_to_line_buf ---

.equ CARD_STAT_LP_THRESHOLD,      0x00000bb8  @ 3000 LP threshold for card stat display branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_999,  0x000003e7  @ 999 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_1500, 0x000005dc  @ 1500 LP threshold (render_card_stats dispatch); 35 ROM refs
.equ CARD_STAT_LP_THRESHOLD_5730, 0x00001662  @ 5730 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_57300,0x0000dfd4  @ 57300 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_572488,0x0008be48 @ 572488 LP threshold (upper range); 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_20000,0x00004e20  @ 20000 LP threshold extended render path; 1 ROM ref

@ gCardInfoPageState.word0 bit-field masks (card_list_on_select_to_info_page)
@ word0 layout: bits[2:0]=flags, bits[16:3]=card_id (14-bit), bit17=active_flag
.equ CARD_INFO_STATE_CARD_ID_MASK,  0x00003fff  @ mask for card_id bits[13:0] before shift-3 into word0
.equ CARD_INFO_STATE_CARD_ID_CLEAR, 0xfffe0007  @ AND mask to clear card_id field bits[16:3], preserve [17]+[2:0]

@ =============================================================================
@ file 02 Seg-1 additions: text render / pack selection / opp card name offsets
@ =============================================================================

.equ GAME_STR_TEXT_BASE,            0x00000C1C  @ str_base_offset=0x0c1c; adds to game_str_id_offset; 15 ROM refs
.equ CARD_ID_BASE_NEG_ADJ,          0xFFFFD8EF  @ neg adj -0x2711 so card_id 0x2711 maps to 0; 5 ROM refs
.equ PACK_DECK_A_KEY,               0x00002711  @ deck A key for find_deck_record_index_by_key; 5 ROM refs
.equ OPP_CARD_NAME_STR_OFF_ES,      0x0003A90C  @ ES offset from game_str_ja_0326 base; 1 ROM ref
.equ OPP_CARD_NAME_STR_OFF_ES_NULL, 0x0003A90E  @ ES offset from game_str_ja_0327 base; 1 ROM ref

@ =============================================================================
@ file 02 Seg-5 additions: field spell type-B effect chain guard
@ =============================================================================
.equ FIELD_SPELL_B_EFFECT_ID, 0x00001407  @ effect chain guard value for field spell type-B placement check; 12 ROM refs

@ =============================================================================
@ file 02 Seg-6 additions: zone slot set_code / card_id mask
@ =============================================================================
.equ SLOT_CARD_SET_CODE_MASK, 0x00001fff  @ 13-bit mask for YGO set_code/card_id fields in zone slot arrays; 101 raw refs; 2 Seg-6 slots

@ =============================================================================
@ file 02 Seg-8 additions: field spell / monster zone card IDs
@ =============================================================================
.equ TOON_WORLD_CARD_ID,             0x000012be  @ Toon World field-magic card id; presence check via equip-zone scan; 9 raw refs
.equ GROUND_COLLAPSE_FIELD_CARD_ID,  0x00001432  @ Ground Collapse field spell card id (data.md line 900, passcode 90502999); placement-block check in check_slot_placement_blocked_by_field_effect; 18 raw refs
.equ OJAMA_KING_CARD_ID,             0x000017ee  @ Ojama King card id (data.md line 1639, passcode 90140980); monster-zone limit effect; placement-block check; 13 raw refs
.equ SPATIAL_COLLAPSE_CARD_ID,       0x000016df  @ Spatial Collapse field spell id; monster zone clamp in count_available_monster_slots; 16 raw refs

@ =============================================================================
@ file 02 Seg-9 additions: equip placement eligibility / lock IDs
@ =============================================================================
@ Zone slot card_id values > 5169 (max card stat entry index) are effect/token IDs
@ used by the equip chain and field effect systems, not regular card stats entries.
.equ EQUIP_LOCKDOWN_CID,        0x000013f2  @ equip lockdown: count_field_copies>0 blocks all equip placement; 4 slots
.equ EQUIP_ZONE_BLOCKER_CID,    0x000013eb  @ cross-player equip blocker effect node; find_effect_node absent -> no equip; 1 slot
.equ EQUIP_LOCK_A_CID,          0x000016a4  @ equip lock chain effect A; check_value_in_slot_chain; 1 slot
.equ EQUIP_LOCK_B_CID,          0x000012d1  @ equip lock chain effect B; check_value_in_slot_chain; 1 slot
.equ EQUIP_ELIG_EXCL_A,         0x000014f9  @ equip eligibility exclusion id A; BST in check_slot_equip_eligibility; 1 slot
.equ EQUIP_ELIG_EXCL_B,         0x00001836  @ equip eligibility exclusion id B; bit-flag check path; 1 slot
.equ EQUIP_ELIG_EXCL_C,         0x00001670  @ equip eligibility exclusion id C; 1 slot
.equ EQUIP_ELIG_EXCL_D,         0x000019ee  @ equip eligibility exclusion id D; bit18 path; 1 slot
.equ EQUIP_PAIR_EXCL_A,         0x000017e9  @ field7 equip-pair whitelist A; check_equip_cards_share_field7; 1 slot
.equ EQUIP_PAIR_EXCL_B,         0x00001521  @ field7 equip-pair whitelist B; 1 slot
.equ EQUIP_PAIR_EXCL_C,         0x00001798  @ field7 equip-pair whitelist C; 1 slot
.equ EQUIP_PAIR_RANGE_MAX,      0x00001874  @ field7 BST range boundary: IDs in [0x1873..0x1874] pass; 1 slot
.equ EQUIP_CHAIN_PAIR_CARD_MAX, 0x0000164f  @ max card_id for chain pairing path in count_equip_placements_with_chain_check; 1 slot

@ =============================================================================
@ file 02 Seg-10a additions: card slot IDs for activation eligibility checks
@ =============================================================================
.equ UMI_CARD_ID,                    0x000010f4  @ Umi field spell (pw=22702055); special-case in check_card_matches_active_effect_slot; 31 raw refs; 2 slots
.equ A_LEGENDARY_OCEAN_CARD_ID,      0x0000150b  @ A Legendary Ocean (pw=295517); proxy reference for Umi activation category; 18 raw refs; 1 slot
.equ SPELL_ZONE_TARGET_CARD_ID,      0x00001368  @ cross-player spell-zone effect node type ID; used in find_paired_zone_entry_for_card + check_card_targeted_by_spell_zone_effect; 11 raw refs; 2 slots
.equ TOTAL_DEFENSE_SHOGUN_CARD_ID,   0x000012b4  @ Total Defense Shogun (pw=75372290); special activation via slot[+0x10] bit5; 5 raw refs; 1 slot
.equ EHERO_RAMPART_BLASTER_CARD_ID,  0x00001956  @ Elemental Hero Rampart Blaster (pw=47737087); activation: inverted bit5 + zone count; 8 raw refs; 1 slot
.equ TWINHEADED_BEAST_CARD_ID,       0x00001723  @ Twinheaded Beast (pw=82035781); monster activation check; 4 raw refs; 1 slot
.equ TYRANT_DRAGON_CARD_ID,          0x000014d5  @ Tyrant Dragon (pw=94568601); monster activation check; 8 raw refs; 1 slot
.equ ARMED_SAMURAI_BEN_KEI_CARD_ID,  0x0000186c  @ Armed Samurai - Ben Kei (pw=84430950); monster activation check; 8 raw refs (1 Seg-10a slot)

@ =============================================================================
@ file 02 Seg-10b additions: fieldspell / activation eligibility card IDs
@ =============================================================================
.equ JINZO_7_CID,                0x0000114c  @ Jinzo #7; fieldspell eligibility BST; 12 raw refs
.equ MANGA_RYU_RAN_CID,          0x0000127d  @ Manga Ryu-Ran; fieldspell chain; 10 raw refs
.equ GEAR_GOLEM_CID,             0x00001295  @ Gear Golem the Moving Fortress; 9 raw refs
.equ BLUE_EYES_TOON_DRAGON_CID,  0x000012a5  @ Blue-Eyes Toon Dragon; activation elig; 10 raw refs
.equ RING_OF_MAGNETISM_CID,      0x00001318  @ Ring of Magnetism; activation elig; 22 raw refs
.equ JOWLS_OF_DARK_DEMISE_CID,   0x000013ab  @ Jowls of Dark Demise; fieldspell chain; 12 raw refs
.equ SERVANT_OF_CATABOLISM_CID,  0x000013b3  @ Servant of Catabolism; fieldspell BST; 5 raw refs
.equ LEGENDARY_FISHERMAN_CID,    0x000013cd  @ The Legendary Fisherman; chain check; 8 raw refs
.equ ZOMBYRA_THE_DARK_CID,       0x0000147d  @ Zombyra the Dark; fieldspell chain; 7 raw refs
.equ MARAUDING_CAPTAIN_CID,      0x000014c6  @ Marauding Captain; activation elig; 9 raw refs
.equ A_FEINT_PLAN_CID,           0x000014d4  @ A Feint Plan; activation elig; 7 raw refs
.equ ASURA_PRIEST_CID,           0x00001505  @ Asura Priest; activation elig BST; 32 raw refs
.equ TOON_DARK_MAGICIAN_GIRL_CID,0x0000154a  @ Toon Dark Magician Girl; 6 raw refs
.equ TOON_DEFENSE_CID,           0x00001561  @ Toon Defense; zone chain filter; 12 raw refs
.equ TOON_GOBLIN_AF_CID,         0x00001566  @ Toon Goblin Attack Force; fieldspell BST; 13 raw refs
.equ REAPER_ON_NIGHTMARE_CID,    0x00001598  @ Reaper on the Nightmare; fieldspell BST; 10 raw refs
.equ DRILLAGO_CID,               0x000015ba  @ Drillago; fieldspell BST; 9 raw refs
.equ KIRYU_CID,                  0x000015cf  @ Kiryu; fieldspell chain filter; 16 raw refs
.equ RAREGOLD_ARMOR_CID,         0x000015ea  @ Raregold Armor; activation elig; 6 raw refs
.equ DIFFUSION_WAVE_MOTION_CID,  0x000015ff  @ Diffusion Wave-Motion; activation/fieldspell elig BST; 23 raw refs
.equ AMAZONESS_TIGER_CID,        0x0000160f  @ Amazoness Tiger; activation elig BST; 10 raw refs
.equ MAGICAL_SCIENTIST_CID,      0x00001619  @ Magical Scientist; fieldspell chain; 83 raw refs
.equ BERSERK_DRAGON_CID,         0x00001644  @ Berserk Dragon; activation elig BST; 14 raw refs
.equ GUARDIAN_KAYEST_CID,        0x0000164e  @ Guardian Kay'est; activation/trap chain; 8 raw refs
.equ SHOOTING_STAR_BOW_CID,      0x0000165d  @ Shooting Star Bow - Ceal; fieldspell chain; 14 raw refs
.equ STAUNCH_DEFENDER_CID,       0x00001669  @ Staunch Defender; activation/fieldspell elig; 14 raw refs
.equ VILEPAWN_ARCHFIEND_CID,     0x0000168c  @ Vilepawn Archfiend; activation elig BST; 8 raw refs
.equ CHECKMATE_CID,              0x0000169b  @ Checkmate; fieldspell chain filter; 13 raw refs
.equ DARK_SCORPION_COMBO_CID,    0x000016a3  @ Dark Scorpion Combination; fieldspell chain; 14 raw refs
.equ MAGICIANS_VALKYRIE_CID,     0x000016ed  @ Magician's Valkyrie; activation elig BST; 8 raw refs
.equ BLACK_TYRANNO_CID,          0x00001701  @ Black Tyranno; fieldspell BST; 8 raw refs
.equ PRICKLE_FAIRY_CID,          0x00001703  @ Prickle Fairy; activation elig BST; 16 raw refs
.equ AMPHIBIOUS_BUGROTH_MK3_CID, 0x00001705  @ Amphibious Bugroth MK-3; fieldspell BST; 11 raw refs
.equ SOLAR_FLARE_DRAGON_CID,     0x00001756  @ Solar Flare Dragon; activation elig BST; 7 raw refs
.equ OPTI_CAMO_ARMOR_CID,        0x00001759  @ Opti-Camouflage Armor; fieldspell chain; 10 raw refs
.equ MARSHMALLON_CID,            0x00001770  @ Marshmallon; activation elig BST; 11 raw refs
.equ MARSHMALLON_GLASSES_CID,    0x00001777  @ Marshmallon glasses; activation elig; 25 raw refs
.equ EMISSARY_OF_OASIS_CID,      0x0000179d  @ Emissary of the Oasis; activation elig BST; 7 raw refs
.equ DELTA_ATTACKER_CID,         0x000017aa  @ Delta Attacker; fieldspell chain; 12 raw refs
.equ TAUNT_CID,                  0x000017fc  @ Taunt; activation/fieldspell elig BST; 8 raw refs
.equ ABSOLUTE_END_CID,           0x000017fd  @ Absolute End; activation/fieldspell zone chain; 7 raw refs
.equ RAGING_FLAME_SPRITE_CID,    0x0000182d  @ Raging Flame Sprite; fieldspell BST; 9 raw refs
.equ ASTRAL_BARRIER_CID,         0x00001852  @ Astral Barrier; activation/fieldspell elig; 14 raw refs
.equ SHADOWSLAYER_CID,           0x0000186d  @ Shadowslayer; fieldspell BST; 6 raw refs
.equ UNION_ATTACK_CID,           0x00001890  @ Union Attack; fieldspell chain; 14 raw refs
.equ OVERPOWERING_EYE_CID,       0x00001893  @ Overpowering Eye; fieldspell chain filter; 13 raw refs
.equ HIERACOSPHINX_CID,          0x000018b1  @ Hieracosphinx; activation elig BST; 12 raw refs
.equ GRAVE_OHJA_CID,             0x000018b6  @ Grave Ohja; activation elig; 7 raw refs
.equ EHERO_WILDEDGE_CID,         0x00001958  @ Elemental Hero Wildedge; activation elig BST (distinct from 0x1956=Rampart Blaster); 11 raw refs
.equ FEATHER_SHOT_CID,           0x0000195b  @ Feather Shot; fieldspell chain; 10 raw refs
.equ HAMON_LORD_CID,             0x000019a4  @ Hamon, Lord of Striking Thunder; 13 raw refs
.equ HAMON_LORD_CID_SHIFTED,     0xcd200000  @ HAMON_LORD_CID<<19; slot_word<<19 sentinel check; 6 raw refs

@ =============================================================================
@ file 03 Seg-1 additions: equip node link + slot eligibility card IDs
@ =============================================================================
.equ EHERO_AVIAN_CID,               0x000018a6  @ Elemental Hero Avian (pw=21844576); link_equip_node_by_card_type_check card_type_A; 12 raw refs; data.md Starter/Opp=0x18A6
.equ CHAIN_THRASHER_CID,            0x000019c1  @ Chain Thrasher (pw=88190453); link_equip_node_by_card_type_check card_type_B; 9 raw refs; data.md=0x19C1
.equ ROYAL_COMMAND_CID,             0x0000148e  @ Royal Command (pw=33950246); check_slot_equip_eligibility_by_type BST; 10 raw refs; data.md=0x148E
.equ FIEND_SKULL_DRAGON_CID,        0x000014da  @ Fiend Skull Dragon (pw=66235877); BST; 12 raw refs; data.md=0x14DA
.equ POSSESSED_DARK_SOUL_CID,       0x000014b8  @ Possessed Dark Soul (pw=52860176); BST; 8 raw refs; data.md=0x14B8
.equ SNATCH_STEAL_CID,              0x00001322  @ Snatch Steal (pw=45986603); BST; 20 raw refs; data.md=0x1322
.equ MAGIC_ARM_SHIELD_CID,          0x000012e2  @ Magic-Arm Shield (pw=96008713); BST; 9 raw refs; data.md=0x12E2
.equ CHANGE_OF_HEART_CID,           0x000012fc  @ Change of Heart (pw=04031928); BST; 8 raw refs; data.md=0x12FC
.equ MYSTIC_BOX_CID,                0x00001430  @ Mystic Box (pw=25774450); BST; 100 raw refs; data.md=0x1430
.equ DARK_NECROFEAR_CID,            0x00001466  @ Dark Necrofear (pw=31829185); BST (3 slots); 19 raw refs; data.md=0x1466
.equ BRAIN_JACKER_CID,              0x00001877  @ Brain Jacker (pw=40267580); BST; 10 raw refs; data.md=0x1877
.equ ENEMY_CONTROLLER_CID,          0x00001581  @ Enemy Controller (pw=98045062); BST; 10 raw refs; data.md=0x1581
.equ FALLING_DOWN_CID,              0x0000169a  @ Falling Down (pw=32919136); BST (2 slots); 15 raw refs; data.md=0x169A
.equ OWNER_SEAL_CID,                0x00001857  @ Owner's Seal (pw=09720537); BST; 5 raw refs; data.md=0x1857
.equ RESHEF_THE_DARK_BEING_CID,     0x000018c6  @ Reshef the Dark Being (pw=62420419); BST; 7 raw refs; data.md=0x18C6
.equ CHTHONIAN_POLYMER_CID,         0x0000195d  @ Chthonian Polymer (pw=72287557); BST; 7 raw refs; card-stats.s card_1963 slot=0x195D
.equ CHARMER_RANGE_MAX_CID,         0x000018c2  @ Wynn the Wind Charmer (pw=37744402); range_max of charmer block [0x18BF..0x18C2] (Aussa/Eria/Hiita/Wynn); 7 raw refs; card-stats.s card_1842
.equ ELEMENT_MAGICIAN_CID,          0x00001826  @ Element Magician (pw=65260293); check_slot_field_zone_card_eligible; 12 raw refs; data.md=0x1826
.equ CANNONBALL_SPEAR_SHELLFISH_CID,0x00001709  @ Cannonball Spear Shellfish (pw=95614612); check_slot_card_effect_eligibility whitelist; 7 raw refs; data.md=0x1709
.equ DEEPSEA_WARRIOR_CID,           0x000012a8  @ Deepsea Warrior (pw=24128274); check_slot_card_effect_eligibility whitelist; 9 raw refs; card-stats.s card_0632 slot=0x12A8
.equ HORUS_LV6_CID,                 0x000017d3  @ Horus the Black Flame Dragon LV6 (pw=11224103); check_slot_card_effect_eligibility; 9 raw refs; data.md=0x17D3
.equ HORUS_LV8_CID,                 0x000017d4  @ Horus the Black Flame Dragon LV8 (pw=48229808); check_zone_slot_equip_prerequisites range; 12 raw refs; data.md=0x17D4
.equ HORUS_SERVANT_CID,             0x000017dc  @ Horus' Servant (pw=09264485); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x17DC
.equ SILENT_SWORDSMAN_LV5_CID,      0x00001814  @ Silent Swordsman LV5 (pw=74388798); check_slot_card_effect_eligibility whitelist; 22 raw refs; data.md=0x1814
.equ METALLIZING_PARASITE_CID,      0x00001693  @ Metallizing Parasite - Lunatite (pw=07369217); count_slot_equip_list_matches ref; 9 raw refs; data.md=0x1693
.equ NON_SPELLCASTING_AREA_CID,     0x00001667  @ Non-Spellcasting Area (pw=20065549); count_field_copies_of_card param; 4 raw refs; data.md=0x1667
.equ DUST_BARRIER_CID,              0x000017a1  @ Dust Barrier (pw=31476755); count_available_effect_zones param; 8 raw refs; data.md=0x17A1
.equ EHERO_WILDHEART_CID,           0x0000194e  @ Elemental Hero Wildheart (pw=86188410); check_slot_card_fieldspell_eligibility; 9 raw refs; data.md=0x194E
.equ LORD_OF_D_CID,                 0x0000128b  @ Lord of D. (pw=17985575); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x128B
.equ KING_DRAGUN_CID,               0x00001879  @ King Dragun (pw=13756293); check_zone_slot_equip_prerequisites; 11 raw refs; data.md=0x1879
.equ HEART_OF_CLEAR_WATER_CID,      0x0000150a  @ Heart of Clear Water (pw=64801562); query_zone_chain_count_with_eligibility param; 22 raw refs; data.md=0x150A
.equ TIMIDITY_CID,                  0x0000153c  @ Timidity (pw=40350910); check_slot_card_eligible_for_special_action; 8 raw refs; data.md=0x153C
.equ EXODIA_NECROSS_CID,            0x00001645  @ Exodia Necross (pw=12600382); check_card_equip_eligible_for_slot TYPE_B; 21 raw refs; data.md=0x1645
.equ EQUIP_TYPE_A_CID,              0x0000150c  @ Fusion Sword Murasame Blade (pw=37684215); check_card_equip_eligible_for_slot TYPE_A; 14 raw refs; data.md=0x150C
.equ DARK_MAGICIAN_OF_CHAOS_CID,    0x000016f8  @ Dark Magician of Chaos (pw=40737112); check_slot_card_special_activation_eligible; 17 raw refs; data.md=0x16F8

@ =============================================================================
@ file 03 Seg-2 additions: special action eligibility card IDs
@ =============================================================================
.equ GAP_CID_13EA,              0x000013ea  @ gap slot (not in card-stats.s; range [0x13E8..0x13EB]: Nuvia the Wicked/Soul Exchange); check_slot_card_eligible_for_special_action
.equ KUNAI_WITH_CHAIN_CID,      0x00001231  @ Kunai with Chain (pw=37390589; card_0533 slot=0x1231); check_slot_card_eligible_for_special_action; note: Metalmorph(0x1238=+7) computed inline
.equ BLAST_WITH_CHAIN_CID,      0x00001514  @ Blast with Chain (pw=98239899; card_1086 slot=0x1514); check_slot_card_eligible_for_special_action; note: Hero_Heyro(0x1980=0xcc<<5) computed inline

@ =============================================================================
@ file 03 Seg-3 additions: equip eligibility / field array card IDs
@ =============================================================================
.equ GRADIUS_OPTION_CID,         0x000014fc  @ Gradius' Option (pw=14291024; card-stats.s card_1063 slot=0x14FC); check_zone_slot_equip_eligible special: count_paired_slots_with_field5_default(player,GRADIUS_CID); 8 raw refs; 2 Seg-3 slots
.equ GRADIUS_CID,                0x00001414  @ Gradius (pw=10992251; card-stats.s card_0895 slot=0x1414); paired with GRADIUS_OPTION_CID in check_zone_slot_equip_eligible count_paired path; 6 raw refs; 2 Seg-3 slots
.equ ULTIMATE_OFFERING_CID,      0x000012f3  @ Ultimate Offering (pw=80604091; card-stats.s card_0678 slot=0x12F3); check_value_in_slot_chain guard in check_zone_slot_equip_eligible; 6 raw refs; 2 Seg-3 slots
.equ XYZ_DRAGON_CANNON_CID,      0x000015b4  @ XYZ-Dragon Cannon (pw=91998119; card-stats.s card_1203 slot=0x15B4); range_base in equip-eligible blacklist; 4 raw refs; 1 Seg-3 slot
.equ HELPOEMER_CID,              0x00001571  @ Helpoemer (pw=76052811; card-stats.s card_1148 slot=0x1571); blacklist single-ID in check_zone_slot_equip_eligible; 4 raw refs; 1 Seg-3 slot
.equ SPHINX_TELEIA_CID,          0x000017c8  @ Sphinx Teleia (pw=51402177; card-stats.s card_1623 slot=0x17C8); range_max in [ANDRO_SPHINX 0x17c7, SPHINX_TELEIA 0x17c8] blacklist; 4 raw refs; 1 Seg-3 slot
.equ YZ_TANK_DRAGON_CID,         0x000015fa  @ YZ-Tank Dragon (pw=25119460; card-stats.s card_1254 slot=0x15FA); range_max in [XZ_TANK_CANNON 0x15f9, YZ_TANK_DRAGON 0x15fa] blacklist; 4 raw refs; 1 Seg-3 slot
.equ LEVEL_CONVERSION_LAB_CID,   0x000018d9  @ Level Conversion Lab (pw=84397023; card-stats.s card_1865 slot=0x18D9); check_level_conv_lab_node_match predicate target; 4 raw refs; 1 Seg-3 slot
.equ COST_DOWN_CID,              0x000015c7  @ Cost Down (pw=23265313; card-stats.s card_1213 slot=0x15C7); eval_equip_bonus_for_slot count_slot_chain_nodes_by_card_id arg; 4 raw refs; 1 Seg-3 slot

@ =============================================================================
@ file 03 Seg-4a additions (compute_zone_effect_atk_delta + check_field_effect_zone_activation_eligible)
@ =============================================================================

@ Field-effect zone activation eligibility guard cards
.equ EYE_OF_TRUTH_CID,            0x0000137b  @ The Eye of Truth (pw=34694160; card-stats.s card_0791 slot=0x137b);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x137B
.equ MIND_ON_AIR_CID,             0x000017e7  @ Mind on Air (pw=66690411; card-stats.s card_1652 slot=0x17e7 L21491);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x17E7
.equ RESPECT_PLAY_CID,            0x0000135e  @ Respect Play (pw=08073514; card-stats.s card_0766 slot=0x135e);
                                               @ check_field_effect_zone_activation_eligible gP1LP+0x1ce8 guard;
                                               @ 2 ROM refs; data.md=0x135E

@ ATK delta table card ID range bounds (compute_zone_effect_atk_delta)
.equ YAMI_CID,                    0x000010f5  @ Yami (pw=59197169; card-stats.s card_0297 slot=0x10f5 L3876);
                                               @ lower bound: card_id <= YAMI -> field-spell ATK bonus table path;
                                               @ 2 ROM refs; data.md=0x10F5
.equ MOLTEN_DESTRUCTION_CID,      0x00001346  @ Molten Destruction (pw=19384334; card-stats.s card_0747 slot=0x1346);
                                               @ upper bound of card-dispatch binary-search; card_id > this -> separate branch;
                                               @ 2 ROM refs; data.md=0x1346
.equ GAIA_POWER_CID,              0x00001344  @ Gaia Power (pw=56594520; card-stats.s card_0745 slot=0x1344);
                                               @ compute_zone_effect_atk_delta binary-search node;
                                               @ 2 ROM refs; data.md=0x1344
.equ MYSTIC_PLASMA_ZONE_CID,      0x00001349  @ Mystic Plasma Zone (pw=18161786; card-stats.s card_0750 slot=0x1349);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x1349
.equ NECROVALLEY_CID,             0x0000159d  @ Necrovalley (pw=47355498; card-stats.s card_1185 slot=0x159d);
                                               @ compute_zone_effect_atk_delta gravekeeper-check branch;
                                               @ 2 ROM refs; data.md=0x159D
.equ HARPIES_HUNTING_GROUND_CID,  0x0000183f  @ Harpies' Hunting Ground (pw=75782277; card-stats.s card_1731 slot=0x183f);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x183F

@ =============================================================================
@ file 03 Seg-4b additions: eval_slot_score_entry_full + dispatch_equip_node_by_type cluster
@ =============================================================================

@ Card IDs verified against data/card-stats.s slot= fields (all confidence high)
.equ SKULL_SERVANT_CID,            0x00000fbe  @ Skull Servant (pw=32274490; card_0281 slot=0x0FBE); eval_skull_servant path
.equ DARK_MAGICIAN_CID_0FC9,       0x00000fc9  @ Dark Magician alt print (card_0730 slot=0x0FC9; pw=46986414); distinct from 0x142d
.equ HARPIE_LADY_CID,              0x00000fe4  @ Harpie Lady (pw=76812113; card_0301 slot=0x0FE4); count_paired_slots path
.equ CASTLE_OF_DARK_ILLUSIONS_CID, 0x00000ff9  @ Castle of Dark Illusions (pw=00062986; card_0310 slot=0x0FF9); classify_equip_target_eligibility
.equ PUMPKING_CID,                 0x00001009  @ Pumpking the King of Ghosts (pw=29155212; card_0315 slot=0x1009); eval path
.equ MACHINE_KING_CID,             0x0000113d  @ Machine King (pw=46700124; card_0365 slot=0x113D); eval path
.equ MUKA_MUKA_CID,                0x000011aa  @ Muka Muka (pw=46657337; card_0430 slot=0x11AA); eval path
.equ MAHA_VAILO_CID,               0x00001193  @ Maha Vailo (pw=05798832; card_0420 slot=0x1193); eval path
.equ REVERSE_TRAP_CID,             0x00001257  @ Reverse Trap (pw=77622396; card_0537 slot=0x1257); eval path
.equ MAGICIAN_OF_BLACK_CHAOS_CID,  0x00001278  @ Magician of Black Chaos (pw=30208479; card_0560 slot=0x1278); Dark Magician path
.equ DARK_MAGICIAN_GIRL_CID,       0x0000129e  @ Dark Magician Girl (pw=38033121; card_0584 slot=0x129E); eval path
.equ SHIELD_AND_SWORD_CID,         0x000012cb  @ Shield & Sword (pw=73051941; card_0619 slot=0x12CB); eval path
.equ MIRROR_WALL_CID,              0x00001381  @ Mirror Wall (pw=22359980; card_0704 slot=0x1381); check_slot_equip_chain_rule
.equ AQUA_CHORUS_CID,              0x0000138e  @ Aqua Chorus (pw=95132338; card_0710 slot=0x138E); eval_aqua_chorus path
.equ COMMAND_KNIGHT_CID,           0x00001399  @ Command Knight (pw=10375182; card_0724 slot=0x1399); eval + chain_rule
.equ FLASH_ASSAILANT_CID,          0x00001336  @ Flash Assailant (pw=96890582; card_0648 slot=0x1336); eval path
.equ SLATE_WARRIOR_CID,            0x000013ad  @ Slate Warrior (pw=78636495; card_0726 slot=0x13AD); eval path
.equ NUVIA_THE_WICKED_CID,         0x000013e8  @ Nuvia the Wicked (pw=12953226; card_0745_nuvia slot=0x13E8); eval path
.equ LIGHTNING_BLADE_CID,          0x000013f6  @ Lightning Blade (pw=55226821; card_0752 slot=0x13F6); eval_bonus_state
.equ YELLOW_LUSTER_SHIELD_CID,     0x00001429  @ Yellow Luster Shield (pw=04811901; card_0778 slot=0x1429); eval_bonus_state
.equ DARK_MAGICIAN_CID_142D,       0x0000142d  @ Dark Magician (card_3256 slot=0x142D; pw=46986414 dup); distinct from 0x0fc9
.equ EMBODIMENT_OF_APOPHIS_CID,    0x00001472  @ Embodiment of Apophis (pw=28649820; card_0823 slot=0x1472); eval path
.equ SOUL_OF_PURITY_CID,           0x00001483  @ Soul of Purity and Light (pw=77527210; card_0833 slot=0x1483); eval_bonus_state
.equ ROCK_SPIRIT_CID,              0x00001486  @ The Rock Spirit (pw=04081094; card_0836 slot=0x1486); eval path
.equ THE_A_FORCES_CID,             0x000014cf  @ The A. Forces (pw=00000000; card_0883 slot=0x14CF); eval_command_knight path
.equ MUDORA_CID,                   0x000014ec  @ Mudora (pw=00000000; card_0897 slot=0x14EC); eval path
.equ MASTER_OF_DRAGON_SOLDIER_CID, 0x0000157d  @ Master of Dragon Soldier (pw=00000000; card_1159 slot=0x157D); eval path
.equ BANNER_OF_COURAGE_CID,        0x000015a2  @ Banner of Courage (pw=10012614; card_1185b slot=0x15A2); eval_bonus_state
.equ DARK_PALADIN_CID,             0x000015fc  @ Dark Paladin (pw=98502113; card_1257 slot=0x15FC); eval_dark_paladin path
.equ MAGICAL_MARIONETTE_CID,       0x00001615  @ Magical Marionette (pw=08034697; card_1280 slot=0x1615); eval path
.equ METAL_REFLECT_SLIME_CID,      0x00001636  @ Metal Reflect Slime (pw=26905245; card_1304 slot=0x1636); eval path
.equ GYAKU_GIRE_PANDA_CID,         0x00001651  @ Gyaku-Gire Panda (pw=00000000; card_1328 slot=0x1651); eval path
.equ NIGHTMARE_PENGUIN_CID,        0x000016ab  @ Nightmare Penguin (pw=81306586; card_1400 slot=0x16AB); eval_bonus_state
.equ PERFECT_MACHINE_KING_CID,     0x000016ac  @ Perfect Machine King (pw=00000000; card_1401 slot=0x16AC); eval path
.equ SKULL_ZOMA_CID,               0x0000172f  @ Skull Zoma (pw=00000000; card_1472 slot=0x172F); eval path
.equ AGENT_OF_FORCE_MARS_CID,      0x00001742  @ The Agent of Force - Mars (pw=91123920; card_1488 slot=0x1742); eval path
.equ UNHAPPY_GIRL_CID,             0x00001743  @ The Unhappy Girl (pw=27618832; card_1489 slot=0x1743); classify_equip_target_eligibility
.equ MOKEY_MOKEY_CID,              0x00001782  @ Mokey Mokey (pw=27973334; card_1540 slot=0x1782); eval_mokey_mokey path
.equ THEBAN_NIGHTMARE_CID,         0x00001789  @ Theban Nightmare (pw=00000000; card_1548 slot=0x1789); eval path
.equ ELEMENT_DRAGON_CID,           0x000017e3  @ Element Dragon (pw=00000000; card_1651 slot=0x17E3); eval path
.equ ENRAGED_MUKA_MUKA_CID,        0x000017eb  @ Enraged Muka Muka (pw=01945754; card_1658 slot=0x17EB); eval path
.equ GREEN_GADGET_CID,             0x00001807  @ Green Gadget (pw=67376548; card_1680 slot=0x1807); eval_gadget path
.equ STRONGHOLD_CID,               0x00001809  @ Stronghold (pw=00000000; card_1682 slot=0x1809); eval path
.equ RED_GADGET_CID,               0x0000180b  @ Red Gadget (pw=86445415; card_1684 slot=0x180B); eval_gadget path
.equ YELLOW_GADGET_CID,            0x0000180c  @ Yellow Gadget (pw=13839120; card_1685 slot=0x180C); eval_gadget path
.equ SILENT_MAGICIAN_LV4_CID,      0x00001817  @ Silent Magician LV4 (pw=73752131; card_1697 slot=0x1817); eval path
.equ ULTIMATE_INSECT_LV3_CID,      0x00001822  @ Ultimate Insect LV3 (pw=00000000; card_1710 slot=0x1822); eval_bonus_state
.equ ELEMENT_SAURUS_CID,           0x00001827  @ Element Saurus (pw=00000000; card_1716 slot=0x1827); eval path
.equ MOKEY_MOKEY_SMACKDOWN_CID,    0x00001843  @ Mokey Mokey Smackdown (pw=01784618; card_1741 slot=0x1843); eval_mokey_mokey path
.equ BEHEMOTH_KING_CID,            0x00001864  @ Behemoth the King of All Animals (pw=00000000; card_1764 slot=0x1864); eval path
.equ ULTIMATE_INSECT_LV5_CID,      0x0000185e  @ Ultimate Insect LV5 (pw=00000000; card_1757 slot=0x185E); eval_bonus_state
.equ RED_EYES_DARKNESS_DRAGON_CID, 0x00001894  @ Red-Eyes Darkness Dragon (pw=00000000; card_1801 slot=0x1894); eval path
.equ KING_OF_SKULL_SERVANTS_CID,   0x000018c5  @ King of the Skull Servants (pw=00000000; card_1842 slot=0x18C5); eval path
.equ DORIADO_CID,                  0x000018c7  @ Elemental Mistress Doriado (pw=00000000; card_1843 slot=0x18C7); eval path
.equ BATTERYMAN_AA_CID,            0x000018c3  @ Batteryman AA (pw=63142001; card-stats.s card_1842b slot=0x18C3); shifted sentinel in eval_hand_field6
.equ BATTERYMAN_AA_CID_SHIFTED,    0xc6180000  @ BATTERYMAN_AA_CID<<19 = 0x18c3<<19; slot_word<<19 sentinel; DAT_08038c84
.equ BATTERYMAN_C_CID,             0x0000191c  @ Batteryman C (pw=00000000; card-stats.s card_1913 slot=0x191C); shifted sentinel
.equ BATTERYMAN_C_CID_SHIFTED,     0xc8e00000  @ BATTERYMAN_C_CID<<19 = 0x191c<<19; slot_word<<19 sentinel; DAT_08039128
.equ SANCTUARY_CID_SHIFTED,        0xbaf00000  @ SANCTUARY_IN_THE_SKY_CID(0x175e)<<19; slot_word<<19 sentinel; DAT_08038ae4
.equ DARK_DREADROUTE_CID,          0x00001905  @ Dark Dreadroute (pw=00000000; card_1904 slot=0x1905); check_slot_equip_chain_rule
.equ TADPOLE_CID,                  0x00001919  @ T.A.D.P.O.L.E. (pw=10012614; card_1912 slot=0x1919); eval_extra_deck path
.equ TYRANNO_INFINITY_CID,         0x0000191b  @ Tyranno Infinity (pw=00000000; card_1914 slot=0x191B); eval path
.equ EHERO_SHINING_FLARE_WINGMAN_CID, 0x00001943 @ Elemental Hero Shining Flare Wingman (pw=25366484; card_1939 slot=0x1943); eval path
.equ WATER_DRAGON_CID,             0x00001951  @ Water Dragon (pw=85066822; card_1958 slot=0x1951); check_slot_equip_chain_rule
.equ CYBER_BLADER_CID,             0x00001955  @ Cyber Blader (pw=00000000; card_1962 slot=0x1955); check_slot_equip_chain_rule
.equ MACHINE_KING_PROTOTYPE_CID,   0x000019be  @ Machine King - 3000/8 (pw=00000000; card_1949 slot=0x19BE); eval path
.equ ANCIENT_GEAR_CASTLE_CID,      0x000019b2  @ Ancient Gear Castle (pw=92001300; card_1933 slot=0x19B2); eval_bonus_state
.equ PARASITIC_TICKY_CID,          0x000019c4  @ Parasitic Ticky (pw=00000000; card_1952 slot=0x19C4); eval path
.equ TREEBORN_FROG_CID,            0x000019cb  @ Treeborn Frog (pw=00000000; card_1960 slot=0x19CB); eval_extra_deck path
.equ BEELZE_FROG_CID,              0x000019cc  @ Beelze Frog (pw=00000000; card_1961 slot=0x19CC); eval path
.equ SAND_MOTH_CID,                0x000019d2  @ Sand Moth (pw=00000000; card_1968 slot=0x19D2); eval path
.equ D3S_FROG_CID,                 0x000019d6  @ D.3.S. Frog (pw=00000000; card_1972 slot=0x19D6); eval path
.equ EHERO_ERIKSHIELER_CID,        0x000019ef  @ Elemental Hero Erikshieler (pw=00000000; card_1992 slot=0x19EF); eval path
.equ GREAT_SPIRIT_CID,             0x000019f1  @ Great Spirit (pw=00000000; card_1994 slot=0x19F1); eval path
.equ HELIOS_CID,                   0x000019f6  @ The Ancient Sun Helios (pw=00000000; card_1999 slot=0x19F6); eval_helios path
.equ HELIOS_DUO_MEGISTE_CID,       0x000019f7  @ Helios Duo Megiste (pw=00000000; card_2000 slot=0x19F7); eval_helios path
.equ GOBLIN_KING_CID,              0x00001755  @ Goblin King (pw=18590133; card_1536 slot=0x1755); eval path
.equ SLOT_CARD_EMPTY,              0x0000ffff  @ empty slot sentinel: u16 card_id = 0xffff means no card; eval_slot_empty_sentinel

@ --- file 03 Seg-5 additions (build_equip_target_eligibility_table .. get_zone_slot_ptr) ---
.equ DEMOTION_CID,                 0x000015e3  @ Demotion (pw=72575145; card_1236 slot=0x15E3); eval_equip_chain_score_for_slot
.equ PARASITE_PARACIDE_CID,        0x000012a1  @ Parasite Paracide (pw=27911549; card_0625 slot=0x12A1); query_slot_card_state_code
.equ DNA_SURGERY_CID,              0x00001357  @ DNA Surgery (pw=74701381; card_0760 slot=0x1357); query_slot_card_state_code
.equ D_TRIBE_CID,                  0x000015ae  @ D. Tribe (pw=02833249; card_1199 slot=0x15AE); query_slot_card_state_code
.equ HOMUNCULUS_CID,               0x0000183b  @ Homunculus the Alchemic Being (pw=40410110; card_1727 slot=0x183B); resolve_slot_chain_best_target
.equ SCROLL_OF_BEWITCHMENT_CID,    0x0000145b  @ Scroll of Bewitchment (pw=10352095; card_0927 slot=0x145B); resolve_slot_chain_best_target
.equ DNA_TRANSPLANT_CID,           0x0000171f  @ DNA Transplant (pw=56769674; card_1495 slot=0x171F); base value for shifted sentinel
.equ DNA_TRANSPLANT_CID_SHIFTED,   0xb8f80000  @ DNA_TRANSPLANT_CID(0x171f)<<19; lsls r0,#0x13 then cmp sentinel; resolve_slot_chain_best_target

@ --- file 03 Seg-6 additions (get_zone_slot_entity_ref_by_type .. check_field_spell_neo_daedalus_group_placeable) ---
.equ CHAIN_ENERGY_CID,               0x0000132c  @ Chain Energy (pw=79323590; card_0723 slot=0x132C); LP-threshold gate in check_lp_exceeds_spell_copy_threshold; 1 slot
.equ JUDGEMENT_OF_PHARAOH_CID,       0x00001679  @ Judgement of Pharaoh (pw=55948544; card_1350 slot=0x1679); zone effect node guard (x5 refs); field-spell placement gates
.equ LIGHT_OF_INTERVENTION_CID,      0x0000135d  @ Light of Intervention (pw=62867251; card_0765 slot=0x135D); field-spell group gate in check_field_spell_group_placeable; 1 slot
.equ NON_AGGRESSION_AREA_CID,        0x000015ad  @ Non Aggression Area (pw=76848240; card_1198 slot=0x15AD); zone node block check (x3 refs); placement gates
.equ LAVA_GOLEM_CID,                 0x00001578  @ Lava Golem (pw=00102380; card_1152 slot=0x1578); field-spell placement block (x2 refs)
.equ BOSS_RUSH_CID,                  0x00001972  @ Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate (x2 refs)
.equ JAM_BREEDING_MACHINE_CID,       0x000013ff  @ Jam Breeding Machine (pw=21770260; card_0874 slot=0x13FF); effect zone count gate (x3 refs)
.equ LAST_WARRIOR_FROM_ANOTHER_PLANET_CID, 0x000012b1  @ The Last Warrior from Another Planet (pw=86099788; card_0634 slot=0x12B1); field-spell Last Warrior gate (x3 refs)
.equ JOWGEN_THE_SPIRITUALIST_CID,    0x0000147f  @ Jowgen the Spiritualist (pw=41855169; card_0957 slot=0x147F); Neo Daedalus placement gate; 1 slot

@ --- file 03 Seg-7 additions (eval_equip_placement_full_check .. tick_equip_candidate_scan_with_display) ---
.equ BALLISTA_OF_RAMPART_SMASHING_CID, 0x00001846  @ Ballista of Rampart Smashing (pw=00242146; card_4305 slot=0x1846); tick_equip_chain_link_display_seq chain pool index; 1 slot

@ =============================================================================
@ file 03 Seg-8 additions: equip chain display seq card IDs
@ =============================================================================
.equ BLUE_EYES_WHITE_DRAGON_CID,    0x00000fa7  @ Blue-Eyes White Dragon (pw=89631139; card_0001 slot=0x0FA7); setup_equip_chain_for_slot card_type upper bound
.equ eval_gap_cid_0fa6,             0x00000fa6  @ gap slot (NOT in card-stats.s; between slot 0x0fa5 and card_0001=BEWD); setup_equip_chain_for_slot card_type lower bound; low confidence
.equ A_DEAL_WITH_DARK_RULER_CID,    0x0000165a  @ A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); tick_normal_summon_zone_state link_equip_node_to_chain chain_type arg
.equ eval_gap_cid_11ed,             0x000011ed  @ gap slot (NOT in card-stats.s; between 0x11eb=Takuhee and 0x11ee=Binding Chain); finalize_equip_chain_removal_state sentinel; low confidence

@ =============================================================================
@ file 03 Seg-9 additions: flip-summon / zone-slot display seq card IDs
@ =============================================================================
.equ UNHAPPY_GIRL_CID_SHIFTED,  0xba180000  @ UNHAPPY_GIRL_CID(0x1743)<<19; lsls r0,r0,#0x13; cmp sentinel in tick_flip_summon_state; 1 slot
.equ BACKFIRE_CID,              0x00001762  @ Backfire (pw=82705573; card_1547 slot=0x1762); tick_zone_card_place_with_slot_resolve_seq + tick_equip_node_chain_link_display_seq; 2 slots
.equ SOUL_ABSORPTION_CID,       0x000016da  @ Soul Absorption (pw=68073522; card_1435 slot=0x16DA); same 2 funcs; 2 slots
.equ HUMAN_WAVE_TACTICS_CID,    0x000017b2  @ Human-Wave Tactics (pw=30353551; card_1606 slot=0x17B2); tick_equip_node_chain_link_display_seq; 1 slot

@ =============================================================================
@ file 03 Seg-10 additions: equip detach / zone display seq shifted CID sentinel
@ =============================================================================
.equ HELPOEMER_CID_SHIFTED,     0xab880000  @ HELPOEMER_CID(0x1571)<<19; lsls r1,r0,#0x13; cmp sentinel in tick_zone_slot_equip_detach_display_seq state=0; 1 slot

@ =============================================================================
@ file 04 Seg-4 additions: equip-chain / draw-card display seq card IDs
@ =============================================================================
.equ POLYMERIZATION_CID,            0x000012e5  @ Polymerization (pw=24094653; card_0669 slot=0x12E5); tick_equip_attach_display_sequence equip chain depth table base offset; 1 Seg-4 slot; 27 ROM refs
.equ RYU_SENSHI_CID,                0x000014c7  @ Ryu Senshi (pw=49868263; card_1016 slot=0x14C7); dispatch_equip_chain_slot_scan_by_player BST card_id gate (lower); 1 Seg-4 slot; 13 ROM refs
.equ FRONTIER_WISEMAN_CID,          0x000014ca  @ Frontier Wiseman (pw=38742075; card_1018 slot=0x14CA); dispatch_equip_chain_slot_scan_by_player BST card_id gate + count_available_effect_zones; 2 Seg-4 slots; 8 ROM refs
.equ VICTORY_D_CID,                 0x000016ec  @ Victory D. (pw=44910027; card_1446 slot=0x16EC); tick_draw_card_display_seq zone_ref == VICTORY_D_CID branch; 1 Seg-4 slot; 12 ROM refs
.equ BLUE_EYES_SHINING_DRAGON_CID,  0x000017c2  @ Blue-Eyes Shining Dragon (pw=53347303; card_1617 slot=0x17C2); dispatch_equip_chain_slot_scan_by_player enqueue_field_slot path; 1 Seg-4 slot; 11 ROM refs
.equ RARE_METALMORPH_CID,           0x0000184b  @ Rare Metalmorph (pw=12503902; card_1743 slot=0x184B); dispatch_equip_chain_slot_scan_by_player find_equip_slot + final BST; 2 Seg-4 slots; 17 ROM refs

@ =============================================================================
@ file 04 Seg-5 additions: Gearfried card IDs (enqueue_zone_slot_sprite_attr_by_card_type BST)
@ =============================================================================
.equ GEARFRIED_IRON_KNIGHT_CID,    0x000013c3  @ Gearfried the Iron Knight (pw=00423705; card_0839 slot=0x13C3); BST dispatch in enqueue_zone_slot_sprite_attr_by_card_type; 10 ROM refs
.equ GEARFRIED_SWORDMASTER_CID,    0x0000186b  @ Gearfried the Swordmaster (pw=57046845; card_1772 slot=0x186B); BST dispatch; set_field_slot_bit_with_sprite_update path; 8 ROM refs

@ =============================================================================
@ file 04 Seg-6 additions: equip zone sprite / banisher cluster card IDs
@ =============================================================================
.equ BANISHER_OF_THE_LIGHT_CID,      0x00001332  @ Banisher of the Light (pw=61528025; card_0729 slot=0x1332); dispatch_equip_zone_sprite_banisher_* cluster; 6 Seg-6 slots
.equ GRAVEROBBER_CID,                0x00001379  @ Graverobber (pw=61705417; card_0789 slot=0x1379); dispatch_equip_zone_sprite_and_activation + render_equip_zone_sprite_with_chain_lp; 2 Seg-6 slots
.equ SUPER_REJUVENATION_CID,         0x000014e2  @ Super Rejuvenation (pw=27770341; card_1042 slot=0x14E2); dispatch_equip_zone_sprite_and_activation + dispatch_equip_zone_sprite_banisher_with_spell_check; 2 Seg-6 slots
.equ SAMSARA_CID,                    0x000019da  @ Samsara (pw=44182827; card_2061 slot=0x19DA); dispatch_equip_zone_sprite_banisher_with_spell_check second-card check; 1 slot
.equ CRASS_CLOWN_CID,                0x00001005  @ Crass Clown (pw=93889755; card_0101 slot=0x1005); apply_slot_equip_activation_with_sprite branch A; 1 slot
.equ BLADE_RABBIT_CID,               0x00001868  @ Blade Rabbit (pw=58268433; card_1769 slot=0x1868); apply_slot_equip_activation_with_sprite branch D; 1 slot
.equ AMEBA_CID,                      0x0000118a  @ Ameba (pw=95174353; card_0407 slot=0x118A); scan_equip_chain_list_for_activation_sprite equip activation range base (0x118a..0x11c9); 1 slot; 28 raw ROM refs
.equ MANTICORE_OF_DARKNESS_CID,      0x000016f9  @ Manticore of Darkness (pw=77121851; card_1458 slot=0x16F9); dispatch_equip_zone_sprite_and_activation BST root; 1 slot
.equ ARCHFIEND_OF_GILFER_CID,        0x000013e3  @ Archfiend of Gilfer (pw=50287060; card_0853 slot=0x13E3); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ MINAR_CID,                      0x000011bc  @ Minar (pw=32539892; card_0444 slot=0x11BC); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ SKULL_MARK_LADYBUG_CID,         0x000012a2  @ Skull-Mark Ladybug (pw=64306248; card_0626 slot=0x12A2); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ MAKYURA_THE_DESTRUCTOR_CID,     0x000014a5  @ Makyura the Destructor (pw=21593977; card_0991 slot=0x14A5); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ DESPAIR_FROM_THE_DARK_CID,      0x00001653  @ Despair from the Dark (pw=71200730; card_1323 slot=0x1653); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ FEAR_FROM_THE_DARK_CID,         0x00001655  @ Fear from the Dark (pw=34193084; card_1325 slot=0x1655); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ OUTSTANDING_DOG_MARRON_CID,     0x00001687  @ Outstanding Dog Marron (pw=11548522; card_1364 slot=0x1687); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ ROC_FROM_THE_VALLEY_OF_HAZE_CID, 0x00001828 @ Roc from the Valley of Haze (pw=28143906; card_1708 slot=0x1828); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ NIGHT_ASSAILANT_CID,            0x0000179a  @ Night Assailant (pw=16226786; card_1585 slot=0x179A); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ BROWW_HUNTSMAN_OF_DARK_WORLD_CID, 0x00001966 @ Broww, Huntsman of Dark World (pw=79126789; card_1972 slot=0x1966); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ SILLVA_WARLORD_OF_DARK_WORLD_CID, 0x00001968 @ Sillva, Warlord of Dark World (pw=32619583; card_1974 slot=0x1968); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ EKIBYO_DRAKMORD_CID_SHIFTED,    0xa4e80000  @ EKIBYO_DRAKMORD_CID(0x149d)<<19; scan_equip_chain_list_for_activation_sprite type-match sentinel; 1 raw ROM ref
@ (card_0987: Ekibyo Drakmord pw=69954399; 0xa4e80000>>19=0x149d; card-stats.s verified)
.equ act_cid_1048_08043b48,          0x00001048  @ card_id branch B in apply_slot_equip_activation_with_sprite; NOT in card-stats.s -> neutral name; 1 slot
.equ act_cid_1197_08043be8,          0x00001197  @ card_id branch C in apply_slot_equip_activation_with_sprite; NOT in card-stats.s -> neutral name; 1 slot

@ =============================================================================
@ file 04 Seg-7 additions: Watapon / Dark Mimic LV1 card IDs
@ =============================================================================
.equ WATAPON_CID,                    0x000017cc  @ Watapon (pw=87774234; card-stats.s card_1626 slot=0x17CC); enqueue_hand_sprite_by_zone_set_code Watapon-path; 10 raw ROM refs
.equ WATAPON_EQUIP_ACTIVATION_MASK,  0x34500000  @ activation flag mask ORed into attr2 arg of apply_equip_activation_with_id_lookup for Watapon path in enqueue_hand_sprite_by_zone_set_code; 24 raw ROM refs
.equ DARK_MIMIC_LV1_CID,             0x000017d5  @ Dark Mimic LV1 (pw=74713516; card-stats.s card_1635 slot=0x17D5); enqueue_equip_chain_sprite_attrs_for_slot card_type filter A; 16 raw ROM refs

@ =============================================================================
@ file 04 Seg-8a additions: card IDs for dispatch_card_effect_sprite_render_by_card_id BST
@   + equip chain activation eligibility cluster (update_duel_field_slot_sprite_state etc.)
@ Values confirmed via data/card-stats.s slot=0xXXXX pattern; 4 gap stubs (*_cid_* names).
@ =============================================================================
.equ SANGAN_CID,                       0x00000fd6  @ Sangan (pw=26202165; card-stats.s slot=0x0fd6)
.equ upd_cid_10c6,                     0x000010c6  @ card gap; no card-stats entry; neutral name
.equ BLACK_PENDANT_CID,                0x000010dd  @ Black Pendant (pw=65169794; card-stats.s slot=0x10dd)
@ UMI_CARD_ID = 0x000010f4 already in card_info.inc -- REUSE
.equ GODDESS_OF_WHIM_CID,              0x00001153  @ Goddess of Whim (pw=67959180; card-stats.s slot=0x1153)
.equ COCKROACH_KNIGHT_CID,             0x00001185  @ Cockroach Knight (pw=33413638; card-stats.s slot=0x1185)
.equ WITCH_OF_THE_BLACK_FOREST_CID,    0x000011e4  @ Witch of the Black Forest (pw=78010363; card-stats.s slot=0x11e4)
.equ upd_cid_120e,                     0x0000120e  @ card gap; no card-stats entry; neutral name
.equ JINZO_CID,                        0x00001296  @ Jinzo (pw=77585513; card-stats.s slot=0x1296)
.equ SATELLITE_CANNON_CID,             0x000012ac  @ Satellite Cannon (pw=50400231; card-stats.s slot=0x12ac)
.equ COPYCAT_CID,                      0x000012bb  @ Copycat (pw=26376390; card-stats.s slot=0x12bb)
.equ GIANT_RAT_CID,                    0x00001333  @ Giant Rat (pw=97017120; card-stats.s slot=0x1333)
.equ KARATE_MAN_CID,                   0x00001337  @ Karate Man (pw=23289281; card-stats.s slot=0x1337)
.equ GIANT_GERM_CID,                   0x00001339  @ Giant Germ (pw=95178994; card-stats.s slot=0x1339); fn_activate handler dispatch_germ_momonga_trigger_display_by_state; shared with Nimble Momonga (0x133a) for summon-from-deck trigger
.equ NIMBLE_MOMONGA_CID,               0x0000133a  @ Nimble Momonga (pw=22567609; card-stats.s slot=0x133a)
.equ SHINING_ANGEL_CID,                0x0000133c  @ Shining Angel (pw=95956346; card-stats.s slot=0x133c)
.equ MYSTIC_TOMATO_CID,                0x00001342  @ Mystic Tomato (pw=83011277; card-stats.s slot=0x1342)
@ SPELL_ZONE_TARGET_CARD_ID = 0x00001368 already in card_info.inc -- REUSE
.equ MUCUS_YOLK_CID,                   0x000013b2  @ Mucus Yolk (pw=70307656; card-stats.s slot=0x13b2)
.equ upd_cid_13e9,                     0x000013e9  @ card gap; no card-stats entry; neutral name
.equ TORNADO_WALL_CID,                 0x000013f7  @ Tornado Wall (pw=18605135; card-stats.s slot=0x13f7)
@ ZOMBYRA_THE_DARK_CID = 0x0000147d already in card_info.inc -- REUSE
.equ THE_EMPERORS_HOLIDAY_CID,         0x00001495  @ The Emperor's Holiday (pw=68400115; card-stats.s slot=0x1495)
.equ AMAZONESS_CHAIN_MASTER_CID,       0x000014ab  @ Amazoness Chain Master (pw=29654737; card-stats.s slot=0x14ab)
.equ AGIDO_CID,                        0x000014f6  @ Agido (pw=16135253; card-stats.s slot=0x14f6)
.equ DARK_COFFIN_CID,                  0x00001544  @ Dark Coffin (pw=01804528; card-stats.s slot=0x1544)
.equ LORD_POISON_CID,                  0x0000156d  @ Lord Poison (pw=40320754; card-stats.s slot=0x156d)
.equ YOMI_SHIP_CID,                    0x00001591  @ Yomi Ship (pw=51534754; card-stats.s slot=0x1591)
.equ COBRA_JAR_CID,                    0x00001595  @ Cobra Jar (pw=86801871; card-stats.s slot=0x1595)
.equ GRANADORA_CID,                    0x0000163f  @ Granadora (pw=13944422; card-stats.s slot=0x163f)
.equ OJAMA_TRIO_CID,                   0x0000166a  @ Ojama Trio (pw=29843091; card-stats.s slot=0x166a)
.equ upd_cid_1672,                     0x00001672  @ card gap; no card-stats entry; neutral name
.equ GREAT_MAJU_GARZETT_CID,           0x00001688  @ Great Maju Garzett (pw=47942531; card-stats.s slot=0x1688)
.equ PANDEMONIUM_CID,                  0x0000169f  @ Pandemonium (pw=94585852; card-stats.s slot=0x169f)
.equ SILPHEED_CID,                     0x000016c8  @ Silpheed (pw=73001017; card-stats.s slot=0x16c8)
.equ FUHMA_SHURIKEN_CID,               0x000016cc  @ Fuhma Shuriken (pw=09373534; card-stats.s slot=0x16cc)
.equ TOWER_OF_BABEL_CID,               0x000016de  @ Tower of Babel (pw=94256039; card-stats.s slot=0x16de)
.equ BURNING_ALGAE_CID,                0x000016f5  @ Burning Algae (pw=41859700; card-stats.s slot=0x16f5)
.equ ABYSS_SOLDIER_CID,                0x00001727  @ Abyss Soldier (pw=18318842; card-stats.s slot=0x1727); check_field_sarcophagus_range_and_banisher_count CID filter; 1 Seg-8 slot; conf: high
.equ EMES_THE_INFINITY_CID,            0x0000172b  @ Emes the Infinity (pw=43580269; card-stats.s slot=0x172b)
.equ EMISSARY_OF_THE_AFTERLIFE_CID,    0x00001796  @ Emissary of the Afterlife (pw=75043725; card-stats.s slot=0x1796)
.equ FAMILIAR_KNIGHT_CID,              0x000017c3  @ Familiar Knight (pw=89731911; card-stats.s slot=0x17c3)
.equ MASKED_DRAGON_CID,                0x000017e6  @ Masked Dragon (pw=39191307; card-stats.s slot=0x17e6)
.equ NINJITSU_ART_OF_DECOY_CID,        0x000017ff  @ Ninjitsu Art of Decoy (pw=89628781; card-stats.s slot=0x17ff)
.equ SILENT_MAGICIAN_LV8_CID,          0x0000181a  @ Silent Magician LV8 (pw=72443568; card-stats.s slot=0x181a)
@ RAGING_FLAME_SPRITE_CID = 0x0000182d already in card_info.inc -- REUSE
.equ GAIA_SOUL_CID,                    0x00001835  @ Gaia Soul the Combustible Collective (pw=51355346; card-stats.s slot=0x1835)
.equ MOKEY_MOKEY_KING_CID,             0x0000183d  @ Mokey Mokey King (pw=13803864; card-stats.s slot=0x183d)
.equ NECKLACE_OF_COMMAND_CID,          0x00001841  @ Necklace of Command (pw=48576971; card-stats.s slot=0x1841)
.equ XING_ZHEN_HU_CID,                 0x0000184a  @ Xing Zhen Hu (pw=76515293; card-stats.s slot=0x184a)
.equ SACRED_PHOENIX_CID,               0x0000185c  @ Sacred Phoenix of Nephthys (pw=61441708; card-stats.s slot=0x185c)
.equ MECHA_DOG_MARRON_CID,             0x00001869  @ Mecha-Dog Marron (pw=94667532; card-stats.s slot=0x1869)
.equ FIREBIRD_CID,                     0x00001875  @ Firebird (pw=87473172; card-stats.s slot=0x1875)
.equ CENTRIFUGAL_FIELD_CID,            0x0000187f  @ Centrifugal Field (pw=01801154; card-stats.s slot=0x187f)
.equ MILLENNIUM_SCORPION_CID,          0x000018ae  @ Millennium Scorpion (pw=82482194; card-stats.s slot=0x18ae)
.equ CRIOSPHINX_CID,                   0x000018b2  @ Criosphinx (pw=18654201; card-stats.s slot=0x18b2)
.equ MEGAROCK_DRAGON_CID,              0x000018b4  @ Megarock Dragon (pw=71544954; card-stats.s slot=0x18b4)
.equ DD_SURVIVOR_CID,                  0x000018bc  @ D.D. Survivor (pw=48092532; card-stats.s slot=0x18bc)
.equ NITRO_UNIT_CID,                   0x000018d1  @ Nitro Unit (pw=23842445; card-stats.s slot=0x18d1)
.equ KOZAKYS_SELF_DESTRUCT_CID,        0x000018d7  @ Kozaky's Self-Destruct Button (pw=21908319; card-stats.s slot=0x18d7)
.equ UFOROID_CID,                      0x000018f4  @ UFOroid (pw=07602840; card-stats.s slot=0x18f4)
.equ UFOROID_FIGHTER_CID,              0x000018fb  @ UFOroid Fighter (pw=32752319; card-stats.s slot=0x18fb)
.equ GIANT_KOZAKY_CID,                 0x00001914  @ Giant Kozaky (pw=58185394; card-stats.s slot=0x1914)
.equ OJAMAGIC_CID,                     0x00001946  @ Ojamagic (pw=24643836; card-stats.s slot=0x1946)
.equ WHITE_HORNS_DRAGON_CID,           0x00001996  @ White Horns Dragon (pw=73891874; card-stats.s slot=0x1996)
.equ RAVIEL_LORD_CID,                  0x000019a5  @ Raviel, Lord of Phantasms (pw=69890967; card-stats.s slot=0x19a5)
.equ GOKIPON_CID,                      0x000019c5  @ Gokipon (pw=14472500; card-stats.s slot=0x19c5)
.equ HELIOS_TRIS_MEGISTE_CID,          0x000019f8  @ Helios Tris Megiste (pw=17286057; card-stats.s slot=0x19f8)
.equ VAMPIRE_LORD_CID,                 0x00001522  @ Vampire Lord (pw=53839837; card-stats.s slot=0x1522)
.equ ROYAL_KEEPER_CID,                 0x00001527  @ Royal Keeper (pw=16509093; card-stats.s slot=0x1527)
.equ EXARION_UNIVERSE_CID,             0x0000154c  @ Exarion Universe (pw=63749102; card-stats.s slot=0x154c)
.equ MAJI_GIRE_PANDA_CID,              0x00001862  @ Maji-Gire Panda (pw=60102563; card-stats.s slot=0x1862)

@ =============================================================================
@ file 04 Seg-8b additions: equip target eligibility / zone action CIDs
@ =============================================================================
.equ PANDEMONIUM_WATCHBEAR_CID,        0x00001683  @ Pandemonium Watchbear (pw=75375465; card-stats.s slot=0x1683)
.equ HEAVY_MECH_SUPPORT_PLATFORM_CID, 0x00001825  @ Heavy Mech Support Platform (pw=23265594; card-stats.s slot=0x1825)
.equ AUTONOMOUS_ACTION_UNIT_CID,      0x000015e6  @ Autonomous Action Unit (pw=71453557; card-stats.s slot=0x15e6)
.equ CALL_OF_THE_HAUNTED_CID,         0x0000137d  @ Call of the Haunted (pw=97077563; card-stats.s slot=0x137d)
.equ PREMATURE_BURIAL_CID,            0x00001366  @ Premature Burial (pw=70828912; card-stats.s slot=0x1366)
.equ SPIRIT_MESSAGE_L_CID,            0x0000149a  @ Spirit Message L (pw=30170981; card-stats.s slot=0x149a)
.equ SPIRITUAL_ENERGY_SETTLE_CID,     0x0000150e  @ Spiritual Energy Settle Machine (pw=99173029; card-stats.s slot=0x150e)
.equ THE_FIRST_SARCOPHAGUS_CID,       0x000017af  @ The First Sarcophagus (pw=31076103; card-stats.s slot=0x17af)
.equ THE_THIRD_SARCOPHAGUS_CID,       0x000017ad  @ The Third Sarcophagus (pw=78697395; card-stats.s slot=0x17ad)
.equ BATTLE_SCARRED_CID,              0x000016a2  @ Battle-Scarred (pw=94463200; card-stats.s slot=0x16a2)
.equ NINJITSU_ART_OF_TRANSFORMATION_CID, 0x00001768  @ Ninjitsu Art of Transformation (pw=70861343; card-stats.s slot=0x1768)
.equ RE_FUSION_CID,                   0x00001881  @ Re-Fusion (pw=74694807; card-stats.s slot=0x1881)
.equ SYMBOL_OF_HERITAGE_CID,          0x000019d7  @ Symbol of Heritage (pw=45305419; card-stats.s slot=0x19d7)
.equ BIG_BANG_SHOT_CID,               0x00001625  @ Big Bang Shot (pw=61127349; card-stats.s slot=0x1625)
.equ DESTINY_BOARD_CID,               0x00001468  @ Destiny Board (pw=94212438; card-stats.s slot=0x1468)
.equ AMPLIFIER_CID,                   0x000012d3  @ Amplifier (pw=00303660; card-stats.s slot=0x12d3)
.equ SOUL_RESURRECTION_CID,           0x000017b7  @ Soul Resurrection (pw=92924317; card-stats.s slot=0x17b7)
.equ FIBER_JAR_CID,                   0x000014fb  @ Fiber Jar (pw=78706415; card-stats.s slot=0x14fb)
.equ GOBLIN_OUT_OF_FRYING_PAN_CID,    0x000019e1  @ Goblin Out of the Frying Pan (pw=69632396; card-stats.s slot=0x19e1)

@ =============================================================================
@ file 04 Seg-10 additions: setup_equip_slot_sprite_attr_by_card + submit_lp_change_indicator dispatch
@ =============================================================================
.equ WHITE_MAGICAL_HAT_CID,          0x00001018  @ White Magical Hat (pw=15150365; card_0117); setup_equip_slot_sprite_attr_by_card dispatch
.equ MASKED_SORCERER_CID,            0x00001082  @ Masked Sorcerer (pw=10189126; card_0208); setup_equip_slot_sprite_attr_by_card dispatch
.equ BISTRO_BUTCHER_CID,             0x000011b1  @ The Bistro Butcher (pw=71107816; card_0436); setup_equip_slot_sprite_attr_by_card dispatch
.equ RELINQUISHED_CID,               0x00001281  @ Relinquished (pw=64631466; card_0592); setup_equip_slot_sprite_attr_by_card dispatch
.equ DRILL_BUG_CID,                  0x000012a7  @ Drill Bug (pw=88733579; card_0631); setup_equip_slot_sprite_attr_by_card dispatch
.equ ROBBINS_GOBLIN_CID,             0x0000130c  @ Robbin' Goblin (pw=88279736; card_0696); setup_equip_slot_sprite_attr_by_card dispatch
.equ CESTUS_OF_DAGLA_CID,            0x000014ed  @ Cestus of Dagla (pw=28106077; card_1053); setup_equip_slot_sprite_attr_by_card dispatch
.equ SECRET_OF_THE_BANDIT_CID,       0x00001511  @ The Secret of the Bandit (pw=99351431; card_1084); setup_equip_slot_sprite_attr_by_card dispatch
.equ DON_ZALOOG_CID,                 0x00001532  @ Don Zaloog (pw=76922029; card_1111); setup_equip_slot_sprite_attr_by_card dispatch
.equ TOON_MASKED_SORCERER_CID,       0x00001563  @ Toon Masked Sorcerer (pw=16392422; card_1139); setup_equip_slot_sprite_attr_by_card dispatch
.equ DARK_ROOM_OF_NIGHTMARE_CID,     0x0000159b  @ Dark Room of Nightmare (pw=85562745; card_1183); submit_lp_change_indicator_with_chain_check LP display gate
.equ FREEZING_BEAST_CID,             0x000015d7  @ Freezing Beast (pw=85359414; card_1227); setup_equip_slot_sprite_attr_by_card dispatch
.equ equip_cid_15de_08048a68,        0x000015de  @ slot_id 0x15de: no match in card-stats.s; setup_equip_slot_sprite_attr_by_card dispatch; conf low
.equ MEFIST_THE_INFERNAL_GENERAL_CID,0x0000168b  @ Mefist the Infernal General (pw=46820049; card_1367); setup_equip_slot_sprite_attr_by_card dispatch
.equ SASUKE_SAMURAI_3_CID,           0x000016bd  @ Sasuke Samurai #3 (pw=77379481; card_1408); setup_equip_slot_sprite_attr_by_card dispatch
.equ VAMPIRE_LADY_CID,               0x00001746  @ Vampire Lady (pw=26495087; card_1521); setup_equip_slot_sprite_attr_by_card dispatch
.equ DES_COUNTERBLOW_CID,            0x000017b5  @ Des Counterblow (pw=39131963; card_1609); setup_equip_slot_sprite_attr_by_card dispatch
.equ HALLOWED_LIFE_BARRIER_CID,      0x00001805  @ Hallowed Life Barrier (pw=88789641; card_1681); submit_lp_change_indicator_with_chain_check chain check gate A
.equ DARK_BLADE_THE_DRAGON_KNIGHT_CID,0x0000183c @ Dark Blade the Dragon Knight (pw=86805855; card_1728); setup_equip_slot_sprite_attr_by_card dispatch
.equ PIKERUS_CIRCLE_OF_ENCHANTMENT_CID,0x00001850 @ Pikeru's Circle of Enchantment (pw=74270067; card_1747); submit_lp_change_indicator_with_chain_check chain check gate B
.equ POISON_FANGS_CID,               0x0000187b  @ Poison Fangs (pw=76539047; card_1788); setup_equip_slot_sprite_attr_by_card dispatch
.equ SPIRAL_SPEAR_STRIKE_CID,        0x0000187d  @ Spiral Spear Strike (pw=49328340; card_1790); setup_equip_slot_sprite_attr_by_card dispatch
.equ DES_WOMBAT_CID,                 0x000018c4  @ Des Wombat (pw=09637706; card_1844); submit_lp_change_indicator_with_chain_check effect zone key
.equ BRRON_MAD_KING_OF_DARK_WORLD_CID,0x00001967 @ Brron, Mad King of Dark World (pw=06214884; card_1973); setup_equip_slot_sprite_attr_by_card dispatch
.equ DOOM_DOZER_CID,                 0x000019ca  @ Doom Dozer (pw=76039636; card_2045); setup_equip_slot_sprite_attr_by_card dispatch
.equ BEGONE_KNAVE_CID,               0x0000171e  @ Begone, Knave! (pw=20374520; card_1494); setup_equip_slot_sprite_attr_by_card dispatch

@ =============================================================================
@ file 05 Seg-1 additions: equip slot sprite + LP/shape sprite dispatch card IDs
@ Source: asm/05_equip_eligibility_a.s, Seg-1 (0x08049014..0x0804a5b8)
@ =============================================================================
.equ PENGUIN_KNIGHT_CID,              0x0000106d  @ Penguin Knight         (pw=36039163)
.equ BAD_REACTION_TO_SIMOCHI_CID,     0x00001256  @ Bad Reaction to Simochi (pw=40633297)
.equ HIROS_SHADOW_SCOUT_CID,          0x00001209  @ Hiro's Shadow Scout     (pw=81863068)
.equ CRUSH_CARD_CID,                  0x0000123b  @ Crush Card              (pw=57728570)
.equ APPROPRIATE_CID,                 0x00001353  @ Appropriate             (pw=48539234)
.equ PROTECTOR_OF_THE_SANCTUARY_CID,  0x0000178b  @ Protector of the Sanctuary (pw=24221739)
.equ HEART_OF_THE_UNDERDOG_CID,       0x000016cd  @ Heart of the Underdog   (pw=35762283)
.equ REGENERATING_MUMMY_CID,          0x00001799  @ Regenerating Mummy      (pw=70821187)
.equ GREED_CID,                       0x00001802  @ Greed                   (pw=89405199)
.equ PETEN_THE_DARK_CLOWN_CID,        0x000017c5  @ Peten the Dark Clown    (pw=52624755)
.equ DECK_DEVASTATION_VIRUS_CID,      0x0000188c  @ Deck Devastation Virus  (pw=35027493)
.equ PIKERU_SECOND_SIGHT_CID,         0x000018d5  @ Pikeru's Second Sight   (pw=58015506)
.equ CYBER_ARCHFIEND_CID,             0x00001911  @ Cyber Archfiend         (pw=59907935)
.equ BUBBLE_ILLUSION_CID,             0x0000198a  @ Bubble Illusion         (pw=80075749)
.equ DANDYLION_CID,                   0x000019fe  @ Dandylion               (pw=15341821)
.equ KAISER_GLIDER_CID,               0x000014e9  @ Kaiser Glider           (pw=52824910)

@ =============================================================================
@ file 05 Seg-2 additions: card IDs for Harpie/Polymerization/BEWD pair checks
@ Source: asm/05_equip_eligibility_a.s, Seg-2 (0x0804a5b8..0x0804ad48)
@ check_card_pair_allowed / map_card_id_to_banlist_canonical / check_card_ids_banlist_compatible
@ =============================================================================
.equ POLYMERIZATION_CID_1303,  0x00001303  @ Polymerization 2nd print (pw=24094653; card_0689 slot=0x1303); pair/fusion whitelist check_card_pair_allowed; 13 raw ROM refs
.equ CYBER_HARPIE_LADY_CID,    0x00001477  @ Cyber Harpie Lady (pw=80316585; card_0951 slot=0x1477); Harpie pair whitelist (interchangeable w/ HARPIE_LADY_CID 0xfe4 group); 9 raw ROM refs
.equ HARPIE_LADY_1_CID,        0x0000182a  @ Harpie Lady 1 (pw=91932350; card_1710 slot=0x182A); Harpie pair whitelist target (equivalent group with HARPIE_LADY_CID + CYBER_HARPIE_LADY_CID); 7 raw ROM refs
.equ HARPIE_LADY_3_CID,        0x0000182c  @ Harpie Lady 3 (pw=54415063; card_1712 slot=0x182C); Harpie pair whitelist target; 12 raw ROM refs
.equ BEWD_RANGE_CHECK_BIAS,    0xfffff05a  @ range-check bias -0xfa6: adds r0,r1,bias; cmp r0,#1; bhi -> tests if r1 in {0xfa6,0xfa7} (BEWD/gap range); check_card_pair_allowed + check_card_ids_banlist_compatible; 2 raw ROM refs

@ =============================================================================
@ file 05 Seg-3 additions: card field/type queries + summon restriction + evolution IDs
@ Source: asm/05_equip_eligibility_a.s, Seg-3 (0x0804ad48..0x0804b4f4)
@ check_card_is_archfiend/gravekeeper/amazoness/ninja/guardian/dark_scorpion/batteryman/
@   dark_world_range_type + effect_monster_b/c/bes/special_summon types +
@   fusion_target_range + get_card_evolution_target_ids
@ =============================================================================
@ -- main-segment EQ (40 new CIDs) --
.equ B_SKULL_DRAGON_CID,               0x0000107f  @ B. Skull Dragon (pw=11901678; card_0205)
.equ WICKED_MIRROR_CID,                0x000010ab  @ Wicked Mirror (pw=15150371; card_0246)
.equ AXE_OF_DESPAIR_CID,               0x000010d6  @ Axe of Despair (pw=40619825; card_0283)
.equ ARMED_NINJA_CID,                  0x0000117b  @ Armed Ninja (pw=09076207; card_0395)
.equ TOON_SUMMONED_SKULL_CID,          0x0000127f  @ Toon Summoned Skull (pw=91842653; card_0591)
.equ BEAST_OF_TALWAR_CID,              0x000012b5  @ Beast of Talwar (pw=11761845; card_0638)
.equ GRAVEKEEPERS_SERVANT_CID,         0x0000131d  @ Gravekeeper's Servant (pw=16762927; card_0710)
.equ AMAZONESS_ARCHERS_CID,            0x000014a6  @ Amazoness Archers (pw=67987611; card_0992)
.equ AMAZONESS_FIGHTER_CID,            0x000014af  @ Amazoness Fighter (pw=55821894; card_0998)
.equ LESSER_FIEND_CID,                 0x000014b7  @ Lesser Fiend (pw=16475472; card_1003)
.equ GUARDIAN_SPHINX_CID,              0x0000152e  @ Guardian Sphinx (pw=40659562; card_1107)
.equ GRAVEKEEPERS_CANNONHOLDER_CID,    0x0000158c  @ Gravekeeper's Cannonholder (pw=99877698; card_1168)
.equ GRAVEKEEPERS_ASSAILANT_CID,       0x0000158d  @ Gravekeeper's Assailant (pw=25262697; card_1169)
.equ OJAMA_GREEN_CID,                  0x00001681  @ Ojama Green (pw=12482652; card_1358)
.equ SKULL_ARCHFIEND_OF_LIGHTNING_CID, 0x00001692  @ Skull Archfiend of Lightning (pw=61370518; card_1374)
.equ OJAMA_BLACK_CID,                  0x000016b4  @ Ojama Black (pw=79335209; card_1400)
.equ STRIKE_NINJA_CID,                 0x000016b9  @ Strike Ninja (pw=41006930; card_1405)
.equ OJAMA_DELTA_HURRICANE_CID,        0x000016cf  @ Ojama Delta Hurricane!! (pw=08251996; card_1425)
.equ THEINEN_THE_GREAT_SPHINX_CID,     0x000017c9  @ Theinen the Great Sphinx (pw=87997872; card_1624)
.equ ULTIMATE_INSECT_LV1_CID,          0x000017d1  @ Ultimate Insect LV1 (pw=49441499; card_1631)
.equ HORUS_LV4_CID,                    0x000017d2  @ Horus the Black Flame Dragon LV4 (pw=75830094; card_1632)
.equ DARK_MIMIC_LV3_CID,               0x000017d6  @ Dark Mimic LV3 (pw=01102515; card_1636)
.equ MYSTIC_SWORDSMAN_LV2_CID,         0x000017d7  @ Mystic Swordsman LV2 (pw=47507260; card_1637)
.equ MYSTIC_SWORDSMAN_LV4_CID,         0x000017d8  @ Mystic Swordsman LV4 (pw=74591968; card_1638)
.equ ARMED_DRAGON_LV5_CID,             0x000017da  @ Armed Dragon LV5 (pw=46384672; card_1640)
.equ ARMED_DRAGON_LV7_CID,             0x000017db  @ Armed Dragon LV7 (pw=73879377; card_1641)
.equ NINJA_GRANDMASTER_SASUKE_CID,     0x000017df  @ Ninja Grandmaster Sasuke (pw=04041838; card_1644)
.equ SILENT_SWORDSMAN_LV3_CID,         0x00001812  @ Silent Swordsman LV3 (pw=01995985; card_1690)
.equ SILENT_SWORDSMAN_LV7_CID,         0x00001816  @ Silent Swordsman LV7 (pw=37267041; card_1692)
.equ MYSTIC_SWORDSMAN_LV6_CID,         0x00001823  @ Mystic Swordsman LV6 (pw=60482781; card_1704)
.equ ANCIENT_GEAR_GOLEM_CID,           0x000018ab  @ Ancient Gear Golem (pw=83104731; card_1819)
.equ ULTIMATE_INSECT_LV7_CID,          0x000018af  @ Ultimate Insect LV7 (pw=19877898; card_1823)
.equ WHITE_NINJA_CID,                  0x000018be  @ White Ninja (pw=01571945; card_1838)
.equ EHERO_BUBBLEMAN_CID,              0x000018f9  @ Elemental Hero Bubbleman (pw=79979666; card_1882)
.equ WINGED_KURIBOH_LV10_CID,          0x00001906  @ Winged Kuriboh LV10 (pw=98585345; card_1891)
.equ BES_CRYSTAL_CORE_CID,             0x00001913  @ B.E.S. Crystal Core (pw=22790789; card_1904)
.equ BES_TETRAN_CID,                   0x00001962  @ B.E.S. Tetran (pw=44954628; card_1968)
.equ EHERO_MADBALLMAN_CID,             0x00001981  @ Elemental Hero Madballman (pw=52031567; card_1996)
.equ ARMED_DRAGON_LV10_CID,            0x0000198c  @ Armed Dragon LV10 (pw=59464593; card_2005)
.equ EHERO_NEO_BUBBLEMAN_CID,          0x000019a6  @ Elemental Hero Neo Bubbleman (pw=05285665; card_2015)
.equ ANCIENT_GEAR_DRILL_CID,           0x000019ae  @ Ancient Gear Drill (pw=67829249; card_2022)
@ -- disasm-block EQ (11 new CIDs; 4 existing reused) --
.equ TOON_ALLIGATOR_CID,               0x00001123  @ Toon Alligator (pw=59383041; card_0316)
.equ METAL_GUARDIAN_CID,               0x00000ffe  @ Metal Guardian (pw=68339286; card_0191)
.equ GATE_GUARDIAN_CID,                0x0000111c  @ Gate Guardian (pw=25833572; card_0218)
.equ GUARDIAN_OF_THRONE_ROOM_CID,      0x000011a7  @ Guardian of the Throne Room (pw=47879985; card_0339)
.equ SKULL_GUARDIAN_CID,               0x00001266  @ Skull Guardian (pw=03627449; card_0584)
.equ GUARDIAN_ANGEL_JOAN_CID,          0x0000170b  @ Guardian Angel Joan (pw=68007326; card_1564)
.equ LOST_GUARDIAN_CID,                0x000018b0  @ Lost Guardian (pw=45871897; card_1828)
.equ DARK_SCORPION_CHICK_CID,          0x00001656  @ Dark Scorpion - Chick the Yellow (pw=61587183; card_1320)
.equ DARK_SCORPION_MEANAE_CID,         0x00001686  @ Dark Scorpion - Meanae the Thorn (pw=74153887; card_1356)
.equ MUSTERING_DARK_SCORPIONS_CID,     0x0000169e  @ Mustering of the Dark Scorpions (pw=68191243; card_1370)
@ NOTE: BATTERYMAN_AA_CID=0x18c3 and BATTERYMAN_C_CID=0x191c already in card_info.inc (reuse)
@ NOTE: BLUE_EYES_TOON_DRAGON_CID/TOON_DARK_MAGICIAN_GIRL_CID/TOON_WORLD_CARD_ID/TOON_GOBLIN_AF_CID already defined (reuse)
@ -- f05 Seg-4a new CIDs (63 + 3 inline + 2 field6) --
.equ HARPIE_LADY_SISTERS_CID,              0x00000fe5  @ Harpie Lady Sisters (pw=12206212)
.equ PERFECTLY_ULTIMATE_GREAT_MOTH_CID,    0x00000fe9  @ Perfectly Ultimate Great Moth (pw=48579379)
.equ MASK_OF_DARKNESS_CID,                 0x0000100c  @ Mask of Darkness (pw=28933734)
.equ PRINCESS_OF_TSURUGI_CID,              0x000010b0  @ Princess of Tsurugi (pw=51371017)
.equ WALL_SHADOW_CID,                      0x00001117  @ Wall Shadow (pw=63162310)
.equ SUIJIN_CID,                           0x0000111b  @ Suijin (pw=98434877)
.equ METALZOA_CID,                         0x0000112e  @ Metalzoa (pw=50705071)
.equ MAGICIAN_OF_FAITH_CID,                0x00001152  @ Magician of Faith (pw=31560081)
.equ HANE_HANE_CID,                        0x000011c3  @ Hane-Hane (pw=07089711)
.equ NEEDLE_WORM_CID,                      0x000011d8  @ Needle Worm (pw=81843628)
.equ MORPHING_JAR_CID,                     0x000011f5  @ Morphing Jar (pw=33508719)
.equ INVADER_OF_THE_THRONE_CID,            0x00001227  @ Invader of the Throne (pw=03056267)
.equ RED_EYES_BLACK_METAL_DRAGON_CID,      0x0000128c  @ Red-Eyes Black Metal Dragon (pw=64335804)
.equ THE_FIEND_MEGACYBER_CID,              0x00001299  @ The Fiend Megacyber (pw=66362965)
.equ GERM_INFECTION_CID,                   0x0000130d  @ Germ Infection (pw=24668830)
.equ STIM_PACK_CID,                        0x0000131a  @ Stim-Pack (pw=83225447)
.equ BUBONIC_VERMIN_CID,                   0x0000136a  @ Bubonic Vermin (pw=06104968)
.equ VALKYRION_THE_MAGNA_WARRIOR_CID,      0x0000138a  @ Valkyrion the Magna Warrior (pw=75347539)
.equ INJECTION_FAIRY_LILY_CID,             0x000013a7  @ Injection Fairy Lily (pw=79575620)
.equ SONIC_JAMMER_CID,                     0x000013bd  @ Sonic Jammer (pw=84550200)
.equ FOUR_STARRED_LADYBUG_OF_DOOM_CID,     0x00001413  @ 4-Starred Ladybug of Doom (pw=83994646)
.equ SUMMONER_OF_ILLUSIONS_CID,            0x00001481  @ Summoner of Illusions (pw=14644902)
.equ GILASAURUS_CID,                       0x00001488  @ Gilasaurus (pw=45894482)
.equ TORNADO_BIRD_CID,                     0x00001489  @ Tornado Bird (pw=71283180)
.equ MARYOKUTAI_CID,                       0x0000148c  @ Maryokutai (pw=71466592)
.equ EKIBYO_DRAKMORD_CID,                  0x0000149d  @ Ekibyo Drakmord (pw=69954399)
.equ DICE_JAR_CID,                         0x00001530  @ Dice Jar (pw=03549275)
.equ FUSHIOH_RICHIE_CID,                   0x00001534  @ Fushioh Richie (pw=39711336)
.equ A_CAT_OF_ILL_OMEN_CID,               0x00001590  @ A Cat of Ill Omen (pw=24140059)
.equ DIFFERENT_DIMENSION_CAPSULE_CID,      0x0000159c  @ Different Dimension Capsule (pw=11961740)
.equ XY_DRAGON_CANNON_CID,                 0x000015b1  @ XY-Dragon Cannon (pw=02111707)
.equ OLD_VINDICTIVE_MAGICIAN_CID,          0x00001613  @ Old Vindictive Magician (pw=45141844)
.equ MAGICAL_PLANT_MANDRAGOLA_CID,         0x00001618  @ Magical Plant Mandragola (pw=07802006)
.equ MAGICAL_MERCHANT_CID,                 0x0000161f  @ Magical Merchant (pw=32362575)
.equ GUARDIAN_GRARL_CID,                   0x0000164c  @ Guardian Grarl (pw=47150851)
.equ IRON_BLACKSMITH_KOTETSU_CID,          0x00001689  @ Iron Blacksmith Kotetsu (pw=73431236)
.equ CRIMSON_NINJA_CID,                    0x000016b8  @ Crimson Ninja (pw=14618326); used in tick_equip_sprite_with_attr11_if_seq_zero as sprite param (attr11 path); F06 Seg-7 slot 0x08058824
.equ FINAL_COUNTDOWN_CID,                  0x0000169c  @ Final Countdown (pw=95308449)
.equ WITCH_DOCTOR_OF_CHAOS_CID,            0x000016c2  @ Witch Doctor of Chaos (pw=75946257)
.equ CHAOS_SORCERER_CID,                   0x000016c9  @ Chaos Sorcerer (pw=09596126)
.equ BLACK_LUSTER_SOLDIER_ENVOY_CID,       0x000016cb  @ Black Luster Soldier - Envoy of the Beginning (pw=72989439)
.equ ARCHLORD_ZERATO_CID,                  0x00001758  @ Archlord Zerato (pw=18378582)
.equ SKULL_DESCOVERY_KNIGHT_CID,           0x00001771  @ Skull Descovery Knight (pw=78700060)
.equ DESERTAPIR_CID,                       0x0000178e  @ Desertapir (pw=13409151)
.equ RARE_METAL_DRAGON_CID,                0x000017c4  @ Rare Metal Dragon (pw=25236056)
.equ SORCERER_OF_DARK_MAGIC_CID,           0x000017c6  @ Sorcerer of Dark Magic (pw=88619463)
.equ NOBLEMAN_EATER_BUG_CID,               0x000017ea  @ Nobleman-Eater Bug (pw=65878864)
.equ THE_TRICKY_CID,                       0x00001806  @ The Tricky (pw=14778250)
.equ THE_BLOCKMAN_CID,                     0x00001810  @ The Blockman (pw=48115277)
.equ A_TEAM_TRAP_DISPOSAL_UNIT_CID,        0x0000183a  @ A-Team: Trap Disposal Unit (pw=13026402)
.equ SWORDS_OF_CONCEALING_LIGHT_CID,       0x0000187c  @ Swords of Concealing Light (pw=12923641)
.equ VAMPIRE_GENESIS_CID,                  0x00001895  @ Vampire Genesis (pw=22056710)
.equ ANCIENT_GEAR_BEAST_CID,               0x000018ac  @ Ancient Gear Beast (pw=10509340)
.equ DUMMY_GOLEM_CID,                      0x000018b5  @ Dummy Golem (pw=13532663)
.equ MASTER_MONK_CID,                      0x000018b9  @ Master Monk (pw=49814180)
.equ ELEMENTAL_HERO_THUNDER_GIANT_CID,     0x000018c9  @ Elemental Hero Thunder Giant (pw=61204971)
.equ CYBER_DRAGON_CID,                     0x000018f6  @ Cyber Dragon (pw=70095154)
.equ VWXYZ_DRAGON_CATAPULT_CANNON_CID,     0x00001954  @ VWXYZ-Dragon Catapult Cannon (pw=84243274)
.equ FAMILIAR_POSSESSED_WYNN_CID,          0x0000196e  @ Familiar-Possessed - Wynn (pw=31764353)
.equ DARK_ERADICATOR_WARLOCK_CID,          0x00001982  @ Dark Eradicator Warlock (pw=29436665)
.equ ELEMENTAL_HERO_STEAM_HEALER_CID,      0x00001987  @ Elemental Hero Steam Healer (pw=81197327)
.equ ANCIENT_GEAR_CID,                     0x000019aa  @ Ancient Gear (pw=31557782)
.equ PRINCESS_PIKERU_CID,                  0x000019cd  @ Princess Pikeru (pw=75917088)
.equ PRINCESS_CURRAN_CID,                  0x000019ce  @ Princess Curran (pw=02316186)
@ -- f05 Seg-4a inline immediate CIDs (movs+lsls computed values) --
.equ KURIBOH_CID,                          0x00000fe0  @ Kuriboh (pw=40640057); BST boundary in get_card_equip_zone_rank
.equ PENGUIN_SOLDIER_CID,                  0x00001200  @ Penguin Soldier (pw=93920745); BST boundary in get_card_field_summon_restriction
.equ DARK_SNAKE_SYNDROME_CID,              0x000015a0  @ Dark Snake Syndrome (pw=47233801); BST boundary in check_card_id_is_equip_set_a
@ -- f05 Seg-4a field6 spell type equates (used in check_card_id_is_equip_excluded_range) --
.equ CARD_FIELD6_EQUIP_CONTINUOUS,         0x00000016  @ field6 value = continuous equip spell type
.equ CARD_FIELD6_EQUIP_RITUAL,             0x00000017  @ field6 value = ritual spell type (field9==1 check)
@ -- f05 Seg-4b new CIDs (57 unique; get_card_effect_category / check_card_id_is_equip_set_* / classify_card_id_summon_category / etc.) --
.equ BEASTKING_OF_THE_SWAMPS_CID,        0x000010a8  @ Beastking of the Swamps (pw=99426834); equip set E
.equ VERSAGO_THE_DESTROYER_CID,          0x000010b3  @ Versago the Destroyer (pw=50259460); equip set E
.equ MONSTER_EYE_CID,                    0x00001138  @ Monster Eye (pw=84133008); summon category BST
.equ THUNDER_DRAGON_CID,                 0x0000114f  @ Thunder Dragon (pw=31786629); equip set C
.equ MYSTICAL_SHEEP_1_CID,               0x00001228  @ Mystical Sheep #1 (pw=30451366); equip set E
.equ MAGICAL_LABYRINTH_CID,              0x00001232  @ Magical Labyrinth (pw=64389297); equip blocker
.equ HANNIBAL_NECROMANCER_CID,           0x0000128e  @ Hannibal Necromancer (pw=05640330); effect category BST
.equ MESMERIC_CONTROL_CID,               0x000012ce  @ Mesmeric Control (pw=48642904); equip set D range bound
.equ MONSTER_REBORN_CID,                 0x000012ea  @ Monster Reborn (pw=83764718); summon category BST
.equ POT_OF_GREED_CID,                   0x000012ec  @ Pot of Greed (pw=55144522); equip set D + effect zone check
.equ ROYAL_DECREE_CID,                   0x00001302  @ Royal Decree (pw=51452091); equip set G
.equ RESTRUCTER_REVOLUTION_CID,          0x00001307  @ Restructer Revolution (pw=99518961); equip set D
.equ UPSTART_GOBLIN_CID,                 0x0000131f  @ Upstart Goblin (pw=70368879); effect zone check
.equ DELINQUENT_DUO_CID,                 0x00001325  @ Delinquent Duo (pw=44763025); equip set D
.equ THE_FORCEFUL_SENTRY_CID,            0x0000132b  @ The Forceful Sentry (pw=42829885); equip set D
.equ SPEAR_CRETIN_CID,                   0x0000133b  @ Spear Cretin (pw=58551308); summon category BST
.equ MORPHING_JAR_2_CID,                 0x00001369  @ Morphing Jar #2 (pw=79106360; card-stats.s slot=0x1369 card_0774); fn_eligible handler check_equip_eligible_morphing_jar_2
.equ SOLOMONS_LAWBOOK_CID,               0x0000137e  @ Solomon's Lawbook (pw=23471572; card-stats.s slot=0x137e card_0794); enqueue_spirit_monster_zone_sprite_otohime Lawbook/Maharaghi special case
.equ DE_FUSION_CID,                      0x000013fe  @ De-Fusion (pw=95286165); summon category BST
.equ JAR_OF_GREED_CID,                   0x0000145a  @ Jar of Greed (pw=83968380); effect zone check
.equ SPIRITUALISM_CID,                   0x0000147e  @ Spiritualism (pw=15866454); zone pair restriction
.equ SPIRIT_MESSAGE_I_CID,               0x00001497  @ Spirit Message "I" (pw=31893528); field spell type B range [0x1497..0x149a]
.equ SPIRIT_MESSAGE_N_CID,               0x00001498  @ Spirit Message "N" (pw=67287533; card-stats.s slot=0x1498); eligible_destiny_board_f85c CID comparison loop; f09 Seg-1R2 pool@0x6f95c
.equ SPIRIT_MESSAGE_A_CID,               0x00001499  @ Spirit Message "A" (pw=94772232; card-stats.s slot=0x1499); eligible_destiny_board_f85c CID comparison loop; f09 Seg-1R2 pool@0x6f964
.equ FUSION_GATE_CID,                    0x0000149c  @ Fusion Gate (pw=33550694); equip blocker
.equ THE_WARRIOR_RETURNING_ALIVE_CID,    0x000014d2  @ The Warrior Returning Alive (pw=95281259); summon category BST
.equ THE_DRAGONS_BEAD_CID,               0x000014de  @ The Dragon's Bead (pw=92408984); equip set G
.equ GREAT_DEZARD_CID,                   0x00001529  @ Great Dezard (pw=88989706); equip sets B + G
.equ CARD_OF_SANCTITY_CID,               0x00001567  @ Card of Sanctity (pw=42664989); effect zone check
.equ MYSTICAL_KNIGHT_OF_JACKAL_CID,      0x0000158f  @ Mystical Knight of Jackal (pw=98745000); summon category BST
.equ SKILLED_WHITE_MAGICIAN_CID,         0x00001610  @ Skilled White Magician (pw=46363422); effect category BST
.equ SKILLED_DARK_MAGICIAN_CID,          0x00001611  @ Skilled Dark Magician (pw=73752131); summon category BST
.equ ROYAL_MAGICAL_LIBRARY_CID,          0x0000161a  @ Royal Magical Library (pw=70791313); effect category BST root + effect zone check
.equ JAR_ROBBER_CID,                     0x0000162a  @ Jar Robber (pw=33784505); effect zone check
.equ MIRACLE_RESTORING_CID,              0x00001631  @ Miracle Restoring (pw=68334074); summon category upper bound
.equ DESROOK_ARCHFIEND_CID,              0x0000168f  @ Desrook Archfiend (pw=72192100); equip set C
.equ RAY_OF_HOPE_CID,                    0x000016a8  @ Ray of Hope (pw=82529174); summon category BST
.equ MATAZA_THE_ZAPPER_CID,              0x0000170a  @ Mataza the Zapper (pw=22609617); field zone special
.equ DEDICATION_THROUGH_LIGHT_DARK_CID, 0x00001713  @ Dedication through Light and Darkness (pw=69542930); summon category BST
.equ THE_KICK_MAN_CID,                   0x00001745  @ The Kick Man (pw=90407382); summon category BST
.equ CORPSE_OF_YATA_GARASU_CID,          0x00001776  @ Corpse of Yata-Garasu (pw=30461781); effect zone check
.equ ASWAN_APPARITION_CID,               0x0000178a  @ Aswan Apparition (pw=88236094); summon category BST
.equ NUBIAN_GUARD_CID,                   0x0000178c  @ Nubian Guard (pw=51616747); summon category BST
.equ KING_OF_THE_SWAMP_CID,              0x0000179c  @ King of the Swamp (pw=79109599); equip set C + E
.equ CARD_7_CID,                         0x000017a5  @ 7 (pw=67048711); effect zone check; card named "7" (conf med)
.equ THE_SECOND_SARCOPHAGUS_CID,         0x000017ae  @ The Second Sarcophagus (pw=04081094); field spell type B range [0x17ad..0x17ae]
.equ THE_END_OF_ANUBIS_CID,              0x000017b9  @ The End of Anubis (pw=65403020); equip set G
.equ DARK_FACTORY_MASS_PROD_CID,         0x000017f1  @ Dark Factory of Mass Production (pw=90928333); summon category BST
.equ CEMETARY_BOMB_CID,                  0x00001804  @ Cemetary Bomb (pw=51394546); equip set D
.equ BIG_CORE_CID,                       0x00001837  @ Big Core (pw=14148099); equip set B
.equ BLAST_MAGICIAN_CID,                 0x0000186a  @ Blast Magician (pw=21051146); effect category BST
.equ A_FEATHER_OF_THE_PHOENIX_CID,       0x0000187a  @ A Feather of the Phoenix (pw=49140998); summon category BST
.equ GOOD_GOBLIN_HOUSEKEEPING_CID,       0x00001888  @ Good Goblin Housekeeping (pw=09744376); effect zone check
.equ CYBER_END_DRAGON_CID,               0x000018fd  @ Cyber End Dragon (pw=01546123); equip excluded set F
.equ SPARK_BLASTER_CID,                  0x00001909  @ Spark Blaster (pw=97362768); equip set B root
.equ DARK_RULER_VANDALGYON_CID,          0x0000190a  @ Dark Ruler Vandalgyon (pw=24857466); summon category BST
.equ ALKANA_KNIGHT_JOKER_CID,            0x00001936  @ Alkana Knight Joker (pw=06150044); equip set G + summon cat
.equ POT_OF_AVARICE_CID,                 0x0000196f  @ Pot of Avarice (pw=67169062); effect zone check
.equ ROLL_OUT_CID,                       0x00001979  @ Roll Out! (pw=91597389); summon category BST
.equ MYTHICAL_BEAST_CERBERUS_CID,        0x00001983  @ Mythical Beast Cerberus (pw=55424270); effect category BST
.equ MAGICAL_MALLET_CID,                 0x0000198d  @ Magical Mallet (pw=85852291); effect zone check

@ =============================================================================
@ file 05 Seg-5 additions: Guardian weapon CIDs (classify_card_id_summon_category case pool)
@   + BST whitelist CIDs (check_card_slot_activation_eligible)
@ =============================================================================
.equ BUTTERFLY_DAGGER_ELMA_CID,             0x0000165c  @ Butterfly Dagger-Elma (pw=69243953; card_1332 slot=0x165C); classify_card_id_summon_category case Guardian weapon
.equ GRAVITY_AXE_GRARL_CID,                0x0000165e  @ Gravity Axe-Grarl (pw=32022366; card_1334 slot=0x165E); classify_card_id_summon_category case Guardian weapon
.equ WICKED_BREAKING_FLAMBERGE_BAOU_CID,   0x0000165f  @ Wicked-Breaking Flamberge-Baou (pw=68427465; card_1335 slot=0x165F); classify_card_id_summon_category case Guardian weapon
.equ TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID, 0x00001661  @ Twin Swords of Flashing Light-Tryce (pw=21900719; card_1337 slot=0x1661); classify_card_id_summon_category case Guardian weapon
.equ COCOON_OF_EVOLUTION_CID,              0x00000fee  @ Cocoon of Evolution (pw=40240595; card_0079 slot=0x0FEE); check_card_slot_activation_eligible BST lower bound
.equ SWORDS_OF_REVEALING_LIGHT_CID,        0x00001102  @ Swords of Revealing Light (pw=72302403; card_0308 slot=0x1102); check_card_slot_activation_eligible BST
.equ METALMORPH_CID,                       0x00001238  @ Metalmorph (pw=68540058; card_0539 slot=0x1238); check_card_slot_activation_eligible BST pivot

@ =============================================================================
@ file 05 Seg-6b additions: check_slot_card_eligible_by_card_id BST equip-target CIDs
@ Named cards (confirmed via data/card-stats.s slot_id match):
@ =============================================================================
.equ PETIT_MOTH_CID,              0x000010bc  @ Petit Moth (slot=0x10BC); BST node in check_slot_card_eligible_by_card_id
.equ LABYRINTH_WALL_CID,          0x00001114  @ Labyrinth Wall (pw=67284908; slot=0x1114); BST node
.equ CYCLON_LASER_CID,            0x00001496  @ Cyclon Laser (pw=05870978; slot=0x1496); BST node
.equ BUSTER_RANCHER_CID,          0x0000159e  @ Buster Rancher (slot=0x159E); BST node
.equ Y_DRAGON_HEAD_CID,           0x000015b0  @ Y-Dragon Head (pw=68514277; slot=0x15B0); BST node
.equ Z_METAL_TANK_CID,            0x000015b3  @ Z-Metal Tank (pw=64500000; slot=0x15B3); BST node
.equ DARK_BLADE_CID,              0x000015cd  @ Dark Blade (slot=0x15CD); BST node
.equ DECAYED_COMMANDER_CID,       0x000015d0  @ Decayed Commander (slot=0x15D0); BST node
.equ GIANT_ORC_CID,               0x000015d2  @ Giant Orc (slot=0x15D2); BST node
.equ SECOND_GOBLIN_CID,           0x000015d3  @ Second Goblin (slot=0x15D3); BST node
.equ VAMPIRE_ORCHIS_CID,          0x000015d4  @ Vampire Orchis (slot=0x15D4); BST node
.equ DES_DENDLE_CID,              0x000015d5  @ Des Dendle (slot=0x15D5); BST node
.equ BURNING_BEAST_CID,           0x000015d6  @ Burning Beast (slot=0x15D6); BST node
.equ AITSU_CID,                   0x0000160a  @ Aitsu (slot=0x160A); BST node
.equ WHITE_MAGICIAN_PIKERU_CID,   0x00001757  @ White Magician Pikeru (slot=0x1757); BST node
.equ RITUAL_WEAPON_CID,           0x000017fb  @ Ritual Weapon (slot=0x17FB); BST node
.equ CHU_SKE_MOUSE_FIGHTER_CID,   0x0000185a  @ Chu-Ske the Mouse Fighter (slot=0x185A); BST node
.equ EHERO_SPARKMAN_CID,          0x000018a9  @ Elemental Hero Sparkman (pw=20721928; slot=0x18A9); BST node
.equ LEGENDARY_BLACK_BELT_CID,    0x000018d0  @ Legendary Black Belt (slot=0x18D0); BST node
.equ SOITSU_CID,                  0x0000190b  @ Soitsu (slot=0x190B); BST node
.equ INDOMITABLE_FIGHTER_LEI_LEI_CID, 0x00001915 @ Indomitable Fighter Lei Lei (slot=0x1915); BST node
.equ EBON_MAGICIAN_CURRAN_CID,    0x0000191d  @ Ebon Magician Curran (pw=46128076; slot=0x191D); BST node
.equ DIVINE_SWORD_PHOENIX_BLADE_CID, 0x0000193a @ Divine Sword - Phoenix Blade (slot=0x193A); BST node
.equ V_TIGER_JET_CID,             0x00001947  @ V-Tiger Jet (pw=51638941; slot=0x1947); BST node
.equ ADHESIVE_EXPLOSIVE_CID,      0x000019bd  @ Adhesive Explosive (slot=0x19BD); BST node
@ Unallocated slot IDs used in BST (no card in card-stats.s with these slot_ids):
.equ cid_10d4,  0x000010d4  @ unallocated; BST node in check_slot_card_eligible_by_card_id
.equ cid_10da,  0x000010da  @ unallocated; BST node
.equ cid_10e2,  0x000010e2  @ unallocated; BST node
.equ cid_10e5,  0x000010e5  @ unallocated; BST node
.equ cid_10ea,  0x000010ea  @ unallocated; BST node
.equ cid_10eb,  0x000010eb  @ unallocated; BST node
.equ cid_10ed,  0x000010ed  @ unallocated; BST node
.equ cid_10ee,  0x000010ee  @ unallocated; BST node
.equ cid_12c6,  0x000012c6  @ unallocated; BST node
.equ cid_12ef,  0x000012ef  @ unallocated; BST node
@ Score threshold (not a CID):
.equ FIELD5_SCORE_THRESHOLD_1299,  0x00000513  @ field5 score upper bound; check_slot_card_eligible_by_card_id after get_slot_field5_score comparison; value 1299 is a score bound not a slot_id

@ =============================================================================
@ file 05 Seg-7 additions: equip slot eligibility BST card IDs
@ Source: asm/05_equip_eligibility_a.s Seg-7 (0x0804ffba..0x08050e40)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
@ Named CIDs (18 new, high-conf from card-stats.s):
.equ INFERNALQUEEN_ARCHFIEND_CID,  0x00001690  @ Infernalqueen Archfiend (slot=0x1690); eval_equip_slot_score_by_card_state BST
.equ THROWSTONE_UNIT_CID,          0x000014c5  @ Throwstone Unit (slot=0x14C5); eval_equip_slot_score_by_card_state BST
.equ DRAGON_SEEKER_CID,            0x0000119a  @ Dragon Seeker (slot=0x119A); eval_equip_slot_score_by_card_state BST
.equ WINGED_MINION_CID,            0x000014b9  @ Winged Minion (slot=0x14B9); eval_equip_slot_score_by_card_state BST
.equ COMBINATION_ATTACK_CID,       0x000015e4  @ Combination Attack (slot=0x15E4); eval_equip_slot_score_by_card_state BST
.equ WILD_NATURES_RELEASE_CID,     0x000016ce  @ Wild Nature's Release (slot=0x16CE); eval_equip_slot_score_by_card_state BST
.equ CYBER_LASER_DRAGON_CID,       0x000019a9  @ Cyber Laser Dragon (slot=0x19A9); eval_equip_slot_score_by_card_state BST
.equ TRIBE_INFECTING_VIRUS_CID,    0x0000161c  @ Tribe-Infecting Virus (slot=0x161C); check_equip_slot_eligible_by_card_id_bst BST
.equ BURST_BREATH_CID,             0x000014e4  @ Burst Breath (slot=0x14E4); check_equip_slot_eligible_by_card_id_bst BST
.equ NEEDLE_CEILING_CID,           0x00001542  @ Needle Ceiling (slot=0x1542); check_equip_slot_eligible_by_card_id_bst BST
.equ OJAMUSCLE_CID,                0x00001945  @ Ojamuscle (slot=0x1945); check_equip_slot_eligible_by_card_id_bst BST
.equ REALLY_ETERNAL_REST_CID,      0x0000166d  @ Really Eternal Rest (slot=0x166D); check_equip_slot_eligible_by_card_id_bst BST
.equ WEED_OUT_CID,                 0x00001977  @ Weed Out (slot=0x1977); check_equip_slot_eligible_by_card_id_bst BST
.equ CURSE_OF_ANUBIS_CID,          0x000017b3  @ Curse of Anubis (slot=0x17B3); check_equip_slot_eligible_with_bst_filter BST
.equ ROULETTE_BARREL_CID,          0x000015df  @ Roulette Barrel (slot=0x15DF); check_equip_slot_eligible_with_bst_filter BST
.equ ZERO_GRAVITY_CID,             0x000016e1  @ Zero Gravity (slot=0x16E1); check_equip_slot_eligible_with_bst_filter BST
.equ BURST_RETURN_CID,             0x00001988  @ Burst Return (slot=0x1988); check_equip_slot_eligible_with_bst_filter BST
.equ EHERO_BURSTINATRIX_CID,       0x000018a7  @ Elemental Hero Burstinatrix (slot=0x18A7); check_equip_slot_eligible_with_bst_filter BST
@ Unallocated slot IDs (4 new, low-conf neutral names; no card in card-stats.s with these slot_ids):
.equ cid_1304,  0x00001304  @ unallocated slot_id; BST root in check_equip_slot_eligible_by_card_id_bst
.equ cid_1305,  0x00001305  @ unallocated slot_id; BST node adjacent to cid_1304
.equ cid_123d,  0x0000123d  @ unallocated slot_id; BST node in check_equip_slot_eligible_by_card_id_bst
.equ cid_123e,  0x0000123e  @ unallocated slot_id; BST node adjacent to cid_123d

@ =============================================================================
@ file 05 Seg-8 additions: equip slot eligibility by card_id tree / pair / score CIDs
@ Source: asm/05_equip_eligibility_a.s Seg-8 (0x08050e40..0x08051cc4)
@ All values verified against data/card-stats.s slot= fields (confidence: high unless noted).
@ =============================================================================
.equ DE_SPELL_GERM_WEAPON_CID,              0x000014ee  @ De-Spell Germ Weapon (pw=54591086; card-stats.s card_1054 slot=0x14EE); check_equip_slot_eligible_by_card_id_tree BST
.equ TORPEDO_FISH_CID,                      0x00001706  @ Torpedo Fish (pw=90337190; card-stats.s card_1470 slot=0x1706); check_equip_slot_eligible_by_card_id_tree BST
.equ ORCA_MEGA_FORTRESS_OF_DARKNESS_CID,    0x00001708  @ Orca Mega-Fortress of Darkness (pw=63120904; card-stats.s card_1472 slot=0x1708); check_equip_slot_eligible_by_card_id_tree BST
.equ ARCANE_ARCHER_OF_THE_FOREST_CID,       0x00001753  @ Arcane Archer of the Forest (pw=55001420; card-stats.s card_1534 slot=0x1753); check_equip_slot_eligible_by_card_id_tree BST
.equ CHAIN_DESTRUCTION_CID,                 0x000012cd  @ Chain Destruction (pw=01248895; card-stats.s card_0654 slot=0x12CD); check_equip_slot_eligible_by_card_id_pair BST
.equ TRAP_HOLE_CID,                         0x000012e4  @ Trap Hole (pw=04206964; card-stats.s card_0668 slot=0x12E4); check_equip_slot_eligible_by_card_id_score BST
.equ ELEMENTAL_BURST_CID,                   0x0000188d  @ Elemental Burst (pw=61411502; card-stats.s card_1804 slot=0x188D); check_equip_slot_eligible_by_card_id_tree BST
.equ SPIRITUAL_WATER_ART_AOI_CID,           0x00001928  @ Spiritual Water Art - Aoi (pw=06540606; card-stats.s card_1925 slot=0x1928); check_equip_slot_eligible_by_card_id_tree BST
.equ SPIRITUAL_WIND_ART_MIYABI_CID,         0x0000192a  @ Spiritual Wind Art - Miyabi (pw=79333300; card-stats.s card_1927 slot=0x192A); check_equip_slot_eligible_by_card_id_tree BST
.equ HYDROGEDDON_CID,                       0x0000194f  @ Hydrogeddon (pw=22587018; card-stats.s card_1950 slot=0x194F); check_equip_slot_eligible_by_card_id_tree BST
.equ OXYGEDDON_CID,                         0x00001950  @ Oxygeddon (pw=58071123; card-stats.s card_1951 slot=0x1950); check_equip_slot_eligible_by_card_id_tree BST
@ Score threshold (not a CID; distinct from FIELD5_SCORE_THRESHOLD_1299=0x513 in this file):
.equ FIELD5_SCORE_THRESHOLD_1999,           0x000007cf  @ field5 score <= 1999 (0x7cf) path; check_equip_slot_eligible_by_card_id_tree Hydrogeddon/Oxygeddon path; value 1999 is score bound not slot_id

@ =============================================================================
@ file 05 Seg-9 additions: equip slot eligibility by_card_id_dispatch / by_type_and_card_id_pair CIDs
@ Source: asm/05_equip_eligibility_a.s, Seg-9 (0x08051cc4..0x08052df8)
@ 27 new CIDs; passcodes verified against data/card-stats.s.
@ =============================================================================
.equ SUMMONED_SKULL_CID,             0x00000fbc  @ Summoned Skull (pw=70781052, card_0022)
.equ RED_EYES_B_DRAGON_CID,          0x00000ff8  @ Red-Eyes B. Dragon (pw=74677422, card_0082)
.equ MULTIPLY_CID,                   0x000012c5  @ Multiply (pw=40703222); Multiply frog tokens
.equ GRACEFUL_DICE_CID,              0x000012cf  @ Graceful Dice (pw=74137509)
.equ SHADOW_TAMER_CID,               0x000014cd  @ Shadow Tamer (pw=37620434)
.equ DRAGON_MANIPULATOR_CID,         0x000014ce  @ Dragon Manipulator (pw=74701381)
.equ WINGBEAT_GIANT_DRAGON_CID,      0x000014df  @ A Wingbeat of Giant Dragon (pw=28596933)
.equ INSECT_IMITATION_CID,           0x0000140b  @ Insect Imitation (pw=96965364)
.equ LIMITER_REMOVAL_CID,            0x00001409  @ Limiter Removal (pw=23171610)
.equ CATHEDRAL_OF_NOBLES_CID,        0x0000146f  @ Cathedral of Nobles (pw=29732298)
.equ PYRAMID_ENERGY_CID,             0x0000153d  @ Pyramid Energy (pw=76826042)
.equ METAMORPHOSIS_CID,              0x000015a3  @ Metamorphosis (pw=46411259)
.equ FORMATION_UNION_CID,            0x000015f7  @ Formation Union (pw=26708437)
.equ KNIGHTS_TITLE_CID,              0x0000167d  @ Knight's Title (pw=87210505)
.equ TERRORKING_ARCHFIEND_CID,       0x00001691  @ Terrorking Archfiend (pw=55321970)
.equ ULTRA_EVOLUTION_PILL_CID,       0x00001715  @ Ultra Evolution Pill (pw=78418106)
.equ ORDER_TO_CHARGE_CID,            0x0000179f  @ Order to Charge (pw=78986941)
.equ ORDER_TO_SMASH_CID,             0x000017b8  @ Order to Smash (pw=39019325)
.equ BIG_WAVE_SMALL_WAVE_CID,        0x000017f9  @ Big Wave Small Wave (pw=51562916)
.equ DOUBLE_ATTACK_CID,              0x000018cb  @ Double Attack (pw=34187685)
.equ KAMINOTE_BLOW_CID,              0x000018cd  @ Kaminote Blow (pw=97570038)
.equ MINEFIELD_ERUPTION_CID,         0x000018d6  @ Minefield Eruption (pw=85519211)
.equ TRANSCENDENT_WINGS_CID,         0x00001907  @ Transcendent Wings (pw=25573054)
.equ SPIRITUAL_EARTH_ART_CID,        0x00001927  @ Spiritual Earth Art - Kurogane (pw=70156997)
.equ ELEMENTAL_HERO_TEMPEST_CID,     0x00001957  @ Elemental Hero Tempest (pw=card_2150+)
.equ HERO_HEART_CID,                 0x000019ab  @ Hero Heart (pw=67951831)
.equ PHOTON_GENERATOR_UNIT_CID,      0x000019b1  @ Photon Generator Unit (pw=card_2205+)

@ =============================================================================
@ file 05 Seg-10 additions: equip slot eligibility field5/chain dispatch CIDs
@ Source: asm/05_equip_eligibility_a.s, Seg-10 (0x08052df8..0x080537c0)
@ Values verified against data/card-stats.s; confidence: high.
@ =============================================================================
.equ BOTTOMLESS_TRAP_HOLE_CID,       0x00001518  @ Bottomless Trap Hole (pw=29401950; card-stats.s card_1088 slot=0x1518); check_equip_slot_eligible_by_field5_score_or_chain_type field5 score gate
.equ FIELD5_SCORE_THRESHOLD_1499,    0x000005db  @ field5 score threshold (1499=0x5db); score<=0x5db -> ineligible (ble branch); score>0x5db -> eligible; distinct from THRESHOLD_1299(0x513)/1999(0x7cf)

@ =============================================================================
@ file 06 Seg-2 additions: equip BST dispatch CIDs + Tricky target slot pattern
@ Source: asm/06_equip_eligibility_b.s, Seg-2 (0x080541cc..0x08054ba0)
@ Values verified against data/card-stats.s slot= fields (confidence: high).
@ =============================================================================
.equ ULTIMATE_BASEBALL_KID_CID,      0x000017e1  @ Ultimate Baseball Kid (pw=67934141; card-stats.s card_1889 slot=0x17E1); equip BST dispatch computed at runtime (0x180e-0x2d); no literal pool slot in Seg-2
.equ TRICKYS_MAGIC_4_CID,            0x0000180e  @ Tricky's Magic 4 (pw=75622824; card-stats.s card_1940 slot=0x180E); equip BST dispatch literal pool 0x08054948; high-conf
.equ GILFORD_THE_LEGEND_CID,         0x00001938  @ Gilford the Legend (pw=69933858; card-stats.s card_2073 slot=0x1938); equip BST dispatch literal pool 0x0805495c; high-conf
.equ SERIAL_SPELL_CID,               0x0000183e  @ Serial Spell (pw=49398568; card-stats.s card_1980 slot=0x183E); invoke_serial_spell_effect_node_handler literal pool 0x08054b9c; high-conf
.equ THE_TRICKY_TARGET_SLOT_PATTERN, 0xc0300000  @ THE_TRICKY_CID(0x1806)<<19 == 0xc0300000; Tricky's Magic 4 target check: (slot_word<<19)==pattern iff slot_word bits[12:0]==THE_TRICKY_CID; python verified; high-conf

@ =============================================================================
@ file 06 Seg-4 additions: equip activation BST card IDs
@ Source: asm/06_equip_eligibility_b.s, Seg-4 (0x08055440..0x080565e8)
@ All values verified against data/card-stats.s slot= fields.
@ 55 new CIDs: 50 named (high-conf) + 5 gap CIDs (low-conf neutral names; no card in card-stats.s).
@ Passcodes verified against data/card-stats.s.
@ =============================================================================
@ Named CIDs (sorted by CID value):
.equ MALEVOLENT_NUZZLER_CID,         0x000010e7  @ Malevolent Nuzzler (pw=99597615); tick_equip_activation BST dispatch
.equ MOOYAN_CURRY_CID,               0x000010f8  @ Mooyan Curry (pw=58074572); lookup_equip_card_score BST
.equ CHIMERA_FLYING_MYTHICAL_BEAST_CID, 0x00001294 @ Chimera the Flying Mythical Beast (pw=4796100); tick_equip_activation BST
.equ BRAIN_CONTROL_CID,              0x000012c3  @ Brain Control (pw=87910978); get_card_lp_cost_by_id BST
.equ DARK_MAGIC_CURTAIN_CID,         0x000012de  @ Dark Magic Curtain (pw=99789342); get_card_lp_cost_by_id BST
.equ SOLEMN_JUDGMENT_CID,            0x000012fd  @ Solemn Judgment (pw=41420027); get_card_lp_cost_by_id BST
.equ SEVEN_TOOLS_OF_THE_BANDIT_CID,  0x000012ff  @ Seven Tools of the Bandit (pw=3819470); get_card_lp_cost_by_id BST
.equ FINAL_DESTINY_CID,              0x00001321  @ Final Destiny (pw=18591904); classify_equip_tier_abce BST
.equ JUDGMENT_OF_ANUBIS_CID,         0x00001470  @ Judgment of Anubis (pw=55256016); classify_equip_tier_abce BST
.equ ROPE_OF_LIFE_CID,               0x000014a7  @ Rope of Life (pw=93382620); classify_equip_tier_abce BST
.equ DARK_BALTER_THE_TERRIBLE_CID,   0x000014b6  @ Dark Balter the Terrible (pw=80071763); get_card_lp_cost_by_id BST
.equ BARK_OF_DARK_RULER_CID,         0x000014be  @ Bark of Dark Ruler (pw=41925941); get_card_lp_cost_by_id BST
.equ SPELL_REPRODUCTION_CID,         0x000014ea  @ Spell Reproduction (pw=29228529); classify_equip_tier_abc_short BST
.equ MAHARAGHI_CID,                  0x000014fd  @ Maharaghi (pw=40695128); lookup_equip_card_score BST
.equ OMINOUS_FORTUNETELLING_CID,     0x00001519  @ Ominous Fortunetelling (pw=56995655); lookup_equip_card_score BST
.equ ORDEAL_OF_A_TRAVELER_CID,       0x0000153f  @ Ordeal of a Traveler (pw=39537362); lookup_equip_card_score BST
.equ PUPPET_MASTER_CID,              0x0000156a  @ Puppet Master (pw=41442341); get_card_lp_cost_by_id BST
.equ CARD_SHUFFLE_CID,               0x00001599  @ Card Shuffle (pw=12183332); get_card_lp_cost_by_id + lookup_equip_card_score BST
.equ REVERSAL_QUIZ_CID,              0x000015a5  @ Reversal Quiz (pw=5990062); lookup_equip_card_score BST
.equ ROPE_OF_SPIRIT_CID,             0x000015b5  @ Rope of Spirit (pw=37383714); get_card_lp_cost_by_id BST
.equ SPELL_SHIELD_TYPE8_CID,         0x000015f1  @ Spell Shield Type-8 (pw=38275183); lookup_equip_card_score BST
.equ BREAKER_MAGICAL_WARRIOR_CID,    0x00001617  @ Breaker the Magical Warrior (pw=71413901); classify_equip_tier_abcx BST
.equ ANTI_SPELL_CID,                 0x00001634  @ Anti-Spell (pw=53112492); classify_equip_tier_abcx BST
.equ SPELL_ABSORBING_LIFE_CID,       0x00001635  @ The Spell Absorbing Life (pw=99517131; card-stats.s card_1301 slot=0x1635); tick_equip_zone_slot_and_lp_indicator_state_machine dispatch by card_id (CID=0x1635 path: submit_effect_zone_lp_and_shape_sprites); conf: high
.equ SKILL_DRAIN_CID,                0x0000166c  @ Skill Drain (pw=82732705); get_card_lp_cost_by_id BST
.equ DARK_SCORPION_GORG_THE_STRONG_CID, 0x00001685 @ Dark Scorpion - Gorg the Strong (pw=48768179); lookup_equip_card_score BST
.equ SPELL_VANISHING_CID,            0x000016a6  @ Spell Vanishing (pw=29735721); classify_equip_tier_abce BST
.equ DIMENSION_FUSION_CID,           0x00001712  @ Dimension Fusion (pw=23557835); get_card_lp_cost_by_id BST
.equ AGENT_OF_CREATION_VENUS_CID,    0x00001741  @ The Agent of Creation - Venus (pw=64734921); get_card_lp_cost_by_id BST
.equ MYSTIK_WOK_CID,                 0x0000175a  @ Mystik Wok (pw=80161395); lookup_equip_card_score BST
.equ RETURN_ZOMBIE_CID,              0x00001775  @ Return Zombie (pw=3072077); get_card_lp_cost_by_id BST
.equ SPECIAL_HURRICANE_CID,          0x0000179e  @ Special Hurricane (pw=42598242); classify_equip_tier_abce BST
.equ SPELL_ECONOMICS_CID,            0x000017a3  @ Spell Economics (pw=4259068); get_card_lp_cost_by_id field6==0x16 gate
.equ ENCHANTING_FITTING_ROOM_CID,    0x000017a7  @ Enchanting Fitting Room (pw=30531525); get_card_lp_cost_by_id BST
.equ CRUSH_D_GANDRA_CID,             0x000017bc  @ Crush D. Gandra (pw=64681432); get_card_lp_cost_by_id BST
.equ ABYSSAL_DESIGNATOR_CID,         0x000017f4  @ Abyssal Designator (pw=89801755); get_card_lp_cost_by_id BST
.equ BACK_TO_SQUARE_ONE_CID,         0x00001844  @ Back to Square One (pw=47453433); classify_equip_tier_abce BST
.equ FUH_RIN_KA_ZAN_CID,             0x0000184e  @ Fuh-Rin-Ka-Zan (pw=1781310); lookup_equip_card_score BST
.equ SPELL_PURIFICATION_CID,         0x00001851  @ Spell Purification (pw=1669772); classify_equip_tier_abce BST
.equ FORCED_CEASEFIRE_CID,           0x0000188e  @ Forced Ceasefire (pw=97806240); classify_equip_tier_abce BST
.equ BATTERY_CHARGER_CID,            0x000018cc  @ Battery Charger (pw=61181383); get_card_lp_cost_by_id BST
.equ BUBBLE_SHUFFLE_CID,             0x00001908  @ Bubble Shuffle (pw=61968753); check_equip_slot_eligible_by_card_id_bst_special_cases
.equ CYBERNETIC_MAGICIAN_CID,        0x0000190e  @ Cybernetic Magician (pw=59023523); classify_equip_tier_abce BST
.equ PROTECTIVE_SOUL_AILIN_CID,      0x00001916  @ Protective Soul Ailin (pw=11678191); lookup_equip_card_score BST
.equ A_RIVAL_APPEARS_CID,            0x0000192b  @ A Rival Appears! (pw=5728014); check_equip_slot_eligible_by_rival_appears_effect
.equ TRIAGE_CID,                     0x00001932  @ Triage (pw=30888983); get_card_lp_cost_by_id BST
.equ DARK_DEAL_CID,                  0x00001975  @ Dark Deal (pw=65824822); get_card_lp_cost_by_id BST
.equ PHANTASMAL_MARTYRS_CID,         0x000019af  @ Phantasmal Martyrs (pw=93224848); classify_equip_tier_abc_short BST
.equ DAMAGE_CONDENSER_CID,           0x000019b6  @ Damage Condenser (pw=28378427); classify_equip_tier_abce BST
.equ DEMISE_KING_OF_ARMAGEDDON_CID,  0x000019d5  @ Demise, King of Armageddon (pw=72426662); get_card_lp_cost_by_id BST
.equ MALFUNCTION_CID,                0x000019e2  @ Malfunction (pw=6137095); get_card_lp_cost_by_id BST
@ Gap CIDs (5 new, low-conf neutral names; no slot= in card-stats.s for these values):
.equ get_card_lp_cost_by_id_cid_1190, 0x00001190 @ unallocated slot_id; BST node in get_card_lp_cost_by_id
.equ get_card_lp_cost_by_id_cid_11cf, 0x000011cf @ unallocated slot_id; BST node in get_card_lp_cost_by_id
.equ get_card_lp_cost_by_id_cid_1393, 0x00001393 @ unallocated slot_id; BST node in get_card_lp_cost_by_id
.equ get_card_lp_cost_by_id_cid_169d, 0x0000169d @ unallocated slot_id; BST node in get_card_lp_cost_by_id
.equ lookup_equip_card_score_cid_1388, 0x00001388 @ unallocated slot_id; BST node in lookup_equip_card_score; same value as LP_COST_5000/EQUIP_SLOT_CARD_ID_RANGE_MAX -- different domain

@ =============================================================================
@ file 06 Seg-5 additions: CID equates used in dispatch_equip_activation_score_by_card_id
@ and related equip-activation sprite display functions
@ Source: asm/06_equip_eligibility_b.s Seg-5 (0x080565e8..0x08057458)
@ =============================================================================
.equ POISON_OF_THE_OLD_MAN_CID,   0x000015e7  @ Poison of the Old Man (pw=08842266); slot=0x15E7 in card-stats.s line 16121; dispatch_equip_activation_score_by_card_id BST; conf: high
.equ CYBER_RAIDER_CID,             0x00001298  @ Cyber Raider (pw=39978267); slot=0x1298 in card-stats.s line 7997; dispatch_equip_activation_score_by_card_id BST; conf: high
.equ SPIRITUAL_FIRE_ART_CID,       0x00001929  @ Spiritual Fire Art - Kurenai (pw=42945701); slot=0x1929 in card-stats.s line 25052; distinct from SPIRITUAL_WIND_ART_MIYABI_CID=0x192a and SPIRITUAL_EARTH_ART_CID=0x1927; conf: high
.equ FRIENDSHIP_CID,               0x0000167a  @ Friendship (pw=81332143); slot=0x167A in card-stats.s line 17577; adjacent to UNITY_CID=0x167b; pair-check in dispatch_equip_activation_score_by_card_id; conf: high
.equ UNITY_CID,                    0x0000167b  @ Unity (pw=14731897); slot=0x167B in card-stats.s line 17590; adjacent to FRIENDSHIP_CID=0x167a; pair-check in dispatch_equip_activation_score_by_card_id; conf: high
.equ ATTACK_REFLECTOR_UNIT_CID,    0x000019b5  @ Attack Reflector Unit (pw=91989718); slot=0x19B5 in card-stats.s line 26378; tick_equip_score_sprite_display_seq BST; conf: high
.equ PITCH_BLACK_POWER_STONE_CID,  0x00001624  @ Pitch-Black Power Stone (pw=34029630); slot=0x1624 in card-stats.s line 16746; tick_equip_activation_state_by_phase phase=1 BST; conf: high

@ =============================================================================
@ file 06 Seg-6 additions: CID equates for equip activation guard functions
@ Source: asm/06_equip_eligibility_b.s Seg-6 (0x08057458..0x08058550)
@ =============================================================================
.equ CLIFF_THE_TRAP_REMOVER_CID,   0x0000161e  @ Cliff the Trap Remover (pw=06967870; card-stats.s card_1282 slot=0x161E); tick_equip_lp_score_and_card_id_seq LP-score dispatch; 2 Seg-6 slots; conf: high
.equ OTOHIME_CID,                  0x00001503  @ Otohime (pw=39751093; card-stats.s card_1070 slot=0x1503); tick_equip_activation_if_not_otohime guard: CID filter to bypass equip activation state machine; 1 Seg-6 slot; conf: high

@ =============================================================================
@ file 06 Seg-9 additions: CID equates for equip placement and effect dispatch
@ Source: asm/06_equip_eligibility_b.s Seg-9 (0x08059de0..0x0805b480)
@ =============================================================================
@ Special sentinel constants (non-CID domain but stored in card_info.inc by context):
.equ URIA_LORD_CID,                0x000019a3  @ Uria, Lord of Searing Flames (pw=06007213; card-stats.s card_2012 slot=0x19A3); partner CID check in apply_card_equip_activation @0x0805aee4; CONST_RENAME from SPECIAL_EQUIP_SENTINEL_ID (F07 Seg-10)
.equ ZONE_STATUS_MASK,             0x0000303e  @ slot[+2] zone flags combined mask; slot[+2]&0x303e==0x201c placement check; check_card_normal_summon_eligible_full plates L19781+L19867; conf: high
.equ SPECIAL_EQUIP_TARGET_CID_A,   0x0000131e  @ check_equip_card_can_target_partner special-case CID (no card-stats.s entry; gap between 0x131D Gravekeeper Servant and 0x131F Upstart Goblin); asm/02 L34470 notes chain effect node type 0x131e; conf: high
@ New CID equates (20 values; all absent from card_info.inc per grep; passcodes from card-stats.s):
.equ SPELLBINDING_CIRCLE_CID,      0x00001103  @ Spellbinding Circle (pw=18807108; card-stats.s slot=0x1103); check_card_zone_activation_blocked dispatch; conf: high
.equ SHADOW_SPELL_CID,             0x00001243  @ Shadow Spell (pw=29267084; card-stats.s slot=0x1243); check_card_zone_activation_blocked dispatch; conf: high
.equ ANTI_SPELL_FRAGRANCE_CID,     0x00001390  @ Anti-Spell Fragrance (pw=58921041; card-stats.s slot=0x1390); check_card_zone_activation_blocked (2 slots); note: same value as FIELD_SPELL_CARD_REF_OFF in duel_field.inc but different domain -- CID vs offset; conf: high
.equ SMOKE_GRENADE_OF_THIEF_CID,   0x0000150d  @ Smoke Grenade of the Thief (pw=63789924; card-stats.s slot=0x150D); check_card_placement_rules dispatch; conf: high
.equ SPELL_CANCELLER_CID,          0x000015da  @ Spell Canceller (pw=84636823; card-stats.s slot=0x15DA); check_card_zone_activation_blocked dispatch; conf: high
.equ WAVE_MOTION_CANNON_CID,       0x000015ee  @ Wave-Motion Cannon (pw=38992735; card-stats.s slot=0x15EE); dispatch_card_effect_by_stat_type dispatch; conf: high
.equ FAIRY_OF_THE_SPRING_CID,      0x00001664  @ Fairy of the Spring (pw=20188127; card-stats.s slot=0x1664); check_card_placement_rules dispatch; conf: high
.equ CURSED_SEAL_FORBIDDEN_SPELL_CID, 0x000016dd @ Cursed Seal of the Forbidden Spell (pw=58851034; card-stats.s slot=0x16DD); check_card_placement_rules dispatch; conf: high
.equ STRAY_LAMBS_CID,              0x00001710  @ Stray Lambs (pw=60764581; card-stats.s slot=0x1710); dispatch_card_effect_by_stat_type dispatch; conf: high
.equ INVADER_OF_DARKNESS_CID,      0x00001722  @ Invader of Darkness (pw=56647086; card-stats.s slot=0x1722); check_card_placement_rules dispatch; conf: high
.equ AGENT_OF_JUDGMENT_SATURN_CID, 0x0000173f  @ The Agent of Judgment - Saturn (pw=91345518; card-stats.s slot=0x173F); dispatch_card_effect_by_stat_type dispatch; conf: high
.equ SPIRIT_RYU_CID,               0x000014d7  @ Spirit Ryu (pw=67957315; card-stats.s card_1031 slot=0x14D7); check_equip_card_can_target_partner special-case CID; conf: high
.equ LEVEL_MODULATION_CID,         0x00001944  @ Level Modulation (pw=61850482; card-stats.s slot=0x1944); check_card_placement_rules dispatch (2 slots); conf: high
.equ CREEPING_DOOM_MANTA_CID,      0x00001832  @ Creeping Doom Manta (pw=52571838; card-stats.s slot=0x1832); check_card_placement_rules dispatch; conf: high
.equ PITCH_BLACK_WARWOLF_CID,      0x00001833  @ Pitch-Black Warwolf (pw=88975532; card-stats.s slot=0x1833); check_card_placement_rules dispatch; conf: high
.equ MIRAGE_DRAGON_CID,            0x00001834  @ Mirage Dragon (pw=15960641; card-stats.s slot=0x1834); check_card_placement_rules dispatch; conf: high
.equ IMPENETRABLE_FORMATION_CID,   0x000018d3  @ Impenetrable Formation (pw=96631852; card-stats.s slot=0x18D3); dispatch_card_effect_by_stat_type dispatch; conf: high
.equ MECHANICAL_HOUND_CID,         0x00001910  @ Mechanical Hound (pw=22512237; card-stats.s slot=0x1910); check_card_placement_rules dispatch; conf: high
.equ ANCIENT_GEAR_CANNON_CID,      0x000019bb  @ Ancient Gear Cannon (pw=80045583; card-stats.s slot=0x19BB); check_card_placement_rules dispatch; conf: high
.equ TRIAL_OF_THE_PRINCESSES_CID,  0x000019d8  @ Trial of the Princesses (pw=72709014; card-stats.s slot=0x19D8); dispatch_card_effect_by_stat_type dispatch; conf: high

@ =============================================================================
@ file 06 Seg-10 additions: equip zone eligibility / special-summon check CIDs
@ Source: asm/06_equip_eligibility_b.s Seg-10 (0x0805b480..0x0805c2f0)
@ =============================================================================
.equ GORGONS_EYE_CID,              0x000012bf  @ Gorgon's Eye (pw=52648457; card-stats.s slot=0x12bf); populate_effect_node_snapshot + check_card_special_summon_eligible_full; conf: high
.equ RITE_OF_SPIRIT_CID,           0x000015ac  @ Rite of Spirit (pw=30450531; card-stats.s slot=0x15ac); check_card_special_summon_eligible_full; conf: high
.equ SILENT_INSECT_CID,            0x000019c6  @ Silent Insect (pw=40867519; card-stats.s slot=0x19c6); populate_effect_node_snapshot; conf: high
.equ cid_134e,                     0x0000134e  @ unassigned slot 0x134e (between Driving Snow 0x134d and Numinous Healer 0x1352 gap); populate_effect_node_snapshot; conf: low
.equ cid_134f,                     0x0000134f  @ unassigned slot 0x134f (gap); populate_effect_node_snapshot; conf: low
.equ cid_1350,                     0x00001350  @ unassigned slot 0x1350 (gap); populate_effect_node_snapshot; conf: low
.equ cid_1351,                     0x00001351  @ unassigned slot 0x1351 (gap between 0x1350 and Numinous Healer 0x1352); populate_effect_node_snapshot; conf: low

@ =============================================================================
@ file 07 Seg-1 additions: equip effect chain / card effect handler dispatch CIDs
@ Source: asm/07_equip_effect_chain.s Seg-1 (0x0805c2f0..0x0805cfec)
@ =============================================================================
.equ SANGA_OF_THUNDER_CID,       0x00001119  @ Sanga of the Thunder (pw=25955164; card-stats.s slot=0x1119); check_equip_slot_eligible_with_sanga_and_prereqs chain node check; conf: high
.equ SCAPEGOAT_CID,              0x000012d2  @ Scapegoat (pw=73915051; card-stats.s slot=0x12d2); min_monster_slots=4 threshold in check_equip_slot_eligible_by_scapegoat_or_stray_lambs; conf: high
.equ GRACEFUL_CHARITY_CID,       0x000012cc  @ Graceful Charity (pw=79571449; card-stats.s slot=0x12cc); tier-3 LP cost threshold in check_lp_draw_card_tier_threshold; conf: high
.equ GREENKAPPA_CID,             0x000011f0  @ Greenkappa (pw=61831093; card-stats.s slot=0x11f0); dispatch branch boundary in check_equip_target_zone_validity_by_card_id; conf: high
.equ REAPER_OF_CARDS_CID,        0x00000ffa  @ Reaper of the Cards (pw=33066139; card-stats.s slot=0x0ffa); direct effect slot read path in check_equip_target_zone_validity_by_card_id; conf: high
.equ HARPIES_FEATHER_DUSTER_CID, 0x00001246  @ Harpie's Feather Duster (pw=18144506; card-stats.s slot=0x1246); direct effect slot read path; conf: high
.equ DRIVING_SNOW_CID,           0x0000134d  @ Driving Snow (pw=00473469; card-stats.s slot=0x134d); dedicated dispatch branch in check_equip_target_zone_validity_by_card_id; conf: high
.equ NOBLEMAN_EXTERMINATION_CID, 0x00001364  @ Nobleman of Extermination (pw=17449108; card-stats.s slot=0x1364); dedicated path in check_equip_target_zone_validity_by_card_id; conf: high
.equ BAIT_DOLL_CID,              0x0000149b  @ Bait Doll (pw=07165085; card-stats.s slot=0x149b); dedicated path in check_equip_target_zone_validity_by_card_id; conf: high
.equ cid_131c,                   0x0000131c  @ unassigned slot 0x131c (not in card-stats.s); dispatch upper boundary in check_equip_target_zone_validity_by_card_id; conf: low
.equ cid_12fb,                   0x000012fb  @ unassigned slot 0x12fb (not in card-stats.s); count_field_copies_of_card arg in check_equip_slot_eligible_without_reserved_field_card; conf: low

@ =============================================================================
@ file 07 Seg-2 additions: spell/zone effect eligibility predicates BST CIDs
@ Source: asm/07_equip_effect_chain.s Seg-2 (0x0805cfec..0x0805e358)
@ =============================================================================
.equ DARK_HOLE_CID,              0x000010f6  @ Dark Hole (pw=53129443; card-stats.s slot=0x10F6); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ RAIGEKI_CID,                0x000010f7  @ Raigeki (pw=12580477; card-stats.s slot=0x10F7); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ ALPHA_MAGNET_WARRIOR_CID,   0x00001288  @ Alpha The Magnet Warrior (pw=99785935; card-stats.s slot=0x1288); check_equip_eligible_with_magnet_warrior_trio; conf: high
.equ BETA_MAGNET_WARRIOR_CID,    0x0000129b  @ Beta The Magnet Warrior (pw=39256679; card-stats.s slot=0x129B); check_equip_eligible_with_magnet_warrior_trio; conf: high
.equ GAMMA_MAGNET_WARRIOR_CID,   0x000012b8  @ Gamma The Magnet Warrior (pw=27175001; card-stats.s slot=0x12B8); check_equip_eligible_with_magnet_warrior_trio; conf: high
.equ cid_12f7,                   0x000012f7  @ unassigned slot 0x12f7 (not in card-stats.s; neighbors: 0x12f8=Tribute to the Doomed, 0x12f9=Soul Release); conf: low
.equ MAGIC_DRAIN_CID,            0x0000140d  @ Magic Drain (pw=59344077; card-stats.s slot=0x140D); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ RIRYOKU_FIELD_CID,          0x0000148f  @ Riryoku Field (pw=70344351; card-stats.s slot=0x148F); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ TUTAN_MASK_CID,             0x0000153e  @ Tutan Mask (pw=86120751; card-stats.s slot=0x153E); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ CURSE_OF_ROYAL_CID,         0x00001541  @ Curse of Royal (pw=02314238; card-stats.s slot=0x1541); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ TRAP_JAMMER_CID,            0x00001721  @ Trap Jammer (pw=19737124; card-stats.s slot=0x1721); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ ARMOR_BREAK_CID,            0x0000176b  @ Armor Break (pw=79649195; card-stats.s slot=0x176B); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ NUMINOUS_HEALER_CID,        0x00001352  @ Numinous Healer (pw=02130625; card-stats.s slot=0x1352); check_equip_zone_eligible_numinous_healer_and_recv dispatch handler; conf: high
.equ FORCED_REQUISITION_CID,     0x00001354  @ Forced Requisition (pw=74923978; card-stats.s slot=0x1354); check_equip_zone_eligible_forced_requisition dispatch handler; conf: high
.equ MINOR_GOBLIN_OFFICIAL_CID,  0x00001355  @ Minor Goblin Official (pw=01918087; card-stats.s slot=0x1355); check_equip_zone_eligible_minor_goblin_official dispatch handler; conf: high
.equ ATTACK_AND_RECEIVE_CID,     0x0000135a  @ Attack and Receive (pw=93553943; card-stats.s slot=0x135A); check_equip_zone_eligible_numinous_healer_and_recv shared handler; conf: high
.equ cid_135b,                   0x0000135b  @ unassigned slot 0x135b (not in card-stats.s; neighbors: 0x135a=Attack and Receive, 0x135c=Ceasefire); conf: low
.equ CEASEFIRE_CID,              0x0000135c  @ Ceasefire (pw=36468556; card-stats.s card_0764 slot=0x135C); tick_equip_zone_slot_and_lp_indicator_state_machine dispatch by card_id (CID=0x135c path: submit_lp_indicator_with_slot_xor_flag); conf: high
.equ MAGICAL_HATS_CID,           0x00001362  @ Magical Hats (pw=81210420; card-stats.s card_0769 slot=0x1362); fn_eligible handler check_equip_eligible_magical_hats via dispatch table @0x1e40490; conf: high
.equ SPELL_STOPPING_STATUTE_CID, 0x000018dd  @ Spell-Stopping Statute (pw=10048942; card-stats.s slot=0x18DD); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high
.equ ROYAL_SURRENDER_CID,        0x000018de  @ Royal Surrender (pw=56058951; card-stats.s slot=0x18DE); check_equip_zone_effect_eligible_by_card_id BST leaf; conf: high

@ =============================================================================
@ file 07 Seg-3 additions: score predicate cluster / card effect handler dispatch CIDs
@ Source: asm/07_equip_effect_chain.s Seg-3 (0x0805e358..0x0805f1cc)
@ =============================================================================
.equ REVIVAL_JAM_CID,            0x000013c7  @ Revival Jam (pw=31709826; card-stats.s card_0843 slot=0x13C7); check_revival_jam_equip_paired_field5 literal pool; conf: high
.equ RED_MOON_BABY_CID,          0x00001415  @ Red-Moon Baby (pw=56387350; card-stats.s card_0896 slot=0x1415); check_equip_or_facedown_slot_eligible_by_dispatch literal pool; conf: high

@ =============================================================================
@ file 07 Seg-4 additions: turn/side predicate cluster / card effect handler dispatch CIDs
@ Source: asm/07_equip_effect_chain.s Seg-4 (0x0805f1cc..0x0805fc94)
@ =============================================================================
.equ FUSHI_NO_TORI_CID,          0x00001506  @ Fushi No Tori spirit monster (pw=38538445; card-stats.s card_1073 slot=0x1506); dispatch_slot_placement_check_by_card_id path; 1 Seg-4 slot
.equ TSUKUYOMI_CID,              0x00001694  @ Tsukuyomi spirit monster (pw=34853266; card-stats.s card_1376 slot=0x1694); dispatch_slot_placement_check_by_card_id path; 1 Seg-4 slot
.equ SWARM_OF_SCARABS_CID,       0x0000152a  @ Swarm of Scarabs (pw=15383415; card-stats.s card_1104 slot=0x152a); distinct from EQUIP_ZONE_SPRITE_ATTR_MODE1=0x152a (sprite domain); check_light_of_intervention_and_swarm_absent; 1 Seg-4 slot
.equ LIFE_ABSORBING_MACHINE_CID, 0x000014c0  @ Life Absorbing Machine (pw=14318794; card-stats.s card_1011 slot=0x14c0); check_slot_has_life_absorbing_machine_node immediate arg; no literal pool slot (inline imm); 0 slots

@ =============================================================================
@ file 07 Seg-5 additions: equip slot eligibility predicate card IDs
@ Source: asm/07_equip_effect_chain.s Seg-5 (0x0805fc94..0x08060898)
@ =============================================================================
.equ PEOPLE_RUNNING_ABOUT_CID,  0x000015ca  @ People Running About (pw=12143771; card-stats.s card_1245 slot=0x15CA); resistance triple check; 1 Seg-5 slot DWORD_0806054c
.equ OPPRESSED_PEOPLE_CID,      0x000015cb  @ Oppressed People (pw=58538870; card-stats.s card_1246 slot=0x15CB); resistance triple check; 1 Seg-5 slot DWORD_08060550
.equ UNITED_RESISTANCE_CID,     0x000015cc  @ United Resistance (pw=85936485; card-stats.s card_1247 slot=0x15CC); resistance triple check; 1 Seg-5 slot DWORD_08060554
.equ REASONING_CID,             0x0000159a  @ Reasoning (pw=58577036; card-stats.s line 15381 slot=0x159A); disasm Block1 handler fn; 1 Seg-5 block
.equ HELPING_ROBO_FOR_COMBAT_CID, 0x000015dc @ Helping Robo For Combat (pw=47025270; card-stats.s line 16005 slot=0x15DC); disasm Block2 handler fn; 1 Seg-5 block
.equ THUNDER_OF_RULER_CID,      0x000015f0  @ Thunder of Ruler (pw=91781589; card-stats.s line 16213 slot=0x15F0); disasm Block3 F1 handler fn
.equ METEORAIN_CID,             0x000015f2  @ Meteorain (pw=64274292; card-stats.s line 16239 slot=0x15F2); disasm Block3 F2 handler fn
.equ PINEAPPLE_BLAST_CID,       0x000015f3  @ Pineapple Blast (pw=90669991; card-stats.s L16252 slot=0x15F3); disasm Block3 F3 handler fn

@ =============================================================================
@ file 07 Seg-6 additions: equip slot eligibility predicate card IDs
@ Source: asm/07_equip_effect_chain.s Seg-6 (0x08060898..0x080613b4)
@ =============================================================================
.equ QUEENS_KNIGHT_CID,             0x0000157f  @ Queen's Knight (pw=25652259; card-stats.s card_1158 slot=0x157F); companion dispatch in check_equip_slot_eligible_by_companion_card_and_paired_slot; conf: high
.equ CONTRACT_WITH_EXODIA_CID,      0x0000165b  @ Contract with Exodia (pw=33244944; card-stats.s card_1331 slot=0x165B); dispatch handler fn check_exodia_set_in_extra_for_cid_165b; conf: high
.equ SAGES_STONE_CID,               0x0000167e  @ Sage's Stone (pw=13604200; card-stats.s card_1355 slot=0x167E); companion dispatch; conf: high
.equ OJAMA_YELLOW_CID,              0x000016b3  @ Ojama Yellow (pw=42941100; card-stats.s card_1399 slot=0x16B3); Ojama trio check; conf: high
.equ FENRIR_CID,                    0x000016c6  @ Fenrir (pw=00218704; card-stats.s card_1416 slot=0x16C6); dispatch handler fn check_zone_type580_direction_mismatch_for_cid_16c6; conf: high
.equ CHAOS_END_CID,                 0x000016d1  @ Chaos End (pw=61044390; card-stats.s card_1427 slot=0x16D1); dispatch handler fn check_lp_zone_hand_above6_for_cid_16d1; conf: high
.equ CHAOS_EMPEROR_DRAGON_CID,      0x000016e4  @ Chaos Emperor Dragon - Envoy of the End (pw=82301904; card-stats.s card_1445 slot=0x16E4); BLS+CED envoy paired check; conf: high
@ Exodia piece CIDs -- Block1 literal pool slots (all new; 0 hits in card_info.inc)
.equ RIGHT_LEG_FORBIDDEN_ONE_CID,   0x00000fb7  @ Right Leg of the Forbidden One (pw=08124921; card-stats.s card_0017 slot=0x0FB7); Exodia set check Block1; conf: high
.equ LEFT_LEG_FORBIDDEN_ONE_CID,    0x00000fb8  @ Left Leg of the Forbidden One (pw=44519536; card-stats.s card_0018 slot=0x0FB8); Exodia set check Block1; conf: high
.equ RIGHT_ARM_FORBIDDEN_ONE_CID,   0x00000fb9  @ Right Arm of the Forbidden One (pw=70903634; card-stats.s card_0019 slot=0x0FB9); Exodia set check Block1; conf: high
.equ LEFT_ARM_FORBIDDEN_ONE_CID,    0x00000fba  @ Left Arm of the Forbidden One (pw=07902349; card-stats.s card_0020 slot=0x0FBA); Exodia set check Block1; conf: high
.equ EXODIA_THE_FORBIDDEN_ONE_CID,  0x00000fbb  @ Exodia the Forbidden One (pw=33396948; card-stats.s card_0021 slot=0x0FBB); Exodia set check Block1; conf: high

@ =============================================================================
@ file 07 Seg-7 additions: equip slot eligibility predicate card IDs
@ Source: asm/07_equip_effect_chain.s Seg-7 (0x080613b4..0x08061eb4)
@ =============================================================================
.equ REVERSAL_OF_GRAVES_CID,         0x000014f0  @ Reversal of Graves (pw=17484499; card-stats.s L13743 slot=0x14F0); Seg-7 DWORD_080613cc
.equ BLASTING_THE_RUINS_CID,         0x000016dc  @ Blasting the Ruins (pw=21466326; card-stats.s L18696 slot=0x16DC); Seg-7 DWORD_080613d0
.equ BURST_STREAM_OF_DESTRUCTION_CID, 0x0000175b @ Burst Stream of Destruction (pw=17655904; card-stats.s L20061 slot=0x175B); Seg-7 DAT_08061ad4
.equ SANCTUARY_IN_THE_SKY_CID,       0x0000175e  @ The Sanctuary in the Sky (pw=56433456; card-stats.s L20087 slot=0x175E); note SANCTUARY_CID_SHIFTED(0xbaf00000) is CID<<19 not raw CID; Seg-7 DAT_08061b90
.equ INFERNO_FIRE_BLAST_CID,         0x000017f6  @ Inferno Fire Blast (pw=52684508; card-stats.s L21686 slot=0x17F6); inline computed via adds r0,#0x9b from 0x175b in check_dragon_spell_target_slot_available; plate reference only
.equ PROTECTOR_OF_SANCTUARY_CID,     0x0000178b  @ Protector of the Sanctuary (pw=24221739; card-stats.s L20464 slot=0x178B); Seg-7 DWORD_08061dc0
.equ MASK_OF_RESTRICT_CID,           0x000013f2  @ Mask of Restrict (pw=29549364; card-stats.s L11234 slot=0x13F2); Seg-7 DWORD_08061c5c

@ =============================================================================
@ file 07 Seg-8 additions: equip slot eligibility predicate card IDs (disasm blocks)
@ Source: asm/07_equip_effect_chain.s Seg-8 (0x08061eb4..0x08062d28)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ MIND_WIPE_CID,      0x000017f3  @ Mind Wipe (pw=52817046; card-stats.s card_1664 slot=0x17F3); Block1 fn check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3; conf: high
.equ HEAVY_SLUMP_CID,    0x00001801  @ Heavy Slump (pw=52417194; card-stats.s card_1678 slot=0x1801); Block2-F2 fn check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801; conf: high
.equ MIND_HAXORZ_CID,    0x0000184d  @ Mind Haxorz (pw=75392615; card-stats.s card_1744 slot=0x184D); Block4 fn check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d; conf: high
.equ COVERING_FIRE_CID,  0x00001853  @ Covering Fire (pw=74458486; card-stats.s card_1750 slot=0x1853); Block5 fn check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853; conf: high

@ =============================================================================
@ file 07 Seg-9 additions: equip slot eligibility predicate card IDs (disasm blocks)
@ Source: asm/07_equip_effect_chain.s Seg-9 (0x08062d28..0x08063830)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ THREATENING_ROAR_CID,  0x00001886  @ Threatening Roar (pw=36361633; card-stats.s card_1797 slot=0x1886); Block A fn check_opp_active_player_duel_phase_leq3 shared CID; conf: high
.equ HERO_BARRIER_CID,       0x0000195f  @ Hero Barrier (pw=44676200; card-stats.s card_4586 slot=0x195F); Block A fn check_opp_active_player_duel_phase_leq3 shared CID; conf: high
.equ D_D_DYNAMITE_CID,       0x0000188b  @ D.D. Dynamite (pw=08628798; card-stats.s card_1802 slot=0x188B); Block B fn check_opp_alt_hand_count_nonzero_for_cid_188b; conf: high
.equ DES_FROG_CID,           0x00001918  @ Des Frog (pw=84451804; card-stats.s card_1909 slot=0x1918); DWORD_08063810 in check_field5_paired_slot_trio_complete param; sibling of TADPOLE_CID=0x1919; conf: high

@ =============================================================================
@ file 07 Seg-10 additions: equip slot eligibility predicate card IDs (disasm blocks + CID checks)
@ Source: asm/07_equip_effect_chain.s Seg-10 (0x08063830..0x080643e0)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ FIRE_DARTS_CID,        0x00001926  @ Fire Darts (pw=43061293; card-stats.s card_1923 slot=0x1926); Block1 fn check_zone_field0c_is_zero_for_player; conf: high
.equ CHTHONIAN_BLAST_CID,   0x0000195e  @ Chthonian Blast (pw=18271561; card-stats.s card_1964 slot=0x195E); Block3 fn check_slot_zone_code_and_link_field_for_cid_195e; conf: high
.equ SIMULTANEOUS_LOSS_CID, 0x00001976  @ Simultaneous Loss (pw=92219931; card-stats.s card_1987 slot=0x1976); Block4 fn check_either_player_lp_slot_active; conf: high
.equ EHERO_CLAYMAN_CID,     0x000018a8  @ Elemental Hero Clayman (pw=84327329; card-stats.s card_1815 slot=0x18A8); DWORD_08064068 clayman_pair check in check_slot_clayman_pair_in_active_chain; conf: high
.equ HERO_KID_CID,          0x000019a7  @ Hero Kid (pw=32679370; card-stats.s card_2016 slot=0x19A7); DWORD_080642a0 in check_slot_hero_kid_in_extra_deck; conf: high

@ =============================================================================
@ file 08 Seg-1 additions: equip LP delta dispatch card IDs
@ Source: asm/08_equip_oam_neodaed.s, Seg-1 (0x080643e0..0x0806544c)
@ dispatch_equip_lp_delta_by_card_id BST node card IDs.
@ All values verified against data/card-stats.s or confirmed unallocated.
@ =============================================================================
.equ DES_KOALA_CID,                    0x0000161d  @ Des Koala (pw=69579761; card_1589 slot=0x161D); write_equip_lp_delta_scaled_by_lp_count path
.equ WOODLAND_SPRITE_CID,              0x000013a8  @ Woodland Sprite (pw=06979239; card_1178 slot=0x13A8); write_equip_lp_delta_by_opponent_side dispatch
.equ cid_10fe,                         0x000010fe  @ unallocated slot 0x10fe; not in card-stats.s; dispatch_equip_lp_delta_by_card_id node
.equ cid_12e8,                         0x000012e8  @ unallocated slot 0x12e8; not in card-stats.s; dispatch node
.equ GRIGGLE_CID,                      0x000011c9  @ Griggle (pw=95744531; card_0393 slot=0x11C9); dispatch node
.equ REFLECT_BOUNDER_CID,              0x0000129a  @ Reflect Bounder (pw=02851070; card_0670 slot=0x129A); dispatch node
.equ GIFT_OF_MYSTICAL_ELF_CID,         0x0000137a  @ Gift of The Mystical Elf (pw=98299011; card_0788 slot=0x137A)
.equ RAIN_OF_MERCY_CID,                0x0000141f  @ Rain of Mercy (pw=66719324; card_0899 slot=0x141F)
.equ AMAZON_ARCHER_CID,                0x0000144b  @ Amazon Archer (pw=91869203; card_0944 slot=0x144B)
.equ MARIE_THE_FALLEN_ONE_CID,         0x00001459  @ Marie the Fallen One (pw=57579381; card_0948 slot=0x1459)
.equ DARK_MAGICIAN_TOME_CID,           0x00001467  @ Dark Magician's Tome of Black Magic (pw=67227834; card_0960 slot=0x1467)
.equ NIGHTMARE_WHEEL_CID,              0x000014b2  @ Nightmare Wheel (pw=54704216; card_1018 slot=0x14B2)
.equ ZOLGA_CID,                        0x000014f3  @ Zolga (pw=16268841; card_1068 slot=0x14F3)
.equ POISON_MUMMY_CID,                 0x00001525  @ Poison Mummy (pw=43716289; card_1096 slot=0x1525)
.equ TOON_CANNON_SOLDIER_CID,          0x00001565  @ Toon Cannon Soldier (pw=79875176; card_1128 slot=0x1565)
.equ SECRET_BARREL_CID,                0x000015f4  @ Secret Barrel (pw=27053506; card_1175 slot=0x15F4)
.equ INFERNO_CID,                      0x000016c5  @ Inferno (pw=74823665; card_1301 slot=0x16C5)
.equ STEALTH_BIRD_CID,                 0x000016fa  @ Stealth Bird (pw=03510565; card_1347 slot=0x16FA)
.equ GOBLIN_THIEF_CID,                 0x00001761  @ Goblin Thief (pw=45311864; card_1338 slot=0x1761)
.equ SOLAR_RAY_CID,                    0x00001767  @ Solar Ray (pw=44472639; card_1342 slot=0x1767)
.equ ELEPHANT_STATUE_CID,              0x00001794  @ Elephant Statue of Disaster (pw=12160911; card_1381 slot=0x1794)
.equ ANDRO_SPHINX_CID,                 0x000017c7  @ Andro Sphinx (pw=15013468; card_1442 slot=0x17C7)
.equ ELEMENTAL_HERO_FLAME_WINGMAN_CID, 0x000018c8  @ Elemental Hero Flame Wingman (pw=35809262; card_1688 slot=0x18C8)
.equ ROCK_BOMBARDMENT_CID,             0x000018da  @ Rock Bombardment (pw=20781762; card_1695 slot=0x18DA)
.equ MAGICAL_BLAST_CID,                0x00001984  @ Magical Blast (pw=91819979; card_1751 slot=0x1984)
.equ MEMORY_CRUSHER_CID,               0x000019cf  @ Memory Crusher (pw=48700891; card_2058 slot=0x19CF)
.equ GUARDIAN_EXODE_CID,               0x000019f0  @ Guardian Exode (pw=55737443; card_2064 slot=0x19F0)

@ =============================================================================
@ file 08 Seg-2 additions: equip effect handler card IDs
@ Source: asm/08_equip_oam_neodaed.s, Seg-2 (0x0806544c..0x08066448)
@ dispatch_equip_draw_counter_sprite_tick / tick_dragon_summon_effect_display_state_machine
@ All values verified against data/card-stats.s slot_id field.
@ =============================================================================
.equ TIME_WIZARD_CID,                  0x00000fb6  @ Time Wizard (pw=71625222; card_0016 slot=0x0FB6); fn_eligible handler via handler table 0x09e4631c
.equ DRAGON_CAPTURE_JAR_CID,           0x000010ef  @ Dragon Capture Jar (pw=50045299; card_0291 slot=0x10EF); drive_equip_slot_bitmap_or_activation_scan dispatch
.equ DARK_RABBIT_CID,                  0x00001126  @ Dark Rabbit (pw=99261403; card_0341 slot=0x1126); write_equip_lp_delta_dark_rabbit handler
.equ SKELENGEL_CID,                    0x000011c2  @ Skelengel (pw=60694853; card_0450 slot=0x11C2); dispatch_equip_draw_counter_sprite_tick dispatch
.equ FLUTE_SUMMONING_DRAGON_CID,       0x000012ca  @ The Flute of Summoning Dragon (pw=43973174; card_0651 slot=0x12CA); tick_dragon_summon_effect dispatch
.equ AIRKNIGHT_PARSHATH_CID,           0x0000139f  @ Airknight Parshath (pw=18036057; card_0816 slot=0x139F); dispatch_equip_draw_counter_sprite_tick dispatch
.equ CARD_OF_SAFE_RETURN_CID,          0x00001403  @ Card of Safe Return (pw=57953380; card_0878 slot=0x1403); dispatch_equip_draw_counter_sprite_tick dispatch
.equ DES_LACOODA_CID,                  0x00001533  @ Des Lacooda (pw=02326738; card_1112 slot=0x1533); dispatch_equip_draw_counter_sprite_tick dispatch
.equ CALL_OF_THE_MUMMY_CID,            0x0000153b  @ Call of the Mummy (pw=04861205; card_1119 slot=0x153B); tick_dragon_summon_effect dispatch
.equ HIDDEN_SOLDIER_CID,               0x00001572  @ Hidden Soldier (pw=02916282; card_1149 slot=0x1572); tick_dragon_summon_effect dispatch
.equ PRECIOUS_CARDS_FROM_BEYOND_CID,   0x00001662  @ Precious Cards from Beyond (pw=68304813; card_1338 slot=0x1662); dispatch_draw_counter; NOTE: same value as CARD_STAT_LP_THRESHOLD_5730 (L85) -- distinct semantic domain (CID vs LP threshold)
.equ MOLTEN_ZOMBIE_CID,                0x000016f7  @ Molten Zombie (pw=04732017; card_1456 slot=0x16F7); dispatch_equip_draw_counter_sprite_tick dispatch
.equ DON_TURTLE_CID,                   0x000016fd  @ Don Turtle (pw=03493978; card_1462 slot=0x16FD); tick_dragon_summon_effect dispatch
.equ AVATAR_OF_THE_POT_CID,            0x00001748  @ Avatar of The Pot (pw=99284890; card_1523 slot=0x1748); dispatch_equip_draw_counter_sprite_tick dispatch
.equ ATOMIC_FIREFLY_CID,               0x0000174e  @ Atomic Firefly (pw=83887306; card_1529 slot=0x174E); write_equip_lp_delta_atomic_firefly handler
.equ MAGNET_CIRCLE_LV2_CID,            0x000019ac  @ Magnet Circle LV2 (pw=84327329; card_2021 slot=0x19AC); tick_dragon_summon_effect dispatch
.equ CHAINSAW_INSECT_CID,              0x000019c7  @ Chainsaw Insect (pw=77252217; card_2042 slot=0x19C7); dispatch_equip_draw_counter_sprite_tick dispatch

@ =============================================================================
@ file 08 Seg-3 additions: dispatch_equip_zone_sprite_by_slot_state cluster
@ Source: asm/08_equip_oam_neodaed.s, Seg-3 (0x08066448..0x08067160)
@ =============================================================================
.equ DE_SPELL_CID,                     0x000012eb  @ De-Spell (pw=19159413; card_0673 slot=0x12EB); dispatch_equip_zone_sprite_by_slot_state second card-id check; value grep=0 (new)
.equ CYBER_STEIN_CID,                  0x0000114a  @ Cyber-Stein (pw=69015963; card_0361 slot=0x114A); dispatch_equip_oam_by_zone_state_with_cyberstein state=0x7e cmp; value grep=0 (new)
.equ ICID_RESERVED_A,                  0x0000162c  @ Internal CID 0x162c (cid=0xFFFF reserved slot, no card-stats.s entry); dispatch_zone_state_for_reserved_icid_slot; value grep=0 (new)
.equ ICID_RESERVED_B,                  0x0000184c  @ Internal CID 0x184c (cid=0xFFFF reserved slot, no card-stats.s entry); dispatch_zone_state_for_reserved_icid_slot; value grep=0 (new)
.equ ICID_RESERVED_C,                  0x00001051  @ Internal CID 0x1051 (cid=0xFFFF reserved slot, no card-stats.s entry); dispatch_zone_state_for_reserved_icid_slot; value grep=0 (new)

@ =============================================================================
@ file 08 Seg-4 additions: dispatch_effect_zone_lp_sprites_by_slot_flags cluster
@ Source: asm/08_equip_oam_neodaed.s, Seg-4 (0x08067160..0x08067fa4)
@ Domain-crited constants: CARD_FIELD3_THRESHOLD_1499/1500 (field3=ATK AI targeting threshold)
@ are domain-distinct from FIELD5_SCORE_THRESHOLD_1499 (field5 score gate) and
@ CARD_STAT_LP_THRESHOLD_1500/LP_COST_1500 (LP domain); per-slot data-equate only.
@ =============================================================================
.equ SOUL_ABSORBING_BONE_TOWER_CID, 0x00001744  @ Soul-Absorbing Bone Tower (pw=63012333; card_1523 slot=0x1744); enqueue_equip_zone_sprite_with_deck_count deck-count=2; value grep=0 (new)
.equ MALICE_ASCENDANT_CID,          0x000019d0  @ Malice Ascendant (pw=14255590; card_2070 slot=0x19D0); enqueue_equip_zone_sprite_with_deck_count count_extra_deck_cards_by_id; value grep=0 (new)
.equ CARD_FIELD3_THRESHOLD_1499,    0x000005db  @ field3(ATK) targeting threshold 1499; Crush Card Virus: field3>1499 -> target; field3(ATK)-domain distinct from FIELD5_SCORE_THRESHOLD_1499(score) and LP thresholds; tick_equip_head_slot_sprite_state_machine 3 slots
.equ CARD_FIELD3_THRESHOLD_1500,    0x000005dc  @ field3(ATK) targeting threshold 1500; Deck Devastation Virus: field3_raw<=1500 -> target; field3(ATK)-domain distinct from CARD_STAT_LP_THRESHOLD_1500(LP render)/LP_COST_1500(LP cost); tick_equip_head_slot_sprite_state_machine 3 slots

@ =============================================================================
@ file 08 Seg-5 additions: equip OAM sprite dispatch CIDs
@ Source: asm/08_equip_oam_neodaed.s, Seg-5 (0x08067fa4..0x080690dc)
@ All values verified against data/card-stats.s slot_id field.
@ =============================================================================
.equ BLAST_SPHERE_CID,              0x00001286  @ Blast Sphere (pw=26302522; card-stats.s L7763 slot=0x1286); invoke_equip_zone_entry_with_lp_chain_state card_id branch; conf: high
.equ BIRDFACE_CID,                  0x0000139d  @ Birdface (pw=45547649; card-stats.s L10597 slot=0x139D); tick_equip_effect_display_state_machine caseD_7f named card branch; conf: high
.equ IMPERIAL_ORDER_CID,            0x00001360  @ Imperial Order (pw=61740673; card-stats.s L9986 slot=0x1360); fn_eligible slot for check_equip_eligible_always_false stub; conf: high

@ =============================================================================
@ file 08 Seg-6 additions: equip/activation sprite CIDs
@ Source: asm/08_equip_oam_neodaed.s, Seg-6 (0x080690dc..0x0806a118)
@ All values verified against data/card-stats.s slot_id field or confirmed unallocated.
@ =============================================================================
.equ WIDESPREAD_RUIN_CID,          0x00001254  @ Widespread Ruin (pw=77754944; card-stats.s slot=0x1254); tick_equip_multi_card_score_state_machine CID check; conf: high
.equ BOTTOMLESS_SHIFTING_SAND_CID, 0x00001540  @ Bottomless Shifting Sand (pw=76532077; card-stats.s slot=0x1540); 0xaa<<5=0x1540 imm-encoded in tick_equip_multi_card_score_state_machine; conf: high
.equ HAMMER_SHOT_CID,              0x000017f2  @ Hammer Shot (pw=26412047; card-stats.s slot=0x17F2); tick_equip_multi_card_score_state_machine CID check; conf: high
.equ cid_12da,                     0x000012da  @ unallocated slot 0x12da; not in card-stats.s (gap 0x12D7..0x12DC: Tragedy=0x12D7, Ectoplasmer=0x12DC); fn_eligible handler at 0x080696d8; dispatch table 0x09e3fba4; conf: high

@ =============================================================================
@ file 08 Seg-9 additions: trap card CIDs used in equip LP sprite dispatch
@ Source: asm/08_equip_oam_neodaed.s, Seg-9 (0x0806cbe8..0x0806d960)
@ dispatch_equip_lp_sprite_by_trap_card_id + submit_ring_of_destruction_lp_indicators_if_zone_matched
@ All values verified against data/card-stats.s slot_id field.
@ =============================================================================
.equ RING_OF_DESTRUCTION_CID,     0x0000138d  @ Ring of Destruction (pw=83555666; card-stats.s card_0802 slot=0x138D); submit_ring_of_destruction_lp_indicators_if_zone_matched CID dispatch
.equ MAGIC_CYLINDER_CID,          0x00001404  @ Magic Cylinder (pw=62279055; card-stats.s card_0879 slot=0x1404); dispatch_equip_lp_sprite_by_trap_card_id BST dispatch
.equ DRAINING_SHIELD_CID,         0x0000176a  @ Draining Shield (pw=43250041; card-stats.s card_1554 slot=0x176A); dispatch_equip_lp_sprite_by_trap_card_id second BST target

@ =============================================================================
@ file 08 Seg-10 additions: Neo Space OAM effect CIDs + fn_eligible CIDs
@ Source: asm/08_equip_oam_neodaed.s, Seg-10 (0x0806d960..0x0806e76c)
@ tick_neo_space_oam_seq_by_card_id + fn_eligible handlers for CID=0x13ed/0x13fe
@ Values verified against data/card-stats.s or confirmed as category codes beyond card range.
@ =============================================================================
.equ GAP_CID_13ED,                0x000013ed  @ CID 0x13ed = card_5101 = card_stat_zero (unallocated slot). fn_eligible handler at 0x0806dbcc; dispatch table 0x09e406c4: CID@+8=0x13ed. Adjacent to GAP_CID_13EA=0x13ea; conf: high
.equ MULTIPLICATION_OF_ANTS_CID,  0x000013fc  @ Multiplication of Ants (card_stat_zero slot=0x13fc). tick_neo_space_oam_seq_by_card_id BST case-match. Plate L22365: CARD_ID_Multiplication_of_Ants=0x13fc; conf: high (plate authority)
.equ NEO_SPACE_SPAWN_CAT_1422,    0x00001422  @ Neo Space spawn category code 0x1422 (card_5154=card_stat_zero). Category for Multiplication of Ants spawn group. tick_neo_space_oam_seq_by_card_id; conf: high (category use beyond card range)
.equ NEO_SPACE_SPAWN_CAT_1813,    0x00001813  @ Neo Space spawn category code 0x1813 (CID 6163 > max card 5169 = beyond card range). Category for The Blockman effect group; conf: high (beyond card range)
.equ NEO_SPACE_SPAWN_CAT_19BA,    0x000019ba  @ Neo Space spawn category code 0x19ba (CID 6586 > max card range). Category for Phantasmal Martyrs group; conf: high (beyond card range)

@ =============================================================================
@ file 09 Seg-1 additions: equip LP display CIDs + reserved internal CIDs
@ Source: asm/09_equip_lp_display.s, Seg-1 (0x0806e76c..0x0806ff50)
@ All values verified against data/card-stats.s or confirmed unallocated (CID=0xFFFF).
@ =============================================================================
.equ BIG_MARCH_OF_ANIMALS_CID,  0x00001882  @ The Big March of Animals (card_1795 pw=01689516); enqueue_slot_sprites_by_card_id_scoring scoring branch; conf: high
.equ CREATURE_SWAP_CID,         0x0000142a  @ Creature Swap (card_0910 pw=31036355); Block1 FS handler fn_eligible CID=0x142a at 0x0806f008; conf: high
.equ ICID_RESERVED_D,           0x0000144c  @ reserved internal CID (CID=0xFFFF, not in card-stats.s); dispatch_hand_card_slot_sprite_by_state_and_card_id BST state 0x80/0x7e; conf: high
.equ ICID_RESERVED_E,           0x00001452  @ reserved internal CID (CID=0xFFFF, not in card-stats.s); sibling of ICID_RESERVED_D in same BST; conf: high

@ =============================================================================
@ file 09 Seg-2 additions: equip LP/zone dispatch CIDs + Bazoo fn_eligible
@ Source: asm/09_equip_lp_display.s, Seg-2 (0x0806ff50..0x0807104c)
@ All values verified against data/card-stats.s slot_id field (pw cross-checked).
@ =============================================================================
.equ GUARDIAN_BAOU_CID,              0x0000164d  @ Guardian Baou (pw=73544866; card-stats.s slot=0x164d); enqueue_zone_sprite_by_special_monster_card_id CID dispatch; conf: high
.equ LEGENDARY_FIEND_CID,            0x0000154d  @ Legendary Fiend (pw=99747800; card-stats.s slot=0x154d); enqueue_zone_sprite_by_special_monster_card_id CID dispatch; conf: high
.equ INSECT_PRINCESS_CID,            0x00001704  @ Insect Princess (pw=37957847; card-stats.s slot=0x1704); enqueue_zone_sprite_by_special_monster_card_id CID dispatch; conf: high
.equ AQUA_SPIRIT_CID,                0x00001485  @ Aqua Spirit (pw=40916023; card-stats.s slot=0x1485); dispatch_equip_lp_row_or_oam_by_state_and_hand_slot CID compare; conf: high
.equ THUNDER_CRASH_CID,              0x000016d7  @ Thunder Crash (pw=69196160; card-stats.s slot=0x16d7); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ ENCHANTED_ARROW_CID,            0x000014aa  @ Enchanted Arrow (pw=93260132; card-stats.s slot=0x14aa); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ TOKEN_THANKSGIVING_CID,         0x00001665  @ Token Thanksgiving (pw=57182235; card-stats.s slot=0x1665); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ TOKEN_FEASTEVIL_CID,            0x000018dc  @ Token Feastevil (pw=83675475; card-stats.s slot=0x18dc); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ GRYPHONS_FEATHER_DUSTER_CID,    0x0000170f  @ Gryphon's Feather Duster (pw=34370473; card-stats.s slot=0x170f); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ CYCLONE_BOOMERANG_CID,          0x000019b0  @ Cyclone Boomerang (pw=29612557; card-stats.s slot=0x19b0); tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf: high
.equ BAZOO_THE_SOUL_EATER_CID,       0x00001482  @ Bazoo the Soul-Eater (pw=40133511; card-stats.s slot=0x1482); fn_eligible stub at 0x08070478; FS table ref at GBA:0x09e46658; conf: high

@ =============================================================================
@ file 09 Seg-3 additions: equip chain dispatch / fn_eligible CIDs
@ Source: asm/09_equip_lp_display.s, Seg-3 (0x0807104c..0x080719fc)
@ =============================================================================
.equ FREED_THE_MATCHLESS_GENERAL_CID, 0x000014c4  @ Freed the Matchless General (pw=49681811; card-stats.s card_1013 slot=0x14C4); dispatch_equip_chain_state_if_tile_count_valid chain check param; conf: high
.equ DRAGGED_DOWN_INTO_GRAVE_CID,     0x000014e8  @ Dragged Down into the Grave (pw=16435215; card-stats.s card_1048 slot=0x14E8); Block1 FS handler fn_eligible CID ref @GBA:0x09e40e94; conf: high

@ =============================================================================
@ file 09 Seg-4a additions: Spirit monster CIDs for dispatch_spirit_monster_zone_sprite_by_card_id
@ Source: asm/09_equip_lp_display.s, Seg-4a (0x080719fc..0x08072404)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ YATA_GARASU_CID,         0x000014ff  @ Yata-Garasu (pw=03078576; card-stats.s card_1066 slot=0x14FF); dispatch_spirit_monster_zone_sprite_by_card_id BST: -> enqueue_spirit_zone_sprite_with_lp_check; conf: high
.equ YAMATA_DRAGON_CID,       0x00001501  @ Yamata Dragon (pw=76862289; card-stats.s card_1068 slot=0x1501); dispatch_spirit_monster_zone_sprite_by_card_id BST: -> dispatch_equip_draw_counter_sprite_tick; conf: high
.equ HINO_KAGU_TSUCHI_CID,    0x00001504  @ Hino-Kagu-Tsuchi (pw=75745607; card-stats.s card_1071 slot=0x1504); dispatch_spirit_monster_zone_sprite_by_card_id BST: -> enqueue_spirit_zone_sprite_type11; conf: high
.equ FENGSHENG_MIRROR_CID,    0x00001509  @ Fengsheng Mirror (pw=37406863; card-stats.s card_1076 slot=0x1509); fn_eligible stub at 0x08071f58; FS table ref at GBA:0x09e40f58; conf: high
.equ DARK_DUST_SPIRIT_CID,    0x00001526  @ Dark Dust Spirit (pw=89111398; card-stats.s card_1100 slot=0x1526); dispatch_spirit_monster_zone_sprite_by_card_id BST: -> submit_equip_zone_bitmap_pair_update; conf: high

@ =============================================================================
@ file 09 Seg-4b additions: fn_eligible CIDs for card effect handler dispatch
@ Source: asm/09_equip_lp_display.s, Seg-4b (0x08072404..0x08072d20)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ FIEND_COMEDIAN_CID,      0x0000151d  @ Fiend Comedian (pw=81172176; card-stats.s L14210 slot=0x151d); fn_eligible_fiend_comedian_2404 stub; FS table THUMB+1 ref at GBA:0x09e41078; conf: high
.equ LAST_TURN_CID,           0x0000151e  @ Last Turn (pw=28566710; card-stats.s L14212 slot=0x151e); fn_eligible_last_turn_2540 stub; FS table THUMB+1 ref at GBA:0x09e41090; conf: high

@ =============================================================================
@ file 09 Seg-5a additions: equip oam placeable card CIDs + token result CIDs
@ Source: asm/09_equip_lp_display.s, Seg-5a (0x08072d20..0x08073a5c)
@ setup_equip_oam_by_placeable_card_id_and_zone BST: input card_id -> result token card_id mapping.
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ STATUE_OF_THE_WICKED_CID, 0x00001543  @ Statue of the Wicked (pw=90928333; card-stats.s L14666 slot=0x1543); setup_equip_oam BST input CID; DWORD_08072f2c; conf: high
.equ TRAP_DUSTSHOOT_CID,       0x00001546  @ Trap Dustshoot (pw=64697231; card-stats.s L14705 slot=0x1546); fn_eligible_trap_dustshoot B1 FS THUMB+1 @GBA:0x09e411b0; conf: high
.equ TOKEN_13FB_CID,           0x000013fb  @ unnamed token slot (card-stats.s L27068 slot=0x13fb copy=0); setup_equip_oam BST result token CID; DWORD_08072f60; conf: high
.equ TOKEN_14FA_CID,           0x000014fa  @ unnamed token slot (card-stats.s L27120 slot=0x14fa copy=0); setup_equip_oam BST result token CID; DWORD_08072f68; conf: high
.equ TOKEN_154E_CID,           0x0000154e  @ unnamed token slot (card-stats.s L27133 slot=0x154e copy=0); setup_equip_oam BST result token CID; DWORD_08072f70; conf: high
.equ TOKEN_15BD_CID,           0x000015bd  @ unnamed token slot (card-stats.s L27146 slot=0x15bd copy=0); setup_equip_oam BST result token CID; DWORD_08072f78; conf: high
.equ TOKEN_15BE_CID,           0x000015be  @ unnamed token slot (card-stats.s L27159 slot=0x15be copy=0); setup_equip_oam BST result token CID; DWORD_08072f84; conf: high
.equ TOKEN_1603_CID,           0x00001603  @ unnamed token slot (card-stats.s L27172 slot=0x1603 copy=0); setup_equip_oam BST result token CID; DWORD_08072f8c; conf: high
.equ TOKEN_1639_CID,           0x00001639  @ unnamed token slot (card-stats.s L27185 slot=0x1639 copy=0); setup_equip_oam BST result token CID; DWORD_08072f94; conf: high
.equ TOKEN_195A_CID,           0x0000195a  @ unnamed token slot (card-stats.s L27250 slot=0x195a copy=0); setup_equip_oam BST result token CID; DWORD_08072fcc; conf: high
@ =============================================================================
@ file 09 Seg-5b additions: equip LP counter display state machine card IDs
@ Source: asm/09_equip_lp_display.s Seg-5b (0x08073a5c..0x08074338)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ RELOAD_CID,                  0x000016d9  @ Reload (pw=22589918; card-stats.s L18657 slot=0x16D9); tick_equip_lp_counter BST; DWORD_08074210; conf: high
.equ DISTURBANCE_STRATEGY_CID,    0x000015aa  @ Disturbance Strategy (pw=77561728; card-stats.s L15563 slot=0x15AA); tick_equip_lp_counter BST; DWORD_08074214; conf: high
@ =============================================================================
@ file 09 Seg-6 additions: equip zone dispatch + fn_eligible handler card IDs
@ Source: asm/09_equip_lp_display.s Seg-6 (0x08074338..0x080752cc)
@ All values verified against data/card-stats.s slot= fields.
@ =============================================================================
.equ DIMENSION_JAR_CID,           0x000015dd  @ Dimension Jar (pw=73414375; card-stats.s L16018 slot=0x15DD); fn_eligible handler via FS table 0x09e44290 THUMB+1 at 0x09e442a0; conf: high
@ =============================================================================
@ file 09 Seg-7 additions: fn_eligible handler card IDs (Emblem/Magical Dimension)
@ Source: asm/09_equip_lp_display.s Seg-7 (0x080752cc..0x0807629c)
@ All values verified against data/card-stats.s slot= fields.
@ FRIENDSHIP_CID=0x167a already exists at line 1071 (REUSE).
@ =============================================================================
.equ EMBLEM_OF_DRAGON_DESTROYER_CID, 0x00001629  @ Emblem of Dragon Destroyer (pw=06390406; card-stats.s L16811 slot=0x1629); fn_eligible B1 @ 0x08075378; FS THUMB+1 @ 0x09e41678; conf: high
.equ MAGICAL_DIMENSION_CID,          0x00001678  @ Magical Dimension (pw=28553439; card-stats.s L17552 slot=0x1678); fn_eligible B3 @ 0x08075d0c; FS THUMB+1 @ 0x09e41948; conf: high

@ =============================================================================
@ file 09 Seg-8 additions: fn_eligible handler CIDs + equip zone display CIDs
@ Source: asm/09_equip_lp_display.s, Seg-8 (0x0807629c..0x0807738c)
@ All values verified against data/card-stats.s slot= fields (0-hit in constants).
@ =============================================================================
.equ DARK_SCORPION_BURGLARS_CID, 0x00001531  @ Dark Scorpion Burglars (pw=40933924; card-stats.s slot=0x1531); check_effect_slot_card_type_flag_by_id BST; conf: high
.equ DD_SCOUT_PLANE_CID,         0x000016be  @ D. D. Scout Plane (pw=03773196; card-stats.s slot=0x16be); enqueue_equip_zone_sprite_with_neo_daedalus_and_chain BST; conf: high
.equ ENERGY_DRAIN_CID,           0x000016e3  @ Energy Drain (pw=56916805; card-stats.s slot=0x16e3); enqueue_effect_slot_sprite_by_card_id_score BST; conf: high
.equ GIFT_OF_THE_MARTYR_CID,     0x000018ca  @ Gift of the Martyr (pw=98792570; card-stats.s slot=0x18ca); enqueue_effect_slot_sprite_by_card_id_score BST; conf: high
.equ DEAL_OF_PHANTOM_CID,        0x00001492  @ Deal of Phantom (pw=69122763; card-stats.s slot=0x1492); enqueue_effect_slot_sprite_by_card_id_score plate ref only; computed at runtime as BARK_OF_DARK_RULER_CID(0x14be)-0x2c; no literal pool slot

@ =============================================================================
@ file 09 Seg-9a additions: fn_eligible handler CIDs (check_equip_activation_by_special_card_id)
@ Source: asm/09_equip_lp_display.s, Seg-9a (0x0807738c..0x08077c50)
@ All values verified 0-hit in constants/*.inc; passcodes from data/card-stats.s.
@ =============================================================================
.equ JADE_INSECT_WHISTLE_CID,    0x00001717  @ Jade Insect Whistle (pw=95214051; card-stats.s L47551 slot=0x1717); fn_eligible B4-embedded @ 0x08077b34; FS THUMB+1 @ 0x09e41de0; conf: high
.equ LEGENDARY_JUJITSU_MASTER_CID, 0x00001749  @ Legendary Jujitsu Master (pw=25773409; card-stats.s L48081 slot=0x1749); check_equip_activation_by_special_card_id zone13 test path; conf: high
.equ KANGAROO_CHAMP_CID,         0x00001866  @ Kangaroo Champ (pw=95789089; card-stats.s L51376 slot=0x1866); check_equip_activation_by_special_card_id activation check path; conf: high

@ =============================================================================
@ file 09 Seg-1 REMEDIATION Cluster-2 additions
@ Source: asm/09_equip_lp_display.s, [0x0806f85e..0x0806fef4)
@ eligible_destiny_board_f85c (CID=0x1468) / eligible_sub_stubs_fe88
@ =============================================================================
.equ CARD_DISPLAY_OP31_LP_BAR_SUB, 0x0000011d  @ sub-op arg 0x11d=285 to trigger_card_display_op31_if_not_active (0x08093390) LP-bar display path; eligible_sub_stubs_fe88 pool@0x6fed8; sibling r1=0x0d used in other path @0x6febc; conf: med
