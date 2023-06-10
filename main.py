import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

import time

import scienceplots

from tsplib_algorithm.cs import do_christofides_serdyukov
from tsplib_algorithm.nn import do_nearest_neighbor
from tsplib_algorithm.sa import do_stimulated_annealing
from tsplib_utils.parser import TSPParser

plt.style.use(["science"])

if __name__ == '__main__':
    with open("tsplib_benchmark/euc_2d", "r") as fin:
        names = [line.strip() for line in fin.readlines()]

    with open("expr", "w") as fout:
        for name in names:
            expr = []
            for _ in range(10):
                TSPParser(name, True)
                step_1_1 = do_nearest_neighbor(TSPParser.G, opt=True)
                TSPParser.boss_info("opt-nearest-neighbor")

                step_1_2 = do_christofides_serdyukov(TSPParser.G, opt=True, visualize=False)
                TSPParser.boss_info("opt-christofides")

                promising_length2tour = {**step_1_1, **step_1_2}
                do_stimulated_annealing(promising_length2tour)
                expr.append(TSPParser.boss_info("opt-stimulated_annealing"))
            expr = np.array(expr)
            fout.write(f"{name} {np.min(expr)} {np.mean(expr)}")
