class Game:
    LARGEUR, HAUTEUR = 1000, 600
    actual_scene = None
    delta_time = 0

    @classmethod
    def get_screen_size(cls):
        return cls.LARGEUR,cls.HAUTEUR
