import Holder
import Gameobject
import SceneManager
from component.render import SpriteRenderer, RelativeCamera
from component.collision import DeleteOnCollision
from taglist import PLAYER
import eventlist
import pygame
import time





class Upgrade_Event(Gameobject.Component):
    """
    Event Receiver who upgrade his Gameobject component.
    """
    def __init__(self, parent, event_name, component = Gameobject.Component, upgrade_value = 10):
        Gameobject.Component.__init__(self, parent)
        self.name_component = component
        self.event_name = event_name
        self.value = upgrade_value

    def update(self):

        if Holder.Game.has_event(SceneManager.resolve_event(self.event_name)):
            print(SceneManager.resolve_event(self.event_name))

            game_object = self.parent

            component = game_object.get_component(SceneManager.resolve_component(self.name_component))
            component.upgrade(self.value)

class LootMoney(Gameobject.Component):
    def __init__(self, parent, money_pathfile = "./resources/credit.png", value = 15):
        super().__init__(parent)
        self.money_pathfile = money_pathfile
        self.value = value

    def delete(self):
        print("Loot Money")
        transform = self.parent.get_component(Gameobject.Transform)
        #Creating bullet Gameobject
        money = Gameobject.GameObject((transform.x, transform.y), angle=transform.angle)
        money.add_self_updated_component(SpriteRenderer(money, self.money_pathfile, 0.5))

        if self.parent.has_component(RelativeCamera):
            money.add_standard_component(RelativeCamera(money))

        money.add_standard_component(DeleteOnCollision(money, planet_collision_ratio= 0.5, reward_money=self.value, tag_filter = PLAYER))

        SceneManager.Scene.add_object(money)
