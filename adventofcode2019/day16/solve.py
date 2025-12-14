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
    s = ''.join(line.strip() for line in lines if line.strip())
    if not s:
        print('')
        print('')
        return

    base = [int(c) for c in s]

    def phase(arr):
        n = len(arr)
        out = [0] * n
        pref = [0] * (n + 1)
        for i, v in enumerate(arr):
            pref[i + 1] = pref[i] + v
        for i in range(n):
            step = i + 1
            total = 0
            j = step - 1
            while j < n:
                end = min(n, j + step)
                total += pref[end] - pref[j]
                j += 2 * step
                if j >= n:
                    break
                end = min(n, j + step)
                total -= pref[end] - pref[j]
                j += 2 * step
            out[i] = abs(total) % 10
        return out

    arr = base[:]
    for _ in range(100):
        arr = phase(arr)
    part1 = ''.join(str(d) for d in arr[:8])

    offset = int(s[:7])
    total_len = len(base) * 10000
    if offset < total_len // 2:
        part2 = ''
    else:
        tail_len = total_len - offset
        tail = [base[(offset + i) % len(base)] for i in range(tail_len)]
        for _ in range(100):
            acc = 0
            for i in range(tail_len - 1, -1, -1):
                acc = (acc + tail[i]) % 10
                tail[i] = acc
        part2 = ''.join(str(d) for d in tail[:8])

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
