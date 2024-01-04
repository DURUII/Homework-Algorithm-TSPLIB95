from tqdm.auto import tqdm
from tsplib_algorithm.cs import ChristofidesSerdyukov
from tsplib_algorithm.nn import GreedyNearestNeighbor
from tsplib_algorithm.sa import SimulatedAnnealing
from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_problem.base import Problem
from tsplib_algorithm.opt import Opt2

for _ in range(10):
    for benchmark in tqdm(open('./benchmark.txt').readlines()):
        benchmark = benchmark.strip()
        problem = Problem(benchmark, verbose=False, vis=False)

        solver = Opt2(base_solver=ChristofidesSerdyukov())
        tour = solver.solve(problem)[-1]
        memo = [tour]

        solver = SimulatedAnnealing()
        solver.solve(problem)

        solver = WangLeiAlgorithm()
        solver.solve(problem)

        solver = GreedyNearestNeighbor()
        memo.append(solver.solve(problem)[-1])

        # ensemble
        solver = GeneticAlgorithm(init_population=memo)
        solver.solve(problem)