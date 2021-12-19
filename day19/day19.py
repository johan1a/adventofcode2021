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
        scanner['overlap'] = defaultdict(lambda: set())
        scanner['rot_indices'] = defaultdict(lambda: set())
        i += 1
        while i < len(lines) and lines[i] != '':
            coord = tuple([int(n) for n in lines[i].split(',')])
            scanner['beacons'].add(coord)
            i += 1
        i += 1
        scanners.append(scanner)
    return scanners


def distance_between(b0, b1):
    return math.sqrt(
        pow(b1[0] - b0[0], 2) + pow(b1[1] - b0[1], 2) + pow(b1[2] - b0[2], 2))


def calculate_distances(scanner):
    distances = defaultdict(lambda: set())
    for beacon0 in scanner['beacons']:
        for beacon1 in scanner['beacons']:
            if beacon0 != beacon1:
                distance = distance_between(beacon0, beacon1)
                distances[distance].add((beacon0, beacon1))
    scanner['distances'] = distances


def edge_distance(beacons0, beacons1):
    # TODO assuming only one edge per distance for now
    assert len(beacons0) == 2
    assert len(beacons1) == 2
    distances = set()
    for edge0 in beacons0:
        for edge1 in beacons1:
            # print('edge0',edge0,'edge1',edge1)
            d0 = distance_between(edge0[0], edge1[0])
            d1 = distance_between(edge0[1], edge1[1])
            distances.add((d0, d1))
    return distances


def round_point(point):
    nbr_decimals = 5
    return (round(point[0], nbr_decimals), round(point[1], nbr_decimals),
            round(point[2], nbr_decimals))


def rotate_around_z(point, rad):
    x = point[0] * math.cos(rad) - point[1] * math.sin(rad)
    y = point[0] * math.sin(rad) + point[1] * math.cos(rad)
    z = point[2]
    return round_point((x, y, z))


def rotate_around_y(point, rad):
    x = point[0] * math.cos(rad) + point[2] * math.sin(rad)
    y = point[1]
    z = -point[0] * math.sin(rad) + point[2] * math.cos(rad)
    return round_point((x, y, z))


def rotate_around_x(point, rad):
    x = point[0]
    y = point[1] * math.cos(rad) - point[2] * math.sin(rad)
    z = point[1] * math.sin(rad) + point[2] * math.cos(rad)
    return round_point((x, y, z))


def rotate(beacon):
    points = []
    for xi in range(0, 4):
        xrad = xi * math.pi / 2
        pointx = rotate_around_x(beacon, xrad)
        points.append(pointx)
        for yi in range(0, 4):
            yrad = yi * math.pi / 2
            pointy = rotate_around_y(pointx, yrad)
            points.append(pointy)
            for zi in range(0, 4):
                zrad = zi * math.pi / 2
                pointz = rotate_around_z(pointy, zrad)
                points.append(pointz)
    return points


def get_offset(point0, point1):
    dx, dy, dz = (point1[0] - point0[0], point1[1] - point0[1],
                  point1[2] - point0[2])
    return (dx, dy, dz)


# find origin and rotation of scanner1 in scanner0's coordinate system
def find_origin(distances0, distances1, matching_edges):

    possible = defaultdict(lambda: defaultdict(lambda: 0))
    for distance in matching_edges:
        pairs0 = distances0[distance]
        pairs1 = distances1[distance]

        for e0 in pairs0:
            for e1 in pairs1:
                possible[e1[0]][e0[0]] += 1
                possible[e1[0]][e0[1]] += 1
                possible[e1[1]][e0[0]] += 1
                possible[e1[1]][e0[1]] += 1

    decided = {}
    for point in possible:
        highest = -1
        best = None
        choices = possible[point]
        for choice in choices:
            if choices[choice] > highest:
                best = choice
                highest = choices[choice]
        decided[point] = best

    rot_index = 0
    while rot_index < 84:  #TODO check
        offsets = set()
        for point in decided:
            offset = get_offset(rotate(point)[rot_index], decided[point])
            offsets.add(offset)
        if len(offsets) == 1:
            break
        rot_index += 1

    return decided, rot_index

def inverse_decided(decided):
    result = {}
    for point in decided:
        result[decided[point]] = point
    return result

# TODO rename
def find_factors(scanner0, scanner1, tentative, distances0, distances1,
                 nbr_required):
    match_counts = defaultdict(lambda: 0)

    matching = defaultdict(lambda: set())
    for edge0 in tentative:

        for edge1 in tentative:
            if edge0 != edge1:
                d0 = edge_distance(distances0[edge0], distances0[edge1])
                d1 = edge_distance(distances1[edge0], distances1[edge1])
                if d0 == d1:
                    matching[edge0].add(edge1)
                    matching[edge0].add(edge0)

    for m in matching:
        if len(matching[m]) >= nbr_required / 2 - 1:
            decided, rot_index = find_origin(distances0, distances1, matching[m])
            scanner0['overlap'][scanner1['id']] = decided
            scanner0['rot_indices'][scanner1['id']] = rot_index
            print(scanner0['id'], scanner1['id'], rot_index)
            #scanner1['overlap'][scanner0['id']] = inverse_decided(decided)
            return True

    return False


def part1(filename, nbr_required=12):
    scanners = get_input(filename)
    for scanner in scanners:
        calculate_distances(scanner)
    canonical_beacons = set()
    canonical_beacons.update(scanners[0]['beacons'])
    added = {0}
    for scanner0 in scanners:
        for scanner1 in scanners:
            if scanner1['id'] not in added and scanner0['id'] != scanner1['id']:
                distances0 = scanner0['distances']
                distances1 = scanner1['distances']
                tentative = set()
                for distance in distances1:
                    if distance in distances0:
                        tentative.add(distance)

                if len(tentative) >= nbr_required:
                    found = find_factors(scanner0, scanner1, tentative, distances0,
                                    distances1, nbr_required)


                    if found:
                        continue

    exit()
    # chosen = None
    # beacons = set()
    # beacons.update(scanners[0]['beacons'])
    # for scanner in scanners[1:]:
    #     print('id: ', scanner['id'], 'count', len(beacons))
    #     if 0 in scanner['rot_indices']:
    #         rot_index = scanner['rot_indices'][0]
    #         for beacon in scanner['beacons']:
    #             beacons.add(rotate(beacon)[rot_index])
    #     else:
    #         for other_index in scanner['rot_indices']:
    #             other_scanner = scanners[other_index]
    #             if 0 in other_scanner['rot_indices']:
    #                 rot_index0 = scanner['rot_indices'][other_scanner['id']]
    #                 rot_index1 = other_scanner['rot_indices'][0]
    #                 print(rot_index0, rot_index1)
    #                 for beacon in scanner['beacons']:
    #                     rotated = rotate(beacon)[rot_index0]
    #                     rotated = rotate(rotated)[rot_index1]
    #                     beacons.add(rotated)
    #                 break

    pp.pprint(sorted(beacons))
    return len(beacons)


# pp.pprint(len(rotate((-1, -1, 1))))
# pp.pprint(len(rotate((5, 6, 4))))
#print(part1('mini.txt', 3))
print(part1('test.txt', 12))

# result1 = part1("input.txt")
# assert result1 == 4184
# print("Part 1: {}".format(result1))

# assert part2("test6.txt") == 3993
# result2 = part2("input.txt")
# assert result2 == 4731
# print("Part 2: {}".format(result2))
