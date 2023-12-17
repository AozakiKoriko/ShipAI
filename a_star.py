import heapq

def a_star(start_node, goal_reached, get_neighbors):
    open_set = []
    heapq.heappush(open_set, (start_node.f, start_node))
    closed_set = set()

    while open_set:
        current_f, current_node = heapq.heappop(open_set)

        if goal_reached(current_node.target_list, current_node.onload_list):
            return reconstruct_path(current_node)

        closed_set.add(current_node)

        for neighbor in get_neighbors(current_node, current_node.ship, current_node.target_list, current_node.block_list, current_node.onload_list, current_node.arm_loc):
            if neighbor in closed_set:
                continue

            tentative_g = current_node.g

            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.f = tentative_g + neighbor.h

                if (neighbor.f, neighbor) not in open_set:
                    heapq.heappush(open_set, (neighbor.f, neighbor))

    return None  

def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return path[::-1]  



