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

    # Day 21: RPG Simulator 20XX
    import re

    # Parse boss stats
    boss_hp = int(re.search(r'Hit Points: (\d+)', lines[0]).group(1))
    boss_damage = int(re.search(r'Damage: (\d+)', lines[1]).group(1))
    boss_armor = int(re.search(r'Armor: (\d+)', lines[2]).group(1))

    # Shop items (cost, damage, armor)
    weapons = [(8,4,0), (10,5,0), (25,6,0), (40,7,0), (74,8,0)]
    armors = [(0,0,0), (13,0,1), (31,0,2), (53,0,3), (75,0,4), (102,0,5)]
    rings = [(0,0,0), (0,0,0), (25,1,0), (50,2,0), (100,3,0), (20,0,1), (40,0,2), (80,0,3)]

    def player_wins(player_hp, player_damage, player_armor, boss_hp, boss_damage, boss_armor):
        player_atk = max(1, player_damage - boss_armor)
        boss_atk = max(1, boss_damage - player_armor)
        player_turns = (boss_hp + player_atk - 1) // player_atk
        boss_turns = (player_hp + boss_atk - 1) // boss_atk
        return player_turns <= boss_turns

    min_cost = float('inf')
    max_cost = 0

    for weapon in weapons:
        for armor in armors:
            for i, ring1 in enumerate(rings):
                for ring2 in rings[i+1:]:
                    cost = weapon[0] + armor[0] + ring1[0] + ring2[0]
                    damage = weapon[1] + armor[1] + ring1[1] + ring2[1]
                    armor_val = weapon[2] + armor[2] + ring1[2] + ring2[2]

                    if player_wins(100, damage, armor_val, boss_hp, boss_damage, boss_armor):
                        min_cost = min(min_cost, cost)
                    else:
                        max_cost = max(max_cost, cost)

    print(f"Part 1: {min_cost}")
    print(f"Part 2: {max_cost}")

if __name__ == '__main__':
    solve()
