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

def calculate_areas_and_sides(map) -> list[tuple[int, set[tuple[int, int, int]]]]:
    rows = len(map)
    cols = len(map[0])
    visited = [[False] * cols for _ in range(rows)]

    def dfs(x: int, y: int, plant_type: str) -> tuple[int, set[tuple[int, int, int]]]:
        stack: list[tuple[int, int]] = [(x, y)]
        area: int = 0
        perimeter: set[tuple[int, int, int]] = set()

        while stack:
            x, y = stack.pop()
            if visited[y][x]:
                continue
            visited[y][x] = True
            area += 1
            for di, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < cols and 0 <= ny < rows) or map[ny][nx] != plant_type:
                    perimeter.add((x, y, di))
                else:
                    stack.append((nx, ny))
        return area, perimeter

    return [dfs(x, y, map[y][x]) for x in range(rows) for y in range(cols) if not visited[y][x]]

# Part 1:
def part1(content: list[str]) -> int:
    return sum(a*len(p) for a, p in calculate_areas_and_sides(content))

# Part 2:
def part2(content: list[str]) -> int:
    areas = calculate_areas_and_sides(content)
    total_fencing_cost: int = 0
    for area, perimeter in areas:
        sides: dict[tuple[int, int], list[int]] = {}
        for x, y, d in perimeter:
            if d < 2:
                fixed = x
                var = y
            else:
                fixed = y
                var = x
            if (d, fixed) in sides:
                sides[(d, fixed)].append(var)
            else:
                sides[(d, fixed)] = [var]
        for k, s in sides.items():
            s = sorted(s)
            count = 1
            for i in range(1, len(s)):
                if s[i] != s[i - 1] + 1:
                    count += 1
            sides[k] = count
        total_fencing_cost += area*sum(sides.values())
    return total_fencing_cost

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    return content

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
    solve()
