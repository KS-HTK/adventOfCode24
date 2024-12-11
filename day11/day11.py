# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import Optional
from collections import defaultdict

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

stone_counts: dict[int, int] = defaultdict(int)

def blink(blinks, stones: Optional[list[int]]= None):
    global stone_counts
    if stones:
        for stone in stones:
            stone_counts[stone] += 1
    for _ in range(blinks):
        new_stone_counts = defaultdict(int)
        for stone, count in stone_counts.items():
            if stone == 0:
                new_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                mid = len(str_stone) // 2
                new_stone_counts[int(str_stone[:mid])] += count
                new_stone_counts[int(str_stone[mid:])] += count
            else:
                new_stone_counts[stone * 2024] += count
        stone_counts = new_stone_counts
    return sum(stone_counts.values())

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [int(c) for c in content[0].split(' ')]
    return content

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {blink(25, content)}')
    print(f'Part 2: {blink(50)}')

if __name__ == "__main__":
    solve()