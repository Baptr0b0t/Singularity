import math

import yaml

from component.render import *
from component.movement import *
from component.ai import *
from component.collision import *
from component.ui import *
from component.fight import *
from component.money import *
from component.audio import *
from component.health import *
from component.menu import *
from Gameobject import *
from taglist import *
from eventlist import *
import Holder
import pygame

def resolve_tag(tag_name):
    return globals()[tag_name]

def resolve_event(event_name):
    return globals()[event_name]

def resolve_component(comp_name):
    return globals()[comp_name]



class Scene:
    alive_objects = []
    tag_memory = {}
    component_memory = {}
    def __init__(self, scene_path_file):
        self.sprite_group = pygame.sprite.Group()
        self.front_sprite_group = pygame.sprite.Group()
        self.scene_objects = []
        Holder.Game.actual_scene = self #Une scene cree est automatiquement la scene active
        LARGEUR = Holder.Game.LARGEUR #used at eval()
        HAUTEUR = Holder.Game.HAUTEUR
        with open(scene_path_file, "r") as file:
            scene = yaml.safe_load(file)
        print(scene)

        for name, data in scene["game_objects"].items():
            position = (eval(str(data["position"][0])),eval(str(data["position"][1]))) #Transforme "LARGEUR" et "HAUTEUR"
            print(position)
            obj = Gameobject.GameObject(position, math.radians(data["angle"]))

            # Ajout des tags
            for tag in data["tags"]:
                if tag in globals():  # Vérifie si le tag existe dans les imports
                    obj.add_tag(resolve_tag(tag))

            for update_type, components in data["components"].items():
                for comp_name, args in components.items():
                    if comp_name in globals():  # Vérifie si la classe existe
                        component_instance = resolve_component(comp_name)(obj, **args)  # Instancie avec arguments
                        getattr(obj, f"add_{update_type}_component")(component_instance)
                    else:
                        print("Composant introuvable :", comp_name)


            Scene.add_object(obj, front= data["front_layer"])

    def boot_up_all(self):
        for game_object in self.scene_objects:
            game_object.boot_up()

    def update_all(self):
        Scene.reset_memory()
        for game_object in self.scene_objects:
            game_object.update()
        self.sprite_group.update()
        self.front_sprite_group.update()
        #self.event_manager.reset() # Reset les événements
        return self.sprite_group, self.front_sprite_group

    @classmethod
    def add_object(cls, game_object, front = False):
        if game_object.has_component(SpriteRenderer):
            if front:
                Holder.Game.actual_scene.front_sprite_group.add(game_object.get_component(SpriteRenderer))
            else:
                Holder.Game.actual_scene.sprite_group.add(game_object.get_component(SpriteRenderer))

        Holder.Game.actual_scene.scene_objects.append(game_object)
        cls.alive_objects.append(game_object)
        #print(cls.alive_objects)

    @classmethod
    def remove_object(cls, game_object):
        #TODO: Use queue list
        Holder.Game.actual_scene.sprite_group.remove(game_object.get_component(SpriteRenderer))
        Holder.Game.actual_scene.front_sprite_group.remove(game_object.get_component(SpriteRenderer))

        if game_object in Holder.Game.actual_scene.scene_objects:
            Holder.Game.actual_scene.scene_objects.remove(game_object)

        if game_object in cls.alive_objects:
            cls.alive_objects.remove(game_object)
        game_object.delete()
        gc.collect()


    @classmethod
    def reset_memory(cls):
        """
        Reset saved result by find_by_tag and find_by_component
        """
        cls.tag_memory = {}
        cls.component_memory = {}

    @classmethod
    def find_by_tag(cls, tag, search_active_scene = True):
        key = (tag, search_active_scene)

        if key in cls.tag_memory:
            return cls.tag_memory[key][:]

        if search_active_scene:
            result = [obj for obj in Holder.Game.actual_scene.scene_objects if obj.has_tag(tag)]
        else:
            result = [obj for obj in cls.alive_objects if obj.has_tag(tag)]

        cls.tag_memory[key] = result
        return result[:] #Renvoie une copie de la liste

    @classmethod
    def find_by_component(cls, component, search_active_scene = True):
        key = (component, search_active_scene)

        if key in cls.component_memory:
            return cls.component_memory[key]

        if search_active_scene:
            result = [obj for obj in Holder.Game.actual_scene.scene_objects if obj.has_component(component)]
        else:
            result = [obj for obj in cls.alive_objects if obj.has_component(component)]

        cls.component_memory[key] = result
        return result[:]

    @classmethod
    def get_all_alive(cls):
        return cls.alive_objects[:]

