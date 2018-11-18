"""
Class for background image
"""
import pygame


class Background:
    """
    Background for Mario Kart 2D game!
    """

    def __init__(self, path: str, x_cor, y_cor) -> None:
        """
        Initializes a background.
        """
        self.img = pygame.image.load(path)
        self.x_cor, self.y_cor = x_cor, y_cor
        self.speed = 0
        self.travelled = 0

    def move_background(self, x, y):
        """
        Move background to (x, y).
        """
        old_x, old_y = self.x_cor, self.y_cor
        self.x_cor, self.y_cor = x, y
        if old_y <= self.y_cor:
            self.travelled += self.y_cor - old_y
