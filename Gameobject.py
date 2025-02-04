class GameObject:
    def __init__(self, location = (0,0)):
        self.components = []
        self.components.append(Transform(location[0], location[1]))

        self.self_updated_components = []

    def add_component(self, component):
        self.components.append(component)

    def add_self_updated_component(self, component):
        self.self_updated_components.append(component)

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component

        for component in self.self_updated_components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, delta_time):
        for component in self.components:
            component.update(self, delta_time)




class Component:
    def update(self, game_object, delta_time):
        pass


#Position
class Transform(Component):
    def __init__(self, x, y, angle = 0):
        self.position = [x, y]
        self.angle = angle

    def goto(self, x, y, angle=0):
        self.position = [x, y]
        self.angle = angle


class Velocity(Component):
    def __init__(self, x=0, y=0, ax=0, ay=0):
        self.velocity = [x, y]
        self.acceleration = [ax,ay]


