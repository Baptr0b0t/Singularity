import math
import Gameobject
import pygame
from component.render import RelativeCamera
import Holder
import SceneManager
import taglist

class Gravity(Gameobject.Component):
    """
    Composant de gravitation de l'objet, s'attire vers les autres objets avec le meme composant.
    :param mass: Masse de l'objet
    :param fixed: Si False, le composant attire l'objet vers les sources de gravité.
                Si True, il attire uniquement les autres objets.
    :param g_force : Constante gravitationnelle
    """

    def __init__(self,parent, mass, fixed=False, g_force = 6.67430*10**-11):
        super().__init__(parent)
        self.G = g_force
        self.mass = mass #kg
        self.fixed = fixed
    def update(self):
        game_object = super().parent
        if not self.fixed:
            velocity = game_object.get_component(Gameobject.Velocity)
            transform = game_object.get_component(Gameobject.Transform)
            if velocity and transform:
                ObjectList = SceneManager.Scene.find_by_component(Gravity)

                for obj in ObjectList:
                    ObjectTransform = obj.get_component(Gameobject.Transform)
                    dx = transform.position[0]-ObjectTransform.position[0]
                    dy = transform.position[1]-ObjectTransform.position[1]
                    distance = math.sqrt(dx**2 + dy**2) * 400
                    if distance <= 10: #For not make black hole
                        continue
                    force = self.G * (self.mass * obj.get_component(Gravity).mass) / (distance ** 2)
                    velocity.acceleration[0] += -force * (dx/distance) / self.mass
                    velocity.acceleration[1] += -force * (dy/distance) / self.mass


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
                transform.angle = math.atan2(souris_y - transform.position[1], souris_x - transform.position[0]) + math.radians(90)

            if velocity:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if keys[pygame.K_LSHIFT]:
                        force = self.deltav * self.boost_force
                    else:
                        force = self.deltav
                    velocity.acceleration[1] += force * math.sin(transform.angle - math.radians(90))
                    velocity.acceleration[0] += force * math.cos(transform.angle - math.radians(90))

class SpaceMovement(Gameobject.Component):
    def __init__(self,parent):
        super().__init__(parent)

    def update(self):
        game_object = super().parent
        delta_time = Holder.Game.delta_time
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform and velocity:
            transform.position[0] += velocity.velocity[0] * delta_time
            transform.position[1] += velocity.velocity[1] * delta_time

            # Limites de l'écran
            transform.position[0] = max(0, min(Holder.Game.LARGEUR, transform.position[0]))
            transform.position[1] = max(0, min(Holder.Game.HAUTEUR, transform.position[1]))