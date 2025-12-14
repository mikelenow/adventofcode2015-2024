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
    if not lines:
        print(0)
        print(0)
        return

    steps = []
    for line in lines:
        if line:
            steps.extend(line.split(','))

    def hsh(s):
        v = 0
        for ch in s:
            v = (v + ord(ch)) * 17 % 256
        return v

    part1 = sum(hsh(s) for s in steps)

    boxes = [[] for _ in range(256)]

    for s in steps:
        if s.endswith('-'):
            label = s[:-1]
            b = boxes[hsh(label)]
            for i in range(len(b)):
                if b[i][0] == label:
                    b.pop(i)
                    break
        else:
            label, val_s = s.split('=')
            focal = int(val_s)
            b = boxes[hsh(label)]
            for i in range(len(b)):
                if b[i][0] == label:
                    b[i] = (label, focal)
                    break
            else:
                b.append((label, focal))

    part2 = 0
    for bi, b in enumerate(boxes, 1):
        for si, (_, focal) in enumerate(b, 1):
            part2 += bi * si * focal

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
