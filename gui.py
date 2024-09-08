import pygame
import pygame_menu
from pygame_menu import Theme, Menu, widgets
from pygame import font, Surface
from typing import Tuple, Any
from game import TetrisGame


class MainMenu:

    def __init__(self, game: TetrisGame):
        self.font = pygame.font.Font("fonts/Oldtimer-GOPpg.ttf", 20)
        self.mytheme = Theme(background_color=(0, 0, 0, 0),
                             title=False,
                             widget_padding=25,
                             widget_font=self.font)
        self.game = game
        self.menu = Menu(
            height=self.game.config.get_game_grid_size()[1],
            theme=self.mytheme,
            title='',
            width=400
        )
        self.user_name = self.menu.add.text_input('Name: ',
                                                  default='Player',
                                                  maxchar=10)
        self.menu.add.range_slider("Level:",
                                   range_values=(1, 30),
                                   increment=1,
                                   default=self.game.config.LEVEL,
                                   onchange=self.change_level)
        self.menu.add.selector('Level auto change: ',
                               [('Yes', True), ('No', False)],
                               onchange=self.set_lvl_auto_change,
                               default=0 if self.game.config.LEVEL_INCREASE else 1)
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
        main_rect = main_text.get_rect(
            center=(screen.get_size()[0]/2, screen.get_size()[1]/2))
        score_rect = score_text.get_rect(
            center=(screen.get_size()[0]/2, 3*screen.get_size()[1]/4))
        surf.blit(main_text, main_rect)
        surf.blit(score_text, score_rect)
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
