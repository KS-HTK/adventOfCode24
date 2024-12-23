# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from itertools import combinations
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def build_graph(content):
    graph = defaultdict(set)
    for pc1, pc2 in content:
        graph[pc1].add(pc2)
        graph[pc2].add(pc1)
    return graph


# Part 1:
def part1(graph) -> int:
    return len({
        tuple(sorted([k, k2, k3]))
        for k, v in graph.items()
        for k2, k3 in combinations(v, r=2)
        if k3 in graph[k2] and (k.startswith('t') or k2.startswith('t') or k3.startswith('t'))
    })


# Part 2:
def part2(graph) -> str:
    groups = [[k] for k in graph.keys()]
    for k, v in graph.items():
        for i, group in enumerate(groups):
            if all([node in v for node in group]):
                group.append(k)
    return ','.join(sorted(max(groups, key=len)))


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip().split('-') for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    graph = build_graph(content)
    print(f'Part 1: {part1(graph)}')
    print(f'Part 2: {part2(graph)}')


if __name__ == "__main__":
    solve()
