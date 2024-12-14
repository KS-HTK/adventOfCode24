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

WIDTH: int = 101
HEIGHT: int = 103

def move_bots(robots):
    new_bots = {}
    for (x, y), lst in robots.items():
        for dx, dy in lst:
            nx = (x + dx) % WIDTH
            ny = (y + dy) % HEIGHT
            if (nx, ny) in new_bots:
                new_bots[(nx, ny)].append((dx, dy))
            else:
                new_bots[(nx, ny)] = [(dx, dy)]
    return new_bots


# Part 1:
def part1(robots) -> str|int:
    for _ in range(100):
        robots = move_bots(robots)

    bots = [0, 0, 0, 0]
    wh = WIDTH//2
    hh = HEIGHT//2
    for y in range(hh):
        for x in range(wh):
            if (x, y) in robots:
                bots[0] += len(robots[(x, y)])
            if (x+wh+1, y) in robots:
                bots[1] += len(robots[(x+wh+1, y)])
            if (x+wh+1, y+hh+1) in robots:
                bots[2] += len(robots[(x+wh+1, y+hh+1)])
            if (x, y+hh+1) in robots:
                bots[3] += len(robots[(x, y+hh+1)])
    for i, x in enumerate(bots):
        if not x:
            bots[i] = 1
    return bots[0]*bots[1]*bots[2]*bots[3]

# Part 2:
def part2(robots) -> int:
    s = 0
    while True:
        s += 1
        robots = move_bots(robots)
        if all([len(x) == 1 for x in robots.values()]):
            # print(s)
            # for y in range(HEIGHT):
            #     for x in range(WIDTH):
            #         if (x, y) in robots:
            #             print(len(robots[(x, y)]), end='')
            #         else:
            #             print(' ', end='')
            #     print()
            # print()
            break
    return s

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [list(map(int, re.findall(r'-?\d+', line))) for line in content]
        robots = {}
        for x, y, dx, dy in content:
            if (x, y) in robots:
                robots[(x, y)].append((dx, dy))
            else:
                robots[(x, y)] = [(dx, dy)]
        return robots

@profiler
def solve():
    robots = get_input()
    print(f'Part 1: {part1(robots)}')
    print(f'Part 2: {part2(robots)}')

if __name__ == "__main__":
    solve()
