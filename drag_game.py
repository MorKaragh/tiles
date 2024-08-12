import pygame
from gaming_grid import GamingGrid

running = True

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

grid = GamingGrid(10, 15, 50)
player = grid.add_square(0, 0)

clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill("White")

    grid.draw(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_k]:
                player.move_up()
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                player.move_down()
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                player.move_right()
            elif event.key in [pygame.K_LEFT, pygame.K_h]:
                player.move_left()
