import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    if not lines or not lines[0]:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    s = lines[0]
    score = 0
    depth = 0
    garbage = 0
    in_garbage = False

    i = 0
    while i < len(s):
        c = s[i]
        if in_garbage:
            if c == '!':
                i += 2
                continue
            if c == '>':
                in_garbage = False
            else:
                garbage += 1
        else:
            if c == '<':
                in_garbage = True
            elif c == '{':
                depth += 1
                score += depth
            elif c == '}':
                depth -= 1
        i += 1

    print(f"Part 1: {score}")
    print(f"Part 2: {garbage}")

if __name__ == '__main__':
    solve()
