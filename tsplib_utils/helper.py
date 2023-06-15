import math
import os
import random
import time
from typing import List

import networkx as nx
from matplotlib import pyplot as plt

import scienceplots

plt.style.use(["science"])


def read_lines(filepath: str) -> List[str]:
    assert os.path.exists(filepath)

    # read by line for later parsing
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]
        return lines


def parse_dimension(lines: List[str]) -> int:
    for line in lines:
        if line.startswith("DIMENSION"):
            return int(line.split(":")[1])


def round_distance(x1: float, y1: float, x2: float, y2: float) -> int:
    return int(round(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))))


def timestamp():
    return time.strftime("%Y-%m-%d %X", time.localtime())


def random_color():
    return f"C{random.randint(1, 10)}"


def plot_tsp_tour(ax: plt.Axes, color: str, G: nx.Graph, permutation: List[int]):
    assert G.number_of_nodes() == len(permutation)

    xs, ys = [], []
    for index in permutation:
        x, y = G.nodes[index]["loc"]
        xs.append(x)
        ys.append(y)
        # label = str(index).zfill(3)
        # assert len(label) == 3
        # ax.text(x - 2, y - 0.5, label, color="w", fontsize=1.5)
    xs.append(G.nodes[permutation[0]]["loc"][0])
    ys.append(G.nodes[permutation[0]]["loc"][1])
    ax.plot(xs, ys, color=color, marker='o', linestyle='-', linewidth=0.6, markersize=2)
