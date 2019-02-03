"""
A player class
"""
from Genome import Genome
from typing import List
from obstacle import Obstacle


class Player:
    """
    A player of the game.
    """
    fitness: float
    brain: Genome
    replay: bool
    unadjusted_fitness: float
    lifespan: int
    best_score: int
    dead: bool
    score: int
    generation: int
    genome_inputs: int
    genome_outputs: int
    vision: List[float]
    decision: List[float]
    position_y: float
    position_x: float
    speed: float
    height: float
    width: float
    run_count: int
    replay_obstacles: List[Obstacle]
    local_obstacle_history: List[int]
    local_random_addition_history: List[int]
    history_counter: int
    local_obstacle_timer: int
    local_random_addition: int

    def __init__(self) -> None:
        """
        Initalizes a new player.
        """
        self.lifespan = 0
        self.best_score = 0
        self.generation = 0
        self.genome_inputs =
