# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import Literal, Optional

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def get_guard_route(
        board: dict[complex, Literal['.', '#', 'X']],
        pos: complex,
) -> Optional[set[complex]]:
    direction = 0-1j
    seen = set()
    while True:
        key = (pos, direction)
        if key in seen:
            return None
        seen.add(key)

        neo_pos = pos+direction
        if neo_pos not in board:
            return {c for c, _ in seen}
        match board[neo_pos]:
            case '.':
                board[neo_pos] = 'X'
                pos = neo_pos
            case 'X':
                pos = neo_pos
            case '#':
                direction = -direction.imag+1j*direction.real

# Part 1:
def part1(board, start_pos) -> int:
    return len(get_guard_route(board, start_pos))

# Part 2:
def part2(board, start_pos) -> int:
    return sum(
        get_guard_route(board | {pos: '#'}, start_pos) is None for pos in get_guard_route(board, start_pos)
    )

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    board = {x + 1j * y: c for y, l in enumerate(content) for x, c in enumerate(l)}
    pos = [x + 1j * y for y, l in enumerate(content) for x, c in enumerate(l) if c == '^'][0]
    board[pos] = 'X'
    return board, pos

@profiler
def solve():
    board, pos = get_input()
    print(f'Part 1: {part1(board, pos)}')
    print(f'Part 2: {part2(board, pos)}')

if __name__ == "__main__":
    solve()