import sys
import re

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

    passports = []
    cur = {}
    for s in lines + ['']:
        if not s:
            if cur:
                passports.append(cur)
            cur = {}
            continue
        for tok in s.split():
            k, v = tok.split(':', 1)
            cur[k] = v

    req = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    part1 = 0
    part2 = 0

    hcl_re = re.compile(r'^#[0-9a-f]{6}$')
    pid_re = re.compile(r'^[0-9]{9}$')
    ecl_ok = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    def valid(p):
        try:
            byr = int(p['byr'])
            if not (1920 <= byr <= 2002):
                return False
            iyr = int(p['iyr'])
            if not (2010 <= iyr <= 2020):
                return False
            eyr = int(p['eyr'])
            if not (2020 <= eyr <= 2030):
                return False

            hgt = p['hgt']
            if hgt.endswith('cm'):
                v = int(hgt[:-2])
                if not (150 <= v <= 193):
                    return False
            elif hgt.endswith('in'):
                v = int(hgt[:-2])
                if not (59 <= v <= 76):
                    return False
            else:
                return False

            if hcl_re.match(p['hcl']) is None:
                return False
            if p['ecl'] not in ecl_ok:
                return False
            if pid_re.match(p['pid']) is None:
                return False
            return True
        except Exception:
            return False

    for p in passports:
        if req.issubset(p.keys()):
            part1 += 1
            if valid(p):
                part2 += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
