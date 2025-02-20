import math
import Gameobject
import pygame
from component.render import RelativeCamera
import Holder
import SceneManager
import taglist

class Mass(Gameobject.Component):
    """
    :param mass: Masse de l'objet
    """
    def __init__(self,parent, mass):
        super().__init__(parent)
        self.mass = mass


class Gravity(Gameobject.Component):
    """
    Composant de gravitation de l'objet, s'attire vers les autres objets avec le meme composant.
    :param fixed: Si False, le composant attire l'objet vers les sources de gravité.
                Si True, il attire uniquement les autres objets.
    :param g_force : Constante gravitationnelle
    """

    def __init__(self,parent, fixed=False, g_force = 6.67430*10**-11):
        super().__init__(parent)
        self.G = g_force
        self.fixed = fixed
    def update(self):
        game_object = super().parent
        if not self.fixed:
            velocity = game_object.get_component(Gameobject.Velocity)
            transform = game_object.get_component(Gameobject.Transform)
            mass = game_object.get_component(Mass).mass
            if velocity and transform:
                object_list = SceneManager.Scene.find_by_component(Gravity)

                for obj in object_list:
                    if obj == game_object:
                        continue
                    object_transform = obj.get_component(Gameobject.Transform)
                    dx = transform.x - object_transform.x
                    dy = transform.y - object_transform.y
                    distance = math.sqrt(dx**2 + dy**2) * 200
                    if distance <= 1: #For not make black hole
                        continue
                    force = self.G * (mass * obj.get_component(Mass).mass) / (distance ** 2)
                    velocity.ax += -force * (dx/distance) / mass
                    velocity.ay += -force * (dy/distance) / mass


class PlayerSpaceMovement(Gameobject.Component):
    """
    Composant de mouvement de l'objet dans l'espace par les inputs.
    :param acceleration_speed: Force de poussée
    :param boost_force: Coefficient du boost
    """
    def __init__(self,parent, acceleration_speed, boost_force = 8):
        super().__init__(parent)
        self.deltav = acceleration_speed
        self.boost_force = boost_force

    def update(self):
        game_object = super().parent
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform:
            souris_x, souris_y = pygame.mouse.get_pos()
            relative_camera = game_object.get_component(RelativeCamera)
            if relative_camera and relative_camera.active:
                transform.angle = math.atan2(souris_y - relative_camera.position[1], souris_x - relative_camera.position[0]) + math.radians(90)
            else:
                transform.angle = math.atan2(souris_y - transform.y, souris_x - transform.x) + math.radians(90)

            if velocity:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if keys[pygame.K_LSHIFT]:
                        force = self.deltav * self.boost_force
                    else:
                        force = self.deltav
                    velocity.ax += force * math.cos(transform.angle - math.radians(90))
                    velocity.ay += force * math.sin(transform.angle - math.radians(90))

class SpaceMovement(Gameobject.Component):
    def __init__(self,parent):
        super().__init__(parent)

    def update(self):
        game_object = super().parent
        delta_time = Holder.Game.delta_time
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform and velocity:
            transform.x += velocity.x * delta_time
            transform.y += velocity.y * delta_time
        #Pygame limitation [-2147483647;2147483646]
        transform.x = max(-214748364, min(214748364, transform.x))
        transform.y = max(-214748364, min(214748364, transform.y))

class SpeedLimit(Gameobject.Component):
    def __init__(self,parent, speedlimit = 10):
        super().__init__(parent)
        self.speedlimit = speedlimit

    def update(self):
        game_object = super().parent
        velocity = game_object.get_component(Gameobject.Velocity)
        velocity.x = max(-self.speedlimit, min(self.speedlimit, velocity.x))
        velocity.y = max(-self.speedlimit, min(self.speedlimit, velocity.y))
