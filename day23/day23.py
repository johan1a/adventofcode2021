from collections import defaultdict
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()
    positions = []

    rooms = defaultdict(lambda: defaultdict(lambda: None))
    i = 0
    for k in range(2, 4):
        line = lines[k]
        j = 0
        for l in range(3, 10, 2):
            rooms[j][i] = line[l]
            j += 1
        i += 1

    return rooms, [None, None, None, None, None, None, None]


def completed(rooms):
    for i, l in enumerate(['A', 'B', 'C', 'D']):
        for j in range(0, 2):
            if rooms[i][j] != l:
                return False
    return True


# room index to aux index
room_to_aux_paths = {
    0: {
        0: [1, 0],
        1: [1],
        2: [2],
        3: [2, 3],
        4: [2, 3, 4],
        5: [2, 3, 4, 5],
        6: [2, 3, 4, 5, 6],
    },
    1: {
        0: [2, 1, 0],
        1: [2, 1],
        2: [2],
        3: [3],
        4: [3, 4],
        5: [3, 4, 5],
        6: [3, 4, 5, 6],
    },
    2: {
        0: [3, 2, 1, 0],
        1: [3, 2, 1],
        2: [3, 2],
        3: [3],
        4: [4],
        5: [4, 5],
        6: [4, 5, 6],
    },
    3: {
        0: [4, 3, 2, 1, 0],
        1: [4, 3, 2, 1],
        2: [4, 3, 2],
        3: [4, 3],
        4: [4],
        5: [5],
        6: [5, 6],
    }
}

hallway_to_aux_distances = {
    0: {
        0: 2,
        1: 1,
        2: 1,
        3: 3,
        4: 5,
        5: 7,
        6: 8,
    },
    1: {
        0: 4,
        1: 3,
        2: 1,
        3: 1,
        4: 3,
        5: 5,
        6: 6,
    },
    2: {
        0: 6,
        1: 5,
        2: 3,
        3: 1,
        4: 1,
        5: 3,
        6: 4,
    },
    3: {
        0: 8,
        1: 7,
        2: 5,
        3: 3,
        4: 1,
        5: 1,
        6: 2,
    }
}

shell_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

shell_rooms = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}


def room_to_aux_cost(rooms, aux, r0, r1, i):
    shell = rooms[r0][r1]
    shell_cost = shell_costs[shell]
    cost = (r1 + 1) * shell_cost
    cost += shell_cost * hallway_to_aux_distances[r0][i]
    return cost


def aux_to_room_cost(rooms, aux, r0, r1, i):
    shell = aux[i]
    shell_cost = shell_costs[shell]
    cost = (r1 + 1) * shell_cost
    cost += shell_cost * hallway_to_aux_distances[r0][i]
    return cost


def can_move_to_aux(rooms, aux, r0, r1, aux_i):
    shell = rooms[r0][r1]

    if shell_rooms[shell] == r0 and (r1 == 1 or
                                     (r1 == 0 and shell == rooms[r0][1])):
        # in correct position
        return False
    if rooms[r0][r1] == None or aux[aux_i] != None or (r1 == 1 and
                                                       rooms[r0][0] != None):
        return False
    path = room_to_aux_paths[r0][aux_i]
    for i in path:
        if i != aux_i and aux[i] != None:
            return False
    return True


def can_move_to_room(rooms, aux, r0, r1, aux_i):
    shell = aux[aux_i]
    wrong_room = r0 != shell_rooms[shell]
    not_empty = rooms[r0][r1] != None
    in_the_way = (r1 == 1 and rooms[r0][0] != None)
    contains_other_type = (rooms[r0][0] != None and rooms[r0][0] != shell
                           or rooms[r0][1] != None and rooms[r0][1] != shell)
    move_to_first_when_second_empty = r1 == 0 and rooms[r0][1] == None
    if wrong_room or not_empty or in_the_way or contains_other_type or move_to_first_when_second_empty:
        return False

    path = room_to_aux_paths[r0][aux_i]
    for i in path:
        if i != aux_i and aux[i] != None:
            return False
    return True


