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

    grid = [list(line) for line in lines if line]

    def part1():
        g = [row[:] for row in grid]
        seen = set()
        while True:
            s = "".join("".join(row) for row in g)
            if s in seen:
                rating = 0
                for r in range(5):
                    for c in range(5):
                        if g[r][c] == '#':
                            rating += 2**(r*5 + c)
                return rating
            seen.add(s)

            new_g = [row[:] for row in g]
            for r in range(5):
                for c in range(5):
                    bugs = 0
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 5 and 0 <= nc < 5 and g[nr][nc] == '#':
                            bugs += 1
                    
                    if g[r][c] == '#' and bugs != 1:
                        new_g[r][c] = '.'
                    elif g[r][c] == '.' and bugs in (1, 2):
                        new_g[r][c] = '#'
            g = new_g

    def part2():
        levels = {0: [row[:] for row in grid]}
        
        for _ in range(200):
            new_levels = {}
            min_level, max_level = min(levels.keys()) - 1, max(levels.keys()) + 1
            
            for level in range(min_level, max_level + 1):
                new_grid = [['.' for _ in range(5)] for _ in range(5)]
                for r in range(5):
                    for c in range(5):
                        if r == 2 and c == 2: continue

                        bugs = 0
                        # Neighbors on same level
                        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 5 and 0 <= nc < 5:
                                if nr == 2 and nc == 2:
                                    # Inner recursion
                                    if level + 1 in levels:
                                        if r == 1: # Row above center
                                            bugs += sum(1 for i in range(5) if levels[level+1][0][i] == '#')
                                        elif r == 3: # Row below center
                                            bugs += sum(1 for i in range(5) if levels[level+1][4][i] == '#')
                                        elif c == 1: # Col left of center
                                            bugs += sum(1 for i in range(5) if levels[level+1][i][0] == '#')
                                        elif c == 3: # Col right of center
                                            bugs += sum(1 for i in range(5) if levels[level+1][i][4] == '#')
                                else:
                                    if level in levels and levels[level][nr][nc] == '#':
                                        bugs += 1
                        
                        # Outer recursion
                        if level - 1 in levels:
                            if r == 0: bugs += 1 if levels[level-1][1][2] == '#' else 0
                            if r == 4: bugs += 1 if levels[level-1][3][2] == '#' else 0
                            if c == 0: bugs += 1 if levels[level-1][2][1] == '#' else 0
                            if c == 4: bugs += 1 if levels[level-1][2][3] == '#' else 0

                        current_char = levels.get(level, [['.']*5]*5)[r][c]
                        if current_char == '#' and bugs != 1:
                            new_grid[r][c] = '.'
                        elif current_char == '.' and bugs in (1, 2):
                            new_grid[r][c] = '#'
                        else:
                            new_grid[r][c] = current_char

                if any('#' in row for row in new_grid):
                    new_levels[level] = new_grid
            levels = new_levels

        return sum(row.count('#') for grid in levels.values() for row in grid)

    print(part1())
    print(part2())

if __name__ == '__main__':
    solve()
