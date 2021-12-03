
# 12
# 0001
# 0011
# 0100
# 101
# 111

lines = []
with open('input.txt', 'r') as file:
    lines = file.readlines()

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
while len(nbrs) > 1:

    temp_0 = []

    counts = most_common_bits(nbrs)
    for nbr in nbrs:
        i = 0
        while i < len(nbr):
            if counts[i] >= n / 2:
                most_common = 1
            else:
                most_common = 0

            if nbr[i] == most_common:
                temp_0 += nbr

            i += 1
    nbrs = temp_0

temp_1 = []
print(temp_0)
# print("Part 1")
# print(gamma_dec * epsilon_dec)
