from gaming_grid import TetrisFigure, GridSquare


def test_get_bottom_border():
    squares = [
        GridSquare(0, 0, 10, 10),
        GridSquare(1, 0, 10, 10),
        GridSquare(1, 1, 10, 10),
        GridSquare(2, 1, 10, 10)
    ]
    figure = TetrisFigure(squares)
    assert figure
    assert len(figure.get_bottom_border_squares()) == 3
