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

    # Day 11: Corporate Policy
    # Generate next valid password

    def is_valid_password(pwd):
        # Must include one increasing straight of 3 letters
        has_straight = False
        for i in range(len(pwd) - 2):
            if ord(pwd[i+1]) == ord(pwd[i]) + 1 and ord(pwd[i+2]) == ord(pwd[i]) + 2:
                has_straight = True
                break
        if not has_straight:
            return False

        # Must not contain i, o, or l
        if 'i' in pwd or 'o' in pwd or 'l' in pwd:
            return False

        # Must contain at least two different, non-overlapping pairs
        pairs = []
        i = 0
        while i < len(pwd) - 1:
            if pwd[i] == pwd[i+1]:
                pairs.append(pwd[i])
                i += 2
            else:
                i += 1
        if len(set(pairs)) < 2:
            return False

        return True

    def increment_password(pwd):
        pwd_list = list(pwd)
        i = len(pwd_list) - 1
        while i >= 0:
            if pwd_list[i] == 'z':
                pwd_list[i] = 'a'
                i -= 1
            else:
                pwd_list[i] = chr(ord(pwd_list[i]) + 1)
                break
        return ''.join(pwd_list)

    current = lines[0]

    # Find next valid password (Part 1)
    while True:
        current = increment_password(current)
        if is_valid_password(current):
            part1 = current
            break

    # Find next valid password after that (Part 2)
    while True:
        current = increment_password(current)
        if is_valid_password(current):
            part2 = current
            break

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
