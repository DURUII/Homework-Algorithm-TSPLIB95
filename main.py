from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_problem.base import Problem

solver = GreedyNearestNeighbor()
problem = Problem('a280')
solver.solve(problem)
print(problem.best_seen.length)
