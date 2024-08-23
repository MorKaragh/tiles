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

    def has_space_right(self, step: int = 1):
        return self.col + step < self.col_max

    def move_left(self, step: int = 1):
        if self.has_space_left(step):
            self.col -= step

    def has_space_left(self, step: int = 1):
        return self.col - step >= 0

    def move_up(self, step: int = 1):
        if self.has_space_up:
            self.row -= step

    def has_space_up(self, step: int = 1):
        return self.row - step >= 0

    def move_down(self, step: int = 1):
        if self.has_space_down(step):
            self.row += step

    def has_space_down(self, step: int = 1):
        return self.row + step < self.row_max

    def draw(self, screen):
        self.x = self.col * self.sizepx
        self.y = self.row * self.sizepx
        pygame.draw.rect(screen, self.color, self)


class GamingGrid:

    def __init__(self,
                 cols: int,
                 rows: int,
                 border_color: str = "Grey",
                 square_width: int = 50):
        self.squares = [[None] * rows for i in range(cols)]
        self.cols = cols
        self.rows = rows
        self.square_width = square_width
        self.border_color = border_color

    def draw(self, screen):
        for row in self.squares:
            for square in row:
                if square:
                    square.draw(screen)
        for i in range(0, self.cols + 1):
            pygame.draw.line(screen, self.border_color,
                             (i * self.square_width, 0),
                             (i * self.square_width,
                              self.rows * self.square_width))
        for i in range(0, self.rows + 1):
            pygame.draw.line(screen, self.border_color,
                             (0, i * self.square_width),
                             (self.cols * self.square_width,
                              i * self.square_width))

    def add_new_square(self,
                       col: int,
                       row: int,
                       color: str = "Grey") -> GridSquare:
        square = GridSquare(col, row,
                            self.cols, self.rows,
                            self.square_width, color)
        self.squares[col][row] = square
        return square

    def add_square(self, square):
        self.squares[square.col][square.row] = square

    def has_square_in(self, col, row):
        if 0 > col > self.cols - 1 or 0 > row > self.rows - 1:
            return False
        return self.squares[col][row]
        # for s in self.squares:
        #     if s.row == row and s.col == col:
        #         return True
        # return False

    def get_center_x(self):
        return self.cols // 2 - 1

    def is_row_full(row: int):
        pass


class GridSolidRow(pygame.Rect):

    def __init__(self, y, color="Green"):
        pygame.Rect.__init__(self, 0, y, SCREEN_SIZE, GRID_CELL_SIZE)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
