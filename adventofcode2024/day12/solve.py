
import sys
from collections import deque

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

    grid = lines
    rows = len(grid)
    cols = len(grid[0])
    
    print(f"Grid: {rows}x{cols}")
    
    visited = set()
    total_price1 = 0
    total_price2 = 0
    total_area = 0
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    loop_count = 0
    
    for r in range(rows):
        for c in range(cols):
            loop_count += 1
            if (r, c) in visited:
                continue
            
            plant = grid[r][c]
            
            # BFS
            region = set()
            region.add((r, c))
            visited.add((r, c))
            q = deque([(r, c)])
            
            area = 0
            perimeter = 0
            corners = 0
            
            while q:
                curr_r, curr_c = q.popleft()
                
                # Process neighbors for BFS
                for dr, dc in directions:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == plant:
                            if (nr, nc) not in visited:
                                visited.add((nr, nc))
                                region.add((nr, nc))
                                q.append((nr, nc))
            
            # Region complete. Calculate stats.
            area = len(region)
            total_area += area
            
            # Calculate Perimeter & Corners by iterating nodes in region
            for rr, cc in region:
                # Perimeter
                for dr, dc in directions:
                    nr, nc = rr + dr, cc + dc
                    if (nr, nc) not in region:
                        perimeter += 1
                        
                # Corners (Part 2)
                # U, R
                u = (rr - 1, cc) in region
                r_side = (rr, cc + 1) in region
                ur = (rr - 1, cc + 1) in region
                if not u and not r_side: corners += 1
                if u and r_side and not ur: corners += 1
                
                # R, D
                d = (rr + 1, cc) in region
                dr_node = (rr + 1, cc + 1) in region
                if not r_side and not d: corners += 1
                if r_side and d and not dr_node: corners += 1
                
                # D, L
                l = (rr, cc - 1) in region
                dl = (rr + 1, cc - 1) in region
                if not d and not l: corners += 1
                if d and l and not dl: corners += 1
                
                # L, U
                ul = (rr - 1, cc - 1) in region
                if not l and not u: corners += 1
                if l and u and not ul: corners += 1
                
            total_price1 += area * perimeter
            total_price2 += area * corners
            
    print(f"Loops: {loop_count}")
    print(f"Total Area: {total_area}")
    print(f"Result (Part 1): {total_price1}")
    print(f"Result (Part 2): {total_price2}")

if __name__ == '__main__':
    solve()
