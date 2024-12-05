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
    # main diags
    diags = ['', '']
    for i in range(l_len):
        diags[0] += content[i][i]
        diags[1] += content[i][l_len-i-1]
    lines.extend(diags)
    for i in range(1, l_len-3):
        diags = [
            ''.join([content[i+j][j] for j in range(l_len-i)]),
            ''.join([content[i+j][l_len-j-1] for j in range(l_len-i)]),
            ''.join([content[j][i+j] for j in range(l_len-i)]),
            ''.join([content[j][l_len-i-j-1] for j in range(l_len-i)])
        ]
        lines.extend([d for d in diags if len(d) >= 4])
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