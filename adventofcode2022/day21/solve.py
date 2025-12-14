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
    defs = {}
    for s in lines:
        if not s:
            continue
        name, expr = s.split(':', 1)
        defs[name] = expr.strip()

    from functools import lru_cache

    @lru_cache(None)
    def eval1(name):
        expr = defs[name]
        parts = expr.split()
        if len(parts) == 1:
            return int(parts[0])
        a, op, b = parts
        x = eval1(a)
        y = eval1(b)
        if op == '+':
            return x + y
        if op == '-':
            return x - y
        if op == '*':
            return x * y
        return x // y

    part1 = eval1('root') if 'root' in defs else 0

    @lru_cache(None)
    def depends(name):
        if name == 'humn':
            return True
        expr = defs[name]
        parts = expr.split()
        if len(parts) == 1:
            return False
        a, _, b = parts
        return depends(a) or depends(b)

    def eval_known(name):
        expr = defs[name]
        parts = expr.split()
        if len(parts) == 1:
            return int(parts[0])
        a, op, b = parts
        x = eval_known(a)
        y = eval_known(b)
        if op == '+':
            return x + y
        if op == '-':
            return x - y
        if op == '*':
            return x * y
        return x // y

    def solve_for(name, target):
        if name == 'humn':
            return target
        expr = defs[name]
        a, op, b = expr.split()
        left_dep = depends(a)
        if left_dep:
            known = eval_known(b)
            if op == '+':
                return solve_for(a, target - known)
            if op == '-':
                return solve_for(a, target + known)
            if op == '*':
                return solve_for(a, target // known)
            return solve_for(a, target * known)
        else:
            known = eval_known(a)
            if op == '+':
                return solve_for(b, target - known)
            if op == '-':
                return solve_for(b, known - target)
            if op == '*':
                return solve_for(b, target // known)
            return solve_for(b, known // target)

    if 'root' not in defs:
        part2 = 0
    else:
        a, _, b = defs['root'].split()
        if depends(a):
            tgt = eval_known(b)
            part2 = solve_for(a, tgt)
        else:
            tgt = eval_known(a)
            part2 = solve_for(b, tgt)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
