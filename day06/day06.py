# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import Literal, Optional
from unittest import case


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
        obs: Optional[complex] = None
) -> tuple[Optional[int], dict[complex, Literal['.', '#', 'X']]]:
    board = board.copy()
    direction = 0-1j
    count = 1
    if obs is not None:
        board[obs] = '#'
    seen = set()
    while pos+direction in board:
        key = (pos, direction)
        if key in seen:
            return None, board
        seen.add(key)
        neo_pos = pos+direction
        match board[neo_pos]:
            case '.':
                count += 1
                board[neo_pos] = 'X'
                pos = neo_pos
            case 'X':
                pos = neo_pos
            case '#':
                direction = -direction.imag+1j*direction.real
    return sum([1 for x in board.values() if x[0] == 'X']), board

# Part 1:
def part1(board, start_pos) -> int:
    return get_guard_route(board, start_pos)[0]

# Part 2:
def part2(board, start_pos) -> int:
    _, route = get_guard_route(board, start_pos)
    possible_blockages = {k for k, v in route.items() if v == 'X'}
    actual_blockages = set()
    if start_pos in possible_blockages:
        possible_blockages.remove(start_pos)
    for k in possible_blockages:
        if get_guard_route(board, start_pos, k)[0] is None:
            actual_blockages.add(k)
    return len(actual_blockages)

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