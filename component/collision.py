import Gameobject
import pygame
import SceneManager
import math
import Holder
from taglist import PLAYER
from component.movement import Mass
from component.render import SpriteRenderer
from component.health import Health
import eventlist


def collide_circle(obj1, obj2, obj1ratio = 1, obj2ratio = 1): #From pygame.sprite.collide_circle
    xdistance = obj1.get_component(Gameobject.Transform).x - obj2.get_component(Gameobject.Transform).x
    ydistance = obj1.get_component(Gameobject.Transform).y - obj2.get_component(Gameobject.Transform).y
    distancesquared = xdistance**2 + ydistance**2

    obj1radius = 0.5 * ((obj1.get_component(SpriteRenderer).scale[0] ** 2 + obj1.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)
    obj2radius = 0.5 * ((obj2.get_component(SpriteRenderer).scale[0] ** 2 + obj2.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)

    return distancesquared <= (obj1radius * obj1ratio + obj2radius * obj2ratio) ** 2

class PlanetCollision(Gameobject.Component):
    """
    Composant de collision d'objet avec des planetes dans l'espace.
    :param restitution: Coefficient de collision.
    :param ratio: Coefficient de la taille de collision par rapport au sprite.
    """
    def __init__(self, parent, restitution = 1, ratio=1):
        super().__init__(parent)
        self.restitution = restitution # 1 = collision parfaite, 0 = Perte totale d'energie
        self.collision_ratio = ratio
        self.handled_collision = []

    def update(self):

        game_object = self.parent

        self.handled_collision.clear()
        ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)
        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        mass = game_object.get_component(Mass).mass
        if velocity and transform:
            for obj in ObjectList:
                if obj == game_object:
                    continue
                if game_object in obj.get_component(PlanetCollision).handled_collision:
                    continue

                if collide_circle(game_object, obj, self.collision_ratio, obj.get_component(PlanetCollision).collision_ratio):

                    obj_mass = obj.get_component(Mass).mass
                    obj_transform = obj.get_component(Gameobject.Transform)
                    obj_velocity = obj.get_component(Gameobject.Velocity)
                    if not obj_velocity:
                        obj_velocity.x = 0
                        obj_velocity.y = 0
                    obj_collision = obj.get_component(PlanetCollision)

                    normal_x = obj_transform.x - transform.x
                    normal_y = obj_transform.y - transform.y
                    distance = math.sqrt(normal_x**2 + normal_y**2)
                    if distance == 0:
                        distance = 1  # Éviter la division par zéro
                    normal_x /= distance
                    normal_y /= distance
                    v1n = velocity.x * normal_x + velocity.y * normal_y
                    v2n = obj_velocity.x * normal_x + obj_velocity.y * normal_y

                    new_v1n = ((v1n * (mass - obj_mass) + 2 * obj_mass * v2n) / (mass + obj_mass))
                    new_v2n = ((v2n * (obj_mass - mass) + 2 * mass * v1n) / (mass + obj_mass))
                    velocity.x += (new_v1n - v1n) * normal_x
                    velocity.y += (new_v1n - v1n) * normal_y
                    velocity.x *= self.restitution
                    velocity.y *= self.restitution

                    obj_velocity.x += (new_v2n - v2n) * normal_x
                    obj_velocity.y += (new_v2n - v2n) * normal_y
                    obj_velocity.x *= obj_collision.restitution
                    obj_velocity.y *= obj_collision.restitution

                    self.handled_collision.append(obj)

                    #Stuck Resolver #Todo: add a delay for don't bug other collision like DamageCollision or use a Collision detector will call all other method from the gameObject
                    if mass<=obj_mass:
                        transform.x -= normal_x
                        transform.y -= normal_y
                    if mass>=obj_mass:
                        obj_transform.x += normal_x
                        obj_transform.y += normal_y



class ScreenLimit(Gameobject.Component):
    def __init__(self, parent, bounce = False, force = 2):
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
        transform.x = max(0, min(Holder.Game.LARGEUR, transform.x))
        transform.y = max(0, min(Holder.Game.HAUTEUR, transform.y))


class DeleteOnCollision(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, screen_limit = False, planet_collision_ratio = 1, seconds_before_start = 0, reward_money = 0, tag_filter=None):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, seconds_before_start) #Timer for not be destroyed by the Gameobject generator
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
        if self.screen_limit:
            if transform.x >= Holder.Game.LARGEUR or transform.x <= 0 or transform.y >= Holder.Game.LARGEUR or transform.y <= 0:
                SceneManager.Scene.remove_object(game_object)
                return

        if self.planet_collision_ratio > 0:
            if self.tag_filter is None:
                ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)
            else:
                ObjectList = SceneManager.Scene.find_by_tag(self.tag_filter)
            for obj in ObjectList:
                if obj == game_object:
                    continue

                if collide_circle(game_object, obj, self.planet_collision_ratio, obj.get_component(PlanetCollision).collision_ratio):
                    if self.reward_money>0:
                        Holder.Game.add_money(self.reward_money)
                    SceneManager.Scene.remove_object(game_object)
                    return


class DamageCollision(Gameobject.Component, Gameobject.Cooldown):
    """
    Composant pour appliquer des damages lorsqu'il y a contact avec un object soumis a des collision par PlanetCollision
    """
    def __init__(self, parent, ratio = 1, damage_on_other = 10, cooldown = .26, do_delete = False):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.planet_collision_ratio = ratio
        self.damage_on_other = damage_on_other
        self.do_delete = do_delete
        Gameobject.Cooldown.reset(self)


    def update(self):
        game_object = self.parent

        if not Gameobject.Cooldown.is_ready(self) or self.damage_on_other==0:
            return

        ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)
        for obj in ObjectList:
            if obj == game_object:
                continue

            if collide_circle(game_object, obj, self.planet_collision_ratio, obj.get_component(PlanetCollision).collision_ratio):
                if obj.has_component(Health):
                    obj.get_component(Health).health_point -= self.damage_on_other
                if self.do_delete:
                    SceneManager.Scene.remove_object(game_object)

    def boot_up(self):
        Gameobject.Cooldown.reset(self) #Lors du retour en jeu, empeche les damages sur le joueur qui tire.








class Checkpoint(Gameobject.Component):
    def __init__(self, parent, ratio = 1):
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

