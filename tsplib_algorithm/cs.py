from typing import List, Dict, Set

import networkx as nx
from matplotlib import pyplot as plt

from tsplib_algorithm.opt import two_opt
from tsplib_utils.helper import plot_tsp_tour
from tsplib_utils.parser import TSPParser


def visualize_procedure(G: nx.Graph,
                        T: nx.Graph,
                        odd_vertices: Set[int],
                        matching,
                        G_prime: nx.Graph,
                        bypass: List[int]):
    fig, axes = plt.subplots(2, 2, figsize=(8.5, 6.5), layout='constrained', dpi=500)

    # Find MST T of Graph
    ax = axes[0][0]
    for src, dst in T.edges:
        x1, y1 = T.nodes[src]["loc"]
        x2, y2 = T.nodes[dst]["loc"]
        ax.plot([x1, x2], [y1, y2], color="C0", marker='o', linestyle='-', linewidth=1, markersize=2)

    xs, ys = [], []
    for i in range(T.number_of_nodes()):
        if (T.degree[i + 1] % 2) != 0:
            odd_vertices.add(i + 1)
            xs.append(T.nodes[i + 1]["loc"][0])
            ys.append(T.nodes[i + 1]["loc"][1])
    ax.scatter(xs, ys, color="r", s=15, zorder=1)
    ax.set_title(f"{G.graph['benchmark']}'s Minimum Spanning Tree")

    # Isolate Set of Odd-Degree Vertices S
    # Find Min Weight Perfect Matching M of S
    ax = axes[0][1]
    for src, dst in matching:
        x1, y1 = G_prime.nodes[src]["loc"]
        x2, y2 = G_prime.nodes[dst]["loc"]
        ax.plot([x1, x2], [y1, y2], color="r", marker='o', linestyle='-', linewidth=1, markersize=2)
    ax.set_title(f"{G.graph['benchmark']}'s Perfect Matching")

    # Combine T and M into Multi-graph G
    ax = axes[1][0]
    for src, dst in T.edges:
        x1, y1 = T.nodes[src]["loc"]
        x2, y2 = T.nodes[dst]["loc"]
        ax.plot([x1, x2], [y1, y2], color="C0", alpha=0.5, marker='o', linestyle='-', linewidth=1, markersize=2)

    for src, dst in matching:
        x1, y1 = G_prime.nodes[src]["loc"]
        x2, y2 = G_prime.nodes[dst]["loc"]
        ax.plot([x1, x2], [y1, y2], color="r", alpha=0.5, marker='o', linestyle='-', linewidth=2, markersize=2)

    ax.set_title(f"{G.graph['benchmark']}'s Union of T and M")

    #  Generate Shortcut TSP Tour from Eulerian Tour
    ax = axes[1][1]
    plot_tsp_tour(ax, "C0", G, bypass)
    uuid = f"{G.graph['benchmark']}'s procedure and experiment result - {TSPParser.length_of_a_tour(bypass)}"
    ax.set_title(uuid)
    plt.savefig(f"{uuid}")
    plt.show()


def do_christofides_serdyukov(G: nx.Graph, visualize=True, opt=True) -> Dict[int, List[int]]:
    # Find MST T of Graph
    T = nx.minimum_spanning_tree(G)

    # Isolate Set of Odd-Degree Vertices S
    odd_vertices = set({})
    for i in range(T.number_of_nodes()):
        if T.degree[i + 1] % 2 != 0:
            odd_vertices.add(i + 1)

    # Find Min Weight Perfect Matching M of S
    G_prime = nx.Graph(G)
    for i in range(G_prime.number_of_nodes()):
        if i + 1 not in odd_vertices:
            G_prime.remove_node(i + 1)
    perf_matching = nx.min_weight_matching(G_prime)

    # Combine T and M into Multi-graph G
    Union = nx.MultiGraph()
    Union.add_edges_from(T.edges)
    Union.add_edges_from(perf_matching)

    # Generate Eulerian Tour of G
    euler_circuit = [u for u, v in nx.eulerian_circuit(Union)]

    #  Generate Shortcut TSP Tour from Eulerian Tour
    visited = set({})
    shortcut = []
    for i in euler_circuit:
        if i not in visited:
            visited.add(i)
            shortcut.append(i)

    # Visualization
    if visualize:
        visualize_procedure(G, T, odd_vertices, perf_matching, G_prime, shortcut)

    # Results Optimization
    length2tour = dict({})
    local_best_tour, local_min_length = shortcut, TSPParser.length_of_a_tour(shortcut)
    length2tour[local_min_length] = local_best_tour
    if opt:
        opt_local_best_tour, opt_local_min_length = two_opt(shortcut)
        length2tour[opt_local_min_length] = opt_local_best_tour

    return length2tour
