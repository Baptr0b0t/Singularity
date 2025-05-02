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
        self.cached_scaled_surfaces = {}  # Cache des images zoomées
        self.visible_off_screen = visible_off_screen

        transform = self.game_object.get_component(Gameobject.Transform)
        self.image = pygame.transform.scale(self.surface, self.scale)
        if use_topleft:
            self.rect = self.image.get_rect(topleft=(transform.x, transform.y))
        else:
            self.rect = self.image.get_rect(center=(transform.x, transform.y))
        self.visible = True


    def get_cached_scaled_surface(self, surface, scale):
        int_scale = (int(scale[0]), int(scale[1]))

        if int_scale not in self.cached_scaled_surfaces:
            self.cached_scaled_surfaces[int_scale] = pygame.transform.scale(surface, int_scale)
        return self.cached_scaled_surfaces[int_scale]

    def reset_cached_scaled_surfaces(self):
        self.cached_scaled_surfaces = {}

    def set_scale(self, scale):
        self.scale = scale

    def set_sprite(self, surface, scale_factor = 1.0):
        self.reset_cached_scaled_surfaces()
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

        self.image = self.get_cached_scaled_surface(self.surface, scale) #self.image = pygame.transform.scale(self.surface, scale)
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
    def __init__(self, parent, font_path = "resources/RobotInvaders.ttf", font_size = 25, texte = "", color = "BLANK", size = 1):
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
        self.middle_button_pressed = False


    def update(self):
        game_object = self.parent
        if game_object.has_tag(PLAYER):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                Holder.Game.zoom_factor = 0.7
                Holder.Game.relative_offset = [0,0]

            for event in Holder.Game.event_manager.pygame_events:
                # Détection du scroll de la souris avec pygame.MOUSEWHEEL
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        Holder.Game.zoom_factor *= 1.03
                    elif event.y < 0:
                        Holder.Game.zoom_factor *= 0.97
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        pygame.mouse.get_rel()  # Réinitialiser le rel
                        self.middle_button_pressed = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        self.middle_button_pressed = False

                if event.type == pygame.MOUSEMOTION:
                    if self.middle_button_pressed:
                        # Mouvement de souris avec molette pressée détecté
                        x, y = event.rel  # Déplacement relatif
                        Holder.Game.relative_offset[0] += 2*x
                        Holder.Game.relative_offset[1] += 2*y
                        MIN_OFFSET_X, MAX_OFFSET_X = -Holder.Game.LARGEUR//2, Holder.Game.LARGEUR//2
                        MIN_OFFSET_Y, MAX_OFFSET_Y = -Holder.Game.HAUTEUR // 2, Holder.Game.HAUTEUR // 2
                        # Mise à jour avec clamp (limitation)
                        Holder.Game.relative_offset[0] = max(MIN_OFFSET_X,
                                                             min(MAX_OFFSET_X, Holder.Game.relative_offset[0] + x))
                        Holder.Game.relative_offset[1] = max(MIN_OFFSET_Y,
                                                             min(MAX_OFFSET_Y, Holder.Game.relative_offset[1] + y))

            Holder.Game.zoom_factor = min(1.5,max(Holder.Game.zoom_factor, 0.1))

        active_scale = Holder.Game.zoom_factor * self.scale_factor_view


        camera_transform = SceneManager.Scene.find_by_tag(taglist.MAIN_CAMERA)[0].get_component(Gameobject.Transform) #not crash proof
        transform = game_object.get_component(Gameobject.Transform)
        newpositionx = (transform.x - camera_transform.x)*active_scale + Holder.Game.LARGEUR//2 + Holder.Game.relative_offset[0]
        newpositiony = (transform.y - camera_transform.y)*active_scale + Holder.Game.HAUTEUR//2 + Holder.Game.relative_offset[1]
        self.position = (newpositionx, newpositiony)

        renderer = game_object.get_component(SpriteRenderer)
        self.scale = (renderer.scale[0] * active_scale, renderer.scale[1] * active_scale) #Modifie la taille pendant les rotations
