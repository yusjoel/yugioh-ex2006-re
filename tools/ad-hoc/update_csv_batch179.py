import csv

addrs = {
    '0x08063a6c': 'check_equip_slot_eligible_neo_daedalus_with_zone_pair_guard',
    '0x08063c14': 'check_equip_slot_eligible_neo_daedalus_with_lp_threshold',
    '0x08063e80': 'classify_neo_daedalus_placement_eligibility',
    '0x08063e94': 'check_equip_slot_eligible_neo_daedalus_with_offering_guard',
    '0x08063f28': 'check_equip_slot_eligible_neo_daedalus_with_lp_bit_guard',
    '0x08064074': 'check_equip_slot_eligible_neo_daedalus_with_chain_pair_score',
    '0x08064204': 'check_equip_slot_eligible_neo_daedalus_with_sacred_beast_pair',
    '0x080643e0': 'check_equip_slot_eligible_neo_daedalus_with_zero_active_equip',
    '0x08064418': 'dispatch_equip_slot_eligible_by_zone_type',
    '0x0806460c': 'check_equip_slot_eligible_via_effect_node_and_bitmap',
    '0x080655ec': 'submit_equip_lp_indicators_with_bar',
    '0x08066530': 'enqueue_graveyard_sprite_via_hand_slot_zone',
    '0x080665d4': 'dispatch_zone_state_for_reserved_icid_slot',
    '0x080666f4': 'render_equip_zone_sprites_both_players',
    '0x08066bf0': 'apply_effect_node_sprites_all_zones',
    '0x08066d68': 'enqueue_graveyard_sprite_for_polymerization_pair',
    '0x08066dac': 'evaluate_equip_zone_nodes_into_bitmap',
    '0x08066e0c': 'dispatch_equip_oam_by_zone_state_with_cyberstein',
    '0x08066ee0': 'tick_equip_activation_display_seq',
    '0x080672a4': 'dispatch_equip_oam_by_zone_state_with_bit2_gate',
}

csvpath = r'E:\Workspace\yugioh-ex2006-re\doc\dev\naming-proposals.csv'
rows = []
updated = set()
with open(csvpath, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for row in reader:
        if len(row) >= 2:
            addr = row[0].strip()
            if addr in addrs:
                old_name = row[1]
                row[1] = addrs[addr]
                updated.add(addr)
                print(f'Updated {addr}: {old_name!r} -> {row[1]!r}')
        rows.append(row)

with open(csvpath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

missing = set(addrs.keys()) - updated
if missing:
    print(f'MISSING from CSV: {missing}')
else:
    print(f'All {len(updated)} addresses updated in CSV')
