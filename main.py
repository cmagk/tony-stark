# Tout = [(ώρα 0-23, θερμοκρασία)]
import matplotlib.pyplot as plt
from Tout import t_out
from Wall import walls
from UFunction import U
from MFunction import get_m
from QFunction import get_q, get_q_internal_1, get_q_internal_2, q_list
import math
# Απορροφητικότητα
ABSORPTION = 0.8
# Συντελεστής συναγωγής περιβάλλοντος
H_OUT = 23
# Συντελεστής συναγωγής εντός του χώρου
H_IN = 8
# Όγκος κτηρίου
VOLUME = 10 * 25 * 3
# Πυκνότητα αέρα
R_AIR = 1.18
# Θερμοχωρητικότητα αέρα
C_AIR = 1005
# Παροχή μάζας
M_AIR = R_AIR * VOLUME
# Αρχική εσωτερική θερμοκρασία
tin = 22
# Ακτινοβολία ανά ώρα
RAD_LIST = [0, 0, 0, 0, 0, 0, 20, 40, 40, 50, 50, 100, 120, 250, 300, 200, 100, 50, 50, 40, 40, 0, 0, 0]
WALLS_INDEX = {"NORTH": 0, "WEST": 1, "EAST": 2, "ROOF": 3, "INTERNAL": 4, "GLASSPANE": 5}


def get_charge(q_wall, area):
    return q_wall * area


node_count_external = int(input("Enter external node count:"))
node_count_roof = int(input("Enter roof node count:"))
node_count_internal = int(input("Enter internal node count:"))
delta_t = int(input("Enter Delta T:"))  # Χρονικό βήμα sec
node_count = {
    "EXTERNAL": node_count_external,
    "ROOF": node_count_roof,
    "INTERNAL": node_count_internal
}
NORTH_WALL_THICKNESS = walls[WALLS_INDEX["NORTH"]].get_thickness()
delta_x = NORTH_WALL_THICKNESS / node_count["EXTERNAL"]  # Δχ

# Συντελεστές συναγωγής
is_found = False
loops_count = 1
tins = []
temps_index_ext = [i for i in range(1, node_count["EXTERNAL"] + 1)]
temps_index_roof = [i for i in range(1, node_count["ROOF"] + 1)]
temps_index_internal = [i for i in range(1, node_count["INTERNAL"] + 1)]
# Αρχική θερμοκρασία τοίχων
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
u_pos_dict = {
            "EXTERNAL": [i for i in range(2, node_count["EXTERNAL"] + 1)],
            "ROOF": [i for i in range(2, node_count["ROOF"] + 1)],
            "INTERNAL": [i for i in range(2, node_count["INTERNAL"] + 1)]
        }

print(t_out)

