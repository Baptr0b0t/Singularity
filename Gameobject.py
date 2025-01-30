class GameObject:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component_type):
        for component in self.components:
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
    def __init__(self, x, y):
        self.position = [x, y]
        self.angle = 0

    def goto(self, x, y, angle=0):
        self.position = [x, y]
        self.angle = angle