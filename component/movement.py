import math
import Gameobject
import pygame
from component.render import RelativeCamera
import Holder

class Gravity(Gameobject.Component):
    def __init__(self):
        self.force = 30
    def update(self, game_object, delta_time):
        velocity = game_object.get_component(Gameobject.Velocity)
        if velocity:
            velocity.acceleration[1] += self.force


class PlayerSpaceMovement(Gameobject.Component):
    def __init__(self, acceleration_speed):
        self.deltav = acceleration_speed

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
                    velocity.acceleration[0] += self.deltav * math.cos(transform.angle - math.radians(90))
                    velocity.acceleration[1] += self.deltav * math.sin(transform.angle - math.radians(90))

class space_movement(Gameobject.Component):
    """
    :requires: Gameobject.Velocity
    """
    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform and velocity:
            transform.position[0] += velocity.velocity[0] * delta_time
            transform.position[1] += velocity.velocity[1] * delta_time

            # Limites de l'écran
            transform.position[0] = max(0, min(Holder.Game.LARGEUR, transform.position[0]))
            transform.position[1] = max(0, min(Holder.Game.HAUTEUR, transform.position[1]))