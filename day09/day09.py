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

def calc_result(fs_list):
    res = 0
    for i, f_id in enumerate(fs_list):
        if f_id == '.':
            return res
        res += f_id * i

# Part 1:
def part1(content = None) -> int:
    file = True
    f_id = 0
    fs = []
    for num in content[0]:
        num = int(num)
        fs.extend([f_id if file else '.'] * num)
        if file:
            f_id += 1
        file = not file
    last_num_ind = len(fs) - 1
    for i in range(len(fs)):
        if fs[i] == '.':
            while fs[last_num_ind] == '.':
                last_num_ind -= 1
            if last_num_ind < i:
                return calc_result(fs)
            fs[i] = fs[last_num_ind]
            fs[last_num_ind] = '.'
    return calc_result(fs)

def calc_result2(fs_list):
    expanded_fs_list = []
    for f_id, num in fs_list:
        expanded_fs_list.extend([f_id] * num)
    checksum = []
    for i, f_id in enumerate(expanded_fs_list):
        if f_id == -1:
            continue
        checksum.append((f_id, i))
    return sum([a*b for a, b in checksum])

# Part 2: > 264203879949
def part2(content = None) -> int:
    file = True
    f_id = 0
    fs: list[tuple[int, int]] = []
    for num in content[0]:
        num = int(num)
        fs.append((f_id, num) if file else (-1, num))
        if file:
            f_id += 1
        file = not file

# Part 2:
    while True:
        no_swap = True
        for i in [i for i, (j, _) in enumerate(fs) if j == -1]:
            last_num_ind = len(fs) - 1
            while 0 <= i <= last_num_ind and (fs[last_num_ind][0] == -1 or fs[last_num_ind][1] > fs[i][1]):
                last_num_ind -= 1
            if last_num_ind < i:
                continue
            no_swap = False
            free_space = fs[i][1]  # store length of free space
            file_to_swap = fs[last_num_ind]
            fs[i] = file_to_swap
            fs[last_num_ind] = (-1, file_to_swap[1])
            if free_space > file_to_swap[1]:
                fs.insert(i+1, (-1, free_space-file_to_swap[1]))
                break
        if no_swap:
            break
    return calc_result2(fs)

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