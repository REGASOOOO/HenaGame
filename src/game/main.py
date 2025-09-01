import pygame
import sys
import pathlib

# Robust import strategy supporting both:
#  - python -m src.game.main (preferred)
#  - python src/game/main.py  (fallback)
try:  # pragma: no cover - depends on invocation style
    from .screens import ScreenManager, LoginMenuScreen  # type: ignore
except Exception:  # noqa: BLE001 - broad so we can fallback gracefully
    # When executed as a plain script, ensure the parent of the package ("src") is on sys.path
    _GAME_DIR = pathlib.Path(__file__).resolve().parent
    _PARENT = _GAME_DIR.parent  # .../src
    if str(_PARENT) not in sys.path:
        sys.path.insert(0, str(_PARENT))
    from game.screens import ScreenManager, LoginMenuScreen  # type: ignore

WINDOW_SIZE = (800, 600)
FPS = 60


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("HenaGame")
    clock = pygame.time.Clock()

    manager = ScreenManager()
    manager.push(LoginMenuScreen(manager))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.render(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    run_game()