while not is_found:
    counter = 0
    temps_close_counter = 0
    daily_tins = []
    delta_t_tins = []
    while counter < 3600 * 24:
        delta_t_tins.append(counter)
        time_int = math.floor(counter / 3600)
        current_tout = t_out[time_int][1]
        radiation = RAD_LIST[time_int]

        u_list = U(WALLS_INDEX["NORTH"], node_count["EXTERNAL"], NORTH_WALL_THICKNESS, delta_x, H_OUT, H_IN,
                   u_pos_dict["EXTERNAL"]).get_u()

        m_list = get_m(delta_x, delta_t, node_count["EXTERNAL"], NORTH_WALL_THICKNESS, WALLS_INDEX["NORTH"])

        (q_north_wall, new_T_north) = get_q(m_list, node_temperatures["EXTERNAL"]["NORTH"], u_list, current_tout,
                                            ABSORPTION, radiation, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_west_wall, new_T_west) = get_q(m_list, node_temperatures["EXTERNAL"]["WEST"], u_list, current_tout,
                                          ABSORPTION, radiation, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_east_wall, new_T_east) = get_q(m_list, node_temperatures["EXTERNAL"]["EAST"], u_list, current_tout,
                                          ABSORPTION, radiation, node_count["EXTERNAL"], temps_index_ext, tin)
        (q_glass_pane_wall, new_T_glass_pane) = get_q(m_list, node_temperatures["EXTERNAL"]["GLASS_PANE"],
                                                      u_list, current_tout, ABSORPTION, radiation,
                                                      node_count["EXTERNAL"], temps_index_ext, tin)

        node_temperatures["EXTERNAL"]["NORTH"] = new_T_north
        node_temperatures["EXTERNAL"]["WEST"] = new_T_west
        node_temperatures["EXTERNAL"]["EAST"] = new_T_east
        node_temperatures["EXTERNAL"]["GLASS_PANE"] = new_T_glass_pane

        north_wall_charge = get_charge(q_north_wall, walls[WALLS_INDEX["NORTH"]].get_area())
        west_wall_charge = get_charge(q_west_wall, walls[WALLS_INDEX["WEST"]].get_area())
        east_wall_charge = get_charge(q_east_wall, walls[WALLS_INDEX["EAST"]].get_area())
        glass_pane_wall_charge = get_charge(q_glass_pane_wall, walls[WALLS_INDEX["GLASSPANE"]].get_area())

        roof_wall_thickness = walls[WALLS_INDEX["ROOF"]].get_thickness()
        roof_delta_x = roof_wall_thickness / node_count["ROOF"]

        roof_u_list = U(WALLS_INDEX["ROOF"], node_count["ROOF"], roof_wall_thickness, roof_delta_x, H_OUT, H_IN,
                        u_pos_dict["ROOF"]).get_u()

        roof_m_list = m_list = get_m(roof_delta_x, delta_t, node_count["ROOF"], roof_wall_thickness,
                                     WALLS_INDEX["ROOF"])

        (q_roof_wall, new_T_roof) = get_q(roof_m_list, node_temperatures["ROOF"], roof_u_list, current_tout, ABSORPTION,
                                          radiation, node_count["ROOF"], temps_index_roof, tin)

        node_temperatures["ROOF"] = new_T_roof

        roof_wall_charge = get_charge(q_roof_wall, walls[WALLS_INDEX["ROOF"]].get_area())

        internal_wall_thickness = walls[WALLS_INDEX["INTERNAL"]].get_thickness()
        internal_delta_x = internal_wall_thickness / node_count["INTERNAL"]

        internal_u_list = U(WALLS_INDEX["INTERNAL"], node_count["INTERNAL"], internal_wall_thickness, internal_delta_x,
                            H_OUT, H_IN, u_pos_dict["INTERNAL"]).get_u()

        internal_m_list = get_m(internal_delta_x, delta_t, node_count["INTERNAL"], internal_wall_thickness,
                                WALLS_INDEX["INTERNAL"])

        (q_internal_wall1, new_T_internal) = get_q_internal_1(internal_m_list, node_temperatures["INTERNAL"],
                                                              internal_u_list, ABSORPTION, radiation,
                                                              node_count["INTERNAL"], temps_index_internal, tin,
                                                              WALLS_INDEX)
        q_internal_wall2 = get_q_internal_2(internal_m_list, node_temperatures["INTERNAL"], internal_u_list, ABSORPTION,
                                            radiation, node_count["INTERNAL"], temps_index_internal, tin, WALLS_INDEX)

        node_temperatures["INTERNAL"] = new_T_internal

        internal_wall_charge1 = get_charge(q_internal_wall1, walls[WALLS_INDEX["INTERNAL"]].get_area())
        internal_wall_charge2 = get_charge(q_internal_wall2, walls[WALLS_INDEX["INTERNAL"]].get_area())

        sq = north_wall_charge + west_wall_charge + east_wall_charge + roof_wall_charge \
            + internal_wall_charge1 + internal_wall_charge2 + glass_pane_wall_charge

        # Φορτίο ανανέωσης
        mass_provision = 2.5 * M_AIR / 3600
        q_infilt = mass_provision * C_AIR * (current_tout - tin)
        # Θερμική μάζα χώρου
        f = 2
        mc_air = R_AIR * VOLUME * C_AIR
        mc_area = f * mc_air
        sq += q_infilt

        tin = tin + (sq * delta_t) / mc_area
        counter += delta_t
        daily_tins.append(tin)

    tins.append(daily_tins)
    print(tins[-1][-1])

    if loops_count > 2:
        if tins[-1][-1] - tins[-2][-1] <= 0.4:
            break

    loops_count += 1

with open("q_list.txt", "w") as qlist:
    for q_dict in q_list:
        qlist.write(f"Type:{q_dict}\n")

plt.ylabel('Εσωτερική θερμοκρασία αέρος')
plt.xlabel('Χρόνος(sec)')
plt.plot(delta_t_tins, tins[-1])
plt.show()
