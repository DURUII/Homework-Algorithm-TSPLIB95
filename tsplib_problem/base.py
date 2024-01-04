from enum import Enum
from collections import namedtuple
import math
import os
import networkx as nx
import rich
from matplotlib import pyplot as plt
from tsplib_utils.plot import plot_tsp_tour

Solution = namedtuple("Solution", ["length", "tour"])


class Problem:
    def __init__(self, benchmark: str, verbose=True, vis=False) -> None:
        self.benchmark = benchmark
        self.filepath = os.path.join("tsplib_benchmark", f"{benchmark}.tsp")
        self.__G = nx.Graph()
        self.dimension = -1

        self.best_seen = Solution(math.inf, [])
        self.__bank = {}

        self.verbose = verbose
        self.vis = vis
        if self.vis:
            self.fig, self.ax = plt.subplots(1, 1, figsize=(5.5, 4.5), layout='constrained')
            plt.ion()

        self.load_parse_tsp_file()

    def load_parse_tsp_file(self):
        # DIMENSION -> nums of cities/nodes/vertices
        with open(self.filepath) as fin:
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
            (x1, y1) = self.__G.nodes[i]["loc"]
            for j in range(i + 1, self.dimension + 1):
                (x2, y2) = self.__G.nodes[j]["loc"]
                # EUC_2D -> ROUNDED Euclidean distance
                weight = int(round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))
                self.__G.add_edge(i, j, weight=weight)

    def calculate_length(self, tour: list[int], leaderboard=False):
        """Calculate the total length of a tour."""
        assert len(tour) == self.dimension, 'Tour Incomplete!'

        length = 0
        # Include the distance of the edge going back to the starting point
        for i in range(0, len(tour)):
            src, dst = tour[i - 1], tour[i]
            length += self.__G.edges[src, dst]["weight"]

        # If this tour is better, update the best seen
        if self.vis and length <= self.best_seen.length:
            self.ax.cla()
            plot_tsp_tour(self.ax, 'C0', self.__G, tour)
            self.ax.set_title(length)
            plt.pause(0.0001)

        if leaderboard and length < self.best_seen.length:
            self.best_seen = Solution(length, tour)
            if self.verbose:
                rich.print(f"[bold red]best length {self.best_seen.length}[/]")

        return length

    def output_plot(self, tag: str, tour: list[int]):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(5.5, 4.5), layout='constrained', dpi=500)
        if not tour:
            plot_tsp_tour(self.ax, 'C0', self.__G, self.best_seen.tour)
            length = self.best_seen.length
        else:
            plot_tsp_tour(self.ax, 'C0', self.__G, tour)
            length = self.calculate_length(tour)
        self.ax.set_title(f'Algorithm {tag} with length {length}')
        plt.savefig(f'{self.benchmark}_{tag}')

    def clear_cache(self):
        self.best_seen = Solution(math.inf, [])

    def get_graph(self):
        return self.__G

    def get_distance(self, i, j):
        return self.__G.edges[i, j]['weight']
