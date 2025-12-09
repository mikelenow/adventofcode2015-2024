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
    components = []
    for line in lines:
        if not line:
            continue
        a, b = map(int, line.split('/'))
        components.append((a, b))

    best_strength = 0
    best_len = 0
    best_long_strength = 0

    def dfs(port, used_mask, cur_strength, cur_len):
        nonlocal best_strength, best_len, best_long_strength
        if cur_strength > best_strength:
            best_strength = cur_strength
        if cur_len > best_len:
            best_len = cur_len
            best_long_strength = cur_strength
        elif cur_len == best_len and cur_strength > best_long_strength:
            best_long_strength = cur_strength

        for i, (a, b) in enumerate(components):
            if used_mask & (1 << i):
                continue
            if a == port or b == port:
                nxt = b if a == port else a
                dfs(nxt, used_mask | (1 << i), cur_strength + a + b, cur_len + 1)

    dfs(0, 0, 0, 0)

    part1 = best_strength
    part2 = best_long_strength

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
