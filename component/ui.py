import Gameobject
import Holder
from component.render import FontRenderer


class FPS_UI(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, end_texte = "FPS", color = (255,255,255), size = 1, cooldown = 1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.end_texte = end_texte



    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            delta_time = Holder.Game.delta_time
            texte = str(round(1/delta_time)) + self.end_texte
            game_object.get_component(FontRenderer).change_text(texte, self.color)
            Gameobject.Cooldown.reset(self)