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
    data = ''.join(line.strip() for line in lines if line.strip())
    if not data:
        print(0)
        print('')
        return

    width = 25
    height = 6
    layer_size = width * height
    layers = [data[i:i + layer_size] for i in range(0, len(data), layer_size)]

    best = None
    best_layer = None
    for layer in layers:
        z = layer.count('0')
        if best is None or z < best:
            best = z
            best_layer = layer
    part1 = best_layer.count('1') * best_layer.count('2')

    # Part 2: decode image (0 black, 1 white, 2 transparent)
    final = ['2'] * layer_size
    for layer in layers:
        for i, ch in enumerate(layer):
            if final[i] == '2' and ch != '2':
                final[i] = ch

    # render as lines using # and space
    out_lines = []
    for r in range(height):
        row = ''
        for c in range(width):
            pix = final[r * width + c]
            row += '#' if pix == '1' else ' '
        out_lines.append(row)

    print(part1)
    # OCR decode using the standard AoC 6-tall font. Most puzzles use 4-wide letters
    # separated by 1 blank column, so we split by blank columns instead of hard slicing.
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
        # 5-wide fallbacks (used in some years/fonts)
        ".##..\n#..#.\n#..#.\n####.\n#..#.\n#..#.": "A",
        "####.\n#....\n###..\n#....\n#....\n####.": "E",
        ".###.\n#....\n#....\n#.##.\n#..#.\n.###.": "G",
        ".##..\n#..#.\n#....\n#.##.\n#..#.\n.###.": "G",
        "#..#.\n#..#.\n####.\n#..#.\n#..#.\n#..#.": "H",
        "#....\n#....\n#....\n#....\n#....\n####.": "L",
        ".##..\n#..#.\n#..#.\n#..#.\n#..#.\n.##..": "O",
        "###..\n#..#.\n#..#.\n###..\n#.#..\n#..#.": "R",
    }

    norm = [row.replace(' ', '.') for row in out_lines]
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

    letters = []
    for start, end in groups:
        # Drop an all-dot trailing column if present (common 4+1 spacing rendered as 5-wide chunks)
        if end - start == 5:
            trailing_all_dot = all(norm[r][end - 1] == '.' for r in range(height))
            if trailing_all_dot:
                end -= 1
        pat_rows = [norm[r][start:end] for r in range(height)]
        pat = '\n'.join(pat_rows)
        letters.append(font.get(pat, '?'))
    decoded = ''.join(letters)

    print(decoded)
    print('\n'.join(out_lines))

if __name__ == '__main__':
    solve()
