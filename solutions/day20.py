from collections import defaultdict
from functools import cache
from functools import singledispatch
from math import prod
from math import sqrt
from operator import attrgetter

real = attrgetter("real")
imag = attrgetter("imag")


def display(map, xmax, ymax):
    return "\n".join(
        "".join("#" if map[complex(i, j)] else "." for i in range(xmax))
        for j in range(ymax)
    )


def identity(x, *args):
    return x


def parse_tile(tile):
    parts = tile.splitlines()
    id = int(parts[0].split(" ")[1].rstrip(":"))
    return id, tuple(parts[1:])


@singledispatch
def hflip(x, dim=None):
    pass


@singledispatch
def vflip(x, dim=None):
    pass


@singledispatch
def left90(x, *args):
    pass


# Rotation
@left90.register
@cache
def _(lines: tuple, dim=10):
    string = "".join(lines)
    return tuple(string[i::dim] for i in reversed(range(dim)))


@left90.register
def _(coords: set, size=None):
    # Rightmost column becomes topmost row, mapping down to left, and so on
    ordered = list(sorted(coords, key=real, reverse=True))
    xmax = ordered[0].real
    return {complex(coord.imag, xmax - coord.real) for coord in ordered}


# Over vertical
@hflip.register
def _(tile: tuple):
    return tuple(line[-1::-1] for line in tile)


@hflip.register
def _(coords: set, dim=None):
    dim = int(max(coords, key=real).real)
    return {complex(abs(coord.real - dim), coord.imag) for coord in coords}


# Over horizontal
@vflip.register
def _(tile: tuple):
    return tile[-1::-1]


@vflip.register
def _(coords: set, dim=None):
    dim = int(max(coords, key=imag).imag)
    return {complex(coord.real, abs(coord.imag - dim)) for coord in coords}


def two_flip(coords: set[complex], *args):
    return hflip(vflip(coords))


def find_monsters(monster, dimension, size):
    border = dimension * size
    found = set()
    transforms = (identity, vflip, hflip, two_flip)
    base = monster

    for _ in range(4):
        # Slide across image rowwise
        for transform in transforms:
            current = transform(base, size)

            # To shut up the linter
            if current is None:
                raise ValueError
            width = int(max(current, key=real).real) + 1
            height = int(max(current, key=imag).imag) + 1

            # Restore each coord to original x-position, but move one down at end of loop
            reset = (width - border) + 1j
            for _ in range(border - height):
                for _ in range(border - width):
                    if all(map[coord] for coord in current):
                        found.update(current)
                    current = {coord + 1 for coord in current}

                current = {coord + reset for coord in current}
                # This actually works
            if found:
                return len(found)
        base = left90(base)
    return 0


# Better idea: map each edge type to all tiles that have it
def find_orientations(tiles, edges, directions):
    reference = {}
    transforms = (
        identity,
        hflip,
        vflip,
        lambda x: hflip(vflip(x)),
    )

    def orient(tile, id):

        # Instead of tupling, create hash for each transformation and map to ID
        for _ in range(4):
            for transform in transforms:
                current = transform(tile)
                # It was a monster hash...
                hashed = edgetonumber("".join(current))
                top = edgetonumber(current[0])
                right = edgetonumber("".join(row[-1] for row in current))
                bottom = edgetonumber(current[-1])
                left = edgetonumber("".join(row[0] for row in current))

                # y increases downward
                if not hashed in reference:
                    reference[hashed] = (
                        dict(zip(directions, (top, right, bottom, left))),
                        id,
                        current,
                    )
                    # Add each edge to dict
                    for dir, edge in zip(directions, (top, right, bottom, left)):
                        edges[dir][edge].add(hashed)
                elif reference[hashed][1] != id:
                    # Everything breaks if different tiles yield same configuration
                    raise ValueError("Duplicate tile")
            tile = left90(tile)

    for id, tile in tiles.items():
        orient(tile, id)
    return edges, reference


def set_dict():
    return defaultdict(set)


@cache
def edgetonumber(edge):
    replacements = {".": "0", "#": "1"}
    return int("".join(replacements[char] for char in edge), base=2)


