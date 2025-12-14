import sys
import math

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
    outputs = {}
    types = {}  # name -> 'broadcaster' | '%' | '&' | 'out'
    for line in lines:
        if not line:
            continue
        left, right = line.split('->')
        left = left.strip()
        dests = [x.strip() for x in right.strip().split(',')]
        if left == 'broadcaster':
            name = 'broadcaster'
            types[name] = 'broadcaster'
        else:
            t = left[0]
            name = left[1:]
            types[name] = t
        outputs[name] = dests

    # add sinks
    for src, dests in list(outputs.items()):
        for d in dests:
            if d not in types:
                types[d] = 'out'
                outputs.setdefault(d, [])

    inputs = {name: [] for name in types}
    for src, dests in outputs.items():
        for d in dests:
            inputs[d].append(src)

    ff_state = {name: False for name, t in types.items() if t == '%'}
    conj_mem = {name: {src: False for src in inputs[name]} for name, t in types.items() if t == '&'}

    rx_parent = None
    for src, dests in outputs.items():
        if 'rx' in dests:
            rx_parent = src
            break

    watch_inputs = set(inputs[rx_parent]) if rx_parent is not None else set()
    first_high = {}

    def press(button_idx, count_pulses):
        from collections import deque

        q = deque([('button', 'broadcaster', False)])  # False=low True=high
        while q:
            src, dst, pulse = q.popleft()
            if count_pulses is not None:
                if pulse:
                    count_pulses[1] += 1
                else:
                    count_pulses[0] += 1

            if rx_parent is not None and dst == rx_parent and pulse and src in watch_inputs:
                if src not in first_high:
                    first_high[src] = button_idx

            t = types.get(dst, 'out')
            if t == 'out':
                continue
            if t == 'broadcaster':
                for nd in outputs[dst]:
                    q.append((dst, nd, pulse))
            elif t == '%':
                if pulse:
                    continue
                ff_state[dst] = not ff_state[dst]
                out_pulse = ff_state[dst]
                for nd in outputs[dst]:
                    q.append((dst, nd, out_pulse))
            elif t == '&':
                conj_mem[dst][src] = pulse
                out_pulse = not all(conj_mem[dst].values())
                for nd in outputs[dst]:
                    q.append((dst, nd, out_pulse))

    counts = [0, 0]
    for i in range(1, 1000 + 1):
        press(i, counts)
    part1 = counts[0] * counts[1]

    part2 = 0
    if rx_parent is not None and watch_inputs:
        i = 1000
        while len(first_high) < len(watch_inputs):
            i += 1
            press(i, None)
        vals = list(first_high.values())
        part2 = vals[0]
        for v in vals[1:]:
            part2 = math.lcm(part2, v)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
