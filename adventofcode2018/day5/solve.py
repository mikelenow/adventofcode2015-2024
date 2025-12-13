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

    polymer = ''
    for line in lines:
        if line:
            polymer = line
            break

    def react(s: str) -> int:
        stack = []
        for ch in s:
            if stack:
                top = stack[-1]
                if top != ch and top.lower() == ch.lower():
                    stack.pop()
                    continue
            stack.append(ch)
        return len(stack)

    part1 = react(polymer)

    best = None
    for i in range(26):
        letter = chr(ord('a') + i)
        filtered = [ch for ch in polymer if ch.lower() != letter]
        length = react(filtered)
        if best is None or length < best:
            best = length

    print(part1)
    print(best)

if __name__ == '__main__':
    solve()
