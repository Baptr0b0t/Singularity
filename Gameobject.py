class GameObject:
    def __init__(self, location = (0,0), angle=0):
        self.components = []

        self.self_updated_components = []

        self.quick_updated_components = []

        self.late_updated_components = []
        self.tag = []

        self.quick_updated_components.append(Transform(location[0], location[1], angle))


    def add_tag(self, tag):
        self.tag.append(tag)

    def has_tag(self, tag):
        return tag in self.tag

    def add_standard_component(self, component):
        self.components.append(component)


    def add_self_updated_component(self, component):
        self.self_updated_components.append(component)

    def add_quick_updated_component(self, component):
        self.quick_updated_components.append(component)

    def add_late_updated_component(self, component):
        self.late_updated_components.append(component)

    def has_component(self, component_type):
        return self.get_component(component_type) is not None

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component

        for component in self.self_updated_components:
            if isinstance(component, component_type):
                return component

        for component in self.quick_updated_components:
            if isinstance(component, component_type):
                return component

        for component in self.late_updated_components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, delta_time):
        for component in self.quick_updated_components:
            component.update(self, delta_time)

        for component in self.components:
            component.update(self, delta_time)

        for component in self.late_updated_components:
            component.update(self, delta_time)




class Component:
    def update(self, game_object, delta_time):
        pass


#Position
class Transform(Component):
    def __init__(self, x, y, angle = 0):
        self.position = [x, y]
        self.angle = angle #radians



class Velocity(Component):
    def __init__(self, x=0, y=0, ax=0, ay=0):
        self.velocity = [x, y]
        self.acceleration = [ax,ay]

    def update(self, game_object, delta_time):
        self.velocity[0] += self.acceleration[0] * delta_time
        self.velocity[1] += self.acceleration[1] * delta_time
        self.acceleration = [0,0]