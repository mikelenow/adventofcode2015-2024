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
        print("Part 1: ")
        print("Part 2: 0")
        return

    from collections import defaultdict, Counter

    weights = {}
    children = defaultdict(list)
    all_children = set()

    for line in lines:
        if not line:
            continue
        parts = line.split("->")
        left = parts[0].strip()
        name, w = left.split()[0], left.split()[1]
        w = int(w.strip("()"))
        weights[name] = w

        if len(parts) > 1:
            child_names = [c.strip() for c in parts[1].split(",")]
            children[name].extend(child_names)
            all_children.update(child_names)

    all_nodes = set(weights.keys())
    roots = list(all_nodes - all_children)
    root = roots[0] if roots else ""

    corrected = None

    def total_weight(node):
        nonlocal corrected
        w = weights[node]
        if node not in children or not children[node]:
            return w

        child_totals = [total_weight(c) for c in children[node]]
        if corrected is None:
            counter = Counter(child_totals)
            if len(counter) > 1:
                common_weight = counter.most_common(1)[0][0]
                odd_weight = None
                for val, cnt in counter.items():
                    if val != common_weight and cnt == 1:
                        odd_weight = val
                        break
                if odd_weight is not None:
                    idx = child_totals.index(odd_weight)
                    bad_child = children[node][idx]
                    diff = common_weight - odd_weight
                    corrected = weights[bad_child] + diff
        return w + sum(child_totals)

    if root:
        total_weight(root)

    print(f"Part 1: {root}")
    print(f"Part 2: {corrected if corrected is not None else 0}")

if __name__ == '__main__':
    solve()
