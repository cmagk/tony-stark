class StructuralComponent:
    def __init__(self, conductivity, density, heat_capacity, thickness):  # k ρ Cp
        self.conductivity = conductivity
        self.density = density
        self.heat_capacity = heat_capacity
        self.thickness = thickness


class Wall:
    def __init__(self, components, length):
        self.components = components
        self.thickness = 0
        self.length = length
        for component in self.components:
            self.thickness += component.thickness

    def get_thickness(self):
        return self.thickness

    def get_thick_list_per_comp(self):
        thickness = []
        for i in range(len(self.components)):
            thickness.append(self.components[i].thickness)
        return thickness

    def get_conduct_list_per_comp(self):
        conductivity = []
        for i in range(len(self.components)):
            conductivity.append(self.components[i].conductivity)
        return conductivity

    def get_comp_conductivity(self, total_x, delta_x, is_first):
        conductivity = []
        thickness_list = self.get_thick_list_per_comp()
        conductivity_list = self.get_conduct_list_per_comp()

        for i in range(len(self.components)):
            if sum(thickness_list[:i + 1]) >= total_x:
                conductivity.append(conductivity_list[i])
                if total_x - delta_x <= sum(thickness_list[:i]) and (total_x > delta_x or is_first):
                    conductivity.append(conductivity_list[i - 1])
                break
            else:
                continue

        return conductivity

    def get_density_heat_cap(self, total_x):
        thickness_list = self.get_thick_list_per_comp()
        for i in range(len(self.components)):
            if sum(thickness_list[:i + 1]) >= total_x:
                return [self.components[i].density, self.components[i].heat_capacity]
                break
            else:
                continue


class VerticalWall(Wall):
    def __init__(self, components, length, height):
        super().__init__(components, length)
        self.height = height

    def get_area(self):
        return self.length * self.height


class RoofWall(Wall):
    def __init__(self, components, length, width):
        super().__init__(components, length)
        self.width = width

    def get_area(self):
        return self.length * self.width


class GlassPaneWall(VerticalWall):
    def __init__(self, components, length, height, pane):
        super().__init__(components, length, height)
        self.glass_pane = pane

    def get_area(self):
        return self.length * self.height - self.glass_pane.get_area()


class GlassPane:
    def __init__(self, length, height, heat_capacity, permeability):
        self.length = length
        self.height = height
        self.heat_capacity = heat_capacity
        self.permeability = permeability

    def get_area(self):
        return self.length * self.height


north_west_east_components = [
    StructuralComponent(0.08, 1100, 1100, 2.5),  # Θερμομονωτικό επίχρισμα (εξωτερικά)
    StructuralComponent(0.49, 1200, 1000, 9),  # Οπτοπλινθοδομή με πλήρεις οπτοπλίνθους
    StructuralComponent(0.01, 1000, 840, 5),  # Πετροβάμβακας σε μορφή παπλώματος
    StructuralComponent(0.49, 1200, 1000, 9),  # Οπτοπλινθοδομή με πλήρεις οπτοπλίνθους
    StructuralComponent(0.87, 1800, 1000, 2.5)  # Ασβεστοκονίαμα
]

roof_components = [
    StructuralComponent(1.4, 2000, 1100, 10),  # Τσιμεντοκονίαμα, επίστρωση τσιμέντου
    StructuralComponent(0.01, 500, 1100, 5),  # Θερμομονωτικό επίχρισμα
    StructuralComponent(2.3, 2300, 1000, 25),  # Οπλισμένο σκυρόδεμα(1% σίδηρος)
    StructuralComponent(0.87, 1800, 1000, 2)  # Ασβεστοκονίαμα
]

internal_wall_components = [
    StructuralComponent(0.87, 1800, 1000, 2.5),  # Ασβεστοκονίαμα
    StructuralComponent(0.26, 940, 1000, 10),  # Τούβλο
    StructuralComponent(0.87, 1800, 1000, 2.5)  # Ασβεστοκονίαμα
]

north_wall = VerticalWall(north_west_east_components, 25, 3)  # Μήκος, ύψος

west_wall = VerticalWall(north_west_east_components, 10, 3)

east_wall = VerticalWall(north_west_east_components, 10, 3)

internal_wall = VerticalWall(internal_wall_components, 25, 3)

roof_wall = RoofWall(roof_components, 10, 25)  # Μήκος, πλάτος

glass_pane = GlassPane(15, 2, 2.8, 0.68)  # heat_capacity Δίδυμος υαλοπίνακας με διάκενο αέρα 12 mm // Πίνακας 3.16 (ΤΟΤΕΕ)

glass_pane_wall = GlassPaneWall(north_west_east_components, 25, 3, glass_pane)

walls = [north_wall, west_wall, east_wall, roof_wall, internal_wall, glass_pane_wall]


