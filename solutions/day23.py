def parse(num):
    return [int(x) for x in str(num)]


def link(number):
    nums = [int(x) for x in str(number)]
    result = {}

    for i in range(len(nums) - 1):
        result[nums[i]] = nums[i + 1]
    result[nums[-1]] = nums[0]

    return result


def unwind(cups, start=1):
    n = len(cups)
    this_cup = start
    result = []

    for _ in range(n - 1):
        next_cup = cups[this_cup]
        result.append(next_cup)
        this_cup = next_cup
    return result


def crab_cups(cups, iterations, start):
    lowest = min(cups.keys())
    highest = max(cups.keys())
    span = lowest - highest
    current_cup = start
    to_remove = 3

    iter = range(to_remove - 1)

    for _ in range(iterations):

        # Get first of three target cups
        current_right = cups[current_cup]
        removals = set((current_right,))
        this_removal = current_right

        # Add next two cups to remove to set
        for __ in iter:
            next_removal = cups[this_removal]
            removals.add(next_removal)
            this_removal = next_removal

        # Splice hole in linked list from removal
        cups[current_cup] = cups[this_removal]
        # Find next valid destination cup
        destination_cup = current_cup
        while destination_cup in removals or destination_cup == current_cup:
            destination_cup -= 1 if destination_cup != lowest else span

        # Cup right of destination
        destination_right = cups[destination_cup]

        cups[destination_cup] = current_right
        cups[this_removal] = destination_right
        current_cup = cups[current_cup]

    return cups


# For each iteration:
# Get first of three target cups
# Read three target cups into set
# Record cup right of rightmost target cup
# While true
# Subtract 1 from current cup or wrap around if min cup
# If cup not current cup and not in removed cups, break

# Set current cup's right cup first of target cups
# Set rightmost of target cup's right cup cup right of current cup
# Set current cup next cup


raw_input = 476138259
cups = link(raw_input)
last_digit = raw_input % 10
first_digit = raw_input // (10 ** (len(cups) - 1))
result = crab_cups(cups.copy(), 100, first_digit)
part1 = "".join(str(x) for x in unwind(result))
print(part1)

# Actual digit position needed to align range
size = 1000000
next = max(cups.keys()) + 1
cups[last_digit] = next

# Add increasing range to right of present cups
for i in range(next, size):
    cups[i] = i + 1
cups[size] = first_digit

result = crab_cups(cups.copy(), 10000000, first_digit)
target = min(cups.keys())
first_right = result[target]
part2 = first_right * result[first_right]
print(part2)
