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
    grid = [line for line in lines if line]
    H = len(grid)
    W = len(grid[0]) if H else 0

    if H == 0 or W == 0:
        print(0)
        print(0)
        return

    # dir: 0=R,1=D,2=L,3=U
    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def energize(start_x, start_y, start_d):
        from collections import deque

        q = deque([(start_x, start_y, start_d)])
        seen = set()
        lit = set()
        while q:
            x, y, d = q.popleft()
            dx, dy = DIRS[d]
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            state = (nx, ny, d)
            if state in seen:
                continue
            seen.add(state)
            lit.add((nx, ny))

            ch = grid[ny][nx]
            if ch == '.':
                q.append((nx, ny, d))
            elif ch == '/':
                nd = {0: 3, 3: 0, 2: 1, 1: 2}[d]
                q.append((nx, ny, nd))
            elif ch == '\\':
                nd = {0: 1, 1: 0, 2: 3, 3: 2}[d]
                q.append((nx, ny, nd))
            elif ch == '|':
                if d in (0, 2):
                    q.append((nx, ny, 3))
                    q.append((nx, ny, 1))
                else:
                    q.append((nx, ny, d))
            elif ch == '-':
                if d in (1, 3):
                    q.append((nx, ny, 0))
                    q.append((nx, ny, 2))
                else:
                    q.append((nx, ny, d))
            else:
                q.append((nx, ny, d))
        return len(lit)

    part1 = energize(-1, 0, 0)

    best = 0
    for x in range(W):
        best = max(best, energize(x, -1, 1))
        best = max(best, energize(x, H, 3))
    for y in range(H):
        best = max(best, energize(-1, y, 0))
        best = max(best, energize(W, y, 2))

    print(part1)
    print(best)

if __name__ == '__main__':
    solve()
