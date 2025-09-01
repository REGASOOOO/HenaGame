from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
import pygame


class Screen(ABC):
    """Abstract screen interface.

    Lifecycle order: on_enter -> (handle_event/update/render)* -> on_exit
    """

    def __init__(self, manager: "ScreenManager") -> None:
        self.manager = manager

    # ---- Lifecycle hooks ----
    def on_enter(self, previous: Optional["Screen"]):  # pragma: no cover - simple hook
        pass

    def on_exit(self, next_screen: Optional["Screen"]):  # pragma: no cover
        pass

    # ---- Core API ----
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        ...


class ScreenManager:
    """Stack-based screen manager (allows push/pop for overlays, or switch)."""

    def __init__(self) -> None:
        self._stack: List[Screen] = []

    # ---- Properties ----
    @property
    def current(self) -> Optional[Screen]:
        return self._stack[-1] if self._stack else None

    # ---- Stack operations ----
    def push(self, screen: Screen) -> None:
        previous = self.current
        self._stack.append(screen)
        screen.on_enter(previous)

    def pop(self) -> Optional[Screen]:
        if not self._stack:
            return None
        top = self._stack.pop()
        next_screen = self.current
        top.on_exit(next_screen)
        return top

    def switch(self, screen: Screen) -> None:
        prev = self.pop()
        self.push(screen)
        # For explicitness; prev already had on_exit in pop

    # ---- Dispatch helpers ----
    def handle_event(self, event: pygame.event.Event) -> None:
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float) -> None:
        if self.current:
            self.current.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if self.current:
            self.current.render(surface)
