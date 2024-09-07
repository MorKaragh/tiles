import time
from config import GameConfig
from effects import SoundEffects
from animation import AnimatorFactory
from enum import Enum
from gaming_grid import GamingGrid
from scoreboard import ScoreBoard
from figures import TetrisFugureFactory, FigureMovement


class GameState(Enum):
    RUNNING = 0
    LOSS = 1
    PAUSE = 2
    MENU = 3


class TetrisGame:

    def __init__(self, config: GameConfig):
        self.config = config
        self.sound_effects = SoundEffects()
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
        self.scoreboard = ScoreBoard(self.config, self.animations)
        self.player = self.figure_factory.random(self.grid.get_center_x(), 0)
        self.next_player = self.figure_factory.random()
        self.movements = FigureMovement(self.next_player, self.grid)
        self.movements.rotate_randomly(move_to_corner=True)
        self.scoreboard.set_next_figure(self.next_player)
        self.movements.figure = self.player
        self.movements.rotate_randomly()
        self.player.add_on_grid(self.grid)
        self.state = GameState.RUNNING
        self.running = True
        self.level = self.config.LEVEL
        self.fall_speed_factor = self.get_fall_speed_factor()
        self.last_time = time.time()
        self.last_fall_time = 0
        self.last_move_time = 0
        self.accelerate_fall = False
        self.side_move_delay = 0
        self.level_increase_limit = self.config.LEVEL_ROW_LIMIT

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
        self.scoreboard.reset()
        self.movements = FigureMovement(self.player, self.grid)
        self.player.add_on_grid(self.grid)
        self.state = GameState.RUNNING
        self.running = True
        self.level = self.config.LEVEL

    def _process_figure_landing(self):
        self._process_full_rows()
        if self.grid.has_square_in_row(0):
            self.state = GameState.LOSS
        self._change_player_figure()
        self.accelerate_fall = False
        self.fall_speed_factor = self.get_fall_speed_factor()

    def _process_full_rows(self):
        full_rows = set()
        for s in self.player.squares:
            if self.grid.is_row_full(s.row):
                full_rows.add(s.row)
        if full_rows:
            self.scoreboard.add_score(self._calc_score(len(full_rows)))
            self.grid.remove_rows(full_rows)
            if len(full_rows) > 2:
                self.sound_effects.break_hard()
            else:
                self.sound_effects.light_break()
            if self.config.LEVEL_INCREASE:
                self.level_increase_limit -= len(full_rows)
                if self.level_increase_limit <= 0:
                    self.level_increase_limit = self.config.LEVEL_ROW_LIMIT
                    self.level += 1
                    self.scoreboard.level = self.level
        else:
            self.sound_effects.touch()

    def _change_player_figure(self):
        self.player = self.next_player
        for s in self.player.squares:
            s.col += self.config.GRID_COLS // 2 - 1
            s.fixed_coords = False
        self.next_player = self.figure_factory.random()
        self.movements.figure = self.next_player
        self.movements.rotate_randomly(move_to_corner=True)
        self.scoreboard.set_next_figure(self.next_player)
        self.movements.figure = self.player
        self.player.add_on_grid(self.grid)

    def _calc_score(self, rows_cnt):
        return self.level * 100 * rows_cnt * rows_cnt // 2

    def get_fall_speed_factor(self):
        return 0.45 - (0.015 * self.level)
