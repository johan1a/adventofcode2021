from collections import defaultdict
import pprint

pp = pprint.PrettyPrinter(indent=2)


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    positions = []
    for line in lines:
        split = line.split()
        state = False
        if split[0] == 'on':
            state = True
        position = {'state': state}
        coords = split[1].split(',')
        x0, x1 = sorted(
            [int(k) for k in coords[0].replace('x=', '').split('..')])
        y0, y1 = sorted(
            [int(k) for k in coords[1].replace('y=', '').split('..')])
        z0, z1 = sorted(
            [int(k) for k in coords[2].replace('z=', '').split('..')])
        position['x'] = (x0, x1)
        position['y'] = (y0, y1)
        position['z'] = (z0, z1)
        positions.append(position)
    return positions


def outside(position, d=50):
    x0, x1 = position['x']
    y0, y1 = position['y']
    z0, z1 = position['z']
    if (z0 > d and z1 > d) or (z0 < -d and z1 < -d):
        return True
    if (y0 > d and y1 > d) or (y0 < -d and y1 < -d):
        return True
    if (x0 > d and x1 > d) or (x0 < -d and x1 < -d):
        return True


def part1(filename):
    total = 0
    cores = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: False)))
    positions = get_input(filename)
    for position in positions:
        if outside(position):
            continue
        print(position)
        for x in range(position['x'][0], position['x'][1] + 1):
            for y in range(position['y'][0], position['y'][1] + 1):
                for z in range(position['z'][0], position['z'][1] + 1):
                    next_state = position['state']
                    if not cores[x][y][z] and next_state:
                        total += 1
                    elif cores[x][y][z] and not next_state:
                        total -= 1
                    cores[x][y][z] = next_state
    return total


print(part1("input.txt"))

# assert part1("test.txt") == 739785
# result1 = part1("input.txt")
# assert result1 == 1073709
# print("Part 1: {}".format(result1))

# assert part2('test.txt') == 444356092776315
# result2 = part2("input.txt")
# assert result2 == 148747830493442
# print("Part 2: {}".format(result2))
