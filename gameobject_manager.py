import yaml
import Gameobject
from component import *

class Scene:
    alive_objects = []
    def __init__(self):

        self.scene_objects = []
        return #not done
        with open("scene/scene1.yml", "r") as file:
            scene = yaml.safe_load(file)
        game_objects = scene["game_objects"]
        for game_object in game_objects.values():
            print(game_object)
            obj = Gameobject.GameObject(game_object["position"],game_object["angle"],game_object["tags"])
            print(obj)
            for components in game_object["components"].values():
                print(components)
                for component_name, args in components.items():
                    print(component_name)
                    obj.add_component(component_name(obj, **args))

            Scene.add_object(obj)


    def update_all(self, delta_time):
        for game_object in self.scene_objects:
            game_object.update(delta_time)

    @classmethod
    def add_object(cls, game_object):
        cls.alive_objects.append(game_object)

    @classmethod
    def remove_object(cls, game_object):
        if game_object in cls.alive_objects:
            cls.alive_objects.remove(game_object)

    @classmethod
    def find_by_tag(cls, tag):
        return [obj for obj in cls.alive_objects if obj.has_tag(tag)]

    @classmethod
    def get_all_alive(cls):
        return cls.alive_objects

