from collections import defaultdict, deque
import  sys

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

def mindist(dists, nodes):
    return sorted(nodes, key=lambda k: dists[k])[0]

def print_path(grid, parents, end):

    parent = parents[end]
    path = []
    while parent != None:
        path.append(parent)
        if parent in parents:
            parent = parents[parent]
        else:
            parent = None
    for y in range(0, end[1]):
        for x in range(0, end[0]):
            if (x,y) in path:
                print('x', end="")
            else:
                print(grid[y][x], end="")
        print()


def part1(filename):
    grid = get_input(filename)

    parents = defaultdict()
    dists = defaultdict(lambda: 10000000)
    visited = set()
    tovisit = set()
    tovisit.add((0,0))
    dists[(0,0)] = 0

    while len(tovisit) > 0:
        node = mindist(dists, tovisit)
        tovisit.remove(node)
        visited.add(node)

        for neighbor in neighbors(grid, node):
            nextdist = dists[node] + grid[neighbor[0]][neighbor[1]]
            if neighbor not in visited and dists[neighbor] > nextdist:
                dists[neighbor] = nextdist
                tovisit.add(neighbor)
                parents[neighbor] = node
    print(dists)
    end = (len(grid) - 1, len(grid[0]) - 1)
    print_path(grid, parents, end)
    print(dists[end])

print(part1("test.txt"))
print(part1("input.txt"))
# result1 = part1("input.txt")
# assert result1 == 3411
# print("Part 1: {}".format(result1))
# print("")

# result2 = part2("input.txt")
# assert result2 == 7477815755570
# print("Part 2: {}".format(result2))
