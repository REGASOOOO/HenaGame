from __future__ import annotations

import pygame
from .screen_manager import Screen


class MenuScreen(Screen):
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

    def handle_event(self, event: pygame.event.Event) -> None:  # pragma: no cover - real time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from .gameplay import GameplayScreen
                self.manager.switch(GameplayScreen(self.manager))
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float) -> None:
        self.blink_timer += dt
        if self.blink_timer >= 0.6:
            self.blink_timer = 0.0
            self.show_press_start = not self.show_press_start

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 20, 35))
        title = self.font.render("HenaGame", True, (240, 240, 255))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 120))
        if self.show_press_start:
            msg = self.small.render("Press ENTER to Start", True, (180, 190, 210))
            surface.blit(msg, (surface.get_width() // 2 - msg.get_width() // 2, 300))
        hint = self.small.render("ESC to Quit", True, (120, 125, 140))
        surface.blit(hint, (10, surface.get_height() - 30))
