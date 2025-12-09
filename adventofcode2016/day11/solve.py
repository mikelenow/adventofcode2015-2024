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

    from collections import deque
    from itertools import combinations

    # Parse input: Po-G, Th-G, Th-M, Pm-G, Ru-G, Ru-M, Co-G, Co-M on floor 1
    # Po-M, Pm-M on floor 2
    initial_state = (
        frozenset(['PoG', 'ThG', 'ThM', 'PmG', 'RuG', 'RuM', 'CoG', 'CoM']),
        frozenset(['PoM', 'PmM']),
        frozenset(),
        frozenset()
    )

    def is_safe(floor):
        if not floor:
            return True
        generators = {item[:-1] for item in floor if item.endswith('G')}
        microchips = {item[:-1] for item in floor if item.endswith('M')}
        if not generators:
            return True
        for chip in microchips:
            if chip not in generators:
                return False
        return True

    def is_valid_state(floors):
        return all(is_safe(floor) for floor in floors)

    def solve_rtg(initial):
        queue = deque([(0, initial, 0)])
        visited = {(0, initial)}

        while queue:
            elevator, floors, steps = queue.popleft()

            if all(len(floor) == 0 for floor in floors[:3]):
                return steps

            current_floor = floors[elevator]
            for num_items in [2, 1]:
                for items in combinations(current_floor, num_items):
                    items_set = set(items)
                    for direction in [-1, 1]:
                        new_elevator = elevator + direction
                        if not (0 <= new_elevator < 4):
                            continue

                        new_floors = list(floors)
                        new_floors[elevator] = frozenset(current_floor - items_set)
                        new_floors[new_elevator] = frozenset(floors[new_elevator] | items_set)
                        new_floors = tuple(new_floors)

                        if not is_valid_state(new_floors):
                            continue

                        state = (new_elevator, new_floors)
                        if state not in visited:
                            visited.add(state)
                            queue.append((new_elevator, new_floors, steps + 1))

        return -1

    part1 = solve_rtg(initial_state)

    # Part 2: Add elerium and dilithium generators and microchips to floor 1
    initial_state_part2 = (
        frozenset(['PoG', 'ThG', 'ThM', 'PmG', 'RuG', 'RuM', 'CoG', 'CoM', 'ElG', 'ElM', 'DiG', 'DiM']),
        frozenset(['PoM', 'PmM']),
        frozenset(),
        frozenset()
    )
    part2 = solve_rtg(initial_state_part2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
