import pygame
from pygame import Surface
from utils import get_grid_state_logger
from game import TetrisGame, GameConfig, GameState
from gui import StateScreen
from input_control import process_events, process_pressed_keys

config = GameConfig()

pygame.init()
screen = pygame.display.set_mode(((config.GRID_COLS + 5) * config.SQUARE_SIZE,
                                  config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

state_logger = get_grid_state_logger()
DEBUG = True

clock = pygame.time.Clock()

game = TetrisGame(config)

bg = pygame.image.load("images/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (config.GRID_COLS * config.SQUARE_SIZE,
                                 config.GRID_ROWS * config.SQUARE_SIZE))

grid_surf = Surface(config.get_game_grid_size())

while game.running:
    clock.tick(60)
    screen.fill("Black")
    screen.blit(bg, (0, 0))

    if game.state == GameState.RUNNING:
        game.update()
        game.grid.draw(screen)
        game.scoreboard.draw(screen)
        # screen.blit(grid_surf, (0, 0))
        if DEBUG:
            state_logger.info(game.grid.__repr__())
    elif game.state == GameState.PAUSE:
        game.grid.draw(screen)
    elif game.state == GameState.LOSS:
        StateScreen.draw_loss(screen)

    pygame.display.update()

    process_pressed_keys(pygame.key.get_pressed(), game, config)
    process_events(pygame.event.get(), game, config)
