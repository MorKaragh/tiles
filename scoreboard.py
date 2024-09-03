from animation import AnimatorFactory
from config import GameConfig
from gaming_grid import GamingGrid
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
            "images/frame/glow_frame_ylw.png", (self.size[0], self.size[0]))
        self.sample = Surface((self.config.SQUARE_SIZE * 4,
                               self.config.SQUARE_SIZE * 4))
        self.sample_grid = GamingGrid(4, 4, "Black", self.config.SQUARE_SIZE)
        self.sample_grid.add_new_square(1, 1)

    def draw(self, screen: Surface):
        self.body.fill("Black")
        # self.body.blit(self.frame.next_frame(), (0, 0))
        self.sample.fill("Grey")
        self.sample_grid.draw(self.sample)
        self.body.blit(self.sample, (25, 25))
        self.body.blit(self.frame, (0, 0))
        screen.blit(self.body, self.coords)
