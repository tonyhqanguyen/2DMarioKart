"""
The Gene class which represents connections
"""
from Node import Node
from random import gauss, uniform


class Gene:
    """
    A gene that represents the connection between 2 nodes.
    """
    starting_node: Node
    ending_node: Node
    weight: float
    enabled: bool
    innovation_number: int

    def __init__(self, starting_node: Node, ending_node: Node, weight: float, no: int) -> None:
        """
        Initializes a gene.
        """
        self.starting_node, self.ending_node, self.weight, self.innovation_number = \
            starting_node, ending_node, weight, no
        self.enabled = True

    def mutate_weight(self) -> None:
        """
        Mutate the weight of this gene
        """
        if uniform(0, 1) < 0.1:
            self.weight = uniform(-1, 1)
        else:
            self.weight += gauss(0, 1)/50
            if self.weight > 1:
                self.weight = 1
            elif self.weight < -1:
                self.weight = -1

    def clone(self, starting_node: Node, ending_node: Node) -> "Gene":
        """
        Return a clone of this gene.
        """
        clone = Gene(starting_node, ending_node, self.weight, self.innovation_number)
        clone.enabled = self.enabled

        return clone
