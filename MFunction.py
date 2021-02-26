from Wall import walls

# Υπολογισμός σταθερών M


def get_m(delta_x, delta_t, node_count, wall_thickness, wall_index):
    distance = delta_x * 0.5
    dens_heat_caps = []
    indexes = [i for i in range(1, node_count + 1)]
    while distance <= wall_thickness:
        dens_heat_caps += [walls[wall_index].get_density_heat_cap(distance)]
        distance += delta_x

    computed = []
    for i in range(len(dens_heat_caps)):
        computed.append(dens_heat_caps[i][0] * dens_heat_caps[i][1] * delta_x / delta_t)

    return list(zip(indexes, computed))
