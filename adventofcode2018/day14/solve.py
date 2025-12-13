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

    s = None
    for line in lines:
        if line:
            s = line
            break
    if s is None:
        print('')
        print('')
        return

    n = int(s)
    pattern = [int(ch) for ch in s]
    plen = len(pattern)

    recipes = [3, 7]
    a = 0
    b = 1

    part2 = None

    def check_tail():
        nonlocal part2
        if part2 is not None:
            return
        L = len(recipes)
        if L >= plen and recipes[L - plen:L] == pattern:
            part2 = L - plen
        elif L >= plen + 1 and recipes[L - plen - 1:L - 1] == pattern:
            part2 = L - plen - 1

    while len(recipes) < n + 10 or part2 is None:
        ssum = recipes[a] + recipes[b]
        if ssum >= 10:
            recipes.append(1)
            recipes.append(ssum - 10)
        else:
            recipes.append(ssum)
        check_tail()
        a = (a + 1 + recipes[a]) % len(recipes)
        b = (b + 1 + recipes[b]) % len(recipes)

    part1 = ''.join(str(d) for d in recipes[n:n + 10])
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
