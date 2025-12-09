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

    import hashlib

    door_id = lines[0]
    password1 = []
    password2 = ['_'] * 8
    index = 0
    found = 0

    while len(password1) < 8 or found < 8:
        hash_input = f"{door_id}{index}"
        hash_result = hashlib.md5(hash_input.encode()).hexdigest()

        if hash_result.startswith('00000'):
            if len(password1) < 8:
                password1.append(hash_result[5])

            pos = hash_result[5]
            if pos.isdigit():
                pos = int(pos)
                if pos < 8 and password2[pos] == '_':
                    password2[pos] = hash_result[6]
                    found += 1

        index += 1

    part1 = ''.join(password1)
    part2 = ''.join(password2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
