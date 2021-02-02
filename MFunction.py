from Wall import walls

def M(deltaX, deltaT, node_count, wall_thickness, wall_index):
    distance = deltaX * 0.5
    dens_heat_caps = []
    indexes = [i for i in range(1, node_count + 1)]
    while distance <= wall_thickness:
        dens_heat_caps += [walls[wall_index].GetDensityAndHeatCap(distance)]
        distance += deltaX

    computed = []
    for i in range(len(dens_heat_caps)):
        computed.append(dens_heat_caps[i][0] * dens_heat_caps[i][1] * deltaX / deltaT)

    return list(zip(indexes, computed))