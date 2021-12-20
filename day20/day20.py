from collections import defaultdict

def get_input(filename):
    lines = []
    with open(filename, "r") as file:
        lines = [l.strip() for l in file.readlines()]

    image = defaultdict(lambda: defaultdict(lambda: '.'))
    for i in range(2, len(lines)):
        for j in range(0, len(lines[i])):
            image[i - 2][j] = lines[i][j]

    return lines[0], image, 0, 0, len(image[2]) - 1, len(image) - 1


def pixel_to_binary(char):
    if char == '.':
        return '0'
    else:
        return '1'


def get_image_number(input_image, x0, y0):
    digits = []
    for y in range(y0 - 1, y0 + 2):
        for x in range(x0 - 1, x0 + 2):
            digits.append(input_image[y][x])
    return int("".join([pixel_to_binary(x) for x in digits]), 2)


border = 20


def enhance(enhancement, input_image, xmin, ymin, xmax, ymax):
    default = enhancement[get_image_number(input_image, -100000, -100000)]

    output_image = defaultdict(lambda: defaultdict(lambda: default))

    next_xmin = xmin
    next_ymin = ymin
    next_xmax = xmax
    next_ymax = ymax

    for y in range(ymin - border, ymax + 1 + border):
        for x in range(xmin - border, xmax + 1 + border):
            num = get_image_number(input_image, x, y)
            output_pixel = enhancement[num]
            output_image[y][x] = output_pixel

            next_xmin = min(next_xmin, x)
            next_ymin = min(next_ymin, y)
            next_xmax = max(next_xmax, x)
            next_ymax = max(next_ymax, y)

    return output_image, next_xmin - 3, next_ymin - 3, next_xmax + 3, next_ymax + 3


def print_image(output_image, xmin, ymin, xmax, ymax):
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            print(output_image[y][x], end="")
        print()
    print()


def run(filename, n):
    enhancement, input_image, xmin, ymin, xmax, ymax = get_input(filename)
    image = input_image
    for i in range(0, n):
        image, xmin, ymin, xmax, ymax = enhance(enhancement, image, xmin, ymin,
                                                xmax, ymax)
        xmin += border
        ymin += border
        xmax -= border
        ymax -= border

    total = 0
    for row in image:
        for col in image:
            if image[row][col] == '#':
                total += 1

    return total


def part1(filename):
    return run(filename, 2)


def part2(filename):
    return run(filename, 50)


assert part1('test.txt') == 35
result1 = part1("input.txt")
assert result1 == 5419
print("Part 1: {}".format(result1))

assert part2('test.txt') == 3351
result2 = part2("input.txt")
assert result2 == 17325
print("Part 2: {}".format(result2))
