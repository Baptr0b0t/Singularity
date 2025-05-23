import Gameobject
import pygame
import SceneManager
import math
import Holder
from taglist import PLAYER
from component.movement import Mass, Gravity
from component.render import SpriteRenderer
from component.health import Health
import eventlist


def collide_circle(obj1, obj2, obj1ratio=1, obj2ratio=1):
    """
    Collision circulaire approximée entre deux objets, en fonction de leur taille.
    """
    xdistance = obj1.get_component(Gameobject.Transform).x - obj2.get_component(Gameobject.Transform).x
    ydistance = obj1.get_component(Gameobject.Transform).y - obj2.get_component(Gameobject.Transform).y
    distancesquared = xdistance**2 + ydistance**2

    # Rayon basé sur l’échelle du sprite
    obj1radius = 0.5 * ((obj1.get_component(SpriteRenderer).scale[0] ** 2 + obj1.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)
    obj2radius = 0.5 * ((obj2.get_component(SpriteRenderer).scale[0] ** 2 + obj2.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)

    return distancesquared <= (obj1radius * obj1ratio + obj2radius * obj2ratio) ** 2

def get_penetration_depth(obj1, obj2, obj1ratio=1, obj2ratio=1):
    """
    Renvoie la profondeur de pénétration entre deux objets circulaires.
    Si les objets ne se chevauchent pas, retourne 0.
    """
    # Obtenir les positions
    pos1 = obj1.get_component(Gameobject.Transform)
    pos2 = obj2.get_component(Gameobject.Transform)

    # Distance entre les centres
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    center_distance = (dx**2 + dy**2) ** 0.5

    # Calcul des rayons basés sur l’échelle
    scale1 = obj1.get_component(SpriteRenderer).scale
    scale2 = obj2.get_component(SpriteRenderer).scale

    radius1 = 0.5 * ((scale1[0] ** 2 + scale1[1] ** 2) ** 0.5) * obj1ratio
    radius2 = 0.5 * ((scale2[0] ** 2 + scale2[1] ** 2) ** 0.5) * obj2ratio

    # Somme des rayons
    sum_radii = radius1 + radius2

    # Profondeur de pénétration
    penetration = sum_radii - center_distance
    return max(0, penetration)  # Retourne 0 si pas de pénétration



class PlanetCollision(Gameobject.Component):
    """
    Gère les collisions entre objets avec restitution (rebond) et dégâts.
    """
    def __init__(self, parent, restitution=1, ratio=1, damage_on_other=0):
        super().__init__(parent)
        self.restitution = restitution
        self.collision_ratio = ratio
        self.handled_collision = []  # Évite les collisions doubles dans le même frame
        self.damage_on_other = damage_on_other

    def update(self):
        game_object = self.parent
        self.handled_collision.clear()
        ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)

        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        mass = game_object.get_component(Mass).mass

        if velocity and transform:
            for obj in ObjectList:
                if obj == game_object or game_object in obj.get_component(PlanetCollision).handled_collision:
                    continue

                if collide_circle(game_object, obj, self.collision_ratio, obj.get_component(PlanetCollision).collision_ratio):
                    # Calcul de la nouvelle vitesse après collision
                    obj_mass = obj.get_component(Mass).mass
                    obj_transform = obj.get_component(Gameobject.Transform)
                    obj_velocity = obj.get_component(Gameobject.Velocity)
                    obj_collision = obj.get_component(PlanetCollision)
                    if not obj_velocity:
                        obj_velocity.x = 0
                        obj_velocity.y = 0

                    normal_x = obj_transform.x - transform.x
                    normal_y = obj_transform.y - transform.y
                    distance = math.sqrt(normal_x**2 + normal_y**2)
                    if distance == 0:
                        distance = 1  # Évite division par 0
                    normal_x /= distance
                    normal_y /= distance

                    v1n = velocity.x * normal_x + velocity.y * normal_y
                    v2n = obj_velocity.x * normal_x + obj_velocity.y * normal_y

                    # Formule de collision élastique
                    new_v1n = ((v1n * (mass - obj_mass) + 2 * obj_mass * v2n) / (mass + obj_mass))
                    new_v2n = ((v2n * (obj_mass - mass) + 2 * mass * v1n) / (mass + obj_mass))

                    # Mise à jour de la vitesse
                    velocity.x += (new_v1n - v1n) * normal_x
                    velocity.y += (new_v1n - v1n) * normal_y
                    velocity.x *= self.restitution
                    velocity.y *= self.restitution

                    obj_velocity.x += (new_v2n - v2n) * normal_x
                    obj_velocity.y += (new_v2n - v2n) * normal_y
                    obj_velocity.x *= obj_collision.restitution
                    obj_velocity.y *= obj_collision.restitution

                    self.handled_collision.append(obj)

                    penetration_depth = get_penetration_depth(game_object, obj, self.collision_ratio, obj.get_component(PlanetCollision).collision_ratio)
                    if penetration_depth > 0:
                        total_mass = mass + obj_mass
                        if total_mass == 0:
                            total_mass = 1  # éviter division par zéro

                        push_self = (obj_mass / total_mass) * penetration_depth
                        push_other = (mass / total_mass) * penetration_depth

                        transform.x -= normal_x * push_self
                        transform.y -= normal_y * push_self

                        obj_transform.x += normal_x * push_other
                        obj_transform.y += normal_y * push_other
                    #Stuck Resolver - End
                    damage_proportion = abs(v1n - v2n) * 0.01
                    if obj.has_component(Health):
                        obj.get_component(Health).health_point -= self.damage_on_other * damage_proportion
                    if game_object.has_component(Health):
                        game_object.get_component(Health).health_point -= obj_collision.damage_on_other * damage_proportion
                    if obj.has_tag(PLAYER) or game_object.has_tag(PLAYER):
                        Holder.Game.sound_player.play_sound(f"planet_collision", volume=0.2)
                        Holder.Game.Collision_done += 1



class ScreenLimit(Gameobject.Component):
    """
    Limite la position de l'objet à l'écran, rebond possible sur les bords.
    """
    def __init__(self, parent, bounce=False, force=2):
        super().__init__(parent)
        self.bounce = bounce
        self.force = force

    def update(self):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)

        if self.bounce:
            velocity = game_object.get_component(Gameobject.Velocity)
            if velocity:
                if transform.x > Holder.Game.LARGEUR or transform.x < 0:
                    velocity.x += -self.force * velocity.x
                if transform.y > Holder.Game.LARGEUR or transform.y < 0:
                    velocity.y += -self.force * velocity.y

        # Force l'objet à rester dans l'écran
        transform.x = max(0, min(Holder.Game.LARGEUR, transform.x))
        transform.y = max(0, min(Holder.Game.HAUTEUR, transform.y))


