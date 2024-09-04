from animation import AnimatorFactory
from config import GameConfig
from figures import TetrisFigure
from pygame import Surface
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

    def draw(self, screen: Surface):
        self.body.fill("Black")
        # self.body.blit(self.frame.next_frame(), (0, 0))
        self.sample.fill("Black")
        for s in self.next_figure.squares:
            s.draw(self.sample)
        self.body.blit(self.sample, (25, 25))
        self.body.blit(self.frame, (0, 0))
        screen.blit(self.body, self.coords)

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
