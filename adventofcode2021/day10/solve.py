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
    opens = '([{<'
    closes = ')]}>'
    match = {o: c for o, c in zip(opens, closes)}
    score_bad = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score_comp = {')': 1, ']': 2, '}': 3, '>': 4}

    part1 = 0
    comps = []
    for s in lines:
        if not s:
            continue
        st = []
        bad = None
        for ch in s:
            if ch in match:
                st.append(ch)
            else:
                if not st:
                    bad = ch
                    break
                o = st.pop()
                if match[o] != ch:
                    bad = ch
                    break
        if bad is not None:
            part1 += score_bad.get(bad, 0)
            continue
        if st:
            sc = 0
            while st:
                c = match[st.pop()]
                sc = sc * 5 + score_comp[c]
            comps.append(sc)

    comps.sort()
    part2 = comps[len(comps) // 2] if comps else 0
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
