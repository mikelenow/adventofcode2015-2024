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

    def decompress_length_v1(s):
        length = 0
        i = 0
        while i < len(s):
            if s[i] == '(':
                marker_end = s.index(')', i)
                marker = s[i+1:marker_end]
                chars, repeat = map(int, marker.split('x'))
                length += chars * repeat
                i = marker_end + 1 + chars
            else:
                length += 1
                i += 1
        return length

    def decompress_length_v2(s):
        if '(' not in s:
            return len(s)

        length = 0
        i = 0
        while i < len(s):
            if s[i] == '(':
                marker_end = s.index(')', i)
                marker = s[i+1:marker_end]
                chars, repeat = map(int, marker.split('x'))
                segment = s[marker_end + 1:marker_end + 1 + chars]
                length += decompress_length_v2(segment) * repeat
                i = marker_end + 1 + chars
            else:
                length += 1
                i += 1
        return length

    data = lines[0]

    part1 = decompress_length_v1(data)
    part2 = decompress_length_v2(data)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
