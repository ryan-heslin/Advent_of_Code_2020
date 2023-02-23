from collections import Counter
from math import prod


def RLE(nums):
    prev = nums[0]
    streak = 0
    vals = []
    runs = []
    end = len(nums) - 1

    for i, num in enumerate(nums):
        if num == prev and i != end:
            streak += 1
        else:
            runs.append(streak)
            vals.append(num)
            prev = num
            streak = 1

    return [vals, runs]


def RLE(seq):
    """Convert list of integers to lists of lengths and values, suitable for RLE creation"""
    lengths = []
    values = []
    last = None
    for el in seq:
        if el != last:
            values.append(el)
            lengths.append(1)
            last = el
        else:
            lengths[-1] += 1

    return [values, lengths]


with open("inputs/day10.txt") as f:
    nums = [int(x) for x in f.read().splitlines()]

nums.insert(0, 0)
nums.sort()
nums.append(max(nums) + 3)

# Last jump is 3
diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]

count = Counter(diffs)

part1 = count[1] * count[3]
print(part1)

# I wrote this in December 2020 and have not a clue why it works.
mapping = {1: 1, 2: 2, 3: 4, 4: 7}
streaks = RLE(diffs)
runs = [streaks[1][i] for i in range(len(streaks[0])) if streaks[0][i] != 3]
permutes = [mapping[num] for num in runs]
part2 = prod(permutes)
print(part2)
