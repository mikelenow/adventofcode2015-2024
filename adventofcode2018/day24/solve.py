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

    import re

    line_re = re.compile(
        r"^(\d+) units each with (\d+) hit points(?: \(([^)]+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)$"
    )

    def parse_army(boost: int):
        groups = []
        army = None
        gid = 0
        for line in lines:
            if not line:
                continue
            if line.endswith(':'):
                army = line[:-1]
                continue
            m = line_re.match(line)
            if not m:
                continue
            units = int(m.group(1))
            hp = int(m.group(2))
            props = m.group(3)
            dmg = int(m.group(4))
            atype = m.group(5)
            init = int(m.group(6))
            weak = set()
            immune = set()
            if props:
                parts = [p.strip() for p in props.split(';')]
                for p in parts:
                    if p.startswith('weak to '):
                        weak.update(x.strip() for x in p[len('weak to '):].split(','))
                    elif p.startswith('immune to '):
                        immune.update(x.strip() for x in p[len('immune to '):].split(','))
            if army == 'Immune System':
                dmg += boost
            groups.append({
                'id': gid,
                'army': army,
                'units': units,
                'hp': hp,
                'weak': weak,
                'immune': immune,
                'dmg': dmg,
                'atype': atype,
                'init': init,
            })
            gid += 1
        return groups

    def effective_power(g):
        return g['units'] * g['dmg']

    def damage(att, defn):
        if att['atype'] in defn['immune']:
            return 0
        d = effective_power(att)
        if att['atype'] in defn['weak']:
            d *= 2
        return d

    def simulate(boost: int):
        groups = parse_army(boost)
        while True:
            alive = [g for g in groups if g['units'] > 0]
            armies = set(g['army'] for g in alive)
            if len(armies) <= 1:
                winner = next(iter(armies)) if armies else None
                total = sum(g['units'] for g in alive)
                return winner, total

            # Target selection
            alive.sort(key=lambda g: (effective_power(g), g['init']), reverse=True)
            chosen = set()
            targets = {}
            for g in alive:
                enemies = [e for e in alive if e['army'] != g['army'] and e['id'] not in chosen and e['units'] > 0]
                if not enemies:
                    continue
                enemies.sort(key=lambda e: (damage(g, e), effective_power(e), e['init']), reverse=True)
                if damage(g, enemies[0]) == 0:
                    continue
                t = enemies[0]
                targets[g['id']] = t['id']
                chosen.add(t['id'])

            # Attacking
            alive.sort(key=lambda g: g['init'], reverse=True)
            any_kill = False
            by_id = {g['id']: g for g in alive}
            for g in alive:
                if g['units'] <= 0:
                    continue
                tid = targets.get(g['id'])
                if tid is None:
                    continue
                t = by_id.get(tid)
                if t is None or t['units'] <= 0:
                    continue
                d = damage(g, t)
                killed = min(t['units'], d // t['hp'])
                if killed > 0:
                    any_kill = True
                t['units'] -= killed

            if not any_kill:
                return None, sum(g['units'] for g in alive)

    # Part 1
    _, part1 = simulate(0)

    # Part 2: minimal boost for immune victory
    lo = 1
    hi = 1
    while True:
        w, _ = simulate(hi)
        if w == 'Immune System':
            break
        hi *= 2

    while lo < hi:
        mid = (lo + hi) // 2
        w, _ = simulate(mid)
        if w == 'Immune System':
            hi = mid
        else:
            lo = mid + 1

    _, part2 = simulate(lo)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
