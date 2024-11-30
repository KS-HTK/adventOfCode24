# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(content = None) -> str|int:
  return 0

# Part 2:
def part2(content = None) -> str|int:
  return 0

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