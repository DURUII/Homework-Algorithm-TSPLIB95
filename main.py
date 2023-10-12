from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

# solver = GreedyNearestNeighbor()
# problem = Problem('a280')
# solver.solve(problem)
# print(problem.best_seen.length)
#
# solver = ChristofidesSerdyukov()
# problem = Problem('a280')
# solver.solve(problem)
# print(problem.best_seen.length)


problem = Problem('a280', verbose=True)

# solver = SimulatedAnnealing(
#     t=1000, eps=1e-14, alpha=0.98, time_out=1,
#     early_stop=problem.dimension)


# base_solver = ChristofidesSerdyukov()
# solver = Opt2(base_solver=base_solver)
# solver.solve(problem)
# print(problem.best_seen.length)


