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

    # TODO: Implement solution
    jets = ''
    for s in lines:
        if s:
            jets = s.strip()
            break
    if not jets:
        print(0)
        print(0)
        return

    shapes = [
        [0b1111],
        [0b010, 0b111, 0b010],
        [0b111, 0b100, 0b100],
        [0b1, 0b1, 0b1, 0b1],
        [0b11, 0b11],
    ]

    def collide(ch, x, y, shape_rows):
        if x < 0:
            return True
        for i, row in enumerate(shape_rows):
            m = row << x
            if m & ~0b1111111:
                return True
            yy = y + i
            if yy < 0:
                return True
            if yy < len(ch) and (ch[yy] & m):
                return True
        return False

    def place(ch, x, y, shape_rows):
        need = y + len(shape_rows)
        while len(ch) < need:
            ch.append(0)
        for i, row in enumerate(shape_rows):
            ch[y + i] |= row << x

    def top_profile(ch, height):
        depths = [0] * 7
        for x in range(7):
            d = 0
            for yy in range(height - 1, max(-1, height - 60), -1):
                d += 1
                if yy < len(ch) and (ch[yy] & (1 << x)):
                    break
            depths[x] = d
        m = min(depths)
        return tuple(d - m for d in depths)

    def simulate(total_rocks):
        ch = []
        height = 0
        jet_i = 0
        seen = {}
        added = 0
        r = 0
        while r < total_rocks:
            si = r % len(shapes)
            shape = shapes[si]
            x = 2
            y = height + 3
            while True:
                j = jets[jet_i]
                jet_i = (jet_i + 1) % len(jets)
                if j == '<':
                    if not collide(ch, x - 1, y, shape):
                        x -= 1
                else:
                    if not collide(ch, x + 1, y, shape):
                        x += 1
                if not collide(ch, x, y - 1, shape):
                    y -= 1
                    continue
                place(ch, x, y, shape)
                height = max(height, y + len(shape))
                break

            r += 1
            key = (si, jet_i, top_profile(ch, height))
            if key in seen and r < total_rocks:
                r0, h0 = seen[key]
                cyc_len = r - r0
                cyc_h = height - h0
                rem = total_rocks - r
                k = rem // cyc_len
                if k:
                    r += k * cyc_len
                    added += k * cyc_h
            else:
                seen[key] = (r, height)

        return height + added

    print(simulate(2022))
    print(simulate(1000000000000))

if __name__ == '__main__':
    solve()
