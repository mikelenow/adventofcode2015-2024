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
    line = ''
    for s in lines:
        if s:
            line = s
            break
    if not line:
        print(0)
        print(0)
        return

    program = [int(x) for x in line.split(',')]

    class VM:
        def __init__(self, prog):
            self.mem = {i: v for i, v in enumerate(prog)}
            self.ip = 0
            self.rb = 0
            self.inputs = []
            self.halted = False

        def clone(self):
            other = VM([])
            other.mem = dict(self.mem)
            other.ip = self.ip
            other.rb = self.rb
            other.inputs = list(self.inputs)
            other.halted = self.halted
            return other

        def r(self, a):
            return self.mem.get(a, 0)

        def w(self, a, v):
            self.mem[a] = v

        def add_input(self, v):
            self.inputs.append(v)

        def run_until_output(self):
            def get(mode, param):
                if mode == 0:
                    return self.r(param)
                if mode == 1:
                    return param
                if mode == 2:
                    return self.r(self.rb + param)
                raise ValueError(mode)

            def addr(mode, param):
                if mode == 0:
                    return param
                if mode == 2:
                    return self.rb + param
                raise ValueError(mode)

            while True:
                instr = self.r(self.ip)
                op = instr % 100
                m1 = (instr // 100) % 10
                m2 = (instr // 1000) % 10
                m3 = (instr // 10000) % 10
                if op == 99:
                    self.halted = True
                    return None
                if op in (1, 2, 7, 8):
                    a = self.r(self.ip + 1)
                    b = self.r(self.ip + 2)
                    c = self.r(self.ip + 3)
                    va = get(m1, a)
                    vb = get(m2, b)
                    dest = addr(m3, c)
                    if op == 1:
                        self.w(dest, va + vb)
                    elif op == 2:
                        self.w(dest, va * vb)
                    elif op == 7:
                        self.w(dest, 1 if va < vb else 0)
                    else:
                        self.w(dest, 1 if va == vb else 0)
                    self.ip += 4
                elif op == 3:
                    if not self.inputs:
                        return None
                    a = self.r(self.ip + 1)
                    self.w(addr(m1, a), self.inputs.pop(0))
                    self.ip += 2
                elif op == 4:
                    a = self.r(self.ip + 1)
                    self.ip += 2
                    return get(m1, a)
                elif op in (5, 6):
                    a = self.r(self.ip + 1)
                    b = self.r(self.ip + 2)
                    va = get(m1, a)
                    vb = get(m2, b)
                    if (op == 5 and va != 0) or (op == 6 and va == 0):
                        self.ip = vb
                    else:
                        self.ip += 3
                elif op == 9:
                    a = self.r(self.ip + 1)
                    self.rb += get(m1, a)
                    self.ip += 2
                else:
                    raise ValueError(op)

    from collections import deque

    moves = {
        1: (0, -1),
        2: (0, 1),
        3: (-1, 0),
        4: (1, 0),
    }

    start_vm = VM(program)
    start = (0, 0)
    q = deque([(start, start_vm, 0)])
    seen = {start}
    grid = {start: 1}
    oxygen = None
    dist_to_oxygen = None

    while q:
        (x, y), vm, d = q.popleft()
        for cmd, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen:
                continue
            nvm = vm.clone()
            nvm.add_input(cmd)
            out = nvm.run_until_output()
            if out is None:
                continue
            if out == 0:
                seen.add((nx, ny))
                grid[(nx, ny)] = 0
                continue
            seen.add((nx, ny))
            grid[(nx, ny)] = 1
            if out == 2:
                oxygen = (nx, ny)
                if dist_to_oxygen is None:
                    dist_to_oxygen = d + 1
            q.append(((nx, ny), nvm, d + 1))

    if oxygen is None:
        print(0)
        print(0)
        return

    def bfs_from(src):
        qq = deque([(src, 0)])
        dist = {src: 0}
        while qq:
            (x, y), dd = qq.popleft()
            for dx, dy in moves.values():
                nx, ny = x + dx, y + dy
                if grid.get((nx, ny), 0) == 0:
                    continue
                if (nx, ny) in dist:
                    continue
                dist[(nx, ny)] = dd + 1
                qq.append(((nx, ny), dd + 1))
        return dist

    dist_map = bfs_from(oxygen)
    part1 = dist_to_oxygen if dist_to_oxygen is not None else dist_map.get(start, 0)
    part2 = max(dist_map.values()) if dist_map else 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
