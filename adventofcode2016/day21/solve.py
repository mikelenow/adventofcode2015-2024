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

    import re

    def scramble(password, instructions):
        pwd = list(password)
        for line in instructions:
            if line.startswith('swap position'):
                x, y = map(int, re.findall(r'\d+', line))
                pwd[x], pwd[y] = pwd[y], pwd[x]
            elif line.startswith('swap letter'):
                x, y = re.findall(r'letter (\w)', line)
                for i in range(len(pwd)):
                    if pwd[i] == x:
                        pwd[i] = y
                    elif pwd[i] == y:
                        pwd[i] = x
            elif line.startswith('rotate left'):
                x = int(re.search(r'\d+', line).group())
                pwd = pwd[x:] + pwd[:x]
            elif line.startswith('rotate right'):
                x = int(re.search(r'\d+', line).group())
                pwd = pwd[-x:] + pwd[:-x]
            elif line.startswith('rotate based'):
                letter = re.search(r'letter (\w)', line).group(1)
                idx = pwd.index(letter)
                rot = 1 + idx + (1 if idx >= 4 else 0)
                rot = rot % len(pwd)
                pwd = pwd[-rot:] + pwd[:-rot]
            elif line.startswith('reverse'):
                x, y = map(int, re.findall(r'\d+', line))
                pwd[x:y+1] = reversed(pwd[x:y+1])
            elif line.startswith('move'):
                x, y = map(int, re.findall(r'\d+', line))
                letter = pwd.pop(x)
                pwd.insert(y, letter)
        return ''.join(pwd)

    def unscramble(password, instructions):
        pwd = list(password)
        for line in reversed(instructions):
            if line.startswith('swap position'):
                x, y = map(int, re.findall(r'\d+', line))
                pwd[x], pwd[y] = pwd[y], pwd[x]
            elif line.startswith('swap letter'):
                x, y = re.findall(r'letter (\w)', line)
                for i in range(len(pwd)):
                    if pwd[i] == x:
                        pwd[i] = y
                    elif pwd[i] == y:
                        pwd[i] = x
            elif line.startswith('rotate left'):
                x = int(re.search(r'\d+', line).group())
                pwd = pwd[-x:] + pwd[:-x]
            elif line.startswith('rotate right'):
                x = int(re.search(r'\d+', line).group())
                pwd = pwd[x:] + pwd[:x]
            elif line.startswith('rotate based'):
                letter = re.search(r'letter (\w)', line).group(1)
                idx = pwd.index(letter)
                # Reverse the rotation
                rot_map = {0: 1, 1: 1, 2: 6, 3: 2, 4: 7, 5: 3, 6: 0, 7: 4}
                rot = rot_map[idx]
                pwd = pwd[rot:] + pwd[:rot]
            elif line.startswith('reverse'):
                x, y = map(int, re.findall(r'\d+', line))
                pwd[x:y+1] = reversed(pwd[x:y+1])
            elif line.startswith('move'):
                x, y = map(int, re.findall(r'\d+', line))
                letter = pwd.pop(y)
                pwd.insert(x, letter)
        return ''.join(pwd)

    part1 = scramble('abcdefgh', lines)
    part2 = unscramble('fbgdceah', lines)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
