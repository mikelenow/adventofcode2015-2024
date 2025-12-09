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

    # Day 14: Reindeer Olympics
    import re

    reindeer = []
    for line in lines:
        match = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.', line)
        if match:
            name = match.group(1)
            speed = int(match.group(2))
            fly_time = int(match.group(3))
            rest_time = int(match.group(4))
            reindeer.append((name, speed, fly_time, rest_time))

    total_time = 2503

    # Part 1: Who travels the farthest?
    distances = []
    for name, speed, fly_time, rest_time in reindeer:
        cycle_time = fly_time + rest_time
        full_cycles = total_time // cycle_time
        remaining = total_time % cycle_time
        distance = full_cycles * speed * fly_time + min(remaining, fly_time) * speed
        distances.append(distance)
    part1 = max(distances)

    # Part 2: Points system
    points = [0] * len(reindeer)
    for t in range(1, total_time + 1):
        distances = []
        for name, speed, fly_time, rest_time in reindeer:
            cycle_time = fly_time + rest_time
            full_cycles = t // cycle_time
            remaining = t % cycle_time
            distance = full_cycles * speed * fly_time + min(remaining, fly_time) * speed
            distances.append(distance)
        max_dist = max(distances)
        for i in range(len(reindeer)):
            if distances[i] == max_dist:
                points[i] += 1
    part2 = max(points)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
