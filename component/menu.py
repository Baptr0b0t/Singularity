import Gameobject

class Button(Gameobject.Component):
    def __init__(self, parent, event_on_click):
        super().__init__(parent)
        self.event_on_click = event_on_click

