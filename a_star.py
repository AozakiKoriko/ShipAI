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



