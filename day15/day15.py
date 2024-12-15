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

def call_move(pos, dx, dy, map_):
    changes = move(pos, dx, dy, map_)
    if not changes:
        return False
    for key, value in changes.items():
        if value == '.':
            del(map_[key])
        else:
            map_[key] = value
    return True

def move(pos, dx, dy, map_):
    if pos not in map_:
        return {}
    npos = (pos[0] + dx, pos[1] + dy)
    m = {npos: map_[pos], pos: '.'}
    if npos not in map_:
        return m
    else:
        if map_[npos] == '#':
            return {}
        if map_[npos] in 'O':
            c = move(npos, dx, dy, map_)
            if c:
                return c | m
        if map_[npos] in '[]':
            if dy == 0:
                c = move(npos, dx, dy, map_)
                if c:
                    return c | m
                return {}
            # nx, ny is bigbox and move is up or down
            npos2 = (npos[0]+(1 if map_[npos] == '[' else -1), npos[1])
            c1 = move(npos, dx, dy, map_)
            c2 = move(npos2, dx, dy, map_)
            if not c1 or not c2:
                return {}
            for k, v in c2.items():
                if k not in c1:
                    c1[k] = v
                if c1[k] == '.':
                    c1[k] = v
            return c1 | m
    return {}

def part(map_, moves, char) -> int:
    x, y = list(map_.keys())[list(map_.values()).index('@')]
    for c in moves:
        dx = 0
        dy = 0
        match c:
            case '^':
                dy = -1
            case 'v':
                dy = 1
            case '>':
                dx = 1
            case '<':
                dx = -1
        if call_move((x, y), dx, dy, map_):
            x += dx
            y += dy
    return sum([x+100*y for x, y in map_.keys() if map_[(x, y)] == char])

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        map_, moves = [s.strip() for s in f.read().rstrip().split('\n\n')]
        moves = moves.replace('\n', '').replace('\r', '')
        map2 = map_.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
        map_ = {(x, y): c for y, l in enumerate(map_.split('\n')) for x, c in enumerate(l) if c != '.'}
        map2 = {(x, y): c for y, l in enumerate(map2.split('\n')) for x, c in enumerate(l) if c != '.'}
    return map_, map2, moves

@profiler
def solve():
    map_, map2, moves = get_input()
    print(f'Part 1: {part(map_, moves, "O")}')
    print(f'Part 2: {part(map2, moves, "[")}')

if __name__ == "__main__":
    solve()
