from collections import defaultdict
import pprint
import sys
import numpy as np
import matplotlib.pyplot as plt

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
        position['x'] = (x0, x1 + 1)
        position['y'] = (y0, y1 + 1)
        position['z'] = (z0, z1 + 1)
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
        for x in range(position['x'][0], position['x'][1]):
            for y in range(position['y'][0], position['y'][1]):
                for z in range(position['z'][0], position['z'][1]):
                    next_state = position['state']
                    if not cores[x][y][z] and next_state:
                        total += 1
                    elif cores[x][y][z] and not next_state:
                        total -= 1
                    cores[x][y][z] = next_state
    return total


def get_bottom(box, diff):
    if box['z'][0] < diff['z'][0] and box['z'][1] >= diff['z'][0]:
        z0 = box['z'][0]
        z1 = diff['z'][0]
        return {
            'x': [box['x'][0], box['x'][1]],
            'y': [box['y'][0], box['y'][1]],
            'z': [z0, z1]
        }
    else:
        return None


def get_top(box, diff):
    if box['z'][1] > diff['z'][1] and box['z'][1] >= diff['z'][0]:
        z0 = diff['z'][1]
        z1 = box['z'][1]
        return {
            'x': [box['x'][0], box['x'][1]],
            'y': [box['y'][0], box['y'][1]],
            'z': [z0, z1]
        }
    else:
        return None


def get_left(box, diff):
    if box['x'][0] < diff['x'][0] and box['x'][1] >= diff['x'][0]:
        x0 = box['x'][0]
        x1 = diff['x'][0]
        z0 = max(box['z'][0], diff['z'][0])
        z1 = min(box['z'][1], diff['z'][1])
        return {'x': [x0, x1], 'y': [box['y'][0], box['y'][1]], 'z': [z0, z1]}
    else:
        return None


def get_right(box, diff):
    if box['x'][1] > diff['x'][1] and box['x'][0] <= diff['x'][1]:
        x0 = diff['x'][1]
        x1 = box['x'][1]
        z0 = max(box['z'][0], diff['z'][0])
        z1 = min(box['z'][1], diff['z'][1])
        return {'x': [x0, x1], 'y': [box['y'][0], box['y'][1]], 'z': [z0, z1]}
    else:
        return None


def get_front(box, diff):
    if box['y'][1] > diff['y'][1] and box['y'][0] <= diff['y'][1]:
        x0 = max(diff['x'][0], box['x'][0])
        x1 = min(diff['x'][1], box['x'][1])
        z0 = max(box['z'][0], diff['z'][0])
        z1 = min(box['z'][1], diff['z'][1])
        return {'x': [x0, x1], 'y': [diff['y'][1], box['y'][1]], 'z': [z0, z1]}
    else:
        return None


def get_back(box, diff):
    if box['y'][0] < diff['y'][0] and box['y'][1] >= diff['y'][0]:
        x0 = max(diff['x'][0], box['x'][0])
        x1 = min(diff['x'][1], box['x'][1])
        z0 = max(box['z'][0], diff['z'][0])
        z1 = min(box['z'][1], diff['z'][1])
        return {'x': [x0, x1], 'y': [box['y'][0], diff['y'][0]], 'z': [z0, z1]}
    else:
        return None


def split(box, diff):
    bottom = get_bottom(box, diff)
    top = get_top(box, diff)
    left = get_left(box, diff)
    right = get_right(box, diff)
    front = get_front(box, diff)
    back = get_back(box, diff)
    new_boxes = [bottom, top, left, right, front, back]

    return [b for b in new_boxes if b != None]


def calculate_volume(boxes):
    total = 0
    for box in boxes:
        volume = (box['x'][1] - box['x'][0]) * (box['y'][1] - box['y'][0]) * (
            box['z'][1] - box['z'][0])
        total += volume
    return total


