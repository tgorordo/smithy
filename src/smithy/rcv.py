import polars as pl
from itertools import combinations


def smith_set(df: pl.DataFrame) -> list:
    """
    Compute the Smith set from a Ranked-Choice ballot.

    The Smith set is the minimal set of candidates which can beat all others pairwise - if there is a single winner
    in the set they are guaranteed the Condorcet i.e. Majority winner.

    parameters
    ---
    df : pl.DataFrame
        A Polars DataFrame representing ballots. Each column is a candidate and each
        row is is a voter's ranking of the candidates. Lower numbers indicate higher
        preference (1 = top-choice).

    returns
    ---
    smith_set : list
        A list of the Smith set candidates - all are equally good winners; ordering is determined lexicographically.
        If there is a Condorcet winner (single Majority winner), the Smith set will contain that single candidate.


    """

    candidates = df.columns

    # Build pairwise majority graph
    graph: dict[str, set[str]] = {c: set() for c in candidates}

    for a, b in combinations(candidates, 2):
        result = df.select(
            [
                (pl.col(a) < pl.col(b)).sum().alias("a_wins"),
                (pl.col(b) < pl.col(a)).sum().alias("b_wins"),
            ]
        ).row(0)

        a_wins, b_wins = result

        if a_wins > b_wins:
            graph[a].add(b)
        elif b_wins > a_wins:
            graph[b].add(a)

    # Find Smith set
    for size in range(1, len(candidates) + 1):
        for sub in combinations(candidates, size):
            subset = set(sub)
            out = set(candidates) - subset

            dom = True

            for member in subset:
                if not out.issubset(graph[member]):
                    dom = False
                    break

            if dom:
                return sorted(subset)

    return []
