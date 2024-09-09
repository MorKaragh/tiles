from src.gaming_grid import GamingGrid


def fill_multirow_with_break(grid: GamingGrid):
    for row in range(grid.rows - 1, grid.rows - 4, -2):
        for col in range(grid.cols - 1):
            grid.add_new_square(col, row, "Black")


def fill_bug_1(grid: GamingGrid):
    state = "7:19;8:19;6:19;9:19;5:19;5:18;6:18;6:17;3:18;3:17;4:19;4:18;1:18;2:19;0:19;1:19;5:17;4:17;6:16;5:16;0:18;0:17;1:17;1:16;2:18;2:17;2:16;3:16;9:17;9:16;9:18;9:15;8:17;8:16;8:18;8:15;4:16;4:15;5:15;5:14;3:14;4:14;2:15;3:15;5:13;4:13;3:13;3:12;0:16;0:15;1:15;1:14;9:12;9:13;9:14;8:14;5:0;6:1;4:1;5:1"
    grid.set_state(state)
    grid.squares = [s for s in grid.squares if s.row > 5]


def fill_tunnel(grid: GamingGrid):
    for i in range(5, grid.rows, 2):
       grid.add_new_square(3, i) 
       grid.add_new_square(7, i) 
