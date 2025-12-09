
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            line = f.read().strip()
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    if not line:
        return

    stones = list(map(int, line.split()))
    
    # We need to simulate blinking 25 times.
    # The order of stones is preserved, but stones can split.
    # The number of stones can grow rapidly.
    # For Part 1 (25 blinks), simulation is likely fine.
    
    from collections import Counter

    current_stones = Counter(stones)
    
    # We need results for 25 and 75 blinks.
    # Simulation loop
    
    for blink in range(75):
        if blink == 25:
            print(f"Result (Part 1): {sum(current_stones.values())}")
            
        next_stones = Counter()
        for stone, count in current_stones.items():
            # Rule 1: 0 -> 1
            if stone == 0:
                next_stones[1] += count
            # Rule 2: Even digits -> split
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                mid = len(s) // 2
                left = int(s[:mid])
                right = int(s[mid:])
                next_stones[left] += count
                next_stones[right] += count
            # Rule 3: * 2024
            else:
                next_stones[stone * 2024] += count
        current_stones = next_stones
        
    print(f"Result (Part 2): {sum(current_stones.values())}")

if __name__ == '__main__':
    solve()
