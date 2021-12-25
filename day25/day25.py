from collections import defaultdict
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    rights = defaultdict(lambda: defaultdict(lambda: '.'))
    downs = defaultdict(lambda: defaultdict(lambda: '.'))

    for i in range(0, len(lines)):
        for j in range(0, len(lines[0])):
            if lines[i][j] == 'v':
                downs[i][j] = 'v'
            elif lines[i][j] == '>':
                rights[i][j] = '>'

    return rights, downs, len(lines), len(lines[0])

def print_state(rights, downs, ywidth, xwidth):
    for i in range(0, ywidth):
        for j in range(0, xwidth):
            if rights[i][j] != '.':
                print('>', end='')
            else:
                print(downs[i][j], end='')
        print()

def part1(filename):
    rights, downs, ywidth, xwidth = get_input(filename)
    moved = True
    steps = 0
    while moved:
        moved = False
        next_rights = defaultdict(lambda: defaultdict(lambda: '.'))
        next_downs = defaultdict(lambda: defaultdict(lambda: '.'))

        for i in range(0, ywidth):
            for j in range(0, xwidth):
                if rights[i][j] != '.':
                    if rights[i][(j+1) % xwidth] == '.' and downs[i][(j+1) % xwidth] == '.':
                        moved = True
                        next_rights[i][(j+1) % xwidth] = '>'
                    else:
                        next_rights[i][j] = '>'
        rights = next_rights
        for i in range(0, ywidth):
            for j in range(0, xwidth):
                if downs[i][j] != '.':
                    if rights[(i+1) % ywidth][j] == '.' and downs[(i+1) % ywidth][j] == '.':
                        moved = True
                        next_downs[(i+1) % ywidth][j] = 'v'
                    else:
                        next_downs[i][j] = 'v'
        downs = next_downs
        steps += 1
    return steps

print(part1("test.txt"))
print(part1("input.txt"))
