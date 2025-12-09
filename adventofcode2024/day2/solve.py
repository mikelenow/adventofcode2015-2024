
def check_safety(levels):
    if len(levels) < 2:
        return False 

    diffs = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
    
    all_increasing = all(d > 0 for d in diffs)
    all_decreasing = all(d < 0 for d in diffs)
    
    if not (all_increasing or all_decreasing):
        return False
        
    if not all(1 <= abs(d) <= 3 for d in diffs):
        return False
        
    return True

def is_safe(report):
    levels = list(map(int, report.split()))
    
    if check_safety(levels):
        return True
        
    # Problem Dampener: Try removing one level
    for i in range(len(levels)):
        modified_levels = levels[:i] + levels[i+1:]
        if check_safety(modified_levels):
            return True
            
    return False

def solve():
    import sys
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Please create 'input.txt' with your puzzle input.")
        return

    count = 0
    for line in lines:
        if line.strip():
            if is_safe(line):
                count += 1
    print(f"Safe reports: {count}")

if __name__ == '__main__':
    solve()
