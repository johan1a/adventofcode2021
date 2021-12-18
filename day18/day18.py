import math, random


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]
    return lines


def numeric(node):
    return 'val' in node


def get_id():
    return random.randrange(0, 1000000)


def parse(line, pos=0):
    if line[pos] == "[":
        node = {'parent': None, 'id': get_id()}
        left, pos = parse(line, pos + 1)
        node['left'] = left
        if not numeric(left):
            left['parent'] = node

        if line[pos] == ',':
            pos += 1
        else:
            print("parse error")
            exit(1)

        right, pos = parse(line, pos)
        node['right'] = right
        if not numeric(right):
            right['parent'] = node

        if line[pos] == ']':
            pos += 1
        else:
            print("parse error")
            exit(1)

        return node, pos
    else:
        chars = []
        while line[pos] >= '0' and line[pos] <= '9':
            chars += line[pos]
            pos += 1
        return {'val': int("".join(chars))}, pos


def add_to_left(node, val):
    parent = node['parent']
    changed = False
    while parent != None and not numeric(
            parent['left']) and parent['left']['id'] == node['id']:
        node = parent
        parent = parent['parent']
    if parent != None:
        node = parent
        if numeric(node['left']):
            node['left']['val'] += val
        else:
            node = parent['left']
            while not numeric(node['right']):
                node = node['right']
            node['right']['val'] += val


def add_to_right(node, val):
    parent = node['parent']
    while parent != None and not numeric(
            parent['right']) and parent['right']['id'] == node['id']:
        node = parent
        parent = parent['parent']
    if parent != None:
        node = parent
        if numeric(node['right']):
            node['right']['val'] += val
        else:
            node = parent['right']
            while not numeric(node['left']):
                node = node['left']
            node['left']['val'] += val


def to_string(node):
    if numeric(node):
        return str(node['val'])
    else:
        return "[" + to_string(node['left']) + "," + to_string(
            node['right']) + "]"


def print_tree(node):
    print(to_string(node))


def explode(node, depth=0):
    if numeric(node):
        return node, False

    left = node['left']

    node['left'], changed_left = explode(left, depth + 1)
    if changed_left:
        return node, True

    left = node['left']
    right = node['right']
    if depth > 3 and numeric(left) and numeric(right):

        add_to_left(node, left['val'])

        add_to_right(node, right['val'])
        return {'val': 0}, True

    node['right'], changed_right = explode(right, depth + 1)
    return node, changed_right


def split(node):
    if numeric(node):
        return node, False

    left = node['left']
    if numeric(left) and left['val'] >= 10:
        node['left'] = {
            'left': {
                'val': left['val'] // 2
            },
            'right': {
                'val': (math.ceil(left['val'] / 2))
            },
            'parent': node,
            'id': get_id()
        }
        return node, True
    else:
        node['left'], changed_left = split(node['left'])
        if changed_left:
            return node, True

    right = node['right']
    if numeric(right) and right['val'] >= 10:
        node['right'] = {
            'left': {
                'val': right['val'] // 2
            },
            'right': {
                'val': (math.ceil(right['val'] / 2))
            },
            'parent': node,
            'id': get_id()
        }
        return node, True
    else:
        node['right'], changed_right = split(node['right'])
        if changed_right:
            return node, True

    return node, False


def magnitude(node):
    if numeric(node):
        return node['val']

    return 3 * magnitude(node['left']) + 2 * magnitude(node['right'])


def expand(root):
    changed = True
    while changed:
        _, changed = explode(root)
        if not changed:
            _, changed = split(root)
    return root


def add(numbers):
    root = None
    for number in numbers:
        new, _ = parse(number)
        if root == None:
            root = new
            root['parent'] = None
        else:
            root = {'left': root, 'right': new, 'parent': None, 'id': get_id()}
            root['left']['parent'] = root
            root['right']['parent'] = root

        expand(root)

    return magnitude(root)


def part1(filename):
    numbers = get_input(filename)

    return add(numbers)


def part2(filename):
    numbers = get_input(filename)

    highest = 0

    for i in range(0, len(numbers)):
        for j in range(0, len(numbers)):
            if i == j:
                continue
            val = add([numbers[i], numbers[j]])
            highest = max(highest, val)

    return highest


assert part1("test0.txt") == 445
assert part1("test1.txt") == 791
assert part1("test2.txt") == 1137
assert part1("test4.txt") == 1384
assert to_string(expand(parse("[[[[[9,8],1],2],3],4]")[0])) == "[[[[0,9],2],3],4]"
assert to_string(expand(parse("[7,[6,[5,[4,[3,2]]]]]")[0])) == "[7,[6,[5,[7,0]]]]"
assert to_string(expand(parse("[[6,[5,[4,[3,2]]]],1]")[0])) == "[[6,[5,[7,0]]],3]"
assert to_string(expand(parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")[0])) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

assert part1("test3.txt") == 3488
assert part1("test5.txt") == 4140

result1 = part1("input.txt")
assert result1 == 4184
print("Part 1: {}".format(result1))

assert part2("test6.txt") == 3993
result2 = part2("input.txt")
assert result2 == 4731
print("Part 2: {}".format(result2))
