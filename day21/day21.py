# -*- coding: utf-8 -*-
import os
import heapq
from functools import cache
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def get_pad(p, p1=True):
    pad = ['789', '456', '123', ' 0A'] if p1 else [' ↑A', '←↓→']
    r, c = p
    if not (0 <= r < len(pad) and 0 <= c < len(pad[r])):
        return None
    if pad[r][c] == ' ':
        return None
    return pad[r][c]


dirs = {'↑': (-1, 0), '←': (0, -1), '↓': (1, 0), '→': (0, 1)}
def apply_pad(p, move, p1=True):
    if move == 'A':
        return p, get_pad(p, p1)
    a, b = dirs[move]
    return (p[0] + a, p[1] + b), None


@cache
def cost(ch, prev_move, pads):
    if pads == 0:
        return 1
    else:
        start_pos = {'↑': (0, 1), '←': (1, 0), '↓': (1, 1), '→': (1, 2), 'A': (0, 2)}[prev_move]
        queue = []
        heapq.heappush(queue, [0, start_pos, 'A', '', ''])
        seen = {}
        while queue:
            d, p, prev, out, path = heapq.heappop(queue)
            if get_pad(p, False) is None:
                continue
            if out == ch:
                return d
            elif len(out) > 0:
                continue
            seen_key = (p, prev)
            if seen_key in seen:
                continue
            seen[seen_key] = d
            for move in ['↑', '←', '↓', '→', 'A']:
                new_p, output = apply_pad(p, move, False)
                cost_move = cost(move, prev, pads - 1)
                new_d = d + cost_move
                new_path = path
                new_out = out
                if output is not None:
                    new_out = new_out + output
                heapq.heappush(queue, [new_d, new_p, move, new_out, new_path])


def get_moves_amount(code, pads):
    start = [0, (3, 2), 'A', '', '']
    queue = []
    heapq.heappush(queue, start)
    seen = {}
    while queue:
        d, p1, p2, out, path = heapq.heappop(queue)
        if out == code:
            return d
        if not code.startswith(out) or get_pad(p1) is None:
            continue
        key = (p1, p2, out)
        if key in seen:
            continue
        seen[key] = d
        for move in ['↑', '←', '↓', '→', 'A']:
            new_out = out
            new_p1, output = apply_pad(p1, move)
            if output is not None:
                new_out = out + output
            cost_move = cost(move, p2, pads)
            new_path = path
            heapq.heappush(queue, [d + cost_move, new_p1, move, new_out, new_path])


def part(content=None) -> tuple[int, int]:
    pt1 = pt2 = 0
    for line in content:
        line_int = int(line[:-1])
        pt1 += line_int * get_moves_amount(line, 2)
        pt2 += line_int * get_moves_amount(line, 25)
    return pt1, pt2


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    pt1, pt2 = part(get_input())
    print(f'Part 1: {pt1}')
    print(f'Part 2: {pt2}')


if __name__ == "__main__":
    solve()
