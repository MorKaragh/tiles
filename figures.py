import random
from gaming_grid import GridSquare, GamingGrid
from typing import List


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

    def random(self, col: int, row: int) -> TetrisFigure:
        funcs = [self.brick, self.L, self.J, self.T, self.S, self.Z, self.line]
        choise = random.choice(funcs)
        return choise(col, row)

    def brick(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col + 1, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def L(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 2, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 2, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def J(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 2, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col - 1, row + 2, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def S(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col + 1, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 2, row + 1, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def Z(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col + 2, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def T(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col + 2, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row + 1, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 1, row + 1, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)

    def line(self, col: int, row: int) -> TetrisFigure:
        squares = [GridSquare(col + 1, row, self.col_max, self.row_max,
                              self.square_size),
                   GridSquare(col + 2, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col, row, self.col_max,
                              self.row_max, self.square_size),
                   GridSquare(col + 3, row, self.col_max, self.row_max,
                              self.square_size)]
        return TetrisFigure(squares)


class FigureMovement:

    @staticmethod
    def move_down(figure: TetrisFigure, grid: GamingGrid):
        for s in figure.get_bottom_border_squares():
            if s.row == grid.rows - 1 or grid.has_square_in(s.col, s.row + 1):
                return False
        figure.move_down()
        return True

    @staticmethod
    def fall_down(figure: TetrisFigure, grid: GamingGrid):
        while FigureMovement.move_down(figure, grid):
            pass

    @staticmethod
    def move_figure_right(figure: TetrisFigure, grid: GamingGrid):
        for s in figure.get_right_border_squares():
            if s.col == grid.cols - 1 or grid.has_square_in(s.col + 1, s.row):
                return False
        figure.move_right()
        return True

    @staticmethod
    def move_figure_left(figure: TetrisFigure, grid: GamingGrid):
        pass
        for s in figure.get_left_border_squares():
            if s.col == 0 or grid.has_square_in(s.col - 1, s.row):
                return False
        figure.move_left()
        return True

    @staticmethod
    def rotate(figure: TetrisFigure, grid: GamingGrid):
        bottom = max(s.row for s in figure.squares)
        center_row = sum(s.row for s in figure.squares) // len(figure.squares)
        center_col = sum(s.col for s in figure.squares) // len(figure.squares)
        new_coords = {}
        for square in figure.squares:
            relative_row = square.row - center_row
            relative_col = square.col - center_col
            new_row = center_row - relative_col
            new_col = center_col + relative_row
            new_coords[(square.col, square.row)] = (new_col, new_row)
        while max(c[1] for c in new_coords.values()) < bottom:
            for c in new_coords:
                new_coords[c] = (new_coords[c][0], new_coords[c][1] + 1)
        if any([grid.has_square_in(*c) and c not in new_coords
                for c in new_coords.values()]):
            return
        for s in figure.squares:
            new_coord = new_coords[(s.col, s.row)]
            s.col = new_coord[0]
            s.row = new_coord[1]
