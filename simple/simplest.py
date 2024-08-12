import pygame
from events_processor import process_events
from grid_objects import GridSquare, Grid, GridSolidRow
from global_config import SCREEN_SIZE, GRID_CELL_SIZE
from state_screens import StateScreen


class SimpleGame():

    def __init__(self):
        self.init_objects()
        self.state = "PLAY"

    def reset(self):
        self.state = "PLAY"
        self.init_objects()

    def init_objects(self):
        self.player = GridSquare(0, 0)
        self.grid = Grid()
        self.opponent = GridSquare(SCREEN_SIZE - GRID_CELL_SIZE,
                                   SCREEN_SIZE - GRID_CELL_SIZE, "Red")
        self.escape = GridSolidRow(SCREEN_SIZE - GRID_CELL_SIZE)

    def update(self):
        if self.player.colliderect(self.escape):
            game.state = "WIN"
        if self.player.colliderect(self.opponent):
            game.state = "LOSS"

    def draw(self, screen):
        screen.fill("White")
        self.escape.draw(screen)
        self.grid.draw(screen)
        self.player.draw(screen)
        self.opponent.draw(screen)


running = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("simplest game ever")
pygame.display.set_icon(pygame.image.load("../images/icon.png"))

game = SimpleGame()

while running:
    if game.state == "PLAY":
        game.draw(screen)
    elif game.state == "LOSS":
        StateScreen.draw_loss(screen)
    elif game.state == "WIN":
        StateScreen.draw_win(screen)

    game.update()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        else:
            process_events(event, game)
