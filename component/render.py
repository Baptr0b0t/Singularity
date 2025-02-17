import pygame

import Gameobject
import math
import taglist
import SceneManager
import Holder



missing_texture = "./resources/missing_texture.jpg"

class SpriteRenderer(pygame.sprite.Sprite):
    """
    Composant de rendu de l'objet.
    :param image_path: Path relative de l'image du sprite.
    :param scale_factor: Coefficient de la taille de l'image
    """
    def __init__(self, game_object, image_path = missing_texture, scale_factor = 1.0):
        pygame.sprite.Sprite.__init__(self)
        self.game_object = game_object
        try:
            self.surface = pygame.image.load(image_path)
        except FileNotFoundError:
            self.surface = pygame.image.load(missing_texture)
        self.scale = (self.surface.get_size()[0] * scale_factor,self.surface.get_size()[1] * scale_factor)
        transform = self.game_object.get_component(Gameobject.Transform)
        self.image = pygame.transform.scale(self.surface, self.scale)
        self.rect = self.image.get_rect(center=(transform.position[0], transform.position[1]))


    def set_scale(self, scale):
        self.scale = scale

    def set_sprite(self, surface, scale_factor = 1.0):
        self.surface = surface
        self.scale = (surface.get_size()[0] * scale_factor, surface.get_size()[1] * scale_factor)

    def update(self): #call on pygame.sprite.group.update()

        transform = self.game_object.get_component(Gameobject.Transform)
        if transform:
            angle = math.degrees(transform.angle)
            relative_camera = self.game_object.get_component(RelativeCamera)

            if relative_camera and relative_camera.active: #Need Clean up
                self.image = pygame.transform.scale(self.surface, relative_camera.scale)
                self.image = pygame.transform.rotate(self.image, -angle)
                self.rect = self.image.get_rect(center=(relative_camera.position[0], relative_camera.position[1]))
            else:
                self.image = pygame.transform.scale(self.surface, self.scale)
                self.image = pygame.transform.rotate(self.image, -angle)
                self.rect = self.image.get_rect(center=(transform.position[0], transform.position[1]))



class RelativeCamera(Gameobject.Component):
    def __init__(self, parent, scale_factor = 4):
        super().__init__(parent)
        self.position = (0,0)
        self.active = False
        self.scale = (0,0)
        self.scale_factor = scale_factor

    def update(self):
        game_object = super().parent
        camera_position = SceneManager.Scene.find_by_tag(taglist.MAIN_CAMERA)[0].get_component(Gameobject.Transform).position #not crash proof
        transform = game_object.get_component(Gameobject.Transform)
        newpositionx = (transform.position[0] - camera_position[0])*self.scale_factor + Holder.Game.LARGEUR//2
        newpositiony = (transform.position[1] - camera_position[1])*self.scale_factor + Holder.Game.HAUTEUR//2
        self.position = (newpositionx, newpositiony)

        renderer = game_object.get_component(SpriteRenderer)

        self.scale = (renderer.scale[0] * self.scale_factor, renderer.scale[1] * self.scale_factor) #Modifie la taille pendant les rotations
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            self.active = False
        else:
            self.active = True