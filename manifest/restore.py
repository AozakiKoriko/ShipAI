import json
import os

TEMP_INSTRUCTION_FILE = "temp_instruction.json"

# Initialize an 8x12 manifest with example container names
manifest = [
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['ca', 'hs', 'xs', 'je', 'iv', 'oe', '0', '0', '0', '0', '0', '0'],
    ['ca', 'hs', 'xs', 'je', 'iv', 'oe', '0', '0', '0', '0', '0', '0'],
    # Add additional rows as needed...
]

# Serialize and save temp_instruction to a file
def save_temp_instruction(manifest):
    with open(TEMP_INSTRUCTION_FILE, 'w') as file:
        json.dump(manifest, file)

# Deserialize and load temp_instruction from a file
def load_temp_instruction():
    if os.path.exists(TEMP_INSTRUCTION_FILE):
        with open(TEMP_INSTRUCTION_FILE, 'r') as file:
            return json.load(file)
    else:
        return None

# Update the manifest according to the instruction and save the state
def execute_instruction(instruction, manifest):
    # Example instruction: ('Move', 'ca', (2, 0), (1, 0))
    action, container, from_pos, to_pos = instruction
    if action == 'Move':
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        manifest[to_row][to_col] = manifest[from_row][from_col]
        manifest[from_row][from_col] = '0'
    # Save the current state after executing the instruction
    save_temp_instruction(manifest)

# Restore the system state from temp_instruction
def restore_state():
    temp_manifest = load_temp_instruction()
    if temp_manifest:
        print("Restoring the system state...")
        return temp_manifest
    else:
        print("No saved state to restore from.")

# Function to clear the temp_instruction after restoration
def clear_temp_instruction():
    if os.path.exists(TEMP_INSTRUCTION_FILE):
        os.remove(TEMP_INSTRUCTION_FILE)

# Example execution of instructions
instructions = [
    ('Move', 'ca', (2, 0), (1, 0)),
    ('Move', 'hs', (2, 1), (1, 1)),
    # Add additional instructions as needed...
]

# Execute instructions up to the point of power cutoff
for i, instruction in enumerate(instructions):
    if i == 2:  # Simulating a power cutoff on the 3rd instruction
        print("Power cutoff occurred during instruction:", i+1)
        break
    execute_instruction(instruction, manifest)

# Restore the manifest after a power cutoff
restored_manifest = restore_state()
if restored_manifest:
    manifest = restored_manifest

# Output the restored manifest
for row in manifest:
    print(row)

# Clear the temp_instruction file after successful restoration
clear_temp_instruction()
