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

    import re
    from collections import defaultdict

    bots = defaultdict(list)
    outputs = defaultdict(list)
    rules = {}
    part1_answer = None

    for line in lines:
        if line.startswith('value'):
            match = re.match(r'value (\d+) goes to bot (\d+)', line)
            if match:
                value, bot = map(int, match.groups())
                bots[bot].append(value)
        elif line.startswith('bot'):
            match = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', line)
            if match:
                bot = int(match.group(1))
                low_type, low_dest = match.group(2), int(match.group(3))
                high_type, high_dest = match.group(4), int(match.group(5))
                rules[bot] = ((low_type, low_dest), (high_type, high_dest))

    while True:
        ready_bots = [b for b in bots if len(bots[b]) == 2]
        if not ready_bots:
            break

        for bot in ready_bots:
            low_val = min(bots[bot])
            high_val = max(bots[bot])
            bots[bot] = []

            if {low_val, high_val} == {17, 61}:
                part1_answer = bot

            if bot in rules:
                low_rule, high_rule = rules[bot]
                if low_rule[0] == 'bot':
                    bots[low_rule[1]].append(low_val)
                else:
                    outputs[low_rule[1]].append(low_val)

                if high_rule[0] == 'bot':
                    bots[high_rule[1]].append(high_val)
                else:
                    outputs[high_rule[1]].append(high_val)

    part2 = outputs[0][0] * outputs[1][0] * outputs[2][0]

    print(f"Part 1: {part1_answer}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