def intersects(box, diff):
    outside = diff['x'][0] > box['x'][1] or diff['x'][1] < box['x'][0] or diff[
        'y'][0] > box['y'][1] or diff['y'][1] < box['y'][0] or diff['z'][
            0] > box['z'][1] or diff['z'][1] < box['z'][0]
    return not outside


def plot_box(ax, box, color):
    for zz in range(0, 2):
        x = np.linspace(box['x'][0], box['x'][1], 10)
        y = np.linspace(box['y'][0], box['y'][0], 10)
        z = np.linspace(box['z'][zz], box['z'][zz], 10)
        ax.plot3D(x, y, z, color)

        x = np.linspace(box['x'][0], box['x'][1], 10)
        y = np.linspace(box['y'][1], box['y'][1], 10)
        z = np.linspace(box['z'][zz], box['z'][zz], 10)
        ax.plot3D(x, y, z, color)

        x = np.linspace(box['x'][0], box['x'][0], 10)
        y = np.linspace(box['y'][0], box['y'][1], 10)
        z = np.linspace(box['z'][zz], box['z'][zz], 10)
        ax.plot3D(x, y, z, color)

        x = np.linspace(box['x'][1], box['x'][1], 10)
        y = np.linspace(box['y'][0], box['y'][1], 10)
        z = np.linspace(box['z'][zz], box['z'][zz], 10)
        ax.plot3D(x, y, z, color)

    x = np.linspace(box['x'][0], box['x'][0], 10)
    y = np.linspace(box['y'][0], box['y'][0], 10)
    z = np.linspace(box['z'][0], box['z'][1], 10)
    ax.plot3D(x, y, z, color)

    x = np.linspace(box['x'][1], box['x'][1], 10)
    y = np.linspace(box['y'][0], box['y'][0], 10)
    z = np.linspace(box['z'][0], box['z'][1], 10)
    ax.plot3D(x, y, z, color)

    x = np.linspace(box['x'][1], box['x'][1], 10)
    y = np.linspace(box['y'][1], box['y'][1], 10)
    z = np.linspace(box['z'][0], box['z'][1], 10)
    ax.plot3D(x, y, z, color)

    x = np.linspace(box['x'][0], box['x'][0], 10)
    y = np.linspace(box['y'][1], box['y'][1], 10)
    z = np.linspace(box['z'][0], box['z'][1], 10)
    ax.plot3D(x, y, z, color)


def plot_boxes(originals, split_boxes, diff):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for original in originals:
        plot_box(ax, original, 'blue')
    for box in split_boxes:
        plot_box(ax, box, 'green')
    plot_box(ax, diff, 'red')
    plt.show()


def part2(filename):
    boxes = []
    positions = get_input(filename)
    i = 0
    for diff in positions:
        i += 1
        on = diff['state']
        boxes_to_add = []
        boxes_to_remove = []
        for box in boxes:

            if intersects(box, diff):
                new_boxes = split(box, diff)

                boxes_to_remove.append(box)
                for new_box in new_boxes:
                    boxes_to_add.append(new_box)
        for new_box in boxes_to_add:
            boxes.append(new_box)
        for box in boxes_to_remove:
            boxes.remove(box)
        if on:
            boxes.append(diff)


    return calculate_volume(boxes)


result1 = part1("input.txt")
assert result1 == 653798
print("Part 1: {}".format(result1))

if False:
    assert part2("test1.txt") == 26
    assert part2("test2.txt") == 25
    assert part2("test3.txt") == 24
    assert part2("test4.txt") == 21
    assert part2("test5.txt") == 18
    assert part2("test6.txt") == 9
    assert part2("test7.txt") == 0
    assert part2("test8.txt") == 24
    assert part2("test9.txt") == 48
    assert part2("test10.txt") == 48
    assert part2("test11.txt") == 48
    assert part2("test12.txt") == 0
    assert part2('test15.txt') == 1557
    assert part2('test16.txt') == 1

assert part2('input_small.txt') == 653798
assert part2('test13.txt') == 2758514936282235
result2 = part2('input.txt')
assert result2 == 1257350313518866
print("Part 2: {}".format(result2))
