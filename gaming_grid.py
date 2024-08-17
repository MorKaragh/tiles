import pygame
from typing import List

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
        self.sizepx = sizepx
        self.color = color
        pygame.Rect.__init__(self,
                             self.sizepx * self.col,
                             self.sizepx * self.row,
                             sizepx,
                             sizepx)

    def move_right(self, step: int = 1):
        if self.has_space_right(step):
            self.col += step
            self.x += self.sizepx * step

    def has_space_right(self, step: int = 1):
        return self.col + step < self.col_max

    def move_left(self, step: int = 1):
        if self.has_space_left(step):
            self.col -= step
            self.x -= self.sizepx * step

    def has_space_left(self, step: int = 1):
        return self.col - step >= 0

    def move_up(self, step: int = 1):
        if self.has_space_up:
            self.row -= step
            self.y -= self.sizepx * step

    def has_space_up(self, step: int = 1):
        return self.row - step >= 0

    def move_down(self, step: int = 1):
        if self.has_space_down(step):
            self.row += step
            self.y += self.sizepx * step

    def has_space_down(self, step: int = 1):
        return self.row + step < self.row_max

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class TetrisFigure:

    def __init__(self,
                 squares: List[GridSquare],
                 is_falling: bool = True):
        self.squares = squares

    def move_right(self):
        if all([s.has_space_right() for s in self.squares]):
            for s in self.squares:
                s.move_right()

    def move_left(self):
        if all([s.has_space_left() for s in self.squares]):
            for s in self.squares:
                s.move_left()

    def move_down(self):
        if all([s.has_space_down() for s in self.squares]):
            for s in self.squares:
                s.move_down()

    def get_bottom_border_squares(self):
        by_col = {}
        for s in self.squares:
            if s.col not in by_col:
                by_col[s.col] = s
            elif by_col.get(s.col) and by_col[s.col].row < s.row:
                by_col[s.col] = s
        return by_col.values()


class GamingGrid:

    def __init__(self,
                 size_hor: int,
                 size_ver: int,
                 color: str = "Grey",
                 square_width: int = 50):
        self.squares = []
        self.size_hor = size_hor
        self.size_ver = size_ver
        self.square_width = square_width
        self.color = color

    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)
        for i in range(0, self.size_hor + 1):
            pygame.draw.line(screen, self.color,
                             (i * self.square_width, 0),
                             (i * self.square_width,
                              self.size_ver * self.square_width))
        for i in range(0, self.size_ver + 1):
            pygame.draw.line(screen, self.color,
                             (0, i * self.square_width),
                             (self.size_hor * self.square_width,
                              i * self.square_width))

    def add_square(self,
                   col: int,
                   row: int,
                   color: str = "Grey") -> GridSquare:
        square = GridSquare(col, row,
                            self.size_hor, self.size_ver,
                            self.square_width, color)
        self.squares.append(square)
        return square

    def has_square_in(self, row, col):
        for s in self.squares:
            if s.row == row and s.col == col:
                return True
        return False

    def add_figure(self, figure: TetrisFigure):
        self.squares.extend(figure.squares)


class TetrisFugureFactory:

    def __init__(self, col_max: int, row_max: int, square_size: int = 50):
        self.col_max = col_max
        self.row_max = row_max
        self.square_size = square_size

    def random(self, col: int, row: int) -> TetrisFigure:
        pass

    def brick(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max, self.square_size),
                   GridSquare(col + 1, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max, self.square_size)]
        return TetrisFigure(squares)


class GridSolidRow(pygame.Rect):

    def __init__(self, y, color="Green"):
        pygame.Rect.__init__(self, 0, y, SCREEN_SIZE, GRID_CELL_SIZE)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
