# -*- coding: utf-8 -*-

import os
from itertools import combinations
from time import perf_counter
from typing import Optional


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def get_state(key, states, gates):
    if key in states:
        return states[key]
    i1, operator, i2 = gates[key]
    v1, v2 = get_state(i1, states, gates), get_state(i2, states, gates)
    match operator:
        case 'AND':
            states[key] = v1 and v2
        case 'OR':
            states[key] = v1 or v2
        case 'XOR':
            states[key] = v2 != v1
        case _:
            raise ValueError(key)
    return states[key]


# Part 1:
def part1(states, gates) -> int:
    num = ''
    key = 0
    while True:
        s_key = f'z{key:02d}'
        if s_key in states:
            num = str(int(states[s_key]))+num
            key += 1
        elif s_key in gates:
            num = str(int(get_state(s_key, states, gates)))+num
            key += 1
        else:
            break
    num = int(num, 2)
    return num


def furthest_made(gates):
    ops = {}
    for res, (x1, op, x2) in gates.items():
        ops[(frozenset([x1, x2]), op)] = res

    def get_res(x1_, x2_, op_) -> Optional[int]:
        return ops.get((frozenset([x1_, x2_]), op_), None)

    carries = {}
    correct = set()
    prev_intermediates = set()
    for i in range(45):
        prev_digit = get_res(f"x{i:02d}", f"y{i:02d}", "XOR")
        prev_carry1 = get_res(f"x{i:02d}", f"y{i:02d}", "AND")
        if i == 0:
            carries[i] = prev_carry1
            continue
        digit = get_res(carries[i - 1], prev_digit, "XOR")
        if digit != f"z{i:02d}":
            return i - 1, correct
        correct.add(carries[i - 1])
        correct.add(prev_digit)
        for wire in prev_intermediates:
            correct.add(wire)
        prev_carry2 = get_res(carries[i - 1], prev_digit, "AND")
        carry_out = get_res(prev_carry1, prev_carry2, "OR")
        carries[i] = carry_out
        prev_intermediates = {prev_carry1, prev_carry2}
    return 45, correct



# Part 2:
def part2(gates) -> str:
    swaps = set()
    base, base_used = furthest_made(gates)

    for _ in range(4):
        for res_i, res_j in combinations(gates.keys(), 2):
            if "z00" in (res_i, res_j) or res_i in base_used or res_j in base_used:
                continue
            gates[res_i], gates[res_j] = gates[res_j], gates[res_i]
            attempt, attempt_used = furthest_made(gates)
            if attempt > base:
                swaps.add((res_i, res_j))
                base, base_used = attempt, attempt_used
                break
            gates[res_i], gates[res_j] = gates[res_j], gates[res_i]
    return ','.join(sorted(sum(swaps, start=tuple())))


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip().split('\n') for s in f.read().rstrip().split('\n\n')]
        states = {n: g == '1' for n, g in map(lambda l: l.split(': '), content[0])}
        gates = {r1: (o1, o2, o3) for o1, o2, o3, _, r1 in map(lambda l: l.split(' '), content[1])}
    return states, gates


@profiler
def solve():
    states, gates = get_input()
    print(f'Part 1: {part1(states, gates)}')
    print(f'Part 2: {part2(gates)}')


if __name__ == "__main__":
    solve()
