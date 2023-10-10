from operator import itemgetter

from tsplib_algorithm.base import Algorithm
from tsplib_instance.base import Instance


class GreedyNearestNeighbor(Algorithm):
    """Naive Greedy Nearest Neighbor Algorithm."""

    def __init__(self, tag: str = 'GreedyNearestNeighbor'):
        super().__init__(tag)

    def solve(self, problem: Instance, verbose: bool = False):
        """Solve the TSP instance using the Greedy Nearest Neighbor algorithm."""
        self.run_algorithm(problem)

        if verbose:
            self.print_best_solution(problem)

    def run_algorithm(self, problem: Instance):
        """Runs the algorithm for each possible starting city."""
        for starting_city in range(1, problem.dimension + 1):
            self.find_feasible_solution(starting_city, problem)

    def find_feasible_solution(self, starting_city: int, problem: Instance):
        """Finds a feasible solution by iteratively choosing the nearest unvisited city."""
        unvisited_cities = {i + 1 for i in range(problem.dimension)}
        tour = [starting_city]
        unvisited_cities.remove(tour[-1])

        while len(tour) < problem.dimension:
            next_city = self.get_nearest_unvisited_city(tour[-1], unvisited_cities, problem)
            tour.append(next_city)
            unvisited_cities.remove(next_city)

        problem.length_of_a_tour(tour, leaderboard=True)

    @staticmethod
    def get_nearest_unvisited_city(current_city: int, unvisited_cities: set, problem: Instance) -> int:
        """Returns the nearest unvisited city from the current city."""
        neighbor_cities = list(
            map(itemgetter(1),
                sorted([(e[2]['weight'], e[1]) for e in problem.G.edges(current_city, data=True)])))

        for city in neighbor_cities:
            if city in unvisited_cities:
                return city
