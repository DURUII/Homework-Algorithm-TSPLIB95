from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_algorithm.pso import ParticleSwarmOpt
from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

for benchmark in open('./benchmark.txt'):
    benchmark = benchmark.strip()
    problem = Problem(benchmark, verbose=True, vis=False)

    for _ in range(10):
        solver = GreedyNearestNeighbor()
        memo = [solver.solve(problem)[-1]]

        solver = Opt2(base_solver=ChristofidesSerdyukov())
        memo.append(solver.solve(problem)[-1])

        solver = SimulatedAnnealing()
        memo.append(solver.solve(problem)[-1])

        # ensemble
        solver = GeneticAlgorithm(init_population=memo)
        solver.solve(problem)

        solver = WangLeiAlgorithm()
        solver.solve(problem)

        
