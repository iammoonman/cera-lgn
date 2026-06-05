from collections import deque
import random

from typing import TypeVar

T = TypeVar("T")


def max_matching(adj: dict[T, tuple[T, int]], nodes: list[T]) -> tuple[dict[T, T], int]:
    """

    Finds maximum matching in a general undirected graph using Edmonds' Blossom algorithm.

    Input: adj — list of lists, adj[u] is the list of neighbors of u (0-indexed).

    Returns: match, size

      match — list where match[u] = v if u–v is in the matching, or -1

      size  — number of matched edges
    """

    n = len(adj)
    match_dict: dict[T, T | None] = {l: None for l in nodes}  # match[u] = v if u is matched to v
    parent: dict[T, T | None] = {l: None for l in nodes}  # parent in the alternating tree
    base: dict[T, T | None] = {l: l for l in nodes}  # base[u] = base vertex of blossom containing u
    queue = deque()  # queue for BFS
    used: dict[T, bool] = {l: False for l in nodes}  # whether vertex is in the tree
    blossom: dict[T, bool] = {l: False for l in nodes}  # helper array for marking blossoms

    def lca(a: T, b: T) -> T:
        """Find least common ancestor of a and b in the forest of alternating tree."""
        nonlocal parent
        nonlocal base
        nonlocal match_dict
        used_path = {l: False for l in nodes}
        count = 0
        while True and count < 10:
            a = base[a]
            used_path[a] = True
            if match_dict[a] is None:
                break
            a = parent[match_dict[a]]
            count += 1
        while True and count < 10:
            b = base[b]
            if used_path[b]:
                return b
            b = parent[match_dict[b]]
            count += 1

    def mark_path(v: T, b: T, x: T) -> None:
        """Mark vertices along the path from v to base b, setting their parent to x."""
        nonlocal blossom
        nonlocal parent
        nonlocal match_dict
        if v is None or b is None:
            return
        while base[v] != b:
            blossom[base[v]] = blossom[base[match_dict[v]]] = True
            parent[v] = x
            x = match_dict[v]
            v = parent[x]

    def find_path(root: T) -> bool:
        """Try to find an augmenting path starting from root."""
        nonlocal used
        nonlocal parent
        nonlocal base
        nonlocal blossom
        nonlocal match_dict
        # reset
        used = {l: False for l in nodes}
        parent = {l: None for l in nodes}
        base = {l: l for l in nodes}
        queue.clear()
        used[root] = True
        queue.append(root)

        while queue:
            v = queue.popleft()
            # BFS over the adjacent nodes
            for u, w in sorted(adj[v], key=lambda x: x[1]):
                # two cases to skip
                if base[v] == base[u] or match_dict[v] == u:
                    continue
                # found a blossom or an odd cycle edge
                if u == root or (match_dict[u] is not None and parent[match_dict[u]] is not None):
                    curbase = lca(v, u)
                    # unfold the blossoms
                    blossom = {n: False for n in nodes}
                    mark_path(v, curbase, u)
                    mark_path(u, curbase, v)
                    # contract blossom
                    for i in nodes:
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                queue.append(i)
                # otherwise extend the alternating tree
                elif parent[u] is None:
                    parent[u] = v
                    if match_dict[u] is None:
                        # augmenting path found: flip matches along the path
                        curr = u
                        while curr is not None:
                            prev = parent[curr]
                            nxt = match_dict[prev] if prev is not None else None
                            match_dict[curr] = prev
                            match_dict[prev] = curr
                            curr = nxt
                        return True
                    # else continue BFS from the matched partner
                    used[match_dict[u]] = True
                    queue.append(match_dict[u])
        return False

    # Main loop: try to grow matching by finding augmenting paths
    res = 0
    for v in nodes:
        if match_dict[v] is None:
            if find_path(v):
                res += 1
    return match_dict, res


def do_matching(nodes: list[T], edges: list[tuple[T, T, int]]) -> tuple[dict[T, T | None], int, int]:
    matchings: list[tuple[dict[T, T | None], int, int]] = []
    for q in range(len(edges)):
        if q != 0 and False:
            random.shuffle(edges)
        else:
            edges = sorted(edges, key=lambda x: x[2], reverse=False)
        weights = {a: 99 for a in nodes}
        adj = {node: [] for node in nodes}
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
            weights[u] = min(weights[u], w)
            weights[v] = min(weights[v], w)
        if q != 0:
            random.shuffle(nodes)
        else:
            nodes = sorted(nodes, key=lambda x: weights[x], reverse=True)
        # print(nodes)
        # print(edges)
        match, msize = max_matching(adj, nodes)
        # print(f"Maximum matching size: {msize}")
        # print("Matched pairs:")
        seen = set()
        total_weight = 0
        for u, v in match.items():
            if v != -1 and (v, u) not in seen:
                w = [a[2] for a in edges if (a[0] == u and a[1] == v) or (a[1] == u and a[0] == v)]
                # print(f"  {u} – {v} : w={w}")
                seen.add((u, v))
                total_weight += max(w + [0])
        # print(f"Weight: {total_weight}, Size: {msize}")
        # if min(matchings + [({}, 0, 999)], key=lambda x: x[2])[2] > total_weight:
        #     print('New cheapest matching: ', edges)
        matchings.append([match, msize, total_weight])
    # print(min(matchings, key=lambda x: x[2]))
    # print("=" * 40)
    # print("=" * 40)
    # print("=" * 40)
    return min(matchings, key=lambda x: x[2])


