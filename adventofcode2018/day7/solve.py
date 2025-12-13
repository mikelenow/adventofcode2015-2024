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

    edges = []
    nodes = set()
    for line in lines:
        if not line:
            continue
        # "Step C must be finished before step A can begin."
        a = line[5]
        b = line[36]
        edges.append((a, b))
        nodes.add(a)
        nodes.add(b)

    prereq = {n: set() for n in nodes}
    outgoing = {n: set() for n in nodes}
    for a, b in edges:
        prereq[b].add(a)
        outgoing[a].add(b)

    # Part 1: lexicographically smallest topological order
    done = set()
    available = sorted([n for n in nodes if not prereq[n]])
    order = []
    while available:
        cur = available.pop(0)
        if cur in done:
            continue
        order.append(cur)
        done.add(cur)
        for nxt in outgoing[cur]:
            if nxt in done:
                continue
            if prereq[nxt].issubset(done):
                if nxt not in available:
                    available.append(nxt)
        available.sort()
    part1 = ''.join(order)

    # Part 2: scheduling with 5 workers and base cost 60
    workers = 5
    base = 60

    done = set()
    in_progress = {}  # step -> remaining
    time = 0

    def duration(step: str) -> int:
        return base + (ord(step) - ord('A') + 1)

    while len(done) < len(nodes):
        # Assign work
        free_slots = workers - len(in_progress)
        if free_slots > 0:
            candidates = []
            for n in nodes:
                if n in done or n in in_progress:
                    continue
                if prereq[n].issubset(done):
                    candidates.append(n)
            candidates.sort()
            for n in candidates[:free_slots]:
                in_progress[n] = duration(n)

        # Advance time to next completion
        if not in_progress:
            break
        step_time = min(in_progress.values())
        time += step_time
        finished = []
        for n in list(in_progress.keys()):
            in_progress[n] -= step_time
            if in_progress[n] == 0:
                finished.append(n)
                del in_progress[n]
        for n in sorted(finished):
            done.add(n)

    print(part1)
    print(time)

if __name__ == '__main__':
    solve()
