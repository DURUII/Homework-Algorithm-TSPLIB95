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
        op = random.choice(["3_opt" for _ in range(10)]
                           + ["2_opt" for _ in range(8)]
                           + ["switch", "insert", "permutation-transform"])
    else:
        op = option

    if op == "insert":
        for _ in range(random.randint(1, len(permutation) // 10)):
            # which to remove
            i = random.randint(0, len(perturbed) - 1)
            n = perturbed.pop(i)
            # where to insert
            j = random.randint(0, len(perturbed) + 1)
            while j == i:
                j = random.randint(0, len(perturbed) + 1)
            perturbed.insert(j, n)

    elif op == "2_opt":
        # edge <i, i+1>
        i = random.randint(0, len(perturbed) - 4)
        # edge <j, j+1>
        j = random.randint(i + 2, len(perturbed) - 2)
        temp = perturbed[:]
        temp[i + 1:j + 1] = temp[j:i:-1]
        perturbed = temp

    elif op == "3_opt":
        # edge <i, i+1>
        i = random.randint(0, len(perturbed) - 6)
        # edge <j, j+1>
        j = random.randint(i + 2, len(perturbed) - 4)
        # edge <k, k+1>
        k = random.randint(j + 2, len(perturbed) - 2)

        odds = random.randint(1, 4)
        if odds == 1:
            temp = perturbed[:i + 1] + perturbed[k:j:-1] + perturbed[i + 1:j + 1] + perturbed[k + 1:]
        elif odds == 2:
            temp = perturbed[:i + 1] + perturbed[j + 1:k + 1] + perturbed[i + 1:j + 1] + perturbed[k + 1:]
        elif odds == 3:
            temp = perturbed[:i + 1] + perturbed[j + 1:k + 1] + perturbed[j:i:-1] + perturbed[k + 1:]
        # elif odds == 4:
        #     temp = perturbed[:i + 1] + perturbed[i + 1:j + 1] + perturbed[k:j:-1] + perturbed[k + 1:]
        # elif odds == 5:
        #     temp = perturbed[:i + 1] + perturbed[j:i:-1] + perturbed[j + 1:k + 1] + perturbed[k + 1:]
        # elif odds == 6:
        #     temp = perturbed[:i + 1] + perturbed[k: i:-1] + perturbed[k + 1:]
        else:
            temp = perturbed[:i + 1] + perturbed[j:i:-1] + perturbed[k:j:-1] + perturbed[k + 1:]

        perturbed = temp

    elif op == "switch":
        for _ in range(random.randint(1, len(permutation) // 10)):
            i = random.randint(1, len(perturbed) - 2)
            j = random.randint(i + 1, len(perturbed) - 1)
            perturbed[i], perturbed[j] = perturbed[j], perturbed[i]

    else:
        i = random.randint(1, len(permutation) - 1)
        perturbed = perturbed[i:] + perturbed[:i]

    return perturbed


def anneal(permutation: List[int], temperature, eps, alpha, max_iterations) -> None:
    # FIXME whether hyperparameters need fine-tuning
    # permutation = perturb(permutation)
    counter = 0
    while counter <= max_iterations and temperature > eps:
        counter += 1
        for _ in range(max(int(temperature), 10)):
            E0 = TSPParser.length_of_a_tour(permutation)
            novel_permutation = perturb(permutation)
            # print(novel_permutation)
            E1 = TSPParser.length_of_a_tour(novel_permutation)
            delta = E1 - E0

            if delta < 0:
                permutation = novel_permutation
                # still improving
                counter = 0

            elif random.random() < np.exp(-delta / temperature):
                permutation = novel_permutation

            temperature *= alpha


def do_stimulated_annealing(lim=500, temperature=200, eps=20, alpha=0.99, max_iterations=25) -> None:
    tic = time.perf_counter()
    while time.perf_counter() - tic < lim:
        # FIXME whether sheer randomness or the record best would be better?
        anneal(TSPParser.G.graph['x_tour'], temperature, eps, alpha, max_iterations)
