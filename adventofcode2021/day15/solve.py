import sys
import heapq

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
    grid = [s for s in lines if s]
    if not grid:
        print(0)
        print(0)
        return

    base = [[int(ch) for ch in row] for row in grid]
    H = len(base)
    W = len(base[0])

    def dijkstra(h, w, risk_at):
        dist = [[10**18] * w for _ in range(h)]
        dist[0][0] = 0
        pq = [(0, 0, 0)]
        while pq:
            d, x, y = heapq.heappop(pq)
            if d != dist[y][x]:
                continue
            if x == w - 1 and y == h - 1:
                return d
            nd = d + 1
            if x > 0:
                v = d + risk_at(x - 1, y)
                if v < dist[y][x - 1]:
                    dist[y][x - 1] = v
                    heapq.heappush(pq, (v, x - 1, y))
            if x + 1 < w:
                v = d + risk_at(x + 1, y)
                if v < dist[y][x + 1]:
                    dist[y][x + 1] = v
                    heapq.heappush(pq, (v, x + 1, y))
            if y > 0:
                v = d + risk_at(x, y - 1)
                if v < dist[y - 1][x]:
                    dist[y - 1][x] = v
                    heapq.heappush(pq, (v, x, y - 1))
            if y + 1 < h:
                v = d + risk_at(x, y + 1)
                if v < dist[y + 1][x]:
                    dist[y + 1][x] = v
                    heapq.heappush(pq, (v, x, y + 1))
        return dist[h - 1][w - 1]

    def risk1(x, y):
        return base[y][x]

    part1 = dijkstra(H, W, risk1)

    H2 = H * 5
    W2 = W * 5

    def risk2(x, y):
        v = base[y % H][x % W] + (x // W) + (y // H)
        v = ((v - 1) % 9) + 1
        return v

    part2 = dijkstra(H2, W2, risk2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
