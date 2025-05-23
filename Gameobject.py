import Holder
import gc

class GameObject:
    def __init__(self, location = (0,0), angle=0):
        self.components = []

        self.self_updated_components = []

        self.quick_updated_components = []

        self.late_updated_components = []
        self.tag = []

        self.quick_updated_components.append(Transform(self ,location[0], location[1], angle))


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

    def update(self):
        for component in self.quick_updated_components:
            component.update()

        for component in self.components:
            component.update()

        for component in self.late_updated_components:
            component.update()

    def boot_up(self):
        """
        Use when the scene active
        """
        for component in self.quick_updated_components:
            component.boot_up()

        for component in self.components:
            component.boot_up()

        for component in self.late_updated_components:
            component.boot_up()

    def delete(self):
        """Delete GameObject"""
        for component in self.quick_updated_components:
            component.delete()

        for component in self.components:
            component.delete()

        for component in self.late_updated_components:
            component.delete()
        del self
        #print("deleted : ", gc.collect())


def requires_active(func): #must add @requires_active to component update() for effect
    def wrapper(self, *args, **kwargs):
        if not self.active:
            return  # Ne fait rien si le composant est désactivé
        return func(self, *args, **kwargs)
    return wrapper

class Component:
    """
    Composant de base, permet de retrouver le Gameobject.
    :param parent: Gameobject du component
    """
    def __init__(self, parent, active = False):
        self._parent = parent
        self._active = active

    @property
    def parent(self):
        return self._parent

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value

    def update(self):
        pass #Permet les composants sans update()

    def boot_up(self):
        """
        Fonction lancer lorsque que la scene ou se situe le composant s'active
        """
        pass #Permet les composants sans boot_up()

    def delete(self):
        pass


#Position
class Transform(Component):
    """
    Composant obligatoire de position de l'objet
    :param angle: L'angle en radian
    """
    def __init__(self, parent, x, y, angle = 0):
        super().__init__(parent)
        self.position = [x, y]
        self.angle = angle
    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @y.setter
    def y(self, value):
        self.position[1] = value


class Velocity(Component):
    """
    Composant de vitesse de l'objet
    :param x: vitesse en x
    :param y: vitesse en y
    :param ax: acceleration en x
    :param ay: acceleration en y
    """
    def __init__(self, parent, x=0, y=0, ax=0, ay=0):
        super().__init__(parent)
        self.velocity = [x, y]
        self.acceleration = [ax,ay]

    @property
    def x(self):
        return self.velocity[0]

    @property
    def y(self):
        return self.velocity[1]

    @x.setter
    def x(self, value):
        self.velocity[0] = value

    @y.setter
    def y(self, value):
        self.velocity[1] = value


    @property
    def ax(self):
        return self.acceleration[0]

    @property
    def ay(self):
        return self.acceleration[1]

    @ax.setter
    def ax(self, value):
        self.acceleration[0] = value

    @ay.setter
    def ay(self, value):
        self.acceleration[1] = value

    def update(self):
        delta_time = Holder.Game.delta_time
        self.x += self.ax * delta_time
        self.y += self.ay * delta_time
        self.acceleration = [0,0]



class Cooldown:
    def __init__(self, cooldown, start_ready = True):
        self.reset_time = Holder.Game.time
        self.cooldown = cooldown
        self.ready = start_ready

    def is_ready(self):
        if Holder.Game.time >= self.reset_time + self.cooldown:
            self.ready = True
        return self.ready

    def reset(self):
        self.reset_time = Holder.Game.time
        self.ready = False
