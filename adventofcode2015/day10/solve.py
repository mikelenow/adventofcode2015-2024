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

    # Day 10: Elves Look, Elves Say
    # Look-and-say sequence

    def look_and_say(s):
        result = []
        i = 0
        while i < len(s):
            char = s[i]
            count = 1
            while i + count < len(s) and s[i + count] == char:
                count += 1
            result.append(str(count) + char)
            i += count
        return ''.join(result)

    sequence = lines[0]

    # Part 1: Apply 40 times
    for _ in range(40):
        sequence = look_and_say(sequence)
    part1 = len(sequence)

    # Part 2: Apply 10 more times (50 total)
    for _ in range(10):
        sequence = look_and_say(sequence)
    part2 = len(sequence)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
