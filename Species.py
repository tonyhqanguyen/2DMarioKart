"""
Species class
"""
from typing import List, Union
from random import uniform
from Genome import Genome
from ConnectionHistory import ConnectionHistory
from Player import Player


class Species:
    """
    A species with distinct properties.
    """
    players: List[Player]
    best_fitness: float
    champion: Player
    average_fitness: float
    staleness: int
    rep: Genome
    excess_coefficient: float
    weight_difference_coefficient: float
    compatibility_threshold: float

    def __init__(self, player: Union[None, Player]=None) -> None:
        """
        Initializes a new species.
        """
        self.best_fitness, self.average_fitness, self.staleness, self.excess_coefficient, \
            self.weight_difference_coefficient, self.compatibility_threshold = 0, 0, 0, 1, 0.5, 3
        if player is not None:
            self.players.append(player)
            self.best_fitness = player.fitness
            self.rep = player.brain.clone()
            self.champion = player.clone_for_replay()

    def are_same_species(self, genome: Genome) -> bool:
        """
        Return whether or not <genome> is in this species.
        """
        # the number of excess & disjoint genes between the genome and this species' rep
        excess_and_disjoint = self.get_excess_disjoint(genome, self.rep)

        # the average weight difference between the matching genes
        average_weight_difference = self.average_weight_difference(genome, self.rep)

        gene_normalizer = len(genome.genes) - 20
        if gene_normalizer < 1:
            gene_normalizer = 1

        compatibility = (self.excess_coefficient * excess_and_disjoint/gene_normalizer) + \
                        (self.weight_difference_coefficient * average_weight_difference)

        return self.compatibility_threshold > compatibility

    def add_to_species(self, player: Player) -> None:
        """
        Add a new player to the species.
        """
        self.players.append(player)

    def get_excess_disjoint(self, genome1: Genome, genome2: Genome) -> float:
        """
        Return the number of excess and disjoint genes between <genome1> and <genome2>
        """
        matching = 0.0
        for gene1 in genome1.genes:
            for gene2 in genome2.genes:
                if gene1.innovation_number == gene2.innovation_number:
                    matching += 1

        return len(genome1.genes) + len(genome2.genes) - 2 * matching

    def average_weight_difference(self, genome1: Genome, genome2: Genome) -> float:
        """
        Returns the average weight difference between matching genes for <genome1> and <genome2>
        """
        if len(genome1.genes) == 0 or len(genome2.genes) == 0:
            return 0

        matching, total_difference = 0, 0
        for gene1 in genome1.genes:
            for gene2 in genome2.genes:
                if gene1.innovation_number == gene2.innovation_number:
                    matching += 1
                    total_difference += abs(gene1.weight - gene2.weight)
                    break

        if matching == 0:
            return 100

        return total_difference/matching

    def sort_species(self) -> None:
        """
        Sort the species by fitness.
        """
        sorted_players = []
        players = [player for player in self.players]
        fitness = [player.fitness for player in self.players]
        while players != []:
            max_fitness = max(fitness)
            index = fitness.index(max_fitness)
            sorted_players.append(players.pop(index))
            fitness.pop(index)

        self.players.clear()
        for player in sorted_players:
            self.players.append(player)

        if self.players == []:
            self.staleness = 0
        else:
            best_player = self.players[0]
            if best_player.fitness > self.best_fitness:
                self.staleness = 0
                self.best_fitness = best_player.fitness
                self.rep = best_player.brain.clone()
                self.champion = best_player.clone_for_replay()
            else:
                self.staleness += 1

    def set_average(self) -> None:
        """
        Set the average fitness of the species.
        """
        total = 0
        for player in self.players:
            total += player.fitness

        self.average_fitness = total/(len(self.players)) if self.players != [] else 0

    def make_offsprings(self, history: List[ConnectionHistory]) -> Player:
        """
        Returns the offspring that is the result of 1 or more players of this species.
        """
        offspring = None
        if uniform(0, 1) < 0.25:
            offspring = self.select_player().clone()
        else:
            parent1 = self.select_player()
            parent2 = self.select_player()

            if parent1.fitness < parent2.fitness:
                offspring = parent2.crossover(parent1)
            else:
                offspring = parent1.crossover(parent2)

        offspring.brain.mutate(history)
        return offspring

    def select_player(self) -> Player:
        """
        Select a player from all the players based on the fitness
        """
        fitness = 0
        for player in self.players:
            fitness += player.fitness

        random = uniform(0, fitness)
        random_fitness = 0
        for player in self.players:
            random_fitness += player.fitness
            if random_fitness > random:
                return player

    def massacre(self) -> None:
        """
        Kill off the bottom half of the species.
        """
        for player in self.players[len(self.players) // 2 + 1:]:
            self.players.remove(player)

    def fitness_sharing(self) -> None:
        """
        Divides fitness of each player by the total number of players to protect unique players.
        """
        for player in self.players:
            player.fitness /= len(self.players)
