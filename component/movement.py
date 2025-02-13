import math
import Gameobject
import pygame
from component.render import RelativeCamera
import Holder
import SceneManager
import taglist

class Gravity(Gameobject.Component):
    def __init__(self, mass, fixed=False, g_force = 6.67430*10**-11):
        self.G = g_force
        self.mass = mass #kg
        self.fixed = fixed
    def update(self, game_object, delta_time):
        if not self.fixed:
            velocity = game_object.get_component(Gameobject.Velocity)
            transform = game_object.get_component(Gameobject.Transform)
            if velocity and transform:
                ObjectList = SceneManager.Scene.find_by_component(Gravity)

                for obj in ObjectList:
                    ObjectTransform = obj.get_component(Gameobject.Transform)
                    dx = transform.position[0]-ObjectTransform.position[0]
                    dy = transform.position[1]-ObjectTransform.position[1]
                    distance = math.sqrt(dx**2 + dy**2) * 100
                    if distance <= 10: #For not make black hole
                        continue
                    force = self.G * (self.mass * obj.get_component(Gravity).mass) / (distance ** 2)
                    print("force:", force)
                    velocity.acceleration[0] += -force * (dx/distance) / self.mass
                    velocity.acceleration[1] += -force * (dy/distance) / self.mass


class PlayerSpaceMovement(Gameobject.Component):
    def __init__(self, acceleration_speed):
        self.deltav = acceleration_speed
        self.boost_force = 2

    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform:
            souris_x, souris_y = pygame.mouse.get_pos()
            relativecamera = game_object.get_component(RelativeCamera)
            if relativecamera and relativecamera.active:
                transform.angle = math.atan2(souris_y - relativecamera.position[1], souris_x - relativecamera.position[0]) + math.radians(90)
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
    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform and velocity:
            transform.position[0] += velocity.velocity[0] * delta_time
            transform.position[1] += velocity.velocity[1] * delta_time

            # Limites de l'écran
            transform.position[0] = max(0, min(Holder.Game.LARGEUR, transform.position[0]))
            transform.position[1] = max(0, min(Holder.Game.HAUTEUR, transform.position[1]))