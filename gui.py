from pygame import font, Surface


class StateScreen:

    @staticmethod
    def draw_loss(screen):
        StateScreen._simple_text("Game over!", screen)

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
