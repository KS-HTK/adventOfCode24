# -*- coding: utf-8 -*-

import os
from time import perf_counter
import heapq

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def find_all_best_paths(maze):
    start = end = None
    for i, row in enumerate(maze):
        if 'S' in row:
            start = (i, row.index('S'))
        if 'E' in row:
            end = (i, row.index('E'))

    priority_queue = [(0, start[0], start[1], (0, 1), [])]
    min_score = float('inf')
    best_path_tiles = set()
    visited = {}

    while priority_queue:
        score, x, y, (dx, dy), path = heapq.heappop(priority_queue)
        current_path = path + [(x, y)]

        if (x, y) == end:
            if score < min_score:
                min_score = score
                best_path_tiles = set(current_path)
            elif score == min_score:
                best_path_tiles.update(current_path)
            continue

        state_key = (x, y, (dx, dy))
        if state_key in visited and visited[state_key] < score:
            continue
        visited[state_key] = score

        for (dx, dy), penalty in [((dx, dy), 1), ((-dy, dx), 1001), ((dy, -dx), 1001)]:
            if 0 <= x + dx < len(maze[0]) and 0 <= y + dy < len(maze) and maze[x + dx][y + dy] != '#':
                heapq.heappush(priority_queue, (score + penalty, x + dx, y + dy, (dx, dy), current_path))
    return min_score, len(best_path_tiles)

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    return content

@profiler
def solve():
    content = get_input()
    min_score, tiles = find_all_best_paths(content)
    print(f'Part 1: {min_score}')
    print(f'Part 2: {tiles}')

if __name__ == "__main__":
    solve()
