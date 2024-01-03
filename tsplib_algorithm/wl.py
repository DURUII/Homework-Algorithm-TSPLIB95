from tsplib_algorithm.base import Algorithm
from tsplib_utils.operator import *
from tsplib_utils.time import *


class WangLeiAlgorithm(Algorithm):
    """
    This implementation is roughly based on content from Wang's lecture.
    From my perspective, the distinguishing features of this algorithm are as follows:

    1. Quasi-online greedy strategy:
        The tour is generated in a quasi-online manner, directed by random arriving order.
    2. Two-tiered strategy:
        It employs mini-step local search complemented by large-step basin-hopping.
    """

    def __init__(self, tag="WangLeiAlgorithm",
                 verbose: bool = False, boost=True,
                 epoch=160, early_stop=200):
        super().__init__(tag, verbose, boost)

        self.epoch = epoch
        self.early_stop = early_stop

        self.mini_operator = [naive_swap, naive_insert]
        self.large_operator = [naive_reverse, chunk_swap, opt_swap_2, opt_swap_3]

    @timeit
    def solve(self, problem: Problem):
        problem.clear_cache()
        
        for _ in range(self.epoch):
            # initial chessboard -> the coming order of cities
            conductor = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))

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
                step += 1

                # steepest descent
                if new_length < local_best_length:
                    local_best_length = new_length
                    # update status
                    step = 0
                    conductor = new_conductor

            if self.verbose:
                print('local search over!')

            # basin-hopping
            if random.random() < 0.5:
                conductor = random.choice(self.large_operator)(conductor)
            else:
                conductor = list(np.random.permutation([i + 1 for i in range(problem.dimension)]))
            
            if self.verbose:
                print('basin-hopping over!')


        # logger
        return self.tag, problem.benchmark, problem.best_seen.length, problem.best_seen.tour

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
