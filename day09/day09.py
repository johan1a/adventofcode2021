from collections import defaultdict

def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        lines = [[int(c) for c in l.strip()] for l in file.readlines()]

    return lines

big_number = 10000000

def get_height(grid, ymax, xmax, y, x):
    if y < 0 or y > ymax or x < 0 or x > xmax:
        return big_number
    return grid[y][x]

def get_low_points(grid):
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    low_points = set()
    for i in range(0, ymax + 1):
        for j in range(0, xmax + 1):
            height = grid[i][j]
            up = get_height(grid, ymax, xmax, i - 1, j)
            down = get_height(grid, ymax, xmax, i + 1, j)
            left = get_height(grid, ymax, xmax, i , j - 1)
            right = get_height(grid, ymax, xmax, i , j + 1)
            if height < up and height < down and height < left and height < right:
                low_points.add((i, j))
    return low_points

def part1(filename):
    grid = get_input(filename)
    low_points = get_low_points(grid)
    total = 0
    for point in low_points:
        total += grid[point[0]][point[1]] + 1

    print('Part 1 for {}: {}'.format(filename, total))

def part_of_basin(grid, point):
    y = point[0]
    x = point[1]
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    return not (y < 0 or y > ymax or x < 0 or x > xmax or grid[y][x] == 9)

def part2(filename):
    grid = get_input(filename)
    xmax = len(grid[0])
    ymax = len(grid)
    low_points = get_low_points(grid)
    sizes = []
    for point in low_points:
        size = 0
        neighbors = [point]
        seen = set()
        while len(neighbors) > 0:
            neighbor = neighbors.pop(0)
            py = neighbor[0]
            px = neighbor[1]
            if neighbor not in seen and part_of_basin(grid, neighbor):
                size += 1
                seen.add(neighbor)
                neighbors.append((py + 1, px))
                neighbors.append((py - 1, px))
                neighbors.append((py, px + 1))
                neighbors.append((py, px - 1))
        sizes.append(size)

    sizes = sorted(sizes)
    total = sizes[-1] * sizes[-2] * sizes[-3]

    print('Part 2 for {}: {}'.format(filename, total))

part1('test.txt')
part1('input.txt')
print('')

part2('test.txt')
part2('input.txt')
