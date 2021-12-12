from collections import defaultdict, deque

def get_input(filename):
    lines = []
    neighs = defaultdict(lambda: set())
    with open(filename, "r") as file:
        lines = file.readlines()
    for line in lines:
        split = [s.strip() for s in line.split("-")]
        neighs[split[0]].add(split[1])
        neighs[split[1]].add(split[0])
    return neighs

def can_visit(node_from, name_to):
    if name_to.isupper():
        return True

    node = node_from
    while node != None:
        if node["name"] == name_to:
            return False
        node = node["prev"]
    return True

def print_path(node):
    stack = deque()
    while node["prev"] != None:
        stack.append(node["name"])
        node = node["prev"]
    stack.append("start")
    while len(stack) > 0:
        node = stack.pop()
        print(node, end=",")
    print()

def part1(filename):
    neighs = get_input(filename)

    stack = deque()
    stack.append({"name": "start", "prev": None})
    total = 0

    while len(stack) > 0:
        node = stack.pop()

        if node["name"] == "end":
            total += 1

        for neigh in neighs[node["name"]]:
            if can_visit(node, neigh):
                stack.append({"name": neigh, "prev": node})

    return total

def can_visit2(nbr_visits, has_two, node, name_to):
    if name_to.isupper():
        return True

    return has_two == None or nbr_visits[name_to] < 2

def part2(filename):
    neighs = get_input(filename)

    stack = deque()
    stack.append({"name": "start", "prev": None})
    nbr_visits = defaultdict(lambda: 0)
    has_two = None
    total = 0

    while len(stack) > 0:
        node = stack.pop()

        name = node["name"]
        if "unvisit" in node:
            nbr_visits[name] -= 1
            if has_two == name:
                has_two = None
        else:
            if node["name"] == "end":
                total += 1
            else:
                if name.islower():
                    if nbr_visits[name] == 1:
                        if has_two == None:
                            has_two = name
                        else:
                            continue
                    nbr_visits[name] += 1
                    stack.append({"unvisit": True, "name": name})

                for neigh in neighs[name]:
                    if neigh != "start" and can_visit2(nbr_visits, has_two, node, neigh):
                        stack.append({"name": neigh, "prev": node})

    return total

assert part1("test1.txt") == 10
assert part1("test2.txt") == 19
assert part1("test3.txt") == 226
result1 = part1("input.txt")
assert result1 == 3510
print("Part 1: {}".format(result1))
print("")

assert part2("test1.txt") == 36
assert part2("test2.txt") == 103
assert part2("test3.txt") == 3509
result2 = part2("input.txt")
assert result2 == 122880
print("Part 2: {}".format(result2))
