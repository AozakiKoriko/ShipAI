from a_star import a_star
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos
from neighbors import Node
from neighbors import get_neighbors
from neighbors import goal_reached
import json
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sdssds5057')

# setting upload path
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def find_block_list(array, target_list):
    min_i = min(i for i, _ in target_list)

    target_ys = set(y for _, y in target_list)
    block_list = []
    for i in range(len(array)):
        if i != 8 and i > min_i:
            for j in range(len(array[i])):
                if j in target_ys and array[i][j] != 0 and array[i][j] != -1 and (i, j) not in target_list:
                    block_list.append((i, j))
    return block_list

def path_to_json(path, total_cost,upload_folder):
    steps = []
    for i, node in enumerate(path[1:], start=1):
        step = {
            "No": i,
            "target": None if isinstance(node.sel_loc, str) else node.sel_loc,
            "targetLoc": node.sel_loc if isinstance(node.sel_loc, str) else "ship",
            "dest": None if isinstance(node.mov_loc, str) else node.mov_loc,
            "destLoc": node.mov_loc if isinstance(node.mov_loc, str) else "ship",
            "cost": node.cost
        }
        steps.append(step)

    output = {
        "steps": steps,
        "currentSteps": None,
        "totalTime": total_cost,   
    }

    # write to json
    output_file_path = os.path.join(upload_folder, 'output.json')
    with open(output_file_path, 'w') as file:
        json.dump(output, file, indent=4)

# Output new_manifest
def write_cargo_info_to_file(cargos, file_path):
    with open(file_path, 'w') as file:
        for cargo in cargos:
            position = f"[{cargo.position[0]+1:02},{cargo.position[1]+1:02}]"
            weight = f"{{{cargo.weight:05}}}"
            name = cargo.name
            line = f"{position}, {weight}, {name}\n"
            file.write(line)

def onload_offload_algorithm(file_path, target_list, onload_list, cargos_weight):
    manifest_path = file_path
    # write cargo information to grid
    cargos = parse_cargo_info( manifest_path )
    grid = fill_grid_with_cargos(cargos)
    initial_ship = grid

    #user input targets
    initial_target_list = target_list

    #get block list
    block_list = []
    if initial_target_list:
        block_list = find_block_list(initial_ship, initial_target_list)
        initial_block_list = block_list
    else:
        initial_block_list = []

    #user input onload cargos
    initial_onload_list = onload_list

    #user input weight for onload cargos
    weight_list = cargos_weight

    #initial arm location, should not change
    initial_arm_loc = (8,0)

    initial_cost = 0
    initial_sel_loc = None
    initial_move_loc = None

    start_node = Node(initial_ship, initial_target_list, initial_block_list, initial_onload_list, initial_arm_loc, initial_sel_loc, initial_move_loc, initial_cost)

    path = a_star(start_node, goal_reached, get_neighbors)

    total_cost = 0
    for node in path:
        total_cost += node.cost
        if node.sel_loc == "truck":
            for i in cargos:
                if i.position == node.mov_loc:
                    i.name = node.ship[node.mov_loc[0]][node.mov_loc[1]]
                    i.weight = weight_list[0]
                    weight_list = weight_list[1:]
        elif node.mov_loc == "truck":
            for i in cargos:
                if i.position == node.sel_loc:
                    i.name = "UNUSED"
                    i.weight = 0
        else:
            for i in cargos:
                if i.position == node.mov_loc:
                    i.name = node.ship[node.mov_loc[0]][node.mov_loc[1]]
                    for j in cargos:
                        if j.position == node.sel_loc:
                            move_weight = j.weight
                    i.weight = move_weight
                elif i.position == node.sel_loc:
                    i.name = "UNUSED"
                    i.weight = 0
    # Write to json
    path_to_json(path,total_cost, app.config['UPLOAD_FOLDER'])

    output_file_path = 'updated_manifest.txt'
    write_cargo_info_to_file(cargos, output_file_path)

    return True 

# Function test

manifest_path = "/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ship_cases/ShipCase2.txt"
initial_target_list = [(2,0)]
initial_onload_list = ["XXX","YYY"]
weight_list = [100, 200]

onload_offload_algorithm(manifest_path, initial_target_list, initial_onload_list, weight_list)
