from collections import defaultdict

def get_initial_nbrs(filename):
    all_nbrs = []
    with open(filename, 'r') as file:
        all_nbrs = [int(n.strip()) for n in file.readline().split(',')]

    nbrs = defaultdict(lambda: 0)
    for nbr in all_nbrs:
        nbrs[nbr] += 1

    return nbrs

def get_cost(positions, current_pos):
    total = 0
    for pos in positions:
        if pos != current_pos:
            total += positions[pos] * abs(pos - current_pos)
    return total

def part1(filename):
    positions = get_initial_nbrs(filename)
    lowest_cost = 10000000
    best_pos = -1
    for pos in positions:
        cost = get_cost(positions, pos)
        if cost < lowest_cost:
            lowest_cost = cost
            best_pos = pos
    print("Part 1 for {}: Best pos: {}, cost: {}".format(filename, best_pos, lowest_cost))


cache = {}

def integral(n):
    if n in cache:
        return cache[n]
    i = 1
    result = 0
    while i <= n:
        result += i
        i += 1
    cache[n] = result
    return result

def get_cost2(positions, current_pos):
    total = 0
    for pos in positions:
        if pos != current_pos:
            total += positions[pos] * integral(abs(pos - current_pos))
    return total

def part2(filename):
    positions = get_initial_nbrs(filename)
    lowest_cost = -1
    best_pos = -1
    for pos in range(0, max(positions)):
        cost = get_cost2(positions, pos)
        if lowest_cost == -1 or cost < lowest_cost:
            lowest_cost = cost
            best_pos = pos
    print("Part 2 for {}: Best pos: {}, cost: {}".format(filename, best_pos, lowest_cost))



part1('test.txt')
part1('input.txt')
print('')

part2('test.txt')
part2('input.txt')
print('')
