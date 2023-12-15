from a_star import a_star
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos
from neighbors import Node
from neighbors import get_neighbors
from neighbors import goal_reached

def find_block_list(array, target_list):
    target_ys = set(y for _, y in target_list)
    block_list = []
    for i in range(len(array)):
        if i != 8:
            for j in range(len(array[i])):
                if j in target_ys and array[i][j] != 0 and (i, j) not in target_list:
                    block_list.append((i, j))
    return block_list

manifest_path = "/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ship_cases/ShipCase2.txt"

# write cargo information to grid
cargos = parse_cargo_info( manifest_path )
grid = fill_grid_with_cargos(cargos)
initial_ship = grid

#user input targets
initial_target_list = [(0,3)]

#get block list
initial_block_list = find_block_list(initial_ship, initial_target_list)

#user input onload cargos
initial_onload_list = ["ONLOAD"]

#initial arm location, should not change
initial_arm_loc = (8,0)

initial_cost = 0

start_node = Node(initial_ship, initial_target_list, initial_block_list, initial_onload_list, initial_arm_loc, initial_cost)

path = a_star(start_node, goal_reached, get_neighbors)

for node in path:
    

    for row in reversed(node.ship):
        print(" ".join(str(item) for item in row))
    print("Arm:", node.arm_loc)
    print("Cost:", node.cost)
    print("-" * 20)  