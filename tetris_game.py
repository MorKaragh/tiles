import pygame
import time
from gaming_grid import GamingGrid, TetrisFugureFactory

clock = pygame.time.Clock()
running = True

GRID_ROWS = 25
GRID_COLS = 15
SQUARE_SIZE = 20

pygame.init()
screen = pygame.display.set_mode((GRID_COLS * SQUARE_SIZE,
                                  GRID_ROWS * SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

grid = GamingGrid(GRID_COLS, GRID_ROWS, "Grey", SQUARE_SIZE)
figure_factory = TetrisFugureFactory(GRID_COLS, GRID_ROWS, SQUARE_SIZE)
player = figure_factory.random(4, 0)
grid.add_figure(player)

last_time = time.time()
last_move_time = 0

while running:
    clock.tick(60)
    last_move_time = last_move_time + time.time() - last_time
    last_time = time.time()

    if last_move_time > 0.2:
        last_move_time = 0
        is_blocked = False
        for s in player.get_bottom_border_squares():
            if s.row == GRID_ROWS - 1 or grid.has_square_in(s.row + 1, s.col):
                is_blocked = True
                break
        if not is_blocked:
            player.move_down()
        else:
            player = figure_factory.random(4, 0)
            grid.add_figure(player)

    screen.fill("White")
    grid.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_k]:
                pass
                # player.move_up()
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                player.move_down()
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                player.move_right()
            elif event.key in [pygame.K_LEFT, pygame.K_h]:
                player.move_left()
