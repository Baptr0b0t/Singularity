import Gameobject
import math
import pygame


class AITarget(Gameobject.Component):
    def __init__(self, parent):
        super().__init__(parent)
        self.target = (500,400)  # Position cible

    def update(self):
        self.target = pygame.mouse.get_pos()
        pass

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

    def __init__(self, parent, acceleration=80, rotation_speed=0.05, min_distance=10, max_distance=80):
        super().__init__(parent)
        self.acceleration = acceleration
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

        # Appliquer l'accélération uniquement si l'angle est bien aligné
        if abs(angle_diff) < math.radians(10):  # Seuil pour éviter les oscillations
            velocity.ax += self.acceleration * math.cos(transform.angle - math.radians(90))
            velocity.ay += self.acceleration * math.sin(transform.angle - math.radians(90))
