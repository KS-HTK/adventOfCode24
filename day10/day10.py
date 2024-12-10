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

def find_trails(map, start):
    seen = set()
    ends = set()
    stack = [(start, )]
    len_y = len(map)
    len_x = len(map[0])
    while stack:
        trail = stack.pop()
        x, y = trail[-1]
        num = map[y][x]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            new_trail = (*trail, (x+dx, y+dy))
            if 0 <= nx < len_x and 0 <= ny < len_y and map[y+dy][x+dx] == num+1 and new_trail not in seen:
                if map[y+dy][x+dx] == 9:
                    ends.add(new_trail)
                    continue
                stack.append(new_trail)
    return {(t[0], t[-1]) for t in ends}, ends

# Part 1 and 2:
def part(content = None,) -> tuple[int, int]:
    trailheads = [(x, y) for y, l in enumerate(content) for x, n in enumerate(l) if n == 0]
    end_counts1 = []
    end_counts2 = []
    for head in trailheads:
        ends1, ends2 = find_trails(content, head)
        end_counts1.append(len(ends1))
        end_counts2.append(len(ends2))
    return sum(end_counts1), sum(end_counts2)

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [[int(c) for c in line] for line in content]
    return content

@profiler
def solve():
    content = get_input()
    pt1, pt2 = part(content)
    print(f'Part 1: {pt1}')
    print(f'Part 2: {pt2}')

if __name__ == "__main__":
    solve()