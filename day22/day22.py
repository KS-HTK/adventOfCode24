# -*- coding: utf-8 -*-

import os
from collections import Counter
from time import perf_counter
from typing import Generator


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def next_secret(seed: int) -> Generator[int, None, None]:
    num = seed
    while True:
        num = (num ^ num*64) % 16777216
        num = (num ^ num//32) % 16777216
        num = (num ^ num*2048) % 16777216
        yield num


def get_nth_num(seq, n) -> int:
    val = next(seq)
    for _ in range(n-1):
        val = next(seq)
    return val


# Part 1:
def part1(content: list[int]) -> int:
    return sum(get_nth_num(next_secret(num), 2000) for num in content)


def get_prices(num: int) -> list[int]:
    gen = next_secret(num)
    return [next(gen)%10 for _ in range(2001)]


def get_sell_map(prices: list[int]) -> Counter[int]:
    c = Counter()
    changes = [p-np for p, np in zip(prices, prices[1:])]
    for i in range(4, len(changes)):
        key = tuple(changes[i-4:i])
        if key in c:
            continue
        c[key] = prices[i]
    return c


# Part 2:
def part2(content: list[int]) -> int:
    sell_prices = list(map(get_prices, content))
    c = Counter()
    for prices in sell_prices:
        c += get_sell_map(prices)
    return max(c.values())


def get_input() -> list[int]:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [int(s.strip()) for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')


if __name__ == "__main__":
    solve()
