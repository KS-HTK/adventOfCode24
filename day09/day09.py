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

def calc_result(fs: list[tuple[int, int]]):
    res = 0
    index = 0
    for f, l in fs:
        if f != -1:
            start = index
            index += l
            res += f * (index * (index - 1) - start * (start - 1)) // 2
        else:
            index += l
    return res

# Part 1:
def part1(fs: list[tuple[int, int]]):
    fs = fs.copy()
    last_num_ind = len(fs) - 1
    while True:
        no_swap = True
        for i, (f_id, l) in enumerate(fs):
            if f_id != -1:
                continue
            while fs[last_num_ind][0] == -1:
                last_num_ind -= 1
            if last_num_ind <= i:
                break
            no_swap = False
            file_id, file_len = fs[last_num_ind]
            if file_len > l:
                fs[last_num_ind] = (file_id, file_len - l)
                fs[i] = (file_id, l)
            elif file_len < l:
                del fs[last_num_ind]
                fs[i] = (file_id, file_len)
                fs.insert(i + 1, (-1, l - file_len))
                break
            else:
                del fs[last_num_ind]
                fs[i] = (file_id, file_len)
        if no_swap:
            break
    return calc_result(fs)

# Part 2:
def part2(fs: list[tuple[int, int]]):
    free_spaces = []
    for ind, (f_id, length) in enumerate(fs):
        if f_id == -1:
            free_spaces.append((ind, length))

    for i in range(len(fs) - 1, -1, -1):
        f_id, length = fs[i]
        if f_id == -1:
            continue
        for j, (index, free_length) in enumerate(free_spaces):
            if free_length >= length and index < i:
                fs[index] = (f_id, length)
                fs[i] = (-1, length)
                remaining_space = free_length - length
                if remaining_space > 0:
                    free_spaces[j] = (index, remaining_space)
                    fs.insert(index+1, (-1, remaining_space))
                    free_spaces = [(k+1 if k >= index else k, l) for k, l in free_spaces]
                else:
                    free_spaces.pop(j)
                break
    return calc_result(fs)

def get_input():
    with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    file = True
    f_id = 0
    fs: list[tuple[int, int]] = []
    for num in content[0]:
        num = int(num)
        fs.append((f_id, num) if file else (-1, num))
        f_id += file
        file = not file
    return fs

@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
    solve()
