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
    pairs = [line for line in lines if line]
    parent = {}
    children = {}
    for p in pairs:
        a, b = p.split(')')
        parent[b] = a
        children.setdefault(a, []).append(b)

    # Part 1: total number of direct and indirect orbits
    memo = {}

    def depth(node: str) -> int:
        if node == 'COM':
            return 0
        if node in memo:
            return memo[node]
        d = 1 + depth(parent[node])
        memo[node] = d
        return d

    part1 = 0
    for node in parent.keys():
        part1 += depth(node)

    # Part 2: orbital transfers between YOU and SAN
    def path_to_com(node: str):
        path = {}
        cur = node
        dist = 0
        while cur in parent:
            cur = parent[cur]
            dist += 1
            path[cur] = dist
        return path

    you_orbit = parent.get('YOU')
    san_orbit = parent.get('SAN')
    if you_orbit is None or san_orbit is None:
        part2 = 0
    else:
        py = path_to_com(you_orbit)
        cur = san_orbit
        dist = 0
        best = None
        while True:
            if cur in py:
                best = dist + py[cur]
                break
            if cur not in parent:
                break
            cur = parent[cur]
            dist += 1
        part2 = best if best is not None else 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
