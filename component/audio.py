import pygame
import Gameobject
import Holder




class MusicPlayer:
    def __init__(self):
        # Initialise le mixer audio
        pygame.mixer.init()
        self.current_music = None
        self.is_paused = False

    def play_music(self, music_file, loops=-1):
        if self.current_music != music_file: #Music playing
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(loops)
            self.current_music = music_file
            self.is_paused = False
        elif self.is_paused: #Music unpaused
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pass #Music is playing

    def pause_music(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def unpause_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
        self.is_paused = False
        print("Musique arrêtée.")

class PlayMusic(Gameobject.Component):
    """
    Play or unpause music when activate the scene with the GameObject
    """
    def __init__(self, parent, filename = ""):
        super().__init__(parent)
        self.filename = filename

    def boot_up(self):
        Holder.Game.music_player.play_music(self.filename)



class PauseMusic(Gameobject.Component):
    """
    Pause music when activate the scene with the GameObject
    """
    def __init__(self, parent):
        super().__init__(parent)

    def boot_up(self):
        Holder.Game.music_player.pause_music()



