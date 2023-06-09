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


def proposed_nearest_neighbor(G: nx.Graph, k=5) -> (List[int], int):
    min_length = math.inf
    a_tour = None

    if k == 1:
        # start at a particular city
        for starter in G.nodes(data=False):
            tic = perf_counter()
            a_best_tour, a_min_cost = traditional_neighbor(G, [starter])
            toc = perf_counter()
            if a_min_cost < min_length:
                min_length = a_min_cost
                a_tour = a_best_tour

            print(f"{starter} - {a_min_cost} - {min_length}")
            # print(toc - tic)
            # x_tours.append(a_best_tour)
            # x_tour_lengths.append(a_min_cost)

    else:
        # start at a particular city
        for starter in G.nodes(data=False):
            tic = perf_counter()
            a_best_tour, a_min_cost = inspired_layer_wise_nearest_neighbor(G, [starter], k=k)
            toc = perf_counter()
            print(f"{starter} - {a_min_cost}")
            print(toc - tic)
            # x_tours.append(a_best_tour)
            # x_tour_lengths.append(a_min_cost)

    return a_tour, min_length


def inspired_layer_wise_nearest_neighbor(G: nx.Graph, intermediate_step: List[int], k):
    assert len(intermediate_step) > 0
    print(f"{len(intermediate_step)}-inspired_layer_wise_nearest_neighbor()")

    if len(intermediate_step) >= G.number_of_nodes():
        return intermediate_step, length_of_a_tour(G, intermediate_step)

    # current chessboard
    tour_permutation = [i for i in intermediate_step]
    counter = 0
    best_tour, min_cost = None, math.inf

    while counter <= k:
        # choose the K-nearest city unvisited from the current city
        for neighbor in nns(G, tour_permutation[-1]):
            # unvisited Kth cities
            if neighbor not in tour_permutation:
                counter += 1
                tour_permutation.append(neighbor)
                # from this chessboard, go abroad, but focusing on the final result
                # 当前格局下，以基础算法下探至终止格局
                tour, cost = traditional_neighbor(G, tour_permutation)
                if cost < min_cost:
                    best_tour = tour
                    min_cost = cost
                tour_permutation.pop()

    print(min_cost)
    # choose the best, hoping to go to the best
    inspired_layer_wise_nearest_neighbor(G, [best_tour[i] for i in range(len(tour_permutation) + 1)], k)


def traditional_neighbor(G: nx.Graph, intermediate_step: List[int]) -> (List[int], int):
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
