import time
from effects import SoundEffects
from animation import AnimatorFactory
from dataclasses import dataclass
from enum import Enum
from gaming_grid import GamingGrid
from scoreboard import ScoreBoard
from figures import TetrisFugureFactory, FigureMovement


@dataclass
class GameConfig:
    GRID_ROWS = 20
    GRID_COLS = 10
    SQUARE_SIZE = 50
    INITIAL_FALL_SPEED_FACTOR = 0.2
    SIDE_MOVE_SPEED_FACTOR = 0.05
    MOVE_DELAY_FACTOR = 2

    def get_game_grid_size(self):
        return (self.GRID_COLS * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)

    def get_scoreboard_size(self):
        return (5 * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)


class GameState(Enum):
    RUNNING = 0
    LOSS = 1
    PAUSE = 2


class TetrisGame:

    def __init__(self, config: GameConfig):
        self.config = config
        self.effects = SoundEffects()
        self.animations = AnimatorFactory()
        self.grid = GamingGrid(
            self.config.GRID_COLS,
            self.config.GRID_ROWS,
            "Black",
            self.config.SQUARE_SIZE,
            self.animations)
        self.figure_factory = TetrisFugureFactory(self.config.GRID_COLS,
                                                  self.config.GRID_ROWS,
                                                  self.config.SQUARE_SIZE)
        self.scoreboard = ScoreBoard(self.config.get_scoreboard_size(),
                                     (self.config.GRID_COLS *
                                      self.config.SQUARE_SIZE, 0),
                                     self.animations)
        self.player = self.figure_factory.random(self.grid.get_center_x(), 0)
        self.movements = FigureMovement(self.player, self.grid)
        self.player.add_on_grid(self.grid)
        self.state = GameState.RUNNING
        self.running = True
        self.fall_speed_factor = self.config.INITIAL_FALL_SPEED_FACTOR
        self.last_time = time.time()
        self.last_fall_time = 0
        self.last_move_time = 0
        self.accelerate_fall = False
        self.side_move_delay = 0

    def update(self):
        time_gap = time.time() - self.last_time
        self.last_fall_time = self.last_fall_time + time_gap
        self.last_move_time = self.last_move_time + time_gap
        self.last_time = time.time()

        if self.side_move_delay <= 0:
            self.side_move_delay += self.last_move_time

        if self.last_fall_time > self.fall_speed_factor:
            self.last_fall_time = 0
            if not self.movements.move_down():
                self._process_figure_landing()

    def reset(self):
        self.grid.clear()
        self.player = self.figure_factory.random(self.grid.get_center_x(), 0)
        self.movements = FigureMovement(self.player, self.grid)
        self.player.add_on_grid(self.grid)
        self.state = GameState.RUNNING
        self.running = True

    def _process_figure_landing(self):
        full_rows = set()
        for s in self.player.squares:
            if self.grid.is_row_full(s.row):
                full_rows.add(s.row)
        if full_rows:
            self.grid.remove_rows(full_rows)
            self.effects.puff()
        else:
            self.effects.touch()
        if self.grid.has_square_in_row(0):
            self.state = GameState.LOSS
        self.player = self.figure_factory.random(
            self.grid.get_center_x(), 0)
        self.movements.figure = self.player
        self.player.add_on_grid(self.grid)
        self.accelerate_fall = False
        self.fall_speed_factor = self.config.INITIAL_FALL_SPEED_FACTOR
