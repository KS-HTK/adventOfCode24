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

def get_same_chars(content, char):
    chars = set()
    for y, line in enumerate(content):
        for x, char2 in enumerate(line):
            if char == char2:
                chars.add((x, y))
    return chars

def get_anti_node(pos1, pos2):
    dist = (pos1[0]-pos2[0], pos1[1]-pos2[1])
    return pos1[0]-2*dist[0], pos1[1]-2*dist[1]

# Part 1:
def part1(content = None) -> int:
    x_lim, y_lim = len(content[0]), len(content)
    char_positions = {}
    anti_set = set()
    for y, line in enumerate(content):
        for x, char in enumerate(line):
            if char == '.':
                continue
            if char not in char_positions:
                char_positions[char] = get_same_chars(content, char)
            for position in char_positions[char]:
                if position != (x, y):
                    anti_node = get_anti_node((x, y), position)
                    if 0 <= anti_node[0] < x_lim and 0 <= anti_node[1] < y_lim:
                        anti_set.add(anti_node)
    return len(anti_set)

def get_anti_nodes(pos1, pos2, x_lim, y_lim):
    anti_nodes = {pos1, pos2}
    dx, dy = (pos1[0]-pos2[0], pos1[1]-pos2[1])
    x, y = pos1
    while True:
        x = x+dx
        y = y+dy
        if 0 <= x < x_lim and 0 <= y < y_lim:
            anti_nodes.add((x, y))
        else:
            break
    return anti_nodes

# Part 2:
def part2(content = None) -> int:
    x_lim, y_lim = len(content[0]), len(content)
    char_positions = {}
    anti_set = set()
    for y, line in enumerate(content):
        for x, char in enumerate(line):
            if char == '.':
                continue
            if char not in char_positions:
                char_positions[char] = get_same_chars(content, char)
            for position in char_positions[char]:
                if position != (x, y):
                    anti_set.update(get_anti_nodes((x, y), position, x_lim, y_lim))
    return len(anti_set)


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