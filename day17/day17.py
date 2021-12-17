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
    return xpos > x1 or ypos < y0


def shoot(v0, target):
    (xpos, ypos) = (0, 0)
    (vx, vy) = v0
    maxy = 0
    hit = False
    closest_y = 1000000

    while not overshot(target, (xpos, ypos)) and not in_target(target, (xpos, ypos)):
        (x0, x1, y0, y1) = target

        if (v0 == (6, 0)) or (v0 == (7, -1)):
            print("pos", xpos, ypos, "vel:", vx, vy)

        xpos += vx
        ypos += vy
        vy -= 1
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        maxy = max(maxy, ypos)
        if in_target(target, (xpos, ypos)):
            hit = True
            if (v0 == (6, 0)) or (v0 == (7, -1)):
                print("hit")

        if ypos < y0:
            ydiff = y0 - ypos
        elif ypos > y1:
            ydiff = ypos - y1
        else:
            ydiff = 0
        closest_y = min(closest_y, ydiff)

        if (v0 == (6, 0)) or (v0 == (7, -1)):
            print("overshot?", target, overshot(target, (xpos, ypos)))

    #print(v0, hit, closest_y)
    return hit, maxy, closest_y


def part1(filename):
    target = get_input(filename)
    (x0, target_xmax, y0, y1) = target
    total_maxy = -1
    vy = 0
    xdiff = 1
    hit = False

    closest_y = 0
    while closest_y < 200:
        vx = 1
        for vx in range(1, target_xmax + 1):
            hit, maxy, closest_y = shoot((vx, vy), target)
            if hit:
                #print(vx,vy)
                total_maxy = max(total_maxy, maxy)
        vy += 1
        #print(total_maxy, closest_y)

    return total_maxy


def part2(filename):
    target = get_input(filename)
    (x0, target_xmax, y0, y1) = target
    vy = 0
    xdiff = 1
    hit = False
    closest_y = 0
    nbr_hits = 0
    hits = set()
    ydiff = 1
    maxdiff = 200
    while abs(closest_y) < maxdiff or ydiff == 1:
        for vx in range(0, target_xmax + 2):
            hit, maxy, closest_y = shoot((vx, vy), target)
            if hit:
                nbr_hits += 1
                hits.add((vx, vy))
                #print(vx,vy)
            # if vx == 6 and vy == 0 or vx == 7 and vy == -1:
            #     print(vx, vy, closest_y, hit)
        vy += ydiff
        #print(total_maxy, closest_y)
        if abs(closest_y) >= maxdiff:
            if ydiff == -1:
                break
            closest_y = 0
            vy = 0
            ydiff = -1
            print("switcheroo")

    # for hit in sorted(hits):
    #     print("{},{}".format(hit[0],hit[1]))

    print(len(hits))
    return len(hits)


#missing:
#< 6,0
#< 7,-1

#print(part1("test.txt"))
#print(part1("input.txt"))
# result1 = part1("input.txt")
# print("Part 1: {}".format(result1))

print(part2("input.txt"))
