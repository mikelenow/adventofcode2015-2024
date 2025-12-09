
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

    if not lines:
        print("Empty input file.")
        return

    grid = lines
    rows = len(grid)
    cols = len(grid[0])
    target = "XMAS"
    target_len = len(target)
    count = 0

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Right
        (0, -1),  # Left
        (1, 0),   # Down
        (-1, 0),  # Up
        (1, 1),   # Down-Right
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
        (-1, -1)  # Up-Left
    ]

    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                # Check bounds for end of word
                end_r = r + (target_len - 1) * dr
                end_c = c + (target_len - 1) * dc
                
                if 0 <= end_r < rows and 0 <= end_c < cols:
                    match = True
                    for k in range(target_len):
                        if grid[r + k*dr][c + k*dc] != target[k]:
                            match = False
                            break
                    if match:
                        count += 1
    
    print(f"Result (Part 1): {count}")

    # Part 2: Find "X-MAS"
    # Look for 'A' as the center of the X
    count_x_mas = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] == 'A':
                # Check diagonal 1: Top-Left to Bottom-Right
                tl = grid[r-1][c-1]
                br = grid[r+1][c+1]
                diag1_valid = (tl == 'M' and br == 'S') or (tl == 'S' and br == 'M')

                # Check diagonal 2: Top-Right to Bottom-Left
                tr = grid[r-1][c+1]
                bl = grid[r+1][c-1]
                diag2_valid = (tr == 'M' and bl == 'S') or (tr == 'S' and bl == 'M')

                if diag1_valid and diag2_valid:
                    count_x_mas += 1
    
    print(f"Result (Part 2): {count_x_mas}")

if __name__ == '__main__':
    solve()
