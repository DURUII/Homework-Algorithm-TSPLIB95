import math

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem
from tsplib_utils.helper import timeit


class GreedyNearestNeighbor(Algorithm):
    def __init__(self, tag: str = 'GreedyNearestNeighbor', verbose: bool = True):
        super().__init__(tag, verbose)

    @timeit
    def solve(self, problem: Problem):
        cities = {i for i in range(1, problem.dimension + 1)}

        # Repeat for each possible starting city
        for starter in range(1, problem.dimension + 1):
            tour, visited = [starter], {starter}

            while len(tour) < problem.dimension:
                # Find the nearest unvisited city from the last city
                candidates = cities - visited
                best_neighbor, mini_distance = -1, math.inf
                for candidate in candidates:
                    if problem.G.edges[tour[-1], candidate]["weight"] < mini_distance:
                        mini_distance = problem.G.edges[tour[-1], candidate]["weight"]
                        best_neighbor = candidate

                # Update tour and visited
                tour.append(best_neighbor)
                visited.add(best_neighbor)

            # For this starting city, calculate the length of the tour
            problem.length_of_a_tour(tour=tour, leaderboard=True)
