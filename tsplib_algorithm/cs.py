import networkx as nx
from matplotlib import pyplot as plt

from tsplib_algorithm.base import Algorithm
from tsplib_instance.base import Instance
from tsplib_utils.helper import plot_tsp_tour


class ChristofidesSerdyukov(Algorithm):
    """A great algorithm with approximation ratio 1.5."""

    def __init__(self, tag='ChristofidesSerdyukov'):
        super().__init__(tag)

    def solve(self, problem: Instance, verbose=False):
        # Find MST T of Graph
        T = nx.minimum_spanning_tree(problem.G)

        # Isolate Set of Odd-Degree Vertices S
        odd_vertices = set({})
        for i in range(T.number_of_nodes()):
            if T.degree[i + 1] % 2 != 0:
                odd_vertices.add(i + 1)

        # Find Min Weight Perfect Matching M of S
        G_prime = nx.Graph(problem.G)
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

        # Generate Shortcut TSP Tour from Eulerian Tour
        visited = set({})
        shortcut = []
        for i in euler_circuit:
            if i not in visited:
                visited.add(i)
                shortcut.append(i)

        # Memo the result
        problem.length_of_a_tour(shortcut, leaderboard=True)

        # Visualization
        if visualize:
            visualize_procedure(problem.G, T, odd_vertices, perf_matching, G_prime, shortcut, problem)

        # Log
        if verbose:
            self.print_best_solution(problem)


def visualize_procedure(G: nx.Graph,
                        T: nx.Graph,
                        odd_vertices: set[int],
                        matching,
                        G_prime: nx.Graph,
                        bypass: list[int],
                        problem: Instance) -> None:
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
    ax.set_title(f"{problem.benchmark}'s Minimum Spanning Tree")

    # Isolate Set of Odd-Degree Vertices S
    # Find Min Weight Perfect Matching M of S
    ax = axes[0][1]
    for src, dst in matching:
        x1, y1 = G_prime.nodes[src]["loc"]
        x2, y2 = G_prime.nodes[dst]["loc"]
        ax.plot([x1, x2], [y1, y2], color="r", marker='o', linestyle='-', linewidth=1, markersize=2)
    ax.set_title(f"{problem.benchmark}'s Perfect Matching")

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

    ax.set_title(f"{problem.benchmark}'s Union of T and M")

    #  Generate Shortcut TSP Tour from Eulerian Tour
    ax = axes[1][1]
    plot_tsp_tour(ax, "C0", G, bypass)
    uuid = f"{problem.benchmark}'s procedure and experiment result {problem.best_seen.length}"
    ax.set_title(uuid)
    # plt.savefig(f"{uuid}")
    plt.show()
