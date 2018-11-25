"""
The connection history that stores history of all past connections
"""
from typing import List
from Genome import Genome
from Node import Node


class ConnectionHistory:
    """
    Stores the connection history of everything up to a specific connection.
    """
    starting_node: int
    ending_node: int
    innovation_number: int
    innovation_numbers: List[int]

    def __init__(self, start: int, end: int, num: int, nums: List[int]) -> None:
        """
        Initializes a new connection history entry.
        """
        self.starting_node, self.ending_node, self.innovation_number, self.innovation_numbers = start, end, num, nums

    def matches(self, genome: Genome, start: Node, end: Node) -> bool:
        """
        Returns whether or not the Genome <genome> matches the original genome that will call this function, and if
        the connection is the same between the nodes <start> and <end>.
        """
        if len(genome.genes) == len(self.innovation_numbers):
            if start.number == self.starting_node and end.number == self.ending_node:
                for gene in genome.genes:
                    if gene.innovation_number not in self.innovation_numbers:
                        return False
                return True

        return False
