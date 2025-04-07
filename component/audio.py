import pygame
import Gameobject
import Holder
import json



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


class SoundEffectManager:
    def __init__(self, json_file = "./resources/audio/sounds.json"):
        self.sounds = {}
        self.load_sounds_from_json(json_file)

    def load_sounds_from_json(self, json_file):
        with open(json_file, 'r') as file:
            sound_data = json.load(file)
            for name, filepath in sound_data.items():
                self.sounds[name] = pygame.mixer.Sound(filepath)
                print(f"Son {filepath} chargé sous le nom: {name}")

    def load_sound(self, name, filepath):
        self.sounds[name] = pygame.mixer.Sound(filepath)
        print(f"Son chargé : {name}")

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
            print(f"Son joué : {name}")
        else:
            print(f"Son non trouvé : {name}")

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
            print(f"Son arrêté : {name}")


class PlaySound(Gameobject.Component):
    """
    Play sound when activate the scene with the GameObject
    """
    def __init__(self, parent, name = "test"):
        super().__init__(parent)
        self.name = name

    def boot_up(self):
        Holder.Game.sound_player.play_sound(self.name)




