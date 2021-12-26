from collections import defaultdict
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)


def parse(line):
    if "inp" in line:
        return {'op': 'inp', 'a': line.replace("inp ", "")}
    elif "mul" in line:
        split = line.replace('mul ', '').split()
        return {'op': 'mul', 'a': split[0], 'b': split[1]}
    elif "add" in line:
        split = line.replace('add ', '').split()
        return {'op': 'add', 'a': split[0], 'b': split[1]}
    elif "mod" in line:
        split = line.replace('mod ', '').split()
        return {'op': 'mod', 'a': split[0], 'b': split[1]}
    elif "div" in line:
        split = line.replace('div ', '').split()
        return {'op': 'div', 'a': split[0], 'b': split[1]}
    elif "eql" in line:
        split = line.replace('eql ', '').split()
        return {'op': 'eql', 'a': split[0], 'b': split[1]}


def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    instructions = []

    for line in lines:
        instructions.append(parse(line))

    return instructions


def register(a):
    if a in ['x', 'y', 'z', 'w']:
        return True
    return False


def execute(registers, cmd, input_data):
    op = cmd['op']
    if op == 'inp':
        registers[cmd['a']] = int(input_data.pop())
    elif op == 'add':
        b = cmd['b']
        if register(b):
            bval = registers[b]
        else:
            bval = int(b)
        registers[cmd['a']] = registers[cmd['a']] + bval
    elif op == 'mul':
        b = cmd['b']
        if register(b):
            bval = registers[b]
        else:
            bval = int(b)
        registers[cmd['a']] = registers[cmd['a']] * bval
    elif op == 'div':
        b = cmd['b']
        if register(b):
            bval = registers[b]
        else:
            bval = int(b)
        if bval == 0:
            return registers, False
        registers[cmd['a']] = registers[cmd['a']] // bval
    elif op == 'mod':
        b = cmd['b']
        if register(b):
            bval = registers[b]
        else:
            bval = int(b)
        if bval <= 0 or registers[cmd['a']] < 0:
            return registers, False
        registers[cmd['a']] = registers[cmd['a']] % bval
    elif op == 'eql':
        b = cmd['b']
        if register(b):
            bval = registers[b]
        else:
            bval = int(b)
        if registers[cmd['a']] == bval:
            registers[cmd['a']] = 1
        else:
            registers[cmd['a']] = 0
    if registers[cmd['a']] < 0:
        return False
    else:
        return True


def run_file(filename, input_raw):
    cmds = get_input(filename)
    registers = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
    return run(input_raw, cmds, registers)


def run(input_raw, cmds, registers):
    input_data = [int(x) for x in str(input_raw)]
    input_data.reverse()
    for cmd in cmds:
        result = execute(registers, cmd, input_data)
        if not result:
            return registers, False
    return registers, True


cache = {}


def tokenize(ci0, regs, i):
    return (ci0, i, regs['w'], regs['x'], regs['y'], regs['z'])


def find_digits(chunks, ci0, input_regs, istart, iend, idiff):
    chunk = chunks[ci0]
    i = istart
    while i != iend:
        token = tokenize(ci0, input_regs, i)
        digits = None
        ok = False
        if token in cache:
            return cache[token]
        else:
            input_copy = {
                'x': input_regs['x'],
                'y': input_regs['y'],
                'z': input_regs['z'],
                'w': input_regs['w'],
            }
            out_regs, ok = run(str(i), chunk, input_copy)

        if ok and ci0 == len(chunks) - 1 and out_regs['z'] == 0:
            cache[token] = str(i)
            return str(i)

        elif ok and ci0 < len(chunks) - 1:
            digits = find_digits(chunks, ci0 + 1, out_regs, istart, iend,
                                 idiff)
            if digits != None:
                cache[token] = str(i) + digits
                return str(i) + digits
            else:
                cache[token] = None
        elif not ok:
            cache[token] = None

        i += idiff
    return None


def search(filename, istart, iend, idiff):
    cmds = get_input(filename)
    chunks = []
    chunk = [cmds[0]]
    i = 1
    while i < len(cmds):
        if cmds[i]['op'] == 'inp':
            chunks.append(chunk)
            chunk = []
        chunk.append(cmds[i])
        i += 1
    chunks.append(chunk)

    return find_digits(chunks, 0, {
        'x': 0,
        'y': 0,
        'z': 0,
        'w': 0
    }, istart, iend, idiff)


def part1(filename):
    return search(filename, 9, 1, -1)


def part2(filename):
    return search(filename, 1, 9, 1)


assert run_file('test0.txt', 5)[0]['x'] == -5
assert run_file('test1.txt', 13)[0]['z'] == 1
assert run_file('test1.txt', 23)[0]['z'] == 0
assert run_file('test1.txt', 43)[0]['z'] == 0
assert run_file('test2.txt', 7) == ({'x': 1, 'y': 1, 'z': 1, 'w': 0}, True)

# Takes ~100 mins
result1 = part1("input.txt")
print("Part 1: {}".format(result1))

result2 = part2("input.txt")
print("Part 2: {}".format(result2))
