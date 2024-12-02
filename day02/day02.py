# -*- coding: utf-8 -*-

import os
from time import perf_counter

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def is_safe(row: list[int]) -> bool:
    if row[0] - row[1] > 0:
        for ind in range(len(row)-1):
            if not 0 < row[ind] - row[ind+1] < 4:
                return False
    else:
        for ind in range(len(row)-1):
            if not 0 > row[ind] - row[ind+1] > -4:
                return False
    return True

# Part 1:
def part1(content = None) -> str|int:
    return sum(map(is_safe, content))

# Part 2:
def part2(content = None) -> str|int:
    counter = 0
    for row in content:
        if is_safe(row):
            counter += 1
        else:
            for ind in range(len(row)):
                new_row = row.copy()
                new_row.pop(ind)
                if is_safe(new_row):
                    counter += 1
                    break
    return counter

def get_input() -> list[list[int]]:
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        file_content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [[int(d) for d in s.split(' ')] for s in file_content]
    return content

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
    solve()