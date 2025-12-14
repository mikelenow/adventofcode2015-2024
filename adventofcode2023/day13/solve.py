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
    blocks = []
    cur = []
    for line in lines + ['']:
        if line == '':
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(line)

    def find_reflection_rows(g, target):
        H = len(g)
        W = len(g[0])
        for i in range(1, H):
            mism = 0
            a = i - 1
            b = i
            while a >= 0 and b < H:
                ra = g[a]
                rb = g[b]
                for x in range(W):
                    if ra[x] != rb[x]:
                        mism += 1
                        if mism > target:
                            break
                if mism > target:
                    break
                a -= 1
                b += 1
            if mism == target:
                return i
        return 0

    def find_reflection_cols(g, target):
        H = len(g)
        W = len(g[0])
        for j in range(1, W):
            mism = 0
            a = j - 1
            b = j
            while a >= 0 and b < W:
                for y in range(H):
                    if g[y][a] != g[y][b]:
                        mism += 1
                        if mism > target:
                            break
                if mism > target:
                    break
                a -= 1
                b += 1
            if mism == target:
                return j
        return 0

    def score(g, target):
        r = find_reflection_rows(g, target)
        if r:
            return 100 * r
        c = find_reflection_cols(g, target)
        return c

    part1 = sum(score(b, 0) for b in blocks)
    part2 = sum(score(b, 1) for b in blocks)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
