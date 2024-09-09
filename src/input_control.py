import pygame

from src.game import GameState, TetrisGame, GameConfig


def process_pressed_keys(pressed, game, config):
    if (game.last_move_time > config.SIDE_MOVE_SPEED_FACTOR
            and game.side_move_delay > 0):
        game.last_move_time = 0
        if pressed[pygame.K_RIGHT]:
            game.movements.move_right()
        elif pressed[pygame.K_LEFT]:
            game.movements.move_left()
    if pressed[pygame.K_DOWN] and game.accelerate_fall:
        game.fall_speed_factor = 0


def _process_keydown(event, game: TetrisGame, config: GameConfig):
    if event.key in [pygame.K_UP, pygame.K_k]:
        game.movements.rotate()
    elif event.key in [pygame.K_DOWN, pygame.K_j]:
        game.accelerate_fall = True
    elif event.key in [pygame.K_RIGHT, pygame.K_l]:
        game.side_move_delay = -3
        game.movements.move_right()
    elif event.key in [pygame.K_LEFT, pygame.K_h]:
        game.side_move_delay = -3
        game.movements.move_left()
    elif event.key == pygame.K_ESCAPE:
        game.state = GameState.MENU
    elif event.key == pygame.K_SPACE:
        if game.state == GameState.PAUSE:
            game.state = GameState.RUNNING
        elif game.state == GameState.LOSS:
            game.reset()
        else:
            game.state = GameState.PAUSE


def process_events(events, game: TetrisGame, config: GameConfig):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            game.running = False
        elif event.type == pygame.KEYDOWN:
            _process_keydown(event, game, config)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                game.accelerate_fall = False
                game.fall_speed_factor = game.get_fall_speed_factor()