not_found = 1000000000


def format(shell):
    if shell == None:
        return '.'
    else:
        return shell


def print_rooms(rooms, aux):
    print("############")
    print("#", end="")
    print(format(aux[0]), end="")
    print(format(aux[1]), end="")
    print(".", end="")
    print(format(aux[2]), end="")
    print(".", end="")
    print(format(aux[3]), end="")
    print(".", end="")
    print(format(aux[4]), end="")
    print(".", end="")
    print(format(aux[5]), end="")
    print(format(aux[6]), end="")
    print("#")

    print("###", end='')
    print(format(rooms[0][0]), end="")
    print("#", end="")
    print(format(rooms[1][0]), end="")
    print("#", end="")
    print(format(rooms[2][0]), end="")
    print("#", end="")
    print(format(rooms[3][0]), end="")
    print("###")
    print("  #", end='')
    print(format(rooms[0][1]), end="")
    print("#", end="")
    print(format(rooms[1][1]), end="")
    print("#", end="")
    print(format(rooms[2][1]), end="")
    print("#", end="")
    print(format(rooms[3][1]), end="")
    print("#  ")
    print('  #########')

cache = {}

def tokenize(rooms, aux):
    token = []
    for r0 in range(0,4):
        for r1 in range(0,2):
            token.append(format(rooms[r0][r1]))
    for a in aux:
        token.append(format(a))
    return "".join(token)

def move(rooms, aux):
    token = tokenize(rooms, aux)
    if token in cache:
        return cache[token]
    #print_rooms(rooms, aux)
    if completed(rooms):
        cache[token] = 0
        return 0
#    sys.stdin.readline()
    min_cost = not_found

    for i, shell in enumerate(aux):
        if shell != None:
            for r0 in range(0, 4):
                for r1 in range(0, 2):
                    if can_move_to_room(rooms, aux, r0, r1, i):
                        #print("from aux {} to room {},{}".format(i, r0, r1))
                        move_cost = aux_to_room_cost(rooms, aux, r0, r1, i)
                        rooms[r0][r1] = aux[i]
                        aux[i] = None

                        cost = move(rooms, aux)

                        if cost != not_found:
                            min_cost = min(min_cost, cost + move_cost)

                        aux[i] = rooms[r0][r1]
                        rooms[r0][r1] = None

    for r0 in range(0, 4):
        for r1 in range(0, 2):
            if rooms[r0][r1] != None:
                for ti, aux_shell in enumerate(aux):
                    # if r0 == 3 and r1 == 0:
                    #     print(rooms[r0][r1], ti, 'can move?',
                    #           can_move_to_aux(rooms, aux, r0, r1, ti))
                    #     print_rooms(rooms, aux)
                    if can_move_to_aux(rooms, aux, r0, r1, ti):
                        #print("from room {},{} to aux {}".format(r0, r1, ti))
                        move_cost = room_to_aux_cost(rooms, aux, r0, r1, ti)
                        aux[ti] = rooms[r0][r1]
                        rooms[r0][r1] = None

                        cost = move(rooms, aux)

                        if cost != not_found:
                            min_cost = min(min_cost, cost + move_cost)

                        rooms[r0][r1] = aux[ti]
                        aux[ti] = None
    cache[token] = min_cost
    return min_cost


def part1(filename):
    rooms, aux = get_input(filename)
    return move(rooms, aux)


print(part1("input.txt"))
# result1 = part1("input.txt")
# assert result1 == 653798
# print("Part 1: {}".format(result1))

# assert part2('input_small.txt') == 653798
# assert part2('test13.txt') == 2758514936282235
# result2 = part2('input.txt')
# assert result2 == 1257350313518866
# print("Part 2: {}".format(result2))
