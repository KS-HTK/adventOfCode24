# -*- coding: utf-8 -*-

import os
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def count_combinations(towels, design):
    dp = [0] * (len(design) + 1)
    dp[0] = 1

    for i in range(1, len(design) + 1):
        for towel in towels:
            if design.startswith(towel, i - len(towel)):
                dp[i] += dp[i - len(towel)]

    return dp[len(design)]


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n\n')]
        towels = content[0].split(', ')
        designs = content[1].split('\n')
    return towels, designs


@profiler
def solve():
    towels, designs = get_input()
    options = [count_combinations(towels, d) for d in designs]
    print(f'Part 1: {sum([True for v in options if v])}')
    print(f'Part 2: {sum(options)}')


if __name__ == "__main__":
    solve()
