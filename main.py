import matplotlib.pyplot as plt

from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

problem = Problem('a280', verbose=True)
solver = GeneticAlgorithm()
solver.solve(problem)
print(problem.best_seen.length)