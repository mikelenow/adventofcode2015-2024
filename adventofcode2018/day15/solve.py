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

    raw = [list(line.rstrip('\n')) for line in lines if line != '']
    if not raw:
        print(0)
        print(0)
        return

    height = len(raw)
    width = max(len(r) for r in raw)
    for r in raw:
        if len(r) < width:
            r.extend([' '] * (width - len(r)))

    def run_battle(elf_power: int, stop_on_elf_death: bool):
        walls = set()
        units = []
        uid = 0
        for y in range(height):
            for x in range(width):
                ch = raw[y][x]
                if ch == '#':
                    walls.add((x, y))
                elif ch in ('E', 'G'):
                    units.append({
                        'id': uid,
                        'type': ch,
                        'x': x,
                        'y': y,
                        'hp': 200,
                        'ap': elf_power if ch == 'E' else 3,
                        'alive': True,
                    })
                    uid += 1

        def reading_order(pos):
            return (pos[1], pos[0])

        def neighbors(x, y):
            return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

        def occupied():
            occ = {}
            for u in units:
                if u['alive']:
                    occ[(u['x'], u['y'])] = u
            return occ

        rounds = 0
        initial_elves = sum(1 for u in units if u['type'] == 'E')

        while True:
            units.sort(key=lambda u: (u['y'], u['x']))
            occ = occupied()

            for u in units:
                if not u['alive']:
                    continue

                enemies_alive = [e for e in units if e['alive'] and e['type'] != u['type']]
                if not enemies_alive:
                    total_hp = sum(x['hp'] for x in units if x['alive'])
                    elves_alive = sum(1 for x in units if x['alive'] and x['type'] == 'E')
                    return rounds * total_hp, elves_alive == initial_elves

                ux, uy = u['x'], u['y']

                def adjacent_enemies():
                    adj = []
                    for nx, ny in neighbors(ux, uy):
                        e = occ.get((nx, ny))
                        if e is not None and e['alive'] and e['type'] != u['type']:
                            adj.append(e)
                    if not adj:
                        return None
                    adj.sort(key=lambda e: (e['hp'], e['y'], e['x']))
                    return adj[0]

                target = adjacent_enemies()

                if target is None:
                    targets = set()
                    for e in enemies_alive:
                        ex, ey = e['x'], e['y']
                        for nx, ny in neighbors(ex, ey):
                            if (nx, ny) in walls:
                                continue
                            if (nx, ny) in occ:
                                continue
                            targets.add((nx, ny))

                    if targets:
                        start = (ux, uy)
                        dist = {start: 0}
                        first_step = {}
                        q = [start]
                        head = 0
                        found_dist = None
                        found_targets = []

                        while head < len(q):
                            cx, cy = q[head]
                            head += 1
                            cd = dist[(cx, cy)]
                            if found_dist is not None and cd > found_dist:
                                break
                            if (cx, cy) in targets and (cx, cy) != start:
                                found_dist = cd
                                found_targets.append((cx, cy))
                                continue
                            for nx, ny in neighbors(cx, cy):
                                if (nx, ny) in walls:
                                    continue
                                if (nx, ny) in occ and (nx, ny) != start:
                                    continue
                                if (nx, ny) in dist:
                                    continue
                                dist[(nx, ny)] = cd + 1
                                if (cx, cy) == start:
                                    first_step[(nx, ny)] = (nx, ny)
                                else:
                                    first_step[(nx, ny)] = first_step[(cx, cy)]
                                q.append((nx, ny))

                        if found_targets:
                            found_targets.sort(key=reading_order)
                            chosen = found_targets[0]
                            step = first_step[chosen]
                            del occ[(ux, uy)]
                            u['x'], u['y'] = step
                            ux, uy = u['x'], u['y']
                            occ[(ux, uy)] = u

                    target = None
                    adj = []
                    for nx, ny in neighbors(ux, uy):
                        e = occ.get((nx, ny))
                        if e is not None and e['alive'] and e['type'] != u['type']:
                            adj.append(e)
                    if adj:
                        adj.sort(key=lambda e: (e['hp'], e['y'], e['x']))
                        target = adj[0]

                if target is not None and target['alive']:
                    target['hp'] -= u['ap']
                    if target['hp'] <= 0:
                        target['alive'] = False
                        pos = (target['x'], target['y'])
                        if pos in occ:
                            del occ[pos]
                        if stop_on_elf_death and target['type'] == 'E':
                            return None, False

            rounds += 1

    part1, _ = run_battle(3, False)

    power = 4
    while True:
        outcome, ok = run_battle(power, True)
        if ok and outcome is not None:
            part2 = outcome
            break
        power += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
