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
def part1(content = None) -> str|int:
    sum_ = 0
    for line in content:
        matches = re.finditer(r'mul\((\d\d?\d?),(\d\d?\d?)\)', line)
        for match in matches:
            sum_ += int(match.group(1))*int(match.group(2))
    return sum_

# Part 2:
def part2(content = None) -> str|int:
    enabled = True
    sum_ = 0
    for line in content:
        matches = re.finditer(r"mul\((\d\d?\d?),(\d\d?\d?)\)|do\(\)|don't\(\)", line)
        for match_ in matches:
            match match_.group(0):
                case 'do()':
                    enabled = True
                case "don't()":
                    enabled = False
                case _:
                    if enabled:
                        sum_ += int(match_.group(1))*int(match_.group(2))
    return sum_

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