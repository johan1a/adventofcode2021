from collections import defaultdict, deque
from queue import PriorityQueue
import sys, math


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [[int(k) for k in l.strip()] for l in file.readlines()]
    return lines


def in_range(grid, x, y):
    ymax = len(grid) - 1
    xmax = len(grid[0]) - 1
    if y < 0 or y > ymax or x < 0 or x > xmax:
        return False
    return True


def neighbors(grid, node):
    x0 = node[0]
    y0 = node[1]
    result = [
        (x0 + 1, y0),
        (x0 - 1, y0),
        (x0, y0 + 1),
        (x0, y0 - 1),
    ]
    return [n for n in result if in_range(grid, n[0], n[1])]


def part1(filename):
    grid = get_input(filename)

    parents = defaultdict()
    dists = defaultdict(lambda: 10000000)
    visited = set()
    tovisit = PriorityQueue()
    tovisit.put((0, (0, 0)))
    dists[(0, 0)] = 0

    while not tovisit.empty():
        (dist, node) = tovisit.get()
        visited.add(node)

        for neighbor in neighbors(grid, node):
            nextdist = dist + grid[neighbor[0]][neighbor[1]]
            if neighbor not in visited and dists[neighbor] > nextdist:
                dists[neighbor] = nextdist
                tovisit.put((nextdist, neighbor))
                parents[neighbor] = node
    end = (len(grid) - 1, len(grid[0]) - 1)
    return dists[end]


def in_range2(grid, x, y):
    ymax = 5 * len(grid) - 1
    xmax = 5 * len(grid[0]) - 1
    if y < 0 or y > ymax or x < 0 or x > xmax:
        return False
    return True


def neighbors2(grid, node):
    x0 = node[0]
    y0 = node[1]
    result = [
        (x0 + 1, y0),
        (x0 - 1, y0),
        (x0, y0 + 1),
        (x0, y0 - 1),
    ]
    return [n for n in result if in_range2(grid, n[0], n[1])]


def get_val(grid, node):
    xsize = len(grid[0])
    ysize = len(grid)
    x = node[0] % xsize
    y = node[1] % ysize
    xextra = math.floor(node[0] / xsize)
    yextra = math.floor(node[1] / ysize)
    extra = (xextra + yextra)
    result = (grid[y][x] + extra) % 10
    wraparounds = math.floor((grid[y][x] + extra) / 10)
    result += wraparounds
    return result


def part2(filename):
    grid = get_input(filename)

    dists = defaultdict(lambda: 10000000)
    visited = set()
    tovisit = PriorityQueue()

    dists[(0, 0)] = 0
    tovisit.put((0, (0, 0)))

    while not tovisit.empty():
        (dist, node) = tovisit.get()
        visited.add(node)

        for neighbor in neighbors2(grid, node):
            nextdist = dist + get_val(grid, neighbor)
            if neighbor not in visited and dists[neighbor] > nextdist:
                dists[neighbor] = nextdist
                tovisit.put((nextdist, neighbor))

    end = (5 * len(grid) - 1, 5 * len(grid[0]) - 1)
    return dists[end]


assert part1("test.txt") == 40
result1 = part1("input.txt")
assert result1 == 714
print("Part 1: {}".format(result1))
print("")

assert part2("test.txt") == 315
result2 = part2("input.txt")
assert result2 == 2948
print("Part 2: {}".format(result2))
