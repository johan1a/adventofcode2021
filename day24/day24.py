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
    if a in ['x','y', 'z', 'w']:
        return True
    return False

def execute(registers, cmd, input_data, interactive=False):
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
        if bval <=0 or registers[cmd['a']] < 0:
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
    # print(input_data)
    # pp.pprint(registers)
    if interactive and op == 'inp':
        print(cmd)
        pp.pprint(registers)
        sys.stdin.readline()
    if registers[cmd['a']] < 0:
        return False
    else:
        return True


def run(filename, input_raw, interactive=False, cmds=None):
    if cmds == None:
        cmds = get_input(filename)
    registers = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
    input_data = [int(x) for x in str(input_raw)]
    input_data.reverse()
    for cmd in cmds:
        result = execute(registers, cmd, input_data, interactive)
        if not result:
            return registers, False
    return registers, True


def part1(filename, interactive=False):
    cmds = get_input(filename)
    i = 99999916280000
    while i >= 0:
        if i % 10000 == 0:
            print(i)
        if '0' not in str(i):
            regs, result = run(filename, i, interactive, cmds)
            if result and regs['z'] == 0:
                return i
        i = i - 1
    return -1


assert run('test0.txt', 5)[0]['x'] == -5
assert run('test1.txt', 13)[0]['z'] == 1
assert run('test1.txt', 23)[0]['z'] == 0
assert run('test1.txt', 43)[0]['z'] == 0
assert run('test2.txt', 7) == ({'x': 1, 'y': 1, 'z': 1, 'w': 0}, True)

#print(part1("input.txt"))
print(run("input.txt", 15199999999999, True))
