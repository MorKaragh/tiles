import argparse
import pygame
from pygame import Surface

from src.config import GameConfig
from src.game import TetrisGame, GameState
from src.gui import MultiplayerMenu
from src.state_screen import StateScreen
from src.input_control import process_events, process_pressed_keys
from src.multiplayer import Multiplayer
from src.utils import get_grid_state_logger


def run(server, port):

    config = GameConfig.load_default()
    config.MULTIPLAYER = True
    config.SQUARE_SIZE = 25

    pygame.init()
    screen = pygame.display.set_mode(
        (2 * (config.GRID_COLS + 5) * config.SQUARE_SIZE,
         config.GRID_ROWS * config.SQUARE_SIZE))
    pygame.display.set_caption("Tetris")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    state_logger = get_grid_state_logger()

    clock = pygame.time.Clock()

    print("initing game")
    game = TetrisGame(config)
    game.state = GameState.MENU

    print(f"initing multiplayer on {server} {port}")
    multiplayer = Multiplayer(game, server, port)

    bg = pygame.image.load("images/bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (config.GRID_COLS * config.SQUARE_SIZE,
                                     config.GRID_ROWS * config.SQUARE_SIZE))

    main_menu = MultiplayerMenu(multiplayer)

    player_surf = Surface(((config.GRID_COLS + 5) * config.SQUARE_SIZE,
                           config.GRID_ROWS * config.SQUARE_SIZE))

    opponent_surf = Surface(player_surf.get_size())

    def refresh():
        clock.tick(60)
        screen.fill("Black")
        player_surf.fill("Black")
        opponent_surf.fill((5, 9, 22))
        player_surf.blit(bg, (0, 0))

    def display_running():
        game.update()
        game.grid.draw(player_surf)
        game.scoreboard.draw(player_surf)
        multiplayer.draw(opponent_surf)
        screen.blit(player_surf, (0, 0))
        screen.blit(opponent_surf,
                    ((config.GRID_COLS + 5) * config.SQUARE_SIZE, 0))
        if config.DEBUG:
            state_logger.info(game.grid.__repr__())

    def display_pause():
        game.grid.draw(screen)
        game.scoreboard.draw(screen)

    def display_loss():
        multiplayer.set_loss()
        multiplayer.draw(opponent_surf)
        StateScreen.draw_multiplayer_loss(
            player_surf,
            game.scoreboard.score,
            True)
        screen.blit(player_surf, (0, 0))
        screen.blit(opponent_surf,
                    ((config.GRID_COLS + 5) * config.SQUARE_SIZE, 0))

    def display_menu():
        events = pygame.event.get()
        main_menu.update()
        main_menu.menu.update(events)
        main_menu.menu.draw(screen)

    while game.running:

        refresh()

        if game.state == GameState.RUNNING:
            display_running()
        elif game.state == GameState.PAUSE:
            display_pause()
        elif game.state == GameState.LOSS:
            display_loss()
        elif game.state == GameState.MENU:
            display_menu()

        pygame.display.update()

        if game.state != GameState.MENU:
            process_pressed_keys(pygame.key.get_pressed(), game, config)
            process_events(pygame.event.get(), game, config, multiplayer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", required=True,
                        help="Server hostname or IP address")
    parser.add_argument("--port", required=True, type=int,
                        help="Server port number")
    args = parser.parse_args()
    run(args.server, args.port)
