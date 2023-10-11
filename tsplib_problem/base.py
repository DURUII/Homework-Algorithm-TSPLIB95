import math
import os
import networkx as nx
import rich

from collections import namedtuple
from typing import List
import matplotlib.pyplot as plt
from tsplib_utils.helper import plot_tsp_tour

# Define a named tuple to hold information about the best tour seen so far
Solution = namedtuple("Solution", ["length", "tour"])


class Problem:
    def __init__(self, benchmark: str, verbose=True) -> None:
        # Initialize a graph to hold the problem instance
        self.benchmark = benchmark
        self.best_seen = Solution(math.inf, [])
        self.dimension = -1
        self.verbose = verbose
        self.__filepath = os.path.join("tsplib_benchmark", f"{benchmark}.tsp")
        self.__G = nx.Graph()

        self.load_parse_tsp_file()

    def load_parse_tsp_file(self):
        # DIMENSION -> nums of cities/nodes/vertices
        with open(self.__filepath) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for line in lines:
                if line.startswith("DIMENSION"):
                    self.dimension = int(line.split(":")[1])

            if self.dimension == -1:
                raise ValueError('File does not contain a "DIMENSION" line.')

        # NODE_COORD_SECTION -> nodes/vertices with location
        starter = lines.index("NODE_COORD_SECTION") + 1
        for idx in range(starter, starter + self.dimension):
            i, x, y = lines[idx].split()
            self.__G.add_node(int(i), loc=(float(x), float(y)))

        # GRAPH -> edges/links with distance
        for i in range(1, self.dimension + 1):
            for j in range(i + 1, self.dimension + 1):
                (x1, y1), (x2, y2) = self.__G.nodes[i]["loc"], self.__G.nodes[j]["loc"]
                # EUC_2D -> ROUNDED Euclidean distance
                weight = int(round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))
                self.__G.add_edge(i, j, weight=weight)

    def get_graph(self):
        return self.__G

    def get_distance(self, i, j):
        assert 1 <= i <= self.dimension and 1 <= j <= self.dimension
        return self.__G.edges[i, j]['weight']

    def plot_tsp_tour(self, ax: plt.Axes, tour: List[int], opt=False):
        assert len(tour) == self.dimension, 'Tour Incomplete!'
        plot_tsp_tour(ax, "C0", self.G, tour)
        # if opt:
        #     plot_tsp_tour(ax, "r", self.G, tour, alpha=0.5, marker='o', linestyle='-', linewidth=2, markersize=2)

    def calculate_length(self, tour: list[int], leaderboard=False):
        """Calculate the total length of a tour."""
        assert len(tour) == self.dimension, 'Tour Incomplete!'

        length = 0
        for i in range(1, len(tour)):
            src, dst = tour[i - 1], tour[i]
            length += self.__G.edges[src, dst]["weight"]

        # Include the distance of the edge going back to the starting point
        src, dst = tour[-1], tour[0]
        length += self.__G.edges[src, dst]["weight"]

        # If this tour is better, update the best seen
        if leaderboard and length < self.best_seen.length:
            self.best_seen = Solution(length, tour)
            if self.verbose:
                rich.print(f"[bold green blink]best length {self.best_seen.length}[/]", )

        return length

    def solve_by(self, algorithm):
        """Solve the TSP instance using the provided algorithm."""
        return algorithm.solve(self)

        # instance = Problem(benchmark='a280')
        #
        # distances = np.zeros(shape=(instance.dimension + 1, instance.dimension + 1), dtype=int)
        #
        # for i in range(1, instance.dimension + 1):
        #     for j in range(1, instance.dimension + 1):
        #         if i != j:
        #             distances[i][j] = instance.G.edges[i, j]['weight']
        #
        # with open('tsplib_benchmark/a280.sum_dist.tsp', 'w') as fout:
        #     fout.write(str(distances.tolist()))
