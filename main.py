import pygame
import math
import Gameobject
import taglist
import gameobject_manager as gm


pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1000, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Singularity")


# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)


spaceship = pygame.image.load('spaceship.png')


class sprite_renderer(pygame.sprite.Sprite):

    def __init__(self, game_object, surface = spaceship, scale_factor = 1.0):
        pygame.sprite.Sprite.__init__(self)
        self.game_object = game_object
        self.surface = surface
        self.scale = (surface.get_size()[0] * scale_factor,surface.get_size()[1] * scale_factor)


    def set_scale(self, scale):
        self.scale = scale

    def set_sprite(self, surface, scale_factor = 1.0):
        self.surface = surface
        self.scale = (surface.get_size()[0] * scale_factor, surface.get_size()[1] * scale_factor)

    def update(self): #call on pygame.sprite.group.update()

        transform = self.game_object.get_component(Gameobject.Transform)
        if transform:
            angle = math.degrees(transform.angle)


            relativecamera = self.game_object.get_component(relative_camera)

            if relativecamera and relativecamera.active: #Need Clean up
                self.image = pygame.transform.scale(self.surface, relativecamera.scale)
                self.image = pygame.transform.rotate(self.image, -angle)
                self.rect = self.image.get_rect(center=(relativecamera.position[0], relativecamera.position[1]))
            else:
                self.image = pygame.transform.scale(self.surface, self.scale)
                self.image = pygame.transform.rotate(self.image, -angle)
                self.rect = self.image.get_rect(center=(transform.position[0], transform.position[1]))


class relative_camera(Gameobject.Component):
    def __init__(self, scale_factor = 8):
        self.position = (0,0)
        self.active = False
        self.scale = (0,0)
        self.scale_factor = scale_factor

    def update(self, game_object, delta_time):
        """
        Must be launched before the gameobject spriterenderer
        """
        camera_position = gm.Gameobjectmanager.find_by_tag(taglist.main_camera)[0].get_component(Gameobject.Transform).position #not crash proof
        transform = game_object.get_component(Gameobject.Transform)
        newpositionx = (transform.position[0] - camera_position[0])*self.scale_factor + LARGEUR//2
        newpositiony = (transform.position[1] - camera_position[1])*self.scale_factor + HAUTEUR//2
        self.position = (newpositionx, newpositiony)

        renderer = game_object.get_component(sprite_renderer)

        self.scale = (renderer.scale[0] * self.scale_factor, renderer.scale[1] * self.scale_factor) #Modifie la taille pendant les rotations
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            self.active = False
        else:
            self.active = True



class Movement(Gameobject.Component):
    def __init__(self, acceleration_speed):
        self.deltav = acceleration_speed

    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform:
            souris_x, souris_y = pygame.mouse.get_pos()
            relativecamera = game_object.get_component(relative_camera)
            if relativecamera and relativecamera.active:
                transform.angle = math.atan2(souris_y - relativecamera.position[1], souris_x - relativecamera.position[0]) + math.radians(90)
            else:
                transform.angle = math.atan2(souris_y - transform.position[1], souris_x - transform.position[0]) + math.radians(90)

            if velocity:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    velocity.acceleration[0] = self.deltav * math.cos(transform.angle - math.radians(90))
                    velocity.acceleration[1] = self.deltav * math.sin(transform.angle - math.radians(90))
                else:
                    velocity.acceleration[0] = 0
                    velocity.acceleration[1] = 0

                velocity.velocity[0] += velocity.acceleration[0] * delta_time
                velocity.velocity[1] += velocity.acceleration[1] * delta_time


                transform.position[0] += velocity.velocity[0] * delta_time
                transform.position[1] += velocity.velocity[1] * delta_time

            # Limites de l'écran
            transform.position[0] = max(0, min(LARGEUR, transform.position[0]))
            transform.position[1] = max(0, min(HAUTEUR, transform.position[1]))





def appliquer_filtre_8bit(surface, largeur, hauteur, facteur):
    """
    Applique un effet 8-bit en réduisant la résolution de l'affichage.
    :param surface: La surface d'origine (pygame.display ou autre surface).
    :param largeur: La largeur de la surface d'origine.
    :param hauteur: La hauteur de la surface d'origine.
    :param facteur: Facteur de réduction (plus le facteur est élevé, plus l'effet est pixelisé).
    """
    # Calcul de la taille réduite
    largeur_reduite = largeur // facteur
    hauteur_reduite = hauteur // facteur

    # Crée une surface réduite
    surface_reduite = pygame.Surface((largeur_reduite, hauteur_reduite))

    # Redimensionne l'affichage actuel sur la surface réduite
    pygame.transform.scale(surface, (largeur_reduite, hauteur_reduite), surface_reduite)

    # Reprojette la surface réduite sur l'affichage principal en la redimensionnant
    pygame.transform.scale(surface_reduite, (largeur, hauteur), surface)

spr = pygame.sprite.Group()

clock = pygame.time.Clock()
triangle = Gameobject.GameObject((LARGEUR//2, HAUTEUR//2), tag=taglist.main_camera)
triangle.add_self_updated_component(sprite_renderer(triangle,spaceship, 0.1))
triangle.add_component(Movement(200))
triangle.add_component(Gameobject.Velocity())
triangle.add_component(relative_camera())
spr.add(triangle.get_component(sprite_renderer))


relativecamtest = Gameobject.GameObject((LARGEUR//2, HAUTEUR//2))
relativecamtest.add_self_updated_component(sprite_renderer(relativecamtest,spaceship, 0.1))
relativecamtest.add_component(relative_camera())
spr.add(relativecamtest.get_component(sprite_renderer))

FPS_number_object = Gameobject.GameObject((LARGEUR // 10, HAUTEUR // 10), math.radians(0))
FPS_number_object.add_self_updated_component(sprite_renderer(FPS_number_object,spaceship, 0.1))
FPS_number_object.add_component(relative_camera())
spr.add(FPS_number_object.get_component(sprite_renderer))


symbolfont = pygame.font.Font("Symbols.ttf", 20)
font = pygame.font.Font("SAIBA-45.ttf", 60)



#pygame.display.toggle_fullscreen()
LARGEUR, HAUTEUR = pygame.display.get_surface().get_size()

# Boucle principale
running = True
while running:
    delta_time = clock.tick(60) / 1000  # Temps écoulé en secondes

    print(1/delta_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour
    FPS_number = symbolfont.render(str(int(clock.get_fps())), False, (255, 125, 0))
    #FPS_number = font.render(str(int(math.degrees(triangle.get_component(Gameobject.Transform).angle))), False, (255, 125, 0))


    # Dessin
    fenetre.fill(NOIR)

    triangle.update(delta_time)
    relativecamtest.update(delta_time)

    FPS_number_object.get_component(sprite_renderer).set_sprite(FPS_number)

    FPS_number_object.update(delta_time)

    spr.update()
    spr.draw(fenetre)


    appliquer_filtre_8bit(fenetre, LARGEUR, HAUTEUR, 1)




    pygame.display.flip()





pygame.quit()