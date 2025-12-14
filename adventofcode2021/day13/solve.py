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
    dots = set()
    folds = []
    i = 0
    while i < len(lines) and lines[i]:
        x, y = (int(v) for v in lines[i].split(','))
        dots.add((x, y))
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1
    for j in range(i, len(lines)):
        s = lines[j]
        if not s:
            continue
        a, b = s.split('=')
        axis = a[-1]
        folds.append((axis, int(b)))

    def do_fold(d, axis, k):
        out = set()
        if axis == 'x':
            for x, y in d:
                if x > k:
                    x = k - (x - k)
                out.add((x, y))
        else:
            for x, y in d:
                if y > k:
                    y = k - (y - k)
                out.add((x, y))
        return out

    part1 = 0
    if folds:
        axis, k = folds[0]
        dots1 = do_fold(dots, axis, k)
        part1 = len(dots1)
        dcur = dots1
        for axis, k in folds[1:]:
            dcur = do_fold(dcur, axis, k)
    else:
        dcur = dots
        part1 = len(dots)

    maxx = max(x for x, _ in dcur)
    maxy = max(y for _, y in dcur)
    out_lines = []
    for y in range(maxy + 1):
        row = []
        for x in range(maxx + 1):
            row.append('#' if (x, y) in dcur else ' ')
        out_lines.append(''.join(row))

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

    part2 = decode_ocr(out_lines)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
