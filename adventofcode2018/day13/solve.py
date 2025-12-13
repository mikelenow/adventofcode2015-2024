import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    grid = [list(line) for line in lines if line != '']
    if not grid:
        print('')
        print('')
        return

    width = max(len(row) for row in grid)
    for row in grid:
        if len(row) < width:
            row.extend([' '] * (width - len(row)))

    carts = []
    # cart: [x,y,dir,turn_state,alive]
    # dir in '^','v','<','>' ; turn_state cycles 0:left 1:straight 2:right
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            ch = grid[y][x]
            if ch in '^v<>':
                carts.append([x, y, ch, 0, True])
                grid[y][x] = '|' if ch in '^v' else '-'

    def left_dir(d):
        return {'^': '<', '<': 'v', 'v': '>', '>': '^'}[d]

    def right_dir(d):
        return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[d]

    def step_cart(cart):
        x, y, d, t, alive = cart
        if d == '^':
            y -= 1
        elif d == 'v':
            y += 1
        elif d == '<':
            x -= 1
        else:
            x += 1

        track = grid[y][x]
        if track == '+':
            if t == 0:
                d = left_dir(d)
            elif t == 2:
                d = right_dir(d)
            t = (t + 1) % 3
        elif track == '/':
            if d in '^v':
                d = right_dir(d)
            else:
                d = left_dir(d)
        elif track == '\\':
            if d in '^v':
                d = left_dir(d)
            else:
                d = right_dir(d)
        cart[0] = x
        cart[1] = y
        cart[2] = d
        cart[3] = t

    first_crash = None

    while True:
        carts.sort(key=lambda c: (c[1], c[0]))
        positions = {}
        for i, c in enumerate(carts):
            if c[4]:
                positions[(c[0], c[1])] = i

        for i, cart in enumerate(carts):
            if not cart[4]:
                continue

            old_pos = (cart[0], cart[1])
            if positions.get(old_pos) == i:
                del positions[old_pos]

            step_cart(cart)
            pos = (cart[0], cart[1])

            if pos in positions:
                other_i = positions[pos]
                carts[other_i][4] = False
                cart[4] = False
                del positions[pos]
                if first_crash is None:
                    first_crash = pos
            else:
                positions[pos] = i

        alive = [c for c in carts if c[4]]
        if len(alive) == 1:
            last = alive[0]
            print(f"{first_crash[0]},{first_crash[1]}")
            print(f"{last[0]},{last[1]}")
            return

if __name__ == '__main__':
    solve()
