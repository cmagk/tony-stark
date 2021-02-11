import numpy as np
from Wall import walls

def GetQ(M_LIST, WALL_TEMPERATURES, U_LIST, Tout, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN):
    ################      right array

    right_array_first = [M_LIST[0][1] * WALL_TEMPERATURES[0][1] + U_LIST[0][1] * Tout[0][1] + ABSORPTION * RADIATION]

    right_array_middle = []

    for i in range(1, NODE_COUNT - 1):
        right_array_middle.append(
            M_LIST[i][1] * WALL_TEMPERATURES[i][1] + U_LIST[i][1] * Tout[0][1] + ABSORPTION * RADIATION)

    right_array_last = [M_LIST[-1][1] * WALL_TEMPERATURES[-1][1] + U_LIST[-1][1] * TIN]

    right_list = [*right_array_first, *right_array_middle, *right_array_last]

    np_right = np.array(right_list)

    ################      left array

    np_left = np.zeros((NODE_COUNT, NODE_COUNT))

    def GetValueFromIterCountForMainDiagonal(iter):
        m = M_LIST[iter][1]
        first_u = U_LIST[iter][1]
        second_u = U_LIST[iter + 1][1]
        total = m + first_u + second_u
        return total

    for i in range(NODE_COUNT):
        np_left[i][i] = GetValueFromIterCountForMainDiagonal(i)

    for i in range(0, NODE_COUNT - 1):
        np_left[i][i + 1] = -U_LIST[i + 1][1]
        np_left[i + 1][i] = np_left[i][i + 1]

    np.set_printoptions(suppress=True, linewidth=np.nan)

    solved = np.linalg.solve(np_left, np_right)
    new_T = list(zip(TEMPS_INDEX, solved))

    q_wall = U_LIST[-1][1] * (new_T[-1][1] - TIN)
    return q_wall

def GetQInternal1(M_LIST, WALL_TEMPERATURES, U_LIST, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN, walls_index):
    ################      right array
    t = 0.8

    new_radiation = 0.1 * RADIATION * t * walls[walls_index["GLASSPANE"]].GetArea() / walls[walls_index["INTERNAL"]].GetArea()
    new_absorption = 0.9

    right_array_first = [M_LIST[0][1] * WALL_TEMPERATURES[0][1] + U_LIST[0][1] * TIN + new_absorption * new_radiation]

    right_array_middle = []

    for i in range(1, NODE_COUNT - 1):
        right_array_middle.append(
            M_LIST[i][1] * WALL_TEMPERATURES[i][1] + U_LIST[i][1] * TIN + new_absorption * new_radiation)

    right_array_last = [M_LIST[-1][1] * WALL_TEMPERATURES[-1][1] + U_LIST[-1][1] * TIN]

    right_list = [*right_array_first, *right_array_middle, *right_array_last]

    np_right = np.array(right_list)

    ################      left array

    np_left = np.zeros((NODE_COUNT, NODE_COUNT))

    def GetValueFromIterCountForMainDiagonal(iter):
        m = M_LIST[iter][1]
        first_u = U_LIST[iter][1]
        second_u = U_LIST[iter + 1][1]
        total = m + first_u + second_u
        return total

    for i in range(NODE_COUNT):
        np_left[i][i] = GetValueFromIterCountForMainDiagonal(i)

    for i in range(0, NODE_COUNT - 1):
        np_left[i][i + 1] = -U_LIST[i + 1][1]
        np_left[i + 1][i] = np_left[i][i + 1]

    np.set_printoptions(suppress=True, linewidth=np.nan)

    solved = np.linalg.solve(np_left, np_right)
    new_T = list(zip(TEMPS_INDEX, solved))

    q_wall = U_LIST[0][1] * (new_T[0][1] - TIN)
    return q_wall

def GetQInternal2(M_LIST, WALL_TEMPERATURES, U_LIST, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN, walls_index):
    ################      right array
    t = 0.8

    new_radiation = 0.1 * RADIATION * t * walls[walls_index["GLASSPANE"]].GetArea() / walls[walls_index["INTERNAL"]].GetArea()
    new_absorption = 0.9

    right_array_first = [M_LIST[0][1] * WALL_TEMPERATURES[0][1] + U_LIST[0][1] * TIN + new_absorption * new_radiation]

    right_array_middle = []

    for i in range(1, NODE_COUNT - 1):
        right_array_middle.append(
            M_LIST[i][1] * WALL_TEMPERATURES[i][1] + U_LIST[i][1] * TIN + new_absorption * new_radiation)

    right_array_last = [M_LIST[-1][1] * WALL_TEMPERATURES[-1][1] + U_LIST[-1][1] * TIN]

    right_list = [*right_array_first, *right_array_middle, *right_array_last]

    np_right = np.array(right_list)

    ################      left array

    np_left = np.zeros((NODE_COUNT, NODE_COUNT))

    def GetValueFromIterCountForMainDiagonal(iter):
        m = M_LIST[iter][1]
        first_u = U_LIST[iter][1]
        second_u = U_LIST[iter + 1][1]
        total = m + first_u + second_u
        return total

    for i in range(NODE_COUNT):
        np_left[i][i] = GetValueFromIterCountForMainDiagonal(i)

    for i in range(0, NODE_COUNT - 1):
        np_left[i][i + 1] = -U_LIST[i + 1][1]
        np_left[i + 1][i] = np_left[i][i + 1]

    np.set_printoptions(suppress=True, linewidth=np.nan)

    solved = np.linalg.solve(np_left, np_right)
    new_T = list(zip(TEMPS_INDEX, solved))

    q_wall = U_LIST[-1][1] * (new_T[-1][1] - TIN)
    return q_wall
