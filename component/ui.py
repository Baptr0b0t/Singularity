import Gameobject
import Holder
from component.render import FontRenderer, SpriteRenderer, RectangleRenderer, RelativeCamera
from component.health import Health
from component.movement import Fuel
import math
import SceneManager
from taglist import PLAYER

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
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)

class Coordinate_UI(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, end_texte = "meter", color = (255,255,255), size = 1, cooldown = 0.3):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.end_texte = end_texte



    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            player_object = SceneManager.Scene.find_by_tag(PLAYER)[0]
            player_transform = player_object.get_component(Gameobject.Transform)
            texte = str(round(player_transform.x)) + "," + str(round(player_transform.y))
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)

class Speed_UI(Gameobject.Component, Gameobject.Cooldown):
    """
    Need FontRenderer and a Gameobject with "PLAYER" tag exist
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, end_texte = "m/s", color = (255,255,255), size = 1, cooldown = 0.3, is_single_value = True):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.end_texte = end_texte
        self.is_single_value = is_single_value



    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            player_object = SceneManager.Scene.find_by_tag(PLAYER)[0] #TODO: Make crash proof (Empty text when no player found)
            player_speed = player_object.get_component(Gameobject.Velocity)
            if self.is_single_value:
                texte = str(round(math.hypot(player_speed.x, player_speed.y))) + self.end_texte
            else:
                texte = str(round(player_speed.x)) + "," + str(round(player_speed.y)) + self.end_texte
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)


class Money_UI(Gameobject.Component, Gameobject.Cooldown):
    """
    Need FontRenderer and a Gameobject with "PLAYER" tag exist
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, end_texte = "$", color = (255,255,255), size = 1, cooldown = 0.3):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.end_texte = end_texte

    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            player_money = Holder.Game.money
            texte = str(round(player_money)) + self.end_texte
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)


class Health_UI(Gameobject.Component, Gameobject.Cooldown):
    """
    Need FontRenderer and a Gameobject with "PLAYER" tag exist
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, begining_texte = "Health  ", color = (0,255,0), size = 1, show_max = True, cooldown = 0.2):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.begining_texte = begining_texte
        self.show_max = show_max

    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            player_object = SceneManager.Scene.find_by_tag(PLAYER)[0] #TODO: Make crash proof (Empty text when no player found)
            health = player_object.get_component(Health)
            texte = self.begining_texte + str(round(health.health_point))
            if self.show_max:
                texte = texte + "/" +str(round(health.max_health_point))
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)

class Score_UI(Gameobject.Component, Gameobject.Cooldown):
    """
    Need FontRenderer and a Gameobject with "PLAYER" tag exist
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, begining_texte = "Score : ", color = (255,255,255), size = 1, cooldown = 0.1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        self.begining_texte = begining_texte

    def update(self):
        if Gameobject.Cooldown.is_ready(self):
            game_object = self.parent
            player_score = Holder.Game.score
            texte = self.begining_texte + str(round(player_score))
            game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)
            Gameobject.Cooldown.reset(self)

class Stat_UI(Gameobject.Component):
    """
    Need FontRenderer
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, color = (255,255,255), size = 1):
        Gameobject.Component.__init__(self, parent)
        self.color = color
        self.size = size
    def boot_up(self):
        game_object = self.parent
        holder = Holder.Game
        texte = "Shot done :" + str(round(holder.Shot_done)) + "Collision :" + str(round(holder.Collision_done)) + "Money received :" + str(round(holder.Money_received)) + "Enemy killed :" + str(round(holder.Enemy_killed))
        game_object.get_component(FontRenderer).change_text(texte, self.color, self.size)


class Health_Rectangle(Gameobject.Component, Gameobject.Cooldown):
    """
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, color = (0,255,0), size = 1, cooldown = 1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size
        #Todo: do the component


class Fuel_Rectangle(Gameobject.Component, Gameobject.Cooldown):
    """
    :param color exemple value (255,255,255) or "BLANK"
    """
    def __init__(self, parent, color = (0,255,0), size = (90,10), cooldown = 0.5):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.color = color
        self.size = size

    def update(self):
        rectangle_renderer = self.parent.get_component(RectangleRenderer)
        player_object = SceneManager.Scene.find_by_tag(PLAYER)[0]
        fuel = player_object.get_component(Fuel)
        if fuel:
            coef = fuel.fuel/fuel.max_fuel
            rectangle_renderer.change_size(size = (self.size[0] * coef, self.size[1]))

class Velocity_Arrow(Gameobject.Component):
    def __init__(self, parent, scale = 0.03, max_speed_size = 80):
        Gameobject.Component.__init__(self, parent)
        self.arrow = Gameobject.GameObject((Holder.Game.LARGEUR//2,Holder.Game.HAUTEUR//2))
        self.max_speed_size = max_speed_size
        self.arrow.add_self_updated_component(SpriteRenderer(self.arrow, "./resources/icon/arrow.png", scale))

        if parent.has_component(RelativeCamera):
            self.arrow.add_standard_component(RelativeCamera(self.arrow))

        SceneManager.Scene.add_object(self.arrow)

    def update(self):
        game_object = self.parent
        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        arrow_transform = self.arrow.get_component(Gameobject.Transform)
        arrow_renderer = self.arrow.get_component(SpriteRenderer)

        arrow_transform.angle = math.atan2(velocity.y, velocity.x)
        arrow_transform.x, arrow_transform.y = transform.x, transform.y
        arrow_renderer.set_scale((min(math.sqrt(velocity.y**2 + velocity.x**2),self.max_speed_size), arrow_renderer.scale[1]))

    def delete(self):
        SceneManager.Scene.remove_object(self.arrow)
