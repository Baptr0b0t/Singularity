from pygments.styles import get_all_styles
import Holder
import Gameobject


class Health(Gameobject.Component):
    """
    Contient les points de vie du joueur
    """
    def __init__(self, parent, health_point=100):
        super().__init__(parent)
        self.health_point = health_point

    def update(self):
        self.health_point = min(100, self.health_point)

class HealthRegen(Gameobject.Component):
    def __init__(self,parent, regen_rate=1):
        super().__init__(parent)
        self.regen_rate = 1

    def update(self):
        health = self.parent.get_component(Health)
        health.health_point+=self.regen_rate*Holder.Game.delta_time

#Todo: Add Health Bar (similar to speed arrow)
