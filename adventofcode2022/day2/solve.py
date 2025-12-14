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
    opp_map = {'A': 0, 'B': 1, 'C': 2}
    me_map = {'X': 0, 'Y': 1, 'Z': 2}
    outcome_score = {0: 3, 1: 6, 2: 0}  # diff (me-opp)%3: 0 draw, 1 win, 2 lose

    p1 = 0
    p2 = 0
    for s in lines:
        if not s:
            continue
        a, b = s.split()
        opp = opp_map[a]

        me = me_map[b]
        diff = (me - opp) % 3
        p1 += (me + 1) + outcome_score[diff]

        if b == 'X':
            me2 = (opp - 1) % 3
            p2 += (me2 + 1) + 0
        elif b == 'Y':
            me2 = opp
            p2 += (me2 + 1) + 3
        else:
            me2 = (opp + 1) % 3
            p2 += (me2 + 1) + 6

    print(p1)
    print(p2)

if __name__ == '__main__':
    solve()
