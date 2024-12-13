# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from sympy import symbols, Eq, solve as sysolve

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def linear_diophantine(a: list[int], b: list[int], c: list[int]) -> tuple[int, int]:
    if len(a) != len(b) != len(c):
        raise ValueError('inputs must have same length')
    n, m = symbols('n m')
    eqs = [Eq(n*a[i]+m*b[i], c[i]) for i in range(len(a))]
    solution = sysolve(eqs, (n, m))
    nt = solution[n]
    mt = solution[m]
    if int(nt) == nt and int(mt) == mt:
        return int(nt), int(mt)
    return 0, 0

def part(content) -> tuple[int, int]:
    parts = []
    for add in [0, 10000000000000]:
        solutions = [linear_diophantine(a, b, [cx+add, cy+add]) for a, b, [cx, cy] in content]
        solutions = [s for s in solutions if s]
        parts.append(sum([3 * a + b for a, b in solutions]))
    return parts[0], parts[1]

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n\n')]
        machines = []
        for lines in content:
            machines.append([])
            for l in lines.split('\n'):
                result = re.search(r'X[+|=](\d*), Y[+|=](\d*)', l)
                machines[-1].append([int(result.group(1)), int(result.group(2))])
    return machines

@profiler
def solve():
    content = get_input()
    pt1, pt2 = part(content)
    print(f'Part 1: {pt1}')
    print(f'Part 2: {pt2}')

if __name__ == "__main__":
    solve()
