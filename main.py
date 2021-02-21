# Tout = [(ώρα 0-23, θερμοκρασία)]
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from Tout import Tout
from Wall import walls
from UFunction import U
from MFunction import M
from QFunction import GetQ, GetQInternal1, GetQInternal2
from Charge import GetCharge
import math

WALLS_INDEX = {"NORTH": 0, "WEST": 1, "EAST": 2, "ROOF": 3, "INTERNAL": 4, "GLASSPANE": 5}

node_count_external = int(input("Enter external node count:"))
node_count_roof = int(input("Enter roof node count:"))
node_count_internal = int(input("Enter internal node count:"))
DELTAT = int(input("Enter Delta T:"))  # Χρονικό βήμα sec

node_count = {
    "EXTERNAL": node_count_external,
    "ROOF": node_count_roof,
    "INTERNAL": node_count_internal
}

WALL_THICKNESS = walls[WALLS_INDEX["NORTH"]].GetThickness()
DELTAX = WALL_THICKNESS / node_count["EXTERNAL"]  # Δχ
ABSORPTION = 0.8

# Συντελεστές συναγωγής
HOUT = 23
HIN = 8

tin = 22
tins = []

# TODO make first day not return counter
isFound = False
loops_count = 1
tins = []
delta_t_tins = []
temps_index_ext = [i for i in range(1, node_count["EXTERNAL"] + 1)]
temps_index_roof = [i for i in range(1, node_count["ROOF"] + 1)]
temps_index_internal = [i for i in range(1, node_count["INTERNAL"] + 1)]
temp = 20.5
node_temperatures = {
    "EXTERNAL": {
        "NORTH": list(zip(temps_index_ext, [temp for i in range(node_count["EXTERNAL"])])),
        "WEST": list(zip(temps_index_ext, [temp for i in range(node_count["EXTERNAL"])])),
        "EAST": list(zip(temps_index_ext, [temp for i in range(node_count["EXTERNAL"])])),
        "GLASS_PANE": list(zip(temps_index_ext, [temp for i in range(node_count["EXTERNAL"])]))
    },
    "ROOF": list(zip(temps_index_roof, [temp for i in range(node_count["ROOF"])])),
    "INTERNAL": list(zip(temps_index_internal, [temp for i in range(node_count["INTERNAL"])]))
}

print(Tout)

