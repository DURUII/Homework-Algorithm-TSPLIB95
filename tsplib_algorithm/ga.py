import random
import time

import numpy as np

from tsplib_utils.helper import timeit
from tsplib_utils.operator import *

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem


class GeneticAlgorithm(Algorithm):
    def __init__(self, tag='GeneticAlgorithm', verbose=True, boost=False,
                 time_out=120, size=1120, pc=0.9, pm=0.5):
        super().__init__(tag, verbose, boost)
        self.operator = [opt_swap_2, opt_swap_3]

        # time of mimicking evolution
        self.time_out = time_out
        # size of population
        self.size = size
        # probability of crossover
        self.pc = pc
        # probability of mutation
        self.pm = pm

    @timeit
    def solve(self, problem: Problem):
        epoch = 0
        # a bank/population/colony of individuals/genotype/chromosome
        # (genotype equals phenotype in this special case)
        population = []

        # init individuals: generate random population
        for _ in range(self.size):
            # a list of n integers, each of which occurs exactly once
            # n.b. an individual exactly represents a tour
            population.append(list(np.random.permutation([i for i in range(1, problem.dimension + 1)])))

        # before it is too late
        tic = time.perf_counter()
        while time.perf_counter() - tic < self.time_out:
            epoch += 1
            # selection (survival of the fittest)
            mating_pool = self.select(population, problem)
            # crossover/inheritance
            offspring = self.crossover(mating_pool)
            # in-place mutate/variation
            self.mutate(offspring)
            population = offspring

        # return value
        for individual in population:
            self.fitness(individual, problem)

    def select(self, population: list[list[int]], problem: Problem):
        selected = []
        # select based on probability of surviving
        roulette = np.array([self.fitness(i, problem) for i in population])
        roulette /= sum(roulette)
        for i in range(1, len(roulette)):
            roulette[i] += roulette[i - 1]

        for _ in range(len(population)):
            target = random.random()
            lo, hi = 0, len(roulette) - 1
            while lo < hi:
                mid = lo + hi >> 1
                if roulette[mid] >= target:
                    hi = mid
                else:
                    lo = mid + 1
            selected.append(population[lo])

        return selected

    def crossover(self, population: list[list[int]]):
        offspring = []
        random.shuffle(population)
        for i in range(len(population) // 2):
            if random.random() <= self.pc:
                offspring.extend(ox(population[i], population[i + len(population) // 2]))
            else:
                offspring.extend([population[i], population[i + len(population) // 2]])
        return offspring

    def mutate(self, population: list[list[int]]):
        for i in range(len(population)):
            if random.random() <= self.pm:
                population[i] = random.choice(self.operator)(population[i])

    @staticmethod
    def fitness(individual: list[int], problem: Problem):
        """The simplest implementation of fitness, regardless of rank and diversity. """
        assert len(individual) == problem.dimension
        return 1 / problem.calculate_length(individual, leaderboard=True)
