import pygame
from game import TetrisGame, GameConfig
from input_control import process_events, process_pressed_keys

clock = pygame.time.Clock()

config = GameConfig()
game = TetrisGame()
pygame.init()
screen = pygame.display.set_mode((config.GRID_COLS * config.SQUARE_SIZE,
                                  config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))


while game.running:
    clock.tick(60)
    game.update()

    screen.fill("White")
    game.grid.draw(screen)
    pygame.display.update()

    process_pressed_keys(pygame.key.get_pressed(), game, config)
    process_events(pygame.event.get(), game, config)
