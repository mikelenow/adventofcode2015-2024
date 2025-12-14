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
    val = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

    def from_snafu(s):
        x = 0
        for ch in s:
            x = x * 5 + val[ch]
        return x

    def to_snafu(n):
        if n == 0:
            return '0'
        out = []
        while n != 0:
            n, r = divmod(n, 5)
            if r <= 2:
                out.append('012'[r])
            elif r == 3:
                out.append('=')
                n += 1
            else:
                out.append('-')
                n += 1
        return ''.join(reversed(out))

    total = 0
    for s in lines:
        if s:
            total += from_snafu(s)

    print(to_snafu(total))
    print(0)

if __name__ == '__main__':
    solve()
