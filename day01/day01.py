
lines = []
with open('input.txt', 'r') as file:
    lines = [int(x) for x in file.readlines()]

increases = 0
i = 1
while i < len(lines):
    n = lines[i]
    increase = lines[i] - lines[i-1]
    if (increase > 0):
        increases+=1
    i += 1

print("Part 1:")
print(increases)

increases = 0
i = 1
while i < len(lines) - 2:
    a = lines[i - 1] + lines[i] + lines[i + 1]
    b = lines[i] + lines[i+1] + lines[i + 2]
    increase = b - a
    if (increase > 0):
        increases+=1
    i += 1

print("Part 2:")
print(increases)
