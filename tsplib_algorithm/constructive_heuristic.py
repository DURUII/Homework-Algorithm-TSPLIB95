import math
from time import perf_counter
from typing import List

import networkx as nx
from operator import itemgetter

from tsplib_utils.helper import length_of_a_tour


# https://stackoverflow.com/questions/70168343/find-k-nearest-neighbors-of-a-node-in-a-networkx-graph
def nns(graph, node):
    assert 1 <= node <= graph.number_of_nodes()
    return list(map(itemgetter(1),
                    sorted([(e[2]['weight'], e[1])
                            for e in graph.edges(node, data=True)])[:]))


def nearest_neighbor(G: nx.Graph, intermediate_step: List[int]) -> (List[int], int):
    assert len(intermediate_step) > 0
    # current chessboard
    tour_permutation = [i for i in intermediate_step]

    # a tour has not been fully constructed
    while len(tour_permutation) < G.number_of_nodes():
        # choose the nearest city unvisited from the current city
        for neighbor in nns(G, tour_permutation[-1]):
            # unvisited
            if neighbor not in tour_permutation:
                tour_permutation.append(neighbor)
                # next time, choose the nearest from there
                break

    # final chessboard
    return tour_permutation, length_of_a_tour(G, tour_permutation)


def step_1_1(G: nx.Graph) -> (List[int], int):
    best_tour, min_length = None, math.inf

    # start at a particular city
    for starter in G.nodes(data=False):
        # 擂台法
        a_best_tour, a_min_length = nearest_neighbor(G, [starter])
        (min_length, best_tour) = (a_min_length, a_best_tour) if a_min_length < min_length else (min_length, best_tour)

    return best_tour, min_length
