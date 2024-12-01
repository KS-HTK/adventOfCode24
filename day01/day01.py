# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

# Part 1:
def part1(content = None) -> int:
    list1, list2 = list(zip(*content))
    list1 = sorted(list1)
    list2 = sorted(list2)

    dists = [abs(l2-l1) for l1, l2 in zip(list1, list2)]

    return sum(dists)

# Part 2:
def part2(content = None) -> int:
    left, right = list(zip(*content))
    left = sorted(left)
    right = sorted(right)

    sim_score = 0
    for num in left:
        occ = right.count(num)
        sim_score += occ*num

    return sim_score

def get_input() -> list[tuple[int, int]]:
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        file_content = [s.strip() for s in f.read().rstrip().split('\n')]
        pattern = re.compile(r"^(\d*)\s*(\d*)")
        content = []
        for s in file_content:
            match = pattern.match(s)
            content.append((int(match.group(1)), int(match.group(2))))
    return content

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
    solve()