if __name__ == "__main__":
    # Example: 5‑cycle (odd cycle)
    # Vertices: 0–1–2–3–4–0
    nodes = ["0", "1", "2", "3", "4", "5"]
    edges = [("0", "1", 8), ("1", "2", 0.5), ("2", "3", 2), ("3", "4", 5), ("4", "0", 2), ("5", "0", 1.5)]
    do_matching(nodes, edges)
    # Example 2:
    nodes = ["0", "1", "2", "3", "4", "5"]
    edges = [("1", "5", 1), ("5", "0", 10), ("0", "2", 3), ("2", "3", -15), ("4", "2", 6), ("1", "4", 15), ("5", "4", 4), ("4", "0", 2)]
    do_matching(nodes, edges)
    # Example 3:
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    edges = [("A", "B", 6), ("B", "C", 2), ("C", "D", 30), ("D", "E", 10), ("D", "F", 22), ("E", "F", 15), ("E", "G", 50), ("F", "G", 8), ("G", "A", 10)]
    do_matching(nodes, edges)
    # Example 4:
    nodes = ["A", "B", "C", "D", "E", "F"]
    edges = [("C", "D", 20), ("D", "F", 7), ("B", "D", 15), ("B", "F", 17), ("B", "A", 8), ("A", "E", 10)]
    do_matching(nodes, edges)
    # Example 5:
    nodes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    edges = [("0", "1", 6), ("1", "4", 14), ("4", "8", 6), ("0", "2", 10), ("1", "2", 12), ("1", "3", 11), ("4", "5", 4), ("2", "3", 12), ("3", "5", 6), ("5", "8", 12), ("2", "7", 16), ("2", "6", 8), ("3", "6", 3), ("6", "8", 16), ("7", "9", 8), ("6", "9", 6), ("9", "8", 13)]
    do_matching(nodes, edges)
    # Example 6:
    nodes = ["MIA", "DFW", "LGA", "PVD", "HNL", "SFO", "LAX", "ORD"]
    edges = [("HNL", "LAX", 2555), ("SFO", "LAX", 337), ("SFO", "ORD", 1843), ("LAX", "ORD", 1743), ("LAX", "DFW", 1233), ("ORD", "DFW", 802), ("ORD", "PVD", 849), ("DFW", "LGA", 1387), ("DFW", "MIA", 1120), ("LGA", "MIA", 1099), ("LGA", "PVD", 142), ("PVD", "MIA", 1205)]
    do_matching(nodes, edges)
    # Example 7:
    nodes = ["11", "12", "13", "14", "15", "16", "17", "18", "19"]
    edges = [("11", "12", 7), ("12", "13", 1), ("13", "14", 4), ("14", "15", 6), ("15", "16", 3), ("16", "17", 3), ("17", "18", 2), ("11", "18", 4), ("11", "19", 6), ("12", "16", 5), ("12", "18", 3), ("12", "19", 3), ("13", "16", 3), ("14", "16", 6), ("14", "18", 2), ("16", "18", 3), ("16", "19", 4), ("17", "19", 2)]
    do_matching(nodes, edges)
    # Example 8:
    nodes = [f"{n + 1}" for n in range(12)]
    edges = [
        ("1", "2", random.randint(1, 12)),
        ("1", "4", random.randint(1, 12)),
        ("1", "5", random.randint(1, 12)),
        ("1", "6", random.randint(1, 12)),
        ("1", "8", random.randint(1, 12)),
        ("1", "9", random.randint(1, 12)),
        ("1", "11", random.randint(1, 12)),
        ("2", "3", random.randint(1, 12)),
        ("2", "4", random.randint(1, 12)),
        ("2", "6", random.randint(1, 12)),
        ("2", "7", random.randint(1, 12)),
        ("2", "8", random.randint(1, 12)),
        ("2", "9", random.randint(1, 12)),
        ("2", "10", random.randint(1, 12)),
        ("2", "11", random.randint(1, 12)),
        ("2", "12", random.randint(1, 12)),
        ("3", "5", random.randint(1, 12)),
        ("3", "6", random.randint(1, 12)),
        ("3", "8", random.randint(1, 12)),
        ("3", "12", random.randint(1, 12)),
        ("4", "6", random.randint(1, 12)),
        ("4", "8", random.randint(1, 12)),
        ("4", "10", random.randint(1, 12)),
        ("4", "11", random.randint(1, 12)),
        ("4", "12", random.randint(1, 12)),
        ("5", "6", random.randint(1, 12)),
        ("5", "7", random.randint(1, 12)),
        ("5", "9", random.randint(1, 12)),
        ("5", "12", random.randint(1, 12)),
        ("6", "7", random.randint(1, 12)),
        ("6", "8", random.randint(1, 12)),
        ("6", "9", random.randint(1, 12)),
        ("6", "10", random.randint(1, 12)),
        ("6", "11", random.randint(1, 12)),
        ("6", "12", random.randint(1, 12)),
        ("7", "12", random.randint(1, 12)),
        ("8", "11", random.randint(1, 12)),
        ("8", "12", random.randint(1, 12)),
        ("9", "10", random.randint(1, 12)),
        ("9", "11", random.randint(1, 12)),
        ("9", "12", random.randint(1, 12)),
        ("10", "11", random.randint(1, 12)),
        ("10", "12", random.randint(1, 12)),
    ]
    print(edges)
    do_matching(nodes, edges)
