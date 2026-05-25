import polars as pl
from itertools import combinations

def pairmaj_from_rcv(rcv_ballots: pl.DataFrame) -> dict[str, set[str]]:
    """
    Build a pairwise majority winner graph from a box of Ranked-Choice Ballots.

    parameters
    ---
    rcv_ballots : pl.DataFrame
        A Polars DataFrame representing ballots. Each column is a candidate and each
        row is is a voter's ranking of the candidates. Lower numbers indicate higher
        preference (1 = top-choice).

    returns
    ---
    pairmaj_graph: dict[str, set[str]]
        A pairwise majority winner graph whose nodes correspond to candidates and 
        (directed) edges show which candidates they beat pairwise.
    """
    candidates = rcv_ballots.columns

    pairmaj_graph: dict[str, set[str]] = {c: set() for c in candidates}

    for a, b in combinations(candidates, 2):
        result = rcv_ballots.select(
            [
                (pl.col(a) < pl.col(b)).sum().alias("a_wins"),
                (pl.col(b) < pl.col(a)).sum().alias("b_wins"),
            ]
        ).row(0)

        a_wins, b_wins = result

        if a_wins > b_wins:
            pairmaj_graph[a].add(b)
        elif b_wins > a_wins:
            pairmaj_graph[b].add(a)

    return pairmaj_graph






