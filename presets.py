from gaming_grid import GamingGrid


def fill_multirow_with_break(grid: GamingGrid):
    for row in range(grid.rows - 1, grid.rows - 4, -2):
        for col in range(grid.cols - 1):
            grid.add_new_square(col, row, "Black")
