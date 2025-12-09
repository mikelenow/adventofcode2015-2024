import re
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

    # Regex for all instructions: mul(X,Y), do(), don't()
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))"
    matches = re.finditer(pattern, content)
    
    total = 0
    enabled = True
    
    for match in matches:
        if match.group(1) and match.group(2):
            if enabled:
                total += int(match.group(1)) * int(match.group(2))
        elif match.group(3):
            enabled = True
        elif match.group(4):
            enabled = False

    print(f"Total (Part 2): {total}")

if __name__ == '__main__':
    solve()
