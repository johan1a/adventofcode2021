from collections import defaultdict, deque
from queue import PriorityQueue
import sys
import math


# target area: x=206..250, y=-105..-57
def get_input(filename):
    line = ""
    with open(filename, "r") as file:
        line = file.readline().strip().replace("target area: ", "")
    x, y = line.split(', ')
    x0, x1 = x.replace('x=', '').split('..')
    y0, y1 = y.replace('y=', '').split('..')

    return [int(x) for x in (x0, x1, y0, y1)]


def in_target(target, pos):
    (x0, x1, y0, y1) = target
    (xpos, ypos) = pos
    return xpos >= x0 and xpos <= x1 and ypos >= y0 and ypos <= y1


def overshot(target, pos):
    (x0, x1, y0, y1) = target
    (xpos, ypos) = pos
    return xpos > x1 or ypos < y1


def shoot(v0, target):
    (xpos, ypos) = (0, 0)
    (vx, vy) = v0
    maxy = 0
    hit = False
    closest_y = 1000000

    while not overshot(target, (xpos, ypos)) and not in_target(target, (xpos, ypos)):
        (x0, x1, y0, y1) = target

        xpos += vx
        ypos += vy
        vy -= 1
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        maxy = max(maxy, ypos)
        if in_target(target, (xpos,ypos)):
            hit = True

        if ypos < y0:
            ydiff = y0 - ypos
        elif ypos > y1:
            ydiff = ypos - y1
        else:
            ydiff = 0
        closest_y = min(closest_y, ydiff)

    #print(v0, hit, closest_y)
    return hit, maxy, closest_y


def part1(filename):
    target = get_input(filename)
    (x0, target_xmax, y0, y1) = target
    total_maxy = -1
    i = 0
    vy = 0
    xdiff = 1
    hit = False

    closest_y = 0
    while closest_y < 200:
        vx = 1
        for vx in range(1, target_xmax + 1):
            hit, maxy, closest_y = shoot((vx, vy), target)
            if hit:
                print(vx,vy)
                total_maxy = max(total_maxy, maxy)
        vy += 1
        print(total_maxy, closest_y)

    return total_maxy


#print(part1("test.txt"))
print(part1("input.txt"))
# result1 = part1("input.txt")
# print("Part 1: {}".format(result1))
