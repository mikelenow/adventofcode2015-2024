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

    # Day 5: Doesn't He Have Intern-Elves For This?
    # Part 1: Count "nice" strings (3 vowels, double letter, no bad pairs)
    # Part 2: Count "nice" strings (pair of letters appearing twice, letter repeating with one between)

    def is_nice_part1(s):
        vowels = sum(1 for c in s if c in 'aeiou')
        if vowels < 3:
            return False

        has_double = any(s[i] == s[i+1] for i in range(len(s)-1))
        if not has_double:
            return False

        bad_pairs = ['ab', 'cd', 'pq', 'xy']
        if any(pair in s for pair in bad_pairs):
            return False

        return True

    def is_nice_part2(s):
        # Check for pair appearing twice without overlapping
        has_pair = False
        for i in range(len(s)-1):
            pair = s[i:i+2]
            if pair in s[i+2:]:
                has_pair = True
                break

        if not has_pair:
            return False

        # Check for letter repeating with one letter between
        has_repeat = any(s[i] == s[i+2] for i in range(len(s)-2))

        return has_repeat

    part1 = sum(1 for line in lines if is_nice_part1(line))
    part2 = sum(1 for line in lines if is_nice_part2(line))

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
