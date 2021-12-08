from collections import defaultdict

def get_input(filename):

    lines = []
    with open(filename, 'r') as file:
        lines = [l.split('|') for l in file.readlines()]

    return lines

def part1(filename):
    lines = get_input(filename)
    total = 0
    for line in lines:
        outputs = line[1].split()
        for output in outputs:
            if len(output.strip()) in {2,3,4,7}:
                total += 1
    print('Part 1 for {}: {}'.format(filename, total))

part1('test.txt')
part1('input.txt')
