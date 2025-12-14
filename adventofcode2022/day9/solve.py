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
    moves = []
    for s in lines:
        if not s:
            continue
        d, n = s.split()
        moves.append((d, int(n)))

    def run(k):
        rope = [[0, 0] for _ in range(k)]
        seen = {(0, 0)}
        for d, n in moves:
            for _ in range(n):
                if d == 'U':
                    rope[0][1] -= 1
                elif d == 'D':
                    rope[0][1] += 1
                elif d == 'L':
                    rope[0][0] -= 1
                else:
                    rope[0][0] += 1

                for i in range(1, k):
                    hx, hy = rope[i - 1]
                    tx, ty = rope[i]
                    dx = hx - tx
                    dy = hy - ty
                    if abs(dx) > 1 or abs(dy) > 1:
                        if dx:
                            tx += 1 if dx > 0 else -1
                        if dy:
                            ty += 1 if dy > 0 else -1
                        rope[i][0] = tx
                        rope[i][1] = ty
                seen.add((rope[-1][0], rope[-1][1]))
        return len(seen)

    print(run(2))
    print(run(10))

if __name__ == '__main__':
    solve()
