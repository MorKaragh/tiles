import pygame
from opponent_ai import move_opponent


def process_events(event, player, opponent):
    global running
    if event.type == pygame.QUIT:
        pygame.quit()
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_k]:
            move_opponent(player, opponent)
            player.move_up()
        elif event.key in [pygame.K_DOWN, pygame.K_j]:
            move_opponent(player, opponent)
            player.move_down()
        elif event.key in [pygame.K_RIGHT, pygame.K_l]:
            move_opponent(player, opponent)
            player.move_right()
        elif event.key in [pygame.K_LEFT, pygame.K_h]:
            move_opponent(player, opponent)
            player.move_left()
