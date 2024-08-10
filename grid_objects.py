import pygame
from global_config import GRID_CELL_SIZE, SCREEN_SIZE


class Grid:

    def draw(self, screen):
        pnt = GRID_CELL_SIZE
        while pnt < SCREEN_SIZE:
            pygame.draw.line(screen, "Grey", (pnt, 0), (pnt, SCREEN_SIZE))
            pygame.draw.line(screen, "Grey", (0, pnt), (SCREEN_SIZE, pnt))
            pnt += GRID_CELL_SIZE


class GridSolidRow(pygame.Rect):

    def __init__(self, y, color="Green"):
        pygame.Rect.__init__(self, 0, y, SCREEN_SIZE, GRID_CELL_SIZE)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class GridSquare(pygame.Rect):

    def __init__(self, x, y, color="Black"):
        pygame.Rect.__init__(self, self.x, self.y,
                             GRID_CELL_SIZE, GRID_CELL_SIZE)
        self.x = x
        self.y = y
        self.color = color

    def move_right(self):
        if self.x + GRID_CELL_SIZE < SCREEN_SIZE:
            self.x += GRID_CELL_SIZE

    def move_left(self):
        if self.x - GRID_CELL_SIZE >= 0:
            self.x -= GRID_CELL_SIZE

    def move_up(self):
        if self.y - GRID_CELL_SIZE >= 0:
            self.y -= GRID_CELL_SIZE

    def move_down(self):
        if self.y + GRID_CELL_SIZE < SCREEN_SIZE:
            self.y += GRID_CELL_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
