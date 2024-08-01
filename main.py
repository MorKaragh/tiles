import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