class DeleteOnCollision(Gameobject.Component, Gameobject.Cooldown):
    """
    Supprime l'objet après une collision ou s'il sort de l'écran.
    """
    def __init__(self, parent, screen_limit=False, planet_collision_ratio=1, seconds_before_start=0, reward_money=0, tag_filter=None):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, seconds_before_start)
        self.screen_limit = screen_limit
        self.planet_collision_ratio = planet_collision_ratio
        self.reward_money = reward_money
        self.tag_filter = tag_filter
        Gameobject.Cooldown.reset(self)

    def update(self):
        game_object = self.parent
        if not Gameobject.Cooldown.is_ready(self):
            return

        transform = game_object.get_component(Gameobject.Transform)

        # Supprime l’objet s’il sort de l’écran
        if self.screen_limit and (
                transform.x >= Holder.Game.LARGEUR or transform.x <= 0 or
                transform.y >= Holder.Game.LARGEUR or transform.y <= 0):
            SceneManager.Scene.remove_object(game_object)
            return

        if self.planet_collision_ratio > 0:
            ObjectList = SceneManager.Scene.find_by_tag(self.tag_filter) if self.tag_filter else SceneManager.Scene.find_by_component(PlanetCollision)

            for obj in ObjectList:
                if obj == game_object:
                    continue

                if collide_circle(game_object, obj, self.planet_collision_ratio, obj.get_component(PlanetCollision).collision_ratio):
                    if self.reward_money > 0:
                        Holder.Game.Money_received += self.reward_money
                        Holder.Game.add_money(self.reward_money)
                    SceneManager.Scene.remove_object(game_object)
                    return


class DamageCollision(Gameobject.Component, Gameobject.Cooldown):
    """
    Inflige des dégâts à l'objet touché.
    """
    def __init__(self, parent, ratio=1, damage_on_other=10, cooldown=.26, do_delete=False):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.planet_collision_ratio = ratio
        self.damage_on_other = damage_on_other
        self.do_delete = do_delete
        Gameobject.Cooldown.reset(self)

    def update(self):
        game_object = self.parent
        if not Gameobject.Cooldown.is_ready(self) or self.damage_on_other == 0:
            return

        ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)
        for obj in ObjectList:
            if obj == game_object:
                continue

            if collide_circle(game_object, obj, self.planet_collision_ratio, obj.get_component(PlanetCollision).collision_ratio):
                if obj.has_component(Health):
                    obj.get_component(Health).health_point -= self.damage_on_other
                    if obj.has_tag(PLAYER):
                        Holder.Game.sound_player.play_sound(f"got_shot", volume=0.8)
                if self.do_delete:
                    SceneManager.Scene.remove_object(game_object)

    def boot_up(self):
        # Réinitialise le cooldown au lancement
        Gameobject.Cooldown.reset(self)


class Checkpoint(Gameobject.Component):
    """
    Déclenche un événement si le joueur touche ce point.
    """
    def __init__(self, parent, ratio=1):
        Gameobject.Component.__init__(self, parent)
        self.planet_collision_ratio = ratio

    def update(self):
        game_object = self.parent
        objectlist = SceneManager.Scene.find_by_tag(PLAYER)

        for obj in objectlist:
            if obj == game_object:
                continue

            if collide_circle(game_object, obj, self.planet_collision_ratio, 1):
                Holder.Game.post_event(eventlist.SCENE_MENU)
