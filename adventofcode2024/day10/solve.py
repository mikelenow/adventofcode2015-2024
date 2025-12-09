
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

    grid = []
    trailheads = []
    
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line):
            if char.isdigit():
                val = int(char)
                row.append(val)
                if val == 0:
                    trailheads.append((r, c))
            else:
                row.append(-1) # impassable
        grid.append(row)
        
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    total_score = 0
    total_rating = 0
    
    # Memoization for distinct paths (Part 2)
    memo_paths = {}

    def count_paths(r, c):
        if (r, c) in memo_paths:
            return memo_paths[(r, c)]
        
        h = grid[r][c]
        if h == 9:
            return 1
            
        paths = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == h + 1:
                    paths += count_paths(nr, nc)
                    
        memo_paths[(r, c)] = paths
        return paths

    for tr, tc in trailheads:
        # Part 1: Reachable 9s (BFS/DFS)
        reachable_nines = set()
        q_bfs = deque([(tr, tc)])
        seen_bfs = set([(tr, tc)]) 
        
        while q_bfs:
            r, c = q_bfs.popleft()
            h = grid[r][c]
            
            if h == 9:
                reachable_nines.add((r, c))
                continue
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nh = grid[nr][nc]
                    if nh == h + 1:
                        if (nr, nc) not in seen_bfs:
                            seen_bfs.add((nr, nc))
                            q_bfs.append((nr, nc))
                            
        total_score += len(reachable_nines)
        
        # Part 2: Distinct Trails (DFS with memo)
        total_rating += count_paths(tr, tc)

    print(f"Result (Part 1): {total_score}")
    print(f"Result (Part 2): {total_rating}")

if __name__ == '__main__':
    solve()
