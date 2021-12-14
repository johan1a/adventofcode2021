from collections import defaultdict, deque

def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]
    counts = defaultdict(lambda: 0)
    initial = lines[0]
    for i in range(0, len(initial) - 1):
        counts[initial[i] + initial[i+1]] += 1

    rules = {}
    for i in range(2, len(lines)):
        rule = lines[i].split(' -> ')
        rules[rule[0]] = rule[1]

    return counts, rules

def run(filename, n):
    pair_counts, rules = get_input(filename)
    element_counts = defaultdict(lambda: 0)

    for pair in pair_counts:
        c0 = pair[0]
        c1 = pair[1]
        element_counts[c0] += 1
        element_counts[c1] += 1


    for i in range(0, n):
        diffs = defaultdict(lambda: 0)
        for rule in rules:
            if pair_counts[rule] > 0:
                c0 = rule[0]
                c1 = rule[1]
                result = rules[rule]
                diffs[rule] -= pair_counts[rule]
                diffs[c0 + result] += pair_counts[rule]
                diffs[result + c1] += pair_counts[rule]

                element_counts[result] += pair_counts[rule]
        for diff in diffs:
            pair_counts[diff] += diffs[diff]

    values = sorted(element_counts.values())
    return values[-1] - values[0]

def part1(filename):
    return run(filename, 10)

def part2(filename):
    return run(filename, 40)

assert part1("test.txt") == 1588
result1 = part1("input.txt")
assert result1 == 3411
print("Part 1: {}".format(result1))
print("")

result2 = part2("input.txt")
assert result2 == 7477815755570
print("Part 2: {}".format(result2))
