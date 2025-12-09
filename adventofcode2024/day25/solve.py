
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

    schematics = content.strip().split('\n\n')
    
    locks = []
    keys = []
    
    for schematic in schematics:
        lines = schematic.split('\n')
        height = len(lines)
        width = len(lines[0])
        
        # Check if it's a lock (top row filled) or key (bottom row filled)
        is_lock = lines[0] == '#' * width
        
        # Calculate heights for each column
        heights = []
        for col in range(width):
            count = 0
            for row in range(height):
                if lines[row][col] == '#':
                    count += 1
            # Convert to pin height (subtract 1 for the base row)
            heights.append(count - 1)
        
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)
    
    # Try every lock/key combination
    max_height = height - 2  # Available space (excluding top and bottom rows)
    fitting_pairs = 0
    
    for lock in locks:
        for key in keys:
            # Check if they fit (no overlap in any column)
            fits = True
            for i in range(len(lock)):
                if lock[i] + key[i] > max_height:
                    fits = False
                    break
            
            if fits:
                fitting_pairs += 1
    
    print(f"Part 1: {fitting_pairs}")
    print(f"Part 2: ⭐ Congratulations! You've collected all 50 stars! ⭐")

if __name__ == '__main__':
    solve()
