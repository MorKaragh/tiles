import pygame
from animation import AnimatorFactory
from config import GameConfig
from figures import TetrisFigure
from pygame import Surface, font
from utils import load_img


class ScoreBoard:

    def __init__(self,
                 config: GameConfig,
                 animations: AnimatorFactory,
                 ):
        self.config = config
        self.size = self.config.get_scoreboard_size()
        self.coords = (self.config.GRID_COLS * self.config.SQUARE_SIZE, 0)
        self.body = Surface(self.size)
        self.coords = self.coords
        # self.frame = animations.get_gold_frame_amin(size[0])
        self.frame = load_img(
            "images/frame/glow_frame_blu.png", (self.size[0], self.size[0]))
        self.sample = Surface((self.config.SQUARE_SIZE * 4,
                               self.config.SQUARE_SIZE * 4))
        self.score_area = Surface((self.config.SQUARE_SIZE * 4,
                                   self.config.SQUARE_SIZE * 4))
        self.score_font = font.Font("fonts/Dimkin Regular.ttf", 40)
        self.score = 0

    def reset(self):
        self.score = 0

    def draw(self, screen: Surface):
        self.body.fill("Black")
        self.score_area.fill("Black")
        self.sample.fill("Black")
        for s in self.next_figure.squares:
            s.draw(self.sample)
        self.body.blit(self.sample, (25, 25))
        pygame.draw.line(self.body, (5, 17, 22), (0, 0), (0, self.size[1]), 5)
        self.draw_score()
        self.body.blit(self.score_area, (25, 525))
        screen.blit(self.body, self.coords)

    def draw_score(self):
        text = self.score_font.render(str(self.score), True, (255, 254, 60))
        rect = text.get_rect(
            center=(self.score_area.get_rect().size[0]/2,
                    self.score_area.get_rect().size[1]/2))
        self.score_area.blit(text, rect)

    def set_next_figure(self, figure: TetrisFigure):
        self.next_figure = figure
        self._set_next_fiture_to_sample_center(self.next_figure)

    def _set_next_fiture_to_sample_center(self, figure: TetrisFigure):
        x_space = max(s.x for s in self.next_figure.squares) + \
            self.config.SQUARE_SIZE
        y_space = max(s.y for s in self.next_figure.squares) + \
            self.config.SQUARE_SIZE
        for s in self.next_figure.squares:
            s.x += ((self.config.SQUARE_SIZE * 4) - x_space) / 2
            s.y += ((self.config.SQUARE_SIZE * 4) - y_space) / 2
            s.fixed_coords = True

    def add_score(self, val: int):
        self.score += val
