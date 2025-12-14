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
    raw = [s for s in lines if s]
    if not raw:
        print(0)
        print(0)
        return

    def parse_num(s):
        out = []
        depth = 0
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == '[':
                depth += 1
                i += 1
            elif ch == ']':
                depth -= 1
                i += 1
            elif ch == ',':
                i += 1
            else:
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                out.append([int(s[i:j]), depth])
                i = j
        return out

    def explode(a):
        for i in range(len(a) - 1):
            v1, d1 = a[i]
            v2, d2 = a[i + 1]
            if d1 > 4 and d1 == d2:
                if i > 0:
                    a[i - 1][0] += v1
                if i + 2 < len(a):
                    a[i + 2][0] += v2
                a[i] = [0, d1 - 1]
                del a[i + 1]
                return True
        return False

    def split(a):
        for i in range(len(a)):
            v, d = a[i]
            if v >= 10:
                left = v // 2
                right = v - left
                a[i] = [left, d + 1]
                a.insert(i + 1, [right, d + 1])
                return True
        return False

    def reduce_num(a):
        while True:
            if explode(a):
                continue
            if split(a):
                continue
            return a

    def add(a, b):
        out = [[v, d + 1] for v, d in a] + [[v, d + 1] for v, d in b]
        return reduce_num(out)

    def magnitude(a):
        a = [[v, d] for v, d in a]
        while len(a) > 1:
            for i in range(len(a) - 1):
                v1, d1 = a[i]
                v2, d2 = a[i + 1]
                if d1 == d2:
                    a[i] = [3 * v1 + 2 * v2, d1 - 1]
                    del a[i + 1]
                    break
        return a[0][0]

    nums = [parse_num(s) for s in raw]
    cur = nums[0]
    for n in nums[1:]:
        cur = add(cur, n)
    part1 = magnitude(cur)

    best = 0
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j:
                continue
            m = magnitude(add([[v, d] for v, d in nums[i]], [[v, d] for v, d in nums[j]]))
            if m > best:
                best = m
    part2 = best

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
