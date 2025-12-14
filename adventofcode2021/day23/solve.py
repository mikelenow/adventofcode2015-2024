import sys
import heapq

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n\r') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    grid = [s for s in lines if s.strip() != '']
    if not grid:
        print(0)
        print(0)
        return

    def parse_rooms(lines_local):
        row1 = [lines_local[2][3], lines_local[2][5], lines_local[2][7], lines_local[2][9]]
        row2 = [lines_local[3][3], lines_local[3][5], lines_local[3][7], lines_local[3][9]]
        return tuple([row1[i] + row2[i] for i in range(4)])

    def parse_rooms_part2(lines_local):
        row1 = [lines_local[2][3], lines_local[2][5], lines_local[2][7], lines_local[2][9]]
        row2 = [lines_local[3][3], lines_local[3][5], lines_local[3][7], lines_local[3][9]]
        ins1 = ['D', 'C', 'B', 'A']
        ins2 = ['D', 'B', 'A', 'C']
        return tuple([row1[i] + ins1[i] + ins2[i] + row2[i] for i in range(4)])

    energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_x = [2, 4, 6, 8]
    hallway_stops = [0, 1, 3, 5, 7, 9, 10]

    def solve_depth(rooms, depth):
        start = ('.' * 11, rooms)
        goal_rooms = ('A' * depth, 'B' * depth, 'C' * depth, 'D' * depth)

        def is_done(state):
            hall, rms = state
            return hall == '.' * 11 and rms == goal_rooms

        def clear_path(hall, a, b):
            if a < b:
                rng = range(a + 1, b + 1)
            else:
                rng = range(b, a)
            for i in rng:
                if hall[i] != '.':
                    return False
            return True

        def room_can_accept(rms, ri, amph):
            r = rms[ri]
            if any(ch != '.' and ch != amph for ch in r):
                return False
            return True

        def room_insert_pos(rms, ri):
            r = rms[ri]
            for i in range(depth - 1, -1, -1):
                if r[i] == '.':
                    return i
            return None

        def room_top(rms, ri):
            r = rms[ri]
            for i in range(depth):
                if r[i] != '.':
                    return i, r[i]
            return None, None

        def room_settled(rms, ri):
            want = 'ABCD'[ri]
            r = rms[ri]
            for ch in r:
                if ch != '.' and ch != want:
                    return False
            return True

        dist = {start: 0}
        pq = [(0, start)]
        while pq:
            d, state = heapq.heappop(pq)
            if d != dist.get(state):
                continue
            if is_done(state):
                return d
            hall, rms = state

            for hi in range(11):
                amph = hall[hi]
                if amph == '.':
                    continue
                ri = 'ABCD'.index(amph)
                if not room_can_accept(rms, ri, amph):
                    continue
                rx = room_x[ri]
                if not clear_path(hall, hi, rx):
                    continue
                ins = room_insert_pos(rms, ri)
                if ins is None:
                    continue
                steps = abs(hi - rx) + (ins + 1)
                nd = d + steps * energy[amph]
                nhall = hall[:hi] + '.' + hall[hi + 1:]
                new_r = list(rms)
                rr = list(new_r[ri])
                rr[ins] = amph
                new_r[ri] = ''.join(rr)
                ns = (nhall, tuple(new_r))
                if nd < dist.get(ns, 10**18):
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))

            for ri in range(4):
                if room_settled(rms, ri):
                    continue
                topi, amph = room_top(rms, ri)
                if amph is None:
                    continue
                rx = room_x[ri]
                for hi in hallway_stops:
                    if hall[hi] != '.':
                        continue
                    if not clear_path(hall, rx, hi):
                        continue
                    steps = abs(hi - rx) + (topi + 1)
                    nd = d + steps * energy[amph]
                    nhall = hall[:hi] + amph + hall[hi + 1:]
                    new_r = list(rms)
                    rr = list(new_r[ri])
                    rr[topi] = '.'
                    new_r[ri] = ''.join(rr)
                    ns = (nhall, tuple(new_r))
                    if nd < dist.get(ns, 10**18):
                        dist[ns] = nd
                        heapq.heappush(pq, (nd, ns))

        return 0

    rooms1 = parse_rooms(grid)
    part1 = solve_depth(rooms1, 2)
    rooms2 = parse_rooms_part2(grid)
    part2 = solve_depth(rooms2, 4)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
