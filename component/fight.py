import Gameobject
import pygame
from component.render import SpriteRenderer, RelativeCamera
import SceneManager
import math
from component.movement import SpaceMovement
from component.collision import DeleteOnCollision, DamageCollision


class PlayerShot(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, fire_rate = 0.07, speed = 220, bullet_pathfile = "./resources/blast_red.png", scale = 0.06):
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
                bullet.add_standard_component(RelativeCamera(bullet))
            bullet.add_standard_component(SpaceMovement(bullet))
            bullet.add_quick_updated_component(Gameobject.Velocity(bullet, x= self.speed * math.cos(transform.angle - math.radians(90)), y= self.speed * math.sin(transform.angle - math.radians(90))))
            if game_object.has_component(Gameobject.Velocity):
                game_object_velocity = game_object.get_component(Gameobject.Velocity)
                bullet_velocity = bullet.get_component(Gameobject.Velocity)
                bullet_velocity.x += game_object_velocity.x
                bullet_velocity.y += game_object_velocity.y

            bullet.add_standard_component(DamageCollision(bullet, damage_on_other=10))
            bullet.add_standard_component(BulletLifeTime(bullet, life_time= 10))
            bullet.add_standard_component(DeleteOnCollision(bullet, screen_limit=False, planet_collision_ratio=1 ,seconds_before_start=.26))
            SceneManager.Scene.add_object(bullet)

    def boot_up(self):
        Gameobject.Cooldown.reset(self)

class Turret_Holder(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, fire_rate = 0.07, offset = 10, turret_pathfile = "./resources/enemy_ship_turret.png", scale = 0.3):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, fire_rate)
        self.turret_path = turret_pathfile
        self.scale = scale
        self.offset = offset

        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        self.turret = Gameobject.GameObject((transform.x, transform.y), angle=0)
        self.turret.add_self_updated_component(SpriteRenderer(self.turret, self.turret_path, self.scale))
        if game_object.has_component(RelativeCamera):
            self.turret.add_standard_component(RelativeCamera(self.turret))
        SceneManager.Scene.add_object(self.turret, front=True)


    def update(self):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        turret_transform = self.turret.get_component(Gameobject.Transform)


        turret_transform.x = transform.x + self.offset * math.cos(transform.angle-math.radians(90))
        turret_transform.y = transform.y + self.offset * math.sin(transform.angle-math.radians(90))


    def delete(self):
        SceneManager.Scene.remove_object(self.turret)




class BulletLifeTime(Gameobject.Component,Gameobject.Cooldown):
    """
    Remove Gameobject when existed for too long (lag killer)
    """
    def __init__(self, parent, life_time = 10):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, life_time)
        Gameobject.Cooldown.reset(self)

    def update(self):
        if not Gameobject.Cooldown.is_ready(self):
            return
        SceneManager.Scene.remove_object(self.parent)
        return

