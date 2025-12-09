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
    prog = [line.split() for line in lines if line]

    from collections import defaultdict, deque

    def get_val(regs, x):
        if x.lstrip('-').isdigit():
            return int(x)
        return regs[x]

    # Part 1
    regs1 = defaultdict(int)
    ip = 0
    last_sound = 0
    part1 = 0
    while 0 <= ip < len(prog):
        inst = prog[ip]
        op = inst[0]
        x = inst[1]
        y = inst[2] if len(inst) > 2 else None

        if op == 'snd':
            last_sound = get_val(regs1, x)
        elif op == 'set':
            regs1[x] = get_val(regs1, y)
        elif op == 'add':
            regs1[x] += get_val(regs1, y)
        elif op == 'mul':
            regs1[x] *= get_val(regs1, y)
        elif op == 'mod':
            regs1[x] %= get_val(regs1, y)
        elif op == 'rcv':
            if get_val(regs1, x) != 0:
                part1 = last_sound
                break
        elif op == 'jgz':
            if get_val(regs1, x) > 0:
                ip += get_val(regs1, y)
                continue
        ip += 1

    # Part 2
    regs = [defaultdict(int), defaultdict(int)]
    regs[0]['p'] = 0
    regs[1]['p'] = 1
    ips = [0, 0]
    queues = [deque(), deque()]
    blocked = [False, False]
    terminated = [False, False]
    send_count1 = 0

    def step(pid):
        nonlocal send_count1
        if terminated[pid]:
            return
        if not (0 <= ips[pid] < len(prog)):
            terminated[pid] = True
            return
        inst = prog[ips[pid]]
        op = inst[0]
        x = inst[1]
        y = inst[2] if len(inst) > 2 else None

        if op == 'snd':
            val = get_val(regs[pid], x)
            queues[1 - pid].append(val)
            if pid == 1:
                send_count1 += 1
            ips[pid] += 1
            blocked[pid] = False
        elif op == 'set':
            regs[pid][x] = get_val(regs[pid], y)
            ips[pid] += 1
            blocked[pid] = False
        elif op == 'add':
            regs[pid][x] += get_val(regs[pid], y)
            ips[pid] += 1
            blocked[pid] = False
        elif op == 'mul':
            regs[pid][x] *= get_val(regs[pid], y)
            ips[pid] += 1
            blocked[pid] = False
        elif op == 'mod':
            regs[pid][x] %= get_val(regs[pid], y)
            ips[pid] += 1
            blocked[pid] = False
        elif op == 'rcv':
            if queues[pid]:
                regs[pid][x] = queues[pid].popleft()
                ips[pid] += 1
                blocked[pid] = False
            else:
                blocked[pid] = True
        elif op == 'jgz':
            if get_val(regs[pid], x) > 0:
                ips[pid] += get_val(regs[pid], y)
            else:
                ips[pid] += 1
            blocked[pid] = False

    while True:
        prev_blocked = blocked[:]
        prev_queues = (len(queues[0]), len(queues[1]))
        step(0)
        step(1)
        if (terminated[0] or blocked[0]) and (terminated[1] or blocked[1]) and not queues[0] and not queues[1]:
            break

    part2 = send_count1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
