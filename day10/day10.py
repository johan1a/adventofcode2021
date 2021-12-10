from collections import defaultdict, deque

def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
    return lines

matching = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
        }

values = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
        }

openers = set(['(', '[', '{', '<'])

def part1(filename):
    lines = get_input(filename)

    stack = deque()
    total = 0
    for line in lines:
        for c in line:
            if c in openers:
                stack.append(c)
            elif len(stack) == 0:
                print('Got ' + c + ', expected opener')
                break
            elif c == matching[stack[-1]]:
                stack.pop()
            else:
                total += values[c]
                break

    print('Part 1 for {}: {}'.format(filename, total))


closer_scores = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
        }

def part2(filename):
    lines = get_input(filename)

    scores = []
    for line in lines:
        stack = deque()
        corrupt = False
        for c in line:
            if c in openers:
                stack.append(c)
            elif len(stack) == 0:
                corrupt = True
                break
            elif c == matching[stack[-1]]:
                stack.pop()
            else:
                corrupt = True
                break

        if not corrupt:
            score = 0
            while len(stack) > 0:
                score *= 5
                c = stack.pop()
                score += closer_scores[c]
            scores.append(score)
    scores = sorted(scores)
    winner = scores[int(len(scores) / 2)]
    print('Part 2 for {}: {}'.format(filename, winner))

part1('test.txt')
part1('input.txt')
print('')

part2('test.txt')
part2('input.txt')
