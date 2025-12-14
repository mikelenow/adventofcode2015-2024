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
    s = ''
    for ln in lines:
        if ln:
            s = ln.strip()
            break
    if not s:
        print(0)
        print(0)
        return

    bits = ''.join(f"{int(ch, 16):04b}" for ch in s)

    def parse(pos):
        version = int(bits[pos:pos + 3], 2)
        type_id = int(bits[pos + 3:pos + 6], 2)
        pos += 6
        ver_sum = version

        if type_id == 4:
            val_bits = []
            while True:
                group = bits[pos:pos + 5]
                pos += 5
                val_bits.append(group[1:])
                if group[0] == '0':
                    break
            value = int(''.join(val_bits), 2) if val_bits else 0
            return pos, ver_sum, value

        length_type = bits[pos]
        pos += 1
        values = []

        if length_type == '0':
            total_len = int(bits[pos:pos + 15], 2)
            pos += 15
            end = pos + total_len
            while pos < end:
                pos, vs, v = parse(pos)
                ver_sum += vs
                values.append(v)
        else:
            count = int(bits[pos:pos + 11], 2)
            pos += 11
            for _ in range(count):
                pos, vs, v = parse(pos)
                ver_sum += vs
                values.append(v)

        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = 1
            for v in values:
                value *= v
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = 1 if values[0] > values[1] else 0
        elif type_id == 6:
            value = 1 if values[0] < values[1] else 0
        elif type_id == 7:
            value = 1 if values[0] == values[1] else 0
        else:
            value = 0

        return pos, ver_sum, value

    _, part1, part2 = parse(0)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
