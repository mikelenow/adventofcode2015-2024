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
    clean = [s for s in lines]
    if not clean or not clean[0]:
        print(0)
        print(0)
        return

    draws = [int(x) for x in clean[0].split(',')]
    boards = []
    i = 1
    while i < len(clean):
        if clean[i] == '':
            i += 1
            continue
        grid = []
        for _ in range(5):
            if i >= len(clean):
                break
            row = [int(x) for x in clean[i].split()]
            grid.append(row)
            i += 1
        if len(grid) == 5:
            boards.append(grid)

    if not boards:
        print(0)
        print(0)
        return

    bpos = []
    for b in boards:
        mp = {}
        for r in range(5):
            for c in range(5):
                mp[b[r][c]] = (r, c)
        bpos.append(mp)

    marks = [[[False] * 5 for _ in range(5)] for _ in boards]
    rowc = [[0] * 5 for _ in boards]
    colc = [[0] * 5 for _ in boards]
    won = [False] * len(boards)

    def unmarked_sum(bi):
        s = 0
        b = boards[bi]
        m = marks[bi]
        for r in range(5):
            for c in range(5):
                if not m[r][c]:
                    s += b[r][c]
        return s

    part1 = None
    part2 = None
    remaining = len(boards)

    for d in draws:
        for bi, mp in enumerate(bpos):
            if won[bi]:
                continue
            rc = mp.get(d)
            if rc is None:
                continue
            r, c = rc
            if marks[bi][r][c]:
                continue
            marks[bi][r][c] = True
            rowc[bi][r] += 1
            colc[bi][c] += 1
            if rowc[bi][r] == 5 or colc[bi][c] == 5:
                won[bi] = True
                remaining -= 1
                score = unmarked_sum(bi) * d
                if part1 is None:
                    part1 = score
                part2 = score
        if remaining == 0:
            break

    print(part1 or 0)
    print(part2 or 0)

if __name__ == '__main__':
    solve()
