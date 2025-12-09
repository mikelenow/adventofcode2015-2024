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

    # Day 9: All in a Single Night
    # Traveling salesman problem - find shortest and longest routes

    from itertools import permutations

    distances = {}
    cities = set()

    for line in lines:
        parts = line.split(' = ')
        dist = int(parts[1])
        city_parts = parts[0].split(' to ')
        city1, city2 = city_parts[0], city_parts[1]
        cities.add(city1)
        cities.add(city2)
        distances[(city1, city2)] = dist
        distances[(city2, city1)] = dist

    min_distance = float('inf')
    max_distance = 0

    for perm in permutations(cities):
        total = sum(distances[(perm[i], perm[i+1])] for i in range(len(perm)-1))
        min_distance = min(min_distance, total)
        max_distance = max(max_distance, total)

    print(f"Part 1: {min_distance}")
    print(f"Part 2: {max_distance}")

if __name__ == '__main__':
    solve()
