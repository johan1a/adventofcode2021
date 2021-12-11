from collections import defaultdict, deque

def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        lines = [[int(n) for n in l.strip()] for l in file.readlines()]
    return lines

def in_range(grid, y, x):
    ymax = len(grid) - 1
    xmax = len(grid[0]) - 1
    if y < 0 or y > ymax or x < 0 or x > xmax:
        return False
    return True

def neighbors(grid, y0, x0):
    result = []
    for y in range(y0-1,y0+2):
        for x in range(x0-1,x0+2):
            if (x != x0 or y != y0) and in_range(grid, y, x):
                result.append((y, x))
    return result

def print_grid(grid):
    for line in grid:
        for c in line:
            if c > 9:
                print('F', end="")
            else:
                print(c, end="")
        print('')
    print('')

def run(filename, max_steps=100, part2=False):
    levels = get_input(filename)

    flashes = 0
    octos = deque()
    for step in range(0, max_steps):
        flashed = defaultdict(lambda: False)
        for y in range(0, len(levels)):
            for x in range(0, len(levels[0])):
                if levels[y][x] > 9:
                    levels[y][x] = 0
                octos.append((y,x))
        while len(octos) > 0:
            y,x = octos.pop()
            levels[y][x] += 1

            if levels[y][x] > 9 and not flashed[(y,x)]:
                flashes += 1
                flashed[(y,x)] = True

                for neighbor in neighbors(levels, y, x):
                    octos.append(neighbor)

        if part2 and len(flashed) == len(levels) * len(levels[0]):
            print('Part 2 for {}: {}'.format(filename, step + 1))
            break
        #print_grid(levels)

    if not part2:
        print('Part 1 for {}: {}'.format(filename, flashes))

def part1(filename, max_steps = 100):
    run(filename, max_steps, part2=False)

def part2(filename):
    run(filename, 1000000, part2=True)

part1('test1.txt', 2)
part1('test.txt', 100)
part1('input.txt', 100)

print('')
part2('test.txt')
part2('input.txt')
