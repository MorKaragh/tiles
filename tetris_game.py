import pygame
from game import TetrisGame, GameConfig

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

    pressed = pygame.key.get_pressed()
    if game.last_move_time > config.SIDE_MOVE_SPEED_FACTOR and game.side_move_delay > 0:
        game.last_move_time = 0
        if pressed[pygame.K_RIGHT]:
            game.movements.move_figure_right()
        elif pressed[pygame.K_LEFT]:
            game.movements.move_figure_left()
    if pressed[pygame.K_DOWN] and game.accelerate_fall:
        game.fall_speed_factor = 0

    screen.fill("White")
    game.grid.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_k]:
                game.movements.rotate()
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                game.accelerate_fall = True
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                game.side_move_delay = -7
                game.movements.move_figure_right()
            elif event.key in [pygame.K_LEFT, pygame.K_h]:
                game.side_move_delay = -7
                game.movements.move_figure_left()
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                game.accelerate_fall = False
                game.fall_speed_factor = config.INITIAL_FALL_SPEED_FACTOR
