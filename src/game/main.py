import pygame
import sys

WINDOW_SIZE = (800, 600)
FPS = 60


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Game Skeleton")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 40))
        text = font.render("Hello Pygame Skeleton", True, (200, 220, 255))
        screen.blit(text, (50, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    run_game()
