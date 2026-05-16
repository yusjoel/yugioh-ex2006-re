#!/usr/bin/env python3
# Update CSV for batch #66: set name column for 20 addresses
# If address missing from CSV, insert in sorted order

import csv
import io

CSV_PATH = "doc/dev/naming-proposals.csv"

UPDATES = {
    "0x0804444c": "dispatch_equip_zone_sprite_banisher_with_count_check",
    "0x0804448c": "dispatch_equip_zone_sprite_banisher_with_spell_check",
    "0x080445a4": "dispatch_equip_zone_sprite_banisher_by_field_count",
    "0x080a6630": "tick_equip_target_phase_with_lp_confirm_slot_context",
    "0x080a672c": "tick_equip_target_phase_with_lp_confirm_multistep",
    "0x080a689c": "tick_equip_card_phase_with_multi_state_machine",
    "0x080a6a20": "tick_equip_target_phase_with_bitmap_query_confirm",
    "0x080a6b38": "tick_equip_target_phase_with_bitmap_confirm",
    "0x080a6cc8": "tick_equip_multi_target_phase_with_slot_confirm",
    "0x080a7064": "dispatch_equip_phase_unless_activation_pending",
    "0x080a70ac": "tick_equip_sprite_enqueue_by_activation_flag",
    "0x080a70d8": "tick_equip_banisher_sprite_phase_by_combined_index",
    "0x080a7650": "tick_equip_ai_placement_phase_with_slot_filter",
    "0x080a78dc": "tick_equip_card_phase_by_7step_table",
    "0x080a7f4c": "tick_equip_card_phase_with_placement_apply",
    "0x080a81fc": "tick_equip_card_phase_by_activation_jump_table",
    "0x080a85d0": "tick_equip_card_phase_by_12step_table",
    "0x080a89f8": "tick_equip_card_phase_with_summon_type_dispatch",
    "0x080abbd8": "init_equip_slot_entry_with_copy_flag_sprite",
    "0x080abe54": "init_equip_slot_entry_with_placement_type_check",
}

def addr_int(s):
    return int(s, 16)

with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
data_rows = rows[1:]

# Build lookup by address (lowercase)
addr_to_idx = {}
for i, row in enumerate(data_rows):
    if row:
        addr_to_idx[row[0].lower()] = i

updated = 0
inserted = 0

for addr, name in UPDATES.items():
    addr_lower = addr.lower()
    if addr_lower in addr_to_idx:
        idx = addr_to_idx[addr_lower]
        row = data_rows[idx]
        # Ensure row has at least 5 columns
        while len(row) < 5:
            row.append("")
        row[1] = name
        data_rows[idx] = row
        updated += 1
        print(f"  Updated: {addr} -> {name}")
    else:
        # Insert new row in sorted order
        new_row = [addr, name, "", "", ""]
        # Find insertion point
        ins_pos = len(data_rows)
        addr_val = addr_int(addr)
        for i, row in enumerate(data_rows):
            if row and row[0].startswith("0x"):
                try:
                    if addr_int(row[0]) > addr_val:
                        ins_pos = i
                        break
                except ValueError:
                    pass
        data_rows.insert(ins_pos, new_row)
        # Rebuild lookup after insertion
        addr_to_idx = {}
        for i, row in enumerate(data_rows):
            if row:
                addr_to_idx[row[0].lower()] = i
        inserted += 1
        print(f"  Inserted: {addr} -> {name} at position {ins_pos}")

print(f"\nTotal: {updated} updated, {inserted} inserted")

# Write back
all_rows = [header] + data_rows
with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(all_rows)

print("CSV written successfully.")
