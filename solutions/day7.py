from collections import deque


def parse(lines):
    result = {}
    for line in lines:
        parts = line.split(", ")
        parts[0] = parts[0].split(" ")
        this_bag = " ".join(parts[0][:2])
        children = [parts[0][-4::1]] + [x.split(" ") for x in parts[1:]]
        if "no" in parts[0]:
            children = {}
        else:
            children = {" ".join(child[-3:-1:1]): int(child[-4]) for child in children}
        result[this_bag] = children
    return result


def find_ancestors(bag, graph):
    found = set()
    current = set([bag])
    while current:
        new_ancestors = frozenset(
            bag
            for bag, children in graph.items()
            if any(k in current for k in children.keys())
        )
        found.update(new_ancestors)
        current = new_ancestors
    return len(found)


def count_bags(root, graph):
    total = 0
    children = deque(graph[root].items())
    while children:
        child, bags = children.popleft()
        total += bags
        this_children = graph[child]
        children.extend(
            deque(zip(this_children.keys(), (v * bags for v in this_children.values())))
        )
    return total


with open("inputs/day7.txt") as f:
    raw_input = f.read().splitlines()

graph = parse(raw_input)

part1 = find_ancestors("shiny gold", graph)
print(part1)

part2 = count_bags("shiny gold", graph)
print(part2)
