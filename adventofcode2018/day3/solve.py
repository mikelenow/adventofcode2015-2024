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

    claims = []
    for line in lines:
        if not line:
            continue
        left, size = line.split(': ')
        size_x, size_y = size.split('x')
        size_x = int(size_x)
        size_y = int(size_y)

        claim_id_part, at_part = left.split(' @ ')
        claim_id = int(claim_id_part[1:])
        x_str, y_str = at_part.split(',')
        x = int(x_str)
        y = int(y_str)
        claims.append((claim_id, x, y, size_x, size_y))

    counts = {}
    owner = {}
    overlapped = set()
    overlap_squares = 0

    for claim_id, x, y, w, h in claims:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                key = (xx, yy)

                prev_count = counts.get(key, 0)
                new_count = prev_count + 1
                counts[key] = new_count
                if new_count == 2:
                    overlap_squares += 1

                prev_owner = owner.get(key)
                if prev_owner is None:
                    owner[key] = claim_id
                elif prev_owner == -1:
                    overlapped.add(claim_id)
                else:
                    overlapped.add(prev_owner)
                    overlapped.add(claim_id)
                    owner[key] = -1

    part1 = overlap_squares
    part2 = None
    for claim_id, _, _, _, _ in claims:
        if claim_id not in overlapped:
            part2 = claim_id
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
