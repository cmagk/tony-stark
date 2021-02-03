# Tout = [(ώρα 0-23, θερμοκρασία)]
import numpy as np
from Tout import Tout
from Wall import walls, vertical_walls, roof_wall, glass_pane_wall
from UFunction import U
from MFunction import M

WALL_INDEX = 0  # North Wall
NODE_COUNT = 800  # λ
WALL_THICKNESS = walls[WALL_INDEX].GetThickness()
DELTAX = WALL_THICKNESS / NODE_COUNT  # Δχ
DELTAT = 60  # Χρονικό βήμα
ABSORPTION = 0.8
RADIATION = 300
# Συντελεστές συναγωγής
HOUT = 23
HIN = 8
TIN = 22
U_POS = [i for i in range(2, NODE_COUNT + 1)]  # 2 - node_count (list)

TEMPS_INDEX = [i for i in range(1, NODE_COUNT + 1)]
WALL_TEMPERATURES = list(zip(TEMPS_INDEX, [25 for i in range(NODE_COUNT)]))  # Ti0

U_LIST = U(WALL_INDEX, NODE_COUNT, WALL_THICKNESS, DELTAX, HOUT, HIN, U_POS).GetU()
M_LIST = M(DELTAX, DELTAT, NODE_COUNT, WALL_THICKNESS, WALL_INDEX)

################      right array

right_array_first = [M_LIST[0][1] * WALL_TEMPERATURES[0][1] + U_LIST[0][1] * Tout[0][1] + ABSORPTION * RADIATION]

right_array_middle = []

for i in range(1, NODE_COUNT - 1):
    right_array_middle.append(M_LIST[i][1] * WALL_TEMPERATURES[i][1] + U_LIST[i][1] * Tout[0][1] + ABSORPTION * RADIATION)

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
    np_left[i][i+1] = -U_LIST[i + 1][1]
    np_left[i+1][i] = np_left[i][i+1]

np.set_printoptions(suppress=True,linewidth=np.nan)

solved = np.linalg.solve(np_left, np_right)
new_T = list(zip(TEMPS_INDEX, solved))

q_wall = U_LIST[-1][1] * (new_T[-1][1] - TIN)

print(q_wall)