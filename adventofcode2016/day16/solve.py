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

    def dragon_curve(data):
        b = data[::-1]
        b = ''.join('0' if c == '1' else '1' for c in b)
        return data + '0' + b

    def checksum(data):
        while len(data) % 2 == 0:
            new_data = []
            for i in range(0, len(data), 2):
                if data[i] == data[i+1]:
                    new_data.append('1')
                else:
                    new_data.append('0')
            data = ''.join(new_data)
        return data

    def fill_disk(initial, length):
        data = initial
        while len(data) < length:
            data = dragon_curve(data)
        data = data[:length]
        return checksum(data)

    initial = lines[0]
    part1 = fill_disk(initial, 272)
    part2 = fill_disk(initial, 35651584)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
