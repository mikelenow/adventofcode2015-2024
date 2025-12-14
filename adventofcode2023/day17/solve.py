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

    cost = [[int(c) for c in row] for row in grid]

    # dir: 0=R,1=D,2=L,3=U
    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def dijkstra(min_run, max_run):
        import heapq

        INF = 10**30
        dist = {}
        pq = []

        for d in (0, 1):
            dx, dy = DIRS[d]
            nx, ny = dx, dy
            if 0 <= nx < W and 0 <= ny < H:
                v = cost[ny][nx]
                st = (nx, ny, d, 1)
                dist[st] = v
                heapq.heappush(pq, (v, st))

        best_end = INF
        while pq:
            cur, (x, y, d, run) = heapq.heappop(pq)
            if cur != dist.get((x, y, d, run)):
                continue
            if x == W - 1 and y == H - 1:
                if run >= min_run:
                    best_end = cur
                    break

            # continue straight
            if run < max_run:
                dx, dy = DIRS[d]
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    nst = (nx, ny, d, run + 1)
                    nv = cur + cost[ny][nx]
                    if nv < dist.get(nst, INF):
                        dist[nst] = nv
                        heapq.heappush(pq, (nv, nst))

            # turn left/right
            if run >= min_run:
                for nd in ((d + 1) % 4, (d + 3) % 4):
                    dx, dy = DIRS[nd]
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        nst = (nx, ny, nd, 1)
                        nv = cur + cost[ny][nx]
                        if nv < dist.get(nst, INF):
                            dist[nst] = nv
                            heapq.heappush(pq, (nv, nst))

        return best_end

    part1 = dijkstra(1, 3)
    part2 = dijkstra(4, 10)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
