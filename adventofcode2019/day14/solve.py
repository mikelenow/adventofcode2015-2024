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
    reactions = {}
    for line in lines:
        if not line:
            continue
        left, right = line.split('=>')
        out_qty_s, out_chem = right.strip().split()
        out_qty = int(out_qty_s)
        ins = []
        for part in left.strip().split(','):
            q_s, chem = part.strip().split()
            ins.append((chem, int(q_s)))
        reactions[out_chem] = (out_qty, ins)

    if not reactions:
        print(0)
        print(0)
        return

    def ore_for(fuel_amount: int) -> int:
        need = {'FUEL': fuel_amount}
        extra = {}
        while True:
            chem = None
            for k, v in need.items():
                if k != 'ORE' and v > 0:
                    chem = k
                    break
            if chem is None:
                break

            qty_needed = need.get(chem, 0)
            if qty_needed <= 0:
                need[chem] = 0
                continue
            use = min(qty_needed, extra.get(chem, 0))
            qty_needed -= use
            extra[chem] = extra.get(chem, 0) - use
            need[chem] = qty_needed
            if qty_needed == 0:
                continue

            out_qty, ins = reactions[chem]
            times = (qty_needed + out_qty - 1) // out_qty
            made = times * out_qty
            if made > qty_needed:
                extra[chem] = extra.get(chem, 0) + (made - qty_needed)
            need[chem] = 0
            for in_chem, in_qty in ins:
                need[in_chem] = need.get(in_chem, 0) + times * in_qty
        return need.get('ORE', 0)

    part1 = ore_for(1)

    ore_limit = 1_000_000_000_000
    lo = 1
    hi = 1
    while ore_for(hi) <= ore_limit:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if ore_for(mid) <= ore_limit:
            lo = mid
        else:
            hi = mid
    part2 = lo

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
