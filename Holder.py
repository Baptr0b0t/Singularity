class EventManager:
    """
    Exemple usage :
        Holder.Game.has_event(eventlist.MY_EVENT)
        Holder.Game.post_event(eventlist.MY_EVENT)
    """
    def __init__(self):
        self.events = []  # Stocke les événements récupérés
        self.pygame_events = []
        self.reset()

    def reset(self):
        """Reset tous les événements"""
        self.events.clear()

    def has_event(self, event, do_remove):
        """Check un événement"""
        if event in self.events:
            if do_remove:
                self.events.remove(event)
                print(self.events)
            return True
        return False

    def get_events(self):
        """Retourne la liste des événements """
        return self.events

    def post_event(self, event):
        """Ajoute un nouvel événement manuellement."""
        self.events.append(event)  # Ajoute l'événement à la file
        print(self.events)

class Game:
    LARGEUR, HAUTEUR = 1000, 600
    actual_scene = None
    music_player = None
    sound_player = None
    event_manager = None
    zoom_factor = 1.0
    relative_offset = [0, 0]
    delta_time = 0
    time = 0
    @classmethod
    def get_screen_size(cls):
        return cls.LARGEUR,cls.HAUTEUR

    @classmethod
    def set_actual_scene(cls, value):
        print("Set : ",value)
        cls.actual_scene = value
        if cls.actual_scene is not None:
            cls.actual_scene.boot_up_all()

    #Money
    money = 100

    @classmethod
    def add_money(cls, value):
        cls.money+=value

    @classmethod
    def remove_money(cls, value):
        cls.money-=value

    @classmethod
    def has_money(cls, cost):
        return cls.money - cost >= 0


    @classmethod
    def get_events(cls):
        """Permet aux objets de la scène de récupérer les événements"""
        return cls.event_manager.get_events()

    @classmethod
    def has_event(cls, event, do_remove=True ):
        """Ajoute un nouvel event."""
        return cls.event_manager.has_event(event, do_remove)

    @classmethod
    def post_event(cls, event):
        """Ajoute un nouvel event."""
        return cls.event_manager.post_event(event)