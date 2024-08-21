import pygame
import time
from gaming_grid import GamingGrid
from figures import TetrisFugureFactory, FigureMovement

clock = pygame.time.Clock()
running = True

GRID_ROWS = 25
GRID_COLS = 15
SQUARE_SIZE = 40
INITIAL_FALL_SPEED_FACTOR = 0.2
FALL_SPEED_FACTOR = INITIAL_FALL_SPEED_FACTOR
SIDE_MOVE_SPEED_FACTOR = 0.05

pygame.init()
screen = pygame.display.set_mode((GRID_COLS * SQUARE_SIZE,
                                  GRID_ROWS * SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

grid = GamingGrid(GRID_COLS, GRID_ROWS, "Grey", SQUARE_SIZE)
figure_factory = TetrisFugureFactory(GRID_COLS, GRID_ROWS, SQUARE_SIZE)

player = figure_factory.random(GRID_COLS // 2 - 1, 0)
player.add_on_grid(grid)

last_time = time.time()
last_fall_time = 0
last_move_time = 0

accelerate_fall = False
side_move_delay = 0

while running:
    clock.tick(60)
    last_fall_time = last_fall_time + time.time() - last_time
    last_move_time = last_move_time + time.time() - last_time
    last_time = time.time()

    if side_move_delay <= 0:
        side_move_delay += last_move_time

    if last_fall_time > FALL_SPEED_FACTOR:
        last_fall_time = 0
        if not FigureMovement.move_down(player, grid):
            player = figure_factory.random(4, 0)
            player.add_on_grid(grid)
            accelerate_fall = False
            FALL_SPEED_FACTOR = INITIAL_FALL_SPEED_FACTOR

    pressed = pygame.key.get_pressed()
    if last_move_time > SIDE_MOVE_SPEED_FACTOR and side_move_delay > 0:
        last_move_time = 0
        if pressed[pygame.K_RIGHT]:
            FigureMovement.move_figure_right(player, grid)
        elif pressed[pygame.K_LEFT]:
            FigureMovement.move_figure_left(player, grid)
    if pressed[pygame.K_DOWN] and accelerate_fall:
        FALL_SPEED_FACTOR = 0


    screen.fill("White")
    grid.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_k]:
                FigureMovement.rotate(player, grid)
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                accelerate_fall = True
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                side_move_delay = -8
                FigureMovement.move_figure_right(player, grid)
            elif event.key in [pygame.K_LEFT, pygame.K_h]:
                side_move_delay = -8
                FigureMovement.move_figure_left(player, grid)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                accelerate_fall = False
                FALL_SPEED_FACTOR = INITIAL_FALL_SPEED_FACTOR
