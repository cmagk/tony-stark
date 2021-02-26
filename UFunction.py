from Wall import walls

# Υπολογισμός συντελεστών U


class U:
    def __init__(self, wall_index, node_count, wall_thickness, delta_x, h_out, h_in, u_pos):
        self.u_pos = u_pos
        self.h_in = h_in
        self.h_out = h_out
        self.delta_x = delta_x
        self.wall_thickness = wall_thickness
        self.node_count = node_count
        self.wall_index = wall_index

    def get_u1(self):
        k = walls[self.wall_index].components[0].conductivity
        return 1 / ((1 / self.h_out) + self.delta_x / (2 * k))

    def get_u_middle(self):
        distance = self.delta_x * 1.5
        is_first = True
        conductivities = []
        while distance <= self.wall_thickness:
            conductivities += [walls[self.wall_index].get_comp_conductivity(distance, self.delta_x, is_first)]
            distance += self.delta_x
            is_first = False

        computed = []
        for i in range(len(conductivities)):
            if len(conductivities[i]) == 1:
                computed.append(1 / (self.delta_x / conductivities[i][0]))
            else:
                computed.append(
                    1 / ((self.delta_x / (2 * conductivities[i][0])) + (self.delta_x / (2 * conductivities[i][1]))))

        return list(zip(self.u_pos, computed))

    def get_u_last(self):
        components = walls[self.wall_index].components
        k = components[len(components) - 1].conductivity
        return 1 / ((1 / self.h_in) + self.delta_x / (2 * k))

    def get_u(self):
        return [(1, self.get_u1())] + self.get_u_middle() + [(self.node_count + 1, self.get_u_last())]
