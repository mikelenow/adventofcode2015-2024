
import sys
import re

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

    # Parse input
    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    
    machines = content.strip().split('\n\n')
    
    def solve_for_machines(machines, offset=0, check_limit=False):
        total = 0
        count = 0
        for machine in machines:
            lines = machine.strip().split('\n')
            if len(lines) < 3:
                continue
                
            # Parse A
            match_a = re.search(r'X\+(\d+), Y\+(\d+)', lines[0])
            ax, ay = int(match_a.group(1)), int(match_a.group(2))
            
            # Parse B
            match_b = re.search(r'X\+(\d+), Y\+(\d+)', lines[1])
            bx, by = int(match_b.group(1)), int(match_b.group(2))
            
            # Parse Prize
            match_p = re.search(r'X=(\d+), Y=(\d+)', lines[2])
            px, py = int(match_p.group(1)) + offset, int(match_p.group(2)) + offset
            
            # Cramer's Rule
            det = ax * by - ay * bx
            
            if det == 0:
                continue
                
            # Da = px * by - py * bx
            num_a = px * by - py * bx
            # Db = ax * py - ay * px
            num_b = ax * py - ay * px
            
            if num_a % det == 0 and num_b % det == 0:
                a = num_a // det
                b = num_b // det
                
                if a >= 0 and b >= 0:
                    if check_limit and (a > 100 or b > 100):
                        continue
                    total += a * 3 + b * 1
                    count += 1
        return total

    # Part 1
    total1 = solve_for_machines(machines, offset=0, check_limit=True)
    print(f"Result (Part 1): {total1}")
    
    # Part 2
    total2 = solve_for_machines(machines, offset=10000000000000, check_limit=False)
    print(f"Result (Part 2): {total2}")

if __name__ == '__main__':
    solve()
