import tsplib_algorithm.greedy_heuristic as gh
from tsplib_parser.tsp_file_parser import TSPParser
from rich import print

if __name__ == '__main__':
    with open("tsplib_benchmark/euc_2d", "r") as fin:
        names = [line.strip() for line in fin.readlines()]

    # a280
    TSPParser(names[0], plot_tsp=True)
    gh.city_nearest_neighbor()
    TSPParser.plot()
