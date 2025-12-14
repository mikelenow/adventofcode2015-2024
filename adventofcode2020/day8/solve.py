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

    prog = []
    for s in lines:
        if not s:
            continue
        op, arg = s.split()
        prog.append((op, int(arg)))

    def run(swapped=None):
        acc = 0
        ip = 0
        seen = set()
        n = len(prog)
        while ip not in seen and 0 <= ip <= n:
            if ip == n:
                return True, acc
            seen.add(ip)
            op, arg = prog[ip]
            if swapped == ip:
                if op == 'jmp':
                    op = 'nop'
                elif op == 'nop':
                    op = 'jmp'
            if op == 'acc':
                acc += arg
                ip += 1
            elif op == 'jmp':
                ip += arg
            else:
                ip += 1
        return False, acc

    part1 = run()[1]
    part2 = 0
    for i, (op, _) in enumerate(prog):
        if op not in ('jmp', 'nop'):
            continue
        ok, acc = run(swapped=i)
        if ok:
            part2 = acc
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
