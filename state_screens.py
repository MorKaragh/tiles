from global_config import SCREEN_SIZE
from pygame import font


class StateScreen:

    @staticmethod
    def draw_loss(screen):
        screen.fill("White")
        text = font.Font(None, 40).render("You lose!", True, "Black")
        rect = text.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2))
        screen.blit(text, rect)

    @staticmethod
    def draw_win(screen):
        screen.fill("White")
        text = font.Font(None, 40).render("You win!", True, "Black")
        rect = text.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2))
        screen.blit(text, rect)
