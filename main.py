from algorithm import a_star
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos
from algorithm import reconstruct_path


manifest_path = "/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ship_cases/ShipCase1.txt"

# write cargo information to grid
cargos = parse_cargo_info( manifest_path )
grid = fill_grid_with_cargos(cargos)
initial_array = grid

#user input targets
initial_targets = [(0,1),(0,2),(0,3)]

#find initial blocks
target_ys = set(y for _, y in initial_targets)
initial_blocks = []
for i in range(len(grid)):
    if i != 8:
        for j in range(len(grid[i])):
            if j in target_ys and grid[i][j] != 0 and (i, j) not in initial_targets :
                initial_blocks.append((i, j))

#set initial position
initial_position = (8,0)

#user input onloads
initial_onloads = []

#set exit
des = (8,0)

#use a_star algorithm
path = a_star(initial_array, initial_targets, initial_blocks, initial_onloads, initial_position, des)
if path:
    print("Found a path!")
    for step in path:
        array, cost = step  # 提取 array, targets, blocks, current_position 和 cost
        for row in array:
            print(' '.join(map(str, row)))
            print("Cost:", cost)
        print()  
else:
    print("No path found.")
