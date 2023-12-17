# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from array import *
import heapq
import copy
import json


class Container:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f"Container(name={self.name}, weight={self.weight})"

    def get_weight(self) -> float:
        return self.weight

    def get_name(self) -> str:
        return self.name

    def set_weight(self, weight):
        self.weight = weight

    def set_name(self, name):
        self.name = name


def manhattan_distance(x: array, y: array):
    val = abs(y[1] - x[1]) + abs(y[0] - x[0])
    return val


class Balancing:
    def __init__(self, container_array):
        height = len(container_array)
        self.start_array = container_array
        start_point = [height, 0]
        self.startNode = self.Node(start_point, 0, container_array, [], "place", 0)
        self.open_list = [self.startNode]
        self.closed_list = []

    class Node:
        def __init__(self, prev_slot, gn, slot_matrix, path, state: str, cost: int):
            self.curr_slot = prev_slot
            self.gn = gn
            self.slot_matrix = slot_matrix
            self.path = path
            self.state = state
            self.move_cost = cost
            self.hn = self.set_hn()
            self.fn = self.gn + self.hn
            self.intmatrix = int_type_matrix(slot_matrix)

        def calc_branch_gn(self, new_spot):
            return self.gn + manhattan_distance(self.curr_slot, new_spot) + self.additional_cost(new_spot)

        def set_hn(self):
            left_list = []
            left_weight = 0
            right_list = []
            right_weight = 0
            temp_hn = 0
            temp_matrix = self.slot_matrix
            half = int(len(temp_matrix[0]) / 2)
            for i in range(len(temp_matrix)):
                for j in range(len(temp_matrix[i])):
                    if temp_matrix[i][j].name != "UNUSED" and temp_matrix[i][j].name != "NAN":
                        if j < half:
                            left_list.append(temp_matrix[i][j].get_weight())
                            left_weight += temp_matrix[i][j].get_weight()
                        else:
                            right_list.append(temp_matrix[i][j].get_weight())
                            right_weight += temp_matrix[i][j].get_weight()
            if left_weight < right_weight:
                diff = right_weight - left_weight
                right_list.sort(reverse=True)
                while right_list:
                    if right_list[0] > diff:
                        right_list.pop(0)
                    else:
                        temp = right_list.pop(0)
                        diff = diff - temp
                        temp_hn += 1
            elif right_weight < left_weight:
                diff = left_weight - right_weight
                left_list.sort(reverse=True)
                while left_list:
                    if left_list[0] > diff:
                        left_list.pop(0)
                    else:
                        temp = left_list.pop(0)
                        diff = diff - temp
                        temp_hn += 1
            return temp_hn

        def get_gn(self):
            return self.gn

        def get_hn(self):
            return self.hn

        def get_fn(self):
            return self.fn

        def top_item(self, matrix, column):
            temp_matrix = matrix
            have_boxes = False
            for i in range(len(temp_matrix)):
                if temp_matrix[i][column].name != "UNUSED":
                    if temp_matrix[i][column].name != "NAN":
                        have_boxes = True
                    continue
                else:
                    if have_boxes == 0:
                        return None
                    return [i-1, column]
            return [i, column]

        def additional_cost(self, new_slot):
            if self.curr_slot[0] > new_slot[0]:
                height_1 = self.curr_slot[0]
            else:
                height_1 = new_slot[0]
            height_2 = height_1
            temp_matrix = self.slot_matrix
            break_out_flag = False
            for i in range(height_1, len(temp_matrix) + 1):
                if i == len(temp_matrix):
                    break
                count = 0
                limit = abs(new_slot[1] - self.curr_slot[1])
                if self.curr_slot[1] < new_slot[1]:
                    val_1 = self.curr_slot[1] + 1
                    val_2 = new_slot[1]
                elif self.curr_slot[1] > new_slot[1]:
                    val_1 = new_slot[1] + 1
                    val_2 = self.curr_slot[1]
                else:
                    return 0
                for j in range(val_1, val_2):
                    count = count + 1
                    if temp_matrix[i][j].name != "UNUSED":
                        height_2 = i + 1
                        break
                    if count == limit:
                        break_out_flag = True
                        break
                if break_out_flag:
                    break
            val = (height_2 - height_1) * 2
            return val

        def balance_check(self, balance_factor):
            left_weight = 0
            right_weight = 0
            temp_matrix = self.slot_matrix
            half = len(temp_matrix[0])/2
            for i in range(len(temp_matrix)):
                for j in range(len(temp_matrix[i])):
                    if j < half:
                        left_weight = left_weight + temp_matrix[i][j].get_weight()
                    else:
                        right_weight = right_weight + temp_matrix[i][j].get_weight()
            if ((left_weight == 0 and right_weight != 0)
                    or (left_weight != 0 and right_weight == 0)):
                return False
            elif (left_weight == 0 and right_weight == 0):
                return True
            else:
                if left_weight < right_weight:
                    return (left_weight / right_weight) > balance_factor
                elif left_weight >= right_weight:
                    return (right_weight / left_weight) > balance_factor

    def branching(self, cur_node: Node):
        num_of_columns = len(cur_node.slot_matrix[0])
        if cur_node.state == "place":
            temp_state = "pick"
            for column in range(num_of_columns):
                top_slot = cur_node.top_item(cur_node.slot_matrix, column)
                if top_slot and top_slot != cur_node.curr_slot:
                    new_gn = cur_node.calc_branch_gn(top_slot)
                    move_cost = new_gn - cur_node.gn
                    new_path = cur_node.path #+ "From " + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    temp_node = self.Node(top_slot, new_gn, cur_node.slot_matrix, new_path, temp_state, move_cost)
                    self.open_list.append(temp_node)
                    self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue
        else:
            temp_state = "place"
            for column in range(num_of_columns):
                new_matrix = copy.deepcopy(cur_node.slot_matrix)
                saved_container = new_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                new_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                top_slot = empty_slot(new_matrix, column)

                if top_slot and top_slot != cur_node.curr_slot:
                    new_gn = cur_node.calc_branch_gn(top_slot)
                    move_cost = cur_node.move_cost + new_gn - cur_node.gn
                    from_slot = [[cur_node.curr_slot[0] + 1, cur_node.curr_slot[1] + 1], "Ship"]
                    to_slot = [[top_slot[0]+1, top_slot[1]+1], "Ship"]
                    #new_path = cur_node.path + "Move container at [" + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    empty_container = new_matrix[top_slot[0]][top_slot[1]]
                    new_matrix[top_slot[0]][top_slot[1]] = saved_container
                    new_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = empty_container
                    #checker = int_type_matrix(new_matrix)
                    visual_matrix = generate_visible_cur_matrix(new_matrix)
                    new_path = copy.copy(cur_node.path)
                    new_path.append([from_slot, to_slot, move_cost, visual_matrix])
                    temp_node = self.Node(top_slot, new_gn, new_matrix, new_path, temp_state, 0)
                    if any(are_arrays_same(node.slot_matrix, new_matrix) for node in self.closed_list):
                        continue
                    else:
                        self.open_list.append(temp_node)
                        self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue

    def can_balance(self, balance_ratio=0.9):
        temp_matrix = self.start_array
        arr = []
        for i in range(len(temp_matrix)):
            for j in range(len(temp_matrix[i])):
                if temp_matrix[i][j].name != "UNUSED" and temp_matrix[i][j].name != "NAN":
                    arr.append(temp_matrix[i][j].weight)
        total_sum = sum(arr)
        target_min = balance_ratio * (total_sum / 2)
        target_max = total_sum / 2

        n = len(arr)
        checkers = [[False for _ in range(int(target_max) + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            checkers[i][0] = True
        for i in range(1, n + 1):
            for j in range(1, int(target_max) + 1):
                if arr[i - 1] <= j:
                    checkers[i][j] = checkers[i - 1][j] or checkers[i - 1][j - arr[i - 1]]
                else:
                    checkers[i][j] = checkers[i - 1][j]
        for j in range(int(target_min), int(target_max) + 1):
            if checkers[n][j]:
                return True
        return False

    def find_optimal_node(self):
        if not self.can_balance():
            nh = No_Branch_Hard_Blance(self.start_array)
            return nh.find_optimal_node()
        while True:
            if check_empty(self.start_array):
                return self.startNode
            if len(self.open_list) == 0:
                nh = No_Branch_Hard_Blance(self.start_array)
                return nh.find_optimal_node()
            n = self.open_list.pop(0)
            self.closed_list.append(n)
            if n.balance_check(0.9):
                return n
            self.branching(n)

class No_Branch_Hard_Blance:
    def __init__(self, start_array):
        self.start_array = start_array
        height = len(start_array)
        self.final_matrix = self.get_hard_balancing_result()
        self.buffer_size = (4, 24)
        buffer = [[Container("UNUSED", 0) for _ in range(self.buffer_size[1])] for _ in range(self.buffer_size[0])]
        start_point = [height, 0]
        last_array = self.get_hard_balancing_result()
        self.startNode = self.Node2(start_point, 0, start_array, [], "place", last_array, 0)
        self.open_list = [self.startNode]
        self.closed_list = []

    def sort_containers(self):
        filtered_containers = []
        for row in self.start_array:
            for container in row:
                if container.name not in ["UNUSED", "NAN"]:
                    filtered_containers.append(container)

        sorted_containers = sorted(filtered_containers, key=lambda c: c.weight, reverse=True)
        return sorted_containers

    def get_hard_balancing_result(self):
        sort_containers_list = self.sort_containers()
        new_matrix = copy.deepcopy(self.start_array)
        cols = len(new_matrix[0])

        for row in new_matrix:
            for i, container in enumerate(row):
                if container.name not in ["UNUSED", "NAN"]:
                    row[i] = Container("UNUSED", 0)

        if cols % 2 == 0:
            start = cols // 2 - 1
        else:
            start = cols // 2

        order = [start]
        left, right = start - 1, start + 1

        while left >= 0 or right < cols:
            if right < cols:
                order.append(right)
                right += 1
            if left >= 0:
                order.append(left)
                left -= 1

        for row in range(len(new_matrix)):
            for col in order:
                if sort_containers_list:
                    if new_matrix[row][col].name == "UNUSED":
                        new_matrix[row][col] = sort_containers_list.pop(0)

        return new_matrix

    class Node2:
        def __init__(self, prev_slot, gn, slot_matrix, path, state: str, result_array, move_cost: int):
            self.curr_slot = prev_slot
            self.gn = gn
            self.slot_matrix = slot_matrix
            self.result_array = result_array
            self.path = path
            self.state = state
            self.move_cost = move_cost
            self.height = len(slot_matrix)
            self.hn = self.set_hn()
            self.fn = self.gn + self.hn
            self.int_slot_matrix = int_type_matrix(slot_matrix)

        def get_gn(self):
            return self.gn

        def get_hn(self):
            return self.hn

        def get_fn(self):
            return self.fn

        def local_branch_gn(self, position, old_spot, new_spot):
            return self.gn + manhattan_distance(old_spot, new_spot) + self.additional_cost(position, old_spot, new_spot)

        def additional_cost(self, position, old_slot, new_slot):
            if old_slot[0] > new_slot[0]:
                height_1 = old_slot[0]
            else:
                height_1 = new_slot[0]
            height_2 = height_1
            if position == "slot":
                temp_matrix = self.slot_matrix
            elif position == "buffer":
                temp_matrix = self.buffer_matrix
            break_out_flag = False
            for i in range(height_1, len(temp_matrix) + 1):
                if i == len(temp_matrix):
                    break
                count = 0
                limit = abs(new_slot[1] - old_slot[1])
                if old_slot[1] < new_slot[1]:
                    val_1 = old_slot[1] + 1
                    val_2 = new_slot[1]
                elif old_slot[1] > new_slot[1]:
                    val_1 = new_slot[1] + 1
                    val_2 = old_slot[1]
                else:
                    return 0
                for j in range(val_1, val_2):
                    count = count + 1
                    if temp_matrix[i][j].name != "UNUSED":
                        height_2 = i + 1
                        break
                    if count == limit:
                        break_out_flag = True
                        break
                if break_out_flag:
                    break
            val = (height_2 - height_1) * 2
            return val

        #number of containers not correctly placed
        def set_hn(self):
            count = 0
            for row1, row2 in zip(self.result_array, self.slot_matrix):
                for container1, container2 in zip(row1, row2):
                    if container1.name not in ["UNUSED", "NAN"] and container2.name not in ["UNUSED", "NAN"]:
                        if container1.weight != container2.weight and container1.name != container2.weight:
                            count += 1
                    elif container1.name in ["UNUSED", "NAN"] and container2.name not in ["UNUSED", "NAN"]:
                        count += 1
                    elif container1.name not in ["UNUSED", "NAN"] and container2.name in ["UNUSED", "NAN"]:
                        count += 1
            return (count*100)

        def top_item(self, matrix, column):
            temp_matrix = matrix
            have_boxes = False
            for i in range(len(temp_matrix)):
                if temp_matrix[i][column].name != "UNUSED":
                    if temp_matrix[i][column].name != "NAN":
                        have_boxes = True
                    continue
                else:
                    if have_boxes == 0:
                        return None
                    return [i-1, column]
            if have_boxes:
                return [i, column]
            else:
                return None

        def same_result(self, result_matrix):
            for row1, row2 in zip(result_matrix, self.slot_matrix):
                for container1, container2 in zip(row1, row2):
                    if container1.weight != container2.weight :
                        return False
                    if container1.name != "UNUSED" or container1.name != "NAN":
                        if container2.name == "UNUSED" or container2.name == "NAN":
                            return False
            return True

        def balance_check(self):
            left_weight = 0
            right_weight = 0
            temp_matrix = self.slot_matrix
            half = len(temp_matrix[0])/2
            for i in range(len(temp_matrix)):
                for j in range(len(temp_matrix[i])):
                    if j < half:
                        left_weight = left_weight + temp_matrix[i][j].get_weight()
                    else:
                        right_weight = right_weight + temp_matrix[i][j].get_weight()
            if left_weight < right_weight:
                return right_weight - left_weight
            elif left_weight >= right_weight:
                return left_weight - right_weight

        def avoid_choosing_slot(self, loc):
            col = loc[1]
            end_row = loc[0]
            if end_row == 0:
                container1 = self.slot_matrix[end_row][col]
                container2 = self.result_array[end_row][col]
                if container1.name != container2.name or container1.weight != container2.weight:
                    return False
                else:
                    return True
            else:
                for row in range(0, end_row):
                    container1 = self.slot_matrix[row][col]
                    container2 = self.result_array[row][col]

                    if container1.name != container2.name or container1.weight != container2.weight:
                        return False

                return True


    def branching(self, cur_node: Node2):
        num_of_slot_columns = len(cur_node.slot_matrix[0])
        num_of_buffer_columns = self.buffer_size[1]
        last_matrix = cur_node.result_array
        if cur_node.state == "place":
            temp_state = "pick"
            # branch for slot
            for column in range(num_of_slot_columns):
                top_slot = cur_node.top_item(cur_node.slot_matrix, column)
                # Check if there exist item for that column, and check if it is the previously moved slot
                if top_slot and top_slot != cur_node.curr_slot and not cur_node.avoid_choosing_slot(top_slot):
                    new_gn = cur_node.local_branch_gn("slot", cur_node.curr_slot, top_slot)
                    move_cost = new_gn - cur_node.gn
                    new_path = cur_node.path #+ "From " + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    temp_node = self.Node2(top_slot, new_gn, cur_node.slot_matrix, new_path, temp_state, last_matrix, move_cost)
                    self.open_list.append(temp_node)
                    self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue

        else:
            temp_state = "place"
            # branch for slot
            for column in range(num_of_slot_columns):
                new_slot_matrix = copy.deepcopy(cur_node.slot_matrix)
                # Get saved container(need to find if it locates slot or matrix)
                saved_container = new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                top_slot = empty_slot(new_slot_matrix, column)

                if top_slot and top_slot != cur_node.curr_slot:
                    # Calculate moving cost for different
                    new_gn = cur_node.local_branch_gn("slot", cur_node.curr_slot, top_slot)
                    move_cost = cur_node.move_cost + new_gn - cur_node.gn
                    start_loc = "Ship"
                    from_slot = [[cur_node.curr_slot[0] + 1, cur_node.curr_slot[1] + 1], start_loc]
                    to_slot = [[top_slot[0]+1, top_slot[1]+1], "Ship"]
                    new_path = copy.copy(cur_node.path)
                    new_slot_matrix[top_slot[0]][top_slot[1]] = saved_container
                    visual_matrix = generate_visible_cur_matrix(new_slot_matrix)
                    new_path.append([from_slot, to_slot, move_cost, visual_matrix])
                    temp_node = self.Node2(top_slot, new_gn, new_slot_matrix, new_path, temp_state, cur_node.result_array, 0)
                    if any(are_arrays_same(node2.slot_matrix, new_slot_matrix) for node2 in self.closed_list):
                        continue
                    else:
                        self.open_list.append(temp_node)
                        self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue

    def find_optimal_node(self):
        result = self.get_hard_balancing_result()
        while True:
            if len(self.open_list) == 0:
                h = Hard_Blance(self.start_array)
                return h.find_optimal_node()
            n = self.open_list.pop(0)
            self.closed_list.append(n)
            if are_arrays_same(n.slot_matrix, result):
                return n
            self.branching(n)

class Hard_Blance:
    def __init__(self, start_array):
        self.start_array = start_array
        height = len(start_array)
        self.final_matrix = self.get_hard_balancing_result()
        self.buffer_size = (4, 24)
        buffer = [[Container("UNUSED", 0) for _ in range(self.buffer_size[1])] for _ in range(self.buffer_size[0])]
        start_point = [height, 0]
        last_array = self.get_hard_balancing_result()
        self.startNode = self.Node2(start_point, 0, start_array, [], "place", last_array, "slot", buffer, 0)
        self.open_list = [self.startNode]
        self.closed_list = []

    def sort_containers(self):
        filtered_containers = []
        for row in self.start_array:
            for container in row:
                if container.name not in ["UNUSED", "NAN"]:
                    filtered_containers.append(container)

        sorted_containers = sorted(filtered_containers, key=lambda c: c.weight, reverse=True)
        return sorted_containers

    def get_hard_balancing_result(self):
        sort_containers_list = self.sort_containers()
        new_matrix = copy.deepcopy(self.start_array)
        cols = len(new_matrix[0])

        for row in new_matrix:
            for i, container in enumerate(row):
                if container.name not in ["UNUSED", "NAN"]:
                    row[i] = Container("UNUSED", 0)

        if cols % 2 == 0:
            start = cols // 2 - 1
        else:
            start = cols // 2

        order = [start]
        left, right = start - 1, start + 1

        while left >= 0 or right < cols:
            if right < cols:
                order.append(right)
                right += 1
            if left >= 0:
                order.append(left)
                left -= 1

        for row in range(len(new_matrix)):
            for col in order:
                if sort_containers_list:
                    if new_matrix[row][col].name == "UNUSED":
                        new_matrix[row][col] = sort_containers_list.pop(0)

        return new_matrix

    class Node2:
        def __init__(self, prev_slot, gn, slot_matrix, path, state: str, result_array, position, buffer_matrix, cost:int):
            self.curr_slot = prev_slot
            self.gn = gn
            self.slot_matrix = slot_matrix
            self.buffer_matrix = buffer_matrix
            self.result_array = result_array
            self.position = position
            self.move_cost = cost
            self.path = path
            self.state = state
            self.height = len(slot_matrix)
            self.buffer_height = len(buffer_matrix)
            self.hn = self.set_hn()
            self.fn = self.gn + self.hn
            self.int_slot_matrix = int_type_matrix(slot_matrix)
            self.int_buffer_matrix = int_type_matrix(buffer_matrix)

        def get_gn(self):
            return self.gn

        def get_hn(self):
            return self.hn

        def get_fn(self):
            return self.fn

        def local_branch_gn(self, position, old_spot, new_spot):
            x = manhattan_distance(old_spot, new_spot)
            y = self.additional_cost(position, old_spot, new_spot)
            return self.gn + manhattan_distance(old_spot, new_spot) + self.additional_cost(position, old_spot, new_spot)

        def switch_branch_gn(self, buffer_spot, slot_spot):
            val = self.local_branch_gn("buffer", buffer_spot, [self.buffer_height,0]) + self.local_branch_gn("slot", slot_spot, [self.height,0]) + 4 -self.gn
            return val

        def additional_cost(self, position, old_slot, new_slot):
            if old_slot[0] > new_slot[0]:
                height_1 = old_slot[0]
            else:
                height_1 = new_slot[0]
            height_2 = height_1
            if position == "slot":
                temp_matrix = self.slot_matrix
            elif position == "buffer":
                temp_matrix = self.buffer_matrix
            break_out_flag = False
            for i in range(height_1, len(temp_matrix) + 1):
                if i == len(temp_matrix):
                    break
                count = 0
                limit = abs(new_slot[1] - old_slot[1])
                if old_slot[1] < new_slot[1]:
                    val_1 = old_slot[1] + 1
                    val_2 = new_slot[1]
                elif old_slot[1] > new_slot[1]:
                    val_1 = new_slot[1] + 1
                    val_2 = old_slot[1]
                else:
                    return 0
                for j in range(val_1, val_2):
                    count = count + 1
                    if temp_matrix[i][j].name != "UNUSED":
                        height_2 = i + 1
                        break
                    if count == limit:
                        break_out_flag = True
                        break
                if break_out_flag:
                    break
            val = (height_2 - height_1) * 2
            return val

        #number of containers not correctly placed
        def set_hn(self):
            count = 0
            count2 = 0
            for row1, row2 in zip(self.result_array, self.slot_matrix):
                for container1, container2 in zip(row1, row2):
                    if container1.name not in ["UNUSED", "NAN"] and container2.name not in ["UNUSED", "NAN"]:
                        if container1.weight != container2.weight and container1.name != container2.weight:
                            count += 1
                    elif container1.name in ["UNUSED", "NAN"] and container2.name not in ["UNUSED", "NAN"]:
                        count += 1
                    elif container1.name not in ["UNUSED", "NAN"] and container2.name in ["UNUSED", "NAN"]:
                        count += 1
            count = count * 100
            for col in range(len(self.buffer_matrix[0])):
                for row in self.buffer_matrix:
                    container = row[col]
                    if container.name not in ["UNUSED", "NAN"]:
                        count2 = col * 2
                        break
            return count + count2

        def top_item(self, matrix, column):
            temp_matrix = matrix
            have_boxes = False
            for i in range(len(temp_matrix)):
                if temp_matrix[i][column].name != "UNUSED":
                    if temp_matrix[i][column].name != "NAN":
                        have_boxes = True
                    continue
                else:
                    if have_boxes == 0:
                        return None
                    return [i-1, column]
            if have_boxes:
                return [i, column]
            else:
                return None

        def same_result(self, result_matrix):
            for row1, row2 in zip(result_matrix, self.slot_matrix):
                for container1, container2 in zip(row1, row2):
                    if container1.weight != container2.weight :
                        return False
                    if container1.name != "UNUSED" or container1.name != "NAN":
                        if container2.name == "UNUSED" or container2.name == "NAN":
                            return False
            return True

    def branching(self, cur_node: Node2):
        num_of_slot_columns = len(cur_node.slot_matrix[0])
        num_of_buffer_columns = self.buffer_size[1]
        last_matrix = cur_node.result_array
        if cur_node.state == "place":
            temp_state = "pick"
            # branch for slot
            for column in range(num_of_slot_columns):
                top_slot = cur_node.top_item(cur_node.slot_matrix, column)
                # Check if there exist item for that column, and check if it is the previously moved slot
                if top_slot and (top_slot != cur_node.curr_slot or (top_slot == cur_node.curr_slot and cur_node.position != "slot")):
                    if cur_node.position == "slot":
                        new_gn = cur_node.local_branch_gn("slot", cur_node.curr_slot, top_slot)
                    elif cur_node.position == "buffer":
                        new_gn = cur_node.switch_branch_gn(cur_node.curr_slot, top_slot)
                    move_cost = new_gn - cur_node.gn
                    new_path = cur_node.path #+ "From " + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    temp_node = self.Node2(top_slot, new_gn, cur_node.slot_matrix, new_path, temp_state, last_matrix, "slot", cur_node.buffer_matrix, move_cost)
                    self.open_list.append(temp_node)
                    self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue
            # branch for buffer
            for column in range(num_of_buffer_columns):
                top_slot = cur_node.top_item(cur_node.buffer_matrix, column)
                # Check if there exist item for that row, and check if it is the previously moved slot
                if top_slot and (top_slot != cur_node.curr_slot or (top_slot == cur_node.curr_slot and cur_node.position != "buffer")):
                    if cur_node.position == "buffer":
                        new_gn = cur_node.local_branch_gn("buffer", cur_node.curr_slot, top_slot)
                    elif cur_node.position == "slot":
                        new_gn = cur_node.switch_branch_gn(top_slot, cur_node.curr_slot)
                    move_cost = new_gn - cur_node.gn
                    new_path = cur_node.path #+ "From " + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    temp_node = self.Node2(top_slot, new_gn, cur_node.slot_matrix, new_path, temp_state, last_matrix, "buffer", cur_node.buffer_matrix, move_cost)
                    self.open_list.append(temp_node)
                    self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue
        else:
            temp_state = "place"
            # branch for slot
            for column in range(num_of_slot_columns):
                new_slot_matrix = copy.deepcopy(cur_node.slot_matrix)
                new_buffer_matrix = copy.deepcopy(cur_node.buffer_matrix)
                # Get saved container(need to find if it locates slot or matrix)
                if cur_node.position == "slot":
                    saved_container = new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                    new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                elif cur_node.position == "buffer":
                    saved_container = new_buffer_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                    new_buffer_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                top_slot = empty_slot(new_slot_matrix, column)

                if top_slot and (top_slot != cur_node.curr_slot or (top_slot == cur_node.curr_slot and cur_node.position != "slot")):
                    # Calculate moving cost for different
                    start_loc = ""
                    if cur_node.position == "slot":
                        new_gn = cur_node.local_branch_gn("slot", cur_node.curr_slot, top_slot)
                        start_loc = "Ship"
                    elif cur_node.position == "buffer":
                        new_gn = cur_node.switch_branch_gn(cur_node.curr_slot, top_slot)
                        start_loc = "Buffer"
                    move_cost = cur_node.move_cost + new_gn - cur_node.gn
                    from_slot = [[cur_node.curr_slot[0] + 1, cur_node.curr_slot[1] + 1], start_loc]
                    to_slot = [[top_slot[0]+1, top_slot[1]+1], "Ship"]
                    new_path = copy.copy(cur_node.path)
                    new_path.append([from_slot, to_slot, move_cost])
                    # new_path = cur_node.path + "Move container at [" + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    new_slot_matrix[top_slot[0]][top_slot[1]] = saved_container
                    #checker1 = int_type_matrix(new_slot_matrix)
                    #checker2 = int_type_matrix(new_buffer_matrix)
                    temp_node = self.Node2(top_slot, new_gn, new_slot_matrix, new_path, temp_state, cur_node.result_array, "slot", new_buffer_matrix, 0)
                    if any(are_arrays_same(node2.slot_matrix, new_slot_matrix) and
                           are_arrays_same(node2.buffer_matrix, new_buffer_matrix) for node2 in
                           self.closed_list):
                        continue
                    else:
                        self.open_list.append(temp_node)
                        self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue

            # branch for buffer(place at buffer)
            for column in range(num_of_buffer_columns):
                new_slot_matrix = copy.deepcopy(cur_node.slot_matrix)
                new_buffer_matrix = copy.deepcopy(cur_node.buffer_matrix)
                # Get saved container(need to find if it locates slot or matrix)
                if cur_node.position == "slot":
                    saved_container = new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                    new_slot_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                elif cur_node.position == "buffer":
                    saved_container = new_buffer_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]]
                    new_buffer_matrix[cur_node.curr_slot[0]][cur_node.curr_slot[1]] = Container("UNUSED", 0)
                top_slot = empty_slot(new_buffer_matrix, column)

                if top_slot and (top_slot != cur_node.curr_slot or (
                        top_slot == cur_node.curr_slot and cur_node.position != "buffer")):
                    # Calculate moving cost for different
                    start_location = ""
                    if cur_node.position == "slot":
                        new_gn = cur_node.switch_branch_gn(top_slot, cur_node.curr_slot)
                        start_location = "Ship"
                    elif cur_node.position == "buffer":
                        new_gn = cur_node.local_branch_gn("buffer", cur_node.curr_slot, top_slot)
                        start_location = "Buffer"
                    move_cost = cur_node.move_cost + new_gn - cur_node.gn
                    from_slot = [[cur_node.curr_slot[0] + 1, cur_node.curr_slot[1] + 1], cur_node.position]
                    to_slot = [[top_slot[0] + 1, top_slot[1] + 1], "Buffer"]
                    new_path = copy.copy(cur_node.path)
                    new_path.append([from_slot, to_slot, move_cost])
                    # new_path = cur_node.path + "Move container at [" + str(cur_node.curr_slot) + " to " + str(top_slot) + ".\n"
                    new_buffer_matrix[top_slot[0]][top_slot[1]] = saved_container
                    # checker1 = int_type_matrix(new_slot_matrix)
                    # checker2 = int_type_matrix(new_buffer_matrix)
                    temp_node = self.Node2(top_slot, new_gn, new_slot_matrix, new_path, temp_state, cur_node.result_array, "buffer", new_buffer_matrix, 0)
                    if any(are_arrays_same(node2.slot_matrix, new_slot_matrix) and
                           are_arrays_same(node2.buffer_matrix, new_buffer_matrix)for node2 in self.closed_list):
                        continue
                    else:
                        self.open_list.append(temp_node)
                        self.open_list.sort(key=lambda x: x.fn)
                else:
                    continue

    def find_optimal_node(self):
        result = self.get_hard_balancing_result()
        while True:
            if len(self.open_list) == 0:
                return None
            n = self.open_list.pop(0)
            self.closed_list.append(n)
            if are_arrays_same(n.slot_matrix,result):
                return n
            self.branching(n)

def int_type_matrix(matrix):
    int_matrix = [[container.get_weight() for container in row] for row in matrix]
    return int_matrix

def are_arrays_same(array1, array2):
    rows = len(array1)
    cols = len(array1[0])

    for i in range(rows):
        for j in range(cols):
            if array1[i][j].name != array2[i][j].name or array1[i][j].weight != array2[i][j].weight:
                return False
    return True

def empty_slot(matrix, column):
    for i in range(len(matrix)):
        if matrix[i][column].name == "UNUSED":
            return [i, column]
    return None

def check_empty(matrix):
    for row in matrix:
        for column in row:
            if column.get_name() not in ["UNUSED", "NAN"]:
                return False
    return True

def parse_line_to_container(line):
    parts = line.strip().split(', ')
    position = tuple(map(int, parts[0].strip('[]').split(',')))
    weight = int(parts[1].strip('{}'))
    name = parts[2]
    return position, Container(name, weight)

def generate_container_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    containers = {}
    max_row, max_col = 0, 0
    for line in lines:
        position, container = parse_line_to_container(line)
        row, col = position
        max_row = max(max_row, row)
        max_col = max(max_col, col)
        containers[position] = container

    matrix = [[None for _ in range(max_col)] for _ in range(max_row)]
    for position, container in containers.items():
        row, col = position
        matrix[row - 1][col - 1] = container

    return matrix

def generate_manifest(filename, container_array):
    with open(filename, 'w') as file:
        for row_index, row in enumerate(container_array):
            for col_index, container in enumerate(row):
                position = f"[{row_index+1:02d},{col_index+1:02d}]"
                weight = f"{{{container.weight:05d}}}"
                file.write(f"{position}, {weight}, {container.name}\n")

def generate_visible_cur_matrix(slot_matrix):
    array2D = []
    for row in slot_matrix:
        row_list = []
        for container in row:
            if container.name == "UNUSED":
                row_list.append("F")
            else:
                row_list.append("T")
        array2D.append(row_list)
    return array2D

def run(doc_path):
    file_path = doc_path
    container_matrix = generate_container_matrix(file_path)
    b = Balancing(container_matrix)
    N = b.find_optimal_node()
    if N:
        steps_data = N.path
        steps_json = []

        for index, step in enumerate(steps_data):
            step_json = {
                "No": index + 1,
                "target": [int(step[0][0][0]), int(step[0][0][1])],
                "targetLoc": step[0][1],
                "dest": [int(step[1][0][0]), int(step[1][0][1])],
                "destLoc": step[1][1],
                "cost": step[2],
                "array": step[3]
            }
            steps_json.append(step_json)

        final_json_structure = {
            "steps": steps_json,
            "currentSteps": 1,
            "totalTime": N.get_gn()
        }

        if N.get_gn() == 0:
            return False

        json_output = json.dumps(final_json_structure, indent=4)
        with open('output_balance.json', 'w') as file:
            file.write(json_output)

        new_file_path = file_path[:-4] + "_Updated" + ".txt"
        generate_manifest(new_file_path, N.slot_matrix)

        #print(generate_visible_cur_matrix(N.slot_matrix))

        return True
    else:
        return False

