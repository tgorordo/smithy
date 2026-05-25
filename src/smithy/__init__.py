import polars as pl
import rustworkx as rwx
from itertools import combinations

from .rcv import pmg_from_rcv


def ss_from_pmg(pmg: rwx.PyDiGraph) -> list[str]:
    """
    Find the Smith set from a pairwise majority graph.

    parameters
    ---
    pmg: rwx.PyDiGraph
        A graph whose nodes correspond to candidates and (directed) edges show
        which candidates they beat pairwise.

    returns
    ---
    smith_set: list
        A list of the Smith set candidates - all are equally good winners;
        ordering is determined lexicographically. If there is a Condorcet winner
        (single Majority winner), the Smith set will contain that single candidate.
    """

    sccs = rwx.strongly_connected_components(pmg)

    cg = rwx.condensation(pmg, sccs)

    src_sccs = [nd for nd in cg.node_indices() if cg.in_degree(nd) == 0]

    smith_set = sorted([c for scc in src_sccs for c in cg[scc]])

    return smith_set


def smith_set_from_rcv(ballots: pl.DataFrame) -> list:
    """
    Compute the Smith set from a Ranked-Choice ballot.

    The Smith set is the minimal set of candidates which can beat all others pairwise -
    if there is a single winner in the set they are guaranteed the Condorcet i.e. Majority winner.

    parameters
    ---
    ballots : pl.DataFrame
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

    # return smith_set_brutefrom_pairmaj(pairmaj_from_rcv(rcv_ballots))
    return ss_from_pmg(pmg_from_rcv(ballots))


def smith_set(df: pl.DataFrame, ballotkind="rcv") -> list:
    if ballotkind == "rcv":
        return smith_set_from_rcv(df)
    else:
        raise NotImplementedError(
            f"`smith_set` ballotkind={ballotkind} is not implemented."
        )
