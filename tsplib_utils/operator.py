import random

import numpy as np


def naive_swap(ll: list[int]):
    ll = ll[:]
    i, j = random.sample(range(len(ll)), 2)
    ll[i], ll[j] = ll[j], ll[i]
    return ll


def naive_insert(ll: list[int]):
    ll = ll[:]
    # which to remove
    i = random.randint(0, len(ll) - 1)
    n = ll.pop(i)
    # where to insert
    j = random.randint(0, len(ll) + 1)
    while j == i:
        j = random.randint(0, len(ll) + 1)
    ll.insert(j, n)
    return ll


def naive_reserve(ll: list[int]):
    ll = ll[:]
    i = random.randint(1, len(ll) - 2)
    j = random.randint(i + 1, len(ll) - 1)
    ll[i:j + 1] = ll[j:i - 1:-1]
    return ll

def chunk_flip(ll: list[int]):
    i = random.randint(1, len(ll) - 2)
    candidate = [ll[i+1:], ll[:i+1]]
    ll = []
    for i in range(len(candidate)):
        ll.extend(candidate[i])
    return ll


def chunk_swap(ll: list[int]):
    i = random.randint(1, len(ll) - 2)
    j = random.randint(i + 1, len(ll) - 1)

    candidate = [ll[:i], ll[i:j], ll[j:]]
    ll = []
    for i in list(np.random.permutation(3)):
        ll.extend(candidate[i])
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
    # elif odds == 4:
    #     temp = ll[:i + 1] + ll[i + 1:j + 1] + ll[k:j:-1] + ll[k + 1:]
    # elif odds == 5:
    #     temp = ll[:i + 1] + ll[j:i:-1] + ll[j + 1:k + 1] + ll[k + 1:]
    # elif odds == 6:
    #     temp = ll[:i + 1] + ll[k: i:-1] + ll[k + 1:]
    else:
        temp = ll[:i + 1] + ll[j:i:-1] + ll[k:j:-1] + ll[k + 1:]

    return temp


if __name__ == '__main__':
    ll = [1, 2, 3, 4, 5, 6, 7]
    for func in [naive_reserve]:
        ll_new = func(ll)
        print(f'{func.__name__}: {ll_new}')
        assert len(ll_new) == len(ll)
