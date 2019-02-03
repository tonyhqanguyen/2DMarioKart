"""
Obstacle class for racing game
"""
from random import choice
import pygame

bowser = "./bowser.png"
donkeykong = "./donkeykong.png"
toad = "./toad.png"
toadette = "./toadette.png"
yoshi = "./yoshi.png"
waluigi = "./waluigi.png"

images = [bowser, donkeykong, toad, toadette, yoshi, waluigi]


class Obstacle:
    """
    An obstacle on the road!
    """

    def __init__(self, x, y):
        """
        Initiates an obstacle
        """
        self.image = pygame.image.load(choice(images))
        self.x, self.y = x, y
        self.passed = False
        self.speed = 0
        self.size = self.image.get_rect().size
        self.created_new = False

    def pass_obstacle(self):
        """
        Sets the obstacle to indicate that it has been passed.
        """
        self.passed = True

    def move(self):
        """
        Move the obstacle vertically.
        """
        self.y += self.speed
