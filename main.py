import pygame
import math
import Gameobject

pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1000, 1000
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Singularity")


# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)


spaceship = pygame.image.load('spaceship.png')

#DELETE SOON
class Renderer(Gameobject.Component):
    def __init__(self, game_object, color, size):
        self.color = color
        self.size = size

    def set_color(self, color):
        self.color = color

    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        if transform:
            x, y = transform.position
            angle = transform.angle
            size = self.size
            #dessine le triangle
            point1 = (x + size * math.cos(angle), y + size * math.sin(angle))
            point2 = (x + size * math.cos(angle + 2 * math.pi / 3), y + size * math.sin(angle + 2 * math.pi / 3))
            point3 = (x + size * math.cos(angle - 2 * math.pi / 3), y + size * math.sin(angle - 2 * math.pi / 3))

            pygame.draw.polygon(fenetre, self.color, [point1, point2, point3])


class sprite_renderer(pygame.sprite.Sprite):

    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.scale = surface.get_size()

    def set_scale(self, scale):
        self.scale = scale

    def update(self, game_object):
        transform = game_object.get_component(Gameobject.Transform)
        if transform:
            angle = math.degrees(transform.angle)+90
            self.image = pygame.transform.scale(self.surface,self.scale)
            self.image = pygame.transform.rotate(self.image, -angle)
            self.rect = self.image.get_rect(center=(transform.position[0], transform.position[1]))




class Movement(Gameobject.Component):
    def __init__(self, acceleration_speed):
        self.deltav = acceleration_speed

    def update(self, game_object, delta_time):
        transform = game_object.get_component(Gameobject.Transform)
        velocity = game_object.get_component(Gameobject.Velocity)
        if transform:
            souris_x, souris_y = pygame.mouse.get_pos()
            transform.angle = math.atan2(souris_y - transform.position[1], souris_x - transform.position[0])


            if velocity:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    velocity.acceleration[0] = self.deltav * math.cos(transform.angle)
                    velocity.acceleration[1] = self.deltav * math.sin(transform.angle)
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
triangle = Gameobject.GameObject((LARGEUR//2, HAUTEUR//2))
#triangle.add_component(Renderer(triangle, ROUGE, 20))
triangle.add_self_updated_component(sprite_renderer(spaceship))
triangle.add_component(Movement(200))
triangle.add_component(Gameobject.Velocity())

spr.add(triangle.get_component(sprite_renderer))


font = pygame.font.Font("Symbols.ttf", 20)
hostile_icon = font.render("|w2q", False, (255, 125, 0))


pygame.display.toggle_fullscreen()
LARGEUR, HAUTEUR = pygame.display.get_surface().get_size()

# Boucle principale
running = True
while running:
    delta_time = clock.tick(60) / 1000  # Temps écoulé en secondes
    print(delta_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour




    # Dessin
    fenetre.fill(NOIR)
    fenetre.blit(hostile_icon, (40, 240))

    triangle.update(delta_time)
    #triangle.get_component(Renderer).update(triangle, delta_time)
    spr.update(triangle)
    spr.draw(fenetre)
    appliquer_filtre_8bit(fenetre, LARGEUR, HAUTEUR, 1)




    pygame.display.flip()





pygame.quit()