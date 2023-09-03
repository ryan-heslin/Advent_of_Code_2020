def read_row(chars):
    row = "".join("0" if char == "F" else "1" for char in chars[:7])
    col = "".join("0" if char == "L" else "1" for char in chars[7:])
    return int(row + col, base = 2)

def id(seat):
    return ((seat >> 3) * 8) + (seat % 8)

def find_missing(seats):
    for i in range(min(seats), max(seats) + 1):
        if i not in seats:
            return i

with open("inputs/day5.txt") as f:
    raw_input = f.read().splitlines()

seats = list(map(read_row, raw_input))
ids = list(map(id, seats))
part1 = max(ids)
print(part1)

part2 = find_missing(seats)
print(part2)
