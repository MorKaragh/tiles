import pygame

from src.game import GamingGrid, GameConfig

clock = pygame.time.Clock()

config = GameConfig()
grid = GamingGrid(config.GRID_COLS, config.GRID_ROWS)
pygame.init()
screen = pygame.display.set_mode((config.GRID_COLS * config.SQUARE_SIZE,
                                  config.GRID_ROWS * config.SQUARE_SIZE))
pygame.display.set_caption("Grid framework testing")
pygame.display.set_icon(pygame.image.load("../images/icon.png"))

running = True

total_lines = 0
with open("../grid_state.log", 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)

curr_debug_line = total_lines


def get_line_from_file(filename, line_number):
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if i + 1 == line_number:
                return line.strip()
        return None


curr_grid_state = get_line_from_file("../grid_state.log", curr_debug_line)


def get_next_state():
    global curr_debug_line
    global curr_grid_state
    prev_record = get_line_from_file("../grid_state.log", curr_debug_line)
    while curr_grid_state == prev_record:
        curr_debug_line -= 1
        prev_record = get_line_from_file("../grid_state.log", curr_debug_line)
    curr_grid_state = prev_record
    return prev_record


def get_prev_state():
    global curr_debug_line
    global curr_grid_state
    prev_record = get_line_from_file("../grid_state.log", curr_debug_line)
    while curr_grid_state == prev_record:
        curr_debug_line += 1
        prev_record = get_line_from_file("../grid_state.log", curr_debug_line)
    curr_grid_state = prev_record
    return prev_record


while running:
    clock.tick(20)
    screen.fill("White")

    grid.draw(screen)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        grid.set_state(get_next_state())
    elif pressed[pygame.K_RIGHT]:
        grid.set_state(get_prev_state())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(grid.__repr__())

    pygame.display.update()
