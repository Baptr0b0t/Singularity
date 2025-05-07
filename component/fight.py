import random

import Gameobject
import pygame
from component.health import Health, DestroyOnNoHealth, ScoreOnDestroy
from component.money import LootMoney
from component.render import SpriteRenderer, RelativeCamera
import SceneManager
import math
from component.movement import SpaceMovement, Mass, Gravity
from component.collision import DamageCollision, PlanetCollision
from component.ai import AITarget, AITargetMovement, AIMaxSpeed, AISwarmBehavior
from component.ui import Velocity_Arrow
from taglist import AI_SWARM


class PlayerShot(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, fire_rate = 0.07, speed = 220, bullet_pathfile = "./resources/blast_red.png", scale = 0.12):
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

            bullet.add_standard_component(DamageCollision(bullet, damage_on_other=10, do_delete=True))
            bullet.add_standard_component(BulletLifeTime(bullet, life_time= 10))
            #bullet.add_standard_component(DeleteOnCollision(bullet, screen_limit=False, planet_collision_ratio=0.5 ,seconds_before_start=.26))
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
        self.turret.add_standard_component(Turret_AI(self.turret, game_object))
        SceneManager.Scene.add_object(self.turret, front=True)


    def update(self):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        turret_transform = self.turret.get_component(Gameobject.Transform)


        turret_transform.x = transform.x + self.offset * math.cos(transform.angle-math.radians(90))
        turret_transform.y = transform.y + self.offset * math.sin(transform.angle-math.radians(90))


    def delete(self):
        SceneManager.Scene.remove_object(self.turret)


class Turret_AI(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, spaceship_parent, fire_rate = 0.2, speed = 220, bullet_pathfile = "./resources/blast_red.png", scale = 0.06, rotation_speed = 0.05):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, fire_rate)
        self.speed = speed
        self.space_ship = spaceship_parent
        self.path_file = bullet_pathfile
        self.scale = scale
        self.rotation_speed = rotation_speed

    def move(self, target):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        if target is None:
            return
        target_x, target_y = target
        dx, dy = target_x - transform.x, target_y - transform.y

        target_angle = math.atan2(dy, dx)

        current_angle = transform.angle - math.radians(90)

        # Rotation progressive vers l'angle désiré
        angle_diff = (target_angle - current_angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) > self.rotation_speed:
            transform.angle += self.rotation_speed * (1 if angle_diff > 0 else -1)

    def shoot(self):
        transform = self.parent.get_component(Gameobject.Transform)
        #Creating bullet Gameobject
        bullet = Gameobject.GameObject((transform.x, transform.y), angle=transform.angle)
        bullet.add_self_updated_component(SpriteRenderer(bullet, self.path_file, self.scale))

        if self.space_ship.has_component(RelativeCamera):
            bullet.add_standard_component(RelativeCamera(bullet))
        bullet.add_standard_component(SpaceMovement(bullet))
        bullet.add_quick_updated_component(Gameobject.Velocity(bullet, x= self.speed * math.cos(transform.angle - math.radians(90)), y= self.speed * math.sin(transform.angle - math.radians(90))))
        if self.space_ship.has_component(Gameobject.Velocity):
            game_object_velocity = self.space_ship.get_component(Gameobject.Velocity)
            bullet_velocity = bullet.get_component(Gameobject.Velocity)
            bullet_velocity.x += game_object_velocity.x
            bullet_velocity.y += game_object_velocity.y

        bullet.add_standard_component(DamageCollision(bullet, damage_on_other=10, cooldown=0.30, do_delete=True))
        bullet.add_standard_component(BulletLifeTime(bullet, life_time= 7))
        #bullet.add_standard_component(DeleteOnCollision(bullet, screen_limit=False, planet_collision_ratio=1 ,seconds_before_start=.30))
        SceneManager.Scene.add_object(bullet)

    def update(self):
        target = self.space_ship.get_component(AITarget).shooting_target
        if target is None:
            return
        self.move(target)

        transform = self.parent.get_component(Gameobject.Transform)
        dx, dy = target[0] - transform.x, target[1] - transform.y
        distance = math.hypot(dx, dy)
        if Gameobject.Cooldown.is_ready(self) and distance <= 300:
            self.shoot()
            Gameobject.Cooldown.reset(self)

    def boot_up(self):
        Gameobject.Cooldown.reset(self)


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

class EnemySpawner(Gameobject.Component,Gameobject.Cooldown):
    def __init__(self, parent, time = 10, spawn_radius=10):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, time)
        self.spawn_radius = spawn_radius

    def update(self):
        if not Gameobject.Cooldown.is_ready(self):
            return
        self.spawn_enemy()
        Gameobject.Cooldown.reset(self)
        return

    def spawn_enemy(self):
        transform = self.parent.get_component(Gameobject.Transform)
        angle_rad = random.uniform(0, 2 * math.pi)
        spawn_x = transform.x + self.spawn_radius * math.cos(angle_rad)
        spawn_y = transform.y + self.spawn_radius * math.sin(angle_rad)
        enemy = Gameobject.GameObject((spawn_x, spawn_y), angle=0)
        enemy.add_tag(AI_SWARM)

        # Self updated component
        enemy.add_self_updated_component(SpriteRenderer(enemy, "./resources/enemy_ship_1.png", 0.3))

        # Quick updated component
        enemy.add_quick_updated_component(Gameobject.Velocity(enemy))

        # Standard components
        enemy.add_standard_component(Mass(enemy, mass=1000))
        enemy.add_standard_component(PlanetCollision(enemy, ratio=0.8, restitution=1))
        enemy.add_standard_component(Health(enemy))
        enemy.add_standard_component(DestroyOnNoHealth(enemy))
        enemy.add_standard_component(DamageCollision(enemy, ratio=0.8))
        enemy.add_standard_component(ScoreOnDestroy(enemy, value=10))
        enemy.add_standard_component(LootMoney(enemy))
        #enemy.add_standard_component(AITargetMovement(enemy))
        enemy.add_standard_component(AITarget(enemy))
        enemy.add_standard_component(AISwarmBehavior(enemy))
        enemy.add_standard_component(AIMaxSpeed(enemy))
        enemy.add_standard_component(Gravity(enemy))
        enemy.add_standard_component(RelativeCamera(enemy))

        # Late updated components
        enemy.add_late_updated_component(SpaceMovement(enemy))
        enemy.add_late_updated_component(Velocity_Arrow(enemy))
        enemy.add_late_updated_component(Turret_Holder(enemy))

        # Ajouter à la scène
        SceneManager.Scene.add_object(enemy)