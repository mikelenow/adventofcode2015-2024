
import sys

def solve():
    # Input from day11/input.txt
    stones = [0, 7, 198844, 5687836, 58, 2478, 25475, 894]
    
    memo = {}

    def count_stones(stone, blinks_left):
        if blinks_left == 0:
            return 1
        
        state = (stone, blinks_left)
        if state in memo:
            return memo[state]
        
        count = 0
        # Rule 1
        if stone == 0:
            count = count_stones(1, blinks_left - 1)
        # Rule 2
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            mid = len(s) // 2
            left = int(s[:mid])
            right = int(s[mid:])
            count = count_stones(left, blinks_left - 1) + count_stones(right, blinks_left - 1)
        # Rule 3
        else:
            count = count_stones(stone * 2024, blinks_left - 1)
            
        memo[state] = count
        return count

    total_25 = sum(count_stones(s, 25) for s in stones)
    print(f"Result 25: {total_25}")
    
    # Clear memo? Not needed, logic holds. But key space large?
    # Depth 75 is fine. width of numbers is limited?
    # Numbers grow in value but often split.
    # Repetitions are high (that's why Counter/Memo works).
    
    total_75 = sum(count_stones(s, 75) for s in stones)
    print(f"Result 75: {total_75}")

if __name__ == '__main__':
    sys.setrecursionlimit(20000)
    solve()
