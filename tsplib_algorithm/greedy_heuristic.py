import math

import numpy as np

from tsplib_parser.tsp_file_parser import TSPParser


def city_nearest_neighbor():
    cost_global = math.inf
    # 起点
    for starter in range(1, TSPParser.dimension + 1):
        path = [starter]
        cost = 0
        # restore the original condition 恢复现场
        visited = [False for i in range(TSPParser.dimension + 1)]
        visited[starter] = True

        while len(path) < TSPParser.dimension:
            for nearest_index in np.argsort(TSPParser.tsp_distance_matrix[path[-1]][:]):
                if not visited[nearest_index] and nearest_index >= 1:
                    visited[nearest_index] = True
                    cost += TSPParser.tsp_distance_matrix[path[-1]][nearest_index]
                    path.append(nearest_index)
                    break

        # print(cost)
        # print(TSPParser.opt_cities_tour, TSPParser.opt_tour_length)
        if cost < cost_global:
            cost_global = cost
            print(cost_global)
            TSPParser.set_a_tour(path, cost)

    TSPParser.plot()
    print(TSPParser.opt_tour_length)


def graph_shortest_path():
    pass
