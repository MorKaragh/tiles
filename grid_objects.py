import pygame
from global_config import GRID_CELL_SIZE, SCREEN_SIZE


class GridSquare:

    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        pygame.draw.rect(screen, "Black",
                         pygame.Rect(self.x, self.y,
                                     GRID_CELL_SIZE, GRID_CELL_SIZE))
