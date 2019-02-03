"""
Node class that is used in the Genome class.
"""
from typing import List
from math import exp


class Node:
    """
    A node in the neural network.
    """
    number: int
    input_sum: float
    output_value: float
    outgoing_connections: List[Gene]
    layer: int

    def __init__(self, number: int) -> None:
        """
        Initializes a node.
        """
        self.number = number
        self.input_sum, self.output_value = 0, 0
        self.outgoing_connections = []
        self.layer = 0

    def engage(self) -> None:
        """
        For each node that this node is connected to, this node will send its output to the connecting nodes
        """
        if self.layer != 0:
            self.output_value = 1 + exp(-4.9 * self.input_sum)

        for outgoing_connection in self.outgoing_connections:
            if outgoing_connection.enabled:
                # The weighted output of this node is added to the input sum of the outgoing connection
                outgoing_connection.ending_node.input_sum += outgoing_connection.weight * self.output_value

    def is_connected_to(self, node: "Node") -> bool:
        """
        Return whether or not this node is connected to <node>.
        """
        if self.layer == node.layer:
            return False

        if self.layer < node.layer:
            for outgoing_connection in node.outgoing_connections:
                if outgoing_connection.ending_node == self:
                    return True
        else:
            for outgoing_connection in self.outgoing_connections:
                if outgoing_connection.ending_node == node:
                    return True

        return False

    def clone(self) -> "Node":
        """
        Return a clone of this node.
        """
        clone = Node(self.number)
        clone.layer = self.layer
        return clone
