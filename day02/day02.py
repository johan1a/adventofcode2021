
lines = []
with open('input.txt', 'r') as file:
    lines = file.readlines()

x = 0
y = 0
for line in lines:
    if "down" in line:
        y += int(line.split("down ")[1])
    if "forward" in line:
        x += int(line.split("forward ")[1])
    if "up" in line:
        y -= int(line.split("up ")[1])

print("Part 1:")
print(x * y)
