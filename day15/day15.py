from collections import defaultdict, deque
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
    end = (len(grid) - 1, len(grid[0]) - 1)
    #print_path(grid, parents, end)
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
    if result > 9 or result < 1:
        print("invalid val: " + str(result))
        exit(1)

    #if node[0] == 44 and node[1] == 0:
        #print("xextra: {}, yextra: {}".format(xextra, yextra))

    return result

def print_path2(grid, parents, end):
    if end in parents:
        parent = parents[end]
    else:
        parent = None
    path = []
    while parent != None:
        path.append(parent)
        if parent in parents:
            parent = parents[parent]
        else:
            parent = None
    for y in range(0, end[1] + 1):
        for x in range(0, end[0] + 1):
            if (x,y) in path:
                print('x', end="")
            else:
                print(get_val(grid, (x,y)), end="")
        print()

    for x in range(0, 5):
        xx = len(grid[0]) * x + 4
        yy = 0
        # 44,0
        print([xx, yy])
        print(get_val(grid, (xx, yy)), end=" ")
    print()

def part2(filename):
    grid = get_input(filename)

    #parents = defaultdict()
    dists = defaultdict(lambda: 10000000)
    visited = set()
    tovisit = set()

    end = (5 * len(grid) - 1, 5 * len(grid[0]) - 1)
    #print_path2(grid, parents, end)

    tovisit.add((0,0))
    dists[(0,0)] = 0

    while len(tovisit) > 0:
        node = mindist(dists, tovisit)
        tovisit.remove(node)
        visited.add(node)

        for neighbor in neighbors2(grid, node):
            nextdist = dists[node] + get_val(grid, neighbor)
            if neighbor not in visited and dists[neighbor] > nextdist:
                dists[neighbor] = nextdist
                tovisit.add(neighbor)
                #parents[neighbor] = node
    #print_path2(grid, parents, end)
    #print(end)


    return dists[end]

assert part1("test.txt") == 40
result1 = part1("input.txt")
assert result1 == 714
print("Part 1: {}".format(result1))
print("")

print(part2("test.txt"))
print(part2("input.txt"))
# result2 = part2("input.txt")
# assert result2 == 7477815755570
# print("Part 2: {}".format(result2))
