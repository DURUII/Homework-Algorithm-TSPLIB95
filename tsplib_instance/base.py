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


class Instance:
    def __init__(self, benchmark: str, verbose=False) -> None:
        # Initialize a graph to hold the problem instance
        self.benchmark = benchmark
        self.verbose = verbose
        self.filepath = os.path.join("tsplib_benchmark", f"{benchmark}.tsp")
        self.best_seen = Solution(math.inf, [])
        self.dimension = -1
        self.reset_leaderboard()
        self.G = nx.Graph()

        # Load and parse the TSP file
        self.load_and_parse_file()
        
        # Load the optimal solution
        

    def reset_leaderboard(self):
        """Reset the best solution seen so far to infinity."""
        self.best_seen = Solution(math.inf, [])

    def load_and_parse_file(self):
        """Load the TSP file and parse its lines."""
        with open(self.filepath) as fin:
            lines = [line.strip() for line in fin.readlines()]
            self.dimension = self.parse_dimension(lines)

        # Create nodes and edges for the graph
        self.init_nodes(lines)
        self.init_edges()

    @staticmethod
    def parse_dimension(lines: List[str]) -> int:
        """Extract the dimension of one instance, which refers to the number of cities/nodes/vertices."""
        for line in lines:
            if line.startswith("DIMENSION"):
                return int(line.split(":")[1])
        raise ValueError('File does not contain a "DIMENSION" line.')

    def init_nodes(self, lines):
        """Create nodes for the graph based on the coordinates from the file."""
        starter = lines.index("NODE_COORD_SECTION") + 1
        for idx in range(starter, starter + self.dimension):
            i, x, y = lines[idx].split()
            self.G.add_node(int(i), loc=(float(x), float(y)))

    def init_edges(self):
        """Create edges for the graph based on the ROUNDED Euclidean distance between nodes."""
        for i in range(1, self.dimension + 1):
            for j in range(i + 1, self.dimension + 1):
                (x1, y1), (x2, y2) = self.G.nodes[i]["loc"], self.G.nodes[j]["loc"]
                weight = int(round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))
                self.G.add_edge(i, j, weight=weight)

    def plot_tsp_tour(self, ax: plt.Axes, tour: List[int], opt=False):
        assert len(tour) == self.dimension, 'Tour Incomplete!'
        plot_tsp_tour(ax, "C0", self.G, tour)
        # if opt:
        #     plot_tsp_tour(ax, "r", self.G, tour, alpha=0.5, marker='o', linestyle='-', linewidth=2, markersize=2)
        

    def length_of_a_tour(self, tour: list[int], leaderboard=False):
        """Calculate the total length of a tour."""
        assert len(tour) == self.dimension, 'Tour Incomplete!'

        length = 0
        for i in range(1, len(tour)):
            src, dst = tour[i - 1], tour[i]
            length += self.G.edges[src, dst]["weight"]

        # Include the distance of the edge going back to the starting point
        src, dst = tour[-1], tour[0]
        length += self.G.edges[src, dst]["weight"]

        # If this tour is better, update the best seen
        if leaderboard and length < self.best_seen.length:
            self.best_seen = Solution(length, tour)
            if self.verbose:
                rich.print(f"[bold green blink]best length {self.best_seen.length}[/]", )

        return length

    def solve_by(self, algorithm):
        """Solve the TSP instance using the provided algorithm."""
        return algorithm.solve(self)
