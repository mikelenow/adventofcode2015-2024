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

    raw = [line.rstrip('\n') for line in lines]
    if not raw:
        print(0)
        print(0)
        return

    def part1():
        deck_size = 10007
        deck = list(range(deck_size))
        for line in raw:
            if line == 'deal into new stack':
                deck.reverse()
            elif line.startswith('cut'):
                n = int(line.split()[-1])
                deck = deck[n:] + deck[:n]
            elif line.startswith('deal with increment'):
                n = int(line.split()[-1])
                new_deck = [0] * deck_size
                for i in range(deck_size):
                    new_deck[(i * n) % deck_size] = deck[i]
                deck = new_deck
        return deck.index(2019)

    def part2():
        deck_size = 119315717514047
        repeats = 101741582076661
        pos = 2020

        a, b = 1, 0
        for line in raw:
            if line == 'deal into new stack':
                na = -a
                nb = -b - 1
            elif line.startswith('cut'):
                n = int(line.split()[-1])
                na = a
                nb = b - n
            elif line.startswith('deal with increment'):
                n = int(line.split()[-1])
                na = a * n
                nb = b * n
            a, b = na % deck_size, nb % deck_size
        
        # We have f(x) = ax + b
        # We want to find f^k(pos)
        # f^k(x) = a^k * x + (a^(k-1) + ... + 1) * b
        # f^k(x) = a^k * x + (a^k - 1) / (a - 1) * b
        # We are looking for the card at pos 2020, so we need the inverse function
        # x = f_inv(y) = (y - b) / a = a_inv * y - a_inv * b
        # Let's find the transformation for the inverse shuffle repeated K times.
        # f_inv(y) = a_inv * y - a_inv * b
        # a' = a_inv
        # b' = -a_inv * b
        # Let the full reverse shuffle be g(y) = a'y + b'
        # g^k(y) = (a')^k * y + ((a')^k - 1) / (a' - 1) * b'
        
        inv_a = pow(a, -1, deck_size)
        
        # This is g^k(y) = A'y + B'
        final_a = pow(inv_a, repeats, deck_size)
        
        # B' = ((a')^k - 1) * (a' - 1)_inv * b'
        final_b = (final_a - 1) * pow(inv_a - 1, -1, deck_size) * (-inv_a * b)
        final_b %= deck_size

        return (final_a * pos + final_b) % deck_size


    p1 = part1()
    p2 = part2()

    print(p1)
    print(p2)

if __name__ == '__main__':
    solve()
