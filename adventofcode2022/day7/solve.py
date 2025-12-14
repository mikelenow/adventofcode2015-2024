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
    path = []
    sizes = {}

    def cur_key():
        if not path:
            return '/'
        return '/' + '/'.join(path)

    for s in lines:
        if not s:
            continue
        if s.startswith('$ cd '):
            dst = s[5:]
            if dst == '/':
                path = []
            elif dst == '..':
                if path:
                    path.pop()
            else:
                path.append(dst)
            sizes.setdefault(cur_key(), 0)
        elif s.startswith('$ ls'):
            continue
        elif s.startswith('dir '):
            dname = s[4:]
            k = cur_key()
            child = (k.rstrip('/') + '/' + dname) if k != '/' else '/' + dname
            sizes.setdefault(child, 0)
        else:
            a, _ = s.split(' ', 1)
            if a.isdigit():
                fsz = int(a)
                sizes.setdefault('/', 0)
                sizes['/'] += fsz
                if path:
                    acc = ''
                    for d in path:
                        acc = acc + '/' + d
                        sizes.setdefault(acc, 0)
                        sizes[acc] += fsz

    part1 = sum(v for v in sizes.values() if v <= 100000)

    total = sizes.get('/', 0)
    free = 70000000 - total
    need = 30000000 - free
    if need <= 0:
        part2 = 0
    else:
        part2 = min(v for v in sizes.values() if v >= need)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
