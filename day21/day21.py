from collections import defaultdict


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    positions = []
    for line in lines:
        pos = (int(line.split("starting position: ")[1]) - 1) % 10
        positions.append(pos)
    return positions

def roll_dice(i):
    return (i + 1) % 100 + (i + 2) % 100 + (i + 3) % 100

def part1(filename):
    players = get_input(filename)
    scores = defaultdict(lambda: 0)
    print(players)

    won = False
    d = 0
    while not won:
        for i in range(0, len(players)):
            step = roll_dice(d)
            d += 3
            pos = players[i]
            pos = (pos + step) % 10
            players[i] = pos
            scores[i] += pos + 1
            #print(d, players, scores)
            if scores[i] >= 1000:
                #print(d, scores[(i + 1) % len(players)], scores)
                return d * scores[(i + 1) % len(players)]


print(part1("test.txt"))
print(part1("input.txt"))

# result1 = part1("input.txt")
# assert result1 == 5419
# print("Part 1: {}".format(result1))

# assert part2('test.txt') == 3351
# result2 = part2("input.txt")
# assert result2 == 17325
# print("Part 2: {}".format(result2))
