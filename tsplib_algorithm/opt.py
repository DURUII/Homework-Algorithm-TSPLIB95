from typing import List

import networkx as nx

from tsplib_utils.helper import length_of_a_tour


def two_opt(G: nx.Graph, permutation: List[int]) -> (List[int], int):
    """
    ref:
    https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python
    """
    tour = permutation[:]
    min_length = length_of_a_tour(G, tour)

    improved = True
    while improved:
        improved = False
        for i in range(len(tour) - 2):
            for j in range(i + 2, len(tour)):
                temp = tour[:]
                temp[i + 1:j + 1] = temp[j:i:-1]
                length = length_of_a_tour(G, temp)
                if length < min_length:
                    min_length = length
                    improved = True
                    tour = temp

    return tour, min_length
