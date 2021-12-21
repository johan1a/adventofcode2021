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
            if scores[i] >= 1000:
                return d * scores[(i + 1) % len(players)]


max_score = 21

wins = {}


def tokenize(positions, scores, next_player):
    return (positions[0], positions[1], scores[0], scores[1], next_player)


def play(positions, scores, current_player):
    token = tokenize(positions, scores, current_player)
    if token in wins:
        return wins[token]
    if scores[0] >= max_score:
        return [1, 0]
    elif scores[1] >= max_score:
        return [0, 1]

    steps = [
        [1, 3],
        [3, 4],
        [6, 5],
        [7, 6],
        [6, 7],
        [3, 8],
        [1, 9],
    ]
    round_wins = [0,0]
    for factor, step in steps:
        original_pos = positions[current_player]
        new_pos = (original_pos + step) % 10
        positions[current_player] = new_pos
        scores[current_player] += new_pos + 1
        next_player = (current_player + 1) % 2

        result = play(positions, scores, next_player)
        round_wins[0] += factor * result[0]
        round_wins[1] += factor * result[1]

        positions[current_player] = original_pos
        scores[current_player] -= (new_pos + 1)
    wins[token] = round_wins
    return round_wins



def part2(filename):
    wins = {}
    positions = get_input(filename)
    result = play(positions, [0, 0], 0)
    print(wins, result)
    return max(result)


assert part1("test.txt") == 739785
assert part1("input.txt") == 1073709

print(part2("test.txt"))
print(part2("input.txt"))

# result1 = part1("input.txt")
# assert result1 == 5419
# print("Part 1: {}".format(result1))

# assert part2('test.txt') == 3351
# result2 = part2("input.txt")
# assert result2 == 17325
# print("Part 2: {}".format(result2))
