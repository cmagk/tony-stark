# Tout = [(ώρα 0-23, θερμοκρασία)]
import numpy as np
from Tout import Tout
from Wall import walls
from UFunction import U
from MFunction import M

wall_index = 0  # North Wall
node_count = 10000000  # λ
wall_thickness = walls[wall_index].GetThickness()
deltaX = wall_thickness / node_count  # Δχ
deltaT = 1  # Χρονικό βήμα
absorption = 0.8
radiation = 300
# Συντελεστές συναγωγής
hout = 23
hin = 8
Tin = 25
u_pos = [i for i in range(2, node_count + 1)]  # 2 - node_count (list)

temperatures_index = [i for i in range(1, node_count + 1)]
wall_temperatures = list(zip(temperatures_index, [22 for i in range(node_count)]))  # Ti0

u_list = U(wall_index, node_count, wall_thickness, deltaX, hout, hin, u_pos).GetU()
m_list = M(deltaX, deltaT, node_count, wall_thickness, wall_index)

################      right array

right_array_first = [m_list[0][1] * wall_temperatures[0][1] + u_list[0][1] * Tout[0][1] + absorption * radiation]

right_array_middle = []

for i in range(1, node_count - 1):
    right_array_middle.append(m_list[i][1] * wall_temperatures[i][1] + u_list[i][1] * Tout[0][1] + absorption * radiation)

right_array_last = [m_list[-1][1] * wall_temperatures[-1][1] + u_list[-1][1] * Tin]

right_list = [*right_array_first, *right_array_middle, *right_array_last]

nplist = np.array(right_list)

print(nplist[:, None])
