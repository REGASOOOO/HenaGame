from __future__ import annotations
from urllib import response
try:  # Support package import and script run
    from ..Component import Button, TextInput  # type: ignore
except Exception:  # pragma: no cover
    from game.Component import Button, TextInput  # type: ignore

import pygame
import requests
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
        center_x = 400
        self.input_username = TextInput(
            rect=(center_x - 150, 180, 300, 50),
            placeholder="Username",
        )
        self.input_password = TextInput(
            rect=(center_x - 150, 250, 300, 50),
            placeholder="Password",
            password=True,
        )

        def attempt_login(_: str | None = None) -> None:
            # Adjust attr name if not 'value'
            username = getattr(self.input_username, "value", "")
            password = getattr(self.input_password, "value", "")
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/auth/login",
                    json={"username": username, "password": password},
                )
                if resp.status_code == 200:
                    print("Login successful")
                else:
                    print(f"Login failed ({resp.status_code})")
            except requests.RequestException as e:
                print(f"Login error: {e}")

        self.button_login = Button(
            rect=(center_x - 100, 330, 200, 60),
            text="Login",
            on_click=lambda: attempt_login(),
        )
        self.input_password.on_submit = attempt_login
        self.input_username.focused = True
    
    def handle_event(self, event: pygame.event.Event) -> None:  # pragma: no cover - real time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from .gameplay import GameplayScreen
                self.manager.switch(GameplayScreen(self.manager))
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # Delegate to widgets
        self.input_username.handle_event(event)
        self.input_password.handle_event(event)
        self.button_login.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            # Toggle focus between inputs
            if self.input_username.focused:
                self.input_username.focused = False
                self.input_password.focused = True
            elif self.input_password.focused:
                self.input_password.focused = False
                self.input_username.focused = True
            else:
                self.input_username.focused = True

    def update(self, dt: float) -> None:
        self.input_username.update(dt)
        self.input_password.update(dt)
        self.button_login.update()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 20, 35))
        title = self.font.render("HenaGame", True, (240, 240, 255))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 120))
        # Draw widgets
        self.input_username.draw(surface)
        self.input_password.draw(surface)
        self.button_login.draw(surface)
        # Footer hint
        hint = self.small.render("ESC to Quit", True, (120, 125, 140))
        surface.blit(hint, (10, surface.get_height() - 30))
