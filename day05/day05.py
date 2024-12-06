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

# Part 1:
def part1(rules = None, lists = None) -> int:
    total = 0
    for i, l in enumerate(lists):
        invalid = False
        for index, page in enumerate(l):
            if page not in rules:
                continue
            invalid = len(set(l[:index]) & set(rules[page])) != 0
            if invalid:
                break
        lists[i] = (l, invalid)
        if not invalid:
            total += l[int((len(l)-1)/2)]
    return total

# Part 2:
def part2(rules = None, lists = None) -> int:
    total = 0
    for l, invalid in lists:
        if invalid:
            sorted_list = [l.pop(0)]
            for page in l:
                for i, page2 in enumerate(sorted_list):
                    if page2 in rules[page]:
                        sorted_list.insert(i, page)
                        break
                else:
                    sorted_list.append(page)
            total += sorted_list[int((len(sorted_list)-1)/2)]
    return total

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        rules, lists = (s for s in f.read().rstrip().split('\n\n'))
        rules = [s.strip() for s in rules.split('\n')]
        rules = [(int(i), int(j)) for i, j in map(lambda r: r.split('|'), rules)]
        rule_map = {k: set() for k, _ in rules}
        for one, two in rules:
            rule_map[one].add(two)
        lists = [s.strip() for s in lists.split('\n')]
        lists = [[int(s) for s in l.split(',')] for l in lists]
    return rule_map, lists

@profiler
def solve():
    rules, lists = get_input()
    print(f'Part 1: {part1(rules, lists)}')
    print(f'Part 2: {part2(rules, lists)}')

if __name__ == "__main__":
    solve()