from typing import Tuple, Any

import pygame
import pygame_menu
from pygame import font, Surface
from pygame_menu import Theme, Menu

from src.multiplayer import Multiplayer
from src.records import load_for_player
from src.game import TetrisGame


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
        if self.multiplayer.status.value == "WFP":
            self.run_btn.set_title("Waiting for player")
        elif self.multiplayer.status.value == "WFS":
            self.run_btn.set_title("Start")

    def set_lvl_auto_change(self, selected: Tuple, value: Any) -> None:
        self.game.config.LEVEL_INCREASE = value

    def start_the_game(self) -> None:
        if self.multiplayer.status == "READY":
            self.game.reset()
            self.game.config.save()
            self.menu.close()
        else:
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


class StateScreen:

    @staticmethod
    def draw_loss(screen, game: TetrisGame):
        surf = Surface(screen.get_size())
        surf.fill((5, 17, 22))
        big_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 60)
        small_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 30)
        main_text = big_font.render("Game over!", True, "White")
        score_text = small_font.render(f"score: {game.scoreboard.score}",
                                       True, "White")
        curr_record = load_for_player(game.config.PLAYER)
        record_text = small_font.render(f"max score: {curr_record}",
                                        True, "White")
        main_rect = main_text.get_rect(
            center=(screen.get_size()[0]/2, 2*screen.get_size()[1]/5))
        score_rect = score_text.get_rect(
            center=(screen.get_size()[0]/2, 3*screen.get_size()[1]/5))
        record_rect = record_text.get_rect(
            center=(screen.get_size()[0]/2, 4*screen.get_size()[1]/5))
        surf.blit(main_text, main_rect)
        surf.blit(score_text, score_rect)
        surf.blit(record_text, record_rect)
        screen.blit(surf, (0, 0))

    @staticmethod
    def draw_win(screen):
        StateScreen._simple_text("You win!", screen)

    @staticmethod
    def _simple_text(text: str, screen: Surface):
        surf = Surface(screen.get_size())
        surf.fill((5, 17, 22))
        text = font.Font("fonts/Oldtimer-GOPpg.ttf",
                         60).render(text, True, "White")
        rect = text.get_rect(
            center=(screen.get_size()[0]/2, screen.get_size()[1]/2))
        surf.blit(text, rect)
        screen.blit(surf, (0, 0))
