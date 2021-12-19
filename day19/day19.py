from collections import defaultdict
import math
import pprint
pp = pprint.PrettyPrinter(indent=2)

# Here be dragons


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    scanners = []
    i = 0
    while i < len(lines):
        scanner = {'beacons': set(), 'id': len(scanners)}
        i += 1
        while i < len(lines) and lines[i] != '':
            coord = tuple([int(n) for n in lines[i].split(',')])
            scanner['beacons'].add(coord)
            i += 1
        i += 1
        scanners.append(scanner)
    return scanners


def round_point(point):
    nbr_decimals = 5
    return (round(point[0], nbr_decimals), round(point[1], nbr_decimals),
            round(point[2], nbr_decimals))


# I blatantly stole this from https://github.com/morgoth1145/advent-of-code/blob/ed74bf9d1d1761edd1df781551a42752aa1a25cc/2021/19/solution.py#L3
rotations = [
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
]


# I stole this too...
def rotate(beacons, i):
    result = []
    for coord in beacons:
        x = sum(a * b for a, b in zip(coord, rotations[i][0]))
        y = sum(a * b for a, b in zip(coord, rotations[i][1]))
        z = sum(a * b for a, b in zip(coord, rotations[i][2]))
        result.append((x, y, z))
    return result


def get_offset(point0, point1):
    dx, dy, dz = (point1[0] - point0[0], point1[1] - point0[1],
                  point1[2] - point0[2])
    return (dx, dy, dz)


def translate(point, offset):
    return (point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])


def check_overlap(canonical_beacons, scanner, nbr_required):
    for i in range(0, 24):
        beacons = rotate(scanner['beacons'], i)
        for b0 in canonical_beacons:
            for assumed_overlapping in beacons:
                matching = 1

                offset = get_offset(assumed_overlapping, b0)

                all_translated = set()
                for b2 in beacons:
                    translated = translate(b2, offset)
                    if translated in canonical_beacons:
                        matching += 1
                    all_translated.add(translated)

                if matching >= nbr_required:
                    canonical_beacons.update(all_translated)
                    scanner['offset'] = offset
                    return True


def part1(filename, nbr_required=12):
    scanners = get_input(filename)
    canonical_beacons = set()
    canonical_beacons.update(scanners[0]['beacons'])
    added = {0}

    i = 1
    while len(added) < len(scanners):
        print(i)
        scanner = scanners[i]
        if scanner['id'] not in added:
            if check_overlap(canonical_beacons, scanner, nbr_required):
                added.add(scanner['id'])
                print("added", scanner['id'], len(added), "/", len(scanners))

        i = (i + 1) % len(scanners)

    scanners[0]['offset'] = (0, 0, 0)

    max_dist = 0
    for scanner0 in scanners:
        for scanner1 in scanners:
            offset0 = scanner0['offset']
            offset1 = scanner1['offset']
            dist = abs(offset0[0] - offset1[0]) + abs(
                offset0[1] - offset1[1]) + abs(offset0[2] - offset1[2])
            if dist > max_dist:
                max_dist = dist

    return len(canonical_beacons), max_dist


test_part1, test_part2 = part1("test.txt")
assert test_part1 == 79
assert test_part2 == 3621
result1, result2 = part1("input.txt")
assert result1 == 472
print("Part 1: {}".format(result1))
print("Part 2: {}".format(result2))
