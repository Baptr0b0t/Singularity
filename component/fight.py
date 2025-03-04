import Gameobject
import pygame
from component.render import SpriteRenderer, RelativeCamera
import SceneManager
import math
from component.movement import SpaceMovement
from component.collision import DeleteOnCollision, PlanetCollision


class PlayerShot(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, fire_rate = 0.07, speed = 190, bullet_pathfile = "./resources/blast_red.png", scale = 0.06):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, fire_rate)
        self.speed = speed
        self.path_file = bullet_pathfile
        self.scale = scale


    def update(self):
        game_object = self.parent


        if not Gameobject.Cooldown.is_ready(self):
            return

        transform = game_object.get_component(Gameobject.Transform)
        mouse_presses = pygame.mouse.get_pressed()

        if mouse_presses[0]:
            Gameobject.Cooldown.reset(self)
            #Creating bullet Gameobject
            bullet = Gameobject.GameObject((transform.x, transform.y), angle=transform.angle)
            bullet.add_self_updated_component(SpriteRenderer(bullet, self.path_file, self.scale))

            if game_object.has_component(RelativeCamera):
                relative_cam = game_object.get_component(RelativeCamera)
                bullet.add_standard_component(RelativeCamera(bullet, relative_cam.scale_factor))
            bullet.add_standard_component(SpaceMovement(bullet))
            bullet.add_quick_updated_component(Gameobject.Velocity(bullet, x= self.speed * math.cos(transform.angle - math.radians(90)), y= self.speed * math.sin(transform.angle - math.radians(90))))
            if game_object.has_component(Gameobject.Velocity):
                game_object_velocity = game_object.get_component(Gameobject.Velocity)
                bullet_velocity = bullet.get_component(Gameobject.Velocity)
                bullet_velocity.x += game_object_velocity.x
                bullet_velocity.y += game_object_velocity.y

            bullet.add_standard_component(DeleteOnCollision(bullet, screen_limit=False, planet_collision_ratio=1 ,seconds_before_start=.26))
            SceneManager.Scene.add_object(bullet)


class BulletMovement(Gameobject.Component):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        pass


#Todo: Add Bullet damager (Similar to Delete on colision)