# mapping: coord -> hash
def dfs(mapping, reference, edges, position, used, max_extent):

    # used: ids of tiles placed
    match (position.real, position.imag):
        # Grid complete
        case (0, 0):
            for hashed in reference.keys():
                result = dfs(
                    mapping=mapping | {position: hashed},
                    reference=reference,
                    edges=edges,
                    used=used | {reference[hashed][1]},
                    position=1 + 0j,
                    max_extent=max_extent,
                )
                if result:
                    return result
            return None
        case (x, y):  # First row, not leftmost - match left
            # Grid filled, return
            if x == 0 and y > max_extent:
                return mapping
            # Left tile
            to_match = {}
            past_leftmost = x > 0
            past_top = y > 0
            if past_leftmost:
                left = mapping[position - 1]
                left_edge = reference[left][0][1]
                to_match[-1] = left_edge
            # Above tile
            if past_top:
                above = mapping[position - 1j]
                # y increases going down
                above_edge = reference[above][0][1j]
                to_match[-1j] = above_edge

            new_position = complex(0, y + 1) if x == max_extent else position + 1

            # A valid tile has to match both bottom edge of tile above and right of tile left
            if past_leftmost and past_top:
                candidates = set()
                # Left
                for cand in edges[-1][to_match[-1]]:
                    if reference[cand][1] not in used:
                        candidates.add(cand)
                # No matches found
                if not candidates:
                    return None
                confirmed = set()
                for cand in edges[-1j][to_match[-1j]]:
                    if cand in candidates:
                        confirmed.add(cand)
            else:
                target = -1j if past_top else -1
                confirmed = set()
                for cand in edges[target][to_match[target]]:
                    if reference[cand][1] not in used:
                        confirmed.add(cand)

            for hashed in confirmed:
                result = dfs(
                    mapping=mapping | {position: hashed},
                    reference=reference,
                    edges=edges,
                    used=used | {reference[hashed][1]},
                    position=new_position,
                    max_extent=max_extent,
                )
                if result:
                    return result
            return None

        case _:
            raise ValueError(f"Can't handle {position!r}")


# Remove borders
def trim(tile):
    return tuple(row[1:-1] for row in tile[1:-1])

    # if at start:
    # Try every tile in as top left
    # For each unused tile:
    # if right edge matches most recent left and if not top, top edge matches tile above
    #   Add tile in position
    # for coord, mapping


with open("inputs/day20.txt") as f:
    raw_input = f.read().split("\n\n")


dimension = int(sqrt(len(raw_input)))
tiles = dict(map(parse_tile, raw_input))
# top, right, bottom, left
directions = (-1j, 1, 1j, -1)
edges = {dir: set_dict() for dir in directions}


edges, reference = find_orientations(tiles, edges, directions)
tile_mapping = {complex(i, j): None for i in range(dimension) for j in range(dimension)}
grid = dfs(
    mapping=tile_mapping,
    reference=reference,
    edges=edges,
    position=0 + 0j,
    used=set(),
    max_extent=dimension - 1,
)
if not grid:
    raise ValueError

corners = [
    grid[0],
    grid[complex(0, dimension - 1)],
    grid[dimension - 1],
    grid[complex(dimension - 1, dimension - 1)],
]
part1 = prod(reference[corner][1] for corner in corners)
print(part1)


# Part 2

# Replace hashes in mapping with tiles
# Trim borders

grid = {k: trim(reference[v][2]) for k, v in grid.items()}
size = len(next(iter(grid.values()))[0])
map = {}

# coord -> char mapping
for coord, tile in grid.items():
    coord *= size
    re, im = coord.real, coord.imag
    for i, row in enumerate(tile):
        for j, char in enumerate(row):
            map[complex(re + j, im + i)] = char == "#"

total = sum(map.values())

monster_raw = """                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""
monster = {
    complex(j, i)
    for i, row in enumerate(monster_raw.splitlines())
    for j, char in enumerate(row)
    if char == "#"
}

part2 = total - find_monsters(monster, dimension, size)
print(part2)
