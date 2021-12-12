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

def is_lower(s):
    lower = [c >= 'a' and c <= 'z' for c in s]
    for l in lower:
        if not l:
            return False
    return True

def can_visit(node_from, name_to):
    #print("Can visit {} -> {}".format(node_from["name"], name_to))
    if not is_lower(name_to):
        #print("True")
        return True

    node = node_from
    while node != None:
        if node["name"] == name_to:
            #print("False")
            return False
        node = node["prev"]
    #print("True")
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

    visited = set()
    stack = deque()
    stack.append({"name": "start", "prev": None})
    total = 0

    while len(stack) > 0:
        node = stack.pop()

        #print(node)
        if node["name"] == "end":
            total += 1
            #print_path(node)

        for neigh in neighs[node["name"]]:
            if can_visit(node, neigh):
                if neigh == "start":
                    print(can_visit(node, neigh))
              #  print("Adding neigh: " + neigh)
                stack.append({"name": neigh, "prev": node})

    print("Part 1 for {}: {}".format(filename, total))

part1("test1.txt")
part1("test2.txt")
part1("test3.txt")
part1("input.txt")
