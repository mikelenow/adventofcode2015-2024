import sys
import re

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
    mem1 = {}
    mem2 = {}
    mem_re = re.compile(r'^mem\[(\d+)\] = (\d+)$')

    and_mask = (1 << 36) - 1
    or_mask = 0
    ones_mask = 0
    floating_mask = 0
    floating_subsets = [0]

    for s in lines:
        if not s:
            continue
        if s.startswith('mask = '):
            mask = s.split('=', 1)[1].strip()

            and_mask = (1 << 36) - 1
            or_mask = 0
            ones_mask = 0
            floating_mask = 0
            floating_bits = []
            for i, ch in enumerate(mask):
                bit = 1 << (35 - i)
                if ch == '0':
                    and_mask &= ~bit
                elif ch == '1':
                    or_mask |= bit
                    ones_mask |= bit
                else:
                    floating_bits.append(bit)
                    floating_mask |= bit

            floating_subsets = [0]
            for bit in floating_bits:
                floating_subsets = floating_subsets + [v | bit for v in floating_subsets]
            continue
        m = mem_re.match(s)
        if not m:
            continue
        addr = int(m.group(1))
        val = int(m.group(2))
        mem1[addr] = (val & and_mask) | or_mask

        base = (addr | ones_mask) & ~floating_mask
        for sub in floating_subsets:
            mem2[base | sub] = val

    print(sum(mem1.values()))
    print(sum(mem2.values()))

if __name__ == '__main__':
    solve()
