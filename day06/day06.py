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

INVALID: tuple[int, int, int] = (-1, -1, -1)
DIRECTIONS: list[tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]

width: int = 0
height: int = 0
start_pos: tuple[int, int, int] = (0, 0, 0)

map_: list[list[list[tuple[int, int, int]]]] = []
visited: list[tuple[int, int, int]] = []

def off_map(x: int, y: int) -> bool:
    return not (0 <= x < width and 0 <= y < height)

# Part 1:
def part1() -> int:
    global start_pos, map_, visited
    pos = start_pos
    while not pos == INVALID:
        x, y, d = pos
        visited.append(pos)
        pos = map_[x][y][d]
    return len({(x, y) for x, y, _ in visited})

# Part 2:
def part2() -> int:
    global INVALID, DIRECTIONS, width, height, visited
    loop_obstacles = [[False for _ in range(height)] for _ in range(width)]
    not_loop_obstacles = [[False for _ in range(height)] for _ in range(width)]
    seen = [[[0 for _ in range(4)] for _ in range(height)] for _ in range(width)]
    for i, pos in enumerate(visited[1:], 1):
        x, y, _ = pos
        if loop_obstacles[x][y] or not_loop_obstacles[x][y]:
            continue
        # modify the map surrounding the new obstacle
        for d, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = (x-dx, y-dy)
            if off_map(nx, ny):
                continue
            map_[nx][ny][d] = (nx, ny, (d+1) % 4)
        # check if valid obstacle
        cx, cy, cd = visited[i-1]
        while not (cx, cy, cd) == INVALID and not seen[cx][cy][cd] == i:
            seen[cx][cy][cd] = i
            cx, cy, cd = map_[cx][cy][cd]
        if (cx, cy, cd) == INVALID:
            not_loop_obstacles[x][y] = True
        else:
            loop_obstacles[x][y] = True
        # reset the map surrounding the new obstacle
        for d, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = (x-dx, y-dy)
            if off_map(nx, ny):
                continue
            map_[nx][ny][d] = (x, y, d)
    return sum(sum(row) for row in loop_obstacles)

def get_input() -> None:
    global INVALID, DIRECTIONS, width, height, start_pos, map_
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]

    width, height = (len(content[0]), len(content))
    map_ = [[[(x, y, d) for d in range(4)] for y in range(height)] for x in range(width)]

    obstacles = [[False for _ in range(height)] for _ in range(width)]

    for x, y in [(x, y) for x in range(width) for y in range(height)]:
        match content[y][x]:
            case '#':
                obstacles[x][y] = True
            case '^':
                start_pos = (x, y, 0)

    for x, y, d in [(x, y, d) for x in range(width) for y in range(height) for d in range(4)]:
        dx, dy = DIRECTIONS[d]
        if off_map(x+dx, y+dy):
            map_[x][y][d] = INVALID
        elif obstacles[x+dx][y+dy]:
            map_[x][y][d] = (x, y, (d+1) % 4)
        else:
            map_[x][y][d] = (x+dx, y+dy, d)

@profiler
def solve():
    get_input()
    print(f'Part 1: {part1()}')
    print(f'Part 2: {part2()}')

if __name__ == "__main__":
    solve()
