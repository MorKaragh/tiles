from typing import List, Iterable

import pygame
from pygame import Surface

from src.animation import AnimatorFactory, Animator


class SquareImages:
    def __init__(self, square_size_px: int):
        self.square_size_px = square_size_px
        self.red = self.load_img("images/red.png")
        self.pink = self.load_img("images/pink.png")
        self.green = self.load_img("images/green.png")
        self.blue = self.load_img("images/blue.png")
        self.bluer = self.load_img("images/bluer.png")
        self.violet = self.load_img("images/violet.png")
        self.yellow = self.load_img("images/yellow.png")

    def load_img(self, path: str):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (self.square_size_px,
                                            self.square_size_px))


class GridSquare(pygame.Rect):

    def __init__(self,
                 col: int,
                 row: int,
                 col_max: int,
                 row_max: int,
                 sizepx: int = 50,
                 color: str = "Black",
                 image: Surface = None):
        self.col = col
        self.row = row
        self.col_max = col_max
        self.row_max = row_max
        self.sizepx = sizepx
        self.color = color
        self.image = image
        self.fixed_coords = None
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
        if self.has_space_up(step):
            self.row -= step

    def has_space_up(self, step: int = 1):
        return self.row - step >= 0

    def move_down(self, step: int = 1):
        if self.has_space_down(step):
            self.row += step

    def has_space_down(self, step: int = 1):
        return self.row + step < self.row_max

    def draw(self, screen: Surface):
        if not self.fixed_coords:
            self.recalc_coords()
        if self.image:
            screen.blit(self.image, self)
        else:
            pygame.draw.rect(screen, self.color, self)

    def recalc_coords(self):
        self.x = self.col * self.sizepx
        self.y = self.row * self.sizepx


class RowRemovalAnimation:

    def __init__(self, rows: List[int], animations: Iterable[Animator]):
        self.rows = sorted(rows)
        self.animations = animations
        self.active = True

    def draw(self, screen: Surface):
        if not self.active:
            return
        played_anim = False
        for a in self.animations:
            if a.is_active():
                screen.blit(a.next_frame(), a.coords)
                played_anim = True
        if not played_anim:
            self.active = False


class GamingGrid:

    def __init__(self,
                 cols: int,
                 rows: int,
                 border_color: str = "Black",
                 square_width: int = 50,
                 animations: AnimatorFactory = None):
        self.squares = []
        self.cols = cols
        self.rows = rows
        self.square_width = square_width
        self.border_color = border_color
        self.animator_factory = animations
        self.rows_removal_anim = None

    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)
        self._draw_grid_skel(screen)
        if self.animator_factory:
            self._process_animations(screen)

    def _draw_grid_skel(self, screen):
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

    def _process_animations(self, screen):
        if self.rows_removal_anim:
            self.rows_removal_anim.draw(screen)
            if not self.rows_removal_anim.active:
                for row in self.rows_removal_anim.rows:
                    self._delete_squares_in_row(row)
                self.rows_removal_anim = None

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

    def remove_rows(self, rows):
        animations = []
        for row in rows:
            for i in range(self.cols):
                coords = (i * self.square_width, self.square_width * row)
                anim = self.animator_factory.get_square_puff(coords)
                anim.related_object = self.get_square_in(i, row)
                animations.append(anim)
        self.rows_removal_anim = RowRemovalAnimation(rows, animations)

    def remove_row(self, row: int):
        for i in range(self.cols):
            coords = (i * self.square_width, self.square_width * row)
            anim = self.animator_factory.get_square_puff(coords)
            anim.related_object = self.get_square_in(i, row)
            self.rows_removal_anim.append(anim)

    def _delete_squares_in_row(self, row: int):
        self.squares = [s for s in self.squares if s.row != row]
        for s in self.squares:
            if s.row < row:
                s.row += 1

    def clear(self):
        self.squares = []

    def __repr__(self):
        return ";".join([f"{s.col}:{s.row}" for s in self.squares])

    def get_state(self) -> str:
        state = "".join([f"!{x.col}:{x.row}:{x.color}" for x in self.squares])
        return state

    def set_state(self, state: str):
        self.clear()
        for coord in state.split(";"):
            x, y = coord.split(":")
            self.add_new_square(int(x), int(y), "Black")