while not isFound:
    counter = 0
    temps_close_counter = 0
    daily_tins = []
    while counter < 3600 * 24:
        delta_t_tins.append(counter)
        time_int = math.floor(counter / 3600)
        tout = Tout[time_int][1]
        rad_list = [0, 0, 0, 0, 0, 0, 20, 40, 40, 50, 50, 100, 120, 250, 300, 200, 100, 50, 50, 40, 40, 0, 0, 0]
        RADIATION = rad_list[time_int]
        upos_dictionary = {
            "EXTERNAL": [i for i in range(2, node_count["EXTERNAL"] + 1)],
            "ROOF": [i for i in range(2, node_count["ROOF"] + 1)],
            "INTERNAL": [i for i in range(2, node_count["INTERNAL"] + 1)]
        }

        U_LIST = U(WALLS_INDEX["NORTH"], node_count["EXTERNAL"], WALL_THICKNESS, DELTAX, HOUT, HIN,
                   upos_dictionary["EXTERNAL"]).GetU()
        M_LIST = M(DELTAX, DELTAT, node_count["EXTERNAL"], WALL_THICKNESS, WALLS_INDEX["NORTH"])

        (q_north_wall, new_T_north) = GetQ(M_LIST, node_temperatures["EXTERNAL"]["NORTH"], U_LIST, tout, ABSORPTION,
                                           RADIATION, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_west_wall, new_T_west) = GetQ(M_LIST, node_temperatures["EXTERNAL"]["WEST"], U_LIST, tout, ABSORPTION,
                                         RADIATION, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_east_wall, new_T_east) = GetQ(M_LIST, node_temperatures["EXTERNAL"]["EAST"], U_LIST, tout, ABSORPTION,
                                         RADIATION, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_glasspane_wall, new_T_glasspane) = GetQ(M_LIST, node_temperatures["EXTERNAL"]["GLASS_PANE"], U_LIST, tout,
                                                   ABSORPTION, RADIATION, node_count["EXTERNAL"], temps_index_ext, tin)

        node_temperatures["EXTERNAL"]["NORTH"] = new_T_north
        node_temperatures["EXTERNAL"]["WEST"] = new_T_west
        node_temperatures["EXTERNAL"]["EAST"] = new_T_east
        node_temperatures["EXTERNAL"]["GLASS_PANE"] = new_T_glasspane

        north_wall_charge = GetCharge(q_north_wall, walls[WALLS_INDEX["NORTH"]].GetArea())
        west_wall_charge = GetCharge(q_west_wall, walls[WALLS_INDEX["WEST"]].GetArea())
        east_wall_charge = GetCharge(q_east_wall, walls[WALLS_INDEX["EAST"]].GetArea())
        glasspane_wall_charge = GetCharge(q_glasspane_wall, walls[WALLS_INDEX["GLASSPANE"]].GetArea())

        #########################################

        ROOF_WALL_THICKNESS = walls[WALLS_INDEX["ROOF"]].GetThickness()
        ROOF_DELTAX = ROOF_WALL_THICKNESS / node_count["ROOF"]

        ROOF_U_LIST = U(WALLS_INDEX["ROOF"], node_count["ROOF"], ROOF_WALL_THICKNESS, ROOF_DELTAX, HOUT, HIN,
                        upos_dictionary["ROOF"]).GetU()
        ROOF_M_LIST = M_LIST = M(ROOF_DELTAX, DELTAT, node_count["ROOF"], ROOF_WALL_THICKNESS, WALLS_INDEX["ROOF"])

        (q_roof_wall, new_T_roof) = GetQ(ROOF_M_LIST, node_temperatures["ROOF"], ROOF_U_LIST, tout, ABSORPTION,
                                         RADIATION, node_count["ROOF"], temps_index_roof, tin)

        node_temperatures["ROOF"] = new_T_roof

        roof_wall_charge = GetCharge(q_roof_wall, walls[WALLS_INDEX["ROOF"]].GetArea())

        ########################################################################################

        INTERNAL_WALL_THICKNESS = walls[WALLS_INDEX["INTERNAL"]].GetThickness()
        INTERNAL_DELTAX = INTERNAL_WALL_THICKNESS / node_count["INTERNAL"]

        INTERNAL_U_LIST = U(WALLS_INDEX["INTERNAL"], node_count["INTERNAL"], INTERNAL_WALL_THICKNESS, INTERNAL_DELTAX,
                            HOUT, HIN, upos_dictionary["INTERNAL"]).GetU()
        INTERNAL_M_LIST = M_LIST = M(INTERNAL_DELTAX, DELTAT, node_count["INTERNAL"], INTERNAL_WALL_THICKNESS,
                                     WALLS_INDEX["INTERNAL"])

        (q_internal_wall1, new_T_internal) = GetQInternal1(INTERNAL_M_LIST, node_temperatures["INTERNAL"],
                                                           INTERNAL_U_LIST, ABSORPTION, RADIATION,
                                                           node_count["INTERNAL"], temps_index_internal, tin,
                                                           WALLS_INDEX)
        q_internal_wall2 = GetQInternal2(INTERNAL_M_LIST, node_temperatures["INTERNAL"], INTERNAL_U_LIST, ABSORPTION,
                                         RADIATION, node_count["INTERNAL"], temps_index_internal, tin, WALLS_INDEX)

        node_temperatures["INTERNAL"] = new_T_internal

        internal_wall_charge1 = GetCharge(q_internal_wall1, walls[WALLS_INDEX["INTERNAL"]].GetArea())
        internal_wall_charge2 = GetCharge(q_internal_wall2, walls[WALLS_INDEX["INTERNAL"]].GetArea())

        SQ = north_wall_charge + west_wall_charge + east_wall_charge + roof_wall_charge + internal_wall_charge1 + internal_wall_charge2 + glasspane_wall_charge

        ########################################################################################

        # Φορτίο ανανέωσης

        VOLUME = 10 * 25 * 3
        RAIR = 1.18
        CAIR = 1005

        Mair = RAIR * VOLUME
        mass_provision = 2.5 * Mair / 3600

        Qinfilt = mass_provision * CAIR * (tout - tin)

        # Θερμική μάζα χώρου
        F = 2
        mc_air = RAIR * VOLUME * CAIR

        mc_area = F * mc_air

        SQ += Qinfilt

        tin = tin + (SQ * DELTAT) / mc_area
        counter += DELTAT
        daily_tins.append(tin)

    tins.append(daily_tins)
    print(tins[-1][-1])

    if loops_count > 2:
        if tins[-1][-1] - tins[-2][-1] <= 0.00000000005:
            break

    break

    loops_count += 1


plt.ylabel('Εσωτερική θερμοκρασία αέρος')
plt.xlabel('Χρόνος(sec)')
plt.plot(delta_t_tins, tins[-1])
plt.show()
