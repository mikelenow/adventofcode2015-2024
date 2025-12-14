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
    prog = [s for s in lines if s]

    x = 1
    cycle = 0
    check = {20, 60, 100, 140, 180, 220}
    strength = 0

    screen = [['.' for _ in range(40)] for _ in range(6)]

    def tick():
        nonlocal cycle, strength
        cycle += 1
        pos = cycle - 1
        r = pos // 40
        c = pos % 40
        if 0 <= r < 6:
            if abs(c - x) <= 1:
                screen[r][c] = '#'
        if cycle in check:
            strength += cycle * x

    for s in prog:
        if s == 'noop':
            tick()
        else:
            op, v = s.split()
            if op != 'addx':
                continue
            tick()
            tick()
            x += int(v)

    out_lines = [''.join(row) for row in screen]

    def decode_ocr(lines6):
        height = len(lines6)
        if height == 0:
            return ''
        norm = [row.replace(' ', '.') for row in lines6]
        cols = len(norm[0])
        nonblank = [any(norm[r][c] == '#' for r in range(height)) for c in range(cols)]
        groups = []
        c = 0
        while c < cols:
            if not nonblank[c]:
                c += 1
                continue
            start = c
            while c < cols and nonblank[c]:
                c += 1
            end = c
            groups.append((start, end))

        font = {
            ".##.\n#..#\n#..#\n####\n#..#\n#..#": "A",
            "###.\n#..#\n###.\n#..#\n#..#\n###.": "B",
            ".##.\n#..#\n#...\n#...\n#..#\n.##.": "C",
            "###.\n#..#\n#..#\n#..#\n#..#\n###.": "D",
            "####\n#...\n###.\n#...\n#...\n####": "E",
            "####\n#...\n###.\n#...\n#...\n#...": "F",
            ".###\n#...\n#...\n#.##\n#..#\n.###": "G",
            "#..#\n#..#\n####\n#..#\n#..#\n#..#": "H",
            "###.\n.#..\n.#..\n.#..\n.#..\n###.": "I",
            "..##\n...#\n...#\n...#\n#..#\n.##.": "J",
            "#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#": "K",
            "#...\n#...\n#...\n#...\n#...\n####": "L",
            ".##.\n#..#\n#..#\n#..#\n#..#\n.##.": "O",
            "###.\n#..#\n#..#\n###.\n#...\n#...": "P",
            "###.\n#..#\n#..#\n###.\n#.#.\n#..#": "R",
            ".###\n#...\n#...\n.##.\n...#\n###.": "S",
            "#..#\n#..#\n#..#\n#..#\n#..#\n.##.": "U",
            "#...#\n.#.#.\n..#..\n..#..\n.#.#.\n#...#": "X",
            "#...#\n.#.#.\n..#..\n.#...\n.#...\n.#...": "Y",
            "####\n...#\n..#.\n.#..\n#...\n####": "Z",
            ".##..\n#..#.\n#..#.\n####.\n#..#.\n#..#.": "A",
            "####.\n#....\n###..\n#....\n#....\n####.": "E",
            ".###.\n#....\n#....\n#.##.\n#..#.\n.###.": "G",
            "#..#.\n#..#.\n####.\n#..#.\n#..#.\n#..#.": "H",
            "#....\n#....\n#....\n#....\n#....\n####.": "L",
            ".##..\n#..#.\n#..#.\n#..#.\n#..#.\n.##..": "O",
            "###..\n#..#.\n#..#.\n###..\n#.#..\n#..#.": "R",
        }

        letters = []
        for start, end in groups:
            if end - start == 5:
                trailing_all_dot = all(norm[r][end - 1] == '.' for r in range(height))
                if trailing_all_dot:
                    end -= 1
            pat_rows = [norm[r][start:end] for r in range(height)]
            pat = '\n'.join(pat_rows)
            letters.append(font.get(pat, '?'))
        return ''.join(letters)

    print(strength)
    print(decode_ocr(out_lines))

if __name__ == '__main__':
    solve()
