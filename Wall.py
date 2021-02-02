class StructuralComponent:
    def __init__(self, conductivity, density, heat_capacity, thickness):  # k ρ Cp
        self.conductivity = conductivity
        self.density = density
        self.heat_capacity = heat_capacity
        self.thickness = thickness


class Wall:
    def __init__(self, components):
        self.components = components
        self.thickness = 0
        for component in self.components:
            self.thickness += component.thickness

    def GetThickness(self):
        return self.thickness

    def GetThicknessListPerComponent(self):
        thickness = []
        for i in range(len(self.components)):
            thickness.append(self.components[i].thickness)
        return thickness

    def GetConductivityListPerComponent(self):
        conductivity = []
        for i in range(len(self.components)):
            conductivity.append(self.components[i].conductivity)
        return conductivity

    def GetStructComponentConductivity(self, totalX, deltaX, isFirst):
        conductivity = []
        thickness_list = self.GetThicknessListPerComponent()
        conductivity_list = self.GetConductivityListPerComponent()

        for i in range(len(self.components)):
            if sum(thickness_list[:i + 1]) >= totalX:
                conductivity.append(conductivity_list[i])
                if totalX - deltaX <= sum(thickness_list[:i]) and (totalX > deltaX or isFirst):
                    conductivity.append(conductivity_list[i - 1])
                break
            else:
                continue

        return conductivity




north_west_east_components = [
    StructuralComponent(0.08, 250, 1100, 2.5),  # Θερμομονωτικό επίχρισμα (εξωτερικά)
    StructuralComponent(0.49, 1200, 1000, 9),  # Οπτοπλινθοδομή με πλήρεις οπτοπλίνθους
    StructuralComponent(0.01, 840, 0.038, 5),  # Πετροβάμβακας σε μορφή παπλώματος
    StructuralComponent(0.49, 1200, 1000, 9),  # Οπτοπλινθοδομή με πλήρεις οπτοπλίνθους
    StructuralComponent(0.87, 1800, 1000, 2.5)  # Ασβεστοκονίαμα
]

roof_components = [
    StructuralComponent(1.4, 2000, 1100, 10),  # Τσιμεντοκονίαμα, επίστρωση τσιμέντου
    StructuralComponent(0.01, 500, 1100, 2.5),  # Θερμομονωτικό επίχρισμα
    StructuralComponent(2.3, 2300, 1000, 25),  # Οπλισμένο σκυρόδεμα(1% σίδηρος)
    StructuralComponent(0.87, 1800, 1000, 2)  # Ασβεστοκονίαμα
]

internal_wall_components = [
    StructuralComponent(0.87, 1800, 1000, 2.5),  # Ασβεστοκονίαμα
    StructuralComponent(0.26, 940, 1000, 10),  # Τούβλο
    StructuralComponent(0.87, 1800, 1000, 2.5)  # Ασβεστοκονίαμα
]

north_wall = Wall(north_west_east_components)

west_wall = Wall(north_west_east_components)

east_wall = Wall(north_west_east_components)

roof_wall = Wall(roof_components)

internal_wall = Wall(internal_wall_components)

walls = [north_wall, west_wall, east_wall, roof_wall, internal_wall]