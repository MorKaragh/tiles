import pygame
from animation import AnimatorFactory
from typing import Tuple
from pygame import Surface
from utils import load_img


class ScoreBoard:

    def __init__(self,
                 size: Tuple[int, int],
                 coords: Tuple[int, int],
                 animations: AnimatorFactory):
        self.body = Surface(size)
        self.coords = coords
        # self.frame = animations.get_gold_frame_amin(size[0])
        self.frame = load_img(
            "images/frame/glow_frame_ylw.png", (size[0], size[0]))

    def draw(self, screen: Surface):
        self.body.fill("Black")
        # self.body.blit(self.frame.next_frame(), (0, 0))
        self.body.blit(self.frame, (0, 0))
        screen.blit(self.body, self.coords)
