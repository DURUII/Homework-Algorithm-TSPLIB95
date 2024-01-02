import random

import numpy as np

from tsplib_utils.helper import timeit
from tsplib_utils.operator import *

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem


class GeneticAlgorithm(Algorithm):
    def __init__(self, problem: Problem,
                 tag='GeneticAlgorithm', verbose=True, boost=False,
                 epoch=40000, size=50, pc=0.9, pm=0.2):
        super().__init__(tag, verbose, boost)

        self.problem = problem
        self.dimension = problem.dimension
        self.graph = problem.graph
        self.size = size
        self.population = np.array([np.random.permutation(self.dimension) + 1 for _ in range(size)])
        self.fitness = self.calculate_fitness(self.population)
        self.pc = pc
        self.pm = pm
        self.epoch = epoch
        self.operator = [opt_swap_2, opt_swap_3]

    @timeit
    def solve(self):
        for epoch in range(self.epoch):
            self.select()
            self.crossover()
            self.mutate()
            print(epoch, self.problem.best_seen.length)

    def crossover(self):
        queue = [i for i in range(self.size) if random.random() < self.pc]
        random.shuffle(queue)
        for k in range(0, len(queue) - 1, 2):
            i, j = queue[k], queue[k + 1]
            self.population[i], self.population[j] = ox(self.population[i], self.population[j])

    def mutate(self):
        for i in range(self.size):
            if random.random() < self.pm:
                operator = random.choice(self.operator)
                self.population[i] = operator(self.population[i], self.problem)
                i -= 1

    def select(self):
        population = []

        fitness = self.fitness / sum(self.fitness)
        fitness = np.cumsum(fitness)

        population.append(self.problem.best_seen.tour)
        operator = random.choice(self.operator)
        population.append(operator(self.problem.best_seen.tour))

        for _ in range(self.size - len(population)):
            sample = np.searchsorted(fitness, np.random.random())
            population.append(self.population[sample])

        self.population = np.array(population)
        self.fitness = self.calculate_fitness(self.population)

    def calculate_fitness(self, bank):
        return np.reciprocal(
            np.array(
                [self.problem.calculate_length(individual, leaderboard=True)
                 for individual in bank]
            )
        )
