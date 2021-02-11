from Wall import walls
class U:
    def __init__(self, wall_index, node_count, wall_thickness, deltaX, hout, hin, u_pos):

        self.u_pos = u_pos
        self.hin = hin
        self.hout = hout
        self.deltaX = deltaX
        self.wall_thickness = wall_thickness
        self.node_count = node_count
        self.wall_index = wall_index

    def GetU1(self):
        k = walls[self.wall_index].components[0].conductivity
        return 1 / ((1 / self.hout) + self.deltaX / (2 * k))

    def GetUmiddle(self):
        distance = self.deltaX * 1.5
        isFirst = True
        conductivities = []
        while distance <= self.wall_thickness:
            conductivities += [walls[self.wall_index].GetStructComponentConductivity(distance, self.deltaX, isFirst)]
            distance += self.deltaX
            isFirst = False

        computed = []
        for i in range(len(conductivities)):
            if len(conductivities[i]) == 1:
                computed.append(1 / (self.deltaX / conductivities[i][0]))
            else:
                computed.append(1 / ((self.deltaX / (2 * conductivities[i][0])) + (self.deltaX / (2 * conductivities[i][1]))))

        return list(zip(self.u_pos, computed))

    def GetUlast(self):
        components = walls[self.wall_index].components
        k = components[len(components) - 1].conductivity
        return 1 / ((1 / self.hin) + self.deltaX / (2 * k))

    def GetU(self):
        return [(1, self.GetU1())] + self.GetUmiddle() + [(self.node_count + 1, self.GetUlast())]