
def get_lines(filename):
    input_lines = []
    with open(filename, 'r') as file:
        input_lines = [l.strip() for l in file.readlines()]

    lines = []
    for line in input_lines:
        split = line.split(' -> ')
        src = [int(n) for n in split[0].split(',')]
        dest = [int(n) for n in split[1].split(',')]
        lines.append({'src': src, 'dest': dest})
    return lines

def non_diagonal(line):
    return line['src'][0] == line['dest'][0] or line['src'][1] == line['dest'][1]

def part1(file):
    nondiagonal_lines = [l for l in get_lines(file) if non_diagonal(l)]
    marks = {}
    for line in nondiagonal_lines:
        x0,y0 = line['src']
        x1,y1 = line['dest']

        if x0 < x1:
            xstart = x0
            xend = x1
        else:
            xstart = x1
            xend = x0
        if y0 < y1:
            ystart = y0
            yend = y1
        else:
            ystart = y1
            yend = y0

        x = xstart
        while x <= xend:
            y = ystart
            while y <= yend:
                if (x,y) in marks:
                    marks[(x,y)] += 1
                else:
                    marks[(x,y)] = 1
                y += 1
            x += 1

    points = 0
    for coord in marks:
        if marks[coord] > 1:
            points += 1
    print("Part 1 for {}:".format(file))
    print(points)

part1('test.txt')
part1('input.txt')
