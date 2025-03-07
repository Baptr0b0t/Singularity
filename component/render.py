import pygame

import Gameobject
import math
import taglist
import SceneManager
import Holder
from colorlist import * #used by globals()

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
    def __init__(self, game_object, image_path = missing_texture, scale_factor = 1.0):
        pygame.sprite.Sprite.__init__(self)
        self.game_object = game_object
        self.surface = load_image(image_path)
        self.scale = (self.surface.get_size()[0] * scale_factor,self.surface.get_size()[1] * scale_factor)
        transform = self.game_object.get_component(Gameobject.Transform)
        self.image = pygame.transform.scale(self.surface, self.scale)
        self.rect = self.image.get_rect(center=(transform.x, transform.y))
        self.visible = True


    def set_scale(self, scale):
        self.scale = scale

    def set_sprite(self, surface, scale_factor = 1.0):
        self.surface = surface
        self.scale = (surface.get_size()[0] * scale_factor, surface.get_size()[1] * scale_factor)

    def update(self): #call on pygame.sprite.group.update()
        """Met à jour l'affichage du sprite."""
        if not self.visible:
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
            self.rect.topleft = (0, 0)
            return

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
        self.rect = self.image.get_rect(center=position)

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

        surface_rect = pygame.Surface(self.size)
        surface_rect.fill(color)
        game_object.get_component(SpriteRenderer).set_sprite(surface_rect)



class RelativeCamera(Gameobject.Component):
    """
    :param scale_factor_long_view Warning: Magic Number
    :param scale_factor_short_view Warning: Magic Number #Todo Add at Game Holder
    :param distance factor of distance the sprite simulate
    These param must never be different from other GameObject in same Scene
    """
    def __init__(self, parent, scale_factor_long_view = 0.05,scale_factor_short_view = 1, distance = 1):
        super().__init__(parent)
        self.position = (0,0) #Add x,y property
        #self.active = True
        self.scale = (0,0)
        self.distance = distance
        self.scale_factor_long_view = scale_factor_long_view * (1/distance)
        self.scale_factor_short_view = scale_factor_short_view * (1/distance)

    def update(self):
        game_object = self.parent #TODO : Change to 3 mode of vision and no real coordinate vision
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            active_scale = self.scale_factor_long_view
        else:
            active_scale = self.scale_factor_short_view
        camera_transform = SceneManager.Scene.find_by_tag(taglist.MAIN_CAMERA)[0].get_component(Gameobject.Transform) #not crash proof
        transform = game_object.get_component(Gameobject.Transform)
        newpositionx = (transform.x - camera_transform.x)*active_scale + Holder.Game.LARGEUR//2
        newpositiony = (transform.y - camera_transform.y)*active_scale + Holder.Game.HAUTEUR//2
        self.position = (newpositionx, newpositiony)

        renderer = game_object.get_component(SpriteRenderer)
        self.scale = (renderer.scale[0] * active_scale, renderer.scale[1] * active_scale) #Modifie la taille pendant les rotations
