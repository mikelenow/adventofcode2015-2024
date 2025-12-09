
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [list(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    if not lines:
        return

    rows = len(lines)
    cols = len(lines[0])
    
    # Directions: Up, Right, Down, Left
    # Guard facing: ^, >, v, <
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_idx = 0 # Initially facing Up
    
    guard_pos = None
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == '^':
                guard_pos = (r, c)
                dir_idx = 0
            elif lines[r][c] == '>':
                guard_pos = (r, c)
                dir_idx = 1
            elif lines[r][c] == 'v':
                guard_pos = (r, c)
                dir_idx = 2
            elif lines[r][c] == '<':
                guard_pos = (r, c)
                dir_idx = 3
    
    if guard_pos is None:
        print("Guard not found")
        return

    start_pos = guard_pos
    start_dir = dir_idx

    # Part 1: Simulate initial path
    visited_positions = set()
    current_path = [] # To keep order if needed, or just set
    visited_positions.add(guard_pos)
    
    curr_r, curr_c = guard_pos
    curr_dir = start_dir
    
    while True:
        dr, dc = directions[curr_dir]
        next_r, next_c = curr_r + dr, curr_c + dc
        
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            break
            
        if lines[next_r][next_c] == '#':
            curr_dir = (curr_dir + 1) % 4
        else:
            curr_r, curr_c = next_r, next_c
            visited_positions.add((curr_r, curr_c))

    print(f"Result (Part 1): {len(visited_positions)}")

    # Part 2: Check for loops by placing obstructions on visited positions
    loop_count = 0
    candidates = visited_positions - {start_pos}
    
    for i, (or_r, or_c) in enumerate(candidates):
        # Temporarily place obstruction
        lines[or_r][or_c] = '#'
        
        # Fast simulation for loop detection
        sim_r, sim_c = start_pos
        sim_dir = start_dir
        
        visited_states = set()
        # State: (r, c, dir)
        # We only need to store states where we turn or move? 
        # Storing every step is safest.
        
        is_loop = False
        while True:
            # Optimization: 6000 steps is rough upper bound for non-loops usually, 
            # but detection by set is exact.
            state = (sim_r, sim_c, sim_dir)
            if state in visited_states:
                is_loop = True
                break
            visited_states.add(state)
            
            dr, dc = directions[sim_dir]
            nr, nc = sim_r + dr, sim_c + dc
            
            if not (0 <= nr < rows and 0 <= nc < cols):
                break # Left map
                
            if lines[nr][nc] == '#':
                sim_dir = (sim_dir + 1) % 4
            else:
                sim_r, sim_c = nr, nc
        
        if is_loop:
            loop_count += 1
            
        # Remove obstruction
        lines[or_r][or_c] = '.'
    
    print(f"Result (Part 2): {loop_count}")

if __name__ == '__main__':
    solve()
