# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def step(a, b, c, instruction, operand, p) -> tuple[int, int, int, int, int]:
    def combo(v):
        return v if v < 4 else (a, b, c)[v - 4]

    o = None
    match instruction:
        case 0:
            a >>= combo(operand)
        case 1:
            b ^= operand
        case 2:
            b = combo(operand) % 8
        case 3:
            if a:
                p = operand - 2
        case 4:
            b ^= c
        case 5:
            o = combo(operand) % 8
        case 6:
            b = a >> combo(operand)
        case 7:
            c = a >> combo(operand)
    return a, b, c, o, p + 2


# Part 1:
def part1(prog, a) -> str:
    out = []
    b = c = 0
    opp = 0

    while opp < len(prog):
        op = prog[opp]
        lv = prog[opp + 1]
        a, b, c, o, opp = step(a, b, c, op, lv, opp)
        if o is not None:
            out.append(str(o))
    return ','.join(out)


def one_cycle(a, prog) -> int:
    b, c = 0, 0
    for i in range(0, len(prog), 2):
        a, b, c, o, _ = step(a, b, c, prog[i], prog[i + 1], 0)
        if o is not None:
            return o


def find_rec(a: int, to: int, prog: list[int]):
    if to == 0:
        return a
    o = prog[to - 1]
    a <<= 3
    for i in range(8):
        if o == one_cycle(a + i, prog):
            oa = find_rec(a + i, to - 1, prog)
            if oa:
                return oa
    else:
        return False


# Part 2:
def part2(prog) -> int:
    res = find_rec(0, len(prog), prog)
    outs = part1(prog, res)
    assert outs == ','.join(map(str, prog))
    return res


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        a, _, _, *prog = list(map(int, re.findall(r"\d+", f.read())))
    return prog, a


@profiler
def solve():
    prog, a = get_input()
    print(f'Part 1: {part1(prog, a)}')
    print(f'Part 2: {part2(prog)}')


if __name__ == "__main__":
    solve()
