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

def reaches_total(nums: list[int], pt2: bool, expected_result) -> int:
    if nums[0] > expected_result:
        return False
    if len(nums) == 1:
        return nums[0] == expected_result
    if reaches_total([nums[0]+nums[1]]+nums[2:], pt2, expected_result):
        return True
    if reaches_total([nums[0]*nums[1]]+nums[2:], pt2, expected_result):
        return True
    if pt2 and reaches_total([int(str(nums[0])+str(nums[1]))]+nums[2:], pt2, expected_result):
        return True
    return False

# Part 1:
def part1(content) -> int:
    total = 0
    for res, lst in content:
        if reaches_total(lst, False, res):
            total += res
    return total

# Part 2:
def part2(content) -> int:
    total = 0
    for res, lst in content:
        if reaches_total(lst, True, res):
            total += res
    return total

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
