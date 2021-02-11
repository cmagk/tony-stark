# Tout = [(ώρα 0-23, θερμοκρασία)]
import numpy as np
from Tout import Tout
from Wall import walls
from UFunction import U
from MFunction import M
from QFunction import GetQ, GetQInternal1, GetQInternal2
from Charge import GetCharge

WALLS_INDEX = {"NORTH": 0, "WEST": 1, "EAST": 2, "ROOF": 3, "INTERNAL": 4, "GLASSPANE": 5 }
NODE_COUNT = 20  # λ
WALL_THICKNESS = walls[WALLS_INDEX["NORTH"]].GetThickness()
DELTAX = WALL_THICKNESS / NODE_COUNT  # Δχ
DELTAT = 60  # Χρονικό βήμα sec
ABSORPTION = 0.8
RADIATION = 300
# Συντελεστές συναγωγής
HOUT = 23
HIN = 8
TIN = 22
U_POS = [i for i in range(2, NODE_COUNT + 1)]  # 2 - node_count (list)

TEMPS_INDEX = [i for i in range(1, NODE_COUNT + 1)]
WALL_TEMPERATURES = list(zip(TEMPS_INDEX, [25 for i in range(NODE_COUNT)]))  # Ti0

U_LIST = U(WALLS_INDEX["NORTH"], NODE_COUNT, WALL_THICKNESS, DELTAX, HOUT, HIN, U_POS).GetU()
M_LIST = M(DELTAX, DELTAT, NODE_COUNT, WALL_THICKNESS, WALLS_INDEX["NORTH"])

q_north_wall = GetQ(M_LIST, WALL_TEMPERATURES, U_LIST, Tout, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN)
q_west_wall = GetQ(M_LIST, WALL_TEMPERATURES, U_LIST, Tout, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN)
q_east_wall = GetQ(M_LIST, WALL_TEMPERATURES, U_LIST, Tout, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN)
q_glasspane_wall = GetQ(M_LIST, WALL_TEMPERATURES, U_LIST, Tout, ABSORPTION, RADIATION, NODE_COUNT, TEMPS_INDEX, TIN)

north_wall_charge = GetCharge(q_north_wall, walls[WALLS_INDEX["NORTH"]].GetArea())
west_wall_charge = GetCharge(q_west_wall, walls[WALLS_INDEX["WEST"]].GetArea())
east_wall_charge = GetCharge(q_east_wall, walls[WALLS_INDEX["EAST"]].GetArea())
glasspane_wall_charge = GetCharge(q_glasspane_wall, walls[WALLS_INDEX["GLASSPANE"]].GetArea())

#########################################

ROOF_NODE_COUNT = 20
ROOF_WALL_THICKNESS = walls[WALLS_INDEX["ROOF"]].GetThickness()
ROOF_DELTAX = ROOF_WALL_THICKNESS / ROOF_NODE_COUNT

ROOF_U_LIST = U(WALLS_INDEX["ROOF"], ROOF_NODE_COUNT, ROOF_WALL_THICKNESS, ROOF_DELTAX, HOUT, HIN, U_POS).GetU()
ROOF_M_LIST = M_LIST = M(ROOF_DELTAX, DELTAT, ROOF_NODE_COUNT, ROOF_WALL_THICKNESS, WALLS_INDEX["ROOF"])

q_roof_wall = GetQ(ROOF_M_LIST, WALL_TEMPERATURES, ROOF_U_LIST, Tout, ABSORPTION, RADIATION, ROOF_NODE_COUNT, TEMPS_INDEX, TIN)

roof_wall_charge = GetCharge(q_roof_wall, walls[WALLS_INDEX["ROOF"]].GetArea())

########################################################################################

INTERNAL_NODE_COUNT = 20
INTERNAL_WALL_THICKNESS = walls[WALLS_INDEX["INTERNAL"]].GetThickness()
INTERNAL_DELTAX = INTERNAL_WALL_THICKNESS / INTERNAL_NODE_COUNT

INTERNAL_U_LIST = U(WALLS_INDEX["INTERNAL"], INTERNAL_NODE_COUNT, INTERNAL_WALL_THICKNESS, INTERNAL_DELTAX, HOUT, HIN, U_POS).GetU()
INTERNAL_M_LIST = M_LIST = M(INTERNAL_DELTAX, DELTAT, INTERNAL_NODE_COUNT, INTERNAL_WALL_THICKNESS, WALLS_INDEX["INTERNAL"])

q_internal_wall1 = GetQInternal1(INTERNAL_M_LIST, WALL_TEMPERATURES, INTERNAL_U_LIST, ABSORPTION, RADIATION, INTERNAL_NODE_COUNT, TEMPS_INDEX, TIN, WALLS_INDEX)
q_internal_wall2 = GetQInternal2(INTERNAL_M_LIST, WALL_TEMPERATURES, INTERNAL_U_LIST, ABSORPTION, RADIATION, INTERNAL_NODE_COUNT, TEMPS_INDEX, TIN, WALLS_INDEX)

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

Qinfilt = mass_provision * CAIR * (Tout[0][1] - TIN)

# Θερμική μάζα χώρου
F = 2
mc_air = RAIR * VOLUME * CAIR

mc_area = F * mc_air

new_tin = TIN + (SQ * DELTAT) / mc_area

print(new_tin)