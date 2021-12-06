from collections import defaultdict

def get_initial_nbrs(filename):
    all_nbrs = []
    with open(filename, 'r') as file:
        all_nbrs = [int(n.strip()) for n in file.readline().split(',')]

    nbrs = defaultdict(lambda: 0)
    for nbr in all_nbrs:
        nbrs[nbr] += 1

    return nbrs

def run(file, part_nbr, n):
    nbrs = get_initial_nbrs(file)
    i = 0
    while i < n:
        next_gen = defaultdict(lambda: 0)
        for nbr in nbrs:
            amount = nbrs[nbr]
            if nbr == 0:
                next_gen[6] += amount
                next_gen[8] += amount
            else:
                next_gen[nbr - 1] += amount
        nbrs = next_gen
        i +=1
    total = sum([nbrs[x] for x in nbrs])
    print("Part {} for {}: {}".format(part_nbr, file, total))


def part1(file):
    run(file, 1, 80)

def part2(file):
    run(file, 1, 256)

part1('test.txt')
part1('input.txt')
print('')

part2('test.txt')
part2('input.txt')
