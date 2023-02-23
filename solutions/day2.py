with open("inputs/day2.txt") as f:
    raw_input = f.read().splitlines()


def parse(line):
    parts = line.split(" ")
    rnge = parts[0].split("-")
    return {
        "lower": int(rnge[0]),
        "upper": int(rnge[1]),
        "char": parts[1].rstrip(":"),
        "password": parts[2],
    }


def solve(policies):
    part1 = part2 = 0
    for policy in policies:
        part1 += (
            policy["lower"]
            <= policy["password"].count(policy["char"])
            <= policy["upper"]
        )
        part2 += (policy["password"][policy["lower"] - 1] == policy["char"]) ^ (
            policy["password"][policy["upper"] - 1] == policy["char"]
        )
    return part1, part2


processed = map(parse, raw_input)
part1, part2 = solve(processed)
print(part1)
print(part2)
