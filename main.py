import matplotlib.pyplot as plt

from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_algorithm.pso import ParticleSwarmOpt
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

problem = Problem('a280', verbose=False, vis=False)
solver = Opt2(base_solver=ChristofidesSerdyukov())
solver.solve(problem)

solver = GeneticAlgorithm()
solver.solve(problem)
