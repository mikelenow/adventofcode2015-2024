
import sys
import heapq

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
    
    start = None
    end = None
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
                
    # Dijkstra with path tracking
    # State: (r, c, direction)
    # direction: 0=East, 1=South, 2=West, 3=North
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Priority Queue: (score, r, c, dir)
    pq = [(0, start[0], start[1], 0)]
    
    # Track minimum score to reach each state
    dist = {}
    dist[(start[0], start[1], 0)] = 0
    
    # Track all parent states for each state (for backtracking)
    parents = {}
    
    while pq:
        score, r, c, d = heapq.heappop(pq)
        
        # Skip if we've found a better path to this state
        if score > dist.get((r, c, d), float('inf')):
            continue
        
        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        
        # Check bounds for nr, nc
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue # Skip if out of bounds
            
        if grid[nr][nc] != '#':
            new_score = score + 1
            state = (nr, nc, d)
            
            if new_score < dist.get(state, float('inf')):
                dist[state] = new_score
                parents[state] = [(r, c, d)]
                heapq.heappush(pq, (new_score, nr, nc, d))
            elif new_score == dist.get(state, float('inf')):
                if state not in parents:
                    parents[state] = []
                parents[state].append((r, c, d))
        
        # Try rotating clockwise
        nd = (d + 1) % 4
        new_score = score + 1000
        state = (r, c, nd)
        
        if new_score < dist.get(state, float('inf')):
            dist[state] = new_score
            parents[state] = [(r, c, d)]
            heapq.heappush(pq, (new_score, r, c, nd))
        elif new_score == dist.get(state, float('inf')):
            if state not in parents:
                parents[state] = []
            parents[state].append((r, c, d))
        
        # Try rotating counter-clockwise
        nd = (d - 1 + 4) % 4 # Ensure positive modulo for negative numbers
        new_score = score + 1000
        state = (r, c, nd)
        
        if new_score < dist.get(state, float('inf')):
            dist[state] = new_score
            parents[state] = [(r, c, d)]
            heapq.heappush(pq, (new_score, r, c, nd))
        elif new_score == dist.get(state, float('inf')):
            if state not in parents:
                parents[state] = []
            parents[state].append((r, c, d))
    
    # Find minimum score to reach end
    min_score = float('inf')
    end_states = []
    for d in range(4):
        if (end[0], end[1], d) in dist:
            score = dist[(end[0], end[1], d)]
            if score < min_score:
                min_score = score
                end_states = [(end[0], end[1], d)]
            elif score == min_score:
                end_states.append((end[0], end[1], d))
    
    print(f"Result (Part 1): {min_score}")
    
    # Part 2: Backtrack from all optimal end states to find all tiles on optimal paths
    tiles_on_path = set()
    visited_states = set()
    stack = list(end_states)
    
    while stack:
        state = stack.pop()
        
        if state in visited_states:
            continue
        visited_states.add(state)
        
        r, c, d = state
        tiles_on_path.add((r, c))
        
        if state in parents:
            for parent in parents[state]:
                if parent not in visited_states:
                    stack.append(parent)
    
    print(f"Result (Part 2): {len(tiles_on_path)}")


if __name__ == '__main__':
    solve()
