import math
import random

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem
from tsplib_utils.helper import timeit


class GreedyNearestNeighbor(Algorithm):
    def __init__(self, tag: str = 'GreedyNearestNeighbor', verbose: bool = True, boost=True):
        super().__init__(tag, verbose, boost)

    @timeit
    def solve(self, problem: Problem):
        cities = {i for i in range(1, problem.dimension + 1)}

        if self.boost:
            # Choose a starting city randomly
            starters = [random.randint(1, problem.dimension)]
        else:
            # Try every possible starting city
            starters = range(1, problem.dimension + 1)

        for starter in starters:
            tour, visited = [starter], {starter}

            while len(tour) < problem.dimension:
                # Find the nearest unvisited city from the last city
                candidates = cities - visited
                best_neighbor, best_distance = -1, math.inf
                for candidate in candidates:
                    if problem.get_distance(tour[-1], candidate) < best_distance:
                        best_distance = problem.get_distance(tour[-1], candidate)
                        best_neighbor = candidate

                # Update tour and visited
                tour.append(best_neighbor)
                visited.add(best_neighbor)

            # Calculate the length of the tour and update history record
            problem.calculate_length(tour=tour, leaderboard=True)
