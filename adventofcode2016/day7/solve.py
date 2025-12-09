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

    import re

    def has_abba(s):
        for i in range(len(s) - 3):
            if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
                return True
        return False

    def get_abas(s):
        abas = []
        for i in range(len(s) - 2):
            if s[i] == s[i+2] and s[i] != s[i+1]:
                abas.append(s[i:i+3])
        return abas

    def supports_tls(ip):
        parts = re.split(r'\[|\]', ip)
        supernet = [parts[i] for i in range(0, len(parts), 2)]
        hypernet = [parts[i] for i in range(1, len(parts), 2)]

        has_abba_supernet = any(has_abba(s) for s in supernet)
        has_abba_hypernet = any(has_abba(h) for h in hypernet)

        return has_abba_supernet and not has_abba_hypernet

    def supports_ssl(ip):
        parts = re.split(r'\[|\]', ip)
        supernet = [parts[i] for i in range(0, len(parts), 2)]
        hypernet = [parts[i] for i in range(1, len(parts), 2)]

        for s in supernet:
            abas = get_abas(s)
            for aba in abas:
                bab = aba[1] + aba[0] + aba[1]
                if any(bab in h for h in hypernet):
                    return True
        return False

    tls_count = sum(1 for ip in lines if supports_tls(ip))
    ssl_count = sum(1 for ip in lines if supports_ssl(ip))

    print(f"Part 1: {tls_count}")
    print(f"Part 2: {ssl_count}")

if __name__ == '__main__':
    solve()
