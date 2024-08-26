import pygame
from animation import AnimatorFactory


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
        self.squares = []
        self.animations = []
        self.cols = cols
        self.rows = rows
        self.square_width = square_width
        self.border_color = border_color
        self.animator_factory = AnimatorFactory()

    def draw(self, screen):
        for square in self.squares:
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
        rows_to_kill = set()
        for a in self.animations:
            if a.is_active():
                screen.blit(a.next_frame(), a.coords)
                if not a.is_active():
                    rows_to_kill.add(a.related_object.row)
        for r in rows_to_kill:
            self._delete_squares_in_row(r)
        if rows_to_kill:
            for r in range(self.rows):
                if self.is_row_full(r):
                    raise Exception("somehow full row stays")
        self.animations = [a for a in self.animations if a.is_active()]

    def add_new_square(self,
                       col: int,
                       row: int,
                       color: str = "Grey") -> GridSquare:
        square = GridSquare(col, row,
                            self.cols, self.rows,
                            self.square_width, color)
        self.squares.append(square)
        return square

    def add_square(self, square):
        self.squares.append(square)

    def remove_square(self, square):
        print(square)
        self.squares = [s for s in self.squares if s != square]

    def has_square_in(self, col, row):
        for s in self.squares:
            if s.col == col and s.row == row:
                return True
        return False

    def get_square_in(self, col, row):
        for s in self.squares:
            if s.col == col and s.row == row:
                return s
        return None

    def has_square_in_row(self, row: int):
        for s in self.squares:
            if s.row == row:
                return True
        return False

    def get_center_x(self):
        return self.cols // 2 - 1

    def is_row_full(self, row: int):
        indexes = {i for i in range(self.cols)}
        for s in self.squares:
            if s.row == row and s.col in indexes:
                indexes.remove(s.col)
        return len(indexes) == 0

    def remove_row(self, row: int):
        for i in range(self.cols):
            coords = (i * self.square_width, self.square_width * row)
            anim = self.animator_factory.get_square_puff(coords)
            anim.related_object = self.get_square_in(i, row)
            self.animations.append(anim)

    def _delete_squares_in_row(self, row: int):
        self.squares = [s for s in self.squares if s.row != row]
        for s in self.squares:
            if s.row < row:
                s.row += 1

    def clear(self):
        self.squares = []

    def __repr__(self):
        return ";".join([f"{s.col}:{s.row}" for s in self.squares])

    def set_state(self, state: str):
        self.clear()
        for coord in state.split(";"):
            x, y = coord.split(":")
            self.add_new_square(int(x), int(y), "Black")
