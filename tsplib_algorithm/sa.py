# https://en.wikipedia.org/wiki/2-opt
import math
import numpy as np
import time
from typing import List, Dict

import networkx as nx
import random

from tsplib_algorithm.opt import do_two_opt
from tsplib_utils.parser import TSPParser


def perturb(permutation: List[int], option=None) -> List[int]:
    perturbed = permutation[:]
    if option is None:
        op = random.choice(["insert", "insert", "insert", "insert",
                            "switch", "switch", "2_opt", "2_opt",
                            "chunk_end_insert", "chunk_end_insert", "chunk_end_insert"])
    else:
        op = option

    if op == "insert":
        # which to remove
        i = random.randint(0, len(perturbed) - 1)
        n = perturbed.pop(i)
        # where to insert
        j = random.randint(0, len(perturbed) + 1)
        perturbed.insert(j, n)

    elif op == "chunk_end_insert":
        # [from, to)
        f = random.randint(0, len(perturbed) // 2)
        t = f + random.randint(1, len(perturbed) // 2)
        # chunk end insert
        perturbed = perturbed[:f] + perturbed[t:] + perturbed[f:t]

    elif op == "2_opt":
        i = random.randint(0, len(perturbed) - 3)
        j = random.randint(i + 2, len(perturbed) - 1)
        temp = perturbed[:]
        temp[i + 1:j + 1] = temp[j:i:-1]
        perturbed = temp

    elif op == "switch":
        i = random.randint(0, len(perturbed) - 1)
        j = random.randint(0, len(perturbed) - 1)
        perturbed[i], perturbed[j] = perturbed[j], perturbed[i]
    else:
        assert False

    return perturbed


def anneal(permutation: List[int], temperature=10e5, eps=10e-5, alpha=0.97) -> None:
    # FIXME whether hyperparameters need fine-tuning
    permutation = perturb(permutation)
    while temperature > eps:
        E0 = TSPParser.length_of_a_tour(permutation)

        novel_permutation = perturb(permutation)
        E1 = TSPParser.length_of_a_tour(novel_permutation)

        delta = E1 - E0

        # FIXME RuntimeWarning: overflow encountered in exp
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            permutation = novel_permutation

        temperature *= alpha


def do_stimulated_annealing(promising_permutation: List[int], lim=500) -> None:
    tic = time.perf_counter()
    while time.perf_counter() - tic < lim:
        # FIXME whether sheer randomness would be better?
        anneal(random.choice(promising_permutation))
