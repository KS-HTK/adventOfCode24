# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

# Part 1:
def part1(content = None) -> int:
    lines = content.copy()
    # add vertical lines
    for i in range(len(content[0])):
        line = ""
        for j in range(len(content)):
            line += content[j][i]
        lines.append(line)
    # add diagonal lines:
    l_len = len(content[0])
    for i in range(len(content[1:])):
        diag = ''
        r_diag = ''
        for j in range(len(content[i+1:])):
            diag += content[i+1+j][j]
            r_diag += content[i+1+j][l_len-j-1]
        if len(diag) >= 4:
            lines.append(diag)
        if len(r_diag) >= 4:
            lines.append(r_diag)
    # add top diagonal lines
    for i in range(len(content[0])):
        diag = ''
        r_diag = ''
        for j in range(len(content[0][i:])):
            diag += content[j][i+j]
            r_diag += content[j][l_len-i-j-1]
        if len(diag) >= 4:
            lines.append(diag)
        if len(r_diag) >= 4:
            lines.append(r_diag)
    return sum([len(list(re.findall(r'(?=XMAS|SAMX)', line))) for line in lines])

# Part 2:
def part2(content = None) -> int:
    count = 0
    for i in range(1, len(content)-1):
        for j in range(1, len(content[i])-1):
            if content[i][j] == 'A':
                tr = content[i-1][j-1]
                tl = content[i-1][j+1]
                br = content[i+1][j-1]
                bl = content[i+1][j+1]
                if ((tr == 'M' and bl == 'S' or tr == 'S' and bl == 'M')
                    and (tl == 'M' and br == 'S' or tl == 'S' and br == 'M')):
                        count += 1
    return count

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