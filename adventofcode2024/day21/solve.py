
import sys
from functools import cache
from itertools import product

# Numeric keypad layout
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# Directional keypad layout
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

NUMERIC_KEYPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2)
}

DIRECTIONAL_KEYPAD = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2)
}

def get_paths(start, end, keypad):
    """Get all shortest paths from start to end on the keypad."""
    sr, sc = keypad[start]
    er, ec = keypad[end]
    
    dr = er - sr
    dc = ec - sc
    
    # Build the moves
    vertical = ('v' if dr > 0 else '^') * abs(dr)
    horizontal = ('>' if dc > 0 else '<') * abs(dc)
    
    # Generate all permutations of moves
    moves = vertical + horizontal
    if not moves:
        return ['A']  # Already at target
    
    # Get all unique orderings
    from itertools import permutations
    paths = set()
    for perm in permutations(moves):
        path = ''.join(perm) + 'A'
        # Check if path is valid (doesn't go through gap)
        r, c = sr, sc
        valid = True
        for move in perm:
            if move == '^': r -= 1
            elif move == 'v': r += 1
            elif move == '<': c -= 1
            elif move == '>': c += 1
            
            # Check if we hit the gap
            if keypad == NUMERIC_KEYPAD and (r, c) == (3, 0):
                valid = False
                break
            if keypad == DIRECTIONAL_KEYPAD and (r, c) == (0, 0):
                valid = False
                break
        
        if valid:
            paths.add(path)
    
    return list(paths) if paths else ['A']

@cache
def min_length(code, depth, is_numeric=False):
    """Find minimum button presses needed at given depth."""
    if depth == 0:
        return len(code)
    
    keypad = NUMERIC_KEYPAD if is_numeric else DIRECTIONAL_KEYPAD
    current = 'A'
    total = 0
    
    for char in code:
        paths = get_paths(current, char, keypad)
        # Try all possible paths and pick the one with minimum length at next level
        min_len = float('inf')
        for path in paths:
            length = min_length(path, depth - 1, False)
            min_len = min(min_len, length)
        total += min_len
        current = char
    
    return total

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            codes = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # Part 1: 2 directional keypads + 1 numeric = depth 3
    total_complexity_p1 = 0
    for code in codes:
        length = min_length(code, 3, True)
        numeric_part = int(code[:-1])
        complexity = length * numeric_part
        total_complexity_p1 += complexity
    
    print(f"Part 1: {total_complexity_p1}")
    
    # Part 2: 25 directional keypads + 1 numeric = depth 26
    total_complexity_p2 = 0
    for code in codes:
        length = min_length(code, 26, True)
        numeric_part = int(code[:-1])
        complexity = length * numeric_part
        total_complexity_p2 += complexity
    
    print(f"Part 2: {total_complexity_p2}")

if __name__ == '__main__':
    solve()
