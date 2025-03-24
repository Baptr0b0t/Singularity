import pygame

import Gameobject
import math
import taglist
import SceneManager
import Holder
from colorlist import * #used by globals()
from taglist import PLAYER

missing_texture = "./resources/missing_texture.jpg"
def load_image(image_path):
    """Charge une image en gérant les erreurs."""
    try:
        return pygame.image.load(image_path)
    except FileNotFoundError:
        return pygame.image.load(missing_texture)



class SpriteRenderer(pygame.sprite.Sprite):
    """
    Composant de rendu de l'objet.
    :param image_path: Path relative de l'image du sprite.
    :param scale_factor: Coefficient de la taille de l'image
    """
    def __init__(self, game_object, image_path = missing_texture, scale_factor = 1.0, use_topleft = False, visible_off_screen = False):
        pygame.sprite.Sprite.__init__(self)
        self.game_object = game_object
        self.surface = load_image(image_path)
        self.scale = (self.surface.get_size()[0] * scale_factor,self.surface.get_size()[1] * scale_factor)
        self.use_topleft = use_topleft
        self.visible_off_screen = visible_off_screen

        transform = self.game_object.get_component(Gameobject.Transform)
        self.image = pygame.transform.scale(self.surface, self.scale)
        if use_topleft:
            self.rect = self.image.get_rect(topleft=(transform.x, transform.y))
        else:
            self.rect = self.image.get_rect(center=(transform.x, transform.y))
        self.visible = True


    def set_scale(self, scale):
        self.scale = scale

    def set_sprite(self, surface, scale_factor = 1.0):
        self.surface = surface
        self.scale = (surface.get_size()[0] * scale_factor, surface.get_size()[1] * scale_factor)

    def is_visible_on_screen(self):
        """Vérifie si le sprite est visible à l'écran."""
        screen_rect = pygame.display.get_surface().get_rect()
        return self.rect.colliderect(screen_rect)

    def update(self): #call on pygame.sprite.group.update()
        """Met à jour l'affichage du sprite."""

        transform = self.game_object.get_component(Gameobject.Transform)
        if not transform:
            return

        angle = -math.degrees(transform.angle)
        relative_camera = self.game_object.get_component(RelativeCamera)

        if relative_camera:
            position, scale = relative_camera.position, relative_camera.scale
        else:
            position, scale = (transform.x, transform.y), self.scale

        self.image = pygame.transform.scale(self.surface, scale)
        self.image = pygame.transform.rotate(self.image, angle)
        if self.use_topleft:
            self.rect = self.image.get_rect(topleft=position)
        else:
            self.rect = self.image.get_rect(center=position)

        if not self.visible_off_screen:
            # Mise à jour de la visibilité en fonction de la position du sprite
            self.visible = self.is_visible_on_screen()

        if not self.visible:
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
            #self.image = pygame.transform.scale(self.surface, (100,100)) #use when want to see what sprite is invisible
            self.rect.topleft = (0, 0)
            return

class FontRenderer(Gameobject.Component):
    def __init__(self, parent, font_path = "resources/SAIBA-45.ttf", font_size = 25, texte = "", color = "BLANK", size = 1):
        super().__init__(parent)
        self.font = pygame.font.Font(font_path, font_size)

        color = globals()[color] #"BLANK" -> (255,255,255) using color list
        self.color = color
        self.change_text(texte, color, size)

    def change_text(self, texte, color = None, size = 1):
        game_object = self.parent
        if color is None:
            color = self.color

        surface_texte = self.font.render(str(texte), False, color)
        game_object.get_component(SpriteRenderer).set_sprite(surface_texte, size)

class RectangleRenderer(Gameobject.Component):
    def __init__(self, parent, color = "BLANK", size = (10,10)):
        super().__init__(parent)

        color = globals()[color] #"BLANK" -> (255,255,255) using color list
        self.color = color
        self.size = size
        self.change_size(color, size)


    def change_size(self, color = None, size = (0,0)):
        game_object = self.parent
        if color is None:
            color = self.color

        surface_rect = pygame.Surface(size)
        surface_rect.fill(color)
        game_object.get_component(SpriteRenderer).set_sprite(surface_rect)



class RelativeCamera(Gameobject.Component):
    """
    :param scale_factor_view factor
    :param distance factor of distance the sprite simulate
    These param must never be different from other GameObject in same Scene
    """
    def __init__(self, parent, scale_factor_view = 1, distance = 1):
        super().__init__(parent)
        self.position = (0,0) #Add x,y property
        self.scale = (0,0)

        self.scale_factor_view = scale_factor_view * (1/distance)


    def update(self):
        game_object = self.parent
        if game_object.has_tag(PLAYER):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                Holder.Game.zoom_factor = 1

            for event in Holder.Game.event_manager.pygame_events:
                # Détection du scroll de la souris avec pygame.MOUSEWHEEL
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        Holder.Game.zoom_factor *= 1.03
                    elif event.y < 0:
                        Holder.Game.zoom_factor *= 0.97

            Holder.Game.zoom_factor = min(1,max(Holder.Game.zoom_factor, 0.1))

        active_scale = Holder.Game.zoom_factor * self.scale_factor_view


        camera_transform = SceneManager.Scene.find_by_tag(taglist.MAIN_CAMERA)[0].get_component(Gameobject.Transform) #not crash proof
        transform = game_object.get_component(Gameobject.Transform)
        newpositionx = (transform.x - camera_transform.x)*active_scale + Holder.Game.LARGEUR//2
        newpositiony = (transform.y - camera_transform.y)*active_scale + Holder.Game.HAUTEUR//2
        self.position = (newpositionx, newpositiony)

        renderer = game_object.get_component(SpriteRenderer)
        self.scale = (renderer.scale[0] * active_scale, renderer.scale[1] * active_scale) #Modifie la taille pendant les rotations
