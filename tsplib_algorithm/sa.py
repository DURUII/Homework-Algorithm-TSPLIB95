# https://en.wikipedia.org/wiki/2-opt
import math
import numpy as np
import time
from typing import List, Dict

import networkx as nx
import random

from tsplib_algorithm.opt import two_opt
from tsplib_utils.parser import TSPParser


def perturb(permutation: List[int]) -> List[int]:
    perturbed = permutation[:]
    operation = random.choice(["insert", "chunk_end_insert", "switch"])
    if operation == "insert":
        # which to remove
        i = random.randint(0, len(perturbed) - 1)
        n = perturbed.pop(i)
        # where to insert
        j = random.randint(0, len(perturbed) + 1)
        perturbed.insert(j, n)

    elif operation == "chunk_end_insert":
        # [from, to)
        f = random.randint(0, len(perturbed) // 2)
        t = f + random.randint(1, len(perturbed) // 2)
        # chunk end insert
        perturbed = perturbed[:f] + perturbed[t:] + perturbed[f:t]

    elif operation == "switch":
        i = random.randint(0, len(perturbed) - 1)
        j = random.randint(0, len(perturbed) - 1)
        perturbed[i], perturbed[j] = perturbed[j], perturbed[i]
    else:
        assert False

    return perturbed


def anneal(permutation: List[int], temperature=10e5, eps=10e-5, alpha=0.99):
    permutation = permutation[:]

    while temperature > eps:
        E0 = TSPParser.length_of_a_tour(permutation)

        novel_permutation = perturb(permutation)
        E1 = TSPParser.length_of_a_tour(novel_permutation)

        delta = E1 - E0

        if random.random() < np.exp(-delta / temperature):
            permutation = novel_permutation
        temperature *= alpha

        two_opt(permutation)


def do_stimulated_annealing(promising_length2tour: Dict[int, List[int]], lim=math.inf):
    lengths = sorted(list(promising_length2tour.keys()))
    index = 0
    tic = time.perf_counter()
    while time.perf_counter() - tic < lim:
        anneal(promising_length2tour[lengths[index]])
        index += 1
