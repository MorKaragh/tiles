import pygame
import time
from gaming_grid import GamingGrid
from figures import TetrisFugureFactory, FigureMovement

clock = pygame.time.Clock()
running = True

GRID_ROWS = 25
GRID_COLS = 15
SQUARE_SIZE = 20
INITIAL_SPEED_FACTOR = 0.2
SPEED_FACTOR = INITIAL_SPEED_FACTOR

pygame.init()
screen = pygame.display.set_mode((GRID_COLS * SQUARE_SIZE,
                                  GRID_ROWS * SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

grid = GamingGrid(GRID_COLS, GRID_ROWS, "Grey", SQUARE_SIZE)
figure_factory = TetrisFugureFactory(GRID_COLS, GRID_ROWS, SQUARE_SIZE)

player = figure_factory.random(4, 0)
player.add_on_grid(grid)

last_time = time.time()
last_move_time = 0

accelerate_fall = False

while running:
    clock.tick(60)
    last_move_time = last_move_time + time.time() - last_time
    last_time = time.time()

    if last_move_time > SPEED_FACTOR:
        last_move_time = 0
        if not FigureMovement.move_down(player, grid):
            player = figure_factory.random(4, 0)
            player.add_on_grid(grid)
            accelerate_fall = False
            SPEED_FACTOR = INITIAL_SPEED_FACTOR

    screen.fill("White")
    grid.draw(screen)
    pygame.display.update()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN] and accelerate_fall:
        SPEED_FACTOR = 0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_k]:
                FigureMovement.rotate(player, grid)
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                accelerate_fall = True
                # FigureMovement.fall_down(player, grid)
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                FigureMovement.move_figure_right(player, grid)
            elif event.key in [pygame.K_LEFT, pygame.K_h]:
                FigureMovement.move_figure_left(player, grid)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                accelerate_fall = False
                SPEED_FACTOR = INITIAL_SPEED_FACTOR
