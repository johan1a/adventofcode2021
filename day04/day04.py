

lines = []
with open('input.txt', 'r') as file:
    lines = [l.strip() for l in file.readlines()]

def create_boards(lines):
    i = 2 # line of first board
    boards = []
    while i < len(lines):
        board = { 'rows': [], 'marks': [], 'has_won': False}
        while i < len(lines) and lines[i] != '':
            line = lines[i]
            row = [int(n.strip()) for n in line.split()]
            board['rows'].append(row)
            board['marks'].append([False, False, False, False, False])

            i += 1
        boards.append(board)
        i += 1
    return boards

def update(board, nbr):
    marks = board['marks']
    rows = board['rows']
    i = 0
    while i < len(rows):
        j = 0
        row = rows[i]
        while j < len(row):
            if nbr == row[j]:
                marks[i][j] = True
            j += 1
        i += 1

def has_won(board):
    marks = board['marks']
    rows = board['rows']
    if [True, True, True, True, True] in marks:
        return True
    i = 0
    while i < len(rows):
        j = 0
        allChecked = True
        while j < len(rows[0]):
            if marks[j][i] == False:
                allChecked = False
            j += 1
        if allChecked:
            return True
        i += 1
    return False

def print_board(board):
    print(board['has_won'])
    i = 0
    rows = board['rows']
    while i < len(rows):
        print(rows[i])
        i += 1
    i = 0
    marks = board['marks']
    while i < len(marks):
        print(marks[i])
        i += 1

def calculate_score(board, last_nbr):
    marks = board['marks']
    rows = board['rows']
    total = 0
    i = 0
    while i < len(rows):
        j = 0
        allChecked = True
        while j < len(rows[0]):
            if marks[i][j] == False:
                total += rows[i][j]
            j += 1
        i += 1
    return total * last_nbr


nbrs = [int(n) for n in lines[0].split(",")]

def part_one():
    boards = create_boards(lines)

    i = 0
    for nbr in nbrs:
        for board in boards:
            update(board, nbr)
            if has_won(board):
                print("Part 1:")
                print(calculate_score(board, nbr))
                return
        i += 1

def part_two():
    boards = create_boards(lines)

    nbr_won = 0
    i = 0
    for nbr in nbrs:
        for board in boards:
            update(board, nbr)
            if (not board['has_won']) and has_won(board):
                board['has_won'] = True
                nbr_won += 1
                if nbr_won == len(boards):
                    print("Part 2:")
                    print(calculate_score(board, nbr))
                    return
        i += 1

part_one()
part_two()
