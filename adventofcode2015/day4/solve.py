import sys
import hashlib

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

    # Day 4: The Ideal Stocking Stuffer
    # Find the lowest number that produces MD5 hash starting with 5 zeros (part 1) and 6 zeros (part 2)

    secret_key = lines[0]

    # Part 1: Find hash starting with 00000
    num = 1
    while True:
        hash_input = f"{secret_key}{num}"
        hash_result = hashlib.md5(hash_input.encode()).hexdigest()
        if hash_result.startswith("00000"):
            part1 = num
            break
        num += 1

    # Part 2: Find hash starting with 000000
    num = 1
    while True:
        hash_input = f"{secret_key}{num}"
        hash_result = hashlib.md5(hash_input.encode()).hexdigest()
        if hash_result.startswith("000000"):
            part2 = num
            break
        num += 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
