import time
from typing import List, Dict, Set

import networkx as nx
from operator import itemgetter

from tsplib_algorithm.opt import two_opt
from tsplib_utils.parser import TSPParser


def neighbors(graph, node):
    # https://stackoverflow.com/questions/70168343/find-k-nearest-neighbors-of-a-node-in-a-networkx-graph
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
        for neighbor in neighbors(G, tour_permutation[-1]):
            # unvisited
            if neighbor not in tour_permutation:
                tour_permutation.append(neighbor)
                # next time, choose the nearest from there
                break

    # final chessboard
    return tour_permutation, TSPParser.length_of_a_tour(tour_permutation)


def do_nearest_neighbor(G: nx.Graph, opt=True, lim=0.4) -> Dict[int, List[int]]:
    length2tour = dict({})

    # n.n algorithm
    for starter in G.nodes(data=False):
        local_best_tour, local_min_length = nearest_neighbor(G, [starter])
        length2tour[local_min_length] = local_best_tour

    # 2-opt with time limits
    if opt:
        lengths = sorted(list(length2tour.keys()))
        index = 0
        tic = time.perf_counter()
        while time.perf_counter() - tic < lim:
            opt_local_best_tour, opt_local_min_length = two_opt(length2tour[lengths[index]])
            length2tour[opt_local_min_length] = opt_local_best_tour
            index += 1
    return length2tour
