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

    records = [line for line in lines if line]
    records.sort()

    sleep = {}  # guard_id -> [60] minute counts
    current_guard = None
    asleep_minute = None

    for rec in records:
        right_bracket = rec.find(']')
        minute = int(rec[15:17])
        action = rec[right_bracket + 2:]

        if action.startswith('Guard #'):
            guard_id = int(action.split('#')[1].split()[0])
            current_guard = guard_id
            if current_guard not in sleep:
                sleep[current_guard] = [0] * 60
            asleep_minute = None
        elif action == 'falls asleep':
            asleep_minute = minute
        elif action == 'wakes up':
            if current_guard is None or asleep_minute is None:
                continue
            for m in range(asleep_minute, minute):
                sleep[current_guard][m] += 1
            asleep_minute = None

    # Part 1
    best_guard = None
    best_total = -1
    for guard_id, minutes in sleep.items():
        total = sum(minutes)
        if total > best_total:
            best_total = total
            best_guard = guard_id

    best_minute = 0
    if best_guard is not None:
        minutes = sleep[best_guard]
        best_minute = max(range(60), key=lambda m: minutes[m])
    part1 = (best_guard or 0) * best_minute

    # Part 2
    best_guard2 = 0
    best_minute2 = 0
    best_count = -1
    for guard_id, minutes in sleep.items():
        for m, cnt in enumerate(minutes):
            if cnt > best_count:
                best_count = cnt
                best_guard2 = guard_id
                best_minute2 = m
    part2 = best_guard2 * best_minute2

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
