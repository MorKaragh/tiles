import pygame
import pygame_menu
from typing import Any, Tuple
from pygame import Surface
from pygame_menu import Theme
from utils import get_grid_state_logger
from game import TetrisGame, GameState
from config import GameConfig
from gui import StateScreen
from input_control import process_events, process_pressed_keys

config = GameConfig()

pygame.init()
screen = pygame.display.set_mode(((config.GRID_COLS + 5) * config.SQUARE_SIZE,
                                  config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

state_logger = get_grid_state_logger()

clock = pygame.time.Clock()

game = TetrisGame(config)
game.state = GameState.MENU

bg = pygame.image.load("images/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (config.GRID_COLS * config.SQUARE_SIZE,
                                 config.GRID_ROWS * config.SQUARE_SIZE))

grid_surf = Surface(config.get_game_grid_size())

font = pygame.font.Font("fonts/Oldtimer-GOPpg.ttf", 20)
mytheme = Theme(background_color=(0, 0, 0, 0),
                title_background_color=(4, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                widget_font=font)

menu = pygame_menu.Menu(
    height=config.get_game_grid_size()[1],
    theme=mytheme,
    title='',
    width=400
)


def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')


def start_the_game() -> None:
    game.state = GameState.RUNNING
    menu.close()


def change_level(val) -> None:
    print(val)
    print(type(val))
    game.config.LEVEL = val
    game.level = val


user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
menu.add.range_slider("Level", range_values=(
    1, 30), increment=1, default=10, onchange=change_level)
menu.add.selector(
    'Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

while game.running:
    clock.tick(60)
    screen.fill("Black")
    screen.blit(bg, (0, 0))

    if game.state == GameState.RUNNING:
        game.update()
        game.grid.draw(screen)
        game.scoreboard.draw(screen)
        if config.DEBUG:
            state_logger.info(game.grid.__repr__())
    elif game.state == GameState.PAUSE:
        game.grid.draw(screen)
        game.scoreboard.draw(screen)
    elif game.state == GameState.LOSS:
        StateScreen.draw_loss(screen, game)
    elif game.state == GameState.MENU:
        events = pygame.event.get()
        screen.fill("Black")
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

    if game.state != GameState.MENU:
        process_pressed_keys(pygame.key.get_pressed(), game, config)
        process_events(pygame.event.get(), game, config)
