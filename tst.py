from gaming_grid import GridSquare, GamingGrid

grid = GamingGrid(3, 3)
grid.add_new_square(0, 0)

assert grid.has_square_in(0, 0)
assert not grid.has_square_in(1, 1)

for row in grid.squares:
    for square in row:
        if square:
            print(type(square))
            square.draw(None)
