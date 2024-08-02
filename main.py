import pygame
from events_processor import process_events
from grid_objects import GridSquare, Grid
from global_config import SCREEN_SIZE, GRID_CELL_SIZE

running = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("simplest game ever")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

player = GridSquare(0, 0)
grid = Grid()
opponent = GridSquare(SCREEN_SIZE - GRID_CELL_SIZE,
                      SCREEN_SIZE - GRID_CELL_SIZE, "Red")

while running:
    screen.fill("White")
    grid.draw(screen)
    player.draw(screen)
    opponent.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        process_events(event, player, opponent)
