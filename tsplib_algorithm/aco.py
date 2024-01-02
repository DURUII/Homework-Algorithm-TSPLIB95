import math
import random
import time

from tsplib_utils.helper import timeit
from tsplib_utils.operator import *

import numpy as np

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem


class Ant:
    problem = None
    # also known as pheromone
    tau = dict()
    # parameter setting
    alpha, beta, rho = 1, 5, 0.5

    def __init__(self, problem: Problem):
        if Ant.problem is None:
            Ant.problem = problem

        if len(Ant.tau) == 0:
            for i in range(1, problem.dimension + 1):
                for j in range(1, problem.dimension + 1):
                    pass

        self.tour = [np.random.randint(1, problem.dimension + 1)]
        self.taboo = {self.tour[0]}

    def select(self, candidates: list[int]):
        roulette = []
        for c in candidates:
            roulette.append(
                Ant.tau[(self.tour[-1], c)] ** Ant.alpha * Ant.problem.get_distance(self.tour[-1], c) ** Ant.beta
            )

        roulette /= sum(roulette)
        for i in range(1, len(roulette)):
            roulette[i] += roulette[i - 1]

        target = random.random()
        lo, hi = 0, len(roulette) - 1
        while lo < hi:
            mid = lo + hi >> 1
            if roulette[mid] >= target:
                hi = mid
            else:
                lo = mid + 1

        return candidates[lo]

    def move(self):
        # with probability
        assert len(self.tour) <= Ant.problem.dimension

        if len(self.tour) == Ant.problem.dimension:
            pass

        else:
            ff = self.tour[0]
            tt = 0

        pass

    def update(self):
        assert len(self.tour) == Ant.problem.dimension
        for idx in range(1, len(self.tour)):
            self.tau[(self.tour[idx - 1], self.tour[idx])] *= (1 - Ant.rho)
            delta = 1
            self.tau[(self.tour[idx - 1], self.tour[idx])] += delta

        pass


class AntColonyOpt(Algorithm):
    def __init__(self, tag='SimulatedAnnealing', verbose=True, boost=False,
                 t=1000, eps=1e-14, alpha=0.98, time_out=1, early_stop=280):
        """hyperparameters: t, eps, alpha, time_out, early_stop"""
        super().__init__(tag, verbose, boost)
        self.size = 11200
        self.time_out = 1200
        self.early_stop = 50

    @timeit
    def solve(self, problem: Problem):
        # before it is too late
        tic = time.perf_counter()
        while time.perf_counter() - tic < self.time_out:
            # ants initialization
            step = 0

            ants = []

            # optimization
            while step < self.early_stop:
                # construct feasible solution
                for ant in ants:
                    ant.move()

                # pheromone update
                for ant in ants:
                    ant.update()

                pass
