import re


def parse(lines):
    result = {}

    for line in lines:
        rule, specs = line.split(": ")
        specs = specs.split(" | ")
        specs = [
            [
                token.strip('"') if '"' in token else int(token)
                for token in alternative.split(" ")
            ]
            for alternative in specs
        ]
        result[int(rule)] = specs
    return result


def resolve(string, rules):
    def inner(rule, index):
        specs = rules[rule]
        for alternative in specs:
            i = index
            for token in alternative:
                if type(token) is str:
                    i = -1 if token != string[i] else i + 1
                else:
                    # Recursive
                    i = inner(token, i)
                if i == -1:
                    break
            else:
                return i
        return -1

    return inner(0, 0) == len(string)


def wrap(string):
    return f"(?:{string})"


def to_regex(rule, variable_rules):
    specs = rules[rule]
    first = specs[0]

    if type(first[0]) == str:
        return first[0]
    result = "".join(to_regex(new_rule, variable_rules) for new_rule in first)
    if len(result) > 1:
        result = wrap(result)
    if len(specs) > 1 and rule not in variable_rules:
        second = "".join(to_regex(new_rule, variable_rules) for new_rule in specs[1])
        if len(second) > 1:
            second = wrap(second)
        result = wrap(
            "|".join(
                [
                    result,
                    second,
                ]
            )
        )
    return result


def verify(string, left_regex, right_regex, full_regex):
    if re.match(full_regex, string):
        left = re.match("^" + left_regex + "+", string)
        left_matches = re.findall(left_regex, string[: left.end()])
        right_matches = re.findall(right_regex, string[left.end() :])
        return (
            "".join(left_matches) + "".join(right_matches) == string
            and len(right_matches) > 0
            and len(left_matches) > len(right_matches)
        )
    return False


with open("inputs/day19.txt") as f:
    raw_input = f.read()

rules, strings = list(map(str.splitlines, raw_input.split("\n\n")))
rules = parse(rules)

part1 = sum(list(resolve(string, rules) for string in strings))
print(part1)

# Only need to try all repeat lengths for rule 8, since 11 always matches exactly
new_rules = """8: 42 | 42 8
11: 42 31 | 42 11 31"""
new_rules_parsed = parse(new_rules.splitlines())
variable_rules = tuple(new_rules_parsed.keys())

left_regex = wrap(to_regex(rules[variable_rules[0]][0][0], variable_rules))
right_regex = wrap(to_regex(rules[variable_rules[1]][0][1], variable_rules))
if rules[0] == reversed(variable_rules):
    left_regex, right_regex = right_regex, left_regex

full_regex = "^" + left_regex + "+" + right_regex + "+$"

part2 = sum(verify(string, left_regex, right_regex, full_regex) for string in strings)
print(part2)
