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
    import re

    particles = []
    pattern = re.compile(r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)}?")

    for line in lines:
        if not line:
            continue
        m = pattern.match(line)
        if not m:
            # Fallback simple parsing
            parts = line.split(', ')
            vals = []
            for part in parts:
                nums = part[part.index('<') + 1:part.index('>')].split(',')
                vals.extend(int(x) for x in nums)
        else:
            vals = [int(x) for x in m.groups()]
        p = vals[0:3]
        v = vals[3:6]
        a = vals[6:9]
        particles.append({'p': p, 'v': v, 'a': a})

    def simulate(num_steps, remove_collisions):
        parts = [
            {
                'p': p['p'][:],
                'v': p['v'][:],
                'a': p['a'][:],
            }
            for p in particles
        ]
        alive = [True] * len(parts)

        for _ in range(num_steps):
            positions = {}
            for i, part in enumerate(parts):
                if not alive[i]:
                    continue
                v = part['v']
                a = part['a']
                pos = part['p']
                v[0] += a[0]
                v[1] += a[1]
                v[2] += a[2]
                pos[0] += v[0]
                pos[1] += v[1]
                pos[2] += v[2]
                positions.setdefault(tuple(pos), []).append(i)

            if remove_collisions:
                for idxs in positions.values():
                    if len(idxs) > 1:
                        for i in idxs:
                            alive[i] = False

        if remove_collisions:
            return sum(alive)
        else:
            best_idx = None
            best_dist = None
            for i, part in enumerate(parts):
                if not alive[i]:
                    continue
                x, y, z = part['p']
                d = abs(x) + abs(y) + abs(z)
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_idx = i
            return best_idx

    # Enough steps for the system to stabilize and resolve collisions
    part1 = simulate(5000, remove_collisions=False)
    part2 = simulate(5000, remove_collisions=True)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
