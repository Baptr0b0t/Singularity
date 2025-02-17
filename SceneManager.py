import yaml

from component.render import *
from component.movement import *
from component.ai import *
from Gameobject import *
from taglist import *
import Holder
import pygame

class Scene:
    alive_objects = []
    def __init__(self):
        self.sprite_group = pygame.sprite.Group()
        self.scene_objects = []
        with open("scene/scene1.yml", "r") as file:
            scene = yaml.safe_load(file)
        LARGEUR = Holder.Game.LARGEUR
        HAUTEUR = Holder.Game.HAUTEUR
        print(scene)
        for name, data in scene["game_objects"].items():
            position = (eval(data["position"][0]),eval(data["position"][1])) #Transforme "LARGEUR" et "HAUTEUR"
            print(position)
            obj = Gameobject.GameObject(position, data["angle"])

            # Ajout des tags
            for tag in data["tags"]:
                if tag in globals():  # Vérifie si le tag existe dans les imports
                    obj.add_tag(globals()[tag])

            for update_type, components in data["components"].items():
                for comp_name, args in components.items():
                    if comp_name in globals():  # Vérifie si la classe existe
                        component_instance = globals()[comp_name](obj, **args)  # Instancie avec arguments
                        getattr(obj, f"add_{update_type}_component")(component_instance)
                    else:
                        print("Composant introuvable :", comp_name)

            self.sprite_group.add(obj.get_component(SpriteRenderer))
            self.scene_objects.append(obj)
            Scene.add_object(obj)


    def update_all(self):
        for game_object in self.scene_objects:
            game_object.update()
        self.sprite_group.update()
        return self.sprite_group

    @classmethod
    def add_object(cls, game_object):
        cls.alive_objects.append(game_object)
        print(cls.alive_objects)

    @classmethod
    def remove_object(cls, game_object):
        if game_object in cls.alive_objects:
            cls.alive_objects.remove(game_object)

    @classmethod
    def find_by_tag(cls, tag, search_active_scene = True):
        if search_active_scene:
            return [obj for obj in Holder.Game.actual_scene.scene_objects if obj.has_tag(tag)]
        else:
            return [obj for obj in cls.alive_objects if obj.has_tag(tag)]

    @classmethod
    def find_by_component(cls, component, search_active_scene = True):
        if search_active_scene:
            return [obj for obj in Holder.Game.actual_scene.scene_objects if obj.has_component(component)]
        else:
            return [obj for obj in cls.alive_objects if obj.has_component(component)]

    @classmethod
    def get_all_alive(cls):
        return cls.alive_objects

