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
import Holder
import pygame

def resolve_component(comp_name):
    return globals()[comp_name]

class EventManager:
    """
    Exemple usage :
        SceneManager.Scene.has_event(eventlist.MY_EVENT)
        SceneManager.Scene.post_event(eventlist.MY_EVENT)
    """
    def __init__(self):
        self.events = []  # Stocke les événements récupérés
        self.reset()

    def reset(self):
        """Reset tous les événements"""
        self.events.clear()

    def has_event(self, event, do_remove):
        """Check un événement"""
        if event in self.events:
            if do_remove:
                self.events.remove(event)
            return True
        return False

    def get_events(self):
        """Retourne la liste des événements """
        return self.events

    def post_event(self, event):
        """Ajoute un nouvel événement manuellement."""
        self.events.append(event)  # Ajoute l'événement à la file


class Scene:
    alive_objects = []
    def __init__(self, scene_path_file):
        self.sprite_group = pygame.sprite.Group()
        self.scene_objects = []
        self.event_manager = EventManager()
        Holder.Game.actual_scene = self #Une scene cree est automatiquement la scene active
        LARGEUR = Holder.Game.LARGEUR
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
                    obj.add_tag(globals()[tag])

            for update_type, components in data["components"].items():
                for comp_name, args in components.items():
                    if comp_name in globals():  # Vérifie si la classe existe
                        component_instance = resolve_component(comp_name)(obj, **args)  # Instancie avec arguments
                        getattr(obj, f"add_{update_type}_component")(component_instance)
                    else:
                        print("Composant introuvable :", comp_name)

            Scene.add_object(obj)

    def boot_up_all(self):
        for game_object in self.scene_objects:
            game_object.boot_up()

    def update_all(self):

        for game_object in self.scene_objects:
            game_object.update()
        self.sprite_group.update()
        #self.event_manager.reset() # Reset les événements
        return self.sprite_group

    @classmethod
    def get_events(cls):
        """Permet aux objets de la scène de récupérer les événements"""
        return Holder.Game.actual_scene.event_manager.get_events()

    @classmethod
    def has_event(cls, event, do_remove=True ):
        """Ajoute un nouvel event."""
        return Holder.Game.actual_scene.event_manager.has_event(event, do_remove)

    @classmethod
    def post_event(cls, event):
        """Ajoute un nouvel event."""
        return Holder.Game.actual_scene.event_manager.post_event(event)

    @classmethod
    def add_object(cls, game_object):

        Holder.Game.actual_scene.sprite_group.add(game_object.get_component(SpriteRenderer))
        Holder.Game.actual_scene.scene_objects.append(game_object)
        cls.alive_objects.append(game_object)
        print(cls.alive_objects)

    @classmethod
    def remove_object(cls, game_object):
        #TODO: Use queue list
        Holder.Game.actual_scene.sprite_group.remove(game_object.get_component(SpriteRenderer))
        Holder.Game.actual_scene.scene_objects.remove(game_object)
        if game_object in cls.alive_objects:
            cls.alive_objects.remove(game_object)
        game_object.delete()

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

