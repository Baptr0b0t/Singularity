import math

import pygame

import Gameobject
import taglist
from component.render import *
from component.movement import *
import Holder


pygame.init()

# Dimensions de la fenêtre

fenetre = pygame.display.set_mode((Holder.Game.get_screen_size()))
pygame.display.set_caption("Singularity")


# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)


spaceship = pygame.image.load('./resources/spaceship.png')















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

main_sprite_group = pygame.sprite.Group()
clock = pygame.time.Clock()


triangle = Gameobject.GameObject((Holder.Game.LARGEUR//2,Holder.Game.HAUTEUR//2))
triangle.add_tag(taglist.MAIN_CAMERA)
triangle.add_tag(taglist.PLAYER)
triangle.add_self_updated_component(SpriteRenderer(triangle, spaceship, 0.1))
triangle.add_quick_updated_component(Gameobject.Velocity())
triangle.add_component(PlayerSpaceMovement(200))
triangle.add_component(Gravity())
triangle.add_late_updated_component(space_movement())
triangle.add_component(RelativeCamera())
main_sprite_group.add(triangle.get_component(SpriteRenderer))


relativecamtest = Gameobject.GameObject((500, 300))
relativecamtest.add_self_updated_component(SpriteRenderer(relativecamtest, spaceship, 0.1))
relativecamtest.add_component(RelativeCamera())
main_sprite_group.add(relativecamtest.get_component(SpriteRenderer))

FPS_number_object = Gameobject.GameObject((100, 100), math.radians(0))
FPS_number_object.add_self_updated_component(SpriteRenderer(FPS_number_object, spaceship, 0.1))
FPS_number_object.add_component(RelativeCamera())
main_sprite_group.add(FPS_number_object.get_component(SpriteRenderer))


symbolfont = pygame.font.Font("resources/Symbols.ttf", 20)
font = pygame.font.Font("resources/SAIBA-45.ttf", 60)



#pygame.display.toggle_fullscreen()
Holder.Game.LARGEUR, Holder.Game.HAUTEUR = pygame.display.get_surface().get_size()

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


    FPS_number_object.get_component(SpriteRenderer).set_sprite(FPS_number)

    FPS_number_object.update(delta_time)

    main_sprite_group.update()
    main_sprite_group.draw(fenetre)


    appliquer_filtre_8bit(fenetre, Holder.Game.LARGEUR, Holder.Game.HAUTEUR, 1)




    pygame.display.flip()





pygame.quit()