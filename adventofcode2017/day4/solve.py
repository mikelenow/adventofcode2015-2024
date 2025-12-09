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
    valid1 = 0
    valid2 = 0

    for line in lines:
        if not line:
            continue
        words = line.split()

        # Part 1: no duplicate words
        if len(words) == len(set(words)):
            valid1 += 1

        # Part 2: no two words are anagrams
        sorted_words = [''.join(sorted(w)) for w in words]
        if len(sorted_words) == len(set(sorted_words)):
            valid2 += 1

    print(f"Part 1: {valid1}")
    print(f"Part 2: {valid2}")

if __name__ == '__main__':
    solve()
