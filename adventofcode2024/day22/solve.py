
import sys
from collections import defaultdict

def evolve_secret(secret):
    """Evolve a secret number to the next one."""
    # Step 1: multiply by 64, mix, prune
    secret = ((secret * 64) ^ secret) % 16777216
    
    # Step 2: divide by 32, mix, prune
    secret = ((secret // 32) ^ secret) % 16777216
    
    # Step 3: multiply by 2048, mix, prune
    secret = ((secret * 2048) ^ secret) % 16777216
    
    return secret

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

    initial_secrets = [int(line) for line in lines if line]
    
    # Part 1
    total = 0
    for secret in initial_secrets:
        current = secret
        for _ in range(2000):
            current = evolve_secret(current)
        total += current
    
    print(f"Part 1: {total}")
    
    # Part 2: Find best sequence of 4 price changes
    # For each buyer, track what price they'd sell at for each sequence
    sequence_totals = defaultdict(int)
    
    for initial_secret in initial_secrets:
        current = initial_secret
        prices = [current % 10]
        
        # Generate 2000 more secrets and their prices
        for _ in range(2000):
            current = evolve_secret(current)
            prices.append(current % 10)
        
        # Calculate price changes
        changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
        
        # Track which sequences this buyer has seen (only count first occurrence)
        seen_sequences = set()
        
        # Look for all 4-change sequences
        for i in range(len(changes) - 3):
            sequence = tuple(changes[i:i+4])
            
            # Only count the first time this buyer sees this sequence
            if sequence not in seen_sequences:
                seen_sequences.add(sequence)
                # The price after this sequence completes
                price = prices[i + 4]
                sequence_totals[sequence] += price
    
    # Find the sequence that gives the most bananas
    best_sequence = max(sequence_totals, key=sequence_totals.get)
    max_bananas = sequence_totals[best_sequence]
    
    print(f"Part 2: {max_bananas}")

if __name__ == '__main__':
    solve()
