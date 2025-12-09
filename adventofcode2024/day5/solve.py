
import sys

def parse_input(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return None, None

    parts = content.strip().split('\n\n')
    if len(parts) != 2:
        return None, None
    
    rules_text = parts[0].strip().split('\n')
    updates_text = parts[1].strip().split('\n')
    
    rules = []
    for line in rules_text:
        parts_rule = line.split('|')
        rules.append((int(parts_rule[0]), int(parts_rule[1])))
        
    updates = []
    for line in updates_text:
        updates.append(list(map(int, line.split(','))))
        
    return rules, updates

def is_ordered(update, rules):
    # Create a map of page -> index
    page_to_index = {page: i for i, page in enumerate(update)}
    
    for x, y in rules:
        if x in page_to_index and y in page_to_index:
            if page_to_index[x] > page_to_index[y]:
                return False
    return True

from functools import cmp_to_key

def compare_pages(a, b, rules_set):
    if (a, b) in rules_set:
        return -1 # a comes before b
    if (b, a) in rules_set:
        return 1  # b comes before a
    return 0

def solve():
    filename = 'input.txt'
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    rules, updates = parse_input(filename)
    if rules is None:
        return

    # Convert list of rules to set for O(1) lookups
    rules_set = set(rules)
    
    total_part1 = 0
    total_part2 = 0
    
    for update in updates:
        if is_ordered(update, rules):
            middle_index = len(update) // 2
            total_part1 += update[middle_index]
        else:
            # Sort the incorrect update
            # Using cmp_to_key to use the custom comparison function which uses the rules
            sorted_update = sorted(update, key=cmp_to_key(lambda x, y: compare_pages(x, y, rules_set)))
            middle_index = len(sorted_update) // 2
            total_part2 += sorted_update[middle_index]

    print(f"Result (Part 1): {total_part1}")
    print(f"Result (Part 2): {total_part2}")

if __name__ == '__main__':
    solve()
