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

    def next_row(row):
        new_row = []
        for i in range(len(row)):
            left = row[i-1] if i > 0 else '.'
            center = row[i]
            right = row[i+1] if i < len(row) - 1 else '.'

            if (left == '^' and center == '^' and right == '.') or \
               (center == '^' and right == '^' and left == '.') or \
               (left == '^' and center == '.' and right == '.') or \
               (left == '.' and center == '.' and right == '^'):
                new_row.append('^')
            else:
                new_row.append('.')

        return ''.join(new_row)

    def count_safe(first_row, num_rows):
        current = first_row
        safe_count = current.count('.')

        for _ in range(num_rows - 1):
            current = next_row(current)
            safe_count += current.count('.')

        return safe_count

    first_row = lines[0]
    part1 = count_safe(first_row, 40)
    part2 = count_safe(first_row, 400000)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
