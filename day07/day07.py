# -*- coding: utf-8 -*-
import os
from functools import reduce
from operator import mul
from time import perf_counter
import itertools
from typing import Literal


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def caculate_total(nums: list[int], ops: tuple[Literal['+', '*', '|']], expected_result: int) -> int:
    total = nums[0]
    for i, op in enumerate(ops):
        match op:
            case '+':
                total += nums[i+1]
            case '*':
                total *= nums[i+1]
            case '|':
                total = int(str(total) + str(nums[i+1]))
        if total > expected_result:
            return 0
    return total


# Part 1:
def part1(content = None) -> str|int:
    test_total = 0
    for res, lst in content:
        if sum(lst) == res or reduce(mul, lst) == res:
            test_total += res
            continue
        operator_options: list[tuple[Literal['*', '+']]] = list(itertools.product(['+', '*'], repeat=len(lst)-1))
        for ops in operator_options:
            ct = caculate_total(lst, ops, res)
            if ct == res:
                test_total += ct
                break
    return test_total

# Part 2:
def part2(content = None) -> str|int:
    test_total = 0
    for res, lst in content:
        if sum(lst) == res or reduce(mul, lst) == res:
            test_total += res
            continue
        operator_options: list[tuple[Literal['*', '+', '|']]] = list(itertools.product(['+', '*', '|'], repeat=len(lst)-1))
        for ops in operator_options:
            ct = caculate_total(lst, ops, res)
            if ct == res:
                test_total += ct
                break
    return test_total

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        content = [(int(r.split(': ')[0]), list(map(int, r.split(': ')[1].split(' ')))) for r in content]
    return content

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
    solve()