import polars as pl
from itertools import combinations

from .rcv import pairmaj_from_rcv


def smith_set_brutefrom_pairmaj(pairmaj_graph: dict[str, set[str]]) -> list:
    """
    Brute-force the Smith set from a pairwise majority winner graph.

    parameters
    ---
    pairmaj_graph: dict[str, set[str]]
        A graph whose nodes correspond to candidates and (directed) edges show
        which candidates they beat pairwise.

    returns
    ---
    smith_set: list
        A list of the Smith set candidates - all are equally good winners;
        ordering is determined lexicographically. If there is a Condorcet winner
        (single Majority winner), the Smith set will contain that single candidate.
    """

    candidates = set(pairmaj_graph.keys())
    size = len(candidates)

    for size in range(1, len(candidates) + 1):
        for sub in combinations(candidates, size):
            subset = set(sub)
            out = set(candidates) - subset

            dom = True

            for member in subset:
                if not out.issubset(pairmaj_graph[member]):
                    dom = False
                    break

            if dom:
                return sorted(subset)

    return []


def smith_set_from_rcv(rcv_ballots: pl.DataFrame) -> list:
    """
    Compute the Smith set from a Ranked-Choice ballot.

    The Smith set is the minimal set of candidates which can beat all others pairwise -
    if there is a single winner in the set they are guaranteed the Condorcet i.e. Majority winner.

    parameters
    ---
    df : pl.DataFrame
        A Polars DataFrame representing ballots. Each column is a candidate and each
        row is is a voter's ranking of the candidates. Lower numbers indicate higher
        preference (1 = top-choice).

    returns
    ---
    smith_set : list
        A list of the Smith set candidates - all are equally good winners;
        ordering is determined lexicographically. If there is a Condorcet winner
        (single Majority winner), the Smith set will contain that single candidate.

    """

    return smith_set_brutefrom_pairmaj(pairmaj_from_rcv(rcv_ballots))


def smith_set(df: pl.DataFrame, ballotkind="rcv") -> list:
    if ballotkind == "rcv":
        return smith_set_from_rcv(df)
    else:
        raise NotImplementedError(
            f"`smith_set` ballotkind={ballotkind} is not implemented."
        )
