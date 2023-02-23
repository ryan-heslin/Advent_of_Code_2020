# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 07:36:10 2020

@author: heslinr1
"""
# <codecell> Day 1
import os

print(os.getcwd())
import itertools as it

with open("./inputs/input1.txt") as inpt:
    inpt = [int(line) for line in inpt]


combs = list(it.combinations(inpt, 2))

for combo in combs:
    if sum(combo) == 2020:
        ans1 = combo[0] * combo[1]

print(ans1)

from functools import reduce


def ans(inpt, m, target=2020):

    combs = list(it.combinations(inpt, m))

    for combo in combs:
        if sum(combo) == target:
            ans = reduce(lambda x, y: x * y, combo)
            return ans


ans2 = ans(inpt, 3)
print(ans2)
# <codecell>


# <codecell Day 2>
import re

with open("./inputs/input2.txt") as inpt:
    raw = inpt.readlines()


def validate(rnge, char, password):

    if rnge[0] <= password.count(char) <= rnge[1]:
        return 1
    else:
        return 0


def validate2(rnge, char, password):
    start, stop = rnge
    if (password[start - 1] == char) ^ (password[stop - 1] == char):
        return 1
    else:
        return 0


def get_range(line):
    rnge = re.findall("\d+", line)
    return list(map(int, rnge))


rnge = [None] * 1000
char = [None] * 1000
password = [None] * 1000

for i, line in enumerate(raw):
    rnge[i], char[i], password[i] = re.split("\s", line)[:-1]

rnge = list(map(get_range, rnge))
char = map(lambda x: re.findall("[a-z]", x), char)
password = map(lambda x: re.findall("[a-z]+", x), password)

char = [j for i in char for j in i]
password = [j for i in password for j in i]

count = [validate(rnge[i], char[i], password[i]) for i in range(len(rnge))]
ans1 = sum(count)
print(ans1)


count2 = [validate2(rnge[i], char[i], password[i]) for i in range(len(rnge))]
ans2 = sum(count2)
print(ans2)

# <codecell>

# <codecell> Day 3
import functools as ft

with open("./inputs/input3.txt") as inpt:
    inpt = [line.rstrip("\n") for line in inpt]

wrap = len(inpt[1])
col = 3
count = 0

for line in inpt[1 : len(inpt)]:
    if line[col] == "#":
        count += 1
    col = (col + 3) % wrap

print(count)
# part 2

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def count_trees(slope, inpt, wrap):
    col, skip = slope
    right = col
    count = 0
    for i in range(skip, len(inpt), skip):
        if inpt[i][col] == "#":
            count += 1
        col = (col + right) % wrap
    return count


ans2 = [count_trees(slope, inpt, wrap) for slope in slopes]
print(ft.reduce(lambda x, y: x * y, ans2))
# <codecell>


# <codecell> Day 4

import re
import numpy as np
from functools import reduce

with open("./inputs/input4.txt") as inpt:
    raw = inpt.readlines()


def filt(fields):
    needed = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all(field in fields for field in needed)


def pass_valid2(di):
    valid = {
        "byr": "^(?:19[2-9]\d|200[0-2])$",
        "iyr": "^(?:201\d|2020)$",
        "eyr": "^(?:202\d|2030)$",
        "hgt": "^(?:(?:1[5-8]\d|19[0-3])cm|(?:59|6\d|7[0-6])in)$",
        "hcl": "^#[\da-f]{6}$",
        "ecl": "^(?:b(?:lu|rn)|gr(?:y|n)|hzl|amb|oth)$",
        "pid": "^\d{9}$",
    }
    if len(di.items()) < len(valid.items()):
        return False
    for k, v in di.items():
        if not re.search(valid.get(k), v):
            return False
    return True


def pass_valid(lines):
    fields = [re.findall("[a-z]{3}(?=:)", line) for line in lines]
    return list(filter(filt, fields))


def pass_dict(lines):

    out = []
    for line in lines:
        keys = re.findall("[a-z]{3}(?=:)", line)
        values = re.findall("(?<=:)[^\s]+", line)
        out.append(dict(zip(keys, values)))
    return out


lines = reduce(lambda x, y: x + y, [re.sub("^\n$", "-", line) for line in raw])
lines = re.split("-", lines)


lines = [re.sub("\n", " ", i) for i in lines]
lines = [re.sub("cid:\d+", "", line) for line in lines]

# lines= pass_valid(lines)

pairs = pass_dict(lines)
# pairs = [filter(lambda x: x != "cid")]

ans2 = [pass_valid2(di) for di in pairs]
print(sum(ans2))
# <codecell>

# <codecell> Day 5
import re

import re

with open("./inputs/input5.txt") as inpt:
    raw = inpt.readlines()
    raw = [line.rstrip("\n") for line in raw]


def convert_binary(stri):
    stri = [re.sub("B|R", "1", line) for line in stri]
    stri = [re.sub("[A-Z]", "0", line) for line in stri]
    stri = [[line[0:7], line[7:]] for line in stri]

    return [[int(line[0], 2), int(line[1], 2)] for line in stri]


def seat_ID(nums):
    return [line[0] * 8 + line[1] for line in nums]


nums = convert_binary(raw)
ids = seat_ID(nums)
ans1 = max(ids)
print(ans1)


def get_seat(ids):
    for i in range(len(ids)):
        if ids[i + 1] - ids[i] > 1:
            return ids[i] + 1


ids.sort()

ans2 = get_seat(ids)
print(ans2)

# <codecell>


# <codecell Day 6>

import collections as coll


def count_alls(stri):
    num_people = stri.count("\n")
    stri = stri.replace("\n", "")
    alls = len(list(filter(lambda x: x == num_people, coll.Counter(stri).values())))
    return alls


with open("./inputs/input6.txt") as inpt:
    inpt = [re.sub("(?<=[a-z])\n", "", i) for i in inpt]

cleaned = str(ft.reduce(lambda x, y: x + y, inpt))
cleaned = cleaned.split("\n")

counts = [len(set(stri)) for stri in cleaned]
ans1 = sum(counts)
print(ans1)

by_grp = [re.sub("^\n$", ",", i) for i in inpt]
by_grp = str(ft.reduce(lambda x, y: x + y, by_grp))
by_grp = by_grp.split(",")

counts2 = [count_alls(stri) for stri in by_grp]
coll.Counter("aaabbc")
ans2 = sum(counts2)
print(ans2)

# <codecell>

# <codecell Day 8>

import re


def run_code(instr, nums, swap=None, replace=None):

    if swap:
        instr[swap] = replace

    prevs = [None]
    i = 0
    acc = 0
    while i not in prevs and i < len(instr):
        prevs.append(i)
        if instr[i] == "acc":
            acc = acc + nums[i]
            i = i + 1
        elif instr[i] == "jmp":
            i = i + nums[i]
        else:
            i = i + 1

        if i == len(instr):
            return acc
    return False


def to_num(num):
    op = num[0]
    num = int(num[1:])

    if op == "+":
        return num
    else:
        return -num


def ans2(instr):
    res = False
    for i in range(len(instr)):
        if instr[i] == "jmp":
            res = run_code(instr=instr.copy(), nums=nums, swap=i, replace="nop")

        if res != False:
            return res

    for i in range(len(instr)):
        if instr[i] == "nop":
            res = run_code(instr=instr.copy(), nums=nums, swap=i, replace="jmp")
        if res != False:
            return res


with open("./inputs/input8.txt") as inpt:
    inpt = [line.rstrip("\n") for line in inpt]


inpt = [re.split("\s", line) for line in inpt]
inpt = list(zip(*inpt))

instr, nums = inpt[0], inpt[1]
nums = list(map(to_num, nums))

instr = list(instr)
ans1 = run_code(instr, nums)
ans2 = ans2(instr)

# <codecell>
# <codecell Day 9>

import itertools as it
import numpy as np


def breakXMAS(nums, seq_max=24):
    for i in range(seq_max, len(nums)):
        next_num = nums[i + 1]
        start = i - seq_max
        # combs = list(it.combinations(nums[start:seq_max+1], r =2))
        sums = [sum(combo) for combo in it.combinations(nums[start : i + 1], r=2)]
        if next_num not in sums:
            return next_num


def breakXMAS2(nums, step, target):
    slices = [None] * (len(nums) - step + 1)
    stop = len(nums) - step + 1

    for i in range(0, stop):
        slices[i] = nums[i : min(i + step, len(nums))]

    for slic in slices:
        if sum(slic) == target:
            return max(slic) + min(slic)
    return "Failed"


with open("./inputs/input9.txt") as inpt:
    inpt = [int(line) for line in inpt]

ans1 = breakXMAS(inpt)
distincts = len(inpt) - len(set(inpt))

ranges = np.arange(2, len(inpt))

for step in ranges:
    ans2 = breakXMAS2(inpt, step, ans1)
    if ans2 != "Failed":
        break
print(ans2)

# <codecell>

# <codecell Day 10>

import numpy as np
import itertools
import functools as ft
import rle

nums = [0]

with open("./inputs/input10.txt") as inpt:
    inpt = [i.rstrip("\n") for i in inpt]


for i, line in enumerate(inpt):
    nums.append(int(line))
nums.sort()
nums.append(max(nums) + 3)

# Last jump is 3
diffs = np.diff(nums, axis=0)


ans1 = np.sum(diffs == 3) * np.sum(diffs == 1)


def all_chains(run, choices=[1, 2, 3]):
    steps = len(run)
    rnge = max(run) - min(run)
    combos = [list(it.combinations(choices, r=i)) for i in range(1, steps)]
    combos = [x for sublist in combos for x in sublist]
    print(combos)

    possibles = list(filter(lambda sub: sum(sub) % rnge == 0, combos))
    return possibles


diffs = np.diff(nums, axis=0)
MAX_DIFF = 3


cheat_dict = {1: 1, 2: 2, 3: 4, 4: 7}
streaks = rle.encode(diffs)
# value-run encoding
runs = [streaks[1][i] for i in range(len(streaks[0])) if streaks[0][i] != 3]
permutes = [cheat_dict.get(num) for num in runs]


ans2 = ft.reduce(lambda x, y: x * y, permutes)
print(ans2)
# <codecell>

# <codecell Day 14>

import re
import numpy as np
import functools as ft
import itertools as it
import collections as col


def extract_dict(sublist):

    mask = re.findall("[01x]+", sublist[0]).pop(0)
    data = [re.findall("\d+", line) for line in sublist[1:]]
    di = {line[0]: line[1] for line in data}
    di["mask"] = mask
    if len(data) - len(set([line[0] for line in data])) != 0:
        print("dupes")
    return di


def assign_mem(program):

    mask = list(program.get("mask"))
    del program["mask"]
    # swaps = [i for i, char in enumerate(mask) if char != "x"]

    # convert each val to binary, sub in from bitmask, update global dict
    for k, v in program.items():
        val = v
        # replace = list(bin(int(v))[2:].rjust(len(mask), "0"))

        # for i in swaps:
        # replace[i] = mask[i]
        addrs = list(map(str, mutate_mem(mask=mask.copy(), mem=k)))
        # change to previously modifed value if addreess already changed
        if k in mem_di.keys():
            val = mem_di[k]

        # replace = int(str(ft.reduce(lambda x, y: x + y, replace)), base = 2)
        # update each address in master dict
        for addr in addrs:
            # if addr in mem_di.keys():
            # print("overwrite " + str(mem_di[k2]) + " at " + k2 + " with " + str(v2))
            mem_di[addr] = int(val)


def mutate_mem(mask, mem):

    # find float bits and convert to base 10 values
    binar = list(bin(int(mem))[2:].rjust(len(mask), "0"))
    swaps = [len(mask) - i - 1 for i, char in enumerate(mask) if char == "x"]

    combos = [
        list(list(combo) for combo in it.combinations(swaps, r=i))
        for i in range(1, len(swaps) + 1)
    ]
    summands = [sum(map(lambda x: 2**x, i)) for sublist in combos for i in sublist]

    # handle 0 as base case
    # sub in new values to create base case
    for i, char in enumerate(mask):

        if char == "1":
            binar[i] = "1"

        elif char == "x":
            binar[i] = "0"

    base = int(str(ft.reduce(lambda x, y: x + y, binar)), base=2)

    # return unmodified if no new addresses
    if len(summands) == 0:
        return [base]
    out = [base + add for add in summands]
    out.append(base)
    out.sort()
    return out


with open("./inputs/input14.txt") as inpt:
    inpt = [i.rstrip("\n") for i in inpt]


# global dict of distinct addresses
addr = str(ft.reduce(lambda x, y: x + y, inpt))
addr = set(re.findall("\[(\d+)\]", addr))
mem_di = {}

# dicts of changes for each program
splits = [i for i, line in enumerate(inpt) if line[0:2] == "ma"]
start_mems = {
    re.findall("\[(\d+)\]", line).pop(): int(re.findall("\s(\d+)", line).pop())
    for line in inpt
    if line[0:2] != "ma"
}
splits.append(len(inpt))
masks = [inpt[splits[i] : splits[i + 1]] for i in range(0, len(splits) - 1)]
programs = list(map(extract_dict, masks))

for i in programs:
    assign_mem(i)
ans2 = sum(mem_di.values())
print(ans2)

# <codecell>
