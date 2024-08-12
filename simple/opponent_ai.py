from grid_objects import GridSquare


def move_opponent(player: GridSquare, opponent: GridSquare):
    diff_x = player.x - opponent.x
    diff_y = player.y - opponent.y
    if diff_x < 0 and abs(diff_x) >= abs(diff_y):
        opponent.move_left()
    elif diff_x > 0 and abs(diff_x) >= abs(diff_y):
        opponent.move_right()
    elif diff_y < 0 and abs(diff_x) < abs(diff_y):
        opponent.move_up()
    elif diff_y > 0 and abs(diff_x) < abs(diff_y):
        opponent.move_down()
