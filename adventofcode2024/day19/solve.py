
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
    patterns_str = parts[0]
    designs = parts[1].split('\n')
    
    patterns = [p.strip() for p in patterns_str.split(',')]
    
    # Part 1: Count how many designs are possible
    memo_possible = {}
    
    def can_make(design):
        if design in memo_possible:
            return memo_possible[design]
        if not design:
            return True
        
        possible = False
        for p in patterns:
            if design.startswith(p):
                if can_make(design[len(p):]):
                    possible = True
                    break
        
        memo_possible[design] = possible
        return possible

    count_possible = 0
    for design in designs:
        if can_make(design):
            count_possible += 1
            
    print(f"Part 1: {count_possible}")
    
    # Part 2: Count total number of ways to make each design
    memo_ways = {}
    
    def count_ways(design):
        if design in memo_ways:
            return memo_ways[design]
        if not design:
            return 1  # Empty string has exactly one way (use no patterns)
        
        total_ways = 0
        for p in patterns:
            if design.startswith(p):
                total_ways += count_ways(design[len(p):])
        
        memo_ways[design] = total_ways
        return total_ways
    
    total_arrangements = 0
    for design in designs:
        ways = count_ways(design)
        total_arrangements += ways
            
    print(f"Part 2: {total_arrangements}")

if __name__ == '__main__':
    solve()
