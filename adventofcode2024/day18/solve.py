
import sys
from collections import deque

def can_reach_exit(corrupted, width, height):
    """Check if exit is reachable with given corrupted positions."""
    start = (0, 0)
    end = (width - 1, height - 1)
    
    q = deque([start])
    visited = set([start])
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while q:
        curr_x, curr_y = q.popleft()
        
        if (curr_x, curr_y) == end:
            return True
            
        for dx, dy in directions:
            nx, ny = curr_x + dx, curr_y + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))
    
    return False

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

    # Determine grid size and bytes to fall based on filename/mode
    if 'test' in filename:
        WIDTH, HEIGHT = 7, 7
        BYTES_TO_FALL = 12
    else:
        WIDTH, HEIGHT = 71, 71
        BYTES_TO_FALL = 1024
    
    # Parse all byte positions
    all_bytes = []
    for line in lines:
        x, y = map(int, line.split(','))
        all_bytes.append((x, y))
    
    # Part 1: Find shortest path after BYTES_TO_FALL bytes
    corrupted = set(all_bytes[:BYTES_TO_FALL])
    
    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)
    
    q = deque([(start, 0)])
    visited = set([start])
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    steps_taken = -1
    
    while q:
        (curr_x, curr_y), steps = q.popleft()
        
        if (curr_x, curr_y) == end:
            steps_taken = steps
            break
            
        for dx, dy in directions:
            nx, ny = curr_x + dx, curr_y + dy
            
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append(((nx, ny), steps + 1))
                    
    print(f"Part 1: {steps_taken}")
    
    # Part 2: Binary search for first blocking byte
    left, right = BYTES_TO_FALL, len(all_bytes) - 1
    first_blocking = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Test if path exists with first 'mid' bytes fallen
        corrupted_test = set(all_bytes[:mid + 1])
        
        if can_reach_exit(corrupted_test, WIDTH, HEIGHT):
            # Path still exists, try more bytes
            left = mid + 1
        else:
            # Path blocked, this might be the answer
            first_blocking = mid
            right = mid - 1
    
    if first_blocking != -1:
        blocking_byte = all_bytes[first_blocking]
        print(f"Part 2: {blocking_byte[0]},{blocking_byte[1]}")

if __name__ == '__main__':
    solve()
