class Game:
    LARGEUR, HAUTEUR = 1000, 600
    actual_scene = None

    @classmethod
    def get_screen_size(cls):
        return cls.LARGEUR,cls.HAUTEUR
