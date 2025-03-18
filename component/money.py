import Holder
import Gameobject
import SceneManager
from taglist import PLAYER
import pygame
import time


class Money(Gameobject.Component):
    def __init__(self, parent, money = 100):
        super().__init__(parent)
        self.money = money

    def add_money(self, value):
        self.money+=value

    def remove_money(self, value):
        self.money-=value

    def has_money(self, cost):
        return self.money - cost >= 0



class Upgrade(Gameobject.Component, Gameobject.Cooldown):
    def __init__(self, parent,  component = Gameobject.Component, value = 10, price = 10, cooldown = 1):
        Gameobject.Component.__init__(self, parent)
        Gameobject.Cooldown.__init__(self, cooldown)
        self.value = value
        self.name_component = component
        self.price = price


    def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] and Gameobject.Cooldown.is_ready(self): #TODO: Use event system with a button
                player_object = SceneManager.Scene.find_by_tag(PLAYER)
                if not player_object and len(player_object)>=1:
                    return
                player_object = player_object[0]
                money = player_object.get_component(Money)
                if not money:
                    return

                if money.has_money(self.price):
                    component = player_object.get_component(SceneManager.resolve_component(self.name_component))
                    component.upgrade(self.value)
                    money.remove_money(self.price)
                    Gameobject.Cooldown.reset(self)
