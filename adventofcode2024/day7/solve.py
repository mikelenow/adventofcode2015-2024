
import sys

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

    lines = [line for line in lines if line]

    def check_equation(target, nums, use_concat):
        # Recursive DFS
        def dfs(index, current_val):
            if index == len(nums):
                return current_val == target
            
            if current_val > target:
                return False
            
            next_num = nums[index]
            
            # Try +
            if dfs(index + 1, current_val + next_num):
                return True
            
            # Try *
            if dfs(index + 1, current_val * next_num):
                return True
                
            # Try ||
            if use_concat:
                concat_val = int(str(current_val) + str(next_num))
                if dfs(index + 1, concat_val):
                    return True
            
            return False

        return dfs(1, nums[0])

    total_part1 = 0
    total_part2 = 0
    
    for line in lines:
        parts = line.split(':')
        target = int(parts[0])
        nums = list(map(int, parts[1].split()))
        
        if check_equation(target, nums, False):
            total_part1 += target
            # If it's valid for Part 1, it's valid for Part 2 (just don't use ||, or || is available but we found a solution without it)
            # Actually, the problem asks "which equations could possibly be true". 
            # If it's true with +/*, it's counted.
            # If it's ONLY true with ||, it's also counted in Part 2.
            # So Part 2 total is superset of Part 1 variables?
            # "Adding up all six test values (the three that could be made before... plus the new three...)"
            # Yes.
            total_part2 += target
        elif check_equation(target, nums, True):
            total_part2 += target

    print(f"Result (Part 1): {total_part1}")
    print(f"Result (Part 2): {total_part2}")

if __name__ == '__main__':
    solve()
