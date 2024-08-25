import time
from dataclasses import dataclass
from enum import Enum
from gaming_grid import GamingGrid
from figures import TetrisFugureFactory, FigureMovement


@dataclass
class GameConfig:
    GRID_ROWS = 20
    GRID_COLS = 10
    SQUARE_SIZE = 50
    INITIAL_FALL_SPEED_FACTOR = 0.2
    SIDE_MOVE_SPEED_FACTOR = 0.05
    MOVE_DELAY_FACTOR = 6


class GameState(Enum):
    RUNNING = 0
    LOSS = 1


class TetrisGame:

    def __init__(self):
        self.config = GameConfig()
        self.grid = GamingGrid(
            self.config.GRID_COLS,
            self.config.GRID_ROWS,
            "Grey",
            self.config.SQUARE_SIZE)
        self.figure_factory = TetrisFugureFactory(self.config.GRID_COLS,
                                                  self.config.GRID_ROWS,
                                                  self.config.SQUARE_SIZE)
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

    def update(self, screen):
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

    def _process_figure_landing(self):
        for s in self.player.squares:
            if self.grid.is_row_full(s.row):
                self.grid.remove_row(s.row)
        if self.grid.has_square_in_row(0):
            self.state = GameState.LOSS
        self.player = self.figure_factory.random(
            self.grid.get_center_x(), 0)
        self.movements.figure = self.player
        self.player.add_on_grid(self.grid)
        self.accelerate_fall = False
        self.fall_speed_factor = self.config.INITIAL_FALL_SPEED_FACTOR
