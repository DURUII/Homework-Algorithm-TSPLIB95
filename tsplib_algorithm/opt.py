from tsplib_algorithm.base import Algorithm
from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_instance.base import Instance


class Opt2(Algorithm):
    def __init__(self, tag='2-OPT', base_solver: Algorithm = ChristofidesSerdyukov()):
        super().__init__(tag)
        self.base_solver = base_solver
    
    @classmethod
    def optimize(cls, problem, tour):
        min_length = problem.length_of_a_tour(tour)
        
        improved = True
        while improved:
            improved = False
            # Perform 2-opt optimization on the tour.
            for i in range(len(tour) - 2):
                for j in range(i + 2, len(tour)):
                    temp = tour[:]
                    temp[i + 1:j + 1] = temp[j:i:-1]
                    length = problem.length_of_a_tour(temp)
                    if length < min_length:
                        min_length = length
                        improved = True
                        tour = temp
                        
        return tour

    def solve(self, problem: Instance, verbose=False):
        self.base_solver.solve(problem, verbose=verbose)
        
        tour = problem.best_seen.tour[:]
        tour = Opt2.optimize(problem, tour)
        
        if verbose:
            self.print_best_solution(problem)
