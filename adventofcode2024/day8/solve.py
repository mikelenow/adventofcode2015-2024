
import sys
from collections import defaultdict

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    grid = lines
    rows = len(grid)
    cols = len(grid[0])
    
    antennas = defaultdict(list)
    
    for r in range(rows):
        for c in range(cols):
            char = grid[r][c]
            if char != '.':
                antennas[char].append((r, c))
                
    antinodes_part1 = set()
    antinodes_part2 = set()
    
    for char, coords in antennas.items():
        n = len(coords)
        if n < 2:
            continue
            
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                r1, c1 = coords[i]
                r2, c2 = coords[j]
                
                # Part 1 Logic
                dr = r2 - r1
                dc = c2 - c1
                
                an_r = r2 + dr
                an_c = c2 + dc
                
                if 0 <= an_r < rows and 0 <= an_c < cols:
                    antinodes_part1.add((an_r, an_c))
                    
                # Part 2 Logic (Resonant Harmonics)
                # Add all points on the line: A1 + k*vec, where k is any integer
                # Actually, iterate both directions from A1 until out of bounds.
                
                # Direction 1: +vec
                curr_r, curr_c = r1, c1
                while 0 <= curr_r < rows and 0 <= curr_c < cols:
                    antinodes_part2.add((curr_r, curr_c))
                    curr_r += dr
                    curr_c += dc
                    
                # Direction 2: -vec
                curr_r, curr_c = r1, c1
                while 0 <= curr_r < rows and 0 <= curr_c < cols:
                    antinodes_part2.add((curr_r, curr_c))
                    curr_r -= dr
                    curr_c -= dc

    print(f"Result (Part 1): {len(antinodes_part1)}")
    print(f"Result (Part 2): {len(antinodes_part2)}")

if __name__ == '__main__':
    solve()
