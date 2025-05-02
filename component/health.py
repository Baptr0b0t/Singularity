import Holder
import Gameobject
import SceneManager

class Health(Gameobject.Component):
    """
    Contient les points de vie du joueur
    """
    def __init__(self, parent, health_point=100, max_health_point=100):
        super().__init__(parent)
        self.health_point = health_point
        self.max_health_point = max_health_point

    def update(self):
        self.health_point = min(self.max_health_point, self.health_point)

    def upgrade(self, value):
        self.health_point += value
        self.max_health_point += value

class HealthRegen(Gameobject.Component):
    def __init__(self,parent, regen_rate=1):
        super().__init__(parent)
        self.regen_rate = 1

    def update(self):
        health = self.parent.get_component(Health)
        health.health_point+=self.regen_rate*Holder.Game.delta_time

#Todo: Add Health Bar (similar to speed arrow)


class DestroyOnNoHealth(Gameobject.Component):
    """
    Destroy GameObject when Health < 0
    """
    def __init__(self,parent):
        super().__init__(parent)

    def update(self):
        game_object = self.parent
        health = game_object.get_component(Health)
        if health.health_point<0:
            SceneManager.Scene.remove_object(game_object)


class EventOnNoHealth(Gameobject.Component):
    """
    Post event when Health < 0
    Exemple : GameOver
    """
    def __init__(self,parent, event):
        super().__init__(parent)
        self.event = event

    def update(self):
        game_object = self.parent
        health = game_object.get_component(Health)
        if health.health_point<0:
            Holder.Game.post_event(eval(str("eventlist." + self.event)))


class ScoreOnDestroy(Gameobject.Component):
    def __init__(self, parent, value = 15):
        super().__init__(parent)
        self.value = value

    def delete(self):
        Holder.Game.add_score(self.value)