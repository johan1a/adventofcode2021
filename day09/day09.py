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


def part1(filename):
    grid = get_input(filename)
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    total = 0
    for i in range(0, ymax + 1):
        for j in range(0, xmax + 1):
            height = grid[i][j]
            up = get_height(grid, ymax, xmax, i - 1, j)
            down = get_height(grid, ymax, xmax, i + 1, j)
            left = get_height(grid, ymax, xmax, i , j - 1)
            right = get_height(grid, ymax, xmax, i , j + 1)
            if height < up and height < down and height < left and height < right:
                total += height + 1

    print('Part 1 for {}: {}'.format(filename, total))

part1('test.txt')
part1('input.txt')
