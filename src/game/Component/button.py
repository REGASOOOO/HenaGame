from __future__ import annotations
from typing import Callable, Optional, Tuple
import pygame

"""
button.py

A reusable action button component for a (pygame) game.

Usage:

    button = Button(
        rect=(100, 100, 200, 60),
        text="Play",
        on_click=lambda: print("Play pressed")
    )

In your main loop:
    for event in pygame.event.get():
        button.handle_event(event)

    button.update()
    button.draw(screen)
"""



class Button:
    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        font: Optional[pygame.font.Font] = None,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (60, 60, 60),
        hover_color: Tuple[int, int, int] = (90, 90, 90),
        pressed_color: Tuple[int, int, int] = (40, 40, 40),
        border_color: Tuple[int, int, int] = (255, 255, 255),
        border_width: int = 2,
        corner_radius: int = 8,
        click_sound: Optional[pygame.mixer.Sound] = None,
        hotkey: Optional[int] = None,  # pygame.K_* constant
    ):
        """
        Create a button.

        rect: (x, y, w, h)
        text: label displayed
        on_click: callback with no arguments
        hotkey: optional pygame key code to trigger button
        """
        self.rect = pygame.Rect(rect)
        self._text = text
        self.on_click = on_click
        self.font = font or pygame.font.SysFont(None, int(self.rect.height * 0.5))
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.click_sound = click_sound
        self.hotkey = hotkey

        self._hover = False
        self._pressed = False
        self._dirty = True
        self._surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self._render_label()

    # Public API

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if value != self._text:
            self._text = value
            self._render_label()

    def set_action(self, action: Callable[[], None]) -> None:
        self.on_click = action

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._pressed
            self._pressed = False
            if was_pressed and self.rect.collidepoint(event.pos):
                self._trigger()
        elif event.type == pygame.KEYDOWN and self.hotkey is not None:
            if event.key == self.hotkey:
                self._trigger(visual_feedback=True)

    def update(self) -> None:
        pass  # Placeholder if you later need animations

    def draw(self, target_surface: pygame.Surface) -> None:
        if self._dirty:
            self._redraw()
        target_surface.blit(self._surface, self.rect.topleft)

    # Internal helpers

    def _trigger(self, visual_feedback: bool = False) -> None:
        if visual_feedback:
            self._pressed = True
            self._redraw()
            # Short-lived visual state could be handled externally
            self._pressed = False
        if self.click_sound:
            self.click_sound.play()
        if self.on_click:
            self.on_click()

    def _render_label(self) -> None:
        self._label_surface = self.font.render(self._text, True, self.text_color)
        self._dirty = True

    def _current_bg(self) -> Tuple[int, int, int]:
        if self._pressed:
            return self.pressed_color
        if self._hover:
            return self.hover_color
        return self.bg_color

    def _redraw(self) -> None:
        self._surface.fill((0, 0, 0, 0))
        bg = self._current_bg()
        pygame.draw.rect(
            self._surface,
            bg,
            self._surface.get_rect(),
            border_radius=self.corner_radius,
        )
        if self.border_width > 0:
            pygame.draw.rect(
                self._surface,
                self.border_color,
                self._surface.get_rect(),
                width=self.border_width,
                border_radius=self.corner_radius,
            )
        # Center label
        label_rect = self._label_surface.get_rect(center=self._surface.get_rect().center)
        self._surface.blit(self._label_surface, label_rect)
        self._dirty = False


# Simple manual test (run this file directly)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    clock = pygame.time.Clock()

    btn = Button(
        rect=(150, 100, 200, 60),
        text="Click Me",
        on_click=lambda: print("Button clicked"),
        hotkey=pygame.K_RETURN,
    )

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            btn.handle_event(ev)

        btn.update()
        screen.fill((30, 30, 30))
        btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()