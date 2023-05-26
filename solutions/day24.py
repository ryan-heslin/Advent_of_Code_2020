from collections import defaultdict
from collections import deque
from functools import cache


def parse(lines):

    black = set()
    movements = {
        "ne": 1 - 1j,
        "e": 1 + 0j,
        "se": 0 + 1j,
        "sw": -1 + 1j,
        "w": -1 + 0j,
        "nw": 0 - 1j,
    }
    for line in lines:
        position = 0 + 0j
        line = deque(line)
        while line:
            current = line.popleft()
            if current in ("n", "s"):
                current += line.popleft()
            position += movements[current]
        if position in black:
            black.remove(position)
        else:
            black.add(position)
    return black


# compute hexagonal axis
@cache
def get_s(coord):
    return -coord.real - coord.imag


@cache
def neighbors(coord):
    q = coord.real
    r = coord.imag
    return frozenset(
        (
            complex(q, r - 1),
            complex(q + 1, r - 1),
            complex(q + 1, r),
            complex(q, r + 1),
            complex(q - 1, r + 1),
            complex(q - 1, r),
        ),
    )


def simulate(start, iterations=100):
    black = start.copy()

    for _ in range(iterations):
        white_black_neighbors = defaultdict(lambda: 0)
        black_black_neighbors = defaultdict(lambda: 0)
        live_number = (1, 2)

        for hex in black:
            this_neighbors = neighbors(hex)
            for neighbor in this_neighbors:
                if neighbor in black:
                    # If on, note that on cube has this point as neighbor
                    black_black_neighbors[hex] += 1
                else:
                    # If white, note that it is neighbor of on cube
                    white_black_neighbors[neighbor] += 1
        black = {hex for hex in black if black_black_neighbors[hex] in live_number}
        black.update(k for k, v in white_black_neighbors.items() if v == 2)
    return len(black)


with open("inputs/day24.txt") as f:
    raw_input = f.read().splitlines()

black = set(parse(raw_input))
part1 = len(black)
print(part1)

iterations = 100
part2 = simulate(black, iterations)
print(part2)
