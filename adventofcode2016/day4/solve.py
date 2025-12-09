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
    from collections import Counter

    def is_real_room(name, checksum):
        freq = Counter(name.replace('-', ''))
        sorted_chars = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
        expected = ''.join(c for c, _ in sorted_chars[:5])
        return expected == checksum

    def decrypt_name(name, sector_id):
        result = []
        for char in name:
            if char == '-':
                result.append(' ')
            else:
                shifted = (ord(char) - ord('a') + sector_id) % 26
                result.append(chr(ord('a') + shifted))
        return ''.join(result)

    total = 0
    north_pole_sector = 0

    for line in lines:
        if line:
            match = re.match(r'([a-z-]+)-(\d+)\[([a-z]+)\]', line)
            if match:
                name, sector_id, checksum = match.groups()
                sector_id = int(sector_id)

                if is_real_room(name, checksum):
                    total += sector_id

                    decrypted = decrypt_name(name, sector_id)
                    if 'north' in decrypted and 'pole' in decrypted:
                        north_pole_sector = sector_id

    print(f"Part 1: {total}")
    print(f"Part 2: {north_pole_sector}")

if __name__ == '__main__':
    solve()
