import pygame
from utils import get_grid_state_logger
from game import TetrisGame, GameConfig, GameState
from gui import StateScreen
from input_control import process_events, process_pressed_keys

state_logger = get_grid_state_logger()
DEBUG = True

clock = pygame.time.Clock()

config = GameConfig()
game = TetrisGame(config)
pygame.init()
screen = pygame.display.set_mode((config.GRID_COLS * config.SQUARE_SIZE,
                                  config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))


while game.running:
    clock.tick(60)
    screen.fill("White")

    if game.state == GameState.RUNNING:
        game.update(screen)
        game.grid.draw(screen)
        if DEBUG:
            state_logger.info(game.grid.__repr__())
    elif game.state == GameState.PAUSE:
        game.grid.draw(screen)
    elif game.state == GameState.LOSS:
        StateScreen.draw_loss(screen)

    pygame.display.update()

    process_pressed_keys(pygame.key.get_pressed(), game, config)
    process_events(pygame.event.get(), game, config)
