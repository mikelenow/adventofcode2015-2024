
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
    
    # Find start and end
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    
    # BFS to find distances from start to all positions
    def bfs_distances(start_pos):
        distances = {}
        q = deque([(start_pos, 0)])
        distances[start_pos] = 0
        
        while q:
            (r, c), dist = q.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] != '#' and (nr, nc) not in distances:
                        distances[(nr, nc)] = dist + 1
                        q.append(((nr, nc), dist + 1))
        
        return distances
    
    # Get distances from start
    dist_from_start = bfs_distances(start)
    
    # Normal path length (no cheating)
    normal_time = dist_from_start[end]
    
    # Find all valid track positions
    track_positions = list(dist_from_start.keys())
    
    def count_cheats(max_cheat_time, min_savings):
        """Count cheats with given max duration that save at least min_savings."""
        cheats = {}
        
        for start_pos in track_positions:
            r1, c1 = start_pos
            start_dist = dist_from_start[start_pos]
            
            # Try all positions within Manhattan distance of max_cheat_time
            for dr in range(-max_cheat_time, max_cheat_time + 1):
                for dc in range(-max_cheat_time, max_cheat_time + 1):
                    manhattan = abs(dr) + abs(dc)
                    if manhattan == 0 or manhattan > max_cheat_time:
                        continue
                    
                    r2, c2 = r1 + dr, c1 + dc
                    end_pos = (r2, c2)
                    
                    # Check if end position is valid track
                    if end_pos not in dist_from_start:
                        continue
                    
                    # Calculate time with this cheat
                    end_dist = dist_from_start[end_pos]
                    cheat_time = start_dist + manhattan + (normal_time - end_dist)
                    saved = normal_time - cheat_time
                    
                    if saved >= min_savings:
                        cheat_key = (start_pos, end_pos)
                        if cheat_key not in cheats or saved > cheats[cheat_key]:
                            cheats[cheat_key] = saved
        
        return len(cheats)
    
    # Part 1: 2-picosecond cheats
    threshold1 = 100 if 'test' not in filename else 1
    count1 = count_cheats(2, threshold1)
    print(f"Part 1: {count1}")
    
    # Part 2: up to 20-picosecond cheats
    threshold2 = 100 if 'test' not in filename else 50
    count2 = count_cheats(20, threshold2)
    print(f"Part 2: {count2}")

if __name__ == '__main__':
    solve()
