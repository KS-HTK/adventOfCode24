# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def find_path(maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = (0, 0)
    end = (70, 70)
    visited = set()
    visited.add(start)
    queue = [(start, 0)]
    while len(queue) > 0:
        (node, path) = queue.pop(0)
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
            if next_node == end:
                return path + 1
            if 0 <= next_node[0] < 71 and 0 <= next_node[1] < 71 and next_node not in maze and next_node not in visited:
                visited.add(next_node)
                queue.append((next_node, path + 1))
    return None

# Part 1:
def part1(content=None) -> str | int:
    return find_path(set(content))


# Part 2:
def part2(content=None) -> str:
    maze = set(content)
    next_remove = len(content) - 1
    path = find_path(maze)
    while path is None:
        rm = content[next_remove]
        next_remove -= 1
        maze.remove(rm)
        path = find_path(maze)
    return ','.join(map(str, content[next_remove+1]))


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [tuple(map(int, re.findall(r"\d+", l))) for l in content]
    return content


@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content[:1024])}')
    print(f'Part 2: {part2(content)}')


if __name__ == "__main__":
    solve()
