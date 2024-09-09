import random
from enum import Enum
from typing import List

from gaming_grid import GridSquare, GamingGrid, SquareImages


class FigureType(Enum):
    LINE = "LINE"
    BRICK = "BRICK"
    T = "T"
    L = "L"
    J = "J"
    Z = "Z"
    S = "S"


class TetrisFigure:

    def __init__(self,
                 squares: List[GridSquare],
                 figure_type: FigureType,
                 is_falling: bool = True):
        self.squares = squares
        self.figure_type = figure_type

    def move_up(self):
        if all([s.has_space_up() for s in self.squares]):
            for s in self.squares:
                s.move_up()

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

    def add_on_grid(self, grid: GamingGrid):
        grid.squares.extend(self.squares)

    def get_bottom_border_squares(self):
        by_col = {}
        for s in self.squares:
            if s.col not in by_col:
                by_col[s.col] = s
            elif by_col[s.col].row < s.row:
                by_col[s.col] = s
        return by_col.values()

    def get_upper_border_squares(self):
        by_row = {}
        for s in self.squares:
            if s.row not in by_row:
                by_row[s.row] = s
            elif by_row[s.row].col > s.col:
                by_row[s.row] = s
        return by_row.values()

    def get_left_border_squares(self):
        by_row = {}
        for s in self.squares:
            if s.row not in by_row:
                by_row[s.row] = s
            elif by_row[s.row].col > s.col:
                by_row[s.row] = s
        return by_row.values()

    def get_right_border_squares(self):
        by_row = {}
        for s in self.squares:
            if s.row not in by_row:
                by_row[s.row] = s
            elif by_row[s.row].col < s.col:
                by_row[s.row] = s
        return by_row.values()


class TetrisFugureFactory:

    def __init__(self, col_max: int, row_max: int, square_size: int = 50):
        self.col_max = col_max
        self.row_max = row_max
        self.square_size = square_size
        self.images = SquareImages(square_size)

    def random(self, col: int = 0, row: int = 0) -> TetrisFigure:
        funcs = [self.brick, self.L, self.J, self.T,
                 self.S, self.Z, self.line, self.line]
        choise = random.choice(funcs)
        return choise(col, row)

    def produce_by_type(self, col: int, row: int, figure_type: FigureType):
        match figure_type:
            case FigureType.LINE:
                return self.line(col, row)
            case FigureType.BRICK:
                return self.brick(col, row)
            case FigureType.L:
                return self.L(col, row)
            case FigureType.J:
                return self.J(col, row)
            case FigureType.Z:
                return self.Z(col, row)
            case FigureType.S:
                return self.S(col, row)
            case FigureType.T:
                return self.T(col, row)

    def brick(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.yellow),
                   GridSquare(col + 1, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.yellow),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.yellow),
                   GridSquare(col + 1, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.yellow)]
        return TetrisFigure(squares, FigureType.BRICK)

    def L(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.red),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.red),
                   GridSquare(col, row + 2, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.red),
                   GridSquare(col + 1, row + 2, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.red)]
        return TetrisFigure(squares, FigureType.L)

    def J(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.bluer),
                   GridSquare(col + 1, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.bluer),
                   GridSquare(col + 1, row + 2, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.bluer),
                   GridSquare(col, row + 2, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.bluer)]
        return TetrisFigure(squares, FigureType.J)

    def S(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.green),
                   GridSquare(col + 1, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.green),
                   GridSquare(col + 1, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.green),
                   GridSquare(col + 2, row + 1, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.green)]
        return TetrisFigure(squares, FigureType.S)

    def Z(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.pink),
                   GridSquare(col + 2, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.pink),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.pink),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.pink)]
        return TetrisFigure(squares, FigureType.Z)

    def T(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.violet),
                   GridSquare(col + 2, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.violet),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.violet),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.violet)]
        return TetrisFigure(squares, FigureType.T)

    def line(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.blue),
                   GridSquare(col + 2, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.blue),
                   GridSquare(col, row, self.col_max,
                              self.row_max, self.square_size,
                              image=self.images.blue),
                   GridSquare(col + 3, row, self.col_max, self.row_max,
                              self.square_size,
                              image=self.images.blue)]
        return TetrisFigure(squares, FigureType.LINE)


