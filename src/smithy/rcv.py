import polars as pl
import rustworkx as rwx
from itertools import combinations


def _pmg_from_rcv(ballots: pl.DataFrame) -> rwx.PyDiGraph:
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
    nodes: dict[str, int]
        A dictionary of candidate names to associated node ids.

    pwm_graph: rwx.PyDiGraph
        A pairwise majority winner graph whose nodes correspond to candidates and
        (directed) edges show which candidates they beat pairwise.
    """
    candidates = ballots.columns

    pmg = rwx.PyDiGraph()
    nodes = {c: pmg.add_node(c) for c in candidates}

    #compressed = ballots.group_by(ballots.columns).len().rename({"len": "count"})

    exprs = []
    pairs = list(combinations(candidates, 2))

    for a, b in pairs:
        exprs.extend(
            [
                (pl.col(a) < pl.col(b)).sum().alias(f"{a}>{b}"),
                (pl.col(b) < pl.col(a)).sum().alias(f"{b}>{a}"),
            ]
        )

    results = ballots.select(exprs).row(0, named=True)

    for a, b in pairs:
        a_wins = results[f"{a}>{b}"]
        b_wins = results[f"{b}>{a}"]

        if a_wins > b_wins:
            pmg.add_edge(nodes[a], nodes[b], a_wins - b_wins)
        elif b_wins > a_wins:
            pmg.add_edge(nodes[b], nodes[a], b_wins - a_wins)

    return pmg

def pmg_from_rcv(ballots: pl.DataFrame) -> rwx.PyDiGraph:
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
    nodes: dict[str, int]
        A dictionary of candidate names to associated node ids.

    pwm_graph: rwx.PyDiGraph
        A pairwise majority winner graph whose nodes correspond to candidates and
        (directed) edges show which candidates they beat pairwise.
    """
    candidates = ballots.columns

    pmg = rwx.PyDiGraph()
    nodes = {c: pmg.add_node(c) for c in candidates}

    compressed = ballots.group_by(ballots.columns).len().rename({"len": "count"})
    counts = compressed["count"].to_numpy()
    
    arr = compressed.drop("count").to_numpy()
    results = ((arr[:, :, None] < arr[:, None, :]) * counts[:, None, None]).sum(axis=0)

    for i, a in enumerate(candidates):
        for j in range(i + 1, len(candidates)):
            b = candidates[j]
            
            a_wins = results[i, j]
            b_wins = results[j, i]
            
            if a_wins > b_wins:
                pmg.add_edge(nodes[a], nodes[b], int(a_wins - b_wins))
            elif b_wins > a_wins:
                pmg.add_edge(nodes[b], nodes[a], int(b_wins - a_wins))

    return pmg