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

    # Day 20: Infinite Elves and Infinite Houses
    target = int(lines[0])

    # Part 1: Each elf delivers 10 presents to infinite houses
    def presents_at_house_part1(house):
        total = 0
        for elf in range(1, int(house**0.5) + 1):
            if house % elf == 0:
                total += elf * 10
                if elf != house // elf:
                    total += (house // elf) * 10
        return total

    house = 1
    while presents_at_house_part1(house) < target:
        house += 1
    part1 = house

    # Part 2: Each elf delivers 11 presents to only 50 houses
    def presents_at_house_part2(house):
        total = 0
        for elf in range(1, int(house**0.5) + 1):
            if house % elf == 0:
                if house // elf <= 50:
                    total += elf * 11
                if elf != house // elf and elf <= 50:
                    total += (house // elf) * 11
        return total

    house = 1
    while presents_at_house_part2(house) < target:
        house += 1
    part2 = house

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
