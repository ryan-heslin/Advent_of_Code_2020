from math import prod


def parse(lines):
    ranges, mine, others = lines
    ranges_map = {}
    for line in ranges.split("\n"):
        field, values = line.split(": ")
        these_ranges = [
            [int(num) for num in pair.split("-")] for pair in values.split(" or ")
        ]
        ranges_map[field] = these_ranges

    mine = [int(x) for x in mine.splitlines()[1].split(",")]
    others = [[int(x) for x in line.split(",")] for line in others.splitlines()[1:]]

    return ranges_map, mine, others


def invalid_sum(tickets, allowed):
    invalid = set()

    s = 0
    for i, ticket in enumerate(tickets):
        valid = True
        for field in ticket:
            for possibility in allowed.values():
                if field in possibility:
                    break
            else:
                s += field
                valid = False
        if not valid:
            invalid.add(i)
    return s, invalid


def discover_fields(tickets, ranges):
    possibilities = [set(allowed.keys()) for _ in range(len(allowed))]
    for ticket in tickets:
        for i, val in enumerate(ticket):
            if len(possibilities[i]) > 1:
                possibilities[i] = {
                    field for field in possibilities[i] if val in ranges[field]
                }
    return possibilities


def solve(possibilities):
    lengths = {len(di): i for i, di in enumerate(possibilities)}
    number = len(lengths)
    done = set()

    for i in range(1, number + 1):
        new = set()
        for field in possibilities[lengths[i]]:
            if field not in done:
                done.add(field)
                new.add(field)
        possibilities[lengths[i]] = new
    return possibilities


with open("inputs/day16.txt") as f:
    raw_input = f.read().split("\n\n")

ranges, mine, others = parse(raw_input)
allowed = {
    field: set(
        list(range(line[0][0], line[0][1] + 1))
        + list(range(line[1][0], line[1][1] + 1))
    )
    for field, line in ranges.items()
}
part1, invalid = invalid_sum(others, allowed)
print(part1)

others = [ticket for i, ticket in enumerate(others) if i not in invalid]
possibilities = discover_fields(others, allowed)
fields = solve(possibilities)
part2 = prod(
    mine[i] for i, field in enumerate(possibilities) if field.pop()[:9] == "departure"
)
print(part2)
