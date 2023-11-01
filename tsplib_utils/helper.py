import math
import os
import random
import time
from typing import List

import networkx as nx
from matplotlib import pyplot as plt

import scienceplots

plt.style.use(["science"])


def timeit(func):
    def wrap(*args, **kwargs):
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f'{func.__name__!r} execution time: {(toc - tic):.4f}s')
        return result

    return wrap


def random_color():
    return f"C{random.randint(1, 10)}"


def plot_tsp_tour(ax: plt.Axes, color: str, G: nx.Graph, tour: List[int], linewidth=0.6, markersize=2, alpha=1):
    assert G.number_of_nodes() == len(tour), f'{G.number_of_nodes()} != {len(tour)}'

    xs, ys = [], []
    for index in tour:
        x, y = G.nodes[index]["loc"]
        xs.append(x)
        ys.append(y)
        # label = str(index).zfill(3)
        # assert len(label) == 3
        # ax.text(x - 2, y - 0.5, label, color="w", fontsize=1.5)
    xs.append(G.nodes[tour[0]]["loc"][0])
    ys.append(G.nodes[tour[0]]["loc"][1])
    ax.plot(xs, ys, color=color, marker='o', linestyle='-', linewidth=linewidth, markersize=markersize, alpha=alpha)
