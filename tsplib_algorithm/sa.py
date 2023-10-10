import math
import random
import time

from tsplib_utils.operator import *

import numpy as np

from tsplib_algorithm.base import Algorithm
from tsplib_instance.base import Instance
from torch.utils.tensorboard import SummaryWriter


class SimulatedAnnealing(Algorithm):
    def __init__(self, tag='SimulatedAnnealing'):
        super().__init__(tag)

    def generate_tour(self, conductor: list[int], problem: Instance):
        assert len(conductor) == problem.dimension, f'{len(conductor)} != {problem.dimension}'

        # suppose cities emerge one by one,
        tour = []

        for i in range(len(conductor)):
            if i < 3:
                tour.append(conductor[i])

            # at this moment, say [1, 2, 3]
            else:
                virtual_tour = tour[:]
                virtual_tour.append(virtual_tour[0])

                best_gain, best_idx = math.inf, -1

                # greedy strategy
                for j in range(1, len(virtual_tour)):
                    # logically, do tour.insert(j, conductor[i]), say j=1, [1, 2, 3, 1] []
                    assert conductor[i] != virtual_tour[j] and conductor[i] != virtual_tour[j - 1]
                    gain = problem.G.edges[virtual_tour[j - 1], conductor[i]]["weight"] + \
                           problem.G.edges[conductor[i], virtual_tour[j]]["weight"] - \
                           problem.G.edges[virtual_tour[j - 1], virtual_tour[j]]["weight"]

                    # where to insert minimize the total length gain
                    if gain < best_gain:
                        best_gain, best_idx = gain, j

                # insert the emergent city into the tour
                tour.insert(best_idx, conductor[i])

        return tour

    def solve(self, problem, verbose=False, patience=500, level_step=50, T0=2e2, EPS=1e-2, ALPHA=0.9):
        epoch = 0
        writer = SummaryWriter(comment=f'_sa_{patience}_{level_step}_{T0}_{EPS}_{ALPHA}')
        tic = time.perf_counter()
        while time.perf_counter() - tic < patience:
            # initial @chessboard
            # conductor = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))
            tour = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))

            t = T0
            while t >= EPS:
                
                # fully search before annealing
                for _ in range(level_step):
                    E = problem.length_of_a_tour(tour, leaderboard=True)

                    # random draw another conductor from the previous' neighborhood
                    tour_new = random.choice([opt_swap_2, opt_swap_3, naive_swap])(tour)
                    E_new = problem.length_of_a_tour(tour_new, leaderboard=True)
                    epoch += 1

                    # delta of E
                    delta = E_new - E
                    writer.add_scalar('Temperature', t, epoch)
                    writer.add_scalar('Length', E_new, epoch)

                    # crucial jump
                    if delta < 0 or (t > 0 and -delta / t < 888 and np.random.rand() < np.exp(-delta / t)):
                        tour = tour_new

                # annealing
                print('annealing')
                t *= ALPHA

        if verbose:
            self.print_best_solution(problem)
