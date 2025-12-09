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
    from collections import defaultdict, deque

    graph = defaultdict(list)

    for line in lines:
        if not line:
            continue
        left, right = line.split('<->')
        src = int(left.strip())
        targets = [int(x.strip()) for x in right.split(',')]
        for t in targets:
            graph[src].append(t)
            graph[t].append(src)

    def bfs(start, visited):
        q = deque([start])
        visited.add(start)
        size = 0
        while q:
            u = q.popleft()
            size += 1
            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return size

    visited = set()
    part1 = bfs(0, visited)

    groups = 1
    for node in graph.keys():
        if node not in visited:
            bfs(node, visited)
            groups += 1

    part2 = groups

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
