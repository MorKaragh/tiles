import pygame


class SoundEffects:

    def __init__(self):
        pygame.mixer.init()
        self.touch_snd = pygame.mixer.Sound("../sounds/touch.wav")
        self.puff_snd = pygame.mixer.Sound("../sounds/break.wav")
        self.break_light_snd = pygame.mixer.Sound("../sounds/break-l3.wav")

    def touch(self):
        self.touch_snd.play()

    def break_hard(self):
        self.puff_snd.play()

    def light_break(self):
        self.break_light_snd.play()
