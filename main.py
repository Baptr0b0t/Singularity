import gc
import math

import pygame

import Gameobject
import SceneManager
import taglist
from component.render import *
from component.movement import *
import Holder
import eventlist

pygame.init()

# Dimensions de la fenêtre

fenetre = pygame.display.set_mode((Holder.Game.get_screen_size()))
pygame.display.set_caption("Singularity")

singularity_icon = pygame.image.load("./resources/icon/windows_logo.png")
pygame.display.set_icon(singularity_icon)


# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)


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


clock = pygame.time.Clock()

#pygame.display.toggle_fullscreen()
Holder.Game.LARGEUR, Holder.Game.HAUTEUR = pygame.display.get_surface().get_size()

menu_scene = SceneManager.Scene("./scene/menu.yml")
space_scene = SceneManager.Scene("./scene/scene1.yml")

Holder.Game.actual_scene = menu_scene
# Boucle principale
running = True
while running:
    delta_time = clock.tick(60) / 1000  # Temps écoulé en secondes
    Holder.Game.delta_time = delta_time
    Holder.Game.time += delta_time
    #print("Time :", Holder.Game.time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit")
            running = False

    if SceneManager.Scene.has_event(eventlist.QUIT):
        running = False


    # Dessin
    fenetre.fill(NOIR)

    sprite_group = Holder.Game.actual_scene.update_all()


    #main_sprite_group.update()
    sprite_group.draw(fenetre)


    #appliquer_filtre_8bit(fenetre, Holder.Game.LARGEUR, Holder.Game.HAUTEUR, 1)




    pygame.display.flip()





pygame.quit()