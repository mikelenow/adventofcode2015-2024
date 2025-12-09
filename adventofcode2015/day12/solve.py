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

    # Day 12: JSAbacusFramework.io
    # Sum all numbers in JSON, ignoring red objects in part 2

    import json
    import re

    data = lines[0]

    # Part 1: Sum all numbers
    numbers = re.findall(r'-?\d+', data)
    part1 = sum(int(n) for n in numbers)

    # Part 2: Sum all numbers, but ignore objects with "red" as a value
    def sum_numbers(obj):
        if isinstance(obj, int):
            return obj
        elif isinstance(obj, list):
            return sum(sum_numbers(item) for item in obj)
        elif isinstance(obj, dict):
            # Check if any value is "red"
            if "red" in obj.values():
                return 0
            return sum(sum_numbers(value) for value in obj.values())
        else:
            return 0

    json_data = json.loads(data)
    part2 = sum_numbers(json_data)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
