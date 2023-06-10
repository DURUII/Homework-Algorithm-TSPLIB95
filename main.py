import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

import time

import scienceplots

from tsplib_algorithm.cs import do_christofides_serdyukov
from tsplib_algorithm.nn import do_nearest_neighbor
from tsplib_algorithm.sa import do_stimulated_annealing
from tsplib_utils.helper import plot_tsp_tour
from tsplib_utils.parser import TSPParser

plt.style.use(["science"])

if __name__ == '__main__':
    with open("tsplib_benchmark/euc_2d", "r") as fin:
        names = [line.strip() for line in fin.readlines()]

    for index in range(len(names)):
        name = names[index]
        tours, costs = [], []

        for i in range(10):
            with open("log.txt", "w+") as fout:
                fout.write(f"###### {i + 1} of {name}[{index + 1}/{len(names)}]")

            TSPParser(name, False)
            step_1_1 = do_nearest_neighbor(TSPParser.G, opt=True)
            TSPParser.boss_info("opt-nearest-neighbor")

            step_1_2 = do_christofides_serdyukov(TSPParser.G, opt=True, visualize=False)
            TSPParser.boss_info("opt-christofides")

            promising_length2tour = {**step_1_1, **step_1_2}
            do_stimulated_annealing(promising_length2tour, lim=50)
            tour, cost = TSPParser.boss_info("opt-stimulated_annealing")
            tours.append(tour)
            costs.append(cost)

        costs = np.array(costs)

        # logger
        with open("log.txt", "w+") as fout:
            fout.write(f"--->>> {name} {int(np.min(costs))} {int(np.mean(costs))}\n")

        # sheet
        with open("assets/experiment.txt", "w+") as fout:
            fout.write(f"{name} {int(np.min(costs))} {int(np.mean(costs))}\n")

        fig, axes = plt.subplots(2, 5, figsize=(22, 6.5), layout='constrained')
        for i in range(2):
            for j in range(5):
                ax = axes[i][j]
                plot_tsp_tour(ax, f"C{i * 5 + j}", TSPParser.G, tours[i * 5 + j])
                ax.set_title(f"{i * 5 + j + 1}")

        fig.suptitle(f"{name} - experimental result with {int(np.min(costs))}", fontsize=25, weight="bold")
        plt.savefig(f"assets/experiment/{name}'s experimental result({int(np.min(costs))})", dpi=600)
