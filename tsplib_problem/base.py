import math
import os

import numpy as np
from numba import jit
import rich
from collections import namedtuple

# Define a named tuple to hold information about the best tour seen so far
Solution = namedtuple("Solution", ["length", "tour"])


@jit(nopython=True)
def jit_matrix(dimension: int, coordinates: np.array):
    dist_matrix = np.full((dimension + 1, dimension + 1), -1)
    for i in range(1, dimension + 1):
        for j in range(i + 1, dimension + 1):
            # EUC_2D -> ROUNDED Euclidean distance
            dist = int(round(np.linalg.norm(coordinates[i] - coordinates[j])))
            dist_matrix[i, j] = dist_matrix[j, i] = dist
    return dist_matrix


class Problem:
    def __init__(self, benchmark: str) -> None:
        self.benchmark = benchmark
        self.filepath = os.path.join("tsplib_benchmark", f"{benchmark}.tsp")
        self.graph = None
        self.dimension = -1
        self.load_parse_tsp_file()
        self.best_seen = Solution(math.inf, [])

    def load_parse_tsp_file(self):
        # DIMENSION -> nums of cities/nodes/vertices
        with open(self.filepath) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for line in lines:
                if line.startswith("DIMENSION"):
                    self.dimension = int(line.split(":")[1])
                    coordinates = np.zeros((self.dimension + 1, 2))
                    rich.print(f'DIMENSION: {self.dimension}')
                    break

            if self.dimension == -1:
                raise ValueError('File does not contain a "DIMENSION" line.')

            # NODE_COORD_SECTION -> nodes/vertices with location
            starter = lines.index("NODE_COORD_SECTION") + 1
            for idx in range(starter, starter + self.dimension):
                i, x, y = lines[idx].split()
                coordinates[int(i)] = [float(x), float(y)]

            # GRAPH -> edges/links with distance
            self.graph = jit_matrix(self.dimension, coordinates)
            rich.print(f'GRAPH INITIALIZED')

    def get_distance(self, i, j):
        weight = self.graph[i, j]
        if weight == -1:
            raise ValueError(f'City ({i}, {j}) illegal.')
        return weight

    def calculate_length(self, tour: np.array, leaderboard=False):
        # Calculate the total length of a tour (fitness/objective)
        length = 0
        for i in range(0, len(tour)):
            src, dst = tour[i - 1], tour[i]
            length += self.graph[src, dst]

        if leaderboard and length < self.best_seen.length:
            print(length)
            self.best_seen = Solution(length, tour)
        return length
