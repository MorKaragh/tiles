import pygame
import time
from gaming_grid import GamingGrid, TetrisFigure, TetrisFugureFactory

clock = pygame.time.Clock()
running = True

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

grid = GamingGrid(10, 15, 50)

figure_factory = TetrisFugureFactory(10, 15)
player = figure_factory.brick(5, 0)
grid.add_figure(player)

last_time = time.time()
last_move_time = 0

while running:
    clock.tick(60)
    last_move_time = last_move_time + time.time() - last_time
    last_time = time.time()

    if last_move_time > 0.5:
        player.move_down()
        last_move_time = 0

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