class FigureMovement:

    def __init__(self, player, grid):
        self.figure = player
        self.grid = grid

    def move_down(self):
        for s in self.figure.get_bottom_border_squares():
            cell_occupied = self.grid.has_square_in(s.col, s.row + 1)
            if s.row == self.grid.rows - 1 or cell_occupied:
                return False
        self.figure.move_down()
        return True

    def move_right(self):

        for s in self.figure.get_right_border_squares():
            cell_occupied = self.grid.has_square_in(s.col + 1, s.row)
            if s.col == self.grid.cols - 1 or cell_occupied:
                return False
        self.figure.move_right()
        return True

    def move_left(self):
        for s in self.figure.get_left_border_squares():
            if s.col == 0 or self.grid.has_square_in(s.col - 1, s.row):
                return False
        self.figure.move_left()
        return True

    def rotate(self):
        new_coords = self._coords_after_rotation()
        self._prevent_moving_up_after_rotation(new_coords)
        self._rotation_wall_bump(new_coords)
        self._rotation_outside_grid_prevention(new_coords)
        if self._intersects_with_other_squares(new_coords):
            return
        for s in self.figure.squares:
            new_coord = new_coords[(s.col, s.row)]
            s.col = new_coord[0]
            s.row = new_coord[1]

    def rotate_randomly(self, move_to_corner: bool = False):
        if self.figure.figure_type == FigureType.BRICK:
            return
        for _ in range(random.randint(0, 3)):
            self.rotate()
        if move_to_corner:
            self.move_to_upper_left_corner()
        for s in self.figure.squares:
            s.recalc_coords()

    def move_to_upper_left_corner(self):
        while all(x.col > 0 for x in self.figure.squares):
            self.figure.move_left()
        while all(x.row > 0 for x in self.figure.squares):
            self.figure.move_up()
        while any(x.col < 0 for x in self.figure.squares):
            self.figure.move_right()
        while any(x.row < 0 for x in self.figure.squares):
            self.figure.move_down()

    def move_to_top(self):
        min_row = min(x.row > 0 for x in self.figure.squares)
        for x in self.figure.squares:
            x.row -= min_row

    def _coords_after_rotation(self):
        center_row = sum(
            s.row for s in self.figure.squares) // len(self.figure.squares)
        center_col = sum(
            s.col for s in self.figure.squares) // len(self.figure.squares)
        new_coords = {}
        for square in self.figure.squares:
            relative_row = square.row - center_row
            relative_col = square.col - center_col
            new_row = center_row - relative_col
            new_col = center_col + relative_row
            new_coords[(square.col, square.row)] = (new_col, new_row)
        return new_coords

    def _prevent_moving_up_after_rotation(self, new_coords):
        bottom = max(s.row for s in self.figure.squares)
        while max(c[1] for c in new_coords.values()) < bottom:
            for c in new_coords:
                new_coords[c] = (new_coords[c][0], new_coords[c][1] + 1)

    def _rotation_wall_bump(self, new_coords):
        while any(c[0] < 0 for c in new_coords.values()):
            for c in new_coords:
                new_coords[c] = (new_coords[c][0] + 1, new_coords[c][1])
        while any(c[0] > self.grid.cols - 1 for c in new_coords.values()):
            for c in new_coords:
                new_coords[c] = (new_coords[c][0] - 1, new_coords[c][1])

    def _rotation_outside_grid_prevention(self, new_coords):
        min_row = min(c[1] for c in new_coords.values())
        if min_row < 0:
            for c in new_coords:
                new_coords[c] = (new_coords[c][0], new_coords[c][1] - min_row)

    def intersects_with_other_squares(self):
        coords = [(c.col, c.row) for c in self.figure.squares]
        return any(self.grid.has_square_in(*c) for c in coords)

    def _intersects_with_other_squares(self, new_coords):
        return any(self.grid.has_square_in(*c) and c not in new_coords
                   for c in new_coords.values())
