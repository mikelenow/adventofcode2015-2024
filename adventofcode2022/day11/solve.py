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
    blocks = []
    cur = []
    for s in lines + ['']:
        if s == '':
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(s)

    monkeys = []
    for b in blocks:
        items = []
        op = None
        test = 1
        tdst = 0
        fdst = 0
        for s in b:
            if s.startswith('Starting items:'):
                rest = s.split(':', 1)[1].strip()
                if rest:
                    items = [int(x.strip()) for x in rest.split(',')]
            elif s.startswith('Operation:'):
                expr = s.split('=', 1)[1].strip()
                parts = expr.split()
                a, oper, b2 = parts[0], parts[1], parts[2]

                def make_op(oper, b2):
                    if b2 == 'old':
                        if oper == '*':
                            return lambda old: old * old
                        return lambda old: old + old
                    v = int(b2)
                    if oper == '*':
                        return lambda old, v=v: old * v
                    return lambda old, v=v: old + v

                op = make_op(oper, b2)
            elif s.startswith('Test:'):
                test = int(s.split()[-1])
            elif s.startswith('If true:'):
                tdst = int(s.split()[-1])
            elif s.startswith('If false:'):
                fdst = int(s.split()[-1])
        monkeys.append([items, op, test, tdst, fdst])

    if not monkeys:
        print(0)
        print(0)
        return

    def run(rounds, relief):
        items = [m[0][:] for m in monkeys]
        ops = [m[1] for m in monkeys]
        tests = [m[2] for m in monkeys]
        tdsts = [m[3] for m in monkeys]
        fdsts = [m[4] for m in monkeys]

        mod = 1
        for d in tests:
            mod *= d

        ins = [0] * len(monkeys)
        for _ in range(rounds):
            for i in range(len(monkeys)):
                q = items[i]
                items[i] = []
                op = ops[i]
                div = tests[i]
                td = tdsts[i]
                fd = fdsts[i]
                for w in q:
                    ins[i] += 1
                    w = op(w)
                    if relief:
                        w //= 3
                    else:
                        w %= mod
                    if w % div == 0:
                        items[td].append(w)
                    else:
                        items[fd].append(w)
        ins.sort(reverse=True)
        return ins[0] * ins[1]

    print(run(20, True))
    print(run(10000, False))

if __name__ == '__main__':
    solve()
