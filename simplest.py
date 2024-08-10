import pygame
from pygame import font
from events_processor import process_events
from grid_objects import GridSquare, Grid, GridSolidRow
from global_config import SCREEN_SIZE, GRID_CELL_SIZE
from state_screens import StateScreen


def init_objects():
    return (GridSquare(0, 0),
            Grid(),
            GridSquare(SCREEN_SIZE - GRID_CELL_SIZE,
                       SCREEN_SIZE - GRID_CELL_SIZE, "Red"),
            GridSolidRow(SCREEN_SIZE - GRID_CELL_SIZE))


running = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("simplest game ever")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

player, grid, opponent, escape = init_objects()

state = "PLAY"

while running:
    if state == "PLAY":
        screen.fill("White")
        escape.draw(screen)
        grid.draw(screen)
        player.draw(screen)
        opponent.draw(screen)
    elif state == "LOSS":
        StateScreen.draw_loss(screen)
    elif state == "WIN":
        StateScreen.draw_win(screen)
    if player.colliderect(opponent):
        state = "LOSS"
    if player.colliderect(escape):
        state = "WIN"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        else:
            process_events(event, player, opponent)
    pygame.display.update()
