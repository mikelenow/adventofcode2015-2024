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

    text = ''
    for line in lines:
        if line:
            text = line
            break
    if not text:
        print(0)
        print(0)
        return

    # "400 players; last marble is worth 71864 points"
    parts = text.split()
    players = int(parts[0])
    last = int(parts[6])

    def high_score(last_marble: int) -> int:
        # Array-backed linked list for O(1) insert/remove.
        nxt = [0] * (last_marble + 1)
        prv = [0] * (last_marble + 1)
        nxt[0] = 0
        prv[0] = 0
        cur = 0
        scores = [0] * players

        for marble in range(1, last_marble + 1):
            p = (marble - 1) % players
            if marble % 23 != 0:
                a = nxt[cur]
                b = nxt[a]
                nxt[a] = marble
                prv[marble] = a
                nxt[marble] = b
                prv[b] = marble
                cur = marble
            else:
                remove = cur
                for _ in range(7):
                    remove = prv[remove]
                scores[p] += marble + remove
                ra = prv[remove]
                rb = nxt[remove]
                nxt[ra] = rb
                prv[rb] = ra
                cur = rb

        return max(scores)

    part1 = high_score(last)
    part2 = high_score(last * 100)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
