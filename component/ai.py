import Gameobject
import math
import pygame
import SceneManager
from random import randint, choice
from taglist import AI_TARGETED, AI_SWARM


class AITarget(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent, cooldown = 0.1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown, start_ready=False)

        self.target = (randint(200,900),randint(200,600))  # Position cible
        self.shooting_target = None
        self.target_obj = None

    def update(self):
        if Gameobject.Cooldown.is_ready(self):

            target_object = SceneManager.Scene.find_by_tag(AI_TARGETED)

            if self.parent in target_object:
                target_object.remove(self.parent) #Don't target himself
            if not len(target_object)>=1:
                return



            target_object = choice(target_object)
            self.target_obj = target_object
            target_transform = target_object.get_component(Gameobject.Transform)
            self.target = (target_transform.x, target_transform.y)
            self.shooting_target = (target_transform.x, target_transform.y)
            Gameobject.Cooldown.reset(self)

class AIMaxSpeed(Gameobject.Component):
    """
    Composant qui limite la vitesse en ajustant l'accélération.
    :param max_speed: Vitesse maximale autorisée
    :param deceleration_force: Force de freinage progressif
    """
    def __init__(self, parent, max_speed=50, deceleration_force=0.1):
        super().__init__(parent)
        self.max_speed = max_speed
        self.deceleration_force = -deceleration_force  # Réduction progressive de l'accélération si trop rapide
        #TODO : add max deceleration_force

    def update(self):
        game_object = self.parent
        velocity = game_object.get_component(Gameobject.Velocity)

        if not velocity:
            return

        # Vérification pour ax
        if abs(velocity.ax) > self.max_speed:
            velocity.ax += self.deceleration_force * velocity.x

        # Vérification pour ay
        if abs(velocity.ay) > self.max_speed:
            velocity.ay += self.deceleration_force * velocity.y


class AITargetMovement(Gameobject.Component):
    """
    Composant AI permettant à un vaisseau de tourner autour d'une cible.

    :param acceleration: Force d'accélération appliquée
    :param rotation_speed: Vitesse de rotation du vaisseau (radians par frame)
    :param min_distance: Distance minimale avant de s'éloigner
    :param max_distance: Distance maximale avant de se rapprocher
    """

    def __init__(self, parent, min_acceleration=20, max_acceleration = 80, rotation_speed=0.05, min_distance=40, max_distance=300):
        super().__init__(parent)
        self.min_acceleration = min_acceleration
        self.max_acceleration = max_acceleration
        self.rotation_speed = rotation_speed
        self.min_distance = min_distance
        self.max_distance = max_distance


    def update(self):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        ai_target = game_object.get_component(AITarget)
        if not transform or not velocity or not ai_target:
            return

        target = ai_target.target
        if target is None:
            return
        target_x, target_y = target
        dx, dy = target_x - transform.x, target_y - transform.y
        distance = math.hypot(dx, dy)  # TODO: REPLACE every distance calcul

        target_angle = math.atan2(dy, dx)

        current_angle = transform.angle - math.radians(90)
        # Déterminer le comportement en fonction de la distance
        if distance < self.min_distance:
            # Trop proche, S'éloigner
            desired_angle = target_angle + math.pi  # Demi-tour
        elif distance > self.max_distance:
            # Trop loin, Se rapprocher
            desired_angle = target_angle
        else:
            # Dans la zone de confort, Orbite
            desired_angle = target_angle + math.radians(90)  # Tourne autour

        # Rotation progressive vers l'angle désiré
        angle_diff = (desired_angle - current_angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) > self.rotation_speed:
            transform.angle += self.rotation_speed * (1 if angle_diff > 0 else -1)

        # Calcul proportionnel de l'accélération entre min_distance et max_distance
        distance_clamped = max(min(distance, self.max_distance), self.min_distance)
        proportion = (distance_clamped - self.min_distance) / (self.max_distance - self.min_distance)
        # Interpolation linéaire entre min et max acceleration
        acceleration = self.min_acceleration + proportion * (self.max_acceleration - self.min_acceleration)

        # Appliquer l'accélération uniquement si l'angle est bien aligné
        if abs(angle_diff) < math.radians(10):  # Seuil pour éviter les oscillations
            velocity.ax += acceleration * math.cos(transform.angle - math.radians(90))
            velocity.ay += acceleration * math.sin(transform.angle - math.radians(90))


class AISwarmBehavior(Gameobject.Component):
    def __init__(self, parent, view_radius=4000, separation_distance=700, max_neighbors=10, rotation_speed=0.05, acceleration=90):
        super().__init__(parent)
        self.view_radius = view_radius
        self.separation_distance = separation_distance
        self.max_neighbors = max_neighbors
        self.rotation_speed = rotation_speed
        self.acceleration = acceleration

    def update(self):
        game_object = self.parent
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if not transform or not velocity:
            return

        # Cherche les voisins dans le champ de vision
        neighbors = []
        for obj in SceneManager.Scene.find_by_tag(AI_SWARM):
            if obj == game_object:
                continue
            other_transform = obj.get_component(Gameobject.Transform)
            if not other_transform:
                continue
            dx = other_transform.x - transform.x
            dy = other_transform.y - transform.y
            dist = math.hypot(dx, dy)
            if dist < self.view_radius:
                neighbors.append((obj, dx, dy, dist))
            if len(neighbors) >= self.max_neighbors:
                break


        if not neighbors:
            return

        # Initialisation des vecteurs de forces
        cohesion_x, cohesion_y = 0, 0
        separation_x, separation_y = 0, 0
        align_x, align_y = 0, 0
        count = len(neighbors)

        for obj, dx, dy, dist in neighbors:
            other_transform = obj.get_component(Gameobject.Transform)
            other_velocity = obj.get_component(Gameobject.Velocity)

            # Cohésion (moyenne des positions)
            cohesion_x += other_transform.x
            cohesion_y += other_transform.y

            # Séparation
            if dist < self.separation_distance:
                separation_x -= dx / (dist + 0.01)
                separation_y -= dy / (dist + 0.01)

            # Alignement
            if other_velocity:
                align_x += other_velocity.x
                align_y += other_velocity.y

        # Moyenne
        cohesion_x = cohesion_x / count - transform.x
        cohesion_y = cohesion_y / count - transform.y
        align_x /= count
        align_y /= count

        # Combine les forces avec des poids
        steer_x = cohesion_x * 0.5 + separation_x * 1.5 + align_x * 1.0
        steer_y = cohesion_y * 0.5 + separation_y * 1.5 + align_y * 1.0

        # Calcule l'angle désiré
        desired_angle = math.atan2(steer_y, steer_x)
        current_angle = transform.angle - math.radians(90)
        angle_diff = (desired_angle - current_angle + math.pi) % (2 * math.pi) - math.pi

        # Tourne vers l’angle désiré (lentement)
        if abs(angle_diff) > self.rotation_speed:
            transform.angle += self.rotation_speed * (1 if angle_diff > 0 else -1)

        # Applique l’accélération vers l’avant si bien orienté
        if abs(angle_diff) < math.radians(10):
            min_d = 30  # trop proche
            max_d = self.view_radius  # trop loin
            distance_to_steering = math.hypot(steer_x, steer_y)
            clamped_distance = max(min(distance_to_steering, max_d), min_d)
            proportion = max((clamped_distance - min_d) / (max_d - min_d), 0)
            acceleration = self.acceleration * proportion
            thrust_x = acceleration * math.cos(transform.angle - math.radians(90))
            thrust_y = acceleration * math.sin(transform.angle - math.radians(90))
            velocity.ax += thrust_x
            velocity.ay += thrust_y
