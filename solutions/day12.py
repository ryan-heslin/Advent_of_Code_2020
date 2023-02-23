from math import pi


orientations = {"N": 0 + 1j, "S": 0 - 1j, "E": 1 + 0j, "W": -1 + 0j}
rotations = {
    90: lambda x: complex(-x.imag, x.real),
    180: lambda x: complex(-x.real, -x.imag),
    270: lambda x: complex(x.imag, -x.real),
}


def l1(x):
    return abs(x.real) + abs(x.imag)


def solve(instructions, orientations, rotations):

    position = ship = 0
    waypoint = 10 + 1j
    direction = 1

    for pair in instructions:
        if change := orientations.get(pair[0]):
            shift = change * pair[1]
            position += shift
            waypoint += shift
        elif pair[0] == "F":
            position += direction * pair[1]
            shift = pair[1] * (waypoint - ship)
            # Waypoint moves with ship
            ship += shift
            waypoint += shift
        else:
            angle = pair[1]
            angle %= 360
            if pair[0] == "R":
                angle = abs(360 - angle)
            direction = rotations[angle](direction)
            # Rotate around ship
            waypoint = ship + rotations[angle](waypoint - ship)
    return position, ship


with open("inputs/day12.txt") as f:
    raw_input = f.read().splitlines()

processed = [(line[0], int(line[1:])) for line in raw_input]
positions = solve(processed, orientations, rotations)

part1 = int(l1(positions[0]))
print(part1)

part2 = int(l1(positions[1]))
print(part2)
