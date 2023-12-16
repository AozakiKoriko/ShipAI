import heapq

class Node:
    def __init__(self, ship, target_list, block_list, onload_list, arm_loc, sel_loc, mov_loc, cost, parent = None, g=0, h=0):
        self.ship = ship
        self.target_list = target_list
        self.block_list = block_list
        self.onload_list = onload_list
        self.arm_loc = arm_loc
        self.sel_loc = sel_loc
        self.mov_loc = mov_loc
        self.cost = cost
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
        

    def __lt__(self, other):
        return self.f < other.F

def man_dis(loc_1, loc_2):
    return abs(loc_1[0] - loc_2[0]) + abs(loc_1[1] - loc_2[1])

def point_dis(loc_1, loc_2, array):
    if abs(loc_1[1] - loc_2[1]) < 2:
        distance = man_dis(loc_1, loc_2)
    else:
        max_height = -1
        y_start = min(loc_1[1], loc_2[1])
        y_end = max(loc_1[1], loc_2[1]) + 1
        for x in range(len(array)):
            for y in range(y_start, y_end):
                if array[x][y] != 0:
                    max_height = max(max_height, x)
        height_dif = max_height - max(loc_1[0],loc_2[0])
        distance = 2*(1 + height_dif) + man_dis(loc_1, loc_2)
    return distance

def heuristic(target_list, block_list, exit):
    h = 0
    targets_total = 0
    for target in target_list:
        targets_total += man_dis(target, exit)
    blocks_total = 2*len(block_list)
    h = targets_total + blocks_total
    return h

def offload(ship, target_list, arm_loc, sel_loc, exit):
    new_ship = [row[:] for row in ship]
    new_ship[sel_loc[0]][sel_loc[1]] = 0 
    new_target_list = [i for i in target_list if i != sel_loc]
    new_arm_loc = "truck"
    if arm_loc == "truck":
        cost = 2 + man_dis(exit, sel_loc) + man_dis(sel_loc, exit) + 2
    elif arm_loc == exit:
        cost = man_dis(exit, sel_loc) + man_dis(sel_loc, exit) + 2
    else:
        cost = point_dis(arm_loc, sel_loc, ship) + man_dis(sel_loc, exit) + 2 
    return new_ship, new_target_list, new_arm_loc, cost

def move_block(ship, block_list, arm_loc, sel_loc, mov_loc, exit):
    new_ship = [row[:] for row in ship]
    new_ship[mov_loc[0]][mov_loc[1]] = new_ship[sel_loc[0]][sel_loc[1]]
    new_ship[sel_loc[0]][sel_loc[1]] = 0
    new_block_list = [i for i in block_list if i != sel_loc]
    new_block_list = [i for i in block_list if i != sel_loc]

    new_arm_loc = mov_loc
    if arm_loc == "truck":
        cost = 2 + man_dis(exit, sel_loc) + point_dis(sel_loc, mov_loc, ship)
    elif arm_loc == exit:
        cost = man_dis(exit, sel_loc) + point_dis(sel_loc, mov_loc, ship)
    else:
        cost = point_dis(arm_loc, sel_loc, ship) + point_dis(sel_loc, mov_loc, ship)
    return new_ship, new_block_list, new_arm_loc, cost

def onload(ship, onload_list, arm_loc, mov_loc, exit):
    new_ship = [row[:] for row in ship]
    new_ship[mov_loc[0]][mov_loc[1]] = onload_list[0]
    new_onload_list = onload_list[1:]
    new_arm_loc = mov_loc
    if arm_loc == "truck":
        cost = 2 + man_dis(exit, mov_loc)
    elif arm_loc == exit:
        cost = man_dis(exit, mov_loc)
    else:
        cost = man_dis(arm_loc, exit) + 4 + man_dis(exit, mov_loc)
    return new_ship, new_onload_list, new_arm_loc, cost

def block_list_renew(target_list, block_list, mov_loc):
    target_ys = set(y for _, y in target_list)
    if mov_loc[1] in target_ys:
        new_block_list = block_list + [mov_loc]
    else:
        new_block_list = block_list
    return new_block_list

def goal_reached(target_list, onload_list):
    return len(target_list) == 0 and len(onload_list) == 0

