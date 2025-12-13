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

    regex = None
    for line in lines:
        if line:
            regex = line
            break
    if not regex:
        print(0)
        print(0)
        return

    # Build undirected graph of rooms
    graph = {}

    def add_edge(a, b):
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    dirs = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0),
    }

    current = {(0, 0)}
    stack = []  # (start_positions, accumulated_end_positions)

    for ch in regex:
        if ch == '^' or ch == '$':
            continue
        if ch in dirs:
            dx, dy = dirs[ch]
            nxt = set()
            for x, y in current:
                nx, ny = x + dx, y + dy
                add_edge((x, y), (nx, ny))
                nxt.add((nx, ny))
            current = nxt
        elif ch == '(':
            stack.append((set(current), set()))
        elif ch == '|':
            start, acc = stack[-1]
            acc.update(current)
            stack[-1] = (start, acc)
            current = set(start)
        elif ch == ')':
            start, acc = stack.pop()
            acc.update(current)
            current = acc

    # BFS distances
    start = (0, 0)
    dist = {start: 0}
    q = [start]
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        for v in graph.get(u, ()): 
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    part1 = max(dist.values()) if dist else 0
    part2 = sum(1 for d in dist.values() if d >= 1000)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
