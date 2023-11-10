import math
import random
import time

import numpy as np

from tsplib_utils.helper import timeit
from tsplib_utils.operator import *

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem


class GeneticAlgorithm(Algorithm):
    def __init__(self, tag='GeneticAlgorithm', verbose=True, boost=False,
                 time_out=3600, size=200, pc=1, pm=0.4):
        super().__init__(tag, verbose, boost)
        self.operator = [naive_insert, chunk_insert, naive_insert, chunk_insert,
                         naive_insert, chunk_insert, naive_insert, chunk_insert,
                         greedy_insert,
                         naive_reverse, naive_reverse, naive_reverse,
                         naive_swap, chunk_swap, naive_swap, chunk_swap,
                         naive_swap, chunk_swap, naive_swap, chunk_swap,
                         opt_swap_2, opt_swap_3, opt_swap_2, opt_swap_3,
                         opt_swap_2, opt_swap_3, opt_swap_2, opt_swap_3,
                         opt_swap_2, opt_swap_3, opt_swap_2, opt_swap_3,
                         opt_swap_2, opt_swap_3, opt_swap_2, opt_swap_3]

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

        if problem.best_seen.tour:
            population.extend(
                random.choice(self.operator)(problem.best_seen.tour, problem)
                for _ in range(self.size)
            )
        else:
            # init individuals: generate random population
            population.extend(
                list(np.random.permutation(list(range(1, problem.dimension + 1))))
                for _ in range(self.size)
            )
        # before it is too late
        tic = time.perf_counter()
        while time.perf_counter() - tic < self.time_out:
            epoch += 1
            # selection (survival of the fittest)
            mating_pool = self.select_diversity(population, problem)
            print(f'{epoch} - selected with best seen {problem.best_seen.length}')
            # crossover/inheritance
            offspring = self.crossover(mating_pool)
            # in-place mutate/variation
            self.mutate(offspring, problem)
            population = offspring

        # return value
        for individual in population:
            self.fitness(individual, problem)

    def select_fitness(self, population: list[list[int]], problem: Problem):
        # select based on probability of surviving
        roulette = np.array([self.fitness(i, problem) for i in population])
        roulette /= sum(roulette)
        for i in range(1, len(roulette)):
            roulette[i] += roulette[i - 1]

        selected = [problem.best_seen.tour]
        for _ in range(len(population) - 1):
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

    def select_rank(self, population: list[list[int]], problem: Problem):
        C = 0.3
        selected = []
        sorted_population = sorted(population, key=lambda p: problem.calculate_length(p, leaderboard=True))

        for item in population:
            idx, target = 0, C
            while random.random() < target:
                idx += 1
                target *= C

            selected.append(sorted_population[idx])
        return selected

    def select_diversity(self, population: list[list[int]], problem: Problem):
        length = [problem.calculate_length(i, leaderboard=True) for i in population]
        diversity = []
        for i in range(len(length)):
            diversity.append(math.inf)
            for j in range(len(length)):
                if j != i:
                    diversity[i] = min(length[j] - length[i], diversity[i])

        C = 0.5
        order_length = np.argsort(length)
        order_diversity = np.argsort(diversity)

        selected = [problem.best_seen.tour]
        for _ in range(len(population) - 1):
            idx, target = 0, 1
            while random.random() < target * (1 - C):
                idx += 1
                target *= C

            if random.random() < 0.7:
                selected.append(population[order_length[idx]])
            else:
                selected.append(population[order_diversity[idx]])

        return selected

    def crossover(self, population: list[list[int]]):
        offspring = []
        for i in range(1, len(population), 2):
            if random.random() <= self.pc:
                operator = [ox, pmx]
                offspring.extend(random.choice(operator)(population[i - 1], population[i]))
            else:
                offspring.extend([population[i - 1], population[i]])
        return offspring

    def mutate(self, population: list[list[int]], problem):
        for i in range(len(population)):
            if random.random() <= self.pm:
                population[i] = random.choice(self.operator)(population[i], problem)

    @staticmethod
    def fitness(individual: list[int], problem: Problem):
        """The simplest implementation of fitness, regardless of rank and diversity. """
        assert len(individual) == problem.dimension
        return 1 / problem.calculate_length(individual, leaderboard=True)
