import Holder
import Gameobject
import SceneManager
from taglist import PLAYER
import pygame
import time


class Money(Gameobject.Component):
    def __init__(self, parent, money = 0):
        super().__init__(parent)
        self.money = money

    def add_money(self, value):
        self.money+=value

    def remove_money(self, value):
        self.money-=value

    def has_money(self, cost):
        return self.money - cost >= 0



class Upgrade(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent,  component = Gameobject.Component, value = 10, cooldown = 1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.value = value
        self.namecomponent = component


    def update(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and Gameobject.Cooldown.is_ready(self):
            player_object = SceneManager.Scene.find_by_tag(PLAYER)[0]

            self.component = player_object.get_component(SceneManager.resolve_component(self.namecomponent))
            self.component.upgrade(self.value)
            Gameobject.Cooldown.reset(self)
