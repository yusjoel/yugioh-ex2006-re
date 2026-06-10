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
