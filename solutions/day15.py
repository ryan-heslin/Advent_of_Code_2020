numbers = (17, 1, 3, 16, 19, 0)
seen = dict(zip(numbers, range(1, 8)))


def elf_game(init, end):
    # 1-indexed here
    start = len(init) + 1
    last = init[max(init.keys())]
    next_num = 0

    for i in range(start, end + 1):
        # If already seen, subtract turns and update, 0 otherwise
        last = next_num
        if last in init.keys():
            next_num = i - init[last]
        else:
            next_num = 0
        init[last] = i

    return last


part1 = elf_game(seen.copy(), 2020)
print(part1)

part2 = elf_game(seen.copy(), 30000000)
print(part2)
