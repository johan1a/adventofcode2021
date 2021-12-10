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
        print(line)
        for c in line:
            if c in openers:
                stack.append(c)
            elif len(stack) == 0:
                print('Got ' + c + ', expected opener')
                break
            elif c == matching[stack[-1]]:
                stack.pop()
            else:
                print('Expected ' + matching[stack[-1]] + ' but got ' + c)
                total += values[c]
                break

    print('Part 1 for {}: {}'.format(filename, total))

part1('input.txt')
