"""
Mario class
"""
import pygame
from obstacle import Obstacle
from typing import List


class Mario:
    """
    Representation of Mario!
    """

    def __init__(self, x_cor, y_cor, obstacles: List[Obstacle]) -> None:
        """
        Initializes an instance of Mario.
        """
        self.obstacles = obstacles
        self.distance_to_obstacles = {}
        for obstacle in obstacles:
            self.distance_to_obstacles[obstacle] = (0, 0, 0)
        self.update_obstacle_distance(obstacles)

        self.image = pygame.image.load("/Users/tonynguyen/Desktop/ML/MachineLearning/evolution/mario.png")
        self.x_cor, self.y_cor = x_cor, y_cor
        self.speed = 0
        self.acceleration = 0
        self.hor_acceleration = 0
        self.hor_speed = 0
        self.size = self.image.get_rect().size

    def move_mario(self, x, y) -> None:
        """
        Moves Mario to the designated location
        """
        self.x_cor, self.y_cor = x, y

    def update_obstacle_distance(self, new_obstacles: List[Obstacle]) -> None:
        """
        Update the all the distances between Mario and the obstacles.
        """
        self.obstacles = new_obstacles
        for obstacle in self.obstacles:
            obstacle_rect = obstacle.image.get_rect()
            obstacle_y_end = obstacle.y + obstacle_rect.size[1]
            obstacle_x_left = obstacle.x
            obstacle_x_right = obstacle.x + obstacle_rect.size[0]
            self.distance_to_obstacles[obstacle] = (obstacle_x_left, obstacle_x_right, obstacle_y_end)