def get_neighbors(current_node, ship, target_list, block_list, onload_list, arm_loc):
    neighbors = []
    exit = (8,0)
    #Situation 1: no cargos need offload and some cargos need onload
    if len(target_list) == 0 and len(onload_list) != 0:

        mov_loc = None
        min_distance = 9999
        for x in range(len(ship)):
            for y in range(len(ship[0])):
                if 0 <= x < len(ship) and 0 <= y < len(ship[0]):
                    if ship[x][y] == 0 and (x == 0 or ship[x-1][y] != 0): 
                        distance = man_dis(exit, (x,y))
                        if distance < min_distance:
                            min_distance = distance
                            mov_loc = (x,y)
        
        new_ship, new_onload_list, new_arm_loc, cost = onload(ship, onload_list, arm_loc, mov_loc, exit)
        new_block_list = block_list_renew(target_list, block_list, mov_loc)

        new_h = heuristic(target_list, new_block_list, exit)
        
        new_node = Node(new_ship, target_list, new_block_list, new_onload_list, new_arm_loc, "truck", mov_loc, cost, current_node, cost, new_h)
        neighbors.append(new_node)
    
    
    elif len(target_list) != 0:
        #Situation 2: if arm are at truck and still have cargos need onload
        if arm_loc == "truck" and len(onload_list) != 0:

            mov_loc = None
            min_distance = 9999
            for x in range(len(ship)):
                for y in range(len(ship[0])):
                    if 0 <= x < len(ship) and 0 <= y < len(ship[0]):
                        if ship[x][y] == 0 and (x == 0 or ship[x-1][y] != 0):
                            distance = man_dis(exit, (x,y))
                            if distance < min_distance:
                                min_distance = distance
                                mov_loc = (x,y)
            new_ship, new_onload_list, new_arm_loc, cost = onload(ship, onload_list, arm_loc, mov_loc, exit)
            new_block_list = block_list_renew(target_list, block_list, mov_loc)

            new_h = heuristic(target_list, new_block_list, exit)
        
            new_node = Node(new_ship, target_list, new_block_list, new_onload_list, new_arm_loc, "truck", mov_loc, cost, current_node, cost, new_h)
            neighbors.append(new_node)
        

        else:

            found_target_without_block = False
            for i in target_list:
                if all(j[1] != i[1] for j in block_list):
                    sel_loc = i
                    found_target_without_block = True
                    break
        
            #Situation 2: if have cargos can directly offload (have't blocks)
            if found_target_without_block: 
                new_ship, new_target_list, new_arm_loc, cost = offload(ship, target_list, arm_loc, sel_loc, exit)

                new_h = heuristic(new_target_list, block_list, exit)

                new_node = Node(new_ship, new_target_list, block_list, onload_list, new_arm_loc, sel_loc, "truck", cost, current_node, cost, new_h)
                neighbors.append(new_node)
        
            #Situation 3: if haven't cargos can directly offload
            if not found_target_without_block:
                sel_loc = None
                mov_loc = None
                min_distance = 9999

                for i in block_list:
                    distance = man_dis(i, exit)
                    if distance < min_distance:
                        min_distance = distance
                        sel_loc = i
                
                min_distance = 9999
                for x in range(len(ship)):
                    for y in range(len(ship[0])):
                        if 0 <= x < len(ship) and 0 <= y < len(ship[0]):
                            if ship[x][y] == 0 and y != sel_loc[1] and (x == 0 or ship[x-1][y] != 0):
                                distance = point_dis(sel_loc, (x,y), ship)
                                if distance < min_distance:
                                    min_distance = distance
                                    mov_loc = (x,y)

                new_ship, new_block_list, new_arm_loc, cost = move_block(ship, block_list, arm_loc, sel_loc, mov_loc, exit)
                new_block_list = block_list_renew(target_list, new_block_list, mov_loc)

                new_h = heuristic(target_list,new_block_list,exit)
                
                new_node = Node(new_ship, target_list, new_block_list, onload_list, new_arm_loc, sel_loc, mov_loc, cost, current_node, cost, new_h)
                neighbors.append(new_node)
    
    return neighbors
        
        