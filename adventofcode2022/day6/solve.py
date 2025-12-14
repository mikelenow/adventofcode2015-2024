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
    s = ''
    for line in lines:
        if line:
            s = line
            break

    def first_unique(k):
        if k <= 0:
            return 0
        cnt = {}
        dup = 0
        for i, ch in enumerate(s):
            prev = cnt.get(ch, 0)
            cnt[ch] = prev + 1
            if prev == 1:
                dup += 1
            if i >= k:
                old = s[i - k]
                prev2 = cnt[old]
                if prev2 == 2:
                    dup -= 1
                if prev2 == 1:
                    del cnt[old]
                else:
                    cnt[old] = prev2 - 1
            if i >= k - 1 and dup == 0 and len(cnt) == k:
                return i + 1
        return 0

    print(first_unique(4))
    print(first_unique(14))

if __name__ == '__main__':
    solve()
