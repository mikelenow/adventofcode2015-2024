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
    part1 = 0
    for s in lines:
        digits = [c for c in s if c.isdigit()]
        part1 += int(digits[0] + digits[-1])

    words = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'zero': 0,
    }
    word_items = list(words.items())

    part2 = 0
    for s in lines:
        vals = []
        for i, ch in enumerate(s):
            if ch.isdigit():
                vals.append(int(ch))
                continue
            for w, v in word_items:
                if s.startswith(w, i):
                    vals.append(v)
                    break
        part2 += vals[0] * 10 + vals[-1]

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
