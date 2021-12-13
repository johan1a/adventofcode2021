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

#print(part1("test.txt"))
assert part1("test.txt") == 17
result1 = part1("input.txt")
#assert result1 == 3510
print("Part 1: {}".format(result1))
print("")

