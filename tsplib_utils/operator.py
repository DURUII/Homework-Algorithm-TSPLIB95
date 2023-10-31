import random

import numpy as np


##############################
#########  MUTATION  #########
##############################

def naive_swap(ll: list[int]):
    # Pick two alleles at random and swap their positions
    ll = ll[:]
    i, j = random.choices(range(len(ll)), k=2)
    ll[i], ll[j] = ll[j], ll[i]
    return ll


def naive_insert(ll: list[int]):
    # Pick two allele values at random, Move the second to follow the first
    ll = ll[:]
    i, j = random.choices(range(len(ll)), k=2)
    (i, j) = sorted((i, j))
    ll.insert(i + 1, ll.pop(j))
    return ll


def naive_reverse(ll: list[int]):
    # Pick two alleles at random and then invert the substring between them.
    ll = ll[:]
    i, j = random.choices(range(1, len(ll)), k=2)
    (i, j) = sorted((i, j))
    ll[i:j + 1] = ll[j:i - 1:-1]
    return ll


def opt_swap_2(ll: list[int]):
    ll = ll[:]

    # edge <i, i+1>
    i = random.randint(0, len(ll) - 4)
    # edge <j, j+1>
    j = random.randint(i + 2, len(ll) - 2)

    ll[i + 1:j + 1] = ll[j:i:-1]
    return ll


def opt_swap_3(ll: list[int]):
    # edge <i, i+1>
    i = random.randint(0, len(ll) - 6)
    # edge <j, j+1>
    j = random.randint(i + 2, len(ll) - 4)
    # edge <k, k+1>
    k = random.randint(j + 2, len(ll) - 2)

    odds = random.randint(1, 4)
    if odds == 1:
        temp = ll[:i + 1] + ll[k:j:-1] + ll[i + 1:j + 1] + ll[k + 1:]
    elif odds == 2:
        temp = ll[:i + 1] + ll[j + 1:k + 1] + ll[i + 1:j + 1] + ll[k + 1:]
    elif odds == 3:
        temp = ll[:i + 1] + ll[j + 1:k + 1] + ll[j:i:-1] + ll[k + 1:]
    else:
        temp = ll[:i + 1] + ll[j:i:-1] + ll[k:j:-1] + ll[k + 1:]

    return temp


##############################
######### CROSSOVER #########
##############################

def ox(p1: list[int], p2: list[int]):
    """order crossover (OX)"""

    # Choose an arbitrary part from the parent
    i, j = random.choices(range(1, len(p1) - 1), k=2)

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
