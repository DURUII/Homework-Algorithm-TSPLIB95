import gc
import math
import os
import networkx as nx
from tsplib_algorithm.base import Algorithm
from collections import namedtuple
from typing import List

# Define a named tuple to hold information about the best tour seen so far
BestSeen = namedtuple("BestSeen", ["length", "tour"])


def parse_dimension(lines: List[str]) -> int:
    """Extract and return the dimension from the file.
       In the context of TSP, dimension refers to the number of cities/nodes/vertices."""
    for line in lines:
        if line.startswith("DIMENSION"):
            return int(line.split(":")[1])
    raise ValueError('File does not contain a "DIMENSION" line.')


class Instance:
    def __init__(self, benchmark: str) -> None:
        # Initialize the best seen tour to infinity and the graph
        self.best_seen = BestSeen(math.inf, [])
        self.G = nx.Graph()
        self.filepath = os.path.join("tsplib_benchmark", f"{benchmark}.tsp")

        # Load and parse the TSP file
        self.load_and_parse_file()

    def load_and_parse_file(self):
        """Load the TSP file and parse its lines."""
        with open(self.filepath) as fin:
            lines = [line.strip() for line in fin.readlines()]
            dimension = parse_dimension(lines)

        # Create nodes and edges for the graph
        self.init_nodes(lines)
        self.init_edges()

        # Collect garbage to free up memory
        gc.collect()

    def init_nodes(self, lines):
        """Create nodes for the graph based on the coordinates from the file."""
        starter = lines.index("NODE_COORD_SECTION") + 1
        for idx in range(starter, starter + self.G.number_of_nodes()):
            i, x, y = lines[idx].split()
            self.G.add_node(int(i), loc=(float(x), float(y)))

    def init_edges(self):
        """Create edges for the graph based on the rounded Euclidean distance between nodes."""
        for i in range(1, self.G.number_of_nodes() + 1):
            for j in range(i + 1, self.G.number_of_nodes() + 1):
                (x1, y1), (x2, y2) = self.G.nodes[i]["loc"], self.G.nodes[j]["loc"]
                weight = int(round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))
                self.G.add_edge(i, j, weight=weight)

    def length_of_a_tour(self, tour: list[int], leaderboard=False):
        """Calculate the total length of a tour."""
        length = 0
        for i in range(1, len(tour)):
            src, dst = tour[i - 1], tour[i]
            length += self.G.edges[src, dst]["weight"]

        # Include the weight of the edge going back to the starting point
        src, dst = tour[-1], tour[0]
        length += self.G.edges[src, dst]["weight"]

        # If this tour is shorter than the best seen so far, update the best seen
        if leaderboard and length < self.best_seen.length:
            self.best_seen = BestSeen(length, tour)

        return length

    def solve_by(self, algorithm: Algorithm):
        """Solve the TSP instance using the provided algorithm."""
        return algorithm.solve(self)
