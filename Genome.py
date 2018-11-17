"""
The Neural Network
"""
from typing import List, Union
from random import choice, uniform


class Genome:
    """
    The Neural Network (game) of the game.
    """
    genes: List[Gene]
    nodes: List[Nodes]
    inputs: int
    outputs: int
    layers: int
    next_node: int
    bias_node: int
    network: List[Nodes]
    is_crossover: bool

    def __init__(self, inputs: int, outputs: int, is_crossover: bool=False) -> None:
        """
        Initializes a genome.
        """
        self.inputs, self.outputs = inputs, outputs
        self.genes, self.nodes = [], []
        self.layers = 2
        self.next_node = 0
        self.bias_node = self.next_node
        self.network = []
        self.is_crossover = is_crossover
        self.initialize_nodes()

    def initialize_nodes(self) -> None:
        """
        Inialize the node structure of the original neural network.
        """

        # input nodes
        for index in range(self.inputs):
            self.nodes.append(Node(index))
            self.next_node += 1
            self.nodes[index].layer = 0

        # output nodes
        for index in range(self.outputs):
            self.nodes.append(Node(index + self.inputs))
            self.next_node += 1
            self.nodes[index + self.inputs].layer = 1

        self.nodes.append(Node(self.next_node))
        self.bias_node = self.next_node
        self.next_node += 1
        self.nodes[self.bias_node].layer = 0

    def get_node(self, node_number: int) -> Union[Node, None]:
        """
        Return the node with node number <node_number> if it exists, else return None.
        """
        for node in self.nodes:
            if node.number == node_number:
                return node

    def connect_nodes(self) -> None:
        """
        Connect the nodes so that each node has reference to all its outgoing connections.
        """

        # clear the current connections
        for node in self.nodes:
            node.outgoing_connections = []

        # for each gene, add the gene to the starting_node of the gene so the starting_node has reference to its
        # outgoing profile
        for gene in self.genes:
            gene.starting_node.outgoing_connections.append(gene)

    def generate_neural_network(self) -> None:
        """
        Generate the neural network
        """
        self.connect_nodes()
        for layer in range(self.layers):
            for node in self.nodes:
                if node.layer == layer:
                    self.network.append(node)

    def mutate_by_node_addition(self, history: List) -> None:
        """
        Mutate the neural network by:
            1. choose a random gene, then disable it
            2. create 2 new connections: + 1 between starting_node of disabled gene and a new added node
                                         + 1 between the new added node and the ending_node of disabled gene
        """
        # randomly add a connection between 2 genes if there are currently no connections between any genes
        if len(self.genes) == 0:
            self.add_connections(history)
            # enough mutation for now!
            return

        # pick a random gene to disable
        gene_to_disable = choice(self.genes)

        while gene_to_disable.starting_node is not self.nodes[self.bias_node] and len(self.genes) != 1:
            gene_to_disable = choice(self.genes)

        gene_to_disable.enabled = False

        new_node_number = self.next_node
        self.nodes.append(Node(new_node_number))
        self.get_node(new_node_number).layer = gene_to_disable.starting_node.layer + 1
        self.next_node += 1

        new_node = self.get_node(new_node_number)

        # add a new connection from starting_node of gene_to_disable to new node with weight 1
        new_inno_num = self.get_inno_num(history, gene_to_disable.starting_node, new_node)
        self.genes.append(
            Gene(
                gene_to_disable.starting_node,
                new_node,
                1,
                new_inno_num)
        )

        # add a new connection from new node to ending_node of gene_to_disable with weight of the disabled connection
        new_inno_num = self.get_inno_num(history, new_node, gene_to_disable.ending_node)
        self.genes.append(
            Gene(
                new_node,
                gene_to_disable.ending_node,
                gene_to_disable.weight,
                new_inno_num)
        )

        # add connection from the bias node to the new node with a weight of 0
        new_inno_num = self.get_inno_num(history, self.get_node(self.bias_node), self.get_node(new_node_number))
        self.genes.append(
            Gene(
                self.get_node(self.bias_node),
                new_node,
                0,
                new_inno_num)
        )

        # ensure that if the layer of the new node is the same as the layer of the disabled gene's ending node then
        # the layers of all nodes with layer >= than the the new node's layer need to be incremented
        for node in self.nodes:
            if node.layer >= new_node.layer:
                node.layer += 1

        # properly reconnect the nodes of the new neural network
        self.connect_nodes()

    def add_connection(self, history) -> None:
        """
        Randomly add a connection between 2 nodes that are not yet connected.
        """
        if self.fully_connected():
            print("Cannot connect the neural network any further")
            return

        node1 = choice(self.nodes)
        node2 = choice(self.nodes)

        while node1.layer == node2.layer or node1.is_connected_to(node2):
            node1 = choice(self.nodes)
            node2 = choice(self.nodes)

        # we want node1's layer to be < node2's layer
        temp = None
        if node1.layer > node2.layer:
            temp = node2
            node1 = node2
            node2 = temp

        new_inno_num = self.get_inno_num(history, node1, node2)
        # add the new connection with a random weight
        self.genes.append(Gene(node1, node2, uniform(-1, 1), new_inno_num))
        self.connect_nodes()

    def fully_connected(self) -> bool:
        """
        Return true if all the nodes in the neural network are connected to one another. Return false otherwise.
        """
        maximum_connections = 0
        node_in_each_layer = [0 for _ in range(self.layers)]

        # the number of nodes in each layer
        for node in self.nodes:
            node_in_each_layer[node.layer] += 1

        # the maximum number of connections between 1 layer and the next is the number of nodes in the starting layer
        # times the number of nodes in the ending layer
        for starting_layer in range(self.layers - 1):
            num_avail_nodes = sum(node_in_each_layer[starting_layer + 1:])
            maximum_connections += num_avail_nodes

        if maximum_connections == len(self.genes):
            return True

        return False

    def get_inno_num(self, history, starting_node: Node, ending_node: Node) -> int:
        """
        Return the innovation number that matches the connection between <starting_node> and <ending_node>. If such a
        connection already exists within <history>, returns the corresponding innovation that has been previously
        created. If not, create a new and unique innovation number to represent the new connection.
        """
        new_connection = True
        innovation_nos = [connection.innovation_number for connection in history]
        innovation_no = max(innovation_nos) + 1

        for connection in history:
            if connection.matches(self, starting_node, ending_node):
                new_connection = False
                innovation_no = connection.innovation_number

        new_inno_nums = []
        if new_connection:
            new_inno_nums = [gene.innovation_number for gene in self.genes]

        history.append(ConnectionHistory(starting_node.number, ending_node.number, innovation_no, new_inno_nums))

        return innovation_no

    def fully_mutate(self, history) -> None:
        """
        Mutate the genome!
        """
        # if there is no gene connection, add one
        if len(self.genes) == 0:
            self.add_connection(history)

        roll1 = uniform(0, 1)
        # 80% chance that the weights within a genome is mutated
        if roll1 < 0.8:
            for gene in self.genes:
                gene.mutate_weight()

        roll2 = uniform(0, 1)
        # 8% chance of adding a random new connection
        if roll2 < 0.08:
            self.add_connection(history)

        roll3 = uniform(0, 1)
        # 2% chance of adding a node
        if roll3 < 0.02:
            self.mutate_by_node_addition(history)

    def crossover(self, spouse: "Genome") -> "Genome":
        """
        Returns the new genome that is the product of the cross over between the current genome and <spouse>.
        """
        offspring = Genome(self.inputs, self.outputs, True)
        offspring.genes, offspring.nodes = [], []
        offspring.layers = self.layers
        offspring.next_node = self.next_node
        offspring.bias_node = self.bias_node

        inheriting_genes = []
        gene_statuses = []
        for gene in self.genes:
            inherit_enabled = True
            spouse_gene_index = self.matching_gene(spouse, gene.innovation_number)
            if spouse_gene_index != -1:
                spouse_gene = spouse.genes[spouse_gene_index]
                # if either the current genome's gene is disabled or the spouse's gene is disabled
                if not (gene.enabled and spouse_gene.enabled):
                    # 75% chance of having this gene disabled in the offspring
                    if uniform(0, 1) < 0.75:
                        inherit_enabled = False

                # 50/50 chance of getting the current genome's gene or the spouse's gene
                if uniform(0, 1) < 0.5:
                    inheriting_genes.append(gene)
                else:
                    inheriting_genes.append(spouse_gene)

            # if the gene is not found in the spouse's genes then add it to the offspring as a disjoint gene
            else:
                inheriting_genes.append(gene)
                inherit_enabled = gene.enabled
            gene_statuses.append(inherit_enabled)

        # inherit all the nodes of this genome to the offspring's genome
        offspring.nodes = [node.clone() for node in self.nodes]

        # clone the connections into the offspring's connections
        for info in zip(inheriting_genes, gene_statuses):
            gene_to_add = info[0].clone
            gene_to_add.enabled = info[1]
            offspring.genes.append(gene_to_add)

        offspring.connect_nodes()
        return offspring

    def matching_gene(self, spouse: "Genome", inno_num: int) -> int:
        """
        Return the index of the gene with the innovation number <inno_num> within <spouse>'s gene, if it exists. Return
        -1 if it does not exist.
        """
        for gene in spouse.genes:
            if gene.innovation_number == inno_num:
                return spouse.genes.index(gene)

        return -1

    def clone(self) -> "Genome":
        """
        Return a clone of this genome.
        """
        clone = Genome(self.inputs, self.outputs)
        clone.nodes = [node.clone() for node in self.nodes]
        clone.genes = [gene.clone() for gene in self.genes]
        clone.layers = self.layers
        clone.next_node = self.next_node
        clone.bias_node = self.bias_node
        clone.is_crossover = self.is_crossover

        return clone
