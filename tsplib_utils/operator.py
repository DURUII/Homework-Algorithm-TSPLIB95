import random
import math
from tsplib_problem.base import Problem
import numpy as np


##############################
#########  MUTATION  #########
##############################

def naive_swap(ll: list[int], problem=None):
    # Pick two alleles at random and swap their positions
    ll = ll[:]
    i, j = random.choices(range(len(ll)), k=2)
    ll[i], ll[j] = ll[j], ll[i]
    return ll


def chunk_swap(ll: list[int], problem=None):
    ll = ll[:]
    i, j, p, q = random.sample(range(len(ll)), k=4)
    i, j, p, q = sorted((i, j, p, q))
    ll = ll[:i] + ll[p:q + 1] + ll[j + 1:p] + ll[i:j + 1] + ll[q + 1:]
    return ll


def naive_insert(ll: list[int], problem=None):
    # Pick two allele values at random, Move the second to follow the first
    ll = ll[:]
    i, j = random.choices(range(len(ll)), k=2)
    (i, j) = sorted((i, j))
    ll.insert(i + 1, ll.pop(j))
    return ll


def greedy_insert(ll: list[int], problem: Problem):
    tour = ll[:]
    if random.random() < 0.1:
        times = max(min(int(abs(np.random.normal(10, 10))), problem.dimension // 2), 1)
    else:
        times = max(min(int(abs(np.random.normal(2, 1))), problem.dimension // 2), 1)

    if random.random() < 0.3:
        conductor = [tour.pop(random.randint(1, len(tour) - 2)) for _ in range(times)]
    else:
        pivot = random.randint(1, 1 + times)
        conductor = [tour.pop(pivot) for _ in range(times)]

    for i in range(len(conductor)):
        vertex = conductor[i]
        tour.append(tour[0])
        best_gain, best_idx = math.inf, -1
        for j in range(1, len(tour)):
            # logically, do tour.insert(j, conductor[i]), say j=1, [1, 4, 2, 3]
            assert tour[j - 1] != vertex
            assert vertex != tour[j]
            assert tour[j - 1] != tour[j]
            gain = problem.get_distance(tour[j - 1], vertex) + \
                   problem.get_distance(vertex, tour[j]) - \
                   problem.get_distance(tour[j - 1], tour[j])

            # where to insert you can minimize the total length gain with high probability
            if gain < best_gain and random.random():
                best_gain, best_idx = gain, j
        del tour[-1]
        # insert the emergent city into the tour
        tour.insert(best_idx, vertex)
    return tour


def chunk_insert(ll: list[int], problem=None):
    ll = ll[:]
    i, j, k = random.sample(range(len(ll)), k=3)
    # Move [i, j] to k
    (i, j, k) = sorted((i, j, k))
    for _ in range(i, j + 1):
        ll.insert(random.randint(k, len(ll) - 1) + 1, ll.pop(i))
        k = k - 1
    return ll


def naive_reverse(ll: list[int], problem=None):
    # Pick two alleles at random and then invert the substring between them.
    ll = ll[:]
    i, j = random.choices(range(1, len(ll)), k=2)
    (i, j) = sorted((i, j))
    ll[i:j + 1] = ll[j:i - 1:-1]
    return ll


def opt_swap_2(ll: list[int], problem=None):
    ll = ll[:]

    # edge <i, i+1>
    i = random.randint(0, len(ll) - 4)
    # edge <j, j+1>
    j = random.randint(i + 2, len(ll) - 2)

    ll[i + 1:j + 1] = ll[j:i:-1]
    return ll


def opt_swap_3(ll: list[int], problem=None):
    # edge <i, i+1>
    i = random.randint(0, len(ll) - 6)
    # edge <j, j+1>
    j = random.randint(i + 2, len(ll) - 4)
    # edge <k, k+1>
    k = random.randint(j + 2, len(ll) - 2)

    odds = random.randint(1, 4)
    if odds == 1:
        return ll[:i + 1] + ll[k:j:-1] + ll[i + 1:j + 1] + ll[k + 1:]
    elif odds == 2:
        return ll[:i + 1] + ll[j + 1:k + 1] + ll[i + 1:j + 1] + ll[k + 1:]
    elif odds == 3:
        return ll[:i + 1] + ll[j + 1:k + 1] + ll[j:i:-1] + ll[k + 1:]
    else:
        return ll[:i + 1] + ll[j:i:-1] + ll[k:j:-1] + ll[k + 1:]


##############################
######### CROSSOVER #########
##############################


def ox(p1: list[int], p2: list[int]):
    """order crossover (OX)"""

    # Choose an arbitrary part from the parent
    i, j = random.sample(range(1, len(p1) - 1), k=2)
    i, j = sorted((i, j))

    def breed(mother, father):
        nonlocal i, j
        # Copy this part to the first child
        offspring = [0 for _ in range(len(mother))]
        offspring[i:j] = mother[i:j]

        # Copy the numbers that are not in the first part, to the first child:
        existed = set(offspring[i:j])
        writer = 0
        for p in range(len(father)):
            if writer >= len(offspring):
                break

            while offspring[writer] != 0:
                writer += 1

            # using the order of the second parent
            if father[p] not in existed:
                offspring[writer] = father[p]
                existed.add(father[p])
                writer += 1

        return offspring

    return breed(p1, p2), breed(p2, p1)


def pmx(p1: list[int], p2: list[int]):
    """partially mapped crossover (PMX)"""
    i, j = random.sample(range(1, len(p1) - 2), k=2)
    i, j = sorted((i, j))

    # naive crossover
    o1 = p1[:i] + p2[i:j + 1] + p1[j + 1:]
    o2 = p2[:i] + p1[i:j + 1] + p2[j + 1:]

    # mapping
    mapping, circles = {}, []
    for idx in range(i, j + 1):
        if p1[idx] not in mapping and p2[idx] not in mapping:
            circles.append([p1[idx], p2[idx]])
            mapping[p1[idx]] = len(circles) - 1
            mapping[p2[idx]] = len(circles) - 1
        elif p1[idx] not in mapping:
            mapping[p1[idx]] = mapping[p2[idx]]
            circles[mapping[p2[idx]]].append(p1[idx])
        elif p2[idx] not in mapping:
            mapping[p2[idx]] = mapping[p1[idx]]
            circles[mapping[p1[idx]]].append(p2[idx])
        else:
            circles[mapping[p1[idx]]].extend(circles[mapping[p2[idx]]])
            for e in circles[mapping[p2[idx]]]:
                mapping[e] = mapping[p1[idx]]

    # resolve conflict
    used = set(o1[i:j + 1])
    for idx in range(len(o1)):
        if (idx < i or idx > j) and o1[idx] in used:
            for n in circles[mapping[o1[idx]]]:
                if n not in used and n != o1[idx]:
                    o1[idx] = n
                    used.add(n)
                    break

    used = set(o2[i:j + 1])
    for idx in range(len(o2)):
        if (idx < i or idx > j) and o2[idx] in used:
            for n in circles[mapping[o2[idx]]]:
                if n not in used and n != o1[idx]:
                    o2[idx] = n
                    used.add(n)
                    break

    return o1, o2
