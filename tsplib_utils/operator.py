import random
import math
from tsplib_problem.base import Problem
import numpy as np


##############################
#########  MUTATION  #########
##############################

def shuffle(ll: np.array, problem=None):
    i = np.random.randint(1, max(len(ll) // 10, 2))
    return np.roll(ll, -i)


def naive_swap(ll, problem=None):
    # Pick two alleles at random and swap their positions
    i, j = np.random.choice(len(ll), 2, replace=False)
    ll[i], ll[j] = ll[j], ll[i]
    return ll


def chunk_swap(ll: np.array, problem=None):
    i, j, p, q = np.sort(np.random.choice(len(ll), 4, replace=False))
    return np.concatenate([ll[:i], ll[p:q + 1], ll[j + 1:p], ll[i:j + 1], ll[q + 1:]])


def naive_insert(ll: np.array, problem=None):
    # Pick two allele values at random, Move the second to follow the first
    i, j = np.sort(np.random.choice(len(ll), 2, replace=False))
    ll = np.insert(ll, i + 1, ll[j])
    return np.delete(ll, j + 1)


def chunk_insert(ll: np.array, problem=None):
    i, j, k = np.sort(np.random.choice(len(ll), 3, replace=False))
    return np.concatenate([ll[:i], ll[j + 1:k + 1], ll[i:j + 1], ll[k + 1:]])


def naive_reverse(ll: np.array, problem=None):
    # Pick two alleles at random and then invert the substring between them.
    i, j = np.sort(np.random.choice(len(ll) - 1, 2, replace=False) + 1)
    ll[i:j + 1] = ll[j:i - 1:-1]
    return ll


def opt_swap_2(ll: np.array, problem=None):
    i = np.random.randint(0, len(ll) - 4)
    j = np.random.randint(i + 2, len(ll) - 2)
    ll[i + 1:j + 1] = ll[j:i:-1]
    return ll


def opt_swap_3(ll: np.array, problem=None):
    i = np.random.randint(0, len(ll) - 6)
    j = np.random.randint(i + 2, len(ll) - 4)
    k = np.random.randint(j + 2, len(ll) - 2)

    odds = np.random.randint(1, 5)
    if odds == 1:
        return np.concatenate([ll[:i + 1], ll[k:j:-1], ll[i + 1:j + 1], ll[k + 1:]])
    elif odds == 2:
        return np.concatenate([ll[:i + 1], ll[j + 1:k + 1], ll[i + 1:j + 1], ll[k + 1:]])
    elif odds == 3:
        return np.concatenate([ll[:i + 1], ll[j + 1:k + 1], ll[j:i:-1], ll[k + 1:]])
    else:
        return np.concatenate([ll[:i + 1], ll[j:i:-1], ll[k:j:-1], ll[k + 1:]])


##############################
######### CROSSOVER #########
##############################

def ox(p1, p2):
    """order crossover (OX) with NumPy"""
    p1, p2 = np.array(p1), np.array(p2)
    n = len(p1)
    i, j = np.sort(np.random.choice(range(1, n - 1), size=2, replace=False))

    def breed(mother, father):
        offspring = np.zeros(n, dtype=int)
        offspring[i:j] = mother[i:j]
        existed = set(offspring[i:j])
        writer = 0
        for p in father:
            if writer >= n:
                break
            while offspring[writer] != 0:
                writer += 1
            if p not in existed:
                offspring[writer] = p
                existed.add(p)
                writer += 1
        return offspring

    return breed(p1, p2), breed(p2, p1)


def pmx(p1, p2):
    """partially mapped crossover (PMX) with NumPy"""
    p1, p2 = np.array(p1), np.array(p2)
    n = len(p1)
    i, j = np.sort(np.random.choice(range(1, n - 2), size=2, replace=False))

    o1 = np.concatenate([p1[:i], p2[i:j + 1], p1[j + 1:]])
    o2 = np.concatenate([p2[:i], p1[i:j + 1], p2[j + 1:]])

    # mapping
    mapping, circles = {}, []
    for idx in range(i, j + 1):
        if p1[idx] not in mapping and p2[idx] not in mapping:
            circles.append({p1[idx], p2[idx]})
            mapping[p1[idx]] = len(circles) - 1
            mapping[p2[idx]] = len(circles) - 1
        elif p1[idx] not in mapping:
            mapping[p1[idx]] = mapping[p2[idx]]
            circles[mapping[p2[idx]]].add(p1[idx])
        elif p2[idx] not in mapping:
            mapping[p2[idx]] = mapping[p1[idx]]
            circles[mapping[p1[idx]]].add(p2[idx])
        else:
            circles[mapping[p1[idx]]].update(circles[mapping[p2[idx]]])
            for e in circles[mapping[p2[idx]]]:
                mapping[e] = mapping[p1[idx]]

    # resolve conflict
    def resolve_conflict(offspring, used, i, j):
        for idx in range(n):
            if idx < i or idx > j and offspring[idx] in used:
                for n in circles[mapping[offspring[idx]]]:
                    if n not in used and n != offspring[idx]:
                        offspring[idx] = n
                        used.add(n)
                        break
        return offspring

    o1 = resolve_conflict(o1, set(o1[i:j + 1]), i, j)
    o2 = resolve_conflict(o2, set(o2[i:j + 1]), i, j)

    return o1, o2
