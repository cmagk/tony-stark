# Tout = [(ώρα 0-23, θερμοκρασία)]
from Tout import Tout
from Wall import walls

wall_index = 0  # North Wall

node_count = 5  # λ
wall_thickness = walls[wall_index].GetThickness()
deltaX = wall_thickness / node_count  # Δχ

# Συντελεστές συναγωγής
hout = 23
hin = 8

u_pos = [i for i in range(2, node_count + 1)]  # 2 - node_count (list)

def GetU1():
    k = walls[wall_index].components[0].conductivity
    return 1 / ((1 / hout) + deltaX / (2 * k))

def Umiddle():
    distance = deltaX * 0.5
    isFirst = True
    while distance <= wall_thickness:
        print(f"{walls[0].GetStructComponentConductivity(distance, deltaX, isFirst)}")
        distance += deltaX
        isFirst = False


def GetUlast():
    components = walls[wall_index].components
    k = components[len(components) - 1].conductivity
    return 1 / ((1 / hin) + deltaX / (2 * k))