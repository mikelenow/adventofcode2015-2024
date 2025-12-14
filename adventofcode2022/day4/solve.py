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
    p1 = 0
    p2 = 0
    for s in lines:
        if not s:
            continue
        a, b = s.split(',')
        a1, a2 = map(int, a.split('-'))
        b1, b2 = map(int, b.split('-'))

        if (a1 <= b1 and a2 >= b2) or (b1 <= a1 and b2 >= a2):
            p1 += 1
        if not (a2 < b1 or b2 < a1):
            p2 += 1

    print(p1)
    print(p2)

if __name__ == '__main__':
    solve()
