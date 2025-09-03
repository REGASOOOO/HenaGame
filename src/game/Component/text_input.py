from __future__ import annotations
from typing import Callable, Optional, Tuple
import pygame

class TextInput:
    """Simple text input field supporting password masking and submit callback."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        *,
        placeholder: str = "",
        text: str = "",
        password: bool = False,
        on_submit: Optional[Callable[[str], None]] = None,
        font: Optional[pygame.font.Font] = None,
        text_color: Tuple[int, int, int] = (235, 235, 235),
        placeholder_color: Tuple[int, int, int] = (140, 140, 150),
        bg_color: Tuple[int, int, int] = (55, 55, 65),
        focus_color: Tuple[int, int, int] = (75, 75, 95),
        border_color: Tuple[int, int, int] = (255, 255, 255),
        border_width: int = 2,
        corner_radius: int = 6,
        max_length: int = 32,
    ):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self._text = text
        self.password = password
        self.on_submit = on_submit
        self.font = font or pygame.font.SysFont(None, int(self.rect.height * 0.55))
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.bg_color = bg_color
        self.focus_color = focus_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.max_length = max_length
        self.focused = False
        self._cursor_visible = True
        self._cursor_timer = 0.0
        self._cursor_interval = 0.5

    @property
    def value(self) -> str:
        return self._text

    def set_value(self, value: str) -> None:
        self._text = value[: self.max_length]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_RETURN:
                if self.on_submit:
                    self.on_submit(self._text)
            elif event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self._text) < self.max_length:
                    self._text += ch

    def update(self, dt: float) -> None:
        if self.focused:
            self._cursor_timer += dt
            if self._cursor_timer >= self._cursor_interval:
                self._cursor_timer = 0.0
                self._cursor_visible = not self._cursor_visible
        else:
            self._cursor_visible = False
            self._cursor_timer = 0.0

    def draw(self, target_surface: pygame.Surface) -> None:
        bg = self.focus_color if self.focused else self.bg_color
        pygame.draw.rect(target_surface, bg, self.rect, border_radius=self.corner_radius)
        if self.border_width:
            pygame.draw.rect(
                target_surface,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.corner_radius,
            )
        if self._text:
            display = ("*" * len(self._text)) if self.password else self._text
            color = self.text_color
        else:
            display = self.placeholder
            color = self.placeholder_color
        text_surface = self.font.render(display, True, color)
        text_pos = (self.rect.x + 10, self.rect.y + (self.rect.height - text_surface.get_height()) // 2)
        target_surface.blit(text_surface, text_pos)
        if self.focused and self._cursor_visible:
            cursor_x = text_pos[0] + text_surface.get_width() + 2
            cursor_y = text_pos[1]
            cursor_h = text_surface.get_height()
            pygame.draw.rect(target_surface, self.text_color, (cursor_x, cursor_y, 2, cursor_h))
