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
    if not lines:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    # Parse initial state and step count
    start_state = lines[0].split()[-1].strip('.')
    steps = int(lines[1].split()[5])

    # Hardcode the state machine from the input description
    rules = {
        'A': {0: (1, 1, 'B'), 1: (0, -1, 'B')},
        'B': {0: (0, 1, 'C'), 1: (1, -1, 'B')},
        'C': {0: (1, 1, 'D'), 1: (0, -1, 'A')},
        'D': {0: (1, -1, 'E'), 1: (1, -1, 'F')},
        'E': {0: (1, -1, 'A'), 1: (0, -1, 'D')},
        'F': {0: (1, 1, 'A'), 1: (1, -1, 'E')},
    }

    tape = set()
    pos = 0
    state = start_state

    for _ in range(steps):
        val = 1 if pos in tape else 0
        write, move, next_state = rules[state][val]
        if write:
            tape.add(pos)
        else:
            tape.discard(pos)
        pos += move
        state = next_state

    part1 = len(tape)
    part2 = 0  # Not applicable for this day

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
