from global_config import SCREEN_SIZE
from pygame import font, Surface


class StateScreen:

    @staticmethod
    def draw_loss(screen):
        StateScreen._simple_text("You lose!", screen)

    @staticmethod
    def draw_win(screen):
        StateScreen._simple_text("You win!", screen)

    @staticmethod
    def _simple_text(text, screen):
        surf = Surface((SCREEN_SIZE, SCREEN_SIZE))
        surf.fill("Grey")
        text = font.Font(None, 40).render(text, True, "Black")
        rect = text.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2))
        surf.blit(text, rect)
        screen.blit(surf, (0, 0))
