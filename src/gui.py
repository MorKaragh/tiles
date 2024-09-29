from typing import Tuple, Any

import pygame
import pygame_menu
from pygame_menu import Theme, Menu

from src.multiplayer import Multiplayer
from src.game import TetrisGame

connect_button_labels = {}


def default_theme():
    MENU_FONT = pygame.font.Font("fonts/Oldtimer-GOPpg.ttf", 20)
    MENU_THEME = Theme(
        background_color=(0, 0, 0, 0),
        title=False,
        widget_padding=25,
        widget_font=MENU_FONT)
    return MENU_THEME


class MultiplayerMenu:

    def __init__(self, multiplayer: Multiplayer):
        self.font = pygame.font.Font("fonts/Oldtimer-GOPpg.ttf", 20)
        self.multiplayer = multiplayer
        self.game = multiplayer.game
        self.menu = Menu(
            height=self.game.config.get_game_grid_size()[1],
            theme=default_theme(),
            width=400,
            title=''
        )
        player = self.game.config.PLAYER
        self.user_name = self.menu.add.text_input('Name: ',
                                                  default=player,
                                                  maxchar=10,
                                                  onchange=self.change_player)
        self.menu.add.range_slider("Level:",
                                   range_values=[i for i in range(1, 31)],
                                   increment=1,
                                   default=self.game.config.LEVEL,
                                   range_text_value_enabled=False,
                                   onchange=self.change_level)
        autochange = 0 if self.game.config.LEVEL_INCREASE else 1
        self.menu.add.selector('Level auto change: ',
                               [('Yes', True), ('No', False)],
                               onchange=self.set_lvl_auto_change,
                               default=autochange)
        self.menu.add.text_input('Room: ',
                                 default='roomname',
                                 maxchar=10,
                                 onchange=self.change_room)
        self.run_btn = self.menu.add.button('Connect', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def update(self):
        match self.multiplayer.status.value:
            case "IDLE":
                self.run_btn.set_title("CONNECT")
            case "WFP":
                self.run_btn.set_title("WAITING FOR PLAYER")
            case "WFS":
                self.run_btn.set_title("READY")
            case "WFR":
                self.run_btn.set_title("READY")
            case "PLAYING":
                self.run_btn.set_title("START")
            case _:
                self.run_btn.set_title(self.multiplayer.status.value)

    def set_lvl_auto_change(self, selected: Tuple, value: Any) -> None:
        self.game.config.LEVEL_INCREASE = value

    def start_the_game(self) -> None:
        print(self.multiplayer.status)
        match self.multiplayer.status.value:
            case "PLAYING":
                self.game.reset()
                self.game.config.save()
                self.menu.close()
            case "WFS":
                self.multiplayer.set_ready()
            case "WFR":
                self.multiplayer.set_ready()
            case "IDLE":
                self.multiplayer.connect_to_room()

    def change_level(self, val: int) -> None:
        self.game.config.LEVEL = val
        self.game.set_level(val)

    def change_player(self, val: str):
        self.game.config.PLAYER = val

    def change_room(self, val: str):
        self.multiplayer.ROOM_NAME = val


class MainMenu:

    def __init__(self, game: TetrisGame):
        self.font = pygame.font.Font("fonts/Oldtimer-GOPpg.ttf", 20)
        self.game = game
        self.menu = Menu(
            height=self.game.config.get_game_grid_size()[1],
            theme=default_theme(),
            width=400,
            title=''
        )
        player = self.game.config.PLAYER
        self.user_name = self.menu.add.text_input('Name: ',
                                                  default=player,
                                                  maxchar=10,
                                                  onchange=self.change_player)
        self.menu.add.range_slider("Level:",
                                   range_values=[i for i in range(1, 31)],
                                   increment=1,
                                   default=self.game.config.LEVEL,
                                   range_text_value_enabled=False,
                                   onchange=self.change_level)
        autochange = 0 if self.game.config.LEVEL_INCREASE else 1
        self.menu.add.selector('Level auto change: ',
                               [('Yes', True), ('No', False)],
                               onchange=self.set_lvl_auto_change,
                               default=autochange)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def set_lvl_auto_change(self, selected: Tuple, value: Any) -> None:
        self.game.config.LEVEL_INCREASE = value

    def start_the_game(self) -> None:
        self.game.reset()
        self.game.config.save()
        self.menu.close()

    def change_level(self, val: int) -> None:
        self.game.config.LEVEL = val
        self.game.set_level(val)

    def change_player(self, val: str):
        self.game.config.PLAYER = val


