import Holder
import Gameobject
import SceneManager
from component.render import SpriteRenderer
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

