import json
from dataclasses import dataclass, asdict, field

FILENAME = "../storage.json"


@dataclass
class GameConfig:

    PLAYER: str = field(default="Player")
    GRID_ROWS: int = field(default=20)
    GRID_COLS: int = field(default=10)
    SQUARE_SIZE: int = field(default=50)
    LEVEL: int = field(default=10)
    LEVEL_INCREASE: bool = field(default=True)
    LEVEL_ROW_LIMIT: int = field(default=10)
    SIDE_MOVE_SPEED_FACTOR: float = field(default=0.05)
    DEBUG: bool = field(default=False)
    MULTIPLAYER: bool = field(default=False)

    def get_game_grid_size(self):
        return (self.GRID_COLS * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)

    def get_scoreboard_size(self):
        return (5 * self.SQUARE_SIZE,
                self.GRID_ROWS * self.SQUARE_SIZE)

    def save(self):
        with open(FILENAME, 'w') as f:
            json.dump(asdict(self), f, indent=4)

    @staticmethod
    def load_default():
        try:
            with open(FILENAME, 'r') as f:
                data = json.load(f)
                to_return = GameConfig(**data)
                return to_return
        except FileNotFoundError:
            return GameConfig()
