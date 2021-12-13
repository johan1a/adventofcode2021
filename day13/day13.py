from collections import defaultdict, deque

def get_input(filename):
    lines = []
    coords = set()
    folds = []
    with open(filename, "r") as file:
        lines = file.readlines()
    for line in lines:
        if "," in line:
            x,y = [int(n) for n in line.split(",")]
            coords.add((x,y))
        elif "fold along x" in line:
            folds.append({"x": int(line.split("fold along x=")[1])})
        elif "fold along y" in line:
            folds.append({"y": int(line.split("fold along y=")[1])})
    return coords,folds

def do_fold(coords, fold):
    new_coords = set()
    to_remove = set()
    if "x" in fold:
        foldx = fold["x"]
        for (x,y) in coords:
            if x == foldx:
                to_remove.add((x,y))
            elif x > foldx:
                to_remove.add((x,y))
                new_coords.add((foldx - (x - foldx), y))

    elif "y" in fold:
        foldy = fold["y"]
        for (x,y) in coords:
            if y == foldy:
                to_remove.add((x,y))
            elif y > foldy:
                to_remove.add((x,y))
                new_coords.add((x, (foldy - (y - foldy))))
    coords.update(new_coords)
    for (x,y) in to_remove:
        coords.remove((x,y))
    return coords


def part1(filename):
    coords, folds = get_input(filename)

    coords = do_fold(coords, folds[0])

    return len(coords)

def part2(filename):
    coords, folds = get_input(filename)

    for fold in folds:
        coords = do_fold(coords, fold)

    endx = None
    endy = None
    i = -1
    while endx == None:
        if "x" in folds[i]:
            endx = folds[i]["x"]
            break
        i -= 1
    i = -1
    while endy == None:
        if "y" in folds[i]:
            endy = folds[i]["y"]
            break
        i -= 1

    for y in range(0, endy):
        for x in range(0, endx):
            if (x, y) in coords:
                print("#", end="")
            else:
                print(".", end="")
        print("")

    return len(coords)

assert part1("test.txt") == 17
result1 = part1("input.txt")
print("Part 1: {}".format(result1))
print("")

print("Part 2:")
part2("input.txt")
