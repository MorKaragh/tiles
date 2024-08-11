import pygame
from opponent_ai import move_opponent


def process_events(event, game):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_k]:
            move_opponent(game.player, game.opponent)
            game.player.move_up()
        elif event.key in [pygame.K_DOWN, pygame.K_j]:
            move_opponent(game.player, game.opponent)
            game.player.move_down()
        elif event.key in [pygame.K_RIGHT, pygame.K_l]:
            move_opponent(game.player, game.opponent)
            game.player.move_right()
        elif event.key in [pygame.K_LEFT, pygame.K_h]:
            move_opponent(game.player, game.opponent)
            game.player.move_left()
        elif event.key == pygame.K_SPACE:
            if game.state in ["WIN", "LOSS"]:
                game.reset()
