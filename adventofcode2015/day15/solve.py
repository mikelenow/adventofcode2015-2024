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

    # Day 15: Science for Hungry People
    import re

    ingredients = []
    for line in lines:
        match = re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
        if match:
            name = match.group(1)
            capacity = int(match.group(2))
            durability = int(match.group(3))
            flavor = int(match.group(4))
            texture = int(match.group(5))
            calories = int(match.group(6))
            ingredients.append((capacity, durability, flavor, texture, calories))

    max_score = 0
    max_score_500cal = 0

    # Try all combinations of 100 teaspoons
    for i in range(101):
        for j in range(101 - i):
            for k in range(101 - i - j):
                l = 100 - i - j - k
                amounts = [i, j, k, l]

                cap = max(0, sum(amounts[idx] * ingredients[idx][0] for idx in range(len(ingredients))))
                dur = max(0, sum(amounts[idx] * ingredients[idx][1] for idx in range(len(ingredients))))
                fla = max(0, sum(amounts[idx] * ingredients[idx][2] for idx in range(len(ingredients))))
                tex = max(0, sum(amounts[idx] * ingredients[idx][3] for idx in range(len(ingredients))))
                cal = sum(amounts[idx] * ingredients[idx][4] for idx in range(len(ingredients)))

                score = cap * dur * fla * tex
                max_score = max(max_score, score)

                if cal == 500:
                    max_score_500cal = max(max_score_500cal, score)

    print(f"Part 1: {max_score}")
    print(f"Part 2: {max_score_500cal}")

if __name__ == '__main__':
    solve()
