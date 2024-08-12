import pygame

SCREEN_SIZE = 10
GRID_CELL_SIZE = 20


class GridSquare(pygame.Rect):

    def __init__(self,
                 col: int,
                 row: int,
                 col_max: int,
                 row_max: int,
                 sizepx: int = 50,
                 color="Black"):
        self.col = col
        self.row = row
        self.col_max = col_max
        self.row_max = row_max
        self.sidepx = sizepx
        self.color = color
        pygame.Rect.__init__(self, self.x, self.y,
                             sizepx, sizepx)

    def move_right(self, step: int = 1):
        if self.col + step < self.col_max:
            self.col += step
            self.x += self.sidepx * step

    def move_left(self, step: int = 1):
        if self.col - step >= 0:
            self.col -= step
            self.x -= self.sidepx * step

    def move_up(self, step: int = 1):
        if self.row - step >= 0:
            self.row -= step
            self.y -= self.sidepx * step

    def move_down(self, step: int = 1):
        if self.row + step < self.row_max:
            self.row += step
            self.y += self.sidepx * step

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class GamingGrid:

    def __init__(self,
                 size_hor: int,
                 size_ver: int,
                 square_width: int = 50):
        self.squares = []
        self.size_hor = size_hor
        self.size_ver = size_ver
        self.square_width = square_width

    def draw(self, screen):
        for i in range(0, self.size_hor + 1):
            pygame.draw.line(screen, "Grey",
                             (i * self.square_width, 0),
                             (i * self.square_width,
                              self.size_ver * self.square_width))
        for i in range(0, self.size_ver + 1):
            pygame.draw.line(screen, "Grey",
                             (0, i * self.square_width),
                             (self.size_hor * self.square_width,
                              i * self.square_width))
        for square in self.squares:
            square.draw(screen)

    def add_square(self,
                   col: int,
                   row: int,
                   color: str = "Grey") -> GridSquare:
        square = GridSquare(col, row,
                            self.size_hor, self.size_ver,
                            self.square_width, color)
        self.squares.append(square)
        return square


class GridSolidRow(pygame.Rect):

    def __init__(self, y, color="Green"):
        pygame.Rect.__init__(self, 0, y, SCREEN_SIZE, GRID_CELL_SIZE)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
