import Holder
import Gameobject
import SceneManager
from component.render import SpriteRenderer, RelativeCamera
from component.collision import DeleteOnCollision
from taglist import PLAYER
import eventlist
import pygame
import time


class PlayerUpgradeEventListener(Gameobject.Component):
    """
    Event Receiver that upgrades specified Gameobject components when corresponding events occur.

    `event_map` should be a dictionary: {event_name: component_class}
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.event_map = {"BOUGHT_FUEL_UPGRADE":("Fuel",1000),"BOUGHT_HEALTH_UPGRADE":("Health", 10)} # Dict[str, Component]

    def update(self):
        game_object = self.parent

        for event_name, component_cls in self.event_map.items():
            resolved_event = SceneManager.resolve_event(event_name)
            if Holder.Game.has_event(resolved_event):
                print(f"Event triggered: {resolved_event}")

                resolved_component = SceneManager.resolve_component(component_cls[0])
                component = game_object.get_component(resolved_component)

                if component:
                    component.upgrade(component_cls[1])
                else:
                    print(f"Component {resolved_component} not found on {game_object}")


class LootMoney(Gameobject.Component):
    def __init__(self, parent, money_pathfile = "./resources/credit.png", value = 15):
        super().__init__(parent)
        self.money_pathfile = money_pathfile
        self.value = value

    def delete(self):
        transform = self.parent.get_component(Gameobject.Transform)
        #Creating bullet Gameobject
        money = Gameobject.GameObject((transform.x, transform.y), angle=transform.angle)
        money.add_self_updated_component(SpriteRenderer(money, self.money_pathfile, 0.5))

        if self.parent.has_component(RelativeCamera):
            money.add_standard_component(RelativeCamera(money))

        money.add_standard_component(DeleteOnCollision(money, planet_collision_ratio= 0.5, reward_money=self.value, tag_filter = PLAYER))
        SceneManager.Scene.add_object(money)
        Holder.Game.Enemy_killed =+ 1
