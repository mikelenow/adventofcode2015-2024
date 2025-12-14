import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n\r') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    i = 0
    drawing = []
    while i < len(lines) and lines[i] != '':
        drawing.append(lines[i])
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1
    moves = [s for s in lines[i:] if s.strip() != '']

    if not drawing:
        print('')
        print('')
        return

    idx_line = drawing[-1]
    n_stacks = max(int(x) for x in idx_line.split() if x.isdigit())
    stacks0 = [[] for _ in range(n_stacks)]

    for row in reversed(drawing[:-1]):
        for si in range(n_stacks):
            col = 1 + 4 * si
            if col < len(row):
                ch = row[col]
                if ch != ' ':
                    stacks0[si].append(ch)

    def run(part2):
        stacks = [s[:] for s in stacks0]
        for m in moves:
            if not m.startswith('move '):
                continue
            parts = m.split()
            cnt = int(parts[1])
            src = int(parts[3]) - 1
            dst = int(parts[5]) - 1

            if part2:
                buf = stacks[src][-cnt:]
                del stacks[src][-cnt:]
                stacks[dst].extend(buf)
            else:
                for _ in range(cnt):
                    stacks[dst].append(stacks[src].pop())

        out = []
        for s in stacks:
            out.append(s[-1] if s else '')
        return ''.join(out)

    print(run(False))
    print(run(True))

if __name__ == '__main__':
    solve()
