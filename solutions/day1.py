from itertools import combinations
from math import prod


def solve(numbers, m, target=2020):
    combos = combinations(numbers, m)
    for combo in combos:
        if sum(combo) == 2020:
            return prod(combo)


with open("inputs/day1.txt") as raw_input:
    raw_input = [int(line) for line in raw_input]

part1 = solve(raw_input, 2)
print(part1)

part2 = solve(raw_input, 3)
print(part2)
