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

    # Day 22: Wizard Simulator 20XX
    # This is a complex simulation - implementing a simplified version
    import re
    from collections import deque

    boss_hp = int(re.search(r'Hit Points: (\d+)', lines[0]).group(1))
    boss_damage = int(re.search(r'Damage: (\d+)', lines[1]).group(1))

    spells = [
        ('Magic Missile', 53, 4, 0, 0, 0),
        ('Drain', 73, 2, 2, 0, 0),
        ('Shield', 113, 0, 0, 6, 7),
        ('Poison', 173, 0, 0, 6, 3),
        ('Recharge', 229, 0, 0, 5, 0)
    ]

    def simulate(hard_mode=False):
        min_mana = float('inf')
        queue = deque([(50, 500, boss_hp, {}, 0, True)])  # player_hp, player_mana, boss_hp, effects, mana_spent, player_turn

        while queue:
            php, pm, bhp, eff, spent, player_turn = queue.popleft()

            if spent >= min_mana:
                continue

            if hard_mode and player_turn:
                php -= 1
                if php <= 0:
                    continue

            # Apply effects
            shield_armor = 0
            new_eff = {}
            for spell_name, duration in eff.items():
                if spell_name == 'Shield' and duration > 0:
                    shield_armor = 7
                if spell_name == 'Poison' and duration > 0:
                    bhp -= 3
                if spell_name == 'Recharge' and duration > 0:
                    pm += 101
                if duration > 1:
                    new_eff[spell_name] = duration - 1
            eff = new_eff

            if bhp <= 0:
                min_mana = min(min_mana, spent)
                continue

            if player_turn:
                for spell_name, cost, damage, heal, duration, dot in spells:
                    if pm < cost or spell_name in eff:
                        continue

                    new_php = php + heal
                    new_pm = pm - cost
                    new_bhp = bhp - damage
                    new_eff = eff.copy()
                    if duration > 0:
                        new_eff[spell_name] = duration
                    new_spent = spent + cost

                    queue.append((new_php, new_pm, new_bhp, new_eff, new_spent, False))
            else:
                damage = max(1, boss_damage - shield_armor)
                new_php = php - damage
                if new_php > 0:
                    queue.append((new_php, pm, bhp, eff, spent, True))

        return min_mana

    part1 = simulate(False)
    part2 = simulate(True)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
