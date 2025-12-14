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
    exprs = [s.replace(' ', '') for s in lines if s]
    if not exprs:
        print(0)
        print(0)
        return

    def parse_num(s, i):
        j = i
        while j < len(s) and s[j].isdigit():
            j += 1
        return int(s[i:j]), j

    def eval_lr(s):
        def atom(i):
            if s[i] == '(':
                v, j = expr(i + 1)
                return v, j + 1
            return parse_num(s, i)

        def expr(i):
            v, i = atom(i)
            while i < len(s) and s[i] != ')':
                op = s[i]
                rhs, i = atom(i + 1)
                if op == '+':
                    v += rhs
                else:
                    v *= rhs
            return v, i

        return expr(0)[0]

    def eval_add_first(s):
        def atom(i):
            if s[i] == '(':
                v, j = expr(i + 1)
                return v, j + 1
            return parse_num(s, i)

        def term(i):
            v, i = atom(i)
            while i < len(s) and s[i] == '+':
                rhs, i = atom(i + 1)
                v += rhs
            return v, i

        def expr(i):
            v, i = term(i)
            while i < len(s) and s[i] != ')':
                if s[i] == '*':
                    rhs, i = term(i + 1)
                    v *= rhs
                else:
                    break
            return v, i

        return expr(0)[0]

    part1 = sum(eval_lr(s) for s in exprs)
    part2 = sum(eval_add_first(s) for s in exprs)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
