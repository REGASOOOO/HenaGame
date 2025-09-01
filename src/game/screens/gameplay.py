from __future__ import annotations

import pygame
from .screen_manager import Screen


class GameplayScreen(Screen):
    """Example gameplay screen with a moving square and pause/return support.

    Keys:
      ESC -> back to menu
      P   -> push a pause overlay (future extension)
    """

    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 32)
        self.rect = pygame.Rect(100, 100, 60, 60)
        self.vel = pygame.Vector2(180, 140)

    def handle_event(self, event: pygame.event.Event) -> None:  # pragma: no cover
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from .menu import MenuScreen
                self.manager.switch(MenuScreen(self.manager))

    def update(self, dt: float) -> None:
        # basic bouncing movement
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)
        surf = pygame.display.get_surface()
        if not surf:
            return
        w, h = surf.get_size()
        if self.rect.right >= w or self.rect.left <= 0:
            self.vel.x *= -1
        if self.rect.bottom >= h or self.rect.top <= 0:
            self.vel.y *= -1

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 25))
        pygame.draw.rect(surface, (80, 200, 250), self.rect, border_radius=8)
        txt = self.font.render("Gameplay - ESC for Menu", True, (230, 230, 240))
        surface.blit(txt, (10, 10))
