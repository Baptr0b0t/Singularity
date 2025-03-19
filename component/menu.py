import Gameobject
import pygame
from component.render import SpriteRenderer
import SceneManager
import eventlist
import Holder


class Button(Gameobject.Component):
    def __init__(self, parent, event_on_click):
        super().__init__(parent)
        self.event_on_click = event_on_click

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Vérifie si la souris est sur l'objet
        if self.parent.get_component(SpriteRenderer).rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                print("posting :", "eventlist."+self.event_on_click, eval("eventlist."+self.event_on_click))
                SceneManager.Scene.post_event(eval(str("eventlist."+self.event_on_click)))

class Button_with_cost(Gameobject.Component):
    def __init__(self, parent, event_on_click, cost = 10):
        super().__init__(parent)
        self.event_on_click = event_on_click
        self.cost = cost

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Vérifie si la souris est sur l'objet
        if self.parent.get_component(SpriteRenderer).rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:

                game_holder = Holder.Game
                if game_holder.has_money(self.cost):
                    print("posting :", "eventlist."+self.event_on_click, eval("eventlist."+self.event_on_click))
                    SceneManager.Scene.post_event(eval(str("eventlist."+self.event_on_click)))
                    game_holder.remove_money(self.cost)



class Grow_on_Hover(Gameobject.Component):
    def __init__(self, parent, factor = 1.2):
        super().__init__(parent)
        self.factor = factor
        self.is_grown = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        renderer = self.parent.get_component(SpriteRenderer)
        if renderer.rect.collidepoint(mouse_pos):
            if not self.is_grown:
                renderer.set_scale((renderer.scale[0] * self.factor, renderer.scale[1] * self.factor))
                self.is_grown = True
        else:
            if self.is_grown:
                renderer.set_scale((renderer.scale[0] * (1/self.factor), renderer.scale[1] * (1/self.factor)))
                self.is_grown = False

