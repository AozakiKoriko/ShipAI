import heapq
from neighbors import Node
from neighbors import goal_reached
from neighbors import get_neighbors

def a_star(start_node, goal_reached, get_neighbors):
    open_set = []
    heapq.heappush(open_set, (start_node.f, start_node))
    closed_set = set()

    while open_set:
        current_f, current_node = heapq.heappop(open_set)

        # 检查是否达到目标
        if goal_reached(current_node.target_list, current_node.onload_list):
            return reconstruct_path(current_node)

        closed_set.add(current_node)

        for neighbor in get_neighbors(current_node, current_node.ship, current_node.target_list, current_node.block_list, current_node.onload_list, current_node.arm_loc):
            if neighbor in closed_set:
                continue

            # 计算新的 g 值（父节点的 g + 从父节点到邻居的成本）
            tentative_g = current_node.g

            if tentative_g < neighbor.g:
                # 更新邻居的 g, h 和 f
                neighbor.g = tentative_g
                neighbor.f = tentative_g + neighbor.h

                # 把邻居加入开放集
                if (neighbor.f, neighbor) not in open_set:
                    heapq.heappush(open_set, (neighbor.f, neighbor))

    return None  # 如果没有找到路径，返回 None

def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return path[::-1]  # 反转路径


initial_ship = [
    [0, "A", "B", "C", 0, 0, 0, 0, 0, 0, 0, 0],
    [0, "D", "E", 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, "F", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

initial_target_list = [(0,2),(0,3)]
initial_block_list = [(1,2)]
initial_onload_list = ["X"]
initial_arm_loc = (8,0)
initial_cost = 0

    # 创建起始节点
start_node = Node(initial_ship, initial_target_list, initial_block_list, initial_onload_list, initial_arm_loc, initial_cost)

path = a_star(start_node, goal_reached, get_neighbors)

for node in path:
    
    # 打印 ship 二维数组
    for row in reversed(node.ship):
        print(" ".join(str(item) for item in row))
    print("Cost:", node.cost)
    print("-" * 20)  # 添加分隔符以区分不同节点的输出
