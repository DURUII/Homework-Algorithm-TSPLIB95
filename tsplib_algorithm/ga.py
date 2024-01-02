import math
import random
import time
from tsplib_utils.time import timeit
from tsplib_utils.operator import *

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem


class GeneticAlgorithm(Algorithm):
    def __init__(self, init_population: list[int] = None, tag='GeneticAlgorithm', verbose=False, boost=False,
                 epoch=6, early_stop=7500, size=50, pc=1, pm=0.4, C=0.5):
        super().__init__(tag, verbose, boost)
        self.operator = [naive_swap, chunk_swap, chunk_swap, 
                         naive_insert, greedy_insert, greedy_insert, 
                         greedy_insert, chunk_insert, chunk_insert,
                         naive_reverse, naive_reverse, 
                         opt_swap_2,opt_swap_2,
                         opt_swap_3, opt_swap_3]

        self.early_stop, self.epoch, self.size,  = early_stop, epoch, size
        self.pc, self.pm, self.C = pc, pm, C
        self.dimension, self.init_population = -1, init_population or []
        self.population, self.problem = [], None

    @timeit
    def solve(self, problem: Problem):
        # lazy initialization
        problem.clear_cache()
        self.problem = problem
        self.dimension = problem.dimension
        self.initialize_population()

        for epoch in range(self.epoch):
            # local search
            boss_length, step = math.inf, 0
            while step <= self.early_stop:
                self.select()
                if self.verbose:
                    print(f'{epoch} - selected with best seen {problem.best_seen.length}')
                self.crossover()
                self.mutate()
                step +=1

                if self.problem.best_seen.length < boss_length:
                    boss_length = self.problem.best_seen.length
                    step = 0
            
            # basin-hopping
            self.initialize_population()
        
        # logger
        return self.tag, problem.benchmark, problem.best_seen.length, problem.best_seen.tour
            

    def initialize_population(self):
        self.population.extend(self.init_population)
        for _ in range(self.size - len(self.population)):
            self.population.append(
                list(np.random.permutation(list(range(1, self.dimension + 1)))))

    def select(self):
        lengths = [self.problem.calculate_length(
            individual, leaderboard=True) for individual in self.population]
        order = np.argsort(lengths)

        selected = [random.choice(self.operator)(i, self.problem) for i in self.init_population]
        selected.append(self.problem.best_seen.tour)
        selected.append(random.choice(self.operator)
                        (self.problem.best_seen.tour, self.problem))
        
        while len(selected) < self.size:
            idx, target = 0, 1
            while random.random() < target * (1 - self.C):
                idx += 1
                target *= self.C
            selected.append(self.population[order[idx]])

        self.population = selected
        
    def crossover(self):
        offspring = []
        random.shuffle(self.population)

        for i in range(1, self.size, 2):
            if random.random() <= self.pc:
                operator = [ox, pmx]
                offspring.extend(random.choice(operator)(self.population[i - 1], self.population[i]))
            else:
                offspring.extend([self.population[i - 1], self.population[i]])

        self.population = offspring

    def mutate(self):
        for i in range(self.size):
            if random.random() <= self.pm:
                self.population[i] = random.choice(self.operator)(
                    self.population[i], self.problem)
