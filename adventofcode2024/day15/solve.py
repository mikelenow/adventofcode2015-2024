
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    parts = content.strip().split('\n\n')
    grid_lines = parts[0].split('\n')
    moves = "".join(parts[1].split()) # Join multiple lines of moves
    
    def solv_part1(input_grid, moves):
        # ... logic mostly same as before, copied here or updated ...
        grid = [list(line) for line in input_grid]
        rows = len(grid)
        cols = len(grid[0])
        
        robot_pos = None
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    robot_pos = (r, c)
                    grid[r][c] = '.'
                    break
        
        directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        rr, rc = robot_pos
        
        for move in moves:
            dr, dc = directions[move]
            nr, nc = rr + dr, rc + dc
            if grid[nr][nc] == '#': continue
            if grid[nr][nc] == '.':
                rr, rc = nr, nc
                continue
            if grid[nr][nc] == 'O':
                cr, cc = nr, nc
                while grid[cr][cc] == 'O':
                    cr += dr
                    cc += dc
                if grid[cr][cc] == '#': continue
                # Push
                grid[cr][cc] = 'O'
                grid[nr][nc] = '.'
                rr, rc = nr, nc
        
        total = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 'O': total += 100 * r + c
        return total

    def solv_part2(input_grid, moves):
        # Expansion
        grid = []
        for line in input_grid:
            new_line = []
            for char in line:
                if char == '#': new_line.extend(['#', '#'])
                elif char == 'O': new_line.extend(['[', ']'])
                elif char == '.': new_line.extend(['.', '.'])
                elif char == '@': new_line.extend(['@', '.'])
            grid.append(new_line)
            
        rows = len(grid)
        cols = len(grid[0])
        
        robot_pos = None
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    robot_pos = (r, c)
                    grid[r][c] = '.'
                    break
                    
        directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        rr, rc = robot_pos
        
        for move in moves:
            dr, dc = directions[move]
            nr, nc = rr + dr, rc + dc
            
            if grid[nr][nc] == '#': continue
            if grid[nr][nc] == '.':
                rr, rc = nr, nc
                continue
                
            # Box interaction
            if grid[nr][nc] in ['[', ']']:
                # Pushing boxes.
                # Horizontal push is simple (like Part 1 but with shifting [ ])
                if dr == 0:
                    cr, cc = nr, nc
                    # Find end of box chain
                    while grid[cr][cc] in ['[', ']']:
                        cc += dc
                    
                    if grid[cr][cc] == '#': continue
                    
                    # Shift
                    # We need to shift everything from nr,nc to cr,cc-dc towards cr,cc
                    # Iterate backwards from free space
                    curr_c = cc
                    while curr_c != nc:
                        prev_c = curr_c - dc
                        grid[cr][curr_c] = grid[cr][prev_c]
                        curr_c = prev_c
                    grid[nr][nc] = '.'
                    rr, rc = nr, nc
                    
                else:
                    # Vertical Push
                    # Complex: A box can push 2 boxes above it if offset.
                    # We need to find the specific SET of blocks that move.
                    # BFS to find all connected boxes in the direction of movement.
                    
                    # Set of (r, c) box parts to move
                    to_move = set()
                    q = [] # Queue of (r, c) to check
                    
                    # Initial box part
                    q.append((nr, nc))
                    if grid[nr][nc] == '[': q.append((nr, nc + 1))
                    else: q.append((nr, nc - 1))
                    
                    possible = True
                    seen = set(q)
                    
                    idx = 0
                    while idx < len(q):
                        curr_r, curr_c = q[idx]
                        idx += 1
                        
                        next_r, next_c = curr_r + dr, curr_c
                        tile = grid[next_r][next_c]
                        
                        if tile == '#':
                            possible = False
                            break
                        if tile == '.':
                            continue
                        
                        # It's a box part
                        if (next_r, next_c) not in seen:
                            seen.add((next_r, next_c))
                            q.append((next_r, next_c))
                            # Add counterpart
                            if tile == '[':
                                if (next_r, next_c + 1) not in seen:
                                    seen.add((next_r, next_c + 1))
                                    q.append((next_r, next_c + 1))
                            elif tile == ']':
                                if (next_r, next_c - 1) not in seen:
                                    seen.add((next_r, next_c - 1))
                                    q.append((next_r, next_c - 1))
                                    
                    if not possible:
                        continue
                        
                    # Move everything
                    # Sort to move furthest first to avoid overwrite?
                    # Up (dr=-1): move top-most first.
                    # Down (dr=1): move bottom-most first.
                    
                    sorted_move = sorted(list(seen), key=lambda x: x[0], reverse=(dr > 0))
                    
                    # First clear old positions? Or verify we don't need to?
                    # Since we sorted, we overwrite safely if we copy to NEW position.
                    # But we also need to clear the OLD position if nothing moves into it.
                    # Easiest: Make a copy of values, clear all old, write all new.
                    
                    vals = {}
                    for r, c in sorted_move:
                        vals[(r, c)] = grid[r][c]
                        grid[r][c] = '.' # Clear old
                        
                    for r, c in sorted_move:
                        grid[r + dr][c] = vals[(r, c)] # Write new
                        
                    rr, rc = nr, nc

        total = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '[': total += 100 * r + c
        return total

    print(f"Result (Part 1): {solv_part1(grid_lines, moves)}")
    print(f"Result (Part 2): {solv_part2(grid_lines, moves)}")

if __name__ == '__main__':
    solve()
