import math
import random
import time

import numpy as np
import matplotlib.pyplot as plt

from tsplib_algorithm.base import Algorithm
from tsplib_algorithm.opt import Opt2
from tsplib_problem.base import Problem
from tsplib_utils.operator import *
from tsplib_utils.helper import *
from torch.utils.tensorboard import SummaryWriter


class WangLeiAlgorithm(Algorithm):
    """
    This implementation is roughly based on content from Wang's lecture.
    From my perspective, the distinguishing features of this algorithm are as follows:

    1. Quasi-online greedy strategy:
        The tour is generated in a quasi-online manner, directed by random arriving order.
    2. Two-tiered strategy:
        It employs mini-step local search complemented by large-step basin-hopping.
    """

    def __init__(self, tag="WangLeiAlgorithm", verbose: bool = True, boost=True,
                 time_out=120, early_stop=280):
        super().__init__(tag, verbose, boost)
        self.time_out = time_out
        self.early_stop = early_stop
        self.mini_operator = [naive_swap, naive_insert, naive_reverse]
        self.large_operator = [opt_swap_2, opt_swap_3]
        self.writer = SummaryWriter(comment=f'_wl')

    def solve(self, problem: Problem, early_stop=500, patience=500, verbose=False):
        epoch = 0
        # initial chessboard -> the coming order of cities
        conductor = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))

        # loop until time is out
        tic = time.perf_counter()
        while time.perf_counter() - tic <= self.time_out:
            # map conductor to tour (a feasible solution to the problem)
            tour = self.generate_tour(conductor, problem)
            local_best_length = problem.calculate_length(tour, leaderboard=True)

            # local search
            step = 0
            while step <= self.early_stop:
                # another @chessboard in neighborhood
                new_conductor = random.choice(self.mini_operator)(conductor)

                # map conductor to tour
                new_tour = self.generate_tour(new_conductor, problem)
                new_length = problem.calculate_length(new_tour, leaderboard=True)
                epoch += 1

                # steepest descent
                if new_length < local_best_length:
                    local_best_length = new_length
                    # update status
                    step = 0
                    conductor = new_conductor
                    self.writer.add_scalar('Length', local_best_length, epoch)

            print('local search over!')

            # basin-hopping
            conductor = random.choice(self.large_operator)(conductor)
            print('basin-hopping over!')

    @staticmethod
    def generate_tour(conductor: list[int], problem: Problem):
        assert len(conductor) == problem.dimension

        # suppose cities emerge one by one,
        tour = []

        # greedy strategy
        for i in range(len(conductor)):
            if i < 3:
                tour.append(conductor[i])

            # at this moment, say [1, 2, 3]
            else:
                tour.append(tour[0])
                best_gain, best_idx = math.inf, -1

                for j in range(1, len(tour)):
                    # logically, do tour.insert(j, conductor[i]), say j=1, [1, 4, 2, 3]
                    gain = problem.get_distance(tour[j - 1], conductor[i]) + \
                           problem.get_distance(conductor[i], tour[j]) - \
                           problem.get_distance(tour[j - 1], tour[j])

                    # where to insert you can minimize the total length gain
                    if gain < best_gain:
                        best_gain, best_idx = gain, j

                del tour[-1]
                # insert the emergent city into the tour
                tour.insert(best_idx, conductor[i])

        return tour
