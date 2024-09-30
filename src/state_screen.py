from src.game import TetrisGame
from pygame import Surface, font
from src.records import load_for_player


class StateScreen:

    @staticmethod
    def draw_loss(screen, game: TetrisGame):
        surf = Surface(screen.get_size())
        surf.fill((5, 17, 22))
        big_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 60)
        small_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 30)
        main_text = big_font.render("Finished", True, "White")
        score_text = small_font.render(f"score: {game.scoreboard.score}",
                                       True, "White")
        curr_record = load_for_player(game.config.PLAYER)
        record_text = small_font.render(f"max score: {curr_record}",
                                        True, "White")
        main_rect = main_text.get_rect(
            center=(screen.get_size()[0]/2, 2*screen.get_size()[1]/5))
        score_rect = score_text.get_rect(
            center=(screen.get_size()[0]/2, 3*screen.get_size()[1]/5))
        record_rect = record_text.get_rect(
            center=(screen.get_size()[0]/2, 4*screen.get_size()[1]/5))
        surf.blit(main_text, main_rect)
        surf.blit(score_text, score_rect)
        surf.blit(record_text, record_rect)
        screen.blit(surf, (0, 0))

    @staticmethod
    def draw_opponent_loss(screen, score: str):
        surf = Surface(screen.get_size())
        surf.fill((5, 9, 22))
        big_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 60)
        small_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 30)
        main_text = big_font.render("Finished", True, "White")
        score_text = small_font.render(f"score: {score}", True, "White")
        main_rect = main_text.get_rect(
            center=(screen.get_size()[0]/2, 2*screen.get_size()[1]/5))
        score_rect = score_text.get_rect(
            center=(screen.get_size()[0]/2, 3*screen.get_size()[1]/5))
        surf.blit(main_text, main_rect)
        surf.blit(score_text, score_rect)
        screen.blit(surf, (0, 0))

    @staticmethod
    def draw_win(screen):
        StateScreen._simple_text("You win!", screen)

    @staticmethod
    def _simple_text(text: str, screen: Surface):
        surf = Surface(screen.get_size())
        surf.fill((5, 17, 22))
        text = font.Font("fonts/Oldtimer-GOPpg.ttf",
                         60).render(text, True, "White")
        rect = text.get_rect(
            center=(screen.get_size()[0]/2, screen.get_size()[1]/2))
        surf.blit(text, rect)
        screen.blit(surf, (0, 0))
