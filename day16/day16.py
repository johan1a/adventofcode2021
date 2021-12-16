from collections import defaultdict, deque
from queue import PriorityQueue
import sys, math


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

literal = ["1", "0", "0"]

length_type_bits = ["0"]
length_type_packets = ["1"]

def parse_packets(chars, pos):
    total = 0
    max_bit_length = len(chars * 4)
    minimum_packet_length = 7
    sub_packet = False
    i = 0
    print("max_bit_length", max_bit_length)
    while pos < max_bit_length - minimum_packet_length:
        print("\nstart pos", pos)
        version, pos = get_bits(chars, pos, 3)

        total += int(str("".join(version)), 2)
        print("total", total)
        type_id, pos = get_bits(chars, pos, 3)
        if type_id == literal:
            print("literal", pos)
#00111000000000000110111101000101001010010001001000000000
            number, pos = get_bits(chars, pos, 5)
            while number[0] == "1":
                number, pos = get_bits(chars, pos, 5)
            if not sub_packet:
                break
        else:
            print("operator", pos)
            length_type, pos = get_bits(chars, pos, 1)
            sub_packet = True
            if length_type == length_type_bits:
                nbr_bits, pos = get_bits(chars, pos, 15)
            else:
                nbr_packets, pos = get_bits(chars, pos, 11)

    print(pos)
    return total

def part1(filename):
    chars = get_input(filename)
    pos = 0
    total = parse_packets(chars, pos)
    return total

assert part1("test.txt") == 6
assert part1("test1.txt") == 9
assert part1("test2.txt") == 16
assert part1("test3.txt") == 12
assert part1("test4.txt") == 23
assert part1("test5.txt") == 31
part1("input.txt")

#0,23,34
# assert part1("test.txt") == 40
# result1 = part1("input.txt")
# assert result1 == 714
# print("Part 1: {}".format(result1))
# print("")

# assert part2("test.txt") == 315
# result2 = part2("input.txt")
# assert result2 == 2948
# print("Part 2: {}".format(result2))
