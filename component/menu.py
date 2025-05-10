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
        self.was_pressed_last_frame = False  # Pour éviter les clics multiples en restant appuyé

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.parent.get_component(SpriteRenderer).rect.collidepoint(mouse_pos):
            if mouse_pressed[0] and not self.was_pressed_last_frame:
                self.was_pressed_last_frame = True
                return True
        if not mouse_pressed[0]:
            self.was_pressed_last_frame = False
        return False

    def update(self):
        if self.is_clicked():
            print("posting :", "eventlist."+self.event_on_click, eval("eventlist."+self.event_on_click))
            Holder.Game.post_event(SceneManager.resolve_event(self.event_on_click))

class Button_with_cost(Button):
    def __init__(self, parent, event_on_click, cost = 10):
        super().__init__(parent, event_on_click)
        self.cost = cost

    def update(self):
        game_holder = Holder.Game
        if self.is_clicked():
            if game_holder.has_money(self.cost):
                game_holder.remove_money(self.cost)

                Holder.Game.post_event(SceneManager.resolve_event(self.event_on_click))
                Holder.Game.sound_player.play_sound(f"purchase")
            else:
                Holder.Game.sound_player.play_sound(f"no_money")



class Grow_on_Hover(Gameobject.Component):
    """
    :param cost How much to have in plaer bank for grow on hober
    """
    def __init__(self, parent, factor = 1.2, cost = 0):
        super().__init__(parent)
        self.factor = factor
        self.is_grown = False
        self.cost = cost

    def update(self):
        money = Holder.Game.money
        mouse_pos = pygame.mouse.get_pos()

        renderer = self.parent.get_component(SpriteRenderer)
        if renderer.rect.collidepoint(mouse_pos) and not money < self.cost:
            if not self.is_grown:
                renderer.set_scale((renderer.scale[0] * self.factor, renderer.scale[1] * self.factor))
                self.is_grown = True
        else:
            if self.is_grown:
                renderer.set_scale((renderer.scale[0] * (1/self.factor), renderer.scale[1] * (1/self.factor)))
                self.is_grown = False

class Score_for_Visible(Gameobject.Component):
    def __init__(self, parent, score_needed = 10):
        super().__init__(parent)
        self.score_needed = score_needed

    def boot_up(self):
        game_holder = Holder.Game
        if game_holder.score>=self.score_needed:
            self.parent.get_component(SpriteRenderer).force_hide = False
        else:
            self.parent.get_component(SpriteRenderer).force_hide = True