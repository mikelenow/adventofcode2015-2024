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

    masses = [int(x) for x in lines if x]

    def fuel_for(m: int) -> int:
        return m // 3 - 2

    part1 = sum(fuel_for(m) for m in masses)

    def total_fuel(m: int) -> int:
        total = 0
        cur = fuel_for(m)
        while cur > 0:
            total += cur
            cur = fuel_for(cur)
        return total

    part2 = sum(total_fuel(m) for m in masses)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
