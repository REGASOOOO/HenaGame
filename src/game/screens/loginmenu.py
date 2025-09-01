from __future__ import annotations
try:  # Support package import and script run
    from ..Component.button import Button  # type: ignore
except Exception:  # pragma: no cover - fallback when run directly
    from game.Component.button import Button  # type: ignore

import pygame
from .screen_manager import Screen

class LoginMenuScreen(Screen):
    """Simple main menu screen.

    Keys:
      ENTER -> switch to gameplay
      ESC   -> quit application
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 64)
        self.small = pygame.font.SysFont(None, 28)
        self.blink_timer = 0.0
        self.show_press_start = True
        # Pre-create UI widgets
        self.button_login = Button(
            rect=(400 - 100, 200, 200, 60),
            text="Login",
            on_click=lambda: print("Login clicked"),
        )
    
    def handle_event(self, event: pygame.event.Event) -> None:  # pragma: no cover - real time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from .gameplay import GameplayScreen
                self.manager.switch(GameplayScreen(self.manager))
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    # Delegate to button
        self.button_login.handle_event(event)

    def update(self, dt: float) -> None:
        self.button_login.update()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 20, 35))
        title = self.font.render("HenaGame", True, (240, 240, 255))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 120))
        # Draw login button
        self.button_login.draw(surface)
        # Footer hint
        hint = self.small.render("ESC to Quit", True, (120, 125, 140))
        surface.blit(hint, (10, surface.get_height() - 30))
