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

    points = []
    for line in lines:
        if not line:
            continue
        points.append(tuple(int(x) for x in line.split(',')))

    n = len(points)
    if n == 0:
        print(0)
        print(0)
        return

    parent = list(range(n))
    rank = [0] * n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1

    def manhattan(p, q):
        return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) + abs(p[3] - q[3])

    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            if manhattan(pi, points[j]) <= 3:
                union(i, j)

    roots = {find(i) for i in range(n)}
    part1 = len(roots)

    print(part1)
    print(0)

if __name__ == '__main__':
    solve()
