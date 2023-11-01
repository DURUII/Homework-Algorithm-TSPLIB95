import math
import random
import time

from tsplib_utils.helper import timeit
from tsplib_utils.operator import *

import numpy as np

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem
from torch.utils.tensorboard import SummaryWriter


class SimulatedAnnealing(Algorithm):
    def __init__(self, tag='SimulatedAnnealing', verbose=True, boost=False,
                 t=1000, eps=1e-14, alpha=0.98, time_out=1, early_stop=280):
        """hyperparameters: t, eps, alpha, time_out, early_stop"""
        super().__init__(tag, verbose, boost)

        self.operator = [naive_swap, naive_swap, naive_swap, naive_swap,
                         naive_insert,
                         naive_reverse,
                         opt_swap_2, opt_swap_2, opt_swap_2, opt_swap_2, opt_swap_2, opt_swap_2,
                         opt_swap_3, opt_swap_3, opt_swap_3, opt_swap_3, opt_swap_3, opt_swap_3]
        self.t = t
        self.eps = eps
        self.alpha = alpha

        self.time_out = time_out
        self.early_stop = early_stop
        self.writer = SummaryWriter(
            comment=f'_sa_{self.t}_{self.eps}_{self.alpha}_{self.time_out}_{self.early_stop}')

    @timeit
    def solve(self, problem):
        tic = time.perf_counter()
        epoch = 0

        # terminate until it is too late
        while time.perf_counter() - tic < self.time_out:
            # one initial chessboard: generate a random feasible solution
            tour = list(np.random.permutation(np.arange(1, problem.dimension + 1)))
            length = problem.calculate_length(tour, leaderboard=True)

            while self.t > self.eps:
                step = 0
                local_best_length = math.inf

                # thermal equilibrium
                while step < self.early_stop:
                    # a naive trick: fix the starting city
                    tour_new = [tour[0]]
                    tour_new.extend(random.choice(self.operator)(tour[1:]))

                    length_new = problem.calculate_length(tour_new, leaderboard=True)
                    delta = length_new - length
                    step += 1
                    epoch += 1
                    self.writer.add_scalar('Length', length, epoch)
                    self.writer.add_scalar('Temperature', self.t, epoch)

                    if length_new < local_best_length:
                        local_best_length = length_new
                        step = 0

                    if delta < 0:
                        tour = tour_new
                        length = length_new

                    elif np.random.rand() <= np.exp(-delta / (np.abs(length) + 1e-6) / (self.t + 1e-6)):
                        tour = tour_new
                        length = length_new

                # simulated annealing
                self.t *= self.alpha
