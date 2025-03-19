class Game:
    LARGEUR, HAUTEUR = 1000, 600
    actual_scene = None
    music_player = None
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
