
# 12
# 0001
# 0011
# 0100
# 101
# 111

lines = []
with open('input.txt', 'r') as file:
    lines = [x.strip() for x in file.readlines()]

n = len(lines)

counts = [0,0,0,0,0,0,0,0,0,0,0,0]
for line in lines:
    i = 0
    for c in line:
        if c == '1':
            counts[i] += 1
        i += 1

def most_common_bits(nbrs):
    n = len(nbrs)
    counts = [0,0,0,0,0,0,0,0,0,0,0,0]

    for line in nbrs:
        i = 0
        for c in line:
            if c == '1':
                counts[i] += 1
            i += 1
    return counts

nbrs = lines
i = 0
while len(nbrs) > 1 and i < len(lines[0]):

    temp_0 = []

    counts = most_common_bits(nbrs)
    if counts[i] >= len(nbrs) / 2:
        most_common = '1'
    else:
        most_common = '0'


    for nbr in nbrs:
        if nbr[i] == most_common:
            temp_0.append(nbr)

    nbrs = temp_0
    i += 1

oxygen = int(nbrs[0], 2)

nbrs = lines
i = 0
while len(nbrs) > 1 and i < len(lines[0]):

    temp_0 = []

    counts = most_common_bits(nbrs)
    if counts[i] >= len(nbrs) / 2:
        most_common = '1'
    else:
        most_common = '0'


    for nbr in nbrs:
        if nbr[i] != most_common:
            temp_0.append(nbr)

    nbrs = temp_0
    i += 1

co2 = int(nbrs[0], 2)
print("Part 2")
print(oxygen * co2)
