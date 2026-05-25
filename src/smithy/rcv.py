import polars as pl
import rustworkx as rwx
from itertools import combinations


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
