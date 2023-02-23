from collections import defaultdict
from functools import cache
from itertools import permutations


def make_neighbors(dimension, adjacencies):
    rnge = range(dimension)

    @cache
    def result(point):
        return {tuple([point[i] + adj[i] for i in rnge]) for adj in adjacencies}

    return result


def parse(grid):
    result = set()
    for j, line in enumerate(grid):
        for i, char in enumerate(line):
            if char == "#":
                result.add((i, j, 0))
    return result


def simulate(start, iterations, neighbors):
    on = start.copy()
    for _ in range(iterations):
        off_on_neighbors = defaultdict(lambda: 0)
        on_on_neighbors = defaultdict(lambda: 0)

        # This shouldn't double-count anywhere
        for cube in on:
            this_neighbors = neighbors(cube)
            assert len(this_neighbors) in (80, 26)
            # current_neighbors[point] = this_neighbors
            for neighbor in this_neighbors:
                if neighbor in on:
                    # If on, note that on cube has this point as neighbor
                    on_on_neighbors[cube] += 1
                else:
                    # If cube is off, note that it is neighbor of on cube
                    off_on_neighbors[neighbor] += 1

        # on.difference_update(
        #     k for k, v in on_on_neighbors.items() if not (v == 2 or v == 3)
        # )
        on = set(filter(lambda x: on_on_neighbors[x] in (2, 3), on))
        on.update(k for k, v in off_on_neighbors.items() if v == 3)
        # current_neighbors = { cube: neighbors(cube) for cube in on}
        # new_on = Counter(neighbors(x) for x in on)
    return len(on)


with open("inputs/day17.txt") as f:
    raw_input = f.read().splitlines()

adjacencies = set(permutations((0, 0, 1, 1, 1, -1, -1, -1), r=3))

neighbors = make_neighbors(3, adjacencies)
on = parse(raw_input)
part1 = simulate(on, 6, neighbors)
print(part1)

neighbors_4d = make_neighbors(
    4, adjacencies=list(permutations([0] * 3 + [1] * 4 + [-1] * 4, r=4))
)
on = {coord + (0,) for coord in on}
part2 = simulate(on, 6, neighbors_4d)
print(part2)
