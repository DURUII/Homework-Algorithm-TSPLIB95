import math
import random
import time

import numpy as np
import matplotlib.pyplot as plt

from tsplib_algorithm.base import Algorithm
from tsplib_algorithm.opt import Opt2
from tsplib_instance.base import Instance
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

    def __init__(self, tag="WangLeiAlgorithm"):
        super().__init__(tag)
        self.mini_operator = [naive_swap, naive_swap, naive_insert]
        self.large_operator = [naive_reserve, chunk_flip, chunk_swap, opt_swap_2, opt_swap_3]
        

    def generate_tour(self, conductor: list[int], problem: Instance):
        assert len(conductor) == problem.dimension

        # suppose cities emerge one by one,
        tour = []
        
        # greedy strategy
        for i in range(len(conductor)):
            if i < 3:
                tour.append(conductor[i])

            # at this moment, say [1, 2, 3]
            else:
                virtual_tour = tour[:]
                virtual_tour.append(virtual_tour[0])

                best_gain, best_idx = math.inf, -1
                for j in range(1, len(virtual_tour)):
                    # logically, do tour.insert(j, conductor[i]), say j=1, [1, 4, 2, 3]
                    assert conductor[i] != virtual_tour[j] and conductor[i] != virtual_tour[j - 1]
                    gain = problem.G.edges[virtual_tour[j - 1], conductor[i]]["weight"] + \
                           problem.G.edges[conductor[i], virtual_tour[j]]["weight"] - \
                           problem.G.edges[virtual_tour[j - 1], virtual_tour[j]]["weight"]

                    # where to insert you can minimize the total length gain
                    if gain < best_gain:
                        best_gain, best_idx = gain, j

                # insert the emergent city into the tour
                tour.insert(best_idx, conductor[i])

        return tour

    def solve(self, problem: Instance, early_stop=500, patience=500, verbose=False):    
        
        epoch = 0
        writer = SummaryWriter(comment=f'_wl_{patience}_{early_stop}')
    
        # initial @chessboard
        conductor = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))

        # loop until time is out
        tic = time.perf_counter()
        while time.perf_counter() - tic <= patience:

            # map conductor to tour (a feasible solution to the problem)
            tour = self.generate_tour(conductor, problem)
            best_length = problem.length_of_a_tour(tour, leaderboard=True)

            # local search
            step = 0
            while step <= early_stop:
                # another @chessboard in neighborhood
                operator = random.choice(self.mini_operator)
                another_conductor = operator(conductor)

                # map conductor to tour
                another_tour = self.generate_tour(another_conductor, problem)
                length = problem.length_of_a_tour(another_tour, leaderboard=True)
                writer.add_scalar('Length', length, epoch)
                epoch += 1
                step += 1

                # steepest descent
                if length < best_length:
                    best_length = length
                    conductor = another_conductor
                    step = 0
                    
                    
                    # for visual analysis
                    # plt.clf()
                    # fig, ax = plt.subplots(1, 1, figsize=(3.5, 2.5), layout='constrained', dpi=200)
                    # problem.plot_tsp_tour(ax, another_tour)
                    # uuid = f"{length}"
                    # ax.set_title(uuid)
                    # writer.add_figure('Tour', fig, epoch)
                    

            print('local search over!')

            # basin-hopping
            conductor = random.choice(self.large_operator)(conductor)
            print('basin-hopping over!')
            
            if problem.best_seen.length <= 2590:
                print(time.perf_counter() - tic)

        if verbose:
            self.print_best_solution(problem)
            print(op2count)