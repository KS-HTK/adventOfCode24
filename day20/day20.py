# -*- coding: utf-8 -*-

import os
from time import perf_counter
from collections import deque
from itertools import combinations


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def bfs(maze, start, end):
    queue = deque([(start[0], start[1], 0)])
    dists = {}
    while queue:
        y, x, n = queue.popleft()
        if (y, x) in dists:
            continue
        dists[(y, x)] = n
        if (y, x) == end:
            continue

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#":
                queue.append((ny, nx, n + 1))
    return dists


def part(maze, start, end) -> tuple[int, int]:
    dists = bfs(maze, start, end)
    pt1 = pt2 = 0
    for ((r1, c1), n1), ((r2, c2), n2) in combinations(dists.items(), 2):
        d = abs(r1 - r2) + abs(c1 - c2)
        if d <= 20 and abs(n2 - n1) >= d + 100:
            pt2 += 1
            if d <= 2:
                pt1 += 1
    return pt1, pt2


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [list(s.strip()) for s in f.read().rstrip().split('\n')]
    start = end = None
    for y, row in enumerate(content):
        for x, c in enumerate(row):
            if c == 'S':
                start = (y, x)
            if c == 'E':
                end = (y, x)
    return content, start, end


@profiler
def solve():
    pt1, pt2 = part(*get_input())
    print(f'Part 1: {pt1}')
    print(f'Part 2: {pt2}')


if __name__ == "__main__":
    solve()
