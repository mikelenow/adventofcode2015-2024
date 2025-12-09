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
    import re

    salt = lines[0]

    def get_hash(s, stretch=False):
        h = hashlib.md5(s.encode()).hexdigest()
        if stretch:
            for _ in range(2016):
                h = hashlib.md5(h.encode()).hexdigest()
        return h

    def find_keys(salt, stretch=False):
        keys = []
        index = 0
        hash_cache = {}

        while len(keys) < 64:
            if index not in hash_cache:
                hash_cache[index] = get_hash(f"{salt}{index}", stretch)

            current_hash = hash_cache[index]

            # Look for triple
            match = re.search(r'(.)\1{2}', current_hash)
            if match:
                char = match.group(1)
                target = char * 5

                # Check next 1000 hashes
                for j in range(index + 1, index + 1001):
                    if j not in hash_cache:
                        hash_cache[j] = get_hash(f"{salt}{j}", stretch)
                    if target in hash_cache[j]:
                        keys.append(index)
                        break

            index += 1

        return keys[63]

    part1 = find_keys(salt, False)
    part2 = find_keys(salt, True)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
