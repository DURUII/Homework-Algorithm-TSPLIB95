from tsplib_algorithm.ga import GeneticAlgorithm
from tsplib_problem.base import Problem


def main():
    # with cProfile.Profile() as pf:
    problem = Problem('a280')
    solver = GeneticAlgorithm(problem)
    solver.solve()
    # stats = pstats.Stats(pf)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename='ga.prof')


if __name__ == '__main__':
    main()
