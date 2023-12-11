import heapq

class Node:
    def __init__(self, array, targets, blocks, current_position, parent=None, g=0, h=0):
        self.array = array
        self.targets = targets
        self.blocks = blocks
        self.current_position = current_position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def heuristic(targets, des):
    # 计算所有 targets 到 des 的曼哈顿距离之和
    total_distance = 0
    for target in targets:
        total_distance += manhattan_distance(target, des)
    return total_distance

def goal_reached(targets):
    return len(targets) == 0

def reconstruct_path(node):
    path = []
    while node is not None:
        path.append((node.array, node.targets, node.blocks, node.current_position,node.g))
        node = node.parent
    return path[::-1]

def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def get_neighbors(array, targets, blocks, current_position, des):
    neighbors = []


    for target in targets:

        if all(block[1] != target[1] for block in blocks):
            new_array = [row[:] for row in array]  
            new_array[target[0]][target[1]] = 0  
            new_targets = [t for t in targets if t != target]
            cost = manhattan_distance(current_position, target) + manhattan_distance(target, des)
            new_position = des  
            new_node = Node(new_array, new_targets, blocks, new_position, g=cost)
            neighbors.append(new_node)
            break  

    if not neighbors:
        selected_block = min(blocks, key=lambda b: manhattan_distance(b, des))
        target_point = None
        min_distance = float('inf')

        selected_block_col = selected_block[1]

        # 遍历selected_block所在列的左侧和右侧列
        for col in [selected_block_col - 1, selected_block_col + 1]:
            if 0 <= col < len(array[0]):  # 确保列索引在数组范围内
                for x in range(len(array)):
                    if array[x][col] == 0 and (x == 0 or array[x-1][col] != 0):
                        distance = manhattan_distance(selected_block, (x, col))
                        if distance < min_distance:
                            min_distance = distance
                            target_point = (x, col)
                            print("select block: ", selected_block)
                            print("target point: ", target_point)

                if target_point is not None:
                    break  # 找到合适的target_point后退出外层循环

        if target_point:
            new_array = [row[:] for row in array]
            new_array[target_point[0]][target_point[1]] = new_array[selected_block[0]][selected_block[1]]
            new_array[selected_block[0]][selected_block[1]] = 0
            cost = manhattan_distance(current_position, selected_block) + manhattan_distance(selected_block, target_point)
            new_blocks = [b for b in blocks if b != selected_block]
            new_node = Node(new_array, targets, new_blocks, target_point, g=cost)
            neighbors.append(new_node)

    return neighbors


def a_star(initial_array, targets, blocks, initial_position, des):
    start_node = Node(initial_array, targets, blocks, initial_position)
    start_node.h = heuristic(targets, des)
    start_node.f = start_node.g + start_node.h

    open_set = []
    heapq.heappush(open_set, (start_node.f, start_node))

    closed_set = set()

    while open_set:
        current_f, current_node = heapq.heappop(open_set)
        
        print("当前处理的节点:", current_node.current_position, "具有 f 值:", current_f)
        for row in current_node.array:
            print(' '.join(map(str, row)))
        print()  # 打印一个空行以分隔不同的步骤

        if goal_reached(current_node.targets):
            
            return reconstruct_path(current_node)

        closed_set.add(current_node)

        neighbors = get_neighbors(current_node.array, current_node.targets, current_node.blocks, current_node.current_position, des)

        for neighbor in neighbors:
            
            if neighbor in closed_set:
                continue

            tentative_g = current_node.g 

            if tentative_g < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor.targets, des)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set:
                    heapq.heappush(open_set, (neighbor.f, neighbor))
                    

    return None


initial_array =[
    [-1,"A", "B","E"],
    [0, "D", "C", 0],
    [0, "F", 0, 0],
    [0, 0, 0, 0]
]
initial_targets = [(0,1),(0,2),(0,3)]
initial_blocks = [(1,1),(1,2),(2,1)]
initial_position = (3,0)
des = (3,0)

path = a_star(initial_array, initial_targets, initial_blocks, initial_position, des)
if path:
    print("Found a path!")
    for step in path:
        array, targets, blocks, current_position, cost = step  # 提取 array, targets, blocks, current_position 和 cost
        for row in array:
            print(' '.join(map(str, row)))
        print()  # 打印一个空行以分隔不同的步骤
else:
    print("No path found.")




