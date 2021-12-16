from collections import defaultdict, deque
from queue import PriorityQueue
import sys
import math


def get_input(filename):
    line = ""
    with open(filename, "r") as file:
        line = file.readline().strip()
    return line


def get_bits(chars, pos, nbr):
    charpos = pos // 4
    bitpos = pos % 4
    result = []
    while len(result) < nbr and len(result) < nbr:
        char = chars[charpos]
        bits = '{:04b}'.format(int(char, 16))
        while len(result) < nbr and bitpos < 4:
            result.append(bits[bitpos])
            bitpos += 1
        if bitpos == 4:
            bitpos = 0
            charpos += 1
    assert len(result) == nbr
    return result, charpos * 4 + bitpos


type_sum = "sum"
type_product = "product"
type_min = "min"
type_max = "max"
type_literal = ["1", "0", "0"]
type_gt = "gt"
type_lt = "lt"
type_eq = "eq"

opcodes = {
    ("0", "0", "0"): "sum",
    ("0", "0", "1"): "product",
    ("0", "1", "0"): "min",
    ("0", "1", "1"): "max",
    ("1", "0", "1"): "gt",
    ("1", "1", "0"): "lt",
    ("1", "1", "1"): "eq"
}

nbr_args = {
    type_sum: -1,
    type_product: -1,
    type_min: -1,
    type_max: -1,
    type_gt: 2,
    type_lt: 2,
    type_eq: 2
}

length_type_bits = ["0"]
length_type_packets = ["1"]


def parse_packets(chars, pos):
    version_total = 0
    total = 0
    max_bit_length = len(chars * 4)
    minimum_packet_length = 7
    sub_packet = False
    i = 0

    op_type = None
    read_bits = 0
    read_packets = 0
    packets_to_read = -1
    bits_to_read = -1
    values = []
    stack = deque()

    while pos < max_bit_length - minimum_packet_length:
        start_pos = pos
        version, pos = get_bits(chars, pos, 3)

        version_total += int(str("".join(version)), 2)
        type_id, pos = get_bits(chars, pos, 3)
        if type_id == type_literal:
            number, pos = get_bits(chars, pos, 5)
            stack.append(int(str("".join(number)), 2))
            while number[0] == "1":
                number, pos = get_bits(chars, pos, 5)
                stack.append(int(str("".join(number)), 2))
            if not sub_packet:
                break
            read_packets += 1
            read_bits += pos - start_pos
        else:
            stack.append(opcodes[tuple(type_id)])
            length_type, pos = get_bits(chars, pos, 1)
            sub_packet = True
            if length_type == length_type_bits:
                nbr_bits, pos = get_bits(chars, pos, 15)
                bits_to_read = int(str("".join(nbr_bits)), 2)
            elif length_type == length_type_packets:
                nbr_packets, pos = get_bits(chars, pos, 11)
                packets_to_read = int(str("".join(nbr_packets)), 2)
            else:
                print("length type error")
                exit(1)

    return version_total


def calculate(element):
    if type(element) == type(1):
        return element

    op_type = element['op']
    values = [calculate(x) for x in element['vals']]
    if len(values) == 0:
        print("calc error", element)
        exit(1)

    if op_type == type_sum:
        return sum(values)
    elif op_type == type_product:
        product = 1
        for value in values:
            product *= value
        return product
    elif op_type == type_min:
        return min(values)
    elif op_type == type_max:
        return max(values)
    elif op_type == type_gt:
        if values[0] > values[1]:
            return 1
        return 0
    elif op_type == type_lt:
        if values[0] < values[1]:
            return 1
        return 0
    elif op_type == type_eq:
        if values[0] == values[1]:
            return 1
        return 0


def should_pop(node, pos):
    if node['length_type'] == 'packets':
        read_packets = len(node['vals'])
        if read_packets == node['nbr_packets']:
            return True
        elif read_packets > node['nbr_packets']:
            print("packets error", read_packets, node['nbr_packets'], node)
            sys.exit(1)
    elif node['length_type'] == 'bits':
        read_bits = pos - node['sub_pos']
        if read_bits == node['nbr_bits']:
            return True
        elif read_bits > node['nbr_bits']:
            print("bits error")
            sys.exit(1)


def parse_packets2(chars, pos):
    max_bit_length = len(chars * 4)
    minimum_packet_length = 7

    op_type = None
    stack = deque()

    while pos < max_bit_length - minimum_packet_length:
        start_pos = pos

        version, pos = get_bits(chars, pos, 3)
        type_id, pos = get_bits(chars, pos, 3)

        if type_id == type_literal:
            number_temp = []
            number_part, pos = get_bits(chars, pos, 5)
            number_temp += number_part[1:]
            while number_part[0] == "1":
                number_part, pos = get_bits(chars, pos, 5)
                number_temp += number_part[1:]
            number = int(str("".join(number_temp)), 2)
            stack[-1]['vals'].append(int(str("".join(number_temp)), 2))
        else:
            node = {
                'op': opcodes[tuple(type_id)],
                'vals': [],
                'start_pos': start_pos,
                'sub_pos': -1,
                'nbr_packets': -1,
                'nbr_bits': -1
            }
            if len(stack) > 0:
                stack[-1]['vals'].append(node)
            stack.append(node)
            length_type, pos = get_bits(chars, pos, 1)
            if length_type == length_type_bits:
                nbr_bits, pos = get_bits(chars, pos, 15)
                stack[-1]['nbr_bits'] = int(str("".join(nbr_bits)), 2)
                stack[-1]['sub_pos'] = pos
                stack[-1]['length_type'] = 'bits'
            else:
                nbr_packets, pos = get_bits(chars, pos, 11)
                stack[-1]['nbr_packets'] = int(str("".join(nbr_packets)), 2)
                stack[-1]['length_type'] = 'packets'

        while len(stack) > 1 and should_pop(stack[-1], pos):
            stack.pop()

    while (len(stack) > 1):
        stack.pop()

    return calculate(stack.pop())


def part1(filename):
    chars = get_input(filename)
    pos = 0
    version_total = parse_packets(chars, pos)
    return version_total


def part2(filename):
    chars = get_input(filename)
    pos = 0
    total = parse_packets2(chars, pos)
    return total


assert part1("test.txt") == 6
assert part1("test1.txt") == 9
assert part1("test2.txt") == 16
assert part1("test3.txt") == 12
assert part1("test4.txt") == 23
assert part1("test5.txt") == 31
result1 = part1("input.txt")
print("Part 1: {}".format(result1))

assert part2("test6.txt") == 3
assert part2("test7.txt") == 54
assert part2("test8.txt") == 7
assert part2("test9.txt") == 9
assert part2("test10.txt") == 1
assert part2("test11.txt") == 0
assert part2("test12.txt") == 0
assert part2("test13.txt") == 1
result2 = part2("input.txt")
print("Part 2: {}".format(result2))
