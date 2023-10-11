from tsplib_algorithm.nn import *
from tsplib_instance.base import *

instance = Instance(benchmark='a280')
solver = GreedyNearestNeighbor()
solver.solve(instance)
