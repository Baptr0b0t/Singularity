import gc
import math

import pygame
import save.save as saving_system
import Gameobject
import SceneManager
import taglist
from component.render import *
from component.movement import *
from component.audio import MusicPlayer, SoundEffectManager
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

Holder.Game.music_player = MusicPlayer()
Holder.Game.event_manager = Holder.EventManager()
Holder.Game.sound_player = SoundEffectManager()

menu_scene = SceneManager.Scene("./scene/menu.yml")
pause_scene = SceneManager.Scene("./scene/pause.yml")
shop_scene = SceneManager.Scene("./scene/shop.yml")

saving_system.init_save_file()
Holder.Game.score = saving_system.get_highest_score()
print("SCORE :", Holder.Game.score)

Holder.Game.set_actual_scene(menu_scene)

# Boucle principale
running = True
while running:
    delta_time = clock.tick(60) / 1000  # Temps écoulé en secondes
    Holder.Game.delta_time = delta_time
    Holder.Game.time += delta_time
    #print("Time :", Holder.Game.time)
    Holder.Game.event_manager.pygame_events = pygame.event.get()
    for event in Holder.Game.event_manager.pygame_events:
        if event.type == pygame.QUIT:
            print("Quit")
            running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_F11]:
        pygame.display.toggle_fullscreen()
        Holder.Game.LARGEUR, Holder.Game.HAUTEUR = pygame.display.get_surface().get_size()
    if keys[pygame.K_ESCAPE]:
        if Holder.Game.actual_scene is space_scene:
            Holder.Game.set_actual_scene(pause_scene)

    if keys[pygame.K_r]:
        if Holder.Game.actual_scene is space_scene:
            Holder.Game.set_actual_scene(shop_scene)

    if Holder.Game.has_event(eventlist.QUIT):
        running = False
    if Holder.Game.has_event(eventlist.SCENE_SPACE):
        space_scene = SceneManager.Scene("./scene/scene1.yml")
        Holder.Game.score = 0
        Holder.Game.set_actual_scene(space_scene)
    if Holder.Game.has_event(eventlist.SCENE_MENU):
        Holder.Game.score = saving_system.get_highest_score()
        Holder.Game.set_actual_scene(menu_scene)
    if Holder.Game.has_event(eventlist.SCENE_TUTORIAL):
        tutorial_scene = SceneManager.Scene("./scene/tutorial.yml")
        Holder.Game.set_actual_scene(tutorial_scene)


    if Holder.Game.has_event(eventlist.GAME_OVER):
        saving_system.new_score(Holder.Game.actual_scene.scene_name, Holder.Game.score)
        Holder.Game.set_actual_scene(menu_scene)


    # Dessin
    fenetre.fill(NOIR)

    sprite_group, front_sprite_group = Holder.Game.actual_scene.update_all()


    #main_sprite_group.update()
    sprite_group.draw(fenetre)
    front_sprite_group.draw(fenetre)


    #appliquer_filtre_8bit(fenetre, Holder.Game.LARGEUR, Holder.Game.HAUTEUR, 1)




    pygame.display.flip()





pygame.quit()