
import sys
import re

def solve():
    filename = 'input.txt'
    # Default grid size 101 wide, 103 tall
    width = 101
    height = 103
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
    # Check if test input, use smaller grid
    if 'test' in filename:
        width = 11
        height = 7

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    robots = []
    # p=0,4 v=3,-3
    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            px, py = int(match.group(1)), int(match.group(2))
            vx, vy = int(match.group(3)), int(match.group(4))
            robots.append({'p': (px, py), 'v': (vx, vy)})
            
    # Part 1: Simulate 100 seconds
    mid_x = (width - 1) // 2
    mid_y = (height - 1) // 2
    
    q1 = q2 = q3 = q4 = 0
    duration_p1 = 100
    
    for r in robots:
        px, py = r['p']
        vx, vy = r['v']
        fx = (px + duration_p1 * vx) % width
        fy = (py + duration_p1 * vy) % height
        
        if fx == mid_x or fy == mid_y: continue
        if fx < mid_x and fy < mid_y: q1 += 1
        elif fx > mid_x and fy < mid_y: q2 += 1
        elif fx < mid_x and fy > mid_y: q3 += 1
        elif fx > mid_x and fy > mid_y: q4 += 1
        
    safety_factor = q1 * q2 * q3 * q4
    print(f"Result (Part 1): {safety_factor}")
    
    # Part 2
    # Search for the Easter Egg (Christmas Tree).
    # Heuristic: The tree likely corresponds to a state where robots effectively cluster together,
    # minimizing the safety factor or variance.
    # We iterate t from 0 to 10000 (enough for most AOC LCM cycles).
    
    min_safety = float('inf')
    best_t = -1
    
    # Pre-calculate positions per second to avoid re-mult
    # Actually just simulate step by step is fast enough.
    
    current_robots = [(r['p'][0], r['p'][1], r['v'][0], r['v'][1]) for r in robots]
    
    # Iterate
    for t in range(1, 10001):
        # Update
        new_robots = []
        
        q1 = q2 = q3 = q4 = 0
        
        # We can optimize: we don't need to store robots if we just want stats,
        # but we need to carry state for next step.
        
        # Also let's check for a line? A tree usually has a border or frame.
        # "Most of the robots should arrange themselves into a picture".
        # Low entropy/safety factor is a common signal.
        
        for i in range(len(current_robots)):
            px, py, vx, vy = current_robots[i]
            nx = (px + vx) % width
            ny = (py + vy) % height
            current_robots[i] = (nx, ny, vx, vy)
            
            # Quadrant check
            if nx == mid_x or ny == mid_y:
                continue
            if nx < mid_x and ny < mid_y: q1 += 1
            elif nx > mid_x and ny < mid_y: q2 += 1
            elif nx < mid_x and ny > mid_y: q3 += 1
            elif nx > mid_x and ny > mid_y: q4 += 1
            
        safety = q1 * q2 * q3 * q4
        
        if safety < min_safety:
            min_safety = safety
            best_t = t
            
    print(f"Result (Part 2 - Estimated): {best_t}")
    print(f"Min Safety Factor found: {min_safety}")
    
    # To be sure, one would visualize `best_t`.
    # But often the minimum safety factor is the unique correct answer for these "hidden message" tasks.

if __name__ == '__main__':
    solve()
