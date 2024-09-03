from dataclasses import dataclass


@dataclass
class GameConfig:
    GRID_ROWS = 20
    GRID_COLS = 10
    SQUARE_SIZE = 50
    INITIAL_FALL_SPEED_FACTOR = 0.2
    SIDE_MOVE_SPEED_FACTOR = 0.05
    MOVE_DELAY_FACTOR = 2
    DEBUG = False

    def get_game_grid_size(self):
        return (self.GRID_COLS * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)

    def get_scoreboard_size(self):
        return (5 * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)


game_config = GameConfig()
