import numpy as np
from Wall import walls

# Διαπερατότητα υαλοπίνακα
T = 0.8

# Ποσοστό 10% επί της ακτινοβολίας
M = 0.1

q_list = []


def get_value_from_item_count(i_pos, m_list, u_list):
    m = m_list[i_pos][1]
    first_u = u_list[i_pos][1]
    second_u = u_list[i_pos + 1][1]
    total = m + first_u + second_u
    return total


def get_left_array(node_count, m_list, u_list):
    np_left = np.zeros((node_count, node_count))
    for i in range(node_count):
        np_left[i][i] = get_value_from_item_count(i, m_list, u_list)

    for i in range(0, node_count - 1):
        np_left[i][i + 1] = -u_list[i + 1][1]
        np_left[i + 1][i] = np_left[i][i + 1]
    return np_left


def solve(m_list, wall_temps, u_list, t_in, right_array_first, right_array_middle, node_count):
    right_array_last = [m_list[-1][1] * wall_temps[-1][1] + u_list[-1][1] * t_in]
    right_list = [*right_array_first, *right_array_middle, *right_array_last]
    np_right = np.array(right_list)
    np_left = get_left_array(node_count, m_list, u_list)
    return np.linalg.solve(np_left, np_right)


def get_new_t_internal(radiation, walls_index, m_list, wall_temps, u_list, t_in, node_count, temp_indexes):
    new_radiation = M * radiation * T * walls[walls_index["GLASSPANE"]].get_area() / walls[
        walls_index["INTERNAL"]].get_area()
    # Απορροφητικότητα υαλοπίνακα
    new_absorption = 0.9

    right_array_first = [m_list[0][1] * wall_temps[0][1] + u_list[0][1] * t_in + new_absorption * new_radiation]

    right_array_middle = []
    for i in range(1, node_count - 1):
        right_array_middle.append(
            m_list[i][1] * wall_temps[i][1] + u_list[i][1] * t_in + new_absorption * new_radiation)
    solved = solve(m_list, wall_temps, u_list, t_in, right_array_first, right_array_middle, node_count)
    return list(zip(temp_indexes, solved))


def get_q(m_list, wall_temps, u_list, t_out, absorption, radiation, node_count, temp_indexes, t_in):
    right_array_first = [m_list[0][1] * wall_temps[0][1] + u_list[0][1] * t_out + absorption * radiation]
    right_array_middle = []
    for i in range(1, node_count - 1):
        right_array_middle.append(
            m_list[i][1] * wall_temps[i][1] + u_list[i][1] * t_out + absorption * radiation)
    solved = solve(m_list, wall_temps, u_list, t_in, right_array_first, right_array_middle, node_count)
    new_t = list(zip(temp_indexes, solved))

    # Θερμοροή εξωτερικών τοίχων
    q_wall = u_list[-1][1] * (new_t[-1][1] - t_in)
    q_list.append({"TYPE": "EXTERNAL", "VALUE": q_wall})
    return q_wall, new_t


def get_q_internal_1(m_list, wall_temps, u_list, absorption, radiation, node_count, temp_indexes, t_in, walls_index):
    new_t = get_new_t_internal(radiation, walls_index, m_list, wall_temps, u_list, t_in, node_count, temp_indexes)
    q_wall = u_list[0][1] * (new_t[0][1] - t_in)
    q_list.append({"TYPE": "INTERNAL", "VALUE": q_wall})
    return q_wall, new_t


def get_q_internal_2(m_list, wall_temps, u_list, absorption, radiation, node_count, temp_indexes, t_in, walls_index):
    new_t = get_new_t_internal(radiation, walls_index, m_list, wall_temps, u_list, t_in, node_count, temp_indexes)
    q_wall = u_list[-1][1] * (new_t[-1][1] - t_in)
    q_list.append({"TYPE": "INTERNAL", "VALUE": q_wall})
    return q_wall
