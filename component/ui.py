import Gameobject
import Holder
from component.render import FontRenderer, SpriteRenderer, RelativeCamera
import math
import SceneManager

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


class Velocity_Arrow(Gameobject.Component):
    def __init__(self, parent, scale = 0.018, max_speed_size = 60):
        Gameobject.Component.__init__(self, parent)
        self.arrow = Gameobject.GameObject((Holder.Game.LARGEUR//2,Holder.Game.HAUTEUR//2))
        self.max_speed_size = max_speed_size
        self.arrow.add_self_updated_component(SpriteRenderer(self.arrow, "./resources/icon/arrow.png", scale))

        if parent.has_component(RelativeCamera):
            relative_cam = parent.get_component(RelativeCamera)
            self.arrow.add_standard_component(RelativeCamera(self.arrow, relative_cam.scale_factor*0.5))

        SceneManager.Scene.add_object(self.arrow)

    def update(self):
        game_object = super().parent
        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        arrow_transform = self.arrow.get_component(Gameobject.Transform)
        arrow_renderer = self.arrow.get_component(SpriteRenderer)

        arrow_transform.angle = math.atan2(velocity.y, velocity.x)
        arrow_transform.x, arrow_transform.y = transform.x, transform.y
        arrow_renderer.set_scale((min(math.sqrt(velocity.y**2 + velocity.x**2),self.max_speed_size), arrow_renderer.scale[1]))
