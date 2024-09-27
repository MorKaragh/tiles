import pygame
from pygame import Surface

from src import records
from src.config import GameConfig
from src.game import TetrisGame, GameState
from src.gui import StateScreen, MultiplayerMenu
from src.input_control import process_events, process_pressed_keys
from src.multiplayer import Multiplayer
from src.utils import get_grid_state_logger

config = GameConfig.load_default()
config.MULTIPLAYER = True

pygame.init()
screen = pygame.display.set_mode(
    (2 * (config.GRID_COLS + 5) * config.SQUARE_SIZE,
     config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Tetris")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

state_logger = get_grid_state_logger()

clock = pygame.time.Clock()

game = TetrisGame(config)
game.state = GameState.MENU

multiplayer = Multiplayer(game)

bg = pygame.image.load("images/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (config.GRID_COLS * config.SQUARE_SIZE,
                                 config.GRID_ROWS * config.SQUARE_SIZE))

main_menu = MultiplayerMenu(multiplayer)

opponent_surf = Surface(((config.GRID_COLS + 5) * config.SQUARE_SIZE,
                         config.GRID_ROWS * config.SQUARE_SIZE))

while game.running:
    clock.tick(60)
    screen.fill("Black")
    screen.blit(bg, (0, 0))

    if game.state == GameState.RUNNING:
        game.update()
        game.grid.draw(screen)
        game.scoreboard.draw(screen)
        opponent_surf.fill("Grey")
        game.opponent.draw(opponent_surf)
        screen.blit(opponent_surf,
                    ((config.GRID_COLS + 5) * config.SQUARE_SIZE, 0))
        if config.DEBUG:
            state_logger.info(game.grid.__repr__())
    elif game.state == GameState.PAUSE:
        game.grid.draw(screen)
        game.scoreboard.draw(screen)
    elif game.state == GameState.LOSS:
        records.save(game.config.PLAYER, game.scoreboard.score)
        StateScreen.draw_loss(screen, game)
    elif game.state == GameState.MENU:
        events = pygame.event.get()
        screen.fill("Black")
        main_menu.update()
        main_menu.menu.update(events)
        main_menu.menu.draw(screen)

    pygame.display.update()

    if game.state != GameState.MENU:
        process_pressed_keys(pygame.key.get_pressed(), game, config)
        process_events(pygame.event.get(), game, config)
