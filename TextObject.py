from typing import Tuple

import pygame

from GameSettings import *


class TextObject:
    
    def __init__(
            self,
            text: str = "Empty Text",
            font_size: int = 18,
            color: Colors = Colors.black,
            position: Tuple[float, float] = (0, 0)
        ) -> None:
        
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position

        self.drawable_text = self._get_drawable_text()
        self.rect = self._get_rect()

    def _get_drawable_text(self) -> pygame.Surface:
        """
        Returns text as pygame.Surface object which can be rendered on screen
        """

        font = pygame.font.SysFont("arial", self.font_size)
        return font.render(self.text, True, self.color)


    def _get_rect(self) -> pygame.Rect:
        """
        Returns pygame.Rect object for given text
        """
        rect = pygame.Rect(0, 0, self.drawable_text.get_width(), self.drawable_text.get_height())

        rect.centerx, rect.centery = self.position

        return rect

    def set_new_text(self, new_text: str) -> None:
        self.text = new_text

        self.drawable_text = self._get_drawable_text()
        self.rect = self._get_rect()

    def set_new_pos(self, new_position: Tuple[int, int]) -> None:
        self.rect.x, self.rect.y = new_position


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws text to screen at given position
        """
        screen.blit(self.drawable_text, self.rect)
