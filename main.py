import pygame
from grid_objects import GridSquare
from global_config import SCREEN_SIZE, GRID_CELL_SIZE


running = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("simplest game ever")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

player = GridSquare(0, 0)


def draw_grid():
    pnt = GRID_CELL_SIZE
    while pnt < SCREEN_SIZE:
        pygame.draw.line(screen, "Black", (pnt, 0), (pnt, SCREEN_SIZE))
        pygame.draw.line(screen, "Black", (0, pnt), (SCREEN_SIZE, pnt))
        pnt += GRID_CELL_SIZE


def process_events(event):
    global running
    if event.type == pygame.QUIT:
        pygame.quit()
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_k]:
            player.move_up()
        elif event.key in [pygame.K_DOWN, pygame.K_j]:
            player.move_down()
        elif event.key in [pygame.K_RIGHT, pygame.K_l]:
            player.move_right()
        elif event.key in [pygame.K_LEFT, pygame.K_h]:
            player.move_left()


while running:
    screen.fill("White")
    draw_grid()
    player.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        process_events(event)
