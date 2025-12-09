
import sys
from collections import defaultdict

def bron_kerbosch(R, P, X, graph, cliques):
    """Bron-Kerbosch algorithm to find all maximal cliques."""
    if not P and not X:
        cliques.append(R)
        return
    
    for node in list(P):
        neighbors = graph[node]
        bron_kerbosch(
            R | {node},
            P & neighbors,
            X & neighbors,
            graph,
            cliques
        )
        P.remove(node)
        X.add(node)

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

    # Build adjacency list
    graph = defaultdict(set)
    
    for line in lines:
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)
    
    # Part 1: Find all sets of 3 interconnected computers
    triangles = set()
    
    for node in graph:
        neighbors = graph[node]
        # Check all pairs of neighbors
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 < n2 and n2 in graph[n1]:
                    # Found a triangle
                    triangle = tuple(sorted([node, n1, n2]))
                    triangles.add(triangle)
    
    # Count triangles with at least one node starting with 't'
    count = 0
    for triangle in triangles:
        if any(node.startswith('t') for node in triangle):
            count += 1
    
    print(f"Part 1: {count}")
    
    # Part 2: Find maximum clique (largest fully connected set)
    all_nodes = set(graph.keys())
    cliques = []
    
    bron_kerbosch(set(), all_nodes, set(), graph, cliques)
    
    # Find the largest clique
    max_clique = max(cliques, key=len)
    password = ','.join(sorted(max_clique))
    
    print(f"Part 2: {password}")

if __name__ == '__main__':
    solve()
