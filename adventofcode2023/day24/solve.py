import sys
from fractions import Fraction

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

    # TODO: Implement solution
    hail = []
    for line in lines:
        if not line:
            continue
        left, right = line.split('@')
        px, py, pz = (int(v.strip()) for v in left.split(','))
        vx, vy, vz = (int(v.strip()) for v in right.split(','))
        hail.append(((px, py, pz), (vx, vy, vz)))

    lo = 200000000000000
    hi = 400000000000000

    part1 = 0
    for i in range(len(hail)):
        (x1, y1, _z1), (vx1, vy1, _vz1) = hail[i]
        for j in range(i + 1, len(hail)):
            (x2, y2, _z2), (vx2, vy2, _vz2) = hail[j]
            den = vx1 * vy2 - vy1 * vx2
            if den == 0:
                continue
            dx = x2 - x1
            dy = y2 - y1
            t = Fraction(dx * vy2 - dy * vx2, den)
            u = Fraction(dx * vy1 - dy * vx1, den)
            if t < 0 or u < 0:
                continue
            ix = Fraction(x1) + Fraction(vx1) * t
            iy = Fraction(y1) + Fraction(vy1) * t
            if lo <= ix <= hi and lo <= iy <= hi:
                part1 += 1

    def cross(a, b):
        return (
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        )

    (p0, v0) = hail[0]
    (p1, v1) = hail[1]
    (p2, v2) = hail[2]

    def build_rows(pi, vi):
        A = (vi[0] - v0[0], vi[1] - v0[1], vi[2] - v0[2])
        B = (pi[0] - p0[0], pi[1] - p0[1], pi[2] - p0[2])
        C0 = cross(pi, vi)
        C1 = cross(p0, v0)
        C = (C0[0] - C1[0], C0[1] - C1[1], C0[2] - C1[2])

        # variables: xr, yr, zr, vxr, vyr, vzr
        rows = []

        # x-component: yr*A_z - zr*A_y + B_y*vz - B_z*vy = C_x
        rows.append([
            Fraction(0),
            Fraction(A[2]),
            Fraction(-A[1]),
            Fraction(0),
            Fraction(-B[2]),
            Fraction(B[1]),
            Fraction(C[0]),
        ])

        # y-component: zr*A_x - xr*A_z + B_z*vx - B_x*vz = C_y
        rows.append([
            Fraction(-A[2]),
            Fraction(0),
            Fraction(A[0]),
            Fraction(B[2]),
            Fraction(0),
            Fraction(-B[0]),
            Fraction(C[1]),
        ])

        # z-component: xr*A_y - yr*A_x + B_x*vy - B_y*vx = C_z
        rows.append([
            Fraction(A[1]),
            Fraction(-A[0]),
            Fraction(0),
            Fraction(-B[1]),
            Fraction(B[0]),
            Fraction(0),
            Fraction(C[2]),
        ])

        return rows

    mat = build_rows(p1, v1) + build_rows(p2, v2)

    # Gaussian elimination on 6x7 augmented matrix
    r = 0
    for c in range(6):
        pivot = None
        for rr in range(r, 6):
            if mat[rr][c] != 0:
                pivot = rr
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        pv = mat[r][c]
        for cc in range(c, 7):
            mat[r][cc] /= pv
        for rr in range(6):
            if rr == r:
                continue
            f = mat[rr][c]
            if f == 0:
                continue
            for cc in range(c, 7):
                mat[rr][cc] -= f * mat[r][cc]
        r += 1

    sol = [Fraction(0) for _ in range(6)]
    for rr in range(6):
        lead = None
        for c in range(6):
            if mat[rr][c] == 1:
                lead = c
                break
        if lead is not None:
            sol[lead] = mat[rr][6]

    xr, yr, zr, vxr, vyr, vzr = sol
    part2 = int(xr + yr + zr)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
