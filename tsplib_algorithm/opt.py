from tsplib_algorithm.base import Algorithm
from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_problem.base import Problem
from tsplib_utils.helper import timeit


class Opt2(Algorithm):
    def __init__(self, tag='2-OPT', verbose=True, boost=True, base_solver=ChristofidesSerdyukov(), ):
        super().__init__(tag, verbose, boost)
        self.base_solver = base_solver

    @staticmethod
    def optimize(problem, tour):
        tour = tour[:]
        best_length = problem.calculate_length(tour, leaderboard=True)

        improved = True
        while improved:
            improved = False
            # Perform 2-opt optimization on the tour.
            for i in range(len(tour) - 2):
                for j in range(i + 2, len(tour)):
                    temp = tour[:]
                    temp[i + 1:j + 1] = temp[j:i:-1]
                    length = problem.calculate_length(temp, leaderboard=True)
                    if length < best_length:
                        best_length = length
                        improved = True
                        tour = temp

        return tour

    @timeit
    def solve(self, problem: Problem):
        self.base_solver.solve(problem)
        tour = Opt2.optimize(problem, problem.best_seen.tour)
        problem.calculate_length(tour, leaderboard=True)
