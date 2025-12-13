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

    depth = None
    target = None
    for line in lines:
        if not line:
            continue
        if line.startswith('depth:'):
            depth = int(line.split(':')[1].strip())
        elif line.startswith('target:'):
            xy = line.split(':')[1].strip().split(',')
            target = (int(xy[0]), int(xy[1]))

    if depth is None or target is None:
        print(0)
        print(0)
        return

    tx, ty = target

    # Memoized erosion / type
    erosion = {}

    def erosion_level(x: int, y: int) -> int:
        key = (x, y)
        if key in erosion:
            return erosion[key]
        if (x, y) == (0, 0) or (x, y) == (tx, ty):
            gi = 0
        elif y == 0:
            gi = x * 16807
        elif x == 0:
            gi = y * 48271
        else:
            gi = erosion_level(x - 1, y) * erosion_level(x, y - 1)
        el = (gi + depth) % 20183
        erosion[key] = el
        return el

    def region_type(x: int, y: int) -> int:
        # 0 rocky, 1 wet, 2 narrow
        return erosion_level(x, y) % 3

    # Part 1
    risk = 0
    for y in range(ty + 1):
        for x in range(tx + 1):
            risk += region_type(x, y)

    # Part 2: Dijkstra on (x,y,tool)
    # tools: 0=torch, 1=climbing, 2=neither
    # allowed by region:
    # rocky: torch/climbing; wet: climbing/neither; narrow: torch/neither
    allowed = {
        0: {0, 1},
        1: {1, 2},
        2: {0, 2},
    }

    import heapq

    margin = 60
    max_x = tx + margin
    max_y = ty + margin

    start = (0, 0, 0)
    dist = {start: 0}
    pq = [(0, start)]

    def neighbors(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        yield x + 1, y
        yield x, y + 1

    while pq:
        d, state = heapq.heappop(pq)
        if d != dist.get(state):
            continue
        x, y, tool = state
        if x == tx and y == ty and tool == 0:
            part2 = d
            print(risk)
            print(part2)
            return

        if x > max_x or y > max_y:
            continue

        rt = region_type(x, y)
        # switch tool
        for new_tool in allowed[rt]:
            if new_tool != tool:
                ns = (x, y, new_tool)
                nd = d + 7
                if nd < dist.get(ns, 10**18):
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))

        # move
        for nx, ny in neighbors(x, y):
            if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                continue
            nrt = region_type(nx, ny)
            if tool in allowed[nrt]:
                ns = (nx, ny, tool)
                nd = d + 1
                if nd < dist.get(ns, 10**18):
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))

    print(risk)
    print(None)

if __name__ == '__main__':
    solve()
