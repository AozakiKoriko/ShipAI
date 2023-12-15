from a_star import a_star
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos
from neighbors import Node
from neighbors import get_neighbors
from neighbors import goal_reached
import json

def find_block_list(array, target_list):
    min_i = min(i for i, _ in target_list)

    target_ys = set(y for _, y in target_list)
    block_list = []
    for i in range(len(array)):
        if i != 8 and i >= min_i:
            for j in range(len(array[i])):
                if j in target_ys and array[i][j] != 0 and (i, j) not in target_list:
                    block_list.append((i, j))
    return block_list


manifest_path = "/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ship_cases/ShipCase4.txt"

# write cargo information to grid
cargos = parse_cargo_info( manifest_path )
grid = fill_grid_with_cargos(cargos)
initial_ship = grid

#user input targets
initial_target_list = [(1,4)]

#get block list
initial_block_list = find_block_list(initial_ship, initial_target_list)
print(initial_block_list)

#user input onload cargos
initial_onload_list = ["ONLOAD"]

#initial arm location, should not change
initial_arm_loc = (8,0)

initial_cost = 0
initial_sel_loc = None
initial_move_loc = None

start_node = Node(initial_ship, initial_target_list, initial_block_list, initial_onload_list, initial_arm_loc, initial_sel_loc, initial_move_loc, initial_cost)

path = a_star(start_node, goal_reached, get_neighbors)

for node in path:
    for row in reversed(node.ship):
        print(" ".join(str(item) for item in row))
    print("Arm:", node.arm_loc)
    print("Move cargo from: ", node.sel_loc, "to ", node.mov_loc, ",cost: ", node.cost, "minutes.")
    print("-" * 20)  



def path_to_json(path):
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
        # "currentSteps": 1  
    }

    # write to json
    with open('output.json', 'w') as file:
        json.dump(output, file, indent=4)

path_to_json(path)
