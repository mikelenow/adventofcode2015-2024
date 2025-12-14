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

    # TODO: Implement solution
    bps = []
    for s in lines:
        if not s:
            continue
        nums = list(map(int, re.findall(r"\d+", s)))
        if len(nums) < 7:
            continue
        _, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = nums[:7]
        bps.append((ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs))

    if not bps:
        print(0)
        print(0)
        return

    from functools import lru_cache

    def best_for_bp(bp, T):
        ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = bp
        max_ore_cost = max(ore_ore, clay_ore, obs_ore, geo_ore)
        max_clay_cost = obs_clay
        max_obs_cost = geo_obs

        @lru_cache(None)
        def dfs(t, ore, clay, obs, oreR, clayR, obsR, geoR):
            if t == 0:
                return 0

            ore = min(ore, max_ore_cost * t)
            clay = min(clay, max_clay_cost * t)
            obs = min(obs, max_obs_cost * t)

            best = 0

            if ore >= geo_ore and obs >= geo_obs:
                return geoR + dfs(
                    t - 1,
                    ore - geo_ore + oreR,
                    clay + clayR,
                    obs - geo_obs + obsR,
                    oreR,
                    clayR,
                    obsR,
                    geoR + 1,
                )

            if obsR < max_obs_cost and ore >= obs_ore and clay >= obs_clay:
                best = max(
                    best,
                    geoR + dfs(
                        t - 1,
                        ore - obs_ore + oreR,
                        clay - obs_clay + clayR,
                        obs + obsR,
                        oreR,
                        clayR,
                        obsR + 1,
                        geoR,
                    ),
                )

            if clayR < max_clay_cost and ore >= clay_ore:
                best = max(
                    best,
                    geoR + dfs(
                        t - 1,
                        ore - clay_ore + oreR,
                        clay + clayR,
                        obs + obsR,
                        oreR,
                        clayR + 1,
                        obsR,
                        geoR,
                    ),
                )

            if oreR < max_ore_cost and ore >= ore_ore:
                best = max(
                    best,
                    geoR + dfs(
                        t - 1,
                        ore - ore_ore + oreR,
                        clay + clayR,
                        obs + obsR,
                        oreR + 1,
                        clayR,
                        obsR,
                        geoR,
                    ),
                )

            best = max(
                best,
                geoR + dfs(
                    t - 1,
                    ore + oreR,
                    clay + clayR,
                    obs + obsR,
                    oreR,
                    clayR,
                    obsR,
                    geoR,
                ),
            )
            return best

        return dfs(T, 0, 0, 0, 1, 0, 0, 0)

    part1 = 0
    for i, bp in enumerate(bps, 1):
        part1 += i * best_for_bp(bp, 24)

    part2 = 1
    for bp in bps[:3]:
        part2 *= best_for_bp(bp, 32)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
