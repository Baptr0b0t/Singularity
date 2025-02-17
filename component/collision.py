import Gameobject
import pygame
import SceneManager
import math

from component.movement import Mass
from component.render import SpriteRenderer

def collide_circle(obj1, obj2, obj1ratio = 1, obj2ratio = 1): #From pygame.sprite.collide_circle
    xdistance = obj1.get_component(Gameobject.Transform).x - obj2.get_component(Gameobject.Transform).x
    ydistance = obj1.get_component(Gameobject.Transform).y - obj2.get_component(Gameobject.Transform).y
    distancesquared = xdistance**2 + ydistance**2

    obj1radius = 0.5 * ((obj1.get_component(SpriteRenderer).scale[0] ** 2 + obj1.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)
    obj2radius = 0.5 * ((obj2.get_component(SpriteRenderer).scale[0] ** 2 + obj2.get_component(SpriteRenderer).scale[1] ** 2) ** 0.5)

    return distancesquared <= (obj1radius * obj1ratio + obj2radius * obj2ratio) ** 2

class Collision(Gameobject.Component):
    """
    Composant de collision avec detection en cercle de l'objet dans l'espace.
    :param restitution: Coefficient de collision.
    """
    def __init__(self, parent, restitution = 1, ratio=1):
        super().__init__(parent)
        self.restitution = restitution # 1 = collision rigide , 0 = aucune collision
        self.collision_ratio = ratio
        self.active = True #Un seul objet doit faire tout les calcul


    def update(self):
        if not self.active:
            return
        game_object = super().parent
        ObjectList = SceneManager.Scene.find_by_component(Collision)
        velocity = game_object.get_component(Gameobject.Velocity)
        transform = game_object.get_component(Gameobject.Transform)
        mass = game_object.get_component(Mass).mass
        if velocity and transform:
            for obj in ObjectList:
                if obj == game_object:
                    continue

                if collide_circle(game_object, obj, self.collision_ratio, obj.get_component(Collision).collision_ratio):
                    collision_angle = math.atan2(transform.y - obj.get_component(Gameobject.Transform).y, transform.x - obj.get_component(Gameobject.Transform).x)
                    self_speed = math.sqrt(velocity.x ** 2 + velocity.y ** 2)  # Norme de la vitesse
                    obj_speed = math.sqrt(obj.get_component(Gameobject.Velocity).x ** 2 + obj.get_component(Gameobject.Velocity).y ** 2)
                    obj_mass = obj.get_component(Mass).mass

                    self_speed = ((self_speed * (mass - obj_mass) + 2 * obj_mass * obj_speed) / (mass + obj_mass) - self_speed)
                    obj_speed = (obj_speed * (obj_mass - mass) + 2 * mass * self_speed) / (mass + obj_mass) - obj_speed


                    velocity.x += math.cos(collision_angle) * -self_speed * self.restitution
                    velocity.y += math.sin(collision_angle) * -self_speed * self.restitution
                    obj.get_component(Gameobject.Velocity).x += math.cos(collision_angle) * obj_speed * obj.get_component(Collision).restitution
                    obj.get_component(Gameobject.Velocity).y += math.sin(collision_angle) * obj_speed * obj.get_component(Collision).restitution
