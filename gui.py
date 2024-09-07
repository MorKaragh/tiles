from pygame import font, Surface
from game import TetrisGame


class StateScreen:

    @staticmethod
    def draw_loss(screen, game: TetrisGame):
        surf = Surface(screen.get_size())
        surf.fill((5, 17, 22))
        big_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 60)
        small_font = font.Font("fonts/Oldtimer-GOPpg.ttf", 30)
        main_text = big_font.render("Game over!", True, "White")
        score_text = small_font.render(f"score: {game.scoreboard.score}",
                                       True, "White")
        main_rect = main_text.get_rect(
            center=(screen.get_size()[0]/2, screen.get_size()[1]/2))
        score_rect = score_text.get_rect(
            center=(screen.get_size()[0]/2, 3*screen.get_size()[1]/4))
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
