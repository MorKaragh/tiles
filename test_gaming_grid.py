from gaming_grid import TetrisFigure, GridSquare

"""
    .......
    ..OO...
    ...OO..
    .......
"""
squares = [
    GridSquare(0, 0, 10, 10),
    GridSquare(1, 0, 10, 10),
    GridSquare(1, 1, 10, 10),
    GridSquare(2, 1, 10, 10)
]


def test_get_bottom_border():
    figure = TetrisFigure(squares)
    assert figure
    assert len(figure.get_bottom_border_squares()) == 3


def test_get_left_border():
    figure = TetrisFigure(squares)
    assert figure
    assert len(figure.get_left_border_squares()) == 2


def test_get_right_border():
    figure = TetrisFigure(squares)
    assert figure
    assert len(figure.get_right_border_squares()) == 2
