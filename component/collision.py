import Gameobject
import pygame
import SceneManager
import math
import Holder
import taglist
from component.movement import Mass
from component.render import SpriteRenderer

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
        self.restitution = restitution # 1 = collision rigide , 0 = aucune collision
        self.collision_ratio = ratio
        self.handled_collision = []

    def update(self):

        game_object = super().parent

        self.handled_collision.clear()
        ObjectList = SceneManager.Scene.find_by_component(PlanetCollision)
        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        mass = game_object.get_component(Mass).mass
        print(f"{game_object} fait des collision")
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
                    obj_collision = obj.get_component(PlanetCollision)

                    normal_x = obj_transform.x - transform.x
                    normal_y = obj_transform.y - transform.y
                    distance = math.sqrt(normal_x**2 + normal_y**2)
                    if distance == 0:
                        distance = 0.001  # Éviter la division par zéro
                    normal_x /= distance
                    normal_y /= distance
                    v1n = velocity.x * normal_x + velocity.y * normal_y
                    v2n = obj_velocity.x * normal_x + obj_velocity.y * normal_y

                    new_v1n = ((v1n * (mass - obj_mass) + 2 * obj_mass * v2n) / (mass + obj_mass)) * self.restitution
                    new_v2n = ((v2n * (obj_mass - mass) + 2 * mass * v1n) / (mass + obj_mass)) * obj_collision.restitution
                    velocity.x += (new_v1n - v1n) * normal_x
                    velocity.y += (new_v1n - v1n) * normal_y
                    obj_velocity.x += (new_v2n - v2n) * normal_x
                    obj_velocity.y += (new_v2n - v2n) * normal_y

                    self.handled_collision.append(obj)