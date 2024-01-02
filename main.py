import matplotlib.pyplot as plt

from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_algorithm.pso import ParticleSwarmOpt
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

for benchmark in open('./benchmark.txt').readlines():
    problem = Problem(benchmark, verbose=True, vis=False)

    for i in range(10):
        solver = GreedyNearestNeighbor()
        solver.solve(problem)

        solver = ChristofidesSerdyukov()
        solver.solve(problem)

        solver = Opt2(base_solver=solver)
        solver.solve(problem)

        solver = SimulatedAnnealing()
        solver.solve(problem)

        solver = WangLeiAlgorithm()
        solver.solve(problem)

        solver = ParticleSwarmOpt()
        solver.solve(problem)

    break
