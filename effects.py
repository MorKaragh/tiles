import pygame


class SoundEffects:

    def __init__(self):
        pygame.mixer.init()
        self.touch_snd = pygame.mixer.Sound("sounds/touch.wav")
        self.puff_snd = pygame.mixer.Sound("sounds/puff.wav")

    def touch(self):
        self.touch_snd.play()

    def puff(self):
        self.puff_snd.play()
